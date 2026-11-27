"""In-force and compile tests for PA_UK_SEC: the splice, future business, counts,
regeneration, the compiled model.

``PA_UK_SEC`` is ``PA_UK_S`` taught to run in force at a valuation date
(UKLIB-SEC-PLAN.md, milestone M11, after USLIB-SEC-PLAN.md's Phase 1), on the payout
chassis of uslib's ``SPIA_US_SEC``, and made to compile under modelx-cython (milestone
M12, after its Phase 2), as ``SPIA_US_SEC`` was at uslib's M23.  It runs on two clocks:
``t`` counts months from the valuation date, the same month for every model point, and
``duration_mth(t)`` counts the months from the annuity's start date,
``duration_mth_init() + t``.  A model point may be an
annuity already in payment at the valuation date, in any month of its policy year, one
starting at it, or one to start after it, as in ``basiclife/BasicTerm_SE``.  A contract in
payment opens with its state beside its count, each per contract and measured at the
valuation instant: each covered life's survival, ``lives_if_init_1`` and
``lives_if_init_2``; the payments made to date on every stream, ``cum_annuity_all_init``;
and on RPI-linked escalation the history no flat ``rpi_rate`` re-derives, the income of the
policy year under way before any month-0 anniversary, ``annual_income_init``, the ratchet's
peak over the latest index, ``rpi_peak_init``, and where value protection is on the first
death the annuitant's as-if-alive instalments to date, ``cum_annuity_pp_init``.  The count
on the books is never decremented: mortality decrements each life's survival, and
``pols_if`` is ``PA_UK_S``'s closing obligation measure on that count, so the registry marks
the model ``closing_pols_if``.

The worked example is not restated here.  On a point starting at the valuation date the two
clocks coincide and the model is ``PA_UK_S``, and ``test_model_conventions_uk.py`` asserts
that cell by cell on the twins of S's ten points (T1), so every golden of
``test_pension_annuity_uk.py`` holds on this model with no number copied.  The conventions
also hold the SEC family's other rules: every frame opens at ``t = 0``, ``BEF_DECR`` is
``BEF_NB`` plus the month's new business, new business enters once, and nothing happens
before the start.  This module holds the rest of the plan's tests (its §5) and the
product's own facts:

* T2, the splice: an S point restated in payment at month ``d``, opened with the state S
  carries into ``d``, continues S's projection from ``d`` on, in every cell of S's.  The
  months straddle the product's events: quarterly payments in arrears, the anniversaries,
  the scenario death, the guarantee's end, value protection running out on the first and
  the last death, the mortality cap, the older life past the limiting age and the frame's
  last month.  Sixteen variants of S's points, in a copy of S's table, add advance timing
  with value protection on either death, semi-annual and annual payments, the dependant
  dying first, both lives dead with and without a guarantee, a guarantee past the age
  stop, a rated joint life, the proportionate payment on the table basis, the RPI bases
  without first-death value protection, value protection apart from the dependant's
  share and on a single life, a dependant older than the annuitant and a dependant's
  share of 0; and the RPI points are spliced under RPIs of 8% and -2%, where the LPI cap
  and floor bind and the ratchet freezes, beside a fixed escalation, which no RPI moves.
* T3, future new business: a point starting ``k`` months after the valuation date is S's
  projection ``k`` months on, with zeros before it and no rate evaluated there.
* D11's R1 and R2, and D3's and D5's chains: on the splice's grid no cell is called at a
  negative month, none on the books reads a month before them, none reads beyond
  ``t + 1``, and on an RPI-linked row none asks a year, an anniversary or a policy month
  closed before the valuation date; on the committed points no recursion runs backward
  over the frame; the policy clock is a closed form; and each chain, called cold, runs one
  cell a month back to ``t_entry()``, at each shape's longest cover.
* T4, the count algebra: the count is never decremented, ``BEF_NB`` a closed form;
  multiplying ``policy_count`` by 2.5 multiplies every flow and every counted cell by 2.5
  and moves no per-contract value, each flow nonzero on some point; and a point restated a
  month on, with the state it carries there, continues its own flows.
* T5, validation: each malformed row of the table is refused as it is read, naming its
  point, on the committed labels and on an extract's; each text value no decode knows
  raises ``PA_UK_S``'s message; the mortality table is refused before a value of it is
  read; the future horizon is a Reference; a point at or past its stop, one owing nothing,
  one the contract does not issue and one read under a Reference outside its domain are
  refused by the frame, each domain at both its edges, each accepted edge projected; a
  value a power or a product takes past the floats is refused where it first is, naming
  the References; the edges of the interface are accepted, each window of ``Data``'s at
  both its ends; and so is every state ``PA_UK_S`` reaches, on each set of inputs on which
  those states differ, but a contract owing nothing, which is set aside and shown
  refused.
* T6, regeneration: the committed ``model_point_table_sec.csv`` is what the generator makes
  of ``PA_UK_S`` and its table as they stand.
* Then the product's own facts: the two clocks; the committed rows continuing their S
  points, and the three read from S under an RPI of their own, the two LPI rows projected
  under it to the cap's and the floor's goldens; each history column read rather than
  recomputed (UKLIB-SEC-PLAN.md K14), the ratchet's catch-up among them, with goldens of
  its own; the income measured before month 0's anniversary; the RPI, inflation
  and improvement each on its clock; no premium and no acquisition; the cap on mortality
  and a NaN that reaches it; the checks failing a NaN residual; the values outside the
  frame; the block; an in-force extract; the runner; the docstrings; the shared input
  table; and what the default grid reaches.
* The C step's representation, in modelx: the claims total ``PA_UK_S``'s to the last bit;
  every decode ``PA_UK_S``'s own on every value; the mortality array's NaN padding and each
  sex's own extents; each ``Data`` vector of the dtype its docstring states; every
  parameterless cell a Python number; each label refusing or returning its column; the
  spec's sizes and the sample's recursion limit held to their comments' derivations; the
  runner's rebuild; what the vectors cannot hold and the codes no cell takes; each column
  only some points read refused by the point that reads it and by no other; each chain
  blocked by policy year opening a year with its own float; and no cell a chain recurses
  through building text.
* C2, the fingerprint: every committed point computes what the model computed when its E
  step ended, frozen at the end of this module before its C step changed anything
  (USLIB-SEC-PLAN.md §5.4), and refrozen once since, when M11's review added point 23,
  which added its entry and changed no other.
* The compiled section, after it, marked ``cython``: the compiled model computes what
  modelx computes on the splice grid under each set of References, on the variants no
  committed row holds, at the contract's extremes, where the cap binds, on every decoded
  value and on keys written as floats; the LPI rows hold their bounds compiled under their
  own RPI; the labels, the refusals and the overflows are modelx's; the deepest calls run
  on a 1 MiB stack; a Reference set late clears no cache; and the runner prints the
  compiled model as it prints modelx.  ``test_compiled_conventions_uk.py`` holds the
  typing, C4 on the committed points and the release.

SEC month ``t`` is S month ``t + source_mth`` throughout, the direction in which
``uk_sec_support`` takes its ``t_offset``: ``d`` for a point restated at S month ``d``,
``-k`` for one starting ``k`` months on.

**The core grid and the full one** (UKLIB-SEC-PLAN.md U6).  T2 and T3 over every S point at
every month, about 400 cases, run by default on a core, chosen so that between them they
reach every branch, every opening-state column, every kind of valuation month and both
sides of every ``min`` and ``max`` the full grid reaches, which
``test_the_core_grid_reaches_every_branch`` asserts.  The other cases, the rules test's
scan of their rows, and the depth test's shapes issued 120 months on, which run as deep as
those issued now, carry the ``sec_full`` marker and are skipped, with the reason shown,
unless ``UKLIB_SEC_FULL=1`` is set.  They are never dropped: one leg of the CI matrix sets
it, and ``UKLIB_SEC_FULL=1 python -m pytest -m sec_full
lifelib/libraries/uklib/tests/test_pension_annuity_uk_sec.py`` runs them alone.  Each
splice row is released once it has been read (``_release``), as ``run_sec.py --block``
releases its points.

Every test keeps four rules.  Each model is read under a name of its own and closed:
``conftest.pension_annuity`` reads S under its default name, and reading a model under a
name in use renames the open one.  No test writes inside the library tree: every changed
input goes through ``uk_sec_support.temp_inputs`` into a temporary directory, because a CSV
added beside the models, even briefly, would fail a concurrent
``test_every_csv_beside_the_model_is_actually_read``.  No test indexes ``Projection`` by
hand: the keys come from ``uk_registry.point_keys`` and the ItemSpaces from
``uk_registry.projection``, and a generated row is found by what it is, its kind, its S
policy and its month (``_row``), so neither a renumbered table nor the C step's positions
can point a test at the wrong row.  And a timing or a kind is passed through ``_code``,
which gives the model's int Reference of its name where the model has one, as at stage
``"EC"`` it does, and the string at stage ``"E"``; every comparison with S passes
``uk_sec_support.codes`` and the spec's ``twin_arg_map`` (``_mismatches``).
"""
import ast
import dataclasses
import gc
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
import warnings

import modelx as mx
import numpy as np
import pandas as pd
import pytest

from uk_registry import model_path, point_keys, projection
from uk_sec_support import (
    SEC_SPECS, TWIN_EXEMPT_DEFAULT, build_sec_table, check_generated,
    codes, compiled_case, compiled_mismatches, exact_here, fingerprint_mismatches,
    frame_mismatches, full_sweep, label_mismatches, labels_refusing_non_text,
    reporting_cells, run_compiled, sweep, temp_inputs, twin_mismatches)
from uk_sec_support import _pa_c4_also
from uk_sec_support import generated_columns

SEC, TWIN = "PA_UK_SEC", "PA_UK_S"
TABLE = "model_point_table_sec.csv"
SPEC = SEC_SPECS[SEC]

# S's ten points, every one starting at the valuation date: the worked example, a joint
# life with a dependant at 50%, quarterly in arrears, fixed 3%, value protection of 50% on
# the first death, on the scenario basis, the annuitant dying in policy month 16 (1); the
# same on the table basis (2); a 120-month guarantee without overlap (3) and with it (4);
# a single life, level, monthly in advance, on the table (5); the RPI catch-up (6) and LPI
# (7) on the table; a single life rated 1.35, level, monthly in arrears (8); the
# proportionate final payment (9); and value protection on the last death (10).
S_POINTS = tuple(range(1, 11))

# Sixteen more S points, in the splice's copy of S's table and never in the committed one,
# each one of S's points changed so as to reach what S's own points cannot.  A committed row
# is one of S's points restated (D8), so a term S's own table never holds, value protection
# apart from the dependant's share or on a single life, reaches T2 alone:
#
# 11, S point 2 in advance: value protection measured after an advance instalment;
# 12, S point 2 paying twice a year, in arrears;
# 13, S point 5 paying once a year, in advance;
# 14, S point 1 with the dependant dying first, in policy month 10, and the annuitant in 40;
# 15, S point 3 with the dependant dying in 30 too: both lives dead inside its guarantee,
#   which pays on to policy month 120, after which nothing is owed;
# 16, S point 1 with the dependant dying in 30: both lives dead without a guarantee, after
#   which nothing is owed;
# 17, S point 5 bought at 90 with a 360-month guarantee: the guarantee past the age stop;
# 18, S point 2 rated, the annuitant at 1.3 and the dependant at 1.5;
# 19, S point 2 with the proportionate final payment, on the table basis, where it is paid
#   in every month a life can die;
# 20, S point 10 in advance on the table basis: last-survivor value protection measured
#   after an advance instalment, which the scenario's dependant, who never dies, never
#   claims;
# 21, S point 6 without value protection: RPI-linked, so the annuitant's payments to date
#   are read nowhere;
# 22, S point 7 with value protection on the last death: RPI-linked, the annuitant's
#   payments to date read nowhere either;
# 23, S point 2 with value protection of 30%, apart from the dependant's 50%: the balance
#   nets v x P, which every S point's v = delta = 0.5 hides;
# 24, S point 5 with value protection of 50% on its single life, monthly in advance;
# 25, S point 2 with a dependant of 70, older than the annuitant: the age stop is on the
#   annuitant, the youngest life;
# 26, S point 2 with a dependant's share of 0: the obligation measure drops the dependant's
#   leg while the dependant is alive.
#
# Each variant is (the S point it changes, the columns it changes); the policy_id keeps the
# generated ids apart.
VARIANTS = {
    11: (2, {"policy_id": "PA-900011", "timing": "advance"}),
    12: (2, {"policy_id": "PA-900012", "frequency": 2}),
    13: (5, {"policy_id": "PA-900013", "frequency": 1}),
    14: (1, {"policy_id": "PA-900014", "death_mth_1": 40.0, "death_mth_2": 10.0}),
    15: (3, {"policy_id": "PA-900015", "death_mth_2": 30.0}),
    16: (1, {"policy_id": "PA-900016", "death_mth_2": 30.0}),
    17: (5, {"policy_id": "PA-900017", "annuitant_age": 90, "guarantee_months": 360}),
    18: (2, {"policy_id": "PA-900018", "rating_multiplier": 1.3, "dependant_rating": 1.5}),
    19: (2, {"policy_id": "PA-900019", "proportion": True}),
    20: (10, {"policy_id": "PA-900020", "timing": "advance", "mort_basis": "table"}),
    21: (6, {"policy_id": "PA-900021", "vp_pct": 0.0}),
    22: (7, {"policy_id": "PA-900022", "vp_basis": "last_survivor"}),
    23: (2, {"policy_id": "PA-900023", "vp_pct": 0.3}),
    24: (5, {"policy_id": "PA-900024", "vp_pct": 0.5}),
    25: (2, {"policy_id": "PA-900025", "dependant_age": 70}),
    26: (2, {"policy_id": "PA-900026", "dependant_pct": 0.0}),
}

# Each point's frame from its start, in months: the age stop on its youngest life, or the
# guarantee if longer.
FRAME = {**{p: 636 for p in (1, 2, 3, 4, 6, 7, 9, 10)}, 5: 600, 8: 600,
         **{p: 636 for p in (11, 12, 14, 15, 16, 18, 19, 20, 21, 22, 23, 26)}, 13: 600,
         17: 360, 24: 600, 25: 600}

# The first S month from which a point owes nothing, every covered life dead and no
# guarantee left, so that proj_len() refuses it restated there or later: S point 8, whose
# rated life the cap kills in policy month 576, and variants 14, 15 and 16 once both their
# lives have died (measured at M11).  The splice leaves those months out, and the
# every-state test sets them aside and shows them refused.
OWES_NOTHING_FROM = {8: 577, 14: 41, 15: 120, 16: 31}

# T2's months (UKLIB-SEC-PLAN.md §6.7): 1, 2 and 3, about the first quarterly payment in
# arrears; 11 to 13 and 23 to 25, about the first two anniversaries; 15 to 17, about the
# scenario death in policy month 16, value protection and the proportionate payment in it
# and the dependant's first instalment after it; 101 and 102, where first-death value
# protection runs out; 119 to 122, about the guarantee's end; 170 and 171, where
# last-survivor value protection runs out; 575 and 576, where point 8's mortality cap first
# binds; 599 and 600, where the older life reaches the limiting age; and 635, the joint
# frames' last month.  A month at or past a point's frame, or from the one it owes nothing
# (OWES_NOTHING_FROM), is left out.  Each variant's months straddle its own events: the
# advance balance's last month, 99, and run-out, 100; the first semi-annual payments; the
# annual instalment's anniversary; each death; the age stop at 300 inside the guarantee;
# the rated annuitant's cap from 576; the advance last-survivor balance's last claim, 98,
# and run-out at 100; the 30% balance's run-out at 63 and the single life's at 91; the
# older dependant past the limiting age from 540; and the dependant at 0% alive past the
# annuitant from 601 (measured at M11).
SPLICE_MTHS = (1, 2, 3, 11, 12, 13, 15, 16, 17, 23, 24, 25, 101, 102, 119, 120, 121, 122,
               170, 171, 575, 576, 599, 600, 635)
VARIANT_MTHS = {11: (2, 3, 99, 100), 12: (1, 5, 6, 101), 13: (1, 12, 13, 599),
                14: (9, 10, 11, 39, 40), 15: (16, 29, 30, 31, 119),
                16: (16, 17, 29, 30), 17: (1, 299, 300, 359), 18: (1, 24, 575, 576),
                19: (1, 2, 24), 20: (1, 3, 16, 98, 99), 21: (12, 24), 22: (12, 24),
                23: (1, 24, 61, 62, 63), 24: (1, 12, 89, 90, 91),
                25: (1, 539, 540, 541, 599), 26: (1, 101, 575, 601)}


def _owes(s_point, month):
    """Whether S point ``s_point`` restated at ``month`` owes something: inside its frame,
    before the month it owes nothing from."""
    return month < min(FRAME[s_point], OWES_NOTHING_FROM.get(s_point, FRAME[s_point]))

# The splice's three sets of References, each set in both models before either evaluates
# anything.  Expense inflation is the one input PA reads on the valuation clock (D7): S
# inflates from the start and SEC from the valuation date, so at the shipped 3% the expenses
# of a point opened at d differ by 1.03^(d // 12), by design, and at 0 both factors are 1.
# The clock itself is asserted on its own, at the shipped rate.  Improvement is dated by the
# calendar on the policy clock in both, and so is left at its shipped scale (D7, precised at
# M11).  rpi_rate is a flat Reference, the RPI on either clock, so the RPI sets run S and
# SEC at one rate: 8%, past the LPI's 5% cap, and -2%, below its floor, where the catch-up's
# index falls and the ratchet freezes the income; and a fixed escalation runs beside them,
# at its own 3%, which the shipped RPI equals.  Nothing else ships at 0 to switch on.
SPLICE_SETS = {
    "shipped": {"inflation_rate": 0.0},
    "rpi_high": {"inflation_rate": 0.0, "rpi_rate": 0.08},
    "rpi_low": {"inflation_rate": 0.0, "rpi_rate": -0.02},
}

# The RPI points, spliced under each RPI set at its anniversaries, the month before and
# after each, and the sixth: S's two RPI points and the variants that move their value
# protection.  And beside them S point 2, fixed at 3%, spliced at 24 and at 101, valued
# late, where the income compounds at the valuation date's key: under an RPI of 3%, the
# shipped one, an income compounded at the RPI rather than at the contract's g is the same
# number.  The RPI sets' S models hold these five points.
RPI_POINTS = (6, 7, 21, 22)
RPI_MTHS = (11, 12, 13, 23, 24, 25, 60, 61)
FIXED_POINT, FIXED_MTHS = 2, (24, 101)
RPI_SET_POINTS = (FIXED_POINT, *RPI_POINTS)

# T2's cases, as (set, row_kind, S point, source_mth): each S point restated in payment at
# each of its months inside its frame, then each variant at its own, then the RPI points
# under the RPI sets.  PA_UK_S has no point in payment, so no twin is a splice case.  T3's
# cases, as (set, S point, k).
SPLICES = (tuple(("shipped", "derived", p, d) for p in S_POINTS for d in SPLICE_MTHS
                 if _owes(p, d))
           + tuple(("shipped", "derived", p, d) for p, mths in VARIANT_MTHS.items()
                   for d in mths if _owes(p, d))
           + tuple((rates, "derived", p, d) for rates in ("rpi_high", "rpi_low")
                   for p in RPI_POINTS for d in RPI_MTHS)
           + tuple((rates, "derived", FIXED_POINT, d) for rates in ("rpi_high", "rpi_low")
                   for d in FIXED_MTHS))
IN_FORCE_TWINS = ()
FUTURES = (tuple(("shipped", p, k) for p in S_POINTS for k in (1, 12))
           + tuple(("shipped", p, 1) for p in VARIANTS)
           + (("shipped", 6, 13), ("shipped", 1, 25))
           + tuple((rates, p, k) for rates in ("rpi_high", "rpi_low") for p in (6, 7)
                   for k in (1, 13)))

# The default run's cases (the module docstring), each with what it is there for.  The rest
# of SPLICES and FUTURES run with UKLIB_SEC_FULL=1.
CORE_SPLICES = {
    ("shipped", "derived", 1, 1): "the worked example in its second month",
    ("shipped", "derived", 1, 2): "the worked example in its first payment month",
    ("shipped", "derived", 1, 12): "the worked example on its first anniversary",
    ("shipped", "derived", 1, 16): "the worked example in the month of the death",
    ("shipped", "derived", 1, 17): "the dependant's first instalment",
    ("shipped", "derived", 9, 16): "value protection and the proportionate payment",
    ("shipped", "derived", 3, 119): "the guarantee's last month, without overlap",
    ("shipped", "derived", 3, 120): "the guarantee ended, the dependant's income starting",
    ("shipped", "derived", 4, 119): "the guarantee's last month, the dependant paid beside "
                                    "it",
    ("shipped", "derived", 2, 13): "the table basis after its first anniversary",
    ("shipped", "derived", 2, 101): "first-death value protection's last balance",
    ("shipped", "derived", 2, 102): "first-death value protection run out",
    ("shipped", "derived", 10, 171): "last-survivor value protection run out",
    ("shipped", "derived", 8, 575): "the month before the rated life's cap binds",
    ("shipped", "derived", 8, 576): "the rated life's cap binding",
    ("shipped", "derived", 2, 600): "the older life past the limiting age",
    ("shipped", "derived", 2, 635): "the joint frame's last month",
    ("shipped", "derived", 5, 120): "the single life, monthly in advance",
    ("shipped", "derived", 6, 25): "the RPI catch-up after an anniversary",
    ("shipped", "derived", 7, 23): "the LPI before an anniversary",
    ("shipped", "derived", 11, 3): "advance value protection, the instalment netted",
    ("shipped", "derived", 12, 5): "semi-annual payments in arrears",
    ("shipped", "derived", 13, 12): "an annual instalment in advance",
    ("shipped", "derived", 14, 11): "the dependant dead first",
    ("shipped", "derived", 14, 40): "the annuitant dying after the dependant",
    ("shipped", "derived", 15, 31): "both lives dead inside the guarantee",
    ("shipped", "derived", 16, 30): "both lives dying without a guarantee",
    ("shipped", "derived", 17, 300): "the guarantee past the age stop",
    ("shipped", "derived", 18, 24): "a rated joint life",
    ("shipped", "derived", 19, 2): "the proportionate payment on the table basis",
    ("shipped", "derived", 20, 3): "last-survivor value protection in advance, claimed",
    ("shipped", "derived", 21, 24): "the RPI catch-up without value protection",
    ("shipped", "derived", 22, 12): "the LPI with last-survivor value protection",
    ("shipped", "derived", 23, 24): "value protection apart from the dependant's share",
    ("shipped", "derived", 24, 12): "value protection on a single life, in advance",
    ("shipped", "derived", 25, 539): "a dependant older than the annuitant, at its stop",
    ("shipped", "derived", 26, 575): "a joint life at a dependant's share of 0",
    ("rpi_high", "derived", 7, 24): "the LPI cap binding, its history capped",
    ("rpi_high", "derived", 6, 13): "the catch-up's index rising past its peak",
    ("rpi_low", "derived", 6, 24): "the ratchet frozen, its peak above the index",
    ("rpi_low", "derived", 7, 25): "the LPI floor binding",
    ("rpi_low", "derived", 21, 61): "the ratchet frozen, no value protection",
    ("rpi_high", "derived", 2, 24): "a fixed escalation under an RPI above it",
    ("rpi_low", "derived", 2, 101): "a fixed escalation under an RPI below it, valued late",
}
CORE_FUTURES = {
    ("shipped", 1, 1): "starting a month off the valuation anniversaries",
    ("shipped", 1, 12): "starting on them, a year on, the block's",
    ("shipped", 5, 1): "the single life in advance",
    ("shipped", 6, 13): "the RPI catch-up, more than a year on",
    ("shipped", 1, 25): "the worked example, more than two years on",
    ("shipped", 17, 1): "the guarantee past the age stop",
    ("rpi_low", 7, 13): "the LPI floor, more than a year on",
}

SEC_FULL = os.environ.get("UKLIB_SEC_FULL") == "1"
FULL_ONLY = (pytest.mark.sec_full,
             pytest.mark.skipif(not SEC_FULL, reason="the full splice grid runs with "
                                "UKLIB_SEC_FULL=1 (UKLIB-SEC-PLAN.md U6)"))

# The cells T2 skips beyond T1's.  proj_len counts from the valuation date on SEC and from
# the start on S, so it differs by d by design; the comparison asserts what it must get
# right, that both frames end at the same instant.  payment_surv_mth returns a time point,
# which on SEC's clock is S's less d, as SPIA's does: payment_factor_life and
# dependant_factor, which read it, are compared, so a wrong survival point still fails.
# annual_income_init is S's first year's income and SEC's income of the year under way at
# the valuation date, the two the same only where that year is the first; the splice
# compares the column with S's income of that year (_compare).  rpi_index and rpi_peak are
# measured relative to the latest index at the valuation date on SEC, and from outset on S,
# so they differ by S's index there; the splice compares them so scaled (_compare).
SPLICE_EXEMPT = (TWIN_EXEMPT_DEFAULT | SPEC.exempt
                 | {"proj_len", "payment_surv_mth", "annual_income_init", "rpi_index",
                    "rpi_peak"})

# T3's: a point starting later measures its index from outset and its income from the
# first year, as S's does, so only the frame and the survival point, a time point on the
# valuation clock, S's plus k, are exempt beyond T1's.
FUTURE_EXEMPT = TWIN_EXEMPT_DEFAULT | SPEC.exempt | {"proj_len", "payment_surv_mth"}

# The result_cf columns that expense inflation moves, and the cells they are made of: on the
# committed points, at the shipped 3%, the only places an in-force row departs from S.
INFLATED = ("expenses", "liability_cf", "net_cf")
INFLATION_CELLS = frozenset({"inflation_factor", "expenses", "liability_cf", "net_cf",
                             "result_cf"})

# The cells whose exact value is 0 and whose computed value is rounding about it, held at
# the harness's absolute floor of 1e-9, as the template's residuals are (§5.2, T2): every
# other cell at none (_compare).
RESIDUALS = frozenset({"check_lives_roll_fwd_resid", "check_payment_factor_resid"})
FLOOR = 1e-9

# The reports, which the comparison reads as frames rather than as cells.
REPORTS = ("result_cf", "result_pols")

# The cells that scale with policy_count.  Every other cell is a per-contract amount, a
# probability, a factor, a clock or a flag, and must not move when the count does.
COUNTED = frozenset({
    "policy_count", "pols_if_init", "pols_if", "pols_if_at", "pols_new_biz",
    "annuity_payments", "claims", "expenses", "liability_cf", "net_cf",
    "result_cf", "result_pols"})

# result_pols' columns, in its order: the closing obligation measure and the new business,
# then PA_UK_S's other columns in its order.
RESULT_POLS = ["pols_if", "pols_new_biz", "lives_if_1", "lives_if_2", "certain_floor",
               "payment_factor", "dependant_factor", "annuity_pp", "cum_annuity_all",
               "vp_balance"]
COUNTED_POLS = ("pols_if", "pols_new_biz")

# The flows of result_cf, each nonzero on some committed point (T4).
FLOWS = ("annuity_payments", "claims_vp", "claims_prop", "expenses", "liability_cf",
         "net_cf")

# The timings and the kinds.
TIMINGS = ("BEF_NB", "BEF_DECR")
KINDS = ("VP", "PROP")

# What each cell holds outside the frame, before the start and from the stop rule on, as
# its docstring says: no count, so no cash flow; no instalment, floor or factor; no rate
# read at a policy year or an age the contract does not have.  The type is part of the
# value: a count is a float in every branch and a flag a bool, because the C step types a
# cell by the values it returns (USLIB-SEC-PLAN.md F3).  The guard test also calls
# pols_if_at at each timing, claims at each kind and each (t, life) cell for both lives,
# all 0.0.
OUTSIDE_COVER = {
    "is_active": False, "is_payment_mth": False, "annuity_pp": 0.0,
    "next_payment_mth": -1, "mths_since_payment": 0, "lives_death_last": 0.0,
    "certain_floor": 0.0, "payment_factor_life": 0.0, "payment_factor": 0.0,
    "overlap_gate": 0.0, "dependant_factor": 0.0, "annuity_payments": 0.0,
    "pols_if": 0.0, "pols_new_biz": 0.0, "expenses": 0.0, "liability_cf": 0.0,
    "net_cf": 0.0, "check_payment_factor_resid": 0.0}
PER_LIFE_OUTSIDE = ("lives_death", "mort_rate", "mort_rate_base", "improve_rate",
                    "improve_factor")

# The time points before the contract is on the books, which hold 0.0 there: survival, the
# expected payments to date, the value-protection balance and the residual.
BEFORE_ENTRY = ("lives_if_last", "cum_annuity_all", "vp_balance",
                "check_lives_roll_fwd_resid")

# The cells a month outside the frame may not reach: the clocks of the contract, keyed by a
# policy year, an attained age or a calendar year.
IN_COVER_ONLY = ("duration", "policy_year", "calendar_year", "age")

# The opening state, in the table's order, and the cells running in force and compiling
# add to PA_UK_S's, each of which the symbol map must name: the C step's last nine, the
# label, the sex's schedule, the three chains' openings of a policy year, the three
# refusals moved off the chains, and the payments on every stream on the policy clock.
STATE = ("lives_if_init_1", "lives_if_init_2", "cum_annuity_all_init",
         "annual_income_init", "rpi_peak_init", "cum_annuity_pp_init")
NEW_CELLS = ("policy_count", "duration_mth_init", "t_entry", "stop_mth", "is_active",
             "pols_if_at", "pols_new_biz", "lives_if_init", "cum_annuity_all_init",
             "rpi_peak_init", "cum_annuity_pp_init", "annual_income_first",
             "policy_year_init", "is_payment_pm", "annuity_pp_pm", "cum_annuity_all",
             "mort_rate_base_at", "is_arrears", "is_scenario", "is_first_death",
             "is_level", "is_fixed", "is_lpi5", "is_rpi_catchup", "point_id",
             "mort_schedule", "lives_if_py", "cum_annuity_all_py", "cum_annuity_pp_py",
             "annual_income_refusal", "cum_annuity_all_refusal", "cum_annuity_pp_refusal",
             "cum_annuity_pp_all")

INFLATION = 0.03        # the shipped inflation_rate, which the inflation test reads

# The recursion limit, as mx.set_recursion takes it, under which the committed points are
# first swept (R2, F7).  A report evaluates each column in ascending t, so a forward
# recursion, through t - 1, finds the month before already cached; the committed points'
# sweep passes under a limit of 7, and fails under 6 (measured at M11).  A backward
# recursion over the frame, through t + 1, opens a chain as long as the frame, and the
# shortest committed frame longer than a month is 25.
CALL_DEPTH = 40

# The reads beyond t + 1 the model makes, as (reader, cell read): none.  PA_UK_S's one,
# the proportionate payment's scan to the next payment month, is a closed form on the
# policy month here (UKLIB-SEC-PLAN.md §6.7).
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
    is the twin's.  The two ``derived_refs`` rows, read from S under an RPI of their own,
    are the only rows of their point and month, and are found the same way.
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


def _s_table():
    """S's committed table, indexed by point_id."""
    return pd.read_csv(model_path(TWIN).parent / "model_point_table.csv",
                       index_col="point_id")


def _s_table_with_variants(points=None):
    """S's committed table with the :data:`VARIANTS` appended, under their own point_ids;
    only ``points`` of it, where given."""
    table = _s_table()
    rows = []
    for point_id, (base, changes) in VARIANTS.items():
        row = table.loc[[base]].assign(**changes)
        row.index = pd.Index([point_id], name="point_id")
        rows.append(row)
    table = pd.concat([table, *rows])
    return table if points is None else table.loc[list(points)]


def _sec_inputs(tmp_path, table, edits=None):
    """A copy of the product directory whose SEC table is ``table``, other inputs changed
    by ``edits``, as :func:`uk_sec_support.temp_inputs` takes them; its SEC folder."""
    return temp_inputs(tmp_path, model_path(SEC), model_points=table,
                       model_point_file=TABLE, edits=edits)


def _read_edited(tmp_path, edit, edits=None):
    """PA_UK_SEC read from a copy whose SEC table is ``edit(_committed())``."""
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


# Every how many time points a sweep evaluates the survival check's residual (_sweep).
SAMPLED = 25


def _sweep(proj):
    """Evaluate on an S point or an SEC row what a comparison reads: the reports and more.

    ``result_cf()``, ``result_pols()`` and the three checks that read the frame once,
    ``check_payment_factor()``, ``check_guarantee_xor()`` and ``check_vp_bound()``; then,
    over the frame, the cells no report reaches on every point, so that the comparisons see
    them too: ``next_payment_mth`` and ``mths_since_payment``, which only the proportionate
    payment reads, ``duration_mth``, ``payment_surv_mth`` and each covered life's
    ``lives_death``.  Not ``check_lives_roll_fwd``: its independent rebuild of survival is
    a product over every month before each time point, quadratic in the frame, about 110 MB
    of modelx's dependency graph on a point on the table basis, which held in the module's
    swept models took its peak past 4 GB (measured at M11), and SPIA's sweep leaves it out
    too (USLIB-SEC-PLAN.md §7.9, *Record — M11*).  Its residual is evaluated instead at
    every :data:`SAMPLED`-th time point and at the frame's close, so that a comparison
    still holds S's residual against this model's there.  The whole check runs on every
    committed row in the conventions, on every twin in T1, and on every splice row in the
    rules test (:func:`_rule_breaches`).
    """
    proj.result_cf()
    proj.result_pols()
    for name in ("check_payment_factor", "check_guarantee_xor", "check_vp_bound"):
        proj.cells[name]()
    lives = (1, 2) if proj.is_joint() else (1,)
    end = proj.proj_len()
    for t in range(end):
        proj.next_payment_mth(t)
        proj.mths_since_payment(t)
        proj.duration_mth(t)
        proj.payment_surv_mth(t)
        for life in lives:
            proj.lives_death(t, life)
    for k in (*range(0, end + 1, SAMPLED), end):
        proj.check_lives_roll_fwd_resid(k)


def _rpi_linked(s_proj):
    """Whether S point ``s_proj`` escalates with the RPI."""
    return s_proj.escalation_type() in ("lpi5", "rpi_catchup")


def _before_valuation(s_proj, month):
    """An ``arg_map`` that skips each S key before the valuation date that SEC does not
    carry as S keys it (USLIB-SEC-PLAN.md §5.2, T2, precised at M7).

    ``cum_annuity_pp``'s keys before S's month ``month``: the ``"ALL"`` payments to date
    are SEC's opening state, one total, and on RPI-linked escalation so are the annuitant's.
    And on RPI-linked escalation ``annual_income``'s years before the one under way at the
    valuation instant: history SEC carries in its opening state.  On level and fixed
    escalation the annuitant's schedule and its income are the contract's, which SEC
    re-derives at every key, so those keys are compared.
    """
    linked = _rpi_linked(s_proj)
    first_year = max(month - 1, 0) // 12 + 1

    def mapped(name, args):
        if name == "cum_annuity_pp" and args[0] < month and (
                args[1] == "ALL" or linked):
            return None
        if name == "annual_income" and linked and args[0] < first_year:
            return None
        return args
    return mapped


def _index_faults(s_proj, sec_proj, month):
    """Where SEC's relative index and peak depart from S's, scaled by S's index at ``a0``.

    SEC measures ``rpi_index`` and ``rpi_peak`` relative to the latest index at the
    valuation instant, the one of the anniversary ``a0`` that opened the year under way,
    where S measures them from outset.  So at every anniversary ``a >= a0`` S cached, SEC's
    is S's over S's index at ``a0``, to 1e-12 relative.
    """
    if s_proj.escalation_type() != "rpi_catchup":
        return []
    a0 = max(month - 1, 0) // 12
    scale = s_proj.rpi_index(a0)
    found = []
    for name in ("rpi_index", "rpi_peak"):
        for a in sorted(s_proj.cells[name].keys()):
            if a < a0:
                continue
            want = s_proj.cells[name](a) / scale
            got = sec_proj.cells[name](a)
            if not math.isclose(got, want, rel_tol=1e-12, abs_tol=0.0):
                found.append(f"{name}({a}): SEC {got!r}, S's over its index at {a0}, "
                             f"{want!r}")
    return found


def _mismatches(s_proj, sec_proj, *, arg_map=None, **kwargs):
    """:func:`uk_sec_support.twin_mismatches` of an S point and an SEC row, the one place
    this module compares them so.

    It passes the SEC Space's :func:`uk_sec_support.codes`, which map S's timing and kind
    strings to the int codes the C step gives them, and the spec's ``twin_arg_map``, which
    maps S's ``claims(t, None)``, its total, onto SEC's ``ALL`` and passes SEC's own keys
    unchanged, composed before ``arg_map``, the comparison's own cut of S's keys, as ULB's
    and FIA's modules compose them (USLIB-SEC-PLAN.md §7.1, *Record -- M14*, *Carried into
    Phase 1*; §7.11, *Record -- M21*).  Every comparison of a row with S goes through here,
    so each takes the C step's codes and map.
    """
    def mapped(name, args):
        args = SPEC.twin_arg_map(name, args)
        return args if arg_map is None or args is None else arg_map(name, args)

    return twin_mismatches(s_proj, sec_proj, codes=codes(sec_proj), arg_map=mapped,
                           **kwargs)


def _compare(s_proj, sec_proj, month, exempt, columns=None):
    """Where SEC's row departs from S's point from S month ``month`` on.

    First the frames, ``result_cf`` (over ``columns``, or every column both hold) and
    ``result_pols``, on every column both hold, SEC row ``t`` against S row ``t + month``,
    frames ending together; then every cell of S's but ``exempt``, :data:`REPORTS` and
    :data:`RESIDUALS`, at every argument S cached inside its frame from ``month`` on,
    moved onto SEC's clock, but the keys before the valuation date SEC carries as opening
    state (:func:`_before_valuation`).  Both to 1e-9 relative with no absolute floor
    (USLIB-SEC-PLAN.md §5.2, T2, precised at M11): a floor of 1e-9 passes an error of 1% in
    any value below 1e-7, and survival late in a long frame, and where the cap binds, falls
    below 1e-9.  Then the cells of :data:`RESIDUALS` at the floor of 1e-9: their exact value
    is 0.  Then, on a row in payment, the opening income against S's income of the year
    under way, and the relative index and peak against S's (:func:`_index_faults`).
    Returns the mismatch lines, empty when the row is S's.
    """
    end = sec_proj.proj_len()
    s_end = s_proj.proj_len() - month
    if s_end != end:
        return [f"the frames end apart: S's at t = {s_end - 1} on SEC's clock, SEC's at "
                f"t = {end - 1}"]
    found = []
    for report in REPORTS:
        keep = columns if report == "result_cf" else None
        found += [f"{report}: {line}" for line in frame_mismatches(
            s_proj.cells[report](), sec_proj.cells[report](), t_offset=month,
            columns=keep, atol=0.0)]
    others = exempt | set(REPORTS)
    history = _before_valuation(s_proj, month)
    found += _mismatches(s_proj, sec_proj, t_offset=month, exempt=others | RESIDUALS,
                         arg_map=history, atol=0.0)
    found += _mismatches(s_proj, sec_proj, t_offset=month,
                         exempt=others | (set(s_proj.cells) - RESIDUALS), arg_map=history)
    if month > 0:
        year = max(month - 1, 0) // 12 + 1
        want = s_proj.annual_income(year)
        if not math.isclose(sec_proj.annual_income_init(), want, rel_tol=1e-12,
                            abs_tol=0.0):
            found.append(f"annual_income_init(): SEC {sec_proj.annual_income_init()!r}, S's "
                         f"annual_income({year}) {want!r}")
        found += _index_faults(s_proj, sec_proj, month)
    return found


def _continues_s(s_proj, sec_proj, month):
    """Where a committed row departs from S's point ``s_proj`` from S month ``month`` on.

    The splice's comparison (:func:`_compare`), on the committed model at the shipped
    assumptions.  The shipped 3% expense inflation runs from the start in S and from the
    valuation date here (D7), so :data:`INFLATED`'s columns, and :data:`INFLATION_CELLS`,
    differ by design and are left out; the inflation test holds them.  Every other column
    and cell must agree, to 1e-9 relative, with no absolute floor but on the residuals.
    """
    keep = [c for c in s_proj.result_cf().columns if c not in INFLATED]
    return _compare(s_proj, sec_proj, month, SPLICE_EXEMPT | INFLATION_CELLS, keep)


def _case_id(rates, kind, s_point, month):
    """A case's id: ``point2-d12``, ``point2-k3`` if it starts later, and the set where it
    is not the shipped RPI's, ``rpi_low-point6-d24``."""
    if kind == "future":
        where = f"point{s_point}-k{-month}"
    else:
        where = f"point{s_point}-" + (f"d{month}" if kind == "derived" else f"{kind}{month}")
    return where if rates == "shipped" else f"{rates}-{where}"


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


@pytest.fixture(scope="module")
def sec_read():
    """PA_UK_SEC read in place, as committed, and swept once, cold; what it met.

    The model is first asked for ``duration_mth(500)`` on the twin of S point 1, and the
    keys that call leaves in ``duration_mth`` are kept.  Then every committed point is
    swept (:func:`_sweep`: the reports, the checks that read the frame once and the
    survival check's residual sampled), in table order and each column in ascending ``t``,
    under a recursion limit lowered to
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
                _sweep(projection(model, key))
            except Exception as err:            # kept, so every point is swept
                record["deep"].append(f"point {point_id}: the sweep raised {_raised(err)}")
    finally:
        mx.set_recursion(limit)
    yield model, record
    model.close()


@pytest.fixture(scope="module")
def sec_model(sec_read):
    """PA_UK_SEC read in place, as committed, with every point swept (sec_read)."""
    return sec_read[0]


@pytest.fixture(scope="module")
def s_model():
    """PA_UK_S read in place, as committed, with every point swept.

    T6 regenerates the SEC inputs from it, which would otherwise project every S point
    again (USLIB-SEC-PLAN.md §4, *Carried into Phase 1*), and the in-force tests read S's
    months off it.
    """
    model = mx.read_model(model_path(TWIN), name=_name("s"))
    for key in point_keys(model):
        _sweep(projection(model, key))
    yield model
    model.close()


# How many S points of a splice set are kept swept at once (_Splices.s_point).  A swept S
# point on the table basis holds about 140 MB, most of it modelx's record of what
# PA_UK_S's survival check reads, a product over every month before each time point, so
# that 22 of the shipped set's points swept together held 1.8 GB (measured at M11).  T2 and
# T3 run their cases point by point, so two are enough.
SWEPT = 2


class _Splices:
    """The splice's models, a pair for each of :data:`SPLICE_SETS`, each made when first
    asked for (:meth:`pair`) and closed at the module's end.

    For a set, S is read from a copy of the product directory whose table has the variants
    appended, only the RPI points under the RPI sets, and the set's References are set on
    it.  SEC runs on the same mortality table, and on a model point table of its own, built
    by the generator from the registered spec with its rows replaced by the set's cases this
    run selects, the core or the full grid (:func:`_selected`), out of this S model, so each
    row opens with the state of the very run it is compared with; the set's References are
    set on it too.  No input table moves with ``d``: PA's one valuation-clock input is the
    ``inflation_rate`` Reference.  An S point is swept (:func:`_sweep`) when a case first
    compares a row with it (:meth:`s_point`), and the :data:`SWEPT` most recently compared
    stay swept; each SEC row is projected by the case that compares it and released once
    compared (:func:`_settle`).
    """

    def __init__(self, root):
        self.root, self.pairs, self.swept = root, {}, {}

    def pair(self, rates):
        if rates not in self.pairs:
            refs = SPLICE_SETS[rates]
            points = None if rates == "shipped" else RPI_SET_POINTS
            s = mx.read_model(temp_inputs(self.root / rates / "s", model_path(TWIN),
                                          model_points=_s_table_with_variants(points)),
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
            assert companions == {}
            sec = mx.read_model(_sec_inputs(self.root / rates / "sec", table),
                                name=_name(f"sec_{rates}"))
            for ref, value in refs.items():
                setattr(sec.Projection, ref, value)
            self.pairs[rates], self.swept[rates] = (s, sec), []
        return self.pairs[rates]

    def s_point(self, rates, s_point):
        """S point ``s_point`` of set ``rates``, swept, as a comparison needs it.

        The S space must be swept before a row is compared with it, since the comparison
        reads what S cached (:func:`uk_sec_support.twin_mismatches`).  The :data:`SWEPT`
        points most recently asked for stay swept, and an older one is released, and its
        memory collected, before another is swept: a released point, asked for again, is
        swept afresh.
        """
        s = self.pair(rates)[0]
        key, swept = _key(s, s_point), self.swept[rates]
        if key in swept:
            swept.remove(key)
        else:
            while len(swept) >= SWEPT:
                _release(s, swept.pop(0))
                gc.collect()
            _sweep(projection(s, key))
        swept.append(key)
        return projection(s, key)

    def close(self):
        for s, sec in self.pairs.values():
            sec.close()
            s.close()


@pytest.fixture(scope="module")
def spliced(tmp_path_factory):
    """The splice's models, by set (:class:`_Splices`)."""
    splices = _Splices(tmp_path_factory.mktemp("spliced"))
    yield splices
    splices.close()


@pytest.fixture(scope="module")
def splice_records():
    """What each splice row was found to do, by case (:func:`_settle`)."""
    return {}


# ---------------------------------------------------------------------------
# The splice's records
#
# Each T2 and T3 case scans its row first, on an ItemSpace made for it, and records what
# the rules test and the core grid's reach need of the row; then it compares the row with
# S, and releases it (_settle).  The scan comes first because the comparison evaluates SEC
# cells at S's cached keys, at months and years before the valuation date among them
# (SPIA's *Record — M11*, carried).  Each of the two tests reads the records, and computes
# any case no earlier test has recorded, which keeps it whole when run alone.


def _cached_args(cells):
    """The argument tuple of every key ``cells`` has cached (uk_sec_support._args)."""
    n = len(cells.parameters)
    return [() if n == 0 else (key,) if n == 1 else tuple(key)
            for key in list(cells.keys())]


def _month(x):
    return isinstance(x, int) and not isinstance(x, bool)


def _month_of(node):
    """The month a precedent ``node`` is keyed by, its ``t``, or None if it takes none."""
    params = getattr(node.obj, "parameters", None) or ()
    u = node.args[params.index("t")] if "t" in params else None
    return u if _month(u) else None


def _months_read(node, reach):
    """The calls keyed by a month that precedent ``node`` reads, as ``(reader, cell, month,
    text)``.

    ``node`` itself if it is keyed by ``t``, its reader ``None``.  Otherwise every
    month-keyed call its own precedents read, followed through every call keyed by no
    month, such as ``proj_len()`` or the payments to date on the policy clock, as far as
    the dependency graph goes, each with the call keyed by no month that reads it: so a read
    that looks ahead through a cell taking no ``t`` is the reader's (USLIB-SEC-PLAN.md §5.2,
    T2, precised at M12; ``DIA_US_SEC``'s form).  ``reach`` holds what each call keyed by
    no month reads, so that each is walked once a row, and the walk is a loop, not a
    recursion.
    """
    month = _month_of(node)
    if month is not None:
        return {(None, node.obj.name, month, f"{node.obj.name}{node.args}")}
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
                    found.add((here.obj.name, pred.obj.name, month,
                               f"{here.obj.name}{here.args} -> {pred.obj.name}{pred.args}"))
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


def _closed_reads(proj):
    """The keys before the valuation date an RPI-linked row has asked of the cells keyed on
    the policy clock (USLIB-SEC-PLAN.md §5.2, T2, precised at M7).

    On RPI-linked escalation the income, the index and the payments before the valuation
    instant are history, held in the opening state, so no cell may ask ``annual_income`` a
    year before the one under way, ``rpi_index`` or ``rpi_peak`` an anniversary before
    the one that opened it, or ``cum_annuity_pp``, ``annuity_pp_pm`` or ``is_payment_pm`` a
    policy month before the valuation date's, nor the cells the C step adds on that clock,
    the income's and the payments' refusals and the payments' opening of a policy year at
    or before the valuation date's key.  On level and fixed escalation the schedule
    is the contract's, which one loop at the valuation date's key sums, R2's admitted read.
    """
    if not (proj.is_lpi5() or proj.is_rpi_catchup()):
        return []
    d = max(proj.duration_mth_init(), 0)
    y0 = proj.policy_year_init()
    bounds = {"annual_income": y0, "rpi_index": y0 - 1, "rpi_peak": y0 - 1,
              "cum_annuity_pp": d, "annuity_pp_pm": d, "is_payment_pm": d,
              "annual_income_refusal": y0, "cum_annuity_pp_refusal": d,
              "cum_annuity_pp_py": d // 12 + 2}
    return [f"{name}{args}" for name, low in bounds.items()
            for args in _cached_args(proj.cells[name])
            if args[0] < low and not (name == "cum_annuity_pp" and args[0] <= 0)]


def _rule_breaches(proj):
    """R1 and R2's look-ahead on one row, once it has run whole.

    The row's reports and every check are run (:func:`uk_sec_support.sweep`), the whole
    survival check among them, and then every monthly cell at every month of the frame and
    the month after it, as the C step's sweep runs them (:func:`uk_sec_support.full_sweep`):
    no report of a row need read every state, and a base at ``t == 0`` would hide in a cell
    the reports leave unread (USLIB-SEC-PLAN.md §5.2, T2, precised at M4).  ``{"negative":
    [...], "early": [...], "ahead": [...], "closed": [...], "raised": [...], "checks":
    [...]}``: every cached call with a negative argument; every call keyed by a month
    before ``t_entry()`` that a call keyed by a month at or after it reads; every call keyed
    by a month beyond ``t + 1`` that a call keyed by ``t`` reads, but :data:`LOOK_AHEAD`'s;
    every key before the valuation date an RPI-linked row asked (:func:`_closed_reads`);
    every call the full sweep found raising; and every check that does not hold.  The row is
    released once read, so its quadratic survival check is held a row at a time.  A call
    reads its precedents, as modelx's dependency graph records them, and, through a
    precedent keyed by no month, whatever that precedent reads in turn
    (:func:`_months_read`).
    """
    checks = [name for name, value in sweep(proj).items()
              if name.startswith("check_") and value is not True]
    raised = [f"{name}{args}: {text}" for (name, args), text in full_sweep(proj).items()]
    entry, end = proj.t_entry(), proj.proj_len()
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
                for reader, cell, u, text in sorted(_months_read(node, reach),
                                                    key=lambda r: (r[2], r[3])):
                    if u < entry <= t:
                        early.append(f"{name}{args} -> {text}")
                    if u <= t + 1 or ((reader, cell) in LOOK_AHEAD and u <= end):
                        continue
                    ahead.append(f"{name}{args} -> {text}")
    return {"negative": negative, "early": early, "ahead": ahead,
            "closed": _closed_reads(proj), "raised": raised, "checks": checks}


def _vp_paid(x, t):
    """The month's value-protection payment per contract in force, before the count."""
    return x.claims(t, _code(x, "VP"))


# What test_the_core_grid_reaches_every_branch asks of the core's rows in the model's own
# values, which no column of the table shows: each holds of some core row, or of a core row
# in some month of its frame.  At the valuation date, each opening-state column in use: a
# life dead in the opening state, each; survival a probability strictly between 0 and 1;
# payments carried in; and on RPI-linked escalation an income past the first year's, a peak
# above the index and the annuitant's payments carried in.  Later in the frame, every branch
# and both sides of each min and max the full grid reaches: the guarantee's floor binding
# and lifted, the overlap gate shut and open, the dependant paid, value protection paid and
# run out, the proportionate payment paid and past the frame, the LPI's cap, floor and
# between, the ratchet frozen and rising, the mortality cap, an age past the limiting age,
# the improvement flat, tapering and spent, the obligation measure's cap binding and not,
# its dependant's leg dropped, and the frame's two ends.
AT_VALUATION = {
    "the annuitant dead in the opening state": lambda x: (
        x.duration_mth_init() > 0 and x.lives_if_init(1) == 0.0),
    "the dependant dead in the opening state": lambda x: (
        x.duration_mth_init() > 0 and x.is_joint() and x.lives_if_init(2) == 0.0),
    "survival a probability in the opening state": lambda x: (
        0.0 < x.lives_if_init(1) < 1.0),
    "payments carried in": lambda x: x.cum_annuity_all_init() > 0.0,
    "an RPI-linked income past the first year's": lambda x: (
        (x.is_lpi5() or x.is_rpi_catchup()) and x.duration_mth_init() > 12
        and x.annual_income_init() != x.annual_income_first()),
    "a peak above the index": lambda x: x.is_rpi_catchup() and x.rpi_peak_init() > 1.0,
    "the annuitant's payments carried in": lambda x: (
        (x.is_lpi5() or x.is_rpi_catchup()) and x.vp_pct() > 0.0 and x.is_first_death()
        and x.cum_annuity_pp_init() > 0.0),
    "valued on an anniversary": lambda x: (
        x.duration_mth_init() > 0 and x.duration_mth_init() % 12 == 0),
    "valued inside the guarantee": lambda x: (
        0 < x.duration_mth_init() < x.guarantee_mths()),
    "valued past the guarantee": lambda x: (
        0 < x.guarantee_mths() <= x.duration_mth_init()),
    "value protection apart from the dependant's share": lambda x: (
        x.vp_pct() > 0.0 and x.is_joint() and x.vp_pct() != x.dependant_pct()),
    "value protection on a single life": lambda x: x.vp_pct() > 0.0 and not x.is_joint(),
    "a dependant older than the annuitant": lambda x: (
        x.is_joint() and x.age_at_entry(2) > x.age_at_entry(1)),
    "a fixed escalation apart from the RPI": lambda x: (
        x.is_fixed() and x.escalation_rate() != x.rpi_rate),
}
IN_FRAME = {
    "the guarantee's floor paying past survival": lambda x, t: (
        x.certain_floor(t) == 1.0 and x.payment_factor_life(t) < 1.0
        and x.annuity_pp(t) > 0.0),
    "the floor lifted": lambda x, t: (
        x.is_active(t) and x.guarantee_mths() > 0 and x.certain_floor(t) == 0.0),
    "the overlap gate shut": lambda x, t: (
        x.is_joint() and x.is_active(t) and x.overlap_gate(t) == 0.0
        and x.lives_if(x.payment_surv_mth(t), 2) > 0.0
        and x.lives_if(x.payment_surv_mth(t), 1) < 1.0),
    "the overlap gate open with overlap": lambda x, t: (
        x.overlap() and x.certain_floor(t) == 1.0 and x.dependant_factor(t) > 0.0
        and x.annuity_pp(t) > 0.0),
    "the dependant paid": lambda x, t: (
        x.dependant_factor(t) > 0.0 and x.annuity_pp(t) > 0.0),
    "value protection paid on the first death": lambda x, t: (
        x.vp_pct() > 0.0 and x.is_first_death() and _vp_paid(x, t) > 0.0),
    "value protection paid on the last death": lambda x, t: (
        x.vp_pct() > 0.0 and not x.is_first_death() and _vp_paid(x, t) > 0.0),
    "value protection run out": lambda x, t: (
        x.vp_pct() > 0.0 and x.is_active(t) and x.vp_balance(t) == 0.0),
    "value protection netting an advance instalment": lambda x, t: (
        x.vp_pct() > 0.0 and not x.is_arrears() and x.is_payment_mth(t)
        and _vp_paid(x, t) > 0.0),
    "last-survivor value protection netting an advance instalment": lambda x, t: (
        x.vp_pct() > 0.0 and not x.is_first_death() and not x.is_arrears()
        and x.is_payment_mth(t) and _vp_paid(x, t) > 0.0),
    "the proportionate payment": lambda x, t: (
        x.proportion() and x.claims(t, _code(x, "PROP")) > 0.0),
    "a payment month": lambda x, t: x.is_payment_mth(t),
    "a month between payments": lambda x, t: (
        x.is_active(t) and not x.is_payment_mth(t)),
    "the LPI cap binding": lambda x, t: (
        x.is_lpi5() and x.is_active(t) and x.rpi_rate > x.esc_lpi_cap),
    "the LPI floor binding": lambda x, t: (
        x.is_lpi5() and x.is_active(t) and x.rpi_rate < 0.0),
    "the LPI between its bounds": lambda x, t: (
        x.is_lpi5() and x.is_active(t) and 0.0 <= x.rpi_rate <= x.esc_lpi_cap),
    "the ratchet frozen": lambda x, t: (
        x.is_rpi_catchup() and x.is_active(t) and x.duration(t) >= x.policy_year_init()
        and x.rpi_index(x.duration(t)) < x.rpi_peak(x.duration(t) - 1)),
    "the ratchet rising": lambda x, t: (
        x.is_rpi_catchup() and x.is_active(t) and x.duration(t) >= x.policy_year_init()
        and x.rpi_index(x.duration(t)) > x.rpi_peak(x.duration(t) - 1)),
    "the mortality cap binding": lambda x, t: (
        x.is_active(t) and not x.is_scenario() and x.mort_rate(t, 1) == 1.0
        and x.age(t, 1) < x.omega_age),
    "an age past the limiting age": lambda x, t: (
        x.is_active(t) and not x.is_scenario() and x.age(t, 1) >= x.omega_age),
    "the improvement flat": lambda x, t: (
        x.is_active(t) and not x.is_scenario()
        and x.improve_rate(t, 1) == x.improve_rate_base),
    "the improvement tapering": lambda x, t: (
        x.is_active(t) and not x.is_scenario()
        and 0.0 < x.improve_rate(t, 1) < x.improve_rate_base),
    "the improvement spent": lambda x, t: (
        x.is_active(t) and not x.is_scenario() and x.improve_rate(t, 1) == 0.0),
    "the obligation's cap binding": lambda x, t: (
        x.dependant_pct() > 0.0 and x.certain_floor(t) == 1.0
        and x.lives_if(t + 1, 1) < 1.0 and x.lives_if(t + 1, 2) > 0.0),
    "the obligation's dependant leg dropped": lambda x, t: (
        x.is_joint() and x.is_active(t) and x.dependant_pct() == 0.0
        and x.lives_if(t + 1, 1) < 1.0 and x.lives_if(t + 1, 2) > 0.0),
    "the frame ending at the age stop": lambda x, t: (
        t == x.proj_len() - 1 and x.stop_mth() == x.horizon_mths()),
    "the frame ending at the guarantee": lambda x, t: (
        t == x.proj_len() - 1 and x.stop_mth() > x.horizon_mths()),
}


def _branches(x):
    """The names in :data:`AT_VALUATION` and :data:`IN_FRAME` that hold of row ``x``."""
    reached = {what for what, holds in AT_VALUATION.items() if holds(x)}
    frame = range(x.t_entry(), x.proj_len())
    return reached | {what for what, holds in IN_FRAME.items()
                      if any(holds(x, t) for t in frame)}


def _scan(records, case, proj):
    """Record what the rules and the core grid's reach need of a row, on an ItemSpace that
    has computed nothing else yet.

    The record is :func:`_rule_breaches`'s, with the row's :func:`_branches`, and a row that
    raises is recorded as raising, which the rules test reports.
    """
    try:
        record = _rule_breaches(proj)
        record["branches"] = _branches(proj)
        record["failed"] = None
    except Exception as err:                    # recorded, and reported by the rules test
        record = {"negative": [], "early": [], "ahead": [], "closed": [], "raised": [],
                  "checks": [], "branches": set(), "failed": _raised(err)}
    records[case] = record
    return record


def _settle(records, case, model, key):
    """Scan a row afresh if no case has, and release it (:func:`_scan`)."""
    try:
        if case not in records:
            if key in model.Projection.itemspaces:
                _release(model, key)
            _scan(records, case, projection(model, key))
    finally:
        _release(model, key)
    return records[case]


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
    nowhere else, because on a point starting at ``t = 0`` the two clocks coincide and the
    opening state is the start date's.  For the same reason it is the test that catches a
    policy month passed as ``t`` (R1a), a scenario death read on the wrong clock, and a
    look-back that stops at the wrong month.  The frame comparisons read SEC row ``t``
    against S row ``t + d`` in every column of ``result_cf`` and every column of
    ``result_pols`` both hold, and fail frames that end apart.  The cell comparison then
    evaluates every cell of S's but :data:`SPLICE_EXEMPT`, at every argument S cached inside
    its own frame from month ``d`` on, moved onto SEC's clock: survival, the payments to
    date on both clocks, the value-protection balance, the floors and factors, the income
    and the residuals among them, but the keys before the valuation date that SEC carries as
    opening state (:func:`_compare`).  Each compares to 1e-9 relative with no absolute floor
    but the residuals.  The opening income is held to S's of the year under way, and the
    relative index and peak to S's.  An S cell this model lacked would fail it.

    The row is first scanned for the rules test, on an ItemSpace made for it, then
    compared, then released (:func:`_scan`, :func:`_settle`).
    """
    sec = spliced.pair(rates)[1]
    key = _row_key(sec, kind, s_point, month)
    if key in sec.Projection.itemspaces:
        _release(sec, key)
    case = (rates, kind, s_point, month)
    try:
        _scan(splice_records, case, projection(sec, key))
        s_proj = spliced.s_point(rates, s_point)
        sec_proj = projection(sec, key)
        assert _compare(s_proj, sec_proj, month, SPLICE_EXEMPT) == []
    finally:
        _settle(splice_records, case, sec, key)


# ---------------------------------------------------------------------------
# T3 -- future new business


@pytest.mark.parametrize(
    "rates, s_point, k",
    [_case(case, CORE_FUTURES, _case_id(case[0], "future", case[1], -case[2]))
     for case in FUTURES])
def test_future_new_business_is_the_s_projection_k_months_on(spliced, splice_records,
                                                             rates, s_point, k):
    """Starting k months after the valuation date, the point is S's projection k months on.

    SEC rows ``k ..`` are S rows ``0 ..``, ending together at the stop rule, in
    ``result_cf`` and ``result_pols``, and every cell of S's but :data:`FUTURE_EXEMPT`
    agrees at every argument S cached inside its own frame, moved ``k`` later: the policy
    clock's keys, the payments to date, the income and the index, need no move.  Each
    compares as the splice compares, with no absolute floor but on the residuals
    (:func:`_compare`).  Before the start every column of ``result_cf`` and
    ``result_pols`` is an exact zero, and the contracts arrive in month ``k`` as new
    business.

    The last assertions are R1 and D4's base rule made testable.  After the reports, no
    mortality rate, no read keyed by a policy year, an age or a calendar year has been
    evaluated at a month before the start.  A survival recursion based at ``t == 0``
    rather than at ``t_entry()``, or a rate evaluated before the month is asked whether it
    is in the frame, still gives the right numbers.

    The pre-start rows are asserted present before they are asserted zero, in every
    report: a frame that opened at the start would have none, its zeros would hold of
    nothing, and the comparisons with S, which start at the start, would not see it.  The
    row is first scanned for the rules test, then compared, then released.
    """
    sec = spliced.pair(rates)[1]
    key = _row_key(sec, "future", s_point, -k)
    if key in sec.Projection.itemspaces:
        _release(sec, key)
    case = (rates, "future", s_point, -k)
    try:
        _scan(splice_records, case, projection(sec, key))
        _release(sec, key)
        s_proj = spliced.s_point(rates, s_point)
        sec_proj = projection(sec, key)
        frames = {name: sec_proj.cells[name]() for name in REPORTS}
        assert _compare(s_proj, sec_proj, -k, FUTURE_EXEMPT) == []
        for report, frame in frames.items():
            assert list(frame.index[:k]) == list(range(k)), report
            assert (frame.loc[:k - 1] == 0.0).all().all(), report
        assert sec_proj.pols_new_biz(k) == sec_proj.policy_count() == 1.0
        early = {}
        for name in ("mort_rate", "mort_rate_base", "improve_rate", "improve_factor",
                     "age", "calendar_year", "duration", "policy_year"):
            months = sorted(args[0] for args in _cached_args(sec_proj.cells[name])
                            if args[0] < k)
            if months:
                early[name] = months
        assert not early, f"rates evaluated before the start: {early}"
    finally:
        _settle(splice_records, case, sec, key)


# ---------------------------------------------------------------------------
# D11's R1 and R2, and D3's closed-form clock


@pytest.mark.parametrize("grid", [pytest.param("core", id="core"),
                                  pytest.param("full", id="full", marks=FULL_ONLY)])
def test_no_cell_is_called_before_the_valuation_date_or_reads_far_ahead(spliced,
                                                                        splice_records,
                                                                        grid):
    """R1, its look-back and R2's look-ahead, on the rows T2 and T3 compare: core or rest.

    Each is a rule of how the model computes, not of what, so no number shows a breach,
    and on a point starting at ``t = 0`` the two clocks coincide and hide it from T1 too.
    The splice's rows are points in payment at every month T2 names, the variants and the
    RPI sets among them, and points starting later, and on each the reports, the checks and
    the full sweep are run first (:func:`_rule_breaches`):

    * R1: no cell holds a negative argument.  modelx evaluates one without complaint, and a
      compiled cache raises ``IndexError`` below 0 (USLIB-SEC-PLAN.md F4).  A policy month
      turned into ``t`` by subtracting ``duration_mth_init()`` (R1a) goes negative on a
      point in payment past it.
    * R1's look-back stops at ``t_entry()``: no cell evaluated at a month from
      ``t_entry()`` on read a month before it, directly or through a cell keyed by no
      month.  On a point starting later a recursion based at ``t == 0`` reads the pre-start
      zeros, so no number need show it and no argument goes negative.
    * R2's look-ahead: no cell evaluated at month ``t`` read a cell keyed by a month beyond
      ``t + 1``, as modelx's dependency graph records each cached call's precedents and
      through every precedent keyed by no month (:data:`LOOK_AHEAD` admits none).
    * On an RPI-linked row no cell asked a year, an anniversary or a policy month before
      the valuation date of the cells keyed on the policy clock (:func:`_closed_reads`):
      that history is the opening state's.
    * No call of the full sweep raised, and every check holds, the whole survival check
      among them, which the module's sweeps sample (:func:`_sweep`).

    Each row was scanned by the T2 or T3 case that compared it, before the comparison
    (:func:`_scan`), and a row no case has scanned is scanned here.  The core case covers
    the core's rows, the full case every other row of the full grid, with
    ``UKLIB_SEC_FULL=1``.  The new-business twins in the splice's tables are no case's, and
    are left out: on them the clocks coincide, and T1 compares them with S cell by cell.
    """
    cases = [case for case in GRID if (case in CORE_GRID) == (grid == "core")]
    negative, early, ahead, closed, raised, failed = [], [], [], [], [], []
    checks = []
    for case in cases:
        record, where = _record_of(spliced, splice_records, case), _case_id(*case)
        negative += [f"{where}: {call}" for call in record["negative"]]
        early += [f"{where}: {read}" for read in record["early"]]
        ahead += [f"{where}: {read}" for read in record["ahead"]]
        closed += [f"{where}: {read}" for read in record["closed"]]
        raised += [f"{where}: {call}" for call in record["raised"]]
        checks += [f"{where}: {name}" for name in record["checks"]]
        if record["failed"]:
            failed.append(f"{where}: {record['failed']}")
    assert cases, f"the {grid} grid has no rows"
    assert not failed, f"rows that raised: {failed[:10]}"
    assert not raised, f"calls the full sweep found raising: {raised[:10]}"
    assert not checks, f"checks that do not hold: {checks[:10]}"
    assert not negative, f"called before the valuation date: {negative[:10]}"
    assert not early, f"read before the start from the books: {early[:10]}"
    assert not ahead, f"read beyond t + 1: {ahead[:10]}"
    assert not closed, f"asked history the opening state holds: {closed[:10]}"


def test_the_policy_clock_is_a_closed_form_and_no_recursion_runs_backward(sec_read):
    """D3 and R2's recursions, on the committed model as it was first swept, cold.

    Both need a model on which nothing had been evaluated yet, which is what the fixture
    held when it made the record asserted here:

    * D3: the policy clock is the closed form.  Called first, ``duration_mth(500)``
      evaluates ``duration_mth`` once, where ``BasicTerm_SE``'s recursion would evaluate it
      at all 501 months from 0.
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


# modelx warns as its stack trace starts and stops, which the test uses to count a depth.
@pytest.mark.filterwarnings("ignore:call stack trace:UserWarning")
def test_the_schedules_are_based_at_the_valuation_dates_key(sec_model, s_model):
    """The payments to date and the income are based at static keys, read in one loop.

    ``cum_annuity_pp`` on the policy clock is based at ``max(duration_mth_init(), 0)``,
    and ``annual_income`` at ``policy_year_init()``, the year under way before any
    month-0 anniversary, keys that read no clock (USLIB-SEC-PLAN.md R2, precised at M12).
    On level and fixed escalation one loop there sums, or compounds, the contract's
    schedule in ``PA_UK_S``'s order, so every key is S's to the last bit, before the base
    and after it, on the table basis's joint point restated at 101 and at 635.  And a
    contract valued late reads its balance without recursing back to its start: on the one
    at 635, a one-row frame, every cell its reports evaluate, called cold, runs within
    :data:`LATE_DEPTH` cells of the report, where ``PA_UK_S``'s ``G(636)`` runs a chain of
    636.  On RPI-linked escalation the base is the opening state, the history: the
    catch-up point's annuitant payments to date at 60 open at 27,000, five years of a
    frozen 5,400.
    """
    table = sec_model.Data.model_point_table()
    for month in (101, 635):
        label = _label(table, "derived", 2, month)
        p, s = _point(sec_model, label), _point(s_model, 2)
        for k in range(1, month + 2):
            assert (p.cum_annuity_pp(k, _code(p, "ANNUITANT"))
                    == s.cum_annuity_pp(k, "ANNUITANT")), (label, k)
        for y in range(1, p.policy_year(0) + 1):
            assert p.annual_income(y) == s.annual_income(y), (label, y)
    fresh = mx.read_model(model_path(SEC), name=_name("late"))
    try:
        late = _point(fresh, _label(table, "derived", 2, 635))
        mx.start_stacktrace(maxlen=None)
        try:
            late.result_cf()
            late.result_pols()
            trace = mx.get_stacktrace(summarize=False)
        finally:
            mx.stop_stacktrace()
        level = deepest = 0
        for event, *_ in trace:
            level += 1 if event == "ENTER" else -1
            deepest = max(deepest, level)
        assert deepest <= LATE_DEPTH, deepest
    finally:
        fresh.close()
    frozen = _point(sec_model, _label(table, "derived", 6, 60))
    assert (frozen.cum_annuity_pp(60, _code(frozen, "ANNUITANT"))
            == frozen.cum_annuity_pp_init() == 27000.0)


# How deep the reports of a contract valued in its last month run, called cold: 10 cells,
# the report, the obligation measure and survival at the frame's closing time point, which
# opens a policy year, so the year's opening, lives_if_py, which reads the first month's
# monthly rate, the annual rate, the improvement factor, the calendar year, the start year
# and its Data vector (measured at M12; 8 at M11, before the survival recursion was
# blocked by policy year and the model point's columns were read as Data vectors).
LATE_DEPTH = 10

# How deep a cold call may run beyond its chain (_chain): the cells above the chain's
# first cell and those below its foot, the first month's rates and Data's first reads of
# its tables.  Every monthly cell, at every code, called cold alone, before anything else
# on a read of its own, in the last month of each shape's longest cover, now and 120
# months on, runs at most 12 cells beyond its chain: the payments to date on every stream,
# their refusal and the claims total 12 on the table basis, the last-death density 11,
# survival's and its densities 10, and net_cf 5 to 10 (measured at M12).  The bound is the
# measure, met with no margin, as ULB_UK_SEC's 16 is (UKLIB-SEC-PLAN.md §6.6, *Record --
# M10*): blocked by policy year, a chain's first cell sits one cell from its head, and at
# its foot the walk's first month reads the year before's opening and the table's first
# rate, as one cell a month's did, so the walk adds nothing to M11's 12.  A chain left one
# cell a month runs about 1,140 cells past it, and one walked descending the same.
CHAIN_OVERHEAD = 12

# The contract's longest cover, held by proj_len() and the mortality table: at its largest
# limiting age, OMEGA_MAX, omega_age_max as shipped, 116, the mortality table's last age
# plus one, which proj_len() admits on the table basis and the caches are sized from, a
# frame of 12 x (OMEGA_MAX - issue_age_min) = 1,392 months from the start.  On the
# scenario basis, which reads no mortality, every covered life issued at issue_age_min, 0,
# reaches it by the age stop.  On the table basis, which reads the table from the issue
# age on, a life issued at its first age, 50, stops at 792 months, and the frame reaches
# 1,392 by a guarantee of that length, which proj_len() accepts at that limiting age.
# Each issued now, and with UKLIB_SEC_FULL=1 future_horizon_mth, 120 months, on too
# (DEPTH_DELAYS); each with omega_age set to OMEGA_MAX on the model that projects it.
OMEGA_MAX = 116
YOUNGEST = {"scenario": 0, "table": 50}
LONGEST = 12 * OMEGA_MAX

# Each shape and the chains it runs, called cold in the last month of the frame at its own
# longest cover, each on a read of its own: (the S point whose twin it is, its basis, its
# guarantee, the chain heads, each a (cell, its arguments beyond the month)).  On the
# scenario basis survival is a step function, so the chains are the payments to date: the
# worked example reads the annuitant's, on the policy clock, through first-death value
# protection, and the last-survivor point the expected payments on both streams, on the
# valuation clock.  On the table basis survival recurses too, and the obligation measure,
# the reports and the survival check read it, through a guarantee to the longest frame:
# the worked example's table twin, the RPI catch-up and the LPI, whose income recurses by
# the year and whose payments to date are the annuitant's; and the rated single life,
# which the cap kills long before its guarantee ends.
SCENARIO_HEADS = (("net_cf", ()), ("vp_balance", ()), ("claims", ("VP",)),
                  ("cum_annuity_all", ()))
TABLE_HEADS = (("net_cf", ()), ("pols_if", ()), ("vp_balance", ()),
               ("cum_annuity_all", ()), ("check_lives_roll_fwd_resid", ()),
               ("claims", ("VP",)), ("lives_if", (1,)), ("lives_if", (2,)))
SINGLE_HEADS = (("net_cf", ()), ("pols_if", ()), ("cum_annuity_all", ()),
                ("check_lives_roll_fwd_resid", ()), ("lives_if", (1,)))
SHAPES = ((1, "scenario", 0, SCENARIO_HEADS), (10, "scenario", 0, SCENARIO_HEADS),
          (2, "table", LONGEST, TABLE_HEADS), (6, "table", LONGEST, TABLE_HEADS),
          (7, "table", LONGEST, TABLE_HEADS), (8, "table", LONGEST, SINGLE_HEADS))

# How deep each shape's deepest chain head runs, called cold in the last month of its
# longest cover, by S point (measured at M12), issued now and, as deep, 120 months on: the
# chain of CHAIN cells back to t_entry(), 11 within the last policy year and two in each
# of the 115 before it, 241, and 8 to 12 cells more.  The deepest, DEEPEST_SHAPE's, the
# payments to date on every stream on the table basis under a 1,392-month guarantee, 253
# cells, as deep on points 6, 7 and 8, is the chain the compiled stack test runs.  At the
# shipped limiting age, 115, one cell a month it ran 1,391 cells, net_cf on the same shapes,
# which the in-force step measured (UKLIB-SEC-PLAN.md §6.7, *Record -- M11*), and compiled
# it needed 244 to 276 KiB of C stack (*Record -- M12*); blocked, 251 cells and 52 to 76 KiB.
CHAIN = 11 + 2 * (LONGEST // 12 - 1)
SHAPE_DEPTHS = {1: 249, 10: 250, 2: 253, 6: 253, 7: 253, 8: 253}
DEEPEST_SHAPE = 2
DEEPEST = SHAPE_DEPTHS[DEEPEST_SHAPE]

# When the shapes are issued, months after the valuation date: now by default, and 120
# months on, the shipped future_horizon_mth, with UKLIB_SEC_FULL=1 alone, since its chains
# run as deep as now's (test_every_chain_runs_one_cell_a_month_from_a_cold_start) and
# would double the test's time.
DEPTH_DELAYS = (pytest.param(0, id="now"),
                pytest.param(120, id="120-months-on", marks=(
                    pytest.mark.sec_full,
                    pytest.mark.skipif(not SEC_FULL, reason="the shapes issued 120 months "
                                       "on run as deep as now's, and run with "
                                       "UKLIB_SEC_FULL=1 (UKLIB-SEC-PLAN.md U6)"))))


def _chain(p, t):
    """The cells a cold read of month or time point ``t`` of ``p`` runs through, past the
    first: one a month back to its policy year's first, or to ``t_entry()`` in the year
    that holds it, and two a policy year before that, back to ``t_entry()``'s year, where
    survival and the payments to date are blocked by policy year (``lives_if_py``,
    ``cum_annuity_all_py``, ``cum_annuity_pp_py``)."""
    first = max(p.t_entry(), t - p.duration_mth(t) % 12)
    return (t - first) + 2 * (p.policy_year(t) - p.policy_year(p.t_entry()))


def _cold_calls(tmp_path, k, year_heads=()):
    """Each chain head of :data:`SHAPES` at its longest cover, issued ``k`` months after the
    valuation date, and each of ``year_heads``, called cold in the last month of its frame,
    each on a read of its own and first, under modelx's stack trace: ``[(label, S point,
    cell, its arguments, whether it is a year head, (proj_len(), t_entry()) and the frame
    and entry expected, the chain, the cells on the stack where the call ran deepest)]``,
    each cell as ``(space, name)`` (:func:`_deepest_stack`).  How deep a call ran is that
    stack's length."""
    folder, frames = _longest_cover(tmp_path, k)
    by_point = {}
    for s_point, cell, extra in year_heads:
        by_point.setdefault(s_point, []).append((cell, extra))
    calls = []
    for label, months, entry, heads, s_point in frames:
        for year_head, (cell, extra) in [*((False, h) for h in heads),
                                         *((True, h) for h in by_point.get(s_point, ()))]:
            fresh = mx.read_model(folder, name=_name("cold"))
            try:
                fresh.Projection.omega_age = OMEGA_MAX
                p = _point(fresh, label)
                last = months - 1
                args = (last, *(_code(p, a) if isinstance(a, str) else a for a in extra))
                stack = _deepest_stack(p, cell, args)
                calls.append((label, s_point, cell, args, year_head,
                              ((p.proj_len(), p.t_entry()), (months, entry)),
                              _chain(p, last), stack))
            finally:
                fresh.close()
    return calls


@pytest.fixture(scope="module")
def cold_now(tmp_path_factory):
    """:func:`_cold_calls` issued now, with :data:`YEAR_HEADS`, read once for the module:
    the depth test and the chain-text test read the same cold calls."""
    return _cold_calls(tmp_path_factory.mktemp("cold_now"), 0, YEAR_HEADS)


def _longest_cover(tmp_path, k):
    """A copy whose table holds each of :data:`SHAPES` at its longest cover: the twin of
    its S point with every covered life issued at :data:`YOUNGEST` on its basis, ``k``
    months after the valuation date, each frame the one it has under an ``omega_age`` of
    :data:`OMEGA_MAX`, which whoever reads the copy sets.  ``(folder, [(label, frame,
    t_entry, heads, S point)])``."""
    committed = _committed()
    rows, frames = [], []
    top = committed.index.max()
    for s_point, basis, guarantee, heads in SHAPES:
        twin = _label(committed, "twin", s_point, 0)
        age = YOUNGEST[basis]
        assert committed.at[twin, "mort_basis"] == basis, s_point
        top += 1
        row = committed.loc[[twin]].assign(annuitant_age=age, duration_mth=-k,
                                           guarantee_months=guarantee)
        if str(row["dependant_present"].iloc[0]) == "True":
            row = row.assign(dependant_age=age)
        row.index = pd.Index([top], name="point_id")
        rows.append(row)
        frames.append((top, max(12 * (OMEGA_MAX - age), guarantee) + k, k, heads,
                       s_point))
    return _sec_inputs(tmp_path, pd.concat(rows)), frames


# modelx warns as its stack trace starts and stops, which is all the test does with it.
@pytest.mark.filterwarnings("ignore:call stack trace:UserWarning")
@pytest.mark.parametrize("k", DEPTH_DELAYS)
def test_every_chain_runs_one_cell_a_month_from_a_cold_start(tmp_path, k, cold_now):
    """Called cold, each chain runs one cell a month within its policy year, and two cells a
    year before it, back to ``t_entry()``, no more (D5, as blocked at M12).

    No number shows how deep a chain runs, and a compiled model runs it on the C stack, so a
    chain of two cells a month, which gives the same numbers, needs twice the stack on every
    platform (F7); ``PA_UK_S``'s payments to date recurse from the start, however old the
    contract.  One cell a month, this model's ran 1,391 cells at the longest cover, and
    compiled needed 244 to 276 KiB of C stack, past what the C step allows
    (UKLIB-SEC-PLAN.md §6.7, *Record -- M12*).  So survival and the payments to date are
    blocked by policy year, each year's opening a cell that walks the year before in
    ascending order (``lives_if_py``, ``cum_annuity_all_py``, ``cum_annuity_pp_py``).  On a
    model just read, nothing is cached, so modelx's stack trace counts how deep a call runs,
    against that chain (:func:`_chain`) and :data:`CHAIN_OVERHEAD` more, with modelx's
    recursion limit where the module leaves it: each chain head of each of :data:`SHAPES`,
    in the last month of the frame, each on a read of its own and called first.  At each
    shape's longest cover, 1,392 months from the start at the contract's largest limiting
    age, :data:`OMEGA_MAX`, every life issued at the youngest age its basis projects, and on
    the table basis a guarantee to that month (:func:`_longest_cover`), issued ``k`` months
    after the valuation date; each row's frame is asserted after.  Issued now, the calls are
    the module's :func:`cold_now`, which the chain-text test reads too.  Each shape's
    deepest call is its measure in :data:`SHAPE_DEPTHS`, so that a shape left out, or a
    chain grown, fails here; the deepest of all, :data:`DEEPEST_SHAPE`'s, is the longest
    chain the compiled stack test runs.  A chain left one cell a month runs about 1,140
    cells past the bound, and one walked descending the same.

    Issued 120 months on, each chain runs as deep as issued now, and the same measures
    hold, so those rows run with ``UKLIB_SEC_FULL=1`` alone (:data:`DEPTH_DELAYS`).  The
    later row runs the same cells over the same policy months, 120 months later on the
    valuation clock: improvement, the income and the schedules are dated on the policy
    clock, and inflation, the one cell the valuation clock dates, is a closed form outside
    every chain, read once by the month's expense.
    """
    calls = cold_now if k == 0 else _cold_calls(tmp_path, k)
    found, deepest = [], {}
    for label, s_point, cell, args, year_head, (frame, expected), chain, stack in calls:
        if year_head:
            continue
        depth = len(stack)
        deepest[s_point] = max(deepest.get(s_point, 0), depth)
        assert frame == expected, label
        assert chain == CHAIN == 241, (label, chain)
        if not chain <= depth <= chain + CHAIN_OVERHEAD:
            found.append(f"point {label}: {cell}{args} cold runs {depth} cells deep, where "
                         f"its chain back to t_entry(), one cell a month within its policy "
                         f"year and two a year before it, is {chain} and {CHAIN_OVERHEAD} "
                         f"more are allowed")
    assert not found, found
    assert deepest == SHAPE_DEPTHS, deepest
    assert max(deepest.values()) == deepest[DEEPEST_SHAPE] == DEEPEST


def test_each_blocked_chain_opens_a_year_with_its_own_float(sec_model):
    """Each chain blocked by policy year opens a year with the month before's own step,
    bit for bit, and reads no other way (§6.7, *Record -- M12*).

    A cold read of survival or of the payments to date runs one cell a month within its
    year and two a year before it, the depth test above shows, because in the first time
    point or key of a policy year after the chain's base each reads the year's opening,
    which walks the year before.  So the forms must give one value: on every committed
    point, at every time point of the frame and its close that opens a policy year after
    ``t_entry()``, ``lives_if_py(y, life)`` is ``l(t - 1)(1 - q_m(t - 1))``, survival's
    inline step from the time point before, bit for bit, on the table basis, and
    ``cum_annuity_all_py(y)`` the payments' inline step; and at every key past the
    valuation date's that opens a policy year, ``cum_annuity_pp_py(y)`` is ``G(k - 1) +
    inst(k - 1)``.  And as modelx's dependency graph records them, each chain's cell reads
    its opening there and not its own value of the time point or key before, and reads that
    value within a year.  The openings are asserted many, on every basis that reads them.
    """
    table = sec_model.Data.model_point_table()
    openings = {"lives_if_py": 0, "cum_annuity_all_py": 0, "cum_annuity_pp_py": 0}
    annuitant = _code(sec_model.Projection, "ANNUITANT")
    for key, point_id in zip(point_keys(sec_model), table.index):
        p = projection(sec_model, key)
        entry, end = p.t_entry(), p.proj_len()
        lives = (1, 2) if p.is_joint() else (1,)
        for t in range(entry + 1, end + 1):
            y = p.policy_year(t)
            opens = p.duration_mth(t) % 12 == 0
            if not p.is_scenario():
                for life in lives:
                    step = p.lives_if(t - 1, life) * (1.0 - p.mort_rate_mth(t - 1, life))
                    assert p.lives_if(t, life) == step, (point_id, t, life)
                    if opens:
                        assert p.lives_if_py(y, life) == step, (point_id, t, life)
                        openings["lives_if_py"] += 1
                    reads = {(n.obj.name, n.args) for n in p.cells["lives_if"].preds(t, life)}
                    assert (("lives_if_py", (y, life)) in reads) == opens, (point_id, t)
                    assert (("lives_if", (t - 1, life)) in reads) != opens, (point_id, t)
            paid = p.annuity_pp(t - 1) * (p.payment_factor(t - 1)
                                          + p.dependant_factor(t - 1))
            step = p.cum_annuity_all(t - 1) + paid
            assert p.cum_annuity_all(t) == step, (point_id, t)
            if opens:
                assert p.cum_annuity_all_py(y) == step, (point_id, t)
                openings["cum_annuity_all_py"] += 1
            reads = {(n.obj.name, n.args) for n in p.cells["cum_annuity_all"].preds(t)}
            assert (("cum_annuity_all_py", (y,)) in reads) == opens, (point_id, t)
            assert (("cum_annuity_all", (t - 1,)) in reads) != opens, (point_id, t)
        if not (p.vp_pct() > 0.0 and p.is_first_death()):
            continue
        base = max(p.duration_mth_init(), 0)
        for k in range(base + 1, p.duration_mth(end) + 1):
            step = (p.cum_annuity_pp(k - 1, annuitant) + p.annuity_pp_pm(k - 1))
            assert p.cum_annuity_pp(k, annuitant) == step, (point_id, k)
            if k % 12 == 0:
                assert p.cum_annuity_pp_py(k // 12 + 1) == step, (point_id, k)
                openings["cum_annuity_pp_py"] += 1
            reads = {(n.obj.name, n.args)
                     for n in p.cells["cum_annuity_pp"].preds(k, annuitant)}
            assert (("cum_annuity_pp_py", (k // 12 + 1,)) in reads) == (k % 12 == 0), (
                point_id, k)
    assert all(n > 50 for n in openings.values()), openings


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
    ``(line, what)``, ``ULB_UK_SEC``'s check (UKLIB-SEC-PLAN.md §6.6, *Record -- M10*).

    Every ``raise`` must call one exception on one string constant, ``raise
    ValueError("invalid kind")``, nothing else: a message built anywhere, at the raise
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
    call down, each as ``(space, name)``: ``Data`` and ``Projection`` share some names,
    ``annual_income`` among them, which are not one cell."""
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
            name = re.search(r"\.(\w+)\(", text).group(1)
            stack.append(("Data" if ".Data." in text else "Projection", name))
            if len(stack) > len(deepest):
                deepest = list(stack)
        else:
            stack.pop()
    return deepest


# The heads beside each shape's that hold the two chains by the year the depth test leaves
# unread at its foot, as (S point, cell, its arguments beyond the month): the LPI's income,
# which recurses by the year, and the catch-up's ratchet, which the income reads, each cold
# in the last month of its longest cover.
YEAR_HEADS = ((7, "annuity_pp", ()), (6, "annuity_pp", ()))

# The cells every chain recurses through, which the test must have checked: the three
# chains blocked by policy year, their openings, the income and the ratchet by the year,
# and the claims total, which holds a kind's cell beneath it.
CHAIN_CELLS = frozenset({"lives_if", "lives_if_py", "cum_annuity_all", "cum_annuity_all_py",
                         "cum_annuity_pp", "cum_annuity_pp_py", "annual_income", "rpi_peak",
                         "claims"})


# modelx warns as its stack trace starts and stops, which is all the test does with it.
@pytest.mark.filterwarnings("ignore:call stack trace:UserWarning")
def test_no_cell_a_chain_recurses_through_formats_a_refusal(sec_model, cold_now):
    """No cell a cold call's deepest path holds more than once builds text (M10, M12).

    A compiled cell's C frame holds the code that formats each of its messages, whether a
    run reaches it or not, and a chain holds a frame of each cell it recurses through at
    each level.  On CI's Ubuntu runner, a refusal formatted inside ``Term_UK_SEC``'s
    recursive waiver cell had its cold call at the longest cover need 512 KiB to 1 MiB, and
    256 to 384 once the cell held none (K12).  So every refusal of this model whose message
    is formatted sits in a cell no chain recurses through: the income, the payments to date
    on every stream and the annuitant's call ``annual_income_refusal``,
    ``cum_annuity_all_refusal`` and ``cum_annuity_pp_refusal`` on their error paths alone,
    and ``cum_annuity_pp(k, ALL)``'s refusal of a key before the valuation date's sits in
    ``cum_annuity_pp_all``.  On a model just read, at each shape's longest cover, issued
    now, each chain head of :data:`SHAPES` and :data:`YEAR_HEADS` is called cold in the last
    month, under modelx's stack trace (:func:`cold_now`, the depth test's calls), and the
    ``Projection`` cells on the stack at its deepest point are counted.  A cell held there
    twice or more is one the chain recurses through, at every month or every year, or at
    both of its ends.  None of them may build text anywhere in its formula, at a raise, in
    an error branch or into a local, nor raise other than one exception on one string
    constant (:func:`_text_faults`): the frame holds a message's code whether or not its
    branch runs.  A cell held once costs its frame once, as ``mort_rate_base_at``, whose
    refusal names an age outside the table, does at the chain's foot.  Every cell of
    :data:`CHAIN_CELLS` must be among those checked, or the test would check less than it
    says.
    """
    assert {cell for _, _, cell, _, year_head, _, _, _ in cold_now if year_head} == {
        cell for _, cell, _ in YEAR_HEADS}
    found, checked = [], set()
    for label, _, cell, args, _, _, _, stack in cold_now:
        assert len(stack) > 100, (label, cell, len(stack))
        names = [name for space, name in stack if space == "Projection"]
        held = {name for name in names if names.count(name) > 1}
        checked |= held
        for name in sorted(held):
            faults = _text_faults(sec_model.Projection.cells[name])
            if faults:
                found.append(f"point {label}: {cell}{args}: {name}, held "
                             f"{names.count(name)} times on the deepest path, builds "
                             f"text: {faults}")
    assert CHAIN_CELLS <= checked, sorted(CHAIN_CELLS - checked)
    assert not found, found


# ---------------------------------------------------------------------------
# T4 -- the count algebra
#
# BEF_DECR == BEF_NB + pols_new_biz, at every t of every point, is a convention
# (test_new_business_joins_the_count_before_decrements), and is not repeated here.


def test_the_count_is_never_decremented(sec_model):
    """The count on the books is ``policy_count`` from the start to the stop rule (D5).

    Mortality decrements each life's survival, never the count, so on every committed point
    ``pols_if_at(t, BEF_NB)`` is ``pols_if_init()`` at ``t_entry()``, ``policy_count()`` at
    every later month of the frame and 0 outside it: a closed form, which no recursion
    reaches, so that ``BEF_NB`` at the frame's last month evaluates nothing at the month
    before.  And ``pols_if``, the closing obligation measure, is the count times
    ``min(1, max(C, l_a(t+1)) + 1{delta > 0} (1 - l_a(t+1)) l_d(t+1))``, ``PA_UK_S``'s, at
    every month: below the count wherever a life may have died, 0.99999965 at ``t = 0`` on
    the twins of S's points 2, 6 and 7.
    """
    table = sec_model.Data.model_point_table()
    bef_nb = _code(_point(sec_model, 1), "BEF_NB")
    for key, point_id in zip(point_keys(sec_model), table.index):
        p = projection(sec_model, key)
        for t in range(p.proj_len() + 1):
            want = (0.0 if not p.is_active(t) else p.pols_if_init() if t == p.t_entry()
                    else p.policy_count())
            assert p.pols_if_at(t, bef_nb) == want, (point_id, t)
            if not p.is_active(t):
                continue
            la, ld = p.lives_if(t + 1, 1), p.lives_if(t + 1, 2)
            obligation = max(p.certain_floor(t), la)
            if p.dependant_pct() > 0.0:
                obligation += (1.0 - la) * ld
            assert p.pols_if(t) == (p.pols_if_at(t, _code(p, "BEF_DECR"))
                                    * min(1.0, obligation)), (point_id, t)
    fresh = mx.read_model(model_path(SEC), name=_name("closed_form"))
    try:
        p = _point(fresh, 1)
        last = p.proj_len() - 1
        p.pols_if_at(last, bef_nb)
        assert list(p.cells["pols_if_at"].keys()) == [(last, bef_nb)]
    finally:
        fresh.close()
    for point_id in (2, 6, 7):
        assert _point(sec_model, point_id).pols_if(0) == pytest.approx(0.99999965, abs=1e-8)


def test_result_pols_is_s_report_with_the_new_business_beside_it(sec_model, s_model):
    """``result_pols()`` is S's report, column for column, with ``pols_new_biz`` second (D5).

    ``pols_if`` comes first and ``pols_new_biz`` second, then ``PA_UK_S``'s other columns in
    its order (:data:`RESULT_POLS`).  On every twin, all starting at the valuation date, each
    column S holds is S's, to 1e-9 relative at no absolute floor, and ``pols_new_biz`` holds
    the count at ``t = 0`` and 0 in every other month.
    """
    table = sec_model.Data.model_point_table()
    twins = table.index[table["row_kind"] == "twin"].tolist()
    assert twins == sorted(s_model.Data.model_point_table().index)
    for point_id in twins:
        p, s = _point(sec_model, point_id), _point(s_model, point_id)
        pols, s_pols = p.result_pols(), s.result_pols()
        assert list(pols.columns) == RESULT_POLS, point_id
        assert set(s_pols.columns) == set(RESULT_POLS) - {"pols_new_biz"}
        assert frame_mismatches(s_pols, pols, atol=0.0) == [], point_id
        assert list(pols["pols_new_biz"]) == [
            p.policy_count() if t == 0 else 0.0 for t in pols.index], point_id


# What T4 multiplies policy_count by: not a whole number, because a count of contracts need
# not be one, so that a flow which read the count as whole contracts would not follow it.
COUNT_FACTOR = 2.5


def test_scaling_the_count_scales_every_flow_and_no_per_contract_value(sec_model, tmp_path):
    """``policy_count`` is a weight: 2.5 times the count, 2.5 times every flow, the same per
    contract.

    The committed model, swept as the module reads it (``sec_model``), and a copy of its
    table with every count multiplied by :data:`COUNT_FACTOR`, read at the shipped
    References, are compared point by point.  On every point every
    column of ``result_cf`` and the counted columns of ``result_pols`` are 2.5 times the
    committed table's, element by element, to 1e-12 relative: a scaled count is a computed
    float, which may come back from the CSV within two ulps.  ``result_pols``' other
    columns, per contract, are the committed table's exactly.  So is every other cell of
    :data:`COUNTED`, at every argument the sweep of the committed table's point cached: the
    count at each timing and the claims of each kind, which no report shows by kind, among
    them.  And every cell outside :data:`COUNTED` (survival, the payments to date, the
    balance, the floors and factors, the income, both clocks, the flags) agrees bit for bit
    at every argument that sweep cached.  So a flow that dropped the count, or read it as
    whole contracts, which a table of counts of 1 hides from every comparison with S and a
    count doubled hides here, fails.  Each flow of :data:`FLOWS` is nonzero on some point
    (USLIB-SEC-PLAN.md §5.2, T4), the proportionate payment on point 9's twin and on
    point 12.
    """
    table = _committed()
    scaled = mx.read_model(_sec_inputs(tmp_path / "scaled", table.assign(
        policy_count=COUNT_FACTOR * table["policy_count"])), name=_name("scaled"))
    counted = sorted(COUNTED - {"result_cf", "result_pols"})
    nonzero = set()
    try:
        for key, scaled_key in zip(point_keys(sec_model), point_keys(scaled)):
            one, many = projection(sec_model, key), projection(scaled, scaled_key)
            _sweep(one)
            for report in REPORTS:
                b, d = one.cells[report](), many.cells[report]()
                assert d.index.equals(b.index) and list(d.columns) == list(b.columns)
                flows = [c for c in b.columns
                         if report == "result_cf" or c in COUNTED_POLS]
                fixed = [c for c in b.columns if c not in flows]
                want = COUNT_FACTOR * b[flows]
                bad = ((d[flows] - want).abs() > 1e-12 * want.abs()).any()
                assert not bad.any(), (key, report, list(bad[bad].index))
                assert d[fixed].equals(b[fixed]), (key, report)
                if report == "result_cf":
                    nonzero |= {c for c in FLOWS if (b[c] != 0.0).any()}
            for name in counted:
                for args in _cached_args(one.cells[name]):
                    want = COUNT_FACTOR * one.cells[name](*args)
                    got = many.cells[name](*args)
                    assert abs(got - want) <= 1e-12 * abs(want), (key, name, args, got, want)
            assert twin_mismatches(one, many, exempt=TWIN_EXEMPT_DEFAULT | COUNTED,
                                   rtol=0.0, atol=0.0) == []
            _release(scaled, scaled_key)
    finally:
        scaled.close()
    assert set(FLOWS) <= nonzero, f"0 on every point: {sorted(set(FLOWS) - nonzero)}"


def _month_on(p):
    """The state point ``p`` carries into its month 1, as the table's opening columns write
    it: what this model would read restated a month on."""
    d = p.duration_mth(1)
    linked = p.is_lpi5() or p.is_rpi_catchup()
    year = max(d - 1, 0) // 12 + 1
    state = {"duration_mth": d, "lives_if_init_1": p.lives_if(1, 1),
             "lives_if_init_2": p.lives_if(1, 2),
             "cum_annuity_all_init": p.cum_annuity_all(1)}
    if linked:
        state["annual_income_init"] = p.annual_income(year)
    if p.is_rpi_catchup():
        state["rpi_peak_init"] = p.rpi_peak(year - 1) / p.rpi_index(year - 1)
    if linked and p.vp_pct() > 0.0 and p.is_first_death():
        state["cum_annuity_pp_init"] = p.cum_annuity_pp(d, _code(p, "ANNUITANT"))
    return state


def test_a_point_restated_a_month_on_continues_its_own_flows(tmp_path):
    """The state a point carries into a month is the state its flows are made of (T4).

    Each point in payment on the committed table is restated a month on, opened with what
    this model carries into its month 1 (:func:`_month_on`): its count, unchanged, since the
    count is never decremented; each life's survival at time 1; the payments to date there;
    and on RPI-linked escalation the income of the policy year under way before any month-1
    anniversary, the ratchet's peak over the latest index and the annuitant's payments to
    date.  The restatement must continue the point's own frames, its row ``t`` the point's
    row ``t + 1``, in ``result_cf`` and ``result_pols``, every flow among them, to 1e-9
    relative, floored at 1e-9 for what a state read back from the CSV an ulp off moves about
    0.  A point whose frame ends in its first month has no month 1, and is left out.  Both
    models run at an inflation rate of 0, set on each as it is read (K7): the restatement
    moves the valuation date a month on, and expense inflation, on the valuation clock,
    would step a month apart by design (D7).  The restatement shows the opening state
    complete on this model's own states, the RPI history read under an RPI of its own
    among them, which S's at the shipped rate do not reach, as the splice shows it on S's;
    and the rated life at 575, restated on its anniversary at 576, crosses the month-0
    rule again.  Ten points: the joint point at 635 is the one with a one-month frame.
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
            top += 1
            row = table.loc[[label]].assign(**_month_on(p))
            row.index = pd.Index([top], name="point_id")
            rows.append(row)
            pairs.append((label, top))
        frames = {label: {report: _point(model, label).cells[report]()
                          for report in REPORTS}
                  for label, _ in pairs}
    finally:
        model.close()
    assert len(pairs) == 11
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


# ---------------------------------------------------------------------------
# T5 -- validation
#
# Each malformed table is the committed one with one fault.  The checks run over the whole
# table as it is read, in Data, and the message names the file it read and the column or
# every point at fault.  A blank cell reads as NaN, and so does a text cell once the checks
# coerce the column to numbers, so each is refused as a count, a duration or a state that
# is not a number.  The repeated point_id holds another contract under the same label, as a
# bad extract would, so that the check must look at the labels and not at whole rows.  The
# point_ids are the committed table's: 1 to 10 the twins of S's points; 11, the worked
# example at 17, the annuitant dead; 12, the proportionate payment's point at 16; 13, the
# guarantee's point at 120; 14, the LPI point at 24; 15, the catch-up point at 30; 16, the
# table basis's joint point at 101; 17, last-survivor value protection at 170; 18, the
# rated single life at 575; 19, the table basis's joint point at 635; 20, the catch-up point
# starting 13 months on; 21, the catch-up point at 60 under an RPI of -2%; 22, the LPI
# point at 42 under 8%.  A {file} in a message is the table's filename: every case is read
# by one model, from a file of its own (the malformed fixture).


def _drop(column):
    return lambda table: table.drop(columns=column)


def _rule(column, rule, points, on=""):
    """The message of one column's rule."""
    return f"{{file}}: {column} must be {rule}{on}; it is not at point_id {points}"


JOINT = " on a contract with a dependant"
LINKED = " on RPI-linked escalation, lpi5 or rpi_catchup"
CATCHUP = " on rpi_catchup escalation"
PAID = " on RPI-linked escalation with value protection on the first death"
START = ("{file}: {column} must hold its value at the start date on a contract not yet in "
         "payment, duration_mth 0 or less: each covered life alive, nothing paid, the first "
         "year's income and a peak of 1; it does not at point_id {points}")
FIRST_YEAR = ("{file}: {column} must hold its first year's value on a contract in its "
              "first policy year, duration_mth 1 to 12, before which no anniversary has "
              "passed: the first year's income and a peak of 1; it does not at point_id "
              "{points}")
STATUS = ("{file}: on the scenario basis lives_if_init_{life} must be 1 while the life "
          "survives to the valuation date, death_mth_{life} blank or duration_mth or "
          "later, and 0 once it has died; it is not at point_id {points}")
DEATH = ("{file}: death_mth_{life} must be blank or a whole number of months, 0 or more, a "
         "policy month, on the scenario basis; it is not at point_id {points}")
BELOW_FIRST_YEAR = ("{file}: annual_income_init must be annual_income or more, to half a "
                    "cent, on RPI-linked escalation, whose income never falls below the "
                    "first year's; it is not at point_id [14]")


def _start(column, points):
    return START.replace("{column}", column).replace("{points}", str(points))


def _first_year(column, points):
    return FIRST_YEAR.replace("{column}", column).replace("{points}", str(points))


def _status(life, points):
    return STATUS.replace("{life}", str(life)).replace("{points}", str(points))


def _death(life, points):
    return DEATH.replace("{life}", str(life)).replace("{points}", str(points))


MALFORMED = [
    *[(f"no {column} column", _drop(column), f"{{file}} has no {column} column")
      for column in ("policy_count", "duration_mth", *STATE)],
    ("a repeated point_id",
     lambda t: pd.concat([t, t.loc[[16]].assign(policy_id="PA-900099")]),
     "{file}: point_id [16] appears more than once"),
    ("a negative count", _set("policy_count", [16], -0.1),
     _rule("policy_count", "a number, zero or more", [16])),
    ("a blank count", _set("policy_count", [11], float("nan")),
     _rule("policy_count", "a number, zero or more", [11])),
    ("two text counts", _set("policy_count", [14, 21], "abc"),
     _rule("policy_count", "a number, zero or more", [14, 21])),
    ("an infinite count", _set("policy_count", [1], float("inf")),
     _rule("policy_count", "a number, zero or more", [1])),
    ("a fractional duration", _set("duration_mth", [16], 101.5),
     "{file}: duration_mth must be a whole number of months; it is not at point_id [16]"),
    ("a blank duration", _set("duration_mth", [20], float("nan")),
     "{file}: duration_mth must be a whole number of months; it is not at point_id [20]"),
    ("a text duration", _set("duration_mth", [13], "x120"),
     "{file}: duration_mth must be a whole number of months; it is not at point_id [13]"),
    ("durations of 2**53 months at two points", _set("duration_mth", [16, 19], 2.0 ** 53),
     "{file}: duration_mth must be below 2**53 months; it is not at point_id [16, 19]"),
    ("starting beyond the horizon", _set("duration_mth", [20], -121),
     "{file}: duration_mth must be -120 or more, an annuity starting at most 120 months "
     "after the valuation date; it is not at point_id [20]"),
    # PA_UK_S reads each flag through bool(), which reads a blank, NaN, as True.
    ("a blank dependant flag", _set("dependant_present", [5], float("nan")),
     _rule("dependant_present", "True or False", [5])),
    ("a blank proportion", _set("proportion", [2], float("nan")),
     _rule("proportion", "True or False", [2])),
    ("a flag written 1", _set("dependant_present", [1], 1),
     _rule("dependant_present", "True or False", [1])),
    # PA_UK_S truncates each of these with int().
    ("a fractional annuitant age", _set("annuitant_age", [2], 65.5),
     _rule("annuitant_age", "a whole number below 2**53", [2])),
    ("a blank annuitant age", _set("annuitant_age", [3], float("nan")),
     _rule("annuitant_age", "a whole number below 2**53", [3])),
    ("an annuitant age of 2**53", _set("annuitant_age", [4], 2.0 ** 53),
     _rule("annuitant_age", "a whole number below 2**53", [4])),
    ("a negative income", _set("annual_income", [7], -1.0),
     _rule("annual_income", "a finite number, 0 or more", [7])),
    ("a blank income", _set("annual_income", [2], float("nan")),
     _rule("annual_income", "a finite number, 0 or more", [2])),
    ("a fractional frequency", _set("frequency", [1], 4.5),
     _rule("frequency", "12, 4, 2 or 1", [1])),
    ("a frequency of 3", _set("frequency", [5], 3),
     _rule("frequency", "12, 4, 2 or 1", [5])),
    ("a fractional guarantee", _set("guarantee_months", [3], 120.5),
     _rule("guarantee_months", "a whole number of months, 0 or more, below 2**53", [3])),
    ("a negative guarantee", _set("guarantee_months", [4], -12),
     _rule("guarantee_months", "a whole number of months, 0 or more, below 2**53", [4])),
    ("value protection past 1", _set("vp_pct", [1], 1.5),
     _rule("vp_pct", "a number from 0 to 1", [1])),
    ("negative value protection", _set("vp_pct", [10], -0.1),
     _rule("vp_pct", "a number from 0 to 1", [10])),
    ("blank value protection", _set("vp_pct", [2], float("nan")),
     _rule("vp_pct", "a number from 0 to 1", [2])),
    ("a fractional dependant age", _set("dependant_age", [2], 62.5),
     _rule("dependant_age", "a whole number below 2**53", [2], JOINT)),
    ("a blank dependant age", _set("dependant_age", [1], float("nan")),
     _rule("dependant_age", "a whole number below 2**53", [1], JOINT)),
    ("a dependant's share past 1", _set("dependant_pct", [3], 1.2),
     _rule("dependant_pct", "a number from 0 to 1", [3], JOINT)),
    ("a blank dependant's share", _set("dependant_pct", [10], float("nan")),
     _rule("dependant_pct", "a number from 0 to 1", [10], JOINT)),
    ("a negative fixed escalation", _set("escalation_rate", [1], -0.01),
     _rule("escalation_rate", "a finite number, 0 or more", [1], " on fixed escalation")),
    ("a blank fixed escalation", _set("escalation_rate", [9], float("nan")),
     _rule("escalation_rate", "a finite number, 0 or more", [9], " on fixed escalation")),
    # PA_UK_S truncates a fractional month of death, and reads a negative one as a life
    # that never dies.
    ("a fractional death month", _set("death_mth_1", [1], 16.5), _death(1, [1])),
    ("a negative death month", _set("death_mth_1", [9], -1), _death(1, [9])),
    ("a text death month", _set("death_mth_2", [10], "x"), _death(2, [10])),
    ("survival past 1", _set("lives_if_init_1", [16], 1.5),
     "{file}: lives_if_init_1 must be a probability, 0 to 1; it is not at point_id [16]"),
    ("negative survival", _set("lives_if_init_2", [16], -0.1),
     "{file}: lives_if_init_2 must be a probability, 0 to 1; it is not at point_id [16]"),
    ("blank survival", _set("lives_if_init_1", [19], float("nan")),
     "{file}: lives_if_init_1 must be a probability, 0 to 1; it is not at point_id [19]"),
    ("a second life on a single-life contract", _set("lives_if_init_2", [18], 0.5),
     "{file}: lives_if_init_2 must be 0 on a single-life contract, which covers no second "
     "life; it is not at point_id [18]"),
    ("negative payments to date", _set("cum_annuity_all_init", [16], -1.0),
     _rule("cum_annuity_all_init", "a finite number, 0 or more", [16])),
    ("blank payments to date", _set("cum_annuity_all_init", [11], float("nan")),
     _rule("cum_annuity_all_init", "a finite number, 0 or more", [11])),
    ("a blank RPI income", _set("annual_income_init", [14], float("nan")),
     _rule("annual_income_init", "a finite number, 0 or more", [14], LINKED)),
    ("an infinite RPI income", _set("annual_income_init", [15], float("inf")),
     _rule("annual_income_init", "a finite number, 0 or more", [15], LINKED)),
    ("a peak below the index", _set("rpi_peak_init", [15], 0.99),
     _rule("rpi_peak_init", "a finite number, 1 or more", [15], CATCHUP)),
    ("a blank peak", _set("rpi_peak_init", [21], float("nan")),
     _rule("rpi_peak_init", "a finite number, 1 or more", [21], CATCHUP)),
    ("blank annuitant payments", _set("cum_annuity_pp_init", [14], float("nan")),
     _rule("cum_annuity_pp_init", "a finite number, 0 or more", [14], PAID)),
    ("negative annuitant payments", _set("cum_annuity_pp_init", [21], -1.0),
     _rule("cum_annuity_pp_init", "a finite number, 0 or more", [21], PAID)),
    # Rule 14 at its edge too: a cent below the first year's 5,400 is refused, half a cent
    # below read (test_the_edges_of_the_in_force_interface_are_accepted).
    ("an RPI income below the first year's", _set("annual_income_init", [14], 5000.0),
     BELOW_FIRST_YEAR),
    ("an RPI income a cent below the first year's",
     _set("annual_income_init", [14], 5399.99), BELOW_FIRST_YEAR),
    # Each window at both its ends: the start date's at duration_mth 0 and -120, the
    # horizon; the first policy year's at 1 and 12.
    ("survival at the start of a contract not yet in payment",
     _set("lives_if_init_1", [20], 0.99), _start("lives_if_init_1", [20])),
    ("survival at the start of a contract 120 months on",
     _then(_set("duration_mth", [20], -120), _set("lives_if_init_1", [20], 0.99)),
     _start("lives_if_init_1", [20])),
    ("a dead dependant at the start", _set("lives_if_init_2", [1], 0.0),
     _start("lives_if_init_2", [1])),
    ("payments before the start", _set("cum_annuity_all_init", [6], 10.0),
     _start("cum_annuity_all_init", [6])),
    ("an RPI income at the start other than the first year's",
     _set("annual_income_init", [20], 5562.0), _start("annual_income_init", [20])),
    ("a peak at the start other than 1", _set("rpi_peak_init", [6], 1.05),
     _start("rpi_peak_init", [6])),
    ("annuitant payments before the start", _set("cum_annuity_pp_init", [7], 1350.0),
     _start("cum_annuity_pp_init", [7])),
    ("an RPI income in the first month other than the first year's",
     _then(_set("duration_mth", [15], 1), _set("annual_income_init", [15], 5562.0)),
     _first_year("annual_income_init", [15])),
    ("an RPI income in the twelfth month other than the first year's",
     _then(_set("duration_mth", [15], 12), _set("annual_income_init", [15], 5562.0)),
     _first_year("annual_income_init", [15])),
    ("a peak in the first month other than 1",
     _then(_set("duration_mth", [21], 1), _set("annual_income_init", [21], 5400.0),
           _set("rpi_peak_init", [21], 1.01)),
     _first_year("rpi_peak_init", [21])),
    ("a peak in the twelfth month other than 1",
     _then(_set("duration_mth", [21], 12), _set("annual_income_init", [21], 5400.0),
           _set("rpi_peak_init", [21], 1.01)),
     _first_year("rpi_peak_init", [21])),
    ("a scenario annuitant alive after the death", _set("lives_if_init_1", [11], 1.0),
     _status(1, [11])),
    ("a scenario annuitant dead before the death", _set("lives_if_init_1", [12], 0.0),
     _status(1, [12])),
    ("a scenario dependant dead with no death", _set("lives_if_init_2", [17], 0.0),
     _status(2, [17])),
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


# The labels an extract carries: the committed points' in reverse, from 123 down, so that
# a label is neither a position plus one nor in the order of the rows.
EXTRACT_LABELS = tuple(range(123, 100, -1))


def _relabelled(message, relabel):
    """``message`` with every ``point_id [...]`` list it holds relabelled by ``relabel``."""
    def labels(match):
        return "point_id [" + ", ".join(str(relabel[int(p)]) for p in
                                        match.group(1).split(", ")) + "]"
    return re.sub(r"point_id \[(\d+(?:, \d+)*)\]", labels, message)


@pytest.fixture(scope="module")
def malformed_extract(tmp_path_factory):
    """:data:`MALFORMED`'s tables as an extract labels its rows, each a file of its own.

    Each case's table is the committed one with its fault, made by its own labels, and then
    relabelled :data:`EXTRACT_LABELS`, in order, so that no label is its position plus one.
    One model reads them all, as :func:`malformed` reads its files.  Returns ``(model,
    {case: filename}, {committed label: extract label})``.
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


# A text value no decode knows, as (case, the table's edit, the point, PA_UK_S's message).
# Data leaves these columns to the decodes, which read and validate each as PA_UK_S's label
# accessor does, so that the refusal is PA_UK_S's own, through a projection of the point.
UNDECODABLE = [
    ("an unknown timing", _set("timing", [1], "monthly"), 1, "invalid timing"),
    ("a timing in capitals", _set("timing", [5], "Advance"), 5, "invalid timing"),
    ("an unknown escalation", _set("escalation_type", [2], "rpi"), 2,
     "invalid escalation_type"),
    ("an escalation with a space", _set("escalation_type", [7], "lpi5 "), 7,
     "invalid escalation_type"),
    ("an unknown value-protection basis", _set("vp_basis", [10], "last"), 10,
     "invalid vp_basis"),
    ("an unknown mortality basis", _set("mort_basis", [2], "stochastic"), 2,
     "invalid mort_basis"),
    ("the proportionate payment in advance",
     _then(_set("timing", [9], "advance")), 9,
     "proportion applies to arrears payments only"),
    ("a fixed escalation past its cap", _set("escalation_rate", [1], 0.11), 1,
     "fixed escalation exceeds the contractual cap"),
]


@pytest.mark.parametrize("case, edit, point, message", UNDECODABLE,
                         ids=[c[0] for c in UNDECODABLE])
def test_a_text_value_no_decode_knows_raises_pa_uk_s_message(tmp_path, case, edit, point,
                                                             message):
    """Each decode reads and validates its column as ``PA_UK_S``'s accessor does (§6.7).

    ``timing``, ``escalation_type``, ``vp_basis`` and ``mort_basis`` are decoded into flags,
    so that no projection cell compares text, and each decode raises ``PA_UK_S``'s own
    message for a value its accessor refuses, through a projection of the point; so do the
    proportion rule and the fixed escalation's cap, which ``PA_UK_S`` checks where it reads
    them.  ``Data`` reads the table, since the checks are the accessors'.  Each names the
    point, a refusal of a value the model point holds, in ``PA_UK_S``'s words.
    """
    model = _read_edited(tmp_path, edit)
    try:
        assert len(model.Data.model_point_table()) == len(_committed())
        _refused(_point(model, point).result_cf, f"point_id {point}: {message}")
    finally:
        model.close()


@pytest.mark.parametrize("case, edit, point, message", UNDECODABLE,
                         ids=[c[0] for c in UNDECODABLE])
def test_a_text_value_no_decode_knows_is_refused_naming_the_extract_s_label(
        tmp_path, case, edit, point, message):
    """Each decode's refusal names the extract's label, never the row's position (T5).

    The committed labels are their positions plus one, so a decode that named its point by
    its place in the table, ``idx + 1``, would pass every case of :data:`UNDECODABLE` on
    them, and the compiled refusal test, which compares the two engines, would see both
    name the same wrong point.  So each case's table is the committed one with its fault,
    made by its own labels, and then relabelled :data:`EXTRACT_LABELS`, as
    :data:`MALFORMED`'s are, and each refusal must name the extract's label.
    """
    committed = _committed()
    relabel = dict(zip(committed.index, EXTRACT_LABELS))
    table = edit(committed).rename(index=relabel)
    model = mx.read_model(_sec_inputs(tmp_path, table), name=_name("undecodable_extract"))
    try:
        assert len(model.Data.model_point_table()) == len(committed)
        assert relabel[point] != point
        _refused(_point(model, relabel[point]).result_cf,
                 f"point_id {relabel[point]}: {message}")
    finally:
        model.close()


# A column only some points' projections read, refused by the point that reads it and by
# no other (USLIB-SEC-PLAN.md R7, precised at M23; UKLIB-SEC-PLAN.md §6.7, *Record --
# M11*, carried): as (case, the column, the value, the point that reads the column, the
# message naming it, a point that never reads the column).  The sexes, the ratings and the
# start year are read on the table basis alone; the purchase price where value protection
# is elected; the overlap on a contract with a dependant.  Stage E refused each at load,
# for every point, those that never read it among them.
SEX = ("point_id {label}: {column} must be M or F, a sex mort_table.csv rates, on the table "
       "basis, which reads it; it is not")
RATING = ("point_id {label}: {column} must be a number, and a finite one, 1 or more, on the "
          "table basis, which reads it; it is not")
PRICE = ("point_id {label}: purchase_price must be a number, and a finite one, 0 or more, "
         "where value protection is elected, which reads it; it is not")
YEAR = ("point_id {label}: start_year must be a number, below 2**53 in size, and a whole "
        "one on the table basis, which reads it; it is not")
OVERLAP = ("point_id {label}: overlap must be True or False on a contract with a dependant, "
           "which reads it; it is not")
BY_POINT = [
    ("an unknown annuitant sex", "annuitant_sex", "X", 5, SEX, 1),
    ("a blank annuitant sex", "annuitant_sex", float("nan"), 2, SEX, 3),
    ("an unknown dependant sex", "dependant_sex", "W", 6, SEX, 4),
    ("a rating below 1", "rating_multiplier", 0.9, 8, RATING, 9),
    ("an infinite rating", "rating_multiplier", float("inf"), 2, RATING, 1),
    ("a blank rating", "rating_multiplier", float("nan"), 16, RATING, 1),
    ("a text rating", "rating_multiplier", "high", 7, RATING, 10),
    ("a dependant rating below 1", "dependant_rating", 0.5, 7, RATING, 3),
    ("a negative purchase price", "purchase_price", -1.0, 1, PRICE, 3),
    ("an infinite purchase price", "purchase_price", float("inf"), 6, PRICE, 5),
    ("a blank purchase price", "purchase_price", float("nan"), 10, PRICE, 4),
    ("a fractional start year", "start_year", 2026.5, 6, YEAR, 1),
    ("a text start year", "start_year", "MMXXVI", 7, YEAR, 9),
    ("a blank overlap", "overlap", float("nan"), 3, OVERLAP, 5),
    ("an overlap written yes", "overlap", "yes", 4, OVERLAP, 8),
    ("start years written as floats, one as text", "start_year", "MMXXVI", 7, YEAR, 9),
]

# The edit a BY_POINT case makes to every row first, in the base table too: the start years
# written as floats, 2026.0, as a spreadsheet may save them, which pandas reads as text
# once another row holds text there.
BY_POINT_BEFORE = {
    "start years written as floats, one as text":
        lambda t: t.assign(start_year=t["start_year"].astype(float)),
}


def _by_point_edit(case, column, value, points):
    """The edit of BY_POINT's ``case``: its table-wide edit first, if it has one, then
    ``value`` written into ``column`` at ``points``."""
    before = BY_POINT_BEFORE.get(case, lambda t: t)
    return lambda t: _set(column, points, value)(before(t))


# The Data cells every point's projection reads whole, the mortality table's, which BY_POINT
# compares whole; every other array cell of Data is by point, compared by element, the
# flags' codes, [flag, point], at each point's column.
SCHEDULED = ("mort_sexes", "mort_table_array", "mort_age_first", "mort_age_last")


def _own_vectors(column):
    """The ``Data`` arrays that hold ``column``'s own value at a point."""
    if column in ("annuitant_sex", "dependant_sex"):
        return {"mort_schedule_1" if column == "annuitant_sex" else "mort_schedule_2"}
    if column == "overlap":
        return {"overlap", "overlap_ok", "flag_codes"}
    return {column, f"{column}_ok"}


def _vector_mismatches(want, got, skip):
    """Where two reads of a table's ``Data`` differ, bit for bit: the mortality table's
    arrays whole, and every array by point at every position, a vector's element or the
    flags' column there, but those ``skip`` maps to the arrays it leaves out there, or to
    None for all of them."""
    n = len(want.Data.model_point_table())
    found = []
    for name, cells in want.Data.cells.items():
        a = cells()
        if name in SCHEDULED:
            if np.asarray(a).tobytes() != np.asarray(got.Data.cells[name]()).tobytes():
                found.append(f"Data.{name}()")
            continue
        if not (isinstance(a, np.ndarray) and a.ndim in (1, 2) and a.shape[-1] == n):
            continue
        b = got.Data.cells[name]()
        for i in range(n):
            left_out = skip.get(i, ())
            if left_out is not None and name not in left_out and (
                    a[..., i].tobytes() != b[..., i].tobytes()):
                found.append(f"Data.{name}()[..., {i}]: {a[..., i]!r} and {b[..., i]!r}")
    return found


@pytest.mark.parametrize("case, column, value, refused, message, projects", BY_POINT,
                         ids=[c[0] for c in BY_POINT])
def test_a_column_some_points_never_read_is_refused_by_the_point_that_reads_it(
        tmp_path, case, column, value, refused, message, projects):
    """A value no projection can use is refused by the point whose projection reads it,
    naming it, and by no other (M12, after SPIA's *Record -- M23*).

    Seven columns are read by a projection on some points and never on others
    (:data:`BY_POINT`).  Stage E held each on every point as the table was read, so that
    one bad value refused the whole table, a contract on the scenario basis whose rating
    was blank among them, which ``PA_UK_S`` projects to a number.  Here the value is
    written into the column at a point that reads it and at one that never does, on an
    extract labelled otherwise than by position (:data:`EXTRACT_LABELS`), so that a
    refusal naming a point by ``idx + 1`` names another: ``Data`` reads the table, the
    first point's projection runs, the point that reads the column refuses it through its
    projection, naming its label, and the point that never reads it projects what it
    projects on the committed table, in both reports, exactly, its column's value read by
    nothing.  And every point but the refused one reads every ``Data`` vector as it does on
    the committed table, bit for bit, the mortality table's arrays too, but the point that
    never reads the column its own value there: a projection reads its own elements alone,
    and the table's, so equal elements project equal frames.  That holds the one value at
    no other point: a single life's overlap written ``yes`` leaves pandas reading the whole
    column as text, where ``bool("False")`` would read every joint contract's False as
    True; a start year written ``MMXXVI`` beside years written ``2026.0`` does too, where
    ``int("2026.0")`` would refuse every year the table basis reads.  A case may first edit
    every row, in both tables (:data:`BY_POINT_BEFORE`).
    """
    committed = _committed()
    relabel = dict(zip(committed.index, EXTRACT_LABELS))
    before = BY_POINT_BEFORE.get(case, lambda t: t)
    table = _by_point_edit(case, column, value, [refused, projects])(committed).rename(
        index=relabel)
    model = mx.read_model(_sec_inputs(tmp_path / "edited", table), name=_name("by_point"))
    base = mx.read_model(_sec_inputs(tmp_path / "base", before(committed).rename(
        index=relabel)), name=_name("by_point_base"))
    try:
        assert len(model.Data.model_point_table()) == len(committed)
        assert len(_point(model, relabel[17]).result_cf()) > 0
        _refused(_point(model, relabel[refused]).result_cf,
                 message.format(label=relabel[refused], column=column))
        for report in REPORTS:
            want = _point(base, relabel[projects]).cells[report]()
            got = _point(model, relabel[projects]).cells[report]()
            assert frame_mismatches(want, got, rtol=0.0, atol=0.0) == [], (case, report)
        at = {label: i for i, label in enumerate(committed.index)}
        found = _vector_mismatches(base, model, {at[refused]: None,
                                                 at[projects]: _own_vectors(column)})
        assert not found, (case, found[:20])
    finally:
        base.close()
        model.close()


def test_a_flag_reads_by_its_value_whatever_type_pandas_gives_its_column(tmp_path):
    """Each flag reads True or False by its value, ``str()`` of it lowered, never through
    ``bool()`` (USLIB-SEC-PLAN.md R6).

    A single-life contract never reads its overlap, so ``Data`` holds no value of it there,
    and an extract may write anything: ``n.a.`` on every single life here.  pandas then
    reads the whole column as text, ``True`` and ``False`` among it, and ``bool("False")``
    is True, which would read every joint contract's overlap as True, the guarantee's
    dependant paid beside the annuitant on point 3, as stage E refused the table to avoid.
    So the column is asserted text as read, every ``Data`` array of every point is held to
    the committed table's, bit for bit, but the single lives' flag codes, where the overlap
    reads -1, neither, and point 3's overlap read as False.
    """
    committed = _committed()
    single = [label for label in committed.index
              if str(committed.at[label, "dependant_present"]) == "False"]
    model = _read_edited(tmp_path / "text", _set("overlap", single, "n.a."))
    base = mx.read_model(model_path(SEC), name=_name("flags_base"))
    try:
        read = model.Data.model_point_table()
        assert {"True", "False", "n.a."} <= set(read["overlap"]), read["overlap"]
        at = {label: i for i, label in enumerate(committed.index)}
        assert not _vector_mismatches(base, model, {at[p]: {"flag_codes"} for p in single})
        codes = model.Data.flag_codes()
        assert [int(codes[1, at[p]]) for p in single] == [-1] * len(single)
        assert _point(model, 3).overlap() is False and _point(model, 3).is_joint() is True
    finally:
        base.close()
        model.close()


# A flag written as PA_UK_S's bool() reads True but no reader of the table writes it, on a
# point whose projection reads the flag: with a space before or after, " True" and
# "True ", which pandas reads as text, and the numbers 1 and 1.0, which it reads as text
# beside True and False.  Each flag column has one rule, Data.flag_codes, which its check
# and its decode both read, so each value is refused by the check, naming the point, or
# read as True by the decode; never passed by the check and read as False, or read as True
# where the check refuses it.  As (column, the point, its refusal): every point reads
# dependant_present and proportion, refused as the table is read, written on point 1, a
# joint contract whose proportion is False; a contract with a dependant reads its overlap,
# refused by its projection, written on point 3, whose overlap is False.
FLAG_SPELLINGS = (" True", "True ", 1, 1.0)
FLAG_READERS = [
    ("dependant_present", 1, f"{TABLE}: dependant_present must be True or False; it is "
     f"not at point_id [1]"),
    ("overlap", 3, OVERLAP.format(label=3)),
    ("proportion", 1, f"{TABLE}: proportion must be True or False; it is not at point_id "
     f"[1]"),
]


@pytest.mark.parametrize("column, point, refusal", FLAG_READERS,
                         ids=[c[0] for c in FLAG_READERS])
def test_a_flag_spelt_otherwise_is_refused_or_read_as_true_by_its_one_rule(
        tmp_path, column, point, refusal):
    """Each of :data:`FLAG_SPELLINGS`, written on a point that reads the flag, is refused
    there by the check or read as True by the decode, both reading one rule (M12).

    ``PA_UK_S``'s ``bool()`` reads each as True.  ``Data.flag_codes`` is each flag's one
    rule, which the check, ``Data.model_point_table`` or ``Data.overlap_ok``, and the
    decode, ``Data.is_joint``, ``Data.overlap`` or ``Data.proportion``, both read, so a
    value the check passes is never read as False.  So each value is written alone on a
    model read afresh, the point's projection is asked for its report, and the outcome is
    the check's refusal of the point (:data:`FLAG_READERS`), or the report and the decode,
    in ``Data`` and in the projection, reading True; and every value has the same outcome,
    whichever pandas makes of the column.
    """
    outcomes = {}
    for i, value in enumerate(FLAG_SPELLINGS):
        model = _read_edited(tmp_path / f"spelling{i}", _set(column, [point], value))
        try:
            try:
                p = _point(model, point)
                p.result_cf()
            except Exception as err:            # the outcome compared below
                outcomes[value] = ("refused", _raised(err))
                continue
            decode = {"dependant_present": "is_joint"}.get(column, column)
            position = list(model.Data.model_point_table().index).index(point)
            outcomes[value] = ("read", int(model.Data.cells[decode]()[position]),
                               p.cells[decode]())
        finally:
            model.close()
    for value, outcome in outcomes.items():
        assert outcome in (("refused", f"ValueError: {refusal}"), ("read", 1, True)), (
            column, value, outcome)
    assert len(set(outcomes.values())) == 1, (column, outcomes)


def test_the_future_horizon_is_a_reference_that_bounds_future_business(tmp_path):
    """``Data.future_horizon_mth`` refuses an annuity starting later than it, and 0 refuses
    all.

    The committed table's one future point starts 13 months on.  It reads at the shipped
    120 months and at 13, the shortest horizon that admits it, and is refused at 12, by
    name.  At 0 the model takes no future new business, D4's fallback for a product that
    cannot support it, and the message says so.  A horizon that is not a whole number of
    months, 0 or more, is itself refused, a NaN and an infinity among them.  Setting the
    Reference clears the table, so each value is read afresh.
    """
    future = _label(_committed(), "future", 6, -13)
    later = (f"{TABLE}: duration_mth must be -12 or more, an annuity starting at most 12 "
             f"months after the valuation date; it is not at point_id [{future}]")
    no_future = (f"{TABLE}: duration_mth must be 0 or more: this model takes no future new "
                 f"business; it is not at point_id [{future}]")
    model = mx.read_model(_sec_inputs(tmp_path, _committed()), name=_name("horizon"))
    try:
        assert model.Data.future_horizon_mth == 120
        cases = [(13, None), (12, later), (0, no_future), (120, None), (13.0, None)]
        cases += [(value, "future_horizon_mth must be a whole number of months, 0 or more, "
                          f"not {float(value)}")
                  for value in (-1, 12.5, math.nan, math.inf)]
        for horizon, refusal in cases:
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


def test_a_point_at_its_stop_is_refused_by_proj_len(tmp_path):
    """A contract at its stop rule has no frame, and ``proj_len()`` refuses it by name.

    The table basis's joint point in its last month, 635, is moved on to ``duration_mth``
    636, the stop rule of its 65/62 pair.  That is a rule of the product, not of the table:
    it needs the limiting age, a Reference, read where the frame is defined, so the table
    reads, and the point is refused on its first projection, rather than projecting
    nothing.  A loop over the block would meet the point only when it reached it, after
    projecting the points before it, so ``run_sec.py --block``, run beside the table, asks
    every point for its frame first: it fails naming the point, and prints nothing before.
    And one month earlier, 635, projects one month, its dependant's survival carried in.
    """
    moved = _label(_committed(), "derived", 2, 635)
    model = _read_edited(tmp_path, _set("duration_mth", [moved], 636))
    message = (f"point_id {moved}: duration_mth 636 is at or past the end of the "
               f"projection, policy month 636")
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
    model = _read_edited(tmp_path / "last", lambda t: t)
    try:
        p = _point(model, moved)
        df = p.result_cf()
        assert len(df) == 1 and p.lives_if(0, 2) == _committed().at[moved, "lives_if_init_2"]
        assert df["annuity_payments"].iloc[0] > 0.0
    finally:
        model.close()


# A contract owing nothing after the valuation date, as (case, the table's edit, the point,
# the message, or None where it is accepted).  Every covered life dead, and no guarantee
# left: no instalment, no dependant's income and no value-protection lump sum to pay.  Point
# 16 is the table basis's joint point at 101, value protection on the first death and no
# guarantee; 13 the guarantee's point at 120, its guarantee ended there, on the scenario
# basis, its annuitant dead in policy month 16, here its dependant written dead in 50.
OWING_NOTHING = [
    ("both lives dead, no guarantee",
     _then(_set("lives_if_init_1", [16], 0.0), _set("lives_if_init_2", [16], 0.0)), 16,
     "point_id 16: duration_mth 101: no payment is owed after the valuation date: every "
     "covered life has died, and the contract has no guarantee"),
    ("both lives dead, the guarantee ended",
     _then(_set("death_mth_2", [13], 50.0), _set("lives_if_init_2", [13], 0.0)), 13,
     "point_id 13: duration_mth 120: no payment is owed after the valuation date: every "
     "covered life has died, and the guarantee ended at policy month 120"),
    ("both lives dead, a month of the guarantee left",
     _then(_set("death_mth_2", [13], 50.0), _set("lives_if_init_2", [13], 0.0),
           _set("duration_mth", [13], 119)), 13, None),
    ("the annuitant dead, the dependant alive",
     _set("lives_if_init_1", [16], 0.0), 16, None),
    ("the dependant alive at a share of 0",
     _then(_set("lives_if_init_1", [16], 0.0), _set("dependant_pct", [16], 0.0)), 16,
     None),
]


@pytest.mark.parametrize("case, edit, point, message", OWING_NOTHING,
                         ids=[c[0] for c in OWING_NOTHING])
def test_a_contract_owing_nothing_is_refused_by_proj_len(tmp_path, case, edit, point,
                                                         message):
    """``proj_len()`` refuses a contract that owes nothing after the valuation date.

    In payment, its guarantee over and every covered life dead, its last payment was made
    before the valuation date, and an in-force extract should not carry it: SPIA's rule,
    worded by whether it had a guarantee (:data:`OWING_NOTHING`).  A month of the guarantee
    left owes its instalments, and a dependant alive owes the dependant's income, or on the
    last-survivor basis the lump sum, and each projects; at a dependant's share of 0 on the
    first-death basis the contract projects zeros, its obligation measure and so its
    maintenance among them, the rule reading the lives and the guarantee alone.
    """
    model = _read_edited(tmp_path, edit)
    try:
        assert len(model.Data.model_point_table()) == len(_committed())
        p = _point(model, point)
        if message is None:
            assert p.proj_len() > 0 and len(p.result_cf()) == p.proj_len()
        else:
            _refused(p.result_cf, message)
    finally:
        model.close()


# What the contract does not issue, or the model cannot project, refused by proj_len(), as
# (case, the table's edit, the References set, the point, the message, and the frame the
# point projects at the shipped References, or None).  Data reads an age as a whole number,
# so each reads.  PA_UK_S projects any age on the scenario basis, so the youngest age the
# contract allows is issue_age_min, 0, and a negative age of either life is refused; and a
# guarantee longer than the longest frame the youngest life allows, 12 x (115 - 0) =
# 1,380 months, which the compiled model's caches are sized from.  Each bound is refused
# just past it here, and accepted at it in the edges test, and each, moved past a committed
# twin, refuses it, which at the shipped bound projects its frame: the issue age raised past
# either life's, and the limiting age lowered to 9, where the longest frame, 108 months, is
# shorter than the guarantee.  Point 1 is the worked example, 65 with a dependant of 62; 3
# its twin with a 120-month guarantee.  And on either basis a frame longer than the table
# basis's longest, 12 x (omega_age_max - issue_age_min) = 1,392 months from the start
# date, which the caches are sized from: on the scenario basis, whose limiting age no
# bound holds, a month past it at the worst configuration the caches meet, the frame's
# edge (FRAME_REFS), accepted at it in the frame's edge tests, in both engines; the same
# lives issued at 0, 1,404 months; and the bound lowered to 52 past point 1's frame of 636
# months, which projects at the shipped 116 and is accepted at 53 (DOMAINS).
FRAME_REFUSAL = ("point_id {label}: the frame, {frame} months from the start date, is "
                 "longer than {bound} months, 12 x (omega_age_max - issue_age_min), the "
                 "longest the table basis projects, which the compiled model's caches are "
                 "sized from")

# The frame's edge where the caches end, at the worst configuration they meet: the worked
# example, point 1, on the scenario basis with value protection on the first death, issued
# future_horizon_mth, 120 months, after the valuation date, both lives at 1, under a
# limiting age of 117, above omega_age_max, which the scenario basis reads no table to be
# held to: the age stop 12 x (117 - 1) = LONGEST, 1,392 months from the start, the table
# basis's longest frame, and a guarantee as long, so that a guarantee a month longer is
# the frame a month longer.  t reaches 1,512, the payments to date's closing key 1,392, the
# policy year 117 and the anniversary 115, as at the contract's extremes.
FRAME_REFS = {"omega_age": OMEGA_MAX + 1}


def _frame_edge(guarantee):
    """The edit that puts point 1 at the frame's edge under a guarantee of ``guarantee``
    months (:data:`FRAME_REFS`)."""
    return _then(_set("annuitant_age", [1], 1), _set("dependant_age", [1], 1),
                 _set("duration_mth", [1], -120), _set("guarantee_months", [1], guarantee))


NOT_ISSUED = [
    ("an annuitant aged -1", _set("annuitant_age", [1], -1), {}, 1,
     "point_id 1: life 1's issue age, -1, is below issue_age_min, 0", None),
    ("a dependant aged -1", _set("dependant_age", [1], -1), {}, 1,
     "point_id 1: life 2's issue age, -1, is below issue_age_min, 0", None),
    ("an annuitant below a bound raised to 66", None, {"issue_age_min": 66}, 1,
     "point_id 1: life 1's issue age, 65, is below issue_age_min, 66", 636),
    ("a dependant below a bound raised to 63", None, {"issue_age_min": 63}, 1,
     "point_id 1: life 2's issue age, 62, is below issue_age_min, 63", 636),
    ("a guarantee of 1,381 months", _set("guarantee_months", [3], 1381), {}, 3,
     "point_id 3: the guarantee, 1381 months, is longer than 1380 months, 12 x (omega_age "
     "- issue_age_min), the longest frame from the start date", None),
    ("a guarantee past a limiting age lowered to 9", None, {"omega_age": 9}, 3,
     "point_id 3: the guarantee, 120 months, is longer than 108 months, 12 x (omega_age "
     "- issue_age_min), the longest frame from the start date", 636),
    ("a frame a month past the table basis's longest", _frame_edge(LONGEST + 1),
     FRAME_REFS, 1, FRAME_REFUSAL.format(label=1, frame=LONGEST + 1, bound=LONGEST), None),
    ("lives issued at 0 past omega_age_max",
     _then(_set("annuitant_age", [1], 0), _set("dependant_age", [1], 0)), FRAME_REFS, 1,
     FRAME_REFUSAL.format(label=1, frame=12 * (OMEGA_MAX + 1), bound=LONGEST), None),
    ("a frame past omega_age_max lowered to 52", None, {"omega_age_max": 52}, 1,
     FRAME_REFUSAL.format(label=1, frame=636, bound=624), 636),
]


@pytest.mark.parametrize("case, edit, refs, point, message, frame", NOT_ISSUED,
                         ids=[c[0] for c in NOT_ISSUED])
def test_a_point_the_contract_does_not_issue_is_refused_by_proj_len(tmp_path, case, edit,
                                                                    refs, point, message,
                                                                    frame):
    """``proj_len()`` refuses a point outside the contract's bounds, naming both (§6.7).

    ``PA_UK_S`` projects any age on the scenario basis, a negative one among them, and any
    guarantee, and the compiled model's caches are sized from the contract: a frame of at
    most ``12 x (omega_age_max - issue_age_min)`` months from the start, the table basis's
    longest, on either basis, and the horizon.  So the frame refuses such a point, naming
    it, as it refuses a point at its stop, and every report with it (:data:`NOT_ISSUED`):
    each bound just past it, and each bound moved past a committed point, which projects at
    the shipped bound, on a model read afresh.  The table reads either way.  Every
    Reference is set on a model just read, before its projection computes anything (K7).
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


def test_the_table_basis_s_longest_frame_projects_on_the_scenario_basis(tmp_path):
    """On either basis a frame of the table basis's longest projects, and one a month
    longer is refused: here the scenario basis, past ``omega_age_max`` (M12).

    ``proj_len()`` holds every frame to ``12 x (omega_age_max - issue_age_min)`` months
    from the start, 1,392, the table basis's longest, which the compiled model's caches are
    sized from.  The scenario basis reads no table, and its limiting age is held to no
    bound, as at stage E, which projected any frame there, and a frame past 1,392 months
    ran past the caches compiled.  So the worked example at the frame's edge, the worst
    configuration the caches meet (:func:`_frame_edge`, :data:`FRAME_REFS`), projects: its
    frame 1,392 months from the start, which it enters 120 months after the valuation date,
    1,512 months from the valuation date in all, its value protection reading the
    annuitant's payments to date at the closing key, 1,392.  A guarantee a month longer is
    refused, naming the point (:data:`NOT_ISSUED`), and the compiled model computes the one
    as modelx does and refuses the other as modelx does, message for message (the frame's
    edge compile test, the refusal test).
    """
    model = _read_edited(tmp_path, _frame_edge(LONGEST))
    try:
        for ref, value in FRAME_REFS.items():
            setattr(model.Projection, ref, value)
        p = _point(model, 1)
        assert (p.is_scenario(), p.is_first_death(), p.vp_pct() > 0.0) == (True,) * 3
        assert (p.stop_mth(), p.t_entry(), p.proj_len()) == (LONGEST, 120, LONGEST + 120)
        assert p.horizon_mths() == p.guarantee_mths() == LONGEST
        assert len(p.result_cf()) == LONGEST + 120
        assert p.duration_mth(LONGEST + 120) == LONGEST
        assert p.cum_annuity_pp(LONGEST, _code(p, "ANNUITANT")) > 0.0
        assert p.vp_balance(LONGEST + 120) >= 0.0
    finally:
        model.close()


# Each Reference proj_len() holds to a domain, at both edges of it, as (case, the References
# set, the point, the refusal, or None where proj_len() accepts them, and then the refusal
# a report meets, or None where the reports project; proj_len's docstring gives each
# domain's reason).  NaN and the infinities are outside every domain: PA_UK_S reads several
# of them through a min or a max whose bound comes first, where a NaN is lost, and the rest
# through a power.  A finite domain's upper edge is the largest float, accepted.  The
# integer References are whole numbers below 2**53, which the compiled model holds as long
# long, printed through int() once whole: each is refused at a fraction and at exactly
# 2**53 either way, and read as a whole float too.  Each is held on the points that read
# it: on every point, the expense and the inflation, held on point 1; on the table basis the
# mortality References, on point 2; on fixed escalation its cap, on point 1; on RPI-linked
# escalation rpi_rate, on points 6 and 7; on lpi5 its cap, on point 7.  A point that does not
# read one projects whatever it is, point 1 a NaN rpi_rate and a NaN annuitant_adj, point 2
# a NaN esc_lpi_cap.  Every accepted edge's reports are projected: an edge that takes a
# value past the floats is refused where that value first is, naming the References (the
# PAST_FLOATS cases below), and a fixed escalation's cap of 0 is the contract's own refusal
# of a 3% escalation.  omega_age's upper edge would size a frame of 2**53 years, which no
# machine projects, so it is projected at 120, on the scenario basis, which no
# omega_age_max bounds; on the table basis omega_age_max, 116, bounds it, and is held to
# its own domain, a whole number below 2**53, refusing the shipped 115 lowered to 114 there
# and not on the scenario basis, and 116 under a bound lowered to 115, which a mortality
# table longer than the shipped one would otherwise admit.  On either basis it bounds the
# frame, at 12 x (omega_age_max - issue_age_min) months, so it is held to its domain on the
# scenario basis too, and point 1's frame, 636 months, is accepted at a bound of 53, 636
# months, and refused at 52 (NOT_ISSUED).
BIG = 1.7976931348623157e308
WHOLE = 2.0 ** 53
BELOW_0 = math.nextafter(0.0, -1.0)
BELOW_MINUS_1 = math.nextafter(-1.0, -2.0)
ABOVE_MINUS_1 = math.nextafter(-1.0, 0.0)
BELOW_1 = math.nextafter(1.0, 0.0)


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


def _whole_domain(ref, point, accepted, below=True, reports=None):
    """The DOMAINS cases of an integer Reference: a whole number below 2**53, and 0 or more
    where ``below``, printed through int() once whole; each of ``accepted`` projects, or
    meets the report refusal ``reports`` gives it."""
    whole = f"point_id {point}: {ref} must be a whole number below 2**53, not {{}}"
    reports = reports or {}
    cases = [(f"{ref}={value!r} on {point}", {ref: value}, point, None, reports.get(value))
             for value in accepted]
    if below:
        cases.append((f"{ref}=-1 on {point}", {ref: -1}, point,
                      f"point_id {point}: {ref} must be 0 or more, not -1", None))
    return cases + [(f"{ref}={value!r} on {point}", {ref: value}, point,
                     whole.format(float(value)), None)
                    for value in (0.5, 2023.5, WHOLE, -WHOLE, 1e300, math.nan, math.inf,
                                  -math.inf)]


def _improvement_past(rate, k, base, year):
    """The refusal of an improvement factor past the floats at point 2's month 0."""
    return (f"point_id 2: the improvement factor improve_factor(0, 1) is past the largest "
            f"float, (1 - {rate}) to the power {k}, under improve_rate_base {float(base)} "
            f"and mort_table_year {int(year)}")


OMEGA_TABLE = ("point_id 2: omega_age must be at most 116, a year past mort_table.csv's "
               "last age, on the table basis, not {}")
DOMAINS = [
    *_domain("expense_maint", "a finite number, 0 or more", 1, (0.0, BIG), (BELOW_0,)),
    *_domain("inflation_rate", "a finite number, -1 or more", 1, (-1.0, BIG),
             (BELOW_MINUS_1,),
             {BIG: f"point_id 1: the expense expenses(12) is inf, not a finite number, under "
                   f"expense_maint 30.0 and inflation_rate {BIG}"}),
    *_domain("annuitant_adj", "a finite number, 0 or more", 2, (0.0, BIG), (BELOW_0,)),
    *_domain("improve_rate_base", "a finite number below 1", 2, (-BIG, BELOW_1), (1.0,),
             {-BIG: _improvement_past(-BIG, 3, -BIG, 2023)}),
    *_domain("improve_flat_age", "a finite number", 2, (-BIG, BIG), ()),
    *_domain("improve_taper_age", "a finite number", 2, (-BIG, BIG), ()),
    *_whole_domain("mort_table_year", 2, (0, 2023, 2023.0, WHOLE - 1, 1 - WHOLE),
                   below=False,
                   reports={WHOLE - 1: _improvement_past(0.0125, 2026 - int(WHOLE - 1),
                                                         0.0125, WHOLE - 1)}),
    *_domain("esc_fixed_cap", "a finite number, 0 or more", 1, (0.03, BIG),
             (BELOW_0,)),
    ("esc_fixed_cap=0.0 on 1", {"esc_fixed_cap": 0.0}, 1, None,
     "point_id 1: fixed escalation exceeds the contractual cap"),
    *_domain("rpi_rate", "a finite number above -1", 7, (ABOVE_MINUS_1, BIG), (-1.0,)),
    *_domain("rpi_rate", "a finite number above -1", 6, (ABOVE_MINUS_1, BIG), (-1.0,),
             {BIG: f"point_id 6: the income annual_income(2) is inf, not a finite number, "
                   f"under rpi_rate {BIG}, annual_income_init 5400.0 and rpi_peak_init "
                   f"1.0"}),
    *_domain("esc_lpi_cap", "a finite number, 0 or more", 7, (0.0, BIG), (BELOW_0,)),
    *_whole_domain("issue_age_min", 1, (0, 0.0)),
    ("issue_age_min=2**53-1 on 1", {"issue_age_min": WHOLE - 1}, 1,
     f"point_id 1: life 1's issue age, 65, is below issue_age_min, {int(WHOLE - 1)}", None),
    *_whole_domain("omega_age", 1, (115, 115.0, 116, 120), below=False),
    ("omega_age=0 on 1", {"omega_age": 0}, 1,
     "point_id 1: omega_age must be above issue_age_min, 0, not 0", None),
    ("omega_age=-5 on 1", {"omega_age": -5}, 1,
     "point_id 1: omega_age must be above issue_age_min, 0, not -5", None),
    ("omega_age=116 on 2", {"omega_age": 116}, 2, None, None),
    ("omega_age=116.0 on 2", {"omega_age": 116.0}, 2, None, None),
    ("omega_age=117 on 2", {"omega_age": 117}, 2, OMEGA_TABLE.format(117), None),
    *_whole_domain("omega_age_max", 2, (116, 116.0, 120), below=False),
    ("omega_age_max=114 on 2", {"omega_age_max": 114}, 2,
     "point_id 2: omega_age, 115, is above omega_age_max, 114, on the table basis", None),
    ("omega_age_max=114 on 1", {"omega_age_max": 114}, 1, None, None),
    ("omega_age_max=53 on 1", {"omega_age_max": 53}, 1, None, None),
    ("omega_age_max=nan on 1", {"omega_age_max": math.nan}, 1,
     "point_id 1: omega_age_max must be a whole number below 2**53, not nan", None),
    ("omega_age=116 under omega_age_max=115 on 2", {"omega_age": 116, "omega_age_max": 115},
     2, "point_id 2: omega_age, 116, is above omega_age_max, 115, on the table basis",
     None),
    ("rpi_rate=nan on 1", {"rpi_rate": math.nan}, 1, None, None),
    ("annuitant_adj=nan on 1", {"annuitant_adj": math.nan}, 1, None, None),
    ("esc_lpi_cap=nan on 6", {"esc_lpi_cap": math.nan}, 6, None, None),
    ("esc_fixed_cap=nan on 7", {"esc_fixed_cap": math.nan}, 7, None, None),
]


@pytest.mark.parametrize("case, refs, point, message, report", DOMAINS,
                         ids=[c[0] for c in DOMAINS])
def test_each_reference_is_held_to_its_domain_at_both_edges(case, refs, point, message,
                                                            report):
    """``proj_len()`` holds each Reference to its domain, NaN and the infinities outside it.

    ``PA_UK_S`` reads ``rpi_rate`` through the LPI's floor, ``max(0, rpi_rate)``, its bound
    first, so that a NaN reads as no increase, and through the index's power, where a rate
    of -1 or below is no price level; ``esc_lpi_cap`` through the cap, ``min(cap, ...)``,
    its bound first, which an infinity switches off; ``esc_fixed_cap`` in a comparison a
    NaN switches off; the mortality References through the cap ``min(q, 1.0)``, which reads
    an infinity as certain death, and the improvement's power; and the integer References in
    comparisons a NaN switches off, the limiting age sizing every frame.  The frame refuses
    each such Reference, by name, before it projects anything, and every report with it, at
    the nearest value outside each edge of its domain (:data:`DOMAINS`), on the points that
    read it; a point that does not read it projects whatever it is.  And the frame accepts
    each edge, whose reports then project, in finite floats over the whole frame, but where
    the edge takes a value past the floats, which is refused where it first is, naming the
    References, or where the contract refuses it.  A whole float, ``115.0``, reads as the
    whole number.  Each case sets its References on a model just read (K7).
    """
    model = mx.read_model(model_path(SEC), name=_name("domain"))
    try:
        for ref, value in refs.items():
            setattr(model.Projection, ref, value)
        p = _row(model, "twin", point, 0)
        if message is not None:
            _refused(p.result_cf, message)
        elif report is not None:
            assert p.proj_len() > 0
            _refused(p.result_cf, report)
        else:
            frames = [p.cells[name]() for name in REPORTS]
            for frame in frames:
                assert list(frame.index) == list(range(p.proj_len()))
                assert np.isfinite(frame.to_numpy(dtype=float)).all(), case
    finally:
        model.close()


# A value a power or a product makes past the floats from References each inside its
# domain, as (case, the References set, the point, the refusal), each where it first is:
# the inflation factor at the second anniversary of the valuation date, where 1e200 squared
# leaves them; the expense at the anniversary where an inflation of 50% takes the largest
# float's expense past them, the factor still finite; the catch-up's index at its second
# anniversary under an RPI of 1e200, its first year's income still finite; and the
# improvement factor in month 0, under a rate of -1e200, or of 0.999999 with the table's
# year 74 years after the contract's (UKLIB-SEC-PLAN.md §6.7; the M11 review).
PAST_FLOATS = [
    ("an inflation of 1e200", {"inflation_rate": 1e200}, 1,
     "point_id 1: the inflation factor inflation_factor(24) is past the largest float, "
     "under inflation_rate 1e+200"),
    ("the largest expense, inflating 50% a year", {"expense_maint": BIG,
                                                   "inflation_rate": 0.5}, 1,
     f"point_id 1: the expense expenses(84) is inf, not a finite number, under "
     f"expense_maint {BIG} and inflation_rate 0.5"),
    ("an RPI of 1e200 on the catch-up", {"rpi_rate": 1e200}, 6,
     "point_id 6: the index rpi_index(2) is past the largest float, under rpi_rate 1e+200"),
    ("an improvement of -1e200", {"improve_rate_base": -1e200}, 2,
     _improvement_past(-1e200, 3, -1e200, 2023)),
    ("an improvement of 0.999999 from 2100", {"improve_rate_base": 0.999999,
                                              "mort_table_year": 2100}, 2,
     _improvement_past(0.999999, -74, 0.999999, 2100)),
]


@pytest.mark.parametrize("case, refs, point, message", PAST_FLOATS,
                         ids=[c[0] for c in PAST_FLOATS])
def test_a_power_past_the_floats_is_refused_where_it_first_is(case, refs, point, message):
    """A power or a product past the floats is refused where it first is, by name (§6.7).

    Each Reference of :data:`PAST_FLOATS` is inside its domain, and the frame reads, but
    the value it makes leaves the floats in some month: Python's power raises
    ``OverflowError`` there, naming no point and no Reference, and a product, or C's power,
    gives an infinity, which the flows would carry on silently.  The cell refuses it in the
    month it first is, naming the point and the References that made it, and so does every
    report that reads it.  Each case sets its References on a model just read (K7).
    """
    model = mx.read_model(model_path(SEC), name=_name("past"))
    try:
        for ref, value in refs.items():
            setattr(model.Projection, ref, value)
        p = _row(model, "twin", point, 0)
        assert p.proj_len() > 0
        _refused(p.result_cf, message)
    finally:
        model.close()


# An income a rate or a history past every amount of money makes, each from References and
# columns inside their domains, as (case, the table's edit, the References set, the S point
# and month of the row, and the year and the reason the refusal names).  The LPI twin under a
# cap and an RPI of 1e300 escalates by that factor a year, past the floats in its third
# year; the fixed twin under an escalation and a cap of 1e300 too.  The table basis's joint
# point at 635 with a first year's income of 1e308 compounds 3% a year at the valuation
# date's key, the one loop, past the floats in its 21st year; and the catch-up point at 30
# carrying an income of 1e308 doubles it under an RPI of 100% at its next anniversary.
INCOMES = [
    ("the LPI past the floats", None, {"esc_lpi_cap": 1e300, "rpi_rate": 1e300}, (7, 0),
     3, "under rpi_rate 1e+300 and esc_lpi_cap 1e+300"),
    ("a fixed escalation past the floats", _set("escalation_rate", [1], 1e300),
     {"esc_fixed_cap": 1e300}, (1, 0), 3, "under escalation_rate 1e+300"),
    ("a fixed income compounded past the floats at the valuation date",
     lambda t: _set("annual_income", [_label(t, "derived", 2, 635)], 1e308)(t), {},
     (2, 635), 21, "under escalation_rate 0.03"),
    ("a catch-up income doubled past the floats",
     lambda t: _set("annual_income_init", [_label(t, "derived", 6, 30)], 1e308)(t),
     {"rpi_rate": 1.0}, (6, 30), 4,
     "under rpi_rate 1.0, annual_income_init 1e+308 and rpi_peak_init 1.0"),
]


@pytest.mark.parametrize("case, edit, refs, row, year, reason", INCOMES,
                         ids=[c[0] for c in INCOMES])
def test_an_income_past_the_floats_is_refused_in_its_year(tmp_path, case, edit, refs, row,
                                                         year, reason):
    """An income that leaves the floats is refused in the year it first does (§6.7).

    Every Reference and column here is inside its domain, and the table reads, but each
    case's income escalates past the largest float (:data:`INCOMES`), where the payments to
    date would carry an infinity on and the value-protection balance, ``max(0, vP - G)``,
    its bound first, would read it as no balance at all.  ``annual_income`` refuses it in
    the year it first is, naming the point, the year and what made it, and so does every
    report that reads it, through the recursion or the valuation date's loop alike.  Every
    Reference is set on a model just read (K7).
    """
    model = _read_edited(tmp_path, edit or (lambda t: t))
    try:
        for ref, value in refs.items():
            setattr(model.Projection, ref, value)
        kind = "twin" if row[1] == 0 else "derived"
        label = _label(model.Data.model_point_table(), kind, *row)
        _refused(_point(model, label).result_cf,
                 f"point_id {label}: the income annual_income({year}) is inf, not a finite "
                 f"number, {reason}")
    finally:
        model.close()


def test_the_payments_to_date_past_the_floats_are_refused(tmp_path):
    """Payments to date that leave the floats are refused where they first do.

    ``Data`` holds each column to a finite number, so the largest float reads, and an
    income of 1e300 does; but the next instalment takes the total past the floats, where
    the value-protection balance, ``max(0, vP - G)``, its bound first, would read it as no
    balance.  ``cum_annuity_all`` refuses it on the last-survivor row at 170, at its first
    instalment, in month 0, closing at time 1; and ``cum_annuity_pp`` the annuitant's on
    the catch-up row at 60 at its first instalment, policy month 62, closing at policy time
    63.  Each names the point and the key.
    """
    big = 1.7976931348623157e308
    last = _label(_committed(), "derived", 10, 170)
    frozen = _label(_committed(), "derived", 6, 60)
    model = _read_edited(tmp_path, _then(_set("cum_annuity_all_init", [last], big),
                                         _set("annual_income", [last], 1e300),
                                         _set("cum_annuity_pp_init", [frozen], big),
                                         _set("annual_income_init", [frozen], 1e300)))
    try:
        _refused(_point(model, last).result_cf,
                 f"point_id {last}: the payments to date cum_annuity_all(1) are inf, not a "
                 f"finite number")
        _refused(_point(model, frozen).result_cf,
                 f"point_id {frozen}: the payments to date cum_annuity_pp(63, 'ANNUITANT') "
                 f"are inf, not a finite number")
    finally:
        model.close()


def _anniversary_edit(root):
    """``(last, frozen, edit)``: the last-survivor row at 170 and the catch-up row at 60,
    and the edit that takes each's payments to date past the floats first at an
    anniversary, read in ``root`` to measure it.

    Each income is 1e300, and the opening state is the largest float less the payments
    the frame adds up to the anniversary and half the anniversary's own step, measured on
    the model with those incomes: so the total is finite in the month or at the key before
    the anniversary, and past the floats at it, by half a step, far more than a rounding.
    The last-survivor row's month 10 opens its policy year 16; the catch-up row's payments
    to date open a policy year at the key 72, its base being the key 60, itself an
    anniversary.  Each step is an instalment's, the month before each anniversary being
    one of the quarterly payments in arrears.
    """
    committed = _committed()
    last = _label(committed, "derived", 10, 170)
    frozen = _label(committed, "derived", 6, 60)
    incomes = _then(_set("annual_income", [last], 1e300),
                    _set("annual_income_init", [frozen], 1e300))
    model = _read_edited(root, incomes)
    try:
        p = _point(model, last)
        assert (p.duration_mth(10) % 12, p.duration_mth(9) % 12) == (0, 11)
        paid = p.cum_annuity_all(9) - p.cum_annuity_all(0)
        step = p.cum_annuity_all(10) - p.cum_annuity_all(9)
        q = _point(model, frozen)
        annuitant = _code(q, "ANNUITANT")
        assert (q.duration_mth_init(), q.duration_mth(12)) == (60, 72)
        pp_paid = q.cum_annuity_pp(71, annuitant) - q.cum_annuity_pp(60, annuitant)
        pp_step = q.cum_annuity_pp(72, annuitant) - q.cum_annuity_pp(71, annuitant)
    finally:
        model.close()
    assert step > 1e295 and pp_step > 1e295, (step, pp_step)
    return last, frozen, _then(incomes,
                               _set("cum_annuity_all_init", [last], BIG - paid - step / 2),
                               _set("cum_annuity_pp_init", [frozen],
                                    BIG - pp_paid - pp_step / 2))


def test_the_payments_to_date_past_the_floats_on_an_anniversary_are_refused_there(
        tmp_path):
    """Payments to date that first leave the floats on an anniversary are refused there.

    A chain blocked by policy year reads a year's first month from the year's opening, not
    from its monthly step, and the opening's total passes the same check, in the same cell,
    as any month's: without it the total would be infinite there, the balance ``max(0, vP
    - G)`` would read it as no balance, and the refusal would come a month or a key later,
    naming another.  On the rows of :func:`_anniversary_edit`, the total is finite the
    month or the key before the anniversary, and each chain refuses it at the anniversary,
    naming the point and the month or the key: the payments on every stream on the
    last-survivor row, ``cum_annuity_all(10)``, and the annuitant's on the catch-up row,
    ``cum_annuity_pp(72, ANNUITANT)``.  The refusals in a year's other months are the
    test above's.
    """
    last, frozen, edit = _anniversary_edit(tmp_path / "steps")
    model = _read_edited(tmp_path / "edge", edit)
    try:
        p = _point(model, last)
        assert p.cum_annuity_all(9) <= BIG
        _refused(p.result_cf, f"point_id {last}: the payments to date cum_annuity_all(10) "
                              f"are inf, not a finite number")
        q = _point(model, frozen)
        assert q.cum_annuity_pp(71, _code(q, "ANNUITANT")) <= BIG
        _refused(q.result_cf, f"point_id {frozen}: the payments to date cum_annuity_pp(72, "
                              f"'ANNUITANT') are inf, not a finite number")
    finally:
        model.close()


def test_each_refusal_cell_is_its_chain_by_its_bits(sec_model):
    """Each refusal moved off a chain computes its chain's value, by its bits, at every
    key of every committed point.

    ``annual_income_refusal``, ``cum_annuity_all_refusal`` and ``cum_annuity_pp_refusal``
    repeat their chain's step, to name what left the floats in a frame no chain holds, and
    return it where it is finite.  A refusal cell whose formula drifted from its chain's
    would refuse a total the chain computes otherwise, or let one pass: so each is held to
    its chain, ``float.hex`` of each, on every committed point, at every month of the
    frame and the month after, at every key of the annuitant's payments to date from the
    valuation date's where a projection reads them, and at every policy year the frame
    reads.
    """
    for key in point_keys(sec_model):
        p = projection(sec_model, key)
        end = p.proj_len()
        for t in range(end + 1):
            assert p.cum_annuity_all_refusal(t).hex() == p.cum_annuity_all(t).hex(), (key, t)
        if p.vp_pct() > 0.0 and p.is_first_death():
            annuitant = _code(p, "ANNUITANT")
            for k in range(max(p.duration_mth_init(), 0), p.duration_mth(end) + 1):
                assert (p.cum_annuity_pp_refusal(k).hex()
                        == p.cum_annuity_pp(k, annuitant).hex()), (key, k)
        for y in range(p.policy_year_init(), p.policy_year(end - 1) + 1):
            assert p.annual_income_refusal(y).hex() == p.annual_income(y).hex(), (key, y)


# A power called directly with a base that is not a finite number, which proj_len() refuses
# before any report reaches the power, as (case, the References set, the point, the call,
# its arguments, the message): each is refused by the power's own check of its result, as
# at stage E, where C's pow and Python's give NaN or an infinity without a raise.
POWER_BASES = [
    ("an inflation of NaN", {"inflation_rate": math.nan}, 1, "inflation_factor", (24,),
     "point_id 1: the inflation factor inflation_factor(24) is past the largest float, "
     "under inflation_rate nan"),
    ("an RPI of infinity", {"rpi_rate": math.inf}, 6, "rpi_index", (2,),
     "point_id 6: the index rpi_index(2) is past the largest float, under rpi_rate inf"),
    ("an improvement of NaN", {"improve_rate_base": math.nan}, 2, "improve_factor", (0, 1),
     "point_id 2: the improvement factor improve_factor(0, 1) is past the largest float, "
     "(1 - nan) to the power 3, under improve_rate_base nan and mort_table_year 2023"),
]


@pytest.mark.parametrize("case, refs, point, cell, args, message", POWER_BASES,
                         ids=[c[0] for c in POWER_BASES])
def test_a_power_on_a_base_no_number_is_refused_by_its_own_check(case, refs, point, cell,
                                                                 args, message):
    """Each of the three powers refuses a result that is not a finite number, as at stage
    E, besides M22's guard on a finite base.

    M22's form calls Python's power where C's gives an infinity from a finite base; from a
    base that is NaN or an infinity, Python's power gives NaN or an infinity too, without
    a raise.  ``proj_len()`` refuses the References that make such a base before any report
    reaches a power, so only a direct call meets one (:data:`POWER_BASES`), and each power
    refuses it by its own check of its result, naming the point and the Reference, as at
    stage ``E``.  Each case sets its References on a model just read (K7).
    """
    model = mx.read_model(model_path(SEC), name=_name("power"))
    try:
        for ref, value in refs.items():
            setattr(model.Projection, ref, value)
        p = _row(model, "twin", point, 0)
        _refused(lambda: p.cells[cell](*args), message)
    finally:
        model.close()


def test_the_edges_of_the_in_force_interface_are_accepted(sec_model, tmp_path):
    """A zero count, whole numbers in any type, the horizon and each bound's edge are read.

    A count of 0 is a point that projects zeros; ``101.0`` is a whole number of months, read
    back as the int the policy clock counts in; an annuity starting 120 months after the
    valuation date, the shipped ``future_horizon_mth``, is the last one the table admits,
    with a frame of 756 months, 636 from its start after 120 before it.  A row valued in its
    first month, 1, holds each life's survival and a payment to date.  Just past the first
    policy year, in month 13, an RPI-linked row holds the income and the peak its history
    gives, which the first year's rule no longer reads.  An RPI-linked income half a cent
    below the first year's, as an extract carrying it to the cent may hold it, is rule 14's
    edge, read and projected (USLIB-SEC-PLAN.md D6).  And each bound of the contract at
    its edge projects: issue at 0, the youngest the contract allows, a frame of 1,380 months
    on the scenario basis, and a guarantee of exactly 1,380 months, the longest frame from
    the start.
    """
    committed = _committed()
    last = _label(committed, "derived", 2, 635)
    future = _label(committed, "future", 6, -13)
    first = _label(committed, "derived", 2, 101)
    capped = _label(committed, "derived", 7, 42)
    frozen = _label(committed, "derived", 6, 60)
    floored = _label(committed, "derived", 7, 54)
    half_cent = committed.at[floored, "annual_income"] - 0.005

    def edit(table):
        table = _set("policy_count", [last], 0.0)(table)
        table = table.assign(duration_mth=table["duration_mth"].astype(float))
        table = _set("duration_mth", [future], -120.0)(table)
        table = _set("duration_mth", [first], 1.0)(table)
        table = _set("duration_mth", [capped, frozen], 13.0)(table)
        table = _set("annual_income_init", [floored], half_cent)(table)
        table = _set("annuitant_age", [1], 0)(table)
        table = _set("dependant_age", [1], 0)(table)
        return _set("guarantee_months", [3], 1380)(table)

    model = _read_edited(tmp_path, edit)
    try:
        read = model.Data.model_point_table()
        assert read["duration_mth"].dtype == float
        df = _point(model, last).result_cf()
        assert len(df) == 1 and (df == 0.0).all().all()
        p = _point(model, _label(committed, "derived", 6, 30))
        assert p.duration_mth(0) == 30 and type(p.duration_mth(0)) is int
        assert frame_mismatches(
            _point(sec_model, _label(committed, "derived", 6, 30)).result_cf(),
            p.result_cf(), rtol=0, atol=0) == []
        late = _point(model, future)
        assert (late.t_entry(), late.proj_len(), late.pols_new_biz(120)) == (120, 756, 1.0)
        one = _point(model, first)
        assert one.duration_mth_init() == 1 and one.cum_annuity_all_init() > 0.0
        for label in (capped, frozen):
            p13 = _point(model, label)
            assert p13.duration_mth_init() == 13 and p13.policy_year_init() == 2, label
            assert p13.annual_income_init() == committed.at[label, "annual_income_init"]
            assert len(p13.result_cf()) == 636 - 13, label
        assert _point(model, frozen).rpi_peak_init() == committed.at[frozen,
                                                                     "rpi_peak_init"]
        low = _point(model, floored)
        assert low.annual_income_init() == half_cent == 5399.995
        assert len(low.result_cf()) == 636 - 54
        assert len(_point(model, 1).result_cf()) == 1380
        assert len(_point(model, 3).result_cf()) == 1380
        for point in (1, 3):
            assert _point(model, point).check_lives_roll_fwd(), point
    finally:
        model.close()


# proj_len()'s refusal of a contract owing nothing, which S point 8 reaches once the cap
# has killed its rated life, and variants 14, 15 and 16 once both their lives have died with
# no guarantee left (OWES_NOTHING_FROM).
OWES_NOTHING = re.compile(
    r"ValueError: point_id \d+: duration_mth \d+: no payment is owed after the valuation "
    r"date: every covered life has died, and (the contract has no guarantee|the guarantee "
    r"ended at policy month \d+)")


def _every_state_months(end):
    """The S months a point whose S frame runs to ``end`` is restated at.

    By default the edges of its windows (USLIB-SEC-PLAN.md §5.2, T5): every month of the
    first policy year and the first anniversary, each anniversary and the month before it,
    through which the income escalates, and the last two months of the frame.  With
    ``UKLIB_SEC_FULL=1``, every month.  Each after 0, the twin's month.
    """
    if SEC_FULL:
        return list(range(1, end))
    months = {*range(1, 14), end - 2, end - 1,
              *(m for a in range(12, end, 12) for m in (a - 1, a))}
    return sorted(m for m in months if 0 < m < end)


def _states(s, points=None):
    """Each ``(S point, month)`` of :func:`_every_state_months` on every point of ``s``, or
    of ``points``."""
    labels = s.Data.model_point_table().index
    return [(point_id, d) for key, point_id in zip(point_keys(s), labels)
            if points is None or point_id in points
            for d in _every_state_months(projection(s, key).proj_len())]


def _restated(root, s, states):
    """The twins of ``s``'s points and a row in payment at each of ``states``, ``(S point,
    month)``, built by the generator out of ``s`` into a copy of the product directory:
    ``(folder, table)``."""
    spec = dataclasses.replace(SPEC, derived=tuple(states), future=(), derived_refs={})
    table, _ = build_sec_table(spec, s)
    return _sec_inputs(root, table), table


def _refused_in_force(folder, refs):
    """What ``Data`` and ``proj_len()`` refuse of the table in ``folder``, read with ``refs``
    set first: ``Data``'s refusal, or each row's ``proj_len()``'s, by its label, each by the
    line that names it.  Each row is released once asked (:func:`_release`)."""
    model = mx.read_model(folder, name=_name("every"))
    try:
        for ref, value in refs.items():
            setattr(model.Projection, ref, value)
        try:
            table = model.Data.model_point_table()
        except Exception as err:                # reported, with the rows' states
            return {"Data": _raised(err)}
        refused = {}
        for key, label in zip(point_keys(model), table.index):
            try:
                projection(model, key).proj_len()
            except Exception as err:            # reported, so every row is asked
                refused[label] = _raised(err)
            _release(model, key)
        return refused
    finally:
        model.close()


def test_every_state_s_reaches_is_accepted_in_force(s_model, spliced, tmp_path):
    """Every state ``PA_UK_S`` reaches is a valid opening state, but a contract owing
    nothing (T5).

    ``Data``'s rules and ``proj_len()``'s hold an opening state to what a contract in
    payment can be, so they must accept each state the S model reaches: a rule exercised
    only on the rows the other tests choose could refuse a state S reaches elsewhere (D6).
    So each point of S is restated in payment by the generator at the edges of its windows,
    or with ``UKLIB_SEC_FULL=1`` at every month of its frame (:func:`_every_state_months`),
    into one table beside the twins: ``Data`` reads it, and no row's ``proj_len()`` refuses
    it (USLIB-SEC-PLAN.md §5.2, T5, precised at M10), but the states the product refuses by
    name, set aside and shown refused: a contract owing nothing, every covered life dead and
    no guarantee left, which S point 8 reaches once the cap has killed its rated life, and
    the splice's variants 14, 15 and 16 once both their lives have died
    (:data:`OWES_NOTHING_FROM`).

    The states S reaches differ with the RPI, which moves the income, the peak and both
    payments to date, and with the variants, which move the lives, the schedule and the
    payments.  So the test runs on each set of inputs on which those states differ
    (precised at M9), and asserts which states each moves:

    * S as shipped, its ten points under its own References, as T1 and the committed rows
      read it (``s_model``);
    * the splice's shipped set, its points and sixteen variants;
    * the RPI sets, the RPI points and the fixed point beside them under 8% and under -2%,
      where the RPI points' income and both payments to date move, and under -2% the peak,
      and nothing else does: the fixed point's states, compared with S's as shipped, move
      with no RPI.

    Expense inflation moves no state, and the mortality basis's References move the lives
    and the payments alike on every point, so neither is run.
    """
    sets = {"shipped": (s_model, {}, None),
            "spliced": (spliced.pair("shipped")[0], SPLICE_SETS["shipped"], None),
            "rpi_high": (spliced.pair("rpi_high")[0], SPLICE_SETS["rpi_high"],
                         RPI_SET_POINTS),
            "rpi_low": (spliced.pair("rpi_low")[0], SPLICE_SETS["rpi_low"], RPI_SET_POINTS)}
    found, states, set_aside = {}, {}, {}
    for tag, (s, refs, points) in sets.items():
        s_table = s.Data.model_point_table()
        s_point = dict(zip(s_table["policy_id"], s_table.index))
        reached = _states(s, points)
        folder, rows = _restated(tmp_path / tag, s, reached)
        assert len(rows) == len(s_table) + len(reached)
        states[tag] = rows.set_index(["source_policy_id", "source_mth"])
        refused = _refused_in_force(folder, refs)
        if "Data" in refused:
            found[tag] = [refused["Data"]]
            continue
        late = [(int(row.point_id), row.source_policy_id) for row in rows.itertuples()
                if row.source_mth >= OWES_NOTHING_FROM.get(s_point[row.source_policy_id],
                                                           10 ** 9)]
        set_aside[tag] = sorted({policy for _, policy in late})
        for label, _ in late:
            if not OWES_NOTHING.fullmatch(refused.pop(label, "")):
                found.setdefault(tag, []).append(f"{label} not refused as owing nothing")
        if refused:
            found.setdefault(tag, []).append(
                f"{len(refused)} refused, first: {list(refused.items())[:5]}")
    assert not found, found
    assert set_aside == {"shipped": ["PA-000008"],
                         "spliced": ["PA-000008", "PA-900014", "PA-900015", "PA-900016"],
                         "rpi_high": [], "rpi_low": []}, set_aside
    moved = {}
    for tag in ("rpi_high", "rpi_low"):
        shipped, other = states["shipped"], states[tag]
        both = shipped.index.intersection(other.index)
        assert len(both) > 100, tag
        moved[tag] = {c for c in ("policy_count", *STATE)
                      if not shipped.loc[both, c].equals(other.loc[both, c])}
    paid = {"annual_income_init", "cum_annuity_all_init", "cum_annuity_pp_init"}
    assert moved == {"rpi_high": paid, "rpi_low": paid | {"rpi_peak_init"}}, moved


# ---------------------------------------------------------------------------
# The mortality table
#
# Data checks the table before a value of it is read, in the cell the projection takes the
# table's extent from (UKLIB-SEC-PLAN.md §4; USLIB-SEC-PLAN.md §7.1, *Precised at M3*,
# item 9).  Each case is the shipped table with one fault, read from a copy, refused by
# Data.mort_age_first alone, naming the file, the column and the lines at fault, the header
# line 1, and through a projection of the table basis's twin, point 2.  The table holds the
# male ages 50 to 115 on lines 2 to 67 and the female on lines 68 to 133, which its check
# reads as the file stands, where PA_UK_S's reader sorts the table.


def _written(column, value, where):
    """An edit of a table that writes ``value`` into ``column`` on the rows ``where``
    picks."""
    def edit(table):
        cells = table[column].astype(object)
        cells[where(table)] = value
        return table.assign(**{column: cells})
    return edit


def _mort(sex, age):
    return lambda t: (t["sex"] == sex) & (t["age"] == age)


def _mort_line(sex, age):
    """The line of mort_table.csv that holds ``sex`` at ``age``, as shipped."""
    rows = pd.read_csv(model_path(TWIN).parent / "mort_table.csv")
    return int(rows.index[(rows["sex"] == sex) & (rows["age"] == age)][0]) + 2


def _dropped(where):
    return lambda table: table[~where(table)].reset_index(drop=True)


def _repeated(where):
    return lambda table: pd.concat([table, table[where(table)]], ignore_index=True)


MORT = "mort_table.csv"
RATE = f"{MORT}: mort_rate must be a number from 0 to 1; it is not on line "


def _ages_apart(*faults):
    """The message of a mortality table whose sexes do not run one row an age, naming
    ``faults``."""
    return (f"{MORT}: the ages of each sex must run from 50 to 115, the table's first and "
            f"last, one row an age, none below 0; " + "; ".join(faults))


# A table the reader cannot read, or whose value is not a number in its range, as (case,
# its edit, its message).  A value no point reads is refused too: the male rate at 115,
# which no frame reaches.
UNREADABLE = [
    ("a blank mortality rate", _written("mort_rate", float("nan"), _mort("M", 70)),
     RATE + f"[{_mort_line('M', 70)}]"),
    ("a text mortality rate", _written("mort_rate", "low", _mort("M", 66)),
     RATE + f"[{_mort_line('M', 66)}]"),
    ("an infinite mortality rate", _written("mort_rate", float("inf"), _mort("M", 115)),
     RATE + f"[{_mort_line('M', 115)}]"),
    ("a negative mortality rate", _written("mort_rate", -0.001, _mort("F", 50)),
     RATE + f"[{_mort_line('F', 50)}]"),
    ("a mortality rate past 1", _written("mort_rate", 1.5, _mort("M", 80)),
     RATE + f"[{_mort_line('M', 80)}]"),
    ("two rows at fault", _then(_written("mort_rate", float("nan"), _mort("M", 50)),
                                _written("mort_rate", float("nan"), _mort("F", 90))),
     RATE + f"[{_mort_line('M', 50)}, {_mort_line('F', 90)}]"),
    ("an age not whole", _written("age", 65.5, _mort("M", 65)),
     f"{MORT}: age must be a whole number; it is not on line [{_mort_line('M', 65)}]"),
    ("an age written as text", _written("age", "x", _mort("F", 50)),
     f"{MORT}: age must be a whole number; it is not on line [{_mort_line('F', 50)}]"),
    ("an unknown sex", _written("sex", "X", _mort("F", 51)),
     f"{MORT}: sex must be M or F; it is not on line [{_mort_line('F', 51)}]"),
    ("an age missing", _dropped(_mort("M", 70)),
     _ages_apart("no line holds sex M, age 70")),
    ("an age twice", _repeated(_mort("F", 60)),
     _ages_apart(f"sex F, age 60 repeats on lines [{_mort_line('F', 60)}, 134]")),
    ("a sex missing", _dropped(lambda t: t["sex"] == "F"),
     _ages_apart("no line holds sex F, ages 50 to 115")),
    ("a sex shorter", _dropped(_mort("F", 115)),
     _ages_apart("no line holds sex F, age 115")),
    ("an age of 2**53", _written("age", 2.0 ** 53, _mort("M", 70)),
     f"{MORT}: age must be below 2**53 in size; it is not on line [{_mort_line('M', 70)}]"),
    ("an age of 1e300", _written("age", 1e300, _mort("F", 80)),
     f"{MORT}: age must be below 2**53 in size; it is not on line [{_mort_line('F', 80)}]"),
    ("an age of 2**53 - 1, far from the rest", _written("age", 2 ** 53 - 1, _mort("M", 70)),
     f"{MORT}: the ages of each sex must run from 50 to {2 ** 53 - 1}, the table's first "
     f"and last, one row an age, none below 0; no line holds sex M, age 70; no line holds "
     f"sex M, ages 116 to {2 ** 53 - 2}; no line holds sex F, ages 116 to {2 ** 53 - 1}"),
]


@pytest.mark.parametrize("case, edit, message", UNREADABLE, ids=[c[0] for c in UNREADABLE])
def test_a_table_the_reader_cannot_read_is_refused_naming_its_lines(tmp_path, case, edit,
                                                                    message):
    """``Data`` refuses the mortality table before a value of it is read (T5).

    ``PA_UK_S`` reads a blank rate as NaN, which its cap would keep and every flow carry; an
    infinite one, which the cap reads as certain death; a key that is not whole, gapped or
    repeated, as a ``KeyError`` only where a projection reaches it, or as a wrong row.
    Here the extent cell the projection asks first refuses each, naming the file, the
    column and the rows at fault (:data:`UNREADABLE`), and so does a projection of the table
    basis's twin.  A scenario point reads no mortality, and projects.
    """
    model = _read_edited(tmp_path, lambda t: t, edits={MORT: edit})
    try:
        _refused(model.Data.mort_age_first, message)
        _refused(_point(model, 2).result_cf, message)
        assert len(_point(model, 1).result_cf()) == 636
    finally:
        model.close()


def test_a_read_beyond_the_mortality_table_is_refused_naming_its_point(tmp_path):
    """A read past the mortality table's ages is refused, naming the point.

    ``PA_UK_S``'s lookup raises ``KeyError`` beyond the table, naming no point.  Below it,
    an annuitant issued at 49 on the table basis, which the table first rates at 50, is
    refused by the one cell that reads it, naming the point and the age; on the scenario
    basis, which reads no mortality, the same age projects, a frame of 12 x (115 - 49) =
    792 months.  Above it, the table is read at attained ages to ``omega_age - 1``, and
    ``proj_len()`` holds the limiting age to a year past the table's last age on the table
    basis, so no frame reads past it: at 116 the table basis's twin projects what
    ``PA_UK_S`` projects at that limiting age, in every column.
    """
    model = _read_edited(tmp_path, _then(_set("annuitant_age", [2], 49),
                                         _set("annuitant_age", [1], 49)))
    try:
        _refused(_point(model, 2).result_cf,
                 "point_id 2: mort_table.csv has no rate at attained age 49")
        assert len(_point(model, 1).result_cf()) == 792
    finally:
        model.close()
    s = mx.read_model(model_path(TWIN), name=_name("s_omega"))
    sec = mx.read_model(model_path(SEC), name=_name("sec_omega"))
    try:
        for each in (s, sec):
            each.Projection.omega_age = 116
        sp, p = _point(s, 2), _row(sec, "twin", 2, 0)
        assert sp.proj_len() == p.proj_len() == 12 * (116 - 62)
        assert frame_mismatches(sp.result_cf(), p.result_cf(), rtol=0.0, atol=0.0) == []
    finally:
        sec.close()
        s.close()


def test_a_key_written_as_a_float_reads_as_pa_uk_s_reads_it(sec_model, tmp_path):
    """A key written ``65.0`` is the key 65, in the table and in its extents.

    ``PA_UK_S``'s lookups match a float key to the int the projection asks, so a table
    written by a tool that writes every number with a decimal point reads the same.  The
    mortality table's ages and the model point table's ``duration_mth``, ages, frequency,
    guarantee and start year are written as floats, and every committed point projects
    what the committed tables project, exactly.
    """
    def as_float(*columns):
        return lambda table: table.assign(**{c: table[c].astype(float) for c in columns})

    model = _read_edited(tmp_path, as_float("duration_mth", "annuitant_age", "frequency",
                                            "guarantee_months", "start_year"),
                         edits={MORT: as_float("age")})
    try:
        for point_id in _committed().index:
            for report in REPORTS:
                assert frame_mismatches(_point(sec_model, point_id).cells[report](),
                                        _point(model, point_id).cells[report](),
                                        rtol=0, atol=0) == [], (point_id, report)
    finally:
        model.close()


# ---------------------------------------------------------------------------
# T6 -- regeneration


def test_the_committed_sec_inputs_are_what_s_generates(s_model):
    """``model_point_table_sec.csv`` is what PA_UK_S and its table generate today.

    Every row and column, the text cells and the opening-state columns included: an edit to
    an S row the table copies or derives from, or to an S formula a row's state is read
    from, fails here until ``python tools/gen_sec_points.py PA_UK_SEC`` regenerates it, in
    the same commit.  Text and integers compare exactly, and a float by its value, to 1e-12,
    because the text the writer picks for a computed float depends on the platform's parser
    (§5).
    """
    assert check_generated(SEC, s_model=s_model) == []


# ---------------------------------------------------------------------------
# The product's own facts


def test_the_payments_on_every_stream_are_one_total_before_the_valuation_date(sec_model):
    """``cum_annuity_pp(k, "ALL")`` refuses a key before the valuation date (§6.7, *E*).

    The payments to date on every stream are the opening state's one total,
    ``cum_annuity_all_init``, so a key before the valuation date's policy time has no value
    here: the worked example in payment 17 months reads its total at policy time 17, the
    column, and later keys from the valuation clock, and refuses policy time 16, naming the
    point and the column, where :mod:`~.PA_UK_S` would sum a schedule this model does not
    carry.  A key at or before 0 is 0, as in ``PA_UK_S``.
    """
    old = _row(sec_model, "derived", 1, 17)
    label = _label(sec_model.Data.model_point_table(), "derived", 1, 17)
    every = _code(old, "ALL")
    assert old.cum_annuity_pp(17, every) == old.cum_annuity_all_init() == 6790.5
    assert old.cum_annuity_pp(20, every) == old.cum_annuity_all(3)
    assert old.cum_annuity_pp(0, every) == 0.0
    _refused(lambda: old.cum_annuity_pp(16, every),
             f"point_id {label}: cum_annuity_pp(16, 'ALL') is before the valuation date, "
             f"policy time 17, where the payments to date are cum_annuity_all_init, one "
             f"total")


def test_the_two_clocks_on_the_shipped_points(sec_model):
    """``t`` counts from the valuation date; ``duration_mth(t)`` from the start (D3, D4).

    On a twin of S's points the two coincide, and its contracts enter as new business at
    ``t = 0``.  The worked example in payment 17 months is in policy year 2 at attained age
    66 at ``t = 0``, its annuitant dead since policy month 16 and its dependant paid from
    ``t = 0``, steps into policy year 3 at ``t = 7``, and has 619 months of its frame left,
    to the same stop as from the start.  The point starting 13 months on has nothing on the
    books and nothing to do before ``t = 13``, and a frame of 649 months.  The joint point
    in its last month has a one-month frame.  A timing or a kind the model does not know is
    refused rather than answered with another count.
    """
    twin = _row(sec_model, "twin", 1, 0)
    assert [twin.duration_mth(t) for t in (0, 1, 635)] == [0, 1, 635]
    assert (twin.t_entry(), twin.pols_if_init(), twin.pols_new_biz(0)) == (0, 0.0, 1.0)
    assert (twin.horizon_mths(), twin.stop_mth(), twin.proj_len()) == (636, 636, 636)
    old = _row(sec_model, "derived", 1, 17)
    assert (old.duration_mth(0), old.duration(0), old.policy_year(0), old.age(0, 1)) == (
        17, 1, 2, 66)
    assert (old.policy_year(6), old.policy_year(7)) == (2, 3)
    assert (old.proj_len(), old.stop_mth(), old.t_entry(), old.pols_new_biz(0)) == (
        619, 636, 0, 0.0)
    assert old.lives_if(0, 1) == 0.0 and old.lives_if(0, 2) == 1.0
    assert old.annuity_payments(0) == pytest.approx(695.25, abs=0.005)
    assert old.pols_if_at(0, _code(old, "BEF_DECR")) == old.pols_if_init() == 1.0
    fut = _row(sec_model, "future", 6, -13)
    assert (fut.duration_mth(0), fut.t_entry(), fut.proj_len()) == (-13, 13, 649)
    assert not fut.is_active(12) and fut.is_active(13)
    assert (fut.pols_if_init(), fut.pols_new_biz(13), fut.lives_if(13, 1)) == (
        0.0, 1.0, 1.0)
    assert fut.lives_if(12, 1) == 0.0 and fut.annuity_pp(15) == 1350.0
    last = _row(sec_model, "derived", 2, 635)
    assert (last.proj_len(), last.age(0, 2), last.policy_year(0)) == (1, 114, 53)
    _refused(lambda: old.pols_if_at(0, "BEF_NOTHING"), "invalid timing")
    _refused(lambda: old.claims(0, "NOTHING"), "invalid kind")
    _refused(lambda: old.cum_annuity_pp(20, "NOTHING"), "invalid kind")


def test_the_committed_rows_continue_their_s_points(sec_model, s_model):
    """Each committed row in payment, or starting later, is its S point from its month on.

    T6 compares a float to 1e-12, which pins a small survival only to that much of itself,
    so each committed row is compared with its S point frame by frame and cell by cell, at
    the shipped assumptions (USLIB-SEC-PLAN.md §7.1, *Precised at M3*, item 11): the nine
    derived rows from their months, and the row starting 13 months on from S's start, all
    to 1e-9 relative with no absolute floor but on the residuals, every cell but those
    expense inflation moves (:func:`_continues_s`), which the inflation test holds.  The two
    rows read from S under an RPI of their own continue S under that RPI, which the shipped
    one replaces from the valuation date, and their own test holds them.
    """
    table = sec_model.Data.model_point_table()
    s_table = s_model.Data.model_point_table()
    found = []
    for point_id in table.index:
        kind, month = table.at[point_id, "row_kind"], int(table.at[point_id, "source_mth"])
        policy = table.at[point_id, "source_policy_id"]
        s_point = int(s_table.index[s_table["policy_id"] == policy][0])
        if kind == "twin" or (s_point, month) in SPEC.derived_refs:
            continue
        found += [f"point {point_id}: {line}" for line in _continues_s(
            _point(s_model, s_point), _point(sec_model, point_id), month)]
    assert not found, found[:20]


def test_the_rows_read_under_an_rpi_of_their_own_continue_s_under_it(sec_model):
    """The three committed rows S reaches only under an RPI of its own are S's under it (C2).

    At ``PA_UK_S``'s flat 3% no state holds a ratchet's peak above its index, nor an LPI
    increase capped or floored, so the spec restates the catch-up point at its month 60
    from S run under an RPI of -2%, the LPI point at its month 42 from S under 8%, and the
    LPI point at its month 54 from S under -2% (the spec's ``derived_refs``), and C2
    freezes all three.  Three things are held of each:

    * the row is S's state under that RPI: S read under it holds, at the row's month, the
      row's count, survival, payments to date, income, peak and annuitant's payments;
    * set on this model too, that RPI gives the row S's path: it continues S's projection
      from its month on in every cell, over the whole of both frames, as the splice
      compares them (:func:`_continues_s`);
    * at today's References, which take over from the valuation date, the income parts
      from S's at the row's next anniversary, but no RPI moves survival, the guarantee's
      floor or the obligation measure: the committed row holds S's in every month.
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
            year = max(month - 1, 0) // 12 + 1
            opening = {"policy_count": sp.pols_if_init(),
                       "lives_if_init": (sp.lives_if(month, 1), sp.lives_if(month, 2)),
                       "cum_annuity_all_init": sp.cum_annuity_pp(month, "ALL"),
                       "annual_income_init": sp.annual_income(year)}
            assert row.policy_count() == opening["policy_count"]
            assert (row.lives_if_init(1), row.lives_if_init(2)) == pytest.approx(
                opening["lives_if_init"], rel=1e-12)
            assert row.cum_annuity_all_init() == pytest.approx(
                opening["cum_annuity_all_init"], rel=1e-12)
            assert row.annual_income_init() == pytest.approx(
                opening["annual_income_init"], rel=1e-12)
            if sp.escalation_type() == "rpi_catchup":
                assert row.rpi_peak_init() == pytest.approx(
                    sp.rpi_peak(year - 1) / sp.rpi_index(year - 1), rel=1e-12)
            assert row.cum_annuity_pp_init() == pytest.approx(
                sp.cum_annuity_pp(month, "ANNUITANT"), rel=1e-12)
            _sweep(sp)
            assert _continues_s(sp, _point(sec, label), month) == []
            for t in range(row.proj_len()):
                for cell in ("pols_if", "certain_floor"):
                    assert row.cells[cell](t) == pytest.approx(
                        sp.cells[cell](month + t), rel=1e-9, abs=0.0), (cell, t)
                for life in (1, 2):
                    assert row.lives_if(t, life) == pytest.approx(
                        sp.lives_if(month + t, life), rel=1e-9, abs=0.0), (life, t)
        finally:
            sec.close()
            s.close()


# The ratchet's catch-up branch, which a flat RPI never reaches: the committed catch-up row
# at S month 60, read from S under -2%, its income frozen at 5,400 and its peak 1 / 0.98^4,
# 1.0841657847339398, over the latest index, at the shipped 3% from the valuation date.
# Its fifth anniversary falls in month 0, where the index, 1.03 over the latest, stays below
# the peak, and so does its sixth, at t = 12, 1.03^2 = 1.0609; at its seventh, t = 24,
# 1.03^3 = 1.092727 passes it, and the income catches up by the excess over the peak:
# 5,400 x 1.092727 / 1.0841657847 = 5,442.64; then 5,400 x 1.03^4 / peak = 5,605.92 at its
# eighth, and so on, each anniversary's index over the same peak.  Hand-computed goldens, a
# quarter of each year's income paid in arrears at policy months 62, 65, ... .
CATCH_UP = {5: 5400.0, 6: 5400.0, 7: 5400.0, 8: 5442.64, 9: 5605.92, 10: 5774.10}


def test_the_ratchet_catches_up_from_a_peak_above_the_index(sec_model, tmp_path):
    """Carried in above the index, the ratchet freezes the income, then catches up (§6.7).

    ``PA_UK_S``'s deterministic RPI is monotone, so its catch-up branch, an index rising
    from below its peak, is never reached, and S cannot give it a golden.  The committed
    catch-up row at 60 carries a peak above the index, history S makes only under an RPI
    of -2% (:data:`CATCH_UP`): at the shipped 3% from the valuation date its income is
    frozen at 5,400 through its sixth and seventh policy years, the index rising from 1 to
    1.0609 under a peak of 1.0842, and catches up in its eighth, by the excess of the index
    over the peak, 5,442.64, each to the penny.  The peak runs on from the opening state:
    ``rpi_peak`` is the opening peak at the fourth anniversary, the latest, and at the fifth
    and sixth, and the index itself, 1.03^3, from the seventh.  Read from the index instead,
    a peak of 1 at the valuation date, the income would escalate at once, to 5,562.00 in the
    sixth year; a test writes the peak at 1 and sees that.  And a peak of 1.2 freezes the
    income to the eleventh year, 1.03^6 = 1.194 still short of it, and the twelfth's is
    5,400 x 1.03^7 / 1.2.
    """
    row = _point(sec_model, _label(sec_model.Data.model_point_table(), "derived", 6, 60))
    assert row.rpi_peak_init() == pytest.approx(1.0 / 0.98 ** 4, rel=1e-12)
    assert row.policy_year_init() == 5
    for year, income in CATCH_UP.items():
        assert row.annual_income(year) == pytest.approx(income, abs=0.005), year
    assert row.rpi_peak(4) == row.rpi_peak(5) == row.rpi_peak(6) == row.rpi_peak_init()
    assert row.rpi_peak(7) == row.rpi_index(7) == pytest.approx(1.03 ** 3, rel=1e-12)
    for t, income in ((2, 5400.0), (14, 5400.0), (26, 5442.64), (38, 5605.92)):
        assert row.annuity_pp(t) == pytest.approx(income / 4, abs=0.005), t
    label = _label(_committed(), "derived", 6, 60)
    for peak, frozen_to in ((1.0, None), (1.2, 11)):
        model = _read_edited(tmp_path / f"peak{peak}", _set("rpi_peak_init", [label], peak))
        try:
            p = _point(model, label)
            if frozen_to is None:
                assert p.annual_income(6) == pytest.approx(5400.0 * 1.03, rel=1e-12)
            else:
                for year in range(5, frozen_to + 1):
                    assert p.annual_income(year) == 5400.0, year
                assert p.annual_income(frozen_to + 1) == pytest.approx(
                    5400.0 * 1.03 ** 7 / 1.2, rel=1e-12)
        finally:
            model.close()


def test_the_rpi_linked_income_is_read_from_the_model_point(sec_model, tmp_path):
    """The RPI increases already given are the point's, not today's (UKLIB-SEC-PLAN.md K14).

    ``PA_UK_S`` rebuilds the income of every year from a flat ``rpi_rate``, so a model that
    dropped ``annual_income_init`` and did the same would pass the splice, which runs S and
    this model at one rate.  The committed LPI row at 42, read from S under 8%, carries the
    5% cap's increases: 5,400 x 1.05^3 = 6,251.18 in its fourth year, where the shipped 3%
    rebuilt from the start would give 5,900.66.  Its income is the column through the year
    under way, and 3% more at each anniversary after, the LPI at today's RPI.  And the LPI
    row at 24 written at 6,000.00, an income no flat RPI gives, escalates that by 3% in month
    0, its second anniversary, and pays a quarter of it at each instalment.
    """
    capped = _point(sec_model, _label(sec_model.Data.model_point_table(), "derived", 7, 42))
    assert capped.policy_year_init() == 4
    assert capped.annual_income_init() == pytest.approx(5400.0 * 1.05 ** 3, rel=1e-12)
    assert [capped.annual_income(y) for y in (4, 5, 6)] == pytest.approx(
        [5400.0 * 1.05 ** 3 * 1.03 ** n for n in range(3)], rel=1e-12)
    assert capped.annuity_pp(2) == pytest.approx(5400.0 * 1.05 ** 3 / 4, rel=1e-12)
    label = _label(_committed(), "derived", 7, 24)
    model = _read_edited(tmp_path, _set("annual_income_init", [label], 6000.0))
    try:
        p = _point(model, label)
        assert p.annual_income(2) == 6000.0
        assert p.annual_income(3) == pytest.approx(6000.0 * 1.03, rel=1e-12)
        assert p.annuity_pp(2) == pytest.approx(6000.0 * 1.03 / 4, rel=1e-12)
    finally:
        model.close()


# The LPI rows read from S under an RPI of their own, by (S point, month): above the cap,
# and below the floor (the spec's derived_refs).  Projected under that RPI from the
# valuation date, each year's income is the column's times (1 + step)^n, the step the cap,
# 5%, under 8%, and the floor, 0, under -2%: 6,251.18 rises to 6,563.73 and on to 7,978.26
# in five years, and 5,400.00 stays 5,400.00.
LPI_BOUNDS = {(7, 42): (0.08, 0.05, 6251.175, (6563.73375, 6891.9204375, 7236.516459375,
                                               7598.34228234375, 7978.2593964609375)),
              (7, 54): (-0.02, 0.0, 5400.0, (5400.0, 5400.0, 5400.0, 5400.0, 5400.0))}


def test_the_lpi_rows_hold_the_cap_and_the_floor_under_their_own_rpi(sec_model):
    """Each LPI row read under an RPI of its own, projected under it, meets its bound.

    C2 projects every committed row at the shipped References, under which the LPI's step,
    ``min(esc_lpi_cap, max(0, rpi_rate))``, is 3% on every row, so it freezes the history
    the cap and the floor made, read from S under 8% and -2%, but neither bound itself.
    Here each row is projected under the RPI it was read under (:data:`LPI_BOUNDS`), on a
    model read for it: under 8% the cap holds each year's increase at 5%, and under -2%
    the floor at 0, to the penny over five years, and the instalments follow, a quarter of
    the year's income.  Dropping the cap, or the floor, fails here in the default run, as
    the splice's RPI sets also see.
    """
    table = sec_model.Data.model_point_table()
    for (s_point, month), (rpi, step, opening, goldens) in LPI_BOUNDS.items():
        label = _label(table, "derived", s_point, month)
        assert SPEC.derived_refs[(s_point, month)] == {"rpi_rate": rpi}
        model = mx.read_model(model_path(SEC), name=_name("lpi_bounds"))
        try:
            model.Projection.rpi_rate = rpi
            row = _point(model, label)
            y0 = row.policy_year_init()
            assert row.annual_income_init() == opening
            incomes = [row.annual_income(y0 + n) for n in range(1, 6)]
            assert incomes == pytest.approx(list(goldens), abs=0.005), (label, incomes)
            assert incomes == pytest.approx([opening * (1.0 + step) ** n
                                             for n in range(1, 6)], rel=1e-12)
            first = 12 * y0 - month            # the first month of the year after y0's
            paid = [t for t in range(first, first + 12) if row.is_payment_mth(t)]
            assert paid and all(row.annuity_pp(t) == pytest.approx(goldens[0] / 4, abs=0.005)
                                for t in paid), label
        finally:
            model.close()


def test_the_income_is_taken_before_month_0s_anniversary(s_model, tmp_path):
    """The RPI-linked income is measured before month 0's own anniversary (D6, M9).

    The opening state is measured at the valuation instant, before any month-0 event, and an
    anniversary's escalation is one: on a row valued on an anniversary the column is the
    income of the year the anniversary closes, and month 0 escalates it at the valuation
    date's RPI, as every month-0 event reads the valuation date's References.  So the LPI
    point restated by the generator at its month 24, its second anniversary, read at an RPI
    of 1%, opens with its second year's income, S's ``annual_income(2)``, 5,562.00, and pays
    5,562.00 x 1.01 from month 0; and its twin, starting at the valuation date, escalates at
    1% at its first anniversary, ``t = 12``.  A column that held month 0's escalation too,
    5,728.86 at S's 3%, would pay that at the new rate's expense; and a model that read the
    column as the year after month 0's anniversary would pay 5,562.00 in month 0.
    """
    spec = dataclasses.replace(SPEC, derived=((7, 24), (6, 24)), future=(),
                               derived_refs={})
    rows, _ = build_sec_table(spec, s_model)
    model = mx.read_model(_sec_inputs(tmp_path, rows), name=_name("anniversary"))
    try:
        model.Projection.rpi_rate = 0.01
        lpi = _row(model, "derived", 7, 24)
        assert lpi.annual_income_init() == _point(s_model, 7).annual_income(2) == 5562.0
        assert lpi.policy_year_init() == 2 and lpi.policy_year(0) == 3
        assert lpi.annual_income(3) == pytest.approx(5562.0 * 1.01, rel=1e-12)
        assert lpi.annuity_pp(2) == pytest.approx(5562.0 * 1.01 / 4, rel=1e-12)
        catchup = _row(model, "derived", 6, 24)
        assert catchup.annual_income_init() == 5562.0 and catchup.rpi_peak_init() == 1.0
        assert catchup.annual_income(3) == pytest.approx(5562.0 * 1.01, rel=1e-12)
        twin = _row(model, "twin", 7, 0)
        assert twin.annual_income(2) == pytest.approx(5400.0 * 1.01, rel=1e-12)
    finally:
        model.close()


def test_the_annuitants_payments_to_date_are_read_from_the_model_point(sec_model,
                                                                       tmp_path):
    """On RPI-linked escalation the annuitant's payments to date are the point's (K14).

    ``PA_UK_S`` rebuilds the as-if-alive annuitant schedule from the start at today's RPI,
    which first-death value protection nets against, so a model that re-derived the column
    would pass the splice.  The committed catch-up row at 60 carries five years of a frozen
    5,400, 27,000.00, where today's 3% would rebuild 28,669.34: its balance at ``t = 0`` is
    50,000 - 27,000 = 23,000.00, and its value protection in the month pays that on the
    annuitant's death.  Written at 30,000.00, a history no RPI gives, the balance is
    20,000.00 at ``t = 0`` and falls by each instalment paid after.
    """
    label = _label(sec_model.Data.model_point_table(), "derived", 6, 60)
    frozen = _point(sec_model, label)
    assert frozen.cum_annuity_pp_init() == 27000.0
    assert frozen.vp_balance(0) == 23000.0
    assert frozen.claims(0, _code(frozen, "VP")) == pytest.approx(
        23000.0 * frozen.lives_death(0, 1), rel=1e-12)
    model = _read_edited(tmp_path, _set("cum_annuity_pp_init", [label], 30000.0))
    try:
        p = _point(model, label)
        assert p.vp_balance(0) == 20000.0
        assert p.vp_balance(3) == 20000.0 - p.annuity_pp(2)
        assert p.vp_balance(6) == 20000.0 - p.annuity_pp(2) - p.annuity_pp(5)
    finally:
        model.close()


def test_the_payments_to_date_and_survival_are_read_from_the_model_point(sec_model,
                                                                         tmp_path):
    """Survival and the payments to date are the point's, not the basis's of the day (K14).

    ``PA_UK_S`` rebuilds each life's survival from the start on the mortality basis it
    holds, and the expected payments to date from that survival, so a basis changed at the
    valuation date would rewrite both back to the start.  Here each is read from the model
    point, history the basis of the day reaches back over no month of: under an
    ``annuitant_adj`` of 0.5 set at the valuation date, the table basis's joint point at
    101 opens with the survival and the payments S carried there at 0.8, and only its later
    months move.  And on a record, the last-survivor row at 170 written as having paid
    45,000.00 to date, its balance opens at 5,000.00, where the scenario's expectation gives
    471.67; and the annuitant written dead on the joint table row, a record's 0, stops the
    annuitant's instalments and starts the dependant's, half of them, from its first
    payment, in month 0.
    """
    joint = _label(_committed(), "derived", 2, 101)
    columns = _committed().loc[joint, ["lives_if_init_1", "lives_if_init_2",
                                       "cum_annuity_all_init"]].tolist()
    model = mx.read_model(model_path(SEC), name=_name("basis"))
    try:
        model.Projection.annuitant_adj = 0.5
        p, base = _point(model, joint), _point(sec_model, joint)
        for each in (p, base):
            assert [each.lives_if(0, 1), each.lives_if(0, 2),
                    each.cum_annuity_all(0)] == columns
        assert p.lives_if(1, 1) > base.lives_if(1, 1)
    finally:
        model.close()
    last = _label(_committed(), "derived", 10, 170)
    model = _read_edited(tmp_path, _then(_set("cum_annuity_all_init", [last], 45000.0),
                                         _set("lives_if_init_1", [joint], 0.0)))
    try:
        p = _point(model, last)
        assert _point(sec_model, last).vp_balance(0) == pytest.approx(471.674763, abs=1e-6)
        assert p.vp_balance(0) == 5000.0
        q = _point(model, joint)
        assert q.payment_factor(0) == 0.0
        assert q.annuity_pp(0) > 0.0
        assert q.annuity_payments(0) == pytest.approx(
            q.annuity_pp(0) * 0.5 * q.lives_if(1, 2), rel=1e-12)
    finally:
        model.close()


def test_the_rpi_is_one_flat_rate_on_either_clock(sec_model, s_model):
    """``rpi_rate`` is the RPI from the valuation date on, the same on both clocks (D7).

    A flat rate is the same on the valuation clock as on the policy clock, so the splice
    runs S and this model at one rate, and no path is introduced (UKLIB-SEC-PLAN.md §9,
    item 4).  On every RPI-linked committed row in payment the relative index is 1 at the
    latest anniversary, ``rpi_index(a0)``, and rises by the shipped 3% an anniversary from
    there; and on each such row read from S at the shipped RPI, the income of the year under
    way and of the four after it is S's, to 1e-12.  The three rows read from S under an RPI of
    their own carry history S's 3% does not make, which their own tests hold.
    """
    table = sec_model.Data.model_point_table()
    linked = 0
    for label in table.index:
        p = _point(sec_model, label)
        if not (p.is_lpi5() or p.is_rpi_catchup()) or p.duration_mth_init() <= 0:
            continue
        linked += 1
        a0 = p.policy_year_init() - 1
        s_point = int(table.at[label, "source_policy_id"][3:])
        if p.is_rpi_catchup():
            assert p.rpi_index(a0) == 1.0, label
            assert p.rpi_index(a0 + 3) == pytest.approx(1.03 ** 3, rel=1e-12), label
        if (s_point, int(table.at[label, "source_mth"])) in SPEC.derived_refs:
            continue
        s = _point(s_model, s_point)
        for year in range(p.policy_year_init(), p.policy_year_init() + 5):
            assert p.annual_income(year) == pytest.approx(s.annual_income(year),
                                                          rel=1e-12), (label, year)
    assert linked == 5


def test_expense_inflation_runs_on_the_valuation_clock(sec_model, s_model):
    """Maintenance is in valuation-date pounds, for every point alike (D7).

    At the shipped 3%, the factor at ``t`` is ``1.03^(t // 12)`` on every point, whatever its
    duration, stepping on the valuation date's anniversaries.  So the worked example in
    payment 17 months pays S's month-``17 + t`` maintenance with S's factor taken out and this
    model's put in: at ``t = 0`` S's less 1.03, the inflation S had applied since the start,
    and from ``t = 7``, where S's policy anniversary falls, a further 1.03 less until the
    valuation date's own.  And the point starting 13 months on pays S's maintenance with a
    year or two more of inflation: its factor at ``t`` is ``1.03^(t // 12)``, where S's at
    ``t - 13`` is ``1.03^((t - 13) // 12)``.  This is the only test that sees inflation run
    on the policy clock: the splice sets the rate to 0, and on a point starting at ``t = 0``
    the clocks agree.
    """
    assert sec_model.Projection.inflation_rate == INFLATION
    p, s = _row(sec_model, "derived", 1, 17), _point(s_model, 1)
    fut, s6 = _row(sec_model, "future", 6, -13), _point(s_model, 6)
    for t in (0, 11, 12, 30):
        assert p.inflation_factor(t) == fut.inflation_factor(t) == (1 + INFLATION) ** (t // 12)
    for t in range(p.proj_len()):
        assert p.expenses(t) == pytest.approx(
            s.expenses(17 + t) / s.inflation_factor(17 + t) * p.inflation_factor(t),
            rel=1e-12), t
    assert p.expenses(0) == pytest.approx(s.expenses(17) / (1 + INFLATION), rel=1e-12)
    for t in range(13, fut.proj_len()):
        assert fut.expenses(t) == pytest.approx(
            s6.expenses(t - 13) * (1 + INFLATION) ** (t // 12 - (t - 13) // 12),
            rel=1e-12), t


def test_improvement_runs_on_the_policy_clock(sec_model, s_model):
    """Mortality improvement is dated by the calendar from the start, on the policy clock.

    Its exponent is ``calendar_year(t) - mort_table_year``, and ``calendar_year(t) =
    start_year() + duration(t)``, the calendar year the contract reaches whatever the
    valuation date (D7, precised at M11; UKLIB-SEC-PLAN.md §9 item 4).  So the table basis's
    joint point at 101 reads, at each ``t``, S's improvement factor and rate of policy month
    ``101 + t``, bit for bit, and its calendar year steps at its own anniversaries, ``t =
    7``, not the valuation date's.  On the valuation clock it would read the factor of
    ``2026 + t // 12``, 8 years of improvement too few at ``t = 0``.
    """
    p, s = _row(sec_model, "derived", 2, 101), _point(s_model, 2)
    assert (p.calendar_year(6), p.calendar_year(7)) == (2034, 2035)
    for t in range(0, p.proj_len(), 7):
        for life in (1, 2):
            assert p.improve_factor(t, life) == s.improve_factor(101 + t, life), (t, life)
            assert p.mort_rate(t, life) == s.mort_rate(101 + t, life), (t, life)


def test_new_business_brings_no_premium_and_no_acquisition(sec_model):
    """An annuity starting in a month brings its count and nothing else (§6.7).

    The purchase price is a pricing input, as in ``PA_UK_S``: no cash flow in the issue
    month but the instalments, any value protection and the maintenance, on every point.
    ``liability_cf`` is the sum of those three, and ``net_cf`` its negative, in every month,
    the issue month of the point starting 13 months on among them, where the expense is the
    maintenance alone.
    """
    table = sec_model.Data.model_point_table()
    for key, point_id in zip(point_keys(sec_model), table.index):
        p = projection(sec_model, key)
        df = p.result_cf()
        total = df["annuity_payments"] + df["claims_vp"] + df["claims_prop"] + df["expenses"]
        assert ((df["liability_cf"] - total).abs() <= 1e-9).all(), point_id
        assert (df["net_cf"] == -df["liability_cf"]).all(), point_id
    fut = _row(sec_model, "future", 6, -13)
    assert fut.expenses(13) == pytest.approx(
        fut.expense_maint / 12.0 * fut.inflation_factor(13) * fut.pols_if(13), rel=1e-12)


def test_the_payment_schedule_runs_on_the_policy_clock(sec_model):
    """The payment months, the months since a payment and the next payment read the policy
    month, not ``t`` (R1a).

    ``PA_UK_S`` reads ``(t + 1) % step``, ``t % step`` and its months since a payment on its
    one clock, which is the policy clock only on a point starting at ``t = 0``.  The worked
    example in payment 17 months pays quarterly in arrears at policy months 17, 20, ..., so
    at ``t = 0, 3, ...``; at ``t = 0`` two months have passed since the last payment date,
    policy time 15, at ``t = 1`` none, the month-17 instalment having fallen at policy time
    18, and its next payment is policy month 20; the proportionate payment's
    point at 16, the month of the death, accrues one month since policy time 15 and pays a
    proportionate quarter of its year's 5,562, ``1.5 / 3 x 1,390.50``, on the annuitant's
    death, with its value protection.  The point starting 13 months on pays at policy months
    2, 5, ..., so at ``t = 15, 18, ...``.
    """
    p = _row(sec_model, "derived", 1, 17)
    assert [t for t in range(9) if p.is_payment_mth(t)] == [0, 3, 6]
    assert (p.mths_since_payment(0), p.mths_since_payment(1), p.next_payment_mth(1)) == (
        2, 0, 20)
    prop = _row(sec_model, "derived", 9, 16)
    assert (prop.mths_since_payment(0), prop.next_payment_mth(0)) == (1, 17)
    assert prop.claims(0, _code(prop, "PROP")) == pytest.approx(695.25, abs=0.005)
    assert prop.claims(0, _code(prop, "VP")) == pytest.approx(43209.50, abs=0.005)
    fut = _row(sec_model, "future", 6, -13)
    assert [t for t in range(13, 22) if fut.is_payment_mth(t)] == [15, 18, 21]


# ---------------------------------------------------------------------------
# The cap on mortality
#
# mort_rate caps the annual rate at 1, the bound second, as PA_UK_S's does since M0.  It
# binds on S point 8, rated 1.35, from policy month 576, attained age 113, where 1.35 times
# the table rate, the adjustment and the improvement passes 1, to the end of its frame.


def test_an_annual_mortality_past_1_is_capped_in_both_models(sec_model, s_model):
    """Where the rated annual mortality passes 1, both models' rate is the float 1.0.

    On S point 8, rated 1.35, the product of the rating and the improved table rate passes 1
    from policy month 576 to the end of its 600-month frame (UKLIB-SEC-PLAN.md §6.7).  Both
    models cap it: ``mort_rate`` and the monthly rate are 1.0 in every one of those months,
    the float, not the int 1, which compares equal to it, and floats below 1 in every month
    before.  So every contract's annuitant alive at the start of the first capped month dies
    in it, and none is alive after it.  On the twin, and on the committed row restated in
    payment the month before, at 575, which T2 and the committed rows' test compare with S
    in every cell: from its ``t = 1``, on its own clock.  Every report holds finite floats.
    """
    s = _point(s_model, 8)
    capped = [t for t in range(s.proj_len())
              if s.rating_factor(1) * s.mort_rate_base(t, 1) * s.improve_factor(t, 1) > 1.0]
    assert capped == list(range(576, 600))
    for case, first in ((("twin", 8, 0), 576), (("derived", 8, 575), 1)):
        p = _row(sec_model, *case)
        for rate in (p.mort_rate, p.mort_rate_mth):
            assert all(type(rate(t, 1)) is float and rate(t, 1) < 1.0
                       for t in range(first)), case
            assert [(type(rate(t, 1)), rate(t, 1)) for t in range(first, p.proj_len())] == (
                [(float, 1.0)] * (p.proj_len() - first)), case
        assert p.lives_if(first, 1) > 0.0 and p.lives_if(first + 1, 1) == 0.0, case
        for report in REPORTS:
            frame = p.cells[report]()
            assert (frame.dtypes == "float64").all(), (case, report)
            assert np.isfinite(frame.to_numpy()).all(), (case, report)
    for t in range(576, 600):
        assert (type(s.mort_rate(t, 1)), s.mort_rate(t, 1)) == (float, 1.0)


# A NaN sent to a bound written with its bound second, as (the bound, the Reference that
# feeds it, set to NaN on a model read for the test before it computes anything, the S
# point whose twin reads it, and the calls that must give the float NaN).  The cap reads
# annuitant_adj on the table basis, through the base rate.  A bound written first would turn
# the NaN into the bound: a blank input read as certain death.  proj_len() refuses an
# annuitant_adj that is not a number, so no report projects it; the calls here read no
# frame.  This form runs compiled unchanged, since a compiled ItemSpace takes the References
# when it is made (USLIB-SEC-PLAN.md §5.1, step 6, precised at M12).
NAN_BOUNDS = [
    ("the mortality cap, min(q, 1.0)", "annuitant_adj", 2,
     [("mort_rate", (0, 1)), ("mort_rate", (300, 2)), ("mort_rate_mth", (100, 1))]),
    ("the mortality cap on the rated life, min(q, 1.0)", "annuitant_adj", 8,
     [("mort_rate", (580, 1)), ("mort_rate_mth", (590, 1))]),
]


@pytest.mark.parametrize("bound, ref, s_point, calls", NAN_BOUNDS,
                         ids=[c[0] for c in NAN_BOUNDS])
def test_a_nan_that_reaches_a_bound_stays_nan(bound, ref, s_point, calls):
    """A NaN that reaches the bound written second stays NaN, and is not read as the bound.

    ``min`` keeps its first argument unless a later one compares smaller, in modelx and
    compiled alike, and no comparison with NaN holds, so with its bound first the cap would
    turn a NaN into 1: certain death, where the rated life's cap binds as on point 8 at
    580.  It is written with its bound second, as ``PA_UK_S`` writes it (:data:`NAN_BOUNDS`):
    the Reference that feeds it is set to NaN on a model read for the test, and every call
    must give the float NaN.  The cells are called on their own, without the frame:
    ``proj_len()`` refuses the Reference at NaN before a report reaches the bound (the domain
    test).  Every other ``min`` and ``max`` keeps ``PA_UK_S``'s order, and the domains and
    ``Data`` keep a NaN from each.
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


@pytest.mark.parametrize("check, resid", [
    ("check_lives_roll_fwd", "check_lives_roll_fwd_resid"),
    ("check_payment_factor", "check_payment_factor_resid")])
def test_a_check_fails_a_residual_that_is_not_a_number(check, resid):
    """Each check returns False where its residual is NaN (§7.1, item 11).

    A check is ``abs(resid) < tolerance`` over the frame, which no NaN passes, as
    ``PA_UK_S``'s is; but no input the frame accepts gives a NaN residual, so the residual's
    formula is replaced, on a model read for the test, by one that returns NaN in every
    month.  Then the check is the bool False on every committed point, where with its own
    formula it is True, as it is first shown on the worked example's twin and on the rated
    life at 575, each released once read: the whole survival check is quadratic in the
    frame, and the conventions run it on every point.  A check that asked whether any
    residual was past its tolerance would pass NaN.
    """
    model = mx.read_model(model_path(SEC), name=_name("nan_resid"))
    try:
        table = model.Data.model_point_table()
        for kind, s_point, month in (("twin", 1, 0), ("derived", 8, 575)):
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
    kind and each of :data:`PER_LIFE_OUTSIDE` for each life the point covers, at each of
    ``months``, every one outside the frame; and before the contract is on the books, each of
    :data:`BEFORE_ENTRY`, and survival of each life, 0.0.  Then whether any of
    :data:`IN_COVER_ONLY` was evaluated on the way, which only a fresh ItemSpace can say.  A
    cell that raises is reported as a fault too, so the scan goes on.
    """
    faults = []
    lives = (1, 2) if p.is_joint() else (1,)
    for t in months:
        calls = [(name, (t,), want) for name, want in OUTSIDE_COVER.items()]
        calls += [("pols_if_at", (t, _code(p, timing)), 0.0) for timing in TIMINGS]
        calls += [("claims", (t, _code(p, kind)), 0.0) for kind in KINDS]
        calls += [(name, (t, life), 0.0) for name in PER_LIFE_OUTSIDE for life in lives]
        if t < p.t_entry():
            calls += [(name, (t,), 0.0) for name in BEFORE_ENTRY]
            calls += [("lives_if", (t, life), 0.0) for life in lives]
        for name, args, want in calls:
            try:
                got = p.cells[name](*args)
            except Exception as err:        # reported, so the scan goes on
                faults.append(f"{where}: {name}{args} raised {_raised(err)}")
                continue
            if got != want or type(got) is not type(want):
                faults.append(f"{where}: {name}{args} = {got!r}, not {want!r}")
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

    On every committed point, in every month before the start and in the first month after
    the frame, ``t = proj_len()``, on a model that evaluates nothing else.  So afterwards
    none of :data:`IN_COVER_ONLY` may hold a value outside the frame at all: ``is_active``'s
    docstring promises that outside the frame no count evaluates a rate, and no table is
    read at a policy year or an attained age the contract does not have.

    The committed table's one point starting after the valuation date is the catch-up point,
    so on it a cell tied to another basis would hold zero before the start, guarded or not.
    So the same scan runs on the splice's future rows, the core's or, with
    ``UKLIB_SEC_FULL=1``, all of them: the worked example, the single life in advance, the
    guarantee past the age stop and the LPI among them.  Each row is made afresh first and
    released after.

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
            where = _case_id(rates, "future", s_point, -k)
            faults += _outside_cover_faults(p, where, [*range(k), p.proj_len()])
        finally:
            _release(sec, key)
    assert futures and not faults, (
        f"{len(faults)} faults outside the frame, first:\n  " + "\n  ".join(faults[:20]))


def test_the_points_sum_row_by_row_into_a_block(spliced):
    """Row ``t`` is the same month on every point, so a block is its frames summed (D3).

    S point 1's twin, the point restated at month 12 and the point starting 12 months on,
    summed as ``run_sec.py --block`` sums them, are indexed 0..647 and equal S's frame added
    to itself moved 12 months earlier and 12 months later.  A model whose frames sat on the
    policy clock would fail it.
    """
    s, sec = spliced.pair("shipped")
    cases = (("shipped", "derived", 1, 12), ("shipped", "future", 1, -12))
    keys = [_row_key(sec, *case[1:]) for case in cases if SEC_FULL or case in CORE_GRID]
    if len(keys) < 2:
        keys = None
    twin = _row_key(sec, "twin", 1, 0)
    if keys is None:
        pytest.skip("the block's rows are the full grid's")
    try:
        frames = [projection(sec, key).result_cf() for key in (twin, *keys)]
    finally:
        for key in (twin, *keys):
            _release(sec, key)
    block = pd.concat(frames).groupby(level="t").sum()
    sdf = _point(s, 1).result_cf()
    expected = pd.concat([sdf, sdf.set_axis(sdf.index - 12).loc[0:],
                          sdf.set_axis(sdf.index + 12)]).groupby(level=0).sum()
    assert list(block.index) == list(range(648))
    assert frame_mismatches(expected, block) == []


def _extract():
    """The committed table as an administration extract would hold it: without the
    generator's columns, and labelled :data:`EXTRACT_LABELS`."""
    extract = _committed().drop(columns=list(generated_columns(SPEC)))
    extract.index = pd.Index(EXTRACT_LABELS, name="point_id")
    return extract


def test_an_in_force_extract_needs_none_of_the_generator_columns(sec_model, tmp_path):
    """The model reads the in-force interface and S's columns, never where a row came from,
    and names each point by its label, wherever the row stands.

    ``row_kind``, ``source_policy_id``, ``source_mth`` and ``source_refs`` record how the
    generator made each shipped row, from which S row, at which month and under which
    References, and an administration extract carries none of them.  Read without them,
    and with every label changed, every point projects what the committed table projects,
    in ``result_cf`` and ``result_pols``, to 1e-12, and ``run_sec.py``, run beside that
    extract, prints the point without saying where it came from.  On every shipped row
    ``source_mth`` equals ``duration_mth``, so a formula that read the one for the other would
    pass every test that leaves ``duration_mth`` as generated.  And a refusal names the
    extract's label.
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
        for key, base_key in zip(point_keys(model), point_keys(sec_model)):
            mine, base = projection(model, key), projection(sec_model, base_key)
            for report in REPORTS:
                assert frame_mismatches(base.cells[report](), mine.cells[report](),
                                        rtol=1e-12, atol=1e-12) == [], (key, report)
            _release(model, key)
    finally:
        model.close()
    runner = folder.parent / "run_sec.py"
    shutil.copy(model_path(SEC).parent / "run_sec.py", runner)
    label = extract.index[extract["policy_id"] == "PA-000001-M17"][0]
    out = _run_sec(runner, str(label))
    p = _row(sec_model, "derived", 1, 17)
    assert out.splitlines()[:2] == [
        f"model point {label}: PA-000001-M17 - M65 with dependant F62 at 50%, purchase "
        f"price 100,000, income 5,400.00 a year, 4 payments in arrears, fixed escalation, "
        f"value protection 50% on first_death, scenario basis",
        f"at the valuation date: {_standing(p)}"]
    last = extract.index[extract["policy_id"] == "PA-000002-M635"][0]
    moved = _set("duration_mth", [last], 637)(extract)
    model = mx.read_model(_sec_inputs(tmp_path / "moved", moved), name=_name("moved"))
    try:
        _refused(_point(model, last).result_cf,
                 f"point_id {last}: duration_mth 637 is at or past the end of the "
                 f"projection, policy month 636")
    finally:
        model.close()


def _standing(p):
    """What ``run_sec.py`` says of point ``p`` at the valuation date, stated here."""
    d = p.duration_mth_init()
    if d < 0:
        return f"to start at t = {-d}, {-d} months after the valuation date"
    if d == 0:
        return "starting at the valuation date, t = 0"
    alive = f"survival {p.lives_if_init(1):.6g}"
    if p.is_joint():
        alive += f", the dependant's {p.lives_if_init(2):.6g}"
    return (f"in payment {d} months: policy year {p.policy_year(0)}, annuitant aged "
            f"{p.age(0, 1)}, {alive}, income {p.annual_income_init():,.2f} a year, "
            f"{p.cum_annuity_all_init():,.2f} paid to date a contract")


def test_run_sec_prints_a_point_and_the_block(sec_model):
    """The runner prints one point, saying where it came from, and the block (D8).

    Each mode in an interpreter of its own, as a user runs it, with exit code 0 and ASCII
    output, so that it prints on a Windows console under any code page.  The numbers are
    the model's.  The worked example, the runner's default, with its lines at the valuation
    date, each asserted whole, so that a longer number cannot pass for the one asserted,
    and its first twelve rows of cash flows and counts.  Point 11, the worked example in
    payment 17 months; point 13, the guarantee's point at 120, whose frame ends at the age
    stop; and point 20, to start 13 months on: each with the lines that say where its row
    came from and where it stands, which only the committed table's generator columns can
    say.  And the block: a line for each of the 23 points, in table order, its first twelve
    rows, which must be the committed points' frames summed row by row, as this test sums
    them, and those frames summed into projection years, each year's ``pols_if`` the one of
    its first month.  Nothing else runs the runner on the committed table.
    """
    runner = model_path(SEC).parent / "run_sec.py"
    out = _run_sec(runner)
    assert out.splitlines()[:3] == [
        "model point 1: PA-000001 (S's PA-000001) - M65 with dependant F62 at 50%, purchase "
        "price 100,000, income 5,400.00 a year, 4 payments in arrears, fixed escalation, "
        "value protection 50% on first_death, scenario basis",
        "at the valuation date: starting at the valuation date, t = 0",
        "proj_len = 636 months from the valuation date (t = 0..635); the frame ends at "
        "policy month 636, the age stop on the youngest life"]
    anchor = _row(sec_model, "twin", 1, 0)
    assert anchor.result_cf().head(12).round(2).to_string() in out
    assert anchor.result_pols().head(12).round(6).to_string() in out
    for point_id, lines in (
            ("11", ["model point 11: PA-000001-M17 (S's PA-000001 at its month 17) - M65 "
                    "with dependant F62 at 50%, purchase price 100,000, income 5,400.00 a "
                    "year, 4 payments in arrears, fixed escalation, value protection 50% on "
                    "first_death, scenario basis",
                    f"at the valuation date: {_standing(_row(sec_model, 'derived', 1, 17))}",
                    "proj_len = 619 months from the valuation date (t = 0..618); the frame "
                    "ends at policy month 636, the age stop on the youngest life"]),
            ("13", ["model point 13: PA-000003-M120 (S's PA-000003 at its month 120) - M65 "
                    "with dependant F62 at 50%, purchase price 100,000, income 5,400.00 a "
                    "year, 4 payments in arrears, fixed escalation, guarantee 120 months, "
                    "scenario basis",
                    f"at the valuation date: "
                    f"{_standing(_row(sec_model, 'derived', 3, 120))}",
                    "proj_len = 516 months from the valuation date (t = 0..515); the frame "
                    "ends at policy month 636, the age stop on the youngest life"]),
            ("20", ["model point 20: PA-000006-F13 (S's PA-000006, starting 13 months on) "
                    "- M65 with dependant F62 at 50%, purchase price 100,000, income "
                    "5,400.00 a year, 4 payments in arrears, rpi_catchup escalation, value "
                    "protection 50% on first_death, table basis",
                    "at the valuation date: to start at t = 13, 13 months after the "
                    "valuation date",
                    "proj_len = 649 months from the valuation date (t = 0..648); the frame "
                    "ends at policy month 636, the age stop on the youngest life"])):
        assert _run_sec(runner, point_id).splitlines()[:3] == lines, point_id
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


# run_sec.py run as though it sat at /m/products/pension_annuity, in a products/ folder
# whose parent carries no build tool: the source compiled under that name, so that its own
# __file__ is it.
SHALLOW_RUN = """\
import sys
source = open(sys.argv[1], encoding="utf-8").read()
where = "/m/products/pension_annuity/run_sec.py"
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
    as ``source_refs`` records them, point 21's ``under rpi_rate -0.02``, and no other row's
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
    assert space["origin"](21) == (
        " (S's PA-000006 at its month 60, under rpi_rate -0.02)")


def _defaulted(model_name):
    """The cells of ``model_name``'s Projection with a parameter that has a default, sorted,
    read from its source, as the C step's build reads it."""
    source = (model_path(model_name) / "Projection" / "__init__.py").read_text(
        encoding="utf-8")
    return sorted(node.name for node in ast.parse(source).body
                  if isinstance(node, ast.FunctionDef)
                  and (node.args.defaults or any(node.args.kw_defaults)))


def test_no_cell_takes_a_default():
    """No cell has a defaulted parameter, ``PA_UK_S``'s total among them (R12).

    A compiled model declares a defaulted parameter in its ``.pxd`` as ``long long x=*``,
    which the typing guard would read as a parameter of that name, and ``None`` is no C
    integer, so ``PA_UK_S``'s one, ``claims``' ``kind=None``, its total, is the code ``ALL``
    here, ``claims(t, ALL)``, as ``Term_UK_SEC``'s is.
    """
    assert _defaulted(TWIN) == ["claims"]
    assert _defaulted(SEC) == []


# The texts a computed cell may hold beside a column's name read off the model point: at
# stage "E", the kinds and the timings, which the C step made int References, as it did
# Term's, CI's and ULB's (R9); at stage "EC", none.
CODES = frozenset()

# The cells the static check leaves alone: the reporting cells, the reports, the checks,
# the model point and the five label accessors, which stay Python.  At stage "E" it left
# the rest of UKLIB-SEC-PLAN.md §6.7's C list too, which the C step made C: the seven
# decodes, the claims total, horizon_mths's list and the mortality table's reader.
STATIC_EXEMPT = {
    "result_cf", "result_pols", "check_lives_roll_fwd", "check_payment_factor",
    "check_guarantee_xor", "check_vp_bound", "model_point", "sex", "payment_timing",
    "escalation_type", "vp_basis", "mort_basis"}


def test_no_computed_cell_builds_a_python_object(sec_model):
    """No computed cell builds a tuple, a text or a generator but to raise (§6.7, *C*).

    The C step's static check (C5, ``test_compiled_conventions_uk.py``) refuses a Python
    object in a computed cell; this held, at stage ``E``, that the C step would restructure
    nothing beyond UKLIB-SEC-PLAN.md §6.7's C list, and holds the model to it now.  No
    ``Projection`` cell but the reporting ones (:data:`STATIC_EXEMPT`, which is exactly
    ``uk_sec_support.reporting_cells``) holds a tuple, a list, a set, a dict, a
    comprehension, a generator or an f-string, or a text other than a column's name read
    off ``model_point()``, which no computed cell reads now, but inside a ``raise``
    statement, and but the index of a table read, ``[s, x]``, which C5 admits too, read
    from the source as the build reads it.  ``try`` is allowed: a power
    that leaves the floats raises Python's ``OverflowError``, which the cell names.  Every
    cell of the Space is read, and every exemption is a cell of it.
    """
    source = (model_path(SEC) / "Projection" / "__init__.py").read_text(encoding="utf-8")
    built = (ast.Tuple, ast.List, ast.Set, ast.Dict, ast.GeneratorExp, ast.ListComp,
             ast.SetComp, ast.DictComp, ast.JoinedStr, ast.Lambda)
    found, read = [], set()
    for node in ast.parse(source).body:
        if not isinstance(node, ast.FunctionDef):
            continue
        read.add(node.name)
        if node.name in STATIC_EXEMPT:
            continue
        raises = {id(n) for r in ast.walk(node) if isinstance(r, ast.Raise)
                  for n in ast.walk(r)}
        columns = {id(n) for s in ast.walk(node)
                   if isinstance(s, ast.Subscript) and isinstance(s.value, ast.Call)
                   and getattr(s.value.func, "id", None) == "model_point"
                   for n in ast.walk(s.slice)}
        body = node.body[1:] if ast.get_docstring(node) is not None else node.body
        index = {id(n.slice) for statement in body for n in ast.walk(statement)
                 if isinstance(n, ast.Subscript) and isinstance(n.slice, ast.Tuple)}
        for inner in (n for statement in body for n in ast.walk(statement)):
            if id(inner) in raises or id(inner) in index:
                continue
            if isinstance(inner, built):
                found.append(f"{node.name}: {type(inner).__name__} at line {inner.lineno}")
            elif (isinstance(inner, ast.Constant) and isinstance(inner.value, str)
                  and inner.value not in CODES and id(inner) not in columns):
                found.append(f"{node.name}: the text {inner.value!r} at line "
                             f"{inner.lineno}")
    assert read == set(sec_model.Projection.cells)
    assert STATIC_EXEMPT == reporting_cells(SEC, sec_model.Projection)
    assert not found, found


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
    outside the parentheses and quotes of the column, ``claims`` of ``claims(t, "VP")``; a
    cell of two names, ``expense_maint, inflation_rate``, maps both.
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


# What only PA_UK_S's docstrings may say: a reference into its Spaces, which the SEC pages
# would link to the wrong model; its clock, t counting months from the annuity start date;
# and the first year's income under the name SEC gives the year under way.
STALE = re.compile(r"~\.PA_UK_S\.|``t`` counts \*\*months from the annuity start date\*\*"
                   r"|A\(1\)\s+annual_income_init\(\)")


def test_the_docstrings_describe_the_valuation_clock(sec_model, s_model):
    """The docstrings say what this model is, and none says what only PA_UK_S is.

    Whitespace is collapsed first, as ``test_model_conventions_uk`` collapses it, so that a
    phrase split across a line break still matches.  The model docstring names the valuation
    date, BasicTerm_SE, the policy clock, the SEC table, the payout chassis and the product.
    The symbol map in the Projection docstring maps every cell running in force adds, which
    are exactly the cells ``PA_UK_S`` lacks, and names nothing the model lacks: every name in
    it is a cell or a Reference.  No row of a simple table in any docstring puts text between
    two of its columns (:func:`_table_overruns`), which would drop the table from the
    rendered page.  And no docstring says what :data:`STALE` matches.
    """
    flat = {where: re.sub(r"\s+", " ", doc) for where, doc in _docs(sec_model)}
    for phrase in ("valuation date", "BasicTerm_SE", "duration_mth", TABLE, "SPIA_US_SEC",
                   "pension annuit"):
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
    assert not stale, f"docstrings that describe PA_UK_S: {stale}"


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


def test_the_sec_model_reads_the_s_table_in_place(sec_model, s_model):
    """One copy of the mortality table serves both models (D1).

    The two ``input_dir()`` s are one directory, and SEC's filename References are S's with
    ``model_point_file`` changed, to ``model_point_table_sec.csv``: an edit to the table
    reaches both models, and the two can never drift apart.  And every Reference of S's is
    the SEC model's at S's value, but those it adds, the youngest issue age, the largest
    limiting age and the C step's codes, so that no assumption moves between the two; S's
    ``point_id`` is SEC's ``idx``, the position.  The improvement ages are S's values as
    floats, 90.0 and 110.0, which the compiled model holds as ``double``, so that a
    fraction set on either reads in both engines as modelx reads it; each is the same
    number as S's, and every value computed from it the same float.
    """
    assert sec_model.Data.input_dir() == s_model.Data.input_dir()
    files = {r: v for r, v in s_model.Data.refs.items() if r.endswith("_file")}
    assert {r: v for r, v in sec_model.Data.refs.items() if r.endswith("_file")} == {
        **files, "model_point_file": TABLE}
    plain = (bool, int, float, str)
    s_refs = {r: v for r, v in s_model.Projection.refs.items()
              if isinstance(v, plain) and r != "point_id"}
    sec_refs = {r: v for r, v in sec_model.Projection.refs.items()
                if isinstance(v, plain) and r != "idx"}
    assert s_model.Projection.point_id == 1 and sec_model.Projection.idx == 0
    assert sec_refs == {**s_refs, "issue_age_min": 0, "omega_age_max": 116, "BEF_NB": 0,
                        "BEF_DECR": 1, "VP": 0, "PROP": 1, "ANNUITANT": 2, "ALL": 3}
    assert {r: type(sec_refs[r]) for r in ("improve_flat_age", "improve_taper_age")} == {
        "improve_flat_age": float, "improve_taper_age": float}


def test_the_core_grid_reaches_every_branch(spliced, splice_records):
    """What the default run's T2 and T3 cases reach, which the full grid only multiplies.

    The default run thins the splice to a core (the module docstring), and this test is what
    keeps the thinning from costing a branch.  First, statically, over S's table with the
    variants, each property below holds of some core case: every escalation basis, timing,
    frequency and mortality basis, each value-protection basis, the guarantee with and
    without overlap, the proportionate payment, a single and a joint life, a rating, each
    variant, and each RPI set; and each kind of valuation month: the first months, a payment
    month and one between, on an anniversary, the month before and after one, about the
    scenario death, about the guarantee's end, about value protection running out, about the
    cap, past the limiting age and the last month of a frame.  And of some core future case:
    starting off the valuation anniversaries and on them, more than a year on, each basis,
    a variant and an RPI set.

    Then, on the splice's models, of some core row, each of :data:`AT_VALUATION` and
    :data:`IN_FRAME`, what no column of the table shows: every opening-state column in use,
    and every branch and both sides of every ``min`` and ``max`` the full grid reaches.

    Each core row's branches were recorded by the T2 or T3 case that compared it
    (:func:`_scan`), and a row no case has recorded is evaluated here.  With
    ``UKLIB_SEC_FULL=1`` it asks the same of the full grid's rows, which must reach nothing
    the core does not.
    """
    assert set(CORE_SPLICES) <= set(SPLICES) and set(CORE_FUTURES) <= set(FUTURES)
    s_table = _s_table_with_variants()

    def at(p, column):
        return s_table.at[p, column]

    def flag(p, column):
        return str(at(p, column)).lower() == "true"

    splices = {
        **{f"{e} escalation": (lambda r, k, p, d, e=e: at(p, "escalation_type") == e)
           for e in ("level", "fixed", "lpi5", "rpi_catchup")},
        **{f"{w} timing": (lambda r, k, p, d, w=w: at(p, "timing") == w)
           for w in ("arrears", "advance")},
        **{f"{m} payments a year": (lambda r, k, p, d, m=m: at(p, "frequency") == m)
           for m in (12, 4, 2, 1)},
        **{f"the {b} basis": (lambda r, k, p, d, b=b: at(p, "mort_basis") == b)
           for b in ("table", "scenario")},
        **{f"value protection on {b}": (
            lambda r, k, p, d, b=b: at(p, "vp_pct") > 0 and at(p, "vp_basis") == b)
           for b in ("first_death", "last_survivor")},
        "a guarantee without overlap": lambda r, k, p, d: (
            at(p, "guarantee_months") > 0 and not flag(p, "overlap")),
        "a guarantee with overlap": lambda r, k, p, d: (
            at(p, "guarantee_months") > 0 and flag(p, "overlap")),
        "the proportionate payment": lambda r, k, p, d: flag(p, "proportion"),
        "a single life": lambda r, k, p, d: not flag(p, "dependant_present"),
        "a rating": lambda r, k, p, d: at(p, "rating_multiplier") > 1.0,
        **{f"variant {v}": (lambda r, k, p, d, v=v: p == v) for v in VARIANTS},
        **{f"the {s} set": (lambda r, k, p, d, s=s: r == s) for s in SPLICE_SETS},
        "in the second month": lambda r, k, p, d: d == 1,
        "on an anniversary": lambda r, k, p, d: d % 12 == 0,
        "in the month before an anniversary": lambda r, k, p, d: d % 12 == 11,
        "in the month after an anniversary": lambda r, k, p, d: d % 12 == 1 and d > 12,
        "about the scenario death": lambda r, k, p, d: (
            at(p, "mort_basis") == "scenario" and 15 <= d <= 17),
        "about the guarantee's end": lambda r, k, p, d: (
            at(p, "guarantee_months") > 0 and 119 <= d <= 122),
        "about value protection running out": lambda r, k, p, d: d in (101, 102, 170, 171),
        "about the cap": lambda r, k, p, d: d in (575, 576),
        "past the limiting age": lambda r, k, p, d: d >= 600,
        "the last month of a frame": lambda r, k, p, d: d == FRAME[p] - 1,
    }
    futures = {
        "starting off the anniversaries": lambda r, p, k: k % 12 != 0,
        "starting on them": lambda r, p, k: k % 12 == 0,
        "starting more than a year on": lambda r, p, k: k > 12,
        **{f"{e} escalation": (lambda r, p, k, e=e: at(p, "escalation_type") == e)
           for e in ("level", "fixed", "lpi5", "rpi_catchup")},
        "a variant": lambda r, p, k: p in VARIANTS,
        "an RPI set": lambda r, p, k: r != "shipped",
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
# The C step's representation (UKLIB-SEC-PLAN.md §6.7, *C*)
#
# Data decodes each model point's text into the flag the projection branches on, holds
# each column a projection reads as an int64 or float64 vector, with a 0/1 flag beside a
# column only some points' projections read, and turns the mortality table into an array
# by sex and age (USLIB-SEC-PLAN.md R5-R8); a timing and a kind are int codes, and the
# claims total is a code of its own (R9, R12); and survival and the payments to date are
# blocked by policy year (K12), which the depth tests above hold.  These tests hold the
# representation in modelx, with no compiler, in seconds: the compiled section after the
# fingerprint holds the compiled model to modelx on it.


def test_the_all_total_is_s_total_bit_for_bit(sec_model, s_model):
    """``claims(t, ALL)`` is ``PA_UK_S``'s ``claims(t)``, its ``sum``, to the last bit.

    S totals its two kinds with Python's ``sum``, which compensates, and the total here is
    written left to right from ``0.0`` (``Projection.claims``), which is ``sum``'s float
    wherever at most two kinds are non-zero in a month, and there are only two.  T1
    compares the totals to 1e-9; this compares them by ``float.hex``: on every committed
    point, in every month of its frame and the month after it, with ``sum`` of the row's
    own two kinds, both of them paying in some month, which is asserted, value protection
    and the proportionate payment together on point 12 at ``t = 0``; and on every twin of
    S's new business, whose kinds are S's to the last bit, with S's ``claims(t)`` itself.
    A row restated in payment opens on a state read back from the CSV, which may part from
    S's by an ulp, so its total is held to its own kinds' ``sum``.
    """
    total = _code(sec_model.Projection, "ALL")
    vp, prop = (_code(sec_model.Projection, kind) for kind in KINDS)
    found, both = [], 0
    table = sec_model.Data.model_point_table()
    for key, point_id in zip(point_keys(sec_model), table.index):
        p = projection(sec_model, key)
        for t in range(p.proj_len() + 1):
            kinds = [p.claims(t, vp), p.claims(t, prop)]
            both += kinds[0] != 0.0 and kinds[1] != 0.0
            if p.claims(t, total).hex() != sum(kinds).hex():
                found.append(f"point {point_id}, t = {t}: {p.claims(t, total)!r}, the "
                             f"kinds' sum {sum(kinds)!r}")
    for point_id in table.index[table["row_kind"] == "twin"]:
        s, p = _point(s_model, point_id), _point(sec_model, point_id)
        for t in range(p.proj_len()):
            if p.claims(t, total).hex() != s.claims(t).hex():
                found.append(f"point {point_id}, t = {t}: {p.claims(t, total)!r}, S "
                             f"{s.claims(t)!r}")
    assert both, both
    assert not found, found[:10]


# One S point per value a decoded column can hold, as (the S point it changes, the columns
# it changes): each timing; each escalation basis; each value-protection basis, elected;
# each mortality basis; each sex of each life; a dependant and none; the overlap each way;
# the proportionate payment each way; each frequency; and, on the scenario basis, which
# never reads it, a start year with a fraction, which int truncates, above .5 so that a
# decode that rounded would part.
DECODED = [
    (2, {"timing": "advance"}), (5, {"timing": "arrears"}),
    (1, {"escalation_type": "level"}), (1, {"escalation_type": "lpi5"}),
    (1, {"escalation_type": "rpi_catchup"}), (5, {"escalation_type": "fixed",
                                                  "escalation_rate": 0.02}),
    (10, {"vp_basis": "first_death"}), (1, {"vp_basis": "last_survivor"}),
    (1, {"mort_basis": "table"}), (2, {"mort_basis": "scenario"}),
    (2, {"annuitant_sex": "F", "dependant_sex": "M"}), (5, {"annuitant_sex": "F"}),
    (5, {"dependant_present": True, "dependant_age": 60, "dependant_sex": "F",
         "dependant_rating": 1.2, "dependant_pct": 0.6}),
    (2, {"dependant_present": False}),
    (3, {"overlap": True}), (4, {"overlap": False}),
    (9, {"proportion": False}), (1, {"proportion": True}),
    (2, {"frequency": 12}), (5, {"frequency": 4}), (2, {"frequency": 2}),
    (5, {"frequency": 1, "timing": "arrears"}),
    (1, {"start_year": 2026.7}),
]

# The cells each decoded point is compared on, PA_UK_S's own, which read the text or the
# number themselves, and the decodes here, each against S's comparison of the text.
DECODING_CELLS = ("payment_timing", "escalation_type", "vp_basis", "mort_basis",
                  "is_joint", "overlap", "proportion", "payment_freq", "escalation_rate",
                  "guarantee_mths", "vp_pct", "purchase_price", "dependant_pct",
                  "start_year", "annual_income_init")
DECODES = {"is_arrears": lambda s: s.payment_timing() == "arrears",
           "is_level": lambda s: s.escalation_type() == "level",
           "is_fixed": lambda s: s.escalation_type() == "fixed",
           "is_lpi5": lambda s: s.escalation_type() == "lpi5",
           "is_rpi_catchup": lambda s: s.escalation_type() == "rpi_catchup",
           "is_first_death": lambda s: s.vp_basis() == "first_death",
           "is_scenario": lambda s: s.mort_basis() == "scenario"}


def _decoded_tables(tmp_path):
    """S's points of :data:`DECODED`, in a copy of S's table, and the SEC twins the
    generator makes of them: ``(S model, SEC model, S labels)``, both to be closed."""
    s_table = _s_table()
    rows = []
    for i, (base, changes) in enumerate(DECODED, start=1):
        row = s_table.loc[[base]].assign(**changes, policy_id=f"PA-8{i:05d}")
        row.index = pd.Index([i], name="point_id")
        rows.append(row)
    table = pd.concat(rows)
    s = mx.read_model(temp_inputs(tmp_path / "s", model_path(TWIN), model_points=table),
                      name=_name("decoded_s"))
    spec = dataclasses.replace(SPEC, derived=(), future=(), derived_refs={})
    twins, _ = build_sec_table(spec, s)
    sec = mx.read_model(_sec_inputs(tmp_path / "sec", twins), name=_name("decoded"))
    return s, sec, list(table.index)


def test_every_decode_is_pa_uk_s_own_on_every_value(tmp_path):
    """``Data`` decodes every value a column can hold as ``PA_UK_S``'s cells read it.

    A point of each case of :data:`DECODED` goes into a copy of S's table, and its twin,
    generated from it, into a copy of SEC's.  On each pair every cell of
    :data:`DECODING_CELLS` agrees exactly, in value and in type, the labels among them, and
    so do each life's age, the rating and the sex, the label returning each life's column,
    and the annual rate at ``t = 0`` and 240; each decode of :data:`DECODES` is S's
    comparison of the text, as a bool; and on the table basis each life's row of the
    mortality table, ``mort_schedule(life)``, holds S's rate for its sex at every age of
    the table, so that ``mort_rate`` is S's at every month the frame reads.  T1 and the
    splice see these through the cells that use them, at the values their points carry;
    this sees every value, on its own.
    """
    s, sec, labels = _decoded_tables(tmp_path)
    found = []
    try:
        rates = s.Data.mort_table()["mort_rate"]
        array = sec.Data.mort_table_array()
        for (base, changes), key, label in zip(DECODED, point_keys(sec), labels):
            case = f"S point {base} with {changes}"
            sp, p = projection(s, label), projection(sec, key)
            lives = (1, 2) if sp.is_joint() else (1,)
            calls = [(cell, ()) for cell in DECODING_CELLS]
            calls += [(cell, (life,)) for cell in ("age_at_entry", "sex") for life in lives]
            if sp.mort_basis() == "table":
                calls += [(cell, (life,)) for cell in ("rating_factor",) for life in lives]
                calls += [("mort_rate", (t, life)) for t in (0, 240) for life in lives]
            for cell, args in calls:
                want, got = sp.cells[cell](*args), p.cells[cell](*args)
                if got != want or type(got) is not type(want):
                    found.append(f"{case}: {cell}{args} is {got!r}, S {want!r}")
            for cell, read in DECODES.items():
                if cell == "is_first_death" and not sp.vp_pct() > 0.0:
                    continue
                want, got = read(sp), p.cells[cell]()
                if got != want or type(got) is not type(want):
                    found.append(f"{case}: {cell}() is {got!r}, S's text gives {want!r}")
            if sp.mort_basis() != "table":
                continue
            for life in lives:
                row = p.mort_schedule(life)
                first, last = sec.Data.mort_age_first()[row], sec.Data.mort_age_last()[row]
                if row != ("F", "M").index(sp.sex(life)) + 1:
                    found.append(f"{case}: life {life}'s schedule is {row}, not its sex's")
                for a in range(first, last + 1):
                    want = rates.loc[(sp.sex(life), a)]
                    if array[row, a] != want:
                        found.append(f"{case}: row {row} at age {a} is {array[row, a]!r}, "
                                     f"S's rate {want!r}")
    finally:
        sec.close()
        s.close()
    assert not found, found[:20]


def test_every_padded_array_holds_nan_and_each_sex_its_own_extents(sec_model, tmp_path):
    """The padding is NaN, each sex's extents are its own, and the reader reads none past
    them.

    ``Data`` tables the mortality rates by schedule, F 1 and M 2, from age 0, and pads
    what no file holds with NaN, as its docstring says, so that a read past a check, were
    one lost, would make every number after it NaN rather than another key's value: row
    0, a sex the table lacks, and each sex's ages below the table's first, 50 as shipped.
    Inside, nothing is NaN, and each row is its sex's rates, by age.  Each schedule's first
    and last ages are its own sex's, 50 and 115 as shipped, and row 0's are 1 and 0, so
    that no age lies between them.  The table's check holds every sex to the table's span
    (UNREADABLE's "a sex shorter"), so that the two sexes' extents are equal on any table
    the check reads; so the extents' own reading is held on a table the check would
    refuse, set past it, the women's ages from 55 and the men's from 50, as SPIA_US_SEC's
    are on tables whose sexes start apart (USLIB-SEC-PLAN.md §7.9, *Record -- M23*): each
    schedule's extents are its own sex's, and on the extract labelled otherwise than by
    position (:func:`_extract`), where a label read as ``idx + 1`` would name another
    point, the reader refuses a woman's attained age below her schedule's first, naming
    the point and the age, and reads a man's at 50, where a reader that took one
    schedule's extents for another's, or the table's for each, would part.
    """
    data = sec_model.Data
    mort = data.mort_table_array()
    first, last = data.mort_age_first(), data.mort_age_last()
    assert data.mort_sexes() == 2 and mort.shape == (3, 116)
    assert first.tolist() == [1, 50, 50] and last.tolist() == [0, 115, 115]
    assert np.isnan(mort[0]).all() and np.isnan(mort[1:, :50]).all()
    assert not np.isnan(mort[1:, 50:]).any()
    rows = pd.read_csv(model_path(TWIN).parent / MORT)
    for row, sex in ((1, "F"), (2, "M")):
        part = rows[rows["sex"] == sex].set_index("age")["mort_rate"]
        assert mort[row, part.index.to_numpy()].tolist() == part.tolist(), sex
    extract = _extract()
    anchor = extract.index[extract["policy_id"] == _committed().at[2, "policy_id"]][0]
    women = _then(_set("annuitant_sex", [anchor], "F"), _set("dependant_sex", [anchor], "M"))
    model = mx.read_model(_sec_inputs(tmp_path, women(extract)), name=_name("padded"))
    try:
        cut = model.Data.mort_table_rows()
        cut = cut[~((cut["sex"] == "F") & (cut["age"] < 55))].reset_index(drop=True)
        model.Data.mort_table_rows[()] = cut
        model.Data.mort_sexes[()] = 2
        p = _point(model, anchor)
        position = list(extract.index).index(anchor)
        assert p.point_id() == anchor != point_keys(model)[position] + 1
        assert model.Data.mort_age_first().tolist() == [1, 55, 50]
        assert model.Data.mort_age_last().tolist() == [0, 115, 115]
        assert np.isnan(model.Data.mort_table_array()[1, :55]).all()
        assert p.mort_schedule(1) == 1 and p.mort_schedule(2) == 2
        assert p.mort_rate_base_at(50, 2) == model.Data.mort_table_array()[2, 50]
        _refused(lambda: p.mort_rate_base_at(54, 1),
                 f"point_id {anchor}: mort_table.csv has no rate at attained age 54")
        assert p.mort_rate_base_at(55, 1) == model.Data.mort_table_array()[1, 55]
    finally:
        model.close()


# Data's readers, each a DataFrame or a path, which only the label accessors, the reports
# and Data's own cells read.  Every other Data cell is a vector or an int in the Data
# docstring's table of its vectors.
READERS = ("input_dir", "model_point_table", "model_point_rows", "mort_table",
           "mort_table_rows")


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
    vector is of R5's kind, int64 for ages, months, years, codes, flags and schedules,
    float64 for counts, amounts, rates, shares and probabilities, as the table states it:
    a month held as a float64 reads the same numbers, and compiled reads a double through
    ``int()``, Python arithmetic, which neither C3 nor C5 sees.  Every cell is in the table,
    and every cell the table names is a cell.
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
    or a ``bool``, and so does each cell of a life, at each life the point covers.
    """
    space = sec_model.Projection
    reporting = reporting_cells(SEC, space)
    names = sorted(name for name, cell in space.cells.items()
                   if not cell.parameters and name not in reporting)
    per_life = ("age_at_entry", "mort_schedule", "rating_factor", "death_mth",
                "lives_if_init")
    assert {"point_id", "is_joint", "payment_freq", "guarantee_mths", "start_year",
            "duration_mth_init", "rpi_peak_init", "proj_len"} <= set(names)
    found = []
    for key in point_keys(sec_model):
        proj = projection(sec_model, key)
        found += [f"{key}: {name} {type(value).__name__}" for name in names
                  if type(value := proj.cells[name]()) not in (int, float, bool)]
        for life in ((1, 2) if proj.is_joint() else (1,)):
            for name in per_life:
                if name in ("mort_schedule", "rating_factor") and proj.is_scenario():
                    continue
                value = proj.cells[name](life)
                if type(value) not in (int, float, bool):
                    found.append(f"{key}: {name}({life}) {type(value).__name__}")
    assert not found, found


# Each validating label and the refusal its own formula makes of a value that is not one
# of its column's, which no check of Data's refuses first: the four text columns PA_UK_S
# validates as it reads them.
LABEL_REFUSALS = {"payment_timing": ("timing", "invalid timing"),
                  "escalation_type": ("escalation_type", "invalid escalation_type"),
                  "vp_basis": ("vp_basis", "invalid vp_basis"),
                  "mort_basis": ("mort_basis", "invalid mort_basis")}


def test_each_label_refuses_or_returns_its_column_as_read():
    """The four validating labels return text or raise; ``sex`` returns its column as read.

    Each is a reporting cell, which a reader asks for and no projection cell reads, and the
    registry names them (``"reporting"``).  ``payment_timing()``, ``escalation_type()``,
    ``vp_basis()`` and ``mort_basis()`` refuse a value that is not one of their column's
    themselves, as ``PA_UK_S``'s do, so that compiled each may return ``str`` and still
    raises where modelx raises (``uk_sec_support.labels_refusing_non_text``, C3).  So each
    is called in modelx on the committed model whose table is replaced, past ``Data``'s
    checks, by one holding the first point's column blank, as the number 7 and as a text no
    value is, and must refuse each, with its message; and the harness's own reading finds
    all four refusing.  ``sex(life)`` validates nothing, and returns the column as read, a
    blank as NaN and a number as the number, which a scenario point's sexes, never read by
    its projection, may now hold (``Data``, *refused by point*), each life's, the second
    life's of a single-life contract among them, where ``PA_UK_S`` refuses it.
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
    model = mx.read_model(model_path(SEC), name=_name("sex"))
    try:
        table = model.Data.model_point_table().astype({"annuitant_sex": object})
        table.iloc[0, table.columns.get_loc("annuitant_sex")] = 7
        model.Data.model_point_table[()] = table
        keys = point_keys(model)
        assert projection(model, keys[0]).sex(1) == 7
        single = list(table.index).index(_label(table, "twin", 5, 0))
        assert math.isnan(projection(model, keys[single]).sex(2))
        _refused(lambda: projection(model, keys[0]).sex(3), "invalid life")
    finally:
        model.close()


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


def test_the_spec_sizes_each_cache_as_its_comment_derives():
    """``spec_sec.py`` gives each cache the size its comment derives from the contract.

    The spec check, C3, holds the compiled caches to the spec, and C4 at the contract's
    extremes holds the spec to the largest argument a projection reads; neither sees a
    size above the comment's.  So this reads the spec as mx2cy does, and the bounds of the
    contract from the model's own References, and holds each size to the comment's
    derivation from them: ``t`` to ``12 * (omega_age_max - issue_age_min) +
    future_horizon_mth + 2``, ``k`` to ``12 * (omega_age_max - issue_age_min) + 2``, ``y``
    to ``omega_age_max - issue_age_min + 2``, ``a`` to ``omega_age_max - issue_age_min +
    1`` and ``x`` to ``omega_age_max + 1``, ``omega_age_max`` itself being the shipped
    mortality table's last age plus one, so that every limiting age the table admits on the
    table basis fits; every 2-D cache, and the per-life 1-D one, to one inner width, the
    kinds', since gcc refuses two widths and MSVC, which builds the Windows leg, accepts
    them (USLIB-SEC-PLAN.md §7.2, *Record -- M15*); and the codes dense from 0, ints, as
    the caches index them, the timings, and the kinds of the claims and of the payments to
    date in one numbering with the total last.  A change to a bound or a size is derived
    again in the comment and here.
    """
    source, comment = _comment("spec_sec.py")
    for formula in ("12 * (omega_age_max - issue_age_min) + future_horizon_mth + 2",
                    "12 * (omega_age_max - issue_age_min) + 2",
                    "omega_age_max - issue_age_min + 2", "omega_age_max - issue_age_min + 1",
                    "omega_age_max + 1"):
        assert formula in comment, formula
    sizes = ast.literal_eval(source)["spaces"]["Projection"]["cells_param_size"]
    proj, data = _references("Projection"), _references("Data")
    for names in (TIMINGS, (*KINDS, "ANNUITANT", "ALL")):
        values = [proj[name] for name in names]
        assert values == list(range(len(names))), (names, values)
        assert all(type(v) is int for v in values), (names, values)
    ages = pd.read_csv(model_path(TWIN).parent / MORT)["age"]
    assert proj["omega_age_max"] == ages.max() + 1 == OMEGA_MAX, proj["omega_age_max"]
    span = proj["omega_age_max"] - proj["issue_age_min"]
    t = 12 * span + data["future_horizon_mth"] + 2
    k = 12 * span + 2
    width = len(KINDS) + 2
    assert sizes == {"t": t, ("t", "life"): (t, width), ("t", "timing"): (t, width),
                     ("t", "kind"): (t, width), "k": k, ("k", "kind"): (k, width),
                     "y": span + 2, ("y", "life"): (span + 2, width), "a": span + 1,
                     ("x", "life"): (proj["omega_age_max"] + 1, width), "life": width}, sizes
    assert len({size[1] for size in sizes.values() if isinstance(size, tuple)}) == 1
    assert (t, k, span + 2, span + 1, proj["omega_age_max"] + 1, width) == (
        1514, 1394, 118, 117, 117, 4)


def test_the_sample_raises_the_recursion_limit_its_comment_derives():
    """``sample_sec.py`` sets the recursion limit its comment derives, before the import.

    The export does not raise the recursion limit as modelx does (F7), so the sample sets
    it, and its comment records the measured need: the deepest cold call at the longest
    cover needs the limit the comment states in the export, and the reports and checks the
    sample runs in ascending ``t`` less, from a script's top level (measured at M12).  The
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


def test_the_sample_traces_sex_on_a_blank(sec_model):
    """The sample types ``sex`` on a blank, so that it compiles as a Python object.

    ``sex(life)`` returns its column as read, and the compiled cell returns what mx2cy
    traced it returning: text alone, and it would compile to ``str`` and raise
    ``TypeError`` on a blank or a number, which ``Data`` holds where no projection reads
    the sex.  The sample calls ``sex(1)`` and ``sex(2)`` on every committed point, and the
    committed table holds single-life points, whose ``dependant_sex`` is blank, so the trace
    meets a NaN beside the text; were the table to lose them, the sample would trace text
    alone, which this would see.  The compiled label test holds the result.
    """
    source = (model_path(SEC).parent / "sample_sec.py").read_text(encoding="utf-8")
    assert "p.sex(1), p.sex(2)" in source
    table = sec_model.Data.model_point_table()
    singles = table.index[~table["dependant_present"].astype(bool)].tolist()
    assert singles and table.loc[singles, "dependant_sex"].isna().all(), singles


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
    import importlib.machinery
    import pathlib
    import types
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
# the point, the call, its arguments, the message): a point_id that is not a whole number
# below 2**53, which Data.point_id refuses when a refusal first names a point, here the
# table basis's twin at its stop; a start year and a month of death of 2**53, which no
# int64 can be trusted to hold, on a point whose projection never reads them, refused by
# their accessors when called; a timing, a kind and a life no cell takes, inside the one
# inner width the caches share, each refused by the cell as PA_UK_S's are, a kind of the
# other cell among them, ValueError and its message.
NOT_HELD = [
    ("a label with a fraction",
     lambda t: _set("duration_mth", [2], 636)(t).rename(index={2: 2.5}), 2,
     "result_cf", (), "model_point_table_sec.csv: point_id must be a whole number; [2.5] "
     "is not"),
    ("a label of 2**53", lambda t: _set("duration_mth", [2], 636)(t).rename(
        index={2: 2 ** 53}), 2, "result_cf", (),
     f"model_point_table_sec.csv: point_id must be below 2**53 in size; [{2 ** 53}] is "
     f"not"),
    ("a start year of 2**53 on the scenario basis", _set("start_year", [1], 2.0 ** 53), 1,
     "start_year", (), "point_id 1: start_year must be a number, below 2**53 in size, and "
     "a whole one on the table basis, which reads it; it is not"),
    ("a month of death of 2**53 on the table basis", _set("death_mth_1", [2], 2.0 ** 53), 2,
     "death_mth", (1,), "point_id 2: death_mth_1 must be blank or below 2**53 months in "
     "size; it is not"),
    ("a timing no cell takes", None, 1, "pols_if_at", (0, 2), "invalid timing"),
    ("the last timing inside the caches", None, 1, "pols_if_at", (0, 3), "invalid timing"),
    ("the payments' kind in the claims", None, 1, "claims", (0, 2), "invalid kind"),
    ("a claims kind in the payments", None, 1, "cum_annuity_pp", (5, 0), "invalid kind"),
    ("the other claims kind in the payments", None, 1, "cum_annuity_pp", (5, 1),
     "invalid kind"),
    ("a life 0", None, 1, "lives_if_init", (0,), "invalid life"),
    ("a life 3", None, 1, "age_at_entry", (3,), "invalid life"),
    ("a life 0's month of death", None, 1, "death_mth", (0,), "invalid life"),
    ("a life 3's month of death", None, 1, "death_mth", (3,), "invalid life"),
    ("a second life on a single life", None, 5, "mort_schedule", (2,), "invalid life"),
]


@pytest.mark.parametrize("case, edit, point, cell, args, message", NOT_HELD,
                         ids=[c[0] for c in NOT_HELD])
def test_what_the_c_step_cannot_hold_or_take_is_refused(tmp_path, case, edit, point, cell,
                                                        args, message):
    """A label or a number the vectors cannot hold, and a code no cell takes, are refused.

    ``Data.point_id`` reads each label by value, and refuses one that is not a whole
    number, or is ``2**53`` or more in size, naming every such label, when a refusal first
    names a point: here the table basis's twin moved to its stop, a refusal of
    ``proj_len()``'s, which
    meets the label's own first.  A projection that names no point reads no label, and
    runs.  A start year or a month of death no int64 can be trusted to hold is refused by
    its accessor, naming the point, on a point whose projection never reads it, so that the
    point projects (:data:`NOT_HELD`).  And a timing, a kind or a life no cell takes is
    refused by the cell, as ``PA_UK_S``'s are, a kind of the claims by the payments' cell
    and theirs by the claims': compiled, a code past a cache raises ``IndexError``
    instead, which the compiled refusal test holds.
    """
    model = _read_edited(tmp_path, edit or (lambda t: t))
    try:
        keys = point_keys(model)
        p = projection(model, keys[point - 1])
        _refused(lambda: p.cells[cell](*args), message)
        if edit is not None:
            assert len(projection(model, keys[0]).result_cf()) == 636
        if cell in ("start_year", "death_mth"):
            assert len(p.result_cf()) == 636
    finally:
        model.close()


# ---------------------------------------------------------------------------
# C2 -- the Phase 1 fingerprint


def test_the_phase_1_fingerprint_is_reproduced(sec_model):
    """Every committed point computes what the model computed when its E step ended (C2).

    The C step changes how the model is represented and no number it computes
    (UKLIB-SEC-PLAN.md U2, after USLIB-SEC-PLAN.md D2), so before it changed anything the
    model as M11 committed it was frozen below (USLIB-SEC-PLAN.md §5.4): for each point,
    each column of ``result_cf()`` and ``result_pols()``, its sum, its largest absolute value
    and its values at five fixed months, the frame's first and last and the three quartiles
    between.  Every later version must reproduce it, to 1e-12 relative, floored at 1e-12 of
    the column's own magnitude (``uk_sec_support.fingerprint_mismatches``), with the same
    points, frames and columns exactly.  ``python tools/gen_sec_fingerprint.py PA_UK_SEC
    --check`` runs the same comparison from the command line.  Until the freeze, which is
    committed alone, the block is empty and the test skips.  The block was refrozen once,
    in a commit of its own, when M11's review added point 23, the LPI point held at its
    floor: it added that point's entry, and every other point's is what M11 first froze.
    """
    if not FINGERPRINT:
        pytest.skip("the Phase 1 fingerprint is frozen in a commit of its own")
    assert fingerprint_mismatches(FINGERPRINT, sec_model) == []


# PA_UK_SEC's fingerprint, frozen from the model as M11 committed it and committed alone,
# before its C step changed anything, and refrozen alone once since, when M11's review
# added point 23, which added its entry and changed no other.  Each point is keyed by its
# point_id; each column holds (its sum over the frame, its largest absolute value, (its
# values at the months)).  The block is written by tools/gen_sec_fingerprint.py, and is
# never edited by hand: a refreeze goes through the tool's --force, in a commit of its own
# that says why.
# BEGIN generated fingerprint: PA_UK_SEC -- tools/gen_sec_fingerprint.py
FINGERPRINT = {
    1: {"rows": 636, "months": (0, 158, 317, 476, 635),
        "result_cf": {
            "pols_if": (636.0, 1.0, (
                1.0, 1.0, 1.0, 1.0, 1.0)),
            "annuity_payments": (344532.3724893371, 3139.347979291292, (
                0.0, 991.2602565798063, 1455.699105592094, 2137.7432132032795,
                3139.347979291292)),
            "claims_vp": (43209.5, 43209.5, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_prop": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (3790.4124721037456, 11.627214738115894, (
                2.5, 3.6713342836289122, 5.3914781688596065, 7.917567456308441,
                11.627214738115894)),
            "liability_cf": (391532.28496144083, 43212.075, (
                2.5, 994.9315908634352, 1461.0905837609535, 2145.660780659588,
                3150.975194029408)),
            "net_cf": (-391532.28496144083, 43212.075, (
                -2.5, -994.9315908634352, -1461.0905837609535, -2145.660780659588,
                -3150.975194029408)),
        },
        "result_pols": {
            "pols_if": (636.0, 1.0, (
                1.0, 1.0, 1.0, 1.0, 1.0)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (16.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_2": (636.0, 1.0, (
                1.0, 1.0, 1.0, 1.0, 1.0)),
            "certain_floor": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor": (16.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "dependant_factor": (310.0, 0.5, (
                0.0, 0.5, 0.5, 0.5, 0.5)),
            "annuity_pp": (682274.2449786742, 6278.695958582584, (
                0.0, 1982.5205131596126, 2911.398211184188, 4275.486426406559,
                6278.695958582584)),
            "cum_annuity_all": (83223198.6694261, 344532.372489337, (
                0.0, 46554.54446722057, 110399.86229012994, 204840.90806671337,
                344532.372489337)),
            "vp_balance": (2613228.2674394264, 50000.0, (
                50000.0, 0.0, 0.0, 0.0, 0.0)),
        },
    },
    2: {"rows": 636, "months": (0, 158, 317, 476, 635),
        "result_cf": {
            "pols_if": (401.3639797203242, 0.9999996527930258, (
                0.9999996527930258, 0.9786592131323972, 0.7969351733402389,
                0.25123977404281717, 0.0007810393830953411)),
            "annuity_payments": (254846.7812328438, 1872.0932658719873, (
                0.0, 1760.74568844968, 1766.8491633953627, 613.1141716348682,
                2.4519544090672767)),
            "claims_vp": (2629.202964676305, 41.92133577406443, (
                41.92133577406443, 0.0, 0.0, 0.0, 0.0)),
            "claims_prop": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (1773.3206084225367, 4.355937739992102, (
                2.4999991319825647, 3.5929851211622643, 4.296658589060244,
                1.9892078586916953, 0.009081312626175096)),
            "liability_cf": (259249.30480594264, 1876.3001596047736, (
                44.421334906046994, 1764.3386735708423, 1771.1458219844228,
                615.1033794935598, 2.461035721693452)),
            "net_cf": (-259249.30480594264, 1876.3001596047736, (
                -44.421334906046994, -1764.3386735708423, -1771.1458219844228,
                -615.1033794935598, -2.461035721693452)),
        },
        "result_pols": {
            "pols_if": (401.3639797203242, 0.9999996527930258, (
                0.9999996527930258, 0.9786592131323972, 0.7969351733402389,
                0.25123977404281717, 0.0007810393830953411)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (276.4174277088396, 0.9991615732845187, (
                0.9991615732845187, 0.7976106178854093, 0.41681096183837085,
                0.03556463157901314, 0.0)),
            "lives_if_2": (359.27999007317993, 0.9995858827400101, (
                0.9995858827400101, 0.8945557981123737, 0.6518027374110514,
                0.22362840427235284, 0.0007810393830953411)),
            "certain_floor": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor": (276.4174277088396, 0.9991615732845187, (
                0.9991615732845187, 0.7976106178854093, 0.41681096183837085,
                0.03556463157901314, 0.0)),
            "dependant_factor": (62.473276005742306, 0.1962284948587069, (
                0.0004190397542535856, 0.09052429762349393, 0.19006210575093402,
                0.107837571231902, 0.00039051969154767056)),
            "annuity_pp": (682274.2449786742, 6278.695958582584, (
                0.0, 1982.5205131596126, 2911.398211184188, 4275.486426406559,
                6278.695958582584)),
            "cum_annuity_all": (101435853.36923331, 254846.7812328438, (
                0.0, 81887.70612398398, 178200.2726710993, 245403.96321923507,
                254846.7812328438)),
            "vp_balance": (2613228.2674394264, 50000.0, (
                50000.0, 0.0, 0.0, 0.0, 0.0)),
        },
    },
    3: {"rows": 636, "months": (0, 158, 317, 476, 635),
        "result_cf": {
            "pols_if": (636.0, 1.0, (
                1.0, 1.0, 1.0, 1.0, 1.0)),
            "annuity_payments": (372089.5966303081, 3139.347979291292, (
                0.0, 991.2602565798063, 1455.699105592094, 2137.7432132032795,
                3139.347979291292)),
            "claims_vp": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_prop": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (3790.4124721037456, 11.627214738115894, (
                2.5, 3.6713342836289122, 5.3914781688596065, 7.917567456308441,
                11.627214738115894)),
            "liability_cf": (375880.00910241186, 3150.975194029408, (
                2.5, 994.9315908634352, 1461.0905837609535, 2145.660780659588,
                3150.975194029408)),
            "net_cf": (-375880.00910241186, 3150.975194029408, (
                -2.5, -994.9315908634352, -1461.0905837609535, -2145.660780659588,
                -3150.975194029408)),
        },
        "result_pols": {
            "pols_if": (636.0, 1.0, (
                1.0, 1.0, 1.0, 1.0, 1.0)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (16.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_2": (636.0, 1.0, (
                1.0, 1.0, 1.0, 1.0, 1.0)),
            "certain_floor": (120.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor": (120.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "dependant_factor": (258.0, 0.5, (
                0.0, 0.5, 0.5, 0.5, 0.5)),
            "annuity_pp": (682274.2449786742, 6278.695958582584, (
                0.0, 1982.5205131596126, 2911.398211184188, 4275.486426406559,
                6278.695958582584)),
            "cum_annuity_all": (98813808.09033085, 372089.5966303081, (
                0.0, 74111.76860819152, 137957.08643110088, 232398.13220768436,
                372089.5966303081)),
            "vp_balance": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
        },
    },
    4: {"rows": 636, "months": (0, 158, 317, 476, 635),
        "result_cf": {
            "pols_if": (636.0, 1.0, (
                1.0, 1.0, 1.0, 1.0, 1.0)),
            "annuity_payments": (399646.82077127905, 3139.347979291292, (
                0.0, 991.2602565798063, 1455.699105592094, 2137.7432132032795,
                3139.347979291292)),
            "claims_vp": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_prop": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (3790.4124721037456, 11.627214738115894, (
                2.5, 3.6713342836289122, 5.3914781688596065, 7.917567456308441,
                11.627214738115894)),
            "liability_cf": (403437.2332433828, 3150.975194029408, (
                2.5, 994.9315908634352, 1461.0905837609535, 2145.660780659588,
                3150.975194029408)),
            "net_cf": (-403437.2332433828, 3150.975194029408, (
                -2.5, -994.9315908634352, -1461.0905837609535, -2145.660780659588,
                -3150.975194029408)),
        },
        "result_pols": {
            "pols_if": (636.0, 1.0, (
                1.0, 1.0, 1.0, 1.0, 1.0)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (16.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_2": (636.0, 1.0, (
                1.0, 1.0, 1.0, 1.0, 1.0)),
            "certain_floor": (120.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor": (120.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "dependant_factor": (310.0, 0.5, (
                0.0, 0.5, 0.5, 0.5, 0.5)),
            "annuity_pp": (682274.2449786742, 6278.695958582584, (
                0.0, 1982.5205131596126, 2911.398211184188, 4275.486426406559,
                6278.695958582584)),
            "cum_annuity_all": (114404417.51123567, 399646.8207712792, (
                0.0, 101668.99274916259, 165514.3105720719, 259955.3563486554,
                399646.8207712792)),
            "vp_balance": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
        },
    },
    5: {"rows": 600, "months": (0, 149, 299, 449, 599),
        "result_cf": {
            "pols_if": (276.4174277088396, 0.9991615732845187, (
                0.9991615732845187, 0.8137041019416205, 0.4670748754713106,
                0.07405012124087278, 2.2262204334465577e-06)),
            "annuity_payments": (153897.316786483, 554.75, (
                554.75, 452.37852604622356, 260.5739909675787, 42.050408153281644,
                0.0014122545281038566)),
            "claims_vp": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_prop": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (1070.1563008632647, 2.9458657038134453, (
                2.4979039332112967, 2.9003687050366467, 2.3736676353345185,
                0.5526409935643593, 2.3688206692123985e-05)),
            "liability_cf": (154967.47308734627, 557.2479039332113, (
                557.2479039332113, 455.2788947512602, 262.94765860291324,
                42.603049146846004, 0.0014359427347959805)),
            "net_cf": (-154967.47308734627, 557.2479039332113, (
                -557.2479039332113, -455.2788947512602, -262.94765860291324,
                -42.603049146846004, -0.0014359427347959805)),
        },
        "result_pols": {
            "pols_if": (276.4174277088396, 0.9991615732845187, (
                0.9991615732845187, 0.8137041019416205, 0.4670748754713106,
                0.07405012124087278, 2.2262204334465577e-06)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (276.4174277088396, 0.9991615732845187, (
                0.9991615732845187, 0.8137041019416205, 0.4670748754713106,
                0.07405012124087278, 2.2262204334465577e-06)),
            "lives_if_2": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "certain_floor": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor": (277.4174254826192, 1.0, (
                1.0, 0.8154637693487581, 0.4697142694323186, 0.07580064561204443,
                2.54574948734359e-06)),
            "dependant_factor": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "annuity_pp": (332850.0, 554.75, (
                554.75, 554.75, 554.75, 554.75, 554.75)),
            "cum_annuity_all": (66668377.01000083, 153897.3167864827, (
                554.75, 76507.03035744594, 130951.6704879523, 152598.53369829335,
                153897.3167864827)),
            "vp_balance": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
        },
    },
    6: {"rows": 636, "months": (0, 158, 317, 476, 635),
        "result_cf": {
            "pols_if": (401.3639797203242, 0.9999996527930258, (
                0.9999996527930258, 0.9786592131323972, 0.7969351733402389,
                0.25123977404281717, 0.0007810393830953411)),
            "annuity_payments": (254846.78123284376, 1872.093265871987, (
                0.0, 1760.7456884496798, 1766.8491633953627, 613.1141716348681,
                2.451954409067276)),
            "claims_vp": (2629.202964676305, 41.92133577406443, (
                41.92133577406443, 0.0, 0.0, 0.0, 0.0)),
            "claims_prop": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (1773.3206084225367, 4.355937739992102, (
                2.4999991319825647, 3.5929851211622643, 4.296658589060244,
                1.9892078586916953, 0.009081312626175096)),
            "liability_cf": (259249.30480594258, 1876.3001596047732, (
                44.421334906046994, 1764.338673570842, 1771.1458219844228,
                615.1033794935597, 2.461035721693451)),
            "net_cf": (-259249.30480594258, 1876.3001596047732, (
                -44.421334906046994, -1764.338673570842, -1771.1458219844228,
                -615.1033794935597, -2.461035721693451)),
        },
        "result_pols": {
            "pols_if": (401.3639797203242, 0.9999996527930258, (
                0.9999996527930258, 0.9786592131323972, 0.7969351733402389,
                0.25123977404281717, 0.0007810393830953411)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (276.4174277088396, 0.9991615732845187, (
                0.9991615732845187, 0.7976106178854093, 0.41681096183837085,
                0.03556463157901314, 0.0)),
            "lives_if_2": (359.27999007317993, 0.9995858827400101, (
                0.9995858827400101, 0.8945557981123737, 0.6518027374110514,
                0.22362840427235284, 0.0007810393830953411)),
            "certain_floor": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor": (276.4174277088396, 0.9991615732845187, (
                0.9991615732845187, 0.7976106178854093, 0.41681096183837085,
                0.03556463157901314, 0.0)),
            "dependant_factor": (62.473276005742306, 0.1962284948587069, (
                0.0004190397542535856, 0.09052429762349393, 0.19006210575093402,
                0.107837571231902, 0.00039051969154767056)),
            "annuity_pp": (682274.2449786742, 6278.6959585825825, (
                0.0, 1982.5205131596124, 2911.398211184188, 4275.486426406558,
                6278.6959585825825)),
            "cum_annuity_all": (101435853.36923331, 254846.78123284376, (
                0.0, 81887.70612398398, 178200.27267109926, 245403.96321923504,
                254846.78123284376)),
            "vp_balance": (2613228.2674394264, 50000.0, (
                50000.0, 0.0, 0.0, 0.0, 0.0)),
        },
    },
    7: {"rows": 636, "months": (0, 158, 317, 476, 635),
        "result_cf": {
            "pols_if": (401.3639797203242, 0.9999996527930258, (
                0.9999996527930258, 0.9786592131323972, 0.7969351733402389,
                0.25123977404281717, 0.0007810393830953411)),
            "annuity_payments": (254846.7812328438, 1872.0932658719873, (
                0.0, 1760.74568844968, 1766.8491633953627, 613.1141716348682,
                2.4519544090672767)),
            "claims_vp": (2629.202964676305, 41.92133577406443, (
                41.92133577406443, 0.0, 0.0, 0.0, 0.0)),
            "claims_prop": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (1773.3206084225367, 4.355937739992102, (
                2.4999991319825647, 3.5929851211622643, 4.296658589060244,
                1.9892078586916953, 0.009081312626175096)),
            "liability_cf": (259249.30480594264, 1876.3001596047736, (
                44.421334906046994, 1764.3386735708423, 1771.1458219844228,
                615.1033794935598, 2.461035721693452)),
            "net_cf": (-259249.30480594264, 1876.3001596047736, (
                -44.421334906046994, -1764.3386735708423, -1771.1458219844228,
                -615.1033794935598, -2.461035721693452)),
        },
        "result_pols": {
            "pols_if": (401.3639797203242, 0.9999996527930258, (
                0.9999996527930258, 0.9786592131323972, 0.7969351733402389,
                0.25123977404281717, 0.0007810393830953411)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (276.4174277088396, 0.9991615732845187, (
                0.9991615732845187, 0.7976106178854093, 0.41681096183837085,
                0.03556463157901314, 0.0)),
            "lives_if_2": (359.27999007317993, 0.9995858827400101, (
                0.9995858827400101, 0.8945557981123737, 0.6518027374110514,
                0.22362840427235284, 0.0007810393830953411)),
            "certain_floor": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor": (276.4174277088396, 0.9991615732845187, (
                0.9991615732845187, 0.7976106178854093, 0.41681096183837085,
                0.03556463157901314, 0.0)),
            "dependant_factor": (62.473276005742306, 0.1962284948587069, (
                0.0004190397542535856, 0.09052429762349393, 0.19006210575093402,
                0.107837571231902, 0.00039051969154767056)),
            "annuity_pp": (682274.2449786742, 6278.695958582584, (
                0.0, 1982.5205131596126, 2911.398211184188, 4275.486426406559,
                6278.695958582584)),
            "cum_annuity_all": (101435853.36923331, 254846.7812328438, (
                0.0, 81887.70612398398, 178200.2726710993, 245403.96321923507,
                254846.7812328438)),
            "vp_balance": (2613228.2674394264, 50000.0, (
                50000.0, 0.0, 0.0, 0.0, 0.0)),
        },
    },
    8: {"rows": 600, "months": (0, 149, 299, 449, 599),
        "result_cf": {
            "pols_if": (243.54429129936705, 0.9988662863073619, (
                0.9988662863073619, 0.7563952296327764, 0.35519933492572275,
                0.027179186481920845, 0.0)),
            "annuity_payments": (160333.32510541665, 657.5869718190132, (
                657.5869718190132, 497.9601928415778, 233.83956215943417,
                17.892964433931223, 0.0)),
            "claims_vp": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_prop": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (900.9163959547881, 2.746223095907662, (
                2.4971657157684044, 2.6960968335186166, 1.805117786639161,
                0.20284008141973303, 0.0)),
            "liability_cf": (161234.24150137146, 660.0841375347817, (
                660.0841375347817, 500.6562896750964, 235.64467994607332,
                18.095804515350956, 0.0)),
            "net_cf": (-161234.24150137146, 660.0841375347817, (
                -660.0841375347817, -500.6562896750964, -235.64467994607332,
                -18.095804515350956, -0.0)),
        },
        "result_pols": {
            "pols_if": (243.54429129936705, 0.9988662863073619, (
                0.9988662863073619, 0.7563952296327764, 0.35519933492572275,
                0.027179186481920845, 0.0)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (243.54429129936705, 0.9988662863073619, (
                0.9988662863073619, 0.7563952296327764, 0.35519933492572275,
                0.027179186481920845, 0.0)),
            "lives_if_2": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "certain_floor": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor": (243.54429129936705, 0.9988662863073619, (
                0.9988662863073619, 0.7563952296327764, 0.35519933492572275,
                0.027179186481920845, 0.0)),
            "dependant_factor": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "annuity_pp": (395000.0, 658.3333333333334, (
                658.3333333333334, 658.3333333333334, 658.3333333333334, 658.3333333333334,
                658.3333333333334)),
            "cum_annuity_all": (72087556.50971282, 160333.32510541662, (
                657.5869718190132, 88047.26898219695, 143641.6424749281, 159927.70691758662,
                160333.32510541662)),
            "vp_balance": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
        },
    },
    9: {"rows": 636, "months": (0, 158, 317, 476, 635),
        "result_cf": {
            "pols_if": (636.0, 1.0, (
                1.0, 1.0, 1.0, 1.0, 1.0)),
            "annuity_payments": (344532.3724893371, 3139.347979291292, (
                0.0, 991.2602565798063, 1455.699105592094, 2137.7432132032795,
                3139.347979291292)),
            "claims_vp": (43209.5, 43209.5, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_prop": (695.25, 695.25, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (3790.4124721037456, 11.627214738115894, (
                2.5, 3.6713342836289122, 5.3914781688596065, 7.917567456308441,
                11.627214738115894)),
            "liability_cf": (392227.53496144083, 43907.325, (
                2.5, 994.9315908634352, 1461.0905837609535, 2145.660780659588,
                3150.975194029408)),
            "net_cf": (-392227.53496144083, 43907.325, (
                -2.5, -994.9315908634352, -1461.0905837609535, -2145.660780659588,
                -3150.975194029408)),
        },
        "result_pols": {
            "pols_if": (636.0, 1.0, (
                1.0, 1.0, 1.0, 1.0, 1.0)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (16.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_2": (636.0, 1.0, (
                1.0, 1.0, 1.0, 1.0, 1.0)),
            "certain_floor": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor": (16.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "dependant_factor": (310.0, 0.5, (
                0.0, 0.5, 0.5, 0.5, 0.5)),
            "annuity_pp": (682274.2449786742, 6278.695958582584, (
                0.0, 1982.5205131596126, 2911.398211184188, 4275.486426406559,
                6278.695958582584)),
            "cum_annuity_all": (83223198.6694261, 344532.372489337, (
                0.0, 46554.54446722057, 110399.86229012994, 204840.90806671337,
                344532.372489337)),
            "vp_balance": (2613228.2674394264, 50000.0, (
                50000.0, 0.0, 0.0, 0.0, 0.0)),
        },
    },
    10: {"rows": 636, "months": (0, 158, 317, 476, 635),
        "result_cf": {
            "pols_if": (636.0, 1.0, (
                1.0, 1.0, 1.0, 1.0, 1.0)),
            "annuity_payments": (344532.3724893371, 3139.347979291292, (
                0.0, 991.2602565798063, 1455.699105592094, 2137.7432132032795,
                3139.347979291292)),
            "claims_vp": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_prop": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (3790.4124721037456, 11.627214738115894, (
                2.5, 3.6713342836289122, 5.3914781688596065, 7.917567456308441,
                11.627214738115894)),
            "liability_cf": (348322.7849614409, 3150.975194029408, (
                2.5, 994.9315908634352, 1461.0905837609535, 2145.660780659588,
                3150.975194029408)),
            "net_cf": (-348322.7849614409, 3150.975194029408, (
                -2.5, -994.9315908634352, -1461.0905837609535, -2145.660780659588,
                -3150.975194029408)),
        },
        "result_pols": {
            "pols_if": (636.0, 1.0, (
                1.0, 1.0, 1.0, 1.0, 1.0)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (16.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_2": (636.0, 1.0, (
                1.0, 1.0, 1.0, 1.0, 1.0)),
            "certain_floor": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor": (16.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "dependant_factor": (310.0, 0.5, (
                0.0, 0.5, 0.5, 0.5, 0.5)),
            "annuity_pp": (682274.2449786742, 6278.695958582584, (
                0.0, 1982.5205131596126, 2911.398211184188, 4275.486426406559,
                6278.695958582584)),
            "cum_annuity_all": (83223198.6694261, 344532.372489337, (
                0.0, 46554.54446722057, 110399.86229012994, 204840.90806671337,
                344532.372489337)),
            "vp_balance": (4270862.840938796, 50000.0, (
                50000.0, 3445.4555327794296, 0.0, 0.0, 0.0)),
        },
    },
    11: {"rows": 619, "months": (0, 154, 309, 463, 618),
        "result_cf": {
            "pols_if": (619.0, 1.0, (
                1.0, 1.0, 1.0, 1.0, 1.0)),
            "annuity_payments": (337741.87248933717, 3139.347979291292, (
                695.25, 0.0, 1499.3700787598568, 0.0, 3139.347979291292)),
            "claims_vp": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_prop": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (3594.443105255501, 11.288557998170772, (
                2.5, 3.564402217115448, 5.23444482413554, 7.686958695445089,
                11.288557998170772)),
            "liability_cf": (341336.3155945926, 3150.636537289463, (
                697.75, 3.564402217115448, 1504.6045235839924, 7.686958695445089,
                3150.636537289463)),
            "net_cf": (-341336.3155945926, 3150.636537289463, (
                -697.75, -3.564402217115448, -1504.6045235839924, -7.686958695445089,
                -3150.636537289463)),
        },
        "result_pols": {
            "pols_if": (619.0, 1.0, (
                1.0, 1.0, 1.0, 1.0, 1.0)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_2": (619.0, 1.0, (
                1.0, 1.0, 1.0, 1.0, 1.0)),
            "certain_floor": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "dependant_factor": (309.5, 0.5, (
                0.5, 0.5, 0.5, 0.5, 0.5)),
            "annuity_pp": (675483.7449786743, 6278.695958582584, (
                1390.5, 0.0, 2998.7401575197136, 0.0, 6278.695958582584)),
            "cum_annuity_all": (83162327.1694261, 344532.372489337, (
                7485.75, 50549.32330123719, 114810.63058007398, 206978.65127991664,
                344532.372489337)),
            "vp_balance": (1824099.7674394264, 41819.0, (
                41819.0, 0.0, 0.0, 0.0, 0.0)),
        },
    },
    12: {"rows": 620, "months": (0, 154, 309, 464, 619),
        "result_cf": {
            "pols_if": (620.0, 1.0, (
                1.0, 1.0, 1.0, 1.0, 1.0)),
            "annuity_payments": (337741.8724893371, 3139.347979291292, (
                0.0, 1020.9980642772006, 0.0, 0.0, 3139.347979291292)),
            "claims_vp": (43209.5, 43209.5, (
                43209.5, 0.0, 0.0, 0.0, 0.0)),
            "claims_prop": (695.25, 695.25, (
                695.25, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (3605.7316632536717, 11.288557998170772, (
                2.5, 3.564402217115448, 5.23444482413554, 7.686958695445089,
                11.288557998170772)),
            "liability_cf": (385252.3541525908, 43907.25, (
                43907.25, 1024.562466494316, 5.23444482413554, 7.686958695445089,
                3150.636537289463)),
            "net_cf": (-385252.3541525908, 43907.25, (
                -43907.25, -1024.562466494316, -5.23444482413554, -7.686958695445089,
                -3150.636537289463)),
        },
        "result_pols": {
            "pols_if": (620.0, 1.0, (
                1.0, 1.0, 1.0, 1.0, 1.0)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_2": (620.0, 1.0, (
                1.0, 1.0, 1.0, 1.0, 1.0)),
            "certain_floor": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "dependant_factor": (310.0, 0.5, (
                0.5, 0.5, 0.5, 0.5, 0.5)),
            "annuity_pp": (675483.7449786742, 6278.695958582584, (
                0.0, 2041.9961285544011, 0.0, 0.0, 6278.695958582584)),
            "cum_annuity_all": (83169117.66942608, 344532.372489337, (
                6790.5, 50549.32330123719, 113311.26050131413, 206978.65127991664,
                344532.372489337)),
            "vp_balance": (1867309.2674394264, 43209.5, (
                43209.5, 0.0, 0.0, 0.0, 0.0)),
        },
    },
    13: {"rows": 516, "months": (0, 128, 257, 386, 515),
        "result_cf": {
            "pols_if": (516.0, 1.0, (
                1.0, 1.0, 1.0, 1.0, 1.0)),
            "annuity_payments": (310184.64834836614, 3139.347979291292, (
                0.0, 1219.1250834018551, 1687.554233094613, 2335.96972813398,
                3139.347979291292)),
            "claims_vp": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_prop": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (2564.5167703377747, 8.651739733829555, (
                2.5, 3.3597909483603057, 4.650736429273743, 6.437706889212782,
                8.651739733829555)),
            "liability_cf": (312749.16511870397, 3147.9997190251215, (
                2.5, 1222.4848743502155, 1692.2049695238868, 2342.4074350231926,
                3147.9997190251215)),
            "net_cf": (-312749.16511870397, 3147.9997190251215, (
                -2.5, -1222.4848743502155, -1692.2049695238868, -2342.4074350231926,
                -3147.9997190251215)),
        },
        "result_pols": {
            "pols_if": (516.0, 1.0, (
                1.0, 1.0, 1.0, 1.0, 1.0)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_2": (516.0, 1.0, (
                1.0, 1.0, 1.0, 1.0, 1.0)),
            "certain_floor": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "dependant_factor": (258.0, 0.5, (
                0.5, 0.5, 0.5, 0.5, 0.5)),
            "annuity_pp": (620369.2966967323, 6278.695958582584, (
                0.0, 2438.2501668037103, 3375.108466189226, 4671.93945626796,
                6278.695958582584)),
            "cum_annuity_all": (95311351.5620034, 372089.5966303081, (
                61904.94828194194, 107159.86051142371, 169334.81368644178,
                254751.0742869686, 372089.5966303081)),
            "vp_balance": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
        },
    },
    14: {"rows": 612, "months": (0, 152, 305, 458, 611),
        "result_cf": {
            "pols_if": (377.36575233567964, 0.9997662830741708, (
                0.9997662830741708, 0.9705431692095241, 0.7692040918638099,
                0.22957704947886634, 0.0007810393830953411)),
            "annuity_payments": (243948.6743196447, 1872.0932658719873, (
                0.0, 1770.3609901502903, 1727.108445653783, 569.8530722170404,
                2.4519544090672767)),
            "claims_vp": (1692.8630618425448, 37.50554556494462, (
                37.50554556494462, 0.0, 0.0, 0.0, 0.0)),
            "claims_prop": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (1614.124946808446, 4.105889094157887, (
                2.499415707685427, 3.459406224136681, 4.026356377360398, 1.764749296766199,
                0.008560008130997358)),
            "liability_cf": (247255.6623282957, 1876.0586666946722, (
                40.00496127263005, 1773.820396374427, 1731.1348020311434, 571.6178215138067,
                2.460514417198274)),
            "net_cf": (-247255.6623282957, 1876.0586666946722, (
                -40.00496127263005, -1773.820396374427, -1731.1348020311434,
                -571.6178215138067, -2.460514417198274)),
        },
        "result_pols": {
            "pols_if": (377.36575233567964, 0.9997662830741708, (
                0.9997662830741708, 0.9705431692095241, 0.7692040918638099,
                0.22957704947886634, 0.0007810393830953411)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (252.67260331880402, 0.9783036659475713, (
                0.9783036659475713, 0.7634081986646054, 0.3826852716229489,
                0.029226443149435264, 0.0)),
            "lives_if_2": (335.4064433613744, 0.9892278149265049, (
                0.9892278149265049, 0.8754951328650746, 0.6261292700030612,
                0.20638243070754747, 0.0007810393830953411)),
            "certain_floor": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor": (252.67260331880402, 0.9783036659475713, (
                0.9783036659475713, 0.7634081986646054, 0.3826852716229489,
                0.029226443149435264, 0.0)),
            "dependant_factor": (62.34657450843784, 0.19622849485870686, (
                0.010731308563299761, 0.10356748527245932, 0.1932594101204305,
                0.10017530316471554, 0.00039051969154767056)),
            "annuity_pp": (671312.2449786743, 6278.695958582584, (
                0.0, 2041.9961285544011, 2998.7401575197136, 4403.751019198756,
                6278.695958582584)),
            "cum_annuity_all": (101311263.7402125, 254846.7812328438, (
                10898.106913199103, 92462.97587600358, 185146.91590377095,
                246558.03682302352, 254846.7812328438)),
            "vp_balance": (1538319.2674394264, 39038.0, (
                39038.0, 0.0, 0.0, 0.0, 0.0)),
        },
    },
    15: {"rows": 606, "months": (0, 151, 302, 453, 605),
        "result_cf": {
            "pols_if": (371.3674906026247, 0.9996256019369548, (
                0.9996256019369548, 0.9679269241207766, 0.7619565922528438,
                0.2259540101204383, 0.0007810393830953411)),
            "annuity_payments": (241120.57005426823, 1872.093265871987, (
                0.0, 0.0, 1703.5071936108125, 0.0, 2.4519544090672762)),
            "claims_vp": (1472.4928143306734, 34.549483381891164, (
                34.549483381891164, 0.0, 0.0, 0.0, 0.0)),
            "claims_prop": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (1575.77996310231, 4.046506948669839, (
                2.499064004842387, 3.4500808743418325, 3.988419740533853,
                1.6863098474427094, 0.008560008130997358)),
            "liability_cf": (244168.8428317012, 1875.9431695833314, (
                37.04854738673355, 3.4500808743418325, 1707.4956133513463,
                1.6863098474427094, 2.4605144171982736)),
            "net_cf": (-244168.8428317012, 1875.9431695833314, (
                -37.04854738673355, -3.4500808743418325, -1707.4956133513463,
                -1.6863098474427094, -2.4605144171982736)),
        },
        "result_pols": {
            "pols_if": (371.3674906026247, 0.9996256019369548, (
                0.9996256019369548, 0.9679269241207766, 0.7619565922528438,
                0.2259540101204383, 0.0007810393830953411)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (246.81715953352483, 0.9725589604139413, (
                0.9725589604139413, 0.7534912390671861, 0.37419199290486443,
                0.028221456045297834, 0.0)),
            "lives_if_2": (329.4782593854673, 0.9863562726233098, (
                0.9863562726233098, 0.8698907261638265, 0.6196223042078005,
                0.20347491237093773, 0.0007810393830953411)),
            "certain_floor": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor": (246.81715953352483, 0.9725589604139413, (
                0.9725589604139413, 0.7534912390671861, 0.37419199290486443,
                0.028221456045297834, 0.0)),
            "dependant_factor": (62.27516553454993, 0.1962284948587069, (
                0.013533320761506777, 0.1072178425267953, 0.1938822996739897,
                0.09886627703757024, 0.00039051969154767056)),
            "annuity_pp": (668447.8149786742, 6278.695958582583, (
                0.0, 0.0, 2998.7401575197127, 0.0, 6278.695958582583)),
            "cum_annuity_all": (101238801.67720452, 254846.78123284376, (
                13726.211178575504, 94225.89913204522, 186850.42309738172,
                246558.0368230235, 254846.78123284376)),
            "vp_balance": (1311252.3424394268, 36173.57, (
                36173.57, 0.0, 0.0, 0.0, 0.0)),
        },
    },
    16: {"rows": 535, "months": (0, 133, 267, 400, 534),
        "result_cf": {
            "pols_if": (300.5429140613909, 0.9937851467769392, (
                0.9937851467769392, 0.9273331206979856, 0.6604859223003041,
                0.1667120045563878, 0.0007810393830953411)),
            "annuity_payments": (206463.88648203548, 1872.0932658719873, (
                1610.2426629636404, 0.0, 1525.004334156141, 0.0, 2.4519544090672767)),
            "claims_vp": (0.3801586523959143, 0.3801586523959143, (
                0.3801586523959143, 0.0, 0.0, 0.0, 0.0)),
            "claims_prop": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (1162.903807141328, 3.397131353412798, (
                2.484462866942348, 3.2091147877868806, 3.1638983180604257,
                1.1054403108545443, 0.007168872046794359)),
            "liability_cf": (207627.1704478292, 1875.3174996199864, (
                1613.1072844829787, 3.2091147877868806, 1528.1682324742014,
                1.1054403108545443, 2.459123281114071)),
            "net_cf": (-207627.1704478292, 1875.3174996199864, (
                -1613.1072844829787, -3.2091147877868806, -1528.1682324742014,
                -1.1054403108545443, -2.459123281114071)),
        },
        "result_pols": {
            "pols_if": (300.5429140613909, 0.9937851467769392, (
                0.9937851467769392, 0.9273331206979856, 0.6604859223003041,
                0.1667120045563878, 0.0007810393830953411)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (180.48852419054907, 0.8893858571190014, (
                0.8893858571190014, 0.6358644501754204, 0.27030162418369735,
                0.01423036345127105, 0.0)),
            "lives_if_2": (260.8288687522316, 0.9438150216492038, (
                0.9438150216492038, 0.8004400302661432, 0.5347199761546864,
                0.15468283405336883, 0.0007810393830953411)),
            "certain_floor": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor": (180.48852419054907, 0.8893858571190014, (
                0.8893858571190014, 0.6358644501754204, 0.27030162418369735,
                0.01423036345127105, 0.0)),
            "dependant_factor": (60.027194935420916, 0.1962284948587069, (
                0.0521996448289689, 0.1457343352612826, 0.19509214905830338,
                0.07624082055255837, 0.00039051969154767056)),
            "annuity_pp": (632545.4907190301, 6278.695958582584, (
                1710.139609873282, 0.0, 3276.8043361060445, 0.0, 6278.695958582584)),
            "cum_annuity_all": (99041927.52623053, 254846.7812328438, (
                49993.13741377194, 127058.02684473725, 206289.4610033556, 249428.0855570811,
                254846.7812328438)),
            "vp_balance": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
        },
    },
    17: {"rows": 466, "months": (0, 116, 232, 348, 465),
        "result_cf": {
            "pols_if": (466.0, 1.0, (
                1.0, 1.0, 1.0, 1.0, 1.0)),
            "annuity_payments": (295004.04725237715, 3139.347979291292, (
                1020.9980642772006, 0.0, 0.0, 2406.0488199779993, 3139.347979291292)),
            "claims_vp": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_prop": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (2151.6530651324842, 7.686958695445089, (
                2.5, 3.2619329595731124, 4.383765132692754, 5.891413765023453,
                7.686958695445089)),
            "liability_cf": (297155.70031750965, 3147.034937986737, (
                1023.4980642772006, 3.2619329595731124, 4.383765132692754,
                2411.940233743023, 3147.034937986737)),
            "net_cf": (-297155.70031750965, 3147.034937986737, (
                -1023.4980642772006, -3.2619329595731124, -4.383765132692754,
                -2411.940233743023, -3147.034937986737)),
        },
        "result_pols": {
            "pols_if": (466.0, 1.0, (
                1.0, 1.0, 1.0, 1.0, 1.0)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_2": (466.0, 1.0, (
                1.0, 1.0, 1.0, 1.0, 1.0)),
            "certain_floor": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "dependant_factor": (233.0, 0.5, (
                0.5, 0.5, 0.5, 0.5, 0.5)),
            "annuity_pp": (590008.0945047543, 6278.695958582584, (
                2041.9961285544011, 0.0, 0.0, 4812.097639955999, 6278.695958582584)),
            "cum_annuity_all": (78994061.51036489, 344532.372489337, (
                50549.32330123719, 95014.54868642578, 155686.07402378996,
                236607.80815037756, 344532.372489337)),
            "vp_balance": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
        },
    },
    18: {"rows": 25, "months": (0, 6, 12, 18, 24),
        "result_cf": {
            "pols_if": (4.479177739724404e-10, 4.479177739724404e-10, (
                4.479177739724404e-10, 0.0, 0.0, 0.0, 0.0)),
            "annuity_payments": (2.948792011985233e-07, 2.948792011985233e-07, (
                2.948792011985233e-07, 0.0, 0.0, 0.0, 0.0)),
            "claims_vp": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_prop": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (1.1197944349311012e-09, 1.1197944349311012e-09, (
                1.1197944349311012e-09, 0.0, 0.0, 0.0, 0.0)),
            "liability_cf": (2.959989956334544e-07, 2.959989956334544e-07, (
                2.959989956334544e-07, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (-2.959989956334544e-07, 2.959989956334544e-07, (
                -2.959989956334544e-07, -0.0, -0.0, -0.0, -0.0)),
        },
        "result_pols": {
            "pols_if": (4.479177739724404e-10, 4.479177739724404e-10, (
                4.479177739724404e-10, 0.0, 0.0, 0.0, 0.0)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (4.479177739724404e-10, 4.479177739724404e-10, (
                4.479177739724404e-10, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_2": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "certain_floor": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor": (4.479177739724404e-10, 4.479177739724404e-10, (
                4.479177739724404e-10, 0.0, 0.0, 0.0, 0.0)),
            "dependant_factor": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "annuity_pp": (16458.333333333332, 658.3333333333334, (
                658.3333333333334, 658.3333333333334, 658.3333333333334, 658.3333333333334,
                658.3333333333334)),
            "cum_annuity_all": (4008333.1276354156, 160333.32510541662, (
                160333.32510541662, 160333.32510541662, 160333.32510541662,
                160333.32510541662, 160333.32510541662)),
            "vp_balance": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
        },
    },
    19: {"rows": 1, "months": (0,),
        "result_cf": {
            "pols_if": (0.0007810393830953411, 0.0007810393830953411, (
                0.0007810393830953411,)),
            "annuity_payments": (2.4519544090672767, 2.4519544090672767, (
                2.4519544090672767,)),
            "claims_vp": (0.0, 0.0, (
                0.0,)),
            "claims_prop": (0.0, 0.0, (
                0.0,)),
            "expenses": (0.0019525984577383527, 0.0019525984577383527, (
                0.0019525984577383527,)),
            "liability_cf": (2.453907007525015, 2.453907007525015, (
                2.453907007525015,)),
            "net_cf": (-2.453907007525015, 2.453907007525015, (
                -2.453907007525015,)),
        },
        "result_pols": {
            "pols_if": (0.0007810393830953411, 0.0007810393830953411, (
                0.0007810393830953411,)),
            "pols_new_biz": (0.0, 0.0, (
                0.0,)),
            "lives_if_1": (0.0, 0.0, (
                0.0,)),
            "lives_if_2": (0.0007810393830953411, 0.0007810393830953411, (
                0.0007810393830953411,)),
            "certain_floor": (0.0, 0.0, (
                0.0,)),
            "payment_factor": (0.0, 0.0, (
                0.0,)),
            "dependant_factor": (0.00039051969154767056, 0.00039051969154767056, (
                0.00039051969154767056,)),
            "annuity_pp": (6278.695958582584, 6278.695958582584, (
                6278.695958582584,)),
            "cum_annuity_all": (254846.7812328438, 254846.7812328438, (
                254846.7812328438,)),
            "vp_balance": (0.0, 0.0, (
                0.0,)),
        },
    },
    20: {"rows": 649, "months": (0, 162, 324, 486, 648),
        "result_cf": {
            "pols_if": (401.3639797203242, 0.9999996527930258, (
                0.0, 0.9820012940344517, 0.8101240414937017, 0.26213425372567845,
                0.0007810393830953411)),
            "annuity_payments": (254846.78123284376, 1872.093265871987, (
                0.0, 1728.166399569887, 1758.3944645371303, 643.6721837590176,
                2.451954409067276)),
            "claims_vp": (2629.202964676305, 41.92133577406443, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_prop": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (1830.9922729768807, 4.498799066295056, (
                0.0, 3.6052550173566384, 4.498799066295056, 2.1377296055765953,
                0.009634364565109162)),
            "liability_cf": (259306.9764704969, 1876.4263664167568, (
                0.0, 1731.7716545872438, 1762.8932636034253, 645.8099133645942,
                2.461588773632385)),
            "net_cf": (-259306.9764704969, 1876.4263664167568, (
                -0.0, -1731.7716545872438, -1762.8932636034253, -645.8099133645942,
                -2.461588773632385)),
        },
        "result_pols": {
            "pols_if": (401.3639797203242, 0.9999996527930258, (
                0.0, 0.9820012940344517, 0.8101240414937017, 0.26213425372567845,
                0.0007810393830953411)),
            "pols_new_biz": (1.0, 1.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (276.4174277088396, 0.9991615732845187, (
                0.0, 0.8137041019416205, 0.43405223883490035, 0.03896467143218165, 0.0)),
            "lives_if_2": (359.27999007317993, 0.9995858827400101, (
                0.0, 0.903386461252582, 0.664499143674663, 0.23221787551356202,
                0.0007810393830953411)),
            "certain_floor": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor": (276.4174277088396, 0.9991615732845187, (
                0.0, 0.8137041019416205, 0.43405223883490035, 0.03896467143218165, 0.0)),
            "dependant_factor": (62.473276005742306, 0.1962284948587069, (
                0.0, 0.08414859604641563, 0.18803590132940068, 0.11158479114674841,
                0.00039051969154767056)),
            "annuity_pp": (682274.2449786741, 6278.6959585825825, (
                0.0, 1924.777197242342, 2826.6002050331917, 4275.486426406558,
                6278.6959585825825)),
            "cum_annuity_all": (101435853.36923328, 254846.78123284376, (
                0.0, 76688.8507383215, 174644.54234790738, 244790.84904760018,
                254846.78123284376)),
            "vp_balance": (2613228.2674394264, 50000.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
        },
    },
    21: {"rows": 576, "months": (0, 143, 287, 431, 575),
        "result_cf": {
            "pols_if": (341.39530530657316, 0.9982726644687168, (
                0.9982726644687168, 0.9541902609342185, 0.7231486040089359,
                0.19909813250408087, 0.0007810393830953411)),
            "annuity_payments": (186078.45896652207, 1534.2032027192527, (
                0.0, 1475.0203851954998, 1334.3994284938626, 397.7560109603246,
                2.0094064627492965)),
            "claims_vp": (768.6874189257287, 26.926226118640038, (
                26.926226118640038, 0.0, 0.0, 0.0, 0.0)),
            "claims_prop": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (1392.365114968722, 3.7574701587476893, (
                2.495681661171792, 3.302056195751356, 3.567990826030178, 1.4005868994718011,
                0.007833620045077459)),
            "liability_cf": (188239.51150041656, 1537.8321062081247, (
                29.42190777981183, 1478.3224413912512, 1337.9674193198928,
                399.1565978597964, 2.0172400827943737)),
            "net_cf": (-188239.51150041656, 1537.8321062081247, (
                -29.42190777981183, -1478.3224413912512, -1337.9674193198928,
                -399.1565978597964, -2.0172400827943737)),
        },
        "result_pols": {
            "pols_if": (341.39530530657316, 0.9982726644687168, (
                0.9982726644687168, 0.9541902609342185, 0.7231486040089359,
                0.19909813250408087, 0.0007810393830953411)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (218.0810337613445, 0.9412898611586333, (
                0.9412898611586333, 0.7074738898102813, 0.3312003675891318,
                0.021330794451386068, 0.0)),
            "lives_if_2": (300.1092851975895, 0.9705785820750582, (
                0.9705785820750582, 0.8433994865071313, 0.5860473263224161,
                0.1816419041743972, 0.0007810393830953411)),
            "certain_floor": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor": (218.0810337613445, 0.9412898611586333, (
                0.9412898611586333, 0.7074738898102813, 0.3312003675891318,
                0.021330794451386068, 0.0)),
            "dependant_factor": (61.65713577261436, 0.1962284948587069, (
                0.02849140165504173, 0.12335818556196865, 0.19597411820990202,
                0.0888836690263474, 0.00039051969154767056)),
            "annuity_pp": (536022.8454659935, 5145.467709415132, (
                0.0, 1775.3532018303756, 2531.229155506881, 3608.9275255663965,
                5145.467709415132)),
            "cum_annuity_all": (84662600.19064893, 212683.78021733015, (
                26605.321250808007, 92882.42206195297, 163798.7670174127, 207150.6914719923,
                212683.78021733015)),
            "vp_balance": (596824.0824723833, 23000.0, (
                23000.0, 0.0, 0.0, 0.0, 0.0)),
        },
    },
    22: {"rows": 594, "months": (0, 148, 296, 444, 593),
        "result_cf": {
            "pols_if": (359.3739923615178, 0.9992270508833735, (
                0.9992270508833735, 0.9627649585470677, 0.7467965602388613,
                0.215450278842151, 0.0007810393830953411)),
            "annuity_payments": (249386.79353412974, 1983.2785013137402, (
                0.0, 0.0, 1805.7084765417555, 0.0, 2.5975780984605548)),
            "claims_vp": (975.5242306303214, 30.4667179195464, (
                30.4667179195464, 0.0, 0.0, 0.0, 0.0)),
            "claims_prop": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (1500.773026698585, 3.928647522980426, (
                2.498067627208434, 3.4316815528062303, 3.7952091159461485,
                1.607919800370623, 0.008310687505822676)),
            "liability_cf": (251863.0907914586, 1987.0162719072785, (
                32.96478554675483, 3.4316815528062303, 1809.5036856577017,
                1.607919800370623, 2.6058887859663775)),
            "net_cf": (-251863.0907914586, 1987.0162719072785, (
                -32.96478554675483, -3.4316815528062303, -1809.5036856577017,
                -1.607919800370623, -2.6058887859663775)),
        },
        "result_pols": {
            "pols_if": (359.3739923615178, 0.9992270508833735, (
                0.9992270508833735, 0.9627649585470677, 0.7467965602388613,
                0.215450278842151, 0.0007810393830953411)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (235.2108467504088, 0.9606302650695717, (
                0.9606302650695717, 0.7351330733479711, 0.35688897070126213,
                0.02540912864397729, 0.0)),
            "lives_if_2": (317.6742815340567, 0.9803669209865787, (
                0.9803669209865787, 0.8594198153631686, 0.6062834748189014,
                0.19499582417979655, 0.0007810393830953411)),
            "certain_floor": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor": (235.2108467504088, 0.9606302650695717, (
                0.9606302650695717, 0.7351330733479711, 0.35688897070126213,
                0.02540912864397729, 0.0)),
            "dependant_factor": (62.08157280555451, 0.1962284948587069, (
                0.019298392906900864, 0.11381594259954832, 0.19495379476879957,
                0.09502057509908686, 0.00039051969154767056)),
            "annuity_pp": (701987.3693830438, 6651.593132643529, (
                0.0, 0.0, 3272.1430623515494, 0.0, 6651.593132643529)),
            "cum_annuity_all": (106655349.13359152, 269328.2269246159, (
                19941.43339048627, 104886.36623117932, 200879.1996505286,
                261119.18507579862, 269328.2269246159)),
            "vp_balance": (833236.1332074542, 29850.9125, (
                29850.9125, 0.0, 0.0, 0.0, 0.0)),
        },
    },
    23: {"rows": 582, "months": (0, 145, 290, 435, 581),
        "result_cf": {
            "pols_if": (347.38626527230383, 0.9986414813716636, (
                0.9986414813716636, 0.9569125799377458, 0.7310100056068868,
                0.20547209018350543, 0.0007810393830953411)),
            "annuity_payments": (203959.47023296118, 1663.3306192174425, (
                0.0, 0.0, 1468.9552140722778, 0.0, 2.1785297345360415)),
            "claims_vp": (892.1975717977265, 28.002637202196023, (
                28.002637202196023, 0.0, 0.0, 0.0, 0.0)),
            "claims_prop": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (1427.9647659956797, 3.814220896097501, (
                2.4966037034291593, 3.4108213215157646, 3.7149820779031657,
                1.488788264970661, 0.008068628646429783)),
            "liability_cf": (206279.63257075462, 1666.9595227063146, (
                30.499240905625182, 3.4108213215157646, 1472.670196150181,
                1.488788264970661, 2.1865983631824712)),
            "net_cf": (-206279.63257075462, 1666.9595227063146, (
                -30.499240905625182, -3.4108213215157646, -1472.670196150181,
                -1.488788264970661, -2.1865983631824712)),
        },
        "result_pols": {
            "pols_if": (347.38626527230383, 0.9986414813716636, (
                0.9986414813716636, 0.9569125799377458, 0.7310100056068868,
                0.20547209018350543, 0.0007810393830953411)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "lives_if_1": (223.75207242707788, 0.9478898134802793, (
                0.9478898134802793, 0.7159216813773177, 0.3395509232434521,
                0.022877055578206393, 0.0)),
            "lives_if_2": (305.9445930205485, 0.9739298835972843, (
                0.9739298835972843, 0.8483255594050328, 0.5927165259824154,
                0.18687007161964506, 0.0007810393830953411)),
            "certain_floor": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "payment_factor": (223.75207242707788, 0.9478898134802793, (
                0.9478898134802793, 0.7159216813773177, 0.3395509232434521,
                0.022877055578206393, 0.0)),
            "dependant_factor": (61.81709642261301, 0.1962284948587069, (
                0.025375833945692157, 0.12049544928021405, 0.19572954118171734,
                0.09129751730264951, 0.00039051969154767056)),
            "annuity_pp": (583419.4984148317, 5578.540037001206, (
                0.0, 0.0, 2744.2720437215457, 0.0, 5578.540037001206)),
            "cum_annuity_all": (90420967.87937877, 227942.38869908007, (
                23982.9184661188, 94851.46313810047, 173496.21979792096, 221512.36973973288,
                227942.38869908007)),
            "vp_balance": (715204.6502170002, 25700.0, (
                25700.0, 0.0, 0.0, 0.0, 0.0)),
        },
    },
}
# END generated fingerprint: PA_UK_SEC


# ---------------------------------------------------------------------------
# Compiled (UKLIB-SEC-PLAN.md U2, the C step, after USLIB-SEC-PLAN.md's Phase 2)
#
# These compile the model, once a session, into a temporary directory (conftest.sec_build),
# and run the compiled package in a child process only.  They skip without modelx-cython or
# a C compiler, and the cython_uk CI job, which sets UKLIB_REQUIRE_CYTHON=1, fails a skip.
# test_compiled_conventions_uk.py checks the compiled model's types, its caches and its
# release, and compares it with modelx on the committed points; these hold what is PA's
# own: the comparison on the splice grid under each of its sets of References, the RPI
# rows among them, on the variants no committed row holds, at the contract's extremes,
# where the cap on mortality binds, on every value a decoded column holds and on keys
# written as floats; the LPI rows under their own RPI; the labels; the refusals and the
# overflows; the deepest calls on a 1 MiB stack; a Reference set late; and the runner.


def _as_modelx(have, want):
    """Whether a compiled value is modelx's: identical where ``exact_here()``, as on
    x86-64, and to 1e-12 relative elsewhere, as C4 compares (uk_sec_support)."""
    return have == want if exact_here() else have == pytest.approx(want, rel=1e-12, abs=0)


def _mismatch_lines(found):
    return f"{len(found)} mismatches, first:\n  " + "\n  ".join(found[:50])


# How many rows of a grid C4 compares at once.  compiled_mismatches sweeps every row of its
# case in one modelx read and keeps every value of every row, in the parent and in the
# child, until it compares them, and modelx's record of a row on the table basis, its
# survival check's quadratic reads among it, holds about 110 MB on a frame of 636 months
# (*Record -- M11*): ten rows hold about half what ULB's chunks of twenty did, its rows a
# third as long.  The record grows as the square of the frame, so a row at the contract's
# longest cover, 1,392 to 1,512 months, holds five to six times as much, and the extremes
# go one row at a time: all eighteen in one read took the module past 6 GB (measured at
# M12).
C4_CHUNK = 10
EXTREMES_CHUNK = 1


def _c4_chunks(build, table, refs, root, also=None, size=C4_CHUNK):
    """C4 on ``table`` ``size`` rows at a time under ``refs``, each row with ``also``,
    :func:`_pa_c4_also` by default: the mismatch lines.  Each chunk's case is read back,
    and the rows the chunks compared must be the table's, every one once, in order."""
    found, compared = [], []
    for start in range(0, len(table), size):
        chunk = table.iloc[start:start + size]
        case = compiled_case(build, root / f"chunk{start}", model_points=chunk)
        compared += list(pd.read_csv(case.parent / TABLE, index_col="point_id").index)
        found += [f"rows {start} on: {line}"
                  for line in compiled_mismatches(build, case, refs=refs,
                                                  also=also or _pa_c4_also)]
    labels = list(table["point_id"] if "point_id" in table.columns else table.index)
    assert compared == labels, f"C4 compared {len(compared)} rows of {len(labels)}"
    return found


@pytest.mark.cython
def test_the_compiled_model_computes_what_modelx_computes_on_the_splice_grid(spliced,
                                                                             sec_build,
                                                                             tmp_path):
    """C4 on the branches: compiled, every cell of the splice grid is modelx's.

    The sample traces the committed points alone, and they leave branches untaken, which
    are typed all the same, because every branch of a cell returns the one type the others
    return (sample_sec.py).  What the compiled model computes on them is held here: the
    splice grid's rows, S's points and its sixteen variants restated in payment at T2's
    months and starting later, under each of the splice's sets of References
    (:data:`SPLICE_SETS`), inflation at 0 and the RPI at the shipped 3%, at 8% and at -2%,
    where the LPI's cap and floor bind and the ratchet freezes, the RPI rows and the fixed
    point 2 beside them, set on modelx and on the compiled model before either computes.
    The grid is the one this run's ``spliced`` selects, the core by default and the full
    grid under ``UKLIB_SEC_FULL=1``, and the test carries no ``sec_full`` mark, since a
    skipped compile test fails the cython_uk job.  Each set's SEC table goes beside the
    build :data:`C4_CHUNK` rows at a time, modelx sweeps every point fully, and the compiled
    model must agree at every argument modelx caches, identically on x86-64 and to 1e-12
    relative elsewhere, with every raise and every ``Data`` array
    (``uk_sec_support.compiled_mismatches``).
    """
    build = sec_build(SEC)
    found = []
    for rates, refs in SPLICE_SETS.items():
        folder = spliced.pair(rates)[1].Data.input_dir()
        table = pd.read_csv(folder / TABLE, index_col="point_id")
        found += [f"{rates}: {line}" for line in
                  _c4_chunks(build, table, refs, tmp_path / rates)]
    assert not found, _mismatch_lines(found)


# The variants no committed row and no fingerprint holds, whose branches C2 cannot freeze
# (UKLIB-SEC-PLAN.md §6.7, *Record -- M11*, carried): the table basis paying in advance,
# last-survivor value protection claimed after an advance instalment (20); value protection
# apart from the dependant's share (23), and on a single life (24); a dependant older than
# the annuitant (25); and a dependant's share of 0 (26).
UNFROZEN_VARIANTS = (20, 23, 24, 25, 26)


@pytest.mark.cython
def test_the_compiled_model_computes_what_modelx_computes_on_the_unfrozen_variants(
        sec_build, tmp_path):
    """C4 on the variants C2 cannot freeze: every row of each, compiled, is modelx's.

    The core grid holds one row of each of :data:`UNFROZEN_VARIANTS`, and no committed row
    and no fingerprint holds any, so a compiled model that parted from modelx on their
    branches would part nowhere else.  Here each is generated from a copy of S's table with
    the variants, as the splice generates it: its twin, starting at the valuation date, and
    a row restated in payment at each of its own splice months (:data:`VARIANT_MTHS`),
    opened with S's state there, by default as on the full grid, at the shipped References
    and the splice's inflation of 0.  modelx sweeps every row fully, and the compiled model
    must agree everywhere.
    """
    build = sec_build(SEC)
    s = mx.read_model(temp_inputs(tmp_path / "s", model_path(TWIN), model_points=(
        _s_table_with_variants())), name=_name("unfrozen_s"))
    try:
        s.Projection.inflation_rate = 0.0
        derived = tuple((p, d) for p in UNFROZEN_VARIANTS for d in VARIANT_MTHS[p]
                        if _owes(p, d))
        spec = dataclasses.replace(SPEC, derived=derived, future=(), derived_refs={})
        table, _ = build_sec_table(spec, s)
    finally:
        s.close()
    keep = table["source_policy_id"].isin(
        [_s_table_with_variants().at[p, "policy_id"] for p in UNFROZEN_VARIANTS])
    table = table[keep]
    assert len(table) == len(UNFROZEN_VARIANTS) + len(derived)
    found = _c4_chunks(build, table, {"inflation_rate": 0.0}, tmp_path / "unfrozen")
    assert not found, _mismatch_lines(found)


def _contract_extremes(tmp_path):
    """The rows at the contract's extremes, built by the generator.

    Each shape of :data:`SHAPES` at its longest cover, 1,392 months from the start, every
    covered life issued at :data:`YOUNGEST` on its basis, the table basis under a guarantee
    of 1,392 months, at the contract's largest limiting age, :data:`OMEGA_MAX`, in a copy of
    S's table, S read under that limiting age: its twin, starting at the valuation date; the
    same starting ``future_horizon_mth``, 120 months, after it, a frame of 1,512 months;
    and the same restated in payment in the last month of its frame, opened with S's state
    there.  So ``t`` reaches 1,512, the policy month 1,392, the policy year 117, the
    anniversary 115, the attained age 115 and each code its last, the furthest
    ``spec_sec.py`` sizes for.  Returns the rows.
    """
    s_table = _s_table()
    rows = []
    for i, (s_point, basis, guarantee, _) in enumerate(SHAPES, start=1):
        age = YOUNGEST[basis]
        changes = {"annuitant_age": age, "guarantee_months": guarantee,
                   "policy_id": f"PA-7000{i:02d}"}
        if bool(s_table.at[s_point, "dependant_present"]):
            changes["dependant_age"] = age
        row = s_table.loc[[s_point]].assign(**changes)
        row.index = pd.Index([70 + i], name="point_id")
        rows.append(row)
    s = mx.read_model(temp_inputs(tmp_path, model_path(TWIN), model_points=pd.concat(rows)),
                      name=_name("extremes_s"))
    try:
        s.Projection.omega_age = OMEGA_MAX
        last = {70 + i: LONGEST - 1 for i in range(1, len(SHAPES) + 1)}
        spec = dataclasses.replace(SPEC, derived=tuple(last.items()),
                                   future=tuple((p, 120) for p in last), derived_refs={})
        table, _ = build_sec_table(spec, s)
    finally:
        s.close()
    return table


@pytest.mark.cython
def test_the_compiled_model_computes_what_modelx_computes_at_the_contract_extremes(
        sec_build, tmp_path):
    """C4 where the caches end: the contract's longest covers, every cell compiled.

    The rows of :func:`_contract_extremes`, each shape at its longest cover from the
    youngest issue age its basis projects, the table basis under the 1,392-month guarantee
    ``proj_len()`` admits at the contract's largest limiting age, :data:`OMEGA_MAX`, set on
    both engines, starting now and 120 months on and in payment in its last month, read
    every cache as far as ``spec_sec.py`` sizes it for: ``t`` to 1,512, the frame's closing
    time point; ``k`` to 1,392; ``y`` to 117, the opening of the year that closing point
    begins; ``a`` to 115 and ``x`` to 115; and every timing and kind.  modelx sweeps
    every row fully, with the payments to date at every key the frame reads and their
    refusals beside them, and the compiled model must agree everywhere.  A cache one too
    small for the contract raises ``IndexError`` compiled where modelx reads on, and fails
    here, though the spec check passes it, which holds the caches to the spec and not the
    spec to the contract.  The rows go :data:`EXTREMES_CHUNK` at a time, each read
    released before the next, since a sweep's record grows as the square of the frame.
    """
    build = sec_build(SEC)
    rows = _contract_extremes(tmp_path / "s")
    covers = rows["guarantee_months"].clip(lower=12 * (OMEGA_MAX - rows["annuitant_age"]))
    assert (covers - rows["duration_mth"]).max() == LONGEST + 120 == 1512
    assert (covers == LONGEST).all()
    found = _c4_chunks(build, rows, {"omega_age": OMEGA_MAX}, tmp_path / "extremes",
                       size=EXTREMES_CHUNK)
    assert not found, _mismatch_lines(found)


@pytest.mark.cython
def test_the_compiled_model_computes_what_modelx_computes_at_the_frame_s_edge(sec_build,
                                                                             tmp_path):
    """C4 at the frame's edge on the scenario basis: the longest frame ``proj_len()``
    admits past ``omega_age_max``, every cell compiled.

    The scenario basis reads no table, and its limiting age is held to no bound, so there
    the frame alone, held to the table basis's longest, 1,392 months from the start, keeps
    the reads in the caches.  The worked example at the frame's edge, the worst
    configuration they meet (:func:`_frame_edge`), value protection on the first death,
    issued 120 months on, both lives at 1 under a limiting age of 117 set on both engines
    (:data:`FRAME_REFS`), reads ``t`` to 1,512, ``k`` to 1,392, ``y`` to 117 and ``a`` to
    115, the furthest ``spec_sec.py`` sizes for.  modelx sweeps it fully, and the compiled
    model must agree everywhere; a guarantee a month longer is refused alike, message for
    message (:data:`NOT_ISSUED`, the refusal test).
    """
    build = sec_build(SEC)
    table = _frame_edge(LONGEST)(_committed()).loc[[1]]
    found = _c4_chunks(build, table, FRAME_REFS, tmp_path / "edge", size=EXTREMES_CHUNK)
    assert not found, _mismatch_lines(found)


# The codes each cell that takes one is called at, on every row C4 compares, by the sweep
# and _pa_c4_also between them: the timings, the kinds of the claims and of the payments
# to date, and the two lives in every cell of a life that the row's basis reads.  The
# scenario basis reads each life's month of death and no mortality; the table basis the
# mortality cells, survival blocked by policy year, and no month of death.
CODED = {"pols_if_at": "timing", "claims": "kind", "cum_annuity_pp": "kind"}
LIFE_CELLS = {
    "scenario": ("age_at_entry", "sex", "death_mth", "lives_if_init", "lives_if",
                 "lives_death"),
    "table": ("age_at_entry", "sex", "mort_schedule", "rating_factor", "lives_if_init",
              "age", "mort_rate_base", "improve_rate", "improve_factor", "mort_rate",
              "mort_rate_mth", "lives_if", "lives_death", "lives_if_py",
              "mort_rate_base_at")}
# The cells of a life a single-life contract is asked at either life: the label, which
# returns the column as read, survival, which reads the second life as none, and the death
# densities _pa_c4_also asks.  Every other is asked at the annuitant alone, a second life
# being refused, invalid life.
EITHER_LIFE = ("sex", "lives_if", "lives_death")

# The stand-ins test_c4_asks_every_cell_at_every_code reads the codes on, a row of each
# basis and each kind, as (basis, kind, the row): joint contracts with value protection on
# the first death, which read every code, the worked example's twin on the scenario basis,
# point 1, and on the table basis, point 2; each restated in payment, at 17 months, point
# 11, and at 101, point 16; and starting 13 months after the valuation date, the RPI
# catch-up, point 20, and the worked example, which no committed row is, made here from
# point 1 (None).  And a single life on the table basis, the rated twin, point 8, which
# reads no annuitant's payments to date.
CODE_ROWS = (("scenario", "twin", 1), ("scenario", "derived", 11),
             ("scenario", "future", None), ("table", "twin", 2), ("table", "derived", 16),
             ("table", "future", 20), ("table", "twin", 8))


def test_c4_asks_every_cell_at_every_code(tmp_path):
    """C4's sweep and its ``also`` ask every cell that takes a code at every code it takes,
    on each row they compare.

    C4 compares the compiled model with modelx at the arguments modelx caches, so a code no
    cell asks would go uncompared: the payments to date at ``ALL``, which no cell reads, and
    the death densities, which the last-death density replaces, among them
    (:func:`_pa_c4_also`).  What a row asks depends on its basis and its kind, so the codes
    are held row by row, on a stand-in of each basis and each kind of row
    (:data:`CODE_ROWS`), each swept fully on a fresh read, with the ``also``: both timings
    of the count; the claims' two kinds and their total; the payments to date at ``ALL``,
    and at ``ANNUITANT`` under value protection on the first death; and both lives in every
    cell of a life the row's basis reads (:data:`LIFE_CELLS`), on a single life in those
    that read the second life as none (:data:`EITHER_LIFE`) and the annuitant alone in the
    rest.  A code asked on one row alone would leave the others uncompared there, which a
    union over the rows would not see.  Each row is released once its codes are read, as
    C4 releases none: a full sweep holds the survival check's quadratic record
    (:data:`C4_CHUNK`).  The ``also`` must be the spec's ``c4_also``, which the
    conventions' C4 on the committed points passes (``uk_sec_support.spec_c4_also``).
    """
    assert SPEC.c4_also is _pa_c4_also, SPEC.c4_also
    committed = _committed()
    late = committed.loc[[1]].assign(duration_mth=-13, row_kind="future", source_mth=-13)
    late.index = pd.Index([committed.index.max() + 1], name="point_id")
    model = mx.read_model(_sec_inputs(tmp_path, pd.concat([committed, late])),
                          name=_name("codes"))
    try:
        table = model.Data.model_point_table()
        found = {}
        for basis, kind, label in CODE_ROWS:
            label = late.index[0] if label is None else label
            assert (table.at[label, "mort_basis"], table.at[label, "row_kind"]) == (
                basis, kind), label
            key = _key(model, label)
            p = projection(model, key)
            if ("proj_len", ()) not in full_sweep(p):
                _pa_c4_also(p)
            seen = {}
            for name in (*CODED, *LIFE_CELLS["table"], "death_mth"):
                cells = p.cells[name]
                where = list(cells.parameters).index(CODED.get(name, "life"))
                for args in cells.keys():
                    args = args if isinstance(args, tuple) else (args,)
                    seen.setdefault(name, set()).add(args[where])
            joint = p.is_joint()
            want = {"pols_if_at": {p.BEF_NB, p.BEF_DECR},
                    "claims": {p.VP, p.PROP, p.ALL},
                    "cum_annuity_pp": ({p.ANNUITANT, p.ALL} if p.vp_pct() > 0.0
                                       and p.is_first_death() else {p.ALL}),
                    **{name: {1, 2} if joint or name in EITHER_LIFE else {1}
                       for name in LIFE_CELLS[basis]}}
            if seen != want:
                found[basis, kind, label] = {
                    name: (seen.get(name), want.get(name))
                    for name in {*seen, *want} if seen.get(name) != want.get(name)}
            _release(model, key)
        assert not found, found
    finally:
        model.close()


@pytest.mark.cython
def test_the_compiled_model_computes_what_modelx_computes_where_the_cap_binds(sec_build,
                                                                              tmp_path):
    """C4 where ``mort_rate`` caps the annual rate at 1: compiled, every cell is modelx's.

    S's point 8, the single life rated 1.35, whose rated rate passes 1 from policy month 576
    to 599: its twin, and its rows restated in payment the month before the cap binds and
    in its first capped month, built by the generator from S, go beside the build.  First,
    in modelx, the cap is asserted reached on the twin, ``mort_rate`` and ``mort_rate_mth``
    the float 1.0 at every month from 576 to 599, so that the case reaches the side of
    ``min(q, 1.0)`` that returns the bound.  modelx then sweeps the rows fully, and the
    compiled model must agree at every argument modelx caches, identically on x86-64 and to
    1e-12 relative elsewhere (``uk_sec_support.compiled_mismatches``): no other compiled
    test reaches that side on a frame where every life in payment dies in a month.
    """
    build = sec_build(SEC)
    s = mx.read_model(model_path(TWIN), name=_name("capped_s"))
    try:
        spec = dataclasses.replace(SPEC, derived=((8, 575), (8, 576)), future=(),
                                   derived_refs={})
        table, _ = build_sec_table(spec, s)
    finally:
        s.close()
    table = table[table["source_policy_id"] == _s_table().at[8, "policy_id"]]
    assert sorted(table["source_mth"]) == [0, 575, 576]
    folder = compiled_case(build, tmp_path / "capped", model_points=table)
    model = mx.read_model(folder, name=_name("capped"))
    try:
        twin = _point(model, int(table.loc[table["row_kind"] == "twin", "point_id"].iloc[0]))
        for t in range(576, 600):
            assert twin.mort_rate(t, 1) == twin.mort_rate_mth(t, 1) == 1.0, t
        assert twin.mort_rate(575, 1) < 1.0
    finally:
        model.close()
    found = compiled_mismatches(build, folder, also=_pa_c4_also)
    assert not found, _mismatch_lines(found)


@pytest.mark.cython
def test_the_compiled_model_computes_what_modelx_computes_on_every_decoded_value(
        sec_build, tmp_path):
    """C4 on every value a decoded column holds: compiled, every cell is modelx's.

    The twins of :data:`DECODED`'s points, each timing, escalation basis, value-protection
    basis and mortality basis, each sex of each life, a dependant and none, the overlap and
    the proportionate payment each way, each frequency and a start year with a fraction,
    built by the generator from a copy of S's table, go beside the build: modelx sweeps
    them fully, with each life's label, and the compiled model must agree everywhere, each
    decode's flag and the mortality row each sex selects among them, which the committed
    points, all male annuitants on four of the bases' values, reach only in part.  The
    twins go :data:`C4_CHUNK` at a time.
    """
    build = sec_build(SEC)
    s, sec, _ = _decoded_tables(tmp_path / "tables")
    try:
        twins = sec.Data.model_point_table()
    finally:
        sec.close()
        s.close()
    found = _c4_chunks(build, twins, {}, tmp_path / "decoded")
    assert not found, _mismatch_lines(found)


# The model point table's columns that hold whole numbers, which a spreadsheet may save as
# floats: the months, the ages, the frequency, the guarantee and the start year.  And the
# mortality table's ages.
FLOAT_COLUMNS = ("duration_mth", "annuitant_age", "frequency", "guarantee_months",
                 "start_year")
FLOAT_KEYS = {MORT: lambda t: t.assign(age=t["age"].astype(float))}


@pytest.mark.cython
def test_the_compiled_model_reads_keys_written_as_floats_as_modelx_does(sec_build,
                                                                         tmp_path):
    """C4 on keys written as floats: the compiled model reads 65.0 as 65, as modelx does.

    The committed table with its labels written ``1.0`` to ``23.0`` and its whole numbers as
    floats (:data:`FLOAT_COLUMNS`), and the mortality table's ages as floats
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
    found = compiled_mismatches(build, folder, also=_pa_c4_also)
    assert not found, _mismatch_lines(found)


@pytest.mark.cython
def test_the_compiled_lpi_rows_hold_the_cap_and_the_floor_under_their_own_rpi(sec_build,
                                                                             tmp_path):
    """Compiled, each LPI row projects its cap's or its floor's goldens under its own RPI.

    The committed LPI rows read under an RPI of their own (``derived_refs``), point 22 from
    S under 8%, its increases capped at 5%, and point 23 under -2%, its income held at the
    floor, are projected in modelx under their own RPI by
    ``test_the_lpi_rows_hold_the_cap_and_the_floor_under_their_own_rpi``, which the
    fingerprint, read at the shipped 3%, cannot freeze (*Record -- M11*).  Compiled, no cache
    is cleared when a Reference is set, so each row runs in a child of its own whose
    ``rpi_rate`` is set on the base ``Projection`` before any ItemSpace is made (K7): the
    row's income in each year and its whole ``result_cf`` must be modelx's under the same
    RPI, identically on x86-64, and the income each year the golden of :data:`LPI_BOUNDS`.
    """
    build = sec_build(SEC)
    folder = compiled_case(build, tmp_path / "lpi")
    table = _committed()
    model = None
    for (s_point, month), (rpi, cap, first, years) in LPI_BOUNDS.items():
        label = _label(table, "derived", s_point, month)
        idx = list(table.index).index(label)
        model = mx.read_model(folder, name=_name("lpi"))
        try:
            model.Projection.rpi_rate = rpi
            p = projection(model, point_keys(model)[idx])
            y0 = p.policy_year_init()
            want = [p.annual_income(y0 + i) for i in range(len(years) + 1)]
            frame = p.result_cf()
        finally:
            model.close()
        calls = [("annual_income", (y0 + i,)) for i in range(len(years) + 1)]
        calls.append(("result_cf", ()))
        got = run_compiled(folder.parent, build.package.name,
                           {"refs": {"rpi_rate": rpi}, "calls": {idx: calls}})
        assert got["exit"] == 0, got["stderr"]
        values = got["values"][idx]
        assert all(status == "ok" for status, _ in values), values
        incomes = [value for _, value in values[:-1]]
        assert all(_as_modelx(h, w) for h, w in zip(incomes, want)), (label, incomes, want)
        assert incomes[0] == pytest.approx(first, abs=1e-9), (label, incomes[0])
        assert incomes[1:] == pytest.approx(list(years), rel=1e-12), (label, incomes)
        assert frame_mismatches(frame, values[-1][1], rtol=0.0 if exact_here() else 1e-12,
                                atol=0.0) == [], label


# The labels compiled against modelx: each point's labels as the committed table holds
# them, and on a copy whose scenario points hold a sex no projection reads, a blank and a
# number, which a label traced on text alone would raise TypeError on, compiled.
LABEL_CALLS = (("payment_timing", ()), ("escalation_type", ()), ("vp_basis", ()),
               ("mort_basis", ()), ("sex", (1,)), ("sex", (2,)))


@pytest.mark.cython
def test_the_compiled_labels_return_what_modelx_returns(sec_build, tmp_path):
    """Compiled, each label returns what modelx returns, a blank and a number among them.

    ``sex(life)`` returns its column as read, a single-life contract's blank second life as
    NaN, and a scenario point's sex, which no projection reads (``Data``, *refused by
    point*), may be blank or any text, a 7 among them, which pandas reads as text beside
    the others; the four validating labels return text or raise.  The shared
    ``uk_sec_support.label_mismatches`` takes labels without a parameter, so this runs its
    own comparison, as ``Term_UK_SEC``'s module does: on the committed table with the worked
    example's twin holding a blank annuitant's sex and the scenario twin of point 3 a 7,
    every label of :data:`LABEL_CALLS` on every point, in modelx and compiled, must return
    the same value of the same kind, NaN meeting NaN, or the same raise.  A ``sex``
    compiled to ``str`` raises ``TypeError`` on the blank (C3, uslib's M22), and fails
    here.
    """
    build = sec_build(SEC)
    table = _then(_set("annuitant_sex", [1], float("nan")),
                  _set("annuitant_sex", [3], 7))(_committed())
    folder = compiled_case(build, tmp_path / "labels", model_points=table)
    model = mx.read_model(folder, name=_name("labels"))
    try:
        keys = point_keys(model)
        want = {key: [_did(lambda: projection(model, key).cells[cell](*args))
                      for cell, args in LABEL_CALLS] for key in keys}
    finally:
        model.close()
    got = run_compiled(folder.parent, build.package.name,
                       {"refs": {}, "calls": {key: list(LABEL_CALLS) for key in keys}})
    assert got["exit"] == 0, got["stderr"]
    found = []
    for key in keys:
        for (cell, args), mine, have in zip(LABEL_CALLS, want[key], got["values"][key]):
            blank = (mine[0] == have[0] == "ok" and isinstance(mine[1], float)
                     and isinstance(have[1], float) and mine[1] != mine[1]
                     and have[1] != have[1])
            if not (blank or (mine == have and type(mine[1]) is type(have[1]))):
                found.append(f"idx {key}: {cell}{args} compiled {have!r}, modelx {mine!r}")
    assert want[0][4][0] == "ok" and want[0][4][1] != want[0][4][1], want[0]
    assert want[2][4] == ("ok", "7"), want[2]
    assert not found, found


# The compiled refusals' child: one process, which imports the compiled package once and
# runs each case on a fresh instance of the model, whose Data reads the case's own copies
# of the two files by absolute path.  A refusal names a file by its Reference, so the
# child's names the path, and the test writes each path as the file's name (_named), as
# modelx, reading the files by name, writes it.
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
CASE_FILES = {"model_point_file": TABLE, "mort_table_file": MORT}


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
# fraction is truncated as it is set, 115.5 to 115, where modelx computes with 115.5, so
# the compiled refusals take a domain's cases at whole numbers alone, and model-sec.md says
# to set each as a whole number (UKLIB-SEC-PLAN.md §6.1, *Record -- M2*).
INT_REFERENCES = frozenset({"issue_age_min", "omega_age", "omega_age_max",
                            "mort_table_year"})


def _held_compiled(refs):
    """Whether the compiled model holds every one of ``refs`` as modelx does."""
    return all(math.isfinite(value) and value == value // 1 and abs(value) < 2.0 ** 63
               for ref, value in refs.items() if ref in INT_REFERENCES)


# Codes no cell takes, inside the one inner width every 2-D cache shares, which each cell
# refuses by its own formula, ValueError, in both engines, as (call, arguments), on point 1:
# the two timings past BEF_DECR in the count's cell; the payments' kind in the claims';
# each claims kind in the payments' cell; and the lives 0 and 3, in a life's 1-D cache and
# in a 2-D one.  Each slot of the cache a call leaves unused is a code some other cell
# takes, or a life none does, so a cell must refuse it itself.
CODES_IN_CACHE = [("pols_if_at", (0, 2)), ("pols_if_at", (0, 3)), ("claims", (0, 2)),
                  ("cum_annuity_pp", (5, 0)), ("cum_annuity_pp", (5, 1)),
                  ("lives_if_init", (0,)), ("lives_if_init", (3,)), ("age_at_entry", (0,)),
                  ("mort_rate", (0, 3)), ("lives_if", (0, 3)), ("death_mth", (0,)),
                  ("death_mth", (3,))]

# Projection's idx past the extract's last row, 23, and -1, beside the last row, 22, as
# (position, cell, arguments): past the last row the first read of a vector raises
# IndexError in both engines, each in its own words, and -1 reads every vector at its last
# element in both, so it is the last point, under that point's own point_id.
IDX_CASE = "an idx past the table and one before it"
IDX_EDGES = [(23, "point_id", ()), (23, "result_cf", ()), (-1, "point_id", ()),
             (-1, "proj_len", ()), (-1, "net_cf", (0,)), (22, "point_id", ()),
             (22, "proj_len", ()), (22, "net_cf", (0,))]

# Calls past the caches spec_sec.py sizes, which raise IndexError in the compiled model
# alone, on the extract's first row, point 1, the worked example's twin, as (call,
# arguments): a month either side of the t cache, which modelx answers with 0, the month
# outside the frame; a timing, a kind and a life past the one inner width, which modelx
# refuses as codes it does not take; a key, a policy year, an anniversary and an attained
# age past their caches, each of which modelx computes or refuses as at any other.  No
# frame of the contract reads any of them.
COMPILED_ONLY = [("net_cf", (1514,)), ("net_cf", (-1,)), ("pols_if_at", (0, 4)),
                 ("claims", (0, 4)), ("cum_annuity_pp", (5, 4)), ("lives_if", (5, 4)),
                 ("cum_annuity_pp", (1394, 2)), ("annual_income", (118,)),
                 ("lives_if_py", (118, 1)), ("rpi_peak", (117,)),
                 ("mort_rate_base_at", (117, 1))]


def _refusal_cases(anniversary=None):
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
    for case, column, value, refused, _, _ in BY_POINT:
        cases.append((f"by point: {case}", extract(_by_point_edit(case, column, value,
                                                                  [refused])), None,
                      {}, [(at(refused), "result_cf", ())], ()))
    for column, point, _ in FLAG_READERS:
        for value in FLAG_SPELLINGS:
            cases.append((f"{column} written {value!r}",
                          extract(_set(column, [point], value)), None, {},
                          [(at(point), "result_cf", ())],
                          () if column == "overlap" else ("model_point_table",)))
    for case, edit, message in UNREADABLE:
        cases.append((case, extract(), {MORT: edit}, {}, [(at(2), "result_cf", ())],
                      ("mort_age_first",)))
    for case, edit, point, _ in UNDECODABLE:
        cases.append((case, extract(edit), None, {}, [(at(point), "result_cf", ())], ()))
    for case, edit, refs, point, _, _ in NOT_ISSUED:
        cases.append((case, extract(edit), None, refs,
                      [(at(point), cell, ()) for cell in ("result_cf", "proj_len")], ()))
    for case, edit, point, message in OWING_NOTHING:
        if message is not None:
            cases.append((case, extract(edit), None, {},
                          [(at(point), cell, ()) for cell in ("result_cf", "proj_len")],
                          ()))
    for case, refs, point, message, report in DOMAINS:
        if message is not None and _held_compiled(refs):
            cases.append((f"domain {case}", extract(), None, refs,
                          [(at(point), "result_cf", ()), (at(point), "proj_len", ())], ()))
        elif report is not None and _held_compiled(refs):
            cases.append((f"domain {case}, its report", extract(), None, refs,
                          [(at(point), "result_cf", ())], ()))
    for case, refs, point, _ in PAST_FLOATS:
        cases.append((case, extract(), None, refs, [(at(point), "result_cf", ())], ()))
    for case, edit, refs, (s_point, month), _, _ in INCOMES:
        label = _label(committed, "twin" if month == 0 else "derived", s_point, month)
        cases.append((case, extract(edit), None, refs, [(at(label), "result_cf", ())], ()))
    last = _label(committed, "derived", 10, 170)
    frozen = _label(committed, "derived", 6, 60)
    big = 1.7976931348623157e308
    cases.append(("the payments to date past the floats",
                  extract(_then(_set("cum_annuity_all_init", [last], big),
                                _set("annual_income", [last], 1e300),
                                _set("cum_annuity_pp_init", [frozen], big),
                                _set("annual_income_init", [frozen], 1e300))), None, {},
                  [(at(last), "result_cf", ()), (at(frozen), "result_cf", ())], ()))
    if anniversary is not None:
        on_last, on_frozen, edit = anniversary
        cases.append(("the payments to date past the floats on an anniversary",
                      extract(edit), None, {},
                      [(at(on_last), "result_cf", ()), (at(on_frozen), "result_cf", ())],
                      ()))
    for case, refs, point, cell, args, _ in POWER_BASES:
        cases.append((case, extract(), None, refs, [(at(point), cell, args)], ()))
    cases.append(("at its stop", extract(_set("duration_mth", [10], 636)), None, {},
                  [(at(10), "result_cf", ()), (at(10), "proj_len", ())], ()))
    cases.append(("an age below the mortality table",
                  extract(_set("annuitant_age", [2], 49)), None, {},
                  [(at(2), "result_cf", ()), (at(2), "mort_rate", (0, 1))], ()))
    for case, edit, point, cell, args, _ in NOT_HELD:
        if edit is not None:
            cases.append((case, edit(committed), None, {}, [(point - 1, cell, args)],
                          ("point_id",) if cell == "result_cf" else ()))
    cases.append(("codes no cell takes, inside the caches", extract(), None, {},
                  [(at(1), cell, args) for cell, args in CODES_IN_CACHE], ()))
    return cases


@pytest.mark.cython
def test_the_compiled_model_refuses_what_modelx_refuses(sec_build, tmp_path):
    """Compiled, the model refuses what modelx refuses, with modelx's error and message.

    A ``ValueError`` raised in a cell typed ``long long`` or ``double`` propagates out of
    the compiled model as out of modelx.  So, each on its own inputs and References
    (:func:`_refusal_cases`), on an extract labelled otherwise than by position: every case
    of :data:`MALFORMED`, refused by a projection and by ``Data``'s reader; every case of
    :data:`BY_POINT`, by the projection of the point that reads the column alone; each flag
    spelt as only ``PA_UK_S``'s ``bool()`` reads it (:data:`FLAG_SPELLINGS`), by the check,
    as the table is read or by the point; every case of :data:`UNREADABLE`, by a projection
    and by the ``Data`` cell that checks the table, so that a compiled ``Data`` cell
    refuses each value its modelx cell refuses; every text no decode knows; every case of
    :data:`NOT_ISSUED` and of :data:`OWING_NOTHING`, by ``result_cf`` and ``proj_len``;
    every case of :data:`DOMAINS` that refuses and that the compiled model can hold, its
    integer References whole (:func:`_held_compiled`), each printed as the compiled model
    types it; each power, each income and the payments past the floats, which the compiled
    powers reach through Python's own power where C's gives an infinity, uslib's M22 form,
    so that the compiled model raises the cell's refusal as modelx does
    (:data:`PAST_FLOATS`, :data:`INCOMES`); a label, a start year and a month of death the
    vectors cannot hold (:data:`NOT_HELD`); and each code of :data:`CODES_IN_CACHE`, inside
    the caches, which the cell's own formula refuses.

    And the refusals that are the compiled model's alone (:data:`COMPILED_ONLY`): a month
    past the ``t`` cache either side, a timing, a kind and a life past their codes, and a
    key, a year, an anniversary and an age past their caches, each raising ``IndexError``
    compiled, beside what modelx does, which is never that.  And ``Projection``'s ``idx`` at
    the table's edges (:data:`IDX_EDGES`): one past the last row raises ``IndexError`` in
    both engines, compared by its type, the words being each engine's own, and ``-1`` is
    the last row in both, its every outcome the last row's and modelx's, which a build
    without bounds checks, or without Python's negative indices, would part from.

    The compiled model runs every case in one child, each on a fresh instance of the model
    that reads the case's own copies of the two files by absolute path
    (:data:`REFUSALS_CHILD`), each path in a message written as the file's name, as modelx
    names it (:func:`_named`), and modelx reads each case afresh.
    """
    build = sec_build(SEC)
    cases = _refusal_cases(_anniversary_edit(tmp_path / "anniversary"))
    plain = len(cases)
    committed = _committed()
    relabelled = committed.rename(index=dict(zip(committed.index, EXTRACT_LABELS)))
    cases.append(("compiled only", relabelled, None, {},
                  [(0, cell, args) for cell, args in COMPILED_ONLY], ()))
    assert len(relabelled) == 23
    cases.append((IDX_CASE, relabelled, None, {}, IDX_EDGES, ()))
    root = tmp_path / "refused"
    compiled_case(build, root / "base")
    jobs, wants = [], []
    for i, (case, table, edits, refs, calls, data) in enumerate(cases):
        folder = temp_inputs(root / f"case{i:03d}", model_path(SEC), model_points=table,
                             model_point_file=TABLE, edits=edits)
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
    for (case, *_, calls, data), (files, *_), (want, want_data), (have, have_data) in zip(
            cases, jobs, wants, got, strict=True):
        have = [_named(did, files) for did in have]
        have_data = [_named(did, files) for did in have_data]
        for (idx, cell, args), modelx_did, compiled_did in zip(calls, want, have,
                                                              strict=True):
            where = f"{case}: idx {idx}: {cell}{args}"
            if case == IDX_CASE:
                edges[idx, cell, args] = (modelx_did, compiled_did)
                if idx == 23:
                    for engine, did in (("modelx", modelx_did), ("compiled", compiled_did)):
                        if (did[0], str(did[1]).split(":")[0]) != ("raised", "IndexError"):
                            found.append(f"{where}: {engine} {did}, not IndexError")
                elif compiled_did != modelx_did:
                    found.append(f"{where}: compiled {compiled_did}, modelx {modelx_did}")
                continue
            if case == "compiled only":
                if str(modelx_did[1]).startswith("IndexError"):
                    found.append(f"{where}: modelx {modelx_did}, which no cache bounds")
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
        if idx == -1 and outcomes != edges[22, cell, args]:
            found.append(f"{IDX_CASE}: {cell}{args} at idx -1 is {outcomes}, at the last "
                         f"row {edges[22, cell, args]}")
    assert edges[-1, "point_id", ()][0] == ("ok", EXTRACT_LABELS[-1]), edges
    assert not found, "\n".join(found[:40])
    assert refused == sum(len(calls) + len(data) for *_, calls, data in cases[:plain])


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

# The chain heads the stack test calls cold, each in an ItemSpace of its own: net_cf, the
# payments to date on every stream, the deepest call a projection makes (the depth test),
# and value protection's balance, which runs the annuitant's payments to date.  The runner
# makes one ItemSpace for each key of a job and deletes it after the key's calls, so a key
# with two calls would run the second warm, on the first's caches.
STACK_HEADS = ("net_cf", "cum_annuity_all", "vp_balance")

# How long the stack test waits for each child, in seconds: one runs in a few seconds, more
# under load.  A bracketing size may kill its child on a stack overflow by design, and
# where the overflow hangs instead, as Windows Error Reporting could, the wait ends sooner
# than for the two runs asserted, and the size is recorded as timed out.
BRACKET_TIMEOUT, ASSERTED_TIMEOUT = 120, 300


@pytest.mark.cython
def test_the_longest_cover_runs_cold_on_a_one_megabyte_stack(sec_build, tmp_path):
    """The deepest call the contract allows runs compiled on a 1 MiB stack (F7).

    On the rows of :func:`_longest_cover`, each shape of :data:`SHAPES` at its longest
    cover, 1,392 months from the start at the contract's largest limiting age,
    :data:`OMEGA_MAX`, every life issued at the youngest age its basis projects, the table
    basis under a 1,392-month guarantee, starting now and 120 months on: the worked example
    and the last-survivor point on the scenario basis, the worked example's table twin, the
    RPI catch-up, the LPI and the rated single life on the table basis.  Each of
    :data:`STACK_HEADS`, cold in the last month, runs the chains back to ``t_entry()``, one
    cell a month within the policy year and two a year before it, survival and the payments
    to date being blocked by policy year: 253 cells deep in modelx at the longest cover
    (:func:`test_every_chain_runs_one_cell_a_month_from_a_cold_start`).  Each runs in an
    ItemSpace of its own, on a copy of its row, so that each is cold: in one ItemSpace the
    second would run on the first's caches, a few cells deep.  Compiled they run on the C
    stack, which the interpreter's recursion limit does not count, and one cell a month they
    needed 244 to 276 KiB of it here, 52 to 76 blocked (UKLIB-SEC-PLAN.md §6.7, *Record --
    M12*).  1 MiB is the stack MSVC gives an executable's main thread unless the executable
    asks for more: a host that embeds Python, where python.exe itself asks for 2,000,000
    bytes.  A thread whose stack is reserved at 1 MiB stands in for it on every platform
    (``uk_sec_support.run_compiled``), and in one each call runs cold and returns modelx's
    number, identically on x86-64 (``uk_sec_support.exact_here``) and to 1e-12 elsewhere.  A
    stack too small kills the child, and the test fails naming the stack.  The thread's
    stack is read back too, from Windows or from glibc, and must be at most 1 MiB and a
    page: a stand-in larger than asked for would stand for nothing.  And the calls run again
    on the child's main thread, which is what ``run_sec.py --cython`` runs on.

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
    frames, tables = [], []
    for k in (0, 120):
        folder, found = _longest_cover(tmp_path / f"rows{k}", k)
        tables.append(pd.read_csv(folder.parent / TABLE, index_col="point_id"))
        frames += [(label + 100 * (k // 120), months, entry)
                   for label, months, entry, _, _ in found]
    tables[1] = tables[1].set_axis(tables[1].index + 100, axis=0)
    rows = pd.concat(tables)
    copies = [rows.set_axis(rows.index + 1000 * i, axis=0) for i in range(len(STACK_HEADS))]
    case = compiled_case(build, tmp_path / "longest", model_points=pd.concat(copies))
    model = mx.read_model(case, name=_name("longest"))
    try:
        model.Projection.omega_age = OMEGA_MAX
        calls, want = {}, {}
        for label, months, entry in frames:
            for i, head in enumerate(STACK_HEADS):
                key = _key(model, label + 1000 * i)
                proj = projection(model, key)
                assert (proj.proj_len(), proj.t_entry()) == (months, entry), label
                calls[key] = [(head, (months - 1,))]
                want[key] = [proj.cells[head](months - 1)]
                _release(model, key)
    finally:
        model.close()
    assert len(calls) == len(frames) * len(STACK_HEADS), "a head shares an ItemSpace"
    assert all(len(each) == 1 for each in calls.values()), "a head runs after another, warm"
    job = {"refs": {"omega_age": OMEGA_MAX}, "calls": calls}

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
    record = (f"the compiled cold net_cf, payments to date and value-protection balance at "
              f"the longest cover, each in an ItemSpace of its own, ran on a thread of "
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
early = p[10]
values = [p.expenses(12), early.expenses(12)]
p.inflation_rate = 0.0
values += [p.expenses(12), early.expenses(12), p[11].expenses(12)]
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
    ``Projection``, the worked example's twin at ``idx`` 0, the worked example in payment
    17 months at ``idx`` 10, made before, and the proportionate payment's point at 16, made
    after, so that a modelx-cython that began to clear caches would be seen here, and the
    advice changed with it.  A compiled value meets modelx's as C4 holds it
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
        before = (p.expenses(12), projection(model, 10).expenses(12))
        p.inflation_rate = 0.0
        fresh = (p.expenses(12), projection(model, 10).expenses(12),
                 projection(model, 11).expenses(12))
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
    modelx's: point 11's description and its first twelve rows and counts, point 20's, the
    catch-up point starting 13 months on, and the block's lines for each point, its first
    twelve rows and its first twelve projection years.

    The same output is what a runner that ignored ``--build`` and ran modelx would print,
    so the runner is also given a directory that holds no build, and must refuse it,
    saying so, rather than print anything.
    """
    build = sec_build(SEC)
    runner = model_path(SEC).parent / "run_sec.py"
    for args in (("11",), ("20",), ("--block",)):
        expected = _run_sec(runner, *args)
        assert _run_sec(runner, *args, "--cython", "--build", str(build.out)) == expected
    empty = tmp_path / "no_build"
    empty.mkdir()
    done = _run_sec(runner, "11", "--build", str(empty), check=False)
    stderr = done.stderr.decode(errors="replace")
    assert done.returncode != 0 and done.stdout == b"", stderr
    assert f"holds no build of {SEC} for this interpreter" in stderr, stderr
