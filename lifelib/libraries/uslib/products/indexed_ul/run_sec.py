"""Run the IUL_US_SEC model and print a model point's cash flows, or the block's.

    python products/indexed_ul/run_sec.py          # point 1: S point 1, issued now
    python products/indexed_ul/run_sec.py 7        # S point 4 in force 65 months
    python products/indexed_ul/run_sec.py --block  # every model point, row by row

Point 7 is in force 65 months at the valuation date with all twelve index segments live,
carried in from the segment ladder, so its rows show the segments it brings in maturing
one a month and their credits reaching the account value.  ``t`` counts months from the
valuation date, which is the same instant for every model point, so row ``t`` of one
point's frame is the same month as row ``t`` of any other's, and a block is the frames
summed row by row.  A point is named by its ``point_id``, and ``Projection`` is indexed
through a key that follows its parameter, the label here and the position once the model
compiles, so the runner reads the same at both stages.

Output is ASCII-only so it prints on a Windows console under any code page.
"""
import gc
import sys
from pathlib import Path

import modelx as mx
import pandas as pd

model = mx.read_model(Path(__file__).parent / "IUL_US_SEC")
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
    live = min(proj.seg_term_mth, d)
    held = 0.0
    for k in range(1, live + 1):
        held = held + proj.seg_bal_pp_init(k)
    return ("in force {}: policy year {}, attained age {}, {:.6f} in force, "
            "account value {:,.2f}: fixed account {:,.2f}, segments of the last {} "
            "{:,.2f}, collateral {:,.2f}; loan {:,.2f}, face in force {:,.2f}, "
            "premiums paid {:,.2f}, no-lapse accumulator {:,.2f}, {}".format(
                months(d), proj.policy_year(0), proj.age(0), proj.pols_if(0),
                proj.av_pp_init(), proj.fa_pp_init(), months(live), held,
                proj.lca_pp_init(),
                proj.loan_bal_init(), proj.sum_assured_init(), proj.cum_prem_init(),
                proj.cum_prem_net_init(),
                "a MEC" if proj.is_mec_init() else "not a MEC"))


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
    # Every point's frame first.  The table and the segment ladder check themselves as
    # they are read, but whether a point is still inside the projection, withdraws less
    # than its fee, or holds one ladder row for each live segment is the product's rule,
    # which proj_len() applies, so a point past it would otherwise stop the run part-way,
    # after the points before it.
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
    print("model point {}: {}{} - {}{} {} face {:,.0f} option {} {}, premium "
          "{:,.2f}/yr {}, indexed allocation {:.0%}".format(
              label, table.at[label, "policy_id"], origin(label), proj.sex(),
              proj.age_at_entry(), proj.rate_class(), proj.sum_assured(),
              proj.db_option(), proj.premium_type(), proj.premium_pp_ann(),
              proj.premium_mode(), proj.index_alloc_rate()))
    print("at the valuation date: {}".format(describe(proj)))
    print("proj_len = {} months from the valuation date (t = 0..{}); the projection ends "
          "at policy month {}, attained age {}".format(
              proj.proj_len(), proj.proj_len() - 1, proj.maturity_mth(),
              proj.maturity_age))
    print()
    print("first 12 rows, t = 0..11 (months from the valuation date):")
    print(proj.result_cf().head(12).round(2).to_string())
    print()
    print("account value per policy, t = 0..11:")
    print(proj.result_av().head(12).round(2).to_string())
    print()
    print("segment ladder per policy, t = 0..11:")
    print(proj.result_seg().head(12).round(4).to_string())
    print()
    print("policy counts and decrement rates, t = 0..11:")
    print(proj.result_pols().head(12).round(6).to_string())

model.close()
