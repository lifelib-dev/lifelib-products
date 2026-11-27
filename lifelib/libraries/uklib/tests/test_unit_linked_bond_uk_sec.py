"""Tests for ULB_UK_SEC: the splice, future business, counts, regeneration, compiled.

``ULB_UK_SEC`` is ``ULB_UK_S`` taught to run in force at a valuation date
(UKLIB-SEC-PLAN.md, milestone M9, after USLIB-SEC-PLAN.md's Phase 1), and then made to
compile under modelx-cython (milestone M10, after USLIB-SEC-PLAN.md's Phase 2).  It runs on two
clocks: ``t`` counts months from the valuation date, the same month for every model point,
and ``duration_mth(t)`` counts the months the bond has been in force,
``duration_mth_init() + t``.  A model point may be a bond already in force at the valuation
date, in any month of its policy year, one issued at it, or one to be issued after it, as
in ``basiclife/BasicTerm_SE``.  A bond in force opens with three columns of state beside
its count, each per policy and measured at the valuation instant: the unit fund,
``av_pp_init``; the withdrawals and adviser charges since issue, ``wd_cum_pp_init``, which
open the guaranteed minimum death benefit; and the 5% allowance accrued since issue,
``allowance_cum_pp_init``, which the excess gain is measured against.  Its frame ends at the limiting age or at
the first month its fund opens at or below ``depletion_threshold``, half a pence, where
``ULB_UK_S``'s ends at the first that opens on exactly 0 or less: a recorded departure,
whose effect on each S point ``test_the_depletion_threshold_moves_point_3_alone`` states.

The worked example is not restated here.  On a point issued at the valuation date the two
clocks coincide and the model is ``ULB_UK_S``, and ``test_model_conventions_uk.py``
asserts that cell by cell on the twins of S's six new-business points (T1), so every
golden of ``test_unit_linked_bond_uk.py`` on them holds on this model with no number
copied; on S's point 3, whose fund S closes on a rounding of 3.4e-15 and projects a month
more, over the months both frames run alike.  The conventions also hold the SEC family's
other rules: every frame opens at ``t = 0``, ``pols_if`` is the ``BEF_DECR`` count,
``BEF_DECR`` is ``BEF_NB`` plus the month's new business, new business enters once, and
nothing happens before issue.  This module holds the rest of the plan's tests (its §5)
and the product's own facts:

* T2, the splice: an S point restated in force at month ``d``, opened with the state S
  carries into ``d``, continues S's projection from ``d`` on, in every cell of S's.  The
  months straddle the product's events: the surrender bands' edges, policy year 21, where
  the allowance-exhaustion step starts, the allowance stops accruing and the GMDB of the
  anchor's pattern has run out, and each frame's last month.  Every switch that ships off
  is on, and four variants of S's points, in a copy of S's table, add the GMDB in the
  money, a custom withdrawal above the 7.5% cap, the rider beside an adviser charge, and
  the cap binding net of an adviser charge.
* T3, future new business: a point issued ``k`` months after the valuation date is S's
  projection ``k`` months on, with zeros before issue and no rate evaluated there.
* D11's R1 and R2, and D3's and D5's chains: on the splice's grid no cell is called at a
  negative month, none on the books reads a month before them, and none reads beyond
  ``t + 1`` but the exhaustion search R2 admits; on the committed points no recursion runs
  backward over the frame; the policy clock is a closed form; and each chain, called cold,
  runs one cell a month back to ``t_entry()``, at each shape's longest cover.
* T4, the count algebra: the count rolls forward through new business and decrements,
  multiplying ``policy_count`` by 2.5 with every switch that ships off switched on
  multiplies every flow and every counted cell by 2.5 and moves no per-policy value, each
  flow nonzero on some point, the rider charge among them; a point restated a month on,
  with the count it carries there, continues its own flows, so that each is weighted by the
  count in force; and the roll-forward, whose tolerance scales with the count, closes on a
  million policies.
* T5, validation: each malformed row of the table is refused as it is read, naming its
  point; each assumption table, malformed or holding a value that is not a number in its
  range, is refused before a value of it is read, and a read beyond the mortality table is
  refused naming the point; the future horizon is a Reference that bounds future business;
  a point past its cover, one the contract does not issue, one read under a Reference
  outside its domain and one whose fund is exhausted at the valuation date are refused by
  the frame, each bound just inside it and each domain at both its edges, and a surrender
  rate outside 0 to 1 in the month it leaves, where one of exactly 1 is accepted; the edges of the interface and of each bound are accepted; and so is every state
  ``ULB_UK_S`` reaches, on each set of inputs on which those states differ, but the
  exhausted fund it runs on past the threshold, which is set aside and shown refused.
* T6, regeneration: the committed ``model_point_table_sec.csv`` is what the generator makes
  of ``ULB_UK_S`` and its table as they stand.
* Then the product's own facts: the two clocks on the shipped points; the committed rows
  continuing their S points, and the one read from S under a fund return of its own
  holding the guarantee in the money and the rider charging; each history column read rather than recomputed, the unit
  fund, the withdrawals since issue, which open the GMDB, and the allowance accrued, which
  an allowance rate changed at the valuation date does not rewrite (UKLIB-SEC-PLAN.md
  K14); the
  depletion threshold, its effect on each S point, and its rules at the Reference's value,
  part of it and just past it; the fund chain written inline; expense inflation on the
  valuation clock; acquisition on new business alone; the cap on mortality and a NaN that
  reaches it; the values outside cover; the block; an in-force extract; the runner; the
  cells' defaulted parameters; the docstrings; the shared input tables; and what the
  default grid reaches.
* The C step's representation, in modelx: the claims total held to ``ULB_UK_S``'s by its
  bits, every decode on every value, the padded arrays, the vectors' dtypes, the labels'
  refusals, the chains blocked by policy year, and the spec's and the sample's comments.
* C2, the fingerprint: every committed point computes what the model computed when its E
  step ended, frozen at the end of this module before its C step changed anything
  (USLIB-SEC-PLAN.md §5.4).
* Compiled, after the fingerprint, the tests marked ``cython``: C4 on the splice grid, at
  the contract's extremes, where the cap binds, at the threshold's edges, on keys written
  as floats and on the committed row in the money, each with the model's ``also``, every
  code no swept cell reads, which a test holds to the codes each cell takes in modelx, row
  by row; the refusals and overflows, message for message; each shape's deepest cold call
  on a 1 MiB stack; a Reference set late; and the runner.

SEC month ``t`` is S month ``t + source_mth`` throughout, the direction in which
``uk_sec_support`` takes its ``t_offset``: ``d`` for a point restated at S month ``d``,
``-k`` for one issued ``k`` months on.

**The core grid and the full one** (UKLIB-SEC-PLAN.md U6).  T2 and T3 over every S point
at every month, about 130 cases, run by default on a core, chosen so that between them they
reach every branch, every opening-state column, every kind of valuation month and both
sides of every ``min`` and ``max`` the full grid reaches, which
``test_the_core_grid_reaches_every_branch`` asserts.  The other cases, and the rules
test's scan of their rows, carry the ``sec_full`` marker and are skipped, with the reason
shown, unless ``UKLIB_SEC_FULL=1`` is set.  They are never dropped: one leg of the CI
matrix sets it, and ``UKLIB_SEC_FULL=1 python -m pytest -m sec_full
lifelib/libraries/uklib/tests/test_unit_linked_bond_uk_sec.py`` runs them alone.  Each
splice row is released once it has been read (``_release``), as ``run_sec.py --block``
releases its points.

Every test keeps four rules.  Each model is read under a name of its own and closed:
``conftest.unit_linked_bond`` reads S under its default name, and reading a model under a
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
through the same helpers, unchanged; a call that spells a timing as text is ``ULB_UK_S``'s.
"""
import ast
import dataclasses
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
    compiled_case, compiled_mismatches, exact_here, labels_refusing_non_text,
    reporting_cells, run_compiled)
from uk_sec_support import _ULB_CODED, _LIVES, _ulb_c4_also
from uk_sec_support import generated_columns

SEC, TWIN = "ULB_UK_SEC", "ULB_UK_S"
TABLE = "model_point_table_sec.csv"
SPEC = SEC_SPECS[SEC]

# S's six new-business points: the anchor cell, a 5% withdrawal (1); the accumulation cell,
# no withdrawals (2); the anchor with a 0.5% adviser charge (3); the anchor with the GMDB
# rider (4); the anchor at a 101% death uplift (5); and a female 55, a larger premium and a
# 3% custom withdrawal (6).
S_POINTS = (1, 2, 3, 4, 5, 6)

# The depletion threshold as shipped (Projection.depletion_threshold), half a pence.
THRESHOLD = 0.005

# T2's months (UKLIB-SEC-PLAN.md §6.6): the second month; 11, 12, 23, 24, 59, 60, 119 and 120,
# either side of the surrender bands' edges, policy years 1 to 2, 2 to 3, 5 to 6 and 10 to
# 11, the first of which is also the first anniversary; 37 and 125, mid-band; 239, 240 and
# 241, either side of policy year 21, where the allowance-exhaustion step starts, the
# allowance stops accruing, the first excess gain of the anchor's pattern appears and the
# GMDB point's guarantee reaches 0; and each frame's last month, 322, 352, 659 and 779.  A
# month at or past a point's frame is left out.  T3's: issued one month on, which puts the
# policy anniversaries a month off the valuation years, and twelve, which puts them back on;
# and later, more than a year after the valuation date (USLIB-SEC-PLAN.md §7.1, *Record —
# M14*, *Splice grid*).
SPLICE_MTHS = (1, 11, 12, 23, 24, 37, 59, 60, 119, 120, 125, 239, 240, 241, 322, 352, 659,
               779)
FUTURE_MTHS = (1, 12)
LATE_FUTURES = ((4, 13), (6, 25))

# Four more S points, in the splice's copy of S's table and never in the committed one,
# each one of S's points changed so as to reach what S's own points cannot:
#
# 7, S point 4, the GMDB point, at an AMC of 4%: its fund falls faster than its guarantee,
#   which is in the money from month 5, so the rider charges and the guarantee pays on
#   death, where S's own GMDB point is in the money only in its issue month, on the death
#   strain;
# 8, S point 6, the custom pattern, at 9% a year: above the 7.5% product cap, which then
#   binds every month the fund can pay;
# 9, S point 3, the adviser charge, with the GMDB rider beside it: both of the charges that
#   leave the fund on a rounding where the withdrawal cap closes it;
# 10, S point 6 at 9% a year with an adviser charge of 0.5%: the 7.5% cap binding net of
#   the charge, which counts against the same limit, so that the withdrawal is the cap's
#   twelfth less the charge in every month but the last, which no other point reaches.
#
# Each variant is (the S point it changes, the columns it changes); the policy_id keeps
# the generated ids apart.
VARIANTS = {
    7: (4, {"policy_id": "ULB-900007", "amc_rate": 0.04}),
    8: (6, {"policy_id": "ULB-900008", "wd_rate_custom": 0.09}),
    9: (3, {"policy_id": "ULB-900009", "gmdb_flag": True}),
    10: (6, {"policy_id": "ULB-900010", "wd_rate_custom": 0.09, "oac_rate": 0.005}),
}
VARIANT_MTHS = {7: (1, 5, 6, 60, 120, 232), 8: (1, 12, 120, 200), 9: (12, 66, 322),
                10: (1, 60, 200)}

# Each point's frame from issue, in months, as this model ends it and as ULB_UK_S does.  Its
# fund runs out at 353 on the anchor's pattern, at 323 under the adviser charge, where S
# runs one month more on a rounding of 3.4e-15, at 233 on the GMDB in the money and at 201
# on the custom 9%, with or without the adviser charge, and never on the accumulation cell
# or the custom 3%, whose frames run to the limiting age.
# test_the_depletion_threshold_moves_point_3_alone holds both.
FRAME = {1: 353, 2: 660, 3: 323, 4: 353, 5: 353, 6: 780, 7: 233, 8: 201, 9: 323, 10: 201}
S_FRAME = {**FRAME, 3: 324, 9: 324}


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


# T2's cases, as (row_kind, S point, source_mth): each S point restated in force at each of
# its months inside its frame, then each variant at its own.  ULB_UK_S has no point in force,
# so no twin is a splice case.  T3's cases, as (S point, k).
SPLICES = (tuple(("derived", p, d) for p in S_POINTS for d in SPLICE_MTHS if d < FRAME[p])
           + tuple(("derived", p, d) for p, mths in VARIANT_MTHS.items() for d in mths))
IN_FORCE_TWINS = ()
FUTURES = (tuple((p, k) for p in S_POINTS for k in FUTURE_MTHS)
           + tuple((p, 1) for p in VARIANTS) + LATE_FUTURES)

# The default run's cases (the module docstring), each with what it is there for.  The
# rest of SPLICES and FUTURES run with UKLIB_SEC_FULL=1.
CORE_SPLICES = {
    ("derived", 1, 1): "the anchor cell in its second month",
    ("derived", 1, 11): "the anchor cell the month before its first anniversary",
    ("derived", 1, 12): "the anchor cell on its first anniversary: the 3% band",
    ("derived", 1, 59): "the last month of the 5% band",
    ("derived", 1, 60): "the first month of the 8% band",
    ("derived", 1, 120): "the first month of the ultimate 10% band",
    ("derived", 1, 239): "the last month of policy year 20",
    ("derived", 1, 240): "policy year 21: the step, the allowance spent",
    ("derived", 1, 241): "policy year 21 under way, an excess gain carried in",
    ("derived", 1, 352): "the last month before the fund is exhausted",
    ("derived", 2, 125): "the accumulation cell mid-band",
    ("derived", 2, 659): "the accumulation cell at the limiting age",
    ("derived", 3, 37): "the adviser charge mid-band, in its fourth year",
    ("derived", 3, 322): "the adviser charge's last month: S runs on past it",
    ("derived", 4, 23): "the GMDB in the month before its second anniversary",
    ("derived", 4, 24): "the GMDB on its second anniversary: the 5% band",
    ("derived", 4, 239): "the GMDB in the last month of its guarantee",
    ("derived", 4, 240): "the GMDB's guarantee run out",
    ("derived", 5, 119): "the 101% uplift in the last month of the 8% band",
    ("derived", 6, 12): "the custom 3%, female, on her first anniversary",
    ("derived", 6, 779): "the custom 3% at the limiting age",
    ("derived", 7, 1): "the GMDB out of the money, its fund falling faster",
    ("derived", 7, 6): "the GMDB in the money: the rider charges",
    ("derived", 7, 232): "the GMDB in the money in its last month",
    ("derived", 8, 1): "the 7.5% cap binding",
    ("derived", 8, 200): "the 7.5% cap's last month, the fund exhausted",
    ("derived", 9, 66): "the rider beside the adviser charge",
    ("derived", 9, 322): "the rider and the adviser charge's last month",
    ("derived", 10, 1): "the 7.5% cap binding net of the adviser charge",
}
CORE_FUTURES = {
    (1, 1): "issued a month off the valuation anniversaries",
    (1, 12): "issued on them, a year on",
    (3, 1): "the adviser charge, whose S frame runs on",
    (4, 13): "the GMDB, more than a year on",
    (6, 25): "the custom 3%, female, more than two years on",
    (7, 1): "the GMDB in the money",
    (8, 1): "the 7.5% cap binding",
}

SEC_FULL = os.environ.get("UKLIB_SEC_FULL") == "1"
FULL_ONLY = (pytest.mark.sec_full,
             pytest.mark.skipif(not SEC_FULL, reason="the full splice grid runs with "
                                "UKLIB_SEC_FULL=1 (UKLIB-SEC-PLAN.md U6)"))

# What the splice sets in both models, S and SEC alike, before either evaluates anything.
# Expense inflation is the one input ULB reads on the valuation clock (D7): S inflates from
# issue and SEC from the valuation date, so at the shipped 2.5% the expenses of a point
# opened at d differ by 1.025^(d // 12), by design, and at 0 both factors are 1.  The clock
# itself is then asserted on its own, at the shipped rate.  The fund return is a flat
# Reference, the same on both clocks, so no input moves with d.  The rest switch on what
# ships off, each of which hides some of the state from any comparison:
#   return_shock, at -0.75, a trailing return 75 points below the fund's, which takes the
#     performance multiplier past its cap of 2, so that the surrender rate is twice the
#     table's;
#   surr_rate_cap, lowered to 0.25, which the ultimate 10% at that multiple and the
#     allowance-exhaustion step's 1.5 then pass from policy year 21, so that the surrender
#     cap binds there and not before.
# The identity does not depend on the values, only on both models having the same ones.
SPLICED_REFS = {"inflation_rate": 0.0, "return_shock": -0.75, "surr_rate_cap": 0.25}

# The splice's switches, for T4, at the shipped inflation.
SWITCHED_ON = {ref: value for ref, value in SPLICED_REFS.items() if ref != "inflation_rate"}

# The cells T2 and T3 skip beyond T1's, which already drop S's av_init_pp, the accessor of
# the column this model renames (the spec's exempt).  proj_len counts from the valuation
# date on SEC and from issue on S, so it differs by d, or by -k, by design; the comparison
# asserts what it must get right, that both frames end at the same instant.
SPLICE_EXEMPT = TWIN_EXEMPT_DEFAULT | SPEC.exempt | {"proj_len"}
FUTURE_EXEMPT = SPLICE_EXEMPT

# The result_cf columns that expense inflation moves, and the cells they are made of: on
# the committed points, at the shipped 2.5%, the only places an in-force row departs from S.
INFLATED = ("expenses", "net_cf")
INFLATION_CELLS = frozenset({"inflation_factor", "expenses", "net_cf", "result_cf"})

# The cells whose exact value is 0 and whose computed value is rounding about it: the three
# residuals, and the excess gain where the withdrawals equal the allowance in exact
# arithmetic, at each policy year's end on the anchor's pattern, where S's value is a
# rounding of 1e-11.  A comparison with S holds them at the harness's absolute floor of
# 1e-9, and every other cell at none (_compare).  result_uf carries the excess gain, and is
# held with them.
RESIDUALS = frozenset({"check_av_roll_fwd_resid", "check_pols_roll_fwd_resid",
                       "check_unit_funding_resid", "excess_gain_pp", "result_uf"})
FLOOR = 1e-9

# The reports, which the comparison reads as frames rather than as cells.
REPORTS = ("result_cf", "result_uf")

# The decrement rates, the allowance step and the policy clock's year and age, none of
# which a report may evaluate before issue (R1, D4): a count asks whether the month is in
# cover before it reads a rate.  allowance_cum_pp is not among them: result_uf reads it at
# every month of the frame, and it guards itself, holding 0 before issue.
DECREMENT_RATES = ("mort_rate", "mort_rate_mth", "surr_rate_base", "surr_rate",
                   "surr_rate_mth", "allow_factor", "age", "duration", "policy_year")

# The cells that scale with policy_count.  Every other cell is a per-policy amount, a rate,
# a ratio, a clock or a flag, and must not move when the count does.
COUNTED = frozenset({
    "policy_count", "pols_if_init", "pols_if", "pols_if_at", "pols_if_py", "pols_new_biz",
    "pols_death", "pols_surr", "pols_maturity", "claims", "withdrawals", "unit_releases",
    "amc_charges", "gmdb_charges", "further_costs", "tax_provisions", "death_strain",
    "expenses", "net_cf", "check_pols_roll_fwd_resid", "check_unit_funding_resid",
    "result_cf", "result_pols"})

# result_pols' columns, in its order: the count, the new business within it, then the
# month's deaths and surrenders in processing order and the frame's last survivors.
RESULT_POLS = ["pols_if", "pols_new_biz", "pols_death", "pols_surr", "pols_maturity"]
OUTFLOWS = RESULT_POLS[2:]

# result_cf's per-policy column: the unit fund, which no count moves.
PER_POLICY_COLUMNS = ("av_pp",)

# S's three timings and BEF_NB, the one running in force adds; the fund's four; and the
# kinds.
TIMINGS = ("BEF_NB", "BEF_DECR", "BEF_SURR", "AFT_DECR")
FUND_TIMINGS = ("BEF_GROWTH", "AFT_GROWTH", "AFT_CHARGE", "AFT_WD")
KINDS = ("DEATH", "SURRENDER")

# What each cell holds outside cover, before issue and from the limiting age, as its
# docstring says: no count, so no cash flow; no fund, no charge and no withdrawal; no rate
# read at a policy year or an age the bond does not have.  The type is part of the value.
# A count is a float in every branch and a flag a bool, because the C step types a cell by
# the values it returns (USLIB-SEC-PLAN.md F3).  The guard test also calls pols_if_at at
# each timing, av_pp_at at each of the fund's and claims at each kind, all 0.0.
OUTSIDE_COVER = {
    "is_active": False, "av_pp": 0.0, "av_per_segment_pp": 0.0, "fund_growth_pp": 0.0,
    "tax_provision_pp": 0.0, "amc_pp": 0.0, "further_costs_pp": 0.0, "wd_cap_pp": 0.0,
    "wd_pp": 0.0, "adviser_charge_pp": 0.0, "gmdb_guarantee_pp": 0.0,
    "gmdb_charge_pp": 0.0, "death_strain_pp": 0.0, "wd_cum_pp": 0.0,
    "allowance_cum_pp": 0.0, "excess_gain_pp": 0.0, "mort_rate": 0.0,
    "surr_rate_base": 0.0, "allow_factor": 0.0, "surr_rate": 0.0,
    "pols_if": 0.0, "pols_new_biz": 0.0, "pols_death": 0.0, "pols_surr": 0.0,
    "pols_maturity": 0.0, "withdrawals": 0.0, "unit_releases": 0.0, "amc_charges": 0.0,
    "gmdb_charges": 0.0, "further_costs": 0.0, "tax_provisions": 0.0, "death_strain": 0.0,
    "expenses": 0.0, "net_cf": 0.0}

# The counts and the cash flows: what a month after an exhausted fund holds, the frame
# having ended there while the bond is still short of the limiting age, and so in cover.
FRAME_CELLS = ("pols_if", "pols_new_biz", "pols_death", "pols_surr", "pols_maturity",
               "withdrawals", "unit_releases", "amc_charges", "gmdb_charges",
               "further_costs", "tax_provisions", "death_strain", "expenses", "net_cf")

# The cells a month outside cover may not reach: the clocks of the contract and the
# monthly rates, each keyed by a policy year or an attained age.  The reads that guard
# themselves are held by their values in OUTSIDE_COVER instead.
IN_COVER_ONLY = ("age", "duration", "policy_year", "mort_rate_mth", "surr_rate_mth")

# The opening state, in the table's order, and the cells running in force adds to
# ULB_UK_S's, each of which the symbol map must name.
STATE = ("av_pp_init", "wd_cum_pp_init", "allowance_cum_pp_init")
NEW_CELLS = ("policy_count", "duration_mth_init", "t_entry", "is_active", "pols_new_biz",
             *STATE, "result_pols", "point_id", "mort_schedule", "wd_pattern_code",
             "av_pp_py", "wd_cum_pp_py", "pols_if_py", "av_pp_grown_refusal")

INFLATION = 0.025       # the shipped inflation_rate, which the inflation test reads

# The recursion limit, as mx.set_recursion takes it, under which the committed points are
# first swept (R2, F7).  A report asks for the frame first, which searches the fund in
# ascending t, and evaluates each column in ascending t, so a forward recursion, through
# t - 1, finds the month before already cached: the committed points' sweep runs 16 cells
# deep at most, and passes under a limit of 16 (measured at M9).  A backward recursion over
# the frame, through t + 1, opens a chain as long as the frame, and the shortest committed
# frame longer than a month is 113.
CALL_DEPTH = 40

# The reads beyond t + 1 the model makes, as (reader, cell read): fund_exhaust_mth's search
# of the unit fund, the loop R2 admits, which every count reads through proj_len() (the
# rules test follows calls keyed by no month), at months up to the frame's end, the first
# month whose fund is exhausted.  The rules test admits no other.
LOOK_AHEAD = frozenset({("fund_exhaust_mth", "av_pp")})


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
                       model_point_file=TABLE, edits=edits)


def _read_edited(tmp_path, edit, edits=None):
    """ULB_UK_SEC read from a copy whose SEC table is ``edit(_committed())``."""
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
    """Evaluate on an S point what the splice compares: the sweep, and the cells it misses.

    :func:`uk_sec_support.sweep` reaches ``ULB_UK_S``'s ``pols_if_at(t, "BEF_DECR")`` and
    ``av_pp_at(t, "BEF_GROWTH")`` nowhere, nor ``duration_mth``, ``av_per_segment_pp`` or
    ``lives``, which no formula of S reads; a cell S never evaluates is compared nowhere.
    They are evaluated here over the frame, so the splice and the future comparison see
    them too.
    """
    sweep(proj)
    proj.lives()
    for t in range(proj.proj_len()):
        proj.pols_if_at(t, "BEF_DECR")
        proj.av_pp_at(t, "BEF_GROWTH")
        proj.duration_mth(t)
        proj.av_per_segment_pp(t)


def _from(last):
    """An ``arg_map`` that skips every S key at month ``last`` or later, the ``t`` of a
    cell's arguments; keys without a ``t`` pass."""
    def mapped(name, args, last=last):
        return None if args and _month(args[0]) and args[0] >= last else args
    return mapped


def _only(month, skip=()):
    """An ``arg_map`` that keeps the S keys at ``month`` alone, but those of ``skip``,
    ``(name, args)`` pairs."""
    def mapped(name, args, month=month):
        if not (args and _month(args[0]) and args[0] == month):
            return None
        return None if (name, args) in skip else args
    return mapped


def _departure(s_proj, sec_proj, month):
    """What the depletion threshold changes where S runs on past the SEC frame (§6.6).

    The SEC frame ends at the first month whose fund opens at or below
    ``depletion_threshold``, and S's at the first that opens on 0 or less.  So where S
    projects months past the SEC frame, the first of them opens on a fund above 0 and at or
    below the threshold, a rounding the withdrawal cap closed the month before on; the SEC
    frame's survivors leave in its last month, where S's carry on; and nothing else in that
    month moves.  The mismatch lines, empty when the row is so.
    """
    end = sec_proj.proj_len()
    last = end - 1
    found = []
    opened = s_proj.av_pp(month + end)
    if not 0.0 < opened <= sec_proj.depletion_threshold:
        found.append(f"S's run-on month {month + end} opens on {opened!r}, which is not "
                     f"above 0 and at or below depletion_threshold, "
                     f"{sec_proj.depletion_threshold}")
    if sec_proj.fund_exhaust_mth() != sec_proj.duration_mth(end):
        found.append(f"fund_exhaust_mth() is {sec_proj.fund_exhaust_mth()}, not the policy "
                     f"month of t = {end}, {sec_proj.duration_mth(end)}")
    survivors = s_proj.pols_if_at(month + last, "AFT_DECR")
    left = sec_proj.pols_maturity(last)
    if not math.isclose(left, survivors, rel_tol=1e-9, abs_tol=0.0):
        found.append(f"pols_maturity({last}) is {left!r}, not S's survivors "
                     f"pols_if_at({month + last}, 'AFT_DECR'), {survivors!r}")
    aft = sec_proj.pols_if_at(last, _code(sec_proj, "AFT_DECR"))
    if aft != 0.0 or s_proj.pols_maturity(month + last) != 0.0:
        found.append(f"in the SEC frame's last month the count carries {aft!r} on, and S "
                     f"matures {s_proj.pols_maturity(month + last)!r}: both must be 0")
    return found


def _mismatches(s_proj, sec_proj, *, arg_map=None, **kwargs):
    """:func:`uk_sec_support.twin_mismatches` of an S point and an SEC row, the one place
    this module compares them so.

    It passes the SEC Space's :func:`uk_sec_support.codes`, which map S's timing and kind
    strings to the int codes the C step gives them, and the spec's ``twin_arg_map``, which
    maps S's ``claims(t, None)``, its total, onto SEC's ``ALL`` and passes SEC's own keys
    unchanged, composed before ``arg_map``, the comparison's own cut of S's keys, as FIA's
    module composes them (USLIB-SEC-PLAN.md §7.1, *Record -- M14*, *Carried into Phase 1*;
    §7.11, *Record -- M21*).  Every comparison of a row with S goes through here, so each
    takes the C step's codes and map.
    """
    def mapped(name, args):
        args = SPEC.twin_arg_map(name, args)
        return args if arg_map is None or args is None else arg_map(name, args)

    return twin_mismatches(s_proj, sec_proj, codes=codes(sec_proj), arg_map=mapped,
                           **kwargs)


def _compare(s_proj, sec_proj, month, exempt, columns=None):
    """Where SEC's row departs from S's point from S month ``month`` on.

    First the frames, ``result_cf`` (over ``columns``, or every column both hold) and
    ``result_uf``, SEC row ``t`` against S row ``t + month``, frames ending together; then
    every cell of S's but ``exempt``, :data:`REPORTS` and :data:`RESIDUALS`, at every
    argument S cached inside its frame from ``month`` on, moved onto SEC's clock.  Both to
    1e-9 relative with no absolute floor (USLIB-SEC-PLAN.md §5.2, T2, precised at M11): a
    floor of 1e-9 passes an error of 1% in any value below 1e-7, and the counts late in a
    long frame, under the splice's switches, fall below 1e-12.  Then the cells of
    :data:`RESIDUALS`, and ``result_uf``, which shows the excess gain, at the floor of
    1e-9: their exact value is 0, and the computed one moves by an ulp of what it closes
    when an opening state comes back from the CSV one ulp off; every other value
    ``result_uf`` shows is a cell held at no floor.

    Two departures are by design, and taken as such.  Where the frame ends because the fund
    is exhausted, its last month closes the fund on a subtraction whose exact value is 0,
    and whose computed value, 0 or a rounding of either sign floored at 0, turns on the
    fund's last bit, which a fund read back from the CSV may hold otherwise: that month is
    compared at the floor (VA's ``_residue_months``, USLIB-SEC-PLAN.md §7.7, *Record —
    M9*).  And where S's frame runs past SEC's, on a rounding at or below
    ``depletion_threshold``, the months the two run alike are compared so, S's months past
    the SEC frame are not, the count's exit in the SEC frame's last month is held to S's
    survivors, and the rest of the departure is :func:`_departure`'s.  Returns the
    mismatch lines, empty when the row is S's.
    """
    end = sec_proj.proj_len()
    s_end = s_proj.proj_len() - month
    if s_end < end:
        return [f"the SEC frame runs past S's: S's ends at t = {s_end - 1} on SEC's clock, "
                f"SEC's at t = {end - 1}"]
    cut = s_end > end
    last = end - 1
    exhausted = sec_proj.fund_exhaust_mth() <= sec_proj.horizon_mths()
    found = _departure(s_proj, sec_proj, month) if cut else []
    for report in REPORTS:
        keep = columns if report == "result_cf" else None
        floor = FLOOR if report in RESIDUALS else 0.0
        s_df = s_proj.cells[report]().loc[: month + last]
        sec_df = sec_proj.cells[report]()
        if exhausted:
            if last > 0 and len(s_df.loc[month: month + last - 1]):
                found += [f"{report}: {line}" for line in frame_mismatches(
                    s_df.loc[: month + last - 1], sec_df.loc[: last - 1], t_offset=month,
                    columns=keep, atol=floor)]
            found += [f"{report}, its last month: {line}" for line in frame_mismatches(
                s_df.loc[month + last:], sec_df.loc[last:], t_offset=month, columns=keep,
                atol=FLOOR)]
        else:
            found += [f"{report}: {line}" for line in frame_mismatches(
                s_df, sec_df, t_offset=month, columns=keep, atol=floor)]
    others = exempt | set(REPORTS) | ({"fund_exhaust_mth"} if cut else set())
    head = _from(month + last) if exhausted else None
    found += _mismatches(s_proj, sec_proj, t_offset=month, exempt=others | RESIDUALS,
                         arg_map=head, atol=0.0)
    found += _mismatches(s_proj, sec_proj, t_offset=month,
                         exempt=others | (set(s_proj.cells) - RESIDUALS), arg_map=head)
    if exhausted:
        exits = {("pols_if_at", (month + last, "AFT_DECR")),
                 ("pols_maturity", (month + last,))} if cut else set()
        found += [f"its last month: {line}" for line in _mismatches(
            s_proj, sec_proj, t_offset=month, exempt=others,
            arg_map=_only(month + last, exits))]
    return found


