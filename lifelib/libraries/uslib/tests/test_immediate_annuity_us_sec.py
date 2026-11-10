"""In-force tests for SPIA_US_SEC: the splice, future business, counts, regeneration.

``SPIA_US_SEC`` is ``SPIA_US_S`` taught to run in force at a valuation date
(USLIB-SEC-PLAN.md, milestone M11).  It runs on two clocks: ``t`` counts months from the
valuation date, the same month for every model point, and ``duration_mth(t)`` counts the
months from the annuity date, ``duration_mth_init() + t``.  A model point may be a contract
already in payment at the valuation date, in any month of any policy year, one whose annuity
commences at it, or one commencing up to ten years after it, as in
``basiclife/BasicTerm_SE``.  A contract in payment opens with four columns of state beside
its count: each covered life's probability of being alive at the valuation date, the
commutation fraction the owner's withdrawals have taken by then, and the 10-year CMT's
change since its annuity date, which moves its commutation discount rate.  The payments to
date need no column, because they are a deterministic schedule summed on the policy clock,
and neither do the certain months left, which follow from ``duration_mth``.

The worked example is not restated here.  On a point commencing at the valuation date the
two clocks coincide and the model is ``SPIA_US_S``, and ``test_model_conventions.py``
asserts that cell by cell on the twins of S's fifteen points (T1), so every golden of
``test_immediate_annuity_us.py`` holds on this model with no number copied.  The
conventions also hold the SEC family's other rules: every frame opens at ``t = 0``,
``BEF_DECR`` is ``BEF_NB`` plus the month's new business, new business enters once, and
nothing happens before the annuity date.  ``pols_if`` here is the notes' closing obligation
measure, as in S, so the model is registered ``closing_pols_if`` and skips the convention
that ``pols_if`` is the ``BEF_DECR`` count; this module asserts what it is instead.  It
holds the rest of the plan's tests (its §5.2) and the product's own facts:

* T2, the splice: an S point restated in payment at month ``d``, opened with the state S
  carries into ``d``, continues S's projection from ``d`` on, in every cell of S's and in
  ``result_pols``.  The months are the ones S's events need: the first anniversary and the
  months either side, the worked example's death month and the month after it, the last
  month of a certain period and the first after it, the trim months of the installment
  refunds, the commutation months, and the last month of a frame.  Eleven variants of S's
  points, in a copy of S's table, reach what S's own points cannot.
* T3, future new business: an annuity commencing ``k`` months after the valuation date is
  S's projection ``k`` months on, with zeros before it and no rate evaluated there.
* D11's R1, R1a and R2, and D3's clock: on the splice's grid no cell is called at a negative
  argument, nor at a policy month, a policy year or an age the contract does not have, none
  evaluated on the books reads a month before them, and none reads beyond ``t + 1``; on the
  committed points no recursion runs backward over the frame, a cold call runs one cell a
  month, and the policy clock is a closed form.
* T4, the count algebra: the count is on the books from the annuity date to the stop rule,
  ``pols_if`` is S's closing measure on it, ``result_pols`` is S's report with the new
  business beside it, and multiplying ``policy_count`` by 2.5, with every assumption that
  ships at zero switched on, multiplies every flow and moves no per-contract value.
* T5, validation: each malformed in-force row is refused as the table is read, naming its
  point, and so is a malformed surrender-charge scale; a point at or past the stop rule, or
  owing nothing, is refused by ``proj_len()``; the future horizon is a Reference that
  bounds future business, and at 0 refuses it; the edges of the interface are accepted,
  each check over a window of contract months refused just inside each end and read just
  outside it; and every state S reaches, restated in force, is accepted, but a contract
  owing nothing, which is refused by name.
* T6, regeneration: the committed ``model_point_table_sec.csv`` is what the generator makes
  of ``SPIA_US_S`` and its table as they stand.
* Then the product's own facts: the worked example's derived rows, survival per life, the
  payments to date on the annuity-date clock, the commutation fraction, the CMT's change
  since each contract's own annuity date, the simple discount, improvement on the policy
  clock and inflation on the valuation clock, the capped mortality rate and a NaN that
  reaches either cap, no premium and no acquisition, the name clash, the stop rule, the
  values outside cover, the block, an in-force extract, the runner, the docstrings, the
  shared input tables, invalid values, and what the default grid reaches.
* C2, the fingerprint: every committed point computes what the model computed when Phase 1
  ended, frozen at the end of this module before Phase 2 changed anything (§5.4).

SEC month ``t`` is S month ``t + source_mth`` throughout, the direction in which
``sec_support`` takes its ``t_offset``: ``d`` for a point restated at S month ``d``, ``-k``
for one commencing ``k`` months on.  ``SPIA_US_S`` has no point in payment, so every twin is
new business, compared by T1, and every splice case is a derived row.

**The core grid and the full one** (USLIB-SEC-PLAN.md K6).  T2 and T3 over every month the
product's events need, 62 splices and 29 future points, would take this module past three
minutes in every run.  By default they run a core of 29 and 11, chosen so that between them
they reach every form, trigger, basis, timing and frequency, every opening-state column,
every kind of valuation month and every branch the full grid reaches, which
``test_the_core_grid_reaches_every_branch`` asserts.  The other cases, and the rules test's
scan of their rows, carry the ``sec_full`` marker and are skipped, with the reason shown,
unless ``USLIB_SEC_FULL=1`` is set.  They are never dropped: one leg of the CI matrix sets
it, and ``USLIB_SEC_FULL=1 python -m pytest -m sec_full`` on this module runs them alone.
The every-state test restates S's states at the edges of the product's windows by
default, and at every month of every frame with ``USLIB_SEC_FULL=1``.  Memory is the other
cost.  A projected point holds its cached values and their dependency graph, so a row read
once, a splice case's or a point of a temporary copy, is released as soon as it has been
read (``_release``), and the splice's rows are held one at a time, however large the grid.
The three models the module sweeps once and holds, the splice's S model and the committed
S and SEC models, are frozen out of the collector (``gc.freeze``), so that a collection
scans only what a test has made since, and the freeze is undone as the module ends
(:func:`_freeze`).

Every test keeps four rules.  Each model is read under a name of its own and closed:
``test_immediate_annuity_us.py`` reads S under its default name, and reading a model under a
name in use renames the open one.  No test writes inside the library tree: every changed
input goes through ``sec_support.temp_inputs`` into a temporary directory, because a CSV
added beside the models, even briefly, would fail a concurrent
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
    codes, fingerprint_mismatches, frame_mismatches, temp_inputs, twin_mismatches)
from us_registry import model_path, point_keys, projection

SEC, TWIN, TABLE = "SPIA_US_SEC", "SPIA_US_S", "model_point_table_sec.csv"
SPEC = SEC_SPECS[SEC]
NAN = float("nan")

# Eleven more S points, in the splice's copy of S's table and never in the committed one,
# each one of S's points changed so as to reach what S's own points cannot.  S's points
# pay monthly, but for one quarterly in advance; carry the worked example's male primary
# and female joint annuitant; are rated 1.0, issued in 2026 at 65 and 62, pay no premium
# tax and hold no commutation right but on one point.  Each variant is (the S point it
# changes, the columns it changes); the policy_id keeps the generated ids apart.
#
# 16, the anchor on the table basis paying semi-annually, its sexes swapped, so that the
#   two table joins read each sex in each role;
# 17, the cash refund on the table basis paying annually in advance: a refund weighted by
#   a probability, and the refund balance G(k + 1) of an advance payment month;
# 18, the installment refund on a 2% COLA path paying quarterly, with the commutation
#   right: the refund period searched on a rising schedule, a trim that is not a no-op
#   (197.93 of 1,979.22 at policy month 176), and withdrawals from a derived period;
# 19, the installment refund at B(1) 4,800 paying semi-annually in advance: the advance
#   search, from k = 1, and its trim, 1,600.00 at policy month 246;
# 20, the anchor on the primary trigger, rated 1.25 and commencing in 2020: the primary
#   trigger on probabilities, another calendar origin for the improvement, and the rating's
#   cap, min(1.25 q, 1), binding from attained age 117, before omega;
# 21, the commuting anchor in an issue state that bars the withdrawal;
# 22, certain_only paying annually in advance, with the right: commutation on the one form
#   without a life contingency, and a commutation month with no certain instalment left to
#   commute (policy month 108);
# 23, certain_only turned life_certain at 95 on a female life, 360 months certain, with a
#   premium tax and qualified money: a certain period that outlasts the age stop, so that
#   mortality reaches 1 and improvement 0 inside the frame;
# 24, the anchor as a joint cash refund at a survivor percentage of 100%, as [S5] offers
#   it: the refund on the last death;
# 25, the installment refund at B(1) 1,500 paying annually in arrears: a search that never
#   repays the premium, capped at the age stop, whose last instalment repays the rest,
#   19,000.00 at policy month 659 against 1,500.00 scheduled;
# 26, the installment refund at a premium of 1,000 paying quarterly in advance: the first
#   instalment repays the premium, so the trim at policy month 0 reads G at the annuity
#   date, where S reads it two months before.
VARIANTS = {
    16: (8, {"policy_id": "IA-900016", "frequency": 2, "primary_sex": "F",
             "joint_sex": "M"}),
    17: (6, {"policy_id": "IA-900017", "mort_basis": "table", "death_mth_1": NAN,
             "frequency": 1, "timing": "advance"}),
    18: (7, {"policy_id": "IA-900018", "cola_rate": 0.02, "frequency": 4,
             "commutation_enabled": True}),
    19: (12, {"policy_id": "IA-900019", "timing": "advance", "frequency": 2}),
    20: (8, {"policy_id": "IA-900020", "reduction_trigger": "primary",
             "annuity_year": 2020, "rating_factor": 1.25}),
    21: (9, {"policy_id": "IA-900021", "issue_state_excludes_withdrawal": True}),
    22: (15, {"policy_id": "IA-900022", "commutation_enabled": True, "frequency": 1,
              "timing": "advance"}),
    23: (15, {"policy_id": "IA-900023", "form": "life_certain", "primary_age": 95,
              "primary_sex": "F", "certain_months": 360, "premium_tax_rate": 0.02,
              "qualified": True}),
    24: (8, {"policy_id": "IA-900024", "form": "cash_refund", "survivor_pct": 1.0}),
    25: (7, {"policy_id": "IA-900025", "annual_income": 1500, "frequency": 1}),
    26: (7, {"policy_id": "IA-900026", "frequency": 4, "timing": "advance",
             "premium": 1000}),
}

# T2's months, by S point or variant: every month S's events need, and no others.  11, the
# last month of policy year 1; 12, the first anniversary, B(2) and the first commutation
# month; 13, the worked example's death month, valued at its start, and the month after
# the first withdrawal; 14, the month after a scenario death; 24, the second anniversary
# and the second withdrawal; 37, after the residual floor's cap at 36; 119 and 120, 199 and
# 200, 249 and 250, the last month of a certain period and the first after it; 176, 246
# and 659, trim months; 30, both lives dead; 695, 659 and 359, the last month of a frame;
# 299 and 300, either side of omega inside a certain period; 72, a contract six years in
# payment; 100, before a commutation month with nothing left to commute; 1, 2 and 5,
# months between quarterly or semi-annual instalments.
SPLICE_MTHS = {1: (12, 13, 14), 2: (13, 14), 3: (14,), 4: (14,), 5: (14, 119, 120),
               6: (12, 13), 7: (12, 199, 200), 8: (11, 12, 13, 24, 695),
               9: (12, 13, 24, 37, 120), 10: (13,), 11: (13,), 12: (249, 250),
               13: (14, 30, 119), 14: (1, 2), 15: (12, 119), 16: (5, 11, 12),
               17: (12, 13), 18: (12, 13, 176), 19: (12, 245, 246), 20: (13, 72),
               21: (12,), 22: (12, 13, 100), 23: (12, 299, 300, 359), 24: (13, 24),
               25: (12, 659), 26: (1,)}

# T2's cases, as (row_kind, S point, source_mth), and T3's, as (S point, k).  SPIA_US_S has
# no point in payment, so there is no twin to splice (§5.2's IN_FORCE_TWINS).  The future
# offset is 13: more than a year, so that a read before the annuity date lands at policy
# year -1, and off every payment step, so that the payment months fall apart on the two
# clocks.  12 puts the anniversaries back on the valuation years for the table basis and
# commutation, and 1 puts them a month off.
SPLICES = tuple(("derived", p, d) for p, ds in SPLICE_MTHS.items() for d in ds)
IN_FORCE_TWINS = ()
FUTURES = (tuple((p, 13) for p in range(1, 16)) + ((8, 12), (9, 12), (1, 1))
           + tuple((p, 13) for p in VARIANTS))

# The default run's cases (the module docstring), each with what it is there for.  The
# rest of SPLICES and FUTURES run with USLIB_SEC_FULL=1.
CORE_SPLICES = {
    ("derived", 1, 13): "the anchor in its death month: the reduction at t = 0",
    ("derived", 1, 14): "a joint contract with one life already dead",
    ("derived", 2, 14): "the primary trigger, the joint annuitant dead: paid in full",
    ("derived", 3, 14): "the primary dead: the two triggers coincide",
    ("derived", 5, 120): "the certain period ending at the valuation date",
    ("derived", 6, 13): "a cash refund in its death month: P - G(13) at t = 0",
    ("derived", 7, 199): "an installment refund in its last certain month",
    ("derived", 8, 12): "the table basis on an anniversary: two fractional lives",
    ("derived", 8, 695): "the last month: a one-row frame, the primary dead at omega",
    ("derived", 9, 12): "a withdrawal at t = 0",
    ("derived", 9, 13): "the commutation fraction opened at 0.5",
    ("derived", 9, 24): "a second withdrawal on an opened fraction; the floor at 36",
    ("derived", 10, 13): "advance in the death month: the instalment at t = 0 paid",
    ("derived", 11, 13): "an advance cash refund in a payment month: P - G(14)",
    ("derived", 13, 30): "both lives dead inside the certain period",
    ("derived", 14, 1): "quarterly in advance, valued between instalments",
    ("derived", 15, 119): "certain_only in its last certain month",
    ("derived", 16, 5): "semi-annual in arrears in a payment month; the sexes swapped",
    ("derived", 17, 13): "a table-basis cash refund annual in advance, off its period",
    ("derived", 18, 13): "a COLA installment refund paid quarterly, its fraction opened",
    ("derived", 18, 176): "the trim at t = 0, off its period",
    ("derived", 19, 245): "an installment refund semi-annual in advance: trim at t = 1",
    ("derived", 20, 72): "the primary trigger on the table basis, rated, from 2020",
    ("derived", 21, 12): "commutation barred by the issue state",
    ("derived", 22, 12): "certain_only commuting, annual in advance; nothing left at 108",
    ("derived", 23, 12): "a certain period past the age stop: q = 1 inside it",
    ("derived", 24, 13): "a joint cash refund on the table basis",
    ("derived", 25, 659): "the refund search capped: the last instalment repays the rest",
    ("derived", 26, 1): "a refund form quarterly in advance, valued between instalments",
}
CORE_FUTURES = {
    (1, 1): "scenario, joint, a month off the valuation anniversaries",
    (6, 13): "a cash refund more than a year on: G from its own annuity date",
    (7, 13): "an installment refund: its search and trim from its own annuity date",
    (8, 13): "the table basis, joint: policy year -1 before the annuity date",
    (9, 12): "commutation, on the valuation anniversaries: its first year barred",
    (14, 13): "quarterly in advance",
    (15, 13): "certain_only",
    (17, 13): "a cash refund annual in advance",
    (18, 13): "a COLA installment refund that commutes",
    (23, 13): "a certain period past the age stop",
    (26, 13): "the trim at the annuity date, its balance read at G(0)",
}

SEC_FULL = os.environ.get("USLIB_SEC_FULL") == "1"
FULL_ONLY = (pytest.mark.sec_full,
             pytest.mark.skipif(not SEC_FULL, reason="the full splice grid runs with "
                                "USLIB_SEC_FULL=1 (USLIB-SEC-PLAN.md K6)"))

# What the splice sets in S as it is read, before it computes anything, and in SEC alike
# but for the CMT's change (below).  Expense inflation is the one input SPIA reads on the
# valuation clock (D7): S inflates by policy year and SEC by valuation year, so at the
# shipped 2.5% the expenses of a point opened at d differ by design, and at 0 both factors
# are 1.  The clock itself is then asserted on its own, at the shipped rate.  Mortality
# improvement is calendar-dated, from each contract's own annuity year, so it moves with no
# clock and is not neutralized.  The rest ship at a value that hides some of the state from
# any comparison, and are switched on (SWITCHED_ON): commutation ships at zero
# utilization, which hides the fraction, and 0.5 reaches a withdrawal at t = 0, an opened
# fraction, the residual floor withholding one (36) and the minimum (48 on); cmt10_shift
# ships at 0, which hides the CMT's change in the discount rate.  The identity does not
# depend on the values, only on the two models describing the same contract.
SWITCHED_ON = {"commute_util_base": 0.5, "cmt10_shift": 0.005}
SPLICED_REFS = {"inflation_rate": 0.0, **SWITCHED_ON}

# The CMT's change is S's cmt10_shift, the change since each S contract's own annuity date,
# which S applies from month 0 on.  SEC reads the splice's table once, as a block is read,
# on one path of the CMT, which every point shares (D7).  Restated in payment at d, a
# point has seen all of S's change by the valuation date and carries it in
# cmt10_shift_init (the spec's state), and on that path nothing changes after it, so SEC's
# own cmt10_shift, the change made at the valuation date, is 0 (SEC_REFS).  Restated to
# commence k months on, a point has seen no change by its annuity date, its column is 0,
# and sees none after it, so its S twin, the same contract on that path, is S read with
# its cmt10_shift at 0 (LATER_REFS): the splice reads S twice, once for each kind of row.
# What SEC's cmt10_shift moves, each contract on the books at the valuation date and no
# contract commencing later, the CMT test below asserts, on one table read at two values.
SEC_REFS = {**SPLICED_REFS, "cmt10_shift": 0.0}
LATER_REFS = {**SPLICED_REFS, "cmt10_shift": 0.0}


def _improvement_apart(df):
    """Every ``(age, sex)`` row of the improvement scale apart from every other.

    The shipped scale is the same for both sexes at every age and flat at 0.01 below 86,
    so a join on the wrong sex or the wrong age would read the same number there, and no
    comparison with S could see it.  Scaled by age and sex, plus a small offset that keeps
    the scale's zero tail apart without lowering old-age mortality enough to move the
    rating's cap.  The mortality table is already apart by age and sex below omega, which
    ``test_the_core_grid_reaches_every_branch`` asserts of both copies.
    """
    age, female = df["age"], df["sex"] == "F"
    scale = female.map({True: 1.25, False: 1.0})
    offset = female.map({True: 1.5, False: 1.0})
    return df.assign(improvement_rate=df["improvement_rate"] * (1 + 0.004 * (age - 40))
                     * scale + 0.000001 * (age - 39) * offset)


# The edit both copies, S's and SEC's, carry.
SPLICED_EDITS = {"improvement_scale.csv": _improvement_apart}

# The cells T2 and T3 skip beyond T1's, which already drop result_pols (the spec's exempt).
# proj_len counts from the valuation date on SEC and from the annuity date on S, so it
# differs by d, or by -k, by design; frame_mismatches asserts what it must get right, that
# both frames end at the same instant.  payment_surv_mth returns a time point, which on
# SEC's clock is S's less d: payment_factor_life, which reads it, is compared, so a wrong
# survival point still fails.  cum_annuity_pp is not exempt: it is keyed by the policy
# clock in both models, and compares at the same k.
SPLICE_EXEMPT = TWIN_EXEMPT_DEFAULT | SPEC.exempt | {"proj_len", "payment_surv_mth"}
FUTURE_EXEMPT = SPLICE_EXEMPT

# The result_cf columns that expense inflation moves, and the cells they are made of: on
# the committed rows, at the shipped 2.5%, the only places a row in payment departs from S.
INFLATED = ("expenses", "liability_cf", "net_cf")
INFLATION_CELLS = frozenset({"inflation_factor", "expenses", "liability_cf", "net_cf",
                             "result_cf"})

# The decrement rates, none of which may be evaluated before the annuity date (R1, D4),
# and the two age-keyed table readers, which may not be read below an issue age.
DECREMENT_RATES = ("mort_rate", "mort_rate_mth", "mort_rate_base", "improvement_rate")
AGE_READERS = ("mort_rate_base_at", "improvement_rate_at")

# The opening state, in Data's order, and the cells running in force adds to SPIA_US_S's,
# each of which the symbol map must name.
STATE = ("lives_if_init_1", "lives_if_init_2", "commute_frac_cum_init", "cmt10_shift_init")
NEW_CELLS = ("policy_count", "duration_mth_init", "lives_if_init", "commute_frac_cum_init",
             "cmt10_shift_init", "annual_income_first", "t_entry", "stop_mth", "is_active",
             "is_payment_pm", "annuity_pp_sched_pm", "mort_rate_base_at",
             "improvement_rate_at", "pols_if_at", "pols_new_biz", "is_arrears",
             "is_scenario", "is_trigger_either", "is_period_certain", "is_certain_only",
             "is_cash_refund", "is_installment_refund", "is_disc_compound")

# The cells that scale with policy_count.  Every other cell is a per-contract amount, a
# probability, a rate, a clock or a flag, and must not move when the count does.
COUNTED = frozenset({
    "policy_count", "pols_if_init", "pols_if", "pols_if_at", "pols_new_biz",
    "annuity_payments", "claims", "commutations", "surr_charge", "expenses",
    "liability_cf", "net_cf", "result_cf", "result_pols"})

# result_pols' columns, in its order: the closing obligation measure and the annuities
# commencing in the month, then S's other seven columns in S's order, which no count moves.
RESULT_POLS = ["pols_if", "pols_new_biz", "lives_if_1", "lives_if_2", "lives_if_last",
               "lives_death_last", "certain_floor", "payment_factor_life", "payment_factor"]
RATES = RESULT_POLS[2:]

# BasicTerm_SE's two timings, which running in force adds (S has none), and the one kind.
TIMINGS = ("BEF_NB", "BEF_DECR")
KINDS = ("REFUND",)

# What each monthly cell holds outside cover, before the annuity date and from the stop
# rule on, as its docstring says: no count, so no cash flow; no instalment, no payment
# factor and no commutation; no question about the contract answered yes.  The type is part
# of the value: an amount, a probability or a rate is a float in every branch and a flag a
# bool, because Phase 2 types a cell by the values it returns (USLIB-SEC-PLAN.md F3).  The
# guard test also calls each of PER_LIFE for every covered life, pols_if_at at each timing,
# and claim_pp and claims at each kind, all 0.0, and before the annuity date the time-point
# cells of BEFORE_ISSUE, lives_if for both lives among them.
OUTSIDE_COVER = {
    "is_active": False, "is_payment_mth": False, "commute_elig": False,
    "annuity_pp_sched": 0.0, "annuity_pp": 0.0, "annuity_pp_paid": 0.0,
    "lives_death_last": 0.0, "certain_floor": 0.0, "payment_factor_life": 0.0,
    "payment_factor": 0.0, "pols_if": 0.0, "pols_new_biz": 0.0, "commuted_value": 0.0,
    "commute_amount": 0.0, "commute_frac_cum": 0.0, "surr_charge": 0.0,
    "annuity_payments": 0.0, "commutations": 0.0, "expenses": 0.0, "liability_cf": 0.0,
    "net_cf": 0.0, "check_payment_factor_resid": 0.0}
PER_LIFE = ("mort_rate_base", "improvement_rate", "mort_rate", "mort_rate_mth",
            "lives_death")
BEFORE_ISSUE = {"lives_if_last": 0.0, "check_lives_roll_fwd_resid": 0.0}

# The cells a month outside cover may not reach: every read keyed by an attained age or a
# policy year, and the calendar year.  The rates that read them hold 0.0 outside cover by
# their own guards, which the guard test asserts first; these have none, and no formula may
# reach them there, nor a caller (USLIB-SEC-PLAN.md F4).
IN_COVER_ONLY = ("age", "calendar_year", "mort_rate_base_at", "improvement_rate_at",
                 "commute_util_rate", "surr_charge_rate")

INFLATION = 0.025       # the shipped inflation_rate, which the inflation test reads

# The recursion limit, as mx.set_recursion takes it, under which the committed points are
# first swept (R2, F7).  A limit of n admits a call n + 1 cells deep, counted as modelx's
# stack trace counts them.  A report evaluates each column in ascending t, so a forward
# recursion, through t - 1, finds the month before already cached: the committed points'
# sweep runs 10 cells deep, a limit of 9, and a limit of 8 fails on points 7, 12 and 15,
# the payments to date and the income by policy year being based at the valuation date.
# Based at the annuity date, the income of the point in its 58th policy year needs a limit
# of 63, and a backward recursion over a frame longer than a month at least 576.
CALL_DEPTH = 40

# How deep a cold call may run beyond its chain, one cell a month from its month back to
# t_entry (D5).  Three cells recurse a month at a time, survival on the table basis, the
# commutation fraction on every point and the payments to date on a refund form, and the
# longest of them sets the depth: 696 lives_if cells of 706 levels on the anchor's twin on
# the table basis, 695 commute_frac_cum cells of 702 on its twin on the scenario basis,
# 647 cum_annuity_pp cells of 654 on the cash refund in payment 13 months.  Beyond the
# chain are the cells above it, from net_cf down, and below it the first month's rates,
# the age readers and Data's first reads of its tables: measured by modelx's stack trace
# at 7 to 11 levels on the committed points, and at 11 on the contract's longest cover,
# 1,224 months from issue age 18, which runs 1,234 cells deep, a recursion limit of 1,233
# (M11).  A chain of two cells a month doubles the depth, and needs twice the stack
# compiled.
CHAIN_OVERHEAD = 16

# The product's youngest lifetime issue age (product-spec), from which the longest cover
# runs to the age stop, and the depth test's two points there.
CONTRACT_MIN_AGE = 18

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
    collection scans only what the row made; with them in it, each would take seconds.
    """
    del model.Projection[key]
    if collect:
        gc.collect()


