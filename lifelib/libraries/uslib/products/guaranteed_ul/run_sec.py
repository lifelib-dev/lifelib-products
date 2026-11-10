"""Run the ULSG_US_SEC model and print a model point's cash flows, or the block's.

    python products/guaranteed_ul/run_sec.py          # point 1: the worked example
    python products/guaranteed_ul/run_sec.py 5        # S point 1 at 81, in its grace
    python products/guaranteed_ul/run_sec.py --block  # every model point, row by row

Point 1 is in force 300 months at the valuation date, so its rows ``t = 0..4`` are the
worked example's five months.  ``t`` counts months from the valuation date, which is the
same instant for every model point, so row ``t`` of one point's frame is the same month as
row ``t`` of any other's, and a block is the frames summed row by row.  A point is named by
its ``point_id``, and ``Projection`` is indexed through a key that follows its parameter,
the label here and the position once the model compiles, so the runner reads the same at
both stages.

Output is ASCII-only so it prints on a Windows console under any code page.
"""
import gc
import sys
from pathlib import Path

import modelx as mx
import pandas as pd

model = mx.read_model(Path(__file__).parent / "ULSG_US_SEC")
table = model.Data.model_point_table()
position = {label: i for i, label in enumerate(table.index)}
by_position = model.Projection.parameters == ("idx",)
key = {label: (position[label] if by_position else label) for label in table.index}
args = sys.argv[1:]


def months(n):
    """``n`` with its unit: "1 month", "25 months"."""
    return "{} month{}".format(n, "" if n == 1 else "s")


def release(label):
    """Drop a point's ItemSpace once read, and collect it."""
    del model.Projection[key[label]]
    gc.collect()


def describe(proj):
    """One line on where the point stands at the valuation date."""
    d = proj.duration_mth_init()
    if d < 0:
        return "to be issued at t = {}, {} after the valuation date".format(-d, months(-d))
    if d == 0:
        return "issued at the valuation date, t = 0"
    return ("in force {}: policy year {}, attained age {}, {:.6f} in force, "
            "account value {:,.2f}, shadow account {:,.2f}, loan {:,.2f}, "
            "premiums paid {:,.2f}, {} in grace".format(
                months(d), proj.policy_year(0), proj.age(0), proj.pols_if(0),
                proj.av_pp_init(), proj.sg_pp_init(), proj.loan_bal_init(),
                proj.cum_prem_init(), months(proj.grace_mth_init())))


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


if args == ["--block"]:
    # Every point's frame first.  The table checks itself as it is read, but whether a
    # point is still inside the projection, or past the end of its grace, is the product's
    # rule, which proj_len() applies, so a point past it would otherwise stop the run
    # part-way, after the points before it.
    gc.freeze()             # the model and its table, so that a collection scans a point
    lengths = {}
    for label in table.index:
        lengths[label] = model.Projection[key[label]].proj_len()
        release(label)      # collected now, or the next freeze would keep it for good
    gc.freeze()
    frames = []
    print("model points, t = 0 the valuation date for each:")
    for label in table.index:
        proj = model.Projection[key[label]]
        frames.append(proj.result_cf())
        print("  {:>2}  {:<16} {}; proj_len {}".format(
            label, table.at[label, "policy_id"], describe(proj), lengths[label]))
        del proj
        release(label)      # each point is read once, then released
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
    if label not in key:
        sys.exit(f"no model point {label} in the table: {list(key)}")
    proj = model.Projection[key[label]]
    print("model point {}: {}{} - {}{} {} face {:,.0f} guarantee to age {} {}, premium "
          "{:,.2f}/yr mode {}".format(
              label, table.at[label, "policy_id"], origin(label), proj.sex(),
              proj.age_at_entry(), proj.rate_class(), proj.sum_assured(),
              proj.guarantee_age(), proj.premium_type(), proj.premium_pp_ann(),
              proj.premium_mode()))
    print("at the valuation date: {}".format(describe(proj)))
    print("proj_len = {} months from the valuation date (t = 0..{}); the projection ends "
          "at policy month {}, attained age {}, where premiums and charges cease".format(
              proj.proj_len(), proj.proj_len() - 1, proj.charges_cease_mth(),
              proj.charges_cease_age))
    print()
    print("first 12 rows, t = 0..11 (months from the valuation date):")
    print(proj.result_cf().head(12).round(2).to_string())
    print()
    print("account value and shadow account per policy, t = 0..11:")
    print(proj.result_av().head(12).round(2).to_string())
    print()
    print("guarantee diagnostics, t = 0..11:")
    print(proj.result_guar().head(12).round(2).to_string())
    print()
    print("policy counts and decrement rates, t = 0..11:")
    print(proj.result_pols().head(12).round(6).to_string())

model.close()
