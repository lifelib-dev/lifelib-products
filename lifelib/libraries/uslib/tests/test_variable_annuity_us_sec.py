"""In-force tests for VA_US_SEC: the splice, future business, counts, regeneration.

``VA_US_SEC`` is ``VA_US_S`` taught to run in force at a valuation date
(USLIB-SEC-PLAN.md, milestone M9).  It runs on two clocks: ``t`` counts months from the
valuation date, the same month for every model point, and ``duration_mth(t)`` counts the
months the contract has been in force, ``duration_mth_init() + t``.  ``VA_US_S`` already
counts ``t`` from the valuation date, and projects its point 2 in force at 26 months, but
it opens every recursion at ``t == 0`` and keys its issue events there; this model gives
the frame its two edges, ``t_entry()`` and ``maturity_mth()``, and moves the issue events
to the issue month.  A model point may be a contract already in force at the valuation
date, in any month of its contract year, one issued at it, or one to be issued after it,
as in ``basiclife/BasicTerm_SE``.  A contract in force opens with twenty columns of state
beside its count: its two subaccount values; the seven guarantee bases, the locked GAWA%,
the Bonus Period's end and whether a withdrawal has been taken, entering month 0; the
withdrawals, the free allowance used, the dollar-for-dollar reduction and the
proportional factor of the contract year to date, and whether the year has a withdrawal;
the roll-up base at the anniversary that opened the year; the year's highest quarterly
account value before the valuation month; and the VIX fee of the last quarter to end
before it.  Its depletion takes no column: it enters a month depleted exactly where its
account value entering the month is at or below the threshold.  Both scenarios are copies
of S's re-based to the month each row is valued at, in the companions
``return_scenario_sec.csv`` and ``rate_scenario_sec.csv``.

The worked example sits on S's point 1 at ``t = 26``, the 27th policy month, and on S's
point 2, in force at 26, at ``t = 0``.  Both carry to this model unchanged, on the twins
of the two points, the second reading its scenario re-based by 26 months, ``base-M26``:
``test_the_worked_example_holds_on_the_valuation_clock`` asserts S's own goldens there,
read from ``test_variable_annuity_us.py``, with none copied.  On a point issued at the
valuation date the two clocks coincide and the model is ``VA_US_S``, and
``test_model_conventions.py`` asserts that cell by cell on the twins of S's eight
new-business points (T1), with the SEC family's other rules: every frame opens at
``t = 0``, ``pols_if`` is the ``BEF_DECR`` count, ``BEF_DECR`` is ``BEF_NB`` plus the
month's new business, new business enters once, nothing happens before issue, and the
roll-forward residuals close.  This module holds the rest of the plan's tests (its §5.2)
and the product's own facts:

* T2, the splice: an S point restated in force at month ``d``, opened with the state S
  carries into ``d``, continues S's projection from ``d`` on, in every cell of S's and in
  ``result_pols``.  S's own in-force point 2 is a splice case at offset 0, since S
  projects it from the valuation date (§5.2), its acquisition at S's ``t == 0`` apart.
  The months straddle the product's events, on S's own paths: the anniversaries of the
  Bonus Period; the worked example's month; mid-year and an anniversary before any
  withdrawal; a contract year's last month; the first withdrawal, the year to date after
  it and the dollar-for-dollar reduction; the GWB Adjustment Date; the excess withdrawal
  and the premium after it; the highest quarterly step-up and both edges of its history;
  the VIX fee's prior quarter and the CMT-linked roll-up; depletion, with and without a
  withdrawal, and the GLWB paid from the columns at a contract year's start, from the GWB
  where it is below the GAWA; and the last policy month.  Variants of S's points, in a
  copy of S's table, add premiums and withdrawals mid-year, one in a contract year's last
  month among them, a crash path, the female table, a second fund set and GAWA grid, issue
  ages 55 and 72 and either side of the roll-up rate's split, 69 and 70, a path that
  swings between quarters, a GAWA grid of 60% on a path that spikes, whose withdrawals
  take the GWB to its floors and the GAWA to the GWB, a CMT that falls mid-year below the
  year's dollar-for-dollar use, a contract not for life whose excess withdrawals run its
  GWB down to rounding about 0, which the comparison reads at the residuals' floor, two
  never-withdrawing contracts with no premium tax whose accounts run out on a rounding
  above 0 and below it, each restated the month after, and a fund set of three
  subaccounts, the third a column the generator takes from the S model it reads.  Each
  variant's twin, issued at the valuation date, is compared with S cell by cell, as a
  restated row is.  The same fixture, read again under the switched References, runs the
  bounds S ships idle: the GWB cap, at a premium after issue too, the VIX corridor's low,
  the lapse capped at 1 in the shock year and the Bonus Period's restart age, a step-up
  at it, a year past it and later.
* T3, future new business: a point issued ``k`` months after the valuation date is S's
  projection ``k`` months on, with zeros before issue, every decrement rate 0.0 there,
  and no age, year, quarter or policy month read before the contract's first.
* D11's R1, R1a and R2, and D3's clock: on the splice's rows no cell is called at a
  negative month, none evaluated on the books reads a month before them, none reads
  beyond ``t + 1`` but the one R2 admits, and no table is read at an age, a year, a
  quarter or a policy month before the books; on the committed points no recursion runs
  backward over the frame, the deepest cold call runs one cell a month, and the policy
  clock is a closed form.  The admitted read is ``lapse_wd_factor``'s: it reads whether
  the contract year has a withdrawal at the anniversary closing it, ``anniv_mth(t)``, up
  to 11 months ahead, and the rules test walks what each such read depends on, which may
  hold no count, no decrement and nothing after that anniversary.
* T4, the count algebra: the count rolls forward through new business and decrements,
  ``result_pols`` is S's report with the new business beside it, and 2.5 times the count,
  with every assumption that ships at zero switched on, is 2.5 times every flow and moves
  no per-contract value.
* T5, validation: each malformed in-force row is refused as the table is read, naming its
  point, by the one rule its case is built for (``MALFORMED``); each assumption table and
  companion whose keys or values cannot be read is refused, naming the file and the lines
  (``TABLE_FAULTS``); every refusal of ``Data``'s checks is the first refusal of some
  case; a text value no decode knows raises ``VA_US_S``'s own message in both models
  (``UNDECODABLE``); the future horizon is a Reference that bounds future business, and at
  0 refuses it; a point past its cover, or with none at all, and an opening state that a
  rule needing a ``Projection`` Reference forbids, are refused by ``proj_len()``
  (``NOT_ISSUED``), each window of months at both ends; the edges of the interface are
  accepted, each value column at the bounds of its range, each flag spelled each way
  ``Data`` reads it and an extract carried to the cent among them; and a table shortened
  below its cover is read past its end as ``VA_US_S`` reads it.
* T6, regeneration: the committed ``model_point_table_sec.csv`` and its two scenario
  companions are what the generator makes of ``VA_US_S`` and its inputs as they stand, and
  every text cell in them is S's or composed from S's keys.
* Then the product's own facts: the opening state as S carries it, each column shown on a
  committed row, the year under way read from its columns, the worked example on the
  valuation clock, depletion derived from the opening account value, the scenarios on
  the valuation clock, the transactions on the policy clock, expense inflation on the
  valuation clock, the premium and acquisition in the issue month, the lapse read at the
  anniversary, a depleted row in force, a NaN sent to the mortality and to a residual,
  the keyed readers against S's lookups, the checks' tolerance on a point of a million
  contracts, the values outside cover, the block, an in-force extract, the runner, the
  docstrings and their tables, the shared input tables and S's References, each Reference
  that ships equal to another read as itself, and what the default grid reaches.

SEC month ``t`` is S month ``t + source_mth`` throughout, the direction in which
``sec_support`` takes its ``t_offset``: ``d`` for a point restated at S month ``d``, 0 for
the twin of S's point 2, which S projects from the valuation date, and ``-k`` for one
issued ``k`` months on.

**The core grid and the full one** (USLIB-SEC-PLAN.md K6).  T2, T3 and the switched
References over every point at every month, 88, 27 and 11 cases, would take this module
to about eighteen minutes in every run.  By default they run a core chosen so that between
them they reach every branch, every opening-state column, every kind of valuation month
and every input category the full grid reaches, and bind each side of every ``min`` and
``max`` in ``Projection`` but those :data:`IDLE_SIDES` lists, which
``test_the_core_grid_reaches_every_branch`` asserts, and every line of ``Projection``'s
formulas the full grid's rows execute when swept, as line coverage of the two grids
showed when the core was last chosen: the shipped References' core runs every line its
full grid does, and the switched References' grid runs none it does not, so that core
holds the rows that reach its bounds.  Line coverage cannot tell ``>=`` from ``>``, so
each boundary of the step-up base's two reads and of the year-open roll-up base's has a
core row on each side of it.  The other cases, and the rules test's scan of their
rows, carry the ``sec_full`` marker and are skipped, with the reason shown, unless
``USLIB_SEC_FULL=1`` is set.  They are never dropped: one leg of the CI matrix sets it, so
every CI run runs the full grid, and ``USLIB_SEC_FULL=1 python -m pytest -m sec_full`` on
this module runs them alone.  Memory is the other cost: a projected point holds its
cached values and their dependency graph, so a row read once, a splice case's or a point
of a temporary copy, is released as soon as it has been read (``_release``), the
splice's rows are held one at a time, however large the grid, each S point of the splice
is released after the last case that compares with it, and the two splice fixtures, the
shipped References' and the switched ones', are one fixture that holds one of them at a
time.  The committed models, swept, are most of what the module holds, so every test that
reads a model of its own runs before those are read, never beside them, but the extract
test, which projects five rows.  The swept models the module holds are frozen out of the
collector, and the freeze is undone as the module ends.

Every test keeps five rules.  Each model is read under a name of its own and closed:
``test_variable_annuity_us.py`` reads S under its default name, and reading a model under
a name in use renames the open one.  No test writes inside the library tree: every
changed input goes through ``sec_support.temp_inputs`` into a temporary directory, because
a CSV added beside the models, even briefly, would fail a concurrent
``test_every_csv_beside_the_model_is_actually_read``.  No test indexes ``Projection`` by
hand: the keys come from ``us_registry.point_keys`` and the ItemSpaces from
``us_registry.projection``, and a generated row is found by what it is, its kind, its S
policy and its month (``_row``), so neither a renumbered table nor Phase 2's positions can
point a test at the wrong row; a table the model refuses has no keys, and a row's is taken
from the file as ``run_sec.py`` takes one (``_file_key``).  Every Reference a test changes
is set on a model read afresh, before it computes anything, because a compiled model never
clears a cache.  And a timing or a kind is passed through ``_code``, which hands the model
its own Reference where it defines one and the string otherwise, and every twin
comparison goes through ``_mismatches``, which passes the SEC Space's codes, so that the
same calls serve Phase 2's int codes.  At stage E there are none: the phase is S's text,
``PRE_ISSUE`` before issue and ``EXPIRED`` from maturity, a leaf no cell, report or check
reads, and ``codes()`` is ``{}``.  What a projection cell still compares as text is S's own
timing and kind strings, the ten decodes of the point's text columns, each comparing its
column once, and the join keys, each in the cells that read its table.
"""
import ast
import bisect
import builtins
import collections
import contextlib
import dataclasses
import gc
import inspect
import io
import itertools
import math
import os
import re
import shutil
import subprocess
import sys
import unicodedata

import modelx as mx
import numpy as np
import pandas as pd
import pytest

import test_variable_annuity_us as s_tests
from sec_support import (
    GENERATED_COLUMNS, SEC_SPECS, TWIN_EXEMPT_DEFAULT, build_sec_table, check_generated,
    codes, frame_mismatches, sweep, temp_inputs, twin_mismatches)
from us_registry import model_path, point_keys, projection

SEC, TWIN, TABLE = "VA_US_SEC", "VA_US_S", "model_point_table_sec.csv"
RETURNS, RATES = "return_scenario_sec.csv", "rate_scenario_sec.csv"
COMPANIONS = (RETURNS, RATES)
SPEC = SEC_SPECS[SEC]

# S's eight new-business points: the worked example's anchor issued at t = 0 (1) and its
# variants: the decline path that exhausts the account (3), the excess withdrawal and the
# premium after it (4), the highest quarterly step-up on the annual-ratchet GMDB (5), the
# VIX fee and the CMT-linked roll-up (6), the never-withdrawing basic death benefit on the
# quinquennial fee (7), the never-withdrawing roll-up (8) and the withdrawing basic death
# benefit (9).
S_POINTS = (1, 3, 4, 5, 6, 7, 8, 9)

# S's in-force point 2, the worked example's carried state entered at 26 months.  VA_US_S
# projects it from the valuation date, so it is a splice case at offset 0 (§5.2): its twin
# is in force 26 months at the valuation date, and SEC's t = 0 is S's t = 0.
IN_FORCE_TWINS = (("twin", 2, 0),)

# Eight more S points, in the splice's copy of S's table and never in the committed one,
# for what S's own points do not carry, each on keys of its own, so that no S value
# changes for them (§7.3, *Record — M3*):
#
# 10, the anchor on the midyear programme: a premium of 10,000 at policy month 62 and
#   withdrawals of 12,000 at 66, 3,000 at 69 and 2,000 at 83, the last month of contract
#   year 7: a premium and a withdrawal in one contract year on the roll-up death benefit,
#   whose year-open roll-up base the withdrawal reads, and withdrawals mid-year, which
#   move the lapse in the months before them;
# 11, the never-withdrawing roll-up on the crash path: an account exhausted at 56 with no
#   withdrawal, the GWB Adjustment carried to its date;
# 12, the anchor, female: the female mortality rows;
# 13, the anchor on the second fund set, 25/75: a split that moves;
# 14, the anchor on the second GAWA grid: every band of another grid;
# 15, the decline path at issue age 55: a payment not for life, and the GWB Adjustment
#   at policy year 15, where the account is exhausted before the first withdrawal;
# 16, the anchor at issue age 72: withdrawals from issue and the older roll-up rate;
# 17, the highest quarterly step-up on the hq_swing path: a highest value at a quarter
#   end before the valuation month that wins the anniversary's step-up;
# 18 and 19, the never-withdrawing basic death benefit at issue ages 55 and 56: under the
#   switched References' lower GLWB fee, a step-up raising the Bonus Base at the
#   anniversary closing policy month 311, at attained age 81 on the first, the Bonus
#   Period's restart age, which restarts it, and at 82 on the second, which does not;
# 20, the never-withdrawing roll-up at issue age 69, the last age of the younger roll-up
#   rate, on the lateprem programme: a premium of 60,000 at policy month 100, which under
#   the switched References' GWB cap meets a GWB already at the cap, 151,000, and takes
#   the Bonus Base past it;
# 21, the anchor at issue age 70, the first age of the older roll-up rate, on the
#   high_grid GAWA grid (60%), with no utilization withdrawal and the floors programme,
#   on the spike path: a withdrawal of 50,000 in its issue month, inside the limit, leaves
#   the GWB below the GAWA; the account then falls through the first year and gains 10% a
#   month in the second, so that a withdrawal inside the limit at policy month 18 is above
#   the GWB left, and an excess one at 20 has a part inside the limit above the GWB and a
#   GAWA after it above the GWB after it, each floored or capped;
# 22, the VIX fee and CMT-linked roll-up on the cmtdrop programme and path: withdrawals at
#   policy months 62, 68 and 70 and the CMT falling at 66, so that the year's
#   dollar-for-dollar use passes the allowance, which the lower rate cuts mid-year;
# 23, the anchor at issue age 59, not for life, withdrawing 130% of its limit from age 62:
#   excess withdrawals each year that run the GWB down to rounding about 0;
# 24 and 25, the never-withdrawing roll-up and basic death benefit with no premium tax, on
#   S's own premium: their accounts run out at policy months 524 and 659 on a rounding
#   about 0, above it on the first, 5.7e-15, and below it on the second, -2.3e-14, where
#   the taxed points run out on exactly 0, so that a row valued the month after opens
#   depleted on an account value that only the threshold, not 0, says is out;
# 26, the anchor on a fund set of three subaccounts, trio: a subaccount that S's shipped
#   fund table lacks, whose value column the generator takes from the S model it reads.
VARIANTS = {
    10: (1, {"policy_id": "VA-900010", "txn_id": "midyear"}),
    11: (8, {"policy_id": "VA-900011", "scenario_id": "crash"}),
    12: (1, {"policy_id": "VA-900012", "sex": "F"}),
    13: (1, {"policy_id": "VA-900013", "fund_set": "alt_25_75"}),
    14: (1, {"policy_id": "VA-900014", "glwb_option": "alt_grid"}),
    15: (3, {"policy_id": "VA-900015", "age_at_entry": 55}),
    16: (1, {"policy_id": "VA-900016", "age_at_entry": 72}),
    17: (5, {"policy_id": "VA-900017", "scenario_id": "hq_swing"}),
    18: (7, {"policy_id": "VA-900018", "age_at_entry": 55}),
    19: (7, {"policy_id": "VA-900019", "age_at_entry": 56}),
    20: (8, {"policy_id": "VA-900020", "age_at_entry": 69, "txn_id": "lateprem"}),
    21: (1, {"policy_id": "VA-900021", "age_at_entry": 70, "glwb_option": "high_grid",
             "wd_start_age": 0, "txn_id": "floors", "scenario_id": "spike"}),
    22: (6, {"policy_id": "VA-900022", "txn_id": "cmtdrop", "scenario_id": "cmtdrop"}),
    23: (1, {"policy_id": "VA-900023", "age_at_entry": 59, "wd_start_age": 62,
             "wd_intensity": 1.3}),
    24: (8, {"policy_id": "VA-900024", "premium_tax_rate": 0.0}),
    25: (7, {"policy_id": "VA-900025", "premium_tax_rate": 0.0}),
    26: (1, {"policy_id": "VA-900026", "fund_set": "trio"}),
}

# The premium tax the splice's copy of S's table charges on every point issued at its
# t = 0 but a variant that sets its own, as SEC's generated rows copy it: S ships it at 0
# on every point.
PREMIUM_TAX = 0.02

# What the splice sets in both models, S and SEC alike, before either evaluates anything.
# Expense inflation is read on the valuation clock in SEC and on the policy clock in S
# (D7): S inflates by completed contract years, so at the shipped 2.5% the expenses of a
# row opened at d differ by 1.025 ** (d // 12) and more by design, and at 0 both factors
# are 1; the clock itself is asserted on its own, at the shipped rate.  The rest are
# assumptions that ship at a value that hides some of the state from any comparison:
#   expense_acq $150 and comm_rate_acq 5%, an acquisition expense and a commission on new
#     business, with the premium tax above, all 0 as shipped;
#   gwb_adj_pct 200%, against the shipped 105%, at which the GWB Adjustment never binds:
#     the 6% bonus of every year without a withdrawal lifts the GWB past 105% of the
#     premium first.  At 200% it binds at policy month 143 on points 7 and 8, and at 179
#     on variant 15, so that the adjustment's base and its date show.
# The identity does not depend on the values, only on both models having the same ones.
SPLICED_REFS = {"inflation_rate": 0.0, "expense_acq": 150.0, "comm_rate_acq": 0.05,
                "gwb_adj_pct": 2.0}

# The switched References, beside SPLICED_REFS: the bounds S ships idle, each set where it
# binds with an effect:
#   phi_glwb_curr 0.7%, against the shipped 1.25%, which puts the VIX corridor's low,
#     0.6%, within the fee's reach on point 6 within 26 quarters, and leaves point 16's
#     account value to step its GWB up at policy month 23, after its first withdrawal,
#     raising the GAWA;
#   gwb_cap $151,000, against the shipped $10,000,000, which binds from policy month 95 on
#     points 1, 7 and 8 and from 107 on point 4;
#   lapse_rate_shock 125%, against the shipped 25%, which takes the shock year's lapse past
#     1 on points 7 and 4, where min(1.0, ...) caps it; and the lower fee's step-ups bring
#     the Bonus Period's restart age, 81, within reach: past it on point 7 from policy month
#     311, at it on variant 18 there, a year past it on variant 19.
# The GWB Adjustment stays in the main splice: under the GWB cap it would not bind.
SWITCHED_REFS = {**SPLICED_REFS, "phi_glwb_curr": 0.007, "gwb_cap": 151000.0,
                 "lapse_rate_shock": 1.25}
REFS = {"spliced": SPLICED_REFS, "switched": SWITCHED_REFS}

# The return paths the variants read, (scenario, ((t, subaccount 1, subaccount 2), ...)):
# crash, a fall of 6% and 5% a month to 60, which exhausts point 8's account at 56 with no
# withdrawal; hq_swing, gains at each contract year's start and losses from its second
# quarter, so that the year's highest quarterly value falls before an in-force row's
# valuation month and wins the anniversary's step-up; and spike, a fall of 0.5% and 0.4%
# a month through the first contract year, below the GWB, then gains of 10% and 9% a month
# through the second, which take variant 21's account above its GWB within the year.  The
# cmtdrop scenario's returns are variant's.  S's own paths are not stepped: the grid's
# months follow the events they set, the depletions among them.  And base's third
# subaccount, which only variant 26's set holds, (t, return), stepped at 30 so that a copy
# re-based to the wrong month reads another number.
TRIO_RETURNS = ((0, 0.0021), (30, 0.0035))
VARIANT_RETURNS = (
    ("crash", ((0, -0.060, -0.050), (60, 0.004, 0.0015))),
    ("hq_swing", (*((12 * y, 0.030, 0.025) for y in range(10)),
                  *((12 * y + 3, -0.020, -0.015) for y in range(10)),
                  (120, 0.004, 0.0015))),
    ("spike", ((0, -0.005, -0.004), (12, 0.100, 0.090), (24, 0.004, 0.0015))),
)

# The VIX and CMT path of the variant scenario, the one a point on the vix fee or the
# cmt_linked roll-up reads, stepped in both copies, (t, vix_sq, cmt10): S's flat path
# after month 12 would read the same level wherever a row's re-based copy started, and at
# these steps a level read a month off, or at the wrong row's month, reads another number,
# the VIX band and the corridor's high bind, and the CMT roll-up meets its floor and its
# cap.  The two new scenarios set a level at 0, which no row reads (neither is vix nor
# cmt_linked) and Data's join does not ask for.
VARIANT_RATES = ((24, 150.0, 0.020), (36, 1500.0, 0.075), (60, 1500.0, 0.072),
                 (84, 420.0, 0.035), (120, 250.0, 0.025), (180, 700.0, 0.041))

# cmtdrop's rates: variant's, stepped as above, with the CMT falling to 2.0% at policy month
# 66, between variant 22's withdrawals at 62 and 68, the VIX level held.
CMT_DROP = (66, 0.020)


def _variant_paths(table):
    """S's return scenarios with the variants' paths, each subaccount on its rows,
    cmtdrop's, a copy of variant's, and base's third subaccount (:data:`TRIO_RETURNS`)."""
    rows = [table, table[table["scenario_id"] == "variant"].assign(scenario_id="cmtdrop")]
    for scenario, path in VARIANT_RETURNS:
        for t, first, second in path:
            rows.append(pd.DataFrame([(scenario, 1, t, first, "a test"),
                                      (scenario, 2, t, second, "a test")],
                                     columns=table.columns))
    rows.append(pd.DataFrame([("base", 3, t, r, "a test") for t, r in TRIO_RETURNS],
                             columns=table.columns))
    return pd.concat(rows, ignore_index=True).sort_values(["scenario_id", "sub_id", "t"],
                                                          kind="stable")


def _stepped_rates(table):
    """S's rate scenarios with the variant path stepped, the new return paths' level at 0,
    and cmtdrop's, the stepped variant path with the CMT's fall (:data:`CMT_DROP`)."""
    rows = [table, pd.DataFrame([(scenario, 0, 330.0, 0.04, "a test")
                                 for scenario, _ in VARIANT_RETURNS],
                                columns=table.columns)]
    rows += [pd.DataFrame([("variant", t, vix, cmt, "stepped for a test")],
                          columns=table.columns) for t, vix, cmt in VARIANT_RATES]
    variant = pd.concat(rows, ignore_index=True)
    variant = variant[variant["scenario_id"] == "variant"].sort_values("t", kind="stable")
    month, cmt = CMT_DROP
    held = variant[variant["t"] <= month].iloc[-1]["vix_sq"]
    rows += [variant.assign(scenario_id="cmtdrop"),
             pd.DataFrame([("cmtdrop", month, held, cmt, "a test")], columns=table.columns)]
    return pd.concat(rows, ignore_index=True).sort_values(["scenario_id", "t"],
                                                          kind="stable")


# The variants' programmes, keyed by policy month, (programme, month, premium, withdrawal):
# variant 10's midyear, 20's lateprem, 21's floors and 22's cmtdrop.
PROGRAMMES = (("midyear", 62, 10000.0, 0.0), ("midyear", 66, 0.0, 12000.0),
              ("midyear", 69, 0.0, 3000.0), ("midyear", 83, 0.0, 2000.0),
              ("lateprem", 100, 60000.0, 0.0),
              ("floors", 0, 0.0, 50000.0), ("floors", 18, 0.0, 55000.0),
              ("floors", 20, 0.0, 15000.0),
              ("cmtdrop", 62, 0.0, 9000.0), ("cmtdrop", 68, 0.0, 3000.0),
              ("cmtdrop", 70, 0.0, 500.0))


def _midyear(table):
    """S's programmes with the variants' (:data:`PROGRAMMES`), keyed by policy month."""
    extra = pd.DataFrame([(*row, "a test") for row in PROGRAMMES], columns=table.columns)
    return pd.concat([table, extra], ignore_index=True)


def _second_fund_set(table):
    """S's fund sets with variant 13's, 25/75, and variant 26's, trio, 50/30/20 over three
    subaccounts, each subaccount at a fee of its own."""
    extra = pd.DataFrame([("alt_25_75", 1, 0.25, 0.0120, "equity", "a test"),
                          ("alt_25_75", 2, 0.75, 0.0040, "fixed income", "a test"),
                          ("trio", 1, 0.50, 0.0080, "equity", "a test"),
                          ("trio", 2, 0.30, 0.0050, "fixed income", "a test"),
                          ("trio", 3, 0.20, 0.0020, "money market", "a test")],
                         columns=table.columns)
    return pd.concat([table, extra], ignore_index=True)


def _second_grid(table):
    """S's GAWA grids with variant 14's, each band at a percentage of its own, and variant
    21's high_grid, 60% at every age from 35."""
    extra = pd.DataFrame([("alt_grid", age, pct, "a test") for age, pct in
                          ((35, 0.031), (60, 0.037), (65, 0.049), (70, 0.051),
                           (75, 0.053), (81, 0.058))]
                         + [("high_grid", 35, 0.60, "a test")], columns=table.columns)
    return pd.concat([table, extra], ignore_index=True)


# The input files the splice's copies change, S's and SEC's alike.  SEC reads its two
# scenarios from the companions, which the generator writes afresh from the edited S.
SPLICED_EDITS = {"return_scenario.csv": _variant_paths, "rate_scenario.csv": _stepped_rates,
                 "transaction_table.csv": _midyear, "fund_table.csv": _second_fund_set,
                 "gawa_pct_table.csv": _second_grid}
SEC_EDITS = {name: edit for name, edit in SPLICED_EDITS.items()
             if name not in ("return_scenario.csv", "rate_scenario.csv")}

# T2's rows restated from S's new-business points and the variants, as (row_kind, S point,
# source_mth).  The months are S's, each chosen for what falls there, on S's own events:
#   on the anchor (1), which withdraws from policy month 120, at age 70, and depletes at
#     228: 12 and 24, contract-year starts in the Bonus Period; 26, the worked example's
#     month; 40 and 60, mid-year and anniversary 5, before any withdrawal; 71, the last
#     month of contract year 6; 119, the last month before the first withdrawal, whose
#     year-open roll-up base the roll-up death benefit then reads from the frame at
#     t_entry() itself; 120, the first withdrawal, a year start in force; 125 and
#     131, after it, mid-year and the year's last month, the year to date and the
#     dollar-for-dollar reduction; 143, the GWB Adjustment Date, voided; 228, 230 and
#     240, the depletion month, a year start, depleted mid-year, and depleted at a year
#     start, paying from the columns;
#   on S's in-force point (2): S months 14, 34, 45 and 99, policy months 40, 60, 71 and
#     125, each copy moving by 26 + d;
#   on the decline path (3), first withdrawal at 120 and depletion at 134: 125, 134, 143,
#     144 (depleted at a year start) and 150;
#   on the excess programme (4), 20,000 at 60 and a premium of 25,000 at 72: 60, 71, 72
#     and 75;
#   on the highest quarterly step-up (5): 40, 71 and 125;
#   on the VIX fee and the CMT roll-up (6): 40 and 41, either side of a quarter's last
#     month, 60 and 125;
#   on the never-withdrawing basic death benefit (7): 60, 131, 143 (the GWB Adjustment
#     Date at t = 0, binding at 200%) and 719, the last policy month;
#   on the never-withdrawing roll-up (8): 125; 524, the month its account runs out with no
#     withdrawal under the splice's References (554 at the shipped ones, from which the
#     committed row at 560 is read), valued in it; and 560, depleted;
#   on the withdrawing basic death benefit (9): 125 and 131;
#   on the midyear programme (10): 64, between the premium and the first withdrawal; 66,
#     the first withdrawal; 68, between two withdrawals; 69, valued in a withdrawal month
#     after another that year; 75 and 83, before a withdrawal in a contract year's last
#     month and in it;
#   on the crash path (11): 60 and 70, depleted without a withdrawal, the adjustment
#     carried; the female table (12), the second fund set (13) and grid (14), one each;
#   at issue age 55 (15): 175, 179, 186 and 192, around the adjustment at 179 and the
#     depletion before the first withdrawal; and 396, a contract year's start depleted not
#     for life, its GWB of 196 below its GAWA, so that the first payment on the books is
#     the GWB the row carries;
#   at issue age 72 (16): 6 and 30;
#   on the swinging path (17): 2, valued at a quarter end; 3, the month after one, the
#     year's highest, which the column alone holds; 6, its highest quarterly value before
#     the valuation month; and 11, a year's last month, the next year's step-up reading no
#     column;
#   on the cmtdrop programme (22): 64, between the year's first withdrawal and the CMT's
#     fall, so that the withdrawals at 68 and 70 find the year's dollar-for-dollar use above
#     the allowance the lower rate gives;
#   on the anchor not for life at 59 (23): 125, its excess withdrawals under way, which
#     later run its GWB down to rounding about 0;
#   with no premium tax (24 and 25): 525 and 660, the months after their accounts run out
#     on a rounding above 0 and below it, valued depleted on what is left;
#   on three subaccounts (26): 40, the three apart from the set's split since issue.
SPLICES = (
    *(("derived", 1, d) for d in (12, 24, 26, 40, 60, 71, 119, 120, 125, 131, 143, 228,
                                  230, 240)),
    *(("derived", 2, d) for d in (14, 34, 45, 99)),
    *(("derived", 3, d) for d in (125, 134, 143, 144, 150)),
    *(("derived", 4, d) for d in (60, 71, 72, 75)),
    *(("derived", 5, d) for d in (40, 71, 125)),
    *(("derived", 6, d) for d in (40, 41, 60, 125)),
    *(("derived", 7, d) for d in (60, 131, 143, 719)),
    *(("derived", 8, d) for d in (125, 524, 560)),
    *(("derived", 9, d) for d in (125, 131)),
    *(("derived", 10, d) for d in (64, 66, 68, 69, 75, 83)),
    *(("derived", 11, d) for d in (60, 70)),
    ("derived", 12, 125), ("derived", 13, 40), ("derived", 14, 120),
    *(("derived", 15, d) for d in (175, 179, 186, 192, 396)),
    *(("derived", 16, d) for d in (6, 30)),
    *(("derived", 17, d) for d in (2, 3, 6, 11)),
    ("derived", 22, 64), ("derived", 23, 125), ("derived", 24, 525), ("derived", 25, 660),
    ("derived", 26, 40),
)

# The variants' twins in the splice's table, each issued at the valuation date: on them the
# two clocks coincide, as on T1's committed twins of S's points, and each is compared with
# its S point cell by cell under SPLICE_EXEMPT, as a restated row is.  Variant 16's
# withdraws in its first contract year on the roll-up death benefit, so that its year-open
# roll-up base is read by the issue rule at t = 0, which no committed twin reads.
VARIANT_TWINS = tuple(("twin", p, 0) for p in VARIANTS)

# T3's cases, as (S point, k): every S new-business point and variant issued a month on,
# which puts its anniversaries a month off the valuation years, and the anchor 15 months
# on and the VIX point 13 months on, more than a year, so that a missing guard reads
# contract year -1, or a quarter before issue, there.
FUTURES = (*((p, 1) for p in (*S_POINTS, *VARIANTS)), (1, 15), (6, 13))

# The default run's cases (the module docstring), each with what it is there for: between
# them every Projection line the full grid's rows run, every predicate of the core test's
# dicts the full grid reaches, and every category of its static list.  The rest of
# SPLICES and FUTURES run with USLIB_SEC_FULL=1.
CORE_SPLICES = {
    ("twin", 2, 0): "S's in-force point, the worked example's month at t = 0",
    ("derived", 1, 119): "a year's last month before a withdrawal: the year-open RB read "
                         "from the frame at t_entry()",
    ("derived", 3, 134): "the account value running out in the valuation month",
    ("derived", 3, 144): "depleted at a contract year's start: the GLWB paid from columns",
    ("derived", 3, 150): "depleted mid-year after a withdrawal in an earlier year",
    ("derived", 4, 60): "the excess withdrawal at the valuation month, in the 4% charge "
                        "year, and the premium after it",
    ("derived", 4, 72): "a premium at the valuation month on a contract that has "
                        "withdrawn: the GAWA takes the locked GAWA% of it",
    ("derived", 6, 41): "the VIX fee's prior from its column, the CMT-linked roll-up",
    ("derived", 7, 143): "the GWB Adjustment binding at t = 0, a year's last month",
    ("derived", 10, 64): "the year-open RB read by a withdrawal after a premium that year",
    ("derived", 10, 69): "valued in a withdrawal month after another that year",
    ("derived", 10, 83): "valued at a withdrawal in a contract year's last month",
    ("derived", 11, 60): "depleted without a withdrawal, the adjustment carried",
    ("derived", 12, 125): "the female table, after the first withdrawal",
    ("derived", 15, 175): "a payment not for life, before the adjustment at 179",
    ("derived", 15, 396): "depleted not for life at a year's start, the GWB below the "
                          "GAWA: the first payment the GWB from its column",
    ("derived", 16, 6): "the first policy year, the older roll-up rate, the year flag "
                        "alone",
    ("twin", 16, 0): "issued at the valuation date, withdrawing in its first year on the "
                     "roll-up death benefit: the year-open base by the issue rule at t = 0",
    ("derived", 17, 2): "a quarter end at the valuation month, read from the frame",
    ("derived", 17, 3): "the year's highest quarter end at month -1, the column's alone",
    ("derived", 17, 6): "the year's highest quarterly value from the column wins",
    ("derived", 17, 11): "a year's last month: the next year's step-up reads no column",
    ("derived", 22, 64): "the year's dollar-for-dollar use above the allowance a CMT fall "
                         "cuts",
    ("derived", 24, 525): "depleted at the opening on an account value above 0, at or "
                          "below the threshold",
    ("derived", 25, 660): "depleted at the opening on an account value below 0, which "
                          "Data reads to a cent",
    ("derived", 26, 40): "three subaccounts, the third a column the generator takes from "
                         "the S model's fund table",
}
CORE_FUTURES = {
    (1, 15): "issued more than a year on: contract year -1 before issue",
    (5, 1): "the highest quarterly step-up from issue: a quarter end's value below a "
            "later one's, and the death benefit ratcheted to the account value",
    (6, 1): "the VIX fee and the CMT roll-up from issue, the CMT floor and cap",
    (13, 1): "the second fund set's allocation and fees, which no line shows",
    (14, 1): "the second GAWA grid, which no line shows",
    (16, 1): "issue age 72, withdrawing from issue on the older roll-up rate",
    (20, 1): "issue age 69, the younger roll-up rate's last",
    (21, 1): "issue age 70, the older roll-up rate's first; the GWB floored at 0 by a "
             "withdrawal inside the limit and by an excess one, and the GAWA after the "
             "excess capped at the GWB after it",
}

# The switched References' grid and its core, as T2's and T3's, each at a month where a
# bound acts: the VIX fee at 40 and 125, whose fee meets the corridor's low; the anchor,
# the never-withdrawing roll-up and basic death benefit at 84 and 83, whose GWB meets its
# cap from 95; the excess programme at 75, which meets the cap from 107; the VIX point
# issued a month on; the point issued at age 72 at 23, the month its step-up after its
# first withdrawal raises the GAWA, which only these References' lower GLWB fee reaches;
# variants 18 and 19 issued a month on, whose step-ups closing policy month 311 raise the
# Bonus Base at attained ages 81 and 82, at the restart age and a year past it; and variant
# 20 at 99, whose premium at 100 meets a GWB already at the cap and takes the Bonus Base
# past it.  The switched grid runs no Projection line the shipped References' core does
# not, so its core is the rows that reach its bounds.
SWITCHED_GRID = (("derived", 6, 40), ("derived", 6, 125), ("derived", 1, 84),
                 ("derived", 8, 83), ("derived", 7, 83), ("derived", 4, 75),
                 ("future", 6, -1), ("derived", 16, 23), ("future", 18, -1),
                 ("future", 19, -1), ("derived", 20, 99))
SWITCHED_CORE = {
    ("derived", 7, 83): "the GWB cap, the lapse capped at 1, a step-up past the Bonus "
                        "Period's restart age",
    ("future", 6, -1): "the VIX corridor's low",
    ("derived", 16, 23): "the GAWA raised by a step-up after the first withdrawal",
    ("future", 18, -1): "a Bonus-Base-raising step-up at the restart age, 81, which "
                        "restarts the Bonus Period",
    ("future", 19, -1): "one at 82, a year past it, which does not",
    ("derived", 20, 99): "the GWB cap at a premium after issue, in the GWB and the Bonus "
                         "Base",
}

SEC_FULL = os.environ.get("USLIB_SEC_FULL") == "1"
FULL_ONLY = (pytest.mark.sec_full,
             pytest.mark.skipif(not SEC_FULL, reason="the full splice grid runs with "
                                "USLIB_SEC_FULL=1 (USLIB-SEC-PLAN.md K6)"))

# The opening state of S's columns: S's cells read its own columns, 0 on its new business,
# where a derived row's are the state S carries into d, by design.
OPENING = frozenset({"av_pp_init", "gwb_pp_init", "gawa_pp_init", "gawa_pct_init",
                     "has_wd_init", "bb_pp_init", "rb_pp_init", "np_pp_init",
                     "rp_pp_init", "adj_pp_init", "bonus_end_init"})

# The cells T2 and T3 skip beyond T1's (TWIN_EXEMPT_DEFAULT and the spec's exempt, which
# drop model_point, pols_if_init, input_dir and result_pols as a whole):
#   OPENING, above, on a row restated in force;
#   proj_len counts from the valuation date on SEC and from issue on S, so it differs by
#     d, or by -k, by design; frame_mismatches asserts what it must get right, that both
#     frames end at the same instant;
#   duration_mth_init and is_inforce are the row's months in force, not S's;
#   t_of_month is keyed by a policy month, so S's and the row's differ by d;
#   scenario_id names a row's own re-based copy of its S scenario, -M{m} or -F{k};
#   policy_id is the generator's composed id, VA-000001-M60 or VA-000001-F15.
SPLICE_EXEMPT = (TWIN_EXEMPT_DEFAULT | SPEC.exempt | OPENING
                 | {"proj_len", "duration_mth_init", "is_inforce", "t_of_month",
                    "scenario_id", "policy_id"})
FUTURE_EXEMPT = (TWIN_EXEMPT_DEFAULT | SPEC.exempt
                 | {"proj_len", "duration_mth_init", "t_of_month", "scenario_id",
                    "policy_id"})

# The roll-forward residuals, whose exact value is 0 and whose computed value is rounding
# around it, up to about 3e-11 in most months: the splice compares them at the harness's
# absolute floor of 1e-9 and everything else with none (§5.2, precised at M11).
RESIDUALS = frozenset({"check_av_roll_fwd_resid", "check_pols_roll_fwd_resid",
                       "check_charge_split_resid"})

# The other cells whose exact value can be 0 while the computed one is rounding about it,
# compared at the same floor, each a value a contract: the GWB a contract not for life
# runs down to 0 by its payments or its withdrawals, read at each timing and after the
# bonus and the step-up, and what reads it as it is, the payment on it and the GWB's
# moneyness, and result_bases, which holds the GWB.  An opening state the CSV gives back
# one ulp off leaves S's GWB and the row's a rounding apart there, 9.5e-12 against 0.0 on
# variant 23 valued at 125, where no number moves; a GWB or a payment of a dollar a
# contract is still compared to 1e-9 of itself.
ROUNDED = frozenset({"gwb_pp", "gwb_pp_at", "gwb_pp_aft_bonus", "gwb_pp_aft_stepup",
                     "glwb_payment_pp", "moneyness_glwb", "result_bases"})
FLOORED = RESIDUALS | ROUNDED
FLOOR = 1e-9            # the harness's absolute floor, twin_mismatches' default atol

# The payments in force, a payment a contract weighted by a count that falls far below 1,
# to 3.3e-8 on variant 18 and 1.1e-8 on point 5 under the switched References, where a
# floor of 1e-9 would pass an error of 3% to 9%.  So the cell and result_cf's column of it
# are compared with no floor, but at the months where both models' payment a contract,
# glwb_payment_pp, is below the floor, 0 or the GWB's rounding about it, the 9.5e-12 a
# contract S pays variant 23 at policy month 336 against the row's 0.0
# (:func:`_residue_months`).
PAID = "glwb_payments"

# The cells the acquisition expense moves, which S charges at its t == 0, the valuation
# date, on its in-force point 2, and this model in the issue month only: on S's in-force
# twin they are compared from t = 1 (§5.2, as precised in the spec's comment).
ACQ = ("expenses", "net_cf", "net_cf_ga")

# The result_cf columns that expense inflation moves, and the cells they are made of: on
# the committed points, at the shipped 2.5%, the only places an in-force row departs from S.
INFLATED = ("expenses", "net_cf")
INFLATION_CELLS = frozenset({"inflation_factor", "expenses", "net_cf", "net_cf_ga",
                             "result_cf"})

# The decrement rates, which the counts read in every month: before issue each is the
# float 0.0 (R1, D4).
DECREMENT_RATES = ("mort_rate", "mort_rate_mth", "lapse_rate", "lapse_rate_mth",
                   "lapse_rate_base")

# The cells keyed by an attained age, a count of completed years, a policy month or a
# contract quarter, which a row may not read below its first on the books: the ages from
# the age in its first month, the years and months likewise, and the quarters from the
# quarter under way in its first month, whose fee's prior is phi_glwb_init.
AGE_READERS = ("gawa_pct_at_age", "mort_rate_base_at")
YEAR_READERS = ("surr_charge_rate_at",)
MONTH_READERS = ("prem_scheduled_pm", "wd_scheduled_pm")
QUARTER_READERS = ("phi_glwb_vix", "vix_sq")

# The four count timings, BEF_NB the one running in force adds; the account value's five,
# which each subaccount, the account value and the account value in force share; the
# guarantee bases' three; and the three benefit kinds.  Each is passed through _code.
TIMINGS = ("BEF_NB", "BEF_DECR", "BEF_LAPSE", "AFT_DECR")
AV_TIMINGS = ("BEF_PREM", "BEF_WD", "BEF_INV", "BEF_FEE", "EOM")
BASE_TIMINGS = ("BEF_PREM", "BEF_WD", "BEF_ANNIV")
KINDS = ("DEATH", "LAPSE", "MATURITY")
KINDED = ("pols_decr", "claim_pp", "claim_from_av_pp", "claims", "claims_from_av",
          "claims_over_av")
TIMED = {"pols_if_at": TIMINGS, "av_pp_at": AV_TIMINGS, "av_at": AV_TIMINGS,
         "gwb_pp_at": BASE_TIMINGS, "gawa_pp_at": BASE_TIMINGS, "rb_pp_at": BASE_TIMINGS}

# The cells keyed by a month and a subaccount: the subaccount at a timing, and at the
# month's end and its share of the account value.
SUBACCOUNT_TIMED = ("sa_pp_at",)
SUBACCOUNT = ("sa_pp", "sa_weight")

REPORTS = ("result_cf", "result_pols", "result_av", "result_bases")

# result_pols' columns, in its order: the count, the new business within it, the month's
# deaths, surrenders and deemed maturities, and the count leaving the month.
RESULT_POLS = ["pols_if", "pols_new_biz", "pols_death", "pols_lapse", "pols_maturity",
               "pols_if_aft_decr"]
OUTFLOWS = ["pols_death", "pols_lapse", "pols_maturity"]

# What each monthly cell holds outside cover, before issue and from the month cover has
# ended, as its docstring says: no count, so no cash flow; no account value, base,
# withdrawal, charge, rate or residual; no question about the contract answered yes; the
# four factors at 1.0, "no change": the death benefit's proportional factor of the month
# and of the year to date, the lapse's moneyness multiplier and its withdrawal-year
# factor; the Bonus Period's end at the int 0; and the phase PRE_ISSUE before issue and
# EXPIRED from maturity on.  The type is part of the value: a count, an amount or a rate
# is a float in every branch, a flag a bool, because Phase 2 types a cell by the values it
# returns (USLIB-SEC-PLAN.md F3).  The guard test also calls each of TIMED at each of its
# timings, the KINDED cells at each kind and the subaccount cells at each subaccount, all
# 0.0.
_ZERO = ("adj_pp", "adj_pp_bef_anniv", "asset_charge_pp", "asset_charges", "av_change",
         "av_pp", "bb_pp", "bb_pp_bef_anniv", "bonus_pp", "charge_income",
         "charge_income_pp", "charge_pp", "charge_pp_due", "charge_scale",
         "charges_from_av", "check_av_roll_fwd_resid", "check_charge_split_resid",
         "check_pols_roll_fwd_resid", "commissions", "cv_pre_excess_pp", "db_pp",
         "excess_factor", "expenses", "fee_glwb_pp", "fee_glwb_pp_due", "fee_gmdb_pp",
         "fee_gmdb_pp_due", "fees_glwb", "fees_gmdb", "free_wd_allow", "free_wd_avail",
         "free_wd_used_cum_pp", "fund_expense_pp", "gawa_pct_fixed", "gawa_pp",
         "glwb_payment_pp", "glwb_payments", "gmdb_allow_pp", "gmdb_claim_pp",
         "gmdb_claims", "gmdb_dfd_acc_pp", "gmdb_guarantee_pp", "gmdb_wd_dfd_pp",
         "gmdb_wd_excess_pp", "gross_inv_income_pp", "gwb_pp", "gwb_pp_aft_bonus",
         "gwb_pp_aft_stepup", "inv_income", "inv_income_pp", "lapse_rate",
         "lapse_rate_base", "lapse_rate_mth", "maint_fee_pp", "maint_fee_pp_due",
         "maint_fees", "moneyness_glwb", "moneyness_gmdb", "mort_rate", "mort_rate_mth",
         "net_cf", "net_cf_ga", "np_pp", "phi_glwb", "phi_gmdb", "pols_death", "pols_if",
         "pols_lapse", "pols_maturity", "pols_new_biz", "prem_scheduled_pp", "prem_to_av",
         "prem_to_av_pp", "premium_pp", "premium_taxes", "premiums", "rb_pp",
         "rb_prior_anniv_pp", "rollup_rate", "rp_pp", "rp_reduction_pp", "stepup_base_pp",
         "sum_wd_pp", "surr_benefit_pp", "surr_charge_pp", "surr_charge_rate",
         "surr_chargeable_pp", "surr_free_pp", "wd_charge_pp", "wd_chargeable_pp",
         "wd_charges", "wd_excess_pp", "wd_exempt_pp", "wd_free_pp", "wd_from_av",
         "wd_glwb_pp", "wd_limit_pp", "wd_nonexcess_pp", "wd_payment_pp", "wd_pp",
         "wd_pp_due", "wd_scheduled_pp", "withdrawals")
_FALSE = ("is_active", "is_anniv", "is_quarterly_anniv", "is_year_start", "depleted_open",
          "is_wd_month", "is_wd_taken", "has_wd_by", "is_first_wd", "is_wd_year",
          "is_stepup", "is_gwb_adj_date", "depleted_flag")
OUTSIDE_COVER = {
    **{name: 0.0 for name in _ZERO}, **{name: False for name in _FALSE},
    "gmdb_wd_factor": 1.0, "gmdb_factor_acc": 1.0, "lapse_dyn_mult": 1.0,
    "lapse_wd_factor": 1.0, "bonus_end": 0, "phase": ("PRE_ISSUE", "EXPIRED")}

# The cells a month outside cover may not reach.  None has a guard of its own: the clock
# cells keyed by the contract year, the attained age, the quarter and the month closing or
# opening the year are arithmetic and would answer harmlessly; the scenario readers are
# inputs, left unguarded so that a pre-issue read of a future row's re-based scenario
# fails loudly (T3); the keyed readers would read a table at a key the contract does not
# have; and S's engine functions, keyed by a float, are Phase 2's to inline.  No formula
# reaches them outside cover, and a caller must not either (USLIB-SEC-PLAN.md F4).  The
# opening state's subaccount values, sa_pp_init, are not among them: proj_len() reads them
# on a contract in force, as the account value it checks the opening state against.
IN_COVER_ONLY = ("policy_year", "duration", "age", "age_at_anniv", "contract_quarter",
                 "anniv_mth", "year_open_mth", "t_of_month", "inv_return_mth",
                 "scenario_rate", "cmt10", "vix_sq", "unit_growth", "phi_glwb_vix",
                 "gawa_pct_at_age", "mort_rate_base_at", "surr_charge_rate_at",
                 "prem_scheduled_pm", "wd_scheduled_pm", "alloc", "fund_expense_rate",
                 "fee_rate_vix_raw", "fee_rate_vix_clip", "lapse_itm_mult")

# The monthly cells that read a scenario, which a future row's re-based copy sets no level
# for before issue, so that each raises there, naming the point (T3, D4).
SCENARIO_READERS = ("inv_return_mth", "scenario_rate", "cmt10", "unit_growth")

# The readers of IN_COVER_ONLY keyed by an age, a year, a policy month or a quarter, which
# Phase 2's full sweep must not reach outside cover; the subaccount's readers, keyed by
# the subaccount alone, and the engine functions answer at every month.
KEYED_READERS = (*AGE_READERS, *YEAR_READERS, *MONTH_READERS, *QUARTER_READERS)

# The monthly cells defined at every month, inside cover or out: the policy clock and
# expense inflation, an input on the valuation clock (D7).
EVERY_MONTH = ("duration_mth", "inflation_factor")

# The bools each text column S branches on is decoded into, once a point, so that no
# monthly cell compares a column's text or calls a label accessor (USLIB-SEC-PLAN.md
# §7.1, *Record — M14*), each read where S asks its question.
DECODES = ("is_stepup_annual", "is_stepup_highest_quarterly", "is_gmdb_rollup",
           "is_gmdb_ratchet", "is_gmdb_basic", "is_fee_reset_none",
           "is_fee_reset_quinquennial", "is_fee_reset_vix", "is_rollup_fixed",
           "is_rollup_cmt_linked")

# The opening state, in the table's order: the seven bases, the locked GAWA% and the Bonus
# Period's end, S's columns renamed; the two subaccount values; the withdrawal status;
# the four values of the year to date and the year's withdrawal flag; the roll-up base at
# the anniversary that opened the year; the year's highest quarterly account value; and
# the VIX fee of the quarter before.  And the cells running in force adds to VA_US_S's,
# each of which the symbol map must name.
MONEY = ("gwb_pp_init", "gawa_pp_init", "bb_pp_init", "rb_pp_init", "np_pp_init",
         "rp_pp_init", "adj_pp_init", "sum_wd_pp_ytd_init", "free_wd_used_cum_pp_ytd_init",
         "gmdb_dfd_acc_pp_ytd_init", "rb_pp_prev_anniv_init", "stepup_base_pp_ytd_init")
RATES_COLUMNS = ("gawa_pct_init", "gmdb_factor_acc_ytd_init", "phi_glwb_init")
FLAGS = ("has_wd_init", "wd_this_year_init")
FUNDS = ("sa_pp_init_1", "sa_pp_init_2")
STATE = ("gwb_pp_init", "gawa_pp_init", "gawa_pct_init", "bb_pp_init", "rb_pp_init",
         "np_pp_init", "rp_pp_init", "adj_pp_init", "bonus_end_init", *FUNDS,
         "has_wd_init", "sum_wd_pp_ytd_init", "free_wd_used_cum_pp_ytd_init",
         "gmdb_dfd_acc_pp_ytd_init", "gmdb_factor_acc_ytd_init", "wd_this_year_init",
         "rb_pp_prev_anniv_init", "stepup_base_pp_ytd_init", "phi_glwb_init")
# The state Data checks column by column, as it reads them: the money, the rates, the
# Bonus Period's end and the two flags, the fund values apart.
CHECKED_STATE = (*MONEY, *RATES_COLUMNS, "bonus_end_init", *FLAGS)
NEW_CELLS = ("policy_count", "maturity_mth", "t_entry", "is_active", "anniv_mth",
             "year_open_mth", "pols_new_biz", "depleted_open", *DECODES, "sa_pp_init",
             "sum_wd_pp_ytd_init", "free_wd_used_cum_pp_ytd_init",
             "gmdb_dfd_acc_pp_ytd_init", "gmdb_factor_acc_ytd_init", "wd_this_year_init",
             "rb_pp_prev_anniv_init", "stepup_base_pp_ytd_init", "phi_glwb_init",
             "prem_scheduled_pm", "wd_scheduled_pm", "surr_charge_rate_at",
             "mort_rate_base_at")

INFLATION = 0.025       # the shipped inflation_rate, which the inflation test reads

# The recursion limit, as mx.set_recursion takes it, under which the committed points are
# first swept (R2, F7).  Every chain runs forward, one cell a month, and a report evaluates
# each column in ascending t, so a forward recursion, through t - 1, finds the month before
# already cached.  But the GAWA's chain is first read cold deep in the frame on a contract
# that never withdraws: S point 8's glwb_payments column first asks for gawa_pp at policy
# month 563, the month before the first contract-year start after its account value is
# exhausted at 554, and the chain walks back to t_entry().  The committed points' sweep
# reaches 569 on point 8, and VA_US_S's same sweep reaches 1,123 on the same point, its
# GAWA chain two cells a month; every other point stays under 160.  So it runs under 600.
# A backward recursion over the frame, through t + 1, opens a chain as long as the frame,
# and every committed frame but the nine the clock test lists is longer than 660.
CALL_DEPTH = 600

# The frames a cold call may hold on modelx's stack beyond one a month back to t_entry()
# (asserted as a bound, as Term's is).  Measured on a model just read, at the last month:
# 10 to 15 on net_cf over the committed rows, 15 on twin 4 and on row 14 (point 4 at 60);
# a chain head called alone runs at most 17, twin 4's bonus_end and gmdb_factor_acc,
# since VA's year chains open the withdrawals' chain, the GLWB bases, the step-up base and
# the account value in their first month; and 14 on net_cf at the contract's longest
# cover, 1,020 months from issue age 35, at the valuation date and 120 months on (1,034
# levels).  20, UL_US_SEC's allowance, leaves 3 levels above the deepest head for the
# reader Phase 2 adds under a table.  A chain of two cells a month doubles the depth and
# fails here.
CHAIN_OVERHEAD = 20

# The months R2's one admitted read reaches ahead, at most: lapse_wd_factor(t) reads the
# year at anniv_mth(t), up to 11 months on.  A count called cold, alone, opens its chain at
# its first month on the books, where the lapse reads that anniversary's withdrawal year,
# and so the withdrawals' chain up to 11 months long, under the count's: the count's cold
# depth is bounded by CHAIN_OVERHEAD and this together.  Measured: 20 over the month
# count on the committed rows, and 20 at the longest cover (1,040 levels against 1,020).
LOOK_AHEAD_MTHS = 11

# What only VA_US_S's docstrings may say: a reference into its Spaces, which the SEC pages
# would link to the wrong model; the purchase payment and the acquisition at t = 0 and
# every opening read there; S's split of the account value by the allocation; the scenario
# keyed by the elapsed policy month; inflation by completed contract years; the RB
# fallback at the first projected month; and "then clear the cache", modelx-only advice
# that a compiled model cannot follow.  Each is a phrase of VA_US_S's own, which the
# docstring test checks.
STALE_PHRASES = (r"~\.VA_US_S\.",
                 r"The purchase payment falls at the beginning of month ``t = 0``",
                 r"which every recursion reads as the opening balance of ``t = 0``",
                 r"``S_init\(\) if t == 0 else",
                 r"the acquisition expense are all beginning-of-month flows of ``t = 0``",
                 r"paid at the beginning of the first projected month",
                 r"Negative before the model point entered",
                 r"as a step function of the \*\*elapsed policy\*\* month",
                 r"split by ``alloc\(i\)`` in the first projected month",
                 r"is :func:`has_wd_init` in the first projected month",
                 r"completed contract years",
                 r"the carried-in Benefit Base plus the premium taken at the start of the "
                 r"first projected month",
                 r"Row ``t = 0`` is the first projected month: it carries the purchase "
                 r"payment",
                 r"then clear the cache")
STALE = re.compile("|".join(STALE_PHRASES))


# ---------------------------------------------------------------------------
# Helpers

_names = itertools.count(1)


def _name(tag):
    """A model name that no other read in this session uses."""
    return f"{SEC}_{tag}_{next(_names)}"


def _read(folder, tag, refs=None, data=None):
    """The model in ``folder``, read under a name of its own, its References set at once.

    ``refs`` go on ``Projection`` and ``data`` on ``Data``, before the model computes
    anything: a compiled model never clears a cache, so a Reference set after a Space has
    computed would leave its values as they were.
    """
    model = mx.read_model(folder, name=_name(tag))
    for ref, value in (refs or {}).items():
        setattr(model.Projection, ref, value)
    for ref, value in (data or {}).items():
        setattr(model.Data, ref, value)
    return model


def _key(model, point_id):
    """The registry's key for the row labelled ``point_id`` (``us_registry.point_keys``)."""
    return dict(zip(model.Data.model_point_table().index, point_keys(model)))[point_id]


def _point(model, point_id):
    """The ItemSpace of the row labelled ``point_id``, through the registry's keys."""
    return projection(model, _key(model, point_id))


def _label(table, kind, s_point, month):
    """The ``point_id`` of the one ``kind`` row generated from S point ``s_point``.

    ``month`` is the row's ``source_mth``: 0 for the twin of a new-business point and for
    the twin of S's point 2, which S projects from the valuation date, ``d`` for a derived
    row, ``-k`` for a future one.  The twins keep S's ``point_id`` and ``policy_id``, so
    the S policy is the twin's.
    """
    policy = table.at[s_point, "policy_id"]
    hit = table.index[(table["row_kind"] == kind) & (table["source_policy_id"] == policy)
                      & (table["source_mth"] == month)].tolist()
    assert len(hit) == 1, f"{kind} rows of S point {s_point} at month {month}: {hit}"
    return hit[0]


def _row_key(model, kind, s_point, month):
    """The registry's key for that row of ``model``'s table (:func:`_label`)."""
    return _key(model, _label(model.Data.model_point_table(), kind, s_point, month))


def _row(model, kind, s_point, month):
    """The ItemSpace of that row of ``model``'s table (:func:`_label`)."""
    return projection(model, _row_key(model, kind, s_point, month))


def _release(model, key, collect=False):
    """Drop the ItemSpace at ``key``, the registry's key, and every value it has cached.

    The splice's rows and the points of the temporary copies are each needed once, so each
    is released when read, as ``run_sec.py --block`` releases its points
    (USLIB-SEC-PLAN.md F5): held together they would raise this module's memory several
    times over.  Asked for again, the ItemSpace is made afresh and recomputes.  With
    ``collect``, the collector runs at once, as it does for each splice row; the swept
    models the module holds are frozen out of it (:func:`_freeze`), so the collection
    scans only what the row made.
    """
    del model.Projection[key]
    if collect:
        gc.collect()


def _freeze():
    """Collect what is garbage, then freeze everything still alive out of the collector.

    Each module fixture that sweeps a model calls this once its sweep is done, so that the
    collections after it, automatic or :func:`_release`'s, no longer scan the millions of
    objects a swept model holds.  The collection first means no garbage is frozen with
    them.  The freeze is undone as the module ends (:func:`_collector`), and before the
    splice fixture closes one pair of models to read the other (:class:`_Splices`).
    """
    gc.collect()
    gc.freeze()


def _committed():
    """The committed SEC table as the file holds it, unvalidated, indexed by point_id."""
    return pd.read_csv(model_path(SEC).parent / TABLE, index_col="point_id")


def _companion(name):
    """A committed scenario companion as the file holds it, on a default index."""
    return pd.read_csv(model_path(SEC).parent / name)


def _relabeled(table):
    """``table`` relabeled ``100 + point_id`` and written in reverse order.

    Every generated table numbers its points from 1 in table order, so on it no test can
    tell a label from a position; on this one none is the other.
    """
    return table.set_axis(table.index + 100).iloc[::-1]


def _sec_inputs(tmp_path, table, edits=None):
    """A copy of the product directory whose SEC table is ``table``; its SEC folder.

    The copy holds the two committed scenario companions, which ``edits`` may replace,
    under their names, where ``table`` names a scenario the committed ones lack, and any
    other input ``edits`` names.
    """
    return temp_inputs(tmp_path, model_path(SEC), model_points=table,
                       model_point_file=TABLE, edits=edits)


def _read_edited(tmp_path, edit, tag="edited", refs=None):
    """VA_US_SEC read from a copy whose SEC table is ``edit(_committed())``."""
    return _read(_sec_inputs(tmp_path, edit(_committed())), tag, refs)


def _set(column, points, value):
    """An edit of the table that writes ``value`` into ``column`` at ``points`` alone.

    The column is made ``object`` first, so a text or a number of another type can go in
    beside the numbers it holds: the file then carries what an extract with a bad cell
    would.
    """
    def edit(table):
        cells = table[column].astype(object)
        return table.assign(**{column: cells.where(~table.index.isin(points), value)})
    return edit


def _plus(column, points, amount):
    """An edit that adds ``amount`` to ``column`` at ``points`` alone."""
    def edit(table):
        moved = table[column].where(~table.index.isin(points), table[column] + amount)
        return table.assign(**{column: moved})
    return edit


def _cells(point, **columns):
    """An edit that sets each of ``columns`` at row ``point``."""
    def edit(table):
        for column, value in columns.items():
            table = _set(column, [point], value)(table)
        return table
    return edit


def _both(*edits):
    """The edits applied in turn."""
    def edit(table):
        for one in edits:
            table = one(table)
        return table
    return edit


def _drop(column):
    return lambda table: table.drop(columns=column)


def _refused(call, message):
    """``call()`` raises ``ValueError`` with ``message``, inside modelx's wrapper.

    modelx re-raises an error inside a formula as ``FormulaError``, with the original type
    and message in its text, so the text is asserted rather than a modelx class.
    """
    with pytest.raises(Exception) as excinfo:
        call()
    text = str(excinfo.value)
    assert "ValueError" in text and message in text, text


def _raised(err):
    """The line that names an error: modelx's ``FormulaError`` puts it second."""
    lines = [line for line in str(err).splitlines() if line.strip()]
    if type(err).__name__ == "FormulaError" and len(lines) > 1:
        return lines[1]
    return f"{type(err).__name__}: {lines[0] if lines else ''}"


def _code(space, label):
    """The argument or value that stands for timing, kind or phase ``label``.

    The conventions' lookup (``test_model_conventions._timing``), on ``Projection`` or any
    of its ItemSpaces, which see its References: the model's own int Reference named
    ``label`` where it defines one, and the string otherwise.  At stage ``"E"`` every
    timing, kind and phase is S's string; Phase 2 makes them codes (R9, R10), and every
    call below reads the same at both stages.
    """
    value = space.refs.get(label)
    return value if isinstance(value, int) and not isinstance(value, bool) else label


def _at(space, cell, t, label):
    """``cell(t, label)`` on ``space``, the timing or kind passed through :func:`_code`."""
    return space.cells[cell](t, _code(space, label))


def _mismatches(s_proj, sec_proj, **kwargs):
    """:func:`sec_support.twin_mismatches`, the one place this module calls it.

    It passes the SEC Space's :func:`sec_support.codes`, which map S's strings onto the
    int codes the SEC model names as its References: none at stage ``"E"``, where VA's
    timings, kinds and phases are S's strings, and at stage ``"EC"`` each of them.  Every
    comparison goes through here, so each takes Phase 2's codes when they come.
    """
    return twin_mismatches(s_proj, sec_proj, codes=codes(sec_proj), **kwargs)


def _timed(proj, t, timings):
    """Evaluate each cell of :data:`TIMED`, and each subaccount at each of the account
    value's timings, at month ``t`` and every timing it has among ``timings``."""
    for name, labels in TIMED.items():
        for label in labels:
            if label in timings:
                proj.cells[name](t, _code(proj, label))
    for i in proj.sub_ids():
        for label in AV_TIMINGS:
            proj.sa_pp_at(t, i, _code(proj, label))
        proj.sa_weight(t, i)


# The arguments _sweep_s gives S's cells keyed by a float, which no projection reaches at
# these values: the lapse's moneyness multiplier below, at and above its threshold and its
# two bounds, the raw VIX fee at the disclosed examples' levels and at both ends, and the
# fee's clip inside its band, at the band's edges and at the corridor's.
ITM_RATIOS = (0.0, 0.5, 1.0, 1.1, 1.3, 1.5, 2.0)
VIX_RAW_ARGS = ((0.0125, 204.42), (0.0145, 602.30), (0.0125, 0.0), (0.0125, 1500.0))
VIX_CLIP_ARGS = ((0.0142, 0.0186), (0.0142, 0.0126), (0.008, 0.002), (0.0245, 0.04))


def _sweep_s(proj):
    """Evaluate on an S point what the splice compares: the sweep, and the cells it misses.

    :func:`sec_support.sweep` reaches neither the subaccounts at each timing and their
    weights, nor the account value, the account value in force, the bases and the count
    at each of their timings, ``claims_over_av``, ``charge_income_pp``, ``gmdb_claims``,
    ``net_cf_ga``, ``wd_charges`` and ``phase`` on ``VA_US_S``, because no result column or
    check reads them, and a cell S never evaluates is compared nowhere (USLIB-SEC-PLAN.md
    §7.7, *C*).  Nor does it reach the label accessors ``designated_lives``, ``tax_status``
    and ``policy_id``, or S's three engine functions keyed by a float.  So they are
    evaluated here, the monthly ones over the frame at every timing and kind each has, and
    the others at arguments of their own (:data:`ITM_RATIOS`, :data:`VIX_RAW_ARGS`,
    :data:`VIX_CLIP_ARGS`).
    """
    sweep(proj)
    timings = set(TIMINGS) - {"BEF_NB"}             # S has no BEF_NB, which SEC adds
    for t in range(proj.proj_len()):
        _timed(proj, t, timings | set(AV_TIMINGS) | set(BASE_TIMINGS))
        _monthly_extras(proj, t)
    _point_extras(proj)


def _monthly_extras(proj, t):
    """The monthly cells no report reaches, at month ``t``: the claims over the account
    value at each kind and in total, the charge income per contract, the GMDB claims, the
    general-account net cash flow, the withdrawal charges and the phase."""
    proj.claims_over_av(t)
    for kind in KINDS:
        proj.claims_over_av(t, _code(proj, kind))
    proj.charge_income_pp(t)
    proj.gmdb_claims(t)
    proj.net_cf_ga(t)
    proj.wd_charges(t)
    proj.phase(t)


def _point_extras(proj):
    """The cells keyed by no month that no report reaches: three label accessors and S's
    engine functions at :data:`ITM_RATIOS`, :data:`VIX_RAW_ARGS` and
    :data:`VIX_CLIP_ARGS`."""
    proj.designated_lives()
    proj.tax_status()
    proj.policy_id()
    for ratio in ITM_RATIOS:
        proj.lapse_itm_mult(ratio)
    for args in VIX_RAW_ARGS:
        proj.fee_rate_vix_raw(*args)
    for args in VIX_CLIP_ARGS:
        proj.fee_rate_vix_clip(*args)


def _sweep_sec(proj):
    """:func:`_sweep_s` on an SEC row, its monthly cells over the whole frame.

    Every month from ``t = 0``, so a future row's cells are evaluated before its issue too,
    where each holds its guard's value; the count's timings include ``BEF_NB``.  The cells
    keyed by no month the comparison evaluates at S's own arguments.
    """
    sweep(proj)
    for t in range(proj.proj_len()):
        _timed(proj, t, set(TIMINGS) | set(AV_TIMINGS) | set(BASE_TIMINGS))
        _monthly_extras(proj, t)
    _point_extras(proj)


def _on_the_books(d):
    """T2's ``arg_map`` for a row valued at policy month ``d``: the quarters it reads.

    S reads the VIX fee by contract quarter from the first, recursing through every
    quarter's rate, and ``vix_sq`` at each quarter's last month.  A row valued at ``d``
    reads neither before the quarter under way in its first month on the books, quarter
    ``max(d, 0) // 3 + 1``: the rate of the quarter before is the row's ``phi_glwb_init``,
    and the rest is history, which a re-based scenario does not hold.  So S's
    ``phi_glwb_vix`` and ``vix_sq`` at an earlier quarter are skipped.  Every other key
    passes unchanged, its ``t`` moved by the comparison itself.
    """
    first = max(d, 0) // 3 + 1

    def arg_map(name, args):
        if name in QUARTER_READERS and args[0] < first:
            return None
        return args
    return arg_map


def _from_t1(books):
    """``books`` with :data:`ACQ`'s cells at ``t = 0`` skipped too, on S's in-force twin."""
    def arg_map(name, args):
        if name in ACQ and args[0] == 0:
            return None
        return books(name, args)
    return arg_map


def _residue_months(s_proj, sec_proj, month):
    """The S months from ``month`` on at which both models' GLWB payment a contract is
    below :data:`FLOOR`, at which :data:`PAID` is compared at the floor (:func:`_compare`).
    """
    out = set()
    for t in range(max(month, 0), s_proj.proj_len()):
        u = t - month
        mine = sec_proj.glwb_payment_pp(u) if 0 <= u < sec_proj.proj_len() else 0.0
        if abs(s_proj.glwb_payment_pp(t)) < FLOOR and abs(mine) < FLOOR:
            out.add(t)
    return out


def _paid_frames(s_cf, sec_cf, month, residue):
    """``result_cf``'s :data:`PAID` column, with no floor off the ``residue`` months and at
    the floor on them: both frames cut to the months they share, from S month ``month``,
    then each pass to its months, on each frame's clock."""
    first = max(month, 0)
    s_cf, sec_cf = s_cf.loc[first:], sec_cf.loc[first - month:]
    s_at = s_cf.index.isin(sorted(residue))
    sec_at = sec_cf.index.isin([t - month for t in sorted(residue)])
    lines = []
    for at, atol in ((False, 0.0), (True, FLOOR)):
        s_part, sec_part = s_cf[s_at == at], sec_cf[sec_at == at]
        if len(s_part) or len(sec_part):
            lines += frame_mismatches(s_part, sec_part, t_offset=month, columns=[PAID],
                                      atol=atol)
    return lines


def _split_paid(books, residue):
    """``books`` as two ``arg_map`` s: one that skips :data:`PAID` at the ``residue``
    months, and one that keeps it there alone."""
    def exact(name, args):
        return None if name == PAID and args[0] in residue else books(name, args)

    def floored(name, args):
        return None if name == PAID and args[0] not in residue else books(name, args)
    return exact, floored


def _compare(s_proj, sec_proj, month, exempt, columns=None, s_in_force=False):
    """Where SEC's row departs from S's point from S month ``month`` on, in two passes.

    First the frames, ``result_cf`` (over ``columns``, or every column both hold) and
    ``result_pols``, SEC row ``t`` against S row ``t + month``, frames ending together;
    then every cell of S's but ``exempt`` and :data:`FLOORED`, at every argument S cached
    inside its frame from ``month`` on, moved onto SEC's clock, the quarters before the
    books skipped (:func:`_on_the_books`).  Both to 1e-9 relative with no absolute floor: a
    count late in a long frame falls far below 1e-7, where a floor of 1e-9 would hide any
    error.  Then the cells of :data:`FLOORED` alone at the floor of 1e-9: their exact value
    can be 0, and the computed one rounding of it, the residuals' of what they close and
    the GWB's of what ran it down (§5.2, precised at M11).  The payments in force,
    :data:`PAID`, in the cell and in ``result_cf``'s column, take the floor only at the
    months where both models pay below it a contract (:func:`_residue_months`), and none at
    the others.  ``result_cf`` is compared through its frame, column by column, and not
    again as a cell.  On S's in-force twin (``s_in_force``) the cells of :data:`ACQ` are
    compared from ``t = 1``, in the frame and cell by cell: S charges its acquisition at
    its ``t == 0``, the valuation date, on a contract issued 26 months before it.  Returns
    the mismatch lines, empty when the row is S's.
    """
    found = []
    s_cf, sec_cf = s_proj.result_cf(), sec_proj.result_cf()
    keep = columns or [c for c in s_cf.columns if c in sec_cf.columns]
    paid = PAID in keep
    keep = [c for c in keep if c != PAID]
    if s_in_force:
        found += [f"result_cf: {line}" for line in frame_mismatches(
            s_cf, sec_cf, t_offset=month, columns=[c for c in keep if c not in ACQ],
            atol=0.0)]
        later = [c for c in keep if c in ACQ]
        if later:
            found += [f"result_cf from t = 1: {line}" for line in frame_mismatches(
                s_cf.loc[1:], sec_cf.loc[1:], t_offset=month, columns=later, atol=0.0)]
    else:
        found += [f"result_cf: {line}" for line in frame_mismatches(
            s_cf, sec_cf, t_offset=month, columns=keep, atol=0.0)]
    residue = _residue_months(s_proj, sec_proj, month)
    if paid:
        found += [f"result_cf: {line}" for line in _paid_frames(s_cf, sec_cf, month,
                                                                residue)]
    found += [f"result_pols: {line}" for line in frame_mismatches(
        s_proj.result_pols(), sec_proj.result_pols(), t_offset=month, atol=0.0)]
    books = _on_the_books(sec_proj.duration_mth_init())
    if s_in_force:
        books = _from_t1(books)
    exact, floored = _split_paid(books, residue)
    exempt = exempt | {"result_cf"}
    found += _mismatches(s_proj, sec_proj, t_offset=month, exempt=exempt | FLOORED,
                         arg_map=exact, atol=0.0)
    found += _mismatches(s_proj, sec_proj, t_offset=month, arg_map=floored,
                         exempt=(set(s_proj.cells) - FLOORED - {PAID}) | exempt)
    return found


def _continues_s(s_proj, sec_proj, month, exempt, s_in_force=False):
    """Where a committed row departs from S's point ``s_proj`` from S month ``month`` on.

    The splice's comparison (:func:`_compare`), on the committed model at the shipped
    assumptions, under ``exempt``, T2's or T3's.  The shipped 2.5% expense inflation runs
    by completed contract years in S and from the valuation date here (D7), so
    :data:`INFLATED`'s two columns, and :data:`INFLATION_CELLS`, differ by design and are
    left out; the inflation test holds them.  The committed companions re-base each row's
    scenarios to its month, so nothing else moves with the clock, and every other column
    and cell must agree.
    """
    keep = [c for c in s_proj.result_cf().columns if c not in INFLATED]
    return _compare(s_proj, sec_proj, month, exempt | INFLATION_CELLS, keep, s_in_force)


def _case_id(kind, s_point, month):
    """A case's id: ``point1-d60``, ``point2-twin0``, or ``point1-k15`` if issued later."""
    if kind == "future":
        return f"point{s_point}-k{-month}"
    return f"point{s_point}-" + (f"d{month}" if kind == "derived" else f"{kind}{month}")


def _case(case, core, case_id):
    """One parametrized case: run by default if it is in ``core``, else on the full grid."""
    return pytest.param(*case, id=case_id, marks=() if case in core else FULL_ONLY)


def _selected(cases, core):
    """The cases this run makes rows for: the core, or every one under USLIB_SEC_FULL."""
    return [case for case in cases if SEC_FULL or case in core]


# Every row the splice compares, as (row_kind, S point, source_mth), T3's included, and the
# default run's among them; and the switched References' likewise.
GRID = (*IN_FORCE_TWINS, *VARIANT_TWINS, *SPLICES, *(("future", p, -k) for p, k in FUTURES))
CORE_GRID = frozenset({*CORE_SPLICES, *(("future", p, -k) for p, k in CORE_FUTURES)})
GRIDS = {"spliced": (GRID, CORE_GRID),
         "switched": (SWITCHED_GRID, frozenset(SWITCHED_CORE))}


def _s_table_with(variants):
    """S's committed table with ``variants`` appended, under their own point_ids, and the
    premium tax of the splice (:data:`PREMIUM_TAX`) on every point issued at S's t = 0 but
    a variant that sets its own."""
    table = pd.read_csv(model_path(TWIN).parent / "model_point_table.csv",
                        index_col="point_id")
    rows = []
    for point_id, (base, changes) in variants.items():
        row = table.loc[[base]].assign(**changes)
        row.index = pd.Index([point_id], name="point_id")
        rows.append(row)
    table = pd.concat([table, *rows])
    own = [point_id for point_id, (_, changes) in variants.items()
           if "premium_tax_rate" in changes]
    new = (table["duration_mth_init"] == 0) & ~table.index.isin(own)
    return table.assign(premium_tax_rate=table["premium_tax_rate"].where(~new,
                                                                         PREMIUM_TAX))


def _splice_pair(root, which):
    """S and SEC on the splice's inputs under ``which``'s References: ``(s, sec)``.

    S is read from a copy of the product directory whose table has the variants appended
    and the premium tax on its new business (:func:`_s_table_with`), and whose return and
    rate scenarios, programmes, fund sets and GAWA grids are the splice's
    (:data:`SPLICED_EDITS`).  SEC runs on the same tables, and on a model point table of
    its own, built by the generator from the registered spec with its rows replaced by the
    cases this run selects, the core or the full grid (:func:`_selected`), out of this S
    model, so that each row opens with the state of the very run it is compared with; and
    on the two scenario companions the generator builds from it, which re-base the
    edited scenarios to each row's month under an id of their own.  No companion value is
    moved: VA carries no column holding a level a scenario also sets, a past VIX reaching
    the fee only through ``phi_glwb_init``.  Both read ``which``'s References before either
    computes anything.
    """
    s_folder = temp_inputs(root / "s", model_path(TWIN),
                           model_points=_s_table_with(VARIANTS), edits=SPLICED_EDITS)
    s = _read(s_folder, f"s_{which}", REFS[which])
    grid, core = GRIDS[which]
    cases = _selected(grid, core)
    spec = dataclasses.replace(
        SPEC, derived=tuple((p, d) for kind, p, d in cases if kind == "derived"),
        future=tuple((p, -d) for kind, p, d in cases if kind == "future"))
    table, companions = build_sec_table(spec, s)
    assert set(companions) == set(COMPANIONS)
    sec_folder = temp_inputs(root / "sec", model_path(SEC), model_points=table,
                             model_point_file=spec.model_point_file,
                             edits={**SEC_EDITS, **companions})
    return s, _read(sec_folder, f"sec_{which}", REFS[which])


class _Splices:
    """The splice's two pairs of models, the shipped References' and the switched ones'.

    One pair is held at a time: :meth:`pair` reads the pair asked for, closing the other
    first, so that the module never holds both, each with its swept S points, beside the
    committed models.  The tests that read a pair run together in the module's order, so
    each pair is read once a run.  Each S point is swept the first time a case asks for it
    (:meth:`s_point`), and released once the last case this run selects for it has been
    compared (:meth:`done`).  The pair's SEC model's calls of ``min`` and ``max`` are
    listed as it is read (:attr:`bounds`, :class:`_BoundSides`).
    """

    def __init__(self, root):
        self.root, self.which, self.s, self.sec = root, None, None, None
        self.swept, self.left, self.bounds = set(), {}, None

    def pair(self, which):
        """``(s, sec)`` under ``which``'s References, read now if not already held."""
        if which != self.which:
            self.close()
            self.s, self.sec = _splice_pair(self.root / which, which)
            self.which, self.bounds = which, _BoundSides(self.sec)
            grid, core = GRIDS[which]
            self.left = {}
            for _, s_point, _ in _selected(grid, core):
                self.left[s_point] = self.left.get(s_point, 0) + 1
            _freeze()
        return self.s, self.sec

    def s_point(self, which, point_id):
        """S point ``point_id`` of ``which``'s pair, swept (:func:`_sweep_s`)."""
        s, _ = self.pair(which)
        proj = _point(s, point_id)
        if point_id not in self.swept:
            _sweep_s(proj)
            self.swept.add(point_id)
        return proj

    def done(self, which, point_id):
        """Count one compared case of S point ``point_id``; release the point after its
        last, so that the pair holds only the S points cases still to run will read."""
        if which != self.which or point_id not in self.left:
            return
        self.left[point_id] -= 1
        if self.left[point_id] == 0 and point_id in self.swept:
            _release(self.s, _key(self.s, point_id), collect=True)
            self.swept.discard(point_id)

    def close(self):
        """Close the pair held, if any, and collect it.

        Its models are frozen out of the collector with everything else alive, and a frozen
        cycle is never collected, so the freeze is undone first; the next pair's read
        freezes what is then alive.
        """
        if self.which is None:
            return
        gc.unfreeze()
        self.sec.close()
        self.s.close()
        self.which, self.s, self.sec, self.swept, self.left = None, None, None, set(), {}
        self.bounds = None
        gc.collect()


# ---------------------------------------------------------------------------
# Fixtures


@pytest.fixture(scope="module", autouse=True)
def _collector():
    """Undo, as the module ends, the freezes its fixtures made (:func:`_freeze`).

    Set up before every other fixture of the module, it is torn down after them all, once
    every model the module read is closed, and then returns what was frozen to the
    collector and collects it, so that nothing frozen here outlives the module.
    """
    yield
    gc.unfreeze()
    gc.collect()


@pytest.fixture(scope="module")
def sec_read():
    """VA_US_SEC read in place, as committed, and swept once, cold; what it met.

    The model is first asked for ``duration_mth(400)`` on the twin of S point 1, and the
    keys that call leaves in ``duration_mth`` are kept.  Then every committed point is
    swept (:func:`sec_support.sweep`: ``result_cf``, the other reports and the checks), in
    table order and each column in ascending ``t``, under a recursion limit lowered to
    :data:`CALL_DEPTH`, and whatever that raises is kept, point by point, rather than
    raised.  So the record says what a cold model does, which the clock test asserts (D3,
    R2), and every test on the committed model reads a model already swept: the sweep is
    paid once, not once for each.  The sides of the bounds each point's sweep binds are
    kept too, by point (:class:`_BoundSides`), for the sides :data:`BOUND_ELSEWHERE` names
    on the committed rows.  The swept model is then frozen out of the collector
    (:func:`_freeze`).  Returns ``(model, record)``.
    """
    model = _read(model_path(SEC), "sec")
    first = _row(model, "twin", 1, 0)
    record = {"duration_mth(400)": first.duration_mth(400),
              "keys": list(first.cells["duration_mth"].keys()), "deep": [], "bounds": {}}
    labels = model.Data.model_point_table().index
    bounds = _BoundSides(model)
    limit = mx.get_recursion()
    mx.set_recursion(CALL_DEPTH)
    try:
        for key, point_id in zip(point_keys(model), labels):
            with bounds.watch() as won:
                try:
                    sweep(projection(model, key))
                except Exception as err:        # kept, so every point is swept
                    record["deep"].append(f"point {point_id}: the sweep raised "
                                          f"{_raised(err)}")
            record["bounds"][point_id] = won
    finally:
        mx.set_recursion(limit)
    _freeze()
    yield model, record
    model.close()


@pytest.fixture(scope="module")
def sec_model(sec_read):
    """VA_US_SEC read in place, as committed, with every point swept (sec_read)."""
    return sec_read[0]


@pytest.fixture(scope="module")
def s_model():
    """VA_US_S read in place, as committed, with every point swept (``sec_support.sweep``).

    T6 regenerates the SEC files from it, which would otherwise project every S point again
    (USLIB-SEC-PLAN.md §4, *Carried into Phase 1*), and the in-force tests read S's months
    off it.  It is swept by its reports and checks alone: the cells only the splice's
    sweep reaches (:func:`_sweep_s`) are compared there, and the committed rows are
    compared with S frame by frame and in every cell the reports read.  The swept model is
    then frozen out of the collector (:func:`_freeze`).
    """
    model = _read(model_path(TWIN), "s")
    for key in point_keys(model):
        sweep(projection(model, key))
    _freeze()
    yield model
    model.close()


@pytest.fixture(scope="module")
def splices(tmp_path_factory):
    """The splice's pairs of models, one held at a time (:class:`_Splices`)."""
    held = _Splices(tmp_path_factory.mktemp("spliced"))
    yield held
    held.close()


@pytest.fixture(scope="module")
def splice_records():
    """What each splice row was found to do, by ``(which, case)`` (:func:`_record`)."""
    return {}


# ---------------------------------------------------------------------------
# The splice's records
#
# Each T2 and T3 case sweeps its row, records what the rules test and the core grid's reach
# need of it, compares it with S, and releases it: held together, the rows of the full grid
# would hold gigabytes.  The record is made before the comparison, because the comparison
# evaluates SEC's cells at S's own cached arguments, keys SEC never asks for itself among
# them, and the rules test judges what the model asks for.  So each of the two tests reads
# the records, and computes any case no earlier test has recorded, which keeps it whole
# when run alone.


def _cached_args(cells):
    """The argument tuple of every key ``cells`` has cached (:func:`sec_support._args`)."""
    n = len(cells.parameters)
    return [() if n == 0 else (key,) if n == 1 else tuple(key)
            for key in list(cells.keys())]


def _month(x):
    return isinstance(x, int) and not isinstance(x, bool)


def _month_reads(proj, node, memo):
    """The calls keyed by a month that ``node``, a call keyed by none, makes or has made.

    ``node`` is a call of a cell of ``proj`` with no ``t``: one keyed by an age, a count of
    completed years, a policy month, a contract quarter or a subaccount, or by nothing.
    Its precedents keyed by ``t`` are its own reads, and through each precedent of
    ``proj``'s keyed by no month, that precedent's, down every path to the first call
    keyed by ``t``, so that the reads are judged against the month that asked.  ``memo``
    holds each call's reads, once, by cells and arguments.
    """
    key = (node.obj.name, node.args)
    if key not in memo:
        memo[key] = []                      # a call met again on its own path adds nothing
        found = []
        for pred in node.obj.preds(*node.args):
            if pred.obj.parent is not proj:
                continue
            if "t" in (pred.obj.parameters or ()):
                found.append(pred)
            else:
                found += _month_reads(proj, pred, memo)
        memo[key] = found
    return memo[key]


# R2's one admitted read (USLIB-SEC-PLAN.md D11, precised at M2): lapse_wd_factor(t) reads
# whether the contract year of t has a withdrawal at the anniversary that closes it,
# is_wd_year(anniv_mth(t)), up to 11 months ahead.  Admitted by reader and cell, at that
# month alone and inside the frame, and only where the state read depends on no cell of
# FORBIDDEN, the counts and the decrements, the reader itself among them, and on no month
# after that anniversary.  is_wd_year is not in FORBIDDEN: the year's answer rests on
# is_wd_year at earlier anniversaries, through the bonus, the benefit base and the rider
# fee, which R2 allows (§7.11, *Carried into VA (M9)*).
LOOK_AHEAD = frozenset({("lapse_wd_factor", "is_wd_year")})
FORBIDDEN = frozenset({"pols_if", "pols_if_at", "pols_new_biz", "pols_death", "pols_lapse",
                       "pols_maturity", "pols_decr", "lapse_rate", "lapse_rate_mth",
                       "lapse_wd_factor", "lapse_dyn_mult", "mort_rate", "mort_rate_mth",
                       "policy_count", "pols_if_init"})


def _closing(proj, t, u):
    """Whether month ``u`` is the anniversary closing the contract year of ``t``, ahead of
    it and inside the frame."""
    return (u == proj.anniv_mth(t) and t < u <= t + 11
            and proj.duration_mth(u) % 12 == 11 and u < proj.proj_len())


def _closure(proj, node, memo):
    """What ``node``'s value rests on: ``(latest month, FORBIDDEN cells)`` over its
    precedents.

    The latest ``t`` of any call of ``proj``'s that ``node`` reaches through its
    precedents, itself included, and the names of :data:`FORBIDDEN` among them, walked
    down modelx's dependency graph without recursion, so that a chain as long as the frame
    walks too.  ``memo`` holds each call's answer once, by cells and arguments, so the
    thousands of reads a row admits share the walk.
    """
    stack = [node]
    preds = {}
    while stack:
        n = stack[-1]
        key = (n.obj.name, n.args)
        if key in memo:
            stack.pop()
            continue
        if key not in preds:
            preds[key] = [p for p in n.obj.preds(*n.args) if p.obj.parent is proj]
            todo = [p for p in preds[key] if (p.obj.name, p.args) not in memo]
            if todo:
                stack.extend(todo)
                continue
        params = n.obj.parameters or ()
        latest = (n.args[params.index("t")] if "t" in params
                  and _month(n.args[params.index("t")]) else -1)
        reached = {n.obj.name} & FORBIDDEN
        for p in preds.pop(key):
            their_latest, theirs = memo[(p.obj.name, p.args)]
            latest, reached = max(latest, their_latest), reached | theirs
        memo[key] = (latest, frozenset(reached))
        stack.pop()
    return memo[(node.obj.name, node.args)]


def _rule_breaches(proj):
    """R1, R1a and R2 on one row, once it has been swept.

    ``{"negative", "early", "ahead", "condition", "year", "admitted"}``: every cached call
    with a negative argument, a month, an age, a year, a quarter or a policy month; every
    read keyed by a month before ``t_entry()`` of a call keyed by a month at or after it;
    every read keyed by a month beyond ``t + 1`` of a call keyed by ``t``, but R2's
    admitted read (:data:`LOOK_AHEAD`) at the closing anniversary inside the frame; every
    admitted read whose state rests on a count, a decrement or a month after the
    anniversary (:func:`_closure`); every keyed reader read below the books, an age below
    the row's attained age in its first month on the books, a count of completed years or
    a policy month below its own there, or a contract quarter before the one under way
    there; and how many reads were admitted.  A read is a precedent of the call's, as
    modelx's dependency graph records it, keyed by a month, or one a precedent keyed by no
    month makes on the call's behalf (:func:`_month_reads`).
    """
    entry = proj.t_entry()
    negative, early, ahead, condition, year = [], [], [], [], []
    admitted = 0
    memo, closures = {}, {}
    for name, cells in proj.cells.items():
        t_pos = cells.parameters.index("t") if "t" in cells.parameters else None
        for args in _cached_args(cells):
            if any(_month(a) and a < 0 for a in args):
                negative.append(f"{name}{args}")
            if t_pos is None:
                continue
            t = args[t_pos]
            for pred in cells.preds(*args):
                params = getattr(pred.obj, "parameters", None) or ()
                if "t" in params:
                    reads, via = [pred], ""
                elif pred.obj.parent is proj:
                    reads = _month_reads(proj, pred, memo)
                    via = f"{pred.obj.name}{pred.args} -> "
                else:
                    continue
                for node in reads:
                    u = node.args[node.obj.parameters.index("t")]
                    if not _month(u):
                        continue
                    if u < entry <= t:
                        early.append(f"{name}{args} -> {via}{node.obj.name}{node.args}")
                    if u <= t + 1:
                        continue
                    if (name, node.obj.name) in LOOK_AHEAD and _closing(proj, t, u):
                        admitted += 1
                        latest, counts = _closure(proj, node, closures)
                        if latest > u or counts:
                            condition.append(f"{name}{args} -> {node.obj.name}{node.args}: "
                                             f"rests on month {latest}, {sorted(counts)}")
                        continue
                    ahead.append(f"{name}{args} -> {via}{node.obj.name}{node.args}")
    lowest = {**{name: proj.age(entry) for name in AGE_READERS},
              **{name: proj.duration(entry) for name in YEAR_READERS},
              **{name: proj.duration_mth(entry) for name in MONTH_READERS},
              **{name: proj.contract_quarter(entry) for name in QUARTER_READERS}}
    for name, low in lowest.items():
        year += [f"{name}{args}" for args in _cached_args(proj.cells[name])
                 if args[0] < low]
    return {"negative": negative, "early": early, "ahead": ahead, "condition": condition,
            "year": year, "admitted": admitted}


# What test_the_core_grid_reaches_every_branch asks of the core's rows in the model's own
# values, which no column of the table shows: each holds of some core row, or of a core row
# in some month of its frame.  At the valuation date, the kinds of valuation month; a
# depleted opening, with and without a withdrawal, and the GLWB paid from the columns; the
# year to date read by a later withdrawal of the year, and by one in the valuation month;
# the year-open roll-up base read by a withdrawal, from its column and from the frame at
# t_entry() itself, the two sides of its boundary; the year flag alone marking the year;
# the step-up base's history winning, its value at the valuation month winning, and its
# history above the next year's, the two sides of the base's two boundaries; the VIX
# prior from its column binding; the GWB Adjustment binding at t = 0; and a contract that
# has withdrawn, but not in the year under way.  Later in the frame, each event and each
# bound the product has, on the shipped References with the splice's assumptions on.
def _year(p):
    """The months of the contract year under way at the valuation date, on the books."""
    return range(0, min(p.anniv_mth(0) + 1, p.proj_len()))


def _frame(p):
    return range(p.t_entry(), p.proj_len())


def _any(p, holds):
    return any(holds(t) for t in _frame(p))


def _quarter_ends(p, a):
    """The quarterly anniversaries of the contract year closing at month ``a``, on the
    books."""
    return [u for u in (a, a - 3, a - 6, a - 9) if p.t_entry() <= u < p.proj_len()]


def _hq_history_wins(p):
    """In force on the highest quarterly basis, the column above every quarter end of the
    year under way on the books."""
    if not (p.duration_mth_init() > 0 and p.is_stepup_highest_quarterly()):
        return False
    a = p.anniv_mth(0)
    return a < p.proj_len() and p.stepup_base_pp_ytd_init() > max(
        p.av_pp(u) for u in _quarter_ends(p, a))


def _hq_valuation_month_wins(p):
    """The account value at the valuation month, a quarter end, above the year's others
    and the column: the frame's read at ``t_entry()`` itself."""
    if not (p.duration_mth_init() > 0 and p.is_stepup_highest_quarterly()):
        return False
    a = p.anniv_mth(0)
    if a >= p.proj_len() or a not in (3, 6, 9):
        return False
    others = [p.av_pp(u) for u in _quarter_ends(p, a) if u > 0]
    return p.av_pp(0) > max([*others, p.stepup_base_pp_ytd_init()])


def _hq_history_above_next_year(p):
    """Valued in a contract year's last month, the column above every quarter end of the
    year after: the column's read confined to the year under way."""
    if not (p.duration_mth_init() > 0 and p.is_stepup_highest_quarterly()
            and p.duration_mth_init() % 12 == 11):
        return False
    a = p.anniv_mth(0) + 12
    return a < p.proj_len() and p.stepup_base_pp_ytd_init() > max(
        p.av_pp(u) for u in _quarter_ends(p, a))


def _vix_prior_binds(p):
    """In force on the VIX fee past the first quarter, the raw rate of the quarter under
    way more than a band from the column's prior, so that the prior moves the fee."""
    if not (p.duration_mth_init() > 0 and p.is_fee_reset_vix()):
        return False
    k = p.contract_quarter(0)
    if k <= 1:
        return False
    raw = p.fee_rate_vix_raw(p.phi_glwb_curr, p.vix_sq(k))
    return abs(raw - p.phi_glwb_init()) > p.vix_band


def _vix_raws(p):
    """``(quarter, raw rate)`` at each quarterly anniversary on the books after the first
    quarter under way."""
    out = []
    for t in _frame(p):
        if p.is_quarterly_anniv(t):
            k = p.contract_quarter(t)
            if k > max(p.contract_quarter(p.t_entry()), 1):
                out.append((k, p.fee_rate_vix_raw(p.phi_glwb_curr, p.vix_sq(k))))
    return out


AT_VALUATION = {
    "in force mid-year": lambda x: (x.duration_mth_init() > 0
                                    and x.duration_mth_init() % 12 != 0),
    "in force at a year start": lambda x: (x.duration_mth_init() > 0
                                           and x.duration_mth_init() % 12 == 0),
    "in the first policy year": lambda x: 0 < x.duration_mth_init() < 12,
    "in a year's last month": lambda x: (x.duration_mth_init() > 0
                                         and x.duration_mth_init() % 12 == 11),
    "depleted at the opening": lambda x: x.depleted_open(0),
    "depleted at the opening on an account value above 0": lambda x: (
        x.depleted_open(0) and x.av_pp_init() > 0.0),
    "depleted at the opening on an account value below 0": lambda x: (
        x.depleted_open(0) and x.av_pp_init() < 0.0),
    "depleted without a withdrawal": lambda x: x.depleted_open(0) and not x.has_wd_init(),
    "the GLWB paid at t = 0 from the columns": lambda x: x.glwb_payment_pp(0) > 0.0,
    "the GLWB paid at t = 0 from the GWB's column, below the GAWA's": lambda x: (
        x.glwb_payment_pp(0) > 0.0
        and x.glwb_payment_pp(0) == x.gwb_pp_init() < x.gawa_pp_init()),
    "the account value runs out in the valuation month": lambda x: (
        x.duration_mth_init() > 0 and not x.depleted_open(0) and x.depleted_flag(0)),
    "a premium at t = 0 on a contract that has withdrawn": lambda x: (
        x.has_wd_init() and x.prem_to_av_pp(0) > 0.0),
    "the year to date read by a withdrawal": lambda x: (
        x.sum_wd_pp_ytd_init() > 0.0 and any(x.wd_pp(t) > 0.0 for t in _year(x))),
    "valued in a withdrawal month after another that year": lambda x: (
        x.sum_wd_pp_ytd_init() > 0.0 and x.wd_pp(0) > 0.0),
    "the year-open RB read by a withdrawal": lambda x: (
        x.duration_mth_init() > 0 and x.duration_mth_init() % 12 != 0
        and x.is_gmdb_rollup() and any(x.wd_pp(t) > 0.0 for t in _year(x))),
    "the year-open RB read from the frame at t_entry() by a withdrawal": lambda x: (
        x.duration_mth_init() % 12 == 11 and x.is_gmdb_rollup() and any(
            x.wd_pp(t) > 0.0 for t in range(1, min(13, x.proj_len())))),
    "the year flag alone marks the year": lambda x: (
        x.wd_this_year_init() and not any(x.is_wd_taken(t) for t in _year(x))),
    "the step-up base's history wins": _hq_history_wins,
    "the step-up base's value at the valuation month wins": _hq_valuation_month_wins,
    "the step-up base's history above the next year's": _hq_history_above_next_year,
    "the VIX prior from the column binds": _vix_prior_binds,
    "the GWB Adjustment binds at t = 0": lambda x: (
        x.is_gwb_adj_date(0) and not x.has_wd_by(0)
        and x.adj_pp_bef_anniv(0) > x.gwb_pp_aft_stepup(0)),
    "a withdrawal already taken, none this year": lambda x: (
        x.has_wd_init() and not x.wd_this_year_init()
        and x.duration_mth_init() % 12 != 0),
}

IN_FRAME = {
    "depletion": lambda x: _any(x, lambda t: x.depleted_flag(t) and not x.depleted_open(t)),
    "a first withdrawal": lambda x: _any(x, x.is_first_wd),
    "an excess withdrawal": lambda x: _any(
        x, lambda t: x.wd_pp(t) > 0.0 and x.sum_wd_pp(t) > x.wd_limit_pp(t)),
    "a withdrawal mid-year": lambda x: _any(
        x, lambda t: x.wd_pp(t) > 0.0 and x.duration_mth(t) % 12 != 0),
    "a withdrawal in a year's last month": lambda x: _any(
        x, lambda t: x.wd_pp(t) > 0.0 and x.duration_mth(t) % 12 == 11),
    "a scheduled premium after issue": lambda x: _any(
        x, lambda t: x.duration_mth(t) > 0 and x.prem_scheduled_pp(t) > 0.0),
    "a premium after a withdrawal": lambda x: _any(
        x, lambda t: t > x.t_entry() and x.has_wd_by(t - 1) and x.prem_to_av_pp(t) > 0.0),
    "a first-year withdrawal on the roll-up death benefit, issued at t = 0": lambda x: (
        x.duration_mth_init() == 0 and x.is_gmdb_rollup()
        and any(x.wd_pp(t) > 0.0 for t in range(min(12, x.proj_len())))),
    "a step-up": lambda x: _any(x, x.is_stepup),
    "a bonus": lambda x: _any(x, lambda t: x.bonus_pp(t) > 0.0),
    "the Bonus Period restarts": lambda x: _any(
        x, lambda t: t > x.t_entry() and x.bonus_end(t) != x.bonus_end(t - 1)),
    "the GWB Adjustment binds": lambda x: _any(
        x, lambda t: x.is_gwb_adj_date(t) and not x.has_wd_by(t) and not x.depleted_open(t)
        and x.adj_pp_bef_anniv(t) > x.gwb_pp_aft_stepup(t)),
    "a payment not for life capped at the GWB": lambda x: (not x.forlife_flag()) and _any(
        x, lambda t: t > x.t_entry() and x.glwb_payment_pp(t) > 0.0
        and x.gwb_pp(t - 1) < x.gawa_pp(t - 1)),
    "the death benefit's growth cutoff": lambda x: (not x.is_gmdb_basic()) and _any(
        x, lambda t: x.is_anniv(t) and x.age_at_anniv(t) > x.gmdb_growth_cutoff_age),
    "the maintenance fee charged": lambda x: _any(x, lambda t: x.maint_fee_pp_due(t) > 0.0),
    "the maintenance fee waived": lambda x: _any(
        x, lambda t: x.is_anniv(t) and not x.depleted_open(t)
        and x.maint_fee_pp_due(t) == 0.0),
    "charges capped at the AV": lambda x: _any(
        x, lambda t: x.charge_pp_due(t) > 0.0 and x.charge_scale(t) < 1.0),
    "a withdrawal capped at the AV": lambda x: _any(
        x, lambda t: x.wd_pp_due(t) > _at(x, "av_pp_at", t, "BEF_WD")),
    "a withdrawal charge": lambda x: _any(x, lambda t: x.wd_charge_pp(t) > 0.0),
    "the lapse ITM floor": lambda x: _any(
        x, lambda t: x.av_pp(t) > 0.0 and x.lapse_dyn_mult(t) == x.lapse_itm_lower),
    "the lapse ITM cap": lambda x: _any(
        x, lambda t: x.av_pp(t) > 0.0 and x.lapse_dyn_mult(t) == x.lapse_itm_upper),
    "the shock lapse year": lambda x: _any(
        x, lambda t: x.policy_year(t) == x.surr_charge_years + 1 and x.lapse_rate(t) > 0.0),
    "the withdrawal year's lapse factor": lambda x: _any(
        x, lambda t: x.lapse_rate(t) > 0.0 and x.lapse_wd_factor(t) != 1.0),
    "the VIX band": lambda x: x.is_fee_reset_vix() and any(
        abs(abs(x.phi_glwb_vix(k) - x.phi_glwb_vix(k - 1)) - x.vix_band) < 1e-15
        and x.phi_glwb_vix(k) != raw for k, raw in _vix_raws(x)),
    "the VIX corridor's high": lambda x: x.is_fee_reset_vix() and any(
        x.phi_glwb_vix(k) == x.vix_corridor_hi for k, _ in _vix_raws(x)),
    "the CMT floor": lambda x: x.is_rollup_cmt_linked() and _any(
        x, lambda t: x.is_anniv(t) and x.rollup_rate(t) == x.cmt_floor),
    "the CMT cap": lambda x: x.is_rollup_cmt_linked() and _any(
        x, lambda t: x.is_anniv(t) and x.rollup_rate(t) == x.cmt_cap),
    "the older roll-up rate": lambda x: (x.is_gmdb_rollup()
                                         and x.rollup_pct() == x.rollup_pct_old),
    "not for life": lambda x: not x.forlife_flag(),
    "premium tax, commission and acquisition at issue": lambda x: _any(
        x, lambda t: x.duration_mth(t) == 0 and x.premium_taxes(t) > 0.0
        and x.commissions(t) > 0.0 and x.expenses(t) > x.expense_acq * x.pols_if(t) > 0.0),
    "the female table": lambda x: x.model_point()["sex"] == "F" and _any(
        x, lambda t: x.pols_death(t) > 0.0),
}

# What the switched References' core must reach in the frame: each bound S ships idle
# binding with an effect.
SWITCHED_FRAME = {
    "the GWB cap": lambda x: _any(x, lambda t: x.gwb_pp(t) >= x.gwb_cap),
    "the VIX corridor's low": lambda x: x.is_fee_reset_vix() and any(
        x.phi_glwb_vix(k) == x.vix_corridor_lo for k, _ in _vix_raws(x)),
    "the lapse capped at 1": lambda x: _any(
        x, lambda t: x.av_pp(t) > 0.0
        and x.lapse_rate_base(t) * x.lapse_dyn_mult(t) * x.lapse_wd_factor(t) > 1.0
        and x.lapse_rate(t) == 1.0),
    "a Bonus-Base-raising step-up past the restart age": lambda x: _any(
        x, lambda t: x.is_stepup(t) and x.age_at_anniv(t) > x.bonus_restart_age
        and x.gwb_pp_aft_stepup(t) > x.bb_pp_bef_anniv(t)),
    "one at the restart age, which restarts the Bonus Period": lambda x: _any(
        x, lambda t: x.is_stepup(t) and x.age_at_anniv(t) == x.bonus_restart_age
        and x.gwb_pp_aft_stepup(t) > x.bb_pp_bef_anniv(t)
        and x.bonus_end(t) == x.policy_year(t) + x.bonus_period_years),
    "one a year past the restart age, which does not": lambda x: _any(
        x, lambda t: x.is_stepup(t) and x.age_at_anniv(t) == x.bonus_restart_age + 1
        and x.gwb_pp_aft_stepup(t) > x.bb_pp_bef_anniv(t)
        and x.bonus_end(t) == x.bonus_end(t - 1)),
}
REACH = {"spliced": (AT_VALUATION, IN_FRAME), "switched": ({}, SWITCHED_FRAME)}


def _branches(x, kind, which):
    """The names in ``which``'s reach dicts (:data:`REACH`) that hold of row ``x``.

    The dict of the valuation date asks about the state at the valuation date, which only
    a row in force holds; the frame's about the frame, which a future row has too, and
    which alone has the premium tax, the commission and the acquisition of new business.
    """
    at, frame = REACH[which]
    reached = set() if kind == "future" else {what for what, holds in at.items()
                                              if holds(x)}
    return reached | {what for what, holds in frame.items() if holds(x)}


class _BoundSides:
    """Which side of each ``min`` and ``max`` in a model's ``Projection`` wins, by case.

    Every bound binds, with an effect, on a row the default run compares with S cell by
    cell, and the core-reach test checks each by the values it bounds, never by the
    bounded output (USLIB-SEC-PLAN.md §7.6, *Carried into every product still to come*).
    So, while a splice case is swept and compared (:func:`_splice_case`), ``builtins.min``
    and ``max`` are wrapped (:meth:`watch`): a call made from one of the model's formulas
    with two arguments or more, not all equal, records each argument equal to its result
    as a side that won, ``(cell, call, i)``, the cell, the call's text with its spaces
    collapsed and the argument's position.  Every other call passes straight through.  The
    sides are the formulas' own calls, found in their source (:attr:`sides`); a call is
    told apart by its position in its formula's code, which Python gives from 3.11, and
    before it :meth:`watch` records nothing.
    """

    def __init__(self, model):
        self.codes = {cells.formula.func.__code__: name
                      for name, cells in model.Projection.cells.items()}
        self.sites, self.positions = {}, {}
        for name, cells in model.Projection.cells.items():
            source = cells.formula.source
            fn = ast.parse(source).body[0]
            for node in ast.walk(fn):
                if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                        and node.func.id in ("min", "max") and len(node.args) > 1):
                    call = " ".join(ast.get_source_segment(source, node).split())
                    self.sites[name, node.lineno - fn.lineno, node.col_offset] = (
                        name, call, len(node.args))
        named = collections.Counter(site[:2] for site in self.sites.values())
        twice = [site for site, n in named.items() if n > 1]
        assert not twice, f"a cell calls the same min or max twice: {twice}"
        self.sides = {(name, call, i) for name, call, n in self.sites.values()
                      for i in range(n)}

    def _wrap(self, builtin, won):
        def call(*args, **kwargs):
            result = builtin(*args, **kwargs)
            frame = sys._getframe(1)
            code = frame.f_code
            if code in self.codes and len(args) > 1 and not kwargs:
                if code not in self.positions:
                    self.positions[code] = list(code.co_positions())
                line, _, col, _ = self.positions[code][frame.f_lasti // 2]
                site = self.sites.get((self.codes[code], line - code.co_firstlineno, col))
                try:
                    if site and any(a != args[0] for a in args[1:]):
                        won.update((*site[:2], i) for i, a in enumerate(args)
                                   if a == result)
                except (TypeError, ValueError):     # an array has no one side: not a bound
                    pass
            return result
        return call

    @contextlib.contextmanager
    def watch(self):
        """Wrap the two builtins while the block runs, yielding the sides that won."""
        won = set()
        if sys.version_info < (3, 11):
            yield won
            return
        saved = builtins.min, builtins.max
        builtins.min, builtins.max = self._wrap(saved[0], won), self._wrap(saved[1], won)
        try:
            yield won
        finally:
            builtins.min, builtins.max = saved


# The sides of a min or max no core row binds, each with its reason, which the core-reach
# test holds to: a side named here that a core row binds fails it, as does a side named
# nowhere that none binds.  Two are SEC's own, the roll-forward checks' tolerance scaled by
# a count above 1, which the million-contract test reads.  Eight cannot bind, each by a
# premise the model's own cells hold: a withdrawal is capped at the account value before it
# (wd_pp), so neither excess passes what the withdrawal's other part leaves of that value,
# no pro-rata reduction passes 1 and no withdrawal's part above the earnings passes the
# premium left; the Remaining Premium's reduction is capped at that premium; a payment not
# for life is capped at the GWB; cover ends at an anniversary; and the year's
# dollar-for-dollar use, at most the largest allowance of the year, a roll-up rate times
# the year-open base, stays below the base before the anniversary while every roll-up rate
# is below 1 (8% at most, cmt_cap, as shipped) and the opening use is S's.  The probe that
# listed them, over every month of every point of S on the splice's inputs, its variants
# among them, under both sets of References, and over every row of both full grids, found
# none of these sides winning.
IDLE_SIDES = {
    ("check_av_roll_fwd", "max(policy_count(), 1.0)", 0): "SEC's own: a count above 1",
    ("check_pols_roll_fwd", "max(policy_count(), 1.0)", 0): "SEC's own: a count above 1",
    ("excess_factor", "max(0.0, 1.0 - wd_excess_pp(t) / base)", 0):
        "cannot bind: the excess is at most what the part within the limit leaves",
    ("gmdb_wd_factor", "max(0.0, 1.0 - gmdb_wd_excess_pp(t) / base)", 0):
        "cannot bind: the excess is at most what the dollar-for-dollar part leaves",
    ("rb_pp_at", "max(0.0, 1.0 - wd_pp(t) / base)", 0):
        "cannot bind: a withdrawal is at most the account value before it",
    ("rp_reduction_pp", "min(rp, max(0.0, wd_pp(t) - earnings))", 0):
        "cannot bind: a withdrawal is at most the account value before it",
    ("rp_pp", "max(0.0, prev + premium_pp(t) - rp_reduction_pp(t))", 0):
        "cannot bind: the reduction is capped at the premium left",
    ("gwb_pp", "max(0.0, prev - glwb_payment_pp(t))", 0):
        "cannot bind: a payment not for life is capped at the GWB",
    ("is_wd_year", "min(first + 12, proj_len())", 1):
        "cannot bind: cover ends at an anniversary",
    ("rb_pp", "max(0.0, (r - gmdb_dfd_acc_pp(t)) * gmdb_factor_acc(t))", 0):
        "cannot bind: the year's dollar-for-dollar use stays below the base while every "
        "roll-up rate is below 1",
}

# The sides that bind on rows outside the splice's core, each compared with S cell by cell
# by the test named, which asserts that the side wins there (:class:`_BoundSides`): the
# GWB above the GWB Adjustment on its date, at the shipped 105% on the committed rows of
# the never-withdrawing contracts, where the splice's 200% puts the adjustment above the
# GWB on every row; and the mortality's age clamp, on a table that stops below cover,
# where no table the splice reads does.
BOUND_ELSEWHERE = {
    ("gwb_pp", "max(g, adj_pp_bef_anniv(t))", 0):
        "test_the_opening_state_is_what_s_carries_into_the_valuation_month",
    ("mort_rate_base_at", "min(x, top)", 1):
        "test_a_table_shortened_below_its_cover_reads_its_last_row_as_s_does",
}


def _record(which, case, proj):
    """Sweep the splice row ``proj`` of ``case`` and record what the rules test needs of it.

    :func:`_rule_breaches`'s record, with the row's :func:`_branches`.  A row that raises is
    recorded as raising, which the rules test reports.
    """
    try:
        _sweep_sec(proj)
        record = _rule_breaches(proj)
        record["branches"] = _branches(proj, case[0], which)
        record["raised"] = None
    except Exception as err:                    # recorded, and reported by the rules test
        record = {"negative": [], "early": [], "ahead": [], "condition": [], "year": [],
                  "admitted": 0, "branches": set(), "raised": _raised(err)}
    return record


def _record_of(splices, records, which, case):
    """The record of ``case``, from the case that compared its row or, failing it, now.

    A row no case has compared is compared here, its mismatches left to its own case, so
    that its record holds the sides of each bound the comparison's calls bind too.
    """
    if (which, case) not in records:
        _splice_case(splices, records, which, case)
    return records[which, case]


def _future_facts(proj, k):
    """What a row issued ``k`` months on holds before issue, and what it reads (R1, D4).

    The pre-issue rows of the four reports are present, and zeros; the contracts arrive in
    month ``k`` as new business; every decrement rate is the float 0.0 before issue; and no
    reader keyed by an age, a count of completed years, a policy month or a contract
    quarter has been read below the contract's first, so no rate read its table there.
    Returns the faults found.
    """
    faults = []
    for report in REPORTS:
        frame = proj.cells[report]()
        if list(frame.index[:k]) != list(range(k)):
            faults.append(f"{report}: no row for each month before issue")
        numeric = frame.loc[:k - 1].select_dtypes("number")
        if not (numeric == 0.0).all().all():
            faults.append(f"{report}: a number before issue")
    if not proj.pols_new_biz(k) == proj.policy_count() == 1.0:
        faults.append(f"new business at k: {proj.pols_new_biz(k)}")
    for name in DECREMENT_RATES:
        early = [(t, proj.cells[name](t)) for t in range(k)]
        if any((type(rate), rate) != (float, 0.0) for _, rate in early):
            faults.append(f"{name} before issue: {early[:5]}")
    floors = {**{name: proj.age_at_entry() for name in AGE_READERS},
              **{name: 0 for name in (*YEAR_READERS, *MONTH_READERS)},
              **{name: 1 for name in QUARTER_READERS}}
    for name, lowest in floors.items():
        low = [args for args in _cached_args(proj.cells[name]) if args[0] < lowest]
        if low:
            faults.append(f"{name} read below {lowest}: {low[:5]}")
    return faults


# ---------------------------------------------------------------------------
# T2 -- the splice


def _splice_case(splices, records, which, case):
    """Record, compare and release the row of ``case`` in ``which``'s pair (T2, T3).

    Returns the mismatches with S, then, on a row issued later, :func:`_future_facts`'s.
    The S point is counted done either way (:meth:`_Splices.done`).  The sides of SEC's
    bounds the sweep and the comparison bind are kept in the record, as ``bounds``
    (:class:`_BoundSides`).
    """
    kind, s_point, month = case
    _, sec = splices.pair(which)
    key = _row_key(sec, *case)
    try:
        proj = projection(sec, key)
        s_proj = splices.s_point(which, s_point)
        with splices.bounds.watch() as won:
            records[which, case] = {**_record(which, case, proj), "bounds": won}
            exempt = FUTURE_EXEMPT if kind == "future" else SPLICE_EXEMPT
            found = _compare(s_proj, proj, month, exempt, s_in_force=case in IN_FORCE_TWINS)
            if kind == "future":
                found += _future_facts(proj, -month)
        return found
    finally:
        _release(sec, key, collect=True)
        splices.done(which, s_point)


@pytest.mark.parametrize(
    "kind, s_point, month",
    [_case(case, CORE_SPLICES, _case_id(*case))
     for case in (*IN_FORCE_TWINS, *VARIANT_TWINS, *SPLICES)])
def test_an_in_force_point_continues_its_s_projection(splices, splice_records, kind,
                                                      s_point, month):
    """Opened with S's state at month d, the point is S from d on, in every cell of S's.

    And issued at the valuation date, each variant's twin is its S point, compared cell
    by cell as a restated row is.

    This is the test that says the opening state is complete: a state column the SEC row
    did not carry, or carried from the wrong instant, would make SEC part from S here, and
    nowhere else, because on a point issued at ``t = 0`` the two clocks coincide and the
    opening state is zero.  For the same reason it is the test that catches a policy month
    passed as ``t`` (R1a), a year-to-date value restarted at the valuation date, a
    year-open value read at the wrong anniversary, and a scenario read on the wrong clock:
    each row reads S's scenarios re-based to its own month, and S's paths step at months
    of their own.  S's own in-force point 2 is a case too, at offset 0, where S projects
    it from: its twin reproduces S's frame from the valuation date, the worked example's
    27th policy month at its ``t = 0``, S's acquisition at its ``t == 0`` apart.  The frame
    comparisons read SEC row ``t`` against S row ``t + d`` in every column of ``result_cf``
    and of ``result_pols`` both reports hold, and fail frames that end apart.  The cell
    comparison then evaluates every cell of S's but :data:`SPLICE_EXEMPT`, at every
    argument S cached inside its own frame from month ``d`` on, moved onto SEC's clock, to
    1e-9 relative with no absolute floor but on the residuals (:func:`_compare`): each
    subaccount and the account value at every timing, the seven bases, the GAWA% and the
    Bonus Period's end, the withdrawal status, the year to date, the year-open roll-up
    base, the step-up base, the VIX fee, the depletion, the counts and the reports among
    them.  The quarters before the books are skipped (:func:`_on_the_books`).  An S cell
    this model lacked would fail it.

    The row is swept and recorded for the rules test first (:func:`_record`), then
    compared, and released either way.
    """
    found = _splice_case(splices, splice_records, "spliced", (kind, s_point, month))
    assert not found, f"{len(found)} mismatches, first:\n  " + "\n  ".join(found[:20])


# ---------------------------------------------------------------------------
# T3 -- future new business


@pytest.mark.parametrize(
    "s_point, k",
    [_case(case, CORE_FUTURES, _case_id("future", case[0], -case[1]))
     for case in FUTURES])
def test_future_new_business_is_the_s_projection_k_months_on(splices, splice_records,
                                                             s_point, k):
    """Issued k months after the valuation date, the point is S's projection k months on.

    SEC rows ``k ..`` are S rows ``0 ..``, ending together at the end of cover, in
    ``result_cf`` and in every column of ``result_pols`` S's has, and every cell of S's but
    :data:`FUTURE_EXEMPT` agrees at every argument S cached inside its own frame, moved
    ``k`` later, ``result_av`` and ``result_bases`` included, to 1e-9 relative with no
    absolute floor (:func:`_compare`).  An S cell this model lacked would fail it.  The
    row's scenarios are copies of S's moved ``k`` months later, with no level before issue,
    so a scenario read there raises inside the comparison.

    Then :func:`_future_facts`, R1 and D4's base rule made testable: before issue every row
    of the four monthly reports is present, and zeros; the contracts arrive in month ``k``
    as new business; every decrement rate is the float 0.0 before issue; and no age, year,
    policy month or quarter has been read below the contract's first, so no rate read its
    table there.  A rate left unguarded before issue still gives the right numbers, a
    count of 0 times the rate, but it is not 0.0 there, and it reads its table at an age or
    a year the contract never reaches: the last two checks see it, and the guard test does
    too.  (A recursion based at ``t == 0`` rather than at ``t_entry()`` gives the right
    numbers as well, every cell before issue holding its guard's value; the rules test sees
    it, as a read before the books.)  The pre-issue rows are asserted present before they
    are asserted zero: a frame that opened at issue would have none, its zeros would hold
    of nothing, and the comparisons with S, which start at issue, would not see it.  The
    row is recorded for the rules test first, and released after.
    """
    found = _splice_case(splices, splice_records, "spliced", ("future", s_point, -k))
    assert not found, f"{len(found)} faults, first:\n  " + "\n  ".join(found[:20])


# ---------------------------------------------------------------------------
# The values outside cover


def _monthly_args(p, name, cells, t):
    """Every argument tuple Phase 2's full sweep calls monthly cell ``name`` with at ``t``.

    ``t`` alone; ``t`` with each timing, each kind, the kind-less total too, or each
    subaccount, the subaccount's timings with it; or ``t`` with each of the rate
    scenario's two names, each passed through :func:`_code`.
    """
    params = tuple(cells.parameters)
    if params == ("t",):
        return [(t,)]
    if name in TIMED:
        return [(t, _code(p, label)) for label in TIMED[name]]
    if name in KINDED:
        totals = [(t,)] if name in ("claims", "claims_over_av") else []
        return totals + [(t, _code(p, kind)) for kind in KINDS]
    if params == ("t", "i"):
        return [(t, i) for i in p.sub_ids()]
    if params == ("t", "i", "timing"):
        return [(t, i, _code(p, label)) for i in p.sub_ids() for label in AV_TIMINGS]
    if params == ("t", "name"):
        return [(t, "vix_sq"), (t, "cmt10")]
    raise AssertionError(f"{name}{params}: a monthly cell _monthly_args lacks")


def _outside_cover_faults(p, where):
    """Where ``p``, an ItemSpace that has evaluated nothing, answers wrongly outside cover.

    In every month before issue and at ``t = proj_len()``, the first month after cover,
    which the count's and the account value's look-ahead reads: first every cell of
    :data:`OUTSIDE_COVER`, each of :data:`TIMED` at each of its timings, the
    :data:`KINDED` cells at each kind and the subaccount cells at each subaccount, against
    its value and its type; then whether any of :data:`IN_COVER_ONLY` was evaluated on the
    way, which only a fresh ItemSpace can say.  Then every monthly cell is called at those
    months, as Phase 2's full sweep will call it, with each of its arguments
    (:func:`_monthly_args`), the scenario readers before issue apart, which raise there by
    design (:func:`_scenario_faults`): none may raise or return a numpy type, and
    afterwards none of the readers keyed by an age, a year, a policy month or a quarter
    (:data:`KEYED_READERS`) may hold a key, and no cell keyed by the month may hold one
    past ``t = proj_len()``, the last month Phase 2's ``t`` cache holds: a cell that reads
    ``t + 1`` is guarded there.  A cell that raises is reported as a fault too, so the scan
    goes on.
    """
    faults = []
    entry = p.t_entry()
    months = [*range(entry), p.proj_len()]

    def call(name, args, want=None):
        try:
            got = p.cells[name](*args)
        except Exception as err:            # reported, so the scan goes on
            faults.append(f"{where}: {name}{args} raised {_raised(err)}")
            return
        if want is not None and (got != want or type(got) is not type(want)):
            faults.append(f"{where}: {name}{args} = {got!r}, not {want!r}")
        if isinstance(got, (np.generic, np.ndarray)):
            faults.append(f"{where}: {name}{args} is a numpy {type(got).__name__}")

    def reached(names):
        found = {name: list(p.cells[name].keys())[:5] for name in names}
        return {name: keys for name, keys in found.items() if keys}

    for t in months:
        for name, want in OUTSIDE_COVER.items():
            if isinstance(want, tuple):
                want = _code(p, want[0] if t < entry else want[1])
            call(name, (t,), want)
        for name, labels in TIMED.items():
            for label in labels:
                call(name, (t, _code(p, label)), 0.0)
        for name in KINDED:
            for kind in KINDS:
                call(name, (t, _code(p, kind)), 0.0)
        for i in p.sub_ids():
            for name in SUBACCOUNT:
                call(name, (t, i), 0.0)
            for label in AV_TIMINGS:
                call("sa_pp_at", (t, i, _code(p, label)), 0.0)
    if reached(IN_COVER_ONLY):
        faults.append(f"{where}: evaluated outside cover: {reached(IN_COVER_ONLY)}")
    for name, cells in p.cells.items():
        if "t" not in cells.parameters:
            continue
        for t in months:
            if name in SCENARIO_READERS and t < entry:
                continue
            for args in _monthly_args(p, name, cells, t):
                call(name, args)
    if reached(KEYED_READERS):
        faults.append(f"{where}: read outside cover by Phase 2's sweep: "
                      f"{reached(KEYED_READERS)}")
    end = p.proj_len()
    past = {name: [args for args in _cached_args(cells)
                   if _month(args[cells.parameters.index("t")])
                   and args[cells.parameters.index("t")] > end][:5]
            for name, cells in p.cells.items() if "t" in cells.parameters}
    past = {name: keys for name, keys in past.items() if keys}
    if past:
        faults.append(f"{where}: read past t = proj_len() = {end}: {past}")
    return faults


def _scenario_faults(p, where):
    """Where a row issued later answers a scenario reader before issue rather than raise.

    Its re-based scenarios set no level before its issue month, so each reader raises at
    the month before, naming the point and the month: ``inv_return_mth`` for each
    subaccount, ``scenario_rate`` for each name, ``cmt10``, and ``unit_growth`` through
    ``inv_return_mth``, as no projection may read either scenario before the contract's
    first month (D4).
    """
    faults = []
    before = p.t_entry() - 1
    calls = [("inv_return_mth", (before, i), "the return scenario sets no return for "
              f"subaccount {i} by month {before}") for i in p.sub_ids()]
    calls += [("unit_growth", (before, i), "the return scenario sets no return for "
               f"subaccount {i} by month {before}") for i in p.sub_ids()]
    calls += [(name, args, f"the rate scenario sets no level by month {before}")
              for name, args in (("scenario_rate", (before, "vix_sq")),
                                 ("scenario_rate", (before, "cmt10")),
                                 ("cmt10", (before,)))]
    for name, args, message in calls:
        try:
            got = p.cells[name](*args)
        except Exception as err:
            text = _raised(err)
            if not (text.startswith("ValueError") and message in text):
                faults.append(f"{where}: {name}{args} raised {text}")
            continue
        faults.append(f"{where}: {name}{args} = {got!r} before issue, not a refusal")
    return faults


@pytest.mark.parametrize("which", [
    pytest.param("spliced", id="spliced"),
    pytest.param("switched", id="switched", marks=FULL_ONLY)])
def test_every_guarded_cell_holds_its_outside_cover_value(splices, which):
    """Outside cover each cell holds :data:`OUTSIDE_COVER`'s value, and reads no rate.

    On every committed point, in every month before issue and in the first month after
    cover, ``t = proj_len()``, which the count's look-ahead reads, on a model that evaluates
    nothing else (:func:`_outside_cover_faults`).  ``is_active``'s docstring promises that
    outside cover no count evaluates a rate, and no table is read at an age, a year, a
    policy month or a quarter the contract does not have, so afterwards none of
    :data:`IN_COVER_ONLY` may hold a key.  Then every monthly cell, guarded or not, is
    called there, as Phase 2's full sweep will call it: each answers, with a Python value,
    no keyed reader is read on the way, and no month past ``t = proj_len()`` is, which
    Phase 2's ``t`` cache does not hold: the count's roll-forward residual and the account
    value in force at the month's end, which read ``t + 1``, are guarded there.  Every
    monthly cell is one of those lists, or :data:`EVERY_MONTH`'s, so that a cell added to
    the model is placed in one.  And on every row issued after the valuation date each
    scenario reader raises at the month before issue, naming the point, rather than
    answering (:func:`_scenario_faults`).

    The committed table's one point issued after the valuation date is the anchor, which
    reads the base path and carries neither the VIX fee, nor the CMT roll-up, nor a
    programme, nor a premium tax, so on it a cell tied to one of those would hold zero
    before issue, guarded or not.  So the same scan runs on the splice's future rows, the
    core's or, with ``USLIB_SEC_FULL=1``, all of them, under the shipped References with the
    splice's assumptions switched on, and, on the full grid, under the switched ones: the
    VIX fee, the female table, the second fund set and grid and the programmes among them.
    Each row is made afresh first and released after.

    Several of these guards change no number the frame shows: once the counts are zero
    outside cover, every cash flow is too, and an unguarded value multiplies a zero count.
    They are held here because they are what the docstrings promise a caller, and because
    Phase 2 needs them: a table read at an age or a year the contract does not have would
    wrap round in a compiled model rather than fail (USLIB-SEC-PLAN.md F4, R1).
    """
    faults = []
    if which == "spliced":
        model = _read(model_path(SEC), "cover")
        try:
            monthly = {n for n, c in model.Projection.cells.items() if "t" in c.parameters}
            placed = {*OUTSIDE_COVER, *IN_COVER_ONLY, *EVERY_MONTH, *TIMED, *KINDED,
                      *SUBACCOUNT, *SUBACCOUNT_TIMED}
            assert monthly <= placed, f"monthly cells unplaced: {sorted(monthly - placed)}"
            table = model.Data.model_point_table()
            for key, point_id in zip(point_keys(model), table.index):
                p = projection(model, key)
                faults += _outside_cover_faults(p, f"point {point_id}")
                if p.t_entry() > 0:
                    faults += _scenario_faults(p, f"point {point_id}")
        finally:
            model.close()
    _, sec = splices.pair(which)
    grid, core = GRIDS[which]
    futures = [case for case in _selected(grid, core) if case[0] == "future"]
    for case in futures:
        key = _row_key(sec, *case)
        if key in sec.Projection.itemspaces:
            _release(sec, key)
        try:
            p = projection(sec, key)
            faults += _outside_cover_faults(p, f"{which} {_case_id(*case)}")
            faults += _scenario_faults(p, f"{which} {_case_id(*case)}")
        finally:
            _release(sec, key, collect=True)
    assert futures and not faults, (
        f"{len(faults)} faults outside cover, first:\n  " + "\n  ".join(faults[:20]))


# ---------------------------------------------------------------------------
# T2 and T3 on the switched References


@pytest.mark.parametrize(
    "kind, s_point, month",
    [_case(case, SWITCHED_CORE, _case_id(*case)) for case in SWITCHED_GRID])
def test_the_switched_references_continue_s(splices, splice_records, kind, s_point,
                                            month):
    """Under :data:`SWITCHED_REFS`, each row is S from its month on, as under the shipped.

    S ships several bounds where they never bind, and the splice's comparison sees a bound
    only where it acts.  So both models are read again with each bound where it binds
    (:data:`SWITCHED_REFS`), and each row of :data:`SWITCHED_GRID` is compared with S as T2
    and T3 compare theirs (:func:`_compare`): the GWB at its cap, the VIX fee at the
    corridor's low, the shock year's lapse capped at 1, the Bonus Period's restart past
    its age, and the GAWA raised by a step-up after the first withdrawal, which only the
    lower GLWB fee leaves the account value to make.  What each case reaches is recorded
    for the core's reach test, and the row released.
    """
    found = _splice_case(splices, splice_records, "switched", (kind, s_point, month))
    assert not found, f"{len(found)} faults, first:\n  " + "\n  ".join(found[:20])


# ---------------------------------------------------------------------------
# D11's R1, R1a and R2


@pytest.mark.parametrize("which, grid", [
    pytest.param("spliced", "core", id="spliced-core"),
    pytest.param("spliced", "full", id="spliced-full", marks=FULL_ONLY),
    pytest.param("switched", "core", id="switched-core"),
    pytest.param("switched", "full", id="switched-full", marks=FULL_ONLY)])
def test_no_cell_is_called_before_the_valuation_date_or_reads_far_ahead(
        splices, splice_records, which, grid):
    """R1, its look-back, R1a and R2's look-ahead, on the rows T2 and T3 compare.

    Each is a rule of how the model computes, not of what, so no number shows a breach,
    and on a point issued at ``t = 0`` the two clocks coincide and hide it from T1 too.
    The splice's rows are points in force at every month T2 names, S's own in-force point
    and the variants among them, and points issued later, under both sets of References,
    and each row was swept first:

    * R1: no cell holds a negative argument.  modelx evaluates one without complaint, and
      a compiled cache raises ``IndexError`` below 0 (USLIB-SEC-PLAN.md F4).  A policy
      month turned into ``t`` by subtracting ``duration_mth_init()`` (R1a) goes negative
      on a point in force past it, and so does a balance read a month back without the
      opening state's branch: ``VA_US_S``'s GLWB payment reads ``gawa_pp(t - 1)`` at
      ``t = 0``, which on a contract valued depleted at a contract year's start recurses
      below the valuation date.  The age, year, policy month and quarter keys are held to
      it too.
    * R1's look-back stops at ``t_entry()``: no cell evaluated at a month from
      ``t_entry()`` on read a month before it.  On a point issued later a recursion based
      at ``t == 0`` reads the pre-issue zeros, so no number shows it and no argument goes
      negative.
    * R2's look-ahead: no cell evaluated at month ``t`` read a cell keyed by a month beyond
      ``t + 1``, as modelx's dependency graph records each cached call's precedents, but
      the one R2 admits (:data:`LOOK_AHEAD`): ``lapse_wd_factor`` reads whether the year has
      a withdrawal at the anniversary closing it, ``anniv_mth(t)``, at most 11 months on
      and inside the frame.  Each such read is admitted only where what it reads rests on
      no count, no decrement and nothing the reader holds, and on no month after that
      anniversary, which is walked over the read's precedents (:func:`_closure`); and some
      read is admitted, so the exception is exercised.  ``VA_US_S`` scans the year's
      months from ``t`` instead, 421 to 3,300 reads beyond ``t + 1`` a point.  A read
      through a cell keyed by no month is judged against the month that asked
      (:func:`_month_reads`).
    * No table is read below the books: no GAWA% band or mortality rate at an age below the
      row's attained age in its first month on the books, no withdrawal charge at a count
      of completed years below its own there, no programme at a policy month before it,
      and no VIX fee or level at a contract quarter before the one under way there, whose
      rate of the quarter before is the row's ``phi_glwb_init``.  The rest is history,
      which a re-based scenario does not hold.

    Each row was scanned by the case that compared it, and a row no case has scanned is
    scanned here.  The core case covers the core's rows, the full case every other row of
    the full grid, with ``USLIB_SEC_FULL=1``.  The twins of S's own new-business points in
    the splice's table are no case's, and are left out: on them the clocks coincide, and T1
    compares their committed twins with S cell by cell.  The variants' twins are T2's
    cases, and are scanned with them.
    """
    grid_cases, core = GRIDS[which]
    cases = [case for case in grid_cases if (case in core) == (grid == "core")]
    found = {"negative": [], "early": [], "ahead": [], "condition": [], "year": []}
    raised, admitted = [], 0
    for case in cases:
        record = _record_of(splices, splice_records, which, case)
        where = _case_id(*case)
        for rule in found:
            found[rule] += [f"{where}: {line}" for line in record[rule]]
        admitted += record["admitted"]
        if record["raised"]:
            raised.append(f"{where}: {record['raised']}")
    assert cases, f"the {which} {grid} grid has no rows"
    assert not raised, f"rows that raised: {raised[:10]}"
    assert not found["negative"], (f"called before the valuation date: "
                                   f"{found['negative'][:10]}")
    assert not found["early"], f"read before issue from the books: {found['early'][:10]}"
    assert not found["ahead"], f"read beyond t + 1: {found['ahead'][:10]}"
    assert not found["condition"], (f"an admitted read rests on a count or a later month: "
                                    f"{found['condition'][:10]}")
    assert not found["year"], f"read below the books: {found['year'][:10]}"
    assert admitted > 0, "no read of the closing anniversary was admitted"


def test_the_core_grid_reaches_every_branch(splices, splice_records):
    """What the default run's T2 and T3 cases reach, which the full grid only multiplies.

    The default run thins the splice to a core (the module docstring), and this test is
    what keeps the thinning from costing a branch.  First, statically, over S's table with
    the variants, each property below holds of some core case, T2's or T3's: each fund set,
    GAWA grid, sex, scenario, programme, death benefit, step-up basis, fee rule, roll-up
    rule and withdrawal-charge schedule; S's own in-force point; each kind of valuation
    month, the first policy year, a contract year's start, mid-year and its last month; a
    point issued a month on and one more than a year on.

    Then, on the splice's rows, of some core row, each of :data:`AT_VALUATION` and
    :data:`IN_FRAME`, what no column of the table shows: the depleted openings and the
    GLWB paid from the columns, the year to date and the year-open roll-up base each read
    by a withdrawal, the year flag alone, both sides of the step-up base's two boundaries,
    the VIX prior binding, the GWB Adjustment binding at the valuation date, a withdrawal
    taken in an earlier year; and in the frame each event and each bound the product has:
    depletion, the first, excess and mid-year withdrawals, one in a contract year's last
    month among them, a premium after issue and after a withdrawal, the step-up, the bonus
    and its restart, the GWB Adjustment, a payment not for life, the death benefit's
    growth cutoff, the maintenance fee and its waiver, the charges and a withdrawal capped
    at the account value, the withdrawal charge, the lapse's two ITM bounds, its shock year
    and its withdrawal-year factor, the VIX band and the corridor's high, the CMT floor
    and cap, the older roll-up rate, the premium tax, commission and acquisition of new
    business and the female table.  And of some row of the switched References' core,
    each of :data:`SWITCHED_FRAME`.

    Last, each bound by the values it bounds: each side of every ``min`` and ``max`` in
    ``Projection`` wins, the others below it, in some call the sweep or the comparison of
    a core row of either grid makes (:class:`_BoundSides`), but the sides
    :data:`IDLE_SIDES` names, each with its reason, and those :data:`BOUND_ELSEWHERE`
    names, each with the test that binds it on rows of its own; and no side either names
    wins on a core row.

    Each core row's branches were recorded by the case that compared it (:func:`_record`),
    and a row no case has recorded is evaluated here.  The splice's models are the last
    thing a test of this module reads, so they are closed here, and the module's other
    tests run without them.
    """
    s_table = _s_table_with(VARIANTS)

    def at(p, column):
        return s_table.at[p, column]

    def choices(column, values):
        return {f"{column} {v}": (lambda k, p, d, v=v, column=column: at(p, column) == v)
                for v in values}

    static = {
        **choices("fund_set", ("core_60_40", "alt_25_75", "trio")),
        **choices("glwb_option", ("s3_single", "alt_grid", "high_grid")),
        **choices("sex", ("M", "F")),
        **choices("scenario_id", ("base", "decline", "variant", "crash", "hq_swing",
                                  "spike", "cmtdrop")),
        **choices("txn_id", ("none", "excess", "midyear", "lateprem", "floors",
                             "cmtdrop")),
        **choices("age_at_entry", (69, 70)),
        **choices("gmdb_option", ("rollup", "ratchet", "basic")),
        **choices("glwb_stepup_basis", ("annual_CV", "highest_quarterly_CV")),
        **choices("fee_reset_rule", ("none", "quinquennial", "vix")),
        **choices("rollup_rule", ("fixed", "cmt_linked")),
        **choices("cdsc_schedule", ("commission_7yr", "none")),
        "S's own in-force point": lambda k, p, d: (k, p, d) in IN_FORCE_TWINS,
        "the first policy year": lambda k, p, d: k == "derived" and 0 < d < 12,
        "a contract year's start": lambda k, p, d: k == "derived" and d % 12 == 0,
        "mid-year": lambda k, p, d: k == "derived" and d % 12 not in (0, 11),
        "a contract year's last month": lambda k, p, d: k == "derived" and d % 12 == 11,
        "issued a month on": lambda k, p, d: k == "future" and d == -1,
        "issued more than a year on": lambda k, p, d: k == "future" and -d > 12,
    }
    missing = [what for what, holds in static.items()
               if not any(holds(*case) for case in sorted(CORE_GRID))]
    assert not missing, f"no core case reaches: {missing}"
    try:
        won = set()
        for which, (grid, core) in GRIDS.items():
            reached = set()
            for case in sorted(core):
                record = _record_of(splices, splice_records, which, case)
                reached |= record["branches"]
                won |= record["bounds"]
            at_valuation, frame = REACH[which]
            missing = [what for what in (*at_valuation, *frame) if what not in reached]
            assert not missing, f"no core row of the {which} grid reaches: {missing}"
        sides = (splices.bounds or _BoundSides(splices.pair("spliced")[1])).sides
        named = set(IDLE_SIDES) | set(BOUND_ELSEWHERE)
        assert named <= sides, sorted(named - sides)
        assert not set(IDLE_SIDES) & set(BOUND_ELSEWHERE)
        if sys.version_info >= (3, 11):
            unbound = sorted(sides - won - named)
            assert not unbound, f"sides of a bound no core row binds: {unbound}"
            bound = sorted(named & won)
            assert not bound, f"sides named idle or bound elsewhere that bind here: {bound}"
    finally:
        splices.close()


# ---------------------------------------------------------------------------
# Models read afresh: a NaN sent to the mortality and to the residuals, the cold depth,
# the count's scale, the issue month, T5's tables and the opening state's pairs
#
# Every test that reads a model of its own runs here, once the splice's pairs are closed
# and before the committed models are read and swept, so that the models it reads never
# sit in memory beside those.


def _not_a_number_at(x):
    """NaN, what a blank rate carries: a formula a test puts in place of a reader's."""
    return float("nan")


# The calls of the twins of S points 1 and 2 that a NaN mortality rate must reach as NaN:
# the annual rate in the first month, at the first withdrawal's anniversary and in the
# last covered month, the monthly rate, and the count the month after the first.
NAN_CALLS = (("mort_rate", 0), ("mort_rate", 119), ("mort_rate", "last"),
             ("mort_rate_mth", 0), ("pols_if", 1))


def test_a_nan_reaches_the_mortality_rate_and_the_count_as_nan():
    """A NaN mortality rate stays NaN through the count, and the count's check fails it.

    ``VA_US_S`` reads its annual mortality from the table at the attained age and sex,
    with no factor and so no cap (§5.1, step 6; ``tests/test_mortality_caps.py`` lists it
    among the models with none): no ``min`` stands between the table and the count to lose
    a NaN.  ``Data`` refuses a blank, text or infinite rate (:data:`TABLE_FAULTS`), so to
    send the projection a NaN the formula of the table's one reader,
    ``mort_rate_base_at``, is replaced by one returning NaN, in a model read for the test,
    before it computes anything, which modelx allows and a compiled model does not
    (USLIB-SEC-PLAN.md K7).  On the twin of S point 1, issued at the valuation date, and on
    the twin of S's point 2, in force at 26, each of :data:`NAN_CALLS` is then the float
    NaN: the annual and the monthly rate, and the count the month after; the count's
    roll-forward residual in month 0 is NaN, and both roll-forward checks are ``False``.
    """
    model = _read(model_path(SEC), "nan")
    try:
        model.Projection.cells["mort_rate_base_at"].formula = _not_a_number_at
        lost = []
        for case in (("twin", 1, 0), ("twin", 2, 0)):
            p = _row(model, *case)
            for name, t in NAN_CALLS:
                t = p.proj_len() - 1 if t == "last" else t
                value = p.cells[name](t)
                if not (type(value) is float and math.isnan(value)):
                    lost.append(f"{case} {name}({t}) = {value!r}")
            resid = p.check_pols_roll_fwd_resid(0)
            assert type(resid) is float and math.isnan(resid), (case, resid)
            assert p.check_pols_roll_fwd() is False, case
            assert p.check_av_roll_fwd() is False, case
        assert not lost, f"the mortality loses a NaN rate: {lost}"
    finally:
        model.close()


def test_a_residual_that_is_not_a_number_fails_its_check():
    """A check whose residual is not a number fails, as ``VA_US_S``'s strict bound does.

    Each check asks of every month whether the residual is within its tolerance,
    ``not abs(r) < tol`` failing it, so that a residual that is not a number fails, where
    a check that asked whether the residual exceeds its tolerance would pass it: no
    comparison with NaN holds (USLIB-SEC-PLAN.md §7.1, precised at M3).  The NaN goes in
    through a Reference, ``asset_charge_me``, set on a model read for the test before it
    computes anything, the form that runs compiled too.  On the twin of S point 1 and the
    twin of S's point 2 the account-value and charge-split residuals are then NaN in month
    0, and ``check_av_roll_fwd()`` and ``check_charge_split()`` are ``False``.  From month 1
    both residuals are within their tolerances again, 0.0: ``VA_US_S``'s subaccount step,
    ``sa * (1 - charge / base) if base > 0.0 else 0.0``, reads the NaN account value as not
    above 0, so month 0 closes every subaccount at 0.0 and the contract is depleted from
    month 1, a step this model keeps in S's order.  The count's residual stays a number in
    every month, the lapse reading no NaN, so the count's check is asserted where a NaN
    reaches it, in the test above.
    """
    model = _read(model_path(SEC), "nan_check", {"asset_charge_me": float("nan")})
    try:
        for case in (("twin", 1, 0), ("twin", 2, 0)):
            p = _row(model, *case)
            for check in ("check_av_roll_fwd", "check_charge_split"):
                resid = p.cells[f"{check}_resid"](0)
                assert type(resid) is float and math.isnan(resid), (case, check, resid)
                assert p.cells[check]() is False, (case, check)
                later = [p.cells[f"{check}_resid"](t) for t in range(1, p.proj_len())]
                assert later == [0.0] * (p.proj_len() - 1), (case, check)
            assert p.av_pp(0) == 0.0 and p.depleted_open(1), case
            counts = [p.check_pols_roll_fwd_resid(t) for t in range(p.proj_len())]
            assert not any(math.isnan(r) for r in counts), case
            assert p.check_pols_roll_fwd() is True, case
    finally:
        model.close()


def _cold_depth(proj, cell, args):
    """The frames on modelx's stack at the deepest point of ``cell(*args)``, called cold.

    The deepest stack position modelx's trace records, plus one, on an ItemSpace that has
    evaluated nothing.  modelx warns as the trace starts and as it stops.
    """
    with pytest.warns(UserWarning, match="call stack trace"):
        mx.start_stacktrace(maxlen=None)
        try:
            proj.cells[cell](*args)
            trace = mx.get_stacktrace()
        finally:
            mx.stop_stacktrace()
    return 1 + max(depth for event, depth, *_ in trace if event == "ENTER")


# The cold calls the depth test makes on the committed model, each on an ItemSpace of its
# own, and the chains each walks the length of: the last month's net cash flow walks the
# count, the subaccounts, the bases, the status chains and the year-to-date chains, on the
# anchor issued at the valuation date, on S's in-force point, on the excess programme, on
# its row valued at its excess withdrawal, on the contract depleted without a withdrawal,
# and on the point issued 15 months on, from issue, not from t = 0; the year chains are
# called alone on the excess programme's twin, whose first month opens the withdrawals',
# the GLWB bases', the step-up base's and the account value's chains under them, and the
# account value's, a subaccount's, the bases' and the withdrawal status's chains alone on
# the future row.
COLD_CALLS = (*((case, "net_cf") for case in (
    ("twin", 1, 0), ("twin", 2, 0), ("twin", 4, 0), ("derived", 4, 60), ("derived", 8, 560),
    ("future", 1, -15))),
    *((("twin", 4, 0), cell) for cell in ("bonus_end", "gmdb_factor_acc",
                                          "free_wd_used_cum_pp", "sum_wd_pp")),
    *((("future", 1, -15), cell) for cell in ("av_pp", "sa_pp", "gwb_pp", "gawa_pp",
                                              "rb_pp", "has_wd_by")))

# The count's chain called alone, cold: its first month on the books reads the lapse's
# withdrawal year at the anniversary closing the first contract year, R2's admitted read,
# and so walks the withdrawals' chain there, up to LOOK_AHEAD_MTHS long, under the count's.
COUNT_CALLS = ((("twin", 1, 0), "pols_if"), (("future", 1, -15), "pols_if"))

# The youngest issue age the GLWB allows (product-spec.md), and the rates a test gives the
# mortality table below its first age, 40: a distinct geometric rate per age and sex, each
# 0.93 (male) or 0.91 (female) of the age above, so that a rate read at the wrong age
# reads another number.
YOUNGEST_ISSUE_AGE = 35
YOUNGER_RATIOS = {"M": 0.93, "F": 0.91}
LONGEST_COVER = 12 * (120 - YOUNGEST_ISSUE_AGE)


def _younger_ages(table):
    """The mortality table extended down to :data:`YOUNGEST_ISSUE_AGE`, each sex geometric
    in age from its rate at 40 (:data:`YOUNGER_RATIOS`)."""
    rows = []
    for sex, ratio in YOUNGER_RATIOS.items():
        q40 = float(table.loc[(table["age"] == 40) & (table["sex"] == sex),
                              "mort_rate"].iloc[0])
        rows += [(age, sex, q40 * ratio ** (40 - age), "a test")
                 for age in range(YOUNGEST_ISSUE_AGE, 40)]
    return pd.concat([pd.DataFrame(rows, columns=table.columns), table],
                     ignore_index=True)


def _longest_cover(committed):
    """The anchor issued at age 35, at the valuation date and 120 months on: its table and
    the edits that give the later one its scenarios, ``base-F120``, and the mortality its
    younger ages.

    35 is the youngest issue age the GLWB allows, and cover runs to attained age 120,
    ``omega_age``, so 1,020 months of cover is the longest a contract has, and 120 months on
    is the horizon (D4).
    """
    twin, future = _label(committed, "twin", 1, 0), _label(committed, "future", 1, -15)
    table = committed.loc[[twin, future]].assign(age_at_entry=YOUNGEST_ISSUE_AGE)
    table = _cells(future, duration_mth=-120, scenario_id="base-F120")(table)

    def later(name):
        scenarios = _companion(name)
        base = scenarios[scenarios["scenario_id"] == "base"]
        moved = base.assign(scenario_id="base-F120", t=base["t"] + 120)
        return pd.concat([scenarios, moved], ignore_index=True)

    return table, {RETURNS: later(RETURNS), RATES: later(RATES),
                   "mort_table.csv": _younger_ages}


@pytest.mark.filterwarnings("ignore:call stack trace:UserWarning")
def test_the_deepest_cold_call_runs_one_cell_a_month(tmp_path):
    """A cold call holds one frame a month back to ``t_entry()``, and a few more (F7).

    Every recursion here is one cell a month: the count, each subaccount, the seven bases,
    the status chains, the year-to-date chains and the VIX fee's over its quarters.  A
    compiled model runs each chain on the C stack, so the depth is what sizes it, and no
    comparison sees it: a chain of two cells a month gives the same numbers.  So each cold
    call of :data:`COLD_CALLS`, each on an ItemSpace of the committed model that has
    evaluated nothing, its ``Data`` read first, holds at least one frame for each month
    back to ``t_entry()``, and so walked its chain, and at most :data:`CHAIN_OVERHEAD`
    more.  The point issued 15 months on walks from its issue: a chain that ran on through
    its months before issue, as one guarded by the frame rather than by cover would, walks
    15 months further.  The count's chain alone (:data:`COUNT_CALLS`) holds at most
    :data:`LOOK_AHEAD_MTHS` more, R2's admitted read of the closing anniversary, which
    opens the withdrawals' chain under the count's first month.

    The same holds at the contract's longest cover from issue, 1,020 months at issue age
    35 (:func:`_longest_cover`), at the valuation date and 120 months after it, the
    horizon, each cold: that is the depth Phase 2's stack is sized from (USLIB-SEC-PLAN.md
    §7.7, *C*), 1,034 levels on ``net_cf`` and 1,040 on the count alone, against 1,020
    months.
    """
    model = _read(model_path(SEC), "depth")
    try:
        model.Data.model_point_table()
        for case, cell in (*COLD_CALLS, *COUNT_CALLS):
            key = _row_key(model, *case)
            p = projection(model, key)
            months = p.proj_len() - p.t_entry()
            args = (p.proj_len() - 1, 1) if cell == "sa_pp" else (p.proj_len() - 1,)
            depth = _cold_depth(p, cell, args)
            extra = LOOK_AHEAD_MTHS if (case, cell) in COUNT_CALLS else 0
            assert months <= depth <= months + CHAIN_OVERHEAD + extra, (case, cell, months,
                                                                         depth)
            _release(model, key)
    finally:
        model.close()
    table, edits = _longest_cover(_committed())
    model = _read(_sec_inputs(tmp_path, table, edits), "depth35")
    try:
        model.Data.model_point_table()
        for key in point_keys(model):
            for cell, extra in (("net_cf", 0), ("pols_if", LOOK_AHEAD_MTHS)):
                p = projection(model, key)
                months = p.proj_len() - p.t_entry()
                assert months == LONGEST_COVER == 1020, (key, p.proj_len(), p.t_entry())
                depth = _cold_depth(p, cell, (p.proj_len() - 1,))
                assert months <= depth <= months + CHAIN_OVERHEAD + extra, (key, cell,
                                                                             depth)
                _release(model, key)
    finally:
        model.close()


# What T4 multiplies policy_count by: not a whole number, because a count of contracts need
# not be one, so that a flow which read the count as whole contracts would not follow it.
# And the rows it multiplies: S's in-force point, the first policy year, the year to date
# after a withdrawal, the excess withdrawal at the valuation month with its withdrawal
# charge, the year after it with the premium at 72, the contract depleted without a
# withdrawal and the anchor issued 15 months on: between them every flow, the GLWB paid
# after depletion, a withdrawal and its charge, the premium after issue and at issue, its
# commission, tax and acquisition, the death benefit's claims, the deemed maturity.  Each
# carries the premium tax, so that the tax follows the count where a premium falls after
# the valuation date; the first policy year's row has its year-open roll-up base moved to
# the premium after the tax, as Data requires there.
COUNT_FACTOR = 2.5
SCALED_ROWS = (("twin", 2, 0), ("derived", 1, 6), ("derived", 1, 131), ("derived", 4, 60),
               ("derived", 4, 65), ("derived", 8, 560), ("future", 1, -15))

# The cells that scale with policy_count.  Every other cell is a per-contract amount, a
# rate, a clock, a code or a flag, and must not move when the count does.  The residuals
# are rounding on that many contracts, and scale with nothing; the checks over them must
# still close.
COUNTED = frozenset({
    "policy_count", "pols_if_init", "pols_if", "pols_if_at", "pols_new_biz",
    "pols_death", "pols_lapse", "pols_maturity", "pols_decr",
    "premiums", "prem_to_av", "asset_charges", "fees_glwb", "fees_gmdb", "maint_fees",
    "wd_charges", "withdrawals", "glwb_payments", "inv_income", "wd_from_av",
    "charges_from_av", "charge_income", "commissions", "premium_taxes", "expenses",
    "gmdb_claims", "net_cf", "net_cf_ga", "av_change", "av_at", "claims",
    "claims_from_av", "claims_over_av", "result_cf", "result_pols"})
SCALED = sorted(COUNTED - {"result_cf", "result_pols"})


def _taxed(table):
    """``table`` with the premium tax on every row, and the year-open roll-up base of a row
    in its first policy year moved to the premium credited after it (Data's rule)."""
    out = table.assign(premium_tax_rate=PREMIUM_TAX)
    first = out.index[(out["duration_mth"] > 0) & (out["duration_mth"] < 12)]
    return out.assign(rb_pp_prev_anniv_init=out["rb_pp_prev_anniv_init"].where(
        ~out.index.isin(first), out["premium"] * (1.0 - PREMIUM_TAX)))


def test_scaling_the_count_scales_every_flow_and_no_per_contract_value(tmp_path):
    """``policy_count`` is a weight: 2.5 times the count, 2.5 times every flow, the same per
    contract.

    The committed rows of :data:`SCALED_ROWS`, each with the premium tax (:func:`_taxed`),
    and a copy of them with every count multiplied by :data:`COUNT_FACTOR`, are each read
    with :data:`SPLICED_REFS` set before either computes anything: the assumptions that
    ship at zero switched on at the splice's values, so that every flow is nonzero on some
    row, the commission, the acquisition and the premium tax among them.  On every row
    ``result_cf`` and ``result_pols`` are 2.5 times the committed rows', element by
    element, to 1e-12 relative: a scaled count is a computed float, which may come back
    from the CSV within two ulps (``sec_support``'s module docstring).  So is every other
    cell of :data:`COUNTED`, at every argument the sweep of the committed row cached, the
    counts and the account value in force at each timing among them, the month's change
    in it to 1e-12 of the two balances it is the difference of.  And every cell
    outside :data:`COUNTED` (the subaccounts, the account value, the bases, the GAWA%, the
    year to date, the step-up base, the VIX fee, the opening state, the rates, both clocks,
    the flags) agrees at every argument that sweep cached, the checks still closing.  So a
    flow that dropped the count, or read it as whole contracts, which a table of counts of
    1 hides from every comparison with S, fails here.  Each row is released once compared.
    """
    committed = _committed()
    table = _taxed(committed.loc[[_label(committed, *case) for case in SCALED_ROWS]])
    base = _read(_sec_inputs(tmp_path / "base", table), "counted", SPLICED_REFS)
    scaled = _read(_sec_inputs(tmp_path / "scaled", table.assign(
        policy_count=COUNT_FACTOR * table["policy_count"])), "scaled", SPLICED_REFS)
    nonzero = set()
    try:
        for key, scaled_key in zip(point_keys(base), point_keys(scaled)):
            one, many = projection(base, key), projection(scaled, scaled_key)
            _sweep_sec(one)
            for report in ("result_cf", "result_pols"):
                b, d = one.cells[report](), many.cells[report]()
                assert d.index.equals(b.index) and list(d.columns) == list(b.columns)
                want = COUNT_FACTOR * b
                bad = ((d - want).abs() > 1e-12 * want.abs()).any()
                assert not bad.any(), (key, report, list(bad[bad].index))
            for name in SCALED:
                for args in _cached_args(one.cells[name]):
                    want = COUNT_FACTOR * one.cells[name](*args)
                    got = many.cells[name](*args)
                    scale = abs(want)
                    if name == "av_change":         # a difference of two balances
                        scale = COUNT_FACTOR * (
                            abs(_at(one, "av_at", args[0], "EOM"))
                            + abs(one.av_pp_init() * one.pols_if_init()))
                        if args[0] > one.t_entry():
                            scale += COUNT_FACTOR * abs(_at(one, "av_at", args[0] - 1,
                                                            "EOM"))
                    assert abs(got - want) <= 1e-12 * scale, (key, name, args, got, want)
                    if want != 0.0:
                        nonzero.add(name)
            assert _mismatches(one, many, exempt=TWIN_EXEMPT_DEFAULT | COUNTED | RESIDUALS,
                               rtol=1e-12, atol=0.0) == []
            assert (many.check_av_roll_fwd() and many.check_pols_roll_fwd()
                    and many.check_charge_split()), key
            _release(base, key)
            _release(scaled, scaled_key)
    finally:
        scaled.close()
        base.close()
    assert nonzero == set(SCALED), f"0 on every row: {sorted(set(SCALED) - nonzero)}"


def test_the_roll_forward_checks_close_on_a_million_contracts(tmp_path):
    """Both roll-forward checks scale their tolerance with the count, and close at 1e6.

    A residual is rounding on that many contracts, so ``check_av_roll_fwd`` holds it to
    ``check_tol_av x max(policy_count(), 1)`` and ``check_pols_roll_fwd`` likewise, where
    ``VA_US_S``'s tolerances are fixed: at the counts the other tests use, one contract or
    less, the residuals are far inside either.  So S's in-force point, the anchor in the
    year of its first withdrawal and the excess programme after its excess withdrawal are
    projected from a copy where each counts a million contracts: all three checks close,
    and each scaled residual somewhere exceeds the fixed tolerance it would have had, so
    the scaling is what closes them.  The charge split is per contract and keeps its
    tolerance unscaled.
    """
    committed = _committed()
    rows = [_label(committed, *case) for case in (("twin", 2, 0), ("derived", 1, 131),
                                                  ("derived", 4, 65))]
    model = _read_edited(tmp_path, _set("policy_count", rows, 1e6), "million")
    try:
        for row in rows:
            p = _point(model, row)
            assert p.policy_count() == 1e6
            assert p.check_av_roll_fwd() and p.check_pols_roll_fwd(), row
            assert p.check_charge_split(), row
            av = max(abs(p.check_av_roll_fwd_resid(t)) for t in range(p.proj_len()))
            pols = max(abs(p.check_pols_roll_fwd_resid(t)) for t in range(p.proj_len()))
            assert av > p.check_tol_av and pols > p.check_tol_pols, (row, av, pols)
    finally:
        model.close()


def test_acquisition_and_the_premium_fall_in_the_issue_month(tmp_path):
    """The single premium, the acquisition, the commission and the tax, per contract issued.

    On a model read with :data:`SPLICED_REFS`, an acquisition expense of $150 and a
    commission of 5% that ship at 0, set before it computes anything, from a copy whose rows
    carry the premium tax of 2% (:func:`_taxed`) and whose anchor issued at the valuation
    date and anchor issued 15 months on each count 3 contracts: in the issue month, ``t =
    0`` and ``t = 15``, the premium is 300,000, the acquisition 450, the commission 15,000
    and the tax 6,000, and each is 0 in every other month.  On the rows in force, S's point
    2 and the anchor at its first withdrawal, there is none in any month, though on the
    valuation clock their row 0 is ``t = 0``; and on the excess programme valued at 65 the
    premium of 25,000 a contract at ``t = 7`` brings its commission and its tax on the
    contracts then in force but no acquisition.  S charges the acquisition at its ``t ==
    0``, which on its point 2, in force at 26, is the valuation date, not the issue month:
    read under the same References, S's point 2 pays $150 more expense at ``t = 0`` than
    this model's twin does, and nothing else differs there.
    """
    committed = _committed()
    issued = [_label(committed, "twin", 1, 0), _label(committed, "future", 1, -15)]
    table = _set("policy_count", issued, 3.0)(_taxed(committed))
    fresh = _read(_sec_inputs(tmp_path, table), "acquisition", SPLICED_REFS)
    s = _read(model_path(TWIN), "acquisition_s", SPLICED_REFS)
    try:
        for case, flows in ((("twin", 1, 0), (300000.0, 450.0, 15000.0, 6000.0)),
                            (("future", 1, -15), (300000.0, 450.0, 15000.0, 6000.0)),
                            (("twin", 2, 0), None), (("derived", 1, 120), None),
                            (("derived", 4, 65), None)):
            p = _row(fresh, *case)
            issue = -p.duration_mth_init()
            for t in range(p.proj_len()):
                acq = p.expenses(t) - (
                    (p.expense_maint / 12.0) * p.inflation_factor(t)
                    + (p.expense_av_rate / 12.0) * p.av_pp(t)) * p.pols_if(t)
                got = (p.premiums(t), acq, p.commissions(t), p.premium_taxes(t))
                if flows is not None and t == issue:
                    assert got == pytest.approx(flows, abs=1e-9), (case, t)
                elif case[1:] == (4, 65) and t == 7:
                    premium = 25000.0 * p.pols_if(7)
                    assert got == pytest.approx(
                        (premium, 0.0, 0.05 * premium, PREMIUM_TAX * premium), abs=1e-9)
                else:
                    assert got == pytest.approx((0.0,) * 4, abs=1e-9), (case, t)
        s2, twin = _point(s, 2), _row(fresh, "twin", 2, 0)
        assert s2.expenses(0) - twin.expenses(0) == pytest.approx(150.0, abs=1e-9)
        assert s2.expenses(1) == pytest.approx(twin.expenses(1), rel=1e-12)
    finally:
        s.close()
        fresh.close()


# The two tables shortened below their cover, each ending on a rate other than 0: the
# mortality stopped at attained age 110, both sexes, where cover runs to 119, so that
# every older age reads 110's rate; and the seven-year withdrawal charge stopped at three
# completed years, on 5.5%, where the shipped schedule runs on to 0% at seven, so that
# every later year reads 5.5%.  A reader that answered 0 past a table's end, or read its
# first row, would pass every test on the shipped tables, whose last rows are 1.0 at 120
# and 0%.
SHORT_AGE, SHORT_YEARS = 110, 3


def _short_mortality(table):
    return table[table["age"] <= SHORT_AGE]


def _short_charges(table):
    return table[~((table["cdsc_schedule"] == "commission_7yr")
                   & (table["completed_years"] > SHORT_YEARS))]


SHORT_TABLES = {"mort_table.csv": _short_mortality, "cdsc_table.csv": _short_charges}


def test_a_table_shortened_below_its_cover_reads_its_last_row_as_s_does(tmp_path):
    """Past a table's last row each reader reads that row, as ``VA_US_S`` does.

    ``VA_US_S`` caps the attained age at the mortality table's last and the completed years
    at the charge schedule's, and ``mort_rate_base_at`` and ``surr_charge_rate_at`` read
    ``min(x, top)`` and ``min(k, last)`` (USLIB-SEC-PLAN.md §7.6, *Keys and clamps*).  So
    both models are read on a copy with each table shortened below its cover
    (:data:`SHORT_TABLES`), on a table of the two committed rows that read past both ends,
    the anchor issued at the valuation date and the anchor valued at 131, in contract year
    11 at attained age 70, whose opening state neither table moves: each continues S's
    point 1 from its month in every cell, as the committed rows do (:func:`_continues_s`).
    Past each end the rate is the last row's, 5.5% from three completed years on and
    110's rate from 111 on, and the clamps' sides win: ``min(x, top)``'s, which no row of
    the splice binds (:data:`BOUND_ELSEWHERE`), and ``min(k, last)``'s, here with an
    effect on every surrender value.
    """
    committed = _committed()
    cases = (("twin", 1, 0), ("derived", 1, 131))
    table = committed.loc[[_label(committed, *case) for case in cases]]
    s = _read(temp_inputs(tmp_path / "s", model_path(TWIN), edits=SHORT_TABLES), "short_s")
    sec = _read(_sec_inputs(tmp_path / "sec", table, SHORT_TABLES), "short")
    try:
        s1 = _point(s, 1)
        _sweep_s(s1)
        bounds = _BoundSides(sec)
        with bounds.watch() as won:
            for case in cases:
                p = _row(sec, *case)
                found = _continues_s(s1, p, case[2], SPLICE_EXEMPT)
                assert not found, (case, found[:10])
        p = _row(sec, "twin", 1, 0)
        rates = sec.Data.mort_rates()
        last = float(rates.loc[(SHORT_AGE, "M"), "mort_rate"])
        old = [t for t in range(p.proj_len()) if p.age(t) > SHORT_AGE]
        assert old and all(p.mort_rate(t) == last for t in old)
        assert sec.Data.mort_last_age() == SHORT_AGE
        late = [t for t in range(p.proj_len()) if p.duration(t) > SHORT_YEARS]
        assert late and all(p.surr_charge_rate(t) == 0.055 for t in late)
        for side in (("mort_rate_base_at", "min(x, top)", 1),
                     ("surr_charge_rate_at", "min(k, last)", 1)):
            assert side in won, side
        assert BOUND_ELSEWHERE[("mort_rate_base_at", "min(x, top)", 1)] == (
            "test_a_table_shortened_below_its_cover_reads_its_last_row_as_s_does")
    finally:
        sec.close()
        s.close()


# The shipped References that a rewritten cell reads and that ship equal to another, which
# a formula reading the wrong one of a pair would pass at the shipped values
# (USLIB-SEC-PLAN.md §7.8, *Record — M10*, *Set-apart References*): the M&E charge and the
# CMT spread, 1%; the surrender rate of the charge years and the CMT floor, 4%; the bonus
# and the younger roll-up rate, 6%; the VIX formula's offset and the Bonus Period, 10; and
# the age the GWB Adjustment Date is set from and the roll-up rate's split, 70.  One of each
# pair moves a little, the M&E charge and the CMT spread both, so that no pair stays equal
# and every branch the twins take stays as it was.  The acquisition expense and the
# commission, both 0, are set apart in the splice (SPLICED_REFS).
APART_REFS = {"asset_charge_me": 0.0105, "cmt_spread": 0.0095, "lapse_rate_sc": 0.042,
              "cmt_floor": 0.038, "bonus_pct": 0.062, "rollup_pct_young": 0.058,
              "vix_offset": 10.5, "gwb_adj_age": 71}


def test_each_reference_that_ships_equal_to_another_is_read_as_itself():
    """A rewritten cell reads each Reference of a pair that ships equal as itself.

    Both models are read in place with :data:`APART_REFS` set before either computes
    anything.  The twin of each of S's new-business points, issued at the valuation date,
    is then S's point in every cell S evaluates, as T1 holds at the shipped values, and the
    twin of S's in-force point 2 continues S from ``t = 0`` as the committed rows do
    (:func:`_continues_s`), its acquisition at S's ``t == 0`` and expense inflation apart.
    A rewritten formula that read the wrong one of a pair, the bonus at the younger
    roll-up rate say, passes every comparison at the shipped values, and the splice's, and
    fails here.
    """
    s = _read(model_path(TWIN), "apart_s", APART_REFS)
    sec = _read(model_path(SEC), "apart", APART_REFS)
    try:
        assert all(getattr(sec.Projection, name) == value
                   for name, value in APART_REFS.items())
        found = {}
        for case in (*(("twin", p, 0) for p in S_POINTS), *IN_FORCE_TWINS):
            _, point, _ = case
            s_proj = _point(s, point)
            _sweep_s(s_proj)
            key = _row_key(sec, *case)
            proj = projection(sec, key)
            if case in IN_FORCE_TWINS:
                lines = _continues_s(s_proj, proj, 0, SPLICE_EXEMPT, s_in_force=True)
            else:
                lines = _compare(s_proj, proj, 0, TWIN_EXEMPT_DEFAULT | SPEC.exempt)
            if lines:
                found[case] = lines[:5]
            _release(sec, key, collect=True)
            _release(s, _key(s, point), collect=True)
        assert not found, found
    finally:
        sec.close()
        s.close()


# ---------------------------------------------------------------------------
# T5 -- validation
#
# Each malformed table is the committed one with one fault, built so that only the rule
# under test refuses it, wherever one can be: a column the rules tie to another is moved
# with it.  The checks run over the whole table as it is read, in Data, and the message
# names the file it read and the column or every point at fault.  A blank cell reads as NaN,
# and so does a text cell once the checks coerce the column to numbers, so each is refused
# as a number that is not one.  The repeated point_id holds another contract under the same
# label, as a bad extract would, so that the check must look at the labels and not at whole
# rows.  The point_ids are the committed table's: 1, 3 and 4, S's anchor, decline path and
# excess programme issued at the valuation date; 2, S's in-force point at 26, mid-year; 10,
# the anchor in its first policy year, 6; 11, the anchor at its first withdrawal, 120, a
# contract year's start; 12, the anchor in the year's last month after it, 131; 13, the
# decline path depleted at a year's start, 144; 14 and 15, the excess programme at its
# excess withdrawal, 60, and after it, 65; 16, the highest quarterly step-up at 40; 17, the
# VIX fee at 41; 18, the never-withdrawing roll-up depleted at 560; 19, the last policy
# month; 20, S's in-force point restated at its month 14, in force at 40; 21, the basic
# death benefit after its first withdrawal, 125; 22, the never-withdrawing basic death
# benefit before its GWB Adjustment Date, 100; and 23, the anchor issued 15 months on.  The
# rules that turn on the policy month are tested at the ends of their windows: the first
# policy year's at months 1 and 11, at two cents either side of the issue value, a part of a
# cent inside it accepted and month 12 an accepted edge; the step-up base's at 2 and 3
# months into the year; and the VIX prior's at months 2 and 3.  The rule of the locked GAWA%
# reads the GAWA grid at the ages the contract reached before the valuation month, which is
# tested at both ends of those ages: withdrawn with no GAWA% locked on the decline path,
# issued at 35, the shipped grid's first age, where 34, below it, is accepted (the edges
# test), and issued at 59 on a grid of 0% from 60, zero_mid, valued at 12 months, whose
# month before the valuation month is still at 59, where 13 months is accepted.  A
# subaccount value is refused just past a cent below 0, where a cent below it is read (the
# bounds test).  Where a fault breaks two rules by its nature, a value no rule can
# take alone, the case is named for the order it pins: the earlier rule must refuse it, with
# its own message, before the later one would refuse it otherwise: a month written as text,
# before the two joins that read the first month on the books, and an issue age written as
# text, before the mortality's join.  The last checks join each point's keys to the tables
# they key: a fund set, the returns of each of its subaccounts by its first month on the
# books, a programme, a GAWA grid, a withdrawal-charge schedule, and a sex and an attained
# age in the mortality table; and the withdrawal status against the GAWA% it locked.  A
# {file} in a message is the table's filename: every case reads its own file (the malformed
# fixture).

_POINT = "it is not at point_id {points}"
_COUNT = "{{file}}: policy_count must be a number, zero or more; " + _POINT
_DURATION = "{{file}}: duration_mth must be a whole number of months; " + _POINT
_WHOLE = "{{file}}: {column} must be a whole number, 0 or more; " + _POINT
_FLAG = "{{file}}: {column} must be True or False, or 1 or 0; " + _POINT
_NUMBER = "{{file}}: {column} must be a number, zero or more; " + _POINT
_FUND_VALUE = ("{{file}}: {column} must be a number, zero or more to within a cent; "
               + _POINT)
_TAX = "{{file}}: premium_tax_rate must be a number from 0 to below 1; " + _POINT
_RATE = "{{file}}: {column} must be a number from 0 to 1; " + _POINT
_NO_STATE = ("{{file}}: {column} must be 0 on a policy not yet in force, duration_mth 0 or "
             "less; " + _POINT)
_YEAR_START = ("{{file}}: on a point valued at a contract year's start, duration_mth a "
               "multiple of 12, {column} must be {empty}; " + _POINT)
_YEAR_FLAG = ("{{file}}: on a point valued at a contract year's start, wd_this_year_init "
              "must be False; " + _POINT)
_YEAR_RB = ("{{file}}: on a point valued at a contract year's start, rb_pp_prev_anniv_init "
            "must equal rb_pp_init; it does not at point_id {points}")
_STEPUP = ("{{file}}: stepup_base_pp_ytd_init must be 0 before the contract year's first "
           "quarterly anniversary, duration_mth % 12 below 3; " + _POINT)
_PHI = ("{{file}}: phi_glwb_init must be 0 on a policy in force unless it is on the vix "
        "rule and past its first contract quarter, duration_mth 3 or more; " + _POINT)
_FIRST_YEAR = ("{{file}}: rb_pp_prev_anniv_init must be its issue value in the first "
               "policy year, duration_mth 1 to 11, the premium credited at issue, to a "
               "cent; " + _POINT)
_BONUS_END = "{{file}}: bonus_end_init must be 1 or more on a policy in force; " + _POINT
_ADJ = ("{{file}}: adj_pp_init must be 0 on a policy that has withdrawn, has_wd_init True: "
        "any withdrawal voids the GWB Adjustment; " + _POINT)
_GAWA = ("{{file}}: gawa_pct_init must be more than 0 where gawa_pp_init is: the GAWA is "
         "the locked percentage of a base; " + _POINT)
_YEAR_WD = ("{{file}}: has_wd_init must be True where wd_this_year_init is: a withdrawal "
            "this year is a withdrawal; " + _POINT)
_YTD_FLAG = ("{{file}}: wd_this_year_init must be True where sum_wd_pp_ytd_init is more "
             "than 0; " + _POINT)
_YTD_PART = ("{{file}}: {column} must not exceed sum_wd_pp_ytd_init, the withdrawals it is "
             "part of, to a cent; it does at point_id {points}")
_FACTOR = ("{{file}}: gmdb_factor_acc_ytd_init must be 1 where sum_wd_pp_ytd_init is 0: "
           "only a withdrawal reduces it; " + _POINT)
_FUND_SET = "{{file}}: fund_set must be a fund set of fund_table.csv; " + _POINT
_NO_FUND = ("{{file}} has no {column} column, which point_id {points} needs: its fund set "
            "holds subaccount {i}")
_RETURN_JOIN = ("{{file}}: scenario_id must be a scenario of return_scenario_sec.csv that "
                "sets a return for each subaccount of the point's fund set by the first "
                "month the point is on the books, t = 0 or its issue month if later; "
                + _POINT)
_RATE_JOIN = ("{{file}}: scenario_id must be a scenario of rate_scenario_sec.csv that sets "
              "its levels by the first month the point is on the books, on a point the vix "
              "fee or the cmt_linked roll-up reads it for; " + _POINT)
_PROGRAMME = "{{file}}: txn_id must be a programme of transaction_table.csv; " + _POINT
_GRID = "{{file}}: glwb_option must be a grid of gawa_pct_table.csv; " + _POINT
_LOCKED = ("{{file}}: gawa_pct_init must be more than 0 where has_wd_init is True: the "
           "first withdrawal locks the GAWA% of the attained age it is taken at, which the "
           "point's grid gives as more than 0 at every attained age the policy reached "
           "before the valuation month; " + _POINT)
_BARE = ("{{file}}: gawa_pp_init must be more than 0 where gwb_pp_init and gawa_pct_init "
         "are: the withdrawal or the depletion that locked the GAWA% set the GAWA to it "
         "times the GWB, unless the point's grid gave 0% at an attained age the policy "
         "reached before the valuation month; " + _POINT)
_SCHEDULE = "{{file}}: cdsc_schedule must be a schedule of cdsc_table.csv; " + _POINT
_MORTALITY = ("{{file}}: mort_table.csv must give a rate at the point's sex and its "
              "attained age in the first month it is on the books; it does not at point_id "
              "{points}")


def _says(template, points, **names):
    """``template``'s message for ``points``, its ``{file}`` left for the case's file."""
    return template.format(points=points, **names)


def _twice(point):
    """The table with a second contract under point ``point``'s label."""
    return lambda t: pd.concat([t, t.loc[[point]].assign(policy_id="VA-900099")])


def _state_value(column):
    """A value of ``column`` that passes every check before the rule of new business."""
    return (True if column in FLAGS else 5 if column == "bonus_end_init"
            else 1.0 if column == "gmdb_factor_acc_ytd_init"
            else 0.05 if column in RATES_COLUMNS else 5.0)


# Row 10, the anchor at policy month 6 on its issue values, moved within its first policy
# year: the step-up base is 0 before the year's first quarterly anniversary.
def _first_year(month, **columns):
    return _cells(10, duration_mth=month, **({"stepup_base_pp_ytd_init": 0.0}
                                            if month < 3 else {}), **columns)


_YTD = 9573.749999993472            # row 12's withdrawals of the year to date, as written

MALFORMED = [
    *[(f"no {column} column", _drop(column), f"{{file}} has no {column} column")
      for column in ("policy_count", "duration_mth", *CHECKED_STATE)],
    ("a repeated point_id", _twice(2), "{file}: point_id [2] appears more than once"),
    ("a count written as text", _set("policy_count", [2], "x"), _says(_COUNT, [2])),
    ("a negative count", _set("policy_count", [2], -1.0), _says(_COUNT, [2])),
    ("an infinite count", _set("policy_count", [2], float("inf")), _says(_COUNT, [2])),
    ("a blank count", _set("policy_count", [2], float("nan")), _says(_COUNT, [2])),
    ("two bad counts", _both(_set("policy_count", [2], -1.0),
                             _set("policy_count", [3], -2.0)), _says(_COUNT, [2, 3])),
    ("a fractional duration", _set("duration_mth", [2], 26.5), _says(_DURATION, [2])),
    ("a duration written as text, before the joins that read it",
     _set("duration_mth", [2], "x"), _says(_DURATION, [2])),
    ("a fractional issue age", _set("age_at_entry", [1], 60.5),
     _says(_WHOLE, [1], column="age_at_entry")),
    ("an issue age written as text, before the mortality's join",
     _set("age_at_entry", [1], "x60"), _says(_WHOLE, [1], column="age_at_entry")),
    ("a negative withdrawal age", _set("wd_start_age", [1], -1),
     _says(_WHOLE, [1], column="wd_start_age")),
    ("a fractional bonus end", _set("bonus_end_init", [2], 12.5),
     _says(_WHOLE, [2], column="bonus_end_init")),
    ("issued beyond the horizon", _set("duration_mth", [23], -121),
     "{file}: duration_mth must be -120 or more, a policy issued at most 120 months after "
     "the valuation date; it is not at point_id [23]"),
    ("a withdrawal status written as yes", _set("has_wd_init", [2], "yes"),
     _says(_FLAG, [2], column="has_wd_init")),
    ("a blank year flag", _set("wd_this_year_init", [2], float("nan")),
     _says(_FLAG, [2], column="wd_this_year_init")),
    ("a negative premium", _set("premium", [1], -1.0),
     _says(_NUMBER, [1], column="premium")),
    ("an intensity written as text", _set("wd_intensity", [1], "x"),
     _says(_NUMBER, [1], column="wd_intensity")),
    ("a premium tax of 100%", _set("premium_tax_rate", [1], 1.0), _says(_TAX, [1])),
    ("a negative premium tax", _set("premium_tax_rate", [2], -0.1), _says(_TAX, [2])),
    *[(f"{column} below 0", _set(column, [10 if column == "stepup_base_pp_ytd_init" else 2],
                                 -1.0),
       _says(_NUMBER, [10 if column == "stepup_base_pp_ytd_init" else 2], column=column))
      for column in MONEY if column != "sum_wd_pp_ytd_init"],
    ("the year's withdrawals written as text", _set("sum_wd_pp_ytd_init", [2], "x"),
     _says(_NUMBER, [2], column="sum_wd_pp_ytd_init")),
    ("a blank GWB", _set("gwb_pp_init", [2], float("nan")),
     _says(_NUMBER, [2], column="gwb_pp_init")),
    ("an infinite remaining premium", _set("rp_pp_init", [2], float("inf")),
     _says(_NUMBER, [2], column="rp_pp_init")),
    ("a GAWA% above 1", _set("gawa_pct_init", [12], 1.5),
     _says(_RATE, [12], column="gawa_pct_init")),
    ("a proportional factor above 1", _set("gmdb_factor_acc_ytd_init", [2], 1.5),
     _says(_RATE, [2], column="gmdb_factor_acc_ytd_init")),
    ("a VIX prior above 1", _set("phi_glwb_init", [17], 1.5),
     _says(_RATE, [17], column="phi_glwb_init")),
    *[(f"{column} on new business", _set(column, [1], _state_value(column)),
       _says(_NO_STATE, [1], column=column)) for column in CHECKED_STATE],
    *[(f"{column} at a year's start", _set(column, [11], 100.0),
       _says(_YEAR_START, [11], column=column, empty="0"))
      for column in ("sum_wd_pp_ytd_init", "free_wd_used_cum_pp_ytd_init",
                     "gmdb_dfd_acc_pp_ytd_init")],
    ("a proportional factor below 1 at a year's start",
     _set("gmdb_factor_acc_ytd_init", [11], 0.9),
     _says(_YEAR_START, [11], column="gmdb_factor_acc_ytd_init", empty="1")),
    ("a withdrawal this year at a year's start", _set("wd_this_year_init", [11], True),
     _says(_YEAR_FLAG, [11])),
    ("a stale year-open RB at a year's start",
     _set("rb_pp_prev_anniv_init", [11], 170000.0),
     _says(_YEAR_RB, [11])),
    ("a step-up base at a year's start", _set("stepup_base_pp_ytd_init", [11], 100.0),
     _says(_STEPUP, [11])),
    ("a step-up base two months into the year", _set("stepup_base_pp_ytd_init", [2], 100.0),
     _says(_STEPUP, [2])),
    ("a VIX prior off the vix rule", _set("phi_glwb_init", [12], 0.01), _says(_PHI, [12])),
    ("a VIX prior in the first contract quarter",
     _cells(17, duration_mth=2, stepup_base_pp_ytd_init=0.0,
            rb_pp_prev_anniv_init=100000.0),
     _says(_PHI, [17])),
    ("a stale RB in the first policy year", _set("rb_pp_prev_anniv_init", [10], 99000.0),
     _says(_FIRST_YEAR, [10])),
    *[(f"an RB {cents:+d} cents off its issue value at month {month}",
       _first_year(month, rb_pp_prev_anniv_init=100000.0 + cents / 100.0),
       _says(_FIRST_YEAR, [10])) for month in (1, 11) for cents in (2, -2)],
    ("no bonus end in force", _set("bonus_end_init", [11], 0), _says(_BONUS_END, [11])),
    ("an adjustment after a withdrawal", _set("has_wd_init", [20], True),
     _says(_ADJ, [20])),
    ("a GAWA without its percentage", _set("gawa_pct_init", [12], 0.0), _says(_GAWA, [12])),
    ("a withdrawal this year without one ever", _set("wd_this_year_init", [10], True),
     _says(_YEAR_WD, [10])),
    ("withdrawals to date without the year flag", _set("wd_this_year_init", [12], False),
     _says(_YTD_FLAG, [12])),
    *[(f"{column} two cents above the withdrawals", _set(column, [12], _YTD + 0.02),
       _says(_YTD_PART, [12], column=column))
      for column in ("free_wd_used_cum_pp_ytd_init", "gmdb_dfd_acc_pp_ytd_init")],
    ("a proportional factor below 1 with no withdrawal",
     _set("gmdb_factor_acc_ytd_init", [10], 0.9), _says(_FACTOR, [10])),
    ("a fund set the table lacks", _set("fund_set", [1], "Core_60_40"),
     _says(_FUND_SET, [1])),
    *[(f"no sa_pp_init_{i} column", _drop(f"sa_pp_init_{i}"),
       _says(_NO_FUND, list(range(1, 24)), column=f"sa_pp_init_{i}", i=i)) for i in (1, 2)],
    ("a negative fund value", _set("sa_pp_init_1", [2], -1.0),
     _says(_FUND_VALUE, [2], column="sa_pp_init_1")),
    ("a fund value just past a cent below 0", _set("sa_pp_init_1", [18], -0.0101),
     _says(_FUND_VALUE, [18], column="sa_pp_init_1")),
    ("a fund value written as text", _set("sa_pp_init_2", [2], "x"),
     _says(_FUND_VALUE, [2], column="sa_pp_init_2")),
    *[(f"sa_pp_init_{i} on new business", _set(f"sa_pp_init_{i}", [1], 5.0),
       _says(_NO_STATE, [1], column=f"sa_pp_init_{i}")) for i in (1, 2)],
    ("a return scenario the companion lacks", _set("scenario_id", [1], "Base"),
     _says(_RETURN_JOIN, [1])),
    ("two return scenarios the companion lacks",
     _both(_set("scenario_id", [1], "Base"), _set("scenario_id", [3], "Decline")),
     _says(_RETURN_JOIN, [1, 3])),
    ("a programme the table lacks", _set("txn_id", [4], "Excess"), _says(_PROGRAMME, [4])),
    ("a GAWA grid the table lacks", _set("glwb_option", [1], "S3_Single"),
     _says(_GRID, [1])),
    ("withdrawn with no GAWA% locked",
     _cells(13, gawa_pct_init=0.0, gawa_pp_init=0.0), _says(_LOCKED, [13])),
    ("withdrawn with no GAWA% locked, issued at the grid's first age",
     _cells(13, gawa_pct_init=0.0, gawa_pp_init=0.0, age_at_entry=35),
     _says(_LOCKED, [13])),
    ("withdrawn with no GAWA% locked, the month before a 0% band's first age",
     _cells(13, gawa_pct_init=0.0, gawa_pp_init=0.0, age_at_entry=59, duration_mth=12,
            glwb_option="zero_mid"), _says(_LOCKED, [13])),
    ("a depleted contract that withdrew, its GAWA zeroed", _set("gawa_pp_init", [13], 0.0),
     _says(_BARE, [13])),
    ("one depleted without a withdrawal, its GAWA zeroed", _set("gawa_pp_init", [18], 0.0),
     _says(_BARE, [18])),
    ("a schedule the table lacks", _set("cdsc_schedule", [1], "x"), _says(_SCHEDULE, [1])),
    ("an issue age below the mortality table's first", _set("age_at_entry", [1], 39),
     _says(_MORTALITY, [1])),
    ("an attained age past the mortality table's last", _set("age_at_entry", [1], 121),
     _says(_MORTALITY, [1])),
    ("a sex the mortality table lacks", _set("sex", [1], "X"), _says(_MORTALITY, [1])),
]


@pytest.fixture(scope="module")
def malformed(tmp_path_factory):
    """Every table of :data:`MALFORMED`, each a file of its own, beside one model folder.

    Returns ``(folder, {case: filename})``.  Each case reads the model afresh and points
    ``Data.model_point_file`` at its own file before the model computes anything (a
    Reference set after a Space has computed does not reach a compiled model), so the
    files share one copy of the product directory, and no read.  The copy's GAWA grids
    hold zero_mid, 0% from 60 to 64 (:func:`_zero_band`), which no committed row reads, so
    that a case can sit at the edge of a 0% band.
    """
    root = tmp_path_factory.mktemp("malformed")
    files = {}
    folder = None
    for number, (case, edit, _) in enumerate(MALFORMED):
        files[case] = f"malformed_{number:03d}_sec.csv"
        folder = temp_inputs(root, model_path(SEC), model_points=edit(_committed()),
                             model_point_file=files[case],
                             edits={"gawa_pct_table.csv": _zero_band})
    return folder, files


def _file_key(model, table, label):
    """The ``Projection`` key of row ``label`` of ``table``, a table the model may refuse.

    A refused table gives no ``point_keys``, so the key is taken from the file, the way
    ``run_sec.py`` takes one: the row's position on a model indexed by position, and its
    label otherwise.
    """
    if model.Projection.parameters == ("idx",):
        return list(table.index).index(label)
    return label


@pytest.mark.parametrize("case, edit, message", MALFORMED, ids=[c[0] for c in MALFORMED])
def test_a_malformed_in_force_row_is_refused_naming_its_point(malformed, case, edit,
                                                               message):
    """``Data.model_point_table()`` refuses the table, naming the fault (D6, T5).

    And a projection meets the same refusal: the base ``Projection``'s default point and
    the first point of the file each read the table through their model point, and raise
    the table's own message, so that no point projects from a table the model refuses,
    compiled or not.  Each case is refused by the one rule it is built for; a case named
    for the order it pins, listed above the table, is refused by the earlier rule, with
    its message.
    """
    folder, files = malformed
    model = _read(folder, "malformed", data={"model_point_file": files[case]})
    try:
        text = message.format(file=files[case])
        _refused(model.Data.model_point_table, text)
        _refused(model.Projection.result_cf, text)
        table = pd.read_csv(folder.parent / files[case], index_col="point_id")
        _refused(model.Projection[_file_key(model, table, table.index[0])].result_cf, text)
    finally:
        model.close()


# The six assumption tables and the two companions, each with the Data Reference naming its
# file and the cell that checks it, which is the only way the projection reads the table
# (Data's docstring).
CHECKED = {"mort_table.csv": ("mort_table_file", "mort_rates"),
           "fund_table.csv": ("fund_file", "fund_sets"),
           RETURNS: ("return_scenario_file", "return_scenario_steps"),
           RATES: ("rate_scenario_file", "rate_scenario_steps"),
           "gawa_pct_table.csv": ("gawa_pct_file", "gawa_pct_bands"),
           "cdsc_table.csv": ("cdsc_file", "cdsc_scale"),
           "transaction_table.csv": ("transaction_file", "transactions")}


def _cell(column, row, value):
    """An edit of a plain table that writes ``value`` into ``column`` at row ``row``.

    ``row`` is the position among the data rows, so the file's line is ``row + 2``, its
    header line 1.  The column is made ``object`` first, so that text can go in.
    """
    def edit(table):
        table = table.assign(**{column: table[column].astype(object)})
        table.loc[row, column] = value
        return table
    return edit


def _repeat_row(row):
    """An edit of a plain table that writes data row ``row`` twice, the copy after it."""
    return lambda table: pd.concat([table.iloc[:row + 1], table.iloc[[row]],
                                    table.iloc[row + 1:]], ignore_index=True)


def _drop_where(**cells):
    """An edit of a plain table that leaves out the rows holding ``cells``."""
    def edit(table):
        hit = pd.Series(True, index=table.index)
        for column, value in cells.items():
            hit &= table[column] == value
        return table[~hit].reset_index(drop=True)
    return edit


_MORT_RUN = ("{file}: the ages of each sex must run one row an age, without a gap or a "
             "repeat")
_CDSC_RUN = ("{file}: the completed years of each schedule must run from 0, one row a "
             "year, without a gap or a repeat")

# Each assumption table and companion with one fault: (case, file, edit, message).  The
# message names the faulty file by {file}, the column and the file's lines.  The model
# point table joins every one of them, so a projection meets each fault as the table is
# read.  In every table a key written as text is refused, and each value a bound, a min or
# a max reads, blank, text or infinite; then a key out of its range, a blank text key, a
# repeated key, and keys that leave a gap where the projection reads every age or year
# between the first and the last, the message naming each repeated key with its lines and
# each key or span missing, and two faults in one table together.  The mortality table
# holds each age on two lines, male then female, from 40; the withdrawal charges hold the
# seven-year schedule's years 0 to 7, then the year 0 of the schedule with no charge.
TABLE_FAULTS = [
    ("mortality, a fractional age", "mort_table.csv", _cell("age", 0, 40.5),
     "{file}: age must be a whole number; it is not on line [2]"),
    ("mortality, an age written as text", "mort_table.csv", _cell("age", 3, "61x"),
     "{file}: age must be a whole number; it is not on line [5]"),
    ("mortality, a blank sex", "mort_table.csv", _cell("sex", 1, None),
     "{file}: sex must not be blank; it is on line [3]"),
    ("mortality, a rate above 1", "mort_table.csv", _cell("mort_rate", 2, 1.5),
     "{file}: mort_rate must be a number from 0 to 1; it is not on line [4]"),
    ("mortality, a rate written as text", "mort_table.csv", _cell("mort_rate", 2, "x"),
     "{file}: mort_rate must be a number from 0 to 1; it is not on line [4]"),
    ("mortality, a blank rate", "mort_table.csv", _cell("mort_rate", 2, None),
     "{file}: mort_rate must be a number from 0 to 1; it is not on line [4]"),
    ("mortality, an infinite rate", "mort_table.csv", _cell("mort_rate", 2, float("inf")),
     "{file}: mort_rate must be a number from 0 to 1; it is not on line [4]"),
    ("mortality, two rates at fault", "mort_table.csv",
     _both(_cell("mort_rate", 2, 2.0), _cell("mort_rate", 5, -0.1)),
     "{file}: mort_rate must be a number from 0 to 1; it is not on line [4, 7]"),
    ("mortality, a rate no point reads", "mort_table.csv", _cell("mort_rate", 159, 2.0),
     "{file}: mort_rate must be a number from 0 to 1; it is not on line [161]"),
    ("mortality, a male age repeated", "mort_table.csv", _repeat_row(20),
     f"{_MORT_RUN}; sex M age 50 repeats on lines [22, 23]"),
    ("mortality, a male age missing", "mort_table.csv", _drop_where(age=70, sex="M"),
     f"{_MORT_RUN}; no line holds sex M age 70"),
    ("mortality, three female ages missing", "mort_table.csv",
     _both(_drop_where(age=70, sex="F"), _drop_where(age=71, sex="F"),
           _drop_where(age=72, sex="F")),
     f"{_MORT_RUN}; no line holds sex F ages 70 to 72"),
    ("fund sets, a blank fund set", "fund_table.csv", _cell("fund_set", 0, None),
     "{file}: fund_set must not be blank; it is on line [2]"),
    ("fund sets, subaccount 0", "fund_table.csv", _cell("sub_id", 0, 0),
     "{file}: sub_id must be a whole number, 1 or more; it is not on line [2]"),
    ("fund sets, a subaccount written as text", "fund_table.csv", _cell("sub_id", 0, "1x"),
     "{file}: sub_id must be a whole number, 1 or more; it is not on line [2]"),
    ("fund sets, a fractional subaccount", "fund_table.csv", _cell("sub_id", 1, 1.5),
     "{file}: sub_id must be a whole number, 1 or more; it is not on line [3]"),
    ("fund sets, an allocation above 1", "fund_table.csv", _cell("alloc", 0, 1.5),
     "{file}: alloc must be a number from 0 to 1; it is not on line [2]"),
    ("fund sets, a fund expense written as text", "fund_table.csv",
     _cell("fund_expense", 1, "x"),
     "{file}: fund_expense must be a number from 0 to 1; it is not on line [3]"),
    ("fund sets, a subaccount twice", "fund_table.csv", _cell("sub_id", 1, 1),
     "{file}: a fund set must hold each subaccount once; one holds one twice on lines "
     "[2, 3]"),
    ("fund sets, allocations summing to 1.1", "fund_table.csv", _cell("alloc", 1, 0.5),
     "{file}: the allocations of a fund set must sum to 1; they do not in fund set "
     "['core_60_40']"),
    *[(f"{what}, a fractional month", name, _cell("t", 1, 12.5),
       "{file}: t must be a whole number, 0 or more; it is not on line [3]")
      for what, name in (("returns", RETURNS), ("rates", RATES))],
    *[(f"{what}, a month written as text", name, _cell("t", 1, "x"),
       "{file}: t must be a whole number, 0 or more; it is not on line [3]")
      for what, name in (("returns", RETURNS), ("rates", RATES))],
    *[(f"{what}, a negative month", name, _cell("t", 1, -1),
       "{file}: t must be a whole number, 0 or more; it is not on line [3]")
      for what, name in (("returns", RETURNS), ("rates", RATES))],
    *[(f"{what}, a blank scenario", name, _cell("scenario_id", 1, None),
       "{file}: scenario_id must not be blank; it is on line [3]")
      for what, name in (("returns", RETURNS), ("rates", RATES))],
    ("returns, subaccount 0", RETURNS, _cell("sub_id", 1, 0),
     "{file}: sub_id must be a whole number, 1 or more; it is not on line [3]"),
    ("returns, a subaccount written as text", RETURNS, _cell("sub_id", 1, "x"),
     "{file}: sub_id must be a whole number, 1 or more; it is not on line [3]"),
    ("returns, a return of -100%", RETURNS, _cell("gross_return", 1, -1.0),
     "{file}: gross_return must be a number above -1; it is not on line [3]"),
    ("returns, a return written as text", RETURNS, _cell("gross_return", 1, "x"),
     "{file}: gross_return must be a number above -1; it is not on line [3]"),
    ("returns, an infinite return", RETURNS, _cell("gross_return", 1, float("inf")),
     "{file}: gross_return must be a number above -1; it is not on line [3]"),
    ("returns, two in one month", RETURNS, _cell("t", 1, 0),
     "{file}: a scenario must set one return a month for each subaccount; one sets two on "
     "lines [2, 3]"),
    ("rates, a negative VIX-squared", RATES, _cell("vix_sq", 0, -1.0),
     "{file}: vix_sq must be a number zero or more; it is not on line [2]"),
    ("rates, a CMT of -100%", RATES, _cell("cmt10", 0, -1.0),
     "{file}: cmt10 must be a number above -1; it is not on line [2]"),
    ("rates, a VIX-squared written as text", RATES, _cell("vix_sq", 0, "x"),
     "{file}: vix_sq must be a number zero or more; it is not on line [2]"),
    ("rates, two in one month", RATES, _repeat_row(0),
     "{file}: a scenario must set one level a month; one sets two on lines [2, 3]"),
    ("GAWA grids, a blank grid", "gawa_pct_table.csv", _cell("gawa_grid", 0, None),
     "{file}: gawa_grid must not be blank; it is on line [2]"),
    ("GAWA grids, a fractional band age", "gawa_pct_table.csv", _cell("age_from", 0, 35.5),
     "{file}: age_from must be a whole number, 0 or more; it is not on line [2]"),
    ("GAWA grids, a band age written as text", "gawa_pct_table.csv",
     _cell("age_from", 2, "x"),
     "{file}: age_from must be a whole number, 0 or more; it is not on line [4]"),
    ("GAWA grids, a percentage above 1", "gawa_pct_table.csv", _cell("gawa_pct", 0, 1.5),
     "{file}: gawa_pct must be a number from 0 to 1; it is not on line [2]"),
    ("GAWA grids, a blank percentage", "gawa_pct_table.csv", _cell("gawa_pct", 0, None),
     "{file}: gawa_pct must be a number from 0 to 1; it is not on line [2]"),
    ("GAWA grids, a band started twice", "gawa_pct_table.csv", _cell("age_from", 1, 35),
     "{file}: a grid must start each band once; one starts a band twice on lines [2, 3]"),
    ("charges, a blank schedule", "cdsc_table.csv", _cell("cdsc_schedule", 0, None),
     "{file}: cdsc_schedule must not be blank; it is on line [2]"),
    ("charges, a fractional year", "cdsc_table.csv", _cell("completed_years", 1, 0.5),
     "{file}: completed_years must be a whole number; it is not on line [3]"),
    ("charges, a year written as text", "cdsc_table.csv",
     _cell("completed_years", 1, "1x"),
     "{file}: completed_years must be a whole number; it is not on line [3]"),
    ("charges, a charge above 1", "cdsc_table.csv", _cell("surr_charge_rate", 1, 1.5),
     "{file}: surr_charge_rate must be a number from 0 to 1; it is not on line [3]"),
    ("charges, a year below 0", "cdsc_table.csv", _cell("completed_years", 1, -1),
     f"{_CDSC_RUN}; schedule commission_7yr completed_years -1, below 0, is on lines [3]; "
     f"no line holds schedule commission_7yr completed_years 1"),
    ("charges, a year twice", "cdsc_table.csv", _cell("completed_years", 2, 1),
     f"{_CDSC_RUN}; schedule commission_7yr completed_years 1 repeats on lines [3, 4]; "
     f"no line holds schedule commission_7yr completed_years 2"),
    ("charges, a year missing", "cdsc_table.csv",
     _drop_where(cdsc_schedule="commission_7yr", completed_years=3),
     f"{_CDSC_RUN}; no line holds schedule commission_7yr completed_years 3"),
    ("charges, three years missing", "cdsc_table.csv",
     _both(_drop_where(cdsc_schedule="commission_7yr", completed_years=3),
           _drop_where(cdsc_schedule="commission_7yr", completed_years=4),
           _drop_where(cdsc_schedule="commission_7yr", completed_years=5)),
     f"{_CDSC_RUN}; no line holds schedule commission_7yr completed_years 3 to 5"),
    ("charges, no year 0", "cdsc_table.csv",
     _drop_where(cdsc_schedule="commission_7yr", completed_years=0),
     f"{_CDSC_RUN}; no line holds schedule commission_7yr completed_years 0"),
    ("charges, a schedule with no year 0 or later", "cdsc_table.csv",
     _cell("completed_years", 8, -1),
     f"{_CDSC_RUN}; schedule none completed_years -1, below 0, is on lines [10]; no line "
     f"holds schedule none completed_years 0"),
    ("programmes, a blank programme", "transaction_table.csv", _cell("txn_id", 1, None),
     "{file}: txn_id must not be blank; it is on line [3]"),
    ("programmes, a fractional month", "transaction_table.csv", _cell("t", 1, 60.5),
     "{file}: t must be a whole number, 0 or more; it is not on line [3]"),
    ("programmes, a month written as text", "transaction_table.csv", _cell("t", 1, "x"),
     "{file}: t must be a whole number, 0 or more; it is not on line [3]"),
    ("programmes, a negative withdrawal", "transaction_table.csv",
     _cell("wd_amount", 1, -1.0),
     "{file}: wd_amount must be a number, zero or more; it is not on line [3]"),
    ("programmes, a premium written as text", "transaction_table.csv",
     _cell("prem_amount", 2, "x"),
     "{file}: prem_amount must be a number, zero or more; it is not on line [4]"),
    ("programmes, an infinite withdrawal", "transaction_table.csv",
     _cell("wd_amount", 1, float("inf")),
     "{file}: wd_amount must be a number, zero or more; it is not on line [3]"),
    ("programmes, two in one month", "transaction_table.csv", _cell("t", 2, 60),
     "{file}: a programme must hold one row a month; one holds two on lines [3, 4]"),
]


@pytest.fixture(scope="module")
def malformed_tables(tmp_path_factory):
    """Every table of :data:`TABLE_FAULTS`, each a file of its own beside one model folder.

    Returns ``(folder, {case: filename})``.  Each file is the shipped table with the case's
    fault, written as plain CSV under the table's name and a number, so that each case
    points the table's Reference at its own file before the model computes anything, as
    the malformed fixture does with the model point table.
    """
    root = tmp_path_factory.mktemp("malformed_tables")
    folder = temp_inputs(root, model_path(SEC))
    files = {}
    for number, (case, source, edit, _) in enumerate(TABLE_FAULTS):
        files[case] = f"{source[:-4]}_fault_{number:02d}.csv"
        edit(pd.read_csv(folder.parent / source)).to_csv(folder.parent / files[case],
                                                         index=False)
    return folder, files


@pytest.mark.parametrize("case, source, edit, message", TABLE_FAULTS,
                         ids=[c[0] for c in TABLE_FAULTS])
def test_an_assumption_table_whose_keys_cannot_be_read_is_refused(malformed_tables, case,
                                                                 source, edit, message):
    """The cell that checks the table refuses it, naming the file and the lines (T5).

    ``VA_US_S`` reads each assumption table's keys and values as pandas reads them: one
    key written as text turns its column to text, and then a lookup raises an error that
    names no file, a programme's month or a band is silently missed, and a scenario's month
    sorts as text; and a blank rate a bound reads becomes the bound's, without a word.
    Here the table's checked cell, the one way the projection reads it, refuses the table,
    and so does a projection that reads it, the anchor's twin's ``result_cf()``, with the
    same message, before it reads a value from the table.  The twin's key is taken from the
    file (:func:`_file_key`): the model point table checks each point's keys against every
    one of the tables, so it reads them all and is refused with them.
    """
    folder, files = malformed_tables
    reference, checked = CHECKED[source]
    committed = _committed()
    model = _read(folder, "table")
    try:
        setattr(model.Data, reference, files[case])
        text = message.format(file=files[case])
        _refused(model.Data.cells[checked], text)
        key = _file_key(model, committed, _label(committed, "twin", 1, 0))
        _refused(model.Projection[key].result_cf, text)
    finally:
        model.close()


# The horizon's refusals (Data's rule of future business), which the horizon test reads:
# the Reference itself below 0, future business under a horizon of 0, and a point issued
# past a horizon of 14 months.
_HORIZON_NEGATIVE = "future_horizon_mth must be 0 months or more, not -1"
_HORIZON_NONE = ("{file}: duration_mth must be 0 or more: this model takes no future new "
                 "business; it is not at point_id [23]")
_HORIZON_14 = ("{file}: duration_mth must be -14 or more, a policy issued at most 14 "
               "months after the valuation date; it is not at point_id [23]")

# The scenarios' joins on a companion cut short, which the scenarios test reads: the
# future row's subaccount 2 set from month 27, after its issue at 15, and the VIX point's
# levels set from month 12, after the valuation date.
_RETURN_CUT = _says(_RETURN_JOIN, [23])
_RATE_CUT = _says(_RATE_JOIN, [6])

# Data's checking cells, in the order the projection first reads them: the model point
# table, which joins every other.
CHECKING_CELLS = ("model_point_table", "mort_rates", "fund_sets", "return_scenario_steps",
                  "rate_scenario_steps", "gawa_pct_bands", "cdsc_scale", "transactions")


def _pattern(node):
    """A regex for the text an f-string, a string or a sum of them makes, its ``column``
    named, every other field any text."""
    if isinstance(node, ast.JoinedStr):
        out = ""
        for part in node.values:
            if isinstance(part, ast.Constant):
                out += re.escape(part.value)
            elif isinstance(part.value, ast.Name) and part.value.id == "column":
                out += r"(?P<column>[a-z0-9_]+)"
            else:
                out += ".*?"
        return out
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return re.escape(node.value)
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        return _pattern(node.left) + _pattern(node.right)
    if isinstance(node, ast.IfExp):
        return f"(?:{_pattern(node.body)}|{_pattern(node.orelse)})"
    return ".*?"


def _literal(node, assigned):
    """The values a literal tuple, a name bound to one in the function, or one of their
    starred parts holds."""
    if isinstance(node, ast.Name):
        return _literal(assigned[node.id], assigned)
    if isinstance(node, (ast.Tuple, ast.List)):
        out = []
        for elt in node.elts:
            if isinstance(elt, ast.Starred):
                out += _literal(elt.value, assigned)
            elif isinstance(elt, (ast.Tuple, ast.List)):
                out.append(tuple(_literal(elt, assigned)))
            else:
                out += _literal(elt, assigned)
        return out
    return [ast.literal_eval(node)]


def _column_entries(loop, assigned, sub_ids):
    """The columns a ``for`` loop over columns goes through, by the name ``column`` takes:
    the loop's own literal, a pair's first item, or ``sa_pp_init_<i>`` for each subaccount
    of the committed fund sets where the loop runs over them."""
    target = loop.target
    if isinstance(target, ast.Name) and target.id == "i":
        return [f"sa_pp_init_{i}" for i in sub_ids]
    values = _literal(loop.iter, assigned)
    if isinstance(target, ast.Tuple):
        place = [elt.id for elt in target.elts].index("column")
        return [value[place] for value in values]
    return values


def _refusal_entries():
    """Every entry of Data's checks: ``{(cell, line, column or None): pattern}``.

    Each ``raise`` of each of :data:`CHECKING_CELLS`, read from the source of
    ``VA_US_SEC``'s ``Data``, is one entry, or one for each column of the loop it sits in
    where its message names the loop's column; and each fault a grouped message collects,
    ``faults.append(...)``, is an entry of its own, matched anywhere in the message.
    """
    tree = ast.parse((model_path(SEC) / "Data" / "__init__.py").read_text())
    sub_ids = sorted(set(pd.read_csv(model_path(SEC).parent / "fund_table.csv")["sub_id"]))
    entries = {}
    for cell in tree.body:
        if not (isinstance(cell, ast.FunctionDef) and cell.name in CHECKING_CELLS):
            continue
        assigned = {node.targets[0].id: node.value for node in ast.walk(cell)
                    if isinstance(node, ast.Assign)
                    and isinstance(node.targets[0], ast.Name)
                    and isinstance(node.value, (ast.Tuple, ast.List))}

        def visit(node, loops):
            if isinstance(node, ast.For):
                loops = (*loops, node)
            if isinstance(node, ast.Raise) and isinstance(node.exc, ast.Call):
                pattern = "^" + _pattern(node.exc.args[0]) + "$"
                columns = [None]
                if "(?P<column>" in pattern:
                    columns = _column_entries(loops[-1], assigned, sub_ids)
                for column in columns:
                    entries[(cell.name, node.lineno, column)] = pattern
            if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                    and node.func.attr == "append"
                    and isinstance(node.func.value, ast.Name)
                    and node.func.value.id == "faults"):
                entries[(cell.name, node.lineno, "grouped")] = _pattern(node.args[0])
            for child in ast.iter_child_nodes(node):
                visit(child, loops)
        visit(cell, ())
    return entries


def test_every_refusal_of_data_is_the_first_of_some_case():
    """Each rule of ``Data``'s checks, entry by entry, is the first refusal of a case.

    A rule that reads several columns in turn hides an entry dropped from inside it, and a
    sweep that drops whole rules does not see that (USLIB-SEC-PLAN.md §7.11, *Record — M8*,
    *Each rule entry by entry*).  So every ``raise`` of the eight cells that check an input,
    the model point table, the two companions and the five assumption tables, is read from
    ``Data``'s source (:func:`_refusal_entries`): one entry for each, or one for each column
    of the loop it sits in where its message names the column, and one for each fault a
    grouped message collects.  Each case's message, which its own test asserts is the
    model's first refusal of that case (:data:`MALFORMED`, :data:`TABLE_FAULTS`, the
    horizon's and the scenarios' refusals), is then matched to the one entry of the cell
    that checks the case's file whose message it is, with the column it names, and every
    entry is the first refusal of some case.  So an entry no case reaches, a column dropped
    from a loop or a check no case breaks, fails here, and so does a case two entries could
    have raised.
    """
    entries = _refusal_entries()
    cases = [("model_point_table", message.format(file=TABLE))
             for _, _, message in MALFORMED]
    cases += [(CHECKED[source][1], message.format(file=source))
              for _, source, _, message in TABLE_FAULTS]
    cases += [("model_point_table", message.format(file=TABLE)) for message in (
        _HORIZON_NEGATIVE, _HORIZON_NONE, _HORIZON_14, _RETURN_CUT, _RATE_CUT)]
    reached, ambiguous = set(), []
    for cell, message in cases:
        whole = [(key, found) for key, pattern in entries.items()
                 if key[0] == cell and key[2] != "grouped"
                 for found in [re.match(pattern, message)] if found]
        mine = [key for key, found in whole
                if key[2] in (None, found.groupdict().get("column"))]
        if len(mine) != 1:
            ambiguous.append((message, mine))
            continue
        reached.add(mine[0])
        reached |= {key for key, pattern in entries.items()
                    if key[2] == "grouped" and key[0] == mine[0][0]
                    and re.search(pattern, message)}
    assert not ambiguous, f"messages that are not one entry's: {ambiguous[:5]}"
    unreached = sorted(set(entries) - reached, key=str)
    assert not unreached, f"entries no case is refused by first: {unreached}"
    assert len(entries) > 60


# Each text value no decode knows (T5, USLIB-SEC-PLAN.md §7.1, precised at M3): a column of
# the model point table, on the anchor issued at the valuation date, set to a spelling
# VA_US_S does not know, in S and in SEC alike, as (column, the message).  Every decode of
# the column answers False for it, as each of VA_US_S's comparisons does, and the cell that
# branches on the decodes raises VA_US_S's own message, where VA_US_S raises it: the
# step-up basis at the first anniversary, the death benefit at the first month's claim,
# the fee rule at the first month's GLWB fee and the roll-up rule at the first month's
# roll-up base.  So a decode that answered an unknown value as one of the known, the last
# of a chain read as the fall-through, fails here.
UNDECODABLE = [("glwb_stepup_basis", "invalid stepup_basis"),
               ("gmdb_option", "invalid gmdb_option"),
               ("fee_reset_rule", "invalid fee_reset_rule"),
               ("rollup_rule", "invalid rollup_rule")]


@pytest.mark.parametrize("column, message", UNDECODABLE, ids=[c[0] for c in UNDECODABLE])
def test_an_undecodable_value_raises_s_message_in_both_models(tmp_path, column, message):
    """An unknown text value raises ``VA_US_S``'s message in both models, through a
    projection.

    S point 1 and its twin are each read from a copy holding the value ``x`` in the
    column, and ``Data`` reads the SEC table, which checks no such column, and each
    projection raises ``ValueError`` with ``VA_US_S``'s message, matched whole: the line
    that names the error is the same in both.
    """
    s_table = pd.read_csv(model_path(TWIN).parent / "model_point_table.csv",
                          index_col="point_id")
    committed = _committed()
    label = _label(committed, "twin", 1, 0)
    s = _read(temp_inputs(tmp_path / "s", model_path(TWIN),
                          model_points=_set(column, [1], "x")(s_table)), "undecodable_s")
    sec = _read(_sec_inputs(tmp_path / "sec", _set(column, [label], "x")(committed)),
                "undecodable")
    try:
        assert len(sec.Data.model_point_table()) == len(committed)
        for model, point_id in ((s, 1), (sec, label)):
            with pytest.raises(Exception) as excinfo:
                _point(model, point_id).result_cf()
            assert _raised(excinfo.value) == f"ValueError: {message}", (model.name, column)
    finally:
        sec.close()
        s.close()


def _starting(name, scenario, month, sub_id=None):
    """A companion edit: ``scenario``'s first level at ``month``, the levels before it
    dropped, but for the one in force there, which moves to ``month``; on the return
    scenario, for subaccount ``sub_id`` alone."""
    def edit(table):
        mine = table["scenario_id"] == scenario
        if sub_id is not None:
            mine &= table["sub_id"] == sub_id
        before = table.index[mine & (table["t"] < month)]
        moved = before[-1:] if not (mine & (table["t"] == month)).any() else before[:0]
        table = table.drop(index=before.difference(moved)).copy()
        table.loc[moved, "t"] = month
        return table
    return {name: edit}


def test_a_points_scenarios_must_set_their_levels_by_its_first_month_on_the_books(tmp_path):
    """A scenario may start after ``t = 0``, but not after a point that runs on it starts.

    Each scenario is a step function of the valuation month, and a point reads it from the
    first month it is on the books, ``t = 0`` or its issue month if later, so the
    companions hold, for the anchor issued 15 months on, ``base-F15``, a copy of its paths
    that sets nothing before month 15.  Its return path for subaccount 2 cut to start at 27,
    a step later, is refused for that point, by ``Data`` and by its projection, where the
    scenario's lookup would find no return and raise naming no file; its paths moved to
    start at 16 and back to 15, as committed, the first is refused and the second projects
    its frame, reading its first return in its issue month.  And ``variant``'s rates, which
    the VIX point issued at the valuation date reads, cut to start at 12, are refused for
    that point, on the books from ``t = 0``.  The rate scenario is joined only where the
    VIX fee or the CMT-linked roll-up reads it: ``decline``'s rates removed, which no point
    on ``decline`` reads, is an accepted edge (the edges test).  Each table is read on a
    model of its own.
    """
    committed = _committed()
    future = _label(committed, "future", 1, -15)
    vix = _label(committed, "twin", 6, 0)
    cut_27 = _starting(RETURNS, "base-F15", 27, sub_id=2)
    for edits, refused, message in (
            (cut_27, future, _RETURN_CUT),
            ({**_starting(RETURNS, "base-F15", 16), **_starting(RATES, "base-F15", 16)},
             future, _RETURN_CUT),
            ({**_starting(RETURNS, "base-F15", 15), **_starting(RATES, "base-F15", 15)},
             None, None),
            (_starting(RATES, "variant", 12), vix, _RATE_CUT)):
        folder = _sec_inputs(tmp_path / f"case{next(_names)}", committed, edits)
        model = _read(folder, "scenario")
        try:
            if refused is None:
                assert len(model.Data.model_point_table()) == len(committed)
                p = _point(model, future)
                assert p.inv_return_mth(15, 1) == _point(model, 1).inv_return_mth(0, 1)
                assert len(p.result_cf()) == 735
                assert np.isfinite(p.result_cf().to_numpy()).all()
            else:
                text = message.format(file=TABLE)
                assert f"[{refused}]" in text
                _refused(model.Data.model_point_table, text)
                _refused(model.Projection[_file_key(model, committed, refused)].result_cf,
                         text)
        finally:
            model.close()


# The spellings of a flag that Data reads beside True and False, each written for the
# whole column, as an extract writes it: 1 and 0, and 1.0 and 0.0.  The committed table
# writes True and False.
FLAG_SPELLINGS = {"flags_as_ints": int, "flags_as_floats": float}


@pytest.mark.parametrize("spelling", FLAG_SPELLINGS.values(), ids=FLAG_SPELLINGS)
def test_table_keys_written_as_floats_are_read_by_value(tmp_path, spelling):
    """A key written ``1.0`` is the whole number it holds, in every table, as in S.

    On a copy whose six assumption tables and two companions carry every integer key as a
    float, the age, the subaccount, the months, the band's age and the completed years,
    and whose model point table carries ``duration_mth``, the issue age, the Bonus Period's
    end and the withdrawal age as floats and the two flags as 1 and 0, or as 1.0 and 0.0
    (:data:`FLAG_SPELLINGS`), the rows read project exactly what the committed model
    projects: the anchor issued at the valuation date, the excess programme after its
    withdrawal and the VIX point valued mid-year, which together read every table, every
    integer column and each flag both ways, against the same rows of the committed model
    read beside it.  Each integer column is read back as the int the clocks count in, and
    each flag as the bool.
    """
    def floats(*columns):
        return lambda table: table.assign(**{c: table[c].astype(float) for c in columns})

    edits = {"mort_table.csv": floats("age"), "fund_table.csv": floats("sub_id"),
             RETURNS: floats("sub_id", "t"), RATES: floats("t"),
             "gawa_pct_table.csv": floats("age_from"),
             "cdsc_table.csv": floats("completed_years"),
             "transaction_table.csv": floats("t")}
    table = floats("duration_mth", "age_at_entry", "bonus_end_init", "wd_start_age")(
        _committed())
    table = table.assign(**{flag: table[flag].astype(spelling) for flag in FLAGS})
    model = _read(_sec_inputs(tmp_path, table, edits), "floats")
    committed = _read(model_path(SEC), "floats_committed")
    try:
        written = pd.read_csv(tmp_path / "cdsc_table.csv")
        assert written["completed_years"].dtype == float
        read = model.Data.model_point_table()
        assert read["duration_mth"].dtype == float
        for case in (("twin", 1, 0), ("derived", 4, 65), ("derived", 6, 41)):
            mine, base = _row(model, *case), _row(committed, *case)
            for report in REPORTS:
                assert frame_mismatches(base.cells[report](), mine.cells[report](), rtol=0,
                                        atol=0) == [], (case, report)
            for cell in ("duration_mth_init", "bonus_end_init", "wd_start_age"):
                value = mine.cells[cell]()
                assert type(value) is int and value == base.cells[cell](), (case, cell)
            for cell in FLAGS:
                value = mine.cells[cell]()
                assert value is base.cells[cell](), (case, cell)
    finally:
        committed.close()
        model.close()


def test_the_future_horizon_is_a_reference_that_bounds_future_business(tmp_path):
    """``Data.future_horizon_mth`` refuses a contract issued later than it; 0 refuses all.

    The committed table's one future point is issued 15 months on.  It reads at the
    shipped 120 months and at 15, the shortest horizon that admits it, and is refused at
    14, by name, and at 15 it projects its 735 months.  At 0 the model takes no future new
    business, D4's fallback for a product that cannot support it, and the message says so.
    A negative horizon is itself refused, even on a table holding only contracts in force,
    which no horizon could refuse.  Each value is set on a model read afresh, before it
    computes anything.
    """
    committed = _committed()
    future = _label(committed, "future", 1, -15)
    assert future == 23
    folder = _sec_inputs(tmp_path / "all", committed)
    in_force = _sec_inputs(tmp_path / "in_force", committed[committed["duration_mth"] > 0])
    for where, horizon, refusal in ((folder, None, None), (folder, 15, None),
                                    (folder, 14, _HORIZON_14), (folder, 0, _HORIZON_NONE),
                                    (in_force, -1, _HORIZON_NEGATIVE)):
        data = {} if horizon is None else {"future_horizon_mth": horizon}
        model = _read(where, "horizon", data=data)
        try:
            if horizon is None:
                assert model.Data.future_horizon_mth == 120
            if refusal is None:
                assert len(model.Data.model_point_table()) == len(committed), horizon
            else:
                _refused(model.Data.model_point_table, refusal.format(file=TABLE))
            if horizon == 15:
                assert len(_point(model, future).result_cf()) == 735
        finally:
            model.close()


# proj_len()'s refusals (T5), each a case of its own: (case, the row as (kind, S point,
# month), the columns changed on it, and the message, or the frame's length where the point
# projects).  Whether a point is in cover is a rule of the product, not of the table: it
# needs omega_age, a Projection Reference, so the table reads, and the point is refused
# where its frame is defined, on its first projection, rather than projecting nothing.  The
# anchor issued at 120, the age cover ends at, is refused as a contract with no cover at
# all, and issued at 119 projects its twelve months; the never-withdrawing basic death
# benefit in its last policy month moved on to 720, the month its cover has ended, a
# contract year's start where its step-up base is 0, is refused, and at 719 projects its
# one month.  So is each opening state no contract can be in by a rule needing a
# Projection Reference, on a row Data reads: the highest quarterly step-up at 40, with a
# GAWA% and a GAWA locked but neither a withdrawal nor depletion, and moved to 39 and to
# 47, three and eleven months into its year, the window's first month and its last, with
# no quarterly history, which at 38 and 48, the months either side of the window,
# projects; the never-withdrawing roll-up depleted at 560 with no GAWA% locked; and the
# VIX fee moved into its second contract quarter's first month, 3, and its last, 5, with a
# prior other than phi_glwb_curr, which at 2, the month before, with no prior, and at 6,
# the month after, inside the corridor, projects, and into its third quarter's first, 6,
# and kept at 41, with a prior below the corridor, and at 41 one above it.  The rules on
# the depletion threshold are tested on both sides of it: the step-up history at exactly
# av_depletion_threshold, 0.005, three months into the year, is refused, where 0.0051 is
# read (the edges test); and the never-withdrawing roll-up depleted at 560 with an account
# value of 0.6 cents, just above the threshold, so not depleted, its GAWA% locked with no
# withdrawal, is refused, where half a cent and less enters month 0 depleted (the edges
# test).  Every table is the committed one relabeled 100 + point_id and written in reverse
# order (_relabeled), so that the label a refusal names is no position.
_VIX_EARLY = {"rb_pp_prev_anniv_init": 100000.0}
_CORRIDOR = ("point_id {{label}}: phi_glwb_init must be at most vix_corridor_hi, 0.025, "
             "and at least vix_corridor_lo, 0.006, where phi_glwb_curr is, from the third "
             "contract quarter, duration_mth 6 or more: the clip holds every rate after "
             "the first there; it is {phi}")
NOT_ISSUED = [
    ("issued at the age cover ends", ("twin", 1, 0), {"age_at_entry": 120},
     "point_id {label}: age_at_entry 120 is at or past omega_age 120: the contract has no "
     "cover"),
    ("issued a year before it", ("twin", 1, 0), {"age_at_entry": 119}, 12),
    ("valued at the end of cover", ("derived", 7, 719),
     {"duration_mth": 720, "stepup_base_pp_ytd_init": 0.0},
     "point_id {label}: duration_mth 720 is at or past the end of cover, policy month 720"),
    ("valued in its last covered month", ("derived", 7, 719), {}, 1),
    ("a GAWA% locked with neither a withdrawal nor depletion", ("derived", 5, 40),
     {"gawa_pct_init": 0.04, "gawa_pp_init": 4000.0},
     "point_id {label}: gawa_pct_init must be 0 on a policy that has not withdrawn and is "
     "not depleted, its account value above av_depletion_threshold 0.005: the GAWA% locks "
     "at the first withdrawal or at depletion; it is 0.04"),
    ("depleted without a withdrawal, with no GAWA% locked", ("derived", 8, 560),
     {"gawa_pct_init": 0.0, "gawa_pp_init": 0.0},
     "point_id {label}: gawa_pct_init must be more than 0 on a depleted policy that has "
     "not withdrawn: depletion locks the GAWA% of the attained age it falls at, which the "
     "point's grid gives as more than 0 at every attained age the policy reached before "
     "the valuation month"),
    ("no quarterly history three months into the year", ("derived", 5, 40),
     {"duration_mth": 39, "stepup_base_pp_ytd_init": 0.0},
     "point_id {label}: stepup_base_pp_ytd_init must be above av_depletion_threshold 0.005 "
     "on a policy not depleted, duration_mth % 12 3 or more: every quarter end of the year "
     "before the valuation month closed above it; it is 0.0"),
    ("no quarterly history in the year's last month", ("derived", 5, 40),
     {"duration_mth": 47, "stepup_base_pp_ytd_init": 0.0},
     "point_id {label}: stepup_base_pp_ytd_init must be above av_depletion_threshold 0.005 "
     "on a policy not depleted, duration_mth % 12 3 or more: every quarter end of the year "
     "before the valuation month closed above it; it is 0.0"),
    ("no quarterly history two months into the year", ("derived", 5, 40),
     {"duration_mth": 38, "stepup_base_pp_ytd_init": 0.0}, 682),
    ("no quarterly history at the next year's start", ("derived", 5, 40),
     {"duration_mth": 48, "stepup_base_pp_ytd_init": 0.0}, 672),
    ("a quarterly history at the threshold three months into the year", ("derived", 5, 40),
     {"duration_mth": 39, "stepup_base_pp_ytd_init": 0.005},
     "point_id {label}: stepup_base_pp_ytd_init must be above av_depletion_threshold 0.005 "
     "on a policy not depleted, duration_mth % 12 3 or more: every quarter end of the year "
     "before the valuation month closed above it; it is 0.005"),
    ("an account value just above the threshold, a GAWA% locked with no withdrawal",
     ("derived", 8, 560), {"sa_pp_init_1": 0.006},
     "point_id {label}: gawa_pct_init must be 0 on a policy that has not withdrawn and is "
     "not depleted, its account value above av_depletion_threshold 0.005: the GAWA% locks "
     "at the first withdrawal or at depletion; it is 0.062"),
    ("a VIX prior other than phi_glwb_curr in the second quarter's first month",
     ("derived", 6, 41), {"duration_mth": 3, **_VIX_EARLY, "phi_glwb_init": 0.013},
     "point_id {label}: phi_glwb_init must be phi_glwb_curr, 0.0125, in the second "
     "contract quarter, duration_mth 3 to 5: the prior is the first quarter's rate; it is "
     "0.013"),
    ("a VIX prior other than phi_glwb_curr in the second quarter's last month",
     ("derived", 6, 41), {"duration_mth": 5, **_VIX_EARLY, "phi_glwb_init": 0.013},
     "point_id {label}: phi_glwb_init must be phi_glwb_curr, 0.0125, in the second "
     "contract quarter, duration_mth 3 to 5: the prior is the first quarter's rate; it is "
     "0.013"),
    ("no VIX prior in the first quarter's last month", ("derived", 6, 41),
     {"duration_mth": 2, **_VIX_EARLY, "phi_glwb_init": 0.0,
      "stepup_base_pp_ytd_init": 0.0}, 718),
    ("a VIX prior other than phi_glwb_curr in the third quarter", ("derived", 6, 41),
     {"duration_mth": 6, **_VIX_EARLY, "phi_glwb_init": 0.013}, 714),
    ("a VIX prior below the corridor in the third quarter", ("derived", 6, 41),
     {"duration_mth": 6, **_VIX_EARLY, "phi_glwb_init": 0.005},
     _CORRIDOR.format(phi=0.005)),
    ("a VIX prior of 0", ("derived", 6, 41), {"phi_glwb_init": 0.0},
     _CORRIDOR.format(phi=0.0)),
    ("a VIX prior above the corridor", ("derived", 6, 41), {"phi_glwb_init": 0.03},
     _CORRIDOR.format(phi=0.03)),
]


@pytest.mark.parametrize("case, row, columns, outcome", NOT_ISSUED,
                         ids=[c[0] for c in NOT_ISSUED])
def test_a_point_past_its_cover_is_refused_by_proj_len(tmp_path, case, row, columns,
                                                       outcome):
    """A point whose cover has ended, or that has none, has no frame: ``proj_len()`` says.

    And so does a point whose opening state a rule needing a ``Projection`` Reference
    forbids: a GAWA% locked with neither a withdrawal nor depletion, none on a contract
    depleted without a withdrawal, no quarterly history on a contract not depleted three to
    eleven months into its year, and a VIX prior that no quarter's rate can be, each rule
    that holds over a window of months refused at the window's first month and at its
    last, where it has one, and admitted in the month on either side of it, here or, for
    the corridor's first month, in the edges test.  Each case of
    :data:`NOT_ISSUED` is read on a model of its own: the table reads, and the point's
    projection raises ``ValueError`` naming it, the message matched whole, or, where the
    case is one the rule admits, projects its frame, every number finite and the three
    checks closing.
    """
    committed = _committed()
    label = 100 + _label(committed, *row)
    table = _cells(label, **columns)(_relabeled(committed))
    model = _read(_sec_inputs(tmp_path, table), "past")
    try:
        assert len(model.Data.model_point_table()) == len(committed)
        p = _point(model, label)
        if isinstance(outcome, int):
            frame = p.result_cf()
            assert len(frame) == p.proj_len() == outcome
            assert np.isfinite(frame.to_numpy()).all()
            assert p.check_av_roll_fwd() and p.check_pols_roll_fwd()
            assert p.check_charge_split()
        else:
            with pytest.raises(Exception) as excinfo:
                p.result_cf()
            assert _raised(excinfo.value) == "ValueError: " + outcome.format(label=label)
    finally:
        model.close()


def _run_sec(script, *args, check=True):
    """Run ``script``, a ``run_sec.py``, with ``args``; its output, checked ASCII.

    With ``check=False`` the finished process is returned instead, whatever its exit code,
    for a test that expects the runner to fail.
    """
    done = subprocess.run([sys.executable, str(script), *args], capture_output=True,
                          timeout=600)
    if not check:
        return done
    assert done.returncode == 0, done.stderr.decode(errors="replace")
    assert done.stdout.isascii(), "run_sec.py printed a non-ASCII character"
    return done.stdout.decode("ascii")


def test_run_sec_block_asks_every_point_for_its_frame_first(tmp_path):
    """``run_sec.py --block`` refuses a point past its cover before it prints anything.

    A loop over the block would meet such a point only when it reached it, after
    projecting the points before it, so the runner asks every point for its frame first:
    run beside :data:`NOT_ISSUED`'s table, the last policy month's point moved on to 720,
    it fails naming the point, and prints nothing before.
    """
    committed = _committed()
    last = 100 + _label(committed, "derived", 7, 719)
    table = _cells(last, duration_mth=720, stepup_base_pp_ytd_init=0.0)(
        _relabeled(committed))
    folder = _sec_inputs(tmp_path, table)
    runner = folder.parent / "run_sec.py"
    shutil.copy(model_path(SEC).parent / "run_sec.py", runner)
    done = _run_sec(runner, "--block", check=False)
    assert done.returncode != 0 and done.stdout == b""
    assert (f"point_id {last}: duration_mth 720 is at or past the end of cover, policy "
            f"month 720" in done.stderr.decode(errors="replace"))


def _zero_band(table):
    """The GAWA grids with one that pays 0% from 60 to 64, for a test."""
    extra = pd.DataFrame([("zero_mid", age, pct, "a test") for age, pct in
                          ((35, 0.04), (60, 0.0), (65, 0.05))], columns=table.columns)
    return pd.concat([table, extra], ignore_index=True)


def _without_decline_rates(table):
    """The rate scenarios without decline's, which no point on decline reads."""
    return table[~table["scenario_id"].str.startswith("decline")]


def test_the_edges_of_the_in_force_interface_are_accepted(tmp_path):
    """What a contract in force can be is read: the edges each rule allows, and no more.

    Copies of committed rows, appended under ids of their own, each read and projected,
    every number of its frame finite and the three checks closing:

    * the first policy year at both ends, the anchor's row at 6 moved to policy months 1
      and 11 on its issue values, a year-open roll-up base a part of a cent off its issue
      value, and month 12, the second year, its year-open roll-up base the one entering
      the month, which the first-year rule no longer ties to the premium;
    * the free allowance used a part of a cent above the year's withdrawals;
    * the step-up base's history at policy month 39, three months into the year, where it
      may be above 0, and the VIX prior at month 3, the second quarter's first month;
    * a withdrawal status with no GAWA% locked where the grid gave 0%: issued at 34, below
      the grid's first band, and in force in a band at 0%, on a grid of the test's own,
      zero_mid, at both ends of the ages read: issued at 60, the band's first, and at 59,
      valued at 13 months, whose month before the valuation month is its first at 60, which
      at 12 months is refused (:data:`MALFORMED`, as issued at 35 is on the shipped grid);
      on that grid, a contract depleted without a withdrawal with no GAWA% and no GAWA,
      which ``proj_len()`` admits there alone; and a depleted contract with a GWB and a
      GAWA% above 0 and no GAWA, the GAWA% read again past the band after the depletion
      locked 0 and froze the GAWA there;
    * a depleted contract that never withdrew, marked as one that did, whose GAWA% is
      locked; and a count of 0, a point that projects zeros;
    * the VIX prior at the second quarter's last month, 5, at ``phi_glwb_curr``, and in the
      fourteenth quarter at each end of the corridor, 0.6% and 2.5%; and the highest
      quarterly history three months into the year just above ``av_depletion_threshold``;
    * the contract depleted without a withdrawal with an account value carried in of
      exactly ``av_depletion_threshold``, half a cent, and of part of it, each of which
      enters month 0 depleted, as the account value S leaves where a depletion closes on a
      rounding above 0 does, which an account value of 0.6 cents is not
      (:data:`NOT_ISSUED`);
    * and ``decline``'s rates removed: the rate scenario is joined only for a point the VIX
      fee or the CMT-linked roll-up reads it for, which no point on ``decline`` is.

    And on a model whose first quarter's VIX fee, ``phi_glwb_curr``, is 0.1%, below the
    corridor's foot, a VIX point in its third quarter carrying the second quarter's rate
    the clip gives there, 0.5%, below the foot too: the clip's band about a prior below the
    foot keeps the next rate below it, so ``proj_len()`` holds the prior to the foot only
    from a first rate at or above it.  At the shipped 1.25% the same row is refused
    (:data:`NOT_ISSUED`).

    Each copy's ``row_kind`` says what it is, which no formula reads, so the rows it copies
    are still found as the ones they are.
    """
    committed = _committed()
    first, ytd, depleted, hq, vix, never = (
        _label(committed, "derived", s_point, month)
        for s_point, month in ((1, 6), (1, 131), (3, 144), (5, 40), (6, 41), (8, 560)))
    at = committed.at
    copies = {
        101: (first, {"duration_mth": 1, "stepup_base_pp_ytd_init": 0.0}),
        102: (first, {"duration_mth": 11}),
        103: (first, {"rb_pp_prev_anniv_init": at[first, "rb_pp_prev_anniv_init"]
                      + 0.009}),
        104: (first, {"duration_mth": 12, "rb_pp_prev_anniv_init": 104000.0,
                      "rb_pp_init": 104000.0, "stepup_base_pp_ytd_init": 0.0}),
        105: (ytd, {"free_wd_used_cum_pp_ytd_init": at[ytd, "sum_wd_pp_ytd_init"]
                    + 0.009}),
        106: (hq, {"duration_mth": 39}),
        107: (vix, {"duration_mth": 3, "rb_pp_prev_anniv_init": 100000.0,
                    "phi_glwb_init": 0.0125}),
        108: (depleted, {"gawa_pct_init": 0.0, "gawa_pp_init": 0.0, "age_at_entry": 34}),
        109: (depleted, {"gawa_pct_init": 0.0, "gawa_pp_init": 0.0, "duration_mth": 13,
                         "glwb_option": "zero_mid", "stepup_base_pp_ytd_init": 0.0}),
        110: (never, {"has_wd_init": True}),
        111: (first, {"policy_count": 0.0}),
        112: (never, {"gawa_pct_init": 0.0, "gawa_pp_init": 0.0,
                      "glwb_option": "zero_mid"}),
        113: (vix, {"duration_mth": 5, "rb_pp_prev_anniv_init": 100000.0,
                    "phi_glwb_init": 0.0125}),
        114: (vix, {"phi_glwb_init": 0.006}),
        115: (vix, {"phi_glwb_init": 0.025}),
        116: (hq, {"duration_mth": 39, "stepup_base_pp_ytd_init": 0.0051}),
        117: (never, {"sa_pp_init_1": 0.005}),
        118: (never, {"sa_pp_init_1": 0.003}),
        119: (depleted, {"gawa_pct_init": 0.0, "gawa_pp_init": 0.0, "age_at_entry": 59,
                         "duration_mth": 13, "glwb_option": "zero_mid"}),
        120: (depleted, {"gawa_pp_init": 0.0, "glwb_option": "zero_mid"}),
    }
    rows = [committed.loc[[row]].assign(**changes, row_kind="copy").set_axis([label])
            for label, (row, changes) in copies.items()]
    table = pd.concat([committed, *rows]).rename_axis("point_id")
    edits = {"gawa_pct_table.csv": _zero_band, RATES: _without_decline_rates}
    model = _read(_sec_inputs(tmp_path / "edges", table, edits), "edges")
    try:
        assert list(model.Data.model_point_table().index) == list(table.index)
        for label in copies:
            p = _point(model, label)
            assert np.isfinite(p.result_cf().to_numpy()).all(), label
            assert p.check_av_roll_fwd() and p.check_pols_roll_fwd(), label
            assert p.check_charge_split(), label
        assert [_point(model, label).policy_year(0) for label in (101, 102, 104)] == [
            1, 1, 2]
        assert _point(model, 109).gawa_pct_at_age(60) == 0.0
        assert _point(model, 112).depleted_open(0) and _point(model, 112).gawa_pp(0) == 0.0
        assert [_point(model, label).phi_glwb_init() for label in (113, 114, 115)] == [
            0.0125, 0.006, 0.025]
        assert _point(model, 110).has_wd_by(0) and not _point(model, never).has_wd_by(0)
        zero = _point(model, 111)
        assert (zero.result_cf() == 0.0).all().all()
        assert zero.av_pp(0) == _point(model, first).av_pp(0)
        assert "decline" not in set(model.Data.rate_scenario_steps().index.get_level_values(
            "scenario_id"))
        assert [(_point(model, label).av_pp_init(), _point(model, label).depleted_open(0))
                for label in (117, 118)] == [(0.005, True), (0.003, True)]
        assert _point(model, 119).gawa_pct_at_age(60) == 0.0
        p = _point(model, 120)
        assert p.gawa_pp_init() == 0.0 < p.gawa_pct_init() and p.gwb_pp_init() > 0.0
    finally:
        model.close()
    early = committed.loc[[vix]].assign(duration_mth=6, rb_pp_prev_anniv_init=100000.0,
                                        phi_glwb_init=0.005, row_kind="copy")
    early = early.set_axis([121])
    model = _read(_sec_inputs(tmp_path / "low_fee", pd.concat([committed, early])
                              .rename_axis("point_id")), "edges_low_fee",
                  {"phi_glwb_curr": 0.001})
    try:
        p = _point(model, 121)
        assert np.isfinite(p.result_cf().to_numpy()).all()
        assert p.check_av_roll_fwd() and p.check_pols_roll_fwd() and p.check_charge_split()
        assert p.contract_quarter(0) == 3 and p.phi_glwb_init() == 0.005 < p.vix_corridor_lo
        assert p.vix_corridor_lo <= p.phi_glwb_vix(3) <= p.phi_glwb_init() + p.vix_band
    finally:
        model.close()


# Each value column at each bound of its range that a contract can hold, which Data's rules
# include, written into a copy of a committed row or into a table of the test's own beside
# the shipped ones: the allocation and the fund expense at 0 and 1, in a fund set; the
# GAWA% at 1, in a grid, locked by a withdrawal at 61; the withdrawal charge at 1 and 0, in
# a schedule; the mortality at 0 at age 40 and 1 at 41, male, read by the anchor issued at
# 40; a return and a CMT just above -1 and a VIX-squared average of 0, in a scenario read
# by the VIX point; the locked GAWA% at 1 and the GMDB's proportional factor of the year at
# 0, on the anchor at 131; a premium, a withdrawal intensity and a premium tax of 0, on
# the anchor issued at the valuation date; and a subaccount value a cent below 0, on
# the contract depleted without a withdrawal at 560.  Each copy: (label, row, its
# columns).
BOUND = -0.999999
AT_BOUNDS = {
    201: (("twin", 1, 0), {"fund_set": "edge_set", "cdsc_schedule": "edge_charge"}),
    202: (("twin", 1, 0), {"age_at_entry": 40}),
    203: (("twin", 1, 0), {"glwb_option": "full_grid", "wd_start_age": 61}),
    204: (("twin", 6, 0), {"scenario_id": "edge"}),
    205: (("derived", 1, 131), {"gawa_pct_init": 1.0, "gmdb_factor_acc_ytd_init": 0.0}),
    206: (("twin", 1, 0), {"premium": 0.0, "wd_intensity": 0.0, "premium_tax_rate": 0.0}),
    208: (("derived", 8, 560), {"sa_pp_init_1": -0.01}),
}


def _bounds_tables():
    """The edits that give :data:`AT_BOUNDS`' copies their tables, by file."""
    def rows(*values):
        return lambda table: pd.concat(
            [table, pd.DataFrame([(*v, "a test") for v in values], columns=table.columns)],
            ignore_index=True)

    def mortality(table):
        table = table.copy()
        for age, rate in ((40, 0.0), (41, 1.0)):
            table.loc[(table["age"] == age) & (table["sex"] == "M"), "mort_rate"] = rate
        return table

    return {"fund_table.csv": rows(("edge_set", 1, 0.0, 0.0, "equity"),
                                   ("edge_set", 2, 1.0, 1.0, "fixed income")),
            "cdsc_table.csv": rows(("edge_charge", 0, 1.0), ("edge_charge", 1, 0.0)),
            "gawa_pct_table.csv": rows(("full_grid", 35, 1.0)),
            "mort_table.csv": mortality,
            RETURNS: rows(*((("edge", i, 0, BOUND)) for i in (1, 2)),
                          ("edge", 1, 1, 0.004), ("edge", 2, 1, 0.0015)),
            RATES: rows(("edge", 0, 0.0, BOUND))}


def test_a_value_at_the_bound_of_its_range_is_read(tmp_path):
    """Each value column holds the bounds of its range, which ``Data`` reads (§5.1, step 6).

    ``Data`` holds each value to a range, and a rule written with the wrong bound, ``< 1``
    for ``<= 1``, refuses a value a contract can hold.  So a copy holding each column at
    each bound a contract can reach (:data:`AT_BOUNDS`) reads, and each copy projects its
    frame, every number finite and the three checks closing, reading the bound where it
    is: a subaccount with no allocation and one with all of it and a fund expense of 100%,
    a charge of 100% in the first year and none after, a mortality of 0 and then 1 that
    leaves no contract in force after the second year, a GAWA% of 100% locked at the
    first withdrawal, a month's return and a CMT of -99.9999% and a VIX average of 0, a
    locked GAWA% of 100% and a year's proportional factor of 0 carried in, a premium, a
    withdrawal intensity and a premium tax of 0, and a subaccount value a cent below 0,
    read as the rounding about 0 a depletion closes on, the contract depleted.  And on
    a model whose first quarter's VIX fee, ``phi_glwb_curr``, is 100%, a contract in its
    second quarter carrying that rate as its prior, ``phi_glwb_init`` 1, which ``Data``
    admits and ``proj_len()`` requires there.  The bounds a range excludes are refused,
    each by its rule (:data:`MALFORMED`, :data:`TABLE_FAULTS`).
    """
    committed = _committed()
    copies = [committed.loc[[_label(committed, *row)]].assign(**changes, row_kind="copy")
              .set_axis([label]) for label, (row, changes) in AT_BOUNDS.items()]
    table = pd.concat([committed, *copies]).rename_axis("point_id")
    edits = _bounds_tables()
    model = _read(_sec_inputs(tmp_path / "bounds", table, edits), "bounds")
    try:
        assert list(model.Data.model_point_table().index) == list(table.index)
        for label in AT_BOUNDS:
            p = _point(model, label)
            assert np.isfinite(p.result_cf().to_numpy()).all(), label
            assert p.check_av_roll_fwd() and p.check_pols_roll_fwd(), label
            assert p.check_charge_split(), label
        p = _point(model, 201)
        assert (p.alloc(1), p.alloc(2), p.fund_expense_rate(1), p.fund_expense_rate(2),
                p.surr_charge_rate(0), p.surr_charge_rate(12)) == (0.0, 1.0, 0.0, 1.0,
                                                                   1.0, 0.0)
        p = _point(model, 202)
        assert (p.mort_rate(0), p.mort_rate(12), p.pols_if(24)) == (0.0, 1.0, 0.0)
        p = _point(model, 203)
        first = [t for t in range(p.proj_len()) if p.is_first_wd(t)]
        assert first and p.gawa_pct_fixed(first[0]) == 1.0
        p = _point(model, 204)
        assert (p.inv_return_mth(0, 1), p.cmt10(0), p.vix_sq(1)) == (BOUND, BOUND, 0.0)
        p = _point(model, 205)
        assert (p.gawa_pct_fixed(0), p.gmdb_factor_acc(0)) == (1.0, 0.0)
        p = _point(model, 206)
        assert (p.premium_pp(0), p.wd_intensity(), p.premium_taxes(0)) == (0.0, 0.0, 0.0)
        p = _point(model, 208)
        assert (p.sa_pp_init(1), p.av_pp_init(), p.depleted_open(0)) == (-0.01, -0.01,
                                                                         True)
    finally:
        model.close()
    vix = _label(committed, "derived", 6, 41)
    early = committed.loc[[vix]].assign(duration_mth=3, rb_pp_prev_anniv_init=100000.0,
                                        phi_glwb_init=1.0, row_kind="copy").set_axis([207])
    model = _read(_sec_inputs(tmp_path / "fee", pd.concat([committed, early])
                              .rename_axis("point_id")), "bounds_fee",
                  {"phi_glwb_curr": 1.0})
    try:
        p = _point(model, 207)
        assert p.phi_glwb_init() == 1.0 and p.phi_glwb_vix(1) == 1.0
        assert np.isfinite(p.result_cf().to_numpy()).all()
    finally:
        model.close()


def test_an_extract_carried_to_the_cent_is_read(tmp_path):
    """The opening state carried to the cent, as an extract carries it, is read.

    The committed table with each subaccount value and each of the twelve amounts of the
    opening state rounded to the cent (:data:`FUNDS`, :data:`MONEY`) reads, every point
    passes ``proj_len()``, and each enters its first month on the books depleted exactly
    where its committed row does.  The rules that hold one amount to another hold it to a
    cent, or tie two values of one instant, which round alike; each held to a cent is
    pinned from both sides elsewhere, two cents off refused (:data:`MALFORMED`) and a part
    of a cent off read (the edges test).
    """
    committed = _committed()
    table = committed.assign(**{c: committed[c].round(2) for c in (*FUNDS, *MONEY)})
    model = _read(_sec_inputs(tmp_path, table), "cents")
    base = _read(model_path(SEC), "cents_committed")
    try:
        assert list(model.Data.model_point_table().index) == list(committed.index)
        for label in committed.index:
            p, q = _point(model, label), _point(base, label)
            assert p.proj_len() == q.proj_len(), label
            assert p.depleted_open(p.t_entry()) == q.depleted_open(q.t_entry()), label
    finally:
        base.close()
        model.close()


def _with_withdrawal(table, programme, name, month, amount):
    """The programmes with ``programme``'s rows copied under ``name``, a withdrawal of
    ``amount`` added at policy month ``month``, for a test."""
    rows = table[table["txn_id"] == programme].assign(txn_id=name)
    extra = pd.DataFrame([(name, month, 0.0, amount, "a test")], columns=table.columns)
    return pd.concat([table, rows, extra], ignore_index=True)


# The year to date with nothing in it, which a test's paired baseline takes.
EMPTY_YEAR = {"sum_wd_pp_ytd_init": 0.0, "free_wd_used_cum_pp_ytd_init": 0.0,
              "gmdb_dfd_acc_pp_ytd_init": 0.0, "gmdb_factor_acc_ytd_init": 1.0}

# Each opening-state column and the committed row that reads it, as (row, the changes, the
# baseline's own changes, the programme): the row copied twice, once with the baseline's
# changes and once with both, so that a column Data ties to another is moved against a
# baseline that differs in it alone; and, where S's points never read the column, a
# withdrawal later in the year under way, under a programme of the test's own, which the
# copies run on.  The rows: 2, S's in-force point at 26; 11, the anchor at its first
# withdrawal, 120, here on a grid of 0% from 60 to 64, at which a withdrawal status of True
# with no GAWA% locked is a state the contract can be in; 12, the anchor after its first
# withdrawal, 131; 15, the excess programme after its excess withdrawal, 65, whose year
# reads its year to date, its locked GAWA% and its remaining premium in every withdrawal
# charge and benefit test of the year; 16, the highest quarterly step-up at 40; 17, the VIX
# fee at 41; 18, the never-withdrawing roll-up depleted at 560; 20, S's in-force point
# restated at 40, in the Bonus Period; 21, the basic death benefit after its first
# withdrawal, 125; and 22, the never-withdrawing basic death benefit at 100, before its
# GWB Adjustment Date.
SHOWS = {
    "policy_count": (2, {"policy_count": 2.5}, {}, None),
    "sa_pp_init_1": (2, {"sa_pp_init_1": 67000.0}, {}, None),
    "sa_pp_init_2": (2, {"sa_pp_init_2": 45000.0}, {}, None),
    "gwb_pp_init": (2, {"gwb_pp_init": 113500.0}, {}, None),
    "gawa_pp_init": (12, {"gawa_pp_init": 9673.75}, {}, None),
    "gawa_pct_init": (15, {"gawa_pct_init": 0.0565}, {}, None),
    "bb_pp_init": (2, {"bb_pp_init": 113500.0}, {}, None),
    "rb_pp_init": (2, {"rb_pp_init": 113360.0}, {}, None),
    "np_pp_init": (2, {"np_pp_init": 200000.0}, {}, None),
    "rp_pp_init": (15, {"rp_pp_init": 100262.365944}, {}, None),
    "adj_pp_init": (22, {"adj_pp_init": 205000.0}, {}, None),
    "bonus_end_init": (20, {"bonus_end_init": 4}, {}, None),
    "has_wd_init": (11, {"has_wd_init": True},
                    {"adj_pp_init": 0.0, "glwb_option": "zero_mid"}, None),
    "sum_wd_pp_ytd_init": (21, {"sum_wd_pp_ytd_init": 9000.0}, {}, ("none", 126, 500.0)),
    "free_wd_used_cum_pp_ytd_init": (15, {"free_wd_used_cum_pp_ytd_init": 5000.0}, {},
                                     None),
    "gmdb_dfd_acc_pp_ytd_init": (15, {"gmdb_dfd_acc_pp_ytd_init": 7929.353466}, {}, None),
    "gmdb_factor_acc_ytd_init": (15, {"gmdb_factor_acc_ytd_init": 0.881908}, {}, None),
    "wd_this_year_init": (15, {"wd_this_year_init": False},
                          {**EMPTY_YEAR, "wd_this_year_init": True}, None),
    "rb_pp_prev_anniv_init": (15, {"rb_pp_prev_anniv_init": 134822.55776}, {},
                              ("excess", 67, 1000.0)),
    "stepup_base_pp_ytd_init": (16, {"stepup_base_pp_ytd_init": 130132.461102}, {}, None),
    "phi_glwb_init": (17, {"phi_glwb_init": 0.010}, {}, None),
}

# And the controls, each moving nothing: the GWB Adjustment on the excess programme's row
# at its excess withdrawal, which voids it at t = 0; and the year's withdrawals and the
# year-open roll-up base each without the later withdrawal of the year that reads them.
CONTROLS = {
    "adj_pp_init on a row that withdraws at t = 0": (14, {"adj_pp_init": 0.0}, {}, None),
    "sum_wd_pp_ytd_init with no withdrawal later that year": (
        21, {"sum_wd_pp_ytd_init": 9000.0}, {}, None),
    "rb_pp_prev_anniv_init with no withdrawal later that year": (
        15, {"rb_pp_prev_anniv_init": 134822.55776}, {}, None),
}


# The months from t = 0 a pair is compared over, and the cells: every column shows within
# its row's first five years, the GWB Adjustment Date of the never-withdrawing basic death
# benefit at t = 43 the latest, and the rest of a frame costs time and shows nothing more;
# the cells are the net cash flow, the count, the account value, the withdrawal and the
# guarantee bases a report shows.
SHOW_MONTHS = 60
SHOWN = ("net_cf", "pols_if", "av_pp", "wd_pp", "gwb_pp", "gawa_pp", "bb_pp", "rb_pp",
         "db_pp")


def _moved(base, changed):
    """The cells of :data:`SHOWN` in which ``changed`` departs from ``base`` in some month
    of its first :data:`SHOW_MONTHS`."""
    months = range(min(SHOW_MONTHS, base.proj_len()))
    return [cell for cell in SHOWN
            if any(abs(base.cells[cell](t) - changed.cells[cell](t))
                   > 1e-9 * (abs(base.cells[cell](t)) + 1.0) for t in months)]


def test_each_opening_state_column_shows_on_a_committed_row(tmp_path):
    """Each column, changed, changes what its committed row reports, where it is read.

    A column the projection never read, or read where another belongs, would pass every test
    that leaves the column as generated.  So each of :data:`SHOWS`, ``policy_count`` and the
    twenty opening-state columns, is changed on a copy of a committed row that reads it,
    against a baseline copy that differs from it in that column alone, each pair appended to
    the committed table under ids of its own, all in one read: then a cash flow, the count,
    the account value, the withdrawal or a guarantee base of the copy differs from the
    baseline's in some month of its first five years (:data:`SHOWN`, :data:`SHOW_MONTHS`),
    each a column of a report.  The baseline is the committed row, but where ``Data`` ties
    the column to another: the withdrawal status, whose rules void the GWB Adjustment and
    lock a GAWA%, and with it a GAWA, unless the grid gave 0%, on the anchor at its first
    withdrawal, 120, on a grid of the test's own that gives 0% from 60 to 64, where the
    status says whether the month's withdrawal is the first, which locks the grid's 5% of
    attained age 70, or one on a GAWA locked at 0, which takes nothing; and the year flag,
    against an empty year to date.  The year's withdrawals and
    the year-open roll-up base are read only by a withdrawal later in the same contract
    year, which no S point takes, so each pair runs on a programme of the test's own that
    withdraws then.  The depleted contract that never withdrew shows the status too, in
    ``has_wd_by(0)``, though no cash flow of an exhausted account reads it.  And each of
    :data:`CONTROLS` moves none of them: the GWB Adjustment voided by a withdrawal at the
    valuation month, and the two columns without the withdrawal that reads them.
    """
    committed = _committed()
    cases = {**SHOWS, **CONTROLS}
    labels, rows = {}, []
    programmes = pd.read_csv(model_path(SEC).parent / "transaction_table.csv")
    for n, (what, (row, changes, baseline, wd)) in enumerate(cases.items()):
        txn = {}
        if wd is not None:
            name = f"{wd[0]}_test_{n}"
            programmes = _with_withdrawal(programmes, wd[0], name, wd[1], wd[2])
            txn = {"txn_id": name}
        labels[what] = (101 + 2 * n, 102 + 2 * n)
        rows.append(committed.loc[[row]].assign(**{**baseline, **txn}).set_axis(
            [labels[what][0]]))
        rows.append(committed.loc[[row]].assign(**{**baseline, **txn, **changes}).set_axis(
            [labels[what][1]]))
    table = pd.concat([committed, *rows]).rename_axis("point_id")
    model = _read(_sec_inputs(tmp_path, table, {"transaction_table.csv": programmes,
                                                "gawa_pct_table.csv": _zero_band}), "shown")
    try:
        assert set(SHOWS) == {"policy_count", *STATE}
        still, moved = [], []
        for what in cases:
            base, changed = (_point(model, label) for label in labels[what])
            found = _moved(base, changed)
            if what in SHOWS and not found:
                still.append(what)
            if what in CONTROLS and found:
                moved.append((what, found))
            for label in labels[what]:
                _release(model, _key(model, label))
        assert not still, f"columns that move nothing: {still}"
        assert not moved, f"controls that move something: {moved}"
        never = _point(model, 18)
        assert never.depleted_open(0) and never.has_wd_by(0) is False
    finally:
        model.close()
    flagged = _read_edited(tmp_path / "flagged", _set("has_wd_init", [18], True), "flagged")
    try:
        assert _point(flagged, 18).has_wd_by(0) is True
    finally:
        flagged.close()


def test_run_sec_says_one_month_where_a_point_is_a_month_from_the_valuation_date(tmp_path):
    """The runner writes "1 month", not "1 months", on both sides of the valuation date.

    No committed point is in force one month or issued one month on, so the runner is run,
    with ``--block``, beside a table of two: the anchor's first-year row moved back to
    policy month 1, its first-year state as ``Data`` requires it, and the anchor issued a
    month on, reading S's own scenarios, which set their levels from ``t = 0``.  Each block
    line is asserted whole.
    """
    committed = _committed()
    first, future = _label(committed, "derived", 1, 6), _label(committed, "future", 1, -15)
    table = _both(_cells(first, duration_mth=1, stepup_base_pp_ytd_init=0.0),
                  _cells(future, duration_mth=-1, scenario_id="base"))(committed)
    folder = _sec_inputs(tmp_path, table.loc[[first, future]])
    runner = folder.parent / "run_sec.py"
    shutil.copy(model_path(SEC).parent / "run_sec.py", runner)
    out = _run_sec(runner, "--block").splitlines()
    count, av = committed.at[first, "policy_count"], (
        committed.at[first, "sa_pp_init_1"] + committed.at[first, "sa_pp_init_2"])
    assert out[:3] == [
        "model points, t = 0 the valuation date for each:",
        f"  {first:>2}  VA-000001-M6     in force 1 month: contract year 1, attained age "
        f"60, {count:.6f} in force, AV {av:,.2f} per contract; proj_len 719",
        f"  {future:>2}  VA-000001-F15    to be issued at t = 1, 1 month after the "
        f"valuation date; proj_len 721"]


# ---------------------------------------------------------------------------
# The committed models
#
# From here on every test reads the committed models, each read and swept once (sec_read,
# s_model), and none reads another model beside them but the extract's, which projects
# five rows, and the runner's, each in an interpreter of its own.


# ---------------------------------------------------------------------------
# D3's closed-form clock, and R2's recursions on the committed model


def test_the_policy_clock_is_a_closed_form_and_no_recursion_runs_backward(sec_read):
    """D3 and R2's recursions, on the committed model as it was first swept, cold.

    Both need a model on which nothing had been evaluated yet, which is what the fixture
    held when it made the record asserted here:

    * D3: the policy clock is the closed form.  Called first, ``duration_mth(400)``
      evaluates ``duration_mth`` once, where ``BasicTerm_SE``'s recursion would evaluate
      it at all 401 months from 0.  And on every committed point, at every month of its
      frame, ``duration_mth(t)`` is ``duration_mth_init() + t``, ``anniv_mth(t)`` is the
      month whose policy month closes the contract year of ``t``, and ``year_open_mth(t)``
      the month before that year's first, twelve months earlier: both months of the
      frame, on the valuation clock, before the valuation date where the year opened
      before it.
    * R2's recursions run forward: under modelx's recursion limit lowered to
      :data:`CALL_DEPTH`, every committed point is swept, each column in ascending ``t``.
      A forward recursion, through ``t - 1``, finds the month before already cached and
      stays shallow; the GAWA's chain, first read deep in the frame on a contract that
      never withdraws, takes the sweep to 569, which is what sets the limit.  A backward
      recursion over the frame, through ``t + 1``, keeps every step within the look-ahead
      but opens a chain as long as the frame, which a compiled model would run on the C
      stack (F7), and fails here, on every committed frame but the nine listed below,
      those no longer than ``CALL_DEPTH + 60`` months.
    """
    model, record = sec_read
    assert record["duration_mth(400)"] == 400
    assert record["keys"] == [400]
    assert not record["deep"], f"under a recursion limit of {CALL_DEPTH}: {record['deep']}"
    table = model.Data.model_point_table()
    short = []
    for key, point_id in zip(point_keys(model), table.index):
        p = projection(model, key)
        d0 = p.duration_mth_init()
        assert d0 == table.at[point_id, "duration_mth"]
        for t in range(p.proj_len()):
            year = p.duration(t)
            assert p.duration_mth(t) == d0 + t, (point_id, t)
            assert p.duration_mth(p.anniv_mth(t)) == 12 * year + 11, (point_id, t)
            assert t <= p.anniv_mth(t) <= t + 11, (point_id, t)
            assert p.year_open_mth(t) == p.anniv_mth(t) - 12, (point_id, t)
            assert p.duration_mth(p.year_open_mth(t) + 1) == 12 * year, (point_id, t)
        if p.proj_len() <= CALL_DEPTH + 60:
            short.append(point_id)
    assert short == [_label(table, "derived", s_point, month) for s_point, month in (
        (1, 120), (1, 131), (3, 144), (4, 60), (4, 65), (8, 560), (7, 719), (9, 125),
        (7, 100))], short


# ---------------------------------------------------------------------------
# T4 -- the count algebra
#
# BEF_DECR == BEF_NB + pols_new_biz, at every t of every point, is a convention
# (test_new_business_joins_the_count_before_decrements), and is not repeated here.


def test_the_count_rolls_forward_through_new_business_and_decrements(sec_model):
    """The count leaves month t by its deaths, surrenders and deemed maturities alone.

    On every committed point and at every ``t`` of its frame, the count weighting month
    ``t``, ``pols_if_at(t, "BEF_DECR")``, less the count carried into ``t + 1``,
    ``pols_if_at(t + 1, "BEF_NB")``, is the three outflows of month ``t``, to 1e-12.  The
    step from the last row to ``t = proj_len()`` is what catches cover that runs a month
    too long: the maturities would then leave a month late, and the count would carry
    over.  And the count leaving the month, ``pols_if_at(t, "AFT_DECR")``, is exactly the
    count carried into the next month before its new business, in every month but the
    last covered one, where it is what the deemed maturity takes out and the next month
    opens empty: the two are one product in one order.

    ``result_pols()`` sets the same movement out row by row, in :data:`RESULT_POLS`'s
    columns, indexed by ``t`` over the frame: ``pols_if`` at ``t + 1`` is ``pols_if`` less
    the outflows at ``t``, plus the new business of ``t + 1``, and row 0 opens from
    ``pols_if_init()``.  A timing the model does not have, ``basiclife.BasicTerm_SE``'s
    ``"BEF_MAT"``, which a formula ported from it might ask for, is refused rather than
    answered with another count.
    """
    bef_nb, bef_decr, aft_decr = (_code(sec_model.Projection, label)
                                  for label in ("BEF_NB", "BEF_DECR", "AFT_DECR"))
    table = sec_model.Data.model_point_table()
    for key, point_id in zip(point_keys(sec_model), table.index):
        p = projection(sec_model, key)
        last = p.proj_len() - 1
        for t in range(p.proj_len()):
            out = p.pols_death(t) + p.pols_lapse(t) + p.pols_maturity(t)
            moved = p.pols_if_at(t, bef_decr) - p.pols_if_at(t + 1, bef_nb)
            assert moved == pytest.approx(out, abs=1e-12), (point_id, t)
            if t < last:
                assert p.pols_if_at(t, aft_decr) == p.pols_if_at(t + 1, bef_nb), (
                    point_id, t)
                assert p.pols_maturity(t) == 0.0, (point_id, t)
        assert p.pols_maturity(last) == p.pols_if_at(last, aft_decr), point_id
        assert p.pols_if_at(last + 1, bef_nb) == 0.0, point_id
        pols = p.result_pols()
        assert list(pols.columns) == RESULT_POLS, point_id
        assert pols.index.name == "t" and list(pols.index) == list(range(p.proj_len()))
        carried = (pols["pols_if"] - pols[OUTFLOWS].sum(axis=1)).shift(1)
        expected = carried.fillna(p.pols_if_init()) + pols["pols_new_biz"]
        assert ((pols["pols_if"] - expected).abs() <= 1e-12).all(), point_id
    twin = _row(sec_model, "twin", 2, 0)
    _refused(lambda: twin.pols_if_at(0, _code(twin, "BEF_MAT")), "invalid timing")


def test_result_pols_is_s_report_with_the_new_business_beside_it(sec_model, s_model):
    """``result_pols()`` is S's, column for column, with ``pols_new_biz`` second (D5).

    T1 skips the report as a whole, because its frame has a column S's lacks (the spec's
    exempt), so it is compared here, on every twin: the eight issued at the valuation date
    and S's point 2, in force at 26, each row for row from its ``t = 0``, which is S's.
    Every column S's report has agrees, to 1e-9 relative with no absolute floor, frames
    ending together, and ``pols_new_biz`` holds the count in the issue month and 0 in every
    other, so on the twin in force, 0 throughout.
    """
    table = sec_model.Data.model_point_table()
    twins = table.index[table["row_kind"] == "twin"].tolist()
    assert twins == sorted(s_model.Data.model_point_table().index)
    for point_id in twins:
        p = _point(sec_model, point_id)
        month = int(table.at[point_id, "source_mth"])
        assert month == 0, point_id
        mine, theirs = p.result_pols(), _point(s_model, point_id).result_pols()
        assert list(mine.columns) == [theirs.columns[0], "pols_new_biz",
                                      *theirs.columns[1:]], point_id
        assert frame_mismatches(theirs, mine, t_offset=month, atol=0.0) == [], point_id
        issue = -p.duration_mth_init()
        assert list(mine["pols_new_biz"]) == [
            p.policy_count() if t == issue else 0.0 for t in mine.index], point_id


# ---------------------------------------------------------------------------
# T6 -- regeneration


def test_the_committed_sec_tables_are_what_s_generates(s_model):
    """``model_point_table_sec.csv`` and its companions are what VA_US_S generates today.

    Every row and column, the text cells, the twenty opening-state columns and every
    re-based scenario included: an edit to an S row or an S scenario the files copy or
    derive from, or to an S formula a row's state is read from, fails here until
    ``python tools/gen_sec_points.py VA_US_SEC`` regenerates them, in the same commit.
    Text and integers compare exactly, and a float by its value, to 1e-12, because the text
    the writer picks for a computed float depends on the platform's parser (§5.2).
    """
    assert check_generated(SEC, s_model=s_model) == []


# The words the generator composes ids and provenance from, beside S's keys and a month:
# VA-000001-M6, VA-000001-F15, base-M26, "S point 1 (VA-000001) restated in force at S
# month 6", "... issued 15 months after the valuation date".  A word outside this set in a
# generated text cell is one the generator added, which CLAUDE.md forbids.
TEMPLATE_WORDS = {"M", "F", "S", "point", "restated", "in", "force", "at", "month",
                  "months", "issued", "after", "the", "valuation", "date"}


def _composed(value, keys):
    """Whether ``value`` is ``keys`` and :data:`TEMPLATE_WORDS` with punctuation, alone."""
    rest = value
    for key in sorted(keys, key=len, reverse=True):
        rest = rest.replace(key, " ")
    return set(re.findall(r"[A-Za-z]+", rest)) <= TEMPLATE_WORDS and not re.search(
        r"\d", rest)


def test_generated_text_is_s_text_or_composed_from_s_keys():
    """Every text cell of the three committed files is S's, or composed from S's keys (D8).

    ``CLAUDE.md`` holds every input file to naming no company or product, and the
    generator keeps to it by adding no word of its own.  So each text cell of
    ``model_point_table_sec.csv`` is its S row's text in the same column, or, with S's
    policy id, scenario id and point id and the row's months taken out, its S month and
    its policy month, nothing but the template's words and punctuation: an id, a re-based
    scenario's id or a provenance.  And each row of the two scenario companions is a level
    S's own scenario sets, its provenance S's for that level, under S's scenario id or one
    composed from it and the month of a row of the table that reads it.  The test holds no
    list of names: what it holds is the template, and a word outside it fails.
    """
    s_dir = model_path(TWIN).parent
    s_table = pd.read_csv(s_dir / "model_point_table.csv", index_col="point_id")
    s_rows = {row["policy_id"]: {**row, "point_id": point_id}
              for point_id, row in s_table.to_dict("index").items()}
    rename = {"pols_if_init": "policy_count", **SPEC.column_map}
    s_column = {new: old for old, new in rename.items() if new is not None}
    table = _committed().reset_index()
    foreign = []
    readers = {}
    for record in table.to_dict("records"):
        source = s_rows[record["source_policy_id"]]
        months = (str(abs(record["source_mth"])), str(abs(record["duration_mth"])))
        keys = (source["policy_id"], source["scenario_id"], *months,
                str(source["point_id"]))
        readers.setdefault(record["scenario_id"], (source["scenario_id"], months[1]))
        for column, value in record.items():
            if not isinstance(value, str):
                continue
            if column == "row_kind" and value in ("twin", "derived", "future"):
                continue
            if source.get(s_column.get(column, column)) == value:
                continue
            if not _composed(value, keys):
                foreign.append((TABLE, record["point_id"], column, value))
    for name, s_file, level in (
            (RETURNS, "return_scenario.csv", ("sub_id", "gross_return")),
            (RATES, "rate_scenario.csv", ("vix_sq", "cmt10"))):
        s_levels = pd.read_csv(s_dir / s_file)
        said = {(r["scenario_id"], *(r[c] for c in level)): r["provenance"]
                for r in s_levels.to_dict("records")}
        for record in _companion(name).to_dict("records"):
            scenario = record["scenario_id"]
            base, month = readers.get(scenario, (scenario, ""))
            if scenario != base and not _composed(scenario, (base, month)):
                foreign.append((name, scenario, "scenario_id", scenario))
            key = (base, *(record[c] for c in level))
            if said.get(key) != record["provenance"]:
                foreign.append((name, scenario, "provenance", record["provenance"]))
    assert not foreign, f"text the generator did not take from S: {foreign}"


# ---------------------------------------------------------------------------
# The product's own facts


def test_the_opening_state_is_what_s_carries_into_the_valuation_month(sec_read, s_model):
    """Each committed in-force row opens with S's state at its month, and continues S.

    For each derived row, restated from S point ``p`` at its S month ``d``, for the twin of
    S's point 2, in force at 26, and for the anchor issued 15 months on, each of the twenty
    opening-state columns is what the spec's extractor reads off S at ``d``, the subaccount
    values' among them, which the spec builds from S's fund table, to 1e-12 relative,
    because a computed float may come back from the CSV within two ulps, and the row's
    scenario is the extractor's, S's re-based to its policy month.  Then the row is
    S's point from month ``d`` on, at the shipped assumptions, in every cell but those
    expense inflation moves (:func:`_continues_s`), with T2's exemptions, or T3's on the
    row issued later: the committed rows themselves are splices, on the shipped inputs and
    the committed companions, as T2's rows are on the splice's (§7.1, *Precised at M3*,
    item 11).  And the side of the GWB Adjustment's floor that keeps the GWB, which the
    splice's 200% puts out of reach, binds on one of these rows, the never-withdrawing
    basic death benefit before its Adjustment Date (:data:`BOUND_ELSEWHERE`), as the
    committed points' sweep recorded it.
    """
    sec_model, record = sec_read
    table = sec_model.Data.model_point_table()
    rows = table[(table["row_kind"] != "twin") | (table["duration_mth"] > 0)]
    assert sorted(rows["row_kind"].value_counts().items()) == [
        ("derived", 13), ("future", 1), ("twin", 1)]
    s_table = s_model.Data.model_point_table()
    s_of = {policy: point_id for point_id, policy in s_table["policy_id"].items()}
    extractors = {**SPEC.model_state(s_model), **SPEC.state}
    assert set(extractors) >= set(FUNDS)
    for point_id, row in rows.iterrows():
        s, d = _point(s_model, s_of[row["source_policy_id"]]), int(row["source_mth"])
        p = _point(sec_model, point_id)
        for column, extract in extractors.items():
            value = extract(s, max(d, 0))
            if row["row_kind"] == "future":
                continue
            if isinstance(value, str):
                assert p.scenario_id() == value, point_id
            elif column in FUNDS:
                i = int(column.rsplit("_", 1)[1])
                assert p.sa_pp_init(i) == pytest.approx(value, rel=1e-12, abs=1e-12), (
                    point_id, column)
            else:
                assert p.cells[column]() == pytest.approx(value, rel=1e-12, abs=1e-12), (
                    point_id, column)
        future = row["row_kind"] == "future"
        exempt = FUTURE_EXEMPT if future else SPLICE_EXEMPT
        found = _continues_s(s, p, d, exempt, s_in_force=row["row_kind"] == "twin")
        assert not found, f"point {point_id}: " + "\n  ".join(found[:20])
    mine = [side for side, test in BOUND_ELSEWHERE.items()
            if test == "test_the_opening_state_is_what_s_carries_into_the_valuation_month"]
    for side in mine:
        assert any(side in record["bounds"][point_id] for point_id in rows.index), side
    assert mine


def test_the_year_under_way_reads_its_opening_state(sec_model):
    """The quantities of the contract year under way are its columns, then the frame's.

    A year-to-date quantity is read three ways: from its column where the year opened
    before the valuation date, from the frame where it opened on the books, and empty at
    a contract year's start.  The anchor in the last month of its first withdrawal's year,
    131, adds the month's withdrawal to the year's, and reads its free allowance used, its
    dollar-for-dollar reduction and its proportional factor from their columns.  The
    excess programme after its excess withdrawal, 65, takes no withdrawal on the books in
    that year, and its year flag alone says the year has one.  The highest quarterly
    step-up at 40 takes, at the anniversary closing its year, the largest of the column
    and the account values at the year's quarter ends on the books.  The VIX fee at 41
    clips its first quarter's raw rate on the books against the column's prior.  The
    anchor in its first policy year, 6, reads its year-open roll-up base from the column,
    and from the next year on from the frame.  The anchor at its first withdrawal, 120, a
    contract year's start, opens every year-to-date value empty.  And the anchor issued 15
    months on opens its first year, in its issue month, on the issue rule: an empty year
    to date, and the year-open roll-up base after the issue month's premium.
    """
    p = _row(sec_model, "derived", 1, 131)
    assert p.sum_wd_pp(0) == p.sum_wd_pp_ytd_init() + p.wd_pp(0) > 0.0
    assert p.free_wd_avail(0) == max(0.0, p.free_wd_allow(0)
                                     - p.free_wd_used_cum_pp_ytd_init())
    assert p.gmdb_dfd_acc_pp(0) == p.gmdb_dfd_acc_pp_ytd_init() + p.gmdb_wd_dfd_pp(0) > 0.0
    assert p.gmdb_factor_acc(0) == p.gmdb_factor_acc_ytd_init() * p.gmdb_wd_factor(0)
    assert p.sum_wd_pp(1) == p.wd_pp(1) and p.is_year_start(1)
    p = _row(sec_model, "derived", 4, 65)
    year = range(p.anniv_mth(0) + 1)
    assert p.wd_this_year_init() and not any(p.is_wd_taken(t) for t in year)
    assert all(p.is_wd_year(t) for t in year) and not p.is_wd_year(p.anniv_mth(0) + 12)
    p = _row(sec_model, "derived", 5, 40)
    a = p.anniv_mth(0)
    assert p.is_anniv(a) and p.stepup_base_pp(a) == max(
        p.stepup_base_pp_ytd_init(), *(p.av_pp(u) for u in (a, a - 3, a - 6) if u >= 0))
    p = _row(sec_model, "derived", 6, 41)
    k = p.contract_quarter(0)
    assert p.phi_glwb_vix(k) == p.fee_rate_vix_clip(
        p.phi_glwb_init(), p.fee_rate_vix_raw(p.phi_glwb_curr, p.vix_sq(k)))
    assert p.phi_glwb_vix(k + 1) == p.fee_rate_vix_clip(
        p.phi_glwb_vix(k), p.fee_rate_vix_raw(p.phi_glwb_curr, p.vix_sq(k + 1)))
    p = _row(sec_model, "derived", 1, 6)
    assert [p.rb_prior_anniv_pp(t) for t in range(6)] == [p.rb_pp_prev_anniv_init()] * 6
    assert p.rb_prior_anniv_pp(6) == p.rb_pp(5) and p.year_open_mth(6) == 5
    p = _row(sec_model, "derived", 1, 120)
    assert p.is_year_start(0) and p.wd_pp(0) > 0.0
    assert (p.sum_wd_pp(0), p.free_wd_used_cum_pp(0), p.gmdb_dfd_acc_pp(0),
            p.gmdb_factor_acc(0)) == (p.wd_pp(0), p.wd_free_pp(0), p.gmdb_wd_dfd_pp(0),
                                      p.gmdb_wd_factor(0))
    assert p.rb_prior_anniv_pp(0) == p.rb_pp_prev_anniv_init() == p.rb_pp_init()
    p = _row(sec_model, "future", 1, -15)
    assert (p.sum_wd_pp(15), p.gmdb_factor_acc(15)) == (0.0, 1.0)
    assert p.rb_prior_anniv_pp(15) == _at(p, "rb_pp_at", 15, "BEF_WD") == 100000.0


def test_the_worked_example_holds_on_the_valuation_clock(sec_model):
    """S's goldens hold on twin 1 at ``t = 26`` and on twin 2 at ``t = 0``, as in S.

    ``test_variable_annuity_us.py`` asserts the worked example twice, on S's point 1,
    issued at its ``t = 0``, at the 27th policy month, ``t = 26``, and on S's point 2,
    which enters the carried state in force at 26, at ``t = 0``.  On this model both
    readings fall at the same months, twin 2 reading its scenarios re-based by 26 months,
    ``base-M26``, whose returns at ``t = 0`` are ``base``'s at policy month 26, +1.20% and
    -0.30%.  So the six printed steps, the memo lines, the GMDB test and the carried bases
    are asserted here on both twins against S's own goldens, ``WORKED_EXAMPLE`` and
    ``CARRIED_STATE``, read from that module with its tolerances, none restated.
    """
    g, c = s_tests.WORKED_EXAMPLE, s_tests.CARRIED_STATE
    cent, weight, factor, ratio = (s_tests.CENT, s_tests.WEIGHT, s_tests.FACTOR,
                                   s_tests.RATIO)
    for case, t in ((("twin", 1, 0), 26), (("twin", 2, 0), 0)):
        p = _row(sec_model, *case)
        assert p.t_of_month(26) == t and p.duration_mth(t) == 26, case
        assert (p.inv_return_mth(t, 1), p.inv_return_mth(t, 2)) == (0.0120, -0.0030), case
        for i, name in ((1, "sa1"), (2, "sa2")):
            assert p.sa_pp_at(t, i, _code(p, "BEF_PREM")) == pytest.approx(
                g[f"{name}_bom"], abs=cent), case
            assert p.sa_pp_at(t, i, _code(p, "BEF_FEE")) == pytest.approx(
                g[f"{name}_aft_growth"], abs=cent), case
            assert p.sa_pp(t, i) == pytest.approx(g[f"{name}_eom"], abs=cent), case
            assert p.unit_growth(t, i) == pytest.approx(g[f"growth_{i}"], abs=factor), case
            assert p.sa_weight(t, i) == pytest.approx(g[f"weight_{i}"], abs=weight), case
        assert _at(p, "av_pp_at", t, "BEF_PREM") == pytest.approx(g["av_bom"], abs=cent)
        assert _at(p, "av_pp_at", t, "BEF_INV") == pytest.approx(g["av_bom"], abs=cent)
        assert _at(p, "av_pp_at", t, "BEF_FEE") == pytest.approx(g["av_aft_growth"],
                                                                 abs=cent)
        assert (p.premium_pp(t), p.wd_pp(t)) == (0.0, 0.0), case
        assert p.is_quarterly_anniv(t) is True and p.contract_quarter(t) == 9, case
        for cell, key in (("fee_glwb_pp", "fee_glwb"), ("fee_gmdb_pp", "fee_gmdb"),
                          ("charge_pp", "fee_total"), ("maint_fee_pp", "maint_fee"),
                          ("av_pp", "av_eom"), ("asset_charge_pp", "asset_charge"),
                          ("fund_expense_pp", "fund_expense"),
                          ("charge_income_pp", "charge_income"), ("db_pp", "db"),
                          ("gmdb_claim_pp", "gmdb_claim"), ("free_wd_allow", "free_wd")):
            assert p.cells[cell](t) == pytest.approx(g[key], abs=cent), (case, cell)
        for i in (1, 2):
            assert p.sa_pp(t, i) - p.sa_pp_at(t, i, _code(p, "BEF_FEE")) == pytest.approx(
                g[f"fee_sa{i}"], abs=cent), case
        assert p.moneyness_glwb(t) == pytest.approx(g["moneyness_glwb"], abs=ratio)
        assert p.moneyness_gmdb(t) == pytest.approx(g["moneyness_gmdb"], abs=ratio)
        assert p.lapse_dyn_mult(t) == pytest.approx(g["lapse_mult"], abs=1e-9)
        assert p.lapse_rate(t) == pytest.approx(g["lapse_base_ann"], abs=1e-12)
        assert p.lapse_rate_mth(t) == pytest.approx(g["lapse_mth"], abs=5e-7)
        assert p.duration(t) == g["cdsc_years"]
        assert p.surr_charge_rate(t) == pytest.approx(g["cdsc_rate"], abs=1e-12)
        assert p.av_pp(t) - p.rp_pp(t) == pytest.approx(g["earnings"], abs=cent)
        assert p.age(t) == 62 and p.gawa_pct_at_age(62) == pytest.approx(g["gawa_pct"],
                                                                        abs=1e-12)
        assert p.gawa_pct_fixed(t) == 0.0 and p.gawa_pp(t) == 0.0
        assert p.gawa_pct_at_age(62) * p.gwb_pp(t) == pytest.approx(
            g["gawa_if_taken_now"], abs=cent)
        assert _at(p, "gwb_pp_at", t, "BEF_ANNIV") == pytest.approx(c["gwb_anniv_2"],
                                                                    abs=cent)
        assert p.bb_pp_bef_anniv(t) == pytest.approx(c["bb_anniv_2"], abs=cent)
        assert _at(p, "rb_pp_at", t, "BEF_ANNIV") == pytest.approx(c["rb_anniv_2"],
                                                                   abs=cent)
        assert (p.np_pp(t), p.rp_pp(t)) == pytest.approx((c["np"], c["rp"]), abs=cent)
        assert p.adj_pp(t) == pytest.approx(c["adj"], abs=cent)
        assert p.bonus_end(t) == c["bonus_end_anniv_2"] and p.has_wd_by(t) is False
    assert _row(sec_model, "twin", 2, 0).scenario_id() == "base-M26"


def test_depletion_is_derived_from_the_opening_account_value(sec_model):
    """A contract in force enters month 0 depleted exactly where its account value is out.

    ``depleted_flag`` is absorbing, and from the month after it is set every subaccount is
    held at 0, so a contract enters a month depleted exactly where its account value
    entering the month, the sum of its subaccount columns, is at or below
    ``av_depletion_threshold``; new business, whose opening account value is 0, never does
    (§7.11, *Carried into VA (M9)*, *Depletion*).  So on every committed row
    ``depleted_open(t_entry())`` is that test, and it takes no column.  The decline path
    valued at 144 and the never-withdrawing roll-up at 560 open depleted.  The second
    never withdrew: its ``has_wd_init`` is False while its GAWA% is locked at 6.2%, by its
    depletion, where ``VA_US_S``'s inference from the GAWA%, ``gawa_pct_init() > 0``,
    would say it had withdrawn, which is why the status is a column.
    """
    table = sec_model.Data.model_point_table()
    opened = []
    for key, point_id in zip(point_keys(sec_model), table.index):
        p = projection(sec_model, key)
        entry = p.t_entry()
        want = p.duration_mth_init() > 0 and p.av_pp_init() <= p.av_depletion_threshold
        assert p.depleted_open(entry) is want, point_id
        assert p.av_pp_init() == sum(p.sa_pp_init(i) for i in p.sub_ids()), point_id
        if want:
            opened.append(point_id)
    assert opened == [_label(table, "derived", 3, 144), _label(table, "derived", 8, 560)]
    never = _row(sec_model, "derived", 8, 560)
    assert never.has_wd_init() is False and never.gawa_pct_init() == 0.062
    assert never.gawa_pct_init() > 0.0


def _s_levels(table, column, by):
    """``{key: (months, levels)}``, the months ascending, of S's scenario table ``table``:
    each scenario's, or each scenario's subaccount's, ``column`` by its policy months."""
    out = {}
    for key, rows in table.groupby(by):
        rows = rows.sort_values("t")
        out[key] = (rows["t"].tolist(), rows[column].tolist())
    return out


def _in_force(levels, key, month):
    """The level ``levels`` sets in force for ``key`` at policy month ``month``: its last
    row at or before it."""
    months, values = levels[key]
    return float(values[bisect.bisect_right(months, month) - 1])


def test_the_scenarios_run_on_the_valuation_clock(sec_model):
    """The returns and the rates are read at the valuation month (D7).

    ``VA_US_S`` keys its scenarios by the elapsed policy month; this model reads them at
    ``t`` from the companions, where each row's paths are S's re-based to its own
    ``duration_mth``.  So on every committed row, at every month of its frame, each
    subaccount's return is the one S's scenario sets in force at the row's policy month
    then, ``duration_mth(t)``, and on the rows the VIX fee or the CMT roll-up reads the
    rates for, both rates likewise.  S's point 2 is in force at 26 and S projects it from
    the valuation date, so its twin's copy moves by 26, ``base-M26``, though the twin's
    ``source_mth`` is 0; and the row restated from it at its S month 14 moves by 40, its
    copy ``base-M40``, the copy the highest quarterly step-up's row at 40 reads too: rows
    moved alike share one.  The anchor issued 15 months on reads ``base-F15``, whose paths
    set nothing before its issue month.
    """
    s_dir = model_path(TWIN).parent
    returns = _s_levels(pd.read_csv(s_dir / "return_scenario.csv"), "gross_return",
                        ["scenario_id", "sub_id"])
    rates = {name: _s_levels(pd.read_csv(s_dir / "rate_scenario.csv"), name, "scenario_id")
             for name in ("vix_sq", "cmt10")}
    s_ids = dict(zip(*pd.read_csv(s_dir / "model_point_table.csv")[
        ["policy_id", "scenario_id"]].T.to_numpy()))
    table = sec_model.Data.model_point_table()
    steps = sec_model.Data.return_scenario_steps()
    for key, point_id in zip(point_keys(sec_model), table.index):
        p = projection(sec_model, key)
        source = s_ids[table.at[point_id, "source_policy_id"]]
        rated = p.is_fee_reset_vix() or p.is_rollup_cmt_linked()
        for t in range(p.t_entry(), p.proj_len()):
            m = p.duration_mth(t)
            for i in p.sub_ids():
                assert p.inv_return_mth(t, i) == _in_force(returns, (source, i), m), (
                    point_id, t, i)
            if rated:
                for name in ("vix_sq", "cmt10"):
                    assert p.scenario_rate(t, name) == _in_force(rates[name], source, m), (
                        point_id, t, name)
        first = steps.loc[p.scenario_id()].index.get_level_values("t").min()
        assert first == p.t_entry(), point_id
    twin, restated, hq = (_row(sec_model, *case) for case in (
        ("twin", 2, 0), ("derived", 2, 14), ("derived", 5, 40)))
    assert (twin.scenario_id(), restated.scenario_id(), hq.scenario_id()) == (
        "base-M26", "base-M40", "base-M40")
    assert table.at[_label(table, "derived", 2, 14), "source_mth"] == 14
    assert _row(sec_model, "future", 1, -15).scenario_id() == "base-F15"


def test_transactions_stay_on_the_policy_clock(sec_model, tmp_path):
    """A programme's premium or withdrawal falls where the contract has it, however old.

    ``transaction_table.csv`` is keyed by the policy month (D7): the excess programme's
    withdrawal of 20,000 at policy month 60 and premium of 25,000 at 72 fall at ``t = 60``
    and ``t = 72`` on its twin, at ``t = 0`` and ``t = 12`` on its row valued at 60, and its
    premium alone at ``t = 7`` on its row valued at 65, the withdrawal having fallen before
    the valuation date.  The twin is also read issued 18 months on, from a copy of the
    table where it is a point of its own: there they fall at ``t = 78`` and ``t = 90``.
    """
    def scheduled(p):
        return [(t, p.wd_scheduled_pp(t), p.prem_scheduled_pp(t))
                for t in range(p.proj_len())
                if p.wd_scheduled_pp(t) != 0.0 or p.prem_scheduled_pp(t) != 0.0]

    def later(table):
        row = table.loc[[_label(table, "twin", 4, 0)]]
        row = row.assign(duration_mth=-18, scenario_id="base-F18", row_kind="copy")
        return pd.concat([table, row.set_axis([201])]).rename_axis("point_id")

    def moved(name):
        scenarios = _companion(name)
        base = scenarios[scenarios["scenario_id"] == "base"]
        return pd.concat([scenarios, base.assign(scenario_id="base-F18", t=base["t"] + 18)],
                         ignore_index=True)

    assert scheduled(_row(sec_model, "twin", 4, 0)) == [(60, 20000.0, 0.0),
                                                        (72, 0.0, 25000.0)]
    assert scheduled(_row(sec_model, "derived", 4, 60)) == [(0, 20000.0, 0.0),
                                                            (12, 0.0, 25000.0)]
    assert scheduled(_row(sec_model, "derived", 4, 65)) == [(7, 0.0, 25000.0)]
    assert scheduled(_row(sec_model, "twin", 1, 0)) == []
    model = _read(_sec_inputs(tmp_path, later(_committed()),
                              {RETURNS: moved(RETURNS), RATES: moved(RATES)}), "later")
    try:
        p = _point(model, 201)
        assert scheduled(p) == [(78, 20000.0, 0.0), (90, 0.0, 25000.0)]
        assert p.duration_mth(78) == 60 and p.wd_pp(78) == 20000.0
    finally:
        model.close()


def test_expense_inflation_runs_on_the_valuation_clock(sec_model, s_model):
    """Maintenance is in valuation-date dollars, for every point alike (D7).

    At the shipped 2.5%, on every committed point and in every month, the inflation factor
    is ``1.025 ** (valuation_year - expense_base_year + t // 12)``, eleven years at
    ``t = 0`` on every point, whatever the contract's age, and ``expenses(t)`` is the
    acquisition, 0 as shipped, plus the maintenance at that factor and the expense on the
    account value, per contract in force: ``VA_US_S``'s formula, on projection years.  S
    inflates by completed contract years instead (§7.7, D7), so S's point 2, in force at
    26, pays at its ``t = 0`` a maintenance term ``1.025 ** 2`` dearer than its twin's, and
    ``1.025 ** 3`` from its month 10, where its third contract year completes before the
    valuation date's first projection year does; on a twin issued at the valuation date
    the two clocks give S's expenses in every month.  This is the only test that sees
    inflation on the valuation clock: the splice sets the rate to 0.
    """
    assert sec_model.Projection.inflation_rate == INFLATION
    table = sec_model.Data.model_point_table()
    for key, point_id in zip(point_keys(sec_model), table.index):
        p = projection(sec_model, key)
        years = p.valuation_year - p.expense_base_year
        assert p.inflation_factor(0) == (1 + INFLATION) ** 11 == (
            1 + INFLATION) ** years, point_id
        for t in range(p.proj_len()):
            assert p.inflation_factor(t) == (1 + INFLATION) ** (years + t // 12)
            want = ((p.expense_maint / 12.0) * p.inflation_factor(t)
                    + (p.expense_av_rate / 12.0) * p.av_pp(t)) * p.pols_if(t)
            assert p.expenses(t) == pytest.approx(want, rel=1e-12, abs=1e-12), (
                point_id, t)
    s1, s2 = _point(s_model, 1), _point(s_model, 2)
    twin1, twin2 = _row(sec_model, "twin", 1, 0), _row(sec_model, "twin", 2, 0)
    assert [twin1.expenses(t) for t in range(720)] == [s1.expenses(t) for t in range(720)]
    for t in range(twin2.proj_len()):
        maint = (twin2.expense_maint / 12.0) * twin2.pols_if(t)
        theirs = s2.expenses(t) - (s2.expense_av_rate / 12.0) * s2.av_pp(t) * s2.pols_if(t)
        assert theirs == pytest.approx(maint * twin2.inflation_factor(t) * (
            1 + INFLATION) ** (s2.duration(t) - t // 12), rel=1e-12), t
    assert s2.duration(0) - 0 == 2 and s2.duration(10) - 10 // 12 == 3


def test_lapse_reads_the_withdrawal_year_at_its_anniversary(sec_model, s_model):
    """The lapse's withdrawal-year factor is the contract year's, read at its anniversary.

    ``lapse_wd_factor(t)`` reads whether the contract year of ``t`` has a withdrawal at the
    anniversary that closes it, ``is_wd_year(anniv_mth(t))``, up to 11 months ahead: R2's
    one admitted read, which ``VA_US_S`` makes as a scan of the year from ``t``.  So on
    every committed row, in every month in cover, the factor is ``lapse_wd_year_factor``
    exactly where the year closing at ``anniv_mth(t)`` has a withdrawal, and 1.0 elsewhere,
    one value over each contract year; and on each twin issued at the valuation date the
    year's answer at its anniversary is S's ``is_wd_year(t)`` in every month of the year.
    """
    table = sec_model.Data.model_point_table()
    for key, point_id in zip(point_keys(sec_model), table.index):
        p = projection(sec_model, key)
        for t in range(p.proj_len()):
            want = p.lapse_wd_year_factor if p.is_wd_year(p.anniv_mth(t)) else 1.0
            assert p.lapse_wd_factor(t) == want, (point_id, t)
            assert p.lapse_wd_factor(t) == p.lapse_wd_factor(min(p.anniv_mth(t),
                                                                 p.proj_len() - 1))
    for point_id in S_POINTS:
        p, s = _row(sec_model, "twin", point_id, 0), _point(s_model, point_id)
        assert [p.is_wd_year(p.anniv_mth(t)) for t in range(p.proj_len())] == [
            s.is_wd_year(t) for t in range(s.proj_len())], point_id


def test_a_depleted_row_projects_its_whole_frame_at_a_zero_account_value(sec_model):
    """In force with no account value and the rider live, the GLWB pays on (D6, M7).

    The decline path valued at 144, a contract year's start, and the never-withdrawing
    roll-up valued at 560 have exhausted their account values, so each opens depleted on an
    account value of 0, which ``Data`` accepts for a contract whose rider pays on.  Each
    frame runs to the end of cover, every number finite: every ratio over the account value,
    the moneyness and the subaccount weights among them, is guarded.  Each stays depleted,
    its account value 0, with no charge, no lapse and no surrender value; the GLWB pays its
    GAWA at each contract year's start, the first from the columns, at ``t = 0`` on the row
    valued at a year's start, ``gawa_pp_init()``, and every later one on the contracts still
    in force.
    """
    for case in (("derived", 3, 144), ("derived", 8, 560)):
        p = _row(sec_model, *case)
        assert p.av_pp_init() == 0.0 and p.depleted_open(0), case
        for report in REPORTS:
            frame = p.cells[report]().select_dtypes("number")
            assert np.isfinite(frame.to_numpy()).all(), (case, report)
        for t in range(p.proj_len()):
            assert p.depleted_flag(t) and p.av_pp(t) == 0.0, (case, t)
            assert (p.charge_pp(t), p.lapse_rate(t), p.surr_benefit_pp(t)) == (
                0.0, 0.0, 0.0), (case, t)
            paid = p.glwb_payment_pp(t)
            if p.is_year_start(t):
                gawa = p.gawa_pp(t - 1) if t > 0 else p.gawa_pp_init()
                gwb = p.gwb_pp(t - 1) if t > 0 else p.gwb_pp_init()
                want = gawa if p.forlife_flag() else min(gawa, gwb)
                assert paid == want > 0.0, (case, t)
            else:
                assert paid == 0.0, (case, t)
    row = _row(sec_model, "derived", 3, 144)
    assert row.glwb_payment_pp(0) == row.gawa_pp_init() == 9200.0


def test_each_keyed_reader_is_s_lookup_at_every_key(sec_model, s_model):
    """Each assumption table's readers return what S's own lookups return, key by key.

    ``Projection`` reads each table through one cell, but the fund table through three and
    the programme through two, each reading ``Data``'s checked copy.  ``VA_US_S`` has the
    same cells for the GAWA% grid and the fund table, and looks the mortality, the
    withdrawal charge and the programme up inside its monthly cells, where this model keys
    its readers by an age, a year count and a policy month, the keys Phase 2's caches are
    sized on.  At every key the contract can ask for, each returns what S's own lookup
    does: the GAWA% at every attained age from 0 to 125, against S's ``gawa_pct_at_age``;
    the mortality at every age from 40 to 130, S's table capped at its last age, on a male
    point and on ``Data``'s checked copy of both sexes; the withdrawal charge at every count
    of completed years of S's frame, on both schedules, against S's ``surr_charge_rate``;
    the excess programme's premium and withdrawal at every policy month of S's frame,
    against S's ``prem_scheduled_pp`` and ``wd_scheduled_pp``; and each subaccount's
    allocation and fund expense, against S's.
    """
    p1, s1 = _row(sec_model, "twin", 1, 0), _point(s_model, 1)
    assert [p1.gawa_pct_at_age(a) for a in range(126)] == [
        s1.gawa_pct_at_age(a) for a in range(126)]
    rates = s_model.Data.mort_table()
    assert [p1.mort_rate_base_at(x) for x in range(40, 131)] == [
        float(rates.loc[(min(x, 120), "M"), "mort_rate"]) for x in range(40, 131)]
    checked = sec_model.Data.mort_rates()
    for sex in ("M", "F"):
        assert [float(checked.loc[(x, sex), "mort_rate"]) for x in range(40, 121)] == [
            float(rates.loc[(x, sex), "mort_rate"]) for x in range(40, 121)], sex
    for point_id in (1, 7):
        p, s = _row(sec_model, "twin", point_id, 0), _point(s_model, point_id)
        years = range(s.proj_len() // 12)
        assert [p.surr_charge_rate_at(k) for k in years] == [
            s.surr_charge_rate(12 * k) for k in years], point_id
    p4, s4 = _row(sec_model, "twin", 4, 0), _point(s_model, 4)
    assert [p4.prem_scheduled_pm(m) for m in range(720)] == [
        s4.prem_scheduled_pp(m) for m in range(720)]
    assert [p4.wd_scheduled_pm(m) for m in range(720)] == [
        s4.wd_scheduled_pp(m) for m in range(720)]
    assert p1.sub_ids() == s1.sub_ids() == [1, 2]
    for i in (1, 2):
        assert (p1.alloc(i), p1.fund_expense_rate(i)) == (s1.alloc(i),
                                                          s1.fund_expense_rate(i))


def test_the_points_sum_row_by_row_into_a_block(sec_model, s_model):
    """Row ``t`` is the same month on every point, so a block is its frames summed (D3).

    The anchor issued at the valuation date, the anchor valued at its first withdrawal,
    120, and the anchor issued 15 months on, summed as ``run_sec.py --block`` sums them,
    are indexed 0..734 and equal S's frame added to itself moved 120 months earlier and 15
    months later, in every column but the two expense inflation moves (:data:`INFLATED`).
    A model whose frames sat on the policy clock would fail it.  The committed rows are
    already swept, so it costs a sum.
    """
    cases = (("twin", 1, 0), ("derived", 1, 120), ("future", 1, -15))
    block = pd.concat([_row(sec_model, *case).result_cf() for case in cases]).groupby(
        level="t").sum()
    sdf = _point(s_model, 1).result_cf()
    expected = pd.concat([sdf, sdf.set_axis(sdf.index - 120).loc[0:],
                          sdf.set_axis(sdf.index + 15)]).groupby(level=0).sum()
    assert list(block.index) == list(range(735))
    keep = [c for c in sdf.columns if c not in INFLATED]
    assert frame_mismatches(expected, block, columns=keep, atol=0.0) == []


@pytest.fixture(scope="module")
def committed_runs():
    """``run_sec.py`` on the committed table: each argument list run once, its output kept.

    The runner test and the extract test both read ``run_sec.py``'s default point, and an
    interpreter that reads the model and projects a point costs seconds.
    """
    runs = {}

    def run(*args):
        if args not in runs:
            runs[args] = _run_sec(model_path(SEC).parent / "run_sec.py", *args)
        return runs[args]
    return run


# The rows the extract test projects: the twins of S's points 2 and 1, the row restated
# from S's point 2, the decline path depleted at 144 and the anchor issued 15 months on.
EXTRACT_ROWS = (("twin", 2, 0), ("twin", 1, 0), ("derived", 2, 14), ("derived", 3, 144),
                ("future", 1, -15))


def test_an_in_force_extract_needs_none_of_the_generator_columns(sec_model, tmp_path,
                                                                 committed_runs):
    """The model reads the in-force interface and S's columns, never where a row came from.

    ``row_kind``, ``source_policy_id`` and ``source_mth`` record how the generator made each
    shipped row, and an administration extract carries none of them.  Read without them,
    relabeled ``100 + point_id`` and written in reverse order, so that no label is its
    position, every point projects what the committed point it was made from projects, in
    ``result_cf`` and ``result_pols``, exactly.  On S's point 2 and the row restated from it
    ``source_mth`` is not ``duration_mth``, so a formula that read the one for the other
    fails here too.  The rows projected are those whose generator columns say most: S's
    point 2 and the row restated from it, the anchor issued at the valuation date, the
    depleted row and the anchor issued 15 months on.  And ``run_sec.py``, run beside the
    extract, finds point 101 by its label and prints it without saying where it came from,
    every later line as it prints committed point 1, and refuses point 1, which the
    extract does not have, and a label that is not a number, naming the labels it does,
    without a traceback.
    """
    committed = _committed()
    extract = _relabeled(committed.drop(columns=list(GENERATED_COLUMNS)))
    folder = _sec_inputs(tmp_path, extract)
    model = _read(folder, "extract")
    try:
        table = model.Data.model_point_table()
        assert not set(GENERATED_COLUMNS) & set(table.columns)
        assert list(table.index) == [100 + p for p in reversed(committed.index)]
        for label in [100 + _label(committed, *case) for case in EXTRACT_ROWS]:
            mine, base = _point(model, label), _point(sec_model, label - 100)
            for report in ("result_cf", "result_pols"):
                assert frame_mismatches(base.cells[report](), mine.cells[report](), rtol=0,
                                        atol=0) == [], (label, report)
            _release(model, _key(model, label))
    finally:
        model.close()
    runner = folder.parent / "run_sec.py"
    shutil.copy(model_path(SEC).parent / "run_sec.py", runner)
    out, base = _run_sec(runner, "101").splitlines(), committed_runs().splitlines()
    assert out[0] == "model point 101: VA-000001 - M60 NQ single life, premium 100,000"
    assert out[1:] == base[1:]
    labels = [100 + p for p in reversed(committed.index)]
    for label in ("1", "x"):
        refused = _run_sec(runner, label, check=False)
        assert refused.returncode == 1 and refused.stdout == b"", label
        assert refused.stderr.decode(errors="replace").strip() == (
            f"no model point {label} in the table: {labels}")


def _months(n):
    """``n`` with its unit, as ``run_sec.py`` writes it: "1 month", "15 months"."""
    return f"{n} month" if n == 1 else f"{n} months"


def _standing(p):
    """What ``run_sec.py`` says of point ``p`` at the valuation date, stated here."""
    d = p.duration_mth_init()
    if d < 0:
        return f"to be issued at t = {-d}, {_months(-d)} after the valuation date"
    if d == 0:
        return "issued at the valuation date, t = 0"
    return (f"in force {_months(d)}: contract year {p.policy_year(0)}, attained age "
            f"{p.age(0)}, {p.pols_if(0):.6f} in force, AV {p.av_pp_init():,.2f} per "
            f"contract" + (", depleted" if p.depleted_open(0) else ""))


def _worked_block(out):
    """The worked-example block of a run's output, its heading's ``t`` cut off."""
    lines = out.splitlines()
    start = next(i for i, line in enumerate(lines) if line.startswith("worked-example"))
    return lines[start + 1:start + 7]


def test_run_sec_prints_a_point_and_the_block(sec_model, s_model, committed_runs):
    """The runner prints one point, saying where it came from, and the block (D8).

    Each mode in an interpreter of its own, as a user runs it, with exit code 0 and ASCII
    output, so that it prints on a Windows console under any code page.  The numbers are
    the model's.  The anchor issued at the valuation date, the runner's default, S's
    point 2 in force at 26, the decline path depleted at 144 and the anchor issued 15
    months on, each with its lines at the valuation date asserted whole, so that a longer
    number cannot pass for the one asserted: where its row came from, which only the
    committed table's generator columns can say, the contract and its riders, where it
    stands, its frame, and when its first withdrawal falls and its account value runs out,
    or that each fell before the valuation date.  On the anchor and on S's point 2 the
    worked example's month is printed, at ``t = 26`` and at ``t = 0``, and its six lines are
    the same on both, as S's two readings are.  Then the bases and the account value at
    the first fourteen anniversaries on the books, the cash flows month by month and by
    projection year.  And the block: a line for each of the 23 points, in table order, its
    first twelve rows, which must be the committed points' frames summed row by row, as
    this test sums them, and those frames summed into projection years, each year's count
    the one in force in its first month.
    """
    header = "model point {}: {}{} - M60 NQ single life, premium {}"
    riders = ["GLWB s3_single at 1.25% of GWB, bonus 6.00%, step-up on annual_CV; "
              "GMDB rollup at 0.90% of RB",
              "For Life Guarantee in effect; GLWB activates at age 70 at 100% of GAWA"]
    frame = ("proj_len = {} from the valuation date (t = 0..{}); cover ends at policy "
             "month 720, attained age 120")
    cases = (((), ("twin", 1, 0), "1", "VA-000001", " (S's VA-000001)", "100,000",
              "first withdrawal in contract year 11, at t = 120; account value runs out in "
              "contract year 20, at t = 228"),
             (("2",), ("twin", 2, 0), "2", "VA-000002", " (S's VA-000002)", "0", None),
             (("13",), ("derived", 3, 144), "13", "VA-000003-M144",
              " (S's VA-000003 at its month 144)", "100,000",
              "first withdrawal before the valuation date; account value runs out before "
              "the valuation date"),
             (("23",), ("future", 1, -15), "23", "VA-000001-F15",
              " (S's VA-000001, issued 15 months on)", "100,000",
              "first withdrawal in contract year 11, at t = 135; account value runs out in "
              "contract year 20, at t = 243"))

    def by_year(cf):
        """``cf`` summed into projection years, each year's count its first month's."""
        years = pd.Index(cf.index // 12 + 1, name="proj_year")
        annual = cf.drop(columns="pols_if").groupby(years).sum()
        annual.insert(0, "pols_if", [cf.at[12 * (y - 1), "pols_if"] for y in annual.index])
        return annual

    for args, case, label, policy, origin, premium, events in cases:
        p = _row(sec_model, *case)
        out = committed_runs(*args)
        lines = out.splitlines()
        assert lines[0] == header.format(label, policy, origin, premium), args
        assert lines[3] == f"at the valuation date: {_standing(p)}", args
        assert lines[4] == frame.format(_months(p.proj_len()), p.proj_len() - 1), args
        if events is not None:
            assert lines[5] == events, args
        if case[1] in (1, 2):
            assert lines[1:3] == riders, args
        anniversaries = [t for t in range(p.t_entry(), p.proj_len())
                         if p.duration_mth(t) % 12 == 11]
        bases = p.result_bases().loc[anniversaries[:14], ["gwb_pp", "gawa_pp", "bb_pp",
                                                          "rb_pp", "adj_pp", "db_pp"]]
        trace = bases.join(p.result_av().loc[anniversaries[:14], ["av_pp"]])
        assert trace.round(2).to_string() in out, args
        assert p.result_cf().head(12).round(2).to_string() in out, args
        assert by_year(p.result_cf()).head(14).round(2).to_string() in out, args
    assert _worked_block(committed_runs()) == _worked_block(committed_runs("2"))
    assert "(the 27th policy month, t = 26)" in committed_runs()
    assert "(the 27th policy month, t = 0)" in committed_runs("2")
    assert "worked-example" not in committed_runs("13")
    s2 = _point(s_model, 2).result_bases()
    twin = _row(sec_model, "twin", 2, 0).result_bases()
    assert twin.loc[9].tolist() == s2.loc[9].tolist()
    out = committed_runs("--block")
    table = sec_model.Data.model_point_table()
    points = [projection(sec_model, key) for key in point_keys(sec_model)]
    assert out.splitlines()[:len(points) + 1] == [
        "model points, t = 0 the valuation date for each:",
        *("  {:>2}  {:<16} {}; proj_len {}".format(
            point_id, table.at[point_id, "policy_id"], _standing(p), p.proj_len())
          for point_id, p in zip(table.index, points))]
    assert ("  23  VA-000001-F15    to be issued at t = 15, 15 months after the valuation "
            "date; proj_len 735") in out
    block = pd.concat([p.result_cf() for p in points]).groupby(level="t").sum()
    assert block.head(12).round(2).to_string() in out
    assert by_year(block).head(12).round(2).to_string() in out


def _docs(model):
    """``(where, docstring)`` for the model, each Space and each cells, blanks as ``""``."""
    yield "model", model.doc or ""
    for space in model.spaces.values():
        yield space.name, space.doc or ""
        for cells in space.cells.values():
            yield f"{space.name}.{cells.name}", cells.doc or ""


def _symbol_map(doc):
    """The rows of the symbol map in ``doc``, the Projection docstring, with their spans.

    The map is an RST simple table whose header row starts ``Notes symbol``.  The runs of
    ``=`` in the border under the header give the column spans.  Returns ``(spans, rows)``,
    each row the list of its lines, a line whose first column is blank continuing the row
    above.
    """
    lines = doc.splitlines()
    head = next(i for i, line in enumerate(lines) if line.startswith("Notes symbol"))
    spans = [m.span() for m in re.finditer("=+", lines[head + 1])]
    rows = []
    for line in lines[head + 2:]:
        if line.startswith("="):
            break
        if not line.strip():
            continue
        if line[spans[0][0]:spans[0][1]].strip() or not rows:
            rows.append([line])
        else:
            rows[-1].append(line)
    return spans, rows


def _mapped_cells(doc):
    """The names in the Cells column of the symbol map in ``doc``, the Projection docstring.

    A name is the identifier that opens the column, ``age`` of ``age(t)``.
    """
    spans, rows = _symbol_map(doc)
    start, end = spans[1]
    names = set()
    for row in rows:
        for line in row:
            found = re.match(r"[a-z_][a-z0-9_]*", line[start:end].strip())
            if found:
                names.add(found.group())
    return names


def _rows_with_a_blank_column(doc):
    """The symbol map's rows, with their continuation lines, that leave a column blank.

    docutils reads a simple table's row and the lines under it whose first column is blank
    as one row, each column's text joined: a row whose cell runs into the symbol's column,
    and its meaning into the cell's, leaves its last column blank, and the page shows the
    meaning under the wrong heading.
    """
    spans, rows = _symbol_map(doc)
    blank = []
    for row in rows:
        for n, (start, end) in enumerate(spans):
            last = n == len(spans) - 1
            if not any(line[start:None if last else end].strip() for line in row):
                blank.append(row[0].strip())
                break
    return blank


_RULE = re.compile(r"^\s*=+(\s+=+)+\s*$")


def _columns_taken(line):
    """The display columns ``line``'s text occupies, an East Asian wide character two."""
    taken, col = set(), 0
    for ch in line:
        width = 2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1
        if ch != " ":
            taken.update(range(col, col + width))
        col += width
    return taken


def _table_overruns(doc):
    """The rows of the RST simple tables in ``doc`` that put text between two columns.

    A simple table's rule lines, runs of ``=`` apart, give its columns' spans, and a row
    whose text runs into the gap between two spans is what docutils rejects as a
    malformed table, dropping the whole table from the page.  Only the last column may run
    past its rule.  Each table runs from a rule line to the blank line that ends it.
    """
    lines, found, i = doc.splitlines(), [], 0
    while i < len(lines):
        if not _RULE.match(lines[i]):
            i += 1
            continue
        spans = [m.span() for m in re.finditer("=+", lines[i])]
        gaps = set()
        for (_, end), (start, _) in zip(spans, spans[1:]):
            gaps.update(range(end, start))
        i += 1
        while i < len(lines) and lines[i].strip():
            if not _RULE.match(lines[i]) and _columns_taken(lines[i]) & gaps:
                found.append(lines[i].strip())
            i += 1
    return found


def test_the_docstrings_describe_the_valuation_clock(sec_model, s_model):
    """The docstrings say what this model is, and none says what only VA_US_S is.

    Whitespace is collapsed first, as ``test_model_conventions`` collapses it, so that a
    phrase split across a line break still matches.  The model docstring names the
    valuation date, BasicTerm_SE, the policy clock, the SEC table and the product.  The
    symbol map in the Projection docstring maps every cell running in force adds, which are
    exactly the cells ``VA_US_S`` lacks, and every opening-state column that is a cell, the
    two subaccount values through ``sa_pp_init``, and names nothing the model lacks: every
    name in it is a cell or a Reference.  No row of a simple table in any docstring puts
    text between two of its columns (:func:`_table_overruns`), which would drop the table
    from the rendered page; no row of the symbol map, with the lines under it whose first
    column is blank, leaves a column blank (:func:`_rows_with_a_blank_column`), which
    docutils would read into the wrong cells, as it reads five of ``VA_US_S``'s; and no
    docstring line is over 92 characters.  And no docstring says what :data:`STALE`
    matches, each of whose phrases ``VA_US_S``'s docstrings say.
    """
    flat = {where: re.sub(r"\s+", " ", doc) for where, doc in _docs(sec_model)}
    for phrase in ("valuation date", "BasicTerm_SE", "duration_mth", TABLE,
                   "variable annuit"):
        assert phrase in flat["model"], phrase
    assert set(NEW_CELLS) == set(sec_model.Projection.cells) - set(s_model.Projection.cells)
    doc = sec_model.Projection.doc
    mapped = _mapped_cells(doc)
    missing = [cells for cells in (*NEW_CELLS, *STATE)
               if cells not in FUNDS and cells not in mapped]
    assert not missing, f"the symbol map does not map {missing}"
    known = set(sec_model.Projection.cells) | set(sec_model.Projection.refs)
    unknown = sorted(mapped - known)
    assert not unknown, f"the symbol map names what the model lacks: {unknown}"
    blank = _rows_with_a_blank_column(doc)
    assert not blank, f"symbol-map rows that leave a column blank: {blank}"
    assert _rows_with_a_blank_column(s_model.Projection.doc), (
        "VA_US_S's map has rows that leave a column blank, which the check must see")
    overruns = {where: rows for where, rows in ((where, _table_overruns(doc))
                                                for where, doc in _docs(sec_model)) if rows}
    assert not overruns, f"table rows that run into a column gap: {overruns}"
    long = [(where, len(line)) for where, doc in _docs(sec_model)
            for line in doc.splitlines() if len(line) > 92]
    assert not long, f"docstring lines over 92 characters: {long[:5]}"
    stale = sorted(where for where, doc in flat.items() if STALE.search(doc))
    assert not stale, f"docstrings that describe VA_US_S: {stale}"
    s_flat = [re.sub(r"\s+", " ", doc) for _, doc in _docs(s_model)]
    unsaid = [phrase for phrase in STALE_PHRASES
              if not any(re.search(phrase, doc) for doc in s_flat)]
    assert not unsaid, f"phrases VA_US_S does not say, so STALE holds nothing: {unsaid}"
    broken = ("=" * 24 + "  " + "=" * 4 + "\n(shortfall at exhaustion) av_depletion_pp(t)\n"
              + "=" * 24 + "  " + "=" * 4 + "\n")
    assert _table_overruns(broken) == ["(shortfall at exhaustion) av_depletion_pp(t)"]


def test_the_docstrings_parse_as_rst(sec_model):
    """Every docstring of the model parses as reStructuredText, without a warning.

    The docs build reads each docstring through docutils, which reports a malformed table, a
    bad indentation or an unclosed inline markup and drops what it cannot read; a raw-text
    test sees none of it.  Each docstring, dedented as autodoc dedents it and its Sphinx
    roles read as plain interpreted text, which docutils alone does not know, is parsed
    here, and any warning or error is a fault.  docutils comes with the docs build, not with
    the models' requirements, so the test is skipped where it is absent; the column checks
    in the test above run everywhere.
    """
    core = pytest.importorskip("docutils.core")
    faults = []
    for where, doc in _docs(sec_model):
        stream = io.StringIO()
        core.publish_doctree(re.sub(r":[a-z]+:`", "`", inspect.cleandoc(doc)),
                             settings_overrides={"report_level": 2, "halt_level": 5,
                                                 "warning_stream": stream})
        faults += [f"{where}: {line}" for line in stream.getvalue().splitlines()
                   if re.search(r"\((WARNING|ERROR|SEVERE)/", line)]
    assert not faults, f"{len(faults)} docutils messages, first:\n  " + "\n  ".join(
        faults[:10])


def _values(refs):
    """The values of ``refs``, a Space's References, each as it compares: a module by its
    name; the Interface to the other Space left out."""
    return {name: value.__name__ if inspect.ismodule(value) else value
            for name, value in refs.items() if name != "data"}


# The References this model adds to VA_US_S's: on Projection, the three tolerances its
# checks read, S's own literals, 1e-6 of a currency unit, 1e-12 of a contract and 1e-8 per
# contract; on Data, the horizon of future business (D4).
ADDED_REFERENCES = {"Projection": {"check_tol_av": 1e-06, "check_tol_pols": 1e-12,
                                   "check_tol_charge": 1e-08},
                    "Data": {"future_horizon_mth": 120}}


def test_the_sec_model_reads_the_s_tables_in_place(sec_model, s_model):
    """One copy of each assumption table serves both models (D1), on S's own References.

    The two ``input_dir()`` s are one directory, and SEC's filename References are S's with
    three changed: ``model_point_file``, to ``model_point_table_sec.csv``, and
    ``return_scenario_file`` and ``rate_scenario_file``, to the companions, the scenarios
    re-based to each row's valuation month (D8).  An edit to any other table reaches both
    models, and the two can never drift apart; an edit to S's scenarios reaches this model
    through the companions' regeneration, which T6 holds.  And every other Reference of
    either Space is S's, value for value, but those this model adds
    (:data:`ADDED_REFERENCES`): a constant copied wrong that changes no number a comparison
    reads, a GWB cap of $1,000,000 for S's $10,000,000 or a Bonus Period restart age of 80
    for S's 81, would otherwise pass every test whose rows never reach it.
    """
    assert sec_model.Data.input_dir() == s_model.Data.input_dir()
    files = {r: v for r, v in s_model.Data.refs.items() if r.endswith("_file")}
    assert {r: v for r, v in sec_model.Data.refs.items() if r.endswith("_file")} == {
        **files, "model_point_file": TABLE, "return_scenario_file": RETURNS,
        "rate_scenario_file": RATES}
    for space in ("Projection", "Data"):
        theirs = _values(s_model.spaces[space].refs)
        mine = _values(sec_model.spaces[space].refs)
        if space == "Data":
            theirs = {**theirs, **{r: mine[r] for r in files}}
        assert mine == {**theirs, **ADDED_REFERENCES[space]}, space
