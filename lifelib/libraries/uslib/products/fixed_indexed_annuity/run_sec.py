"""Run the FIA_US_SEC model and print a model point's account value, rider and cash flows.

    python products/fixed_indexed_annuity/run_sec.py          # point 1, in force 84 months
    python products/fixed_indexed_annuity/run_sec.py 14       # the anchor, depleted
    python products/fixed_indexed_annuity/run_sec.py --block  # the block, row by row

``t`` counts months from the valuation date, which is the same instant for every model
point, so row ``t`` of one point's frame is the same month as row ``t`` of any other's, and
a block is the frames summed row by row. Point 1 is the worked example's anchor in force at
anniversary 7: its row ``t = 11`` is the worked example's policy month 95, the anniversary
closing contract year 8, where its first lifetime withdrawal is taken.

The contract is annual on a monthly grid, so the account value and rider traces are
printed at the anniversary months, those where ``duration_mth(t) % 12 == 11``, and the cash
flows are printed month by month for the first year and summed into contract years by
``result_cf_annual()``.

Points are named by their ``point_id``. The runner looks each one up in ``Projection`` the
way the model indexes it, by the label itself or, on a model indexed by position, by its
position in the table, so it runs unchanged once the model is compiled.

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
if args not in ([], ["--block"]) and not (len(args) == 1 and args[0].isdigit()):
    sys.exit(USAGE)

model = mx.read_model(Path(__file__).parent / "FIA_US_SEC")
table = model.Data.model_point_table()
position = {label: i for i, label in enumerate(table.index)}


def key(label):
    """The key that selects point ``label`` in ``Projection``."""
    return position[label] if model.Projection.parameters == ("idx",) else label


def months(n):
    """``n`` with its unit: "1 month", "15 months"."""
    return "{} month{}".format(n, "" if n == 1 else "s")


def release(label):
    """Drop a point's ItemSpace once read, and collect it (see the module docstring)."""
    del model.Projection[key(label)]
    gc.collect()


def phase_label(proj, t):
    """The label ``result_glwb()`` gives the phase of month ``t``."""
    return proj.result_glwb()["phase"].iloc[t]


def describe(proj):
    """One line on where the point stands at the valuation date."""
    d = proj.duration_mth_init()
    if d < 0:
        return "to be issued at t = {}, {} after the valuation date".format(-d, months(-d))
    if d == 0:
        return "issued at the valuation date, t = 0"
    return ("in force {}: contract year {}, attained age {}, {:.6f} in force, "
            "AV {:,.2f} per contract, phase {} in month 0".format(
                months(d), proj.policy_year(0), proj.age(0), proj.pols_if(0),
                proj.av_pp_init(), phase_label(proj, 0)))


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
    if m:
        return " (S's {}, in force at its month {})".format(source, m)
    return " (S's {})".format(source)


def events(proj, anniversaries):
    """The first lifetime withdrawal and the account value running out.

    Each in the frame, or before the valuation date on a point in force that opens
    month 0 in income, or with no account value left, as the depleted anchor does.
    """
    exercise = [t for t in anniversaries if proj.is_exercise(t)]
    glwb = proj.result_glwb()["phase"]
    out = [t for t in anniversaries if glwb.iloc[t] in ("DEPLETED", "TERMINATED")]
    in_force = proj.duration_mth_init() > 0
    if exercise:
        first = "in contract year {}, at t = {}".format(proj.policy_year(exercise[0]),
                                                       exercise[0])
    elif in_force and glwb.iloc[0] in ("INCOME", "DEPLETED"):
        first = "before the valuation date"
    else:
        first = "not in the frame"
    if in_force and proj.av_pp_init() == 0.0:
        empty = "before the valuation date"
    elif out:
        empty = "in contract year {}, at t = {} ({})".format(
            proj.policy_year(out[0]), out[0], glwb.iloc[out[0]])
    else:
        empty = "not in the frame"
    return "first lifetime withdrawal {}; account value runs out {}".format(first, empty)


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
    label = int(args[0]) if args else 1
    if label not in position:
        sys.exit("no model point {} in the table: {}".format(label, list(position)))
    proj = model.Projection[key(label)]
    print("model point {}: {}{} - {}{} {} premium {:,.0f}, bonus {:.0%}, {} indexed".format(
        label, table.at[label, "policy_id"], origin(label), proj.sex(),
        proj.age_at_entry(), proj.tax_status(), proj.premium_pp(), proj.bonus_rate(),
        "{:.0%}".format(proj.alloc_indexed())))
    print("GLWB {}  basis {}  income from age {}  utilization {:.0%}  "
          "cap {:.2%}  rollup {}  stack {:.2f}x".format(
              "elected" if proj.glwb_elected() else "not elected", proj.glwb_basis(),
              proj.income_start_age(), proj.utilization_intensity(),
              proj.cap_rate_in_force(), proj.rollup_id(), proj.stack_factor()))
    print("at the valuation date: {}".format(describe(proj)))
    n = proj.proj_len()
    print("proj_len = {} from the valuation date (t = 0..{}); cover ends at policy month "
          "{}, the anniversary at attained age {}".format(
              months(n), n - 1, proj.maturity_mth(),
              proj.age_at_entry() + proj.policy_term()))
    anniversaries = [t for t in range(proj.t_entry(), n) if proj.is_anniv(t)]
    print(events(proj, anniversaries))
    print("every contractual event falls in an anniversary month, where "
          "duration_mth(t) % 12 == 11; the rows below are those months")
    print()
    print("account value, benefit base and lifetime withdrawal (per contract), at the")
    print("anniversaries closing the first fourteen contract years on the books:")
    cols = ["av_pp_bef_inv", "index_credit_pp", "rider_charge_pp", "wd_pp", "av_pp",
            "mgsv_pp"]
    av = proj.result_av().loc[anniversaries[:14], cols]
    bb = proj.result_glwb().loc[anniversaries[:14], ["benefit_base_pp", "lw_pp", "phase"]]
    print(av.join(bb).round(2).to_string())
    print()
    print("cash flows, t = 0..11 (months from the valuation date):")
    print(proj.result_cf().head(12).round(2).to_string())
    print()
    print("cash flows, summed into contract years (months in cover only):")
    print(proj.result_cf_annual().head(14).round(2).to_string())

model.close()
gc.unfreeze()
