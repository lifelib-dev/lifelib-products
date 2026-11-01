"""Run the WholeLife_US_SEC model and print a model point's cash flows, or the block's.

    python products/whole_life/run_sec.py            # point 1: the anchor cell, in force
    python products/whole_life/run_sec.py 19         # the loan variant, in force mid-year
    python products/whole_life/run_sec.py --block    # every model point, summed row by row

``t`` counts months from the valuation date, which is the same instant for every model
point, so row ``t`` of one point's frame is the same month as row ``t`` of any other's, and
a block is the frames summed row by row.

Output is ASCII-only so it prints on a Windows console under any code page.
"""
import sys
from pathlib import Path

import modelx as mx
import pandas as pd

model = mx.read_model(Path(__file__).parent / "WholeLife_US_SEC")
table = model.Data.model_point_table()
args = sys.argv[1:]


def describe(proj):
    """One line on where the point stands at the valuation date."""
    d = proj.duration_mth_init()
    if d < 0:
        return "to be issued at t = {}, {} months after the valuation date".format(-d, -d)
    if d == 0:
        return "issued at the valuation date, t = 0"
    return ("in force {} months: policy year {}, attained age {}, {:.6f} in force, "
            "next anniversary at t = {}".format(
                d, proj.policy_year(0), proj.age(0), proj.pols_if(0), proj.anniv_mth(0)))


def origin(point_id):
    """Where the generator took the row from, where the table records it."""
    if "row_kind" not in table.columns:
        return ""
    kind, source, m = (table.at[point_id, c]
                       for c in ("row_kind", "source_policy_id", "source_mth"))
    if kind == "derived":
        return " (S's {} at its month {})".format(source, m)
    if kind == "future":
        return " (S's {}, issued {} months on)".format(source, -m)
    return " (S's {})".format(source)


if args == ["--block"]:
    # Every point's frame first.  The table checks itself as it is read, but whether a
    # point is still in cover is the product's rule, which proj_len() applies, so a point
    # past its cover would otherwise stop the run part-way, after the points before it.
    for point_id in table.index:
        model.Projection[point_id].proj_len()
        del model.Projection[point_id]
    frames = []
    print("model points, t = 0 the valuation date for each:")
    for point_id in table.index:
        proj = model.Projection[point_id]
        frames.append(proj.result_cf())
        print("  {:>2}  {:<18} {}; proj_len {}".format(
            point_id, table.at[point_id, "policy_id"], describe(proj), proj.proj_len()))
        del model.Projection[point_id]          # each point is read once, then released
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
    point_id = int(args[0]) if args else 1
    proj = model.Projection[point_id]
    print("model point {}: {}{} - {} {}{} {} face {:,.0f}, {} mode, "
          "dividend option {}".format(
              point_id, table.at[point_id, "policy_id"], origin(point_id), proj.product(),
              proj.sex(), proj.age_at_entry(), proj.risk_class(), proj.sum_assured(),
              proj.premium_mode(), proj.dividend_option()))
    print("at the valuation date: {}".format(describe(proj)))
    print("proj_len = {} months from the valuation date (t = 0..{}); maturity at policy "
          "month {}, attained age 100".format(proj.proj_len(), proj.proj_len() - 1,
                                               proj.maturity_mth()))
    print("net_cf: INCOME POSITIVE (library convention);   "
          "liability_cf = -net_cf: OUTGO POSITIVE (the technical notes' NetCF_t)")
    print()
    print("first 12 rows, t = 0..11 (months from the valuation date):")
    print(proj.result_cf().head(12).round(2).to_string())
    print()
    print("policy counts and decrement rates, t = 0..11:")
    print(proj.result_pols().head(12).round(6).to_string())

model.close()
