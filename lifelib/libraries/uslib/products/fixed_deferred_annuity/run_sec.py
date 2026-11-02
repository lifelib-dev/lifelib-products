"""Run the MYGA_US_SEC model and print a model point's account value and cash flows.

    python products/fixed_deferred_annuity/run_sec.py          # point 1, issued at t = 0
    python products/fixed_deferred_annuity/run_sec.py 8        # the anchor, a year on
    python products/fixed_deferred_annuity/run_sec.py --block  # the block, row by row

``t`` counts months from the valuation date, which is the same instant for every model
point, so row ``t`` of one point's frame is the same month as row ``t`` of any other's, and
a block is the frames summed row by row.

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

model = mx.read_model(Path(__file__).parent / "MYGA_US_SEC")
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


def describe(proj):
    """One line on where the point stands at the valuation date."""
    d = proj.duration_mth_init()
    if d < 0:
        return "to be issued at t = {}, {} after the valuation date".format(-d, months(-d))
    if d == 0:
        return "issued at the valuation date, t = 0"
    return ("in force {}: contract year {}, attained age {}, {:.6f} in force, "
            "AV {:,.2f} per contract".format(months(d), proj.policy_year(0), proj.age(0),
                                             proj.pols_if(0), proj.av_pp_init()))


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


def shock(proj):
    """The shock lapse of the first renewal year, where that year opens in the frame."""
    n = proj.guar_period()
    t = 12 * n - proj.duration_mth_init()
    if t < 0:
        return ("the first renewal year, contract year {}, opened before the valuation "
                "date".format(n + 1))
    if t >= proj.proj_len():
        return ("the first renewal year, contract year {}, falls after the deemed "
                "maturity".format(n + 1))
    return "shock lapse at contract year {}, t = {}: {:.2%} p.a.".format(
        n + 1, t, proj.lapse_rate(t))


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
    print("model point {}: {}{} - {}{} {} premium {:,.0f}, {}-year guarantee period".format(
        label, table.at[label, "policy_id"], origin(label), proj.sex(),
        proj.age_at_entry(), proj.tax_status(), proj.premium_pp(), proj.guar_period()))
    print("declared rate = {:.2%}  GMIR = {:.2%}  GMSV rate = {:.2%}  "
          "renewal = {}  MVA = {} / {}".format(
              proj.declared_rate_initial(), proj.gmir(), proj.mgsv_rate(),
              proj.renewal_architecture(), proj.mva_family(), proj.mva_cap_rule()))
    print("at the valuation date: {}".format(describe(proj)))
    print("proj_len = {} from the valuation date (t = 0..{}); deemed maturity at policy "
          "month {}, attained age 100".format(months(proj.proj_len()), proj.proj_len() - 1,
                                                proj.maturity_mth()))
    print(shock(proj))
    print()
    print("account value and Model #805 floor, t = 0..11 (per contract):")
    print(proj.result_av().iloc[:12, :5].round(2).to_string())
    print()
    print("cash flows, t = 0..11 (months from the valuation date):")
    print(proj.result_cf().head(12).round(2).to_string())

model.close()
