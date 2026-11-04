"""Run the RILA_US_SEC model and print a model point's interim values and cash flows.

    python products/registered_index_linked_annuity/run_sec.py          # point 1
    python products/registered_index_linked_annuity/run_sec.py 16       # in force 71 months
    python products/registered_index_linked_annuity/run_sec.py --block  # the block

``t`` counts months from the valuation date, which is the same instant for every model
point, so row ``t`` of one point's frame is the same month as row ``t`` of any other's, and
a block is the frames summed row by row. On point 1, issued at the valuation date, every
number is the one ``run.py`` prints for ``RILA_US_S``'s point 1; on point 16, the same
contract in force 71 months, row ``t = 0`` is ``RILA_US_S``'s month 71, the worked
example's Term End Date at +40%.

Points are named by their ``point_id``. The runner looks each one up in ``Projection`` the
way the model indexes it, by the label itself or, on a model indexed by position, by its
position in the table, so it runs unchanged once the model is compiled.

The shipped table is a set of test cases, not a block valued at one date: each row
restated in force runs on its own copy of its scenario, re-based to its month, so
``--block`` adds points whose markets differ, which shows how frames add and nothing more.

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

model = mx.read_model(Path(__file__).parent / "RILA_US_SEC")
table = model.Data.model_point_table()
position = {label: i for i, label in enumerate(table.index)}


def key(label):
    """The key that selects point ``label`` in ``Projection``."""
    return position[label] if model.Projection.parameters == ("idx",) else label


def months(n):
    """``n`` with its unit: "1 month", "15 months"."""
    return "{} month{}".format(n, "" if n == 1 else "s")


def rows_shown(n, most):
    """What a heading says of the rows printed from a frame of ``n``: at most ``most``."""
    if n == 1:
        return "the one row, t = 0"
    if n <= most:
        return "all {} rows, t = 0..{}".format(n, n - 1)
    return "first {} rows, t = 0..{}".format(most, most - 1)


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
            "AV {:,.2f} per contract".format(months(d), proj.duration(0) + 1, proj.age(0),
                                             proj.pols_if(0), proj.av_pp_init()))


def crediting(proj, t):
    """The rate the option in force at month ``t`` credits at: its cap, step or edge."""
    if proj.is_step_crediting():
        return "step rate {:.2%}".format(proj.step_rate(t))
    if proj.is_edge_crediting():
        return "edge rate {:.2%}".format(proj.edge_rate(t))
    cap = proj.cap_rate(t)
    return "uncapped" if cap == float("inf") else "cap {:.2%}".format(cap)


def term_under_way(proj):
    """Where the term in force in the point's first month on the books started."""
    t = proj.t_entry()
    d = proj.duration_mth_init()
    start, level = proj.term_start_month(t), proj.index_at_term_start(t)
    if start < d:
        began = ("began at policy month {}, {} before the valuation date: I_s = {:.2f} "
                 "from the model point".format(start, months(d - start), level))
    else:
        began = ("starts at policy month {}, t = {}: I_s = {:.2f} from the "
                 "scenario".format(start, t, level))
    return "{}, {}".format(began, crediting(proj, t))


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


def iv_rows(proj):
    """The months the decomposition prints: the first on the books, its first
    anniversary, its first term midpoint and its first two Term End Dates."""
    frame = range(proj.t_entry(), proj.proj_len())
    anniv = [t for t in frame if proj.is_anniv(t)][:1]
    mid = [t for t in frame if proj.tau(t) == proj.term_years() / 2.0][:1]
    ends = [t for t in frame if proj.is_term_end(t)][:2]
    return sorted(set([proj.t_entry()] + anniv + mid + ends))


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
        print("  {:>2}  {:<17} {}; proj_len {}".format(
            label, table.at[label, "policy_id"], describe(proj), rows[label]))
        del proj
        release(label)                          # each point is read once, then released
    block = pd.concat(frames).groupby(level="t").sum()
    print()
    print("the block, {} (months from the valuation date):".format(
        rows_shown(len(block), 12)))
    print(block.head(12).round(2).to_string())
    print()
    years = pd.Index(block.index // 12 + 1, name="proj_year")
    annual = block.drop(columns="pols_if").groupby(years).sum()
    annual.insert(0, "pols_if", block["pols_if"].groupby(years).first())
    last = min(len(annual), 12)
    print("the block summed into projection year{}, year = t // 12 + 1:".format(
        " 1" if last == 1 else "s 1-{}".format(last)))
    print(annual.head(12).round(2).to_string())
else:
    label = int(args[0]) if args else 1
    if label not in position:
        sys.exit("no model point {} in the table: {}".format(label, list(position)))
    proj = model.Projection[key(label)]
    print("model point {}: {}{} - {}{} premium {:,.0f}, one {}-year {} option, "
          "buffer {:.0%}".format(
              label, table.at[label, "policy_id"], origin(label), proj.sex(),
              proj.age_at_entry(), proj.premium_pp(), proj.term_years(),
              proj.crediting_type(), proj.buffer()))
    print("interim value family = {} / {}   scenario = {}".format(
        proj.iv_family(), proj.amort_rule(), proj.scenario_id()))
    print("at the valuation date: {}".format(describe(proj)))
    print("term under way: {}".format(term_under_way(proj)))
    n = proj.proj_len()
    print("proj_len = {} from the valuation date (t = 0..{}); the Maturity Date closes "
          "policy month {}, at attained age {}".format(
              months(n), n - 1, proj.maturity_mth() - 1,
              proj.age_at_entry() + proj.policy_term()))
    # The budget is a share of the notional, struck at the term's start; on a term begun
    # before the valuation date the notional entering t_entry() is no longer the one it
    # opened on, a withdrawal since having reduced it, so the amounts are said to be on it.
    t = proj.t_entry()
    notional, beta = proj.inv_amt_basis_pp(t), proj.opt_budget(t)
    print("option budget of the term in force at t = {}: beta = {:.4%}, {:,.2f} on the "
          "notional entering that month, {:,.2f}; the fixed leg {:,.2f}, accreting at "
          "{:.4%}, a {:.2%} spread".format(
              t, beta, beta * notional, notional, notional * (1 - beta),
              proj.fixed_leg_yield(t), proj.nge_spread_implied(t)))
    print()
    print("interim value decomposition in the first month on the books, the first month "
          "ending on an anniversary, the first term midpoint and the first term ends:")
    print(proj.result_iv().loc[iv_rows(proj)].round(2).to_string())
    print()
    print("cash flows, {} (months from the valuation date):".format(rows_shown(n, 12)))
    print(proj.result_cf().head(12).round(2).to_string())

model.close()