def _continues_s(s_proj, sec_proj, month):
    """Where a committed row departs from S's point ``s_proj`` from S month ``month`` on.

    The splice's comparison (:func:`_compare`), on the committed model at the shipped
    assumptions.  The shipped 2.5% expense inflation runs from issue in S and from the
    valuation date here (D7), so :data:`INFLATED`'s two columns, and
    :data:`INFLATION_CELLS`, differ by design and are left out; the inflation test holds
    them.  Every other column and cell must agree, to 1e-9 relative, with no absolute floor
    but on the residuals and in an exhausted frame's last month.
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
    """ULB_UK_SEC read in place, as committed, and swept once, cold; what it met.

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
    """ULB_UK_SEC read in place, as committed, with every point swept (sec_read)."""
    return sec_read[0]


@pytest.fixture(scope="module")
def s_model():
    """ULB_UK_S read in place, as committed, with every point swept.

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
    selects, the core or the full grid (:func:`_selected`), out of this S model, so each row
    opens with the state of the very run it is compared with.  No input table moves with
    ``d``: ULB's one valuation-clock input is the ``inflation_rate`` Reference.  Every S
    point is then swept (:func:`_sweep_s`), and stays swept; each SEC row is projected by
    the case that compares it and released once compared (:func:`_settle`).
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
                               future=tuple(_selected(FUTURES, CORE_FUTURES)),
                               derived_refs={})
    table, companions = build_sec_table(spec, s)
    assert companions == {}
    sec_folder = _sec_inputs(root / "sec", table)
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
    month, such as ``proj_len()`` and the ``fund_exhaust_mth()`` it reads, as far as the
    dependency graph goes, each with the call keyed by no month that reads it: so a read
    that looks ahead through a cell taking no ``t`` is the reader's, and the reader names
    the loop that makes it (USLIB-SEC-PLAN.md §5.2, T2, precised at M12; ``DIA_US_SEC``'s
    form).  ``reach`` holds what each call keyed by no month reads, so that each is walked
    once a row, and the walk is a loop, not a recursion.
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


def _rule_breaches(proj):
    """R1 and R2's look-ahead on one row, once it has run whole.

    The row's reports and checks are run (:func:`uk_sec_support.sweep`), and then every
    monthly cell at every month of the frame and the month after it, as the C step's sweep
    runs them (:func:`uk_sec_support.full_sweep`): no report of a row need read every
    state, and a base at ``t == 0`` would hide in a cell the reports leave unread
    (USLIB-SEC-PLAN.md §5.2, T2, precised at M4).  ``{"negative": [...], "early": [...],
    "ahead": [...], "raised": [...]}``: every cached call with a negative argument; every
    call keyed by a month before ``t_entry()`` that a call keyed by a month at or after it
    reads; every call keyed by a month beyond ``t + 1`` that a call keyed by ``t`` reads, but
    :data:`LOOK_AHEAD`'s, at months up to ``proj_len()``; and every call the full sweep found
    raising.  A call reads its precedents, as modelx's dependency graph records them, and,
    through a precedent keyed by no month, whatever that precedent reads in turn
    (:func:`_months_read`): every count reads the frame, ``proj_len()``, which reads
    ``fund_exhaust_mth()``, whose search reads the fund to the frame's end.
    """
    sweep(proj)
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
    return {"negative": negative, "early": early, "ahead": ahead, "raised": raised}


def _excess(x, t):
    """The withdrawals since issue less the allowance accrued in month ``t``, the excess
    gain's max's argument."""
    return x.wd_cum_pp(t) - x.allowance_cum_pp(t)


def _scheduled(x):
    """The month's scheduled withdrawal, before either cap."""
    return x.wd_rate() * x.premium() / 12.0


