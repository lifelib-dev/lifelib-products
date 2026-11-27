"""In-force tests for Term_UK_SEC: the splice, future business, counts, regeneration.

``Term_UK_SEC`` is ``Term_UK_S`` taught to run in force at a valuation date
(UKLIB-SEC-PLAN.md, milestone M1, after USLIB-SEC-PLAN.md's Phase 1), and represented so
that it compiles under modelx-cython (milestone M2, the C step, after its Phase 2).  It
runs on two clocks: ``t`` counts months from the valuation date, the same month for every
model point, and ``duration_mth(t)`` counts the months the policy has been in force,
``duration_mth_init() + t``.  A model point may be a policy already in force at the
valuation date, in any month of its policy year, one issued at it, or one to be issued
after it, as in ``basiclife/BasicTerm_SE``.  A policy in force opens with seven columns of
state beside its count, the selective-lapse ratio, the deaths since issue and the family
income benefit streams in payment per policy in force, the two indexation factors, the
share whose premium is waived and the initial commission paid at issue, and with the
lives still in the waiver's deferred period in a companion, ``wop_pipeline_sec.csv``,
each measured at the valuation instant.

The worked example is not restated here.  On a point issued at the valuation date the two
clocks coincide and the model is ``Term_UK_S``, and ``test_model_conventions_uk.py``
asserts that cell by cell on the twins of S's seven new-business points (T1), so every
golden of ``test_term_assurance_uk.py`` on them holds on this model with no number copied.
S's point 8, in force five years, is a splice case (T2), and at the shipped assumptions it
is S's point from month 60 on, in every cell but those expense inflation moves.  The
conventions also hold the SEC family's other rules: every frame opens at ``t = 0``,
``pols_if`` is the ``BEF_DECR`` count, ``BEF_DECR`` is ``BEF_NB`` plus the month's new
business, new business enters once, and nothing happens before issue.  This module holds
the rest of the plan's tests (its §5) and the product's own facts:

* T2, the splice: an S point restated in force at month ``d``, opened with the state S
  carries into ``d``, continues S's projection from ``d`` on, in every cell of S's and in
  ``result_pols``.  The months straddle the product's events: the waiver's first entrants,
  the first anniversary, the selective-lapse ratio crossing its reference, the clawback
  window's end, the select period's end, the last covered month.  Every switch that ships
  off is on, and five variants of S's points, in a copy of S's table, add an annual payer,
  the family income benefit commuted in part, an indexed waiver point, the decreasing
  shape at a zero schedule rate and a joint life who smokes.
* T3, future new business: a point issued ``k`` months after the valuation date is S's
  projection ``k`` months on, with zeros before issue and no rate evaluated there.
* D11's R1 and R2, and D3's and D5's chains: on the splice's grid no cell is called at a
  negative month, none on the books reads a month before them, and none reads beyond
  ``t + 1``; on the committed points no recursion runs backward over the frame; the policy
  clock is a closed form; and each chain, called cold, runs one cell a month back to
  ``t_entry()``, at the contract's longest cover.
* T4, the count algebra: the count rolls forward through new business and decrements,
  ``result_pols`` is S's report with the new business beside it, multiplying
  ``policy_count`` by 2.5 with every switch that ships off switched on multiplies every
  flow and every counted cell by 2.5 and moves no per-policy value, and the checks, whose
  tolerances scale with the count, close on a million policies.
* T5, validation: each malformed row of the table or of the pipeline is refused as it is
  read, naming its point or its line, and a waiver point whose waived and deferred shares
  sum past 1, naming the point; each assumption table, malformed or holding a value that
  is not a number in its range, is refused before a value of it is read, naming its
  lines, and a read beyond one is refused naming the point; the future horizon is a
  Reference that bounds future business; a point past its cover, one the contract does
  not issue, one whose pipeline is not exactly its lags, one with a share waived before
  the deferred period has run and a waiver point under a waiver rate outside 0 to 1 are
  refused by the frame, each bound just inside it; at waiver rates inside 0 to 1, their
  worst among them, the waived share stays inside 0 to 1; the edges of the interface and
  of each bound are accepted; and so is every state ``Term_UK_S`` reaches, on each set of
  inputs on which those states differ.
* T6, regeneration: the committed ``model_point_table_sec.csv`` and ``wop_pipeline_sec.csv``
  are what the generator makes of ``Term_UK_S`` and its table as they stand.
* Then the product's own facts: the two clocks on the shipped points; the committed rows
  continuing their S points; each history column read rather than recomputed, the
  indexation factors, the streams in payment, the commission paid at issue and the
  waiver's pipeline, and a take-up, a commission rate and a recovery rate changed at the
  valuation date reaching back over no month already run (UKLIB-SEC-PLAN.md K14), and an
  RPI changed there making the increase of an anniversary that falls at the valuation
  date, month 0's own event (USLIB-SEC-PLAN.md D6, precised at its M7), and the lapse
  ratio's cohort; expense inflation on the valuation clock;
  acquisition and the initial commission on new business, renewal commission and the
  clawback on the policy clock, and an annual premium on the anniversary; the cap on
  mortality and a NaN that reaches a bound; the values outside cover; the block; an
  in-force extract; the runner; the cells' defaulted parameters; the docstrings; the
  shared input tables; and what the default grid reaches.
* The C step's representation, in modelx: the claims total, a code of its own, is S's
  total to the last bit; the ledger's residual is S's too, its sum of the deaths ``sum``'s
  where it compensates, as from Python 3.12: Python 3.11's ``sum`` adds left to right, and
  there S's residual parts from this one, so its bits skip, naming 3.11, and the rest is
  held; each decode is S's reading of its text, on every value a column can hold; each
  padded array holds NaN where no file does, and its one reader refuses a key outside it;
  each ``Data`` vector is the int64 or float64 its docstring states; each parameterless
  cell returns a Python number; the spec's sizes and the sample's recursion limit are
  what their comments derive; and what the vectors cannot hold, or a cell cannot take, is
  refused.
* C2, the fingerprint: every committed point computes what the model computed when its E
  step ended, frozen at the end of this module before its C step changed anything
  (USLIB-SEC-PLAN.md §5.4), and refrozen once since, when both models' waiver came to take
  its incidence from the active lives alone, which moved the four waiver points and
  nothing else.
* Compiled, the tests marked ``cython``, after the fingerprint: C4 on the splice grid, at
  the contract's extremes, where the cap on mortality binds and on keys written as floats,
  each with the model's ``also``, every code no swept cell reads and both lives of every
  cell of a life, which a test holds to the codes and lives each cell takes in modelx,
  row by row, and another to leaving no call of a life uncompared; each life's label that
  is not text; the refusals; the deepest cold call on a 1 MiB stack; a Reference set
  late; and the runner.  ``test_compiled_conventions_uk.py`` holds C3, C4 on the
  committed points, with the same ``also``, and the release.

SEC month ``t`` is S month ``t + source_mth`` throughout, the direction in which
``uk_sec_support`` takes its ``t_offset``: ``d`` for a point restated at S month ``d``, 60
for the twin of S's point 8, ``-k`` for one issued ``k`` months on.

**The core grid and the full one** (UKLIB-SEC-PLAN.md U6).  T2 and T3 over every S point
at every month, about 150 cases, run by default on a core, chosen so that between them they
reach every branch, every opening-state column, every kind of valuation month and both
sides of every ``min`` and ``max`` the full grid reaches, which
``test_the_core_grid_reaches_every_branch`` asserts.  The other cases, and the rules
test's scan of their rows, carry the ``sec_full`` marker and are skipped, with the reason
shown, unless ``UKLIB_SEC_FULL=1`` is set.  They are never dropped: one leg of the CI
matrix sets it, and ``UKLIB_SEC_FULL=1 python -m pytest -m sec_full
lifelib/libraries/uklib/tests/test_term_assurance_uk_sec.py`` runs them alone.  Each
splice row is released once it has been read (``_release``), as ``run_sec.py --block``
releases its points.

Every test keeps four rules.  Each model is read under a name of its own and closed:
``conftest.term_assurance`` reads S under its default name, and reading a model under a
name in use renames the open one.  No test writes inside the library tree: every changed
input goes through ``uk_sec_support.temp_inputs`` into a temporary directory, because a
CSV added beside the models, even briefly, would fail a concurrent
``test_every_csv_beside_the_model_is_actually_read``.  No test indexes ``Projection`` by
hand: the keys come from ``uk_registry.point_keys`` and the ItemSpaces from
``uk_registry.projection``, and a generated row is found by what it is, its kind, its S
policy and its month (``_row``), so neither a renumbered table nor the C step's positions
can point a test at the wrong row.  And a timing or a kind is passed through ``_code``,
which gives the model's int Reference of its name where the model has one, as at stage
``"EC"`` it does, and the string at stage ``"E"``; every comparison with S passes
``uk_sec_support.codes``, ``{}`` at stage ``"E"``, and the spec's ``twin_arg_map``,
which turns S's ``claims(t, None)``, its total, into ``claims(t, ALL)``.
"""
import ast
import dataclasses
import errno
import importlib.machinery
import inspect
import io
import itertools
import json
import math
import os
import pathlib
import pickle
import re
import shutil
import subprocess
import sys
import types
import warnings

import modelx as mx
import numpy as np
import pandas as pd
import pytest

from uk_registry import model_path, point_keys, projection
from uk_sec_support import (
    SEC_SPECS, TWIN_EXEMPT_DEFAULT, build_sec_table, check_generated,
    codes, fingerprint_mismatches, frame_mismatches, full_sweep, sweep, temp_inputs,
    twin_mismatches)
from uk_sec_support import (
    compiled_case, compiled_mismatches, exact_here, reporting_cells, run_compiled)
from uk_sec_support import (
    _TERM_CODED, _TERM_LIVES, _LIVES, _term_c4_also, c4_expected)
from uk_sec_support import generated_columns

SEC, TWIN = "Term_UK_SEC", "Term_UK_S"
TABLE, PIPELINE = "model_point_table_sec.csv", "wop_pipeline_sec.csv"
SPEC = SEC_SPECS[SEC]

# S's seven new-business points: the anchor cell level (1), decreasing (2), the family
# income benefit uncommuted (3) and commuted whole (4), indexed (5), joint first death (6)
# and the select basis with the waiver of premium (7), a 20-year term; and point 8, the
# anchor cell in force five years, which S opens at its own month 60.
S_POINTS = (1, 2, 3, 4, 5, 6, 7)

# T2's months (UKLIB-SEC-PLAN.md §6.1): the second month; 6 and 7, the months either side
# of the waiver's first entrants, whose deferred period is six months; 11, 12 and 13 about
# the first anniversary, where renewal commission starts, an annual premium falls due and
# the index steps; 22 and 23, where the selective-lapse ratio crosses its reference under
# the splice's References, and 30, where it crosses at the loading alone; 47 and 48, the
# clawback window's end; 59 and 60, the select period's end and the ultimate lapse rate;
# 66, mid-year after them; 120; 239, the waiver point's last month; and 299, the last month
# of a 25-year term.  A month at or past a point's cover is left out.  S's in-force point 8
# is restated too, at months after its own 60.  T3's: issued one month on, which puts the
# policy anniversaries a month off the valuation years, and twelve, which puts them back
# on; and later, more than a year after the valuation date (USLIB-SEC-PLAN.md §7.1,
# *Record — M14*, *Splice grid*).
SPLICE_MTHS = (1, 6, 7, 11, 12, 13, 22, 23, 30, 47, 48, 59, 60, 66, 120, 239, 299)
IN_FORCE_MTHS = {8: (66, 120, 299)}
FUTURE_MTHS = (1, 12)
LATE_FUTURES = ((7, 13), (5, 25))

# Five more S points, in the splice's copy of S's table and never in the committed one,
# each one of S's points changed so as to reach what S's own points cannot:
#
# 9, S point 5, the indexed point, paying annually and a smoker: an annual premium falls
#   due on each anniversary, on the policy clock, indexed there, and the male smoker's
#   rates, which no S point reads;
# 10, S point 3 with half of each family income benefit claim commuted: the lump sum and
#   the instalments both, where S's points take one or the other;
# 11, S point 7, the waiver point, indexed: the waiver's loading on an indexed premium, and
#   an indexed point on the select basis;
# 12, S point 2, decreasing, at a schedule rate of 0: the straight line, which the closed
#   form cannot express;
# 13, S point 6, joint, with a male smoker as its second life.
#
# Each variant is (the S point it changes, the columns it changes); the policy_id keeps
# the generated ids apart.
VARIANTS = {
    9: (5, {"policy_id": "TA-900009", "premium_mode": "annual", "smoker": "S"}),
    10: (3, {"policy_id": "TA-900010", "fib_commute_rate": 0.5}),
    11: (7, {"policy_id": "TA-900011", "indexation": True}),
    12: (2, {"policy_id": "TA-900012", "sched_rate": 0.0}),
    13: (6, {"policy_id": "TA-900013", "joint_sex": "M", "joint_smoker": "S"}),
}
VARIANT_MTHS = {9: (1, 11, 12, 13, 66), 10: (12, 66), 11: (1, 6, 7, 12, 30, 239),
                12: (12, 299), 13: (12, 120)}


def _s_table():
    """S's committed table, indexed by point_id."""
    return pd.read_csv(model_path(TWIN).parent / "model_point_table.csv",
                       index_col="point_id")


def _s_table_with_variants():
    """S's committed table with the :data:`VARIANTS` appended, under their own point_ids."""
    table = _s_table()
    rows = []
    for point_id, (base, changes) in VARIANTS.items():
        row = table.loc[[base]].assign(**changes)
        row.index = pd.Index([point_id], name="point_id")
        rows.append(row)
    return pd.concat([table, *rows])


# The months of cover from issue of each S point and variant, 12 times its term.
COVER = {p: 12 * int(n) for p, n in _s_table_with_variants()["policy_term"].items()}

# T2's cases, as (row_kind, S point, source_mth): each S point restated in force at each
# of its months, then the twin of S's own in-force row, which is a splice case too (§5),
# aligned at its source_mth, the first row of its S frame.  T3's cases, as (S point, k).
SPLICES = (tuple(("derived", p, d) for p in S_POINTS for d in SPLICE_MTHS if d < COVER[p])
           + tuple(("derived", p, d) for p, mths in IN_FORCE_MTHS.items() for d in mths)
           + tuple(("derived", p, d) for p, mths in VARIANT_MTHS.items() for d in mths))
IN_FORCE_TWINS = (("twin", 8, 60),)
FUTURES = (tuple((p, k) for p in S_POINTS for k in FUTURE_MTHS)
           + tuple((p, 1) for p in VARIANTS) + LATE_FUTURES)

# The default run's cases (the module docstring), each with what it is there for.  The
# rest of SPLICES and FUTURES run with UKLIB_SEC_FULL=1.
CORE_SPLICES = {
    ("twin", 8, 60): "S's in-force row, opened where S opens it",
    ("derived", 8, 66): "S's in-force row restated mid-year",
    ("derived", 1, 1): "the anchor cell in its second month",
    ("derived", 1, 11): "the anchor cell in the month before its first anniversary",
    ("derived", 1, 12): "the anchor cell on its first anniversary: renewal commission",
    ("derived", 1, 22): "the lapse ratio just below its reference",
    ("derived", 1, 23): "the lapse ratio just past its reference",
    ("derived", 1, 47): "the clawback window's last month",
    ("derived", 1, 48): "the first month past the clawback window",
    ("derived", 1, 299): "the anchor cell in its last covered month",
    ("derived", 2, 60): "decreasing on the select period's end",
    ("derived", 2, 299): "decreasing in its last month",
    ("derived", 3, 13): "the family income benefit after its first anniversary",
    ("derived", 3, 66): "the family income benefit mid-year, streams in payment",
    ("derived", 4, 120): "the family income benefit commuted whole",
    ("derived", 5, 12): "indexed on its first anniversary: the step at t = 0",
    ("derived", 5, 60): "indexed on its fifth anniversary",
    ("derived", 5, 66): "indexed mid-year: the factors of the year under way",
    ("derived", 6, 120): "joint first death",
    ("derived", 7, 1): "the waiver one month into its deferred period",
    ("derived", 7, 6): "the waiver's deferred period full, no entrant yet",
    ("derived", 7, 7): "the waiver's first entrants at t = 0",
    ("derived", 7, 13): "the waiver past its first anniversary, a share waived",
    ("derived", 7, 59): "the select basis in its last select year",
    ("derived", 7, 60): "the select basis on its ultimate rates",
    ("derived", 7, 239): "the waiver point in its last covered month",
    ("derived", 9, 11): "an annual payer the month before its anniversary",
    ("derived", 9, 12): "an annual payer on its anniversary: a premium at t = 0, indexed",
    ("derived", 9, 66): "an annual payer mid-year, a male smoker",
    ("derived", 10, 66): "the family income benefit commuted in part",
    ("derived", 11, 7): "an indexed waiver point at its first entrants",
    ("derived", 11, 30): "an indexed waiver point after its anniversaries",
    ("derived", 12, 12): "decreasing in a straight line",
    ("derived", 13, 120): "joint with a male smoker as the second life",
}
CORE_FUTURES = {
    (1, 1): "issued a month off the valuation anniversaries",
    (1, 12): "issued on them, a year on",
    (3, 1): "the family income benefit",
    (6, 12): "joint first death",
    (7, 13): "the waiver point, more than a year on",
    (5, 25): "indexed, more than two years on",
    (9, 1): "an annual payer",
    (11, 1): "an indexed waiver point",
}

SEC_FULL = os.environ.get("UKLIB_SEC_FULL") == "1"
FULL_ONLY = (pytest.mark.sec_full,
             pytest.mark.skipif(not SEC_FULL, reason="the full splice grid runs with "
                                "UKLIB_SEC_FULL=1 (UKLIB-SEC-PLAN.md U6)"))

# What the splice sets in both models, S and SEC alike, before either evaluates anything.
# Expense inflation is the one input Term reads on the valuation clock (D7): S inflates
# from issue and SEC from the valuation date, so at the shipped 3% the expenses of a point
# opened at d differ by 1.03^(d // 12), by design, and at 0 both factors are 1.  The clock
# itself is then asserted on its own, at the shipped rate.  There is no scenario table and
# no mortality improvement, so no input table moves with d.  The rest are switches that
# ship off, each of which hides some of the state from any comparison:
#   sel_lapse_lambda, the selective-lapse loading, without which the lapse ratio and the
#     cohort it is a share of reach no number;
#   premium_market_ratio, at 1.25, for a rebroking multiplier of 1.25, so that its cell
#     is reached on the side of its max that is not 1;
#   clawback_mths, at 48, the notes' four-year rule, without which the clawback window,
#     read on the policy clock, is never open.
# The identity does not depend on the values, only on both models having the same ones.
SPLICED_REFS = {"inflation_rate": 0.0, "sel_lapse_lambda": 0.25,
                "premium_market_ratio": 1.25, "clawback_mths": 48}

# The splice's switches, for T4, at the shipped inflation.
SWITCHED_ON = {ref: value for ref, value in SPLICED_REFS.items() if ref != "inflation_rate"}

# The cells T2 and T3 skip beyond T1's, which already drop result_pols as a whole and S's
# proj_start and duration_inforce, cells this model does not have (the spec's exempt).
# proj_len counts from the valuation date on SEC and from issue on S, so it differs by d,
# or by -k, by design; frame_mismatches asserts what it must get right, that both frames
# end at the same instant.  Both tests compare result_pols column by column instead.
SPLICE_EXEMPT = TWIN_EXEMPT_DEFAULT | SPEC.exempt | {"proj_len"}
FUTURE_EXEMPT = SPLICE_EXEMPT

# The result_cf columns that expense inflation moves, and the cells they are made of: on
# the committed points, at the shipped 3%, the only places an in-force row departs from S.
INFLATED = ("expenses", "net_cf")
INFLATION_CELLS = frozenset({"inflation_factor", "expenses", "net_cf", "result_cf"})

# The S cells whose exact value is 0 and whose computed value is rounding about it, the two
# residuals: a comparison with S holds them at the harness's absolute floor of 1e-9, and
# every other cell at none (_compare).
RESIDUALS = frozenset({"check_pols_roll_fwd_resid", "check_fib_ledger_resid"})

# The decrement rates and the reads keyed by a select duration or an attained age, none of
# which may be evaluated before issue (R1, D4).
DECREMENT_RATES = ("select_factor", "mort_rate_base", "mort_rate_life", "mort_rate",
                   "mort_rate_mth", "lapse_rate_base", "lapse_rate", "lapse_rate_mth")

# The cells that scale with policy_count.  Every other cell is a per-policy amount, a rate,
# a ratio, a clock or a flag, and must not move when the count does.
COUNTED = frozenset({
    "policy_count", "pols_if_init", "pols_if", "pols_if_at", "pols_new_biz",
    "pols_death", "pols_lapse", "pols_maturity", "pols_payer", "fib_cum", "fib_streams",
    "premiums", "claims", "claim_expenses", "expenses", "comm_clawback", "commissions",
    "net_cf",
    "check_pols_roll_fwd_resid", "check_fib_ledger_resid", "result_cf", "result_pols"})

# result_pols' columns, in its order: the count, the new business within it, the month's
# deaths and lapses in processing order, the expiries of the last covered month, then S's
# other four: the payers, the FIB ledger and the two monthly rates, which no count moves.
RESULT_POLS = ["pols_if", "pols_new_biz", "pols_death", "pols_lapse", "pols_maturity",
               "pols_payer", "fib_cum", "mort_rate_mth", "lapse_rate_mth"]
OUTFLOWS = RESULT_POLS[2:5]
RATES = RESULT_POLS[7:]

# S's three timings and BEF_NB, the one running in force adds; and the kinds, with ALL,
# their total, S's kind=None, in their numbering's order (the Projection docstring's
# *Codes*).
TIMINGS = ("BEF_NB", "BEF_DECR", "BEF_LAPSE", "AFT_DECR")
KINDS = ("DEATH", "FIB", "LAPSE", "ALL")

# What each cell holds outside cover, before issue and from the month cover has ended, as
# its docstring says: no count, so no cash flow; no factor, no ratio, no ledger and no
# waiver; no rate read at a select duration, a policy year or an age the policy does not
# have.  The type is part of the value.  A count is a float in every branch and a flag a
# bool, because the C step types a cell by the values it returns (USLIB-SEC-PLAN.md F3).
# The guard test also calls pols_if_at at each timing, claims at each kind and at ALL, and
# mort_rate_base at each life the point has, all 0.0: mort_rate_base takes its life with
# no default, so it is called with one, as every caller calls it.
OUTSIDE_COVER = {
    "is_active": False, "select_factor": 0.0,
    "lapse_rate_base": 0.0, "lapse_cum": 0.0, "cohort_frac": 0.0, "fib_cum": 0.0,
    "fib_streams": 0.0,
    "wop_active_frac": 0.0, "wop_waived_frac": 0.0, "idx_factor": 0.0,
    "idx_prem_factor": 0.0, "premium_pp": 0.0,
    "fib_commute_pp": 0.0, "benefit_pp": 0.0,
    "pols_if": 0.0, "pols_new_biz": 0.0, "pols_death": 0.0, "pols_lapse": 0.0,
    "pols_maturity": 0.0, "pols_payer": 0.0, "premiums": 0.0,
    "claim_expenses": 0.0, "expenses": 0.0, "comm_clawback": 0.0, "commissions": 0.0,
    "net_cf": 0.0}

# The cells a month outside cover may not reach: the clocks of the contract, the rates and
# the schedules, each keyed by a policy month, a select duration or an attained age.  The
# reads that guard themselves are held by their values in OUTSIDE_COVER instead.
IN_COVER_ONLY = ("age", "duration", "policy_year", "benefit_sched", "annuity_certain_factor",
                 "mort_rate_life", "mort_rate", "mort_rate_mth", "sel_lapse_factor",
                 "lapse_rate", "lapse_rate_mth", "wop_deferred_init")

# The opening state, in the table's order, and the cells running in force adds to
# Term_UK_S's, then those compiling adds, the label and the decoded columns, each of which
# the symbol map must name.
STATE = ("lapse_cum_init", "fib_cum_init", "fib_streams_init", "idx_factor_init",
         "idx_prem_factor_init", "wop_waived_frac_init", "comm_init_pp_init")
NEW_CELLS = ("policy_count", "duration_mth_init", "t_entry", "is_active", "pols_new_biz",
             *STATE, "wop_deferred_init", "cohort_frac", "fib_streams",
             "point_id", "is_level", "is_decreasing", "is_fib", "prem_cycle",
             "is_select_basis", "mort_group")

INFLATION = 0.03        # the shipped inflation_rate, which the inflation test reads

# The recursion limit, as mx.set_recursion takes it, under which the committed points are
# first swept (R2, F7).  A report evaluates each column in ascending t, so a forward
# recursion, through t - 1, finds the month before already cached: the committed points'
# sweep runs 11 cells deep at most, and passes under a limit of 10 (measured at M1).  A
# backward recursion over the frame, through t + 1, opens a chain as long as the frame,
# and the shortest committed frame longer than a month is 174.
CALL_DEPTH = 40

# The reads beyond t + 1 the model makes, as (reader, cell read): none.  The rules test
# admits no other.
LOOK_AHEAD = frozenset()


# ---------------------------------------------------------------------------
# Helpers

_names = itertools.count(1)


def _name(tag):
    """A model name that no other read in this session uses."""
    return f"{SEC}_{tag}_{next(_names)}"


def _key(model, point_id):
    """The registry's key for the row labelled ``point_id`` (``uk_registry.point_keys``)."""
    return dict(zip(model.Data.model_point_table().index, point_keys(model)))[point_id]


def _point(model, point_id):
    """The ItemSpace of the row labelled ``point_id``, through the registry's keys."""
    return projection(model, _key(model, point_id))


def _label(table, kind, s_point, month):
    """The ``point_id`` of the one ``kind`` row generated from S point ``s_point``.

    ``month`` is the row's ``source_mth``: 0 for a new-business twin, 60 for the twin of
    S's point 8, ``d`` for a derived row, ``-k`` for a future one.  The twins keep S's
    ``point_id`` and ``policy_id``, so the S policy is the twin's.
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


def _release(model, key):
    """Drop the ItemSpace at ``key``, the registry's key, and every value it has cached.

    Each splice row is needed once, so each is released when read, as ``run_sec.py
    --block`` releases its points (USLIB-SEC-PLAN.md F5).  Asked for again, the ItemSpace
    is made afresh and recomputes.
    """
    del model.Projection[key]


def _code(proj, label):
    """The argument that selects timing or kind ``label``: the model's int Reference of
    that name where it has one, as at stage ``"EC"``, else the string, as at ``"E"``."""
    value = proj.refs.get(label) if label in proj.refs else None
    return value if isinstance(value, int) and not isinstance(value, bool) else label


def _committed():
    """The committed SEC table as the file holds it, unvalidated, indexed by point_id."""
    return pd.read_csv(model_path(SEC).parent / TABLE, index_col="point_id")


def _committed_pipeline():
    """The committed pipeline as the file holds it, unvalidated, on a default index."""
    return pd.read_csv(model_path(SEC).parent / PIPELINE)


def _sec_inputs(tmp_path, table, pipeline=None, edits=None):
    """A copy of the product directory whose SEC table is ``table``, and whose pipeline is
    ``pipeline`` (the committed one where ``None``), other inputs changed by ``edits``, as
    :func:`uk_sec_support.temp_inputs` takes them; its SEC folder."""
    edits = dict(edits or {})
    if pipeline is not None:
        edits[PIPELINE] = pipeline
    return temp_inputs(tmp_path, model_path(SEC), model_points=table,
                       model_point_file=TABLE, edits=edits)


def _read_edited(tmp_path, edit, pipeline_edit=None, edits=None):
    """Term_UK_SEC read from a copy whose SEC table is ``edit(_committed())`` and whose
    pipeline is ``pipeline_edit(_committed_pipeline())``."""
    pipeline = None if pipeline_edit is None else pipeline_edit(_committed_pipeline())
    folder = _sec_inputs(tmp_path, edit(_committed()), pipeline, edits)
    return mx.read_model(folder, name=_name("edited"))


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


def _then(*edits):
    """One edit made of ``edits``, applied in turn."""
    def edit(table):
        for each in edits:
            table = each(table)
        return table
    return edit


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


def _sweep_s(proj):
    """Evaluate on an S point what the splice compares: the sweep, and two cells more.

    :func:`uk_sec_support.sweep` reaches ``Term_UK_S``'s ``pols_if_at(t, "BEF_DECR")``
    nowhere, since S's ``pols_if`` is a recursion of its own, and ``duration_mth`` only on
    the decreasing shape, whose schedule it keys; a cell S never evaluates is compared
    nowhere.  They are evaluated here over the frame, so the splice and the future
    comparison see them too.
    """
    sweep(proj)
    for t in range(proj.proj_start(), proj.proj_len()):
        proj.pols_if_at(t, "BEF_DECR")
        proj.duration_mth(t)


def _mismatches(s_proj, sec_proj, **kwargs):
    """:func:`uk_sec_support.twin_mismatches` of an S point and an SEC row, the one place
    this module calls it.

    It passes the SEC Space's :func:`uk_sec_support.codes`, which map S's timing and kind
    strings to the int codes the C step gives them, and the spec's ``twin_arg_map``, which
    maps S's ``claims(t, None)``, its total, onto SEC's ``ALL`` and passes SEC's own keys
    unchanged.  Every comparison of a row with S goes through here, so each takes the C
    step's codes and map (USLIB-SEC-PLAN.md §7.1, *Record -- M14*, *Carried into Phase 1*).
    """
    return twin_mismatches(s_proj, sec_proj, codes=codes(sec_proj),
                           arg_map=SPEC.twin_arg_map, **kwargs)


def _compare(s_proj, sec_proj, month, exempt, columns=None):
    """Where SEC's row departs from S's point from S month ``month`` on, in two passes.

    First the frames, ``result_cf`` (over ``columns``, or every column both hold) and
    ``result_pols``, SEC row ``t`` against S row ``t + month``, frames ending together;
    then every cell of S's but ``exempt`` and :data:`RESIDUALS`, at every argument S cached
    inside its frame from ``month`` on, moved onto SEC's clock, S's timing and kind strings
    mapped onto SEC's codes and its total onto ``ALL`` (:func:`_mismatches`).  Both to
    1e-9 relative with no
    absolute floor (USLIB-SEC-PLAN.md §5.2, T2, precised at M11): a floor of 1e-9 passes an
    error of 1% in any value below 1e-7, and the counts late in a long frame, under the
    splice's switches, fall below 1e-3.  Then the cells of :data:`RESIDUALS` alone, at the
    floor of 1e-9: their exact value is 0, and the computed one moves by an ulp of what it
    closes when an opening state comes back from the CSV one ulp off.  Returns the mismatch
    lines, empty when the row is S's.
    """
    found = []
    for report, keep in (("result_cf", columns), ("result_pols", None)):
        found += [f"{report}: {line}" for line in frame_mismatches(
            s_proj.cells[report](), sec_proj.cells[report](), t_offset=month,
            columns=keep, atol=0.0)]
    found += _mismatches(s_proj, sec_proj, t_offset=month, exempt=exempt | RESIDUALS,
                         atol=0.0)
    return found + _mismatches(s_proj, sec_proj, t_offset=month,
                               exempt=exempt | (set(s_proj.cells) - RESIDUALS))


def _continues_s(s_proj, sec_proj, month):
    """Where a committed row departs from S's point ``s_proj`` from S month ``month`` on.

    The splice's comparison (:func:`_compare`), on the committed model at the shipped
    assumptions: frame by frame, ``result_cf`` and ``result_pols``, then cell by cell over
    every cell of S's but :data:`SPLICE_EXEMPT`.  The shipped 3% expense inflation runs
    from issue in S and from the valuation date here (D7), so :data:`INFLATED`'s two
    columns, and :data:`INFLATION_CELLS`, differ by design and are left out; the inflation
    test holds them.  Every other column and cell must agree, to 1e-9 relative, with no
    absolute floor but on the residuals.
    """
    keep = [c for c in s_proj.result_cf().columns if c not in INFLATED]
    return _compare(s_proj, sec_proj, month, SPLICE_EXEMPT | INFLATION_CELLS, keep)


def _case_id(kind, s_point, month):
    """A case's id: ``point2-d12``, ``point8-twin60``, or ``point2-k3`` if issued later."""
    if kind == "future":
        return f"point{s_point}-k{-month}"
    return f"point{s_point}-" + (f"d{month}" if kind == "derived" else f"{kind}{month}")


def _case(case, core, case_id):
    """One parametrized case: run by default if it is in ``core``, else on the full grid."""
    return pytest.param(*case, id=case_id, marks=() if case in core else FULL_ONLY)


def _selected(cases, core):
    """The cases this run makes rows for: the core, or every one under UKLIB_SEC_FULL."""
    return [case for case in cases if SEC_FULL or case in core]


# Every row the splice compares, as (row_kind, S point, source_mth), T3's included, and the
# default run's among them.
GRID = (*SPLICES, *IN_FORCE_TWINS, *(("future", p, -k) for p, k in FUTURES))
CORE_GRID = frozenset({*CORE_SPLICES, *(("future", p, -k) for p, k in CORE_FUTURES)})


# ---------------------------------------------------------------------------
# Fixtures


@pytest.fixture(scope="module")
def sec_read():
    """Term_UK_SEC read in place, as committed, and swept once, cold; what it met.

    The model is first asked for ``duration_mth(500)`` on the twin of S point 1, and the
    keys that call leaves in ``duration_mth`` are kept.  Then every committed point is
    swept (:func:`uk_sec_support.sweep`: ``result_cf``, the other reports and the checks),
    in table order and each column in ascending ``t``, under a recursion limit lowered to
    :data:`CALL_DEPTH`, and whatever that raises is kept, point by point, rather than
    raised.  So the record says what a cold model does, which the clock and depth test
    asserts (D3, R2), and every test on the committed model reads a model already swept:
    the sweep is paid once, not once for each.  Returns ``(model, record)``.
    """
    model = mx.read_model(model_path(SEC), name=_name("sec"))
    first = _row(model, "twin", 1, 0)
    record = {"duration_mth(500)": first.duration_mth(500),
              "keys": list(first.cells["duration_mth"].keys()), "deep": []}
    labels = model.Data.model_point_table().index
    limit = mx.get_recursion()
    mx.set_recursion(CALL_DEPTH)
    try:
        for key, point_id in zip(point_keys(model), labels):
            try:
                sweep(projection(model, key))
            except Exception as err:            # kept, so every point is swept
                record["deep"].append(f"point {point_id}: the sweep raised {_raised(err)}")
    finally:
        mx.set_recursion(limit)
    yield model, record
    model.close()


@pytest.fixture(scope="module")
def sec_model(sec_read):
    """Term_UK_SEC read in place, as committed, with every point swept (sec_read)."""
    return sec_read[0]


@pytest.fixture(scope="module")
def s_model():
    """Term_UK_S read in place, as committed, with every point swept.

    T6 regenerates the SEC inputs from it, which would otherwise project every S point
    again (USLIB-SEC-PLAN.md §4, *Carried into Phase 1*), and the in-force tests read S's
    months off it.
    """
    model = mx.read_model(model_path(TWIN), name=_name("s"))
    for key in point_keys(model):
        _sweep_s(projection(model, key))
    yield model
    model.close()


@pytest.fixture(scope="module")
def spliced(tmp_path_factory):
    """S and SEC on the splice's inputs, with :data:`SPLICED_REFS` set in both.

    S is read from a copy of the product directory whose table has the variants appended.
    SEC runs on the same assumption tables, and on a model point table and a pipeline of
    its own, built by the generator from the registered spec with its rows replaced by the
    cases this run selects, the core or the full grid (:func:`_selected`), out of this S
    model, so each row opens with the state of the very run it is compared with.  No input
    table moves with ``d``: Term's one valuation-clock input is the ``inflation_rate``
    Reference.  Every S point is then swept (:func:`_sweep_s`), and stays swept; each SEC
    row is projected by the case that compares it and released once compared
    (:func:`_settle`).
    """
    root = tmp_path_factory.mktemp("spliced")
    s_folder = temp_inputs(root / "s", model_path(TWIN),
                           model_points=_s_table_with_variants())
    s = mx.read_model(s_folder, name=_name("s_spliced"))
    for ref, value in SPLICED_REFS.items():
        setattr(s.Projection, ref, value)
    derived = [(p, d) for kind, p, d in _selected(SPLICES + IN_FORCE_TWINS, CORE_SPLICES)
               if kind == "derived"]
    spec = dataclasses.replace(SPEC, derived=tuple(derived),
                               future=tuple(_selected(FUTURES, CORE_FUTURES)))
    table, companions = build_sec_table(spec, s)
    assert set(companions) == {PIPELINE}
    sec_folder = _sec_inputs(root / "sec", table, companions[PIPELINE])
    sec = mx.read_model(sec_folder, name=_name("sec_spliced"))
    for ref, value in SPLICED_REFS.items():
        setattr(sec.Projection, ref, value)
    for key in point_keys(s):
        _sweep_s(projection(s, key))
    yield s, sec
    sec.close()
    s.close()


@pytest.fixture(scope="module")
def splice_records():
    """What each splice row was found to do once compared, by case (:func:`_settle`)."""
    return {}


# ---------------------------------------------------------------------------
# The splice's records
#
# Each T2 and T3 case compares its row with S, then records what the rules test and the
# core grid's reach need of the row, and releases it (_settle).  So each of the two tests
# reads the records, and computes any case no earlier test has recorded, which keeps it
# whole when run alone.


def _cached_args(cells):
    """The argument tuple of every key ``cells`` has cached (uk_sec_support._args)."""
    n = len(cells.parameters)
    return [() if n == 0 else (key,) if n == 1 else tuple(key)
            for key in list(cells.keys())]


def _month(x):
    return isinstance(x, int) and not isinstance(x, bool)


def _rule_breaches(proj):
    """R1 and R2's look-ahead on one row, once it has run whole.

    The row's reports and checks are run (:func:`uk_sec_support.sweep`), and then every
    monthly cell at every month of the frame and the month after it, as the C step's sweep
    runs them (:func:`uk_sec_support.full_sweep`): no report of a row need read every
    state, and a base at ``t == 0`` would hide in a cell the reports leave unread
    (USLIB-SEC-PLAN.md §5.2, T2, precised at M4).  ``{"negative": [...], "early": [...],
    "ahead": [...], "raised": [...]}``: every cached call with a negative argument; every
    precedent keyed by a month before ``t_entry()`` of a call keyed by a month at or after
    it; every precedent keyed by a month beyond ``t + 1`` of a call keyed by ``t``, but
    :data:`LOOK_AHEAD`'s, which is empty; and every call the full sweep found raising.  A
    precedent is a call's as modelx's dependency graph records it.
    """
    sweep(proj)
    raised = [f"{name}{args}: {text}" for (name, args), text in full_sweep(proj).items()]
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
                if u <= t + 1 or (name, node.obj.name) in LOOK_AHEAD:
                    continue
                ahead.append(f"{name}{args} -> {node.obj.name}{node.args}")
    return {"negative": negative, "early": early, "ahead": ahead, "raised": raised}


def _excess(x, t):
    """The selective-lapse ratio less its reference in month ``t``, the max's argument."""
    return x.lapse_cum(t) - x.sel_lapse_ref


def _src(x, t):
    """The incidence month the waiver's entrants of month ``t`` come from."""
    return t - 1 - x.wop_defer_mths


def _anniversaries_before(x):
    """The anniversaries row ``x`` passed before month 0, whose increases its factors carry:
    those up to policy month ``duration_mth_init() - 1`` on a point in force, none on one
    issued at or after the valuation date.  An anniversary at the valuation date is month
    0's own event, the projection's (D6, precised at uslib's M7)."""
    return max(x.duration_mth_init() - 1, 0) // 12


# What test_the_core_grid_reaches_every_branch asks of the core's rows in the model's own
# values, which no column of the table shows: each holds of some core row, or of a core row
# in some month of its frame.  At the valuation date, every opening-state column in use,
# a factor apart from 1 and a ratio, a ledger, the streams, a waived share and a
# commission apart from 0, a deferred share in the pipeline, the pipeline both partly
# and wholly filled, and an anniversary's index step made at t = 0, the projection's
# first event.  Later in the frame, every branch and both sides of each
# min and max the full grid reaches: the select duration's min, the lapse table's last
# year, the selective-lapse excess's max, the waiver's three sources of entrants, the
# clawback window, an index step, the expiry.
AT_VALUATION = {
    "lapse_cum_init non-zero": lambda x: x.lapse_cum_init() != 0.0,
    "fib_cum_init non-zero": lambda x: x.fib_cum_init() != 0.0,
    "idx_factor_init above 1": lambda x: x.idx_factor_init() > 1.0,
    "idx_prem_factor_init above 1": lambda x: x.idx_prem_factor_init() > 1.0,
    "wop_waived_frac_init non-zero": lambda x: x.wop_waived_frac_init() != 0.0,
    "fib_streams_init non-zero": lambda x: x.fib_streams_init() != 0.0,
    "comm_init_pp_init non-zero": lambda x: x.comm_init_pp_init() != 0.0,
    "a deferred share in the pipeline": lambda x: (
        x.wop() and x.duration_mth_init() > 0
        and x.wop_deferred_init(1) > 0.0),
    "the pipeline partly filled": lambda x: (
        x.wop() and 0 < x.duration_mth_init() < x.wop_defer_mths),
    "the pipeline full": lambda x: x.wop() and x.duration_mth_init() >= x.wop_defer_mths,
    "a FIB stream in payment at t = 0": lambda x: (
        x.shape() == "fib" and x.claims(0, _code(x, "FIB")) > x.fib_income()
        * (1.0 - x.fib_commute_rate()) * x.pols_death(0)),
    "the lapse ratio past its reference at t = 0": lambda x: _excess(x, 0) > 0.0,
    "an index step at the valuation date": lambda x: (
        x.indexation() and x.idx_factor(0) > x.idx_factor_init()),
}
IN_FRAME = {
    "inside the select period": lambda x, t: (
        x.mort_basis() == "select" and x.duration(t) < x.select_period),
    "past the select period": lambda x, t: (
        x.mort_basis() == "select" and x.duration(t) >= x.select_period),
    "inside the lapse table": lambda x, t: (
        x.policy_year(t) <= x.data.lapse_last_year()),
    "past the lapse table's last year": lambda x, t: (
        x.policy_year(t) > x.data.lapse_last_year()),
    "the lapse ratio below its reference": lambda x, t: _excess(x, t) < 0.0,
    "the lapse ratio past its reference": lambda x, t: _excess(x, t) > 0.0,
    "entrants from the frame": lambda x, t: (
        x.wop() and t > x.t_entry() and _src(x, t) >= x.t_entry()),
    "entrants from the pipeline": lambda x, t: (
        x.wop() and t > x.t_entry() and _src(x, t) < x.t_entry()
        and x.duration_mth_init() + _src(x, t) >= 0),
    "no entrants, the incidence before issue": lambda x, t: (
        x.wop() and t > x.t_entry() and x.duration_mth_init() + _src(x, t) < 0),
    "a clawback inside the window": lambda x, t: x.comm_clawback(t) > 0.0,
    "past the clawback window": lambda x, t: (
        x.duration_mth(t) + 1 >= x.clawback_mths and x.pols_lapse(t) > 0.0),
    "an index step in the frame": lambda x, t: (
        x.indexation() and x.duration(t) > _anniversaries_before(x)),
    "a renewal commission": lambda x, t: (
        x.duration_mth(t) >= 12 and x.premiums(t) > 0.0),
    "an annual premium due": lambda x, t: (
        x.premium_mode() == "annual" and x.premium_pp(t) > 0.0),
    "an annual payer between premiums": lambda x, t: (
        x.premium_mode() == "annual" and x.is_active(t) and x.premium_pp(t) == 0.0),
    "the decreasing shape's straight line": lambda x, t: (
        x.shape() == "decreasing" and x.sched_rate() == 0.0),
    "a FIB claim commuted in part": lambda x, t: (
        x.shape() == "fib" and 0.0 < x.fib_commute_rate() < 1.0
        and x.claims(t, _code(x, "DEATH")) > 0.0 and x.claims(t, _code(x, "FIB")) > 0.0),
    "a second life": lambda x, t: x.is_joint() and x.mort_rate_life(t, 2) > 0.0,
    "the expiry": lambda x, t: x.pols_maturity(t) > 0.0,
}


def _branches(x):
    """The names in :data:`AT_VALUATION` and :data:`IN_FRAME` that hold of row ``x``."""
    reached = {what for what, holds in AT_VALUATION.items() if holds(x)}
    frame = range(x.t_entry(), x.proj_len())
    return reached | {what for what, holds in IN_FRAME.items()
                      if any(holds(x, t) for t in frame)}


def _settle(records, case, model, key):
    """Record what the rules and the core grid's reach need of a row, and release it.

    ``case`` is the row's (row_kind, S point, source_mth) and ``key`` its registry key in
    ``model``, the splice's SEC model.  A T2 or T3 case calls this once it has compared
    the row, whatever the comparison found, so the row is released either way.  The record
    is :func:`_rule_breaches`'s, with the row's :func:`_branches`, and a row that raises is
    recorded as raising, which the rules test reports.
    """
    try:
        proj = projection(model, key)
        record = _rule_breaches(proj)
        record["branches"] = _branches(proj)
        record["failed"] = None
    except Exception as err:                    # recorded, and reported by the rules test
        record = {"negative": [], "early": [], "ahead": [], "raised": [],
                  "branches": set(), "failed": _raised(err)}
    finally:
        _release(model, key)
    records[case] = record
    return record


def _record_of(spliced, records, case):
    """The record of ``case``, from the case that compared its row or, failing it, now."""
    if case not in records:
        sec = spliced[1]
        _settle(records, case, sec, _row_key(sec, *case))
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
    opening state is the issue value.  For the same reason it is the test that catches a
    policy month passed as ``t`` (R1a) and a look-back that stops at the wrong month.  The
    frame comparisons read SEC row ``t`` against S row ``t + d`` in every column of
    ``result_cf`` and every column of ``result_pols`` both reports hold, and fail frames
    that end apart.  The cell comparison then evaluates every cell of S's but
    :data:`SPLICE_EXEMPT`, at every argument S cached inside its own frame from month ``d``
    on, moved onto SEC's clock: the counts, the lapse ratio and its loading, the ledger,
    the waived share, the index factors and the schedules among them.  Each compares to
    1e-9 relative with no absolute floor, but the residuals, which keep the floor of 1e-9
    (:func:`_compare`).  An S cell this model lacked would fail it.

    The months 1 to 7 are the ones that see the waiver's pipeline read at the wrong lag:
    the entrants of the frame's first six months come from incidence before the valuation
    date.  The row is then recorded for the rules test and released (:func:`_settle`).
    """
    s, sec = spliced
    key = _row_key(sec, kind, s_point, month)
    s_proj, sec_proj = _point(s, s_point), projection(sec, key)
    try:
        assert _compare(s_proj, sec_proj, month, SPLICE_EXEMPT) == []
    finally:
        _settle(splice_records, (kind, s_point, month), sec, key)


# ---------------------------------------------------------------------------
# T3 -- future new business


@pytest.mark.parametrize(
    "s_point, k",
    [_case(case, CORE_FUTURES, _case_id("future", case[0], -case[1]))
     for case in FUTURES])
def test_future_new_business_is_the_s_projection_k_months_on(spliced, splice_records,
                                                             s_point, k):
    """Issued k months after the valuation date, the point is S's projection k months on.

    SEC rows ``k ..`` are S rows ``0 ..``, ending together at the end of the term, in
    ``result_cf`` and in every column of ``result_pols`` S's has, and every cell of S's but
    :data:`FUTURE_EXEMPT` agrees at every argument S cached inside its own frame, moved
    ``k`` later.  Each compares as the splice compares, with no absolute floor but on the
    residuals (:func:`_compare`).  An S cell this model lacked would fail it.  Before issue
    every column of ``result_cf`` and ``result_pols`` is an exact zero, and the policies
    arrive in month ``k`` as new business.

    The last assertions are R1 and D4's base rule made testable.  After the reports, no
    decrement rate or read keyed by a select duration or an age has been evaluated at a
    month before issue.  A count recursion based at ``t == 0`` rather than at
    ``t_entry()``, or a decrement count that evaluates its rate before asking whether the
    month is in cover, still gives the right numbers.  This is the only test that sees
    the first, and the guard test sees the second too.

    The pre-issue rows are asserted present before they are asserted zero, in both reports:
    a frame that opened at issue would have none, its zeros would hold of nothing, and the
    comparisons with S, which start at issue, would not see it.  The row is then recorded
    for the rules test and released (:func:`_settle`).
    """
    s, sec = spliced
    key = _row_key(sec, "future", s_point, -k)
    s_proj, sec_proj = _point(s, s_point), projection(sec, key)
    try:
        df, pols = sec_proj.result_cf(), sec_proj.result_pols()
        assert _compare(s_proj, sec_proj, -k, FUTURE_EXEMPT) == []
        for report, frame in (("result_cf", df), ("result_pols", pols)):
            assert list(frame.index[:k]) == list(range(k)), report
            assert (frame.loc[:k - 1] == 0.0).all().all(), report
        assert sec_proj.pols_new_biz(k) == sec_proj.policy_count() == 1.0
        early = {name: sorted(args[0] for args in _cached_args(sec_proj.cells[name])
                              if args[0] < k)
                 for name in DECREMENT_RATES}
        assert not any(early.values()), f"rates evaluated before issue: {early}"
    finally:
        _settle(splice_records, ("future", s_point, -k), sec, key)


# ---------------------------------------------------------------------------
# D11's R1 and R2, and D3's closed-form clock


@pytest.mark.parametrize("grid", [pytest.param("core", id="core"),
                                  pytest.param("full", id="full", marks=FULL_ONLY)])
def test_no_cell_is_called_before_the_valuation_date_or_reads_far_ahead(spliced,
                                                                        splice_records,
                                                                        grid):
    """R1, its look-back and R2's look-ahead, on the rows T2 and T3 compare: core or rest.

    Each is a rule of how the model computes, not of what, so no number shows a breach,
    and on a point issued at ``t = 0`` the two clocks coincide and hide it from T1 too.
    The splice's rows are points in force at every month T2 names, the variants among them,
    and points issued later, and on each the reports, the checks and the full sweep are run
    first (:func:`_rule_breaches`):

    * R1: no cell holds a negative argument.  modelx evaluates one without complaint, and
      a compiled cache raises ``IndexError`` below 0 (USLIB-SEC-PLAN.md F4).  A policy
      month turned into ``t`` by subtracting ``duration_mth_init()`` (R1a) goes negative
      on a point in force past it, and so does the waiver's incidence month read without
      the pipeline's branch.  The pipeline's lag and the schedules' policy months are
      held to it too.
    * R1's look-back stops at ``t_entry()``: no cell evaluated at a month from
      ``t_entry()`` on read a month before it.  On a point issued later a recursion based
      at ``t == 0`` reads the pre-issue zeros, so no number shows it and no argument goes
      negative.
    * R2's look-ahead: no cell evaluated at month ``t`` read a cell keyed by a month beyond
      ``t + 1``, as modelx's dependency graph records each cached call's precedents; this
      model admits none (:data:`LOOK_AHEAD`).
    * And no call of the full sweep raised.

    Each row was scanned by the T2 or T3 case that compared it (:func:`_settle`), and a row
    no case has scanned is scanned here.  The core case covers the core's rows, the full
    case every other row of the full grid, with ``UKLIB_SEC_FULL=1``.  The new-business
    twins in the splice's table are no case's, and are left out: on them the clocks
    coincide, and T1 compares them with S cell by cell.  The closed-form clock and the
    recursion depth are asserted on the committed model, in the tests after this one.
    """
    cases = [case for case in GRID if (case in CORE_GRID) == (grid == "core")]
    negative, early, ahead, raised, failed = [], [], [], [], []
    for case in cases:
        record, where = _record_of(spliced, splice_records, case), _case_id(*case)
        negative += [f"{where}: {call}" for call in record["negative"]]
        early += [f"{where}: {read}" for read in record["early"]]
        ahead += [f"{where}: {read}" for read in record["ahead"]]
        raised += [f"{where}: {call}" for call in record["raised"]]
        if record["failed"]:
            failed.append(f"{where}: {record['failed']}")
    assert cases, f"the {grid} grid has no rows"
    assert not failed, f"rows that raised: {failed[:10]}"
    assert not raised, f"calls the full sweep found raising: {raised[:10]}"
    assert not negative, f"called before the valuation date: {negative[:10]}"
    assert not early, f"read before issue from the books: {early[:10]}"
    assert not ahead, f"read beyond t + 1: {ahead[:10]}"


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
      stays shallow, which is why D3 is asserted on its own.  A backward recursion over the
      frame, through ``t + 1``, keeps every step within the look-ahead but opens a chain as
      long as the frame, which a compiled model would run on the C stack (F7), and fails
      here.
    """
    record = sec_read[1]
    assert record["duration_mth(500)"] == 500
    assert record["keys"] == [500]
    assert not record["deep"], f"under a recursion limit of {CALL_DEPTH}: {record['deep']}"


# How deep a cold call may run beyond its chain, one cell a month from its month back to
# t_entry() (D5): the cells above the chain and those below it, the first month's rates and
# Data's first reads of its tables.  A cold net_cf in the last month runs 11 cells beyond
# the count's chain, on every committed point and at the contract's longest cover alike,
# and each chain head called alone at most 8 beyond: the count, the lapse ratio and the
# cohort's share 6, the waived share 3, the ledger 8 (measured at M1).  On the family
# income benefit's point at its longest cover, the streams in payment run 8 beyond, its
# claims 10 and net_cf 11 (measured at M1's review).  The active share, which the waived
# share's incidence reads since both models were fixed to take it from the active lives,
# runs 3 beyond, and leaves the waived share at 3 and net_cf where they were: the waived
# share reads it after its own month before, one cell deep.  Term's 16, as for uslib's
# Term (USLIB-SEC-PLAN.md D5).  Any chain of two cells a month runs a frame's length
# beyond.
CHAIN_OVERHEAD = 16

# The contract's longest cover (product-spec.md, held by proj_len()): a 50-year term,
# policy_term_max, issued at issue_age_min, 18, which expires at 68, inside expiry_age_max.
LONGEST_TERM, YOUNGEST = 50, 18

# The family income benefit's longest cover: a 40-year term, policy_term_max_fib, issued
# at 30, which expires at 70, expiry_age_max_fib.
LONGEST_FIB_TERM, OLDEST_FIB = 40, 30

# Each chain of the model and the cell that heads it, called cold in the last month of the
# frame, each on a read of its own: (cell, the timing it takes, or None).  The count, the
# lapse ratio, the cohort's share in force, which the lapse ratio and the mortality it
# loads read, the active and the waived shares and the ledger.  On the waiver point, on
# the select basis with every switch on, every chain runs the frame's length.
CHAIN_HEADS = (("net_cf", None), ("pols_if_at", "BEF_NB"), ("lapse_cum", None),
               ("cohort_frac", None), ("wop_active_frac", None),
               ("wop_waived_frac", None), ("fib_cum", None))

# The chains the family income benefit's point adds, which return at once on the waiver
# point, a level shape: the streams in payment and the claims they pay, and net_cf over
# them.  Its count, lapse and ledger chains are those the waiver point measures.
FIB_CHAIN_HEADS = (("net_cf", None), ("claims", "FIB"), ("fib_streams", None))


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


def _longest_rows():
    """The waiver point and the family income benefit's point at their longest cover, an
    empty pipeline, and each row's frame, ``t_entry()`` and chain heads.

    S point 7's twin, the waiver point on the select basis, issued at 18 on a 50-year
    term, and S point 3's twin, the family income benefit, issued at 30 on a 40-year term,
    the longest its shape takes; each issued now and 120 months on, the shipped
    ``future_horizon_mth``: frames of 600 and 720 months, and of 480 and 600, whose chains
    stop at ``t_entry()``.  The shipped tables serve both: the mortality table runs from
    18, and the policies expire at 68 and 70.  Returns ``(rows, pipeline, frames)``.
    """
    committed = _committed()
    level, fib = _label(committed, "twin", 7, 0), _label(committed, "twin", 3, 0)
    top = committed.index.max()
    rows = committed.loc[[level, level, fib, fib]].assign(
        age_at_entry=[YOUNGEST, YOUNGEST, OLDEST_FIB, OLDEST_FIB],
        policy_term=[LONGEST_TERM, LONGEST_TERM, LONGEST_FIB_TERM, LONGEST_FIB_TERM],
    ).set_axis([level, top + 1, fib, top + 2]).rename_axis("point_id")
    rows = _set("duration_mth", [top + 1, top + 2], -120)(rows)
    empty = _committed_pipeline().iloc[0:0]
    frames = ((level, 600, 0, CHAIN_HEADS), (top + 1, 720, 120, CHAIN_HEADS),
              (fib, 480, 0, FIB_CHAIN_HEADS), (top + 2, 600, 120, FIB_CHAIN_HEADS))
    return rows, empty, frames


def _longest_cover(tmp_path):
    """A copy whose table holds the rows of :func:`_longest_rows`, and each row's frame,
    ``t_entry()`` and chain heads."""
    rows, pipeline, frames = _longest_rows()
    return _sec_inputs(tmp_path, rows, pipeline), frames


# modelx warns as its stack trace starts and stops, which is all the test does with it.
@pytest.mark.filterwarnings("ignore:call stack trace:UserWarning")
def test_every_chain_runs_one_cell_a_month_from_a_cold_start(tmp_path):
    """Called cold, each chain runs one cell a month back to ``t_entry()``, no more (D5).

    No number shows how deep a chain runs, and a compiled model runs it on the C stack, so
    a chain of two cells a month, which gives the same numbers, needs twice the stack on
    every platform (F7); ``Term_UK_S``'s count chain runs three cells a month.  On a model
    just read, nothing is cached, so modelx's stack trace counts how deep a call runs,
    against one cell a month back to ``t_entry()`` and :data:`CHAIN_OVERHEAD` more, with
    modelx's recursion limit where the module leaves it: each of :data:`CHAIN_HEADS` in the
    last month of the frame, ``net_cf``, the deepest call a projection makes, among them,
    each on a read of its own, with :data:`SWITCHED_ON` set, so that the lapse ratio loads
    mortality and the clawback reads the lapses.  At the contract's longest cover, 50 years
    from issue age 18, issued now and 120 months on, and on the family income benefit's
    point, at its own longest cover, 40 years from issue age 30, the chains of
    :data:`FIB_CHAIN_HEADS` (:func:`_longest_cover`), each row's frame asserted first, as
    §7.5's *Record — M5* and M14's carried rule ask.
    """
    folder, frames = _longest_cover(tmp_path)
    found = []
    for label, months, entry, heads in frames:
        for cell, timing in heads:
            fresh = mx.read_model(folder, name=_name("cold"))
            try:
                for ref, value in SWITCHED_ON.items():
                    setattr(fresh.Projection, ref, value)
                p = _point(fresh, label)
                assert p.proj_len() == months and p.t_entry() == entry, label
                last = p.proj_len() - 1
                args = (last,) if timing is None else (last, _code(p, timing))
                depth, chain = _cold_depth(p, cell, args), last - p.t_entry()
                if not chain <= depth <= chain + CHAIN_OVERHEAD:
                    found.append(f"point {label}: {cell}{args} cold runs {depth} cells "
                                 f"deep, where one cell a month back to t_entry() "
                                 f"{p.t_entry()} is {chain} and {CHAIN_OVERHEAD} more are "
                                 f"allowed")
            finally:
                fresh.close()
    assert not found, found


# ---------------------------------------------------------------------------
# T4 -- the count algebra
#
# BEF_DECR == BEF_NB + pols_new_biz, at every t of every point, is a convention
# (test_new_business_joins_the_count_before_decrements), and is not repeated here.


def test_the_count_rolls_forward_through_new_business_and_decrements(sec_model):
    """The count leaves month t by its deaths, lapses and expiries alone.

    On every committed point and at every ``t`` of its frame, the count weighting month
    ``t``, ``pols_if_at(t, BEF_DECR)``, less the count carried into ``t + 1``,
    ``pols_if_at(t + 1, BEF_NB)``, is the three outflows of month ``t``, to 1e-12.  The
    step from the last row to ``t = proj_len()`` is what catches cover that runs a month too
    long: the expiries would then leave a month late, and the count would carry over.  And
    the notes' end-of-month count, ``pols_if_at(t, AFT_DECR)``, is exactly the count
    carried into the next month before its new business, in every month: the two are one
    product in one order.

    ``result_pols()`` sets the same movement out row by row, in :data:`RESULT_POLS`'s
    columns, indexed by ``t`` over the frame: ``pols_if`` at ``t + 1`` is ``pols_if`` less
    the outflows at ``t``, plus the new business of ``t + 1``, and row 0 opens from
    ``pols_if_init()``.
    """
    table = sec_model.Data.model_point_table()
    for key, point_id in zip(point_keys(sec_model), table.index):
        p = projection(sec_model, key)
        bef_nb, bef_decr, aft = (_code(p, c) for c in ("BEF_NB", "BEF_DECR", "AFT_DECR"))
        for t in range(p.proj_len()):
            out = p.pols_death(t) + p.pols_lapse(t) + p.pols_maturity(t)
            moved = p.pols_if_at(t, bef_decr) - p.pols_if_at(t + 1, bef_nb)
            assert moved == pytest.approx(out, abs=1e-12), (point_id, t)
            assert p.pols_if_at(t, aft) == p.pols_if_at(t + 1, bef_nb), (point_id, t)
        pols = p.result_pols()
        assert list(pols.columns) == RESULT_POLS, point_id
        assert pols.index.name == "t" and list(pols.index) == list(range(p.proj_len()))
        carried = (pols["pols_if"] - pols[OUTFLOWS].sum(axis=1)).shift(1)
        expected = carried.fillna(p.pols_if_init()) + pols["pols_new_biz"]
        assert ((pols["pols_if"] - expected).abs() <= 1e-12).all(), point_id


def test_result_pols_is_s_report_with_the_new_business_beside_it(sec_model, s_model):
    """``result_pols()`` is S's, column for column, with ``pols_new_biz`` second (D5).

    T1 skips the report as a whole, because its frame has a column S's lacks (the spec's
    exempt), so it is compared here, on every twin: on the seven issued at the valuation
    date at offset 0, and on S's in-force point at its month 60.  Every column S's report
    has agrees, to 1e-9, frames ending together, and ``pols_new_biz`` holds the count in
    the issue month and 0 in every other.  The counts and rates carry no inflation, so the
    shipped assumptions serve.
    """
    table = sec_model.Data.model_point_table()
    twins = table.index[table["row_kind"] == "twin"].tolist()
    assert twins == sorted(s_model.Data.model_point_table().index)
    for point_id in twins:
        p = _point(sec_model, point_id)
        mine, theirs = p.result_pols(), _point(s_model, point_id).result_pols()
        assert list(mine.columns) == [theirs.columns[0], "pols_new_biz",
                                      *theirs.columns[1:]], point_id
        month = int(table.at[point_id, "source_mth"])
        assert frame_mismatches(theirs, mine, t_offset=month) == [], point_id
        issue = -int(table.at[point_id, "duration_mth"])
        assert list(mine["pols_new_biz"]) == [
            p.policy_count() if t == issue else 0.0 for t in mine.index], point_id


# What T4 multiplies policy_count by: not a whole number, because a count of policies need
# not be one, so that a flow which read the count as whole policies would not follow it.
COUNT_FACTOR = 2.5


def test_scaling_the_count_scales_every_flow_and_no_per_policy_value(tmp_path):
    """``policy_count`` is a weight: 2.5 times the count, 2.5 times every flow, the same per
    policy.

    The committed table, and a copy with every count multiplied by :data:`COUNT_FACTOR`,
    are each read with :data:`SWITCHED_ON` set before either computes anything: the
    switches that ship off, at the splice's values, so that every flow is nonzero on some
    point and the selective-lapse loading, rebroking and the clawback reach every count.
    On every point ``result_cf`` and the counts of ``result_pols`` are 2.5 times the
    committed table's, element by element, to 1e-12 relative: a scaled count is a computed
    float, which may come back from the CSV within two ulps (``uk_sec_support``'s module
    docstring).  ``result_pols``'s two rates are the committed table's exactly.  So is
    every other cell of :data:`COUNTED`, at every argument the sweep of the committed
    table's point cached: the count at each timing and the claims of each kind, which no
    report shows, among them, and the two residuals, a rounding about 0 on that many
    policies, to the residuals' floor of 1e-9.  And every cell outside :data:`COUNTED` (the
    premium, the benefit, the lapse ratio and the cohort's share in force, which the
    mortality loading reads, the waived share, the factors, the rates, both clocks, the
    flags) agrees bit for bit at every argument that sweep cached.  So a flow that dropped
    the count, or read it as whole policies, which a table of counts of 1 hides from every
    comparison with S and a count doubled hides here, fails, and so does a lapse ratio
    that divided the lapses by the count, as S's does, which moves the mortality it loads
    by an ulp (USLIB-SEC-PLAN.md §5.2, T4, precised at M11).  Each counted cell but the
    residuals is nonzero on some point.
    """
    table = _committed()
    base = mx.read_model(_sec_inputs(tmp_path / "base", table), name=_name("counted"))
    scaled = mx.read_model(_sec_inputs(tmp_path / "scaled", table.assign(
        policy_count=COUNT_FACTOR * table["policy_count"])), name=_name("scaled"))
    reports = ("result_cf", "result_pols")
    counted = sorted(COUNTED - set(reports))
    nonzero = set()
    try:
        for model in (base, scaled):
            for ref, value in SWITCHED_ON.items():
                setattr(model.Projection, ref, value)
        for key, scaled_key in zip(point_keys(base), point_keys(scaled)):
            one, many = projection(base, key), projection(scaled, scaled_key)
            sweep(one)
            for report in reports:
                b, d = one.cells[report](), many.cells[report]()
                assert d.index.equals(b.index) and list(d.columns) == list(b.columns)
                flows = [c for c in b.columns if c not in RATES]
                want = COUNT_FACTOR * b[flows]
                bad = ((d[flows] - want).abs() > 1e-12 * want.abs()).any()
                assert not bad.any(), (key, report, list(bad[bad].index))
                rates = [c for c in b.columns if c in RATES]
                assert d[rates].equals(b[rates]), (key, report)
            for name in counted:
                floor = 1e-9 if name in RESIDUALS else 0.0
                for args in _cached_args(one.cells[name]):
                    want = COUNT_FACTOR * one.cells[name](*args)
                    got = many.cells[name](*args)
                    assert abs(got - want) <= floor + 1e-12 * abs(want), (
                        key, name, args, got, want)
                    if want != 0.0 and name not in RESIDUALS:
                        nonzero.add(name)
            assert twin_mismatches(one, many, exempt=TWIN_EXEMPT_DEFAULT | COUNTED,
                                   rtol=0.0, atol=0.0) == []
            _release(base, key)
            _release(scaled, scaled_key)
    finally:
        scaled.close()
        base.close()
    want = set(counted) - RESIDUALS
    assert want <= nonzero, f"0 on every point: {sorted(want - nonzero)}"


def test_the_checks_close_on_a_million_policies(tmp_path):
    """``check_pols_roll_fwd`` and ``check_fib_ledger`` scale their tolerances with the
    count, and close at 1e6.

    A residual is rounding on that many policies, so each check holds it to 1e-10 times
    ``max(policy_count(), 1)``, where its tolerance unscaled would be 1e-10: at the counts
    the other tests use, one policy or less, the two are one.  ``Term_UK_S`` scales by
    ``pols_if_init()``, which here is 0 on a point issued at the valuation date, the count
    entering as new business.  So every committed point is projected from a copy where
    each counts a million policies: both checks close on each, and on some point the
    largest residual of each exceeds the unscaled 1e-10, so the scaling is what closes it
    (USLIB-SEC-PLAN.md §5.2, T4, precised at M10).
    """
    table = _committed()
    model = mx.read_model(_sec_inputs(tmp_path, table.assign(policy_count=1e6)),
                          name=_name("million"))
    past = set()
    try:
        for key, point_id in zip(point_keys(model), table.index):
            p = projection(model, key)
            assert p.policy_count() == 1e6
            assert p.check_pols_roll_fwd() and p.check_fib_ledger(), point_id
            for check in ("check_pols_roll_fwd_resid", "check_fib_ledger_resid"):
                worst = max(abs(p.cells[check](t)) for t in range(p.proj_len()))
                if worst > 1e-10:
                    past.add(check)
            _release(model, key)
    finally:
        model.close()
    assert past == {"check_pols_roll_fwd_resid", "check_fib_ledger_resid"}, past


# ---------------------------------------------------------------------------
# T5 -- validation
#
# Each malformed table is the committed one with one fault.  The checks run over the whole
# table as it is read, in Data, and the message names the file it read and the column or
# every point at fault.  A blank cell reads as NaN, and so does a text cell once the checks
# coerce the column to numbers, so each is refused as a count, a duration or a state that
# is not a number.  The repeated point_id holds another policy under the same label, as a
# bad extract would, so that the check must look at the labels and not at whole rows.  The
# point_ids are the committed table's: 1 to 8 the twins of S's points, 8 in force at 60;
# 9, the indexed point on its fifth anniversary; 10, the family income benefit mid-year at
# 66; 11, the waiver point at 66, its pipeline full; 12, the waiver point at 4, inside its
# deferred period; 13, the anchor cell in its last month; 14, the waiver point issued 13
# months on.  A {file} in a message is the table's filename: every case is read by one
# model, from a file of its own (the malformed fixture).


def _drop(column):
    return lambda table: table.drop(columns=column)


MALFORMED = [
    ("a negative count", _set("policy_count", [9], -0.1),
     "{file}: policy_count must be a number, zero or more; it is not at point_id [9]"),
    ("a blank count", _set("policy_count", [10], float("nan")),
     "{file}: policy_count must be a number, zero or more; it is not at point_id [10]"),
    ("two bad counts", _set("policy_count", [9, 11], -1.0),
     "{file}: policy_count must be a number, zero or more; it is not at point_id [9, 11]"),
    ("a text count", _set("policy_count", [12], "abc"),
     "{file}: policy_count must be a number, zero or more; it is not at point_id [12]"),
    ("an infinite count", _set("policy_count", [12], float("inf")),
     "{file}: policy_count must be a number, zero or more; it is not at point_id [12]"),
    ("a fractional duration", _set("duration_mth", [10], 66.5),
     "{file}: duration_mth must be a whole number of months; it is not at point_id [10]"),
    ("a blank duration", _set("duration_mth", [14], float("nan")),
     "{file}: duration_mth must be a whole number of months; it is not at point_id [14]"),
    ("a text duration", _set("duration_mth", [12], "x4"),
     "{file}: duration_mth must be a whole number of months; it is not at point_id [12]"),
    # numpy casts a float past int64 to the least int64, a policy issued 2**63 months on,
    # without a word: the table refuses it first.
    ("a duration past int64", _set("duration_mth", [9], 1e19),
     "{file}: duration_mth must be below 2**53 months; it is not at point_id [9]"),
    ("durations of 2**53 months at two points", _set("duration_mth", [9, 11], 2.0 ** 53),
     "{file}: duration_mth must be below 2**53 months; it is not at point_id [9, 11]"),
    ("issued beyond the horizon", _set("duration_mth", [14], -121),
     "{file}: duration_mth must be -120 or more, a policy issued at most 120 months after "
     "the valuation date; it is not at point_id [14]"),
    *[(f"no {column} column", _drop(column), f"{{file}} has no {column} column")
      for column in ("policy_count", "duration_mth", *STATE)],
    ("a repeated point_id",
     lambda t: pd.concat([t, t.loc[[9]].assign(policy_id="TA-900099")]),
     "{file}: point_id [9] appears more than once"),
    ("a negative lapse ratio", _set("lapse_cum_init", [9], -0.1),
     "{file}: lapse_cum_init must be a number, 0 or more and below 1, the share of the "
     "issued cohort lapsed; it is not at point_id [9]"),
    ("a lapse ratio of 1", _set("lapse_cum_init", [9], 1.0),
     "{file}: lapse_cum_init must be a number, 0 or more and below 1, the share of the "
     "issued cohort lapsed; it is not at point_id [9]"),
    ("a blank lapse ratio", _set("lapse_cum_init", [10], float("nan")),
     "{file}: lapse_cum_init must be a number, 0 or more and below 1, the share of the "
     "issued cohort lapsed; it is not at point_id [10]"),
    ("a negative ledger", _set("fib_cum_init", [10], -1.0),
     "{file}: fib_cum_init must be a number, zero or more; it is not at point_id [10]"),
    ("an infinite ledger", _set("fib_cum_init", [10], float("inf")),
     "{file}: fib_cum_init must be a number, zero or more; it is not at point_id [10]"),
    ("a cover factor below 1", _set("idx_factor_init", [9], 0.99),
     "{file}: idx_factor_init must be a number, 1 or more; it is not at point_id [9]"),
    ("a blank cover factor", _set("idx_factor_init", [9], float("nan")),
     "{file}: idx_factor_init must be a number, 1 or more; it is not at point_id [9]"),
    ("a premium factor below 1", _set("idx_prem_factor_init", [9], 0.5),
     "{file}: idx_prem_factor_init must be a number, 1 or more; it is not at point_id [9]"),
    ("a negative waived share", _set("wop_waived_frac_init", [11], -0.1),
     "{file}: wop_waived_frac_init must be a number from 0 to 1; it is not at point_id "
     "[11]"),
    ("a waived share past 1", _set("wop_waived_frac_init", [11], 1.5),
     "{file}: wop_waived_frac_init must be a number from 0 to 1; it is not at point_id "
     "[11]"),
    ("a text waived share", _set("wop_waived_frac_init", [11], "x"),
     "{file}: wop_waived_frac_init must be a number from 0 to 1; it is not at point_id "
     "[11]"),
    ("a lapse ratio on new business", _set("lapse_cum_init", [1], 0.1),
     "{file}: lapse_cum_init must be 0 on a policy not yet in force, duration_mth 0 or "
     "less; it is not at point_id [1]"),
    ("a ledger on future business", _set("fib_cum_init", [14], 0.01),
     "{file}: fib_cum_init must be 0 on a policy not yet in force, duration_mth 0 or less; "
     "it is not at point_id [14]"),
    ("a cover factor on new business", _set("idx_factor_init", [5], 1.03),
     "{file}: idx_factor_init must be 1 on a policy not yet in force, duration_mth 0 or "
     "less; it is not at point_id [5]"),
    ("a premium factor on future business", _set("idx_prem_factor_init", [14], 1.045),
     "{file}: idx_prem_factor_init must be 1 on a policy not yet in force, duration_mth 0 "
     "or less; it is not at point_id [14]"),
    # No increase is given before month 0 in a policy's first twelve months: its first
    # anniversary, at policy month 12, is month 0's own event on a policy valued then
    # (USLIB-SEC-PLAN.md D6, precised at its M7).  The indexed point on its fifth
    # anniversary, moved back to its first with its factors, is refused there, the rule's
    # edge, and in its first month; the edges test reads it one month on.
    ("a cover factor on the first anniversary", _set("duration_mth", [9], 12),
     "{file}: idx_factor_init must be 1 on a policy in force 12 months or fewer, whose "
     "first anniversary falls in month 0 or later; it is not at point_id [9]"),
    ("a premium factor in the first policy year",
     _then(_set("duration_mth", [9], 1), _set("idx_factor_init", [9], 1.0)),
     "{file}: idx_prem_factor_init must be 1 on a policy in force 12 months or fewer, whose "
     "first anniversary falls in month 0 or later; it is not at point_id [9]"),
    ("a waived share on new business", _set("wop_waived_frac_init", [7], 0.01),
     "{file}: wop_waived_frac_init must be 0 on a policy not yet in force, duration_mth 0 "
     "or less; it is not at point_id [7]"),
    ("negative streams in payment", _set("fib_streams_init", [10], -0.001),
     "{file}: fib_streams_init must be a number, zero or more; it is not at point_id [10]"),
    ("blank streams in payment", _set("fib_streams_init", [10], float("nan")),
     "{file}: fib_streams_init must be a number, zero or more; it is not at point_id [10]"),
    ("a negative commission paid", _set("comm_init_pp_init", [9], -1.0),
     "{file}: comm_init_pp_init must be a number, zero or more; it is not at point_id [9]"),
    ("a text commission paid", _set("comm_init_pp_init", [11], "x"),
     "{file}: comm_init_pp_init must be a number, zero or more; it is not at point_id [11]"),
    ("an infinite commission paid", _set("comm_init_pp_init", [8], float("inf")),
     "{file}: comm_init_pp_init must be a number, zero or more; it is not at point_id [8]"),
    ("streams in payment on future business", _set("fib_streams_init", [14], 0.001),
     "{file}: fib_streams_init must be 0 on a policy not yet in force, duration_mth 0 or "
     "less; it is not at point_id [14]"),
    ("a commission paid on new business", _set("comm_init_pp_init", [1], 216.0),
     "{file}: comm_init_pp_init must be 0 on a policy not yet in force, duration_mth 0 or "
     "less; it is not at point_id [1]"),
    ("a blank flag", _set("wop", [3], float("nan")),
     "{file}: wop must be True or False; it is not at point_id [3]"),
    ("a flag written yes", _set("indexation", [2], "yes"),
     "{file}: indexation must be True or False; it is not at point_id [2]"),
    ("a flag written 1", _set("joint_first_death", [1], 1),
     "{file}: joint_first_death must be True or False; it is not at point_id [1]"),
    ("an unknown shape", _set("shape", [1], "flat"),
     "{file}: shape must be level or decreasing or fib; it is not at point_id [1]"),
    ("an unknown sex", _set("sex", [2], "X"),
     "{file}: sex must be M or F; it is not at point_id [2]"),
    ("an unknown smoker status", _set("smoker", [3], "Y"),
     "{file}: smoker must be N or S; it is not at point_id [3]"),
    ("an unknown premium mode", _set("premium_mode", [4], "weekly"),
     "{file}: premium_mode must be monthly or annual; it is not at point_id [4]"),
    ("an unknown mortality basis", _set("mort_basis", [5], "ultimate"),
     "{file}: mort_basis must be applied or select; it is not at point_id [5]"),
    ("a blank issue age", _set("age_at_entry", [1], float("nan")),
     "{file}: age_at_entry must be a finite number; it is not at point_id [1]"),
    ("an infinite issue age", _set("age_at_entry", [2], float("inf")),
     "{file}: age_at_entry must be a finite number; it is not at point_id [2]"),
    ("a text issue age", _set("age_at_entry", [3], "x35"),
     "{file}: age_at_entry must be a finite number; it is not at point_id [3]"),
    ("a blank term", _set("policy_term", [4], float("nan")),
     "{file}: policy_term must be a finite number; it is not at point_id [4]"),
    # numpy casts a number past int64 to the least int64, without a word: the table
    # refuses an age or a term of 2**53 or more, which an int64 vector cannot hold whole.
    ("an issue age past int64", _set("age_at_entry", [1], 1e19),
     "{file}: age_at_entry must be below 2**53 in size; it is not at point_id [1]"),
    ("an issue age of 2**53", _set("age_at_entry", [1], 2.0 ** 53),
     "{file}: age_at_entry must be below 2**53 in size; it is not at point_id [1]"),
    ("a term of 2**53 years", _set("policy_term", [2], 2.0 ** 53),
     "{file}: policy_term must be below 2**53 in size; it is not at point_id [2]"),
    ("a negative sum assured", _set("sum_assured", [1], -1.0),
     "{file}: sum_assured must be a number, zero or more; it is not at point_id [1]"),
    ("a blank income", _set("fib_income", [3], float("nan")),
     "{file}: fib_income must be a number, zero or more; it is not at point_id [3]"),
    ("a text premium", _set("premium_mth", [2], "12 pounds"),
     "{file}: premium_mth must be a number, zero or more; it is not at point_id [2]"),
    ("a negative schedule rate", _set("sched_rate", [2], -0.01),
     "{file}: sched_rate must be a number, zero or more; it is not at point_id [2]"),
    ("a commutation share past 1", _set("fib_commute_rate", [4], 1.5),
     "{file}: fib_commute_rate must be a number from 0 to 1; it is not at point_id [4]"),
    ("a blank commutation share", _set("fib_commute_rate", [3], float("nan")),
     "{file}: fib_commute_rate must be a number from 0 to 1; it is not at point_id [3]"),
    ("a joint point with no second age", _set("joint_age", [6], float("nan")),
     "{file}: joint_age must be a finite number on a joint first-death point; it is not "
     "at point_id [6]"),
    ("a joint point's second age past int64", _set("joint_age", [6], -1e19),
     "{file}: joint_age must be below 2**53 in size on a joint first-death point; it is "
     "not at point_id [6]"),
    ("a joint point's second age of 2**53", _set("joint_age", [6], 2.0 ** 53),
     "{file}: joint_age must be below 2**53 in size on a joint first-death point; it is "
     "not at point_id [6]"),
    ("a joint point with an unknown second sex", _set("joint_sex", [6], "X"),
     "{file}: joint_sex must be M or F on a joint first-death point; it is not at "
     "point_id [6]"),
    ("a joint point with no second smoker status", _set("joint_smoker", [6], float("nan")),
     "{file}: joint_smoker must be N or S on a joint first-death point; it is not at "
     "point_id [6]"),
    ("indexation on the decreasing shape", _set("indexation", [2], True),
     "{file}: indexation is modelled on the level shape only; it is elected at point_id "
     "[2]"),
    ("a cover factor without indexation", _set("idx_factor_init", [10], 1.2),
     "{file}: idx_factor_init must be 1 unless indexation is elected; it is not at "
     "point_id [10]"),
    ("a premium factor without indexation", _set("idx_prem_factor_init", [13], 1.2),
     "{file}: idx_prem_factor_init must be 1 unless indexation is elected; it is not at "
     "point_id [13]"),
    ("a waived share without the waiver", _set("wop_waived_frac_init", [9], 0.01),
     "{file}: wop_waived_frac_init must be 0 unless the waiver of premium rider is in "
     "force; it is not at point_id [9]"),
    ("streams in payment off the family income benefit",
     _set("fib_streams_init", [9], 0.001),
     "{file}: fib_streams_init must be 0 unless the shape is fib; it is not at point_id "
     "[9]"),
    ("more streams in payment than deaths", _set("fib_streams_init", [10], 0.005),
     "{file}: fib_streams_init must be at most fib_cum_init, the streams in payment no "
     "more than the deaths since issue; it is not at point_id [10]"),
]


@pytest.fixture(scope="module")
def malformed(tmp_path_factory):
    """One model, and beside it every table of :data:`MALFORMED`, each a file of its own.

    Reading the model costs more than every check it makes, so the cases share one read:
    each case points ``Data.model_point_file`` at its own file, which clears the table, and
    reads it afresh.  Returns ``(model, {case: filename})``.
    """
    root = tmp_path_factory.mktemp("malformed")
    files = {}
    for number, (case, edit, _) in enumerate(MALFORMED):
        files[case] = f"malformed_{number:02d}_sec.csv"
        temp_inputs(root, model_path(SEC), model_points=edit(_committed()),
                    model_point_file=files[case])
    model = mx.read_model(root / SEC, name=_name("malformed"))
    yield model, files
    model.close()


@pytest.mark.parametrize("case, edit, message", MALFORMED, ids=[c[0] for c in MALFORMED])
def test_a_malformed_in_force_row_is_refused_naming_its_point(malformed, case, edit,
                                                               message):
    """``Data.model_point_table()`` refuses the table, naming the fault (D6, T5)."""
    model, files = malformed
    model.Data.model_point_file = files[case]
    _refused(model.Data.model_point_table, message.format(file=files[case]))


# Each malformed pipeline is the committed one with one fault, on the committed table.  The
# lines are the file's, the header line 1: the committed pipeline holds point 11's six lags
# on lines 2 to 7 and point 12's four on lines 8 to 11.
def _lines(edit_rows):
    """An edit of the pipeline by ``edit_rows(table)``, on a default index."""
    return lambda table: edit_rows(table.copy()).reset_index(drop=True)


def _cell(row, column, value):
    """An edit of the pipeline that writes ``value`` into ``column`` at its ``row``."""
    def edit(table):
        cells = table[column].astype(object)
        cells.iloc[row] = value
        return table.assign(**{column: cells})
    return _lines(edit)


def _extra(**row):
    """An edit of the pipeline that appends a row of its own."""
    return _lines(lambda table: pd.concat([table, pd.DataFrame([row])]))


def _past_one(points):
    """What ``Data.wop_pipeline()`` says of ``points``, whose waived and deferred shares
    sum past 1."""
    return (f"{PIPELINE}: a point's wop_waived_frac_init and its wop_deferred_init must "
            f"sum to 1 or less, shares of the policies in force; they do not at point_id "
            f"{points}")


def _shares(point, shares):
    """An edit of the pipeline that writes ``shares``, ``{lag: share}``, at ``point``'s
    lags."""
    def edit(table):
        table = table.copy()
        for lag, share in shares.items():
            at = (table["point_id"] == point) & (table["lag"] == lag)
            assert at.sum() == 1, (point, lag)
            table.loc[at, "wop_deferred_init"] = share
        return table
    return edit


MALFORMED_PIPELINE = [
    *[(f"no {column} column", _lines(lambda t, c=column: t.drop(columns=c)),
       f"{PIPELINE} has no {column} column")
      for column in ("point_id", "lag", "wop_deferred_init")],
    ("a fractional point_id", _cell(0, "point_id", 11.5),
     f"{PIPELINE}: point_id must be a whole number; it is not on line [2]"),
    ("a text lag", _cell(2, "lag", "three"),
     f"{PIPELINE}: lag must be a whole number; it is not on line [4]"),
    ("a blank lag", _cell(7, "lag", float("nan")),
     f"{PIPELINE}: lag must be a whole number; it is not on line [9]"),
    ("a lag past int64", _cell(1, "lag", 1e19),
     f"{PIPELINE}: lag must be below 2**53 in size; it is not on line [3]"),
    ("a point the table lacks", _extra(point_id=99, lag=1, wop_deferred_init=0.0),
     f"{PIPELINE}: point_id [99] on line [12] is no point of {TABLE}"),
    ("a lag twice", _extra(point_id=11, lag=3, wop_deferred_init=0.0003),
     f"{PIPELINE}: each point_id and lag must have one row; point_id 11 lag 3 is on line "
     f"[4, 12]"),
    ("a lag of 0", _cell(0, "lag", 0),
     f"{PIPELINE}: lag must be from 1 to its point's duration_mth, the months since issue "
     f"at the valuation date; it is not on line [2]"),
    ("a lag before issue", _extra(point_id=12, lag=5, wop_deferred_init=0.0),
     f"{PIPELINE}: lag must be from 1 to its point's duration_mth, the months since issue "
     f"at the valuation date; it is not on line [12]"),
    ("a lag of a point not yet in force", _extra(point_id=14, lag=1, wop_deferred_init=0.0),
     f"{PIPELINE}: lag must be from 1 to its point's duration_mth, the months since issue "
     f"at the valuation date; it is not on line [12]"),
    ("a lag of a point without the waiver", _extra(point_id=9, lag=1, wop_deferred_init=0.0),
     f"{PIPELINE}: a row's point must have the waiver of premium rider in force; it does "
     f"not on line [12]"),
    ("a negative deferred share", _cell(4, "wop_deferred_init", -0.01),
     f"{PIPELINE}: wop_deferred_init must be a number from 0 to 1; it is not on line [6]"),
    ("a deferred share past 1", _cell(8, "wop_deferred_init", 1.5),
     f"{PIPELINE}: wop_deferred_init must be a number from 0 to 1; it is not on line "
     f"[10]"),
    ("a blank deferred share", _cell(9, "wop_deferred_init", float("nan")),
     f"{PIPELINE}: wop_deferred_init must be a number from 0 to 1; it is not on line "
     f"[11]"),
    ("an infinite deferred share", _cell(3, "wop_deferred_init", float("inf")),
     f"{PIPELINE}: wop_deferred_init must be a number from 0 to 1; it is not on line [5]"),
    ("deferred shares past 1 with the waived one", _cell(0, "wop_deferred_init", 0.999),
     _past_one([11])),
]


@pytest.mark.parametrize("case, edit, message", MALFORMED_PIPELINE,
                         ids=[c[0] for c in MALFORMED_PIPELINE])
def test_a_malformed_pipeline_is_refused_naming_its_line(tmp_path, case, edit, message):
    """``Data.wop_pipeline()`` refuses the companion, naming the fault and its lines, and
    so does a projection of the waiver point that reads it (D6, D8, T5)."""
    model = _read_edited(tmp_path, lambda t: t, edit)
    try:
        _refused(model.Data.wop_pipeline, message)
        _refused(_row(model, "derived", 7, 66).result_cf, message)
    finally:
        model.close()


# Point 11's deferred shares written so that, with a waived share of 0.5, they sum to 1
# exactly, from the waived share and then the last lag down, as Data and the active share
# sum them: powers of 2, each partial sum exact.  Lag 1 then takes 2**-52 more, a unit in
# the last place of 1, so that the sum is the float above 1.
EXACT_ONE = {6: 0.25, 5: 0.125, 4: 0.0625, 3: 0.03125, 2: 0.015625, 1: 0.015625}
PAST_ONE_ULP = {**EXACT_ONE, 1: 0.015625 + 2.0 ** -52}

# Two opening states of point 11 whose sum turns on its order (the review's), as (waived
# share, {lag: deferred share}).  Powers of 2 sum exactly in any order, so they cannot
# tell the active share's order, the waived share and then the last lag down, from
# another; these can.  PAST_IN_ORDER sums to 1 from the first lag up, and to the float
# above 1 in the active share's order: refused.  ONE_IN_ORDER sums to 1 exactly in the
# active share's order, and to the float above 1 from the first lag up: accepted.
# test_rule_8_sums_as_the_active_share_does holds both sums.
PAST_IN_ORDER = (0.44447597388895366,
                 {1: 0.07176474865770067, 2: 0.06300620235246578, 3: 0.028168511827111734,
                  4: 0.1303173894130484, 5: 0.26080420398918386, 6: 0.0014629698715359113})
ONE_IN_ORDER = (0.6624947942016208,
                {1: 0.009973524213338492, 2: 0.10665500667616475, 3: 0.08261293840341907,
                 4: 0.014856837475601278, 5: 0.05186757776780304, 6: 0.07153932126205256})

# What Data refuses of an opening state whose waived and deferred shares sum past 1, as
# (case, the table's edit, the pipeline's edit, the points named): the deferred shares
# alone of point 12, which waives nothing; point 11's waived share with its committed
# pipeline; both points at once, each named; the sum one unit in the last place past 1,
# which no share of its own passes; and PAST_IN_ORDER, past 1 in the active share's order
# alone.
OPENING_PAST_ONE = [
    ("point 12's deferred shares alone", lambda t: t, _shares(12, {1: 1.0}), [12]),
    ("point 11's waived share and its pipeline",
     _set("wop_waived_frac_init", [11], 0.9995), None, [11]),
    ("both points", _set("wop_waived_frac_init", [11], 0.9995), _shares(12, {1: 1.0}),
     [11, 12]),
    ("a unit in the last place past 1", _set("wop_waived_frac_init", [11], 0.5),
     _shares(11, PAST_ONE_ULP), [11]),
    ("past 1 in the active share's order alone",
     _set("wop_waived_frac_init", [11], PAST_IN_ORDER[0]), _shares(11, PAST_IN_ORDER[1]),
     [11]),
]


@pytest.mark.parametrize("case, edit, pipeline_edit, points", OPENING_PAST_ONE,
                         ids=[c[0] for c in OPENING_PAST_ONE])
def test_an_opening_state_past_1_is_refused_naming_its_point(tmp_path, case, edit,
                                                             pipeline_edit, points):
    """The waived share and the deferred shares at the valuation date are shares of one
    in-force, so ``Data.wop_pipeline()`` refuses a point whose sum passes 1, naming it, and
    so does a projection of it (§6.1, T5).

    ``wop_active_frac`` opens at what they leave, the active share, which would open below
    0.  Each share alone may be inside 0 to 1, as rule 7 holds it, and the sum still pass
    1 (:data:`OPENING_PAST_ONE`), by as little as a unit in the last place.  The sum is
    taken as the active share takes it, from the waived share and then the last lag down,
    so what ``Data`` passes opens the active share at 0 or more:
    :func:`test_an_opening_state_of_exactly_1_projects` holds the edge.
    """
    model = _read_edited(tmp_path, edit, pipeline_edit)
    try:
        _refused(model.Data.wop_pipeline, _past_one(points))
        _refused(_point(model, points[0]).result_cf, _past_one(points))
    finally:
        model.close()


def test_an_opening_state_of_exactly_1_projects(tmp_path):
    """A point whose waived and deferred shares sum to 1 exactly is accepted, and its
    active share opens at 0, to the last bit (§6.1, T5).

    Point 11 written with a waived share of 0.5 and deferred shares of :data:`EXACT_ONE`:
    every life incapacitated at the valuation date.  No life can fall ill until one
    recovers, so the active share opens at 0 and the entrants of month 7, the first from
    the frame, are 0, and every share stays inside 0 to 1 through the frame, the deferred
    one, what the other two leave, among them.
    """
    model = _read_edited(tmp_path, _set("wop_waived_frac_init", [11], 0.5),
                         _shares(11, EXACT_ONE))
    try:
        model.Data.wop_pipeline()
        p = _point(model, 11)
        assert len(p.result_cf()) == p.proj_len()
        assert p.wop_active_frac(0) == 0.0
        rec = 1.0 - p.wop_rec_rate_mth()
        assert p.wop_waived_frac(7) == p.wop_waived_frac(6) * rec
        for t in range(p.proj_len()):
            act, u = p.wop_active_frac(t), p.wop_waived_frac(t)
            assert 0.0 <= act <= 1.0 and 0.0 <= u <= 1.0 and 0.0 <= 1.0 - act - u, t
    finally:
        model.close()


def _in_order(waived, shares):
    """The sum ``Data``'s rule 8 and the active share take: the waived share, then the
    deferred shares from the last lag down."""
    held = waived
    for lag in sorted(shares, reverse=True):
        held = held + shares[lag]
    return held


def _lag_up(waived, shares):
    """The same shares summed from the first lag up, the order rule 8 does not take."""
    held = waived
    for lag in sorted(shares):
        held = held + shares[lag]
    return held


def test_rule_8_sums_as_the_active_share_does(tmp_path):
    """Rule 8 sums an opening state in the active share's order, and so accepts the one
    that opens the active share at 0 exactly (§6.1, T5).

    :data:`ONE_IN_ORDER` sums to 1 exactly in that order, and to the float above 1 from the
    first lag up; :data:`PAST_IN_ORDER` the other way round, and :data:`OPENING_PAST_ONE`
    holds its refusal.  Written on point 11, ``ONE_IN_ORDER`` is read back as written,
    accepted, and projected: the active share opens at 0, to the last bit, and every share
    stays inside 0 to 1.  A rule 8 summing from the first lag up would refuse it, and pass
    ``PAST_IN_ORDER``, whose active share would open below 0.
    """
    assert _in_order(*PAST_IN_ORDER) == math.nextafter(1.0, 2.0)
    assert _lag_up(*PAST_IN_ORDER) == 1.0
    assert _in_order(*ONE_IN_ORDER) == 1.0
    assert _lag_up(*ONE_IN_ORDER) == math.nextafter(1.0, 2.0)
    waived, shares = ONE_IN_ORDER
    model = _read_edited(tmp_path, _set("wop_waived_frac_init", [11], waived),
                         _shares(11, shares))
    try:
        p = _point(model, 11)
        assert p.wop_waived_frac_init() == waived
        assert {k: p.wop_deferred_init(k) for k in shares} == shares
        assert len(p.result_cf()) == p.proj_len()
        assert p.wop_active_frac(0) == 0.0
        for t in range(p.proj_len()):
            act, u = p.wop_active_frac(t), p.wop_waived_frac(t)
            assert 0.0 <= act <= 1.0 and 0.0 <= u <= 1.0 and 0.0 <= 1.0 - act - u, t
    finally:
        model.close()


def test_the_future_horizon_is_a_reference_that_bounds_future_business(tmp_path):
    """``Data.future_horizon_mth`` refuses a policy issued later than it, and 0 refuses all.

    The committed table's one future point is issued 13 months on.  It reads at the shipped
    120 months and at 13, the shortest horizon that admits it, and is refused at 12, by
    name.  At 0 the model takes no future new business, D4's fallback for a product that
    cannot support it, and the message says so.  A negative horizon is itself refused.
    Setting the Reference clears the table, so each value is read afresh.
    """
    future = _label(_committed(), "future", 7, -13)
    later = (f"{TABLE}: duration_mth must be -12 or more, a policy issued at most 12 months "
             f"after the valuation date; it is not at point_id [{future}]")
    no_future = (f"{TABLE}: duration_mth must be 0 or more: this model takes no future new "
                 f"business; it is not at point_id [{future}]")
    model = mx.read_model(_sec_inputs(tmp_path, _committed()), name=_name("horizon"))
    try:
        assert model.Data.future_horizon_mth == 120
        negative = "future_horizon_mth must be 0 months or more, not -1"
        for horizon, refusal in ((13, None), (12, later), (0, no_future), (-1, negative),
                                 (12.0, later), (-1.0, negative), (120, None)):
            model.Data.future_horizon_mth = horizon
            if refusal is None:
                assert len(model.Data.model_point_table()) == len(_committed()), horizon
            else:
                _refused(model.Data.model_point_table, refusal)
    finally:
        model.close()


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
    # Windows ends each printed line with "\r\n"; read them as "\n", as a frame's
    # to_string() writes them.
    return done.stdout.decode("ascii").replace("\r\n", "\n")


def test_a_point_past_its_cover_is_refused_by_proj_len(tmp_path):
    """A point whose cover has ended has no frame, and ``proj_len()`` refuses it by name.

    The anchor cell in its last covered month is moved on to ``duration_mth`` 300, the
    month its 25-year term ends.  That is a rule of the product, not of the table: it needs
    the term the point's own columns give, read where the frame is defined, so the table
    reads, and the point is refused on its first projection, rather than projecting
    nothing.  A loop over the block would meet the point only when it reached it, after
    projecting the points before it, so ``run_sec.py --block``, run beside the table, asks
    every point for its frame first: it fails naming the point, and prints nothing before.
    And one month earlier, 299, the last covered month, is the committed row, which
    projects one month.
    """
    moved = _label(_committed(), "derived", 1, 299)
    model = _read_edited(tmp_path, _set("duration_mth", [moved], 300))
    message = (f"point_id {moved}: duration_mth 300 is at or past the end of cover, policy "
               f"month 300")
    try:
        assert len(model.Data.model_point_table()) == len(_committed())
        _refused(_point(model, moved).result_cf, message)
    finally:
        model.close()
    runner = tmp_path / "run_sec.py"
    shutil.copy(model_path(SEC).parent / "run_sec.py", runner)
    done = _run_sec(runner, "--block", check=False)
    assert done.returncode != 0 and done.stdout == b""
    assert message in done.stderr.decode(errors="replace")


def _rows_of(table, **match):
    """The point_ids of ``table``'s rows whose columns hold ``match``."""
    hit = pd.Series(True, index=table.index)
    for column, value in match.items():
        hit &= table[column] == value
    return table.index[hit].tolist()


# What the contract does not issue, refused by proj_len() as a point past its cover is, as
# (case, the table's edit, the References set, the point, the message, and the frame the
# point projects at the shipped References, or None).  Data reads a term and an issue age
# as Term_UK_S does, so each reads.  product-spec.md writes terms up to 50 years, 40 on
# the family income benefit, issue ages from 18, and expiry by the 90th birthday, the 70th
# on the family income benefit, and the compiled caches will be sized from them; each bound
# is refused just inside it here, and accepted at it in the edges test.  And each bound,
# moved past a committed twin, refuses it, which at the shipped bound projects its frame:
# the Reference is what refuses it.  A bound lowered below 18 lets no point project, since
# the mortality table starts at 18, which mort_rate_base refuses below, so the age bound
# is the one raised.  Point 1 is the anchor cell, level, issued at 35 for 25 years; point 3
# the family income benefit, the same; point 6 joint, its second life 33.
NOT_ISSUED = [
    ("a 51-year term", _set("policy_term", [1], 51), {}, 1,
     "point_id 1: the term, 51 years, is above policy_term_max, 50", None),
    ("a term above a bound lowered to 24", None, {"policy_term_max": 24}, 1,
     "point_id 1: the term, 25 years, is above policy_term_max, 24", 300),
    ("a 41-year family income benefit",
     _then(_set("policy_term", [3], 41), _set("age_at_entry", [3], 29)), {}, 3,
     "point_id 3: the term, 41 years, is above policy_term_max_fib, 40", None),
    ("a family income benefit above a bound lowered to 24", None,
     {"policy_term_max_fib": 24}, 3,
     "point_id 3: the term, 25 years, is above policy_term_max_fib, 24", 300),
    ("an issue age of 17", _set("age_at_entry", [1], 17), {}, 1,
     "point_id 1: life 1's issue age, 17, is below issue_age_min, 18", None),
    ("an issue age below a bound raised to 36", None, {"issue_age_min": 36}, 1,
     "point_id 1: life 1's issue age, 35, is below issue_age_min, 36", 300),
    ("a second life issued at 17", _set("joint_age", [6], 17), {}, 6,
     "point_id 6: life 2's issue age, 17, is below issue_age_min, 18", None),
    ("a second life below a bound raised to 34", None, {"issue_age_min": 34}, 6,
     "point_id 6: life 2's issue age, 33, is below issue_age_min, 34", 300),
    ("cover to 91", _set("age_at_entry", [1], 66), {}, 1,
     "point_id 1: life 1's cover runs to attained age 91, issue age 66 and a 25-year "
     "term, past expiry_age_max, 90", None),
    ("cover past a bound lowered to 59", None, {"expiry_age_max": 59}, 1,
     "point_id 1: life 1's cover runs to attained age 60, issue age 35 and a 25-year "
     "term, past expiry_age_max, 59", 300),
    ("a family income benefit to 71", _set("age_at_entry", [3], 46), {}, 3,
     "point_id 3: life 1's cover runs to attained age 71, issue age 46 and a 25-year "
     "term, past expiry_age_max_fib, 70", None),
    ("a family income benefit past a bound lowered to 59", None,
     {"expiry_age_max_fib": 59}, 3,
     "point_id 3: life 1's cover runs to attained age 60, issue age 35 and a 25-year "
     "term, past expiry_age_max_fib, 59", 300),
    ("a second life covered to 91", _set("joint_age", [6], 66), {}, 6,
     "point_id 6: life 2's cover runs to attained age 91, issue age 66 and a 25-year "
     "term, past expiry_age_max, 90", None),
    # Each bound written as a float, which the compiled model holds as an int, printed as
    # it does.
    ("a term above a bound lowered to 24, written as a float", None,
     {"policy_term_max": 24.0}, 1,
     "point_id 1: the term, 25 years, is above policy_term_max, 24", 300),
    ("an issue age below a bound raised to 36, written as a float", None,
     {"issue_age_min": 36.0}, 1,
     "point_id 1: life 1's issue age, 35, is below issue_age_min, 36", 300),
    ("cover past a bound lowered to 59, written as a float", None,
     {"expiry_age_max": 59.0}, 1,
     "point_id 1: life 1's cover runs to attained age 60, issue age 35 and a 25-year "
     "term, past expiry_age_max, 59", 300),
]


@pytest.mark.parametrize("case, edit, refs, point, message, frame", NOT_ISSUED,
                         ids=[c[0] for c in NOT_ISSUED])
def test_a_point_the_contract_does_not_issue_is_refused_by_proj_len(tmp_path, case, edit,
                                                                    refs, point, message,
                                                                    frame):
    """``proj_len()`` refuses a point outside the contract's bounds, naming it (§6.1).

    ``Term_UK_S`` projects a term of any length from any age its tables hold, and so would
    modelx here, but the contract does not write it, and the compiled model's caches will
    be sized from the contract: a frame of at most 50 years and the horizon, a schedule of
    at most 600 months, an annuity-certain of at most 480.  So the frame refuses such a
    point, naming it, as it refuses a point past its cover, and every report with it
    (:data:`NOT_ISSUED`): each bound just inside it, a life of a joint point among them,
    and each bound moved past a committed twin, which projects at the shipped bound, on a
    model read afresh.  A bound off by one, a life the rule forgot, or a refusal lost, lets
    a point through.  The table reads either way.  Every Reference is set on a model just
    read, before its projection computes anything (K7).
    """
    model = _read_edited(tmp_path, edit or (lambda t: t))
    try:
        for ref, value in refs.items():
            setattr(model.Projection, ref, value)
        assert len(model.Data.model_point_table()) == len(_committed())
        _refused(_point(model, point).result_cf, message)
    finally:
        model.close()
    if frame is not None:
        shipped = mx.read_model(model_path(SEC), name=_name("bound"))
        try:
            assert len(_point(shipped, point).result_cf()) == frame
        finally:
            shipped.close()


def _drop_lag(point, lag):
    """An edit of the pipeline that drops ``point``'s row at ``lag``."""
    return _lines(lambda t: t[~((t["point_id"] == point) & (t["lag"] == lag))])


def _move_lag(point, lag, to):
    """An edit of the pipeline that moves ``point``'s row at ``lag`` to lag ``to``."""
    def edit(table):
        table.loc[(table["point_id"] == point) & (table["lag"] == lag), "lag"] = to
        return table
    return _lines(edit)


# What proj_len() refuses of a waiver point's pipeline, as (case, the pipeline's edit, the
# References set, the point, the message).  The committed waiver points in force are 11,
# 66 months in, which holds lags 1 to 6, and 12, 4 months in, which holds lags 1 to 4.  A
# point's lags are a rule of the product, since the deferred period is a Reference: so a
# deferred period lengthened or shortened refuses a pipeline Data accepts.  The count and
# the last lag are each checked: a pipeline with no row is refused by its count, and one
# with lags 1 to 5 and 7, as many lags as it should hold, by its last.
SHORT_PIPELINE = [
    ("a waiver point in force with no pipeline",
     _lines(lambda t: t[t["point_id"] != 11]), {}, 11,
     "point_id 11: wop_pipeline_sec.csv holds 0 lags, its last 0, where a waiver point in "
     "force 66 months holds one for each of its last 6, min(wop_defer_mths, "
     "duration_mth), lags 1 to 6"),
    ("a pipeline with a gap, lags 1 to 5 and 7", _move_lag(11, 6, 7), {}, 11,
     "point_id 11: wop_pipeline_sec.csv holds 6 lags, its last 7, where a waiver point in "
     "force 66 months holds one for each of its last 6, min(wop_defer_mths, "
     "duration_mth), lags 1 to 6"),
    ("a full pipeline missing a lag", _drop_lag(11, 3), {}, 11,
     "point_id 11: wop_pipeline_sec.csv holds 5 lags, its last 6, where a waiver point in "
     "force 66 months holds one for each of its last 6, min(wop_defer_mths, "
     "duration_mth), lags 1 to 6"),
    ("a full pipeline missing its last lag", _drop_lag(11, 6), {}, 11,
     "point_id 11: wop_pipeline_sec.csv holds 5 lags, its last 5, where a waiver point in "
     "force 66 months holds one for each of its last 6, min(wop_defer_mths, "
     "duration_mth), lags 1 to 6"),
    ("a partial pipeline missing its last lag", _drop_lag(12, 4), {}, 12,
     "point_id 12: wop_pipeline_sec.csv holds 3 lags, its last 3, where a waiver point in "
     "force 4 months holds one for each of its last 4, min(wop_defer_mths, duration_mth), "
     "lags 1 to 4"),
    ("a deferred period lengthened", lambda t: t, {"wop_defer_mths": 7}, 11,
     "point_id 11: wop_pipeline_sec.csv holds 6 lags, its last 6, where a waiver point in "
     "force 66 months holds one for each of its last 7, min(wop_defer_mths, "
     "duration_mth), lags 1 to 7"),
    ("a deferred period shortened", lambda t: t, {"wop_defer_mths": 5}, 11,
     "point_id 11: wop_pipeline_sec.csv holds 6 lags, its last 6, where a waiver point in "
     "force 66 months holds one for each of its last 5, min(wop_defer_mths, "
     "duration_mth), lags 1 to 5"),
    ("a negative deferred period", lambda t: t, {"wop_defer_mths": -1}, 11,
     "point_id 11: wop_defer_mths must be 0 months or more, not -1"),
    # A count of months written as a float, which the compiled model holds as an int,
    # printed as it does.
    ("a deferred period lengthened, written as a float", lambda t: t,
     {"wop_defer_mths": 7.0}, 11,
     "point_id 11: wop_pipeline_sec.csv holds 6 lags, its last 6, where a waiver point in "
     "force 66 months holds one for each of its last 7, min(wop_defer_mths, "
     "duration_mth), lags 1 to 7"),
    ("a negative deferred period, written as a float", lambda t: t,
     {"wop_defer_mths": -1.0}, 11,
     "point_id 11: wop_defer_mths must be 0 months or more, not -1"),
]


@pytest.mark.parametrize("case, edit, refs, point, message", SHORT_PIPELINE,
                         ids=[c[0] for c in SHORT_PIPELINE])
def test_a_pipeline_the_frame_does_not_read_whole_is_refused_by_proj_len(
        tmp_path, case, edit, refs, point, message):
    """``proj_len()`` refuses a waiver point whose pipeline is not exactly its lags (§6.1).

    A point in force with the rider reads its pipeline at every lag from 1 to
    ``min(wop_defer_mths, duration_mth)`` in the frame's first months, and a sparse
    companion would read as a ``KeyError`` there, naming nothing.  So the frame refuses it
    first, naming the point, the lags held and the last held, and so does every report and
    the pipeline's accessor, which asks the frame first (:data:`SHORT_PIPELINE`).  ``Data``
    reads the companion either way.
    """
    model = _read_edited(tmp_path, lambda t: t, edit)
    try:
        for ref, value in refs.items():
            setattr(model.Projection, ref, value)
        model.Data.wop_pipeline()
        p = _point(model, point)
        _refused(p.result_cf, message)
        _refused(lambda: p.wop_deferred_init(1), message)
    finally:
        model.close()


def _share_too_soon(point, duration):
    """The message ``proj_len()`` gives a waiver point in force ``duration`` months, inside
    the shipped deferred period, whose opening waived share is 1e-6."""
    return (f"point_id {point}: wop_waived_frac_init is 1e-06, where a waiver point in "
            f"force {duration} months, no longer than wop_defer_mths, 6, has waived no "
            f"premium yet: 0")


# A waived share S cannot reach, as (case, the table's edit, the References set, the
# point, the message).  No incapacity runs the deferred period before the month after it,
# so a point in force no longer than it has waived nothing: point 12, 4 months in, is
# refused a share of 1e-6, and so is it moved to 6 months, the deferred period's last,
# and point 11, 66 months in, once the deferred period is lengthened to 66.  At 7 months
# S has waived a share, and T2's core restates S's waiver point there, at month 7, and at
# 6 with nothing waived: both accepted.
WAIVED_TOO_SOON = [
    ("a share waived inside the deferred period",
     _set("wop_waived_frac_init", [12], 1e-6), {}, 12, _share_too_soon(12, 4)),
    ("a share waived in the deferred period's last month",
     _then(_set("duration_mth", [12], 6), _set("wop_waived_frac_init", [12], 1e-6)), {},
     12, _share_too_soon(12, 6)),
    ("a share waived inside a deferred period lengthened to 66", lambda t: t,
     {"wop_defer_mths": 66}, 11,
     f"point_id 11: wop_waived_frac_init is {_committed().at[11, 'wop_waived_frac_init']}, "
     f"where a waiver point in force 66 months, no longer than wop_defer_mths, 66, has "
     f"waived no premium yet: 0"),
    ("a share waived inside a deferred period lengthened to 66, written as a float",
     lambda t: t, {"wop_defer_mths": 66.0}, 11,
     f"point_id 11: wop_waived_frac_init is {_committed().at[11, 'wop_waived_frac_init']}, "
     f"where a waiver point in force 66 months, no longer than wop_defer_mths, 66, has "
     f"waived no premium yet: 0"),
]


@pytest.mark.parametrize("case, edit, refs, point, message", WAIVED_TOO_SOON,
                         ids=[c[0] for c in WAIVED_TOO_SOON])
def test_a_waived_share_the_deferred_period_has_not_run_is_refused(tmp_path, case, edit,
                                                                  refs, point, message):
    """``proj_len()`` refuses a waived share on a point in force no longer than the
    deferred period (§6.1, T5).

    ``Data`` reads the table, since its rule is a product's: the deferred period is
    ``wop_defer_mths``, a Reference of the projection, which ``Data`` cannot see, so the
    frame refuses the point, naming it, as it refuses a pipeline of the wrong length
    (:data:`WAIVED_TOO_SOON`).  Every Reference is set on a model just read (K7).
    """
    model = _read_edited(tmp_path, edit)
    try:
        for ref, value in refs.items():
            setattr(model.Projection, ref, value)
        model.Data.model_point_table()
        _refused(_point(model, point).result_cf, message)
    finally:
        model.close()


# The waiver's two annual rates at the edges of their domain, as (case, the Reference, its
# value, what the model does): "accepted", every waiver point projected, its waived share
# inside 0 to 1, and the twin of S's waiver point S's in every cell; "rate", proj_len()
# refusing the Reference on every waiver point.  Each rate is one Reference with no
# factor, which Term_UK_S leaves uncapped, so that past 1 its monthly rate,
# 1 - (1 - r)^(1/12), is complex there: 0 and 1 are in the rate's range, the float next
# outside each and NaN are not.  Inside it the share stays inside 0 to 1, the incidence
# falling on the active lives alone: at the shipped recovery rate and deferred period an
# incidence of 0.856 a year, which took S's waiver point's share past 1 at month 19 while
# both models counted the deferred lives among those who can fall ill, now peaks at 0.652,
# and one of 1 at 0.806.  A rate written as an int, which the compiled model holds as a
# float, is refused in the same words in both.
WAIVER_RATES = [
    *[(f"wop_inc_rate at {case}", "wop_inc_rate", value, outcome)
      for case, value, outcome in (
          ("0", 0.0, "accepted"), ("0.855", 0.855, "accepted"),
          ("0.856", 0.856, "accepted"), ("1", 1.0, "accepted"),
          ("the float below 0", math.nextafter(0.0, -1.0), "rate"),
          ("the float above 1", math.nextafter(1.0, 2.0), "rate"),
          ("the int 2", 2, "rate"), ("NaN", math.nan, "rate"))],
    *[(f"wop_rec_rate at {case}", "wop_rec_rate", value, outcome)
      for case, value, outcome in (
          ("0", 0.0, "accepted"), ("1", 1.0, "accepted"),
          ("the float below 0", math.nextafter(0.0, -1.0), "rate"),
          ("the float above 1", math.nextafter(1.0, 2.0), "rate"),
          ("the int -1", -1, "rate"), ("NaN", math.nan, "rate"))],
]


@pytest.mark.parametrize("case, ref, value, outcome", WAIVER_RATES,
                         ids=[c[0] for c in WAIVER_RATES])
def test_a_waiver_rate_outside_its_domain_is_refused(case, ref, value, outcome):
    """A waiver rate outside 0 to 1 is refused on a waiver point, and inside it every
    waiver point projects its share inside 0 to 1 (§6.1, T5).

    ``wop_inc_rate`` and ``wop_rec_rate`` are each one Reference, with no factor and no
    annual-rate cell, so the caps never reached them and ``Term_UK_S`` leaves them
    uncapped: past 1, ``wop_inc_rate_mth`` and ``wop_rec_rate_mth`` are complex there, and
    below 0 negative.  This model keeps S's formulas, and its frame refuses such a rate on
    every waiver point, naming the point and the Reference, as it refuses a negative
    deferred period; the float next outside either edge is refused, and so is NaN, which
    no comparison passes.  Inside it, at 0 and 1 for either rate and at incidences of
    0.855 and 0.856, every waiver point projects, its share inside 0 to 1, and the twin of
    S's waiver point is S's in every cell (:data:`WAIVER_RATES`).  The incidence falls on
    the active lives alone, in both models, so the share cannot pass 1, where on the base
    both models once took, ``1 - u``, it passed 1 from an incidence of about 0.8552 and
    this model refused it.  A point without the rider reads neither rate, and projects
    whatever they are.  The rate is set in both models as each is read, before either
    computes anything, the form that runs compiled unchanged (K7).
    """
    sec = mx.read_model(model_path(SEC), name=_name("rates"))
    s = mx.read_model(model_path(TWIN), name=_name("rates_s"))
    try:
        setattr(sec.Projection, ref, value)
        setattr(s.Projection, ref, value)
        table = sec.Data.model_point_table()
        waiver = [label for label in table.index if table.at[label, "wop"]]
        twin = _label(table, "twin", 7, 0)
        s_proj = _point(s, 7)
        if outcome == "rate":
            for label in waiver:
                _refused(_point(sec, label).result_cf,
                         f"point_id {label}: {ref} must be a number from 0 to 1, "
                         f"not {float(value)}")
            if value > 1.0:
                assert isinstance(s_proj.cells[f"{ref}_mth"](), complex), case
        else:
            for label in waiver:
                p = _point(sec, label)
                assert len(p.result_cf()) == p.proj_len()
                assert all(0.0 <= p.wop_waived_frac(t) <= 1.0
                           for t in range(p.proj_len())), label
            _sweep_s(s_proj)
            assert _compare(s_proj, _point(sec, twin), 0,
                            TWIN_EXEMPT_DEFAULT | SPEC.exempt) == [], case
        assert len(_point(sec, 1).result_cf()) == 300
    finally:
        sec.close()
        s.close()


def test_the_waived_share_at_its_worst_stays_inside_0_to_1(tmp_path):
    """At an incidence of 1 and no recovery, the worst the rates allow, the waived share
    reaches 1 and stays there, on every waiver point (§6.1).

    The three shares, active, deferred and waived, partition the in-force, so the waived
    share is at most what the other two leave.  ``wop_waived_frac`` refuses no share any
    more: at rates from 0 to 1, which ``proj_len()`` holds them to, and from an opening
    state whose waived and deferred shares ``Data`` holds to 1 or less, nothing takes it
    outside 0 to 1.  The share can pass 1 only by rounding, at an incidence near 1 with no
    recovery, by a few units in the last place, as in ``Term_UK_S``, and a refusal there
    would refuse a valid input.  At its worst, an incidence of 1 a year with no recovery,
    every life active in the first month on the books falls incapacitated in it and none
    recovers, so on each waiver point every life is waived once the deferred period has
    run, from ``t_entry() + 7``, and no premium is collected after: the share is 1 there
    to the last bit and never more, and the active share 0 from the second month on.  On
    the points in force it is 1 to the last bit because the active share opens at what the
    waived and deferred shares leave, summed in the order the waived share takes them in.
    The twin of S's waiver point is S's in every cell.  And at an incidence of 1 with the
    shipped recovery the share of every waiver point stays below 1.
    """
    sec = mx.read_model(model_path(SEC), name=_name("worst"))
    s = mx.read_model(model_path(TWIN), name=_name("worst_s"))
    try:
        for model in (sec, s):
            model.Projection.wop_inc_rate = 1.0
            model.Projection.wop_rec_rate = 0.0
        table = sec.Data.model_point_table()
        waiver = [label for label in table.index if table.at[label, "wop"]]
        assert len(waiver) == 4
        for label in waiver:
            p = _point(sec, label)
            assert len(p.result_cf()) == p.proj_len()
            full = p.t_entry() + 7
            u = [p.wop_waived_frac(t) for t in range(p.proj_len())]
            assert all(0.0 <= x <= 1.0 for x in u), label
            assert u[full:] == [1.0] * (p.proj_len() - full), label
            assert all(x < 1.0 for x in u[:full]), label
            assert all(p.wop_active_frac(t) == 0.0
                       for t in range(full - 6, p.proj_len())), label
            assert all(p.premiums(t) == 0.0 for t in range(full, p.proj_len())), label
        s_proj = _point(s, 7)
        _sweep_s(s_proj)
        assert _compare(s_proj, _point(sec, _label(table, "twin", 7, 0)), 0,
                        TWIN_EXEMPT_DEFAULT | SPEC.exempt) == []
    finally:
        sec.close()
        s.close()
    sec = mx.read_model(model_path(SEC), name=_name("worst_shipped"))
    try:
        sec.Projection.wop_inc_rate = 1.0
        table = sec.Data.model_point_table()
        for label in [label for label in table.index if table.at[label, "wop"]]:
            p = _point(sec, label)
            assert all(0.0 <= p.wop_waived_frac(t) < 1.0
                       for t in range(p.proj_len())), label
    finally:
        sec.close()


def test_a_waived_share_rounding_takes_past_1_is_projected_as_s_projects_it():
    """At an incidence of 0.999999 a year with no recovery, rounding alone takes the waived
    share a unit in the last place past 1, and every waiver point projects (§6.1).

    The share's sum, the waived lives less recoveries plus each month's entrants, is 1 or
    less in exact arithmetic, and computed, it reaches the float above 1 on the twin of S's
    waiver point and on the same point issued 13 months on, as in ``Term_UK_S``.  This is
    the case ``model-sec.md`` gives for dropping the refusal of a share outside 0 to 1 from
    ``wop_waived_frac``: a refusal there would refuse these inputs for their last bit.  So
    every waiver point projects; the twin is S's in every cell, and the point issued 13
    months on is S's projection moved on, but for the expense inflation the valuation clock
    moves (:func:`_continues_s`); and the largest share on any of them, and on S's point,
    is that float, ``1.0000000000000002``.
    """
    sec = mx.read_model(model_path(SEC), name=_name("rounding"))
    s = mx.read_model(model_path(TWIN), name=_name("rounding_s"))
    try:
        for model in (sec, s):
            model.Projection.wop_inc_rate = 0.999999
            model.Projection.wop_rec_rate = 0.0
        table = sec.Data.model_point_table()
        largest = 0.0
        for label in [label for label in table.index if table.at[label, "wop"]]:
            p = _point(sec, label)
            assert len(p.result_cf()) == p.proj_len()
            largest = max([largest] + [p.wop_waived_frac(t) for t in range(p.proj_len())])
        assert largest == math.nextafter(1.0, 2.0) == 1.0000000000000002
        s_proj = _point(s, 7)
        _sweep_s(s_proj)
        assert max(s_proj.wop_waived_frac(t) for t in range(s_proj.proj_len())) == largest
        assert _compare(s_proj, _point(sec, _label(table, "twin", 7, 0)), 0,
                        TWIN_EXEMPT_DEFAULT | SPEC.exempt) == []
        assert _continues_s(s_proj, _point(sec, _label(table, "future", 7, -13)),
                            -13) == []
    finally:
        sec.close()
        s.close()


# The family income benefit's commutation discount, fib_commute_disc_rate, at the edges
# of its domain, as (case, its value, what the model does): "accepted", every family
# income benefit point projected; "refused", proj_len() refusing the Reference on every
# family income benefit point; "overflow", the discount's power past the largest float,
# Python's OverflowError, raised alike by S, by this model and, compiled, by Python's own
# power (Projection.annuity_certain_factor).  The commuted value discounts at
# (1 + r)^(-m/12): at -1 that power divides by zero, below -1 it has no real value, which
# S projects as a complex number, and an infinite rate gives a factor of 0, NaN one of
# NaN.  A rate of 0 is the closed form's limit, m, in S and here; at 1e-17, where 1 + r is
# 1, this model's monthly rate is 0 and the factor m, where S, which tests the annual rate,
# divides by zero; and so at PAST_ONE, the least float whose 1 + r is not 1, 1 + 2**-52,
# whose twelfth root still rounds to 1, so that the factor tests the monthly rate and not
# 1 + r.  At -0.99 the factor is S's.  The float above -1 is in the domain, its power past
# the largest float on every family income benefit point of the table.  And -2 written as
# an int, which the compiled model holds as -2.0, is refused in the same words in both.
PAST_ONE = math.nextafter(2.0 ** -53, 1.0)
COMMUTE_RATES = [
    ("0", 0.0, "accepted"), ("1e-17", 1e-17, "accepted"),
    ("the float past 1 + r == 1", PAST_ONE, "accepted"), ("-0.99", -0.99, "accepted"),
    ("-1", -1.0, "refused"), ("-2", -2.0, "refused"), ("the int -2", -2, "refused"),
    ("NaN", math.nan, "refused"), ("inf", math.inf, "refused"),
    ("-inf", -math.inf, "refused"),
    ("the float above -1", math.nextafter(-1.0, 0.0), "overflow"),
]

# What S makes of each refused rate, on its point 4's annuity certain at 300 months: a
# raise, by its type, or the value.
S_COMMUTE = {"-1": "ZeroDivisionError", "-2": complex, "the int -2": complex, "NaN": "nan",
             "inf": 0.0, "-inf": 0.0}


def _overflow_text():
    """Python's float power's ``OverflowError``, as the platform words it."""
    return f"OverflowError: ({errno.ERANGE}, {os.strerror(errno.ERANGE)!r})"


@pytest.mark.parametrize("case, value, outcome", COMMUTE_RATES,
                         ids=[c[0] for c in COMMUTE_RATES])
def test_a_commutation_discount_outside_its_domain_is_refused(case, value, outcome):
    """A commutation discount that is not a finite number above -1 is refused on every
    family income benefit point, and inside it the factor is S's or its limit (T5).

    ``fib_commute_disc_rate`` is one Reference, which ``Term_UK_S`` reads unchecked, and
    the commuted value raises, goes complex or goes to 0 or NaN outside its domain, so
    this model's frame refuses it on every family income benefit point, naming the point
    and the Reference, as it refuses a waiver rate outside 0 to 1; S's own outcome is
    asserted beside it (:data:`S_COMMUTE`).  Inside it, every family income benefit point
    projects and every other point projects whatever the rate: at 0 and at -0.99 the
    twins of S's family income benefit points, 3 and 4, are S's in every cell, holding
    the closed form's limit and S's power against S; at 1e-17, where ``1 + r`` is 1, and
    at :data:`PAST_ONE`, where it is not, the monthly rate is 0 and the factor is ``m``,
    where S divides by zero, a departure.  A refusal prints the rate as a float, as the
    compiled model holds it, an int among the rates refused.  The
    float above -1 is accepted, and its power passes the largest float, Python's
    ``OverflowError`` in S and here alike.  The rate is set in both models as each is
    read, before either computes anything, the form that runs compiled unchanged (K7);
    the compiled refusal test holds the compiled model to each refusal and overflow, and
    C4 holds it to modelx at 0 and 1e-17.
    """
    sec = mx.read_model(model_path(SEC), name=_name("discount"))
    s = mx.read_model(model_path(TWIN), name=_name("discount_s"))
    try:
        sec.Projection.fib_commute_disc_rate = value
        s.Projection.fib_commute_disc_rate = value
        table = sec.Data.model_point_table()
        fib = [label for label in table.index if table.at[label, "shape"] == "fib"]
        assert len(fib) == 3, fib
        if outcome == "refused":
            for label in fib:
                _refused(_point(sec, label).result_cf,
                         f"point_id {label}: fib_commute_disc_rate must be a finite "
                         f"number above -1, not {float(value)}")
            want = S_COMMUTE[case]
            try:
                got = _point(s, 4).annuity_certain_factor(300)
            except Exception as err:            # S's own refusal of the rate
                assert _raised(err).startswith(f"{want}:"), (case, _raised(err))
            else:
                assert (isinstance(got, want) if isinstance(want, type)
                        else (math.isnan(got) if want == "nan" else got == want)), (
                    case, got)
        elif outcome == "overflow":
            for label in fib:
                with pytest.raises(Exception) as raised:
                    _point(sec, label).result_cf()
                assert _raised(raised.value) == _overflow_text(), (label, raised.value)
            with pytest.raises(Exception) as raised:
                _point(s, 4).result_cf()
            assert _raised(raised.value) == _overflow_text(), raised.value
        else:
            for label in fib:
                p = _point(sec, label)
                assert len(p.result_cf()) == p.proj_len() and p.check_fib_ledger(), label
            p = _point(sec, 4)
            if value != 0.0 and (1.0 + value) ** (1.0 / 12.0) - 1.0 == 0.0:
                assert p.annuity_certain_factor(300) == 300.0
                with pytest.raises(Exception) as raised:
                    _point(s, 4).annuity_certain_factor(300)
                assert _raised(raised.value).startswith("ZeroDivisionError"), raised.value
            else:
                for point_id in (3, 4):
                    s_proj = _point(s, point_id)
                    _sweep_s(s_proj)
                    assert _compare(s_proj, _point(sec, point_id), 0,
                                    TWIN_EXEMPT_DEFAULT | SPEC.exempt) == [], (case,
                                                                              point_id)
                if value == 0.0:
                    assert p.annuity_certain_factor(300) == 300.0
        others = [label for label in table.index if label not in fib]
        for label in others:
            p = _point(sec, label)
            assert len(p.result_cf()) == p.proj_len(), label
    finally:
        sec.close()
        s.close()


def test_a_select_period_written_as_a_float_reads_the_table_as_an_int():
    """``select_period`` 3.0 projects what 3 projects, as the compiled model, which holds
    the Reference as an int, does.

    ``select_factor`` reads ``Data.select_factor_array`` at ``min(duration(t),
    select_period)``, which a float period makes a float from its third year, an index
    numpy refuses where ``Term_UK_S``'s lookup by label read it; the cell reads the
    duration as an ``int``.  On S's waiver point's twin, on the select basis, every cell
    of the report and the select factor at every month agree, to the bit, with the
    period an int and a float.
    """
    as_int = mx.read_model(model_path(SEC), name=_name("period_int"))
    as_float = mx.read_model(model_path(SEC), name=_name("period_float"))
    try:
        as_int.Projection.select_period = 3
        as_float.Projection.select_period = 3.0
        p, q = _point(as_int, 7), _point(as_float, 7)
        assert p.is_select_basis() and p.proj_len() > 36
        assert frame_mismatches(p.result_cf(), q.result_cf(), rtol=0, atol=0) == []
        assert [p.select_factor(t) for t in range(p.proj_len())] == [
            q.select_factor(t) for t in range(q.proj_len())]
    finally:
        as_float.close()
        as_int.close()


def test_the_edges_of_the_in_force_interface_are_accepted(sec_model, tmp_path):
    """A zero count, whole numbers in any type, the horizon and each bound's edge are read.

    A count of 0 is a point that projects zeros; ``66.0`` is a whole number of months,
    read back as the int the policy clock counts in; a policy issued 120 months after the
    valuation date, the shipped ``future_horizon_mth``, is the last one the table admits,
    with a frame of 360 months, 240 of cover after 120 before issue.  A row valued in its
    first month, 1, holds a lapse ratio, a ledger and a pipeline of one lag, the state a
    policy in force holds where one not yet in force holds none.  The indexed point valued
    on its first anniversary, 12, holds no increase, the anniversary being month 0's own,
    which the projection makes at ``t = 0``; one month on, at 13, it holds the first, and
    steps next at ``t = 11``, policy month 24: the first-year rule's edges, read either
    side.  And each bound of the contract at its edge projects: a 50-year term, a family
    income benefit of 40 years, issue at 18, of each life of a joint point, and cover to
    90, 70 on the family income benefit, of each life.  A single life's second age, which
    no cell reads and ``Data`` holds as 0, is read whatever it holds, here 1e300, past what
    an int64 can hold, on point 2.  The extra rows are copies of the indexed point under
    labels of their own, 21 and 22.
    """
    committed = _committed()
    last = _label(committed, "derived", 1, 299)
    future = _label(committed, "future", 7, -13)
    first = _label(committed, "derived", 7, 4)
    fib = _label(committed, "derived", 3, 66)
    indexed = _label(committed, "derived", 5, 60)
    copies = {21: {"duration_mth": 12, "idx_factor_init": 1.0, "idx_prem_factor_init": 1.0},
              22: {"duration_mth": 13, "idx_factor_init": 1.03,
                   "idx_prem_factor_init": 1.045}}

    def edit(table):
        extra = []
        for label, changes in copies.items():
            row = table.loc[[indexed]].assign(policy_id=f"TA-9000{label}", **changes)
            row.index = pd.Index([label], name="point_id")
            extra.append(row)
        table = pd.concat([table, *extra])
        table = _set("policy_count", [last], 0.0)(table)
        table = _set("duration_mth", [first], 1)(table)
        table = table.assign(duration_mth=table["duration_mth"].astype(float))
        table = _set("duration_mth", [future], -120.0)(table)
        table = _set("policy_term", [1], 50)(table)
        table = _set("age_at_entry", [1], 40)(table)
        table = _set("policy_term", [3], 40)(table)
        table = _set("age_at_entry", [3], 30)(table)
        table = _set("age_at_entry", [6], 18)(table)
        table = _set("joint_age", [6], 65)(table)
        table = _set("joint_age", [2], 1e300)(table)
        return _set("age_at_entry", [2], 18)(table)

    model = _read_edited(tmp_path, edit, _lines(lambda t: t[(t["point_id"] != first)
                                                           | (t["lag"] == 1)]))
    try:
        read = model.Data.model_point_table()
        assert read["duration_mth"].dtype == float
        df = _point(model, last).result_cf()
        assert len(df) == 1 and (df == 0.0).all().all()
        p = _point(model, fib)
        assert p.duration_mth(0) == 66 and type(p.duration_mth(0)) is int
        assert frame_mismatches(_point(sec_model, fib).result_cf(), p.result_cf(),
                                rtol=0, atol=0) == []
        late = _point(model, future)
        assert (late.t_entry(), late.proj_len(), late.pols_new_biz(120)) == (120, 360, 1.0)
        one = _point(model, first)
        assert (one.duration_mth_init(), one.proj_len(), one.lapse_cum_init() > 0.0) == (
            1, 239, True)
        assert one.wop_deferred_init(1) > 0.0
        on, after = _point(model, 21), _point(model, 22)
        assert len(on.result_cf()) == on.proj_len() == 288
        assert len(after.result_cf()) == after.proj_len() == 287
        assert (on.idx_factor(0), on.idx_prem_factor(0)) == (1.03, 1.045)
        assert (after.idx_factor(10), after.idx_prem_factor(10)) == (1.03, 1.045)
        assert after.idx_factor(11) == pytest.approx(1.03 ** 2, rel=1e-15)
        for point, months in ((1, 600), (3, 480), (6, 300), (2, 300)):
            assert len(_point(model, point).result_cf()) == months, point
            assert _point(model, point).check_pols_roll_fwd(), point
    finally:
        model.close()


def _every_state_months(start, end):
    """The S months a point whose S frame runs from ``start`` to ``end`` is restated at.

    By default the edges of its windows (USLIB-SEC-PLAN.md §5.2, T5): every month of the
    first policy year, the first anniversary and the month after it, through which the
    waiver's pipeline fills and ``Data``'s rules for a policy not yet in force and for one
    before its first increase end, an anniversary in the valuation month being month 0's
    own (D6), each anniversary and the month before it, and the last month of the frame,
    before expiry.  With ``UKLIB_SEC_FULL=1``, every month.  Each after ``start``, the
    twin's month.
    """
    if SEC_FULL:
        return list(range(start + 1, end))
    months = {*range(1, 14), end - 1, *(m for a in range(12, end, 12) for m in (a - 1, a))}
    return sorted(m for m in months if start < m < end)


def _states(s):
    """Each ``(S point, month)`` of :func:`_every_state_months` on every point of ``s``."""
    labels = s.Data.model_point_table().index
    return [(point_id, d) for key, point_id in zip(point_keys(s), labels)
            for d in _every_state_months(projection(s, key).proj_start(),
                                         projection(s, key).proj_len())]


def _restated(root, s, states):
    """The twins of ``s``'s points and a row in force at each of ``states``, ``(S point,
    month)``, built by the generator out of ``s`` into a copy of the product directory:
    ``(folder, table)``."""
    spec = dataclasses.replace(SPEC, derived=tuple(states), future=())
    table, companions = build_sec_table(spec, s)
    return _sec_inputs(root, table, companions[PIPELINE]), table


def _states_apart(a, b):
    """The state columns, the count's among them, in which two tables of :func:`_restated`
    differ on the states, ``(S policy, month)``, they share, of which there must be some."""
    both = a.index.intersection(b.index)
    assert len(both), "the two tables share no state"
    return {c for c in ("policy_count", *STATE) if (a.loc[both, c] != b.loc[both, c]).any()}


def _refused_in_force(folder, refs):
    """What ``Data`` and ``proj_len()`` refuse of the table in ``folder``, read with
    ``refs`` set first: ``Data``'s refusal, or each row's ``proj_len()``'s, each by the line
    that names it.  Each row is released once asked (:func:`_release`)."""
    model = mx.read_model(folder, name=_name("every"))
    try:
        for ref, value in refs.items():
            setattr(model.Projection, ref, value)
        try:
            model.Data.model_point_table()
            model.Data.wop_pipeline()
        except Exception as err:                # reported, with the rows' states
            return [f"Data: {_raised(err)}"]
        refused = []
        for key in point_keys(model):
            try:
                projection(model, key).proj_len()
            except Exception as err:            # reported, so every row is asked
                refused.append(_raised(err))
            _release(model, key)
        return refused
    finally:
        model.close()


def test_every_state_s_reaches_is_accepted_in_force(s_model, spliced, tmp_path):
    """Every state ``Term_UK_S`` reaches is a valid opening state (T5).

    ``Data``'s rules and ``proj_len()``'s hold an opening state to what a policy in force
    can be, so they must accept each state the S model reaches: a rule exercised only on
    the rows the other tests choose could refuse a state S reaches elsewhere (D6).  So each
    point of S is restated in force by the generator at the edges of its windows, or with
    ``UKLIB_SEC_FULL=1`` at every month of its frame (:func:`_every_state_months`), into
    one table and one pipeline beside the twins: ``Data`` reads both, and no row's
    ``proj_len()`` refuses it (USLIB-SEC-PLAN.md §5.2, T5, precised at M10).  The splice's
    switches move four of the states S reaches: the count, the lapse ratio, and the deaths
    since issue and the streams of them in payment, through the loading.  They leave alone
    the factors, which the RPI alone moves, the waived share and the pipeline, which read
    no count, and the commission paid at issue, a rate on the premium.  The cap's
    References move the count and the ledger, to 0 once the cap binds.  Expense inflation
    moves no state.  So the test runs on each set of inputs on which those states differ
    (precised at M9), and asserts which states each moves:

    * S as shipped, its eight points under its own References, the switches off, as T1
      and the committed rows read it (``s_model``);
    * the splice's, its points and five variants under :data:`SPLICED_REFS`, the switches
      on (``spliced``);
    * the cap's, its point under :data:`SPLICED_REFS` on :data:`CAPPED`'s table, whose
      count falls to exactly 0 once the cap binds, which neither other set reaches.

    ``Term_UK_SEC`` refuses no state ``Term_UK_S`` reaches on these inputs, so none is set
    aside.  At rates far outside the product it does, by a unit in the last place: at an
    incidence of 0.999999 a year with no recovery, rounding takes S's waived share past 1,
    alone or with the deferred shares, and ``Data.model_point_table``'s rule 6 and
    ``Data.wop_pipeline``'s rule 8 refuse S point 7 restated at 208 of its 239 months,
    from month 32.  No rule is widened for it: each refuses a share no policy can hold, by
    its last bit.
    """
    capped = _capped_s(tmp_path / "capped")
    try:
        sets = {"shipped": (s_model, {}), "spliced": (spliced[0], SPLICED_REFS),
                "capped": (capped, SPLICED_REFS)}
        found, states = {}, {}
        for tag, (s, refs) in sets.items():
            reached = _states(s)
            folder, rows = _restated(tmp_path / tag, s, reached)
            assert len(rows) == len(s.Data.model_point_table()) + len(reached)
            states[tag] = rows.set_index(["source_policy_id", "source_mth"])
            refused = _refused_in_force(folder, refs)
            if refused:
                found[tag] = f"{len(refused)} refused, first: {refused[:5]}"
    finally:
        capped.close()
    assert not found, found
    shipped, splice, cap = states["shipped"], states["spliced"], states["capped"]
    apart = _states_apart(shipped, splice)
    assert apart == {"policy_count", "lapse_cum_init", "fib_cum_init",
                     "fib_streams_init"}, apart
    count = cap["policy_count"]
    assert (count == 0.0).any() and (count > 0.0).any()
    assert (cap.loc[count == 0.0, "fib_cum_init"] == 0.0).all()


# ---------------------------------------------------------------------------
# The assumption tables
#
# Data checks each table before a value of it is read, in the cell the projection takes the
# table's extent from (UKLIB-SEC-PLAN.md §4; USLIB-SEC-PLAN.md §7.1, *Precised at M3*,
# item 9).  Each case is the shipped tables with one fault, read from a copy, refused by
# its Data cell alone, naming the file, the column and its lines, the header line 1, and
# through a projection of the first point that reads the table.  The lines are the
# shipped files': mort_table.csv holds M N at ages 18 to 100 on lines 2 to 84, then M S,
# F N and F S, 83 lines each; select_factor_table.csv durations 0 to 5 on lines 2 to 7;
# lapse_table.csv policy years 1 to 6 on lines 2 to 7.


def _written(column, value, where):
    """An edit of a table that writes ``value`` into ``column`` on the rows ``where``
    picks."""
    def edit(table):
        cells = table[column].astype(object)
        cells[where(table)] = value
        return table.assign(**{column: cells})
    return edit


def _mort(sex, smoker, age):
    return lambda t: (t["sex"] == sex) & (t["smoker"] == smoker) & (t["age"] == age)


def _key_is(column, value):
    return lambda t: t[column] == value


def _dropped(where):
    return lambda table: table[~where(table)].reset_index(drop=True)


def _repeated(where):
    return lambda table: pd.concat([table, table[where(table)]], ignore_index=True)


MORT, SELECT, LAPSE = "mort_table.csv", "select_factor_table.csv", "lapse_table.csv"
RATE = f"{MORT}: mort_rate must be a number from 0 to 1; it is not on line "
FACTOR = f"{SELECT}: factor must be a number, zero or more; it is not on line "
LAPSE_RATE = f"{LAPSE}: lapse_rate must be a number from 0 to 1; it is not on line "


def _ages_apart(*faults):
    """The message of a mortality table whose groups do not run one row an age, naming
    ``faults``: each repeat with its lines, each span a group lacks."""
    return (f"{MORT}: the ages of each sex and smoker status must run from 18 to 100, the "
            f"table's first and last, one row an age, none below 0; " + "; ".join(faults))


DURATIONS = (f"{SELECT}: the durations must run from 0, one row a duration, without a gap "
             f"or a repeat; ")
YEARS = (f"{LAPSE}: the policy years must run from 1, one row a year, without a gap or a "
         f"repeat; ")


# A table a reader cannot read, or whose value is not a number in its range, as (case, the
# file, its edit, the Data cell that refuses it, its message, the point a projection meets
# it on).  The mortality table is read by every point, the select factors by the select
# point, 7, alone, and the lapse table by every point.  A value no point reads is refused
# too: the female smoker at 100, a select factor past every point's duration it is not.
UNREADABLE = [
    ("a blank mortality rate", MORT, _written("mort_rate", float("nan"), _mort("M", "N", 50)),
     "mort_age_first", RATE + "[34]", 1),
    ("a text mortality rate", MORT, _written("mort_rate", "low", _mort("M", "N", 35)),
     "mort_age_first", RATE + "[19]", 1),
    ("an infinite mortality rate", MORT,
     _written("mort_rate", float("inf"), _mort("F", "S", 100)),
     "mort_age_first", RATE + "[333]", 1),
    ("a negative mortality rate", MORT, _written("mort_rate", -0.001, _mort("F", "N", 40)),
     "mort_age_first", RATE + "[190]", 1),
    ("a mortality rate past 1", MORT, _written("mort_rate", 1.5, _mort("M", "S", 60)),
     "mort_age_first", RATE + "[127]", 1),
    ("two lines at fault", MORT, _then(
        _written("mort_rate", float("nan"), _mort("M", "N", 18)),
        _written("mort_rate", float("nan"), _mort("F", "S", 18))),
     "mort_age_first", RATE + "[2, 251]", 1),
    ("an age not whole", MORT, _written("age", 35.5, _mort("M", "N", 35)),
     "mort_age_first", f"{MORT}: age must be a whole number; it is not on line [19]", 1),
    ("an age written as text", MORT, _written("age", "x", _mort("F", "N", 18)),
     "mort_age_first", f"{MORT}: age must be a whole number; it is not on line [168]", 1),
    ("an unknown sex", MORT, _written("sex", "X", _mort("F", "S", 18)),
     "mort_age_first",
     f"{MORT}: sex must be M or F, and smoker N or S; they are not on line [251]", 1),
    ("an age missing", MORT, _dropped(_mort("M", "N", 50)), "mort_age_first",
     _ages_apart("no line holds sex M, smoker N, age 50"), 1),
    ("an age twice", MORT, _repeated(_mort("F", "S", 40)), "mort_age_first",
     _ages_apart("sex F, smoker S, age 40 repeats on lines [273, 334]"), 1),
    ("a group missing", MORT, _dropped(lambda t: (t["sex"] == "M") & (t["smoker"] == "S")),
     "mort_age_first", _ages_apart("no line holds sex M, smoker S, ages 18 to 100"), 1),
    ("a group shorter", MORT, _dropped(_mort("F", "N", 100)), "mort_age_first",
     _ages_apart("no line holds sex F, smoker N, age 100"), 1),
    ("a blank select factor", SELECT, _written("factor", float("nan"), _key_is("duration", 2)),
     "select_last_duration", FACTOR + "[4]", 7),
    ("a negative select factor", SELECT, _written("factor", -0.5, _key_is("duration", 0)),
     "select_last_duration", FACTOR + "[2]", 7),
    ("an infinite select factor", SELECT,
     _written("factor", float("inf"), _key_is("duration", 5)),
     "select_last_duration", FACTOR + "[7]", 7),
    ("a duration not whole", SELECT, _written("duration", 2.5, _key_is("duration", 2)),
     "select_last_duration",
     f"{SELECT}: duration must be a whole number; it is not on line [4]", 7),
    ("a duration missing", SELECT, _dropped(_key_is("duration", 3)), "select_last_duration",
     DURATIONS + "no line holds duration 3", 7),
    ("a duration twice", SELECT, _repeated(_key_is("duration", 1)), "select_last_duration",
     DURATIONS + "duration 1 repeats on lines [3, 8]", 7),
    ("no duration 0", SELECT, _dropped(_key_is("duration", 0)), "select_last_duration",
     DURATIONS + "no line holds duration 0", 7),
    ("a blank lapse rate", LAPSE, _written("lapse_rate", float("nan"),
                                           _key_is("policy_year", 3)),
     "lapse_last_year", LAPSE_RATE + "[4]", 1),
    ("a lapse rate past 1", LAPSE, _written("lapse_rate", 1.5, _key_is("policy_year", 6)),
     "lapse_last_year", LAPSE_RATE + "[7]", 1),
    ("a negative lapse rate", LAPSE, _written("lapse_rate", -0.1, _key_is("policy_year", 1)),
     "lapse_last_year", LAPSE_RATE + "[2]", 1),
    ("a text lapse rate", LAPSE, _written("lapse_rate", "high", _key_is("policy_year", 2)),
     "lapse_last_year", LAPSE_RATE + "[3]", 1),
    ("a policy year not whole", LAPSE, _written("policy_year", 2.5,
                                                _key_is("policy_year", 2)),
     "lapse_last_year",
     f"{LAPSE}: policy_year must be a whole number; it is not on line [3]", 1),
    ("a policy year missing", LAPSE, _dropped(_key_is("policy_year", 3)), "lapse_last_year",
     YEARS + "no line holds policy_year 3", 1),
    ("a policy year twice", LAPSE, _repeated(_key_is("policy_year", 4)), "lapse_last_year",
     YEARS + "policy_year 4 repeats on lines [5, 8]", 1),
    ("no policy year 1", LAPSE, _dropped(_key_is("policy_year", 1)), "lapse_last_year",
     YEARS + "no line holds policy_year 1", 1),
]


@pytest.mark.parametrize("case, file, edit, cell, message, point", UNREADABLE,
                         ids=[c[0] for c in UNREADABLE])
def test_a_table_a_reader_cannot_read_is_refused_naming_its_lines(tmp_path, case, file, edit,
                                                                  cell, message, point):
    """``Data`` refuses an assumption table before a value of it is read (§4, T5).

    ``Term_UK_S`` reads a blank rate as NaN, which its cap would keep and every flow
    carry; an infinite one, which the cap reads as certain death; a key that is not whole,
    gapped or repeated, as a ``KeyError`` only where a projection reaches it, or as a wrong
    row.  Here the extent cell the projection asks first refuses each, naming the file, the
    column and its lines (:data:`UNREADABLE`), and so does a projection of a point that
    reads the table.
    """
    model = _read_edited(tmp_path, lambda t: t, edits={file: edit})
    try:
        _refused(model.Data.cells[cell], message)
        _refused(_point(model, point).result_cf, message)
    finally:
        model.close()


def test_a_read_beyond_a_table_is_refused_naming_its_point(tmp_path):
    """A read past a table's extent is refused by the one cell that reads it, by name.

    ``Term_UK_S``'s lookups raise ``KeyError`` beyond a table, naming no point.  Here the
    select factor's read past the table's last duration, where ``select_period`` runs
    beyond it, and the mortality rate's at an attained age outside the table, above or
    below it, each raise ``ValueError`` naming the point and the key.  The lapse table
    takes its last year for every later one, as ``Term_UK_S`` does, so no read is beyond
    it.
    """
    young = _set("age_at_entry", [1], 18)
    cut = {MORT: _dropped(lambda t: (t["age"] > 50) | (t["age"] < 20))}
    model = _read_edited(tmp_path, young, edits=cut)
    try:
        _refused(_point(model, 1).result_cf,
                 "point_id 1: mort_table.csv has no rate at attained age 18")
        _refused(_point(model, 2).result_cf,
                 "point_id 2: mort_table.csv has no rate at attained age 51")
    finally:
        model.close()
    model = _read_edited(tmp_path / "select", lambda t: t)
    try:
        model.Projection.select_period = 7
        _refused(_point(model, 7).result_cf,
                 "point_id 7: select_factor_table.csv has no factor at duration 6")
        assert len(_point(model, 1).result_cf()) == 300
    finally:
        model.close()


def test_a_key_written_as_a_float_reads_as_term_uk_s_reads_it(sec_model, tmp_path):
    """A key written ``35.0`` is the key 35, in every table and in every extent.

    ``Term_UK_S``'s lookups match a float key to the int the projection asks, so a table
    written by a tool that writes every number with a decimal point reads the same.  Each
    assumption table's keys and the model point table's ``duration_mth`` are written as
    floats, and every committed point projects what the committed tables project, exactly.
    """
    def as_float(column):
        return lambda table: table.assign(**{column: table[column].astype(float)})

    edits = {MORT: as_float("age"), SELECT: as_float("duration"),
             LAPSE: as_float("policy_year")}
    model = _read_edited(tmp_path, as_float("duration_mth"), edits=edits)
    try:
        for point_id in _committed().index:
            for report in ("result_cf", "result_pols"):
                assert frame_mismatches(_point(sec_model, point_id).cells[report](),
                                        _point(model, point_id).cells[report](),
                                        rtol=0, atol=0) == [], (point_id, report)
    finally:
        model.close()


# ---------------------------------------------------------------------------
# T6 -- regeneration


def test_the_committed_sec_inputs_are_what_s_generates(s_model):
    """``model_point_table_sec.csv`` and ``wop_pipeline_sec.csv`` are what Term_UK_S and its
    table generate today.

    Every row and column, the text cells, the five opening-state columns and the
    pipeline's incidences included: an edit to an S row the table copies or derives from,
    or to an S formula a row's state is read from, fails here until ``python
    tools/gen_sec_points.py Term_UK_SEC`` regenerates them, in the same commit.  Text and
    integers compare exactly, and a float by its value, to 1e-12, because the text the
    writer picks for a computed float depends on the platform's parser (§5).
    """
    assert check_generated(SEC, s_model=s_model) == []


# ---------------------------------------------------------------------------
# The product's own facts


def test_the_two_clocks_on_the_shipped_points(sec_model):
    """``t`` counts from the valuation date; ``duration_mth(t)`` from issue (D3, D4).

    On a twin of S's new business the two coincide, and its policies enter as new business
    at ``t = 0``.  S's point 8, in force 60 months, is in policy year 6 at attained age 40
    at ``t = 0``, has 240 months of cover left, and is on the books from ``t = 0`` with no
    new business.  The indexed point valued on its fifth anniversary carries the factors of
    policy year 5, steps them at ``t = 0``, the anniversary's own month, and again at
    ``t = 12``.  The waiver point valued four months in has its first entrants at
    ``t = 3``, incidence from its first month.  The point issued 13 months on has nothing in
    force and nothing to do before ``t = 13``, and a frame of 253 months.  The point in its
    last covered month has a one-month frame, in which its survivors expire.  A timing the
    model does not know is refused rather than answered with another count.
    """
    twin = _row(sec_model, "twin", 1, 0)
    assert [twin.duration_mth(t) for t in (0, 1, 299)] == [0, 1, 299]
    assert (twin.t_entry(), twin.pols_if_init(), twin.pols_new_biz(0), twin.pols_if(0)) == (
        0, 0.0, 1.0, 1.0)
    assert (twin.term_mths(), twin.proj_len()) == (300, 300)
    old = _row(sec_model, "twin", 8, 60)
    assert (old.duration_mth(0), old.duration(0), old.policy_year(0), old.age(0, 1)) == (
        60, 5, 6, 40)
    assert (old.proj_len(), old.t_entry(), old.pols_new_biz(0)) == (240, 0, 0.0)
    assert old.is_active(239) and not old.is_active(240)
    assert old.pols_if(0) == old.pols_if_init() == old.policy_count() == 1.0
    idx = _row(sec_model, "derived", 5, 60)
    assert idx.idx_factor_init() == pytest.approx(1.03 ** 4, rel=1e-12)
    assert idx.idx_factor(0) == idx.idx_factor(11) == pytest.approx(1.03 ** 5, rel=1e-12)
    assert idx.idx_factor(12) == pytest.approx(idx.idx_factor_init() * 1.03 ** 2, rel=1e-12)
    wop = _row(sec_model, "derived", 7, 4)
    assert [wop.wop_waived_frac(t) for t in range(3)] == [0.0, 0.0, 0.0]
    assert wop.wop_waived_frac(3) > 0.0
    fut = _row(sec_model, "future", 7, -13)
    assert (fut.duration_mth(0), fut.t_entry(), fut.proj_len()) == (-13, 13, 253)
    assert not fut.is_active(12) and fut.is_active(13)
    assert (fut.pols_if_init(), fut.pols_new_biz(13), fut.pols_if(13)) == (0.0, 1.0, 1.0)
    last = _row(sec_model, "derived", 1, 299)
    assert (last.proj_len(), last.age(0, 1), last.policy_year(0)) == (1, 59, 25)
    assert last.pols_maturity(0) > 0.0 and last.pols_if_at(1, _code(last, "BEF_NB")) == 0.0
    _refused(lambda: old.pols_if_at(0, "BEF_NOTHING"), "invalid timing")


def test_the_committed_rows_continue_their_s_points(sec_model, s_model):
    """Each committed row in force, or issued later, is its S point from its month on.

    T6 compares a float to 1e-12, which pins a small count only to that much of itself, so
    each committed row is compared with its S point frame by frame and cell by cell, at the
    shipped assumptions (USLIB-SEC-PLAN.md §7.1, *Precised at M3*, item 11): S's in-force
    point 8 from its month 60, the five derived rows from theirs, and the row issued 13
    months on from S's issue month, all to 1e-9 relative with no absolute floor but on the
    residuals, every cell but those expense inflation moves (:func:`_continues_s`), which
    the inflation test holds.  The S point S opens in force, point 8, is exactly the row the
    plan's finding G2 found S to restart: its lapse ratio, ledger, waiver and factors start
    at the issue values where S's frame opens, and the twin carries what S assumes there.
    """
    table = sec_model.Data.model_point_table()
    found = []
    for point_id in table.index:
        kind, month = table.at[point_id, "row_kind"], int(table.at[point_id, "source_mth"])
        if kind == "twin" and month == 0:
            continue
        policy = table.at[point_id, "source_policy_id"]
        s_point = int(s_model.Data.model_point_table().index[
            s_model.Data.model_point_table()["policy_id"] == policy][0])
        found += [f"point {point_id}: {line}" for line in _continues_s(
            _point(s_model, s_point), _point(sec_model, point_id), month)]
    assert not found, found[:20]


def test_the_lapse_ratio_carries_on_from_the_issued_cohort(sec_model, s_model, tmp_path):
    """In force, the selective-lapse ratio goes on as a share of the cohort issued.

    ``Term_UK_S`` divides each month's lapses by the count its frame opened with, so a
    point it restates in force through ``duration_inforce`` restarts the ratio at 0 and
    takes the count in force for the cohort, and its deaths under the loading part from
    the projection from issue by 2.9 to 10% (UKLIB-SEC-PLAN.md G2).  Here the indexed point
    valued on its fifth anniversary opens with S's ratio there, 31%, past the reference,
    and the cohort it is a share of is rebuilt from it and the deaths since issue:
    ``cohort_frac(0)`` is S's count at month 60 per policy issued, to 1e-12.  With the
    loading on, at 0.25, the point restated by the generator from S run so is S's from
    month 60 in every cell, its mortality loaded from ``t = 0``.  Zeroed, as S restarts
    it, the ratio loads no mortality in the first month, and the deaths fall.
    """
    p, s = _row(sec_model, "derived", 5, 60), _point(s_model, 5)
    assert p.lapse_cum_init() == pytest.approx(s.lapse_cum(60), rel=1e-12)
    assert p.lapse_cum_init() > p.sel_lapse_ref
    assert p.cohort_frac(0) == pytest.approx(s.pols_if(60) / s.pols_if_init(), rel=1e-12)
    loaded = {"sel_lapse_lambda": 0.25, "inflation_rate": 0.0}
    s_on = mx.read_model(temp_inputs(tmp_path / "s", model_path(TWIN),
                                     model_points=_s_table().loc[[5]]), name=_name("s_on"))
    on = zeroed = None
    try:
        for ref, value in loaded.items():
            setattr(s_on.Projection, ref, value)
        rows, companions = build_sec_table(
            dataclasses.replace(SPEC, derived=((5, 60),), future=()), s_on)
        restart = rows.assign(lapse_cum_init=rows["lapse_cum_init"].where(
            rows["row_kind"] != "derived", 0.0))
        on = mx.read_model(_sec_inputs(tmp_path / "on", rows, companions[PIPELINE]),
                           name=_name("loaded"))
        zeroed = mx.read_model(_sec_inputs(tmp_path / "zero", restart,
                                           companions[PIPELINE]), name=_name("zeroed"))
        for model in (on, zeroed):
            for ref, value in loaded.items():
                setattr(model.Projection, ref, value)
        mine, theirs = _row(on, "derived", 5, 60), _point(s_on, 5)
        _sweep_s(theirs)
        assert _compare(theirs, mine, 60, SPLICE_EXEMPT) == []
        assert mine.sel_lapse_factor(0) > 1.0
        restarted = _row(zeroed, "derived", 5, 60)
        assert restarted.sel_lapse_factor(0) == 1.0
        assert restarted.pols_death(0) < mine.pols_death(0)
    finally:
        for model in (zeroed, on, s_on):
            if model is not None:
                model.close()


def test_the_indexation_history_is_read_from_the_model_point(sec_model, tmp_path):
    """The RPI increases already given are the point's, not recomputed (UKLIB-SEC-PLAN.md
    K14).

    ``Term_UK_S`` recomputes the factors from a flat ``rpi_rate``, so a model that dropped
    the two columns and did the same would pass the splice, since S and the splice
    recompute them alike.  So the indexed point on its fifth anniversary is projected with
    factors no flat rate gives: cover 1.25 and premium 1.40, the increases of the four
    years before it of an RPI other than the 3% assumed from the valuation date.  Its cover
    is the sum assured at issue times 1.25, and times 1.03 for each anniversary from the
    valuation date on, its fifth among them, at ``t = 0``; its premium the issue premium
    times 1.40, and times 1.045 for each; and the initial commission, a charge at issue,
    reads the issue premium, untouched.
    """
    row = _label(_committed(), "derived", 5, 60)
    model = _read_edited(tmp_path, _then(_set("idx_factor_init", [row], 1.25),
                                         _set("idx_prem_factor_init", [row], 1.40)))
    try:
        p = _point(model, row)
        for t, steps in ((0, 1), (11, 1), (12, 2), (30, 3), (239, 20)):
            assert p.benefit_pp(t) == pytest.approx(150000.0 * 1.25 * 1.03 ** steps,
                                                    rel=1e-12), t
            assert p.premium_pp(t) == pytest.approx(12.0 * 1.40 * 1.045 ** steps,
                                                    rel=1e-12), t
        assert p.comm_init_pp() == _point(sec_model, row).comm_init_pp() == 1.5 * 144.0
    finally:
        model.close()


# The RPI the K14 anniversary test sets at the valuation date, apart from the shipped 3%,
# and the increases it gives, recomputed by hand: the cover's min(max(5%, 0), 10%), and the
# premium's min(1.5 x 5%, 15%).
RPI_TODAY = 0.05
COVER_STEP, PREMIUM_STEP = 1.05, 1.075


def test_an_anniversary_at_the_valuation_date_is_made_at_today_s_rpi(s_model, tmp_path):
    """On a point valued on its anniversary, the factors carried in are those before it,
    and the anniversary's increase is the projection's, at today's RPI (K14; D6).

    The opening state is measured before any month-0 event, and an anniversary's RPI
    increase is one: an event that falls at the valuation date is the projection's first,
    made at the References of the valuation date, as on a point issued then
    (USLIB-SEC-PLAN.md D6, precised at its M7).  So with the RPI raised from the shipped 3%
    to 5% at the valuation date, the figures, recomputed here by hand:

    * The indexed point on its fifth anniversary carries the factors of policy year 5,
      ``1.03^4`` and ``1.045^4``, and takes its fifth step at ``t = 0`` at 5%, and each
      later one too: its cover at ``t = 0`` is ``150,000 x 1.03^4 x 1.05 = 177,267.637575``
      and its premium ``12 x 1.045^4 x 1.075 = 15.383489948``.  A column measured after
      month 0's event would carry ``1.03^5``, the step made at the history's 3%, and pay
      ``173,891.111145``.
    * Against S run under the history's 3%: the columns are S's factors in month 59, the
      month before the event, and not in month 60, where S has made the step at 3%.
    * The same point restated on its first anniversary, at month 12, by the generator from
      S at 3%, carries factors of 1, no increase having been given before it, and takes its
      first at 5% at ``t = 0``.  No state before month 12 reads the RPI, so S run at 5% is S
      under the history's References up to the event and today's from it: the row is S's
      at 5% from month 12 on, in every cell, as the twin issued at ``t = 0`` is S's from
      issue.
    """
    cover0, prem0 = 1.03 ** 4, 1.045 ** 4
    s = _point(s_model, 5)
    assert s.rpi_rate == 0.03
    row = _label(_committed(), "derived", 5, 60)
    model = mx.read_model(model_path(SEC), name=_name("rpi_today"))
    try:
        model.Projection.rpi_rate = RPI_TODAY
        p = _point(model, row)
        assert p.idx_factor_init() == pytest.approx(cover0, rel=1e-15)
        assert p.idx_prem_factor_init() == pytest.approx(prem0, rel=1e-15)
        assert (p.idx_factor_init(), p.idx_prem_factor_init()) == (
            s.idx_factor(59), s.idx_prem_factor(59))
        assert s.idx_factor(60) == pytest.approx(1.03 ** 5, rel=1e-15)
        assert s.idx_prem_factor(60) == pytest.approx(1.045 ** 5, rel=1e-15)
        for t, steps in ((0, 1), (11, 1), (12, 2), (239, 20)):
            assert p.idx_factor(t) == pytest.approx(cover0 * COVER_STEP ** steps,
                                                    rel=1e-12), t
            assert p.idx_prem_factor(t) == pytest.approx(prem0 * PREMIUM_STEP ** steps,
                                                         rel=1e-12), t
            assert p.benefit_pp(t) == pytest.approx(
                150000.0 * cover0 * COVER_STEP ** steps, rel=1e-12), t
            assert p.premium_pp(t) == pytest.approx(
                12.0 * prem0 * PREMIUM_STEP ** steps, rel=1e-12), t
        assert p.benefit_pp(0) == pytest.approx(177267.637575, rel=1e-12)
        assert p.premium_pp(0) == pytest.approx(15.383489948062500, rel=1e-12)
        assert p.benefit_pp(0) != pytest.approx(150000.0 * s.idx_factor(60), rel=1e-6)
        assert 150000.0 * s.idx_factor(60) == pytest.approx(173891.111145, rel=1e-12)
    finally:
        model.close()
    rows, companions = build_sec_table(
        dataclasses.replace(SPEC, derived=((5, 12),), future=()), s_model)
    assert s_model.Projection.rpi_rate == 0.03
    today = {"rpi_rate": RPI_TODAY, "inflation_rate": 0.0}
    sec = mx.read_model(_sec_inputs(tmp_path, rows, companions[PIPELINE]),
                        name=_name("first_anniversary"))
    s_today = mx.read_model(model_path(TWIN), name=_name("rpi_today_s"))
    try:
        for m in (sec, s_today):
            for ref, value in today.items():
                setattr(m.Projection, ref, value)
        first, theirs = _row(sec, "derived", 5, 12), _point(s_today, 5)
        assert (first.idx_factor_init(), first.idx_prem_factor_init()) == (1.0, 1.0)
        assert (first.idx_factor(0), first.idx_prem_factor(0)) == (COVER_STEP, PREMIUM_STEP)
        assert first.policy_count() == s.pols_if(12) == theirs.pols_if(12)
        _sweep_s(theirs)
        assert _compare(theirs, first, 12, SPLICE_EXEMPT) == []
        assert _row(sec, "twin", 5, 0).idx_factor(12) == COVER_STEP
    finally:
        s_today.close()
        sec.close()


def test_no_twin_is_written_of_an_indexed_point_s_opens_in_force(tmp_path):
    """The generator refuses the twin of an indexed point ``Term_UK_S`` opens in force.

    S opens an in-force frame on an anniversary only, at index factors of 1, and takes its
    first step at the next anniversary.  This model takes an anniversary at the valuation
    date as month 0's own step (USLIB-SEC-PLAN.md D6, precised at its M7), from factors
    ``Data`` holds to 1 or more, so no twin of such a point is S's: S's point 8, in force at
    60, made indexed in a copy of S's table, would have a twin paying 154,500 at ``t = 0``,
    one step above S's 150,000 in every month of its frame.  The generator refuses to write
    it, naming the point and why; S itself takes no step at month 60 and its first at 72.
    """
    indexed = _s_table().assign(indexation=lambda t: t["indexation"] | (t.index == 8))
    s = mx.read_model(temp_inputs(tmp_path, model_path(TWIN), model_points=indexed),
                      name=_name("indexed_in_force"))
    try:
        p = _point(s, 8)
        assert (p.idx_factor(60), p.idx_factor(71), p.idx_factor(72)) == (1.0, 1.0, 1.03)
        assert p.benefit_pp(60) == 150000.0
        with pytest.raises(ValueError) as err:
            build_sec_table(SPEC, s)
        assert str(err.value) == (
            "Term_UK_S point 8: S opens it in force at month 60, an anniversary, indexed, "
            "at factors of 1 and with no step there, where Term_UK_SEC makes an "
            "anniversary at the valuation date month 0's own step (D6): no opening factor "
            "of 1 or more gives S's numbers, so no twin is written")
    finally:
        s.close()


def test_the_streams_in_payment_are_read_from_the_model_point(sec_model, s_model,
                                                               tmp_path):
    """The family income benefit valued mid-year pays the streams already in payment
    (UKLIB-SEC-PLAN.md K14, §9 item 5).

    ``Term_UK_S`` restarts its ledger at 0 where its frame opens, and so pays the
    uncommuted benefit 92 to 99% low on a point it restates in force (G2).  Here the point
    valued at 66 opens with S's streams in payment, per policy in force, and its first
    instalments are one for each stream and for the month's deaths, S's at month 66; its
    ledger check rebuilds from the opening streams and closes.  The streams are history,
    not ``(1 - c)`` of the deaths since issue at today's take-up ``c``, which
    ``Term_UK_S`` pays: written as a third of the deaths, as though two in three past
    claims had been commuted, they are what is paid at ``t = 0``, the deaths since issue
    unmoved; and a take-up of 0.5 set from the valuation date leaves every stream already
    in payment in payment and commutes half of each later claim, month by month, where
    S's form would pay 49.6% low at ``t = 0``.
    """
    p, s = _row(sec_model, "derived", 3, 66), _point(s_model, 3)
    fib = _code(p, "FIB")
    assert p.fib_streams(0) == pytest.approx(s.fib_cum(66), rel=1e-12)
    assert p.claims(0, fib) == pytest.approx(s.claims(66, "FIB"), rel=1e-12)
    assert p.check_fib_ledger()
    row = _label(_committed(), "derived", 3, 66)
    third = _set("fib_streams_init", [row], _committed().at[row, "fib_cum_init"] / 3)
    model = _read_edited(tmp_path / "third", third)
    try:
        q = _point(model, row)
        assert q.fib_cum(0) == p.fib_cum(0)
        assert q.claims(0, fib) == pytest.approx(
            q.fib_income() * (q.pols_death(0) + q.pols_if_init() * q.fib_cum_init() / 3),
            rel=1e-12)
        assert q.check_fib_ledger()
    finally:
        model.close()
    model = _read_edited(tmp_path / "half", _set("fib_commute_rate", [row], 0.5))
    try:
        q = _point(model, row)
        paid, later = s.fib_cum(66), 0.0
        for t in range(q.proj_len()):
            want = s.fib_income() * (paid + 0.5 * (later + s.pols_death(66 + t)))
            assert q.claims(t, fib) == pytest.approx(want, rel=1e-9), t
            later += s.pols_death(66 + t)
        assert q.claims(0, fib) / (0.5 * s.claims(66, "FIB")) - 1.0 > 0.9
        assert q.check_fib_ledger()
    finally:
        model.close()


def test_the_waiver_pipeline_brings_its_deferred_lives_in_after_the_deferred_period(
        sec_model, s_model, tmp_path):
    """Each cohort in the pipeline enters waiver at its own month (UKLIB-SEC-PLAN.md K14).

    ``Term_UK_S`` restarts its waiver at its frame's start, with no one waived and no one in
    the deferred period, so its waiver point's premiums part from the projection from issue
    (G2).  Here the waiver point valued at 66 opens with S's waived share and the pipeline
    of the six months before the valuation date, each lag the share still in its deferred
    period at the valuation instant: in the frame's first six months, the entrants of ``t``
    are lag ``7 - t``'s share, carried through the ``t`` months of recovery still to run,
    and its waived share is S's at month ``66 + t``.  The pipeline is read, not recomputed
    from ``wop_inc_rate``: a share of 0.01 written at lag 3, history no incidence rate
    gives, adds 0.01 of the policies, less four months' recoveries, to the waived share at
    ``t = 4`` and to none before, and the recovery rate alone carries it on.  And the
    waived share is read too: written 0.1, which no incidence rate gives in six years, it
    is the share at ``t = 0``, the premium is collected from the other 90%, and it recovers
    at the recovery rate.  Either written share leaves that much fewer lives active at
    ``t = 0``: the active share opens at what the waived share and the pipeline leave, and
    the incidence of the frame's months falls on it.
    """
    p, s = _row(sec_model, "derived", 7, 66), _point(s_model, 7)
    rec = 1.0 - p.wop_rec_rate_mth()
    for t in range(1, 7):
        entrants = p.wop_waived_frac(t) - p.wop_waived_frac(t - 1) * rec
        assert entrants == pytest.approx(p.wop_deferred_init(7 - t) * rec ** t,
                                         rel=1e-9), t
        assert p.wop_waived_frac(t) == pytest.approx(s.wop_waived_frac(66 + t), rel=1e-12), t
    row = _label(_committed(), "derived", 7, 66)
    pipeline = _committed_pipeline()
    at = (pipeline["point_id"] == row) & (pipeline["lag"] == 3)
    pipeline.loc[at, "wop_deferred_init"] = 0.01
    model = mx.read_model(_sec_inputs(tmp_path, _committed(), pipeline), name=_name("pipe"))
    try:
        q = _point(model, row)
        jump = (0.01 - p.wop_deferred_init(3)) * rec ** 4
        for t in range(4):
            assert q.wop_waived_frac(t) == p.wop_waived_frac(t), t
        assert q.wop_waived_frac(4) - p.wop_waived_frac(4) == pytest.approx(jump, rel=1e-9)
        assert q.wop_waived_frac(5) - p.wop_waived_frac(5) == pytest.approx(jump * rec,
                                                                            rel=1e-9)
        assert p.wop_active_frac(0) - q.wop_active_frac(0) == pytest.approx(
            0.01 - p.wop_deferred_init(3), rel=1e-9)
    finally:
        model.close()
    model = _read_edited(tmp_path / "share", _set("wop_waived_frac_init", [row], 0.1))
    try:
        q = _point(model, row)
        assert q.wop_waived_frac(0) == 0.1
        assert q.premiums(0) == pytest.approx(q.premium_pp(0) * q.pols_if(0) * 0.9,
                                              rel=1e-12)
        rec = 1.0 - q.wop_rec_rate_mth()
        assert q.wop_waived_frac(1) - p.wop_waived_frac(1) == pytest.approx(
            (0.1 - p.wop_waived_frac_init()) * rec, rel=1e-9)
        assert p.wop_active_frac(0) - q.wop_active_frac(0) == pytest.approx(
            0.1 - p.wop_waived_frac_init(), rel=1e-9)
    finally:
        model.close()


def _waiver_ladder(inc, rec, defer, months):
    """The waiver's three states at the start of each month from issue, rebuilt from the
    annual rates alone: a list of ``(active, deferred, waived)``, ``deferred`` the list of
    the deferred lives by lag, ``deferred[k - 1]`` those incapacitated ``k`` months before.

    An explicit ladder, with none of either model's cells: every life is active at issue,
    and in each month an active life becomes incapacitated at ``inc_m``, onto lag 1; every
    incapacitated life, deferred or waived, recovers to active at ``rec_m``; and every
    other deferred life climbs a lag, from the last into waiver.
    """
    inc_m = 1.0 - (1.0 - inc) ** (1.0 / 12.0)
    rec_m = 1.0 - (1.0 - rec) ** (1.0 / 12.0)
    active, deferred, waived = 1.0, [0.0] * defer, 0.0
    states = []
    for _ in range(months):
        states.append((active, deferred, waived))
        falling, ill = active * inc_m, sum(deferred) + waived
        waived = (waived + deferred[-1]) * (1.0 - rec_m)
        deferred = [falling] + [d * (1.0 - rec_m) for d in deferred[:-1]]
        active = active * (1.0 - inc_m) + ill * rec_m
    return states


def test_the_committed_waiver_state_is_the_ladder_s(sec_model):
    """The committed opening state of each waiver point in force is the three-state
    ladder's at its month, rebuilt in the test from the rates alone (§6.1, K14).

    The waiver point restated at 66 and at 4 (:func:`_waiver_ladder`, S point 7 at the
    shipped rates): its waived share, ``wop_waived_frac_init``, is the ladder's waived
    lives; its pipeline, each lag the ladder's lives deferred that many months, the
    incidence on the lives active then after the recoveries since; and its active share at
    ``t = 0``, what the two leave, the ladder's active lives.  An incidence taken from
    ``1 - u``, which counts the deferred lives among those who can fall ill, writes each
    lag up to 0.2% high.
    """
    table = _committed()
    ladder = _waiver_ladder(0.004, 0.35, 6, 67)
    for d in (66, 4):
        label = _label(table, "derived", 7, d)
        p = _point(sec_model, label)
        active, deferred, waived = ladder[d]
        assert p.wop_waived_frac_init() == pytest.approx(waived, rel=1e-12, abs=0.0), d
        lags = min(6, d)
        assert [p.wop_deferred_init(k) for k in range(1, lags + 1)] == pytest.approx(
            deferred[:lags], rel=1e-12, abs=0.0), d
        assert p.wop_active_frac(0) == pytest.approx(active, rel=1e-14, abs=0.0), d
        assert sum(deferred) + waived + active == pytest.approx(1.0, rel=1e-14, abs=0.0), d


def test_a_recovery_rate_changed_at_the_valuation_date_reaches_back_over_no_month(s_model):
    """The months of a deferred period already run keep their recoveries (K14; D6).

    The pipeline holds the lives still in their deferred period at the valuation instant,
    after the recoveries of the months already run, not the incidence they began with.  So
    a recovery rate changed at the valuation date, from 0.35 to 0.5 a year, applies to the
    months from it on alone: on the waiver point valued at 66, each cohort's survival
    through its deferred period is the shipped rate's in the months before 66 and the new
    one's from 66, as a rebuild of S's recursions month by month says, at every month of
    the pipeline's reach and past it.  The rebuild carries the active share too, on which
    each month's incidence falls: S's to month 66, and from it on the recoveries back to it
    at 0.5.  Held as the incidence, the months already run would be run again at 0.5 (the
    review's ``wop_recovery_change.py``).
    """
    sec = mx.read_model(model_path(SEC), name=_name("recovery"))
    try:
        sec.Projection.wop_rec_rate = 0.5
        q, p = _row(sec, "derived", 7, 66), _point(s_model, 7)
        d, defer, inc = 66, p.wop_defer_mths, p.wop_inc_rate_mth()
        new = 1.0 - (1.0 - 0.5) ** (1.0 / 12.0)
        rate = {m: p.wop_rec_rate_mth() if m < d else new for m in range(d + 13)}
        u = {m: p.wop_waived_frac(m) for m in range(d + 1)}
        act = {m: p.wop_active_frac(m) for m in range(d + 1)}
        for m in range(d + 1, d + 13):
            act[m] = act[m - 1] * (1.0 - inc) + (1.0 - act[m - 1]) * new
            src = m - 1 - defer
            survive = 1.0
            for month in range(src + 1, src + defer + 1):
                survive *= 1.0 - rate[month]
            u[m] = u[m - 1] * (1.0 - new) + inc * act[src] * survive
        for t in range(13):
            assert q.wop_active_frac(t) == pytest.approx(act[d + t], rel=1e-12), t
            assert q.wop_waived_frac(t) == pytest.approx(u[d + t], rel=1e-12), t
    finally:
        sec.close()


def test_the_commission_paid_at_issue_is_read_from_the_model_point(tmp_path):
    """The initial commission a policy in force paid at issue is history (K14; D6).

    Under the four-year clawback, the waiver point four months in recovers, on each lapse,
    the commission it paid, ``c0 (48 - m)/48``.  ``Term_UK_S`` re-derives that commission
    from ``comm_init_rate``, so a rate changed at the valuation date would change what was
    paid at issue.  Here, with the rate raised from 150% to 250% of the annual premium,
    the point's clawback moves not at all, while the same point issued at the valuation
    date pays and recovers the new rate; and a column written off the rate's path is what
    is recovered.  Every Reference is set on a model just read (K7).
    """
    models = {}
    try:
        for tag, refs in (("shipped", {"clawback_mths": 48}),
                          ("raised", {"clawback_mths": 48, "comm_init_rate": 2.5})):
            models[tag] = mx.read_model(model_path(SEC), name=_name(f"comm_{tag}"))
            for ref, value in refs.items():
                setattr(models[tag].Projection, ref, value)
        old, new = (_row(models[tag], "derived", 7, 4) for tag in ("shipped", "raised"))
        assert old.comm_init_pp() == new.comm_init_pp() == old.comm_init_pp_init() > 0.0
        window = range(48 - 5)
        assert all(new.comm_clawback(t) == old.comm_clawback(t) for t in window)
        assert all(old.comm_clawback(t) > 0.0 for t in window)
        issued = [_row(models[tag], "twin", 7, 0) for tag in ("shipped", "raised")]
        assert issued[1].comm_init_pp() == pytest.approx(
            issued[0].comm_init_pp() * 2.5 / 1.5, rel=1e-12)
        assert issued[1].comm_clawback(0) == pytest.approx(
            issued[0].comm_clawback(0) * 2.5 / 1.5, rel=1e-12)
    finally:
        for model in models.values():
            model.close()
    row = _label(_committed(), "derived", 7, 4)
    model = _read_edited(tmp_path, _set("comm_init_pp_init", [row], 400.0),
                         edits=None)
    try:
        model.Projection.clawback_mths = 48
        q = _point(model, row)
        for t in (0, 20, 42):
            assert q.comm_clawback(t) == pytest.approx(
                400.0 * (48 - (q.duration_mth(t) + 1)) / 48 * q.pols_lapse(t), rel=1e-12)
    finally:
        model.close()


def test_expense_inflation_runs_on_the_valuation_clock(sec_model, s_model):
    """Maintenance is in valuation-date pounds, for every point alike (D7).

    At the shipped 3%, the factor at ``t`` is ``1.03^(t // 12)`` on every point, whatever
    its duration, stepping on the valuation date's anniversaries.  So S's point 8, in force
    60 months, pays S's month-``60 + t`` expenses deflated by ``1.03^5``, the inflation S
    had already applied since issue, and the point issued 13 months on pays S's maintenance
    a year of inflation earlier than S's issue month would: its factor at ``t`` is
    ``1.03^(t // 12)``, where S's at ``t - 13`` is ``1.03^((t - 13) // 12)``.  Acquisition is
    not inflated on either.  This is the only test that sees inflation run on the policy
    clock: the splice sets the rate to 0, and on a point issued at ``t = 0`` the clocks
    agree.
    """
    assert sec_model.Projection.inflation_rate == INFLATION
    p, s = _row(sec_model, "twin", 8, 60), _point(s_model, 8)
    fut = _row(sec_model, "future", 7, -13)
    for t in (0, 11, 12, 30):
        assert p.inflation_factor(t) == fut.inflation_factor(t) == (1 + INFLATION) ** (t // 12)
    for t in range(p.proj_len()):
        assert p.expenses(t) == pytest.approx(
            s.expenses(60 + t) / (1 + INFLATION) ** 5, rel=1e-12), t
    s7 = _point(s_model, 7)
    acq = s7.expense_acq
    for t in range(13, fut.proj_len()):
        issued = acq if t == 13 else 0.0
        maint = (fut.expenses(t) - issued) / fut.pols_if(t)
        want = (s7.expenses(t - 13) - issued) / s7.pols_if(t - 13)
        assert maint == pytest.approx(
            want * (1 + INFLATION) ** (t // 12 - (t - 13) // 12), rel=1e-12), t


def test_acquisition_and_initial_commission_are_charged_on_new_business_only(sec_model):
    """£150 and 150% of the issue premium per policy issued, in the issue month alone.

    On every committed point, what ``expenses(t)`` holds beyond its maintenance part is
    ``150 * policy_count()`` in the issue month, ``t = -duration_mth``, and 0 in every other
    month, to 1e-9, and the commission beyond its renewal part and the clawback is
    ``comm_init_pp() * policy_count()`` there and 0 elsewhere: the twins of S's new business
    bear both at ``t = 0``, the point issued 13 months on at ``t = 13``, and the points
    already in force never, though on the valuation clock their row 0 is ``t = 0``, as S's
    restated rows did not.  ``Term_UK_S`` charges both at ``t = 0`` on the count in force
    there, which on a point issued at the valuation date is the issued count, so the twins
    agree with S at any count.
    """
    table = sec_model.Data.model_point_table()
    for key, point_id in zip(point_keys(sec_model), table.index):
        p = projection(sec_model, key)
        ts = range(p.proj_len())
        issue = -table.at[point_id, "duration_mth"]
        acq = [p.expenses(t) - p.expense_maint / 12 * p.inflation_factor(t) * p.pols_if(t)
               for t in ts]
        assert acq == pytest.approx([p.expense_acq * p.policy_count() if t == issue
                                     else 0.0 for t in ts], abs=1e-9), point_id
        renew = [p.comm_renewal_rate * p.premiums(t) if p.duration_mth(t) >= 12 else 0.0
                 for t in ts]
        init = [p.commissions(t) - renew[t] + p.comm_clawback(t) for t in ts]
        assert init == pytest.approx([p.comm_init_pp() * p.policy_count() if t == issue
                                      else 0.0 for t in ts], abs=1e-9), point_id
        assert (issue in ts) == (sum(acq) > 0.0), point_id


def test_renewal_commission_and_the_clawback_run_on_the_policy_clock(sec_model, tmp_path):
    """Renewal commission starts at policy month 12, and the clawback stops at 48.

    ``Term_UK_S`` tests ``t >= 12`` and counts ``t + 1`` months in force, which are the
    policy's months only on a point issued at ``t = 0``.  On S's point 8, in force 60
    months, renewal commission is paid from ``t = 0``; on the waiver point valued four
    months in, from ``t = 8``, its first anniversary.  With the notes' four-year clawback
    switched on, a lapse of the point valued four months in recovers ``(48 - (4 + t + 1))
    / 48`` of its initial commission at ``t``, to ``t = 42``, policy month 46, and nothing
    from ``t = 43``, policy month 47, whose lapses have 48 months in force; S's point 8,
    past the window at the valuation date, recovers none.
    """
    old, young = _row(sec_model, "twin", 8, 60), _row(sec_model, "derived", 7, 4)
    assert old.commissions(0) == pytest.approx(0.025 * old.premiums(0), rel=1e-12)
    assert [young.commissions(t) for t in range(8)] == [0.0] * 8
    assert young.commissions(8) == pytest.approx(0.025 * young.premiums(8), rel=1e-12)
    model = mx.read_model(_sec_inputs(tmp_path, _committed()), name=_name("claw"))
    try:
        model.Projection.clawback_mths = 48
        y, o = _row(model, "derived", 7, 4), _row(model, "twin", 8, 60)
        for t in (0, 20, 42):
            assert y.comm_clawback(t) == pytest.approx(
                y.comm_init_pp() * (48 - (4 + t + 1)) / 48 * y.pols_lapse(t), rel=1e-12), t
        assert y.comm_clawback(43) == 0.0 and y.pols_lapse(43) > 0.0
        assert all(o.comm_clawback(t) == 0.0 for t in range(o.proj_len()))
    finally:
        model.close()


def test_an_annual_payer_valued_mid_year_pays_on_its_anniversary(sec_model, tmp_path):
    """An annual premium falls due on the policy's anniversary, on the policy clock.

    ``Term_UK_S`` charges an annual payer ``12 P_m`` where ``t % 12 == 0``, its own policy
    months.  The family income benefit point valued at 66, made an annual payer, pays
    nothing until its anniversary at ``t = 6``, policy month 72, then twelve months'
    premium, then nothing for eleven months.  The amounts are the issue premium times
    twelve: the point is not indexed.  The indexed point valued on its fifth anniversary,
    made an annual payer, pays at ``t = 0``, its premium raised by the anniversary's step,
    month 0's own, on the factor of policy year 5 it carries in.
    """
    mid = _label(_committed(), "derived", 3, 66)
    on = _label(_committed(), "derived", 5, 60)
    model = _read_edited(tmp_path, _set("premium_mode", [mid, on], "annual"))
    try:
        p = _point(model, mid)
        assert [p.premium_pp(t) for t in range(19)] == (
            [0.0] * 6 + [144.0] + [0.0] * 11 + [144.0])
        q = _point(model, on)
        assert q.premium_pp(0) == pytest.approx(144.0 * q.idx_prem_factor_init() * 1.045,
                                                rel=1e-12)
        assert q.premium_pp(1) == 0.0
    finally:
        model.close()


# ---------------------------------------------------------------------------
# The cap on mortality
#
# mort_rate_life caps each life's annual rate at 1, the bound second, as Term_UK_S's does
# since M0.  At the shipped tables the rate stays below 0.008 to the end of every frame, so
# neither the committed points nor the splice grid come near the cap, and Data refuses a
# table rate past 1.  So the cap binds through the product: CAPPED's table writes the anchor
# cell's male non-smoker rates from age 50 at 0.96, a probability Data accepts, and the
# splice's selective-lapse loading, past its reference by then, takes the product past 1 at
# attained age 50, policy month 180, where it stays.  S point 1 alone, in a copy of S's
# table, under SPLICED_REFS.
CAPPED = {MORT: _written("mort_rate", 0.96,
                         lambda t: (t["sex"] == "M") & (t["smoker"] == "N") & (t["age"] >= 50))}
CAPPED_POINT = 1
CAPPED_MTH = 12 * (50 - 35)     # the first month at attained age 50, where it passes 1


def _capped_s(tmp_path):
    """Term_UK_S on :data:`CAPPED_POINT` alone, on :data:`CAPPED`'s table, under
    :data:`SPLICED_REFS`, read from a copy of S's inputs; the caller closes it."""
    s = mx.read_model(temp_inputs(tmp_path, model_path(TWIN),
                                  model_points=_s_table().loc[[CAPPED_POINT]],
                                  edits=CAPPED), name=_name("capped_s"))
    for ref, value in SPLICED_REFS.items():
        setattr(s.Projection, ref, value)
    return s


def test_an_annual_mortality_past_1_is_capped_in_both_models(tmp_path):
    """Where the annual mortality product passes 1, both models' rate is 1.

    On :data:`CAPPED_POINT`, on :data:`CAPPED`'s table under :data:`SPLICED_REFS`,
    ``Term_UK_S``'s product of the table rate and the selective-lapse loading passes 1 in
    month :data:`CAPPED_MTH` and stays past it to the end of the frame.  Both models cap
    it: ``mort_rate_life``, ``mort_rate`` and the monthly rate, ``1 - (1 - q)^(1/12)``, are
    1.0 in every one of those months, the float, not the int 1, which compares equal to it,
    and S's are floats below 1 in every month before.  So every policy in force at the
    start of the first capped month dies in it, none is in force after it, and every
    report holds finite floats alone.

    Four rows of the point, built from S by the generator: issued at the valuation date
    and 12 months after it, and restated in force in the month before the cap, opened with
    S's count and state there, each compared with S in every cell, the capped months
    included, as T1, T3 and the splice compare them, to 1e-9 relative with no absolute
    floor, but for the residuals, rounding around 0, which keep the floor of 1e-9
    (USLIB-SEC-PLAN.md §5.1, step 6); and restated five months into the capped year,
    opened with S's state there and one policy, since S's count there is 0.  On each, the
    rate is 1.0 from its first capped month, every policy in force there dies in it, and
    the count is 0.0 after it.
    """
    s = _capped_s(tmp_path / "s")
    sec = None
    try:
        sp = _point(s, CAPPED_POINT)
        end = sp.proj_len()
        product = [sp.mort_rate_base(t, 1) * sp.sel_lapse_factor(t) for t in range(end)]
        cap = next(t for t in range(end) if product[t] > 1)
        assert (cap, sp.age(cap, 1)) == (CAPPED_MTH, 50)
        after = range(cap, end)
        assert all(product[t] > 1 for t in after)
        for rate in (sp.mort_rate, sp.mort_rate_mth):
            assert all(type(rate(t)) is float and rate(t) < 1.0 for t in range(cap))
            assert [(type(rate(t)), rate(t)) for t in after] == [(float, 1.0)] * len(after)
        _sweep_s(sp)
        assert sp.pols_if(cap) > 0.0 and sp.pols_death(cap) == sp.pols_if(cap)
        assert [sp.pols_if(t) for t in range(cap + 1, end)] == [0.0] * (len(after) - 1)
        spec = dataclasses.replace(
            SPEC, derived=((CAPPED_POINT, cap - 1), (CAPPED_POINT, cap + 5)),
            future=((CAPPED_POINT, 12),))
        rows, companions = build_sec_table(spec, s)
        rows.loc[rows["source_mth"] == cap + 5, "policy_count"] = 1.0
        sec = mx.read_model(_sec_inputs(tmp_path / "sec", rows, companions[PIPELINE],
                                        edits=CAPPED), name=_name("capped"))
        for ref, value in SPLICED_REFS.items():
            setattr(sec.Projection, ref, value)
        # Each row with the month its rate is first capped, on its own clock, and the
        # exemptions of its comparison with S: none for the row S's count does not open.
        cases = ((("twin", CAPPED_POINT, 0), cap, TWIN_EXEMPT_DEFAULT | SPEC.exempt),
                 (("future", CAPPED_POINT, -12), cap + 12, FUTURE_EXEMPT),
                 (("derived", CAPPED_POINT, cap - 1), 1, SPLICE_EXEMPT),
                 (("derived", CAPPED_POINT, cap + 5), 0, None))
        for case, first, exempt in cases:
            p = _row(sec, *case)
            if exempt is not None:
                assert _mismatches(sp, p, t_offset=case[2], exempt=exempt | RESIDUALS,
                                   atol=0.0) == [], case
                others = exempt | (set(sp.cells) - RESIDUALS)
                assert _mismatches(sp, p, t_offset=case[2], exempt=others) == [], case
            capped, later = range(first, p.proj_len()), range(first + 1, p.proj_len())
            for rate in (p.mort_rate, p.mort_rate_mth, lambda t: p.mort_rate_life(t, 1)):
                assert [(type(rate(t)), rate(t)) for t in capped] == (
                    [(float, 1.0)] * len(capped)), case
            assert p.pols_if(first) > 0.0 and p.pols_death(first) == p.pols_if(first), case
            assert [p.pols_if(t) for t in later] == [0.0] * len(later), case
            for report in ("result_cf", "result_pols"):
                frame = p.cells[report]()
                assert (frame.dtypes == "float64").all(), (case, report)
                assert np.isfinite(frame.to_numpy()).all(), (case, report)
    finally:
        if sec is not None:
            sec.close()
        s.close()


# A NaN sent to each bound written with its bound second, as (the bound, the Reference that
# feeds it, set to NaN on a model read for the test before it computes anything, the S
# point whose twin reads it, and the calls that must give the float NaN).  The cap reads
# mort_scale on the select basis; the RPI's floor and cover cap, max(rpi, 0.0) and
# min(..., 0.1), read rpi_rate, and the premium increase's cap, min(1.5 x increase, 0.15),
# reads idx_prem_mult, on the indexed point after its first anniversary.  A bound written
# first would turn each NaN into the bound: a blank input read as certain death, or as a
# cover increase of 10%.  This form runs compiled unchanged, since a compiled ItemSpace
# takes the References when it is made (USLIB-SEC-PLAN.md §5.1, step 6, precised at M12).
NAN_BOUNDS = [
    ("the mortality cap, min(q, 1.0)", "mort_scale", 7,
     [("mort_rate_life", (0, 1)), ("mort_rate", (0,)), ("mort_rate_mth", (239,)),
      ("pols_if", (1,))]),
    ("the sel_lapse loading's multiple, through the cap", "sel_lapse_lambda", 1,
     [("mort_rate_life", (0, 1)), ("mort_rate", (299,)), ("pols_if", (1,))]),
    ("the RPI's floor and cover cap", "rpi_rate", 5,
     [("idx_increase", ()), ("idx_factor", (12,)), ("idx_prem_factor", (12,))]),
    ("the premium increase's cap", "idx_prem_mult", 5, [("idx_prem_factor", (12,))]),
]


@pytest.mark.parametrize("bound, ref, s_point, calls", NAN_BOUNDS,
                         ids=[c[0] for c in NAN_BOUNDS])
def test_a_nan_that_reaches_a_bound_stays_nan(bound, ref, s_point, calls):
    """A NaN that reaches a bound written second stays NaN, and is not read as the bound.

    ``min`` keeps its first argument unless a later one compares smaller, and ``max`` unless
    a later one compares larger, in modelx and compiled alike, and no comparison with NaN
    holds, so with its bound first each would turn a NaN into the bound.  Each is written
    with its bound second, as ``Term_UK_S`` writes it (:data:`NAN_BOUNDS`): the Reference
    that feeds it is set to NaN on a model read for the test, and every call must give the
    float NaN.
    """
    model = mx.read_model(model_path(SEC), name=_name("nan"))
    try:
        setattr(model.Projection, ref, float("nan"))
        p = _row(model, "twin", s_point, 0)
        lost = [f"{name}{args} = {value!r}" for name, args in calls
                for value in [p.cells[name](*args)]
                if not (type(value) is float and math.isnan(value))]
        assert not lost, f"{bound} loses a NaN {ref}: {lost}"
    finally:
        model.close()


def _outside_cover_faults(p, where):
    """Where ``p``, an ItemSpace that has evaluated nothing, departs from OUTSIDE_COVER.

    Every cell of :data:`OUTSIDE_COVER`, ``pols_if_at`` at each timing, ``claims`` at each
    kind and ``mort_rate_base`` at each life the point has, in every month before issue
    and at ``t = proj_len()``, the first month after cover, which the count's look-ahead
    reads, against :data:`OUTSIDE_COVER`; then whether any of :data:`IN_COVER_ONLY` was
    evaluated on the way, which only a fresh ItemSpace can say.  A cell that raises is
    reported as a fault too, so the scan goes on.
    """
    faults = []
    lives = (1, 2) if p.is_joint() else (1,)
    for t in [*range(p.t_entry()), p.proj_len()]:
        calls = [(name, (t,), want) for name, want in OUTSIDE_COVER.items()]
        calls += [("pols_if_at", (t, _code(p, timing)), 0.0) for timing in TIMINGS]
        calls += [("claims", (t, _code(p, kind)), 0.0) for kind in KINDS]
        calls += [("mort_rate_base", (t, life), 0.0) for life in lives]
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


def test_every_guarded_cell_holds_its_outside_cover_value(spliced):
    """Outside cover each cell holds :data:`OUTSIDE_COVER`'s value, and reads no rate.

    On every committed point, in every month before issue and in the first month after
    cover, ``t = proj_len()``, which the count's look-ahead reads, on a model that evaluates
    nothing else.  So afterwards none of :data:`IN_COVER_ONLY` may hold a value at all:
    ``is_active``'s docstring promises that outside cover no count evaluates a rate, and no
    table is read at a policy year, a select duration or an attained age the policy does
    not have.

    The committed table's one point issued after the valuation date is the waiver point,
    which is not indexed, and has no ledger to pay, so on it a cell tied to one of those
    would hold zero before issue, guarded or not.  So the same scan runs on the splice's
    future rows, the core's or, with ``UKLIB_SEC_FULL=1``, all of them: the indexed point,
    the family income benefit, the joint point, the annual payer and the indexed waiver
    point among them.  Each row is made afresh first and released after.

    Several of these guards change no number the frame shows: once the counts are zero
    outside cover, every cash flow is too, and an unguarded value multiplies a zero count.
    They are held here because they are what the docstrings promise a caller, and because
    the C step needs them: a table read at a policy year or an age the policy does not have
    would wrap round in a compiled model rather than fail (USLIB-SEC-PLAN.md F4, R1).
    """
    faults = []
    model = mx.read_model(model_path(SEC), name=_name("cover"))
    try:
        table = model.Data.model_point_table()
        for key, point_id in zip(point_keys(model), table.index):
            faults += _outside_cover_faults(projection(model, key), f"point {point_id}")
    finally:
        model.close()
    sec = spliced[1]
    futures = _selected(FUTURES, CORE_FUTURES)
    for s_point, k in futures:
        key = _row_key(sec, "future", s_point, -k)
        if key in sec.Projection.itemspaces:
            _release(sec, key)
        try:
            faults += _outside_cover_faults(projection(sec, key),
                                            _case_id("future", s_point, -k))
        finally:
            _release(sec, key)
    assert futures and not faults, (
        f"{len(faults)} faults outside cover, first:\n  " + "\n  ".join(faults[:20]))


def test_the_points_sum_row_by_row_into_a_block(spliced):
    """Row ``t`` is the same month on every point, so a block is its frames summed (D3).

    S point 1's twin, the point restated at month 12 and the point issued 12 months on,
    summed as ``run_sec.py --block`` sums them, are indexed 0..311 and equal S's frame added
    to itself moved 12 months earlier and 12 months later.  A model whose frames sat on the
    policy clock would fail it.
    """
    s, sec = spliced
    cases = (("derived", 1, 12), ("future", 1, -12))
    keys = [_row_key(sec, *case) for case in cases if SEC_FULL or case in CORE_GRID]
    assert len(keys) == 2, "the block's rows are the core's"
    twin = _row_key(sec, "twin", 1, 0)
    try:
        frames = [projection(sec, key).result_cf() for key in (twin, *keys)]
    finally:
        for key in (twin, *keys):
            _release(sec, key)
    block = pd.concat(frames).groupby(level="t").sum()
    sdf = _point(s, 1).result_cf()
    expected = pd.concat([sdf, sdf.set_axis(sdf.index - 12).loc[0:],
                          sdf.set_axis(sdf.index + 12)]).groupby(level=0).sum()
    assert list(block.index) == list(range(312))
    assert frame_mismatches(expected, block) == []


# The labels an extract carries in the test below: the committed points' in reverse, from
# 114 down, so that a label is neither a position plus one nor in the order of the rows.
EXTRACT_LABELS = tuple(range(114, 100, -1))


def _extract():
    """The committed table and pipeline as an administration extract would hold them:
    without the generator's columns, and labelled :data:`EXTRACT_LABELS`."""
    extract = _committed().drop(columns=list(generated_columns(SPEC)))
    relabel = dict(zip(extract.index, EXTRACT_LABELS))
    extract.index = pd.Index(EXTRACT_LABELS, name="point_id")
    pipeline = _committed_pipeline()
    pipeline["point_id"] = pipeline["point_id"].map(relabel)
    return extract, pipeline


def test_an_in_force_extract_needs_none_of_the_generator_columns(sec_model, tmp_path):
    """The model reads the in-force interface and S's columns, never where a row came from,
    and names each point by its label, wherever the row stands.

    ``row_kind``, ``source_policy_id`` and ``source_mth`` record how the generator made each
    shipped row, and an administration extract carries none of them.  Read without them,
    and with every label changed in the table and the pipeline together, every point
    projects what the committed table projects, in ``result_cf`` and ``result_pols``, to
    1e-12, and ``run_sec.py``, run beside that extract, prints the point without saying
    where it came from.  On every shipped row ``source_mth`` equals ``duration_mth``, 60 on
    the in-force twin as on the indexed point restated at 60, so a formula that read the
    one for the other would pass every test that leaves ``duration_mth`` as generated.
    And a refusal names the extract's label.
    """
    extract, pipeline = _extract()
    absent = ("row_kind", "source_policy_id", "source_mth")
    assert absent == generated_columns(SPEC), generated_columns(SPEC)
    assert not set(absent) & set(extract.columns), list(extract.columns)
    folder = _sec_inputs(tmp_path / "extract", extract, pipeline)
    model = mx.read_model(folder, name=_name("extract"))
    try:
        table = model.Data.model_point_table()
        assert not set(generated_columns(SPEC)) & set(table.columns)
        assert list(table.index) == list(EXTRACT_LABELS)
        for key, base_key in zip(point_keys(model), point_keys(sec_model)):
            mine, base = projection(model, key), projection(sec_model, base_key)
            for report in ("result_cf", "result_pols"):
                assert frame_mismatches(base.cells[report](), mine.cells[report](),
                                        rtol=1e-12, atol=1e-12) == [], (key, report)
            _release(model, key)
    finally:
        model.close()
    runner = folder.parent / "run_sec.py"
    shutil.copy(model_path(SEC).parent / "run_sec.py", runner)
    label = extract.index[extract["policy_id"] == "TA-000007-M66"][0]
    out = _run_sec(runner, str(label))
    count = _row(sec_model, "derived", 7, 66).pols_if(0)
    assert out.splitlines()[:2] == [
        f"model point {label}: TA-000007-M66 - F45 smoker S level shape, 20-year term, "
        f"cover 250,000, monthly mode, select basis, waiver",
        f"at the valuation date: in force 66 months: policy year 6, attained age 50, "
        f"{count:.6f} in force"]
    last = extract.index[extract["policy_id"] == "TA-000001-M299"][0]
    moved = _set("duration_mth", [last], 301)(extract)
    model = mx.read_model(_sec_inputs(tmp_path / "moved", moved, pipeline),
                          name=_name("moved"))
    try:
        _refused(_point(model, last).result_cf,
                 f"point_id {last}: duration_mth 301 is at or past the end of cover, "
                 f"policy month 300")
    finally:
        model.close()


def _standing(p):
    """What ``run_sec.py`` says of point ``p`` at the valuation date, stated here."""
    d = p.duration_mth_init()
    if d < 0:
        return f"to be issued at t = {-d}, {-d} months after the valuation date"
    if d == 0:
        return "issued at the valuation date, t = 0"
    return (f"in force {d} months: policy year {p.policy_year(0)}, attained age "
            f"{p.age(0, 1)}, {p.pols_if(0):.6f} in force")


def test_run_sec_prints_a_point_and_the_block(sec_model):
    """The runner prints one point, saying where it came from, and the block (D8).

    Each mode in an interpreter of its own, as a user runs it, with exit code 0 and ASCII
    output, so that it prints on a Windows console under any code page.  The numbers are
    the model's.  The anchor cell, the runner's default, with its lines at the valuation
    date, each asserted whole, so that a longer number cannot pass for the one asserted,
    and its first twelve rows of cash flows and counts.  Point 6, the joint life, whose
    line names its second life through the cells that take one; point 9, restated in force
    at S's month 60; and point 14, to be issued 13 months on: each with the two lines that
    say where its row came from and where it stands, which only the committed table's
    generator columns can say.  And the block: a line for each of the 14 points, in table
    order, its first twelve rows, which must be the committed points' frames summed row by
    row, as this test sums them, and those frames summed into projection years, each
    year's count the one in force in its first month.  Nothing else runs the runner on the
    committed table.
    """
    runner = model_path(SEC).parent / "run_sec.py"
    out = _run_sec(runner)
    assert out.splitlines()[:3] == [
        "model point 1: TA-000001 (S's TA-000001) - M35 smoker N level shape, 25-year "
        "term, cover 150,000, monthly mode, applied basis",
        "at the valuation date: issued at the valuation date, t = 0",
        "proj_len = 300 months from the valuation date (t = 0..299); cover ends at policy "
        "month 300"]
    anchor = _row(sec_model, "twin", 1, 0)
    assert anchor.result_cf().head(12).round(2).to_string() in out
    assert anchor.result_pols().head(12).round(6).to_string() in out
    count = _row(sec_model, "derived", 5, 60).pols_if(0)
    for point_id, lines in (
            ("6", ["model point 6: TA-000006 (S's TA-000006) - M35 smoker N level shape, "
                   "25-year term, cover 150,000, monthly mode, applied basis, joint with "
                   "F33 smoker N",
                   "at the valuation date: issued at the valuation date, t = 0"]),
            ("9", ["model point 9: TA-000005-M60 (S's TA-000005 at its month 60) - M35 "
                   "smoker N level shape, 25-year term, cover 150,000, monthly mode, "
                   "applied basis, indexed",
                   f"at the valuation date: in force 60 months: policy year 6, attained "
                   f"age 40, {count:.6f} in force"]),
            ("14", ["model point 14: TA-000007-F13 (S's TA-000007, issued 13 months on) "
                    "- F45 smoker S level shape, 20-year term, cover 250,000, monthly "
                    "mode, select basis, waiver",
                    "at the valuation date: to be issued at t = 13, 13 months after the "
                    "valuation date"])):
        assert _run_sec(runner, point_id).splitlines()[:2] == lines, point_id
    out = _run_sec(runner, "--block")
    table = sec_model.Data.model_point_table()
    points = [projection(sec_model, key) for key in point_keys(sec_model)]
    assert out.splitlines()[:len(points) + 1] == [
        "model points, t = 0 the valuation date for each:",
        *("  {:>2}  {:<15} {}; proj_len {}".format(
            point_id, table.at[point_id, "policy_id"], _standing(p), p.proj_len())
          for point_id, p in zip(table.index, points))]
    block = pd.concat([p.result_cf() for p in points]).groupby(level="t").sum()
    assert block.head(12).round(2).to_string() in out
    years = pd.Index(block.index // 12 + 1, name="proj_year")
    annual = block.drop(columns="pols_if").groupby(years).sum()
    annual.insert(0, "pols_if", [block.at[12 * (y - 1), "pols_if"] for y in annual.index])
    assert annual.head(12).round(2).to_string() in out


# run_sec.py run as though it sat at /m/products/term_assurance, in a products/ folder
# whose parent carries no build tool: the source compiled under that name, so that its own
# __file__ is it.
SHALLOW_RUN = """\
import sys
source = open(sys.argv[1], encoding="utf-8").read()
where = "/m/products/term_assurance/run_sec.py"
sys.argv = [where, "--cython"]
exec(compile(source, where, "exec"), {"__name__": "__main__", "__file__": where})
"""


def test_run_sec_says_a_product_outside_a_library_cannot_build(tmp_path):
    """``run_sec.py --cython`` stops, saying it cannot build, outside a library.

    The runner is uslib Term's as it stands, ``--cython`` and ``_tool()`` included
    (USLIB-SEC-PLAN.md §7.1, *Record — M14*, *Carried into Phase 1*), so that the C step
    changes nothing in it.  ``--cython`` builds with the ``build_sec_cy.py`` the library
    carries at its root, beside ``products/``, so that lifelib and every
    ``lifelib.create()`` copy of the library build as the source repository does.  A
    product directory taken out of its library has no tool above it, wherever it is put:
    beside a copy of the model and its inputs, and in a ``products/`` folder whose parent
    carries no tool, the path at which uslib's runner, when it looked for the tool in the
    repository, once raised ``IndexError``.  Each must exit nonzero having printed nothing,
    and say why.  Neither needs modelx-cython, since neither gets as far as building.
    """
    runner = model_path(SEC).parent / "run_sec.py"
    copy = _sec_inputs(tmp_path / "copy", _committed()).parent / "run_sec.py"
    shutil.copy(runner, copy)
    shallow = tmp_path / "shallow.py"
    shallow.write_text(SHALLOW_RUN, encoding="utf-8")
    for args in ((copy, "1", "--cython"), (shallow, runner)):
        done = _run_sec(*args, check=False)
        stderr = done.stderr.decode(errors="replace")
        assert done.returncode != 0 and done.stdout == b"", stderr
        assert "is in no library that carries one, so it cannot build" in stderr, stderr


def test_the_runner_sums_the_block_as_groupby_does(sec_model):
    """``run_sec.py``'s running sum of the block is pandas' ``groupby`` sum, bit for bit.

    A block run keeps one point's frame at a time, so it sums the frames as it goes,
    compensated, with ``add``, so that the block is the frames concatenated and summed by
    ``t``, as a runner that kept every point would, to the last bit.  The printed block, to
    two decimals, cannot show a last bit, so ``add`` itself is read from the runner, which
    runs the model when imported, and run here on the committed points' frames.  A plain
    running sum differs from ``groupby``'s on them, so the comparison can fail.
    """
    tree = ast.parse((model_path(SEC).parent / "run_sec.py").read_text(encoding="utf-8"))
    found = [node for node in tree.body
             if isinstance(node, ast.FunctionDef) and node.name == "add"]
    assert len(found) == 1
    space = {}
    exec(compile(ast.Module(found, []), "run_sec.py", "exec"), space)
    frames = [projection(sec_model, key).result_cf() for key in point_keys(sec_model)]
    columns = list(frames[0].columns)
    rows = max(len(frame) for frame in frames)
    total, compensation = np.zeros((rows, len(columns))), np.zeros((rows, len(columns)))
    plain = np.zeros((rows, len(columns)))
    for frame in frames:
        space["add"](total, compensation, frame[columns].to_numpy())
        plain[:len(frame)] += frame[columns].to_numpy()
    want = pd.concat(frames).groupby(level="t").sum()[columns].to_numpy()
    assert np.array_equal(total, want)
    assert not np.array_equal(plain, want)


# The six cells to which Term_UK_S gives a life defaulted to 1, which here take it with no
# default.
LIFE_CELLS = ("age_at_entry", "sex", "smoker", "age", "mort_rate_base", "mort_rate_life")


def _defaulted(model_name):
    """The cells of ``model_name``'s Projection with a parameter that has a default, sorted,
    read from its source, as the C step's build reads it."""
    source = (model_path(model_name) / "Projection" / "__init__.py").read_text(
        encoding="utf-8")
    return sorted(node.name for node in ast.parse(source).body
                  if isinstance(node, ast.FunctionDef)
                  and (node.args.defaults or any(node.args.kw_defaults)))


def test_no_cell_takes_a_default():
    """No cell has a defaulted parameter (R12).

    ``Term_UK_S`` gives :data:`LIFE_CELLS` a ``life`` defaulted to 1, and ``claims`` a
    ``kind=None`` for its total.  A compiled model declares a defaulted parameter in its
    ``.pxd`` as ``long long life=*``, which the typing guard would read as a parameter
    named ``life=*``, and a ``kind`` traced both as a code and as ``None`` compiles to a
    Python object with a dict for a cache, on ``net_cf``'s path.  So here none of the six
    has a default and every caller passes 1 or 2, positionally, a call that left it out
    raising; and the total is the code ``ALL``, which ``net_cf`` passes, and the spec's
    ``twin_arg_map`` maps S's ``None`` onto.  modelx keys ``Term_UK_S``'s ``age(t)`` by the
    arguments bound, ``(t, 1)``, and its ``claims(t)`` as ``(t, None)``, so the twin
    identity, which ``test_model_conventions_uk`` asserts, pairs the cells as before.
    """
    assert _defaulted(TWIN) == sorted((*LIFE_CELLS, "claims"))
    assert _defaulted(SEC) == []


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
    ``=`` in the border under the header give the column spans.  A name is an identifier
    outside the parentheses of the column, ``age`` of ``age(t, life)``; a cell of two names,
    ``sex(life), smoker(life)``, maps both.
    """
    lines = doc.splitlines()
    head = next(i for i, line in enumerate(lines) if line.startswith("Notes symbol"))
    start, end = [m.span() for m in re.finditer("=+", lines[head + 1])][1]
    names = set()
    for line in lines[head + 2:]:
        if line.startswith("="):
            break
        bare = re.sub(r"\([^)]*\)", "", line[start:end])
        names.update(re.findall(r"[a-z_][a-z0-9_]*", bare))
    return names


_RULE = re.compile(r"^\s*=+(?:\s+=+)+\s*$")


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
            taken = {j for j, ch in enumerate(lines[i]) if ch != " "}
            if not _RULE.match(lines[i]) and taken & gaps:
                found.append(lines[i].strip())
            i += 1
    return found


# What only Term_UK_S's docstrings may say: a reference into its Spaces, which the SEC
# pages would link to the wrong model; its clock, t counting policy months from issue and
# t = 0 the issue month; a call of a cell this model does not have; and S's in-force
# frame opening at 12 x duration_inforce().
STALE = re.compile(r"~\.Term_UK_S\.|``t = 0`` is the issue month"
                   r"|``t`` counts \*\*policy months from issue"
                   r"|\b(?:proj_start|duration_inforce)\(\)")


def test_the_docstrings_describe_the_valuation_clock(sec_model, s_model):
    """The docstrings say what this model is, and none says what only Term_UK_S is.

    Whitespace is collapsed first, as ``test_model_conventions_uk`` collapses it, so that a
    phrase split across a line break still matches.  The model docstring names the
    valuation date, BasicTerm_SE, the policy clock, the SEC table, the pipeline and the
    product.  The symbol map in the Projection docstring maps every cell running in force
    adds, which are exactly the cells ``Term_UK_S`` lacks, and names nothing the model
    lacks: every name in it is a cell or a Reference.  No row of a simple table in any
    docstring puts text between two of its columns (:func:`_table_overruns`), which would
    drop the table from the rendered page.  And no docstring says what :data:`STALE`
    matches.
    """
    flat = {where: re.sub(r"\s+", " ", doc) for where, doc in _docs(sec_model)}
    for phrase in ("valuation date", "BasicTerm_SE", "duration_mth", TABLE, PIPELINE,
                   "term assurance"):
        assert phrase in flat["model"], phrase
    assert set(NEW_CELLS) == set(sec_model.Projection.cells) - set(s_model.Projection.cells)
    mapped = _mapped_cells(sec_model.Projection.doc)
    missing = [cells for cells in NEW_CELLS if cells not in mapped]
    assert not missing, f"the symbol map does not map {missing}"
    known = set(sec_model.Projection.cells) | set(sec_model.Projection.refs)
    unknown = sorted(mapped - known)
    assert not unknown, f"the symbol map names what the model lacks: {unknown}"
    overruns = {where: rows for where, rows in ((where, _table_overruns(doc))
                                                for where, doc in _docs(sec_model)) if rows}
    assert not overruns, f"table rows that run into a column gap: {overruns}"
    stale = sorted(where for where, doc in flat.items() if STALE.search(doc))
    assert not stale, f"docstrings that describe Term_UK_S: {stale}"


@pytest.mark.docutils
def test_the_docstrings_parse_as_rst(sec_model):
    """Every docstring of the model parses as reStructuredText, without a warning.

    The docs build reads each docstring through docutils, which reports a malformed table, a
    bad indentation or an unclosed inline markup and drops what it cannot read; a raw-text
    test sees none of it.  Each docstring, dedented as autodoc dedents it and its Sphinx
    roles read as plain interpreted text, which docutils alone does not know, is parsed
    here, and any warning or error is a fault.  docutils comes with the docs build, not with
    the models' requirements, so the test is skipped where it is absent; the column check
    in the test above runs everywhere.
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


def test_the_sec_model_reads_the_s_tables_in_place(sec_model, s_model):
    """One copy of each assumption table serves both models (D1).

    The two ``input_dir()`` s are one directory, and SEC's filename References are S's with
    ``model_point_file`` changed, to ``model_point_table_sec.csv``, and one added, the
    pipeline's: an edit to a table reaches both models, and the two can never drift apart.
    """
    assert sec_model.Data.input_dir() == s_model.Data.input_dir()
    files = {r: v for r, v in s_model.Data.refs.items() if r.endswith("_file")}
    assert {r: v for r, v in sec_model.Data.refs.items() if r.endswith("_file")} == {
        **files, "model_point_file": TABLE, "wop_pipeline_file": PIPELINE}


def test_the_core_grid_reaches_every_branch(spliced, splice_records):
    """What the default run's T2 and T3 cases reach, which the full grid only multiplies.

    The default run thins the splice to a core (the module docstring), and this test is
    what keeps the thinning from costing a branch.  First, statically, over S's table with
    the variants, each property below holds of some core case: every shape, both
    mortality bases, both premium modes, the four sex and smoker groups of the first life
    and a second life, the indexation option, the waiver, a family income benefit commuted
    in part and whole, a decreasing schedule at a zero rate, S's in-force row as its twin
    and restated; and each kind of valuation month: the first months, inside the waiver's
    deferred period and at its first entrants, on an anniversary, in the month before one,
    mid-year, about the selective-lapse ratio's crossing, either side of the clawback
    window's end and of the select period's, and the last covered month.  And of some core
    future case: issued off the valuation anniversaries and on them, more than a year on,
    each shape, the waiver, an annual payer and the indexation option.

    Then, on the splice's model, of some core row, each of :data:`AT_VALUATION` and
    :data:`IN_FRAME`, what no column of the table shows: every opening-state column in use,
    and the pipeline partly and wholly filled; and every branch and both sides of every
    ``min`` and ``max`` the full grid reaches: the select duration's, the lapse table's
    last year, the selective-lapse excess's, the waiver's three sources of entrants, the
    clawback window, an index step, the decreasing straight line, a part commutation, the
    second life and the expiry.

    Each core row's branches were recorded by the T2 or T3 case that compared it
    (:func:`_settle`), and a row no case has recorded is evaluated here.  With
    ``UKLIB_SEC_FULL=1`` it asks the same of the full grid's rows, which must reach nothing
    the core does not.
    """
    s_table = _s_table_with_variants()

    def at(p, column):
        return s_table.at[p, column]

    def flag(p, column):
        return str(at(p, column)).lower() == "true"

    splices = {
        **{f"the {s} shape": (lambda k, p, d, s=s: at(p, "shape") == s)
           for s in ("level", "decreasing", "fib")},
        **{f"the {b} basis": (lambda k, p, d, b=b: at(p, "mort_basis") == b)
           for b in ("applied", "select")},
        **{f"{m} mode": (lambda k, p, d, m=m: at(p, "premium_mode") == m)
           for m in ("monthly", "annual")},
        **{f"sex {x}, smoker {y}, of either life": (lambda k, p, d, x=x, y=y: (
            (at(p, "sex"), at(p, "smoker")) == (x, y)
            or (flag(p, "joint_first_death")
                and (at(p, "joint_sex"), at(p, "joint_smoker")) == (x, y))))
           for x in ("M", "F") for y in ("N", "S")},
        **{f"a second life, sex {x}, smoker {y}": (lambda k, p, d, x=x, y=y: (
            flag(p, "joint_first_death") and (at(p, "joint_sex"), at(p, "joint_smoker"))
            == (x, y))) for x, y in (("F", "N"), ("M", "S"))},
        "indexation": lambda k, p, d: flag(p, "indexation"),
        "the waiver": lambda k, p, d: flag(p, "wop"),
        "an indexed waiver point": lambda k, p, d: flag(p, "wop") and flag(p, "indexation"),
        "a FIB commuted whole": lambda k, p, d: at(p, "fib_commute_rate") == 1.0,
        "a FIB commuted in part": lambda k, p, d: 0.0 < at(p, "fib_commute_rate") < 1.0,
        "a decreasing schedule at 0": lambda k, p, d: (
            at(p, "shape") == "decreasing" and at(p, "sched_rate") == 0.0),
        "S's in-force row as its twin": lambda k, p, d: (k, p) == ("twin", 8),
        "S's in-force row restated": lambda k, p, d: (k, p) == ("derived", 8),
        "in the second month": lambda k, p, d: d == 1,
        "inside the deferred period, the waiver": lambda k, p, d: (
            flag(p, "wop") and 0 < d < 7),
        "at the waiver's first entrants": lambda k, p, d: flag(p, "wop") and d == 7,
        "on an anniversary": lambda k, p, d: k == "derived" and d % 12 == 0,
        "in the month before an anniversary": lambda k, p, d: d % 12 == 11,
        "mid-year": lambda k, p, d: d % 12 not in (0, 11),
        "the lapse ratio's crossing": lambda k, p, d: d in (22, 23),
        "the clawback window's last month": lambda k, p, d: d == 47,
        "past the clawback window": lambda k, p, d: d == 48,
        "the select period's last year": lambda k, p, d: (
            at(p, "mort_basis") == "select" and 48 <= d < 60),
        "past the select period": lambda k, p, d: (
            at(p, "mort_basis") == "select" and d >= 60),
        "in the last covered month": lambda k, p, d: d == COVER[p] - 1,
    }
    futures = {
        "issued off the anniversaries": lambda p, k: k % 12 != 0,
        "issued on them": lambda p, k: k % 12 == 0,
        "issued more than a year on": lambda p, k: k > 12,
        **{f"the {s} shape": (lambda p, k, s=s: at(p, "shape") == s)
           for s in ("level", "fib")},
        "the waiver": lambda p, k: flag(p, "wop"),
        "an annual payer": lambda p, k: at(p, "premium_mode") == "annual",
        "indexation": lambda p, k: flag(p, "indexation"),
        "a second life": lambda p, k: flag(p, "joint_first_death"),
    }
    missing = [what for what, holds in splices.items()
               if not any(holds(*case) for case in CORE_SPLICES)]
    missing += [what for what, holds in futures.items()
                if not any(holds(*case) for case in CORE_FUTURES)]
    assert not missing, f"no core case reaches: {missing}"

    reached = set()
    for case in sorted(CORE_GRID):
        reached |= _record_of(spliced, splice_records, case)["branches"]
    missing = [what for what in (*AT_VALUATION, *IN_FRAME) if what not in reached]
    assert not missing, f"no core row reaches: {missing}"
    if SEC_FULL:
        beyond = set()
        for case in GRID:
            if case not in CORE_GRID:
                beyond |= _record_of(spliced, splice_records, case)["branches"]
        assert beyond <= reached, f"the full grid alone reaches: {sorted(beyond - reached)}"


# ---------------------------------------------------------------------------
# The C step's representation (UKLIB-SEC-PLAN.md §6.1, *C*)
#
# Data decodes each model point's text into the number the projection reads, and turns
# each table into an array indexed by integers (USLIB-SEC-PLAN.md R5-R8); a timing and a
# kind are int codes, and the claims total is a code of its own (R9, R12).  These tests
# hold the representation in modelx, with no compiler, in seconds: the compiled section
# after the fingerprint holds the compiled model to modelx on it.


# Whether sum() compensates, Neumaier's way, as it does for floats from Python 3.12 on most
# builds, read from sum() itself as test_model_conventions_uk.py's SUM_COMPENSATES reads it.
# The ledger residual sums the deaths as Term_UK_S's sum() does, written out, so it is S's
# bits only where sum() compensates.  Python 3.11's sum() adds left to right, and there
# S's residual parts from this one in most months of a family income benefit point
# (UKLIB-SEC-PLAN.md §6.3, *Record -- M8*, *Carried into M15*): the residual's bit test
# holds the rest and skips the bits there, with this reason.
SUM_COMPENSATES = sum([0.1] * 10) == 1.0
SUM_311 = ("Python 3.11's sum() adds floats left to right, without the compensation it has "
           "from 3.12, so the sum written out here is not its bits; the rest was held")


def _hold_the_sums_bits():
    """Skip the rest of the calling test, naming Python 3.11 (:data:`SUM_311`), where
    ``sum()`` adds floats left to right (:data:`SUM_COMPENSATES`); return where it
    compensates, so that the test goes on to hold the bits."""
    if not SUM_COMPENSATES:
        pytest.skip(SUM_311)


def test_the_sums_bits_skip_only_where_sum_adds_left_to_right(monkeypatch):
    """The guard of the sums' bits skips where, and only where, ``sum()`` adds left to
    right.

    :data:`SUM_COMPENSATES` must be ``sum()``'s own answer on this interpreter, which
    ``math.fsum``, rounding once, gives too: 1.0 for ten tenths where ``sum()``
    compensates, as from Python 3.12, and not on Python 3.11.  So the bits are held
    wherever ``sum()`` compensates; inverted, the guard would skip them there without a
    word, CI running this module on Python 3.13 alone.  And :func:`_hold_the_sums_bits`
    goes on where :data:`SUM_COMPENSATES` holds, and skips, naming Python 3.11, where it
    does not.
    """
    assert SUM_COMPENSATES == (sum([0.1] * 10) == math.fsum([0.1] * 10)), SUM_COMPENSATES
    module = sys.modules[__name__]
    monkeypatch.setattr(module, "SUM_COMPENSATES", True)
    try:
        _hold_the_sums_bits()
    except pytest.skip.Exception as err:
        pytest.fail(f"the guard skips where sum() compensates: {err}")
    monkeypatch.setattr(module, "SUM_COMPENSATES", False)
    with pytest.raises(pytest.skip.Exception, match="Python 3.11's sum"):
        _hold_the_sums_bits()


def _part_commuted(tmp_path, name):
    """S read on its point 10 alone, the family income benefit commuted in half, and SEC
    on that point's twin, which the generator makes from it: ``(s, sec)``, each to close.
    """
    rows = _s_table_with_variants().loc[[10]]
    s = mx.read_model(temp_inputs(tmp_path / "s", model_path(TWIN), model_points=rows),
                      name=_name(f"{name}_s"))
    try:
        spec = dataclasses.replace(SPEC, derived=(), future=())
        twins, companions = build_sec_table(spec, s)
        sec = mx.read_model(_sec_inputs(tmp_path / "sec", twins, companions[PIPELINE]),
                            name=_name(name))
    except BaseException:
        s.close()
        raise
    return s, sec


def test_the_all_total_is_s_total_bit_for_bit(sec_model, s_model, tmp_path):
    """``claims(t, ALL)`` is ``Term_UK_S``'s ``claims(t)``, its ``sum``, to the last bit.

    S totals its three kinds with Python's ``sum``, which compensates, and the total here
    is written left to right from ``0.0`` (``Projection.claims``), which is ``sum``'s float
    wherever at most two kinds are non-zero in a month.  The lapse kind is 0.0 in every
    month, so the two could part only where a third kind paid.  T1 compares the totals to
    1e-9; this compares them by ``float.hex``, in every month of every twin of S's new
    business, of S's in-force point from its month 60, and of the family income benefit
    commuted in part, S's point 3 at a take-up of 0.5, where the lump sum and the
    instalments are both paid in a month, which is asserted of some month.
    """
    total = _code(sec_model.Projection, "ALL")
    found = []
    table = sec_model.Data.model_point_table()
    for point_id in table.index[table["row_kind"] == "twin"]:
        month = int(table.at[point_id, "source_mth"])
        s, p = _point(s_model, point_id), _point(sec_model, point_id)
        found += [f"point {point_id}, t = {t}" for t in range(p.proj_len())
                  if p.claims(t, total).hex() != s.claims(t + month).hex()]
    s, sec = _part_commuted(tmp_path, "total")
    try:
        q, sq = projection(sec, point_keys(sec)[0]), _point(s, 10)
        death, fib = _code(q, "DEATH"), _code(q, "FIB")
        months = range(q.proj_len())
        both = [t for t in months if q.claims(t, death) != 0.0 and q.claims(t, fib) != 0.0]
        found += [f"part commuted, t = {t}" for t in months
                  if q.claims(t, total).hex() != sq.claims(t).hex()]
    finally:
        sec.close()
        s.close()
    assert both, "no month of the part-commuted point pays two kinds"
    assert not found, found[:10]


def test_the_ledger_residual_is_s_own_bit_for_bit(sec_model, s_model, tmp_path):
    """``check_fib_ledger_resid(t)`` is ``Term_UK_S``'s to the last bit, every month.

    The residual rebuilds the streams in payment from the deaths since issue, and S sums
    those deaths with Python's ``sum``, which compensates; this model sums them in a loop,
    compensated as ``sum`` compensates them, by Neumaier's method
    (``Projection.check_fib_ledger_resid``).  Nothing else sees the loop: T1 and T2 floor
    the residual at 1e-9, since at a take-up such as 0.3 the two models' rebuilds round
    apart (*The in-force interface* in ``model-sec.md``), the fingerprint covers the
    reports alone, and C4 compares two engines that run the same loop.  A plain sum gives a
    residual that still closes, ``check_fib_ledger()`` True, and moves 309 of the
    committed points' residuals, 203 of point 3's 300 months.  So this compares the two
    by ``float.hex`` in every month of the twins of S's family income benefit points, 3,
    uncommuted, and 4, commuted whole, at the shipped take-ups, and of S's point 10, the
    same commuted in half, where the two sums agree too; S's residuals there are not all
    0, which is asserted.

    S's deaths are summed by ``sum``'s bits only where it compensates, from Python 3.12.
    Where it does not, on Python 3.11 (:data:`SUM_COMPENSATES`), S adds them left to right,
    as its ledger adds them, so that its residual is 0 in every month and this one's is
    not: there the points are held, and the bits and S's residuals skip, naming Python
    3.11 (:data:`SUM_311`).
    """
    found, nonzero = [], 0
    for point_id in (3, 4):
        s, p = _point(s_model, point_id), _point(sec_model, point_id)
        assert p.duration_mth_init() == 0 and p.is_fib(), point_id
        for t in range(p.proj_len()):
            mine, want = p.check_fib_ledger_resid(t), s.check_fib_ledger_resid(t)
            nonzero += want != 0.0
            if mine.hex() != want.hex():
                found.append(f"point {point_id}, t = {t}: {mine!r}, S {want!r}")
    s, sec = _part_commuted(tmp_path, "ledger")
    try:
        q, sq = projection(sec, point_keys(sec)[0]), _point(s, 10)
        assert q.fib_commute_rate() == 0.5
        for t in range(q.proj_len()):
            mine, want = q.check_fib_ledger_resid(t), sq.check_fib_ledger_resid(t)
            nonzero += want != 0.0
            if mine.hex() != want.hex():
                found.append(f"part commuted, t = {t}: {mine!r}, S {want!r}")
    finally:
        sec.close()
        s.close()
    _hold_the_sums_bits()
    assert not found, f"{len(found)} months apart, first: {found[:10]}"
    assert nonzero, "every residual of S's is 0, so no sum is seen"


# One S point per value a decoded column can hold, as (the S point it changes, the columns
# it changes): each shape; each sex and smoker status of the first life and of the second;
# both premium modes; both mortality bases; each flag both ways; and the numbers
# Term_UK_S reads with int, the issue ages and the term, written with a fraction, which
# int truncates: each fraction above .5, so that a decode that rounded would part.
DECODED = [
    (1, {"shape": "level"}), (2, {"shape": "decreasing"}), (3, {"shape": "fib"}),
    *[(1, {"sex": x, "smoker": y}) for x in ("M", "F") for y in ("N", "S")],
    *[(6, {"joint_sex": x, "joint_smoker": y}) for x in ("M", "F") for y in ("N", "S")],
    (1, {"premium_mode": "annual"}), (1, {"premium_mode": "monthly"}),
    (7, {"mort_basis": "applied"}), (1, {"mort_basis": "select"}),
    (5, {"indexation": True}), (1, {"indexation": False}),
    (7, {"wop": True}), (1, {"wop": False}),
    (6, {"joint_first_death": True}), (6, {"joint_first_death": False}),
    (1, {"age_at_entry": 35.7}), (6, {"joint_age": 33.6}), (1, {"policy_term": 25.6}),
]

# The cells each decoded point is compared on, Term_UK_S's own, which read the text or
# the number themselves, and their decodes here, each against S's comparison of the text.
DECODING_CELLS = ("is_joint", "indexation", "wop", "policy_term", "term_mths", "shape",
                  "premium_mode", "mort_basis")
DECODES = {"is_level": lambda s: s.shape() == "level",
           "is_decreasing": lambda s: s.shape() == "decreasing",
           "is_fib": lambda s: s.shape() == "fib",
           "prem_cycle": lambda s: 12 if s.premium_mode() == "annual" else 1,
           "is_select_basis": lambda s: s.mort_basis() == "select"}


def test_every_decode_is_term_uk_s_own_on_every_value(tmp_path):
    """``Data`` decodes every value a column can hold as ``Term_UK_S``'s cells read it.

    A point of each case of :data:`DECODED` goes into a copy of S's table, and its twin,
    generated from it, into a copy of SEC's.  On each pair every cell of
    :data:`DECODING_CELLS` agrees exactly, in value and in type, the labels among them;
    each decode of :data:`DECODES` is S's comparison of the text, as an int or a bool;
    each life's issue age is S's ``int`` of its column, a fraction truncated; and each
    life's row of the mortality table, ``mort_group(life)``, holds S's rate for that life's
    sex and smoker status at every age of the table, so that ``mort_rate_base`` is S's at
    every month the frame reads.  T1 and the splice see these through the cells that use
    them, at the values their points carry; this sees every value, on its own.
    """
    s_table = _s_table()
    rows = []
    for i, (base, changes) in enumerate(DECODED, start=1):
        row = s_table.loc[[base]].assign(**changes, policy_id=f"TA-8{i:05d}")
        row.index = pd.Index([i], name="point_id")
        rows.append(row)
    table = pd.concat(rows)
    s = mx.read_model(temp_inputs(tmp_path / "s", model_path(TWIN), model_points=table),
                      name=_name("decoded_s"))
    sec = None
    found = []
    try:
        spec = dataclasses.replace(SPEC, derived=(), future=())
        twins, companions = build_sec_table(spec, s)
        sec = mx.read_model(_sec_inputs(tmp_path / "sec", twins, companions[PIPELINE]),
                            name=_name("decoded"))
        rates = s.Data.mort_table()["mort_rate"]
        array = sec.Data.mort_table_array()
        for (base, changes), key, label in zip(DECODED, point_keys(sec), table.index):
            case = f"S point {base} with {changes}"
            sp, p = projection(s, label), projection(sec, key)
            lives = (1, 2) if sp.is_joint() else (1,)
            calls = [(cell, ()) for cell in DECODING_CELLS]
            calls += [(cell, (life,)) for life in lives
                      for cell in ("age_at_entry", "sex", "smoker")]
            calls += [("mort_rate_base", (t, life)) for life in lives for t in (0, 120)]
            for cell, args in calls:
                want, got = sp.cells[cell](*args), p.cells[cell](*args)
                if got != want or type(got) is not type(want):
                    found.append(f"{case}: {cell}{args} is {got!r}, S {want!r}")
            for cell, read in DECODES.items():
                want, got = read(sp), p.cells[cell]()
                if got != want or type(got) is not type(want):
                    found.append(f"{case}: {cell}() is {got!r}, S's text gives {want!r}")
            for life in lives:
                g = p.mort_group(life)
                for a in range(sec.Data.mort_age_first(), sec.Data.mort_age_last() + 1):
                    want = rates.loc[(sp.sex(life), sp.smoker(life), a)]
                    if array[g, a] != want:
                        found.append(f"{case}: life {life}'s row {g} at age {a} is "
                                     f"{array[g, a]!r}, S's rate {want!r}")
    finally:
        if sec is not None:
            sec.close()
        s.close()
    assert not found, found[:20]


def test_every_padded_array_holds_nan_and_no_reader_reads_it(sec_model, tmp_path):
    """The padding is NaN, and each array's one reader refuses a key outside it, by name.

    ``Data`` tables the mortality rates from age 0 and the lapse rates from policy year 0,
    and pads what no file holds with NaN, as its docstring says, so that a read past a
    check, were one lost, would make every number after it NaN rather than another key's
    value: each row's ages below the table's first, 18 as shipped, and year 0.  The waiver
    pipeline, by point and lag, holds NaN at lag 0 and wherever a point holds no row.
    Inside, nothing is NaN.

    And on the extract labelled otherwise than by position (:func:`_extract`), where a
    label read as ``idx + 1`` would name another point, each reader refuses a key outside
    its array before it reads it, naming the point and the key: a lag the point's pipeline
    does not hold, below 1 or past its last; a select duration below the table's, where
    ``select_period`` is set below 0, which a negative index would read from the table's
    end; and an attained age below the mortality table's, on a copy that starts it at 20.
    """
    data = sec_model.Data
    mort = data.mort_table_array()
    first, last = data.mort_age_first(), data.mort_age_last()
    assert mort.shape == (4, last + 1) and (first, last) == (18, 100)
    assert np.isnan(mort[:, :first]).all() and not np.isnan(mort[:, first:]).any()
    lapse = data.lapse_table_array()
    assert lapse.shape == (data.lapse_last_year() + 1,) and np.isnan(lapse[0])
    assert not np.isnan(lapse[1:]).any()
    select = data.select_factor_array()
    assert select.shape == (data.select_last_duration() + 1,)
    assert not np.isnan(select).any()
    pipeline, held = data.wop_deferred_init(), data.wop_pipeline_count()
    assert pipeline.shape == (len(_committed()), data.wop_pipeline_max() + 1) == (14, 7)
    for i in range(pipeline.shape[0]):
        assert np.isnan(pipeline[i, 0]) and np.isnan(pipeline[i, held[i] + 1:]).all(), i
        assert not np.isnan(pipeline[i, 1:held[i] + 1]).any(), i
    extract, moved = _extract()
    young = extract.index[extract["policy_id"] == "TA-000007-M4"][0]
    anchor = extract.index[extract["policy_id"] == "TA-000001"][0]
    cut = {MORT: _dropped(lambda t: t["age"] < 20)}
    model = mx.read_model(_sec_inputs(tmp_path, _set("age_at_entry", [anchor], 18)(extract),
                                      moved, cut), name=_name("padded"))
    try:
        p, q = _point(model, young), _point(model, anchor)
        position = list(extract.index).index(young)
        assert p.point_id() == young != point_keys(model)[position] + 1
        for lag in (0, 5):
            _refused(lambda: p.wop_deferred_init(lag),
                     f"point_id {young}: wop_pipeline_sec.csv holds no lag {lag}")
        assert p.wop_deferred_init(4) == pytest.approx(
            _committed_pipeline().iloc[-1]["wop_deferred_init"], rel=1e-15)
        _refused(lambda: q.mort_rate_base(0, 1),
                 f"point_id {anchor}: mort_table.csv has no rate at attained age 18")
    finally:
        model.close()
    model = mx.read_model(_sec_inputs(tmp_path / "select", extract, moved),
                          name=_name("padded_select"))
    try:
        model.Projection.select_period = -1
        _refused(lambda: _point(model, young).select_factor(0),
                 f"point_id {young}: select_factor_table.csv has no factor at duration -1")
    finally:
        model.close()


# Data's readers, each a DataFrame or a path, which only the label accessors, the reports
# and Data's own cells read.  Every other Data cell is a vector or an int in the Data
# docstring's table of its vectors.
READERS = ("input_dir", "model_point_table", "wop_pipeline", "mort_table",
           "select_factor_table", "lapse_table")


def _vector_kinds():
    """The Data docstring's table of its vectors, as {cell: "int64", "float64" or "int"}.

    The table's first two columns, by the widths its rules give: every cell a row names,
    one to a row, and the dtype beside it.
    """
    source = (model_path(SEC) / "Data" / "__init__.py").read_text(encoding="utf-8")
    lines = ast.get_docstring(ast.parse(source)).splitlines()
    head = next(i for i, line in enumerate(lines) if line.split()[:2] == ["Cells", "dtype"])
    widths = [len(rule) for rule in lines[head - 1].split()]
    first, dtype = widths[0], slice(widths[0] + 2, widths[0] + 2 + widths[1])
    kinds = {}
    for line in lines[head + 2:]:
        if line.startswith("="):
            break
        for name in re.findall(r"(\w+)\(\)", line[:first]):
            assert name not in kinds, name
            kinds[name] = line[dtype].strip()
    return kinds


def test_each_data_vector_is_the_int64_or_float64_its_docstring_states(sec_model):
    """Every ``Data`` cell but the readers is the int64 or float64 array, or the int, that
    the Data docstring's table of its vectors states.

    That is what compiles to a typed memoryview or a C ``long long`` (the Data docstring):
    an array of bools, objects or text compiles as a Python object, and so does a check
    returned as a numpy int.  The typing guard, C3, finds that in the compiled model's
    declarations; this finds it in seconds, in every run, naming the cell.  And each
    vector is of R5's kind, int64 for ages, months, terms, codes, flags and rows, float64
    for counts, amounts, rates and shares, as the table states it: a month held as a
    float64 reads the same numbers, and compiled reads a double through ``int()``, Python
    arithmetic, which neither C3 nor C5 sees.  Every cell is in the table, and every cell
    the table names is a cell.
    """
    data = sec_model.Data
    kinds = _vector_kinds()
    vectors = {name for name, cells in data.cells.items()
               if not cells.parameters and name not in READERS}
    assert set(kinds) == vectors, set(kinds) ^ vectors
    assert set(kinds.values()) == {"int64", "float64", "int"}, set(kinds.values())
    found = []
    for name, kind in kinds.items():
        value = data.cells[name]()
        if kind == "int":
            if type(value) is not int:
                found.append(f"{name}: {type(value).__name__}, not an int")
        elif not (isinstance(value, np.ndarray) and value.dtype == np.dtype(kind)):
            found.append(f"{name}: {getattr(value, 'dtype', type(value).__name__)}, not "
                         f"{kind}")
    assert not found, found
    assert set(READERS) < set(data.cells)


def test_every_parameterless_cell_returns_a_python_number(sec_model):
    """Every parameterless cell but the reporting ones returns a Python int, float or bool.

    R11: a ``Projection`` cell that reads a ``Data`` vector converts the element, ``int()``,
    ``float()`` or ``bool()``, so that modelx returns a Python number, as the compiled cell
    does, and not a numpy scalar, whose arithmetic and printing differ, and which C4
    compares as a kind of its own.  A conversion left out moves no number and still
    compiles, so it is asserted here: on every committed point, each parameterless cell
    outside :func:`uk_sec_support.reporting_cells` returns exactly an ``int``, a ``float``
    or a ``bool``, and so does each cell of a life at each life the point has.
    """
    space = sec_model.Projection
    reporting = reporting_cells(SEC, space)
    names = sorted(name for name, cell in space.cells.items()
                   if not cell.parameters and name not in reporting)
    assert {"point_id", "is_joint", "is_fib", "prem_cycle", "is_select_basis",
            "policy_term", "duration_mth_init"} <= set(names)
    found = []
    for key in point_keys(sec_model):
        proj = projection(sec_model, key)
        found += [f"{key}: {name} {type(value).__name__}" for name in names
                  if type(value := proj.cells[name]()) not in (int, float, bool)]
        for life in ((1, 2) if proj.is_joint() else (1,)):
            found += [f"{key}: {name}({life}) {type(value).__name__}"
                      for name in ("age_at_entry", "mort_group")
                      if type(value := proj.cells[name](life)) is not int]
    assert not found, found


def _references(space):
    """The References a space's ``__init__.py`` assigns, a name to a literal value."""
    source = (model_path(SEC) / space / "__init__.py").read_text(encoding="utf-8")
    return {node.targets[0].id: node.value.value for node in ast.parse(source).body
            if isinstance(node, ast.Assign) and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name)
            and isinstance(node.value, ast.Constant)}


def _comment(file):
    """``file`` beside the model, and its comment lines joined into one line."""
    source = (model_path(SEC).parent / file).read_text(encoding="utf-8")
    return source, " ".join(line.lstrip("# ") for line in source.splitlines()
                            if line.startswith("#"))


# The lives, 1 and 2, index every per-life cache from 0, which the cells refuse.
LIVES = 2


def test_the_spec_sizes_each_cache_as_its_comment_derives():
    """``spec_sec.py`` gives each cache the size its comment derives from the contract.

    The spec check, C3, holds the compiled caches to the spec, and C4 at the contract's
    extremes holds the spec to the largest argument a projection reads; neither sees a
    size above the comment's.  So this reads the spec as mx2cy does, and the bounds of the
    contract from the model's own References, and holds each size to the comment's
    derivation from them: ``t`` to ``12 * policy_term_max + future_horizon_mth + 2``,
    ``k`` to ``12 * policy_term_max`` and ``m`` to ``12 * policy_term_max_fib + 1``; every
    2-D cache to one inner width, the widest of the timings', the kinds' and the lives',
    since gcc refuses two widths and MSVC, which builds the Windows leg, accepts them
    (USLIB-SEC-PLAN.md §7.2, *Record -- M15*), and ``life`` alone to the same width, so
    that a life inside one per-life cache is inside every one; and the codes dense from 0,
    ints, as the caches index them.  A change to a bound or a size is derived again in the
    comment and here.
    """
    source, comment = _comment("spec_sec.py")
    for formula in ("12 * policy_term_max + future_horizon_mth + 2",
                    "12 * policy_term_max", "12 * policy_term_max_fib + 1"):
        assert formula in comment, formula
    sizes = ast.literal_eval(source)["spaces"]["Projection"]["cells_param_size"]
    proj, data = _references("Projection"), _references("Data")
    for names in (TIMINGS, KINDS):
        values = [proj[name] for name in names]
        assert values == list(range(len(names))), (names, values)
        assert all(type(v) is int for v in values), (names, values)
    t = 12 * proj["policy_term_max"] + data["future_horizon_mth"] + 2
    width = max(len(TIMINGS), len(KINDS), LIVES + 1)
    assert sizes == {"t": t, ("t", "timing"): (t, width), ("t", "kind"): (t, width),
                     ("t", "life"): (t, width), "life": width,
                     "k": 12 * proj["policy_term_max"],
                     "m": 12 * proj["policy_term_max_fib"] + 1}, sizes
    assert len({size[1] for size in sizes.values() if isinstance(size, tuple)}) == 1
    assert (t, width) == (722, 4)


def test_the_sample_raises_the_recursion_limit_its_comment_derives():
    """``sample_sec.py`` sets the recursion limit its comment derives, before the import.

    The export does not raise the recursion limit as modelx does (F7), so the sample sets
    it, and its comment records the measured need: a cold ``net_cf`` in the last month of
    the longest cover, the waiver point on the select basis issued at 18 on a 50-year term,
    needs the limit the comment states in the export, and the reports and checks the
    sample runs in ascending ``t`` less, from a script's top level (measured at M2).  The
    limit is four times the first, rounded up to the thousand.  No build can tell a
    lower limit above the reports' need: a limit of 1,000 builds the same model.  So this
    holds the limit, read from the sample's code, to the value derived from its comment's
    need, and holds the call before the import of the export.  A change to the need is
    measured again and written in the comment.
    """
    source, comment = _comment("sample_sec.py")
    need = re.search(r"needs a limit of ([\d,]+) in the export", comment)
    reports = re.search(r"ascending t, need ([\d,]+)", comment)
    assert need and reports, comment
    need, reports = (int(m.group(1).replace(",", "")) for m in (need, reports))
    tree = ast.parse(source)
    calls = [(node.lineno, node.args[0].value) for node in ast.walk(tree)
             if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
             and node.func.attr == "setrecursionlimit"
             and isinstance(node.args[0], ast.Constant)]
    imports = [node.lineno for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)
               and node.module == f"{SEC}_nomx"]
    assert len(calls) == 1 and len(imports) == 1, (calls, imports)
    (line, limit), = calls
    assert reports < need and line < imports[0], (reports, need, line, imports)
    assert limit == -(-4 * need // 1000) * 1000, (limit, need)


def test_the_sample_traces_each_life_label_on_a_copy_whose_second_life_is_blank():
    """``sample_sec.py`` calls ``sex`` and ``smoker`` of each life on a second instance of
    the export, whose table's one point is a single life with its second life blank, after
    the committed points.

    ``sex(life)`` and ``smoker(life)`` return each life's column as read, so mx2cy must see
    each return something other than text, or it compiles to ``str`` and raises
    ``TypeError`` on a blank or a number (the sample's docstring).  The committed table's
    single-life points give a blank second life today, so dropping the trace changes no
    declaration and no compile test fails; a table regenerated with no single life would.
    A second build in every session to show it would cost a compile, so this holds the
    trace in the sample's code: a frame whose ``joint_first_death`` is set to ``False`` and
    ``joint_sex`` and ``joint_smoker`` to ``None``; then a second ``_c_Term_UK_SEC()``
    instance, its ``Data.model_point_file`` set, a ``Projection`` of it, and each label of
    each life called on that, in order.
    """
    source, _ = _comment("sample_sec.py")
    lines = [(node.lineno, ast.unparse(node)) for node in ast.walk(ast.parse(source))
             if isinstance(node, (ast.Assign, ast.Expr))]

    def first(pattern, after=0):
        found = [(line, re.fullmatch(pattern, text)) for line, text in lines
                 if line > after and re.fullmatch(pattern, text)]
        assert found, pattern
        return min(found, key=lambda f: f[0])

    blank, _ = first(r"(\w+) = \1\.assign\(joint_first_death=False, joint_sex=None, "
                     r"joint_smoker=None\)")
    made, match = first(rf"(\w+) = _c_{SEC}\(\)", blank)
    second = match.group(1)
    read, _ = first(rf"{second}\.Data\.model_point_file = .+", made)
    proj, match = first(rf"(\w+) = {second}\.Projection\[\d+\]", read)
    p = match.group(1)
    first(rf"\({p}\.sex\(1\), {p}\.sex\(2\), {p}\.smoker\(1\), {p}\.smoker\(2\)\)", proj)


def test_run_sec_rebuilds_in_place_exactly_when_a_source_is_newer(tmp_path):
    """``run_sec.py --cython`` rebuilds its package where, and only where, it is stale.

    ``compiled_model`` builds in place when no build for this interpreter is there, or
    when the model, ``sample_sec.py``, ``spec_sec.py`` or the tool is newer than it, and
    otherwise imports what is there.  So its three functions are read from the runner,
    which runs the model when imported, and run here on a fake product in a fake library:
    empty sources, the library's tool at its root, where ``_tool`` finds it, and an empty
    file standing for the extension module, their times set by ``os.utime``, with the build
    and the import stubbed, so that nothing is built or imported.  Built after every
    source, it must not build; with any one source newer than the build, or no build, it
    must, and say so on stderr.
    """
    tree = ast.parse((model_path(SEC).parent / "run_sec.py").read_text(encoding="utf-8"))
    found = [node for node in tree.body if isinstance(node, ast.FunctionDef)
             and node.name in ("_built", "_tool", "compiled_model")]
    assert len(found) == 3
    here = tmp_path / "products" / "product"
    tool = tmp_path / "build_sec_cy.py"
    sources = [here / SEC / "Projection" / "__init__.py",
               here / SEC / "Data" / "__init__.py", here / SEC / "__init__.py",
               here / "sample_sec.py", here / "spec_sec.py", tool]
    for path in sources:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("", encoding="utf-8")
    suffix = importlib.machinery.EXTENSION_SUFFIXES[0]
    built = here / f"{SEC}_nomx_cy" / f"_mx_classes{suffix}"
    built.parent.mkdir()
    builds = []

    class Imported(Exception):
        """Raised by the stubbed import, once the runner has decided."""

    def run(args, **kwargs):
        builds.append(args)
        return types.SimpleNamespace(returncode=0)

    def import_module(name):
        raise Imported(name)

    stub = types.SimpleNamespace(path=[], modules={}, executable=sys.executable,
                                 exit=sys.exit, stderr=None)
    space = {"HERE": here, "NAME": SEC, "SUFFIXES": (suffix,), "Path": pathlib.Path,
             "sys": stub, "subprocess": types.SimpleNamespace(run=run, DEVNULL=None),
             "importlib": types.SimpleNamespace(import_module=import_module)}
    exec(compile(ast.Module(found, []), "run_sec.py", "exec"), space)

    def rebuilt(newer=None):
        base = 1_000_000_000
        for path in sources:
            os.utime(path, (base, base))
        if built.exists():
            os.utime(built, (base + 10, base + 10))
        if newer is not None:
            os.utime(newer, (base + 20, base + 20))
        builds.clear()
        said = []
        stub.stderr = types.SimpleNamespace(write=said.append, flush=lambda: None)
        with pytest.raises(Imported):
            space["compiled_model"](None)
        assert ("building" in "".join(said)) == bool(builds)
        return builds == [[sys.executable, str(tool), str(here)]]

    built.write_bytes(b"")
    assert not rebuilt(), "built after every source, the runner rebuilt"
    for source in sources:
        assert rebuilt(source), f"{source.name} newer than the build, the runner did not"
    built.unlink()
    assert rebuilt(), "with no build, the runner did not build"


# What the C step's Data cannot hold, or a cell cannot take, as (case, the table's edit,
# the call, its arguments, the message): a point_id that is not a whole number below 2**53,
# which Data.point_id refuses when a refusal first names a point, here a point past its
# cover; a timing, a kind and a life no cell takes, each refused by the cell, as
# Term_UK_S's are, ValueError and its message.
NOT_HELD = [
    ("a label with a fraction",
     lambda t: _set("duration_mth", [13], 300)(t).rename(index={13: 13.5}),
     "result_cf", (), "model_point_table_sec.csv: point_id must be a whole number; [13.5] "
     "is not"),
    ("a label of 2**53", lambda t: _set("duration_mth", [13], 300)(t).rename(
        index={13: 2 ** 53}), "result_cf", (),
     f"model_point_table_sec.csv: point_id must be below 2**53 in size; [{2 ** 53}] is "
     f"not"),
    ("a timing no cell takes", None, "pols_if_at", (0, 9), "invalid timing"),
    ("a kind no cell takes", None, "claims", (0, 9), "invalid kind"),
    ("a third life", None, "age_at_entry", (3,), "invalid life"),
    ("a life of 0", None, "mort_group", (0,), "invalid life"),
    ("a second life on a single life", None, "mort_group", (2,), "invalid life"),
    ("a second life's issue age on a single life", None, "age_at_entry", (2,),
     "invalid life"),
    ("a label of a third life", None, "sex", (3,), "invalid life"),
]


@pytest.mark.parametrize("case, edit, cell, args, message", NOT_HELD,
                         ids=[c[0] for c in NOT_HELD])
def test_what_the_c_step_cannot_hold_or_take_is_refused(tmp_path, case, edit, cell, args,
                                                        message):
    """A label the vectors cannot hold, and a code or a life no cell takes, are refused.

    ``Data.point_id`` reads each label by value, and refuses one that is not a whole
    number, or is ``2**53`` or more in size, naming every such label, when a refusal first
    names a point: here the anchor cell in its last covered month, the table's thirteenth
    row, moved past its cover, a refusal of ``proj_len()``'s, which meets the label's own
    first.  A projection that names no point reads no label, and runs.  And a timing, a
    kind or a life no cell takes is refused by the cell, as ``Term_UK_S``'s are
    (:data:`NOT_HELD`), on point 1, a single life: compiled, a code past a cache raises
    ``IndexError`` instead, which the compiled refusal test holds.
    """
    model = _read_edited(tmp_path, edit or (lambda t: t))
    try:
        keys = point_keys(model)
        p = projection(model, keys[12] if edit is not None else keys[0])
        _refused(lambda: p.cells[cell](*args), message)
        if edit is not None:
            assert len(projection(model, keys[0]).result_cf()) == 300
    finally:
        model.close()


# ---------------------------------------------------------------------------
# C2 -- the Phase 1 fingerprint


def test_the_phase_1_fingerprint_is_reproduced(sec_model):
    """Every committed point computes what the model computed when its E step ended (C2).

    The C step changes how the model is represented and no number it computes
    (UKLIB-SEC-PLAN.md U2, after USLIB-SEC-PLAN.md D2), so before it changed anything the
    model as M1 committed it was frozen below (USLIB-SEC-PLAN.md §5.4): for each point,
    each column of ``result_cf()`` and ``result_pols()``, its sum, its largest absolute
    value and its values at five fixed months, the frame's first and last and the three
    quartiles between.  Every later version must reproduce it, to 1e-12 relative, floored
    at 1e-12 of the column's own magnitude (``uk_sec_support.fingerprint_mismatches``),
    with the same points, frames and columns exactly.  ``python
    tools/gen_sec_fingerprint.py Term_UK_SEC --check`` runs the same comparison from the
    command line.  The block was refrozen once, in a commit of its own, when the
    repository's owner had the waiver's incidence taken from the active lives in both
    models, a change of numbers, not of representation: it moved the waiver points, 7, 11,
    12 and 14, and every other point's entry is what M1 froze.
    """
    assert fingerprint_mismatches(FINGERPRINT, sec_model) == []


# Term_UK_SEC's fingerprint, frozen from the model as M1 committed it and committed alone,
# before its C step changed anything, and refrozen alone once since, when both models'
# waiver came to take its incidence from the active lives, which moved the waiver points
# 7, 11, 12 and 14 and nothing else.  Each point is keyed by its point_id; each column
# holds (its sum over the frame, its largest absolute value, (its values at the months)).
# The block is written by tools/gen_sec_fingerprint.py, and is never edited by hand: a
# refreeze goes through the tool's --force, in a commit of its own that says why.
# BEGIN generated fingerprint: Term_UK_SEC -- tools/gen_sec_fingerprint.py
FINGERPRINT = {
    1: {"rows": 300, "months": (0, 74, 149, 224, 299),
        "result_cf": {
            "pols_if": (160.12456876563874, 1.0, (
                1.0, 0.6528654928282186, 0.5021194526158201, 0.3841493158437434,
                0.29125316916401034)),
            "premiums": (1921.4948251876651, 12.0, (
                12.0, 7.834385913938624, 6.025433431389842, 4.609791790124921,
                3.495038029968124)),
            "claims_death": (3053.8494010853346, 16.455767279400153, (
                6.8767336821429215, 7.490946669693048, 9.665023337054887,
                12.406858680238193, 15.788468349477215)),
            "claims_fib": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claim_expenses": (5.089749001808892, 0.027426278799000257, (
                0.011461222803571536, 0.01248491111615508, 0.016108372228424813,
                0.020678097800396988, 0.026314113915795356)),
            "expenses": (694.5288592895467, 152.5, (
                152.5, 1.9488888525901795, 1.7897556901606244, 1.6349712393626974,
                1.4801443144112882)),
            "commissions": (260.6063576567361, 216.0, (
                216.0, 0.1958596478484656, 0.15063583578474604, 0.11524479475312302,
                0.08737595074920311)),
            "net_cf": (-2092.5795418457615, 363.3881949049465, (
                -363.3881949049465, -1.8137941673092244, -5.59608980383884,
                -9.56796102202949, -13.887264698585378)),
        },
        "result_pols": {
            "pols_if": (160.12456876563874, 1.0, (
                1.0, 0.6528654928282186, 0.5021194526158201, 0.3841493158437434,
                0.29125316916401034)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.020358996007235567, 0.00010970511519600102, (
                4.584489121428614e-05, 4.993964446462032e-05, 6.443348891369925e-05,
                8.271239120158795e-05, 0.00010525645566318143)),
            "pols_lapse": (0.6894818450847287, 0.008741210196493465, (
                0.008741210196493465, 0.0022169963476928235, 0.0017050055537385469,
                0.0013043106172524062, 0.0009887538003113525)),
            "pols_maturity": (0.29015915890803584, 0.29015915890803584, (
                0.0, 0.0, 0.0, 0.0, 0.29015915890803584)),
            "pols_payer": (160.12456876563874, 1.0, (
                1.0, 0.6528654928282186, 0.5021194526158201, 0.3841493158437434,
                0.29125316916401034)),
            "fib_cum": (2.527500317933801, 0.020253739551572385, (
                0.0, 0.0033105927464806674, 0.007515783902592429, 0.013041992043293078,
                0.020253739551572385)),
            "mort_rate_mth": (0.04639939834534479, 0.0003613916235325476, (
                4.584489121428614e-05, 7.649300661960456e-05, 0.00012832302866983003,
                0.00021531312901057476, 0.0003613916235325476)),
            "lapse_rate_mth": (1.1882963668422937, 0.008741610954696721, (
                0.008741610954696721, 0.003396053198917559, 0.003396053198917559,
                0.003396053198917559, 0.003396053198917559)),
        },
    },
    2: {"rows": 300, "months": (0, 74, 149, 224, 299),
        "result_cf": {
            "pols_if": (160.12456876563874, 1.0, (
                1.0, 0.6528654928282186, 0.5021194526158201, 0.3841493158437434,
                0.29125316916401034)),
            "premiums": (1921.4948251876651, 12.0, (
                12.0, 7.834385913938624, 6.025433431389842, 4.609791790124921,
                3.495038029968124)),
            "claims_death": (1633.5814856868278, 6.8767336821429215, (
                6.8767336821429215, 6.507067875312671, 6.547995817455893, 4.991847317694081,
                0.09971156004918703)),
            "claims_fib": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claim_expenses": (5.089749001808892, 0.027426278799000257, (
                0.011461222803571536, 0.01248491111615508, 0.016108372228424813,
                0.020678097800396988, 0.026314113915795356)),
            "expenses": (694.5288592895467, 152.5, (
                152.5, 1.9488888525901795, 1.7897556901606244, 1.6349712393626974,
                1.4801443144112882)),
            "commissions": (260.6063576567361, 216.0, (
                216.0, 0.1958596478484656, 0.15063583578474604, 0.11524479475312302,
                0.08737595074920311)),
            "net_cf": (-672.3116264472545, 363.3881949049465, (
                -363.3881949049465, -0.829915372928848, -2.479062284239847,
                -2.1529496594853774, 1.8014920908426504)),
        },
        "result_pols": {
            "pols_if": (160.12456876563874, 1.0, (
                1.0, 0.6528654928282186, 0.5021194526158201, 0.3841493158437434,
                0.29125316916401034)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.020358996007235567, 0.00010970511519600102, (
                4.584489121428614e-05, 4.993964446462032e-05, 6.443348891369925e-05,
                8.271239120158795e-05, 0.00010525645566318143)),
            "pols_lapse": (0.6894818450847287, 0.008741210196493465, (
                0.008741210196493465, 0.0022169963476928235, 0.0017050055537385469,
                0.0013043106172524062, 0.0009887538003113525)),
            "pols_maturity": (0.29015915890803584, 0.29015915890803584, (
                0.0, 0.0, 0.0, 0.0, 0.29015915890803584)),
            "pols_payer": (160.12456876563874, 1.0, (
                1.0, 0.6528654928282186, 0.5021194526158201, 0.3841493158437434,
                0.29125316916401034)),
            "fib_cum": (2.527500317933801, 0.020253739551572385, (
                0.0, 0.0033105927464806674, 0.007515783902592429, 0.013041992043293078,
                0.020253739551572385)),
            "mort_rate_mth": (0.04639939834534479, 0.0003613916235325476, (
                4.584489121428614e-05, 7.649300661960456e-05, 0.00012832302866983003,
                0.00021531312901057476, 0.0003613916235325476)),
            "lapse_rate_mth": (1.1882963668422937, 0.008741610954696721, (
                0.008741610954696721, 0.003396053198917559, 0.003396053198917559,
                0.003396053198917559, 0.003396053198917559)),
        },
    },
    3: {"rows": 300, "months": (0, 74, 149, 224, 299),
        "result_cf": {
            "pols_if": (160.12456876563874, 1.0, (
                1.0, 0.6528654928282186, 0.5021194526158201, 0.3841493158437434,
                0.29125316916401034)),
            "premiums": (1921.4948251876651, 12.0, (
                12.0, 7.834385913938624, 6.025433431389842, 4.609791790124921,
                3.495038029968124)),
            "claims_death": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_fib": (2547.8593139410364, 20.358996007235568, (
                0.04584489121428614, 3.3605323909452878, 7.580217391506128,
                13.124704434494666, 20.358996007235568)),
            "claims_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claim_expenses": (5.089749001808892, 0.027426278799000257, (
                0.011461222803571536, 0.01248491111615508, 0.016108372228424813,
                0.020678097800396988, 0.026314113915795356)),
            "expenses": (694.5288592895467, 152.5, (
                152.5, 1.9488888525901795, 1.7897556901606244, 1.6349712393626974,
                1.4801443144112882)),
            "commissions": (260.6063576567361, 216.0, (
                216.0, 0.1958596478484656, 0.15063583578474604, 0.11524479475312302,
                0.08737595074920311)),
            "net_cf": (-1586.5894547014632, 356.5573061140178, (
                -356.5573061140178, 2.316620111438536, -3.511283858290082,
                -10.28580677628596, -18.457792356343727)),
        },
        "result_pols": {
            "pols_if": (160.12456876563874, 1.0, (
                1.0, 0.6528654928282186, 0.5021194526158201, 0.3841493158437434,
                0.29125316916401034)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.020358996007235567, 0.00010970511519600102, (
                4.584489121428614e-05, 4.993964446462032e-05, 6.443348891369925e-05,
                8.271239120158795e-05, 0.00010525645566318143)),
            "pols_lapse": (0.6894818450847287, 0.008741210196493465, (
                0.008741210196493465, 0.0022169963476928235, 0.0017050055537385469,
                0.0013043106172524062, 0.0009887538003113525)),
            "pols_maturity": (0.29015915890803584, 0.29015915890803584, (
                0.0, 0.0, 0.0, 0.0, 0.29015915890803584)),
            "pols_payer": (160.12456876563874, 1.0, (
                1.0, 0.6528654928282186, 0.5021194526158201, 0.3841493158437434,
                0.29125316916401034)),
            "fib_cum": (2.527500317933801, 0.020253739551572385, (
                0.0, 0.0033105927464806674, 0.007515783902592429, 0.013041992043293078,
                0.020253739551572385)),
            "mort_rate_mth": (0.04639939834534479, 0.0003613916235325476, (
                4.584489121428614e-05, 7.649300661960456e-05, 0.00012832302866983003,
                0.00021531312901057476, 0.0003613916235325476)),
            "lapse_rate_mth": (1.1882963668422937, 0.008741610954696721, (
                0.008741610954696721, 0.003396053198917559, 0.003396053198917559,
                0.003396053198917559, 0.003396053198917559)),
        },
    },
    4: {"rows": 300, "months": (0, 74, 149, 224, 299),
        "result_cf": {
            "pols_if": (160.12456876563874, 1.0, (
                1.0, 0.6528654928282186, 0.5021194526158201, 0.3841493158437434,
                0.29125316916401034)),
            "premiums": (1921.4948251876651, 12.0, (
                12.0, 7.834385913938624, 6.025433431389842, 4.609791790124921,
                3.495038029968124)),
            "claims_death": (2059.8966541494483, 9.71066349557447, (
                9.71066349557447, 8.644274001193704, 8.114964568227446, 5.725744389512138,
                0.10499750349414165)),
            "claims_fib": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claim_expenses": (5.089749001808892, 0.027426278799000257, (
                0.011461222803571536, 0.01248491111615508, 0.016108372228424813,
                0.020678097800396988, 0.026314113915795356)),
            "expenses": (694.5288592895467, 152.5, (
                152.5, 1.9488888525901795, 1.7897556901606244, 1.6349712393626974,
                1.4801443144112882)),
            "commissions": (260.6063576567361, 216.0, (
                216.0, 0.1958596478484656, 0.15063583578474604, 0.11524479475312302,
                0.08737595074920311)),
            "net_cf": (-1098.6267949098751, 366.22212471837804, (
                -366.22212471837804, -2.9671214988098806, -4.046031035011399,
                -2.8868467313034345, 1.796206147397696)),
        },
        "result_pols": {
            "pols_if": (160.12456876563874, 1.0, (
                1.0, 0.6528654928282186, 0.5021194526158201, 0.3841493158437434,
                0.29125316916401034)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.020358996007235567, 0.00010970511519600102, (
                4.584489121428614e-05, 4.993964446462032e-05, 6.443348891369925e-05,
                8.271239120158795e-05, 0.00010525645566318143)),
            "pols_lapse": (0.6894818450847287, 0.008741210196493465, (
                0.008741210196493465, 0.0022169963476928235, 0.0017050055537385469,
                0.0013043106172524062, 0.0009887538003113525)),
            "pols_maturity": (0.29015915890803584, 0.29015915890803584, (
                0.0, 0.0, 0.0, 0.0, 0.29015915890803584)),
            "pols_payer": (160.12456876563874, 1.0, (
                1.0, 0.6528654928282186, 0.5021194526158201, 0.3841493158437434,
                0.29125316916401034)),
            "fib_cum": (2.527500317933801, 0.020253739551572385, (
                0.0, 0.0033105927464806674, 0.007515783902592429, 0.013041992043293078,
                0.020253739551572385)),
            "mort_rate_mth": (0.04639939834534479, 0.0003613916235325476, (
                4.584489121428614e-05, 7.649300661960456e-05, 0.00012832302866983003,
                0.00021531312901057476, 0.0003613916235325476)),
            "lapse_rate_mth": (1.1882963668422937, 0.008741610954696721, (
                0.008741610954696721, 0.003396053198917559, 0.003396053198917559,
                0.003396053198917559, 0.003396053198917559)),
        },
    },
    5: {"rows": 300, "months": (0, 74, 149, 224, 299),
        "result_cf": {
            "pols_if": (160.12456876563874, 1.0, (
                1.0, 0.6528654928282186, 0.5021194526158201, 0.3841493158437434,
                0.29125316916401034)),
            "premiums": (3088.917504339328, 12.0, (
                12.0, 10.202408378389327, 10.2184206806728, 10.180627285844741,
                10.051777724568158)),
            "claims_death": (4734.334289007431, 33.45118674284859, (
                6.8767336821429215, 8.944582074123248, 13.780012244428395,
                21.121846403368785, 32.094705410853905)),
            "claims_fib": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claim_expenses": (5.089749001808892, 0.027426278799000257, (
                0.011461222803571536, 0.01248491111615508, 0.016108372228424813,
                0.020678097800396988, 0.026314113915795356)),
            "expenses": (694.5288592895467, 152.5, (
                152.5, 1.9488888525901795, 1.7897556901606244, 1.6349712393626974,
                1.4801443144112882)),
            "commissions": (289.79192463552766, 216.0, (
                216.0, 0.2550602094597332, 0.25546051701682, 0.2545156821461185,
                0.25129444311420396)),
            "net_cf": (-2634.8273175949867, 363.3881949049465, (
                -363.3881949049465, -0.9586076688999892, -5.622916143161464,
                -12.851384136833257, -23.800680557727034)),
        },
        "result_pols": {
            "pols_if": (160.12456876563874, 1.0, (
                1.0, 0.6528654928282186, 0.5021194526158201, 0.3841493158437434,
                0.29125316916401034)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.020358996007235567, 0.00010970511519600102, (
                4.584489121428614e-05, 4.993964446462032e-05, 6.443348891369925e-05,
                8.271239120158795e-05, 0.00010525645566318143)),
            "pols_lapse": (0.6894818450847287, 0.008741210196493465, (
                0.008741210196493465, 0.0022169963476928235, 0.0017050055537385469,
                0.0013043106172524062, 0.0009887538003113525)),
            "pols_maturity": (0.29015915890803584, 0.29015915890803584, (
                0.0, 0.0, 0.0, 0.0, 0.29015915890803584)),
            "pols_payer": (160.12456876563874, 1.0, (
                1.0, 0.6528654928282186, 0.5021194526158201, 0.3841493158437434,
                0.29125316916401034)),
            "fib_cum": (2.527500317933801, 0.020253739551572385, (
                0.0, 0.0033105927464806674, 0.007515783902592429, 0.013041992043293078,
                0.020253739551572385)),
            "mort_rate_mth": (0.04639939834534479, 0.0003613916235325476, (
                4.584489121428614e-05, 7.649300661960456e-05, 0.00012832302866983003,
                0.00021531312901057476, 0.0003613916235325476)),
            "lapse_rate_mth": (1.1882963668422937, 0.008741610954696721, (
                0.008741610954696721, 0.003396053198917559, 0.003396053198917559,
                0.003396053198917559, 0.003396053198917559)),
        },
    },
    6: {"rows": 300, "months": (0, 74, 149, 224, 299),
        "result_cf": {
            "pols_if": (159.0412663370283, 1.0, (
                1.0, 0.6512198445965378, 0.49867669629000416, 0.3786794325542268,
                0.28346119658644936)),
            "premiums": (2862.7427940665093, 18.0, (
                18.0, 11.72195720273768, 8.976180533220075, 6.816229785976082,
                5.102301538556088)),
            "claims_death": (4798.1446072713225, 25.499991945993052, (
                10.927774689323266, 11.87335528572333, 15.251758127540565,
                19.430896481943666, 24.408744609877182)),
            "claims_fib": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claim_expenses": (7.996907678785537, 0.04249998657665509, (
                0.018212957815538777, 0.01978892547620555, 0.025419596879234275,
                0.03238482746990611, 0.04068124101646197)),
            "expenses": (690.0624897419748, 152.5, (
                152.5, 1.9439763774643863, 1.777484321879898, 1.6116909639797057,
                1.4405456245778707)),
            "commissions": (390.422800198606, 324.0, (
                324.0, 0.293048930068442, 0.2244045133305019, 0.17040574464940206,
                0.12755753846390222)),
            "net_cf": (-3023.8840108241793, 469.4459876471388, (
                -469.4459876471388, -2.4082123159946827, -8.302886026410123,
                -14.429148232066598, -20.91522747537933)),
        },
        "result_pols": {
            "pols_if": (159.0412663370283, 1.0, (
                1.0, 0.6512198445965378, 0.49867669629000416, 0.3786794325542268,
                0.28346119658644936)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.03198763071514214, 0.00016999994630662035, (
                7.285183126215511e-05, 7.91557019048222e-05, 0.0001016783875169371,
                0.00012953930987962445, 0.00016272496406584787)),
            "pols_lapse": (0.6856759943432755, 0.00874097411233049, (
                0.00874097411233049, 0.0022113084194660014, 0.001693187284448121,
                0.0012855755759023657, 0.0009620966808016509)),
            "pols_maturity": (0.28233637494158187, 0.28233637494158187, (
                0.0, 0.0, 0.0, 0.0, 0.28233637494158187)),
            "pols_payer": (159.0412663370283, 1.0, (
                1.0, 0.6512198445965378, 0.49867669629000416, 0.3786794325542268,
                0.28346119658644936)),
            "fib_cum": (3.9927136122933815, 0.0318249057510763, (
                0.0, 0.00525795639491979, 0.011909421223099162, 0.02059894441993458,
                0.0318249057510763)),
            "mort_rate_mth": (0.07372237953909311, 0.0005740643376428434, (
                7.285183126215511e-05, 0.00012154989219326229, 0.000203896408782267,
                0.0003420817154126121, 0.0005740643376428434)),
            "lapse_rate_mth": (1.1882963668422937, 0.008741610954696721, (
                0.008741610954696721, 0.003396053198917559, 0.003396053198917559,
                0.003396053198917559, 0.003396053198917559)),
        },
    },
    7: {"rows": 240, "months": (0, 59, 119, 179, 239),
        "result_cf": {
            "pols_if": (138.86775858706818, 1.0, (
                1.0, 0.6866074457977287, 0.5512628091872224, 0.44010277487172395,
                0.3473753645169931)),
            "premiums": (6522.067710636864, 47.25, (
                47.25, 32.23275870134066, 25.853434107747827, 20.637867663590477,
                16.289366045205462)),
            "claims_death": (9226.454271450863, 58.40227298470121, (
                17.147217116514348, 28.116104053974514, 37.3689360571512, 45.93971750362349,
                55.860463308531884)),
            "claims_fib": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claim_expenses": (9.226454271450862, 0.05840227298470121, (
                0.017147217116514346, 0.028116104053974512, 0.037368936057151206,
                0.045939717503623495, 0.05586046330853189)),
            "expenses": (594.6304283332261, 152.5, (
                152.5, 1.9319568231423532, 1.7981823266746642, 1.6642373378779804,
                1.52281201092603)),
            "commissions": (1000.0479151058863, 850.5, (
                850.5, 0.8058189675335165, 0.6463358526936958, 0.5159466915897619,
                0.40723415113013656)),
            "net_cf": (-4308.2913585245615, 972.9143643336308, (
                -972.9143643336308, 1.3507627526363, -13.997389064828887,
                -27.527973587004382, -41.55700388869112)),
        },
        "result_pols": {
            "pols_if": (138.86775858706818, 1.0, (
                1.0, 0.6866074457977287, 0.5512628091872224, 0.44010277487172395,
                0.3473753645169931)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.03690581708580345, 0.00023360909193880484, (
                6.858886846605738e-05, 0.00011246441621589805, 0.0001494757442286048,
                0.00018375887001449397, 0.00022344185323412753)),
            "pols_lapse": (0.6171212066479099, 0.008741011377492768, (
                0.008741011377492768, 0.003530652498227175, 0.0018716101990051983,
                0.0014939883815572703, 0.0011789463974726396)),
            "pols_maturity": (0.3459729762662863, 0.3459729762662863, (
                0.0, 0.0, 0.0, 0.0, 0.3459729762662863)),
            "pols_payer": (138.03317906109763, 1.0, (
                1.0, 0.682174787329961, 0.5471626266190016, 0.43678026801249686,
                0.3447484877292161)),
            "fib_cum": (3.645754440488071, 0.0366823752325693, (
                0.0, 0.0052799025264447415, 0.01366292281687826, 0.024017795091234848,
                0.0366823752325693)),
            "mort_rate_mth": (0.0745682778645893, 0.0006432288413567022, (
                6.858886846605738e-05, 0.00016379725693949077, 0.0002711515120147334,
                0.00041753626767759844, 0.0006432288413567022)),
            "lapse_rate_mth": (0.9845331749072401, 0.008741610954696721, (
                0.008741610954696721, 0.005143012831822946, 0.003396053198917559,
                0.003396053198917559, 0.003396053198917559)),
        },
    },
    8: {"rows": 240, "months": (0, 59, 119, 179, 239),
        "result_cf": {
            "pols_if": (162.21589287194422, 1.0, (
                1.0, 0.8141184570630633, 0.6587156918755797, 0.530767291547224,
                0.4249435190694798)),
            "premiums": (1946.590714463331, 12.0, (
                12.0, 9.769421484756759, 7.904588302506956, 6.369207498566688,
                5.099322228833758)),
            "claims_death": (3876.9953802131854, 24.00925516713926, (
                10.526186738762933, 12.098590050066631, 15.066176070854347,
                18.686944338154085, 23.035654239923012)),
            "claims_fib": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claim_expenses": (6.461658967021976, 0.04001542527856543, (
                0.017543644564604888, 0.020164316750111055, 0.02511029345142391,
                0.031144907230256806, 0.03839275706653835)),
            "expenses": (522.5199654535809, 2.5, (
                2.5, 2.2907437395202117, 2.14868642631696, 2.0070828787087716,
                1.862852582260544)),
            "commissions": (48.66476786158327, 0.30000000000000004, (
                0.30000000000000004, 0.244235537118919, 0.1976147075626739,
                0.1592301874641672, 0.12748305572084395)),
            "net_cf": (-2508.051058032041, 20.808882818163823, (
                -1.3437303833275376, -4.884312158699115, -9.532999195678448,
                -14.515194812990593, -19.965060406137184)),
        },
        "result_pols": {
            "pols_if": (162.21589287194422, 1.0, (
                1.0, 0.8141184570630633, 0.6587156918755797, 0.530767291547224,
                0.4249435190694798)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.025846635868087903, 0.00016006170111426172, (
                7.017457825841955e-05, 8.065726700044421e-05, 0.00010044117380569565,
                0.00012457962892102722, 0.0001535710282661534)),
            "pols_lapse": (0.5508060253526132, 0.003395814882316582, (
                0.003395814882316582, 0.002764515674037231, 0.0022366924290016495,
                0.0018020908792924417, 0.0014426092619133873)),
            "pols_maturity": (0.4233473387793003, 0.4233473387793003, (
                0.0, 0.0, 0.0, 0.0, 0.4233473387793003)),
            "pols_payer": (162.21589287194422, 1.0, (
                1.0, 0.8141184570630633, 0.6587156918755797, 0.530767291547224,
                0.4249435190694798)),
            "fib_cum": (2.6488242511696303, 0.025693064839821745, (
                0.0, 0.004443322527518053, 0.010064704564429617, 0.01705180309666621,
                0.025693064839821745)),
            "mort_rate_mth": (0.04311762720101475, 0.0003613916235325476, (
                7.017457825841955e-05, 9.907313401469331e-05, 0.00015248031137637952,
                0.00023471610045500135, 0.0003613916235325476)),
            "lapse_rate_mth": (0.8150527677402142, 0.003396053198917559, (
                0.003396053198917559, 0.003396053198917559, 0.003396053198917559,
                0.003396053198917559, 0.003396053198917559)),
        },
    },
    9: {"rows": 240, "months": (0, 59, 119, 179, 239),
        "result_cf": {
            "pols_if": (111.18158241636488, 0.6853926606570752, (
                0.6853926606570752, 0.5579908153764863, 0.45147890067116947,
                0.36378400614330064, 0.29125316916401034)),
            "premiums": (2450.4721631841035, 10.491200467607765, (
                10.249487446930374, 9.950729269521407, 10.033368687789576,
                10.074752033998108, 10.051777724568158)),
            "claims_death": (4312.945791227702, 33.45118674284858, (
                8.363665274524875, 10.819550871831053, 15.619374356956701,
                22.458720532007703, 32.0947054108539)),
            "claims_fib": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claim_expenses": (4.428773631665836, 0.027426278799000257, (
                0.01202428522575658, 0.013820474707690655, 0.01721041083855136,
                0.021346490832463445, 0.026314113915795356)),
            "expenses": (358.1313493686726, 1.7134816516426878, (
                1.7134816516426878, 1.5700589465132972, 1.472693906651123,
                1.3756398743974636, 1.276785487767453)),
            "commissions": (61.261804079602584, 0.26228001169019416, (
                0.25623718617325936, 0.2487682317380352, 0.2508342171947394,
                0.2518688008499527, 0.25129444311420396)),
            "net_cf": (-2286.295555123539, 24.594661510449473, (
                -0.09592095063620493, -2.701469255268669, -7.32674420385154,
                -14.032823664089477, -23.59732173108319)),
        },
        "result_pols": {
            "pols_if": (111.18158241636488, 0.6853926606570752, (
                0.6853926606570752, 0.5579908153764863, 0.45147890067116947,
                0.36378400614330064, 0.29125316916401034)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.017715094526663342, 0.00010970511519600102, (
                4.809714090302632e-05, 5.528189883076262e-05, 6.884164335420544e-05,
                8.538596332985378e-05, 0.00010525645566318143)),
            "pols_lapse": (0.37751840722237584, 0.0023274665972898546, (
                0.0023274665972898546, 0.001894778753256567, 0.0015330125749849763,
                0.0012351398625040921, 0.0009887538003113525)),
            "pols_maturity": (0.29015915890803584, 0.29015915890803584, (
                0.0, 0.0, 0.0, 0.0, 0.29015915890803584)),
            "pols_payer": (111.18158241636488, 0.6853926606570752, (
                0.6853926606570752, 0.5579908153764863, 0.45147890067116947,
                0.36378400614330064, 0.29125316916401034)),
            "fib_cum": (2.4500210564594718, 0.020253739551572385, (
                0.0026439014805722224, 0.005689322129865343, 0.00954217612071405,
                0.014331082173996838, 0.020253739551572385)),
            "mort_rate_mth": (0.04311762720101475, 0.0003613916235325476, (
                7.017457825841955e-05, 9.907313401469331e-05, 0.00015248031137637952,
                0.00023471610045500135, 0.0003613916235325476)),
            "lapse_rate_mth": (0.8150527677402142, 0.003396053198917559, (
                0.003396053198917559, 0.003396053198917559, 0.003396053198917559,
                0.003396053198917559, 0.003396053198917559)),
        },
    },
    10: {"rows": 234, "months": (0, 58, 116, 174, 233),
        "result_cf": {
            "pols_if": (107.10469566239227, 0.6712622141358484, (
                0.6712622141358484, 0.5482888555643142, 0.44667809504478767,
                0.3624634803174667, 0.29125316916401034)),
            "premiums": (1285.2563479487073, 8.055146569630182, (
                8.055146569630182, 6.57946626677177, 5.360137140537452, 4.349561763809601,
                3.495038029968124)),
            "claims_death": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_fib": (2450.868516609343, 20.358996007235568, (
                2.9771008319173835, 6.042755425704586, 9.834550051266552, 14.50921188918323,
                20.358996007235568)),
            "claims_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claim_expenses": (4.357250179523994, 0.027426278799000257, (
                0.011776385694449018, 0.014803107743037048, 0.01856126549731116,
                0.02318593796413457, 0.026314113915795356)),
            "expenses": (342.96455408989584, 1.678155535339621, (
                1.678155535339621, 1.5427598434061331, 1.4570340005459241,
                1.3706463399085582, 1.276785487767453)),
            "commissions": (32.131408698717685, 0.20137866424075457, (
                0.20137866424075457, 0.16448665666929427, 0.1340034285134363,
                0.10873904409524003, 0.08737595074920311)),
            "net_cf": (-1545.0653816287725, 18.25443352969989, (
                3.1867351524379743, -1.1853387667512802, -6.084011605285772,
                -11.662221447341564, -18.25443352969989)),
        },
        "result_pols": {
            "pols_if": (107.10469566239227, 0.6712622141358484, (
                0.6712622141358484, 0.5482888555643142, 0.44667809504478767,
                0.3624634803174667, 0.29125316916401034)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.01742900071809598, 0.00010970511519600102, (
                4.7105542777796074e-05, 5.921243097214819e-05, 7.424506198924465e-05,
                9.274375185653828e-05, 0.00010525645566318143)),
            "pols_lapse": (0.3636740545097163, 0.0022794822166992946, (
                0.0022794822166992946, 0.0018618170333044178, 0.0015166904333829803,
                0.0012306302991077526, 0.0009887538003113525)),
            "pols_maturity": (0.29015915890803584, 0.29015915890803584, (
                0.0, 0.0, 0.0, 0.0, 0.29015915890803584)),
            "pols_payer": (107.10469566239227, 0.6712622141358484, (
                0.6712622141358484, 0.5482888555643142, 0.44667809504478767,
                0.3624634803174667, 0.29125316916401034)),
            "fib_cum": (2.4334395158912465, 0.020253739551572385, (
                0.002929995289139587, 0.005983542994732438, 0.009760304989277309,
                0.014416468137326692, 0.020253739551572385)),
            "mort_rate_mth": (0.042696579731464235, 0.0003613916235325476, (
                7.017457825841955e-05, 0.00010799495625568589, 0.00016621603524524797,
                0.0002558706101241093, 0.0003613916235325476)),
            "lapse_rate_mth": (0.7946764485467088, 0.003396053198917559, (
                0.003396053198917559, 0.003396053198917559, 0.003396053198917559,
                0.003396053198917559, 0.003396053198917559)),
        },
    },
    11: {"rows": 174, "months": (0, 43, 86, 129, 173),
        "result_cf": {
            "pols_if": (85.92116224426312, 0.6683951102894978, (
                0.6683951102894978, 0.5718872603601463, 0.48757973073518013,
                0.4137278312934453, 0.3473753645169931)),
            "premiums": (4029.761726658099, 31.369941360695286, (
                31.369941360695286, 26.82217734983913, 22.8647657944357, 19.400936671155282,
                16.289366045205462)),
            "claims_death": (7683.417326206032, 58.40227298470121, (
                32.084137005617066, 38.76702383715429, 42.82220625142874, 51.33217429515286,
                55.860463308531884)),
            "claims_fib": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claim_expenses": (7.683417326206033, 0.05840227298470121, (
                0.03208413700561706, 0.038767023837154295, 0.04282220625142874,
                0.051332174295152855, 0.05586046330853189)),
            "expenses": (258.2292757701908, 1.6709877757237446, (
                1.6709877757237446, 1.562291625878904, 1.4991539203552333,
                1.3900390226644572, 1.313591017590507)),
            "commissions": (100.74404316645247, 0.7842485340173821, (
                0.7842485340173821, 0.6705544337459783, 0.5716191448608926,
                0.48502341677888205, 0.40723415113013656)),
            "net_cf": (-4020.312335810784, 43.189210214533794, (
                -3.201516091668524, -14.216459570777198, -22.071035728460593,
                -33.85763223773607, -41.34778289535559)),
        },
        "result_pols": {
            "pols_if": (85.92116224426312, 0.6683951102894978, (
                0.6683951102894978, 0.5718872603601463, 0.48757973073518013,
                0.4137278312934453, 0.3473753645169931)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.030733669304824136, 0.00023360909193880484, (
                0.00012833654802246825, 0.00015506809534861717, 0.00017128882500571497,
                0.00020532869718061143, 0.00022344185323412753)),
            "pols_lapse": (0.2916884647183873, 0.002269469514695054, (
                0.002269469514695054, 0.001941632940465015, 0.0016552649983284711,
                0.0014043444177664394, 0.0011789463974726396)),
            "pols_maturity": (0.3459729762662863, 0.3459729762662863, (
                0.0, 0.0, 0.0, 0.0, 0.3459729762662863)),
            "pols_payer": (85.28596246895447, 0.6639141028718579, (
                0.6639141028718579, 0.5676651290971244, 0.4839103871838244,
                0.41060183431016467, 0.3447484877292161)),
            "fib_cum": (3.470314979947844, 0.0366823752325693, (
                0.006172147780979315, 0.012137576901381633, 0.01910595983798021,
                0.02716719938712139, 0.0366823752325693)),
            "mort_rate_mth": (0.06658552680971641, 0.0006432288413567022, (
                0.00019200701209032278, 0.0002711515120147334, 0.00035130423643214836,
                0.0004962893033777505, 0.0006432288413567022)),
            "lapse_rate_mth": (0.5909132566116553, 0.003396053198917559, (
                0.003396053198917559, 0.003396053198917559, 0.003396053198917559,
                0.003396053198917559, 0.003396053198917559)),
        },
    },
    12: {"rows": 236, "months": (0, 58, 117, 176, 235),
        "result_cf": {
            "pols_if": (134.9203064360227, 0.9652245245592393, (
                0.9652245245592393, 0.6780729746984693, 0.5472146673321123,
                0.4384250276201522, 0.3473753645169931)),
            "premiums": (6335.550596499965, 45.60685878542406, (
                45.60685878542406, 31.828451399225038, 25.663354453381338,
                20.559182022845405, 16.289366045205462)),
            "claims_death": (9158.766452359832, 58.40227298470121, (
                16.550914488801613, 32.54869146276253, 40.438493213857285,
                49.89370847039523, 55.860463308531884)),
            "claims_fib": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claim_expenses": (9.158766452359835, 0.05840227298470121, (
                0.01655091448880161, 0.03254869146276253, 0.040438493213857285,
                0.04989370847039523, 0.05586046330853189)),
            "expenses": (430.6536515165461, 2.4130613113980983, (
                2.4130613113980983, 1.907942767115086, 1.7849775593324533,
                1.6578929797439022, 1.52281201092603)),
            "commissions": (149.54791510588615, 1.0606799792345656, (
                0.0, 0.795711284980626, 0.6415838613345335, 0.5139795505711352,
                0.40723415113013656)),
            "net_cf": (-3412.576188934661, 43.40158025583458, (
                26.626332070735547, -3.456442807095963, -17.24213867435679,
                -31.55629268633526, -41.55700388869112)),
        },
        "result_pols": {
            "pols_if": (134.9203064360227, 0.9652245245592393, (
                0.9652245245592393, 0.6780729746984693, 0.5472146673321123,
                0.4384250276201522, 0.3473753645169931)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.03663506580943934, 0.00023360909193880484, (
                6.620365795520645e-05, 0.00013019476585105012, 0.00016175397285542913,
                0.00019957483388158092, 0.00022344185323412753)),
            "pols_lapse": (0.5826164824835132, 0.008437038551007359, (
                0.008437038551007359, 0.002302329746473231, 0.0018578207963908745,
                0.00148823695078191, 0.0011789463974726396)),
            "pols_maturity": (0.3459729762662863, 0.3459729762662863, (
                0.0, 0.0, 0.0, 0.0, 0.3459729762662863)),
            "pols_payer": (134.0857269100522, 0.9652245245592393, (
                0.9652245245592393, 0.6736180190312178, 0.5431397767911395,
                0.4351149634464636, 0.3447484877292161)),
            "fib_cum": (3.645345318916208, 0.0366823752325693, (
                0.0002707512763641122, 0.005654164392001955, 0.013974751721751878,
                0.02420155396124934, 0.0366823752325693)),
            "mort_rate_mth": (0.07429392239072508, 0.0006432288413567022, (
                6.858886846605738e-05, 0.00019200701209032278, 0.0002955950973391186,
                0.0004552085791381666, 0.0006432288413567022)),
            "lapse_rate_mth": (0.9495667310884532, 0.008741610954696721, (
                0.008741610954696721, 0.003396053198917559, 0.003396053198917559,
                0.003396053198917559, 0.003396053198917559)),
        },
    },
    13: {"rows": 1, "months": (0,),
        "result_cf": {
            "pols_if": (0.29125316916401034, 0.29125316916401034, (
                0.29125316916401034,)),
            "premiums": (3.495038029968124, 3.495038029968124, (
                3.495038029968124,)),
            "claims_death": (15.788468349477215, 15.788468349477215, (
                15.788468349477215,)),
            "claims_fib": (0.0, 0.0, (
                0.0,)),
            "claims_lapse": (0.0, 0.0, (
                0.0,)),
            "claim_expenses": (0.026314113915795356, 0.026314113915795356, (
                0.026314113915795356,)),
            "expenses": (0.7281329229100258, 0.7281329229100258, (
                0.7281329229100258,)),
            "commissions": (0.08737595074920311, 0.08737595074920311, (
                0.08737595074920311,)),
            "net_cf": (-13.135253307084117, 13.135253307084117, (
                -13.135253307084117,)),
        },
        "result_pols": {
            "pols_if": (0.29125316916401034, 0.29125316916401034, (
                0.29125316916401034,)),
            "pols_new_biz": (0.0, 0.0, (
                0.0,)),
            "pols_death": (0.00010525645566318143, 0.00010525645566318143, (
                0.00010525645566318143,)),
            "pols_lapse": (0.0009887538003113525, 0.0009887538003113525, (
                0.0009887538003113525,)),
            "pols_maturity": (0.29015915890803584, 0.29015915890803584, (
                0.29015915890803584,)),
            "pols_payer": (0.29125316916401034, 0.29125316916401034, (
                0.29125316916401034,)),
            "fib_cum": (0.020253739551572385, 0.020253739551572385, (
                0.020253739551572385,)),
            "mort_rate_mth": (0.0003613916235325476, 0.0003613916235325476, (
                0.0003613916235325476,)),
            "lapse_rate_mth": (0.003396053198917559, 0.003396053198917559, (
                0.003396053198917559,)),
        },
    },
    14: {"rows": 253, "months": (0, 63, 126, 189, 252),
        "result_cf": {
            "pols_if": (138.86775858706818, 1.0, (
                0.0, 0.7202825562481763, 0.563546466194915, 0.44517463701076254,
                0.3473753645169931)),
            "premiums": (6522.067710636864, 47.25, (
                0.0, 33.82817713853215, 26.430334343601356, 20.875738541279407,
                16.289366045205462)),
            "claims_death": (9226.454271450863, 58.40227298470121, (
                0.0, 29.495076733703936, 38.20161909982776, 46.46913910055087,
                55.860463308531884)),
            "claims_fib": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claim_expenses": (9.226454271450862, 0.05840227298470121, (
                0.0, 0.029495076733703936, 0.03820161909982776, 0.046469139100550866,
                0.05586046330853189)),
            "expenses": (609.0858685028079, 152.575, (
                0.0, 2.0875122340726056, 1.8933983161021124, 1.7339189478996027,
                1.6155512623914252)),
            "commissions": (1000.0479151058862, 850.5, (
                0.0, 0.8457044284633037, 0.660758358590034, 0.5218934635319852,
                0.40723415113013656)),
            "net_cf": (-4322.746798694144, 972.9893643336309, (
                0.0, 1.3703886655585988, -14.363643050018378, -27.8956821098036,
                -41.64974314015652)),
        },
        "result_pols": {
            "pols_if": (138.86775858706818, 1.0, (
                0.0, 0.7202825562481763, 0.563546466194915, 0.44517463701076254,
                0.3473753645169931)),
            "pols_new_biz": (1.0, 1.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.036905817085803455, 0.00023360909193880484, (
                0.0, 0.00011798030693481574, 0.00015280647639931105, 0.00018587655640220347,
                0.00022344185323412753)),
            "pols_lapse": (0.6171212066479099, 0.008741011377492768, (
                0.0, 0.003703815655090136, 0.001913314840336936, 0.0015112055034233898,
                0.0011789463974726396)),
            "pols_maturity": (0.3459729762662863, 0.3459729762662863, (
                0.0, 0.0, 0.0, 0.0, 0.3459729762662863)),
            "pols_payer": (138.03317906109763, 1.0, (
                0.0, 0.7159402569001513, 0.5593721554201345, 0.44181457230220966,
                0.3447484877292161)),
            "fib_cum": (3.645754440488072, 0.0366823752325693, (
                0.0, 0.004240338953065868, 0.012754446470674021, 0.02346228850067663,
                0.0366823752325693)),
            "mort_rate_mth": (0.0745682778645893, 0.0006432288413567022, (
                0.0, 0.00016379725693949077, 0.0002711515120147334, 0.00041753626767759844,
                0.0006432288413567022)),
            "lapse_rate_mth": (0.9845331749072401, 0.008741610954696721, (
                0.0, 0.005143012831822946, 0.003396053198917559, 0.003396053198917559,
                0.003396053198917559)),
        },
    },
}
# END generated fingerprint: Term_UK_SEC


# ---------------------------------------------------------------------------
# Compiled (UKLIB-SEC-PLAN.md U2, the C step, after USLIB-SEC-PLAN.md's Phase 2)
#
# These compile the model, once a session, into a temporary directory (conftest.sec_build),
# and run the compiled package in a child process only.  They skip without modelx-cython or
# a C compiler, and the cython_uk CI job, which sets UKLIB_REQUIRE_CYTHON=1, fails a skip.
# test_compiled_conventions_uk.py checks the compiled model's types, its caches and its
# release, and compares it with modelx on the committed points; these hold what is Term's
# own: the comparison on the splice grid, at the contract's extremes, where the cap on
# mortality binds and on keys written as floats; each life's label that is not text; the
# refusals; the deepest calls on a 1 MiB stack; a Reference set late; and the runner.
#
# Every C4 comparison here passes the model's also, _term_c4_also, the spec's c4_also, which
# the conventions' C4 passes on the committed points: every cell of a code at every code it
# takes, in every month of the frame and the month after it, the count at AFT_DECR, which
# no swept cell reads, among them (UKLIB-SEC-PLAN.md, M15).
# test_the_c4_comparisons_ask_every_code_on_every_row, which needs no compiler, holds it to
# the codes each cell takes in modelx, row by row.


def _as_modelx(have, want):
    """Whether a compiled value is modelx's: identical where ``exact_here()``, as on
    x86-64, and to 1e-12 relative elsewhere, as C4 compares (uk_sec_support)."""
    return have == want if exact_here() else have == pytest.approx(want, rel=1e-12, abs=0)


def _mismatch_lines(found):
    return f"{len(found)} mismatches, first:\n  " + "\n  ".join(found[:50])


# The cells C4 asks at every code, each with the names of the codes it takes, read from the
# model's own References (_code), and the cells of a life it asks at both lives
# (uk_sec_support._LIVES), as (those of a life alone, those of a month and a life): the
# harness's, which its _term_c4_also, the spec's c4_also, asks in every month of every
# row.  What each takes is derived in modelx, row by row, and these must name exactly
# that (test_the_c4_comparisons_ask_every_code_on_every_row).
CODED = _TERM_CODED
CELLS_OF_A_LIFE = _TERM_LIVES

# The shapes of the cells of a life the also asks, by their parameters: of a life alone,
# at each life, and of a month and a life, at each life in every month.  A cell of a life
# of any other shape is asked by no also, and fails the codes test until one asks it.
LIFE_SHAPES = (("life",), ("t", "life"))


def _coded_cells(proj):
    """``{cell: its parameters}`` for every cell of ``proj`` that takes a code or a life:
    each of a month and one more parameter, a timing, a kind or a life, and each with a life
    among its parameters, whatever its shape, read from the space, so that such a cell
    added later, under whatever name, is held with the others."""
    return {name: tuple(cells.parameters) for name, cells in proj.cells.items()
            if (len(cells.parameters) == 2 and cells.parameters[0] == "t")
            or "life" in cells.parameters}


def _inner_width():
    """The one inner width ``spec_sec.py`` gives the caches of ``t`` and a code or a life,
    and those of a life alone."""
    source, _ = _comment("spec_sec.py")
    sizes = ast.literal_eval(source)["spaces"]["Projection"]["cells_param_size"]
    (width,) = {size[1] for size in sizes.values() if isinstance(size, tuple)}
    assert sizes.get("life", width) == width, sizes
    return width


def _codes_taken(proj, width):
    """``({cell: codes}, lines)``: the codes or lives each cell of :func:`_coded_cells`
    takes on point ``proj``, in modelx, and a line for each other raise.

    Each such cell is asked every argument of the caches' inner width, ``width``, in the
    point's first month on the books where it takes a month, and the arguments it takes
    are those it does not refuse by its parameter's name, ``invalid timing``, ``invalid
    kind`` or ``invalid life``.  A refused call caches nothing.  A cell of a life of a shape
    no also asks (:data:`LIFE_SHAPES`) is asked nothing, and left out.
    """
    taken, lines, t = {}, [], proj.t_entry()
    for cell, parameters in sorted(_coded_cells(proj).items()):
        if "life" in parameters and parameters not in LIFE_SHAPES:
            continue
        taken[cell] = set()
        for code in range(width):
            args = (t, code) if len(parameters) == 2 else (code,)
            try:
                proj.cells[cell](*args)
            except Exception as err:            # a code or a life the cell does not take
                if _raised(err) != f"ValueError: invalid {parameters[-1]}":
                    lines.append(f"{cell}{args} raised {_raised(err)}")
                continue
            taken[cell].add(code)
    return taken, lines


class _Asked:
    """A stand-in for a point, which records what :func:`_term_c4_also` asks of each
    cell of a code or of a life, the arguments of each call, over the point's frame; its
    References are the point's own."""

    def __init__(self, proj):
        self.refs, self.months, self.asked = proj.refs, proj.proj_len(), {}
        self.cells = {name: self._cell(name) for name in _coded_cells(proj)}

    def _cell(self, name):
        return lambda *args: self.asked.setdefault(name, set()).add(args)

    def proj_len(self):
        return self.months


def test_the_c4_comparisons_ask_every_code_on_every_row(spliced):
    """C4's ``also`` asks every code its cells take, and every cell of a life at both
    lives, in every month of every row.

    Nothing in a comparison shows what it leaves out: dropped from :func:`_term_c4_also`, a
    code or a life is simply not compared.  So the cells of a code or of a life are read
    from the model, each of a month and one more parameter, a timing, a kind or a life, and
    each with a life among its parameters (:func:`_coded_cells`), one of a shape no also
    asks, neither of a life alone nor of a month and a life (:data:`LIFE_SHAPES`), failing
    here until one asks it; and what each takes is derived in modelx, not read from
    :data:`CODED` or :data:`CELLS_OF_A_LIFE`: on a fresh read of the committed model, and on
    every row of the splice grid this run selects, the twins, the rows restated in force and
    the future rows among them, each such cell is asked every argument in the caches' one
    inner width, 0 to 3, in the row's first month on the books, and the arguments it takes
    are those it does not refuse, ``invalid timing``, ``invalid kind`` or ``invalid life``
    (:func:`_codes_taken`).  :data:`CELLS_OF_A_LIFE` must name exactly the cells of a life
    of those shapes, each taking no life there but 1 and 2, and :data:`CODED` every other,
    with exactly the codes each takes, by the model's own References, row by row.  Then
    :func:`_term_c4_also` is run on a stand-in of each of those rows (:class:`_Asked`), one
    at a time: it must ask each cell of a code at every code the cell takes on the row, and
    each cell of a life at both lives, in every month of the frame and the month after it,
    and no other, so that a code or a life left out on one kind of row fails here, where a
    union over the rows would pass it.  A single life's second life is asked too: refused
    where a cell reads it, it computes elsewhere, each rate 0 outside cover, and the
    ``also`` passes over that refusal alone, at life 2 on a point that is a single life by
    its own ``is_joint()``
    (:func:`test_c4_compares_every_cell_of_a_life_at_every_life_it_takes`).  And it must be
    the spec's ``c4_also``, which the conventions' C4 on the committed points passes
    (``uk_sec_support.spec_c4_also``).  Needs no compiler.
    """
    width, found, rows = _inner_width(), [], 0
    alone, monthly = CELLS_OF_A_LIFE
    named_lives = {**dict.fromkeys(alone, ("life",)),
                   **dict.fromkeys(monthly, ("t", "life"))}
    fresh = mx.read_model(model_path(SEC), name=_name("codes"))
    try:
        for name, model in (("committed", fresh), ("spliced", spliced[1])):
            for key, label in zip(point_keys(model), model.Data.model_point_table().index):
                p = projection(model, key)
                where = f"{name} row {label}"
                taken, lines = _codes_taken(p, width)
                found += [f"{where}: {line}" for line in lines]
                cells = _coded_cells(p)
                odd = {cell: parameters for cell, parameters in cells.items()
                       if "life" in parameters and parameters not in LIFE_SHAPES}
                if odd:
                    found.append(f"{where}: no also asks these cells of a life: {odd}")
                of_a_life = {cell: parameters for cell, parameters in cells.items()
                             if parameters in LIFE_SHAPES}
                lives = {cell: taken.pop(cell) for cell in of_a_life}
                if of_a_life != named_lives or not all(
                        took <= set(_LIVES) for took in lives.values()):
                    found.append(f"{where}: the cells of a life are {of_a_life}, taking "
                                 f"{lives} in modelx, CELLS_OF_A_LIFE names "
                                 f"{CELLS_OF_A_LIFE}")
                named = {cell: {_code(p, n) for n in names}
                         for cell, names in CODED.items()}
                if named != taken:
                    found.append(f"{where}: the cells of a code take {taken} in modelx, "
                                 f"CODED names {named}")
                stand_in = _Asked(p)
                _term_c4_also(stand_in)
                months = range(p.proj_len() + 1)
                want = {cell: {(t, code) for t in months for code in codes}
                        for cell, codes in taken.items()}
                want.update({cell: ({(life,) for life in _LIVES} if parameters == ("life",)
                                    else {(t, life) for t in months for life in _LIVES})
                             for cell, parameters in of_a_life.items()})
                if stand_in.asked != want:
                    apart = {cell: sorted(stand_in.asked.get(cell, set())
                                          ^ want.get(cell, set()))[:4]
                             for cell in {*want, *stand_in.asked}
                             if stand_in.asked.get(cell) != want.get(cell)}
                    found.append(f"{where}: asked or missed {apart}")
                rows += 1
                if name != "committed":
                    _release(model, key)
    finally:
        fresh.close()
    assert rows > len(_committed()) and not found, (rows, found[:10])
    assert SPEC.c4_also is _term_c4_also, SPEC.c4_also


def _lives_taken(width):
    """The lives the model has: each life some cell of a life alone takes, in modelx, on
    some committed row (:func:`_codes_taken`), on a read of its own."""
    model = mx.read_model(model_path(SEC), name=_name("lives_taken"))
    try:
        found = set()
        for key in point_keys(model):
            p = projection(model, key)
            taken, _ = _codes_taken(p, width)
            found.update(life for cell, parameters in _coded_cells(p).items()
                         if parameters == ("life",) for life in taken[cell])
        return sorted(found)
    finally:
        model.close()


def test_c4_compares_every_cell_of_a_life_at_every_life_it_takes():
    """C4 compares every call of a cell of a life that computes, on every committed row.

    The ``also`` asks each cell of a life at both lives
    (:func:`test_the_c4_comparisons_ask_every_code_on_every_row`), and passes over a single
    life's second life where a cell refuses it, ``invalid life``.  So each committed row is
    swept and asked as C4 asks it, on a fresh read (``uk_sec_support.c4_expected``, with
    :func:`_term_c4_also`), which must not raise, and then every cell with a life among its
    parameters, read from the model (:func:`_coded_cells`), is asked every life the model
    has, those its cells of a life alone take on some committed row, derived on a read of
    its own (:func:`_lives_taken`), alone or in every month of the frame and the month after
    it: each call not cached must be refused, ``invalid life``, and only at life 2 on a row
    that is a single life by its own ``is_joint()``, as the ``also`` passes over that
    refusal and no other.  A cell of a life of a shape no also asks (:data:`LIFE_SHAPES`)
    fails.  So C4 leaves no call of a life that computes uncompared, each life's labels and
    a single life's rates outside cover, 0, among them, and a refusal of a joint row's
    second life, or of a first life, fails here and in C4.  Needs no compiler.
    """
    lives = _lives_taken(_inner_width())
    assert lives, "no cell of a life takes a life"
    fresh = mx.read_model(model_path(SEC), name=_name("lives"))
    found = []
    try:
        for key, label in zip(point_keys(fresh), fresh.Data.model_point_table().index):
            p = projection(fresh, key)
            try:
                c4_expected(p, _term_c4_also)
            except Exception as err:                    # the also may not raise
                found.append(f"row {label}: C4's also raised {_raised(err)}")
                continue
            joint = p.is_joint()
            for cell, parameters in _coded_cells(p).items():
                if "life" not in parameters:
                    continue
                if parameters not in LIFE_SHAPES:
                    found.append(f"row {label}: no also asks {cell}{parameters}")
                    continue
                cells = p.cells[cell]
                cached = {k if isinstance(k, tuple) else (k,) for k in cells.keys()}
                months = [None] if parameters == ("life",) else range(p.proj_len() + 1)
                for t in months:
                    for life in lives:
                        args = (life,) if t is None else (t, life)
                        if args in cached:
                            continue
                        try:
                            cells(*args)
                        except Exception as err:        # refused, as it must be
                            if (life != 2 or joint
                                    or _raised(err) != "ValueError: invalid life"):
                                found.append(f"row {label}: {cell}{args} raised "
                                             f"{_raised(err)}")
                            continue
                        found.append(f"row {label}: {cell}{args} computes, uncompared")
    finally:
        fresh.close()
    assert not found, (len(found), found[:10])


# How many rows of a grid C4 compares at once.  compiled_mismatches sweeps every row of its
# case in one modelx read and keeps every value of every row, in the parent and in the
# child, until it compares them.  A Term row runs at most 720 months, so twenty rows hold
# what uslib's SPIA's twenty did, below WholeLife's chunk (USLIB-SEC-PLAN.md §7.2,
# *Record -- M15*).
C4_CHUNK = 20


@pytest.mark.cython
def test_the_compiled_model_computes_what_modelx_computes_on_the_splice_grid(spliced,
                                                                             sec_build,
                                                                             tmp_path):
    """C4 on the branches: compiled, every cell of the splice grid is modelx's.

    The sample traces the committed points alone, and they leave branches untaken, which
    are typed all the same, because every branch of a cell returns the one type the
    others return (sample_sec.py).  What the compiled model computes on them is held
    here: the splice grid's rows, S's points and its five variants as twins, restated in
    force at T2's months and issued later, the annual payer, the part commutation, the
    indexed waiver point, the straight-line schedule and the smoking second life among
    them, under the splice's References, every switch that ships off on
    (:data:`SPLICED_REFS`).  The grid is the one this run's ``spliced`` selects, the core
    by default and the full grid under ``UKLIB_SEC_FULL=1``, and the test carries no
    ``sec_full`` mark, since a skipped compile test fails the cython_uk job.  The grid's
    SEC table goes beside the build :data:`C4_CHUNK` rows at a time, each chunk with its
    points' rows of the pipeline, modelx sweeps every point fully, and the compiled model
    must agree at every argument modelx caches, identically on x86-64 and to 1e-12 relative
    elsewhere, with every raise and every ``Data`` array
    (``uk_sec_support.compiled_mismatches``).
    """
    build = sec_build(SEC)
    folder = spliced[1].Data.input_dir()
    table = pd.read_csv(folder / TABLE, index_col="point_id")
    pipeline = pd.read_csv(folder / PIPELINE)
    found = []
    for start in range(0, len(table), C4_CHUNK):
        chunk = table.iloc[start:start + C4_CHUNK]
        rows = pipeline[pipeline["point_id"].isin(chunk.index)]
        case = compiled_case(build, tmp_path / f"chunk{start}", model_points=chunk,
                             edits={PIPELINE: rows})
        found += [f"rows {start} on: {line}"
                  for line in compiled_mismatches(build, case, refs=SPLICED_REFS,
                                                  also=_term_c4_also)]
    assert not found, _mismatch_lines(found)


# The contract's extremes (product-spec.md, held by proj_len()): each shape at its longest
# cover from its youngest issue age, as (the S point it changes, its changes): the waiver
# point on the select basis, a 50-year term from 18; the decreasing shape, the same,
# whose schedule runs 600 policy months; the family income benefit commuted in half, a
# 40-year term from 30, its commuted value read 480 months from the end; the joint point
# from 18 with its second life at 40, each covered to 90 or less; and the indexed point
# paying annually, a 50-year term from 18.
EXTREMES = {
    21: (7, {"age_at_entry": 18, "policy_term": 50}),
    22: (2, {"age_at_entry": 18, "policy_term": 50}),
    23: (3, {"age_at_entry": 30, "policy_term": 40, "fib_commute_rate": 0.5}),
    24: (6, {"age_at_entry": 18, "joint_age": 40, "policy_term": 50}),
    25: (5, {"age_at_entry": 18, "policy_term": 50, "premium_mode": "annual"}),
}


def _contract_extremes(tmp_path):
    """The rows at the contract's extremes, and their pipeline, built by the generator.

    Each of :data:`EXTREMES` in a copy of S's table, read with :data:`SWITCHED_ON` set, its
    twin issued at the valuation date, the same issued ``future_horizon_mth``, 120 months,
    after it, a frame of up to 720 months, and the same restated in force in its last
    covered month, opened with S's state there; so ``t`` reaches 721, the policy month
    599, the months left 480, and each life its last attained age, 89 or 69, the furthest
    ``spec_sec.py`` sizes for.  S's tables serve: the mortality table runs from 18 to 100.
    Returns ``(rows, pipeline)``.
    """
    s_table = _s_table()
    rows = []
    for point_id, (base, changes) in EXTREMES.items():
        row = s_table.loc[[base]].assign(**changes, policy_id=f"TA-7000{point_id}")
        row.index = pd.Index([point_id], name="point_id")
        rows.append(row)
    s = mx.read_model(temp_inputs(tmp_path / "s", model_path(TWIN),
                                  model_points=pd.concat(rows)), name=_name("extremes_s"))
    try:
        for ref, value in SWITCHED_ON.items():
            setattr(s.Projection, ref, value)
        last = {p: 12 * int(changes["policy_term"]) - 1
                for p, (_, changes) in EXTREMES.items()}
        spec = dataclasses.replace(SPEC, derived=tuple(last.items()),
                                   future=tuple((p, 120) for p in EXTREMES))
        table, companions = build_sec_table(spec, s)
    finally:
        s.close()
    return table, companions[PIPELINE]


@pytest.mark.cython
def test_the_compiled_model_computes_what_modelx_computes_at_the_contract_extremes(
        sec_build, tmp_path):
    """C4 where the caches end: the contract's longest covers, every cell compiled.

    The rows of :func:`_contract_extremes`, each shape at its longest cover from its
    youngest issue age, issued now and 120 months on and in force in its last month, with
    every switch that ships off on (:data:`SWITCHED_ON`), read every cache as far as
    ``spec_sec.py`` sizes it for: ``t`` to 721, the roll-forward's month after the month
    after the 720-month frame; ``k`` to 599, the decreasing schedule's last month; ``m`` to
    480, the family income benefit's commuted value in its issue month; each life to 2 at
    the last attained ages; and every timing and kind.  modelx sweeps every row fully, and
    the compiled model must agree everywhere.  A cache one too small for the contract
    raises ``IndexError`` compiled where modelx reads on, and fails here, though the spec
    check passes it, which holds the caches to the spec and not the spec to the contract.
    """
    build = sec_build(SEC)
    rows, pipeline = _contract_extremes(tmp_path / "rows")
    frames = {(row["policy_id"], int(row["duration_mth"])): row["policy_term"]
              for _, row in rows.iterrows()}
    assert max(12 * int(n) - d for (_, d), n in frames.items()) == 720
    folder = compiled_case(build, tmp_path / "extremes", model_points=rows,
                           edits={PIPELINE: pipeline})
    found = compiled_mismatches(build, folder, refs=SWITCHED_ON, also=_term_c4_also)
    assert not found, _mismatch_lines(found)


@pytest.mark.cython
def test_the_compiled_model_computes_what_modelx_computes_where_the_cap_binds(sec_build,
                                                                              tmp_path):
    """C4 where ``mort_rate_life`` caps the annual rate at 1: compiled, every cell is
    modelx's.

    The rows of the cap's test, :data:`CAPPED_POINT`'s twin, its row issued 12 months on and
    its rows restated in force the month before the cap and five months into the capped
    year, built by the generator from S on :data:`CAPPED`'s table under
    :data:`SPLICED_REFS`, go beside the build with that table.  modelx sweeps them fully,
    and the compiled model must agree at every argument modelx caches, identically on
    x86-64 and to 1e-12 relative elsewhere (``uk_sec_support.compiled_mismatches``, which
    reads ``exact_here()``).  No other compiled test reaches the side of ``min(..., 1.0)``
    that returns 1, where the monthly rate is exactly 1 and every policy in force dies.
    """
    build = sec_build(SEC)
    s = _capped_s(tmp_path / "s")
    try:
        spec = dataclasses.replace(
            SPEC, derived=((CAPPED_POINT, CAPPED_MTH - 1), (CAPPED_POINT, CAPPED_MTH + 5)),
            future=((CAPPED_POINT, 12),))
        rows, companions = build_sec_table(spec, s)
    finally:
        s.close()
    rows.loc[rows["source_mth"] == CAPPED_MTH + 5, "policy_count"] = 1.0
    folder = compiled_case(build, tmp_path / "capped", model_points=rows,
                           edits={**CAPPED, PIPELINE: companions[PIPELINE]})
    found = compiled_mismatches(build, folder, refs=SPLICED_REFS, also=_term_c4_also)
    assert not found, _mismatch_lines(found)


@pytest.mark.cython
def test_the_compiled_model_computes_what_modelx_computes_at_a_commutation_discount_of_0(
        sec_build, tmp_path):
    """C4 where the annuity certain is its limit: compiled, every cell is modelx's at a
    commutation discount of 0, and of 1e-17.

    ``annuity_certain_factor`` returns ``m`` where the monthly rate is 0, at a rate of 0,
    as ``Term_UK_S`` does, and at two whose monthly rate rounds to 0, where S divides by
    zero: 1e-17, where ``1 + r`` is 1, and :data:`PAST_ONE`, where it is not.  The shipped
    rate, 3%, takes the closed form on
    every point, so no other compiled test reaches the branch, and
    ``test_a_commutation_discount_outside_its_domain_is_refused`` holds it against S in
    modelx.  On the committed points, with the rate set in both engines before either
    computes, modelx sweeps every point fully, and the compiled model must agree at every
    argument modelx caches, the family income benefit's points 3, 4 and 10, whose
    commuted value reads the factor, among them (``uk_sec_support.compiled_mismatches``).
    """
    build = sec_build(SEC)
    folder = compiled_case(build, tmp_path / "discount")
    found = []
    for value in (0.0, 1e-17, PAST_ONE):
        found += [f"at {value}: {line}" for line in compiled_mismatches(
            build, folder, refs={"fib_commute_disc_rate": value}, also=_term_c4_also)]
    assert not found, _mismatch_lines(found)


# The model point table's columns that hold whole numbers, which a spreadsheet may save as
# floats: the months, the ages and the term.  And the assumption tables' keys.
FLOAT_COLUMNS = ("duration_mth", "age_at_entry", "policy_term", "joint_age")
FLOAT_KEYS = {MORT: lambda t: t.assign(age=t["age"].astype(float)),
              SELECT: lambda t: t.assign(duration=t["duration"].astype(float)),
              LAPSE: lambda t: t.assign(policy_year=t["policy_year"].astype(float))}


@pytest.mark.cython
def test_the_compiled_model_reads_keys_written_as_floats_as_modelx_does(sec_build,
                                                                         tmp_path):
    """C4 on keys written as floats: the compiled model reads 60.0 as 60, as modelx does.

    The committed table with its labels written ``1.0`` to ``14.0`` and its whole numbers
    as floats (:data:`FLOAT_COLUMNS`), the pipeline's labels and lags as floats, and the
    three assumption tables' keys as floats (:data:`FLOAT_KEYS`).  ``Data`` reads each by
    value, so first, in seconds, modelx's ``Data`` on the floats is held to its ``Data`` on
    the same rows as written: every array of the same dtype and values, and every check of
    the same type, so that a key read as a float fails here, naming its cell, and not in
    the compiled sweep.  Then modelx sweeps every point, and the compiled model must agree
    everywhere, every ``Data`` array included, in dtype and shape.
    """
    build = sec_build(SEC)
    rows = _committed()
    as_written = mx.read_model(_sec_inputs(tmp_path / "ints", rows), name=_name("ints"))
    floats = rows.assign(**{c: rows[c].astype(float) for c in FLOAT_COLUMNS})
    floats.index = pd.Index(rows.index.astype(float), name="point_id")
    pipeline = _committed_pipeline()
    pipeline = pipeline.assign(point_id=pipeline["point_id"].astype(float),
                               lag=pipeline["lag"].astype(float))
    folder = compiled_case(build, tmp_path / "floats", model_points=floats,
                           edits={**FLOAT_KEYS, PIPELINE: pipeline})
    written = pd.read_csv(folder.parent / TABLE)
    assert all(written[c].dtype == float for c in ("point_id", *FLOAT_COLUMNS))
    assert all(pd.read_csv(folder.parent / PIPELINE)[c].dtype == float
               for c in ("point_id", "lag"))
    model = mx.read_model(folder, name=_name("floats"))
    try:
        apart = []
        for name, cells in as_written.Data.cells.items():
            if cells.parameters or name in READERS:
                continue
            want, got = cells(), model.Data.cells[name]()
            if isinstance(want, np.ndarray):
                if not (isinstance(got, np.ndarray) and got.dtype == want.dtype
                        and np.array_equal(got, want, equal_nan=want.dtype.kind == "f")):
                    apart.append(f"{name}: {getattr(got, 'dtype', type(got))}")
            elif type(got) is not type(want) or got != want:
                apart.append(f"{name}: {got!r}, not {want!r}")
        assert not apart, apart
    finally:
        model.close()
        as_written.close()
    found = compiled_mismatches(build, folder, also=_term_c4_also)
    assert not found, _mismatch_lines(found)


# A single life's second life as no projection reads it, as (case, the rows, each the S
# point's twin it changes and its changes): numbers, which pandas reads as ints, and a
# blank beside a text, which it reads as an object column.
LABELS_NOT_TEXT = [("numbers", ((1, {"joint_sex": 7, "joint_smoker": 8}),
                                (3, {"joint_sex": 9, "joint_smoker": 10}))),
                   ("a blank and a text",
                    ((1, {"joint_sex": math.nan, "joint_smoker": math.nan}),
                     (3, {"joint_sex": "M", "joint_smoker": "S"})))]
LIFE_LABELS = [("sex", (1,)), ("sex", (2,)), ("smoker", (1,)), ("smoker", (2,))]


def _same_label(want, have):
    """Whether two outcomes of a label, ``("ok", value)`` or ``("raised", text)``, agree:
    the same raise, or a value of the same kind and equal, NaN meeting NaN."""
    if want[0] != have[0]:
        return False
    if want[0] == "raised":
        return want[1] == have[1]
    a, b = want[1], have[1]
    if isinstance(a, float) and isinstance(b, float) and a != a and b != b:
        return True
    return type(a) is type(b) and a == b


@pytest.mark.cython
def test_the_compiled_model_returns_a_label_that_is_not_text_as_modelx_does(sec_build,
                                                                             tmp_path):
    """C4 on labels that are not text: compiled, each life's ``sex`` and ``smoker`` is
    modelx's.

    ``sex(life)`` and ``smoker(life)`` return each life's column as read, and ``Data``
    checks the second life's on a joint point alone, so a single life's may be a number,
    which pandas reads as an int, or a blank, NaN, or any text.  An accessor typed ``str``
    would raise ``TypeError`` compiled; the sample types both on a blank copy as Python
    objects (sample_sec.py).  So on the anchor's twin and the family income benefit's, each
    case of :data:`LABELS_NOT_TEXT`: after checking, in modelx, that each second life's
    label is the int, the NaN or the text the file holds, each label of each life is called
    compiled and must return what modelx returns, in kind and value.
    """
    build = sec_build(SEC)
    found = []
    for case, changes in LABELS_NOT_TEXT:
        rows = pd.concat([_committed().loc[[point]].assign(**columns)
                          for point, columns in changes])
        folder = compiled_case(build, tmp_path / case.replace(" ", "_"), model_points=rows)
        model = mx.read_model(folder, name=_name("labels"))
        try:
            want = {}
            for key, (point, columns) in zip(point_keys(model), changes):
                p = projection(model, key)
                want[key] = [_did(lambda: p.cells[cell](*args))
                             for cell, args in LIFE_LABELS]
                for cell, column in (("sex", "joint_sex"), ("smoker", "joint_smoker")):
                    value, held = p.cells[cell](2), columns[column]
                    assert (math.isnan(value) if held != held else value == held), (
                        case, point, cell, value)
        finally:
            model.close()
        job = {"refs": {}, "calls": {key: LIFE_LABELS for key in want}}
        got = run_compiled(folder.parent, build.package.name, job)
        assert got["exit"] == 0, got["stderr"]
        assert all(got["compiled"].values()), got["compiled"]
        for key, outcomes in want.items():
            for (cell, args), mine, have in zip(LIFE_LABELS, outcomes, got["values"][key]):
                if not _same_label(mine, have):
                    found.append(f"{case}: idx {key}: {cell}{args} is {have!r} compiled, "
                                 f"{mine!r} in modelx")
    assert not found, "\n".join(found)


def _did(call):
    """``("ok", value)`` or ``("raised", "Type: message")``, as the compiled runner reports
    a call, modelx's ``FormulaError`` unwrapped to the error it carries."""
    try:
        return ("ok", call())
    except Exception as err:            # the outcome compared with the compiled one
        return ("raised", _raised(err))


# The compiled refusals' child: one process, which imports the compiled package once and
# runs each case on a fresh instance of the model, whose Data reads the case's own copies
# of the five files by absolute path, as sample_sec.py's second instance reads its table.
# A refusal names a file by its Reference, so the child's names the path, and the test
# writes each path as the file's name (_named), as modelx, reading the files by name,
# writes it.
REFUSALS_CHILD = '''\
import pickle, sys
case_root, package, job_path, result_path = sys.argv[1:5]
sys.path.insert(0, case_root)
import importlib
module = importlib.import_module(package + "._mx_model")
with open(job_path, "rb") as f:
    cases = pickle.load(f)


def did(call):
    try:
        value = call()
    except Exception as err:
        return ("raised", f"{type(err).__name__}: {err}")
    return ("ok", value)


results = []
for files, refs, calls, data in cases:
    model = getattr(module, "_c_" + module.mx_model._name)()
    for ref, path in files.items():
        setattr(model.Data, ref, path)
    for ref, value in refs.items():
        setattr(model.Projection, ref, value)
    values = [did(lambda: getattr(model.Projection[idx], cell)(*args))
              for idx, cell, args in calls]
    read = [did(lambda: getattr(model.Data, name)()) for name in data]
    results.append((values, read))
    del model
with open(result_path, "wb") as f:
    pickle.dump(results, f)
'''

# The files a case holds its own copy of, by the Data Reference that names each.
CASE_FILES = {"model_point_file": TABLE, "wop_pipeline_file": PIPELINE,
              "mort_table_file": MORT, "select_factor_file": SELECT,
              "lapse_table_file": LAPSE}


def _named(outcome, files):
    """A compiled outcome with each of a case's ``files``, ``{Reference: absolute path}``,
    written as the file's name in its message, as modelx's ``Data`` names it."""
    if outcome[0] != "raised":
        return outcome
    text = outcome[1]
    for path in files.values():
        text = text.replace(path, pathlib.Path(path).name)
    return ("raised", text)

# Lives no cell takes, inside the caches spec_sec.py sizes, which each cell refuses by its
# own formula, ValueError("invalid life"), in both engines, as (call, arguments), on the
# anchor's twin, a single life: a life of 0 and of 3, inside every life's cache, a second
# life on a single life, and a label's third life.  Every timing and kind inside its
# cache is a code the cell takes.
LIVES_IN_CACHE = [("age_at_entry", (0,)), ("age_at_entry", (2,)), ("age_at_entry", (3,)),
                  ("mort_group", (0,)), ("mort_group", (2,)), ("age", (0, 0)),
                  ("age", (0, 3)), ("mort_rate_base", (0, 3)), ("sex", (3,)),
                  ("smoker", (0,))]

# Powers an input the model accepts pushes past the largest float, which Python's float
# power refuses with OverflowError where C's pow gives an infinity, so that each cell calls
# Python's own there (Projection.idx_factor), as (case, the committed table's edit, the
# References, [(S point, cell, arguments)]): expense inflation of 1e20 a year, past it at
# t = 192, (1e20)^16; RPI and both caps at 1e200, the indexed point's cover and premium
# factors past it at its second anniversary; and a decreasing schedule at a rate of 1e14
# a year, its (1 + j_m)^300 past it.  The commutation discount's own, within 2e-8 of -1,
# is COMMUTE_RATES' "overflow".
OVERFLOWS = [
    ("expense inflation past the largest float", None, {"inflation_rate": 1e20},
     [(1, "inflation_factor", (192,)), (1, "result_cf", ())]),
    ("the index factors past the largest float", None,
     {"rpi_rate": 1e200, "idx_cover_cap": 1e200, "idx_prem_cap": 1e200},
     [(5, "idx_factor", (24,)), (5, "idx_prem_factor", (24,)), (5, "result_cf", ())]),
    ("the decreasing schedule past the largest float", _set("sched_rate", [2], 1e14), {},
     [(2, "benefit_sched", (0,)), (2, "result_cf", ())]),
]

# Projection's idx past the extract's last row, 14, and -1, beside the last row, 13, as
# (position, cell, arguments): past the last row the first read of a vector raises
# IndexError in both engines, each in its own words, and -1 reads every vector at its last
# element in both, so it is the last point, under that point's own point_id.
IDX_CASE = "an idx past the table and one before it"
IDX_EDGES = [(14, "point_id", ()), (14, "result_cf", ()), (-1, "point_id", ()),
             (-1, "proj_len", ()), (-1, "net_cf", (0,)), (13, "point_id", ()),
             (13, "proj_len", ()), (13, "net_cf", (0,))]

# Calls past the caches spec_sec.py sizes, which raise IndexError in the compiled model
# alone, as (call, arguments, what modelx does): a month either side of the t cache; a
# timing, a kind and a life past their codes; a policy month past the k cache; and the
# months left past the m cache.  modelx answers a month outside cover with zero, refuses
# a code it does not take, and computes the schedule and the annuity at any month.
COMPILED_ONLY = [
    ("net_cf", (722,), ("ok", 0.0)), ("net_cf", (-1,), ("ok", 0.0)),
    ("pols_if_at", (0, 4), ("raised", "ValueError: invalid timing")),
    ("claims", (0, 4), ("raised", "ValueError: invalid kind")),
    ("age_at_entry", (4,), ("raised", "ValueError: invalid life")),
    ("benefit_sched", (600,), None), ("annuity_certain_factor", (481,), None),
]


def _refusal_cases():
    """Every refusal the compiled model must make as modelx does, as (case, the table, the
    pipeline, the edits, the References, [(position, cell, arguments)], the Data cells to
    read).

    Each table is an extract, labelled otherwise than by position (:func:`_extract`), with
    its pipeline relabelled with it, so that a refusal naming a point by ``idx + 1`` names
    another; a case that edits the committed table edits it first, by its own labels, and
    is then relabelled.  A position, not a label, since a table ``Data`` refuses has no
    keys to give: each is the row's place in the table written, ``Projection``'s ``idx``,
    which the test indexes ``Projection`` by in modelx too.
    """
    committed, pipeline = _committed(), _committed_pipeline()
    relabel = dict(zip(committed.index, EXTRACT_LABELS))

    def extract(edit=None):
        table = edit(committed) if edit is not None else committed
        return table.rename(index=relabel)

    def lags(edit=None):
        table = edit(pipeline.copy()) if edit is not None else pipeline
        if "point_id" not in table:          # a pipeline that lost the column
            return table
        return table.assign(point_id=table["point_id"].map(lambda p: relabel.get(p, p)))

    def at(point):
        return list(committed.index).index(point)

    cases = []
    for case, edit, _ in MALFORMED:
        cases.append((case, extract(edit), lags(), None, {}, [(0, "result_cf", ())],
                      ("model_point_table",)))
    for case, edit, _ in MALFORMED_PIPELINE:
        cases.append((case, extract(), lags(edit), None, {}, [(at(11), "result_cf", ())],
                      ("wop_pipeline",)))
    for case, file, edit, cell, _, point in UNREADABLE:
        cases.append((case, extract(), lags(), {file: edit}, {},
                      [(at(point), "result_cf", ())], (cell,)))
    for case, edit, refs, point, _, _ in NOT_ISSUED:
        cases.append((case, extract(edit), lags(), None, refs,
                      [(at(point), cell, ()) for cell in ("result_cf", "proj_len")], ()))
    for case, edit, refs, point, _ in SHORT_PIPELINE:
        cases.append((case, extract(), lags(edit), None, refs,
                      [(at(point), "result_cf", ()),
                       (at(point), "wop_deferred_init", (1,))], ()))
    for case, edit, refs, point, _ in WAIVED_TOO_SOON:
        cases.append((case, extract(edit), lags(), None, refs,
                      [(at(point), "result_cf", ())], ()))
    for case, edit, pipeline_edit, points in OPENING_PAST_ONE:
        cases.append((case, extract(edit), lags(pipeline_edit), None, {},
                      [(at(points[0]), "result_cf", ())], ("wop_pipeline",)))
    waiver = [at(p) for p in committed.index[committed["wop"]]]
    for case, ref, value, outcome in WAIVER_RATES:
        if outcome != "accepted":
            cases.append((case, extract(), lags(), None, {ref: value},
                          [(i, "result_cf", ()) for i in waiver], ()))
    cases.append(("past its cover", extract(_set("duration_mth", [13], 300)), lags(), None,
                  {}, [(at(13), "result_cf", ()), (at(13), "proj_len", ())], ()))
    cut = {MORT: _dropped(lambda t: (t["age"] > 50) | (t["age"] < 20))}
    cases.append(("an age outside the mortality table",
                  extract(_set("age_at_entry", [1], 18)), lags(), cut, {},
                  [(at(1), "result_cf", ()), (at(2), "result_cf", ())], ()))
    cases.append(("a select duration past the table", extract(), lags(), None,
                  {"select_period": 7}, [(at(7), "result_cf", ())], ()))
    cases.append(("a select duration below the table", extract(), lags(), None,
                  {"select_period": -1}, [(at(7), "select_factor", (0,))], ()))
    cases.append(("a select duration below the table, written as a float", extract(),
                  lags(), None, {"select_period": -1.0},
                  [(at(7), "select_factor", (0,))], ()))
    cases.append(("a select duration past the table, written as a float", extract(),
                  lags(), None, {"select_period": 7.0}, [(at(7), "result_cf", ())], ()))
    cases.append(("a lag the pipeline does not hold", extract(), lags(), None, {},
                  [(at(12), "wop_deferred_init", (k,)) for k in (0, 5)]
                  + [(at(1), "wop_deferred_init", (1,))], ()))
    for case, edit, cell, args, _ in NOT_HELD:
        if edit is not None:
            cases.append((case, edit(committed), pipeline, None, {}, [(12, cell, args)],
                          ("point_id",)))
    cases.append(("lives no cell takes, inside the caches", extract(), lags(), None, {},
                  [(0, cell, args) for cell, args in LIVES_IN_CACHE], ()))
    fib = [at(p) for p in committed.index[committed["shape"] == "fib"]]
    for case, value, outcome in COMMUTE_RATES:
        if outcome != "accepted":
            cases.append((f"fib_commute_disc_rate at {case}", extract(), lags(), None,
                          {"fib_commute_disc_rate": value},
                          [(i, "result_cf", ()) for i in fib]
                          + ([(at(4), "proj_len", ())] if outcome == "refused"
                             else [(at(4), "annuity_certain_factor", (300,))]), ()))
    for case, edit, refs, calls in OVERFLOWS:
        cases.append((case, extract(edit), lags(), None, refs,
                      [(at(point), cell, args) for point, cell, args in calls], ()))
    return cases


@pytest.mark.cython
def test_the_compiled_model_refuses_what_modelx_refuses(sec_build, tmp_path):
    """Compiled, the model refuses what modelx refuses, with modelx's error and message.

    A ``ValueError`` raised in a cell typed ``long long`` or ``double`` propagates out of
    the compiled model as out of modelx.  So, each on its own inputs and References
    (:func:`_refusal_cases`), on an extract labelled otherwise than by position: every
    case of :data:`MALFORMED` and :data:`MALFORMED_PIPELINE`, refused by a projection and by
    the ``Data`` reader that checks the file; every case of :data:`UNREADABLE`, by a
    projection and by the ``Data`` cell that checks the table, so that a compiled ``Data``
    cell refuses each value its modelx cell refuses; every case of :data:`NOT_ISSUED`, by
    ``result_cf`` and ``proj_len``, of :data:`SHORT_PIPELINE` and :data:`WAIVED_TOO_SOON`;
    every opening state of :data:`OPENING_PAST_ONE`, by a projection and by the pipeline's
    reader; every waiver rate of :data:`WAIVER_RATES` that is refused, by the frame on
    every waiver point; a point past its cover; an age outside the mortality table, either
    side; a select duration outside its table, either side; a lag the pipeline does not
    hold; a label the vectors cannot hold, by ``Data.point_id``; and each life of
    :data:`LIVES_IN_CACHE`, inside the caches, which every cell refuses by its own
    formula.

    And every commutation discount :data:`COMMUTE_RATES` refuses, by the frame on every
    family income benefit point, and the float above -1, whose power passes the largest
    float; and each power of :data:`OVERFLOWS` past it: compiled, each cell calls Python's
    own power where C's gives an infinity, so that it raises the platform's
    ``OverflowError`` as modelx does, where it would carry an infinity on.

    And the refusals that are the compiled model's alone (:data:`COMPILED_ONLY`): a month
    past the ``t`` cache either side, a timing, a kind and a life past their codes, a policy
    month past the ``k`` cache and the months left past the ``m`` cache, each raising
    ``IndexError`` compiled, beside what modelx does.  And ``Projection``'s ``idx`` at the
    table's edges (:data:`IDX_EDGES`): one past the last row raises ``IndexError`` in both
    engines, compared by its type, the words being each engine's own, and ``-1`` is the
    last row in both, its every outcome the last row's and modelx's, which a build without
    bounds checks, or without Python's negative indices, would part from.

    The compiled model runs every case in one child, each on a fresh instance of the model
    that reads the case's own copies of the five files by absolute path, as
    ``sample_sec.py``'s second instance reads its table (:data:`REFUSALS_CHILD`), each
    path in a message written as the file's name, as modelx names it (:func:`_named`),
    and modelx reads each case afresh.
    """
    build = sec_build(SEC)
    cases = _refusal_cases()
    plain = len(cases)
    cases.append(("compiled only", _extract()[0], _extract()[1], None, {},
                  [(0, cell, args) for cell, args, _ in COMPILED_ONLY], ()))
    assert len(_extract()[0]) == 14
    cases.append((IDX_CASE, _extract()[0], _extract()[1], None, {}, IDX_EDGES, ()))
    root = tmp_path / "refused"
    compiled_case(build, root / "base")
    jobs, wants = [], []
    for i, (case, table, pipeline, edits, refs, calls, data) in enumerate(cases):
        folder = temp_inputs(root / f"case{i:03d}", model_path(SEC), model_points=table,
                             model_point_file=TABLE, edits={**(edits or {}),
                                                            PIPELINE: pipeline})
        model = mx.read_model(folder, name=_name("refused"))
        try:
            for ref, value in refs.items():
                setattr(model.Projection, ref, value)
            want = [_did(lambda: model.Projection[idx].cells[cell](*args))
                    for idx, cell, args in calls]
            want_data = [_did(model.Data.cells[name]) for name in data]
        finally:
            model.close()
        files = {ref: str((folder.parent / name).resolve())
                 for ref, name in CASE_FILES.items()}
        jobs.append((files, refs, calls, data))
        wants.append((want, want_data))
    job, result = tmp_path / "cases.pickle", tmp_path / "results.pickle"
    job.write_bytes(pickle.dumps(jobs))
    child = tmp_path / "refusals_child.py"
    child.write_text(REFUSALS_CHILD, encoding="utf-8")
    done = subprocess.run([sys.executable, "-P", str(child), str(root / "base"),
                           build.package.name, str(job), str(result)],
                          capture_output=True, text=True, timeout=900)
    assert done.returncode == 0, done.stderr[-4000:]
    got = pickle.loads(result.read_bytes())
    found, refused, edges = [], 0, {}
    only = iter(COMPILED_ONLY)
    for (case, *_, calls, data), (files, *_), (want, want_data), (have, have_data) in zip(
            cases, jobs, wants, got, strict=True):
        have = [_named(did, files) for did in have]
        have_data = [_named(did, files) for did in have_data]
        for (idx, cell, args), modelx_did, compiled_did in zip(calls, want, have,
                                                              strict=True):
            where = f"{case}: idx {idx}: {cell}{args}"
            if case == IDX_CASE:
                edges[idx, cell, args] = (modelx_did, compiled_did)
                if idx == 14:
                    for engine, did in (("modelx", modelx_did), ("compiled", compiled_did)):
                        if (did[0], str(did[1]).split(":")[0]) != ("raised", "IndexError"):
                            found.append(f"{where}: {engine} {did}, not IndexError")
                elif compiled_did != modelx_did:
                    found.append(f"{where}: compiled {compiled_did}, modelx {modelx_did}")
                continue
            if case == "compiled only":
                _, _, does = next(only)
                if does is not None and modelx_did != does:
                    found.append(f"{where}: modelx {modelx_did}, not {does}")
                if does is None and (modelx_did[0] != "ok" or type(modelx_did[1]) is not
                                     float):
                    found.append(f"{where}: modelx {modelx_did}, not a number")
                if (compiled_did[0], str(compiled_did[1]).split(":")[0]) != (
                        "raised", "IndexError"):
                    found.append(f"{where}: compiled {compiled_did}, not IndexError")
                continue
            if modelx_did[0] != "raised":
                found.append(f"{where}: modelx returned, where a refusal was meant")
            elif compiled_did != modelx_did:
                found.append(f"{where}: compiled {compiled_did}, modelx {modelx_did}")
            refused += 1
        for name, modelx_did, compiled_did in zip(data, want_data, have_data, strict=True):
            if modelx_did[0] != "raised":
                found.append(f"{case}: Data.{name}: modelx returned, where a refusal was "
                             f"meant")
            elif compiled_did != modelx_did:
                found.append(f"{case}: Data.{name}: compiled {compiled_did}, modelx "
                             f"{modelx_did}")
            refused += 1
    for (idx, cell, args), outcomes in edges.items():
        if idx == -1 and outcomes != edges[13, cell, args]:
            found.append(f"{IDX_CASE}: {cell}{args} at idx -1 is {outcomes}, at the last "
                         f"row {edges[13, cell, args]}")
    assert edges[-1, "point_id", ()][0] == ("ok", EXTRACT_LABELS[-1]), edges
    assert not found, "\n".join(found[:40])
    assert refused == sum(len(calls) + len(data) for *_, calls, data in cases[:plain])


# The cold call the stack test makes compiled, in a thread whose stack is reserved at each
# of these sizes in KiB, and then on the main thread.  1 MiB is the size asserted; the
# others bracket what the call needs, and the test reports the smallest that ran.
STACK_KIB = (64, 96, 128, 192, 256, 384, 512, 1024, 2048)

# How long the stack test waits for each child, in seconds: one runs in a few seconds, more
# under load.  A bracketing size may kill its child on a stack overflow by design, and
# where the overflow hangs instead, as Windows Error Reporting could, the wait ends sooner
# than for the two runs asserted, and the size is recorded as timed out.
BRACKET_TIMEOUT, ASSERTED_TIMEOUT = 120, 300


def _every_shape_rows():
    """Each shape at its longest cover, each issued now and 120 months on, and the
    pipeline, empty: the rows of :func:`_longest_rows`, the waiver point, of the level
    shape, and the family income benefit's point, and beside them S point 2's twin, the
    decreasing shape, and S point 6's, the joint point with both lives at 18, each on a
    50-year term from 18.  Returns ``(rows, pipeline, frames)``, each frame ``(label, its
    proj_len(), its t_entry())``.
    """
    rows, pipeline, frames = _longest_rows()
    committed = _committed()
    top = rows.index.max()
    more, frames = [], [(label, months, entry) for label, months, entry, _ in frames]
    for s_point, changes in ((2, {}), (6, {"joint_age": YOUNGEST})):
        twin = _label(committed, "twin", s_point, 0)
        for issued, months, entry in ((0, 600, 0), (-120, 720, 120)):
            top += 1
            row = committed.loc[[twin]].assign(age_at_entry=YOUNGEST,
                                               policy_term=LONGEST_TERM,
                                               duration_mth=issued, **changes)
            row.index = pd.Index([top], name="point_id")
            more.append(row)
            frames.append((top, months, entry))
    return pd.concat([rows, *more]), pipeline, frames


@pytest.mark.cython
def test_the_longest_cover_runs_cold_on_a_one_megabyte_stack(sec_build, tmp_path):
    """The deepest call the contract allows runs compiled on a 1 MiB stack (F7).

    On the rows of :func:`_every_shape_rows`, each shape at its longest cover: the waiver
    point, of the level shape on the select basis, the decreasing shape and the joint
    point, 50 years from 18, and the family income benefit's point, 40 years from 30, each
    issued now and 120 months on.  A cold ``net_cf`` in the last month runs the count
    chain, one cell a month from the end of the frame back to ``t_entry()``, 600 and 480
    months, 611 and 491 cells deep in modelx on a model just read
    (:func:`test_every_chain_runs_one_cell_a_month_from_a_cold_start`), with every switch
    that ships off on (:data:`SWITCHED_ON`).  Compiled it runs on the C stack, which the
    interpreter's recursion limit does not count.  1 MiB is the stack MSVC gives an
    executable's main thread unless the executable asks for more: a host that embeds
    Python, where python.exe itself asks for 2,000,000 bytes.  A thread whose stack is
    reserved at 1 MiB stands in for it on every platform (``uk_sec_support.run_compiled``),
    and in one each call runs cold and returns modelx's number, identically on x86-64
    (``uk_sec_support.exact_here``) and to 1e-12 elsewhere.  A stack too small kills the
    child, and the test fails naming the stack.  The thread's stack is read back too, from
    Windows or from glibc, and must be at most 1 MiB and a page: a stand-in larger than
    asked for would stand for nothing.  And the calls run again on the child's main
    thread, which is what ``run_sec.py --cython`` runs on.

    The calls run first at each size of :data:`STACK_KIB`, before anything is asserted,
    and every size's outcome goes into a warning, which the job's summary shows, and into
    the failure, if there is one: the smallest size that ran bounds the stack the chain
    needs on the compiler at hand.  A size below the need kills its child on a stack
    overflow, by design.  Each bracketing child is waited for :data:`BRACKET_TIMEOUT`
    seconds and the two asserted runs :data:`ASSERTED_TIMEOUT`, so that an overflow that
    hangs, rather than ends its child, costs minutes, not the job's hour, and a bracketing
    size that timed out is recorded as such.
    """
    build = sec_build(SEC)
    rows, pipeline, frames = _every_shape_rows()
    folder = compiled_case(build, tmp_path / "longest", model_points=rows,
                           edits={PIPELINE: pipeline})
    model = mx.read_model(folder, name=_name("longest"))
    try:
        for ref, value in SWITCHED_ON.items():
            setattr(model.Projection, ref, value)
        calls, want = {}, {}
        for label, months, entry in frames:
            key = _key(model, label)
            proj = projection(model, key)
            assert (proj.proj_len(), proj.t_entry()) == (months, entry), label
            calls[key] = [("net_cf", (months - 1,))]
            want[key] = proj.net_cf(months - 1)
    finally:
        model.close()
    job = {"refs": SWITCHED_ON, "calls": calls}

    def child(timeout, **where):
        try:
            return run_compiled(folder.parent, build.package.name, job, timeout=timeout,
                                **where)
        except subprocess.TimeoutExpired:
            return {"exit": f"none, timed out after {timeout} s", "stderr": ""}

    runs = {f"a {kib} KiB thread": child(ASSERTED_TIMEOUT if kib == 1024
                                         else BRACKET_TIMEOUT, stack_kib=kib)
            for kib in STACK_KIB}
    runs["the main thread"] = child(ASSERTED_TIMEOUT, main_thread=True)
    ran = [kib for kib in STACK_KIB if runs[f"a {kib} KiB thread"]["exit"] == 0]
    late = [kib for kib in STACK_KIB
            if str(runs[f"a {kib} KiB thread"]["exit"]).startswith("none")]
    record = (f"the compiled cold net_cf at the longest cover ran on a thread of "
              f"{ran or 'no size'} KiB and not of "
              f"{[kib for kib in STACK_KIB if kib not in ran]} KiB"
              f"{f', timed out at {late} KiB' if late else ''}; on the main thread "
              f"{'it ran' if runs['the main thread']['exit'] == 0 else 'it failed'}")
    warnings.warn(record, UserWarning)
    for where in ("a 1024 KiB thread", "the main thread"):
        got = runs[where]
        assert got["exit"] == 0, (
            f"the compiled model's deepest cold call failed on {where}, exit code "
            f"{got['exit']} ({record}):\n{got['stderr']}")
        assert all(got["compiled"].values()), got["compiled"]
        for key, value in want.items():
            assert got["values"][key][0][0] == "ok", (where, got["values"][key])
            have = got["values"][key][0][1]
            assert _as_modelx(have, value), (where, have, value)
        reserved = got["stack"]["reserved"]
        if where == "a 1024 KiB thread" and reserved is not None:
            assert reserved <= (1 << 20) + 4096, (
                f"the thread has {reserved} bytes of stack, not 1 MiB")


# A compiled model's Reference set after it has computed, in a child of its own: what the
# base Projection, an ItemSpace made before the change and one made after give for
# expenses(12), before inflation_rate is set to 0 and after.
STALE_CHILD = """\
import json, sys
sys.path.insert(0, sys.argv[1])
model = __import__(sys.argv[2]).mx_model
p = model.Projection
early = p[7]
values = [p.expenses(12), early.expenses(12)]
p.inflation_rate = 0.0
values += [p.expenses(12), early.expenses(12), p[8].expenses(12)]
print(json.dumps(values))
"""


@pytest.mark.cython
def test_a_compiled_model_clears_no_cache_when_a_reference_is_set(sec_build, tmp_path):
    """Compiled, a Reference set after a Space has computed leaves its values as they were.

    modelx recomputes what a Reference reaches when it is set.  The compiled model clears
    no cache: the base ``Projection``, and an ItemSpace made before the Reference was set,
    keep the values they computed, and only an ItemSpace made afterwards, which takes the
    References when it is made, computes with the new value.  The Projection docstring
    and ``model-sec.md`` say so, and tell a user to set every Reference on a model just
    imported.  This holds the compiled model to what they say, on ``inflation_rate``,
    which moves ``expenses(12)`` on every point on the books then: the base
    ``Projection``, the anchor's twin at ``idx`` 0, S's point 8 in force, made before, and
    the indexed point restated in force, made after, so that a modelx-cython that began to
    clear caches would be seen here, and the advice changed with it.  A compiled value
    meets modelx's as C4 holds it (:func:`_as_modelx`), and one the compiled model kept,
    its own value of before, identically.
    """
    build = sec_build(SEC)
    folder = compiled_case(build, tmp_path / "stale")
    child = tmp_path / "stale_child.py"
    child.write_text(STALE_CHILD, encoding="utf-8")
    done = subprocess.run([sys.executable, "-P", str(child), str(folder.parent),
                           build.package.name], capture_output=True, text=True,
                          timeout=300)
    assert done.returncode == 0, done.stderr
    base, early, base_after, early_after, late = json.loads(done.stdout.splitlines()[-1])
    model = mx.read_model(folder, name=_name("stale"))
    try:
        p = model.Projection
        before = (p.expenses(12), projection(model, 7).expenses(12))
        p.inflation_rate = 0.0
        fresh = (p.expenses(12), projection(model, 7).expenses(12),
                 projection(model, 8).expenses(12))
    finally:
        model.close()
    assert _as_modelx(base, before[0]) and _as_modelx(early, before[1]), (base, early,
                                                                          before)
    assert fresh[0] != base and fresh[1] != early
    assert (base_after, early_after) == (base, early), "the compiled model cleared a cache"
    assert _as_modelx(late, fresh[2]), (late, fresh[2])


@pytest.mark.cython
def test_run_sec_prints_the_compiled_model_as_it_prints_modelx(sec_build, tmp_path):
    """``run_sec.py --cython`` prints, for a point and for the block, what modelx prints.

    Each run in an interpreter of its own, as a user runs it.  With ``--build`` it runs the
    session's build, so nothing is built in the tree, and it checks for itself that the
    package it imported is compiled.  Line for line, the compiled model's output is
    modelx's: point 8's description and its first twelve rows and counts, point 6's, the
    joint life, whose line names its second life through each life's labels, and the
    block's lines for each point, its first twelve rows and its first twelve projection
    years.

    The same output is what a runner that ignored ``--build`` and ran modelx would print,
    so the runner is also given a directory that holds no build, and must refuse it,
    saying so, rather than print anything.
    """
    build = sec_build(SEC)
    runner = model_path(SEC).parent / "run_sec.py"
    for args in (("8",), ("6",), ("--block",)):
        expected = _run_sec(runner, *args)
        assert _run_sec(runner, *args, "--cython", "--build", str(build.out)) == expected
    empty = tmp_path / "no_build"
    empty.mkdir()
    done = _run_sec(runner, "8", "--build", str(empty), check=False)
    stderr = done.stderr.decode(errors="replace")
    assert done.returncode != 0 and done.stdout == b"", stderr
    assert f"holds no build of {SEC} for this interpreter" in stderr, stderr
