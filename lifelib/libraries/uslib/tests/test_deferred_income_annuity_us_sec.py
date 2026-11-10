"""In-force tests for DIA_US_SEC: the splice, future business, counts, regeneration.

``DIA_US_SEC`` is ``DIA_US_S`` taught to run in force at a valuation date
(USLIB-SEC-PLAN.md, milestone M12).  It runs on two clocks: ``t`` counts months from the
valuation date, the same month for every model point, and ``duration_mth(t)`` counts the
months from issue, ``duration_mth_init() + t``.  A model point may be a contract already in
force at the valuation date, in its deferral or in its income phase, one issued at it, or
one issued up to ten years after it, as in ``basiclife/BasicTerm_SE``.  A contract in force
opens with eight columns of state beside its count: each covered life's probability of
being alive at the valuation date; the premiums paid and the income they bought; on a cash
or installment refund, the guarantee period the pricing kernel prices every slice with, a
fixed point over the whole premium schedule; the cohort that reached the income phase,
``l_last(T)``, past the income start month, and the cohort that commuted, ``l_last(t_c)``,
past a commutation; and the reference rate's change since issue, which moves the
commutation discount rate.  Its premiums still due are in its own premium schedule,
``premium_schedule_sec.csv``.  Pricing stays at issue and at the premium dates, on a
survival curve of its own from issue, and the payout schedule is fixed at the income start
month and read by policy month, so neither needs a column.

The worked example is not restated here.  On a point issued at the valuation date the two
clocks coincide and the model is ``DIA_US_S``, and ``test_model_conventions.py`` asserts
that cell by cell on the twins of S's seventeen points (T1), so every golden of
``test_deferred_income_annuity_us.py`` holds on this model with no number copied.  The
conventions also hold the SEC family's other rules: every frame opens at ``t = 0``,
``BEF_DECR`` is ``BEF_NB`` plus the month's new business, new business enters once, and
nothing happens before issue.  ``pols_if`` here is the count on the books weighted by the
probability that a covered life is alive, as ``DIA_US_S`` weights its constant count, so
the model is registered ``survival_pols_if`` and skips the convention that ``pols_if`` is
the ``BEF_DECR`` count; this module asserts what it is instead.  It holds the rest of the
plan's tests (its §5.2) and the product's own facts:

* T2, the splice: an S point restated in force at month ``d``, opened with the state S
  carries into ``d``, continues S's projection from ``d`` on, in every cell of S's and in
  ``result_pols``.  The months are the ones S's events need: either side of the second
  premium, of the income start month and of each option month, the last month of each
  refund, derived and certain period and the first after it, the month before mortality's
  cap binds and the months after a life dies with certainty, the anniversaries and the
  last month of a frame.  Eighteen variants of S's points, in a copy of S's table, reach
  what S's own points cannot.
* T3, future new business: a contract issued ``k`` months after the valuation date is S's
  projection ``k`` months on, with zeros before it and no rate evaluated there.
* D11's R1, R1a and R2, and D3's clock: on the splice's grid no cell is called at a
  negative argument, nor at a policy month, a policy year or an age the contract does not
  have, none evaluated on the books reads a month before them, and none reads beyond
  ``t + 1``; on the committed points no recursion runs backward over the frame, a cold
  call runs one cell a month, a cold first month a handful of cells, and the policy clock
  is a closed form.
* T4, the count algebra: the count is on the books from issue to the stop rule,
  ``pols_if`` is that count weighted by survival, ``result_pols`` is S's report with the
  new business beside it, and multiplying ``policy_count`` by 2.5, with the reference
  rate's change switched on, multiplies every flow and moves no per-contract value.
* T5, validation: each malformed in-force row and each malformed premium schedule is
  refused as its table is read, naming its point, and each malformed assumption table, a
  key or a value, by the count cell beside its reader, naming the file's lines, and each
  again through a projection; a point at or past the stop rule, owing nothing, or
  accelerating inside a commuted guarantee, is refused by ``proj_len()``; the future
  horizon is a Reference that bounds future business, and at 0 refuses it; the edges of
  the interface, and assumption keys written as floats, are accepted, each check over a
  window of contract months refused just inside each end and read just outside it; and
  every state S reaches, restated in force, is accepted, but a contract owing nothing,
  which is refused by name.
* T6, regeneration: the committed ``model_point_table_sec.csv`` and
  ``premium_schedule_sec.csv`` are what the generator makes of ``DIA_US_S`` and its inputs
  as they stand, and each derived and future row in them is its S point from its month on,
  frame by frame.
* Then the product's own facts: the worked example's derived rows, pricing at issue and
  the premium dates, the payout schedule fixed at the income start month, survival per
  life, the contract open after the last death in a guarantee, a commutation and an
  acceleration before the valuation date, the commutation residual where its guarantee
  ends, the reference rate's change since each contract's own issue, improvement on the
  policy clock and inflation on the valuation clock, the capped mortality rate, the checks
  failing a residual that is not a number, new business with its premiums and no
  acquisition, no lapse, the stop rule, the values outside cover, the block, the annual
  display, an in-force extract, the runner, the docstrings, the shared input tables,
  invalid values, and what the default grid reaches.

SEC month ``t`` is S month ``t + source_mth`` throughout, the direction in which
``sec_support`` takes its ``t_offset``: ``d`` for a point restated at S month ``d``, ``-k``
for one issued ``k`` months on.  ``DIA_US_S`` has no point in force, so every twin is new
business, compared by T1, and every splice case is a derived row.

**The core grid and the full one** (USLIB-SEC-PLAN.md K6).  T2 and T3 over every month the
product's events need, 112 splices and 21 future points, would take this module well past
three minutes in every run.  By default they run a core of 36 and 8, chosen so that between
them they reach every form, trigger, basis, timing and frequency, every market type and
option, every opening-state column, every kind of valuation month and every branch the full
grid reaches, which ``test_the_core_grid_reaches_every_branch`` asserts; measured line by
line when the module was written, the core's cases execute every line of ``Projection`` the
full grid's execute.  The other cases, and the rules test's scan of their rows, carry the
``sec_full`` marker and are skipped, with the reason shown, unless ``USLIB_SEC_FULL=1`` is
set.  They are never dropped: one leg of the CI matrix sets it, and ``USLIB_SEC_FULL=1
python -m pytest -m sec_full`` on this module runs them alone.  The every-state test
restates S's states at the edges of the product's windows by default, and at every month
of every frame with ``USLIB_SEC_FULL=1``.  Memory is the other cost.  A projected point
holds its cached values and their dependency graph, so a row read once, a splice case's
or a point of a temporary copy, is released as soon as it has been read (``_release``),
and the splice's rows are held one at a time, however large the grid.  The three models
the module sweeps once and holds, the splice's S model and the committed S and SEC models,
are frozen out of the collector (``gc.freeze``), so that a collection scans only what a
test has made since, and the freeze is undone as the module ends (:func:`_freeze`).

Every test keeps four rules.  Each model is read under a name of its own and closed:
``test_deferred_income_annuity_us.py`` reads S under its default name, and reading a model
under a name in use renames the open one.  No test writes inside the library tree: every
changed input goes through ``sec_support.temp_inputs`` into a temporary directory, because
a CSV added beside the models, even briefly, would fail a concurrent
``test_every_csv_beside_the_model_is_actually_read``.  No test indexes ``Projection`` by
hand: the keys come from ``us_registry.point_keys`` and the ItemSpaces from
``us_registry.projection``, and a generated row is found by what it is, its kind, its S
policy and its month (``_row``), so neither a renumbered table nor Phase 2's positions can
point a test at the wrong row.  And every Reference a test changes, ``Data``'s included, is
set on a model just read, before it computes anything, because a compiled model never
clears a cache; timings and kinds pass through :func:`_code`, so that the same calls serve
Phase 2's int codes (C1).
"""
import dataclasses
import gc
import itertools
import math
import os
import re
import shutil
import subprocess
import sys

import modelx as mx
import pandas as pd
import pytest

from sec_support import (
    GENERATED_COLUMNS, SEC_SPECS, TWIN_EXEMPT_DEFAULT, build_sec_table, check_generated,
    codes, frame_mismatches, temp_inputs, twin_mismatches)
from us_registry import model_path, point_keys, projection

SEC, TWIN = "DIA_US_SEC", "DIA_US_S"
TABLE, SCHEDULE = "model_point_table_sec.csv", "premium_schedule_sec.csv"
SPEC = SEC_SPECS[SEC]
NAN = float("nan")

# Eighteen more S points, in the splice's copy of S's table and never in the committed
# one, each one of S's points changed so as to reach what S's own points cannot.  S's
# points are the female anchor life at 60, paying monthly in arrears from policy month 240
# but for one in advance, nonqualified but for the two QLACs, on the anchor mortality basis
# but for one, and each exercises at most one option.  Each variant is (the S point it
# changes, the columns it changes), and takes its base's premium rows; the policy_id keeps
# the generated ids apart.
#
# 18, the anchor on the table basis on a male life, TradIRA, its purchase rate rounded to 4
#   places: both factor tables read on their male rows, and the cap on a male life;
# 19, the death-benefit fork as life only on the table basis, RothIRA: the life-only payout
#   factor and a pricing guarantee of 0;
# 20, life only with the return-of-premium death benefit, LO_ROP: ROP in deferral and a
#   pure life annuity in payout;
# 21, the installment refund paying quarterly in arrears on a 2% COLA, half of its derived
#   period commuted at policy month 252;
# 22, the installment refund paying semi-annually in advance: the refund-period search in
#   advance;
# 23, the cash refund on computed factors paying semi-annually in arrears;
# 24, the 10-year period certain paying annually in arrears;
# 25, the period certain accelerated at policy month 357, so that the five instalments the
#   lump sum pulls forward straddle the guarantee's end: floors 1, 1, 0, 0, 0;
# 26, the commuting period certain paying quarterly in advance, half of it commuted;
# 27, the cash refund with a commutation at policy month 252 and nothing guaranteed to
#   commute;
# 28, the joint point with a female joint annuitant at 57, the younger life;
# 29, the joint point on the primary trigger, generational: improvement on both sexes;
# 30, the 10-year period certain bought at 80 with a 30-year guarantee: the life dies with
#   certainty at 120 inside it;
# 31, the joint point bought at 80 and 85 as a 30-year period certain: both lives dead
#   inside the guarantee;
# 32, the QLAC breaching its limit turned installment refund on a 1% COLA from policy month
#   360, with 20,000 of other QLAC premium, a half commutation at 365 inside its derived
#   period and an acceleration at 390 on life-contingent instalments: a QLAC failing all
#   six of its conditions;
# 33, the start-date adjustment advancing the income start to policy month 180 at policy
#   month 30, before the second premium, which is then priced to the new date;
# 34, the advance cash refund paying annually;
# 35, the commuting period certain half commuted at policy month 252 and accelerating in
#   its guarantee's last month, 359, so that its lump sum pulls forward only the life tail
#   (proj_len() refuses a lump sum that pulls forward instalments of the commuted
#   guarantee), and the commutation residual adds the lump sum back.
VARIANTS = {
    18: (1, {"policy_id": "DIA-900018", "sex": "M", "market_type": "TradIRA",
             "purchase_rate_dp": 4}),
    19: (4, {"policy_id": "DIA-900019", "income_form": "LO", "market_type": "RothIRA"}),
    20: (6, {"policy_id": "DIA-900020", "income_form": "LO_ROP", "db_form": "ROP"}),
    21: (5, {"policy_id": "DIA-900021", "frequency": 4, "cola_rate": 0.02,
             "commute_mth": 252, "commute_frac": 0.5}),
    22: (5, {"policy_id": "DIA-900022", "frequency": 2, "timing": "advance"}),
    23: (3, {"policy_id": "DIA-900023", "frequency": 2}),
    24: (7, {"policy_id": "DIA-900024", "frequency": 1}),
    25: (7, {"policy_id": "DIA-900025", "accel_mth": 357}),
    26: (15, {"policy_id": "DIA-900026", "frequency": 4, "timing": "advance",
              "commute_frac": 0.5}),
    27: (3, {"policy_id": "DIA-900027", "commute_mth": 252, "commute_frac": 1.0}),
    28: (8, {"policy_id": "DIA-900028", "joint_sex": "F", "joint_age": 57}),
    29: (9, {"policy_id": "DIA-900029", "mort_basis": "generational"}),
    30: (7, {"policy_id": "DIA-900030", "issue_age": 80, "certain_period": 30}),
    31: (8, {"policy_id": "DIA-900031", "issue_age": 80, "joint_age": 85,
             "income_form": "PC", "certain_period": 30}),
    32: (12, {"policy_id": "DIA-900032", "income_form": "IR", "cola_rate": 0.01,
              "income_start_mth": 360, "commute_mth": 365, "commute_frac": 0.5,
              "accel_mth": 390, "other_qlac_premium": 20000.0}),
    33: (13, {"policy_id": "DIA-900033", "adjust_mth": 30, "adjust_start_mth": 180}),
    34: (17, {"policy_id": "DIA-900034", "frequency": 1}),
    35: (15, {"policy_id": "DIA-900035", "commute_frac": 0.5, "accel_mth": 359}),
}

# T2's months, by S point or variant: every month S's events need, chosen on the splice's
# edited inputs, where the set-apart tables and the A/E move some events from where the
# shipped inputs put them (below).  12 and 24, anniversaries in deferral; 59, 60 and 61,
# either side of the second premium; 239, 240 and 241, either side of the income start
# month T, and 299, 300 and 301 where T is 300; 270, 279 and 280 on the installment refund,
# inside its derived period, its last certain month and the first after; 279 and 280 on
# the anchor, the refund's last month and the first without; 359 and 360, the end of a
# 10-year guarantee; 251, 252 and 253 around the COLA's first step, the acceleration and
# the commutation, and 257 and 258, the blackout's end; 119, 120 and 121 around the
# start-date adjustment, and 179 and 180 around its advanced start; 647 and 683, the month
# before the cap binds on a male life of 117, and 649, the joint annuitant dead from it;
# 479, 480, 500 and 599, around omega inside a 30-year guarantee; 384 and 500, both lives
# dead inside one; 356 to 362 around an acceleration straddling a guarantee's end, and 240,
# its income start month, where l_last(T) is derived and the lump sum's floor reads it; 365
# and 390, a commutation inside a derived period and an acceleration after it; 252 and 359,
# a half commutation and an acceleration in the guarantee's last month; months off the
# payment step of each frequency below monthly; and 719, the last month of a frame.
SPLICE_MTHS = {
    1: (12, 24, 59, 60, 61, 239, 240, 241, 279, 280, 719),
    2: (60, 241), 3: (59, 241), 4: (59, 240), 5: (239, 240, 270, 279, 280),
    6: (60, 240), 7: (239, 300, 359, 360), 8: (12, 240, 300, 647, 649), 9: (240, 649),
    10: (251, 252), 11: (299, 300), 12: (300,), 13: (59, 119, 120, 121, 299, 300, 301),
    14: (59, 60, 61, 251, 252, 253, 257, 258), 15: (59, 251, 252, 253, 359, 360),
    16: (24, 240), 17: (239, 240, 241), 18: (60, 241, 683), 19: (240,), 20: (59, 240),
    21: (241, 252, 253), 22: (241, 250), 23: (243, 245), 24: (250, 251, 359),
    25: (240, 356, 357, 358, 362), 26: (250, 252, 253), 27: (252,), 28: (240, 300),
    29: (24, 240, 649), 30: (479, 480, 500, 599), 31: (384, 500), 32: (365, 390),
    33: (29, 30, 31, 179, 180), 34: (245,), 35: (252, 359)}

# T2's cases, as (row_kind, S point, source_mth), and T3's, as (S point, k).  DIA_US_S has
# no point in force, so there is no twin to splice (§5.2's IN_FORCE_TWINS).  The future
# offset is 13: more than a year, so that a read before issue lands at policy year -1, and
# off every payment step, so that the payment months fall apart on the two clocks.  12
# puts the anniversaries back on the valuation years, and 1 puts them a month off; 120 is
# the horizon itself, the commutation of point 15 falling 372 months on.
SPLICES = tuple(("derived", p, d) for p, ds in SPLICE_MTHS.items() for d in ds)
IN_FORCE_TWINS = ()
FUTURES = (((1, 1), (8, 12), (15, 120))
           + tuple((p, 13) for p in (1, 3, 5, 7, 9, 11, 13, 14, 15, 16, 17, 21, 22, 25,
                                     26, 30, 32, 33)))

# The default run's cases (the module docstring), each with what it is there for.  The
# rest of SPLICES and FUTURES run with USLIB_SEC_FULL=1.
CORE_SPLICES = {
    ("derived", 1, 59): "the table basis in deferral: the second slice at t = 1, dp 6",
    ("derived", 1, 240): "the income start at t = 0: the refund of the whole CP(T)",
    ("derived", 1, 719): "the last month: a one-row frame",
    ("derived", 5, 240): "the installment refund at T: l_last(T) derived at t = 0",
    ("derived", 5, 279): "the installment refund's last certain month",
    ("derived", 7, 239): "the period certain the month before T: l_last(T) at t = 1",
    ("derived", 7, 300): "inside the guarantee: the contract open above the life alive",
    ("derived", 8, 300): "joint: two fractional lives",
    ("derived", 9, 649): "the primary trigger, the joint annuitant dead with certainty",
    ("derived", 11, 300): "a QLAC at its income start, at its limit",
    ("derived", 13, 120): "the start-date adjustment at t = 0",
    ("derived", 14, 60): "the second slice at t = 0, priced with the n_g column",
    ("derived", 14, 252): "the acceleration's lump sum at t = 0",
    ("derived", 14, 253): "inside the blackout, the lump sum paid before t = 0",
    ("derived", 15, 252): "the commutation at t = 0, with the rate change in its column",
    ("derived", 17, 240): "advance timing at T: the balance at G(m)",
    ("derived", 18, 683): "the table basis on a male life, dp 4: the month before the cap",
    ("derived", 19, 240): "life only on the table basis, RothIRA, at T",
    ("derived", 20, 59): "LO_ROP in deferral",
    ("derived", 21, 253): "the installment refund quarterly in arrears, COLA, commuted",
    ("derived", 22, 250): "the installment refund semi-annual in advance, off its period",
    ("derived", 23, 243): "the cash refund semi-annual in arrears, off its period",
    ("derived", 24, 250): "the period certain annual in arrears, off its period",
    ("derived", 25, 240): "an acceleration in a guarantee, l_last(T) derived at t = 0",
    ("derived", 25, 357): "an acceleration straddling the guarantee's end at t = 0",
    ("derived", 26, 252): "half commuted at t = 0, quarterly in advance, a payment month",
    ("derived", 26, 253): "after it, off its period: the frozen weight, quarterly",
    ("derived", 27, 252): "a commutation month with nothing to commute",
    ("derived", 28, 300): "a female joint annuitant, the younger life",
    ("derived", 29, 649): "the primary trigger, generational, the joint annuitant dead",
    ("derived", 30, 479): "the month before the cap at omega, inside a guarantee",
    ("derived", 31, 500): "both lives dead in a guarantee",
    ("derived", 32, 365): "a QLAC failing every condition, commuting in its derived period",
    ("derived", 33, 31): "after an advancing adjustment: the second slice priced to T'",
    ("derived", 34, 245): "the advance cash refund annual, off its period",
    ("derived", 35, 252): "half commuted at t = 0, accelerating at its guarantee's end",
}
CORE_FUTURES = {
    (1, 1): "the table basis, a month off the valuation anniversaries",
    (8, 12): "joint, on the valuation anniversaries",
    (13, 13): "the start-date adjustment from its own issue",
    (14, 13): "an acceleration from its own issue",
    (15, 13): "a commutation from its own issue, on no rate change",
    (21, 13): "a commuting installment refund, quarterly, COLA",
    (25, 13): "an acceleration in a guarantee from its own issue, l_last(T) derived",
    (30, 13): "a guarantee past the age stop",
}

SEC_FULL = os.environ.get("USLIB_SEC_FULL") == "1"
FULL_ONLY = (pytest.mark.sec_full,
             pytest.mark.skipif(not SEC_FULL, reason="the full splice grid runs with "
                                "USLIB_SEC_FULL=1 (USLIB-SEC-PLAN.md K6)"))

# What the splice sets in S as it is read, before it computes anything, and in SEC alike
# but for the reference rate's change (below).  Expense inflation is the one input DIA
# reads on the valuation clock (D7): S inflates by policy year and SEC by valuation year,
# so at the shipped 2.5% the expenses of a point opened at d differ by design, and at 0
# both factors are 1.  The clock itself is then asserted on its own, at the shipped rate.
# Mortality improvement is calendar-dated, from each contract's issue year, so it moves
# with no clock and is not neutralized.  The rest ship at a value that hides some of the
# state from any comparison, and are set apart: ref_rate_shift ships at 0, which hides the
# change in the commutation discount rate (SWITCHED_ON, the one assumption that ships at
# zero); baa_yield ships so that the repricing rate equals the pricing rate, which would
# hide a mix-up of the two; and mort_ae_factor ships at 1, which hides a dropped factor
# and leaves the cap on mortality idle below the limiting age.  The identity does not
# depend on the values, only on the two models describing the same contract.
SWITCHED_ON = {"ref_rate_shift": 0.005}
SPLICED_REFS = {"inflation_rate": 0.0, "baa_yield": 0.0625, "mort_ae_factor": 1.05,
                **SWITCHED_ON}

# The reference rate's change is S's ref_rate_shift, the change since each S contract's
# own issue, which S applies from month 0 on.  SEC reads the splice's table once, as a
# block is read, on one path of the reference rate, which every point shares (D7).
# Restated in force at d, a point has seen all of S's change by the valuation date and
# carries it in ref_rate_shift_init (the spec's state), and on that path nothing changes
# after it, so SEC's own ref_rate_shift, the change made at the valuation date, is 0
# (SEC_REFS).  Restated to be issued k months on, a point has seen no change by its issue
# date, its column is 0, and sees none after it, so its S twin, the same contract on that
# path, is S read with its ref_rate_shift at 0 (LATER_REFS): the splice reads S twice,
# once for each kind of row.  What SEC's ref_rate_shift moves, each contract on the books
# at the valuation date and no contract issued later, the reference-rate test asserts, on
# one table read at two values, and with the column and the Reference of opposite signs.
SEC_REFS = {**SPLICED_REFS, "ref_rate_shift": 0.0}
LATER_REFS = {**SPLICED_REFS, "ref_rate_shift": 0.0}


def _mortality_apart(df):
    """Every ``(age, sex)`` row of the mortality table apart from every other.

    The shipped rates are band-constant over ages 60 to 84 and the male rates are the
    female rates three years on, so a join on the wrong age or the wrong sex would read
    the same number there, and no comparison with S could see it.  Scaled a little by age
    and by sex.  The factor is kept small on purpose: a steeper one takes the female rate
    past 1 at 118 under the splice's A/E, kills the anchor with certainty before its last
    months, and leaves every row valued after it a contract owing nothing, which
    ``proj_len()`` refuses.
    """
    age, male = df["age"], df["sex"] == "M"
    return df.assign(mort_rate=df["mort_rate"] * (1 + 0.0001 * (age - 40))
                     * male.map({True: 1.004, False: 1.0}))


def _improvement_apart(df):
    """Every ``(age, sex)`` row of the improvement scale apart from every other.

    The shipped scale is the same for both sexes at every age and flat at 0.01 below 86,
    so a join on the wrong sex or the wrong age would read the same number there.  Scaled
    by age and sex, plus a small offset that keeps the scale's zero tail apart without
    lowering old-age mortality enough to move the cap.
    """
    age, female = df["age"], df["sex"] == "F"
    scale = female.map({True: 1.25, False: 1.0})
    offset = female.map({True: 1.5, False: 1.0})
    return df.assign(improvement_rate=df["improvement_rate"] * (1 + 0.004 * (age - 40))
                     * scale + 0.000001 * (age - 39) * offset)


# The edits both copies, S's and SEC's, carry.
SPLICED_EDITS = {"mort_table.csv": _mortality_apart,
                 "improvement_scale.csv": _improvement_apart}

# The opening state, in Data's order, and the cells running in force adds to DIA_US_S's,
# each of which the symbol map must name.
STATE = ("lives_if_init_1", "lives_if_init_2", "cum_premium_pp_init", "annual_income_init",
         "guarantee_mths_pricing_init", "surv_to_payout_init", "commute_weight_init",
         "ref_rate_shift_init")
NEW_CELLS = (
    "policy_count", "duration_mth_init", "t_entry", "stop_mth", "is_active", "pols_if_at",
    "pols_new_biz", "lives_if_init", "cum_premium_pp_init", "annual_income_init",
    "guarantee_mths_pricing_init", "surv_to_payout_init", "commute_weight_init",
    "ref_rate_shift_init", "lives_if_pm", "lives_if_last_pm", "mort_rate_py",
    "mort_rate_mth_py", "mort_rate_base_at", "improvement_rate_at", "premium_pm",
    "cum_premium_payout", "annual_income_payout", "is_payment_pm", "cola_factor_pm",
    "annuity_pp_sched_pm", "certain_floor_pm", "is_trigger_either", "is_life_only",
    "is_cash_refund", "is_installment_refund", "is_period_certain", "is_rop", "is_arrears",
    "is_generational", "is_formula_basis")

# The four roll-forward residuals.  Each is 0 exactly or rounding around 0, and an opening
# state the CSV gives back an ulp off moves one by an ulp of what it closes, so T2 and T3
# compare them at the default absolute floor of 1e-9, in a pass of their own, and every
# other cell with no floor (§5.2).
RESIDUALS = frozenset({"check_lives_roll_fwd_resid", "check_income_roll_fwd_resid",
                       "check_payment_factor_resid", "check_commutation_value_resid"})

# The cells T2 skips beyond T1's, which already drop result_pols (the spec's exempt).
# proj_len counts from the valuation date on SEC and from issue on S, so it differs by d by
# design; frame_mismatches asserts what it must get right, that both frames end at the
# same instant.  payment_surv_mth returns a time point, which on SEC's clock is S's less
# d: payment_factor_life, which reads it, is compared, so a wrong survival point still
# fails.  premium_by_mth and premium_schedule hold the premiums still due, and the
# companion's own row labels, where S's hold the whole schedule: the slices still due are
# compared through premium_pp, purchase_rate and annual_income, and the slices paid through
# the opening state.  result_annual's first row on a row restated mid-year holds part of
# a policy year, and its later rows are compared through the year-keyed cells it reads
# (and by test_result_annual_keeps_the_policy_year_key).  The cells keyed by policy month
# are compared at S's keys unshifted, which are policy months on both sides.  Per case,
# accel_payment_factor too, on a row valued after its acceleration month
# (:func:`_after_the_exercise`).
SPLICE_EXEMPT = (TWIN_EXEMPT_DEFAULT | SPEC.exempt
                 | {"proj_len", "payment_surv_mth", "premium_by_mth", "premium_schedule",
                    "result_annual"})
# A future row holds its whole schedule and whole policy years, which T3 compares; the
# schedule's row labels are still the companion's.
FUTURE_EXEMPT = SPLICE_EXEMPT - {"premium_by_mth", "result_annual"}

# The result_cf columns that expense inflation moves, and the cells they are made of: on
# the committed rows, at the shipped 2.5%, the only places a row in force departs from S.
INFLATED = ("expenses", "liability_cf", "net_cf")
INFLATION_CELLS = frozenset({"inflation_factor", "expenses", "liability_outgo",
                             "liability_cf", "net_cf", "result_cf"})

# The decrement rates keyed by month, none of which may be evaluated before issue (R1,
# D4), and the two age-keyed table readers, which may not be read below an issue age.
DECREMENT_RATES = ("mort_rate", "mort_rate_mth", "mort_rate_base", "improvement_rate")
AGE_READERS = ("mort_rate_base_at", "improvement_rate_at")

# The label accessors, DIA_US_S's, which no projection cell calls and the sweep calls, so
# that T2 compares them with S's.
LABELS = ("reduction_trigger", "market_type", "income_form", "payout_form", "db_form",
          "payment_timing", "mort_basis", "factor_basis")

# The cells that scale with policy_count.  Every other cell is a per-contract amount, a
# probability, a rate, a clock or a flag, and must not move when the count does.
# result_annual is both: its claims and income columns are counted, its age, premium,
# CP, B and survival columns are per contract.
COUNTED = frozenset({
    "policy_count", "pols_if_init", "pols_if", "pols_if_at", "pols_new_biz", "premiums",
    "annuity_payments", "claims", "commutations", "expenses", "liability_outgo",
    "liability_cf", "net_cf", "claims_ann", "annuity_payments_ann", "result_cf",
    "result_pols", "result_annual", "check_commutation_value_resid"})
ANNUAL_COUNTED = ("claims_death", "claims_refund", "annuity_payments")

# result_pols' columns, in its order: the count on the books weighted by survival and the
# contracts issued in the month, then S's other seven columns in S's order, which no count
# moves.
RESULT_POLS = ["pols_if", "pols_new_biz", "lives_if_1", "lives_if_2", "lives_if_last",
               "lives_death_last", "certain_floor", "payment_factor_life", "payment_factor"]
RATES = RESULT_POLS[2:]

# BasicTerm_SE's two timings, which running in force adds (S has none), and the two kinds.
TIMINGS = ("BEF_NB", "BEF_DECR")
KINDS = ("DEATH", "REFUND")

# What each monthly cell holds outside cover, before issue and from the stop rule on, as
# its docstring says: no count, so no cash flow; no premium, no instalment, no payment
# factor, no refund and no commutation; no question about the contract answered yes; and a
# COLA factor that moves nothing.  The type is part of the value: an amount, a probability
# or a rate is a float in every branch and a flag a bool, because Phase 2 types a cell by
# the values it returns (USLIB-SEC-PLAN.md F3).  The guard test also calls each of
# PER_LIFE for every covered life, pols_if_at at each timing, and claim_pp and claims at
# each kind, all 0.0, and before issue the time-point cells of BEFORE_ISSUE, lives_if for
# both lives among them; and phase, PRE_ISSUE before issue and TERMINATED from the stop
# rule on, each label passed through _code, as Phase 2's int codes will be.
OUTSIDE_COVER = {
    "is_active": False, "is_payout": False, "is_payment_mth": False,
    "accel_blackout": False, "premium_pp": 0.0, "cum_premium_pp": 0.0,
    "annual_income": 0.0, "annuity_pp_sched": 0.0, "annuity_pp": 0.0,
    "annuity_pp_paid": 0.0, "lives_death_last": 0.0, "certain_floor": 0.0,
    "payment_factor_life": 0.0, "payment_factor": 0.0, "refund_balance": 0.0,
    "accel_payment_factor": 0.0, "commute_frac_cum": 0.0, "commute_weight": 0.0,
    "commuted_value": 0.0, "commutations": 0.0, "annuity_payments": 0.0,
    "premiums": 0.0, "pols_if": 0.0, "pols_new_biz": 0.0, "expenses": 0.0,
    "liability_outgo": 0.0, "liability_cf": 0.0, "net_cf": 0.0,
    "check_payment_factor_resid": 0.0, "check_income_roll_fwd_resid": 0.0,
    "check_commutation_value_resid": 0.0, "cola_factor": 1.0}