# What test_the_core_grid_reaches_every_branch asks of the core's rows in the model's own
# values, which no column of the table shows: each holds of some core row, or of a core row
# in some month of its frame.  At the valuation date, each opening-state column in use, the
# withdrawals since issue past the premium, so that the GMDB opens at 0, and short of it,
# the GMDB in the money and out of it, and an excess gain carried in.  Later in the frame,
# every branch and both sides of each min and max the full grid reaches: the withdrawal's
# three bounds, the cap net of an adviser charge, the cap's two bases, the GMDB in and out of the money on its charge and on
# its death benefit, the fund closed on 0 and on a rounding, the excess gain, the
# surrender table's last year, the surrender cap, the allowance step, the allowance's
# twenty years, and the frame's two ends.
AT_VALUATION = {
    "a fund carried in": lambda x: x.duration_mth_init() > 0 and x.av_pp_init() > 0.0,
    "withdrawals carried in": lambda x: x.wd_cum_pp_init() > 0.0,
    "an allowance carried in": lambda x: x.allowance_cum_pp_init() > 0.0,
    "the GMDB opened from what is left of it": lambda x: (
        x.gmdb_flag() and x.duration_mth_init() > 0 and x.gmdb_guarantee_pp(0) > 0.0),
    "the GMDB opened at 0, all drawn": lambda x: (
        x.gmdb_flag() and x.duration_mth_init() > 0 and x.gmdb_guarantee_pp(0) == 0.0),
    "an excess gain carried in": lambda x: (
        x.duration_mth_init() > 0 and x.wd_cum_pp_init() > x.allowance_cum_pp(0)),
    "the GMDB in the money at t = 0": lambda x: (
        x.gmdb_flag() and x.gmdb_charge_pp(x.t_entry()) > 0.0),
}
IN_FRAME = {
    "the scheduled withdrawal paid": lambda x, t: (
        x.wd_pp(t) > 0.0 and x.wd_pp(t) == _scheduled(x)),
    "the 7.5% cap binding": lambda x, t: (
        x.wd_pp(t) < _scheduled(x) and x.wd_pp(t) == max(
            0.0, x.wd_cap_pp(t) / 12.0 - x.adviser_charge_pp(t))
        and x.wd_pp(t) < x.av_pp_at(t, _code(x, "AFT_CHARGE")) - x.adviser_charge_pp(t)
        - x.gmdb_charge_pp(t)),
    "the 7.5% cap binding net of an adviser charge": lambda x, t: (
        x.adviser_charge_pp(t) > 0.0
        and 0.0 < x.wd_pp(t) == x.wd_cap_pp(t) / 12.0 - x.adviser_charge_pp(t)
        and x.wd_pp(t) < _scheduled(x)
        and x.wd_pp(t) < x.av_pp_at(t, _code(x, "AFT_CHARGE")) - x.adviser_charge_pp(t)
        - x.gmdb_charge_pp(t)),
    "the fund drawn to nothing": lambda x, t: (
        _scheduled(x) > 0.0 and x.wd_pp(t) < _scheduled(x)
        and x.av_pp_at(t, _code(x, "AFT_WD")) <= x.depletion_threshold),
    "the cap on the fund": lambda x, t: x.av_pp_at(t, _code(x, "AFT_CHARGE")) > x.premium(),
    "the cap on the premium": lambda x, t: (
        x.is_active(t) and x.av_pp_at(t, _code(x, "AFT_CHARGE")) < x.premium()),
    "the GMDB charge in the money": lambda x, t: x.gmdb_charge_pp(t) > 0.0,
    "the GMDB charge out of the money": lambda x, t: (
        x.gmdb_flag() and x.is_active(t) and x.gmdb_guarantee_pp(t) > 0.0
        and x.gmdb_charge_pp(t) == 0.0),
    "the GMDB paying on death": lambda x, t: (
        x.gmdb_flag()
        and x.gmdb_guarantee_pp(t) > x.db_uplift() * x.av_pp_at(t, _code(x, "AFT_WD"))
        and x.pols_death(t) > 0.0),
    "the fund closed on 0": lambda x, t: (
        t == x.proj_len() - 1 and x.av_pp_at(t, _code(x, "AFT_WD")) == 0.0
        and x.fund_exhaust_mth() <= x.horizon_mths()),
    "the fund closed on a rounding": lambda x, t: (
        t == x.proj_len() - 1
        and 0.0 < x.av_pp_at(t, _code(x, "AFT_WD")) <= x.depletion_threshold),
    "an excess gain": lambda x, t: _excess(x, t) > 0.0,
    "no excess gain": lambda x, t: x.is_active(t) and _excess(x, t) < 0.0,
    "inside the surrender table": lambda x, t: (
        x.is_active(t) and x.policy_year(t) <= x.data.surr_last_year()),
    "past the surrender table's last year": lambda x, t: (
        x.is_active(t) and x.policy_year(t) > x.data.surr_last_year()),
    "the surrender cap binding": lambda x, t: (
        x.is_active(t) and x.surr_rate(t) == x.surr_rate_cap
        < x.surr_rate_base(t) * x.perf_factor(t) * x.allow_factor(t)),
    "the surrender cap not binding": lambda x, t: (
        x.is_active(t) and x.surr_rate(t) < x.surr_rate_cap),
    "the allowance-exhaustion step": lambda x, t: (
        x.is_active(t) and x.allow_factor(t) == x.allow_step),
    "before the step": lambda x, t: x.is_active(t) and x.allow_factor(t) == 1.0,
    "the allowance accruing": lambda x, t: (
        x.is_active(t) and x.policy_year(t) < x.allowance_years),
    "the allowance spent": lambda x, t: (
        x.is_active(t) and x.policy_year(t) > x.allowance_years),
    "the frame ending at exhaustion": lambda x, t: (
        x.pols_maturity(t) > 0.0 and x.fund_exhaust_mth() <= x.horizon_mths()),
    "the frame ending at the limiting age": lambda x, t: (
        x.pols_maturity(t) > 0.0 and x.fund_exhaust_mth() > x.horizon_mths()),
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
    ``result_cf`` and ``result_uf``, and fail frames that end apart.  The cell comparison
    then evaluates every cell of S's but :data:`SPLICE_EXEMPT`, at every argument S cached
    inside its own frame from month ``d`` on, moved onto SEC's clock: the counts, the fund
    at each of its timings, the withdrawals since issue, the GMDB, the allowance and the
    excess gain among them.  Each compares to 1e-9 relative with no absolute floor, but the
    residuals and an exhausted frame's last month, which keep the floor of 1e-9, and on the
    adviser charge's rows S's month past the SEC frame, which the depletion threshold drops
    (:func:`_compare`).  An S cell this model lacked would fail it.

    The months about policy year 21 are the ones that see the withdrawals since issue read
    at the wrong instant: the GMDB of the anchor's pattern runs out there, and the excess
    gain first appears.  The row is then recorded for the rules test and released
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

    SEC rows ``k ..`` are S rows ``0 ..``, ending together where the fund is exhausted or
    at the limiting age, in ``result_cf`` and ``result_uf``, and every cell of S's but
    :data:`FUTURE_EXEMPT` agrees at every argument S cached inside its own frame, moved
    ``k`` later.  Each compares as the splice compares, with no absolute floor but on the
    residuals and in an exhausted frame's last month (:func:`_compare`).  An S cell this
    model lacked would fail it.  Before issue every column of ``result_cf``, ``result_uf``
    and ``result_pols`` is an exact zero, and the policies arrive in month ``k`` as new
    business.

    The last assertions are R1 and D4's base rule made testable.  After the reports, no
    decrement rate or read keyed by a policy year or an age has been evaluated at a month
    before issue.  A count recursion based at ``t == 0`` rather than at ``t_entry()``, or a
    decrement count that evaluates its rate before asking whether the month is in cover,
    still gives the right numbers.  And the frame is searched from issue: searched from
    ``t = 0``, the empty fund before issue would end it there.

    The pre-issue rows are asserted present before they are asserted zero, in every report:
    a frame that opened at issue would have none, its zeros would hold of nothing, and the
    comparisons with S, which start at issue, would not see it.  The row is then recorded
    for the rules test and released (:func:`_settle`).
    """
    s, sec = spliced
    key = _row_key(sec, "future", s_point, -k)
    s_proj, sec_proj = _point(s, s_point), projection(sec, key)
    try:
        frames = {name: sec_proj.cells[name]() for name in (*REPORTS, "result_pols")}
        assert _compare(s_proj, sec_proj, -k, FUTURE_EXEMPT) == []
        for report, frame in frames.items():
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
      on a point in force past it.
    * R1's look-back stops at ``t_entry()``: no cell evaluated at a month from
      ``t_entry()`` on read a month before it, directly or through a cell keyed by no
      month.  On a point issued later a recursion based at ``t == 0``, or the exhaustion
      search started there, reads the pre-issue zeros, so no number need show it and no
      argument goes negative.
    * R2's look-ahead: no cell evaluated at month ``t`` read a cell keyed by a month beyond
      ``t + 1``, as modelx's dependency graph records each cached call's precedents and
      through every precedent keyed by no month, but the loop R2 admits: the exhaustion
      search, ``fund_exhaust_mth()``, which reads the fund to the frame's end and which
      every count reads through ``proj_len()`` (:data:`LOOK_AHEAD`), at months up to
      ``proj_len()``, the first whose fund is exhausted.
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


def test_the_exhaustion_search_is_the_one_far_read_and_stays_in_the_frame(sec_model):
    """The exhaustion search, R2's admitted loop, reads the fund from issue to the frame's
    end, and nothing else reads ahead.

    :data:`LOOK_AHEAD` admits one reader and one cell, and the rules test above holds every
    other read to ``t + 1``; this holds what the admitted one reads, on every committed
    point: of the cells keyed by a month, ``fund_exhaust_mth()`` has read ``av_pp`` alone,
    as modelx's dependency graph records it, and at exactly the months from ``t_entry()``
    to the frame's end, ``proj_len()`` itself where the fund is exhausted there, and the
    frame's last month where the frame ends at the limiting age.  A search from ``t = 0``
    reads the months before a later issue, and one past the frame reads months no report
    reads (§6.6).
    """
    table = sec_model.Data.model_point_table()
    for key, point_id in zip(point_keys(sec_model), table.index):
        p = projection(sec_model, key)
        monthly = [pred for pred in p.cells["fund_exhaust_mth"].preds()
                   if _month_of(pred) is not None]
        assert {pred.obj.name for pred in monthly} == {"av_pp"}, point_id
        read = sorted(pred.args[0] for pred in monthly)
        exhausted = p.fund_exhaust_mth() <= p.horizon_mths()
        end = p.proj_len() if exhausted else p.proj_len() - 1
        assert read == list(range(p.t_entry(), end + 1)), (point_id, read[:3], read[-3:])


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


# How deep a cold call may run beyond its chain (D5, as blocked at M10): one cell a month
# from its month back to its policy year's first month, or to t_entry() in the year that
# holds it, and two cells a year before that, the year's opening and the month that opens
# the year before, back to t_entry()'s year (_chain).  Beyond it, the cells above the chain
# and those below it, the first month's rates, the year walks' own steps at the bottom and
# Data's first reads of its tables.  Each chain head called cold alone, before anything
# else on a read of its own, runs at most 16 cells beyond its chain, the unit-funding
# residual on the GMDB's shape, the rider's cover to the limiting age, the deepest call a
# projection makes, 231 cells on 215 at omega_age 121 and 229 on 213 at the shipped 120
# (measured at M10; at M9, one cell a month, 12 beyond 1,224).  Term's 16, as for uslib's
# Term (USLIB-SEC-PLAN.md D5), and met exactly: the year walk's own steps at the chain's
# foot take the 12 beyond of one cell a month to 16, so a product copying the walk
# measures its own overhead rather than copy this one.  A chain left one cell a month runs
# some 1,000 levels beyond at the longest cover, and one of two cells a month a frame's
# length; ULB_UK_S's fund runs four, about 5,400 levels (UKLIB-SEC-PLAN.md §6.6).
CHAIN_OVERHEAD = 16

# The contract's longest cover (product-spec.md, held by proj_len()): a bond issued at
# issue_age_min, 18, the youngest the mortality table rates, whose fund lasts to the
# largest limiting age the contract allows, omega_age_max, 121, the shipped table's last
# age plus one: 1,236 months from issue.  LONGEST_REFS sets omega_age there, beside the
# switches that ship off, for each test of the longest cover.
YOUNGEST = 18
OMEGA_MAX = 121
LONGEST_REFS = {**SWITCHED_ON, "omega_age": OMEGA_MAX}

# Each shape and the chains it runs, called cold in the last month of the frame at its own
# longest cover, each on a read of its own: (the S point whose twin it is, its frame from
# issue at YOUNGEST, the chain heads, each a (cell, the timing it takes, or None)).  The
# accumulation cell, no withdrawals, runs to the limiting age; the custom 3% withdraws to
# policy month 1,176, where its fund runs out at that age; the GMDB point withdraws 5% to
# month 353, its guarantee reading the withdrawals' chain; the adviser charge to 323; and
# the GMDB point with no withdrawals keeps the rider to the limiting age, 1,236 months, its
# death strain and its claims reading the guarantee's chain every month.  Each is issued now
# and future_horizon_mth, 120 months, on; the last entry is the columns a shape changes in
# its S point's twin.
CHAIN_HEADS = (("net_cf", None), ("av_pp", None), ("av_pp_at", "AFT_WD"),
               ("pols_if_at", "BEF_NB"), ("wd_cum_pp", None), ("excess_gain_pp", None),
               ("check_pols_roll_fwd_resid", None))
GMDB_HEADS = (("net_cf", None), ("check_unit_funding_resid", None), ("death_strain", None),
              ("gmdb_guarantee_pp", None), ("claims", "DEATH"), ("gmdb_charges", None))
SHAPES = ((2, 1236, CHAIN_HEADS, {}), (6, 1176, CHAIN_HEADS, {}),
          (4, 353, CHAIN_HEADS + (("gmdb_guarantee_pp", None), ("claims", "DEATH")), {}),
          (3, 323, CHAIN_HEADS, {}),
          (4, 1236, GMDB_HEADS, {"wd_pattern": "none"}))


def _chain(p, t):
    """The cells a cold read of month ``t`` of ``p`` runs through, past the first: one a
    month back to its policy year's first month, or to ``t_entry()`` in the year that holds
    it, and two a policy year before that, back to ``t_entry()``'s year, where the fund, the
    withdrawals since issue and the count are blocked by policy year (``av_pp_py``,
    ``wd_cum_pp_py``, ``pols_if_py``)."""
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


def _longest_cover(tmp_path):
    """A copy whose table holds each of :data:`SHAPES` at its longest cover: the twin of
    its S point issued at :data:`YOUNGEST`, now and 120 months on, the shipped
    ``future_horizon_mth``, each frame as it runs under :data:`LONGEST_REFS`.
    ``(folder, [(label, frame, t_entry, heads)])``."""
    committed = _committed()
    rows, frames = [], []
    top = committed.index.max()
    for s_point, months, heads, changes in SHAPES:
        twin = _label(committed, "twin", s_point, 0)
        for k in (0, 120):
            top += 1
            row = committed.loc[[twin]].assign(age_at_entry=YOUNGEST, duration_mth=-k,
                                               **changes)
            row.index = pd.Index([top], name="point_id")
            rows.append(row)
            frames.append((top, months + k, k, heads))
    return _sec_inputs(tmp_path, pd.concat(rows)), frames


# modelx warns as its stack trace starts and stops, which is all the test does with it.
@pytest.mark.filterwarnings("ignore:call stack trace:UserWarning")
def test_every_chain_runs_one_cell_a_month_from_a_cold_start(tmp_path):
    """Called cold, each chain runs one cell a month within its policy year, and two cells a
    year before it, back to ``t_entry()``, no more (D5, as blocked at M10).

    No number shows how deep a chain runs, and a compiled model runs it on the C stack, so
    a chain of two cells a month, which gives the same numbers, needs twice the stack on
    every platform (F7); ``ULB_UK_S``'s fund chain runs four cells a month, through
    ``av_pp_at`` at three timings, and its count three.  One cell a month, this model's ran
    1,236 cells at the longest cover at the shipped limiting age, 1,224 months, and compiled
    the count's needed 288 KiB of C stack, the fund's 252, past what the C step allows
    (UKLIB-SEC-PLAN.md §6.6, *Record -- M10*).  So the fund, the withdrawals since issue and the count are blocked by policy
    year, each year's opening a cell that walks the year before in ascending order
    (``av_pp_py``, ``wd_cum_pp_py``, ``pols_if_py``).  On a model just read, nothing is
    cached, so modelx's stack trace counts how deep a call runs, against that chain
    (:func:`_chain`) and :data:`CHAIN_OVERHEAD` more, with modelx's recursion limit where the
    module leaves it: each chain head of each of :data:`SHAPES`, in the last month of the
    frame, each on a read of its own and called first, since ``proj_len()`` searches the
    fund in ascending ``t`` and would leave it cached, with :data:`LONGEST_REFS` set.  At
    each shape's longest cover, issued at 18, the youngest the table rates, now and 120
    months on, the limiting age at the contract's largest, 121 (:func:`_longest_cover`);
    each row's frame is asserted after.  A chain left one cell a
    month runs about a thousand cells past the bound, and one walked descending the same.
    """
    folder, frames = _longest_cover(tmp_path)
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
                assert (p.proj_len(), p.t_entry()) == (months, entry), label
                chain = _chain(p, last)
                if not chain <= depth <= chain + CHAIN_OVERHEAD:
                    found.append(f"point {label}: {cell}{args} cold runs {depth} cells "
                                 f"deep, where its chain back to t_entry() {entry}, one "
                                 f"cell a month within its policy year and two a year "
                                 f"before it, is {chain} and {CHAIN_OVERHEAD} more are "
                                 f"allowed")
            finally:
                fresh.close()
    assert not found, found


def test_the_fund_chain_is_written_inline_and_av_pp_at_reads_it(sec_model):
    """``av_pp`` writes the month before's steps inline within a policy year, opens each
    year from the year before's walk, and ``av_pp_at`` reads it (§6.6, *Record -- M10*).

    The fund's chain of calls is one cell a month within a policy year, the depth test
    above shows, because ``av_pp(t)`` reads ``av_pp(t - 1)`` and computes the month
    before's growth, tax provision, charges and cancellations itself, where ``ULB_UK_S``
    reads ``av_pp_at(t - 1, "AFT_WD")`` through three timings; and in a year's first month
    after ``t_entry()`` it reads the year's opening, ``av_pp_py(y)``, which walks the year
    before.  So the forms must give one fund: on every committed point, in every month whose
    next is in cover, ``av_pp_at(t, AFT_WD)``, computed from that month's own fund, is
    ``av_pp(t + 1)`` bit for bit, a year's opening among them, and ``BEF_GROWTH`` is
    ``av_pp(t)``.  The withdrawals since issue open each year at ``wd_cum_pp`` of the month
    before, and the count at the month before's end-of-month count, ``AFT_DECR``, bit for
    bit.  And as modelx's dependency graph records them, ``av_pp``'s precedents in a month
    after ``t_entry()`` are ``av_pp`` of the month before and none of the fund's timings
    within a year, and the year's opening alone of the chains at a year's first month, where
    the withdrawals since issue and the count read theirs too.
    """
    table = sec_model.Data.model_point_table()
    openings = 0
    for key, point_id in zip(point_keys(sec_model), table.index):
        p = projection(sec_model, key)
        wd, gr = _code(p, "AFT_WD"), _code(p, "BEF_GROWTH")
        bef_nb, aft = _code(p, "BEF_NB"), _code(p, "AFT_DECR")
        for t in range(p.t_entry(), p.proj_len()):
            if p.is_active(t + 1):
                assert p.av_pp_at(t, wd) == p.av_pp(t + 1), (point_id, t)
            assert p.av_pp_at(t, gr) == p.av_pp(t), (point_id, t)
            if t > p.t_entry() and p.duration_mth(t) % 12 == 0:
                y, openings = p.policy_year(t), openings + 1
                assert p.av_pp_py(y) == p.av_pp_at(t - 1, wd), (point_id, t)
                assert p.wd_cum_pp_py(y) == p.wd_cum_pp(t - 1), (point_id, t)
                assert p.pols_if_py(y) == p.pols_if_at(t - 1, aft), (point_id, t)
                for cell, args, opening in (("av_pp", (t,), "av_pp_py"),
                                            ("wd_cum_pp", (t,), "wd_cum_pp_py"),
                                            ("pols_if_at", (t, bef_nb), "pols_if_py")):
                    reads = {(n.obj.name, n.args) for n in p.cells[cell].preds(*args)}
                    assert (opening, (y,)) in reads, (point_id, cell, t, reads)
                    assert not any(name == cell for name, _ in reads), (point_id, cell, t)
        mid = next((t for t in range(p.t_entry() + 1, p.proj_len())
                    if p.duration_mth(t) % 12 != 0), None)
        if mid is not None:
            reads = {(n.obj.name, n.args) for n in p.cells["av_pp"].preds(mid)}
            assert ("av_pp", (mid - 1,)) in reads, (point_id, reads)
            assert not any(name in ("av_pp_at", "av_pp_py") for name, _ in reads), (
                point_id, reads)
    assert openings > 100, openings


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


# modelx warns as its stack trace starts and stops, which is all the test does with it.
@pytest.mark.filterwarnings("ignore:call stack trace:UserWarning")
def test_no_cell_a_chain_recurses_through_formats_a_refusal(tmp_path):
    """No cell a cold call's deepest path holds more than once builds text (M10).

    A compiled cell's C frame holds the code that formats each of its messages, whether a
    run reaches it or not, and a chain holds a frame of each cell it recurses through at
    each level.  On CI's Ubuntu runner, a refusal formatted inside ``Term_UK_SEC``'s
    recursive waiver cell had its cold call at the longest cover need 512 KiB to 1 MiB,
    and 256 to 384 once the cell held none (K12).  So every refusal of this model whose
    message is formatted sits in a cell no chain recurses through: ``av_pp_at``, on the
    fund's chain, calls ``av_pp_grown_refusal`` on its error path alone.  On a model just
    read, at the longest cover of the accumulation cell and of the GMDB point with no
    withdrawals, issued now, each chain head of :data:`SHAPES` is called cold in the last
    month, under modelx's stack trace, with :data:`LONGEST_REFS` set, and the cells on the
    stack at its deepest point are counted.  A cell held there twice or more is one the
    chain recurses through, at every month or every year, or at both of its ends, as
    ``av_pp_at`` is, three timings at each.  None of them may build text anywhere in its
    formula, at a raise, in an error branch or into a local, nor raise other than one
    exception on one string constant (:func:`_text_faults`): the frame holds a message's
    code whether or not its branch runs.  A cell held once costs its frame once, as
    ``mort_rate``, whose refusal names an age outside the table, does at the chain's
    foot.  ``av_pp``, ``av_pp_py``, ``av_pp_at``, ``pols_if_at``, ``pols_if_py``,
    ``wd_cum_pp`` and ``wd_cum_pp_py`` must be among the cells checked, every cell the
    three blocked chains recurse through, or the test would check less than it says.
    """
    folder, frames = _longest_cover(tmp_path)
    found, checked = [], set()
    for label, months, entry, heads in frames:
        if entry != 0 or months != 12 * (OMEGA_MAX - YOUNGEST):
            continue
        for cell, timing in heads:
            fresh = mx.read_model(folder, name=_name("deepest"))
            try:
                for ref, value in LONGEST_REFS.items():
                    setattr(fresh.Projection, ref, value)
                p = _point(fresh, label)
                last = months - 1
                args = (last,) if timing is None else (last, _code(p, timing))
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
    assert {"av_pp", "av_pp_py", "av_pp_at", "pols_if_at", "pols_if_py", "wd_cum_pp",
            "wd_cum_pp_py"} <= checked, sorted(checked)
    assert not found, found


# ---------------------------------------------------------------------------
# T4 -- the count algebra
#
# BEF_DECR == BEF_NB + pols_new_biz, at every t of every point, is a convention
# (test_new_business_joins_the_count_before_decrements), and is not repeated here.


def test_the_count_rolls_forward_through_new_business_and_decrements(sec_model):
    """The count leaves month t by its deaths, surrenders and last survivors alone.

    On every committed point and at every ``t`` of its frame, the count weighting month
    ``t``, ``pols_if_at(t, BEF_DECR)``, less the count carried into ``t + 1``,
    ``pols_if_at(t + 1, BEF_NB)``, is the three outflows of month ``t``, to 1e-12.  The
    step from the last row to ``t = proj_len()`` is what catches a frame that runs a month
    too long: the survivors would then leave a month late, and the count would carry over.
    And the notes' end-of-month count, ``pols_if_at(t, AFT_DECR)``, is exactly the count
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
            out = p.pols_death(t) + p.pols_surr(t) + p.pols_maturity(t)
            moved = p.pols_if_at(t, bef_decr) - p.pols_if_at(t + 1, bef_nb)
            assert moved == pytest.approx(out, abs=1e-12), (point_id, t)
            assert p.pols_if_at(t, aft) == p.pols_if_at(t + 1, bef_nb), (point_id, t)
        pols = p.result_pols()
        assert list(pols.columns) == RESULT_POLS, point_id
        assert pols.index.name == "t" and list(pols.index) == list(range(p.proj_len()))
        carried = (pols["pols_if"] - pols[OUTFLOWS].sum(axis=1)).shift(1)
        expected = carried.fillna(p.pols_if_init()) + pols["pols_new_biz"]
        assert ((pols["pols_if"] - expected).abs() <= 1e-12).all(), point_id


def test_result_pols_holds_s_counts_with_the_new_business_beside_them(sec_model, s_model):
    """``result_pols()`` is S's counts, column for column, with ``pols_new_biz`` second (D5).

    ``ULB_UK_S`` has no such report, so each of its columns is held to the S cell of its
    name on every twin, all issued at the valuation date, at offset 0: the count, the
    deaths, the surrenders and the last survivors, to 1e-9 relative at no absolute floor,
    the frames ending together but on S's point 3, which the depletion threshold ends a
    month early, compared over the months before its last.  ``pols_new_biz`` holds the
    count in the issue month and 0 in every other.
    """
    table = sec_model.Data.model_point_table()
    twins = table.index[table["row_kind"] == "twin"].tolist()
    assert twins == sorted(s_model.Data.model_point_table().index)
    for point_id in twins:
        p, s = _point(sec_model, point_id), _point(s_model, point_id)
        pols = p.result_pols()
        assert list(pols.columns) == RESULT_POLS, point_id
        frame = range(p.proj_len() - (1 if p.proj_len() < s.proj_len() else 0))
        for column in ("pols_if", "pols_death", "pols_surr", "pols_maturity"):
            want = [s.cells[column](t) for t in frame]
            assert pols[column].loc[frame.start:frame.stop - 1].tolist() == pytest.approx(
                want, rel=1e-9, abs=0.0), (point_id, column)
        assert list(pols["pols_new_biz"]) == [
            p.policy_count() if t == 0 else 0.0 for t in pols.index], point_id


# What T4 multiplies policy_count by: not a whole number, because a count of policies need
# not be one, so that a flow which read the count as whole policies would not follow it.
COUNT_FACTOR = 2.5

# The withdrawals since issue the K14 test and T4 write at the GMDB point at 240, whose
# pattern has drawn its whole premium: half of it, so that its guarantee opens at 50,000,
# above its fund's 41,263 uplifted, and the rider charges from the first month.
HALF_WITHDRAWN = 50000.0


def test_scaling_the_count_scales_every_flow_and_no_per_policy_value(tmp_path):
    """``policy_count`` is a weight: 2.5 times the count, 2.5 times every flow, the same per
    policy.

    The committed table, with the GMDB point at 240 written as having withdrawn half its
    premium, so that its guarantee is in the money and the rider charges, as the K14 test
    writes it, and a copy of that with every count multiplied by :data:`COUNT_FACTOR`, are
    each read with :data:`SWITCHED_ON` set before either computes anything: the switches
    that ship off, at the splice's values, so that the surrender rate moves with the shock
    and binds its cap.  On every point ``result_cf``'s flows and the counts of
    ``result_pols`` are 2.5 times the committed table's, element by element, to 1e-12
    relative: a scaled count is a computed float, which may come back from the CSV within
    two ulps (``uk_sec_support``'s module docstring).  ``result_cf``'s ``av_pp`` and every
    column of ``result_uf``, per policy, are the committed table's exactly.  So is every
    other cell of :data:`COUNTED`, at every argument the sweep of the committed table's
    point cached: the count at each timing and the claims of each kind, which no report
    shows, among them, and the two count-weighted residuals, a rounding about 0 on that many
    policies, to the residuals' floor of 1e-9.  And every cell outside :data:`COUNTED` (the
    fund at each timing, the withdrawals since issue, the GMDB, the charges, the rates, both
    clocks, the flags) agrees bit for bit at every argument that sweep cached.  So a flow
    that dropped the count, or read it as whole policies, which a table of counts of 1 hides
    from every comparison with S and a count doubled hides here, fails.  Each counted cell
    but the residuals is nonzero on some point, the rider charge on the GMDB point at 240
    (USLIB-SEC-PLAN.md §5.2, T4): a rider charge weighted by the count once more, or a
    per-policy charge weighted by it, which a table of rider charges of 0 hides, fails.
    """
    table = _set("wd_cum_pp_init", [_label(_committed(), "derived", 4, 240)],
                 HALF_WITHDRAWN)(_committed())
    base = mx.read_model(_sec_inputs(tmp_path / "base", table), name=_name("counted"))
    scaled = mx.read_model(_sec_inputs(tmp_path / "scaled", table.assign(
        policy_count=COUNT_FACTOR * table["policy_count"])), name=_name("scaled"))
    counted = sorted(COUNTED - {"result_cf", "result_pols"})
    residuals = {"check_pols_roll_fwd_resid", "check_unit_funding_resid"}
    nonzero = set()
    try:
        for model in (base, scaled):
            for ref, value in SWITCHED_ON.items():
                setattr(model.Projection, ref, value)
        for key, scaled_key in zip(point_keys(base), point_keys(scaled)):
            one, many = projection(base, key), projection(scaled, scaled_key)
            sweep(one)
            for report in ("result_cf", "result_pols", "result_uf"):
                b, d = one.cells[report](), many.cells[report]()
                assert d.index.equals(b.index) and list(d.columns) == list(b.columns)
                fixed = [c for c in b.columns
                         if report == "result_uf" or c in PER_POLICY_COLUMNS]
                flows = [c for c in b.columns if c not in fixed]
                want = COUNT_FACTOR * b[flows]
                bad = ((d[flows] - want).abs() > 1e-12 * want.abs()).any()
                assert not bad.any(), (key, report, list(bad[bad].index))
                assert d[fixed].equals(b[fixed]), (key, report)
            for name in counted:
                floor = 1e-9 if name in residuals else 0.0
                for args in _cached_args(one.cells[name]):
                    want = COUNT_FACTOR * one.cells[name](*args)
                    got = many.cells[name](*args)
                    assert abs(got - want) <= floor + 1e-12 * abs(want), (
                        key, name, args, got, want)
                    if want != 0.0 and name not in residuals:
                        nonzero.add(name)
            assert twin_mismatches(one, many, exempt=TWIN_EXEMPT_DEFAULT | COUNTED,
                                   rtol=0.0, atol=0.0) == []
            _release(base, key)
            _release(scaled, scaled_key)
    finally:
        scaled.close()
        base.close()
    want = set(counted) - residuals
    assert want <= nonzero, f"0 on every point: {sorted(want - nonzero)}"


def test_a_point_restated_a_month_on_continues_its_own_flows(tmp_path):
    """The count a point carries into a month is the count that weights its flows (T4).

    Scaling every count alike, as the test above does, cannot see a flow weighted by the
    count a point opened with, ``policy_count()``, rather than the count in force in its
    month: both move by the same factor.  So each point in force on the committed table,
    with the GMDB point at 240 written as having withdrawn half its premium, so that the
    rider charges, is restated a month on, opened with what this model carries into its
    month 1: the count, ``pols_if_at(1, "BEF_NB")``; the fund, ``av_pp(1)``; the
    withdrawals since issue, ``wd_cum_pp(0)``; and the allowance, ``allowance_cum_pp(1)``.
    The restatement must continue the point's own frames, its row ``t`` the point's row
    ``t + 1``, in ``result_cf``, ``result_uf`` and ``result_pols``, every flow among them,
    to 1e-9 relative, floored at 1e-9 for what a state read back from the CSV an ulp off
    moves about 0.  A point whose frame ends in its first month has no month 1, and is left
    out.  Both models run at an inflation rate of 0, set on each as it is read (K7): the
    restatement moves the valuation date a month on, and expense inflation, on the
    valuation clock, would step a month apart by design (D7).  The restatement also shows
    the opening state complete on this model's own states, as the splice shows it on S's.
    """
    gmdb = _label(_committed(), "derived", 4, 240)
    table = _set("wd_cum_pp_init", [gmdb], HALF_WITHDRAWN)(_committed())
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
            row = table.loc[[label]].assign(
                duration_mth=p.duration_mth(1),
                policy_count=p.pols_if_at(1, _code(p, "BEF_NB")),
                av_pp_init=p.av_pp(1), wd_cum_pp_init=p.wd_cum_pp(0),
                allowance_cum_pp_init=p.allowance_cum_pp(1))
            row.index = pd.Index([top], name="point_id")
            rows.append(row)
            pairs.append((label, top))
        frames = {label: {report: _point(model, label).cells[report]()
                          for report in (*REPORTS, "result_pols")}
                  for label, _ in pairs}
    finally:
        model.close()
    assert gmdb in frames and (frames[gmdb]["result_cf"]["gmdb_charges"] > 0.0).any()
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


def test_the_roll_forward_closes_on_a_million_policies(tmp_path):
    """``check_pols_roll_fwd`` scales its tolerance with the count, and closes at 1e6.

    A residual is rounding on that many policies, so the check holds it to 1e-10 times
    ``max(policy_count(), 1)``, where its tolerance unscaled would be 1e-10: at the counts
    the other tests use, one policy or less, the two are one.  ``ULB_UK_S`` scales by
    ``pols_if_init()``, which here is 0 on a point issued at the valuation date, the count
    entering as new business.  So every committed point is projected from a copy where each
    counts a million policies: the check closes on each, and on some point the largest
    residual exceeds the unscaled 1e-10, so the scaling is what closes it (USLIB-SEC-PLAN.md
    §5.2, T4, precised at M10).  The fund's and the unit funding's checks are per policy and
    scale with nothing.
    """
    table = _committed()
    model = mx.read_model(_sec_inputs(tmp_path, table.assign(policy_count=1e6)),
                          name=_name("million"))
    worst = 0.0
    try:
        for key, point_id in zip(point_keys(model), table.index):
            p = projection(model, key)
            assert p.policy_count() == 1e6
            assert p.check_pols_roll_fwd() and p.check_av_roll_fwd(), point_id
            worst = max(worst, max(abs(p.check_pols_roll_fwd_resid(t))
                                   for t in range(p.proj_len())))
            _release(model, key)
    finally:
        model.close()
    assert worst > 1e-10, worst


# ---------------------------------------------------------------------------
# T5 -- validation
#
# Each malformed table is the committed one with one fault.  The checks run over the whole
# table as it is read, in Data, and the message names the file it read and the column or
# every point at fault.  A blank cell reads as NaN, and so does a text cell once the checks
# coerce the column to numbers, so each is refused as a count, a duration or a state that
# is not a number.  The repeated point_id holds another policy under the same label, as a
# bad extract would, so that the check must look at the labels and not at whole rows.  The
# point_ids are the committed table's: 1 to 6 the twins of S's points; 7, the anchor cell at
# 30; 8, the adviser charge at 66; 9, the GMDB point at 240; 10, the anchor cell in its last
# month, 352; 11, the GMDB point issued 13 months on.  A {file} in a message is the table's
# filename: every case is read by one model, from a file of its own (the malformed fixture).


def _drop(column):
    return lambda table: table.drop(columns=column)


MALFORMED = [
    ("a negative count", _set("policy_count", [7], -0.1),
     "{file}: policy_count must be a number, zero or more; it is not at point_id [7]"),
    ("a blank count", _set("policy_count", [8], float("nan")),
     "{file}: policy_count must be a number, zero or more; it is not at point_id [8]"),
    ("two bad counts", _set("policy_count", [7, 9], -1.0),
     "{file}: policy_count must be a number, zero or more; it is not at point_id [7, 9]"),
    ("a text count", _set("policy_count", [10], "abc"),
     "{file}: policy_count must be a number, zero or more; it is not at point_id [10]"),
    ("an infinite count", _set("policy_count", [10], float("inf")),
     "{file}: policy_count must be a number, zero or more; it is not at point_id [10]"),
    ("a fractional duration", _set("duration_mth", [8], 66.5),
     "{file}: duration_mth must be a whole number of months; it is not at point_id [8]"),
    ("a blank duration", _set("duration_mth", [11], float("nan")),
     "{file}: duration_mth must be a whole number of months; it is not at point_id [11]"),
    ("a text duration", _set("duration_mth", [10], "x4"),
     "{file}: duration_mth must be a whole number of months; it is not at point_id [10]"),
    # numpy casts a float past int64 to the least int64, a bond issued 2**63 months on,
    # without a word: the table refuses it first.
    ("a duration past int64", _set("duration_mth", [7], 1e19),
     "{file}: duration_mth must be below 2**53 months; it is not at point_id [7]"),
    ("durations of 2**53 months at two points", _set("duration_mth", [7, 9], 2.0 ** 53),
     "{file}: duration_mth must be below 2**53 months; it is not at point_id [7, 9]"),
    ("issued beyond the horizon", _set("duration_mth", [11], -121),
     "{file}: duration_mth must be -120 or more, a bond issued at most 120 months after "
     "the valuation date; it is not at point_id [11]"),
    *[(f"no {column} column", _drop(column), f"{{file}} has no {column} column")
      for column in ("policy_count", "duration_mth", *STATE)],
    ("a repeated point_id",
     lambda t: pd.concat([t, t.loc[[7]].assign(policy_id="ULB-900099")]),
     "{file}: point_id [7] appears more than once"),
    ("a negative fund", _set("av_pp_init", [7], -1.0),
     "{file}: av_pp_init must be a number above 0, the unit fund; it is not at point_id "
     "[7]"),
    ("a fund of 0 in force", _set("av_pp_init", [8], 0.0),
     "{file}: av_pp_init must be a number above 0, the unit fund; it is not at point_id "
     "[8]"),
    ("a fund of 0 at outset", _set("av_pp_init", [1], 0.0),
     "{file}: av_pp_init must be a number above 0, the unit fund; it is not at point_id "
     "[1]"),
    ("a blank fund", _set("av_pp_init", [9], float("nan")),
     "{file}: av_pp_init must be a number above 0, the unit fund; it is not at point_id "
     "[9]"),
    ("a text fund", _set("av_pp_init", [10], "x"),
     "{file}: av_pp_init must be a number above 0, the unit fund; it is not at point_id "
     "[10]"),
    ("an infinite fund", _set("av_pp_init", [7], float("inf")),
     "{file}: av_pp_init must be a number above 0, the unit fund; it is not at point_id "
     "[7]"),
    ("negative withdrawals", _set("wd_cum_pp_init", [7], -1.0),
     "{file}: wd_cum_pp_init must be a number, zero or more; it is not at point_id [7]"),
    ("blank withdrawals", _set("wd_cum_pp_init", [8], float("nan")),
     "{file}: wd_cum_pp_init must be a number, zero or more; it is not at point_id [8]"),
    ("text withdrawals", _set("wd_cum_pp_init", [9], "x"),
     "{file}: wd_cum_pp_init must be a number, zero or more; it is not at point_id [9]"),
    ("infinite withdrawals", _set("wd_cum_pp_init", [10], float("inf")),
     "{file}: wd_cum_pp_init must be a number, zero or more; it is not at point_id [10]"),
    ("withdrawals on new business", _set("wd_cum_pp_init", [1], 100.0),
     "{file}: wd_cum_pp_init must be 0 on a bond not yet in force, duration_mth 0 or "
     "less; it is not at point_id [1]"),
    ("withdrawals on future business", _set("wd_cum_pp_init", [11], 1.0),
     "{file}: wd_cum_pp_init must be 0 on a bond not yet in force, duration_mth 0 or "
     "less; it is not at point_id [11]"),
    ("a negative allowance", _set("allowance_cum_pp_init", [7], -1.0),
     "{file}: allowance_cum_pp_init must be a number, zero or more; it is not at "
     "point_id [7]"),
    ("a blank allowance", _set("allowance_cum_pp_init", [8], float("nan")),
     "{file}: allowance_cum_pp_init must be a number, zero or more; it is not at "
     "point_id [8]"),
    ("a text allowance", _set("allowance_cum_pp_init", [9], "x"),
     "{file}: allowance_cum_pp_init must be a number, zero or more; it is not at "
     "point_id [9]"),
    ("an infinite allowance", _set("allowance_cum_pp_init", [10], float("inf")),
     "{file}: allowance_cum_pp_init must be a number, zero or more; it is not at "
     "point_id [10]"),
    ("an allowance on new business", _set("allowance_cum_pp_init", [1], 5000.0),
     "{file}: allowance_cum_pp_init must be 0 on a bond not yet in force, duration_mth 0 "
     "or less; it is not at point_id [1]"),
    ("an allowance on future business", _set("allowance_cum_pp_init", [11], 1.0),
     "{file}: allowance_cum_pp_init must be 0 on a bond not yet in force, duration_mth 0 "
     "or less; it is not at point_id [11]"),
    ("a blank flag", _set("gmdb_flag", [3], float("nan")),
     "{file}: gmdb_flag must be True or False; it is not at point_id [3]"),
    ("a flag written yes", _set("gmdb_flag", [2], "yes"),
     "{file}: gmdb_flag must be True or False; it is not at point_id [2]"),
    ("a flag written 1", _set("gmdb_flag", [1], 1),
     "{file}: gmdb_flag must be True or False; it is not at point_id [1]"),
    ("an unknown sex", _set("sex", [2], "X"),
     "{file}: sex must be M or F; it is not at point_id [2]"),
    ("a joint bond", _set("lives", [1], "joint"),
     "{file}: lives must be single; it is not at point_id [1]"),
    ("an unknown withdrawal pattern", _set("wd_pattern", [4], "monthly"),
     "{file}: wd_pattern must be none or allowance_5pct or custom; it is not at point_id "
     "[4]"),
    ("a blank issue age", _set("age_at_entry", [1], float("nan")),
     "{file}: age_at_entry must be a finite number; it is not at point_id [1]"),
    ("an infinite issue age", _set("age_at_entry", [2], float("inf")),
     "{file}: age_at_entry must be a finite number; it is not at point_id [2]"),
    ("a text issue age", _set("age_at_entry", [3], "x65"),
     "{file}: age_at_entry must be a finite number; it is not at point_id [3]"),
    # int64 holds 2**53 exactly but the floats about it inexactly, and numpy casts a float
    # past int64 to the least int64 without a word: the table refuses 2**53 and more, as a
    # float and as an int, and reads 2**53 - 1, which proj_len() then refuses as an issue
    # age at or past omega_age (NOT_ISSUED).
    ("an issue age of 2**53", _set("age_at_entry", [1], 2.0 ** 53),
     "{file}: age_at_entry must be below 2**53 in size; it is not at point_id [1]"),
    ("issue ages of 2**53, an int, at two points", _set("age_at_entry", [2, 3], 2 ** 53),
     "{file}: age_at_entry must be below 2**53 in size; it is not at point_id [2, 3]"),
    ("a negative premium", _set("premium", [1], -1.0),
     "{file}: premium must be a number, zero or more; it is not at point_id [1]"),
    ("a blank premium", _set("premium", [2], float("nan")),
     "{file}: premium must be a number, zero or more; it is not at point_id [2]"),
    ("no segments", _set("n_segments", [1], 0),
     "{file}: n_segments must be a whole number, 1 or more; it is not at point_id [1]"),
    ("half a segment", _set("n_segments", [2], 2.5),
     "{file}: n_segments must be a whole number, 1 or more; it is not at point_id [2]"),
    ("a blank count of segments", _set("n_segments", [3], float("nan")),
     "{file}: n_segments must be a whole number, 1 or more; it is not at point_id [3]"),
    ("an uplift below 1", _set("db_uplift", [5], 0.999),
     "{file}: db_uplift must be a number, 1 or more; it is not at point_id [5]"),
    ("a blank uplift", _set("db_uplift", [1], float("nan")),
     "{file}: db_uplift must be a number, 1 or more; it is not at point_id [1]"),
    ("an AMC past 1", _set("amc_rate", [1], 1.5),
     "{file}: amc_rate must be a number from 0 to 1; it is not at point_id [1]"),
    ("a negative AMC", _set("amc_rate", [2], -0.01),
     "{file}: amc_rate must be a number from 0 to 1; it is not at point_id [2]"),
    ("blank further costs", _set("further_costs_rate", [3], float("nan")),
     "{file}: further_costs_rate must be a number from 0 to 1; it is not at point_id [3]"),
    ("a tax provision past 1", _set("tax_provision_rate", [4], 1.2),
     "{file}: tax_provision_rate must be a number from 0 to 1; it is not at point_id [4]"),
    ("a negative custom withdrawal", _set("wd_rate_custom", [6], -0.01),
     "{file}: wd_rate_custom must be a number, zero or more; it is not at point_id [6]"),
    ("a blank custom withdrawal", _set("wd_rate_custom", [6], float("nan")),
     "{file}: wd_rate_custom must be a number, zero or more; it is not at point_id [6]"),
    ("a negative adviser charge", _set("oac_rate", [3], -0.001),
     "{file}: oac_rate must be a number from 0 to 1; it is not at point_id [3]"),
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


def test_the_future_horizon_is_a_reference_that_bounds_future_business(tmp_path):
    """``Data.future_horizon_mth`` refuses a bond issued later than it, and 0 refuses all.

    The committed table's one future point is issued 13 months on.  It reads at the shipped
    120 months and at 13, the shortest horizon that admits it, and is refused at 12, by
    name.  At 0 the model takes no future new business, D4's fallback for a product that
    cannot support it, and the message says so.  A negative horizon is itself refused.
    Setting the Reference clears the table, so each value is read afresh.
    """
    future = _label(_committed(), "future", 4, -13)
    later = (f"{TABLE}: duration_mth must be -12 or more, a bond issued at most 12 months "
             f"after the valuation date; it is not at point_id [{future}]")
    no_future = (f"{TABLE}: duration_mth must be 0 or more: this model takes no future new "
                 f"business; it is not at point_id [{future}]")
    model = mx.read_model(_sec_inputs(tmp_path, _committed()), name=_name("horizon"))
    try:
        assert model.Data.future_horizon_mth == 120
        negative = "future_horizon_mth must be 0 months or more, not -1"
        for horizon, refusal in ((13, None), (12, later), (0, no_future), (-1, negative),
                                 (120, None)):
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
    """A bond at the limiting age has no frame, and ``proj_len()`` refuses it by name.

    The anchor cell in its last month before exhaustion is moved on to ``duration_mth``
    660, the month it reaches ``omega_age``, 120, at issue age 65.  That is a rule of the
    product, not of the table: it needs the limiting age, a Reference, read where the frame
    is defined, so the table reads, and the point is refused on its first projection,
    rather than projecting nothing.  A loop over the block would meet the point only when it
    reached it, after projecting the points before it, so ``run_sec.py --block``, run beside
    the table, asks every point for its frame first: it fails naming the point, and prints
    nothing before.  And one month earlier, 659, the last month of cover, projects one
    month, its fund carried in.
    """
    moved = _label(_committed(), "derived", 1, 352)
    model = _read_edited(tmp_path, _set("duration_mth", [moved], 660))
    message = (f"point_id {moved}: duration_mth 660 is at or past the end of cover, policy "
               f"month 660, the limiting age 120")
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
    model = _read_edited(tmp_path / "last", _set("duration_mth", [moved], 659))
    try:
        df = _point(model, moved).result_cf()
        assert len(df) == 1 and df["av_pp"].iloc[0] == _committed().at[moved, "av_pp_init"]
    finally:
        model.close()


# What the contract does not issue, or the model cannot project, refused by proj_len() as
# a point past its cover is, as (case, the table's edit, the References set, the point, the
# message, and the frame the point projects at the shipped References, or None).  Data
# reads an issue age as ULB_UK_S does, so each reads.  The mortality table rates ages from
# 18, so a bond issued younger is refused, though the product admits issue from 3 months;
# one issued at or past omega_age has no cover.  Each bound is refused just inside it here,
# and accepted at it in the edges test, and each, moved past a committed twin, refuses it,
# which at the shipped bound projects its frame: the Reference is what refuses it.  Point 1
# is the anchor cell, issued at 65 with a 5% withdrawal, whose fund lasts 353 months.  The
# References' domains are DOMAINS', below.
NOT_ISSUED = [
    ("an issue age of 17", _set("age_at_entry", [1], 17), {}, 1,
     "point_id 1: the issue age, 17, is below issue_age_min, 18", None),
    ("an issue age below a bound raised to 66", None, {"issue_age_min": 66}, 1,
     "point_id 1: the issue age, 65, is below issue_age_min, 66", 353),
    ("an issue age of 120", _set("age_at_entry", [1], 120), {}, 1,
     "point_id 1: the issue age, 120, is at or past omega_age, 120: the bond has no cover",
     None),
    ("an issue age at a limiting age lowered to 65", None, {"omega_age": 65}, 1,
     "point_id 1: the issue age, 65, is at or past omega_age, 65: the bond has no cover",
     353),
    ("an issue age of 2**53 - 1", _set("age_at_entry", [1], 2 ** 53 - 1), {}, 1,
     f"point_id 1: the issue age, {2 ** 53 - 1}, is at or past omega_age, 120: the bond has "
     f"no cover", None),
]


@pytest.mark.parametrize("case, edit, refs, point, message, frame", NOT_ISSUED,
                         ids=[c[0] for c in NOT_ISSUED])
def test_a_point_the_contract_does_not_issue_is_refused_by_proj_len(tmp_path, case, edit,
                                                                    refs, point, message,
                                                                    frame):
    """``proj_len()`` refuses a point outside the contract's bounds, naming both (§6.6).

    ``ULB_UK_S`` projects a bond from any age its table holds, and so would modelx here, but
    the mortality table rates no age below 18 and the compiled model's caches are sized
    from the contract: a frame of at most ``omega_age_max - issue_age_min`` years and the
    horizon.  So the frame refuses such a point, naming it, as it refuses a point past its
    cover, and every report with it (:data:`NOT_ISSUED`): each bound just inside it, and
    each bound moved past a committed point, which projects at the shipped bound, on a model
    read afresh.  The table reads either way.  Every Reference is set on a model just read,
    before its projection computes anything (K7).
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


# Each Reference proj_len() holds to a domain, at both edges of it, as (case, the
# References set, the refusal, or None where proj_len() accepts them), on the anchor cell's
# twin (proj_len's docstring gives each domain's reason).  NaN and the infinities are
# outside every domain: S reads several of them through a min or a max whose bound comes
# first, where a NaN is lost.  A finite domain's upper edge is the largest float, accepted,
# where the frame computes what it can of it: depletion_threshold there holds the fund at
# outset exhausted, and a fund_return there grows the fund past the floats, each refused by
# its own rule, past the domain.  issue_age_min, allowance_years and omega_age are whole
# numbers of years below 2**53, which the compiled model holds as long long, printed through
# int() once whole: each is refused at a fraction and at exactly 2**53, and its largest
# whole number is accepted, or refused by a later rule.  return_shock is held with
# fund_return: their sum, the trailing year's return, must be above -1.  omega_age_max, the
# largest limiting age the compiled model's caches are sized for (spec_sec.py), 121, the
# shipped table's last age plus one, is a whole number too, and omega_age above it is
# refused, so that a longer table bounds no frame: every limiting age the shipped table
# admits projects, as at stage E, and lowered to 120 the bound refuses 121.
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


def _returns(fund_return, return_shock):
    """The joint rule's refusal, at ``fund_return`` and ``return_shock``."""
    return (f"point_id 1: fund_return + return_shock, the trailing year's return, must be "
            f"above -1, not {float(fund_return + return_shock)}, under fund_return "
            f"{float(fund_return)} and return_shock {float(return_shock)}")


OMEGA = ("point_id 1: omega_age must be above issue_age_min, 18, and at most 121, a year "
         "past mort_table.csv's last age, not {}")
DOMAINS = [
    *_domain("fund_return", "a finite number, -1 or more", (), (math.nextafter(-1.0, -2.0),)),
    ("fund_return=-1.0 with return_shock 0.5", {"fund_return": -1.0, "return_shock": 0.5},
     None),
    ("fund_return=BIG", {"fund_return": BIG},
     f"point_id 1: the unit fund grown in month 11, av_pp_at(11, AFT_GROWTH), is nan, "
     f"not a finite number, under fund_return {BIG} and av_pp_init 100000.0"),
    *_domain("inflation_rate", "a finite number, -1 or more", (-1.0, BIG),
             (math.nextafter(-1.0, -2.0),)),
    *_domain("return_shock", "a finite number", (-1.0, BIG), ()),
    ("fund_return 0 with return_shock -1", {"fund_return": 0.0, "return_shock": -1.0},
     _returns(0.0, -1.0)),
    ("fund_return 0 with return_shock just above -1",
     {"fund_return": 0.0, "return_shock": math.nextafter(-1.0, 0.0)}, None),
    ("fund_return -0.9 with return_shock -0.5", {"fund_return": -0.9, "return_shock": -0.5},
     _returns(-0.9, -0.5)),
    *_domain("mort_be_factor", "a finite number, 0 or more", (0.0, BIG), (BELOW_0,)),
    *_domain("wd_allowance_rate", "a finite number, 0 or more", (0.0, BIG), (BELOW_0,)),
    *_whole_domain("allowance_years", (0, WHOLE - 1)),
    *_domain("depletion_threshold", "a finite number, 0 or more", (0.0,), (BELOW_0,)),
    ("depletion_threshold=BIG", {"depletion_threshold": BIG},
     "point_id 1: av_pp_init, the fund at outset, is 100000.0, at or below "
     f"depletion_threshold, {BIG}: the bond holds nothing to project from its issue month"),
    *_domain("surr_rate_cap", "a number from 0 to 1", (0.0, 1.0), (BELOW_0, ABOVE_1)),
    *_domain("wd_cap_rate", "a number from 0 to 1", (0.0, 1.0), (BELOW_0, ABOVE_1)),
    *_domain("perf_factor_cap", "a finite number, 0 or more", (0.0, BIG), (BELOW_0,)),
    *_domain("perf_factor_slope", "a finite number, 0 or more", (0.0, BIG), (BELOW_0,)),
    *_domain("allow_step", "a finite number, 0 or more", (0.0, BIG), (BELOW_0,)),
    *_whole_domain("issue_age_min", (0,)),
    ("issue_age_min=2**53-1", {"issue_age_min": WHOLE - 1},
     f"point_id 1: the issue age, 65, is below issue_age_min, {int(WHOLE - 1)}"),
    *_whole_domain("omega_age", (120, 121), below=False),
    *_whole_domain("omega_age_max", (120, 121, WHOLE - 1), below=False),
    ("omega_age=121 with omega_age_max 120", {"omega_age": 121, "omega_age_max": 120},
     "point_id 1: omega_age, 121, is above omega_age_max, 120"),
    ("omega_age_max=119", {"omega_age_max": 119},
     "point_id 1: omega_age, 120, is above omega_age_max, 119"),
    ("omega_age=122", {"omega_age": 122}, OMEGA.format(122)),
    ("omega_age=18", {"omega_age": 18}, OMEGA.format(18)),
    ("omega_age=19", {"omega_age": 19},
     "point_id 1: the issue age, 65, is at or past omega_age, 19: the bond has no cover"),
    ("omega_age=2**53-1", {"omega_age": WHOLE - 1}, OMEGA.format(int(WHOLE - 1))),
]


@pytest.mark.parametrize("case, refs, message", DOMAINS, ids=[c[0] for c in DOMAINS])
def test_each_reference_is_held_to_its_domain_at_both_edges(case, refs, message):
    """``proj_len()`` holds each Reference to its domain, NaN and the infinities outside it.

    :mod:`~.ULB_UK_S` reads ``perf_factor_cap`` and ``allow_step`` through a ``min`` whose
    bound comes first, the surrender cap's, so that a NaN of either reads as the cap in every
    month; ``return_shock`` through the shortfall's ``max(0, ...)``, so that a NaN reads as
    no shock; ``wd_cap_rate`` through the room's, so that a NaN, or a negative rate, pays no
    withdrawal, and the anchor cell projects 660 months where it projects 353; and
    ``issue_age_min`` and ``omega_age`` in comparisons a NaN switches off, the limiting age
    sizing every frame.  The frame refuses each such Reference, by name, before it projects
    anything, and every report with it, at the nearest value outside each edge of its
    domain, and accepts the edge itself (:data:`DOMAINS`): the integer References at a
    fraction and at exactly ``2**53``, ``omega_age`` past the mortality table's last age,
    and ``return_shock`` where the trailing year's return it makes with ``fund_return``
    is -100% or less, which a shock of -1 at the shipped 5% return is not.  Each case sets
    its References on a model just read (K7).
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


def test_an_opening_fund_past_the_floats_is_refused_naming_it(tmp_path, sec_model):
    """An opening fund near the largest float is refused where it leaves the floats.

    ``Data`` holds ``av_pp_init`` to a finite number above 0, so a fund of 1.79e308 reads;
    a month's growth at the shipped 5% then takes it past the floats in month 1, where
    ``av_pp_at(1, AFT_GROWTH)`` refuses it, through ``av_pp_grown_refusal(1)``, the cell its
    error path calls so that no cell on the fund's chain formats a message.  The refusal
    names the opening fund beside ``fund_return``, so that it reads true whichever is the
    cause: here the fund, at a shipped return; under ``DOMAINS``' ``fund_return`` at the
    largest float, the return.  And where the fund grown is finite, the refusal's cell
    returns it, the same float as ``av_pp_at``'s, on every committed point in every month.
    """
    model = _read_edited(tmp_path, _set("av_pp_init", [7], 1.79e308))
    try:
        _refused(_point(model, 7).result_cf,
                 "point_id 7: the unit fund grown in month 1, av_pp_at(1, AFT_GROWTH), is "
                 "inf, not a finite number, under fund_return 0.05 and av_pp_init 1.79e+308")
    finally:
        model.close()
    for key in point_keys(sec_model):
        p = projection(sec_model, key)
        grown = _code(p, "AFT_GROWTH")
        for t in range(p.proj_len() + 1):
            assert p.av_pp_grown_refusal(t).hex() == p.av_pp_at(t, grown).hex(), (key, t)


def test_the_allowance_past_the_floats_is_refused_in_its_cell():
    """An allowance a rate past every amount of money makes is refused where it first is.

    ``wd_allowance_rate`` at the largest float is in its domain, and the frame projects, the
    anchor pattern's withdrawal capped at 7.5%; but the allowance it accrues is past the
    floats from the first month, where :func:`excess_gain_pp`'s ``max(0, ...)`` would read
    it as no excess gain.  ``allowance_cum_pp`` refuses it, naming the month and the
    References, and so does every report that reads it: a computed value out of its range
    is refused in its cell (USLIB-SEC-PLAN.md §7.1, *Record - M1*).
    """
    model = mx.read_model(model_path(SEC), name=_name("allowance_big"))
    try:
        model.Projection.wd_allowance_rate = BIG
        p = _row(model, "twin", 1, 0)
        assert len(p.result_cf()) > 0
        _refused(p.result_uf, f"point_id 1: the allowance allowance_cum_pp(0) is inf, not a "
                              f"finite number, under wd_allowance_rate {BIG} and "
                              f"allowance_years 20")
    finally:
        model.close()


def _exhausted(point, value):
    """The message ``proj_len()`` gives a bond in force at ``point`` whose fund is
    ``value``, at or below the shipped threshold."""
    return (f"point_id {point}: av_pp_init is {value}, at or below depletion_threshold, "
            f"{THRESHOLD}: a bond in force whose fund is exhausted at the valuation date has "
            f"nothing to project")


# The depletion threshold's rules on a bond's opening fund, as (case, the table's edit, the
# References set, the point, the message where refused or None, and the frame where it
# projects).  The threshold is half a pence, a Reference, so each rule is stated on it,
# never on a stand-in such as a fund above 0, and tested where the two part: a fund of
# exactly the threshold is exhausted, so is part of it and so is a rounding above 0, and the
# least fund past it is not, and projects; with the threshold moved off its shipped value,
# a fund the shipped one projects is refused (USLIB-SEC-PLAN.md §7.7, *Record — M9*).  A
# bond not yet in force holds its fund at outset, which at or below the threshold has
# nothing to project either.  Point 7 is the anchor cell in force 30 months; 11, the GMDB
# point issued 13 months on.  A fund past the threshold that the next month's withdrawal
# draws to nothing projects that month alone.
PAST_THE_THRESHOLD = math.nextafter(THRESHOLD, 1.0)
EXHAUSTED = [
    ("a fund of exactly the threshold", _set("av_pp_init", [7], THRESHOLD), {}, 7,
     _exhausted(7, THRESHOLD), None),
    ("a fund of part of the threshold", _set("av_pp_init", [7], 0.003), {}, 7,
     _exhausted(7, 0.003), None),
    ("a fund of a rounding above 0", _set("av_pp_init", [7], 3.4e-15), {}, 7,
     _exhausted(7, 3.4e-15), None),
    ("a fund just past the threshold", _set("av_pp_init", [7], PAST_THE_THRESHOLD), {}, 7,
     None, 1),
    ("a fund of 0.006", _set("av_pp_init", [7], 0.006), {}, 7, None, 1),
    ("a fund of 0.006 under a threshold raised to 0.01", _set("av_pp_init", [7], 0.006),
     {"depletion_threshold": 0.01}, 7,
     "point_id 7: av_pp_init is 0.006, at or below depletion_threshold, 0.01: a bond in "
     "force whose fund is exhausted at the valuation date has nothing to project", None),
    ("a fund at outset of the threshold", _set("av_pp_init", [11], THRESHOLD), {}, 11,
     f"point_id 11: av_pp_init, the fund at outset, is {THRESHOLD}, at or below "
     f"depletion_threshold, {THRESHOLD}: the bond holds nothing to project from its issue "
     f"month", None),
]


@pytest.mark.parametrize("case, edit, refs, point, message, frame", EXHAUSTED,
                         ids=[c[0] for c in EXHAUSTED])
def test_a_fund_at_or_below_the_threshold_is_exhausted(tmp_path, case, edit, refs, point,
                                                       message, frame):
    """``proj_len()`` refuses a bond whose fund is at or below ``depletion_threshold``.

    ``Data`` reads the table, since the rule is the product's: the threshold is a Reference
    of the projection, which ``Data`` cannot see, so the frame refuses the point, naming it,
    as it refuses a point past its cover (:data:`EXHAUSTED`).  A bond in force whose fund is
    exhausted has nothing left to project, and ``ULB_UK_S`` would project a month on a fund
    above 0 that the threshold reads as exhausted.  The least fund past the threshold
    projects, and is drawn to nothing in its first month.  Every Reference is set on a model
    just read (K7).
    """
    model = _read_edited(tmp_path, edit)
    try:
        for ref, value in refs.items():
            setattr(model.Projection, ref, value)
        model.Data.model_point_table()
        p = _point(model, point)
        if message is not None:
            _refused(p.result_cf, message)
        else:
            assert len(p.result_cf()) == frame
            assert p.av_pp(0) == p.av_pp_init() > p.depletion_threshold
            assert p.av_pp_at(0, _code(p, "AFT_WD")) <= p.depletion_threshold
    finally:
        model.close()


# The surrender rate at its edges, on the anchor cell's twin, as (case, the References set,
# the month the rate first reaches the edge, the cell's refusal and every report's, or None
# where the rate is accepted).  proj_len() holds the cap to 0 to 1 and each multiplier to a
# finite number, 0 or more, so that no frame reaches a rate outside 0 to 1; the cell
# refuses one itself, for a caller that reads it outside a frame.  Under multipliers that
# take the uncapped rate past 1 from policy year 6, t = 60, a performance multiplier of 19,
# a cap of exactly 1 is the rate there: accepted, every policy left after the month's deaths
# surrenders.  A cap just above 1 is refused, and below 0 a multiplier's cap of -1.
PAST_ONE = {"perf_factor_cap": 20.0, "perf_factor_slope": 20.0, "return_shock": -0.9}
SURRENDER_EDGES = [
    ("exactly 1", {**PAST_ONE, "surr_rate_cap": 1.0}, 60, None, None),
    ("just above 1", {**PAST_ONE, "surr_rate_cap": ABOVE_1}, 60,
     f"point_id 1: the surrender rate surr_rate(60) is {ABOVE_1}, outside 0 to 1, under "
     f"surr_rate_cap {ABOVE_1}, perf_factor_cap 20.0, perf_factor_slope 20.0, return_shock "
     f"-0.9 and allow_step 1.5",
     f"point_id 1: surr_rate_cap must be a number from 0 to 1, not {ABOVE_1}"),
    ("below 0", {"perf_factor_cap": -1.0}, 0,
     "point_id 1: the surrender rate surr_rate(0) is -0.02, outside 0 to 1, under "
     "surr_rate_cap 0.35, perf_factor_cap -1.0, perf_factor_slope 2.0, return_shock 0.0 and "
     "allow_step 1.5",
     "point_id 1: perf_factor_cap must be a finite number, 0 or more, not -1.0"),
]


@pytest.mark.parametrize("case, refs, month, cell_message, report_message", SURRENDER_EDGES,
                         ids=[c[0] for c in SURRENDER_EDGES])
def test_the_surrender_rate_is_a_probability_at_its_edges(case, refs, month, cell_message,
                                                          report_message):
    """A surrender rate of exactly 1 is accepted, and one just outside 0 to 1 refused.

    ``ULB_UK_S``'s rate is ``min(cap, table x multiplier x step)``, the bound S's own,
    which keeps S's order.  Past 1 its monthly rate, ``1 - (1 - w)^(1/12)``, is complex,
    and below 0 its surrenders add policies, every check passing.  At exactly 1 the monthly
    rate is 1, and every policy left after the month's deaths surrenders: a rate the cap
    binds at, in its range (:data:`SURRENDER_EDGES`).  So at a cap of exactly 1 the cell is
    1.0 from the month the uncapped rate passes it, and the frame projects whole, every
    count 0 after that month.  Just above 1, and below 0, the cell refuses the rate in the
    month it first leaves 0 to 1, naming the point, the month, the rate and the References
    that make it, the month before projecting; and every report is refused by the frame,
    which holds the cap and the multipliers to their domains.  The References are set on a
    model just read (K7).
    """
    model = mx.read_model(model_path(SEC), name=_name("surr"))
    try:
        for ref, value in refs.items():
            setattr(model.Projection, ref, value)
        p = _row(model, "twin", 1, 0)
        if month > 0:
            assert 0.0 <= p.surr_rate(month - 1) < 1.0
        if cell_message is None:
            assert p.surr_rate(month) == p.surr_rate_mth(month) == 1.0
            assert len(p.result_cf()) == FRAME[1] and p.check_pols_roll_fwd()
            left = p.pols_if_at(month, _code(p, "BEF_SURR"))
            assert p.pols_surr(month) == left > 0.0 and p.pols_if(month + 1) == 0.0
        else:
            _refused(lambda: p.surr_rate(month), cell_message)
            _refused(p.result_cf, report_message)
    finally:
        model.close()


def test_the_edges_of_the_in_force_interface_are_accepted(sec_model, tmp_path):
    """A zero count, whole numbers in any type, the horizon and each bound's edge are read.

    A count of 0 is a point that projects zeros; ``30.0`` is a whole number of months, read
    back as the int the policy clock counts in; a bond issued 120 months after the valuation
    date, the shipped ``future_horizon_mth``, is the last one the table admits, with a frame
    of 473 months, 353 from its issue after 120 before it.  A row valued in its first month,
    1, holds a fund and a withdrawal, the state a bond in force holds where one not yet in
    force holds none.  And each bound of the contract at its edge projects: issue at 18,
    the youngest the table rates, and at 119, a year short of the limiting age.
    """
    committed = _committed()
    last = _label(committed, "derived", 1, 352)
    future = _label(committed, "future", 4, -13)
    first = _label(committed, "derived", 1, 30)

    def edit(table):
        table = _set("policy_count", [last], 0.0)(table)
        table = _set("duration_mth", [first], 1)(table)
        table = table.assign(duration_mth=table["duration_mth"].astype(float))
        table = _set("duration_mth", [future], -120.0)(table)
        table = _set("age_at_entry", [1], 18)(table)
        return _set("age_at_entry", [2], 119)(table)

    model = _read_edited(tmp_path, edit)
    try:
        read = model.Data.model_point_table()
        assert read["duration_mth"].dtype == float
        df = _point(model, last).result_cf()
        assert len(df) == 1 and (df.drop(columns="av_pp") == 0.0).all().all()
        p = _point(model, _label(committed, "derived", 3, 66))
        assert p.duration_mth(0) == 66 and type(p.duration_mth(0)) is int
        assert frame_mismatches(
            _point(sec_model, _label(committed, "derived", 3, 66)).result_cf(),
            p.result_cf(), rtol=0, atol=0) == []
        late = _point(model, future)
        assert (late.t_entry(), late.proj_len(), late.pols_new_biz(120)) == (120, 473, 1.0)
        one = _point(model, first)
        assert (one.duration_mth_init(), one.av_pp_init() > 0.0,
                one.wd_cum_pp_init() > 0.0) == (1, True, True)
        assert len(_point(model, 1).result_cf()) == 353
        assert len(_point(model, 2).result_cf()) == 12
        for point in (1, 2):
            assert _point(model, point).check_pols_roll_fwd(), point
    finally:
        model.close()


# proj_len()'s refusal of a bond in force whose fund is exhausted, at any fund: the fund the
# generator computed, written to the CSV, may read back an ulp or two off it.
EXHAUSTED_REFUSAL = re.compile(
    r"ValueError: point_id \d+: av_pp_init is \S+, at or below depletion_threshold, "
    + re.escape(f"{THRESHOLD}: a bond in force whose fund is exhausted at the valuation date "
                "has nothing to project"))


def _every_state_months(end):
    """The S months a point whose S frame runs to ``end`` is restated at.

    By default the edges of its windows (USLIB-SEC-PLAN.md §5.2, T5): every month of the
    first policy year and the first anniversary, each anniversary and the month before it,
    through which the surrender bands, the allowance and the step turn, and the last two
    months of the frame, about the fund's exhaustion.  With ``UKLIB_SEC_FULL=1``, every
    month.  Each after 0, the twin's month.
    """
    if SEC_FULL:
        return list(range(1, end))
    months = {*range(1, 14), end - 2, end - 1,
              *(m for a in range(12, end, 12) for m in (a - 1, a))}
    return sorted(m for m in months if 0 < m < end)


def _states(s):
    """Each ``(S point, month)`` of :func:`_every_state_months` on every point of ``s``."""
    labels = s.Data.model_point_table().index
    return [(point_id, d) for key, point_id in zip(point_keys(s), labels)
            for d in _every_state_months(projection(s, key).proj_len())]


def _restated(root, s, states):
    """The twins of ``s``'s points and a row in force at each of ``states``, ``(S point,
    month)``, built by the generator out of ``s`` into a copy of the product directory:
    ``(folder, table)``."""
    spec = dataclasses.replace(SPEC, derived=tuple(states), future=(), derived_refs={})
    table, _ = build_sec_table(spec, s)
    return _sec_inputs(root, table), table


def _refused_in_force(folder, refs):
    """What ``Data`` and ``proj_len()`` refuse of the table in ``folder``, read with
    ``refs`` set first: ``Data``'s refusal, or each row's ``proj_len()``'s, by its label,
    each by the line that names it.  Each row is released once asked (:func:`_release`)."""
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
    """Every state ``ULB_UK_S`` reaches is a valid opening state, but an exhausted fund (T5).

    ``Data``'s rules and ``proj_len()``'s hold an opening state to what a bond in force can
    be, so they must accept each state the S model reaches: a rule exercised only on the
    rows the other tests choose could refuse a state S reaches elsewhere (D6).  So each point
    of S is restated in force by the generator at the edges of its windows, or with
    ``UKLIB_SEC_FULL=1`` at every month of its frame (:func:`_every_state_months`), into one
    table beside the twins: ``Data`` reads it, and no row's ``proj_len()`` refuses it
    (USLIB-SEC-PLAN.md §5.2, T5, precised at M10), but the states the product refuses by
    name, set aside and shown refused: a fund that opens above 0 and at or below
    ``depletion_threshold``, the rounding ``ULB_UK_S`` runs on past the threshold, which it
    reaches on its point 3 at month 323 and on the splice's variant 9 at the same month.

    The splice's switches move one of the states S reaches, the count, through the
    surrender rate: the fund and the withdrawals since issue are per policy and read no
    count, so its variants are what move them, the GMDB charged, the 7.5% cap binding and
    the rider beside the adviser charge.  So the test runs on each set of inputs on which
    those states differ (precised at M9), and asserts which states each moves:

    * S as shipped, its six points under its own References, the switches off, as T1 and the
      committed rows read it (``s_model``);
    * the splice's, its points and three variants under :data:`SPLICED_REFS`, the switches
      on (``spliced``).

    The cap's References, a ``mort_be_factor`` that caps mortality at 1, move only the
    count, to 0 once the cap binds, which ``Data`` reads as it reads every count, so that set
    is not run: the cap's test reads its rows in force.
    """
    sets = {"shipped": (s_model, {}), "spliced": (spliced[0], SPLICED_REFS)}
    found, states, set_aside = {}, {}, {}
    for tag, (s, refs) in sets.items():
        reached = _states(s)
        folder, rows = _restated(tmp_path / tag, s, reached)
        assert len(rows) == len(s.Data.model_point_table()) + len(reached)
        states[tag] = rows.set_index(["source_policy_id", "source_mth"])
        refused = _refused_in_force(folder, refs)
        exhausted = rows.index[(rows["duration_mth"] > 0)
                               & (rows["av_pp_init"] <= THRESHOLD)].tolist()
        set_aside[tag] = sorted((rows.at[label, "source_policy_id"],
                                 int(rows.at[label, "source_mth"])) for label in exhausted)
        for label in exhausted:
            point = int(rows.at[label, "point_id"])
            if not EXHAUSTED_REFUSAL.fullmatch(refused.pop(point, "")):
                found.setdefault(tag, []).append(f"{point} not refused as exhausted")
        if refused:
            found.setdefault(tag, []).append(
                f"{len(refused)} refused, first: {list(refused.items())[:5]}")
    assert not found, found
    assert set_aside["shipped"] == [("ULB-000003", 323)], set_aside
    assert set_aside["spliced"] == [("ULB-000003", 323), ("ULB-900009", 323)], set_aside
    shipped, splice = states["shipped"], states["spliced"]
    both = shipped.index.intersection(splice.index)
    apart = {c for c in ("policy_count", *STATE)
             if (shipped.loc[both, c] != splice.loc[both, c]).any()}
    assert apart == {"policy_count"}, apart


# ---------------------------------------------------------------------------
# The assumption tables
#
# Data checks each table before a value of it is read, in the cell the projection takes the
# table's extent from (UKLIB-SEC-PLAN.md §4; USLIB-SEC-PLAN.md §7.1, *Precised at M3*,
# item 9).  Each case is the shipped tables with one fault, read from a copy, refused by its
# Data cell alone, naming the file, the column and the lines at fault, the header line 1,
# and through a projection of the anchor cell, which reads both tables.  The surrender
# table holds policy years 1 to 11 on lines 2 to 12; the mortality table holds the male ages
# 18 to 120 on lines 2 to 104 and the female on lines 105 to 207, which its check reads as
# the file stands, where ULB_UK_S's reader sorts the table.


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
    return age - 16 if sex == "M" else age + 87


def _key_is(column, value):
    return lambda t: t[column] == value


def _dropped(where):
    return lambda table: table[~where(table)].reset_index(drop=True)


def _repeated(where):
    return lambda table: pd.concat([table, table[where(table)]], ignore_index=True)


MORT, SURR = "mort_table.csv", "surr_table.csv"
RATE = f"{MORT}: mort_rate must be a number from 0 to 1; it is not on line "
SURR_RATE = f"{SURR}: surr_rate must be a number from 0 to 1; it is not on line "


def _ages_apart(*faults):
    """The message of a mortality table whose sexes do not run one row an age, naming
    ``faults``: each repeat with how often it appears, each span a sex lacks."""
    return (f"{MORT}: the ages of each sex must run from 18 to 120, the table's first and "
            f"last, one row an age, none below 0; " + "; ".join(faults))


YEARS = (f"{SURR}: the policy years must run from 1, one row a year, without a gap or a "
         f"repeat; ")


# A table a reader cannot read, or whose value is not a number in its range, as (case, the
# file, its edit, the Data cell that refuses it, its message).  A value no point reads is
# refused too: the female rate at 18, which no point reaches, and the male at 120, which no
# frame does.
UNREADABLE = [
    ("a blank mortality rate", MORT, _written("mort_rate", float("nan"), _mort("M", 70)),
     "mort_age_first", RATE + f"[{_mort_line('M', 70)}]"),
    ("a text mortality rate", MORT, _written("mort_rate", "low", _mort("M", 66)),
     "mort_age_first", RATE + f"[{_mort_line('M', 66)}]"),
    ("an infinite mortality rate", MORT, _written("mort_rate", float("inf"),
                                                  _mort("M", 120)),
     "mort_age_first", RATE + f"[{_mort_line('M', 120)}]"),
    ("a negative mortality rate", MORT, _written("mort_rate", -0.001, _mort("F", 18)),
     "mort_age_first", RATE + f"[{_mort_line('F', 18)}]"),
    ("a mortality rate past 1", MORT, _written("mort_rate", 1.5, _mort("M", 80)),
     "mort_age_first", RATE + f"[{_mort_line('M', 80)}]"),
    ("two rows at fault", MORT, _then(_written("mort_rate", float("nan"), _mort("M", 18)),
                                      _written("mort_rate", float("nan"), _mort("F", 90))),
     "mort_age_first", RATE + f"[{_mort_line('M', 18)}, {_mort_line('F', 90)}]"),
    ("an age not whole", MORT, _written("age", 65.5, _mort("M", 65)),
     "mort_age_first",
     f"{MORT}: age must be a whole number; it is not on line [{_mort_line('M', 65)}]"),
    ("an age written as text", MORT, _written("age", "x", _mort("F", 18)),
     "mort_age_first",
     f"{MORT}: age must be a whole number; it is not on line [{_mort_line('F', 18)}]"),
    ("two blank male ages", MORT, _then(_written("age", float("nan"), _mort("M", 40)),
                                        _written("age", float("nan"), _mort("M", 90))),
     "mort_age_first", f"{MORT}: age must be a whole number; it is not on line [24, 74]"),
    ("an unknown sex", MORT, _written("sex", "X", _mort("F", 18)),
     "mort_age_first",
     f"{MORT}: sex must be M or F; it is not on line [{_mort_line('F', 18)}]"),
    ("an age missing", MORT, _dropped(_mort("M", 70)), "mort_age_first",
     _ages_apart("no line holds sex M, age 70")),
    ("an age twice", MORT, _repeated(_mort("F", 40)), "mort_age_first",
     _ages_apart(f"sex F, age 40 repeats on lines [{_mort_line('F', 40)}, 208]")),
    ("a sex missing", MORT, _dropped(lambda t: t["sex"] == "F"), "mort_age_first",
     _ages_apart("no line holds sex F, ages 18 to 120")),
    ("a sex shorter", MORT, _dropped(_mort("F", 120)), "mort_age_first",
     _ages_apart("no line holds sex F, age 120")),
    ("a blank surrender rate", SURR, _written("surr_rate", float("nan"),
                                              _key_is("policy_year", 3)),
     "surr_last_year", SURR_RATE + "[4]"),
    ("a surrender rate past 1", SURR, _written("surr_rate", 1.5, _key_is("policy_year", 11)),
     "surr_last_year", SURR_RATE + "[12]"),
    ("a negative surrender rate", SURR, _written("surr_rate", -0.1,
                                                 _key_is("policy_year", 1)),
     "surr_last_year", SURR_RATE + "[2]"),
    ("a text surrender rate", SURR, _written("surr_rate", "high", _key_is("policy_year", 2)),
     "surr_last_year", SURR_RATE + "[3]"),
    ("a policy year not whole", SURR, _written("policy_year", 2.5,
                                               _key_is("policy_year", 2)),
     "surr_last_year",
     f"{SURR}: policy_year must be a whole number; it is not on line [3]"),
    ("a policy year missing", SURR, _dropped(_key_is("policy_year", 3)), "surr_last_year",
     YEARS + "no line holds policy_year 3"),
    ("a policy year twice", SURR, _repeated(_key_is("policy_year", 4)), "surr_last_year",
     YEARS + "policy_year 4 repeats on lines [5, 13]"),
    ("no policy year 1", SURR, _dropped(_key_is("policy_year", 1)), "surr_last_year",
     YEARS + "no line holds policy_year 1"),
    # A key int64 holds inexactly, 2**53, is refused before the cast; 2**53 - 1 is cast
    # exactly and refused by the gap it leaves, which the check finds from the keys a table
    # holds, so that a key far from the rest costs no more than the rows.
    ("an age of 2**53", MORT, _written("age", 2.0 ** 53, _mort("M", 70)), "mort_age_first",
     f"{MORT}: age must be below 2**53 in size; it is not on line [{_mort_line('M', 70)}]"),
    ("an age of 2**53 - 1", MORT, _written("age", 2 ** 53 - 1, _mort("M", 70)),
     "mort_age_first",
     f"{MORT}: the ages of each sex must run from 18 to {2 ** 53 - 1}, the table's first and "
     f"last, one row an age, none below 0; no line holds sex M, age 70; no line holds sex "
     f"M, ages 121 to {2 ** 53 - 2}; no line holds sex F, ages 121 to {2 ** 53 - 1}"),
    ("a policy year of 2**53", SURR, _written("policy_year", 2.0 ** 53,
                                              _key_is("policy_year", 3)), "surr_last_year",
     f"{SURR}: policy_year must be below 2**53 in size; it is not on line [4]"),
    ("a policy year of 2**53 - 1", SURR, _written("policy_year", 2 ** 53 - 1,
                                                  _key_is("policy_year", 3)),
     "surr_last_year",
     YEARS + f"no line holds policy_year 3; no line holds policy years 12 to {2 ** 53 - 2}"),
]


@pytest.mark.parametrize("case, file, edit, cell, message", UNREADABLE,
                         ids=[c[0] for c in UNREADABLE])
def test_a_table_a_reader_cannot_read_is_refused_naming_its_rows(tmp_path, case, file, edit,
                                                                 cell, message):
    """``Data`` refuses an assumption table before a value of it is read (§4, T5).

    ``ULB_UK_S`` reads a blank rate as NaN, which its cap would keep and every flow carry;
    an infinite one, which the cap reads as certain death; a key that is not whole, gapped
    or repeated, as a ``KeyError`` only where a projection reaches it, or as a wrong row.
    Here the extent cell the projection asks first refuses each, naming the file, the
    column and the rows at fault (:data:`UNREADABLE`), and so does a projection of the
    anchor cell, which reads both tables.
    """
    model = _read_edited(tmp_path, lambda t: t, edits={file: edit})
    try:
        _refused(model.Data.cells[cell], message)
        _refused(_point(model, 1).result_cf, message)
    finally:
        model.close()


def test_a_read_beyond_the_mortality_table_is_refused_naming_its_point(tmp_path):
    """A read past the mortality table's ages is refused, naming the point.

    ``ULB_UK_S``'s lookup raises ``KeyError`` beyond the table, naming no point.  Above it,
    cover reads attained ages to ``omega_age - 1``, and ``proj_len()`` holds the limiting
    age to a year past the table's last age, so no frame reads past it: a table cut to ages
    20 to 100 refuses every point, naming the limiting age and the bound, and so does a
    limiting age raised to 122, two years past the shipped table's 120.  At 121, a year
    past it, cover reads ages to 120, all in the table, and the accumulation cell projects
    what ``ULB_UK_S`` projects at that limiting age, 672 months, in every column.  Below it, the mortality rate's read at an attained age the
    table does not rate raises ``ValueError`` naming the point and the age: the anchor
    cell issued at 18, the youngest the contract issues, under a table that starts at 20.
    The surrender table takes its last year for every later one, as ``ULB_UK_S`` does, so
    no read is beyond it.
    """
    cut = {MORT: _dropped(lambda t: (t["age"] > 100) | (t["age"] < 20))}
    model = _read_edited(tmp_path, lambda t: t, edits=cut)
    try:
        for point in (2, 6):
            _refused(_point(model, point).result_cf,
                     f"point_id {point}: omega_age must be above issue_age_min, 18, and at "
                     f"most 101, a year past mort_table.csv's last age, not 120")
    finally:
        model.close()
    low = {MORT: _dropped(lambda t: t["age"] < 20)}
    model = _read_edited(tmp_path / "low", _set("age_at_entry", [1], 18), edits=low)
    try:
        _refused(_point(model, 1).result_cf,
                 "point_id 1: mort_table.csv has no rate at attained age 18")
    finally:
        model.close()
    model = _read_edited(tmp_path / "omega", lambda t: t)
    try:
        model.Projection.omega_age = 122
        _refused(_point(model, 2).result_cf,
                 "point_id 2: omega_age must be above issue_age_min, 18, and at most 121, a "
                 "year past mort_table.csv's last age, not 122")
    finally:
        model.close()
    s = mx.read_model(model_path(TWIN), name=_name("s_omega"))
    sec = mx.read_model(model_path(SEC), name=_name("sec_omega"))
    try:
        for each in (s, sec):
            each.Projection.omega_age = 121
        sp, p = _point(s, 2), _row(sec, "twin", 2, 0)
        assert sp.proj_len() == p.proj_len() == 12 * (121 - 65)
        assert frame_mismatches(sp.result_cf(), p.result_cf(), rtol=0.0, atol=0.0) == []
    finally:
        sec.close()
        s.close()


def test_a_key_written_as_a_float_reads_as_ulb_uk_s_reads_it(sec_model, tmp_path):
    """A key written ``35.0`` is the key 35, in every table and in every extent.

    ``ULB_UK_S``'s lookups match a float key to the int the projection asks, so a table
    written by a tool that writes every number with a decimal point reads the same.  Each
    assumption table's keys and the model point table's ``duration_mth`` are written as
    floats, and every committed point projects what the committed tables project, exactly.
    """
    def as_float(column):
        return lambda table: table.assign(**{column: table[column].astype(float)})

    edits = {MORT: as_float("age"), SURR: as_float("policy_year")}
    model = _read_edited(tmp_path, as_float("duration_mth"), edits=edits)
    try:
        for point_id in _committed().index:
            for report in ("result_cf", "result_uf", "result_pols"):
                assert frame_mismatches(_point(sec_model, point_id).cells[report](),
                                        _point(model, point_id).cells[report](),
                                        rtol=0, atol=0) == [], (point_id, report)
    finally:
        model.close()


# ---------------------------------------------------------------------------
# T6 -- regeneration


def test_the_committed_sec_inputs_are_what_s_generates(s_model):
    """``model_point_table_sec.csv`` is what ULB_UK_S and its table generate today.

    Every row and column, the text cells and the two opening-state columns included: an
    edit to an S row the table copies or derives from, or to an S formula a row's state is
    read from, fails here until ``python tools/gen_sec_points.py ULB_UK_SEC`` regenerates
    it, in the same commit.  Text and integers compare exactly, and a float by its value, to
    1e-12, because the text the writer picks for a computed float depends on the platform's
    parser (§5).
    """
    assert check_generated(SEC, s_model=s_model) == []


# ---------------------------------------------------------------------------
# The product's own facts


def test_the_two_clocks_on_the_shipped_points(sec_model):
    """``t`` counts from the valuation date; ``duration_mth(t)`` from issue (D3, D4).

    On a twin of S's new business the two coincide, and its policies enter as new business
    at ``t = 0``.  The anchor cell in force 30 months is in policy year 3 at attained age 67
    at ``t = 0``, steps into policy year 4 at ``t = 6``, and has 323 months of its frame
    left, its fund exhausted at policy month 353 as from issue.  The GMDB point at 240 is in
    policy year 21, past the allowance's twenty years, its guarantee run out.  The point
    issued 13 months on has nothing in force and nothing to do before ``t = 13``, and a
    frame of 366 months.  The anchor cell in its last month before exhaustion has a one-month
    frame, in which its survivors leave.  A timing of the fund's is refused by the count's
    cell, and one of the count's by the fund's, rather than answered with another count or
    another fund: one numbering for the two families (the Projection docstring's *Codes*).
    """
    twin = _row(sec_model, "twin", 1, 0)
    assert [twin.duration_mth(t) for t in (0, 1, 352)] == [0, 1, 352]
    assert (twin.t_entry(), twin.pols_if_init(), twin.pols_new_biz(0), twin.pols_if(0)) == (
        0, 0.0, 1.0, 1.0)
    assert (twin.horizon_mths(), twin.fund_exhaust_mth(), twin.proj_len()) == (660, 353, 353)
    old = _row(sec_model, "derived", 1, 30)
    assert (old.duration_mth(0), old.duration(0), old.policy_year(0), old.age(0)) == (
        30, 2, 3, 67)
    assert (old.policy_year(5), old.policy_year(6)) == (3, 4)
    assert (old.proj_len(), old.fund_exhaust_mth(), old.t_entry(), old.pols_new_biz(0)) == (
        323, 353, 0, 0.0)
    assert old.pols_if(0) == old.pols_if_init() == old.policy_count()
    gmdb = _row(sec_model, "derived", 4, 240)
    assert (gmdb.policy_year(0), gmdb.allow_factor(0), gmdb.gmdb_guarantee_pp(0)) == (
        21, 1.5, 0.0)
    fut = _row(sec_model, "future", 4, -13)
    assert (fut.duration_mth(0), fut.t_entry(), fut.proj_len()) == (-13, 13, 366)
    assert not fut.is_active(12) and fut.is_active(13)
    assert (fut.pols_if_init(), fut.pols_new_biz(13), fut.pols_if(13)) == (0.0, 1.0, 1.0)
    assert (fut.av_pp(12), fut.av_pp(13), fut.gmdb_guarantee_pp(13)) == (
        0.0, 100000.0, 100000.0)
    last = _row(sec_model, "derived", 1, 352)
    assert (last.proj_len(), last.age(0), last.policy_year(0)) == (1, 94, 30)
    assert last.pols_maturity(0) > 0.0 and last.pols_if_at(1, _code(last, "BEF_NB")) == 0.0
    for timing in FUND_TIMINGS:
        _refused(lambda: old.pols_if_at(0, _code(old, timing)), "invalid timing")
    for timing in TIMINGS:
        _refused(lambda: old.av_pp_at(0, _code(old, timing)), "invalid timing")


def test_the_committed_rows_continue_their_s_points(sec_model, s_model):
    """Each committed row in force, or issued later, is its S point from its month on.

    T6 compares a float to 1e-12, which pins a small count only to that much of itself, so
    each committed row is compared with its S point frame by frame and cell by cell, at the
    shipped assumptions (USLIB-SEC-PLAN.md §7.1, *Precised at M3*, item 11): the four
    derived rows from their months, and the row issued 13 months on from S's issue month,
    all to 1e-9 relative with no absolute floor but on the residuals and in an exhausted
    frame's last month, every cell but those expense inflation moves (:func:`_continues_s`),
    which the inflation test holds.  The adviser charge's row at 66 ends a month before S's
    point does, where the depletion threshold drops S's month on a rounding.  The row read
    from S under a fund return of its own continues S under that return, which the
    shipped one replaces from the valuation date, and its own test holds it.
    """
    table = sec_model.Data.model_point_table()
    s_table = s_model.Data.model_point_table()
    found = []
    for point_id in table.index:
        kind, month = table.at[point_id, "row_kind"], int(table.at[point_id, "source_mth"])
        policy = table.at[point_id, "source_policy_id"]
        if kind == "twin" or (int(s_table.index[s_table["policy_id"] == policy][0]),
                              month) in SPEC.derived_refs:
            continue
        policy = table.at[point_id, "source_policy_id"]
        s_point = int(s_model.Data.model_point_table().index[
            s_model.Data.model_point_table()["policy_id"] == policy][0])
        found += [f"point {point_id}: {line}" for line in _continues_s(
            _point(s_model, s_point), _point(sec_model, point_id), month)]
    assert not found, found[:20]


# The committed row S reaches only under a fund return of its own: the GMDB point at its
# month 66, read from S run under a fund_return of 0 (SEC_SPECS' derived_refs).
IN_THE_MONEY, IN_THE_MONEY_REFS = (4, 66), {"fund_return": 0.0}


def test_a_committed_row_holds_the_guarantee_in_the_money(sec_model, tmp_path):
    """One committed row has the GMDB in the money and the rider charging (C2, T4).

    At ``ULB_UK_S``'s References no state it reaches has the rider charging: its GMDB
    point is in the money in its issue month alone, on the death benefit.  So the spec
    restates that point at its month 66 from S run under a ``fund_return`` of 0, a fund
    that has earned nothing since issue (:data:`IN_THE_MONEY`, the spec's
    ``derived_refs``), and C2 freezes the row with the rest.  Three things are held:

    * the row is S's state under that return: S read under it holds, at month 66, the
      row's count, fund, withdrawals since issue and allowance, of which only the fund is
      not S's at the shipped return, since no decrement, no scheduled withdrawal and no
      allowance reads a return;
    * set on this model too, that return gives the row S's path: it continues S's
      projection from month 66 on in every cell, over the whole of both frames, as the
      splice compares them (:func:`_continues_s`);
    * at today's References, which take over from the valuation date, the paths part in
      month 0's growth, 5% where S's history earned 0, so the comparison runs over what no
      return moves: the opening state at ``t = 0``, and the counts, whose decrements read
      no return, in every month both frames run but the shorter's last, where its
      survivors leave.  And the row opens in the money: the guarantee, 72,500, above the
      uplifted fund after charges, the rider charging from ``t = 0``, ``gmdb_charges``
      nonzero, and the death benefit paying the guarantee.
    """
    assert SPEC.derived_refs == {IN_THE_MONEY: IN_THE_MONEY_REFS}
    s_point, month = IN_THE_MONEY
    label = _label(_committed(), "derived", s_point, month)
    s = mx.read_model(model_path(TWIN), name=_name("s_refs"))
    shipped_s = mx.read_model(model_path(TWIN), name=_name("s_shipped"))
    sec = mx.read_model(model_path(SEC), name=_name("sec_refs"))
    try:
        for model in (s, sec):
            for ref, value in IN_THE_MONEY_REFS.items():
                setattr(model.Projection, ref, value)
        sp, row = _point(s, s_point), _point(sec_model, label)
        shipped = _point(shipped_s, s_point)
        opening = {"policy_count": sp.pols_if(month), "av_pp_init": sp.av_pp(month),
                   "wd_cum_pp_init": sp.wd_cum_pp(month - 1),
                   "allowance_cum_pp_init": sp.allowance_cum_pp(month - 1)}
        for column, value in opening.items():
            assert row.cells[column]() == pytest.approx(value, rel=1e-12), column
        assert row.policy_count() == pytest.approx(shipped.pols_if(month), rel=1e-12)
        assert row.av_pp_init() < shipped.av_pp(month) - 10000.0
        _sweep_s(sp)
        assert _continues_s(sp, _point(sec, label), month) == []
        assert row.av_pp(0) == row.av_pp_init()
        assert row.gmdb_guarantee_pp(0) == pytest.approx(
            sp.gmdb_guarantee_pp(month), rel=1e-12)
        both = min(row.proj_len(), sp.proj_len() - month) - 1
        assert both > 100
        for t in range(both):
            for count in ("pols_if", "pols_death", "pols_surr"):
                assert row.cells[count](t) == pytest.approx(
                    sp.cells[count](month + t), rel=1e-9, abs=0.0), (count, t)
        assert row.av_pp_at(0, _code(row, "AFT_GROWTH")) > sp.av_pp_at(month, "AFT_GROWTH")
        uplifted = row.db_uplift() * row.av_pp_at(0, _code(row, "AFT_CHARGE"))
        assert row.gmdb_guarantee_pp(0) == pytest.approx(72500.0, rel=1e-12)
        assert row.gmdb_guarantee_pp(0) > uplifted
        assert row.gmdb_charge_pp(0) > 0.0
        charges = row.result_cf()["gmdb_charges"]
        assert (charges > 0.0).sum() == 36 and (charges.iloc[:36] > 0.0).all()
        deaths = row.pols_death(0)
        assert row.claims(0, _code(row, "DEATH")) == pytest.approx(
            row.gmdb_guarantee_pp(0) * deaths, rel=1e-12)
    finally:
        sec.close()
        shipped_s.close()
        s.close()


def test_the_depletion_threshold_moves_point_3_alone(sec_model, s_model):
    """The threshold's effect on each S point: one month of point 3's, on 3.4e-15 (§6.6).

    ``ULB_UK_S`` ends a frame at the first month whose fund opens on 0 or less; this model
    at the first that opens at or below ``depletion_threshold``, half a pence.  Where the
    withdrawal cap draws a fund to nothing, the month closes it on a subtraction whose
    exact value is 0: on 0 exactly where nothing is cancelled beside the withdrawal, as on
    S's points 1, 4 and 5, but on a rounding of either sign where an adviser or a rider
    charge is, floored at 0.  S's point 3, its adviser charge beside its withdrawal, closes
    its fund on 3.4e-15 at the end of month 322, which S projects a month more: 0.019
    policies, a maintenance charge of about 18 pence against an AMC of 6e-20, and its
    survivors maturing a month later.  Points 2 and 6 never exhaust their funds, and run to
    the limiting age.

    So on every twin the frames, as ``FRAME`` and ``S_FRAME`` hold them, end together but
    on point 3, which ends a month early; there every cell agrees with S's in every month
    before its last, every cell of its last month but where its survivors go, which leave
    here and carry on in S, S's month 323 opens on a fund above 0 and at or below the
    threshold, and the departure moves the frame's net cash flow by S's last month alone.
    """
    table = sec_model.Data.model_point_table()
    twins = table.index[table["row_kind"] == "twin"].tolist()
    frames = {}
    for point_id in twins:
        p, s = _point(sec_model, point_id), _point(s_model, point_id)
        frames[point_id] = (p.proj_len(), s.proj_len())
        if p.proj_len() == s.proj_len():
            continue
        assert _compare(s, p, 0, TWIN_EXEMPT_DEFAULT | SPEC.exempt | {"proj_len"}) == []
        last = p.proj_len()
        assert s.av_pp(last) == 3.3861802251067274e-15, point_id
        moved = s.result_cf()["net_cf"].sum() - p.result_cf()["net_cf"].sum()
        assert moved == pytest.approx(s.net_cf(last), rel=1e-9, abs=0.0)
        assert -0.2 < s.net_cf(last) < -0.15
    assert frames == {p: (FRAME[p], S_FRAME[p]) for p in twins}, frames
    assert [p for p, (mine, theirs) in frames.items() if mine != theirs] == [3]


def test_a_fund_that_reaches_the_threshold_exactly_is_exhausted_there(tmp_path):
    """The search for the fund's exhaustion reads the threshold as exhausted, at or below.

    The anchor cell's fund opens month 352 on 326.68, the last month before the withdrawal
    cap draws it to 0.  With ``depletion_threshold`` set to exactly that fund, the search
    finds it exhausted at month 352, and the frame is 352 months; set to the float below it,
    the frame is the shipped 353.  A test of ``<`` where ``<=`` is meant moves the first by a
    month, which no shipped fund, a rounding of 1e-15 or a fund of hundreds, shows.
    """
    shipped = mx.read_model(model_path(SEC), name=_name("exact"))
    try:
        fund = _row(shipped, "twin", 1, 0).av_pp(352)
    finally:
        shipped.close()
    for threshold, frame in ((fund, 352), (math.nextafter(fund, 0.0), 353)):
        model = mx.read_model(model_path(SEC), name=_name("exact"))
        try:
            model.Projection.depletion_threshold = threshold
            p = _row(model, "twin", 1, 0)
            assert (p.fund_exhaust_mth(), p.proj_len()) == (frame, frame), threshold
            assert p.check_pols_roll_fwd() and p.pols_maturity(frame - 1) > 0.0
        finally:
            model.close()


def test_the_unit_fund_is_read_from_the_model_point(sec_model, tmp_path):
    """The fund a bond in force holds is the point's, not recomputed (UKLIB-SEC-PLAN.md K14).

    ``ULB_UK_S`` rebuilds the fund from the premium at its References, so a model that
    dropped ``av_pp_init`` and did the same would pass the splice, since S and the splice
    recompute it alike.  So the anchor cell in force 30 months is projected with a fund no
    fund return gives, 60% of what S carries there, as though the market had fallen a third
    since issue: the fund at ``t = 0`` is the column; each month after is the month before
    grown, charged and drawn down at the References, ``av_pp(t + 1) = max(0, UF'(t) - W(t))``
    from it; the AMC is levied on it; the withdrawals since issue and the allowance are the
    committed row's in every month but the last, where the smaller fund can no longer pay
    the withdrawal: the fund pays them, and does not set them; and the fund is exhausted,
    and the frame ends, years before the committed row's.  The fund is rounded to pence,
    so that the CSV holds it exactly.
    """
    row = _label(_committed(), "derived", 1, 30)
    fund = round(0.6 * _committed().at[row, "av_pp_init"], 2)
    model = _read_edited(tmp_path, _set("av_pp_init", [row], fund))
    try:
        p, base = _point(model, row), _point(sec_model, row)
        assert p.av_pp(0) == fund
        for t in (0, 1, 11, 100):
            grown = p.av_pp(t) * (1 + p.fund_return_mth() * (1 - p.tax_provision_rate()))
            charged = grown * (1 - p.amc_rate_mth() - p.further_costs_rate_mth())
            assert p.av_pp(t + 1) == pytest.approx(max(0.0, charged - p.wd_pp(t)),
                                                   rel=1e-12), t
            assert p.amc_pp(t) == pytest.approx(p.amc_rate_mth() * grown, rel=1e-12), t
        last = p.proj_len() - 1
        for t in range(last):
            assert p.wd_cum_pp(t) == base.wd_cum_pp(t), t
            assert p.allowance_cum_pp(t) == base.allowance_cum_pp(t), t
        assert p.wd_pp(last) < base.wd_pp(last)
        assert p.av_pp_at(last, _code(p, "AFT_WD")) == 0.0
        assert p.proj_len() < base.proj_len() - 100
        assert p.fund_exhaust_mth() == p.proj_len() + 30
    finally:
        model.close()


def test_the_withdrawals_since_issue_are_read_from_the_model_point(sec_model, tmp_path):
    """What a bond has withdrawn since issue is the point's, not its pattern's (K14; D6).

    ``ULB_UK_S`` rebuilds the withdrawals from the premium and its pattern, so a model that
    dropped ``wd_cum_pp_init`` and did the same would pass the splice, which rebuilds them
    alike; and the GMDB opens from them, ``max(0, P - wd_cum_pp_init)``.  So the GMDB point
    at 240, whose pattern has drawn the whole premium and whose guarantee is 0, is projected
    as though it had withdrawn only half of it, history no pattern of its gives: its
    guarantee opens at 50,000, above its fund's 41,263 uplifted, so the rider charges in the
    first month, the death benefit is the guarantee, and the guarantee runs down from 50,000
    by each later withdrawal.  And the adviser-charge point at 66, written with 10,000 more
    withdrawn, as though one withdrawal had been taken beside its pattern, carries 10,000
    more withdrawn in every month of its frame, and an excess gain of what that leaves above
    the allowance, which the committed row has none of in some months, while its fund and
    its frame are the committed row's: the withdrawals since issue move the tax machinery,
    not the units.
    """
    gmdb = _label(_committed(), "derived", 4, 240)
    adviser = _label(_committed(), "derived", 3, 66)
    more = _committed().at[adviser, "wd_cum_pp_init"] + 10000.0
    model = _read_edited(tmp_path, _then(_set("wd_cum_pp_init", [gmdb], HALF_WITHDRAWN),
                                         _set("wd_cum_pp_init", [adviser], more)))
    try:
        g, base = _point(model, gmdb), _point(sec_model, gmdb)
        assert (base.gmdb_guarantee_pp(0), g.gmdb_guarantee_pp(0)) == (0.0, 50000.0)
        assert g.gmdb_guarantee_pp(0) > g.db_uplift() * g.av_pp_at(0, _code(g, "AFT_CHARGE"))
        assert g.gmdb_charge_pp(0) > 0.0 and base.gmdb_charge_pp(0) == 0.0
        assert g.claims(0, _code(g, "DEATH")) == pytest.approx(
            50000.0 * g.pols_death(0), rel=1e-12)
        assert g.gmdb_guarantee_pp(1) == pytest.approx(
            50000.0 - g.wd_pp(0) - g.adviser_charge_pp(0), rel=1e-12)
        a, abase = _point(model, adviser), _point(sec_model, adviser)
        assert a.proj_len() == abase.proj_len()
        gained = []
        for t in range(a.proj_len()):
            assert a.av_pp(t) == abase.av_pp(t), t
            assert a.wd_cum_pp(t) == pytest.approx(abase.wd_cum_pp(t) + 10000.0,
                                                   rel=1e-12), t
            assert a.excess_gain_pp(t) == pytest.approx(max(
                0.0, abase.wd_cum_pp(t) + 10000.0 - abase.allowance_cum_pp(t)),
                rel=1e-12, abs=1e-9), t
            if abase.excess_gain_pp(t) == 0.0 < a.excess_gain_pp(t):
                gained.append(t)
        assert gained, "the 10,000 moves no month's excess gain off 0"
    finally:
        model.close()


def test_the_allowance_accrued_is_read_from_the_model_point(sec_model, s_model, tmp_path):
    """The allowance a bond has accrued since issue is the point's, not today's (K14; D6).

    ``ULB_UK_S`` rebuilds the 5% allowance from ``wd_allowance_rate`` and
    ``allowance_years``, every policy year from issue at the References of the day, so a
    model that dropped ``allowance_cum_pp_init`` and did the same would pass the splice,
    which runs S and this model at one rate.  Two edits show the column read:

    * ``wd_allowance_rate`` set to 4% at the valuation date.  The adviser-charge point at
      66 keeps the 30,000 it accrued through policy year 6 and accrues 4,000 a year from
      policy year 7, ``t = 6``; its excess gain at ``t = 0`` is what it has withdrawn,
      month 0's withdrawal at the new rate among it, less 30,000, about 415, where the
      allowance rebuilt at 4% from issue would make it about 6,415.  The GMDB point at 240,
      past the allowance's twenty years, keeps its 100,000 and accrues no more: about 333,
      where the rebuild would make it about 20,333.  The withdrawals since issue move on
      neither; the anchor pattern's withdrawals move from the valuation date on, the
      Reference being that pattern's rate too (``model-sec.md``).
    * The GMDB point's allowance written at 95,000, history no rate gives: its allowance is
      95,000 in every month, its excess gain 5,000 above the committed row's, and its fund,
      its withdrawals and its frame the committed row's: the allowance moves the tax
      machinery alone.
    * On an anniversary, at 4% from the valuation date: the column is measured before
      month 0's own events (D6, precised at M7), and the accrual of the year that begins
      in month 0 is one, so it reads the valuation date's rate.  The anchor cell restated
      at its month 12 opens with its first year's 5,000 and accrues 4,000 in month 0, as
      its twin, issued at ``t = 0``, and the row issued 13 months on accrue their first
      year's 4,000 in their issue month.  A column that held month 0's accrual too would
      open at 10,000, its second year at the old 5%.
    """
    adviser = _label(_committed(), "derived", 3, 66)
    gmdb = _label(_committed(), "derived", 4, 240)
    accrued = {adviser: 30000.0, gmdb: 100000.0}
    model = mx.read_model(model_path(SEC), name=_name("allowance"))
    try:
        model.Projection.wd_allowance_rate = 0.04
        for label, held in accrued.items():
            p = _point(model, label)
            assert p.allowance_cum_pp_init() == p.allowance_cum_pp(0) == held, label
            assert p.wd_cum_pp_init() == _point(sec_model, label).wd_cum_pp_init(), label
            assert p.wd_pp(0) == pytest.approx(0.04 * p.premium() / 12.0, rel=1e-12)
            assert p.excess_gain_pp(0) == pytest.approx(p.wd_cum_pp(0) - held, rel=1e-12)
            assert 0.0 < p.excess_gain_pp(0) < 1000.0, label
        a, g = _point(model, adviser), _point(model, gmdb)
        assert [a.allowance_cum_pp(t) for t in (0, 5, 6, 17, 18)] == pytest.approx(
            [30000.0, 30000.0, 34000.0, 34000.0, 38000.0], rel=1e-12)
        assert [g.allowance_cum_pp(t) for t in (0, 12, 100)] == [100000.0] * 3
    finally:
        model.close()
    spec = dataclasses.replace(SPEC, derived=((1, 12),), future=((1, 13),),
                               derived_refs={})
    rows, _ = build_sec_table(spec, s_model)
    model = mx.read_model(_sec_inputs(tmp_path / "anniversary", rows),
                          name=_name("anniversary"))
    try:
        model.Projection.wd_allowance_rate = 0.04
        restated = _row(model, "derived", 1, 12)
        assert restated.allowance_cum_pp_init() == 5000.0
        assert restated.allowance_cum_pp(0) == pytest.approx(9000.0, rel=1e-12)
        assert _row(model, "twin", 1, 0).allowance_cum_pp(0) == pytest.approx(4000.0,
                                                                               rel=1e-12)
        assert _row(model, "future", 1, -13).allowance_cum_pp(13) == pytest.approx(
            4000.0, rel=1e-12)
    finally:
        model.close()
    model = _read_edited(tmp_path, _set("allowance_cum_pp_init", [gmdb], 95000.0))
    try:
        p, base = _point(model, gmdb), _point(sec_model, gmdb)
        assert p.proj_len() == base.proj_len()
        for t in range(p.proj_len()):
            assert p.allowance_cum_pp(t) == 95000.0, t
            assert p.av_pp(t) == base.av_pp(t) and p.wd_cum_pp(t) == base.wd_cum_pp(t), t
            assert p.excess_gain_pp(t) == pytest.approx(base.excess_gain_pp(t) + 5000.0,
                                                        rel=1e-12), t
    finally:
        model.close()


def test_expense_inflation_runs_on_the_valuation_clock(sec_model, s_model):
    """Maintenance is in valuation-date pounds, for every point alike (D7).

    At the shipped 2.5%, the factor at ``t`` is ``1.025^(t // 12)`` on every point, whatever
    its duration, stepping on the valuation date's anniversaries.  So the anchor cell in
    force 30 months pays S's month-``30 + t`` maintenance with S's factor taken out and this
    model's put in: at ``t = 0`` S's less ``1.025^2``, the inflation S had applied since
    issue, and from ``t = 6``, where S's policy anniversary falls, a further 1.025 less until
    the valuation date's own.  And the point issued 13 months on pays S's maintenance with
    a year or two more of inflation: its factor at ``t`` is ``1.025^(t // 12)``, where S's at
    ``t - 13`` is ``1.025^((t - 13) // 12)``.  Acquisition is not inflated on either.  This is the only
    test that sees inflation run on the policy clock: the splice sets the rate to 0, and on
    a point issued at ``t = 0`` the clocks agree.
    """
    assert sec_model.Projection.inflation_rate == INFLATION
    p, s = _row(sec_model, "derived", 1, 30), _point(s_model, 1)
    fut = _row(sec_model, "future", 4, -13)
    for t in (0, 11, 12, 30):
        assert p.inflation_factor(t) == fut.inflation_factor(t) == (1 + INFLATION) ** (t // 12)
    for t in range(p.proj_len()):
        assert p.expenses(t) == pytest.approx(
            s.expenses(30 + t) / s.inflation_factor(30 + t) * p.inflation_factor(t)
            * p.pols_if(t) / s.pols_if(30 + t), rel=1e-12), t
    assert p.expenses(0) == pytest.approx(s.expenses(30) / (1 + INFLATION) ** 2, rel=1e-12)
    s4 = _point(s_model, 4)
    acq = s4.expense_acq
    for t in range(13, fut.proj_len()):
        issued = acq if t == 13 else 0.0
        maint = (fut.expenses(t) - issued) / fut.pols_if(t)
        want = (s4.expenses(t - 13) - issued) / s4.pols_if(t - 13)
        assert maint == pytest.approx(
            want * (1 + INFLATION) ** (t // 12 - (t - 13) // 12), rel=1e-12), t


def test_acquisition_is_charged_on_new_business_only(sec_model):
    """£300 per policy issued, in the issue month alone, uninflated.

    On every committed point, what ``expenses(t)`` holds beyond its maintenance part is
    ``300 * policy_count()`` in the issue month, ``t = -duration_mth``, and 0 in every other
    month, to 1e-9: the twins of S's new business bear it at ``t = 0``, the point issued 13
    months on at ``t = 13``, and the points already in force never, though on the valuation
    clock their row 0 is ``t = 0``.  ``ULB_UK_S`` charges it at ``t = 0`` on the count in
    force there, which on a point issued at the valuation date is the issued count, so the
    twins agree with S at any count.
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
        assert (issue in ts) == (sum(acq) > 0.0), point_id


def test_the_surrender_bands_and_the_step_run_on_the_policy_clock(sec_model):
    """The surrender table, the step and the allowance read the policy year, not ``t``.

    ``ULB_UK_S`` reads them at ``t // 12 + 1``, which is the policy year only on a point
    issued at ``t = 0``.  The anchor cell in force 30 months surrenders at the 5% band, the
    policy years 3 to 5, from ``t = 0`` and at the 8% band from ``t = 30``, policy month 60;
    its allowance accrues to policy year 20, ``t = 210``, and stays there, and the step to
    1.5 starts at ``t = 210``, policy month 240.  The point issued 13 months on reads its
    first band at its issue month, ``t = 13``.
    """
    p = _row(sec_model, "derived", 1, 30)
    assert [p.surr_rate_base(t) for t in (0, 29, 30, 89, 90)] == [0.05, 0.05, 0.08, 0.08,
                                                                 0.10]
    assert (p.allow_factor(209), p.allow_factor(210)) == (1.0, 1.5)
    assert p.allowance_cum_pp(209) == p.allowance_cum_pp(210) == pytest.approx(
        100000.0, rel=1e-12)
    assert p.allowance_cum_pp(0) == pytest.approx(15000.0, rel=1e-12)
    fut = _row(sec_model, "future", 4, -13)
    assert (fut.surr_rate_base(12), fut.surr_rate_base(13), fut.surr_rate_base(25)) == (
        0.0, 0.02, 0.03)


# ---------------------------------------------------------------------------
# The cap on mortality
#
# mort_rate caps the annual rate at 1, the bound second, as ULB_UK_S's does since M0.  At
# the shipped mort_be_factor of 0.8 the rate stays at or below 0.8 to the end of every
# frame, the table's 1.0 from age 114 times the factor, so neither the committed points nor
# the splice grid come near the cap, and Data refuses a table rate past 1.  So the cap
# binds through the factor: at 1.25, the accumulation cell's male rates pass 1 from
# attained age 111, policy month 552, where they stay to the limiting age.  S point 2
# alone, in a copy of S's table, under SPLICED_REFS and the factor.
CAPPED_REFS = {**SPLICED_REFS, "mort_be_factor": 1.25}
CAPPED_POINT = 2
CAPPED_MTH = 12 * (111 - 65)     # the first month at attained age 111, where it passes 1


def _capped_s(tmp_path):
    """ULB_UK_S on :data:`CAPPED_POINT` alone, under :data:`CAPPED_REFS`, read from a copy
    of S's inputs; the caller closes it."""
    s = mx.read_model(temp_inputs(tmp_path, model_path(TWIN),
                                  model_points=_s_table().loc[[CAPPED_POINT]]),
                      name=_name("capped_s"))
    for ref, value in CAPPED_REFS.items():
        setattr(s.Projection, ref, value)
    return s


def test_an_annual_mortality_past_1_is_capped_in_both_models(tmp_path):
    """Where the annual mortality product passes 1, both models' rate is 1.

    On :data:`CAPPED_POINT`, under :data:`CAPPED_REFS`, ``ULB_UK_S``'s product of the table
    rate and ``mort_be_factor`` passes 1 in month :data:`CAPPED_MTH` and stays past it to
    the end of the frame.  Both models cap it: ``mort_rate`` and the monthly rate,
    ``1 - (1 - q)^(1/12)``, are 1.0 in every one of those months, the float, not the int 1,
    which compares equal to it, and S's are floats below 1 in every month before.  So every
    policy in force at the start of the first capped month dies in it, none is in force
    after it, and every report holds finite floats alone.

    Four rows of the point, built from S by the generator: issued at the valuation date
    and 12 months after it, and restated in force in the month before the cap, opened with
    S's count and state there, each compared with S in every cell, the capped months
    included, as T1, T3 and the splice compare them, to 1e-9 relative with no absolute
    floor, but for the residuals, which keep the floor of 1e-9 (:func:`_compare`,
    USLIB-SEC-PLAN.md §5.1, step 6); and restated five months into the capped year, opened
    with S's state there and one policy, since S's count there is 0.  On each, the rate is
    1.0 from its first capped month, every policy in force there dies in it, and the count
    is 0.0 after it.
    """
    s = _capped_s(tmp_path / "s")
    sec = None
    try:
        sp = _point(s, CAPPED_POINT)
        end = sp.proj_len()
        product = [sp.data.mort_table().loc[(sp.sex(), sp.age(t)), "mort_rate"]
                   * sp.mort_be_factor for t in range(end)]
        cap = next(t for t in range(end) if product[t] > 1)
        assert (cap, sp.age(cap)) == (CAPPED_MTH, 111)
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
            future=((CAPPED_POINT, 12),), derived_refs={})
        rows, _ = build_sec_table(spec, s)
        rows.loc[rows["source_mth"] == cap + 5, "policy_count"] = 1.0
        sec = mx.read_model(_sec_inputs(tmp_path / "sec", rows), name=_name("capped"))
        for ref, value in CAPPED_REFS.items():
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
                assert _compare(sp, p, case[2], exempt | {"proj_len"}) == [], case
            capped, later = range(first, p.proj_len()), range(first + 1, p.proj_len())
            for rate in (p.mort_rate, p.mort_rate_mth):
                assert [(type(rate(t)), rate(t)) for t in capped] == (
                    [(float, 1.0)] * len(capped)), case
            assert p.pols_if(first) > 0.0 and p.pols_death(first) == p.pols_if(first), case
            assert [p.pols_if(t) for t in later] == [0.0] * len(later), case
            for report in ("result_cf", "result_uf", "result_pols"):
                frame = p.cells[report]()
                assert (frame.dtypes == "float64").all(), (case, report)
                assert np.isfinite(frame.to_numpy()).all(), (case, report)
    finally:
        if sec is not None:
            sec.close()
        s.close()


# A NaN sent to the bound written with its bound second, as (the bound, the Reference that
# feeds it, set to NaN on a model read for the test before it computes anything, the S
# point whose twin reads it, and the calls that must give the float NaN).  The cap reads
# mort_be_factor on every point, and the GMDB's charge reads the capped rate.  A bound
# written first would turn the NaN into the bound: a blank input read as certain death.
# proj_len() refuses a mort_be_factor that is not a number, so no report projects it; the
# calls here read no frame.  This form runs compiled unchanged, since a compiled ItemSpace
# takes the References when it is made (USLIB-SEC-PLAN.md §5.1, step 6, precised at M12).
NAN_BOUNDS = [
    ("the mortality cap, min(q, 1.0)", "mort_be_factor", 4,
     [("mort_rate", (0,)), ("mort_rate", (300,)), ("mort_rate_mth", (100,)),
      ("gmdb_charge_pp", (0,))]),
]


@pytest.mark.parametrize("bound, ref, s_point, calls", NAN_BOUNDS,
                         ids=[c[0] for c in NAN_BOUNDS])
def test_a_nan_that_reaches_a_bound_stays_nan(bound, ref, s_point, calls):
    """A NaN that reaches the bound written second stays NaN, and is not read as the bound.

    ``min`` keeps its first argument unless a later one compares smaller, in modelx and
    compiled alike, and no comparison with NaN holds, so with its bound first the cap would
    turn a NaN into 1.  It is written with its bound second, as ``ULB_UK_S`` writes it
    (:data:`NAN_BOUNDS`): the Reference that feeds it is set to NaN on a model read for the
    test, and every call must give the float NaN.  Every other ``min`` and ``max`` keeps
    ``ULB_UK_S``'s order, and ``Data`` refuses a blank the projection reads.
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


def _outside_cover_faults(p, where, months):
    """Where ``p``, an ItemSpace that has evaluated nothing, departs from OUTSIDE_COVER.

    Every cell of :data:`OUTSIDE_COVER`, ``pols_if_at`` at each timing, ``av_pp_at`` at each
    of the fund's and ``claims`` at each kind, at each of ``months``, every one outside
    cover, against :data:`OUTSIDE_COVER`; then whether any of :data:`IN_COVER_ONLY` was
    evaluated on the way, which only a fresh ItemSpace can say.  A cell that raises is
    reported as a fault too, so the scan goes on.
    """
    faults = []
    for t in months:
        calls = [(name, (t,), want) for name, want in OUTSIDE_COVER.items()]
        calls += [("pols_if_at", (t, _code(p, timing)), 0.0) for timing in TIMINGS]
        calls += [("av_pp_at", (t, _code(p, timing)), 0.0) for timing in FUND_TIMINGS]
        calls += [("claims", (t, _code(p, kind)), 0.0) for kind in KINDS]
        for name, args, want in calls:
            try:
                got = p.cells[name](*args)
            except Exception as err:        # reported, so the scan goes on
                faults.append(f"{where}: {name}{args} raised {_raised(err)}")
                continue
            if got != want or type(got) is not type(want):
                faults.append(f"{where}: {name}{args} = {got!r}, not {want!r}")
    read = {name: sorted(p.cells[name].keys()) for name in IN_COVER_ONLY
            if any(not p.is_active(key) for key in p.cells[name].keys())}
    if read:
        faults.append(f"{where}: evaluated outside cover: {read}")
    return faults


def _after_the_frame_faults(p, where):
    """Where ``p`` departs from what the month after its frame holds, ``t = proj_len()``.

    At the limiting age the month is outside cover, and :func:`_outside_cover_faults`
    holds it.  After a fund exhausted short of it the bond is in cover and holds no units:
    every count and every flow of :data:`FRAME_CELLS` is 0.0, the frame having ended, and
    the fund at or below ``depletion_threshold``.
    """
    t = p.proj_len()
    if not p.is_active(t):
        return _outside_cover_faults(p, where, [t])
    faults = []
    calls = [(name, (t,)) for name in FRAME_CELLS]
    calls += [("pols_if_at", (t, _code(p, timing))) for timing in TIMINGS]
    calls += [("claims", (t, _code(p, kind))) for kind in KINDS]
    for name, args in calls:
        got = p.cells[name](*args)
        if got != 0.0 or type(got) is not float:
            faults.append(f"{where}: {name}{args} = {got!r}, not 0.0")
    if not 0.0 <= p.av_pp(t) <= p.depletion_threshold:
        faults.append(f"{where}: av_pp({t}) = {p.av_pp(t)!r}, not an exhausted fund")
    return faults


def test_every_guarded_cell_holds_its_outside_cover_value(spliced):
    """Outside cover each cell holds :data:`OUTSIDE_COVER`'s value, and reads no rate.

    On every committed point, in every month before issue, on a model that evaluates nothing
    else.  So afterwards none of :data:`IN_COVER_ONLY` may hold a value outside cover at all:
    ``is_active``'s docstring promises that outside cover no count evaluates a rate, and no
    table is read at a policy year or an attained age the bond does not have.  And in the
    first month after the frame, ``t = proj_len()``, which the count's look-ahead reads: at
    the limiting age the same, and after a fund exhausted short of it, where the bond is in
    cover, no count and no flow, and a fund at or below the threshold
    (:func:`_after_the_frame_faults`).

    The committed table's one point issued after the valuation date is the GMDB point, on
    the anchor's pattern, so on it a cell tied to another pattern would hold zero before
    issue, guarded or not.  So the same scan runs on the splice's future rows, the core's
    or, with ``UKLIB_SEC_FULL=1``, all of them: the accumulation cell, the adviser charge,
    the custom pattern, the GMDB in the money and the cap binding among them.  Each row is
    made afresh first and released after.

    Several of these guards change no number the frame shows: once the counts are zero
    outside cover, every cash flow is too, and an unguarded value multiplies a zero count.
    They are held here because they are what the docstrings promise a caller, and because
    the C step needs them: a table read at a policy year or an age the bond does not have
    would wrap round in a compiled model rather than fail (USLIB-SEC-PLAN.md F4, R1).
    """
    faults = []
    model = mx.read_model(model_path(SEC), name=_name("cover"))
    try:
        table = model.Data.model_point_table()
        for key, point_id in zip(point_keys(model), table.index):
            p = projection(model, key)
            faults += _outside_cover_faults(p, f"point {point_id}", range(p.t_entry()))
            faults += _after_the_frame_faults(p, f"point {point_id}")
    finally:
        model.close()
    sec = spliced[1]
    futures = _selected(FUTURES, CORE_FUTURES)
    for s_point, k in futures:
        key = _row_key(sec, "future", s_point, -k)
        if key in sec.Projection.itemspaces:
            _release(sec, key)
        try:
            p = projection(sec, key)
            faults += _outside_cover_faults(p, _case_id("future", s_point, -k), range(k))
            faults += _after_the_frame_faults(p, _case_id("future", s_point, -k))
        finally:
            _release(sec, key)
    assert futures and not faults, (
        f"{len(faults)} faults outside cover, first:\n  " + "\n  ".join(faults[:20]))


def test_the_points_sum_row_by_row_into_a_block(spliced):
    """Row ``t`` is the same month on every point, so a block is its frames summed (D3).

    S point 1's twin, the point restated at month 12 and the point issued 12 months on,
    summed as ``run_sec.py --block`` sums them, are indexed 0..364 and equal S's frame added
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
    assert list(block.index) == list(range(365))
    assert frame_mismatches(expected, block) == []


# The labels an extract carries in the test below: the committed points' in reverse, from
# 112 down, so that a label is neither a position plus one nor in the order of the rows.
EXTRACT_LABELS = tuple(range(112, 100, -1))


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
    in ``result_cf``, ``result_uf`` and ``result_pols``, to 1e-12, and ``run_sec.py``, run
    beside that extract, prints the point without saying where it came from.  On every
    shipped row ``source_mth`` equals ``duration_mth``, so a formula that read the one for the
    other would pass every test that leaves ``duration_mth`` as generated.  And a refusal
    names the extract's label.
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
            for report in ("result_cf", "result_uf", "result_pols"):
                assert frame_mismatches(base.cells[report](), mine.cells[report](),
                                        rtol=1e-12, atol=1e-12) == [], (key, report)
            _release(model, key)
    finally:
        model.close()
    runner = folder.parent / "run_sec.py"
    shutil.copy(model_path(SEC).parent / "run_sec.py", runner)
    label = extract.index[extract["policy_id"] == "ULB-000003-M66"][0]
    out = _run_sec(runner, str(label))
    p = _row(sec_model, "derived", 3, 66)
    assert out.splitlines()[:2] == [
        f"model point {label}: ULB-000003-M66 - M65, premium 100,000 in 100 segments, AMC "
        f"1.00%, uplift 1.001, allowance_5pct withdrawals at 5.0% a year, adviser charge "
        f"0.50%",
        f"at the valuation date: in force 66 months: policy year 6, attained age 70, "
        f"{p.pols_if(0):.6f} in force, fund {p.av_pp_init():,.2f} a policy, "
        f"{p.wd_cum_pp_init():,.2f} withdrawn since issue"]
    last = extract.index[extract["policy_id"] == "ULB-000001-M352"][0]
    moved = _set("duration_mth", [last], 661)(extract)
    model = mx.read_model(_sec_inputs(tmp_path / "moved", moved), name=_name("moved"))
    try:
        _refused(_point(model, last).result_cf,
                 f"point_id {last}: duration_mth 661 is at or past the end of cover, "
                 f"policy month 660, the limiting age 120")
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
            f"{p.age(0)}, {p.pols_if(0):.6f} in force, fund {p.av_pp_init():,.2f} a "
            f"policy, {p.wd_cum_pp_init():,.2f} withdrawn since issue")


def test_run_sec_prints_a_point_and_the_block(sec_model):
    """The runner prints one point, saying where it came from, and the block (D8).

    Each mode in an interpreter of its own, as a user runs it, with exit code 0 and ASCII
    output, so that it prints on a Windows console under any code page.  The numbers are
    the model's.  The anchor cell, the runner's default, with its lines at the valuation
    date, each asserted whole, so that a longer number cannot pass for the one asserted,
    and its first twelve rows of cash flows and counts.  Point 4, the GMDB; point 8, the
    adviser charge restated in force at S's month 66, whose frame ends where its fund is
    exhausted; and point 11, to be issued 13 months on: each with the lines that say where
    its row came from and where it stands, which only the committed table's generator
    columns can say.  And the block: a line for each of the 12 points, in table order, its
    first twelve rows, which must be the committed points' frames summed row by row, as
    this test sums them, but the fund per policy, which summed is no amount, and those
    frames summed into projection years, each year's count the one in force in its first
    month.  Nothing else runs the runner on the committed table.
    """
    runner = model_path(SEC).parent / "run_sec.py"
    out = _run_sec(runner)
    assert out.splitlines()[:3] == [
        "model point 1: ULB-000001 (S's ULB-000001) - M65, premium 100,000 in 100 segments, "
        "AMC 1.00%, uplift 1.001, allowance_5pct withdrawals at 5.0% a year",
        "at the valuation date: issued at the valuation date, t = 0",
        "proj_len = 353 months from the valuation date (t = 0..352); the frame ends at "
        "policy month 353, the fund exhausted there"]
    anchor = _row(sec_model, "twin", 1, 0)
    assert anchor.result_cf().head(12).round(2).to_string() in out
    assert anchor.result_pols().head(12).round(6).to_string() in out
    adviser = _row(sec_model, "derived", 3, 66)
    for point_id, lines in (
            ("4", ["model point 4: ULB-000004 (S's ULB-000004) - M65, premium 100,000 in "
                   "100 segments, AMC 1.00%, uplift 1.001, allowance_5pct withdrawals at "
                   "5.0% a year, GMDB",
                   "at the valuation date: issued at the valuation date, t = 0",
                   "proj_len = 353 months from the valuation date (t = 0..352); the frame "
                   "ends at policy month 353, the fund exhausted there"]),
            ("8", ["model point 8: ULB-000003-M66 (S's ULB-000003 at its month 66) - M65, "
                   "premium 100,000 in 100 segments, AMC 1.00%, uplift 1.001, "
                   "allowance_5pct withdrawals at 5.0% a year, adviser charge 0.50%",
                   f"at the valuation date: {_standing(adviser)}",
                   "proj_len = 257 months from the valuation date (t = 0..256); the frame "
                   "ends at policy month 323, the fund exhausted there"]),
            ("11", ["model point 11: ULB-000004-F13 (S's ULB-000004, issued 13 months on) "
                    "- M65, premium 100,000 in 100 segments, AMC 1.00%, uplift 1.001, "
                    "allowance_5pct withdrawals at 5.0% a year, GMDB",
                    "at the valuation date: to be issued at t = 13, 13 months after the "
                    "valuation date",
                    "proj_len = 366 months from the valuation date (t = 0..365); the frame "
                    "ends at policy month 353, the fund exhausted there"])):
        assert _run_sec(runner, point_id).splitlines()[:3] == lines, point_id
    shown = _run_sec(runner, "2").splitlines()[2]
    assert shown == ("proj_len = 660 months from the valuation date (t = 0..659); the frame "
                     "ends at policy month 660, the limiting age")
    out = _run_sec(runner, "--block")
    table = sec_model.Data.model_point_table()
    points = [projection(sec_model, key) for key in point_keys(sec_model)]
    assert out.splitlines()[:len(points) + 1] == [
        "model points, t = 0 the valuation date for each:",
        *("  {:>2}  {:<15} {}; proj_len {}".format(
            point_id, table.at[point_id, "policy_id"], _standing(p), p.proj_len())
          for point_id, p in zip(table.index, points))]
    block = pd.concat([p.result_cf() for p in points]).groupby(level="t").sum()
    block = block.drop(columns="av_pp")
    assert block.head(12).round(2).to_string() in out
    years = pd.Index(block.index // 12 + 1, name="proj_year")
    annual = block.drop(columns="pols_if").groupby(years).sum()
    annual.insert(0, "pols_if", [block.at[12 * (y - 1), "pols_if"] for y in annual.index])
    assert annual.head(12).round(2).to_string() in out


# run_sec.py run as though it sat at /m/products/unit_linked_bond, in a products/ folder
# whose parent carries no build tool: the source compiled under that name, so that its own
# __file__ is it.
SHALLOW_RUN = """\
import sys
source = open(sys.argv[1], encoding="utf-8").read()
where = "/m/products/unit_linked_bond/run_sec.py"
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
    columns = [c for c in frames[0].columns if c != "av_pp"]
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
    as ``source_refs`` records them, point 12's ``under fund_return 0.0``, and no other
    row's line names any.  ``origin`` is read from the runner, which runs the model when
    imported, and run here on every row of the table the runner reads.
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
    assert space["origin"](12) == (
        " (S's ULB-000004 at its month 66, under fund_return 0.0)")


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

    A compiled model declares a defaulted parameter in its ``.pxd`` as ``long long x=*``,
    which the typing guard would read as a parameter of that name, and ``None`` is no C
    integer.  ``ULB_UK_S``'s one, ``claims``' ``kind=None``, is R12's total, which the C step
    made a code of its own, ``claims(t, ALL)``, as ``Term_UK_SEC``'s.
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
    outside the parentheses of the column, ``av_pp_at`` of ``av_pp_at(t, timing)``; a cell
    of two names, ``amc_rate(), amc_rate_mth()``, maps both.
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


# What only ULB_UK_S's docstrings may say: a reference into its Spaces, which the SEC pages
# would link to the wrong model; its clock, t counting policy months from issue; and a call
# of the cell this model renamed.
STALE = re.compile(r"~\.ULB_UK_S\.|``t`` counts \*\*policy months\*\* from issue"
                   r"|\bav_init_pp\(\)")


def test_the_docstrings_describe_the_valuation_clock(sec_model, s_model):
    """The docstrings say what this model is, and none says what only ULB_UK_S is.

    Whitespace is collapsed first, as ``test_model_conventions_uk`` collapses it, so that a
    phrase split across a line break still matches.  The model docstring names the
    valuation date, BasicTerm_SE, the policy clock, the SEC table, the threshold and the
    product.  The symbol map in the Projection docstring maps every cell running in force
    adds, which are exactly the cells ``ULB_UK_S`` lacks, and names nothing the model lacks:
    every name in it is a cell or a Reference.  No row of a simple table in any docstring
    puts text between two of its columns (:func:`_table_overruns`), which would drop the
    table from the rendered page.  And no docstring says what :data:`STALE` matches.
    """
    flat = {where: re.sub(r"\s+", " ", doc) for where, doc in _docs(sec_model)}
    for phrase in ("valuation date", "BasicTerm_SE", "duration_mth", TABLE,
                   "depletion_threshold", "unit-linked"):
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
    assert not stale, f"docstrings that describe ULB_UK_S: {stale}"


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
    reaches both models, and the two can never drift apart.  And every Reference of S's is
    the SEC model's at S's value, but those it adds, the threshold, the youngest issue age
    and the largest limiting age, and the C step's ``idx``, for S's ``point_id``, and codes,
    so that no assumption moves between the two (USLIB-SEC-PLAN.md §7.7, *Record — M9*,
    *References held to S's*).
    """
    assert sec_model.Data.input_dir() == s_model.Data.input_dir()
    files = {r: v for r, v in s_model.Data.refs.items() if r.endswith("_file")}
    assert {r: v for r, v in sec_model.Data.refs.items() if r.endswith("_file")} == {
        **files, "model_point_file": TABLE}
    plain = (bool, int, float, str)
    s_refs = {r: v for r, v in s_model.Projection.refs.items()
              if isinstance(v, plain) and r != "point_id"}
    sec_refs = {r: v for r, v in sec_model.Projection.refs.items()
                if isinstance(v, plain) and r != "idx" and r not in codes(sec_model.Projection)}
    assert sec_refs == {**s_refs, "depletion_threshold": THRESHOLD, "issue_age_min": 18,
                        "omega_age_max": 121}


def test_the_core_grid_reaches_every_branch(spliced, splice_records):
    """What the default run's T2 and T3 cases reach, which the full grid only multiplies.

    The default run thins the splice to a core (the module docstring), and this test is
    what keeps the thinning from costing a branch.  First, statically, over S's table with
    the variants, each property below holds of some core case: every withdrawal pattern,
    both sexes, the adviser charge, the GMDB rider, the 101% uplift and each variant; and
    each kind of valuation month: the first months, on an anniversary, in the month before
    one, mid-year, either side of each surrender band's edge, about policy year 21, and the
    last month of a frame, at exhaustion and at the limiting age.  And of some core future
    case: issued off the valuation anniversaries and on them, more than a year on, each
    pattern, the adviser charge, the GMDB and the variants.

    Then, on the splice's model, of some core row, each of :data:`AT_VALUATION` and
    :data:`IN_FRAME`, what no column of the table shows: both opening-state columns in use,
    and the GMDB opened from what is left of its guarantee and at 0; and every branch and
    both sides of every ``min`` and ``max`` the full grid reaches: the withdrawal's three
    bounds, the cap's two bases, the GMDB in and out of the money, the fund closed on 0 and
    on a rounding, the excess gain, the surrender table's last year, the surrender cap, the
    allowance step and its twenty years, and the frame's two ends.

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
        **{f"the {w} pattern": (lambda k, p, d, w=w: at(p, "wd_pattern") == w)
           for w in ("none", "allowance_5pct", "custom")},
        **{f"sex {x}": (lambda k, p, d, x=x: at(p, "sex") == x) for x in ("M", "F")},
        "an adviser charge": lambda k, p, d: at(p, "oac_rate") > 0.0,
        "the GMDB": lambda k, p, d: flag(p, "gmdb_flag"),
        "a 101% uplift": lambda k, p, d: at(p, "db_uplift") > 1.001,
        **{f"variant {v}": (lambda k, p, d, v=v: p == v) for v in VARIANTS},
        "in the second month": lambda k, p, d: d == 1,
        "on an anniversary": lambda k, p, d: k == "derived" and d % 12 == 0,
        "in the month before an anniversary": lambda k, p, d: d % 12 == 11,
        "mid-year": lambda k, p, d: d % 12 not in (0, 11),
        "either side of a band's edge": lambda k, p, d: d in (11, 12, 23, 24, 59, 60, 119,
                                                              120),
        "about policy year 21": lambda k, p, d: d in (239, 240, 241),
        "the last month before exhaustion": lambda k, p, d: (
            d == FRAME[p] - 1 and FRAME[p] < 12 * (120 - at(p, "age_at_entry"))),
        "the last month before the limiting age": lambda k, p, d: (
            d == FRAME[p] - 1 and FRAME[p] == 12 * (120 - at(p, "age_at_entry"))),
        "a frame S runs on past": lambda k, p, d: S_FRAME[p] > FRAME[p],
    }
    futures = {
        "issued off the anniversaries": lambda p, k: k % 12 != 0,
        "issued on them": lambda p, k: k % 12 == 0,
        "issued more than a year on": lambda p, k: k > 12,
        **{f"the {w} pattern": (lambda p, k, w=w: at(p, "wd_pattern") == w)
           for w in ("allowance_5pct", "custom")},
        "an adviser charge": lambda p, k: at(p, "oac_rate") > 0.0,
        "the GMDB": lambda p, k: flag(p, "gmdb_flag"),
        "a variant": lambda p, k: p in VARIANTS,
        "a frame S runs on past": lambda p, k: S_FRAME[p] > FRAME[p],
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
# The C step's representation (UKLIB-SEC-PLAN.md §6.6, *C*)
#
# Data decodes each model point's text into the number the projection reads, and turns
# each table into an array indexed by integers (USLIB-SEC-PLAN.md R5-R8); a timing and a
# kind are int codes, and the claims total is a code of its own (R9, R12); and the fund,
# the withdrawals since issue and the count are blocked by policy year (K12), which the
# depth test and the inline chain's test above hold.  These tests hold the representation
# in modelx, with no compiler, in seconds: the compiled section after the fingerprint
# holds the compiled model to modelx on it.


def test_the_all_total_is_s_total_bit_for_bit(sec_model, s_model):
    """``claims(t, ALL)`` is ``ULB_UK_S``'s ``claims(t)``, its ``sum``, to the last bit.

    S totals its two kinds with Python's ``sum``, which compensates, and the total here is
    written left to right from ``0.0`` (``Projection.claims``), which is ``sum``'s float
    wherever at most two kinds are non-zero in a month, and there are only two.  T1
    compares the totals to 1e-9; this compares them by ``float.hex``: on every committed
    point, in every month of its frame and the month after it, with ``sum`` of the row's
    own two kinds, both of them paying in some month, which is asserted, and the death
    benefit the guarantee in some month, on the committed row in the money
    (:data:`IN_THE_MONEY`), which is asserted too; and on every twin of S's new business,
    whose kinds are S's to the last bit, with S's ``claims(t)`` itself.  A row restated in
    force opens on a state read back from the CSV, which may part from S's by an ulp, so
    its total is held to its own kinds' ``sum``.
    """
    total = _code(sec_model.Projection, "ALL")
    death, surrender = (_code(sec_model.Projection, kind) for kind in KINDS)
    found, both, guaranteed = [], 0, 0
    table = sec_model.Data.model_point_table()
    for key, point_id in zip(point_keys(sec_model), table.index):
        p = projection(sec_model, key)
        wd = _code(p, "AFT_WD")
        for t in range(p.proj_len() + 1):
            kinds = [p.claims(t, death), p.claims(t, surrender)]
            both += kinds[0] != 0.0 and kinds[1] != 0.0
            guaranteed += (p.pols_death(t) > 0.0 and p.gmdb_guarantee_pp(t)
                           > p.db_uplift() * p.av_pp_at(t, wd))
            if p.claims(t, total).hex() != sum(kinds).hex():
                found.append(f"point {point_id}, t = {t}: {p.claims(t, total)!r}, the "
                             f"kinds' sum {sum(kinds)!r}")
    for point_id in table.index[table["row_kind"] == "twin"]:
        s, p = _point(s_model, point_id), _point(sec_model, point_id)
        for t in range(p.proj_len()):
            if p.claims(t, total).hex() != s.claims(t).hex():
                found.append(f"point {point_id}, t = {t}: {p.claims(t, total)!r}, S "
                             f"{s.claims(t)!r}")
    assert both and guaranteed, (both, guaranteed)
    assert not found, found[:10]


# One S point per value a decoded column can hold, as (the S point it changes, the columns
# it changes): each sex; each withdrawal pattern; the rider's flag each way; and the
# numbers ULB_UK_S reads with int, the issue age, written with a fraction, which int
# truncates, above .5 so that a decode that rounded would part, and the segments.
DECODED = [
    (1, {"sex": "F"}), (6, {"sex": "M"}),
    (1, {"wd_pattern": "none"}), (2, {"wd_pattern": "allowance_5pct"}),
    (1, {"wd_pattern": "custom", "wd_rate_custom": 0.04}),
    (1, {"gmdb_flag": True}), (4, {"gmdb_flag": False}),
    (1, {"age_at_entry": 65.7}), (2, {"n_segments": 7}),
]

# The cells each decoded point is compared on, ULB_UK_S's own, which read the text or the
# number themselves, and the decodes here, each against S's comparison of the text.
DECODING_CELLS = ("sex", "lives", "wd_pattern", "wd_rate", "gmdb_flag", "age_at_entry",
                  "n_segments", "premium", "db_uplift", "amc_rate", "further_costs_rate",
                  "tax_provision_rate", "oac_rate")
DECODES = {"mort_schedule": lambda s: ("M", "F").index(s.sex()),
           "wd_pattern_code": lambda s: ("none", "allowance_5pct",
                                         "custom").index(s.wd_pattern())}


def test_every_decode_is_ulb_uk_s_own_on_every_value(tmp_path):
    """``Data`` decodes every value a column can hold as ``ULB_UK_S``'s cells read it.

    A point of each case of :data:`DECODED` goes into a copy of S's table, and its twin,
    generated from it, into a copy of SEC's.  On each pair every cell of
    :data:`DECODING_CELLS` agrees exactly, in value and in type, the labels among them,
    and so does the mortality rate at ``t = 0`` and ``120``; each decode of :data:`DECODES`
    is S's comparison of the text, as an int; and the point's row of the mortality table,
    ``mort_schedule()``, holds S's rate for its sex at every age of the table, so that
    ``mort_rate`` is S's at every month the frame reads.  T1 and the splice see these
    through the cells that use them, at the values their points carry; this sees every
    value, on its own.
    """
    s_table = _s_table()
    rows = []
    for i, (base, changes) in enumerate(DECODED, start=1):
        row = s_table.loc[[base]].assign(**changes, policy_id=f"ULB-8{i:05d}")
        row.index = pd.Index([i], name="point_id")
        rows.append(row)
    table = pd.concat(rows)
    s = mx.read_model(temp_inputs(tmp_path / "s", model_path(TWIN), model_points=table),
                      name=_name("decoded_s"))
    sec = None
    found = []
    try:
        spec = dataclasses.replace(SPEC, derived=(), future=(), derived_refs={})
        twins, _ = build_sec_table(spec, s)
        sec = mx.read_model(_sec_inputs(tmp_path / "sec", twins), name=_name("decoded"))
        rates = s.Data.mort_table()["mort_rate"]
        array = sec.Data.mort_table_array()
        for (base, changes), key, label in zip(DECODED, point_keys(sec), table.index):
            case = f"S point {base} with {changes}"
            sp, p = projection(s, label), projection(sec, key)
            calls = [(cell, ()) for cell in DECODING_CELLS]
            calls += [("mort_rate", (t,)) for t in (0, 120)]
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
                want = rates.loc[(sp.sex(), a)]
                if array[row, a] != want:
                    found.append(f"{case}: row {row} at age {a} is {array[row, a]!r}, S's "
                                 f"rate {want!r}")
    finally:
        if sec is not None:
            sec.close()
        s.close()
    assert not found, found[:20]


def test_every_padded_array_holds_nan_and_no_reader_reads_it(sec_model, tmp_path):
    """The padding is NaN, and the mortality table's one reader refuses an age outside it.

    ``Data`` tables the mortality rates from age 0 and the surrender rates from policy year
    0, and pads what no file holds with NaN, as its docstring says, so that a read past a
    check, were one lost, would make every number after it NaN rather than another key's
    value: each sex's ages below the table's first, 18 as shipped, and year 0.  Inside,
    nothing is NaN.  And on the extract labelled otherwise than by position
    (:func:`_extract`), where a label read as ``idx + 1`` would name another point, the
    mortality rate refuses an attained age below the table, naming the point and the age,
    on a copy of the table that starts at 20, before it reads the array; the surrender rate
    reads a policy year of cover, 1 or more, at most the table's last.
    """
    data = sec_model.Data
    mort = data.mort_table_array()
    first, last = data.mort_age_first(), data.mort_age_last()
    assert mort.shape == (2, last + 1) and (first, last) == (18, 120)
    assert np.isnan(mort[:, :first]).all() and not np.isnan(mort[:, first:]).any()
    surr = data.surr_table_array()
    assert surr.shape == (data.surr_last_year() + 1,) == (12,) and np.isnan(surr[0])
    assert not np.isnan(surr[1:]).any()
    extract = _extract()
    anchor = extract.index[extract["policy_id"] == "ULB-000001"][0]
    cut = {MORT: _dropped(lambda t: t["age"] < 20)}
    model = mx.read_model(_sec_inputs(tmp_path, _set("age_at_entry", [anchor], 18)(extract),
                                      cut), name=_name("padded"))
    try:
        p = _point(model, anchor)
        position = list(extract.index).index(anchor)
        assert p.point_id() == anchor != point_keys(model)[position] + 1
        _refused(lambda: p.mort_rate(0),
                 f"point_id {anchor}: mort_table.csv has no rate at attained age 18")
        assert p.mort_rate(24) == pytest.approx(0.8 * model.Data.mort_table_array()[0, 20],
                                                rel=1e-15)
    finally:
        model.close()


# Data's readers, each a DataFrame or a path, which only the label accessors, the reports
# and Data's own cells read.  Every other Data cell is a vector or an int in the Data
# docstring's table of its vectors.
READERS = ("input_dir", "model_point_table", "mort_table", "mort_table_rows", "surr_table")


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
    vector is of R5's kind, int64 for ages, months, codes, flags, segments and rows,
    float64 for counts, amounts, rates and shares, as the table states it: a month held as
    a float64 reads the same numbers, and compiled reads a double through ``int()``,
    Python arithmetic, which neither C3 nor C5 sees.  Every cell is in the table, and every
    cell the table names is a cell.
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
    or a ``bool``.
    """
    space = sec_model.Projection
    reporting = reporting_cells(SEC, space)
    names = sorted(name for name, cell in space.cells.items()
                   if not cell.parameters and name not in reporting)
    assert {"point_id", "mort_schedule", "wd_pattern_code", "gmdb_flag", "age_at_entry",
            "n_segments", "duration_mth_init", "wd_rate", "proj_len"} <= set(names)
    found = []
    for key in point_keys(sec_model):
        proj = projection(sec_model, key)
        found += [f"{key}: {name} {type(value).__name__}" for name in names
                  if type(value := proj.cells[name]()) not in (int, float, bool)]
    assert not found, found


# Each label and the refusal its own formula makes of a value that is not its column's
# codes, which Data refuses first as it reads the table.
LABEL_REFUSALS = {"sex": "invalid sex", "lives": "invalid lives",
                  "wd_pattern": "invalid wd_pattern"}


def test_each_label_refuses_a_value_that_is_not_its_codes():
    """``sex()``, ``lives()`` and ``wd_pattern()`` return text or raise, in either engine.

    Each is a reporting cell, which a reader asks for and no projection cell reads, and the
    registry names them (``"reporting"``).  ``Data`` refuses a value other than the
    column's codes as it reads the table, so a label sees only text; but each refuses any
    other value itself, as ``ULB_UK_S``'s ``lives`` and ``wd_pattern`` do and the C step
    makes ``sex`` do, so that compiled each may return ``str`` and still raises where
    modelx raises (``uk_sec_support.labels_refusing_non_text``, C3).  So each is called in
    modelx on the committed model whose table is replaced, past ``Data``'s checks, by one
    holding the first point's column blank, as the number 7 and as a text no code is, and
    must refuse each, with its message; and the harness's own reading,
    ``labels_refusing_non_text``, which C3 asks, finds all three refusing.
    """
    for label, message in LABEL_REFUSALS.items():
        for value in (None, 7, "X"):
            model = mx.read_model(model_path(SEC), name=_name("label"))
            try:
                table = model.Data.model_point_table().astype({label: object})
                table.iloc[0, table.columns.get_loc(label)] = value
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


# The withdrawal patterns' codes, in the order ULB_UK_S's wd_rate compares the text.
WD_PATTERNS = ("NONE", "ALLOWANCE_5PCT", "CUSTOM")


def test_the_spec_sizes_each_cache_as_its_comment_derives():
    """``spec_sec.py`` gives each cache the size its comment derives from the contract.

    The spec check, C3, holds the compiled caches to the spec, and C4 at the contract's
    extremes holds the spec to the largest argument a projection reads; neither sees a
    size above the comment's.  So this reads the spec as mx2cy does, and the bounds of the
    contract from the model's own References, and holds each size to the comment's
    derivation from them: ``t`` to ``12 * (omega_age_max - issue_age_min) +
    future_horizon_mth + 2`` and ``y`` to ``omega_age_max - issue_age_min + 1``; every 2-D
    cache to one inner width, the widest of the timings' and the kinds', since gcc refuses
    two widths and MSVC, which builds the Windows leg, accepts them (USLIB-SEC-PLAN.md
    §7.2, *Record -- M15*); and the codes dense from 0, ints, as the caches index them,
    the count's timings and the fund's in one numbering, the kinds with the total, and the
    patterns.  A change to a bound or a size is derived again in the comment and here.
    """
    source, comment = _comment("spec_sec.py")
    for formula in ("12 * (omega_age_max - issue_age_min) + future_horizon_mth + 2",
                    "omega_age_max - issue_age_min + 1"):
        assert formula in comment, formula
    sizes = ast.literal_eval(source)["spaces"]["Projection"]["cells_param_size"]
    proj, data = _references("Projection"), _references("Data")
    timings = TIMINGS + FUND_TIMINGS
    for names in (timings, (*KINDS, "ALL"), WD_PATTERNS):
        values = [proj[name] for name in names]
        assert values == list(range(len(names))), (names, values)
        assert all(type(v) is int for v in values), (names, values)
    span = proj["omega_age_max"] - proj["issue_age_min"]
    t = 12 * span + data["future_horizon_mth"] + 2
    width = max(len(timings), len(KINDS) + 1)
    assert sizes == {"t": t, ("t", "timing"): (t, width), ("t", "kind"): (t, width),
                     "y": span + 1}, sizes
    assert len({size[1] for size in sizes.values() if isinstance(size, tuple)}) == 1
    assert (t, width, span + 1) == (1358, 8, 104)


def test_the_sample_raises_the_recursion_limit_its_comment_derives():
    """``sample_sec.py`` sets the recursion limit its comment derives, before the import.

    The export does not raise the recursion limit as modelx does (F7), so the sample sets
    it, and its comment records the measured need: the deepest cold call at the longest
    cover needs the limit the comment states in the export, and the reports and checks the
    sample runs in ascending ``t`` less, from a script's top level (measured at M10).  The
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
# cover; a timing and a kind no cell takes, and a timing of the other family, each refused
# by the cell, as ULB_UK_S's are, ValueError and its message.
NOT_HELD = [
    ("a label with a fraction",
     lambda t: _set("duration_mth", [10], 660)(t).rename(index={10: 10.5}),
     "result_cf", (), "model_point_table_sec.csv: point_id must be a whole number; [10.5] "
     "is not"),
    ("a label of 2**53", lambda t: _set("duration_mth", [10], 660)(t).rename(
        index={10: 2 ** 53}), "result_cf", (),
     f"model_point_table_sec.csv: point_id must be below 2**53 in size; [{2 ** 53}] is "
     f"not"),
    ("a timing no cell takes", None, "pols_if_at", (0, 9), "invalid timing"),
    ("a fund's timing in the count", None, "pols_if_at", (0, 7), "invalid timing"),
    ("a count's timing in the fund", None, "av_pp_at", (0, 0), "invalid timing"),
    ("a kind no cell takes", None, "claims", (0, 5), "invalid kind"),
]


@pytest.mark.parametrize("case, edit, cell, args, message", NOT_HELD,
                         ids=[c[0] for c in NOT_HELD])
def test_what_the_c_step_cannot_hold_or_take_is_refused(tmp_path, case, edit, cell, args,
                                                        message):
    """A label the vectors cannot hold, and a code no cell takes, are refused.

    ``Data.point_id`` reads each label by value, and refuses one that is not a whole
    number, or is ``2**53`` or more in size, naming every such label, when a refusal first
    names a point: here the anchor cell in its last month before exhaustion, the table's
    tenth row, moved past its cover, a refusal of ``proj_len()``'s, which meets the label's
    own first.  A projection that names no point reads no label, and runs.  And a timing or
    a kind no cell takes is refused by the cell, as ``ULB_UK_S``'s are, a timing of the
    fund's by the count's cell and one of the count's by the fund's (:data:`NOT_HELD`), on
    point 1: compiled, a code past a cache raises ``IndexError`` instead, which the
    compiled refusal test holds.
    """
    model = _read_edited(tmp_path, edit or (lambda t: t))
    try:
        keys = point_keys(model)
        p = projection(model, keys[9] if edit is not None else keys[0])
        _refused(lambda: p.cells[cell](*args), message)
        if edit is not None:
            assert len(projection(model, keys[0]).result_cf()) == 353
    finally:
        model.close()


# ---------------------------------------------------------------------------
# C2 -- the Phase 1 fingerprint


def test_the_phase_1_fingerprint_is_reproduced(sec_model):
    """Every committed point computes what the model computed when its E step ended (C2).

    The C step changes how the model is represented and no number it computes
    (UKLIB-SEC-PLAN.md U2, after USLIB-SEC-PLAN.md D2), so before it changed anything the
    model as M9 committed it was frozen below (USLIB-SEC-PLAN.md §5.4): for each point,
    each column of ``result_cf()`` and ``result_pols()``, its sum, its largest absolute
    value and its values at five fixed months, the frame's first and last and the three
    quartiles between.  Every later version must reproduce it, to 1e-12 relative, floored
    at 1e-12 of the column's own magnitude (``uk_sec_support.fingerprint_mismatches``),
    with the same points, frames and columns exactly.  ``python
    tools/gen_sec_fingerprint.py ULB_UK_SEC --check`` runs the same comparison from the
    command line.
    """
    assert fingerprint_mismatches(FINGERPRINT, sec_model) == []


# ULB_UK_SEC's fingerprint, frozen from the model as M9 committed it and committed alone,
# before its C step changed anything.  Each point is keyed by its point_id; each column
# holds (its sum over the frame, its largest absolute value, (its values at the months)).
# The block is written by tools/gen_sec_fingerprint.py, and is never edited by hand: a
# refreeze goes through the tool's --force, in a commit of its own that says why.
# BEGIN generated fingerprint: ULB_UK_SEC -- tools/gen_sec_fingerprint.py
FINGERPRINT = {
    1: {"rows": 353, "months": (0, 88, 176, 264, 352),
        "result_cf": {
            "pols_if": (125.10814443388098, 1.0, (
                1.0, 0.606817394834682, 0.24412431718181105, 0.06830338468356532,
                0.009551656268754137)),
            "av_pp": (20086002.470771767, 100000.0, (
                100000.0, 82170.47137088465, 60270.085698775154, 33369.38055035574,
                326.6776355940961)),
            "amc_charges": (8453.606182422343, 83.60494158557657, (
                83.60494158557657, 41.68749006169401, 12.301124055731366,
                1.9055586386923395, 0.002608735431110877)),
            "gmdb_charges": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "further_costs": (845.3606182422344, 8.360494158557655, (
                8.360494158557655, 4.1687490061694, 1.2301124055731365, 0.19055586386923393,
                0.00026087354311108763)),
            "tax_provisions": (8238.99577039962, 81.48247567296708, (
                81.48247567296708, 40.629176103689204, 11.988837293730032,
                1.8571825118941028, 0.0025425078622310885)),
            "withdrawals": (52127.54127024679, 416.6666666666667, (
                416.6666666666667, 252.8405811811175, 101.71846549242127, 28.45974361815222,
                3.12761290835883)),
            "claims_death": (15946.770562031725, 89.51197057563012, (
                83.64834654875966, 78.98130851830622, 44.25579564135806, 14.349780820723705,
                0.0)),
            "claims_surrender": (55598.63528837739, 466.89583997982606, (
                167.76635625401042, 343.7775168772437, 127.64402043615358,
                30.15629316691534, 0.0)),
            "unit_releases": (71529.4750106868, 556.1146682543699, (
                251.33113802100308, 422.6799229894378, 171.85560449345434,
                44.491738542263704, 0.0)),
            "death_strain": (15.930839722307663, 0.08942254802759268, (
                0.08356478176698347, 0.07890240611218534, 0.0442115840572959,
                0.014335445375346777, 0.0)),
            "expenses": (1049.4377648493182, 305.0, (
                305.0, 3.606575961590225, 1.7247063462049752, 0.5879457671456821,
                0.09773290007742431)),
            "net_cf": (7388.237577850718, 221.47862319619043, (
                -221.47862319619043, 38.0020116939916, 10.532206125469095,
                1.3032774261713107, -0.09512416464631343)),
        },
        "result_pols": {
            "pols_if": (125.10814443388098, 1.0, (
                1.0, 0.606817394834682, 0.24412431718181105, 0.06830338468356532,
                0.009551656268754137)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.23308306688840066, 0.0010134395411161223, (
                0.0008371773591205889, 0.0009628579030523697, 0.0007369281504909751,
                0.0004340025457378402, 0.00011838435482258846)),
            "pols_surr": (0.757610557071603, 0.00530348486938365, (
                0.0016807343010796071, 0.004195168630805765, 0.00212759786619122,
                0.0009129753322463378, 0.00012689587393475846)),
            "pols_maturity": (0.00930637603999679, 0.00930637603999679, (
                0.0, 0.0, 0.0, 0.0, 0.00930637603999679)),
        },
    },
    2: {"rows": 660, "months": (0, 164, 329, 494, 659),
        "result_cf": {
            "pols_if": (125.42483081695147, 1.0, (
                1.0, 0.2809706158215733, 0.016873099081866644, 4.6687924213440996e-05,
                2.67778774097971e-13)),
            "av_pp": (157101657.93167794, 466470.6809038593, (
                100000.0, 146704.99708000047, 215727.10834126588, 317222.9044652526,
                466470.6809038593)),
            "amc_charges": (13093.372093785225, 83.60494158557657, (
                83.60494158557657, 34.46178417175203, 3.043207227369638,
                0.012382292251651217, 1.0443172434447264e-10)),
            "gmdb_charges": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "further_costs": (1309.3372093785224, 8.360494158557655, (
                8.360494158557655, 3.4461784171752026, 0.30432072273696376,
                0.0012382292251651216, 1.0443172434447264e-11)),
            "tax_provisions": (12760.972651561755, 81.48247567296708, (
                81.48247567296708, 33.58690810814782, 2.965949789201495,
                0.012067944885028187, 1.017805320714741e-10)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (34066.61372231266, 127.39263126348163, (
                83.99751927229288, 113.84704931658251, 37.307987785496856,
                0.6453230793851668, 1.5730559696538488e-08)),
            "claims_surrender": (102608.60016180389, 611.6045678444266, (
                168.46666221279358, 360.17622297891563, 48.57808036275101,
                0.19102372488270883, 1.47283147541884e-09)),
            "unit_releases": (136641.1813029754, 728.4756946310697, (
                252.38026787941985, 473.9095389794976, 85.84879743117943,
                0.8357021258668914, 1.7187676327105642e-08)),
            "death_strain": (34.032581141167746, 0.12726536589757004, (
                0.08391360566661701, 0.11373331600056942, 0.037270717068424324,
                0.0006446784009841117, 1.5714844851685074e-11)),
            "expenses": (1052.8794529640932, 305.0, (
                305.0, 1.9366054859451725, 0.1643271135021634, 0.0006424702920993831,
                5.079662808822741e-12)),
            "net_cf": (12006.460059679965, 221.47897202009005, (
                -221.47897202009005, 32.41144536980629, 2.8416093967990506,
                0.011095143558567722, 8.363721668396483e-11)),
        },
        "result_pols": {
            "pols_if": (125.42483081695147, 1.0, (
                1.0, 0.2809706158215733, 0.016873099081866644, 4.6687924213440996e-05,
                2.67778774097971e-13)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.2381982030239761, 0.0010134395411161223, (
                0.0008371773591205889, 0.0007734422400623484, 0.0001723646168586238,
                2.0275131279561926e-06, 3.361017993585624e-14)),
            "pols_surr": (0.7618017969757932, 0.00530348486938365, (
                0.0016807343010796071, 0.0024493746820551947, 0.00022465739508258081,
                6.007694834502246e-07, 3.150023520512604e-15)),
            "pols_maturity": (2.3101857064160216e-13, 2.3101857064160216e-13, (
                0.0, 0.0, 0.0, 0.0, 2.3101857064160216e-13)),
        },
    },
    3: {"rows": 323, "months": (0, 80, 161, 241, 322),
        "result_cf": {
            "pols_if": (124.6875550619215, 1.0, (
                1.0, 0.6493447013934349, 0.29086518095860986, 0.10597188608082805,
                0.019895889181092436)),
            "av_pp": (17807067.087434106, 100000.0, (
                100000.0, 80608.66562000007, 57692.41517780617, 31276.36470478765,
                58.4600226991882)),
            "amc_charges": (8077.291223764241, 83.60494158557657, (
                83.60494158557657, 43.76117564678119, 14.029506789989464, 2.77101502355646,
                0.0009724208915912992)),
            "gmdb_charges": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "further_costs": (807.7291223764239, 8.360494158557655, (
                8.360494158557655, 4.376117564678118, 1.4029506789989463,
                0.27710150235564596, 9.724208915912991e-05)),
            "tax_provisions": (7872.234262255437, 81.48247567296708, (
                81.48247567296708, 42.65021734880861, 13.673341838878331, 2.700667687390842,
                0.0009477341905905065)),
            "withdrawals": (55980.96685835525, 458.4308185278949, (
                458.4308185278949, 292.4208228651504, 128.20214860380344, 45.53918999690413,
                1.1658354069288084)),
            "claims_death": (14683.290561684758, 88.23570479853991, (
                83.6133475823962, 75.62020499511678, 45.99425033754176, 17.278539247118292,
                6.2595445139209195e-19)),
            "claims_surrender": (51954.327904780606, 453.38087559085466, (
                167.69616181142175, 360.7416944944673, 145.51132826689397,
                43.84486504977654, 8.97860122553116e-19)),
            "unit_releases": (66622.94984452562, 540.0171379401842, (
                251.22597957605333, 436.2863548292493, 191.4596303024002, 61.10614301892567,
                1.5231892448229383e-18)),
            "death_strain": (14.6686219397434, 0.08814755724128892, (
                0.08352981776462237, 0.07554466033477368, 0.04594830203550119,
                0.017261277969147244, 6.253291222697534e-22)),
            "expenses": (1045.2849114427238, 305.0, (
                305.0, 3.7652038817869045, 2.004804322572257, 0.8682363737031283,
                0.18904006493180908)),
            "net_cf": (7017.337690381773, 221.47858823218806, (
                -221.47858823218806, 39.92042710465952, 11.978754165381705,
                1.8855173718841844, -0.18806764404021778)),
        },
        "result_pols": {
            "pols_if": (124.6875550619215, 1.0, (
                1.0, 0.6493447013934349, 0.29086518095860986, 0.10597188608082805,
                0.019895889181092436)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.22854001197278687, 0.0010134395411161223, (
                0.0008371773591205889, 0.0009402308366494505, 0.0008006795175322895,
                0.0005582594860070327, 0.00018467095095333054)),
            "pols_surr": (0.7520139240602456, 0.00530348486938365, (
                0.0016807343010796071, 0.004489800652035088, 0.0025356310233659667,
                0.0014180185192824682, 0.0002651542631712158)),
            "pols_maturity": (0.019446063966967887, 0.019446063966967887, (
                0.0, 0.0, 0.0, 0.0, 0.019446063966967887)),
        },
    },
    4: {"rows": 353, "months": (0, 88, 176, 264, 352),
        "result_cf": {
            "pols_if": (125.10814443388098, 1.0, (
                1.0, 0.606817394834682, 0.24412431718181105, 0.06830338468356532,
                0.009551656268754137)),
            "av_pp": (20086002.470771767, 100000.0, (
                100000.0, 82170.47137088465, 60270.085698775154, 33369.38055035574,
                326.6776355940961)),
            "amc_charges": (8453.606182422343, 83.60494158557657, (
                83.60494158557657, 41.68749006169401, 12.301124055731366,
                1.9055586386923395, 0.002608735431110877)),
            "gmdb_charges": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "further_costs": (845.3606182422344, 8.360494158557655, (
                8.360494158557655, 4.1687490061694, 1.2301124055731365, 0.19055586386923393,
                0.00026087354311108763)),
            "tax_provisions": (8238.99577039962, 81.48247567296708, (
                81.48247567296708, 40.629176103689204, 11.988837293730032,
                1.8571825118941028, 0.0025425078622310885)),
            "withdrawals": (52127.54127024679, 416.6666666666667, (
                416.6666666666667, 252.8405811811175, 101.71846549242127, 28.45974361815222,
                3.12761290835883)),
            "claims_death": (15946.839951395024, 89.51197057563012, (
                83.71773591205888, 78.98130851830622, 44.25579564135806, 14.349780820723705,
                0.0)),
            "claims_surrender": (55598.63528837739, 466.89583997982606, (
                167.76635625401042, 343.7775168772437, 127.64402043615358,
                30.15629316691534, 0.0)),
            "unit_releases": (71529.4750106868, 556.1146682543699, (
                251.33113802100308, 422.6799229894378, 171.85560449345434,
                44.491738542263704, 0.0)),
            "death_strain": (16.000229085606893, 0.1529541450662163, (
                0.1529541450662163, 0.07890240611218534, 0.0442115840572959,
                0.014335445375346777, 0.0)),
            "expenses": (1049.4377648493182, 305.0, (
                305.0, 3.606575961590225, 1.7247063462049752, 0.5879457671456821,
                0.09773290007742431)),
            "net_cf": (7388.168188487418, 221.54801255948965, (
                -221.54801255948965, 38.0020116939916, 10.532206125469095,
                1.3032774261713107, -0.09512416464631343)),
        },
        "result_pols": {
            "pols_if": (125.10814443388098, 1.0, (
                1.0, 0.606817394834682, 0.24412431718181105, 0.06830338468356532,
                0.009551656268754137)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.23308306688840066, 0.0010134395411161223, (
                0.0008371773591205889, 0.0009628579030523697, 0.0007369281504909751,
                0.0004340025457378402, 0.00011838435482258846)),
            "pols_surr": (0.757610557071603, 0.00530348486938365, (
                0.0016807343010796071, 0.004195168630805765, 0.00212759786619122,
                0.0009129753322463378, 0.00012689587393475846)),
            "pols_maturity": (0.00930637603999679, 0.00930637603999679, (
                0.0, 0.0, 0.0, 0.0, 0.00930637603999679)),
        },
    },
    5: {"rows": 353, "months": (0, 88, 176, 264, 352),
        "result_cf": {
            "pols_if": (125.10814443388098, 1.0, (
                1.0, 0.606817394834682, 0.24412431718181105, 0.06830338468356532,
                0.009551656268754137)),
            "av_pp": (20086002.470771767, 100000.0, (
                100000.0, 82170.47137088465, 60270.085698775154, 33369.38055035574,
                326.6776355940961)),
            "amc_charges": (8453.606182422343, 83.60494158557657, (
                83.60494158557657, 41.68749006169401, 12.301124055731366,
                1.9055586386923395, 0.002608735431110877)),
            "gmdb_charges": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "further_costs": (845.3606182422344, 8.360494158557655, (
                8.360494158557655, 4.1687490061694, 1.2301124055731365, 0.19055586386923393,
                0.00026087354311108763)),
            "tax_provisions": (8238.99577039962, 81.48247567296708, (
                81.48247567296708, 40.629176103689204, 11.988837293730032,
                1.8571825118941028, 0.0025425078622310885)),
            "withdrawals": (52127.54127024679, 416.6666666666667, (
                416.6666666666667, 252.8405811811175, 101.71846549242127, 28.45974361815222,
                3.12761290835883)),
            "claims_death": (16090.14811953251, 90.31677350787855, (
                84.4004295846626, 79.69143017331598, 44.65369989787378, 14.478799829101842,
                0.0)),
            "claims_surrender": (55598.63528837739, 466.89583997982606, (
                167.76635625401042, 343.7775168772437, 127.64402043615358,
                30.15629316691534, 0.0)),
            "unit_releases": (71529.4750106868, 556.1146682543699, (
                251.33113802100308, 422.6799229894378, 171.85560449345434,
                44.491738542263704, 0.0)),
            "death_strain": (159.30839722309432, 0.8942254802760261, (
                0.8356478176699275, 0.789024061121941, 0.4421158405730081,
                0.1433544537534837, 0.0)),
            "expenses": (1049.4377648493182, 305.0, (
                305.0, 3.606575961590225, 1.7247063462049752, 0.5879457671456821,
                0.09773290007742431)),
            "net_cf": (7244.860020349932, 222.23070623209335, (
                -222.23070623209335, 37.29189003898184, 10.134301868953383,
                1.1742584177931739, -0.09512416464631343)),
        },
        "result_pols": {
            "pols_if": (125.10814443388098, 1.0, (
                1.0, 0.606817394834682, 0.24412431718181105, 0.06830338468356532,
                0.009551656268754137)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.23308306688840066, 0.0010134395411161223, (
                0.0008371773591205889, 0.0009628579030523697, 0.0007369281504909751,
                0.0004340025457378402, 0.00011838435482258846)),
            "pols_surr": (0.757610557071603, 0.00530348486938365, (
                0.0016807343010796071, 0.004195168630805765, 0.00212759786619122,
                0.0009129753322463378, 0.00012689587393475846)),
            "pols_maturity": (0.00930637603999679, 0.00930637603999679, (
                0.0, 0.0, 0.0, 0.0, 0.00930637603999679)),
        },
    },
    6: {"rows": 780, "months": (0, 194, 389, 584, 779),
        "result_cf": {
            "pols_if": (141.46281753785348, 1.0, (
                1.0, 0.2557166290040634, 0.015062695651626325, 0.00016222624744435845,
                9.817890303605712e-11)),
            "av_pp": (170362094.9456848, 250000.0, (
                250000.0, 240171.74059455236, 224606.80232357036, 200056.63497955757,
                161334.30238009704)),
            "amc_charges": (28974.931978296107, 209.01235396394142, (
                209.01235396394142, 51.346733913075276, 2.8285089272444695,
                0.027133513237136482, 1.3242709086299902e-08)),
            "gmdb_charges": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "further_costs": (2897.493197829611, 20.90123539639414, (
                20.90123539639414, 5.134673391307527, 0.2828508927244469,
                0.0027133513237136476, 1.32427090862999e-09)),
            "tax_provisions": (28239.34979526015, 203.7061891824177, (
                203.7061891824177, 50.04320220325666, 2.7567020021066413,
                0.026444678871093506, 1.2906518448602899e-08)),
            "withdrawals": (88414.26096115842, 625.0, (
                625.0, 159.82289312753963, 9.414184782266453, 0.10139140465272403,
                6.13618143975357e-08)),
            "claims_death": (19878.18505348165, 68.6174636775936, (
                54.754271522123645, 57.68438980474769, 13.80797719176341,
                0.6129581284411646, 1.9870409051159608e-06)),
            "claims_surrender": (222812.38630335734, 1373.5955623546686, (
                420.3761905760418, 536.2292072096309, 45.30469107307908,
                0.42799564550951047, 1.8604400888822294e-07)),
            "unit_releases": (242670.71303011224, 1442.0044223935818, (
                475.07576252621527, 593.8559702513369, 59.098874081833735,
                1.0403414281680168, 2.171099858154917e-06)),
            "death_strain": (19.858326726752708, 0.06854891476282324, (
                0.05469957195016745, 0.05762676304169964, 0.013794183008753137,
                0.0006123457826584387, 1.9850558492664758e-09)),
            "expenses": (1174.7221235632162, 305.0, (
                305.0, 1.8980638652645194, 0.16597260021915858, 0.002653607374923441,
                2.384051126887973e-09)),
            "net_cf": (27780.35152800614, 203.53656711127587, (
                -96.04234560800874, 49.39104328476906, 2.6487421440165577,
                0.023867560079554602, 8.873602110145454e-09)),
        },
        "result_pols": {
            "pols_if": (141.46281753785348, 1.0, (
                1.0, 0.2557166290040634, 0.015062695651626325, 0.00016222624744435845,
                9.817890303605712e-11)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.08273092889717766, 0.00028013924230037664, (
                0.00021883337889949672, 0.00024000285425435197, 6.144202375320216e-05,
                3.063265195633131e-06, 1.2322898288195073e-11)),
            "pols_surr": (0.9172690710181202, 0.005552690702184706, (
                0.0016817744438009674, 0.0022332772738201294, 0.00020179606891375555,
                2.1410520034608856e-06, 1.1549304265190062e-12)),
            "pols_maturity": (8.470107432134305e-11, 8.470107432134305e-11, (
                0.0, 0.0, 0.0, 0.0, 8.470107432134305e-11)),
        },
    },
    7: {"rows": 323, "months": (0, 80, 161, 241, 322),
        "result_cf": {
            "pols_if": (96.33719437049606, 0.9017656115900125, (
                0.9017656115900125, 0.5016772690307959, 0.20385432424611377,
                0.05941438755059913, 0.009551656268754137)),
            "av_pp": (17167241.152528066, 94328.8643597054, (
                94328.8643597054, 77110.09729090484, 56066.83465082465, 30982.520323379395,
                326.6776355940961)),
            "amc_charges": (6112.241287035, 71.11647522361287, (
                71.11647522361287, 32.34205582962157, 9.555598950020462, 1.5390060098188338,
                0.002608735431110877)),
            "gmdb_charges": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "further_costs": (611.2241287035, 7.111647522361285, (
                7.111647522361285, 3.234205582962157, 0.955559895002046,
                0.15390060098188338, 0.00026087354311108763)),
            "tax_provisions": (5957.070748842624, 69.31105210358646, (
                69.31105210358646, 31.520992986442366, 9.313012415524462,
                1.4999354987558233, 0.0025425078622310885)),
            "withdrawals": (40139.64541050307, 375.7356714958385, (
                375.7356714958385, 209.0321954294983, 84.93930176921407, 24.755994812749638,
                3.12761290835883)),
            "claims_death": (13428.54900593099, 89.51197057563012, (
                85.37183903343711, 73.57499347164746, 37.68480336724505, 11.578199011007367,
                0.0)),
            "claims_surrender": (48612.564356990835, 466.89583997982606, (
                361.70124996856003, 266.5358084566353, 99.07410656694101,
                24.331769807702088, 0.0)),
            "unit_releases": (62027.69822904977, 556.1146682543699, (
                446.9878024495162, 340.03730043630316, 136.72126277797503,
                35.898402186330834, 0.0)),
            "death_strain": (13.415133872057453, 0.08942254802759268, (
                0.08528655248094678, 0.07350149197965969, 0.03764715621102988,
                0.011566632378627466, 0.0)),
            "expenses": (566.8385007400924, 4.508828057950062, (
                4.508828057950062, 2.9089591348101567, 1.4050771875710064,
                0.48678696115098335, 0.0907547134393749)),
            "net_cf": (5531.987652422852, 66.52236061318185, (
                66.52236061318185, 29.359595202831756, 8.112874606238426, 1.040652416289223,
                -0.08814597800826401)),
        },
        "result_pols": {
            "pols_if": (96.33719437049606, 0.9017656115900125, (
                0.9017656115900125, 0.5016772690307959, 0.20385432424611377,
                0.05941438755059913, 0.009551656268754137)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.20716005020759948, 0.0010134395411161223, (
                0.000906022848258677, 0.0009561313857188676, 0.0006749058592773089,
                0.0003775214884280706, 0.00011838435482258846)),
            "pols_surr": (0.6852991853424162, 0.00530348486938365, (
                0.0038424533198057626, 0.003467184747131894, 0.001776115429539278,
                0.0007941607940151273, 0.00012689587393475846)),
            "pols_maturity": (0.00930637603999679, 0.00930637603999679, (
                0.0, 0.0, 0.0, 0.0, 0.00930637603999679)),
        },
    },
    8: {"rows": 257, "months": (0, 64, 128, 192, 256),
        "result_cf": {
            "pols_if": (66.3501683410482, 0.7297983027773833, (
                0.7297983027773833, 0.41185977274518476, 0.19646274635736455,
                0.07670970017953539, 0.019895889181092436)),
            "av_pp": (11708901.56837345, 84220.69334213095, (
                84220.69334213095, 66886.2046011241, 47285.05480356625, 25120.8549170457,
                58.4600226991882)),
            "amc_charges": (3551.0161740264084, 51.38704083605311, (
                51.38704083605311, 23.03126944941016, 7.766691505946419, 1.6110783011227612,
                0.0009724208915912992)),
            "gmdb_charges": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "further_costs": (355.10161740264084, 5.138704083605311, (
                5.138704083605311, 2.303126944941016, 0.7766691505946418,
                0.1611078301122761, 9.724208915912991e-05)),
            "tax_provisions": (3460.867067507611, 50.08248586052269, (
                50.08248586052269, 22.446578121320883, 7.569519692145776, 1.570178101782537,
                0.0009477341905905065)),
            "withdrawals": (29412.659409186912, 329.7525941815531, (
                329.7525941815531, 183.11331737003442, 85.73926366826822,
                32.767175814479785, 1.1658354069288084)),
            "claims_death": (9167.046441644075, 82.96844466529996, (
                81.05562711820652, 57.35733782725275, 33.537940657542045,
                10.994837371405556, 6.2595445139209195e-19)),
            "claims_surrender": (32830.921576145134, 423.7528009640277, (
                423.7528009640277, 239.27341332727374, 80.35500989181888, 25.39419204418393,
                8.97860122553116e-19)),
            "unit_releases": (41988.81012923611, 504.72745342976845, (
                504.72745342976845, 296.57345111673703, 113.85944611313961,
                36.378045562071605, 1.5231892448229383e-18)),
            "death_strain": (9.157888553089977, 0.08288555910618464, (
                0.08097465246573186, 0.05730003778945699, 0.03350443622131704,
                0.01098385351788646, 6.253291222697534e-22)),
            "expenses": (382.16334834555596, 3.6489915138869167, (
                3.6489915138869167, 2.329907647215841, 1.2574446256121572,
                0.5693799053785342, 0.16708387191996102)),
            "net_cf": (3159.694937127763, 47.65707466970046, (
                47.65707466970046, 20.644061764404864, 6.475742444112945,
                1.0307145422263404, -0.16611145102836972)),
        },
        "result_pols": {
            "pols_if": (66.3501683410482, 0.7297983027773833, (
                0.7297983027773833, 0.41185977274518476, 0.19646274635736455,
                0.07670970017953539, 0.019895889181092436)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.16858562495144322, 0.0010055654508002582, (
                0.0009643754586173845, 0.0008603855581737177, 0.00071347864024064,
                0.00044374776521338656, 0.00018467095095333054)),
            "pols_surr": (0.5417666138589722, 0.005046724985241304, (
                0.005046724985241304, 0.003592796745407615, 0.0017111639430498716,
                0.0010259255506871758, 0.0002651542631712158)),
            "pols_maturity": (0.019446063966967887, 0.019446063966967887, (
                0.0, 0.0, 0.0, 0.0, 0.019446063966967887)),
        },
    },
    9: {"rows": 113, "months": (0, 28, 56, 84, 112),
        "result_cf": {
            "pols_if": (4.880379558376014, 0.10798572023705956, (
                0.10798572023705956, 0.06307276672972552, 0.03545928581791165,
                0.019006408829758254, 0.009551656268754137)),
            "av_pp": (2449680.1404988756, 41262.727529206815, (
                41262.727529206815, 32010.243298576737, 22132.08965723876,
                11585.957728815809, 326.6776355940961)),
            "amc_charges": (118.6807258584273, 3.725256740038522, (
                3.725256740038522, 1.6879625420915456, 0.6561216266426783,
                0.18410430933610272, 0.002608735431110877)),
            "gmdb_charges": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "further_costs": (11.868072585842727, 0.3725256740038521, (
                0.3725256740038521, 0.16879625420915456, 0.06561216266426782,
                0.01841043093361027, 0.00026087354311108763)),
            "tax_provisions": (115.66779635520616, 3.630684214820531, (
                3.630684214820531, 1.6451104942411943, 0.6394647668845795,
                0.1794304812881467, 0.0025425078622310885)),
            "withdrawals": (2032.6392387863837, 44.99405009877482, (
                44.99405009877482, 26.28031947071897, 14.774702424129854, 7.919337012399273,
                3.12761290835883)),
            "claims_death": (881.3072696170057, 23.31424108437509, (
                23.31424108437509, 12.704368507664205, 5.928857367526921, 2.176034302165481,
                0.0)),
            "claims_surrender": (1874.8416566028843, 59.160658170387016, (
                59.160658170387016, 26.698432958945137, 10.303203786961545,
                2.833376321726749, 0.0)),
            "unit_releases": (2755.2684993771154, 82.45160830462787, (
                82.45160830462787, 39.390109789778506, 16.226138220055372,
                5.007236763450507, 0.0)),
            "death_strain": (0.8804268427741346, 0.02329095013423829, (
                0.02329095013423829, 0.012691676830831975, 0.0059229344330931745,
                0.002173860441723518, 0.0)),
            "expenses": (26.01645001860266, 0.5399286011852978, (
                0.5399286011852978, 0.33132912772708933, 0.19570208389083552,
                0.11296323702163677, 0.059643549078577635)),
            "net_cf": (91.7838489970505, 3.162037188718986, (
                3.162037188718986, 1.3439417375336242, 0.45449660831874955,
                0.06896721187274243, -0.05703481364746676)),
        },
        "result_pols": {
            "pols_if": (4.880379558376014, 0.10798572023705956, (
                0.10798572023705956, 0.06307276672972552, 0.03545928581791165,
                0.019006408829758254, 0.009551656268754137)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.033479096005451014, 0.0005688683565531671, (
                0.0005688683565531671, 0.00040076698181570935, 0.00027210359099290315,
                0.00019415712311678215, 0.00011838435482258846)),
            "pols_surr": (0.06520024819161176, 0.0014449657996783438, (
                0.0014449657996783438, 0.0008430604197367447, 0.00047333611081348657,
                0.00025306141313168165, 0.00012689587393475846)),
            "pols_maturity": (0.00930637603999679, 0.00930637603999679, (
                0.0, 0.0, 0.0, 0.0, 0.00930637603999679)),
        },
    },
    10: {"rows": 1, "months": (0,),
        "result_cf": {
            "pols_if": (0.009551656268754137, 0.009551656268754137, (
                0.009551656268754137,)),
            "av_pp": (326.6776355940961, 326.6776355940961, (
                326.6776355940961,)),
            "amc_charges": (0.002608735431110877, 0.002608735431110877, (
                0.002608735431110877,)),
            "gmdb_charges": (0.0, 0.0, (
                0.0,)),
            "further_costs": (0.00026087354311108763, 0.00026087354311108763, (
                0.00026087354311108763,)),
            "tax_provisions": (0.0025425078622310885, 0.0025425078622310885, (
                0.0025425078622310885,)),
            "withdrawals": (3.12761290835883, 3.12761290835883, (
                3.12761290835883,)),
            "claims_death": (0.0, 0.0, (
                0.0,)),
            "claims_surrender": (0.0, 0.0, (
                0.0,)),
            "unit_releases": (0.0, 0.0, (
                0.0,)),
            "death_strain": (0.0, 0.0, (
                0.0,)),
            "expenses": (0.047758281343770685, 0.047758281343770685, (
                0.047758281343770685,)),
            "net_cf": (-0.04514954591265981, 0.04514954591265981, (
                -0.04514954591265981,)),
        },
        "result_pols": {
            "pols_if": (0.009551656268754137, 0.009551656268754137, (
                0.009551656268754137,)),
            "pols_new_biz": (0.0, 0.0, (
                0.0,)),
            "pols_death": (0.00011838435482258846, 0.00011838435482258846, (
                0.00011838435482258846,)),
            "pols_surr": (0.00012689587393475846, 0.00012689587393475846, (
                0.00012689587393475846,)),
            "pols_maturity": (0.00930637603999679, 0.00930637603999679, (
                0.00930637603999679,)),
        },
    },
    11: {"rows": 366, "months": (0, 91, 182, 273, 365),
        "result_cf": {
            "pols_if": (125.10814443388098, 1.0, (
                0.0, 0.6603425223292329, 0.2651512626976938, 0.07379851086878253,
                0.009551656268754137)),
            "av_pp": (20086002.470771767, 100000.0, (
                0.0, 84386.03112327744, 62181.746040435435, 34715.872260838034,
                326.6776355940961)),
            "amc_charges": (8453.606182422343, 83.60494158557657, (
                0.0, 46.58775399368823, 13.784421996058198, 2.141941611855725,
                0.002608735431110877)),
            "gmdb_charges": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "further_costs": (845.3606182422342, 8.360494158557655, (
                0.0, 4.658775399368823, 1.3784421996058198, 0.21419416118557247,
                0.00026087354311108763)),
            "tax_provisions": (8238.995770399622, 81.48247567296708, (
                0.0, 45.405037781926666, 13.434478975265451, 2.087564466536986,
                0.0025425078622310885)),
            "withdrawals": (52127.5412702468, 416.6666666666667, (
                0.0, 275.14271763718034, 110.47969279070576, 30.74937952865939,
                3.12761290835883)),
            "claims_death": (15946.839951395024, 89.51197057563012, (
                0.0, 80.55700949176739, 49.60285028549982, 14.691930104939772, 0.0)),
            "claims_surrender": (55598.63528837738, 466.89583997982606, (
                0.0, 384.29242699545233, 143.0661711935615, 33.933170812955176, 0.0)),
            "unit_releases": (71529.4750106868, 556.1146682543699, (
                0.0, 464.76895995426094, 192.6194681820728, 48.61042366504286, 0.0)),
            "death_strain": (16.000229085606897, 0.1529541450662163, (
                0.0, 0.08047653295879972, 0.049553296988505864, 0.014677252852086067, 0.0)),
            "expenses": (1069.6991371892937, 305.125, (
                0.0, 3.924698744170462, 1.9200904380486428, 0.6352470274784989,
                0.1001762225793599)),
            "net_cf": (7367.906816147444, 221.67301255948965, (
                0.0, 42.58257871655897, 11.814778261021049, 1.49201733152514,
                -0.09756748714824903)),
        },
        "result_pols": {
            "pols_if": (125.10814443388098, 1.0, (
                0.0, 0.6603425223292329, 0.2651512626976938, 0.07379851086878253,
                0.009551656268754137)),
            "pols_new_biz": (1.0, 1.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.23308306688840064, 0.0010134395411161223, (
                0.0, 0.0009561553377004275, 0.0008004013359907787, 0.0004269072124835987,
                0.00011838435482258846)),
            "pols_surr": (0.757610557071603, 0.00530348486938365, (
                0.0, 0.004565843504933632, 0.0023108523855629773, 0.0009869909245603806,
                0.00012689587393475846)),
            "pols_maturity": (0.00930637603999679, 0.00930637603999679, (
                0.0, 0.0, 0.0, 0.0, 0.00930637603999679)),
        },
    },
    12: {"rows": 203, "months": (0, 50, 101, 151, 202),
        "result_cf": {
            "pols_if": (64.32106673433111, 0.7297983027773833, (
                0.7297983027773833, 0.4757155494719856, 0.27141264105581586,
                0.14691593552581783, 0.06307276672972552)),
            "av_pp": (7358115.43354178, 67232.39320459412, (
                67232.39320459412, 53349.19837271426, 37560.10297602922, 20142.03622156947,
                149.72730947765814)),
            "amc_charges": (2566.956457660336, 41.021672916836174, (
                41.021672916836174, 21.218134257191263, 8.522927479939415,
                2.474025806038603, 0.007895412964189268)),
            "gmdb_charges": (86.71471404079026, 4.863265579721114, (
                4.863265579721114, 0.0, 0.0, 0.0, 0.0)),
            "further_costs": (256.6956457660336, 4.102167291683617, (
                4.102167291683617, 2.121813425719126, 0.8522927479939415,
                0.24740258060386028, 0.0007895412964189267)),
            "tax_provisions": (2501.789525213405, 39.98026195723302, (
                39.98026195723302, 20.679472715947753, 8.306557218699561,
                2.4112180898839513, 0.0076949733183423324)),
            "withdrawals": (26783.629963770007, 304.08262615724306, (
                304.08262615724306, 198.214812279994, 113.08860043992328, 61.21497313575743,
                9.465810602766513)),
            "claims_death": (6279.054879263288, 70.38958155601804, (
                69.91722074976035, 48.15264297727199, 27.844504321429795,
                12.713169399373365, 0.0)),
            "claims_surrender": (23208.18638711875, 337.96081530140407, (
                337.96081530140407, 174.43975214509157, 88.09124573202183,
                25.28243559963908, 0.0)),
            "unit_releases": (29379.247771991017, 402.5415319451926, (
                402.5415319451926, 222.54429058392475, 115.90793336581784, 37.982904530082,
                0.0)),
            "death_strain": (107.9934943910208, 5.336504105971783, (
                5.336504105971783, 0.048104538438827865, 0.027816687633792938,
                0.012700468930441524, 0.0)),
            "expenses": (366.2275972248017, 3.6489915138869167, (
                3.6489915138869167, 2.6255047788896615, 1.6534497414161258,
                0.9879279989618096, 0.4681593836044502)),
            "net_cf": (2179.450080085304, 36.899442876698586, (
                36.899442876698586, 18.544524939862775, 6.841661050889496,
                1.4733973381463519, -0.4602639706402609)),
        },
        "result_pols": {
            "pols_if": (64.32106673433111, 0.7297983027773833, (
                0.7297983027773833, 0.4757155494719856, 0.27141264105581586,
                0.14691593552581783, 0.06307276672972552)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.1532923931415476, 0.0010055654508002582, (
                0.0009643754586173845, 0.0009066517372879832, 0.0007471315121890061,
                0.000642330119842958, 0.00040076698181570935)),
            "pols_surr": (0.5146769703076627, 0.005046724985241304, (
                0.005046724985241304, 0.0032877584832361356, 0.0023660525832851385,
                0.0012786669513998555, 0.0008430604197367447)),
            "pols_maturity": (0.061828939328173065, 0.061828939328173065, (
                0.0, 0.0, 0.0, 0.0, 0.061828939328173065)),
        },
    },
}
# END generated fingerprint: ULB_UK_SEC


# ---------------------------------------------------------------------------
# Compiled (UKLIB-SEC-PLAN.md U2, the C step, after USLIB-SEC-PLAN.md's Phase 2)
#
# These compile the model, once a session, into a temporary directory (conftest.sec_build),
# and run the compiled package in a child process only.  They skip without modelx-cython or
# a C compiler, and the cython_uk CI job, which sets UKLIB_REQUIRE_CYTHON=1, fails a skip.
# test_compiled_conventions_uk.py checks the compiled model's types, its caches and its
# release, and compares it with modelx on the committed points; these hold what is ULB's
# own: the comparison on the splice grid, at the contract's extremes, where the cap on
# mortality binds, at the depletion threshold's edges, on every value a decoded column
# holds, on keys written as floats and on the committed row in the money under the return
# it was read from; the refusals and the overflow; the deepest calls on a 1 MiB stack; a
# Reference set late; and the runner.
#
# Every C4 comparison here passes the model's also, _ulb_c4_also, the spec's c4_also, which
# the conventions' C4 passes on the committed points: every cell of a code at every code it
# takes, in every month of the frame and the month after it, the fund at BEF_GROWTH and the
# count at AFT_DECR, which no swept cell reads, among them (UKLIB-SEC-PLAN.md, M15).
# test_the_c4_comparisons_ask_every_code_on_every_row, which needs no compiler, holds it to
# the codes each cell takes in modelx, row by row.


def _as_modelx(have, want):
    """Whether a compiled value is modelx's: identical where ``exact_here()``, as on
    x86-64, and to 1e-12 relative elsewhere, as C4 compares (uk_sec_support)."""
    return have == want if exact_here() else have == pytest.approx(want, rel=1e-12, abs=0)


def _mismatch_lines(found):
    return f"{len(found)} mismatches, first:\n  " + "\n  ".join(found[:50])


# The cells C4 asks at every code, each with the names of the codes it takes, read from the
# model's own References (_code): the harness's, which its _ulb_c4_also, the spec's c4_also,
# asks in every month of every row.  And the cells of a life, as (those of a life alone,
# those of a month and a life), of which the bond has none: its one life is read by cells
# of no life.  What each takes is derived in modelx, row by row, and these must name
# exactly that (test_the_c4_comparisons_ask_every_code_on_every_row).
CODED = _ULB_CODED
CELLS_OF_A_LIFE = ((), ())

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
    """A stand-in for a point, which records what :func:`_ulb_c4_also` asks of each
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
    """C4's ``also`` asks every code its cells take, in every month of every row.

    Nothing in a comparison shows what it leaves out: dropped from :func:`_ulb_c4_also`, a
    code is simply not compared.  So the cells of a code or of a life are read from the
    model, each of a month and one more parameter, a timing, a kind or a life, and each with
    a life among its parameters, whatever its shape (:func:`_coded_cells`), and what each
    takes is derived in modelx, not read from :data:`CODED`: on a fresh read of the
    committed model, and on every row of the splice grid this run selects, the twins, the
    rows restated in force and the future rows among them, each such cell is asked every
    argument in the caches' one inner width, 0 to 7, in the row's first month on the books,
    and the arguments it takes are those it does not refuse, ``invalid timing``,
    ``invalid kind`` or ``invalid life`` (:func:`_codes_taken`).  :data:`CODED` must name
    exactly those cells and codes, by the model's own References, row by row, and
    :data:`CELLS_OF_A_LIFE` the cells of a life, of which the bond has none, so that one
    added later fails here until the ``also`` asks it.  Then :func:`_ulb_c4_also` is run on
    a stand-in of each of those rows (:class:`_Asked`), one at a time: it must ask each cell
    at every code the cell takes on the row, in every month of the frame and the month after
    it, and no other, so that a code left out on one kind of row fails here, where a union
    over the rows would pass it.  And it must be the spec's ``c4_also``, which the
    conventions' C4 on the committed points passes (``uk_sec_support.spec_c4_also``).  Needs
    no compiler.
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
                _ulb_c4_also(stand_in)
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
    assert SPEC.c4_also is _ulb_c4_also, SPEC.c4_also


# How many rows of a grid C4 compares at once.  compiled_mismatches sweeps every row of its
# case in one modelx read and keeps every value of every row, in the parent and in the
# child, until it compares them.  A ULB row runs at most 1,356 months, so twenty rows hold
# about what uslib's MYGA's chunks of twenty did (USLIB-SEC-PLAN.md §7.10, *Record --
# M20*).
C4_CHUNK = 20


@pytest.mark.cython
def test_the_compiled_model_computes_what_modelx_computes_on_the_splice_grid(spliced,
                                                                             sec_build,
                                                                             tmp_path):
    """C4 on the branches: compiled, every cell of the splice grid is modelx's.

    The sample traces the committed points alone, and they leave branches untaken, which
    are typed all the same, because every branch of a cell returns the one type the others
    return (sample_sec.py).  What the compiled model computes on them is held here: the
    splice grid's rows, S's points and its four variants restated in force at T2's months
    and issued later, the GMDB in the money, the 7.5% cap binding, the rider beside the
    adviser charge and the cap net of the charge among them, under the splice's References,
    every switch that ships off on, the surrender cap binding from policy year 21
    (:data:`SPLICED_REFS`).  The grid is the one this run's ``spliced`` selects, the core
    by default and the full grid under ``UKLIB_SEC_FULL=1``, and the test carries no
    ``sec_full`` mark, since a skipped compile test fails the cython_uk job.  The grid's
    SEC table goes beside the build :data:`C4_CHUNK` rows at a time, modelx sweeps every
    point fully, and the compiled model must agree at every argument modelx caches,
    identically on x86-64 and to 1e-12 relative elsewhere, with every raise and every
    ``Data`` array (``uk_sec_support.compiled_mismatches``).
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
                                                  also=_ulb_c4_also)]
    assert not found, _mismatch_lines(found)


# The contract's extremes (product-spec.md, held by proj_len()): each shape at its longest
# cover from the youngest issue age, as (the S point it changes, its changes): the
# accumulation cell, no withdrawals, its fund lasting to the contract's largest limiting
# age, 121, 1,236 months from 18; the custom 3%, female, whose fund runs out at 1,176; the
# GMDB point with no
# withdrawals, the rider charged to the limiting age; the adviser charge, its fund closing
# on a rounding; and the GMDB point on the anchor's pattern, its guarantee drawn down.
EXTREMES = {
    21: (2, {"age_at_entry": 18}),
    22: (6, {"age_at_entry": 18}),
    23: (4, {"age_at_entry": 18, "wd_pattern": "none"}),
    24: (3, {"age_at_entry": 18}),
    25: (4, {"age_at_entry": 18}),
}


def _contract_extremes(tmp_path):
    """The rows at the contract's extremes, built by the generator.

    Each of :data:`EXTREMES` in a copy of S's table, read with :data:`LONGEST_REFS` set,
    the limiting age at 121, its twin issued at the valuation date, the same issued
    ``future_horizon_mth``, 120 months, after it, a frame of up to 1,356 months, and the
    same restated in force in the last month of its SEC frame, opened with S's state there;
    so ``t`` reaches 1,357, the policy year 103 and each code its last, the furthest
    ``spec_sec.py`` sizes for.  S's tables serve: the mortality table runs from 18 to 120.
    Returns the rows.
    """
    s_table = _s_table()
    rows = []
    for point_id, (base, changes) in EXTREMES.items():
        row = s_table.loc[[base]].assign(**changes, policy_id=f"ULB-7000{point_id}")
        row.index = pd.Index([point_id], name="point_id")
        rows.append(row)
    s = mx.read_model(temp_inputs(tmp_path, model_path(TWIN), model_points=pd.concat(rows)),
                      name=_name("extremes_s"))
    try:
        for ref, value in LONGEST_REFS.items():
            setattr(s.Projection, ref, value)
        last = {}
        for point_id in EXTREMES:
            sp = _point(s, point_id)
            end = next((t for t in range(sp.proj_len()) if sp.av_pp(t) <= THRESHOLD),
                       sp.proj_len())
            last[point_id] = end - 1
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
    opening of the longest cover's last policy year; and every timing and kind.  modelx sweeps every row fully, and the
    compiled model must agree everywhere.  A cache one too small for the contract raises
    ``IndexError`` compiled where modelx reads on, and fails here, though the spec check
    passes it, which holds the caches to the spec and not the spec to the contract.
    """
    build = sec_build(SEC)
    rows = _contract_extremes(tmp_path / "s")
    covers = 12 * (OMEGA_MAX - rows["age_at_entry"]) - rows["duration_mth"]
    assert covers.max() == 1356
    folder = compiled_case(build, tmp_path / "extremes", model_points=rows)
    found = compiled_mismatches(build, folder, refs=LONGEST_REFS, also=_ulb_c4_also)
    assert not found, _mismatch_lines(found)


@pytest.mark.cython
def test_the_compiled_model_computes_what_modelx_computes_where_the_cap_binds(sec_build,
                                                                              tmp_path):
    """C4 where ``mort_rate`` caps the annual rate at 1: compiled, every cell is modelx's.

    The rows of the cap's test, :data:`CAPPED_POINT`'s twin, its row issued 12 months on
    and its rows restated in force the month before the cap and five months into the
    capped year, built by the generator from S under :data:`CAPPED_REFS`, go beside the
    build.  modelx sweeps them fully under the same References, and the compiled model
    must agree at every argument modelx caches, identically on x86-64 and to 1e-12
    relative elsewhere (``uk_sec_support.compiled_mismatches``).  No other compiled test
    reaches the side of ``min(q, 1.0)`` that returns 1, where the monthly rate is exactly 1
    and every policy in force dies.
    """
    build = sec_build(SEC)
    s = _capped_s(tmp_path / "s")
    try:
        spec = dataclasses.replace(
            SPEC, derived=((CAPPED_POINT, CAPPED_MTH - 1), (CAPPED_POINT, CAPPED_MTH + 5)),
            future=((CAPPED_POINT, 12),), derived_refs={})
        rows, _ = build_sec_table(spec, s)
    finally:
        s.close()
    rows.loc[rows["source_mth"] == CAPPED_MTH + 5, "policy_count"] = 1.0
    folder = compiled_case(build, tmp_path / "capped", model_points=rows)
    found = compiled_mismatches(build, folder, refs=CAPPED_REFS, also=_ulb_c4_also)
    assert not found, _mismatch_lines(found)


@pytest.mark.cython
def test_the_compiled_model_computes_what_modelx_computes_at_the_threshold_s_edges(
        sec_build, tmp_path):
    """C4 where the depletion threshold decides the frame: compiled, every cell is modelx's.

    The threshold ends a frame at the first month whose fund opens at or below it, and
    refuses a bond in force whose fund opens there.  So on the committed table with the
    anchor cell in force 30 months opening on the least fund past the threshold, which
    projects one month and is drawn to nothing in it, and on 0.006; and on the committed
    table under a threshold of exactly the anchor cell's fund in its month 352, where its
    frame ends a month early, and under the float below that fund, where it does not, as
    ``test_a_fund_that_reaches_the_threshold_exactly_is_exhausted_there`` holds in modelx:
    each swept fully, and the compiled model must agree everywhere, the frames' ends among
    them, where a compiled ``<`` for ``<=`` would part.
    """
    build = sec_build(SEC)
    shipped = mx.read_model(model_path(SEC), name=_name("edges"))
    try:
        fund = _row(shipped, "twin", 1, 0).av_pp(352)
    finally:
        shipped.close()
    row = _label(_committed(), "derived", 1, 30)
    found = []
    for i, value in enumerate((PAST_THE_THRESHOLD, 0.006)):
        folder = compiled_case(build, tmp_path / f"fund{i}",
                               model_points=_set("av_pp_init", [row], value)(_committed()))
        found += [f"av_pp_init {value!r}: {line}"
                  for line in compiled_mismatches(build, folder, also=_ulb_c4_also)]
    folder = compiled_case(build, tmp_path / "threshold")
    for threshold in (fund, math.nextafter(fund, 0.0)):
        found += [f"depletion_threshold {threshold!r}: {line}" for line in
                  compiled_mismatches(build, folder,
                                      refs={"depletion_threshold": threshold},
                                      also=_ulb_c4_also)]
    assert not found, _mismatch_lines(found)


@pytest.mark.cython
def test_the_compiled_model_computes_what_modelx_computes_on_every_decoded_value(
        sec_build, tmp_path):
    """C4 on every value a decoded column holds: compiled, every cell is modelx's.

    The twins of :data:`DECODED`'s points, each sex, each withdrawal pattern, the rider's
    flag each way and an issue age with a fraction, built by the generator from a copy of
    S's table, go beside the build: modelx sweeps them fully, and the compiled model must
    agree everywhere, each label's text, each decode's code and the mortality row it
    selects among them, which the committed points, all single lives on three patterns,
    reach only in part.
    """
    build = sec_build(SEC)
    s_table = _s_table()
    rows = []
    for i, (base, changes) in enumerate(DECODED, start=1):
        row = s_table.loc[[base]].assign(**changes, policy_id=f"ULB-8{i:05d}")
        row.index = pd.Index([i], name="point_id")
        rows.append(row)
    s = mx.read_model(temp_inputs(tmp_path / "s", model_path(TWIN),
                                  model_points=pd.concat(rows)), name=_name("decoded_s"))
    try:
        spec = dataclasses.replace(SPEC, derived=(), future=(), derived_refs={})
        twins, _ = build_sec_table(spec, s)
    finally:
        s.close()
    folder = compiled_case(build, tmp_path / "decoded", model_points=twins)
    found = compiled_mismatches(build, folder, also=_ulb_c4_also)
    assert not found, _mismatch_lines(found)


# The model point table's columns that hold whole numbers, which a spreadsheet may save as
# floats: the months, the age and the segments.  And the assumption tables' keys.
FLOAT_COLUMNS = ("duration_mth", "age_at_entry", "n_segments")
FLOAT_KEYS = {MORT: lambda t: t.assign(age=t["age"].astype(float)),
              SURR: lambda t: t.assign(policy_year=t["policy_year"].astype(float))}


@pytest.mark.cython
def test_the_compiled_model_reads_keys_written_as_floats_as_modelx_does(sec_build,
                                                                         tmp_path):
    """C4 on keys written as floats: the compiled model reads 30.0 as 30, as modelx does.

    The committed table with its labels written ``1.0`` to ``12.0`` and its whole numbers as
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
    found = compiled_mismatches(build, folder, also=_ulb_c4_also)
    assert not found, _mismatch_lines(found)


@pytest.mark.cython
def test_the_compiled_model_computes_what_modelx_computes_in_the_money(sec_build,
                                                                        tmp_path):
    """C4 on the committed row in the money, under the return it was read from.

    The committed table's row :data:`IN_THE_MONEY` was read from S run under a fund return
    of 0, a fund that has earned nothing since issue, and at the shipped 5% its rider
    charges for 36 months and its death benefit pays the guarantee for 39, which C4 on the
    committed points compares.  Under the return it was read from, set on the compiled
    model as on modelx before either computes, it continues S's path over its whole frame,
    the guarantee above the fund in every month (``test_a_committed_row_holds_the_guarantee
    _in_the_money``): so the committed table is swept fully at that return, and the
    compiled model must agree everywhere, the rider's charge and the guarantee's death
    benefit in every month of that row among it.
    """
    build = sec_build(SEC)
    folder = compiled_case(build, tmp_path / "money")
    found = compiled_mismatches(build, folder, refs=IN_THE_MONEY_REFS, also=_ulb_c4_also)
    assert not found, _mismatch_lines(found)


# The compiled refusals' child: one process, which imports the compiled package once and
# runs each case on a fresh instance of the model, whose Data reads the case's own copies
# of the three files by absolute path.  A refusal names a file by its Reference, so the
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
CASE_FILES = {"model_point_file": TABLE, "mort_table_file": MORT, "surr_table_file": SURR}


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
# fraction is truncated as it is set, 18.5 to 18, where modelx computes with 18.5, so the
# compiled refusals take a domain's cases at whole numbers alone, and model-sec.md says to
# set each as a whole number (UKLIB-SEC-PLAN.md §6.1, *Record -- M2*).
INT_REFERENCES = frozenset({"issue_age_min", "omega_age", "omega_age_max",
                            "allowance_years"})


def _held_compiled(refs):
    """Whether the compiled model holds every one of ``refs`` as modelx does."""
    return all(math.isfinite(value) and value == value // 1 and abs(value) < 2.0 ** 63
               for ref, value in refs.items() if ref in INT_REFERENCES)


# Codes no cell takes, inside the one inner width every 2-D cache shares, which each cell
# refuses by its own formula, ValueError, in both engines, as (call, arguments), on point
# 1: the fund's first and last timings in the count's cell, the count's in the fund's, and
# the first and last codes past the kinds and the total.  Each slot of the cache a call
# leaves unused is a code some other cell takes, so a cell must refuse it itself.
CODES_IN_CACHE = [("pols_if_at", (0, 4)), ("pols_if_at", (0, 7)), ("av_pp_at", (0, 0)),
                  ("av_pp_at", (0, 3)), ("claims", (0, 3)), ("claims", (0, 7))]

# A power an input the model accepts pushes past the largest float, which Python's float
# power refuses with OverflowError where C's pow gives an infinity, so that the cell calls
# Python's own there (Projection.inflation_factor), as (case, the References, [(point,
# cell, arguments)]): expense inflation of 1e20 a year, past it at t = 192, (1e20)^16, on
# the anchor cell's twin, whose frame runs to 352.
OVERFLOWS = [
    ("expense inflation past the largest float", {"inflation_rate": 1e20},
     [(1, "inflation_factor", (192,)), (1, "inflation_factor", (191,)),
      (1, "result_cf", ())]),
]

# Projection's idx past the extract's last row, 12, and -1, beside the last row, 11, as
# (position, cell, arguments): past the last row the first read of a vector raises
# IndexError in both engines, each in its own words, and -1 reads every vector at its last
# element in both, so it is the last point, under that point's own point_id.
IDX_CASE = "an idx past the table and one before it"
IDX_EDGES = [(12, "point_id", ()), (12, "result_cf", ()), (-1, "point_id", ()),
             (-1, "proj_len", ()), (-1, "net_cf", (0,)), (11, "point_id", ()),
             (11, "proj_len", ()), (11, "net_cf", (0,))]

# Calls past the caches spec_sec.py sizes, which raise IndexError in the compiled model
# alone, as (call, arguments, what modelx does), on the extract's first row, point 1, the
# anchor cell issued at 65: a month either side of the t cache, which modelx answers with
# 0.0, the month outside cover; a timing and a kind past the one inner width, which modelx
# refuses as codes it does not take; and a policy year past the y cache, whose opening
# modelx computes as it computes any year's opening, the closing value of the year before:
# 0.0 here, that year long past the point's cover, and the fund that year closes on for a
# bond whose cover reaches it, one issued at 18 under a limiting age of 121.
COMPILED_ONLY = [
    ("net_cf", (1358,), ("ok", 0.0)), ("net_cf", (-1,), ("ok", 0.0)),
    ("pols_if_at", (0, 8), ("raised", "ValueError: invalid timing")),
    ("av_pp_at", (0, 8), ("raised", "ValueError: invalid timing")),
    ("claims", (0, 8), ("raised", "ValueError: invalid kind")),
    ("av_pp_py", (104,), ("ok", 0.0)), ("wd_cum_pp_py", (104,), ("ok", 0.0)),
    ("pols_if_py", (104,), ("ok", 0.0)),
]


def _refusal_cases():
    """Every refusal the compiled model must make as modelx does, as (case, the table, the
    edits, the References, [(position, cell, arguments)], the Data cells to read).

    Each table is an extract, labelled otherwise than by position (:func:`_extract`'s
    labels, the generator's columns kept), so that a refusal naming a point by ``idx + 1``
    names another; a case that edits the committed table edits it first, by its own
    labels, and is then relabelled.  A position, not a label, since a table ``Data`` refuses
    has no keys to give: each is the row's place in the table written, ``Projection``'s
    ``idx``, which the test indexes ``Projection`` by in modelx too.
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
        cases.append((case, extract(), {file: edit}, {}, [(at(1), "result_cf", ())],
                      (cell,)))
    for case, edit, refs, point, _, _ in NOT_ISSUED:
        cases.append((case, extract(edit), None, refs,
                      [(at(point), cell, ()) for cell in ("result_cf", "proj_len")], ()))
    for case, refs, message in DOMAINS:
        if message is not None and _held_compiled(refs):
            cases.append((f"domain {case}", extract(), None, refs,
                          [(at(1), "result_cf", ()), (at(1), "proj_len", ())], ()))
    for case, edit, refs, point, message, _ in EXHAUSTED:
        if message is not None:
            cases.append((case, extract(edit), None, refs, [(at(point), "result_cf", ())],
                          ()))
    for case, refs, month, cell_message, _ in SURRENDER_EDGES:
        if cell_message is not None:
            cases.append((f"surrender {case}", extract(), None, refs,
                          [(at(1), "surr_rate", (month,)), (at(1), "result_cf", ())], ()))
    cases.append(("past its cover", extract(_set("duration_mth", [10], 660)), None, {},
                  [(at(10), "result_cf", ()), (at(10), "proj_len", ())], ()))
    cut = {MORT: _dropped(lambda t: (t["age"] > 100) | (t["age"] < 20))}
    cases.append(("an age outside the mortality table",
                  extract(_set("age_at_entry", [1], 18)), cut, {},
                  [(at(1), "result_cf", ()), (at(1), "mort_rate", (0,)),
                   (at(2), "result_cf", ())], ()))
    cases.append(("an opening fund past the floats",
                  extract(_set("av_pp_init", [7], 1.79e308)), None, {},
                  [(at(7), "result_cf", ())], ()))
    cases.append(("an allowance past the floats", extract(), None,
                  {"wd_allowance_rate": BIG}, [(at(1), "result_uf", ())], ()))
    for case, edit, cell, args, _ in NOT_HELD:
        if edit is not None:
            cases.append((case, edit(committed), None, {}, [(9, cell, args)],
                          ("point_id",)))
    cases.append(("codes no cell takes, inside the caches", extract(), None, {},
                  [(at(1), cell, args) for cell, args in CODES_IN_CACHE], ()))
    for case, refs, calls in OVERFLOWS:
        cases.append((case, extract(), None, refs,
                      [(at(point), cell, args) for point, cell, args in calls], ()))
    return cases


@pytest.mark.cython
def test_the_compiled_model_refuses_what_modelx_refuses(sec_build, tmp_path):
    """Compiled, the model refuses what modelx refuses, with modelx's error and message.

    A ``ValueError`` raised in a cell typed ``long long`` or ``double`` propagates out of
    the compiled model as out of modelx.  So, each on its own inputs and References
    (:func:`_refusal_cases`), on an extract labelled otherwise than by position: every
    case of :data:`MALFORMED`, refused by a projection and by ``Data``'s reader, the
    ``2**53`` bounds among them; every case of :data:`UNREADABLE`, by a projection and by
    the ``Data`` cell that checks the table, so that a compiled ``Data`` cell refuses each
    value its modelx cell refuses; every case of :data:`NOT_ISSUED`, by ``result_cf`` and
    ``proj_len``; every case of :data:`DOMAINS` that refuses and that the compiled model
    can hold, its integer References whole (:func:`_held_compiled`), each printed as the
    compiled model types it; each fund :data:`EXHAUSTED` refuses; each surrender rate
    outside 0 to 1, by its cell and by the frame; a point past its cover; an age outside
    the mortality table, either side; an opening fund and an allowance past the floats; a
    label the vectors cannot hold, by ``Data.point_id``; and each code of
    :data:`CODES_IN_CACHE`, inside the caches, which the cell's own formula refuses.

    And each power of :data:`OVERFLOWS` past the largest float: compiled, the cell calls
    Python's own power where C's gives an infinity, so that it raises the platform's
    ``OverflowError`` as modelx does, where it would carry an infinity on.

    And the refusals that are the compiled model's alone (:data:`COMPILED_ONLY`): a month
    past the ``t`` cache either side, a timing and a kind past their codes and a policy
    year past the ``y`` cache, each raising ``IndexError`` compiled, beside what modelx
    does.  And ``Projection``'s ``idx`` at the table's edges (:data:`IDX_EDGES`): one past
    the last row raises ``IndexError`` in both engines, compared by its type, the words
    being each engine's own, and ``-1`` is the last row in both, its every outcome the last
    row's and modelx's, which a build without bounds checks, or without Python's negative
    indices, would part from.

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
    assert len(relabelled) == 12
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
                if idx == 12:
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
            if cell == "inflation_factor" and args == (191,):
                if modelx_did[0] != "ok" or compiled_did != modelx_did:
                    found.append(f"{where}: compiled {compiled_did}, modelx {modelx_did}, "
                                 f"where the year before the overflow computes")
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
        if idx == -1 and outcomes != edges[11, cell, args]:
            found.append(f"{IDX_CASE}: {cell}{args} at idx -1 is {outcomes}, at the last "
                         f"row {edges[11, cell, args]}")
    assert edges[-1, "point_id", ()][0] == ("ok", EXTRACT_LABELS[-1]), edges
    overflow = [w for (case, *_), (w, _) in zip(cases, wants) if case == OVERFLOWS[0][0]]
    assert overflow and overflow[0][0][1].startswith("OverflowError"), overflow
    assert not found, "\n".join(found[:40])
    assert refused == sum(len(calls) + len(data) for *_, calls, data in cases[:plain]) - 1


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

# The chain heads the stack test calls cold, each in an ItemSpace of its own: net_cf, and
# the unit-funding residual, the deepest call a projection makes.  The runner makes one
# ItemSpace for each key of a job and deletes it after the key's calls, so a key with two
# calls would run the second warm, on the first's caches.
STACK_HEADS = ("net_cf", "check_unit_funding_resid")

# How long the stack test waits for each child, in seconds: one runs in a few seconds, more
# under load.  A bracketing size may kill its child on a stack overflow by design, and
# where the overflow hangs instead, as Windows Error Reporting could, the wait ends sooner
# than for the two runs asserted, and the size is recorded as timed out.
BRACKET_TIMEOUT, ASSERTED_TIMEOUT = 120, 300


@pytest.mark.cython
def test_the_longest_cover_runs_cold_on_a_one_megabyte_stack(sec_build, tmp_path):
    """The deepest call the contract allows runs compiled on a 1 MiB stack (F7).

    On the rows of :func:`_longest_cover`, each shape of :data:`SHAPES` at its longest
    cover, issued at 18 now and 120 months on, the limiting age at the contract's largest,
    121: the accumulation cell, 1,236 months; the custom 3%, 1,176; the GMDB point
    withdrawing, 353, and the adviser charge, 323; and the GMDB point with no withdrawals,
    the rider charged to the limiting age, 1,236.  Each of :data:`STACK_HEADS`, a cold
    ``net_cf`` and a cold unit-funding residual in the last month, runs the chains back to
    ``t_entry()``, one cell a month within the policy year and two a year before it, the
    fund, the withdrawals since issue and the count being blocked by policy year: 231 cells
    deep in modelx at the longest cover, on a model just read
    (:func:`test_every_chain_runs_one_cell_a_month_from_a_cold_start`), with every switch
    that ships off on (:data:`LONGEST_REFS`).  Each runs in an ItemSpace of its own, on a
    copy of its row, so that each is cold: in one ItemSpace the second would run on the
    first's caches, a few cells deep.  Compiled they run on the C stack, which the
    interpreter's recursion limit does not count, and one cell a month they needed 288 KiB
    of it here at the shipped limiting age (UKLIB-SEC-PLAN.md §6.6, *Record -- M10*).  1 MiB is the stack MSVC gives an
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
    folder, frames = _longest_cover(tmp_path / "rows")
    rows = pd.read_csv(folder.parent / TABLE, index_col="point_id")
    copies = [rows.set_axis(rows.index + 1000 * i, axis=0) for i in range(len(STACK_HEADS))]
    case = compiled_case(build, tmp_path / "longest", model_points=pd.concat(copies))
    model = mx.read_model(case, name=_name("longest"))
    try:
        for ref, value in LONGEST_REFS.items():
            setattr(model.Projection, ref, value)
        calls, want = {}, {}
        for label, months, entry, _ in frames:
            for i, head in enumerate(STACK_HEADS):
                key = _key(model, label + 1000 * i)
                proj = projection(model, key)
                assert (proj.proj_len(), proj.t_entry()) == (months, entry), label
                calls[key] = [(head, (months - 1,))]
                want[key] = [proj.cells[head](months - 1)]
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
    record = (f"the compiled cold net_cf and unit-funding residual at the longest cover, "
              f"each in an ItemSpace of its own, ran on a thread of {ran or 'no size'} KiB "
              f"and not of "
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
early = p[6]
values = [p.expenses(12), early.expenses(12)]
p.inflation_rate = 0.0
values += [p.expenses(12), early.expenses(12), p[7].expenses(12)]
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
    ``Projection``, the anchor's twin at ``idx`` 0, the anchor cell in force 30 months, made
    before, and the adviser charge in force 66 months, made after, so that a modelx-cython
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
        before = (p.expenses(12), projection(model, 6).expenses(12))
        p.inflation_rate = 0.0
        fresh = (p.expenses(12), projection(model, 6).expenses(12),
                 projection(model, 7).expenses(12))
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
    modelx's: point 7's description and its first twelve rows and counts, point 12's, the
    row in the money, and the block's lines for each point, its first twelve rows and its
    first twelve projection years.

    The same output is what a runner that ignored ``--build`` and ran modelx would print,
    so the runner is also given a directory that holds no build, and must refuse it,
    saying so, rather than print anything.
    """
    build = sec_build(SEC)
    runner = model_path(SEC).parent / "run_sec.py"
    for args in (("7",), ("12",), ("--block",)):
        expected = _run_sec(runner, *args)
        assert _run_sec(runner, *args, "--cython", "--build", str(build.out)) == expected
    empty = tmp_path / "no_build"
    empty.mkdir()
    done = _run_sec(runner, "7", "--build", str(empty), check=False)
    stderr = done.stderr.decode(errors="replace")
    assert done.returncode != 0 and done.stdout == b"", stderr
    assert f"holds no build of {SEC} for this interpreter" in stderr, stderr