def _freeze():
    """Collect what is garbage, then freeze everything still alive out of the collector.

    Each module fixture that sweeps a model calls this once its sweep is done, so that the
    collections after it, automatic or :func:`_release`'s, no longer scan the millions of
    objects a swept model holds: with the splice's S model and the two committed models
    alive, one full collection takes about 2.7 s, and frozen, under a millisecond.  The
    collection first means no garbage is frozen with them.  The freeze is undone as the
    module ends (:func:`_collector`).
    """
    gc.collect()
    gc.freeze()


def _committed():
    """The committed SEC table as the file holds it, unvalidated, indexed by point_id."""
    return pd.read_csv(model_path(SEC).parent / TABLE, index_col="point_id")


def _sec_inputs(tmp_path, table, edits=None):
    """A copy of the product directory whose SEC table is ``table``; its SEC folder."""
    return temp_inputs(tmp_path, model_path(SEC), model_points=table,
                       model_point_file=TABLE, edits=edits)


def _read_edited(tmp_path, edit, tag="edited", refs=None):
    """SPIA_US_SEC read from a copy whose SEC table is ``edit(_committed())``."""
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


def _sweep(proj):
    """Evaluate on an S point or an SEC row what the splice compares: the reports and more.

    ``result_cf()``, ``result_pols()`` and ``check_payment_factor()``, then the cells no
    report reaches, so that the comparisons see them too: the three no-argument cells
    ``premium_tax_rate``, ``premium_net_pp`` and ``qualified``, and over the frame
    ``duration_mth``, ``surr_charge`` and each covered life's ``lives_death``.  Not
    ``check_lives_roll_fwd``: its independent rebuild of the survival path is quadratic in
    the frame, about 120 MB of modelx's dependency graph on a point on the table basis, and
    held in the splice's swept S model it would raise this module's memory by more than a
    gigabyte.  The conventions run it on every committed row, the rows in payment on the
    table basis among them, and T1 on every twin.
    """
    proj.result_cf()
    proj.result_pols()
    proj.check_payment_factor()
    for name in ("premium_tax_rate", "premium_net_pp", "qualified"):
        proj.cells[name]()
    lives = (1, 2) if proj.is_joint() else (1,)
    for t in range(proj.proj_len()):
        proj.duration_mth(t)
        proj.surr_charge(t)
        for life in lives:
            proj.lives_death(t, life)


def _continues_s(s_proj, sec_proj, month):
    """Where a committed row departs from S's point ``s_proj`` from S month ``month`` on.

    The splice's comparison, on the committed model at the shipped assumptions: frame by
    frame, ``result_cf`` and ``result_pols``, then cell by cell over every cell of S's but
    :data:`SPLICE_EXEMPT`.  The shipped 2.5% expense inflation steps by policy year in S and
    by valuation year here (D7), so :data:`INFLATED`'s three columns, and
    :data:`INFLATION_CELLS`, differ by design and are left out; the inflation test holds
    them.  Every other column and cell must agree, to 1e-9 relative with no absolute floor,
    as in T2 (USLIB-SEC-PLAN.md §5.2, precised at M11): SPIA's roll-forward residuals are
    exact zeros, so none needs the floor.
    """
    s_df = s_proj.result_cf()
    keep = [c for c in s_df.columns if c not in INFLATED]
    found = frame_mismatches(s_df, sec_proj.result_cf(), t_offset=month, columns=keep,
                             atol=0.0)
    found += frame_mismatches(s_proj.result_pols(), sec_proj.result_pols(),
                              t_offset=month, atol=0.0)
    return found + _mismatches(s_proj, sec_proj, t_offset=month,
                               exempt=SPLICE_EXEMPT | INFLATION_CELLS, atol=0.0)


def _case_id(kind, s_point, month):
    """A case's id: ``point2-d14``, or ``point8-k13`` if it commences later."""
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
    """SPIA_US_SEC read in place, as committed, and swept once, cold; what it met.

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
    """SPIA_US_SEC read in place, as committed, with every point swept (sec_read)."""
    return sec_read[0]


@pytest.fixture(scope="module")
def s_model():
    """SPIA_US_S read in place, as committed, with every point swept (:func:`_sweep`).

    T6 regenerates the SEC table from it, which would otherwise project every S point again
    (USLIB-SEC-PLAN.md §4, *Carried into Phase 1*), and the in-force tests read S's months
    off it.  The swept model is then frozen out of the collector (:func:`_freeze`).
    """
    model = mx.read_model(model_path(TWIN), name=_name("s"))
    for key in point_keys(model):
        _sweep(projection(model, key))
    _freeze()
    yield model
    model.close()


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


@pytest.fixture(scope="module")
def spliced(tmp_path_factory):
    """S and SEC on the splice's inputs: ``(s, sec, s_later)``.

    S is read from a copy of the product directory whose table has the variants appended
    and whose improvement scale is set apart (:data:`SPLICED_EDITS`), under
    :data:`SPLICED_REFS`, and every S point is swept (:func:`_sweep`) and stays swept.  SEC
    runs on the same assumption tables, and on a model point table of its own, built by
    the generator from the registered spec with its rows replaced by the cases this run
    selects, the core or the full grid (:func:`_selected`), out of this S model, so each
    row opens with the state of the very run it is compared with.  SEC reads the table
    once, under :data:`SEC_REFS`, as a block is read, on one path of the CMT, and each SEC
    row is projected by the case that compares it and released once compared.  A row
    commencing later is compared with ``s_later``, S read again from the same copy under
    :data:`LATER_REFS`, the same contract on that path; each of its points is swept by the
    T3 case that compares it and released with the row, so that ``s_later`` holds at most
    one swept point at a time.

    Everything alive once S is swept, S's points among them, is then frozen out of the
    collector (:func:`_freeze`), so that the collection after each row's release scans only
    what the row made, not the swept S model the module holds (measured on the full grid
    at M11: 152 s against 330 s collecting without the freeze, at the same peak).
    """
    root = tmp_path_factory.mktemp("spliced")
    s_folder = temp_inputs(root / "s", model_path(TWIN),
                           model_points=_s_table_with_variants(), edits=SPLICED_EDITS)
    s = _read(s_folder, "s_spliced", SPLICED_REFS)
    for key in point_keys(s):
        _sweep(projection(s, key))
    derived = [(p, d) for kind, p, d in _selected(SPLICES, CORE_SPLICES)]
    spec = dataclasses.replace(SPEC, derived=tuple(derived),
                               future=tuple(_selected(FUTURES, CORE_FUTURES)))
    table, companions = build_sec_table(spec, s)
    assert companions == {}
    sec_folder = temp_inputs(root / "sec", model_path(SEC), model_points=table,
                             model_point_file=spec.model_point_file, edits=SPLICED_EDITS)
    sec = _read(sec_folder, "sec_spliced", SEC_REFS)
    s_later = _read(s_folder, "s_spliced_later", LATER_REFS)
    _freeze()
    yield s, sec, s_later
    s_later.close()
    sec.close()
    s.close()


@pytest.fixture(scope="module")
def splice_records():
    """What each splice row was found to do, by case (:func:`_record`)."""
    return {}


# ---------------------------------------------------------------------------
# The splice's records
#
# Each T2 and T3 case sweeps its row, records what the rules test and the core grid's reach
# need of it, compares it with S, and releases it: held together, the rows of the full grid
# would hold several gigabytes.  The record is made before the comparison, because the
# comparison evaluates SEC's cells at S's own cached arguments, and those include keys SEC
# never reads itself: S's trim reads cum_annuity_pp(-2) on variant 26, and comparing it
# would plant that negative key in SEC's cache, for the rules test to report as SEC's.  So
# each of the two tests reads the records, and computes any case no earlier test has
# recorded, which keeps it whole when run alone.


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
    runs from the annuity date to the stop rule, ``stop_mth()``: the payments to date
    ``cum_annuity_pp(k)`` are read at time points 0 to ``stop_mth()``, the schedule at
    policy months 0 to ``stop_mth() - 1``, and the income, the utilization and the
    surrender charge at policy years 1 to the last month's, ``(stop_mth() - 1) // 12 + 1``.
    The age readers are read for a covered life at ages from its issue age to its age in
    the last month, below omega: at and above it the monthly cells answer without them.
    Each is a function of the point, so the ranges hold on every row, in payment or not.
    """
    stop = p.stop_mth()
    years = (stop - 1) // 12 + 1
    lives = (1, 2) if p.is_joint() else (1,)
    ages = {life: (p.age_at_entry(life),
                   min(p.age_at_entry(life) + years - 1, p.omega_age - 1))
            for life in lives}
    ranges = {"cum_annuity_pp": (0, stop), "annuity_pp_sched_pm": (0, stop - 1),
              "is_payment_pm": (0, stop - 1), "annual_income": (1, years),
              "commute_util_rate": (1, years), "surr_charge_rate": (1, years)}
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


def _rule_breaches(proj):
    """R1, R1a and R2 on one row, once it has been swept.

    ``{"negative": [...], "early": [...], "ahead": [...], "outside": [...]}``: every cached
    call with a negative argument; every precedent keyed by a month before ``t_entry()`` of
    a call keyed by a month at or after it; every precedent keyed by a month beyond
    ``t + 1`` of a call keyed by ``t``; and every policy-clock or age argument the contract
    does not have (:func:`_contract`).  A precedent is a call's as modelx's dependency graph
    records it.  SPIA admits no look-ahead at all, the term-blend read WholeLife admits
    included.
    """
    entry = proj.t_entry()
    negative, early, ahead = [], [], []
    for name, cells in proj.cells.items():
        t_pos = cells.parameters.index("t") if "t" in cells.parameters else None
        for args in _cached_args(cells):
            if any(_month(a) and a < 0 for a in args):
                negative.append(f"{name}{args}")
            if t_pos is None:
                continue
            t = args[t_pos]
            for node in cells.preds(*args):
                params = getattr(node.obj, "parameters", None) or ()
                u = node.args[params.index("t")] if "t" in params else None
                if not _month(u):
                    continue
                if u < entry <= t:
                    early.append(f"{name}{args} -> {node.obj.name}{node.args}")
                if u > t + 1:
                    ahead.append(f"{name}{args} -> {node.obj.name}{node.args}")
    return {"negative": negative, "early": early, "ahead": ahead,
            "outside": _outside_contract(proj)}


def _step(x):
    """The months from one instalment to the next on row ``x``."""
    return 12 // x.payment_freq()


def _off_period(x):
    """Whether row ``x`` is valued between two of its instalment dates, off its period."""
    return x.duration_mth_init() % _step(x) != 0


def _requested(x, t):
    """The withdrawal the owner asks for in month t, before the residual floor and the
    minimum: ``u(y) * CV(t)``, at most ``CV(t)``."""
    cv = x.commuted_value(t)
    return min(x.commute_util_rate(x.policy_year(t)) * cv, cv)


def _lives(x):
    return (1, 2) if x.is_joint() else (1,)


# What test_the_core_grid_reaches_every_branch asks of the core's rows in the model's own
# values, which no column of the table shows: each holds of some core row, or of a core row
# in some month of its frame.  At the valuation date, every opening-state column in use, at
# every value it takes: two fractional lives, one life of a joint contract dead, both dead
# inside a certain period, a fraction opened and a change in the CMT already seen, on a
# point whose rate it moves; then what falls at t = 0 because of
# where the contract stands: the survivor reduction, a refund, the advance refund balance,
# the trim, a withdrawal, an advance instalment, a payment month off monthly and a month
# between instalments.  Later in the frame, every branch of the commutation, the trim and
# the advance refund valued off its period (a row valued on its period would hide a
# payment month counted from the wrong clock), the rating's cap below omega, and omega
# inside a certain period.
AT_VALUATION = {
    "two fractional lives": lambda x: (
        x.is_joint() and 0.0 < x.lives_if_init(1) < 1.0 and 0.0 < x.lives_if_init(2) < 1.0),
    "one life of a joint contract dead": lambda x: (
        x.is_joint() and (x.lives_if_init(1) == 0.0) != (x.lives_if_init(2) == 0.0)),
    "both lives dead in a certain period": lambda x: (
        x.is_joint() and x.lives_if_last(0) == 0.0 and x.certain_floor(0) == 1.0),
    "a commutation fraction opened": lambda x: x.commute_frac_cum_init() > 0.0,
    "a CMT change seen, on a commuting point": lambda x: (
        x.cmt10_shift_init() != 0.0 and x.commutation_enabled()
        and x.commuted_value(0) > 0.0),
    "the survivor reduction at t = 0": lambda x: (
        x.is_joint() and x.payment_factor(0) == x.survivor_pct() < 1.0),
    "a refund at t = 0": lambda x: x.claims(0, _code(x, "REFUND")) > 0.0,
    "the advance refund balance at t = 0": lambda x: (
        not x.is_arrears() and x.is_payment_mth(0)
        and x.claims(0, _code(x, "REFUND")) > 0.0),
    "the trim at t = 0": lambda x: (
        x.is_installment_refund() and x.annuity_pp(0) != x.annuity_pp_sched(0)),
    "a withdrawal at t = 0": lambda x: x.commute_amount(0) > 0.0,
    "an advance instalment at t = 0": lambda x: (
        not x.is_arrears() and x.is_payment_mth(0) and x.annuity_payments(0) > 0.0),
    "a payment month at t = 0, off monthly": lambda x: (
        x.payment_freq() != 12 and x.is_payment_mth(0)),
    "a month between instalments at t = 0": lambda x: (
        x.is_active(0) and not x.is_payment_mth(0)),
    "the refund search capped at the age stop": lambda x: (
        x.is_installment_refund() and x.certain_mths_refund() == x.horizon_mths()
        and x.cum_annuity_pp(x.horizon_mths()) < x.premium_pp()),
}
IN_FRAME = {
    "a withdrawal, valued off its period": lambda x, t: (
        _off_period(x) and x.commute_amount(t) > 0.0),
    "the residual floor withholding a withdrawal": lambda x, t: (
        x.commute_elig(t) and x.commuted_value(t) > 0.0
        and _requested(x, t) >= x.commute_min_amount and x.commute_amount(t) == 0.0),
    "a withdrawal below the minimum": lambda x, t: (
        x.commute_elig(t) and 0.0 < _requested(x, t) < x.commute_min_amount),
    "a commutation month with nothing to commute": lambda x, t: (
        x.commute_elig(t) and x.commuted_value(t) == 0.0),
    "a trim, valued off its period": lambda x, t: (
        x.is_installment_refund() and _off_period(x)
        and x.annuity_pp(t) != x.annuity_pp_sched(t)),
    "the trim read at the annuity date": lambda x, t: (
        x.is_installment_refund() and x.certain_mths_refund() < _step(x)
        and x.annuity_pp(t) != x.annuity_pp_sched(t)),
    "the advance refund balance, valued off its period": lambda x, t: (
        x.is_cash_refund() and not x.is_arrears() and _off_period(x)
        and x.is_payment_mth(t) and x.claims(t, _code(x, "REFUND")) > 0.0),
    "mortality at 1 below omega": lambda x, t: not x.is_scenario() and any(
        x.mort_rate(t, life) == 1.0 and x.age(t, life) < x.omega_age for life in _lives(x)),
    "omega inside a certain period": lambda x, t: (
        not x.is_scenario() and x.certain_floor(t) == 1.0
        and x.age(t, 1) >= x.omega_age and x.mort_rate(t, 1) == 1.0
        and x.improvement_rate(t, 1) == 0.0),
}


def _branches(x, kind):
    """The names in :data:`AT_VALUATION` and :data:`IN_FRAME` that hold of row ``x``.

    A future row stands at its annuity date with nothing in payment, so only the frame's
    are asked of it.
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
    nowhere else, because on a point commencing at ``t = 0`` the two clocks coincide and the
    opening state is each life alive, nothing commuted and no change in the CMT.  The row
    is read in the splice's one read of its table, with SEC's CMT shift at 0
    (:data:`SEC_REFS`), so its commutation discount rate is S's only if it reads the change
    it carries.  For the same reason it is the
    test that catches a policy month passed as ``t`` (R1a): the payment months, the certain
    period, the trim, the commutation months and the refund balance all read the policy
    clock.  The frame comparisons read SEC row ``t`` against S row ``t + d`` in every
    column of ``result_cf`` and every column of ``result_pols`` both reports hold, and fail
    frames that end apart.  The cell comparison then evaluates every cell of S's but
    :data:`SPLICE_EXEMPT`, at every argument S cached inside its own frame from month ``d``
    on, moved onto SEC's clock, to 1e-9 relative with no absolute floor: each life's
    survival, the payments to date at every policy time point S read them, the commutation
    fraction, the counts and the payment factors among them.  The floor would hide what
    matters near the limiting age, where a capped rate kills lives whose survival is near
    1e-10.  An S cell this model lacked would fail it.

    The row is swept and recorded for the rules test first (:func:`_record`), then compared,
    and released either way.
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
        assert _mismatches(s_proj, sec_proj, t_offset=month, exempt=SPLICE_EXEMPT,
                           atol=0.0) == []
    finally:
        _release(sec, key, collect=True)


# ---------------------------------------------------------------------------
# T3 -- future new business


@pytest.mark.parametrize(
    "s_point, k",
    [_case(case, CORE_FUTURES, _case_id("future", case[0], -case[1]))
     for case in FUTURES])
def test_future_new_business_is_the_s_projection_k_months_on(spliced, splice_records,
                                                             s_point, k):
    """Commencing k months after the valuation date, the point is S's projection k on.

    SEC rows ``k ..`` are S rows ``0 ..``, ending together at the stop rule, in
    ``result_cf`` and in every column of ``result_pols`` S's has, and every cell of S's but
    :data:`FUTURE_EXEMPT` agrees at every argument S cached inside its own frame, moved
    ``k`` later, to 1e-9 relative with no absolute floor.  The row is read in the splice's
    one read of its table (:data:`SEC_REFS`) and compared with S read with its CMT shift at
    0 (:data:`LATER_REFS`): bought after the valuation date, the contract has seen no
    change in the CMT on the block's path, and S's point is the same contract on it.  An S
    cell this model lacked would fail it.  Before the annuity date every column of
    ``result_cf`` and ``result_pols`` is an exact zero, and the contracts arrive in month
    ``k`` as new business, the annuities commencing then.

    The last assertions are R1 and D4's base rule made testable.  After every report, no
    decrement rate keyed by month has been evaluated at a month before the annuity date,
    and neither age reader has been read below an issue age.  A survival recursion based at
    ``t == 0`` rather than at ``t_entry()``, which carries each life at 1 through the months
    before, or a rate that evaluates its table before asking whether the month is in cover,
    still gives the right numbers.  This is the only test that sees the first, and the
    guard test sees the second too.

    The pre-issue rows are asserted present before they are asserted zero: a frame that
    opened at the annuity date would have none, its zeros would hold of nothing, and the
    comparisons with S, which start there, would not see it.  The row is swept and
    recorded for the rules test first (:func:`_record`), and released after, with the S
    point it was compared with, swept here.
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
        assert _mismatches(s_proj, sec_proj, t_offset=-k, exempt=FUTURE_EXEMPT,
                           atol=0.0) == []
        for report, frame in (("result_cf", df), ("result_pols", pols)):
            assert list(frame.index[:k]) == list(range(k)), report
            assert (frame.loc[:k - 1] == 0.0).all().all(), report
        assert sec_proj.pols_new_biz(k) == sec_proj.policy_count() == 1.0
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
    and on a point commencing at ``t = 0`` the two clocks coincide and hide it from T1 too.
    The splice's rows are points in payment at every month T2 names, the variants among
    them, and points commencing later, and each was swept first:

    * R1: no cell holds a negative argument.  modelx evaluates one without complaint, and
      a compiled cache raises ``IndexError`` below 0 (USLIB-SEC-PLAN.md F4).  A policy
      month turned into ``t`` by subtracting ``duration_mth_init()`` (R1a) goes negative on
      a point in payment past it, and so does a survival or commutation recursion based at
      ``t == 0`` but read a month back from it.  The policy-clock keys are held to it too:
      the trim of variant 26, whose first instalment repays the premium, reads the payments
      to date at ``max(0, n_R - 12/m)``, where ``SPIA_US_S`` reads ``G(-2)``.
    * R1's look-back stops at ``t_entry()``: no cell evaluated at a month from
      ``t_entry()`` on read a month before it.  On a point commencing later a recursion
      based at ``t == 0`` reads the months before, where each life is carried at 1 and
      nothing is commuted, so no number shows it and no argument goes negative.
    * R1a's ranges: every argument of a cell keyed by the policy clock or an age is one the
      contract has (:func:`_contract`): the payments to date, the schedule, the income by
      policy year, the utilization and the surrender charge from the annuity date to the
      stop rule, and the two age readers from each life's issue age to its age in the last
      month, below omega.  A schedule read at a policy year before the annuity date, an age
      table read past omega, or a cache sized from the contract read beyond it would wrap
      round in a compiled model.
    * R2's look-ahead: no cell evaluated at month ``t`` read a cell keyed by a month beyond
      ``t + 1``, as modelx's dependency graph records each cached call's precedents.
      ``SPIA_US_S``'s commuted value and withdrawal read the schedule at every month of the
      certain period still to come, as ``annuity_pp_sched(s)``; here they read it by
      policy month, which no frame index ahead of ``t`` keys.  SPIA admits no look-ahead.

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
    assert not found["early"], f"read before the annuity date from the books: " \
                               f"{found['early'][:10]}"
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
      stays shallow, which is why D3 is asserted on its own.  So do the two static
      schedules, the payments to date and the income by policy year, because each is based
      at the valuation date, the first by a loop over the policy months before it and the
      second by one over the policy years: the point in its 58th policy year reads its
      income without recursing back to the annuity date.  A backward recursion over the
      frame, through ``t + 1``, keeps every step within the look-ahead but opens a chain as
      long as the frame, which a compiled model would run on the C stack (F7), and fails
      here.
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