PER_LIFE = ("mort_rate_base", "improvement_rate", "mort_rate", "mort_rate_mth",
            "lives_death")
BEFORE_ISSUE = {"lives_if_last": 0.0, "check_lives_roll_fwd_resid": 0.0}

# The valuation-clock cells a month outside cover may not reach: the attained age and the
# calendar year.  The rates that read them hold 0.0 outside cover by their own guards,
# which the guard test asserts first; these have none, and no formula may reach them
# there, nor a caller (USLIB-SEC-PLAN.md F4).  The age readers and the annual rate by
# policy year are not among them: an installment refund's stop rule searches its payout
# schedule, which prices its premiums, so they are read on the policy clock from issue on
# every point, in cover or not, and :func:`_contract` bounds their keys instead.
IN_COVER_ONLY = ("age", "calendar_year")

INFLATION = 0.025       # the shipped inflation_rate, which the inflation test reads

# The recursion limit, as mx.set_recursion takes it, under which the committed points are
# first swept (R2, F7).  A limit of n admits a call n + 1 cells deep, counted as modelx's
# stack trace counts them.  A report evaluates each column in ascending t, so a forward
# recursion, through t - 1, finds the month before already cached: the committed points'
# sweep needs a limit of 15, and 14 fails on the installment refund's twin, whose refund
# period is searched over its payout schedule (measured at M12).  The instalments scheduled
# to date are based at the valuation date's policy month, so the anchor in its last month
# reads them without recursing back to its income start month, 478 months earlier; and a
# backward recursion over a frame longer than a month needs a limit of hundreds.
CALL_DEPTH = 40

# How deep a cold call may run beyond its chain, one cell a month from its month back to
# t_entry (D5).  Three cells recurse a month at a time, each life's survival on every
# point, the premiums paid and the income bought, and the longest of them, survival, sets
# the depth: 726 to 728 levels on the 720-month twins.  Beyond the chain are the cells
# above it, from net_cf down, and below it the first month's rates, the age readers, the
# count cells that check their tables and Data's first reads of its tables: measured by
# modelx's stack trace at 7 to 9 levels on the committed points, 12 on the anchor's
# one-row frame in its last month, and 7 at the contract's longest cover, 1,176 months from
# issue age 22, which runs 1,182 cells deep issued at the valuation date and 120 months on
# (M12).  A chain of two cells a month doubles the depth, and needs twice the stack
# compiled.
CHAIN_OVERHEAD = 16

# How deep a cold net_cf(0) may run.  The first month reads the cohort that reaches the
# income phase, l_last(T), only where a certain floor pays it, and on the installment
# refund prices its premiums and searches its payout schedule for its stop rule, by loops
# (lives_if_pm, annuity_factor, the payout income); so a cold first month runs 12 or 13
# cells deep on the committed points, 21 on the installment refund's twin and 8 on the
# point issued later (10 before Data's table is read, where this test reads it first),
# where DIA_US_S's runs 251 on point 1 and 311 on point 13, reading l_last(T) in every
# month through its survival recursion to the income start month (M12).
FIRST_MONTH_DEPTH = 32

# The product's youngest issue age (product-spec), from which the longest cover runs to the
# age stop.  The shipped tables start at 20, so the depth test needs no extended table.
CONTRACT_MIN_AGE = 22

REPORTS = ("result_cf", "result_pols")


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

    ``month`` is the row's ``source_mth``: 0 for a twin, ``d`` for a derived row, ``-k``
    for a future one.  The twins keep S's ``point_id`` and ``policy_id``, so the S policy
    is the twin's.
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


def _source(s_model, table, point_id):
    """The ItemSpace of the S point that row ``point_id`` of ``table`` was made from.

    Found by the row's ``source_policy_id`` among the S table's ``policy_id`` s, so that no
    numbering of either table is assumed.
    """
    s_table = s_model.Data.model_point_table()
    hit = s_table.index[s_table["policy_id"] == table.at[point_id, "source_policy_id"]]
    assert len(hit) == 1, (point_id, hit.tolist())
    return _point(s_model, hit[0])


def _release(model, key, collect=False):
    """Drop the ItemSpace at ``key``, the registry's key, and every value it has cached.

    A projected point holds its cached values and their dependency graph, and the splice's
    rows and the scaled and extract copies' points are each needed once, so each is
    released when read, as ``run_sec.py --block`` releases its points (USLIB-SEC-PLAN.md
    F5): held together they would raise this module's memory by a gigabyte.  Asked for
    again, the ItemSpace is made afresh and recomputes.  With ``collect``, the collector
    runs at once, as it does for each splice row.  That costs little, because the swept
    models the module holds are frozen out of the collector (:func:`_freeze`), so the
    collection scans only what the row made.
    """
    del model.Projection[key]
    if collect:
        gc.collect()


def _freeze():
    """Collect what is garbage, then freeze everything still alive out of the collector.

    Each module fixture that sweeps a model calls this once its sweep is done, so that the
    collections after it, automatic or :func:`_release`'s, no longer scan the millions of
    objects a swept model holds.  The collection first means no garbage is frozen with
    them.  The freeze is undone as the module ends (:func:`_collector`).
    """
    gc.collect()
    gc.freeze()


def _refreeze():
    """Return what is frozen to the collector, collect its garbage, and freeze the rest.

    An ItemSpace released after its model was frozen (:func:`_freeze`) leaves its cycles in
    the frozen generation, where no collection reaches them: the splice's S points, swept
    and frozen in the fixture, released one by one in T2.  Called once, after the last T2
    case, it frees them, at the cost of one full collection.
    """
    gc.unfreeze()
    gc.collect()
    gc.freeze()


def _committed():
    """The committed SEC table as the file holds it, unvalidated, indexed by point_id."""
    return pd.read_csv(model_path(SEC).parent / TABLE, index_col="point_id")


def _committed_schedule():
    """The committed premium schedule as the file holds it, unvalidated, on a default
    index."""
    return pd.read_csv(model_path(SEC).parent / SCHEDULE)


def _sec_inputs(tmp_path, table, edits=None, schedule=None):
    """A copy of the product directory whose SEC table is ``table``; its SEC folder.

    ``schedule``, a premium schedule on a default index, is written over the copy's
    ``premium_schedule_sec.csv``; without it the copy holds the committed one, which names
    the committed table's points.  ``edits`` go to ``sec_support.temp_inputs``.
    """
    edits = dict(edits or {})
    if schedule is not None:
        edits[SCHEDULE] = schedule
    return temp_inputs(tmp_path, model_path(SEC), model_points=table,
                       model_point_file=TABLE, edits=edits)


def _read_edited(tmp_path, edit=None, tag="edited", refs=None, schedule_edit=None):
    """DIA_US_SEC read from a copy whose SEC table is ``edit(_committed())``, and whose
    premium schedule is ``schedule_edit(_committed_schedule())``."""
    table = (edit or (lambda t: t))(_committed())
    schedule = schedule_edit(_committed_schedule()) if schedule_edit else None
    return _read(_sec_inputs(tmp_path, table, schedule=schedule), tag, refs)


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


def _moved(point, month, **columns):
    """An edit that moves row ``point`` to policy month ``month`` and sets ``columns``."""
    def edit(table):
        table = _set("duration_mth", [point], month)(table)
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
    """The argument that selects timing or kind ``label``: at stage ``"E"``, the string.

    The conventions' lookup (``test_model_conventions._timing``), on ``Projection`` or any
    of its ItemSpaces, which see its References: Phase 2 turns the timing and kind strings
    into int References of the same names (R9), and this passes whichever the model
    defines, so the calls below read the same at both stages.
    """
    value = space.refs.get(label)
    return value if isinstance(value, int) else label


def _mismatches(s_proj, sec_proj, **kwargs):
    """:func:`sec_support.twin_mismatches`, the one place this module calls it.

    It passes the SEC Space's :func:`sec_support.codes`, which map S's timing and kind
    strings to the int codes Phase 2 gives them.  At stage ``"E"`` there are none, and the
    codes are ``{}``; every comparison goes through here, so each takes Phase 2's codes when
    they come.
    """
    return twin_mismatches(s_proj, sec_proj, codes=codes(sec_proj), **kwargs)


def _lives(x):
    return (1, 2) if x.is_joint() else (1,)


def _sweep(proj):
    """Evaluate on an S point or an SEC row what the splice compares: the reports and more.

    ``result_cf()``, ``result_pols()`` and ``result_annual()``, and every ``check_*``, the
    survival check among them, which here restates the recursion a month at a time and so
    costs a cell a month.  Then the cells no report or check reaches, so that the
    comparisons see them too: ``guarantee_yrs``, ``qlac_flags``, ``accel_cost``,
    ``payout_factor_calc``, ``other_qlac_premium``, ``is_qlac`` and the label accessors,
    each covered life's ``sex``; over the frame ``phase``, ``duration_mth``,
    ``cola_factor`` and, in a blackout month, ``accel_payment_factor``; and over the months
    on the books, where a contract has an attained age, the calendar year and, for each
    covered life, the attained age, the base-table rate, the improvement rate and the
    deaths.  An S point is swept the same way, so what it caches is what T2 compares.
    """
    proj.result_cf()
    proj.result_pols()
    proj.result_annual()
    for name in proj.cells:
        if name.startswith("check_") and not name.endswith("_resid"):
            proj.cells[name]()
    for name in ("guarantee_yrs", "qlac_flags", "accel_cost", "payout_factor_calc",
                 "other_qlac_premium", "is_qlac", *LABELS):
        proj.cells[name]()
    lives = _lives(proj)
    for life in lives:
        proj.sex(life)
    entry = proj.t_entry() if "t_entry" in proj.cells else 0
    for t in range(proj.proj_len()):
        proj.phase(t)
        proj.duration_mth(t)
        proj.cola_factor(t)
        if proj.accel_blackout(t):
            proj.accel_payment_factor(t)
        if t < entry:
            continue
        proj.calendar_year(t)
        for life in lives:
            proj.age(t, life)
            proj.mort_rate_base(t, life)
            proj.improvement_rate(t, life)
            proj.lives_death(t, life)


def _after_the_exercise(p):
    """``{"accel_payment_factor"}`` on a row valued after its acceleration month, else
    nothing: the cell T2 exempts on that row.

    ``DIA_US_S`` reads the factor only in the exercise month, for the five instalments the
    lump sum pulls forward, and caches it at their months.  A row valued after the exercise
    paid the lump sum before the valuation date, its blackout months pay nothing, and from
    the valuation date on nothing reads the factor, which is 0.0 there; so S's cached
    values have no counterpart (``test_an_acceleration_needs_no_column``).
    """
    a = p.accel_mth()
    return {"accel_payment_factor"} if 0 <= a < p.duration_mth_init() else set()


def _years_on_the_books(month):
    """The ``arg_map`` for S's year-keyed display cells on a row restated at S month
    ``month``.

    ``lives_if_ann(y)`` and ``annuity_payments_ann(y)`` read the survival at the end of
    policy year ``y``, which a year that ended before the valuation date does not have on
    the valuation clock, so those keys are skipped; ``claims_ann(y, kind)`` sums the months
    of policy year ``y`` on the books, so a year begun before the valuation date is a part
    year here and skipped too.  Every other key, and every key of a future row, is a whole
    year on the books and compared.
    """
    def arg_map(name, args):
        if name in ("lives_if_ann", "annuity_payments_ann") and 12 * args[0] < month:
            return None
        if name == "claims_ann" and 12 * (args[0] - 1) < month:
            return None
        return args
    return arg_map


def _compared(s_proj, sec_proj, month, exempt):
    """Where row ``sec_proj``, restated at S month ``month``, departs from S cell by cell.

    In two passes (§5.2): every cell of S's but ``exempt``, :data:`RESIDUALS` and the cell
    :func:`_after_the_exercise` names, at every argument S cached inside its frame from
    month ``month`` on, to 1e-9 relative with no absolute floor; then the residuals alone,
    at the default floor of 1e-9.  The year-keyed display cells are compared on the years
    on the books (:func:`_years_on_the_books`).
    """
    exempt = exempt | _after_the_exercise(sec_proj)
    arg_map = _years_on_the_books(month)
    found = _mismatches(s_proj, sec_proj, t_offset=month, exempt=exempt | RESIDUALS,
                        arg_map=arg_map, atol=0.0)
    return found + _mismatches(s_proj, sec_proj, t_offset=month,
                               exempt=exempt | (set(s_proj.cells) - RESIDUALS),
                               arg_map=arg_map)


def _continues_s(s_proj, sec_proj, month, exempt=SPLICE_EXEMPT):
    """Where a committed row departs from S's point ``s_proj`` from S month ``month`` on.

    The splice's comparison, on the committed model at the shipped assumptions: frame by
    frame, ``result_cf`` and ``result_pols``, then cell by cell over every cell of S's but
    ``exempt`` (:func:`_compared`), :data:`SPLICE_EXEMPT` on a row restated in force and
    :data:`FUTURE_EXEMPT` on one issued later.  The shipped 2.5% expense inflation steps by
    policy year in S and by valuation year here (D7), so :data:`INFLATED`'s three columns,
    and :data:`INFLATION_CELLS`, differ by design and are left out; the inflation test holds
    them.  Every other column and cell must agree, to 1e-9 with no absolute floor.
    """
    s_df = s_proj.result_cf()
    keep = [c for c in s_df.columns if c not in INFLATED]
    found = frame_mismatches(s_df, sec_proj.result_cf(), t_offset=month, columns=keep,
                             atol=0.0)
    found += frame_mismatches(s_proj.result_pols(), sec_proj.result_pols(),
                              t_offset=month, atol=0.0)
    return found + _compared(s_proj, sec_proj, month, exempt | INFLATION_CELLS)


def _case_id(kind, s_point, month):
    """A case's id: ``point14-d59``, or ``point8-k13`` if it is issued later."""
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
# default run's among them.
GRID = (*SPLICES, *IN_FORCE_TWINS, *(("future", p, -k) for p, k in FUTURES))
CORE_GRID = frozenset({*CORE_SPLICES, *(("future", p, -k) for p, k in CORE_FUTURES)})

# This run's T2 cases, in the order they run, the last of them for each S point, after which
# that point's swept S ItemSpace is released, and the last of all, after which what the
# releases left is collected (:func:`_refreeze`).
T2_CASES = tuple(_selected(SPLICES + IN_FORCE_TWINS, CORE_SPLICES))
LAST_OF_POINT = {case[1]: case for case in T2_CASES}


def _s_table_with_variants():
    """S's committed table with the :data:`VARIANTS` appended, under their own point_ids."""
    table = pd.read_csv(model_path(TWIN).parent / "model_point_table.csv",
                        index_col="point_id")
    rows = []
    for point_id, (base, changes) in VARIANTS.items():
        row = table.loc[[base]].assign(**changes)
        row.index = pd.Index([point_id], name="point_id")
        rows.append(row)
    return pd.concat([table, *rows])


def _s_schedule_with_variants(schedule):
    """S's premium schedule with each variant's premiums, its base's rows under its own
    point_id."""
    rows = [schedule[schedule["point_id"] == base].assign(point_id=point_id)
            for point_id, (base, _) in VARIANTS.items()]
    return pd.concat([schedule, *rows], ignore_index=True)


def _s_copy(root):
    """A copy of S's product directory with the variants and the splice's edits; S's
    folder in it."""
    return temp_inputs(root, model_path(TWIN), model_points=_s_table_with_variants(),
                       edits={**SPLICED_EDITS,
                              "premium_schedule.csv": _s_schedule_with_variants})


def _sec_built(root, s, derived=(), future=(), edits=None):
    """SEC's inputs for a table the generator builds from S model ``s``: its folder.

    The registered spec with its rows replaced by ``derived`` and ``future``, built from
    ``s`` (``sec_support.build_sec_table``), written with its premium schedule into a copy
    of the product directory, with ``edits`` beside them.
    """
    spec = dataclasses.replace(SPEC, derived=tuple(derived), future=tuple(future))
    table, companions = build_sec_table(spec, s)
    assert set(companions) == {SCHEDULE}
    return temp_inputs(root, model_path(SEC), model_points=table, model_point_file=TABLE,
                       edits={**(edits or {}), **companions})


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
    """DIA_US_SEC read in place, as committed, and swept once, cold; what it met.

    The model is first asked for ``duration_mth(500)`` on the twin of S point 2, and the
    keys that call leaves in ``duration_mth`` are kept.  Then every committed point is
    swept (:func:`_sweep`), in table order and each column in ascending ``t``, under a
    recursion limit lowered to :data:`CALL_DEPTH`, and whatever that raises is kept, point
    by point, rather than raised.  So the record says what a cold model does, which the
    clock and depth test asserts (D3, R2), and every test on the committed model reads a
    model already swept: the sweep is paid once, not once for each.  The swept model is
    then frozen out of the collector (:func:`_freeze`).  Returns ``(model, record)``.
    """
    model = _read(model_path(SEC), "sec")
    first = _row(model, "twin", 2, 0)
    record = {"duration_mth(500)": first.duration_mth(500),
              "keys": list(first.cells["duration_mth"].keys()), "deep": []}
    labels = model.Data.model_point_table().index
    limit = mx.get_recursion()
    mx.set_recursion(CALL_DEPTH)
    try:
        for key, point_id in zip(point_keys(model), labels):
            try:
                _sweep(projection(model, key))
            except Exception as err:            # kept, so every point is swept
                record["deep"].append(f"point {point_id}: the sweep raised {_raised(err)}")
    finally:
        mx.set_recursion(limit)
    _freeze()
    yield model, record
    model.close()


@pytest.fixture(scope="module")
def sec_model(sec_read):
    """DIA_US_SEC read in place, as committed, with every point swept (sec_read)."""
    return sec_read[0]


@pytest.fixture(scope="module")
def s_model():
    """DIA_US_S read in place, as committed, with every point swept (:func:`_sweep`).

    T6 regenerates the SEC table and its premium schedule from it, which would otherwise
    project every S point again (USLIB-SEC-PLAN.md §4, *Carried into Phase 1*), and the
    in-force tests read S's months off it.  The swept model is then frozen out of the
    collector (:func:`_freeze`).
    """
    model = mx.read_model(model_path(TWIN), name=_name("s"))
    for key in point_keys(model):
        _sweep(projection(model, key))
    _freeze()
    yield model
    model.close()


@pytest.fixture(scope="module")
def spliced(tmp_path_factory):
    """S and SEC on the splice's inputs: ``(s, sec, s_later, events, every)``.

    S is read from a copy of the product directory whose table has the variants appended,
    whose premium schedule has their premiums, and whose mortality table and improvement
    scale are set apart (:data:`SPLICED_EDITS`), under :data:`SPLICED_REFS`, and every S
    point is swept (:func:`_sweep`) and stays swept.  SEC runs on the same assumption
    tables, and on a model point table and a premium schedule of its own, built by the
    generator from the registered spec with its rows replaced by the cases this run
    selects, the core or the full grid (:func:`_selected`), out of this S model, so each
    row opens with the state of the very run it is compared with.  SEC reads the table
    once, under :data:`SEC_REFS`, as a block is read, on one path of the reference rate,
    and each SEC row is projected by the case that compares it and released once compared.
    A row issued later is compared with ``s_later``, S read again from the same copy under
    :data:`LATER_REFS`, the same contract on that path; each of its points is swept by the
    T3 case that compares it and released with the row, so that ``s_later`` holds at most
    one swept point at a time.  The rows the product's own tests read on the splice's inputs
    (:data:`EVENT_ROWS`) are built into a table of their own from the same swept S model, in
    the folder ``events``, which the ``events`` fixture reads, so that no S point is
    projected again for them; and so are the states the every-state test restates,
    ``every`` (:func:`_every_state_table`), whose S points T2 releases before that test
    runs.

    Everything alive once S is swept, S's points among them, is then frozen out of the
    collector (:func:`_freeze`), so that the collection after each row's release scans only
    what the row made, not the swept S model the module holds.  Each S point is held swept
    until the last T2 case that compares a row of it, and released then, and once the last
    T2 case has run, what the releases left is returned to the collector and collected
    (:func:`_refreeze`): held to the end of the module, the swept S model would add 1.5 GB
    to it, under the two committed models' sweeps (measured at M12).
    """
    root = tmp_path_factory.mktemp("spliced")
    s_folder = _s_copy(root / "s")
    s = _read(s_folder, "s_spliced", SPLICED_REFS)
    for key in point_keys(s):
        _sweep(projection(s, key))
    derived = [(p, d) for kind, p, d in _selected(SPLICES, CORE_SPLICES)]
    sec_folder = _sec_built(root / "sec", s, derived, _selected(FUTURES, CORE_FUTURES),
                            SPLICED_EDITS)
    events = _sec_built(root / "events", s, EVENT_ROWS, EVENT_FUTURES, SPLICED_EDITS)
    every = _every_state_table(root / "every", s, SPLICED_EDITS)
    sec = _read(sec_folder, "sec_spliced", SEC_REFS)
    s_later = _read(s_folder, "s_spliced_later", LATER_REFS)
    _freeze()
    yield s, sec, s_later, events, every
    s_later.close()
    sec.close()
    s.close()


@pytest.fixture(scope="module")
def splice_records():
    """What each splice row was found to do, by case (:func:`_record`)."""
    return {}


# The rows the product's own tests read on the splice's inputs, whatever the grid: around
# the acceleration of point 14 and the commutation of point 15 and its variants, the income
# start of point 7, the month before each cap binds, the generational point in payout, the
# COLA cash refund past its first COLA anniversary, its refund still running, the anchor on
# an anniversary, and the anchor issued 13 months on.
EVENT_ROWS = ((1, 12), (7, 240), (8, 647), (10, 265), (14, 251), (14, 252), (14, 253),
              (15, 240), (15, 251), (15, 252), (15, 253), (15, 360), (16, 240), (18, 683),
              (21, 252), (26, 250), (26, 252), (30, 479), (32, 365), (32, 390), (35, 252))
EVENT_FUTURES = ((1, 13),)


@pytest.fixture(scope="module")
def events(spliced):
    """SEC on the splice's inputs, its table the generator's for :data:`EVENT_ROWS`.

    Built by the ``spliced`` fixture from the splice's S model, swept, and read under
    :data:`SEC_REFS`, as the splice's own table is, so each row opens with the state of the
    very run it is compared with.  Each test projects the rows it reads and releases them.
    """
    sec = _read(spliced[3], "events", SEC_REFS)
    yield sec
    sec.close()


# ---------------------------------------------------------------------------
# The splice's records
#
# Each T2 and T3 case sweeps its row, records what the rules test and the core grid's reach
# need of it, compares it with S, and releases it: held together, the rows of the full grid
# would hold several gigabytes.  The record is made before the comparison, because the
# comparison evaluates SEC's cells at S's own cached arguments, and those include keys SEC
# never reads itself: S's instalments scheduled to date from policy month 0, S's pricing at
# the premium months already paid, S's survival from issue.  Comparing them would plant
# those keys in SEC's cache, for the rules test to report as SEC's.  So each of the two
# tests reads the records, and computes any case no earlier test has recorded, which keeps
# it whole when run alone.


def _cached_args(cells):
    """The argument tuple of every key ``cells`` has cached (:func:`sec_support._args`)."""
    n = len(cells.parameters)
    return [() if n == 0 else (key,) if n == 1 else tuple(key)
            for key in list(cells.keys())]


def _month(x):
    return isinstance(x, int) and not isinstance(x, bool)


def _contract(p):
    """The arguments each policy-clock and age-keyed cell may take on row ``p``.

    ``({cell: (lowest, highest)}, {life: (lowest age, highest age)})``.  The policy clock
    runs from issue to the stop rule, ``stop_mth()``, and a little past it, where an
    acceleration in a contract's last months pulls five instalments forward, and the
    pricing kernel reads survival to the mortality horizon, ``horizon_mths()``: so the
    pricing survival, the schedule by policy month, its payment months, COLA and certain
    floor are read at policy months 0 to the later of the two, ``reach``, and the annual
    rate at policy years 1 to ``reach``'s.  The premiums and the pricing of each premium
    at policy months 0 to ``stop_mth() - 1``, the pricing curve's last-survivor exposure
    from issue to the later income start month, and the instalments scheduled to date from
    the month before the income start month in force to the later of the horizon and the
    last month.  The year-keyed display cells at the policy years of the frame, from the
    valuation date's.  The age readers are read for a covered life at ages from its issue
    age to the last below omega: at and above it the rate cells answer without them.  Each
    is a function of the point, so the ranges hold on every row, in force or not.
    """
    stop, horizon = p.stop_mth(), p.horizon_mths()
    start = p.income_start_mth()
    reach = max(horizon, stop + p.accel_months - 1)
    years = (reach - 1) // 12 + 1
    first = p.duration_mth(p.t_entry()) // 12 + 1
    lives = (1, 2) if p.is_joint() else (1,)
    ages = {life: (p.age_at_entry(life), p.omega_age - 1) for life in lives}
    ranges = {name: (0, stop - 1) for name in (
        "premium_pm", "income_start_mth_at", "deferral_yrs", "surv_to_income_start",
        "rop_factor_calc", "rop_factor", "annuity_factor_def", "purchase_rate")}
    ranges.update({name: (0, reach) for name in (
        "lives_if_pm", "is_payment_pm", "cola_factor_pm", "annuity_pp_sched_pm",
        "certain_floor_pm")})
    ranges.update({"mort_rate_py": (1, years), "mort_rate_mth_py": (1, years),
                   "lives_if_last_pm": (0, max(start, p.income_start_mth_init())),
                   "cum_annuity_pp": (start - 1, max(horizon, stop - 1))})
    ranges.update({name: (first, stop // 12) for name in (
        "lives_if_ann", "claims_ann", "annuity_payments_ann")})
    return ranges, ages


def _outside_contract(p):
    """Each cached argument of a policy-clock or age-keyed cell not in :func:`_contract`."""
    ranges, ages = _contract(p)
    found = []
    for name, (lo, hi) in ranges.items():
        found += [f"{name}{args}, outside {lo}..{hi}"
                  for args in _cached_args(p.cells[name])
                  if not (_month(args[0]) and lo <= args[0] <= hi)]
    for name in AGE_READERS:
        for args in _cached_args(p.cells[name]):
            x, life = args
            if life not in ages or not ages[life][0] <= x <= ages[life][1]:
                found.append(f"{name}{args}, outside ages {ages}")
    return found


def _month_of(node):
    """The month a precedent ``node`` is keyed by, its ``t``, or None if it takes none."""
    params = getattr(node.obj, "parameters", None) or ()
    u = node.args[params.index("t")] if "t" in params else None
    return u if _month(u) else None


def _months_read(node, reach):
    """The calls keyed by a month that precedent ``node`` reads, as ``(text, month)``.

    ``node`` itself if it is keyed by ``t``.  Otherwise every month-keyed call its own
    precedents read, followed through every call keyed by no month, such as
    ``surv_to_payout()`` or ``certain_mths_refund()``, as far as the dependency graph
    goes: so a read that looks ahead through a cell taking no ``t`` is the reader's.
    ``reach`` holds what each call keyed by no month reads, so that each is walked once a
    row, and the walk is a loop, not a recursion, since a schedule summed by policy month
    can be hundreds of calls deep.
    """
    month = _month_of(node)
    if month is not None:
        return {(f"{node.obj.name}{node.args}", month)}
    top = (id(node.obj), node.args)
    stack, seen = [(node, False)], set()
    while stack:
        here, done = stack.pop()
        key = (id(here.obj), here.args)
        if key in reach:
            continue
        if done:
            found = set()
            for pred in here.preds:
                month = _month_of(pred)
                if month is not None:
                    found.add((f"{here.obj.name}{here.args} -> {pred.obj.name}{pred.args}",
                               month))
                elif "t" not in (getattr(pred.obj, "parameters", None) or ()):
                    found |= reach[(id(pred.obj), pred.args)]
            reach[key] = found
            continue
        if key in seen:
            continue
        seen.add(key)
        stack.append((here, True))
        for pred in here.preds:
            if _month_of(pred) is None and (id(pred.obj), pred.args) not in reach:
                if "t" not in (getattr(pred.obj, "parameters", None) or ()):
                    stack.append((pred, False))
    return reach[top]


def _rule_breaches(proj):
    """R1, R1a and R2 on one row, once it has been swept.

    ``{"negative": [...], "early": [...], "ahead": [...], "outside": [...]}``: every cached
    call with a negative argument; every call keyed by a month before ``t_entry()`` that a
    call keyed by a month at or after it reads; every call keyed by a month beyond ``t + 1``
    that a call keyed by ``t`` reads; and every policy-clock or age argument the contract
    does not have (:func:`_contract`).  A call reads its precedents, as modelx's dependency
    graph records them, and, through a precedent keyed by no month, whatever that
    precedent reads in turn (:func:`_months_read`): ``payment_factor(t)`` reading
    ``surv_to_payout()``, which reads ``lives_if_last`` at the income start month, reads
    that month.  DIA admits no look-ahead at all.
    """
    entry = proj.t_entry()
    negative, early, ahead = [], [], []
    reach = {}
    for name, cells in proj.cells.items():
        t_pos = cells.parameters.index("t") if "t" in cells.parameters else None
        for args in _cached_args(cells):
            if any(_month(a) and a < 0 for a in args):
                negative.append(f"{name}{args}")
            if t_pos is None:
                continue
            t = args[t_pos]
            for node in cells.preds(*args):
                if _month_of(node) is None and "t" in (
                        getattr(node.obj, "parameters", None) or ()):
                    continue
                for read, u in sorted(_months_read(node, reach)):
                    if u < entry <= t:
                        early.append(f"{name}{args} -> {read}")
                    if u > t + 1:
                        ahead.append(f"{name}{args} -> {read}")
    return {"negative": negative, "early": early, "ahead": ahead,
            "outside": _outside_contract(proj)}


def _step(x):
    """The months from one instalment to the next on row ``x``."""
    return 12 // x.payment_freq()


def _off_period(x):
    """Whether row ``x`` is valued between two of its instalment dates, off its period:
    its months from the income start month to the valuation date are not a whole number of
    payment steps."""
    return (x.duration_mth_init() - x.income_start_mth()) % _step(x) != 0


def _refund_form(x):
    return x.is_cash_refund() or x.is_installment_refund()


