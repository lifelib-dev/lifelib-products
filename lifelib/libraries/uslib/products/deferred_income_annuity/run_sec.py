"""Run the DIA_US_SEC model and print a model point's cash flows, or the block's.

    python products/deferred_income_annuity/run_sec.py           # point 1: the anchor cell
    python products/deferred_income_annuity/run_sec.py 19        # the anchor, in payout
    python products/deferred_income_annuity/run_sec.py --block   # every model point, summed

``t`` counts months from the valuation date, which is the same instant for every model
point, so row ``t`` of one point's frame is the same month as row ``t`` of any other's, and
a block is the frames summed row by row.  Points are named by their ``point_id``, and the
runner maps each to its ``Projection`` key once, so that it reads the same once the model
is indexed by position.

The shipped table is a set of test cases, not a block valued at one date.  Mortality
improvement is dated by calendar year, from each contract's issue year, and every row keeps
the issue year of the S point it was taken from, 2026.  So the twins stand in 2026 at
``t = 0``, a row restated in force ``d`` months stands ``d`` months later, and the row
issued 13 months after the valuation date stands 13 months earlier: ``--block`` adds points
valued at different calendar dates, which shows how frames add and nothing more.  A real
block carries each contract's actual issue year, and its points then share one valuation
date.

A block run asks every point for its frame first, then projects each, and releases each
point's ItemSpace once read and collects it, so that it holds one point's cells at a time.
It freezes everything alive once the model and its table are read (``gc.freeze``), and
again before the projections, so that each collection scans only what the run has made
since.

Output is ASCII-only so it prints on a Windows console under any code page.
"""
import gc
import sys
from pathlib import Path

import modelx as mx
import pandas as pd

model = mx.read_model(Path(__file__).parent / "DIA_US_SEC")
table = model.Data.model_point_table()
args = sys.argv[1:]
position = {label: i for i, label in enumerate(table.index)}
by_position = tuple(model.Projection.parameters or ()) == ("idx",)


def key(label):
    """The ``Projection`` key of the point labelled ``label``.

    The label itself while ``Projection`` is keyed by ``point_id``, and the point's position
    once the model is compiled.
    """
    return position[label] if by_position else label


def release(label):
    """Drop a point's ItemSpace once read, and collect what it held."""
    del model.Projection[key(label)]
    gc.collect()


def rows_shown(n, most):
    """What a heading says of the rows printed from a frame of ``n``: at most ``most``."""
    if n == 1:
        return "the one row, t = 0"
    if n <= most:
        return "all {} rows, t = 0..{}".format(n, n - 1)
    return "first {} rows, t = 0..{}".format(most, most - 1)


def shown(df):
    """A frame rounded for printing, with no negative zero: before a point is issued, and
    after a contract ends, ``net_cf = -liability_cf`` is -0.0, which equals 0."""
    return (df.round(2) + 0.0).to_string()


def lives(proj):
    """The covered lives at issue, ``F60 + M63``, as run.py prints them."""
    text = "{}{}".format(proj.sex(1), proj.age_at_entry(1))
    if proj.is_joint():
        text += " + {}{}".format(proj.sex(2), proj.age_at_entry(2))
    return text


def premiums_due(proj):
    """The premiums still due at the valuation date, by policy month, or ``none``."""
    due = proj.premium_by_mth()
    if not due:
        return "none"
    return ", ".join("{:,.0f} at month {}".format(due[k], k) for k in sorted(due))


def describe(proj):
    """One line on where the point stands at the valuation date."""
    d = proj.duration_mth_init()
    if d < 0:
        return "to be issued at t = {}, {} months after the valuation date".format(-d, -d)
    if d == 0:
        return "issued at the valuation date, t = 0"
    alive = "{:.6g}".format(proj.lives_if_init(1))
    if proj.is_joint():
        alive += " and {:.6g}".format(proj.lives_if_init(2))
    start = proj.income_start_mth()
    if d < start:
        return ("in deferral {} month{}: policy year {}, lives {} alive, premiums paid "
                "{:,.0f}, income bought {:,.2f}/yr, the income starts at t = {}".format(
                    d, "" if d == 1 else "s", proj.policy_year(0), alive,
                    proj.cum_premium_pp_init(), proj.annual_income_init(), start - d))
    paid, left = d - start, max(start + proj.certain_mths_eff() - d, 0)
    return ("in payout {} month{}: policy year {}, lives {} alive, income {:,.2f}/yr, {} "
            "certain month{} left".format(
                paid, "" if paid == 1 else "s", proj.policy_year(0), alive,
                proj.annual_income_init(), left, "" if left == 1 else "s"))