def _extended(column):
    """An edit of a mortality table that adds the ages from 18 to 39, below its first.

    The shipped tables start at 40, the shipped points' youngest age.  The added rows are
    geometric in age and apart by sex, a distinct value at every ``(age, sex)``, so that a
    read at the wrong age or sex changes a number.
    """
    def edit(df):
        rows = []
        for sex, scale in (("M", 1.0), ("F", 0.97)):
            first = float(df.loc[(df["age"] == 40) & (df["sex"] == sex), column].iloc[0])
            rows += [{"age": age, "sex": sex, column: first * 0.94 ** (40 - age) * scale,
                      "provenance": "[std] extended below 40 for a depth test"}
                     for age in range(CONTRACT_MIN_AGE, 40)]
        return pd.concat([pd.DataFrame(rows), df], ignore_index=True)
    return edit


def _longest_cover():
    """The two points at the contract's longest cover from issue, and the tables they need.

    S point 6's twin, the single-life cash refund, on the table basis at the youngest
    lifetime issue age, :data:`CONTRACT_MIN_AGE`: 1,224 months to the age stop, through
    which the survival chain and the payments to date both run.  Once commencing at the
    valuation date and once 120 months on, the longest frame, 1,344 months.
    """
    row = _committed().loc[[6]].assign(primary_age=CONTRACT_MIN_AGE, mort_basis="table",
                                       death_mth_1=NAN)
    rows = pd.concat([row, row.assign(duration_mth=-120, policy_id="IA-000006-F120")])
    rows.index = pd.Index([1, 2], name="point_id")
    edits = {"mort_table.csv": _extended("mort_rate"),
             "improvement_scale.csv": _extended("improvement_rate")}
    return rows, edits


# modelx warns as its stack trace starts and stops, which is all the test does with it.
@pytest.mark.filterwarnings("ignore:call stack trace:UserWarning")
def test_the_deepest_cold_call_runs_one_cell_a_month(tmp_path):
    """A cold ``net_cf`` in the last month runs one cell a month back to ``t_entry`` (D5).

    On a model just read, nothing is cached, so ``net_cf(proj_len() - 1)`` runs each chain
    from the end of the frame back to the first month on the books, survival on the table
    basis, the commutation fraction on every point and the payments to date on a cash
    refund, and modelx's stack trace counts how deep.  Each chain may be one cell a month
    and no more, plus at most :data:`CHAIN_OVERHEAD` cells above and below it: on the
    anchor's twins, 696 months, through survival on the table basis and through the
    commutation fraction on the scenario basis; on the cash refund in payment 13 months,
    whose refund reads the payments to date back to the valuation date's policy month, and
    no further; and at the contract's longest cover
    from issue (:func:`_longest_cover`), 1,224 months from issue age 18, commencing at the
    valuation date and 120 months on.  No number shows the depth, and a compiled model runs
    the chain on the C stack, so a chain of two cells a month, which gives the same
    numbers, needs twice the stack (F7), and so does a payments-to-date chain run back to
    the annuity date.  A future point's chain stops at ``t_entry()``, so the longest frame,
    1,344 months, runs no deeper than the cover it holds.
    """
    rows, edits = _longest_cover()
    refund = _label(_committed(), "derived", 6, 13)
    reads = [("committed", model_path(SEC), [1, 8, refund]),
             ("longest", _sec_inputs(tmp_path, rows, edits), [1, 2])]
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
    assert not found, found
    assert depths["longest", 1] > 1224 - CHAIN_OVERHEAD, (
        f"the longest cover ran {depths['longest', 1]} cells deep: the depth test did not "
        f"reach it")


# ---------------------------------------------------------------------------
# T4 -- the count algebra
#
# BEF_DECR == BEF_NB + pols_new_biz, at every t of every point, is a convention
# (test_new_business_joins_the_count_before_decrements), and so is the new business
# entering once at its policy_count; neither is repeated here.


def test_the_count_is_on_the_books_from_the_annuity_date_to_the_stop_rule(sec_model):
    """The count weights every month from the annuity date to the stop rule, undecremented.

    SPIA_US_S weights every flow by its constant ``pols_if_init`` and carries mortality in
    each life's survival, and so does this model: under independence the two lives'
    probabilities are the whole survival state, which a count weighted by survival could
    not carry.  So on every committed point ``pols_if_at(t, "BEF_DECR")``, the count
    weighting month ``t``, is ``policy_count()`` at every ``t`` from ``t_entry()`` to the
    last row and 0 before, and ``"BEF_NB"`` opens at ``t_entry()`` at ``pols_if_init()``,
    the count in payment at the valuation date, 0 on a point not yet in payment.  The count
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
        moved = [p.pols_if_at(t, decr) - p.pols_if_at(t + 1, nb) for t in range(entry, n)]
        assert moved == [0.0] * (n - 1 - entry) + [count], point_id
        pols = p.result_pols()
        assert list(pols.columns) == RESULT_POLS, point_id
        assert pols.index.name == "t" and list(pols.index) == list(range(n)), point_id
    _refused(lambda: projection(sec_model, point_keys(sec_model)[0]).pols_if_at(
        0, "BEF_MAT"), "invalid timing")


def test_pols_if_is_the_closing_obligation_measure(sec_model):
    """``pols_if(t)`` is the notes' ``IF(t)`` on the count on the books, not ``BEF_DECR``.

    On every committed point and at every ``t`` of its frame, ``pols_if(t)`` is exactly
    ``pols_if_at(t, "BEF_DECR") * max(C(t), l_alive(t + 1))``: the contracts with an
    obligation still open at the end of month ``t``, measured at its close, ``l_alive`` 0 on
    certain_only, whose expense stops with its last instalment.  It is a closing measure,
    and differs from the count that weights the row even where S's own does: on the anchor
    cell's twin, point 8, ``pols_if(0)`` is 0.99999986, on the cash refund in its death
    month, point 17, 0, and on the anchor in its last month, point 21, 3.41e-06, each
    against a count of 1.  That is why the registry marks the model ``closing_pols_if``
    and the convention that ``pols_if`` is ``BEF_DECR`` skips it (D5).
    """
    decr = _code(sec_model.Projection, "BEF_DECR")
    table = sec_model.Data.model_point_table()
    for key, point_id in zip(point_keys(sec_model), table.index):
        p = projection(sec_model, key)
        for t in range(p.proj_len()):
            alive = 0.0 if p.is_certain_only() else p.lives_if_last(t + 1)
            expected = p.pols_if_at(t, decr) * max(p.certain_floor(t), alive)
            assert p.pols_if(t) == expected, (point_id, t)
    for kind, s_point, month, value in (("twin", 8, 0, 0.99999986),
                                        ("derived", 6, 13, 0.0),
                                        ("derived", 8, 695, 3.41e-06)):
        p = _row(sec_model, kind, s_point, month)
        assert p.pols_if(0) == pytest.approx(value, rel=1e-3, abs=1e-12), (s_point, month)
        assert p.pols_if_at(0, decr) == p.policy_count() == 1.0
        assert p.pols_if(0) < p.pols_if_at(0, decr)


def test_result_pols_is_s_report_with_the_new_business_beside_it(sec_model, s_model):
    """``result_pols()`` is S's, column for column, with ``pols_new_biz`` beside it (D5).

    T1 skips the report as a whole, because its frame has a column S's lacks (the spec's
    exempt), so it is compared here, on every twin, at offset 0.  Its columns are
    :data:`RESULT_POLS`: ``pols_if`` first, as ``BasicTerm_SE`` sets its counts out, where
    ``SPIA_US_S`` has it last, then ``pols_new_biz``, the annuities commencing in the month,
    then S's other seven in S's order.  Every column S's report has agrees, to 1e-9, frames
    ending together, and ``pols_new_biz`` holds the count in the month the annuity
    commences and 0 in every other.  Counts and survival carry no inflation, so the shipped
    assumptions serve.
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
        assert frame_mismatches(theirs, mine) == [], point_id
        assert list(mine["pols_new_biz"]) == [
            p.policy_count() if t == 0 else 0.0 for t in mine.index], point_id


# What T4 multiplies policy_count by: not a whole number, because a count of contracts need
# not be one, so that a flow which read the count as whole contracts would not follow it.
COUNT_FACTOR = 2.5


def test_scaling_the_count_scales_every_flow_and_no_per_contract_value(tmp_path):
    """``policy_count`` is a weight: 2.5 times the count, 2.5 times every flow, the same per
    contract.

    The committed table, and a copy with every count multiplied by :data:`COUNT_FACTOR`,
    are each read with :data:`SWITCHED_ON` set before either computes anything: the
    assumptions that ship at zero switched on at the splice's values, so that every flow
    is nonzero on some point, the commutations and their surrender charge among them,
    which the shipped zero utilization makes 0 on every point.  On every point
    ``result_cf`` and the counts of ``result_pols`` are 2.5 times the committed table's,
    element by element, to 1e-12 relative: a scaled count is a computed float, which may
    come back from the CSV within two ulps (``sec_support``'s module docstring).  So is
    every other cell of :data:`COUNTED`, at every argument the sweep of the committed
    table's point cached: the surrender charge, which no report shows, and the counts at
    each timing among them.  ``result_pols``'s seven probabilities and factors are the
    committed table's exactly.  And every cell outside :data:`COUNTED` (the instalment, the
    refund, the withdrawal per contract, the payments to date, each life's survival, the
    opening state, the rates, both clocks, the flags) agrees at every argument that sweep
    cached.  So a flow that dropped the count, or read it as whole contracts, which a table
    of counts of 1 hides from every comparison with S, fails here.  Each point is released
    once compared.
    """
    table = _committed()
    base = _read(_sec_inputs(tmp_path / "base", table), "counted", SWITCHED_ON)
    scaled = _read(_sec_inputs(tmp_path / "scaled", table.assign(
        policy_count=COUNT_FACTOR * table["policy_count"])), "scaled", SWITCHED_ON)
    counted = sorted(COUNTED - set(REPORTS))
    nonzero = set()
    try:
        for key, scaled_key in zip(point_keys(base), point_keys(scaled)):
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
            for name in counted:
                for args in _cached_args(one.cells[name]):
                    want = COUNT_FACTOR * one.cells[name](*args)
                    got = many.cells[name](*args)
                    assert abs(got - want) <= 1e-12 * abs(want), (key, name, args, got,
                                                                  want)
                    if want != 0.0:
                        nonzero.add(name)
            assert _mismatches(one, many, exempt=TWIN_EXEMPT_DEFAULT | COUNTED) == []
            _release(base, key)
            _release(scaled, scaled_key)
    finally:
        scaled.close()
        base.close()
    assert nonzero == set(counted), f"0 on every point: {sorted(set(counted) - nonzero)}"


# ---------------------------------------------------------------------------
# T5 -- validation
#
# Each malformed table is the committed one with one fault, and only the rule under test
# refuses it.  The checks run over the whole table as it is read, in Data, and the message
# names the file it read and the column or every point at fault.  A blank cell reads as
# NaN, and so does a text cell once the checks coerce the column to numbers, so each is
# refused as a count, a duration, a probability, a fraction, a change in the CMT or a month
# of death that is not a number.  The repeated point_id holds another contract under the
# same label, as a bad extract would, so that the check must look at the labels and not at
# whole rows.  The point_ids are the committed table's: 16, the anchor in payment 14
# months, its joint annuitant dead; 17, the single-life cash refund in its death month, 13;
# 18, the certain period over at 120, the joint annuitant dead; 19, both lives dead at 30,
# inside the certain period; 20, the commuting point on its second anniversary, 24, on the
# table basis; 21, the anchor in its last month on the table basis, the primary dead; 22,
# the anchor commencing 13 months on; and the twins 7, a single-life installment refund on
# the table basis, 8, joint on the table basis, and 9, commuting.  One fault is refused by
# two rules by its nature: a commutation fraction at the annuity date breaks the at-issue
# check, which comes first, and the commutation check's ``duration_mth`` 13 or more too,
# which subsumes the at-issue check's fraction leg; the message names the first.  Each
# check over a window of contract months is refused just inside each end of its window,
# its first month as well as its last, and read just outside it (the edges test), where an
# off-by-one would let a row through (USLIB-SEC-PLAN.md §5.2, T5, precised at M10).  The
# at-issue check's window is every month to the annuity date: refused at policy month
# -120, the horizon, and at 0, and read at 1, a contract a month in payment.  The scenario
# check turns at a life's month of death: refused with the life dead in that month, at
# whose start it is alive, and alive in the month after, and read the other way round,
# the committed rows 17 and 16.  The commutation check's window is a contract's first
# policy year in payment: refused at policy months 1 and 12, the month of the first
# withdrawal, and read at 13, the first it reduces.  Two ends have no month just outside
# that another check does not refuse: -121, past the horizon, and a fraction at 0, at
# issue.  No check here has a tolerance: the opening state is two probabilities, a
# fraction and a change in a rate, each held exactly, and no amount carried to the cent.
# Each case is read by a model of its own, its file named by a Reference set before the
# model computes anything (the malformed fixture), so a {file} in a message is the case's
# own filename.

_LIFE = ("{file}: lives_if_init_{n} must be a probability, 0 to 1; it is not at point_id "
         "[{p}]")
_FRACTION = ("{file}: commute_frac_cum_init must be a number, 0 or more and below 1; it is "
             "not at point_id [{p}]")
_SINGLE = ("{file}: lives_if_init_2 must be 0 on a single-life contract, which covers no "
           "second life; it is not at point_id [{p}]")
_AT_ISSUE = ("{file}: {c} must hold its value at issue on a contract not yet in force, "
             "duration_mth 0 or less: each covered life alive, no commutation taken and no "
             "change in the CMT; it does not at point_id [{p}]")
_CMT = ("{file}: cmt10_shift_init must be a number, the change in the 10-year CMT since "
        "the annuity date; it is not at point_id [{p}]")
_DEATH = ("{file}: death_mth_{n} must be blank or a whole number of months, a policy "
          "month; it is not at point_id [{p}]")
_SCENARIO = ("{file}: on the scenario basis lives_if_init_{n} must be 1 while the life "
             "survives to the valuation date, death_mth_{n} blank, negative or "
             "duration_mth or later, and 0 once it has died; it is not at point_id [{p}]")
_COMMUTED = ("{file}: commute_frac_cum_init must be 0 unless a commutation could have been "
             "taken before the valuation date: the right held, the issue state allowing "
             "it, a certain period, and duration_mth 13 or more; it is not at point_id "
             "[{p}]")


def _life(n, p):
    return _LIFE.format(file="{file}", n=n, p=p)