# What test_the_core_grid_reaches_every_branch asks of the core's rows in the model's own
# values, which no column of the table shows: each holds of some core row, or of a core row
# in some month of its frame.  At the valuation date, every opening-state column in use, at
# every value it takes: two fractional lives, one life of a joint contract dead, every life
# dead inside a guarantee, the guarantee-period column pricing a premium still due and an
# adjustment still to come, each frozen weight read where it weighs an instalment, and a
# change in the reference rate already seen, on a point whose commutation it discounts;
# then what falls at t = 0 because of where the contract stands: a premium, the
# adjustment, the lump sum, a blackout month, the commutation and one with nothing to
# commute, the income start, a refund, the advance refund balance, a payment month off
# monthly and a month between instalments.  Later in the frame, every branch of the refund,
# the derived and elected guarantees, the commutation and the acceleration, each valued
# off its period where its frequency is below monthly (a row valued on its period would
# hide a payment month counted from the wrong clock), the cap below omega, omega inside a
# guarantee, a QLAC complying and each of the six conditions a QLAC fails, and a slice
# priced to an adjusted income start month.
AT_VALUATION = {
    "two fractional lives": lambda x: (
        x.is_joint() and 0.0 < x.lives_if_init(1) < 1.0 and 0.0 < x.lives_if_init(2) < 1.0),
    "one life of a joint contract dead": lambda x: (
        x.is_joint() and (x.lives_if_init(1) == 0.0) != (x.lives_if_init(2) == 0.0)),
    "every life dead in a guarantee": lambda x: (
        x.lives_if_last(0) == 0.0 and x.certain_floor(0) == 1.0),
    "the n_g column pricing a premium still due": lambda x: (
        _refund_form(x) and x.is_formula_basis() and x.duration_mth_init() > 0
        and any(k >= x.duration_mth_init() for k in x.premium_by_mth())),
    "the n_g column pricing an adjustment still to come": lambda x: (
        _refund_form(x) and 0 < x.duration_mth_init() <= x.adjust_mth()),
    "l_last(T) from the column weighting a guarantee": lambda x: (
        x.duration_mth_init() > x.income_start_mth() and x.certain_floor(0) == 1.0),
    "l_last(T) derived at t = 0, weighting a guarantee": lambda x: (
        x.duration_mth_init() == x.income_start_mth() and x.certain_mths_eff() > 0),
    "l_last(T) derived ahead of t = 0, weighting a guarantee": lambda x: (
        0 < x.duration_mth_init() < x.income_start_mth() and x.certain_mths_eff() > 0),
    "l_last(t_c) from the column": lambda x: (
        0 <= x.commute_mth() < x.duration_mth_init() and x.commute_weight(0) > 0.0),
    "a rate change seen, on a commuting point": lambda x: (
        x.ref_rate_shift_init() != 0.0 and x.duration_mth_init() <= x.commute_mth()
        and x.commuted_value(x.commute_mth() - x.duration_mth_init()) > 0.0),
    "a premium at t = 0": lambda x: x.duration_mth_init() > 0 and x.premium_pp(0) > 0.0,
    "the adjustment at t = 0": lambda x: x.duration_mth(0) == x.adjust_mth(),
    "the lump sum at t = 0": lambda x: x.duration_mth(0) == x.accel_mth(),
    "a blackout month at t = 0": lambda x: x.accel_blackout(0),
    "the commutation at t = 0": lambda x: (
        x.duration_mth(0) == x.commute_mth() and x.commuted_value(0) > 0.0),
    "a commutation month with nothing to commute": lambda x: (
        x.duration_mth(0) == x.commute_mth() and x.commuted_value(0) == 0.0),
    "the income start month at t = 0": lambda x: (
        x.duration_mth(0) == x.income_start_mth()),
    "a refund at t = 0": lambda x: x.claims(0, _code(x, "REFUND")) > 0.0,
    "the advance refund balance at t = 0": lambda x: (
        not x.is_arrears() and x.is_payment_mth(0)
        and x.claims(0, _code(x, "REFUND")) > 0.0),
    "a payment month at t = 0, off monthly": lambda x: (
        x.payment_freq() != 12 and x.is_payment_mth(0)),
    "a month between instalments at t = 0": lambda x: (
        x.is_payout(0) and not x.is_payment_mth(0)),
}
IN_FRAME = {
    "a premium in the frame": lambda x, t: t > 0 and x.premium_pp(t) > 0.0,
    "the deferral death benefit": lambda x, t: x.claims(t, _code(x, "DEATH")) > 0.0,
    "the refund running out": lambda x, t: (
        x.is_cash_refund() and x.refund_balance(t) > 0.0 and x.is_active(t + 1)
        and x.refund_balance(t + 1) == 0.0),
    "the derived period ending": lambda x, t: (
        x.is_installment_refund() and x.certain_floor(t) == 1.0
        and x.certain_floor(t + 1) == 0.0),
    "an elected guarantee ending": lambda x, t: (
        x.is_period_certain() and x.certain_floor(t) == 1.0
        and x.certain_floor(t + 1) == 0.0),
    "the life tail resuming after a commutation": lambda x, t: (
        x.commute_frac_cum(t) > 0.0 and x.certain_floor(t) == 0.0
        and x.annuity_payments(t) > 0.0),
    "an acceleration straddling a guarantee's end": lambda x, t: (
        x.duration_mth(t) == x.accel_mth() and x.certain_floor(t) == 1.0
        and x.certain_floor_pm(x.accel_mth() + x.accel_months - 1) == 0.0),
    "an acceleration on life-contingent instalments": lambda x, t: (
        x.duration_mth(t) == x.accel_mth() and x.certain_floor(t) == 0.0
        and x.annuity_payments(t) > 0.0),
    "an acceleration on guaranteed instalments, l_last(T) derived": lambda x, t: (
        x.duration_mth(t) == x.accel_mth() and x.certain_floor_pm(x.accel_mth() + 1) == 1.0
        and x.duration_mth_init() <= x.income_start_mth()),
    "an acceleration in a commuted guarantee's last month": lambda x, t: (
        x.duration_mth(t) == x.accel_mth() and x.commute_frac_cum(t) > 0.0
        and x.certain_floor(t) == 1.0 and x.certain_floor(t + 1) == 0.0),
    "a commutation inside a derived period": lambda x, t: (
        x.is_installment_refund() and x.commuted_value(t) > 0.0),
    "a refund, valued off its period": lambda x, t: (
        _off_period(x) and x.claims(t, _code(x, "REFUND")) > 0.0),
    "a certain instalment, valued off its period": lambda x, t: (
        _off_period(x) and x.certain_floor(t) == 1.0 and x.annuity_payments(t) > 0.0),
    "the cap below omega": lambda x, t: any(
        x.mort_rate(t, life) == 1.0 and x.age(t, life) < x.omega_age for life in _lives(x)),
    "omega inside a guarantee": lambda x, t: (
        x.certain_floor(t) == 1.0 and x.age(t, 1) >= x.omega_age
        and x.mort_rate(t, 1) == 1.0),
    "a QLAC complying": lambda x, t: x.is_qlac() and x.qlac_flags() == [],
    **{f"the QLAC condition: {flag}": (lambda x, t, flag=flag: flag in x.qlac_flags())
       for flag in ("premium limit exceeded", "income start after the age limit",
                    "cost-of-living adjustment on a QLAC", "commutation on a QLAC",
                    "payment acceleration on a QLAC",
                    "income form not permitted on a QLAC")},
    "a slice priced to an adjusted start": lambda x, t: (
        x.premium_pp(t) > 0.0 and 0 <= x.adjust_mth() <= x.duration_mth(t)),
}


def _branches(x, kind):
    """The names in :data:`AT_VALUATION` and :data:`IN_FRAME` that hold of row ``x``.

    A future row stands at its issue date with nothing in force, so only the frame's are
    asked of it.
    """
    reached = set() if kind == "future" else {
        what for what, holds in AT_VALUATION.items() if holds(x)}
    return reached | {what for what, holds in IN_FRAME.items()
                      if any(holds(x, t) for t in range(x.t_entry(), x.proj_len()))}


def _record(case, proj):
    """Sweep the splice row ``proj`` of ``case`` and record what the rules test needs of it.

    :func:`_rule_breaches`'s record, with the row's :func:`_branches`.  A row that raises is
    recorded as raising, which the rules test reports.
    """
    try:
        _sweep(proj)
        record = _rule_breaches(proj)
        record["branches"] = _branches(proj, case[0])
        record["raised"] = None
    except Exception as err:                    # recorded, and reported by the rules test
        record = {"negative": [], "early": [], "ahead": [], "outside": [],
                  "branches": set(), "raised": _raised(err)}
    return record


def _record_of(spliced, records, case):
    """The record of ``case``, from the case that compared its row or, failing it, now."""
    if case not in records:
        sec = spliced[1]
        key = _row_key(sec, *case)
        try:
            records[case] = _record(case, projection(sec, key))
        finally:
            _release(sec, key, collect=True)
    return records[case]


# ---------------------------------------------------------------------------
# T2 -- the splice


@pytest.mark.parametrize(
    "kind, s_point, month",
    [_case(case, CORE_SPLICES, _case_id(*case)) for case in SPLICES + IN_FORCE_TWINS])
def test_an_in_force_point_continues_its_s_projection(spliced, splice_records, kind,
                                                      s_point, month):
    """Opened with S's state at month d, the point is S from d on, in every cell of S's.

    This is the test that says the opening state is complete: a state column the SEC row
    did not carry, or carried from the wrong instant, would make SEC part from S here, and
    nowhere else, because on a point issued at ``t = 0`` the two clocks coincide and the
    opening state is each life alive, nothing paid or bought, nothing frozen and no change
    in the reference rate.  The row is read in the splice's one read of its table, with
    SEC's ``ref_rate_shift`` at 0 (:data:`SEC_REFS`), so its commutation discount rate is
    S's only if it reads the change it carries.  For the same reason it is the test that
    catches a policy month passed as ``t`` (R1a): the premium months, the income start
    month, the payment months, the certain period, the option months and the refund balance
    all read the policy clock.  The frame comparisons read SEC row ``t`` against S row
    ``t + d`` in every column of ``result_cf`` and every column of ``result_pols`` both
    reports hold, and fail frames that end apart.  The cell comparison then evaluates every
    cell of S's but :data:`SPLICE_EXEMPT`, at every argument S cached inside its own frame
    from month ``d`` on, moved onto SEC's clock, to 1e-9 relative with no absolute floor
    (:func:`_compared`): each life's survival, the premiums paid and the income bought, the
    pricing of each premium still due at its policy month, the instalments scheduled to
    date at every policy month S read them, the counts and the payment factors among them.
    The floor would hide what matters near the limiting age, where a capped rate kills
    lives whose survival is near 1e-8.  The four roll-forward residuals are compared at the
    floor, since they are rounding around 0.  An S cell this model lacked would fail it.

    The row is swept and recorded for the rules test first (:func:`_record`), then compared,
    and released either way, and so is its S point after the last case that compares a row
    of it.
    """
    s, sec = spliced[0], spliced[1]
    case = (kind, s_point, month)
    key = _row_key(sec, *case)
    try:
        sec_proj = projection(sec, key)
        splice_records[case] = _record(case, sec_proj)
        s_proj = _point(s, s_point)
        for report in REPORTS:
            assert frame_mismatches(s_proj.cells[report](), sec_proj.cells[report](),
                                    t_offset=month, atol=0.0) == [], report
        assert _compared(s_proj, sec_proj, month, SPLICE_EXEMPT) == []
    finally:
        _release(sec, key, collect=True)
        if LAST_OF_POINT.get(s_point) == case:
            _release(s, _key(s, s_point))
        if T2_CASES and case == T2_CASES[-1]:
            _refreeze()


# ---------------------------------------------------------------------------
# T3 -- future new business


@pytest.mark.parametrize(
    "s_point, k",
    [_case(case, CORE_FUTURES, _case_id("future", case[0], -case[1]))
     for case in FUTURES])
def test_future_new_business_is_the_s_projection_k_months_on(spliced, splice_records,
                                                             s_point, k):
    """Issued k months after the valuation date, the point is S's projection k months on.

    SEC rows ``k ..`` are S rows ``0 ..``, ending together at the stop rule, in
    ``result_cf`` and in every column of ``result_pols`` S's has, and every cell of S's but
    :data:`FUTURE_EXEMPT` agrees at every argument S cached inside its own frame, moved
    ``k`` later, to 1e-9 relative with no absolute floor, the residuals at the floor.  A
    future row holds its whole premium schedule and whole policy years, so its premiums by
    month and its annual display are compared too.  The row is read in the splice's one
    read of its table (:data:`SEC_REFS`) and compared with S read with its
    ``ref_rate_shift`` at 0 (:data:`LATER_REFS`): bought after the valuation date, the
    contract has seen no change in the reference rate on the block's path, and S's point is
    the same contract on it.  An S cell this model lacked would fail it.  Before issue
    every column of ``result_cf`` and ``result_pols`` is an exact zero, and the contracts
    arrive in month ``k`` as new business, bringing the first premium.

    The last assertions are R1 and D4's base rule made testable.  After every report, no
    decrement rate keyed by month has been evaluated at a month before issue, and neither
    age reader has been read below an issue age.  A survival recursion based at ``t == 0``
    rather than at ``t_entry()``, which carries each life at 1 through the months before,
    or a rate that evaluates its table before asking whether the month is in cover, still
    gives the right numbers.  The rules test's look-back and the guard test see the first
    too, and the guard test the second.

    The pre-issue rows are asserted present before they are asserted zero: a frame that
    opened at issue would have none, its zeros would hold of nothing, and the comparisons
    with S, which start there, would not see it.  The row is swept and recorded for the
    rules test first (:func:`_record`), and released after, with the S point it was
    compared with, swept here.
    """
    s_later, sec = spliced[2], spliced[1]
    case = ("future", s_point, -k)
    key, s_key = _row_key(sec, *case), _key(s_later, s_point)
    try:
        sec_proj = projection(sec, key)
        splice_records[case] = _record(case, sec_proj)
        s_proj = projection(s_later, s_key)
        _sweep(s_proj)
        df, pols = sec_proj.result_cf(), sec_proj.result_pols()
        assert frame_mismatches(s_proj.result_cf(), df, t_offset=-k, atol=0.0) == []
        assert frame_mismatches(s_proj.result_pols(), pols, t_offset=-k, atol=0.0) == []
        assert _compared(s_proj, sec_proj, -k, FUTURE_EXEMPT) == []
        for report, frame in (("result_cf", df), ("result_pols", pols)):
            assert list(frame.index[:k]) == list(range(k)), report
            assert (frame.loc[:k - 1] == 0.0).all().all(), report
        assert sec_proj.pols_new_biz(k) == sec_proj.policy_count() == 1.0
        assert sec_proj.premiums(k) == s_proj.premiums(0) > 0.0
        early = {name: sorted(args for args in _cached_args(sec_proj.cells[name])
                              if args[0] < k)
                 for name in DECREMENT_RATES}
        assert not any(early.values()), f"rates evaluated before issue: {early}"
        for name in AGE_READERS:
            low = [(x, life) for x, life in _cached_args(sec_proj.cells[name])
                   if x < sec_proj.age_at_entry(life)]
            assert not low, f"{name} read below an issue age: {low[:5]}"
    finally:
        _release(sec, key)
        if s_key in s_later.Projection.itemspaces:
            _release(s_later, s_key)
        gc.collect()


# ---------------------------------------------------------------------------
# D11's R1, R1a and R2, and D3's closed-form clock


@pytest.mark.parametrize("grid", [pytest.param("core", id="core"),
                                  pytest.param("full", id="full", marks=FULL_ONLY)])
def test_no_cell_is_called_before_the_valuation_date_or_reads_far_ahead(spliced,
                                                                        splice_records,
                                                                        grid):
    """R1, its look-back, R1a's ranges and R2's look-ahead, on the rows T2 and T3 compare.

    Each is a rule of how the model computes, not of what, so no number shows a breach,
    and on a point issued at ``t = 0`` the two clocks coincide and hide it from T1 too.
    The splice's rows are points in force at every month T2 names, the variants among
    them, and points issued later, and each was swept first:

    * R1: no cell holds a negative argument.  modelx evaluates one without complaint, and
      a compiled cache raises ``IndexError`` below 0 (USLIB-SEC-PLAN.md F4).  A policy
      month turned into ``t`` by subtracting ``duration_mth_init()`` (R1a) goes negative on
      a point past it: the income start month, a premium month or an option month on a
      contract valued after it, and the ``-1`` an option accessor returns for "never".  So
      does a survival, premium or income recursion based at ``t == 0`` but read a month
      back from it.
    * R1's look-back stops at ``t_entry()``: no cell evaluated at a month from
      ``t_entry()`` on read a month before it.  On a point issued later a recursion based
      at ``t == 0`` reads the months before, where each life is carried at 1 and nothing
      is paid, so no number shows it and no argument goes negative.
    * R1a's ranges: every argument of a cell keyed by the policy clock, a policy year or an
      age is one the contract has (:func:`_contract`): the premiums and their pricing, the
      pricing survival and the annual rate by policy year, the payout schedule by policy
      month and the instalments scheduled to date, the display years from the valuation
      date's, and the two age readers from each life's issue age to the last below omega.
      A schedule read at a policy month before issue, an age table read past omega, or a
      cache sized from the contract read beyond it would wrap round in a compiled model.
    * R2's look-ahead: no cell evaluated at month ``t`` read a cell keyed by a month beyond
      ``t + 1``, as modelx's dependency graph records each cached call's precedents, read
      directly or through a precedent keyed by no month, which is followed to the
      month-keyed calls it reads (:func:`_months_read`): ``surv_to_payout()``, read in
      every month, would read ``lives_if_last`` at the income start month from the
      deferral.  ``DIA_US_S``'s refund, commuted value and acceleration read the schedule
      at months ahead of ``t`` as ``annuity_pp_sched(s)``, and its commutation residual
      reads every guaranteed month still to come; here they read the schedule by policy
      month, which no frame index ahead of ``t`` keys, and the residual is measured where
      the guarantee ends, reading back.  DIA admits no look-ahead.

    Each row was scanned by the T2 or T3 case that compared it (:func:`_record`), and a row
    no case has scanned is scanned here.  The core case covers the core's rows, the full
    case every other row of the full grid, with ``USLIB_SEC_FULL=1``.  The twins in the
    splice's table are no case's, and are left out: on them the clocks coincide, and T1
    compares them with S cell by cell.  The closed-form clock and the recursion depth are
    asserted on the committed model, in the tests after this one.
    """
    cases = [case for case in GRID if (case in CORE_GRID) == (grid == "core")]
    found = {"negative": [], "early": [], "ahead": [], "outside": [], "raised": []}
    for case in cases:
        record, where = _record_of(spliced, splice_records, case), _case_id(*case)
        for what in ("negative", "early", "ahead", "outside"):
            found[what] += [f"{where}: {item}" for item in record[what]]
        if record["raised"]:
            found["raised"].append(f"{where}: {record['raised']}")
    assert cases, f"the {grid} grid has no rows"
    assert not found["raised"], f"rows that raised: {found['raised'][:10]}"
    assert not found["negative"], f"called at a negative argument: {found['negative'][:10]}"
    assert not found["early"], f"read before issue from the books: {found['early'][:10]}"
    assert not found["ahead"], f"read beyond t + 1: {found['ahead'][:10]}"
    assert not found["outside"], f"outside the contract: {found['outside'][:10]}"


def test_the_policy_clock_is_a_closed_form_and_no_recursion_runs_backward(sec_read):
    """D3 and R2's recursions, on the committed model as it was first swept, cold.

    Both need a model on which nothing had been evaluated yet, which is what the fixture
    held when it made the record asserted here:

    * D3: the policy clock is the closed form.  Called first, ``duration_mth(500)``
      evaluates ``duration_mth`` once, where ``BasicTerm_SE``'s recursion would evaluate
      it at all 501 months from 0.
    * R2's recursions run forward: under modelx's recursion limit lowered to
      :data:`CALL_DEPTH`, every committed point is swept, each column in ascending ``t``.
      A forward recursion, through ``t - 1``, finds the month before already cached and
      stays shallow, which is why D3 is asserted on its own.  So do the schedules read by
      policy month, because each is based where it is first read: the instalments scheduled
      to date at the valuation date's policy month, by one loop over the payout months
      before it, so the anchor in its last month reads them without recursing back 478
      months to its income start month; and the pricing survival and the payout income by
      a loop from issue and from the valuation date.  A backward recursion over the frame,
      through ``t + 1``, keeps every step within the look-ahead but opens a chain as long
      as the frame, which a compiled model would run on the C stack (F7), and fails here.
    """
    record = sec_read[1]
    assert record["duration_mth(500)"] == 500
    assert record["keys"] == [500]
    assert not record["deep"], f"under a recursion limit of {CALL_DEPTH}: {record['deep']}"


def _cold_depth(proj, cell, args):
    """How many cells deep ``cell(*args)`` runs on ``proj``, by modelx's stack trace."""
    mx.start_stacktrace(maxlen=None)
    try:
        proj.cells[cell](*args)
        trace = mx.get_stacktrace(summarize=False)
    finally:
        mx.stop_stacktrace()
    level = deepest = 0
    for event, *_ in trace:
        level += 1 if event == "ENTER" else -1
        deepest = max(deepest, level)
    return deepest


def _longest_cover():
    """The two points at the contract's longest cover from issue, and their premiums.

    S point 5's twin, the installment refund, at the youngest issue age,
    :data:`CONTRACT_MIN_AGE`, with its income from policy month 360, the latest the
    product allows: 1,176 months to the age stop, through which each life's survival
    runs, and the refund-period search over its payout schedule from issue.  Once issued at
    the valuation date and once 120 months on, the longest frame, 1,296 months.  Each takes
    point 5's premiums.
    """
    row = _committed().loc[[5]].assign(issue_age=CONTRACT_MIN_AGE, income_start_mth=360)
    rows = pd.concat([row, row.assign(duration_mth=-120, policy_id="DIA-000005-F120",
                                      row_kind="future", source_mth=-120)])
    rows.index = pd.Index([1, 2], name="point_id")
    premiums = _committed_schedule()
    premiums = premiums[premiums["point_id"] == 5]
    schedule = pd.concat([premiums.assign(point_id=1), premiums.assign(point_id=2)],
                         ignore_index=True)
    return rows, schedule


# modelx warns as its stack trace starts and stops, which is all the test does with it.
@pytest.mark.filterwarnings("ignore:call stack trace:UserWarning")
def test_the_deepest_cold_call_runs_one_cell_a_month(tmp_path):
    """A cold ``net_cf`` in the last month runs one cell a month back to ``t_entry`` (D5),
    and a cold first month runs a handful of cells deep.

    On a model just read, nothing is cached, so ``net_cf(proj_len() - 1)`` runs each chain
    from the end of the frame back to the first month on the books, each life's survival,
    the premiums paid and the income bought, and modelx's stack trace counts how deep.
    Each chain may be one cell a month and no more, plus at most :data:`CHAIN_OVERHEAD`
    cells above and below it: on the twins of the anchor, the installment refund and the
    joint point, 720 months; on the anchor a month into its income phase, whose refund
    reads the instalments scheduled to date back to the valuation date's policy month, and
    no further; on the joint point issued 13 months on; and at the contract's longest cover
    from issue (:func:`_longest_cover`), 1,176 months from issue age 22, issued at the
    valuation date and 120 months on.  No number shows the depth, and a compiled model runs
    the chain on the C stack, so a chain of two cells a month, which gives the same
    numbers, needs twice the stack (F7).  A future point's chain stops at ``t_entry()``, so
    the longest frame, 1,296 months, runs no deeper than the cover it holds.

    And a cold ``net_cf(0)`` runs at most :data:`FIRST_MONTH_DEPTH` cells deep on the twins
    of the anchor, the installment refund and the start-date adjustment and on the point in
    deferral with a premium due: the first month reads ``l_last(T)`` only where a certain
    floor pays it, and the installment refund prices its premiums for its stop rule by
    loops from issue (R2, F7), where ``DIA_US_S``'s first month recurses through its
    survival to the income start month, 251 cells on the anchor and 311 on the adjustment.
    A floor weight read in deferral, or a pricing survival written as a recursion, gives the
    same numbers, and fails here.
    """
    rows, schedule = _longest_cover()
    refund = _label(_committed(), "derived", 1, 241)
    later = _label(_committed(), "future", 8, -13)
    reads = [("committed", model_path(SEC), [1, 5, 8, refund, later]),
             ("longest", _sec_inputs(tmp_path, rows, schedule=schedule), [1, 2])]
    found, depths = [], {}
    for where, folder, labels in reads:
        for label in labels:
            fresh = _read(folder, "depth")
            try:
                p = _point(fresh, label)
                last = p.proj_len() - 1
                depth = _cold_depth(p, "net_cf", (last,))
                depths[where, label] = depth
                allowed = last - p.t_entry() + CHAIN_OVERHEAD
                if depth > allowed:
                    found.append(f"{where} point {label}: net_cf({last}) cold runs {depth} "
                                 f"cells deep, beyond {allowed}, one a month back to "
                                 f"t_entry() {p.t_entry()} and {CHAIN_OVERHEAD} more")
            finally:
                fresh.close()
    deferred = _label(_committed(), "derived", 14, 59)
    for label in (1, 5, 13, deferred):
        fresh = _read(model_path(SEC), "first")
        try:
            depth = _cold_depth(_point(fresh, label), "net_cf", (0,))
            if depth > FIRST_MONTH_DEPTH:
                found.append(f"point {label}: net_cf(0) cold runs {depth} cells deep, "
                             f"beyond {FIRST_MONTH_DEPTH}")
        finally:
            fresh.close()
    assert not found, found
    assert depths["longest", 1] > 1176 - CHAIN_OVERHEAD, (
        f"the longest cover ran {depths['longest', 1]} cells deep: the depth test did not "
        f"reach it")


# ---------------------------------------------------------------------------
# T4 -- the count algebra
#
# BEF_DECR == BEF_NB + pols_new_biz, at every t of every point, is a convention
# (test_new_business_joins_the_count_before_decrements), and so is the new business
# entering once at its policy_count; neither is repeated here.


def test_the_count_is_on_the_books_from_issue_to_the_stop_rule(sec_model):
    """The count weights every month from issue to the stop rule, undecremented.

    DIA_US_S weights every flow by its constant ``pols_if_init`` and carries mortality in
    each life's survival, and so does this model: under independence the two lives'
    probabilities are the whole survival state, which a count weighted by survival could
    not carry.  So on every committed point ``pols_if_at(t, "BEF_DECR")``, the count
    weighting month ``t``, is ``policy_count()`` at every ``t`` from ``t_entry()`` to the
    last row and 0 before, and ``"BEF_NB"`` opens at ``t_entry()`` at ``pols_if_init()``,
    the count in force at the valuation date, 0 on a point not yet in force.  The count
    leaves the books once, at the stop rule: ``BEF_DECR(t) - BEF_NB(t + 1)`` is 0 inside
    the frame and the whole count at the last row, whose next month, ``t = proj_len()``,
    is outside cover.  No maturity cell is needed for it, since nothing decrements the
    count.  ``result_pols()`` puts its columns in :data:`RESULT_POLS`'s order, over the
    frame.  And a timing neither model knows is refused rather than answered with another
    count.
    """
    nb = _code(sec_model.Projection, "BEF_NB")
    decr = _code(sec_model.Projection, "BEF_DECR")
    table = sec_model.Data.model_point_table()
    for key, point_id in zip(point_keys(sec_model), table.index):
        p = projection(sec_model, key)
        entry, n, count = p.t_entry(), p.proj_len(), p.policy_count()
        assert [p.pols_if_at(t, decr) for t in range(n)] == (
            [0.0] * entry + [count] * (n - entry)), point_id
        assert p.pols_if_at(entry, nb) == p.pols_if_init(), point_id
        assert p.pols_if_init() == (count if p.duration_mth_init() > 0 else 0.0), point_id
        moved = [p.pols_if_at(t, decr) - p.pols_if_at(t + 1, nb) for t in range(entry, n)]
        assert moved == [0.0] * (n - 1 - entry) + [count], point_id
        pols = p.result_pols()
        assert list(pols.columns) == RESULT_POLS, point_id
        assert pols.index.name == "t" and list(pols.index) == list(range(n)), point_id
    _refused(lambda: projection(sec_model, point_keys(sec_model)[0]).pols_if_at(
        0, "BEF_MAT"), "invalid timing")


def test_pols_if_is_the_count_weighted_by_survival(sec_model):
    """``pols_if(t)`` is the count on the books weighted by survival, not ``BEF_DECR``.

    On every committed point and at every ``t`` of its frame, ``pols_if(t)`` is exactly
    ``pols_if_at(t, "BEF_DECR") * lives_if_last(t)``: the contracts on the books weighted
    by the probability that a covered life is alive at the start of month ``t``,
    ``DIA_US_S``'s ``pols_if_init * l_last(t)`` on the count on the books, which carries
    the maintenance expense.  It differs from the count that weights the row wherever
    survival is below 1: on the period certain in force 300 months, ``pols_if(0)`` is 0.5577
    against a count of 1, on the commuting contract a month after its commutation 0.677527,
    and on the joint point with its joint annuitant dead 4.25e-05.  That is why the
    registry marks the model ``survival_pols_if`` and the convention that ``pols_if`` is
    ``BEF_DECR`` skips it (D5).
    """
    decr = _code(sec_model.Projection, "BEF_DECR")
    table = sec_model.Data.model_point_table()
    for key, point_id in zip(point_keys(sec_model), table.index):
        p = projection(sec_model, key)
        for t in range(p.proj_len()):
            assert p.pols_if(t) == p.pols_if_at(t, decr) * p.lives_if_last(t), (point_id, t)
    for s_point, month, value in ((7, 300, 0.5577), (15, 253, 0.677527),
                                  (8, 672, 4.245667e-05)):
        p = _row(sec_model, "derived", s_point, month)
        assert p.pols_if(0) == pytest.approx(value, rel=1e-6, abs=0.0), (s_point, month)
        assert p.pols_if_at(0, decr) == p.policy_count() == 1.0
        assert p.pols_if(0) < p.pols_if_at(0, decr)


def test_result_pols_is_s_report_with_the_new_business_beside_it(sec_model, s_model):
    """``result_pols()`` is S's, column for column, with ``pols_new_biz`` beside it (D5).

    T1 skips the report as a whole, because its frame has a column S's lacks (the spec's
    exempt), so it is compared here, on every twin, at offset 0.  Its columns are
    :data:`RESULT_POLS`: ``pols_if`` first, as ``BasicTerm_SE`` sets its counts out, where
    ``DIA_US_S`` has it last, then ``pols_new_biz``, the contracts issued in the month, then
    S's other seven in S's order.  Every column S's report has agrees, to 1e-9 with no
    absolute floor, frames ending together, and ``pols_new_biz`` holds the count in the
    month the contract is issued and 0 in every other.  Counts and survival carry no
    inflation, so the shipped assumptions serve.
    """
    table = sec_model.Data.model_point_table()
    twins = table.index[table["row_kind"] == "twin"].tolist()
    assert twins == sorted(s_model.Data.model_point_table().index)
    for point_id in twins:
        p = _point(sec_model, point_id)
        mine, theirs = p.result_pols(), _point(s_model, point_id).result_pols()
        assert list(mine.columns) == RESULT_POLS, point_id
        assert sorted(theirs.columns) == sorted(c for c in RESULT_POLS
                                                if c != "pols_new_biz"), point_id
        assert frame_mismatches(theirs, mine, atol=0.0) == [], point_id
        assert list(mine["pols_new_biz"]) == [
            p.policy_count() if t == 0 else 0.0 for t in mine.index], point_id


# What T4 multiplies policy_count by: not a whole number, because a count of contracts need
# not be one, so that a flow which read the count as whole contracts would not follow it.
COUNT_FACTOR = 2.5

# The twins T4 and the extract test project beside every row in force or issued later: the
# anchor on the table basis, the installment refund, the joint point and the commuting
# point.  Between them those rows carry every flow (the premiums, the death benefit, the
# refund, the instalments, an acceleration's lump sum and a commutation), every
# opening-state column, the count in force and new business.  The other twins are T1's.
FLOW_TWINS = (1, 5, 8, 15)


