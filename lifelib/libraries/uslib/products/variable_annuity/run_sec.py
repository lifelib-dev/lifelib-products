"""Run VA_US_SEC and print a model point's guarantees, account value and cash flows.

    python products/variable_annuity/run_sec.py          # point 1, the anchor cell
    python products/variable_annuity/run_sec.py 2        # the worked example, in force
    python products/variable_annuity/run_sec.py --block  # the block, row by row

``t`` counts months from the valuation date, which is the same instant for every model
point, so row ``t`` of one point's frame is the same month as row ``t`` of any other's, and
a block is the frames summed row by row. Point 1 is the worked example's anchor cell
issued at the valuation date: its row ``t = 26`` is the worked example's month, the 27th
policy month. Point 2 is the worked example's carried state in force at the valuation
date with 26 policy months elapsed, so the same month is its row ``t = 0``, and the two
print the same worked-example block.

The guarantees move at the contract's own events, so the bases are printed at the
anniversary months, those where ``duration_mth(t) % 12 == 11``, and the cash flows are
printed month by month for the first year and summed into projection years,
``t // 12 + 1``, by the runner itself: ``VA_US_SEC`` publishes no annual report.

Points are named by their ``point_id``. The runner looks each one up in ``Projection`` the
way the model indexes it, by the label itself or, on a model indexed by position, by its
position in the table, and passes each timing, ``"BEF_PREM"`` or ``"BEF_FEE"``, as the
model's own Reference of the name where it defines one, the int code Phase 2 gives it, and
as the text otherwise, so it runs unchanged once the model is compiled. A label the table
does not hold, a number or not, is refused with the labels it does hold.

A block run asks every point for its frame before it projects any, because whether a point
is still in cover is the product's rule, which ``proj_len()`` applies, and a point past its
cover would otherwise stop the run part-way. It releases each point once it is read, and
collects, because a released point sits in reference cycles that only Python's cyclic
collector frees, in the pass that asks each point for its frame as in the pass that
projects it. It freezes everything alive (``gc.freeze``) before each pass, the model and
its table first, so that each collection scans only what the block has made since.

Output is ASCII-only so it prints on a Windows console under any code page.
"""
import gc
import sys
from pathlib import Path

import modelx as mx
import pandas as pd

USAGE = "usage: python run_sec.py [point_id | --block]"

args = sys.argv[1:]
if len(args) > 1 or args[:1] in (["--help"], ["-h"]):
    sys.exit(USAGE)

model = mx.read_model(Path(__file__).parent / "VA_US_SEC")
table = model.Data.model_point_table()
position = {label: i for i, label in enumerate(table.index)}


def key(label):
    """The key that selects point ``label`` in ``Projection``."""
    return position[label] if model.Projection.parameters == ("idx",) else label


def code(label):
    """The argument that stands for timing ``label``: the model's own int Reference named
    ``label`` where it defines one, as Phase 2 does, and the text otherwise."""
    value = model.Projection.refs.get(label)
    return value if isinstance(value, int) and not isinstance(value, bool) else label


def months(n):
    """``n`` with its unit: "1 month", "15 months"."""
    return "{} month{}".format(n, "" if n == 1 else "s")


def release(label):
    """Drop a point's ItemSpace once read, and collect it (see the module docstring)."""
    del model.Projection[key(label)]
    gc.collect()


def describe(proj):
    """One line on where the point stands at the valuation date."""
    d = proj.duration_mth_init()
    if d < 0:
        return "to be issued at t = {}, {} after the valuation date".format(-d, months(-d))
    if d == 0:
        return "issued at the valuation date, t = 0"
    return ("in force {}: contract year {}, attained age {}, {:.6f} in force, "
            "AV {:,.2f} per contract{}".format(
                months(d), proj.policy_year(0), proj.age(0), proj.pols_if(0),
                proj.av_pp_init(), ", depleted" if proj.depleted_open(0) else ""))


def origin(label):
    """Where the generator took the row from, where the table records it."""
    if "row_kind" not in table.columns:
        return ""
    kind, source, m = (table.at[label, c]
                       for c in ("row_kind", "source_policy_id", "source_mth"))
    if kind == "derived":
        return " (S's {} at its month {})".format(source, m)
    if kind == "future":
        return " (S's {}, issued {} on)".format(source, months(-m))
    return " (S's {})".format(source)


def events(proj, n):
    """The first withdrawal and the account value running out.

    Each in the frame, or before the valuation date on a point in force that has already
    withdrawn, or whose account value is already exhausted.
    """
    first = [t for t in range(proj.t_entry(), n) if proj.is_first_wd(t)]
    empty = [t for t in range(proj.t_entry(), n) if proj.depleted_flag(t)]
    if first:
        wd = "in contract year {}, at t = {}".format(proj.policy_year(first[0]), first[0])
    elif proj.has_wd_init():
        wd = "before the valuation date"
    else:
        wd = "not in the frame"
    if proj.depleted_open(proj.t_entry()):
        out = "before the valuation date"
    elif empty:
        out = "in contract year {}, at t = {}".format(proj.policy_year(empty[0]),
                                                     empty[0])
    else:
        out = "not in the frame"
    return "first withdrawal {}; account value runs out {}".format(wd, out)


