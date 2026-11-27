"""Tests for WOL_UK_SEC: the splice, future business, counts, regeneration, compiled.

``WOL_UK_SEC`` is ``WOL_UK_S`` taught to run in force at a valuation date
(UKLIB-SEC-PLAN.md, milestone M5, after USLIB-SEC-PLAN.md's Phase 1), and then made to
compile under modelx-cython (milestone M6, after USLIB-SEC-PLAN.md's Phase 2).  It runs on
two clocks: ``t`` counts months from the valuation date, the same month for every model point,
and ``duration_mth(t)`` counts the months the policy has been in force,
``duration_mth_init() + t``.  A model point may be a policy already in force at the
valuation date, in any month of its policy year, one issued at it, or one to be issued
after it, as in ``basiclife/BasicTerm_SE``.  A policy in force opens with two counts, the
full-cover ``policy_count`` and the paid-up ``pols_pu_init``, the library's first
two-strand count, and with five columns of state beside them, each measured at the
valuation instant, before month 0's events: the paid-up cover per paid-up policy, the
premiums paid, the cover and premium of the year an anniversary at the valuation date
closes, and the crossover, if it fell before the valuation date.

The worked example is not restated here.  On a point issued at the valuation date the two
clocks coincide and the model is ``WOL_UK_S``, and ``test_model_conventions_uk.py``
asserts that cell by cell on the twins of S's seven new-business points (T1), so every
golden of ``test_whole_of_life_uk.py`` on them holds on this model with no number
copied.  The conventions also hold the SEC family's other rules: every frame opens at
``t = 0``, ``pols_if`` is the ``BEF_DECR`` count, ``BEF_DECR`` is ``BEF_NB`` plus the
month's new business, new business enters once, and nothing happens before issue.  This
module holds the rest of the plan's tests (its §5) and the product's own facts:

* T2, the splice: an S point restated in force at month ``d``, opened with the state S
  carries into ``d``, continues S's projection from ``d`` on, in every cell of S's and in
  ``result_pols``.  The months straddle the product's events: the moratorium and the
  suicide window, the first anniversary, the first paid-up conversion, the crossover,
  premium cessation, the mortality cap and the limiting age.  The crossover stress that
  ships at 0 is on, at 0.5, and four variants of S's points, in a copy of S's table, add
  the RPI increases with the paid-up value, the double accidental benefit with the
  paid-up value, an over-50s policy issued at 80, and an underwritten female smoker.  A
  stress that lapses every policy is spliced by a test of its own, and the RPI's floor and
  caps are held to ``WOL_UK_S``'s by another.
* T3, future new business: a point issued ``k`` months after the valuation date is S's
  projection ``k`` months on, with zeros before issue and no table read there.
* D11's R1 and R2, and D3's and D5's chains: on the splice's grid no cell is called at a
  negative month, none on the books reads a month before them, and none reads beyond
  ``t + 1``; on the committed points no recursion runs backward over the frame; the policy
  clock is a closed form; and each chain, called cold, runs one cell a month within its
  policy year and two cells a year before it, back to ``t_entry()``, at the contract's
  longest cover, on each shape.
* T4, the count algebra: the counts roll forward on both strands through new business,
  deaths, lapses and conversions, ``result_pols`` is S's report with the new business, the
  paid-up deaths and the truncation residual beside it, multiplying ``policy_count`` and
  ``pols_pu_init`` by 2.5 with every assumption that ships at zero switched on multiplies
  every flow and every counted cell by 2.5 and moves no per-policy value, a point restated
  a month on continues its own flows, and the roll-forward, whose tolerance scales with the
  policies on the books, closes on ten million policies.
* T5, validation: each malformed row of the table is refused as it is read, naming its
  point, by its label on an extract labelled otherwise; each assumption table, malformed or
  holding a value that is not a number in its range, is refused before a value of it is
  read, naming its lines; the future horizon is a Reference that bounds future business; a
  point past the limiting age, one the contract does not issue and one that reads a
  Reference off its domain are refused by the frame, each domain at both its edges; a
  cover, a premium or premiums paid past the floats in the cell where they first are; the
  edges of the interface are accepted; and so is every state ``WOL_UK_S`` reaches, on each
  set of inputs on which those states differ.
* T6, regeneration: the committed ``model_point_table_sec.csv`` is what the generator makes
  of ``WOL_UK_S`` and its table as they stand.
* Then the product's own facts: the two clocks on the shipped points; each twin S's in every
  cell with improvement, the RPI, the take-up and the stress on, where T1 holds them at
  their shipped values and T2 holds improvement at 0; the committed rows continuing their S
  points, those read under References of their own continuing S under them; each history
  column read rather than recomputed (UKLIB-SEC-PLAN.md K14), the cover and the premium
  on the RPI and the fixed increases, the premiums paid, and the paid-up count and cover;
  expense inflation and mortality improvement on the valuation clock, and where
  improvement carries survivors past the truncation check; the crossover a policy month
  carried from the opening state; the moratorium, the suicide window and commission on
  the policy clock; acquisition on new business; a stress that lapses every policy, and
  the RPI's floor and caps; the cap on mortality, a NaN that reaches a bound and a check
  whose residual is NaN; the values outside cover; the block; an
  in-force extract; the runner; the cells' defaulted parameters; the docstrings; the
  shared input tables; and what the default grid reaches.
* The C step's representation, in modelx: the claims total held to ``WOL_UK_S``'s by its
  bits, every decode on every value, the padded arrays, the vectors' dtypes, the
  parameterless cells' Python numbers, the labels' refusals, the chains blocked by policy
  year and building no text, and the spec's and the sample's comments.
* C2, the fingerprint: every committed point computes what the model computed when its E
  step ended, frozen at the end of this module before its C step changed anything
  (USLIB-SEC-PLAN.md §5.4).
* Compiled, after the fingerprint, the tests marked ``cython``: C4 on the splice grid, at
  the contract's extremes, where each cap and bound binds, on every decoded value, on keys
  written as floats, on the committed rows under the References they were read from and
  on the rows valued on an anniversary; the labels; the refusals and overflows, message for
  message; each shape's deepest cold call on a 1 MiB stack; a Reference set late; and the
  runner.

SEC month ``t`` is S month ``t + source_mth`` throughout, the direction in which
``uk_sec_support`` takes its ``t_offset``: ``d`` for a point restated at S month ``d``,
``-k`` for one issued ``k`` months on.  ``WOL_UK_S`` has no point in force, so there is no
in-force twin.

**The core grid and the full one** (UKLIB-SEC-PLAN.md U6).  T2 and T3 over every S point
at every month, 179 cases, run by default on a core of 31, chosen so that between them they
reach every branch, every opening-state column, every kind of valuation month and both
sides of every ``min`` and ``max`` the full grid reaches, which
``test_the_core_grid_reaches_every_branch`` asserts.  The other cases, and the rules
test's scan of their rows, carry the ``sec_full`` marker and are skipped, with the reason
shown, unless ``UKLIB_SEC_FULL=1`` is set.  So do the slower tests' other cases
(``GRIDS``): over the committed points, the default run takes six among which every flow
and counted cell is nonzero (``CORE_POINTS``), and the full grid the rest; the cold
chains run on the paid-up shape by default and on the other three with the full grid; and
so on, each test's docstring saying which.  A compile test is never skipped, since a skip
fails the cython_uk job: those that compare the committed table under References of their
own compare by default the rows each set is for (``_c4_rows``), and the whole table with
the full grid.  They are never dropped: one leg of the CI
matrix sets it, and ``UKLIB_SEC_FULL=1 python -m pytest -m sec_full
lifelib/libraries/uklib/tests/test_whole_of_life_uk_sec.py`` runs them alone.  Each
splice row is released once it has been read (``_release``), as ``run_sec.py --block``
releases its points.

Every test keeps four rules.  Each model is read under a name of its own and closed:
``conftest.whole_of_life`` reads S under its default name, and reading a model under a
name in use renames the open one.  No test writes inside the library tree: every changed
input goes through ``uk_sec_support.temp_inputs`` into a temporary directory, because a
CSV added beside the models, even briefly, would fail a concurrent
``test_every_csv_beside_the_model_is_actually_read``.  No test indexes ``Projection`` by
hand: the keys come from ``uk_registry.point_keys`` and the ItemSpaces from
``uk_registry.projection``, and a generated row is found by what it is, its kind, its S
policy and its month (``_row``), so neither a renumbered table nor the C step's positions
can point a test at the wrong row.  And a timing or a kind is passed through ``_code``,
which gives the model's int Reference of its name where the model has one, as at stage
``"EC"`` it will, and the string at stage ``"E"``; every comparison with S passes
``uk_sec_support.codes``, ``{}`` at stage ``"E"``.  At stage ``"EC"``, from the C step on,
the model is keyed by ``idx`` and every code is an int Reference, and the tests read it
through the same helpers, unchanged; a call that spells a timing as text is ``WOL_UK_S``'s.
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
    compiled_case, compiled_mismatches, exact_here, label_mismatches,
    labels_refusing_non_text, reporting_cells, run_compiled)
from uk_sec_support import _wol_c4_also
from uk_sec_support import generated_columns

SEC, TWIN = "WOL_UK_SEC", "WOL_UK_S"
TABLE = "model_point_table_sec.csv"
SPEC = SEC_SPECS[SEC]

# S's seven points, all new business: the over-50s anchor cell, a 70-year-old woman paying
# £30 a month for £5,000 (1); with the double accidental benefit (2); with the pro-rata
# paid-up value (3); with RPI increases (4); the underwritten cell, a 40-year-old man
# paying £101.25 a month for life for £150,000 (5); with fixed increases of 5% and 10% (6);
# and an over-50s male smoker at 65 (7).
S_POINTS = (1, 2, 3, 4, 5, 6, 7)

# T2's months (UKLIB-SEC-PLAN.md §6.4).  On the over-50s points at 70: the second month; 6,
# inside the moratorium; 11, 12 and 13 about the first anniversary, where the moratorium
# ends, the lapse table moves to its second year and commission stops; 60, the lapse
# table's last year; 118 to 121 about the first conversion to paid-up, at the end of policy
# month 119, the 120th payment, half of 240; 165 to 167 about the crossover at 166, and 185
# and 186 about the RPI point's at 185; 239 to 241 about premium cessation at 240; 479 to
# 481 about the mortality cap, which binds from attained age 110, policy month 480; and
# 599, the last month before the limiting age.  On the underwritten points at 40: 11 to 13
# about the suicide window's end and the first anniversary; 642 and 643 about the
# increasing point's crossover; 887 to 889 about the cap at 888, attained age 114; and 959,
# the last month.  On the male smoker at 65: 222 and 223 about its crossover; 299 to 301
# about its cessation at 300; 431 to 433 about its cap at 432, attained age 101; and 659.
_O50 = (1, 6, 11, 12, 13, 60, 118, 119, 120, 121, 165, 166, 167, 239, 240, 241, 479, 480,
        481, 599)
_UW = (11, 12, 13, 642, 643, 887, 888, 889, 959)
SPLICE_MTHS = {1: _O50, 2: _O50, 3: _O50, 4: (*_O50, 185, 186), 5: _UW, 6: _UW,
               7: (222, 223, 299, 300, 301, 431, 432, 433, 659)}

# T3's months: issued one month on, which puts the policy anniversaries a month off the
# valuation years; twelve, which puts them back on; and the horizon, 120, the latest the
# table admits.  Each variant is issued 13 months on, more than a year after the valuation
# date and off its anniversaries (USLIB-SEC-PLAN.md §7.1, *Record — M14*, *Splice grid*).
FUTURE_MTHS = (1, 12, 120)

# Six more S points, in the splice's copy of S's table and never in the committed one,
# each one of S's points changed so as to reach what S's own points cannot:
#
# 8, S point 4 with the pro-rata paid-up value: conversions at a cover that RPI has
#   raised, so that each paid-up cash sum is a share of an indexed cover;
# 9, S point 2 with the pro-rata paid-up value: the double accidental benefit, the
#   moratorium and the paid-up strand together;
# 10, S point 1 issued at 80, its premiums ceasing at 90, after 120 months: the latest
#   entry age of the over-50s cell, a cessation of its own, total premiums below the cash
#   sum, so no crossover, and the cap from policy month 360;
# 11, S point 6 as a female smoker: the underwritten cell's other mortality rows, the
#   assured female smoker's, which no S point reads, capped from policy month 852;
# 12, S point 3 with its premiums ceasing after 239 months, an odd number: the first
#   conversion at the end of policy month 119, when 120 of 239 payments, more than half,
#   have been made, so that the paid-up strand is in force from 120, half of 239 rounded
#   up, where half rounded down would be 119; with a cessation a multiple of 12 the two
#   agree;
# 13, S point 1 with a cash sum of £7,180, which the 240th premium, its last, passes and
#   the 239th does not: its crossover falls in policy month 239, its last premium month,
#   so that the crossover's search, from issue and from the valuation date, finds it in
#   its last month, where every other point's crossover, 166, 185, 222 and 642, falls
#   short of its last premium month, or never comes.
#
# Each variant is (the S point it changes, the columns it changes); the policy_id keeps
# the generated ids apart.
VARIANTS = {
    8: (4, {"policy_id": "WOL-900008", "variant_paid_up": True}),
    9: (2, {"policy_id": "WOL-900009", "variant_paid_up": True}),
    10: (1, {"policy_id": "WOL-900010", "entry_age": 80, "cessation_months": 120}),
    11: (6, {"policy_id": "WOL-900011", "sex": "F", "smoker": "S"}),
    12: (3, {"policy_id": "WOL-900012", "cessation_months": 239}),
    13: (1, {"policy_id": "WOL-900013", "sum_assured": 7180}),
}
VARIANT_MTHS = {8: (118, 119, 120, 121, 185, 186, 200, 239, 240, 241),
                9: (11, 12, 13, 119, 120, 200),
                10: (1, 11, 12, 13, 119, 120, 121, 359, 360, 361, 479),
                11: (12, 642, 643, 851, 852, 853, 959),
                12: (119, 120, 121, 238, 239, 240),
                13: (238, 239, 240)}
LATE_FUTURES = tuple((p, 13) for p in VARIANTS)


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


# The months from issue to the limiting age of each S point and variant, 12 times the
# years from its entry age to 120.
COVER = {p: 12 * (120 - int(x)) for p, x in _s_table_with_variants()["entry_age"].items()}

# The committed rows the generator reads from S under References of their own (the spec's
# derived_refs), by (S policy, month), with those References.
UNDER_REFS = {(_s_table().at[p, "policy_id"], d): refs
              for (p, d), refs in SPEC.derived_refs.items()}

# T2's cases, as (row_kind, S point, source_mth): each S point restated in force at each
# of its months, and each variant at its own.  WOL_UK_S has no point in force, so no twin
# is a splice case.  T3's cases, as (S point, k).
SPLICES = (tuple(("derived", p, d) for p in S_POINTS for d in SPLICE_MTHS[p]
                 if d < COVER[p])
           + tuple(("derived", p, d) for p, mths in VARIANT_MTHS.items() for d in mths))
IN_FORCE_TWINS = ()
FUTURES = tuple((p, k) for p in S_POINTS for k in FUTURE_MTHS) + LATE_FUTURES

# The default run's cases (the module docstring), each with what it is there for.  The
# rest of SPLICES and FUTURES run with UKLIB_SEC_FULL=1.
CORE_SPLICES = {
    ("derived", 1, 6): "the anchor cell inside its moratorium, in its first policy year",
    ("derived", 1, 11): "the anchor cell in the moratorium's last month",
    ("derived", 1, 166): "the anchor cell in its crossover month, stressed from t = 0",
    ("derived", 1, 240): "the anchor cell as its premiums cease",
    ("derived", 1, 480): "the anchor cell in its first capped month",
    ("derived", 1, 599): "the anchor cell in the last month before the limiting age",
    ("derived", 3, 119): "the paid-up point in the month of its first conversions",
    ("derived", 3, 120): "the paid-up point with its first conversions in force",
    ("derived", 3, 241): "the paid-up point after cessation, its strand running off",
    ("derived", 4, 12): "the RPI point on its first anniversary, its first increase",
    ("derived", 4, 186): "the RPI point past its crossover",
    ("derived", 4, 239): "the RPI point in its last premium month",
    ("derived", 4, 241): "the RPI point after its premiums ceased, its crossover history",
    ("derived", 5, 12): "underwritten on its first anniversary, the suicide window over",
    ("derived", 5, 888): "underwritten in its first capped month",
    ("derived", 6, 11): "underwritten increasing, inside the suicide window",
    ("derived", 6, 643): "underwritten increasing past its crossover",
    ("derived", 7, 223): "the male smoker past its crossover",
    ("derived", 7, 300): "the male smoker as its premiums cease",
    ("derived", 8, 186): "RPI and paid-up past the crossover",
    ("derived", 9, 200): "the double accidental benefit with paid-up, the strand in force",
    ("derived", 10, 360): "issued at 80, its first capped month",
    ("derived", 11, 852): "an underwritten female smoker in its first capped month",
    ("derived", 12, 120): "an odd cessation, its strand in force from half of 239 up",
    ("derived", 13, 239): "a crossover in the last premium month, the valuation month",
}
CORE_FUTURES = {
    (1, 1): "issued a month off the valuation anniversaries",
    (3, 120): "the paid-up point at the horizon",
    (4, 1): "the RPI increases a month off the valuation anniversaries",
    (6, 12): "underwritten increasing, a year on",
    (8, 13): "RPI and paid-up, more than a year on",
    (13, 13): "a crossover in the last premium month, searched from issue",
}

SEC_FULL = os.environ.get("UKLIB_SEC_FULL") == "1"
FULL_ONLY = (pytest.mark.sec_full,
             pytest.mark.skipif(not SEC_FULL, reason="the full splice grid runs with "
                                "UKLIB_SEC_FULL=1 (UKLIB-SEC-PLAN.md U6)"))

# The tests that run over every committed point run the core's by default and the rest on
# the full grid (GRIDS): the twins of the anchor, paid-up and underwritten points, the
# paid-up point in force, the RPI point issued later and the point paid-up entirely, by
# label, among which every flow and every counted cell is nonzero.
CORE_POINTS = (1, 3, 5, 10, 14, 17)
GRIDS = [pytest.param("core", id="core"), pytest.param("full", id="full", marks=FULL_ONLY)]


def _on_grid(grid, label):
    """Whether committed point ``label`` is one the ``grid`` case of a test runs on."""
    return (label in CORE_POINTS) == (grid == "core")

# What the splice sets in both models, S and SEC alike, before either evaluates anything.
# Two inputs run on the valuation clock (D7): expense inflation, which S runs from issue
# and SEC from the valuation date, so at the shipped 3% the expenses of a point opened at d
# differ by the inflation of the policy years before d, by design, and at 0 both factors
# are 1; and mortality improvement, which S runs from issue too, and which ships at 0,
# where the splice keeps it (UKLIB-SEC-PLAN.md §6.4, §9 item 4): on it SEC's mortality at d
# is S's at d with none of the improvement since issue, by design.  Each clock is then
# asserted on its own, with its rate on.  There is no scenario table, so no input table
# moves with d.  The one other assumption that ships at zero, the crossover stress on the
# lapse rate, is on, at 0.5, so that past the crossover the premiums paid, which the
# opening state carries, move the lapses, the conversions and so every count: without it
# no number past the moratorium reads them.  The identity does not depend on the value,
# only on both models having the same one; a stress that lapses every policy, the lapse
# rate's bound at 1, has a test of its own.
SPLICED_REFS = {"inflation_rate": 0.0, "mort_improvement": 0.0, "lapse_crossover_beta": 0.5}

# The improvement the module switches on where it compares the model with itself or a twin
# with S: a rate at which check_truncation holds on every committed point, 0.2% a year
# (UKLIB-SEC-PLAN.md §6.4).  The truncation test records where it gives way.
IMPROVEMENT = 0.002

# Every assumption that ships at zero, switched on, for T4, at the shipped inflation: the
# stress, as the splice sets it, and improvement, which T4 can hold since it compares the
# model with itself.
SWITCHED_ON = {"lapse_crossover_beta": 0.5, "mort_improvement": IMPROVEMENT}

# The cells T2 and T3 skip beyond T1's, which already drop result_pols as a whole (the
# spec's exempt).  proj_len counts from the valuation date on SEC and from issue on S, so it
# differs by d, or by -k, by design; frame_mismatches asserts what it must get right, that
# both frames end at the same instant.  Both tests compare result_pols column by column
# instead.
SPLICE_EXEMPT = TWIN_EXEMPT_DEFAULT | SPEC.exempt | {"proj_len"}
FUTURE_EXEMPT = SPLICE_EXEMPT

# The result_cf columns that expense inflation moves, and the cells they are made of: on
# the committed points, at the shipped 3% and the shipped improvement of 0, the only places
# an in-force row departs from S.
INFLATED = ("expenses", "net_cf")
INFLATION_CELLS = frozenset({"inflation_factor", "expenses", "net_cf", "result_cf"})

# The S cell whose exact value is 0 and whose computed value is rounding about it, the
# roll-forward's residual: a comparison with S holds it at the harness's absolute floor of
# 1e-9, and every other cell at none (_compare).
RESIDUALS = frozenset({"check_pols_roll_fwd_resid"})

# The reads keyed by an attained age or a policy year, and the monthly rates, none of which
# may be evaluated before issue (R1, D4).  The annual rates, mort_rate and lapse_rate, are
# columns of result_pols, as in WOL_UK_S, so the report evaluates them in every month of
# the frame, and before issue each is 0.0 without a read (OUTSIDE_COVER): the reads under
# them are what T3 holds.
KEYED_READS = ("age", "duration", "policy_year", "lapse_rate_base", "mort_rate_mth",
               "lapse_rate_mth")

# The cells that scale with the counts.  Every other cell is a per-policy amount, a rate,
# a factor, a clock or a flag, and must not move when the counts do.  The year openings of
# the counted chains are counts too, the C step's (§6.4, *Record -- M6*); the premiums
# paid's is per policy.  The paid-up cover's refusal scales with it, but no sweep reaches
# it, whose error path alone calls it, so no test of the counts sees it.
COUNTED = frozenset({
    "policy_count", "pols_if_init", "pols_pu_init", "pols_if", "pols_if_at", "pols_new_biz",
    "pols_pu", "pu_benefit", "pols_all", "pols_death", "pols_death_pu", "pols_exit",
    "pols_convert", "pols_lapse", "pols_maturity", "premiums", "claims", "expenses",
    "commissions", "net_cf", "check_pols_roll_fwd_resid", "result_cf", "result_pols",
    "pols_if_py", "pols_pu_py", "pu_benefit_py"})

# result_pols' columns, in its order: the full-cover count, the new business within it,
# the paid-up count, the month's deaths on each strand, its lapses and conversions in
# processing order, and the truncation residual; then S's other columns, the premiums paid,
# the cover, the benefit per death and the rates, which no count moves.
RESULT_POLS = ["pols_if", "pols_new_biz", "pols_pu", "pols_death", "pols_death_pu",
               "pols_lapse", "pols_convert", "pols_maturity", "prem_cum_pp", "cover_pp",
               "benefit_death_pp", "mort_rate", "lapse_rate"]
COUNTS_POLS = RESULT_POLS[:8]
PER_POLICY_POLS = RESULT_POLS[8:]

# S's three timings and BEF_NB, the one running in force adds; and the kinds.
TIMINGS = ("BEF_NB", "BEF_DECR", "BEF_LAPSE", "AFT_DECR")
KINDS = ("DEATH", "DEATH_PU", "LAPSE")
BENEFITS = ("NON_ACC", "ACC", "DEATH", "PAID_UP")

# What each cell holds outside cover, before issue and from the month cover has ended, as
# its docstring says: no count, so no cash flow; no cover, premium or premiums paid; no
# rate read at a policy year or an age the policy does not have; no window open.  The type
# is part of the value.  A count is a float in every branch, a flag a bool and the payments
# made an int, because the C step types a cell by the values it returns (USLIB-SEC-PLAN.md
# F3).  The guard test also calls pols_if_at at each timing, claims at each kind and the
# total, ALL, and benefit_pp at each benefit, all 0.0.  The two refusals the C step moves
# off their chains hold their chains' 0.0 there too.
OUTSIDE_COVER = {
    "is_active": False, "in_moratorium": False, "payments_made": 0, "pu_eligible": False,
    "cover_pp": 0.0, "premium_pp": 0.0, "prem_cum_pp": 0.0, "mort_rate": 0.0,
    "lapse_rate_base": 0.0, "lapse_rate": 0.0, "pols_if": 0.0, "pols_pu": 0.0,
    "pu_benefit": 0.0, "pols_all": 0.0, "pols_new_biz": 0.0, "pols_death": 0.0,
    "pols_death_pu": 0.0, "pols_exit": 0.0, "pols_convert": 0.0, "pols_lapse": 0.0,
    "pols_maturity": 0.0, "premiums": 0.0, "expenses": 0.0, "commissions": 0.0,
    "net_cf": 0.0, "check_pols_roll_fwd_resid": 0.0, "prem_cum_pp_refusal": 0.0,
    "pu_benefit_refusal": 0.0}

# The cells a month outside cover may not reach: the clocks of the contract and the
# monthly rates, each keyed by a policy year or an attained age.  The reads that guard
# themselves are held by their values in OUTSIDE_COVER instead.
IN_COVER_ONLY = ("age", "duration", "policy_year", "mort_rate_mth", "lapse_rate_mth")

# The opening state, in the table's order, and the cells running in force and compiling add
# to WOL_UK_S's, each of which the symbol map must name: at the C step, the label, the
# decodes, the cell's last lapse year, the two refusals moved off their chains and the four
# chains' year openings.
STATE = ("pols_pu_init", "pu_benefit_pp_init", "prem_cum_pp_init", "cover_pp_init",
         "premium_pp_init", "crossover_mth_init")
OPENINGS = ("pols_if_py", "pols_pu_py", "pu_benefit_py", "prem_cum_pp_py")
NEW_CELLS = ("policy_count", "duration_mth_init", "duration_init", "t_entry", "is_active",
             "limit_mth", "pols_new_biz", *STATE, "point_id", "cell_code",
             "escalation_code", "mort_schedule", "lapse_last_year", "prem_cum_pp_refusal",
             "pu_benefit_refusal", *OPENINGS)

INFLATION = 0.03        # the shipped inflation_rate, which the inflation test reads

# The recursion limit, as mx.set_recursion takes it, under which the committed points are
# first swept (R2, F7).  A report evaluates each column in ascending t, so a forward
# recursion, through t - 1, finds the month before already cached: the committed points'
# sweep passes under a limit of 12 (measured at M5).  A backward recursion over the frame,
# through t + 1, opens a chain as long as the frame, and the shortest committed frame is
# 360.
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


def _sec_inputs(tmp_path, table, edits=None):
    """A copy of the product directory whose SEC table is ``table``, other inputs changed
    by ``edits``, as :func:`uk_sec_support.temp_inputs` takes them; its SEC folder."""
    return temp_inputs(tmp_path, model_path(SEC), model_points=table,
                       model_point_file=TABLE, edits=dict(edits or {}))


def _read_edited(tmp_path, edit, edits=None):
    """WOL_UK_SEC read from a copy whose SEC table is ``edit(_committed())``."""
    folder = _sec_inputs(tmp_path, edit(_committed()), edits)
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
    """Evaluate on an S point what the splice compares: the sweep, and cells more.

    :func:`uk_sec_support.sweep` reaches ``WOL_UK_S``'s ``pols_if_at`` at none of its
    timings, since S's ``pols_if`` is a recursion of its own and its exits read
    ``"BEF_LAPSE"`` alone; nor ``duration_mth``, which no S formula reads, nor the
    crossover, which no report reads; nor, on a point that does not reach them, the
    benefit of each kind, the payments made, the moratorium and the paid-up eligibility.
    A cell S never evaluates is compared nowhere, so they are evaluated here, over the
    frame, and the splice and the future comparison see them too.
    """
    sweep(proj)
    for t in range(proj.proj_len()):
        for timing in ("BEF_DECR", "BEF_LAPSE", "AFT_DECR"):
            proj.pols_if_at(t, timing)
        for kind in BENEFITS:
            proj.benefit_pp(t, kind)
        proj.duration_mth(t)
        proj.payments_made(t)
        proj.in_moratorium(t)
        proj.pu_eligible(t)
    proj.crossover_mth()
    proj.payments_expected()


def _mismatches(s_proj, sec_proj, **kwargs):
    """:func:`uk_sec_support.twin_mismatches` of an S point and an SEC row, the one place
    this module compares them so.

    It passes the SEC Space's :func:`uk_sec_support.codes`, which map S's timing, benefit
    and kind strings to the int codes the C step gives them, unless the caller passes its
    own, and the spec's ``twin_arg_map``, which maps S's ``claims(t, None)``, its total,
    onto SEC's ``ALL`` and passes every other key unchanged, as ULB's module composes them
    (USLIB-SEC-PLAN.md §7.1, *Record -- M14*, *Carried into Phase 1*).  Every comparison of
    a row with S goes through here, so each takes the C step's codes and map.
    """
    kwargs.setdefault("codes", codes(sec_proj))
    return twin_mismatches(s_proj, sec_proj, arg_map=SPEC.twin_arg_map, **kwargs)


def _compare(s_proj, sec_proj, month, exempt, columns=None):
    """Where SEC's row departs from S's point from S month ``month`` on, in two passes.

    First the frames, ``result_cf`` (over ``columns``, or every column both hold) and
    ``result_pols``, SEC row ``t`` against S row ``t + month``, frames ending together;
    then every cell of S's but ``exempt`` and :data:`RESIDUALS`, at every argument S cached
    inside its frame from ``month`` on, moved onto SEC's clock, S's timing and kind strings
    mapped onto SEC's codes (``uk_sec_support.codes``).  Both to 1e-9 relative with no
    absolute floor (USLIB-SEC-PLAN.md §5.2, T2, precised at M11): a floor of 1e-9 passes an
    error of 1% in any value below 1e-7.  Then the cells of :data:`RESIDUALS` alone, at the
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
                             atol=0.0, codes=codes(sec_proj))
    return found + _mismatches(s_proj, sec_proj, t_offset=month,
                                   exempt=exempt | (set(s_proj.cells) - RESIDUALS),
                                   codes=codes(sec_proj))


def _continues_s(s_proj, sec_proj, month):
    """Where a committed row departs from S's point ``s_proj`` from S month ``month`` on.

    The splice's comparison (:func:`_compare`), on the committed model at the shipped
    assumptions: frame by frame, ``result_cf`` and ``result_pols``, then cell by cell over
    every cell of S's but :data:`SPLICE_EXEMPT`.  The shipped 3% expense inflation runs
    from issue in S and from the valuation date here (D7), so :data:`INFLATED`'s two
    columns, and :data:`INFLATION_CELLS`, differ by design and are left out; the inflation
    test holds them.  Improvement ships at 0, where the two clocks agree.  Every other
    column and cell must agree, to 1e-9 relative, with no absolute floor but on the
    residual.
    """
    keep = [c for c in s_proj.result_cf().columns if c not in INFLATED]
    return _compare(s_proj, sec_proj, month, SPLICE_EXEMPT | INFLATION_CELLS, keep)


def _case_id(kind, s_point, month):
    """A case's id: ``point2-d12``, or ``point2-k3`` if issued later."""
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
    """WOL_UK_SEC read in place, as committed, and swept once, cold; what it met.

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
    """WOL_UK_SEC read in place, as committed, with every point swept (sec_read)."""
    return sec_read[0]


@pytest.fixture(scope="module")
def s_model():
    """WOL_UK_S read in place, as committed, with every point swept.

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
    SEC runs on the same assumption tables, and on a model point table of its own, built by
    the generator from the registered spec with its rows replaced by the cases this run
    selects, the core or the full grid (:func:`_selected`), out of this S model, so each
    row opens with the state of the very run it is compared with.  No input table moves
    with ``d``: WOL's two valuation-clock inputs are the ``inflation_rate`` and
    ``mort_improvement`` References.  Every S point is then swept (:func:`_sweep_s`), and
    stays swept; each SEC row is projected by the case that compares it and released once
    compared (:func:`_settle`).
    """
    root = tmp_path_factory.mktemp("spliced")
    s_folder = temp_inputs(root / "s", model_path(TWIN),
                           model_points=_s_table_with_variants())
    s = mx.read_model(s_folder, name=_name("s_spliced"))
    for ref, value in SPLICED_REFS.items():
        setattr(s.Projection, ref, value)
    derived = [(p, d) for kind, p, d in _selected(SPLICES + IN_FORCE_TWINS, CORE_SPLICES)
               if kind == "derived"]
    spec = dataclasses.replace(SPEC, derived=tuple(derived), derived_refs={},
                               future=tuple(_selected(FUTURES, CORE_FUTURES)))
    table, companions = build_sec_table(spec, s)
    assert companions == {}
    sec = mx.read_model(_sec_inputs(root / "sec", table), name=_name("sec_spliced"))
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


def _active(x, t):
    return x.is_active(t)


# What test_the_core_grid_reaches_every_branch asks of the core's rows in the model's own
# values, which no column of the table shows: each holds of some core row, or of a core row
# in some month of its frame.  At the valuation date, every opening-state column in use, a
# count or an amount apart from its issue value, and each kind of valuation month the
# contract's windows make: inside the moratorium, inside the suicide window, after
# cessation and past the crossover.  Later in the frame, every branch and both sides of
# each min and max the full grid reaches: the moratorium and its end, the suicide window,
# an increase, cessation, commission, a conversion, a terminating lapse, a paid-up death,
# the crossover stress and the premiums paid below the cover, the lapse table inside and
# past its last year, the cap on mortality binding and not, the double accidental benefit,
# the payments made capped at cessation, and the limiting age's last month.
AT_VALUATION = {
    "pols_pu_init above 0": lambda x: x.pols_pu_init() > 0.0,
    "pu_benefit_pp_init above 0": lambda x: x.pu_benefit_pp_init() > 0.0,
    "prem_cum_pp_init above 0": lambda x: x.prem_cum_pp_init() > 0.0,
    "cover_pp_init above the sum assured": lambda x: x.cover_pp_init() > x.sum_assured(),
    "premium_pp_init above the premium at issue": lambda x: (
        x.premium_pp_init() > x.premium_mth()),
    "valued inside the moratorium": lambda x: (
        0 < x.duration_mth_init() < x.moratorium_mths()),
    "valued inside the suicide window": lambda x: (
        x.cell() == "UW" and 0 < x.duration_mth_init() < x.suicide_mths),
    "valued once premiums have ceased": lambda x: (
        0 < x.cessation_mths() <= x.duration_mth_init()),
    "valued past the crossover": lambda x: 0 <= x.crossover_mth() < x.duration_mth_init(),
    "crossover_mth_init 0 or more": lambda x: x.crossover_mth_init() >= 0,
    "an escalating point valued once premiums have ceased": lambda x: (
        x.escalation() != "level" and 0 < x.cessation_mths() <= x.duration_mth_init()),
    "an increase at t = 0 on an anniversary valuation": lambda x: (
        0 < x.duration_mth_init() and x.duration_mth_init() % 12 == 0
        and x.cover_pp(0) > x.cover_pp_init()),
}
IN_FRAME = {
    "the moratorium": lambda x, t: x.in_moratorium(t),
    "the moratorium's end": lambda x, t: (
        _active(x, t) and x.cell() == "O50" and x.duration_mth(t) == x.moratorium_mths()),
    "the suicide window": lambda x, t: (
        _active(x, t) and x.cell() == "UW" and x.duration_mth(t) < x.suicide_mths),
    "an increase": lambda x, t: (
        _active(x, t) and x.esc_cover_step() > 0.0 and x.duration(t) > x.duration_init()),
    "premiums ceasing": lambda x, t: (
        x.cessation_mths() > 0 and x.duration_mth(t) == x.cessation_mths()),
    "commission": lambda x, t: x.commissions(t) > 0.0,
    "a conversion to paid-up": lambda x, t: x.pols_convert(t) > 0.0,
    "a lapse that terminates": lambda x, t: x.pols_lapse(t) > 0.0,
    "a paid-up death": lambda x, t: x.pols_death_pu(t) > 0.0,
    "the crossover stress": lambda x, t: (
        _active(x, t) and x.lapse_rate(t) > x.lapse_rate_base(t)),
    "premiums paid below the cover": lambda x, t: (
        _active(x, t) and x.prem_cum_pp(t) <= x.cover_pp(t)),
    "inside the lapse table": lambda x, t: (
        _active(x, t) and x.policy_year(t) <= x.lapse_last_year()),
    "past the lapse table's last year": lambda x, t: (
        _active(x, t) and x.policy_year(t) > x.lapse_last_year()),
    "the mortality cap binding": lambda x, t: x.mort_rate(t) == 1.0,
    "a mortality rate below the cap": lambda x, t: 0.0 < x.mort_rate(t) < 1.0,
    "the double accidental benefit": lambda x, t: (
        _active(x, t) and x.adb_multiplier() > 1.0 and not x.in_moratorium(t)),
    "the payments made capped at cessation": lambda x, t: (
        _active(x, t) and 0 < x.cessation_mths() == x.payments_made(t)
        and x.duration_mth(t) + 1 > x.cessation_mths()),
    "the limiting age's last month": lambda x, t: x.duration_mth(t) == x.limit_mth() - 1,
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
    policy month passed as ``t`` (R1a), as a moratorium, a cessation or a payment count
    read on ``t`` would be.  The frame comparisons read SEC row ``t`` against S row
    ``t + d`` in every column of ``result_cf`` and every column of ``result_pols`` both
    reports hold, and fail frames that end apart.  The cell comparison then evaluates every
    cell of S's but :data:`SPLICE_EXEMPT`, at every argument S cached inside its own frame
    from month ``d`` on, moved onto SEC's clock: the counts on both strands, the paid-up
    cover, the premiums paid, the cover and premium, the benefits, the payments made, the
    rates and the crossover, a policy month, among them.  Each compares to 1e-9 relative
    with no absolute floor, but the roll-forward's residual, which keeps the floor of 1e-9
    (:func:`_compare`).  An S cell this model lacked would fail it.

    The rows past the first conversion are the ones that see the paid-up strand carried in
    at the wrong instant, and the rows past the crossover the premiums paid, which the
    stress reads in every month.  The row is then recorded for the rules test and released
    (:func:`_settle`).
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

    SEC rows ``k ..`` are S rows ``0 ..``, ending together at the limiting age, in
    ``result_cf`` and in every column of ``result_pols`` S's has, and every cell of S's but
    :data:`FUTURE_EXEMPT` agrees at every argument S cached inside its own frame, moved
    ``k`` later.  Each compares as the splice compares, with no absolute floor but on the
    residual (:func:`_compare`).  An S cell this model lacked would fail it.  Before issue
    every column of ``result_cf`` and ``result_pols`` is an exact zero, and the policies
    arrive in month ``k`` as new business.

    The last assertions are R1 and D4's base rule made testable.  After the reports, no read
    keyed by an attained age or a policy year, and no monthly rate, has been evaluated at a
    month before issue (:data:`KEYED_READS`); the annual rates, columns of ``result_pols``,
    are 0.0 there without a read.  A count recursion based at ``t == 0`` rather than at
    ``t_entry()``, or a decrement count that evaluates its rate before asking whether the
    month is in cover, still gives the right numbers.  This is the only test that sees the
    first, and the guard test sees the second too.

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
                 for name in KEYED_READS}
        assert not any(early.values()), f"read before issue: {early}"
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
    first (:func:`_rule_breaches`), :func:`crossover_mth` among the cells it calls:

    * R1: no cell holds a negative argument.  modelx evaluates one without complaint, and
      a compiled cache raises ``IndexError`` below 0 (USLIB-SEC-PLAN.md F4).  A policy
      month turned into ``t`` by subtracting ``duration_mth_init()`` (R1a) goes negative
      on a point in force past it, as the crossover's search over the policy months would.
    * R1's look-back stops at ``t_entry()``: no cell evaluated at a month from
      ``t_entry()`` on read a month before it.  On a point issued later a recursion based
      at ``t == 0`` reads the pre-issue zeros, so no number shows it and no argument goes
      negative.  The increases counted from ``t_entry()`` read it, the month of entry, and
      no month before.
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


# How deep a cold call may run beyond its chain (D5): the cells above the chain and those
# below it, the first month's rates and Data's first reads of its tables.  WOL runs four
# chains, the full-cover count, the paid-up count, the paid-up cover and the premiums
# paid; the cover, the premium and the improvement are closed forms.  One cell a month, as
# the in-force step left them, a cold net_cf at the longest cover needed 292 KiB of C stack
# compiled, past the 256 KiB the C step allows itself (UKLIB-SEC-PLAN.md §6.6, *Record --
# M10*, *Carried into M12 and M14*), so each chain is blocked by policy year, its year's
# opening a cell that walks the year before (OPENINGS), and its chain is one cell a month
# within the year and two cells a year before it (_chain).  Measured at M6, on the blocked
# chains at the contract's longest cover, issued at 18 now and 120 months on, its limiting
# age at the contract's largest, 121, with the stress and improvement on, each head cold
# in the last month on a read of its own: the chain is 215 cells on every shape, and the
# count's head runs 8 beyond it, the premiums paid 5, net_cf 11 or 12, the roll-forward's
# residual 12, the claims total 13, the paid-up cover 23, and the paid-up count and its
# deaths' claims 24, the most, at the foot of the paid-up chain, where the first walked
# month's conversions read the full-cover count, its rates, the premiums paid and the cover
# cold.  So each head's bound is its own measured overhead, rather than Term's 16, which
# the paid-up chains' walk passes, or the paid-up count's 24 for every head, which a count
# chain of two cells a month within its year, 11 cells more in the frame's last month,
# would meet: any chain left one cell a month runs about a thousand beyond its bound, one
# of two cells a month within its year 11, and a year's opening that walks from the year's
# second month a cell more a year.
CHAIN_OVERHEAD = {("net_cf", None): 12, ("pols_if_at", "BEF_NB"): 8, ("prem_cum_pp", None): 5,
                  ("check_pols_roll_fwd_resid", None): 12, ("pols_pu", None): 24,
                  ("pu_benefit", None): 23, ("claims", "DEATH_PU"): 24, ("claims", "ALL"): 13}

# The contract's longest cover (held by proj_len()): issued at issue_age_min, 18, to the
# largest limiting age the contract allows, omega_age_max, 121, the shipped table's last age
# plus one, 1,236 months, the same on every shape.  LONGEST_REFS sets omega_age there,
# beside the switches that ship off, for each test of the longest cover.
YOUNGEST = 18
OMEGA_MAX = 121
LONGEST_REFS = {**SWITCHED_ON, "omega_age": OMEGA_MAX}

# The chains of the model and the cells that head them, called cold in the last month of
# the frame, each on a read of its own: (cell, the timing or kind it takes, or None).  The
# count, the premiums paid, the roll-forward's residual and net_cf over them, the deepest
# call a projection makes, on every shape; and on the paid-up shape its two chains, the
# paid-up deaths' claims and the claims total.
CHAIN_HEADS = (("net_cf", None), ("pols_if_at", "BEF_NB"), ("prem_cum_pp", None),
               ("check_pols_roll_fwd_resid", None))
PAID_UP_HEADS = (("pols_pu", None), ("pu_benefit", None), ("claims", "DEATH_PU"),
                 ("claims", "ALL"))

# The shapes the chains run at their longest cover on, by the S point whose twin each is,
# with their heads: the anchor cell, level; the paid-up point, its strand's two chains
# among them; the RPI point, its increases in every year; and the underwritten increasing
# point, paying for life.
CHAIN_SHAPES = {1: CHAIN_HEADS, 3: CHAIN_HEADS + PAID_UP_HEADS, 4: CHAIN_HEADS,
                6: CHAIN_HEADS}


def _chain(p, t):
    """The cells a cold read of month ``t`` of ``p`` runs through, past the first: one a
    month back to its policy year's first month, or to ``t_entry()`` in the year that holds
    it, and two a policy year before that, back to ``t_entry()``'s year, where the four
    chains are blocked by policy year (:data:`OPENINGS`)."""
    first = max(p.t_entry(), t - p.duration_mth(t) % 12)
    return (t - first) + 2 * (p.policy_year(t) - p.policy_year(p.t_entry()))


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


def _longest_cover(tmp_path, shapes):
    """A copy whose table holds the twins of S points ``shapes``, each one of
    :data:`CHAIN_SHAPES`, at the longest cover, issued now and 120 months on, and each
    row's frame, ``t_entry()`` and heads, under :data:`LONGEST_REFS`.

    Each S point's twin, issued at 18, 1,236 months from the contract's largest limiting
    age, 121, issued at the valuation date and 120 months after it, the shipped
    ``future_horizon_mth``: frames of 1,236 and 1,356 months, whose chains stop at
    ``t_entry()``.  The shipped tables serve every age from 18 to 120.
    """
    committed = _committed()
    labels = [_label(committed, "twin", shape, 0) for shape in shapes]
    heads = [CHAIN_SHAPES[shape] for shape in shapes]
    top = committed.index.max()
    rows = committed.loc[labels + labels].assign(entry_age=YOUNGEST)
    later = list(range(top + 1, top + 1 + len(labels)))
    rows = rows.set_axis(labels + later).rename_axis("point_id")
    rows = _set("duration_mth", later, -120)(rows)
    cover = 12 * (OMEGA_MAX - YOUNGEST)
    frames = ([(label, cover, 0, h) for label, h in zip(labels, heads)]
              + [(label, cover + 120, 120, h) for label, h in zip(later, heads)])
    return _sec_inputs(tmp_path, rows), frames


# modelx warns as its stack trace starts and stops, which is all the test does with it.
@pytest.mark.filterwarnings("ignore:call stack trace:UserWarning")
@pytest.mark.parametrize("shape", [pytest.param(p, id=f"point{p}",
                                                marks=() if p == 3 else FULL_ONLY)
                                   for p in CHAIN_SHAPES])
def test_every_chain_runs_one_cell_a_month_from_a_cold_start(tmp_path, shape):
    """Called cold, each chain runs one cell a month within its policy year, and two cells a
    year before it, back to ``t_entry()``, no more (D5, as blocked at M6).

    No number shows how deep a chain runs, and a compiled model runs it on the C stack, so
    a chain of two cells a month, which gives the same numbers, needs twice the stack on
    every platform (F7); ``WOL_UK_S``'s chains each run one cell a month, but its count
    reaches back to issue.  One cell a month, this model's ran 1,236 cells at the longest
    cover, and compiled the count's needed 292 KiB of C stack, past what the C step allows
    (UKLIB-SEC-PLAN.md §6.4, *Record -- M6*).  So the four chains are blocked by policy
    year, each year's opening a cell that walks the year before in ascending order
    (:data:`OPENINGS`).  On a model just read, nothing is cached, so modelx's stack trace
    counts how deep a call runs, against that chain (:func:`_chain`) and the head's own
    measured overhead more, :data:`CHAIN_OVERHEAD`, with modelx's recursion limit where the
    module leaves it: each head of :data:`CHAIN_SHAPES` in the last month of the frame, each
    on a read of its own, with :data:`LONGEST_REFS` set, so that the stress reads the
    premiums paid in every month, improvement moves the rates and the limiting age is the
    contract's largest.  On each shape at the contract's longest cover, 1,236 months from
    issue age 18, issued now and 120 months on (:func:`_longest_cover`), each row's frame
    asserted first, as §7.5's *Record — M5* and M14's carried rule ask, and M1's that every
    chain runs at its own shape's longest cover.  The paid-up shape, which runs all four
    chains, runs by default, and the others on the full grid.  A chain left one cell a month
    runs about a thousand cells past its bound, and one walked descending the same; a chain
    of two cells a month within its year runs 11 past it in the frame's last month, the
    year's twelfth, and a year's opening that walks from the year's second month a cell more
    a year.
    """
    folder, frames = _longest_cover(tmp_path, (shape,))
    found = []
    for label, months, entry, heads in frames:
        for cell, timing in heads:
            fresh = mx.read_model(folder, name=_name("cold"))
            try:
                for ref, value in LONGEST_REFS.items():
                    setattr(fresh.Projection, ref, value)
                p = _point(fresh, label)
                last = months - 1
                args = (last,) if timing is None else (last, _code(p, timing))
                depth = _cold_depth(p, cell, args)
                assert p.proj_len() == months and p.t_entry() == entry, label
                chain = _chain(p, last)
                bound = CHAIN_OVERHEAD[cell, timing]
                if not chain <= depth <= chain + bound:
                    found.append(f"point {label}: {cell}{args} cold runs {depth} cells "
                                 f"deep, where its chain back to t_entry() {entry}, one "
                                 f"cell a month within its policy year and two a year "
                                 f"before it, is {chain} and {bound} more are allowed")
            finally:
                fresh.close()
    assert not found, found


def test_each_chain_opens_a_policy_year_with_the_year_before_s_close(sec_model):
    """Each blocked chain opens a policy year with the value the year before closes on, bit
    for bit, and reads it there alone (§6.4, *Record -- M6*).

    Each of the four chains runs one cell a month within a policy year, the depth test
    above shows, and in a year's first month after ``t_entry()`` reads the year's opening
    (:data:`OPENINGS`), which walks the year before.  So the forms must give one number:
    on every committed point, in every such month in cover, the full-cover count carried
    in is the month before's ``BEF_NB`` count plus its new business, less its deaths and
    would-be lapses, the product ``BEF_NB`` forms within a year; the paid-up count is the
    month before's survivors and conversions; the paid-up cover is the month before's
    surviving cover and the cover its conversions bring; and the premiums paid carried in
    are the month before's, each as the monthly cells compute it, bit for bit, whatever the
    opening's walk.  And as modelx's dependency graph records them, each chain's precedents
    in such a month are its opening and none of its own months, and in every other month
    after ``t_entry()`` the month before and no opening.
    """
    table = sec_model.Data.model_point_table()
    openings, middles = 0, 0
    for key, point_id in zip(point_keys(sec_model), table.index):
        p = projection(sec_model, key)
        bef_nb, paid_up = _code(p, "BEF_NB"), _code(p, "PAID_UP")
        for t in range(p.t_entry() + 1, p.proj_len()):
            s = t - 1
            if p.duration_mth(t) % 12 == 0:
                y, openings = p.policy_year(t), openings + 1
                closes = {
                    "pols_if_py": ((p.pols_if_at(s, bef_nb) + p.pols_new_biz(s))
                                   * (1.0 - p.mort_rate_mth(s))
                                   * (1.0 - p.lapse_rate_mth(s))),
                    "pols_pu_py": (p.pols_pu(s) * (1.0 - p.mort_rate_mth(s))
                                   + p.pols_convert(s)),
                    "pu_benefit_py": (p.pu_benefit(s) * (1.0 - p.mort_rate_mth(s))
                                      + p.pols_convert(s) * p.benefit_pp(s, paid_up)),
                    "prem_cum_pp_py": p.prem_cum_pp(s)}
                if not p.pu_variant():
                    del closes["pols_pu_py"], closes["pu_benefit_py"]
                for opening, close in closes.items():
                    got = p.cells[opening](y)
                    assert got.hex() == close.hex(), (point_id, opening, y, got, close)
                assert p.pols_if_at(t, bef_nb) == closes["pols_if_py"], (point_id, t)
                assert p.prem_cum_pp(t) == closes["prem_cum_pp_py"] + p.premium_pp(t)
                if p.pu_variant():
                    assert p.pols_pu(t) == closes["pols_pu_py"], (point_id, t)
                    assert p.pu_benefit(t) == closes["pu_benefit_py"], (point_id, t)
            else:
                middles += 1
            chains = [("pols_if_at", (t, bef_nb), "pols_if_py"),
                      ("prem_cum_pp", (t,), "prem_cum_pp_py")]
            if p.pu_variant():
                chains += [("pols_pu", (t,), "pols_pu_py"),
                           ("pu_benefit", (t,), "pu_benefit_py")]
            for cell, args, opening in chains:
                reads = {(n.obj.name, n.args) for n in p.cells[cell].preds(*args)}
                own = any(name == cell for name, _ in reads)
                opened = any(name == opening for name, _ in reads)
                if p.duration_mth(t) % 12 == 0:
                    assert opened and not own, (point_id, cell, t, reads)
                else:
                    assert own and not opened, (point_id, cell, t, reads)
    assert openings > 100 and middles > 1000, (openings, middles)


# The builtins that make text of what they are given, and the methods that make text of
# what they are called on, or join or format it (_text_faults).
TEXT_CALLS = frozenset({"str", "repr", "ascii", "format", "chr", "hex", "oct", "bin"})
TEXT_METHODS = frozenset({"format", "format_map", "join", "hex", "__str__", "__repr__",
                          "__format__", "__mod__", "__add__"})


def _is_text(node):
    """Whether ``node`` is text by its form: a string constant, an f-string, a call of
    :data:`TEXT_CALLS` or :data:`TEXT_METHODS`, or a ``+`` or ``%`` with text either side."""
    if isinstance(node, ast.Constant):
        return isinstance(node.value, str)
    if isinstance(node, ast.JoinedStr):
        return True
    if isinstance(node, ast.Call):
        func = node.func
        return ((isinstance(func, ast.Name) and func.id in TEXT_CALLS)
                or (isinstance(func, ast.Attribute) and func.attr in TEXT_METHODS))
    if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Add, ast.Mod)):
        return _is_text(node.left) or _is_text(node.right)
    return False


def _text_faults(cells):
    """Each place ``cells``' formula builds text, or raises other than a constant, as
    ``(line, what)``.

    Every ``raise`` must call one exception on one string constant, ``raise
    ValueError("invalid timing")``, nothing else: a message built anywhere, at the raise
    or into a local before it, is code in the cell's frame.  And nothing else in the
    formula may build text, the docstring and those constants apart: no f-string, no other
    string constant, no call of :data:`TEXT_CALLS` or :data:`TEXT_METHODS` and no name of
    the first, and no ``+`` or ``%`` with text either side (:func:`_is_text`).  A ``%``
    or ``+`` on numbers, ``duration_mth(t) % 12``, builds none.
    """
    func = ast.parse(cells.formula.source).body[0]
    body = func.body
    doc = (body[0].value if body and isinstance(body[0], ast.Expr)
           and isinstance(body[0].value, ast.Constant) and isinstance(body[0].value.value, str)
           else None)
    raised, faults = set(), []
    for node in ast.walk(func):
        if isinstance(node, ast.Raise):
            exc = node.exc
            if (isinstance(exc, ast.Call) and not exc.keywords and len(exc.args) == 1
                    and isinstance(exc.args[0], ast.Constant)
                    and isinstance(exc.args[0].value, str)):
                raised.add(exc.args[0])
            else:
                faults.append((node.lineno, "raises other than one string constant"))
    for node in ast.walk(func):
        if node is doc or node in raised:
            continue
        if isinstance(node, ast.JoinedStr):
            faults.append((node.lineno, "an f-string"))
        elif isinstance(node, ast.Constant) and isinstance(node.value, str):
            faults.append((node.lineno, f"the text {node.value!r}"))
        elif isinstance(node, ast.Name) and node.id in TEXT_CALLS:
            faults.append((node.lineno, f"{node.id}, which makes text"))
        elif (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                and node.func.attr in TEXT_METHODS):
            faults.append((node.lineno, f".{node.func.attr}(), which makes text"))
        elif (isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Add, ast.Mod))
                and (_is_text(node.left) or _is_text(node.right))):
            faults.append((node.lineno, "a + or % on text"))
    return sorted(set(faults))


def _deepest_stack(proj, cell, args):
    """The cells on modelx's stack where ``cell(*args)`` on ``proj`` runs deepest, from the
    call down, each by name."""
    mx.start_stacktrace(maxlen=None)
    try:
        proj.cells[cell](*args)
        trace = mx.get_stacktrace(summarize=False)
    finally:
        mx.stop_stacktrace()
    stack, deepest = [], []
    for event, *rest in trace:
        if event == "ENTER":
            text = next(x for x in rest if isinstance(x, str))
            stack.append(re.search(r"\.(\w+)\(", text).group(1))
            if len(stack) > len(deepest):
                deepest = list(stack)
        else:
            stack.pop()
    return deepest


# The heads the chain-text test calls cold, each with the shapes it runs on: every head of
# CHAIN_SHAPES but the claims total, which holds claims itself twice, the total over its
# full-cover kind, at the top of any path, whatever the cover: no chain recurses through
# it, and its refusal, of a total past the floats, names the kind by its code.
TEXT_HEADS = tuple(head for head in CHAIN_HEADS + PAID_UP_HEADS if head != ("claims", "ALL"))


# modelx warns as its stack trace starts and stops, which is all the test does with it.
@pytest.mark.filterwarnings("ignore:call stack trace:UserWarning")
def test_no_cell_a_chain_recurses_through_formats_a_refusal(tmp_path):
    """No cell a cold call's deepest path holds more than once builds text (M10).

    A compiled cell's C frame holds the code that formats each of its messages, whether a
    run reaches it or not, and a chain holds a frame of each cell it recurses through at
    each level.  On CI's Ubuntu runner, a refusal formatted inside ``Term_UK_SEC``'s
    recursive waiver cell had its cold call at the longest cover need 512 KiB to 1 MiB,
    and 256 to 384 once the cell held none (K12).  So every refusal of this model whose
    message is formatted sits in a cell no chain recurses through: ``prem_cum_pp`` and
    ``pu_benefit``, two of the four chains, call ``prem_cum_pp_refusal`` and
    ``pu_benefit_refusal`` on their error paths alone.  On a model just read, at the
    longest cover of the paid-up point, which runs all four chains, issued now, each head of
    :data:`TEXT_HEADS` is called cold in the last month, under modelx's stack trace, with
    :data:`LONGEST_REFS` set, and the cells on the stack at its deepest point are counted.
    A cell held there twice or more is one the chain recurses through, at every month or
    every year.  None of them may build text anywhere in its formula, at a raise, in an
    error branch or into a local, nor raise other than one exception on one string
    constant (:func:`_text_faults`): the frame holds a message's code whether or not its
    branch runs.  A cell held once costs its frame once, as ``mort_rate``, whose refusal
    names an age outside the table, does at the chain's foot.  Each chain's monthly cell
    and its year's opening must be among the cells checked, every cell the four blocked
    chains recurse through, or the test would check less than it says.
    """
    folder, frames = _longest_cover(tmp_path, (3,))
    found, checked = [], set()
    for label, months, entry, _ in frames:
        if entry != 0:
            continue
        for cell, code in TEXT_HEADS:
            fresh = mx.read_model(folder, name=_name("deepest"))
            try:
                for ref, value in LONGEST_REFS.items():
                    setattr(fresh.Projection, ref, value)
                p = _point(fresh, label)
                last = months - 1
                args = (last,) if code is None else (last, _code(p, code))
                stack = _deepest_stack(p, cell, args)
                assert len(stack) > 200, (label, cell, len(stack))
                held = {name for name in stack if stack.count(name) > 1}
                checked |= held
                for name in sorted(held):
                    faults = _text_faults(p.cells[name])
                    if faults:
                        found.append(f"point {label}: {cell}{args}: {name}, held "
                                     f"{stack.count(name)} times on the deepest path, "
                                     f"builds text: {faults}")
            finally:
                fresh.close()
    assert {"pols_if_at", "pols_pu", "pu_benefit", "prem_cum_pp", *OPENINGS} <= checked, (
        sorted(checked))
    assert not found, found


# ---------------------------------------------------------------------------
# T4 -- the count algebra
#
# BEF_DECR == BEF_NB + pols_new_biz, at every t of every point, is a convention
# (test_new_business_joins_the_count_before_decrements), and is not repeated here.


def test_the_counts_roll_forward_on_both_strands(sec_model):
    """Each strand's count leaves month t by its own outflows, and conversions move
    policies between them.

    On every committed point and at every ``t`` of its frame but the last, to 1e-12: the
    full-cover count weighting month ``t``, ``pols_if_at(t, BEF_DECR)``, less the count it
    carries into ``t + 1``, ``pols_if_at(t + 1, BEF_NB)``, is its deaths, its terminating
    lapses and its conversions to paid-up; the paid-up count, ``pols_pu(t)``, less
    ``pols_pu(t + 1)``, is its deaths less the conversions it takes in.  In every month the
    two together, ``pols_all``, less what they carry into ``t + 1`` before its new business,
    is the deaths on both strands, the terminating lapses and the truncation residual,
    which in the last month before the limiting age takes every survivor, a conversion of
    that month among them.  And the notes' end-of-month count, ``pols_if_at(t,
    AFT_DECR)``, is exactly the count carried into the next month before its new business.

    ``result_pols()`` sets the same movement out row by row, in :data:`RESULT_POLS`'s
    columns, indexed by ``t`` over the frame: ``pols_if`` at ``t + 1`` is ``pols_if`` less
    its outflows at ``t``, plus the new business of ``t + 1``, and ``pols_pu`` at ``t + 1``
    is ``pols_pu`` less its deaths plus the conversions, row 0 opening from
    ``pols_if_init()`` and ``pols_pu_init()``.
    """
    table = sec_model.Data.model_point_table()
    for key, point_id in zip(point_keys(sec_model), table.index):
        p = projection(sec_model, key)
        bef_nb, bef_decr, aft = (_code(p, c) for c in ("BEF_NB", "BEF_DECR", "AFT_DECR"))
        last = p.proj_len() - 1
        for t in range(p.proj_len()):
            carried = p.pols_if_at(t + 1, bef_nb)
            assert p.pols_if_at(t, aft) == carried, (point_id, t)
            out = (p.pols_death(t) + p.pols_death_pu(t) + p.pols_lapse(t)
                   + p.pols_maturity(t))
            moved = p.pols_all(t) - (carried + p.pols_pu(t + 1))
            assert moved == pytest.approx(out, abs=1e-12), (point_id, t)
            if t == last:
                continue
            full = p.pols_death(t) + p.pols_lapse(t) + p.pols_convert(t)
            assert p.pols_if_at(t, bef_decr) - carried == pytest.approx(full, abs=1e-12), (
                point_id, t)
            paid_up = p.pols_death_pu(t) - p.pols_convert(t)
            assert p.pols_pu(t) - p.pols_pu(t + 1) == pytest.approx(paid_up, abs=1e-12), (
                point_id, t)
        pols = p.result_pols()
        assert list(pols.columns) == RESULT_POLS, point_id
        assert pols.index.name == "t" and list(pols.index) == list(range(p.proj_len()))
        full = (pols["pols_if"] - pols[["pols_death", "pols_lapse", "pols_convert"]]
                .sum(axis=1)).shift(1)
        expected = full.fillna(p.pols_if_init()) + pols["pols_new_biz"]
        assert ((pols["pols_if"] - expected).abs() <= 1e-12).all(), point_id
        paid_up = (pols["pols_pu"] - pols["pols_death_pu"] + pols["pols_convert"]).shift(1)
        expected = paid_up.fillna(p.pols_pu_init())
        assert ((pols["pols_pu"] - expected).abs() <= 1e-12).all(), point_id


def test_result_pols_is_s_report_with_the_new_business_beside_it(sec_model, s_model):
    """``result_pols()`` is S's, column for column, with three columns added (D5).

    T1 skips the report as a whole, because its frame has columns S's lacks (the spec's
    exempt), so it is compared here, on every twin, each issued at the valuation date, at
    offset 0.  The SEC report is S's columns in S's order with ``pols_new_biz`` second, the
    paid-up deaths after the full-cover ones and the truncation residual after the
    conversions; every column S's report has agrees, to 1e-9, frames ending together, and
    ``pols_new_biz`` holds the count in the issue month and 0 in every other.  The counts
    and rates carry no inflation, so the shipped assumptions serve.
    """
    table = sec_model.Data.model_point_table()
    twins = table.index[table["row_kind"] == "twin"].tolist()
    assert twins == sorted(s_model.Data.model_point_table().index)
    for point_id in twins:
        p = _point(sec_model, point_id)
        mine, theirs = p.result_pols(), _point(s_model, point_id).result_pols()
        assert [c for c in mine.columns if c in theirs.columns] == list(theirs.columns)
        assert [c for c in mine.columns if c not in theirs.columns] == [
            "pols_new_biz", "pols_death_pu", "pols_maturity"], point_id
        assert list(mine.columns)[:2] == ["pols_if", "pols_new_biz"]
        month = int(table.at[point_id, "source_mth"])
        assert frame_mismatches(theirs, mine, t_offset=month) == [], point_id
        issue = -int(table.at[point_id, "duration_mth"])
        assert list(mine["pols_new_biz"]) == [
            p.policy_count() if t == issue else 0.0 for t in mine.index], point_id


# What T4 multiplies the counts by: not a whole number, because a count of policies need
# not be one, so that a flow which read the count as whole policies would not follow it.
COUNT_FACTOR = 2.5


@pytest.mark.parametrize("grid", GRIDS)
def test_scaling_the_counts_scales_every_flow_and_no_per_policy_value(tmp_path, grid):
    """The counts are the weights: 2.5 times both, 2.5 times every flow, the same per policy.

    The committed table, and a copy with every ``policy_count`` and every ``pols_pu_init``
    multiplied by :data:`COUNT_FACTOR` together, are each read with :data:`SWITCHED_ON` set
    before either computes anything: every assumption that ships at zero, on, so that every
    flow is nonzero on some point, the stress moves the lapses and the conversions past the
    crossover, and improvement moves the rates.  On every point ``result_cf`` and the counts
    of ``result_pols`` are 2.5 times the committed table's, element by element, to 1e-12
    relative: a scaled count is a computed float, which may come back from the CSV within
    two ulps (``uk_sec_support``'s module docstring).  ``result_pols``'s per-policy columns
    are the committed table's exactly.  So is every other cell of :data:`COUNTED`, at every
    argument the sweep of the committed table's point cached: the counts at each timing and
    the claims of each kind, which no report shows, among them, and the roll-forward's
    residual, a rounding about 0 on that many policies, to the residual's floor of 1e-9.
    And every cell outside :data:`COUNTED` (the premiums paid, the cover, the premium, the
    benefits, the payments made, the rates, both clocks, the flags) agrees bit for bit at
    every argument that sweep cached.  So a flow that dropped a count, or read it as whole
    policies, which a table of counts of 1 hides from every comparison with S and a count
    doubled hides here, fails (USLIB-SEC-PLAN.md §5.2, T4, precised at M11).  Each counted
    cell but the residual is nonzero on some point, the paid-up ones on the committed
    paid-up rows.  A paid-up flow weighted by the full-cover count scales with both counts
    alike, so this test cannot see it: the month-on restatement, which moves one count and
    not the other, does.

    The default run takes :data:`CORE_POINTS`, among which every counted cell is nonzero,
    and the full grid the other committed points.
    """
    table = _committed()
    base = mx.read_model(_sec_inputs(tmp_path / "base", table), name=_name("counted"))
    scaled = mx.read_model(_sec_inputs(tmp_path / "scaled", table.assign(
        policy_count=COUNT_FACTOR * table["policy_count"],
        pols_pu_init=COUNT_FACTOR * table["pols_pu_init"])), name=_name("scaled"))
    reports = ("result_cf", "result_pols")
    counted = sorted(COUNTED - set(reports))
    nonzero = set()
    try:
        for model in (base, scaled):
            for ref, value in SWITCHED_ON.items():
                setattr(model.Projection, ref, value)
        for key, scaled_key, label in zip(point_keys(base), point_keys(scaled), table.index):
            if not _on_grid(grid, label):
                continue
            one, many = projection(base, key), projection(scaled, scaled_key)
            sweep(one)
            for report in reports:
                b, d = one.cells[report](), many.cells[report]()
                assert d.index.equals(b.index) and list(d.columns) == list(b.columns)
                flows = [c for c in b.columns if c not in PER_POLICY_POLS]
                want = COUNT_FACTOR * b[flows]
                bad = ((d[flows] - want).abs() > 1e-12 * want.abs()).any()
                assert not bad.any(), (key, report, list(bad[bad].index))
                fixed = [c for c in b.columns if c in PER_POLICY_POLS]
                assert d[fixed].equals(b[fixed]), (key, report)
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
    if grid == "core":
        want = set(counted) - RESIDUALS
        assert want <= nonzero, f"0 on every core point: {sorted(want - nonzero)}"


def test_a_point_restated_a_month_on_continues_its_own_flows(tmp_path):
    """The counts a point carries into a month are the counts that weight its flows (T4).

    Scaling every count alike, as the test above does, cannot see a flow weighted by the
    count a point opened with, ``policy_count()`` or ``pols_pu_init()``, rather than the
    count in force in its month: both move by the same factor.  So each point in force on
    the committed table is restated a month on, opened with what this model carries into
    its month 1: the full-cover count, ``pols_if_at(1, "BEF_NB")``; the paid-up count,
    ``pols_pu(1)``, and its cover per paid-up policy, ``pu_benefit(1) / pols_pu(1)``; the
    premiums paid, ``prem_cum_pp(0)``; the cover and the premium before month 1's events,
    ``cover_pp(0)`` and ``premium_pp(0)``, or once the premiums have ceased the last one
    paid; and the crossover, if it fell in month 0 or before.  The
    restatement must continue the point's own frames, its row ``t`` the point's row
    ``t + 1``, in ``result_cf`` and ``result_pols``, every flow among them, to 1e-9
    relative, floored at 1e-9 for what a state read back from the CSV an ulp off moves
    about 0.  The point valued in its first policy year continues its commission.  Both
    models run at an inflation rate of 0, set on each as it is read (K7): the restatement
    moves the valuation date a month on, and expense inflation, on the valuation clock,
    would step a month apart by design (D7), as improvement would, which ships at 0.  The
    restatement also shows the opening state complete on this model's own states, as the
    splice shows it on S's.
    """
    table = _committed()
    model = mx.read_model(_sec_inputs(tmp_path / "base", table), name=_name("month_on"))
    model.Projection.inflation_rate = 0.0
    rows, pairs = [], []
    try:
        top = table.index.max()
        for label in table.index[table["duration_mth"] > 0]:
            p = _point(model, label)
            if p.proj_len() < 2:
                continue
            cessation, d = p.cessation_mths(), p.duration_mth_init()
            crossover = p.crossover_mth()
            premium = (p.premium_pp(0) if cessation <= 0 or d < cessation
                       else p.premium_pp_init())
            paid_up = p.pols_pu(1)
            top += 1
            row = table.loc[[label]].assign(
                duration_mth=p.duration_mth(1),
                policy_count=p.pols_if_at(1, _code(p, "BEF_NB")),
                pols_pu_init=paid_up,
                pu_benefit_pp_init=p.pu_benefit(1) / paid_up if paid_up > 0 else 0.0,
                prem_cum_pp_init=p.prem_cum_pp(0), cover_pp_init=p.cover_pp(0),
                premium_pp_init=premium,
                crossover_mth_init=crossover if 0 <= crossover <= d else -1)
            row.index = pd.Index([top], name="point_id")
            rows.append(row)
            pairs.append((label, top))
        frames = {label: {report: _point(model, label).cells[report]()
                          for report in ("result_cf", "result_pols")}
                  for label, _ in pairs}
    finally:
        model.close()
    first_year = [label for label, _ in pairs
                  if (frames[label]["result_cf"]["commissions"] > 0.0).any()]
    assert first_year, "no restated point pays commission"
    restated = mx.read_model(_sec_inputs(tmp_path / "on", pd.concat([table, *rows])),
                             name=_name("month_on"))
    restated.Projection.inflation_rate = 0.0
    found = []
    try:
        for label, moved in pairs:
            p = _point(restated, moved)
            for report, frame in frames[label].items():
                found += [f"point {label} restated as {moved}, {report}: {line}"
                          for line in frame_mismatches(frame, p.cells[report](),
                                                       t_offset=1)]
    finally:
        restated.close()
    assert not found, found[:20]


@pytest.mark.parametrize("grid", GRIDS)
def test_the_roll_forward_closes_on_ten_million_policies(tmp_path, grid):
    """``check_pols_roll_fwd`` scales its tolerance with the policies on the books, and
    closes at 1e7.

    A residual is rounding on that many policies, so the check holds it to 1e-10 times
    ``max(policy_count() + pols_pu_init(), 1)``, where its tolerance unscaled would be
    1e-10: at the counts the other tests use, one policy or less, the two are one.
    ``WOL_UK_S`` scales by ``pols_if_init()``, which here is 0 on a point issued at the
    valuation date, the count entering as new business, and which leaves out the paid-up
    strand, whose policies the residual rounds on too.  So every committed point is
    projected from a copy where each counts ten million policies on each strand it holds:
    the check closes on each, and the largest residual on every point exceeds the unscaled
    1e-10, so the scaling is what closes it (USLIB-SEC-PLAN.md §5.2, T4, precised at M10).
    The point paid-up entirely, whose ``policy_count`` is 0, closes on its paid-up count
    alone, which a tolerance scaled by the full-cover count would leave at 1e-10.  At a
    million policies the largest residuals are about 1e-10, and the paid-up point's
    5.7e-11, which an unscaled tolerance would pass.

    The default run takes :data:`CORE_POINTS`, the point paid-up entirely among them, and
    the full grid the other committed points.
    """
    table = _committed()
    table = table.assign(policy_count=1e7 * (table["policy_count"] > 0),
                         pols_pu_init=1e7 * (table["pols_pu_init"] > 0))
    model = mx.read_model(_sec_inputs(tmp_path, table), name=_name("ten_million"))
    least, paid_up_only = math.inf, 0.0
    try:
        for key, point_id in zip(point_keys(model), table.index):
            if not _on_grid(grid, point_id):
                continue
            p = projection(model, key)
            assert p.check_pols_roll_fwd() and p.check_truncation(), point_id
            largest = max(abs(p.check_pols_roll_fwd_resid(t)) for t in range(p.proj_len()))
            least = min(least, largest)
            if p.policy_count() == 0.0 and p.pols_pu_init() > 0.0:
                paid_up_only = max(paid_up_only, largest)
            _release(model, key)
    finally:
        model.close()
    assert least > 1e-10, least
    if grid == "core":
        assert paid_up_only > 1e-10, paid_up_only


# ---------------------------------------------------------------------------
# T5 -- validation
#
# Each malformed table is the committed one with one fault.  The checks run over the whole
# table as it is read, in Data, and the message names the file it read and the column or
# every point at fault.  A blank cell reads as NaN, and so does a text cell once the checks
# coerce the column to numbers, so each is refused as a count, a duration or a state that
# is not a number.  The repeated point_id holds another policy under the same label, as a
# bad extract would, so that the check must look at the labels and not at whole rows.  The
# point_ids are the committed table's: 1 to 7 the twins of S's points; 8, the anchor cell
# at 6, inside its moratorium; 9, the anchor cell at 166; 10, the paid-up point at 200; 11,
# the RPI point at 186; 12, the underwritten increasing point at 12; 13, the male smoker at
# 300; 14, the RPI point issued 13 months on; 15, the RPI point at 120 under an RPI of 5%;
# 16, the underwritten increasing point at 120 under a take-up of a half; 17, the paid-up
# point at 180 paid-up entirely.  A {file} in a message is the table's filename: every case
# is read by one model, from a file of its own (the malformed fixture).


def _drop(column):
    return lambda table: table.drop(columns=column)


_NOT_YET = "on a policy not yet in force, duration_mth 0 or less; it is not at point_id"
_FIRST_YEAR = ("on a policy in force 12 months or fewer, whose columns are its first "
               "policy year's, the first anniversary's increase being the projection's; it "
               "is not at point_id")
_EARLIEST = ("before the first policy month a converted policy can be in force at, half "
             "of cessation_months, rounded up; it is not at point_id")
_CROSS_WHOLE = ("{file}: crossover_mth_init must be a whole number of months, -1 or more, "
                "below 2**53; it is not at point_id ")
_CROSS_MONTH = ("{file}: crossover_mth_init must be -1, or a premium-paying policy month "
                "before the valuation date, below duration_mth and cessation_months; it is "
                "not at point_id ")
_CROSS_LEVEL = ("{file}: crossover_mth_init must be the month the contract puts the "
                "crossover in on a level point, the whole number of premiums the sum assured "
                "holds, to the cent; it is not at point_id ")
_PAID_LEVEL = ("{file}: prem_cum_pp_init must be premium_mth times the premiums due, "
               "min(duration_mth, cessation_months), to the cent, on a level point; it is "
               "not at point_id [8]")
_PAID_ESCALATING = ("{file}: prem_cum_pp_init must lie between premium_mth and "
                    "premium_pp_init times the premiums due, min(duration_mth, "
                    "cessation_months), to the cent, on an escalating point; it is not at "
                    "point_id [11]")
_PU_COVER = ("{file}: pu_benefit_pp_init must lie between sum_assured times the payments a "
             "conversion needs, half of cessation_months rounded up, and cover_pp_init times "
             "the payments made, min(duration_mth, cessation_months), each over "
             "cessation_months, to the cent, where paid-up policies are in force; it is not "
             "at point_id [10]")

MALFORMED = [
    ("a negative count", _set("policy_count", [8], -0.1),
     "{file}: policy_count must be a number, zero or more; it is not at point_id [8]"),
    ("a blank count", _set("policy_count", [9], float("nan")),
     "{file}: policy_count must be a number, zero or more; it is not at point_id [9]"),
    ("two bad counts", _set("policy_count", [8, 10], -1.0),
     "{file}: policy_count must be a number, zero or more; it is not at point_id [8, 10]"),
    ("a text count", _set("policy_count", [11], "abc"),
     "{file}: policy_count must be a number, zero or more; it is not at point_id [11]"),
    ("an infinite count", _set("policy_count", [11], float("inf")),
     "{file}: policy_count must be a number, zero or more; it is not at point_id [11]"),
    ("a fractional duration", _set("duration_mth", [9], 166.5),
     "{file}: duration_mth must be a whole number of months; it is not at point_id [9]"),
    ("a blank duration", _set("duration_mth", [14], float("nan")),
     "{file}: duration_mth must be a whole number of months; it is not at point_id [14]"),
    ("a text duration", _set("duration_mth", [11], "x4"),
     "{file}: duration_mth must be a whole number of months; it is not at point_id [11]"),
    # numpy casts a float past int64 to the least int64, a policy issued 2**63 months on,
    # without a word: the table refuses it first.
    ("a duration past int64", _set("duration_mth", [8], 1e19),
     "{file}: duration_mth must be below 2**53 months; it is not at point_id [8]"),
    ("durations of 2**53 months at two points", _set("duration_mth", [8, 10], 2.0 ** 53),
     "{file}: duration_mth must be below 2**53 months; it is not at point_id [8, 10]"),
    ("issued beyond the horizon", _set("duration_mth", [14], -121),
     "{file}: duration_mth must be -120 or more, a policy issued at most 120 months after "
     "the valuation date; it is not at point_id [14]"),
    *[(f"no {column} column", _drop(column), f"{{file}} has no {column} column")
      for column in ("policy_count", "duration_mth", *STATE)],
    ("a repeated point_id",
     lambda t: pd.concat([t, t.loc[[8]].assign(policy_id="WOL-900099")]),
     "{file}: point_id [8] appears more than once"),
    ("a negative paid-up count", _set("pols_pu_init", [10], -0.01),
     "{file}: pols_pu_init must be a number, zero or more; it is not at point_id [10]"),
    ("a blank paid-up count", _set("pols_pu_init", [17], float("nan")),
     "{file}: pols_pu_init must be a number, zero or more; it is not at point_id [17]"),
    ("an infinite paid-up count", _set("pols_pu_init", [10], float("inf")),
     "{file}: pols_pu_init must be a number, zero or more; it is not at point_id [10]"),
    ("a negative paid-up cover", _set("pu_benefit_pp_init", [10], -1.0),
     "{file}: pu_benefit_pp_init must be a number, zero or more; it is not at point_id "
     "[10]"),
    ("a text paid-up cover", _set("pu_benefit_pp_init", [17], "x"),
     "{file}: pu_benefit_pp_init must be a number, zero or more; it is not at point_id "
     "[17]"),
    ("negative premiums paid", _set("prem_cum_pp_init", [9], -30.0),
     "{file}: prem_cum_pp_init must be a number, zero or more; it is not at point_id [9]"),
    ("blank premiums paid", _set("prem_cum_pp_init", [13], float("nan")),
     "{file}: prem_cum_pp_init must be a number, zero or more; it is not at point_id [13]"),
    ("an infinite cover", _set("cover_pp_init", [11], float("inf")),
     "{file}: cover_pp_init must be a number, zero or more; it is not at point_id [11]"),
    ("a blank cover", _set("cover_pp_init", [12], float("nan")),
     "{file}: cover_pp_init must be a number, zero or more; it is not at point_id [12]"),
    ("a negative premium", _set("premium_pp_init", [15], -1.0),
     "{file}: premium_pp_init must be a number, zero or more; it is not at point_id [15]"),
    ("a text premium", _set("premium_pp_init", [16], "high"),
     "{file}: premium_pp_init must be a number, zero or more; it is not at point_id [16]"),
    ("a blank flag", _set("variant_paid_up", [3], float("nan")),
     "{file}: variant_paid_up must be True or False; it is not at point_id [3]"),
    ("a flag written yes", _set("variant_adb_2x", [2], "yes"),
     "{file}: variant_adb_2x must be True or False; it is not at point_id [2]"),
    ("a flag written 1", _set("variant_adb_2x", [1], 1),
     "{file}: variant_adb_2x must be True or False; it is not at point_id [1]"),
    ("an unknown cell", _set("cell", [1], "O60"),
     "{file}: cell must be O50 or UW; it is not at point_id [1]"),
    ("an unknown escalation", _set("escalation", [4], "indexed"),
     "{file}: escalation must be level or fixed_5pct or rpi; it is not at point_id [4]"),
    ("an unknown sex", _set("sex", [2], "X"),
     "{file}: sex must be M or F; it is not at point_id [2]"),
    ("term assurance's smoker code", _set("smoker", [3], "N"),
     "{file}: smoker must be NS or S; it is not at point_id [3]"),
    ("a blank entry age", _set("entry_age", [1], float("nan")),
     "{file}: entry_age must be a finite number; it is not at point_id [1]"),
    ("an infinite entry age", _set("entry_age", [5], float("inf")),
     "{file}: entry_age must be a finite number; it is not at point_id [5]"),
    ("a text entry age", _set("entry_age", [7], "x65"),
     "{file}: entry_age must be a finite number; it is not at point_id [7]"),
    # int64 holds 2**53 exactly but the floats about it inexactly, and numpy casts a float
    # past int64 to the least int64 without a word: the table refuses 2**53 and more, as a
    # float and as an int (the C step), and reads 2**53 - 1, which proj_len() then refuses
    # as an issue age at or past omega_age (NOT_ISSUED).
    ("an entry age of 2**53", _set("entry_age", [1], 2.0 ** 53),
     "{file}: entry_age must be below 2**53 in size; it is not at point_id [1]"),
    ("entry ages of 2**53, an int, at two points", _set("entry_age", [2, 3], 2 ** 53),
     "{file}: entry_age must be below 2**53 in size; it is not at point_id [2, 3]"),
    ("an entry age of -2**53", _set("entry_age", [4], -2.0 ** 53),
     "{file}: entry_age must be below 2**53 in size; it is not at point_id [4]"),
    ("a negative sum assured", _set("sum_assured", [1], -1.0),
     "{file}: sum_assured must be a number, zero or more; it is not at point_id [1]"),
    ("a text premium at issue", _set("premium_mth", [2], "30 pounds"),
     "{file}: premium_mth must be a number, zero or more; it is not at point_id [2]"),
    ("an infinite premium at issue", _set("premium_mth", [6], float("inf")),
     "{file}: premium_mth must be a number, zero or more; it is not at point_id [6]"),
    ("a fractional cessation", _set("cessation_months", [1], 240.5),
     "{file}: cessation_months must be a whole number of months, 0 or more, below 2**53; "
     "it is not at point_id [1]"),
    ("a negative cessation", _set("cessation_months", [5], -12),
     "{file}: cessation_months must be a whole number of months, 0 or more, below 2**53; "
     "it is not at point_id [5]"),
    ("a blank moratorium", _set("moratorium_months", [7], float("nan")),
     "{file}: moratorium_months must be a whole number of months, 0 or more, below 2**53; "
     "it is not at point_id [7]"),
    ("a moratorium of 2**53 months", _set("moratorium_months", [2], 2.0 ** 53),
     "{file}: moratorium_months must be a whole number of months, 0 or more, below 2**53; "
     "it is not at point_id [2]"),
    # The bound at 2**53 itself; 2**53 - 1 reads, and proj_len() refuses it as a cessation
    # past the limiting age (NOT_ISSUED).
    ("a cessation of 2**53 months", _set("cessation_months", [1], 2.0 ** 53),
     "{file}: cessation_months must be a whole number of months, 0 or more, below 2**53; "
     "it is not at point_id [1]"),
    ("the paid-up value without a cessation date", _set("cessation_months", [3], 0),
     "{file}: a pro-rata paid-up point must have a premium cessation date, "
     "cessation_months above 0, which the paid-up value is measured to; it is not at "
     "point_id [3]"),
    ("a paid-up count on new business", _set("pols_pu_init", [3], 0.1),
     f"{{file}}: pols_pu_init must be 0 {_NOT_YET} [3]"),
    ("a paid-up cover on future business", _set("pu_benefit_pp_init", [14], 2500.0),
     f"{{file}}: pu_benefit_pp_init must be 0 {_NOT_YET} [14]"),
    ("premiums paid on new business", _set("prem_cum_pp_init", [1], 30.0),
     f"{{file}}: prem_cum_pp_init must be 0 {_NOT_YET} [1]"),
    ("a cover on new business", _set("cover_pp_init", [4], 5150.0),
     f"{{file}}: cover_pp_init must be the sum assured {_NOT_YET} [4]"),
    ("a premium on future business", _set("premium_pp_init", [14], 31.35),
     f"{{file}}: premium_pp_init must be the premium at issue {_NOT_YET} [14]"),
    # No anniversary has passed in a policy's first twelve months: the RPI point at 186,
    # moved back into its first policy year with its increases, and the anchor cell inside
    # its moratorium given an increase.
    ("a cover in the first policy year", _set("duration_mth", [11], 11),
     f"{{file}}: cover_pp_init must be the sum assured {_FIRST_YEAR} [11]"),
    ("a premium in the first policy year", _set("premium_pp_init", [8], 31.0),
     f"{{file}}: premium_pp_init must be the premium at issue {_FIRST_YEAR} [8]"),
    ("a level cover moved", _set("cover_pp_init", [9], 5100.0),
     "{file}: cover_pp_init must be the sum assured on a level point, which never "
     "escalates; it is not at point_id [9]"),
    ("a level premium moved", _set("premium_pp_init", [13], 46.0),
     "{file}: premium_pp_init must be the premium at issue on a level point, which never "
     "escalates; it is not at point_id [13]"),
    ("an escalated cover below the sum assured", _set("cover_pp_init", [11], 4999.0),
     "{file}: cover_pp_init must be the sum assured or more on an escalating point, each "
     "increase being floored at 0; it is not at point_id [11]"),
    ("an escalated premium below the premium at issue", _set("premium_pp_init", [16], 100.0),
     "{file}: premium_pp_init must be the premium at issue or more on an escalating point, "
     "each increase being floored at 0; it is not at point_id [16]"),
    ("a paid-up count without the variant", _set("pols_pu_init", [9], 0.1),
     "{file}: pols_pu_init must be 0 on a point without the pro-rata paid-up variant; it "
     "is not at point_id [9]"),
    ("a paid-up cover without the variant", _set("pu_benefit_pp_init", [13], 5000.0),
     "{file}: pu_benefit_pp_init must be 0 on a point without the pro-rata paid-up "
     "variant; it is not at point_id [13]"),
    # The first conversion is at the end of policy month 119, when the 120th of 240
    # payments has been made, so a paid-up policy is first in force at 120: the paid-up
    # point moved to 119 with its strand, and with its count gone but its cover left.
    ("a paid-up count before the first conversion", _set("duration_mth", [10], 119),
     f"{{file}}: pols_pu_init must be 0 {_EARLIEST} [10]"),
    ("a paid-up cover before the first conversion",
     _then(_set("duration_mth", [10], 119), _set("pols_pu_init", [10], 0.0)),
     f"{{file}}: pu_benefit_pp_init must be 0 {_EARLIEST} [10]"),
    ("a paid-up cover on no paid-up policy", _set("pols_pu_init", [10], 0.0),
     "{file}: pu_benefit_pp_init must be 0 where no paid-up policy is in force, "
     "pols_pu_init 0; it is not at point_id [10]"),
    # The first year's history at its last month: an increase on the first anniversary,
    # read after month 0's step, where the columns are measured before it.
    ("a cover on the first anniversary", _set("cover_pp_init", [12], 157500.0),
     f"{{file}}: cover_pp_init must be the sum assured {_FIRST_YEAR} [12]"),
    ("a premium on the first anniversary", _set("premium_pp_init", [12], 111.375),
     f"{{file}}: premium_pp_init must be the premium at issue {_FIRST_YEAR} [12]"),
    # The first year's history at its first month: an increase a month after issue.
    ("a cover a month after issue",
     _then(_set("duration_mth", [14], 1), _set("cover_pp_init", [14], 5150.0)),
     f"{{file}}: cover_pp_init must be the sum assured {_FIRST_YEAR} [14]"),
    # The earliest paid-up month on an odd cessation: 239 months, half of which rounded up
    # is 120, so a strand at 119 is one no conversion can have made, where half rounded
    # down would admit it.
    ("a paid-up count at half an odd cessation rounded down",
     _then(_set("cessation_months", [10], 239), _set("duration_mth", [10], 119)),
     f"{{file}}: pols_pu_init must be 0 {_EARLIEST} [10]"),
    ("a crossover not whole", _set("crossover_mth_init", [10], 166.5), _CROSS_WHOLE + "[10]"),
    ("a crossover below -1", _set("crossover_mth_init", [11], -2), _CROSS_WHOLE + "[11]"),
    ("a blank crossover", _set("crossover_mth_init", [13], float("nan")),
     _CROSS_WHOLE + "[13]"),
    # The bound at 2**53 itself, and 2**53 - 1, a whole number Data reads and then refuses
    # as no month before the valuation date.
    ("a crossover of 2**53", _set("crossover_mth_init", [11], 2.0 ** 53),
     _CROSS_WHOLE + "[11]"),
    ("a crossover of 2**53 - 1", _set("crossover_mth_init", [11], 2 ** 53 - 1),
     _CROSS_MONTH + "[11]"),
    ("a crossover on new business", _set("crossover_mth_init", [1], 166),
     "{file}: crossover_mth_init must be -1 on a policy not yet in force, duration_mth 0 "
     "or less; it is not at point_id [1]"),
    ("a crossover in the valuation month", _set("crossover_mth_init", [9], 166),
     _CROSS_MONTH + "[9]"),
    ("a crossover after cessation",
     _then(_set("duration_mth", [13], 310), _set("crossover_mth_init", [13], 305)),
     _CROSS_MONTH + "[13]"),
    ("premiums paid past the cover with no crossover",
     _set("crossover_mth_init", [10], -1),
     "{file}: crossover_mth_init must not be -1 where the premiums paid exceed the cover, "
     "prem_cum_pp_init above cover_pp_init, to the cent: they crossed it before the "
     "valuation date; it is not at point_id [10]"),
    ("a level crossover a month early", _set("crossover_mth_init", [10], 165),
     _CROSS_LEVEL + "[10]"),
    ("a level crossover a month late", _set("crossover_mth_init", [10], 167),
     _CROSS_LEVEL + "[10]"),
    # The premiums paid: the review's refund of 1,000,030 on a 5,000 policy, and each
    # bound a cent outside.
    ("a million paid on a level point", _set("prem_cum_pp_init", [8], 1e6), _PAID_LEVEL),
    ("a cent short of the level premiums", _set("prem_cum_pp_init", [8], 179.99),
     _PAID_LEVEL),
    ("a cent past the level premiums", _set("prem_cum_pp_init", [8], 180.01), _PAID_LEVEL),
    ("a cent short of the premiums at issue", _set("prem_cum_pp_init", [11], 5579.99),
     _PAID_ESCALATING),
    ("a cent past the latest premium", lambda t: _set(
        "prem_cum_pp_init", [11], t.at[11, "premium_pp_init"] * 186 + 0.01)(t),
     _PAID_ESCALATING),
    # Past cessation the premiums due are cessation_months, 240, not the months in force,
    # 250: a cent past the latest premium times 240, which times 250 would admit.
    ("a cent past the latest premium after cessation", lambda t: _then(
        _set("duration_mth", [11], 250),
        _set("prem_cum_pp_init", [11], t.at[11, "premium_pp_init"] * 240 + 0.01))(t),
     _PAID_ESCALATING),
    # The paid-up cover: the review's 0 and 1e7 beside paid-up policies, and each bound a
    # cent outside, 5,000 x 120 / 240 and 5,000 x 200 / 240.
    ("no paid-up cover beside paid-up policies", _set("pu_benefit_pp_init", [10], 0.0),
     _PU_COVER),
    ("a paid-up cover of 1e7", _set("pu_benefit_pp_init", [10], 1e7), _PU_COVER),
    ("a cent short of the paid-up cover", _set("pu_benefit_pp_init", [10], 2499.99),
     _PU_COVER),
    ("a cent past the paid-up cover",
     _set("pu_benefit_pp_init", [10], 5000.0 * 200 / 240 + 0.01), _PU_COVER),
    # On an odd cessation, 239 months, a conversion needs 120 payments, half rounded up, so
    # the paid-up cover is at least 5,000 x 120 / 239: a cent below it, which half rounded
    # down, 5,000 x 119 / 239, would admit.
    ("a cent short of the paid-up cover on an odd cessation",
     _then(_set("cessation_months", [10], 239),
           _set("pu_benefit_pp_init", [10], 5000.0 * 120 / 239 - 0.01)), _PU_COVER),
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


def _relabelled(message, relabel):
    """``message`` with every ``point_id [...]`` list it holds relabelled by ``relabel``."""
    def labels(match):
        return "point_id [" + ", ".join(str(relabel[int(p)]) for p in
                                        match.group(1).split(", ")) + "]"
    return re.sub(r"point_id \[(\d+(?:, \d+)*)\]", labels, message)


@pytest.fixture(scope="module")
def malformed_extract(tmp_path_factory):
    """:data:`MALFORMED`'s tables as an extract labels its rows, each a file of its own.

    Each case's table is the committed one with its fault, made by its own labels, and
    then relabelled :data:`EXTRACT_LABELS`, in order, so that no label is its position
    plus one.  One model reads them all, as :func:`malformed` reads its files.  Returns
    ``(model, {case: filename}, {committed label: extract label})``.
    """
    root = tmp_path_factory.mktemp("malformed_extract")
    relabel = dict(zip(_committed().index, EXTRACT_LABELS))
    files = {}
    for number, (case, edit, _) in enumerate(MALFORMED):
        files[case] = f"extract_{number:02d}_sec.csv"
        table = edit(_committed()).rename(index=relabel)
        temp_inputs(root, model_path(SEC), model_points=table, model_point_file=files[case])
    model = mx.read_model(root / SEC, name=_name("malformed_extract"))
    yield model, files, relabel
    model.close()


@pytest.mark.parametrize("case, edit, message", MALFORMED, ids=[c[0] for c in MALFORMED])
def test_a_malformed_row_of_an_extract_is_refused_naming_its_label(malformed_extract, case,
                                                                    edit, message):
    """Each refusal names the extract's labels, never the rows' positions (T5).

    The committed labels are their positions plus one, so a check that named a row by its
    place in the table, ``idx + 1``, would pass every case of :data:`MALFORMED`.  On the
    extract each label is another, and each case's message names the extract's.
    """
    model, files, relabel = malformed_extract
    model.Data.model_point_file = files[case]
    _refused(model.Data.model_point_table,
             _relabelled(message, relabel).format(file=files[case]))


def test_the_future_horizon_is_a_reference_that_bounds_future_business(tmp_path):
    """``Data.future_horizon_mth`` refuses a policy issued later than it, and 0 refuses all.

    The committed table's one future point is issued 13 months on.  It reads at the shipped
    120 months and at 13, the shortest horizon that admits it, and is refused at 12, by
    name.  At 0 the model takes no future new business, D4's fallback for a product that
    cannot support it, and the message says so.  A horizon that is not a whole number of
    months, 0 or more, below ``2**53``, is itself refused, a NaN and an infinity among
    them: either would admit every policy.  A whole number written as a float, ``13.0``,
    reads as 13 does, and ``2**53 - 1``, the largest whole number the compiled model holds
    exactly, reads; ``2**53`` does not.  Setting the Reference clears the table, so each
    value is read afresh.
    """
    future = _label(_committed(), "future", 4, -13)
    later = (f"{TABLE}: duration_mth must be -12 or more, a policy issued at most 12 months "
             f"after the valuation date; it is not at point_id [{future}]")
    no_future = (f"{TABLE}: duration_mth must be 0 or more: this model takes no future new "
                 f"business; it is not at point_id [{future}]")
    model = mx.read_model(_sec_inputs(tmp_path, _committed()), name=_name("horizon"))
    try:
        assert model.Data.future_horizon_mth == 120
        off = ("future_horizon_mth must be a whole number of months, 0 or more, below "
               "2**53, not {}")
        for horizon, refusal in ((13, None), (12, later), (0, no_future), (13.0, None),
                                 *((h, off.format(h)) for h in (
                                     -1, 12.5, math.nan, math.inf, -math.inf, WHOLE)),
                                 (WHOLE - 1, None), (120, None)):
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


def _moved_on(label, months):
    """An edit that moves the anchor cell's row ``label`` on to policy month ``months``,
    past its cessation at 240, with the history the move gives it: 240 premiums of 30
    paid, and its crossover at 166, so that ``Data`` reads it."""
    return _then(_set("duration_mth", [label], months),
                 _set("prem_cum_pp_init", [label], 30.0 * 240),
                 _set("crossover_mth_init", [label], 166))


def test_a_point_past_the_limiting_age_is_refused_by_proj_len(tmp_path):
    """A point at or past the limiting age has no frame, and ``proj_len()`` refuses it.

    The anchor cell at its crossover month is moved on to ``duration_mth`` 600, the policy
    month it reaches ``omega_age``, 120, from entry at 70, on the policy clock.  That is a
    rule of the product, not of the table: it needs the limiting age, a Reference, and the
    entry age the point's own columns give, read where the frame is defined, so the table
    reads, and the point is refused on its first projection, rather than projecting
    nothing.  A loop over the block would meet the point only when it reached it, after
    projecting the points before it, so ``run_sec.py --block``, run beside the table, asks
    every point for its frame first: it fails naming the point, and prints nothing before.
    And one month earlier, 599, the last month before the limiting age, projects one month.
    """
    moved = _label(_committed(), "derived", 1, 166)
    model = _read_edited(tmp_path, _moved_on(moved, 600))
    message = (f"point_id {moved}: duration_mth 600 is at or past the limiting age, policy "
               f"month 600, omega_age 120")
    try:
        assert len(model.Data.model_point_table()) == len(_committed())
        _refused(_point(model, moved).result_cf, message)
    finally:
        model.close()
    model = _read_edited(tmp_path / "last", _moved_on(moved, 599))
    try:
        assert len(_point(model, moved).result_cf()) == 1
    finally:
        model.close()
    runner = tmp_path / "run_sec.py"
    shutil.copy(model_path(SEC).parent / "run_sec.py", runner)
    done = _run_sec(runner, "--block", check=False)
    assert done.returncode != 0 and done.stdout == b""
    assert message in done.stderr.decode(errors="replace")


# What the contract does not issue, refused by proj_len() as a point past the limiting age
# is, as (case, the table's edit, the References set, the point, the message, and the
# frame the point projects at the shipped References, or None).  Data reads an entry age as
# WOL_UK_S does, so each reads.  The product issues from 18, the mortality table's first
# age, and the frame runs to omega_age, 120; the compiled caches are sized from both.
# Each bound is refused just inside it here, and accepted at it in the edges test.  And
# each bound, moved past a committed twin, refuses it, which at the shipped bound projects
# its frame: the Reference is what refuses it.  Point 1 is the anchor cell, issued at 70;
# point 5 the underwritten one, at 40.  And a point whose premiums cease past the limiting
# age, which no contract writes, and on which the crossover's search, which runs the
# premium-paying months, would run past the contract's longest cover: a month past it, at
# 2**53 - 1, which Data reads, and past a limiting age lowered below the anchor cell's
# cessation at 90; the edges test reads premiums ceasing at the limiting age itself.
NOT_ISSUED = [
    ("an issue age of 17", _set("entry_age", [5], 17), {}, 5,
     "point_id 5: the issue age, 17, is below issue_age_min, 18", None),
    ("an issue age below a bound raised to 41", None, {"issue_age_min": 41}, 5,
     "point_id 5: the issue age, 40, is below issue_age_min, 41", 960),
    ("an issue age of 120", _set("entry_age", [1], 120), {}, 1,
     "point_id 1: the issue age, 120, is at or past omega_age, 120: the policy has no cover",
     None),
    ("an issue age at a limiting age lowered to 70", None, {"omega_age": 70}, 1,
     "point_id 1: the issue age, 70, is at or past omega_age, 70: the policy has no cover",
     600),
    ("an issue age of 2**53 - 1", _set("entry_age", [1], 2 ** 53 - 1), {}, 1,
     f"point_id 1: the issue age, {2 ** 53 - 1}, is at or past omega_age, 120: the policy "
     f"has no cover", None),
    ("a cessation a month past the limiting age", _set("cessation_months", [1], 601), {}, 1,
     "point_id 1: cessation_months 601 is past the limiting age, policy month 600, "
     "omega_age 120", None),
    ("a cessation of 2**53 - 1", _set("cessation_months", [1], 2 ** 53 - 1), {}, 1,
     f"point_id 1: cessation_months {2 ** 53 - 1} is past the limiting age, policy month "
     f"600, omega_age 120", None),
    ("a cessation past a limiting age lowered to 89", None, {"omega_age": 89}, 1,
     "point_id 1: cessation_months 240 is past the limiting age, policy month 228, "
     "omega_age 89", 600),
]


@pytest.mark.parametrize("case, edit, refs, point, message, frame", NOT_ISSUED,
                         ids=[c[0] for c in NOT_ISSUED])
def test_a_point_the_contract_does_not_issue_is_refused_by_proj_len(tmp_path, case, edit,
                                                                    refs, point, message,
                                                                    frame):
    """``proj_len()`` refuses a point outside the contract's bounds, naming it (§6.4).

    ``WOL_UK_S`` projects any entry age from any age its tables reach, and so would modelx
    here, but the contract does not write it, and the compiled model's caches are sized
    from the contract: a frame of at most 103 years and the horizon, attained ages from 18
    to 120.  So the frame refuses such a point, naming it, as it refuses a point past the
    limiting age, and every report with it (:data:`NOT_ISSUED`): each bound just inside it,
    and each bound moved past a committed twin, which projects at the shipped bound, on a
    model read afresh.  So it refuses a point whose premiums cease past the limiting age,
    whose crossover search would run past the contract's longest cover, a cessation of
    ``2**53 - 1`` months among them, which would run it about ``9e15`` times in either
    engine.  A bound off by one, or a refusal lost, lets a point through.  The table reads
    either way.  Every Reference is set on a model just read, before its projection
    computes anything (K7).
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


# Each Reference proj_len() holds to a domain, as (case, the References set, the message
# where refused, or None where the twin of S point 1 projects).  NaN and the infinities are
# outside every domain.  WOL_UK_S reads the mortality loadings and improvement inside the
# cap's min, which reads an infinity as certain death; the RPI through a max and a min,
# max(rpi, 0.0) then the cover cap, which read an infinity as no increase or the cap; each
# cap as a bound written second, which a NaN cap is lost through; the stress through a
# comparison with 0, which a NaN switches off, and through the lapse rate's min, its bound
# first, which reads an infinity as a certain lapse; and the shares, the take-up, the
# expenses and commission as weights, which below 0 or past 1 make a negative benefit,
# expense or rate.  Each is refused at the nearest value outside each edge of its domain,
# and accepted at the edge itself: the largest finite float an edge of each domain
# unbounded above, -1 inflation's and 1 improvement's.  issue_age_min, suicide_mths and
# omega_age are whole numbers below 2**53, which the compiled model holds as long long,
# printed through int() once whole: each is refused at a fraction and at exactly 2**53, and
# its largest whole number accepted, or refused by a later rule.
BIG = 1.7976931348623157e308
WHOLE = 2.0 ** 53
BELOW_0 = math.nextafter(0.0, -1.0)
ABOVE_1 = math.nextafter(1.0, 2.0)


def _domain(ref, rule, accepted, refused, printed=float):
    """The DOMAINS cases of ``ref`` alone: each of ``accepted`` projects, each of
    ``refused`` is refused by the domain's ``rule``, and NaN and the infinities by it
    too."""
    message = f"point_id 1: {ref} must be {rule}, not {{}}"
    cases = [(f"{ref}={value!r}", {ref: value}, None) for value in accepted]
    cases += [(f"{ref}={value!r}", {ref: value}, message.format(printed(value)))
              for value in refused]
    return cases + [(f"{ref}={value!r}", {ref: value}, message.format(float(value)))
                    for value in (math.nan, math.inf, -math.inf)]


def _whole_domain(ref, accepted, below=True):
    """The DOMAINS cases of an integer Reference: a whole number below 2**53, and 0 or
    more where ``below``, printed through int() once whole."""
    whole = f"point_id 1: {ref} must be a whole number below 2**53, not {{}}"
    cases = [(f"{ref}={value!r}", {ref: value}, None) for value in accepted]
    if below:
        cases.append((f"{ref}=-1", {ref: -1}, f"point_id 1: {ref} must be 0 or more, not -1"))
    return cases + [(f"{ref}={value!r}", {ref: value}, whole.format(float(value)))
                    for value in (0.5, 120.5, WHOLE, 1e300, math.nan, math.inf, -math.inf)]


_FINITE_0 = ("a finite number, 0 or more", (0.0, BIG), (BELOW_0,))
_SHARE = ("a number from 0 to 1", (0.0, 1.0), (BELOW_0, ABOVE_1))
OMEGA = ("point_id 1: omega_age must be above issue_age_min, 18, and at most 121, a year "
         "past mort_table.csv's last age, not {}")
DOMAINS = [
    *_domain("mort_loading_o50", *_FINITE_0),
    *_domain("mort_loading_uw", *_FINITE_0),
    *_domain("mort_improvement", "a finite number, 1 or less", (-BIG, 1.0), (ABOVE_1,)),
    *_domain("acc_share", *_SHARE),
    *_domain("suicide_share", *_SHARE),
    *_whole_domain("suicide_mths", (0, WHOLE - 1)),
    *_domain("rpi_rate", "a finite number", (-BIG, BIG), ()),
    *_domain("esc_rpi_cover_cap", *_FINITE_0),
    *_domain("esc_rpi_prem_mult", *_FINITE_0),
    *_domain("esc_rpi_prem_cap", *_FINITE_0),
    *_domain("esc_fixed_cover", *_FINITE_0),
    *_domain("esc_fixed_prem", *_FINITE_0),
    *_domain("esc_take_up", *_SHARE),
    *_domain("lapse_crossover_beta", *_FINITE_0),
    *_domain("inflation_rate", "a finite number, -1 or more", (-1.0, BIG),
             (math.nextafter(-1.0, -2.0),)),
    *_domain("expense_acq_o50", *_FINITE_0),
    *_domain("expense_acq_uw", *_FINITE_0),
    *_domain("expense_maint_o50", *_FINITE_0),
    *_domain("expense_maint_uw", *_FINITE_0),
    *_domain("comm_init_rate", *_FINITE_0),
    *_whole_domain("issue_age_min", (0,)),
    ("issue_age_min=2**53-1", {"issue_age_min": WHOLE - 1},
     f"point_id 1: the issue age, 70, is below issue_age_min, {int(WHOLE - 1)}"),
    *_whole_domain("omega_age", (120, 121, 120.0), below=False),
    ("omega_age=122", {"omega_age": 122}, OMEGA.format(122)),
    ("omega_age=18", {"omega_age": 18}, OMEGA.format(18)),
    ("omega_age=19", {"omega_age": 19},
     "point_id 1: the issue age, 70, is at or past omega_age, 19: the policy has no cover"),
    ("omega_age=2**53-1", {"omega_age": WHOLE - 1}, OMEGA.format(int(WHOLE - 1))),
    # omega_age_max, the contract's largest limiting age, 121, which the compiled model's
    # caches are sized for (spec_sec.py, the C step): a whole number below 2**53, which
    # omega_age may not pass; at 121, the table's last age plus one, it refuses nothing the
    # table admits, so only a bound lowered refuses a limiting age.
    *_whole_domain("omega_age_max", (120, 121, WHOLE - 1), below=False),
    ("omega_age=121 with omega_age_max 120", {"omega_age": 121, "omega_age_max": 120},
     "point_id 1: omega_age, 121, is above omega_age_max, 120"),
    ("omega_age_max=119", {"omega_age_max": 119},
     "point_id 1: omega_age, 120, is above omega_age_max, 119"),
]


@pytest.mark.parametrize("case, refs, message", DOMAINS, ids=[c[0] for c in DOMAINS])
def test_each_reference_is_held_to_its_domain_at_both_edges(case, refs, message):
    """``proj_len()`` holds each Reference to its domain, NaN and the infinities outside it.

    ``WOL_UK_S`` checks none of them, and off its domain each projects a negative rate,
    benefit or expense, a factor that changes sign each year, or a NaN that a comparison
    loses, every check passing: a NaN cover cap is lost through its ``min``, a NaN stress
    switches itself off, a NaN suicide window closes, and a NaN limiting age switches off
    every comparison with it, the limiting age sizing every frame.  The frame refuses each
    such Reference, by name, before it projects anything, and every report with it, at the
    nearest value outside each edge of its domain, and accepts the edge itself
    (:data:`DOMAINS`): the integer References at a fraction and at exactly ``2**53``, and
    ``omega_age`` past the mortality table's last age.  Each Reference is refused on every
    point, whether or not the point's cell reads it, as a model-wide assumption.  Each case
    sets its References on a model just read (K7).
    """
    model = mx.read_model(model_path(SEC), name=_name("domain"))
    try:
        for ref, value in refs.items():
            setattr(model.Projection, ref, value)
        p = _row(model, "twin", 1, 0)
        if message is None:
            assert p.proj_len() > 0
        else:
            _refused(p.result_cf, message)
    finally:
        model.close()


@pytest.mark.parametrize("refs, message", [
    ({"rpi_rate": math.nan}, "point_id 4: rpi_rate must be a finite number, not nan"),
    ({"esc_take_up": 5}, "point_id 4: esc_take_up must be a number from 0 to 1, not 5.0")],
    ids=["rpi_rate=nan", "esc_take_up=5"])
def test_the_crossover_asks_for_the_frame_first(refs, message):
    """``crossover_mth()`` refuses a Reference off its domain, as a report does (§6.4).

    No cell of the projection reads the crossover, so no report's call of ``proj_len()``
    stands before it when it is asked alone: the review found it searching at an RPI of NaN
    and reporting no crossover, -1, and at a take-up of 5 reporting 260, months no policy
    has.  It asks ``proj_len()`` for the frame first, so each is refused, by name, on the
    twin of the RPI point.  Each Reference is set on a model just read (K7).
    """
    model = mx.read_model(model_path(SEC), name=_name("crossover_frame"))
    try:
        for ref, value in refs.items():
            setattr(model.Projection, ref, value)
        _refused(_row(model, "twin", 4, 0).crossover_mth, message)
    finally:
        model.close()


# A value that leaves the floats, from an opening state and References each in its domain,
# as (case, the table's edit, the References set, the point, the call, a report that reads
# it, the start of the message).  The RPI row at 186 opened on a cover or a premium near
# the largest float, which its next anniversary's increase takes past it at t = 6, and on
# premiums paid at it, which month 0's premium, opened at 1e306, takes past it at t = 0: a
# premium of a few pounds would round back to the largest float.  Then the review's
# expenses, an expense of 1.7e308 inflated at 100% a year, past the floats at t = 48; a
# commission rate of 1e308; a commission and an expense each just inside the floats, whose
# sum, the net cash flow, is not; a count of 1e307 paying 30 a month; a count of 1e300
# with a cover of 1e300, whose claims leave the floats; a paid-up count and cover of 1e300
# and 6e299, whose summed paid-up cover does; and the double accidental benefit on a cover
# of 1e308, from the first anniversary.  Each is refused in the cell where it first is,
# naming the point, the month and what makes it, and a kind by its code, which the C step
# makes an int in both engines: the claims' DEATH 0 and the accidental benefit's ACC 2,
# which the spec test holds.  And each of the two chains whose refusal is a cell of its own
# (REFUSAL_CELLS) leaves the floats in each of its branches, which its refusal cell
# repeats: the opening month, above, a month within a policy year and a year's first
# month, which reads the year's opening.  The premiums paid on the RPI row at 186, whose
# anniversary is at t = 6, opened 2.5 and 6.5 premiums of 1e306 short of the largest
# float; the paid-up cover on the paid-up row at 200, whose anniversary is at t = 4, on a
# million policies on full cover with a cover of 2e303, whose conversions add about 1.3e306
# a month, opened on 113,000 and 110,000 paid-up policies at 1.5e303 each.
NET = 1.7e308


def _paid_up_near_the_floats(policies):
    """An edit of the paid-up row at 200 whose summed paid-up cover opens near the largest
    float on ``policies`` paid-up policies and grows past it by its conversions: a million
    policies on full cover with a cover and a sum assured of 2e303, so no crossover, each
    paid-up policy carrying 1.5e303, between the share of the sum assured at the first
    conversion and today's cover's share of the payments made."""
    return _then(_set("policy_count", [10], 1e6), _set("sum_assured", [10], 2e303),
                 _set("cover_pp_init", [10], 2e303), _set("crossover_mth_init", [10], -1),
                 _set("pols_pu_init", [10], policies),
                 _set("pu_benefit_pp_init", [10], 1.5e303))
PAST_THE_FLOATS = [
    ("a cover", _set("cover_pp_init", [11], 1.79e308), {}, 11, ("cover_pp", 6),
     "result_cf",
     "point_id 11: the cover cover_pp(6) is inf, not a finite number, from cover_pp_init "
     "1.79e+308 and an annual increase of 0.03"),
    ("a premium", _set("premium_pp_init", [11], 1.79e308), {}, 11, ("premium_pp", 6),
     "result_cf",
     "point_id 11: the premium premium_pp(6) is inf, not a finite number, from "
     "premium_pp_init 1.79e+308 and an annual increase of 0.045"),
    ("premiums paid",
     _then(_set("prem_cum_pp_init", [11], BIG), _set("premium_pp_init", [11], 1e306)), {},
     11, ("prem_cum_pp", 0), "result_pols",
     "point_id 11: the premiums paid prem_cum_pp(0) are inf, not a finite number, from "
     "prem_cum_pp_init 1.7976931348623157e+308"),
    ("premiums paid within a policy year",
     _then(_set("prem_cum_pp_init", [11], BIG - 2.5e306), _set("premium_pp_init", [11], 1e306)),
     {}, 11, ("prem_cum_pp", 2), "result_pols",
     "point_id 11: the premiums paid prem_cum_pp(2) are inf, not a finite number, from "
     "prem_cum_pp_init 1.7726931348623157e+308"),
    ("premiums paid on an anniversary",
     _then(_set("prem_cum_pp_init", [11], BIG - 6.5e306), _set("premium_pp_init", [11], 1e306)),
     {}, 11, ("prem_cum_pp", 6), "result_pols",
     "point_id 11: the premiums paid prem_cum_pp(6) are inf, not a finite number, from "
     "prem_cum_pp_init 1.7326931348623157e+308"),
    ("the expenses", None, {"expense_maint_o50": NET, "inflation_rate": 1.0}, 1,
     ("expenses", 48), "result_cf",
     "point_id 1: the expenses expenses(48) are inf, not a finite number, from "
     "expense_acq_o50 150.0, expense_maint_o50 1.7e+308 and inflation_rate 1.0, on "
     "pols_all(48) "),
    ("the commission", None, {"comm_init_rate": 1e308}, 1, ("commissions", 0), "result_cf",
     "point_id 1: the commission commissions(0) is inf, not a finite number, from "
     "comm_init_rate 1e+308 on premiums(0) 30.0"),
    ("the net cash flow", None, {"comm_init_rate": NET / 30, "expense_acq_o50": NET}, 1,
     ("net_cf", 0), "result_cf",
     "point_id 1: the net cash flow net_cf(0) is -inf, not a finite number, from premiums "
     "30.0, claims "),
    ("the premiums", _set("policy_count", [1], 1e307), {}, 1, ("premiums", 0), "result_cf",
     "point_id 1: the premiums premiums(0) are inf, not a finite number, from premium_pp(0) "
     "30.0 on pols_if(0) 1e+307 policies"),
    ("the claims",
     _then(_set("policy_count", [1], 1e300), _set("sum_assured", [1], 1e300),
           _set("cover_pp_init", [1], 1e300)), {}, 1, ("claims", 0, "DEATH"), "result_cf",
     "point_id 1: the claims claims(0, 0) are inf, not a finite number, from "
     "pols_death(0) "),
    ("the paid-up cover",
     _then(_set("sum_assured", [10], 1e300), _set("cover_pp_init", [10], 1e300),
           _set("pols_pu_init", [10], 1e300), _set("pu_benefit_pp_init", [10], 6e299),
           _set("crossover_mth_init", [10], -1)), {}, 10, ("pu_benefit", 0), "result_cf",
     "point_id 10: the paid-up cover pu_benefit(0) is inf, not a finite number, from "
     "pols_pu_init 1e+300 paid-up policies at pu_benefit_pp_init 6e+299"),
    ("the paid-up cover within a policy year", _paid_up_near_the_floats(113000.0), {}, 10,
     ("pu_benefit", 3), "result_cf",
     "point_id 10: the paid-up cover pu_benefit(3) is inf, not a finite number, from "
     "pols_pu_init 113000.0 paid-up policies at pu_benefit_pp_init 1.5e+303 and the "
     "conversions since"),
    ("the paid-up cover on an anniversary", _paid_up_near_the_floats(110000.0), {}, 10,
     ("pu_benefit", 4), "result_cf",
     "point_id 10: the paid-up cover pu_benefit(4) is inf, not a finite number, from "
     "pols_pu_init 110000.0 paid-up policies at pu_benefit_pp_init 1.5e+303 and the "
     "conversions since"),
    ("a benefit",
     _then(_set("sum_assured", [2], 1e308), _set("cover_pp_init", [2], 1e308)), {}, 2,
     ("benefit_pp", 12, "ACC"), "result_cf",
     "point_id 2: the benefit benefit_pp(12, 2) is inf, not a finite number, from the "
     "cover cover_pp(12) 1e+308"),
]


@pytest.mark.parametrize("case, edit, refs, point, call, report, message", PAST_THE_FLOATS,
                         ids=[c[0] for c in PAST_THE_FLOATS])
def test_a_value_past_the_floats_is_refused_where_it_first_is(tmp_path, case, edit, refs,
                                                              point, call, report, message):
    """A value past the largest float is refused in the cell where it first is.

    ``Data`` and ``proj_len()`` hold each opening amount, count and Reference to a finite
    number, so a value near the largest float reads; an increase, a premium, a count, an
    inflation rate or a sum then takes a value the projection computes past the floats,
    where ``WOL_UK_S`` would pay an infinite claim, charge an infinite expense or compare
    an infinite total, every report infinite and its checks NaN or passing.  The cell where
    the value first leaves the floats refuses it, naming the point, the month and what makes
    it (:data:`PAST_THE_FLOATS`), and so does a report that reads it first: ``result_cf``,
    or ``result_pols`` for the premiums paid, which no cash flow reads on that point at the
    shipped References (USLIB-SEC-PLAN.md §7.1, *Record — M1*; UKLIB-SEC-PLAN.md §6.6,
    *Carried into M10 and after*).  The month before projects.  Each Reference is set on a
    model just read (K7).
    """
    model = _read_edited(tmp_path, edit or (lambda t: t))
    try:
        for ref, value in refs.items():
            setattr(model.Projection, ref, value)
        p = _point(model, point)
        name, t, *rest = call
        rest = [_code(p, arg) for arg in rest]
        if t > 0:
            p.cells[name](t - 1, *rest)
        _refused(lambda: p.cells[name](t, *rest), message)
        _refused(p.cells[report], message)
    finally:
        model.close()


# A step to the policy years that overflows the floats, from a Reference in its domain, as
# (case, the table's edit, the References set, the committed point read, the call): each
# of the five powers the projection raises, the cover's and the premium's steps, the
# inflation and improvement factors and the crossover's search.  A step of 1e200 squares
# past the floats at the second anniversary, t = 24.  The search guards both its steps in
# both its loops, from issue on a point not yet in force and from the valuation date on
# one in force, and each guard is reached: on the underwritten increasing twin, point 6,
# and on the same point in force 12 months, point 12.  The cover's step in each loop, the
# premiums paid never passing the cover; the premium's from issue on a premium of 0, which
# pays nothing however it grows, and on a cover of 1e300, which the premiums paid do not
# reach first; and the premium's in force on that cover.  Compiled without its guard, each
# search returns -1 or 24 where modelx raises.
OVERFLOWING_POWERS = [
    ("the cover's step", None, {"esc_fixed_cover": 1e200}, 6, ("cover_pp", 24)),
    ("the premium's step", None, {"esc_fixed_prem": 1e200}, 6, ("premium_pp", 24)),
    ("the inflation factor", None, {"inflation_rate": 1e200}, 1, ("inflation_factor", 24)),
    ("the improvement factor", None, {"mort_improvement": -1e200}, 1,
     ("mort_improve_factor", 24)),
    ("the crossover's search: the cover's step from issue", None,
     {"esc_fixed_cover": 1e200}, 6, ("crossover_mth",)),
    ("the crossover's search: the premium's step from issue, a premium of 0",
     _then(_set("premium_mth", [6], 0.0), _set("premium_pp_init", [6], 0.0)),
     {"esc_fixed_prem": 1e200}, 6, ("crossover_mth",)),
    ("the crossover's search: the premium's step from issue, a cover of 1e300",
     _then(_set("sum_assured", [6], 1e300), _set("cover_pp_init", [6], 1e300)),
     {"esc_fixed_prem": 1e200}, 6, ("crossover_mth",)),
    ("the crossover's search: the cover's step in force", None,
     {"esc_fixed_cover": 1e200}, 12, ("crossover_mth",)),
    ("the crossover's search: the premium's step in force, a cover of 1e300",
     _then(_set("sum_assured", [12], 1e300), _set("cover_pp_init", [12], 1e300)),
     {"esc_fixed_prem": 1e200}, 12, ("crossover_mth",)),
]


@pytest.mark.parametrize("case, edit, refs, point, call", OVERFLOWING_POWERS,
                         ids=[c[0] for c in OVERFLOWING_POWERS])
def test_an_overflowing_power_raises_python_s_overflow_error(tmp_path, case, edit, refs,
                                                             point, call):
    """A power that leaves the floats raises ``OverflowError``, as Python raises it.

    The cells check what they compute, but a ``**`` whose result passes the largest float
    raises before the cell can look at it: modelx runs the formula as Python does, and
    Python's float power raises ``OverflowError`` with the platform's own message,
    ``os.strerror(errno.ERANGE)``, "Numerical result out of range" on Linux, rather than
    return an infinity.  So a step to the policy years at a Reference in its domain but large
    enough, 1e200, is refused, not projected, though the refusal names neither the point nor
    the Reference (:data:`OVERFLOWING_POWERS`).  The compiled model's ``pow`` returns an
    infinity there, so each of these cells takes uslib's M22 form, Python's own float power
    where the compiled one gives an infinity, so that both engines raise this error, which
    the compiled refusal test holds.  Each Reference is set on a model just read (K7).
    The crossover's search guards each of its two steps in each of its two loops, and each
    guard is reached by a case of its own.
    """
    model = _read_edited(tmp_path, edit or (lambda t: t))
    try:
        for ref, value in refs.items():
            setattr(model.Projection, ref, value)
        p = _point(model, point)
        name, *args = call
        with pytest.raises(Exception) as excinfo:
            p.cells[name](*args)
        text = str(excinfo.value)
        assert "OverflowError" in text and os.strerror(errno.ERANGE) in text, text
    finally:
        model.close()


@pytest.mark.parametrize("grid", GRIDS)
def test_a_whole_limit_written_as_a_float_projects_as_the_int_does(grid):
    """``omega_age = 120.0`` projects what 120 projects, cell for cell (§6.4).

    ``proj_len()`` holds ``omega_age``, ``issue_age_min`` and ``suicide_mths`` to whole
    numbers, which ``120.0``, ``18.0`` and ``12.0`` are, and reads ``omega_age`` as the
    ``int`` it is: a float limit would make ``proj_len()`` the float 600.0, on which every
    report's ``range`` raises ``TypeError``, where the compiled model, typing the Reference
    ``long long``, would project.  So with the three set as floats, on a model just read,
    the twins of S's anchor and underwritten points, the paid-up point in force and the RPI
    point issued later are what the shipped model makes of them in every cell, bit for bit,
    each integer cell an ``int`` in both.

    The twin of the anchor cell and the paid-up point in force run by default, and the
    underwritten twin and the RPI point issued later with the full grid.
    """
    floats = mx.read_model(model_path(SEC), name=_name("floats"))
    ints = mx.read_model(model_path(SEC), name=_name("ints"))
    try:
        floats.Projection.omega_age = 120.0
        floats.Projection.issue_age_min = 18.0
        floats.Projection.suicide_mths = 12.0
        cases = ((("twin", 1, 0), ("derived", 3, 200)) if grid == "core"
                 else (("twin", 5, 0), ("future", 4, -13)))
        for case in cases:
            mine, theirs = _row(floats, *case), _row(ints, *case)
            sweep(theirs)
            assert twin_mismatches(theirs, mine, exempt=frozenset(), rtol=0.0,
                                   atol=0.0) == [], case
            for name in ("proj_len", "limit_mth", "t_entry", "duration_mth_init"):
                assert type(mine.cells[name]()) is int, (case, name)
    finally:
        ints.close()
        floats.close()


def test_the_edges_of_the_in_force_interface_are_accepted(sec_model, tmp_path):
    """A zero count, whole numbers in any type, the horizon and each bound's edge are read.

    A count of 0 is a point that projects zeros, and a point paid-up entirely, its full
    cover count 0 and its paid-up strand in force, projects the strand alone: the committed
    row read under a stress of its own.  ``166.0`` is a whole number of months, read back as
    the int the policy clock counts in; a policy issued 120 months after the valuation date,
    the shipped ``future_horizon_mth``, is the last one the table admits, with a frame of
    720 months.  The paid-up point valued at 120, the first policy month a converted policy
    can be in force at, holds its strand.  An escalated cover and premium at the issue
    values, an RPI of 0 since issue, are read; and so is a level point valued after its
    premiums ceased, its premium the last one paid.  And each bound of the contract at its
    edge projects: issue at 18, 1,224 months to the limiting age, and issue at 119, 12
    months, its premiums ceasing at the limiting age, the last cessation the frame reads.
    Then the history's bounds, each at its edge (``Data``'s rules 16 and 17): the
    premiums paid on an escalating point at the premium at issue and at the latest premium
    times the premiums due; on a level point a third of a cent past the premiums due, an
    extract rounded to the cent; the paid-up cover at the sum assured's share at the first
    conversion and at today's cover's share of the payments made; and an odd cessation, 239
    months, at its first paid-up month, 120, where the two shares meet.  And the first
    year's rule at its edge: a month past the first anniversary, its first increase in the
    columns; the paid-up cover at its lower bound on an odd cessation, valued at 200, where
    the upper bound does not meet it; and the premiums paid on an escalating point past
    cessation at the latest premium times the 240 premiums due.  The extra rows are copies
    of committed rows under labels of their own, 21 to 32.
    """
    committed = _committed()
    crossover = _label(committed, "derived", 1, 166)
    future = _label(committed, "future", 4, -13)
    paid_up = _label(committed, "derived", 3, 200)
    rpi = _label(committed, "derived", 4, 186)
    entire = _label(committed, "derived", 3, 180)
    ceased = _label(committed, "derived", 7, 300)
    latest = committed.at[rpi, "premium_pp_init"] * 186
    latest_paid = committed.at[rpi, "premium_pp_init"] * 240
    copies = {21: (paid_up, {"duration_mth": 120, "prem_cum_pp_init": 3600.0,
                             "pu_benefit_pp_init": 2500.0, "crossover_mth_init": -1}),
              22: (rpi, {"cover_pp_init": 5000.0, "premium_pp_init": 30.0,
                         "prem_cum_pp_init": 5580.0, "crossover_mth_init": 166}),
              23: (crossover, {"entry_age": 119, "duration_mth": 0, "prem_cum_pp_init": 0.0,
                               "cessation_months": 12}),
              24: (rpi, {"prem_cum_pp_init": 5580.0}),
              25: (rpi, {"prem_cum_pp_init": latest}),
              26: (paid_up, {"pu_benefit_pp_init": 2500.0}),
              27: (paid_up, {"pu_benefit_pp_init": 5000.0 * 200 / 240}),
              28: (paid_up, {"cessation_months": 239, "duration_mth": 120,
                             "prem_cum_pp_init": 3600.0,
                             "pu_benefit_pp_init": 5000.0 * 120 / 239,
                             "crossover_mth_init": -1}),
              29: (_label(committed, "derived", 1, 6), {"prem_cum_pp_init": 180.004}),
              30: (_label(committed, "derived", 6, 12),
                   {"duration_mth": 13, "cover_pp_init": 157500.0,
                    "premium_pp_init": 111.375, "prem_cum_pp_init": 1215.0 + 111.375}),
              31: (paid_up, {"cessation_months": 239,
                             "pu_benefit_pp_init": 5000.0 * 120 / 239}),
              32: (rpi, {"duration_mth": 250, "prem_cum_pp_init": latest_paid})}

    def edit(table):
        extra = []
        for label, (source, changes) in copies.items():
            row = table.loc[[source]].assign(policy_id=f"WOL-9000{label}", **changes)
            row.index = pd.Index([label], name="point_id")
            extra.append(row)
        table = pd.concat([table, *extra])
        table = _set("policy_count", [crossover], 0.0)(table)
        table = table.assign(duration_mth=table["duration_mth"].astype(float))
        table = _set("duration_mth", [future], -120.0)(table)
        table = _set("entry_age", [5], 18)(table)
        return table

    model = _read_edited(tmp_path, edit)
    try:
        read = model.Data.model_point_table()
        assert read["duration_mth"].dtype == float
        df = _point(model, crossover).result_cf()
        assert len(df) == 434 and (df == 0.0).all().all()
        p = _point(model, entire)
        assert (p.policy_count(), p.duration_mth(0)) == (0.0, 180)
        assert type(p.duration_mth(0)) is int
        pols = p.result_cf()
        assert (pols["pols_if"] == 0.0).all() and (pols["premiums"] == 0.0).all()
        assert pols["pols_pu"].iloc[0] == p.pols_pu_init() > 0.0
        assert (pols["claims_death_pu"] > 0.0).any() and p.check_pols_roll_fwd()
        late = _point(model, future)
        assert (late.t_entry(), late.proj_len(), late.pols_new_biz(120)) == (120, 720, 1.0)
        first = _point(model, 21)
        assert first.pols_pu(0) == first.pols_pu_init() > 0.0
        assert len(first.result_cf()) == first.proj_len() == 480
        flat = _point(model, 22)
        assert flat.cover_pp(0) == 5000.0 and flat.premium_pp(0) == 30.0
        assert flat.cover_pp(6) == pytest.approx(5150.0, rel=1e-12)
        last = _point(model, 23)
        assert len(last.result_cf()) == last.proj_len() == 12
        assert last.cessation_mths() == last.limit_mth() and last.crossover_mth() == -1
        old = _point(model, ceased)
        assert old.premium_pp_init() == 45.0 and old.premium_pp(0) == 0.0
        assert len(old.result_cf()) == 360
        young = _point(model, 5)
        assert len(young.result_cf()) == young.proj_len() == 1224
        assert young.check_pols_roll_fwd() and young.check_truncation()
        for label in (24, 25):
            edge = _point(model, label)
            assert edge.prem_cum_pp(0) == edge.prem_cum_pp_init() + edge.premium_pp(0)
        assert _point(model, 25).prem_cum_pp_init() == latest
        for label in (26, 27, 28):
            edge = _point(model, label)
            assert edge.pu_benefit(0) == edge.pols_pu_init() * edge.pu_benefit_pp_init()
            assert edge.pols_pu(0) > 0.0 and edge.proj_len() > 0
        odd = _point(model, 28)
        assert (odd.cessation_mths(), odd.duration_mth(0)) == (239, 120)
        refund = _point(model, 29)
        assert refund.benefit_pp(0, _code(refund, "NON_ACC")) == 180.004 + 30.0
        second = _point(model, 30)
        assert (second.duration_init(), second.cover_pp(0)) == (1, 157500.0)
        odd = _point(model, 31)
        assert odd.pu_benefit_pp_init() == 5000.0 * 120 / 239
        assert odd.pu_benefit(0) == odd.pols_pu_init() * odd.pu_benefit_pp_init()
        ceased = _point(model, 32)
        assert ceased.prem_cum_pp(0) == latest_paid and ceased.premium_pp(0) == 0.0
    finally:
        model.close()


def _every_state_months(start, end, cessation):
    """The S months a point whose S frame runs from ``start`` to ``end`` is restated at.

    By default the edges of its windows (USLIB-SEC-PLAN.md §5.2, T5): every month of the
    first policy year and the first anniversary, through which the moratorium, the suicide
    window and ``Data``'s first-year rule end, each anniversary and the month before it,
    which takes in the first conversion at half the payments and cessation, each month of
    the year the crossover falls in on any S point, and the last month of the frame.  With
    ``UKLIB_SEC_FULL=1``, every month.  Each after ``start``, the twin's month.
    """
    if SEC_FULL:
        return list(range(start + 1, end))
    months = {*range(1, 14), end - 1, *(m for a in range(12, end, 12) for m in (a - 1, a)),
              *range(160, 192), *range(636, 648), *range(216, 228)}
    if cessation > 0:
        months |= {cessation // 2 - 1, cessation // 2, -(-cessation // 2)}
    return sorted(m for m in months if start < m < end)


def _states(s):
    """Each ``(S point, month)`` of :func:`_every_state_months` on every point of ``s``."""
    table = s.Data.model_point_table()
    return [(point_id, d) for key, point_id in zip(point_keys(s), table.index)
            for d in _every_state_months(0, projection(s, key).proj_len(),
                                         int(table.at[point_id, "cessation_months"]))]


def _restated(root, s, states):
    """The twins of ``s``'s points and a row in force at each of ``states``, ``(S point,
    month)``, built by the generator out of ``s`` into a copy of the product directory:
    ``(folder, table)``."""
    spec = dataclasses.replace(SPEC, derived=tuple(states), future=(), derived_refs={})
    table, _ = build_sec_table(spec, s)
    return _sec_inputs(root, table), table


def _states_apart(a, b):
    """The state columns, the counts among them, in which two tables of :func:`_restated`
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


# The stress that lapses every policy past its crossover, as the committed row paid-up
# entirely is read under: S reaches a full-cover count of 0 with paid-up policies in force
# under it, and under no other set of inputs.
LAPSE_ALL = {**SPLICED_REFS, "lapse_crossover_beta": 100.0}

# The other inputs that move the states S reaches, each moving the cover, the premium, the
# premiums paid and the crossover of an escalating point: an RPI of 8%, under which the
# RPI point's premiums rise faster and it crosses at 201, and a take-up of a half, under
# which both escalating points take half their increases.
RPI_SET = {"rpi_rate": 0.08}
TAKE_UP_SET = {"esc_take_up": 0.5}
ESCALATED = {"cover_pp_init", "premium_pp_init", "prem_cum_pp_init", "crossover_mth_init"}


def test_every_state_s_reaches_is_accepted_in_force(s_model, spliced, tmp_path):
    """Every state ``WOL_UK_S`` reaches is a valid opening state (T5).

    ``Data``'s rules and ``proj_len()``'s hold an opening state to what a policy in force
    can be, so they must accept each state the S model reaches: a rule exercised only on
    the rows the other tests choose could refuse a state S reaches elsewhere (D6).  So each
    point of S is restated in force by the generator at the edges of its windows, or with
    ``UKLIB_SEC_FULL=1`` at every month of its frame (:func:`_every_state_months`), into
    one table beside the twins: ``Data`` reads it, and no row's ``proj_len()`` refuses it
    (USLIB-SEC-PLAN.md §5.2, T5, precised at M10).  The splice's stress moves three of the
    states S reaches: the full-cover count, the paid-up count and the paid-up cover per
    policy, through the stressed lapses and conversions past the crossover.  It leaves
    alone the premiums paid, the cover, the premium and the crossover, which per policy no
    decrement moves.  A stress that lapses every policy moves the counts to a full-cover
    count of 0 with paid-up policies in force, which no other set reaches.  The RPI and the
    take-up move the other four on an escalating point: its cover, its premium, its
    premiums paid and its crossover.  Expense inflation and improvement move no state, each
    at 0 or on the valuation clock.  So the test runs on each set of inputs on which those
    states differ (precised at M9), and asserts which states each moves:

    * S as shipped, its seven points under its own References, as T1 and the committed rows
      read it (``s_model``);
    * the splice's, its points and five variants under :data:`SPLICED_REFS`, the stress
      on (``spliced``), an odd cessation among them;
    * the stress that lapses every policy, :data:`LAPSE_ALL`, on S's points, whose paid-up
      point is paid-up entirely from policy month 167;
    * an RPI of 8%, :data:`RPI_SET`, on S's points, the RPI point crossing at 201;
    * a take-up of a half, :data:`TAKE_UP_SET`, on S's points, both escalating points
      taking half their increases.

    ``WOL_UK_SEC`` refuses no state ``WOL_UK_S`` reaches, so none is set aside.
    """
    extra = {"lapse_all": LAPSE_ALL, "rpi": RPI_SET, "take_up": TAKE_UP_SET}
    read = {tag: mx.read_model(model_path(TWIN), name=_name(tag)) for tag in extra}
    try:
        for tag, refs in extra.items():
            for ref, value in refs.items():
                setattr(read[tag].Projection, ref, value)
        sets = {"shipped": (s_model, {}), "spliced": (spliced[0], SPLICED_REFS),
                **{tag: (read[tag], refs) for tag, refs in extra.items()}}
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
        for model in read.values():
            model.close()
    assert not found, found
    shipped, every = states["shipped"], states["lapse_all"]
    apart = _states_apart(shipped, states["spliced"])
    assert apart == {"policy_count", "pols_pu_init", "pu_benefit_pp_init"}, apart
    entire = every[(every["policy_count"] == 0.0) & (every["pols_pu_init"] > 0.0)]
    assert len(entire), "no state paid-up entirely"
    for tag in ("rpi", "take_up"):
        apart = _states_apart(shipped, states[tag])
        assert apart == ESCALATED, (tag, apart)


# ---------------------------------------------------------------------------
# The assumption tables
#
# Data checks each table before a value of it is read, in the cell the projection takes
# its extent from, reading the file as it stands (UKLIB-SEC-PLAN.md §4; USLIB-SEC-PLAN.md
# §7.1, *Precised at M3*, item 9).  Each case is the shipped tables with one fault, read
# from a copy, refused by its Data cell alone, naming the file, the column and its lines,
# the header line 1, and through a projection of the anchor cell, which reads both tables.
# The lines are the shipped files': mort_table.csv holds each basis, sex and smoker group at
# ages 18 to 120, 103 lines a group, assured F NS on lines 2 to 104, then assured F S,
# assured M NS, assured M S, population F NS from line 414, population F S, population M NS
# and population M S on lines 723 to 825; lapse_table.csv O50's policy years 1 to 6 on
# lines 2 to 7 and UW's on lines 8 to 13.


def _written(column, value, where):
    """An edit of a table that writes ``value`` into ``column`` on the rows ``where``
    picks."""
    def edit(table):
        cells = table[column].astype(object)
        cells[where(table)] = value
        return table.assign(**{column: cells})
    return edit


def _rate_at(basis, sex, smoker, age):
    return lambda t: ((t["basis"] == basis) & (t["sex"] == sex) & (t["smoker"] == smoker)
                      & (t["age"] == age))


def _group(basis, sex, smoker):
    return lambda t: (t["basis"] == basis) & (t["sex"] == sex) & (t["smoker"] == smoker)


def _year(cell, year):
    return lambda t: (t["cell"] == cell) & (t["policy_year"] == year)


def _dropped(where):
    return lambda table: table[~where(table)].reset_index(drop=True)


def _repeated(where):
    return lambda table: pd.concat([table, table[where(table)]], ignore_index=True)


MORT = "mort_table.csv"
LAPSE = "lapse_table.csv"
RATE = f"{MORT}: mort_rate must be a number from 0 to 1; it is not on line "
AGES = (f"{MORT}: the ages of each basis, sex and smoker status must run from 18 to 120, "
        f"the table's first and last, one row an age, none below 0; ")
LAPSE_RATE = f"{LAPSE}: lapse_rate must be a number from 0 to 1; it is not on line "
YEARS = (f"{LAPSE}: the policy years of each cell must run from 1, one row a year, without a "
         f"gap or a repeat; ")

# A table a reader cannot read, or whose value is not a number in its range, as (case, the
# file, its edit, the Data cell that refuses it, its message).  A value no point reads is
# refused too: the assured female smoker's rates, which no committed point reaches.
UNREADABLE = [
    ("a blank rate", MORT, _written("mort_rate", float("nan"),
                                    _rate_at("population", "F", "NS", 70)),
     "mort_age_first", RATE + "[466]"),
    ("a text rate", MORT, _written("mort_rate", "low", _rate_at("assured", "F", "S", 50)),
     "mort_age_first", RATE + "[137]"),
    ("an infinite rate", MORT, _written("mort_rate", float("inf"),
                                        _rate_at("assured", "M", "NS", 40)),
     "mort_age_first", RATE + "[230]"),
    ("a negative rate", MORT, _written("mort_rate", -0.001,
                                       _rate_at("population", "M", "S", 65)),
     "mort_age_first", RATE + "[770]"),
    ("a rate past 1", MORT, _written("mort_rate", 1.5, _rate_at("assured", "F", "NS", 100)),
     "mort_age_first", RATE + "[84]"),
    ("two lines at fault", MORT, _then(
        _written("mort_rate", float("nan"), _rate_at("assured", "F", "NS", 18)),
        _written("mort_rate", float("nan"), _rate_at("population", "M", "S", 120))),
     "mort_age_first", RATE + "[2, 825]"),
    ("an age not whole", MORT, _written("age", 45.5, _rate_at("assured", "M", "S", 45)),
     "mort_age_first", f"{MORT}: age must be a whole number; it is not on line [338]"),
    ("an age written as text", MORT, _written("age", "x", _rate_at("population", "F", "S", 18)),
     "mort_age_first", f"{MORT}: age must be a whole number; it is not on line [517]"),
    ("an unknown basis", MORT, _written("basis", "select", _rate_at("assured", "F", "NS", 20)),
     "mort_age_first", f"{MORT}: basis must be population or assured, sex M or F, and "
                       f"smoker NS or S; they are not on line [4]"),
    ("term assurance's smoker code", MORT,
     _written("smoker", "N", _rate_at("population", "M", "NS", 30)),
     "mort_age_first", f"{MORT}: basis must be population or assured, sex M or F, and "
                       f"smoker NS or S; they are not on line [632]"),
    ("an age twice", MORT, _repeated(_rate_at("assured", "M", "NS", 60)), "mort_age_first",
     AGES + "basis assured, sex M, smoker NS, age 60 repeats on lines [250, 826]"),
    ("a group missing", MORT, _dropped(_group("population", "M", "S")), "mort_age_first",
     AGES + "no line holds basis population, sex M, smoker S, ages 18 to 120"),
    ("a gap in a group", MORT, _dropped(_rate_at("assured", "F", "S", 80)), "mort_age_first",
     AGES + "no line holds basis assured, sex F, smoker S, age 80"),
    ("an age below 0", MORT, _written("age", -1, _rate_at("assured", "F", "NS", 18)),
     "mort_age_first", AGES + "age -1, below 0, is on lines [2]; no line holds basis "
                              "assured, sex F, smoker NS, age 18"),
    ("a blank lapse rate", LAPSE, _written("lapse_rate", float("nan"), _year("O50", 3)),
     "lapse_last_year", LAPSE_RATE + "[4]"),
    ("a lapse rate past 1", LAPSE, _written("lapse_rate", 1.5, _year("UW", 6)),
     "lapse_last_year", LAPSE_RATE + "[13]"),
    ("a negative lapse rate", LAPSE, _written("lapse_rate", -0.1, _year("O50", 1)),
     "lapse_last_year", LAPSE_RATE + "[2]"),
    ("a text lapse rate", LAPSE, _written("lapse_rate", "high", _year("UW", 2)),
     "lapse_last_year", LAPSE_RATE + "[9]"),
    ("a policy year not whole", LAPSE, _written("policy_year", 2.5, _year("O50", 2)),
     "lapse_last_year", f"{LAPSE}: policy_year must be a whole number; it is not on line [3]"),
    ("an unknown cell", LAPSE, _written("cell", "O60", _year("UW", 1)),
     "lapse_last_year", f"{LAPSE}: cell must be O50 or UW; it is not on line [8]"),
    ("a policy year missing", LAPSE, _dropped(_year("O50", 3)), "lapse_last_year",
     YEARS + "no line holds cell O50, policy_year 3"),
    ("a policy year twice", LAPSE, _repeated(_year("UW", 4)), "lapse_last_year",
     YEARS + "cell UW, policy_year 4 repeats on lines [11, 14]"),
    ("no policy year 1", LAPSE, _dropped(_year("O50", 1)), "lapse_last_year",
     YEARS + "no line holds cell O50, policy_year 1"),
    ("a cell missing", LAPSE, _dropped(lambda t: t["cell"] == "UW"), "lapse_last_year",
     YEARS + "no line holds cell UW, policy_year 1"),
    # A key int64 holds inexactly, 2**53, is refused before the cast (the C step); 2**53 - 1
    # is cast exactly and refused by the gap it leaves, which the check finds from the keys
    # a table holds, so that a key far from the rest costs no more than the rows.
    ("an age of 2**53", MORT, _written("age", 2.0 ** 53, _rate_at("assured", "M", "NS", 70)),
     "mort_age_first", f"{MORT}: age must be below 2**53 in size; it is not on line [260]"),
    ("an age of 2**53 - 1", MORT,
     _written("age", 2 ** 53 - 1, _rate_at("assured", "M", "NS", 70)), "mort_age_first",
     f"{MORT}: the ages of each basis, sex and smoker status must run from 18 to "
     f"{2 ** 53 - 1}, the table's first and last, one row an age, none below 0; "
     + "; ".join(f"no line holds basis {b}, sex {s}, smoker {k}, "
                 + ("age 70; no line holds basis assured, sex M, smoker NS, ages 121 to "
                    f"{2 ** 53 - 2}" if (b, s, k) == ("assured", "M", "NS")
                    else f"ages 121 to {2 ** 53 - 1}")
                 for b in ("population", "assured") for s in ("M", "F")
                 for k in ("NS", "S"))),
    ("a policy year of 2**53", LAPSE, _written("policy_year", 2.0 ** 53, _year("UW", 3)),
     "lapse_last_year", f"{LAPSE}: policy_year must be below 2**53 in size; it is not on "
                        f"line [10]"),
    ("a policy year of 2**53 - 1", LAPSE, _written("policy_year", 2 ** 53 - 1,
                                                   _year("UW", 3)), "lapse_last_year",
     YEARS + f"no line holds cell UW, policy_year 3; no line holds cell UW, policy years 7 "
             f"to {2 ** 53 - 2}"),
]


@pytest.mark.parametrize("case, file, edit, cell, message", UNREADABLE,
                         ids=[c[0] for c in UNREADABLE])
def test_a_table_a_reader_cannot_read_is_refused_naming_its_lines(tmp_path, case, file, edit,
                                                                  cell, message):
    """``Data`` refuses an assumption table before a value of it is read (§4, T5).

    ``WOL_UK_S`` reads a blank rate as NaN, which its cap would keep and every flow carry;
    an infinite one, which the cap reads as certain death; a negative one, a lapse rate
    past 1 whose monthly rate has no real value, and a key that is not whole as one ``int``
    truncates; and a gap in a group or a cell's year as a ``KeyError``, only where a
    projection reaches it.  Here the cell the projection asks first refuses each, naming the
    file, the column and its lines (:data:`UNREADABLE`), and so does a projection of the
    anchor cell, which reads both tables: ``Data.mort_age_first`` the mortality table and
    ``Data.lapse_last_year`` the lapse table, each cell's last year at once; and so does
    each table's array, which asks its check first.
    """
    model = _read_edited(tmp_path, lambda t: t, edits={file: edit})
    try:
        _refused(model.Data.cells[cell], message)
        array = "mort_table_array" if file == MORT else "lapse_table_array"
        _refused(model.Data.cells[array], message)
        _refused(_point(model, 1).result_cf, message)
    finally:
        model.close()


def test_a_read_beyond_the_mortality_table_is_refused_naming_its_point(tmp_path):
    """An attained age the mortality table lacks is refused by the cell that reads it.

    ``proj_len()`` holds the limiting age to a year past the table's last age, and the
    issue age to ``issue_age_min``, the table's first, so no frame the shipped References
    admit reads past the table.  With ``issue_age_min`` lowered to 10, a point issued at 15
    is admitted by the frame and reads an age the table, from 18, lacks: ``mort_rate``
    refuses it, naming the point and the age, where ``WOL_UK_S``'s lookup raised
    ``KeyError``, and so does every report.  The bound is a Reference, so it is what admits
    the point.
    """
    model = _read_edited(tmp_path, _set("entry_age", [5], 15))
    try:
        model.Projection.issue_age_min = 10
        p = _point(model, 5)
        assert p.proj_len() == 12 * (120 - 15)
        message = "point_id 5: mort_table.csv has no rate at attained age 15"
        _refused(lambda: p.mort_rate(0), message)
        _refused(p.result_cf, message)
        assert p.mort_rate_mth(36) > 0.0
    finally:
        model.close()


# The rows the float keys are read on, by what they are: the anchor cell, the underwritten
# cell and the male smoker, issued at the valuation date; the paid-up point and the RPI
# point in force; and the RPI point issued 13 months on.
FLOAT_KEYED = (("twin", 1, 0), ("twin", 5, 0), ("twin", 7, 0), ("derived", 3, 200),
               ("derived", 4, 186), ("future", 4, -13))


def test_a_key_written_as_a_float_reads_as_wol_uk_s_reads_it(sec_model, tmp_path):
    """A key written ``70.0`` is the key 70, in every table and in every extent.

    ``WOL_UK_S``'s lookups match a float key to the int the projection asks, so a table
    written by a tool that writes every number with a decimal point reads the same.  Each
    assumption table's keys and the model point table's ``duration_mth`` are written as
    floats, and a point of each cell, sex and smoker status, issued at the valuation date,
    in force on both strands and to be issued later, projects what the committed tables
    project, exactly (:data:`FLOAT_KEYED`): between them they read both tables over every
    age from 40 to 119 and every policy year.
    """
    def as_float(column):
        return lambda table: table.assign(**{column: table[column].astype(float)})

    edits = {MORT: as_float("age"), LAPSE: as_float("policy_year")}
    model = _read_edited(tmp_path, as_float("duration_mth"), edits=edits)
    committed = _committed()
    points = [_label(committed, *case) for case in FLOAT_KEYED]
    try:
        for point_id in points:
            for report in ("result_cf", "result_pols"):
                assert frame_mismatches(_point(sec_model, point_id).cells[report](),
                                        _point(model, point_id).cells[report](),
                                        rtol=0, atol=0) == [], (point_id, report)
    finally:
        model.close()


# ---------------------------------------------------------------------------
# T6 -- regeneration


def test_the_committed_sec_inputs_are_what_s_generates():
    """``model_point_table_sec.csv`` is what WOL_UK_S and its table generate today.

    Every row and column, the text cells and the five opening-state columns included: an
    edit to an S row the table copies or derives from, or to an S formula a row's state is
    read from, fails here until ``python tools/gen_sec_points.py WOL_UK_SEC`` regenerates
    it, in the same commit.  Text and integers compare exactly, and a float by its value, to
    1e-12, because the text the writer picks for a computed float depends on the platform's
    parser (§5).  The generator reads S itself: the rows of the spec's ``derived_refs`` are
    read with References set on S, which drops what an S model given to it had cached.
    """
    assert check_generated(SEC) == []


# ---------------------------------------------------------------------------
# The product's own facts


def test_the_two_clocks_on_the_shipped_points(sec_model):
    """``t`` counts from the valuation date; ``duration_mth(t)`` from issue (D3, D4).

    On a twin of S's new business the two coincide, and its policies enter as new business
    at ``t = 0``.  The paid-up point valued 200 months after issue is in policy year 17 at
    attained age 86 at ``t = 0``, has 400 months to the limiting age, and is on the books
    from ``t = 0`` on both strands with no new business; its premiums cease at ``t = 40``,
    policy month 240.  The RPI point valued at 186 steps its increases at ``t = 6``, policy
    month 192.  The point issued 13 months on has nothing in force and nothing to do before
    ``t = 13``, and a frame of 613 months; its increase steps at ``t = 25``.  A timing the
    model does not know is refused rather than answered with another count.
    """
    twin = _row(sec_model, "twin", 1, 0)
    assert [twin.duration_mth(t) for t in (0, 1, 599)] == [0, 1, 599]
    assert (twin.t_entry(), twin.pols_if_init(), twin.pols_new_biz(0), twin.pols_if(0)) == (
        0, 0.0, 1.0, 1.0)
    assert (twin.limit_mth(), twin.proj_len()) == (600, 600)
    old = _row(sec_model, "derived", 3, 200)
    assert (old.duration_mth(0), old.duration(0), old.policy_year(0), old.age(0)) == (
        200, 16, 17, 86)
    assert (old.proj_len(), old.t_entry(), old.pols_new_biz(0)) == (400, 0, 0.0)
    assert old.is_active(399) and not old.is_active(400)
    assert old.pols_if(0) == old.pols_if_init() == old.policy_count()
    assert old.pols_pu(0) == old.pols_pu_init() > 0.0
    assert old.premium_pp(39) == 30.0 and old.premium_pp(40) == 0.0
    idx = _row(sec_model, "derived", 4, 186)
    assert idx.cover_pp(5) == idx.cover_pp_init() == pytest.approx(5000 * 1.03 ** 15,
                                                                   rel=1e-12)
    assert idx.cover_pp(6) == pytest.approx(idx.cover_pp_init() * 1.03, rel=1e-12)
    fut = _row(sec_model, "future", 4, -13)
    assert (fut.duration_mth(0), fut.t_entry(), fut.proj_len()) == (-13, 13, 613)
    assert not fut.is_active(12) and fut.is_active(13)
    assert (fut.pols_if_init(), fut.pols_new_biz(13), fut.pols_if(13)) == (0.0, 1.0, 1.0)
    assert fut.cover_pp(24) == 5000.0
    assert fut.cover_pp(25) == pytest.approx(5150.0, rel=1e-12)
    _refused(lambda: old.pols_if_at(0, "BEF_NOTHING"), "invalid timing")


def test_the_committed_rows_continue_their_s_points(sec_model, s_model):
    """Each committed row in force, or issued later, is its S point from its month on.

    T6 compares a float to 1e-12, which pins a small count only to that much of itself, so
    each committed row is compared with its S point frame by frame and cell by cell, at the
    shipped assumptions (USLIB-SEC-PLAN.md §7.1, *Precised at M3*, item 11): the six
    derived rows from their months, and the row issued 13 months on from S's issue month,
    all to 1e-9 relative with no absolute floor but on the residual, every cell but those
    expense inflation moves (:func:`_continues_s`), which the inflation test holds.  The
    rows read from S under References of their own are S's under them, which the test after
    this one compares.
    """
    table = sec_model.Data.model_point_table()
    found = []
    for point_id in table.index:
        kind, month = table.at[point_id, "row_kind"], int(table.at[point_id, "source_mth"])
        if kind == "twin" and month == 0:
            continue
        policy = table.at[point_id, "source_policy_id"]
        if (policy, month) in UNDER_REFS:
            continue
        s_point = int(s_model.Data.model_point_table().index[
            s_model.Data.model_point_table()["policy_id"] == policy][0])
        found += [f"point {point_id}: {line}" for line in _continues_s(
            _point(s_model, s_point), _point(sec_model, point_id), month)]
    assert not found, found[:20]


# Whether each committed row read under References of its own is S's under them through its
# whole frame at the shipped References.  Rows 15 and 16 are valued on their tenth
# anniversary, whose increase is the projection's first event, made at today's References,
# so they part from S under theirs at t = 0, in the cover and the premium and all that
# reads them, and are S's in their counts throughout, since neither moves a decrement.
# The stress lapses nothing on a point with no full cover, so row 17, paid-up entirely, is
# S's throughout, but in the lapse rates themselves, which weight no policy.
UNDER_REFS_THROUGHOUT = {("WOL-000004", 120): False, ("WOL-000006", 120): False,
                         ("WOL-000003", 180): True}
UNDER_REFS_RATES = frozenset({"lapse_rate", "lapse_rate_mth"})


def test_the_committed_rows_under_references_of_their_own_are_s_under_them(sec_model):
    """Each row read from S under References of its own holds S's history under them, and
    projects today's References from the valuation date on (§6.4, K14).

    At S's References each history is what today's References rebuild, so the spec reads
    three rows from S under References of their own, which its ``derived_refs`` records
    (:data:`UNDER_REFS`): the RPI point at 120 under an RPI of 5%, its cover and premium
    1.05 and 1.075 to the ninth power, the year its tenth anniversary closes; the
    underwritten increasing point at 120 under a take-up of a half, its increases 2.5% and
    5% a year; and the paid-up point at 180 under a stress of 100, paid-up entirely.  Each
    row's opening state is S's under them before month 0's events: the premiums paid to
    the end of month ``d - 1`` and the cover and premium of that month.  At the shipped
    References the committed model projects each from that history: the first two make
    their tenth anniversary's increase at ``t = 0`` at today's References, the cover S's of
    month ``d - 1`` times ``1 +`` today's step, where S under theirs steps at its own, and
    their counts are S's throughout (:data:`UNDER_REFS_THROUGHOUT`); the third is S's under
    its stress over the whole frame, in every cell S evaluates and both reports, to 1e-9
    relative with no absolute floor but on the residual, but in the lapse rates, which on a
    point with no full cover multiply nothing, and those expense inflation moves
    (:func:`_continues_s`).  The history is history.  And with each row's References set in
    both models the row is S's in every month of its frame.  Each Reference is set on a
    model just read (K7).
    """
    assert set(UNDER_REFS) == set(UNDER_REFS_THROUGHOUT), UNDER_REFS
    counts = ["pols_if", "pols_pu", "pols_death", "pols_lapse", "pols_convert"]
    for (policy, d), refs in UNDER_REFS.items():
        s_point = int(policy.rsplit("-", 1)[1])
        row = _row(sec_model, "derived", s_point, d)
        s = mx.read_model(model_path(TWIN), name=_name("under"))
        try:
            for ref, value in refs.items():
                setattr(s.Projection, ref, value)
            sp = _point(s, s_point)
            _sweep_s(sp)
            assert (row.prem_cum_pp_init(), row.cover_pp_init(), row.premium_pp_init()) == (
                sp.prem_cum_pp(d - 1), sp.cover_pp(d - 1), sp.premium_pp(d - 1)), policy
            assert frame_mismatches(sp.result_pols(), row.result_pols(), t_offset=d,
                                    columns=counts, atol=0.0) == [], (policy, d)
            if UNDER_REFS_THROUGHOUT[(policy, d)]:
                exempt = SPLICE_EXEMPT | INFLATION_CELLS | UNDER_REFS_RATES
                found = _mismatches(sp, row, t_offset=d, exempt=exempt | RESIDUALS,
                                        atol=0.0, codes=codes(row))
                found += _mismatches(sp, row, t_offset=d,
                                         exempt=exempt | (set(sp.cells) - RESIDUALS),
                                         codes=codes(row))
                keep = [c for c in sp.result_cf().columns if c not in INFLATED]
                pols = [c for c in sp.result_pols().columns if c not in UNDER_REFS_RATES]
                for report, columns in (("result_cf", keep), ("result_pols", pols)):
                    found += [f"{report}: {line}" for line in frame_mismatches(
                        sp.cells[report](), row.cells[report](), t_offset=d,
                        columns=columns, atol=0.0)]
                assert not found, (policy, d, found[:20])
            else:
                for name, step in (("cover_pp", row.esc_cover_step()),
                                   ("premium_pp", row.esc_prem_step())):
                    mine, theirs = row.cells[name](0), sp.cells[name](d)
                    assert mine == pytest.approx(sp.cells[name](d - 1) * (1.0 + step),
                                                 rel=1e-12), (policy, name)
                    assert mine != pytest.approx(theirs, rel=1e-9), (policy, name)
        finally:
            s.close()
        sec = mx.read_model(model_path(SEC), name=_name("under_sec"))
        s = mx.read_model(model_path(TWIN), name=_name("under_s"))
        try:
            for model in (sec, s):
                for ref, value in refs.items():
                    setattr(model.Projection, ref, value)
            sp = _point(s, s_point)
            _sweep_s(sp)
            assert _continues_s(sp, _row(sec, "derived", s_point, d), d) == [], (policy, d)
        finally:
            sec.close()
            s.close()


def _rpi_history(path, months, premium=30.0, cover=5000.0, cessation=240):
    """The cover, the premium and the premiums paid before policy month ``months``' events
    on a policy whose RPI at each anniversary ``y`` was ``path[y - 1]``, as the contract
    gives them: the cover up by the RPI floored at 0 and capped at 10%, the premium by 1.5
    times it capped at 15%, at each anniversary, and a premium paid at the start of each
    month to cessation.  ``(cover, premium, premiums paid)``: the cover and premium of
    month ``months - 1``, an anniversary at ``months`` being the projection's, the premium
    the last one paid once premiums have ceased, and the premiums paid to the end of month
    ``months - 1``."""
    paid = 0.0
    for m in range(months):
        if m and m % 12 == 0:
            r = path[m // 12 - 1]
            cover *= 1.0 + min(max(r, 0.0), 0.10)
            premium *= 1.0 + min(max(1.5 * r, 0.0), 0.15)
        if m < cessation:
            paid += premium
    return cover, premium, paid


# An RPI that held at 0 for ten years and then rose to 12% a year, past the caps: a
# history no flat rpi_rate gives, which leaves the RPI point at its policy month 186 with a
# cover of 5,000 x 1.1^5, a premium of 30 x 1.15^5, and premiums paid of 30 x 132 for the
# first eleven years and the capped increases after.
RPI_PATH = (0.0,) * 10 + (0.12,) * 10


def test_the_cover_history_is_read_from_the_model_point(sec_model, tmp_path):
    """The cash sum's increases already given are the point's, not recomputed (K14).

    ``WOL_UK_S`` rebuilds the RPI variant's cover from issue at today's flat ``rpi_rate``,
    so a model that dropped the column and did the same would pass the splice, since S and
    the splice rebuild it alike.  So the RPI point at 186 is projected with the cover of
    :data:`RPI_PATH`, which no flat rate gives: its cash sum is that through the policy year
    under way, and times 1.03 for each anniversary after, at today's RPI; the claims on a
    death pay it, beyond the moratorium.  The committed row's own cover, at today's 3% since
    issue, is 5,000 x 1.03^15, and projects as that.
    """
    row = _label(_committed(), "derived", 4, 186)
    cover, premium, paid = _rpi_history(RPI_PATH, 186)
    assert cover == pytest.approx(5000.0 * 1.1 ** 5, rel=1e-12)
    model = _read_edited(tmp_path, _then(_set("cover_pp_init", [row], cover)))
    try:
        p = _point(model, row)
        death = _code(p, "DEATH")
        for t, years in ((0, 0), (5, 0), (6, 1), (30, 3), (413, 34)):
            assert p.cover_pp(t) == pytest.approx(cover * 1.03 ** years, rel=1e-12), t
            assert p.benefit_pp(t, death) == p.cover_pp(t), t
        q = _point(sec_model, row)
        assert q.cover_pp(0) == pytest.approx(5000.0 * 1.03 ** 15, rel=1e-12)
        assert p.cover_pp(0) != pytest.approx(q.cover_pp(0), rel=1e-6)
    finally:
        model.close()


def test_the_premium_history_is_read_from_the_model_point(sec_model, tmp_path):
    """The premium's increases already given are the point's, not recomputed (K14).

    ``WOL_UK_S`` rebuilds the RPI variant's premium from issue at today's flat ``rpi_rate``
    as it does the cover.  So the RPI point at 186 is projected with the premium of
    :data:`RPI_PATH`, 30 x 1.15^5: its premium is that through the policy year under way,
    times 1.045 for each anniversary after, at 1.5 times today's RPI, to cessation at policy
    month 240, ``t = 54``, and nothing from then on; the premiums paid add it month by month.
    """
    row = _label(_committed(), "derived", 4, 186)
    _, premium, _ = _rpi_history(RPI_PATH, 186)
    assert premium == pytest.approx(30.0 * 1.15 ** 5, rel=1e-12)
    model = _read_edited(tmp_path, _set("premium_pp_init", [row], premium))
    try:
        p = _point(model, row)
        for t, years in ((0, 0), (5, 0), (6, 1), (53, 4)):
            assert p.premium_pp(t) == pytest.approx(premium * 1.045 ** years, rel=1e-12), t
        assert p.premium_pp(54) == 0.0 and p.premium_pp(100) == 0.0
        assert p.prem_cum_pp(1) == p.prem_cum_pp(0) + p.premium_pp(1)
        assert _point(sec_model, row).premium_pp(0) == pytest.approx(30.0 * 1.045 ** 15,
                                                                      rel=1e-12)
    finally:
        model.close()


def test_the_premiums_paid_are_read_from_the_model_point(sec_model, tmp_path):
    """The premiums already paid are the point's, not rebuilt from the schedule (K14).

    ``WOL_UK_S`` sums the premiums from issue at today's RPI, so a model that rebuilt them
    from the schedule would pass the splice.  The stress on the lapse rate compares them
    with the cover in every month, so the RPI point at 186 is projected under a stress of
    0.5 with the whole history of :data:`RPI_PATH`, which never crossed: its premiums paid,
    6,389.30, below its cover of 8,052.55, cross it at ``t`` = 37, policy month 223, where
    the stressed lapse starts, and the crossover, a policy month, is found there, searched
    forward from the columns.  At today's 3% since issue the row's premiums paid exceed its
    cover from month 0, and stress it there.  And the moratorium refunds of the anchor cell
    valued at 6 pay the premiums it carries in plus the month's: the 180 it holds, and
    180.004, which ``Data`` reads, an extract rounded to the cent, where a refund rebuilt
    from the premium schedule would pay 180.
    """
    row = _label(_committed(), "derived", 4, 186)
    cover, premium, paid = _rpi_history(RPI_PATH, 186)
    model = _read_edited(tmp_path, _then(_set("cover_pp_init", [row], cover),
                                         _set("premium_pp_init", [row], premium),
                                         _set("prem_cum_pp_init", [row], paid),
                                         _set("crossover_mth_init", [row], -1)))
    try:
        model.Projection.lapse_crossover_beta = 0.5
        p = _point(model, row)
        assert p.prem_cum_pp(0) == pytest.approx(paid + premium, rel=1e-15)
        crossing = next(t for t in range(p.proj_len()) if p.prem_cum_pp(t) > p.cover_pp(t))
        for t in range(crossing):
            assert p.lapse_rate(t) == p.lapse_rate_base(t), t
        assert p.lapse_rate(crossing) == pytest.approx(1.5 * p.lapse_rate_base(crossing),
                                                       rel=1e-12)
        assert (crossing, p.crossover_mth()) == (37, 223)
        assert (round(paid, 2), round(cover, 2)) == (6389.30, 8052.55)
        shipped = _point(sec_model, row)
        assert shipped.prem_cum_pp(0) > shipped.cover_pp(0) and crossing > 0
    finally:
        model.close()
    anchor = _row(sec_model, "derived", 1, 6)
    non_acc = _code(anchor, "NON_ACC")
    assert anchor.prem_cum_pp_init() == 180.0
    assert [anchor.benefit_pp(t, non_acc) for t in (0, 5, 6)] == [210.0, 360.0, 5000.0]
    label = anchor.point_id()
    model = _read_edited(tmp_path / "cent", _set("prem_cum_pp_init", [label], 180.004))
    try:
        p = _point(model, label)
        assert [p.benefit_pp(t, _code(p, "NON_ACC")) for t in (0, 5)] == [
            180.004 + 30.0, 180.004 + 30.0 + 150.0]
    finally:
        model.close()


def test_the_fixed_increases_taken_up_are_read_from_the_model_point(sec_model):
    """The underwritten variant's increases taken up are the point's (K14).

    ``WOL_UK_S`` rebuilds the fixed increases from issue at today's ``esc_take_up``, so a
    take-up changed at the valuation date would reach back over every increase already
    given, though they are history, a fact of the contract, as the RPI's are.  The cover and
    premium columns carry them on the fixed variant as on the RPI one: the committed row of
    the underwritten increasing point at 120, read from S under a take-up of a half, holds a
    cover of 150,000 x 1.025^9 and a premium of 101.25 x 1.05^9, the year its tenth
    anniversary, at the valuation date, closes; and at today's take-up of 1 its cover steps
    by 5% and its premium by 10% at that anniversary, ``t = 0``, and each after, from
    those.  With the take-up raised to 1 at the valuation date in ``WOL_UK_S`` the whole
    history would be 1.05^10 and 1.1^10.
    """
    row = _row(sec_model, "derived", 6, 120)
    assert row.cover_pp_init() == pytest.approx(150000.0 * 1.025 ** 9, rel=1e-12)
    assert row.premium_pp_init() == pytest.approx(101.25 * 1.05 ** 9, rel=1e-12)
    for t, years in ((0, 1), (11, 1), (12, 2), (60, 6)):
        assert row.cover_pp(t) == pytest.approx(row.cover_pp_init() * 1.05 ** years,
                                                rel=1e-12), t
        assert row.premium_pp(t) == pytest.approx(row.premium_pp_init() * 1.1 ** years,
                                                  rel=1e-12), t
    assert row.cover_pp(0) != pytest.approx(150000.0 * 1.05 ** 10, rel=1e-6)


def test_an_anniversary_at_the_valuation_date_is_the_projection_s_first_event(sec_model):
    """The columns are measured before month 0's events, and the anniversary's increase is
    the projection's, at today's References (D6, as precised at uslib's M7; K14).

    Point 12, the underwritten increasing point valued on its first anniversary, ``d =
    12``, holds the first year's cover and premium, 150,000 and 101.25, which ``WOL_UK_S``
    gives in policy month 11, and its first increase is made at ``t = 0``.  With the take-up
    set to a half at the valuation date the increase is a half of 5% on the cover and of
    10% on the premium, so the point projects a cover of 150,000 x 1.025 = 153,750 and a
    premium of 101.25 x 1.05 = 106.3125, through policy year 2, and steps again at ``t =
    12``; read after month 0's step, as the instant first was, the columns would hold
    157,500 and 111.375, at the take-up of 1 the history does not have.  At the shipped
    take-up of 1 the point is ``WOL_UK_S``'s month 12, as T2 holds.  The take-up is set on
    a model just read (K7).
    """
    model = mx.read_model(model_path(SEC), name=_name("instant"))
    try:
        model.Projection.esc_take_up = 0.5
        row = _row(model, "derived", 6, 12)
        assert (row.duration_mth_init(), row.duration_init()) == (12, 0)
        assert (row.cover_pp_init(), row.premium_pp_init()) == (150000.0, 101.25)
        for t in (0, 11):
            assert row.cover_pp(t) == pytest.approx(153750.0, rel=1e-15), t
            assert row.premium_pp(t) == pytest.approx(106.3125, rel=1e-15), t
        assert row.cover_pp(12) == pytest.approx(153750.0 * 1.025, rel=1e-15)
        assert (round(row.cover_pp(0), 2), round(row.premium_pp(0), 2)) == (153750.0, 106.31)
        assert row.prem_cum_pp(0) == row.prem_cum_pp_init() + row.premium_pp(0) == (
            1215.0 + row.premium_pp(0))
    finally:
        model.close()
    shipped = _row(sec_model, "derived", 6, 12)
    assert shipped.cover_pp(0) == pytest.approx(157500.0, rel=1e-15)
    assert shipped.premium_pp(0) == pytest.approx(111.375, rel=1e-15)


def test_the_paid_up_strand_is_read_from_the_model_point(sec_model, spliced, tmp_path):
    """The paid-up policies and their cover are the point's, not rebuilt (K14).

    ``WOL_UK_S`` builds the paid-up strand from issue, its conversions at today's lapse
    table and stress and its cash sums at today's cover, so a stress or an RPI set at the
    valuation date would convert lapses long past or reprice a paid-up value already fixed.
    So the paid-up point at 200 is projected at the shipped References, with no stress, from
    the strand ``WOL_UK_S`` reaches at policy month 200 under the splice's stress of 0.5,
    more policies converted past the crossover, at the cash sums of their months: its
    paid-up count and its paid-up cover are the columns', which today's References, the
    committed row's, do not give; each paid-up death pays the cover per paid-up policy;
    and the strand runs off from them on mortality alone, taking in the month's
    conversions.
    """
    stressed = _point(spliced[0], 3)
    count = stressed.pols_pu(200)
    cover = stressed.pu_benefit(200) / count
    label = _label(_committed(), "derived", 3, 200)
    shipped = _point(sec_model, label)
    assert count != pytest.approx(shipped.pols_pu_init(), rel=1e-6)
    assert cover != pytest.approx(shipped.pu_benefit_pp_init(), rel=1e-9)
    model = _read_edited(tmp_path, _then(_set("pols_pu_init", [label], count),
                                         _set("pu_benefit_pp_init", [label], cover)))
    try:
        p = _point(model, label)
        pu_kind = _code(p, "DEATH_PU")
        assert p.pols_pu(0) == count and p.pu_benefit(0) == count * cover
        assert p.claims(0, pu_kind) == p.pu_benefit(0) * p.mort_rate_mth(0)
        assert p.pols_death_pu(0) == count * p.mort_rate_mth(0)
        assert p.pols_pu(1) == count * (1.0 - p.mort_rate_mth(0)) + p.pols_convert(0)
        assert p.pols_if(0) == shipped.pols_if(0)
    finally:
        model.close()


# Histories of the crossover no flat rate at today's 3% rebuilds, as (WOL_UK_S's RPI, its
# crossover there, the months S point 4 is restated at): at an RPI of 0 the RPI point is a
# level point and crosses at 166; at 8% its premiums rise faster and it crosses at 201.
CROSSOVER_HISTORIES = ((0.0, 166, (167, 186, 200)), (0.08, 201, (202, 230, 239)))


@pytest.mark.parametrize("rpi, month, restated", CROSSOVER_HISTORIES,
                         ids=[f"rpi {rpi:.0%}" for rpi, _, _ in CROSSOVER_HISTORIES])
def test_the_crossover_is_read_from_the_model_point(tmp_path, rpi, month, restated):
    """A crossover before the valuation date is the point's, not searched for again (K14).

    ``WOL_UK_S`` searches for the crossover from issue at today's ``rpi_rate``, so a model
    that carried the opening state back at today's increases would report the month today's
    RPI puts it in, where the RPI of its day put it elsewhere: the review found the RPI
    point restated after a crossover at 166 under an RPI of 0 reported at 166, 150 and 137,
    and one at 201 under 8% at 220.  So S point 4 is restated by the generator out of
    ``WOL_UK_S`` run under each of :data:`CROSSOVER_HISTORIES`, after its crossover, and
    projected at the shipped RPI of 3%: each row's ``crossover_mth_init`` is S's month, and
    ``crossover_mth()`` reports it.  Restated in the crossover month itself, the crossover
    is the projection's, ``crossover_mth_init`` -1, and the search forward from the opening
    state finds it there, in month 0.
    """
    s = mx.read_model(model_path(TWIN), name=_name("crossover_s"))
    try:
        s.Projection.rpi_rate = rpi
        assert _point(s, 4).crossover_mth() == month
        spec = dataclasses.replace(SPEC, derived=tuple((4, d) for d in (month, *restated)),
                                   future=(), derived_refs={})
        table, _ = build_sec_table(spec, s)
    finally:
        s.close()
    model = mx.read_model(_sec_inputs(tmp_path, table), name=_name("crossover"))
    try:
        assert model.Projection.rpi_rate == 0.03
        for d in restated:
            row = _row(model, "derived", 4, d)
            assert (row.crossover_mth_init(), row.crossover_mth()) == (month, month), d
        at = _row(model, "derived", 4, month)
        assert (at.crossover_mth_init(), at.crossover_mth()) == (-1, month)
    finally:
        model.close()


def test_the_truncation_check_scales_with_the_paid_up_policies(tmp_path):
    """``check_truncation`` closes on the paid-up strand's policies too (§7.1, T4).

    The survivors at the limiting age are rounding on every policy on the books, so the
    check holds them to 1e-9 times ``max(policy_count() + pols_pu_init(), 1)``.  At the
    shipped loading the over-50s cap takes every life before the limiting age and the
    survivors are exactly 0, which any tolerance passes; at a loading of 0.8 the cap no
    longer binds there and the paid-up point paid-up entirely keeps 3.0e-11 of a policy at
    age 120 for each it holds.  So that point is projected with ten million paid-up
    policies and no full cover: its survivors, 3.0e-4 of a policy, exceed 1e-9, which a
    tolerance scaled by ``policy_count()`` alone, 0, would hold them to, and the check
    closes on the paid-up count.  The loading is set on a model just read (K7).
    """
    label = _label(_committed(), "derived", 3, 180)
    model = _read_edited(tmp_path, _set("pols_pu_init", [label], 1e7))
    try:
        model.Projection.mort_loading_o50 = 0.8
        p = _point(model, label)
        survivors = p.pols_maturity(p.proj_len() - 1)
        assert p.policy_count() == 0.0 and p.pols_pu_init() == 1e7
        assert 1e-9 < survivors < 1e-9 * 1e7, survivors
        assert p.check_truncation() is True
    finally:
        model.close()


def test_expense_inflation_runs_on_the_valuation_clock(sec_model, s_model):
    """Maintenance is in valuation-date pounds, for every point alike (D7).

    At the shipped 3%, the factor at ``t`` is ``1.03^(t // 12)`` on every point, whatever
    its duration, stepping on the valuation date's anniversaries.  So the underwritten
    increasing point valued on its first anniversary, in force 12 months, pays S's
    month-``12 + t`` expenses deflated by ``1.03``, the inflation S had already applied
    since issue, and the point issued 13 months on pays S's maintenance a year of inflation
    earlier than S's issue month would: its factor at ``t`` is ``1.03^(t // 12)``, where S's
    at ``t - 13`` is ``1.03^((t - 13) // 12)``.  The acquisition expense is not inflated on
    either.  This is the only test that sees inflation run on the policy clock: the splice
    sets the rate to 0, and on a point issued at ``t = 0`` the clocks agree.
    """
    assert sec_model.Projection.inflation_rate == INFLATION
    p, s = _row(sec_model, "derived", 6, 12), _point(s_model, 6)
    fut = _row(sec_model, "future", 4, -13)
    for t in (0, 11, 12, 30):
        assert p.inflation_factor(t) == fut.inflation_factor(t) == (1 + INFLATION) ** (t // 12)
    for t in range(p.proj_len()):
        assert p.expenses(t) == pytest.approx(s.expenses(12 + t) / (1 + INFLATION),
                                              rel=1e-12), t
    s4 = _point(s_model, 4)
    acq = s4.expense_acq_pp()
    for t in range(13, fut.proj_len()):
        issued = acq if t == 13 else 0.0
        if fut.pols_all(t) == 0.0:
            continue
        maint = (fut.expenses(t) - issued) / fut.pols_all(t)
        want = (s4.expenses(t - 13) - issued) / s4.pols_all(t - 13)
        assert maint == pytest.approx(
            want * (1 + INFLATION) ** (t // 12 - (t - 13) // 12), rel=1e-12), t


def test_mortality_improvement_runs_on_the_valuation_clock(tmp_path):
    """Improvement steps on the valuation date's anniversaries, for every point (D7).

    With improvement at 1% a year, the factor at ``t`` is ``0.99^(t // 12)`` on every point,
    whatever its duration: 1 through the first valuation year, whether the policy is new, in
    force 186 or 12 months, or to be issued 13 months on.  The mortality rate it multiplies
    is the table's at the point's attained age times the loading, capped, the table stated
    at the valuation date.  So the RPI point valued at 186 dies at S's table rate at month
    ``186 + t`` times ``0.99^(t // 12)``, where ``WOL_UK_S`` would improve it from issue,
    ``0.99^((186 + t) // 12)``.  This is the only test that sees improvement run on the
    policy clock: the splice keeps it at 0, where the clocks agree.  The References are set
    on a model just read (K7).
    """
    model = mx.read_model(_sec_inputs(tmp_path, _committed()), name=_name("improve"))
    try:
        model.Projection.mort_improvement = 0.01
        rows = [_row(model, *case) for case in (("twin", 1, 0), ("derived", 4, 186),
                                                 ("derived", 6, 12), ("future", 4, -13))]
        for t in (0, 11, 12, 30, 200):
            assert {p.mort_improve_factor(t) for p in rows} == {0.99 ** (t // 12)}, t
        p = rows[1]
        table = p.data.mort_table()
        for t in (0, 5, 6, 18, 290):
            q = float(table.loc[("population", "F", "NS", p.age(t)), "mort_rate"])
            assert p.mort_rate(t) == min(q * 1.2 * 0.99 ** (t // 12), 1.0), t
            assert p.mort_rate(t) != pytest.approx(
                min(q * 1.2 * 0.99 ** ((186 + t) // 12), 1.0), rel=1e-9), t
        assert rows[3].mort_rate(13) == min(
            float(table.loc[("population", "F", "NS", 70), "mort_rate"]) * 1.2 * 0.99, 1.0)
    finally:
        model.close()


@pytest.mark.parametrize("grid", GRIDS)
def test_improvement_carries_survivors_past_the_truncation_check(grid):
    """Where improvement gives way to the truncation check, recorded (§6.4).

    The shipped tables reach 1 well before the limiting age, so ``check_truncation()``
    holds on every point at no improvement.  Improvement lowers every rate, and the cap
    with it, and carries survivors to the limiting age.  At :data:`IMPROVEMENT`, 0.2%, the
    rate the module switches improvement on at, the check holds on every committed point,
    the largest residual 4.1e-12 of a policy; at 0.4% it first gives way, on the
    underwritten twins and the underwritten row valued at 12, each past the check's 1e-9;
    at 1% the underwritten twins hold 7.1e-6 of a policy at age 120; and at 2% the check
    gives way on every twin but the male smoker's, whose rates are the heaviest.  The
    underwritten twins hold the same count, as the escalation moves no decrement.  The two
    larger rates are read on the twins alone.  The default run reads :data:`IMPROVEMENT`,
    and the full grid where the check gives way.  Each improvement is set on a model just
    read (K7).
    """
    found, worst = {}, {}
    for rate in (IMPROVEMENT,) if grid == "core" else (0.004, 0.01, 0.02):
        model = mx.read_model(model_path(SEC), name=_name("truncation"))
        try:
            model.Projection.mort_improvement = rate
            table = model.Data.model_point_table()
            gives_way, largest = {}, 0.0
            for key, point_id in zip(point_keys(model), table.index):
                if rate > 0.004 and point_id not in S_POINTS:
                    continue
                p = projection(model, key)
                survivors = p.pols_maturity(p.proj_len() - 1)
                largest = max(largest, survivors)
                if not p.check_truncation():
                    gives_way[point_id] = survivors
            found[rate], worst[rate] = gives_way, largest
        finally:
            model.close()
    if grid == "core":
        assert found[IMPROVEMENT] == {} and 1e-12 < worst[IMPROVEMENT] < 1e-11
        return
    assert set(found[0.004]) == {5, 6, 12}
    assert found[0.01][5] == found[0.01][6] == pytest.approx(7.1e-6, rel=0.01)
    assert set(found[0.02]) == set(S_POINTS) - {7}


@pytest.mark.parametrize("grid", GRIDS)
def test_every_twin_is_s_with_improvement_rpi_take_up_and_the_stress_on(grid):
    """On new business, each twin is S's in every cell with every rate dial moved, in both.

    T1 compares the twins at the shipped References, where improvement and the stress are
    0 and the RPI and the take-up at their shipped values, and the splice holds improvement
    at 0 by design (D7), so a cell that dropped improvement, or read the RPI or the take-up
    from another clock, would pass both.  On a point issued at ``t = 0`` the two clocks
    coincide, and improvement, which runs on the valuation clock here and from issue in
    ``WOL_UK_S``, is the same factor in every month.  So with improvement at
    :data:`IMPROVEMENT`, the RPI at 6%, the take-up at 0.8 and the stress at the splice's
    0.5 set in both models, each twin of S's seven points is S's in every cell S evaluates
    in its sweep and in both reports, to 1e-9 relative with no absolute floor but on the
    residual (:func:`_compare`).  The References are set on models just read (K7).

    The twins of S points 1, 3, 4 and 6 run by default, and those of 2, 5 and 7 with the
    full grid.
    """
    refs = {"mort_improvement": IMPROVEMENT, "rpi_rate": 0.06, "esc_take_up": 0.8,
            "lapse_crossover_beta": SPLICED_REFS["lapse_crossover_beta"]}
    sec = mx.read_model(model_path(SEC), name=_name("dials"))
    s = mx.read_model(model_path(TWIN), name=_name("dials_s"))
    try:
        for model in (sec, s):
            for ref, value in refs.items():
                setattr(model.Projection, ref, value)
        found = []
        for point in S_POINTS:
            if (point in (1, 3, 4, 6)) != (grid == "core"):
                continue
            s_proj, twin = _point(s, point), _row(sec, "twin", point, 0)
            _sweep_s(s_proj)
            found += [f"point {point}: {line}" for line in _compare(
                s_proj, twin, 0, TWIN_EXEMPT_DEFAULT | SPEC.exempt)]
        assert not found, found[:20]
        if grid == "full":
            return
        twin = _row(sec, "twin", 4, 0)
        assert twin.mort_improve_factor(12) == 1.0 - IMPROVEMENT
        assert twin.esc_cover_step() == pytest.approx(0.06 * 0.8, rel=1e-15)
        assert _row(sec, "twin", 1, 0).lapse_rate(166) == pytest.approx(
            1.5 * _point(s, 1).lapse_rate_base(166), rel=1e-15)
    finally:
        sec.close()
        s.close()


def test_the_crossover_is_a_policy_month_carried_from_the_opening_state(sec_model,
                                                                        s_model):
    """The crossover is ``WOL_UK_S``'s policy month on every committed point S reaches.

    ``WOL_UK_S`` searches the policy months it projects, which in force start at the
    valuation date, where look-back stops, and passes each as ``t`` (R1a).  Here a crossover
    before the valuation date is the point's ``crossover_mth_init``, and the search runs
    forward from the valuation date over the policy months on the contractual schedule, the
    premiums paid and the cover carried from the opening state.  So on every committed row
    S reaches at the shipped References, the twins, the rows in force and the row issued
    later, it is S's policy month: 166 on the level over-50s points, valued before it, at it
    or after it, 185 on the RPI point valued after it, 642 on the underwritten increasing
    one, 222 on the male smoker valued after cessation, and none on the level underwritten
    point.  On no point is it a month of the frame.  The test of the column itself, on
    histories today's References do not rebuild, follows the paid-up strand's.
    """
    table = sec_model.Data.model_point_table()
    s_table = s_model.Data.model_point_table()
    seen = {}
    for point_id in table.index:
        policy, month = table.at[point_id, "source_policy_id"], int(
            table.at[point_id, "source_mth"])
        if (policy, month) in UNDER_REFS:
            continue
        s_point = int(s_table.index[s_table["policy_id"] == policy][0])
        mine = _point(sec_model, point_id).crossover_mth()
        assert mine == _point(s_model, s_point).crossover_mth(), point_id
        seen[point_id] = mine
    assert seen[_label(table, "derived", 1, 166)] == 166
    assert seen[_label(table, "derived", 3, 200)] == 166
    assert seen[_label(table, "derived", 4, 186)] == 185
    assert seen[_label(table, "derived", 7, 300)] == 222
    assert seen[_label(table, "derived", 6, 12)] == 642
    assert seen[5] == -1


def test_the_moratorium_the_suicide_window_and_commission_run_on_the_policy_clock(
        sec_model, tmp_path):
    """The year-one rules count policy months, wherever they fall in the frame.

    The anchor cell valued 6 months after issue is inside its moratorium for six more
    months: a non-accidental death refunds the premiums paid through ``t = 5`` and pays the
    cash sum from ``t = 6``, its policy month 12, where ``WOL_UK_S`` would read the
    moratorium on ``t``; its accidental benefit doubles there on the double-benefit variant;
    and commission, 25% of each premium of policy year 1, continues through ``t = 5`` and
    stops at ``t = 6``.  The underwritten point valued on its first anniversary is past its
    suicide window, and one valued at 6 months inside it for six months more.  A point
    valued later pays no commission at all.
    """
    anchor = _row(sec_model, "derived", 1, 6)
    non_acc, death = _code(anchor, "NON_ACC"), _code(anchor, "DEATH")
    assert [anchor.in_moratorium(t) for t in (0, 5, 6)] == [True, True, False]
    assert anchor.benefit_pp(5, non_acc) == pytest.approx(360.0, rel=1e-15)
    assert anchor.benefit_pp(6, non_acc) == 5000.0
    assert [anchor.commissions(t) > 0.0 for t in (0, 5, 6, 7)] == [True, True, False, False]
    assert anchor.commissions(0) == pytest.approx(0.25 * anchor.premiums(0), rel=1e-15)
    uw = _row(sec_model, "derived", 6, 12)
    assert uw.benefit_pp(0, death) == uw.cover_pp(0)
    assert all(uw.commissions(t) == 0.0 for t in range(uw.proj_len()))
    assert all(_row(sec_model, "derived", 1, 166).commissions(t) == 0.0
               for t in range(434))
    model = _read_edited(tmp_path, _then(
        _set("duration_mth", [uw.point_id()], 6),
        _set("cover_pp_init", [uw.point_id()], 150000.0),
        _set("premium_pp_init", [uw.point_id()], 101.25),
        _set("prem_cum_pp_init", [uw.point_id()], 607.5),
        _set("variant_adb_2x", [anchor.point_id()], True)))
    try:
        p = _point(model, uw.point_id())
        for t in (0, 5):
            assert p.benefit_pp(t, death) == pytest.approx(
                0.99 * p.cover_pp(t) + 0.01 * p.prem_cum_pp(t), rel=1e-15), t
        assert p.benefit_pp(6, death) == p.cover_pp(6)
        q = _point(model, anchor.point_id())
        acc = _code(q, "ACC")
        assert [q.benefit_pp(t, acc) for t in (5, 6)] == [5000.0, 10000.0]
    finally:
        model.close()


def test_acquisition_is_charged_on_new_business_only(sec_model):
    """The acquisition expense per policy issued, in the issue month alone.

    On every committed point, what ``expenses(t)`` holds beyond its maintenance part is
    the cell's acquisition expense times ``policy_count()`` in the issue month,
    ``t = -duration_mth``, and 0 in every other month, to 1e-9: the twins of S's new business
    bear it at ``t = 0``, the point issued 13 months on at ``t = 13``, and the points
    already in force never, though on the valuation clock their row 0 is ``t = 0``, as S's
    restated rows did not.  ``WOL_UK_S`` charges it at ``t = 0`` on the count in force there,
    which on a point issued at the valuation date is the issued count, so the twins agree
    with S at any count.
    """
    table = sec_model.Data.model_point_table()
    for key, point_id in zip(point_keys(sec_model), table.index):
        p = projection(sec_model, key)
        ts = range(p.proj_len())
        issue = -table.at[point_id, "duration_mth"]
        acq = [p.expenses(t) - p.expense_maint_pp() / 12 * p.inflation_factor(t)
               * p.pols_all(t) for t in ts]
        assert acq == pytest.approx([p.expense_acq_pp() * p.policy_count() if t == issue
                                     else 0.0 for t in ts], abs=1e-9), point_id
        assert (issue in ts) == (sum(acq) > 0.0), point_id


# A stress that lapses every policy past the crossover, as (the S points restated, their
# months): at a stress of 100 the lapse rate's bound at 1 binds, min(1.0, w), its bound
# first as in WOL_UK_S, and every would-be lapse leaves at the crossover, the paid-up
# point's converting.
LAPSE_ALL_CASES = {"core": ((1, (166, 200)), (3, (166, 200))),
                   "full": ((1, (165, 167)), (3, (165, 167)))}


@pytest.mark.parametrize("grid", GRIDS)
def test_a_stress_that_lapses_every_policy_continues_the_s_projection(tmp_path, grid):
    """T2 with the lapse rate's bound binding, which the splice's stress does not reach.

    The splice's stress of 0.5 takes no lapse rate past 1, so the bound side of the lapse
    rate's ``min`` is compared with S nowhere there.  So S's anchor and paid-up points are
    restated by the generator about their crossover under :data:`LAPSE_ALL`, a stress of
    100 set in S and SEC alike with the splice's inflation and improvement of 0, and each
    row is S's from its month on in every cell (:func:`_compare`): the lapse rates, the
    lapses and the conversions among them.  Then what the bound reaches: the lapse rate is 1
    from the crossover, every policy on full cover leaves in it, the paid-up point's
    converting, and the rows after it are paid-up entirely or empty, the states the
    every-state test reads.

    The default run splices the crossover month and month 200, and the full grid the months
    either side of the crossover.
    """
    s = mx.read_model(model_path(TWIN), name=_name("lapse_all_s"))
    sec = None
    try:
        for ref, value in LAPSE_ALL.items():
            setattr(s.Projection, ref, value)
        cases = LAPSE_ALL_CASES[grid]
        spec = dataclasses.replace(SPEC, derived=tuple((p, d) for p, mths in cases
                                                       for d in mths),
                                   future=(), derived_refs={})
        table, _ = build_sec_table(spec, s)
        sec = mx.read_model(_sec_inputs(tmp_path, table), name=_name("lapse_all"))
        for ref, value in LAPSE_ALL.items():
            setattr(sec.Projection, ref, value)
        found = []
        for p, mths in cases:
            s_proj = _point(s, p)
            _sweep_s(s_proj)
            for d in mths:
                found += [f"point {p} at {d}: {line}" for line in _compare(
                    s_proj, _row(sec, "derived", p, d), d, SPLICE_EXEMPT)]
        assert not found, found[:20]
        if grid == "full":
            return
        on = _row(sec, "derived", 3, 166)
        assert on.lapse_rate(0) == 1.0 and on.lapse_rate_mth(0) == 1.0
        assert on.pols_if(1) == 0.0 and on.pols_convert(0) == on.pols_exit(0) > 0.0
        after = _row(sec, "derived", 3, 200)
        assert after.policy_count() == 0.0 and after.pols_pu_init() > 0.0
        gone = _row(sec, "derived", 1, 200)
        assert gone.policy_count() == 0.0 and gone.pols_pu_init() == 0.0
    finally:
        if sec is not None:
            sec.close()
        s.close()


@pytest.mark.parametrize("rpi, steps", [(-0.02, (0.0, 0.0)), (0.25, (0.10, 0.15))],
                         ids=["an RPI below 0", "an RPI past both caps"])
def test_the_rpi_increases_are_floored_at_0_and_capped(rpi, steps):
    """The RPI's floor and caps, which the splice's 3% sits between, as in ``WOL_UK_S``.

    The cover's increase is the RPI floored at 0 and capped at 10%, and the premium's 1.5
    times it, floored at 0 and capped at 15%: ``max`` and then ``min``, each bound written
    second.  With the RPI at -2% neither the twin of the RPI point nor its row in force at
    186 increases at its next anniversary, and at 25% each cover rises 10% and each premium
    15%; the twin's steps, cover and premium are ``WOL_UK_S``'s at the same RPI, read on a
    model of each just read with the RPI set (K7).  T1 compares them at the shipped 3% and
    the twins test at 6%; the NaN test holds the bounds' order.
    """
    model = mx.read_model(model_path(SEC), name=_name("rpi"))
    s = mx.read_model(model_path(TWIN), name=_name("rpi_s"))
    try:
        for each in (model, s):
            each.Projection.rpi_rate = rpi
        twin, row, s_proj = _row(model, "twin", 4, 0), _row(model, "derived", 4, 186), _point(s, 4)
        for proj in (twin, s_proj):
            assert (proj.esc_cover_step(), proj.esc_prem_step()) == steps
            assert proj.cover_pp(12) == pytest.approx(5000.0 * (1 + steps[0]), rel=1e-15)
            assert proj.premium_pp(12) == pytest.approx(30.0 * (1 + steps[1]), rel=1e-15)
        assert _mismatches(s_proj, twin, rtol=0.0, atol=0.0, codes=codes(twin)) == []
        assert row.cover_pp(6) == pytest.approx(row.cover_pp_init() * (1 + steps[0]),
                                                rel=1e-15)
        assert row.premium_pp(6) == pytest.approx(row.premium_pp_init() * (1 + steps[1]),
                                                  rel=1e-15)
    finally:
        s.close()
        model.close()


# ---------------------------------------------------------------------------
# The cap on mortality
#
# mort_rate caps the annual rate at 1, the bound second, as WOL_UK_S's does since M0.  The
# shipped tables reach 1 in the tail, loaded or not, so the cap binds on S's own points: on
# the over-50s anchor cell from attained age 110, policy month 480, where the population
# rate times the loading of 1.2 passes 1; on the male smoker from 101, policy month 432; and
# on the underwritten cell from 114, policy month 888, where the assured rate reaches 1.
# S points 1, 7 and 5, each as (its first capped month, the attained age then).
CAPPED_POINTS = {1: (480, 110), 7: (432, 101), 5: (888, 114)}


@pytest.mark.parametrize("capped", [pytest.param(p, id=f"point{p}",
                                                 marks=() if p == 1 else FULL_ONLY)
                                    for p in CAPPED_POINTS])
def test_an_annual_mortality_past_1_is_capped_in_both_models(s_model, tmp_path, capped):
    """Where the annual mortality rate passes 1, both models' rate is 1.

    On each of :data:`CAPPED_POINTS`, at the shipped tables, ``WOL_UK_S``'s rate reaches 1
    in its first capped month and stays there to the end of the frame, and the uncapped
    product passes 1 there or later: the capped rate and the monthly rate,
    ``1 - (1 - q)^(1/12)``, are 1.0 in every one of those months, the float, not the int 1,
    which compares equal to it, and S's are floats below 1 in every month before.  So every
    policy in force at the start of the first capped month dies in it, on both strands, none
    is in force after it, and every report holds finite floats alone.

    Four rows of each point, built from S by the generator under :data:`SPLICED_REFS`:
    issued at the valuation date and 12 months after it, and restated in force in the month
    before the cap, opened with S's count and state there, each compared with S in every
    cell, the capped months included, as T1, T3 and the splice compare them, to 1e-9
    relative with no absolute floor, but for the residual, rounding around 0, which keeps
    the floor of 1e-9 (USLIB-SEC-PLAN.md §5.1, step 6); and restated five months into the
    capped year, opened with S's state there and one policy, since S's count there is 0.  On
    each, the capped rates are 1.0 from its first capped month, every policy in force there
    dies in it, and the count is 0.0 after it.

    The anchor cell runs by default, and the male smoker and the underwritten point with
    the full grid.
    """
    s = mx.read_model(model_path(TWIN), name=_name("capped_s"))
    sec = None
    try:
        for ref, value in SPLICED_REFS.items():
            setattr(s.Projection, ref, value)
        derived, future = [], []
        points = {capped: CAPPED_POINTS[capped]}
        for s_point, (cap, age) in points.items():
            sp = _point(s, s_point)
            end = sp.proj_len()
            first = next(t for t in range(end) if sp.mort_rate(t) == 1.0)
            assert (first, sp.age(first)) == (cap, age), s_point
            after = range(cap, end)
            for name in ("mort_rate", "mort_rate_mth"):
                assert all(type(sp.cells[name](t)) is float and sp.cells[name](t) < 1.0
                           for t in range(cap)), name
                assert [(type(sp.cells[name](t)), sp.cells[name](t)) for t in after] == [
                    (float, 1.0)] * len(after), name
            _sweep_s(sp)
            assert sp.pols_if(cap) > 0.0 and sp.pols_death(cap) == sp.pols_if(cap)
            assert [sp.pols_all(t) for t in range(cap + 1, end)] == [0.0] * (len(after) - 1)
            derived += [(s_point, cap - 1), (s_point, cap + 5)]
            future.append((s_point, 12))
        rows, _ = build_sec_table(dataclasses.replace(SPEC, derived=tuple(derived),
                                                      future=tuple(future),
                                                      derived_refs={}), s)
        emptied = (rows["row_kind"] == "derived") & (rows["policy_count"] == 0.0)
        assert emptied.sum() == len(points)
        rows.loc[emptied, "policy_count"] = 1.0
        sec = mx.read_model(_sec_inputs(tmp_path / "sec", rows), name=_name("capped"))
        for ref, value in SPLICED_REFS.items():
            setattr(sec.Projection, ref, value)
        for s_point, (cap, _) in points.items():
            sp = _point(s, s_point)
            cases = ((("twin", s_point, 0), cap, TWIN_EXEMPT_DEFAULT | SPEC.exempt),
                     (("future", s_point, -12), cap + 12, FUTURE_EXEMPT),
                     (("derived", s_point, cap - 1), 1, SPLICE_EXEMPT),
                     (("derived", s_point, cap + 5), 0, None))
            for case, first, exempt in cases:
                p = _row(sec, *case)
                if exempt is not None:
                    assert _mismatches(sp, p, t_offset=case[2],
                                           exempt=exempt | RESIDUALS, atol=0.0,
                                           codes=codes(p)) == [], case
                    others = exempt | (set(sp.cells) - RESIDUALS)
                    assert _mismatches(sp, p, t_offset=case[2], exempt=others,
                                           codes=codes(p)) == [], case
                capped, later = range(first, p.proj_len()), range(first + 1, p.proj_len())
                for name in ("mort_rate", "mort_rate_mth"):
                    assert [(type(p.cells[name](t)), p.cells[name](t)) for t in capped] == [
                        (float, 1.0)] * len(capped), (case, name)
                assert p.pols_if(first) > 0.0 and p.pols_death(first) == p.pols_if(first)
                assert [p.pols_all(t) for t in later] == [0.0] * len(later), case
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
# each cell's loading on its own cell's points, and improvement from the second valuation
# year, where its power first reads it; the RPI's floor and cover cap, max(rpi, 0.0) and
# min(..., 0.1), read rpi_rate, and the premium step's, max(1.5 x rpi, 0.0) and
# min(..., 0.15), esc_rpi_prem_mult, on the RPI point.  A bound written first would turn
# each NaN into the bound: a blank input read as certain death, or an increase of 10%.  This
# form runs compiled unchanged, since a compiled ItemSpace takes the References when it is
# made (USLIB-SEC-PLAN.md §5.1, step 6, precised at M12).
NAN_BOUNDS = [
    ("the mortality cap on the over-50s cell, min(q, 1.0)", "mort_loading_o50", 1,
     [("mort_rate", (0,)), ("mort_rate_mth", (0,)), ("pols_death", (0,))]),
    ("the mortality cap on the underwritten cell", "mort_loading_uw", 5,
     [("mort_rate", (0,)), ("mort_rate_mth", (300,)), ("pols_death", (0,))]),
    ("the mortality cap, through improvement", "mort_improvement", 1,
     [("mort_improve_factor", (12,)), ("mort_rate", (12,)), ("mort_rate_mth", (12,))]),
    ("the RPI's floor and cover cap", "rpi_rate", 4,
     [("esc_cover_step", ()), ("esc_prem_step", ())]),
    ("the RPI premium step's floor and cap", "esc_rpi_prem_mult", 4,
     [("esc_prem_step", ())]),
]


@pytest.mark.parametrize("bound, ref, s_point, calls", NAN_BOUNDS,
                         ids=[c[0] for c in NAN_BOUNDS])
def test_a_nan_that_reaches_a_bound_stays_nan(bound, ref, s_point, calls):
    """A NaN that reaches a bound written second stays NaN, and is not read as the bound.

    ``min`` keeps its first argument unless a later one compares smaller, and ``max`` unless
    a later one compares larger, in modelx and compiled alike, and no comparison with NaN
    holds, so with its bound first each would turn a NaN into the bound.  Each is written
    with its bound second, as ``WOL_UK_S`` writes it (:data:`NAN_BOUNDS`): the Reference
    that feeds it is set to NaN on a model read for the test, and every call must give the
    float NaN.  The cells are called on their own, without the frame: ``proj_len()`` refuses
    each of these References at NaN before a report reaches a bound (the domain test).  The
    lapse rate's bound keeps ``WOL_UK_S``'s order, the bound first, and is no cap on a
    mortality rate (USLIB-SEC-PLAN.md §5.1, step 6); ``Data`` and ``proj_len()`` hold what it
    reads to domains no NaN is in.
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


def test_no_check_passes_a_residual_that_is_not_a_number():
    """No check passes a residual that is NaN (§7.1).

    A check is ``abs(resid) <= tolerance`` over the frame, and no comparison with NaN
    holds, so a NaN residual would fail it, as ``WOL_UK_S``'s does (USLIB-SEC-PLAN.md §7.1,
    *Precised at M3*, item 11); and the frame comes first.  With ``mort_loading_o50`` NaN,
    set on a model read for the test before it computes anything, the mortality rates, the
    counts on both strands and so the roll-forward's residual and the truncation residual
    are NaN on the paid-up twin, and each check, asking ``proj_len()`` for the frame, is
    refused the Reference, by name, before it compares one.  So no check passes; and on the
    shipped References each is the bool True.
    """
    for loading, closes in ((float("nan"), False), (1.2, True)):
        model = mx.read_model(model_path(SEC), name=_name("nan_check"))
        try:
            model.Projection.mort_loading_o50 = loading
            p = _row(model, "twin", 3, 0)
            assert math.isnan(p.check_pols_roll_fwd_resid(0)) != closes
            assert math.isnan(p.pols_maturity(599)) != closes
            if closes:
                assert p.check_pols_roll_fwd() is True and p.check_truncation() is True
            else:
                refusal = "point_id 3: mort_loading_o50 must be a finite number, 0 or more, not nan"
                _refused(p.check_pols_roll_fwd, refusal)
                _refused(p.check_truncation, refusal)
        finally:
            model.close()


def _nan_in_the_first_month(t):
    """A residual NaN in the frame's first month, ``t = 0``, and 0 in every other."""
    return float("nan") if t == 0 else 0.0


def _nan_in_the_last_month(t):
    """A residual NaN in the frame's last month, ``t = proj_len() - 1``, and 0 in every
    other: a formula for the model, which reads ``proj_len`` as its own cell."""
    return float("nan") if t == proj_len() - 1 else 0.0              # noqa: F821


@pytest.mark.parametrize("check, resid, month", [
    ("check_pols_roll_fwd", "check_pols_roll_fwd_resid", _nan_in_the_first_month),
    ("check_pols_roll_fwd", "check_pols_roll_fwd_resid", _nan_in_the_last_month),
    ("check_truncation", "pols_maturity", _nan_in_the_last_month)],
    ids=["roll_fwd-first", "roll_fwd-last", "truncation-last"])
def test_a_check_fails_a_residual_that_is_not_a_number(sec_model, check, resid, month):
    """Each check returns False where its residual is NaN in one month (§7.1, item 11).

    A check is ``abs(resid) <= tolerance`` over the frame, or the truncation residual
    ``<= tolerance`` in its last month, which no NaN passes, as ``WOL_UK_S``'s are; but no
    input the frame accepts gives a NaN residual any more, so the residual's formula is
    replaced, on a model read for the test, by one that is NaN in one month and 0 in every
    other: the roll-forward's in the frame's first month, and in its last, and the
    truncation residual, ``pols_maturity``, in the last, which is the month its check
    reads.  Then the check is the bool False on every committed point, where with its own
    formula it is True.  A check that asked whether any residual was past its tolerance
    would pass NaN, and a loop over the frame that stopped a month short, or started a
    month late, would pass the month it skips.
    """
    model = mx.read_model(model_path(SEC), name=_name("nan_resid"))
    try:
        model.Projection.cells[resid].formula = month
        for key in point_keys(model):
            p, shipped = projection(model, key), projection(sec_model, key)
            first = 0 if month is _nan_in_the_first_month else p.proj_len() - 1
            assert math.isnan(p.cells[resid](first)), key
            assert shipped.cells[check]() is True and p.cells[check]() is False, key
    finally:
        model.close()


def _outside_cover_faults(p, where):
    """Where ``p``, an ItemSpace that has evaluated nothing, departs from OUTSIDE_COVER.

    Every cell of :data:`OUTSIDE_COVER`, ``pols_if_at`` at each timing, ``claims`` at each
    kind and ``benefit_pp`` at each benefit, in every month before issue and at
    ``t = proj_len()``, the first month after cover, which the count's look-ahead reads,
    against :data:`OUTSIDE_COVER`; then whether any of :data:`IN_COVER_ONLY` was evaluated
    on the way, which only a fresh ItemSpace can say.  A cell that raises is reported as a
    fault too, so the scan goes on.
    """
    faults = []
    for t in [*range(p.t_entry()), p.proj_len()]:
        calls = [(name, (t,), want) for name, want in OUTSIDE_COVER.items()]
        calls += [("pols_if_at", (t, _code(p, timing)), 0.0) for timing in TIMINGS]
        calls += [("claims", (t, _code(p, kind)), 0.0) for kind in (*KINDS, "ALL")]
        calls += [("benefit_pp", (t, _code(p, kind)), 0.0) for kind in BENEFITS]
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
    table is read at a policy year or an attained age the policy does not have.

    The committed table's one point issued after the valuation date is the RPI point, which
    has no paid-up value and is on the over-50s cell, so on it a cell tied to the paid-up
    strand or to the underwritten cell would hold zero before issue, guarded or not.  So
    the same scan runs on the splice's future rows, the core's or, with
    ``UKLIB_SEC_FULL=1``, all of them: the paid-up point, the underwritten one and the
    variants among them.  Each row is made afresh first and released after.

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

    S point 1's twin, the point restated at month 6 and the point issued a month on, summed
    as ``run_sec.py --block`` sums them, are indexed 0..600 and equal S's frame added to
    itself moved 6 months earlier and a month later.  A model whose frames sat on the
    policy clock would fail it.
    """
    s, sec = spliced
    cases = (("derived", 1, 6), ("future", 1, -1))
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
    expected = pd.concat([sdf, sdf.set_axis(sdf.index - 6).loc[0:],
                          sdf.set_axis(sdf.index + 1)]).groupby(level=0).sum()
    assert list(block.index) == list(range(601))
    assert frame_mismatches(expected, block) == []


# The labels an extract carries in the test below and in the malformed extract's: the
# committed points' in reverse, from 100 plus their number down to 101, so that a label is
# neither a position plus one nor in the order of the rows.
EXTRACT_LABELS = tuple(range(100 + len(_committed()), 100, -1))


def _extract():
    """The committed table as an administration extract would hold it: without the
    generator's columns, and labelled :data:`EXTRACT_LABELS`."""
    extract = _committed().drop(columns=list(generated_columns(SPEC)))
    extract.index = pd.Index(EXTRACT_LABELS, name="point_id")
    return extract


@pytest.mark.parametrize("grid", GRIDS)
def test_an_in_force_extract_needs_none_of_the_generator_columns(sec_model, tmp_path, grid):
    """The model reads the in-force interface and S's columns, never where a row came from,
    and names each point by its label, wherever the row stands.

    ``row_kind``, ``source_policy_id``, ``source_mth`` and ``source_refs`` record how the
    generator made each shipped row, from which S row, at which month and under which
    References, and an administration extract carries none of them.  Read without them,
    and with every label changed, every point projects what the committed table projects,
    in ``result_cf`` and ``result_pols``, to 1e-12, and ``run_sec.py``, run beside that
    extract, prints the point without saying where it came from.  On every shipped row
    ``source_mth`` equals ``duration_mth``, so a formula that read the one for the other
    would pass every test that leaves ``duration_mth`` as generated.  And a refusal names
    the extract's label.

    The default run compares :data:`CORE_POINTS` and runs the runner and the moved row, and
    the full grid compares the other committed points.
    """
    extract = _extract()
    absent = ("row_kind", "source_policy_id", "source_mth", "source_refs")
    assert absent == generated_columns(SPEC), generated_columns(SPEC)
    assert not set(absent) & set(extract.columns), list(extract.columns)
    folder = _sec_inputs(tmp_path / "extract", extract)
    model = mx.read_model(folder, name=_name("extract"))
    try:
        table = model.Data.model_point_table()
        assert not set(generated_columns(SPEC)) & set(table.columns)
        assert list(table.index) == list(EXTRACT_LABELS)
        for key, base_key, label in zip(point_keys(model), point_keys(sec_model),
                                        _committed().index):
            if not _on_grid(grid, label):
                continue
            mine, base = projection(model, key), projection(sec_model, base_key)
            for report in ("result_cf", "result_pols"):
                assert frame_mismatches(base.cells[report](), mine.cells[report](),
                                        rtol=1e-12, atol=1e-12) == [], (key, report)
            _release(model, key)
    finally:
        model.close()
    if grid == "full":
        return
    runner = folder.parent / "run_sec.py"
    shutil.copy(model_path(SEC).parent / "run_sec.py", runner)
    label = extract.index[extract["policy_id"] == "WOL-000003-M200"][0]
    out = _run_sec(runner, str(label))
    row = _row(sec_model, "derived", 3, 200)
    assert out.splitlines()[:2] == [
        f"model point {label}: WOL-000003-M200 - O50 cell, F70 smoker NS, level cover "
        f"5,000, premium 30.00 a month to policy month 240, pro-rata paid-up value",
        f"at the valuation date: in force 200 months: policy year 17, attained age 86, "
        f"{row.pols_if(0):.6f} on full cover, {row.pols_pu(0):.6f} paid-up"]
    last = extract.index[extract["policy_id"] == "WOL-000001-M166"][0]
    moved = _moved_on(last, 601)(extract)
    model = mx.read_model(_sec_inputs(tmp_path / "moved", moved), name=_name("moved"))
    try:
        _refused(_point(model, last).result_cf,
                 f"point_id {last}: duration_mth 601 is at or past the limiting age, policy "
                 f"month 600, omega_age 120")
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
            f"{p.age(0)}, {p.pols_if(0):.6f} on full cover, {p.pols_pu(0):.6f} paid-up")


def test_run_sec_prints_a_point_and_the_block(sec_model):
    """The runner prints one point, saying where it came from, and the block (D8).

    Each mode in an interpreter of its own, as a user runs it, with exit code 0 and ASCII
    output, so that it prints on a Windows console under any code page.  The numbers are
    the model's.  The anchor cell, the runner's default, with its lines at the valuation
    date, each asserted whole, so that a longer number cannot pass for the one asserted,
    and its first twelve rows of cash flows and counts.  Point 6, the underwritten
    increasing point, whose line says it pays for life; point 10, restated in force at S's
    month 200 with its paid-up strand; and point 14, to be issued 13 months on: each with
    the two lines that say where its row came from and where it stands, which only the
    committed table's generator columns can say.  And the block: a line for each committed
    point, in table order, its first twelve rows, which must be the committed points'
    frames summed row by row, as this test sums them, and those frames summed into
    projection years, each year's counts, on full cover and paid-up, the ones in force in
    its first month.  Nothing else runs the runner on the committed table.
    """
    runner = model_path(SEC).parent / "run_sec.py"
    out = _run_sec(runner)
    assert out.splitlines()[:3] == [
        "model point 1: WOL-000001 (S's WOL-000001) - O50 cell, F70 smoker NS, level cover "
        "5,000, premium 30.00 a month to policy month 240",
        "at the valuation date: issued at the valuation date, t = 0",
        "proj_len = 600 months from the valuation date (t = 0..599); the limiting age is "
        "policy month 600"]
    anchor = _row(sec_model, "twin", 1, 0)
    assert anchor.result_cf().head(12).round(2).to_string() in out
    assert anchor.result_pols().head(12).round(6).to_string() in out
    row = _row(sec_model, "derived", 3, 200)
    for point_id, lines in (
            ("6", ["model point 6: WOL-000006 (S's WOL-000006) - UW cell, M40 smoker NS, "
                   "fixed_5pct cover 150,000, premium 101.25 a month for life",
                   "at the valuation date: issued at the valuation date, t = 0"]),
            ("10", ["model point 10: WOL-000003-M200 (S's WOL-000003 at its month 200) - "
                    "O50 cell, F70 smoker NS, level cover 5,000, premium 30.00 a month to "
                    "policy month 240, pro-rata paid-up value",
                    f"at the valuation date: in force 200 months: policy year 17, attained "
                    f"age 86, {row.pols_if(0):.6f} on full cover, {row.pols_pu(0):.6f} "
                    f"paid-up"]),
            ("14", ["model point 14: WOL-000004-F13 (S's WOL-000004, issued 13 months on) - "
                    "O50 cell, F70 smoker NS, rpi cover 5,000, premium 30.00 a month to "
                    "policy month 240",
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
    annual = block.drop(columns=["pols_if", "pols_pu"]).groupby(years).sum()
    annual.insert(0, "pols_pu", [block.at[12 * (y - 1), "pols_pu"] for y in annual.index])
    annual.insert(0, "pols_if", [block.at[12 * (y - 1), "pols_if"] for y in annual.index])
    assert annual.head(12).round(2).to_string() in out


# run_sec.py run as though it sat at /m/products/whole_of_life, in a products/ folder whose
# parent carries no build tool: the source compiled under that name, so that its own
# __file__ is it.
SHALLOW_RUN = """\
import sys
source = open(sys.argv[1], encoding="utf-8").read()
where = "/m/products/whole_of_life/run_sec.py"
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


def test_the_runner_names_the_references_a_row_was_read_under(sec_model):
    """``run_sec.py`` says where each row came from, and under which References.

    The line it prints for a point names the row's source from the committed table's
    generator columns (``origin``).  A row read from S under References of its own, the
    spec's ``derived_refs``, is no restatement at the shipped ones, so its line names them
    as ``source_refs`` records them, point 15's ``under rpi_rate 0.05``, and no other row's
    line names any.  ``origin`` is read from the runner, which runs the model when imported,
    and run here on every row of the table the runner reads.
    """
    tree = ast.parse((model_path(SEC).parent / "run_sec.py").read_text(encoding="utf-8"))
    found = [node for node in tree.body
             if isinstance(node, ast.FunctionDef) and node.name == "origin"]
    assert len(found) == 1
    table = sec_model.Data.model_point_table()
    space = {"table": table}
    exec(compile(ast.Module(found, []), "run_sec.py", "exec"), space)
    refs = table["source_refs"].fillna("")
    assert sum(map(bool, refs)) == len(SPEC.derived_refs) > 0
    for label, under in refs.items():
        line = space["origin"](label)
        assert (line.endswith(f", under {under})") if under
                else ", under " not in line), (label, line)
    assert space["origin"](15) == (
        " (S's WOL-000004 at its month 120, under rpi_rate 0.05)")


def _defaulted(model_name):
    """The cells of ``model_name``'s Projection with a parameter that has a default, sorted,
    read from its source, as the C step's build reads it."""
    source = (model_path(model_name) / "Projection" / "__init__.py").read_text(
        encoding="utf-8")
    return sorted(node.name for node in ast.parse(source).body
                  if isinstance(node, ast.FunctionDef)
                  and (node.args.defaults or any(node.args.kw_defaults)))


def test_no_cell_takes_a_default():
    """No cell has a defaulted parameter, ``WOL_UK_S``'s ``claims`` total settled (R12).

    ``WOL_UK_S`` defaults one parameter, ``claims(t, kind=None)``, its total, and running in
    force added none: a compiled model declares a defaulted parameter in its ``.pxd`` as
    ``long long life=*``, which the typing guard would read as a parameter of that name, and
    ``None`` is no C integer.  The C step settles R12's total as a code of its own,
    ``claims(t, ALL)``, so no cell here takes a default.
    """
    assert _defaulted(TWIN) == ["claims"]
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
    outside the parentheses of the column, ``age`` of ``age(t)``.
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


# What only WOL_UK_S's docstrings may say: a reference into its Spaces, which the SEC pages
# would link to the wrong model; its clock, t counting policy months from issue, t = 0 the
# issue month, the policy year t // 12 + 1, and its anniversaries at t = 12, 24; and its
# frame of 12 x (omega_age - entry_age) months from t = 0.
STALE = re.compile(r"~\.WOL_UK_S\.|``t = 0`` is the issue month"
                   r"|``t`` counts \*\*policy months|t // 12 \+ 1|``t = 12, 24"
                   r"|``proj_len\(\) = 12 x|indexed by policy month ``t``")


def test_the_docstrings_describe_the_valuation_clock(sec_model, s_model):
    """The docstrings say what this model is, and none says what only WOL_UK_S is.

    Whitespace is collapsed first, as ``test_model_conventions_uk`` collapses it, so that a
    phrase split across a line break still matches.  The model docstring names the
    valuation date, BasicTerm_SE, the policy clock, the SEC table and the product.  The
    symbol map in the Projection docstring maps every cell running in force adds, which are
    exactly the cells ``WOL_UK_S`` lacks, and names nothing the model lacks: every name in
    it is a cell or a Reference.  No row of a simple table in any docstring puts text between
    two of its columns (:func:`_table_overruns`), which would drop the table from the
    rendered page.  And no docstring says what :data:`STALE` matches.
    """
    flat = {where: re.sub(r"\s+", " ", doc) for where, doc in _docs(sec_model)}
    for phrase in ("valuation date", "BasicTerm_SE", "duration_mth", TABLE,
                   "whole of life"):
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
    assert not stale, f"docstrings that describe WOL_UK_S: {stale}"


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
    ``model_point_file`` changed, to ``model_point_table_sec.csv``: an edit to a table
    reaches both models, and the two can never drift apart.
    """
    assert sec_model.Data.input_dir() == s_model.Data.input_dir()
    files = {r: v for r, v in s_model.Data.refs.items() if r.endswith("_file")}
    assert {r: v for r, v in sec_model.Data.refs.items() if r.endswith("_file")} == {
        **files, "model_point_file": TABLE}


# The policy month of each S point's and variant's crossover and first capped month, read
# off S at the shipped References: the static properties of the grid read them.
CROSSOVER = {1: 166, 2: 166, 3: 166, 4: 185, 5: -1, 6: 642, 7: 222, 8: 185, 9: 166,
             10: -1, 11: 642, 12: 166, 13: 239}
CAP = {1: 480, 2: 480, 3: 480, 4: 480, 5: 888, 6: 888, 7: 432, 8: 480, 9: 480, 10: 360,
       11: 852, 12: 480, 13: 480}


def test_the_core_grid_reaches_every_branch(spliced, splice_records):
    """What the default run's T2 and T3 cases reach, which the full grid only multiplies.

    The default run thins the splice to a core (the module docstring), and this test is
    what keeps the thinning from costing a branch.  First, statically, over S's table with
    the variants, each property below holds of some core case: both cells, every
    escalation, both sexes and smoker statuses on each cell, the paid-up value, the double
    accidental benefit, the paid-up value with RPI increases and with the double benefit,
    an entry age of its own; and each kind of valuation month: the first policy year, on an
    anniversary, in the month before one, mid-year, inside the moratorium and at its last
    month, at the crossover and past it, at cessation and past it, the first conversion, the
    cap and the last month before the limiting age, and a crossover in the last premium
    month, the crossover search's last, valued at or before it.  And of some core future
    case: issued off the valuation anniversaries and on them, more than a year on, at the
    horizon, on each cell, with the paid-up value and with RPI increases, and a crossover in
    the last premium month, which the search from issue reaches in its last month.

    Then, on the splice's model, of some core row, each of :data:`AT_VALUATION` and
    :data:`IN_FRAME`, what no column of the table shows: every opening-state column in use,
    and each kind of valuation month the windows make; and every branch and both sides of
    every ``min`` and ``max`` the full grid reaches: the moratorium, the suicide window, an
    increase, cessation, commission, conversions, terminating lapses, paid-up deaths, the
    stress and the premiums paid either side of the cover, the lapse table inside and past
    its last year, the cap binding and not, the double benefit, the payments capped and the
    limiting age's last month.

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

    def o50(p):
        return at(p, "cell") == "O50"

    def cessation(p):
        return int(at(p, "cessation_months"))

    splices = {
        **{f"the {c} cell": (lambda k, p, d, c=c: at(p, "cell") == c) for c in ("O50", "UW")},
        **{f"{e} escalation": (lambda k, p, d, e=e: at(p, "escalation") == e)
           for e in ("level", "fixed_5pct", "rpi")},
        **{f"sex {x}, smoker {y} on the {c} cell": (
            lambda k, p, d, x=x, y=y, c=c: (at(p, "sex"), at(p, "smoker"), at(p, "cell"))
            == (x, y, c)) for x, y, c in (("F", "NS", "O50"), ("M", "S", "O50"),
                                          ("M", "NS", "UW"), ("F", "S", "UW"))},
        "the paid-up value": lambda k, p, d: flag(p, "variant_paid_up"),
        "the double accidental benefit": lambda k, p, d: flag(p, "variant_adb_2x"),
        "the paid-up value with RPI increases": lambda k, p, d: (
            flag(p, "variant_paid_up") and at(p, "escalation") == "rpi"),
        "the paid-up value with the double benefit": lambda k, p, d: (
            flag(p, "variant_paid_up") and flag(p, "variant_adb_2x")),
        "an entry age of 80": lambda k, p, d: int(at(p, "entry_age")) == 80,
        "an odd cessation": lambda k, p, d: cessation(p) % 2 == 1,
        "an escalating point past cessation": lambda k, p, d: (
            at(p, "escalation") != "level" and 0 < cessation(p) < d),
        "in the first policy year": lambda k, p, d: d < 12,
        "on an anniversary": lambda k, p, d: d % 12 == 0,
        "in the month before an anniversary": lambda k, p, d: d % 12 == 11,
        "mid-year": lambda k, p, d: d % 12 not in (0, 11),
        "inside the moratorium": lambda k, p, d: o50(p) and d < 12,
        "in the moratorium's last month": lambda k, p, d: o50(p) and d == 11,
        "at the crossover": lambda k, p, d: d == CROSSOVER[p],
        "past the crossover": lambda k, p, d: 0 <= CROSSOVER[p] < d,
        "at cessation": lambda k, p, d: d == cessation(p) > 0,
        "past cessation": lambda k, p, d: 0 < cessation(p) < d,
        "the first conversion": lambda k, p, d: (
            flag(p, "variant_paid_up") and d == cessation(p) // 2 - 1),
        "at the cap": lambda k, p, d: d == CAP[p],
        "in the last month before the limiting age": lambda k, p, d: d == COVER[p] - 1,
        "a crossover in its last premium month": lambda k, p, d: (
            0 <= CROSSOVER[p] == cessation(p) - 1 and d <= CROSSOVER[p]),
    }
    futures = {
        "issued off the anniversaries": lambda p, k: k % 12 != 0,
        "issued on them": lambda p, k: k % 12 == 0,
        "issued more than a year on": lambda p, k: k > 12,
        "issued at the horizon": lambda p, k: k == 120,
        "the over-50s cell": lambda p, k: at(p, "cell") == "O50",
        "the underwritten cell": lambda p, k: at(p, "cell") == "UW",
        "the paid-up value": lambda p, k: flag(p, "variant_paid_up"),
        "RPI increases": lambda p, k: at(p, "escalation") == "rpi",
        "fixed increases": lambda p, k: at(p, "escalation") == "fixed_5pct",
        "a crossover in its last premium month": lambda p, k: (
            0 <= CROSSOVER[p] == cessation(p) - 1),
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
# The C step's representation (UKLIB-SEC-PLAN.md §6.4, *C*)
#
# Data decodes each model point's text into the number the projection reads, and turns
# each table into an array indexed by integers (USLIB-SEC-PLAN.md R5-R8); a timing and a
# kind are int codes, and the claims total is a code of its own (R9, R12); and the four
# chains are blocked by policy year (K12), which the depth test and the openings' test
# above hold.  These tests hold the representation in modelx, with no compiler, in
# seconds: the compiled section after the fingerprint holds the compiled model to modelx
# on it.


def test_the_all_total_is_s_total_bit_for_bit(sec_model, s_model):
    """``claims(t, ALL)`` is ``WOL_UK_S``'s ``claims(t)``, its ``sum``, to the last bit.

    S totals its three kinds with Python's ``sum``, which compensates, and the total here
    is written left to right from ``0.0`` (``Projection.claims``), which is ``sum``'s
    float wherever at most two kinds are non-zero in a month (USLIB-SEC-PLAN.md R12; §6.2,
    *Record -- M4*: three or more take the compensated sum written out).  So the kinds
    non-zero together are counted, in every month of every committed point's frame and the
    month after it: never three, the lapse kind being 0 in every month by the product's
    design, and two, the full-cover and the paid-up deaths, in some months, on the
    committed paid-up rows, which is asserted, so that the count is no vacuous one.  The
    total is compared by ``float.hex`` with ``sum`` of the row's own three kinds there; and
    on every twin of S's new business, whose kinds are S's to the last bit, with S's
    ``claims(t)`` itself.  T1 compares the totals to 1e-9; this compares their bits.  A row
    restated in force opens on a state read back from the CSV, which may part from S's by
    an ulp, so its total is held to its own kinds' ``sum``.
    """
    total = _code(sec_model.Projection, "ALL")
    kinds = [_code(sec_model.Projection, kind) for kind in KINDS]
    found, counts = [], {0: 0, 1: 0, 2: 0, 3: 0}
    table = sec_model.Data.model_point_table()
    for key, point_id in zip(point_keys(sec_model), table.index):
        p = projection(sec_model, key)
        for t in range(p.proj_len() + 1):
            values = [p.claims(t, kind) for kind in kinds]
            counts[sum(v != 0.0 for v in values)] += 1
            if values[2] != 0.0:
                found.append(f"point {point_id}, t = {t}: the lapse kind is {values[2]!r}")
            if p.claims(t, total).hex() != sum(values).hex():
                found.append(f"point {point_id}, t = {t}: {p.claims(t, total)!r}, the "
                             f"kinds' sum {sum(values)!r}")
    for point_id in table.index[table["row_kind"] == "twin"]:
        s, p = _point(s_model, point_id), _point(sec_model, point_id)
        for t in range(p.proj_len()):
            if p.claims(t, total).hex() != s.claims(t).hex():
                found.append(f"point {point_id}, t = {t}: {p.claims(t, total)!r}, S "
                             f"{s.claims(t)!r}")
    assert counts[3] == 0 and counts[2] > 0 and counts[1] > 0, counts
    assert not found, found[:10]


# The two chains whose refusal of a value past the floats is a cell of its own, which
# computes the value again from the same cells and raises only where the chain would, as
# (the chain, its refusal cell).
REFUSAL_CELLS = (("prem_cum_pp", "prem_cum_pp_refusal"), ("pu_benefit", "pu_benefit_refusal"))


def test_each_refusal_cell_computes_its_chain_s_value_bit_for_bit(sec_model):
    """``prem_cum_pp_refusal`` and ``pu_benefit_refusal`` are their chains, bit for bit.

    No cell a chain recurses through builds text (the chain-text test), so ``prem_cum_pp``
    and ``pu_benefit`` call a refusal cell of their own on their error paths alone, and
    each refusal cell repeats its chain's formula, branch by branch, to name the value it
    refuses (:data:`REFUSAL_CELLS`).  Nothing else holds the two formulas together: C4
    compares two engines that share any drift, and a refusal cell is reached only past the
    floats.  So on every committed point, in every month of its frame and the month after
    it, each refusal cell must return its chain's value, by ``float.hex``: the opening
    month, every month within a policy year and every year's first month after
    ``t_entry()``, whose value is the year's opening, on the paid-up points for the
    paid-up cover.  A refusal that dropped the month's premium, or read the month before
    where the chain reads the year's opening, parts here, though the value it would refuse
    only ever passes the floats in a test of its own.
    """
    found, months = [], {"entry": 0, "anniversary": 0, "within": 0}
    for key, point_id in zip(point_keys(sec_model), sec_model.Data.model_point_table().index):
        p = projection(sec_model, key)
        for t in range(p.proj_len() + 1):
            if p.is_active(t):
                months["entry" if t == p.t_entry() else "anniversary"
                       if p.duration_mth(t) % 12 == 0 else "within"] += 1
            for chain, refusal in REFUSAL_CELLS:
                want, got = p.cells[chain](t), p.cells[refusal](t)
                if got.hex() != want.hex():
                    found.append(f"point {point_id}: {refusal}({t}) is {got!r}, "
                                 f"{chain}({t}) {want!r}")
    assert min(months.values()) > 10, months
    assert not found, found[:10]


# One S point per value a decoded column can hold, as (the S point it changes, the columns
# it changes): each cell; each escalation, on each cell; each of the eight mortality
# schedules, the basis the cell's, by sex and smoker status; each variant's flag each way;
# and the numbers WOL_UK_S reads with int, the entry age, written with a fraction, which
# int truncates, above .5 so that a decode that rounded would part, and an odd cessation.
DECODED = [
    (1, {}), (5, {}),
    (1, {"escalation": "fixed_5pct"}), (1, {"escalation": "rpi"}),
    (5, {"escalation": "level"}), (5, {"escalation": "rpi"}),
    *((1, {"sex": sex, "smoker": smoker}) for sex in ("M", "F") for smoker in ("NS", "S")),
    *((5, {"sex": sex, "smoker": smoker}) for sex in ("M", "F") for smoker in ("NS", "S")),
    (1, {"variant_adb_2x": True}), (2, {"variant_adb_2x": False}),
    (1, {"variant_paid_up": True}), (3, {"variant_paid_up": False}),
    (1, {"entry_age": 70.7}), (5, {"entry_age": 40.6}),
    (1, {"cessation_months": 239, "moratorium_months": 11}),
]

# The cells each decoded point is compared on, WOL_UK_S's own, which read the text or the
# number themselves, the labels among them; and the decodes here, each against S's
# comparison of the text.
DECODING_CELLS = ("cell", "sex", "smoker", "escalation", "mort_basis", "age_at_entry",
                  "sum_assured", "premium_mth", "cessation_mths", "moratorium_mths",
                  "adb_multiplier", "pu_variant", "esc_cover_step", "esc_prem_step",
                  "mort_loading", "expense_acq_pp", "expense_maint_pp")
DECODES = {"cell_code": lambda s: ("O50", "UW").index(s.cell()),
           "escalation_code": lambda s: ("level", "fixed_5pct", "rpi").index(s.escalation()),
           "mort_schedule": lambda s: (4 * ("population", "assured").index(s.mort_basis())
                                       + 2 * ("M", "F").index(s.sex())
                                       + ("NS", "S").index(s.smoker()))}


def _decoded_twins(tmp_path):
    """``(S, its table)``: :data:`DECODED`'s points in a copy of S's table, read; and the
    twins of them the generator makes, the SEC table."""
    s_table = _s_table()
    rows = []
    for i, (base, changes) in enumerate(DECODED, start=1):
        row = s_table.loc[[base]].assign(**changes, policy_id=f"WOL-8{i:05d}")
        row.index = pd.Index([i], name="point_id")
        rows.append(row)
    table = pd.concat(rows)
    s = mx.read_model(temp_inputs(tmp_path / "s", model_path(TWIN), model_points=table),
                      name=_name("decoded_s"))
    spec = dataclasses.replace(SPEC, derived=(), future=(), derived_refs={})
    twins, _ = build_sec_table(spec, s)
    return s, twins


def test_every_decode_is_wol_uk_s_own_on_every_value(tmp_path):
    """``Data`` decodes every value a column can hold as ``WOL_UK_S``'s cells read it.

    A point of each case of :data:`DECODED` goes into a copy of S's table, and its twin,
    generated from it, into a copy of SEC's.  On each pair every cell of
    :data:`DECODING_CELLS` agrees exactly, in value and in type, the labels among them, and
    so do the mortality and lapse rates at ``t = 0``, ``12``, ``60`` and ``120``; each
    decode of :data:`DECODES` is S's comparison of the text, as an int; the point's row of
    the mortality table, ``mort_schedule()``, holds S's rate for its basis, sex and smoker
    status at every age of the table, so that ``mort_rate`` is S's at every month the frame
    reads, and its cell's row of the lapse table, ``cell_code()``, S's rate at every policy
    year of the cell's rows, its last year its own.  T1 and the splice see these through
    the cells that use them, at the values their points carry; this sees every value, on
    its own.  A mortality array off by one age, or a schedule numbered otherwise than
    ``Data.mort_schedule`` numbers it, parts here.
    """
    s, twins = _decoded_twins(tmp_path)
    sec = None
    found = []
    try:
        sec = mx.read_model(_sec_inputs(tmp_path / "sec", twins), name=_name("decoded"))
        rates = s.Data.mort_table()["mort_rate"]
        lapses = s.Data.lapse_table()["lapse_rate"]
        mort, lapse = sec.Data.mort_table_array(), sec.Data.lapse_table_array()
        labels = s.Data.model_point_table().index
        for (base, changes), key, label in zip(DECODED, point_keys(sec), labels,
                                               strict=True):
            case = f"S point {base} with {changes}"
            sp, p = _point(s, label), projection(sec, key)
            calls = [(cell, ()) for cell in DECODING_CELLS]
            calls += [(cell, (t,)) for cell in ("mort_rate", "lapse_rate_base")
                      for t in (0, 12, 60, 120)]
            for cell, args in calls:
                want, got = sp.cells[cell](*args), p.cells[cell](*args)
                if got != want or type(got) is not type(want):
                    found.append(f"{case}: {cell}{args} is {got!r}, S {want!r}")
            for cell, read in DECODES.items():
                want, got = read(sp), p.cells[cell]()
                if got != want or type(got) is not type(want):
                    found.append(f"{case}: {cell}() is {got!r}, S's text gives {want!r}")
            row = p.mort_schedule()
            for a in range(sec.Data.mort_age_first(), sec.Data.mort_age_last() + 1):
                want = rates.loc[(sp.mort_basis(), sp.sex(), sp.smoker(), a)]
                if mort[row, a] != want:
                    found.append(f"{case}: row {row} at age {a} is {mort[row, a]!r}, S's "
                                 f"rate {want!r}")
            cell, last = p.cell_code(), p.lapse_last_year()
            assert last == int(lapses.loc[sp.cell()].index.max()), case
            for y in range(1, last + 1):
                if lapse[cell, y] != lapses.loc[(sp.cell(), y)]:
                    found.append(f"{case}: lapse row {cell} at year {y} is "
                                 f"{lapse[cell, y]!r}, S's {lapses.loc[(sp.cell(), y)]!r}")
    finally:
        if sec is not None:
            sec.close()
        s.close()
    assert not found, found[:20]


def _uw_to_year_9(table):
    """*lapse_table.csv* with the UW cell's rows run on to policy year 9, at 1.1%, 1.2%
    and 1.3%, three years past O50's last."""
    last = table[(table["cell"] == "UW") & (table["policy_year"] == 6)]
    more = [last.assign(policy_year=year, lapse_rate=rate)
            for year, rate in ((7, 0.011), (8, 0.012), (9, 0.013))]
    return pd.concat([table, *more], ignore_index=True)


def test_every_padded_array_holds_nan_and_no_reader_reads_it(sec_model, tmp_path):
    """The padding is NaN, and each table's one reader reads inside its keys alone.

    ``Data`` tables the mortality rates from age 0, eight schedules, and the lapse rates
    from policy year 0, one row a cell, and pads what no file holds with NaN, as its
    docstring says, so that a read past a check, were one lost, would make every number
    after it NaN rather than another key's value: each schedule's ages below the table's
    first, 18 as shipped, and year 0 of each cell; inside, nothing is NaN.  On a copy whose
    UW rows stop at policy year 3, the UW row holds NaN from year 4, past its own last
    year, which ``Data.lapse_last_year`` says is 3, and the underwritten point's lapse rate
    reads year 3 at every later year, as ``WOL_UK_S``'s ``tbl.index.max()`` on the cell's
    own rows does; and on a copy whose UW rows run on to policy year 9, past O50's 6, the
    array is ten years wide, as wide as the longest cell, O50's row NaN past its own last
    year, and each point reads its own cell's last year at every later year.  And on the
    extract labelled otherwise than by position
    (:func:`_extract`), where a label read as ``idx + 1`` would name another point, the
    mortality rate refuses an attained age below the table, naming the point and the age,
    on a copy of the table that starts at 20, before it reads the array.
    """
    data = sec_model.Data
    mort = data.mort_table_array()
    first, last = data.mort_age_first(), data.mort_age_last()
    assert mort.shape == (8, last + 1) and (first, last) == (18, 120)
    assert np.isnan(mort[:, :first]).all() and not np.isnan(mort[:, first:]).any()
    lapse, lasts = data.lapse_table_array(), data.lapse_last_year()
    assert lapse.shape == (2, 7) and list(lasts) == [6, 6] and lasts.dtype == np.int64
    assert np.isnan(lapse[:, 0]).all() and not np.isnan(lapse[:, 1:]).any()
    model = _read_edited(tmp_path / "short", lambda t: t,
                         edits={LAPSE: _dropped(lambda t: (t["cell"] == "UW")
                                                & (t["policy_year"] > 3))})
    try:
        array = model.Data.lapse_table_array()
        assert list(model.Data.lapse_last_year()) == [6, 3]
        assert np.isnan(array[1, 4:]).all() and not np.isnan(array[1, 1:4]).any()
        uw = _row(model, "twin", 5, 0)
        assert [uw.lapse_rate_base(t) for t in (24, 36, 120)] == [array[1, 3]] * 3
    finally:
        model.close()
    # And the other way about: the UW rows running to year 9, three years past O50's last,
    # so that the array is as wide as the longest cell, not the first, and O50's row holds
    # NaN past its own last year, which its point reads every later year at.
    model = _read_edited(tmp_path / "long", lambda t: t, edits={LAPSE: _uw_to_year_9})
    try:
        array = model.Data.lapse_table_array()
        assert list(model.Data.lapse_last_year()) == [6, 9] and array.shape == (2, 10)
        assert np.isnan(array[0, 7:]).all() and not np.isnan(array[1, 1:]).any()
        assert list(array[1, 7:]) == [0.011, 0.012, 0.013]
        uw, o50 = _row(model, "twin", 5, 0), _row(model, "twin", 1, 0)
        assert [uw.lapse_rate_base(t) for t in (72, 96, 108, 240)] == [
            0.011, 0.013, 0.013, 0.013]
        assert [o50.lapse_rate_base(t) for t in (60, 96, 108)] == [array[0, 6]] * 3
    finally:
        model.close()
    extract = _extract()
    anchor = extract.index[extract["policy_id"] == "WOL-000001"][0]
    cut = {MORT: _dropped(lambda t: t["age"] < 20)}
    model = mx.read_model(_sec_inputs(tmp_path / "cut", _set("entry_age", [anchor], 18)(
        extract), cut), name=_name("padded"))
    try:
        p = _point(model, anchor)
        position = list(extract.index).index(anchor)
        assert p.point_id() == anchor != point_keys(model)[position] + 1
        _refused(lambda: p.mort_rate(0),
                 f"point_id {anchor}: mort_table.csv has no rate at attained age 18")
        assert p.mort_rate(24) == 1.2 * model.Data.mort_table_array()[p.mort_schedule(), 20]
    finally:
        model.close()


# Data's readers, each a DataFrame or a path, which only the label accessors, the reports
# and Data's own cells read.  Every other Data cell is a vector or an int in the Data
# docstring's table of its vectors.
READERS = ("input_dir", "model_point_table", "mort_table", "mort_table_rows", "lapse_table",
           "lapse_table_rows")


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
    vector is of R5's kind, int64 for ages, months, codes, flags, schedules and years,
    float64 for counts, amounts and rates, as the table states it: a month held as a
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
    assert not any(cells.parameters for cells in data.cells.values())


def test_every_parameterless_cell_returns_a_python_number(sec_model):
    """Every parameterless cell but the reporting ones returns a Python int, float or bool.

    R11: a ``Projection`` cell that reads a ``Data`` vector converts the element, ``int()``,
    ``float()`` or ``bool()``, so that modelx returns a Python number, as the compiled cell
    does, and not a numpy scalar, whose arithmetic and printing differ, and which C4
    compares as a kind of its own.  A conversion left out moves no number and still
    compiles, so it is asserted here: on every committed point, each parameterless cell
    outside :func:`uk_sec_support.reporting_cells` returns exactly an ``int``, a ``float``
    or a ``bool``.
    """
    space = sec_model.Projection
    reporting = reporting_cells(SEC, space)
    names = sorted(name for name, cell in space.cells.items()
                   if not cell.parameters and name not in reporting)
    assert {"point_id", "cell_code", "escalation_code", "mort_schedule", "lapse_last_year",
            "age_at_entry", "cessation_mths", "duration_mth_init", "adb_multiplier",
            "pu_variant", "crossover_mth", "proj_len"} <= set(names)
    found = []
    for key in point_keys(sec_model):
        proj = projection(sec_model, key)
        found += [f"{key}: {name} {type(value).__name__}" for name in names
                  if type(value := proj.cells[name]()) not in (int, float, bool)]
    assert not found, found


# Each label and the refusal its own formula makes of a value that is not its column's
# codes, which Data refuses first as it reads the table: as (the column, the refusal).
# mort_basis reads the cell's column through the registry's map, and refuses what cell
# refuses.
LABEL_REFUSALS = {"cell": ("cell", "invalid cell"),
                  "escalation": ("escalation", "invalid escalation"),
                  "mort_basis": ("cell", "invalid cell"),
                  "sex": ("sex", "invalid sex"), "smoker": ("smoker", "invalid smoker")}


def test_each_label_refuses_a_value_that_is_not_its_codes():
    """The five labels return text or raise, in either engine.

    Each is a reporting cell, which a reader asks for and no projection cell reads, and the
    registry names them (``"reporting"``).  ``Data`` refuses a value other than the
    column's codes as it reads the table, so a label sees only text; but each refuses any
    other value itself, as ``WOL_UK_S``'s ``cell`` and ``escalation`` do and the C step
    makes ``sex`` and ``smoker`` do, and ``mort_basis`` reads ``cell``, so that compiled
    each may return ``str`` and still raises where modelx raises
    (``uk_sec_support.labels_refusing_non_text``, C3).  So each is called in modelx on the
    committed model whose table is replaced, past ``Data``'s checks, by one holding the
    first point's column blank, as the number 7 and as a text no code is, and must refuse
    each, with its message; and the harness's own reading, ``labels_refusing_non_text``,
    which C3 asks, finds all five refusing.
    """
    for label, (column, message) in LABEL_REFUSALS.items():
        for value in (None, 7, "X"):
            model = mx.read_model(model_path(SEC), name=_name("label"))
            try:
                table = model.Data.model_point_table().astype({column: object})
                table.iloc[0, table.columns.get_loc(column)] = value
                model.Data.model_point_table[()] = table
                p = projection(model, point_keys(model)[0])
                _refused(p.cells[label], message)
            finally:
                model.close()
    assert labels_refusing_non_text(SEC, set(LABEL_REFUSALS)) == set(LABEL_REFUSALS)


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


# The code families, each in its numbering: benefit_pp's kinds, DEATH first, the one code
# it shares with claims'; claims' kinds and their total; the cells and the escalations,
# which index no cache.
BENEFIT_CODES = ("DEATH", "NON_ACC", "ACC", "PAID_UP")
CLAIM_CODES = (*KINDS, "ALL")
CELL_CODES = ("O50", "UW")
ESCALATION_CODES = ("LEVEL", "FIXED_5PCT", "RPI")


def test_the_spec_sizes_each_cache_as_its_comment_derives():
    """``spec_sec.py`` gives each cache the size its comment derives from the contract.

    The spec check, C3, holds the compiled caches to the spec, and C4 at the contract's
    extremes holds the spec to the largest argument a projection reads; neither sees a
    size above the comment's.  So this reads the spec as mx2cy does, and the bounds of the
    contract from the model's own References, and holds each size to the comment's
    derivation from them: ``t`` to ``12 * (omega_age_max - issue_age_min) +
    future_horizon_mth + 2`` and ``y`` to ``omega_age_max - issue_age_min + 1``; every 2-D
    cache to one inner width, the widest of the timings', the benefits' and the claims',
    since gcc refuses two widths and MSVC, which builds the Windows leg, accepts them
    (USLIB-SEC-PLAN.md §7.2, *Record -- M15*); and the codes dense from 0, ints, as the
    caches index them, each family in its own numbering, ``DEATH`` one code in two, and
    the cells' and escalations' codes too.  A change to a bound or a size is derived again
    in the comment and here.
    """
    source, comment = _comment("spec_sec.py")
    for formula in ("12 * (omega_age_max - issue_age_min) + future_horizon_mth + 2",
                    "omega_age_max - issue_age_min + 1"):
        assert formula in comment, formula
    sizes = ast.literal_eval(source)["spaces"]["Projection"]["cells_param_size"]
    proj, data = _references("Projection"), _references("Data")
    for names in (TIMINGS, BENEFIT_CODES, CLAIM_CODES, CELL_CODES, ESCALATION_CODES):
        values = [proj[name] for name in names]
        assert values == list(range(len(names))), (names, values)
        assert all(type(v) is int for v in values), (names, values)
    span = proj["omega_age_max"] - proj["issue_age_min"]
    t = 12 * span + data["future_horizon_mth"] + 2
    width = max(len(TIMINGS), len(BENEFIT_CODES), len(CLAIM_CODES))
    assert sizes == {"t": t, ("t", "timing"): (t, width), ("t", "kind"): (t, width),
                     "y": span + 1}, sizes
    assert len({size[1] for size in sizes.values() if isinstance(size, tuple)}) == 1
    assert (t, width, span + 1) == (1358, 4, 104)


def test_the_sample_raises_the_recursion_limit_its_comment_derives():
    """``sample_sec.py`` sets the recursion limit its comment derives, before the import.

    The export does not raise the recursion limit as modelx does (F7), so the sample sets
    it, and its comment records the measured need: the deepest cold call at the longest
    cover needs the limit the comment states in the export, and the reports and checks the
    sample runs in ascending ``t`` less, from a script's top level (measured at M6).  The
    limit is four times the first, rounded up to the thousand.  No build can tell a lower
    limit above the reports' need: a limit of 1,000 builds the same model.  So this holds
    the limit, read from the sample's code, to the value derived from its comment's need,
    and holds the call before the import of the export.  A change to the need is measured
    again and written in the comment.
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
# which Data.point_id refuses when a refusal first names a point, here a point past the
# limiting age; and a timing, a benefit and a kind no cell takes, past the four codes of
# each family, each refused by the cell, as WOL_UK_S's are, ValueError and its message.
NOT_HELD = [
    ("a label with a fraction",
     lambda t: _moved_on(9, 600)(t).rename(index={9: 9.5}),
     "result_cf", (), "model_point_table_sec.csv: point_id must be a whole number; [9.5] "
     "is not"),
    ("a label of 2**53", lambda t: _moved_on(9, 600)(t).rename(
        index={9: 2 ** 53}), "result_cf", (),
     f"model_point_table_sec.csv: point_id must be below 2**53 in size; [{2 ** 53}] is "
     f"not"),
    ("a timing no cell takes", None, "pols_if_at", (0, 4), "invalid timing"),
    ("a benefit no cell takes", None, "benefit_pp", (0, 4), "invalid kind"),
    ("a kind no cell takes", None, "claims", (0, 4), "invalid kind"),
]


@pytest.mark.parametrize("case, edit, cell, args, message", NOT_HELD,
                         ids=[c[0] for c in NOT_HELD])
def test_what_the_c_step_cannot_hold_or_take_is_refused(tmp_path, case, edit, cell, args,
                                                        message):
    """A label the vectors cannot hold, and a code no cell takes, are refused.

    ``Data.point_id`` reads each label by value, and refuses one that is not a whole
    number, or is ``2**53`` or more in size, naming every such label, when a refusal first
    names a point: here the anchor cell at its crossover month, the table's ninth row,
    moved on to the limiting age with the history the move gives it (:func:`_moved_on`), a
    refusal of ``proj_len()``'s, which meets the label's own first.  A projection that
    names no point reads no label, and runs.  And a timing, a benefit or a kind no cell
    takes is refused by the cell, as ``WOL_UK_S``'s are (:data:`NOT_HELD`), on point 1.
    Every code inside the one inner width, 4, is one its cell takes, so no code inside a
    cache is refused: compiled, a code past it raises ``IndexError`` instead, which the
    compiled refusal test holds.
    """
    model = _read_edited(tmp_path, edit or (lambda t: t))
    try:
        keys = point_keys(model)
        p = projection(model, keys[8] if edit is not None else keys[0])
        _refused(lambda: p.cells[cell](*args), message)
        if edit is not None:
            assert len(projection(model, keys[0]).result_cf()) == 600
    finally:
        model.close()


# ---------------------------------------------------------------------------
# C2 -- the Phase 1 fingerprint


def test_the_phase_1_fingerprint_is_reproduced(sec_model):
    """Every committed point computes what the model computed when its E step ended (C2).

    The C step changes how the model is represented and no number it computes
    (UKLIB-SEC-PLAN.md U2, after USLIB-SEC-PLAN.md D2), so before it changed anything the
    model as M5 committed it was frozen below, and refrozen once when M5's review moved the
    instant of an anniversary at the valuation date (USLIB-SEC-PLAN.md §5.4): for each point,
    each column of ``result_cf()`` and ``result_pols()``, its sum, its largest absolute
    value and its values at five fixed months, the frame's first and last and the three
    quartiles between.  Every later version must reproduce it, to 1e-12 relative, floored
    at 1e-12 of the column's own magnitude (``uk_sec_support.fingerprint_mismatches``),
    with the same points, frames and columns exactly.  ``python
    tools/gen_sec_fingerprint.py WOL_UK_SEC --check`` runs the same comparison from the
    command line.
    """
    assert fingerprint_mismatches(FINGERPRINT, sec_model) == []


# WOL_UK_SEC's fingerprint, frozen from the model as M5 committed it and committed alone,
# before its C step changed anything; refrozen once, alone, when M5's review moved the
# cover and premium columns before month 0's events, which moved points 15 and 16, valued
# on an anniversary under References of their own.  Each point is keyed by its point_id;
# each column holds (its sum over the frame, its largest absolute value, (its values at
# the months)).
# The block is written by tools/gen_sec_fingerprint.py, and is never edited by hand: a
# refreeze goes through the tool's --force, in a commit of its own that says why.
# BEGIN generated fingerprint: WOL_UK_SEC -- tools/gen_sec_fingerprint.py
FINGERPRINT = {
    1: {"rows": 600, "months": (0, 149, 299, 449, 599),
        "result_cf": {
            "pols_if": (114.72542869134317, 1.0, (
                1.0, 0.32338578013476976, 0.03343488549823728, 5.265637242601398e-06, 0.0)),
            "pols_pu": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "premiums": (3296.8393833512946, 30.0, (
                30.0, 9.701573404043092, 0.0, 0.0, 0.0)),
            "claims_death": (2742.7905913148893, 11.286308984382895, (
                0.3622016939630002, 10.517455501513004, 3.715375696228344,
                0.003464980967042672, 0.0)),
            "claims_death_pu": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (509.1278461695021, 152.5, (
                152.5, 1.1526769916959823, 0.16991559547748794, 3.929780193114011e-05,
                0.0)),
            "commissions": (85.70735294691069, 7.5, (
                7.5, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-40.786407080007365, 130.36220169396302, (
                -130.36220169396302, -1.9685590891658937, -3.885291291705832,
                -0.003504278768973812, 0.0)),
        },
        "result_pols": {
            "pols_if": (114.72542869134317, 1.0, (
                1.0, 0.32338578013476976, 0.03343488549823728, 5.265637242601398e-06, 0.0)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_pu": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.5701155297708609, 0.002257261796876579, (
                0.002022343349877165, 0.0021034911003026007, 0.0007430751392456689,
                6.929961934085344e-07, 0.0)),
            "pols_death_pu": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_lapse": (0.4298844702291391, 0.006910379149139073, (
                0.006910379149139073, 0.001091091745431058, 0.0, 0.0, 0.0)),
            "pols_convert": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "prem_cum_pp": (3459600.0, 7200.0, (
                30.0, 4500.0, 7200.0, 7200.0, 7200.0)),
            "cover_pp": (3000000.0, 5000.0, (
                5000.0, 5000.0, 5000.0, 5000.0, 5000.0)),
            "benefit_death_pp": (2944069.8, 5000.0, (
                179.1, 5000.0, 5000.0, 5000.0, 5000.0)),
            "mort_rate": (247.46665603728002, 1.0, (
                0.024, 0.07532228099999999, 0.2363935842, 0.81609476604, 1.0)),
            "lapse_rate": (10.32, 0.08, (
                0.08, 0.04, 0.0, 0.0, 0.0)),
        },
    },
    2: {"rows": 600, "months": (0, 149, 299, 449, 599),
        "result_cf": {
            "pols_if": (114.72542869134317, 1.0, (
                1.0, 0.32338578013476976, 0.03343488549823728, 5.265637242601398e-06, 0.0)),
            "pols_pu": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "premiums": (3296.8393833512946, 30.0, (
                30.0, 9.701573404043092, 0.0, 0.0, 0.0)),
            "claims_death": (2824.841326875163, 11.624898253914383, (
                0.3622016939630002, 10.832979166558394, 3.8268369671151947,
                0.0035689303960539523, 0.0)),
            "claims_death_pu": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (509.1278461695021, 152.5, (
                152.5, 1.1526769916959823, 0.16991559547748794, 3.929780193114011e-05,
                0.0)),
            "commissions": (85.70735294691069, 7.5, (
                7.5, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-122.83714264028123, 130.36220169396302, (
                -130.36220169396302, -2.284082754211284, -3.9967525625926825,
                -0.0036082281979850925, 0.0)),
        },
        "result_pols": {
            "pols_if": (114.72542869134317, 1.0, (
                1.0, 0.32338578013476976, 0.03343488549823728, 5.265637242601398e-06, 0.0)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_pu": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.5701155297708609, 0.002257261796876579, (
                0.002022343349877165, 0.0021034911003026007, 0.0007430751392456689,
                6.929961934085344e-07, 0.0)),
            "pols_death_pu": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_lapse": (0.4298844702291391, 0.006910379149139073, (
                0.006910379149139073, 0.001091091745431058, 0.0, 0.0, 0.0)),
            "pols_convert": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "prem_cum_pp": (3459600.0, 7200.0, (
                30.0, 4500.0, 7200.0, 7200.0, 7200.0)),
            "cover_pp": (3000000.0, 5000.0, (
                5000.0, 5000.0, 5000.0, 5000.0, 5000.0)),
            "benefit_death_pp": (3032269.8, 5150.0, (
                179.1, 5150.0, 5150.0, 5150.0, 5150.0)),
            "mort_rate": (247.46665603728002, 1.0, (
                0.024, 0.07532228099999999, 0.2363935842, 0.81609476604, 1.0)),
            "lapse_rate": (10.32, 0.08, (
                0.08, 0.04, 0.0, 0.0, 0.0)),
        },
    },
    3: {"rows": 600, "months": (0, 149, 299, 449, 599),
        "result_cf": {
            "pols_if": (114.72542869134317, 1.0, (
                1.0, 0.32338578013476976, 0.03343488549823728, 5.265637242601398e-06, 0.0)),
            "pols_pu": (7.722306625015724, 0.05732805609862964, (
                0.0, 0.03474597957753035, 0.0170271665376639, 2.681596808860805e-06, 0.0)),
            "premiums": (3296.8393833512946, 30.0, (
                30.0, 9.701573404043092, 0.0, 0.0, 0.0)),
            "claims_death": (2742.7905913148893, 11.286308984382895, (
                0.3622016939630002, 10.517455501513004, 3.715375696228344,
                0.003464980967042672, 0.0)),
            "claims_death_pu": (344.601138660018, 2.671127347993102, (
                0.0, 0.6320942172298808, 1.3864514174568086, 0.0012930126495939481, 0.0)),
            "claims_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (541.974134943921, 152.5, (
                152.5, 1.2765256383379795, 0.2564474049461954, 5.931073776371327e-05, 0.0)),
            "commissions": (85.70735294691069, 7.5, (
                7.5, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-418.2338345144443, 130.36220169396302, (
                -130.36220169396302, -2.7245019530377714, -5.358274518631348,
                -0.004817304354400333, 0.0)),
        },
        "result_pols": {
            "pols_if": (114.72542869134317, 1.0, (
                1.0, 0.32338578013476976, 0.03343488549823728, 5.265637242601398e-06, 0.0)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_pu": (7.722306625015724, 0.05732805609862964, (
                0.0, 0.03474597957753035, 0.0170271665376639, 2.681596808860805e-06, 0.0)),
            "pols_death": (0.5701155297708609, 0.002257261796876579, (
                0.002022343349877165, 0.0021034911003026007, 0.0007430751392456689,
                6.929961934085344e-07, 0.0)),
            "pols_death_pu": (0.09946495445807699, 0.0007290632593001773, (
                0.0, 0.0002260082641301418, 0.00037842104010198704, 3.5291766127795995e-07,
                0.0)),
            "pols_lapse": (0.33041951577106216, 0.006910379149139073, (
                0.006910379149139073, 0.0, 0.0, 0.0, 0.0)),
            "pols_convert": (0.09946495445807695, 0.0014384879451534512, (
                0.0, 0.001091091745431058, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "prem_cum_pp": (3459600.0, 7200.0, (
                30.0, 4500.0, 7200.0, 7200.0, 7200.0)),
            "cover_pp": (3000000.0, 5000.0, (
                5000.0, 5000.0, 5000.0, 5000.0, 5000.0)),
            "benefit_death_pp": (2944069.8, 5000.0, (
                179.1, 5000.0, 5000.0, 5000.0, 5000.0)),
            "mort_rate": (247.46665603728002, 1.0, (
                0.024, 0.07532228099999999, 0.2363935842, 0.81609476604, 1.0)),
            "lapse_rate": (10.32, 0.08, (
                0.08, 0.04, 0.0, 0.0, 0.0)),
        },
    },
    4: {"rows": 600, "months": (0, 149, 299, 449, 599),
        "result_cf": {
            "pols_if": (114.72542869134317, 1.0, (
                1.0, 0.32338578013476976, 0.03343488549823728, 5.265637242601398e-06, 0.0)),
            "pols_pu": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "premiums": (4476.866602558695, 30.0, (
                30.0, 16.452718204551218, 0.0, 0.0, 0.0)),
            "claims_death": (4019.710590529493, 15.934062393626284, (
                0.3622016939630002, 14.995376683202407, 7.552593818579198,
                0.010343753621033163, 0.0)),
            "claims_death_pu": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (509.1278461695021, 152.5, (
                152.5, 1.1526769916959823, 0.16991559547748794, 3.929780193114011e-05,
                0.0)),
            "commissions": (85.70735294691069, 7.5, (
                7.5, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-137.6791870872106, 130.36220169396302, (
                -130.36220169396302, 0.30466452965282853, -7.722509414056686,
                -0.010383051422964303, 0.0)),
        },
        "result_pols": {
            "pols_if": (114.72542869134317, 1.0, (
                1.0, 0.32338578013476976, 0.03343488549823728, 5.265637242601398e-06, 0.0)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_pu": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.5701155297708609, 0.002257261796876579, (
                0.002022343349877165, 0.0021034911003026007, 0.0007430751392456689,
                6.929961934085344e-07, 0.0)),
            "pols_death_pu": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_lapse": (0.4298844702291391, 0.006910379149139073, (
                0.006910379149139073, 0.001091091745431058, 0.0, 0.0, 0.0)),
            "pols_convert": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "prem_cum_pp": (5230802.107143078, 11293.712198699246, (
                30.0, 5872.310120041152, 11293.712198699246, 11293.712198699246,
                11293.712198699246)),
            "cover_pp": (6767812.037414186, 21281.097178189782, (
                5000.0, 7128.804434230897, 10163.97053230202, 14926.133389213763,
                21281.097178189782)),
            "benefit_death_pp": (6711881.837414185, 21281.097178189782, (
                179.1, 7128.804434230896, 10163.970532302019, 14926.133389213763,
                21281.097178189782)),
            "mort_rate": (247.46665603728002, 1.0, (
                0.024, 0.07532228099999999, 0.2363935842, 0.81609476604, 1.0)),
            "lapse_rate": (10.32, 0.08, (
                0.08, 0.04, 0.0, 0.0, 0.0)),
        },
    },
    5: {"rows": 960, "months": (0, 239, 479, 719, 959),
        "result_cf": {
            "pols_if": (308.58218922392905, 1.0, (
                1.0, 0.5728814419221651, 0.2700455819277968, 0.014630523250624694, 0.0)),
            "pols_pu": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "premiums": (31243.946658922818, 101.25, (
                101.25, 58.00424599461921, 27.342115170189427, 1.4813404791257503, 0.0)),
            "claims_death": (57996.165313486155, 161.45180244556863, (
                11.142172830996692, 39.51631272158369, 127.17144792767878,
                51.777039859802365, 0.0)),
            "claims_death_pu": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (2749.8560487432596, 304.1666666666667, (
                304.1666666666667, 4.1856294837752275, 3.5635068519856654,
                0.34869432118605953, 0.0)),
            "commissions": (295.1830886463622, 25.3125, (
                25.3125, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-29797.257791952958, 239.37133949766337, (
                -239.37133949766337, 14.302303789260296, -103.39283960947502,
                -50.644393701862676, 0.0)),
        },
        "result_pols": {
            "pols_if": (308.58218922392905, 1.0, (
                1.0, 0.5728814419221651, 0.2700455819277968, 0.014630523250624694, 0.0)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_pu": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.3866498138438875, 0.0010763453496371242, (
                7.503095530070336e-05, 0.0002634420848105579, 0.0008478096528511919,
                0.00034518026573201576, 0.0)),
            "pols_death_pu": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_lapse": (0.6133501861561121, 0.0051426269466570505, (
                0.0051426269466570505, 0.0009632251039910364, 0.00045282902784638354,
                2.4029983315367736e-05, 0.0)),
            "pols_convert": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "prem_cum_pp": (46704600.0, 97200.0, (
                101.25, 24300.0, 48600.0, 72900.0, 97200.0)),
            "cover_pp": (144000000.0, 150000.0, (
                150000.0, 150000.0, 150000.0, 150000.0, 150000.0)),
            "benefit_death_pp": (143982078.975, 150000.0, (
                148501.0125, 150000.0, 150000.0, 150000.0, 150000.0)),
            "mort_rate": (196.7690000964, 1.0, (
                0.0009, 0.0055043181, 0.0370303, 0.2491213414, 1.0)),
            "lapse_rate": (20.4, 0.06, (
                0.06, 0.02, 0.02, 0.02, 0.02)),
        },
    },
    6: {"rows": 960, "months": (0, 239, 479, 719, 959),
        "result_cf": {
            "pols_if": (308.58218922392905, 1.0, (
                1.0, 0.5728814419221651, 0.2700455819277968, 0.014630523250624694, 0.0)),
            "pols_pu": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "premiums": (503632.0380498866, 1399.4122141697894, (
                101.25, 354.7486927177009, 1124.9852529655527, 410.0372525484368, 0.0)),
            "claims_death": (486045.1197572478, 1827.8101935618524, (
                11.142172830996692, 99.85575415233079, 852.6529123003878, 921.0980500844421,
                0.0)),
            "claims_death_pu": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (2749.8560487432596, 304.1666666666667, (
                304.1666666666667, 4.1856294837752275, 3.5635068519856654,
                0.34869432118605953, 0.0)),
            "commissions": (295.1830886463622, 25.3125, (
                25.3125, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (14541.879155249087, 760.1188542795003, (
                -239.37133949766337, 250.7073090815949, 268.76883381317924,
                -511.40949185719137, 0.0)),
        },
        "result_pols": {
            "pols_if": (308.58218922392905, 1.0, (
                1.0, 0.5728814419221651, 0.2700455819277968, 0.014630523250624694, 0.0)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_pu": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.3866498138438875, 0.0010763453496371242, (
                7.503095530070336e-05, 0.0002634420848105579, 0.0008478096528511919,
                0.00034518026573201576, 0.0)),
            "pols_death_pu": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_lapse": (0.6133501861561121, 0.0051426269466570505, (
                0.0051426269466570505, 0.0009632251039910364, 0.00045282902784638354,
                2.4029983315367736e-05, 0.0)),
            "pols_convert": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "prem_cum_pp": (3135138944.8125124, 24875912.607213527, (
                101.25, 69589.12438430607, 537749.9551533383, 3687301.9204282453,
                24875912.607213527)),
            "cover_pp": (1748211878.4063323, 7080205.8666918, (
                150000.0, 379042.529306346, 1005712.6731606653, 2668455.127731856,
                7080205.8666918)),
            "benefit_death_pp": (1748193957.3813324, 7080205.8666918, (
                148501.0125, 379042.529306346, 1005712.6731606653, 2668455.127731856,
                7080205.8666918)),
            "mort_rate": (196.7690000964, 1.0, (
                0.0009, 0.0055043181, 0.0370303, 0.2491213414, 1.0)),
            "lapse_rate": (20.4, 0.06, (
                0.06, 0.02, 0.02, 0.02, 0.02)),
        },
    },
    7: {"rows": 660, "months": (0, 164, 329, 494, 659),
        "result_cf": {
            "pols_if": (98.78170848228129, 1.0, (
                1.0, 0.20455288798561502, 0.002167274414410266, 0.0, 0.0)),
            "pols_pu": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "premiums": (4437.558965477801, 45.0, (
                45.0, 9.204879959352676, 0.0, 0.0, 0.0)),
            "claims_death": (5780.4632888393735, 29.36945527351167, (
                1.0061256623035115, 21.55134726383172, 1.063458608812075, 0.0, 0.0)),
            "claims_death_pu": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (448.4886255712781, 152.5, (
                152.5, 0.750982030476893, 0.012035357071957567, 0.0, 0.0)),
            "commissions": (127.93387212352953, 11.25, (
                11.25, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-1919.3268210563792, 119.7561256623035, (
                -119.7561256623035, -13.097449334955936, -1.0754939658840326, 0.0, 0.0)),
        },
        "result_pols": {
            "pols_if": (98.78170848228129, 1.0, (
                1.0, 0.20455288798561502, 0.002167274414410266, 0.0, 0.0)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_pu": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.6094141934830261, 0.002936945527351167, (
                0.002927762730404515, 0.002155134726383172, 0.00010634586088120749, 0.0,
                0.0)),
            "pols_death_pu": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_lapse": (0.3905858065169741, 0.006904109678909223, (
                0.006904109678909223, 0.0006873535374097411, 0.0, 0.0, 0.0)),
            "pols_convert": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "prem_cum_pp": (6891750.0, 13500.0, (
                45.0, 7425.0, 13500.0, 13500.0, 13500.0)),
            "cover_pp": (6600000.0, 10000.0, (
                10000.0, 10000.0, 10000.0, 10000.0, 10000.0)),
            "benefit_death_pp": (6487004.7, 10000.0, (
                343.65, 10000.0, 10000.0, 10000.0, 10000.0)),
            "mort_rate": (352.10017090992, 1.0, (
                0.03457289928, 0.11935502495999999, 0.45325050864, 1.0, 1.0)),
            "lapse_rate": (12.719999999999999, 0.08, (
                0.08, 0.04, 0.0, 0.0, 0.0)),
        },
    },
    8: {"rows": 594, "months": (0, 148, 296, 444, 593),
        "result_cf": {
            "pols_if": (108.85783431166041, 0.9475864076695066, (
                0.9475864076695066, 0.3077253423036933, 0.03109145420377051,
                4.572641049192864e-06, 0.0)),
            "pols_pu": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "premiums": (3120.8115519608123, 28.4275922300852, (
                28.4275922300852, 9.231760269110799, 0.0, 0.0, 0.0)),
            "claims_death": (2739.811102637476, 11.286308984382895, (
                0.6778112512534888, 10.008132061397868, 3.8527782412534606,
                0.0030089642477429367, 0.0)),
            "claims_death_pu": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (339.5092134322118, 2.3689660191737665, (
                2.3689660191737665, 1.0968568923698947, 0.1580063121667706,
                3.412592512062353e-05, 0.0)),
            "commissions": (41.700395099290155, 7.1068980575213, (
                7.1068980575213, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-0.20915920816506173, 18.273916902136648, (
                18.273916902136648, -1.8732286846569637, -4.0107845534202315,
                -0.0030430901728635603, 0.0)),
        },
        "result_pols": {
            "pols_if": (108.85783431166041, 0.9475864076695066, (
                0.9475864076695066, 0.3077253423036933, 0.03109145420377051,
                4.572641049192864e-06, 0.0)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_pu": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.5582492392973328, 0.002257261796876579, (
                0.0019163450699844187, 0.0020016264122795736, 0.0007705556482506921,
                6.017928495485873e-07, 0.0)),
            "pols_death_pu": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_lapse": (0.3893371683721738, 0.006548181353566956, (
                0.006548181353566956, 0.0010382540033379987, 0.0, 0.0, 0.0)),
            "pols_convert": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "prem_cum_pp": (3458970.0, 7200.0, (
                210.0, 4650.0, 7200.0, 7200.0, 7200.0)),
            "cover_pp": (2970000.0, 5000.0, (
                5000.0, 5000.0, 5000.0, 5000.0, 5000.0)),
            "benefit_death_pp": (2942558.7, 5000.0, (
                353.7, 5000.0, 5000.0, 5000.0, 5000.0)),
            "mort_rate": (247.32265603728, 1.0, (
                0.024, 0.07532228099999999, 0.26003294268, 0.81609476604, 1.0)),
            "lapse_rate": (9.84, 0.08, (
                0.08, 0.04, 0.0, 0.0, 0.0)),
        },
    },
    9: {"rows": 434, "months": (0, 108, 216, 324, 433),
        "result_cf": {
            "pols_if": (18.015819242028112, 0.27130934818144503, (
                0.27130934818144503, 0.05654313507900997, 0.0016654512969787995, 0.0, 0.0)),
            "pols_pu": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "premiums": (395.55109987184323, 8.139280445443351, (
                8.139280445443351, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (1134.84656953584, 10.534292367451181, (
                9.742065844452595, 5.075020360965567, 0.4176135699604161, 0.0, 0.0)),
            "claims_death_pu": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (50.857325198769864, 0.6782733704536126, (
                0.6782733704536126, 0.18443991595181725, 0.007088298374653967, 0.0, 0.0)),
            "commissions": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-790.1527948627665, 7.451380813889131, (
                -2.281058769462857, -5.259460276917384, -0.42470186833507007, 0.0, 0.0)),
        },
        "result_pols": {
            "pols_if": (18.015819242028112, 0.27130934818144503, (
                0.27130934818144503, 0.05654313507900997, 0.0016654512969787995, 0.0, 0.0)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_pu": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.22696931390716799, 0.0021068584734902362, (
                0.0019484131688905192, 0.0010150040721931134, 8.352271399208322e-05, 0.0,
                0.0)),
            "pols_death_pu": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_lapse": (0.04434003427427714, 0.0009147640650128105, (
                0.0009147640650128105, 0.0, 0.0, 0.0, 0.0)),
            "pols_convert": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "prem_cum_pp": (3043770.0, 7200.0, (
                5010.0, 7200.0, 7200.0, 7200.0, 7200.0)),
            "cover_pp": (2170000.0, 5000.0, (
                5000.0, 5000.0, 5000.0, 5000.0, 5000.0)),
            "benefit_death_pp": (2170000.0, 5000.0, (
                5000.0, 5000.0, 5000.0, 5000.0, 5000.0)),
            "mort_rate": (239.57556984936, 1.0, (
                0.08285450916, 0.19536659856, 0.46066421987999995, 1.0, 1.0)),
            "lapse_rate": (2.96, 0.04, (
                0.04, 0.0, 0.0, 0.0, 0.0)),
        },
    },
    10: {"rows": 400, "months": (0, 99, 199, 299, 399),
        "result_cf": {
            "pols_if": (10.346690223563272, 0.18020175881063383, (
                0.18020175881063383, 0.03343488549823728, 0.0006045439654619611, 0.0, 0.0)),
            "pols_pu": (4.661759492952453, 0.05732805609862964, (
                0.057169538009509614, 0.0170271665376639, 0.00030787217081402124, 0.0,
                0.0)),
            "premiums": (165.47722931789804, 5.406052764319015, (
                5.406052764319015, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (808.4239246949178, 9.163270837802965, (
                8.730827346033395, 3.715375696228344, 0.19849970829825014, 0.0, 0.0)),
            "claims_death_pu": (272.64141565070156, 2.671127347993102, (
                1.8251514680133294, 1.3864514174568086, 0.074073317057613, 0.0, 0.0)),
            "claims_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (41.76254963938744, 0.5934282420503586, (
                0.5934282420503586, 0.15980954441126166, 0.0036604001225492657, 0.0, 0.0)),
            "commissions": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-957.3506606671089, 10.234335809638676, (
                -5.743354291778068, -5.261636658096415, -0.2762334254784124, 0.0, 0.0)),
        },
        "result_pols": {
            "pols_if": (10.346690223563272, 0.18020175881063383, (
                0.18020175881063383, 0.03343488549823728, 0.0006045439654619611, 0.0, 0.0)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_pu": (4.661759492952453, 0.05732805609862964, (
                0.057169538009509614, 0.0170271665376639, 0.00030787217081402124, 0.0,
                0.0)),
            "pols_death": (0.16168478493898353, 0.0018326541675605932, (
                0.0017461654692066792, 0.0007430751392456689, 3.969994165965003e-05, 0.0,
                0.0)),
            "pols_death_pu": (0.07568651188116, 0.0007290632593001773, (
                0.000553976131096527, 0.00037842104010198704, 2.0217730914916414e-05, 0.0,
                0.0)),
            "pols_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_convert": (0.01851697387165037, 0.0006060446886318847, (
                0.0006060446886318847, 0.0, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "prem_cum_pp": (2856600.0, 7200.0, (
                6030.0, 7200.0, 7200.0, 7200.0, 7200.0)),
            "cover_pp": (2000000.0, 5000.0, (
                5000.0, 5000.0, 5000.0, 5000.0, 5000.0)),
            "benefit_death_pp": (2000000.0, 5000.0, (
                5000.0, 5000.0, 5000.0, 5000.0, 5000.0)),
            "mort_rate": (236.23089902447998, 1.0, (
                0.11027935164000001, 0.2363935842, 0.55740370608, 1.0, 1.0)),
            "lapse_rate": (1.6, 0.04, (
                0.04, 0.0, 0.0, 0.0, 0.0)),
        },
    },
    11: {"rows": 414, "months": (0, 103, 206, 309, 413),
        "result_cf": {
            "pols_if": (13.130544205870645, 0.21538403111628068, (
                0.21538403111628068, 0.04186089727076868, 0.0009380613326661115, 0.0, 0.0)),
            "pols_pu": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "premiums": (525.6334139256243, 12.504868018246096, (
                12.504868018246096, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (1730.9208986171625, 15.563277464552115, (
                14.705844670080682, 9.455942476131838, 0.6907498563377353, 0.0, 0.0)),
            "claims_death_pu": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (36.67748811721925, 0.5384600777907017, (
                0.5384600777907017, 0.1325703306066257, 0.0038761811315571656, 0.0, 0.0)),
            "commissions": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-1241.9649728087575, 13.204697714115694, (
                -2.739436729625287, -9.588512806738464, -0.6946260374692925, 0.0, 0.0)),
        },
        "result_pols": {
            "pols_if": (13.130544205870645, 0.21538403111628068, (
                0.21538403111628068, 0.04186089727076868, 0.0009380613326661115, 0.0, 0.0)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_pu": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.18750061294798873, 0.0019397039963636633, (
                0.0018878244196103248, 0.0009303394225790007, 5.364875010814619e-05, 0.0,
                0.0)),
            "pols_death_pu": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_lapse": (0.02788341816829203, 0.0007250444757089917, (
                0.0007250444757089917, 0.0, 0.0, 0.0, 0.0)),
            "pols_convert": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "prem_cum_pp": (4580785.422967019, 11293.712198699246, (
                7888.668857778385, 11293.712198699246, 11293.712198699246,
                11293.712198699246, 11293.712198699246)),
            "cover_pp": (5605138.1817146335, 21281.097178189782, (
                7789.837083003826, 10163.970532302019, 12875.413778425564,
                16799.49462879525, 21281.097178189782)),
            "benefit_death_pp": (5605138.181714633, 21281.097178189782, (
                7789.837083003826, 10163.970532302019, 12875.413778425562,
                16799.49462879525, 21281.097178189782)),
            "mort_rate": (237.71465757407998, 1.0, (
                0.10025395608, 0.2363935842, 0.50673064188, 1.0, 1.0)),
            "lapse_rate": (2.16, 0.04, (
                0.04, 0.0, 0.0, 0.0, 0.0)),
        },
    },
    12: {"rows": 948, "months": (0, 236, 473, 710, 947),
        "result_cf": {
            "pols_if": (296.9206351045666, 0.9391540000000004, (
                0.9391540000000004, 0.5617281575281621, 0.26191431207585203,
                0.013474623012090353, 0.0)),
            "pols_pu": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "premiums": (502451.30569530115, 1399.4122141697894, (
                104.59827675000005, 382.62639781967977, 1200.222237204407,
                415.40599982603595, 0.0)),
            "claims_death": (485915.17988846486, 1827.8101935618524, (
                12.208672963559183, 113.11667034715332, 956.8367358331232,
                994.2448036293057, 0.0)),
            "claims_death_pu": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (2331.32644651707, 4.21727583614519, (
                3.9131416666666685, 4.104140518372834, 3.4562070560552987,
                0.32114535098656055, 0.0)),
            "commissions": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (14204.7993603192, 760.0926553106705, (
                88.4764621197742, 265.4055869541536, 239.92929431522862, -579.1599491542562,
                0.0)),
        },
        "result_pols": {
            "pols_if": (296.9206351045666, 0.9391540000000004, (
                0.9391540000000004, 0.5617281575281621, 0.26191431207585203,
                0.013474623012090353, 0.0)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_pu": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.38577483629802095, 0.0010763453496371242, (
                7.751538389561386e-05, 0.0002842165559430285, 0.0009060968466092433,
                0.00035484944196350064, 0.0)),
            "pols_death_pu": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_lapse": (0.5533791637019793, 0.004005460563398711, (
                0.004005460563398711, 0.0009444287440871752, 0.0004390530254517186,
                2.2069329404618374e-05, 0.0)),
            "pols_convert": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "prem_cum_pp": (3135131047.312513, 24875912.607213527, (
                1326.375, 75719.55871312901, 565244.9529110052, 3779788.2184389513,
                24875912.607213527)),
            "cover_pp": (1746411878.4063323, 7080205.8666918, (
                157500.0, 397994.65577166335, 1055998.3068186988, 2801877.8841184494,
                7080205.8666918)),
            "benefit_death_pp": (1746411878.4063323, 7080205.8666918, (
                157500.0, 397994.65577166335, 1055998.3068186988, 2801877.8841184494,
                7080205.8666918)),
            "mort_rate": (196.7582000964, 1.0, (
                0.00099, 0.00605475, 0.04073333, 0.2740334756, 1.0)),
            "lapse_rate": (19.68, 0.05, (
                0.05, 0.02, 0.02, 0.02, 0.02)),
        },
    },
    13: {"rows": 360, "months": (0, 89, 179, 269, 359),
        "result_cf": {
            "pols_if": (0.16928702721902053, 0.007579814271932304, (
                0.007579814271932304, 2.66879672345351e-05, 0.0, 0.0, 0.0)),
            "pols_pu": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (75.79814271932307, 2.9073855572538516, (
                2.9073855572538516, 0.02758451816315208, 0.0, 0.0, 0.0)),
            "claims_death_pu": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (0.43759912339065327, 0.018949535679830758, (
                0.018949535679830758, 8.205708355767492e-05, 0.0, 0.0, 0.0)),
            "commissions": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-76.23574184271372, 2.9263350929336824, (
                -2.9263350929336824, -0.027666575246709756, 0.0, 0.0, 0.0)),
        },
        "result_pols": {
            "pols_if": (0.16928702721902053, 0.007579814271932304, (
                0.007579814271932304, 2.66879672345351e-05, 0.0, 0.0, 0.0)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_pu": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.0075798142719323055, 0.00029073855572538516, (
                0.00029073855572538516, 2.758451816315208e-06, 0.0, 0.0, 0.0)),
            "pols_death_pu": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_convert": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "prem_cum_pp": (4860000.0, 13500.0, (
                13500.0, 13500.0, 13500.0, 13500.0, 13500.0)),
            "cover_pp": (3600000.0, 10000.0, (
                10000.0, 10000.0, 10000.0, 10000.0, 10000.0)),
            "benefit_death_pp": (3600000.0, 10000.0, (
                10000.0, 10000.0, 10000.0, 10000.0, 10000.0)),
            "mort_rate": (311.29845516048, 1.0, (
                0.37458719712, 0.7299644766, 1.0, 1.0, 1.0)),
            "lapse_rate": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
        },
    },
    14: {"rows": 613, "months": (0, 153, 306, 459, 612),
        "result_cf": {
            "pols_if": (114.72542869134317, 1.0, (
                0.0, 0.3527415575057059, 0.03826176992717273, 8.04085840041836e-06, 0.0)),
            "pols_pu": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "premiums": (4476.866602558695, 30.0, (
                0.0, 17.173431328407993, 0.0, 0.0, 0.0)),
            "claims_death": (4019.7105905294925, 15.934062393626284, (
                0.0, 14.388461707963344, 8.64293694246685, 0.015795364238659997, 0.0)),
            "claims_death_pu": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (520.779713765115, 152.575, (
                0.0, 1.2573127896420944, 0.20027912355755415, 6.18097463999386e-05, 0.0)),
            "commissions": (85.7073529469107, 7.5, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-149.3310546828236, 130.437201693963, (
                0.0, 1.5276568308025544, -8.843216066024404, -0.015857173985059935, 0.0)),
        },
        "result_pols": {
            "pols_if": (114.72542869134317, 1.0, (
                0.0, 0.3527415575057059, 0.03826176992717273, 8.04085840041836e-06, 0.0)),
            "pols_new_biz": (1.0, 1.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_pu": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.5701155297708609, 0.002257261796876579, (
                0.0, 0.002078906175071857, 0.0008503504526108979, 1.0582355005667024e-06,
                0.0)),
            "pols_death_pu": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_lapse": (0.42988447022913906, 0.006910379149139073, (
                0.0, 0.0011908690187923125, 0.0, 0.0, 0.0)),
            "pols_convert": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "prem_cum_pp": (5230802.107143078, 11293.712198699246, (
                0.0, 5420.994688028956, 11293.712198699246, 11293.712198699246,
                11293.712198699246)),
            "cover_pp": (6767812.037414186, 21281.097178189782, (
                0.0, 6921.169353622229, 10163.97053230202, 14926.133389213763,
                21281.097178189782)),
            "benefit_death_pp": (6711881.837414185, 21281.097178189782, (
                0.0, 6921.169353622229, 10163.970532302019, 14926.133389213763,
                21281.097178189782)),
            "mort_rate": (247.46665603728, 1.0, (
                0.0, 0.06847480092, 0.2363935842, 0.81609476604, 1.0)),
            "lapse_rate": (10.32, 0.08, (
                0.0, 0.04, 0.0, 0.0, 0.0)),
        },
    },
    15: {"rows": 480, "months": (0, 119, 239, 359, 479),
        "result_cf": {
            "pols_if": (33.921439348243936, 0.422137899377621, (
                0.422137899377621, 0.09992331667213186, 0.004988714607953328,
                3.619333640475052e-09, 0.0)),
            "pols_pu": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "premiums": (2044.4999513805672, 25.372780834669705, (
                25.372780834669705, 8.925389512823534, 0.0, 0.0, 0.0)),
            "claims_death": (3224.8436834751974, 18.945024999555464, (
                18.015290540388534, 13.688269052886431, 2.7358330820078076,
                2.0838260449587823e-05, 0.0)),
            "claims_death_pu": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (98.28471802324961, 1.0553447484440523, (
                1.0553447484440523, 0.3259431600826884, 0.0218693531553008,
                2.1322992029707165e-08, 0.0)),
            "commissions": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-1278.62845011788, 15.701315984897846, (
                6.302145545837118, -5.0888227001455855, -2.7577024351631083,
                -2.085958344161753e-05, 0.0)),
        },
        "result_pols": {
            "pols_if": (33.921439348243936, 0.422137899377621, (
                0.422137899377621, 0.09992331667213186, 0.004988714607953328,
                3.619333640475052e-09, 0.0)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_pu": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.3241114328646976, 0.0022549159049686574, (
                0.0022549159049686574, 0.0013131144786530464, 0.00019528613344444893,
                1.1068047764681482e-09, 0.0)),
            "pols_death_pu": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_lapse": (0.09802646651292349, 0.0014259449491933493, (
                0.0014259449491933493, 0.00033488549260507104, 0.0, 0.0, 0.0)),
            "pols_convert": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "prem_cum_pp": (6133035.532466132, 13956.009102134818, (
                5153.056930459325, 13956.009102134818, 13956.009102134818,
                13956.009102134818, 13956.009102134818)),
            "cover_pp": (7228875.88781609, 25302.456341582136, (
                7989.340312289359, 10424.27699596112, 14009.356597692293,
                18827.403795711314, 25302.456341582136)),
            "benefit_death_pp": (7228875.88781609, 25302.456341582136, (
                7989.340312289359, 10424.27699596112, 14009.356597692291, 18827.40379571131,
                25302.456341582136)),
            "mort_rate": (242.87667775248, 1.0, (
                0.06224981904, 0.14678181708, 0.38071423128, 0.9874746669599999, 1.0)),
            "lapse_rate": (4.8, 0.04, (
                0.04, 0.04, 0.0, 0.0, 0.0)),
        },
    },
    16: {"rows": 840, "months": (0, 209, 419, 629, 839),
        "result_cf": {
            "pols_if": (209.1490200413217, 0.7262110548597567, (
                0.7262110548597567, 0.462231094695573, 0.18949350013487623,
                0.005823471311495339, 0.0)),
            "pols_pu": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "premiums": (321027.6418967712, 920.6937295143598, (
                125.47415060526016, 403.66975759936764, 836.4442918821675,
                142.91999002676923, 0.0)),
            "claims_death": (389467.88611822366, 1471.438760231951, (
                27.817072319026842, 206.0138390785745, 1000.776248566815, 478.0818047431221,
                0.0)),
            "claims_death_pu": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (1472.0488716999487, 3.2321907657301328, (
                3.025879395248986, 3.183323210124824, 2.1569929020104124,
                0.11285125243335618, 0.0)),
            "commissions": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-69912.29309315239, 744.3640423010536, (
                94.63119889098432, 194.4725953106683, -166.4889495866579,
                -335.2746659687862, 0.0)),
        },
        "result_pols": {
            "pols_if": (209.1490200413217, 0.7262110548597567, (
                0.7262110548597567, 0.462231094695573, 0.18949350013487623,
                0.005823471311495339, 0.0)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_pu": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.37502343125645743, 0.0010763453496371242, (
                0.00014142170633155908, 0.00045696502811289644, 0.000968513045026669,
                0.0001922486580392382, 0.0)),
            "pols_death_pu": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_lapse": (0.3511876236032983, 0.0012213526261793885, (
                0.0012213526261793885, 0.0007767699132679163, 0.00031712590303851476,
                9.472519249329562e-06, 0.0)),
            "pols_convert": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "prem_cum_pp": (2064136872.211842, 16368768.435395626, (
                15454.918610746432, 104585.34898702255, 577210.5573615314,
                3086848.364247778, 16368768.435395626)),
            "cover_pp": (1389133866.552732, 5699765.423876013, (
                196695.91776675728, 450830.64655809355, 1033312.1001372342,
                2486788.7745959973, 5699765.423876013)),
            "benefit_death_pp": (1389133866.552732, 5699765.423876013, (
                196695.91776675728, 450830.64655809355, 1033312.1001372342,
                2486788.7745959973, 5699765.423876013)),
            "mort_rate": (196.59687591120002, 1.0, (
                0.0023343682, 0.0117989948, 0.0596376685, 0.3315805055, 1.0)),
            "lapse_rate": (16.799999999999997, 0.02, (
                0.02, 0.02, 0.02, 0.02, 0.02)),
        },
    },
    17: {"rows": 420, "months": (0, 104, 209, 314, 419),
        "result_cf": {
            "pols_if": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_pu": (20.255037425937065, 0.28519318513354724, (
                0.28519318513354724, 0.07004224820069264, 0.0016893719029589947, 0.0, 0.0)),
            "premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death_pu": (970.6153814850065, 8.50736895265714, (
                8.50736895265714, 4.758155634831591, 0.3288226057070529, 0.0, 0.0)),
            "claims_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (57.11232651496061, 0.7129829628338681, (
                0.7129829628338681, 0.2218185611344076, 0.006980685874580494, 0.0, 0.0)),
            "commissions": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-1027.7277079999672, 9.220351915491008, (
                -9.220351915491008, -4.979974195965998, -0.3358032915816334, 0.0, 0.0)),
        },
        "result_pols": {
            "pols_if": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_pu": (20.255037425937065, 0.28519318513354724, (
                0.28519318513354724, 0.07004224820069264, 0.0016893719029589947, 0.0, 0.0)),
            "pols_death": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death_pu": (0.28519318513354724, 0.0024996962700122014, (
                0.0024996962700122014, 0.001398075475357299, 9.661702055661835e-05, 0.0,
                0.0)),
            "pols_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_convert": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "prem_cum_pp": (2970900.0, 7200.0, (
                5430.0, 7200.0, 7200.0, 7200.0, 7200.0)),
            "cover_pp": (2100000.0, 5000.0, (
                5000.0, 5000.0, 5000.0, 5000.0, 5000.0)),
            "benefit_death_pp": (2100000.0, 5000.0, (
                5000.0, 5000.0, 5000.0, 5000.0, 5000.0)),
            "mort_rate": (238.31618131056, 1.0, (
                0.10025395608, 0.21490325844, 0.50673064188, 1.0, 1.0)),
            "lapse_rate": (2.4000000000000004, 0.04, (
                0.04, 0.0, 0.0, 0.0, 0.0)),
        },
    },
}
# END generated fingerprint: WOL_UK_SEC


# ---------------------------------------------------------------------------
# Compiled (UKLIB-SEC-PLAN.md U2, the C step, after USLIB-SEC-PLAN.md's Phase 2)
#
# These compile the model, once a session, into a temporary directory (conftest.sec_build),
# and run the compiled package in a child process only.  They skip without modelx-cython or
# a C compiler, and the cython_uk CI job, which sets UKLIB_REQUIRE_CYTHON=1, fails a skip.
# test_compiled_conventions_uk.py checks the compiled model's types, its caches and its
# release, and compares it with modelx on the committed points; these hold what is WOL's
# own: the comparison on the splice grid, at the contract's extremes, where each cap and
# bound binds, on every value a decoded column holds, on keys written as floats, on the
# committed rows under the References they were read from, and on the rows valued on an
# anniversary, whose increase is made at t = 0; the labels; the refusals and the
# overflows; the deepest calls on a 1 MiB stack; a Reference set late; and the runner.


def _as_modelx(have, want):
    """Whether a compiled value is modelx's: identical where ``exact_here()``, as on
    x86-64, and to 1e-12 relative elsewhere, as C4 compares (uk_sec_support)."""
    return have == want if exact_here() else have == pytest.approx(want, rel=1e-12, abs=0)


def _mismatch_lines(found):
    return f"{len(found)} mismatches, first:\n  " + "\n  ".join(found[:50])


# How many rows of a grid C4 compares at once.  compiled_mismatches sweeps every row of its
# case in one modelx read and keeps every value of every row, in the parent and in the
# child, until it compares them.  A WOL row runs at most 1,356 months, as ULB's do, so
# twenty rows hold about what its chunks of twenty do (UKLIB-SEC-PLAN.md §6.6, *Record --
# M10*).
C4_CHUNK = 20

# The committed rows a C4 comparison under References other than the shipped ones reads by
# default, by the References set.  An RPI moves the RPI rows alone, and a take-up the
# escalating rows alone, so under each the default compares every row it moves: under an
# RPI, of its own, of -2% or of 25%, the RPI rows, the twin, the row past its crossover,
# the row issued 13 months on and the row read under an RPI of 5%; under a take-up, those
# and the fixed increases' rows, the twin, the row on its first anniversary and the row
# read under a take-up of a half.  A stress of 100 moves 15 of the 17 committed rows, every
# row on which the premiums paid pass the cover while premiums are due; the default
# compares four of them: the paid-up rows, where a stressed lapse converts, the twin, the
# row with its strand in force and the row paid-up entirely, read under the stress; and the
# RPI row past its crossover, without the paid-up value, stressed from its first month,
# where a stressed lapse terminates.  The anniversary's References, an RPI and a take-up,
# move the seven escalating rows; the default compares the three valued on an
# anniversary, whose month-0 increase the test is for, the other four being compared under
# an RPI and under a take-up on their own.  So what the default leaves out under the stress
# and the anniversary's References is combinations, rows whose every branch another default
# comparison reaches, on the Windows legs alone, which run the default.  The full grid
# compares the whole committed table under each set, as the cython_uk job's Linux legs run
# it (UKLIB_SEC_FULL=1).  A compile test is never skipped, since a skip fails that job, so
# the default run compares these rows rather than none: the eight comparisons of the whole
# table took about 100 s of the default run (UKLIB-SEC-PLAN.md U6).  A test holds each
# selection to what modelx says of the rows (test_the_c4_comparisons_ask_every_code_and_
# their_rows).
RPI_ROWS = (4, 11, 14, 15)
ESCALATING_ROWS = (*RPI_ROWS, 6, 12, 16)
PAID_UP_ROWS = (3, 10, 17)
STRESSED_ROWS = (*PAID_UP_ROWS, 11)
ANNIVERSARY_ROWS = (12, 15, 16)
OWN_REFS_ROWS = {"rpi_rate": RPI_ROWS, "esc_take_up": ESCALATING_ROWS,
                 "lapse_crossover_beta": STRESSED_ROWS}


def _c4_rows(labels):
    """The committed table under ``UKLIB_SEC_FULL=1``, and its rows ``labels`` otherwise."""
    rows = _committed()
    return rows if SEC_FULL else rows.loc[list(labels)]


class _Asked:
    """A stand-in for a point, which records what :func:`_wol_c4_also` asks of it: each
    cell's calls, as (month, code), over a frame of ``months``, the codes read from the
    model's own References, ``refs``."""

    def __init__(self, months, refs):
        self.months, self.refs, self.asked = months, refs, {}
        self.cells = {name: self._cell(name) for name in ("pols_if_at", "benefit_pp",
                                                           "claims")}

    def _cell(self, name):
        return lambda t, code: self.asked.setdefault(name, set()).add((t, code))

    def proj_len(self):
        return self.months


def test_the_c4_comparisons_ask_every_code_and_their_rows(sec_model):
    """C4's ``also`` asks every code in every month, and each default selection is what
    modelx says of the committed rows.

    Nothing in a comparison shows what it leaves out: dropped from :func:`_wol_c4_also`, a
    code is simply not compared, and dropped from a selection, a row.  So
    :func:`_wol_c4_also` is run on a stand-in point (:class:`_Asked`), over a frame of five
    months, with the model's References read as the spec test reads them: it must ask
    ``pols_if_at``, ``benefit_pp`` and ``claims`` at every code inside the one inner width
    ``spec_sec.py`` gives, in every month of the frame and the month after it; and it must
    be the spec's ``c4_also``, which the conventions' C4 on the committed points passes
    (``uk_sec_support.spec_c4_also``).  And each selection of :data:`OWN_REFS_ROWS` and
    :data:`ANNIVERSARY_ROWS` is derived in modelx from the committed points: under each RPI
    the comparisons set, of 5%, -2% and 25%, the rows whose steps move are
    :data:`RPI_ROWS`, and under a take-up of a half :data:`ESCALATING_ROWS`; the stress's
    rows are the paid-up ones and those in force past their crossover with lapses running,
    each of whose lapse rates the stress moves; and the anniversary's are the escalating
    rows valued on an anniversary.
    """
    source, _ = _comment("spec_sec.py")
    sizes = ast.literal_eval(source)["spaces"]["Projection"]["cells_param_size"]
    (width,) = {size[1] for size in sizes.values() if isinstance(size, tuple)}
    stand_in = _Asked(5, _references("Projection"))
    _wol_c4_also(stand_in)
    every = {(t, code) for t in range(6) for code in range(width)}
    for cell in ("pols_if_at", "benefit_pp", "claims"):
        assert stand_in.asked.get(cell) == every, (cell, sorted(stand_in.asked.get(cell, ())))
    assert SPEC.c4_also is _wol_c4_also, SPEC.c4_also

    labels = dict(zip(sec_model.Data.model_point_table().index, point_keys(sec_model)))
    points = {label: projection(sec_model, key) for label, key in labels.items()}

    def steps(p):
        return p.esc_cover_step(), p.esc_prem_step()

    def moved(refs, of):
        model = mx.read_model(model_path(SEC), name=_name("moved"))
        try:
            for ref, value in refs.items():
                setattr(model.Projection, ref, value)
            return sorted(label for label, key in labels.items()
                          if of(projection(model, key)) != of(points[label]))
        finally:
            model.close()

    for rpi in (0.05, -0.02, 0.25):
        assert moved({"rpi_rate": rpi}, steps) == sorted(RPI_ROWS), rpi
    assert moved({"esc_take_up": 0.5}, steps) == sorted(ESCALATING_ROWS)
    stressed = sorted(label for label, p in points.items() if p.pu_variant() or (
        p.duration_mth_init() > 0 and p.crossover_mth_init() >= 0 and p.lapse_rate(0) > 0))
    assert stressed == sorted(STRESSED_ROWS), stressed

    def lapses(p):
        return [p.lapse_rate(t) for t in range(p.proj_len())]
    stress_moves = moved({"lapse_crossover_beta": 100.0}, lapses)
    assert set(STRESSED_ROWS) <= set(stress_moves), stress_moves
    level = _code(points[1], "LEVEL")
    anniversaries = sorted(label for label, p in points.items()
                           if p.escalation_code() != level and p.duration_mth_init() > 0
                           and p.duration_mth_init() % 12 == 0)
    assert anniversaries == sorted(ANNIVERSARY_ROWS), anniversaries


@pytest.mark.cython
def test_the_compiled_model_computes_what_modelx_computes_on_the_splice_grid(spliced,
                                                                             sec_build,
                                                                             tmp_path):
    """C4 on the branches: compiled, every cell of the splice grid is modelx's.

    The sample traces the committed points alone, and they leave branches untaken, which
    are typed all the same, because every branch of a cell returns the one type the others
    return (sample_sec.py).  What the compiled model computes on them is held here: the
    splice grid's rows, S's points and its five variants restated in force at T2's months
    and issued later, the RPI increases and the double accidental benefit with the paid-up
    value, an issue age of 80, an underwritten female smoker and an odd cessation among
    them, under the splice's References, the crossover stress on (:data:`SPLICED_REFS`).
    The grid is the one this run's ``spliced`` selects, the core by default and the full
    grid under ``UKLIB_SEC_FULL=1``, and the test carries no ``sec_full`` mark, since a
    skipped compile test fails the cython_uk job.  The grid's SEC table goes beside the
    build :data:`C4_CHUNK` rows at a time, modelx sweeps every point fully, and the
    compiled model must agree at every argument modelx caches, identically on x86-64 and
    to 1e-12 relative elsewhere, with every raise and every ``Data`` array
    (``uk_sec_support.compiled_mismatches``).
    """
    build = sec_build(SEC)
    folder = spliced[1].Data.input_dir()
    table = pd.read_csv(folder / TABLE, index_col="point_id")
    found = []
    for start in range(0, len(table), C4_CHUNK):
        chunk = table.iloc[start:start + C4_CHUNK]
        case = compiled_case(build, tmp_path / f"chunk{start}", model_points=chunk)
        found += [f"rows {start} on: {line}"
                  for line in compiled_mismatches(build, case, refs=SPLICED_REFS,
                                                 also=_wol_c4_also)]
    assert not found, _mismatch_lines(found)


# The contract's extremes (held by proj_len()): each shape at its longest cover, issued at
# the youngest issue age, 18, to the contract's largest limiting age, 121, 1,236 months, as
# (the S point it changes, its changes): the anchor cell, level, premiums ceasing at 240;
# the paid-up point, its strand in force from the first conversion; the RPI point; the
# underwritten level point and the underwritten increasing one, paying for life; and the
# over-50s male smoker.
EXTREMES = {
    21: (1, {"entry_age": 18}),
    22: (3, {"entry_age": 18}),
    23: (4, {"entry_age": 18}),
    24: (5, {"entry_age": 18}),
    25: (6, {"entry_age": 18}),
    26: (7, {"entry_age": 18}),
}


def _contract_extremes(tmp_path):
    """The rows at the contract's extremes, built by the generator.

    Each of :data:`EXTREMES` in a copy of S's table, read with :data:`LONGEST_REFS` set,
    the limiting age at 121, its twin issued at the valuation date, the same issued
    ``future_horizon_mth``, 120 months, after it, a frame of 1,356 months, and the same
    restated in force in the last month of its frame, opened with S's state there; so ``t``
    reaches 1,357, the policy year 103 and each code its last, the furthest ``spec_sec.py``
    sizes for.  S's tables serve: the mortality table runs from 18 to 120.  Returns the
    rows.
    """
    s_table = _s_table()
    rows = []
    for point_id, (base, changes) in EXTREMES.items():
        row = s_table.loc[[base]].assign(**changes, policy_id=f"WOL-7000{point_id}")
        row.index = pd.Index([point_id], name="point_id")
        rows.append(row)
    s = mx.read_model(temp_inputs(tmp_path, model_path(TWIN), model_points=pd.concat(rows)),
                      name=_name("extremes_s"))
    try:
        for ref, value in LONGEST_REFS.items():
            setattr(s.Projection, ref, value)
        last = {point_id: _point(s, point_id).proj_len() - 1 for point_id in EXTREMES}
        spec = dataclasses.replace(SPEC, derived=tuple(last.items()),
                                   future=tuple((p, 120) for p in EXTREMES),
                                   derived_refs={})
        table, _ = build_sec_table(spec, s)
    finally:
        s.close()
    return table


@pytest.mark.cython
def test_the_compiled_model_computes_what_modelx_computes_at_the_contract_extremes(
        sec_build, tmp_path):
    """C4 where the caches end: the contract's longest covers, every cell compiled.

    The rows of :func:`_contract_extremes`, each shape at its longest cover from the
    youngest issue age, issued now and 120 months on and in force in its last month, with
    every switch that ships off on and the limiting age at 121 (:data:`LONGEST_REFS`),
    read every cache as far as ``spec_sec.py`` sizes it for: ``t`` to 1,357, the
    roll-forward's month after the month after the 1,356-month frame; ``y`` to 103, the
    opening of the longest cover's last policy year, on each of the four chains; and every
    timing and kind.  modelx sweeps every row fully, and the compiled model must agree
    everywhere.  A cache one too small for the contract raises ``IndexError`` compiled
    where modelx reads on, and fails here, though the spec check passes it, which holds the
    caches to the spec and not the spec to the contract.
    """
    build = sec_build(SEC)
    rows = _contract_extremes(tmp_path / "s")
    covers = 12 * (OMEGA_MAX - rows["entry_age"]) - rows["duration_mth"]
    assert covers.max() == 1356
    folder = compiled_case(build, tmp_path / "extremes", model_points=rows)
    found = compiled_mismatches(build, folder, refs=LONGEST_REFS, also=_wol_c4_also)
    assert not found, _mismatch_lines(found)


def _capped_rows(tmp_path, points=tuple(CAPPED_POINTS)):
    """The rows of the mortality cap's test, on each of ``points``, by default every one of
    :data:`CAPPED_POINTS`: the twin, the row issued 12 months on, and the rows restated the
    month before the cap and five months into the capped year, the last opened with one
    policy, built from S under :data:`SPLICED_REFS`."""
    s = mx.read_model(model_path(TWIN), name=_name("capped_s"))
    try:
        for ref, value in SPLICED_REFS.items():
            setattr(s.Projection, ref, value)
        derived = tuple((p, d) for p in points for d in (CAPPED_POINTS[p][0] - 1,
                                                          CAPPED_POINTS[p][0] + 5))
        spec = dataclasses.replace(SPEC, derived=derived, derived_refs={},
                                   future=tuple((p, 12) for p in points))
        rows, _ = build_sec_table(spec, s)
    finally:
        s.close()
    rows.loc[(rows["row_kind"] == "derived") & (rows["policy_count"] == 0.0),
             "policy_count"] = 1.0
    return rows


def _lapse_all_rows():
    """The rows of the lapse bound's test, the anchor and paid-up points restated at their
    crossover and at 200, built from S under :data:`LAPSE_ALL`."""
    s = mx.read_model(model_path(TWIN), name=_name("lapse_all_s"))
    try:
        for ref, value in LAPSE_ALL.items():
            setattr(s.Projection, ref, value)
        spec = dataclasses.replace(SPEC, derived=((1, 166), (1, 200), (3, 166), (3, 200)),
                                   future=(), derived_refs={})
        rows, _ = build_sec_table(spec, s)
    finally:
        s.close()
    return rows


# Where each cap and each bound binds, as (case, the References): the mortality cap,
# min(q, 1.0), on the cap test's rows (_capped_rows); the RPI's floor at 0, under an RPI of
# -2%, and its two caps, the cover's 10% and the premium's 15%, under 25%, on the committed
# table, whose RPI rows step every year; and the lapse rate's bound at 1, min(1.0, w), under
# a stress of 100 (_lapse_all_rows).
BINDS = [("the mortality cap", SPLICED_REFS),
         ("the RPI's floor", {"rpi_rate": -0.02}),
         ("the RPI's caps", {"rpi_rate": 0.25}),
         ("the lapse rate's bound", LAPSE_ALL)]


@pytest.mark.cython
@pytest.mark.parametrize("case, refs", BINDS, ids=[c[0] for c in BINDS])
def test_the_compiled_model_computes_what_modelx_computes_where_each_cap_binds(
        sec_build, tmp_path, case, refs):
    """C4 where each cap and bound binds: compiled, every cell is modelx's.

    The splice grid and the committed points leave each bound's binding side mostly
    untaken: the cap on mortality binds only in the tail, where the splice's rows are few,
    the RPI's floor and caps not at all at the shipped 3%, and the lapse rate's bound only
    under a stress of 100.  So each case of :data:`BINDS` is first asserted to bind in
    modelx, on its rows, under its References: the capped rate 1.0, the cover's and the
    premium's steps 0.0, or 10% and 15%, the lapse rate 1.0; then modelx sweeps the rows
    fully under the same References, and the compiled model must agree at every argument
    modelx caches, identically on x86-64 and to 1e-12 relative elsewhere.  No other compiled
    test reaches these sides of the ``min`` and the ``max``.  By default the cap's rows are
    the male smoker's: the core grid's rows reach each capped point's capped months, the
    male smoker's row at 300 among them, but none is restated about a cap, and the row five
    months into the capped year, opened on one policy, is this test's alone; the RPI's rows
    are the committed RPI rows (:data:`RPI_ROWS`), the only ones an RPI moves.  With the
    full grid, all three capped points' rows and the whole committed table.
    """
    build = sec_build(SEC)
    if case == "the mortality cap":
        rows = _capped_rows(tmp_path / "s", tuple(CAPPED_POINTS) if SEC_FULL else (7,))
    elif case == "the lapse rate's bound":
        rows = _lapse_all_rows()
    else:
        rows = _c4_rows(RPI_ROWS)
    model = mx.read_model(_sec_inputs(tmp_path / "check", rows), name=_name("binds"))
    try:
        for ref, value in refs.items():
            setattr(model.Projection, ref, value)
        if case == "the mortality cap":
            bound = [any(p.mort_rate(t) == 1.0 for t in range(p.proj_len()))
                     for p in (projection(model, key) for key in point_keys(model))]
        elif case == "the lapse rate's bound":
            bound = [projection(model, key).lapse_rate(0) == 1.0 for key in point_keys(model)
                     if model.Data.model_point_table().iloc[key]["source_mth"] == 166]
        else:
            rpi = _row(model, "twin", 4, 0)
            steps = (0.0, 0.0) if refs["rpi_rate"] < 0.0 else (0.10, 0.15)
            bound = [(rpi.esc_cover_step(), rpi.esc_prem_step()) == steps]
    finally:
        model.close()
    assert bound and all(bound), (case, bound)
    folder = compiled_case(build, tmp_path / "binds", model_points=rows)
    found = compiled_mismatches(build, folder, refs=refs, also=_wol_c4_also)
    assert not found, _mismatch_lines(found)


@pytest.mark.cython
def test_the_compiled_model_computes_what_modelx_computes_on_every_decoded_value(
        sec_build, tmp_path):
    """C4 on every value a decoded column holds: compiled, every cell is modelx's.

    The twins of :data:`DECODED`'s points, each cell, each escalation on each cell, each of
    the eight mortality schedules, each variant's flag each way, an entry age with a
    fraction and an odd cessation, built by the generator from a copy of S's table, go
    beside the build: modelx sweeps them fully, and the compiled model must agree
    everywhere, each label's text, each decode's code and the mortality row it selects
    among them, which the committed points reach only in part: no committed point is an
    assured female smoker.
    """
    build = sec_build(SEC)
    s, twins = _decoded_twins(tmp_path)
    s.close()
    folder = compiled_case(build, tmp_path / "decoded", model_points=twins)
    found = compiled_mismatches(build, folder, also=_wol_c4_also)
    assert not found, _mismatch_lines(found)


@pytest.mark.cython
def test_the_compiled_model_returns_each_label_as_modelx_does(sec_build, tmp_path):
    """The labels, compiled, are modelx's: their text on every committed and decoded point.

    The five labels are reporting cells, which no projection cell calls, so C4's sweep
    compares them only as cells without parameters; this calls each on every point, in
    modelx and compiled (``uk_sec_support.label_mismatches``), on the committed table and
    on the twins of :data:`DECODED`, which carry every value of every labelled column: each
    must be the same text in both engines, ``mort_basis`` the basis of its point's cell.  A
    label refuses what is not its column's codes, in either engine
    (:func:`test_each_label_refuses_a_value_that_is_not_its_codes`), so each compiles to
    ``str``, which C3 admits of a refusing label.
    """
    build = sec_build(SEC)
    labels = list(LABEL_REFUSALS)
    s, twins = _decoded_twins(tmp_path / "decoded")
    s.close()
    for name, rows in (("committed", None), ("decoded", twins)):
        folder = compiled_case(build, tmp_path / name, model_points=rows)
        want, found = label_mismatches(build, folder, labels)
        assert not found, (name, found)
        values = {label: {v[1] for point in want.values() for lab, v in point.items()
                          if lab == label} for label in labels}
        assert all(isinstance(v, str) for vs in values.values() for v in vs), values
        if name == "decoded":
            assert values["mort_basis"] == {"population", "assured"}, values
            assert values["escalation"] == {"level", "fixed_5pct", "rpi"}, values
            assert values["sex"] == {"M", "F"} and values["smoker"] == {"NS", "S"}, values


# The model point table's columns that hold whole numbers, which a spreadsheet may save as
# floats: the months, the age and the crossover.  And the assumption tables' keys.
FLOAT_COLUMNS = ("duration_mth", "entry_age", "cessation_months", "moratorium_months",
                 "crossover_mth_init")
FLOAT_KEYS = {MORT: lambda t: t.assign(age=t["age"].astype(float)),
              LAPSE: lambda t: t.assign(policy_year=t["policy_year"].astype(float))}


@pytest.mark.cython
def test_the_compiled_model_reads_keys_written_as_floats_as_modelx_does(sec_build,
                                                                         tmp_path):
    """C4 on keys written as floats: the compiled model reads 200.0 as 200, as modelx does.

    The committed table with its labels written ``1.0`` to ``17.0`` and its whole numbers as
    floats (:data:`FLOAT_COLUMNS`), and the two assumption tables' keys as floats
    (:data:`FLOAT_KEYS`).  ``Data`` reads each by value, so first, in seconds, modelx's
    ``Data`` on the floats is held to its ``Data`` on the same rows as written: every array
    of the same dtype and values, and every check of the same type, so that a key read as
    a float fails here, naming its cell, and not in the compiled sweep.  Then modelx sweeps
    every point, and the compiled model must agree everywhere, every ``Data`` array
    included, in dtype and shape.
    """
    build = sec_build(SEC)
    rows = _committed()
    as_written = mx.read_model(_sec_inputs(tmp_path / "ints", rows), name=_name("ints"))
    floats = rows.assign(**{c: rows[c].astype(float) for c in FLOAT_COLUMNS})
    floats.index = pd.Index(rows.index.astype(float), name="point_id")
    folder = compiled_case(build, tmp_path / "floats", model_points=floats,
                           edits=FLOAT_KEYS)
    written = pd.read_csv(folder.parent / TABLE)
    assert all(written[c].dtype == float for c in ("point_id", *FLOAT_COLUMNS))
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
    found = compiled_mismatches(build, folder, also=_wol_c4_also)
    assert not found, _mismatch_lines(found)


@pytest.mark.cython
@pytest.mark.parametrize("refs", list(SPEC.derived_refs.values()),
                         ids=[f"{k}={v}" for refs in SPEC.derived_refs.values()
                              for k, v in refs.items()])
def test_the_compiled_model_computes_what_modelx_computes_under_a_row_s_own_references(
        sec_build, tmp_path, refs):
    """C4 on the committed table under the References each of its own rows was read from.

    Three committed rows were read from S under References of their own (the spec's
    ``derived_refs``): the RPI point at 120 under an RPI of 5%, the underwritten increasing
    point at 120 under a take-up of a half, and the paid-up point at 180 under a stress of
    100, paid-up entirely, its ``policy_count`` 0.  C4 on the committed points compares
    them at the shipped References; under their own, set on the compiled model as on modelx
    before either computes, each continues S's path, which other rows' References leave
    untaken: so the committed rows :data:`OWN_REFS_ROWS` gives each set, every row the RPI
    and the take-up move and four of those the stress moves, and the whole committed table
    with the full grid, are swept fully under it, and the compiled model must agree
    everywhere, the point paid-up entirely and the rows past cessation among them.
    """
    build = sec_build(SEC)
    (ref,) = refs
    folder = compiled_case(build, tmp_path / "own",
                           model_points=_c4_rows(OWN_REFS_ROWS[ref]))
    found = compiled_mismatches(build, folder, refs=refs, also=_wol_c4_also)
    assert not found, _mismatch_lines(found)


# The References under which the anniversary rows' month-0 increase is not the one the
# rows were read with: an RPI of 8% and a take-up of a half.
ANNIVERSARY_REFS = {"rpi_rate": 0.08, "esc_take_up": 0.5}


@pytest.mark.cython
def test_the_compiled_model_computes_what_modelx_computes_on_an_anniversary(sec_build,
                                                                             tmp_path):
    """C4 on the rows valued on an anniversary, whose increase is made at ``t = 0``.

    The owner's decision (D6): an anniversary at the valuation date is the projection's
    first event, made at today's References, the cover and premium columns holding the
    year it closes.  Three committed rows are valued on an anniversary: the underwritten
    increasing point on its first, and the RPI and underwritten increasing points on their
    tenth.  In modelx, under :data:`ANNIVERSARY_REFS`, each steps its cover and its premium
    at ``t = 0``, from its columns, at today's step, which is asserted: ``cover_pp(0)`` is
    ``cover_pp_init()`` times ``1 + esc_cover_step()``, above the column.  Then the three
    rows, the whole committed table with the full grid (:data:`ANNIVERSARY_ROWS`), are swept
    fully under those References, and the compiled model must agree everywhere, the
    month-0 step and every year's after it among it.
    """
    build = sec_build(SEC)
    model = mx.read_model(model_path(SEC), name=_name("anniversary"))
    try:
        for ref, value in ANNIVERSARY_REFS.items():
            setattr(model.Projection, ref, value)
        rows = [_row(model, "derived", 6, 12)]
        table = model.Data.model_point_table()
        rows += [projection(model, key) for key, label in zip(point_keys(model), table.index)
                 if table.at[label, "row_kind"] == "derived"
                 and table.at[label, "source_mth"] == 120]
        assert len(rows) == 3
        for p in rows:
            assert p.duration_mth_init() % 12 == 0 and p.duration_init() == (
                p.duration_mth_init() // 12 - 1)
            step = 1.0 + p.esc_cover_step()
            assert p.cover_pp(0) == p.cover_pp_init() * step > p.cover_pp_init()
            assert p.premium_pp(0) == p.premium_pp_init() * (1.0 + p.esc_prem_step())
    finally:
        model.close()
    folder = compiled_case(build, tmp_path / "anniversary",
                           model_points=_c4_rows(ANNIVERSARY_ROWS))
    found = compiled_mismatches(build, folder, refs=ANNIVERSARY_REFS, also=_wol_c4_also)
    assert not found, _mismatch_lines(found)


# The compiled refusals' child: one process, which imports the compiled package once and
# runs each case on a fresh instance of the model, whose Data reads the case's own copies
# of the three files by absolute path.  A refusal names a file by its Reference, so the
# child's names the path, and the test writes each path as the file's name (_named), as
# modelx, reading the files by name, writes it.  It sets every space's References that a
# case gives, Data's named "Data.<name>" and Projection's by name (UKLIB-SEC-PLAN.md §6.2,
# *Record -- M4*, *Carried into M6 and after*).
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
        if ref.startswith("Data."):
            setattr(model.Data, ref[len("Data."):], value)
        else:
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
CASE_FILES = {"model_point_file": TABLE, "mort_table_file": MORT, "lapse_table_file": LAPSE}


def _named(outcome, files):
    """A compiled outcome with each of a case's ``files``, ``{Reference: absolute path}``,
    written as the file's name in its message, as modelx's ``Data`` names it."""
    if outcome[0] != "raised":
        return outcome
    text = outcome[1]
    for path in files.values():
        text = text.replace(path, pathlib.Path(path).name)
    return ("raised", text)


# The integer References, which the compiled model holds as long long: one set to a value
# that is not a whole number below 2**63 cannot be held compiled at all, and one with a
# fraction is truncated as it is set, 18.5 to 18, where modelx refuses 18.5, so the
# compiled refusals take a domain's cases at whole numbers alone, and model-sec.md says to
# set each as a whole number (UKLIB-SEC-PLAN.md §6.1, *Record -- M2*).
INT_REFERENCES = frozenset({"issue_age_min", "omega_age", "omega_age_max", "suicide_mths"})


def _held_compiled(refs):
    """Whether the compiled model holds every one of ``refs`` as modelx does."""
    return all(math.isfinite(value) and value == value // 1 and abs(value) < 2.0 ** 63
               for ref, value in refs.items() if ref in INT_REFERENCES)


# Data's integer Reference, which the compiled model holds as a long long, as it holds
# Projection's (INT_REFERENCES), and which the child sets as it sets theirs: the horizon
# is refused at -1 and at 2**53 in both engines, message for message, and a fraction is
# truncated as it is set, 12.5 to 12, where modelx refuses 12.5 (the horizon test), so
# that compiled, 12.5 does what 12 does in modelx: it refuses the point issued 13 months
# on.  model-sec.md says to set it as a whole number.
DATA_INT_REFERENCES = frozenset({"future_horizon_mth"})
HORIZONS = (-1, 12.5, 2 ** 53)


def _as_held(ref, value):
    """What the compiled model holds of ``value`` set on Reference ``ref``, ``"Data."``
    before a ``Data`` Reference's name: a fraction set on a ``Data`` integer Reference
    truncated, as a ``long long`` takes it, and any other value as it is."""
    name = ref[len("Data."):] if ref.startswith("Data.") else None
    if name in DATA_INT_REFERENCES and math.isfinite(value) and value % 1:
        return int(value)
    return value


def _set_refs(model, refs):
    """Set each of ``refs`` on ``model`` as the compiled model holds it (:func:`_as_held`):
    ``"Data.<name>"`` on its ``Data``, any other on its ``Projection``."""
    for ref, value in refs.items():
        if ref.startswith("Data."):
            setattr(model.Data, ref[len("Data."):], _as_held(ref, value))
        else:
            setattr(model.Projection, ref, value)


# Projection's idx past the extract's last row, 17, and -1, beside the last row, 16, as
# (position, cell, arguments): past the last row the first read of a vector raises
# IndexError in both engines, each in its own words, and -1 reads every vector at its last
# element in both, so it is the last point, under that point's own point_id.
IDX_CASE = "an idx past the table and one before it"
IDX_EDGES = [(17, "point_id", ()), (17, "result_cf", ()), (-1, "point_id", ()),
             (-1, "proj_len", ()), (-1, "net_cf", (0,)), (16, "point_id", ()),
             (16, "proj_len", ()), (16, "net_cf", (0,))]

# Calls past the caches spec_sec.py sizes, which raise IndexError in the compiled model
# alone, as (call, arguments, what modelx does), on the extract's first row, point 1, the
# anchor cell issued at 70: a month either side of the t cache, which modelx answers with
# 0.0, the month outside cover; a timing, a benefit and a kind past the one inner width,
# which modelx refuses as codes it does not take; and a policy year past the y cache, whose
# opening modelx computes as it computes any year's opening, the value the year before
# closes on: 0.0 here, that year long past the point's cover.
COMPILED_ONLY = [
    ("net_cf", (1358,), ("ok", 0.0)), ("net_cf", (-1,), ("ok", 0.0)),
    ("pols_if_at", (0, 4), ("raised", "ValueError: invalid timing")),
    ("benefit_pp", (0, 4), ("raised", "ValueError: invalid kind")),
    ("claims", (0, 4), ("raised", "ValueError: invalid kind")),
    ("pols_if_py", (104,), ("ok", 0.0)), ("pols_pu_py", (104,), ("ok", 0.0)),
    ("pu_benefit_py", (104,), ("ok", 0.0)), ("prem_cum_pp_py", (104,), ("ok", 0.0)),
]


def _codes_of(args):
    """``args`` with each text that names a code of the model as that code, as ``_code``
    gives it, read from the model's own References."""
    refs = _references("Projection")
    return tuple(refs[a] if isinstance(a, str) else a for a in args)


def _refusal_cases():
    """Every refusal the compiled model must make as modelx does, as (case, the table, the
    edits, the References, [(position, cell, arguments)], the Data cells to read).

    Each table is an extract, labelled otherwise than by position (:data:`EXTRACT_LABELS`,
    the generator's columns kept), so that a refusal naming a point by ``idx + 1`` names
    another; a case that edits the committed table edits it first, by its own labels, and
    is then relabelled.  A position, not a label, since a table ``Data`` refuses has no
    keys to give: each is the row's place in the table written, ``Projection``'s ``idx``,
    which the test indexes ``Projection`` by in modelx too.
    """
    committed = _committed()
    relabel = dict(zip(committed.index, EXTRACT_LABELS))

    def extract(edit=None):
        table = edit(committed) if edit is not None else committed
        return table.rename(index=relabel)

    def at(point):
        return list(committed.index).index(point)

    cases = []
    for case, edit, _ in MALFORMED:
        cases.append((case, extract(edit), None, {}, [(0, "result_cf", ())],
                      ("model_point_table",)))
    for case, file, edit, cell, _ in UNREADABLE:
        array = "mort_table_array" if file == MORT else "lapse_table_array"
        cases.append((case, extract(), {file: edit}, {}, [(at(1), "result_cf", ())],
                      (cell, array)))
    for case, edit, refs, point, _, _ in NOT_ISSUED:
        cases.append((case, extract(edit), None, refs,
                      [(at(point), cell, ()) for cell in ("result_cf", "proj_len")], ()))
    for case, refs, message in DOMAINS:
        if message is not None and _held_compiled(refs):
            cases.append((f"domain {case}", extract(), None, refs,
                          [(at(1), "result_cf", ()), (at(1), "proj_len", ())], ()))
    for case, edit, refs, point, call, report, _ in PAST_THE_FLOATS:
        name, t, *rest = call
        calls = [(at(point), name, _codes_of((t, *rest))), (at(point), report, ())]
        cases.append((f"past the floats: {case}", extract(edit), None, refs, calls, ()))
    cases.append(("past the limiting age", extract(_moved_on(9, 600)), None, {},
                  [(at(9), "result_cf", ()), (at(9), "proj_len", ())], ()))
    cut = {MORT: _dropped(lambda t: t["age"] < 20)}
    cases.append(("an age below the mortality table",
                  extract(_set("entry_age", [5], 18)), cut, {},
                  [(at(5), "result_cf", ()), (at(5), "mort_rate", (0,))], ()))
    cut = {MORT: _dropped(lambda t: t["age"] > 100)}
    cases.append(("an omega_age past a shortened mortality table", extract(), cut, {},
                  [(at(1), "result_cf", ()), (at(1), "proj_len", ())], ()))
    for case, edit, cell, args, _ in NOT_HELD:
        if edit is not None:
            cases.append((case, edit(committed), None, {}, [(8, cell, args)],
                          ("point_id",)))
    for case, edit, refs, point, call in OVERFLOWING_POWERS:
        name, *args = call
        calls = [(at(point), name, tuple(args))]
        if args:
            calls.insert(0, (at(point), name, (args[0] - 1,)))
        cases.append((f"overflow: {case}", extract(edit), None, refs, calls, ()))
    for horizon in HORIZONS:
        cases.append((f"future_horizon_mth at {horizon!r}", extract(), None,
                      {"Data.future_horizon_mth": horizon}, [(at(1), "result_cf", ())],
                      ("model_point_table",)))
    return cases


@pytest.mark.cython
def test_the_compiled_model_refuses_what_modelx_refuses(sec_build, tmp_path):
    """Compiled, the model refuses what modelx refuses, with modelx's error and message.

    A ``ValueError`` raised in a cell typed ``long long`` or ``double`` propagates out of
    the compiled model as out of modelx.  So, each on its own inputs and References
    (:func:`_refusal_cases`), on an extract labelled otherwise than by position: every
    case of :data:`MALFORMED`, refused by a projection and by ``Data``'s reader, the
    ``2**53`` bounds among them; every case of :data:`UNREADABLE`, by a projection, by the
    ``Data`` cell that checks the table and by the table's array, so that a compiled
    ``Data`` cell refuses each value its modelx cell refuses; every case of
    :data:`NOT_ISSUED`, by ``result_cf`` and ``proj_len``; every case of :data:`DOMAINS`
    that refuses and that the compiled model can hold, its integer References whole
    (:func:`_held_compiled`), each printed as the compiled model types it, the contract's
    ``omega_age_max`` among them; each value of :data:`PAST_THE_FLOATS`, by its cell and by
    a report, a kind named by its code; a point past the limiting age; an attained age
    below a mortality table cut at 20, by ``mort_rate`` and a report, and an ``omega_age``
    past one cut at 100, by ``proj_len()``, which no frame then passes; a label the
    vectors cannot hold, by ``Data.point_id``; and ``Data.future_horizon_mth`` at each of
    :data:`HORIZONS`, set by the child as every space's References are, refused by a
    projection and by ``Data``'s reader: at ``-1`` and ``2**53`` as modelx refuses it, and
    at ``12.5``, which the compiled model truncates as it is set, as modelx refuses 12
    (:func:`_as_held`).

    And each power of :data:`OVERFLOWING_POWERS` past the largest float, the month before
    it computing: compiled, the cell calls Python's own power where C's gives an infinity,
    uslib's M22 form, so that it raises the platform's ``OverflowError`` as modelx does,
    where it would carry an infinity on; the cover's, the premium's, the inflation's, the
    improvement's and the crossover search's, each of the search's four guards among them.

    And the refusals that are the compiled model's alone (:data:`COMPILED_ONLY`): a month
    past the ``t`` cache either side, a timing, a benefit and a kind past their codes and a
    policy year past the ``y`` cache on each of the four openings, each raising
    ``IndexError`` compiled, beside what modelx does.  And ``Projection``'s ``idx`` at the
    table's edges (:data:`IDX_EDGES`): one past the last row raises ``IndexError`` in both
    engines, compared by its type, the words being each engine's own, and ``-1`` is the
    last row in both, its every outcome the last row's and modelx's, which a build without
    bounds checks, or without Python's negative indices, would part from.

    The compiled model runs every case in one child, each on a fresh instance of the model
    that reads the case's own copies of the three files by absolute path
    (:data:`REFUSALS_CHILD`), each path in a message written as the file's name, as modelx
    names it (:func:`_named`), and modelx reads each case afresh.
    """
    build = sec_build(SEC)
    cases = _refusal_cases()
    plain = len(cases)
    committed = _committed()
    relabelled = committed.rename(index=dict(zip(committed.index, EXTRACT_LABELS)))
    cases.append(("compiled only", relabelled, None, {},
                  [(0, cell, args) for cell, args, _ in COMPILED_ONLY], ()))
    assert len(relabelled) == 17
    cases.append((IDX_CASE, relabelled, None, {}, IDX_EDGES, ()))
    root = tmp_path / "refused"
    compiled_case(build, root / "base")
    jobs, wants = [], []
    for i, (case, table, edits, refs, calls, data) in enumerate(cases):
        folder = temp_inputs(root / f"case{i:03d}", model_path(SEC), model_points=table,
                             model_point_file=TABLE, edits=edits)
        model = mx.read_model(folder, name=_name("refused"))
        try:
            _set_refs(model, refs)
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
    found, refused, computed, edges = [], 0, 0, {}
    only = iter(COMPILED_ONLY)
    for (case, *_, calls, data), (files, *_), (want, want_data), (have, have_data) in zip(
            cases, jobs, wants, got, strict=True):
        have = [_named(did, files) for did in have]
        have_data = [_named(did, files) for did in have_data]
        for n, ((idx, cell, args), modelx_did, compiled_did) in enumerate(
                zip(calls, want, have, strict=True)):
            where = f"{case}: idx {idx}: {cell}{args}"
            if case == IDX_CASE:
                edges[idx, cell, args] = (modelx_did, compiled_did)
                if idx == 17:
                    for engine, did in (("modelx", modelx_did), ("compiled", compiled_did)):
                        if (did[0], str(did[1]).split(":")[0]) != ("raised", "IndexError"):
                            found.append(f"{where}: {engine} {did}, not IndexError")
                elif compiled_did != modelx_did:
                    found.append(f"{where}: compiled {compiled_did}, modelx {modelx_did}")
                continue
            if case == "compiled only":
                _, _, does = next(only)
                if modelx_did != does:
                    found.append(f"{where}: modelx {modelx_did}, not {does}")
                if (compiled_did[0], str(compiled_did[1]).split(":")[0]) != (
                        "raised", "IndexError"):
                    found.append(f"{where}: compiled {compiled_did}, not IndexError")
                continue
            if case.startswith("overflow: ") and n == 0 and len(calls) == 2:
                computed += 1
                if modelx_did[0] != "ok" or not (
                        compiled_did[0] == "ok" and _as_modelx(compiled_did[1],
                                                               modelx_did[1])):
                    found.append(f"{where}: compiled {compiled_did}, modelx {modelx_did}, "
                                 f"where the month before the overflow computes")
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
        if idx == -1 and outcomes != edges[16, cell, args]:
            found.append(f"{IDX_CASE}: {cell}{args} at idx -1 is {outcomes}, at the last "
                         f"row {edges[16, cell, args]}")
    assert edges[-1, "point_id", ()][0] == ("ok", EXTRACT_LABELS[-1]), edges
    overflows = [w for (case, *_), (w, _) in zip(cases, wants) if case.startswith("overflow")]
    assert len(overflows) == len(OVERFLOWING_POWERS) and all(
        w[-1][1].startswith("OverflowError") for w in overflows), overflows
    assert not found, "\n".join(found[:40])
    assert refused + computed == sum(len(calls) + len(data)
                                     for *_, calls, data in cases[:plain])


def _did(call):
    """``("ok", value)`` or ``("raised", "Type: message")``, as the compiled runner reports
    a call, modelx's ``FormulaError`` unwrapped to the error it carries."""
    try:
        return ("ok", call())
    except Exception as err:            # the outcome compared with the compiled one
        return ("raised", _raised(err))


# The cold call the stack test makes compiled, in a thread whose stack is reserved at each
# of these sizes in KiB, and then on the main thread.  1 MiB is the size asserted; the
# others bracket what the call needs, and the test reports the smallest that ran.
STACK_KIB = (48, 64, 96, 128, 192, 256, 384, 512, 1024, 2048)

# The chain heads the stack test calls cold, each in an ItemSpace of its own, as (cell, the
# code it takes, or None): net_cf and the roll-forward's residual, the deepest calls a
# projection makes, and the paid-up deaths' claims, the deepest call into the paid-up
# chains.  The runner makes one ItemSpace for each key of a job and deletes it after the
# key's calls, so a key with two calls would run the second warm, on the first's caches.
STACK_HEADS = (("net_cf", None), ("check_pols_roll_fwd_resid", None),
               ("claims", "DEATH_PU"))

# How long the stack test waits for each child, in seconds: one runs in a few seconds, more
# under load.  A bracketing size may kill its child on a stack overflow by design, and
# where the overflow hangs instead, as Windows Error Reporting could, the wait ends sooner
# than for the two runs asserted, and the size is recorded as timed out.
BRACKET_TIMEOUT, ASSERTED_TIMEOUT = 120, 300


@pytest.mark.cython
def test_the_longest_cover_runs_cold_on_a_one_megabyte_stack(sec_build, tmp_path):
    """The deepest call the contract allows runs compiled on a 1 MiB stack (F7).

    On the rows of :func:`_longest_cover`, each shape of :data:`CHAIN_SHAPES` at its longest
    cover, issued at 18 now and 120 months on, the limiting age at the contract's largest,
    121, 1,236 months from issue: the anchor cell, the paid-up point, the RPI point and the
    underwritten increasing point.  Each of :data:`STACK_HEADS`, a cold ``net_cf``, a cold
    roll-forward residual and cold paid-up deaths' claims in the last month, runs the
    chains back to ``t_entry()``, one cell a month within the policy year and two a year
    before it, the four chains being blocked by policy year: 226 to 239 cells deep in
    modelx, on a model just read
    (:func:`test_every_chain_runs_one_cell_a_month_from_a_cold_start`), with every switch
    that ships off on (:data:`LONGEST_REFS`).  Each runs in an ItemSpace of its own, on a
    copy of its row, so that each is cold: in one ItemSpace the second would run on the
    first's caches, a few cells deep.  Compiled they run on the C stack, which the
    interpreter's recursion limit does not count, and one cell a month they needed 292 KiB
    of it here (UKLIB-SEC-PLAN.md §6.4, *Record -- M6*).  1 MiB is the stack MSVC gives an
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
    folder, frames = _longest_cover(tmp_path / "rows", tuple(CHAIN_SHAPES))
    rows = pd.read_csv(folder.parent / TABLE, index_col="point_id")
    copies = [rows.set_axis(rows.index + 1000 * i, axis=0) for i in range(len(STACK_HEADS))]
    case = compiled_case(build, tmp_path / "longest", model_points=pd.concat(copies))
    model = mx.read_model(case, name=_name("longest"))
    try:
        for ref, value in LONGEST_REFS.items():
            setattr(model.Projection, ref, value)
        calls, want = {}, {}
        for label, months, entry, _ in frames:
            for i, (head, code) in enumerate(STACK_HEADS):
                key = _key(model, label + 1000 * i)
                proj = projection(model, key)
                assert (proj.proj_len(), proj.t_entry()) == (months, entry), label
                args = (months - 1,) if code is None else (months - 1, _code(proj, code))
                calls[key] = [(head, args)]
                want[key] = [proj.cells[head](*args)]
    finally:
        model.close()
    assert len(calls) == len(frames) * len(STACK_HEADS), "a head shares an ItemSpace"
    assert all(len(each) == 1 for each in calls.values()), "a head runs after another, warm"
    job = {"refs": LONGEST_REFS, "calls": calls}

    def child(timeout, **where):
        try:
            return run_compiled(case.parent, build.package.name, job, timeout=timeout,
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
    record = (f"the compiled cold net_cf, roll-forward residual and paid-up deaths' claims "
              f"at the longest cover, each in an ItemSpace of its own, ran on a thread of "
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
        for key, values in want.items():
            for (status, have), value in zip(got["values"][key], values, strict=True):
                assert status == "ok", (where, got["values"][key])
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
values += [p.expenses(12), early.expenses(12), p[9].expenses(12)]
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
    ``Projection``, the anchor's twin at ``idx`` 0, the anchor cell in force 6 months, made
    before, and the paid-up point in force 200 months, made after, so that a modelx-cython
    that began to clear caches would be seen here, and the advice changed with it.  A
    compiled value meets modelx's as C4 holds it (:func:`_as_modelx`), and one the compiled
    model kept, its own value of before, identically.
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
                 projection(model, 9).expenses(12))
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
    modelx's: point 10's description, the paid-up point in force, and its first twelve rows
    and counts, point 17's, paid-up entirely, and the block's lines for each point, its
    first twelve rows and its first twelve projection years.

    The same output is what a runner that ignored ``--build`` and ran modelx would print,
    so the runner is also given a directory that holds no build, and must refuse it,
    saying so, rather than print anything.
    """
    build = sec_build(SEC)
    runner = model_path(SEC).parent / "run_sec.py"
    for args in (("10",), ("17",), ("--block",)):
        expected = _run_sec(runner, *args)
        assert _run_sec(runner, *args, "--cython", "--build", str(build.out)) == expected
    empty = tmp_path / "no_build"
    empty.mkdir()
    done = _run_sec(runner, "10", "--build", str(empty), check=False)
    stderr = done.stderr.decode(errors="replace")
    assert done.returncode != 0 and done.stdout == b"", stderr
    assert f"holds no build of {SEC} for this interpreter" in stderr, stderr