def _flow_points(table):
    """The labels of ``table``'s rows that T4 and the extract test project."""
    return [p for p in table.index
            if table.at[p, "row_kind"] != "twin" or p in FLOW_TWINS]


def test_scaling_the_count_scales_every_flow_and_no_per_contract_value(tmp_path):
    """``policy_count`` is a weight: 2.5 times the count, 2.5 times every flow, the same per
    contract.

    The committed table, and a copy with every count multiplied by :data:`COUNT_FACTOR`,
    are each read with :data:`SWITCHED_ON` set before either computes anything: the one
    assumption that ships at zero, the reference rate's change, switched on at the
    splice's value, so that the commutation is discounted at a moved rate on every point
    on the books.  On every point ``result_cf`` and the counts of ``result_pols`` are 2.5
    times the committed table's, element by element, to 1e-12 relative: a scaled count is a
    computed float, which may come back from the CSV within two ulps (``sec_support``'s
    module docstring).  So is every other cell of :data:`COUNTED`, at every argument the
    sweep of the committed table's point cached: the gross outgo, the annual claims and
    income, the counts at each timing and the commutation residual among them, the
    residual, rounding around 0, at a floor of 1e-9.  ``result_pols``'s seven probabilities
    and factors are the committed table's exactly, and so are ``result_annual``'s age,
    premium, CP, B and survival, its claims and income 2.5 times.  And every cell outside
    :data:`COUNTED` (the instalment, the refund, the commuted value per contract, the
    instalments scheduled to date, each life's survival, the opening state, the pricing,
    the rates, both clocks, the flags) agrees at every argument that sweep cached.  So a
    flow that dropped the count, or read it as whole contracts, which a table of counts of
    1 hides from every comparison with S, fails here.  Each counted cell is nonzero on some
    point: the premiums, the death benefit and the refund, the instalments, the lump sum
    of an acceleration and a commutation among them.  The points are every row in force or
    issued later and the twins that carry each flow beside them (:data:`FLOW_TWINS`), each
    released once compared.
    """
    table = _committed()
    base = _read(_sec_inputs(tmp_path / "base", table), "counted", SWITCHED_ON)
    scaled = _read(_sec_inputs(tmp_path / "scaled", table.assign(
        policy_count=COUNT_FACTOR * table["policy_count"])), "scaled", SWITCHED_ON)
    counted = sorted(COUNTED - set(REPORTS) - {"result_annual"})
    nonzero = set()
    try:
        for point_id in _flow_points(table):
            key, scaled_key = _key(base, point_id), _key(scaled, point_id)
            one, many = projection(base, key), projection(scaled, scaled_key)
            _sweep(one)
            for report in REPORTS:
                b, d = one.cells[report](), many.cells[report]()
                assert d.index.equals(b.index) and list(d.columns) == list(b.columns)
                flows = [c for c in b.columns if c not in RATES]
                bad = ((d[flows] - COUNT_FACTOR * b[flows]).abs()
                       > 1e-12 * (COUNT_FACTOR * b[flows]).abs()).any()
                assert not bad.any(), (key, report, list(bad[bad].index))
                nonzero |= {c for c in flows if (b[c] != 0.0).any()}
                rates = [c for c in b.columns if c in RATES]
                assert d[rates].equals(b[rates]), (key, report)
            b, d = one.result_annual(), many.result_annual()
            assert d.index.equals(b.index) and list(d.columns) == list(b.columns)
            for c in b.columns:
                want = COUNT_FACTOR * b[c] if c in ANNUAL_COUNTED else b[c]
                bad = (d[c] - want).abs() > 1e-12 * want.abs()
                assert not bad.any(), (key, "result_annual", c, list(bad[bad].index))
            for name in counted:
                for args in _cached_args(one.cells[name]):
                    want = COUNT_FACTOR * one.cells[name](*args)
                    got = many.cells[name](*args)
                    floor = 1e-9 if name in RESIDUALS else 0.0
                    assert abs(got - want) <= floor + 1e-12 * abs(want), (
                        key, name, args, got, want)
                    if want != 0.0 and name not in RESIDUALS:
                        nonzero.add(name)
            assert _mismatches(one, many, exempt=TWIN_EXEMPT_DEFAULT | COUNTED) == []
            _release(base, key)
            _release(scaled, scaled_key)
    finally:
        scaled.close()
        base.close()
    want = set(counted) - RESIDUALS
    assert want <= nonzero, f"0 on every point: {sorted(want - nonzero)}"


# ---------------------------------------------------------------------------
# T5 -- validation
#
# Each malformed table is the committed one with one fault, and only the rule under test
# refuses it.  The checks run over the whole table as it is read, in Data, and the message
# names the file it read and the column or every point at fault.  A blank cell reads as
# NaN, and so does a text cell once the checks coerce the column to numbers, so each is
# refused as a count, a duration, a month, a probability, an amount, a rate or a change in
# the reference rate that is not a number.  The repeated point_id holds another contract
# under the same label, as a bad extract would, so that the check must look at the labels
# and not at whole rows.  The point_ids are the committed table's: 18, the acceleration
# contract in deferral 59 months, with a premium due and its guarantee-period column; 19,
# the anchor on the table basis a month into its income phase, its cash refund running;
# 20, the period certain inside its guarantee at 300; 21, the commuting period certain a
# month after its commutation, with both frozen weights; 22, the start-date adjustment a
# month after it; 23, the joint point at 672, its joint annuitant dead; 26, the joint point
# issued 13 months on; and the twins 1, the anchor, 5, the installment refund, 8, joint, 13,
# the start-date adjustment, and 15, the commuting point.  A frozen weight of 0 is refused
# on a contract whose lives have all died, rows 20 and 21 with life 1 at 0, where it would
# otherwise pass every other rule.
#
# Where the docs say a check runs before another, its case sits on a row the later check
# would refuse differently, so that a check moved after it fails its case: a fractional
# income start month on point 20, whose frozen weight's presence rule reads the start
# month; the broken adjustment pair on point 19, past its income start month, where the
# start month in force it gives is blank; the life probabilities on point 18, which
# carries no frozen weight to break as well.
#
# Each check over a window of contract months is refused just inside each end of its
# window, its first month as well as its last, and read just outside it (the edges test),
# where an off-by-one would let a row through (USLIB-SEC-PLAN.md §5.2, T5, precised at
# M10).  An income start month is refused at -1 and read at 0.  An acceleration or a
# commutation, payout-phase options, are refused at policy months 0 and 239 and read at
# 240, the income start month, and at -1, never; on the adjustment's twin, deferred to 300,
# an acceleration is refused at 299 and read at 300.  The interlock is refused five months
# either side of the commutation and read six months either side: six before by the edges
# test, and six after in REFUSED, where proj_len() refuses it instead.  The at-issue
# check and the guarantee-period column's are refused at -120, the horizon, and at 0, and
# read at 1, a contract a month in force.  The frozen weights are refused given at -120
# and at their month, the income start month and the commutation month, and blank the
# month after, and read blank at their month and given after it.  The two checks on the
# adjustment's months, its new start month after the exercise and the exercise before the
# income start month, are refused where the months meet and read a month apart.  The two
# bounds between the frozen weights and the lives are held exactly, with no tolerance:
# each is read at equality and refused an ulp past it, l_last(t_c) above l_last(T) and
# either weight below the life alive, so that neither a floating-point slack nor a strict
# inequality passes.  Each case is read by a model of its own, its file named by a
# Reference set before the model computes anything (the malformed fixture), so a {file}
# in a message is the case's own filename.

_INTEGER = "{file}: {c} must be {what}; it is not at point_id [{p}]"
_LIFE = ("{file}: lives_if_init_{n} must be a probability, 0 to 1; it is not at "
         "point_id [{p}]")
_AMOUNT = "{file}: {c} must be a number, zero or more; it is not at point_id [{p}]"
_OPTION = ("{file}: {c} must be blank or a whole number of months, a policy month; it is "
           "not at point_id [{p}]")
_PAYOUT_OPTION = ("{file}: {c} must be blank or the income start month in force or later: "
                  "{option} is a payout-phase option; it is not at point_id [{p}]")
_START = ("{file}: income_start_mth must be a whole number of months, 0 or more, a policy "
          "month; it is not at point_id [{p}]")
_GUARANTEE = ("{file}: guarantee_mths_pricing_init must be blank or a number of months, "
              "zero or more; it is not at point_id [{p}]")
_WEIGHT = ("{file}: {c} must be blank or a probability, 0 to 1; it is not at point_id "
           "[{p}]")
_CHANGE = ("{file}: ref_rate_shift_init must be a number, the change in the reference rate "
           "since issue; it is not at point_id [{p}]")
_SINGLE = ("{file}: lives_if_init_2 must be 0 on a single-life contract, which covers no "
           "second life; it is not at point_id [{p}]")
_AT_ISSUE = ("{file}: {c} must hold its value at issue on a contract not yet in force, "
             "duration_mth 0 or less: each covered life alive, no premium paid, no income "
             "bought and no change in the reference rate; it does not at point_id [{p}]")
_NG_GIVEN = ("{file}: guarantee_mths_pricing_init must be given on a contract in force on "
             "a refund form, income_form CR or IR, whose premiums still due the kernel "
             "prices with it; it is blank at point_id [{p}]")
_NG_BLANK = ("{file}: guarantee_mths_pricing_init must be blank unless the contract is in "
             "force on a refund form: on new business the kernel derives it from the "
             "premium schedule, and the other forms fix it; it is not at point_id [{p}]")
_S2P_GIVEN = ("{file}: surv_to_payout_init must be given on a contract past its income "
              "start month in force; it is blank at point_id [{p}]")
_S2P_BLANK = ("{file}: surv_to_payout_init must be blank unless duration_mth is after the "
              "income start month in force, where the projection derives it; it is not at "
              "point_id [{p}]")
_CW_GIVEN = ("{file}: commute_weight_init must be given on a contract whose commutation "
             "month precedes the valuation date; it is blank at point_id [{p}]")
_CW_BLANK = ("{file}: commute_weight_init must be blank unless the commutation month "
             "precedes the valuation date, where the projection derives it; it is not at "
             "point_id [{p}]")
_ORDER = ("{file}: commute_weight_init must be at most surv_to_payout_init: a commutation "
          "is taken in the income phase, by part of the cohort that reached it; it is not "
          "at point_id [{p}]")
_FLOOR = ("{file}: {c} must be at least the probability that a covered life is alive at "
          "the valuation date: the cohort it weighs includes every life still alive; it "
          "is not at point_id [{p}]")
_EMPTY = ("{file}: {c} must be above 0 where it is given: {why}, so the cohort it weighs "
          "is not empty; it is not at point_id [{p}]")
_SEX = ("{file}: sex must be M or F, and so must joint_sex on a joint contract; it is not "
        "at point_id [{p}]")


def _m(template, **values):
    """A message of the templates above, ``{file}`` left for the case to fill."""
    return template.format(file="{file}", **values)


_YEARS = "a whole number of years, 0 or more"

MALFORMED = [
    *[(f"no {column} column", _drop(column), f"{{file}} has no {column} column")
      for column in ("policy_count", "duration_mth", *STATE)],
    ("a repeated point_id",
     lambda t: pd.concat([t, t.loc[[18]].assign(policy_id="DIA-900099")]),
     "{file}: point_id [18] appears more than once"),
    ("a negative count", _set("policy_count", [18], -0.1),
     "{file}: policy_count must be a number, zero or more; it is not at point_id [18]"),
    ("a count written as text", _set("policy_count", [19], "abc"),
     "{file}: policy_count must be a number, zero or more; it is not at point_id [19]"),
    ("a blank count", _set("policy_count", [20], NAN),
     "{file}: policy_count must be a number, zero or more; it is not at point_id [20]"),
    ("an infinite count", _set("policy_count", [21], float("inf")),
     "{file}: policy_count must be a number, zero or more; it is not at point_id [21]"),
    ("two bad counts", _both(_set("policy_count", [18], -1.0),
                             _set("policy_count", [26], "x")),
     "{file}: policy_count must be a number, zero or more; it is not at point_id "
     "[18, 26]"),
    ("a fractional duration", _set("duration_mth", [18], 59.5),
     "{file}: duration_mth must be a whole number of months; it is not at point_id [18]"),
    ("a blank duration", _set("duration_mth", [18], NAN),
     "{file}: duration_mth must be a whole number of months; it is not at point_id [18]"),
    ("a duration written as text", _set("duration_mth", [18], "ten"),
     "{file}: duration_mth must be a whole number of months; it is not at point_id [18]"),
    ("issued beyond the horizon", _set("duration_mth", [26], -121),
     "{file}: duration_mth must be -120 or more, a policy issued at most 120 months after "
     "the valuation date; it is not at point_id [26]"),
    ("a fractional income start month", _set("income_start_mth", [20], 300.5),
     _m(_START, p=20)),
    ("an income start month written as text", _set("income_start_mth", [20], "x"),
     _m(_START, p=20)),
    ("a negative income start month", _set("income_start_mth", [1], -12),
     _m(_START, p=1)),
    ("an income start month of -1", _set("income_start_mth", [1], -1), _m(_START, p=1)),
    ("an adjustment month written as text", _set("adjust_mth", [22], "x"),
     _m(_OPTION, c="adjust_mth", p=22)),
    ("a fractional adjustment month", _set("adjust_mth", [22], 120.5),
     _m(_OPTION, c="adjust_mth", p=22)),
    ("a new start month written as text", _set("adjust_start_mth", [22], "x"),
     _m(_OPTION, c="adjust_start_mth", p=22)),
    ("a fractional new start month", _set("adjust_start_mth", [22], 300.5),
     _m(_OPTION, c="adjust_start_mth", p=22)),
    ("an acceleration month written as text", _set("accel_mth", [18], "x"),
     _m(_OPTION, c="accel_mth", p=18)),
    ("a fractional acceleration month", _set("accel_mth", [18], 252.5),
     _m(_OPTION, c="accel_mth", p=18)),
    ("a commutation month written as text", _set("commute_mth", [21], "x"),
     _m(_OPTION, c="commute_mth", p=21)),
    ("a fractional commutation month", _set("commute_mth", [21], 252.5),
     _m(_OPTION, c="commute_mth", p=21)),
    ("an adjustment without its new start month, past T",
     _set("adjust_mth", [19], 120),
     "{file}: adjust_mth and adjust_start_mth go together, both blank or both a policy "
     "month; they do not at point_id [19]"),
    ("a new start month without its adjustment, past T",
     _set("adjust_start_mth", [19], 300),
     "{file}: adjust_mth and adjust_start_mth go together, both blank or both a policy "
     "month; they do not at point_id [19]"),
    ("a new start month at the exercise", _set("adjust_start_mth", [22], 120),
     "{file}: adjust_start_mth must follow adjust_mth: an income start date moves to a "
     "month after the exercise; it does not at point_id [22]"),
    ("an adjustment at the income start month", _set("adjust_mth", [13], 240),
     "{file}: adjust_mth must precede income_start_mth: a start-date adjustment is a "
     "deferral option; it does not at point_id [13]"),
    ("an acceleration in deferral", _set("accel_mth", [18], 200),
     _m(_PAYOUT_OPTION, c="accel_mth", option="payment acceleration", p=18)),
    ("an acceleration at issue", _set("accel_mth", [14], 0),
     _m(_PAYOUT_OPTION, c="accel_mth", option="payment acceleration", p=14)),
    ("an acceleration the month before the income start month",
     _set("accel_mth", [14], 239),
     _m(_PAYOUT_OPTION, c="accel_mth", option="payment acceleration", p=14)),
    ("an acceleration the month before an adjusted income start month",
     _set("accel_mth", [13], 299),
     _m(_PAYOUT_OPTION, c="accel_mth", option="payment acceleration", p=13)),
    ("a commutation in deferral", _set("commute_mth", [15], 200),
     _m(_PAYOUT_OPTION, c="commute_mth", option="commutation", p=15)),
    ("a commutation at issue", _set("commute_mth", [15], 0),
     _m(_PAYOUT_OPTION, c="commute_mth", option="commutation", p=15)),
    ("a commutation the month before the income start month",
     _set("commute_mth", [15], 239),
     _m(_PAYOUT_OPTION, c="commute_mth", option="commutation", p=15)),
    ("an acceleration five months after a commutation", _set("accel_mth", [15], 257),
     "{file}: accel_mth and commute_mth must fall six months apart or more, the product's "
     "interlock between its two payout options; they do not at point_id [15]"),
    ("an acceleration five months before a commutation", _set("accel_mth", [15], 247),
     "{file}: accel_mth and commute_mth must fall six months apart or more, the product's "
     "interlock between its two payout options; they do not at point_id [15]"),
    ("a joint flag written as text", _set("joint", [19], "no"),
     "{file}: joint must be True or False, a flag; it is not at point_id [19]"),
    ("a sex neither M nor F", _set("sex", [18], "X"), _m(_SEX, p=18)),
    ("no joint sex on a joint contract", _set("joint_sex", [23], NAN), _m(_SEX, p=23)),
    ("a fractional issue age", _set("issue_age", [18], 60.5),
     _m(_INTEGER, c="issue_age", what=_YEARS, p=18)),
    ("an issue age written as text", _set("issue_age", [19], "sixty"),
     _m(_INTEGER, c="issue_age", what=_YEARS, p=19)),
    ("a joint age written as text", _set("joint_age", [23], "x"),
     _m(_INTEGER, c="joint_age", what=_YEARS + ", on a joint contract", p=23)),
    ("a negative certain period", _set("certain_period", [20], -1),
     _m(_INTEGER, c="certain_period", what=_YEARS, p=20)),
    ("a fractional frequency", _set("frequency", [19], 12.5),
     _m(_INTEGER, c="frequency", what="a whole number of payments a year", p=19)),
    ("a fractional issue year", _set("issue_year", [18], 2026.5),
     _m(_INTEGER, c="issue_year", what="a whole number, a calendar year", p=18)),
    ("a negative rounding", _set("purchase_rate_dp", [19], -1),
     "{file}: purchase_rate_dp must be blank, for full precision, or a whole number of "
     "decimal places, 0 or more; it is not at point_id [19]"),
    ("a rounding written as text", _set("purchase_rate_dp", [19], "six"),
     "{file}: purchase_rate_dp must be blank, for full precision, or a whole number of "
     "decimal places, 0 or more; it is not at point_id [19]"),
    ("a blank survivor percentage", _set("survivor_pct", [23], NAN),
     _m(_INTEGER, c="survivor_pct", what="a probability, 0 to 1", p=23)),
    ("a survivor percentage above 1", _set("survivor_pct", [23], 1.5),
     _m(_INTEGER, c="survivor_pct", what="a probability, 0 to 1", p=23)),
    ("a blank COLA", _set("cola_rate", [18], NAN),
     _m(_INTEGER, c="cola_rate", what="a number, zero or more", p=18)),
    ("a negative COLA", _set("cola_rate", [18], -0.01),
     _m(_INTEGER, c="cola_rate", what="a number, zero or more", p=18)),
    ("an infinite other QLAC premium", _set("other_qlac_premium", [18], float("inf")),
     _m(_INTEGER, c="other_qlac_premium", what="a number, zero or more", p=18)),
    ("a commuted fraction above 1", _set("commute_frac", [21], 1.5),
     "{file}: commute_frac must be blank or a fraction, 0 to 1; it is not at point_id "
     "[21]"),
    ("a commuted fraction written as text", _set("commute_frac", [21], "all"),
     "{file}: commute_frac must be blank or a fraction, 0 to 1; it is not at point_id "
     "[21]"),
    ("a joint contract on the table basis", _set("factor_basis", [23], "table"),
     "{file}: factor_basis must be formula on a joint contract: the table basis, equation "
     "(1), factors a single life's survival out of the payout factor; it is not at "
     "point_id [23]"),
    ("life 1 above 1", _set("lives_if_init_1", [18], 1.5), _m(_LIFE, n=1, p=18)),
    ("life 1 below 0", _set("lives_if_init_1", [18], -0.1), _m(_LIFE, n=1, p=18)),
    ("life 1 blank", _set("lives_if_init_1", [18], NAN), _m(_LIFE, n=1, p=18)),
    ("life 1 written as text", _set("lives_if_init_1", [18], "alive"),
     _m(_LIFE, n=1, p=18)),
    ("life 2 below 0 on future business", _set("lives_if_init_2", [26], -0.1),
     _m(_LIFE, n=2, p=26)),
    ("life 2 written as text", _set("lives_if_init_2", [23], "0.0x"),
     _m(_LIFE, n=2, p=23)),
    ("negative premiums paid", _set("cum_premium_pp_init", [18], -1.0),
     _m(_AMOUNT, c="cum_premium_pp_init", p=18)),
    ("premiums paid written as text", _set("cum_premium_pp_init", [18], "x"),
     _m(_AMOUNT, c="cum_premium_pp_init", p=18)),
    ("a negative income bought", _set("annual_income_init", [18], -1.0),
     _m(_AMOUNT, c="annual_income_init", p=18)),
    ("an income bought written as text", _set("annual_income_init", [18], "x"),
     _m(_AMOUNT, c="annual_income_init", p=18)),
    ("a guarantee period written as text", _set("guarantee_mths_pricing_init", [18], "x"),
     _m(_GUARANTEE, p=18)),
    ("a negative guarantee period", _set("guarantee_mths_pricing_init", [18], -1.0),
     _m(_GUARANTEE, p=18)),
    ("l_last(T) written as text", _set("surv_to_payout_init", [19], "x"),
     _m(_WEIGHT, c="surv_to_payout_init", p=19)),
    ("l_last(T) above 1", _set("surv_to_payout_init", [19], 1.5),
     _m(_WEIGHT, c="surv_to_payout_init", p=19)),
    ("l_last(t_c) written as text", _set("commute_weight_init", [21], "x"),
     _m(_WEIGHT, c="commute_weight_init", p=21)),
    ("a rate change written as text", _set("ref_rate_shift_init", [19], "up"),
     _m(_CHANGE, p=19)),
    ("a blank rate change", _set("ref_rate_shift_init", [20], NAN), _m(_CHANGE, p=20)),
    ("an infinite rate change", _set("ref_rate_shift_init", [21], float("inf")),
     _m(_CHANGE, p=21)),
    ("a second life on a single-life contract", _set("lives_if_init_2", [19], 0.5),
     _m(_SINGLE, p=19)),
    ("a life not alive on future business", _set("lives_if_init_1", [26], 0.9),
     _m(_AT_ISSUE, c="lives_if_init_1", p=26)),
    ("a joint life not alive at issue", _set("lives_if_init_2", [8], 0.5),
     _m(_AT_ISSUE, c="lives_if_init_2", p=8)),
    ("premiums paid at issue", _set("cum_premium_pp_init", [1], 100.0),
     _m(_AT_ISSUE, c="cum_premium_pp_init", p=1)),
    ("income bought at issue", _set("annual_income_init", [5], 10.0),
     _m(_AT_ISSUE, c="annual_income_init", p=5)),
    ("a rate change at issue", _set("ref_rate_shift_init", [15], 0.005),
     _m(_AT_ISSUE, c="ref_rate_shift_init", p=15)),
    ("a rate change on future business", _set("ref_rate_shift_init", [26], -0.005),
     _m(_AT_ISSUE, c="ref_rate_shift_init", p=26)),
    ("a life not alive on business issued at the horizon",
     _moved(26, -120, lives_if_init_1=0.9), _m(_AT_ISSUE, c="lives_if_init_1", p=26)),
    ("no guarantee period on a refund form in force",
     _set("guarantee_mths_pricing_init", [18], NAN), _m(_NG_GIVEN, p=18)),
    ("a guarantee period at issue", _set("guarantee_mths_pricing_init", [1], 40.0),
     _m(_NG_BLANK, p=1)),
    ("a guarantee period on a period certain",
     _set("guarantee_mths_pricing_init", [20], 120.0), _m(_NG_BLANK, p=20)),
    ("no guarantee period a month in force",
     _moved(18, 1, guarantee_mths_pricing_init=NAN), _m(_NG_GIVEN, p=18)),
    ("a guarantee period on business issued at the horizon",
     _moved(26, -120, guarantee_mths_pricing_init=40.0), _m(_NG_BLANK, p=26)),
    ("no l_last(T) past the income start month", _set("surv_to_payout_init", [19], NAN),
     _m(_S2P_GIVEN, p=19)),
    ("l_last(T) in deferral", _set("surv_to_payout_init", [18], 0.99),
     _m(_S2P_BLANK, p=18)),
    ("l_last(T) at the income start month", _set("duration_mth", [19], 240),
     _m(_S2P_BLANK, p=19)),
    ("l_last(T) on business issued at the horizon",
     _moved(26, -120, surv_to_payout_init=0.9), _m(_S2P_BLANK, p=26)),
    ("no l_last(t_c) past the commutation", _set("commute_weight_init", [21], NAN),
     _m(_CW_GIVEN, p=21)),
    ("l_last(t_c) with no commutation", _set("commute_weight_init", [20], 0.6),
     _m(_CW_BLANK, p=20)),
    ("l_last(t_c) at the commutation month", _set("duration_mth", [21], 252),
     _m(_CW_BLANK, p=21)),
    ("l_last(t_c) on business issued at the horizon",
     _moved(26, -120, commute_mth=252, commute_frac=1.0, commute_weight_init=0.5),
     _m(_CW_BLANK, p=26)),
    ("l_last(t_c) above l_last(T)", _set("commute_weight_init", [21], 0.9),
     _m(_ORDER, p=21)),
    ("l_last(t_c) an ulp above l_last(T)",
     _both(_set("surv_to_payout_init", [21], 0.75),
           _set("commute_weight_init", [21], math.nextafter(0.75, 1.0))),
     _m(_ORDER, p=21)),
    ("l_last(T) below the life alive", _set("surv_to_payout_init", [19], 0.5),
     _m(_FLOOR, c="surv_to_payout_init", p=19)),
    ("l_last(t_c) below the life alive", _set("commute_weight_init", [21], 0.6),
     _m(_FLOOR, c="commute_weight_init", p=21)),
    ("l_last(T) an ulp below the life alive",
     _both(_set("lives_if_init_1", [19], 0.5),
           _set("surv_to_payout_init", [19], math.nextafter(0.5, 0.0))),
     _m(_FLOOR, c="surv_to_payout_init", p=19)),
    ("l_last(t_c) an ulp below the life alive",
     _both(_set("lives_if_init_1", [21], 0.5),
           _set("commute_weight_init", [21], math.nextafter(0.5, 0.0))),
     _m(_FLOOR, c="commute_weight_init", p=21)),
    ("l_last(T) below two joint lives' last survivor",
     _both(_set("lives_if_init_1", [23], 0.5), _set("lives_if_init_2", [23], 0.5),
           _set("surv_to_payout_init", [23], 0.7)),
     _m(_FLOOR, c="surv_to_payout_init", p=23)),
    ("l_last(T) of 0, every life dead in the guarantee",
     _both(_set("lives_if_init_1", [20], 0.0), _set("surv_to_payout_init", [20], 0.0)),
     _m(_EMPTY, c="surv_to_payout_init", p=20,
        why="a contract in force past its income start month reached it")),
    ("l_last(t_c) of 0, every life dead after the commutation",
     _both(_set("lives_if_init_1", [21], 0.0), _set("commute_weight_init", [21], 0.0)),
     _m(_EMPTY, c="commute_weight_init", p=21,
        why="a commutation is exercised by an owner alive to exercise it")),
]


@pytest.fixture(scope="module")
def malformed(tmp_path_factory):
    """A copy of the product directory holding every table of :data:`MALFORMED`.

    Each case is a file of its own beside one copy of the model, ``{case: filename}``.
    The cases do not share a model: each reads one of its own, with ``model_point_file``
    pointed at its file before the model computes anything (:func:`_read`).
    """
    root = tmp_path_factory.mktemp("malformed")
    files = {}
    for number, (case, edit, _) in enumerate(MALFORMED):
        files[case] = f"malformed_{number:02d}_sec.csv"
        temp_inputs(root, model_path(SEC), model_points=edit(_committed()),
                    model_point_file=files[case])
    return root / SEC, files


@pytest.mark.parametrize("case, edit, message", MALFORMED, ids=[c[0] for c in MALFORMED])
def test_a_malformed_in_force_row_is_refused_naming_its_point(malformed, case, edit,
                                                               message):
    """``Data.model_point_table()`` refuses the table, naming the fault (D6, T5).

    And a projection, which reads the table at its first ``model_point()``, meets the same
    refusal before it computes a number: the base ``Projection``'s default point is asked
    for its ``result_cf()``, since a table that is refused gives no keys to ask by.
    """
    folder, files = malformed
    model = _read(folder, "malformed", data={"model_point_file": files[case]})
    try:
        _refused(model.Data.model_point_table, message.format(file=files[case]))
        _refused(model.Projection.result_cf, message.format(file=files[case]))
    finally:
        model.close()


def _premium(point_id, column, value):
    """An edit of the premium schedule that writes ``value`` into ``column`` on the rows of
    point ``point_id``, the column made ``object`` first, as :func:`_set` makes it."""
    def edit(schedule):
        cells = schedule[column].astype(object)
        return schedule.assign(**{column: cells.where(schedule["point_id"] != point_id,
                                                      value)})
    return edit


def _added(point_id, month, amount=1000.0):
    """An edit of the premium schedule that adds a premium of ``amount`` to point
    ``point_id`` at policy month ``month``."""
    def edit(schedule):
        row = {"point_id": point_id, "slice": 9, "premium_mth": month,
               "premium_amt": amount, "provenance": "[std] a test case"}
        return pd.concat([schedule, pd.DataFrame([row])], ignore_index=True)
    return edit


_PREMIUM_MTH = ("{file}: premium_mth must be a whole number of months, 0 or more, a policy "
                "month; it is not at point_id [{p}]")
_PREMIUM_AMT = ("{file}: premium_amt must be a number, zero or more; it is not at "
                "point_id [{p}]")