MALFORMED = [
    ("a negative count", _set("policy_count", [16], -0.1),
     "{file}: policy_count must be a number, zero or more; it is not at point_id [16]"),
    ("a count written as text", _set("policy_count", [19], "abc"),
     "{file}: policy_count must be a number, zero or more; it is not at point_id [19]"),
    ("a blank count", _set("policy_count", [20], NAN),
     "{file}: policy_count must be a number, zero or more; it is not at point_id [20]"),
    ("an infinite count", _set("policy_count", [21], float("inf")),
     "{file}: policy_count must be a number, zero or more; it is not at point_id [21]"),
    ("two bad counts", _both(_set("policy_count", [16], -1.0),
                             _set("policy_count", [22], "x")),
     "{file}: policy_count must be a number, zero or more; it is not at point_id "
     "[16, 22]"),
    ("a fractional duration", _set("duration_mth", [18], 120.5),
     "{file}: duration_mth must be a whole number of months; it is not at point_id [18]"),
    ("a blank duration", _set("duration_mth", [18], NAN),
     "{file}: duration_mth must be a whole number of months; it is not at point_id [18]"),
    ("a duration written as text", _set("duration_mth", [18], "ten"),
     "{file}: duration_mth must be a whole number of months; it is not at point_id [18]"),
    ("commencing beyond the horizon", _set("duration_mth", [22], -121),
     "{file}: duration_mth must be -120 or more, a policy issued at most 120 months after "
     "the valuation date; it is not at point_id [22]"),
    *[(f"no {column} column", _drop(column), f"{{file}} has no {column} column")
      for column in ("policy_count", "duration_mth", *STATE)],
    ("a repeated point_id",
     lambda t: pd.concat([t, t.loc[[16]].assign(policy_id="IA-900099")]),
     "{file}: point_id [16] appears more than once"),
    ("life 1 above 1", _set("lives_if_init_1", [20], 1.5), _life(1, 20)),
    ("life 2 below 0", _set("lives_if_init_2", [20], -0.1), _life(2, 20)),
    ("life 1 blank", _set("lives_if_init_1", [21], NAN), _life(1, 21)),
    ("life 1 written as text", _set("lives_if_init_1", [20], "alive"), _life(1, 20)),
    ("life 2 written as text", _set("lives_if_init_2", [21], "0.000004x"), _life(2, 21)),
    ("a negative fraction", _set("commute_frac_cum_init", [20], -0.1),
     _FRACTION.format(file="{file}", p=20)),
    ("a fraction of 1", _set("commute_frac_cum_init", [20], 1.0),
     _FRACTION.format(file="{file}", p=20)),
    ("a blank fraction", _set("commute_frac_cum_init", [20], NAN),
     _FRACTION.format(file="{file}", p=20)),
    ("a fraction written as text", _set("commute_frac_cum_init", [20], "half"),
     _FRACTION.format(file="{file}", p=20)),
    ("a CMT change written as text", _set("cmt10_shift_init", [20], "up"),
     _CMT.format(file="{file}", p=20)),
    ("a blank CMT change", _set("cmt10_shift_init", [21], NAN),
     _CMT.format(file="{file}", p=21)),
    ("an infinite CMT change", _set("cmt10_shift_init", [16], float("inf")),
     _CMT.format(file="{file}", p=16)),
    ("a second life on a single-life contract",
     _moved(7, 24, lives_if_init_1=0.9, lives_if_init_2=0.5),
     _SINGLE.format(file="{file}", p=7)),
    ("a life not alive on future business", _set("lives_if_init_1", [22], 0.9),
     _AT_ISSUE.format(file="{file}", c="lives_if_init_1", p=22)),
    ("a joint life not alive at the annuity date", _set("lives_if_init_2", [8], 0.5),
     _AT_ISSUE.format(file="{file}", c="lives_if_init_2", p=8)),
    ("a fraction at the annuity date", _set("commute_frac_cum_init", [9], 0.1),
     _AT_ISSUE.format(file="{file}", c="commute_frac_cum_init", p=9)),
    ("a CMT change on future business", _set("cmt10_shift_init", [22], 0.005),
     _AT_ISSUE.format(file="{file}", c="cmt10_shift_init", p=22)),
    ("a CMT change at the annuity date", _set("cmt10_shift_init", [9], -0.005),
     _AT_ISSUE.format(file="{file}", c="cmt10_shift_init", p=9)),
    ("a life not alive on business commencing at the horizon",
     _moved(22, -120, lives_if_init_1=0.9),
     _AT_ISSUE.format(file="{file}", c="lives_if_init_1", p=22)),
    ("a death month written as text", _set("death_mth_1", [16], "x"),
     _DEATH.format(file="{file}", n=1, p=16)),
    ("a fractional death month", _set("death_mth_2", [16], 13.5),
     _DEATH.format(file="{file}", n=2, p=16)),
    ("a death month between -1 and 0", _set("death_mth_1", [16], -0.5),
     _DEATH.format(file="{file}", n=1, p=16)),
    ("a death month written as text on the table basis", _set("death_mth_1", [20], "x"),
     _DEATH.format(file="{file}", n=1, p=20)),
    ("a scenario life alive after its death", _set("lives_if_init_2", [16], 1.0),
     _SCENARIO.format(file="{file}", n=2, p=16)),
    ("a scenario life dead in its death month", _set("lives_if_init_1", [17], 0.0),
     _SCENARIO.format(file="{file}", n=1, p=17)),
    ("a scenario life dead before its death", _set("lives_if_init_1", [16], 0.0),
     _SCENARIO.format(file="{file}", n=1, p=16)),
    ("a scenario life as a probability", _set("lives_if_init_1", [18], 0.5),
     _SCENARIO.format(file="{file}", n=1, p=18)),
    ("a negative death month on a dead life", _both(_set("death_mth_2", [16], -1),
                                                     _set("lives_if_init_2", [16], 0.0)),
     _SCENARIO.format(file="{file}", n=2, p=16)),
    ("a fraction without the right", _set("commute_frac_cum_init", [18], 0.1),
     _COMMUTED.format(file="{file}", p=18)),
    ("a fraction with no certain period",
     _both(_set("commutation_enabled", [16], True),
           _set("commute_frac_cum_init", [16], 0.1)),
     _COMMUTED.format(file="{file}", p=16)),
    ("a fraction with a certain period of 0 months",
     _both(_set("certain_months", [20], 0), _set("commute_frac_cum_init", [20], 0.1)),
     _COMMUTED.format(file="{file}", p=20)),
    ("a fraction in the month of the first withdrawal",
     _moved(20, 12, commute_frac_cum_init=0.1), _COMMUTED.format(file="{file}", p=20)),
    ("a fraction in the first month in payment",
     _moved(20, 1, commute_frac_cum_init=0.1), _COMMUTED.format(file="{file}", p=20)),
    ("a fraction where the state bars it",
     _both(_set("commute_frac_cum_init", [20], 0.1),
           _set("issue_state_excludes_withdrawal", [20], True)),
     _COMMUTED.format(file="{file}", p=20)),
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


def _year(year, value):
    """An edit of the surrender-charge scale that writes ``value`` for policy year
    ``year``, the column made ``object`` first, as :func:`_set` makes it."""
    def edit(df):
        years = df["policy_year"].astype(object)
        return df.assign(policy_year=years.where(df["policy_year"] != year, value))
    return edit


# The malformed surrender-charge scales, as (case, the edit of surr_charge_table.csv, the
# message): what Data.surr_charge_scale refuses, naming the file.  The scale's years run
# from 2 to 10 as shipped.  SPIA_US_S took int() of the raw years for the scale's first and
# last, so that a year written as text raised Python's own message, or turned every lookup
# into a miss; here the years are read by value once, and the extents and the rates come
# from that one checked column.
_RUN = ("surr_charge_table.csv: the policy years must run from {} to 10 without a gap or a "
        "repeat, from 1 on, each with a rate")
SCALES = [
    ("a year written as text", _year(3, "3a"),
     "surr_charge_table.csv: a policy year must be a whole number; ['3a'] is not"),
    ("a fractional year", _year(3, 3.5),
     "surr_charge_table.csv: a policy year must be a whole number; [3.5] is not"),
    ("a blank year", _year(3, NAN),
     "surr_charge_table.csv: a policy year must be a whole number; [nan] is not"),
    ("a gap", lambda df: df[df["policy_year"] != 5], _RUN.format(2)),
    ("a repeated year", lambda df: pd.concat([df, df[df["policy_year"] == 5]]),
     _RUN.format(2)),
    ("a year below 1", lambda df: pd.concat([df.iloc[:1].assign(policy_year=0), df]),
     _RUN.format(0)),
    ("a blank rate", lambda df: df.assign(surr_charge_rate=df["surr_charge_rate"].where(
        df["policy_year"] != 5, NAN)), _RUN.format(2)),
    ("no year at all", lambda df: df.iloc[:0], "surr_charge_table.csv has no policy year"),
]


@pytest.mark.parametrize("case, edit, message", SCALES, ids=[c[0] for c in SCALES])
def test_a_malformed_surrender_charge_scale_is_refused_naming_the_file(tmp_path, case,
                                                                        edit, message):
    """``Data.surr_charge_scale()`` refuses the scale, and a projection meets the refusal.

    The scale is ``SPIA_US_S``'s file, read in place by both models, so each case is read
    by a model of its own from a copy of the inputs with the one fault.  The commuting
    point in payment 24 months reads the surrender charge's rate in every month of its
    frame, whether or not it withdraws, so its ``result_cf()`` meets the same refusal
    before it computes a number.
    """
    model = _read(_sec_inputs(tmp_path, _committed(), {"surr_charge_table.csv": edit}),
                  "scale")
    try:
        _refused(model.Data.surr_charge_scale, message)
        _refused(_point(model, _label(_committed(), "derived", 9, 24)).result_cf, message)
    finally:
        model.close()


def test_a_surrender_charge_scale_written_as_floats_is_read_by_value(sec_model, tmp_path):
    """Policy years written ``2.0`` to ``10.0`` are the years 2 to 10, read by value.

    One blank or one ``1.0`` in a column makes pandas read it as float64.  The checked
    scale is indexed by the whole years, and the commuting point in payment 24 months
    projects exactly what the committed model projects, its rate of policy year 3 the
    scale's 7% at every month of the year.
    """
    model = _read(_sec_inputs(tmp_path, _committed(), {"surr_charge_table.csv": lambda df:
                  df.assign(policy_year=df["policy_year"].astype(float))}), "floats")
    try:
        scale = model.Data.surr_charge_scale()
        assert model.Data.surr_charge_table().index.dtype == float
        assert scale.index.dtype == "int64" and list(scale.index) == list(range(2, 11))
        label = _label(_committed(), "derived", 9, 24)
        p = _point(model, label)
        assert (p.policy_year(0), p.surr_charge_rate(3)) == (3, 0.07)
        assert frame_mismatches(_point(sec_model, label).result_cf(), p.result_cf(),
                                rtol=0, atol=0) == []
    finally:
        model.close()


# The points a rule of the product refuses, each in proj_len() and each by name, with the
# reason by form: a point at or past the stop rule, and a contract that owes nothing after
# the valuation date because its certain period is over and no life-contingent payment is
# left, every covered life having died or the form being certain_only.  The table reads in
# each: the rule needs the certain period, which an installment refund derives in
# Projection.  Each window is refused at its first month and at its last, the frame's last
# month, and read just outside it (the edges test), USLIB-SEC-PLAN.md §5.2's T5 (precised
# at M10): on the 10-year certain points, a certain_only contract at 120 and 659 and one
# with both lives dead at 120 and 695, each read at 119; on the anchor, every life dead on
# a form with no certain period at 1 and 695, the first month in payment and the last,
# where the at-issue check refuses 0.  The stop rule is refused at 696 and read at 695,
# the committed row 21; past each frame's last month the stop rule refuses first.  As
# (case, point_id, edit, message).
_OWED = "point_id {p}: duration_mth {d}: no payment is owed after the valuation date: "
REFUSED = [
    ("past the stop rule", 21, _set("duration_mth", [21], 696),
     "point_id 21: duration_mth 696 is at or past the end of the projection, policy "
     "month 696"),
    ("a single life dead, no certain period", 17, _moved(17, 14, lives_if_init_1=0.0),
     _OWED.format(p=17, d=14) + "every covered life has died, and the form has no certain "
     "period"),
    ("both lives dead, no certain period", 21, _set("lives_if_init_2", [21], 0.0),
     _OWED.format(p=21, d=695) + "every covered life has died, and the form has no "
     "certain period"),
    ("both lives dead after the certain period", 19, _set("duration_mth", [19], 120),
     _OWED.format(p=19, d=120) + "every covered life has died, and the certain period "
     "ended at policy month 120"),
    ("certain_only after its certain period", 15, _moved(15, 120, lives_if_init_1=0.9),
     _OWED.format(p=15, d=120) + "a certain_only contract pays nothing after its certain "
     "period, which ended at policy month 120"),
    ("certain_only in the last month of its frame", 15,
     _moved(15, 659, lives_if_init_1=0.9),
     _OWED.format(p=15, d=659) + "a certain_only contract pays nothing after its certain "
     "period, which ended at policy month 120"),
    ("both lives dead in the last month of the frame", 19, _set("duration_mth", [19], 695),
     _OWED.format(p=19, d=695) + "every covered life has died, and the certain period "
     "ended at policy month 120"),
    ("both lives dead in the first month in payment, no certain period", 21,
     _moved(21, 1, lives_if_init_1=0.0, lives_if_init_2=0.0),
     _OWED.format(p=21, d=1) + "every covered life has died, and the form has no certain "
     "period"),
]


@pytest.mark.parametrize("case, point_id, edit, message", REFUSED,
                         ids=[c[0] for c in REFUSED])
def test_a_point_owing_nothing_is_refused_by_proj_len(tmp_path, case, point_id, edit,
                                                      message):
    """A point with no frame left is read, and refused by ``proj_len()`` by name (D6, T5).

    The rules need ``stop_mth()`` and the certain period, which an installment refund
    derives from the schedule in ``Projection``, so they are rules of the product, not of
    the table: the table reads, and the point is refused where its frame is defined, on its
    first projection, rather than projecting nothing.  An in-force extract should carry
    neither kind of point: a contract that owes nothing has made its last payment, or its
    refund, before the valuation date, as ``Term_US_SEC``'s point past its cover has
    ended.  The other points of the same table project.
    """
    model = _read_edited(tmp_path, edit, "refused")
    try:
        assert len(model.Data.model_point_table()) == len(_committed())
        _refused(_point(model, point_id).result_cf, message)
        assert len(_point(model, 16 if point_id != 16 else 18).result_cf()) > 0
    finally:
        model.close()


def test_the_future_horizon_is_a_reference_that_bounds_future_business(tmp_path):
    """``Data.future_horizon_mth`` refuses an annuity commencing later, and 0 refuses all.

    The committed table's one future point commences 13 months on.  It reads at the shipped
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
                    assert (late.proj_len(), late.pols_new_biz(13)) == (709, 1.0)
                    assert late.result_cf()["annuity_payments"].iloc[13] > 0.0
            else:
                _refused(model.Data.model_point_table, refusal)
        finally:
            model.close()


_WHOLE = ("duration_mth", "certain_months", "frequency", "annuity_year", "primary_age",
          "policy_count", "lives_if_init_1", "lives_if_init_2", "commute_frac_cum_init",
          "cmt10_shift_init")


def test_the_edges_of_the_in_force_interface_are_accepted(sec_model, tmp_path):
    """A zero count, whole numbers in any type, the horizon and the checks' edges are read.

    A count of 0 is a point that projects zeros.  The integer columns written as floats,
    as one blank or one ``1.0`` in a column makes pandas read it, are read by value, and
    every other point projects exactly what the committed table projects: ``12.0`` is the
    int the policy clock counts in.  An annuity commencing 120 months after the valuation
    date, the shipped ``future_horizon_mth``, is the last one the table admits, with a frame
    of 816 months, 696 to the stop rule after 120 before it.  A death month written as -1,
    on a life that survives, is a survivor, as ``SPIA_US_S`` reads one, and changes no
    number.  A commutation fraction is read at policy month 13, the first month a
    withdrawal taken at 12 reduces, and a change in the CMT since the annuity date may be
    a fall: 25 basis points, on the same point, lower its discount rate to 3.75%.  The
    committed table holds the other edges: one life
    already dead on a joint contract (16), a scenario life in its death month, alive at
    its start (17), and both lives dead inside a certain period (19).

    Each window of contract months is read just outside it (USLIB-SEC-PLAN.md §5.2, T5,
    precised at M10), by copies of committed rows appended under ids of their own, each
    reading and projecting its whole frame in finite numbers: the commuting point at
    policy month 1, a month past the at-issue check's window, its lives below 1 and the
    CMT up 10 basis points; the certain_only twin at 119 and the joint point with both
    lives dead at 119, each a month before ``proj_len()``'s window of a contract owing
    nothing, each paying its last certain instalment at ``t = 0`` and nothing after; and the
    anchor in payment 14 months whose joint annuitant died in policy month 0, the first
    death month that is not a survivor's, which projects the anchor's committed frame.

    And a fraction past the residual floor, 0.85 on the commuting point on its second
    anniversary, read at a utilization of 1: the month is eligible and the owner asks for
    the whole commuted value, more than the $5,000 minimum, but no withdrawal can leave the
    remaining instalments at $100 once 81% of each is commuted, so none is taken, and the
    instalment paid is 15% of the scheduled one, 79.57 of 530.45.
    """
    committed = _committed()
    zero = _label(committed, "derived", 1, 14)
    later = _label(committed, "future", 8, -13)
    survivor = _label(committed, "derived", 5, 120)
    commuting = _label(committed, "derived", 9, 24)
    dead = _label(committed, "derived", 13, 30)
    copies = {101: (commuting, {"duration_mth": 1.0, "cmt10_shift_init": 0.001}),
              102: (15, {"duration_mth": 119.0, "lives_if_init_1": 0.9}),
              103: (dead, {"duration_mth": 119.0}),
              104: (zero, {"death_mth_2": 0.0})}

    def edit(table):
        table = table.assign(**{c: table[c].astype(float) for c in _WHOLE})
        rows = [table.loc[[row]].assign(**changes).set_axis([label])
                for label, (row, changes) in copies.items()]
        table = pd.concat([table, *rows]).rename_axis("point_id")
        table = _set("policy_count", [zero], 0.0)(table)
        table = _set("duration_mth", [later], -120.0)(table)
        table = _set("death_mth_1", [survivor], -1.0)(table)
        return _moved(commuting, 13, commute_frac_cum_init=0.1,
                      cmt10_shift_init=-0.0025)(table)

    model = _read_edited(tmp_path, edit)
    try:
        read = model.Data.model_point_table()
        assert all(read[c].dtype == float for c in _WHOLE)
        assert len(read) == len(committed) + len(copies)
        df = _point(model, zero).result_cf()
        assert len(df) == 682 and (df == 0.0).all().all()
        for point_id in committed.index.drop([zero, later, commuting]):
            assert frame_mismatches(_point(sec_model, point_id).result_cf(),
                                    _point(model, point_id).result_cf(), rtol=0,
                                    atol=0) == [], point_id
        for label in copies:
            p = _point(model, label)
            frame = p.result_cf()
            assert len(frame) == p.proj_len() > 0, label
            assert all(math.isfinite(v) for v in frame.to_numpy().ravel()), label
        first = _point(model, 101)
        assert (first.duration_mth(0), first.cmt10_shift_init()) == (1, 0.001)
        assert first.lives_if_init(1) < 1.0 and first.lives_if_init(2) < 1.0
        for label in (102, 103):
            p = _point(model, label)
            paid = [p.annuity_payments(t) for t in range(p.proj_len())]
            assert p.duration_mth(0) == 119 and paid[0] == p.annuity_pp_sched(0) > 0.0
            assert paid[1:] == [0.0] * (len(paid) - 1), label
        assert _point(model, 103).lives_if_last(0) == 0.0
        widowed = _point(model, 104)
        assert (widowed.death_mth(2), widowed.lives_if_init(2)) == (0, 0.0)
        assert frame_mismatches(_point(sec_model, zero).result_cf(), widowed.result_cf(),
                                rtol=0, atol=0) == []
        p = _point(model, survivor)
        assert p.duration_mth(0) == 120 and type(p.duration_mth(0)) is int
        assert p.death_mth(1) == -1 and p.lives_if(p.proj_len(), 1) == 1.0
        late = _point(model, later)
        assert (late.t_entry(), late.proj_len(), late.pols_new_biz(120)) == (120, 816, 1.0)
        assert late.result_cf().loc[:119].eq(0.0).all().all()
        moved = _point(model, commuting)
        assert (moved.duration_mth(0), moved.commute_frac_cum(0)) == (13, 0.1)
        assert moved.cmt10_shift_init() == -0.0025
        assert moved.commute_disc_rate(0) == (
            moved.commute_disc_rate_base + -0.0025 + moved.cmt10_shift)
        assert moved.commute_disc_rate(0) == pytest.approx(0.0375, rel=1e-12)
    finally:
        model.close()
    floor = _read_edited(tmp_path / "floor",
                         _set("commute_frac_cum_init", [commuting], 0.85), "floor",
                         {"commute_util_base": 1.0})
    try:
        p = _point(floor, commuting)
        assert p.commute_elig(0) and p.commuted_value(0) > p.commute_min_amount
        assert p.commute_util_rate(p.policy_year(0)) == 1.0
        assert 1.0 - p.commute_min_payment / p.annuity_pp_sched(1) < 0.85
        assert p.commute_amount(0) == 0.0 and p.commutations(0) == 0.0
        assert p.annuity_pp_sched(0) == pytest.approx(530.45, abs=0.005)
        assert p.annuity_payments(0) == pytest.approx(0.15 * p.annuity_pp_sched(0),
                                                      rel=1e-12)
        assert p.commute_frac_cum(1) == 0.85
    finally:
        floor.close()


# Every state SPIA_US_S reaches, restated in force at its month, is an opening state Data's
# checks and proj_len()'s accept, but a state the product refuses by name: a check
# exercised only on the rows the tests above choose could refuse a state S reaches
# elsewhere (D6).  SPIA_US_S keeps a contract on its books after it owes nothing, a
# certain_only contract after its certain period or one whose every covered life has died
# after it, and projects it as zeros to its stop rule, where proj_len() refuses it by
# name (REFUSED): the every-state test sets each such state aside and shows it refused.


def _every_state_months(sp):
    """The months S point ``sp``, projected, is restated at by the every-state test.

    By default the edges of each window a check of ``Data`` or ``proj_len()`` reads a
    month against (USLIB-SEC-PLAN.md §5.2, T5, precised at M10): policy month 1, the first
    past the at-issue check's window; 12 and 13, either side of the commutation check's;
    each scenario life's month of death and the month after it, where its status turns;
    the month before each covered life's survival reaches 0, and the month it does; the
    certain period's last month and the first after it, where a contract with nothing
    life-contingent left starts to owe nothing; and the frame's last month, before the stop
    rule.  With ``USLIB_SEC_FULL=1``, every month of its frame.
    """
    n = sp.proj_len()
    if SEC_FULL:
        return list(range(1, n))
    certain = sp.certain_mths_eff()
    months = {1, 12, 13, certain - 1, certain, n - 1}
    for life in _lives(sp):
        if sp.mort_basis() == "scenario":
            months |= {sp.death_mth(life), sp.death_mth(life) + 1}
        zero = next((d for d in range(n) if sp.lives_if(d, life) == 0.0), None)
        if zero is not None:
            months |= {zero - 1, zero}
    return sorted(d for d in months if 1 <= d < n)


def _owing(sp, d):
    """Why S point ``sp`` restated at month ``d`` owes nothing after it, as ``proj_len()``
    says it, or None where it owes a payment.

    As ``proj_len()`` reads a contract in payment: its certain period over, and the form
    certain_only or every covered life dead, ``SPIA_US_S``'s survival exactly 0.
    """
    certain = sp.certain_mths_eff()
    if d < certain:
        return None
    if sp.form() == "certain_only":
        return (f"a certain_only contract pays nothing after its certain period, which "
                f"ended at policy month {certain}")
    if any(sp.lives_if(d, life) > 0.0 for life in _lives(sp)):
        return None
    if certain > 0:
        return (f"every covered life has died, and the certain period ended at policy "
                f"month {certain}")
    return "every covered life has died, and the form has no certain period"


def _every_state_table(root, s, edits):
    """The states ``s``'s points reach, restated in force: ``(folder, rows, owing)``.

    Each month of :func:`_every_state_months` of each point of ``s``, an S model already
    swept, a derived row of a table the generator builds beside every point's twin
    (``sec_support.build_sec_table``), written into ``folder`` under ``root`` with
    ``edits`` beside it, the inputs S read.  ``rows`` is the table's length, and ``owing``
    holds ``{(S point, month): why}`` for each state owing nothing (:func:`_owing`).
    """
    states, owing = [], {}
    for key, point_id in zip(point_keys(s), s.Data.model_point_table().index):
        sp = projection(s, key)
        for d in _every_state_months(sp):
            states.append((point_id, d))
            why = _owing(sp, d)
            if why is not None:
                owing[(point_id, d)] = why
    spec = dataclasses.replace(SPEC, derived=tuple(states), future=())
    table, companions = build_sec_table(spec, s)
    assert companions == {}
    folder = temp_inputs(root, model_path(SEC), model_points=table,
                         model_point_file=TABLE, edits=edits)
    return folder, len(table), owing


def _departures(model, rows, owing):
    """Where ``Data`` and ``proj_len()`` depart from what the every-state test expects.

    ``model`` holds a table of ``rows`` rows (:func:`_every_state_table`), which ``Data``
    must read.  Each row's ``proj_len()`` must give a frame, but a state of ``owing``,
    ``{(S point, month): why}``, which it must refuse, naming the row, its month and why.
    Each row is released once asked, the collector run every 500.  Returns each departure,
    the line that names it.
    """
    try:
        table = model.Data.model_point_table()
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
    """Every state ``SPIA_US_S`` reaches is a valid opening state, but one owing nothing.

    ``Data``'s checks and ``proj_len()``'s hold an opening state to what a contract in
    payment can be, so they must accept each state the S model reaches (D6).  So every S
    point, swept, is restated in force by the generator at the edges of its windows, or
    with ``USLIB_SEC_FULL=1`` at every month of its frame (:func:`_every_state_months`),
    into one table beside the twins: ``Data`` reads it, and every row's ``proj_len()``
    gives a frame.  But for the states set aside, which ``SPIA_US_S`` keeps on its books,
    projecting zeros to its stop rule, and ``proj_len()`` refuses, each by name, its row,
    its month and why it owes nothing (:func:`_owing`): the single-life cash refunds and
    life annuities after their scenario deaths, points 6, 10, 11 and 14; the joint point
    with both lives dead after its certain period, 13; and the certain_only points after
    theirs, 15 and, on the splice, variant 22 (USLIB-SEC-PLAN.md §5.2, T5, precised at
    M10).

    It runs under each set of inputs on which the states S reaches differ (§5.2, T5,
    precised at M9).  S's shipped References, on S's own table: the committed S model,
    whose points withdraw nothing, at a utilization of 0, and see no change in the CMT.
    And the splice's References, improvement scale and variants (:data:`SPLICED_REFS`):
    the commuting points withdraw from policy month 12 on, commuting up to 87.5% of each
    certain instalment, and every state carries the CMT's change.  On the module's other
    inputs S's states are among these: under :data:`LATER_REFS` the splice's but for the
    CMT's change, 0 as under the shipped References, which ``Data`` holds only to be a
    number in payment; under the simple discount, exactly the splice's.
    """
    sets = (("shipped", _every_state_table(tmp_path / "shipped", s_model, None), {},
             {6, 10, 11, 13, 14, 15}),
            ("spliced", _every_state_table(tmp_path / "spliced", spliced[0], SPLICED_EDITS),
             SEC_REFS, {6, 10, 11, 13, 14, 15, 22}))
    for name, (folder, rows, owing), refs, owing_points in sets:
        assert {p for p, _ in owing} == owing_points, (name, sorted(owing)[:5])
        model = _read(folder, "every", refs)
        try:
            found = _departures(model, rows, owing)
        finally:
            model.close()
        assert not found, f"{name}: {len(found)} departures, first: {found[:5]}"


# ---------------------------------------------------------------------------
# T6 -- regeneration


def test_the_committed_sec_table_is_what_s_generates(s_model):
    """``model_point_table_sec.csv`` is what SPIA_US_S and its table generate today.

    Every row and column, the text cells and the three opening-state columns included: an
    edit to an S row the table copies or derives from, or to an S formula a row's state is
    read from, fails here until ``python tools/gen_sec_points.py SPIA_US_SEC`` regenerates
    it, in the same commit.  Text and integers compare exactly, and a float by its value, to
    1e-12, because the text the writer picks for a computed float depends on the platform's
    parser (§5.2).
    """
    assert check_generated(SEC, s_model=s_model) == []


# ---------------------------------------------------------------------------
# The product's own facts


def test_the_worked_example_carries_over_at_the_valuation_date(sec_model, s_model):
    """S's worked example and its traces, restated in payment, continue S's months.

    At the shipped assumptions, on the four rows derived from the worked example's points:

    * the anchor in payment 14 months, its joint annuitant dead since the end of policy
      month 13, pays the reduced 343.33 from ``t = 0`` and 353.63 from its next COLA
      anniversary, policy month 24, at ``t = 10``: the COLA continues after the reduction;
    * the cash refund in its death month, policy month 13, pays the refund at ``t = 0``:
      ``100,000 - G(13) = 93,485.00``, ``G(13) = 12 x 500.00 + 515.00``, the payments to
      date summed on the policy clock, and no instalment, the death being decremented at the
      end of the month;
    * the life-certain contract whose certain period ends at the valuation date, policy
      month 120, its joint annuitant dead since 13, pays the deferred reduction from
      ``t = 0``, 447.97 = 671.96 x 2/3;
    * the life-certain contract with both lives dead in its certain period pays the full
      instalment through the floor alone, 530.45 at ``t = 0`` rising with the COLA to 652.39
      in its last certain month, policy month 119, ``t = 89``, and nothing from ``t = 90``,
      its ``pols_if`` 1 then 0.

    Each row is S's point from its month on in every cell but those expense inflation moves
    (:func:`_continues_s`).
    """
    anchor = _row(sec_model, "derived", 1, 14)
    assert anchor.annuity_payments(0) == pytest.approx(343.33, abs=0.005)
    assert anchor.annuity_payments(9) == anchor.annuity_payments(0)
    assert anchor.annuity_payments(10) == pytest.approx(353.63, abs=0.005)
    assert anchor.annuity_pp_sched(10) == pytest.approx(
        anchor.annuity_pp_sched(9) * 1.03, rel=1e-12)
    refund = _row(sec_model, "derived", 6, 13)
    assert refund.cum_annuity_pp(13) == 12 * 500.0 + 515.0 == 6515.0
    assert refund.claims(0, _code(refund, "REFUND")) == pytest.approx(93485.0, abs=1e-9)
    assert refund.annuity_payments(0) == 0.0
    assert refund.result_cf()["claims"].iloc[1:].eq(0.0).all()
    deferred = _row(sec_model, "derived", 5, 120)
    assert deferred.certain_floor(0) == 0.0 and deferred.payment_factor(0) == pytest.approx(
        2 / 3, rel=1e-9)
    assert deferred.annuity_pp_sched(0) == pytest.approx(671.96, abs=0.005)
    assert deferred.annuity_payments(0) == pytest.approx(447.97, abs=0.005)
    floor = _row(sec_model, "derived", 13, 30)
    assert floor.lives_if_last(0) == 0.0
    paid = [floor.annuity_payments(t) for t in range(floor.proj_len())]
    assert paid[:90] == [floor.annuity_pp_sched(t) for t in range(90)]
    assert paid[0] == pytest.approx(530.45, abs=0.005)
    assert paid[89] == pytest.approx(652.39, abs=0.005)
    assert paid[90:] == [0.0] * (len(paid) - 90)
    assert (floor.pols_if(89), floor.pols_if(90)) == (1.0, 0.0)
    for (s_point, month), p in (((1, 14), anchor), ((6, 13), refund), ((5, 120), deferred),
                                ((13, 30), floor)):
        assert _continues_s(_point(s_model, s_point), p, month) == [], (s_point, month)


def test_survival_opens_per_life_at_the_valuation_date(sec_model, s_model):
    """Each life's survival opens at ``t_entry()`` at its column, and runs on from there.

    On every committed point ``lives_if(t, life)`` is 0 before the contract is on the books
    and ``lives_if_init(life)`` at ``t_entry()``, for each life separately: 1 for each
    covered life at the annuity date, and on a row restated from S at its month ``d``,
    S's ``lives_if(d, life)``, read back from the CSV to 1e-12.  The scenario rows hold 1 or
    0 exactly; the anchor in its last month holds a primary dead at omega, exactly 0, and a
    living joint annuitant; and on the commuting point at its second anniversary both lives
    are fractions, each moved by its own sex's and age's rates, so that a life's
    probability read in the other's place would show.  On a row with both lives dead in a
    certain period nothing is life-contingent, and the floor pays.

    Then each life runs on from its opening value as S's does, for every row in payment on
    either basis: the table basis multiplies it by each month's survival from
    ``t_entry()``, the scenario basis steps on the policy clock.  Every derived row is S's
    point from its month on in every cell but those inflation moves (:func:`_continues_s`).
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
            if p.is_scenario():
                assert p.lives_if_init(life) in (0.0, 1.0), point_id
        assert _continues_s(s, p, month) == [], point_id
    last = _row(sec_model, "derived", 8, 695)
    assert last.lives_if_init(1) == 0.0 < last.lives_if_init(2)
    two = _row(sec_model, "derived", 9, 24)
    assert 0.0 < two.lives_if_init(1) < two.lives_if_init(2) < 1.0
    assert (two.lives_if(1, 1) / two.lives_if(0, 1)
            != two.lives_if(1, 2) / two.lives_if(0, 2))
    dead = _row(sec_model, "derived", 13, 30)
    assert dead.lives_if_init(1) == dead.lives_if_init(2) == 0.0
    assert dead.payment_factor_life(0) == 0.0 and dead.payment_factor(0) == 1.0


def test_payments_to_date_stay_on_the_annuity_date_clock(sec_model, s_model, spliced):
    """``cum_annuity_pp(k)`` is S's ``G(k)`` at every policy time point, summed to the
    valuation date by one loop, and the refund period does not move with it.

    The payments to date are deterministic, the as-if-alive schedule from the annuity date,
    so they need no opening column, and stay keyed by ``k``, months from the annuity date
    (§7.9).  On every row derived from S, ``G(k)`` is S's at every ``k`` from 0 to
    ``stop_mth()``, bit for bit: the loop that sums the instalments before the valuation
    date's policy month adds them in S's order.  On a model just read, the cash refund in
    payment 13 months reads ``G`` from 13 on and never below: the loop serves the
    payments to date, so the first refund of a contract long in payment does not recurse as
    deep as it is old, and each refund after it recurses one month back.  And the
    installment refund's period, ``n_R = 200`` on S point 7, is the same in payment at its
    last certain month as commencing 13 months on, and is S's.
    """
    table = sec_model.Data.model_point_table()
    for point_id in table.index[table["row_kind"] == "derived"]:
        p, s = _point(sec_model, point_id), _source(s_model, table, point_id)
        mine = [p.cum_annuity_pp(k) for k in range(p.stop_mth() + 1)]
        assert mine == [s.cum_annuity_pp(k) for k in range(p.stop_mth() + 1)], point_id
    fresh = _read(model_path(SEC), "g_keys")
    try:
        refund = _row(fresh, "derived", 6, 13)
        refund.result_cf()
        keys = sorted(refund.cells["cum_annuity_pp"].keys())
        assert keys[0] == 13 and keys == list(range(13, keys[-1] + 1)), keys[:5]
        assert keys[-1] == refund.stop_mth() - 1
    finally:
        fresh.close()
    s, sec = spliced[0], spliced[1]
    for case in (("derived", 7, 199), ("future", 7, -13)):
        key = _row_key(sec, *case)
        try:
            assert projection(sec, key).certain_mths_refund() == 200, case
        finally:
            _release(sec, key, collect=True)
    assert _point(s, 7).certain_mths_refund() == 200


def test_the_commutation_fraction_carries_over_in_force(spliced, tmp_path):
    """The commutation fraction taken before the valuation date reduces what follows.

    On the splice's inputs, utilization 0.5 and the CMT 50 basis points up since the annuity
    date, the change the row carries as already seen: the commuting point restated at policy
    month
    13, the month after its first withdrawal, opens with ``commute_frac_cum_init`` 0.5, S's
    ``commute_frac_cum(13)``, and pays 257.50 at ``t = 0``, half the 515.00 scheduled and
    S's month 13.  Its next withdrawal, at policy month 24, ``t = 11``, is 11,735.74, half
    of a commuted value already halved, and the rest of its certain period pays 17,115.93.
    From policy month 120, ``t = 107``, the life tail pays in full, 640.04 on the splice's
    inputs, since the fraction reduces certain instalments only.  The same row with the
    fraction zeroed, read from a copy, pays 515.00 at ``t = 0``, withdraws 23,471.48 at
    policy month 24 and pays 21,808.98 over the rest of the certain period: the figures of a
    contract that never commuted.  The column is the only state that says what the owner
    has taken, so it is what makes the difference.
    """
    s, sec = spliced[0], spliced[1]
    key = _row_key(sec, "derived", 9, 13)
    try:
        p = projection(sec, key)
        rest = sum(p.annuity_payments(t) for t in range(107))
        opened = (p.commute_frac_cum_init(), p.annuity_payments(0), p.commute_amount(11),
                  rest, p.annuity_payments(107))
        row = sec.Data.model_point_table().loc[[_label(sec.Data.model_point_table(),
                                                       "derived", 9, 13)]]
    finally:
        _release(sec, key, collect=True)
    s9 = _point(s, 9)
    assert opened[0] == 0.5 == s9.commute_frac_cum(13)
    assert opened[1] == pytest.approx(257.50, abs=1e-9) == s9.annuity_payments(13)
    assert opened[2] == pytest.approx(11735.74, abs=0.005)
    assert opened[3] == pytest.approx(17115.93, abs=0.005)
    assert opened[4] == pytest.approx(640.04, abs=0.005)
    zeroed = _read(_sec_inputs(tmp_path, row.assign(commute_frac_cum_init=0.0),
                               SPLICED_EDITS), "zeroed", SEC_REFS)
    try:
        z = _point(zeroed, row.index[0])
        assert z.annuity_payments(0) == pytest.approx(515.00, abs=1e-9)
        assert z.commute_amount(11) == pytest.approx(23471.48, abs=0.005)
        assert sum(z.annuity_payments(t) for t in range(107)) == pytest.approx(
            21808.98, abs=0.005)
        assert z.annuity_payments(107) == pytest.approx(opened[4], rel=1e-12)
    finally:
        zeroed.close()


def test_the_residual_floor_caps_a_withdrawal_in_force(tmp_path):
    """The largest withdrawal the floor allows leaves every certain instalment at $100.

    The commuting point on its second anniversary, opened with half its certain instalments
    already commuted, is read at a utilization of 1, set before the model computes
    anything: the owner asks for the whole commuted value, but no withdrawal may leave a
    remaining guaranteed payment below $100 [S1], so the residual floor caps it, at the
    fraction that leaves the smallest remaining certain instalment, B(3)/12 = 530.45 from
    policy month 25, at exactly $100.  That is the cap the splice's utilization of 0.5
    never binds with a withdrawal taken, and the cap reads the instalments still to come on
    the policy clock, from the valuation date's policy month: read from the annuity date,
    the smallest would be policy year 1's 500.00, and the fraction another.  From ``t = 1``
    each certain instalment is paid at the capped fraction, policy month 25's at $100.00,
    and the next withdrawal, a year on, is below the $5,000 minimum, so none is taken.
    """
    commuting = _label(_committed(), "derived", 9, 24)
    model = _read_edited(tmp_path, _set("commute_frac_cum_init", [commuting], 0.5), "cap",
                         {"commute_util_base": 1.0})
    try:
        p = _point(model, commuting)
        assert p.commute_elig(0) and p.commute_frac_cum(0) == 0.5
        asked, taken = p.commuted_value(0), p.commute_amount(0)
        assert p.commute_min_amount <= taken < asked, (taken, asked)
        floor = 1.0 - p.commute_min_payment / p.annuity_pp_sched(1)
        assert p.commute_frac_cum(1) == pytest.approx(floor, rel=1e-12)
        assert p.annuity_pp_sched(1) == pytest.approx(530.45, abs=0.005)
        assert p.annuity_pp_paid(1) == pytest.approx(100.0, rel=1e-12)
        assert min(p.annuity_pp_paid(t) for t in range(1, 96)) == pytest.approx(
            100.0, rel=1e-12)
        assert p.commute_elig(12) and p.commute_amount(12) == 0.0
        assert (p.policy_year(0), p.surr_charge_rate(3)) == (3, 0.07)
        assert p.commutations(0) == pytest.approx(taken * (1.0 - 0.07), rel=1e-12)
    finally:
        model.close()


def test_the_simple_discount_continues_s(tmp_path):
    """Under the simple discount convention, the commuting rows continue S's months too.

    ``commute_disc_convention`` ships ``"compound"``, the convention the splice runs, so a
    point restated in payment is compared under the simple one here: S point 9 restated at
    13 and 24, and the COLA installment refund that commutes at 13, read from small copies
    of their own, with the splice's References and the simple convention set on each before
    it computes, SEC's CMT shift at 0 as in the splice's read of its table
    (:data:`SEC_REFS`).  Each is S's point from its month on in every cell, the
    commuted value and the withdrawals among them, which here differ from the compound
    convention's.
    """
    s_table = _s_table_with_variants().loc[[9, 18]]
    simple = {"commute_disc_convention": "simple"}
    s = _read(temp_inputs(tmp_path / "s", model_path(TWIN), model_points=s_table,
                          edits=SPLICED_EDITS), "s_simple", {**SPLICED_REFS, **simple})
    try:
        for key in point_keys(s):
            _sweep(projection(s, key))
        spec = dataclasses.replace(SPEC, derived=((9, 13), (9, 24), (18, 13)), future=())
        table, _ = build_sec_table(spec, s)
        sec = _read(temp_inputs(tmp_path / "sec", model_path(SEC), model_points=table,
                                model_point_file=TABLE, edits=SPLICED_EDITS),
                    "sec_simple", {**SEC_REFS, **simple})
        try:
            for case in (("derived", 9, 13), ("derived", 9, 24), ("derived", 18, 13)):
                p, s_proj = _row(sec, *case), _point(s, case[1])
                assert p.is_disc_compound() is False
                _sweep(p)
                for report in REPORTS:
                    assert frame_mismatches(s_proj.cells[report](), p.cells[report](),
                                            t_offset=case[2], atol=0.0) == [], (case,
                                                                                report)
                assert _mismatches(s_proj, p, t_offset=case[2], exempt=SPLICE_EXEMPT,
                                   atol=0.0) == [], case
            compound = 23471.48               # the compound value at 24, from the splice
            assert _row(sec, "derived", 9, 24).commuted_value(0) != pytest.approx(
                compound, abs=0.005)
        finally:
            sec.close()
    finally:
        s.close()


def test_each_contract_reads_the_cmt_change_since_its_own_annuity_date(s_model, tmp_path):
    """Each contract reads the CMT's change since its own annuity date, on one path.

    The commutation discount rate moves one for one with the 10-year CMT's change since the
    annuity date, and every contract of a block reads that change on one path of the CMT,
    which every point shares (D7, as precised at M11).  Contracts bought at different dates
    have seen different changes by the valuation date, which ``cmt10_shift_init`` carries,
    and the Reference ``cmt10_shift`` is the change made at the valuation date, which every
    contract on the books there sees and a contract commencing later, bought after it,
    does not.  One table holds three contracts on S point 9's terms: the commuting point in
    payment 24 months, its column set to 0.005, the CMT 50 basis points up since its
    annuity date; its twin, commencing at the valuation date; and the same contract
    commencing 13 months on, a row added to the table.  Read with the Reference at 0, the
    point in payment discounts at 4.5%, its commuted value at ``t = 0`` 46,942.96, S point
    9's at its month 24 with S's shift at 0.005, against 47,837.36 at 4.0%, and the other
    two at 4.0%, each commuted value at the first withdrawal month, policy month 12,
    52,062.79, S point 9's on S's shipped 4.0%.  Read with the Reference at 0.005, the CMT
    50 basis points up again at the valuation date, the point in payment discounts at 5.0%,
    its commuted value S's with S's shift at 0.010, the twin at 4.5%, S's at 0.005, and the
    contract commencing later at 4.0% still, its commuted value unmoved.  A Reference read
    as the change since each contract's own annuity date would move the last too, and one
    ignored would leave the twin at 4.0%.
    """
    committed = _committed()
    in_payment = _label(committed, "derived", 9, 24)
    twin = _label(committed, "twin", 9, 0)
    later = int(committed.index.max()) + 1

    def edit(table):
        table = _set("cmt10_shift_init", [in_payment], 0.005)(table)
        row = table.loc[[twin]].assign(duration_mth=-13, row_kind="future", source_mth=-13,
                                       policy_id="IA-000009-F13")
        row.index = pd.Index([later], name="point_id")
        return pd.concat([table, row])

    folder = _sec_inputs(tmp_path, edit(committed))
    flat = _read(folder, "cmt_flat")
    step = _read(folder, "cmt_step", {"cmt10_shift": 0.005})
    up = _read(model_path(TWIN), "s_cmt_up", {"cmt10_shift": 0.005})
    up_twice = _read(model_path(TWIN), "s_cmt_up_twice", {"cmt10_shift": 0.01})
    try:
        rates, values = {}, {}
        for name, model in (("flat", flat), ("step", step)):
            p, t9, f = (_point(model, i) for i in (in_payment, twin, later))
            assert (p.cmt10_shift_init(), t9.cmt10_shift_init(), f.cmt10_shift_init(),
                    f.t_entry(), f.duration_mth(25)) == (0.005, 0.0, 0.0, 13, 12), name
            rates[name] = (p.commute_disc_rate(0), t9.commute_disc_rate(12),
                           f.commute_disc_rate(25))
            values[name] = (p.commuted_value(0), t9.commuted_value(12),
                            f.commuted_value(25))
        assert rates["flat"] == pytest.approx((0.045, 0.04, 0.04), rel=1e-12)
        assert rates["step"] == pytest.approx((0.05, 0.045, 0.04), rel=1e-12)
        s9, s9_up, s9_up_twice = _point(s_model, 9), _point(up, 9), _point(up_twice, 9)
        assert values["flat"] == (s9_up.commuted_value(24), s9.commuted_value(12),
                                  s9.commuted_value(12))
        assert values["step"][0] == pytest.approx(s9_up_twice.commuted_value(24),
                                                  rel=1e-12)
        assert values["step"][1:] == (s9_up.commuted_value(12), s9.commuted_value(12))
        assert values["flat"][0] == pytest.approx(46942.96, abs=0.005)
        assert s9.commuted_value(24) == pytest.approx(47837.36, abs=0.005)
        assert values["flat"][2] == pytest.approx(52062.79, abs=0.005)
    finally:
        for model in (up_twice, up, step, flat):
            model.close()


def test_mortality_improvement_is_calendar_dated_on_the_policy_clock(sec_model, s_model,
                                                                    spliced):
    """Improvement reads each contract's own calendar years, whatever the valuation date.

    The exponent is ``calendar_year(t) - mort_table_year``, and ``calendar_year(t)`` is
    ``annuity_year() + duration(t)``, on the policy clock (D7): a contract in payment at
    the valuation date reads the improvement of the calendar years it reaches, from its own
    annuity year, so nothing is re-based onto the valuation clock and the splice need not
    neutralize it.  On the commuting point in payment 24 months, ``calendar_year(0)`` is
    2028, and its rates at every ``t`` and for both lives are S point 9's at month
    ``24 + t``, with no input re-based; on the anchor commencing 13 months on,
    ``calendar_year(13)``, its annuity month, is 2026, its rates S point 8's ``13`` months
    earlier.  A rated contract commencing in 2020 reads its own calendar years too, and its
    rating's cap reaches 1 at attained age 117, before omega (variant 20 on the splice's
    inputs).
    """
    commuting, s9 = _row(sec_model, "derived", 9, 24), _point(s_model, 9)
    assert (commuting.annuity_year(), commuting.calendar_year(0)) == (2026, 2028)
    for t in range(commuting.proj_len()):
        for life in (1, 2):
            assert commuting.mort_rate(t, life) == s9.mort_rate(24 + t, life), (t, life)
            assert commuting.improvement_rate(t, life) == s9.improvement_rate(24 + t, life)
    later, s8 = _row(sec_model, "future", 8, -13), _point(s_model, 8)
    assert (later.duration_mth(13), later.calendar_year(13)) == (0, 2026)
    for t in range(s8.proj_len()):
        for life in (1, 2):
            assert later.mort_rate(13 + t, life) == s8.mort_rate(t, life), (t, life)
    sec = spliced[1]
    key = _row_key(sec, "derived", 20, 72)
    try:
        rated = projection(sec, key)
        assert (rated.annuity_year(), rated.calendar_year(0)) == (2020, 2026)
        capped = [t for t in range(rated.proj_len()) if rated.mort_rate(t, 1) == 1.0]
        assert capped and rated.age(capped[0], 1) == 117 < rated.omega_age
    finally:
        _release(sec, key, collect=True)


# The cap on mortality
#
# SPIA_US_S caps the annual rate twice, q_be = min(AE * q_base, 1.0) and
# q_rated = min(theta * q_be, 1.0), so that its monthly rate stays real at any rating, and
# this model caps both as S does, each with its bound second (USLIB-SEC-PLAN.md §5.1,
# step 6).  The first binds at the limiting age, where the base rate is 1 and AE 1.084,
# and the second below it, on a rated life.  The rows on which one binds inside the frame,
# each a row of the committed table or of the splice's core, as (row_kind, S point,
# source_mth): the life it binds on and the first month it binds in, on the row's clock.
CAPPED = {
    ("twin", 8, 0): (1, 660),       # the anchor's primary at the limiting age: the A/E cap
    ("derived", 8, 695): (1, 0),    # the same in its last month, the primary dead by then
    ("derived", 20, 72): (1, 552),  # rated 1.25: theta * q_be passes 1 at attained age 117
    ("derived", 23, 12): (1, 288),  # a certain period past the age stop: omega at month 300
}


def test_a_capped_annual_mortality_is_the_float_1_and_kills_every_life(sec_model, s_model,
                                                                       spliced):
    """Where a cap binds, the annual and the monthly rates are the float 1.0, and survival
    is exactly 0 after it.

    On each row of :data:`CAPPED`, from the month a cap first binds to the end of the
    frame, ``mort_rate`` and ``mort_rate_mth`` are ``(float, 1.0)``, the type asserted with
    the value, since ``1 == 1.0`` would let an int cap through; every life alive at the
    start of that month dies in it, so that its survival is exactly 0 at every time point
    after; and every report is float64 and finite.  Survival where the caps bind is near
    1e-10, 6e-09 on the anchor's primary at the limiting age and 2e-10 on the rated life at
    117, where an absolute floor of 1e-9 would hide any difference, so T2 and T3 compare
    every row with S to 1e-9 relative with no floor, and this test the twin, which T1
    compares at the conventions' floor.  The rows in payment are the splice's, read with
    its References (:data:`SEC_REFS`), but for the anchor in its last month, the committed
    table's, as is the twin.
    """
    found = []
    for case, (life, first) in CAPPED.items():
        splice = case not in (("twin", 8, 0), ("derived", 8, 695))
        sec = spliced[1] if splice else sec_model
        key = _row_key(sec, *case)
        try:
            p = projection(sec, key)
            n = p.proj_len()
            capped = [t for t in range(n) if p.mort_rate(t, life) == 1.0]
            assert capped == list(range(first, n)), (case, capped[:3])
            found += [(case, t, rate.name) for t in capped
                      for rate in (p.cells["mort_rate"], p.cells["mort_rate_mth"])
                      if (type(rate(t, life)), rate(t, life)) != (float, 1.0)]
            if first > 0:
                assert p.lives_if(first, life) > 0.0, case
            assert [p.lives_if(t, life) for t in range(first + 1, n + 1)] == [0.0] * (
                n - first), case
            for frame in (p.result_cf(), p.result_pols()):
                assert (frame.dtypes == "float64").all(), (case, frame.dtypes)
                assert (frame.abs() < float("inf")).all().all(), case
        finally:
            if splice:
                _release(sec, key, collect=True)
    assert not found, f"a capped rate that is not the float 1.0: {found[:5]}"
    assert _mismatches(_point(s_model, 8), _row(sec_model, "twin", 8, 0),
                       exempt=TWIN_EXEMPT_DEFAULT | SPEC.exempt, atol=0.0) == []


def _nan_rate(t, life):
    """NaN, what a blank rate carries: the formula a test puts in place of a cell's.

    It names no global of this module: modelx runs a formula in the model's namespace.
    """
    return float("nan")


def _nan_factor():
    """NaN, what a blank factor carries: the formula a test puts in place of a cell's."""
    return float("nan")


# The two caps a NaN must pass through, as (the cap, the cell whose formula returns NaN in
# a model read for the test, that formula).  mort_rate_base feeds the A/E cap and, through
# it, the rating cap; rating_factor feeds the rating cap alone.  Bound first, either cap
# would turn the NaN into 1.0: every life dead in the first month, every flow finite.
NAN_CAPS = [
    ("q_be = min(AE * q_base, 1.0)", "mort_rate_base", _nan_rate),
    ("q_rated = min(theta * q_be, 1.0)", "rating_factor", _nan_factor),
]


@pytest.mark.parametrize("cap, cell, formula", NAN_CAPS,
                         ids=["the AE cap", "the rating cap"])
def test_a_nan_that_reaches_a_cap_stays_nan(cap, cell, formula):
    """A NaN that reaches either cap on mortality stays NaN, and is not read as 1.

    ``min`` keeps its first argument unless a later one compares smaller, in modelx and
    compiled alike, and no comparison with NaN holds, so with its bound first a cap would
    turn a NaN into 1.0: a blank rate read as certain death, every flow finite.  Each cap
    is written with its bound second, as ``SPIA_US_S`` writes it.  To send one a NaN, the
    formula of the cell that feeds it (:data:`NAN_CAPS`) is replaced by one returning NaN,
    in a model read for the test, which modelx allows.  On the anchor's twin, the primary's
    ``mort_rate`` and ``mort_rate_mth`` must then be the float NaN, in the first month and
    the last.
    """
    model = mx.read_model(model_path(SEC), name=_name("nan"))
    try:
        model.Projection.cells[cell].formula = formula
        p = _row(model, "twin", 8, 0)
        lost = [f"{name}({t}, 1) = {value!r}"
                for name in ("mort_rate", "mort_rate_mth") for t in (0, p.proj_len() - 1)
                for value in [p.cells[name](t, 1)]
                if not (type(value) is float and math.isnan(value))]
        assert not lost, f"{cap} loses a NaN {cell}(): {lost}"
    finally:
        model.close()


def test_expense_inflation_runs_on_the_valuation_clock(sec_model, s_model):
    """Maintenance is in valuation-date dollars, for every point alike (D7).

    At the shipped 2.5%, the factor at ``t`` is ``1.025 ** (t // 12)`` on every point,
    whatever its duration: S's annual steps, moved onto the valuation clock.  So the
    life-certain contract in payment 120 months, valued on its anniversary, pays S's month
    ``120 + t`` expenses deflated by ``1.025 ** 10``, the inflation S had already applied
    since the annuity date; the anchor in payment 14 months, valued off its anniversary,
    pays S's month ``14 + t`` expenses divided by 1.025 or by 1.025 squared, as its policy
    years and the valuation years step apart; and the anchor commencing 13 months on pays
    S's month ``t - 13`` maintenance times 1.025 or 1.025 squared, valuation years against
    policy years.  This is the only test that sees inflation run on the valuation clock: the
    splice sets the rate to 0, and on a point commencing at ``t = 0`` the clocks agree.
    """
    assert sec_model.Projection.inflation_rate == INFLATION
    for key in point_keys(sec_model):
        p = projection(sec_model, key)
        for t in range(p.proj_len()):
            assert p.inflation_factor(t) == (1.0 + INFLATION) ** (t // 12), (key, t)
    p, s = _row(sec_model, "derived", 5, 120), _point(s_model, 5)
    for t in range(p.proj_len()):
        assert p.expenses(t) == pytest.approx(
            s.expenses(120 + t) / (1.0 + INFLATION) ** 10, rel=1e-12), t
    ratios = set()
    p, s = _row(sec_model, "derived", 1, 14), _point(s_model, 1)
    for t in range(p.proj_len()):
        if p.expenses(t):
            ratio = s.expenses(14 + t) / p.expenses(t)
            ratios.add(1 if ratio == pytest.approx(1.025, rel=1e-12) else
                       2 if ratio == pytest.approx(1.025 ** 2, rel=1e-12) else ratio)
    assert ratios == {1, 2}
    ratios = set()
    p, s = _row(sec_model, "future", 8, -13), _point(s_model, 8)
    for t in range(13, p.proj_len()):
        ratio = p.expenses(t) / s.expenses(t - 13)
        ratios.add(1 if ratio == pytest.approx(1.025, rel=1e-12) else
                   2 if ratio == pytest.approx(1.025 ** 2, rel=1e-12) else ratio)
    assert ratios == {1, 2}


def test_annuities_commencing_later_carry_no_premium_and_no_acquisition(sec_model):
    """The single premium is a pricing input, for an annuity commencing later as for one in
    payment, and new business brings no acquisition cost.

    ``SPIA_US_S`` keeps the single premium out of the projection, and SEC keeps that (§7.9):
    ``result_cf()`` has S's columns and no premium income.  ``expenses(t)`` is the
    maintenance charge alone, ``expense_maint / 12 * inflation_factor(t) * pols_if(t)``, in
    every month of every point, the month an annuity commences included, where
    ``Term_US_SEC`` charges acquisition per policy issued.  And the premium is read by
    nothing but the refund forms' guarantee: the refund, the installment-refund search and
    its trim, and ``premium_net_pp``, which nothing reads.
    """
    columns = ["pols_if", "annuity_payments", "claims", "commutations", "expenses",
               "liability_cf", "net_cf"]
    readers = set()
    for key in point_keys(sec_model):
        p = projection(sec_model, key)
        assert list(p.result_cf().columns) == columns
        for t in range(p.proj_len()):
            assert p.expenses(t) == (
                p.expense_maint / 12.0 * p.inflation_factor(t) * p.pols_if(t)), (key, t)
            assert p.liability_cf(t) == (p.annuity_payments(t) + p.claims(t)
                                         + p.commutations(t) + p.expenses(t)), (key, t)
        for name, cells in p.cells.items():
            for args in _cached_args(cells):
                if any(node.obj.name == "premium_pp" for node in cells.preds(*args)):
                    readers.add(name)
    assert readers <= {"claim_pp", "certain_mths_refund", "annuity_pp", "premium_net_pp"}
    assert {"claim_pp", "certain_mths_refund"} <= readers
    later = _row(sec_model, "future", 8, -13)
    assert later.pols_new_biz(13) == 1.0 and later.premium_pp() == 100000.0
    maintenance = later.expense_maint / 12.0 * later.inflation_factor(13)
    assert 0.0 < later.expenses(13) <= maintenance
    assert later.liability_cf(13) < later.annuity_pp_sched(13) + later.expenses(13) + 1e-9


def test_annuities_commence_and_there_is_no_lapse(sec_model):
    """``pols_new_biz`` exists, meaning annuities commencing; a lapse still does not (§7.9).

    ``SPIA_US_S``'s tests forbid ``pols_new_biz`` on a SPIA, together with the lapse and
    surrender names, because S has no new business to count: every point commences at its
    own month 0.  Here ``pols_new_biz`` is D5's, the annuities commencing in the month,
    which the conventions hold to the count.  The rest of S's ban stands: the contract has
    no account value and no surrender right [S1][S4][S5], so there is no ``pols_lapse``,
    ``lapse_rate``, ``surr_value``, ``cash_value`` or ``av_pp``, and the model is
    undiscounted, with no ``pv_*`` or ``disc_*`` cell beside the contractual commutation
    discount.
    """
    names = set(sec_model.Projection.cells) | set(sec_model.Projection.refs)
    assert "pols_new_biz" in names
    for forbidden in ("pols_lapse", "lapse_rate", "surr_value", "cash_value", "av_pp"):
        assert forbidden not in names, forbidden
    assert not any(n.startswith("pv_") or n.startswith("disc_") for n in names)
    assert "commute_disc_rate" in names


def test_the_stop_rule_ends_every_frame(sec_model, s_model):
    """Every frame ends at the stop rule, S's frame from the annuity date (D3).

    ``stop_mth()`` is S's frame length from the annuity date, the age stop on the youngest
    covered life or the end of the certain period if later, so it is S's ``proj_len()`` on
    every twin, and the frame runs from the valuation date to it: 696, 682, 576, 666, 672,
    1 and 709 months on the anchor's twin and the rows in payment 14, 120, 30, 24 and 695
    months and commencing 13 months on.  Its last month is policy month ``stop_mth() - 1``
    on every point, inside cover, and the next is outside.  A contract's own end is no end
    of the frame: the anchor in its last month still carries S's residual obligation,
    ``pols_if(0)`` 3.41e-06, which is why the notes' other stop test is not subsumed.
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
    lengths = [_row(sec_model, *case).proj_len() for case in (
        ("twin", 8, 0), ("derived", 1, 14), ("derived", 5, 120), ("derived", 13, 30),
        ("derived", 9, 24), ("derived", 8, 695), ("future", 8, -13))]
    assert lengths == [696, 682, 576, 666, 672, 1, 709]
    last = _row(sec_model, "derived", 8, 695)
    assert last.pols_if(0) == pytest.approx(_point(s_model, 8).pols_if(695), rel=1e-12)
    assert last.pols_if(0) == pytest.approx(3.41e-06, rel=1e-3)


def _outside_cover_faults(p, where):
    """Where ``p``, an ItemSpace that has evaluated nothing, departs from OUTSIDE_COVER.

    Every cell of :data:`OUTSIDE_COVER`, each of :data:`PER_LIFE` for every covered life,
    ``pols_if_at`` at each timing and ``claim_pp`` and ``claims`` at each kind, in every
    month before the annuity date and at ``t = proj_len()``, the month after the stop rule,
    which the closing time points read; and before the annuity date :data:`BEFORE_ISSUE`'s
    time points and ``lives_if`` for both lives, all 0.0.  Then whether any of
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
    ``is_active``, which on an installment refund searches the payments to date for the
    refund period; neither may leave the contract.
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

    On every committed point, in every month before the annuity date and in the month after
    the stop rule, ``t = proj_len()``, which the closing time points read, on a model that
    evaluates nothing else.  So afterwards none of :data:`IN_COVER_ONLY` may hold a value at
    all: ``is_active``'s docstring promises that outside cover no cell reads a rate, a
    policy year or an attained age the contract does not have.  Then every monthly cell is
    called at those months, as Phase 2's full sweep calls it, and the policy-clock and age
    keys it reaches must stay inside the contract (:func:`_guard_faults`).

    The committed table's one point commencing after the valuation date is the anchor, a
    life annuity with no certain period, no refund and no commutation, so on it a cell tied
    to one of those would hold zero before the annuity date, guarded or not.  So the same
    scan runs on the splice's future rows, the core's or, with ``USLIB_SEC_FULL=1``, all of
    them: the refund forms, the certain periods, commutation and quarterly payments in
    advance among them, 13 months on, so that a read before the annuity date lands at
    policy year -1.  Each row is made afresh first and released after.

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


def test_the_points_sum_row_by_row_into_a_block(spliced):
    """Row ``t`` is the same month on every point, so a block is its frames summed (D3).

    The anchor on the table basis commencing at the valuation date, in payment 12 months
    and commencing 13 months on, summed as ``run_sec.py --block`` sums them, are indexed
    0..708 and equal S's frame added to itself moved 12 months earlier and 13 months later.
    A model whose frames sat on the policy clock would fail it.  The three are read from
    the splice's one read of its table (:data:`SEC_REFS`), as a block is read; the anchor
    holds no commutation right, so the CMT's change, which the splice's S reads 50 basis
    points up, moves no number of its frame.
    """
    s, sec = spliced[0], spliced[1]
    keys = [_row_key(sec, *case)
            for case in (("twin", 8, 0), ("derived", 8, 12), ("future", 8, -13))]
    try:
        frames = [projection(sec, key).result_cf() for key in keys]
    finally:
        for key in keys:
            _release(sec, key, collect=True)
    block = pd.concat(frames).groupby(level="t").sum()
    sdf = _point(s, 8).result_cf()
    expected = pd.concat([sdf, sdf.set_axis(sdf.index - 12).loc[0:],
                          sdf.set_axis(sdf.index + 13)]).groupby(level=0).sum()
    assert list(block.index) == list(range(709))
    assert frame_mismatches(expected, block) == []


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


def test_an_in_force_extract_needs_none_of_the_generator_columns(sec_model, tmp_path):
    """The model reads the in-force interface and S's columns, never where a row came from.

    ``row_kind``, ``source_policy_id`` and ``source_mth`` record how the generator made each
    shipped row, and an administration extract carries none of them; nor does it number
    its points 1 to n in table order.  Read without them, relabelled 101..122 and reversed
    (:func:`_relabelled`), every point projects what the committed row it was relabelled
    from projects, in ``result_cf`` and ``result_pols``, to 1e-12, and ``run_sec.py``, run
    beside that extract, prints the point it was given by its label, 116, the anchor in
    payment 14 months, without saying where it came from.  On every shipped row
    ``source_mth`` equals ``duration_mth``, so a formula that read the one for the other
    would pass every test that leaves ``duration_mth`` as generated.
    """
    extract = _relabelled(_committed())
    folder = _sec_inputs(tmp_path, extract)
    model = _read(folder, "extract")
    try:
        table = model.Data.model_point_table()
        assert not set(GENERATED_COLUMNS) & set(table.columns)
        assert list(table.index) == list(range(122, 100, -1))
        for point_id in table.index:
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
    out = _run_sec(runner, "116")
    assert out.splitlines()[:3] == [
        "model point 116: IA-000001-M14 - life_only M65 + F62 premium 100,000 income "
        "6,000/yr",
        "m = 12 in arrears   COLA = 3%   survivor = 66.67% on either death   certain = 0 "
        "mths",
        "at the valuation date: in payment 14 months: policy year 2, lives 1.000000 and "
        "0.000000 alive, 0 certain months left"]


def test_run_sec_block_refuses_before_printing(tmp_path):
    """``run_sec.py --block`` asks every point for its frame before it projects any.

    The point at or past the stop rule is refused in ``proj_len()`` when the block reaches
    it, which a loop over the block would do only after projecting the points before it.
    So the runner asks every point for its frame first: run beside the refused table, as an
    extract relabelled and reversed (:func:`_relabelled`) holds it, it exits non-zero,
    prints nothing, and names the point by its label, 121, not by its position.
    """
    extract = _relabelled(REFUSED[0][2](_committed()))
    folder = _sec_inputs(tmp_path, extract)
    runner = folder.parent / "run_sec.py"
    shutil.copy(model_path(SEC).parent / "run_sec.py", runner)
    done = _run_sec(runner, "--block", check=False)
    assert done.returncode != 0 and done.stdout == b""
    assert REFUSED[0][3].replace("point_id 21", "point_id 121") in done.stderr.decode(
        errors="replace")


def _shown(df):
    """A frame as ``run_sec.py`` prints it: to the cent, with no negative zero."""
    return (df.round(2) + 0.0).to_string()


def _standing(p):
    """What ``run_sec.py`` says of point ``p`` at the valuation date, stated here."""
    d = p.duration_mth_init()
    if d < 0:
        return f"to commence at t = {-d}, {-d} months after the valuation date"
    if d == 0:
        return "commencing at the valuation date, t = 0"
    alive = f"{p.lives_if_init(1):.6f}"
    if p.is_joint():
        alive += f" and {p.lives_if_init(2):.6f}"
    left = max(p.certain_mths_eff() - d, 0)
    return (f"in payment {d} months: policy year {p.policy_year(0)}, lives {alive} alive, "
            f"{left} certain months left")


def test_run_sec_prints_a_point_and_the_block(sec_model):
    """The runner prints one point, saying where it came from, and the block (D8).

    Each mode in an interpreter of its own, as a user runs it, with exit code 0 and ASCII
    output, so that it prints on a Windows console under any code page.  The numbers are
    the model's.  Point 1, the runner's default, the worked example's anchor commencing at
    the valuation date, with its lines each asserted whole, so that a longer number cannot
    pass for the one asserted, and its first fifteen rows of cash flows and counts, as
    ``run.py`` prints S's.  Point 16, the anchor in payment 14 months with its joint
    annuitant dead, point 22, the anchor commencing 13 months on, and point 21, the anchor
    in its last month, each with the lines that say where its row came from and where it
    stands, which only the committed table's generator columns can say; point 21's frame
    has one row, and its headings say so, in the singular.  And the block: a line for each
    of the 22 points, in table
    order, its first fifteen rows, which must be the committed points' frames summed row by
    row, as this test sums them, and those frames summed into projection years, each year's
    ``pols_if`` its first month's.  Nothing else runs the runner on the committed table.
    """
    runner = model_path(SEC).parent / "run_sec.py"
    head = ("mortality basis = {}   proj_len = {} months from the valuation date "
            "(t = 0..{}); the stop rule at policy month {}")
    out = _run_sec(runner)
    assert out.splitlines()[:4] == [
        "model point 1: IA-000001 (S's IA-000001) - life_only M65 + F62 premium 100,000 "
        "income 6,000/yr",
        "m = 12 in arrears   COLA = 3%   survivor = 66.67% on either death   certain = 0 "
        "mths",
        "at the valuation date: commencing at the valuation date, t = 0",
        head.format("scenario", 696, 695, 696)]
    assert "first 15 rows, t = 0..14 (months from the valuation date):" in out.splitlines()
    anchor = _point(sec_model, 1)
    assert _shown(anchor.result_cf().head(15)) in out
    assert (anchor.result_pols().head(15).round(6) + 0.0).to_string() in out
    for point_id, lines in (
            ("16", ["model point 16: IA-000001-M14 (S's IA-000001 at its month 14) - "
                    "life_only M65 + F62 premium 100,000 income 6,000/yr",
                    "at the valuation date: in payment 14 months: policy year 2, lives "
                    "1.000000 and 0.000000 alive, 0 certain months left",
                    head.format("scenario", 682, 681, 696)]),
            ("22", ["model point 22: IA-000008-F13 (S's IA-000008, commencing 13 months "
                    "on) - life_only M65 + F62 premium 100,000 income 6,000/yr",
                    "at the valuation date: to commence at t = 13, 13 months after the "
                    "valuation date",
                    head.format("table", 709, 708, 696)]),
            ("21", ["model point 21: IA-000008-M695 (S's IA-000008 at its month 695) - "
                    "life_only M65 + F62 premium 100,000 income 6,000/yr",
                    "at the valuation date: in payment 695 months: policy year 58, lives "
                    "0.000000 and 0.000004 alive, 0 certain months left",
                    "mortality basis = table   proj_len = 1 month from the valuation date "
                    "(t = 0..0); the stop rule at policy month 696"])):
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
        *("  {:>2}  {:<15} {}; proj_len {}".format(
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


# What only SPIA_US_S's docstrings may say: a reference into its Spaces, which the SEC
# pages would link to the wrong model; its clock, t counting policy months from the annuity
# date and t = 0 the first projected month; S's names for the time points of the three
# cells this model moves onto the valuation clock; and "then clear the cache", modelx-only
# advice that a compiled model cannot follow.
STALE = re.compile(r"~\.SPIA_US_S\.|``t`` counts \*\*policy months from the annuity "
                   r"date\*\*|``t = 0`` is the first projected month"
                   r"|\blives_if\(k, life\)|\blives_if_last\(k\)"
                   r"|check_lives_roll_fwd_resid\(k\)|then clear the cache")


def test_the_docstrings_describe_the_valuation_clock(sec_model):
    """The docstrings say what this model is, and none says what only SPIA_US_S is.

    Whitespace is collapsed first, as ``test_model_conventions`` collapses it, so that a
    phrase split across a line break still matches.  The model docstring names the
    valuation date, BasicTerm_SE, the policy clock, the SEC table and the product.  The
    symbol map in the Projection docstring maps every cell running in force adds, and names
    nothing the model lacks: every name in it is a cell, or a Reference the notes give a
    symbol to, as the A/E factor is in ``SPIA_US_S``'s map.  And no docstring says what
    :data:`STALE` matches.
    """
    flat = {where: re.sub(r"\s+", " ", doc) for where, doc in _docs(sec_model)}
    for phrase in ("valuation date", "BasicTerm_SE", "duration_mth", TABLE,
                   "single premium immediate annuit"):
        assert phrase in flat["model"], phrase
    mapped = _mapped_cells(sec_model.Projection.doc)
    missing = [cells for cells in NEW_CELLS if cells not in mapped]
    assert not missing, f"the symbol map does not map {missing}"
    known = set(sec_model.Projection.cells) | set(sec_model.Projection.refs)
    unknown = sorted(mapped - known)
    assert not unknown, f"the symbol map names what the model lacks: {unknown}"
    stale = sorted(where for where, doc in flat.items() if STALE.search(doc))
    assert not stale, f"docstrings that describe SPIA_US_S: {stale}"


def test_the_sec_model_reads_the_s_tables_in_place(sec_model, s_model):
    """One copy of each assumption table serves both models (D1).

    The two ``input_dir()`` s are one directory, and SEC's filename References are S's with
    ``model_point_file`` alone changed, to ``model_point_table_sec.csv``: an edit to a table
    reaches both models, and the two can never drift apart.
    """
    assert sec_model.Data.input_dir() == s_model.Data.input_dir()
    files = {r: v for r, v in s_model.Data.refs.items() if r.endswith("_file")}
    assert {r: v for r, v in sec_model.Data.refs.items() if r.endswith("_file")} == {
        **files, "model_point_file": TABLE}


# What the decodes refuse, as (case, the table's edit, the References set before the model
# computes anything, the point, its message): each text value a projection branches on, and
# the frequency, which picks its payment months.  The decodes read the model point's columns
# and validate them as SPIA_US_S's label accessors do, so an invalid value raises S's own
# message wherever the projection first meets it, and only the rule under test refuses
# each case: the trigger on a joint point, where the payment factor reads it, and the
# discount convention, a Reference, on a point with a certain period still to discount.
UNDECODABLE = [
    ("an unknown form", _set("form", [16], "joint_survivor"), None, 16, "invalid form"),
    ("an unknown reduction trigger", _set("reduction_trigger", [18], "first"), None, 18,
     "invalid reduction_trigger"),
    ("an unknown payment timing", _set("timing", [17], "middle"), None, 17,
     "invalid timing"),
    ("an unknown mortality basis", _set("mort_basis", [20], "select"), None, 20,
     "invalid mort_basis"),
    ("an unknown frequency", _set("frequency", [16], 3), None, 16, "invalid frequency"),
    ("an unknown discount convention", None, {"commute_disc_convention": "continuous"},
     20, "invalid commute_disc_convention"),
]


@pytest.mark.parametrize("case, edit, refs, point_id, message", UNDECODABLE,
                         ids=[c[0] for c in UNDECODABLE])
def test_an_undecodable_value_is_refused_where_the_projection_meets_it(tmp_path, case,
                                                                        edit, refs,
                                                                        point_id, message):
    """An invalid switch raises ``ValueError`` with S's message, not a quiet default.

    Each case is read by a model of its own, from a copy of the inputs with the one fault,
    or with the Reference set before the model computes anything.  The table reads,
    because these are rules of the projection, not of the in-force interface, and the
    point's projection meets the fault on its way to its first number.  A decode that read
    an unknown form as a life annuity, or an unknown trigger as the primary's, would
    project a contract no one wrote.
    """
    model = _read_edited(tmp_path, edit or (lambda table: table), "undecodable", refs)
    try:
        assert len(model.Data.model_point_table()) == len(_committed())
        _refused(_point(model, point_id).result_cf, message)
    finally:
        model.close()


def test_a_life_a_kind_or_a_timing_neither_model_knows_is_refused(sec_model):
    """A third life, an unknown claim kind or timing raises, rather than answers.

    The opening state and both age-keyed table readers take a life, 1 or 2, as
    ``SPIA_US_S``'s ``age_at_entry`` does; ``claim_pp`` takes the one kind,
    ``"REFUND"``; and ``pols_if_at`` the two timings, ``BasicTerm_SE``'s ``"BEF_NB"`` and
    ``"BEF_DECR"`` (the count test asks for ``"BEF_MAT"``).  Each refuses anything else with
    ``ValueError`` instead of answering with another life's, kind's or timing's number.
    """
    p = _row(sec_model, "derived", 1, 14)
    for call, message in ((lambda: p.lives_if_init(3), "invalid life"),
                          (lambda: p.mort_rate_base_at(70, 3), "invalid life"),
                          (lambda: p.improvement_rate_at(70, 3), "invalid life"),
                          (lambda: p.claim_pp(0, "DEATH"), "invalid kind"),
                          (lambda: p.pols_if_at(0, "AFT_DECR"), "invalid timing")):
        _refused(call, message)


def test_the_core_grid_reaches_every_branch(spliced, splice_records):
    """What the default run's T2 and T3 cases reach, which the full grid only multiplies.

    The default run thins the splice to a core (the module docstring), and this test is
    what keeps the thinning from costing a branch.  First, statically, over S's table with
    the variants, each property below holds of some core case: each form; joint and single
    lives; each trigger on a joint contract, and the primary trigger on the table basis;
    each basis, timing and frequency; a commutation taken, barred by the issue state and
    not held; each sex in each role; a COLA and none on a refund form; a premium tax,
    qualified money, a rating and an annuity year other than 2026; and each kind of
    valuation month: an anniversary, mid-year, the last month of a policy year, a scenario
    death month and the month after one, both lives dead, the last certain month and the
    first after a certain period, a trim month and the last month of a frame.  And every
    frequency and timing other than monthly that a refund or commuting point carries is
    valued off its period by some core case, where a payment month counted on the wrong
    clock shows.  Of some core future case: commencing 1, 12 and more than 12 months on,
    each basis, a commuting point, payment in advance, certain_only and a refund form.  And
    the splice's two mortality tables give every ``(age, sex)`` a value of its own, so that
    a join on the wrong key changes a number.

    Then, on the splice's model, of some core row, each of :data:`AT_VALUATION` and
    :data:`IN_FRAME`, what no column of the table shows: every opening-state column at each
    value it takes, what falls at ``t = 0`` because of where the contract stands, and each
    branch of the commutation, the trim and the refund later in the frame.  Each core row's
    branches were recorded by the case that compared it (:func:`_record`), and a row no case
    has recorded is evaluated here.
    """
    s = spliced[0]
    s_table = _s_table_with_variants()

    def at(p, column):
        return s_table.at[p, column]

    def n_eff(p):
        return _point(s, p).certain_mths_eff()

    def deaths(p):
        lives = ("death_mth_1", "death_mth_2") if at(p, "joint") else ("death_mth_1",)
        return [int(at(p, c)) for c in lives if at(p, "mort_basis") == "scenario"
                and not pd.isna(at(p, c))]

    def refund_or_commuting(p):
        return (at(p, "form") in ("cash_refund", "installment_refund")
                or at(p, "commutation_enabled"))

    def on(p):
        return 12 // int(at(p, "frequency"))

    splices = {
        **{f"the {f} form": (lambda k, p, d, f=f: at(p, "form") == f)
           for f in ("life_only", "life_certain", "cash_refund", "installment_refund",
                     "certain_only")},
        "a joint contract": lambda k, p, d: at(p, "joint"),
        "a single life": lambda k, p, d: not at(p, "joint"),
        "the either trigger, joint": lambda k, p, d: (
            at(p, "joint") and at(p, "reduction_trigger") == "either"),
        "the primary trigger, joint": lambda k, p, d: (
            at(p, "joint") and at(p, "reduction_trigger") == "primary"),
        "the primary trigger on the table basis": lambda k, p, d: (
            at(p, "joint") and at(p, "reduction_trigger") == "primary"
            and at(p, "mort_basis") == "table"),
        **{f"the {b} basis": (lambda k, p, d, b=b: at(p, "mort_basis") == b)
           for b in ("table", "scenario")},
        **{f"{m} timing": (lambda k, p, d, m=m: at(p, "timing") == m)
           for m in ("arrears", "advance")},
        **{f"{m} payments a year": (lambda k, p, d, m=m: at(p, "frequency") == m)
           for m in (12, 4, 2, 1)},
        "a commutation taken": lambda k, p, d: (
            at(p, "commutation_enabled") and not at(p, "issue_state_excludes_withdrawal")),
        "a commutation barred by the state": lambda k, p, d: (
            at(p, "commutation_enabled") and at(p, "issue_state_excludes_withdrawal")),
        "no commutation right": lambda k, p, d: not at(p, "commutation_enabled"),
        **{f"a {sex} {role}": (lambda k, p, d, sex=sex, c=c: (
            (c == "primary_sex" or at(p, "joint")) and at(p, c) == sex))
           for sex in ("M", "F") for role, c in (("primary", "primary_sex"),
                                                 ("joint annuitant", "joint_sex"))},
        "a COLA on a refund form": lambda k, p, d: (
            at(p, "form") in ("cash_refund", "installment_refund")
            and at(p, "cola_rate") > 0.0),
        "no COLA on a refund form": lambda k, p, d: (
            at(p, "form") in ("cash_refund", "installment_refund")
            and at(p, "cola_rate") == 0.0),
        "a premium tax": lambda k, p, d: at(p, "premium_tax_rate") > 0.0,
        "qualified money": lambda k, p, d: at(p, "qualified"),
        "a rating": lambda k, p, d: at(p, "rating_factor") != 1.0,
        "an annuity year other than 2026": lambda k, p, d: at(p, "annuity_year") != 2026,
        "on an anniversary": lambda k, p, d: d % 12 == 0,
        "mid-year": lambda k, p, d: d % 12 not in (0, 11),
        "in the last month of a policy year": lambda k, p, d: d % 12 == 11,
        "in a scenario death month": lambda k, p, d: d in deaths(p),
        "the month after a scenario death": lambda k, p, d: d - 1 in deaths(p),
        "both lives dead": lambda k, p, d: (
            at(p, "joint") and len(deaths(p)) == 2 and max(deaths(p)) < d),
        "in the last certain month": lambda k, p, d: d == n_eff(p) - 1,
        "the first month after a certain period": lambda k, p, d: 0 < n_eff(p) == d,
        "in a trim month": lambda k, p, d: (
            at(p, "form") == "installment_refund" and d == n_eff(p) - 1),
        "in the last month of a frame": lambda k, p, d: d == _point(s, p).proj_len() - 1,
    }
    pairs = {(int(at(p, "frequency")), at(p, "timing")) for p in s_table.index
             if refund_or_commuting(p) and at(p, "frequency") != 12}
    for m, timing in sorted(pairs):
        splices[f"a refund or commutation, {m} a year in {timing}, off its period"] = (
            lambda k, p, d, m=m, timing=timing: refund_or_commuting(p)
            and (int(at(p, "frequency")), at(p, "timing")) == (m, timing)
            and d % on(p) != 0)
    futures = {
        "commencing a month on": lambda p, k: k == 1,
        "commencing a year on": lambda p, k: k == 12,
        "commencing more than a year on": lambda p, k: k > 12,
        **{f"the {b} basis": (lambda p, k, b=b: at(p, "mort_basis") == b)
           for b in ("table", "scenario")},
        "a commuting point": lambda p, k: at(p, "commutation_enabled"),
        "advance timing": lambda p, k: at(p, "timing") == "advance",
        "certain_only": lambda p, k: at(p, "form") == "certain_only",
        "a refund form": lambda p, k: at(p, "form") in ("cash_refund",
                                                        "installment_refund"),
    }
    missing = [what for what, holds in splices.items()
               if not any(holds(*case) for case in CORE_SPLICES)]
    missing += [what for what, holds in futures.items()
                if not any(holds(*case) for case in CORE_FUTURES)]
    assert not missing, f"no core case reaches: {missing}"
    assert len(pairs) == 5, sorted(pairs)

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


# ---------------------------------------------------------------------------
# C2 -- the Phase 1 fingerprint


def test_the_phase_1_fingerprint_is_reproduced(sec_model):
    """Every committed point computes what the model computed when Phase 1 ended (C2).

    Phase 2 changes how the model is represented and no number it computes (D2), so before
    it changed anything the model as Phase 1 left it was frozen below, at M13
    (USLIB-SEC-PLAN.md §5.4): for each point, each column of ``result_cf()`` and
    ``result_pols()``, its sum, its largest absolute value and its values at five fixed
    months, the frame's first and last and the three quartiles between.  Every later version
    must reproduce it, to 1e-12 relative, floored at 1e-12 of the column's own magnitude
    (``sec_support.fingerprint_mismatches``), with the same points, frames and columns
    exactly.  ``python tools/gen_sec_fingerprint.py SPIA_US_SEC --check`` runs the same
    comparison from the command line.
    """
    assert fingerprint_mismatches(FINGERPRINT, sec_model) == []


# SPIA_US_SEC's fingerprint, frozen at M13 from the model as Phase 1 left it and committed
# alone, before Phase 2 changed anything.  Each point is keyed by its point_id; each column
# holds (its sum over the frame, its largest absolute value, (its values at the months)).
# The block is written by tools/gen_sec_fingerprint.py, and is never edited by hand: a
# refreeze goes through the tool's --force, in a commit of its own that says why.
# BEGIN generated fingerprint: SPIA_US_SEC -- tools/gen_sec_fingerprint.py
FINGERPRINT = {
    1: {"rows": 696, "months": (0, 173, 347, 521, 695),
        "result_cf": {
            "pols_if": (696.0, 1.0, (
                1.0, 1.0, 1.0, 1.0, 1.0)),
            "annuity_payments": (609291.7979119049, 1797.2171470520775, (
                500.0, 504.1965749769138, 762.64255861722, 1188.1722568386679,
                1797.2171470520775)),
            "claims": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "commutations": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (7650.679735544165, 20.428210844601907, (
                5.0, 7.064869104868828, 9.982475093786014, 14.457600375443329,
                20.428210844601907)),
            "liability_cf": (616942.4776474491, 1817.6453578966793, (
                505.0, 511.2614440817826, 772.6250337110059, 1202.629857214111,
                1817.6453578966793)),
            "net_cf": (-616942.4776474491, 1817.6453578966793, (
                -505.0, -511.2614440817826, -772.6250337110059, -1202.629857214111,
                -1817.6453578966793)),
        },
        "result_pols": {
            "pols_if": (696.0, 1.0, (
                1.0, 1.0, 1.0, 1.0, 1.0)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (696.0, 1.0, (
                1.0, 1.0, 1.0, 1.0, 1.0)),
            "lives_if_2": (13.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_last": (696.0, 1.0, (
                1.0, 1.0, 1.0, 1.0, 1.0)),
            "lives_death_last": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "certain_floor": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor_life": (468.33333335610007, 1.0, (
                1.0, 0.6666666667, 0.6666666667, 0.6666666667, 0.6666666667)),
            "payment_factor": (468.33333335610007, 1.0, (
                1.0, 0.6666666667, 0.6666666667, 0.6666666667, 0.6666666667)),
        },
    },
    2: {"rows": 696, "months": (0, 173, 347, 521, 695),
        "result_cf": {
            "pols_if": (696.0, 1.0, (
                1.0, 1.0, 1.0, 1.0, 1.0)),
            "annuity_payments": (910680.1968226491, 2695.8257204433253, (
                500.0, 756.2948624275559, 1143.9638378686318, 1782.258385168889,
                2695.8257204433253)),
            "claims": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "commutations": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (7650.679735544165, 20.428210844601907, (
                5.0, 7.064869104868828, 9.982475093786014, 14.457600375443329,
                20.428210844601907)),
            "liability_cf": (918330.8765581934, 2716.253931287927, (
                505.0, 763.3597315324248, 1153.9463129624178, 1796.7159855443322,
                2716.253931287927)),
            "net_cf": (-918330.8765581934, 2716.253931287927, (
                -505.0, -763.3597315324248, -1153.9463129624178, -1796.7159855443322,
                -2716.253931287927)),
        },
        "result_pols": {
            "pols_if": (696.0, 1.0, (
                1.0, 1.0, 1.0, 1.0, 1.0)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (696.0, 1.0, (
                1.0, 1.0, 1.0, 1.0, 1.0)),
            "lives_if_2": (13.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_last": (696.0, 1.0, (
                1.0, 1.0, 1.0, 1.0, 1.0)),
            "lives_death_last": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "certain_floor": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor_life": (696.0, 1.0, (
                1.0, 1.0, 1.0, 1.0, 1.0)),
            "payment_factor": (696.0, 1.0, (
                1.0, 1.0, 1.0, 1.0, 1.0)),
        },
    },
    3: {"rows": 696, "months": (0, 173, 347, 521, 695),
        "result_cf": {
            "pols_if": (696.0, 1.0, (
                1.0, 1.0, 1.0, 1.0, 1.0)),
            "annuity_payments": (609291.7979119049, 1797.2171470520775, (
                500.0, 504.1965749769138, 762.64255861722, 1188.1722568386679,
                1797.2171470520775)),
            "claims": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "commutations": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (7650.679735544165, 20.428210844601907, (
                5.0, 7.064869104868828, 9.982475093786014, 14.457600375443329,
                20.428210844601907)),
            "liability_cf": (616942.4776474491, 1817.6453578966793, (
                505.0, 511.2614440817826, 772.6250337110059, 1202.629857214111,
                1817.6453578966793)),
            "net_cf": (-616942.4776474491, 1817.6453578966793, (
                -505.0, -511.2614440817826, -772.6250337110059, -1202.629857214111,
                -1817.6453578966793)),
        },
        "result_pols": {
            "pols_if": (696.0, 1.0, (
                1.0, 1.0, 1.0, 1.0, 1.0)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (13.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_2": (696.0, 1.0, (
                1.0, 1.0, 1.0, 1.0, 1.0)),
            "lives_if_last": (696.0, 1.0, (
                1.0, 1.0, 1.0, 1.0, 1.0)),
            "lives_death_last": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "certain_floor": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor_life": (468.33333335610007, 1.0, (
                1.0, 0.6666666667, 0.6666666667, 0.6666666667, 0.6666666667)),
            "payment_factor": (468.33333335610007, 1.0, (
                1.0, 0.6666666667, 0.6666666667, 0.6666666667, 0.6666666667)),
        },
    },
    4: {"rows": 696, "months": (0, 173, 347, 521, 695),
        "result_cf": {
            "pols_if": (696.0, 1.0, (
                1.0, 1.0, 1.0, 1.0, 1.0)),
            "annuity_payments": (609291.7979119049, 1797.2171470520775, (
                500.0, 504.1965749769138, 762.64255861722, 1188.1722568386679,
                1797.2171470520775)),
            "claims": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "commutations": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (7650.679735544165, 20.428210844601907, (
                5.0, 7.064869104868828, 9.982475093786014, 14.457600375443329,
                20.428210844601907)),
            "liability_cf": (616942.4776474491, 1817.6453578966793, (
                505.0, 511.2614440817826, 772.6250337110059, 1202.629857214111,
                1817.6453578966793)),
            "net_cf": (-616942.4776474491, 1817.6453578966793, (
                -505.0, -511.2614440817826, -772.6250337110059, -1202.629857214111,
                -1817.6453578966793)),
        },
        "result_pols": {
            "pols_if": (696.0, 1.0, (
                1.0, 1.0, 1.0, 1.0, 1.0)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (13.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_2": (696.0, 1.0, (
                1.0, 1.0, 1.0, 1.0, 1.0)),
            "lives_if_last": (696.0, 1.0, (
                1.0, 1.0, 1.0, 1.0, 1.0)),
            "lives_death_last": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "certain_floor": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor_life": (468.33333335610007, 1.0, (
                1.0, 0.6666666667, 0.6666666667, 0.6666666667, 0.6666666667)),
            "payment_factor": (468.33333335610007, 1.0, (
                1.0, 0.6666666667, 0.6666666667, 0.6666666667, 0.6666666667)),
        },
    },
    5: {"rows": 696, "months": (0, 173, 347, 521, 695),
        "result_cf": {
            "pols_if": (696.0, 1.0, (
                1.0, 1.0, 1.0, 1.0, 1.0)),
            "annuity_payments": (630047.8898661041, 1797.2171470520775, (
                500.0, 504.1965749769138, 762.64255861722, 1188.1722568386679,
                1797.2171470520775)),
            "claims": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "commutations": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (7650.679735544165, 20.428210844601907, (
                5.0, 7.064869104868828, 9.982475093786014, 14.457600375443329,
                20.428210844601907)),
            "liability_cf": (637698.5696016483, 1817.6453578966793, (
                505.0, 511.2614440817826, 772.6250337110059, 1202.629857214111,
                1817.6453578966793)),
            "net_cf": (-637698.5696016483, 1817.6453578966793, (
                -505.0, -511.2614440817826, -772.6250337110059, -1202.629857214111,
                -1817.6453578966793)),
        },
        "result_pols": {
            "pols_if": (696.0, 1.0, (
                1.0, 1.0, 1.0, 1.0, 1.0)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (696.0, 1.0, (
                1.0, 1.0, 1.0, 1.0, 1.0)),
            "lives_if_2": (13.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_last": (696.0, 1.0, (
                1.0, 1.0, 1.0, 1.0, 1.0)),
            "lives_death_last": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "certain_floor": (120.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor_life": (468.33333335610007, 1.0, (
                1.0, 0.6666666667, 0.6666666667, 0.6666666667, 0.6666666667)),
            "payment_factor": (504.0000000192001, 1.0, (
                1.0, 0.6666666667, 0.6666666667, 0.6666666667, 0.6666666667)),
        },
    },
    6: {"rows": 660, "months": (0, 164, 329, 494, 659),
        "result_cf": {
            "pols_if": (13.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "annuity_payments": (6515.0, 515.0, (
                500.0, 0.0, 0.0, 0.0, 0.0)),
            "claims": (93485.0, 93485.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "commutations": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (65.125, 5.125, (
                5.0, 0.0, 0.0, 0.0, 0.0)),
            "liability_cf": (100065.125, 93485.0, (
                505.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-100065.125, 93485.0, (
                -505.0, -0.0, -0.0, -0.0, -0.0)),
        },
        "result_pols": {
            "pols_if": (13.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (13.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_2": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_last": (13.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_death_last": (1.0, 1.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "certain_floor": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor_life": (13.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor": (13.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
        },
    },
    7: {"rows": 660, "months": (0, 164, 329, 494, 659),
        "result_cf": {
            "pols_if": (316.8789871406775, 1.0, (
                1.0, 1.0, 0.4533615758332075, 0.0270725005003155, 3.195196447684427e-09)),
            "annuity_payments": (158439.49357033876, 500.0, (
                500.0, 500.0, 226.68078791660375, 13.53625025015775,
                1.5975982238422135e-06)),
            "claims": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "commutations": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (2295.3725762129266, 7.422528103302811, (
                5.0, 6.892555224262271, 4.415288428521536, 0.3725433845544806,
                6.061167699664998e-08)),
            "liability_cf": (160734.86614655168, 507.4225281033028, (
                505.0, 506.89255522426225, 231.09607634512528, 13.90879363471223,
                1.6582099008388635e-06)),
            "net_cf": (-160734.86614655168, 507.4225281033028, (
                -505.0, -506.89255522426225, -231.09607634512528, -13.90879363471223,
                -1.6582099008388635e-06)),
        },
        "result_pols": {
            "pols_if": (316.8789871406775, 1.0, (
                1.0, 1.0, 0.4533615758332075, 0.0270725005003155, 3.195196447684427e-09)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (299.9336617853571, 0.999472363658361, (
                0.999472363658361, 0.8457105269741015, 0.4533615758332075,
                0.0270725005003155, 3.195196447684427e-09)),
            "lives_if_2": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_last": (299.9336617853571, 0.999472363658361, (
                0.999472363658361, 0.8457105269741015, 0.4533615758332075,
                0.0270725005003155, 3.195196447684427e-09)),
            "lives_death_last": (0.9999999968048036, 0.003502978072599694, (
                0.0005276363416389929, 0.0014857527692960781, 0.0032422009541358543,
                0.0009723874275236778, 7.097109274103579e-10)),
            "certain_floor": (200.0, 1.0, (
                1.0, 1.0, 0.0, 0.0, 0.0)),
            "payment_factor_life": (299.9336617853571, 0.999472363658361, (
                0.999472363658361, 0.8457105269741015, 0.4533615758332075,
                0.0270725005003155, 3.195196447684427e-09)),
            "payment_factor": (316.8789871406775, 1.0, (
                1.0, 1.0, 0.4533615758332075, 0.0270725005003155, 3.195196447684427e-09)),
        },
    },
    8: {"rows": 696, "months": (0, 173, 347, 521, 695),
        "result_cf": {
            "pols_if": (415.44406510564505, 0.9999998617079374, (
                0.9999998617079374, 0.9853740775545553, 0.7816680689068627,
                0.11929383070992665, 3.4077840442356674e-06)),
            "annuity_payments": (312391.8876179644, 761.9478747288152, (
                499.8683546770539, 688.2590037313373, 692.3749553837064, 142.35633170051923,
                0.0061245279177508175)),
            "claims": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "commutations": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (3346.9141110099436, 8.190040407587535, (
                4.999999308539687, 6.9615388772537985, 7.802982029470567,
                1.7247025316599085, 6.96149309685164e-05)),
            "liability_cf": (315738.8017289743, 770.0413168545047, (
                504.8683539855936, 695.2205426085911, 700.1779374131769, 144.08103423217915,
                0.006194142848719334)),
            "net_cf": (-315738.8017289743, 770.0413168545047, (
                -504.8683539855936, -695.2205426085911, -700.1779374131769,
                -144.08103423217915, -0.006194142848719334)),
        },
        "result_pols": {
            "pols_if": (415.44406510564505, 0.9999998617079374, (
                0.9999998617079374, 0.9853740775545553, 0.7816680689068627,
                0.11929383070992665, 3.4077840442356674e-06)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (299.9336617853571, 0.999472363658361, (
                0.999472363658361, 0.8315997682341367, 0.3948442765477495,
                0.009321164091820239, 0.0)),
            "lives_if_2": (375.76703714559807, 0.9997379026959461, (
                0.9997379026959461, 0.9131478484793301, 0.6392136393462291,
                0.11100738466598184, 3.4077840442356674e-06)),
            "lives_if_last": (415.44406510564505, 0.9999998617079374, (
                0.9999998617079374, 0.9853740775545553, 0.7816680689068627,
                0.11929383070992665, 3.4077840442356674e-06)),
            "lives_death_last": (0.9999965922159558, 0.004696395448573587, (
                1.382920625792039e-07, 0.00028352457043634427, 0.0025835516238846834,
                0.002699008278418291, 4.368066565053951e-07)),
            "certain_floor": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor_life": (363.71492135070633, 0.9997367093541079, (
                0.9997367093541079, 0.9100405647635407, 0.6052419949512564,
                0.07987412649318487, 2.2718560296040377e-06)),
            "payment_factor": (363.71492135070633, 0.9997367093541079, (
                0.9997367093541079, 0.9100405647635407, 0.6052419949512564,
                0.07987412649318487, 2.2718560296040377e-06)),
        },
    },
    9: {"rows": 696, "months": (0, 173, 347, 521, 695),
        "result_cf": {
            "pols_if": (415.59176738246333, 1.0, (
                1.0, 0.9853740775545553, 0.7816680689068627, 0.11929383070992665,
                3.4077840442356674e-06)),
            "annuity_payments": (313923.332751018, 761.9478747288152, (
                500.0, 688.2590037313373, 692.3749553837064, 142.35633170051923,
                0.0061245279177508175)),
            "claims": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "commutations": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (3347.7989228627466, 8.190040407587535, (
                5.0, 6.9615388772537985, 7.802982029470567, 1.7247025316599085,
                6.96149309685164e-05)),
            "liability_cf": (317271.13167388074, 770.0413168545047, (
                505.0, 695.2205426085911, 700.1779374131769, 144.08103423217915,
                0.006194142848719334)),
            "net_cf": (-317271.13167388074, 770.0413168545047, (
                -505.0, -695.2205426085911, -700.1779374131769, -144.08103423217915,
                -0.006194142848719334)),
        },
        "result_pols": {
            "pols_if": (415.59176738246333, 1.0, (
                1.0, 0.9853740775545553, 0.7816680689068627, 0.11929383070992665,
                3.4077840442356674e-06)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (299.9336617853571, 0.999472363658361, (
                0.999472363658361, 0.8315997682341367, 0.3948442765477495,
                0.009321164091820239, 0.0)),
            "lives_if_2": (375.76703714559807, 0.9997379026959461, (
                0.9997379026959461, 0.9131478484793301, 0.6392136393462291,
                0.11100738466598184, 3.4077840442356674e-06)),
            "lives_if_last": (415.44406510564505, 0.9999998617079374, (
                0.9999998617079374, 0.9853740775545553, 0.7816680689068627,
                0.11929383070992665, 3.4077840442356674e-06)),
            "lives_death_last": (0.9999965922159558, 0.004696395448573587, (
                1.382920625792039e-07, 0.00028352457043634427, 0.0025835516238846834,
                0.002699008278418291, 4.368066565053951e-07)),
            "certain_floor": (120.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor_life": (363.71492135070633, 0.9997367093541079, (
                0.9997367093541079, 0.9100405647635407, 0.6052419949512564,
                0.07987412649318487, 2.2718560296040377e-06)),
            "payment_factor": (366.2444700838551, 1.0, (
                1.0, 0.9100405647635407, 0.6052419949512564, 0.07987412649318487,
                2.2718560296040377e-06)),
        },
    },
    10: {"rows": 660, "months": (0, 164, 329, 494, 659),
        "result_cf": {
            "pols_if": (13.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "annuity_payments": (7030.0, 515.0, (
                500.0, 0.0, 0.0, 0.0, 0.0)),
            "claims": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "commutations": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (65.125, 5.125, (
                5.0, 0.0, 0.0, 0.0, 0.0)),
            "liability_cf": (7095.125, 520.125, (
                505.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-7095.125, 520.125, (
                -505.0, -0.0, -0.0, -0.0, -0.0)),
        },
        "result_pols": {
            "pols_if": (13.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (13.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_2": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_last": (13.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_death_last": (1.0, 1.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "certain_floor": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor_life": (14.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor": (14.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
        },
    },
    11: {"rows": 660, "months": (0, 164, 329, 494, 659),
        "result_cf": {
            "pols_if": (13.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "annuity_payments": (7030.0, 515.0, (
                500.0, 0.0, 0.0, 0.0, 0.0)),
            "claims": (92970.0, 92970.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "commutations": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (65.125, 5.125, (
                5.0, 0.0, 0.0, 0.0, 0.0)),
            "liability_cf": (100065.125, 93485.0, (
                505.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-100065.125, 93485.0, (
                -505.0, -0.0, -0.0, -0.0, -0.0)),
        },
        "result_pols": {
            "pols_if": (13.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (13.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_2": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_last": (13.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_death_last": (1.0, 1.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "certain_floor": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor_life": (14.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor": (14.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
        },
    },
    12: {"rows": 660, "months": (0, 164, 329, 494, 659),
        "result_cf": {
            "pols_if": (330.1264603296302, 1.0, (
                1.0, 1.0, 0.4533615758332075, 0.0270725005003155, 3.195196447684427e-09)),
            "annuity_payments": (132050.58413185208, 400.0, (
                400.0, 400.0, 181.34463033328302, 10.8290002001262,
                1.2780785790737709e-06)),
            "claims": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "commutations": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (2399.7005423563337, 8.193082201451972, (
                5.0, 6.892555224262271, 4.415288428521536, 0.3725433845544806,
                6.061167699664998e-08)),
            "liability_cf": (134450.28467420844, 408.19308220145194, (
                405.0, 406.89255522426225, 185.75991876180456, 11.201543584680682,
                1.3386902560704208e-06)),
            "net_cf": (-134450.28467420844, 408.19308220145194, (
                -405.0, -406.89255522426225, -185.75991876180456, -11.201543584680682,
                -1.3386902560704208e-06)),
        },
        "result_pols": {
            "pols_if": (330.1264603296302, 1.0, (
                1.0, 1.0, 0.4533615758332075, 0.0270725005003155, 3.195196447684427e-09)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (299.9336617853571, 0.999472363658361, (
                0.999472363658361, 0.8457105269741015, 0.4533615758332075,
                0.0270725005003155, 3.195196447684427e-09)),
            "lives_if_2": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_last": (299.9336617853571, 0.999472363658361, (
                0.999472363658361, 0.8457105269741015, 0.4533615758332075,
                0.0270725005003155, 3.195196447684427e-09)),
            "lives_death_last": (0.9999999968048036, 0.003502978072599694, (
                0.0005276363416389929, 0.0014857527692960781, 0.0032422009541358543,
                0.0009723874275236778, 7.097109274103579e-10)),
            "certain_floor": (250.0, 1.0, (
                1.0, 1.0, 0.0, 0.0, 0.0)),
            "payment_factor_life": (299.9336617853571, 0.999472363658361, (
                0.999472363658361, 0.8457105269741015, 0.4533615758332075,
                0.0270725005003155, 3.195196447684427e-09)),
            "payment_factor": (330.1264603296302, 1.0, (
                1.0, 1.0, 0.4533615758332075, 0.0270725005003155, 3.195196447684427e-09)),
        },
    },
    13: {"rows": 696, "months": (0, 173, 347, 521, 695),
        "result_cf": {
            "pols_if": (120.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "annuity_payments": (68783.27586882439, 652.3865919146225, (
                500.0, 0.0, 0.0, 0.0, 0.0)),
            "claims": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "commutations": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (672.2029060712586, 6.244314849738326, (
                5.0, 0.0, 0.0, 0.0, 0.0)),
            "liability_cf": (69455.47877489564, 658.6309067643608, (
                505.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-69455.47877489564, 658.6309067643608, (
                -505.0, -0.0, -0.0, -0.0, -0.0)),
        },
        "result_pols": {
            "pols_if": (120.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (29.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_2": (13.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_last": (29.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_death_last": (1.0, 1.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "certain_floor": (120.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor_life": (23.666666667199998, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor": (120.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
        },
    },
    14: {"rows": 660, "months": (0, 164, 329, 494, 659),
        "result_cf": {
            "pols_if": (2.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "annuity_payments": (1500.0, 1500.0, (
                1500.0, 0.0, 0.0, 0.0, 0.0)),
            "claims": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "commutations": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (10.0, 5.0, (
                5.0, 0.0, 0.0, 0.0, 0.0)),
            "liability_cf": (1510.0, 1505.0, (
                1505.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-1510.0, 1505.0, (
                -1505.0, -0.0, -0.0, -0.0, -0.0)),
        },
        "result_pols": {
            "pols_if": (2.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (2.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_2": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_last": (2.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_death_last": (1.0, 1.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "certain_floor": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor_life": (3.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor": (3.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
        },
    },
    15: {"rows": 660, "months": (0, 164, 329, 494, 659),
        "result_cf": {
            "pols_if": (120.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "annuity_payments": (68783.27586882439, 652.3865919146225, (
                500.0, 0.0, 0.0, 0.0, 0.0)),
            "claims": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "commutations": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (672.2029060712586, 6.244314849738326, (
                5.0, 0.0, 0.0, 0.0, 0.0)),
            "liability_cf": (69455.47877489564, 658.6309067643608, (
                505.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-69455.47877489564, 658.6309067643608, (
                -505.0, -0.0, -0.0, -0.0, -0.0)),
        },
        "result_pols": {
            "pols_if": (120.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (299.9336617853571, 0.999472363658361, (
                0.999472363658361, 0.8457105269741015, 0.4533615758332075,
                0.0270725005003155, 3.195196447684427e-09)),
            "lives_if_2": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_last": (299.9336617853571, 0.999472363658361, (
                0.999472363658361, 0.8457105269741015, 0.4533615758332075,
                0.0270725005003155, 3.195196447684427e-09)),
            "lives_death_last": (0.9999999968048036, 0.003502978072599694, (
                0.0005276363416389929, 0.0014857527692960781, 0.0032422009541358543,
                0.0009723874275236778, 7.097109274103579e-10)),
            "certain_floor": (120.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor_life": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor": (120.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
        },
    },
    16: {"rows": 682, "months": (0, 170, 340, 510, 681),
        "result_cf": {
            "pols_if": (682.0, 1.0, (
                1.0, 1.0, 1.0, 1.0, 1.0)),
            "annuity_payments": (602433.4645785545, 1797.2171470520775, (
                343.33333335049997, 519.3224722262212, 785.5218353757366,
                1188.1722568386679, 1797.2171470520775)),
            "claims": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "commutations": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (7365.68128180972, 19.929961799611622, (
                5.0, 7.064869104868828, 9.982475093786014, 14.104975976042272,
                19.929961799611622)),
            "liability_cf": (609799.1458603642, 1817.1471088516892, (
                348.33333335049997, 526.38734133109, 795.5043104695226, 1202.27723281471,
                1817.1471088516892)),
            "net_cf": (-609799.1458603642, 1817.1471088516892, (
                -348.33333335049997, -526.38734133109, -795.5043104695226,
                -1202.27723281471, -1817.1471088516892)),
        },
        "result_pols": {
            "pols_if": (682.0, 1.0, (
                1.0, 1.0, 1.0, 1.0, 1.0)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (682.0, 1.0, (
                1.0, 1.0, 1.0, 1.0, 1.0)),
            "lives_if_2": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_last": (682.0, 1.0, (
                1.0, 1.0, 1.0, 1.0, 1.0)),
            "lives_death_last": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "certain_floor": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor_life": (454.6666666894001, 0.6666666667, (
                0.6666666667, 0.6666666667, 0.6666666667, 0.6666666667, 0.6666666667)),
            "payment_factor": (454.6666666894001, 0.6666666667, (
                0.6666666667, 0.6666666667, 0.6666666667, 0.6666666667, 0.6666666667)),
        },
    },
    17: {"rows": 647, "months": (0, 161, 323, 484, 646),
        "result_cf": {
            "pols_if": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "annuity_payments": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims": (93485.0, 93485.0, (
                93485.0, 0.0, 0.0, 0.0, 0.0)),
            "commutations": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "liability_cf": (93485.0, 93485.0, (
                93485.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-93485.0, 93485.0, (
                -93485.0, -0.0, -0.0, -0.0, -0.0)),
        },
        "result_pols": {
            "pols_if": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_2": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_last": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_death_last": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "certain_floor": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor_life": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
        },
    },
    18: {"rows": 576, "months": (0, 143, 287, 431, 575),
        "result_cf": {
            "pols_if": (576.0, 1.0, (
                1.0, 1.0, 1.0, 1.0, 1.0)),
            "annuity_payments": (561264.6139972797, 1797.2171470520775, (
                447.9721264704394, 620.0981906008374, 884.1117461627613, 1260.531947280143,
                1797.2171470520775)),
            "claims": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "commutations": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (5451.574945664256, 15.958485661919182, (
                5.0, 6.560433289006328, 8.823053412597988, 11.866025930331185,
                15.958485661919182)),
            "liability_cf": (566716.188942944, 1813.1756327139967, (
                452.9721264704394, 626.6586238898437, 892.9347995753593, 1272.3979732104742,
                1813.1756327139967)),
            "net_cf": (-566716.188942944, 1813.1756327139967, (
                -452.9721264704394, -626.6586238898437, -892.9347995753593,
                -1272.3979732104742, -1813.1756327139967)),
        },
        "result_pols": {
            "pols_if": (576.0, 1.0, (
                1.0, 1.0, 1.0, 1.0, 1.0)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (576.0, 1.0, (
                1.0, 1.0, 1.0, 1.0, 1.0)),
            "lives_if_2": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_last": (576.0, 1.0, (
                1.0, 1.0, 1.0, 1.0, 1.0)),
            "lives_death_last": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "certain_floor": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor_life": (384.00000001920006, 0.6666666667, (
                0.6666666667, 0.6666666667, 0.6666666667, 0.6666666667, 0.6666666667)),
            "payment_factor": (384.00000001920006, 0.6666666667, (
                0.6666666667, 0.6666666667, 0.6666666667, 0.6666666667, 0.6666666667)),
        },
    },
    19: {"rows": 666, "months": (0, 166, 332, 498, 665),
        "result_cf": {
            "pols_if": (90.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "annuity_payments": (53420.575868824395, 652.3865919146225, (
                530.45, 0.0, 0.0, 0.0, 0.0)),
            "claims": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "commutations": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (488.50638141375725, 5.943428768341061, (
                5.0, 0.0, 0.0, 0.0, 0.0)),
            "liability_cf": (53909.08225023816, 658.3300206829635, (
                535.45, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-53909.08225023816, 658.3300206829635, (
                -535.45, -0.0, -0.0, -0.0, -0.0)),
        },
        "result_pols": {
            "pols_if": (90.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_2": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_last": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_death_last": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "certain_floor": (90.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor_life": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor": (90.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
        },
    },
    20: {"rows": 672, "months": (0, 167, 335, 503, 671),
        "result_cf": {
            "pols_if": (391.5917673824633, 1.0, (
                1.0, 0.9794947093447094, 0.7470775839667796, 0.10436471671971674,
                3.4077840442356674e-06)),
            "annuity_payments": (301743.332751018, 761.9478747288152, (
                530.45, 695.2860525976997, 671.59197922878, 124.41709353005793,
                0.0061245279177508175)),
            "claims": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "commutations": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (3070.8377612019012, 7.795398365342093, (
                5.0, 6.751221376031131, 7.275788658608984, 1.4361578751981094,
                6.626049348579791e-05)),
            "liability_cf": (304814.1705122199, 769.6513294587993, (
                535.45, 702.0372739737309, 678.867767887389, 125.85325140525603,
                0.006190788411236615)),
            "net_cf": (-304814.1705122199, 769.6513294587993, (
                -535.45, -702.0372739737309, -678.867767887389, -125.85325140525603,
                -0.006190788411236615)),
        },
        "result_pols": {
            "pols_if": (391.5917673824633, 1.0, (
                1.0, 0.9794947093447094, 0.7470775839667796, 0.10436471671971674,
                3.4077840442356674e-06)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (276.09520782166703, 0.9861902999721686, (
                0.9861902999721686, 0.8014425967879621, 0.3549384679523142,
                0.007111684193975277, 0.0)),
            "lives_if_2": (351.84741527141176, 0.9931238646745103, (
                0.9931238646745103, 0.8967286521500626, 0.6079096280468895,
                0.09794961928501661, 3.4077840442356674e-06)),
            "lives_if_last": (391.4447799412157, 0.9999050426338043, (
                0.9999050426338043, 0.9794947093447094, 0.7470775839667796,
                0.10436471671971674, 3.4077840442356674e-06)),
            "lives_death_last": (0.9999100429381391, 0.004696395448573587, (
                8.408088379097123e-06, 0.00035869194487847533, 0.00287738853432018,
                0.0023449413379820483, 4.368066565053951e-07)),
            "certain_floor": (96.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor_life": (339.79580101659644, 0.9930730690941776, (
                0.9930730690941776, 0.892555319436272, 0.569975226673038,
                0.06980867340302513, 2.2718560296040377e-06)),
            "payment_factor": (342.2444700838551, 1.0, (
                1.0, 0.892555319436272, 0.569975226673038, 0.06980867340302513,
                2.2718560296040377e-06)),
        },
    },
    21: {"rows": 1, "months": (0,),
        "result_cf": {
            "pols_if": (3.4077840442356674e-06, 3.4077840442356674e-06, (
                3.4077840442356674e-06,)),
            "annuity_payments": (0.0061245279177508175, 0.0061245279177508175, (
                0.0061245279177508175,)),
            "claims": (0.0, 0.0, (
                0.0,)),
            "commutations": (0.0, 0.0, (
                0.0,)),
            "expenses": (1.7038920221178336e-05, 1.7038920221178336e-05, (
                1.7038920221178336e-05,)),
            "liability_cf": (0.006141566837971996, 0.006141566837971996, (
                0.006141566837971996,)),
            "net_cf": (-0.006141566837971996, 0.006141566837971996, (
                -0.006141566837971996,)),
        },
        "result_pols": {
            "pols_if": (3.4077840442356674e-06, 3.4077840442356674e-06, (
                3.4077840442356674e-06,)),
            "pols_new_biz": (0.0, 0.0, (
                0.0,)),
            "lives_if_1": (0.0, 0.0, (
                0.0,)),
            "lives_if_2": (3.4077840442356674e-06, 3.4077840442356674e-06, (
                3.4077840442356674e-06,)),
            "lives_if_last": (3.4077840442356674e-06, 3.4077840442356674e-06, (
                3.4077840442356674e-06,)),
            "lives_death_last": (4.368066565053951e-07, 4.368066565053951e-07, (
                4.368066565053951e-07,)),
            "certain_floor": (0.0, 0.0, (
                0.0,)),
            "payment_factor_life": (2.2718560296040377e-06, 2.2718560296040377e-06, (
                2.2718560296040377e-06,)),
            "payment_factor": (2.2718560296040377e-06, 2.2718560296040377e-06, (
                2.2718560296040377e-06,)),
        },
    },
    22: {"rows": 709, "months": (0, 177, 354, 531, 708),
        "result_cf": {
            "pols_if": (415.4440651056451, 0.9999998617079374, (
                0.0, 0.9877691413826699, 0.7971541074190328, 0.1275854757933902,
                3.4077840442356674e-06)),
            "annuity_payments": (312391.88761796436, 761.9478747288152, (
                0.0, 674.1077651791418, 711.1868526707815, 152.3427176622142,
                0.0061245279177508175)),
            "claims": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "commutations": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (3437.598460271658, 8.414040009394514, (
                0.0, 6.978459689697234, 8.156510298800209, 1.8906943182999245,
                7.313918684879753e-05)),
            "liability_cf": (315829.486078236, 770.243652907647, (
                0.0, 681.086224868839, 719.3433629695817, 154.23341198051412,
                0.006197667104599615)),
            "net_cf": (-315829.486078236, 770.243652907647, (
                -0.0, -681.086224868839, -719.3433629695817, -154.23341198051412,
                -0.006197667104599615)),
        },
        "result_pols": {
            "pols_if": (415.4440651056451, 0.9999998617079374, (
                0.0, 0.9877691413826699, 0.7971541074190328, 0.1275854757933902,
                3.4077840442356674e-06)),
            "pols_new_biz": (1.0, 1.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (299.93366178535706, 0.999472363658361, (
                0.0, 0.8457105269741015, 0.41414355528184443, 0.01067134102146671, 0.0)),
            "lives_if_2": (375.7670371455981, 0.9997379026959461, (
                0.0, 0.9207278476135752, 0.6537617800235135, 0.11817522287551595,
                3.4077840442356674e-06)),
            "lives_if_last": (415.4440651056451, 0.9999998617079374, (
                0.0, 0.9877691413826699, 0.7971541074190328, 0.1275854757933902,
                3.4077840442356674e-06)),
            "lives_death_last": (0.9999965922159557, 0.004696395448573587, (
                0.0, 0.00023917761977498841, 0.0025761607677620146, 0.0028969224106900338,
                4.368066565053951e-07)),
            "certain_floor": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor_life": (363.71492135070633, 0.9997367093541079, (
                0.0, 0.9180691719970856, 0.621686480925677, 0.08547734656766842,
                2.2718560296040377e-06)),
            "payment_factor": (363.71492135070633, 0.9997367093541079, (
                0.0, 0.9180691719970856, 0.621686480925677, 0.08547734656766842,
                2.2718560296040377e-06)),
        },
    },
}
# END generated fingerprint: SPIA_US_SEC