if args == ["--block"]:
    gc.freeze()
    rows = {}
    for label in table.index:
        rows[label] = model.Projection[key(label)].proj_len()
        release(label)
    gc.freeze()
    frames = []
    print("model points, t = 0 the valuation date for each:")
    for label in table.index:
        proj = model.Projection[key(label)]
        frames.append(proj.result_cf())
        print("  {:>2}  {:<16} {}; proj_len {}".format(
            label, table.at[label, "policy_id"], describe(proj), rows[label]))
        del proj
        release(label)                          # each point is read once, then released
    block = pd.concat(frames).groupby(level="t").sum()
    print()
    print("the block, first 12 rows, t = 0..11 (months from the valuation date):")
    print(block.head(12).round(2).to_string())
    print()
    print("the block summed into projection years 1-12, year = t // 12 + 1:")
    years = pd.Index(block.index // 12 + 1, name="proj_year")
    annual = block.drop(columns="pols_if").groupby(years).sum()
    annual.insert(0, "pols_if", block["pols_if"].groupby(years).first())
    print(annual.head(12).round(2).to_string())
else:
    try:
        label = int(args[0]) if args else 1
    except ValueError:      # not a number, so no point_id: refused below, by name
        label = args[0]
    if label not in position:
        sys.exit("no model point {} in the table: {}".format(label, list(position)))
    proj = model.Projection[key(label)]
    entry = proj.t_entry()
    print("model point {}: {}{} - {}{} {} {} life, premium {:,.0f}".format(
        label, table.at[label, "policy_id"], origin(label), proj.sex(),
        proj.age_at_entry(), proj.tax_status(), proj.designated_lives(),
        proj.premium_single()))
    print("GLWB {} at {:.2%} of GWB, bonus {:.2%}, step-up on {}; GMDB {} at {:.2%} of RB"
          .format(proj.glwb_option(), proj.phi_glwb(entry), proj.bonus_pct,
                  proj.stepup_basis(), proj.gmdb_option(), proj.phi_gmdb(entry)))
    print("For Life Guarantee {}; GLWB activates at age {} at {:.0%} of GAWA".format(
        "in effect" if proj.forlife_flag() else "not in effect", proj.wd_start_age(),
        proj.wd_intensity()))
    print("at the valuation date: {}".format(describe(proj)))
    n = proj.proj_len()
    print("proj_len = {} from the valuation date (t = 0..{}); cover ends at policy month "
          "{}, attained age {}".format(months(n), n - 1, proj.maturity_mth(),
                                       proj.omega_age))
    print(events(proj, n))
    print()

    worked = proj.t_of_month(26)          # the 27th policy month, 26 months elapsed
    if entry <= worked < n:
        print("worked-example month (the 27th policy month, t = {}), per contract:".format(
            worked))
        print("  BOM subaccounts    {:>12,.2f} {:>12,.2f}   total {:>12,.2f}".format(
            proj.sa_pp_at(worked, 1, code("BEF_PREM")),
            proj.sa_pp_at(worked, 2, code("BEF_PREM")),
            proj.av_pp_at(worked, code("BEF_PREM"))))
        print("  after growth       {:>12,.2f} {:>12,.2f}   total {:>12,.2f}".format(
            proj.sa_pp_at(worked, 1, code("BEF_FEE")),
            proj.sa_pp_at(worked, 2, code("BEF_FEE")),
            proj.av_pp_at(worked, code("BEF_FEE"))))
        print("  rider fees         GLWB {:>9,.2f}   GMDB {:>9,.2f}   total {:>12,.2f}"
              .format(proj.fee_glwb_pp(worked), proj.fee_gmdb_pp(worked),
                      proj.charge_pp(worked)))
        print("  EOM subaccounts    {:>12,.2f} {:>12,.2f}   total {:>12,.2f}".format(
            proj.sa_pp(worked, 1), proj.sa_pp(worked, 2), proj.av_pp(worked)))
        print("  GMDB test          DB {:>12,.2f}   guarantee claim {:>10,.2f}".format(
            proj.db_pp(worked), proj.gmdb_claim_pp(worked)))
        print("  guarantee bases    GWB {:>11,.2f}   BB {:>11,.2f}   GAWA {:>9,.2f}   "
              "RB {:>11,.2f}".format(proj.gwb_pp(worked), proj.bb_pp(worked),
                                    proj.gawa_pp(worked), proj.rb_pp(worked)))
        print()

    anniversaries = [t for t in range(entry, n) if proj.duration_mth(t) % 12 == 11]
    print("guarantee bases and account value (per contract), at the anniversary months")
    print("closing the first fourteen contract years on the books, duration_mth(t) % 12 "
          "== 11:")
    bases = proj.result_bases().loc[anniversaries[:14],
                                    ["gwb_pp", "gawa_pp", "bb_pp", "rb_pp", "adj_pp",
                                     "db_pp"]]
    av = proj.result_av().loc[anniversaries[:14], ["av_pp"]]
    print(bases.join(av).round(2).to_string())
    print()
    print("cash flows, t = 0..11 (months from the valuation date):")
    cf = proj.result_cf()
    print(cf.head(12).round(2).to_string())
    print()
    print("cash flows summed into projection years 1-14, year = t // 12 + 1:")
    years = pd.Index(cf.index // 12 + 1, name="proj_year")
    annual = cf.drop(columns="pols_if").groupby(years).sum()
    annual.insert(0, "pols_if", cf["pols_if"].groupby(years).first())
    print(annual.head(14).round(2).to_string())

model.close()
gc.unfreeze()