# The malformed premium schedules, as (case, the edit of premium_schedule_sec.csv, the
# message): what Data.premium_schedule_table refuses, naming the file and the point.  The
# committed schedule holds S's schedule as it stands, then row 18's premium still due, at
# policy month 60, and row 26's two.  DIA_US_S takes int() of the raw month, so that 60.5
# is 60 and text raises Python's own message, and a point with no premium row projects
# silently, buying no income; here the months and amounts are read by value, each checked
# against the point it names, and a point that buys nothing is refused.  The two checks
# over a window of policy months are refused at each end and read just outside it (the
# edges test), USLIB-SEC-PLAN.md §5.2's T5 (precised at M10): a premium before the
# valuation date, on row 18 at 59, at policy months 0 and 58, and read at 59, due in the
# valuation month; and one at or after the income start month, at 240 and at the adjusted
# 300, and read at 239.
SCHEDULES = [
    *[(f"no {column} column", _drop(column), f"{{file}} has no {column} column")
      for column in ("point_id", "premium_mth", "premium_amt")],
    ("a point_id written as text", _premium(18, "point_id", "x"),
     "{file}: point_id must be a whole number, a model point's label; ['x'] is not"),
    ("a fractional point_id", _premium(18, "point_id", 18.5),
     "{file}: point_id must be a whole number, a model point's label; [18.5] is not"),
    ("a point the table lacks", _premium(18, "point_id", 99),
     "{file}: point_id [99] is no model point of model_point_table_sec.csv"),
    ("a fractional premium month", _premium(18, "premium_mth", 60.5),
     _m(_PREMIUM_MTH, p=18)),
    ("a premium month written as text", _premium(18, "premium_mth", "sixty"),
     _m(_PREMIUM_MTH, p=18)),
    ("a negative premium month", _premium(26, "premium_mth", -1), _m(_PREMIUM_MTH, p=26)),
    ("a premium written as text", _premium(18, "premium_amt", "x"),
     _m(_PREMIUM_AMT, p=18)),
    ("a negative premium", _premium(18, "premium_amt", -1.0), _m(_PREMIUM_AMT, p=18)),
    ("a blank premium", _premium(26, "premium_amt", NAN), _m(_PREMIUM_AMT, p=26)),
    ("a premium before the valuation date", _added(18, 58),
     "{file}: a premium falls before the valuation date at point_id [18]: those paid "
     "before it are in cum_premium_pp_init and annual_income_init, and the schedule holds "
     "the premiums still due"),
    ("a premium at issue on a contract in force", _added(18, 0),
     "{file}: a premium falls before the valuation date at point_id [18]: those paid "
     "before it are in cum_premium_pp_init and annual_income_init, and the schedule holds "
     "the premiums still due"),
    ("a premium at the income start month", _added(1, 240),
     "{file}: a premium falls at or after the income start month in force at point_id "
     "[1]: the income is level in payout"),
    ("a premium at an adjusted income start month", _added(13, 300),
     "{file}: a premium falls at or after the income start month in force at point_id "
     "[13]: the income is level in payout"),
    ("a point with no premium row", lambda s: s[s["point_id"] != 6],
     "{file}: point_id [6] buys no income: annual_income_init is 0 and no premium is due"),
    ("a point whose premiums are all 0", _premium(6, "premium_amt", 0.0),
     "{file}: point_id [6] buys no income: annual_income_init is 0 and no premium is due"),
]


@pytest.mark.parametrize("case, edit, message", SCHEDULES, ids=[c[0] for c in SCHEDULES])
def test_a_malformed_premium_schedule_is_refused_naming_its_point(tmp_path, case, edit,
                                                                  message):
    """``Data.premium_schedule_table()`` refuses the schedule, and a projection meets the
    refusal (D8, T5).

    The schedule is the model's own companion, checked against the model point table as
    that table is checked, so each case is the committed schedule with one fault, read by a
    model of its own from a copy of the inputs, its file named by a Reference set before
    the model computes anything.  The base ``Projection``'s default point, the anchor's
    twin, reads its premiums in its first month, so its ``result_cf()`` meets the same
    refusal before it computes a number, whichever point the fault is on.
    """
    folder = _sec_inputs(tmp_path, _committed())
    name = "malformed_premiums_sec.csv"
    edit(_committed_schedule()).to_csv(folder.parent / name, index=False)
    model = _read(folder, "schedule", data={"premium_schedule_file": name})
    try:
        _refused(model.Data.premium_schedule_table, message.format(file=name))
        _refused(model.Projection.result_cf, message.format(file=name))
    finally:
        model.close()


def _at(df, file, key_columns, key):
    """The one row of an assumption table at ``key``, as a mask of ``df``'s rows."""
    at = pd.Series(True, index=df.index)
    for c, v in zip(key_columns, key):
        at &= df[c] == v
    assert at.sum() == 1, (file, key)
    return at


def _cell(file, key_columns, key, column, value):
    """An edit of an assumption table that writes ``value`` into ``column`` at ``key``."""
    def edit(df):
        at = _at(df, file, key_columns, key)
        cells = df[column].astype(object)
        return df.assign(**{column: cells.where(~at, value)})
    return edit


def _row_again(file, key_columns, key):
    """An edit of an assumption table that writes the row at ``key`` a second time, last."""
    def edit(df):
        return pd.concat([df, df[_at(df, file, key_columns, key)]], ignore_index=True)
    return edit


def _row_gone(file, key_columns, key):
    """An edit of an assumption table that leaves out the row at ``key``."""
    def edit(df):
        return df[~_at(df, file, key_columns, key)]
    return edit


# Where the cases below write: the female rate at 70 is line 103 of each age-keyed table,
# which the anchor's life reads, and the female row at 120, its last line, 203, which no
# join reads, so that a fault in its key leaves no gap in the female ages; the factor
# tables' first line, 2, is the anchor's key, and their last, 5, a male row no point reads.
_MORT_KEY, _MORT_LAST = (70, "F"), (120, "F")
_PAYOUT_KEY, _PAYOUT_LAST = (80, "F", "CR"), (80, "M", "LO")
_ROP_KEY, _ROP_LAST = (60, "F", 20), (65, "M", 15)
_AGE_SEX = ("age", "sex")
_PAYOUT_KEYS = ("income_start_age", "sex", "payout_form")
_ROP_KEYS = ("issue_age", "sex", "deferral_years")


def _tables(file, keys, key, column, message, values):
    return [(f"{file}: {what}", file, _cell(file, keys, key, column, value), message)
            for what, value in values]


_BAD = (("blank", NAN), ("written as text", "x"), ("infinite", float("inf")))
_KEY_BAD = (("blank", NAN), ("written as text", "x"), ("fractional", 120.5))


def _age_keyed(file, column, what, out_of_range):
    """The cases of an assumption table keyed by age and sex, ``file``, rate ``column``."""
    cases = _tables(file, _AGE_SEX, _MORT_KEY, column,
                    f"{file}: {column} must be {what}; it is not on line [103]",
                    (*_BAD, out_of_range))
    cases += [(f"{file}: an age {how}", file, _cell(file, _AGE_SEX, _MORT_LAST, "age", v),
               f"{file}: age must be a whole number; it is not on line [203]")
              for how, v in _KEY_BAD]
    cases += [(f"{file}: a sex {how}", file, _cell(file, _AGE_SEX, _MORT_LAST, "sex", v),
               f"{file}: sex must be M or F; it is not on line [203]")
              for how, v in (("blank", NAN), ("neither M nor F", "X"))]
    cases += [(f"{file}: an age and sex on two rows", file,
               _row_again(file, _AGE_SEX, _MORT_KEY),
               f"{file}: each age and sex must have one row; age 70, sex F is on line "
               f"[103, 204]"),
              (f"{file}: an age missing", file, _row_gone(file, _AGE_SEX, _MORT_KEY),
               f"{file}: the ages of each sex must run one row an age, without a gap; no "
               f"line holds age 70 of sex F")]
    return cases


# The malformed assumption tables, as (case, the file, its edit, the message): what the
# count cell beside each of Data's four readers of DIA_US_S's tables refuses, naming the
# file, the column and the lines.  Each value reaches a floor through survival or the
# purchase rates, where a blank would be lost without a word, so each is refused blank,
# written as text, infinite, and outside its table's range: a negative rate or factor, a
# payout factor of 0, which divides the purchase rate, and an improvement rate of 1, which
# makes 1 - G2 zero.  A negative improvement rate, a deterioration, is accepted
# (test_a_negative_improvement_rate_projects_as_s_projects_it).  Each key is read by value:
# an age or a year that is blank, text or not whole is refused, and so is a sex or a payout
# form no join reads, a key on two rows, and, where a join reads every age, a gap.
TABLES = [
    *_age_keyed("mort_table.csv", "mort_rate", "a finite number, zero or more",
                ("negative", -0.001)),
    *_age_keyed("improvement_scale.csv", "improvement_rate", "a finite number below 1",
                ("of 1", 1.0)),
    *_tables("payout_factor_table.csv", _PAYOUT_KEYS, _PAYOUT_KEY, "payout_factor",
             "payout_factor_table.csv: payout_factor must be a finite number above zero; "
             "it is not on line [2]", (*_BAD, ("of 0", 0.0))),
    ("payout_factor_table.csv: an income start age written as text",
     "payout_factor_table.csv",
     _cell("payout_factor_table.csv", _PAYOUT_KEYS, _PAYOUT_LAST, "income_start_age", "x"),
     "payout_factor_table.csv: income_start_age must be a whole number; it is not on line "
     "[5]"),
    ("payout_factor_table.csv: a blank sex", "payout_factor_table.csv",
     _cell("payout_factor_table.csv", _PAYOUT_KEYS, _PAYOUT_LAST, "sex", NAN),
     "payout_factor_table.csv: sex must be M or F; it is not on line [5]"),
    ("payout_factor_table.csv: a payout form no join reads", "payout_factor_table.csv",
     _cell("payout_factor_table.csv", _PAYOUT_KEYS, _PAYOUT_LAST, "payout_form", "LO_ROP"),
     "payout_factor_table.csv: payout_form must be LO, CR, IR or PC; it is not on line "
     "[5]"),
    ("payout_factor_table.csv: a key on two rows", "payout_factor_table.csv",
     _row_again("payout_factor_table.csv", _PAYOUT_KEYS, _PAYOUT_LAST),
     "payout_factor_table.csv: each income_start_age, sex and payout_form must have one "
     "row; income_start_age 80, sex M, payout_form LO is on line [5, 6]"),
    *_tables("rop_factor_table.csv", _ROP_KEYS, _ROP_KEY, "rop_factor",
             "rop_factor_table.csv: rop_factor must be a finite number, zero or more; it "
             "is not on line [2]", (*_BAD, ("negative", -0.1))),
    ("rop_factor_table.csv: an issue age written as text", "rop_factor_table.csv",
     _cell("rop_factor_table.csv", _ROP_KEYS, _ROP_LAST, "issue_age", "x"),
     "rop_factor_table.csv: issue_age must be a whole number; it is not on line [5]"),
    ("rop_factor_table.csv: a fractional deferral", "rop_factor_table.csv",
     _cell("rop_factor_table.csv", _ROP_KEYS, _ROP_LAST, "deferral_years", 15.5),
     "rop_factor_table.csv: deferral_years must be a whole number; it is not on line [5]"),
    ("rop_factor_table.csv: a sex neither M nor F", "rop_factor_table.csv",
     _cell("rop_factor_table.csv", _ROP_KEYS, _ROP_LAST, "sex", "m"),
     "rop_factor_table.csv: sex must be M or F; it is not on line [5]"),
    ("rop_factor_table.csv: a key on two rows", "rop_factor_table.csv",
     _row_again("rop_factor_table.csv", _ROP_KEYS, _ROP_LAST),
     "rop_factor_table.csv: each issue_age, sex and deferral_years must have one row; "
     "issue_age 65, sex M, deferral_years 15 is on line [5, 6]"),
]

# Each table's reader, DIA_US_S's and unchanged, its count cell, which checks it, and the
# point its refusal is read through, one whose projection reads the table: the anchor's
# twin reads the mortality table and, on the table basis, both factor tables; the
# generational twin reads the improvement scale.
TABLE_READERS = {"mort_table.csv": ("mort_table", "mort_table_count", 1),
                 "improvement_scale.csv": ("improvement_scale", "improvement_scale_count",
                                           16),
                 "payout_factor_table.csv": ("payout_factor_table", "payout_factor_count",
                                             1),
                 "rop_factor_table.csv": ("rop_factor_table", "rop_factor_count", 1)}


@pytest.mark.parametrize("case, file, edit, message", TABLES, ids=[c[0] for c in TABLES])
def test_a_malformed_assumption_table_is_refused_naming_the_file(tmp_path, case, file,
                                                                 edit, message):
    """Each assumption table's count cell refuses a key or a value the joins cannot use,
    and a projection meets the refusal.

    The four tables are ``DIA_US_S``'s files, read in place by both models, so each case is
    read by a model of its own from a copy of the inputs with the one fault.
    ``DIA_US_S``'s reader, unchanged, reads the table as it stands; the count cell beside
    it refuses it, naming the file, the column and the lines at fault (§7.1, *Precised at
    M3*, item 9); and the point named in :data:`TABLE_READERS`, whose projection reads that
    table, meets the same refusal in its ``result_cf()`` before it computes a number,
    because the join asks the count before it reads a value.
    """
    model = _read(_sec_inputs(tmp_path, _committed(), {file: edit}), "table")
    reader, count, point_id = TABLE_READERS[file]
    try:
        assert len(model.Data.cells[reader]()) > 0
        _refused(model.Data.cells[count], message)
        _refused(_point(model, point_id).result_cf, message)
    finally:
        model.close()


def test_a_negative_improvement_rate_projects_as_s_projects_it(tmp_path):
    """An improvement rate below 0 is a deterioration, which both models project alike, and
    a scale of whole zeros is read by value.

    The generational basis improves the base rate by ``(1 - G2) ** k``, so a negative rate
    raises it year on year, which ``DIA_US_S`` projects without complaint and this model's
    reader accepts: on a copy of both models' inputs whose scale is -0.01 at every age, the
    generational twin's ``result_cf`` is S's point 16's, to 1e-9, and its rate at the
    income start month is above the anchor basis's.  And a scale written as the integer 0
    throughout, read as int64, is read by value: the generational twin then projects what
    the twin on the anchor basis, point 3, projects, in every column.
    """
    worse = {"improvement_scale.csv": lambda df: df.assign(improvement_rate=-0.01)}
    sec = _read(_sec_inputs(tmp_path / "sec", _committed(), worse), "worse")
    s = _read(temp_inputs(tmp_path / "s", model_path(TWIN), edits=worse), "s_worse")
    try:
        p, s16 = _point(sec, 16), _point(s, 16)
        assert frame_mismatches(s16.result_cf(), p.result_cf()) == []
        assert p.mort_rate(240, 1) > _point(sec, 3).mort_rate(240, 1)
    finally:
        s.close()
        sec.close()
    zero = {"improvement_scale.csv": lambda df: df.assign(improvement_rate=0)}
    folder = _sec_inputs(tmp_path / "zero", _committed(), zero)
    flat = _read(folder, "flat")
    try:
        assert flat.Data.improvement_scale()["improvement_rate"].dtype == "int64"
        assert frame_mismatches(_point(flat, 3).result_cf(), _point(flat, 16).result_cf(),
                                rtol=0.0, atol=0.0) == []
    finally:
        flat.close()


# The four assumption tables with every age and year written as a float, as one blank or
# one 70.0 in a key column makes pandas read it.
FLOAT_KEYS = {
    "mort_table.csv": lambda df: df.assign(age=df["age"].astype(float)),
    "improvement_scale.csv": lambda df: df.assign(age=df["age"].astype(float)),
    "payout_factor_table.csv": lambda df: df.assign(
        income_start_age=df["income_start_age"].astype(float)),
    "rop_factor_table.csv": lambda df: df.assign(
        issue_age=df["issue_age"].astype(float),
        deferral_years=df["deferral_years"].astype(float)),
}


def test_an_assumption_tables_keys_written_as_floats_are_read_by_value(sec_model,
                                                                       tmp_path):
    """An assumption table whose keys are written as floats is read as the same table.

    The joins match each key by value, as ``DIA_US_S``'s do, and each count cell reads the
    keys by value too.  On a copy of the inputs whose four tables carry every age and every
    year written as a float (:data:`FLOAT_KEYS`), ``DIA_US_S``'s readers read the keys as
    floats, each count cell counts what it counts on the committed tables, and the
    anchor's twin, which reads the mortality table and both factor tables on the table
    basis, and the generational twin, which reads the improvement scale, project exactly
    what the committed model projects.
    """
    model = _read(_sec_inputs(tmp_path, _committed(), FLOAT_KEYS), "float_keys")
    try:
        assert model.Data.mort_table().index.levels[0].dtype == "float64"
        for name in ("mort_table_count", "improvement_scale_count", "payout_factor_count",
                     "rop_factor_count"):
            assert model.Data.cells[name]() == sec_model.Data.cells[name](), name
        for point_id in (1, 16):
            assert frame_mismatches(_point(sec_model, point_id).result_cf(),
                                    _point(model, point_id).result_cf(), rtol=0.0,
                                    atol=0.0) == [], point_id
    finally:
        model.close()


# The points a rule of the product refuses, each in proj_len() and each by name, with the
# reason by form: a point at or past the stop rule, and a contract that owes nothing after
# the valuation date, every covered life having died before its income start month, whose
# death benefit was paid, or after it, its certain period over or the form having none,
# the refund, if any, having been paid at the last death.  The table reads in each: the
# rules need the certain period, which an installment refund derives in Projection.  Each
# window is refused at its first month and at its last and read just outside it (the
# edges test), USLIB-SEC-PLAN.md §5.2's T5 (precised at M10): every life dead in deferral
# at 1, the first month in force, and at 240, the income start month, where the at-issue
# check refuses 0, and read inside the guarantee at 241; after the period certain's
# guarantee at 360 and 719, the frame's last month, and read at 359; and on a form with
# no certain period at 241 and 719.  The stop rule is refused at 720 and read at 719, the
# committed row 25; past each frame's last month the stop rule refuses first.  As (case,
# point_id, edit, message).
_OWED = "point_id {p}: duration_mth {d}: no payment is owed after the valuation date: "
# Row 21, a month after its full commutation at policy month 252, accelerating inside the
# guarantee that runs to 359: six months after the commutation, the least the interlock
# allows, so that Data reads the table and only proj_len() refuses it; and at 358, where
# the lump sum pulls forward 359, the guarantee's last month, valued before the exercise
# and at it.  The commuting twin, point 15, accelerating at 258 on the books from issue,
# at the valuation date and issued 120 months on, the window's first month.  An
# acceleration at 359, which pulls forward the life tail alone, and one valued a month
# after it, its lump sum paid, are read (the edges test).
_ACCEL = ("point_id {p}: accel_mth {a} pulls forward guaranteed instalments that the "
          "commutation at policy month 252 reduced, the guarantee running to policy month "
          "359: the lump sum would pay the cohort that commuted its instalments again")
REFUSED = [
    ("past the stop rule", 25, _set("duration_mth", [25], 720),
     "point_id 25: duration_mth 720 is at or past the end of the projection, policy "
     "month 720"),
    ("every life dead in deferral", 18, _set("lives_if_init_1", [18], 0.0),
     _OWED.format(p=18, d=59) + "every covered life has died before the income start "
     "month, 240"),
    ("every life dead at the income start month", 20,
     _moved(20, 240, lives_if_init_1=0.0, surv_to_payout_init=NAN),
     _OWED.format(p=20, d=240) + "every covered life has died before the income start "
     "month, 240"),
    ("every life dead after the certain period", 20,
     _moved(20, 360, lives_if_init_1=0.0),
     _OWED.format(p=20, d=360) + "every covered life has died, and the certain period "
     "ended at policy month 360"),
    ("every life dead, no certain period", 19, _set("lives_if_init_1", [19], 0.0),
     _OWED.format(p=19, d=241) + "every covered life has died, and the form has no "
     "certain period"),
    ("both joint lives dead, no certain period", 23, _set("lives_if_init_1", [23], 0.0),
     _OWED.format(p=23, d=672) + "every covered life has died, and the form has no "
     "certain period"),
    ("an acceleration six months after a commutation, inside its guarantee", 21,
     _set("accel_mth", [21], 258), _ACCEL.format(p=21, a=258)),
    ("an acceleration pulling forward a guarantee's last month", 21,
     _set("accel_mth", [21], 358), _ACCEL.format(p=21, a=358)),
    ("an acceleration inside a commuted guarantee at the valuation date", 21,
     _moved(21, 358, accel_mth=358), _ACCEL.format(p=21, a=358)),
    ("an acceleration inside a commuted guarantee at issue", 15,
     _set("accel_mth", [15], 258), _ACCEL.format(p=15, a=258)),
    ("an acceleration inside a commuted guarantee issued at the horizon", 15,
     _moved(15, -120, accel_mth=258), _ACCEL.format(p=15, a=258)),
    ("every life dead in the first month in force", 18,
     _moved(18, 1, lives_if_init_1=0.0),
     _OWED.format(p=18, d=1) + "every covered life has died before the income start "
     "month, 240"),
    ("every life dead in the last month, after the certain period", 20,
     _moved(20, 719, lives_if_init_1=0.0),
     _OWED.format(p=20, d=719) + "every covered life has died, and the certain period "
     "ended at policy month 360"),
    ("every life dead in the last month, no certain period", 25,
     _set("lives_if_init_1", [25], 0.0),
     _OWED.format(p=25, d=719) + "every covered life has died, and the form has no "
     "certain period"),
]


@pytest.mark.parametrize("case, point_id, edit, message", REFUSED,
                         ids=[c[0] for c in REFUSED])
def test_a_point_owing_nothing_is_refused_by_proj_len(tmp_path, case, point_id, edit,
                                                      message):
    """A point with no frame left is read, and refused by ``proj_len()`` by name (D6, T5).

    The rules need ``stop_mth()`` and the certain period, which an installment refund
    derives from its payout schedule in ``Projection``, so they are rules of the product,
    not of the table: the table reads, and the point is refused where its frame is defined,
    on its first projection, rather than projecting nothing.  An in-force extract should
    carry neither kind of point: a contract that owes nothing has paid its death benefit,
    its last instalment or its refund before the valuation date, as ``Term_US_SEC``'s point
    past its cover has ended.  The other points of the same table project.
    """
    model = _read_edited(tmp_path, edit, "refused")
    try:
        assert len(model.Data.model_point_table()) == len(_committed())
        _refused(_point(model, point_id).result_cf, message)
        assert len(_point(model, 24).result_cf()) > 0
    finally:
        model.close()


def test_the_future_horizon_is_a_reference_that_bounds_future_business(tmp_path):
    """``Data.future_horizon_mth`` refuses a contract issued later, and 0 refuses all.

    The committed table's one future point is issued 13 months on.  It reads at the shipped
    120 months and at 13, the shortest horizon that admits it, where it also projects, and
    is refused at 12, by name.  At 0 the model takes no future new business, D4's fallback
    for a product that cannot support it, and the message says so.  A negative horizon is
    itself refused.  Each value is set on a model read for it, before the model computes
    anything.
    """
    future = _label(_committed(), "future", 8, -13)
    later = (f"model_point_table_sec.csv: duration_mth must be -12 or more, a policy "
             f"issued at most 12 months after the valuation date; it is not at point_id "
             f"[{future}]")
    no_future = (f"model_point_table_sec.csv: duration_mth must be 0 or more: this model "
                 f"takes no future new business; it is not at point_id [{future}]")
    negative = "future_horizon_mth must be 0 months or more, not -1"
    folder = _sec_inputs(tmp_path, _committed())
    shipped = _read(folder, "horizon")
    try:
        assert shipped.Data.future_horizon_mth == 120
    finally:
        shipped.close()
    for horizon, refusal in ((120, None), (13, None), (12, later), (0, no_future),
                             (-1, negative)):
        model = _read(folder, "horizon", data={"future_horizon_mth": horizon})
        try:
            if refusal is None:
                assert len(model.Data.model_point_table()) == len(_committed()), horizon
                if horizon == 13:
                    late = _point(model, future)
                    assert (late.proj_len(), late.pols_new_biz(13)) == (733, 1.0)
                    assert late.result_cf()["premiums"].iloc[13] == 100000.0
            else:
                _refused(model.Data.model_point_table, refusal)
        finally:
            model.close()


# The integer and state columns the edges test writes as floats, as one blank or one 1.0 in
# a column makes pandas read it.
_WHOLE = ("duration_mth", "income_start_mth", "certain_period", "frequency", "issue_age",
          "joint_age", "issue_year", "purchase_rate_dp", "policy_count", "adjust_mth",
          "adjust_start_mth", "accel_mth", "commute_mth", *STATE)

# The columns Data reads by value and returns as the numbers it checked them as.
_CHECKED = ("income_start_mth", "adjust_mth", "adjust_start_mth", "accel_mth",
            "commute_mth", "issue_age", "joint_age", "certain_period", "frequency",
            "issue_year", "purchase_rate_dp", "survivor_pct", "cola_rate",
            "other_qlac_premium", "commute_frac")


def test_the_edges_of_the_in_force_interface_are_accepted(sec_model, tmp_path):
    """A zero count, whole numbers in any type, the horizon and the checks' edges are read.

    A count of 0 is a point that projects zeros.  The integer columns written as floats,
    as one blank or one ``1.0`` in a column makes pandas read it, and the premium months of
    the schedule likewise, are read by value, and the other rows in force or issued later
    and the twins that carry each flow (:data:`FLOW_TWINS`) project exactly what the
    committed table projects: ``12.0`` is the int the policy clock counts in.  ``Data``
    returns the columns it read by value as the numbers it checked them as.  A contract
    issued 120 months after the valuation date, the shipped ``future_horizon_mth``, is the
    last one the table admits, with a frame of 840 months, 720 to the stop rule after 120
    before it.  An option month written -1, on a contract that never exercises it, is never,
    as ``DIA_US_S`` reads one, and changes no number.  A fall in the reference rate since
    issue is a change like any other: 25 basis points down on the commuted contract.  A
    premium after the elected income start month but before the adjusted one, at policy
    month 250 on the adjustment's twin, deferred to 300, is a premium of the deferral,
    priced to the new start month.  And a contract with every life dead inside its
    guarantee pays its beneficiary, through the frozen ``l_last(T)``: the period certain at
    300 with its life dead pays 0.715 of each instalment until its guarantee ends at policy
    month 360, ``t = 60``, and nothing after.

    Each window of contract months is read just outside it (USLIB-SEC-PLAN.md §5.2, T5,
    precised at M10), by copies of committed rows appended under ids of their own, each
    with its source's premiums still due, and each reading and projecting its whole frame
    in finite numbers: an income start month of 0, the least a policy month can be; the
    adjustment exercised the month before the income start month, and the new start month
    the month after the exercise; an acceleration and a commutation at the income start
    month, 240, and an acceleration at the adjustment's 300; a commutation at -1, never; an
    acceleration six months before a commutation; the deferral row a month in force, its
    guarantee-period column given; the anchor at its income start month and the commuting
    point at its commutation month, each frozen weight blank and derived; a premium due in
    the valuation month and one the month before the income start month; the period
    certain with its life dead at 241 and 359, inside its guarantee, paying its
    beneficiary; and an acceleration inside a commuted guarantee valued the month after
    it, its lump sum paid, and one in the guarantee's last month, which pulls forward the
    life tail alone.  And each bound between the frozen weights and the lives is read at
    equality: ``l_last(t_c)`` at ``l_last(T)``, and each weight at the life alive.
    """
    committed = _committed()
    zero = _label(committed, "derived", 1, 241)
    later = _label(committed, "future", 8, -13)
    dead = _label(committed, "derived", 7, 300)
    fall = _label(committed, "derived", 15, 253)
    deferral = _label(committed, "derived", 14, 59)
    copies = {101: (zero, {"income_start_mth": 0.0}),
              102: (13, {"adjust_mth": 239.0}),
              103: (13, {"adjust_start_mth": 121.0}),
              104: (14, {"accel_mth": 240.0}),
              105: (13, {"accel_mth": 300.0}),
              106: (15, {"commute_mth": 240.0}),
              107: (15, {"commute_mth": -1.0}),
              108: (15, {"accel_mth": 246.0}),
              109: (deferral, {"duration_mth": 1.0}),
              110: (zero, {"duration_mth": 240.0, "surv_to_payout_init": NAN}),
              111: (fall, {"duration_mth": 252.0, "commute_weight_init": NAN}),
              112: (fall, {"surv_to_payout_init": 0.75, "commute_weight_init": 0.75}),
              113: (zero, {"lives_if_init_1": 0.5, "surv_to_payout_init": 0.5}),
              114: (fall, {"lives_if_init_1": 0.5, "commute_weight_init": 0.5}),
              115: (deferral, {}),
              116: (17, {}),
              117: (dead, {"duration_mth": 241.0, "lives_if_init_1": 0.0}),
              118: (dead, {"duration_mth": 359.0, "lives_if_init_1": 0.0}),
              119: (fall, {"duration_mth": 359.0, "accel_mth": 358.0}),
              120: (fall, {"accel_mth": 359.0})}

    def edit(table):
        table = table.assign(**{c: table[c].astype(float) for c in _WHOLE})
        rows = [table.loc[[row]].assign(**changes).set_axis([label])
                for label, (row, changes) in copies.items()]
        table = pd.concat([table, *rows]).rename_axis("point_id")
        table = _set("policy_count", [zero], 0.0)(table)
        table = _set("duration_mth", [later], -120.0)(table)
        table = _set("accel_mth", [1], -1.0)(table)
        table = _set("ref_rate_shift_init", [fall], -0.0025)(table)
        return _set("lives_if_init_1", [dead], 0.0)(table)

    def schedule_edit(schedule):
        rows = [schedule[schedule["point_id"] == row].assign(point_id=label)
                for label, (row, _) in copies.items()]
        schedule = pd.concat([schedule, *rows], ignore_index=True)
        schedule = _added(115, 59)(_added(116, 239)(_added(13, 250)(schedule)))
        return schedule.assign(premium_mth=schedule["premium_mth"].astype(float))

    model = _read_edited(tmp_path, edit, schedule_edit=schedule_edit)
    try:
        read = model.Data.model_point_table()
        assert all(read[c].dtype == float for c in (*_WHOLE, *_CHECKED)), read.dtypes
        assert len(read) == len(committed) + len(copies)
        for label in copies:
            key = _key(model, label)
            frame = projection(model, key).result_cf()
            assert len(frame) == projection(model, key).proj_len() > 0, label
            assert all(math.isfinite(v) for v in frame.to_numpy().ravel()), label
            _release(model, key)
        at = {label: _point(model, label) for label in copies}
        assert at[101].income_start_mth() == 0
        assert (at[102].adjust_mth(), at[102].income_start_mth()) == (239, 300)
        assert (at[103].adjust_mth(), at[103].income_start_mth()) == (120, 121)
        assert at[104].accel_mth() == at[104].income_start_mth() == 240
        assert at[105].accel_mth() == at[105].income_start_mth() == 300
        assert at[106].commute_mth() == at[106].income_start_mth() == 240
        assert (at[107].commute_mth(), at[108].accel_mth()) == (-1, 246)
        assert at[109].duration_mth(0) == 1 and at[109].guarantee_mths_pricing_init() > 0
        assert at[110].duration_mth(0) == at[110].income_start_mth() == 240
        assert at[111].duration_mth(0) == at[111].commute_mth() == 252
        assert at[111].commutations(0) > 0.0
        assert at[112].commute_weight_init() == at[112].surv_to_payout_init() == 0.75
        assert at[113].surv_to_payout_init() == at[113].lives_if_init(1) == 0.5
        assert at[114].commute_weight_init() == at[114].lives_if_init(1) == 0.5
        assert (at[115].premium_pp(0), at[116].premium_pp(239)) == (1000.0, 1000.0)
        for label in (117, 118):
            paid = [at[label].annuity_payments(t) for t in range(at[label].proj_len())]
            last = 360 - at[label].duration_mth_init()
            assert at[label].lives_if_last(0) == 0.0 and all(paid[:last]), label
            assert paid[last:] == [0.0] * (len(paid) - last), label
        assert at[119].accel_mth() == at[119].duration_mth_init() - 1
        assert at[120].accel_mth() == 359
        assert model.Data.premium_schedule_table()["premium_mth"].dtype == "int64"
        df = _point(model, zero).result_cf()
        assert len(df) == 479 and (df == 0.0).all().all()
        deferred = _point(model, 13)
        assert deferred.income_start_mth() == deferred.income_start_mth_at(250) == 300
        assert deferred.premium_pp(250) == 1000.0
        assert deferred.annual_income(250) == pytest.approx(
            deferred.annual_income(249) + 1000.0 * deferred.purchase_rate(250), rel=1e-15)
        assert deferred.annual_income_payout() == deferred.annual_income(250)
        for point_id in sorted(set(_flow_points(committed)) - {zero, later, dead}):
            key = _key(model, point_id)
            assert frame_mismatches(_point(sec_model, point_id).result_cf(),
                                    projection(model, key).result_cf(), rtol=0,
                                    atol=0) == [], point_id
            _release(model, key)
        p = _point(model, 18)
        assert p.duration_mth(0) == 59 and type(p.duration_mth(0)) is int
        assert p.income_start_mth() == 240 and type(p.income_start_mth()) is int
        assert p.accel_mth() == 252 and type(p.accel_mth()) is int
        assert _point(model, 1).accel_mth() == -1
        late = _point(model, later)
        assert (late.t_entry(), late.proj_len(), late.pols_new_biz(120)) == (120, 840, 1.0)
        assert late.result_cf().loc[:119].eq(0.0).all().all()
        assert late.premiums(120) == 100000.0
        moved = _point(model, fall)
        assert moved.ref_rate_shift_init() == -0.0025
        assert moved.commute_disc_rate(0) == pytest.approx(0.0525, rel=1e-12)
        gone = _point(model, dead)
        assert gone.lives_if_last(0) == 0.0 and gone.pols_if(0) == 0.0
        paid = [gone.annuity_payments(t) for t in range(gone.proj_len())]
        assert paid[:60] == [gone.annuity_pp_sched(t) * gone.surv_to_payout()
                             for t in range(60)]
        assert gone.surv_to_payout() == pytest.approx(0.715, rel=1e-9)
        assert paid[60:] == [0.0] * (len(paid) - 60)
    finally:
        model.close()


