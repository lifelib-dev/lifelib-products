"""Tests for IP_UK_SEC: the splice, future business, counts, regeneration, compiled.

``IP_UK_SEC`` is ``IP_UK_S`` taught to run in force at a valuation date
(UKLIB-SEC-PLAN.md, milestone M7, after USLIB-SEC-PLAN.md's Phase 1), and then made to
compile under modelx-cython (milestone M8, after USLIB-SEC-PLAN.md's Phase 2), its claim
cohorts, a tuple a month in ``IP_UK_S``, a recursion of two parameters, a cohort a cell.
It runs on two clocks: ``t`` counts months from the valuation date, the same month for
every model point,
and ``duration_mth(t)`` counts the months the policy has been in force,
``duration_mth_init() + t``; and on the claim duration ``z``, a cohort index the
termination rates read.  A model point may be a policy already in force at the valuation
date, in any month of its policy year, one issued at it, or one to be issued after it, as
in ``basiclife/BasicTerm_SE``.  A policy in force opens with its count, the lives in health
and in claim together, and with three columns of state beside it and a vector of claim
cohorts, each measured at the valuation instant, before month 0's events, recoveries
already returned to health: the healthy share of the count, the share in claim at each
claim duration, read from a sparse companion, ``inforce_cohorts_sec.csv``, and the benefit
and premium entering month 0.

The worked example is not restated here.  On a point issued at the valuation date the two
clocks coincide and the model is ``IP_UK_S``, and ``test_model_conventions_uk.py`` asserts
that cell by cell on the twins of S's four new-business points (T1), so every golden of
``test_income_protection_uk.py`` on them holds on this model with no number copied.  The
twins of S's three claims in payment, the claims-in-payment worked example among them, are
on policy clocks of whole years since issue, ``duration_mth = 12n``, and are splice cases,
which this module compares with S cell by cell.  The conventions also hold the SEC family's
other rules: every frame opens at ``t = 0``, ``pols_if`` is the ``BEF_DECR`` count,
``BEF_DECR`` is ``BEF_NB`` plus the month's new business, new business enters once, and
nothing happens before issue.  This module holds the rest of the plan's tests (its §5) and
the product's own facts:

* T2, the splice: an S point restated in force at month ``d``, opened with the state S
  carries into ``d``, its claim cohorts among it, continues S's projection from ``d`` on,
  in every cell of S's, the cohort vector included, and in its reports.  The months
  straddle the product's events: the anniversaries, the lapse table's last year, the
  inception table's pivot ages, the claim-duration years, the first month and the last two.
  Every assumption that ships idle is on, under four sets of References: the escalation
  lapse shock at an RPI of 5%, beside the cycle overlay, the active-life mortality factor,
  the amount-payable ratio and the claim severity, each moved off its neutral 1 and off
  each other; the escalation cap at 12%; the RPI's floor at -2%; and the recovery rate's
  bound at an overlay of 0.35.  Three variants of S's points, in a copy of S's table, add
  an active cell on the exit basis, the youngest entry ages below the inception table's
  first pivot, and the oldest entry age to the latest expiry, past its last.  The twins of
  S's two claims on the exit basis are splice cases, on their policy clocks; the claim on
  the active-lives basis, whose recovered lives S lapses on its clock restarted at the
  valuation date, a year behind the clock its twin is given, is spliced under a flat lapse
  table by a test of its own; and so is the inception rate's floor at 0, on a schedule in a
  copy of the inception table that falls below 0 above the youngest issue age.
* T3, future new business: a point issued ``k`` months after the valuation date is S's
  projection ``k`` months on, with zeros before issue and no table read there.
* D11's R1 and R2, and D3's and D5's chains: on the splice's grid no cell is called at a
  negative month, none on the books reads a month before them, and none reads beyond
  ``t + 1``; on the committed points no recursion runs backward over the frame; the policy
  clock is a closed form; each chain, called cold, runs one cell a month back to
  ``t_entry()``, the cohorts' down their diagonal, at the contract's longest cover, on
  each shape, each head within its own measured overhead; and no cell a chain recurses
  through builds text.
* T4, the count algebra: the counts roll forward through new business, the transitions
  between the states and the exits, ``result_pols`` holds S's counts with the new business
  beside them, multiplying ``policy_count`` by 2.5 with every assumption that ships idle
  switched on multiplies every flow and every counted cell, the cohort vector's every
  element among them, by 2.5 and moves no per-policy value, a point restated a month on
  continues its own flows, and the roll-forward and the population identity, whose
  tolerances scale with the policies on the books, close on ten million policies.
* T5, validation: each malformed row of the table and of the companion is refused as it is
  read, naming its point or its line, by its label on an extract labelled otherwise; each
  assumption table, malformed or holding a value that is not a number in its range, is
  refused before a value of it is read, naming its lines; the future horizon is a
  Reference that bounds future business; a point past its policy end date, one the
  contract does not issue, one whose escalation history the contract cannot have and one
  that reads a Reference off its domain are refused by the frame, each domain at both its
  edges, NaN and the infinities included, and each bound of the history a cent outside
  and accepted half a cent inside; a value past the floats is refused in the cell where it
  first is; the edges of the interface are accepted, the shares' tolerance pinned from
  both sides; and so is every state ``IP_UK_S`` reaches, on each set of inputs on which
  those states differ.
* T6, regeneration: the committed ``model_point_table_sec.csv`` and
  ``inforce_cohorts_sec.csv`` are what the generator makes of ``IP_UK_S`` and its table as
  they stand.
* Then the product's own facts: the two clocks on the shipped points; the twins of S's
  claims on their policy clocks, and the claim on the active-lives basis under a flat
  lapse table, where the table is not flat its twin's clock running a year ahead of S's
  restarted one; the committed rows
  continuing their S points, those read under an RPI of their own continuing S under it;
  each history column read rather than recomputed (UKLIB-SEC-PLAN.md K14), the healthy
  share, the claim cohorts, the benefit and the premium; an anniversary at the valuation
  date as the projection's first event; the cumulative counts restarting on the books; the
  present value and the annuity factor on the valuation clock; expense inflation on it; the
  escalation's floor, cap and lapse shock; the caps on mortality and inception and the
  lapse rate's bound; a NaN that reaches a bound and a check whose residual is NaN; the
  values outside cover; the block; an in-force extract; the runner; the cells' defaulted
  parameters; the static check the C step made; the docstrings; the shared input tables;
  and what the default grid reaches.
* The C step's representation, in modelx: the claims total held to ``IP_UK_S``'s by its
  bits; the cohorts' sums held to ``IP_UK_S``'s ``sum`` by theirs and by their order, the
  cohorts past the live ones zero, their bits ``sum``'s where it compensates, as from
  Python 3.12: Python 3.11's ``sum`` adds left to right, and there ``IP_UK_S``'s sums, and
  its claims, part from these in their last bits, so those bits skip, naming 3.11, and
  the rest is held;
  every schedule at every age of the inception and mortality arrays, on the shipped
  inception table and on the floor's; every decode on every value, the escalation flag
  read by its text alone; the padded arrays; the vectors' dtypes; the parameterless cells'
  Python numbers; the labels' refusals; the spec's and the sample's comments; the
  runner's rebuild; and what the vectors cannot hold.
* C2, the fingerprint: every committed point computes what the model computed when its E
  step ended, frozen at the end of this module before its C step changed anything
  (USLIB-SEC-PLAN.md §5.4).
* Compiled, after the fingerprint, the tests marked ``cython``: C4 on the splice grid, at
  the contract's extremes, where each cap, floor and bound binds, on every schedule, on
  keys written as floats, on every committed row with the codes and claim durations no
  swept cell reads, under the References its own rows were read from and on the rows
  valued on an anniversary, in chunks sized by their frames; the labels; the refusals and
  overflows, message for message; each shape's deepest cold call on a 1 MiB stack; a
  Reference set late; and the runner.

SEC month ``t`` is S month ``t + source_mth`` throughout, the direction in which
``uk_sec_support`` takes its ``t_offset``: ``d`` for a point restated at S month ``d``,
``-k`` for one issued ``k`` months on, and 0 for the twin of an S claim in payment, which S
opens at the valuation date.

**The core grid and the full one** (UKLIB-SEC-PLAN.md U6).  T2 and T3 over every S point
at every month, under every set, run by default on a core, chosen so that between them they
reach every branch, every opening-state column, every kind of valuation month and both
sides of every ``min`` and ``max`` the full grid reaches, which
``test_the_core_grid_reaches_every_branch`` asserts.  The other cases, and the rules
test's scan of their rows, carry the ``sec_full`` marker and are skipped, with the reason
shown, unless ``UKLIB_SEC_FULL=1`` is set.  So do the slower tests' other cases
(``GRIDS``): over the committed points, the default run takes five among which every flow
and counted cell is nonzero (``CORE_POINTS``), and the full grid the rest; the cold
chains run on one shape by default and on the other three with the full grid; and so on,
each test's docstring saying which.  A compile test is never skipped, since a skip fails
the cython_uk job: those that compare committed rows under References of their own
compare by default the rows each set moves or binds on (``_c4_rows``), and the whole
table with the full grid.  They are never dropped: one leg of the CI matrix sets
it, and ``UKLIB_SEC_FULL=1 python -m pytest -m sec_full
lifelib/libraries/uklib/tests/test_income_protection_uk_sec.py`` runs them alone.  Each
splice row is released once it has been read (``_release``), as ``run_sec.py --block``
releases its points.

Every test keeps four rules.  Each model is read under a name of its own and closed:
``conftest.income_protection`` reads S under its default name, and reading a model under a
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
through the same helpers, unchanged; a call that spells a timing as text is ``IP_UK_S``'s.
"""
import ast
import dataclasses
import gc
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
from uk_sec_support import _IP_CODED, _ip_c4_also
from uk_sec_support import generated_columns

SEC, TWIN = "IP_UK_SEC", "IP_UK_S"
TABLE, COHORTS = "model_point_table_sec.csv", "inforce_cohorts_sec.csv"
SPEC = SEC_SPECS[SEC]

# S's seven points: the active-lives anchor cell, a 35-year-old man, occupation class 1, a
# 26-week deferred period, £2,000 a month to 65 with RPI escalation (1); the
# claims-in-payment worked example, the same cell level and in claim from duration 0, on
# the exit basis (2); the level-cover anchor cell (3); a 42-year-old woman, class 3, 13
# weeks, £1,500 a month to 60 with RPI escalation (4); a claim at duration 30 months at 50,
# to 65, on the exit basis (5); a 55-year-old man, class 2, 52 weeks, £3,000 a month to 65
# with RPI escalation (6); and the worked example's claim on the active-lives basis, its
# recovered lives back in health (7).
S_POINTS = (1, 2, 3, 4, 5, 6, 7)
NEW_BUSINESS = (1, 3, 4, 6)
IN_CLAIM = (2, 5, 7)

# T2's months (UKLIB-SEC-PLAN.md §6.3).  On the new-business points: the second month; 11 to
# 13 about the first anniversary, where the benefit and the premium first escalate and the
# lapse table moves to its second year; 59 to 61 about the lapse table's last year, policy
# year 6; on the anchor cell the inception table's pivot ages, 40 at 60, 45 at 120, 50 at
# 180, 55 at 240, 60 at 300 and its last pivot, 64, at 348, past which it extrapolates;
# on the female cell 45 at 36, 50 at 96 and 55 at 156; on the older male cell its last
# pivot at 108; and the last two months of each frame.  On the claims on the exit basis the
# claim-duration years the termination table changes at: the claim from duration 0 at 11
# to 13, 23 to 25 and 47 to 49, about the starts of its years 2, 3 and 5, the last row; and
# the claim from duration 30 at 5 and 6 and 17 and 18, about the starts of its years 4 and
# 5; and the first and last months of each.
SPLICE_MTHS = {
    1: (1, 11, 12, 13, 59, 60, 61, 120, 180, 240, 300, 348, 358, 359),
    2: (1, 11, 12, 13, 23, 24, 25, 47, 48, 49, 358, 359),
    3: (1, 11, 12, 13, 59, 60, 61, 358, 359),
    4: (1, 11, 12, 13, 36, 59, 60, 61, 96, 156, 214, 215),
    5: (1, 5, 6, 17, 18, 178, 179),
    6: (1, 11, 12, 13, 59, 60, 61, 108, 118, 119),
}

# T3's months: issued one month on, which puts the policy anniversaries a month off the
# valuation years; twelve, which puts them back on; and the horizon, 120, the latest the
# table admits.  Each variant is issued 13 months on, more than a year after the valuation
# date and off its anniversaries (USLIB-SEC-PLAN.md §7.1, *Record — M14*, *Splice grid*).
FUTURE_MTHS = (1, 12, 120)

# Three more S points, in the splice's copy of S's table and never in the committed one,
# each one of S's points changed so as to reach what S's own points cannot:
#
# 8, S point 1 on the exit basis: an active cell whose recovered lives leave the model,
#   S's exit basis on lives that started healthy;
# 9, S point 3 at 22, to 55, occupation class 4 and a 4-week deferred period: the youngest
#   attained ages, below the inception table's first pivot, 30, from which it
#   extrapolates, a class and a deferred period no S point holds, and the expiry age 55;
# 10, S point 4 as a man of 59, occupation class 2 and an 8-week deferred period, to 70:
#   the latest entry age the product issues at, the latest expiry, attained ages past the
#   inception table's last pivot, 64, and the mortality table read to 69.
#
# Each variant is (the S point it changes, the columns it changes); the policy_id keeps
# the generated ids apart.
VARIANTS = {
    8: (1, {"policy_id": "IP-900008", "recovery_basis": "exit"}),
    9: (3, {"policy_id": "IP-900009", "occ_class": 4, "deferred_weeks": 4, "entry_age": 22,
            "expiry_age": 55}),
    10: (4, {"policy_id": "IP-900010", "sex": "M", "occ_class": 2, "deferred_weeks": 8,
             "entry_age": 59, "expiry_age": 70}),
}
VARIANT_MTHS = {8: (12, 60, 120), 9: (1, 12, 95, 96, 395), 10: (1, 11, 12, 13, 60, 131)}
LATE_FUTURES = tuple((p, 13) for p in VARIANTS)


def _s_table():
    """S's committed table, indexed by point_id."""
    return pd.read_csv(model_path(TWIN).parent / "model_point_table.csv",
                       index_col="point_id")


def _s_table_with_variants(points=None):
    """S's committed table with the :data:`VARIANTS` appended, under their own point_ids;
    or, given ``points``, those of them alone."""
    table = _s_table()
    rows = []
    for point_id, (base, changes) in VARIANTS.items():
        row = table.loc[[base]].assign(**changes)
        row.index = pd.Index([point_id], name="point_id")
        rows.append(row)
    table = pd.concat([table, *rows])
    return table if points is None else table.loc[list(points)]


# The months from issue to the policy end date of each S point and variant, 12 times the
# years from its entry age to its expiry age; S's frames, but on its claims, which S opens
# at the valuation date with the clock restarted.
COVER = {p: 12 * (int(row["expiry_age"]) - int(row["entry_age"]))
         for p, row in _s_table_with_variants().iterrows()}

# The committed rows the generator reads from S under References of their own (the spec's
# derived_refs), by (S policy, month), with those References.
UNDER_REFS = {(_s_table().at[p, "policy_id"], d): refs
              for (p, d), refs in SPEC.derived_refs.items()}

# The sets of References T2 and T3 run under, each set in S and SEC alike before either
# evaluates anything.  Every set holds the valuation clock's one input at 0: expense
# inflation, which S runs from its frame's start and SEC from the valuation date, so at the
# shipped 3% the expenses of a point opened at d differ by the inflation of the policy years
# before d, by design, and at 0 both factors are 1; the clock is asserted on its own, at
# the shipped rate.  Discounting is no cash flow, and its clock has a test of its own.
# Every assumption that ships idle is on in the main set: the escalation lapse shock, which
# the shipped RPI of 3% leaves at 1, at an RPI of 5%, where premiums grow 7.5% a year, past
# the threshold of 5%; and the four factors that ship at a neutral 1, each moved off it and
# off each other, so that a formula that read one for another would part from S: the cycle
# overlay on inception and recovery at 1.25, the active-life mortality factor at 1.1, the
# amount-payable ratio at 0.9 and the claim severity at 0.95.  The RPI is a flat Reference,
# the same on either clock.  Three more sets each reach a bound the main one does not: the
# escalation cap at an RPI of 12%, the RPI's floor at -2%, and the recovery rate's bound at
# an overlay of 0.35, under which the first claim-duration year's recovery rate, 0.4 /
# 0.35, binds at 1.
MAIN = {"inflation_rate": 0.0, "rpi_rate": 0.05, "cycle_factor": 1.25,
        "mort_active_factor": 1.1, "ap_ratio": 0.9, "claim_severity": 0.95}
SPLICE_SETS = {
    "main": MAIN,
    "rpi_cap": {**MAIN, "rpi_rate": 0.12},
    "rpi_floor": {**MAIN, "rpi_rate": -0.02},
    "recovery": {**MAIN, "cycle_factor": 0.35},
}

# The cases of the three sets beyond the main one, each with the points it holds: the RPI
# points about their first anniversary and later, under the cap and the floor, and under the
# recovery bound the anchor cell, whose claims of the first year all recover in the month,
# on the active-lives basis and on the exit basis.
SET_MTHS = {
    "rpi_cap": {1: (11, 12, 13, 60), 4: (12, 13), 6: (12, 61)},
    "rpi_floor": {1: (12, 13), 4: (12,), 6: (60,)},
    "recovery": {1: (12, 60), 8: (60,)},
}
SET_FUTURES = {"rpi_cap": ((1, 1), (4, 13)), "rpi_floor": ((1, 1),), "recovery": ()}

# T2's cases, as (set, row_kind, S point, source_mth): each S point restated in force at
# each of its months, each variant at its own, and the other sets' cases; the twins of S's
# two claims on the exit basis, which S opens in force at the valuation date.  T3's cases,
# as (set, S point, k).
SPLICES = (tuple(("main", "derived", p, d) for p, mths in SPLICE_MTHS.items() for d in mths)
           + tuple(("main", "derived", p, d) for p, mths in VARIANT_MTHS.items()
                   for d in mths)
           + tuple((rates, "derived", p, d) for rates, points in SET_MTHS.items()
                   for p, mths in points.items() for d in mths))
IN_FORCE_TWINS = (("main", "twin", 2, 0), ("main", "twin", 5, 0))
FUTURES = (tuple(("main", p, k) for p in NEW_BUSINESS for k in FUTURE_MTHS)
           + tuple(("main", p, k) for p, k in LATE_FUTURES)
           + tuple((rates, p, k) for rates, cases in SET_FUTURES.items() for p, k in cases))

# The default run's cases (the module docstring), each with what it is there for.  The rest
# of SPLICES, IN_FORCE_TWINS and FUTURES run with UKLIB_SEC_FULL=1.
CORE_SPLICES = {
    ("main", "derived", 1, 12): "the anchor cell on its first anniversary, escalating at 0",
    ("main", "derived", 1, 13): "the anchor cell a month past its first anniversary",
    ("main", "derived", 1, 60): "the anchor cell in the lapse table's last year, at a pivot",
    ("main", "derived", 1, 348): "the anchor cell at its last pivot, cohorts 348 long",
    ("main", "derived", 1, 359): "the anchor cell in its last month",
    ("main", "derived", 2, 12): "the claim from duration 0 in its second claim year",
    ("main", "derived", 2, 48): "the claim from duration 0 in the termination's last row",
    ("main", "derived", 3, 1): "the level cell a month after issue, one cohort",
    ("main", "derived", 3, 61): "the level cell past the lapse table's last year",
    ("main", "derived", 4, 11): "the female cell in the month before its anniversary",
    ("main", "derived", 4, 215): "the female cell in its last month",
    ("main", "derived", 5, 6): "the claim from duration 30 in its fourth claim year",
    ("main", "derived", 5, 18): "the claim from duration 30 in its fifth",
    ("main", "derived", 6, 108): "the older male cell at its last pivot",
    ("main", "derived", 6, 118): "the older male cell in its last two months",
    ("main", "derived", 8, 60): "an active cell on the exit basis, its recoveries leaving",
    ("main", "derived", 9, 95): "the youngest cell below the first pivot, then at it",
    ("main", "derived", 10, 60): "the oldest cell past the last pivot",
    ("main", "twin", 2, 0): "the claims-in-payment worked example on its policy clock",
    ("main", "twin", 5, 0): "the claim from duration 30 on its policy clock",
    ("rpi_cap", "derived", 1, 12): "the escalation cap at the valuation anniversary",
    ("rpi_cap", "derived", 4, 13): "the escalation cap a month past an anniversary",
    ("rpi_floor", "derived", 1, 12): "the RPI's floor at the valuation anniversary",
    ("recovery", "derived", 1, 12): "the recovery rate's bound, on the active-lives basis",
    ("recovery", "derived", 8, 60): "the recovery rate's bound, on the exit basis",
}
CORE_FUTURES = {
    ("main", 1, 1): "issued a month off the valuation anniversaries",
    ("main", 3, 12): "the level cell a year on",
    ("main", 4, 120): "the female cell at the horizon",
    ("main", 8, 13): "the exit basis, more than a year on",
    ("rpi_cap", 4, 13): "the escalation cap, more than a year on",
}

SEC_FULL = os.environ.get("UKLIB_SEC_FULL") == "1"
FULL_ONLY = (pytest.mark.sec_full,
             pytest.mark.skipif(not SEC_FULL, reason="the full splice grid runs with "
                                "UKLIB_SEC_FULL=1 (UKLIB-SEC-PLAN.md U6)"))

# The tests that run over every committed point run the core's by default and the rest on
# the full grid (GRIDS): the anchor cell's twin, the anchor cell in force at 60, the claim
# on the exit basis at 24, the claim on the active-lives basis at 12 and the female cell
# issued 13 months on, by label, among which every flow and every counted cell is nonzero.
CORE_POINTS = (1, 9, 11, 13, 17)
GRIDS = [pytest.param("core", id="core"), pytest.param("full", id="full", marks=FULL_ONLY)]


def _on_grid(grid, label):
    """Whether committed point ``label`` is one the ``grid`` case of a test runs on."""
    return (label in CORE_POINTS) == (grid == "core")


# The cells T2 and T3 skip beyond T1's: the spec's exempt, proj_len, and the three
# cumulative counts.  proj_len counts from the valuation date on SEC and from issue on S,
# so it differs by d, or by -k, by design; frame_mismatches asserts what it must get right,
# that both frames end at the same instant.  The cumulative counts restart at t_entry() on
# SEC, on the count on the books, where S counts from its frame's start: the splice
# compares their increments instead (_cumulative_faults).
CUMULATIVE = ("pols_dead_cum", "pols_lapse_cum", "pols_exit_cum")
SPLICE_EXEMPT = TWIN_EXEMPT_DEFAULT | SPEC.exempt | {"proj_len", *CUMULATIVE}
FUTURE_EXEMPT = SPLICE_EXEMPT

# What else differs on a row of an S claim, which S opens with its policy clock restarted
# at the valuation date and the SEC twin n whole years after issue: the issue age, n years
# less; the policy clock, 12n months on, and so the policy year, which the lapse rates
# read, the healthy lives on the exit basis being none, so that no lapse is weighted by
# them; and the cohort vector and its rates, as long as the cover from issue, 12n longer
# than S's.  _clock_faults holds the clock to S's plus 12n and the attained age to S's,
# and _cohort_faults the cohorts and their rates to S's, the rest zeros; result_states is
# compared frame by frame, without its lapse_rate column.  The claim on the active-lives
# basis has a test of its own.  S's two tuple cells, sick_cohorts and claim_rate_vectors,
# are the spec's exemptions on every row (SPLICE_EXEMPT): this model carries their
# elements in cells of their own, which _cohort_faults holds to S's on every row.
IN_CLAIM_CELLS = frozenset({"age_at_entry", "duration", "duration_mth", "policy_year",
                            "lapse_rate_base", "lapse_rate", "lapse_rate_mth", "max_dur",
                            "result_states"})

# The result_cf columns that expense inflation moves, and the cells they are made of: on
# the committed points, at the shipped 3%, the only places an in-force row's flows depart
# from S.
INFLATED = ("expenses", "net_cf")
INFLATION_CELLS = frozenset({"inflation_factor", "expenses", "net_cf", "result_cf"})

# The discount factor and the two values it makes, which discount to each model's own
# start, S's frame's and the valuation date here (D7): on a row S does not open at the
# valuation date they differ by design, and the present value test holds them.  No report
# shows them, so a comparison meets them only where S has evaluated them.
DISCOUNT_CELLS = frozenset({"disc_factor", "pv_benefits", "annuity_dis"})

# The S cells whose exact value is 0 and whose computed value is rounding about it, the
# roll-forward's residual and the population identity's: a comparison with S holds them at
# the harness's absolute floor of 1e-9, and every other cell at none (_compare).
RESIDUALS = frozenset({"check_pols_roll_fwd_resid", "check_states_resid"})

# The reads keyed by an attained age or a policy year, and the monthly rates, none of which
# may be evaluated before issue (R1, D4).  The annual rates, inception_rate, mort_rate and
# lapse_rate, are columns of result_states, as in IP_UK_S, so the report evaluates them in
# every month of the frame, and before issue each is 0.0 without a read (OUTSIDE_COVER):
# the reads under them are what T3 holds.
KEYED_READS = ("age", "duration", "policy_year", "lapse_rate_base", "mort_rate_mth",
               "lapse_rate_mth", "inception_rate_mth")

# The cells that scale with the counts.  Every other cell is a per-policy amount, a share,
# a rate, a factor, a clock or a flag, and must not move when the counts do.
COUNTED = frozenset({
    "policy_count", "pols_if_init", "pols_if", "pols_if_at", "pols_new_biz", "pols_active",
    "pols_sick", "pols_sick_dur", "pols_sick_surv", "pols_recovery",
    "pols_death_sick", "pols_exit", "pols_death_active", "pols_lapse", "pols_inception",
    "pols_maturity", "pols_dead_cum", "pols_lapse_cum", "pols_exit_cum", "premiums",
    "claims", "expenses", "net_cf", "pv_benefits", "check_pols_roll_fwd_resid",
    "check_states_resid", "result_cf", "result_states", "result_pols"})

# result_pols' columns, in its order: the count in force, the new business within it, the
# healthy and the sick counts, then the month's movements in the notes' processing order,
# out of H the deaths, the lapses and the inceptions, out of S the recoveries and the deaths,
# the recoveries leaving the model and the expiry; then the amounts per policy, which no
# count moves.
RESULT_POLS = ["pols_if", "pols_new_biz", "pols_active", "pols_sick", "pols_death_active",
               "pols_lapse", "pols_inception", "pols_recovery", "pols_death_sick",
               "pols_exit", "pols_maturity", "benefit_pp", "premium_pp"]
COUNTS_POLS = RESULT_POLS[:11]
PER_POLICY_POLS = RESULT_POLS[11:]

# S's two timings and BEF_NB, the one running in force adds; and the kinds.
TIMINGS = ("BEF_NB", "BEF_DECR", "AFT_DECR")
KINDS = ("BENEFIT", "DEATH", "LAPSE")

# The recovery bases, each by the code the C step gives it; and every code the model names,
# each an int Reference at stage "EC", the claims total among them.
RECOVERY_CODES = ("RETURN_TO_H", "EXIT")
CODE_NAMES = frozenset({*TIMINGS, *KINDS, "ALL", *RECOVERY_CODES})

# What each cell holds outside cover, before issue and from the month cover has ended, as
# its docstring says: no count, so no cash flow; no benefit or premium; no rate read at a
# policy year or an age the policy does not have.  The type is part of the value: a count
# is a float in every branch, because the C step types a cell by the values it returns
# (USLIB-SEC-PLAN.md F3).  The guard test also calls pols_if_at at each timing and claims
# at each kind, all 0.0, and the cohort vector, all zeros.
OUTSIDE_COVER = {
    "is_active": False, "benefit_pp": 0.0, "premium_pp": 0.0, "amount_payable_pp": 0.0,
    "inception_rate": 0.0, "mort_rate": 0.0, "lapse_rate_base": 0.0, "lapse_rate": 0.0,
    "pols_active": 0.0, "pols_sick": 0.0, "pols_if": 0.0, "pols_new_biz": 0.0,
    "pols_sick_surv": 0.0, "pols_recovery": 0.0, "pols_death_sick": 0.0, "pols_exit": 0.0,
    "pols_death_active": 0.0, "pols_lapse": 0.0, "pols_inception": 0.0,
    "pols_maturity": 0.0, "pols_dead_cum": 0.0, "pols_lapse_cum": 0.0,
    "pols_exit_cum": 0.0, "premiums": 0.0, "expenses": 0.0, "net_cf": 0.0,
    "check_pols_roll_fwd_resid": 0.0, "check_states_resid": 0.0, "claim_dur_live": 0}

# The cells a month outside cover may not reach: the clocks of the contract and the
# monthly rates, each keyed by a policy year or an attained age.  The reads that guard
# themselves are held by their values in OUTSIDE_COVER instead.
IN_COVER_ONLY = ("age", "duration", "policy_year", "mort_rate_mth", "lapse_rate_mth",
                 "inception_rate_mth")

# The opening state, in the table's order, and the cells running in force adds to
# IP_UK_S's, each of which the symbol map must name.
STATE = ("pols_active_init", "benefit_pp_init", "premium_pp_init")

# IP_UK_S's columns the projection reads, each of which Data requires; status, IP_UK_S's
# label, which no formula reads, is not among them.
S_COLUMNS_READ = ("entry_age", "sex", "occ_class", "benefit_mth", "earnings_annual",
                  "deferred_weeks", "expiry_age", "escalation", "premium_mth",
                  "premium_basis", "recovery_basis")
NEW_CELLS = ("policy_count", "duration_mth_init", "duration_init", "t_entry", "is_active",
             "expiry_mth", "pols_new_biz", "pols_sick_dur_init", "result_pols", *STATE,
             "point_id", "inception_schedule", "mort_schedule", "is_escalating",
             "recovery_code", "claim_dur_init", "claim_dur_live")

INFLATION = 0.03        # the shipped inflation_rate, which the inflation test reads

# The recursion limit, as mx.set_recursion takes it, under which the committed points are
# first swept (R2, F7).  A report evaluates each column in ascending t, so a forward
# recursion, through t - 1, finds the month before already cached: the committed points'
# sweep passes under a limit far below it (measured at M7).  A backward recursion over the
# frame, through t + 1, opens a chain as long as the frame, and the committed frames run to
# 360 months.
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


def _committed_cohorts():
    """The committed claim cohorts as the file holds them, unvalidated, a plain table."""
    return pd.read_csv(model_path(SEC).parent / COHORTS)


def _sec_inputs(tmp_path, table, cohorts=None, edits=None):
    """A copy of the product directory whose SEC table is ``table``, and whose claim
    cohorts are ``cohorts`` (the committed ones where ``None``), other inputs changed by
    ``edits``, as :func:`uk_sec_support.temp_inputs` takes them; its SEC folder."""
    edits = dict(edits or {})
    if cohorts is not None:
        edits[COHORTS] = cohorts
    return temp_inputs(tmp_path, model_path(SEC), model_points=table,
                       model_point_file=TABLE, edits=edits)


def _read_edited(tmp_path, edit, cohorts_edit=None, edits=None):
    """IP_UK_SEC read from a copy whose SEC table is ``edit(_committed())`` and whose
    claim cohorts are ``cohorts_edit(_committed_cohorts())``."""
    cohorts = None if cohorts_edit is None else cohorts_edit(_committed_cohorts())
    folder = _sec_inputs(tmp_path, edit(_committed()), cohorts, edits)
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


def _extract_inputs(tmp_path, edit=None, cohorts_edit=None, edits=None):
    """A copy whose table is an extract: the committed table, ``edit`` made first by its
    own labels, then labelled :data:`EXTRACT_LABELS`, the generator's columns kept; and
    whose claim cohorts, ``cohorts_edit`` made first, are relabelled alike.  So a refusal
    that named a point by its place, ``idx + 1``, names another.  Its SEC folder."""
    relabel = _relabel_map()
    table = (edit or (lambda t: t))(_committed()).rename(index=relabel)
    held = (cohorts_edit or (lambda t: t))(_committed_cohorts())
    held = held.assign(point_id=[relabel.get(p, p) for p in held["point_id"]])
    return _sec_inputs(tmp_path, table, held, edits)


def _read_extract(tmp_path, edit=None, cohorts_edit=None, edits=None):
    """IP_UK_SEC read from an extract (:func:`_extract_inputs`)."""
    return mx.read_model(_extract_inputs(tmp_path, edit, cohorts_edit, edits),
                         name=_name("extract"))


def _as_extract(message):
    """``message``, each ``point_id N:`` in it the committed label N's extract label."""
    relabel = _relabel_map()
    return re.sub(r"point_id (\d+):", lambda m: f"point_id {relabel[int(m.group(1))]}:",
                  message)


def _refused_naming(call, message, label):
    """``call()`` refuses with ``message`` (:func:`_refused`), and its error begins by
    naming the point, ``ValueError: point_id <label>:``, the extract's label."""
    with pytest.raises(Exception) as excinfo:
        call()
    text = str(excinfo.value)
    assert "ValueError" in text and message in text, text
    assert _raised(excinfo.value).startswith(f"ValueError: point_id {label}: "), text


def _raised(err):
    """The line that names an error: modelx's ``FormulaError`` puts it second."""
    lines = [line for line in str(err).splitlines() if line.strip()]
    if type(err).__name__ == "FormulaError" and len(lines) > 1:
        return lines[1]
    return f"{type(err).__name__}: {lines[0] if lines else ''}"


def _sweep_s(proj):
    """Evaluate on an S point what the splice compares: the sweep, and cells more.

    :func:`uk_sec_support.sweep` reaches ``IP_UK_S``'s ``pols_if_at`` at none of its
    timings, since S's roll-forward reads ``pols_if(t + 1)``; nor ``duration_mth``, which no
    S formula reads; nor the survival step of each claim duration, which no report reads,
    nor ``premium_basis``, which no formula calls.  A cell S never evaluates is compared
    nowhere, so they are evaluated here, over the frame and the cohort vector, and the
    splice and the future comparison see them too.  The present value and the annuity
    factor discount from each model's own start, and a test of their own compares them.
    """
    sweep(proj)
    for t in range(proj.proj_len()):
        for timing in ("BEF_DECR", "AFT_DECR"):
            proj.pols_if_at(t, timing)
        proj.duration_mth(t)
    for z in range(1, proj.max_dur() + 1):
        proj.claim_surv_step(z)
    proj.premium_basis()


def _years_in_force(s_proj, sec_proj, month):
    """n: the whole years by which the SEC row's policy clock runs ahead of S's, 0 on a
    row of S's new business and ``n`` on a row of one of S's claims (the spec's
    ``_ip_twin_years``)."""
    gap = sec_proj.duration_mth_init() - s_proj.duration_mth(month)
    assert gap % 12 == 0, gap
    return gap // 12


def _cumulative_faults(s_proj, sec_proj, month):
    """Where SEC's cumulative counts depart from S's increments since S's month ``month``.

    Each restarts at ``t_entry()`` on SEC, on the count on the books, where S's counts from
    its frame's start, so at every month of SEC's frame SEC's count is S's at
    ``month + t`` less S's at ``month``, to 1e-9 relative with no absolute floor: 0.0 in
    both at ``t = 0``.  On a row issued later, before issue, SEC's is 0.0.
    """
    found = []
    entry = sec_proj.t_entry()
    for name in CUMULATIVE:
        base = s_proj.cells[name](month) if month > 0 else 0.0
        for t in range(sec_proj.proj_len()):
            got = sec_proj.cells[name](t)
            want = 0.0 if t < entry else s_proj.cells[name](month + t) - base
            if not abs(got - want) <= 1e-9 * max(abs(got), abs(want)):
                found.append(f"{name}({t}): SEC {got!r}, S's increment since its month "
                             f"{month} {want!r}")
    return found


def _clock_faults(s_proj, sec_proj, month):
    """Where a row of one of S's claims departs from S's clocks shifted by its years.

    SEC's policy clock runs ``12n`` months ahead of S's restarted one, at every month of
    the frame, and its issue age ``n`` years behind, so its attained age is S's, which the
    cell comparison holds, ``age`` being compared there; the cohort vector is ``12n``
    longer, the cover from issue and a cohort of headroom.
    """
    n = _years_in_force(s_proj, sec_proj, month)
    found = []
    if not n > 0:
        found.append(f"the row's clock is S's, n = {n}")
    if sec_proj.age_at_entry() != s_proj.age_at_entry() - n:
        found.append(f"issue age {sec_proj.age_at_entry()}, S's {s_proj.age_at_entry()} "
                     f"less {n}")
    for t in range(sec_proj.proj_len()):
        if sec_proj.duration_mth(t) != s_proj.duration_mth(month + t) + 12 * n:
            found.append(f"duration_mth({t}) {sec_proj.duration_mth(t)}, S's "
                         f"{s_proj.duration_mth(month + t)} plus {12 * n}")
            break
    if sec_proj.max_dur() != sec_proj.expiry_mth() + 1:
        found.append(f"max_dur() {sec_proj.max_dur()}, not expiry_mth() + 1")
    return found


def _cohort_faults(s_proj, sec_proj, month):
    """Where a row's cohorts, and the rates they are aged by, depart from S's.

    S carries a month's cohorts in one tuple, ``sick_cohorts(t)``, and their rates in three,
    ``claim_rate_vectors()``, and this model each element in a cell of its own, so the
    spec exempts S's two cells (``uk_sec_support.SEC_SPECS``) and the comparison maps them
    onto SEC's here, on every row.  At every month of the frame SEC's
    ``pols_sick_dur(t, z)`` holds S's ``sick_cohorts(month + t)`` element ``z - 1``, to
    1e-9 relative with no absolute floor, at every claim duration up to SEC's
    ``claim_dur_live(t)``, the cohorts that can hold lives, which the sums read; past it,
    to the end of S's vector, S's element is 0.0 exactly, which is why the sums may stop
    there; and SEC's vector is no shorter than S's.  And SEC's ``rec_rate_mth``,
    ``mort_rate_sick_mth`` and ``claim_surv_step`` hold S's three vectors element by
    element, exactly, at every claim duration S's vectors reach.  SEC's cohorts past
    ``claim_dur_live(t)`` are evaluated by none of this, and are held to 0.0 by C4's ``also``
    and the cohorts' own test.
    """
    found = []
    n = sec_proj.max_dur()
    for t in range(sec_proj.proj_len()):
        theirs = s_proj.sick_cohorts(month + t)
        if len(theirs) > n:
            found.append(f"max_dur() is {n}, S's vector {len(theirs)} long at {month + t}")
            break
        live = sec_proj.claim_dur_live(t)
        bad = []
        for z in range(1, live + 1):
            a = theirs[z - 1] if z <= len(theirs) else 0.0
            b = sec_proj.pols_sick_dur(t, z)
            if not abs(a - b) <= 1e-9 * max(abs(a), abs(b)):
                bad.append(z)
        bad += [z for z in range(live + 1, len(theirs) + 1) if theirs[z - 1] != 0.0]
        if bad:
            found.append(f"pols_sick_dur({t}, z) departs from S's sick_cohorts({month + t}) "
                         f"at z = {bad[:5]}, claim_dur_live {live}")
            break
    for cell, theirs in zip(("rec_rate_mth", "mort_rate_sick_mth", "claim_surv_step"),
                            s_proj.claim_rate_vectors()):
        mine = [sec_proj.cells[cell](z) for z in range(1, len(theirs) + 1)]
        if mine != list(theirs):
            found.append(f"{cell}(z) departs from S's claim_rate_vectors()")
    return found


def _compare(s_proj, sec_proj, month, exempt, columns=None):
    """Where SEC's row departs from S's point from S month ``month`` on, in two passes.

    First the frames, ``result_cf`` (over ``columns``, or every column both hold) and
    ``result_states``, SEC row ``t`` against S row ``t + month``, frames ending together;
    then every cell of S's but ``exempt`` and :data:`RESIDUALS`, at every argument S cached
    inside its frame from ``month`` on, moved onto SEC's clock, S's timing and kind strings
    mapped onto SEC's codes (``uk_sec_support.codes``).  Both to 1e-9 relative with no
    absolute floor (USLIB-SEC-PLAN.md §5.2, T2, precised at M11): a floor of 1e-9 passes an
    error of 1% in any value below 1e-7.  Then the cells of :data:`RESIDUALS` alone, at the
    floor of 1e-9: their exact value is 0, and the computed one moves by an ulp of what it
    closes when an opening state comes back from the CSV one ulp off.  Then the cumulative
    counts, by their increments (:func:`_cumulative_faults`).  Then the cohorts and their
    rates, which S carries in tuples and this model a cell an element, element by element
    (:func:`_cohort_faults`).  On a row of one of S's claims, whose policy clock S
    restarts, the cells of :data:`IN_CLAIM_CELLS` are left to :func:`_clock_faults`, and
    the lapse rate to neither report column: such a row on the exit basis holds no healthy
    life to lapse.  On a row S does not open at the valuation date, ``month`` not 0,
    :data:`DISCOUNT_CELLS` are left out.  Returns the mismatch lines, empty when the row
    is S's.
    """
    in_claim = s_proj.status() == "in_claim"
    if in_claim:
        exempt = exempt | IN_CLAIM_CELLS
    if month != 0:
        exempt = exempt | DISCOUNT_CELLS
    states = [c for c in s_proj.result_states().columns
              if not (in_claim and c == "lapse_rate")]
    found = []
    for report, keep in (("result_cf", columns), ("result_states", states)):
        found += [f"{report}: {line}" for line in frame_mismatches(
            s_proj.cells[report](), sec_proj.cells[report](), t_offset=month,
            columns=keep, atol=0.0)]
    found += twin_mismatches(s_proj, sec_proj, t_offset=month, exempt=exempt | RESIDUALS,
                             atol=0.0, codes=codes(sec_proj), arg_map=SPEC.twin_arg_map)
    found += twin_mismatches(s_proj, sec_proj, t_offset=month,
                             exempt=exempt | (set(s_proj.cells) - RESIDUALS),
                             codes=codes(sec_proj), arg_map=SPEC.twin_arg_map)
    found += _cumulative_faults(s_proj, sec_proj, month)
    found += _cohort_faults(s_proj, sec_proj, month)
    if in_claim:
        found += _clock_faults(s_proj, sec_proj, month)
    return found


def _continues_s(s_proj, sec_proj, month):
    """Where a committed row departs from S's point ``s_proj`` from S month ``month`` on.

    The splice's comparison (:func:`_compare`), on the committed model at the shipped
    assumptions: frame by frame, ``result_cf`` and ``result_states``, then cell by cell
    over every cell of S's but :data:`SPLICE_EXEMPT`.  The shipped 3% expense inflation
    runs from S's frame's start and from the valuation date here (D7), so on a row valued
    after that start :data:`INFLATED`'s two columns, and :data:`INFLATION_CELLS`, differ by
    design and are left out; the inflation test holds them.  On the twin of one of S's
    claims, which S opens at the valuation date, the two clocks of inflation are one.
    Every other column and cell must agree, to 1e-9 relative, with no absolute floor but on
    the residuals.
    """
    if month == 0:
        return _compare(s_proj, sec_proj, month, SPLICE_EXEMPT)
    keep = [c for c in s_proj.result_cf().columns if c not in INFLATED]
    return _compare(s_proj, sec_proj, month, SPLICE_EXEMPT | INFLATION_CELLS, keep)


def _case_id(rates, kind, s_point, month):
    """A case's id: ``main-point2-d12``, or ``main-point2-k3`` if issued later."""
    if kind == "future":
        return f"{rates}-point{s_point}-k{-month}"
    return f"{rates}-point{s_point}-" + (f"d{month}" if kind == "derived" else
                                         f"{kind}{month}")


def _case(case, core, case_id):
    """One parametrized case: run by default if it is in ``core``, else on the full grid."""
    return pytest.param(*case, id=case_id, marks=() if case in core else FULL_ONLY)


def _selected(cases, core):
    """The cases this run makes rows for: the core, or every one under UKLIB_SEC_FULL."""
    return [case for case in cases if SEC_FULL or case in core]


# Every row the splice compares, as (set, row_kind, S point, source_mth), T3's included,
# and the default run's among them.
GRID = (*SPLICES, *IN_FORCE_TWINS, *((r, "future", p, -k) for r, p, k in FUTURES))
CORE_GRID = frozenset({*CORE_SPLICES, *((r, "future", p, -k) for r, p, k in CORE_FUTURES)})


# ---------------------------------------------------------------------------
# Fixtures


class _KeptCell:
    """A cell of a kept point (:class:`_Kept`): called at arguments its sweep cached, the
    value cached; called at any other, the point's cell, computed afresh."""

    def __init__(self, point, name, parameters, values):
        self._point, self.name, self.parameters = point, name, parameters
        self._values = values

    def _key(self, args):
        """The key modelx caches ``args`` under (``uk_sec_support._args``, reversed)."""
        if not self.parameters:
            return ()
        return args[0] if len(self.parameters) == 1 else tuple(args)

    def __call__(self, *args):
        if len(args) == len(self.parameters):
            try:
                return self._values[self._key(args)]
            except (KeyError, TypeError):
                pass
        return self._point.live().cells[self.name](*args)

    def keys(self):
        return self._values.keys()


def _cohort_key(key):
    """Whether ``key`` is a month and a claim duration, each an int of 0 or more."""
    return (isinstance(key, tuple) and len(key) == 2
            and all(type(a) is int and a >= 0 for a in key))


class _KeptCohorts(_KeptCell):
    """``pols_sick_dur`` of a kept point, each float it cached held in a float64 array of
    the months by the claim durations, beside a mask of which are cached, rather than in a
    dict of some hundreds of thousands of floats: the same doubles, each returned as the
    Python float modelx caches.  A value cached under any other key, or of any other type,
    is kept as :class:`_KeptCell` keeps it."""

    def __init__(self, point, name, parameters, values):
        held = {k: v for k, v in values.items() if _cohort_key(k) and type(v) is float}
        shape = ((max(t for t, _ in held) + 1, max(z for _, z in held) + 1) if held
                 else (0, 0))
        self._array, self._held = np.zeros(shape), np.zeros(shape, dtype=bool)
        for (t, z), value in held.items():
            self._array[t, z], self._held[t, z] = value, True
        super().__init__(point, name, parameters,
                         {k: v for k, v in values.items() if k not in held})

    def __call__(self, *args):
        if _cohort_key(args):
            t, z = args
            if t < self._held.shape[0] and z < self._held.shape[1] and self._held[t, z]:
                return float(self._array[t, z])
        return super().__call__(*args)

    def keys(self):
        return [*((int(t), int(z)) for t, z in zip(*np.nonzero(self._held))),
                *self._values]


def _refuse_set(what, name):
    """A kept model takes no Reference: refuse ``what``'s ``name`` set, naming K7."""
    raise AttributeError(
        f"{what}.{name}: the committed model is kept as its sweep left it (sec_read), and "
        f"a Reference set on it would change nothing kept; set it on a model of the "
        f"test's own, read afresh, before anything is computed (K7)")


class _Kept:
    """One committed point as :func:`sec_read`'s sweep left it, kept as its values.

    Swept and held for the module, the committed points took 2 GB of the default run's
    peak: modelx keeps each value with the dependencies it records, and each claim cohort is
    a cell, read by four sums, about 2.9 KB an entry (measured at M8's review).  So each
    point is kept as what its sweep cached, a value and its arguments, and its ItemSpace
    released, and a test reads it as it read the swept point: through its cells
    (:class:`_KeptCell`), by name or as ``cells[name]``, every cell of the space among
    them, one the record holds nothing of computed on the point read afresh
    (:meth:`_KeptModel.live`), as is a call the sweep did not cache; ``idx`` and ``refs``
    are the point's own; ``data`` is ``Data`` as kept (:class:`_KeptData`); and its other
    References are the committed ``Projection``'s.  Any other attribute raises
    ``AttributeError``, and so does setting one (:func:`_refuse_set`).
    """

    def __init__(self, owner, key, proj):
        state = self.__dict__
        state["_owner"], state["_key"], state["cells"] = owner, key, {}
        for name, cells in proj.cells.items():
            n = len(cells.parameters)
            values = {k: cells(*(() if n == 0 else (k,) if n == 1 else k))
                      for k in list(cells.keys())}
            kind = _KeptCohorts if name == "pols_sick_dur" else _KeptCell
            self.cells[name] = kind(self, name, tuple(cells.parameters), values)
        for name, cells in owner.model.Projection.cells.items():
            if name not in self.cells:          # none in the record: each call is live
                self.cells[name] = _KeptCell(self, name, tuple(cells.parameters), {})

    def live(self):
        """The point's ItemSpace, read afresh, for a call its sweep did not cache."""
        return self._owner.live(self._key)

    def __getattr__(self, name):
        state = self.__dict__
        if name in state.get("cells", {}):
            return state["cells"][name]
        if "_owner" not in state:
            raise AttributeError(name)
        space = state["_owner"].model.Projection
        if name in space.parameters:            # idx: the point's own, as its ItemSpace's
            return state["_key"]
        if name == "refs":
            return {**dict(space.refs), **dict.fromkeys(space.parameters, state["_key"])}
        if name == "data":                      # Data as kept, which takes no Reference
            return state["_owner"].Data
        if name in space.refs:                  # a Reference, the space's and the point's
            return space.refs[name]
        raise AttributeError(f"a kept committed point (sec_read) has no {name!r}: it holds "
                             f"the space's cells, its References, idx and refs")

    def __setattr__(self, name, value):
        _refuse_set("a kept point", name)


class _KeptSpace:
    """The committed model's ``Projection`` as kept: indexed by the registry's keys, it
    gives each point kept (:class:`_Kept`); anything else it reads is the space's own, and
    a Reference set on it is refused (:func:`_refuse_set`)."""

    def __init__(self, owner):
        self.__dict__["_owner"] = owner

    def __getitem__(self, key):
        return self._owner.points[key]

    def __getattr__(self, name):
        return getattr(self.__dict__["_owner"].model.Projection, name)

    def __setattr__(self, name, value):
        _refuse_set("sec_model.Projection", name)


class _KeptData:
    """The committed model's ``Data`` as kept: every read is the space's own, as its
    sweep left it, and a Reference set on it is refused (:func:`_refuse_set`), since a
    point kept would hold the values of the one before and a call it did not cache would
    compute under the new."""

    def __init__(self, data):
        self.__dict__["_data"] = data

    def __getattr__(self, name):
        return getattr(self.__dict__["_data"], name)

    def __setattr__(self, name, value):
        _refuse_set("sec_model.Data", name)


# Each kept model, whose points read afresh after a test are released (_release_live).
_KEPT = []

# How many cache entries sec_read releases between its collections.  A released ItemSpace
# sits in reference cycles until Python's cyclic collector runs, at about 2.9 KB an entry
# with the dependencies modelx records; a collection over the module's heap costs a second
# or more, so the sweep collects after some 700 MB of released points, not after each.
KEPT_COLLECT = 250_000


class _KeptModel:
    """The committed model as :func:`sec_read` swept it, each point kept (:class:`_Kept`).

    ``Data`` is the model's own, as its sweep left it, its tables read once
    (:class:`_KeptData`); ``Projection`` gives the kept points (:class:`_KeptSpace`).
    Neither takes a Reference: a test that needs others reads a model of its own (K7).  A
    point a test calls where its sweep did not is read afresh, held until the test ends or
    until three more are (:meth:`live`), and released, so that the module holds the swept
    points' values and not their ItemSpaces.  ``uk_registry``'s helpers take it as they
    take a model.
    """

    LIVE = 3

    def __init__(self, model):
        self.model, self.name, self.Data = model, model.name, _KeptData(model.Data)
        self.points, self.held = {}, []
        self.Projection = _KeptSpace(self)
        _KEPT.append(self)

    def live(self, key):
        """``key``'s ItemSpace in the model, read afresh where it was released."""
        if key in self.held:
            self.held.remove(key)
        elif len(self.held) >= self.LIVE:
            _release(self.model, self.held.pop(0))
        self.held.append(key)
        return projection(self.model, key)

    def release(self):
        """Release every point read afresh, as a test ends."""
        while self.held:
            _release(self.model, self.held.pop())
        return True

    def __getattr__(self, name):
        return getattr(self.__dict__["model"], name)


@pytest.fixture(autouse=True)
def _release_live():
    """After each test, release the committed points it read afresh (:class:`_KeptModel`),
    and collect them, so that no test holds another's."""
    yield
    if any([kept.release() for kept in _KEPT if kept.held]):
        gc.collect()


@pytest.fixture(scope="module")
def sec_read():
    """IP_UK_SEC read in place, as committed, and swept once, cold; what it met; and each
    point kept as its sweep left it.

    The model is first asked for ``duration_mth(500)`` on the twin of S point 1, and the
    keys that call leaves in ``duration_mth`` are kept.  Then every committed point is
    swept (:func:`uk_sec_support.sweep`: ``result_cf``, the other reports and the checks),
    in table order and each column in ascending ``t``, under a recursion limit lowered to
    :data:`CALL_DEPTH`, and whatever that raises is kept, point by point, rather than
    raised.  So the record says what a cold model does, which the clock and depth test
    asserts (D3, R2).  Then, at the module's recursion limit, each point is swept whole,
    as C4 sweeps it (``uk_sec_support.full_sweep`` and :func:`_ip_c4_also`), kept
    (:class:`_Kept`) and released, one at a time, and the model holds no point: so every
    test on the committed model reads it as swept, and the sweep is paid once, not once
    for each.  Returns ``(the kept model, record)`` (:class:`_KeptModel`).
    """
    model = mx.read_model(model_path(SEC), name=_name("sec"))
    kept = _KeptModel(model)
    try:
        first = _row(model, "twin", 1, 0)
        record = {"duration_mth(500)": first.duration_mth(500),
                  "keys": list(first.cells["duration_mth"].keys()), "deep": []}
        del first                       # the point is swept, kept and released below
        labels = model.Data.model_point_table().index
        limit, released = mx.get_recursion(), 0
        for key, point_id in zip(point_keys(model), labels):
            proj = projection(model, key)
            mx.set_recursion(CALL_DEPTH)
            try:
                sweep(proj)
            except Exception as err:            # kept, so every point is swept
                record["deep"].append(f"point {point_id}: the sweep raised {_raised(err)}")
            finally:
                mx.set_recursion(limit)
            full_sweep(proj)
            _ip_c4_also(proj)
            kept.points[key] = _Kept(kept, key, proj)
            released += sum(len(cells.keys()) for cells in proj.cells.values())
            del proj
            _release(model, key)
            if released > KEPT_COLLECT:
                gc.collect()
                released = 0
        gc.collect()
        yield kept, record
    finally:
        _KEPT.remove(kept)
        model.close()


@pytest.fixture(scope="module")
def sec_model(sec_read):
    """IP_UK_SEC read in place, as committed, with every point swept and kept (sec_read)."""
    return sec_read[0]


@pytest.fixture(scope="module")
def s_model():
    """IP_UK_S read in place, as committed, with every point swept.

    T6 regenerates the SEC inputs from it, which would otherwise project every S point
    again (USLIB-SEC-PLAN.md §4, *Carried into Phase 1*), and the in-force tests read S's
    months off it.
    """
    model = mx.read_model(model_path(TWIN), name=_name("s"))
    for key in point_keys(model):
        _sweep_s(projection(model, key))
    yield model
    model.close()


def _set_points(rates):
    """The S points a splice set's S model holds: every point and variant in the main
    set, and the points of its cases in the others."""
    if rates == "main":
        return None
    return sorted({*SET_MTHS[rates], *(p for p, _ in SET_FUTURES[rates])})


class _Splices:
    """The splice's models, a pair for each of :data:`SPLICE_SETS`, each made when first
    asked for (:meth:`pair`) and closed at the module's end.

    For a set, S is read from a copy of the product directory whose table has the variants
    appended, only the set's points outside the main set, and the set's References are set
    on it.  SEC runs on the same assumption tables, and on a model point table and claim
    cohorts of its own, built by the generator from the registered spec with its rows
    replaced by the set's cases this run selects, the core or the full grid
    (:func:`_selected`), out of this S model, so each row opens with the state of the very
    run it is compared with, its cohorts among it; the set's References are set on it too.
    No input table moves with ``d``: IP's one valuation-clock input is the
    ``inflation_rate`` Reference.  An S point is swept (:func:`_sweep_s`) when a case first
    compares a row with it (:meth:`s_point`), and stays swept, the points of a set holding
    some tens of megabytes; each SEC row is projected by the case that compares it and
    released once compared (:func:`_settle`).
    """

    def __init__(self, root):
        self.root, self.pairs, self.swept = root, {}, {}

    def pair(self, rates):
        if rates not in self.pairs:
            refs = SPLICE_SETS[rates]
            s = mx.read_model(temp_inputs(self.root / rates / "s", model_path(TWIN),
                                          model_points=_s_table_with_variants(
                                              _set_points(rates))),
                              name=_name(f"s_{rates}"))
            for ref, value in refs.items():
                setattr(s.Projection, ref, value)
            derived = [(p, d) for r, kind, p, d in _selected(SPLICES + IN_FORCE_TWINS,
                                                             CORE_SPLICES)
                       if r == rates and kind == "derived"]
            futures = [(p, k) for r, p, k in _selected(FUTURES, CORE_FUTURES) if r == rates]
            spec = dataclasses.replace(SPEC, derived=tuple(derived), future=tuple(futures),
                                       derived_refs={})
            table, companions = build_sec_table(spec, s)
            sec = mx.read_model(_sec_inputs(self.root / rates / "sec", table,
                                            companions[COHORTS]),
                                name=_name(f"sec_{rates}"))
            for ref, value in refs.items():
                setattr(sec.Projection, ref, value)
            self.pairs[rates], self.swept[rates] = (s, sec), set()
        return self.pairs[rates]

    def s_point(self, rates, s_point):
        """S point ``s_point`` of set ``rates``, swept, as a comparison needs it: the S
        space must be swept before a row is compared with it, since the comparison reads
        what S cached (:func:`uk_sec_support.twin_mismatches`)."""
        s = self.pair(rates)[0]
        proj = _point(s, s_point)
        if s_point not in self.swept[rates]:
            _sweep_s(proj)
            self.swept[rates].add(s_point)
        return proj

    def close(self):
        for s, sec in self.pairs.values():
            sec.close()
            s.close()


@pytest.fixture(scope="module")
def spliced(tmp_path_factory):
    """The splice's models, by set, each pair made when first asked for (:class:`_Splices`)."""
    splices = _Splices(tmp_path_factory.mktemp("spliced"))
    yield splices
    splices.close()


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
    runs them (:func:`uk_sec_support.full_sweep`), and the cells of ``t`` and a second
    parameter at every argument C4 asks of them (:func:`_ip_c4_also`): every timing and
    kind in every month, and the cohorts outside the live ones, every claim duration in the
    month the row is first on the books among them.  No report of a row need read every
    state, and a base at ``t == 0`` would hide in a cell the reports leave unread
    (USLIB-SEC-PLAN.md §5.2, T2, precised at M4): the cohorts' base among them, which on a
    row issued later only a cohort of that first month reads, and no sum does, the live
    ones being none there (M8's review).  ``{"negative": [...], "early": [...],
    "ahead": [...], "raised": [...]}``: every cached call with a negative argument; every
    precedent keyed by a month before ``t_entry()`` of a call keyed by a month at or after
    it; every precedent keyed by a month beyond ``t + 1`` of a call keyed by ``t``, but
    :data:`LOOK_AHEAD`'s, which is empty; and every call the full sweep found raising, and
    C4's asks, the first that raised.  A precedent is a call's as modelx's dependency graph
    records it.
    """
    sweep(proj)
    raised = [f"{name}{args}: {text}" for (name, args), text in full_sweep(proj).items()]
    try:
        _ip_c4_also(proj)
    except Exception as err:                    # reported by the rules test
        raised.append(f"C4's asks: {_raised(err)}")
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


def _pivots(x):
    """The pivot ages of row ``x``'s inception schedule, sorted."""
    sub = x.data.inception_table().loc[(x.sex(), x.occ_class(), x.deferred_weeks())]
    return sorted(int(a) for a in sub.index)


def _held(x, t):
    """The claim durations at which row ``x`` holds lives in claim at the start of month
    ``t``: those its cohorts that can hold lives do, ``claim_dur_live(t)``."""
    return [z for z in range(1, x.claim_dur_live(t) + 1) if x.pols_sick_dur(t, z) > 0.0]


# What test_the_core_grid_reaches_every_branch asks of the core's rows in the model's own
# values, which no column of the table shows: each holds of some core row, or of a core row
# in some month of its frame.  At the valuation date, every opening-state column in use, a
# share or an amount apart from its issue value, and each kind of valuation month: in the
# first policy year, on an anniversary whose escalation is month 0's, every life in claim,
# lives in health and in claim, and a claim in the termination table's last year.  Later in
# the frame, every branch and both sides of each min and max the full grid reaches: an
# inception, a recovery back to health and one leaving the model, a death in each state, a
# lapse, an escalation, the escalation lapse shock and the RPI's floor and cap, the lapse
# table inside and past its last year, the termination table inside and past its last
# year, the inception rate interpolated between pivots and extrapolated beyond each end,
# the recovery rate's bound binding and not, an active cell on the exit basis and the
# policy end date's last month.  Four bounds bind elsewhere, each in a test of its own: the
# caps on mortality and inception, the lapse rate's bound, and the inception rate's floor
# at 0, which no shipped schedule reaches, each extrapolating to 0 only below age 13.3,
# under the youngest issue age, but which Data accepts a schedule that does, spliced in a
# copy of the inception table (test_the_inception_floor_continues_s_on_a_schedule_below_0).
# One is idle on every input the model accepts: the in-claim mortality's cap, since Data
# holds the termination table's rates to 0 to 1 and no factor multiplies them; its NaN
# test holds its order.
AT_VALUATION = {
    "lives in health and in claim": lambda x: 0.0 < x.pols_active_init() < 1.0,
    "every life in claim": lambda x: (
        x.duration_mth_init() > 0 and x.pols_active_init() == 0.0),
    "a claim in the termination table's last year": lambda x: (
        x.duration_mth_init() > 0 and any(
            x.claim_dur_year(z) >= x.data.termination_last_year()
            and x.pols_sick_dur_init(z) > 0.0 for z in range(1, x.duration_mth_init() + 1))),
    "benefit_pp_init above the benefit at issue": lambda x: (
        x.benefit_pp_init() > x.benefit_mth()),
    "premium_pp_init above the premium at issue": lambda x: (
        x.premium_pp_init() > x.premium_mth()),
    "valued in the first policy year": lambda x: 0 < x.duration_mth_init() < 12,
    "an escalation at t = 0 on an anniversary valuation": lambda x: (
        0 < x.duration_mth_init() and x.duration_mth_init() % 12 == 0
        and x.benefit_pp(0) > x.benefit_pp_init()),
    "a claim on a policy clock of whole years": lambda x: (
        x.status() == "in_claim" and x.duration_mth_init() % 12 == 0),
}
IN_FRAME = {
    "an inception": lambda x, t: x.pols_inception(t) > 0.0,
    "a recovery back to health": lambda x, t: (
        x.recovery_basis() == "return_to_h" and x.pols_recovery(t) > 0.0),
    "a recovery leaving the model": lambda x, t: x.pols_exit(t) > 0.0,
    "a death in claim": lambda x, t: x.pols_death_sick(t) > 0.0,
    "a death in health": lambda x, t: x.pols_death_active(t) > 0.0,
    "a lapse": lambda x, t: x.pols_lapse(t) > 0.0,
    "an escalation": lambda x, t: (
        _active(x, t) and x.esc_rate() > 0.0 and x.duration(t) > x.duration_init()),
    "the escalation lapse shock": lambda x, t: (
        _active(x, t) and x.esc_lapse_factor(t) > 1.0),
    "the RPI's floor binding": lambda x, t: (
        _active(x, t) and x.escalation() == "RPI" and x.rpi_rate < 0.0),
    "the escalation cap binding": lambda x, t: (
        _active(x, t) and x.escalation() == "RPI" and x.rpi_rate > x.esc_cap),
    "inside the lapse table": lambda x, t: (
        _active(x, t) and x.policy_year(t) < x.data.lapse_last_year()),
    "past the lapse table's last year": lambda x, t: (
        _active(x, t) and x.policy_year(t) > x.data.lapse_last_year()),
    "a claim inside the termination table": lambda x, t: (
        _active(x, t) and any(x.claim_dur_year(z) < x.data.termination_last_year()
                              for z in _held(x, t))),
    "a claim past the termination table's last year": lambda x, t: (
        _active(x, t) and any(x.claim_dur_year(z) > x.data.termination_last_year()
                              for z in _held(x, t))),
    "the inception rate between pivots": lambda x, t: (
        _active(x, t) and _pivots(x)[0] < x.age(t) < _pivots(x)[-1]),
    "the inception rate below the first pivot": lambda x, t: (
        _active(x, t) and x.age(t) < _pivots(x)[0]),
    "the inception rate past the last pivot": lambda x, t: (
        _active(x, t) and x.age(t) > _pivots(x)[-1]),
    "the recovery rate's bound binding": lambda x, t: (
        _active(x, t) and any(x.rec_rate(z) == 1.0 for z in _held(x, t))),
    "a recovery rate below its bound": lambda x, t: (
        _active(x, t) and any(0.0 < x.rec_rate(z) < 1.0 for z in _held(x, t))),
    "an active cell on the exit basis": lambda x, t: (
        x.recovery_basis() == "exit" and x.pols_active(t) > 0.0),
    "the policy end date's last month": lambda x, t: x.pols_maturity(t) > 0.0,
}


def _branches(x):
    """The names in :data:`AT_VALUATION` and :data:`IN_FRAME` that hold of row ``x``."""
    reached = {what for what, holds in AT_VALUATION.items() if holds(x)}
    frame = range(x.t_entry(), x.proj_len())
    return reached | {what for what, holds in IN_FRAME.items()
                      if any(holds(x, t) for t in frame)}


def _settle(records, case, model, key):
    """Record what the rules and the core grid's reach need of a row, and release it.

    ``case`` is the row's (set, row_kind, S point, source_mth) and ``key`` its registry key
    in ``model``, the splice's SEC model.  A T2 or T3 case calls this once it has compared
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
        sec = spliced.pair(case[0])[1]
        _settle(records, case, sec, _row_key(sec, *case[1:]))
    return records[case]


# ---------------------------------------------------------------------------
# T2 -- the splice


@pytest.mark.parametrize(
    "rates, kind, s_point, month",
    [_case(case, CORE_SPLICES, _case_id(*case)) for case in SPLICES + IN_FORCE_TWINS])
def test_an_in_force_point_continues_its_s_projection(spliced, splice_records, rates, kind,
                                                      s_point, month):
    """Opened with S's state at month d, the point is S from d on, in every cell of S's.

    This is the test that says the opening state is complete: a state column the SEC row
    did not carry, or carried from the wrong instant, would make SEC part from S here, and
    nowhere else, because on a point issued at ``t = 0`` the two clocks coincide and the
    opening state is the issue value.  For the same reason it is the test that catches a
    policy month passed as ``t`` (R1a), as an anniversary, a lapse table's year or an
    escalation read on ``t`` would be.  The frame comparisons read SEC row ``t`` against S
    row ``t + d`` in every column of ``result_cf`` and ``result_states``, and fail frames
    that end apart.  The cell comparison then evaluates every cell of S's but
    :data:`SPLICE_EXEMPT`, at every argument S cached inside its own frame from month ``d``
    on, moved onto SEC's clock: the healthy count, the cohort vector element by element,
    the transitions out of each state, the benefit, the premium and the rates, among them.
    Each compares to 1e-9 relative with no absolute floor, but the residuals, which keep the
    floor of 1e-9, and the cumulative counts, which restart on the books and are compared
    by their increments (:func:`_compare`).  An S cell this model lacked would fail it.

    A row of one of S's claims, which S opens with its policy clock restarted at the
    valuation date, is on its policy clock of whole years here, and is compared with S's
    clock shifted by them, its cohorts with S's padded with zeros.  The twins of those
    claims, issued ``n`` years before the valuation date, are compared at offset 0.  The
    row is then recorded for the rules test and released (:func:`_settle`).
    """
    s, sec = spliced.pair(rates)
    key = _row_key(sec, kind, s_point, month)
    s_proj, sec_proj = spliced.s_point(rates, s_point), projection(sec, key)
    try:
        assert _compare(s_proj, sec_proj, month, SPLICE_EXEMPT) == []
    finally:
        _settle(splice_records, (rates, kind, s_point, month), sec, key)


# ---------------------------------------------------------------------------
# T3 -- future new business


@pytest.mark.parametrize(
    "rates, s_point, k",
    [_case(case, CORE_FUTURES, _case_id(case[0], "future", case[1], -case[2]))
     for case in FUTURES])
def test_future_new_business_is_the_s_projection_k_months_on(spliced, splice_records,
                                                             rates, s_point, k):
    """Issued k months after the valuation date, the point is S's projection k months on.

    SEC rows ``k ..`` are S rows ``0 ..``, ending together at the policy end date, in
    ``result_cf`` and ``result_states``, and every cell of S's but :data:`FUTURE_EXEMPT`
    agrees at every argument S cached inside its own frame, moved ``k`` later, the cohort
    vector among them, all zeros until claims incept.  Each compares as the splice compares,
    with no absolute floor but on the residuals (:func:`_compare`).  An S cell this model
    lacked would fail it.  Before issue every column of ``result_cf``, ``result_states`` and
    ``result_pols`` is an exact zero, and the policies arrive in month ``k`` as new
    business, all healthy.

    The last assertions are R1 and D4's base rule made testable.  After the reports, no read
    keyed by an attained age or a policy year, and no monthly rate, has been evaluated at a
    month before issue (:data:`KEYED_READS`); the annual rates, columns of
    ``result_states``, are 0.0 there without a read.  A count recursion based at ``t == 0``
    rather than at ``t_entry()``, or a transition that evaluates its rate before asking
    whether the month is in cover, still gives the right numbers.  This is the only test
    that sees the first, and the guard test sees the second too.

    The pre-issue rows are asserted present before they are asserted zero, in every report:
    a frame that opened at issue would have none, its zeros would hold of nothing, and the
    comparisons with S, which start at issue, would not see it.  The row is then recorded
    for the rules test and released (:func:`_settle`).
    """
    s, sec = spliced.pair(rates)
    key = _row_key(sec, "future", s_point, -k)
    s_proj, sec_proj = spliced.s_point(rates, s_point), projection(sec, key)
    try:
        assert _compare(s_proj, sec_proj, -k, FUTURE_EXEMPT) == []
        for report in ("result_cf", "result_states", "result_pols"):
            frame = sec_proj.cells[report]()
            assert list(frame.index[:k]) == list(range(k)), report
            assert (frame.loc[:k - 1] == 0.0).all().all(), report
        assert sec_proj.pols_new_biz(k) == sec_proj.policy_count() == 1.0
        assert sec_proj.pols_active(k) == 1.0 and sec_proj.pols_sick(k) == 0.0
        early = {name: sorted(args[0] for args in _cached_args(sec_proj.cells[name])
                              if args[0] < k)
                 for name in KEYED_READS}
        assert not any(early.values()), f"read before issue: {early}"
    finally:
        _settle(splice_records, (rates, "future", s_point, -k), sec, key)


# ---------------------------------------------------------------------------
# The claim on the active-lives basis, under a flat lapse table
#
# IP_UK_S's point 7 is the worked example's claim on the return_to_h basis: its recovered
# lives return to health and lapse there.  S's row holds no issue date: S restarts the
# policy clock at the valuation date, and the twin is given one, issued a whole year before
# it, the least whole year that holds the claim, though a claim at duration 0 after a
# 26-week deferral fits a policy 7 to 11 months old.  So the twin's clock runs a year
# ahead of S's: in each year S lapses the recovered lives at a policy year's rate, 10% in
# its first, where the twin lapses them at the next year's, 8% in its second, and so on
# down the table (UKLIB-SEC-PLAN.md §6.3, model-sec.md).  Neither is the policy's real
# clock, which S's row does not record.  So the twin and its rows are compared with S under
# a lapse table that is flat, every year at 10%, the shipped first year's rate, on which
# the two clocks lapse alike.  The first year's rate being the shipped one, S's states up
# to any month are what the shipped table gives them, so the committed row of point 7 at
# month 12 continues S there too.
FLAT_LAPSE = {"lapse_table.csv": lambda t: t.assign(lapse_rate=0.10)}
POINT7_MTHS = {"core": (1, 12), "full": (13, 24, 60, 359)}


@pytest.mark.parametrize("grid", GRIDS)
def test_the_claim_on_the_active_lives_basis_continues_s_under_a_flat_lapse_table(
        tmp_path, grid):
    """S's point 7, its twin and its rows, are S's under a flat lapse table (§6.3).

    Under :data:`FLAT_LAPSE`, in S and SEC alike, with the main set's References
    (:data:`MAIN`), the twin of S's point 7, issued a year before the valuation date at
    34, and the point restated in force at a month after its claim's first recoveries
    have returned to health and started claiming again, are S's from their months on, in
    every cell, as the splice compares them (:func:`_compare`): the healthy lives, each
    cohort, the recoveries back to health and every flow.  The default run compares the
    twin and the rows at months 1 and 12, and the full grid the rows at 13, 24, 60 and 359.

    And at the shipped lapse table the twin parts from S, its clock a year ahead of S's
    restarted one: in their first year its recovered lives lapse at the second policy
    year's 8% where S's lapse at the first's 10%, so that 60 months on 0.8002 of the policy
    is in force where S holds 0.7791.  The difference is the clock each model gives the
    claim, S's row recording none: S's restarted clock, which model-sec.md records, against
    the least whole year the generator gives the twin, and no departure of this model's.
    """
    s = mx.read_model(temp_inputs(tmp_path / "s", model_path(TWIN), edits=FLAT_LAPSE),
                      name=_name("flat_s"))
    sec = None
    try:
        for ref, value in MAIN.items():
            setattr(s.Projection, ref, value)
        months = POINT7_MTHS[grid]
        spec = dataclasses.replace(SPEC, derived=tuple((7, d) for d in months), future=(),
                                   derived_refs={})
        table, companions = build_sec_table(spec, s)
        sec = mx.read_model(_sec_inputs(tmp_path / "sec", table, companions[COHORTS],
                                        edits=FLAT_LAPSE), name=_name("flat"))
        for ref, value in MAIN.items():
            setattr(sec.Projection, ref, value)
        s_proj = _point(s, 7)
        _sweep_s(s_proj)
        cases = ((("twin", 7, 0),) if grid == "core" else ()) + tuple(
            ("derived", 7, d) for d in months)
        found = []
        for case in cases:
            found += [f"{case}: {line}" for line in _compare(
                s_proj, _row(sec, *case), case[2], SPLICE_EXEMPT)]
        assert not found, found[:20]
        if grid == "full":
            return
        back = _row(sec, "derived", 7, 12)
        assert 0.0 < back.pols_active_init() < 1.0 and back.pols_recovery(0) > 0.0
        assert back.pols_inception(0) > 0.0
    finally:
        if sec is not None:
            sec.close()
        s.close()
    shipped_s = mx.read_model(model_path(TWIN), name=_name("defect_s"))
    shipped = mx.read_model(model_path(SEC), name=_name("defect"))
    try:
        twin, s7 = _row(shipped, "twin", 7, 0), _point(shipped_s, 7)
        assert (twin.lapse_rate(0), s7.lapse_rate(0)) == (0.08, 0.1)
        assert round(twin.pols_if(60), 4) == 0.8002 and round(s7.pols_if(60), 4) == 0.7791
        assert twin.pols_if(1) == s7.pols_if(1) and twin.pols_if(2) != s7.pols_if(2)
    finally:
        shipped.close()
        shipped_s.close()


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
    The splice's rows are points in force at every month T2 names, the variants and the
    twins of S's claims among them, and points issued later, under every set, and on each
    the reports, the checks and the full sweep are run first, with the cells of ``t`` and a
    timing, a kind or a claim duration at every argument C4 asks (:func:`_rule_breaches`):

    * R1: no cell holds a negative argument.  modelx evaluates one without complaint, and
      a compiled cache raises ``IndexError`` below 0 (USLIB-SEC-PLAN.md F4).  A policy
      month turned into ``t`` by subtracting ``duration_mth_init()`` (R1a) goes negative
      on a point in force past it.
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
    twins in the splice's tables are no case's, and are left out: on them the clocks
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


def test_the_kept_committed_model_takes_no_reference(sec_model):
    """The committed model, kept as its sweep left it, refuses a Reference set, and each
    kept point reads as its own ItemSpace would.

    The swept model recomputed after a Reference was set; the kept one cannot, since its
    points are values (:func:`sec_read`).  So setting a Reference on its ``Projection``,
    on its ``Data`` or on a point raises ``AttributeError`` naming K7, before any test can
    read a value of the References before beside one computed under the new, and the
    model's own References are as shipped after.  A kept point's ``idx`` is its own
    position, not the base space's 0, its ``refs`` hold it, and an attribute that is no
    cell, Reference, ``idx`` or ``refs`` of it raises (M8's verification).
    """
    key = point_keys(sec_model)[8]
    p = projection(sec_model, key)
    for target, name, value in ((sec_model.Projection, "rpi_rate", 0.12),
                                (sec_model.Data, "rate_age_min", 36.0),
                                (p, "rpi_rate", 0.12), (p.data, "rate_age_min", 36.0)):
        with pytest.raises(AttributeError, match=r"\(K7\)"):
            setattr(target, name, value)
    assert (sec_model.Projection.rpi_rate, sec_model.Data.rate_age_min) == (0.03, 18.0)
    assert (p.rpi_rate, p.data.rate_age_min) == (0.03, 18.0)
    assert p.idx == p.refs["idx"] == key == 8 and p.point_id() == 9
    with pytest.raises(AttributeError, match="has no 'nonesuch'"):
        p.nonesuch


# How deep a cold call may run beyond its chain, one cell a month from its month back to
# t_entry() (D5): the cells above the chain and those below it, the first month's rates and
# Data's first reads of its tables.  IP runs its chains one cell a month: the healthy count,
# pols_active, which reads itself at t - 1 and the recoveries of t - 1; the cohorts,
# pols_sick_dur(t, z), each reading the cohort a duration younger at t - 1, down the
# diagonal to the inceptions of the month it opened or to the companion at t_entry(); and
# the three cumulative counts, each reading itself at t - 1.  At M7, the cohort vector a
# tuple, a cold net_cf in the last month ran 8 or 9 cells beyond its chain, 631 or 632
# levels deep from issue at 18 to expiry at 70.  Measured at M8, on the chains as the C
# step left them, one cell a month, at the contract's longest cover, issued at 18 now and
# 120 months on and in claim a year at the valuation date on each basis, with the
# escalation lapse shock on, each head cold in the last month on a read of its own, as the
# test below calls it: the chain is 623 cells on the healthy shapes and 611 on the
# claims, the same on every head, and the healthy count's head runs 5 beyond it, the
# oldest cohort the month can hold 6 down its diagonal on the healthy shapes and 5 on the
# claims, the cumulative count and the population identity's residual 6, the lives in
# claim, the roll-forward's residual, the count by timing and net_cf 7, and the benefit
# claims 8, the most.  Compiled, the diagonal ran on 144 KiB of C stack and every other
# head on 136 or less, inside the 256 KiB the C step allows itself (UKLIB-SEC-PLAN.md
# §6.6, *Record -- M10*), so no chain is blocked by policy year.  So each head's bound is
# its own measured overhead, rather than Term's 16 (USLIB-SEC-PLAN.md D5) or the benefit
# claims' 8 for every head: any chain of two cells a month runs a frame's length beyond
# it, and the diagonal read a duration at a time, (t - 1, z), runs no deeper but parts
# from IP_UK_S's cohorts.
CHAIN_OVERHEAD = {("net_cf", None): 7, ("pols_active", None): 5, ("pols_sick", None): 7,
                  ("pols_sick_dur", "LIVE"): 6, ("claims", "BENEFIT"): 8,
                  ("pols_dead_cum", None): 6, ("check_states_resid", None): 6,
                  ("check_pols_roll_fwd_resid", None): 7, ("pols_if_at", "BEF_NB"): 7}

# The contract's longest cover (held by proj_len()): issued at issue_age_min, 18, to
# expiry_age_max, 70, 624 months, the same on every shape.
YOUNGEST, OLDEST_EXPIRY = 18, 70

# The chains of the model and the cells that head them, called cold in the last month of
# the frame, each on a read of its own: (cell, the timing or kind it takes, "LIVE" for the
# oldest cohort the month can hold, claim_dur_live(t), or None).
CHAIN_HEADS = tuple(CHAIN_OVERHEAD)


def _head_args(proj, last, second):
    """The arguments a head of :data:`CHAIN_HEADS` is called cold with in month ``last``."""
    if second is None:
        return (last,)
    if second == "LIVE":
        return (last, proj.claim_dur_live(last))
    return (last, _code(proj, second))

# The shapes the chains run at their longest cover on, by the S point whose twin each is,
# with the recovery basis each runs on: the anchor cell, healthy at issue, on the
# active-lives basis and on the exit basis, issued now and 120 months on; and the claim
# from duration 0 on each basis, in force a year at the valuation date, the cohort in
# payment its one row.  The anchor cell on the active-lives basis runs by default, and the
# other three with the full grid.
CHAIN_SHAPES = {"active": (1, "return_to_h"), "active_exit": (1, "exit"),
                "claim_exit": (2, "exit"), "claim": (7, "return_to_h")}


class _ColdRuns:
    """Each chain head called cold at the contract's longest cover, under modelx's stack
    trace, kept by (shape, label, head) once made, for the depth test and the chain-text
    test alike: a head's run at the longest cover forms a few hundred thousand cohorts in
    modelx, and the two tests read the same trace, the depth of its deepest point and the
    cells on the stack there.  Each run is made on a read of its own, closed once the
    trace is read, so that it is cold and holds nothing after; the shape's rows are made
    once (:func:`_longest_cover`)."""

    def __init__(self, root):
        self.root, self.covers, self.runs = root, {}, {}

    def frames(self, shape):
        """The rows of ``shape`` at its longest cover, as ``(label, months, entry)``."""
        if shape not in self.covers:
            self.covers[shape] = _longest_cover(self.root / shape, shape)
        return self.covers[shape][1]

    def run(self, shape, label, head):
        """``(the call's arguments, its depth, its chain back to t_entry(), the cells on
        the stack at its deepest point)`` for ``head`` of :data:`CHAIN_HEADS` on row
        ``label`` of ``shape``, at an RPI of 5%, cold."""
        key = (shape, label, head)
        if key not in self.runs:
            months, entry = next((m, e) for lab, m, e in self.frames(shape) if lab == label)
            fresh = mx.read_model(self.covers[shape][0], name=_name("cold"))
            try:
                fresh.Projection.rpi_rate = 0.05
                p = _point(fresh, label)
                assert p.proj_len() == months and p.t_entry() == entry, label
                last = months - 1
                args = _head_args(p, last, head[1])
                stack = _deepest_stack(p, head[0], args)
                self.runs[key] = (args, len(stack), last - entry, stack)
            finally:
                fresh.close()
        return self.runs[key]


@pytest.fixture(scope="module")
def cold_runs(tmp_path_factory):
    """The chain heads' cold runs at the longest cover, made when first asked for
    (:class:`_ColdRuns`)."""
    return _ColdRuns(tmp_path_factory.mktemp("cold"))


def _longest_cover(tmp_path, shape):
    """A copy whose table holds the twin of :data:`CHAIN_SHAPES`'s ``shape`` at the
    contract's longest cover, and each row's frame and ``t_entry()``.

    The twin issued at 18 and expiring at 70, 624 months of cover.  On a healthy shape,
    issued at the valuation date and 120 months after it, the shipped
    ``future_horizon_mth``: frames of 624 and 744 months, whose chains stop at
    ``t_entry()``.  On a claim, in force a year at the valuation date, its cohort in
    payment carried over: a frame of 612 months.  The shipped tables serve every age from
    18 to 69.
    """
    s_point, basis = CHAIN_SHAPES[shape]
    committed = _committed()
    label = _label(committed, "twin", s_point, 0)
    top = committed.index.max()
    row = committed.loc[[label]].assign(recovery_basis=basis, expiry_age=OLDEST_EXPIRY,
                                        entry_age=YOUNGEST)
    cover = 12 * (OLDEST_EXPIRY - YOUNGEST)
    if committed.at[label, "duration_mth"] > 0:
        rows = row.set_axis([top + 1]).rename_axis("point_id")
        held = _committed_cohorts()
        held = pd.concat([held, held[held["point_id"] == label].assign(point_id=top + 1)],
                         ignore_index=True)
        d = int(committed.at[label, "duration_mth"])
        return _sec_inputs(tmp_path, pd.concat([committed, rows]), held), [
            (top + 1, cover - d, 0)]
    rows = pd.concat([row.set_axis([top + 1]),
                      row.assign(duration_mth=-120).set_axis([top + 2])])
    rows = rows.rename_axis("point_id")
    return _sec_inputs(tmp_path, pd.concat([committed, rows])), [
        (top + 1, cover, 0), (top + 2, cover + 120, 120)]


# modelx warns as its stack trace starts and stops, which is all the test does with it.
@pytest.mark.filterwarnings("ignore:call stack trace:UserWarning")
@pytest.mark.parametrize("shape", [pytest.param(s, id=s,
                                                marks=() if s == "active" else FULL_ONLY)
                                   for s in CHAIN_SHAPES])
def test_every_chain_runs_one_cell_a_month_from_a_cold_start(cold_runs, shape):
    """Called cold, each chain runs one cell a month back to ``t_entry()``, no more.

    No number shows how deep a chain runs, and a compiled model runs it on the C stack, so
    a chain of two cells a month, which gives the same numbers, needs twice the stack on
    every platform (F7); ``IP_UK_S``'s chains each run one cell a month, but reach back to
    its frame's start.  On a model just read, nothing is cached, so modelx's stack trace
    counts how deep a call runs, against one cell a month back to ``t_entry()`` and the
    head's own measured overhead more, :data:`CHAIN_OVERHEAD`, with modelx's recursion
    limit where the module leaves it: each head of :data:`CHAIN_HEADS` in the last month of
    the frame, each on a read of its own (:class:`_ColdRuns`), the cohorts' at the oldest
    cohort the month can hold, whose diagonal runs back to the month it opened, at an RPI
    of 5%, so that the escalation lapse shock reads the RPI in every month.  On each shape
    at the contract's longest cover, 624 months from issue age 18 to expiry age 70, issued
    now and 120 months on, or in claim a year at the valuation date
    (:func:`_longest_cover`), each row's frame asserted first, as M1's carried rule asks,
    that every chain runs at its own shape's longest cover.  The anchor cell on the
    active-lives basis issued 120 months on, which runs every chain and stops each at a
    ``t_entry()`` of 120, past which a chain reaching before it would run 120 cells more,
    runs by default, and the anchor cell issued now and the other shapes on the full grid:
    each head's cold run forms the whole triangle of cohorts in modelx, some seconds each.
    """
    frames = cold_runs.frames(shape)
    if shape == "active" and not SEC_FULL:
        frames = [frame for frame in frames if frame[2] > 0]
    found = []
    for label, months, entry in frames:
        for head in CHAIN_HEADS:
            args, depth, chain, _ = cold_runs.run(shape, label, head)
            assert chain == months - 1 - entry, (label, head)
            bound = CHAIN_OVERHEAD[head]
            if not chain <= depth <= chain + bound:
                found.append(f"point {label}: {head[0]}{args} cold runs {depth} cells "
                             f"deep, where one cell a month back to t_entry() {entry} is "
                             f"{chain} and {bound} more are allowed")
    assert frames and not found, found


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


# The cells the chains recurse through, each of which the chain-text test must find held
# more than once on some head's deepest path, or it would check less than it says.
CHAIN_CELLS = frozenset({"pols_active", "pols_sick_dur", "pols_dead_cum"})


# modelx warns as its stack trace starts and stops, which is all the test does with it.
@pytest.mark.filterwarnings("ignore:call stack trace:UserWarning")
def test_no_cell_a_chain_recurses_through_formats_a_refusal(cold_runs, sec_model):
    """No cell a cold call's deepest path holds more than once builds text (M10).

    A compiled cell's C frame holds the code that formats each of its messages, whether a
    run reaches it or not, and a chain holds a frame of each cell it recurses through at
    each level.  On CI's Ubuntu runner, a refusal formatted inside ``Term_UK_SEC``'s
    recursive waiver cell had its cold call at the longest cover need 512 KiB to 1 MiB,
    and 256 to 384 once the cell held none (K12).  So every refusal of this model whose
    message is formatted sits in a cell no chain recurses through: ``proj_len()``, the
    rates' reads of their tables and the cells that refuse a value past the floats are each
    held once, at a chain's head or its foot.  On a model just read, at the longest cover
    of the anchor cell on the active-lives basis, which runs every chain, issued 120 months
    on, the depth test's default run, whose traces this reads (:class:`_ColdRuns`), each
    head of :data:`CHAIN_HEADS` is called cold in the last month, under modelx's stack
    trace, at an RPI of 5%, and the cells on the stack at its deepest point are counted.  A
    cell held there twice or more is one a chain recurses through, at every month.  None of
    them may build text anywhere in its formula, at a raise, in an error branch or into a
    local, nor raise other than one exception on one string constant
    (:func:`_text_faults`): the frame holds a message's code whether or not its branch
    runs.  The healthy count, the cohorts and a cumulative count must be among the cells
    checked (:data:`CHAIN_CELLS`), or the test would check less than it says.
    """
    found, checked = [], set()
    for label, months, entry in cold_runs.frames("active"):
        if entry == 0:
            continue
        for head in CHAIN_HEADS:
            args, _, _, stack = cold_runs.run("active", label, head)
            assert len(stack) > 600, (label, head, len(stack))
            held = {name for name in stack if stack.count(name) > 1}
            checked |= held
            for name in sorted(held):
                faults = _text_faults(sec_model.Projection.cells[name])
                if faults:
                    found.append(f"point {label}: {head[0]}{args}: {name}, held "
                                 f"{stack.count(name)} times on the deepest path, "
                                 f"builds text: {faults}")
    assert CHAIN_CELLS <= checked, sorted(checked)
    assert not found, found


# ---------------------------------------------------------------------------
# T4 -- the count algebra
#
# BEF_DECR == BEF_NB + pols_new_biz, at every t of every point, is a convention
# (test_new_business_joins_the_count_before_decrements), and is not repeated here.


def test_the_counts_roll_forward_through_the_states(sec_model):
    """The count leaves month t by its exits, and the transitions move lives between the
    states.

    On every committed point and at every ``t`` of its frame, to 1e-12: the count in force
    weighting month ``t``, ``pols_if(t)``, less the count it carries into ``t + 1``,
    ``pols_if_at(t + 1, BEF_NB)``, is the deaths in health and in claim, the lapses, the
    recoveries that leave the model and the expiry, which in the last month takes every
    survivor; and the notes' end-of-month count, ``pols_if_at(t, AFT_DECR)``, is exactly the
    count carried into the next month before its new business, 0 in the last.  Within the
    frame the healthy count falls by its deaths, its lapses and its inceptions and rises by
    the recoveries that return to health, and the sick count falls by its recoveries and its
    deaths and rises by the inceptions, so that an inception or a returning recovery moves
    a life between the states and out of neither.

    ``result_pols()`` sets the same movement out row by row, in :data:`RESULT_POLS`'s
    columns, indexed by ``t`` over the frame: ``pols_if`` at ``t + 1`` is ``pols_if`` less
    its exits at ``t``, plus the new business of ``t + 1``, row 0 opening from
    ``pols_if_init()`` within the shares' tolerance, 1e-10 of the count, which ``Data``
    holds the opening shares to.
    """
    table = sec_model.Data.model_point_table()
    for key, point_id in zip(point_keys(sec_model), table.index):
        p = projection(sec_model, key)
        bef_nb, aft = (_code(p, c) for c in ("BEF_NB", "AFT_DECR"))
        last = p.proj_len() - 1
        back = p.recovery_basis() == "return_to_h"
        for t in range(p.proj_len()):
            carried = p.pols_if_at(t + 1, bef_nb)
            assert p.pols_if_at(t, aft) == (0.0 if t == last else carried), (point_id, t)
            out = (p.pols_death_active(t) + p.pols_death_sick(t) + p.pols_lapse(t)
                   + p.pols_exit(t) + p.pols_maturity(t))
            assert p.pols_if(t) - carried == pytest.approx(out, abs=1e-12), (point_id, t)
            if t == last:
                continue
            healthy = (p.pols_death_active(t) + p.pols_lapse(t) + p.pols_inception(t)
                       - (p.pols_recovery(t) if back else 0.0))
            entering = p.pols_active(t + 1) - p.pols_new_biz(t + 1)
            assert p.pols_active(t) - entering == pytest.approx(healthy, abs=1e-12), (
                point_id, t)
            sick = p.pols_recovery(t) + p.pols_death_sick(t) - p.pols_inception(t)
            assert p.pols_sick(t) - p.pols_sick(t + 1) == pytest.approx(sick, abs=1e-12), (
                point_id, t)
        pols = p.result_pols()
        assert list(pols.columns) == RESULT_POLS, point_id
        assert pols.index.name == "t" and list(pols.index) == list(range(p.proj_len()))
        out = pols[["pols_death_active", "pols_death_sick", "pols_lapse", "pols_exit"]]
        carried = (pols["pols_if"] - out.sum(axis=1)).shift(1)
        expected = carried.fillna(p.pols_if_init()) + pols["pols_new_biz"]
        gap = (pols["pols_if"] - expected).abs()
        assert gap.iloc[0] <= 1e-10 * max(p.policy_count(), 1.0), point_id
        assert (gap.iloc[1:] <= 1e-12).all(), point_id


def test_result_pols_holds_s_counts_with_the_new_business_beside_it(sec_model, s_model):
    """``result_pols()`` is S's counts and amounts, column by column, the new business
    beside them (D5).

    ``IP_UK_S`` has no ``result_pols``: its counts are cells, some in ``result_states``,
    which T1 compares at every month.  So the report is compared here with S's cells, on
    the twins S projects from the valuation date, its new business and its two claims on
    the exit basis, each at offset 0: every column but ``pols_new_biz`` is S's cell of its
    name, the benefit and the premium included, to 1e-9 relative with no absolute floor,
    and ``pols_new_biz`` holds the count in the issue month and 0 in every other.  The
    counts and amounts carry no inflation, so the shipped assumptions serve.  The claim on
    the active-lives basis, which S lapses on its restarted clock, has a test of its own.
    """
    table = sec_model.Data.model_point_table()
    twins = table.index[table["row_kind"] == "twin"].tolist()
    assert twins == sorted(s_model.Data.model_point_table().index)
    for point_id in (1, 2, 3, 4, 5, 6):
        p, s = _point(sec_model, point_id), _point(s_model, point_id)
        pols = p.result_pols()
        assert list(pols.columns)[:2] == ["pols_if", "pols_new_biz"]
        assert len(pols) == s.proj_len(), point_id
        for column in RESULT_POLS:
            if column == "pols_new_biz":
                continue
            theirs = [s.cells[column](t) for t in pols.index]
            bad = [t for t, (a, b) in enumerate(zip(theirs, pols[column]))
                   if not abs(a - b) <= 1e-9 * max(abs(a), abs(b))]
            assert not bad, (point_id, column, bad[:5])
        issue = -int(table.at[point_id, "duration_mth"])
        assert list(pols["pols_new_biz"]) == [
            p.policy_count() if t == issue else 0.0 for t in pols.index], point_id


# What T4 multiplies the counts by: not a whole number, because a count of policies need
# not be one, so that a flow which read the count as whole policies would not follow it.
COUNT_FACTOR = 2.5

# Every assumption that ships idle or neutral switched on, for T4, at the shipped inflation:
# the main splice set's (MAIN), but its inflation of 0.
SWITCHED_ON = {ref: value for ref, value in MAIN.items() if ref != "inflation_rate"}


def _pairs(want, got):
    """The values a counted cell holds, as pairs: its two numbers, or a cohort vector's
    elements, which must be as many."""
    if isinstance(want, tuple):
        assert isinstance(got, tuple) and len(got) == len(want)
        return list(zip(want, got))
    return [(want, got)]


@pytest.mark.parametrize("grid", GRIDS)
def test_scaling_the_counts_scales_every_flow_and_no_per_policy_value(tmp_path, grid):
    """The count is the weight: 2.5 times it, 2.5 times every flow, the same per policy.

    The committed table, and a copy with every ``policy_count`` multiplied by
    :data:`COUNT_FACTOR`, are each read with :data:`SWITCHED_ON` set before either computes
    anything: every assumption that ships idle or neutral, on, so that the escalation lapse
    shock moves the lapses, the cycle overlay the inceptions and the recoveries, and the
    amount payable and the severity the benefit.  The shares and the amounts of the opening
    state are per policy, and stay.  On every point ``result_cf``, the counts of
    ``result_pols`` and every column of ``result_states`` but its rates are 2.5 times the
    committed table's, element by element, to 1e-12 relative: a scaled count is a computed
    float, which may come back from the CSV within two ulps (``uk_sec_support``'s module
    docstring).  ``result_pols``'s per-policy columns are the committed table's exactly.
    So is every other cell of :data:`COUNTED`, at every argument the sweep of the committed
    table's point cached, the present value among them: the counts at each timing, the
    cohort vector element by element, the transitions out of each state and the claims of
    each kind, which no report shows, and the two residuals, roundings about 0 on that many
    policies, to their floor of 1e-9.  And every cell outside :data:`COUNTED` (the shares,
    the benefit, the premium, the rates, both clocks, the flags) agrees bit for bit at
    every argument that sweep cached, but the annuity factor, the present value over the
    count, a ratio of two scaled floats, which agrees to 1e-12.  So a flow that dropped the
    count, or read it as whole policies, which a table of counts of 1 hides from every
    comparison with S and a count doubled hides here, fails (USLIB-SEC-PLAN.md §5.2, T4,
    precised at M11).  Each counted cell but the residuals is nonzero on some point; the
    death and lapse claims are zero on every point by design, the product paying no death
    benefit and no surrender value.

    The default run takes :data:`CORE_POINTS`, among which every counted cell is nonzero,
    and the full grid the other committed points.
    """
    table = _committed()
    base = mx.read_model(_sec_inputs(tmp_path / "base", table), name=_name("counted"))
    scaled = mx.read_model(_sec_inputs(tmp_path / "scaled", table.assign(
        policy_count=COUNT_FACTOR * table["policy_count"])), name=_name("scaled"))
    reports = ("result_cf", "result_states", "result_pols")
    counted = sorted(COUNTED - set(reports))
    per_policy = {"result_pols": PER_POLICY_POLS,
                  "result_states": ["inception_rate", "mort_rate", "lapse_rate"],
                  "result_cf": []}
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
            one.pv_benefits()
            one.annuity_dis()
            for report in reports:
                b, d = one.cells[report](), many.cells[report]()
                assert d.index.equals(b.index) and list(d.columns) == list(b.columns)
                flows = [c for c in b.columns if c not in per_policy[report]]
                want = COUNT_FACTOR * b[flows]
                bad = ((d[flows] - want).abs() > 1e-12 * want.abs()).any()
                assert not bad.any(), (key, report, list(bad[bad].index))
                fixed = per_policy[report]
                assert d[fixed].equals(b[fixed]), (key, report)
            for name in counted:
                floor = 1e-9 if name in RESIDUALS else 0.0
                for args in _cached_args(one.cells[name]):
                    for one_value, got in _pairs(one.cells[name](*args),
                                                 many.cells[name](*args)):
                        want = COUNT_FACTOR * one_value
                        assert abs(got - want) <= floor + 1e-12 * abs(want), (
                            key, name, args, got, want)
                        if want != 0.0 and name not in RESIDUALS:
                            nonzero.add(name)
            assert twin_mismatches(one, many, exempt=TWIN_EXEMPT_DEFAULT | COUNTED
                                   | {"annuity_dis"}, rtol=0.0, atol=0.0) == []
            assert many.annuity_dis() == pytest.approx(one.annuity_dis(), rel=1e-12, abs=0)
            _release(base, key)
            _release(scaled, scaled_key)
    finally:
        scaled.close()
        base.close()
    if grid == "core":
        want = set(counted) - RESIDUALS - {"pols_sick_dur"}
        assert want <= nonzero, f"0 on every core point: {sorted(want - nonzero)}"


def _restated_a_month_on(p, label):
    """Point ``p``'s row as this model carries it into month 1, under ``label``: its count,
    healthy share and cohorts at the start of month 1, before its events, and the benefit
    and premium of month 0, entering month 1.  ``(the table's row, the cohorts' rows)``."""
    count = p.pols_if_at(1, _code(p, "BEF_NB"))
    cohorts = pd.DataFrame(
        [{"point_id": label, "z": z, "pols_sick_dur_init": held / count}
         for z in range(1, p.claim_dur_live(1) + 1)
         if (held := p.pols_sick_dur(1, z)) != 0.0],
        columns=["point_id", "z", "pols_sick_dur_init"])
    return {"duration_mth": p.duration_mth(1), "policy_count": count,
            "pols_active_init": p.pols_active(1) / count,
            "benefit_pp_init": p.benefit_pp(0), "premium_pp_init": p.premium_pp(0)}, cohorts


@pytest.mark.parametrize("grid", GRIDS)
def test_a_point_restated_a_month_on_continues_its_own_flows(tmp_path, grid):
    """The counts a point carries into a month are the counts that weight its flows (T4).

    Scaling the count, as the test above does, cannot see a flow weighted by the count a
    point opened with, ``policy_count()``, rather than the count in force in its month, nor
    one weighted by the healthy or the sick count of the valuation date: each moves by the
    same factor.  So each point in force on the committed table is restated a month on,
    opened with what this model carries into its month 1: the count,
    ``pols_if_at(1, "BEF_NB")``, the healthy share and the cohorts at the start of month 1,
    over that count, and the benefit and premium of month 0, entering month 1.  The
    restatement must continue the point's own frames, its row ``t`` the point's row
    ``t + 1``, in ``result_cf``, ``result_states`` and ``result_pols``, every flow among
    them, to 1e-9 relative, floored at 1e-9 for what a state read back from the CSV an ulp
    off moves about 0.  The point valued on its first anniversary takes no step at its
    restated month 0, and the one valued a month before an anniversary steps there.  Both
    models run at an inflation rate of 0, set on each as it is read (K7): the restatement
    moves the valuation date a month on, and expense inflation, on the valuation clock,
    would step a month apart by design (D7).  The restatement also shows the opening state
    complete on this model's own states, as the splice shows it on S's.  Each point is
    released once read (``_release``), since a point forms its cohorts a cell an element in
    modelx, and a model holding every point in force at once holds gigabytes.  The default
    run takes the core's points in force (:data:`CORE_POINTS`), on both bases and in
    claim, and the full grid the rest.
    """
    table = _committed()
    model = mx.read_model(_sec_inputs(tmp_path / "base", table), name=_name("month_on"))
    model.Projection.inflation_rate = 0.0
    rows, held, pairs, frames = [], [_committed_cohorts()], [], {}
    try:
        top = table.index.max()
        for label in table.index[table["duration_mth"] > 0]:
            if not _on_grid(grid, label):
                continue
            p = _point(model, label)
            if p.proj_len() >= 2:
                top += 1
                state, cohorts = _restated_a_month_on(p, top)
                row = table.loc[[label]].assign(**state)
                row.index = pd.Index([top], name="point_id")
                rows.append(row)
                held.append(cohorts)
                pairs.append((label, top))
                frames[label] = {report: p.cells[report]()
                                 for report in ("result_cf", "result_states", "result_pols")}
            del p
            _release(model, _key(model, label))
    finally:
        model.close()
    assert len(pairs) >= (3 if grid == "core" else 10), pairs
    restated = mx.read_model(_sec_inputs(tmp_path / "on", pd.concat([table, *rows]),
                                         pd.concat(held, ignore_index=True)),
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
            del p
            _release(restated, _key(restated, moved))
    finally:
        restated.close()
    assert not found, found[:20]


@pytest.mark.parametrize("grid", GRIDS)
def test_the_checks_close_on_ten_million_policies(tmp_path, grid):
    """``check_pols_roll_fwd`` and ``check_states`` scale their tolerance with the
    policies on the books, and close at 1e7.

    A residual is rounding on that many policies, so each check holds it to 1e-10 times
    ``max(policy_count(), 1)``, where its tolerance unscaled would be 1e-10: at the counts
    the other tests use, one policy or less, the two are one.  ``IP_UK_S`` scales by
    ``pols_if_init()``, which here is 0 on a point issued at the valuation date, the count
    entering as new business.  So every committed point is projected from a copy where
    each counts ten million policies: both checks close on each, and the largest residual
    of each check exceeds the unscaled 1e-10 on some point, so the scaling is what closes
    it (USLIB-SEC-PLAN.md §5.2, T4, precised at M10).

    The default run takes :data:`CORE_POINTS`, the point issued later among them, and the
    full grid the other committed points.
    """
    table = _committed().assign(policy_count=1e7)
    model = mx.read_model(_sec_inputs(tmp_path, table), name=_name("ten_million"))
    largest = {"check_pols_roll_fwd_resid": 0.0, "check_states_resid": 0.0}
    try:
        for key, point_id in zip(point_keys(model), table.index):
            if not _on_grid(grid, point_id):
                continue
            p = projection(model, key)
            assert p.check_pols_roll_fwd() and p.check_states(), point_id
            for resid in largest:
                largest[resid] = max(largest[resid], max(
                    abs(p.cells[resid](t)) for t in range(p.proj_len())))
            _release(model, key)
    finally:
        model.close()
    assert all(value > 1e-10 for value in largest.values()), largest


# ---------------------------------------------------------------------------
# T5 -- validation
#
# Each malformed table is the committed one with one fault.  The checks run over the whole
# table as it is read, in Data, and the message names the file it read and the column or
# every point at fault.  A blank cell reads as NaN, and so does a text cell once the checks
# coerce the column to numbers, so each is refused as a count, a duration or a state that
# is not a number.  The repeated point_id holds another policy under the same label, as a
# bad extract would, so that the check must look at the labels and not at whole rows.  The
# point_ids are the committed table's: 1 to 7 the twins of S's points, 2, 5 and 7 in claim
# on their policy clocks of 12, 36 and 12 months; 8, the anchor cell on its first
# anniversary; 9, at 60; 10, at 359; 11, the claim from duration 0 at 24; 12, the claim
# from duration 30 at 6; 13, the claim on the active-lives basis at 12; 14, the female cell
# at 13; 15, the older male cell at 118; 16, the level cell at 30; 17, the female cell issued
# 13 months on; 18, the anchor cell at 40 under an RPI of 5%; 19, the female cell at 30
# under 12%.  A {file} in a message is the table's filename: every case is read by one
# model, from a file of its own (the malformed fixture).


def _drop(column):
    return lambda table: table.drop(columns=column)


_NOT_YET = "on a policy not yet in force, duration_mth 0 or less; it is not at point_id"
_FIRST_YEAR = ("on a policy in force 12 months or fewer, whose amounts are its first policy "
               "year's, the first anniversary's increase being the projection's; it is not "
               "at point_id")
_LEVEL = "on a point without escalation, which never escalates; it is not at point_id"
_RPI = ("or more, to half a cent, on a point with RPI escalation, each increase being "
        "floored at 0; it is not at point_id")
_SHARE_RULE = "must be a number from 0 to 1, a share of the count; it is not at point_id"

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
    ("a fractional duration", _set("duration_mth", [9], 60.5),
     "{file}: duration_mth must be a whole number of months; it is not at point_id [9]"),
    ("a blank duration", _set("duration_mth", [17], float("nan")),
     "{file}: duration_mth must be a whole number of months; it is not at point_id [17]"),
    ("a text duration", _set("duration_mth", [11], "x36"),
     "{file}: duration_mth must be a whole number of months; it is not at point_id [11]"),
    # numpy casts a float past int64 to the least int64, a policy issued 2**63 months on,
    # without a word: the table refuses it first.
    ("a duration past int64", _set("duration_mth", [8], 1e19),
     "{file}: duration_mth must be below 2**53 months; it is not at point_id [8]"),
    ("durations of 2**53 months at two points", _set("duration_mth", [8, 10], 2.0 ** 53),
     "{file}: duration_mth must be below 2**53 months; it is not at point_id [8, 10]"),
    ("issued beyond the horizon", _set("duration_mth", [17], -121),
     "{file}: duration_mth must be -120 or more, a policy issued at most 120 months after "
     "the valuation date; it is not at point_id [17]"),
    *[(f"no {column} column", _drop(column), f"{{file}} has no {column} column")
      for column in ("policy_count", "duration_mth", *STATE, *S_COLUMNS_READ)],
    ("a repeated point_id",
     lambda t: pd.concat([t, t.loc[[8]].assign(policy_id="IP-900099")]),
     "{file}: point_id [8] appears more than once"),
    ("a negative healthy share", _set("pols_active_init", [9], -0.01),
     f"{{file}}: pols_active_init {_SHARE_RULE} [9]"),
    ("a healthy share past 1", _set("pols_active_init", [9], 1.01),
     f"{{file}}: pols_active_init {_SHARE_RULE} [9]"),
    ("a blank healthy share", _set("pols_active_init", [13], float("nan")),
     f"{{file}}: pols_active_init {_SHARE_RULE} [13]"),
    ("a text healthy share", _set("pols_active_init", [16], "most"),
     f"{{file}}: pols_active_init {_SHARE_RULE} [16]"),
    ("an infinite healthy share", _set("pols_active_init", [9], float("inf")),
     f"{{file}}: pols_active_init {_SHARE_RULE} [9]"),
    ("a negative benefit", _set("benefit_pp_init", [9], -1.0),
     "{file}: benefit_pp_init must be a number, zero or more; it is not at point_id [9]"),
    ("a blank benefit", _set("benefit_pp_init", [14], float("nan")),
     "{file}: benefit_pp_init must be a number, zero or more; it is not at point_id [14]"),
    ("a text benefit", _set("benefit_pp_init", [18], "high"),
     "{file}: benefit_pp_init must be a number, zero or more; it is not at point_id [18]"),
    ("an infinite benefit", _set("benefit_pp_init", [10], float("inf")),
     "{file}: benefit_pp_init must be a number, zero or more; it is not at point_id [10]"),
    ("a negative premium", _set("premium_pp_init", [14], -1.0),
     "{file}: premium_pp_init must be a number, zero or more; it is not at point_id [14]"),
    ("a blank premium", _set("premium_pp_init", [9], float("nan")),
     "{file}: premium_pp_init must be a number, zero or more; it is not at point_id [9]"),
    ("an infinite premium", _set("premium_pp_init", [19], float("inf")),
     "{file}: premium_pp_init must be a number, zero or more; it is not at point_id [19]"),
    ("an unknown sex", _set("sex", [1], "X"),
     "{file}: sex must be M or F; it is not at point_id [1]"),
    ("an unknown escalation", _set("escalation", [4], "LPI"),
     "{file}: escalation must be RPI or none; it is not at point_id [4]"),
    # IP_UK_S checks the premium basis in a cell no formula calls, so it projects a
    # reviewable premium as guaranteed.
    ("a reviewable premium", _set("premium_basis", [3], "reviewable"),
     "{file}: premium_basis must be guaranteed; it is not at point_id [3]"),
    ("an unknown status", _set("status", [2], "claim"),
     "{file}: status must be active or in_claim; it is not at point_id [2]"),
    ("an unknown recovery basis", _set("recovery_basis", [7], "return"),
     "{file}: recovery_basis must be return_to_h or exit; it is not at point_id [7]"),
    ("an occupation class of 5", _set("occ_class", [1], 5),
     "{file}: occ_class must be a whole number from 1 to 4; it is not at point_id [1]"),
    ("an occupation class of 0", _set("occ_class", [6], 0),
     "{file}: occ_class must be a whole number from 1 to 4; it is not at point_id [6]"),
    ("an occupation class not whole", _set("occ_class", [4], 2.5),
     "{file}: occ_class must be a whole number from 1 to 4; it is not at point_id [4]"),
    ("an occupation class written as text", _set("occ_class", [3], "OC1"),
     "{file}: occ_class must be a whole number from 1 to 4; it is not at point_id [3]"),
    ("a blank occupation class", _set("occ_class", [5], float("nan")),
     "{file}: occ_class must be a whole number from 1 to 4; it is not at point_id [5]"),
    ("a deferred period off the menu", _set("deferred_weeks", [1], 6),
     "{file}: deferred_weeks must be 4, 8, 13, 26 or 52; it is not at point_id [1]"),
    ("a blank deferred period", _set("deferred_weeks", [4], float("nan")),
     "{file}: deferred_weeks must be 4, 8, 13, 26 or 52; it is not at point_id [4]"),
    ("a deferred period written as text", _set("deferred_weeks", [6], "26w"),
     "{file}: deferred_weeks must be 4, 8, 13, 26 or 52; it is not at point_id [6]"),
    ("a blank entry age", _set("entry_age", [1], float("nan")),
     "{file}: entry_age must be a finite number; it is not at point_id [1]"),
    ("an infinite entry age", _set("entry_age", [5], float("inf")),
     "{file}: entry_age must be a finite number; it is not at point_id [5]"),
    ("a text entry age", _set("entry_age", [7], "x34"),
     "{file}: entry_age must be a finite number; it is not at point_id [7]"),
    ("an entry age of 2**53", _set("entry_age", [3], 2.0 ** 53),
     "{file}: entry_age must be below 2**53 in size; it is not at point_id [3]"),
    ("a blank expiry age", _set("expiry_age", [6], float("nan")),
     "{file}: expiry_age must be a finite number; it is not at point_id [6]"),
    ("a text expiry age", _set("expiry_age", [2], "65y"),
     "{file}: expiry_age must be a finite number; it is not at point_id [2]"),
    ("a negative benefit at issue", _set("benefit_mth", [1], -1.0),
     "{file}: benefit_mth must be a number, zero or more; it is not at point_id [1]"),
    ("text earnings", _set("earnings_annual", [4], "40k"),
     "{file}: earnings_annual must be a number, zero or more; it is not at point_id [4]"),
    ("an infinite premium at issue", _set("premium_mth", [6], float("inf")),
     "{file}: premium_mth must be a number, zero or more; it is not at point_id [6]"),
    ("lives in claim on new business", _set("pols_active_init", [1], 0.9),
     "{file}: pols_active_init must be 1 on a policy not yet in force, duration_mth 0 or "
     "less, which is issued healthy; it is not at point_id [1]"),
    ("lives in claim on future business", _set("pols_active_init", [17], 0.0),
     "{file}: pols_active_init must be 1 on a policy not yet in force, duration_mth 0 or "
     "less, which is issued healthy; it is not at point_id [17]"),
    ("a benefit on new business", _set("benefit_pp_init", [3], 2100.0),
     f"{{file}}: benefit_pp_init must be the benefit at issue {_NOT_YET} [3]"),
    ("a premium on future business", _set("premium_pp_init", [17], 60.0),
     f"{{file}}: premium_pp_init must be the premium at issue {_NOT_YET} [17]"),
    # No anniversary has passed in a policy's first twelve months: the female cell at 13,
    # moved back to its first anniversary with its first increase, and the anchor cell on
    # its first anniversary given the increase that anniversary makes, read after month
    # 0's step, where the columns are measured before it.
    ("a benefit in the first policy year", _set("duration_mth", [14], 12),
     f"{{file}}: benefit_pp_init must be the benefit at issue {_FIRST_YEAR} [14]"),
    ("a benefit on the first anniversary", _set("benefit_pp_init", [8], 2060.0),
     f"{{file}}: benefit_pp_init must be the benefit at issue {_FIRST_YEAR} [8]"),
    ("a premium on the first anniversary", _set("premium_pp_init", [8], 36.575),
     f"{{file}}: premium_pp_init must be the premium at issue {_FIRST_YEAR} [8]"),
    # The first year's history at its first month: an increase a month after issue.
    ("a premium a month after issue",
     _then(_set("duration_mth", [8], 1), _set("premium_pp_init", [8], 36.575)),
     f"{{file}}: premium_pp_init must be the premium at issue {_FIRST_YEAR} [8]"),
    ("a level benefit moved", _set("benefit_pp_init", [16], 2001.0),
     f"{{file}}: benefit_pp_init must be the benefit at issue {_LEVEL} [16]"),
    ("a level premium moved", _set("premium_pp_init", [16], 35.5),
     f"{{file}}: premium_pp_init must be the premium at issue {_LEVEL} [16]"),
    ("a level claim's benefit moved", _set("benefit_pp_init", [11], 2060.0),
     f"{{file}}: benefit_pp_init must be the benefit at issue {_LEVEL} [11]"),
    # An escalated amount a cent below the amount at issue, which half a cent's slack, for
    # an extract rounded to the cent, does not admit.
    ("an escalated benefit a cent below the benefit at issue",
     _set("benefit_pp_init", [9], 1999.99),
     f"{{file}}: benefit_pp_init must be the benefit at issue {_RPI} [9]"),
    ("an escalated premium a cent below the premium at issue",
     _set("premium_pp_init", [9], 34.99),
     f"{{file}}: premium_pp_init must be the premium at issue {_RPI} [9]"),
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
    """``message`` with every point it names relabelled by ``relabel``, a label it does not
    hold left as it is: each ``point_id [...]`` list, and each ``point_id p z``, the
    companion's key."""
    def one(p):
        return str(relabel.get(int(p), int(p)))

    def labels(match):
        return "point_id [" + ", ".join(one(p) for p in match.group(1).split(", ")) + "]"
    message = re.sub(r"point_id \[(\d+(?:, \d+)*)\]", labels, message)
    return re.sub(r"point_id (\d+) z ", lambda m: f"point_id {one(m.group(1))} z ", message)


# The labels an extract carries in the tests below: the committed points' in reverse, from
# 100 plus their number down to 101, so that a label is neither a position plus one nor in
# the order of the rows.
EXTRACT_LABELS = tuple(range(100 + len(_committed()), 100, -1))


def _relabel_map():
    """``{committed label: extract label}``."""
    return dict(zip(_committed().index, EXTRACT_LABELS))


@pytest.fixture(scope="module")
def malformed_extract(tmp_path_factory):
    """:data:`MALFORMED`'s tables as an extract labels its rows, each a file of its own.

    Each case's table is the committed one with its fault, made by its own labels, and
    then relabelled :data:`EXTRACT_LABELS`, in order, so that no label is its position
    plus one.  One model reads them all, as :func:`malformed` reads its files.  Returns
    ``(model, {case: filename}, {committed label: extract label})``.
    """
    root = tmp_path_factory.mktemp("malformed_extract")
    relabel = _relabel_map()
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


def _cell(row, column, value):
    """An edit that writes ``value`` into ``column`` on row ``row``, line ``row + 2``."""
    def edit(table):
        cells = table[column].astype(object)
        cells.iloc[row] = value
        return table.assign(**{column: cells})
    return edit


def _extra(**row):
    """An edit that appends a row of its own, on the line after the last."""
    return lambda table: pd.concat([table, pd.DataFrame([row])], ignore_index=True)


def _without(point):
    """An edit that drops every row of ``point``."""
    return lambda table: table[table["point_id"] != point].reset_index(drop=True)


def _sum_off(point, by):
    """An edit that moves ``point``'s largest cohort share by ``by``, so that its shares
    and its healthy share sum to ``1 + by``, within the float of it."""
    def edit(table):
        table = table.copy()
        mine = table.index[table["point_id"] == point]
        at = table.loc[mine, "pols_sick_dur_init"].idxmax()
        table.loc[at, "pols_sick_dur_init"] = table.at[at, "pols_sick_dur_init"] + by
        return table
    return edit


def _past_one(points):
    """What ``Data.inforce_cohorts()`` says of ``points``, whose shares do not sum to 1."""
    return (f"{{file}}: a point's pols_active_init and its pols_sick_dur_init must sum to "
            f"1 within 1e-10, shares of one count; they do not at point_id {points}")


_Z_RANGE = ("{file}: z must be from 1 to its point's duration_mth, the months since issue "
            "at the valuation date; it is not on line ")
_IN_FORCE = ("{file}: a row's point must be in force, duration_mth above 0: a point not yet "
             "in force is issued healthy; it is not on line ")
_COHORT_SHARE = ("{file}: pols_sick_dur_init must be a number from 0 to 1, a share of the "
                 "count; it is not on line ")

# The claim cohorts with one fault each, as (case, the edit of the committed file, the
# message), {file} in a message the companion's filename.  The committed file holds, by
# line, the header line 1: the twins of S's claims, point 2's cohort z 1 on line 2, point
# 5's z 31 on line 3 and point 7's z 1 on line 4; point 8's cohorts z 1 to 12 on lines 5 to
# 16; point 9's z 1 to 60 on lines 17 to 76; point 10's, 359 of them, on lines 77 to 435;
# point 11's z 25 on line 436; point 12's z 37 on line 437; point 13's z 1 to 11 and 13 on
# lines 438 to 449; then points 14, 15, 16, 18 and 19, to line 680.
MALFORMED_COHORTS = [
    *[(f"no {column} column", (lambda t, c=column: t.drop(columns=c)),
       f"{{file}} has no {column} column")
      for column in ("point_id", "z", "pols_sick_dur_init")],
    ("a fractional point_id", _cell(0, "point_id", 2.5),
     "{file}: point_id must be a whole number; it is not on line [2]"),
    ("a text z", _cell(1, "z", "thirty-one"),
     "{file}: z must be a whole number; it is not on line [3]"),
    ("a blank z", _cell(7, "z", float("nan")),
     "{file}: z must be a whole number; it is not on line [9]"),
    ("a z past int64", _cell(2, "z", 1e19),
     "{file}: z must be below 2**53 in size; it is not on line [4]"),
    ("a point the table lacks", _extra(point_id=99, z=1, pols_sick_dur_init=0.0),
     f"{{file}}: point_id [99] on line [681] is no point of {TABLE}"),
    ("a z twice", _extra(point_id=9, z=5, pols_sick_dur_init=0.0),
     "{file}: each point_id and z must have one row; point_id 9 z 5 is on line [21, 681]"),
    ("a claim on new business", _extra(point_id=1, z=1, pols_sick_dur_init=0.0),
     _IN_FORCE + "[681]"),
    ("a claim on future business", _extra(point_id=17, z=1, pols_sick_dur_init=0.0),
     _IN_FORCE + "[681]"),
    ("a z of 0", _cell(0, "z", 0), _Z_RANGE + "[2]"),
    ("a claim older than its policy", _cell(0, "z", 13), _Z_RANGE + "[2]"),
    ("a claim duration past the policy's at a later point",
     _extra(point_id=12, z=43, pols_sick_dur_init=0.0), _Z_RANGE + "[681]"),
    ("a negative cohort share", _cell(4, "pols_sick_dur_init", -0.01),
     _COHORT_SHARE + "[6]"),
    ("a cohort share past 1", _cell(8, "pols_sick_dur_init", 1.5),
     _COHORT_SHARE + "[10]"),
    ("a blank cohort share", _cell(9, "pols_sick_dur_init", float("nan")),
     _COHORT_SHARE + "[11]"),
    ("an infinite cohort share", _cell(3, "pols_sick_dur_init", float("inf")),
     _COHORT_SHARE + "[5]"),
    # The shares' tolerance, 1e-10, pinned from outside on each side; the edges test
    # accepts each side just inside it.
    ("shares past 1 by 1.1e-10", _sum_off(13, 1.1e-10), _past_one([13])),
    ("shares short of 1 by 1.1e-10", _sum_off(9, -1.1e-10), _past_one([9])),
    ("a claim's cohort lost", _without(11), _past_one([11])),
    ("one of several cohorts lost",
     lambda t: t.drop(index=t.index[(t["point_id"] == 13) & (t["z"] == 13)]).reset_index(
         drop=True), _past_one([13])),
    ("two points' shares off", _then(_sum_off(13, 1e-3), _sum_off(18, 1e-6)),
     _past_one([13, 18])),
]


@pytest.fixture(scope="module")
def malformed_cohorts(tmp_path_factory):
    """One model, and beside it every companion of :data:`MALFORMED_COHORTS`, each a file
    of its own, read as the committed table's claim cohorts in turn; and the same as an
    extract labels its rows, table and companion relabelled alike
    (:data:`EXTRACT_LABELS`).  Returns ``{"committed": (model, files), "extract": (model,
    files, relabel)}``.
    """
    root = tmp_path_factory.mktemp("malformed_cohorts")
    relabel = _relabel_map()
    out = {}
    for tag in ("committed", "extract"):
        files = {}
        for number, (case, edit, _) in enumerate(MALFORMED_COHORTS):
            files[case] = f"{tag}_cohorts_{number:02d}_sec.csv"
            frame = edit(_committed_cohorts())
            if tag == "extract" and "point_id" in frame:
                frame = frame.assign(point_id=frame["point_id"].map(
                    lambda p: relabel.get(p, p)))
            temp_inputs(root / tag, model_path(SEC), model_points=frame,
                        model_point_file=files[case])
        # Last, since each copy writes the committed CSVs over the folder's.
        table = _committed() if tag == "committed" else _committed().rename(index=relabel)
        temp_inputs(root / tag, model_path(SEC), model_points=table, model_point_file=TABLE)
        model = mx.read_model(root / tag / SEC, name=_name(f"cohorts_{tag}"))
        out[tag] = (model, files)
    out["extract"] = (*out["extract"], relabel)
    yield out
    for tag in ("committed", "extract"):
        out[tag][0].close()


@pytest.mark.parametrize("case, edit, message", MALFORMED_COHORTS,
                         ids=[c[0] for c in MALFORMED_COHORTS])
def test_malformed_claim_cohorts_are_refused_naming_their_lines(malformed_cohorts, case,
                                                                 edit, message):
    """``Data.inforce_cohorts()`` refuses the companion, naming the fault and its lines or
    its points, and so does a projection of a point in force that reads it (D6, D8, T5);
    and on an extract labelled otherwise, table and companion alike, each refusal names the
    extract's labels.

    The checks are :func:`IP_UK_SEC.Data.inforce_cohorts`'s eight rules: the columns; keys
    whole and below ``2**53``; a point of the table; one row a point and duration; a point
    in force, since a point not yet in force is issued healthy; a duration from 1 to the
    point's months in force; a share from 0 to 1; and the healthy share and the cohort
    shares summing to 1 within 1e-10, on every point in force, a point holding no row
    among them, which is all healthy.  ``IP_UK_S`` has no companion: it seeds one cohort
    from its ``claim_duration_months``.
    """
    model, files = malformed_cohorts["committed"]
    model.Data.inforce_cohorts_file = files[case]
    _refused(model.Data.inforce_cohorts, message.format(file=files[case]))
    _refused(_point(model, 9).result_cf, message.format(file=files[case]))
    model, files, relabel = malformed_cohorts["extract"]
    model.Data.inforce_cohorts_file = files[case]
    _refused(model.Data.inforce_cohorts,
             _relabelled(message, relabel).format(file=files[case]))


def test_the_future_horizon_is_a_reference_that_bounds_future_business(tmp_path):
    """``Data.future_horizon_mth`` refuses a policy issued later than it, and 0 refuses all.

    The committed table's one future point is issued 13 months on.  It reads at the shipped
    120 months and at 13, the shortest horizon that admits it, and is refused at 12, by
    name.  At 0 the model takes no future new business, D4's fallback for a product that
    cannot support it, and the message says so.  A horizon that is not a whole number of
    months, 0 or more, below ``2**53``, is itself refused, a NaN and an infinity among
    them: either would admit every policy.  It ships as a float, ``120.0``, which a compiled
    model holds as a double, so that 12.5 is refused there as here (``Data``'s docstring),
    and the refusal prints it as a float, as the compiled model holds it, whether set as an
    int or a float.  A whole number written as an int, ``13``, reads as 13.0 does, and
    ``2**53 - 1``, the largest whole number a double holds with every smaller one, reads;
    ``2**53`` does not.  Setting the Reference clears the table, so each value is read
    afresh.
    """
    future = _label(_committed(), "future", 4, -13)
    later = (f"{TABLE}: duration_mth must be -12 or more, a policy issued at most 12 months "
             f"after the valuation date; it is not at point_id [{future}]")
    no_future = (f"{TABLE}: duration_mth must be 0 or more: this model takes no future new "
                 f"business; it is not at point_id [{future}]")
    model = mx.read_model(_sec_inputs(tmp_path, _committed()), name=_name("horizon"))
    try:
        assert model.Data.future_horizon_mth == 120
        assert type(model.Data.future_horizon_mth) is float
        off = ("future_horizon_mth must be a whole number of months, 0 or more, below "
               "2**53, not {}")
        for horizon, refusal in ((13, None), (12, later), (0, no_future), (13.0, None),
                                 *((h, off.format(float(h))) for h in (
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


def test_a_point_past_its_policy_end_date_is_refused_by_proj_len(tmp_path):
    """A point at or past its policy end date has no frame, and ``proj_len()`` refuses it.

    The anchor cell valued at 60 is moved on to ``duration_mth`` 360, the policy month
    cover ends at, from entry at 35 to expiry at 65, on the policy clock.  That is a rule of
    the product, not of the table: it needs the expiry age and the entry age the point's
    own columns give, read where the frame is defined, so the table and its cohorts read,
    and the point is refused on its first projection, rather than projecting nothing.  A
    loop over the block would meet the point only when it reached it, after projecting the
    points before it, so ``run_sec.py --block``, run beside the table, asks every point for
    its frame first: it fails naming the point, and prints nothing before.  And one month
    earlier, 359, the last covered month, projects one month.
    """
    moved = _label(_committed(), "derived", 1, 60)
    model = _read_edited(tmp_path, _set("duration_mth", [moved], 360))
    message = (f"point_id {moved}: duration_mth 360 is at or past the policy end date, "
               f"policy month 360, expiry age 65")
    try:
        assert len(model.Data.model_point_table()) == len(_committed())
        assert len(model.Data.inforce_cohorts()) == len(_committed_cohorts())
        _refused(_point(model, moved).result_cf, message)
    finally:
        model.close()
    model = _read_edited(tmp_path / "last", _set("duration_mth", [moved], 359))
    try:
        assert len(_point(model, moved).result_cf()) == 1
    finally:
        model.close()
    runner = tmp_path / "run_sec.py"
    shutil.copy(model_path(SEC).parent / "run_sec.py", runner)
    done = _run_sec(runner, "--block", check=False)
    assert done.returncode != 0 and done.stdout == b""
    assert message in done.stderr.decode(errors="replace")


# What the contract does not issue, refused by proj_len() as a point past its policy end date
# is, as (case, the table's edit, the References set, the point, the message, and the frame
# the point projects at the shipped References, or None).  Data reads an entry and an expiry
# age as IP_UK_S does, so each reads.  The product issues from 18 to 59 and expires from 50
# to 70; the compiled caches will be sized from the youngest issue and the latest expiry.
# Each bound is refused just past it here, and accepted at it in the edges test.  And each
# bound, moved past a committed twin, refuses it, which at the shipped bound projects its
# frame: the Reference is what refuses it.  Point 1 is the anchor cell, issued at 35 to 65;
# point 4 the female cell at 42 to 60; point 6 the older male cell at 55 to 65.
NOT_ISSUED = [
    ("an issue age of 17", _set("entry_age", [3], 17), {}, 3,
     "point_id 3: the issue age, 17, is below issue_age_min, 18", None),
    ("an issue age of 60", _set("entry_age", [6], 60), {}, 6,
     "point_id 6: the issue age, 60, is above issue_age_max, 59", None),
    ("an issue age below a bound raised to 36", None, {"issue_age_min": 36}, 1,
     "point_id 1: the issue age, 35, is below issue_age_min, 36", 360),
    ("an issue age above a bound lowered to 54", None, {"issue_age_max": 54}, 6,
     "point_id 6: the issue age, 55, is above issue_age_max, 54", 120),
    ("an expiry age of 49", _set("expiry_age", [4], 49), {}, 4,
     "point_id 4: the expiry age, 49, is below expiry_age_min, 50", None),
    ("an expiry age of 71", _set("expiry_age", [1], 71), {}, 1,
     "point_id 1: the expiry age, 71, is above expiry_age_max, 70", None),
    ("an expiry age below a bound raised to 61", None, {"expiry_age_min": 61}, 4,
     "point_id 4: the expiry age, 60, is below expiry_age_min, 61", 216),
    ("an expiry age above a bound lowered to 64", None, {"expiry_age_max": 64}, 1,
     "point_id 1: the expiry age, 65, is above expiry_age_max, 64", 360),
    ("an issue age at the expiry age", _then(_set("entry_age", [6], 55),
                                             _set("expiry_age", [6], 55)), {}, 6,
     "point_id 6: the issue age, 55, is at or past the expiry age, 55: the policy has no "
     "cover", None),
    # A contract moved past the compiled caches, which stage E projects: a cover longer
    # than 624 months, the expiry bound raised to 71 or the issue bound lowered to 17, and a
    # frame longer than 744, the horizon lengthened to 121 months.  Each would read a claim
    # duration or a month past the compiled caches, so proj_len() refuses it in either
    # engine (M8), naming the point.
    ("a cover past the caches, the expiry bound raised to 71",
     _then(_set("entry_age", [1], 18), _set("expiry_age", [1], 71)),
     {"expiry_age_max": 71}, 1,
     "point_id 1: its cover, 636 months from issue at 18 to expiry at 71, is longer than "
     "624, the longest the compiled model's caches are sized for (spec_sec.py)", None),
    ("a cover past the caches, the issue bound lowered to 17",
     _then(_set("entry_age", [1], 17), _set("expiry_age", [1], 70)),
     {"issue_age_min": 17}, 1,
     "point_id 1: its cover, 636 months from issue at 17 to expiry at 70, is longer than "
     "624, the longest the compiled model's caches are sized for (spec_sec.py)", None),
    ("a frame past the caches, the horizon lengthened to 121",
     _then(_set("entry_age", [17], 18), _set("expiry_age", [17], 70),
           _set("duration_mth", [17], -121)),
     {"Data.future_horizon_mth": 121}, 17,
     "point_id 17: its frame, 745 months from the valuation date, is longer than 744, the "
     "longest the compiled model's caches are sized for (spec_sec.py)", None),
]


@pytest.mark.parametrize("case, edit, refs, point, message, frame", NOT_ISSUED,
                         ids=[c[0] for c in NOT_ISSUED])
def test_a_point_the_contract_does_not_issue_is_refused_by_proj_len(tmp_path, case, edit,
                                                                    refs, point, message,
                                                                    frame):
    """``proj_len()`` refuses a point outside the contract's bounds, naming it (§6.3).

    ``IP_UK_S`` projects any entry age to any expiry age its tables reach, and so would
    modelx here, but the contract does not write it, and the compiled model's caches are
    sized from the contract: a frame of at most 52 years and the horizon, claim durations
    to 625 months, attained ages from 18 to 69.  So the frame refuses such a point, naming
    it, as it refuses a point past its policy end date, and every report with it
    (:data:`NOT_ISSUED`): each bound just past it, and each bound moved past a committed
    twin, which projects at the shipped bound, on a model read afresh.  A bound off by one,
    or a refusal lost, lets a point through.  And a contract moved past the caches, its
    bounds or ``Data``'s horizon set past the shipped ones, is refused for a point whose
    cover or frame would pass them, in either engine, which stage E projected: the
    compiled model would read past a cache, and raise ``IndexError`` alone.  The table
    reads either way.  Every Reference is set on a model just read, before its projection
    computes anything (K7), ``Data``'s named ``"Data.<name>"``.  Each case runs on an
    extract labelled otherwise than by position (:func:`_read_extract`), and its refusal
    must begin by naming the point by the extract's label, as every refusal does, so that
    one naming a point by its place in the table, ``idx + 1``, fails here (M8's review).
    """
    model = _read_extract(tmp_path, edit)
    label = _relabel_map()[point]
    try:
        for ref, value in refs.items():
            if ref.startswith("Data."):
                setattr(model.Data, ref[len("Data."):], value)
            else:
                setattr(model.Projection, ref, value)
        assert len(model.Data.model_point_table()) == len(_committed())
        _refused_naming(_point(model, label).result_cf, _as_extract(message), label)
    finally:
        model.close()
    if frame is not None:
        shipped = mx.read_model(model_path(SEC), name=_name("bound"))
        try:
            assert len(_point(shipped, point).result_cf()) == frame
        finally:
            shipped.close()


def _raised_by(amount, rise, years):
    """``amount`` raised by ``rise`` at each of ``years`` anniversaries, multiplied in turn,
    as proj_len() multiplies it."""
    for _ in range(years):
        amount = amount * rise
    return amount


# The escalation history of the anchor cell in force at 60, point 9, its four anniversaries
# before the valuation date each raising the benefit by an increase j from 0 to the cap,
# 10%, and the premium by 1.5 j.  At the cap each time, the benefit and premium of
# TOP_BENEFIT and TOP_PREMIUM; at 5% each time, the history IP_UK_S gives at an RPI of 5%,
# 2,000 x 1.05^4 beside the most premium that benefit allows, 35 x 1.075^4, its increases
# equal; and beside that benefit the least premium it allows, its increases made at the
# cap twice and once part-way (proj_len()).
TOP_BENEFIT = _raised_by(2000.0, 1.0 + 0.1, 4)
TOP_PREMIUM = _raised_by(35.0, 1.0 + 1.5 * 0.1, 4)
BENEFIT_5 = 2000.0 * 1.05 ** 4
PREMIUM_5 = 35.0 * (1.0 + 1.5 * 0.05) ** 4
LEAST_PREMIUM_5 = 35.0 * 1.15 ** 2 * (1.0 + 1.5 * (1.05 ** 4 / 1.1 ** 2 - 1.0))

# What proj_len() says of a history past a bound, in parts, each of which the message must
# hold: the amount read back is left out, since the CSV may return a computed float two
# ulps off.
_BENEFIT_PAST = ("point_id 9: benefit_pp_init ",
                 f" is above {TOP_BENEFIT}, the benefit at issue, 2000.0, increased by "
                 f"esc_cap, 0.1, at each of the 4 anniversaries before the valuation date, "
                 f"by more than half a cent: no increase passes the cap")
_PREMIUM_PAST = ("point_id 9: premium_pp_init ",
                 f" is above {TOP_PREMIUM}, the premium at issue, 35.0, increased by "
                 f"esc_prem_mult times esc_cap, 1.5 x 0.1, at each of the 4 anniversaries "
                 f"before the valuation date, by more than half a cent")
def _outside(mult=1.5):
    """The parts of what proj_len() says of a premium outside the range its benefit's
    increases allow, at a premium multiplier of ``mult``."""
    return ("point_id 9: premium_pp_init ", " is outside ",
            ", by more than half a cent: the premiums its benefit's increases allow, from "
            "2000.0 to ", " over the 4 anniversaries before the valuation date, each "
            f"increase j of the benefit's raising the premium by esc_prem_mult x j, {mult} x j")


_OUTSIDE = _outside()

# The history's bounds, as (case, point 9's benefit and premium, the References set, the
# message's parts, or None where the history is accepted): each bound a cent outside, and
# half a cent inside, where an extract rounded to the cent may sit; the two states M7's
# review found the K14 tests opened with, a benefit risen faster than its premium and a
# premium faster than its benefit; and the committed history, at 3%, under a cap lowered to
# 2% and under a premium multiplier raised to 2, which the contract it was written under
# did not have.
HISTORY_BOUNDS = [
    ("a benefit a cent past the cap", (TOP_BENEFIT + 0.01, TOP_PREMIUM), {}, _BENEFIT_PAST),
    ("a benefit half a cent past the cap", (TOP_BENEFIT + 0.005, TOP_PREMIUM), {}, None),
    ("a premium a cent past the cap", (TOP_BENEFIT, TOP_PREMIUM + 0.01), {}, _PREMIUM_PAST),
    ("a premium half a cent past the cap", (TOP_BENEFIT, TOP_PREMIUM + 0.005), {}, None),
    ("a premium a cent above the most its benefit allows", (BENEFIT_5, PREMIUM_5 + 0.01),
     {}, _OUTSIDE),
    ("a premium half a cent above the most its benefit allows",
     (BENEFIT_5, PREMIUM_5 + 0.005), {}, None),
    ("a premium a cent below the least its benefit allows",
     (BENEFIT_5, LEAST_PREMIUM_5 - 0.01), {}, _OUTSIDE),
    ("a premium half a cent below the least its benefit allows",
     (BENEFIT_5, LEAST_PREMIUM_5 - 0.005), {}, None),
    ("a benefit risen faster than its premium", (2400.0, 41.73815102187499), {}, _OUTSIDE),
    ("a premium risen faster than its benefit", (2251.01762, 45.0), {}, _OUTSIDE),
    ("the committed history past a cap lowered to 2%", (2251.01762, 41.73815102187499),
     {"esc_cap": 0.02},
     ("point_id 9: benefit_pp_init 2251.01762 is above "
      f"{_raised_by(2000.0, 1.0 + 0.02, 4)}, the benefit at issue, 2000.0, increased by "
      f"esc_cap, 0.02, at each of the 4 anniversaries",)),
    ("the committed history under a premium multiplier of 2",
     (2251.01762, 41.73815102187499), {"esc_prem_mult": 2.0}, _outside(2.0)),
    # Under a multiplier of 1e150 both of the premium's even paths leave the floats, the
    # least's and the most's, each power's OverflowError read as the cap's path, whose
    # premium is past the floats too, top_p: the bounds are 8.1e298 and inf.  Compiled,
    # each power is M22's form, Python's own power called where C's is infinite, inside the
    # except that reads it, so both engines take the same path (M8).
    ("the committed history under a premium multiplier of 1e150",
     (2251.01762, 41.73815102187499), {"esc_prem_mult": 1e150},
     ("point_id 9: premium_pp_init 41.73815102187499 is outside 8.115644090909081e+298 to "
      "inf, by more than half a cent",)),
]


@pytest.mark.parametrize("case, amounts, refs, message", HISTORY_BOUNDS,
                         ids=[c[0] for c in HISTORY_BOUNDS])
def test_the_escalation_history_is_bounded_by_the_contract(tmp_path, case, amounts, refs,
                                                           message):
    """``proj_len()`` refuses an escalation history the contract cannot have (§6.3).

    ``Data``'s rule 12 bounds an escalating point's benefit and premium from below, at the
    amounts at issue.  Above, the contract bounds them by References, which ``Data`` cannot
    see: no increase passes ``esc_cap``, and each raises the premium ``esc_prem_mult``
    times as much as the benefit, so a benefit of one increase bounds its premium on both
    sides, the premium having risen least when the benefit's increases fell at the cap,
    one part-way and the rest none, and most when they were equal.  So ``proj_len()``
    refuses each history outside them, naming the point, and the projection with it
    (:data:`HISTORY_BOUNDS`): each bound tried a cent outside, refused, and half a cent
    inside, accepted, the tolerance an extract rounded to the cent needs; the two
    histories M7's review found unreachable; and the committed history under a contract
    it was not written under, twice, the second under a premium multiplier whose even
    paths' powers leave the floats, reaching the guard each power has, M22's form, in the
    ``except`` that reads its overflow as the cap's path, which the compiled refusal test
    reaches compiled.  Each case reads the history back as written, within the two
    ulps the CSV's text can cost a computed float, and exactly where a case sits at a
    bound's edge computed alike, and sets its References on a model just read (K7).  Each
    runs on an extract labelled otherwise than by position (:func:`_read_extract`), and a
    refusal must begin by naming the point by the extract's label.
    """
    benefit, premium = amounts
    model = _read_extract(tmp_path, _then(_set("benefit_pp_init", [9], benefit),
                                          _set("premium_pp_init", [9], premium)))
    label = _relabel_map()[9]
    try:
        for ref, value in refs.items():
            setattr(model.Projection, ref, value)
        table = model.Data.model_point_table()
        read = (table.at[label, "benefit_pp_init"], table.at[label, "premium_pp_init"])
        assert read == pytest.approx(amounts, rel=1e-15, abs=0.0)
        if "half a cent past the cap" in case:
            assert read == amounts
        if message is None:
            assert len(_point(model, label).result_cf()) == 300
        else:
            with pytest.raises(Exception) as excinfo:
                _point(model, label).result_cf()
            text = str(excinfo.value)
            assert _raised(excinfo.value).startswith(
                f"ValueError: point_id {label}: "), text
            missing = [part for part in map(_as_extract, message) if part not in text]
            assert not missing, (missing, text)
    finally:
        model.close()


# Each Reference proj_len() holds to a domain, as (case, the References set, the point,
# the message where refused, and where an accepted edge takes a value past the floats, the
# refusal its report meets there).  NaN and the infinities are outside every domain.
# IP_UK_S reads the cycle overlay inside the inception cap's min and the recovery bound's
# min, which a NaN is lost through and a 0 divides by; the mortality factor inside the
# mortality cap's min, which reads an infinity as certain death; the RPI through a max and
# a min, max(rpi, 0.0) then the escalation cap, which read an infinity as no increase or as
# the cap; the cap as a bound written second, which a NaN cap is lost through; the lapse
# shock's threshold through a bound-first max, which a NaN is lost through; the shares and
# the expenses as weights, which below 0 or past 1 make a negative benefit, expense or rate;
# and the discount rate through a negative power, which at -1 divides by zero.  Each is
# refused at the nearest value outside each edge of its domain, and accepted at the edge
# itself, where its reports project in finite floats over the whole frame, but where the
# edge takes a value past the floats, which is refused where it first is.  The four age
# bounds are whole numbers below 2**53, which the compiled model holds as long long,
# printed through int() once whole: each is refused at a fraction and at exactly 2**53.
BIG = 1.7976931348623157e308
WHOLE = 2.0 ** 53
BELOW_0 = math.nextafter(0.0, -1.0)
ABOVE_0 = math.nextafter(0.0, 1.0)
ABOVE_1 = math.nextafter(1.0, 2.0)
BELOW_MINUS_1 = math.nextafter(-1.0, -2.0)
ABOVE_MINUS_1 = math.nextafter(-1.0, 0.0)


def _domain(ref, rule, point, accepted, refused, reports=None):
    """The DOMAINS cases of ``ref`` on ``point``: each of ``accepted`` projects, or meets
    the report refusal ``reports`` gives it, and each of ``refused`` is refused by the
    domain's ``rule``, and NaN and the infinities by it too."""
    message = f"point_id {point}: {ref} must be {rule}, not {{}}"
    reports = reports or {}
    cases = [(f"{ref}={value!r} on {point}", {ref: value}, point, None, reports.get(value))
             for value in accepted]
    return cases + [(f"{ref}={value!r} on {point}", {ref: value}, point,
                     message.format(float(value)), None)
                    for value in (*refused, math.nan, math.inf, -math.inf)]


def _whole_domain(ref, point, accepted, below=True):
    """The DOMAINS cases of an integer Reference: a whole number below 2**53, and 0 or more
    where ``below``, printed through int() once whole; each of ``accepted`` projects."""
    whole = f"point_id {point}: {ref} must be a whole number below 2**53, not {{}}"
    cases = [(f"{ref}={value!r} on {point}", {ref: value}, point, None, None)
             for value in accepted]
    if below:
        cases.append((f"{ref}=-1 on {point}", {ref: -1}, point,
                      f"point_id {point}: {ref} must be 0 or more, not -1", None))
    return cases + [(f"{ref}={value!r} on {point}", {ref: value}, point,
                     whole.format(float(value)), None)
                    for value in (0.5, 50.5, WHOLE, 1e300, math.nan, math.inf, -math.inf)]


_FINITE_0 = ("a finite number, 0 or more", (0.0, BIG), (BELOW_0,))
_SHARE = ("a number from 0 to 1", (0.0, 1.0), (BELOW_0, ABOVE_1))
_EXPIRY_MAX = ("point_id 1: expiry_age_max must be expiry_age_min, 50, or more, and at most "
               "76, a year past mort_table.csv's last age, not {}")
DOMAINS = [
    *_domain("cycle_factor", "a finite number above 0", 1, (ABOVE_0, BIG), (0.0,)),
    *_domain("mort_active_factor", *_FINITE_0[:1], 1, *_FINITE_0[1:]),
    *_domain("ap_ratio", *_SHARE[:1], 2, *_SHARE[1:]),
    *_domain("claim_severity", *_SHARE[:1], 2, *_SHARE[1:]),
    *_domain("rpi_rate", "a finite number", 1, (-BIG, BIG), ()),
    *_domain("esc_cap", *_FINITE_0[:1], 1, *_FINITE_0[1:]),
    *_domain("esc_prem_mult", *_FINITE_0[:1], 1, *_FINITE_0[1:],
             {BIG: "point_id 1: the premium premium_pp(12) is inf, not a finite number, "
                   "from premium_pp_init 35.0"}),
    *_domain("esc_lapse_slope", *_FINITE_0[:1], 1, *_FINITE_0[1:]),
    *_domain("esc_lapse_threshold", *_FINITE_0[:1], 1, *_FINITE_0[1:]),
    *_domain("ben_band1_rate", *_SHARE[:1], 6, *_SHARE[1:]),
    *_domain("ben_band2_rate", *_SHARE[:1], 6, *_SHARE[1:]),
    *_domain("ben_breakpoint", *_FINITE_0[:1], 6, *_FINITE_0[1:]),
    *_domain("ben_cap_mth", *_FINITE_0[:1], 6, *_FINITE_0[1:]),
    *_domain("ben_guarantee_mth", *_FINITE_0[:1], 6, *_FINITE_0[1:]),
    *_domain("ben_tolerance", "a number above 0 and at most 1", 6, (ABOVE_0, 1.0),
             (0.0, ABOVE_1)),
    *_domain("expense_maint", *_FINITE_0[:1], 1, *_FINITE_0[1:]),
    *_domain("expense_claim", *_FINITE_0[:1], 2, *_FINITE_0[1:]),
    *_domain("inflation_rate", "a finite number, -1 or more", 1, (-1.0, BIG),
             (BELOW_MINUS_1,),
             {BIG: "point_id 1: the expenses expenses(12) are inf, not a finite number, "
                   "from expense_maint 60.0, expense_claim 300.0 and inflation_rate "
                   f"{BIG}"}),
    *_domain("disc_rate", "a finite number above -1", 2, (ABOVE_MINUS_1, BIG), (-1.0,)),
    *_whole_domain("issue_age_min", 1, (0, 18, 18.0, 35)),
    ("issue_age_min=2**53-1 on 1", {"issue_age_min": WHOLE - 1}, 1,
     f"point_id 1: issue_age_max must be issue_age_min, {int(WHOLE - 1)}, or more, not 59",
     None),
    *_whole_domain("issue_age_max", 1, (35, 59, 59.0, int(WHOLE - 1)), below=False),
    ("issue_age_max=17 on 1", {"issue_age_max": 17}, 1,
     "point_id 1: issue_age_max must be issue_age_min, 18, or more, not 17", None),
    *_whole_domain("expiry_age_min", 1, (0, 50, 50.0, 65), below=False),
    *_whole_domain("expiry_age_max", 1, (65, 70, 70.0, 76), below=False),
    ("expiry_age_max=77 on 1", {"expiry_age_max": 77}, 1, _EXPIRY_MAX.format(77), None),
    ("expiry_age_max=49 on 1", {"expiry_age_max": 49}, 1, _EXPIRY_MAX.format(49), None),
]


# The accepted edges that are the anchor cell's own ages, each a bound set at its issue age,
# 35, or its expiry age, 65, which project on the anchor cell by default too: on another
# point the bound would not be at its edge, or would refuse it.
OWN_POINT_EDGES = frozenset({"issue_age_min=35 on 1", "issue_age_max=35 on 1",
                             "expiry_age_min=65 on 1", "expiry_age_max=65 on 1"})


@pytest.fixture(scope="module")
def extract_folder(tmp_path_factory):
    """The SEC folder of an extract, unedited (:func:`_extract_inputs`), which the cases
    that read it as it is each read afresh."""
    return _extract_inputs(tmp_path_factory.mktemp("extract"))


@pytest.mark.parametrize("case, refs, point, message, report", DOMAINS,
                         ids=[c[0] for c in DOMAINS])
def test_each_reference_is_held_to_its_domain_at_both_edges(extract_folder, case, refs,
                                                            point, message, report):
    """``proj_len()`` holds each Reference to its domain, NaN and the infinities outside it.

    ``IP_UK_S`` checks none of them, and off its domain each projects a negative rate,
    benefit or expense, a factor that changes sign each year, or a NaN that a comparison
    loses, every check passing: a NaN escalation cap is lost through its ``min``, a NaN
    lapse threshold through the shock's ``max``, a NaN cycle overlay through the recovery
    rate's bound, and a NaN age bound switches off every comparison with it.  The frame
    refuses each such Reference, by name, before it projects anything, and every report with
    it, at the nearest value outside each edge of its domain (:data:`DOMAINS`), on a point
    that reads it.  Each Reference is refused on every point, whether or not the point reads
    it, as a model-wide assumption.  And the frame accepts each edge, whose reports then
    project, in finite floats over the whole frame, but where the edge takes a value past
    the floats, which is refused where it first is, naming the References.  A whole float,
    ``70.0``, reads as the whole number.  Each case sets its References on a model just read
    (K7).  An accepted edge projects on the case's point with the full grid, and by default
    on the twin of S point 6, the older male cell, RPI-escalating, active and claiming,
    which reads every Reference over the shortest frame of S's points, 120 months, but for
    the four age bounds set at the anchor cell's own ages (:data:`OWN_POINT_EDGES`): since
    the C step a frame forms its claim cohorts a cell an element in modelx, and the
    accepted edges on frames of 360 months took about three minutes of the default run.
    Each case runs on an extract labelled otherwise than by position (:func:`_read_extract`,
    :func:`extract_folder`), and a refusal must begin by naming the point by the extract's
    label.
    """
    assert OWN_POINT_EDGES <= {c[0] for c in DOMAINS if c[3] is None}, OWN_POINT_EDGES
    model = mx.read_model(extract_folder, name=_name("domain"))
    try:
        for ref, value in refs.items():
            setattr(model.Projection, ref, value)
        if (message is None and report is None and not SEC_FULL
                and case not in OWN_POINT_EDGES):
            point = 6
        label = _relabel_map()[_label(_committed(), "twin", point, 0)]
        p = _point(model, label)
        if message is not None:
            _refused_naming(p.result_cf, _as_extract(message), label)
        elif report is not None:
            assert p.proj_len() > 0
            _refused_naming(p.result_cf, _as_extract(report), label)
        else:
            for name in ("result_cf", "result_states", "result_pols"):
                frame = p.cells[name]()
                assert list(frame.index) == list(range(p.proj_len())), (case, name)
                assert np.isfinite(frame.to_numpy(dtype=float)).all(), (case, name)
            assert p.check_pols_roll_fwd() and p.check_states(), case
    finally:
        model.close()


# A value past the floats from an opening state and References each in its domain, as
# (case, the table's edit, the References set, the point, the call, a report that reads it,
# the start of the message).  The anchor cell at 60, issued on a benefit near the largest
# float and not yet increased, its premium neither, a history an RPI of 0 gives, which
# month 0's escalation, its fifth anniversary's, takes past it; the female cell at 13,
# issued on a premium near it and its first anniversary's increase not taken, which its
# second anniversary, at t = 11, takes past it; each history within the contract's bounds
# (test_the_escalation_history_is_bounded_by_the_contract), which an amount near the
# largest float beside an amount at issue far below it is not.  Then a count of 1e307
# paying 35 a month; the claim at 24 paying 1e300 a month on a count of
# 1e300; the claims-in-payment twin paying 1.75e308 a month beside a claim expense of the
# largest float, each finite and their sum, the net cash flow, not; the same twin's present
# value at 1e308 a month; the lapse shock under an escalation of 1e300 and a slope of 1e10;
# and the powers: the inflation factor and the benefit's and premium's steps under rates of
# 1e200, which square past the floats at the second anniversary, and the discount factor at
# a rate a hair above -1.  And the lives in claim (M8's review): the claim at 24, its count
# the largest float, all of it in claim at claim durations 24 and 25 with shares of 0.5 and
# 0.5 + 9e-11, which Data reads, summing to 1 within its 1e-10, at a claim severity of 0, so
# that it claims nothing: their sum, pols_sick(0), leaves the floats, and the expenses on it
# are refused first, printing it as sum makes it, inf, where a sum that dropped its test of
# the carried error would make NaN.  Each is refused in the cell where it first is, naming
# the point, the month and what makes it.
def _with_cohorts(edit, cohorts_edit):
    """``edit`` of the table, carrying ``cohorts_edit``, an edit of the claim cohorts that
    the case makes too (:func:`_read_extract`)."""
    def both(table):
        return (edit or (lambda t: t))(table)
    both.cohorts = cohorts_edit
    return both


def _in_claim_at(point, shares):
    """An edit of the claim cohorts that holds ``point``'s lives in claim at ``shares``,
    ``{claim duration: share}``, and nowhere else."""
    def edit(table):
        table = table[table["point_id"] != point]
        rows = pd.DataFrame({"point_id": point, "z": list(shares),
                             "pols_sick_dur_init": list(shares.values())})
        return pd.concat([table, rows], ignore_index=True)
    return edit


# The claim at 24, all in claim at claim durations 24 and 25 at shares summing to 1 + 9e-11.
LIVES_PAST = _in_claim_at(11, {24: 0.5, 25: 0.5 + 9e-11})
PAST_THE_FLOATS = [
    ("a benefit",
     _then(_set("benefit_mth", [9], 1.75e308), _set("benefit_pp_init", [9], 1.75e308),
           _set("premium_pp_init", [9], 35.0)), {}, 9, ("benefit_pp", 0), "result_cf",
     "point_id 9: the benefit benefit_pp(0) is inf, not a finite number, from "
     "benefit_pp_init 1.75e+308 and an annual increase of 0.03"),
    ("a premium",
     _then(_set("premium_mth", [14], 1.75e308), _set("premium_pp_init", [14], 1.75e308),
           _set("benefit_pp_init", [14], 1500.0)), {}, 14, ("premium_pp", 11), "result_cf",
     "point_id 14: the premium premium_pp(11) is inf, not a finite number, from "
     "premium_pp_init 1.75e+308 and an annual increase of 0.045"),
    ("the premiums", _set("policy_count", [1], 1e307), {}, 1, ("premiums", 0), "result_cf",
     "point_id 1: the premiums premiums(0) are inf, not a finite number, from "
     "premium_pp(0) 35.0 on pols_active(0) 1e+307 healthy lives"),
    ("the claims",
     _then(_set("policy_count", [11], 1e300), _set("benefit_mth", [11], 1e300),
           _set("benefit_pp_init", [11], 1e300)), {}, 11, ("claims", 0, "BENEFIT"),
     "result_cf",
     "point_id 11: the claims claims(0, 0) are inf, not a finite number, from "
     "amount_payable_pp(0) 1e+300 on pols_sick_surv(0) "),
    ("the net cash flow",
     _then(_set("benefit_mth", [2], 1.75e308), _set("benefit_pp_init", [2], 1.75e308)),
     {"expense_claim": BIG}, 2, ("net_cf", 0), "result_cf",
     "point_id 2: the net cash flow net_cf(0) is -inf, not a finite number, from premiums "
     "0.0, claims "),
    ("the present value",
     _then(_set("benefit_mth", [2], 1e308), _set("benefit_pp_init", [2], 1e308)), {}, 2,
     ("pv_benefits",), "pv_benefits",
     "point_id 2: the present value pv_benefits() is inf, not a finite number, at "
     "disc_rate 0.03"),
    ("the lapse shock", None,
     {"rpi_rate": 1e300, "esc_cap": 1e300, "esc_lapse_slope": 1e10}, 1,
     ("esc_lapse_factor", 12), "result_cf",
     "point_id 1: the lapse shock esc_lapse_factor(12) is inf, not a finite number, from "
     "esc_lapse_slope 10000000000.0, esc_prem_mult 1.5 and an escalation rate of 1e+300"),
    ("the inflation factor", None, {"inflation_rate": 1e200}, 1, ("inflation_factor", 24),
     "result_cf",
     "point_id 1: the inflation factor inflation_factor(24) is past the largest float, "
     "under inflation_rate 1e+200"),
    ("the benefit's step", None, {"rpi_rate": 1e200, "esc_cap": 1e200}, 1,
     ("benefit_pp", 24), "result_pols",
     "point_id 1: the benefit benefit_pp(24) is past the largest float, from "
     "benefit_pp_init 2000.0 and an annual increase of 1e+200"),
    ("the premium's step", None, {"rpi_rate": 1e200, "esc_cap": 1e200}, 1,
     ("premium_pp", 24), "result_cf",
     "point_id 1: the premium premium_pp(24) is past the largest float, from "
     "premium_pp_init 35.0 and an annual increase of 1.5e+200"),
    ("the discount factor", None, {"disc_rate": ABOVE_MINUS_1}, 2, ("disc_factor", 231),
     "pv_benefits",
     "point_id 2: the discount factor disc_factor(231) is past the largest float, under "
     "disc_rate -0.9999999999999999"),
    ("the lives in claim", _with_cohorts(_set("policy_count", [11], BIG), LIVES_PAST),
     {"claim_severity": 0.0}, 11, ("expenses", 0), "result_cf",
     "point_id 11: the expenses expenses(0) are inf, not a finite number, from "
     "expense_maint 60.0, expense_claim 300.0 and inflation_rate 0.03, on pols_if(0) inf "
     "policies, pols_sick(0) inf in claim"),
]


@pytest.mark.parametrize("case, edit, refs, point, call, report, message", PAST_THE_FLOATS,
                         ids=[c[0] for c in PAST_THE_FLOATS])
def test_a_value_past_the_floats_is_refused_where_it_first_is(tmp_path, case, edit, refs,
                                                              point, call, report, message):
    """A value past the largest float is refused in the cell where it first is.

    ``Data`` and ``proj_len()`` hold each opening amount, count and Reference to a finite
    number, so a value near the largest float reads; an escalation, a premium, a count, a
    rate or a sum then takes a value the projection computes past the floats, where
    ``IP_UK_S`` would pay an infinite benefit, charge an infinite expense or discount by an
    infinite factor, every report infinite and its checks NaN or passing, or where a power
    raises Python's ``OverflowError``, naming nothing.  The cell where the value first
    leaves the floats refuses it, naming the point, the month and what makes it
    (:data:`PAST_THE_FLOATS`), and so does a report that reads it first: ``result_cf``, or
    ``result_pols`` for the benefit's step, which no cash flow reads before the premium's,
    or ``pv_benefits`` for the discount factor, which no report reads
    (USLIB-SEC-PLAN.md §7.1, *Record — M1*; UKLIB-SEC-PLAN.md §6.6, *Carried into M10 and
    after*; §6.7, *Record — M11*).  The month before projects.  Each Reference is set on a
    model just read (K7).  A kind is passed as its code, and a refusal names it by its code,
    as the compiled model prints it.  Each case runs on an extract labelled otherwise than
    by position (:func:`_read_extract`), and each refusal must begin by naming the point by
    the extract's label.
    """
    model = _read_extract(tmp_path, edit, getattr(edit, "cohorts", None))
    label = _relabel_map()[point]
    try:
        for ref, value in refs.items():
            setattr(model.Projection, ref, value)
        p = _point(model, label)
        name, *args = call
        args = [_code(p, a) if isinstance(a, str) else a for a in args]
        if args and args[0] > 0:
            p.cells[name](args[0] - 1, *args[1:])
        _refused_naming(lambda: p.cells[name](*args), _as_extract(message), label)
        _refused_naming(p.cells[report], _as_extract(message), label)
    finally:
        model.close()


@pytest.mark.parametrize("grid", GRIDS)
def test_a_whole_bound_written_as_an_int_projects_as_the_shipped_float_does(grid):
    """The four age bounds written as ints project what the shipped floats project.

    ``issue_age_min``, ``issue_age_max``, ``expiry_age_min`` and ``expiry_age_max`` ship as
    floats, ``18.0``, ``59.0``, ``50.0`` and ``70.0``, so that a fraction set on one is the
    fraction in either engine, refused as not whole in both, where a compiled model holding
    an int Reference as a C integer would truncate it as it is set (UKLIB-SEC-PLAN.md §6.3,
    M8).  ``proj_len()`` holds each to a whole number and compares it with an ``int`` age.
    So with the four set as the ints, on a model just read, the twins of S's anchor cell
    and of its claims-in-payment cell, the anchor cell in force at 60 and the female cell
    issued later are what the shipped model makes of them in every cell, bit for bit, each
    integer cell an ``int`` in both.

    The twin of the anchor cell and the anchor cell in force run by default, and the claim's
    twin and the point issued later with the full grid.
    """
    as_ints = mx.read_model(model_path(SEC), name=_name("ints"))
    shipped = mx.read_model(model_path(SEC), name=_name("floats"))
    try:
        assert all(type(shipped.Projection.refs[ref]) is float for ref in (
            "issue_age_min", "issue_age_max", "expiry_age_min", "expiry_age_max"))
        for ref, value in (("issue_age_min", 18), ("issue_age_max", 59),
                           ("expiry_age_min", 50), ("expiry_age_max", 70)):
            setattr(as_ints.Projection, ref, value)
        cases = ((("twin", 1, 0), ("derived", 1, 60)) if grid == "core"
                 else (("twin", 2, 0), ("future", 4, -13)))
        for case in cases:
            mine, theirs = _row(as_ints, *case), _row(shipped, *case)
            sweep(theirs)
            assert twin_mismatches(theirs, mine, exempt=frozenset(), rtol=0.0,
                                   atol=0.0) == [], case
            for name in ("proj_len", "expiry_mth", "t_entry", "duration_mth_init",
                         "max_dur"):
                assert type(mine.cells[name]()) is int, (case, name)
                assert type(theirs.cells[name]()) is int, (case, name)
    finally:
        shipped.close()
        as_ints.close()


def test_the_edges_of_the_in_force_interface_are_accepted(tmp_path):
    """A zero count, whole numbers in any type, the horizon and each bound's edge are read.

    A count of 0 is a point that projects zeros.  ``60.0`` is a whole number of months,
    read back as the int the policy clock counts in; a policy issued 120 months after the
    valuation date, the shipped ``future_horizon_mth``, is the last one the table admits,
    with a frame of 336 months.  And each bound of the contract at its edge projects: issue
    at 18 to expiry at 70, 624 months, and issue at 59 to expiry at 60, 12 months, the
    oldest issue and the shortest cover, and expiry at 50, the earliest.  Then the
    history's bounds, each at its edge: an escalated benefit and premium half a cent below
    those at issue, an extract rounded to the cent, which ``Data``'s rule 12 admits; and
    the first-year rule's edge, the female cell a month past its first anniversary, its
    first increase in the columns.  And the claim cohorts' edges: shares summing to 1
    within 9e-11 either side, inside the tolerance of 1e-10 the malformed cases refuse
    1.1e-10 past; a claim as old as its policy, ``z = duration_mth``; and a point in force
    all healthy, holding no row in the companion.  The extra rows are copies of committed
    rows under labels of their own, 41 to 49.
    """
    committed = _committed()
    claim = _label(committed, "derived", 2, 24)
    anchor = _label(committed, "derived", 1, 60)
    female = _label(committed, "derived", 4, 13)
    future = _label(committed, "future", 4, -13)
    copies = {41: (1, {"entry_age": 18, "expiry_age": 70}),
              42: (6, {"entry_age": 59, "expiry_age": 60}),
              43: (3, {"entry_age": 18, "expiry_age": 50}),
              44: (anchor, {"benefit_pp_init": 1999.995, "premium_pp_init": 34.995}),
              46: (anchor, {}),
              47: (anchor, {}),
              48: (claim, {}),
              49: (anchor, {"pols_active_init": 1.0})}

    def edit(table):
        extra = []
        for label, (source, changes) in copies.items():
            row = table.loc[[source]].assign(policy_id=f"IP-9000{label}", **changes)
            row.index = pd.Index([label], name="point_id")
            extra.append(row)
        table = pd.concat([table, *extra])
        table = _set("policy_count", [1], 0.0)(table)
        table = table.assign(duration_mth=table["duration_mth"].astype(float))
        table = _set("duration_mth", [future], -120.0)(table)
        return table

    def cohorts(table):
        def copy_of(source, label):
            return table[table["point_id"] == source].assign(point_id=label)
        held = [table, copy_of(anchor, 44)]
        for label, by in ((46, 9e-11), (47, -9e-11)):
            rows = copy_of(anchor, label).reset_index(drop=True)
            at = rows["pols_sick_dur_init"].idxmax()
            rows.loc[at, "pols_sick_dur_init"] = rows.at[at, "pols_sick_dur_init"] + by
            held.append(rows)
        held.append(copy_of(claim, 48).assign(z=36))
        return pd.concat(held, ignore_index=True)

    model = _read_edited(tmp_path, edit, cohorts)
    try:
        read = model.Data.model_point_table()
        assert read["duration_mth"].dtype == float
        assert len(model.Data.inforce_cohorts()) == len(cohorts(_committed_cohorts()))
        zero = _point(model, 1)
        df = zero.result_cf()
        assert len(df) == 360 and (df == 0.0).all().all()
        assert type(zero.duration_mth(0)) is int
        late = _point(model, future)
        assert (late.t_entry(), late.proj_len(), late.pols_new_biz(120)) == (120, 336, 1.0)
        for label, months in ((41, 624), (42, 12), (43, 384)):
            edge = _point(model, label)
            assert len(edge.result_cf()) == edge.proj_len() == months, label
            assert edge.check_pols_roll_fwd() and edge.check_states(), label
        half = _point(model, 44)
        assert half.benefit_pp(0) == pytest.approx(1999.995 * 1.03, rel=1e-15)
        first = _point(model, female)
        assert (first.duration_mth_init(), first.duration_init()) == (13, 1)
        assert first.benefit_pp(0) == first.benefit_pp_init() == 1545.0
        for label in (46, 47):
            p = _point(model, label)
            assert p.check_states() and p.proj_len() == 300, label
        old = _point(model, 48)
        assert old.pols_sick_dur_init(36) > 0.0 and old.pols_sick_dur_init(25) == 0.0
        assert old.pols_sick_dur(0, 36) == old.pols_if_init() * old.pols_sick_dur_init(36)
        healthy = _point(model, 49)
        assert healthy.pols_active(0) == healthy.policy_count()
        assert healthy.pols_sick(0) == 0.0 and healthy.check_states()
    finally:
        model.close()


def _every_state_months(start, end):
    """The S months a point whose S frame runs from ``start`` to ``end`` is restated at.

    By default the edges of its windows (USLIB-SEC-PLAN.md §5.2, T5): every month of the
    first policy year and the first anniversary, through which ``Data``'s first-year rule
    ends and the first claims start, each anniversary and the month before it, which on
    S's clock are the escalation's steps, the lapse table's years and, on a claim, its
    claim-duration years, and the last month of the frame.  With ``UKLIB_SEC_FULL=1``,
    every month.  Each after ``start``, the twin's month.
    """
    if SEC_FULL:
        return list(range(start + 1, end))
    months = {*range(1, 14), end - 1, *(m for a in range(12, end, 12) for m in (a - 1, a))}
    return sorted(m for m in months if start < m < end)


def _states(s):
    """Each ``(S point, month)`` of :func:`_every_state_months` on every point of ``s``."""
    table = s.Data.model_point_table()
    return [(point_id, d) for key, point_id in zip(point_keys(s), table.index)
            for d in _every_state_months(0, projection(s, key).proj_len())]


def _restated(root, s, states):
    """The twins of ``s``'s points and a row in force at each of ``states``, ``(S point,
    month)``, with their claim cohorts, built by the generator out of ``s`` into a copy of
    the product directory: ``(folder, table, cohorts)``."""
    spec = dataclasses.replace(SPEC, derived=tuple(states), future=(), derived_refs={})
    table, companions = build_sec_table(spec, s)
    return _sec_inputs(root, table, companions[COHORTS]), table, companions[COHORTS]


def _refused_in_force(folder, refs):
    """What ``Data`` and ``proj_len()`` refuse of the table and cohorts in ``folder``, read
    with ``refs`` set first: ``Data``'s refusal, or each row's ``proj_len()``'s, each by
    the line that names it.  Each row is released once asked (:func:`_release`)."""
    model = mx.read_model(folder, name=_name("every"))
    try:
        for ref, value in refs.items():
            setattr(model.Projection, ref, value)
        try:
            model.Data.model_point_table()
            model.Data.inforce_cohorts()
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


def test_every_state_s_reaches_is_accepted_in_force(s_model, tmp_path):
    """Every state ``IP_UK_S`` reaches is a valid opening state (T5).

    ``Data``'s rules and ``proj_len()``'s hold an opening state to what a policy in force
    can be, so they must accept each state the S model reaches: a rule exercised only on
    the rows the other tests choose could refuse a state S reaches elsewhere (D6).  So each
    point of S is restated in force by the generator at the edges of its windows, or with
    ``UKLIB_SEC_FULL=1`` at every month of its frame (:func:`_every_state_months`), into
    one table beside the twins, with its claim cohorts: ``Data`` reads both, and no row's
    ``proj_len()`` refuses it (USLIB-SEC-PLAN.md §5.2, T5, precised at M10).  The test runs
    on each set of inputs on which the states S reaches differ (precised at M9), and
    asserts which states each moves:

    * S as shipped, its seven points under its own References, as T1 and the committed rows
      read it (``s_model``);
    * the main splice set's, :data:`MAIN`, which moves the count, the healthy share, the
      cohorts, the benefit and the premium, every column of the state: the escalation lapse
      shock and the overlays move the first three, and the RPI the last two;
    * the escalation cap's, an RPI of 12%, which moves them all again, the escalation at
      10% a year;
    * the RPI floor's, an RPI of -2%, under which an escalating point's benefit and premium
      stay those at issue past its first year, the edge of ``Data``'s rule 12, which the
      shipped set reaches only in a first policy year or on a level point;
    * the recovery bound's, an overlay of 0.35, under which every claim of a first claim
      year recovers in its month, which moves the count, the healthy share and the cohorts
      and leaves the benefit and the premium the main set's, at its RPI of 5%.

    Expense inflation moves no state, being on the valuation clock and no count.
    ``IP_UK_SEC`` refuses no state ``IP_UK_S`` reaches, so none is set aside.
    """
    extra = {tag: SPLICE_SETS[tag] for tag in ("main", "rpi_cap", "rpi_floor", "recovery")}
    read = {tag: mx.read_model(model_path(TWIN), name=_name(tag)) for tag in extra}
    try:
        for tag, refs in extra.items():
            for ref, value in refs.items():
                setattr(read[tag].Projection, ref, value)
        sets = {"shipped": (s_model, {}), **{tag: (read[tag], refs)
                                             for tag, refs in extra.items()}}
        found, states, held = {}, {}, {}
        for tag, (s, refs) in sets.items():
            reached = _states(s)
            folder, rows, cohorts = _restated(tmp_path / tag, s, reached)
            assert len(rows) == len(s.Data.model_point_table()) + len(reached)
            states[tag] = rows.set_index(["source_policy_id", "source_mth"])
            held[tag] = cohorts.assign(
                policy=cohorts["point_id"].map(rows.set_index("point_id")[
                    "source_policy_id"]),
                month=cohorts["point_id"].map(rows.set_index("point_id")["source_mth"]))
            refused = _refused_in_force(folder, refs)
            if refused:
                found[tag] = f"{len(refused)} refused, first: {refused[:5]}"
    finally:
        for model in read.values():
            model.close()
    assert not found, found
    shipped = states["shipped"]
    columns = ("policy_count", *STATE)
    for tag, moved in (("main", set(columns)), ("rpi_cap", set(columns)),
                       ("rpi_floor", set(columns)),
                       ("recovery", {"policy_count", "pols_active_init"})):
        both = shipped.index.intersection(states[tag].index)
        assert len(both), tag
        apart = {c for c in columns
                 if (shipped.loc[both, c] != states[tag].loc[both, c]).any()}
        if tag == "recovery":
            apart -= {c for c in STATE[1:]
                      if (states["main"].loc[both, c] == states[tag].loc[both, c]).all()}
        assert apart == moved, (tag, apart)
        keys = ["policy", "month", "z"]
        a = held["shipped"].set_index(keys)["pols_sick_dur_init"]
        b = held[tag].set_index(keys)["pols_sick_dur_init"]
        assert not a.reindex(b.index).equals(b), tag


# ---------------------------------------------------------------------------
# The assumption tables
#
# Data checks each table before a value of it is read, in the cell the projection takes the
# table's extent from, or in the reader where it takes none (UKLIB-SEC-PLAN.md §4;
# USLIB-SEC-PLAN.md §7.1, *Precised at M3*, item 9).  Each case is the shipped table with
# one fault, read from a copy, refused by that cell alone, naming the file, the column and
# the lines at fault, the header line 1, and through a projection of the anchor cell in
# force at 60, which reads every table.  The lines are the shipped file's (_line): the
# mortality table holds the male ages 16 to 75 on lines 2 to 61 and the female on lines 62
# to 121; the lapse table the policy years 1 to 6 on lines 2 to 7; the termination table the
# claim duration years 1 to 5 on lines 2 to 6; and the inception table its forty schedules,
# eight pivot ages each, on lines 2 to 321.

MORT, LAPSE, TERM, INCEPTION = ("mort_table.csv", "lapse_table.csv",
                                "termination_table.csv", "inception_table.csv")

# The Data cell that checks each table, the first a projection asks of it.
CHECKED_BY = {MORT: "mort_age_first", LAPSE: "lapse_last_year",
              TERM: "termination_last_year", INCEPTION: "inception_table"}


def _line(file, **keys):
    """The line of the shipped ``file`` whose columns hold ``keys``, the header line 1."""
    rows = pd.read_csv(model_path(TWIN).parent / file)
    hit = rows.index[_where(**keys)(rows)].tolist()
    assert len(hit) == 1, (file, keys, hit)
    return hit[0] + 2


def _where(**keys):
    """The rows of a table whose columns hold ``keys``, as a boolean array."""
    return lambda table: np.logical_and.reduce(
        [(table[c] == v).to_numpy() for c, v in keys.items()])


def _written(column, value, where):
    """An edit of a table that writes ``value`` into ``column`` on the rows ``where``
    picks."""
    def edit(table):
        cells = table[column].astype(object)
        cells[where(table)] = value
        return table.assign(**{column: cells})
    return edit


def _dropped(where):
    return lambda table: table[~where(table)].reset_index(drop=True)


def _repeated(where):
    return lambda table: pd.concat([table, table[where(table)]], ignore_index=True)


def _rate_rule(file, column, *lines):
    return f"{file}: {column} must be a number from 0 to 1; it is not on line {list(lines)}"


def _whole_rule(file, column, *lines):
    return (f"{file}: {column} must be a whole number below 2**53 in size; it is not on "
            f"line {list(lines)}")


def _ages_apart(*faults):
    """The message of a mortality table whose sexes do not run one row an age."""
    return (f"{MORT}: the ages of each sex must run from 16 to 75, the table's first and "
            f"last, one row an age, none below 0; " + "; ".join(faults))


def _years_apart(file, years, *faults):
    """The message of a lapse or termination table whose years do not run one row a
    year."""
    return (f"{file}: the {years} must run from 1, one row a year, without a gap or a "
            f"repeat; " + "; ".join(faults))


def _schedules_apart(*faults):
    """The message of an inception table whose schedules do not hold two pivots each."""
    return (f"{INCEPTION}: each sex, occupation class and deferred period must hold two "
            f"pivot ages or more, one row an age; " + "; ".join(faults))


def _mort(sex, age):
    return _where(sex=sex, age=age)


def _pivot(sex, occ, weeks, age):
    return _where(sex=sex, occ_class=occ, deferred_weeks=weeks, age=age)


def _pivot_line(sex, occ, weeks, age):
    return _line(INCEPTION, sex=sex, occ_class=occ, deferred_weeks=weeks, age=age)


NAN, INF = float("nan"), float("inf")
_CODES = (f"{INCEPTION}: sex must be M or F, occ_class 1 to 4, and deferred_weeks 4, 8, 13, "
          f"26 or 52; they are not on line ")

# A table the reader cannot read, or whose value is not a number in its range, as (case,
# the file, its edit, the message).  A value no point reads is refused too: the male
# mortality at 75, which no frame reaches, and the female inception schedule of class 4
# and 52 weeks, which no point holds.
UNREADABLE = [
    ("a blank mortality rate", MORT, _written("mort_rate", NAN, _mort("M", 40)),
     _rate_rule(MORT, "mort_rate", _line(MORT, sex="M", age=40))),
    ("a text mortality rate", MORT, _written("mort_rate", "low", _mort("F", 40)),
     _rate_rule(MORT, "mort_rate", _line(MORT, sex="F", age=40))),
    ("an infinite mortality rate no point reads", MORT,
     _written("mort_rate", INF, _mort("M", 75)),
     _rate_rule(MORT, "mort_rate", _line(MORT, sex="M", age=75))),
    ("a negative mortality rate", MORT, _written("mort_rate", -0.001, _mort("F", 16)),
     _rate_rule(MORT, "mort_rate", _line(MORT, sex="F", age=16))),
    ("a mortality rate past 1", MORT, _written("mort_rate", 1.5, _mort("M", 60)),
     _rate_rule(MORT, "mort_rate", _line(MORT, sex="M", age=60))),
    ("two mortality rows at fault", MORT,
     _then(_written("mort_rate", NAN, _mort("M", 16)),
           _written("mort_rate", NAN, _mort("F", 75))),
     _rate_rule(MORT, "mort_rate", _line(MORT, sex="M", age=16),
                _line(MORT, sex="F", age=75))),
    ("an age not whole", MORT, _written("age", 65.5, _mort("M", 65)),
     _whole_rule(MORT, "age", _line(MORT, sex="M", age=65))),
    ("an age past 2**53", MORT, _written("age", 1e19, _mort("F", 50)),
     _whole_rule(MORT, "age", _line(MORT, sex="F", age=50))),
    ("an age written as text", MORT, _written("age", "x", _mort("F", 17)),
     _whole_rule(MORT, "age", _line(MORT, sex="F", age=17))),
    ("an unknown sex", MORT, _written("sex", "X", _mort("F", 18)),
     f"{MORT}: sex must be M or F; it is not on line [{_line(MORT, sex='F', age=18)}]"),
    ("an age missing", MORT, _dropped(_mort("M", 40)),
     _ages_apart("no line holds sex M, age 40")),
    ("an age twice", MORT, _repeated(_mort("F", 30)),
     _ages_apart(f"sex F, age 30 repeats on lines [{_line(MORT, sex='F', age=30)}, 122]")),
    ("an age below 0", MORT, _written("age", -1, _mort("M", 16)),
     _ages_apart(f"age -1, below 0, is on lines [{_line(MORT, sex='M', age=16)}]",
                 "no line holds sex M, age 16")),
    ("a sex missing", MORT, _dropped(lambda t: (t["sex"] == "F").to_numpy()),
     _ages_apart("no line holds sex F, ages 16 to 75")),
    ("a sex shorter", MORT, _dropped(_mort("F", 75)),
     _ages_apart("no line holds sex F, age 75")),
    ("a blank lapse rate", LAPSE, _written("lapse_rate", NAN, _where(policy_year=2)),
     _rate_rule(LAPSE, "lapse_rate", 3)),
    ("a lapse rate past 1", LAPSE, _written("lapse_rate", 1.2, _where(policy_year=6)),
     _rate_rule(LAPSE, "lapse_rate", 7)),
    ("an infinite lapse rate", LAPSE, _written("lapse_rate", INF, _where(policy_year=1)),
     _rate_rule(LAPSE, "lapse_rate", 2)),
    ("a text lapse rate", LAPSE, _written("lapse_rate", "six", _where(policy_year=4)),
     _rate_rule(LAPSE, "lapse_rate", 5)),
    ("a policy year not whole", LAPSE, _written("policy_year", 3.5, _where(policy_year=3)),
     _whole_rule(LAPSE, "policy_year", 4)),
    ("a policy year missing", LAPSE, _dropped(_where(policy_year=4)),
     _years_apart(LAPSE, "policy years", "no line holds policy_year 4")),
    ("a policy year twice", LAPSE, _repeated(_where(policy_year=2)),
     _years_apart(LAPSE, "policy years", "policy_year 2 repeats on lines [3, 8]")),
    ("a policy year of 0", LAPSE, _written("policy_year", 0, _where(policy_year=1)),
     _years_apart(LAPSE, "policy years", "policy_year 0, below 1, is on lines [2]",
                  "no line holds policy_year 1")),
    ("a blank recovery rate", TERM,
     _written("recovery_rate", NAN, _where(claim_duration_year=1)),
     _rate_rule(TERM, "recovery_rate", 2)),
    ("a recovery rate past 1", TERM,
     _written("recovery_rate", 1.4, _where(claim_duration_year=2)),
     _rate_rule(TERM, "recovery_rate", 3)),
    ("a negative in-claim mortality", TERM,
     _written("mort_rate_sick", -0.01, _where(claim_duration_year=3)),
     _rate_rule(TERM, "mort_rate_sick", 4)),
    ("an infinite in-claim mortality", TERM,
     _written("mort_rate_sick", INF, _where(claim_duration_year=5)),
     _rate_rule(TERM, "mort_rate_sick", 6)),
    ("a claim duration year written as text", TERM,
     _written("claim_duration_year", "4+", _where(claim_duration_year=4)),
     _whole_rule(TERM, "claim_duration_year", 5)),
    ("two claim duration years missing", TERM,
     _dropped(lambda t: t["claim_duration_year"].isin([2, 3]).to_numpy()),
     _years_apart(TERM, "claim duration years", "no line holds claim duration years 2 to 3")),
    ("a claim duration year twice", TERM, _repeated(_where(claim_duration_year=5)),
     _years_apart(TERM, "claim duration years",
                  "claim_duration_year 5 repeats on lines [6, 7]")),
    ("a blank inception rate", INCEPTION,
     _written("inception_rate", NAN, _pivot("M", 1, 26, 40)),
     _rate_rule(INCEPTION, "inception_rate", _pivot_line("M", 1, 26, 40))),
    ("an inception rate past 1", INCEPTION,
     _written("inception_rate", 1.2, _pivot("F", 3, 13, 45)),
     _rate_rule(INCEPTION, "inception_rate", _pivot_line("F", 3, 13, 45))),
    ("a text inception rate", INCEPTION,
     _written("inception_rate", "high", _pivot("M", 2, 52, 60)),
     _rate_rule(INCEPTION, "inception_rate", _pivot_line("M", 2, 52, 60))),
    ("an infinite inception rate no point reads", INCEPTION,
     _written("inception_rate", INF, _pivot("F", 4, 52, 64)),
     _rate_rule(INCEPTION, "inception_rate", _pivot_line("F", 4, 52, 64))),
    ("an occupation class of 5", INCEPTION, _written("occ_class", 5, _pivot("M", 4, 8, 30)),
     _CODES + f"[{_pivot_line('M', 4, 8, 30)}]"),
    ("a deferred period off the menu", INCEPTION,
     _written("deferred_weeks", 6, _pivot("F", 1, 4, 35)),
     _CODES + f"[{_pivot_line('F', 1, 4, 35)}]"),
    ("an unknown sex in the inception table", INCEPTION,
     _written("sex", "X", _pivot("M", 3, 26, 50)),
     _CODES + f"[{_pivot_line('M', 3, 26, 50)}]"),
    ("a pivot age not whole", INCEPTION, _written("age", 37.5, _pivot("M", 1, 26, 35)),
     _whole_rule(INCEPTION, "age", _pivot_line("M", 1, 26, 35))),
    ("an occupation class written as text", INCEPTION,
     _written("occ_class", "OC2", _pivot("F", 2, 8, 40)),
     _whole_rule(INCEPTION, "occ_class", _pivot_line("F", 2, 8, 40))),
    ("a schedule of one pivot", INCEPTION,
     _dropped(lambda t: (_where(sex="M", occ_class=1, deferred_weeks=4)(t)
                         & (t["age"] != 30).to_numpy())),
     _schedules_apart("sex M, occ_class 1, deferred_weeks 4 holds 1 pivot age")),
    ("a schedule missing", INCEPTION,
     _dropped(_where(sex="F", occ_class=4, deferred_weeks=52)),
     _schedules_apart("sex F, occ_class 4, deferred_weeks 52 holds 0 pivot ages")),
    ("a pivot age twice", INCEPTION, _repeated(_pivot("M", 1, 26, 40)),
     _schedules_apart(f"sex M, occ_class 1, deferred_weeks 26, age 40 repeats on lines "
                      f"[{_pivot_line('M', 1, 26, 40)}, 322]")),
]


@pytest.mark.parametrize("case, file, edit, message", UNREADABLE,
                         ids=[c[0] for c in UNREADABLE])
def test_a_table_a_reader_cannot_read_is_refused_naming_its_lines(tmp_path, case, file,
                                                                  edit, message):
    """``Data`` refuses each assumption table before a value of it is read (T5).

    ``IP_UK_S`` reads a blank rate as NaN, which its caps keep and every flow carries; an
    infinite one, which a cap reads as certain death or a certain claim; a key that is not
    whole, gapped or repeated, as a ``KeyError`` only where a projection reaches it, or as a
    wrong row; and an inception schedule of one pivot as an interpolation it cannot make.
    Here the cell that checks the table (:data:`CHECKED_BY`), the first a projection asks
    of it, refuses each, naming the file, the column and the lines at fault
    (:data:`UNREADABLE`), and so does a projection of the anchor cell in force at 60, which
    reads all four tables.
    """
    model = _read_edited(tmp_path, lambda t: t, edits={file: edit})
    try:
        _refused(model.Data.cells[CHECKED_BY[file]], message)
        _refused(_row(model, "derived", 1, 60).result_cf, message)
    finally:
        model.close()


def test_a_read_beyond_the_mortality_table_is_refused_naming_its_point(tmp_path):
    """A read past the mortality table's ages is refused, naming the point, and the
    contract keeps every frame inside it.

    ``IP_UK_S``'s lookup raises ``KeyError`` beyond the table, naming no point.  The table
    rates ages 16 to 75, and the contract issues from 18, ``issue_age_min``, and expires by
    70, ``expiry_age_max``, which ``proj_len()`` holds to a year past the table's last age,
    so no frame the contract writes reads past it.  With ``issue_age_min`` lowered to 0, a
    policy issued at 15 is refused by the one cell that reads the table, naming the point
    and the age.  And with the table cut to ages 16 to 68, the shipped ``expiry_age_max`` of
    70 is itself refused, naming the table's last age, since a cover to 70 reads 69; at 69
    the anchor cell projects.  Each Reference is set on a model just read (K7).
    """
    model = _read_edited(tmp_path / "young", _set("entry_age", [3], 15))
    try:
        model.Projection.issue_age_min = 0
        _refused(_point(model, 3).result_cf,
                 "point_id 3: mort_table.csv has no rate at attained age 15")
    finally:
        model.close()
    model = _read_edited(tmp_path / "short", lambda t: t,
                         edits={MORT: _dropped(lambda t: (t["age"] > 68).to_numpy())})
    try:
        _refused(_point(model, 1).result_cf,
                 "point_id 1: expiry_age_max must be expiry_age_min, 50, or more, and at "
                 "most 69, a year past mort_table.csv's last age, not 70")
    finally:
        model.close()
    model = _read_edited(tmp_path / "shorter", lambda t: t,
                         edits={MORT: _dropped(lambda t: (t["age"] > 68).to_numpy())})
    try:
        model.Projection.expiry_age_max = 69
        assert len(_point(model, 1).result_cf()) == 360
    finally:
        model.close()


@pytest.mark.parametrize("grid", GRIDS)
def test_a_key_written_as_a_float_reads_as_ip_uk_s_reads_it(sec_model, tmp_path, grid):
    """A key written ``65.0`` is the key 65, in every table and in its extents.

    ``IP_UK_S``'s lookups match a float key to the int the projection asks, so a table
    written by a tool that writes every number with a decimal point reads the same.  The
    four assumption tables' keys, the model point table's ``duration_mth``, ages,
    occupation class and deferred period, and the claim cohorts' ``point_id`` and ``z`` are
    written as floats, and every committed point projects what the committed tables
    project, exactly.  The default run takes :data:`CORE_POINTS`, and the full grid the
    other committed points.
    """
    def as_float(*columns):
        return lambda table: table.assign(**{c: table[c].astype(float) for c in columns})

    model = _read_edited(tmp_path, as_float("duration_mth", "entry_age", "expiry_age",
                                            "occ_class", "deferred_weeks"),
                         as_float("point_id", "z"),
                         edits={MORT: as_float("age"), LAPSE: as_float("policy_year"),
                                TERM: as_float("claim_duration_year"),
                                INCEPTION: as_float("occ_class", "deferred_weeks", "age")})
    try:
        for point_id in _committed().index:
            if not _on_grid(grid, point_id):
                continue
            for report in ("result_cf", "result_states", "result_pols"):
                assert frame_mismatches(_point(sec_model, point_id).cells[report](),
                                        _point(model, point_id).cells[report](),
                                        rtol=0, atol=0) == [], (point_id, report)
    finally:
        model.close()


# ---------------------------------------------------------------------------
# T6 -- regeneration


def test_the_committed_sec_inputs_are_what_s_generates():
    """``model_point_table_sec.csv`` and ``inforce_cohorts_sec.csv`` are what IP_UK_S and
    its table generate today.

    Every row and column of both, the text cells, the opening state and the claim cohorts
    among them: an edit to an S row the table copies or derives from, or to an S formula a
    row's state is read from, fails here until ``python tools/gen_sec_points.py
    IP_UK_SEC`` regenerates them, in the same commit.  Text and integers compare exactly,
    and a float by its value, to 1e-12, because the text the writer picks for a computed
    float depends on the platform's parser (``uk_sec_support``'s module docstring).  The
    generator reads IP_UK_S afresh, as CI's and WOL's T6 let it: the spec's
    ``derived_refs`` rows set References on the S model they are read from, which drops
    its ItemSpaces, and the module's swept S model, which other tests compare with, is not
    handed to it.
    """
    assert check_generated(SEC) == []


# ---------------------------------------------------------------------------
# The product's own facts


def test_the_two_clocks_on_the_shipped_points(sec_model):
    """``t`` counts from the valuation date; ``duration_mth(t)`` from issue (D3, D4).

    On the twin of S's anchor cell the two coincide, and its policy enters as new business
    at ``t = 0``.  The anchor cell in force 60 months, its fifth anniversary falling at the
    valuation date, is in policy year 6 at attained age 40 at ``t = 0``, its count on the
    books and none new, steps into policy year 7 at ``t = 12``, and has 300 months of its
    frame left, to the same policy end date as from issue, policy month 360.  The twin of
    S's claims-in-payment worked example is in force 12 months, issued at 34 so that it is
    35 at the valuation date, as S's point is, every life in claim at claim duration 1, to
    the policy end date 372 months from issue.  The female cell issued 13 months on has
    nothing on the books and nothing to do before ``t = 13``, and a frame of 229 months.
    The anchor cell in its last month has a one-month frame, at whose end the policies in
    force reach the policy end date.  A timing or a kind the model does not know is refused
    rather than answered with another count.
    """
    twin = _row(sec_model, "twin", 1, 0)
    assert [twin.duration_mth(t) for t in (0, 1, 359)] == [0, 1, 359]
    assert (twin.t_entry(), twin.pols_if_init(), twin.pols_new_biz(0)) == (0, 0.0, 1.0)
    assert (twin.expiry_mth(), twin.proj_len(), twin.max_dur()) == (360, 360, 361)
    old = _row(sec_model, "derived", 1, 60)
    assert (old.duration_mth(0), old.duration_init(), old.duration(0), old.policy_year(0),
            old.age(0)) == (60, 4, 5, 6, 40)
    assert (old.policy_year(11), old.policy_year(12)) == (6, 7)
    assert (old.proj_len(), old.expiry_mth(), old.t_entry(), old.pols_new_biz(0)) == (
        300, 360, 0, 0.0)
    assert old.pols_if_at(0, _code(old, "BEF_DECR")) == old.pols_if_init() == (
        old.policy_count())
    claim = _row(sec_model, "twin", 2, 0)
    assert (claim.duration_mth(0), claim.age_at_entry(), claim.age(0),
            claim.policy_year(0)) == (12, 34, 35, 2)
    assert (claim.pols_active(0), claim.pols_sick(0), claim.pols_sick_dur(0, 1)) == (
        0.0, 1.0, 1.0)
    assert (claim.proj_len(), claim.expiry_mth()) == (360, 372)
    fut = _row(sec_model, "future", 4, -13)
    assert (fut.duration_mth(0), fut.t_entry(), fut.proj_len()) == (-13, 13, 229)
    assert not fut.is_active(12) and fut.is_active(13)
    assert (fut.pols_if_init(), fut.pols_new_biz(13), fut.pols_active(13)) == (0.0, 1.0, 1.0)
    last = _row(sec_model, "derived", 1, 359)
    assert (last.proj_len(), last.age(0), last.policy_year(0)) == (1, 64, 30)
    assert last.pols_maturity(0) > 0.0
    _refused(lambda: old.pols_if_at(0, "BEF_NOTHING"), "invalid timing")
    _refused(lambda: old.claims(0, "NOTHING"), "invalid kind")


DISC = 0.03             # the shipped disc_rate, which the present value test reads


def test_the_present_value_and_the_annuity_factor_run_on_the_valuation_clock(sec_model,
                                                                            s_model):
    """``pv_benefits`` discounts to the valuation date, and ``annuity_dis`` is per policy
    of the amount payable there (D7).

    On the twin of S's claims-in-payment worked example, which S opens at the valuation
    date, both are S's: the notes' ``a_dis(35, 0)``, 49.783 per £1 a month, on £2,000 a
    month a value of 99,566.90.  On a row restated in force at S month ``d``, they are S's
    claims from ``d`` on, discounted to ``d``, which S does not compute: the claim from
    duration 0 at 24, the claim from duration 30 at 6, and the anchor cell at 60, its value
    one of future claims; the factor is that value over the amount payable at the valuation
    date times the count, per policy on the books.  On the female cell issued 13 months on
    the value is S's discounted 13 months more, nothing being paid before issue.  And the
    discount factor runs on ``t``, ``1.03^-((t + 1) / 12)``, on every point.
    """
    assert sec_model.Projection.disc_rate == DISC
    twin, s2 = _row(sec_model, "twin", 2, 0), _point(s_model, 2)
    assert twin.pv_benefits() == pytest.approx(s2.pv_benefits(), rel=1e-12)
    assert twin.annuity_dis() == pytest.approx(s2.annuity_dis(), rel=1e-12)
    assert (round(twin.annuity_dis(), 3), round(twin.pv_benefits(), 2)) == (49.783, 99566.9)
    for s_point, month in ((2, 24), (5, 6), (1, 60)):
        p, s = _row(sec_model, "derived", s_point, month), _point(s_model, s_point)
        want = sum(s.claims(month + t, "BENEFIT") * (1.0 + DISC) ** (-(t + 1) / 12.0)
                   for t in range(p.proj_len()))
        assert p.pv_benefits() == pytest.approx(want, rel=1e-12), (s_point, month)
        assert p.annuity_dis() == pytest.approx(
            want / (p.amount_payable_pp(0) * p.policy_count()), rel=1e-12), (s_point, month)
    fut, s4 = _row(sec_model, "future", 4, -13), _point(s_model, 4)
    assert fut.pv_benefits() == pytest.approx(
        s4.pv_benefits() * (1.0 + DISC) ** (-13 / 12.0), rel=1e-12)
    for p in (twin, fut, _row(sec_model, "derived", 1, 60)):
        assert [p.disc_factor(t) for t in (0, 11, 12)] == [
            (1.0 + DISC) ** (-(t + 1) / 12.0) for t in (0, 11, 12)]


@pytest.mark.parametrize("grid", GRIDS)
def test_the_committed_rows_continue_their_s_points(sec_model, s_model, tmp_path, grid):
    """Each committed row in force, or issued later, is its S point from its month on.

    T6 compares a float to 1e-12, which pins a small count only to that much of itself, so
    each committed row is compared with its S point frame by frame and cell by cell, at the
    shipped assumptions (USLIB-SEC-PLAN.md §7.1, *Precised at M3*, item 11): the derived
    rows from their months, and the row issued 13 months on from S's start, all to 1e-9
    relative with no absolute floor but on the residuals, every cell but those expense
    inflation moves (:func:`_continues_s`), which the inflation test holds.  The twins are
    T1's and T2's.  The row of S's claim on the active-lives basis at its month 12 is
    compared under :data:`FLAT_LAPSE`, read by S and SEC alike, on which S's restarted
    clock lapses as the twin's does: its state at month 12 is the shipped table's, whose
    first year's rate the flat one is.  The two rows read from S under an RPI of their own
    continue S under that RPI, which the shipped one replaces from the valuation date, and
    their own test holds them.  Each S point is swept here first (:func:`_sweep_s`), so
    that the comparison reaches every cell S evaluates, whatever an earlier test has done
    with the module's S model.  The default run takes the rows among :data:`CORE_POINTS`,
    and the full grid the rest.
    """
    table = sec_model.Data.model_point_table()
    s_table = s_model.Data.model_point_table()
    found, flat = [], None
    try:
        for point_id in table.index:
            kind, month = table.at[point_id, "row_kind"], int(table.at[point_id,
                                                                       "source_mth"])
            policy = table.at[point_id, "source_policy_id"]
            s_point = int(s_table.index[s_table["policy_id"] == policy][0])
            if (kind == "twin" or (s_point, month) in SPEC.derived_refs
                    or not _on_grid(grid, point_id)):
                continue
            if s_point == 7:
                if flat is None:
                    flat = (mx.read_model(temp_inputs(tmp_path / "s", model_path(TWIN),
                                                      edits=FLAT_LAPSE),
                                          name=_name("flat_s")),
                            mx.read_model(_sec_inputs(tmp_path / "sec", _committed(),
                                                      edits=FLAT_LAPSE),
                                          name=_name("flat_sec")))
                s_proj, sec_proj = _point(flat[0], 7), _point(flat[1], point_id)
            else:
                s_proj, sec_proj = _point(s_model, s_point), _point(sec_model, point_id)
            _sweep_s(s_proj)
            found += [f"point {point_id}: {line}"
                      for line in _continues_s(s_proj, sec_proj, month)]
    finally:
        for model in flat or ():
            model.close()
    assert not found, found[:20]


def test_the_rows_read_under_an_rpi_of_their_own_continue_s_under_it(sec_model):
    """The two committed rows S reaches only under an RPI of its own are S's under it (C2).

    At ``IP_UK_S``'s flat 3% no state holds a lapse shocked by escalation, nor an increase
    capped, so the spec restates the anchor cell at its month 40 from S run under an RPI of
    5%, and the female cell at its month 30 from S under 12% (the spec's ``derived_refs``),
    and C2 freezes both.  Three things are held of each:

    * the row is S's state under that RPI: S read under it holds, at the row's month, the
      row's count, its healthy share and its claim cohorts, and the month before, its
      benefit and premium;
    * set on this model too, that RPI gives the row S's path: it continues S's projection
      from its month on in every cell, over the whole of both frames, as the splice
      compares them (:func:`_continues_s`);
    * at today's References, which take over from the valuation date, the benefit and the
      premium are S's under that RPI until the row's next anniversary, and from it step at
      today's 3% and 4.5%.
    """
    for (s_point, month), refs in SPEC.derived_refs.items():
        label = _label(sec_model.Data.model_point_table(), "derived", s_point, month)
        s = mx.read_model(model_path(TWIN), name=_name("s_refs"))
        sec = mx.read_model(model_path(SEC), name=_name("sec_refs"))
        try:
            for model in (s, sec):
                for ref, value in refs.items():
                    setattr(model.Projection, ref, value)
            sp, row = _point(s, s_point), _point(sec_model, label)
            count = sp.pols_if(month)
            assert row.policy_count() == pytest.approx(count, rel=1e-12)
            assert row.pols_active_init() == pytest.approx(sp.pols_active(month) / count,
                                                           rel=1e-12)
            held = sp.sick_cohorts(month)
            assert [row.pols_sick_dur_init(z) for z in range(1, len(held) + 1)] == (
                pytest.approx([h / count for h in held], rel=1e-12, abs=0.0))
            assert row.benefit_pp_init() == pytest.approx(sp.benefit_pp(month - 1),
                                                          rel=1e-12)
            assert row.premium_pp_init() == pytest.approx(sp.premium_pp(month - 1),
                                                          rel=1e-12)
            _sweep_s(sp)
            assert _continues_s(sp, _point(sec, label), month) == []
            anniversary = 12 - month % 12
            for t in range(anniversary):
                assert row.benefit_pp(t) == pytest.approx(sp.benefit_pp(month + t),
                                                          rel=1e-12), t
                assert row.premium_pp(t) == pytest.approx(sp.premium_pp(month + t),
                                                          rel=1e-12), t
            assert row.benefit_pp(anniversary) == pytest.approx(
                row.benefit_pp_init() * 1.03, rel=1e-12)
            assert row.premium_pp(anniversary) == pytest.approx(
                row.premium_pp_init() * 1.045, rel=1e-12)
        finally:
            sec.close()
            s.close()


def test_the_healthy_share_is_read_from_the_model_point(sec_model, tmp_path):
    """The healthy share of the count is the point's, not rebuilt (K14).

    ``IP_UK_S`` opens an active cell all healthy and a claim all in claim, so a model that
    read the shares from ``status`` would pass every comparison with S's twins.  So the
    claim on the active-lives basis at its month 12, 0.3913 of it healthy, its recoveries
    back in health, is opened with half its count healthy and its cohorts scaled to the
    other half: it opens its healthy lives and its lives in claim at the shares the row
    holds, and its premiums, paid by the healthy lives alone, follow them.
    """
    row = _label(_committed(), "derived", 7, 12)
    share = _committed().at[row, "pols_active_init"]
    scale = 0.5 / (1.0 - share)

    def cohorts(frame):
        mine = frame["point_id"] == row
        return frame.assign(pols_sick_dur_init=frame["pols_sick_dur_init"].where(
            ~mine, frame["pols_sick_dur_init"] * scale))

    model = _read_edited(tmp_path, _set("pols_active_init", [row], 0.5), cohorts)
    try:
        p, q = _point(model, row), _point(sec_model, row)
        count = p.policy_count()
        assert (p.pols_active(0), q.pols_active(0)) == (count * 0.5, count * share)
        assert p.pols_sick(0) == pytest.approx(count * 0.5, rel=1e-12)
        assert p.premiums(0) == p.premium_pp(0) * (count * 0.5)
        assert q.premiums(0) == q.premium_pp(0) * (count * share)
        for z in range(1, 14):
            assert p.pols_sick_dur(0, z) == pytest.approx(q.pols_sick_dur(0, z) * scale,
                                                          rel=1e-12, abs=0.0), z
    finally:
        model.close()


def test_the_claim_cohorts_are_read_from_the_model_point(sec_model, tmp_path):
    """The lives in claim at each claim duration are the point's, not rebuilt (K14).

    ``IP_UK_S`` seeds a claim in one cohort, ``claim_duration_months``, and builds the rest
    from the inceptions since issue, so a model that rebuilt them from the history would
    pass the splice.  So the anchor cell at 60 is opened with its lives in claim at
    duration 5 moved to duration 17, a claim year on: the cohort vector opens with them
    there, and they recover at the second claim year's rate, 0.25 a year, where at
    duration 5 the first year's 0.40 would apply; every other cohort is the committed
    row's.
    """
    row = _label(_committed(), "derived", 1, 60)

    def moved(frame):
        frame = frame.copy()
        mine = frame["point_id"] == row
        five = frame.index[mine & (frame["z"] == 5)][0]
        later = frame.index[mine & (frame["z"] == 17)][0]
        frame.loc[later, "pols_sick_dur_init"] += frame.at[five, "pols_sick_dur_init"]
        return frame.drop(index=five).reset_index(drop=True)

    model = _read_edited(tmp_path, lambda t: t, moved)
    try:
        p, q = _point(model, row), _point(sec_model, row)
        lives = q.pols_sick_dur(0, 5)
        assert lives > 0.0 and p.pols_sick_dur(0, 5) == 0.0
        assert p.pols_sick_dur(0, 17) == pytest.approx(q.pols_sick_dur(0, 17) + lives,
                                                       rel=1e-12)
        assert [p.pols_sick_dur(0, z) for z in range(1, 61) if z not in (5, 17)] == (
            pytest.approx([q.pols_sick_dur(0, z) for z in range(1, 61)
                           if z not in (5, 17)], rel=1e-12, abs=0.0))
        assert (p.rec_rate(5), p.rec_rate(17)) == (0.4, 0.25)
        assert p.pols_recovery(0) - q.pols_recovery(0) == pytest.approx(
            lives * (p.rec_rate_mth(17) - p.rec_rate_mth(5)), rel=1e-9)
    finally:
        model.close()


def _history_under(rpi, s_point, month):
    """The benefit and premium ``IP_UK_S``, run under an RPI of ``rpi``, carries into S month
    ``month`` on ``s_point``: its ``benefit_pp(month - 1)`` and ``premium_pp(month - 1)``,
    the opening state a row restated there under that RPI holds, a history the contract
    can have."""
    s = mx.read_model(model_path(TWIN), name=_name("history"))
    try:
        s.Projection.rpi_rate = rpi
        sp = _point(s, s_point)
        return sp.benefit_pp(month - 1), sp.premium_pp(month - 1)
    finally:
        s.close()


def test_the_benefit_is_read_from_the_model_point(sec_model, tmp_path):
    """The benefit entering month 0 is the point's, not rebuilt from issue (K14).

    ``IP_UK_S`` rebuilds an RPI cell's benefit from issue at today's flat ``rpi_rate``, so
    a model that did the same would pass the splice.  So the anchor cell at 60 is opened
    with the history ``IP_UK_S`` gives it at its month 60 under an RPI of 5%, a benefit of
    2,000 x 1.05^4 beside a premium of 35 x 1.075^4, and valued under today's 3%: it pays
    that benefit times 1.03 from ``t = 0``, month 0's anniversary step at today's RPI,
    through policy year 6, and times 1.03 again from ``t = 12``, where a model that rebuilt
    it from issue at 3% would pay 2,000 x 1.03^5; its claims pay it on the lives in claim.
    The committed row's own benefit, 2,000 x 1.03^4, projects as that.
    """
    row = _label(_committed(), "derived", 1, 60)
    benefit, premium = _history_under(0.05, 1, 60)
    assert (benefit, premium) == (pytest.approx(2000.0 * 1.05 ** 4, rel=1e-15),
                                  pytest.approx(35.0 * 1.075 ** 4, rel=1e-15))
    model = _read_edited(tmp_path, _then(_set("benefit_pp_init", [row], benefit),
                                         _set("premium_pp_init", [row], premium)))
    try:
        p, q = _point(model, row), _point(sec_model, row)
        for t, years in ((0, 1), (11, 1), (12, 2), (299, 25)):
            assert p.benefit_pp(t) == pytest.approx(benefit * 1.03 ** years, rel=1e-12), t
        assert p.claims(0, _code(p, "BENEFIT")) == pytest.approx(
            p.benefit_pp(0) * p.pols_sick_surv(0), rel=1e-15)
        assert q.benefit_pp_init() == pytest.approx(2000.0 * 1.03 ** 4, rel=1e-12)
        assert q.benefit_pp(0) == pytest.approx(2000.0 * 1.03 ** 5, rel=1e-12)
        assert p.benefit_pp(0) > q.benefit_pp(0) * 1.07
    finally:
        model.close()


def test_the_premium_is_read_from_the_model_point(sec_model, tmp_path):
    """The premium entering month 0 is the point's, not rebuilt from issue (K14).

    ``IP_UK_S`` rebuilds an RPI cell's premium from issue at 1.5 times today's flat
    ``rpi_rate``, as it does the benefit.  So the anchor cell at 60 is opened, as in the
    test above, with the history ``IP_UK_S`` gives it at its month 60 under an RPI of 5%, a
    premium of 35 x 1.075^4 beside a benefit of 2,000 x 1.05^4, and valued under today's
    3%: it charges that premium times 1.045 from ``t = 0`` through policy year 6, and times
    1.045 again from ``t = 12``, on its healthy lives, where a model that rebuilt it from
    issue at 3% would charge 35 x 1.045^5.  The committed row's own, 35 x 1.045^4,
    projects as that.
    """
    row = _label(_committed(), "derived", 1, 60)
    benefit, premium = _history_under(0.05, 1, 60)
    model = _read_edited(tmp_path, _then(_set("benefit_pp_init", [row], benefit),
                                         _set("premium_pp_init", [row], premium)))
    try:
        p, q = _point(model, row), _point(sec_model, row)
        for t, years in ((0, 1), (11, 1), (12, 2), (299, 25)):
            assert p.premium_pp(t) == pytest.approx(premium * 1.045 ** years, rel=1e-12), t
        assert p.premiums(0) == p.premium_pp(0) * p.pols_active(0)
        assert q.premium_pp_init() == pytest.approx(35.0 * 1.045 ** 4, rel=1e-12)
        assert p.premium_pp(0) > q.premium_pp(0) * 1.11
    finally:
        model.close()


def test_an_anniversary_at_the_valuation_date_is_the_projection_s_first_event(sec_model):
    """The columns are measured before month 0's events, and the anniversary's increase is
    the projection's, at today's References (D6, as precised at uslib's M7; K14).

    The anchor cell valued on its first anniversary, ``d = 12``, holds the first year's
    benefit and premium, 2,000 and 35, which ``IP_UK_S`` gives in policy month 11, and its
    first escalation is made at ``t = 0``: 3% on the benefit and 4.5% on the premium, at
    today's RPI, so that it pays 2,060 and charges 36.575 through policy year 2, steps again
    at ``t = 12``, and lapses at policy year 2's rate from ``t = 0``.  With the RPI set to
    5% on a model just read (K7), the step at ``t = 0`` is 5% and 7.5%, which shocks its
    lapses from month 0 by 1.05; read after month 0's step, as the instant first was, the
    columns would hold 2,060 and 36.575, at the 3% the history does not have.
    """
    shipped = _row(sec_model, "derived", 1, 12)
    assert (shipped.duration_mth_init(), shipped.duration_init()) == (12, 0)
    assert (shipped.benefit_pp_init(), shipped.premium_pp_init()) == (2000.0, 35.0)
    for t in (0, 11):
        assert shipped.benefit_pp(t) == pytest.approx(2060.0, rel=1e-15), t
        assert shipped.premium_pp(t) == pytest.approx(36.575, rel=1e-15), t
    assert shipped.benefit_pp(12) == pytest.approx(2000.0 * 1.03 ** 2, rel=1e-15)
    assert (shipped.policy_year(0), shipped.lapse_rate(0)) == (2, 0.08)
    model = mx.read_model(model_path(SEC), name=_name("instant"))
    try:
        model.Projection.rpi_rate = 0.05
        row = _row(model, "derived", 1, 12)
        assert row.benefit_pp(0) == pytest.approx(2100.0, rel=1e-15)
        assert row.premium_pp(0) == pytest.approx(37.625, rel=1e-15)
        assert row.esc_lapse_factor(0) == pytest.approx(1.05, rel=1e-15)
        assert row.lapse_rate(0) == pytest.approx(0.084, rel=1e-15)
    finally:
        model.close()


def test_the_cumulative_counts_restart_on_the_books(sec_model, s_model):
    """The cumulative deaths, lapses and exits count from ``t_entry()`` (D5).

    On the anchor cell in force at 60 each is 0.0 at ``t = 0``, where ``IP_UK_S``'s at month
    60 counts the five years before, and adds each month's own from there:
    ``pols_dead_cum(t + 1)`` is ``pols_dead_cum(t)`` plus the deaths of month ``t`` in both
    states, and so S's at ``61 + t`` less S's at 60, as the splice holds its increments.  On
    the twin of the claim on the exit basis, the exits are its recoveries, from its month 0.
    """
    p, s = _row(sec_model, "derived", 1, 60), _point(s_model, 1)
    assert (p.pols_dead_cum(0), p.pols_lapse_cum(0), p.pols_exit_cum(0)) == (0.0, 0.0, 0.0)
    assert s.pols_dead_cum(60) > 0.0 and s.pols_lapse_cum(60) > 0.0
    for t in (0, 1, 11, 12, 298):
        assert p.pols_dead_cum(t + 1) == (
            p.pols_dead_cum(t) + p.pols_death_active(t) + p.pols_death_sick(t)), t
        assert p.pols_lapse_cum(t + 1) == p.pols_lapse_cum(t) + p.pols_lapse(t), t
        assert p.pols_dead_cum(t + 1) == pytest.approx(
            s.pols_dead_cum(61 + t) - s.pols_dead_cum(60), rel=1e-9), t
    claim = _row(sec_model, "twin", 2, 0)
    assert claim.pols_exit_cum(1) == claim.pols_exit(0) > 0.0


def test_expense_inflation_runs_on_the_valuation_clock(sec_model, s_model):
    """The expense loads are in valuation-date pounds, for every point alike (D7).

    At the shipped 3%, the factor at ``t`` is ``1.03^(t // 12)`` on every point, whatever
    its duration, stepping on the valuation date's anniversaries.  So the anchor cell in
    force 60 months pays S's month-``60 + t`` expenses with S's factor taken out and this
    model's put in: at ``t = 0`` S's less 1.03^5, the inflation S has applied since issue.
    And the female cell issued 13 months on pays S's expenses with a year more of inflation
    from its ``t = 24``: its factor at ``t`` is ``1.03^(t // 12)``, where S's at ``t - 13`` is
    ``1.03^((t - 13) // 12)``.  This is the only test that sees inflation run on the
    valuation clock: the splice sets the rate to 0, and on a point issued at ``t = 0``, and
    on the twins of S's claims, which S opens at the valuation date, the clocks agree.
    """
    assert sec_model.Projection.inflation_rate == INFLATION
    p, s = _row(sec_model, "derived", 1, 60), _point(s_model, 1)
    fut, s4 = _row(sec_model, "future", 4, -13), _point(s_model, 4)
    for t in (0, 11, 12, 30):
        assert p.inflation_factor(t) == fut.inflation_factor(t) == (
            (1 + INFLATION) ** (t // 12)), t
    for t in range(p.proj_len()):
        assert p.expenses(t) == pytest.approx(
            s.expenses(60 + t) / s.inflation_factor(60 + t) * p.inflation_factor(t),
            rel=1e-12), t
    assert p.expenses(0) == pytest.approx(s.expenses(60) / (1 + INFLATION) ** 5, rel=1e-12)
    for t in range(13, fut.proj_len()):
        assert fut.expenses(t) == pytest.approx(
            s4.expenses(t - 13) * (1 + INFLATION) ** (t // 12 - (t - 13) // 12),
            rel=1e-12), t


@pytest.mark.parametrize("rpi, esc, shock", [(-0.02, 0.0, 1.0), (0.05, 0.05, 1.05),
                                              (0.12, 0.10, 1.2)])
def test_the_rpi_increases_are_floored_at_0_and_capped(rpi, esc, shock):
    """An RPI point's increases are the RPI floored at 0 and capped at 10%, and premiums
    growing past 5% a year shock its lapses (K14).

    On the anchor cell in force at 60 the benefit steps at ``t = 0`` and each anniversary
    after by ``max(rpi, 0)`` capped at ``esc_cap``, 10%, and the premium by 1.5 times that;
    from policy year 2 its lapses are shocked by ``1 + 2 max(0, 1.5 j - 0.05)``.  At an RPI
    of -2% the floor holds the amounts and leaves the lapses unshocked; at 5% the premium
    grows 7.5% a year and the lapses are shocked by 1.05; at 12% the cap holds the increase
    to 10%, the premium's to 15%, and the shock to 1.2.  The level cell at 30 never moves.
    The RPI is set on a model just read (K7).
    """
    model = mx.read_model(model_path(SEC), name=_name("rpi"))
    try:
        model.Projection.rpi_rate = rpi
        p = _row(model, "derived", 1, 60)
        assert p.esc_rate() == esc
        for t, years in ((0, 1), (11, 1), (12, 2), (299, 25)):
            assert p.benefit_pp(t) == pytest.approx(
                p.benefit_pp_init() * (1 + esc) ** years, rel=1e-12), t
            assert p.premium_pp(t) == pytest.approx(
                p.premium_pp_init() * (1 + 1.5 * esc) ** years, rel=1e-12), t
            assert p.esc_lapse_factor(t) == pytest.approx(shock, rel=1e-12), t
        level = _row(model, "derived", 3, 30)
        assert (level.esc_rate(), level.benefit_pp(299), level.premium_pp(299)) == (
            0.0, 2000.0, 35.0)
    finally:
        model.close()


# ---------------------------------------------------------------------------
# The caps
#
# The mortality and inception caps are written with their bound second, min(q, 1.0), as
# IP_UK_S writes them since M0, and the lapse rate's bound first, min(1.0, w), S's; each
# binds only under References the product does not ship.  Active-life mortality times 100
# passes 1 at attained age 61, on S points 1 and 3 from month 312 and on point 6 from
# month 72; inception under a cycle factor of 50 at age 54 on the female cell, from month
# 144; and the lapse rate at an RPI of 12% under a shock slope of 300 from the first
# anniversary on every RPI point.  Each as (the bound, the References, the annual rate
# capped, the S point, its first capped month, and a committed row of that point).
CAPS = [
    ("the mortality cap", {"mort_active_factor": 100.0}, "mort_rate", 6, 72,
     ("derived", 6, 118)),
    ("the inception cap", {"cycle_factor": 50.0}, "inception_rate", 4, 144,
     ("derived", 4, 13)),
    ("the lapse rate's bound", {"rpi_rate": 0.12, "esc_lapse_slope": 300.0}, "lapse_rate",
     1, 12, ("derived", 1, 12)),
]


@pytest.mark.parametrize("bound, refs, cell, s_point, first, row", CAPS,
                         ids=[c[0] for c in CAPS])
def test_a_rate_past_1_is_capped_in_both_models(bound, refs, cell, s_point, first, row):
    """Where an annual rate passes 1, both models' rate is the float 1.0, and every
    healthy life leaves health in the month.

    On S's point, its twin and a committed row of the point, read with :data:`CAPS`'
    References set on S and SEC alike before either computes anything (K7): the annual rate
    and the monthly rate are 1.0 from the first capped month to the end of the frame, the
    float, not the int 1, which compares equal to it, and floats below 1 before.  So in each
    capped month no healthy life is left at its end: deaths, lapses and inceptions take
    them all, by death under the mortality cap, by lapse under the lapse bound, and by a
    claim under the inception cap.  Every report holds finite floats.  On the committed row
    the first capped month is on its own clock.
    """
    s = mx.read_model(model_path(TWIN), name=_name("cap_s"))
    sec = mx.read_model(model_path(SEC), name=_name("cap"))
    try:
        for model in (s, sec):
            for ref, value in refs.items():
                setattr(model.Projection, ref, value)
        cases = ((_point(s, s_point), first), (_row(sec, "twin", s_point, 0), first),
                 (_row(sec, *row), max(first - row[2], 0)))
        for p, start in cases:
            n = p.proj_len()
            assert 0 <= start < n, (bound, start, n)
            for name in (cell, f"{cell}_mth"):
                rates = [p.cells[name](t) for t in range(n)]
                assert all(type(r) is float and r < 1.0 for r in rates[:start]), (bound, name)
                assert [(type(r), r) for r in rates[start:]] == [(float, 1.0)] * (
                    n - start), (bound, name)
            for t in range(start, n):
                left = (p.pols_active(t) - p.pols_death_active(t) - p.pols_lapse(t)
                        - p.pols_inception(t))
                assert left == pytest.approx(0.0, abs=1e-12), (bound, t)
            for report in ("result_cf", "result_states"):
                frame = p.cells[report]()
                assert np.isfinite(frame.to_numpy(dtype=float)).all(), (bound, report)
    finally:
        sec.close()
        s.close()


# The inception rate's floor at 0, max(0.0, r) before the overlay and the cap, which no
# shipped schedule reaches: each, one shape scaled, extrapolates below its first pivot, 30,
# to 0 only below age 13.3, under the youngest issue age.  Data accepts a schedule that
# falls below 0 above it, so the floor is spliced on one: in a copy of the inception table,
# variant 9's schedule, male, class 4, 4 weeks, made 0.0005 at its first pivot and 0.01 at
# its second, extrapolates below 0 under age 29.7, and variant 9, issued at 22, is floored
# until it is 30, in its first 96 months.
FLOOR_INCEPTION = {INCEPTION: _then(
    _written("inception_rate", 0.0005, _pivot("M", 4, 4, 30)),
    _written("inception_rate", 0.01, _pivot("M", 4, 4, 35)))}
FLOOR_MTHS = (1, 12, 95)


def test_the_inception_floor_continues_s_on_a_schedule_below_0(tmp_path):
    """The inception rate's floor at 0 holds where a schedule falls below 0 (§6.3).

    ``IP_UK_S`` floors the interpolated inception rate at 0 before the overlay and the
    cap, and so does this model, as its C step must; but no shipped schedule reaches the
    floor, so no other test would see it dropped.  ``Data`` accepts a schedule that falls
    below 0 above the youngest issue age, so one is spliced here (:data:`FLOOR_INCEPTION`),
    with the main set's References (:data:`MAIN`) in S and SEC alike: variant 9, issued at
    22, has an inception rate of 0 in S in each of its first 96 months, and its twin and
    the rows restated at its months 1, 12 and 95, each opening at an inception rate of 0,
    are S's from their months on, in every cell, as the splice compares them
    (:func:`_compare`).
    """
    s = mx.read_model(temp_inputs(tmp_path / "s", model_path(TWIN),
                                  model_points=_s_table_with_variants((9,)),
                                  edits=FLOOR_INCEPTION), name=_name("floor_s"))
    sec = None
    try:
        for ref, value in MAIN.items():
            setattr(s.Projection, ref, value)
        spec = dataclasses.replace(SPEC, derived=tuple((9, d) for d in FLOOR_MTHS),
                                   future=(), derived_refs={})
        table, companions = build_sec_table(spec, s)
        sec = mx.read_model(_sec_inputs(tmp_path / "sec", table, companions[COHORTS],
                                        edits=FLOOR_INCEPTION), name=_name("floor"))
        for ref, value in MAIN.items():
            setattr(sec.Projection, ref, value)
        s_proj = _point(s, 9)
        _sweep_s(s_proj)
        assert [t for t in range(s_proj.proj_len())
                if s_proj.inception_rate(t) == 0.0] == list(range(96))
        found = []
        for case in (("twin", 9, 0), *(("derived", 9, d) for d in FLOOR_MTHS)):
            row = _row(sec, *case)
            assert row.inception_rate(0) == 0.0, case
            found += [f"{case}: {line}"
                      for line in _compare(s_proj, row, case[2], SPLICE_EXEMPT)]
        assert not found, found[:20]
    finally:
        if sec is not None:
            sec.close()
        s.close()


# A NaN sent to a bound written with its bound second, as (the bound, the References set to
# NaN on a model read for the test before it computes anything, a replacement of
# Data.mort_rate_sick_array's formula or None, the S point whose twin reads it, and the
# calls that must give the float NaN).  The mortality cap reads mort_active_factor, the
# inception cap cycle_factor, and the in-claim mortality's cap the termination table's
# array, which is replaced by one that holds NaN for every in-claim mortality, which Data's
# check of the file does not see.  A bound written first would turn the NaN into the bound:
# a blank input read as certain death or a certain claim.  proj_len() refuses a Reference
# that is not a number and Data a rate that is not, so no report projects one; the calls
# here read no frame.
def _nan_sick_mortality():
    """``Data.mort_rate_sick_array`` as a formula holding NaN at every claim duration year:
    run in the Data Space, where ``termination_last_year`` is its cell and ``np`` its
    Reference."""
    return np.full(termination_last_year() + 1, np.nan)             # noqa: F821


NAN_BOUNDS = [
    ("the mortality cap, min(q, 1.0)", {"mort_active_factor": NAN}, None, 6,
     [("mort_rate", (0,)), ("mort_rate", (100,)), ("mort_rate_mth", (72,))]),
    ("the inception cap, min(i, 1.0)", {"cycle_factor": NAN}, None, 4,
     [("inception_rate", (0,)), ("inception_rate", (150,)), ("inception_rate_mth", (144,))]),
    ("the in-claim mortality's cap, min(q, 1.0)", {}, _nan_sick_mortality, 2,
     [("mort_rate_sick", (1,)), ("mort_rate_sick", (60,)), ("mort_rate_sick_mth", (13,))]),
]


@pytest.mark.parametrize("bound, refs, table, s_point, calls", NAN_BOUNDS,
                         ids=[c[0] for c in NAN_BOUNDS])
def test_a_nan_that_reaches_a_bound_stays_nan(bound, refs, table, s_point, calls):
    """A NaN that reaches a cap written with its bound second stays NaN, and is not read as
    the bound.

    ``min`` keeps its first argument unless a later one compares smaller, in modelx and
    compiled alike, and no comparison with NaN holds, so with its bound first a cap would
    turn a NaN into 1: certain death, or a certain claim.  The three caps are written with
    the bound second, as ``IP_UK_S`` writes them (:data:`NAN_BOUNDS`): what feeds each is
    made NaN on a model read for the test, and every call must give the float NaN.  The
    cells are called on their own, without the frame: ``proj_len()`` refuses each Reference
    at NaN before a report reaches its cap (the domain test), and ``Data`` each rate.  The
    lapse rate's bound and the recovery rate's keep ``IP_UK_S``'s order, the bound first,
    and the domains and ``Data`` keep a NaN from each.
    """
    model = mx.read_model(model_path(SEC), name=_name("nan"))
    try:
        for ref, value in refs.items():
            setattr(model.Projection, ref, value)
        if table is not None:
            model.Data.cells["mort_rate_sick_array"].formula = table
        p = _row(model, "twin", s_point, 0)
        lost = [f"{name}{args} = {value!r}" for name, args in calls
                for value in [p.cells[name](*args)]
                if not (type(value) is float and math.isnan(value))]
        assert not lost, f"{bound} loses a NaN: {lost}"
    finally:
        model.close()


@pytest.mark.parametrize("check, resid", [
    ("check_pols_roll_fwd", "check_pols_roll_fwd_resid"),
    ("check_states", "check_states_resid")])
def test_a_check_fails_a_residual_that_is_not_a_number(check, resid):
    """Each check returns False where its residual is NaN (§7.1, item 11).

    A check is ``abs(resid) <= tolerance`` over the frame, which no NaN passes, as
    ``IP_UK_S``'s is; but no input the frame accepts gives a NaN residual, so the residual's
    formula is replaced, on a model read for the test, by one that returns NaN in every
    month.  Then the check is the bool False on every committed point, where with its own
    formula it is True, as it is first shown on the twin of the anchor cell and on the
    anchor cell in force at 60, each released once read.  A check that asked whether any
    residual was past its tolerance would pass NaN.
    """
    model = mx.read_model(model_path(SEC), name=_name("nan_resid"))
    try:
        table = model.Data.model_point_table()
        for kind, s_point, month in (("twin", 1, 0), ("derived", 1, 60)):
            key = _row_key(model, kind, s_point, month)
            assert projection(model, key).cells[check]() is True, (kind, s_point, month)
            _release(model, key)
        model.Projection.cells[resid].formula = lambda t: float("nan")
        for key, point_id in zip(point_keys(model), table.index):
            p = projection(model, key)
            assert math.isnan(p.cells[resid](0)), point_id
            assert p.cells[check]() is False, point_id
            _release(model, key)
    finally:
        model.close()


def _outside_cover_faults(p, where, months):
    """Where ``p``, an ItemSpace that has evaluated nothing, departs from OUTSIDE_COVER.

    Every cell of :data:`OUTSIDE_COVER`, ``pols_if_at`` at each timing, ``claims`` at each
    kind and in total, and the cohorts at every claim duration of the vector, 0 to
    ``max_dur()``, all zeros, at each of ``months``, every one outside the frame.  Then
    whether any of :data:`IN_COVER_ONLY` was evaluated on the way, which only a fresh
    ItemSpace can say.  A cell that raises is reported as a fault too, so the scan goes on.
    """
    faults = []
    n = p.max_dur()
    for t in months:
        calls = [(name, (t,), want) for name, want in OUTSIDE_COVER.items()]
        calls += [("pols_if_at", (t, _code(p, timing)), 0.0) for timing in TIMINGS]
        calls += [("claims", (t, _code(p, kind)), 0.0) for kind in (*KINDS, "ALL")]
        calls += [("pols_sick_dur", (t, z), 0.0) for z in range(n + 1)]
        for name, args, want in calls:
            try:
                got = p.cells[name](*args)
            except Exception as err:        # reported, so the scan goes on
                faults.append(f"{where}: {name}{args} raised {_raised(err)}")
                continue
            if got != want or type(got) is not type(want):
                faults.append(f"{where}: {name}{args} = {got!r}, not {want!r}"[:200])
    read = {}
    for name in IN_COVER_ONLY:
        months_read = sorted(args[0] for args in _cached_args(p.cells[name])
                             if not p.is_active(args[0]))
        if months_read:
            read[name] = months_read
    if read:
        faults.append(f"{where}: evaluated outside the frame: {read}")
    return faults


def test_every_guarded_cell_holds_its_outside_cover_value(spliced):
    """Outside the frame each cell holds :data:`OUTSIDE_COVER`'s value, and reads no rate.

    On every committed point, in every month before issue and in the first month after the
    frame, ``t = proj_len()``, on a model that evaluates nothing else.  So afterwards none of
    :data:`IN_COVER_ONLY` may hold a value outside the frame at all: ``is_active``'s
    docstring promises that outside cover no count evaluates a rate, and no table is read
    at a policy year or an attained age the policy does not have.

    The committed table's one point issued after the valuation date is the female cell, so
    the same scan runs on the splice's future rows, the core's or, with
    ``UKLIB_SEC_FULL=1``, all of them: the anchor cell, the level cell, an active cell on
    the exit basis and the cap's set among them.  Each row is made afresh first and released
    after.

    Several of these guards change no number the frame shows: once the counts are zero
    outside the frame, every cash flow is too, and an unguarded value multiplies a zero
    count.  They are held here because they are what the docstrings promise a caller, and
    because the C step needs them: a table read at a policy year or an age the contract
    does not have would wrap round in a compiled model rather than fail (USLIB-SEC-PLAN.md
    F4, R1).
    """
    faults = []
    model = mx.read_model(model_path(SEC), name=_name("cover"))
    try:
        table = model.Data.model_point_table()
        for key, point_id in zip(point_keys(model), table.index):
            p = projection(model, key)
            faults += _outside_cover_faults(p, f"point {point_id}",
                                            [*range(p.t_entry()), p.proj_len()])
    finally:
        model.close()
    futures = _selected(FUTURES, CORE_FUTURES)
    for rates, s_point, k in futures:
        sec = spliced.pair(rates)[1]
        key = _row_key(sec, "future", s_point, -k)
        if key in sec.Projection.itemspaces:
            _release(sec, key)
        try:
            p = projection(sec, key)
            faults += _outside_cover_faults(p, _case_id(rates, "future", s_point, -k),
                                            [*range(k), p.proj_len()])
        finally:
            _release(sec, key)
    assert futures and not faults, (
        f"{len(faults)} faults outside the frame, first:\n  " + "\n  ".join(faults[:20]))


def test_the_points_sum_row_by_row_into_a_block(spliced):
    """Row ``t`` is the same month on every point, so a block is its frames summed (D3).

    The twin of S's anchor cell, the anchor cell restated at month 12 and the anchor cell
    issued a month on, of the main splice set, summed as ``run_sec.py --block`` sums them,
    are indexed 0..360 and equal S's frame added to itself moved 12 months earlier and a
    month later.  A model whose frames sat on the policy clock would fail it.
    """
    s, sec = spliced.pair("main")
    keys = [_row_key(sec, "twin", 1, 0), _row_key(sec, "derived", 1, 12),
            _row_key(sec, "future", 1, -1)]
    try:
        frames = [projection(sec, key).result_cf() for key in keys]
    finally:
        for key in keys:
            _release(sec, key)
    block = pd.concat(frames).groupby(level="t").sum()
    sdf = _point(s, 1).result_cf()
    expected = pd.concat([sdf, sdf.set_axis(sdf.index - 12).loc[0:],
                          sdf.set_axis(sdf.index + 1)]).groupby(level=0).sum()
    assert list(block.index) == list(range(361))
    assert frame_mismatches(expected, block) == []


def _extract():
    """The committed table as an administration extract would hold it: without the
    generator's columns, nor ``IP_UK_S``'s ``status``, a label no formula reads, and
    labelled :data:`EXTRACT_LABELS`."""
    extract = _committed().drop(columns=[*generated_columns(SPEC), "status"])
    extract.index = pd.Index(EXTRACT_LABELS, name="point_id")
    return extract


def _extract_cohorts():
    """The committed claim cohorts under the extract's labels (:func:`_extract`)."""
    cohorts = _committed_cohorts()
    return cohorts.assign(point_id=cohorts["point_id"].map(_relabel_map()))


def _standing(p):
    """What ``run_sec.py`` says of point ``p`` at the valuation date, stated here."""
    d = p.duration_mth_init()
    if d < 0:
        return f"to be issued at t = {-d}, {-d} months after the valuation date"
    if d == 0:
        return "issued at the valuation date, t = 0"
    return (f"in force {d} months: policy year {p.policy_year(0)}, attained age {p.age(0)}, "
            f"{p.pols_if(0):.6f} in force, {p.pols_active(0):.6f} healthy, "
            f"{p.pols_sick(0):.6f} in claim")


def _product(p):
    """What ``run_sec.py`` says of point ``p``'s product, stated here."""
    return (f"{p.sex()}{p.age_at_entry()} occupation class {p.occ_class()}, "
            f"{p.deferred_weeks()}-week deferred period, benefit {p.benefit_mth():,.2f} a "
            f"month to age {p.expiry_age()}, premium {p.premium_mth():,.2f} a month, "
            f"escalation {p.escalation()}, recoveries {p.recovery_basis()}")


@pytest.mark.parametrize("grid", GRIDS)
def test_an_in_force_extract_needs_none_of_the_generator_columns(sec_model, tmp_path, grid):
    """The model reads the in-force interface and S's columns, never where a row came from,
    and names each point by its label, wherever the row stands.

    ``row_kind``, ``source_policy_id``, ``source_mth`` and ``source_refs`` record how the
    generator made each shipped row, from which S row, at which month and under which
    References, and an administration extract carries none of them, nor ``IP_UK_S``'s
    ``status``, the kind of S row a point was, which no formula reads.  Read without them,
    and with every label changed, in the table and its claim cohorts alike, every point
    projects what the committed table projects, in ``result_cf``, ``result_states`` and
    ``result_pols``, to 1e-12, and ``run_sec.py``, run beside that extract, prints the point
    without saying where it came from.  On every shipped row in force at the valuation date
    but the twins of S's claims ``source_mth`` equals ``duration_mth``, so a formula that
    read the one for the other would pass every test that leaves ``duration_mth`` as
    generated.  And a refusal names the extract's label.

    The default run compares :data:`CORE_POINTS` and runs the runner and the moved row, and
    the full grid compares the other committed points.
    """
    extract = _extract()
    absent = ("row_kind", "source_policy_id", "source_mth", "source_refs")
    assert absent == generated_columns(SPEC), generated_columns(SPEC)
    assert not set(absent) & set(extract.columns), list(extract.columns)
    folder = _sec_inputs(tmp_path / "extract", extract, _extract_cohorts())
    model = mx.read_model(folder, name=_name("extract"))
    try:
        table = model.Data.model_point_table()
        assert not {*generated_columns(SPEC), "status"} & set(table.columns)
        assert list(table.index) == list(EXTRACT_LABELS)
        for key, base_key, label in zip(point_keys(model), point_keys(sec_model),
                                        _committed().index):
            if not _on_grid(grid, label):
                continue
            mine, base = projection(model, key), projection(sec_model, base_key)
            for report in ("result_cf", "result_states", "result_pols"):
                assert frame_mismatches(base.cells[report](), mine.cells[report](),
                                        rtol=1e-12, atol=1e-12) == [], (key, report)
            _release(model, key)
    finally:
        model.close()
    if grid == "full":
        return
    runner = folder.parent / "run_sec.py"
    shutil.copy(model_path(SEC).parent / "run_sec.py", runner)
    label = extract.index[extract["policy_id"] == "IP-000001-M60"][0]
    out = _run_sec(runner, str(label))
    row = _row(sec_model, "derived", 1, 60)
    assert out.splitlines()[:2] == [
        f"model point {label}: IP-000001-M60 - {_product(row)}",
        f"at the valuation date: {_standing(row)}"]
    last = extract.index[extract["policy_id"] == "IP-000001-M359"][0]
    moved = _set("duration_mth", [last], 360)(extract)
    model = mx.read_model(_sec_inputs(tmp_path / "moved", moved, _extract_cohorts()),
                          name=_name("moved"))
    try:
        _refused(_point(model, last).result_cf,
                 f"point_id {last}: duration_mth 360 is at or past the policy end date, "
                 f"policy month 360, expiry age 65")
    finally:
        model.close()


def test_run_sec_prints_a_point_and_the_block(sec_model):
    """The runner prints one point, saying where it came from, and the block (D8).

    Each mode in an interpreter of its own, as a user runs it, with exit code 0 and ASCII
    output, so that it prints on a Windows console under any code page.  The numbers are
    the model's.  The anchor cell, the runner's default, with its lines at the valuation
    date, each asserted whole, so that a longer number cannot pass for the one asserted,
    and its first twelve rows of cash flows and counts.  Point 9, the anchor cell in force
    60 months; point 11, the claims-in-payment worked example restated at its month 24;
    and point 17, the female cell to be issued 13 months on: each with the lines that say
    where its row came from and where it stands, which only the committed table's generator
    columns can say.  And the block: a line for each committed point, in table order, its
    first twelve rows, which must be the committed points' frames summed row by row, as
    this test sums them, and those frames summed into projection years, each year's counts,
    in force, healthy and in claim, the ones of its first month.  Nothing else runs the
    runner on the committed table.
    """
    runner = model_path(SEC).parent / "run_sec.py"
    out = _run_sec(runner)
    anchor = _row(sec_model, "twin", 1, 0)
    assert out.splitlines()[:3] == [
        f"model point 1: IP-000001 (S's IP-000001) - {_product(anchor)}",
        "at the valuation date: issued at the valuation date, t = 0",
        "proj_len = 360 months from the valuation date (t = 0..359); the policy end date "
        "is policy month 360"]
    assert _product(anchor) == (
        "M35 occupation class 1, 26-week deferred period, benefit 2,000.00 a month to age "
        "65, premium 35.00 a month, escalation RPI, recoveries return_to_h")
    assert anchor.result_cf().head(12).round(2).to_string() in out
    assert anchor.result_pols().head(12).round(6).to_string() in out
    for point_id, case, origin, frame in (
            (9, ("derived", 1, 60), "S's IP-000001 at its month 60",
             "proj_len = 300 months from the valuation date (t = 0..299); the policy end "
             "date is policy month 360"),
            (11, ("derived", 2, 24), "S's IP-000002 at its month 24",
             "proj_len = 336 months from the valuation date (t = 0..335); the policy end "
             "date is policy month 372"),
            (17, ("future", 4, -13), "S's IP-000004, issued 13 months on",
             "proj_len = 229 months from the valuation date (t = 0..228); the policy end "
             "date is policy month 216")):
        p = _row(sec_model, *case)
        policy = sec_model.Data.model_point_table().at[point_id, "policy_id"]
        assert _run_sec(runner, str(point_id)).splitlines()[:3] == [
            f"model point {point_id}: {policy} ({origin}) - {_product(p)}",
            f"at the valuation date: {_standing(p)}", frame], point_id
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
    counts = ["pols_if", "pols_active", "pols_sick"]
    annual = block.drop(columns=counts).groupby(years).sum()
    for column in reversed(counts):
        annual.insert(0, column, block[column].groupby(years).first())
    assert annual.head(12).round(2).to_string() in out


# run_sec.py run as though it sat at /m/products/income_protection, in a products/ folder
# whose parent carries no build tool: the source compiled under that name, so that its own
# __file__ is it.
SHALLOW_RUN = """\
import sys
source = open(sys.argv[1], encoding="utf-8").read()
where = "/m/products/income_protection/run_sec.py"
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
    carries no tool.  Each must exit nonzero having printed nothing, and say why.  Neither
    needs modelx-cython, since neither gets as far as building.
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
    as ``source_refs`` records them, point 18's ``under rpi_rate 0.05``, and no other row's
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
    assert space["origin"](18) == (
        " (S's IP-000001 at its month 40, under rpi_rate 0.05)")


def _defaulted(model_name):
    """The cells of ``model_name``'s Projection with a parameter that has a default, sorted,
    read from its source, as the C step's build reads it."""
    source = (model_path(model_name) / "Projection" / "__init__.py").read_text(
        encoding="utf-8")
    return sorted(node.name for node in ast.parse(source).body
                  if isinstance(node, ast.FunctionDef)
                  and (node.args.defaults or any(node.args.kw_defaults)))


def test_no_cell_takes_a_default():
    """No cell has a defaulted parameter, ``IP_UK_S``'s ``claims(t, kind=None)`` among them
    (R12).

    A compiled model declares a defaulted parameter in its ``.pxd`` as ``long long x=*``,
    which the typing guard would read as a parameter of that name, so no cell here has one:
    ``IP_UK_S``'s one, ``claims``' ``kind=None``, the total, is ``claims(t, ALL)``, R12's
    total, as ``Term_UK_SEC``'s is.
    """
    assert _defaulted(TWIN) == ["claims"]
    assert _defaulted(SEC) == []


# The texts a computed cell may hold outside its refusals, beside a column's name read off
# the model point: none.  The kinds and the timings are int References (R9), as Term's,
# CI's, ULB's and WOL's are.
CODES = frozenset()

# IP_UK_S's tuple cells, which this model carries a cell an element (M8): a cell that calls
# one, to sum, index or step its tuple, would be IP_UK_S's form, which compiles to no C.
TUPLE_CELLS = frozenset({"sick_cohorts", "claim_rate_vectors"})

# The model point's text columns, which Data decodes to ints: a cell that reads one returns
# or compares a text.  policy_id, the generator's columns and status are labels no formula
# reads.  A text column reads as object under pandas 2 and as str under pandas 3, and
# is_string_dtype takes either.
TEXT_COLUMNS = frozenset(c for c in _committed().columns
                         if pd.api.types.is_string_dtype(_committed()[c]))

# The cells the static check leaves alone, each a reporting cell that stays Python
# (uk_registry's "reporting", R17): the three reports, which build DataFrames, and the five
# labels, which read and return a text column.  The checks are loops on C numbers here.
STATIC_EXEMPT = {
    "result_cf", "result_states", "result_pols", "sex", "escalation", "premium_basis",
    "status", "recovery_basis"}


def _static_findings(tree, exempt):
    """What the static check finds in ``tree``, the Projection's source parsed, every cell
    of ``exempt`` left out: ``(the cells read, [(cell, what it holds), ...])``.  A tuple
    that is the index of a subscript, ``[s, x]``, is a table read's, as C5 reads it, and no
    Python object."""
    built = (ast.Tuple, ast.List, ast.Set, ast.Dict, ast.GeneratorExp, ast.ListComp,
             ast.SetComp, ast.DictComp, ast.JoinedStr, ast.Lambda)
    found, read = [], set()
    for node in tree.body:
        if not isinstance(node, ast.FunctionDef):
            continue
        read.add(node.name)
        if node.name in exempt:
            continue
        raises = {id(n) for r in ast.walk(node) if isinstance(r, ast.Raise)
                  for n in ast.walk(r)}
        columns = {id(n) for s in ast.walk(node)
                   if isinstance(s, ast.Subscript) and isinstance(s.value, ast.Call)
                   and getattr(s.value.func, "id", None) == "model_point"
                   for n in ast.walk(s.slice)}
        indices = {id(s.slice) for s in ast.walk(node) if isinstance(s, ast.Subscript)}
        body = node.body[1:] if ast.get_docstring(node) is not None else node.body
        for inner in (n for statement in body for n in ast.walk(statement)):
            if id(inner) in raises:
                continue
            if isinstance(inner, built) and id(inner) not in indices:
                found.append((node.name, f"{type(inner).__name__} at line {inner.lineno}"))
            elif (isinstance(inner, ast.Constant) and isinstance(inner.value, str)
                  and inner.value not in CODES and id(inner) not in columns):
                found.append((node.name, f"the text {inner.value!r} at line "
                                         f"{inner.lineno}"))
            elif (isinstance(inner, ast.Call)
                  and getattr(inner.func, "id", None) in TUPLE_CELLS):
                found.append((node.name, f"reads the tuple cell {inner.func.id} at line "
                                         f"{inner.lineno}"))
            elif (isinstance(inner, ast.Constant) and inner.value in TEXT_COLUMNS
                  and id(inner) in columns):
                found.append((node.name, f"reads the text column {inner.value!r} at line "
                                         f"{inner.lineno}"))
    return read, found


def test_no_computed_cell_builds_a_python_object(sec_model):
    """No computed cell builds a tuple, a text or a generator but to raise (§6.3, *C*).

    The C step turned ``IP_UK_S``'s Python objects into the C forms UKLIB-SEC-PLAN.md §6.3
    lists, which M7's form of this test named one by one, so that only the reporting cells
    that stay Python are left (:data:`STATIC_EXEMPT`).  No other ``Projection`` cell holds
    a tuple but a table read's index, a list, a set, a dict, a comprehension, a generator
    or an f-string, or any text, but the name of a column it reads off ``model_point()``,
    outside a ``raise`` statement, read from the source as the build reads it; and none
    calls a cell of :data:`TUPLE_CELLS`, ``IP_UK_S``'s tuples, or reads one of
    :data:`TEXT_COLUMNS`, whose text it would return or compare.  ``try`` is allowed: a
    power that leaves the floats raises Python's ``OverflowError``, which the cell names.
    Every cell of the Space is read, and every exemption is a cell of it.  C5, in
    ``test_compiled_conventions_uk.py``, holds the compiled model's whole rule set; this
    holds the module's own, in seconds.

    The rules check themselves too, so that narrowing one cannot pass unseen: the text
    columns are found under pandas 2 and 3 alike, ``sex``, ``escalation`` and
    ``recovery_basis`` among them; and each exemption is needed, the scan flagging its cell
    once that one exemption is taken away, which keeps :data:`STATIC_EXEMPT` to the cells
    that stay Python.
    """
    tree = ast.parse(
        (model_path(SEC) / "Projection" / "__init__.py").read_text(encoding="utf-8"))
    read, found = _static_findings(tree, STATIC_EXEMPT)
    assert read == set(sec_model.Projection.cells)
    assert STATIC_EXEMPT <= read
    assert not found, found
    assert {"sex", "escalation", "recovery_basis"} <= TEXT_COLUMNS, sorted(TEXT_COLUMNS)
    needless = sorted(cell for cell in STATIC_EXEMPT
                      if cell not in {name for name, _ in
                                      _static_findings(tree, STATIC_EXEMPT - {cell})[1]})
    assert not needless, f"exempt, though the scan finds nothing in them: {needless}"


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
    outside the parentheses and quotes of the column, ``claims`` of ``claims(t, "BENEFIT")``;
    a cell of two names, ``expense_maint, inflation_rate``, maps both.
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
    whose text runs into the gap between two spans is what docutils rejects as a malformed
    table, dropping the whole table from the page.  Only the last column may run past its
    rule.  Each table runs from a rule line to the blank line that ends it.
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


# What only IP_UK_S's docstrings may say: a reference into its Spaces, which the SEC pages
# would link to the wrong model, and its clock, t counting policy months.
STALE = re.compile(r"~\.IP_UK_S\.|``t`` counts \*\*policy months\*\*")


def test_the_docstrings_describe_the_valuation_clock(sec_model, s_model):
    """The docstrings say what this model is, and none says what only IP_UK_S is.

    Whitespace is collapsed first, as ``test_model_conventions_uk`` collapses it, so that a
    phrase split across a line break still matches.  The model docstring names the valuation
    date, BasicTerm_SE, the policy clock, the SEC table, its companion and the product.  The
    symbol map in the Projection docstring maps every cell running in force adds, which are
    exactly the cells ``IP_UK_S`` lacks, and names nothing the model lacks: every name in it
    is a cell or a Reference.  No row of a simple table in any docstring puts text between
    two of its columns (:func:`_table_overruns`), which would drop the table from the
    rendered page.  And no docstring says what :data:`STALE` matches.
    """
    flat = {where: re.sub(r"\s+", " ", doc) for where, doc in _docs(sec_model)}
    for phrase in ("valuation date", "BasicTerm_SE", "duration_mth", TABLE, COHORTS,
                   "income protection"):
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
    assert not stale, f"docstrings that describe IP_UK_S: {stale}"


@pytest.mark.docutils
def test_the_docstrings_parse_as_rst(sec_model):
    """Every docstring of the model parses as reStructuredText, without a warning.

    The docs build reads each docstring through docutils, which reports a malformed table, a
    bad indentation or an unclosed inline markup and drops what it cannot read; a raw-text
    test sees none of it.  Each docstring, dedented as autodoc dedents it and its Sphinx
    roles read as plain interpreted text, which docutils alone does not know, is parsed
    here, and any warning or error is a fault.  docutils comes with the docs build, not with
    the models' requirements, so the test is skipped where it is absent; the column check in
    the test above runs everywhere.
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
    ``model_point_file`` changed, to ``model_point_table_sec.csv``, and the claim cohorts'
    added: an edit to a table reaches both models, and the two can never drift apart.  And
    every Reference of S's is the SEC model's at S's value, but the four it adds, the
    contract's issue and expiry ages, so that no assumption moves between the two, and the
    C step's ``idx`` and codes (:data:`CODE_NAMES`); ``Data`` adds the future horizon and
    the inception table's interpolated ages.
    """
    assert sec_model.Data.input_dir() == s_model.Data.input_dir()
    files = {r: v for r, v in s_model.Data.refs.items() if r.endswith("_file")}
    assert {r: v for r, v in sec_model.Data.refs.items() if r.endswith("_file")} == {
        **files, "model_point_file": TABLE, "inforce_cohorts_file": COHORTS}
    assert sec_model.Data.future_horizon_mth == 120
    assert (sec_model.Data.rate_age_min, sec_model.Data.rate_age_max) == (18, 69)
    plain = (bool, int, float, str)
    s_refs = {r: v for r, v in s_model.Projection.refs.items()
              if isinstance(v, plain) and r != "point_id"}
    sec_refs = {r: v for r, v in sec_model.Projection.refs.items()
                if isinstance(v, plain) and r != "idx" and r not in CODE_NAMES}
    assert sec_refs == {**s_refs, "issue_age_min": 18, "issue_age_max": 59,
                        "expiry_age_min": 50, "expiry_age_max": 70}


# The inception table's pivot ages, which every schedule shares.
PIVOTS = (30, 35, 40, 45, 50, 55, 60, 64)


def test_the_core_grid_reaches_every_branch(spliced, splice_records):
    """What the default run's T2 and T3 cases reach, which the full grid only multiplies.

    The default run thins the splice to a core (the module docstring), and this test is what
    keeps the thinning from costing a branch.  First, statically, over S's table with the
    variants, each property below holds of some core case: each escalation, status and
    recovery basis, each sex, each variant and each set of References; and each kind of
    valuation month: the second month, on an anniversary, the month before and after one,
    about the lapse table's last year, at an inception pivot, on a claim's anniversary,
    and the last month of a frame.  And of some core future case: issued off the valuation
    anniversaries and on them, more than a year on, each escalation, a variant and a set
    other than the main one.

    Then, on the splice's models, of some core row, each of :data:`AT_VALUATION` and
    :data:`IN_FRAME`, what no column of the table shows: every opening-state column in use,
    the month-0 events, and every branch and both sides of every ``min`` and ``max`` the
    full grid reaches.

    Each core row's branches were recorded by the T2 or T3 case that compared it
    (:func:`_settle`), and a row no case has recorded is evaluated here.  With
    ``UKLIB_SEC_FULL=1`` it asks the same of the full grid's rows, which must reach nothing
    the core does not.
    """
    assert set(CORE_SPLICES) <= set(SPLICES + IN_FORCE_TWINS)
    assert set(CORE_FUTURES) <= set(FUTURES)
    s_table = _s_table_with_variants()

    def at(p, column):
        return s_table.at[p, column]

    splices = {
        **{f"{e} escalation": (lambda r, k, p, d, e=e: at(p, "escalation") == e)
           for e in ("RPI", "none")},
        **{f"the {s} status": (lambda r, k, p, d, s=s: at(p, "status") == s)
           for s in ("active", "in_claim")},
        **{f"the {b} basis": (lambda r, k, p, d, b=b: at(p, "recovery_basis") == b)
           for b in ("return_to_h", "exit")},
        **{f"sex {x}": (lambda r, k, p, d, x=x: at(p, "sex") == x) for x in ("M", "F")},
        **{f"variant {v}": (lambda r, k, p, d, v=v: p == v) for v in VARIANTS},
        **{f"the {s} set": (lambda r, k, p, d, s=s: r == s) for s in SPLICE_SETS},
        "a twin in claim": lambda r, k, p, d: k == "twin",
        "in the second month": lambda r, k, p, d: d == 1,
        "on an anniversary": lambda r, k, p, d: d > 0 and d % 12 == 0,
        "in the month before an anniversary": lambda r, k, p, d: d % 12 == 11,
        "in the month after an anniversary": lambda r, k, p, d: d % 12 == 1 and d > 12,
        "about the lapse table's last year": lambda r, k, p, d: (
            at(p, "status") == "active" and 59 <= d <= 61),
        "at an inception pivot": lambda r, k, p, d: (
            at(p, "status") == "active" and d % 12 == 0
            and at(p, "entry_age") + d // 12 in PIVOTS),
        "on a claim's anniversary": lambda r, k, p, d: (
            at(p, "status") == "in_claim" and d > 0
            and (at(p, "claim_duration_months") + d) % 12 == 0),
        "the last month of a frame": lambda r, k, p, d: d == COVER[p] - 1,
    }
    futures = {
        "issued off the anniversaries": lambda r, p, k: k % 12 != 0,
        "issued on them": lambda r, p, k: k % 12 == 0,
        "issued more than a year on": lambda r, p, k: k > 12,
        **{f"{e} escalation": (lambda r, p, k, e=e: at(p, "escalation") == e)
           for e in ("RPI", "none")},
        "a variant": lambda r, p, k: p in VARIANTS,
        "a set other than the main one": lambda r, p, k: r != "main",
    }
    missing = [what for what, holds in splices.items()
               if not any(holds(r, k, p, d) for r, k, p, d in CORE_SPLICES)]
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
# The C step's representation (UKLIB-SEC-PLAN.md §6.3, *C*)
#
# Data decodes each model point's text into the number the projection reads, and turns
# each table into an array indexed by integers (USLIB-SEC-PLAN.md R5-R8); a timing and a
# kind are int codes, and the claims total is a code of its own (R9, R12); and the claim
# cohorts, IP_UK_S's tuple a month, are a recursion of two parameters, pols_sick_dur(t, z),
# whose sums are IP_UK_S's sum written out (§6.3, *C -- the restructure*), and whose chain
# the depth test above holds to one cell a month.  These tests hold the representation in
# modelx, with no compiler, in seconds: the compiled section after the fingerprint holds
# the compiled model to modelx on it.


# Whether sum() compensates, Neumaier's way, as it does for floats from Python 3.12 on most
# builds, read from sum() itself as test_model_conventions_uk.py's SUM_COMPENSATES reads it.
# The cohort sums are IP_UK_S's sum() written out, so they are its bits only where it
# compensates.  Python 3.11's sum() adds left to right, and there IP_UK_S's sums, and the
# counts, cohorts and benefit claims that read them, part from these in their last bits
# (UKLIB-SEC-PLAN.md §6.3, *Record -- M8*, *Python 3.11's sum*): the tests of the sums' bits
# and of the claims total hold the rest and skip those bits there, with this reason.
SUM_COMPENSATES = sum([0.1] * 10) == 1.0
SUM_311 = ("Python 3.11's sum() adds floats left to right, without the compensation it has "
           "from 3.12, so the sums written out here are not its bits; the rest was held")


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


def test_the_all_total_is_s_total_bit_for_bit(sec_model, s_model):
    """``claims(t, ALL)`` is ``IP_UK_S``'s ``claims(t)``, its ``sum``, to the last bit.

    S totals its three kinds with Python's ``sum``, which compensates, and the total here
    is written left to right from ``0.0`` (``Projection.claims``), which is ``sum``'s
    float wherever at most two kinds are non-zero in a month (USLIB-SEC-PLAN.md R12; §6.2,
    *Record -- M4*: three or more take the compensated sum written out).  So the kinds
    non-zero together are counted, in every month of every committed point's frame and the
    month after it: never two, the death and the lapse kinds being 0.0 in every month by
    the product's design, and one, the benefit, in some months, which is asserted, so that
    the count is no vacuous one.  The total is compared by ``float.hex`` with ``sum`` of
    the row's own three kinds there; and on every twin of S's new business, whose kinds
    are S's to the last bit, with S's ``claims(t)`` itself.  T1 compares the totals to
    1e-9; this compares their bits.

    The twins' kinds are S's bits only where ``sum`` compensates, from Python 3.12: S's
    benefit claim reads its cohort sums, which on Python 3.11 (:data:`SUM_COMPENSATES`) add
    left to right and part from this model's in their last bits.  There the kinds counted
    and the total against its row's own kinds are held, which one kind non-zero leaves
    ``sum``'s on any Python, and the twins' bits skip, naming Python 3.11
    (:data:`SUM_311`).
    """
    total = _code(sec_model.Projection, "ALL")
    kinds = [_code(sec_model.Projection, kind) for kind in KINDS]
    found, bits, counts = [], [], {0: 0, 1: 0, 2: 0, 3: 0}
    table = sec_model.Data.model_point_table()
    for key, point_id in zip(point_keys(sec_model), table.index):
        p = projection(sec_model, key)
        for t in range(p.proj_len() + 1):
            values = [p.claims(t, kind) for kind in kinds]
            counts[sum(v != 0.0 for v in values)] += 1
            if values[1:] != [0.0, 0.0]:
                found.append(f"point {point_id}, t = {t}: the death and lapse kinds are "
                             f"{values[1:]!r}")
            if p.claims(t, total).hex() != sum(values).hex():
                found.append(f"point {point_id}, t = {t}: {p.claims(t, total)!r}, the "
                             f"kinds' sum {sum(values)!r}")
    assert counts[2] == counts[3] == 0 and counts[1] > 0 and counts[0] > 0, counts
    assert not found, found[:10]
    _hold_the_sums_bits()
    for point_id in NEW_BUSINESS:
        s, p = _point(s_model, point_id), _point(sec_model, point_id)
        for t in range(p.proj_len()):
            if p.claims(t, total).hex() != s.claims(t).hex():
                bits.append(f"point {point_id}, t = {t}: {p.claims(t, total)!r}, S "
                            f"{s.claims(t)!r}")
    assert not bits, bits[:10]


# The cells that sum the cohorts, each with S's term for cohort z holding a lives, and
# whether S's generator leaves out a cohort that holds none: the lives in claim, S's
# sum(sick_cohorts(t)), over every cohort; and the month's three flows out of claim, each
# over the cohorts that hold lives.
COHORT_SUMS = {
    "pols_sick": (lambda p, z, a: a, False),
    "pols_sick_surv": (lambda p, z, a: a * p.claim_surv_step(z), True),
    "pols_recovery": (lambda p, z, a: a * p.rec_rate_mth(z), True),
    "pols_death_sick": (lambda p, z, a: a * (1.0 - p.rec_rate_mth(z))
                        * p.mort_rate_sick_mth(z), True),
}


def _plain(values):
    """``values`` added left to right from 0.0, uncompensated."""
    total = 0.0
    for v in values:
        total = total + v
    return total


@pytest.mark.parametrize("grid", GRIDS)
def test_the_cohort_sums_are_s_sums_bit_for_bit(sec_model, s_model, grid):
    """Each sum over the cohorts is ``IP_UK_S``'s ``sum``, to the last bit (§6.3, *C*).

    ``IP_UK_S`` sums a month's tuple of cohorts with Python's ``sum``, which compensates,
    Neumaier's way, and this model writes each sum out as a loop over ``pols_sick_dur(t,
    z)`` in ``z`` order, from 1 to ``claim_dur_live(t)`` (:data:`COHORT_SUMS`), and the
    present value as a loop over the frame's months.  Nothing else holds a loop to
    ``sum``'s float: T1 and the splice compare to 1e-9, and a plain sum parts from it by
    an ulp in some months; one out of ``z`` order the test below holds.  So on every
    committed point, in every month of its frame and the month after it: the two cohorts
    past ``claim_dur_live(t)``, where ``max_dur()`` has them, are 0.0 exactly, and at the
    frame's first two months and its last every cohort past it is, so that the sums may
    stop there, the cohorts past them being each the zero of the one below on the
    diagonal; on the books, the cohort at ``claim_dur_live(t)`` holds lives, so that the
    sums stop at the oldest cohort that can, not past it (M8's review); each sum is, by
    ``float.hex``, ``sum`` of S's term over the cohorts to
    ``claim_dur_live(t)``, each cohort that holds no lives left out where S's generator
    leaves it out; and ``pv_benefits()`` is ``sum`` over the frame of the month's benefit
    times its discount factor.  The months where a plain left-to-right sum parts from
    ``sum`` are counted, and must be some, so that the comparison is no vacuous one.  And
    on every twin of S's new business, issued at the valuation date, each cohort is the
    element of S's ``sick_cohorts(t)``, every element past ``claim_dur_live(t)`` 0.0, and
    each sum and the present value S's own, by ``float.hex``.  Where no cohort holds lives
    ``sum`` of no terms is the int 0, which each cell holds as 0.0, a C double, the one
    difference, of type alone, from ``IP_UK_S``.  The core's points by default
    (:data:`CORE_POINTS`), with the twins, and the rest on the full grid.

    The bits are ``sum``'s where it compensates, from Python 3.12.  Where it does not, on
    Python 3.11 (:data:`SUM_COMPENSATES`), ``sum`` and ``IP_UK_S`` with it add left to
    right, and the sums here part from theirs in the last bits, and so, through the
    recoveries back in health, do the twins' cohorts: there the cohorts past the live ones,
    this model's and on the twins S's, the live one's lives and each sum's type are held,
    and the bits skip, naming Python 3.11 (:data:`SUM_311`).
    """
    found, bits, plain = [], [], 0
    table = sec_model.Data.model_point_table()
    for key, point_id in zip(point_keys(sec_model), table.index):
        if not _on_grid(grid, point_id):
            continue
        p = projection(sec_model, key)
        top, entry = p.max_dur(), p.t_entry()
        for t in range(p.proj_len() + 1):
            live = p.claim_dur_live(t)
            past = (range(live + 1, top + 1) if t in (entry, entry + 1, p.proj_len() - 1)
                    else range(live + 1, min(live + 2, top) + 1))
            held = [p.pols_sick_dur(t, z) for z in past]
            if any(v != 0.0 for v in held):
                found.append(f"point {point_id}, t = {t}: a cohort past claim_dur_live "
                             f"{live} holds {[v for v in held if v != 0.0][:3]}")
            if (entry <= t < p.proj_len() and live > 0
                    and not p.pols_sick_dur(t, live) > 0.0):
                found.append(f"point {point_id}, t = {t}: the cohort at claim_dur_live "
                             f"{live} holds no lives")
            cohorts = [(z, p.pols_sick_dur(t, z)) for z in range(1, live + 1)]
            for cell, (term, filtered) in COHORT_SUMS.items():
                terms = [term(p, z, a) for z, a in cohorts if a != 0.0 or not filtered]
                want, got = float(sum(terms)), p.cells[cell](t)
                if type(got) is not float:
                    found.append(f"point {point_id}: {cell}({t}) is {got!r}, not a float")
                elif got.hex() != want.hex():
                    bits.append(f"point {point_id}: {cell}({t}) is {got!r}, sum {want!r}")
                plain += _plain(terms) != want
        terms = [p.claims(t, _code(p, "BENEFIT")) * p.disc_factor(t)
                 for t in range(p.proj_len())]
        if p.pv_benefits().hex() != float(sum(terms)).hex():
            bits.append(f"point {point_id}: pv_benefits() is {p.pv_benefits()!r}, sum "
                        f"{sum(terms)!r}")
    for point_id in NEW_BUSINESS if grid == "core" else ():
        s, p = _point(s_model, point_id), _point(sec_model, point_id)
        for t in range(p.proj_len()):
            past = s.sick_cohorts(t)[p.claim_dur_live(t):]
            if any(v != 0.0 for v in past):
                found.append(f"point {point_id}, t = {t}: S's sick_cohorts({t}) holds "
                             f"{[v for v in past if v != 0.0][:3]} past claim_dur_live")
    assert not found, found[:10]
    _hold_the_sums_bits()
    for point_id in NEW_BUSINESS if grid == "core" else ():
        s, p = _point(s_model, point_id), _point(sec_model, point_id)
        for t in range(p.proj_len()):
            live, held = p.claim_dur_live(t), s.sick_cohorts(t)
            mine = tuple(p.pols_sick_dur(t, z) for z in range(1, live + 1))
            if [v.hex() for v in mine] != [v.hex() for v in held[:live]]:
                bits.append(f"point {point_id}, t = {t}: the cohorts part from S's "
                            f"sick_cohorts({t})")
            for cell in COHORT_SUMS:
                if p.cells[cell](t).hex() != float(s.cells[cell](t)).hex():
                    bits.append(f"point {point_id}: {cell}({t}) is {p.cells[cell](t)!r}, "
                                f"S {s.cells[cell](t)!r}")
        if p.pv_benefits().hex() != float(s.pv_benefits()).hex():
            bits.append(f"point {point_id}: pv_benefits() is {p.pv_benefits()!r}, S "
                        f"{s.pv_benefits()!r}")
    assert plain > 0, "no month where a plain sum parts from sum: the test sees no order"
    assert not bits, bits[:10]


def _mortality_in_claim(rate):
    """An edit of the termination table that sets the in-claim mortality of claim
    duration years 2 and 3, claim durations 13 to 36, to ``rate``."""
    def edit(table):
        table = table.copy()
        table.loc[table["claim_duration_year"].isin([2, 3]), "mort_rate_sick"] = rate
        return table
    return edit


# Each cohort sum taken past the floats on the claim at 24, its count the largest float, all
# in claim at claim durations 24 and 25 at shares summing to 1 + 9e-11, which Data reads
# (LIVES_PAST), as (the References, the termination table's edit): the lives in claim at the
# shipped rates; the recoveries under an overlay of 0.1, every recovery rate capped at 1;
# the deaths in claim and the survivors, under an overlay of the largest float, which takes
# every recovery rate to 0, with the in-claim mortality of those claim durations set to 1
# and to 0.  The termination table's rates are each held to 0 to 1 by Data, and the overlay
# to a finite number above 0 by proj_len(), so each input is one the model accepts.
SUMS_PAST = {
    "pols_sick": ({}, None),
    "pols_recovery": ({"cycle_factor": 0.1}, None),
    "pols_death_sick": ({"cycle_factor": BIG}, _mortality_in_claim(1.0)),
    "pols_sick_surv": ({"cycle_factor": BIG}, _mortality_in_claim(0.0)),
}


@pytest.mark.parametrize("cell", list(SUMS_PAST))
def test_a_cohort_sum_past_the_floats_is_sum_s_infinity(tmp_path, cell):
    """A cohort sum that leaves the floats is ``sum``'s infinity, not NaN.

    ``sum`` adds back its carried error only where it is finite, and so does each loop here
    (:func:`pols_sick`'s docstring): once the running sum leaves the floats, the error
    carried is an infinity of the other sign, and added back it would make the sum NaN,
    which every refusal downstream would print where ``IP_UK_S`` prints ``inf``.  No
    committed point reaches it, so the bit test above cannot see the test dropped; here
    each sum is taken past the floats on an input the model accepts (:data:`SUMS_PAST`)
    and must be, by ``float.hex``, ``sum`` of :mod:`~.IP_UK_S`'s terms over the cohorts
    (:data:`COHORT_SUMS`), the infinity, in the month the claim is valued at (M8's
    review).
    """
    refs, term = SUMS_PAST[cell]
    model = _read_edited(tmp_path, _set("policy_count", [11], BIG), LIVES_PAST,
                         edits={TERM: term} if term else None)
    try:
        for ref, value in refs.items():
            setattr(model.Projection, ref, value)
        p = _point(model, 11)
        term_of, filtered = COHORT_SUMS[cell]
        cohorts = [(z, p.pols_sick_dur(0, z)) for z in range(1, p.claim_dur_live(0) + 1)]
        want = float(sum(term_of(p, z, a) for z, a in cohorts if a != 0.0 or not filtered))
        got = p.cells[cell](0)
        assert want == math.inf and got.hex() == want.hex(), (cell, got, want)
    finally:
        model.close()


def _direct_reads(proj, cell, args, read):
    """The arguments of each call of ``read`` that ``cell(*args)`` makes itself, in the
    order it makes them, by modelx's stack trace.  On a model just read every read is cold,
    and the trace records it; a read of a value already cached it does not."""
    mx.start_stacktrace(maxlen=None)
    try:
        proj.cells[cell](*args)
        trace = mx.get_stacktrace(summarize=False)
    finally:
        mx.stop_stacktrace()
    level, found = 0, []
    for event, _, _, text, called in trace:
        if event == "ENTER":
            level += 1
            if level == 2 and f".{read}(" in text:
                found.append(tuple(called))
        else:
            level -= 1
    return found


# modelx warns as its stack trace starts and stops, which is all the test does with it.
@pytest.mark.filterwarnings("ignore:call stack trace:UserWarning")
def test_each_sum_reads_its_terms_in_ip_uk_s_order():
    """Each compensated sum reads its terms in ``IP_UK_S``'s order: ``z``, and ``t``,
    ascending.

    A compensated sum of terms all 0 or more is the correctly rounded sum in almost any
    order, so the bit test above cannot see a loop run out of order: on the committed
    points it passes one summed in reverse.  But ``sum``'s float is its order's, and a sum
    whose exact value lies near a rounding tie parts in another.  So the order itself is
    held: on a model just read, each cohort sum of :data:`COHORT_SUMS` on the anchor cell
    in force in its last month, point 10, whose 359 opening cohorts are each read cold, is
    called under modelx's stack trace, and the cohorts it reads itself must be claim
    durations 1 to ``claim_dur_live(0)``, in order; and the present value's reads of the
    benefit outgo, on the twin of the older male cell, its months 0 to ``proj_len() - 1``,
    in order.
    """
    for cell in (*COHORT_SUMS, "pv_benefits"):
        model = mx.read_model(model_path(SEC), name=_name("order"))
        try:
            if cell == "pv_benefits":
                p = _point(model, 6)
                want = [(t, _code(p, "BENEFIT")) for t in range(p.proj_len())]
                got = _direct_reads(p, cell, (), "claims")
            else:
                p = _point(model, 10)
                want = [(0, z) for z in range(1, p.claim_dur_live(0) + 1)]
                got = _direct_reads(p, cell, (0,), "pols_sick_dur")
            assert got == want and len(want) > 100, (cell, got[:5], len(got), len(want))
        finally:
            model.close()


# Every schedule of the inception table, as Data.inception_schedule numbers them: by sex,
# then occupation class, then deferred period.
SCHEDULES = tuple((sex, occ, weeks) for sex in ("M", "F") for occ in (1, 2, 3, 4)
                  for weeks in (4, 8, 13, 26, 52))


def _schedule_rows(table, base, prefix):
    """A row of ``table``'s ``base`` for each of :data:`SCHEDULES`, issued at 18 to expire
    at 70, labelled 1 to 40 in their order, each with a ``policy_id`` of its own."""
    rows = []
    for i, (sex, occ, weeks) in enumerate(SCHEDULES, start=1):
        row = table.loc[[base]].assign(sex=sex, occ_class=occ, deferred_weeks=weeks,
                                       entry_age=YOUNGEST, expiry_age=OLDEST_EXPIRY,
                                       policy_id=f"{prefix}{i:05d}")
        row.index = pd.Index([i], name="point_id")
        rows.append(row)
    return pd.concat(rows)


@pytest.mark.parametrize("edits", [pytest.param(None, id="shipped"),
                                   pytest.param(FLOOR_INCEPTION, id="floored")])
def test_every_schedule_and_age_is_ip_uk_s_own_rate(tmp_path, edits):
    """``Data``'s inception and mortality arrays hold ``IP_UK_S``'s rates, element by
    element, on every schedule at every age the contract admits (§6.3, *C*).

    ``Data.inception_array`` makes ``IP_UK_S``'s interpolation, extrapolation and floor at
    0 once, by S's own formula, at every attained age from 18 to 69, on each of the forty
    schedules, sex by occupation class by deferred period, and ``Data.inception_schedule``
    numbers each point's.  T1 and the splice see the rates of the schedules and ages the
    grid's points reach; this sees every one.  A point of each schedule, issued at 18 to
    expire at 70, goes into a copy of S's table and into one of SEC's, the anchor cell's
    row changed; on each, at every age from 18 to 69, SEC's ``inception_rate`` and
    ``mort_rate`` are S's, in value and type, the array's element at the point's schedule
    and the age is S's rate, the cycle overlay being 1, and the point's schedule and
    mortality row are S's keys decoded.  On the shipped table, and on the floor's
    (:data:`FLOOR_INCEPTION`), whose schedule of men in class 4 on 4 weeks falls below 0
    under age 29.7, so that the floor is held element by element, at 0.0 from 18 to 29.
    An array off by one age, a schedule numbered otherwise than the decode numbers it, or
    the floor dropped, parts here.
    """
    s = mx.read_model(temp_inputs(tmp_path / "s", model_path(TWIN),
                                  model_points=_schedule_rows(_s_table(), 1, "IP-8"),
                                  edits=edits), name=_name("schedules_s"))
    sec = None
    found = []
    try:
        sec = mx.read_model(_sec_inputs(tmp_path / "sec",
                                        _schedule_rows(_committed(), 1, "IP-8"),
                                        _committed_cohorts().iloc[0:0], edits=edits),
                            name=_name("schedules"))
        array, mort = sec.Data.inception_array(), sec.Data.mort_table_array()
        assert array.shape == (40, OLDEST_EXPIRY) and list(
            sec.Data.inception_schedule()) == list(range(40))
        floored = 0
        for i, (sex, occ, weeks) in enumerate(SCHEDULES, start=1):
            sp, p = _point(s, i), _point(sec, i)
            want = 20 * ("M", "F").index(sp.sex()) + 5 * (sp.occ_class() - 1) + (
                4, 8, 13, 26, 52).index(sp.deferred_weeks())
            if (p.inception_schedule(), p.mort_schedule()) != (want, ("M", "F").index(
                    sp.sex())):
                found.append(f"schedule {i}: decoded {p.inception_schedule()}, "
                             f"{p.mort_schedule()}, S's keys {want}")
            for x in range(YOUNGEST, OLDEST_EXPIRY):
                t = 12 * (x - YOUNGEST)
                for cell in ("inception_rate", "mort_rate"):
                    theirs, mine = sp.cells[cell](t), p.cells[cell](t)
                    if mine != theirs or type(mine) is not type(theirs):
                        found.append(f"{sex}, class {occ}, {weeks} weeks, age {x}: {cell} "
                                     f"{mine!r}, S {theirs!r}")
                rate = sp.inception_rate(t)
                floored += rate == 0.0
                if array[want, x] != rate or mort[p.mort_schedule(), x] != sp.mort_rate(t):
                    found.append(f"{sex}, class {occ}, {weeks} weeks, age {x}: the arrays "
                                 f"hold {array[want, x]!r} and "
                                 f"{mort[p.mort_schedule(), x]!r}, S {rate!r} and "
                                 f"{sp.mort_rate(t)!r}")
        assert floored == (0 if edits is None else 12), floored
    finally:
        if sec is not None:
            sec.close()
        s.close()
    assert not found, found[:20]


# The labels and decodes each twin of an S point is compared on, against S's reading of
# the same text: the five labels as S returns them, and each decode as S's comparison of
# the text gives it.
DECODES = {"is_escalating": lambda s: s.escalation() == "RPI",
           "recovery_code": lambda s: ("return_to_h", "exit").index(s.recovery_basis()),
           "mort_schedule": lambda s: ("M", "F").index(s.sex()),
           "inception_schedule": lambda s: (20 * ("M", "F").index(s.sex())
                                            + 5 * (s.occ_class() - 1)
                                            + (4, 8, 13, 26, 52).index(s.deferred_weeks()))}


def test_every_decode_is_ip_uk_s_own_reading_of_the_text(sec_model, s_model):
    """``Data`` decodes every value of each text column as ``IP_UK_S``'s cells read it.

    On the twin of each of S's seven points, which between them hold each sex, each
    escalation, each recovery basis and each status, the five labels are S's text, and
    each decode of :data:`DECODES`, the escalation flag, the recovery basis's code and the
    two schedules, is S's comparison of the text, in value and in type, and the
    ``escalation`` and ``recovery_basis`` columns are decoded by their text alone, element
    by element (``Data.escalation_rpi`` and ``Data.recovery_code``).  Every schedule at
    every age is the test above's.
    """
    found = []
    for point_id in S_POINTS:
        s, p = _point(s_model, point_id), _point(sec_model, point_id)
        for label in LABEL_REFUSALS:
            if p.cells[label]() != s.cells[label]():
                found.append(f"point {point_id}: {label}() is {p.cells[label]()!r}, S "
                             f"{s.cells[label]()!r}")
        for cell, read in DECODES.items():
            want, got = read(s), p.cells[cell]()
            if got != want or type(got) is not type(want):
                found.append(f"point {point_id}: {cell}() is {got!r}, S's text gives "
                             f"{want!r}")
    values = {column: set(_committed()[column]) for column in ("sex", "escalation",
                                                                "recovery_basis", "status")}
    assert values == {"sex": {"M", "F"}, "escalation": {"RPI", "none"},
                      "recovery_basis": {"return_to_h", "exit"},
                      "status": {"active", "in_claim"}}, values
    data = sec_model.Data
    table = data.model_point_table()
    assert list(data.escalation_rpi()) == [int(e == "RPI") for e in table["escalation"]]
    assert list(data.recovery_code()) == [("return_to_h", "exit").index(b)
                                          for b in table["recovery_basis"]]
    assert not found, found


# The values a test writes into the escalation column of the anchor cell's twin, which
# elects RPI escalation and so reads the flag in every month: what an extract might carry
# where it means RPI, each a text Data.model_point_table refuses, since the check and the
# decode read the column by its text alone, exactly RPI or none.
FLAG_WRITINGS = (" True", "True ", 1, 1.0, True, " RPI", "RPI ", "rpi")


@pytest.mark.parametrize("value", FLAG_WRITINGS, ids=[repr(v) for v in FLAG_WRITINGS])
def test_the_escalation_flag_is_read_by_its_text_alone(tmp_path, value):
    """The escalation column is checked and decoded by one rule: its text, RPI or none.

    ``escalation`` is the flag the escalation reads (§6.3, *C*), decoded once for every
    point, ``Data.escalation_rpi``, 1 where the text is RPI and 0 where it is none, and
    read by ``is_escalating()``; ``Data.model_point_table`` refuses any other text, naming
    the point, before the decode reads it.  So no value is read as RPI by one and refused
    by the other, nor read one way in modelx and another compiled: each value of
    :data:`FLAG_WRITINGS` written on the anchor cell's twin, point 1, which escalates, is
    refused as the table is read, with the one message, on the committed table and on the
    extract, labelled otherwise (:data:`EXTRACT_LABELS`), by its label; and the compiled
    refusal test refuses them as modelx does.  The committed values decode as S reads them
    (:func:`test_every_decode_is_ip_uk_s_own_reading_of_the_text`).
    """
    for name, table, label in (("committed", _committed(), 1),
                               ("extract", _extract(), _relabel_map()[1])):
        model = mx.read_model(_sec_inputs(tmp_path / name,
                                          _set("escalation", [label], value)(table),
                                          _extract_cohorts() if name == "extract"
                                          else None),
                              name=_name("flag"))
        try:
            _refused(model.Data.model_point_table,
                     f"{TABLE}: escalation must be RPI or none; it is not at point_id "
                     f"[{label}]")
            _refused(model.Data.escalation_rpi, "escalation must be RPI or none")
        finally:
            model.close()


def test_every_padded_array_holds_nan_and_no_reader_reads_it(sec_model, tmp_path):
    """The padding is NaN, and each table's one reader reads inside its keys alone.

    ``Data`` tables the inception rates from age 0, forty schedules, the mortality rates
    from age 0, two sexes, the termination rates and the lapse rates from year 0, and the
    claim cohorts from claim duration 0, and pads what no file holds with NaN, as its
    docstring says, so that a read past a check, were one lost, would make every number
    after it NaN rather than another key's value: the ages below 18, the inception
    array's first, and below the mortality table's, 16 as shipped, year 0 of each
    duration-year and policy-year array, and claim duration 0 of every point's cohorts;
    inside, nothing is NaN.  And each reader refuses, naming the point by its label, what
    it would read in the padding: on the extract labelled otherwise
    (:data:`EXTRACT_LABELS`), the inception rate at an attained age below the array's
    first, under a ``Data.rate_age_min`` raised to 36, past the anchor cell's issue age,
    and the recovery and in-claim mortality rates at claim duration 0, which no cohort is
    aged at; the lapse rate reads no table outside cover, and the opening cohorts read
    claim durations 0 and past the companion's last as no lives, without a read.
    """
    data = sec_model.Data
    inception, mort = data.inception_array(), data.mort_table_array()
    assert inception.shape == (40, 70) and (data.rate_age_first(), data.rate_age_last()) == (
        18, 69)
    assert np.isnan(inception[:, :18]).all() and not np.isnan(inception[:, 18:]).any()
    first, last = data.mort_age_first(), data.mort_age_last()
    assert mort.shape == (2, last + 1) and (first, last) == (16, 75)
    assert np.isnan(mort[:, :first]).all() and not np.isnan(mort[:, first:]).any()
    years = data.termination_last_year()
    for array, width in ((data.recovery_rate_array(), years + 1),
                         (data.mort_rate_sick_array(), years + 1),
                         (data.lapse_rate_array(), data.lapse_last_year() + 1)):
        assert array.shape == (width,) and np.isnan(array[0])
        assert not np.isnan(array[1:]).any()
    assert (years, data.lapse_last_year()) == (5, 6)
    shares = data.cohort_share()
    assert shares.shape == (len(_committed()), data.cohort_z_last() + 1)
    assert np.isnan(shares[:, 0]).all() and not np.isnan(shares[:, 1:]).any()
    model = mx.read_model(_sec_inputs(tmp_path / "extract", _extract(), _extract_cohorts()),
                          name=_name("padded"))
    try:
        model.Data.rate_age_min = 36.0
        label = _relabel_map()[9]
        p = _point(model, label)
        position = list(_extract().index).index(label)
        assert p.point_id() == label != point_keys(model)[position] + 1
        assert p.age(0) == 40
        young = _point(model, _relabel_map()[1])
        _refused(lambda: young.inception_rate(0),
                 f"point_id {_relabel_map()[1]}: inception_table.csv is interpolated at "
                 f"attained ages 36 to 69, Data's rate_age_min to rate_age_max, not at 35")
        for cell in ("rec_rate", "mort_rate_sick"):
            _refused(lambda: p.cells[cell](0),
                     f"point_id {label}: termination_table.csv has no rate at claim "
                     f"duration year 0, claim duration 0")
        assert p.inception_rate(0) == model.Data.inception_array()[p.inception_schedule(),
                                                                   40]
        assert p.lapse_rate_base(p.proj_len()) == 0.0
        z_last = model.Data.cohort_z_last()
        assert p.pols_sick_dur_init(0) == p.pols_sick_dur_init(z_last + 1) == 0.0
    finally:
        model.close()


# Data's readers, each a DataFrame or a path, which only the label accessors, the reports
# and Data's own cells read.  Every other Data cell is a vector or an int in the Data
# docstring's table of its vectors.
READERS = ("input_dir", "model_point_table", "inforce_cohorts", "inception_table",
           "termination_table", "termination_table_rows", "mort_table", "mort_table_rows",
           "lapse_table", "lapse_table_rows")


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
    vector is of R5's kind, int64 for ages, months, codes, flags, schedules and claim
    durations, float64 for counts, shares, amounts and rates, as the table states it: a
    month held as a float64 reads the same numbers, and compiled reads a double through
    ``int()``, Python arithmetic, which neither C3 nor C5 sees.  Every cell is in the
    table, and every cell the table names is a cell.
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
    assert {"point_id", "inception_schedule", "mort_schedule", "is_escalating",
            "recovery_code", "age_at_entry", "expiry_age", "occ_class", "deferred_weeks",
            "duration_mth_init", "claim_dur_init", "max_dur", "proj_len",
            "pv_benefits", "annuity_dis"} <= set(names)
    found = []
    for key in point_keys(sec_model):
        proj = projection(sec_model, key)
        found += [f"{key}: {name} {type(value).__name__}" for name in names
                  if type(value := proj.cells[name]()) not in (int, float, bool)]
    assert not found, found


# Each label and the refusal its own formula makes of a value that is not its column's
# codes, which Data refuses first as it reads the table: as (the column, the refusal).
LABEL_REFUSALS = {"sex": ("sex", "invalid sex"),
                  "escalation": ("escalation", "invalid escalation"),
                  "premium_basis": ("premium_basis", "invalid premium_basis"),
                  "status": ("status", "invalid status"),
                  "recovery_basis": ("recovery_basis", "invalid recovery_basis")}


def test_each_label_refuses_a_value_that_is_not_its_codes():
    """The five labels return text or raise, in either engine.

    Each is a reporting cell, which a reader asks for and no projection cell reads, and the
    registry names them (``"reporting"``).  ``Data`` refuses a value other than the
    column's codes as it reads the table, so a label sees only text; but each refuses any
    other value itself, as ``IP_UK_S``'s ``escalation``, ``premium_basis``,
    ``recovery_basis`` and ``status`` do and the C step makes ``sex`` do, so that compiled
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


# The code families, each in its numbering: the timings, claims' kinds and their total,
# and the recovery bases, which index no cache.
CLAIM_CODES = (*KINDS, "ALL")


def test_the_spec_sizes_each_cache_as_its_comment_derives():
    """``spec_sec.py`` gives each cache the size its comment derives from the contract.

    The spec check, C3, holds the compiled caches to the spec, and C4 at the contract's
    extremes holds the spec to the largest argument a projection reads; neither sees a
    size above the comment's.  So this reads the spec as mx2cy does, and the bounds of the
    contract from the model's own References, and holds each size to the comment's
    derivation from them: ``t`` to ``12 * (expiry_age_max - issue_age_min) +
    future_horizon_mth + 2``, the timings' and kinds' 2-D caches to it by the one inner
    width, 4, the most codes a family has; ``z`` to ``12 * (expiry_age_max -
    issue_age_min) + 2``; and the cohorts' to ``z``'s width and ``t``'s months and one
    more, the outer size no other 2-D cache has, since Cython's unpickle code reads the
    caches of one outer size and element type back through one temporary, its C-array
    types comparing no inner size, which two widths break (``spec_sec.py``; the generated
    C is held by :func:`test_each_2d_cache_is_unpickled_through_a_temporary_of_its_shape`).
    And ``proj_len()``'s two bounds to the longest cover and the longest frame the sizes are
    for, 624 and 744 months, so that no input it accepts reads past a cache; ``Data``'s
    interpolated ages to the ages the contract admits, ``issue_age_min`` to
    ``expiry_age_max - 1``; and the codes dense from 0, ints, as the caches index them, each
    family in its own numbering, the recovery bases too.  A change to a bound or a size is
    derived again in the comment and here.
    """
    source, comment = _comment("spec_sec.py")
    for formula in ("12 * (expiry_age_max - issue_age_min) + future_horizon_mth + 2",
                    "12 * (expiry_age_max - issue_age_min) + 2"):
        assert formula in comment, formula
    sizes = ast.literal_eval(source)["spaces"]["Projection"]["cells_param_size"]
    proj, data = _references("Projection"), _references("Data")
    for names in (TIMINGS, CLAIM_CODES, RECOVERY_CODES):
        values = [proj[name] for name in names]
        assert values == list(range(len(names))), (names, values)
        assert all(type(v) is int for v in values), (names, values)
    span = int(proj["expiry_age_max"] - proj["issue_age_min"])
    t = 12 * span + int(data["future_horizon_mth"]) + 2
    width = max(len(TIMINGS), len(CLAIM_CODES))
    z = 12 * span + 2
    assert sizes == {"t": t, ("t", "timing"): (t, width), ("t", "kind"): (t, width),
                     "z": z, ("t", "z"): (t + 1, z)}, sizes
    assert (t, width, z) == (746, 4, 626)
    two_d = [size for size in sizes.values() if isinstance(size, tuple)]
    assert all(len({w for o, w in two_d if o == outer}) == 1 for outer, _ in two_d), two_d
    projection_source = (model_path(SEC) / "Projection" / "__init__.py").read_text(
        encoding="utf-8")
    (frame,) = [node for node in ast.parse(projection_source).body
                if isinstance(node, ast.FunctionDef) and node.name == "proj_len"]
    bounds = ast.get_source_segment(projection_source, frame)
    assert f"expiry_mth() > {12 * span}:" in bounds, "proj_len's cover bound"
    assert f"expiry_mth() - d > {12 * span + int(data['future_horizon_mth'])}:" in bounds
    assert (data["rate_age_min"], data["rate_age_max"]) == (
        proj["issue_age_min"], proj["expiry_age_max"] - 1)


def test_the_sample_raises_the_recursion_limit_its_comment_derives():
    """``sample_sec.py`` sets the recursion limit its comment derives, before the import.

    The export does not raise the recursion limit as modelx does (F7), so the sample sets
    it, and its comment records the measured need: the deepest cold call at the longest
    cover needs the limit the comment states in the export, and the reports and checks the
    sample runs in ascending ``t`` less, from a script's top level (measured at M8).  The
    limit is four times the first, rounded up to the thousand.  No build can tell a lower
    limit above the reports' need.  So this holds the limit, read from the sample's code,
    to the value derived from its comment's need, and holds the call before the import of
    the export.  A change to the need is measured again and written in the comment.
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
# which Data.point_id refuses when a refusal first names a point, here the level anchor
# cell's twin, point 3, the table's third row, issued at the valuation date and so holding
# no claim cohorts, written as issued at 17, below issue_age_min, a refusal of
# proj_len()'s, which meets the label's own first; and a timing and a kind no cell takes,
# each refused by the cell, as IP_UK_S's are, ValueError and its message: the timing 3,
# inside the one inner width, 4, of the timings' and the kinds' caches, and the timing
# and the kind 4, past it.
NOT_HELD = [
    ("a label with a fraction",
     lambda t: _set("entry_age", [3], 17)(t).rename(index={3: 3.5}),
     "result_cf", (), f"{TABLE}: point_id must be a whole number; [3.5] is not"),
    ("a label of 2**53",
     lambda t: _set("entry_age", [3], 17)(t).rename(index={3: 2 ** 53}),
     "result_cf", (), f"{TABLE}: point_id must be below 2**53 in size; [{2 ** 53}] is not"),
    ("the timing 3, inside the width", None, "pols_if_at", (0, 3), "invalid timing"),
    ("a timing past the width", None, "pols_if_at", (0, 4), "invalid timing"),
    ("a kind past the width", None, "claims", (0, 4), "invalid kind"),
]


@pytest.mark.parametrize("case, edit, cell, args, message", NOT_HELD,
                         ids=[c[0] for c in NOT_HELD])
def test_what_the_c_step_cannot_hold_or_take_is_refused(tmp_path, case, edit, cell, args,
                                                        message):
    """A label the vectors cannot hold, and a code no cell takes, are refused.

    ``Data.point_id`` reads each label by value, and refuses one that is not a whole
    number, or is ``2**53`` or more in size, naming every such label, when a refusal first
    names a point: here the level anchor cell's twin, the table's third row, which holds no
    claim cohorts, written as issued at 17, a refusal of ``proj_len()``'s, which meets the
    label's own first.  A projection that names no point reads no label, and runs.  And a
    timing or a kind no
    cell takes is refused by the cell, as ``IP_UK_S``'s are (:data:`NOT_HELD`), on point 1:
    the timing 3, inside the one inner width of 4, which the timings share with the kinds'
    cache, and the timing and the kind 4, past it.  Compiled, a code past the width
    raises ``IndexError`` instead, which the compiled refusal test holds.
    """
    model = _read_edited(tmp_path, edit or (lambda t: t))
    try:
        keys = point_keys(model)
        p = projection(model, keys[2] if edit is not None else keys[0])
        _refused(lambda: p.cells[cell](*args), message)
        if edit is not None:
            assert len(projection(model, keys[0]).result_cf()) == 360
    finally:
        model.close()


# ---------------------------------------------------------------------------
# C2 -- the Phase 1 fingerprint


def test_the_phase_1_fingerprint_is_reproduced(sec_model):
    """Every committed point computes what the model computed when its E step ended (C2).

    The C step changes how the model is represented and no number it computes
    (UKLIB-SEC-PLAN.md U2, after USLIB-SEC-PLAN.md D2), so before it changed anything the
    model as M7 committed it was frozen below (USLIB-SEC-PLAN.md §5.4): for each point,
    each column of ``result_cf()`` and ``result_pols()``, its sum, its largest absolute value
    and its values at five fixed months, the frame's first and last and the three quartiles
    between.  Every later version must reproduce it, to 1e-12 relative, floored at 1e-12 of
    the column's own magnitude (``uk_sec_support.fingerprint_mismatches``), with the same
    points, frames and columns exactly.  ``python tools/gen_sec_fingerprint.py IP_UK_SEC
    --check`` runs the same comparison from the command line.  Until the freeze, which is
    committed alone, the block is empty and the test skips.
    """
    if not FINGERPRINT:
        pytest.skip("the Phase 1 fingerprint is frozen in a commit of its own")
    assert fingerprint_mismatches(FINGERPRINT, sec_model) == []


# IP_UK_SEC's fingerprint, frozen from the model as M7 committed it and committed alone,
# before its C step changed anything.  Each point is keyed by its point_id; each column
# holds (its sum over the frame, its largest absolute value, (its values at the months)).
# The block is written by tools/gen_sec_fingerprint.py, and is never edited by hand: a
# refreeze goes through the tool's --force, in a commit of its own that says why.
# BEGIN generated fingerprint: IP_UK_SEC -- tools/gen_sec_fingerprint.py
FINGERPRINT = {
    1: {"rows": 360, "months": (0, 89, 179, 269, 359),
        "result_cf": {
            "pols_if": (173.22606301057516, 1.0, (
                1.0, 0.6164010477201897, 0.44452682592348036, 0.31489434015296836,
                0.21595065704956337)),
            "pols_active": (170.9680294293639, 1.0, (
                1.0, 0.6128221979302395, 0.43851676539784407, 0.30588638587430766,
                0.20367709922579866)),
            "pols_sick": (2.258033581211283, 0.012273557823764708, (
                0.0, 0.0035788497899501247, 0.006010060525636274, 0.0090079542786607,
                0.012273557823764708)),
            "premiums": (10381.997170348277, 35.0, (
                35.0, 29.18882183088657, 28.42381138530616, 28.195940302932325,
                25.549515470056136)),
            "claims_benefit": (7954.77531012982, 56.84900170617029, (
                0.0, 8.60692629430172, 17.839760835492893, 33.89391535038977,
                56.84900170617029)),
            "claims_death": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (1340.0414042858185, 5.0, (
                5.0, 3.900516041681371, 3.5892024414924357, 3.4483548904954424,
                3.2675954221027)),
            "net_cf": (1087.1804559326372, 34.56708165821686, (
                30.0, 16.68137949490348, 6.994848108320831, -9.146329937952887,
                -34.56708165821686)),
        },
        "result_pols": {
            "pols_if": (173.22606301057516, 1.0, (
                1.0, 0.6164010477201897, 0.44452682592348036, 0.31489434015296836,
                0.21595065704956337)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_active": (170.9680294293639, 1.0, (
                1.0, 0.6128221979302395, 0.43851676539784407, 0.30588638587430766,
                0.20367709922579866)),
            "pols_sick": (2.258033581211283, 0.012273557823764708, (
                0.0, 0.0035788497899501247, 0.006010060525636274, 0.0090079542786607,
                0.012273557823764708)),
            "pols_death_active": (0.053980455789236534, 0.00024228464227594627, (
                9.588388262971037e-05, 0.00010643034009796734, 0.00013799167469268113,
                0.0001900139547206286, 0.0002297075958327801)),
            "pols_lapse": (0.7253917576716465, 0.008740772775097947, (
                0.008740772775097947, 0.002080815342551728, 0.001488757636840065,
                0.0010381611417550054, 0.0006909181651563791)),
            "pols_inception": (0.05572428741855007, 0.00025111629229539347, (
                0.00010744006026721274, 0.00010798380603389967, 0.00013566737351341273,
                0.00020129656049174024, 0.0002380807930529868)),
            "pols_recovery": (0.0377959627912942, 0.00018106924010360815, (
                0.0, 7.08474792276741e-05, 9.798134756601884e-05, 0.00014098595945538875,
                0.00018106924010360815)),
            "pols_death_sick": (0.005628410296963661, 3.0655046421846046e-05, (
                0.0, 8.892956395132848e-06, 1.4987408125259746e-05, 2.247819574653525e-05,
                3.0655046421846046e-05)),
            "pols_exit": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.21499937624215237, 0.21499937624215237, (
                0.0, 0.0, 0.0, 0.0, 0.21499937624215237)),
            "benefit_pp": (1141809.9769517286, 4713.131012018762, (
                2000.0, 2459.7477308497405, 3025.1794497102237, 3832.2068177215647,
                4713.131012018762)),
            "premium_pp": (25622.969255677413, 125.44127723329201, (
                35.0, 47.630164066297866, 64.81807225664149, 92.17782027905737,
                125.44127723329201)),
        },
    },
    2: {"rows": 360, "months": (0, 89, 179, 269, 359),
        "result_cf": {
            "pols_if": (63.66535365852508, 1.0, (
                1.0, 0.23049064123760885, 0.12484419196810688, 0.06762128034561764,
                0.03662675438476751)),
            "pols_active": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_sick": (63.66535365852508, 1.0, (
                1.0, 0.23049064123760885, 0.12484419196810688, 0.06762128034561764,
                0.03662675438476751)),
            "premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_benefit": (125403.46346712217, 1911.7902587184922, (
                1911.7902587184922, 457.85142488783964, 247.99311102025771,
                134.32432394105084, 72.75615007203362)),
            "claims_death": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (2486.2868063250244, 30.0, (
                30.0, 8.50423247649465, 5.665141259363926, 3.8870809734530574,
                2.5894003794066283)),
            "net_cf": (-127889.75027344721, 1941.7902587184922, (
                -1941.7902587184922, -466.3556573643343, -253.65825227962165,
                -138.2114049145039, -75.34555045144025)),
        },
        "result_pols": {
            "pols_if": (63.66535365852508, 1.0, (
                1.0, 0.23049064123760885, 0.12484419196810688, 0.06762128034561764,
                0.03662675438476751)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_active": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_sick": (63.66535365852508, 1.0, (
                1.0, 0.23049064123760885, 0.12484419196810688, 0.06762128034561764,
                0.03662675438476751)),
            "pols_death_active": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_inception": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_recovery": (0.8042660118610426, 0.04167547137285199, (
                0.04167547137285199, 0.000983116060122767, 0.0005325002762709522,
                0.0002884263168208555, 0.00015622478323845052)),
            "pols_death_sick": (0.15935591310294223, 0.002429399267901949, (
                0.002429399267901949, 0.0005818127335662748, 0.00031513618170708236,
                0.00017069205827136932, 9.245456551224613e-05)),
            "pols_exit": (0.8042660118610426, 0.04167547137285199, (
                0.04167547137285199, 0.000983116060122767, 0.0005325002762709522,
                0.0002884263168208555, 0.00015622478323845052)),
            "pols_maturity": (0.03637807503601681, 0.03637807503601681, (
                0.0, 0.0, 0.0, 0.0, 0.03637807503601681)),
            "benefit_pp": (720000.0, 2000.0, (
                2000.0, 2000.0, 2000.0, 2000.0, 2000.0)),
            "premium_pp": (12600.0, 35.0, (
                35.0, 35.0, 35.0, 35.0, 35.0)),
        },
    },
    3: {"rows": 360, "months": (0, 89, 179, 269, 359),
        "result_cf": {
            "pols_if": (173.22606301057516, 1.0, (
                1.0, 0.6164010477201897, 0.44452682592348036, 0.31489434015296836,
                0.21595065704956337)),
            "pols_active": (170.9680294293639, 1.0, (
                1.0, 0.6128221979302395, 0.43851676539784407, 0.30588638587430766,
                0.20367709922579866)),
            "pols_sick": (2.258033581211283, 0.012273557823764708, (
                0.0, 0.0035788497899501247, 0.006010060525636274, 0.0090079542786607,
                0.012273557823764708)),
            "premiums": (5983.8810300277355, 35.0, (
                35.0, 21.448776927558384, 15.348086788924542, 10.706023505600768,
                7.128698472902953)),
            "claims_benefit": (4429.218416246049, 24.12366707447851, (
                0.0, 6.998218708654635, 11.794183539889993, 17.688980246917552,
                24.12366707447851)),
            "claims_death": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (1340.0414042858185, 5.0, (
                5.0, 3.900516041681371, 3.5892024414924357, 3.4483548904954424,
                3.2675954221027)),
            "net_cf": (214.6212094958678, 30.0, (
                30.0, 10.550042177222378, -0.035299192457886264, -10.431311631812227,
                -20.26256402367826)),
        },
        "result_pols": {
            "pols_if": (173.22606301057516, 1.0, (
                1.0, 0.6164010477201897, 0.44452682592348036, 0.31489434015296836,
                0.21595065704956337)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_active": (170.9680294293639, 1.0, (
                1.0, 0.6128221979302395, 0.43851676539784407, 0.30588638587430766,
                0.20367709922579866)),
            "pols_sick": (2.258033581211283, 0.012273557823764708, (
                0.0, 0.0035788497899501247, 0.006010060525636274, 0.0090079542786607,
                0.012273557823764708)),
            "pols_death_active": (0.053980455789236534, 0.00024228464227594627, (
                9.588388262971037e-05, 0.00010643034009796734, 0.00013799167469268113,
                0.0001900139547206286, 0.0002297075958327801)),
            "pols_lapse": (0.7253917576716465, 0.008740772775097947, (
                0.008740772775097947, 0.002080815342551728, 0.001488757636840065,
                0.0010381611417550054, 0.0006909181651563791)),
            "pols_inception": (0.05572428741855007, 0.00025111629229539347, (
                0.00010744006026721274, 0.00010798380603389967, 0.00013566737351341273,
                0.00020129656049174024, 0.0002380807930529868)),
            "pols_recovery": (0.0377959627912942, 0.00018106924010360815, (
                0.0, 7.08474792276741e-05, 9.798134756601884e-05, 0.00014098595945538875,
                0.00018106924010360815)),
            "pols_death_sick": (0.005628410296963661, 3.0655046421846046e-05, (
                0.0, 8.892956395132848e-06, 1.4987408125259746e-05, 2.247819574653525e-05,
                3.0655046421846046e-05)),
            "pols_exit": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.21499937624215237, 0.21499937624215237, (
                0.0, 0.0, 0.0, 0.0, 0.21499937624215237)),
            "benefit_pp": (720000.0, 2000.0, (
                2000.0, 2000.0, 2000.0, 2000.0, 2000.0)),
            "premium_pp": (12600.0, 35.0, (
                35.0, 35.0, 35.0, 35.0, 35.0)),
        },
    },
    4: {"rows": 216, "months": (0, 53, 107, 161, 215),
        "result_cf": {
            "pols_if": (130.79557877931396, 1.0, (
                1.0, 0.7094243669871011, 0.578366034800435, 0.47572124287070394,
                0.38967334315727875)),
            "pols_active": (125.66973713982436, 1.0, (
                1.0, 0.6950140118115505, 0.5547944667930101, 0.44227251138430534,
                0.3464687183539283)),
            "pols_sick": (5.125841639489591, 0.04320462480335046, (
                0.0, 0.014410355175550523, 0.0235715680074249, 0.03344873148639862,
                0.04320462480335046)),
            "premiums": (10196.282104293361, 58.0, (
                58.0, 48.07139393325608, 45.76046597103251, 45.46002987838643,
                42.468699374381956)),
            "claims_benefit": (10508.627010792085, 105.14448186961228, (
                0.0, 23.660286504365892, 43.8366863738726, 72.24034961411162,
                105.14448186961228)),
            "claims_death": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (997.4224576156463, 5.059299753539624, (
                5.0, 4.397791417996058, 4.409777872959884, 4.721078163302674,
                5.005619858219809)),
            "net_cf": (-1309.767364114371, 67.68140235345012, (
                53.0, 20.013316010894133, -2.485998275799977, -31.501397899027868,
                -67.68140235345012)),
        },
        "result_pols": {
            "pols_if": (130.79557877931396, 1.0, (
                1.0, 0.7094243669871011, 0.578366034800435, 0.47572124287070394,
                0.38967334315727875)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_active": (125.66973713982436, 1.0, (
                1.0, 0.6950140118115505, 0.5547944667930101, 0.44227251138430534,
                0.3464687183539283)),
            "pols_sick": (5.125841639489591, 0.04320462480335046, (
                0.0, 0.014410355175550523, 0.0235715680074249, 0.03344873148639862,
                0.04320462480335046)),
            "pols_death_active": (0.028401042602250563, 0.0001743721057051195, (
                0.00011284918248499753, 0.00011013228911956724, 0.00012345822131169787,
                0.00015048774139560903, 0.0001656220882298646)),
            "pols_lapse": (0.5706292676819184, 0.008740624471046883, (
                0.008740624471046883, 0.003573899569267409, 0.0018836922530067455,
                0.0015014699127044084, 0.0011760637378681806)),
            "pols_inception": (0.15409307736943212, 0.0009843087207179104, (
                0.000605036655185828, 0.0005739981764779483, 0.0006385956712805597,
                0.0008304730447151006, 0.0009349159667995031)),
            "pols_recovery": (0.09800291867554342, 0.0006874144609124853, (
                0.0, 0.0003601651881632129, 0.00044287897284198575, 0.0005706085990107735,
                0.0006874144609124853)),
            "pols_death_sick": (0.012745815579794078, 0.00010778319514280028, (
                0.0, 3.561791465166831e-05, 5.863235107697922e-05, 8.334763985122485e-05,
                0.00010778319514280028)),
            "pols_exit": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.3882238741360379, 0.3882238741360379, (
                0.0, 0.0, 0.0, 0.0, 0.3882238741360379)),
            "benefit_pp": (421459.83674394235, 2479.2714484076278, (
                1500.0, 1688.2632150000002, 1900.1551220814245, 2202.8005701773473,
                2479.2714484076278)),
            "premium_pp": (18691.138253078985, 122.57585497516371, (
                58.0, 69.16607883624998, 82.48183554452322, 102.78737364006032,
                122.57585497516371)),
        },
    },
    5: {"rows": 180, "months": (0, 44, 89, 134, 179),
        "result_cf": {
            "pols_if": (94.04345223106125, 1.0, (
                1.0, 0.664022521368666, 0.48869774237153724, 0.35966473382073927,
                0.2647008765102848)),
            "pols_active": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_sick": (94.04345223106125, 1.0, (
                1.0, 0.664022521368666, 0.48869774237153724, 0.35966473382073927,
                0.2647008765102848)),
            "premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_benefit": (186612.71181303513, 1968.0942114278405, (
                1968.0942114278405, 1319.0282084071557, 970.7594047326965,
                714.4455409448597, 525.8073509126017)),
            "claims_death": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (3341.815913854607, 30.0, (
                30.0, 21.76786013122855, 18.031097443046697, 14.935803199792785,
                12.011514779087957)),
            "net_cf": (-189954.5277268897, 1998.0942114278405, (
                -1998.0942114278405, -1340.7960685383844, -988.7905021757432,
                -729.3813441446524, -537.8188656916897)),
        },
        "result_pols": {
            "pols_if": (94.04345223106125, 1.0, (
                1.0, 0.664022521368666, 0.48869774237153724, 0.35966473382073927,
                0.2647008765102848)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_active": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_sick": (94.04345223106125, 1.0, (
                1.0, 0.664022521368666, 0.48869774237153724, 0.35966473382073927,
                0.2647008765102848)),
            "pols_death_active": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_inception": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_recovery": (0.49995902174999696, 0.013451947011868914, (
                0.013451947011868914, 0.002832267729116936, 0.0020844516570888124,
                0.0015340847427919504, 0.001129033619016079)),
            "pols_death_sick": (0.23713730279370615, 0.002500947274210845, (
                0.002500947274210845, 0.001676149435971267, 0.0012335883481001716,
                0.0009078786055174837, 0.0006681674349678921)),
            "pols_exit": (0.49995902174999696, 0.013451947011868914, (
                0.013451947011868914, 0.002832267729116936, 0.0020844516570888124,
                0.0015340847427919504, 0.001129033619016079)),
            "pols_maturity": (0.26290367545630083, 0.26290367545630083, (
                0.0, 0.0, 0.0, 0.0, 0.26290367545630083)),
            "benefit_pp": (360000.0, 2000.0, (
                2000.0, 2000.0, 2000.0, 2000.0, 2000.0)),
            "premium_pp": (6300.0, 35.0, (
                35.0, 35.0, 35.0, 35.0, 35.0)),
        },
    },
    6: {"rows": 120, "months": (0, 29, 59, 89, 119),
        "result_cf": {
            "pols_if": (83.59524262889164, 1.0, (
                1.0, 0.7944674828107864, 0.6676287549678728, 0.5872683823335583,
                0.5147770092243252)),
            "pols_active": (82.26998845969385, 1.0, (
                1.0, 0.7871604657379319, 0.6561422513012599, 0.572080336447802,
                0.4962072005922156)),
            "pols_sick": (1.3252541691978055, 0.018569808632109566, (
                0.0, 0.007307017072854569, 0.011486503666612817, 0.015188045885756339,
                0.018569808632109566)),
            "premiums": (6313.524608003509, 64.0, (
                64.0, 55.014330086237756, 50.077557717293786, 49.8254268052328,
                47.19431100407378)),
            "claims_benefit": (4607.523056051799, 71.20416634414374, (
                0.0, 22.45161632812347, 37.76288918287133, 54.77873095917679,
                71.20416634414374)),
            "claims_death": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (511.13296990369884, 5.0, (
                5.0, 4.408053122884602, 4.080314254450112, 4.078314694656055,
                3.9640708947390317)),
            "net_cf": (1194.868582048011, 59.0, (
                59.0, 28.154660635229682, 8.234354279972347, -9.031618848600043,
                -27.973926234808992)),
        },
        "result_pols": {
            "pols_if": (83.59524262889164, 1.0, (
                1.0, 0.7944674828107864, 0.6676287549678728, 0.5872683823335583,
                0.5147770092243252)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_active": (82.26998845969385, 1.0, (
                1.0, 0.7871604657379319, 0.6561422513012599, 0.572080336447802,
                0.4962072005922156)),
            "pols_sick": (1.3252541691978055, 0.018569808632109566, (
                0.0, 0.007307017072854569, 0.011486503666612817, 0.015188045885756339,
                0.018569808632109566)),
            "pols_death_active": (0.06214810163969327, 0.0005901919156121277, (
                0.0005240067387547453, 0.0004889772150763747, 0.0004832318332581747,
                0.0005440157205801662, 0.0005596238532275521)),
            "pols_lapse": (0.42208222806083817, 0.008737030291648887, (
                0.008737030291648887, 0.004045861559902304, 0.003372062750424384,
                0.0019409677503032538, 0.0016832455385201767)),
            "pols_inception": (0.05264003645012738, 0.0004948712704217465, (
                0.0004357392154130059, 0.00041856413475517594, 0.0004108937359246468,
                0.00046344050449899154, 0.00046924019099413923)),
            "pols_recovery": (0.03069834614813341, 0.00033288898800155816, (
                0.0, 0.00023482147843956856, 0.0002741337869393123, 0.0003036060588493989,
                0.00033288898800155816)),
            "pols_death_sick": (0.003281761944756284, 4.623147786444707e-05, (
                0.0, 1.7928359638403678e-05, 2.842390272129055e-05, 3.7732778550936025e-05,
                4.623147786444707e-05)),
            "pols_exit": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.512487908354713, 0.512487908354713, (
                0.0, 0.0, 0.0, 0.0, 0.512487908354713)),
            "benefit_pp": (412699.65521294647, 3914.3195514877348, (
                3000.0, 3182.7, 3376.5264300000003, 3689.6215962746105,
                3914.3195514877348)),
            "premium_pp": (9437.344797574773, 95.1100889865123, (
                64.0, 69.88959999999999, 76.32119043999998, 87.0951571498018,
                95.1100889865123)),
        },
    },
    7: {"rows": 360, "months": (0, 89, 179, 269, 359),
        "result_cf": {
            "pols_if": (204.83502964814946, 1.0, (
                1.0, 0.7290857786456274, 0.5400879628492968, 0.39157569641351797,
                0.27456808400577853)),
            "pols_active": (139.17649379703482, 0.5253882157241561, (
                0.0, 0.49613729973011583, 0.4102420338512155, 0.31546269675988314,
                0.22531773486351203)),
            "pols_sick": (65.65853585111468, 1.0, (
                1.0, 0.23294847891551157, 0.1298459289980813, 0.0761129996536348,
                0.0492503491422665)),
            "premiums": (4871.1772828962185, 18.388587550345463, (
                0.0, 17.364805490554055, 14.358471184792542, 11.04119438659591,
                7.886120720222921)),
            "claims_benefit": (129310.47603252057, 1911.7902587184922, (
                1911.7902587184922, 462.6461616926935, 257.79573354955943,
                150.9836786603514, 97.55014656739586)),
            "claims_death": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (3645.3003457368227, 30.0, (
                30.0, 11.645848879262598, 8.994747966037984, 7.397507085998612,
                6.136730227785117)),
            "net_cf": (-128084.59909536116, 1941.7902587184922, (
                -1941.7902587184922, -456.92720508140206, -252.43201033080487,
                -147.3399913597541, -95.80075607495806)),
        },
        "result_pols": {
            "pols_if": (204.83502964814946, 1.0, (
                1.0, 0.7290857786456274, 0.5400879628492968, 0.39157569641351797,
                0.27456808400577853)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_active": (139.17649379703482, 0.5253882157241561, (
                0.0, 0.49613729973011583, 0.4102420338512155, 0.31546269675988314,
                0.22531773486351203)),
            "pols_sick": (65.65853585111468, 1.0, (
                1.0, 0.23294847891551157, 0.1298459289980813, 0.0761129996536348,
                0.0492503491422665)),
            "pols_death_active": (0.05075673212018357, 0.0002660147436878282, (
                0.0, 8.616538650836261e-05, 0.00012909423252974476, 0.0001959626755105434,
                0.00025411396455821735)),
            "pols_lapse": (0.5114968547427892, 0.002701744144551599, (
                0.0, 0.001684616041614292, 0.0013927653605095213, 0.0010706626007995251,
                0.0007643280297138609)),
            "pols_inception": (0.05233628494976246, 0.0002757113926136321, (
                0.0, 8.74230635267201e-05, 0.00012691979789393153, 0.0002075985030837785,
                0.00026337681167452914)),
            "pols_recovery": (0.8389771022987, 0.04167547137285199, (
                0.04167547137285199, 0.0010374924443776877, 0.0006204694010778125,
                0.00042929846166237656, 0.000351314428399228)),
            "pols_death_sick": (0.16432073255569168, 0.002429399267901949, (
                0.002429399267901949, 0.0005879056247871468, 0.0003275928222237926,
                0.00019186186179673978, 0.00012396143016934132)),
            "pols_exit": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.2734256805813371, 0.2734256805813371, (
                0.0, 0.0, 0.0, 0.0, 0.2734256805813371)),
            "benefit_pp": (720000.0, 2000.0, (
                2000.0, 2000.0, 2000.0, 2000.0, 2000.0)),
            "premium_pp": (12600.0, 35.0, (
                35.0, 35.0, 35.0, 35.0, 35.0)),
        },
    },
    8: {"rows": 348, "months": (0, 86, 173, 260, 347),
        "result_cf": {
            "pols_if": (161.7923082047461, 0.8990020046529406, (
                0.8990020046529406, 0.5968983985183911, 0.43470799287565637,
                0.31115759434064993, 0.21595065704956345)),
            "pols_active": (159.54023195884588, 0.8980369489072441, (
                0.8980369489072441, 0.5930746967133909, 0.4285250718029683,
                0.30204055901307725, 0.20367709922579874)),
            "pols_sick": (2.2520762459002324, 0.012273557823764714, (
                0.0009650557456964584, 0.0038237018050002666, 0.00618292107268808,
                0.009117035327572678, 0.012273557823764714)),
            "premiums": (9982.024258880147, 32.845701406282444, (
                32.845701406282444, 29.519416137889937, 29.026096675963103,
                27.841440365693458, 25.549515470056146)),
            "claims_benefit": (7943.386134514236, 56.84900170617032, (
                1.9003336989550834, 9.47808051127858, 18.905729076235435,
                34.305061994813364, 56.84900170617032)),
            "claims_death": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (1245.362812498929, 4.519136416907115, (
                4.519136416907115, 3.7881154762373344, 3.5214797887839886,
                3.3182332017396634, 3.172422739905535)),
            "net_cf": (793.275311866983, 34.471908976019705, (
                26.426231290420247, 16.253220150374023, 6.59888781094368,
                -9.781854830859569, -34.471908976019705)),
        },
        "result_pols": {
            "pols_if": (161.7923082047461, 0.8990020046529406, (
                0.8990020046529406, 0.5968983985183911, 0.43470799287565637,
                0.31115759434064993, 0.21595065704956345)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_active": (159.54023195884588, 0.8980369489072441, (
                0.8980369489072441, 0.5930746967133909, 0.4285250718029683,
                0.30204055901307725, 0.20367709922579874)),
            "pols_sick": (2.2520762459002324, 0.012273557823764714, (
                0.0009650557456964584, 0.0038237018050002666, 0.00618292107268808,
                0.009117035327572678, 0.012273557823764714)),
            "pols_death_active": (0.0528847141978573, 0.00024228464227594638, (
                9.373251387698123e-05, 0.00011212559263708589, 0.0001468040112511499,
                0.00018762496062079477, 0.00022970759583278017)),
            "pols_lapse": (0.6255039766620092, 0.006217702408793537, (
                0.006217702408793537, 0.0020137324364930165, 0.0014547953866808237,
                0.0010251086222914957, 0.0006909181651563794)),
            "pols_inception": (0.05449648416959612, 0.0002511162922953935, (
                0.00010410145863117724, 0.00011239778344148573, 0.00014256939050187568,
                0.00019876571323876525, 0.0002380807930529869)),
            "pols_recovery": (0.037547688034080026, 0.00018106924010360823, (
                4.021915310297908e-05, 7.315183892050131e-05, 0.00010006670022939809,
                0.00014250716368835188, 0.00018106924010360823)),
            "pols_death_sick": (0.005613937550920347, 3.065504642184606e-05, (
                2.3445057220795452e-06, 9.507826492635746e-06, 1.5420331545071817e-05,
                2.2750865181693274e-05, 3.065504642184606e-05)),
            "pols_exit": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.21499937624215248, 0.21499937624215248, (
                0.0, 0.0, 0.0, 0.0, 0.21499937624215248)),
            "benefit_pp": (1117809.9769517288, 4713.131012018762, (
                2060.0, 2533.5401627752326, 3115.93483320153, 3832.2068177215647,
                4713.131012018762)),
            "premium_pp": (25202.969255677413, 125.44127723329201, (
                36.574999999999996, 49.77352144928126, 67.73488550819035, 92.17782027905737,
                125.44127723329201)),
        },
    },
    9: {"rows": 300, "months": (0, 74, 149, 224, 299),
        "result_cf": {
            "pols_if": (124.2498038784439, 0.6833048851582468, (
                0.6833048851582468, 0.5242942317945674, 0.3972657425777203,
                0.2965315011475069, 0.21595065704956337)),
            "pols_active": (122.09187514615107, 0.680544177973712, (
                0.680544177973712, 0.51953400328575, 0.3903416800873472,
                0.28696846929402947, 0.20367709922579866)),
            "pols_sick": (2.1579287322928282, 0.012273557823764708, (
                0.0027607071845347957, 0.004760228508817411, 0.006924062490373089,
                0.009563031853477446, 0.012273557823764708)),
            "premiums": (8522.526456015428, 29.74121481166265, (
                29.682865182804168, 29.509456885392535, 28.87286691241715,
                27.64247374781659, 25.54951547005614)),
            "claims_benefit": (7745.337588585269, 56.849001706170284, (
                6.235078387832318, 12.91865763854462, 22.464362396789134, 37.0663920890376,
                56.849001706170284)),
            "claims_death": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (930.2771275374874, 3.485542105404604, (
                3.485542105404604, 3.2722727022299614, 3.0788312241773994,
                2.9311356960893304, 2.818656514919269)),
            "net_cf": (-153.08826010732992, 34.11814275103342, (
                19.962244689567246, 13.318526544617953, 3.329673291450618,
                -12.355054037310339, -34.11814275103342)),
        },
        "result_pols": {
            "pols_if": (124.2498038784439, 0.6833048851582468, (
                0.6833048851582468, 0.5242942317945674, 0.3972657425777203,
                0.2965315011475069, 0.21595065704956337)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_active": (122.09187514615107, 0.680544177973712, (
                0.680544177973712, 0.51953400328575, 0.3903416800873472,
                0.28696846929402947, 0.20367709922579866)),
            "pols_sick": (2.1579287322928282, 0.012273557823764708, (
                0.0027607071845347957, 0.004760228508817411, 0.006924062490373089,
                0.009563031853477446, 0.012273557823764708)),
            "pols_death_active": (0.048457305255410046, 0.00024228464227594627, (
                9.973924691739356e-05, 0.0001267144721425374, 0.00015849455161898429,
                0.00019409747724682087, 0.0002297075958327801)),
            "pols_lapse": (0.414465939565406, 0.0023108255128237937, (
                0.0023108255128237937, 0.001763934784716548, 0.0013250828554024533,
                0.0009739010227759583, 0.0006909181651563791)),
            "pols_inception": (0.04970981644217828, 0.00025111629229539347, (
                0.00010180405765048338, 0.0001243986967570978, 0.0001623967053862533,
                0.00020563548129808222, 0.0002380807930529868)),
            "pols_recovery": (0.034788345201143406, 0.00018106924010360815, (
                6.465586905064148e-05, 8.201243204688855e-05, 0.00011113704543057546,
                0.00014854817188290822, 0.00018106924010360815)),
            "pols_death_sick": (0.005382264095277463, 3.0655046421846046e-05, (
                6.834621150150684e-06, 1.185950518064562e-05, 1.727109720537422e-05,
                2.3866173807014352e-05, 3.0655046421846046e-05)),
            "pols_exit": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.21499937624215237, 0.21499937624215237, (
                0.0, 0.0, 0.0, 0.0, 0.21499937624215237)),
            "benefit_pp": (1014390.7175117286, 4713.131012018761, (
                2318.5481486000003, 2768.4677414488915, 3305.6952645435035,
                3947.173022253211, 4713.131012018761)),
            "premium_pp": (23325.271170914915, 125.44127723329203, (
                43.61636781785936, 56.79985659988068, 73.96818834708155, 96.32582219161493,
                125.44127723329203)),
        },
    },
    10: {"rows": 1, "months": (0,),
        "result_cf": {
            "pols_if": (0.21595065704956337, 0.21595065704956337, (
                0.21595065704956337,)),
            "pols_active": (0.20367709922579866, 0.20367709922579866, (
                0.20367709922579866,)),
            "pols_sick": (0.012273557823764708, 0.012273557823764708, (
                0.012273557823764708,)),
            "premiums": (25.549515470056132, 25.549515470056132, (
                25.549515470056132,)),
            "claims_benefit": (56.849001706170284, 56.849001706170284, (
                56.849001706170284,)),
            "claims_death": (0.0, 0.0, (
                0.0,)),
            "claims_lapse": (0.0, 0.0, (
                0.0,)),
            "expenses": (1.3865922308419347, 1.3865922308419347, (
                1.3865922308419347,)),
            "net_cf": (-32.68607846695609, 32.68607846695609, (
                -32.68607846695609,)),
        },
        "result_pols": {
            "pols_if": (0.21595065704956337, 0.21595065704956337, (
                0.21595065704956337,)),
            "pols_new_biz": (0.0, 0.0, (
                0.0,)),
            "pols_active": (0.20367709922579866, 0.20367709922579866, (
                0.20367709922579866,)),
            "pols_sick": (0.012273557823764708, 0.012273557823764708, (
                0.012273557823764708,)),
            "pols_death_active": (0.0002297075958327801, 0.0002297075958327801, (
                0.0002297075958327801,)),
            "pols_lapse": (0.0006909181651563791, 0.0006909181651563791, (
                0.0006909181651563791,)),
            "pols_inception": (0.0002380807930529868, 0.0002380807930529868, (
                0.0002380807930529868,)),
            "pols_recovery": (0.00018106924010360815, 0.00018106924010360815, (
                0.00018106924010360815,)),
            "pols_death_sick": (3.0655046421846046e-05, 3.0655046421846046e-05, (
                3.0655046421846046e-05,)),
            "pols_exit": (0.0, 0.0, (
                0.0,)),
            "pols_maturity": (0.21499937624215237, 0.21499937624215237, (
                0.21499937624215237,)),
            "benefit_pp": (4713.131012018762, 4713.131012018762, (
                4713.131012018762,)),
            "premium_pp": (125.441277233292, 125.441277233292, (
                125.441277233292,)),
        },
    },
    11: {"rows": 336, "months": (0, 83, 167, 251, 335),
        "result_cf": {
            "pols_if": (48.126235170116146, 0.4234050000000007, (
                0.4234050000000007, 0.2038901782140296, 0.11504392289861061,
                0.06491290709456435, 0.03662675438476751)),
            "pols_active": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_sick": (48.126235170116146, 0.4234050000000007, (
                0.4234050000000007, 0.2038901782140296, 0.11504392289861061,
                0.06491290709456435, 0.03662675438476751)),
            "premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_benefit": (95478.41649030431, 833.3009295896062, (
                833.3009295896062, 405.01170943289907, 228.5256518051677,
                128.94435473507977, 72.75615007203362)),
            "claims_death": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (1899.008120666905, 12.702150000000021, (
                12.702150000000021, 7.303666066085075, 5.0683763791299645,
                3.517197923356339, 2.440758204738079)),
            "net_cf": (-97377.42461097123, 846.0030795896063, (
                -846.0030795896063, -412.31537549898417, -233.59402818429768,
                -132.46155265843612, -75.1969082767717)),
        },
        "result_pols": {
            "pols_if": (48.126235170116146, 0.4234050000000007, (
                0.4234050000000007, 0.2038901782140296, 0.11504392289861061,
                0.06491290709456435, 0.03662675438476751)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_active": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_sick": (48.126235170116146, 0.4234050000000007, (
                0.4234050000000007, 0.2038901782140296, 0.11504392289861061,
                0.06491290709456435, 0.03662675438476751)),
            "pols_death_active": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_inception": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_recovery": (0.26569813690045285, 0.0056956216245603675, (
                0.0056956216245603675, 0.0008696566056964868, 0.0004906990045836829,
                0.00027687424153649494, 0.00015622478323845052)),
            "pols_death_sick": (0.1213287880635329, 0.0010589135806372445, (
                0.0010589135806372445, 0.0005146668918836062, 0.00029039799144307674,
                0.00016385548548797087, 9.245456551224613e-05)),
            "pols_exit": (0.26569813690045285, 0.0056956216245603675, (
                0.0056956216245603675, 0.0008696566056964868, 0.0004906990045836829,
                0.00027687424153649494, 0.00015622478323845052)),
            "pols_maturity": (0.03637807503601681, 0.03637807503601681, (
                0.0, 0.0, 0.0, 0.0, 0.03637807503601681)),
            "benefit_pp": (672000.0, 2000.0, (
                2000.0, 2000.0, 2000.0, 2000.0, 2000.0)),
            "premium_pp": (11760.0, 35.0, (
                35.0, 35.0, 35.0, 35.0, 35.0)),
        },
    },
    12: {"rows": 174, "months": (0, 43, 86, 129, 173),
        "result_cf": {
            "pols_if": (88.27771625999614, 0.9080198235721512, (
                0.9080198235721512, 0.641784465741572, 0.47881105344214075,
                0.35722277047242984, 0.2647008765102848)),
            "pols_active": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_sick": (88.27771625999614, 0.9080198235721512, (
                0.9080198235721512, 0.641784465741572, 0.47881105344214075,
                0.35722277047242984, 0.2647008765102848)),
            "premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_benefit": (175265.20022376056, 1795.6010304613533, (
                1795.6010304613533, 1274.8540701387656, 951.120279302521, 709.5947739352146,
                525.8073509126017)),
            "claims_death": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (3124.07974591118, 27.240594707164533, (
                27.240594707164533, 21.038856416891726, 17.66631603315119,
                14.402325969377529, 12.011514779087957)),
            "net_cf": (-178389.27996967177, 1822.8416251685178, (
                -1822.8416251685178, -1295.8929265556574, -968.7865953356722,
                -723.9970999045921, -537.8188656916897)),
        },
        "result_pols": {
            "pols_if": (88.27771625999614, 0.9080198235721512, (
                0.9080198235721512, 0.641784465741572, 0.47881105344214075,
                0.35722277047242984, 0.2647008765102848)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_active": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_sick": (88.27771625999614, 0.9080198235721512, (
                0.9080198235721512, 0.641784465741572, 0.47881105344214075,
                0.35722277047242984, 0.2647008765102848)),
            "pols_death_active": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_inception": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_recovery": (0.4223986469828025, 0.007937556036820101, (
                0.007937556036820101, 0.0027374153328742533, 0.0020422817771503566,
                0.0015236689906682913, 0.001129033619016079)),
            "pols_death_sick": (0.22271750113305144, 0.002281752304654424, (
                0.002281752304654424, 0.001620015339314993, 0.0012086320137299543,
                0.000901714514154295, 0.0006681674349678921)),
            "pols_exit": (0.4223986469828025, 0.007937556036820101, (
                0.007937556036820101, 0.0027374153328742533, 0.0020422817771503566,
                0.0015236689906682913, 0.001129033619016079)),
            "pols_maturity": (0.26290367545630083, 0.26290367545630083, (
                0.0, 0.0, 0.0, 0.0, 0.26290367545630083)),
            "benefit_pp": (348000.0, 2000.0, (
                2000.0, 2000.0, 2000.0, 2000.0, 2000.0)),
            "premium_pp": (6090.0, 35.0, (
                35.0, 35.0, 35.0, 35.0, 35.0)),
        },
    },
    13: {"rows": 348, "months": (0, 86, 173, 260, 347),
        "result_cf": {
            "pols_if": (192.26614869933107, 0.9565537273793496, (
                0.9565537273793496, 0.7052489205901273, 0.5269565656361147,
                0.38573672461060127, 0.27354150141565015)),
            "pols_active": (136.09628270361122, 0.5219442862117151, (
                0.37434038107341494, 0.4857886362426922, 0.4019457703554252,
                0.3109025473099095, 0.22434934580133503)),
            "pols_sick": (56.169865995719846, 0.5822133463059347, (
                0.5822133463059347, 0.2194602843474352, 0.12501079528068948,
                0.07483417730069174, 0.04919215561431509)),
            "premiums": (4763.369894626392, 18.268050017410026, (
                13.101913337569522, 17.002602268494226, 14.068101962439883,
                10.881589155846832, 7.852227103046726)),
            "claims_benefit": (111169.6109368867, 1133.9536507291352, (
                1133.9536507291352, 435.8497412840426, 248.18823547579137,
                148.44164226099946, 97.43577062841267)),
            "claims_death": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (3245.8815037134736, 19.338102294545116, (
                19.338102294545116, 11.084547785705016, 8.712596544069047,
                7.068260019781086, 5.94291821423709)),
            "net_cf": (-109652.12254597378, 1140.1898396861106, (
                -1140.1898396861106, -429.93168680125336, -242.83273005742055,
                -144.62831312493373, -95.52646173960304)),
        },
        "result_pols": {
            "pols_if": (192.26614869933107, 0.9565537273793496, (
                0.9565537273793496, 0.7052489205901273, 0.5269565656361147,
                0.38573672461060127, 0.27354150141565015)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_active": (136.09628270361122, 0.5219442862117151, (
                0.37434038107341494, 0.4857886362426922, 0.4019457703554252,
                0.3109025473099095, 0.22434934580133503)),
            "pols_sick": (56.169865995719846, 0.5822133463059347, (
                0.5822133463059347, 0.2194602843474352, 0.12501079528068948,
                0.07483417730069174, 0.04919215561431509)),
            "pols_death_active": (0.05028273327211082, 0.00026486278475874175, (
                3.9071738647696155e-05, 9.184229075514993e-05, 0.0001376984808504762,
                0.0001931299504494724, 0.00025302181269554365)),
            "pols_lapse": (0.49259906755301075, 0.002684034161502853, (
                0.0019250364368768379, 0.0016494521508044783, 0.001364561587840546,
                0.0010551857107574053, 0.0007610430379472848)),
            "pols_inception": (0.05182731113394738, 0.00027451744299952785, (
                4.3471799965770985e-05, 9.206524277181824e-05, 0.00013372651278786374,
                0.00020459757711257433, 0.0002622448491869284)),
            "pols_recovery": (0.4437922211998328, 0.01379555420542261, (
                0.01379555420542261, 0.0009815595168794007, 0.0006012934075220933,
                0.0004247245902420427, 0.00035045421267309934)),
            "pols_death_sick": (0.14126830607665794, 0.0014409667359445138, (
                0.0014409667359445138, 0.0005538541885345077, 0.0003153841352716858,
                0.00018863157994997208, 0.00012381608743565795)),
            "pols_exit": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.27240362047757166, 0.27240362047757166, (
                0.0, 0.0, 0.0, 0.0, 0.27240362047757166)),
            "benefit_pp": (696000.0, 2000.0, (
                2000.0, 2000.0, 2000.0, 2000.0, 2000.0)),
            "premium_pp": (12180.0, 35.0, (
                35.0, 35.0, 35.0, 35.0, 35.0)),
        },
    },
    14: {"rows": 203, "months": (0, 50, 101, 151, 202),
        "result_cf": {
            "pols_if": (118.46326783917183, 0.8926809653552612, (
                0.8926809653552612, 0.6765652213330389, 0.5640019654053865,
                0.4705353897144851, 0.38967334315727875)),
            "pols_active": (113.37634002420924, 0.8869172872810266, (
                0.8869172872810266, 0.6604184425006571, 0.539111471990995,
                0.43657488342770007, 0.3464687183539283)),
            "pols_sick": (5.086927814962587, 0.04320462480335046, (
                0.005763678074234626, 0.01614677883238184, 0.024890493414391555,
                0.03396050628678503, 0.04320462480335046)),
            "premiums": (9480.932852608461, 53.75605678210302, (
                53.75605678210302, 47.734088991564995, 46.4679144427088, 44.874385664748786,
                42.46869937438196)),
            "claims_benefit": (10452.597561727089, 105.14448186961228, (
                8.521894846643045, 27.3594501280752, 47.690897852636915, 73.35288279423615,
                105.14448186961228)),
            "claims_death": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (905.3231425490983, 4.9084332773675, (
                4.607496778632171, 4.261734131473858, 4.360567387304953, 4.564843811688981,
                4.8598251050677765)),
            "net_cf": (-1876.987851667723, 67.53560760029809, (
                40.62666515682781, 16.112904732015938, -5.583550797233065,
                -33.043340941176346, -67.53560760029809)),
        },
        "result_pols": {
            "pols_if": (118.46326783917183, 0.8926809653552612, (
                0.8926809653552612, 0.6765652213330389, 0.5640019654053865,
                0.4705353897144851, 0.38967334315727875)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_active": (113.37634002420924, 0.8869172872810266, (
                0.8869172872810266, 0.6604184425006571, 0.539111471990995,
                0.43657488342770007, 0.3464687183539283)),
            "pols_sick": (5.086927814962587, 0.04320462480335046, (
                0.005763678074234626, 0.01614677883238184, 0.024890493414391555,
                0.03396050628678503, 0.04320462480335046)),
            "pols_death_active": (0.02700481264026822, 0.0001743721057051195, (
                0.00010895154767303903, 0.0001139206806401035, 0.00013059975806324582,
                0.00014854906526170624, 0.0001656220882298646)),
            "pols_lapse": (0.4648010002159791, 0.006140600234583153, (
                0.006140600234583153, 0.002242429283586598, 0.0018304077153020238,
                0.0014821270489034232, 0.0011760637378681806)),
            "pols_inception": (0.14661311009829697, 0.0009843087207179104, (
                0.0005783160666622511, 0.0005997637006390201, 0.0006986558274188074,
                0.0008197743774568402, 0.0009349159667995031)),
            "pols_recovery": (0.0963811666954601, 0.0006874144609124853, (
                0.0002338701976896275, 0.00037312383922422977, 0.0004611624763590314,
                0.0005760458358634919, 0.0006874144609124853)),
            "pols_death_sick": (0.012651278362976906, 0.00010778319514280028, (
                1.4018331792218597e-05, 3.9986982225542356e-05, 6.192954153141706e-05,
                8.463123018979437e-05, 0.00010778319514280028)),
            "pols_exit": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.3882238741360379, 0.3882238741360379, (
                0.0, 0.0, 0.0, 0.0, 0.3882238741360379)),
            "benefit_pp": (401914.8367439423, 2479.2714484076278, (
                1545.0, 1738.9111114500001, 1957.1597757438674, 2202.800570177347,
                2479.2714484076278)),
            "premium_pp": (17934.52825307899, 122.57585497516374, (
                60.61, 72.27855238388123, 86.19351814402677, 102.78737364006032,
                122.57585497516374)),
        },
    },
    15: {"rows": 2, "months": (0, 1),
        "result_cf": {
            "pols_if": (1.0318537002734889, 0.5170766910491637, (
                0.5170766910491637, 0.5147770092243252)),
            "pols_active": (0.9948072513388695, 0.4986000507466539, (
                0.4986000507466539, 0.4962072005922156)),
            "pols_sick": (0.037046448934619274, 0.018569808632109566, (
                0.018476640302509707, 0.018569808632109566)),
            "premiums": (94.61620619926758, 47.4218951951938, (
                47.4218951951938, 47.19431100407378)),
            "claims_benefit": (142.04671793390762, 71.20416634414374, (
                70.84255158976387, 71.20416634414374)),
            "claims_death": (0.0, 0.0, (
                0.0, 0.0)),
            "claims_lapse": (0.0, 0.0, (
                0.0, 0.0)),
            "expenses": (6.0854297247329265, 3.047299462808561, (
                3.047299462808561, 3.0381302619243655)),
            "net_cf": (-53.51594145937296, 27.047985601994327, (
                -26.467955857378634, -27.047985601994327)),
        },
        "result_pols": {
            "pols_if": (1.0318537002734889, 0.5170766910491637, (
                0.5170766910491637, 0.5147770092243252)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0)),
            "pols_active": (0.9948072513388695, 0.4986000507466539, (
                0.4986000507466539, 0.4962072005922156)),
            "pols_sick": (0.037046448934619274, 0.018569808632109566, (
                0.018476640302509707, 0.018569808632109566)),
            "pols_death_active": (0.0011219463694773753, 0.0005623225162498232, (
                0.0005623225162498232, 0.0005596238532275521)),
            "pols_lapse": (0.003374608158658674, 0.0016913626201384977, (
                0.0016913626201384977, 0.0016832455385201767)),
            "pols_inception": (0.0009407431896665002, 0.000471502998672361, (
                0.000471502998672361, 0.00046924019099413923)),
            "pols_recovery": (0.0006652269686239275, 0.00033288898800155816, (
                0.00033233798062236937, 0.00033288898800155816)),
            "pols_death_sick": (9.222816631458135e-05, 4.623147786444707e-05, (
                4.5996688450134294e-05, 4.623147786444707e-05)),
            "pols_exit": (0.0, 0.0, (
                0.0, 0.0)),
            "pols_maturity": (0.512487908354713, 0.512487908354713, (
                0.0, 0.512487908354713)),
            "benefit_pp": (7828.63910297547, 3914.319551487735, (
                3914.319551487735, 3914.319551487735)),
            "premium_pp": (190.2201779730246, 95.1100889865123, (
                95.1100889865123, 95.1100889865123)),
        },
    },
    16: {"rows": 330, "months": (0, 82, 164, 246, 329),
        "result_cf": {
            "pols_if": (146.51925522605154, 0.8004288450760463, (
                0.8004288450760463, 0.5676547715020311, 0.4203464515503459,
                0.3062456358499245, 0.21595065704956337)),
            "pols_active": (144.29237015398306, 0.7986149793517856, (
                0.7986149793517856, 0.5634514822457842, 0.4139165918578226,
                0.2970025227312271, 0.20367709922579866)),
            "pols_sick": (2.226885072068476, 0.012273557823764708, (
                0.0018138657242607256, 0.004203289256246939, 0.006429859692523276,
                0.00924311311869734, 0.012273557823764708)),
            "premiums": (5050.232955389407, 27.951524277312497, (
                27.951524277312497, 19.720801878602447, 14.48708071502379,
                10.395088295592949, 7.128698472902953)),
            "claims_benefit": (4369.367439080438, 24.12366707447851, (
                3.5041273773297803, 8.232005771023022, 12.62140655407901,
                18.152004183971652, 24.12366707447851)),
            "claims_death": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (1117.3009043030597, 4.047490868486749, (
                4.047490868486749, 3.514521097473158, 3.3225263204379325, 3.182920678560124,
                3.080022077578188)),
            "net_cf": (-436.43538799409157, 20.399906031495966, (
                20.399906031495966, 7.9742750101062665, -1.456852159493153,
                -10.939836566938826, -20.074990679153746)),
        },
        "result_pols": {
            "pols_if": (146.51925522605154, 0.8004288450760463, (
                0.8004288450760463, 0.5676547715020311, 0.4203464515503459,
                0.3062456358499245, 0.21595065704956337)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_active": (144.29237015398306, 0.7986149793517856, (
                0.7986149793517856, 0.5634514822457842, 0.4139165918578226,
                0.2970025227312271, 0.20367709922579866)),
            "pols_sick": (2.226885072068476, 0.012273557823764708, (
                0.0018138657242607256, 0.004203289256246939, 0.006429859692523276,
                0.00924311311869734, 0.012273557823764708)),
            "pols_death_active": (0.05124809672216304, 0.00024228464227594627, (
                9.073674851005596e-05, 0.00011596318223161383, 0.00015437430234739545,
                0.00020088423142755406, 0.0002297075958327801)),
            "pols_lapse": (0.5286290171871827, 0.004106820426230346, (
                0.004106820426230346, 0.0019131173915796615, 0.0014051585025204945,
                0.0010079541538712173, 0.0006909181651563791)),
            "pols_inception": (0.052687401134288006, 0.00025111629229539347, (
                9.937051351667027e-05, 0.00011428375204435549, 0.0001549537495077311,
                0.00021282566986829295, 0.0002380807930529868)),
            "pols_recovery": (0.036648997603709516, 0.00018106924010360815, (
                5.734918076707047e-05, 7.682558472488904e-05, 0.0001031178172627902,
                0.0001440444452837702, 0.00018106924010360815)),
            "pols_death_sick": (0.005552354924547015, 3.0655046421846046e-05, (
                4.452854828764801e-06, 1.0460786010539424e-05, 1.6038598220981623e-05,
                2.30665814277419e-05, 3.0655046421846046e-05)),
            "pols_exit": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.21499937624215237, 0.21499937624215237, (
                0.0, 0.0, 0.0, 0.0, 0.21499937624215237)),
            "benefit_pp": (660000.0, 2000.0, (
                2000.0, 2000.0, 2000.0, 2000.0, 2000.0)),
            "premium_pp": (11550.0, 35.0, (
                35.0, 35.0, 35.0, 35.0, 35.0)),
        },
    },
    17: {"rows": 229, "months": (0, 57, 114, 171, 228),
        "result_cf": {
            "pols_if": (130.79557877931398, 1.0, (
                0.0, 0.7437919054211092, 0.590922664768311, 0.48096768052531064,
                0.38967334315727875)),
            "pols_active": (125.66973713982435, 1.0, (
                0.0, 0.7309884338479415, 0.5682601948060042, 0.44808633562338845,
                0.3464687183539283)),
            "pols_sick": (5.125841639489591, 0.04320462480335046, (
                0.0, 0.012803471573167595, 0.022662469962306784, 0.0328813449019222,
                0.04320462480335046)),
            "premiums": (10196.282104293361, 58.0, (
                0.0, 48.3823958314963, 46.87114393448757, 46.0576176027267,
                42.468699374381956)),
            "claims_benefit": (10508.627010792086, 105.14448186961228, (
                0.0, 20.364992939655227, 42.127929895960776, 71.00857511470069,
                105.14448186961228)),
            "claims_death": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (1029.8803143233208, 5.310462107585398, (
                0.0, 4.545982213145344, 4.594334810686895, 4.880933468701518,
                5.310462107585398)),
            "net_cf": (-1342.2252208220448, 67.98624460281572, (
                0.0, 23.471420678695726, 0.14887922783989893, -29.831890980675507,
                -67.98624460281572)),
        },
        "result_pols": {
            "pols_if": (130.79557877931398, 1.0, (
                0.0, 0.7437919054211092, 0.590922664768311, 0.48096768052531064,
                0.38967334315727875)),
            "pols_new_biz": (1.0, 1.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_active": (125.66973713982435, 1.0, (
                0.0, 0.7309884338479415, 0.5682601948060042, 0.44808633562338845,
                0.3464687183539283)),
            "pols_sick": (5.125841639489591, 0.04320462480335046, (
                0.0, 0.012803471573167595, 0.022662469962306784, 0.0328813449019222,
                0.04320462480335046)),
            "pols_death_active": (0.028401042602250563, 0.0001743721057051195, (
                0.0, 0.0001064074178266072, 0.00012645474512124698, 0.00015246595450198593,
                0.0001656220882298646)),
            "pols_lapse": (0.5706292676819184, 0.008740624471046883, (
                0.0, 0.0037589356404788385, 0.0019294124053467585, 0.0015212072509925428,
                0.0011760637378681806)),
            "pols_inception": (0.15409307736943212, 0.0009843087207179104, (
                0.0, 0.000544779160929372, 0.0006540953853808946, 0.0008413898984489163,
                0.0009349159667995031)),
            "pols_recovery": (0.09800291867554342, 0.0006874144609124853, (
                0.0, 0.0003473256834551569, 0.0004353385152747193, 0.0005638288440626573,
                0.0006874144609124853)),
            "pols_death_sick": (0.012745815579794074, 0.00010778319514280028, (
                0.0, 3.1576935371463075e-05, 5.634685876436449e-05, 8.192647428512173e-05,
                0.00010778319514280028)),
            "pols_exit": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.3882238741360379, 0.3882238741360379, (
                0.0, 0.0, 0.0, 0.0, 0.3882238741360379)),
            "benefit_pp": (421459.8367439423, 2479.2714484076278, (
                0.0, 1639.0905, 1900.1551220814245, 2202.8005701773473,
                2479.2714484076278)),
            "premium_pp": (18691.13825307899, 122.57585497516371, (
                0.0, 66.18763524999999, 82.48183554452322, 102.78737364006032,
                122.57585497516371)),
        },
    },
    18: {"rows": 320, "months": (0, 79, 159, 239, 319),
        "result_cf": {
            "pols_if": (137.51361943540485, 0.7528583307461296, (
                0.7528583307461296, 0.5487912238313405, 0.40899538706276817,
                0.299974241821854, 0.21410156272083639)),
            "pols_active": (135.32439218705827, 0.750699698543944, (
                0.750699698543944, 0.5444471290684625, 0.4024532635789154,
                0.29067801956487554, 0.2019323111528704)),
            "pols_sick": (2.18922724834655, 0.012169251567966012, (
                0.002158632202185595, 0.00434409476287796, 0.0065421234838527725,
                0.009296222256978477, 0.012169251567966012)),
            "premiums": (9835.544316820175, 32.68597369005319, (
                32.64071613476043, 30.82810942490371, 31.011349563996504,
                30.481156353196152, 27.575462461031705)),
            "claims_benefit": (8249.892269284177, 59.71353472161252, (
                4.844190351957195, 11.764750706656203, 21.830964485031163,
                38.170579106818174, 59.71353472161252)),
            "claims_death": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (1042.6016037862212, 3.818257458785288, (
                3.818257458785288, 3.4061040138527137, 3.2433007950792603,
                3.037557793968222, 2.9647503442567236)),
            "net_cf": (543.0504437497764, 35.102822604837534, (
                23.978268324017947, 15.657254704394793, 5.93708428388608,
                -10.726980547590244, -35.102822604837534)),
        },
        "result_pols": {
            "pols_if": (137.51361943540485, 0.7528583307461296, (
                0.7528583307461296, 0.5487912238313405, 0.40899538706276817,
                0.299974241821854, 0.21410156272083639)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_active": (135.32439218705827, 0.750699698543944, (
                0.750699698543944, 0.5444471290684625, 0.4024532635789154,
                0.29067801956487554, 0.2019323111528704)),
            "pols_sick": (2.18922724834655, 0.012169251567966012, (
                0.002158632202185595, 0.00434409476287796, 0.0065421234838527725,
                0.009296222256978477, 0.012169251567966012)),
            "pols_death_active": (0.04989990069722042, 0.00024020907784303022, (
                9.284586021788542e-05, 0.0001120519221850312, 0.00015009894025646645,
                0.00019660651369623564, 0.0002277398190184327)),
            "pols_lapse": (0.4843408385940542, 0.0038603806750066396, (
                0.0038603806750066396, 0.001848590880025652, 0.0013662429492057751,
                0.0009864903320185503, 0.0006849994547146229)),
            "pols_inception": (0.0512486514909439, 0.0002489650703280495, (
                9.963928620338095e-05, 0.00011042913659880948, 0.00015066233975611425,
                0.00020829366586177822, 0.0002360412877296532)),
            "pols_recovery": (0.035752744483017684, 0.0001795216533353496, (
                6.1017767388273656e-05, 7.767243666741708e-05, 0.00010497592533208131,
                0.00014479741304523246, 0.0001795216533353496)),
            "pols_death_sick": (0.005459162555951896, 3.0394548200360727e-05, (
                5.317554565296777e-06, 1.0815588004101936e-05, 1.6318481995290097e-05,
                2.31993068652436e-05, 3.0394548200360727e-05)),
            "pols_exit": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.21315842889890296, 0.21315842889890296, (
                0.0, 0.0, 0.0, 0.0, 0.21315842889890296)),
            "benefit_pp": (1121774.7480585226, 4993.047932180883, (
                2315.2500000000005, 2764.5295795387683, 3400.022680068736,
                4181.599036068364, 4993.047932180883)),
            "premium_pp": (26285.456353002395, 136.55795005563047, (
                43.480390625, 56.622778923731225, 77.05577857220088, 104.86226787572136,
                136.55795005563047)),
        },
    },
    19: {"rows": 186, "months": (0, 46, 92, 138, 185),
        "result_cf": {
            "pols_if": (101.64750376353345, 0.7817909121530964, (
                0.7817909121530964, 0.6308973831390576, 0.5351581303127442,
                0.45284418799773385, 0.3805410174702614)),
            "pols_active": (96.80203788661791, 0.7717569150731439, (
                0.7717569150731439, 0.6128180673191329, 0.5094267195304285,
                0.41905450345425277, 0.3383248604990171)),
            "pols_sick": (4.845465876915543, 0.04221615697124432, (
                0.010033997079952497, 0.018079315819924714, 0.0257314107823157,
                0.03378968454348107, 0.04221615697124432)),
            "premiums": (10175.364699488284, 59.82888529307967, (
                59.19761417068549, 56.055779595436185, 55.56940131828481, 54.51169319112937,
                50.22291804108328)),
            "claims_benefit": (11436.88143644897, 117.17883620598376, (
                17.59345777897606, 36.052860356616044, 57.93665854073423, 85.7517717795585,
                117.17883620598376)),
            "claims_death": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_lapse": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (777.3694574179551, 4.634416922449567, (
                4.159804487764294, 3.940886937375937, 4.08204473274845, 4.303531961590378,
                4.608637454876396)),
            "net_cf": (-2038.8861943786426, 71.56455561977688, (
                37.44435190394513, 16.062032301444205, -6.449301955197868,
                -35.54361055001951, -71.56455561977688)),
        },
        "result_pols": {
            "pols_if": (101.64750376353345, 0.7817909121530964, (
                0.7817909121530964, 0.6308973831390576, 0.5351581303127442,
                0.45284418799773385, 0.3805410174702614)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_active": (96.80203788661791, 0.7717569150731439, (
                0.7717569150731439, 0.6128180673191329, 0.5094267195304285,
                0.41905450345425277, 0.3383248604990171)),
            "pols_sick": (4.845465876915543, 0.04221615697124432, (
                0.010033997079952497, 0.018079315819924714, 0.0257314107823157,
                0.03378968454348107, 0.04221615697124432)),
            "pols_death_active": (0.0246096734919244, 0.00017027279204161492, (
                0.00010320124261263256, 0.00011507476132083102, 0.0001343458506033404,
                0.00015523229664566918, 0.00016172908816167454)),
            "pols_lapse": (0.36599907774339946, 0.003968624951954254, (
                0.003968624951954254, 0.0020807719578623193, 0.0017295839948196872,
                0.0014226042098390256, 0.0011484199841838144)),
            "pols_inception": (0.13387270704644194, 0.0009611686079594558, (
                0.0005396369388415949, 0.0006061093852050054, 0.0007341114547454559,
                0.0008725723554739887, 0.0009129404684743576)),
            "pols_recovery": (0.0894976842125633, 0.0006713700457429075, (
                0.0003159963080865923, 0.0003857016107437126, 0.0004686172666548067,
                0.0005679631555914046, 0.0006713700457429075)),
            "pols_death_sick": (0.012056610574363066, 0.0001053180545076329, (
                2.4635604385982525e-05, 4.485417217474542e-05, 6.404240968351862e-05,
                8.421867875363835e-05, 0.0001053180545076329)),
            "pols_exit": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_maturity": (0.3791255503434083, 0.3791255503434083, (
                0.0, 0.0, 0.0, 0.0, 0.3791255503434083)),
            "benefit_pp": (428126.8747857199, 2827.710861130389, (
                1815.0, 2042.7984901500004, 2299.187697718524, 2587.7560096258153,
                2827.710861130389)),
            "premium_pp": (20452.010690182877, 148.44583979730686, (
                76.70499999999998, 91.47213926094058, 109.08222750763194, 130.0825853004591,
                148.44583979730686)),
        },
    },
}
# END generated fingerprint: IP_UK_SEC


# ---------------------------------------------------------------------------
# Compiled (UKLIB-SEC-PLAN.md U2, the C step, after USLIB-SEC-PLAN.md's Phase 2)
#
# These compile the model, once a session, into a temporary directory (conftest.sec_build),
# and run the compiled package in a child process only.  They skip without modelx-cython or
# a C compiler, and the cython_uk CI job, which sets UKLIB_REQUIRE_CYTHON=1, fails a skip.
# test_compiled_conventions_uk.py checks the compiled model's types, its caches and its
# release, and compares it with modelx on the committed points; these hold what is IP's
# own: the comparison on the splice grid, at the contract's extremes, where each cap, floor
# and bound binds, the inception floor's splice among them, on every schedule a decoded
# column selects, on keys written as floats, on every committed row with the codes and the
# claim durations no swept cell reads, under the References its own rows were read from,
# and on the rows valued on an anniversary, whose increase is made at t = 0; the labels;
# the refusals and the overflows; the deepest calls on a 1 MiB stack; a Reference set
# late; and the runner.


def _as_modelx(have, want):
    """Whether a compiled value is modelx's: identical where ``exact_here()``, as on
    x86-64, and to 1e-12 relative elsewhere, as C4 compares (uk_sec_support)."""
    return have == want if exact_here() else have == pytest.approx(want, rel=1e-12, abs=0)


def _mismatch_lines(found):
    return f"{len(found)} mismatches, first:\n  " + "\n  ".join(found[:50])


# The cells C4 asks at every code, each with the names of the codes it takes, read from the
# model's own References (_code): the timings and the kinds, the claims total among them.
# The harness's, which its _ip_c4_also, the spec's c4_also, asks.  What each takes is
# derived in modelx, row by row, on every row C4 compares (_code_faults), and these must
# name exactly that (M8's review, after M14's).
CODED = _IP_CODED


def _inner_width():
    """The one inner width ``spec_sec.py`` gives the caches of ``t`` and a code."""
    source, _ = _comment("spec_sec.py")
    sizes = ast.literal_eval(source)["spaces"]["Projection"]["cells_param_size"]
    (width,) = {size[1] for name, size in sizes.items()
                if isinstance(size, tuple) and name != ("t", "z")}
    return width


def _codes_taken(proj, width):
    """``({cell: codes}, lines)``: the codes each cell of :data:`CODED` takes on point
    ``proj``, in modelx, and a line for each other raise.

    Each cell is asked every code of the caches' inner width, ``width``, in the point's
    first month on the books, and the codes it takes are those it does not refuse with
    ``invalid timing`` or ``invalid kind``.  A refused call caches nothing, so asking adds
    nothing to what a comparison holds.
    """
    taken, lines, t = {}, [], proj.t_entry()
    for cell in CODED:
        taken[cell] = set()
        for code in range(width):
            try:
                proj.cells[cell](t, code)
            except Exception as err:            # a code the cell does not take
                if not re.search(r"ValueError: invalid (timing|kind)", _raised(err)):
                    lines.append(f"point {proj.point_id()}: {cell}({t}, {code}) raised "
                                 f"{_raised(err)}")
                continue
            taken[cell].add(code)
    return taken, lines


def _code_faults(proj, width):
    """Where :data:`CODED` misnames the codes each of its cells takes on point ``proj``, in
    modelx (:func:`_codes_taken`), a line each: the codes it names, read from the point's
    References, must be exactly those, so that a cell that took a code more, or one fewer,
    parts here; and a line for each raise but a refused code."""
    taken, lines = _codes_taken(proj, width)
    for cell, names in CODED.items():
        named = {_code(proj, name) for name in names}
        if taken[cell] != named:
            lines.append(f"point {proj.point_id()}: {cell} takes {sorted(taken[cell])} in "
                         f"modelx, CODED names {sorted(named)}")
    return lines


class _Asked:
    """A stand-in for a point, which records what :func:`_ip_c4_also` asks of it: each
    cell's calls over a frame of ``months``, ``top`` claim durations, first on the books
    at ``entry``, with ``z0`` the longest opening claim duration, the codes read from the
    model's own References, ``refs``."""

    def __init__(self, months, top, entry, z0, refs):
        self.months, self.top, self.entry, self.z0 = months, top, entry, z0
        self.refs, self.asked = refs, {}
        self.cells = {name: self._cell(name) for name in ("pols_if_at", "claims",
                                                           "pols_sick_dur",
                                                           "claim_surv_step")}
        self.cells["claim_dur_live"] = self.live

    def _cell(self, name):
        return lambda *args: self.asked.setdefault(name, set()).add(args)

    def live(self, t):
        if not self.entry <= t < self.months:
            return 0
        return min(self.top, self.z0 + t - self.entry)

    def proj_len(self):
        return self.months

    def max_dur(self):
        return self.top

    def t_entry(self):
        return self.entry


class _AskedOf(_Asked):
    """:class:`_Asked` of a real point, ``proj``: its frame, its claim durations, its live
    cohorts and its References are the point's own."""

    def __init__(self, proj):
        self._proj = proj
        super().__init__(proj.proj_len(), proj.max_dur(), proj.t_entry(), None, proj.refs)

    def live(self, t):
        return self._proj.claim_dur_live(t)


# How many months squared of frames C4 compares at once.  compiled_mismatches sweeps every
# row of its case in one modelx read and keeps every value of every row, in the parent and
# in the child, until it compares them, and a row forms its cohorts on a triangle of its
# frame's months by the claim durations that can hold lives, about half its frame's square
# on new business, each a cache entry modelx keeps at about a kilobyte with the
# dependencies it records.  So memory grows with the square of the frame, not with the
# rows, and C4 compares a grid in chunks of rows whose frames' squares sum to at most this,
# the longest frame's square, 744 months, and a little more: the longest rows one or two to
# a chunk, and the committed table's in two (measured at M8).
C4_BUDGET = 800_000


def _c4_chunks(table):
    """``table``'s rows in order, in chunks whose frames' squares, ``proj_len()`` read off
    each row, sum to at most :data:`C4_BUDGET`, a row whose frame alone passes it a chunk
    of its own."""
    frames = 12 * (table["expiry_age"] - table["entry_age"]) - table["duration_mth"]
    chunks, chunk, held = [], [], 0
    for label, months in frames.items():
        cost = int(months) ** 2
        if chunk and held + cost > C4_BUDGET:
            chunks.append(table.loc[chunk])
            chunk, held = [], 0
        chunk.append(label)
        held += cost
    if chunk:
        chunks.append(table.loc[chunk])
    return chunks


def _c4(build, root, table, cohorts, refs=None, edits=None):
    """C4 on every row of ``table``, its claim cohorts ``cohorts`` and its other inputs
    changed by ``edits``, under ``refs``, chunk by chunk (:func:`_c4_chunks`), with
    :func:`_ip_c4_also`: the mismatch lines, each naming its chunk.

    Each chunk's case is asserted to hold the chunk's rows, in order, and its claim cohorts
    the chunk's, so that the rows compared are the case's, and between them the chunks
    hold every row of ``table`` once.  And on each row, in modelx, before
    :func:`_ip_c4_also` asks it, the codes each cell of :data:`CODED` takes are derived and
    held to :data:`CODED` (:func:`_code_faults`), a line for each row they part on, so that
    every code a cell takes is compared on every row C4 compares.
    """
    found, compared, width = [], [], _inner_width()
    for i, chunk in enumerate(_c4_chunks(table)):
        held = cohorts[cohorts["point_id"].isin(chunk.index)]
        folder = compiled_case(build, root / f"chunk{i}", model_points=chunk,
                               edits={**(edits or {}), COHORTS: held})
        written = pd.read_csv(folder.parent / TABLE, index_col="point_id")
        assert list(written.index) == list(chunk.index), (i, list(written.index))
        assert len(pd.read_csv(folder.parent / COHORTS)) == len(held), i
        compared += list(written.index)
        coded, asked = [], []

        def also(proj):
            coded.extend(_code_faults(proj, width))
            asked.append(proj.point_id())
            _ip_c4_also(proj)

        found += [f"chunk {i}, rows {list(chunk.index)}: {line}"
                  for line in compiled_mismatches(build, folder, refs=refs, also=also)]
        assert asked == list(chunk.index), (i, asked)
        found += [f"chunk {i}: {line}" for line in coded]
    assert compared == list(table.index), compared
    return found


def _c4_rows(labels):
    """The committed table under ``UKLIB_SEC_FULL=1``, and its rows ``labels`` otherwise."""
    rows = _committed()
    return rows if SEC_FULL else rows.loc[list(labels)]


# The committed rows a C4 comparison under References other than the shipped ones reads by
# default, by the References set: under an RPI of its own, of 5% or 12%, the row read from
# S under it (the spec's derived_refs), the anchor cell at 40 and the female cell at 30,
# whose opening state is S's under that RPI (OWN_REFS_ROWS), among the rows the RPI moves,
# the RPI rows with an anniversary in their frame (RPI_ROWS); and the rows valued on an
# anniversary with RPI escalation, whose month-0 increase the anniversary test is for.  The
# full grid compares the whole committed table under each, as the cython_uk job's Linux
# legs run it (UKLIB_SEC_FULL=1).  A compile test is never skipped, since a skip fails
# that job, so the default compares these rows rather than none; the nine RPI rows took a
# minute and a half of the default run under each RPI, every row forming its claim
# cohorts in modelx.  A test holds each selection to what modelx says of the rows
# (test_the_c4_comparisons_ask_every_code_and_their_rows).
RPI_ROWS = (1, 4, 6, 8, 9, 14, 17, 18, 19)
OWN_REFS_ROWS = {0.05: (18,), 0.12: (19,)}
ANNIVERSARY_ROWS = (8, 9)


def _ask_faults(stand_in, taken):
    """Where :func:`_ip_c4_also`, run on ``stand_in`` (:class:`_Asked`), asks other than
    every code of ``taken``, ``{cell: codes}``, in every month of the frame and the month
    after it, the cohorts outside the live ones C4 compares, and every claim duration's
    survival: a line each."""
    _ip_c4_also(stand_in)
    asked, lines = stand_in.asked, []
    frame = range(stand_in.months + 1)
    for cell in CODED:
        want = {(t, c) for t in frame for c in taken[cell]}
        if asked.get(cell) != want:
            lines.append(f"{cell}: {sorted(asked.get(cell, set()) ^ want)[:6]} asked or "
                         f"missed")
    top, entry = stand_in.top, stand_in.entry
    edges = {entry, entry + 1, stand_in.months - 1, stand_in.months} & set(frame)
    cohorts = ({(t, 0) for t in frame}
               | {(t, z) for t in edges for z in range(top + 1)}
               | {(t, stand_in.live(t) + 1) for t in frame if stand_in.live(t) + 1 <= top})
    if asked.get("pols_sick_dur") != cohorts:
        apart = sorted(asked.get("pols_sick_dur", set()) ^ cohorts)
        lines.append(f"pols_sick_dur: {apart[:6]} asked or missed")
    if asked.get("claim_surv_step") != {(z,) for z in range(1, top + 1)}:
        lines.append("claim_surv_step: not every claim duration's survival")
    return lines


def test_the_c4_comparisons_ask_every_code_and_their_rows(sec_model, spliced):
    """C4's ``also`` asks every code its cells take in every month of every row, and each
    default selection is what modelx says of the committed rows.

    Nothing in a comparison shows what it leaves out: dropped from :func:`_ip_c4_also`, a
    code is simply not compared, and dropped from a selection, a row.  So what each cell of
    :data:`CODED` takes is first derived in modelx, not read from :data:`CODED`
    (:func:`_codes_taken`): on a fresh read of the committed model, and on every row of the
    splice grid this run selects under each of its sets, the twins, the rows restated in
    force and the future rows among them, each such cell is asked every code in the caches'
    one inner width, 0 to 3, in the row's first month on the books, and the codes it takes
    are those it does not refuse, ``invalid timing`` or ``invalid kind``; :data:`CODED`
    must name exactly those, by the model's own References, row by row
    (:func:`_code_faults`), as :func:`_c4` holds on every row it compares.  Then
    :func:`_ip_c4_also` is run on a stand-in of each of those rows (:class:`_AskedOf`),
    one at a time: it must ask each cell of :data:`CODED` at every code the cell takes on
    the row, in every month of the frame and the month after it, and no other, so that a
    code left out on one kind of row fails here, where a union over the rows would pass
    it; the cohorts at claim duration 0 and at the first past the live ones in every month,
    and at every claim duration from 0 to ``max_dur()`` at the four edges of the live
    triangle; and every claim duration's survival (:func:`_ask_faults`).  The same is held
    on stand-ins of shapes no such row has (:class:`_Asked`), at the codes the committed
    rows take, one whose cohorts fill ``max_dur()`` before the frame ends among them.  It
    must be the spec's ``c4_also``, which the conventions' C4 on the committed points passes
    (``uk_sec_support.spec_c4_also``).  And each selection is derived in modelx from the
    committed points: the rows an RPI of 5% or 12% moves, whose benefit or premium in some
    month differs from the shipped RPI's, are :data:`RPI_ROWS`, and the row each was read
    for, the spec's ``derived_refs`` row, :data:`OWN_REFS_ROWS`, is one of them; and the
    rows valued on an anniversary with RPI escalation, :data:`ANNIVERSARY_ROWS`.
    """
    width = _inner_width()
    found, rows, committed_takes = [], 0, None
    fresh = mx.read_model(model_path(SEC), name=_name("codes"))
    try:
        models = [("committed", fresh)] + [(rates, spliced.pair(rates)[1])
                                           for rates in SPLICE_SETS]
        for name, model in models:
            for key in point_keys(model):
                p = projection(model, key)
                where = f"{name} row {p.point_id()}"
                taken, _ = _codes_taken(p, width)
                found += [f"{name}: {line}" for line in _code_faults(p, width)]
                found += [f"{where}: {line}" for line in _ask_faults(_AskedOf(p), taken)]
                if name == "committed":
                    if committed_takes not in (None, taken):
                        found.append(f"{where}: takes {taken}, another row "
                                     f"{committed_takes}")
                    committed_takes = taken
                rows += 1
                _release(model, key)
    finally:
        fresh.close()
    assert rows > len(_committed()) and not found, (rows, found[:10])
    refs = _references("Projection")
    for months, top, entry, z0 in ((5, 7, 0, 0), (6, 4, 2, 0), (4, 9, 0, 3), (8, 3, 0, 1)):
        lines = _ask_faults(_Asked(months, top, entry, z0, refs), committed_takes)
        assert not lines, ((months, top, entry, z0), lines)
    assert SPEC.c4_also is _ip_c4_also, SPEC.c4_also

    labels = dict(zip(sec_model.Data.model_point_table().index, point_keys(sec_model)))
    points = {label: projection(sec_model, key) for label, key in labels.items()}

    def amounts(p):
        return [(p.benefit_pp(t), p.premium_pp(t)) for t in range(p.proj_len())]

    for rpi in (0.05, 0.12):
        model = mx.read_model(model_path(SEC), name=_name("moved"))
        try:
            model.Projection.rpi_rate = rpi
            moved = sorted(label for label, key in labels.items()
                           if amounts(projection(model, key)) != amounts(points[label]))
        finally:
            model.close()
        assert moved == sorted(RPI_ROWS), (rpi, moved)
    anniversaries = sorted(label for label, p in points.items()
                           if p.is_escalating() and p.duration_mth_init() > 0
                           and p.duration_mth_init() % 12 == 0)
    assert anniversaries == sorted(ANNIVERSARY_ROWS), anniversaries
    committed = _committed()
    read_for = {refs["rpi_rate"]: (_label(committed, "derived", p, d),)
                for (p, d), refs in SPEC.derived_refs.items() if refs.keys() == {"rpi_rate"}}
    assert read_for == OWN_REFS_ROWS and len(read_for) == len(SPEC.derived_refs), read_for
    assert {label for rows in read_for.values() for label in rows} <= set(RPI_ROWS)


def _two_d_caches():
    """``{cell: (outer, width)}``: each cell of ``Projection`` whose parameters
    ``spec_sec.py`` sizes in two dimensions, the cells read from the space's own formulas,
    so that a 2-D cache added later is held with the others."""
    source, _ = _comment("spec_sec.py")
    sizes = ast.literal_eval(source)["spaces"]["Projection"]["cells_param_size"]
    formulas = (model_path(SEC) / "Projection" / "__init__.py").read_text(encoding="utf-8")
    caches = {}
    for node in ast.parse(formulas).body:
        if isinstance(node, ast.FunctionDef):
            params = tuple(arg.arg for arg in node.args.args)
            if len(params) > 1 and isinstance(sizes.get(params), tuple):
                caches[node.name] = sizes[params]
    return caches


_TWO_D = r"^  \w+(?: \w+)* ({name})\[(\d+)\]\[(\d+)\];$"


def _unpickled_through(source):
    """What the generated C ``source`` declares and its unpickle function,
    ``__pyx_unpickle__c_Projection__set_state``, does, as three dicts: each 2-D C-array
    member of the compiled ``Projection``'s struct, a cache's values or flags, by its
    declared shape, ``{member: (outer, width)}``; each member the function reads back
    through a 2-D temporary, by the length and the inner width the converter is called
    with, ``{member: (outer, width, temporary)}``; and each 2-D temporary of the function
    by its declared shape, ``{temporary: (outer, width)}``."""
    struct = re.search(r"\nstruct __pyx_obj_\w+__c_Projection \{\n(.*?)\n\};\n", source,
                       re.S)
    match = re.search(r"\nstatic PyObject \*__pyx_f_\w+___pyx_unpickle__c_Projection__set_"
                      r"state\(struct \w+ \*__pyx_v___pyx_result, PyObject \*\w+\) \{\n"
                      r"(.*?)\n\}\n", source, re.S)
    assert struct and match, "no Projection struct or unpickle function in the generated C"
    members = {name: (int(outer), int(width)) for name, outer, width in re.findall(
        _TWO_D.format(name=r"_(?:v|has)_\w+"), struct.group(1), re.M)}
    body = match.group(1)
    declared = {name: (int(outer), int(width)) for name, outer, width in re.findall(
        _TWO_D.format(name=r"__pyx_t_\d+"), body, re.M)}
    read, pending = {}, None
    for line in body.splitlines():
        call = re.search(r"__Pyx_carray_from_py_\w+?___5b_(\d+)_5d_\(\w+, (__pyx_t_\d+), "
                         r"(\d+)\)", line)
        if call:
            pending = (int(call.group(3)), int(call.group(1)), call.group(2))
            continue
        copy = re.search(r"memcpy\(&\(__pyx_v___pyx_result->(\w+)\[0\]\), (__pyx_t_\d+), ",
                         line)
        if copy and pending and copy.group(2) == pending[2]:
            read[copy.group(1)], pending = pending, None
    return members, read, declared


def _unpickle_faults(source, caches):
    """Where the generated C ``source`` reads a 2-D cache back other than through a
    temporary of its own shape as a point is unpickled, a line each
    (:func:`_unpickled_through`): every 2-D member of the compiled ``Projection``, and the
    values and flags of each cache of ``caches``, ``{cell: (outer, width)}``, at that
    shape, must be read through a temporary declared with the member's own outer size and
    inner width, by a converter of that width called with that length, and no temporary
    may serve two shapes."""
    members, read, declared = _unpickled_through(source)
    found, temporaries = [], {}
    for cell, shape in caches.items():
        for member in (f"_v_{cell}", f"_has_{cell}"):
            if members.get(member) != shape:
                found.append(f"{member}: declared {members.get(member)}, where "
                             f"spec_sec.py sizes {cell} {shape}")
    for member, shape in sorted(members.items()):
        if member not in read:
            found.append(f"{member}: read back through no 2-D temporary")
            continue
        length, inner, temporary = read[member]
        temporaries.setdefault(shape, set()).add(temporary)
        if (length, inner) != shape or declared.get(temporary) != shape:
            found.append(f"{member}, a {shape[0]} by {shape[1]} cache: read with a "
                         f"converter of width {inner} and length {length} through "
                         f"{temporary}, declared {declared.get(temporary)}")
    found += [f"{a} and {b} share a temporary" for a, ta in temporaries.items()
              for b, tb in temporaries.items() if a < b and ta & tb]
    return found


@pytest.mark.cython
def test_each_2d_cache_is_unpickled_through_a_temporary_of_its_shape(sec_build):
    """As a compiled point is unpickled, each 2-D cache is read back through a temporary
    of its own shape (M8's review).

    Cython's unpickle code reads each C-array cache back through a temporary, with a
    converter named by the inner type, and pools its temporaries by C type, its C-array
    types comparing equal on the outer size and the element type, the inner size not
    compared: so the caches of one outer size share a temporary of the first one's shape
    for their values, and another for their flags (``spec_sec.py``).  That is why the
    cohorts' cache takes an outer size of its own, 747 by 626, beside the timings' and
    kinds' 746 by 4.  Were the two outer sizes one, the cohorts would be read into a
    temporary of 746 by 4: gcc and clang refuse the build under
    ``-Werror=incompatible-pointer-types``, which the library's ``build_sec_cy.py`` passes
    on Linux and macOS, and the spec test holds the sizes, but MSVC, on the ``cython_uk``
    job's Windows legs, only warns, and the build would write 746 x 626 doubles into it.
    So this reads the generated C, which Cython writes alike for every compiler: in
    ``__pyx_unpickle__c_Projection__set_state``, every 2-D member of the compiled
    ``Projection``'s struct, values and flags, the caches ``spec_sec.py`` sizes in two
    dimensions among them, at its sizes (:func:`_two_d_caches`), is read through a 2-D
    temporary declared with the member's own shape, by a converter of that width called
    with that length (:func:`_unpickle_faults`), so that a 2-D cache added later is held
    too.  A layout this cannot read fails here, rather than passing unread.
    """
    build = sec_build(SEC)
    caches = _two_d_caches()
    assert set(caches) >= {"pols_if_at", "claims", "pols_sick_dur"}, caches
    source = (build.package / "_mx_classes.c").read_text(encoding="utf-8", errors="replace")
    found = _unpickle_faults(source, caches)
    assert not found, found


@pytest.mark.cython
@pytest.mark.parametrize("rates", list(SPLICE_SETS))
def test_the_compiled_model_computes_what_modelx_computes_on_the_splice_grid(
        spliced, sec_build, tmp_path, rates):
    """C4 on the branches: compiled, every cell of the splice grid is modelx's.

    The sample traces the committed points alone, and they leave branches untaken, which
    are typed all the same, because every branch of a cell returns the one type the others
    return (sample_sec.py).  What the compiled model computes on them is held here: the
    splice grid's rows of each set of References (:data:`SPLICE_SETS`), S's points and its
    three variants restated in force at T2's months and issued later, the claims on both
    bases, the youngest and the oldest issue ages and the escalation cap's and floor's
    rows and the recovery bound's among them, under the set's References, each row with
    the claim cohorts the generator read for it.  The grid is the one this run's
    ``spliced`` selects, the core by default and the full grid under ``UKLIB_SEC_FULL=1``,
    and the test carries no ``sec_full`` mark, since a skipped compile test fails the
    cython_uk job.  The set's rows go beside the build in chunks sized by their frames
    (:func:`_c4`), modelx sweeps every point fully, with :func:`_ip_c4_also`, and the
    compiled model must agree at every argument modelx caches, identically on x86-64 and to
    1e-12 relative elsewhere, with every raise and every ``Data`` array
    (``uk_sec_support.compiled_mismatches``).
    """
    build = sec_build(SEC)
    folder = spliced.pair(rates)[1].Data.input_dir()
    table = pd.read_csv(folder / TABLE, index_col="point_id")
    cohorts = pd.read_csv(folder / COHORTS)
    assert len(table) > 0, rates
    found = _c4(build, tmp_path, table, cohorts, refs=SPLICE_SETS[rates])
    assert not found, _mismatch_lines(found)


# The contract's extremes (held by proj_len()), as (the S point it changes, its changes):
# the anchor cell issued at the youngest issue age, 18, to the latest expiry, 70, 624
# months, on the active-lives basis and on the exit basis; the female cell issued at the
# oldest issue age, 59, to 70, and at 18 to the earliest expiry, 50; and the claim from
# duration 0 on the exit basis and on the active-lives basis, which S opens in claim at 19,
# its twin issued at 18, a year before the valuation date, to 70.
EXTREMES = {
    21: (1, {"entry_age": 18, "expiry_age": 70}),
    22: (1, {"entry_age": 18, "expiry_age": 70, "recovery_basis": "exit"}),
    23: (4, {"entry_age": 59, "expiry_age": 70}),
    24: (4, {"entry_age": 18, "expiry_age": 50}),
    25: (2, {"entry_age": 19, "expiry_age": 70}),
    26: (7, {"entry_age": 19, "expiry_age": 70}),
}


def _contract_extremes(tmp_path):
    """The rows at the contract's extremes, built by the generator, and their claim
    cohorts.

    Each of :data:`EXTREMES` in a copy of S's table, read at the shipped References with
    an RPI of 5%, so that the lapse shock reads the RPI every month: its twin; the
    healthy shapes issued ``future_horizon_mth``, 120 months, after the valuation date,
    the anchor cell's a frame of 744 months; and the anchor cell's and the claim's rows
    restated in force in the last month of S's frame, opened with S's state there.  So
    ``t`` reaches 745, the roll-forward's month after the month after the longest frame,
    the claim durations 625, the longest cover and one, and every code its last, the
    furthest ``spec_sec.py`` sizes for.  Returns ``(rows, cohorts)``.
    """
    s_table = _s_table()
    rows = []
    for point_id, (base, changes) in EXTREMES.items():
        row = s_table.loc[[base]].assign(**changes, policy_id=f"IP-7000{point_id}")
        row.index = pd.Index([point_id], name="point_id")
        rows.append(row)
    s = mx.read_model(temp_inputs(tmp_path, model_path(TWIN), model_points=pd.concat(rows)),
                      name=_name("extremes_s"))
    try:
        s.Projection.rpi_rate = 0.05
        derived = tuple((p, _point(s, p).proj_len() - 1) for p in (21, 25))
        spec = dataclasses.replace(SPEC, derived=derived,
                                   future=tuple((p, 120) for p in (21, 22, 23, 24)),
                                   derived_refs={})
        table, companions = build_sec_table(spec, s)
    finally:
        s.close()
    return table.set_index("point_id"), companions[COHORTS]


@pytest.mark.cython
def test_the_compiled_model_computes_what_modelx_computes_at_the_contract_extremes(
        sec_build, tmp_path):
    """C4 where the caches end: the contract's longest covers, every cell compiled.

    The rows of :func:`_contract_extremes`, each shape at its longest cover from the
    youngest issue age, issued now and 120 months on and in force in its last month, the
    oldest issue age and the earliest expiry, at an RPI of 5%, read every cache as far as
    ``spec_sec.py`` sizes it for: ``t`` to 745, the roll-forward's month after the month
    after the 744-month frame; the claim durations to 625, a cohort a month for the
    longest cover and one, the cohorts' cache to its last month and claim duration; and
    every timing and kind.  modelx sweeps every row fully, with :func:`_ip_c4_also`, and
    the compiled model must agree everywhere.  A cache one too small for the contract
    raises ``IndexError`` compiled where modelx reads on, and fails here, though the spec
    check passes it, which holds the caches to the spec and not the spec to the contract.
    """
    build = sec_build(SEC)
    rows, cohorts = _contract_extremes(tmp_path / "s")
    frames = 12 * (rows["expiry_age"] - rows["entry_age"]) - rows["duration_mth"]
    covers = 12 * (rows["expiry_age"] - rows["entry_age"])
    assert (frames.max(), covers.max()) == (744, 624), (frames.max(), covers.max())
    assert {18, 59} <= set(rows["entry_age"]) and {50, 70} <= set(rows["expiry_age"])
    found = _c4(build, tmp_path / "extremes", rows, cohorts, refs={"rpi_rate": 0.05})
    assert not found, _mismatch_lines(found)


def _floor_rows(tmp_path):
    """The inception floor's splice rows (:data:`FLOOR_INCEPTION`): variant 9's twin and
    its rows restated at :data:`FLOOR_MTHS`, built from S under :data:`MAIN`, and their
    claim cohorts."""
    s = mx.read_model(temp_inputs(tmp_path, model_path(TWIN),
                                  model_points=_s_table_with_variants((9,)),
                                  edits=FLOOR_INCEPTION), name=_name("floor_rows_s"))
    try:
        for ref, value in MAIN.items():
            setattr(s.Projection, ref, value)
        spec = dataclasses.replace(SPEC, derived=tuple((9, d) for d in FLOOR_MTHS),
                                   future=(), derived_refs={})
        table, companions = build_sec_table(spec, s)
    finally:
        s.close()
    return table.set_index("point_id"), companions[COHORTS]


# Where each cap, floor and bound binds, as (case, the References, the committed rows it is
# compared on by default, the cell and the value it binds at): on the older male cell's
# rows, its twin, 120 months, and its row at 118, its frame's last two months, RPI rows
# active and claiming, the shortest of S's points' that reach each bound, the mortality
# cap, min(q, 1.0), at 61; the lapse rate's bound at 1, min(1.0, w), from the first
# anniversary; the escalation cap and the RPI's floor at 0, every year; and the recovery
# rate's bound at 1, min(1.0, rho), on every claim in its first year; on the female
# cell's twin and its row at 30, the inception cap at 54; and the inception rate's floor at
# 0, max(0.0, r), on its splice's rows, in a copy of the inception table that falls below 0
# (_floor_rows).
BINDS = [
    ("the mortality cap", {"mort_active_factor": 100.0}, (6, 15), "mort_rate", 1.0),
    ("the inception cap", {"cycle_factor": 50.0}, (4, 19), "inception_rate", 1.0),
    ("the lapse rate's bound", {"rpi_rate": 0.12, "esc_lapse_slope": 300.0}, (6, 15),
     "lapse_rate", 1.0),
    ("the escalation cap", {"rpi_rate": 0.12}, (6, 15), "esc_rate", 0.1),
    ("the RPI's floor", {"rpi_rate": -0.02}, (6, 15), "esc_rate", 0.0),
    ("the recovery bound", {"cycle_factor": 0.35}, (6, 15), "rec_rate", 1.0),
    ("the inception floor", MAIN, None, "inception_rate", 0.0),
]


@pytest.mark.cython
@pytest.mark.parametrize("case, refs, labels, cell, value", BINDS, ids=[c[0] for c in BINDS])
def test_the_compiled_model_computes_what_modelx_computes_where_each_cap_binds(
        sec_build, tmp_path, case, refs, labels, cell, value):
    """C4 where each cap, floor and bound binds: compiled, every cell is modelx's.

    The splice grid and the committed points leave each bound's binding side mostly
    untaken: the caps on mortality and inception bind only under References the product
    does not ship, the lapse rate's bound only under a shock, the escalation's cap and floor
    not at the shipped 3%, the recovery bound only under an overlay below 0.4, and the
    inception floor on no shipped schedule.  So each case of :data:`BINDS` is first
    asserted to bind in modelx, on each of its rows, under its References: the rate the
    case names at its bound in some month, or at claim duration 1, before the
    comparison's own read; then modelx sweeps the rows fully under the same References,
    with :func:`_ip_c4_also`, and the compiled model must agree at every argument modelx
    caches, identically on x86-64 and to 1e-12 relative elsewhere.  No other compiled test
    reaches these sides of the ``min`` and the ``max``.  By default each case's committed
    rows, a twin and a row in force of one S point, and the whole committed table with the
    full grid; the floor on its splice's rows, variant 9's twin and its rows at 1, 12 and
    95, in the copy of the inception table whose schedule falls below 0.
    """
    build = sec_build(SEC)
    edits = None
    if labels is None:
        rows, cohorts = _floor_rows(tmp_path / "s")
        edits = FLOOR_INCEPTION
    else:
        rows, cohorts = _c4_rows(labels), _committed_cohorts()
        cohorts = cohorts[cohorts["point_id"].isin(rows.index)]
    model = mx.read_model(_sec_inputs(tmp_path / "check", rows, cohorts, edits=edits),
                          name=_name("binds"))
    try:
        for ref, val in refs.items():
            setattr(model.Projection, ref, val)
        bound = []
        for key, label in zip(point_keys(model), model.Data.model_point_table().index):
            p = projection(model, key)
            if labels is not None and label not in labels:
                continue
            if cell == "rec_rate":
                bound.append(p.rec_rate(1) == value)
            elif cell == "esc_rate":
                bound.append(p.esc_rate() == value)
            else:
                bound.append(any(p.cells[cell](t) == value for t in range(p.proj_len())))
    finally:
        model.close()
    assert bound and all(bound), (case, bound)
    found = _c4(build, tmp_path / "binds", rows, cohorts, refs=refs, edits=edits)
    assert not found, _mismatch_lines(found)


@pytest.mark.cython
def test_the_compiled_model_computes_what_modelx_computes_on_every_schedule(sec_build,
                                                                             tmp_path):
    """C4 on every schedule a decoded column selects: compiled, every cell is modelx's.

    A point of each of the forty inception schedules, sex by occupation class by deferred
    period, issued at the oldest issue age, 59, to expire at 60, a year of cover each, so
    that each reads its own row of the inception array and its sex's row of the mortality
    array (:func:`_schedule_rows`), goes beside the build: modelx sweeps them fully, and
    the compiled model must agree everywhere, each decode's code and the rows it selects
    among them, and ``Data``'s arrays whole, every schedule at every age, which the
    committed points reach only in part: no committed point is a woman in class 1.  The
    committed rows hold each value of the other decoded columns, the escalation, the
    recovery basis and the status, which C4 on them compares.
    """
    build = sec_build(SEC)
    rows = _schedule_rows(_committed(), 1, "IP-8").assign(entry_age=59, expiry_age=60)
    found = _c4(build, tmp_path / "schedules", rows, _committed_cohorts().iloc[0:0])
    assert not found, _mismatch_lines(found)


@pytest.mark.cython
def test_the_compiled_model_returns_each_label_as_modelx_does(sec_build, tmp_path):
    """The labels, compiled, are modelx's: their text on every committed and decoded point.

    The five labels are reporting cells, which no projection cell calls, so C4's sweep
    compares them only as cells without parameters; this calls each on every point, in
    modelx and compiled (``uk_sec_support.label_mismatches``), on the committed table and
    on a point of each of the forty schedules (:func:`_schedule_rows`), which between them
    carry every value of every labelled column: each must be the same text in both
    engines.  A label refuses what is not its column's codes, in either engine
    (:func:`test_each_label_refuses_a_value_that_is_not_its_codes`), so each compiles to
    ``str``, which C3 admits of a refusing label.
    """
    build = sec_build(SEC)
    labels = list(LABEL_REFUSALS)
    schedules = _schedule_rows(_committed(), 1, "IP-8")
    for name, rows, edits in (("committed", None, None),
                              ("schedules", schedules,
                               {COHORTS: _committed_cohorts().iloc[0:0]})):
        folder = compiled_case(build, tmp_path / name, model_points=rows, edits=edits)
        want, found = label_mismatches(build, folder, labels)
        assert not found, (name, found)
        values = {label: {v[1] for point in want.values() for lab, v in point.items()
                          if lab == label} for label in labels}
        assert all(isinstance(v, str) for vs in values.values() for v in vs), values
        if name == "committed":
            assert values == {"sex": {"M", "F"}, "escalation": {"RPI", "none"},
                              "premium_basis": {"guaranteed"},
                              "status": {"active", "in_claim"},
                              "recovery_basis": {"return_to_h", "exit"}}, values


# The model point table's columns that hold whole numbers, which a spreadsheet may save as
# floats: the ages, the class, the deferred period and the months; and the claim cohorts'
# keys and the assumption tables' keys.
FLOAT_COLUMNS = ("entry_age", "occ_class", "deferred_weeks", "expiry_age", "duration_mth")
FLOAT_KEYS = {
    MORT: lambda t: t.assign(age=t["age"].astype(float)),
    LAPSE: lambda t: t.assign(policy_year=t["policy_year"].astype(float)),
    TERM: lambda t: t.assign(claim_duration_year=t["claim_duration_year"].astype(float)),
    INCEPTION: lambda t: t.assign(**{c: t[c].astype(float)
                                     for c in ("occ_class", "deferred_weeks", "age")}),
}


@pytest.mark.cython
def test_the_compiled_model_reads_keys_written_as_floats_as_modelx_does(sec_build,
                                                                         tmp_path):
    """C4 on keys written as floats: the compiled model reads 300.0 as 300, as modelx does.

    The committed table with its labels written ``1.0`` to ``19.0`` and its whole numbers
    as floats (:data:`FLOAT_COLUMNS`), the claim cohorts' point and claim duration as
    floats, and the four assumption tables' keys as floats (:data:`FLOAT_KEYS`).  ``Data``
    reads each by value, so first, in seconds, modelx's ``Data`` on the floats is held to
    its ``Data`` on the same rows and cohorts written with their ints, by the same writer
    (``uk_sec_support.temp_inputs``), whose text for a share reads back the same double
    either way, if not always the committed text's: every array of the same dtype and
    values, and every extent of the same type, so that a key read as a float fails here,
    naming its cell, and not in the compiled sweep.  Then modelx sweeps the core's points by
    default (:data:`CORE_POINTS`) and every point with the full grid, with
    :func:`_ip_c4_also`, and the compiled model must agree everywhere, every ``Data`` array
    included, in dtype and shape: the arrays are the whole table's either way.
    """
    build = sec_build(SEC)
    rows, cohorts = _committed(), _committed_cohorts()
    as_written = mx.read_model(_sec_inputs(tmp_path / "ints", rows, cohorts),
                               name=_name("ints"))
    floats = rows.assign(**{c: rows[c].astype(float) for c in FLOAT_COLUMNS})
    floats.index = pd.Index(rows.index.astype(float), name="point_id")
    float_cohorts = cohorts.assign(point_id=cohorts["point_id"].astype(float),
                                   z=cohorts["z"].astype(float))
    folder = _sec_inputs(tmp_path / "floats", floats, float_cohorts, edits=FLOAT_KEYS)
    written = pd.read_csv(folder.parent / TABLE)
    assert all(written[c].dtype == float for c in ("point_id", *FLOAT_COLUMNS))
    assert pd.read_csv(folder.parent / COHORTS)["z"].dtype == float
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
    chosen = floats if SEC_FULL else floats.loc[[float(p) for p in CORE_POINTS]]
    found = _c4(build, tmp_path / "c4", chosen, float_cohorts, edits=FLOAT_KEYS)
    assert not found, _mismatch_lines(found)


@pytest.mark.cython
def test_the_compiled_model_computes_what_modelx_computes_on_every_committed_row(
        sec_build, tmp_path):
    """C4 on every committed row, with the codes and claim durations no swept cell reads.

    ``test_compiled_conventions_uk.py`` compares the committed points as the harness sweeps
    every model's; this compares them with :func:`_ip_c4_also` beside the sweep: the twins
    of S's claims in payment, on both bases, the rows restated in force, the two rows read
    under References of their own, each with the claim cohorts the companion holds for it,
    and the row issued 13 months on, each at every timing, every kind, every claim
    duration's survival and the cohorts at the edges of its live triangle, which no swept
    cell reads.
    """
    build = sec_build(SEC)
    found = _c4(build, tmp_path, _committed(), _committed_cohorts())
    assert not found, _mismatch_lines(found)


@pytest.mark.cython
@pytest.mark.parametrize("refs", list(SPEC.derived_refs.values()),
                         ids=[f"{k}={v}" for refs in SPEC.derived_refs.values()
                              for k, v in refs.items()])
def test_the_compiled_model_computes_what_modelx_computes_under_a_row_s_own_references(
        sec_build, tmp_path, refs):
    """C4 on the committed table under the References each of its own rows was read from.

    Two committed rows were read from S under References of their own (the spec's
    ``derived_refs``): the anchor cell at 40 under an RPI of 5%, and the female cell at 30
    under one of 12%, where the escalation cap binds.  C4 on the committed points compares
    them at the shipped References; under their own, set on the compiled model as on modelx
    before either computes, each continues S's path, which other rows' References leave
    untaken: so the row read under each set (:data:`OWN_REFS_ROWS`), and the whole
    committed table with the full grid, every row the RPI moves among it
    (:data:`RPI_ROWS`), are swept fully under it, and the compiled model must agree
    everywhere.
    """
    build = sec_build(SEC)
    found = _c4(build, tmp_path, _c4_rows(OWN_REFS_ROWS[refs["rpi_rate"]]),
                _committed_cohorts(), refs=refs)
    assert not found, _mismatch_lines(found)


# The References under which the anniversary rows' month-0 increase is not the one the
# rows were read with: an RPI of 8%.
ANNIVERSARY_REFS = {"rpi_rate": 0.08}


@pytest.mark.cython
def test_the_compiled_model_computes_what_modelx_computes_on_an_anniversary(sec_build,
                                                                             tmp_path):
    """C4 on the rows valued on an anniversary, whose increase is made at ``t = 0``.

    The owner's decision (D6): an anniversary at the valuation date is the projection's
    first event, made at today's References, the benefit and premium columns holding the
    year it closes.  Two committed rows with RPI escalation are valued on an anniversary,
    the anchor cell at 12 and at 60 months (:data:`ANNIVERSARY_ROWS`).  In modelx, under
    :data:`ANNIVERSARY_REFS`, each steps its benefit and its premium at ``t = 0``, from its
    columns, at today's rate, which is asserted: ``benefit_pp(0)`` is
    ``benefit_pp_init()`` times ``1 + esc_rate()``, above the column.  Then the two rows,
    the whole committed table with the full grid, are swept fully under those References,
    and the compiled model must agree everywhere, the month-0 step and every year's after
    it among it.
    """
    build = sec_build(SEC)
    model = mx.read_model(model_path(SEC), name=_name("anniversary"))
    try:
        for ref, value in ANNIVERSARY_REFS.items():
            setattr(model.Projection, ref, value)
        for label in ANNIVERSARY_ROWS:
            p = _point(model, label)
            assert p.duration_mth_init() % 12 == 0 and p.duration_init() == (
                p.duration_mth_init() // 12 - 1)
            step = 1.0 + p.esc_rate()
            assert p.benefit_pp(0) == p.benefit_pp_init() * step > p.benefit_pp_init()
            assert p.premium_pp(0) == p.premium_pp_init() * (
                1.0 + p.esc_rate() * model.Projection.esc_prem_mult)
    finally:
        model.close()
    found = _c4(build, tmp_path, _c4_rows(ANNIVERSARY_ROWS), _committed_cohorts(),
                refs=ANNIVERSARY_REFS)
    assert not found, _mismatch_lines(found)


# The compiled refusals' child: one process, which imports the compiled package once and
# runs each case on a fresh instance of the model, whose Data reads the case's own copies
# of the six files by absolute path.  A refusal names a file by its Reference, so the
# child's names the path, and the test writes each path as the file's name (_named), as
# modelx, reading the files by name, writes it.  It sets every space's References that a
# case gives, Data's named "Data.<name>" and Projection's by name (UKLIB-SEC-PLAN.md §6.2,
# *Record -- M4*, *Carried into M6 and after*; §6.4, *Carried into M8 and M14*).
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
CASE_FILES = {"model_point_file": TABLE, "inforce_cohorts_file": COHORTS,
              "inception_file": INCEPTION, "termination_file": TERM,
              "mort_table_file": MORT, "lapse_table_file": LAPSE}

# The array each assumption table is read into, which the refusal test reads beside the
# cell that checks the table.
ARRAYS = {MORT: "mort_table_array", LAPSE: "lapse_rate_array", TERM: "recovery_rate_array",
          INCEPTION: "inception_array"}


def _named(outcome, files):
    """A compiled outcome with each of a case's ``files``, ``{Reference: absolute path}``,
    written as the file's name in its message, as modelx's ``Data`` names it."""
    if outcome[0] != "raised":
        return outcome
    text = outcome[1]
    for path in files.values():
        text = text.replace(path, pathlib.Path(path).name)
    return ("raised", text)


def _set_refs(model, refs):
    """Set each of ``refs`` on ``model``: ``"Data.<name>"`` on its ``Data``, any other on
    its ``Projection``.  Every Reference with a domain is a float, the contract's four ages
    and ``Data``'s horizon and interpolated ages among them, so the compiled model holds
    each as modelx does, a fraction as the fraction."""
    for ref, value in refs.items():
        if ref.startswith("Data."):
            setattr(model.Data, ref[len("Data."):], value)
        else:
            setattr(model.Projection, ref, value)


# Data's References with a domain, each refused off it in both engines, message for
# message, each a float, so that a fraction is the fraction compiled too: the horizon at
# -1, 12.5 and 2**53, and the inception array's ages, a fraction and a last age below the
# first.  And the inception array's first age raised to 36, past the anchor cell's issue
# age, which inception_rate refuses, naming the point and the age.
DATA_REFUSALS = [
    *((f"future_horizon_mth at {h!r}", {"Data.future_horizon_mth": h})
      for h in (-1.0, 12.5, 2.0 ** 53)),
    ("rate_age_min at 18.5", {"Data.rate_age_min": 18.5}),
    ("rate_age_max below rate_age_min", {"Data.rate_age_max": 17.0}),
    ("rate_age_min past the anchor cell's issue age", {"Data.rate_age_min": 36.0}),
]

# Projection's idx past the extract's last row, 19, and -1, beside the last row, 18, as
# (position, cell, arguments): past the last row the first read of a vector raises
# IndexError in both engines, each in its own words, and -1 reads every vector at its last
# element in both, so it is the last point, under that point's own point_id.
IDX_CASE = "an idx past the table and one before it"
IDX_EDGES = [(19, "point_id", ()), (19, "result_cf", ()), (-1, "point_id", ()),
             (-1, "proj_len", ()), (-1, "net_cf", (0,)), (-1, "pols_sick_dur", (0, 30)),
             (18, "point_id", ()), (18, "proj_len", ()), (18, "net_cf", (0,)),
             (18, "pols_sick_dur", (0, 30))]

# Calls past the caches spec_sec.py sizes, which raise IndexError in the compiled model
# alone, as (call, arguments, what modelx does), on the extract's first row, point 1, the
# anchor cell issued at the valuation date: a month either side of the t cache, which
# modelx answers with 0.0, the month outside cover; a timing and a kind past the one inner
# width, which modelx refuses as codes it does not take; a claim duration either side of
# the z cache, whose year modelx computes as it computes any; and a month and a claim
# duration either side of the cohorts' cache, a cohort modelx answers with 0.0, outside
# cover or past max_dur().
COMPILED_ONLY = [
    ("net_cf", (746,), ("ok", 0.0)), ("net_cf", (-1,), ("ok", 0.0)),
    ("pols_if_at", (0, 4), ("raised", "ValueError: invalid timing")),
    ("claims", (0, 4), ("raised", "ValueError: invalid kind")),
    ("claim_dur_year", (626,), ("ok", 53)), ("claim_dur_year", (-1,), ("ok", 0)),
    ("pols_sick_dur", (747, 1), ("ok", 0.0)), ("pols_sick_dur", (-1, 1), ("ok", 0.0)),
    ("pols_sick_dur", (0, 626), ("ok", 0.0)), ("pols_sick_dur", (0, -1), ("ok", 0.0)),
]


def _refusal_cases():
    """Every refusal the compiled model must make as modelx does, as (case, the table, the
    claim cohorts, the other edits, the References, [(position, cell, arguments)], the
    Data cells to read, whether each refusal names its point).

    Each table is an extract, labelled otherwise than by position (:data:`EXTRACT_LABELS`,
    the generator's columns kept), with its claim cohorts relabelled alike, so that a
    refusal naming a point by ``idx + 1`` names another; a case that edits the committed
    table or cohorts edits them first, by their own labels, and they are then relabelled.
    A position, not a label, since a table ``Data`` refuses has no keys to give: each is
    the row's place in the table written, ``Projection``'s ``idx``, which the test indexes
    ``Projection`` by in modelx too.  The refusals of a point's own, by its frame, its
    References, its history, a value past the floats or a rate its tables do not hold,
    each name the point, and must name it by the extract's label (M8's review).
    """
    committed, held = _committed(), _committed_cohorts()
    relabel = _relabel_map()

    def extract(edit=None):
        table = edit(committed) if edit is not None else committed
        return table.rename(index=relabel)

    def cohorts(edit=None):
        table = edit(held) if edit is not None else held
        if "point_id" not in table.columns:
            return table
        return table.assign(point_id=[relabel.get(p, p) for p in table["point_id"]])

    def at(point):
        return list(committed.index).index(point)

    cases = []
    for case, edit, _ in MALFORMED:
        cases.append((case, extract(edit), cohorts(), None, {}, [(0, "result_cf", ())],
                      ("model_point_table",), False))
    for value in FLAG_WRITINGS:
        cases.append((f"the escalation written {value!r}",
                      extract(_set("escalation", [1], value)), cohorts(), None, {},
                      [(at(1), "result_cf", ()), (at(1), "is_escalating", ())],
                      ("model_point_table", "escalation_rpi"), False))
    for case, edit, _ in MALFORMED_COHORTS:
        cases.append((f"cohorts: {case}", extract(), cohorts(edit), None, {},
                      [(at(9), "result_cf", ())], ("inforce_cohorts",), False))
    for case, file, edit, _ in UNREADABLE:
        cases.append((case, extract(), cohorts(), {file: edit}, {},
                      [(at(9), "result_cf", ())], (CHECKED_BY[file], ARRAYS[file]), False))
    for case, edit, refs, point, _, _ in NOT_ISSUED:
        cases.append((case, extract(edit), cohorts(), None, refs,
                      [(at(point), cell, ()) for cell in ("result_cf", "proj_len")], (),
                      True))
    for case, refs, point, message, _ in DOMAINS:
        if message is not None:
            cases.append((f"domain {case}", extract(), cohorts(), None, refs,
                          [(at(point), "result_cf", ()), (at(point), "proj_len", ())], (),
                          True))
    for case, amounts, refs, message in HISTORY_BOUNDS:
        if message is not None:
            edit = _then(_set("benefit_pp_init", [9], amounts[0]),
                         _set("premium_pp_init", [9], amounts[1]))
            cases.append((f"history: {case}", extract(edit), cohorts(), None, refs,
                          [(at(9), "result_cf", ()), (at(9), "proj_len", ())], (), True))
    for case, edit, refs, point, call, report, _ in PAST_THE_FLOATS:
        name, *args = call
        args = tuple(_codes_of(args))
        calls = [(at(point), name, args), (at(point), report, ())]
        if args and args[0] > 0:
            calls.insert(0, (at(point), name, (args[0] - 1, *args[1:])))
        cases.append((f"past the floats: {case}", extract(edit),
                      cohorts(getattr(edit, "cohorts", None)), None, refs, calls, (), True))
    cut = {MORT: _dropped(lambda t: (t["age"] < 40).to_numpy())}
    cases.append(("an age below the mortality table", extract(), cohorts(), cut, {},
                  [(at(1), "result_cf", ()), (at(1), "mort_rate", (0,))], (), True))
    for case, refs in DATA_REFUSALS:
        cases.append((case, extract(), cohorts(), None, refs,
                      [(at(1), "result_cf", ()), (at(1), "inception_rate", (0,))],
                      ("model_point_table",) if "horizon" in case else (),
                      "issue age" in case))
    for case, edit, cell, args, _ in NOT_HELD:
        if edit is not None:
            cases.append((case, edit(committed), held, None, {}, [(2, cell, args)],
                          ("point_id",), False))
    return cases


def _codes_of(args):
    """``args`` with each text that names a code of the model as that code, read from the
    model's own References."""
    refs = _references("Projection")
    return tuple(refs[a] if isinstance(a, str) else a for a in args)


@pytest.mark.cython
def test_the_compiled_model_refuses_what_modelx_refuses(sec_build, tmp_path):
    """Compiled, the model refuses what modelx refuses, with modelx's error and message.

    A ``ValueError`` raised in a cell typed ``long long`` or ``double`` propagates out of
    the compiled model as out of modelx.  So, each on its own inputs and References
    (:func:`_refusal_cases`), on an extract labelled otherwise than by position, its claim
    cohorts relabelled alike: every case of :data:`MALFORMED`, refused by a projection and
    by ``Data``'s reader, the ``2**53`` bounds among them, and every writing of the
    escalation flag of :data:`FLAG_WRITINGS`, by a projection, by the flag's cell and by
    ``Data``'s decode; every case of :data:`MALFORMED_COHORTS`, by a projection of the
    anchor cell in force and by the companion's reader; every case of :data:`UNREADABLE`,
    by a projection, by the ``Data`` cell that checks the table and by the table's array,
    so that a compiled ``Data`` cell refuses each value its modelx cell refuses; every case
    of :data:`NOT_ISSUED`, by ``result_cf`` and ``proj_len``, the contract moved past the
    caches among them, ``Data``'s horizon set by the child as every space's References are;
    every case of :data:`DOMAINS` that refuses, each Reference printed as the compiled
    model types it; every history of :data:`HISTORY_BOUNDS` that is refused, the one whose
    premium's least and most leave the floats, reaching the two powers' guards in the
    ``except`` that reads them as the cap's path, among them; each value of
    :data:`PAST_THE_FLOATS`, by its cell, the month before it computing, and by a report, a
    kind named by its code, the benefit's, the premium's, the inflation's and the discount
    factor's powers among them, where the compiled cell calls Python's own power where C's
    gives an infinity, uslib's M22 form, so that it refuses as modelx does where it would
    carry an infinity on; an attained age below a mortality table cut at 40; ``Data``'s
    References off their domains (:data:`DATA_REFUSALS`); and a label the vectors cannot
    hold, by ``Data.point_id``.

    And the refusals that are the compiled model's alone (:data:`COMPILED_ONLY`): a month
    past the ``t`` cache either side, a timing and a kind past their codes, a claim
    duration past the ``z`` cache either side, and a month and a claim duration past the
    cohorts' cache either side, each raising ``IndexError`` compiled, beside what modelx
    does.  And ``Projection``'s ``idx`` at the table's edges (:data:`IDX_EDGES`): one past
    the last row raises ``IndexError`` in both engines, compared by its type, the words
    being each engine's own, and ``-1`` is the last row in both, its every outcome the last
    row's and modelx's, its cohorts among them, which a build without bounds checks, or
    without Python's negative indices, would part from.

    The compiled model runs every case in one child, each on a fresh instance of the model
    that reads the case's own copies of the six files by absolute path
    (:data:`REFUSALS_CHILD`), each path in a message written as the file's name, as modelx
    names it (:func:`_named`), and modelx reads each case afresh.  Engines agreeing is not
    enough where both name a point by its place: so each refusal of a point's own, by its
    frame, a Reference, its history, a value past the floats or a rate its tables do not
    hold, must begin ``ValueError: point_id <label>:``, the extract's label of its row, in
    both engines, and the refusals that do are counted, every such case's but the month
    before a value past the floats, which computes (M8's review).
    """
    build = sec_build(SEC)
    cases = _refusal_cases()
    plain = len(cases)
    relabelled = _extract_with_generated()
    cases.append(("compiled only", relabelled, _extract_cohorts(), None, {},
                  [(0, cell, args) for cell, args, _ in COMPILED_ONLY], (), False))
    assert len(relabelled) == 19
    cases.append((IDX_CASE, relabelled, _extract_cohorts(), None, {}, IDX_EDGES, (), False))
    root = tmp_path / "refused"
    compiled_case(build, root / "base")
    jobs, wants = [], []
    for i, (case, table, cohorts, edits, refs, calls, data, _) in enumerate(cases):
        folder = temp_inputs(root / f"case{i:03d}", model_path(SEC), model_points=table,
                             model_point_file=TABLE,
                             edits={**(edits or {}), COHORTS: cohorts})
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
                          capture_output=True, text=True, timeout=1800)
    assert done.returncode == 0, done.stderr[-4000:]
    got = pickle.loads(result.read_bytes())
    found, refused, computed, edges = [], 0, 0, {}
    named = {"modelx": 0, "compiled": 0}
    only = iter(COMPILED_ONLY)
    for (case, *_, calls, data, names), (files, *_), (want, want_data), (
            have, have_data) in zip(cases, jobs, wants, got, strict=True):
        have = [_named(did, files) for did in have]
        have_data = [_named(did, files) for did in have_data]
        for n, ((idx, cell, args), modelx_did, compiled_did) in enumerate(
                zip(calls, want, have, strict=True)):
            where = f"{case}: idx {idx}: {cell}{args}"
            if case == IDX_CASE:
                edges[idx, cell, args] = (modelx_did, compiled_did)
                if idx == 19:
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
            if case.startswith("past the floats: ") and n == 0 and len(calls) == 3:
                computed += 1
                if modelx_did[0] != "ok" or not (
                        compiled_did[0] == "ok" and _as_modelx(compiled_did[1],
                                                               modelx_did[1])):
                    found.append(f"{where}: compiled {compiled_did}, modelx {modelx_did}, "
                                 f"where the month before the value computes")
                continue
            if modelx_did[0] != "raised":
                found.append(f"{where}: modelx returned, where a refusal was meant")
            elif compiled_did != modelx_did:
                found.append(f"{where}: compiled {compiled_did}, modelx {modelx_did}")
            refused += 1
            if not names:
                continue
            for engine, did in (("modelx", modelx_did), ("compiled", compiled_did)):
                if did[0] == "raised" and str(did[1]).startswith(
                        f"ValueError: point_id {EXTRACT_LABELS[idx]}: "):
                    named[engine] += 1
                else:
                    found.append(f"{where}: {engine} {did}, not naming point_id "
                                 f"{EXTRACT_LABELS[idx]}")
        for name, modelx_did, compiled_did in zip(data, want_data, have_data, strict=True):
            if modelx_did[0] != "raised":
                found.append(f"{case}: Data.{name}: modelx returned, where a refusal was "
                             f"meant")
            elif compiled_did != modelx_did:
                found.append(f"{case}: Data.{name}: compiled {compiled_did}, modelx "
                             f"{modelx_did}")
            refused += 1
    for (idx, cell, args), outcomes in edges.items():
        if idx == -1 and outcomes != edges[18, cell, args]:
            found.append(f"{IDX_CASE}: {cell}{args} at idx -1 is {outcomes}, at the last "
                         f"row {edges[18, cell, args]}")
    assert edges[-1, "point_id", ()][0] == ("ok", EXTRACT_LABELS[-1]), edges
    assert not found, "\n".join(found[:40])
    assert refused + computed == sum(len(calls) + len(data)
                                     for *_, calls, data, _ in cases[:plain])
    naming = sum(len(calls) - (case.startswith("past the floats: ") and len(calls) == 3)
                 for case, *_, calls, _, names in cases[:plain] if names)
    assert named == {"modelx": naming, "compiled": naming} and naming > 200, (named, naming)


def _extract_with_generated():
    """The committed table under :data:`EXTRACT_LABELS`, the generator's columns kept."""
    committed = _committed()
    return committed.rename(index=_relabel_map())


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
STACK_KIB = (96, 128, 144, 160, 192, 256, 384, 512, 1024, 2048)

# The chain heads the stack test calls cold, each in an ItemSpace of its own, as (cell, the
# code it takes, "LIVE" for the oldest cohort the month can hold, or None): net_cf and the
# roll-forward's residual, the deepest calls a projection makes, and the oldest cohort,
# whose diagonal is the deepest compiled call (the depth test's CHAIN_OVERHEAD).  The
# runner makes one ItemSpace for each key of a job and deletes it after the key's calls,
# so a key with two calls would run the second warm, on the first's caches.
STACK_HEADS = (("net_cf", None), ("check_pols_roll_fwd_resid", None),
               ("pols_sick_dur", "LIVE"))

# How long the stack test waits for each child, in seconds: one runs in a few seconds, more
# under load.  A bracketing size may kill its child on a stack overflow by design, and
# where the overflow hangs instead, as Windows Error Reporting could, the wait ends sooner
# than for the two runs asserted, and the size is recorded as timed out.
BRACKET_TIMEOUT, ASSERTED_TIMEOUT = 120, 300


@pytest.mark.cython
def test_the_longest_cover_runs_cold_on_a_one_megabyte_stack(sec_build, tmp_path):
    """The deepest call the contract allows runs compiled on a 1 MiB stack (F7).

    On the rows of :func:`_longest_cover`, each shape of :data:`CHAIN_SHAPES` at its
    longest cover, 624 months from issue at 18 to expiry at 70, issued now and 120 months
    on, or in claim a year at the valuation date: the anchor cell on the active-lives basis
    and on the exit basis, and the claim from duration 0 on each.  Each of
    :data:`STACK_HEADS`, a cold ``net_cf``, a cold roll-forward residual and the oldest
    cohort the last month can hold, runs the chains back to ``t_entry()``, one cell a
    month, 616 to 630 cells deep in modelx, on a model just read
    (:func:`test_every_chain_runs_one_cell_a_month_from_a_cold_start), at an RPI of 5%.
    Each runs in an ItemSpace of its own, on a copy of its row, so that each is cold: in
    one ItemSpace the second would run on the first's caches, a few cells deep.  Compiled
    they run on the C stack, which the interpreter's recursion limit does not count, and
    they needed 136 to 144 KiB of it here (UKLIB-SEC-PLAN.md §6.3, *Record -- M8*).  1 MiB
    is the stack MSVC gives an executable's main thread unless the executable asks for
    more: a host that embeds Python, where python.exe itself asks for 2,000,000 bytes.  A
    thread whose stack is reserved at 1 MiB stands in for it on every platform
    (``uk_sec_support.run_compiled``), and in one each call runs cold and returns modelx's
    number, identically on x86-64 (``uk_sec_support.exact_here``) and to 1e-12 elsewhere.
    A stack too small kills the child, and the test fails naming the stack.  The thread's
    stack is read back too, from Windows or from glibc, and must be at most 1 MiB and a
    page: a stand-in larger than asked for would stand for nothing.  And the calls run
    again on the child's main thread, which is what ``run_sec.py --cython`` runs on.  In
    modelx the heads' values are computed on one copy of each row, in an ItemSpace released
    as soon as they are read, since a row at the longest cover forms some hundreds of
    thousands of cohorts: a value is the same cold or warm.

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
    rows, held, frames = [], [], []
    for shape in CHAIN_SHAPES:
        folder, shape_frames = _longest_cover(tmp_path / "rows" / shape, shape)
        table = pd.read_csv(folder.parent / TABLE, index_col="point_id")
        cohorts = pd.read_csv(folder.parent / COHORTS)
        for label, months, entry in shape_frames:
            for i in range(len(STACK_HEADS)):
                new = 1000 * (len(frames) + 1) + i
                rows.append(table.loc[[label]].set_axis([new]).rename_axis("point_id"))
                held.append(cohorts[cohorts["point_id"] == label].assign(point_id=new))
            frames.append((1000 * (len(frames) + 1), months, entry))
    case = compiled_case(build, tmp_path / "longest", model_points=pd.concat(rows),
                         edits={COHORTS: pd.concat(held, ignore_index=True)})
    model = mx.read_model(case, name=_name("longest"))
    try:
        model.Projection.rpi_rate = 0.05
        calls, want = {}, {}
        for label, months, entry in frames:
            first = _key(model, label)
            proj = projection(model, first)
            assert (proj.proj_len(), proj.t_entry()) == (months, entry), label
            for i, (head, second) in enumerate(STACK_HEADS):
                args = _head_args(proj, months - 1, second)
                calls[_key(model, label + i)] = [(head, args)]
                want[_key(model, label + i)] = [proj.cells[head](*args)]
            del proj
            _release(model, first)
            gc.collect()
    finally:
        model.close()
    assert len(calls) == len(frames) * len(STACK_HEADS), "a head shares an ItemSpace"
    assert all(len(each) == 1 for each in calls.values()), "a head runs after another, warm"
    assert len(frames) == 6, frames
    job = {"refs": {"rpi_rate": 0.05}, "calls": calls}

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
    record = (f"the compiled cold net_cf, roll-forward residual and oldest cohort at the "
              f"longest cover, each in an ItemSpace of its own, ran on a thread of "
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
early = p[8]
values = [p.expenses(12), early.expenses(12)]
p.inflation_rate = 0.0
values += [p.expenses(12), early.expenses(12), p[10].expenses(12)]
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
    ``Projection``, the anchor cell's twin at ``idx`` 0, the anchor cell in force 60
    months at ``idx`` 8, made before, and the claim on the exit basis at 24, ``idx`` 10,
    made after, so that a modelx-cython that began to clear caches would be seen here, and
    the advice changed with it.  A compiled value meets modelx's as C4 holds it
    (:func:`_as_modelx`), and one the compiled model kept, its own value of before,
    identically.
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
        before = (p.expenses(12), projection(model, 8).expenses(12))
        p.inflation_rate = 0.0
        fresh = (p.expenses(12), projection(model, 8).expenses(12),
                 projection(model, 10).expenses(12))
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
    modelx's: point 9's description, the anchor cell in force at 60, and its first twelve
    rows and counts, point 11's, the claim on the exit basis in force at 36 months, its
    claim at 25, and the block's lines for each point, its first twelve rows and its first
    twelve projection years.

    The same output is what a runner that ignored ``--build`` and ran modelx would print,
    so the runner is also given a directory that holds no build, and must refuse it,
    saying so, rather than print anything.
    """
    build = sec_build(SEC)
    runner = model_path(SEC).parent / "run_sec.py"
    for args in (("9",), ("11",), ("--block",)):
        expected = _run_sec(runner, *args)
        assert _run_sec(runner, *args, "--cython", "--build", str(build.out)) == expected
    empty = tmp_path / "no_build"
    empty.mkdir()
    done = _run_sec(runner, "9", "--build", str(empty), check=False)
    stderr = done.stderr.decode(errors="replace")
    assert done.returncode != 0 and done.stdout == b"", stderr
    assert f"holds no build of {SEC} for this interpreter" in stderr, stderr