def origin(label):
    """Where the generator took the row from, where the table records it."""
    if "row_kind" not in table.columns:
        return ""
    kind, source, m = (table.at[label, c]
                       for c in ("row_kind", "source_policy_id", "source_mth"))
    if kind == "derived":
        return " (S's {} at its month {})".format(source, m)
    if kind == "future":
        return " (S's {}, issued {} months on)".format(source, -m)
    return " (S's {})".format(source)


if args == ["--block"]:
    gc.freeze()
    # Every point's frame first.  The table and the premium schedule check themselves as
    # they are read, but whether a point still owes a payment is the product's rule, which
    # proj_len() applies, so a point owing nothing would otherwise stop the run part-way,
    # after the points before it.  A refusal names the point by its label.
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
    print("the block, {} (months from the valuation date):".format(
        rows_shown(len(block), 15)))
    print(shown(block.head(15)))
    print()
    years = pd.Index(block.index // 12 + 1, name="proj_year")
    annual = block.drop(columns="pols_if").groupby(years).sum()
    annual.insert(0, "pols_if", block["pols_if"].groupby(years).first())
    last = min(len(annual), 12)
    print("the block summed into projection year{}, year = t // 12 + 1:".format(
        " 1" if last == 1 else "s 1-{}".format(last)))
    print(shown(annual.head(12)))
else:
    label = int(args[0]) if args else 1
    if label not in position:
        sys.exit("no model point {} in the table: {}".format(label, list(position)))
    proj = model.Projection[key(label)]
    start = proj.income_start_mth()
    print("model point {}: {}{} - {} {} {} - premiums due {}".format(
        label, table.at[label, "policy_id"], origin(label), proj.market_type(),
        proj.income_form(), lives(proj), premiums_due(proj)))
    print("deferral DB = {}   income starts at policy month {} (attained age {})   "
          "m = {} in {}   COLA = {:.0%}".format(
              proj.db_form(), start, proj.age_at_entry(1) + start // 12,
              proj.payment_freq(), proj.payment_timing(), proj.cola_rate()))
    print("at the valuation date: {}".format(describe(proj)))
    n = proj.proj_len()
    print("proj_len = {} month{} from the valuation date (t = 0..{}); the stop rule at "
          "policy month {}".format(n, "" if n == 1 else "s", n - 1, proj.stop_mth()))
    income = proj.annual_income_payout()
    print("pricing factors = {}   CP(T) = {:,.0f}   B = {:,.2f}/yr = {:,.2f}/instalment   "
          "guarantee = {:.4f} yrs ({} certain months)".format(
              proj.factor_basis(), proj.cum_premium_payout(), income,
              income / proj.payment_freq(), proj.guarantee_yrs(),
              proj.certain_mths_eff()))
    if proj.is_qlac():
        flags = proj.qlac_flags()
        print("QLAC: room at t = {} {:,.0f}   compliance {}".format(
            proj.t_entry(), proj.qlac_room(proj.t_entry()),
            "OK" if not flags else "; ".join(flags)))
    print("net_cf: INCOME POSITIVE (library convention);   "
          "liability_cf = -net_cf: OUTGO POSITIVE")
    print()
    print("{} (months from the valuation date):".format(rows_shown(n, 15)))
    print(shown(proj.result_cf().head(15)))
    print()
    print("counts, survival and payment factors, {}:".format(rows_shown(n, 15)))
    print((proj.result_pols().head(15).round(6) + 0.0).to_string())
    print()
    annual = proj.result_annual()
    first = int(annual.index[0])
    print("annual display grid, policy years {}-{} (the technical notes' worked-example "
          "table, from the valuation date's policy year):".format(
              first, int(annual.index[min(len(annual), 25) - 1])))
    print(annual.head(25).round(2).to_string())
    lo = start - 2 - proj.duration_mth_init()
    if lo >= 0:
        print()
        print("monthly cash flows around the income start date, t = {} to {} (policy "
              "months {} to {}):".format(lo, lo + 5, start - 2, start + 3))
        print(shown(proj.result_cf().loc[lo:lo + 5]))

model.close()