# Every state DIA_US_S reaches, restated in force at its month, is an opening state Data's
# checks and proj_len()'s accept, but a state the product refuses by name: a check
# exercised only on the rows the tests above choose could refuse a state S reaches
# elsewhere (D6).  DIA_US_S keeps a contract on its books after it owes nothing, every
# covered life dead before its income start month or after its certain period, or on a
# form with none, and projects it as zeros to its stop rule, where proj_len() refuses it by
# name (REFUSED): the every-state test sets each such state aside and shows it refused.


def _every_state_months(sp):
    """The months S point ``sp``, projected, is restated at by the every-state test.

    By default the edges of each window a check of ``Data`` or ``proj_len()`` reads a
    month against (USLIB-SEC-PLAN.md §5.2, T5, precised at M10): policy month 1, the first
    past the at-issue check's window and inside the guarantee-period column's; each
    premium month and the month after it, where the premium leaves the schedule for the
    premiums paid; the income start month in force and the month either side, where the
    deferral ends and ``l_last(T)`` becomes a column; the month of the first instalment and
    the month after it, below monthly in arrears a payment step after the income start
    month; each option month and the month after it, where ``l_last(t_c)`` becomes a
    column and an acceleration leaves the books; the guarantee's last month and the first
    after it; the month before each covered life's survival reaches 0, and the month it
    does; and the frame's last month, before the stop rule.  With ``USLIB_SEC_FULL=1``,
    every month of its frame.
    """
    n = sp.proj_len()
    if SEC_FULL:
        return list(range(1, n))
    start = sp.income_start_mth()
    end = start + sp.certain_mths_eff()
    first = next(t for t in range(start, n) if sp.is_payment_mth(t))
    months = {1, start - 1, start, start + 1, first, first + 1, end - 1, end, n - 1}
    for m in (*sp.premium_by_mth(), sp.adjust_mth(), sp.accel_mth(), sp.commute_mth()):
        if m >= 0:
            months |= {m, m + 1}
    for life in _lives(sp):
        zero = next((d for d in range(n) if sp.lives_if(d, life) == 0.0), None)
        if zero is not None:
            months |= {zero - 1, zero}
    return sorted(d for d in months if 1 <= d < n)


def _owing(sp, d):
    """Why S point ``sp`` restated at month ``d`` owes nothing after it, as ``proj_len()``
    says it, or None where it owes a payment.

    As ``proj_len()`` reads a contract in force with every covered life dead,
    ``DIA_US_S``'s survival exactly 0: valued at or before its income start month in
    force, or at or after the end of its certain period, or on a form with none.  Inside a
    guarantee the beneficiary is paid.
    """
    if any(sp.lives_if(d, life) > 0.0 for life in _lives(sp)):
        return None
    start = sp.income_start_mth()
    end = start + sp.certain_mths_eff()
    if d <= start:
        return f"every covered life has died before the income start month, {start}"
    if d < end:
        return None
    if end > start:
        return (f"every covered life has died, and the certain period ended at policy "
                f"month {end}")
    return "every covered life has died, and the form has no certain period"


def _every_state_table(root, s, edits):
    """The states ``s``'s points reach, restated in force: ``(folder, rows, owing)``.

    Each month of :func:`_every_state_months` of each point of ``s``, an S model already
    swept, a derived row of a table the generator builds beside every point's twin, with
    its premium schedule, written into ``folder`` under ``root`` with ``edits`` beside
    them, the inputs S read (:func:`_sec_built`).  ``rows`` is the table's length, and
    ``owing`` holds ``{(S point, month): why}`` for each state owing nothing
    (:func:`_owing`).
    """
    states, owing = [], {}
    for key, point_id in zip(point_keys(s), s.Data.model_point_table().index):
        sp = projection(s, key)
        for d in _every_state_months(sp):
            states.append((point_id, d))
            why = _owing(sp, d)
            if why is not None:
                owing[(point_id, d)] = why
    folder = _sec_built(root, s, states, (), edits)
    return folder, len(s.Data.model_point_table()) + len(states), owing


def _departures(model, rows, owing):
    """Where ``Data`` and ``proj_len()`` depart from what the every-state test expects.

    ``model`` holds a table of ``rows`` rows (:func:`_every_state_table`), which ``Data``
    must read, and its premium schedule.  Each row's ``proj_len()`` must give a frame, but
    a state of ``owing``, ``{(S point, month): why}``, which it must refuse, naming the
    row, its month and why.  Each row is released once asked, the collector run every
    500.  Returns each departure, the line that names it.
    """
    try:
        table = model.Data.model_point_table()
        model.Data.premium_schedule_table()
    except Exception as err:                    # reported, with the rows' states
        return [f"Data: {_raised(err)}"]
    assert len(table) == rows
    twins = table.index[table["row_kind"] == "twin"]
    point_of = dict(zip(table.loc[twins, "policy_id"], twins))
    found = []
    for i, (key, label) in enumerate(zip(point_keys(model), table.index)):
        state = (point_of[table.at[label, "source_policy_id"]],
                 int(table.at[label, "source_mth"]))
        why = owing.get(state) if table.at[label, "row_kind"] == "derived" else None
        try:
            projection(model, key).proj_len()
            if why is not None:
                found.append(f"point_id {label}, S point {state}: it has a frame")
        except Exception as err:                # reported, so every row is asked
            text = str(err)
            if why is None or not ("ValueError" in text
                                   and _OWED.format(p=label, d=state[1]) + why in text):
                found.append(_raised(err))
        _release(model, key, collect=i % 500 == 499)
    return found


def test_every_state_s_reaches_is_accepted_in_force(s_model, spliced, tmp_path):
    """Every state ``DIA_US_S`` reaches is a valid opening state, but one owing nothing.

    ``Data``'s checks and ``proj_len()``'s hold an opening state to what a contract in
    force can be, so they must accept each state the S model reaches (D6).  So every S
    point, swept, is restated in force by the generator at the edges of its windows, or
    with ``USLIB_SEC_FULL=1`` at every month of its frame (:func:`_every_state_months`),
    into one table beside the twins, with its premiums still due: ``Data`` reads the table
    and the schedule, and every row's ``proj_len()`` gives a frame.  But for the states set
    aside, which ``DIA_US_S`` keeps on its books, projecting zeros to its stop rule, and
    ``proj_len()`` refuses, each by name, its row, its month and why it owes nothing
    (:func:`_owing`): on the splice, variant 18, the anchor on a male life on the table
    basis, dead from policy month 685, after mortality's cap at 117, its form a cash refund
    with no certain period (USLIB-SEC-PLAN.md §5.2, T5, precised at M10).  No state S
    reaches is an acceleration ``proj_len()`` refuses: no point accelerates inside a
    guarantee a commutation before it reduced.

    It runs under each set of inputs on which the states S reaches differ (§5.2, T5,
    precised at M9).  S's shipped References, on S's own table: the committed S model,
    whose points see no change in the reference rate, price at the shipped A/E of 1 and
    reprice at the pricing rate, and none of whose contracts has every covered life dead
    before its stop rule, so that none owes nothing.  And the splice's References,
    set-apart tables and variants (:data:`SPLICED_REFS`): the reference rate up 50 basis
    points in every state, and the A/E at 1.05, under which variant 18's male life reaches
    mortality's cap at 117 and dies with certainty.  Under :data:`LATER_REFS`, under which
    the splice reads S a second time, S's states are the splice's but for the reference
    rate's change, 0 as under the shipped References, which ``Data`` holds only to be a
    number.  The splice's table is built while its S model is swept, in the ``spliced``
    fixture, before T2 releases its points.
    """
    sets = (("shipped", _every_state_table(tmp_path / "shipped", s_model, None), {},
             set()),
            ("spliced", spliced[4], SEC_REFS, {18}))
    for name, (folder, rows, owing), refs, owing_points in sets:
        assert {p for p, _ in owing} == owing_points, (name, sorted(owing)[:5])
        model = _read(folder, "every", refs)
        try:
            found = _departures(model, rows, owing)
        finally:
            model.close()
        assert not found, f"{name}: {len(found)} departures, first: {found[:5]}"


# What the decodes refuse, as (case, the table's edit, the point, the cell it is read
# through, its message): each text value a projection branches on, and the frequency,
# which picks its payment months.  The decodes read the model point's columns and validate
# them as DIA_US_S's label accessors do, so an invalid value raises S's own message
# wherever the projection first meets it, and only the rule under test refuses each case:
# the form on a twin, whose guarantee-period column is blank whatever its form; the trigger
# on a joint point, where the payment factor and the pricing kernel read it.  The market
# type is read by the QLAC overlay alone, as in S, so its refusal is met there, and every
# cash flow of the point projects.
UNDECODABLE = [
    ("an unknown reduction trigger", _set("reduction_trigger", [8], "first"), 8,
     "result_cf", "invalid reduction_trigger"),
    ("an unknown income form", _set("income_form", [3], "LCR"), 3, "result_cf",
     "invalid income_form"),
    ("an unknown death-benefit form", _set("db_form", [3], "RCP"), 3, "result_cf",
     "invalid db_form"),
    ("an unknown payment timing", _set("timing", [17], "middle"), 17, "result_cf",
     "invalid timing"),
    ("an unknown mortality basis", _set("mort_basis", [16], "select"), 16, "result_cf",
     "invalid mort_basis"),
    ("an unknown factor basis", _set("factor_basis", [3], "tabular"), 3, "result_cf",
     "invalid factor_basis"),
    ("an unknown frequency", _set("frequency", [1], 5), 1, "result_cf",
     "invalid frequency"),
    ("an unknown market type", _set("market_type", [11], "IRA"), 11, "qlac_flags",
     "invalid market_type"),
]


@pytest.mark.parametrize("case, edit, point_id, cell, message", UNDECODABLE,
                         ids=[c[0] for c in UNDECODABLE])
def test_an_undecodable_value_is_refused_where_the_projection_meets_it(tmp_path, case,
                                                                        edit, point_id,
                                                                        cell, message):
    """An invalid switch raises ``ValueError`` with S's message, not a quiet default.

    Each case is read by a model of its own, from a copy of the inputs with the one fault.
    The table reads, because these are rules of the projection, not of the in-force
    interface, and the point's projection meets the fault on its way to its first number.
    A decode that read an unknown form as a life annuity, or an unknown trigger as the
    primary's, would project a contract no one wrote.  The market type is read only by the
    QLAC overlay, which refuses it, while the cash flows, which it does not reach, project.
    """
    model = _read_edited(tmp_path, edit, "undecodable")
    try:
        assert len(model.Data.model_point_table()) == len(_committed())
        p = _point(model, point_id)
        _refused(p.cells[cell], message)
        if cell != "result_cf":
            assert len(p.result_cf()) == p.proj_len()
    finally:
        model.close()


def test_a_life_a_kind_or_a_timing_neither_model_knows_is_refused(sec_model):
    """A third life, an unknown claim kind or timing raises, rather than answers.

    The opening state, the issue ages, the two age-keyed table readers, the pricing
    survival and the projection's take a life, 1 or 2, as ``DIA_US_S``'s ``age_at_entry``
    does; ``claim_pp`` takes the two kinds, ``"DEATH"`` and ``"REFUND"``; and ``pols_if_at``
    the two timings, ``BasicTerm_SE``'s ``"BEF_NB"`` and ``"BEF_DECR"`` (the count test asks
    for ``"BEF_MAT"``).  Each refuses anything else with ``ValueError`` instead of
    answering with another life's, kind's or timing's number.
    """
    p = _row(sec_model, "derived", 1, 241)
    for call, message in ((lambda: p.lives_if_init(3), "invalid life"),
                          (lambda: p.age_at_entry(3), "invalid life"),
                          (lambda: p.mort_rate_base_at(70, 3), "invalid life"),
                          (lambda: p.improvement_rate_at(70, 3), "invalid life"),
                          (lambda: p.lives_if_pm(12, 3), "invalid life"),
                          (lambda: p.lives_if(0, 3), "invalid life"),
                          (lambda: p.claim_pp(0, "LAPSE"), "invalid kind"),
                          (lambda: p.pols_if_at(0, "AFT_DECR"), "invalid timing")):
        _refused(call, message)


# ---------------------------------------------------------------------------
# T6 -- regeneration


def test_the_committed_sec_files_are_what_s_generates(s_model):
    """``model_point_table_sec.csv`` and ``premium_schedule_sec.csv`` are what DIA_US_S and
    its inputs generate today.

    Every row and column of both files, the text cells and the opening-state columns
    included: an edit to an S row or a premium the files copy or derive from, or to an S
    formula a row's state is read from, fails here until ``python tools/gen_sec_points.py
    DIA_US_SEC`` regenerates them, in the same commit.  Text and integers compare exactly,
    and a float by its value, to 1e-12, because the text the writer picks for a computed
    float depends on the platform's parser (§5.2).  The premium schedule is the spec's one
    companion, so both files are checked.
    """
    assert set(SPEC.companions) == {SCHEDULE}
    assert check_generated(SEC, s_model=s_model) == []


def test_every_committed_row_continues_its_s_point(sec_model, s_model):
    """Each derived and future row of the committed table is its S point from its month on.

    T6 holds the committed table to what the generator makes of ``DIA_US_S``, each float to
    1e-12 absolute and relative, which pins a probability as small as the anchor's survival
    in its last month, 6.1e-08, only to about 1.6e-5 of itself, and says nothing of what the
    model makes of a row.  So each derived and future row is projected too, at the shipped
    assumptions, and compared with its S point from the row's ``source_mth`` on
    (:func:`_continues_s`): ``result_cf`` and ``result_pols`` frame by frame, and every
    other cell of S's at every argument S cached, to 1e-9 relative with no absolute floor,
    the roll-forward residuals at the floor.  The eight rows restated in force skip what
    the splice skips.  The joint point issued 13 months on, its ``source_mth`` -13, holds
    its whole premium schedule and whole policy years, so its premiums by month and its
    annual display are compared too, as T3 compares future business on the splice's
    inputs.  The shipped expense inflation runs from issue in S and from the valuation date
    here (D7), so the cells it moves are left out; the inflation test holds them.
    """
    table = sec_model.Data.model_point_table()
    rows = table.index[table["row_kind"] != "twin"]
    assert set(table.loc[rows, "row_kind"]) == {"derived", "future"}
    for point_id in rows:
        month = int(table.at[point_id, "source_mth"])
        later = table.at[point_id, "row_kind"] == "future"
        p, s = _point(sec_model, point_id), _source(s_model, table, point_id)
        found = _continues_s(s, p, month, FUTURE_EXEMPT if later else SPLICE_EXEMPT)
        assert found == [], point_id


# ---------------------------------------------------------------------------
# The product's own facts


def test_the_worked_example_carries_over_at_the_valuation_date(sec_model, s_model):
    """S's worked example and its traces, restated in force, continue S's months.

    At the shipped assumptions, on the three rows derived from the worked example's points:

    * the anchor a month into its income phase, at policy month 241, pays the instalment
      3,688.30, ``B(T) / 12`` on the 44,259.65 the two slices bought, from ``t = 0``, and
      its refund balance at ``t = 0`` is ``CP(T) - G(240) = 150,000 - 3,688.30``,
      146,311.70, the cash refund of a death in the month, read off the instalments
      scheduled to date on the policy clock; the balance runs out in the fourth payment
      year and stays at the float 0.0 from then on, where ``max(0.0, CP(T) - G)`` floors
      it;
    * the acceleration contract in deferral at policy month 59, the month before its second
      premium, carries the 100,000 paid and the 32,024.03 it bought, and buys the second
      slice at ``t = 1``, 50,000 at ``DIA_US_S``'s ``purchase_rate(60)``, its income rising
      to 44,106.53 and its premium income 48,750.00, the premium weighted by survival to
      policy month 60;
    * the start-date adjustment a month after its exercise, at policy month 121, carries the
      repriced income, 82,907.43, the 44,106.53 the slices bought times the factor 1.8797,
      and pays it from policy month 300, its first instalment at ``t = 179``, the end of the
      adjusted income start month.

    Each row is S's point from its month on in every cell but those expense inflation moves
    (:func:`_continues_s`).
    """
    anchor = _row(sec_model, "derived", 1, 241)
    assert anchor.annuity_pp_sched(0) == pytest.approx(3688.30, abs=0.005)
    assert anchor.annual_income_payout() == pytest.approx(44259.65, abs=0.005)
    assert anchor.refund_balance(0) == pytest.approx(150000.0 - 3688.30, abs=0.005)
    assert anchor.claim_pp(0, _code(anchor, "REFUND")) == anchor.refund_balance(0)
    assert anchor.cum_annuity_pp(240) == anchor.annuity_pp_sched_pm(240)
    balances = [anchor.refund_balance(t) for t in range(anchor.proj_len())]
    out = balances.index(0.0)
    assert 24 < out + 1 <= 48 and balances[out - 1] > 0.0
    floored = [(type(b), b) for b in balances[out:]]
    assert floored == [(float, 0.0)] * len(floored)
    deferred = _row(sec_model, "derived", 14, 59)
    s14 = _point(s_model, 14)
    assert (deferred.cum_premium_pp_init(), deferred.premium_pp(1)) == (100000.0, 50000.0)
    assert deferred.annual_income(0) == pytest.approx(32024.03, abs=0.005)
    assert deferred.purchase_rate(60) == s14.purchase_rate(60)
    assert deferred.annual_income(1) == pytest.approx(
        deferred.annual_income(0) + 50000.0 * s14.purchase_rate(60), rel=1e-15)
    assert deferred.annual_income(1) == pytest.approx(44106.53, abs=0.005)
    assert deferred.premiums(1) == pytest.approx(48750.00, abs=0.005)
    adjusted = _row(sec_model, "derived", 13, 121)
    assert adjusted.income_start_mth() == 300
    assert adjusted.annual_income_init() == pytest.approx(82907.43, abs=0.005)
    assert adjusted.annual_income_init() == pytest.approx(
        44106.53 * 1.8797, rel=1e-4)
    paid = [adjusted.annuity_payments(t) for t in range(adjusted.proj_len())]
    assert paid[:179] == [0.0] * 179 and paid[179] > 0.0
    assert paid[179] == pytest.approx(
        adjusted.annual_income_init() / 12 * adjusted.lives_if(180, 1), rel=1e-12)
    for (s_point, month), p in (((1, 241), anchor), ((14, 59), deferred),
                                ((13, 121), adjusted)):
        assert _continues_s(_point(s_model, s_point), p, month) == [], (s_point, month)


def test_pricing_stays_at_issue_and_premium_dates(sec_model, s_model, tmp_path):
    """Each premium still due is priced at its own date on survival from issue, as S
    prices it.

    The pricing survival, ``lives_if_pm(k, life)``, is one explicit loop from issue, S's
    recursion unrolled, so it is ``DIA_US_S``'s ``lives_if(k, life)`` bit for bit at every
    time point from issue to the horizon, on the anchor's twin, the joint twin for both
    lives, and the generational and adjustment twins.  On the contract in deferral at
    policy month 59, the slice still due, at policy month 60, is priced with
    ``guarantee_mths_pricing_init``, ``DIA_US_S``'s fixed point over the whole schedule, the
    slice already bought included, and its purchase rate is ``DIA_US_S``'s bit for bit; on
    a fresh read its projection prices that one premium and no other, the first slice
    being in the opening state.  Set to 0, the column gives the slice another price and
    the contract another income: the schedule of premiums still due cannot recover it.  And
    on the adjustment a month after its exercise, the repriced income is in the opening
    state, and nothing in its projection evaluates the repricing factor again.
    """
    deferred = _row(sec_model, "derived", 14, 59)
    s14 = _point(s_model, 14)
    assert deferred.guarantee_mths_pricing() == deferred.guarantee_mths_pricing_init()
    assert deferred.guarantee_mths_pricing() == pytest.approx(
        s14.guarantee_mths_pricing(), rel=1e-15)
    assert deferred.purchase_rate(60) == s14.purchase_rate(60)
    label = _label(_committed(), "derived", 14, 59)
    adjusted = _label(_committed(), "derived", 13, 121)
    fresh = _read(model_path(SEC), "pricing")
    try:
        for point_id, lives in ((1, (1,)), (8, (1, 2)), (13, (1,)), (16, (1,))):
            p, s = _point(fresh, point_id), _point(s_model, point_id)
            for life in lives:
                mine = [p.lives_if_pm(k, life) for k in range(p.horizon_mths() + 1)]
                assert mine == [s.lives_if(k, life)
                                for k in range(p.horizon_mths() + 1)], (point_id, life)
        p = _point(fresh, label)
        p.result_cf()
        assert sorted(p.cells["purchase_rate"].keys()) == [60]
        q = _point(fresh, adjusted)
        q.result_cf()
        assert len(q.cells["adjust_income_factor"].keys()) == 0
        assert len(q.cells["purchase_rate"].keys()) == 0
    finally:
        fresh.close()
    zeroed = _read_edited(tmp_path, _set("guarantee_mths_pricing_init", [label], 0.0),
                          "zeroed")
    try:
        z = _point(zeroed, label)
        assert z.purchase_rate(60) != s14.purchase_rate(60)
        assert abs(z.annual_income(1) - deferred.annual_income(1)) > 1.0
    finally:
        zeroed.close()


def test_the_payout_schedule_is_fixed_at_the_income_start(sec_model, s_model, events,
                                                          spliced):
    """The income, the refund base and the instalments scheduled to date are S's, read by
    policy month and based at the valuation date's.

    On every twin, ``annual_income_payout()``, ``cum_premium_payout()`` and
    ``cum_annuity_pp(k)`` at every policy month from issue to the stop rule are
    ``DIA_US_S``'s ``annual_income(T)``, ``cum_premium_pp(T)`` and ``cum_annuity_pp(k)``,
    bit for bit.  On every row restated in force they are S's to the last ulp of the opening
    state, which the CSV gives back exactly or within two ulps, and bit for bit where it
    gives it back exactly, as on the cash refund a month into its income phase: the loop
    that sums the instalments before the valuation date's policy month adds them in S's
    order.  The committed rows' instalments are level before their valuation dates, where
    any order of addition gives one float, so the order is asserted on a row whose
    instalments step: the COLA cash refund restated at policy month 265, past its first COLA
    anniversary, its refund still running, on the splice's inputs, whose ``G`` at the
    valuation date's key is the instalments added one by one from the income start month,
    in S's order, to the last bit.  On a model just read, the cash refunds in payout, a
    month in, 432 months in and in the last month, read ``G`` from the valuation date's
    policy month on and never below, keys ``d - 1`` to the last month's (R2's static
    schedule): the refund of a contract long in payout does not recurse back to its income
    start month.  An installment refund's derived period, ``n_R``, is a fixed point of the
    whole payout schedule, which its stop rule needs, so the installment refund valued 30
    months into its income phase reads ``G`` at every payment point from the income start
    month to the end of its derived period, in ascending order, a cell deep each, and at no
    other key.
    """
    table = sec_model.Data.model_point_table()
    exact = set()
    for point_id in table.index[table["row_kind"] != "future"]:
        p, s = _point(sec_model, point_id), _source(s_model, table, point_id)
        start = p.income_start_mth()
        keys = range(p.stop_mth() + 1)
        mine = [p.annual_income_payout(), p.cum_premium_payout(),
                *(p.cum_annuity_pp(k) for k in keys)]
        theirs = [s.annual_income(start), s.cum_premium_pp(start),
                  *(s.cum_annuity_pp(k) for k in keys)]
        if table.at[point_id, "row_kind"] == "twin" or mine[0] == theirs[0]:
            assert mine == theirs, point_id
            exact.add(point_id)
        else:
            assert mine == pytest.approx(theirs, rel=1e-15, abs=0.0), point_id
    assert _label(table, "derived", 1, 241) in exact
    key = _row_key(events, "derived", 10, 265)
    try:
        p = projection(events, key)
        start, base = p.income_start_mth(), p.duration_mth_init() - 1
        steps = [p.annuity_pp_sched_pm(j) for j in range(start, base + 1)]
        assert len(set(steps) - {0.0}) > 1, sorted(set(steps))
        total = 0.0
        for inst in steps:
            total += inst
        assert p.cum_annuity_pp(base) == total
        assert p.cum_annuity_pp(base) == pytest.approx(
            _point(spliced[0], 10).cum_annuity_pp(base), rel=1e-15, abs=0.0)
        assert p.refund_balance(0) > 0.0
    finally:
        _release(events, key, collect=True)
    fresh = _read(model_path(SEC), "g_keys")
    try:
        for s_point, month in ((1, 241), (8, 672), (1, 719)):
            p = _row(fresh, "derived", s_point, month)
            p.result_cf()
            keys = sorted(p.cells["cum_annuity_pp"].keys())
            assert keys == list(range(month - 1, keys[-1] + 1)), (month, keys[:5])
            assert keys[-1] == p.stop_mth() - 2, (month, keys[-3:])
        p = _row(fresh, "derived", 5, 270)
        p.result_cf()
        start = p.income_start_mth()
        assert sorted(p.cells["cum_annuity_pp"].keys()) == list(
            range(start, start + p.certain_mths_refund()))
    finally:
        fresh.close()


def test_survival_opens_per_life_at_the_valuation_date(sec_model, s_model):
    """Each life's survival opens at ``t_entry()`` at its column, and runs on from there.

    On every committed point ``lives_if(t, life)`` is 0 before the contract is on the
    books and ``lives_if_init(life)`` at ``t_entry()``, for each life separately: 1 for
    each covered life at issue, and on a row restated from S at its month ``d``, S's
    ``lives_if(d, life)``, read back from the CSV to 1e-12.  On the joint point at 672 the
    joint annuitant died with certainty at 118, so that life is exactly 0 and the primary a
    fraction, and the payment factor is the survivor percentage times the primary's
    survival from ``t = 0``, read at the end of each month, arrears; on the anchor in its
    last month the life is 6.1e-08.  That each life then runs on from its opening value as
    S's does is asserted with the rest of each derived row's projection, by
    :func:`test_every_committed_row_continues_its_s_point`.
    """
    table = sec_model.Data.model_point_table()
    for key, point_id in zip(point_keys(sec_model), table.index):
        p = projection(sec_model, key)
        entry = p.t_entry()
        for life in (1, 2):
            assert [p.lives_if(t, life) for t in range(entry)] == [0.0] * entry
            covered = life == 1 or p.is_joint()
            assert p.lives_if(entry, life) == (p.lives_if_init(life) if covered else 0.0)
        if table.at[point_id, "row_kind"] != "derived":
            assert (p.lives_if_init(1), p.lives_if_init(2)) == (
                1.0, 1.0 if p.is_joint() else 0.0), point_id
    for point_id in table.index[table["row_kind"] == "derived"]:
        month = int(table.at[point_id, "source_mth"])
        p, s = _point(sec_model, point_id), _source(s_model, table, point_id)
        for life in _lives(p):
            assert p.lives_if_init(life) == pytest.approx(s.lives_if(month, life),
                                                          rel=1e-12, abs=0.0), point_id
    joint = _row(sec_model, "derived", 8, 672)
    assert joint.lives_if_init(2) == 0.0 < joint.lives_if_init(1) < 1e-4
    for t in range(joint.proj_len()):
        assert joint.payment_factor(t) == joint.payment_factor_life(t) == (
            joint.survivor_pct() * joint.lives_if(t + 1, 1)), t
    assert _row(sec_model, "derived", 1, 719).lives_if_init(1) == pytest.approx(
        6.132e-08, rel=1e-3)


def test_contract_open_is_not_life_alive_in_a_guarantee(sec_model, events, spliced,
                                                        tmp_path):
    """In a certain period the guarantee pays the cohort that reached the income phase,
    ``l_last(T)``, which the lives alive cannot say.

    On the period certain in force 300 months, inside its guarantee, the payment factor is
    ``surv_to_payout_init``, 0.715, ``DIA_US_S``'s ``l_last(240)``, while the probability
    that the life is alive, ``lives_if_last(0)``, is 0.5577: the guarantee runs on to a
    beneficiary after the last death, and the contract open exceeds the life alive.  Set to
    the life alive, the column cuts the guaranteed instalments to 0.5577 of each, which
    nothing else on the row could restore: only the column carries the continuation.  And
    on the same contract valued on its income start month, where the column is blank, the
    weight is derived from the projection at ``t = 0``, ``lives_if_last(0)``, bit for bit
    ``DIA_US_S``'s ``surv_to_payout()``, read only where the certain floor is positive.
    """
    p = _row(sec_model, "derived", 7, 300)
    assert p.certain_floor(0) == 1.0
    assert p.surv_to_payout_init() == pytest.approx(0.715, rel=1e-9)
    assert p.payment_factor(0) == p.surv_to_payout_init()
    assert p.lives_if_last(0) == pytest.approx(0.5577, rel=1e-9)
    assert p.payment_factor_life(0) < p.payment_factor(0)
    label = _label(_committed(), "derived", 7, 300)
    alive = _read_edited(tmp_path, _set("surv_to_payout_init", [label],
                                        p.lives_if_last(0)), "alive")
    try:
        q = _point(alive, label)
        for t in (0, 30, 59):
            assert q.annuity_payments(t) < p.annuity_payments(t)
            assert q.annuity_payments(t) == pytest.approx(
                p.annuity_payments(t) * p.lives_if_last(0) / p.surv_to_payout_init(),
                rel=1e-12)
        assert q.annuity_payments(60) == p.annuity_payments(60)
    finally:
        alive.close()
    s7 = _point(spliced[0], 7)
    key = _row_key(events, "derived", 7, 240)
    try:
        r = projection(events, key)
        assert pd.isna(r.model_point()["surv_to_payout_init"])
        assert r.surv_to_payout() == r.lives_if_last(0) == r.payment_factor(0)
        assert r.surv_to_payout() == pytest.approx(s7.surv_to_payout(), rel=1e-15, abs=0.0)
        assert r.payment_factor(0) == pytest.approx(s7.payment_factor(240), rel=1e-15,
                                                    abs=0.0)
    finally:
        _release(events, key, collect=True)


def test_a_commutation_before_the_valuation_date_leaves_its_weight(sec_model, s_model,
                                                                   events, spliced,
                                                                   tmp_path):
    """A contract that commuted before the valuation date pays its beneficiaries'
    guarantee, and its life tail, through the frozen ``l_last(t_c)``.

    The commuting period certain a month after its commutation, at policy month 253,
    carries ``commute_weight_init``, 0.680338, ``DIA_US_S``'s ``l_last(252)``, the cohort
    alive to commute, beside ``surv_to_payout_init``, 0.715, the cohort that reached the
    income phase.  The commuted cohort's guaranteed instalments are gone, so through the
    end of the guarantee, policy month 359, ``t = 106``, it pays the rest of the cohort's,
    the beneficiaries' of contracts whose life died between the income start and the
    commutation: ``inst * (0.715 - 0.680338)``, 79.54 a month, S's months 253 to 359; and
    from policy month 360 the life tail, which a commutation does not reach, 919.16 at
    ``t = 107``.  Set to 0.715, the column extinguishes the beneficiaries' guarantee too:
    read from a copy of the table whose column is 0.715, the row pays nothing until the
    tail, which is unchanged, the fault ``DIA_US_S``'s ``model.md`` prices at 6,898.37 of
    present value.  And on the same contract valued on its
    commutation month, where the column is blank, the weight is derived at ``t = 0``,
    ``lives_if_last(0)``, bit for bit ``DIA_US_S``'s ``commute_weight(252)``.
    """
    p = _row(sec_model, "derived", 15, 253)
    assert p.commute_weight_init() == pytest.approx(0.680338, abs=5e-7)
    assert p.surv_to_payout_init() == pytest.approx(0.715, rel=1e-9)
    assert p.commute_weight(0) == p.commute_weight_init()
    residual = p.annuity_pp_sched(0) * (p.surv_to_payout() - p.commute_weight(0))
    assert residual == pytest.approx(79.54, abs=0.005)
    paid = [p.annuity_payments(t) for t in range(p.proj_len())]
    assert paid[:107] == pytest.approx([residual] * 107, rel=1e-12)
    assert p.certain_floor(106) == 1.0 and p.certain_floor(107) == 0.0
    assert paid[107] == pytest.approx(919.16, abs=0.005)
    assert paid[107] == pytest.approx(
        p.annuity_pp_sched(107) * p.lives_if(108, 1), rel=1e-12)
    s15 = _point(s_model, 15)
    assert sum(paid[:107]) == pytest.approx(sum(s15.annuity_payments(253 + t)
                                                for t in range(107)), rel=1e-12)
    label = _label(_committed(), "derived", 15, 253)
    whole = _read_edited(tmp_path, _set("commute_weight_init", [label],
                                        p.surv_to_payout_init()), "whole")
    try:
        q = _point(whole, label)
        assert q.commute_weight(0) == q.surv_to_payout() == p.surv_to_payout_init()
        later = [q.annuity_payments(t) for t in range(q.proj_len())]
        assert later[:107] == [0.0] * 107
        assert later[107:] == paid[107:]
    finally:
        whole.close()
    key = _row_key(events, "derived", 15, 252)
    try:
        r = projection(events, key)
        assert pd.isna(r.model_point()["commute_weight_init"])
        assert r.commute_weight(0) == r.lives_if_last(0)
        assert r.commute_weight(0) == pytest.approx(
            _point(spliced[0], 15).commute_weight(252), rel=1e-15, abs=0.0)
    finally:
        _release(events, key, collect=True)


# The rows of the commutation residual's test, on the splice's inputs: each commuting point
# valued before, at and after its commutation, as (S point, source_mth).
COMMUTED = ((15, 251), (15, 252), (15, 253), (15, 360), (21, 252), (26, 250), (26, 252),
            (32, 365), (32, 390), (35, 252))


def test_the_commutation_residual_closes_at_the_guarantees_last_month(events, spliced):
    """The exchange residual is measured where the guarantee ends, reading back to the
    commutation, and is ``DIA_US_S``'s residual at the exercise, bit for bit.

    ``DIA_US_S`` computes ``check_commutation_value_resid`` at the commutation month, over
    every guaranteed month still to come, a read R2 does not admit.  This model sums the
    same months, month by month, in the same order and discounted from the exercise at the
    rate of the exercise month, at the guarantee's last month, policy month
    ``T + n_eff - 1``, reading back.  So on every row valued at or before its commutation,
    on the splice's inputs, its residual there is S's at the exercise, to the last bit:
    rounding, 8.7e-11 on point 15, 2.9e-11 on its quarterly variant, and exactly 0 on the
    commuting installment refund.  It is 0.0 in every other month, and on every row valued
    after the commutation, where the exchange closed before the valuation date or the
    commutation fell after the guarantee.  Its precedents at that month include the
    commutation itself, ``commutations(t_c)``.  A residual moved to the wrong month, or
    measured on ``t`` where ``duration_mth(t)`` belongs, is 0 there and passes every
    comparison at the floor; only this equality sees it.
    """
    s = spliced[0]
    for s_point, month in COMMUTED:
        key = _row_key(events, "derived", s_point, month)
        try:
            p = projection(events, key)
            sp = _point(s, s_point)
            c, d = p.commute_mth(), p.duration_mth_init()
            end = p.income_start_mth() + p.certain_mths_eff()
            residuals = [p.check_commutation_value_resid(t) for t in range(p.proj_len())]
            if d <= c < end:
                at = end - 1 - d
                assert residuals[at] == sp.check_commutation_value_resid(c), (
                    s_point, month, residuals[at], sp.check_commutation_value_resid(c))
                others = residuals[:at] + residuals[at + 1:]
                preds = {(node.obj.name, node.args) for node in
                         p.cells["check_commutation_value_resid"].preds(at)}
                assert ("commutations", (c - d,)) in preds, (s_point, month)
                assert p.check_commutation_value() is True
            else:
                others = residuals
            assert others == [0.0] * len(others), (s_point, month)
        finally:
            _release(events, key, collect=True)


def test_an_acceleration_needs_no_column(events, spliced):
    """An acceleration is read only in its exercise month, so nothing of it is opening
    state.

    On the splice's inputs, the acceleration contract valued in its exercise month, policy
    month 252, pays at ``t = 0`` S's lump sum, the instalment and the five it pulls forward,
    each weighted by the survival at the lump sum's own date, and nothing in the five
    blackout months after it.  Valued a month later, at 253, inside the blackout, the lump
    sum was paid before the valuation date: the blackout pays nothing through policy month
    257, ``accel_payment_factor`` is 0.0 at every month from the valuation date on, since
    nothing reads it, and the instalments resume at 258 as S's.  Valued the month before
    the exercise, at 251, the factor in the blackout is S's, read back at the exercise
    month on the valuation clock.
    """
    s14 = _point(spliced[0], 14)
    for month in (251, 252, 253):
        key = _row_key(events, "derived", 14, month)
        try:
            p = projection(events, key)
            a = p.accel_mth() - month
            paid = [p.annuity_payments(t) for t in range(p.proj_len())]
            assert paid == pytest.approx([s14.annuity_payments(month + t)
                                          for t in range(p.proj_len())], rel=1e-12)
            blackout = [t for t in range(p.proj_len()) if p.accel_blackout(t)]
            assert blackout == [t for t in range(a + 1, a + 6) if t >= 0], month
            assert all(paid[t] == 0.0 for t in blackout), month
            factors = [p.accel_payment_factor(t) for t in blackout]
            if a >= 0:
                assert paid[a] == pytest.approx(s14.annuity_payments(252), rel=1e-12)
                assert paid[a] > 5.0 * p.annuity_pp_sched(a) * p.payment_factor(a)
                assert factors == pytest.approx([s14.accel_payment_factor(month + t)
                                                 for t in blackout], rel=1e-12)
            else:
                assert factors == [0.0] * len(blackout)
                assert all(p.accel_payment_factor(t) == 0.0 for t in range(p.proj_len()))
                assert paid[a + 6] > 0.0
        finally:
            _release(events, key, collect=True)
    _release(spliced[0], _key(spliced[0], 14), collect=True)


def test_each_contract_reads_the_reference_rate_change_since_its_own_issue(s_model,
                                                                         tmp_path):
    """Each contract reads the reference rate's change since its own issue, on one path,
    floored as a whole.

    The commutation discount rate moves one for one with the reference rate's change since
    issue, floored at 0, and every contract of a block reads that change on one path of the
    reference rate, which every point shares (D7, as precised at M11).  Contracts issued at
    different dates have seen different changes by the valuation date, which
    ``ref_rate_shift_init`` carries, and the Reference ``ref_rate_shift`` is the change made
    at the valuation date, which every contract on the books there sees and a contract
    issued later, bought after it, does not.  One table holds three contracts on S point
    15's terms, all of them commuting at policy month 252: the point in force at its income
    start month, 240, its column set to 0.005; its twin, issued at the valuation date; and
    the same contract issued 13 months on.  Read with the Reference at 0, the point in force
    discounts at 5.75%, ``i_p + 0.005 + m_c``, its commuted value S's with S's change at
    0.005, and the other two at 5.25%, S's on its shipped rate.  Read with the Reference at
    0.005, the rate 50 basis points up again at the valuation date, the point in force
    discounts at 6.25%, S's at 0.010, the twin at 5.75%, S's at 0.005, and the contract
    issued later at 5.25% still, its commuted value unmoved.  A Reference read as the change
    since each contract's own issue would move the last too, and one ignored would leave the
    twin at 5.25%.

    The floor is on the whole change since issue, column and Reference added first (§7.9,
    *Record — M11*): a column of -0.01 at the Reference 0.005, a fall before the valuation
    date that a rise at it only part offsets, discounts at ``i_p + m_c``, 5.25%, where a
    floor on each part would give 5.75%; and a column of 0.01 at -0.005 at ``i_p + 0.005 +
    m_c``, 5.75%, where a floor on each part would give 6.25%.  The contract issued later
    reads 5.25% at every value.  Each value is set on a model read for it, before the model
    computes anything.
    """
    spec = dataclasses.replace(SPEC, derived=((15, 240),), future=((15, 13),))
    table, companions = build_sec_table(spec, s_model)
    in_force = _label(table.set_index("point_id"), "derived", 15, 240)
    later = _label(table.set_index("point_id"), "future", 15, -13)
    twin = 15

    def with_change(change):
        edited = table.set_index("point_id")
        return _set("ref_rate_shift_init", [in_force], change)(edited)

    def rates(change, shift, tag):
        folder = _sec_inputs(tmp_path / tag, with_change(change),
                             schedule=companions[SCHEDULE])
        model = _read(folder, tag, {"ref_rate_shift": shift})
        try:
            p, t15, f = (_point(model, i) for i in (in_force, twin, later))
            assert (p.ref_rate_shift_init(), t15.ref_rate_shift_init(),
                    f.ref_rate_shift_init(), f.t_entry()) == (change, 0.0, 0.0, 13)
            return ((p.commute_disc_rate(12), t15.commute_disc_rate(252),
                     f.commute_disc_rate(265)),
                    (p.commuted_value(12), t15.commuted_value(252), f.commuted_value(265)))
        finally:
            model.close()

    up = _read(model_path(TWIN), "s_rate_up", {"ref_rate_shift": 0.005})
    up_twice = _read(model_path(TWIN), "s_rate_up_twice", {"ref_rate_shift": 0.01})
    try:
        s15, s15_up, s15_up_twice = (_point(m, 15) for m in (s_model, up, up_twice))
        flat_rates, flat_values = rates(0.005, 0.0, "flat")
        step_rates, step_values = rates(0.005, 0.005, "step")
        assert flat_rates == pytest.approx((0.0575, 0.0525, 0.0525), rel=1e-12)
        assert step_rates == pytest.approx((0.0625, 0.0575, 0.0525), rel=1e-12)
        assert flat_values == pytest.approx((s15_up.commuted_value(252),
                                             s15.commuted_value(252),
                                             s15.commuted_value(252)), rel=1e-12)
        assert step_values == pytest.approx((s15_up_twice.commuted_value(252),
                                             s15_up.commuted_value(252),
                                             s15.commuted_value(252)), rel=1e-12)
        assert step_values[2] == flat_values[2]
    finally:
        up_twice.close()
        up.close()
    fall_rates, _ = rates(-0.01, 0.005, "fall")
    rise_rates, _ = rates(0.01, -0.005, "rise")
    assert fall_rates == pytest.approx((0.0525, 0.0575, 0.0525), rel=1e-12)
    assert rise_rates == pytest.approx((0.0575, 0.0525, 0.0525), rel=1e-12)


def test_mortality_improvement_is_calendar_dated_on_the_policy_clock(sec_model, s_model,
                                                                    events, spliced):
    """Improvement reads each contract's own calendar years, whatever the valuation date.

    The exponent is the calendar year of the policy year less ``mort_table_year``, and the
    calendar year is ``issue_year() + duration(t)``, on the policy clock (D7): a contract in
    force at the valuation date reads the improvement of the calendar years it reaches,
    from its own issue year, so nothing is re-based onto the valuation clock and the splice
    need not neutralize it.  On the generational point in force at its income start month,
    on the splice's set-apart scale, ``calendar_year(0)`` is 2046, and its rates at every
    ``t`` are S point 16's at month ``240 + t``, the improvement rates by age S's too, with
    no input re-based.  On the joint point issued 13 months on, at the shipped assumptions,
    ``calendar_year(13)``, its issue month, is 2026, and its rates are S point 8's ``13``
    months earlier, for both lives.
    """
    s16 = _point(spliced[0], 16)
    key = _row_key(events, "derived", 16, 240)
    try:
        p = projection(events, key)
        assert p.is_generational() and (p.issue_year(), p.calendar_year(0)) == (2026, 2046)
        for t in range(p.proj_len()):
            assert p.mort_rate(t, 1) == s16.mort_rate(240 + t, 1), t
            assert p.improvement_rate(t, 1) == s16.improvement_rate(240 + t, 1), t
    finally:
        _release(events, key, collect=True)
    later, s8 = _row(sec_model, "future", 8, -13), _point(s_model, 8)
    assert (later.duration_mth(13), later.calendar_year(13)) == (0, 2026)
    for t in range(s8.proj_len()):
        for life in (1, 2):
            assert later.mort_rate(13 + t, life) == s8.mort_rate(t, life), (t, life)


# The cap on mortality
#
# DIA_US_S caps the annual rate, the bound second, min(mort_ae_factor * q, 1.0), so that
# its monthly rate stays real at any A/E and a lost rate stays NaN, and this model caps it
# as S does, in mort_rate_py (USLIB-SEC-PLAN.md §5.1, step 6).  On the shipped tables the
# male rate is 1.0 at 118 and 119, so the cap changes no value there; under the splice's
# A/E of 1.05 it binds with an effect at male 117, and at omega inside a guarantee that
# outlasts the age stop.  The S points on which it binds inside the frame, each with the
# life it binds on, the first S month it binds in and the month before it, at which a row is
# restated in force, on the splice's inputs; each point's twin is new business there.
CAPPED = {
    8: (2, 648, 647),     # the joint annuitant, male, at 117
    18: (1, 684, 683),    # the male life on the table basis, at 117
    30: (1, 480, 479),    # omega inside a 30-year guarantee
}


def _uncapped_mort_rate(s, m, life):
    """``DIA_US_S``'s annual mortality of ``life`` in month ``m`` before its cap, from S's
    own cells: the A/E times the base rate, improved on the generational basis."""
    q = s.mort_rate_base(m, life)
    if s.mort_basis() == "generational":
        q = q * (1.0 - s.improvement_rate(m, life)) ** (s.calendar_year(m)
                                                        - s.mort_table_year)
    return s.mort_ae_factor * q


def test_a_capped_annual_mortality_is_the_float_1_in_both_models(sec_model, events,
                                                                  spliced):
    """Where the annual mortality product passes 1, both models' rate is the float 1.0, and
    the life's survival is exactly 0 after it.

    On each S point of :data:`CAPPED`, on the splice's inputs, ``DIA_US_S``'s product of
    the A/E, the base rate and, on the generational basis, the improvement, computed from
    S's own cells (:func:`_uncapped_mort_rate`), passes 1 in every month from the point's
    first capped month to the end of its frame.  Both models cap it there: ``mort_rate`` and
    ``mort_rate_mth`` are ``(float, 1.0)`` in each of those months, the type asserted with
    the value, since ``1 == 1.0`` would let an int cap through, and below 1 in every month
    before.  The life alive at the start of the first capped month dies in it, so that its
    survival is exactly 0 at every time point after, in both models.  Two rows of each
    point are read, its twin and the point restated in force the month before the cap,
    opened with S's state there: on each, every report is float64 and finite, and every
    cell of S's agrees with S at every argument S cached, the capped months included, to
    1e-9 relative with no absolute floor (:func:`_compared`), since survival where the cap
    binds is near 1e-8.  A cap applied to new business alone fails on the rows in force.
    On the shipped tables the joint annuitant of the committed joint twin reaches 118,
    where the table's rate is 1, and its rate is ``(float, 1.0)`` too.

    And the cap's order: on a model read with ``mort_ae_factor`` set to NaN before it
    computes anything, the anchor's twin's ``mort_rate(0, 1)`` is NaN, not 1.0.  The cap
    with its bound second keeps a lost value a NaN, where ``min(1.0, nan)`` is 1.0 and would
    pass it as certain death in month 0 with every flow finite; so would a cap on the
    monthly rate.  No reader is patched, so the case runs compiled at Phase 2 too.
    """
    s = spliced[0]
    found = []
    for s_point, (life, first, month) in CAPPED.items():
        sp = _point(s, s_point)
        try:
            _sweep(sp)
            end = sp.proj_len()
            assert [m for m in range(end) if sp.mort_rate(m, life) == 1.0] == list(
                range(first, end)), s_point
            assert all(_uncapped_mort_rate(sp, m, life) > 1.0 for m in range(first, end))
            assert all(sp.mort_rate(m, life) < 1.0 for m in range(first))
            found += [("S", s_point, m, rate.name) for m in range(first, end)
                      for rate in (sp.cells["mort_rate"], sp.cells["mort_rate_mth"])
                      if (type(rate(m, life)), rate(m, life)) != (float, 1.0)]
            assert sp.lives_if(first, life) > 0.0, s_point
            assert [sp.lives_if(m, life) for m in range(first + 1, end + 1)] == (
                [0.0] * (end - first)), s_point
            for case in (("derived", s_point, month), ("twin", s_point, 0)):
                key = _row_key(events, *case)
                try:
                    p = projection(events, key)
                    n, at = p.proj_len(), first - case[2]
                    capped = [t for t in range(n) if p.mort_rate(t, life) == 1.0]
                    assert capped == list(range(at, n)), (case, capped[:3])
                    found += [(case, t, rate.name) for t in capped
                              for rate in (p.cells["mort_rate"], p.cells["mort_rate_mth"])
                              if (type(rate(t, life)), rate(t, life)) != (float, 1.0)]
                    assert p.lives_if(at, life) > 0.0, case
                    assert [p.lives_if(t, life) for t in range(at + 1, n + 1)] == (
                        [0.0] * (n - at)), case
                    for frame in (p.result_cf(), p.result_pols()):
                        assert (frame.dtypes == "float64").all(), (case, frame.dtypes)
                        assert (frame.abs() < float("inf")).all().all(), case
                    exempt = SPLICE_EXEMPT if case[0] == "derived" else FUTURE_EXEMPT
                    assert _compared(sp, p, case[2], exempt) == [], case
                finally:
                    _release(events, key)
        finally:
            _release(s, _key(s, s_point), collect=True)
    assert not found, f"a capped rate that is not the float 1.0: {found[:5]}"
    joint = _point(sec_model, 8)
    rate = joint.mort_rate(12 * (118 - 63), 2)
    assert (type(rate), rate) == (float, 1.0)
    lost = _read(model_path(SEC), "lost", {"mort_ae_factor": NAN})
    try:
        q = _point(lost, 1).mort_rate(0, 1)
        assert q != q, f"mort_rate(0, 1) is {q!r} with a lost A/E"
    finally:
        lost.close()


# The model's four checks, each a bool over its residual's months (RESIDUALS).
CHECKS = ("check_lives_roll_fwd", "check_income_roll_fwd", "check_payment_factor",
          "check_commutation_value")


def test_a_residual_that_is_not_a_number_fails_its_check():
    """A check whose residual is not a number fails, as ``DIA_US_S``'s does.

    Each check asks whether every month's residual is within its tolerance, or is 0.0,
    never whether one is beyond it, so a NaN fails it, where ``abs(r) > tol`` would pass
    it.  On a model read with ``mort_ae_factor`` set to NaN before it computes anything,
    each life's monthly mortality is NaN, and so is its survival from ``t = 1``.  On every
    committed twin the survival roll-forward's residual is 0.0 at ``t = 0`` and NaN in
    every month after, and ``check_lives_roll_fwd()`` is ``False``.  On the twin of S point
    15, a 10-year period certain commuted in full at policy month 252, each of the four
    residuals is NaN in some month and 0.0 in every other, and each check is ``False``: what
    each check fails is the NaN.

    The other three are not asserted on every twin, because they read survival through
    ``DIA_US_S``'s own comparisons and ``max``, which can lose a NaN: ``nan > 0.0`` is
    ``False``, and ``max(0.0, nan)`` is 0.0.  On the anchor's twin, with no certain floor,
    the payment factor in its income phase is ``max(0.0, nan)``, and its residual 0.0; on
    the installment refund's twin the guarantee search finds no income, so no instalment is
    certain, each is valued at 0.0 and every premium buys 0.0, which the income
    roll-forward closes.  No formula is replaced, so the case runs compiled at Phase 2 too.
    """
    assert {f"{check}_resid" for check in CHECKS} == RESIDUALS
    model = _read(model_path(SEC), "nan", {"mort_ae_factor": NAN})
    try:
        table = model.Data.model_point_table()
        twins = table.index[table["row_kind"] == "twin"].tolist()
        assert len(twins) == 17
        for point_id in twins:
            p = _point(model, point_id)
            lives = [p.check_lives_roll_fwd_resid(t) for t in range(p.proj_len())]
            assert lives[0] == 0.0 and all(r != r for r in lives[1:]), point_id
            assert p.check_lives_roll_fwd() is False, point_id
            for check in CHECKS if point_id == 15 else ():
                resid = [p.cells[f"{check}_resid"](t) for t in range(p.proj_len())]
                assert any(r != r for r in resid), check
                assert all(r != r or r == 0.0 for r in resid), check
                assert p.cells[check]() is False, check
            _release(model, _key(model, point_id))
    finally:
        model.close()


def test_expense_inflation_runs_on_the_valuation_clock(sec_model, s_model):
    """Maintenance is in valuation-date dollars, for every point alike (D7).

    At the shipped 2.5%, the factor at ``t`` is ``1.025 ** (t // 12)`` on every point,
    whatever its duration: S's annual steps, moved onto the valuation clock.  So the period
    certain in force 300 months, valued on its anniversary, pays S's month ``300 + t``
    expenses deflated by ``1.025 ** 25``, the inflation S had already applied since issue;
    the anchor a month into its income phase, valued a month off its anniversary, pays S's
    month ``241 + t`` expenses divided by ``1.025 ** 20`` or ``1.025 ** 21``, as its policy
    years and the valuation years step apart; and the joint point issued 13 months on pays
    S's month ``t - 13`` maintenance times 1.025 or 1.025 squared, valuation years against
    policy years.  This is the only test that sees inflation run on the valuation clock:
    the splice sets the rate to 0, and on a point issued at ``t = 0`` the clocks agree.
    """
    assert sec_model.Projection.inflation_rate == INFLATION
    for key in point_keys(sec_model):
        p = projection(sec_model, key)
        for t in range(p.proj_len()):
            assert p.inflation_factor(t) == (1.0 + INFLATION) ** (t // 12), (key, t)
    p, s = _row(sec_model, "derived", 7, 300), _point(s_model, 7)
    for t in range(p.proj_len()):
        assert p.expenses(t) == pytest.approx(
            s.expenses(300 + t) / (1.0 + INFLATION) ** 25, rel=1e-12), t
    for (kind, s_point, month), steps in ((("derived", 1, 241), {20, 21}),
                                          (("future", 8, -13), {-1, -2})):
        p, s = _row(sec_model, kind, s_point, month), _point(s_model, s_point)
        ratios = set()
        for t in range(max(0, -month), p.proj_len()):
            if p.expenses(t):
                ratio = s.expenses(month + t) / p.expenses(t)
                ratios |= {n for n in steps
                           if ratio == pytest.approx((1.0 + INFLATION) ** n, rel=1e-12)}
                assert any(ratio == pytest.approx((1.0 + INFLATION) ** n, rel=1e-12)
                           for n in steps), (s_point, t, ratio)
        assert ratios == steps, (s_point, ratios)


def test_new_business_brings_its_premiums_and_no_acquisition(sec_model):
    """A contract issued later brings its premium schedule into the frame, and no cost.

    ``DIA_US_S`` charges no acquisition cost, and neither does this model: on every point
    and in every month ``expenses(t)`` is the maintenance charge alone,
    ``expense_maint / 12 * inflation_factor(t) * pols_if(t)``, the issue month included,
    where ``Term_US_SEC`` charges acquisition per policy issued, and the gross outgo is the
    income, the claims, the commutations and that charge.  The joint point issued 13 months
    on brings its premiums as new business, weighted by its count and its survival from
    issue: the first, 100,000, at ``t = 13``, its issue month, and the second at policy
    month 60, ``t = 73``, ``50,000 * l_last(60)``; before issue there is none.
    """
    for key in point_keys(sec_model):
        p = projection(sec_model, key)
        for t in range(p.proj_len()):
            assert p.expenses(t) == (
                p.expense_maint / 12.0 * p.inflation_factor(t) * p.pols_if(t)), (key, t)
            assert p.liability_outgo(t) == (p.annuity_payments(t) + p.claims(t)
                                            + p.commutations(t) + p.expenses(t)), (key, t)
    later = _row(sec_model, "future", 8, -13)
    premiums = [later.premiums(t) for t in range(later.proj_len())]
    assert [t for t, x in enumerate(premiums) if x] == [13, 73]
    assert premiums[13] == 100000.0 == later.policy_count() * later.premium_pm(0)
    assert premiums[73] == 50000.0 * later.lives_if_last(73)
    assert later.pols_new_biz(13) == 1.0


def test_there_is_no_lapse_decrement_and_no_account_value(sec_model):
    """``pols_new_biz`` exists, meaning contracts issued; a lapse still does not.

    ``DIA_US_S``'s tests forbid every name that would make a DIA a deferred annuity with a
    balance: "A nonzero lapse assumption in a DIA model is a defect, not a margin", and the
    liability is a schedule of income slices, not a balance.  Running in force adds the
    count's names, ``pols_new_biz`` and ``pols_if_at`` among them, none of which is a lapse
    (``pols_if_at`` holds ``if_at``, not ``av_at``), and the same ban holds over every cell
    and Reference of both Spaces.  ``result_cf()`` keeps ``DIA_US_S``'s columns.
    """
    names = set(sec_model.Projection.cells) | set(sec_model.Projection.refs)
    names |= set(sec_model.Data.cells)
    assert {"pols_new_biz", "pols_if_at"} <= names
    forbidden = ("lapse", "surr_charge", "surrender", "av_pp", "av_at", "account_value",
                 "crediting", "credit_rate", "interim_value", "benefit_base",
                 "annuitization_rate", "free_withdrawal", "market_value_adj")
    bad = sorted((n, word) for n in names for word in forbidden if word in n)
    assert not bad, bad
    assert set(_point(sec_model, 1).result_cf().columns) == {
        "pols_if", "premiums", "annuity_payments", "claims", "commutations", "expenses",
        "liability_cf", "net_cf"}


def test_the_stop_rule_ends_every_frame(sec_model, s_model):
    """Every frame ends at the stop rule, S's frame from issue (D3).

    ``stop_mth()`` is S's frame length from issue, the age stop on the youngest covered
    life or the end of the guarantee if later, so it is S's ``proj_len()`` on every twin,
    and the frame runs from the valuation date to it: 661, 479, 420, 467, 599, 48, 450, 1
    and 733 months on the rows restated at policy months 59, 241, 300, 253, 121, 672, 270
    and 719 and the row issued 13 months on.  Its last month is policy month
    ``stop_mth() - 1`` on every point, inside cover, and the next is outside.  A contract's
    own end is no end of the frame: the anchor in its last month still carries a life,
    6.13e-08, and pays its instalment weighted by it.
    """
    table = sec_model.Data.model_point_table()
    for key, point_id in zip(point_keys(sec_model), table.index):
        p = projection(sec_model, key)
        n = p.proj_len()
        assert n == p.stop_mth() - p.duration_mth_init(), point_id
        assert p.duration_mth(n - 1) == p.stop_mth() - 1, point_id
        assert p.is_active(n - 1) and not p.is_active(n), point_id
        if table.at[point_id, "row_kind"] == "twin":
            assert p.stop_mth() == _point(s_model, point_id).proj_len(), point_id
    rows = table.index[table["row_kind"] != "twin"]
    assert [_point(sec_model, i).proj_len() for i in rows] == [
        661, 479, 420, 467, 599, 48, 450, 1, 733]
    last = _row(sec_model, "derived", 1, 719)
    assert last.annuity_payments(0) == pytest.approx(
        _point(s_model, 1).annuity_payments(719), rel=1e-12)
    assert last.annuity_payments(0) > 0.0


def _outside_cover_faults(p, where):
    """Where ``p``, an ItemSpace that has evaluated nothing, departs from OUTSIDE_COVER.

    Every cell of :data:`OUTSIDE_COVER`, each of :data:`PER_LIFE` for every covered life,
    ``pols_if_at`` at each timing and ``claim_pp`` and ``claims`` at each kind, in every
    month before issue and at ``t = proj_len()``, the month after the stop rule, which the
    closing time points read; and before issue :data:`BEFORE_ISSUE`'s time points and
    ``lives_if`` for both lives, all 0.0.  And ``phase``, ``PRE_ISSUE`` before issue and
    ``TERMINATED`` at ``t = proj_len()``, through :func:`_code`.  Then whether any of
    :data:`IN_COVER_ONLY` was evaluated on the way, which only a fresh ItemSpace can say.
    A cell that raises is reported as a fault too, so the scan goes on.
    """
    faults = []
    for t in [*range(p.t_entry()), p.proj_len()]:
        calls = [(name, (t,), want) for name, want in OUTSIDE_COVER.items()]
        calls += [(name, (t, life), 0.0) for name in PER_LIFE for life in _lives(p)]
        calls += [("pols_if_at", (t, _code(p, timing)), 0.0) for timing in TIMINGS]
        calls += [(name, (t, _code(p, kind)), 0.0) for name in ("claim_pp", "claims")
                  for kind in KINDS]
        if t < p.t_entry():
            calls += [(name, (t,), want) for name, want in BEFORE_ISSUE.items()]
            calls += [("lives_if", (t, life), 0.0) for life in (1, 2)]
        phase = "PRE_ISSUE" if t < p.t_entry() else "TERMINATED"
        calls.append(("phase", (t,), _code(p, phase)))
        for name, args, want in calls:
            try:
                got = p.cells[name](*args)
            except Exception as err:        # reported, so the scan goes on
                faults.append(f"{where}: {name}{args} raised {_raised(err)}")
                continue
            if got != want or type(got) is not type(want):
                faults.append(f"{where}: {name}{args} = {got!r}, not {want!r}")
    read = {name: sorted(p.cells[name].keys()) for name in IN_COVER_ONLY
            if len(p.cells[name].keys())}
    if read:
        faults.append(f"{where}: evaluated outside cover: {read}")
    return faults


def _monthly_calls(p, t):
    """Every call of a monthly cell of ``p`` at ``t``: each life, kind and timing.

    A monthly cell is one whose first parameter is ``t``: each covered life for a
    ``(t, life)`` cell, and both lives for ``lives_if`` and ``lives_death``, which answer
    for a life the contract does not cover; each of :data:`KINDS` for a kind; each of
    :data:`TIMINGS` for a timing.
    """
    calls = []
    for name, cells in p.cells.items():
        params = cells.parameters
        if not params or params[0] != "t":
            continue
        if params == ("t",):
            calls.append((name, (t,)))
        elif params == ("t", "life"):
            lives = (1, 2) if name in ("lives_if", "lives_death") else _lives(p)
            calls += [(name, (t, life)) for life in lives]
        elif params == ("t", "kind"):
            calls += [(name, (t, _code(p, kind))) for kind in KINDS]
        elif params == ("t", "timing"):
            calls += [(name, (t, _code(p, timing))) for timing in TIMINGS]
        else:
            raise AssertionError(f"{name}{params}: a monthly cell the guard test does not "
                                 f"know how to call")
    return calls


def _guard_faults(p, where):
    """:func:`_outside_cover_faults`, then every monthly cell outside cover, and the keys.

    After the first scan, every monthly cell (:func:`_monthly_calls`) is called at the same
    months, as Phase 2's full sweep calls every cell of ``t`` from 0 to ``proj_len()``: none
    may raise, and afterwards every policy-clock and age-keyed cell's keys must lie inside
    the contract (:func:`_contract`).  Two kinds of key are reached on purpose: the closing
    time points at ``t = proj_len()``, which evaluate every covered month's rates, and
    ``is_active``, which on an installment refund searches its payout schedule, and so
    prices its premiums, for the refund period; neither may leave the contract.
    """
    faults = _outside_cover_faults(p, where)
    for t in [*range(p.t_entry()), p.proj_len()]:
        for name, args in _monthly_calls(p, t):
            try:
                p.cells[name](*args)
            except Exception as err:        # reported, so the scan goes on
                faults.append(f"{where}: {name}{args} raised {_raised(err)}")
    return faults + [f"{where}: {line}" for line in _outside_contract(p)]


def test_every_guarded_cell_holds_its_outside_cover_value(spliced):
    """Outside cover each cell holds :data:`OUTSIDE_COVER`'s value, and reads no rate.

    On every committed point, in every month before issue and in the month after the stop
    rule, ``t = proj_len()``, which the closing time points read, on a model that evaluates
    nothing else.  So afterwards none of :data:`IN_COVER_ONLY` may hold a value at all:
    ``is_active``'s docstring promises that outside cover no cell reads a rate, a policy
    year or an attained age the contract does not have.  Then every monthly cell is called
    at those months, as Phase 2's full sweep calls it, and the policy-clock and age keys it
    reaches must stay inside the contract (:func:`_guard_faults`).

    The committed table's one point issued after the valuation date is the joint cash
    refund, with no certain period, no option and no adjustment, so on it a cell tied to
    one of those would hold zero before issue, guarded or not.  So the same scan runs on the
    splice's future rows, the core's or, with ``USLIB_SEC_FULL=1``, all of them: the
    installment refund, the start-date adjustment, the acceleration, the commutation and a
    guarantee past the age stop among them, 13 months on, so that a read before issue lands
    at policy year -1.  Each row is made afresh first and released after.

    Several of these guards change no number the frame shows: once the counts are zero
    outside cover, every cash flow is too, and an unguarded value multiplies a zero count.
    They are held here because they are what the docstrings promise a caller, and because
    Phase 2 needs them: a table read at a policy year or an age the contract does not have
    would wrap round in a compiled model rather than fail (USLIB-SEC-PLAN.md F4, R1).
    """
    faults = []
    model = _read(model_path(SEC), "cover")
    try:
        table = model.Data.model_point_table()
        for key, point_id in zip(point_keys(model), table.index):
            faults += _guard_faults(projection(model, key), f"point {point_id}")
    finally:
        model.close()
    sec = spliced[1]
    futures = _selected(FUTURES, CORE_FUTURES)
    for s_point, k in futures:
        key = _row_key(sec, "future", s_point, -k)
        if key in sec.Projection.itemspaces:
            _release(sec, key, collect=True)
        try:
            faults += _guard_faults(projection(sec, key), _case_id("future", s_point, -k))
        finally:
            _release(sec, key, collect=True)
    assert futures and not faults, (
        f"{len(faults)} faults outside cover, first:\n  " + "\n  ".join(faults[:20]))


def test_the_points_sum_row_by_row_into_a_block(events, spliced):
    """Row ``t`` is the same month on every point, so a block is its frames summed (D3).

    The anchor issued at the valuation date, in force 12 months and issued 13 months on,
    summed as ``run_sec.py --block`` sums them, are indexed 0..732 and equal S's frame added
    to itself moved 12 months earlier and 13 months later.  A model whose frames sat on the
    policy clock would fail it.  The three are read from one read of a table, on the
    splice's inputs (:data:`SEC_REFS`), as a block is read; the anchor holds no commutation,
    so the reference rate's change, which the splice's S reads 50 basis points up, moves no
    number of its frame.
    """
    keys = [_row_key(events, *case)
            for case in (("twin", 1, 0), ("derived", 1, 12), ("future", 1, -13))]
    try:
        frames = [projection(events, key).result_cf() for key in keys]
    finally:
        for key in keys:
            _release(events, key, collect=True)
    block = pd.concat(frames).groupby(level="t").sum()
    try:
        sdf = _point(spliced[0], 1).result_cf()
    finally:
        _release(spliced[0], _key(spliced[0], 1), collect=True)
    expected = pd.concat([sdf, sdf.set_axis(sdf.index - 12).loc[0:],
                          sdf.set_axis(sdf.index + 13)]).groupby(level=0).sum()
    assert list(block.index) == list(range(733))
    assert frame_mismatches(expected, block) == []


def test_result_annual_keeps_the_policy_year_key(sec_model, s_model):
    """The annual display is indexed by the policy year, from the valuation date's.

    ``result_annual`` keeps ``DIA_US_S``'s key, so a point in force shows the policy years
    from the one the valuation date falls in, and the years before it are left out, as
    ``Term_US_SEC``'s annual report leaves them out.  On the period certain in force 300
    months, valued on its anniversary, every row is S's year, policy years 26 to 60, in
    every column.  On the anchor a month into its income phase, valued a month after its
    anniversary, the first row, policy year 21, holds the months of that year on the books,
    policy months 241 to 251: its claims are those eleven months' and its CP, B and survival
    the year's closing values, S's; every later row is S's year.  The joint point issued 13
    months on starts at policy year 1, as S does.
    """
    on = _row(sec_model, "derived", 7, 300)
    mine, theirs = on.result_annual(), _point(s_model, 7).result_annual()
    assert list(mine.index) == list(range(26, 61))
    assert frame_mismatches(theirs.loc[26:], mine, atol=0.0) == []
    off = _row(sec_model, "derived", 1, 241)
    s1 = _point(s_model, 1)
    mine, theirs = off.result_annual(), s1.result_annual()
    assert list(mine.index) == list(range(21, 61))
    assert frame_mismatches(theirs.loc[22:], mine.loc[22:], atol=0.0) == []
    first, whole = mine.loc[21], theirs.loc[21]
    for c in ("age", "cum_premium_pp", "annual_income", "lives_if", "annuity_payments"):
        assert first[c] == pytest.approx(whole[c], rel=1e-12), c
    assert first["claims_refund"] == pytest.approx(
        sum(s1.claims(m, "REFUND") for m in range(241, 252)), rel=1e-12)
    assert first["claims_refund"] < whole["claims_refund"]
    later = _row(sec_model, "future", 8, -13).result_annual()
    assert list(later.index) == list(range(1, 61))


def _run_sec(script, *args, check=True):
    """Run ``script``, a ``run_sec.py``, with ``args``; its output, checked ASCII.

    With ``check=False`` the finished process is returned instead, whatever its exit code,
    for a test that expects the runner to fail.
    """
    done = subprocess.run([sys.executable, str(script), *args], capture_output=True,
                          timeout=300)
    if not check:
        return done
    assert done.returncode == 0, done.stderr.decode(errors="replace")
    assert done.stdout.isascii(), "run_sec.py printed a non-ASCII character"
    return done.stdout.decode("ascii")


def _relabelled(table):
    """An administration extract of ``table``: no generator columns, labels moved by 100,
    the rows in reverse order.

    Every generated table numbers its points from 1, in table order, so on it a label and a
    position look alike; on this one they never agree.
    """
    extract = table.drop(columns=list(GENERATED_COLUMNS))
    extract.index = pd.Index(extract.index + 100, name="point_id")
    return extract.iloc[::-1]


def _relabelled_schedule(schedule):
    """The premium schedule of :func:`_relabelled`'s extract: each premium under its point's
    new label."""
    return schedule.assign(point_id=schedule["point_id"] + 100)


def test_an_in_force_extract_needs_none_of_the_generator_columns(sec_model, tmp_path):
    """The model reads the in-force interface and S's columns, never where a row came from.

    ``row_kind``, ``source_policy_id`` and ``source_mth`` record how the generator made each
    shipped row, and an administration extract carries none of them; nor does it number
    its points 1 to n in table order.  Read without them, relabelled 101..126 and reversed,
    its premium schedule relabelled with it (:func:`_relabelled`), each point projects what
    the committed row it was relabelled from projects, in ``result_cf`` and
    ``result_pols``, to 1e-12: every row in force or issued later, and the twins that carry
    each flow beside them (:data:`FLOW_TWINS`).  And ``run_sec.py``, run beside that
    extract, prints the point it was given by its label, 119, the anchor a month into its
    income phase, without saying where it came from.  On every shipped row ``source_mth``
    equals ``duration_mth``, so a formula that read the one for the other would pass every
    test that leaves ``duration_mth`` as generated.
    """
    extract = _relabelled(_committed())
    folder = _sec_inputs(tmp_path, extract,
                         schedule=_relabelled_schedule(_committed_schedule()))
    model = _read(folder, "extract")
    try:
        table = model.Data.model_point_table()
        assert not set(GENERATED_COLUMNS) & set(table.columns)
        assert list(table.index) == list(range(126, 100, -1))
        for point_id in (p + 100 for p in _flow_points(_committed())):
            key = _key(model, point_id)
            mine, base = projection(model, key), _point(sec_model, point_id - 100)
            for report in REPORTS:
                assert frame_mismatches(base.cells[report](), mine.cells[report](),
                                        rtol=1e-12, atol=1e-12) == [], (point_id, report)
            _release(model, key)
    finally:
        model.close()
    runner = folder.parent / "run_sec.py"
    shutil.copy(model_path(SEC).parent / "run_sec.py", runner)
    out = _run_sec(runner, "119")
    assert out.splitlines()[:3] == [
        "model point 119: DIA-000001-M241 - NQ CR F60 - premiums due none",
        "deferral DB = ROP   income starts at policy month 240 (attained age 80)   m = 12 "
        "in arrears   COLA = 0%",
        "at the valuation date: in payout 1 month: policy year 21, lives 0.712045 alive, "
        "income 44,259.65/yr, 0 certain months left"]


def test_run_sec_block_refuses_before_printing(tmp_path):
    """``run_sec.py --block`` asks every point for its frame before it projects any.

    The point at or past the stop rule is refused in ``proj_len()`` when the block reaches
    it, which a loop over the block would do only after projecting the points before it.
    So the runner asks every point for its frame first: run beside the refused table, as an
    extract relabelled and reversed (:func:`_relabelled`) holds it, it exits non-zero,
    prints nothing, and names the point by its label, 125, not by its position.
    """
    extract = _relabelled(REFUSED[0][2](_committed()))
    folder = _sec_inputs(tmp_path, extract,
                         schedule=_relabelled_schedule(_committed_schedule()))
    runner = folder.parent / "run_sec.py"
    shutil.copy(model_path(SEC).parent / "run_sec.py", runner)
    done = _run_sec(runner, "--block", check=False)
    assert done.returncode != 0 and done.stdout == b""
    assert REFUSED[0][3].replace("point_id 25", "point_id 125") in done.stderr.decode(
        errors="replace")


def _shown(df):
    """A frame as ``run_sec.py`` prints it: to the cent, with no negative zero."""
    return (df.round(2) + 0.0).to_string()


def _standing(p):
    """What ``run_sec.py`` says of point ``p`` at the valuation date, stated here."""
    d = p.duration_mth_init()
    if d < 0:
        return f"to be issued at t = {-d}, {-d} months after the valuation date"
    if d == 0:
        return "issued at the valuation date, t = 0"
    alive = f"{p.lives_if_init(1):.6g}"
    if p.is_joint():
        alive += f" and {p.lives_if_init(2):.6g}"
    start = p.income_start_mth()
    if d < start:
        return (f"in deferral {d} month{'' if d == 1 else 's'}: policy year "
                f"{p.policy_year(0)}, lives {alive} alive, premiums paid "
                f"{p.cum_premium_pp_init():,.0f}, income bought "
                f"{p.annual_income_init():,.2f}/yr, the income starts at t = {start - d}")
    paid, left = d - start, max(start + p.certain_mths_eff() - d, 0)
    return (f"in payout {paid} month{'' if paid == 1 else 's'}: policy year "
            f"{p.policy_year(0)}, lives {alive} alive, income "
            f"{p.annual_income_init():,.2f}/yr, {left} certain month"
            f"{'' if left == 1 else 's'} left")


def test_run_sec_prints_a_point_and_the_block(sec_model):
    """The runner prints one point, saying where it came from, and the block (D8).

    Each mode in an interpreter of its own, as a user runs it, with exit code 0 and ASCII
    output, so that it prints on a Windows console under any code page.  The numbers are
    the model's.  Point 1, the runner's default, the worked example's anchor issued at the
    valuation date, with its lines each asserted whole, so that a longer number cannot pass
    for the one asserted, and its first fifteen rows of cash flows and counts, as ``run.py``
    prints S's.  Point 19, the anchor a month into its income phase, point 26, the joint
    point issued 13 months on, and point 25, the anchor in its last month, each with the
    lines that say where its row came from and where it stands, which only the committed
    table's generator columns can say;
    point 25's frame has one row, and its headings say so, in the singular.  And the block:
    a line for each of the 26 points, in table order, its first fifteen rows, which must be
    the committed points' frames summed row by row, as this test sums them, and those frames
    summed into projection years, each year's ``pols_if`` its first month's.  Nothing else
    runs the runner on the committed table.
    """
    runner = model_path(SEC).parent / "run_sec.py"
    head = ("proj_len = {} months from the valuation date (t = 0..{}); the stop rule at "
            "policy month 720")
    out = _run_sec(runner)
    assert out.splitlines()[:5] == [
        "model point 1: DIA-000001 (S's DIA-000001) - NQ CR F60 - premiums due 100,000 at "
        "month 0, 50,000 at month 60",
        "deferral DB = ROP   income starts at policy month 240 (attained age 80)   m = 12 "
        "in arrears   COLA = 0%",
        "at the valuation date: issued at the valuation date, t = 0",
        head.format(720, 719),
        "pricing factors = table   CP(T) = 150,000   B = 44,259.65/yr = 3,688.30/instalment"
        "   guarantee = 3.3891 yrs (0 certain months)"]
    assert "first 15 rows, t = 0..14 (months from the valuation date):" in out.splitlines()
    anchor = _point(sec_model, 1)
    assert _shown(anchor.result_cf().head(15)) in out
    assert (anchor.result_pols().head(15).round(6) + 0.0).to_string() in out
    for point_id, lines in (
            ("19", ["model point 19: DIA-000001-M241 (S's DIA-000001 at its month 241) - "
                    "NQ CR F60 - premiums due none",
                    "at the valuation date: in payout 1 month: policy year 21, lives "
                    "0.712045 alive, income 44,259.65/yr, 0 certain months left",
                    head.format(479, 478)]),
            ("26", ["model point 26: DIA-000008-F13 (S's DIA-000008, issued 13 months on) "
                    "- NQ CR F60 + M63 - premiums due 100,000 at month 0, 50,000 at month "
                    "60",
                    "at the valuation date: to be issued at t = 13, 13 months after the "
                    "valuation date",
                    head.format(733, 732)]),
            ("25", ["model point 25: DIA-000001-M719 (S's DIA-000001 at its month 719) - "
                    "NQ CR F60 - premiums due none",
                    "at the valuation date: in payout 479 months: policy year 60, lives "
                    "6.13203e-08 alive, income 44,259.65/yr, 0 certain months left",
                    "proj_len = 1 month from the valuation date (t = 0..0); the stop rule "
                    "at policy month 720"])):
        printed = _run_sec(runner, point_id).splitlines()
        assert [printed[0], *printed[2:4]] == lines, point_id
    for heading in ("the one row, t = 0 (months from the valuation date):",
                    "counts, survival and payment factors, the one row, t = 0:"):
        assert heading in printed, heading
    out = _run_sec(runner, "--block")
    table = sec_model.Data.model_point_table()
    points = [projection(sec_model, key) for key in point_keys(sec_model)]
    assert out.splitlines()[:len(points) + 1] == [
        "model points, t = 0 the valuation date for each:",
        *("  {:>2}  {:<16} {}; proj_len {}".format(
            point_id, table.at[point_id, "policy_id"], _standing(p), p.proj_len())
          for point_id, p in zip(table.index, points))]
    block = pd.concat([p.result_cf() for p in points]).groupby(level="t").sum()
    assert _shown(block.head(15)) in out
    years = pd.Index(block.index // 12 + 1, name="proj_year")
    annual = block.drop(columns="pols_if").groupby(years).sum()
    annual.insert(0, "pols_if", [block.at[12 * (y - 1), "pols_if"] for y in annual.index])
    assert _shown(annual.head(12)) in out


def _docs(model):
    """``(where, docstring)`` for the model, each Space and each cells, blanks as ``""``."""
    yield "model", model.doc or ""
    for space in model.spaces.values():
        yield space.name, space.doc or ""
        for cells in space.cells.values():
            yield f"{space.name}.{cells.name}", cells.doc or ""


def _mapped_cells(doc):
    """The names in the Cells column of the symbol map in ``doc``, the Projection docstring.

    The map is an RST simple table whose header row starts ``Notes symbol``.  The runs of
    ``=`` in the border under the header give the column spans, and a row whose Cells
    column is blank continues the meaning of the row above.  A name is the identifier that
    opens the column, ``age`` of ``age(t, life)``.
    """
    lines = doc.splitlines()
    head = next(i for i, line in enumerate(lines) if line.startswith("Notes symbol"))
    start, end = [m.span() for m in re.finditer("=+", lines[head + 1])][1]
    names = set()
    for line in lines[head + 2:]:
        if line.startswith("="):
            break
        found = re.match(r"[a-z_][a-z0-9_]*", line[start:end].strip())
        if found:
            names.add(found.group())
    return names


# What only DIA_US_S's docstrings may say: a reference into its Spaces, which the SEC pages
# would link to the wrong model; its clock, t counting policy months from issue and t = 0
# the issue month; and "then clear the cache", modelx-only advice that a compiled model
# cannot follow.
STALE = re.compile(r"~\.DIA_US_S\.|``t`` counts \*\*policy months from issue"
                   r"|t counts months from issue|``t = 0`` is the issue month"
                   r"|then clear the cache")


def test_the_docstrings_describe_the_valuation_clock(sec_model, s_model):
    """The docstrings say what this model is, and none says what only DIA_US_S is.

    Whitespace is collapsed first, as ``test_model_conventions`` collapses it, so that a
    phrase split across a line break still matches.  The model docstring names the
    valuation date, BasicTerm_SE, the policy clock, both SEC files and the product.  The
    cells running in force adds are exactly :data:`NEW_CELLS`, beside every cell of
    ``DIA_US_S``'s, and the symbol map in the Projection docstring maps each of them and
    names nothing the model lacks: every name in it is a cell, or a Reference the notes give
    a symbol to, as the A/E factor is in ``DIA_US_S``'s map.  And no docstring says what
    :data:`STALE` matches, which ``DIA_US_S``'s own docstrings say.
    """
    flat = {where: re.sub(r"\s+", " ", doc) for where, doc in _docs(sec_model)}
    for phrase in ("valuation date", "BasicTerm_SE", "duration_mth", TABLE, SCHEDULE,
                   "deferred income annuit"):
        assert phrase in flat["model"], phrase
    sec_cells, s_cells = set(sec_model.Projection.cells), set(s_model.Projection.cells)
    assert s_cells <= sec_cells, sorted(s_cells - sec_cells)
    assert sec_cells - s_cells == set(NEW_CELLS), sorted((sec_cells - s_cells)
                                                         ^ set(NEW_CELLS))
    mapped = _mapped_cells(sec_model.Projection.doc)
    missing = [cells for cells in NEW_CELLS if cells not in mapped]
    assert not missing, f"the symbol map does not map {missing}"
    known = set(sec_model.Projection.cells) | set(sec_model.Projection.refs)
    unknown = sorted(mapped - known)
    assert not unknown, f"the symbol map names what the model lacks: {unknown}"
    stale = sorted(where for where, doc in flat.items() if STALE.search(doc))
    assert not stale, f"docstrings that describe DIA_US_S: {stale}"
    s_flat = [re.sub(r"\s+", " ", doc) for _, doc in _docs(s_model)]
    assert all(any(re.search(part, doc) for doc in s_flat)
               for part in STALE.pattern.split("|")), "a STALE phrase S does not say"


def test_the_sec_model_reads_the_s_tables_in_place(sec_model, s_model):
    """One copy of each assumption table serves both models (D1).

    The two ``input_dir()`` s are one directory, and SEC's filename References are S's with
    ``model_point_file`` and ``premium_schedule_file`` alone changed, to
    ``model_point_table_sec.csv`` and ``premium_schedule_sec.csv``: an edit to an assumption
    table reaches both models, and the two can never drift apart.
    """
    assert sec_model.Data.input_dir() == s_model.Data.input_dir()
    files = {r: v for r, v in s_model.Data.refs.items() if r.endswith("_file")}
    assert {r: v for r, v in sec_model.Data.refs.items() if r.endswith("_file")} == {
        **files, "model_point_file": TABLE, "premium_schedule_file": SCHEDULE}


def test_the_core_grid_reaches_every_branch(spliced, splice_records):
    """What the default run's T2 and T3 cases reach, which the full grid only multiplies.

    The default run thins the splice to a core (the module docstring), and this test is
    what keeps the thinning from costing a branch.  First, statically, over S's table with
    the variants, each property below holds of some core case: each form; joint and single
    lives; each trigger on a joint contract; each mortality and factor basis; each timing
    and frequency, and each frequency below monthly with each timing valued off its period,
    where a payment month counted on the wrong clock shows; each market type and
    death-benefit form; each sex in each role; a COLA and none on a refund form; a rounding
    of the purchase rate to 6 and to 4 places and none; each option, the adjustment
    deferring and advancing; and each kind of valuation month: an anniversary, mid-year,
    the month before a premium and the premium's own, the income start month and the month
    before it, each option's month and a month after it, a guarantee's last month, and the
    last month of a frame.  Of some core future case: issued 1, 12 and more than 12
    months on, joint and single, each refund form, a guarantee, each option.  And the
    splice's two edited tables give every ``(age, sex)`` below omega a value of its own, so
    that a join on the wrong key changes a number.

    Then, on the splice's model, of some core row, each of :data:`AT_VALUATION` and
    :data:`IN_FRAME`, what no column of the table shows: every opening-state column at each
    value it takes, what falls at ``t = 0`` because of where the contract stands, and each
    branch of the refund, the guarantees, the options, the cap and the QLAC overlay later in
    the frame.  Each core row's branches were recorded by the case that compared it
    (:func:`_record`), and a row no case has recorded is evaluated here.
    """
    s = spliced[0]
    s_table = _s_table_with_variants()

    def at(p, column):
        return s_table.at[p, column]

    def option(p, column):
        value = at(p, column)
        return -1 if pd.isna(value) else int(value)

    def start(p):
        return option(p, "adjust_start_mth") if option(p, "adjust_mth") >= 0 else int(
            at(p, "income_start_mth"))

    def n_eff(p):
        return _point(s, p).certain_mths_eff()

    def premium_months(p):
        return set(_point(s, p).premium_by_mth())

    def step(p):
        return 12 // int(at(p, "frequency"))

    splices = {
        **{f"the {f} form": (lambda k, p, d, f=f: at(p, "income_form") == f)
           for f in ("LO", "LO_ROP", "CR", "IR", "PC")},
        "a joint contract": lambda k, p, d: at(p, "joint"),
        "a single life": lambda k, p, d: not at(p, "joint"),
        **{f"the {trig} trigger, joint": (lambda k, p, d, trig=trig: (
            at(p, "joint") and at(p, "reduction_trigger") == trig))
           for trig in ("either", "primary")},
        **{f"the {b} mortality basis": (lambda k, p, d, b=b: at(p, "mort_basis") == b)
           for b in ("anchor", "generational")},
        **{f"the {b} factor basis": (lambda k, p, d, b=b: at(p, "factor_basis") == b)
           for b in ("table", "formula")},
        **{f"{m} timing": (lambda k, p, d, m=m: at(p, "timing") == m)
           for m in ("arrears", "advance")},
        **{f"{m} payments a year": (lambda k, p, d, m=m: at(p, "frequency") == m)
           for m in (12, 4, 2, 1)},
        **{f"the {m} market": (lambda k, p, d, m=m: at(p, "market_type") == m)
           for m in ("NQ", "TradIRA", "RothIRA", "QLAC")},
        **{f"the {f} death benefit": (lambda k, p, d, f=f: at(p, "db_form") == f)
           for f in ("ROP", "NONE")},
        **{f"a {sex} {role}": (lambda k, p, d, sex=sex, c=c: (
            (c == "sex" or at(p, "joint")) and at(p, c) == sex))
           for sex in ("M", "F") for role, c in (("primary", "sex"),
                                                 ("joint annuitant", "joint_sex"))},
        "a COLA on a refund form": lambda k, p, d: (
            at(p, "income_form") in ("CR", "IR") and at(p, "cola_rate") > 0.0),
        "no COLA on a refund form": lambda k, p, d: (
            at(p, "income_form") in ("CR", "IR") and at(p, "cola_rate") == 0.0),
        **{f"a purchase rate rounded to {n} places": (
            lambda k, p, d, n=n: at(p, "purchase_rate_dp") == n) for n in (6, 4)},
        "a purchase rate at full precision": lambda k, p, d: pd.isna(
            at(p, "purchase_rate_dp")),
        "other QLAC premium": lambda k, p, d: at(p, "other_qlac_premium") > 0.0,
        "an adjustment deferring the start": lambda k, p, d: (
            option(p, "adjust_mth") >= 0 and start(p) > at(p, "income_start_mth")),
        "an adjustment advancing the start": lambda k, p, d: (
            option(p, "adjust_mth") >= 0 and start(p) < at(p, "income_start_mth")),
        "on an anniversary": lambda k, p, d: d % 12 == 0,
        "mid-year": lambda k, p, d: d % 12 not in (0, 11),
        "the month before a premium": lambda k, p, d: d + 1 in premium_months(p),
        "a premium month": lambda k, p, d: d in premium_months(p) and d > 0,
        "the month before the income start": lambda k, p, d: d == start(p) - 1,
        "the income start month": lambda k, p, d: d == start(p),
        **{f"valued in the {o} month": (
            lambda k, p, d, o=o: option(p, o) >= 0 and d == option(p, o))
           for o in ("adjust_mth", "accel_mth", "commute_mth")},
        **{f"valued after the {o} month": (
            lambda k, p, d, o=o: 0 <= option(p, o) < d)
           for o in ("adjust_mth", "accel_mth", "commute_mth")},
        "in a guarantee's last month": lambda k, p, d: n_eff(p) > 0 and (
            d == start(p) + n_eff(p) - 1),
        "in the last month of a frame": lambda k, p, d: d == _point(s, p).proj_len() - 1,
    }
    pairs = {(int(at(p, "frequency")), at(p, "timing")) for p in s_table.index
             if at(p, "frequency") != 12}
    for m, timing in sorted(pairs):
        splices[f"{m} a year in {timing}, off its period"] = (
            lambda k, p, d, m=m, timing=timing:
            (int(at(p, "frequency")), at(p, "timing")) == (m, timing)
            and (d - start(p)) % step(p) != 0)
    futures = {
        "issued a month on": lambda p, k: k == 1,
        "issued a year on": lambda p, k: k == 12,
        "issued more than a year on": lambda p, k: k > 12,
        "a joint contract": lambda p, k: at(p, "joint"),
        "a single life": lambda p, k: not at(p, "joint"),
        **{f"the {f} form": (lambda p, k, f=f: at(p, "income_form") == f)
           for f in ("CR", "IR", "PC")},
        **{f"the {o} option": (lambda p, k, o=o: option(p, o) >= 0)
           for o in ("adjust_mth", "accel_mth", "commute_mth")},
    }
    missing = [what for what, holds in splices.items()
               if not any(holds(*case) for case in CORE_SPLICES)]
    missing += [what for what, holds in futures.items()
                if not any(holds(*case) for case in CORE_FUTURES)]
    assert not missing, f"no core case reaches: {missing}"
    assert len(pairs) == 6, sorted(pairs)

    for name, column in (("mort_table", "mort_rate"),
                         ("improvement_scale", "improvement_rate")):
        rates = s.Data.cells[name]()[column]
        below = rates[rates.index.get_level_values("age") < s.Projection.omega_age]
        assert below.is_unique, f"{name}: two (age, sex) rows share a value"

    reached = set()
    for case in sorted(CORE_GRID, key=str):
        reached |= _record_of(spliced, splice_records, case)["branches"]
    missing = [what for what in (*AT_VALUATION, *IN_FRAME) if what not in reached]
    assert not missing, f"no core row reaches: {missing}"
