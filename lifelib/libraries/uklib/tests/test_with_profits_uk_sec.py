"""In-force and compile tests for WP_UK_SEC: the splice, future business, counts,
regeneration, the compiled form.

``WP_UK_SEC`` is ``WP_UK_S`` taught to run in force at a valuation date (UKLIB-SEC-PLAN.md,
milestone M13, after USLIB-SEC-PLAN.md's Phase 1), and then to compile under
modelx-cython (milestone M14, after its Phase 2).  It runs on two clocks: ``t`` counts
months from the valuation date, the same month for every model point, and
``duration_mth(t)`` counts the months the policy has been in force,
``duration_mth_init() + t``.  A model point may be a policy already in force at the
valuation date, in any month of its policy year, one issued at it, or one to be issued
after it, as in ``basiclife/BasicTerm_SE``.  A policy in force opens with its count and
eight columns of state beside it, each per policy and measured at the valuation instant,
before month 0's events, ``WP_UK_S``'s close of the month before: the asset share, the
units and the unit price, the endowment's attaching bonus, the smoothed payout, the bonus
rate of the year under way, and the two cumulants ``WP_UK_S`` restarts at 0 where its frame
opens, the guarantee charges taken and the smoothing account.

The worked example is not restated here.  On a point issued at the valuation date the two
clocks coincide and the model is ``WP_UK_S``, and ``test_model_conventions_uk.py`` asserts
that cell by cell on the twins of S's two new-business points, the endowment and the bond
S's point 7 issues at the valuation date (T1).  The conventions also hold the SEC family's
other rules: every frame opens at ``t = 0``, ``pols_if`` is the ``BEF_DECR`` count,
``BEF_DECR`` is ``BEF_NB`` plus the month's new business, new business enters once, and
nothing happens before issue.  This module holds the rest of the plan's tests (its §5) and
the product's own facts:

* T2, the splice: an S point restated in force at month ``d``, opened with the state S
  carries into ``d``, continues S's projection from ``d`` on, in every cell of S's and in
  the three reports.  The months straddle the product's events: the declarations, the
  guarantee window, the smoothing cap, the corridor, the market value reduction turning
  on, the guarantee charge's cap, the asset share's floor, exhaustion and the one-row
  frames.  S's own in-force points are spliced as twins at 60 and 240.  It runs on two sets
  of References: the main one, with the estate distribution that ships at 0 on, and a
  second with the bonus rule on, on fewer rows.  Variants of S's points, in a copy of S's
  table, add a female life, a -40% crash, the pension tax basis on a bond, and three bonds
  issued at the valuation date for the charge's cap.
* T3, future new business: a point issued ``k`` months after the valuation date is S's
  projection ``k`` months on, with zeros before issue and no table read there.
* D11's R1 and R2, and D3's and D5's chains: on the splice's grid no cell is called at a
  negative month, none on the books reads a month before them, and none reads beyond
  ``t + 1`` but the bonus rate's declaration read, inside the frame; the exhaustion search
  reads the units to the month they run out and no further; on the committed points no
  recursion runs backward over the frame; the policy clock is a closed form; each chain,
  called cold, runs one cell a month back to ``t_entry()`` at the contract's longest cover,
  on each shape; and each chain written inline is its step-by-step cells, bit for bit.
* T4, the count algebra: the count rolls forward through new business, deaths,
  surrenders and maturities, ``result_pols`` holds it, multiplying ``policy_count`` by 2.5
  with every switch that ships off on multiplies every flow and counted cell by 2.5 and
  moves no per-policy value, a point restated a month on continues its own flows, and the
  roll-forward, whose tolerance scales with the count, closes on ten million policies.
* T5, validation: each malformed row of the table is refused as it is read, naming its
  point, by its label on an extract labelled otherwise; each assumption table, malformed or
  holding a value that is not a number in its range, is refused before a value of it is
  read; the future horizon is a Reference that bounds future business; a point past its
  cover, one the contract does not issue, a bond spent in its first month and one that
  reads a Reference off its domain are refused by the frame, each domain at both its edges
  and each accepted edge projecting its reports; a value past the floats in the cell where
  it first is; the edges of the interface are accepted; and so is every state ``WP_UK_S``
  reaches.
* T6, regeneration: the committed ``model_point_table_sec.csv`` is what the generator makes
  of ``WP_UK_S`` and its table as they stand.
* The C step's representation, in modelx (UKLIB-SEC-PLAN.md §6.5, *C*): the claims total
  ``WP_UK_S``'s ``sum`` to the last bit where ``sum`` compensates, as from Python 3.12:
  Python 3.11's ``sum`` adds left to right, and there the total parts from it where the
  kinds are of a size, so the bits skip, naming 3.11, and the rest is held; each refusal
  cell its chain, and each chain past the floats after its first month refused there;
  every decode ``WP_UK_S``'s own; the padded arrays, the vectors' dtypes, the Python
  numbers, the labels; the spec's sizes and the bounds they come from; the sample; the
  runner's rebuild; and what the vectors cannot hold.  Then C2, the Phase 1 fingerprint,
  and the compiled model, each test marked
  ``cython``: C4 on the splice grid, the contract's extremes, the bounds that bind, the
  decoded values, float keys, the committed rows under their own References, the rule's
  declarations and the exhaustion, with every code asked of every row; the labels; the
  refusals message for message; the 1 MiB stack; a Reference set late; and the runner.
* Then the product's own facts: the two clocks on the shipped points; the committed rows
  continuing their S points, those read under References of their own continuing S under
  them; each history column read rather than recomputed (UKLIB-SEC-PLAN.md K14), both
  cumulants among them; the single premium, the declaration and the guarantee window on the
  policy clock; the bonus rate's read bounded by the frame, the recorded departure; the
  exhaustion's new "never"; expense inflation on the valuation clock; the cap on mortality,
  a NaN that reaches a bound and a check whose residual is NaN; the values outside cover;
  the block; an in-force extract; the runner; the cells' defaulted parameters; the
  docstrings; the shared input tables; the parameters a formula could confuse, apart on
  some core row; and what the default grid reaches.

SEC month ``t`` is S month ``t + source_mth`` throughout, the direction in which
``uk_sec_support`` takes its ``t_offset``: ``d`` for a point restated at S month ``d``,
``-k`` for one issued ``k`` months on.

**The core grid and the full one** (UKLIB-SEC-PLAN.md U6).  T2 and T3 over every S point and
variant at every month run by default on a core, chosen so that between them they reach
every branch, every opening-state column, every kind of valuation month and both sides of
every ``min`` and ``max`` the full grid reaches, which
``test_the_core_grid_reaches_every_branch`` asserts.  The other cases, and the rules
test's scan of their rows, carry the ``sec_full`` marker and are skipped, with the reason
shown, unless ``UKLIB_SEC_FULL=1`` is set.  So do the slower tests' other cases
(``GRIDS``), each test's docstring saying which.  They are never dropped: one leg of the CI
matrix sets it, and ``UKLIB_SEC_FULL=1 python -m pytest -m sec_full
lifelib/libraries/uklib/tests/test_with_profits_uk_sec.py`` runs them alone.  Each splice
row is released once it has been read (``_release``), as ``run_sec.py --block`` releases
its points.

Every test keeps four rules.  Each model is read under a name of its own and closed:
``conftest.with_profits`` reads S under its default name, and reading a model under a name
in use renames the open one.  No test writes inside the library tree: every changed input
goes through ``uk_sec_support.temp_inputs`` into a temporary directory, because a CSV added
beside the models, even briefly, would fail a concurrent
``test_every_csv_beside_the_model_is_actually_read``.  No test indexes ``Projection`` by
hand: the keys come from ``uk_registry.point_keys`` and the ItemSpaces from
``uk_registry.projection``, and a generated row is found by what it is, its kind, its S
policy and its month (``_row``), so neither a renumbered table nor the C step's positions
can point a test at the wrong row.  And a timing or a kind is passed through ``_code``,
which gives the model's int Reference of its name where the model has one, as at stage
``"EC"`` it does, and the string at stage ``"E"``; every comparison with S passes
``uk_sec_support.codes``, which maps S's strings onto the codes.
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
    SEC_SPECS, TWIN_EXEMPT_DEFAULT, build_sec_table, check_generated, codes, compiled_case,
    compiled_mismatches, exact_here, fingerprint_mismatches, frame_mismatches, full_sweep,
    label_mismatches, labels_refusing_non_text, reporting_cells, run_compiled, sweep,
    temp_inputs, twin_mismatches)
from uk_sec_support import _WP_CODED, _wp_c4_also
from uk_sec_support import generated_columns

SEC, TWIN = "WP_UK_SEC", "WP_UK_S"
TABLE = "model_point_table_sec.csv"
SPEC = SEC_SPECS[SEC]

# S's seven points: the worked example's bond in force 60 months at +7% (1) and -15% (2),
# on a 5% return (3), and with the 5% withdrawal election (4); the endowment issued at the
# valuation date (5) and in force 240 months on a gross pension basis (6); and the down
# scenario's bond issued at the valuation date with the withdrawal election (7), the bond
# variant the spec adds to S's table.
S_POINTS = (1, 2, 3, 4, 5, 6, 7)

# Eleven more S points, in the splice's copy of S's table and never in the committed one,
# each one of S's points changed so as to reach what S's own points cannot:
#
# 8, S point 1 as a woman: the mortality table's female rows, which no S point reads;
# 9, S point 2 at -40%, the crash the S module uses: the corridor's ceiling binding a
#   month after the cap's floor, the charge cap from 115 and the asset share floored from
#   154;
# 10, S point 3 on the pension tax basis: a bond on the other basis, which no S bond holds;
# 11, S point 7 at 5% without withdrawals: a bond issued at the valuation date whose charge
#   cap binds from 442, the cap a +5% bond reopened late without its charges misses;
# 12, S point 7 at 5% with them: its cap from 197, and its units exhausted at 303;
# 13, S point 7 without withdrawals: the -15% bond issued at the valuation date, its charges
#   stopping from 101, which a bond reopened at 60 without them would charge on past;
# 14, S point 2 at a 6% bonus: under the rule, its first declaration in S's rule, at 83, cut
#   by the change cap, 1.5%, to 4.5%, above the floor;
# 15, S point 1 at a 12% return and a 20% bonus: its guarantee outruns its asset share,
#   whose rise outruns the smoothed payout, so that the MVR is held to its contractual
#   bound, the guarantee less the asset share, from 71;
# 16, S point 7 at 5% with a 6% withdrawal: under the rule its units run out at policy
#   month 287, so its frame ends the month before a declaration, the bonus rate's frame
#   bound at its edge;
# 17, S point 4 withdrawing a little more: its units run out at policy month 779, the last
#   month of its cover, issued at 55 to 120, which the exhaustion search reads last;
# 18, S point 4 withdrawing a little more again: its units run out a month earlier, at 778.
#   Each rate is the middle of the window of rates whose units run out in that month,
#   measured at M14 by bisection; neither moves with the main set's References.
#
# Each variant is (the S point it changes, the columns it changes); the policy_id keeps the
# generated ids apart.  11 to 13 are new business, so their twins are cases too: an issue
# month no S bond but point 7 takes.
VARIANTS = {
    8: (1, {"policy_id": "WP-900008", "sex": "F"}),
    9: (2, {"policy_id": "WP-900009", "fund_return": -0.40}),
    10: (3, {"policy_id": "WP-900010", "tax_basis": "pension_gross"}),
    11: (7, {"policy_id": "WP-900011", "wd_rate": 0.0, "fund_return": 0.05,
             "bonus_rate": 0.02}),
    12: (7, {"policy_id": "WP-900012", "fund_return": 0.05, "bonus_rate": 0.02}),
    13: (7, {"policy_id": "WP-900013", "wd_rate": 0.0}),
    14: (2, {"policy_id": "WP-900014", "bonus_rate": 0.06}),
    15: (1, {"policy_id": "WP-900015", "fund_return": 0.12, "bonus_rate": 0.20}),
    16: (7, {"policy_id": "WP-900016", "fund_return": 0.05, "bonus_rate": 0.02,
             "wd_rate": 0.06}),
    17: (4, {"policy_id": "WP-900017", "wd_rate": 0.0311508}),
    18: (4, {"policy_id": "WP-900018", "wd_rate": 0.0311735}),
}

# T2's months under the main set of References (UKLIB-SEC-PLAN.md §6.5), S months, each
# after the point's own entry and inside its frame.  The declarations at the end of each
# policy year's twelfth month, 71, 119, and on the endowment 11 and 287, the month after
# each and mid-year; on the down scenario the smoothing cap's floor from 61, the market
# value reduction from 68, the corridor's ceiling from 92, the guarantee window, 106, 107
# and 118 to 120, the encashment at 119, the corridor again at 131, 144, 154 and 155, the
# charge's cap from 160 and the asset share's floor from 242; the 5% bond's cap from 504,
# where it flickers monthly; the withdrawing bond's cap from 284 and its exhaustion at
# 403, its last month 402; on the endowment the cap's ceiling at 289 and 290 and maturity
# at 299; the bond variant's cap from 88, and past it at 100, its floor from 196 and its
# last month, 266; and the limiting age's last month, 779.  The events are S's under
# SPLICED_REFS, whose estate
# distribution moves the charge's cap and the floor a few months from where S ships them.
SPLICE_MTHS = {
    1: (61, 65, 71, 72, 119, 120, 125, 778, 779),
    2: (61, 64, 65, 67, 68, 71, 72, 92, 93, 106, 107, 118, 119, 120, 125, 131, 144, 154,
        155, 159, 160, 161, 241, 242, 243, 600, 779),
    3: (71, 72, 503, 504, 505, 779),
    4: (65, 71, 119, 283, 284, 285, 396, 401, 402),
    5: (1, 11, 12, 13, 65, 125, 287, 288, 289, 290, 299),
    6: (241, 287, 288, 289, 290, 299),
    7: (1, 11, 12, 87, 88, 89, 100, 106, 107, 119, 120, 195, 196, 197, 266),
}
VARIANT_MTHS = {8: (65, 119, 779), 9: (61, 65, 66, 71, 92, 115, 116, 119, 153, 154),
                10: (71, 119), 11: (1, 441, 442, 443), 12: (1, 196, 197, 198, 302),
                13: (1, 100, 101, 102, 600), 15: (71, 85), 17: (777,), 18: (777,)}

# The second set's months, with the bonus rule on: each declaration the rule sets, the
# first in S's frame at 83 on the bonds in force and at 11 and 23 on the bonds issued at the
# valuation date, the month after it and mid-year; the endowment's; and the withdrawing
# variant's frame, whose units run out at policy month 400 under the rule, in its 34th
# policy year, the partial year whose rate the frame bounds: restated before that year, at
# 395, and inside it, at 397, where its rate is the row's own.
RULE_MTHS = {1: (61, 83, 84, 125), 2: (83, 84, 119), 5: (11, 12, 13, 150, 299),
             7: (1, 23, 24, 100), 12: (1, 302, 395, 397), 14: (83, 95), 16: (275, 280)}

# The third set's months, a deterrent of 25, under which the surrender rate is held to its
# bound, 1, wherever the market value reduction applies: the down scenario the month before
# it turns on, 67.
BOUND_MTHS = {2: (67,)}

# T3's months: issued one month on, which puts the policy anniversaries a month off the
# valuation years; twelve, which puts them back on; and the horizon, 120, the latest the
# table admits.  Each new-business variant is issued 13 months on, more than a year after
# the valuation date and off its anniversaries (USLIB-SEC-PLAN.md §7.1, *Record — M14*,
# *Splice grid*).  The endowment is closed to new business, and is issued later all the
# same, as a projection's mechanics.
FUTURE_MTHS = (1, 12, 120)
LATE_FUTURES = ((11, 13), (12, 13), (13, 13))


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


# The month each S point and variant enters S's frame: 60 on the bonds in force, 240 on the
# endowment in force, 0 on new business.
ENTRY = {p: 12 * int(y) for p, y in _s_table_with_variants()["duration_inforce"].items()}

# The committed rows the generator reads from S under References of their own (the spec's
# derived_refs), by (S policy, month), with those References.
UNDER_REFS = {(_s_table().at[p, "policy_id"], d): refs
              for (p, d), refs in SPEC.derived_refs.items()}

# T2's cases, as (row_kind, S point, source_mth, set): each S point and variant restated in
# force at each of its months, and the twins of S's points in force, at their own months,
# and of the new business, at 0, on each set.  T3's cases, as (S point, k, set).
SPLICES = (tuple(("derived", p, d, "main") for p in S_POINTS for d in SPLICE_MTHS[p])
           + tuple(("derived", p, d, "main") for p, mths in VARIANT_MTHS.items()
                   for d in mths)
           + tuple(("derived", p, d, "rule") for p, mths in RULE_MTHS.items()
                   for d in mths)
           + tuple(("derived", p, d, "bound") for p, mths in BOUND_MTHS.items()
                   for d in mths))
IN_FORCE_TWINS = (tuple(("twin", p, ENTRY[p], "main") for p in (*S_POINTS, *VARIANTS))
                  + tuple(("twin", p, ENTRY[p], "rule") for p in (1, 5, 6, 7, 12)))
FUTURES = (tuple((p, k, "main") for p in (5, 7) for k in FUTURE_MTHS)
           + tuple((p, k, "main") for p, k in LATE_FUTURES)
           + ((7, 13, "rule"), (12, 13, "rule")))

# The default run's cases (the module docstring), each with what it is there for.  The
# rest of SPLICES, IN_FORCE_TWINS and FUTURES run with UKLIB_SEC_FULL=1.
CORE_SPLICES = {
    ("twin", 1, 60, "main"): "S's worked example in force, an anniversary valuation",
    ("twin", 4, 60, "main"): "S's withdrawing bond in force, to its exhaustion",
    ("twin", 6, 240, "main"): "S's endowment in force, to maturity",
    ("twin", 7, 0, "main"): "the bond variant issued at the valuation date",
    ("derived", 1, 71, "main"): "a declaration at the end of month 0",
    ("derived", 1, 779, "main"): "the limiting age's last month, a one-row frame",
    ("derived", 2, 65, "main"): "mid-year, the smoothing cap's floor binding",
    ("derived", 2, 68, "main"): "the market value reduction turning on",
    ("derived", 2, 92, "main"): "the corridor's ceiling binding",
    ("derived", 2, 107, "main"): "inside the guarantee-imminent window",
    ("derived", 2, 119, "main"): "the guarantee date in month 0, the encashment",
    ("derived", 2, 242, "main"): "the asset share floored at 0, the payout with it",
    ("derived", 3, 504, "main"): "the 5% bond as its charge cap binds",
    ("derived", 4, 402, "main"): "the withdrawing bond's last month, a forced encashment",
    ("derived", 5, 1, "main"): "the endowment in its second month",
    ("derived", 5, 11, "main"): "the endowment's first declaration in month 0",
    ("derived", 5, 290, "main"): "the endowment's payout at the cap's ceiling",
    ("derived", 5, 299, "main"): "the endowment's maturity, a one-row frame",
    ("derived", 7, 100, "main"): "the bond variant past its charge cap",
    ("derived", 7, 266, "main"): "the bond variant's last month, floored and exhausted",
    ("derived", 17, 777, "main"): "units running out in the last month of cover",
    ("derived", 18, 777, "main"): "units running out a month before the last of cover",
    ("derived", 8, 119, "main"): "a woman on her guarantee date",
    ("derived", 9, 92, "main"): "the -40% crash, the corridor's ceiling binding",
    ("derived", 10, 71, "main"): "a bond on the pension tax basis",
    ("derived", 11, 443, "main"): "the +5% bond issued at t = 0, past its charge cap",
    ("derived", 13, 102, "main"): "the -15% bond issued at t = 0, past its charge cap",
    ("twin", 1, 60, "rule"): "S's worked example in force: its first declaration, D6's",
    ("derived", 1, 83, "rule"): "the rule's declaration as month 0's own event",
    ("derived", 1, 84, "rule"): "the rule's year under way, from S's declared rate",
    ("derived", 2, 84, "rule"): "the down scenario under the rule, its rate floored",
    ("derived", 5, 150, "rule"): "the endowment under the rule, mid-term",
    ("derived", 12, 302, "rule"): "the withdrawing bond under the rule, to its cut year",
    ("derived", 14, 83, "rule"): "a 6% rate the rule cuts by its cap, above the floor",
    ("derived", 16, 280, "rule"): "a frame ending the month before a declaration",
    ("derived", 15, 71, "main"): "a 20% bonus on a 12% return: the MVR at its bound",
    ("derived", 2, 67, "bound"): "a deterrent of 25: the surrender rate at its bound",
}
CORE_FUTURES = {
    (7, 1, "main"): "the bond variant a month off the valuation anniversaries",
    (12, 13, "rule"): "the withdrawing bond more than a year on, under the rule",
}

SEC_FULL = os.environ.get("UKLIB_SEC_FULL") == "1"
FULL_ONLY = (pytest.mark.sec_full,
             pytest.mark.skipif(not SEC_FULL, reason="the full splice grid runs with "
                                "UKLIB_SEC_FULL=1 (UKLIB-SEC-PLAN.md U6)"))

# The tests that run over every committed point run the core's by default and the rest on
# the full grid (GRIDS): the in-force twins of S's withdrawing bond and its endowment, the
# bond issued at the valuation date, the down scenario on its guarantee date and with its
# asset share floored, the withdrawing bond's last month, the endowment at its first
# declaration, the bond variant past its cap, the future row and the rows under the
# doubled charge and under the rule, by label, among which every flow and every counted
# cell is nonzero.
CORE_POINTS = (4, 6, 7, 11, 12, 14, 15, 18, 19, 20, 22)
GRIDS = [pytest.param("core", id="core"), pytest.param("full", id="full", marks=FULL_ONLY)]


def _on_grid(grid, label):
    """Whether committed point ``label`` is one the ``grid`` case of a test runs on."""
    return (label in CORE_POINTS) == (grid == "core")


# What the main splice sets in both models, S and SEC alike, before either evaluates
# anything.  One input runs on the valuation clock (D7): expense inflation, which S runs
# from issue and SEC from the valuation date, so at the shipped 3% the expenses of a point
# opened at d differ by the inflation of the policy years before d, by design, and at 0 both
# factors are 1; its clock is then asserted on its own, with its rate on.  The fund return
# and the bonus rate are levels of the model point, no path, so no input table moves with
# d.  The one assumption that ships at zero, the estate distribution, is on, at a hundredth
# of a percent of the asset share a month, so that the opening asset share feeds it in
# every month.  And two References a formula could confuse with another that ships equal
# are set apart from it: the MVR deterrent, which ships at the 0.6 of mortality's
# best-estimate factor, at 0.65, and the guarantee-imminent factor, which ships at the 0.8
# of the corridor's floor, at 0.75.  The identity does not depend on the values, only on
# both models having the same ones.  The bonus rule ships off, and the second set switches
# it on (RULE_REFS).
SPLICED_REFS = {"inflation_rate": 0.0, "misc_surplus_rate": 0.0001,
                "mvr_deterrent_factor": 0.65, "guarantee_imminent_factor": 0.75}

# The second set: the main one with the bonus rule on, its guarantee-fill target and its
# annual change cap set apart from the corridor's floor and the annual management charge
# they ship equal to.
RULE_REFS = {**SPLICED_REFS, "bonus_rule_on": True, "guar_fill_target": 0.85,
             "bonus_change_cap": 0.015}
# The third set: the main one with the MVR deterrent at 25, which takes the surrender rate
# to its bound, 1, wherever the market value reduction applies (UKLIB-SEC-PLAN.md §6.5;
# ULB_UK_SEC's T2 variant for its own bound).
BOUND_REFS = {**SPLICED_REFS, "mvr_deterrent_factor": 25.0}
REF_SETS = {"main": SPLICED_REFS, "rule": RULE_REFS, "bound": BOUND_REFS}

# Every switch that ships off, on, for T4, at the shipped inflation: the second set's.
SWITCHED_ON = {ref: value for ref, value in RULE_REFS.items() if ref != "inflation_rate"}

# The accessors of S's columns that open its frame: on a row restated at d, S's value is
# the column at S's own opening, 60 or 240 or issue, and SEC's the state at d, by design;
# the cells they open are compared.  And declaration_month, which S returns as a policy month
# and SEC as a valuation month, the same number only where the clocks coincide; a test of
# its own holds its form.
OPENING = frozenset({"asset_share_init", "units_init", "unit_price_init",
                     "smoothed_payout_init", "bonus_rate_init"})

# The reports, which the comparison reads as frames rather than as cells.
REPORTS = ("result_cf", "result_payout", "result_pols")

# The cells T2 and T3 skip beyond T1's (the spec's exempt): proj_len counts from the
# valuation date on SEC and from issue on S, so it differs by d, or by -k, by design;
# frame_mismatches asserts what it must get right, that both frames end at the same
# instant.  OPENING's, for their reason.  And the reports, compared as frames.
SPLICE_EXEMPT = (TWIN_EXEMPT_DEFAULT | SPEC.exempt | OPENING
                 | {"proj_len", "declaration_month", *REPORTS})
FUTURE_EXEMPT = SPLICE_EXEMPT

# The result_cf columns that expense inflation moves, and the cells they are made of: on
# the committed points, at the shipped 3%, the only places an in-force row departs from S.
INFLATED = ("expenses", "net_cf")
INFLATION_CELLS = frozenset({"inflation_factor", "expenses", "net_cf"})

# The S cells whose exact value is 0 and whose computed value is rounding about it, the
# roll-forwards' residuals: a comparison with S holds them at the harness's absolute floor
# of 1e-9, and every other cell at none (_compare).
RESIDUALS = frozenset({"check_pols_roll_fwd_resid", "check_asset_share_roll_fwd_resid"})
FLOOR = 1e-9

# The S cells whose value is the difference of two amounts equal in many months: the
# smoothing cost of an exit, the claim less the asset share it releases.  Where the payout
# is the asset share, the computed value is rounding about 0 at the asset share's last
# bit, 2.9e-11 on the 5% bond at 487, and an opening state read back from the CSV one ulp
# off moves it, so a comparison holds it to the residuals' floor (_compare).
DIFFERENCES = frozenset({"smoothing_cost_pp"})
FLOORED = RESIDUALS | DIFFERENCES

# The reads keyed by an attained age or a policy year, and the monthly rates, none of which
# may be evaluated before issue (R1, D4).
KEYED_READS = ("age", "duration", "policy_year", "mort_rate", "surr_rate_base",
               "mort_rate_mth", "surr_rate_mth")

# The cells that scale with the count, the two counted chains' year openings among them.
# Every other cell is a per-policy amount, a rate, a factor, a clock or a flag, and must not
# move when the count does.
COUNTED = frozenset({
    "policy_count", "pols_if_init", "pols_if", "pols_if_at", "pols_if_py", "pols_new_biz",
    "pols_death", "pols_surr", "pols_maturity", "premiums", "withdrawals", "claims",
    "expenses", "shareholder_transfers", "smoothing_cost", "smoothing_account",
    "smoothing_account_py", "smoothing_account_refusal", "net_cf",
    "check_pols_roll_fwd_resid", "result_cf", "result_payout", "result_pols"})

# result_pols' columns, in its order: the count, the new business within it, the month's
# deaths and surrenders in processing order, and the survivors of the frame's last month.
RESULT_POLS = ["pols_if", "pols_new_biz", "pols_death", "pols_surr", "pols_maturity"]

# result_payout's columns: each a per-policy amount or a rate, but the smoothing account,
# which sums the exits of the count.
PAYOUT_COUNTED = ("smoothing_account",)

# S's three timings and BEF_NB, the one running in force adds; the asset share's six; and
# the kinds.
TIMINGS = ("BEF_NB", "BEF_DECR", "BEF_SURR", "AFT_DECR")
AS_TIMINGS = ("BEF_PREM", "BEF_RETURN", "AFT_RETURN", "AFT_CHARGE", "AFT_ST", "AFT_MC")
KINDS = ("DEATH", "SURRENDER", "MATURITY")
CLAIM_KINDS = ("DEATH", "SURRENDER", "GUARANTEE", "MATURITY")

# What each cell holds outside cover, before issue and from the month cover has ended, as
# its docstring says: no count, so no cash flow; no balance, price or rate read at a policy
# year or an age the policy does not have; no declaration, guarantee date or window.  The
# type is part of the value.  A count is a float in every branch and a flag a bool, because
# the C step types a cell by the values it returns (USLIB-SEC-PLAN.md F3).  The guard test
# also calls pols_if_at at each timing and asset_share_at at each, all 0.0.
OUTSIDE_COVER = {
    "is_active": False, "is_declaration_month": False, "is_guarantee_date": False,
    "premium_pp": 0.0, "wd_pp": 0.0, "wd_as_pp": 0.0, "guar_charge_rate": 0.0,
    "guar_charge_rate_mth": 0.0, "guar_charge_pp": 0.0, "guar_charge_cum_pp": 0.0,
    "misc_surplus_pp": 0.0, "asset_share": 0.0, "unit_price": 0.0, "units": 0.0,
    "guar_benefit_pp": 0.0, "guar_benefit_open": 0.0, "bonus_rate": 0.0,
    "cost_of_bonus_pp": 0.0, "shareholder_transfer_pp": 0.0, "mort_rate": 0.0,
    "mort_rate_mth": 0.0, "mort_charge_pp": 0.0, "smoothed_payout": 0.0,
    "smoothed_payout_open": 0.0, "final_bonus_pp": 0.0, "mvr_pp": 0.0,
    "mvr_applied_pp": 0.0, "surr_rate_base": 0.0, "surr_rate": 0.0, "surr_rate_mth": 0.0,
    "pols_if": 0.0, "pols_new_biz": 0.0, "pols_death": 0.0, "pols_surr": 0.0,
    "pols_maturity": 0.0, "premiums": 0.0, "withdrawals": 0.0,
    "expenses": 0.0, "shareholder_transfers": 0.0, "smoothing_cost": 0.0,
    "smoothing_account": 0.0, "net_cf": 0.0, "check_pols_roll_fwd_resid": 0.0}

# The cells a month outside cover may not reach: the clocks of the contract, each keyed
# by a policy year or an attained age.  The reads that guard themselves are held by their
# values in OUTSIDE_COVER instead.
IN_COVER_ONLY = ("age", "policy_year", "duration")

# The opening state, in the table's order, and the cells running in force adds to
# WP_UK_S's, each of which the symbol map must name.
STATE = ("units_init", "unit_price_init", "attaching_bonus_init", "asset_share_init",
         "smoothed_payout_init", "bonus_rate_init", "guar_charge_cum_pp_init",
         "smoothing_account_init")
NEW_CELLS = ("policy_count", "duration_mth_init", "t_entry", "is_active", "cover_end_mth",
             "pols_new_biz", "result_pols", "attaching_bonus_init", "guar_charge_cum_pp_init",
             "smoothing_account_init")

# The cells the C step adds (UKLIB-SEC-PLAN.md §6.5, *C*), each of which the symbol map must
# name too: the label of the point at idx; the chassis and the sex decoded, the lapse
# table's extent and the guarantee dates' reader by policy year; and the openings of the
# year the eight chains are blocked by.
OPENINGS = ("pols_if_py", "asset_share_py", "smoothed_payout_py", "guar_benefit_pp_py",
            "units_py", "unit_price_py", "guar_charge_cum_pp_py", "smoothing_account_py")
EC_CELLS = ("point_id", "chassis_code", "mort_schedule", "lapse_last_year",
            "is_guarantee_year", *OPENINGS)

INFLATION = 0.03        # the shipped inflation_rate, which the inflation test reads

# The edges of the floats the domains and the past-the-floats cases read.
BIG = 1.7976931348623157e308
WHOLE = 2.0 ** 53
BELOW_0 = math.nextafter(0.0, -1.0)
ABOVE_0 = math.nextafter(0.0, 1.0)
ABOVE_1 = math.nextafter(1.0, 2.0)
BELOW_1 = math.nextafter(1.0, 0.0)

# The recursion limit, as mx.set_recursion takes it, under which the committed points are
# first swept (R2, F7).  A report evaluates each column in ascending t, so a forward
# recursion, through t - 1, finds the month before already cached.  A backward recursion
# over the frame, through t + 1, opens a chain as long as the frame, and the shortest
# committed frame of more than a row is 167.
CALL_DEPTH = 60

# The reads beyond t + 1 the model makes, as (reader, cell read): the bonus rate's read of
# the rate of the declaration closing its policy year, up to 11 months ahead, R2's
# anniversary read, with the bonus rule on.  The rules test admits it, and asserts each
# such read lies inside the frame.  The exhaustion search reads the units of the month
# they run out, from a cell that takes no month, which a test of its own holds.
LOOK_AHEAD = frozenset({("bonus_rate", "bonus_rate")})


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

    ``month`` is the row's ``source_mth``: S's entry month for a twin, ``d`` for a derived
    row, ``-k`` for a future one.  The twins keep S's ``point_id`` and ``policy_id``, so the
    S policy is the twin's.
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
    --block`` releases its points (USLIB-SEC-PLAN.md F5).  Asked for again, the ItemSpace is
    made afresh and recomputes.
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
    """WP_UK_SEC read from a copy whose SEC table is ``edit(_committed())``."""
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

    :func:`uk_sec_support.sweep` reaches ``WP_UK_S``'s ``pols_if_at`` at two of its
    timings, ``asset_share_at`` at the timings the recursion reads, and ``claim_pp`` and
    ``smoothing_cost_pp`` at the kinds the flows read; nor ``duration_mth``, which no S
    formula reads, nor ``policy_value_pp``, ``is_guarantee_date``, ``guarantee_imminent`` or
    ``death_guar_pp`` where no flow asks.  A cell S never evaluates is compared nowhere, so
    they are evaluated here, over the frame, and the splice and the future comparison see
    them too.
    """
    sweep(proj)
    for t in range(proj.proj_start(), proj.proj_len()):
        for timing in ("BEF_DECR", "BEF_SURR", "AFT_DECR"):
            proj.pols_if_at(t, timing)
        for timing in AS_TIMINGS:
            proj.asset_share_at(t, timing)
        for kind in CLAIM_KINDS:
            proj.claim_pp(t, kind)
            proj.smoothing_cost_pp(t, kind)
        proj.duration_mth(t)
        proj.policy_value_pp(t)
        proj.policy_value_open(t)
        proj.is_guarantee_date(t)
        proj.guarantee_imminent(t)
        proj.death_guar_pp(t)
        proj.guar_benefit_open(t)
        proj.smoothed_payout_capped(t)


def _departure(s_proj, month):
    """Where SEC's bonus rate departs from S's by design on a row: ``(S month, rate)``, or
    ``None``.

    With the bonus rule on, each month reads the rate declared at the end of its policy
    year.  Where a forced encashment ends the frame mid-year, no declaration falls in the
    frame in the year it ends in, and S reads the rate past its frame, where this model
    reads the rate declared before the year (``bonus_rate``'s docstring, the recorded
    departure).  So the months of that year, S months from its first, ``12 x ((L - 1) //
    12)``, to the frame's last, ``L - 1``, S's policy months, are the departure, unless the
    year is the one under way at the row's valuation date, S month ``month``, whose rate is
    the row's column and S's own; returned with the rate this model reads there, S's of
    the year before, declared the month before the year.  It changes ``bonus_rate`` in
    those months, and the ``bonus_rate`` column of ``result_payout``, and no other cell: no
    declaration falls in them.
    """
    if not (s_proj.bonus_rule_on and s_proj.is_forced_encashment()):
        return None
    end = s_proj.proj_len()
    first = 12 * ((end - 1) // 12)
    if end % 12 == 0:
        return None
    return first, s_proj.bonus_rate(first - 1)


def _carried_cut(s_proj, month):
    """The S month of a row's first declaration in the frame, where S makes it from its
    carried column rather than by its rule; or ``None``.

    Under the rule every declaration in this model's frame is the rule's, at today's
    References (D6), but ``WP_UK_S``'s first frame year keeps its column: so a twin of S's
    points, in force or new, and a row valued inside S's first frame year, part from S at
    their first declaration in the frame, the departure ``model-sec.md`` records.  The
    comparison runs to the month before it, S month ``cut``, but on the ``bonus_rate``,
    which every month of the year reads from that declaration.
    """
    if not s_proj.bonus_rule_on:
        return None
    first = 11 if month < 0 else 12 * (month // 12) + 11
    if first <= s_proj.proj_start() + 11 and first < s_proj.proj_len():
        return first
    return None


def _s_result_pols(s_proj):
    """S's counts as ``result_pols`` sets them out, from S's own cells.

    ``WP_UK_S`` has no ``result_pols``: its frame's rows are S months from
    ``proj_start()``, each holding S's ``pols_if``, ``pols_death``, ``pols_surr`` and
    ``pols_maturity``, and the new business is the count S opens a frame from issue with,
    ``pols_if_init()``, in its month 0.
    """
    ts = list(range(s_proj.proj_start(), s_proj.proj_len()))
    new = s_proj.pols_if_init() if s_proj.proj_start() == 0 else 0.0
    return pd.DataFrame(
        {"pols_if": [s_proj.pols_if(t) for t in ts],
         "pols_new_biz": [new if t == 0 else 0.0 for t in ts],
         "pols_death": [s_proj.pols_death(t) for t in ts],
         "pols_surr": [s_proj.pols_surr(t) for t in ts],
         "pols_maturity": [s_proj.pols_maturity(t) for t in ts]},
        index=pd.Index(ts, name="t"))


def _compare(s_proj, sec_proj, month, exempt, columns=None):
    """Where SEC's row departs from S's point from S month ``month`` on, in three passes.

    First the frames, ``result_cf`` (over ``columns``, or every column both hold),
    ``result_payout`` and ``result_pols``, SEC row ``t`` against S row ``t + month``, frames
    ending together; then every cell of S's but ``exempt`` and :data:`RESIDUALS`, at every
    argument S cached inside its frame from ``month`` on, moved onto SEC's clock, S's
    timing and kind strings mapped onto SEC's codes (``uk_sec_support.codes``).  Both to
    1e-9 relative with no absolute floor (USLIB-SEC-PLAN.md §5.2, T2, precised at M11): a
    floor of 1e-9 passes an error of 1% in any value below 1e-7.  Then the cells of
    :data:`RESIDUALS` and :data:`DIFFERENCES` alone, at the floor of 1e-9: a residual's
    exact value is 0, and a difference's is in many months, and the computed one moves by
    an ulp of what it closes when an opening state comes back from the CSV one ulp off.  The
    bonus rate's recorded departure in a cut year (:func:`_departure`) is compared over the
    months before it, and held to its own rate in its months; a row whose first declaration
    S makes from its carried column (:func:`_carried_cut`) is compared to the month before
    that declaration.  Returns the mismatch lines, empty when the row is S's.
    """
    found = []
    cut = _carried_cut(s_proj, month)
    gone = None if cut is not None else _departure(s_proj, month)

    def arg_map(name, args):
        args = SPEC.twin_arg_map(name, args)
        if cut is not None and (name == "bonus_rate"
                                or (args and _month(args[0]) and args[0] >= cut)):
            return None
        if gone is not None and name == "bonus_rate" and args[0] >= gone[0]:
            return None
        return args

    for report, keep in (("result_cf", columns), ("result_payout", None),
                         ("result_pols", None)):
        sec_df = sec_proj.cells[report]()
        s_df = (_s_result_pols(s_proj) if report == "result_pols"
                else s_proj.cells[report]())
        if cut is not None:
            if cut <= month:
                continue                    # month 0's declaration: nothing before it
            names = [c for c in (s_df.columns if keep is None else keep)
                     if c in sec_df.columns and c != "bonus_rate"]
            found += [f"{report} before the first declaration: {line}"
                      for line in frame_mismatches(
                          s_df[s_df.index < cut], sec_df[sec_df.index < cut - month],
                          t_offset=month, columns=names, atol=0.0)]
            continue
        if report == "result_payout" and gone is not None:
            found += [f"{report}: {line}" for line in frame_mismatches(
                s_df, sec_df, t_offset=month,
                columns=[c for c in s_df.columns if c != "bonus_rate"], atol=0.0)]
            start = gone[0] - month
            if start > 0:
                found += [f"{report} before the departure: {line}"
                          for line in frame_mismatches(
                              s_df[s_df.index < gone[0]], sec_df[sec_df.index < start],
                              t_offset=month, columns=["bonus_rate"], atol=0.0)]
            held = sec_df.loc[sec_df.index >= start, "bonus_rate"]
            if not (held == gone[1]).all():
                found.append(f"the departure's months hold {sorted(set(held))}, not the "
                             f"rate declared before them, {gone[1]}")
            continue
        found += [f"{report}: {line}" for line in frame_mismatches(
            s_df, sec_df, t_offset=month, columns=keep, atol=0.0)]
    found += twin_mismatches(s_proj, sec_proj, t_offset=month, exempt=exempt | FLOORED,
                             arg_map=arg_map, atol=0.0, codes=codes(sec_proj))
    return found + twin_mismatches(s_proj, sec_proj, t_offset=month,
                                   exempt=exempt | (set(s_proj.cells) - FLOORED),
                                   arg_map=arg_map, atol=FLOOR, codes=codes(sec_proj))


def _continues_s(s_proj, sec_proj, month):
    """Where a committed row departs from S's point ``s_proj`` from S month ``month`` on.

    The splice's comparison (:func:`_compare`), on the committed model at the shipped
    assumptions: frame by frame, then cell by cell over every cell of S's but
    :data:`SPLICE_EXEMPT`.  The shipped 3% expense inflation runs from issue in S and from
    the valuation date here (D7), so :data:`INFLATED`'s two columns, and
    :data:`INFLATION_CELLS`, differ by design and are left out; the inflation test holds
    them.  Every other column and cell must agree, to 1e-9 relative, with no absolute floor
    but on the residuals.
    """
    keep = [c for c in s_proj.result_cf().columns if c not in INFLATED]
    return _compare(s_proj, sec_proj, month, SPLICE_EXEMPT | INFLATION_CELLS, keep)


def _case_id(kind, s_point, month, refs="main"):
    """A case's id: ``point2-d119``, ``point2-twin60-rule``, or ``point7-k13`` if issued
    later."""
    tail = "" if refs == "main" else f"-{refs}"
    if kind == "future":
        return f"point{s_point}-k{-month}{tail}"
    return f"point{s_point}-" + (f"d{month}" if kind == "derived" else f"{kind}{month}") + tail


def _case(case, core, case_id):
    """One parametrized case: run by default if it is in ``core``, else on the full grid."""
    return pytest.param(*case, id=case_id, marks=() if case in core else FULL_ONLY)


def _selected(cases, core):
    """The cases this run makes rows for: the core, or every one under UKLIB_SEC_FULL."""
    return [case for case in cases if SEC_FULL or case in core]


# Every row the splice compares, as (row_kind, S point, source_mth, set), T3's included,
# and the default run's among them.
GRID = (*SPLICES, *IN_FORCE_TWINS, *(("future", p, -k, refs) for p, k, refs in FUTURES))
CORE_GRID = frozenset({*CORE_SPLICES, *(("future", p, -k, refs)
                                        for p, k, refs in CORE_FUTURES)})


# ---------------------------------------------------------------------------
# Fixtures


@pytest.fixture(scope="module")
def sec_read():
    """WP_UK_SEC read in place, as committed, and swept once, cold; what it met.

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
    first = _row(model, "twin", 1, 60)
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
    """WP_UK_SEC read in place, as committed, with every point swept (sec_read)."""
    return sec_read[0]


@pytest.fixture(scope="module")
def s_model():
    """WP_UK_S read in place, as committed, with every point swept.

    T6 regenerates the SEC inputs from it, which would otherwise project every S point
    again (USLIB-SEC-PLAN.md §4, *Carried into Phase 1*), and the in-force tests read S's
    months off it.
    """
    model = mx.read_model(model_path(TWIN), name=_name("s"))
    for key in point_keys(model):
        _sweep_s(projection(model, key))
    yield model
    model.close()


def _spliced_pair(root, refs, set_name):
    """S and SEC on one set of the splice's inputs, ``refs`` set in both: see
    :func:`spliced`."""
    chosen = [case for case in _selected(SPLICES + IN_FORCE_TWINS, CORE_SPLICES)
              if case[3] == set_name]
    derived = [(p, d) for kind, p, d, _ in chosen if kind == "derived"]
    futures = [(p, k) for p, k, refs_name in _selected(FUTURES, CORE_FUTURES)
               if refs_name == set_name]
    compared = {p for _, p, _, _ in chosen} | {p for p, _ in futures}
    s_folder = temp_inputs(root / "s", model_path(TWIN),
                           model_points=_s_table_with_variants().loc[sorted(compared)])
    s = mx.read_model(s_folder, name=_name(f"s_{set_name}"))
    for ref, value in refs.items():
        setattr(s.Projection, ref, value)
    spec = dataclasses.replace(SPEC, derived=tuple(derived), derived_refs={},
                               future=tuple(futures))
    table, companions = build_sec_table(spec, s)
    assert companions == {}
    sec = mx.read_model(_sec_inputs(root / "sec", table), name=_name(f"sec_{set_name}"))
    for ref, value in refs.items():
        setattr(sec.Projection, ref, value)
    for key in point_keys(s):
        _sweep_s(projection(s, key))
    return s, sec


@pytest.fixture(scope="module")
def spliced(tmp_path_factory):
    """S and SEC on each set of the splice's inputs, ``{set: (s, sec)}``.

    For each set, :data:`SPLICED_REFS`, :data:`RULE_REFS` and :data:`BOUND_REFS`, S is read
    from a copy of the product directory whose table holds the points and variants the
    set's selected cases compare, and no other, with the set's References set: the
    generator writes a twin of every point S holds, and under the rule each withdrawing
    bond's exhaustion search runs through the asset share, so a point no case compares
    would cost a set's build its projection for nothing (the M13 verification).
    SEC runs on the same assumption tables, and on a model point table of its own, built by
    the generator from the registered spec with its rows replaced by the set's cases this
    run selects, the core or the full grid (:func:`_selected`), out of this S model, so each
    row opens with the state of the very run it is compared with.  No input table moves
    with ``d``: WP's one valuation-clock input is the ``inflation_rate`` Reference.  Every S
    point is then swept (:func:`_sweep_s`), and stays swept; each SEC row is projected by
    the case that compares it and released once compared (:func:`_settle`).
    """
    root = tmp_path_factory.mktemp("spliced")
    pairs = {name: _spliced_pair(root / name, refs, name) for name, refs in REF_SETS.items()}
    yield pairs
    for s, sec in pairs.values():
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
    "ahead": [...], "outside": [...], "raised": [...]}``: every cached call with a negative
    argument; every precedent keyed by a month before ``t_entry()`` of a call keyed by a
    month at or after it; every precedent keyed by a month beyond ``t + 1`` of a call keyed
    by ``t``, but :data:`LOOK_AHEAD`'s; every read :data:`LOOK_AHEAD` admits that lies past
    the frame, from a month inside it; and every call the full sweep found raising.  A
    precedent is a call's as modelx's dependency graph records it.
    """
    sweep(proj)
    raised = [f"{name}{args}: {text}" for (name, args), text in full_sweep(proj).items()]
    entry, end = proj.t_entry(), proj.proj_len()
    negative, early, ahead, outside = [], [], [], []
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
                if u <= t + 1:
                    continue
                if (name, node.obj.name) in LOOK_AHEAD:
                    if t < end <= u:
                        outside.append(f"{name}{args} -> {node.obj.name}{node.args}")
                    continue
                ahead.append(f"{name}{args} -> {node.obj.name}{node.args}")
    return {"negative": negative, "early": early, "ahead": ahead, "outside": outside,
            "raised": raised}


def _active(x, t):
    return x.is_active(t)


def _first_year(x):
    """The months of the policy year under way at the valuation date, on the books."""
    d = x.duration_mth_init()
    return range(x.t_entry(), x.t_entry() + 12 - max(d, 0) % 12)


# What test_the_core_grid_reaches_every_branch asks of the core's rows in the model's own
# values, which no column of the table shows: each holds of some core row, or of a core row
# in some month of its frame.  At the valuation date, every opening-state column in use, a
# count or an amount apart from its issue value, and each kind of valuation month: an
# anniversary, mid-year, a declaration month and a guarantee date, inside the
# guarantee-imminent window, and with the asset share floored.  Later in the frame, every
# branch and both sides of each min and max the full grid reaches: a declaration on each
# chassis and the cost of each, the smoothing cap's floor and ceiling and the cap skipped,
# the corridor's floor and ceiling, the asset share's floor, the market value reduction
# applied and waived on a guarantee date, the guarantee exercised, the imminent window,
# the charge's cap binding and released, a forced encashment and a maturity paid, the
# limiting age paying nothing, the lapse table inside and past its last year, and with the
# rule on a declaration set by it, its rise and its cut held to the cap and its rate floored
# at 0, a withdrawal capped at the unit fund, which it is in every withdrawing bond's issue
# month, its fund 0, the surrender rate at its bound, under a deterrent of 25, and the MVR
# held to its contractual bound.  Each at-valuation kind is keyed by the set its row runs
# under: the main set must reach every one, and the rule set its declarations' months.
AT_VALUATION = {
    "asset_share_init above 0": lambda x: x.asset_share_init() > 0.0,
    "asset_share_init 0 in force": lambda x: (
        x.duration_mth_init() > 0 and x.asset_share_init() == 0.0),
    "units_init above 0": lambda x: x.units_init() > 0.0,
    "unit_price_init above the seed": lambda x: x.unit_price_init() > 1.0,
    "attaching_bonus_init above 0": lambda x: x.attaching_bonus_init() > 0.0,
    "smoothed_payout_init above 0": lambda x: x.smoothed_payout_init() > 0.0,
    "guar_charge_cum_pp_init above 0": lambda x: x.guar_charge_cum_pp_init() > 0.0,
    "smoothing_account_init above 0": lambda x: x.smoothing_account_init() > 0.0,
    "smoothing_account_init below 0": lambda x: x.smoothing_account_init() < 0.0,
    "valued on an anniversary": lambda x: (
        x.duration_mth_init() > 0 and x.duration_mth_init() % 12 == 0),
    "valued mid-year": lambda x: x.duration_mth_init() % 12 not in (0, 11),
    "valued in a declaration month": lambda x: (
        x.duration_mth_init() > 0 and x.is_declaration_month(0)),
    "valued on a guarantee date": lambda x: (
        x.duration_mth_init() > 0 and x.is_guarantee_date(0)),
    "valued inside the guarantee-imminent window": lambda x: (
        x.duration_mth_init() > 0 and x.guarantee_imminent(0) != 1.0),
    "valued past the charge's cap": lambda x: (
        x.duration_mth_init() > 0 and x.guar_charge_rate(0) == 0.0),
    "an endowment in force": lambda x: (
        not x.is_unitised() and x.duration_mth_init() > 0),
    "a bond issued at or after the valuation date": lambda x: (
        x.is_unitised() and x.duration_mth_init() <= 0),
}
IN_FRAME = {
    "a declaration on the bond": lambda x, t: (
        x.is_unitised() and x.is_declaration_month(t) and x.cost_of_bonus_pp(t) > 0.0),
    "a declaration on the endowment": lambda x, t: (
        not x.is_unitised() and x.is_declaration_month(t) and x.cost_of_bonus_pp(t) > 0.0),
    "the smoothing cap skipped": lambda x, t: (
        _active(x, t) and x.smoothed_payout_open(t) <= 0.0),
    "the smoothing cap's floor": lambda x, t: (
        _active(x, t) and x.smoothed_payout_open(t) > 0.0
        and x.smoothed_payout_capped(t) == x.smooth_cap_dn_mth()
        * x.smoothed_payout_open(t) and x.asset_share(t) < x.smoothed_payout_capped(t)),
    "the smoothing cap's ceiling": lambda x, t: (
        _active(x, t) and x.smoothed_payout_open(t) > 0.0
        and x.smoothed_payout_capped(t) == x.smooth_cap_up_mth()
        * x.smoothed_payout_open(t) and x.asset_share(t) > x.smoothed_payout_capped(t)),
    "the corridor's floor": lambda x, t: (
        x.asset_share(t) > 0.0
        and x.smoothed_payout(t) == x.corridor_lo * x.asset_share(t)
        and x.smoothed_payout_capped(t) < x.smoothed_payout(t)),
    "the corridor's ceiling": lambda x, t: (
        x.asset_share(t) > 0.0
        and x.smoothed_payout(t) == x.corridor_hi * x.asset_share(t)
        and x.smoothed_payout_capped(t) > x.smoothed_payout(t)),
    "the asset share's floor": lambda x, t: (
        _active(x, t) and x.asset_share_at(t, _code(x, "AFT_MC")) < 0.0),
    "a market value reduction applied": lambda x, t: x.mvr_applied_pp(t) > 0.0,
    "a market value reduction waived on a guarantee date": lambda x, t: (
        x.is_guarantee_date(t) and x.mvr_pp(t) > 0.0),
    "the guarantee exercised": lambda x, t: x.guarantee_exercise(t) > 0.0,
    "the guarantee date out of the money": lambda x, t: (
        x.is_guarantee_date(t) and x.guarantee_exercise(t) == 0.0),
    "the guarantee-imminent window": lambda x, t: (
        _active(x, t) and x.guarantee_imminent(t) != 1.0),
    "the charge's cap binding": lambda x, t: (
        _active(x, t) and x.guar_charge_rate(t) == 0.0),
    "the charge's cap released": lambda x, t: (
        _active(x, t) and t > x.t_entry() and x.guar_charge_rate(t) > 0.0
        and x.guar_charge_rate(t - 1) == 0.0),
    "a forced encashment paid": lambda x, t: (
        x.is_unitised() and x.claim_pp(t, _code(x, "MATURITY")) > 0.0),
    "a maturity paid": lambda x, t: (
        not x.is_unitised() and x.claim_pp(t, _code(x, "MATURITY")) > 0.0),
    "the limiting age paying nothing": lambda x, t: (
        x.is_unitised() and not x.is_forced_encashment() and t == x.proj_len() - 1),
    "inside the lapse table": lambda x, t: (
        _active(x, t) and x.policy_year(t) <= x.lapse_last_year()),
    "past the lapse table's last year": lambda x, t: (
        _active(x, t) and x.policy_year(t) > x.lapse_last_year()),
    "a rate set by the rule": lambda x, t: (
        _active(x, t) and x.bonus_rule_on and x.is_declaration_month(t)),
    "a rule's rise held to its cap": lambda x, t: (
        _declared(x, t) and _rule_step(x, t)[1] == x.bonus_change_cap),
    "a rule's cut held to its cap, above the floor": lambda x, t: (
        _declared(x, t) and _rule_step(x, t)[1] == -x.bonus_change_cap
        and sum(_rule_step(x, t)) > 0.0),
    "a rule's rate floored at 0": lambda x, t: (
        _declared(x, t) and sum(_rule_step(x, t)) < 0.0),
    "a withdrawal capped at the unit fund": lambda x, t: (
        _active(x, t) and x.is_unitised() and x.wd_rate() > 0.0
        and x.wd_pp(t) < x.wd_rate() * x.premium_single_pp() / 12.0),
    "the surrender rate's bound": lambda x, t: _active(x, t) and x.surr_rate(t) == 1.0,
    "the MVR at its contractual bound": lambda x, t: (
        x.mvr_pp(t) > 0.0 and x.guar_benefit_pp(t) - x.asset_share(t)
        < x.guar_benefit_pp(t) - x.smoothed_payout(t)),
}

# The at-valuation kinds the rule set's core must reach as well as the main set's: the
# months the rule declares in, so that a core row holds a declaration as month 0's own
# event under the rule, and the months either side of one (the M13 review).
RULE_AT_VALUATION = ("valued on an anniversary", "valued mid-year",
                     "valued in a declaration month")
REACHED = frozenset({*(f"{what} [main]" for what in AT_VALUATION),
                     *(f"{what} [rule]" for what in RULE_AT_VALUATION), *IN_FRAME})


def _prev_rate(x, t):
    """The rate the declaration at the end of month ``t`` starts from: the one before it, or
    in the frame's first the rate declared before the valuation date."""
    return x.bonus_rate(t - 12) if t - 12 >= x.t_entry() else x.bonus_rate_init()


def _rule_step(x, t):
    """``(the rate the declaration at the end of month t starts from, its step clamped)``."""
    prev = _prev_rate(x, t)
    step = x.bonus_speed * (x.bonus_supportable(t) - prev)
    return prev, max(-x.bonus_change_cap, min(x.bonus_change_cap, step))


def _declared(x, t):
    """Whether month ``t`` carries a declaration the rule makes."""
    return _active(x, t) and x.bonus_rule_on and x.is_declaration_month(t)


def _branches(x, refs):
    """The names in :data:`AT_VALUATION`, keyed by ``refs``, the set the row runs under, and
    in :data:`IN_FRAME` that hold of row ``x``."""
    reached = {f"{what} [{refs}]" for what, holds in AT_VALUATION.items() if holds(x)}
    frame = range(x.t_entry(), x.proj_len())
    return reached | {what for what, holds in IN_FRAME.items()
                      if any(holds(x, t) for t in frame)}


def _settle(records, case, model, key):
    """Record what the rules and the core grid's reach need of a row, and release it.

    ``case`` is the row's (row_kind, S point, source_mth, set) and ``key`` its registry key
    in ``model``, the splice's SEC model.  A T2 or T3 case calls this once it has compared
    the row, whatever the comparison found, so the row is released either way.  The record
    is :func:`_rule_breaches`'s, with the row's :func:`_branches`, and a row that raises is
    recorded as raising, which the rules test reports.
    """
    try:
        proj = projection(model, key)
        record = _rule_breaches(proj)
        record["branches"] = _branches(proj, case[3])
        record["failed"] = None
    except Exception as err:                    # recorded, and reported by the rules test
        record = {"negative": [], "early": [], "ahead": [], "outside": [], "raised": [],
                  "branches": set(), "failed": _raised(err)}
    finally:
        _release(model, key)
    records[case] = record
    return record


def _record_of(spliced, records, case):
    """The record of ``case``, from the case that compared its row or, failing it, now."""
    if case not in records:
        sec = spliced[case[3]][1]
        _settle(records, case, sec, _row_key(sec, *case[:3]))
    return records[case]


# ---------------------------------------------------------------------------
# T2 -- the splice


@pytest.mark.parametrize(
    "kind, s_point, month, refs",
    [_case(case, CORE_SPLICES, _case_id(*case)) for case in SPLICES + IN_FORCE_TWINS])
def test_an_in_force_point_continues_its_s_projection(spliced, splice_records, kind,
                                                      s_point, month, refs):
    """Opened with S's state at month d, the point is S from d on, in every cell of S's.

    This is the test that says the opening state is complete: a state column the SEC row
    did not carry, or carried from the wrong instant, would make SEC part from S here, and
    nowhere else, because on a point issued at ``t = 0`` the two clocks coincide and the
    opening state is the issue value.  For the same reason it is the test that catches a
    policy month passed as ``t`` (R1a), as a declaration, a guarantee date or a single
    premium read on ``t`` would be.  The frame comparisons read SEC row ``t`` against S row
    ``t + d`` in every column of the three reports both hold, and fail frames that end
    apart.  The cell comparison then evaluates every cell of S's but :data:`SPLICE_EXEMPT`,
    at every argument S cached inside its own frame from month ``d`` on, moved onto SEC's
    clock: the count, the asset share at each step, the units, the price, the guarantee,
    the payout, the bonus rate, the cumulants and the claims of each kind among them.  Each
    compares to 1e-9 relative with no absolute floor, but the roll-forwards' residuals,
    which keep the floor of 1e-9 (:func:`_compare`).  An S cell this model lacked would fail
    it.

    The rows past a cap the cumulants carry are the ones that see a cumulant dropped: the
    -15% and +5% bonds issued at the valuation date, restated past their caps at 102 and
    443, charge on without their charges where S has stopped.  The twins of S's points in
    force are spliced at their own months, and the twins of the new business at 0, on each
    set.  The row is then recorded for the rules test and released (:func:`_settle`).
    """
    s, sec = spliced[refs]
    key = _row_key(sec, kind, s_point, month)
    s_proj, sec_proj = _point(s, s_point), projection(sec, key)
    try:
        assert _compare(s_proj, sec_proj, month, SPLICE_EXEMPT) == []
    finally:
        _settle(splice_records, (kind, s_point, month, refs), sec, key)


# ---------------------------------------------------------------------------
# T3 -- future new business


@pytest.mark.parametrize(
    "s_point, k, refs",
    [_case(case, CORE_FUTURES, _case_id("future", case[0], -case[1], case[2]))
     for case in FUTURES])
def test_future_new_business_is_the_s_projection_k_months_on(spliced, splice_records,
                                                             s_point, k, refs):
    """Issued k months after the valuation date, the point is S's projection k months on.

    SEC rows ``k ..`` are S rows ``0 ..``, ending together at the end of the frame, in the
    three reports, and every cell of S's but :data:`FUTURE_EXEMPT` agrees at every argument
    S cached inside its own frame, moved ``k`` later.  Each compares as the splice compares,
    with no absolute floor but on the residuals (:func:`_compare`).  Before issue every
    column of ``result_cf`` and ``result_pols`` is an exact zero, and the policies arrive in
    month ``k`` as new business, paying the single premium there and nowhere else.

    The last assertions are R1 and D4's base rule made testable.  After the reports, no read
    keyed by an attained age or a policy year, and no rate, has been evaluated at a month
    before issue (:data:`KEYED_READS`).  A chain based at ``t == 0`` rather than at
    ``t_entry()``, or a rate evaluated before the month is asked whether it is in cover,
    still gives the right numbers.  This is the only test that sees the first, and the guard
    test sees the second too.  The row is then recorded for the rules test and released
    (:func:`_settle`).
    """
    s, sec = spliced[refs]
    key = _row_key(sec, "future", s_point, -k)
    s_proj, sec_proj = _point(s, s_point), projection(sec, key)
    try:
        df, pols = sec_proj.result_cf(), sec_proj.result_pols()
        assert _compare(s_proj, sec_proj, -k, FUTURE_EXEMPT) == []
        for report, frame in (("result_cf", df), ("result_pols", pols)):
            assert list(frame.index[:k]) == list(range(k)), report
            assert (frame.loc[:k - 1] == 0.0).all().all(), report
        assert sec_proj.pols_new_biz(k) == sec_proj.policy_count() == 1.0
        assert [t for t in range(sec_proj.proj_len())
                if sec_proj.premium_pp(t) > sec_proj.premium_regular_pp() / 12.0] == (
            [k] if sec_proj.premium_single_pp() > 0.0 else [])
        early = {name: sorted(args[0] for args in _cached_args(sec_proj.cells[name])
                              if args[0] < k)
                 for name in KEYED_READS}
        assert not any(early.values()), f"read before issue: {early}"
    finally:
        _settle(splice_records, ("future", s_point, -k, refs), sec, key)


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
    and points issued later, on both sets, and on each the reports, the checks and the full
    sweep are run first (:func:`_rule_breaches`):

    * R1: no cell holds a negative argument.  modelx evaluates one without complaint, and
      a compiled cache raises ``IndexError`` below 0 (USLIB-SEC-PLAN.md F4).  A policy
      month turned into ``t`` by subtracting ``duration_mth_init()`` (R1a) goes negative
      on a point in force past it.
    * R1's look-back stops at ``t_entry()``: no cell evaluated at a month from
      ``t_entry()`` on read a month before it.  On a point issued later a chain based at
      ``t == 0`` reads the pre-issue zeros, so no number shows it and no argument goes
      negative.
    * R2's look-ahead: no cell evaluated at month ``t`` read a cell keyed by a month beyond
      ``t + 1``, as modelx's dependency graph records each cached call's precedents, but the
      bonus rate's read of its year's declaration (:data:`LOOK_AHEAD`), which reads no
      month past the frame from a month inside it.
    * And no call of the full sweep raised.

    Each row was scanned by the T2 or T3 case that compared it (:func:`_settle`), and a row
    no case has scanned is scanned here.  The core case covers the core's rows, the full
    case every other row of the full grid, with ``UKLIB_SEC_FULL=1``.  The closed-form
    clock and the recursion depth are asserted on the committed model, in the tests after
    this one, and the exhaustion search's reads by a test of its own.
    """
    cases = [case for case in GRID if (case in CORE_GRID) == (grid == "core")]
    negative, early, ahead, outside, raised, failed = [], [], [], [], [], []
    for case in cases:
        record, where = _record_of(spliced, splice_records, case), _case_id(*case)
        negative += [f"{where}: {call}" for call in record["negative"]]
        early += [f"{where}: {read}" for read in record["early"]]
        ahead += [f"{where}: {read}" for read in record["ahead"]]
        outside += [f"{where}: {read}" for read in record["outside"]]
        raised += [f"{where}: {call}" for call in record["raised"]]
        if record["failed"]:
            failed.append(f"{where}: {record['failed']}")
    assert cases, f"the {grid} grid has no rows"
    assert not failed, f"rows that raised: {failed[:10]}"
    assert not raised, f"calls the full sweep found raising: {raised[:10]}"
    assert not negative, f"called before the valuation date: {negative[:10]}"
    assert not early, f"read before issue from the books: {early[:10]}"
    assert not ahead, f"read beyond t + 1: {ahead[:10]}"
    assert not outside, f"the declaration's read past the frame: {outside[:10]}"


def test_the_exhaustion_search_reads_the_units_to_their_exhaustion_and_no_further(
        sec_model):
    """``fund_exhaust_mth()`` reads the units month by month, from ``t_entry()`` to the month
    they run out.

    The search is R2's far read, one loop in one cell, from the first month on the books,
    ascending.  On each committed bond whose units run out the cell reads ``units`` at every
    month from ``t_entry()`` to ``proj_len()``, the month the withdrawal takes the last of
    them, which is the first month the frame does not project, and at no month after it;
    on the bond issued 13 months on it reads none before its issue month, where a search
    from 0 would find a bond with no units and read it as exhausted.  It returns the policy
    month of that read, and the frame ends the month before.  On the bonds that take no
    withdrawal, and on the endowment, it reads no units at all, and returns a month past
    cover.  Its precedents are read off modelx's dependency graph.
    """
    table = sec_model.Data.model_point_table()
    exhausting = 0
    for key, label in zip(point_keys(sec_model), table.index):
        p = projection(sec_model, key)
        exhaust = p.fund_exhaust_mth()
        reads = sorted(node.args[0] for node in p.cells["fund_exhaust_mth"].preds()
                       if node.obj.name == "units")
        if not (p.is_unitised() and p.wd_rate() > 0.0):
            assert reads == [] and exhaust == p.cover_end_mth() + 1, label
            continue
        assert exhaust < p.cover_end_mth(), label
        assert reads == list(range(p.t_entry(), p.proj_len() + 1)), label
        assert exhaust == p.duration_mth(p.proj_len()), label
        assert p.units(p.proj_len()) <= 1e-9 < p.units(p.proj_len() - 1), label
        exhausting += 1
    assert exhausting >= 4


# The rows whose units run out at the end of cover, as {S variant: (the policy month they
# run out in, the frame from the S month 777 the row is restated at)}: in the last month of
# cover, 779, which the search reads last, and a month before it.
LAST_COVERED = {17: (779, 2), 18: (778, 1)}


def test_the_exhaustion_search_reads_the_last_month_of_cover(spliced, splice_records):
    """A bond whose units run out in the last month of its cover is encashed the month
    before, as ``WP_UK_S`` encashes it.

    The search runs over the months of cover, to policy month ``cover_end_mth() - 1``, its
    last read: a search a month short reads that month's run-out as "never", and projects
    the bond to the limiting age, its frame a month longer, its survivors paid the
    limiting age's benefit rather than encashed.  So on the main set of the splice, two
    variants of S's withdrawing bond, issued at 55 to 120, whose units run out in policy
    month 779, the last of cover, and in 778 (:data:`LAST_COVERED`), restated in force at
    777, each continue S's projection in every cell (T2, the splice test's core cases, and
    C4 on the splice grid), and each ends its frame the month before its units run out, a
    forced encashment: two months, and one.
    """
    sec = spliced["main"][1]
    for variant, (month, frame) in LAST_COVERED.items():
        p = _row(sec, "derived", variant, 777)
        assert p.cover_end_mth() == 780, variant
        assert p.fund_exhaust_mth() == month, variant
        assert p.proj_len() == frame and p.is_forced_encashment(), variant
        assert p.units(frame) <= 1e-9 < p.units(frame - 1), variant


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
      stays shallow.  A backward recursion over the frame, through ``t + 1``, keeps every
      step within the look-ahead but opens a chain as long as the frame, which a compiled
      model would run on the C stack (F7), and fails here.
    """
    record = sec_read[1]
    assert record["duration_mth(500)"] == 560
    assert record["keys"] == [500]
    assert not record["deep"], f"under a recursion limit of {CALL_DEPTH}: {record['deep']}"


# How deep a cold call may run beyond its chain (D5): the cells above the chain and those
# below it, the first month's rates and Data's first reads of its tables.  WP runs eight
# chains a month at a time: the count, the asset share, the smoothed payout and the
# endowment's guarantee, which M13 wrote one cell a month, and the units, the unit price
# and the two cumulants, which were already.  One cell a month, a cold net_cf at the
# longest cover, 1,236 months from issue at 18 to the largest limiting age, 121,
# needed 292 KiB of C stack compiled, past the 256 KiB the C step allows itself
# (UKLIB-SEC-PLAN.md §6.4, *Record -- M6*, *Carried into M8 and M14*), so each chain is
# blocked by policy year, its year's opening a cell that walks the year before (OPENINGS),
# and its chain is one cell a month within the year and two cells a year before it
# (_chain).  Measured at M14, on the blocked chains at that cover, issued at 18 now and 120
# months on, with the bonus rule and the estate's distribution on, each head cold in the
# last month on a read of its own: the chain is 215 cells on every shape, and each head
# runs beyond it, at most over the shapes, this many cells: the asset share 8, the payout
# and the asset share's residual 9, the cumulant of the charges and the smoothing account
# 12, the count 13 and its residual 16, the units 20, the guarantee and the unit price 22,
# the claims total 24 and net_cf 25, on the endowment, whose first month's declaration
# discounts its bonus cost at the foot of the chain.  So each head's bound is its own
# measured overhead, rather than Term's 16, which half the heads pass, or net_cf's 25 for
# every head, which a chain of two cells a month within its year, 11 cells more in the
# frame's last month, the year's twelfth, would meet on the shallower heads: any chain
# left one cell a month runs about a thousand beyond its bound, and a year's opening that
# walks from the year's second month a cell more a year.
CHAIN_OVERHEAD = {("net_cf", None): 25, ("pols_if_at", "BEF_NB"): 13, ("asset_share", None): 8,
                  ("smoothed_payout", None): 9, ("guar_benefit_pp", None): 22,
                  ("units", None): 20, ("unit_price", None): 22,
                  ("guar_charge_cum_pp", None): 12, ("smoothing_account", None): 12,
                  ("check_asset_share_roll_fwd_resid", None): 9,
                  ("check_pols_roll_fwd_resid", None): 16, ("claims", "ALL"): 24}

# The bonus rule's own chain, the rate declared each year from the year before's, runs one
# cell a policy year, its declaration's read of the asset share and the payout opening
# beneath its first: measured at M14, 20 cells beyond one a year at the longest cover, on
# each shape, where M13's chains, one cell a month, put 30 beneath it.
RULE_OVERHEAD = 20

# The longest cover proj_len() admits, 1,236 months, the compiled model's caches' bound:
# issued at issue_age_min, 18, to the largest limiting age the shipped mortality table
# admits, 121, its last age plus one, on the bond, and an endowment maturing there, 103
# years.  LONGEST_REFS sets omega_age there, beside the switches that ship off, for each
# test of the longest cover.  At the shipped limiting age, 120, the longest cover is
# LONGEST.
YOUNGEST = 18
LONGEST = 12 * (120 - YOUNGEST)
OMEGA_MAX = 121
LONGEST_MAX = 12 * (OMEGA_MAX - YOUNGEST)
LONGEST_REFS = {**SWITCHED_ON, "omega_age": OMEGA_MAX}

# The chains of the model and the cells that head them, called cold in the last month of
# the frame, each on a read of its own: (cell, the timing or kind it takes, or None).
CHAIN_HEADS = tuple(CHAIN_OVERHEAD)

# The shapes the chains run at their longest cover on: the anchor bond issued at 18, the
# endowment issued at 18 for 103 years, and the bond with a 1% withdrawal at 7%, whose
# units never run out, so that the exhaustion search runs over the whole cover.  Each is a
# committed twin made new business at 18: (the twin's S point, the columns changed).
SHAPES = {
    "bond": (1, {}),
    "endowment": (5, {"policy_term": OMEGA_MAX - YOUNGEST}),
    "withdrawing bond": (7, {"fund_return": 0.07, "wd_rate": 0.01}),
}


def _chain(p, t):
    """The cells a cold read of month ``t`` of ``p`` runs through, past the first: one a
    month back to its policy year's first month, or to ``t_entry()`` in the year that holds
    it, and two a policy year before that, back to ``t_entry()``'s year, where the eight
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


def _new_business(row):
    """``row``, a committed twin's, as new business: no opening state, the seed price."""
    return row.assign(duration_mth=0, units_init=0.0, unit_price_init=1.0,
                      attaching_bonus_init=0.0, asset_share_init=0.0,
                      smoothed_payout_init=0.0, guar_charge_cum_pp_init=0.0,
                      smoothing_account_init=0.0)


def _longest_cover(tmp_path, shapes):
    """A copy whose table holds each of ``shapes`` at the contract's longest cover, issued
    now and 120 months on, and each row's label, shape, frame and ``t_entry()``, under
    :data:`LONGEST_REFS`.

    Each shape's twin, issued at 18, 1,236 months from the largest limiting age the shipped
    table admits, 121, issued at the valuation date and 120 months after it, the shipped
    ``future_horizon_mth``: frames of 1,236 and 1,356 months, whose chains stop at
    ``t_entry()``.  The shipped tables serve every age from 18 to 120.
    """
    committed = _committed()
    rows, frames, label = [], [], committed.index.max()
    for shape in shapes:
        s_point, changes = SHAPES[shape]
        twin = _label(committed, "twin", s_point, 0 if s_point in (5, 7) else 60)
        row = _new_business(committed.loc[[twin]]).assign(age_at_entry=YOUNGEST, **changes)
        for issue in (0, 120):
            label += 1
            rows.append(row.assign(duration_mth=-issue).set_axis([label]))
            frames.append((label, shape, LONGEST_MAX + issue, issue))
    table = pd.concat(rows).rename_axis("point_id")
    return _sec_inputs(tmp_path, table), frames


# modelx warns as its stack trace starts and stops, which is all the test does with it.
@pytest.mark.filterwarnings("ignore:call stack trace:UserWarning")
@pytest.mark.parametrize("shape", [pytest.param(s, id=s.replace(" ", "_"))
                                   for s in SHAPES])
def test_every_chain_runs_one_cell_a_month_from_a_cold_start(tmp_path, shape):
    """Called cold, each chain runs one cell a month within its policy year, and two cells a
    year before it, back to ``t_entry()``, no more (D5, as blocked at M14).

    No number shows how deep a chain runs, and a compiled model runs it on the C stack, so a
    chain of several cells a month, which gives the same numbers, needs that many times the
    stack on every platform (F7).  ``WP_UK_S``'s asset share runs seven cells a month: a
    cold read of ``asset_share(779)`` on the worked example's bond runs 5,042 deep.  One
    cell a month, as M13 left them, this model's chains ran 1,236 cells at the longest
    cover, and compiled the count's needed 292 KiB of C stack, past what the C step allows
    (UKLIB-SEC-PLAN.md §6.5, *Record -- M14*).  So the eight chains are blocked by policy
    year, each year's opening a cell that walks the year before in ascending order
    (:data:`OPENINGS`).  On a model just read, nothing is cached, so modelx's stack trace
    counts how deep a call runs, against that chain (:func:`_chain`) and the head's own
    measured overhead more, :data:`CHAIN_OVERHEAD`: each head of :data:`CHAIN_HEADS` in the
    last month of the frame, each on a read of its own, with :data:`LONGEST_REFS` set, so
    that the bonus rule declares from the asset share, the estate distribution reads it and
    the limiting age is the largest the shipped table admits.  On each shape at the longest
    cover, 1,236 months from issue age 18, issued now and, with the full grid, 120 months on
    (:func:`_longest_cover`), each row's frame asserted on its own read first.  The bonus
    rule's own chain, one cell a year, is held to a year a cell and :data:`RULE_OVERHEAD`
    more.  Every shape runs by default, the withdrawing bond among them, whose exhaustion
    search runs the units' chain ascending first, so that a fault in its depth fails the
    default run; the rows issued 120 months on run with the full grid.  A chain left one
    cell a month runs about a thousand cells past its bound; one of two cells a month within
    its year 11 past it in the frame's last month, the year's twelfth; and a year's opening
    that walks from the year's second month a cell more a year.
    """
    folder, frames = _longest_cover(tmp_path, (shape,))
    frames = frames if SEC_FULL else frames[:1]
    framed = mx.read_model(folder, name=_name("framed"))
    try:
        for ref, value in LONGEST_REFS.items():
            setattr(framed.Projection, ref, value)
        for label, _, months, entry in frames:
            p = _point(framed, label)
            assert p.proj_len() == months and p.t_entry() == entry, label
    finally:
        framed.close()
    found = []
    for label, _, months, entry in frames:
        for cell, timing in (*CHAIN_HEADS, ("bonus_rate", None)):
            if cell == "units" and shape == "endowment":
                continue                    # no units on the endowment: no chain
            fresh = mx.read_model(folder, name=_name("cold"))
            try:
                for ref, value in LONGEST_REFS.items():
                    setattr(fresh.Projection, ref, value)
                p = _point(fresh, label)
                last = months - 1
                args = (last,) if timing is None else (last, _code(p, timing))
                depth = _cold_depth(p, cell, args)
                if cell == "bonus_rate":
                    chain, allowed = (last - entry) // 12 + 1, RULE_OVERHEAD
                else:
                    chain, allowed = _chain(p, last), CHAIN_OVERHEAD[cell, timing]
                if not chain <= depth <= chain + allowed:
                    found.append(f"{shape} {label}: {cell}{args} cold runs {depth} cells "
                                 f"deep, where its chain back to t_entry() {entry} is "
                                 f"{chain} and {allowed} more are allowed")
            finally:
                fresh.close()
    assert not found, found


def test_each_chain_written_inline_is_its_steps_bit_for_bit(sec_model):
    """The chains written inline are the cells that expose their steps, to the last bit.

    ``asset_share(t)`` writes the month's premium and withdrawal, return, charges,
    shareholder transfer, mortality charge and estate distribution inline, for its chain;
    ``asset_share_at(t, "AFT_MC")`` builds the same balance a step at a time, as
    ``WP_UK_S``'s does, each step a cell.  ``smoothed_payout(t)`` writes the cap and the
    corridor inline; ``smoothed_payout_capped(t)`` is the cap as a cell.  And the endowment's
    ``guar_benefit_pp(t)`` writes the declaration on the guarantee the month before, which
    ``guar_benefit_open(t)`` reads.  On every committed point and month the inline cell is
    the step-by-step one, floored or clamped as it floors or clamps, compared with ``==``,
    so a step reordered, a float rounded otherwise or a floor dropped fails.
    """
    for key, label in zip(point_keys(sec_model), sec_model.Data.model_point_table().index):
        p = projection(sec_model, key)
        for t in range(p.t_entry(), p.proj_len()):
            aft_mc, bef_prem = _code(p, "AFT_MC"), _code(p, "BEF_PREM")
            assert p.asset_share(t) == max(0.0, p.asset_share_at(t, aft_mc)), (label, t)
            capped, as_t = p.smoothed_payout_capped(t), p.asset_share(t)
            assert p.smoothed_payout(t) == max(p.corridor_lo * as_t,
                                               min(p.corridor_hi * as_t, capped)), (label, t)
            if not p.is_unitised():
                g = p.guar_benefit_open(t)
                want = g * (1.0 + p.bonus_rate(t)) if p.is_declaration_month(t) else g
                assert p.guar_benefit_pp(t) == want, (label, t)
            if t > p.t_entry():
                assert p.asset_share_at(t, bef_prem) == p.asset_share(t - 1)
                assert p.smoothed_payout_open(t) == p.smoothed_payout(t - 1)


def test_each_chain_opens_a_policy_year_with_the_year_before_s_close(sec_model):
    """Each blocked chain opens a policy year with the value the year before closes on, bit
    for bit, and reads it there alone (§6.5, *Record -- M14*).

    Each of the eight chains runs one cell a month within a policy year, the depth test
    above shows, and in a year's first month after ``t_entry()`` reads the year's opening
    (:data:`OPENINGS`), which walks the year before.  So the forms must give one number: on
    every committed point, in every such month in its frame, the count carried in is the
    month before's ``BEF_NB`` count plus its new business, less its deaths and surrenders,
    the product ``BEF_NB`` forms within a year; and the asset share, the payout, the
    guarantee, the units, the unit price and the two cumulants carried in are the month
    before's, each as the monthly cell computes it, bit for bit, whatever the opening's
    walk.  And as modelx's dependency graph records them, each chain's precedents in such a
    month are its opening and none of its own months, and in every other month after
    ``t_entry()`` the month before and no opening, the endowment's guarantee and the bond's
    units each on its own chassis alone.
    """
    table = sec_model.Data.model_point_table()
    openings, middles = 0, 0
    for key, point_id in zip(point_keys(sec_model), table.index):
        p = projection(sec_model, key)
        bef_nb = _code(p, "BEF_NB")
        chains = [("pols_if_at", "pols_if_py", True), ("asset_share", "asset_share_py", True),
                  ("smoothed_payout", "smoothed_payout_py", True),
                  ("guar_benefit_pp", "guar_benefit_pp_py", not p.is_unitised()),
                  ("units", "units_py", p.is_unitised()),
                  ("unit_price", "unit_price_py", True),
                  ("guar_charge_cum_pp", "guar_charge_cum_pp_py", True),
                  ("smoothing_account", "smoothing_account_py", True)]
        for t in range(p.t_entry() + 1, p.proj_len()):
            s = t - 1
            first = p.duration_mth(t) % 12 == 0
            if first:
                y, openings = p.policy_year(t), openings + 1
                closes = {
                    "pols_if_py": ((p.pols_if_at(s, bef_nb) + p.pols_new_biz(s))
                                   * (1.0 - p.mort_rate_mth(s)) * (1.0 - p.surr_rate_mth(s))),
                    "asset_share_py": p.asset_share(s),
                    "smoothed_payout_py": p.smoothed_payout(s),
                    "guar_benefit_pp_py": p.guar_benefit_pp(s),
                    "units_py": p.units(s),
                    "unit_price_py": p.unit_price(s),
                    "guar_charge_cum_pp_py": p.guar_charge_cum_pp(s),
                    "smoothing_account_py": p.smoothing_account(s)}
                for cell, opening, chained in chains:
                    if chained:
                        got, close = p.cells[opening](y), closes[opening]
                        assert got.hex() == close.hex(), (point_id, opening, y, got, close)
                assert p.pols_if_at(t, bef_nb) == closes["pols_if_py"], (point_id, t)
            else:
                middles += 1
            for cell, opening, chained in chains:
                if not chained:
                    continue
                args = (t, bef_nb) if cell == "pols_if_at" else (t,)
                p.cells[cell](*args)
                reads = {(n.obj.name, n.args) for n in p.cells[cell].preds(*args)}
                own = any(name == cell and n_args[0] < t for name, n_args in reads)
                opened = any(name == opening for name, _ in reads)
                if first:
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
# CHAIN_HEADS but the claims total, which holds claims itself twice, the total over its
# death kind, at the top of any path, whatever the cover: no chain recurses through it, and
# its refusal, of a total past the floats, names the kinds' values.  net_cf reads the total
# too, and on the endowment, whose count's chain reads no guarantee, its deepest path runs
# through the death claim's guarantee: so claims is held twice there as well, at the top of
# the path, which TOP_TWICE admits there alone.
TEXT_HEADS = tuple(head for head in CHAIN_HEADS if head != ("claims", "ALL"))
TOP_TWICE = frozenset({"claims"})


# modelx warns as its stack trace starts and stops, which is all the test does with it.
@pytest.mark.filterwarnings("ignore:call stack trace:UserWarning")
def test_no_cell_a_chain_recurses_through_formats_a_refusal(tmp_path):
    """No cell a cold call's deepest path holds more than once builds text (M10).

    A compiled cell's C frame holds the code that formats each of its messages, whether a
    run reaches it or not, and a chain holds a frame of each cell it recurses through at
    each level.  On CI's Ubuntu runner, a refusal formatted inside ``Term_UK_SEC``'s
    recursive waiver cell had its cold call at the longest cover need 512 KiB to 1 MiB, and
    256 to 384 once the cell held none (K12).  So every refusal of this model whose message
    is formatted sits in a cell no chain recurses through: the asset share, the unit price,
    the units, the guarantee, the cumulant of the charges and the smoothing account call
    ``asset_share_refusal``, ``unit_price_refusal``, ``units_refusal``,
    ``guar_benefit_refusal``, ``guar_charge_cum_refusal`` and ``smoothing_account_refusal``
    on their error paths alone, and the count and the payout refuse nothing a value makes.
    On a model just read, at the longest cover of each shape of :data:`SHAPES`, the
    withdrawing bond among them, whose exhaustion search runs the units' chain first, issued
    now, each head of :data:`TEXT_HEADS` is called cold in the last month, under modelx's
    stack trace, with :data:`LONGEST_REFS` set, and the cells on the stack at its deepest
    point are counted.  A cell held there twice or more is one the chain recurses through,
    at every month or every year.  None of them may build text anywhere in its formula, at a
    raise, in an error branch or into a local, nor raise other than one exception on one
    string constant (:func:`_text_faults`): the frame holds a message's code whether or not
    its branch runs.  A cell held once costs its frame once, as ``mort_rate``, whose refusal
    names an age outside the table, does at the chain's foot.  Each chain's monthly cell and
    its year's opening must be among the cells checked, every cell the eight blocked chains
    recurse through, or the test would check less than it says.
    """
    folder, frames = _longest_cover(tmp_path, tuple(SHAPES))
    found, checked = [], set()
    for label, shape, months, entry in frames:
        if entry != 0:
            continue
        for cell, code in TEXT_HEADS:
            if cell == "units" and shape == "endowment":
                continue
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
                for name in held & TOP_TWICE:
                    where = [i for i, n in enumerate(stack) if n == name]
                    assert len(where) == 2 and where[-1] < 4, (label, cell, name, where)
                held -= TOP_TWICE
                checked |= held
                for name in sorted(held):
                    faults = _text_faults(p.cells[name])
                    if faults:
                        found.append(f"{shape} {label}: {cell}{args}: {name}, held "
                                     f"{stack.count(name)} times on the deepest path, "
                                     f"builds text: {faults}")
            finally:
                fresh.close()
    chains = {"pols_if_at", "asset_share", "smoothed_payout", "guar_benefit_pp", "units",
              "unit_price", "guar_charge_cum_pp", "smoothing_account"}
    assert chains | set(OPENINGS) <= checked, sorted(checked)
    assert not found, found


# ---------------------------------------------------------------------------
# T4 -- the count algebra
#
# BEF_DECR == BEF_NB + pols_new_biz, at every t of every point, is a convention
# (test_new_business_joins_the_count_before_decrements), and is not repeated here.


def test_the_count_rolls_forward_and_result_pols_holds_it(sec_model, s_model):
    """The count leaves month t by its decrements, and ``result_pols`` sets it out (D5).

    On every committed point and at every ``t`` of its frame, to 1e-12: the count weighting
    month ``t``, ``pols_if_at(t, BEF_DECR)``, less the count it carries into ``t + 1``,
    ``pols_if_at(t + 1, BEF_NB)``, is its deaths, its surrenders and, in the frame's last
    month, the survivors paid or truncated there, ``pols_maturity``; the count before
    surrenders is the count less its deaths; and the notes' end-of-month count,
    ``pols_if_at(t, AFT_DECR)``, is exactly the count carried into the next month, 0 from
    the last.  The new business is ``policy_count()`` in the issue month alone.

    ``result_pols()`` sets the same movement out row by row, in :data:`RESULT_POLS`'s
    columns, indexed by ``t`` over the frame: ``pols_if`` at ``t + 1`` is ``pols_if`` less
    its decrements at ``t``, plus the new business of ``t + 1``, row 0 opening from
    ``pols_if_init()``.  ``WP_UK_S`` has no ``result_pols``, so on each twin the report is
    compared with S's own counts (:func:`_s_result_pols`), to 1e-9, frames ending together:
    the counts carry no inflation, so the shipped assumptions serve.
    """
    table = sec_model.Data.model_point_table()
    for key, point_id in zip(point_keys(sec_model), table.index):
        p = projection(sec_model, key)
        bef_nb, bef_decr, bef_surr, aft = (_code(p, c) for c in TIMINGS)
        last, issue = p.proj_len() - 1, -p.duration_mth_init()
        for t in range(p.proj_len()):
            carried = p.pols_if_at(t + 1, bef_nb)
            assert p.pols_if_at(t, aft) == carried, (point_id, t)
            out = p.pols_death(t) + p.pols_surr(t) + p.pols_maturity(t)
            assert p.pols_if_at(t, bef_decr) - carried == pytest.approx(out, abs=1e-12), (
                point_id, t)
            assert p.pols_if_at(t, bef_surr) == pytest.approx(
                p.pols_if(t) - p.pols_death(t), abs=1e-12), (point_id, t)
            assert p.pols_new_biz(t) == (p.policy_count() if t == issue else 0.0)
            assert (p.pols_maturity(t) == 0.0) == (t != last) or p.pols_if(t) == 0.0
        assert p.pols_if_at(last + 1, bef_nb) == 0.0, point_id
        pols = p.result_pols()
        assert list(pols.columns) == RESULT_POLS, point_id
        assert pols.index.name == "t" and list(pols.index) == list(range(p.proj_len()))
        moved = (pols["pols_if"] - pols[["pols_death", "pols_surr", "pols_maturity"]]
                 .sum(axis=1)).shift(1)
        expected = moved.fillna(p.pols_if_init()) + pols["pols_new_biz"]
        assert ((pols["pols_if"] - expected).abs() <= 1e-12).all(), point_id
        if table.at[point_id, "row_kind"] == "twin":
            s = _point(s_model, point_id)
            assert frame_mismatches(_s_result_pols(s), pols,
                                    t_offset=int(table.at[point_id, "source_mth"])) == []


# What T4 multiplies the counts by: not a whole number, because a count of policies need
# not be one, so that a flow which read the count as whole policies would not follow it.
COUNT_FACTOR = 2.5

# The per-policy columns of each report, which the count must not move: the rest are
# counts or flows, which it scales.
PER_POLICY = {"result_cf": ("asset_share",), "result_pols": (),
              "result_payout": tuple(c for c in (
                  "asset_share", "guar_benefit_pp", "smoothed_payout", "final_bonus_pp",
                  "mvr_pp", "mvr_applied_pp", "claim_death", "claim_surrender",
                  "claim_guarantee", "bonus_rate", "cost_of_bonus_pp",
                  "shareholder_transfer_pp", "mort_charge_pp"))}

# The counted cells no sweep evaluates: a refusal's cell, called on the error path alone.
NEVER_SWEPT = frozenset({"smoothing_account_refusal"})


@pytest.mark.parametrize("grid", GRIDS)
def test_scaling_the_counts_scales_every_flow_and_no_per_policy_value(tmp_path, grid):
    """The count is the weight: 2.5 times it, 2.5 times every flow, the same per policy.

    The committed table, and a copy with every ``policy_count`` multiplied by
    :data:`COUNT_FACTOR`, are each read with :data:`SWITCHED_ON` set before either computes
    anything: every switch that ships off, on, so that every flow is nonzero on some point,
    the bonus rule declares from the asset share and the estate distribution reads it.  On
    every point each report's counts and flows are 2.5 times the committed table's, element
    by element, to 1e-12 relative: a scaled count is a computed float, which may come back
    from the CSV within two ulps (``uk_sec_support``'s module docstring); and its per-policy
    columns (:data:`PER_POLICY`) are the committed table's exactly.  So is every other cell
    of :data:`COUNTED`, at every argument the sweep of the committed table's point cached:
    the counts at each timing and the claims of each kind, which no report shows, among
    them, and the roll-forward's residual, a rounding about 0, to its floor of 1e-9.  And
    every cell outside :data:`COUNTED` (the asset share, the units, the price, the
    guarantee, the payout, the rates, both clocks, the flags) agrees bit for bit at every
    argument that sweep cached.  So a flow that dropped the count, or read it as whole
    policies, which a table of counts of 1 hides from every comparison with S, fails
    (USLIB-SEC-PLAN.md §5.2, T4, precised at M11).  The smoothing account opens from its
    per-policy column times the count, and scales with it.  Each counted cell is nonzero on
    some point but the residual and :data:`NEVER_SWEPT`.

    The default run takes :data:`CORE_POINTS`, among which every counted cell is nonzero,
    and the full grid the other committed points.
    """
    table = _committed()
    base = mx.read_model(_sec_inputs(tmp_path / "base", table), name=_name("counted"))
    scaled = mx.read_model(_sec_inputs(tmp_path / "scaled", table.assign(
        policy_count=COUNT_FACTOR * table["policy_count"])), name=_name("scaled"))
    counted = sorted(COUNTED - set(PER_POLICY))
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
            for report, fixed in PER_POLICY.items():
                b, d = one.cells[report](), many.cells[report]()
                assert d.index.equals(b.index) and list(d.columns) == list(b.columns)
                flows = [c for c in b.columns if c not in fixed]
                want = COUNT_FACTOR * b[flows]
                bad = ((d[flows] - want).abs() > 1e-12 * want.abs()).any()
                assert not bad.any(), (label, report, list(bad[bad].index))
                assert d[list(fixed)].equals(b[list(fixed)]), (label, report)
            for name in counted:
                floor = FLOOR if name in RESIDUALS else 0.0
                for args in _cached_args(one.cells[name]):
                    want = COUNT_FACTOR * one.cells[name](*args)
                    got = many.cells[name](*args)
                    assert abs(got - want) <= floor + 1e-12 * abs(want), (
                        label, name, args, got, want)
                    if want != 0.0 and name not in RESIDUALS:
                        nonzero.add(name)
            assert twin_mismatches(one, many, exempt=TWIN_EXEMPT_DEFAULT | COUNTED
                                   | set(PER_POLICY), rtol=0.0, atol=0.0) == [], label
            _release(base, key)
            _release(scaled, scaled_key)
    finally:
        scaled.close()
        base.close()
    if grid == "core":
        want = set(counted) - RESIDUALS - NEVER_SWEPT
        assert want <= nonzero, f"0 on every core point: {sorted(want - nonzero)}"


def _month_on(p):
    """The columns that restate ``p``, a point in force, a month on: what this model
    carries into its month 1, at month 1's ``BEF_NB`` instant (D6)."""
    count = p.pols_if_at(1, _code(p, "BEF_NB"))
    return dict(
        duration_mth=p.duration_mth(1), policy_count=count,
        asset_share_init=p.asset_share(0), units_init=p.units(0),
        unit_price_init=p.unit_price(0),
        attaching_bonus_init=(0.0 if p.is_unitised()
                              else p.guar_benefit_pp(0) - p.sum_assured()),
        smoothed_payout_init=p.smoothed_payout(0),
        bonus_rate_init=p.bonus_rate(0) if p.is_declaration_month(0) else p.bonus_rate_init(),
        guar_charge_cum_pp_init=p.guar_charge_cum_pp(0),
        smoothing_account_init=p.smoothing_account(0) / count)


@pytest.mark.parametrize("grid", GRIDS)
def test_a_point_restated_a_month_on_continues_its_own_flows(tmp_path, grid):
    """The state a point carries into a month is the state its month opens with (T4, D6).

    Each point in force on the committed table, its frame longer than a month, is restated
    a month on, opened with what this model carries into its month 1 (:func:`_month_on`):
    its count, ``pols_if_at(1, "BEF_NB")``; its asset share, units, unit price, guarantee
    less the sum assured on the endowment, smoothed payout and two cumulants at the close
    of month 0, the smoothing account per policy in force at month 1; and the rate declared
    at the last declaration before month 1, month 0's own where month 0 declares, and the
    point's opening rate otherwise (D6).  The restatement must continue the point's own
    frames, its row ``t`` the point's row ``t + 1``, in ``result_cf``, ``result_payout``
    and ``result_pols``, every flow among them, to 1e-9 relative, floored at 1e-9 for what a
    state read back from the CSV an ulp off moves about 0.  Scaling every count alike
    cannot see a flow weighted by the count a point opened with rather than the one in force
    in its month, and the splice sees only S's states: this sees both, on this model's own.
    It runs with the bonus rule on, so that the rate of the year under way is a state, and
    the estate distribution on, so that every month reads the opening asset share, at an
    inflation rate of 0, set on each model as it is read (K7): the restatement moves the
    valuation date a month on, and expense inflation, on the valuation clock, would step a
    month apart by design (D7).  The rows of a declaration in month 0, at 71 and 11, carry
    the declaration in their state.

    The default run restates the points in force among :data:`CORE_POINTS` and the twins
    in force at 60, and the full grid the others.
    """
    table = _committed()
    refs = {**SWITCHED_ON, "inflation_rate": 0.0}
    model = mx.read_model(_sec_inputs(tmp_path / "base", table), name=_name("month_on"))
    rows, pairs, frames = [], [], {}
    try:
        for ref, value in refs.items():
            setattr(model.Projection, ref, value)
        top = table.index.max()
        for label in table.index[table["duration_mth"] > 0]:
            core = label in CORE_POINTS or table.at[label, "duration_mth"] == 60
            if core != (grid == "core"):
                continue
            p = _point(model, label)
            if p.proj_len() < 2:
                continue
            top += 1
            row = table.loc[[label]].assign(**_month_on(p))
            row.index = pd.Index([top], name="point_id")
            rows.append(row)
            pairs.append((label, top))
            frames[label] = {report: p.cells[report]() for report in REPORTS}
            _release(model, _key(model, label))
    finally:
        model.close()
    if grid == "core":
        assert {table.at[label, "duration_mth"] % 12 for label, _ in pairs} >= {0, 11}
    restated = mx.read_model(_sec_inputs(tmp_path / "on", pd.concat([table, *rows])),
                             name=_name("month_on"))
    found = []
    try:
        for ref, value in refs.items():
            setattr(restated.Projection, ref, value)
        for label, moved in pairs:
            p = _point(restated, moved)
            for report, frame in frames[label].items():
                found += [f"point {label} restated as {moved}, {report}: {line}"
                          for line in frame_mismatches(frame, p.cells[report](),
                                                       t_offset=1)]
            _release(restated, _key(restated, moved))
    finally:
        restated.close()
    assert not found, found[:20]


@pytest.mark.parametrize("grid", GRIDS)
def test_the_roll_forward_closes_on_ten_million_policies(tmp_path, grid):
    """``check_pols_roll_fwd`` scales its tolerance with the policies, and closes at 1e7.

    A residual is rounding on that many policies, so the check holds it to 1e-10 times
    ``max(policy_count(), 1)``, where ``WP_UK_S``'s holds it to 1e-10 unscaled: at the
    counts the other tests use, one policy or less, the two are one.  ``WP_UK_S`` cannot
    scale by ``pols_if_init()``, which here is 0 on a point issued at or after the valuation
    date, its count entering as new business.  So every committed point is projected from a
    copy where each counts ten million policies: the check closes on each, and the largest
    residual over the points exceeds the unscaled 1e-10, so the scaling is what closes it
    (USLIB-SEC-PLAN.md §5.2, T4, precised at M10).

    The default run takes :data:`CORE_POINTS`, and the full grid the other points.
    """
    table = _committed()
    model = mx.read_model(_sec_inputs(tmp_path, table.assign(policy_count=1e7)),
                          name=_name("ten_million"))
    largest = 0.0
    try:
        for key, point_id in zip(point_keys(model), table.index):
            if not _on_grid(grid, point_id):
                continue
            p = projection(model, key)
            assert p.check_pols_roll_fwd() is True, point_id
            resid = max(abs(p.check_pols_roll_fwd_resid(t)) for t in range(p.proj_len()))
            assert resid <= 1e-10 * 1e7, point_id
            largest = max(largest, resid)
            _release(model, key)
    finally:
        model.close()
    assert largest > 1e-10, largest


# ---------------------------------------------------------------------------
# T5 -- validation
#
# Each malformed table is the committed one with one fault.  The checks run over the whole
# table as it is read, in Data, and the message names the file it read and the column or
# every point at fault.  A blank cell reads as NaN, and so does a text cell once the checks
# coerce the column to numbers, so each is refused as a count, a duration or a state that
# is not a number.  The repeated point_id holds another policy under the same label, as a
# bad extract would, so that the check must look at the labels and not at whole rows.  The
# point_ids are the committed table's: 1 to 7 the twins of S's points, 1 to 4 bonds in
# force at 60, 5 the endowment issued at the valuation date, 6 the endowment in force at
# 240 and 7 the bond variant issued at it; then S point 1 at 71 (8), point 2 at 68, 92, 119
# and 242 (9 to 12), point 3 at 487 (13), point 4 at 402 (14), the endowment at 11 and 299
# (15, 16), point 1 at 779 (17), the bond variant at 100 (18), its future row 13 months on
# (19), and the rows under References of their own, the bond variant at 60 (20), point 3
# at 300 (21), point 1 at 150 (22), the endowment at 150 (23) and point 1 at 156 (24).  A
# {file} in a message is the table's filename: every case is read by one model, from a
# file of its own (the malformed fixture).


def _drop(column):
    return lambda table: table.drop(columns=column)


_COUNT = "{file}: policy_count must be a number, zero or more; it is not at point_id "
_WHOLE_MONTHS = "{file}: duration_mth must be a whole number of months; it is not at point_id "
_BELOW_2_53 = "{file}: duration_mth must be below 2**53 months; it is not at point_id "
_WHOLE = "must be a whole number, 0 or more, below 2**53; it is not at point_id "
_AMOUNT = "must be a number, zero or more; it is not at point_id "
_DATES = ("{file}: guarantee_dates must be blank or policy anniversaries separated by ';', "
          "each a whole number of years, 1 or more, below 2**53; they are not at point_id ")
_NOT_YET = "must be 0 on a policy not yet in force, duration_mth 0 or less; it is not at point_id "
_PRICE = "{file}: unit_price_init must be a finite number above 0, a price; it is not at point_id "
_RATE = ("{file}: bonus_rate_init must be a finite number, zero or more, a declared bonus being "
         "floored at 0; it is not at point_id ")
_ACCOUNT = "{file}: smoothing_account_init must be a finite number; it is not at point_id "

MALFORMED = [
    ("a negative count", _set("policy_count", [8], -0.1), _COUNT + "[8]"),
    ("a blank count", _set("policy_count", [9], float("nan")), _COUNT + "[9]"),
    ("two bad counts", _set("policy_count", [8, 10], -1.0), _COUNT + "[8, 10]"),
    ("a text count", _set("policy_count", [11], "abc"), _COUNT + "[11]"),
    ("an infinite count", _set("policy_count", [11], float("inf")), _COUNT + "[11]"),
    ("a fractional duration", _set("duration_mth", [9], 68.5), _WHOLE_MONTHS + "[9]"),
    ("a blank duration", _set("duration_mth", [19], float("nan")), _WHOLE_MONTHS + "[19]"),
    ("a text duration", _set("duration_mth", [11], "x4"), _WHOLE_MONTHS + "[11]"),
    # numpy casts a float past int64 to the least int64, a policy issued 2**63 months on,
    # without a word: the table refuses it first.
    ("a duration past int64", _set("duration_mth", [8], 1e19), _BELOW_2_53 + "[8]"),
    ("durations of 2**53 months at two points", _set("duration_mth", [8, 10], 2.0 ** 53),
     _BELOW_2_53 + "[8, 10]"),
    ("issued beyond the horizon", _set("duration_mth", [19], -121),
     "{file}: duration_mth must be -120 or more, a policy issued at most 120 months after "
     "the valuation date; it is not at point_id [19]"),
    *[(f"no {column} column", _drop(column), f"{{file}} has no {column} column")
      for column in ("policy_count", "duration_mth", *STATE)],
    ("a point_id twice", lambda table: table.rename(index={9: 8}),
     "{file}: point_id [8] appears more than once"),
    ("an unknown chassis", _set("chassis", [8], "UWP_fund"),
     "{file}: chassis must be UWP_bond or CWP_endowment; it is not at point_id [8]"),
    ("an unknown sex", _set("sex", [9], "X"),
     "{file}: sex must be M or F; it is not at point_id [9]"),
    ("an unknown tax basis", _set("tax_basis", [10], "pension_net"),
     "{file}: tax_basis must be life_net or pension_gross; it is not at point_id [10]"),
    ("a fractional issue age", _set("age_at_entry", [8], 55.5),
     "{file}: age_at_entry " + _WHOLE + "[8]"),
    ("a negative issue age", _set("age_at_entry", [9], -1),
     "{file}: age_at_entry " + _WHOLE + "[9]"),
    ("an issue age of 2**53", _set("age_at_entry", [9], 2.0 ** 53),
     "{file}: age_at_entry " + _WHOLE + "[9]"),
    ("a fractional term", _set("policy_term", [6], 25.5),
     "{file}: policy_term " + _WHOLE + "[6]"),
    ("a negative single premium", _set("premium_single", [1], -1.0),
     "{file}: premium_single " + _AMOUNT + "[1]"),
    ("a blank regular premium", _set("premium_regular", [6], float("nan")),
     "{file}: premium_regular " + _AMOUNT + "[6]"),
    ("an infinite sum assured", _set("sum_assured", [6], float("inf")),
     "{file}: sum_assured " + _AMOUNT + "[6]"),
    ("a withdrawal past 1", _set("wd_rate", [4], ABOVE_1),
     "{file}: wd_rate must be a number from 0 to 1; it is not at point_id [4]"),
    ("a negative withdrawal", _set("wd_rate", [14], -0.01),
     "{file}: wd_rate must be a number from 0 to 1; it is not at point_id [14]"),
    ("a return of -1", _set("fund_return", [2], -1.0),
     "{file}: fund_return must be a finite number above -1; it is not at point_id [2]"),
    ("an infinite return", _set("fund_return", [3], float("inf")),
     "{file}: fund_return must be a finite number above -1; it is not at point_id [3]"),
    ("a guarantee date of 0", _set("guarantee_dates", [1], "0"), _DATES + "[1]"),
    ("a guarantee date not whole", _set("guarantee_dates", [2], "10;12.5"), _DATES + "[2]"),
    ("a guarantee date in text", _set("guarantee_dates", [3], "10;x"), _DATES + "[3]"),
    ("guarantee dates on an endowment", _set("guarantee_dates", [6], "10"),
     "{file}: guarantee_dates must be blank on a conventional endowment, which has no "
     "guarantee dates; it is not at point_id [6]"),
    ("an endowment with no term", _set("policy_term", [6], 0),
     "{file}: policy_term must be 1 or more on a conventional endowment, the years to its "
     "maturity; it is not at point_id [6]"),
    ("a bond with a term", _set("policy_term", [8], 10),
     "{file}: policy_term must be 0 on a bond, which is whole of life and has no term; it "
     "is not at point_id [8]"),
    ("a negative asset share", _set("asset_share_init", [8], -0.01),
     "{file}: asset_share_init " + _AMOUNT + "[8]"),
    ("blank units", _set("units_init", [9], float("nan")),
     "{file}: units_init " + _AMOUNT + "[9]"),
    ("a negative attaching bonus", _set("attaching_bonus_init", [16], -1.0),
     "{file}: attaching_bonus_init " + _AMOUNT + "[16]"),
    ("an infinite payout", _set("smoothed_payout_init", [10], float("inf")),
     "{file}: smoothed_payout_init " + _AMOUNT + "[10]"),
    ("negative charges taken", _set("guar_charge_cum_pp_init", [11], -0.01),
     "{file}: guar_charge_cum_pp_init " + _AMOUNT + "[11]"),
    ("a unit price of 0", _set("unit_price_init", [12], 0.0), _PRICE + "[12]"),
    ("an infinite unit price", _set("unit_price_init", [13], float("inf")), _PRICE + "[13]"),
    ("a text unit price", _set("unit_price_init", [7], "par"), _PRICE + "[7]"),
    ("a negative bonus rate", _set("bonus_rate_init", [14], -0.01), _RATE + "[14]"),
    ("a blank bonus rate", _set("bonus_rate_init", [19], float("nan")), _RATE + "[19]"),
    ("an infinite smoothing account", _set("smoothing_account_init", [17], float("inf")),
     _ACCOUNT + "[17]"),
    ("a smoothing account of -inf", _set("smoothing_account_init", [24], -math.inf),
     _ACCOUNT + "[24]"),
    ("a text smoothing account", _set("smoothing_account_init", [18], "x"),
     _ACCOUNT + "[18]"),
    ("units on an endowment", _set("units_init", [16], 1.0),
     "{file}: units_init must be 0 on a conventional endowment, which holds no units; it is "
     "not at point_id [16]"),
    ("an attaching bonus on a bond", _set("attaching_bonus_init", [8], 1.0),
     "{file}: attaching_bonus_init must be 0 on a bond, whose bonus is in its unit price; it "
     "is not at point_id [8]"),
    ("an asset share before issue", _set("asset_share_init", [19], 1.0),
     "{file}: asset_share_init " + _NOT_YET + "[19]"),
    ("units before issue", _set("units_init", [19], 1.0),
     "{file}: units_init " + _NOT_YET + "[19]"),
    ("an attaching bonus at issue", _set("attaching_bonus_init", [5], 1.0),
     "{file}: attaching_bonus_init " + _NOT_YET + "[5]"),
    ("a payout at issue", _set("smoothed_payout_init", [7], 1.0),
     "{file}: smoothed_payout_init " + _NOT_YET + "[7]"),
    ("charges taken before issue", _set("guar_charge_cum_pp_init", [19], 1.0),
     "{file}: guar_charge_cum_pp_init " + _NOT_YET + "[19]"),
    ("a smoothing account at issue", _set("smoothing_account_init", [5], -1.0),
     "{file}: smoothing_account_init " + _NOT_YET + "[5]"),
    # Rule 13 refuses a payout of 0 beside an asset share above a cent: a cent outside is
    # refused, and a cent and half a cent are read (the edges test).
    ("a payout of 0 beside an asset share", _set("smoothed_payout_init", [8], 0.0),
     "{file}: smoothed_payout_init must be above 0 on a policy in force with an asset share "
     "above a cent, which holds the payout above 0; it is not at point_id [8]"),
    ("a payout of 0 beside two cents", _set("asset_share_init", [12], 0.02),
     "{file}: smoothed_payout_init must be above 0 on a policy in force with an asset share "
     "above a cent, which holds the payout above 0; it is not at point_id [12]"),
    ("a bond in force without units", _set("units_init", [14], 0.0),
     "{file}: units_init must be above 0 on a bond in force, whose units are spent only "
     "when it is encashed; it is not at point_id [14]"),
    # Rule 14 holds the endowment's attaching bonus to 0, to the cent, before its first
    # declaration: a cent past 0 is refused, and half a cent read (the edges test).
    ("an attaching bonus a cent past 0 at 11", _set("attaching_bonus_init", [15], 0.01),
     "{file}: attaching_bonus_init must be 0, to the cent, on a conventional endowment in "
     "force 11 months or fewer, before its first declaration at the end of policy month "
     "11; it is not at point_id [15]"),
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


# An extract's labels: none is its position plus one, as every committed label is.
EXTRACT_LABELS = tuple(range(100 + len(_committed()), 100, -1))


def _relabelled(message, relabel):
    """``message`` with every ``point_id [...]`` list it holds relabelled by ``relabel``."""
    def labels(match):
        return "point_id [" + ", ".join(str(relabel[int(p)]) for p in
                                        match.group(1).split(", ")) + "]"
    return re.sub(r"point_id \[(\d+(?:, \d+)*)\]", labels, message)


def _by_label(message, relabel):
    """``message``, which names its point first, ``point_id N: ...``, naming it by
    ``relabel[N]`` instead."""
    match = re.match(r"point_id (\d+): ", message)
    assert match, message
    return f"point_id {relabel[int(match.group(1))]}: " + message[match.end():]


def _extract_of(edit=None):
    """The committed table, edited by ``edit`` by its own labels, then relabelled
    :data:`EXTRACT_LABELS`, so that no label is its position plus one; and the relabelling,
    ``{committed label: extract label}``.

    Every label is asserted to be neither its row's position nor that plus one, so that an
    extract that came to relabel nothing fails each test that reads it, rather than let a
    refusal naming its point by ``idx`` or ``idx + 1`` pass as the extract's label.
    """
    committed = _committed()
    relabel = dict(zip(committed.index, EXTRACT_LABELS))
    table = edit(committed) if edit is not None else committed
    extract = table.rename(index=relabel)
    clashes = [(position, label) for position, label in enumerate(extract.index)
               if label in (position, position + 1)]
    assert not clashes, f"the extract labels rows by their positions: {clashes}"
    return extract, relabel


def _refused_naming(call, message):
    """``call()`` raises ``ValueError`` whose message starts with ``message``, which names
    the point first: a refusal naming another point, its position plus one, fails here
    even where the rest of its words are right."""
    with pytest.raises(Exception) as excinfo:
        call()
    line = _raised(excinfo.value)
    assert line.startswith(f"ValueError: {message}"), (line, message)


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

    The committed table's one future point is the bond variant issued 13 months on.  It
    reads at the shipped 120 months and at 13, the shortest horizon that admits it, and is
    refused at 12, by name.  At 0 the model takes no future new business, D4's fallback for
    a product that cannot support it, and the message says so.  A horizon that is not a
    whole number of months, 0 or more, below ``2**53``, is itself refused, printed as a
    float, as the compiled model prints the ``long long`` it holds: a NaN and an infinity
    among them, either of which would admit every policy, and ``2**53`` and ``-1``, as ints
    and as floats.  A longer horizon than 120 reads, as at the in-force step, ``121``,
    ``121.0`` and ``2**53 - 1`` among them: the compiled model's caches, sized from 120,
    hold frames to 1,356 months, and ``proj_len()`` refuses a longer one by point (the
    caches' bounds test), so no value of the Reference refuses a table.  A whole number
    written as a float, ``13.0``, reads as 13 does.  Setting the Reference clears the
    table, so each value is read afresh.
    """
    future = _label(_committed(), "future", 7, -13)
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
                                 *((h, off.format(float(h))) for h in (
                                     -1, -1.0, 12.5, math.nan, math.inf, -math.inf,
                                     2 ** 53, WHOLE)),
                                 (121, None), (121.0, None), (WHOLE - 1, None),
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
                          timeout=600)
    if not check:
        return done
    assert done.returncode == 0, done.stderr.decode(errors="replace")
    assert done.stdout.isascii(), "run_sec.py printed a non-ASCII character"
    # Windows ends each printed line with "\r\n"; read them as "\n", as a frame's
    # to_string() writes them.
    return done.stdout.decode("ascii").replace("\r\n", "\n")


# A point at the end of its cover, as (case, the S point and month of the committed row,
# the policy month it is moved to, the end of cover): the worked example's bond at the
# limiting age, 780 months from issue at 55, and the endowment at its maturity, 300 months.
PAST_COVER = [("the bond at the limiting age", (1, 779), 780),
              ("the endowment at maturity", (5, 299), 300)]


@pytest.mark.parametrize("case, row, end", PAST_COVER, ids=[c[0] for c in PAST_COVER])
def test_a_point_past_its_cover_is_refused_by_proj_len(tmp_path, case, row, end):
    """A point at or past the end of its cover has no frame, and ``proj_len()`` refuses it.

    The committed row in the last month of its cover is moved on a month, to the policy
    month cover ends, the bond's limiting age, ``omega_age``, 120, from issue at 55, or the
    endowment's maturity, on the policy clock.  That is a rule of the product, not of the
    table: it needs the limiting age, a Reference, or the term, and the entry age the
    point's own columns give, read where the frame is defined, so the table reads, and the
    point is refused on its first projection, rather than projecting nothing.  A loop over
    the block would meet the point only when it reached it, after projecting the points
    before it, so ``run_sec.py --block``, run beside the table, asks every point for its
    frame first: it fails naming the point, and prints nothing before.  The month before,
    the committed row, projects one month.  The table is an extract labelled otherwise
    than by position, and the refusal names the extract's label.
    """
    moved = _label(_committed(), "derived", *row)
    table, relabel = _extract_of(_set("duration_mth", [moved], end))
    model = mx.read_model(_sec_inputs(tmp_path, table), name=_name("past_cover"))
    message = (f"point_id {relabel[moved]}: duration_mth {end} is at or past the end of "
               f"cover, policy month {end}")
    try:
        assert len(model.Data.model_point_table()) == len(_committed())
        _refused_naming(_point(model, relabel[moved]).result_cf, message)
    finally:
        model.close()
    shipped = mx.read_model(model_path(SEC), name=_name("last"))
    try:
        assert len(_point(shipped, moved).result_cf()) == 1
    finally:
        shipped.close()
    runner = tmp_path / "run_sec.py"
    shutil.copy(model_path(SEC).parent / "run_sec.py", runner)
    done = _run_sec(runner, "--block", check=False)
    assert done.returncode != 0 and done.stdout == b""
    assert message in done.stderr.decode(errors="replace")


# What the contract does not issue, refused by proj_len() as a point past cover is, as
# (case, the table's edit, the References set, the point, the message, and the frame the
# point projects at the shipped References, or None).  Data reads an issue age as WP_UK_S
# does, so each reads.  The product issues from 18, the mortality table's first age, and
# cover runs to omega_age, 120, on the bond, and to an endowment's maturity at most then;
# the compiled caches will be sized from both.  Each bound is refused just inside it here,
# and accepted at it in the edges test.  And each bound, moved past a committed twin,
# refuses it, which at the shipped bound projects its frame: the Reference is what refuses
# it.  Point 1 is the worked example's bond, issued at 55; point 5 the endowment, issued at
# 35 for 25 years.
NOT_ISSUED = [
    ("an issue age of 17", _set("age_at_entry", [5], 17), {}, 5,
     "point_id 5: the issue age, 17, is below issue_age_min, 18", None),
    ("an issue age below a bound raised to 36", None, {"issue_age_min": 36}, 5,
     "point_id 5: the issue age, 35, is below issue_age_min, 36", 300),
    ("a bond issued at 120", _set("age_at_entry", [7], 120), {}, 7,
     "point_id 7: the issue age, 120, is at or past omega_age, 120: the bond has no cover",
     None),
    ("a bond issued at a limiting age lowered to 55", None, {"omega_age": 55}, 7,
     "point_id 7: the issue age, 55, is at or past omega_age, 55: the bond has no cover",
     267),
    ("an endowment maturing at 121", _set("age_at_entry", [5], 96), {}, 5,
     "point_id 5: the endowment matures at age 121, past omega_age, 120, whose attained "
     "ages mort_table.csv may not rate", None),
    ("an endowment maturing past a limiting age lowered to 59", None, {"omega_age": 59}, 5,
     "point_id 5: the endowment matures at age 60, past omega_age, 59, whose attained ages "
     "mort_table.csv may not rate", 300),
]


@pytest.mark.parametrize("case, edit, refs, point, message, frame", NOT_ISSUED,
                         ids=[c[0] for c in NOT_ISSUED])
def test_a_point_the_contract_does_not_issue_is_refused_by_proj_len(tmp_path, case, edit,
                                                                    refs, point, message,
                                                                    frame):
    """``proj_len()`` refuses a point outside the contract's bounds, naming it (§6.5).

    ``WP_UK_S`` projects any issue age its tables reach, and an endowment maturing past the
    limiting age at the limiting age's rate, and so would modelx here, but the contract
    does not write either, and the compiled model's caches will be sized from the contract:
    a frame of at most 102 years and the horizon, attained ages from 18 to 119.  So the frame
    refuses such a point, naming it, as it refuses a point past its cover, and every report
    with it (:data:`NOT_ISSUED`): each bound just inside it, and each bound moved past a
    committed twin, which projects at the shipped bound, on a model read afresh.  A bound
    off by one, or a refusal lost, lets a point through.  The table reads either way, an
    extract labelled otherwise than by position, and each refusal names the extract's
    label.  Every Reference is set on a model just read, before its projection computes
    anything (K7).
    """
    table, relabel = _extract_of(edit)
    model = mx.read_model(_sec_inputs(tmp_path, table), name=_name("not_issued"))
    try:
        for ref, value in refs.items():
            setattr(model.Projection, ref, value)
        assert len(model.Data.model_point_table()) == len(_committed())
        _refused_naming(_point(model, relabel[point]).result_cf,
                        _by_label(message, relabel))
    finally:
        model.close()
    if frame is not None:
        shipped = mx.read_model(model_path(SEC), name=_name("bound"))
        try:
            assert len(_point(shipped, point).result_cf()) == frame
        finally:
            shipped.close()


# A bond whose units run out in its first month on the books, as (case, the table's edit,
# the point, the policy month): the withdrawing bond in its last month, 402, opened with a
# unit, which month 0's withdrawal, capped at the unit fund, takes; and the bond variant
# issued 13 months on and the one issued at the valuation date, each with no premium, so
# that its withdrawal election finds no units in its issue month.  WP_UK_S's search returns
# 0 there, its "never", and projects the bond to the limiting age.
SPENT = [
    ("a bond in force spent in month 0", _set("units_init", [14], 1.0), 14, 402),
    ("a bond issued later with no premium", _set("premium_single", [19], 0.0), 19, 0),
    ("a bond issued now with no premium", _set("premium_single", [7], 0.0), 7, 0),
]


@pytest.mark.parametrize("case, edit, point, month", SPENT, ids=[c[0] for c in SPENT])
def test_a_bond_spent_in_its_first_month_is_refused_by_proj_len(tmp_path, case, edit, point,
                                                                month):
    """A bond whose units run out in its first month on the books has no frame (§6.5).

    The frame ends the month before the units run out, so a bond spent in its first month,
    month 0 in force or its issue month, would end before it began: ``proj_len()`` refuses
    it, naming the point and the policy month, and every report with it.  On new business
    the withdrawal is capped at the unit fund the month opens with, 0, so a bond with a
    premium is never spent in its issue month; with none it is, and ``WP_UK_S``'s search,
    whose "never" is that month, would project it to the limiting age.
    """
    table, relabel = _extract_of(edit)
    model = mx.read_model(_sec_inputs(tmp_path, table), name=_name("spent"))
    try:
        p = _point(model, relabel[point])
        assert p.fund_exhaust_mth() == month
        _refused_naming(p.result_cf, f"point_id {relabel[point]}: the bond's units run out "
                                     f"in its first month on the books, policy month "
                                     f"{month}, so its frame would end before it began")
    finally:
        model.close()


# The two bounds the compiled model's caches are sized for (spec_sec.py), which proj_len()
# refuses a point past, by point and in both engines, each Reference keeping its in-force
# domain, so that a table the in-force step projected is refused only at a point whose own
# cover or frame is longer than the caches are sized for (UKLIB-SEC-PLAN.md §6.5, *Record
# -- M14*): a cover of 1,236 months, from issue at 18 to 121, the shipped table's last age
# plus one, whose policy years the y cache holds, and a frame of 1,356 months, that cover
# issued 120 months after the valuation date, whose months the t cache holds to the count
# carried into the month after the month after it.  As (case, the committed twin it is
# made from, its columns, its frame or the refusal after its label), each read under
# CACHE_REFS, a limiting age of 121, an issue_age_min of 17 and a horizon of 200 months,
# each in its domain, the twin made new business unless the case puts it in force: the
# bond issued at 18, 120 months on, the longest frame, and a month later; a bond and an
# endowment issued at 17, a cover a year longer, covers being whole years; a bond issued
# 200 months on withdrawing at +7%, whose units run out in month 1,356, ending the longest
# frame, or in month 1,357, or never, the last two refused alike, since the exhaustion
# search reads no month past 1,356; and the worked example's bond issued at 17 and in force
# at 24, withdrawing 3% at +5%, whose cover is a year longer though its units run out at
# policy month 798, a frame of 774 months the caches hold.  The in-force step projects
# that bond, and this one refuses it: the cover's bound is read before the exhaustion
# search, whose months it bounds, so it is conservative where a bond's units would run out
# within the caches (model-sec.md, *The bounds the caches hold*).  Each withdrawal rate of
# the bond issued 200 months on is the middle of the window of rates whose units run out
# in that month, measured at M14 by bisection.
CACHE_REFS = {"omega_age": OMEGA_MAX, "issue_age_min": YOUNGEST - 1,
              "Data.future_horizon_mth": 200}
_LATER = {"age_at_entry": YOUNGEST, "fund_return": 0.07, "duration_mth": -200}
_PAST_FRAME = ("the frame is longer than 1356 months, the longest the compiled model's "
               "caches hold: cover ends {} months after the valuation date")
_PAST_COVER = ("the cover, 1248 months from issue, is longer than 1236 months, issue at 18 "
               "to 121, the longest the compiled model's caches hold")
CACHE_EDGES = [
    ("the longest frame", 7,
     {"age_at_entry": YOUNGEST, "wd_rate": 0.0, "duration_mth": -120}, 1356),
    ("a frame a month longer", 7,
     {"age_at_entry": YOUNGEST, "wd_rate": 0.0, "duration_mth": -121},
     _PAST_FRAME.format(1357)),
    ("a bond's cover a year longer", 7, {"age_at_entry": YOUNGEST - 1, "wd_rate": 0.0},
     _PAST_COVER),
    ("an endowment's cover a year longer", 5,
     {"age_at_entry": YOUNGEST - 1, "policy_term": OMEGA_MAX - YOUNGEST + 1}, _PAST_COVER),
    ("the longest frame a run-out ends", 7, {**_LATER, "wd_rate": 0.0160762}, 1356),
    ("a run-out a month later", 7, {**_LATER, "wd_rate": 0.0160679},
     _PAST_FRAME.format(1436)),
    ("units that never run out", 7, {**_LATER, "wd_rate": 0.01}, _PAST_FRAME.format(1436)),
    ("a cover a year longer, its units running out within the caches", 1,
     {"age_at_entry": YOUNGEST - 1, "duration_mth": 24, "wd_rate": 0.03,
      "fund_return": 0.05}, _PAST_COVER),
]

# The row of CACHE_EDGES the cover's bound refuses conservatively, and the policy month its
# units run out in, within the caches.
CONSERVATIVE, CONSERVATIVE_RUN_OUT = len(CACHE_EDGES) - 1, 798


def _cache_edges():
    """:data:`CACHE_EDGES`' rows, each its committed twin with its columns, as new business
    unless the case puts it in force, when it keeps the twin's opening state, under labels
    301 on, none its position plus one."""
    committed = _committed()
    rows = []
    for n, (_, twin, changes, _) in enumerate(CACHE_EDGES):
        row = committed.loc[[twin]]
        if changes.get("duration_mth", 0) <= 0:
            row = _new_business(row)
        rows.append(row.assign(**changes).set_axis([301 + n]))
    return pd.concat(rows).rename_axis("point_id")


def test_a_cover_or_a_frame_past_the_caches_is_refused_by_point(tmp_path):
    """``proj_len()`` refuses a point whose cover or frame is longer than the compiled
    caches are sized for, naming it, and projects every other, whatever the References
    (§6.5).

    The caches are sized from the shipped References and table (``spec_sec.py``), and the
    in-force step projected any table its References admit: an ``issue_age_min`` below 18,
    a longer mortality table and a horizon past 120 months each admit a longer cover or
    frame.  Rather than hold the References to the shipped values, which would refuse
    whole tables the in-force step projected, the frame refuses, by point, a cover longer
    than 1,236 months and a frame longer than 1,356 (:data:`CACHE_EDGES`), under
    References that admit both: the longest frame projects, a month longer is refused; a
    cover a year longer is refused on either chassis; and a bond whose units run out in
    month 1,356 projects the longest frame, its exhaustion found there and its survivors
    encashed, while one whose units last a month longer, or never run out, is refused, the
    search reading no month past 1,356 and so finding none.  A bound a month too long
    admits a frame the compiled model reads past its ``t`` cache, raising ``IndexError``
    where modelx projects; the compile tests hold both engines to these rows.  The cover's
    bound is conservative: it is read before the exhaustion search, whose months it bounds,
    so it refuses a withdrawing bond whose cover is a year longer even where its units run
    out within the caches, the bond in force at 24 whose units run out at policy month 798,
    a frame of 774 months, which the in-force step projects.
    """
    model = mx.read_model(_sec_inputs(tmp_path, _cache_edges()), name=_name("caches"))
    try:
        _set_refs(model, CACHE_REFS)
        for n, (case, _, _, outcome) in enumerate(CACHE_EDGES):
            p = _point(model, 301 + n)
            if isinstance(outcome, int):
                assert p.proj_len() == outcome, case
            else:
                _refused(p.result_cf, f"point_id {301 + n}: {outcome}")
        ended, later, never = (_point(model, 301 + n) for n in (4, 5, 6))
        assert ended.fund_exhaust_mth() == 1156 and ended.is_forced_encashment()
        for p in (later, never):
            assert p.fund_exhaust_mth() == p.cover_end_mth() + 1 == 1237
        held = _point(model, 301 + CONSERVATIVE)
        assert held.cover_end_mth() == 1248 > 1236, held.cover_end_mth()
        assert held.fund_exhaust_mth() == CONSERVATIVE_RUN_OUT
        assert held.fund_exhaust_mth() - held.duration_mth_init() == 774 < 1356
    finally:
        model.close()


# Each Reference proj_len() holds to a domain, as (case, the References set, the S point
# whose twin is read, the message where refused, and where the frame accepts a value the
# reports refuse, the start of their message).  The point is the bond variant issued at the
# valuation date, whose 267 months read every bond Reference, its market value reduction and
# its guarantee date among them, or for the rule and the discount the endowment.  NaN and
# the infinities are outside every domain.  WP_UK_S reads mort_be_factor inside the cap's
# min, which reads an infinity as certain death; amc_rate, guar_charge_rate_base and
# smooth_cap through twelfth roots with no real value past 1, and the two charges together
# as one factor on the balance; corridor_lo and corridor_hi, the guarantee-imminent and
# MVR-deterrent factors and guarantee_exercise_rate through a max and a min, the surrender
# rate's bound first, which reads a NaN as certain surrender; the estate distribution and
# the death uplift before a floor, which reads a NaN as an exhausted share; bonus_change_cap
# through a clamp a NaN is lost through; and the limits in comparisons a NaN switches off,
# omega_age sizing every bond's frame.  Each is refused at the nearest value outside each
# edge of its domain, and accepted at the edge itself, whose reports then project, in finite
# floats over the whole frame (M11's template), or are refused where a value first leaves
# the floats, or where the contract refuses it, a bond that buys no units being spent in its
# issue month: the largest finite float an edge of each domain unbounded above.  The
# horizon's largest whole number grows the worked example's +7% past the floats, and decays
# the down scenario's below the smallest, each refused, the latter by the frame, whose
# exhaustion search declares on that withdrawing bond: a horizon of 4,500 underflows there,
# where 4,000 does not.  issue_age_min, omega_age and bonus_horizon are whole numbers below
# 2**53, which the compiled model holds as long long, printed through int() once whole:
# each is refused at a fraction and at exactly 2**53, and its largest whole number
# accepted, or refused by a later rule.  issue_age_min is 0 or more, as at the in-force
# step, and accepted at 0: a value of it refuses no point whose frame the compiled model's
# caches hold, which proj_len() holds by point instead (CACHE_EDGES).  The rule's
# References are read with the rule on, on the endowment, point 5, where its every term is
# read.
RULE = {"bonus_rule_on": True}


def _domain(ref, rule, accepted, refused, printed=float, point=7, also=None):
    """The DOMAINS cases of ``ref``: each of ``accepted`` projects, or its reports refuse
    as ``accepted`` maps it; each of ``refused`` is refused by the domain's ``rule``, and NaN
    and the infinities by it too.  ``also`` are References set beside it."""
    also = also or {}
    message = f"point_id {point}: {ref} must be {rule}, not {{}}"
    if not isinstance(accepted, dict):
        accepted = dict.fromkeys(accepted)
    cases = [(f"{ref}={value!r}", {**also, ref: value}, point, None, report)
             for value, report in accepted.items()]
    cases += [(f"{ref}={value!r}", {**also, ref: value}, point,
               message.format(printed(value)), None) for value in refused]
    return cases + [(f"{ref}={value!r}", {**also, ref: value}, point,
                     message.format(float(value)), None)
                    for value in (math.nan, math.inf, -math.inf)]


def _whole_domain(ref, accepted, least=0, point=7, also=None):
    """The DOMAINS cases of an integer Reference: a whole number below 2**53, and
    ``least`` or more, printed through int() once whole."""
    also = also or {}
    whole = f"point_id {point}: {ref} must be a whole number below 2**53, not {{}}"
    cases = [(f"{ref}={value!r}", {**also, ref: value}, point, None, None)
             for value in accepted]
    if least is not None:
        cases.append((f"{ref}={least - 1}", {**also, ref: least - 1}, point,
                      f"point_id {point}: {ref} must be {least} or more, not {least - 1}", None))
    return cases + [(f"{ref}={value!r}", {**also, ref: value}, point,
                     whole.format(float(value)), None)
                    for value in (0.5, 120.5, WHOLE, 1e300, math.nan, math.inf, -math.inf)]


_FINITE_0 = ("a finite number, 0 or more", (0.0, BIG), (BELOW_0,))
_SHARE = ("a number from 0 to 1", (0.0, 1.0), (BELOW_0, ABOVE_1))
_ASSET_SHARE = "point_id {}: the asset share of month {} before its floor"
OMEGA = ("point_id 7: omega_age must be above issue_age_min, 18, and at most 121, a year "
         "past mort_table.csv's last age, not {}")
CHARGED = ("point_id 7: amc_rate and guar_charge_rate_base must together charge at most the "
           "whole asset share in a month, their monthly rates summing to 1 or less, not ")
DOMAINS = [
    *_domain("mort_be_factor", *_FINITE_0),
    *_domain("amc_rate", "a number from 0 to 1", (0.0,), (BELOW_0, ABOVE_1)),
    *_domain("guar_charge_rate_base", "a number from 0 to 1", (0.0,), (BELOW_0, ABOVE_1)),
    ("amc_rate=1 with no guarantee charge", {"amc_rate": 1.0, "guar_charge_rate_base": 0.0},
     7, None, None),
    ("guar_charge_rate_base=1 with no management charge",
     {"amc_rate": 0.0, "guar_charge_rate_base": 1.0}, 7, None, None),
    ("amc_rate=1 with a guarantee charge", {"amc_rate": 1.0}, 7,
     CHARGED + "1.0000833715521975, under amc_rate 1.0 and guar_charge_rate_base 0.001", None),
    ("both charges at 1", {"amc_rate": 1.0, "guar_charge_rate_base": 1.0}, 7,
     CHARGED + "2.0, under amc_rate 1.0 and guar_charge_rate_base 1.0", None),
    *_domain("guar_charge_cap", *_SHARE),
    *_domain("misc_surplus_rate", "a finite number, 0 or more",
             {0.0: None, BIG: "point_id 7: the estate distribution misc_surplus_pp(1) is "
                              "inf, not a finite number"}, (BELOW_0,)),
    *_domain("prem_alloc_rate", "a number from 0 to 1", (1.0,), (BELOW_0, ABOVE_1)),
    ("prem_alloc_rate=0.0", {"prem_alloc_rate": 0.0}, 7,
     "point_id 7: the bond's units run out in its first month on the books, policy month 0, "
     "so its frame would end before it began", None),
    *_domain("death_benefit_factor", "a finite number, 0 or more",
             {0.0: None, BIG: "point_id 7: the guaranteed death benefit death_guar_pp(0) is "
                              "inf, not a finite number"}, (BELOW_0,)),
    *_domain("shareholder_transfer_divisor", "a finite number above 0",
             {ABOVE_0: "point_id 7: the shareholder transfer shareholder_transfer_pp(11) is "
                       "inf, not a finite number", BIG: None}, (0.0,)),
    *_domain("surr_disc_rate", "a finite number above -1",
             {math.nextafter(-1.0, 0.0): (
                 "point_id 5: the endowment's discount on its bonus cost, "
                 "(1 + surr_disc_rate)^24 in cost_of_bonus_pp(11), is 0.0, below the "
                 "smallest float"), BIG: (
                 "point_id 5: the endowment's discount on its bonus cost, "
                 "(1 + surr_disc_rate)^24 in cost_of_bonus_pp(11), is past the largest "
                 "float")}, (-1.0,), point=5),
    *_domain("smooth_cap", *_SHARE),
    *_domain("corridor_lo", *_SHARE),
    *_domain("corridor_hi", "a finite number, 1 or more", (1.0, BIG), (BELOW_1,)),
    ("bonus_rule_on=True", {"bonus_rule_on": True}, 7, None, None),
    ("bonus_rule_on=1", {"bonus_rule_on": 1}, 7, None, None),
    *[(f"bonus_rule_on={value!r}", {"bonus_rule_on": value}, 7,
       f"point_id 7: bonus_rule_on must be True or False, not {value!r}", None)
      for value in (2, 0.5, math.nan, None, "yes")],
    *_domain("guar_fill_target", "a finite number, 0 or more",
             {0.0: None, BIG: "point_id 5: the supportable bonus rate bonus_supportable(11) "
                              "is inf, not a finite number"}, (BELOW_0,), point=5, also=RULE),
    *_domain("bonus_speed", *_SHARE, point=5, also=RULE),
    *_domain("bonus_change_cap", *_FINITE_0, point=5, also=RULE),
    *_whole_domain("bonus_horizon", (1, 10.0), least=1, also=RULE),
    ("bonus_horizon=2**53-1", {**RULE, "bonus_horizon": WHOLE - 1}, 7,
     "point_id 7: the bonus rule's growth factor (1 + r_e)^m in bonus_supportable(11) is "
     "0.0, below the smallest float", None),
    ("bonus_horizon=4500", {**RULE, "bonus_horizon": 4500}, 7,
     "point_id 7: the bonus rule's growth factor (1 + r_e)^m in bonus_supportable(11) is "
     "0.0, below the smallest float", None),
    ("bonus_horizon=4000", {**RULE, "bonus_horizon": 4000}, 7, None, None),
    ("bonus_horizon=2**53-1 at +7%", {**RULE, "bonus_horizon": WHOLE - 1}, 1, None,
     "point_id 1: the bonus rule's growth factor (1 + r_e)^m in bonus_supportable(11) is "
     "past the largest float"),
    *_domain("mvr_deterrent_factor", *_FINITE_0),
    *_domain("guarantee_exercise_rate", *_SHARE),
    *_domain("guarantee_imminent_factor", *_FINITE_0),
    *_domain("expense_maint", *_FINITE_0),
    *_domain("inflation_rate", "a finite number, -1 or more",
             {-1.0: None, BIG: "point_id 7: the expenses expenses(12) are inf, not a finite "
                               "number, from expense_maint 30.0 and inflation_rate "
                               "1.7976931348623157e+308"},
             (math.nextafter(-1.0, -2.0),)),
    *_whole_domain("issue_age_min", (0, 18.0), least=0),
    ("issue_age_min=2**53-1", {"issue_age_min": WHOLE - 1}, 7,
     f"point_id 7: the issue age, 55, is below issue_age_min, {int(WHOLE - 1)}", None),
    *_whole_domain("omega_age", (120, 121, 120.0), least=None),
    ("omega_age=122", {"omega_age": 122}, 7, OMEGA.format(122), None),
    ("omega_age=18", {"omega_age": 18}, 7, OMEGA.format(18), None),
    ("omega_age=55", {"omega_age": 55}, 7,
     "point_id 7: the issue age, 55, is at or past omega_age, 55: the bond has no cover",
     None),
    ("omega_age=2**53-1", {"omega_age": WHOLE - 1}, 7, OMEGA.format(int(WHOLE - 1)), None),
]


@pytest.fixture(scope="module")
def domain_extract(tmp_path_factory):
    """The committed table as an extract labels it (:func:`_extract_of`), in a folder of its
    own: ``(the SEC folder, {committed label: extract label})``."""
    table, relabel = _extract_of()
    return _sec_inputs(tmp_path_factory.mktemp("domain_extract"), table), relabel


@pytest.mark.parametrize("case, refs, point, message, report", DOMAINS,
                         ids=[c[0] for c in DOMAINS])
def test_each_reference_is_held_to_its_domain_at_both_edges(domain_extract, case, refs,
                                                            point, message, report):
    """``proj_len()`` holds each Reference to its domain, NaN and the infinities outside it.

    ``WP_UK_S`` checks none of them, and off its domain each projects a negative rate,
    charge or expense, a twelfth root with no real value, a factor that changes sign each
    year, or a NaN that a comparison loses, every check passing: a NaN smoothing cap is lost
    through the cap's ``max`` and ``min``, a NaN deterrent reads as certain surrender, a NaN
    estate distribution as an exhausted share, and a NaN limiting age switches off every
    comparison with it, the limiting age sizing every bond's frame.  The frame refuses each
    such Reference, by name, before it projects anything, and every report with it, at the
    nearest value outside each edge of its domain, and on each combination a formula reads,
    the two charges' monthly rates summed, and accepts the edge itself (:data:`DOMAINS`):
    the integer References at a fraction and at exactly ``2**53``, and ``omega_age`` past
    the mortality table's last age.  Each edge accepted projects its reports, in finite
    floats over the whole frame, but where the edge makes a value past the floats, which is
    refused where it first is, naming the point (M11's template).  A whole float, ``120.0``,
    reads as the whole number.  Each case sets its References on a model just read (K7),
    from an extract labelled otherwise than by position, and each refusal must name the
    extract's label: a refusal naming its point by ``idx + 1`` names another here.
    """
    folder, relabel = domain_extract
    model = mx.read_model(folder, name=_name("domain"))
    try:
        for ref, value in refs.items():
            setattr(model.Projection, ref, value)
        p = _point(model, relabel[_label(_committed(), "twin", point, ENTRY[point])])
        if message is not None:
            _refused_naming(p.result_cf, _by_label(message, relabel))
        elif report is not None:
            assert p.proj_len() > 0
            _refused_naming(lambda: [p.cells[name]() for name in REPORTS],
                            _by_label(report, relabel))
        else:
            for name in REPORTS:
                frame = p.cells[name]()
                assert list(frame.index) == list(range(p.proj_len())), (case, name)
                assert np.isfinite(frame.to_numpy(dtype=float)).all(), (case, name)
    finally:
        model.close()


# A value that leaves the floats, from an opening state and References each in its domain,
# as (case, the table's edit, the References set, the point, the call, the report that
# reads it first, the start of the message).  An opening premium near the largest float on
# the bond issued at the valuation date, with a regular premium beside it; a unit price of
# 1e305 opening the bond variant at 60, whose withdrawal reads the guarantee it opens with,
# and the down scenario at 68, whose guarantee is the units at that price; an opening asset
# share of 1.79e308 grown by a month's return; the smallest price above 0 buying units with
# a premium; a price near the largest float raised by a declaration in month 0; an
# endowment's bonus cost discounted at a rate a hair above -1, the discount near the
# smallest float; the charges taken grown past the floats by a charge of the whole asset
# share, under a cap of all of it; an opening smoothing account of 1e308 on two policies;
# and each flow on a count that takes it past the floats, the transfers through a divisor
# near 0, and the net cash flow summing an expense and a transfer each just inside them.
# Then the three powers: the inflation factor at the second anniversary under 1e200, the
# bonus rule's growth to a horizon of 20 years at a return of 1e20, and the endowment's
# discount at a rate of 1e200.  Each is refused in the cell where it first is, naming the
# point, the month and what makes it, and so is the report that reads it first; but the
# withdrawals' report reads first the guarantee date's surrenders on that count, past the
# floats too, which it names instead (the report given with its own message).
NET = 1.7e308
PAST_THE_FLOATS = [
    ("a premium", _then(_set("premium_single", [7], BIG), _set("premium_regular", [7], BIG)),
     {}, 7, ("premium_pp", 0), "result_cf",
     "point_id 7: the premium premium_pp(0) is inf, not a finite number, from the single "
     "premium 1.7976931348623157e+308 and the regular premium's twelfth "),
    ("an opening guarantee", _set("unit_price_init", [20], 1e305), {}, 20,
     ("guar_benefit_open", 0), "result_cf",
     "point_id 20: the guarantee the books open with, guar_benefit_open(0), is inf, not a "
     "finite number, from "),
    ("an asset share", _set("asset_share_init", [13], BIG), {}, 13, ("asset_share", 0),
     "result_cf",
     "point_id 13: the asset share of month 0 before its floor, asset_share_at(0, 'AFT_MC'), "
     "is inf, not a finite number, from the opening asset share 1.7976931348623157e+308"),
    ("the units", _set("unit_price_init", [7], ABOVE_0), {}, 7, ("units", 0), "result_cf",
     "point_id 7: the units held units(0) are inf, not a finite number, from the opening "
     "units 0.0 at the price 5e-324 and the premium 25000.0"),
    ("a unit price", _set("unit_price_init", [8], 1.79e308), {}, 8, ("unit_price", 0),
     "result_cf",
     "point_id 8: the unit price unit_price(0) is inf, not a finite number, from the opening "
     "price 1.79e+308 and the bonus rate 0.02"),
    ("a guarantee", _set("unit_price_init", [9], 1e305), {}, 9, ("guar_benefit_pp", 0),
     "result_cf",
     "point_id 9: the guaranteed benefit guar_benefit_pp(0) is inf, not a finite number, from "
     "25000.0 units at the price 1e+305"),
    ("a cost of bonus", None, {"surr_disc_rate": -1.0 + 1e-13}, 5, ("cost_of_bonus_pp", 11),
     "result_cf",
     "point_id 5: the cost of bonus cost_of_bonus_pp(11) is inf, not a finite number, from "
     "the bonus rate 0.015"),
    ("the charges taken",
     _then(_set("asset_share_init", [13], 1.7e308),
           _set("guar_charge_cum_pp_init", [13], 1.69e308)),
     {"guar_charge_cap": 1.0, "guar_charge_rate_base": 1.0, "amc_rate": 0.0}, 13,
     ("guar_charge_cum_pp", 0), "result_cf",
     "point_id 13: the cumulative guarantee charge guar_charge_cum_pp(0) is inf, not a finite "
     "number, from the charges carried in, 1.69e+308, and the month's charge, "),
    ("the smoothing account",
     _then(_set("smoothing_account_init", [24], 1e308), _set("policy_count", [24], 2.0)), {},
     24, ("smoothing_account", 0), "result_payout",
     "point_id 24: the smoothing account smoothing_account(0) is inf, not a finite number, "
     "from the account carried in, inf, and the month's cost, "),
    ("the premiums", _set("policy_count", [7], 1e307), {}, 7, ("premiums", 0), "result_cf",
     "point_id 7: the premiums premiums(0) are inf, not a finite number, from premium_pp(0) "
     "25000.0 on pols_if(0) 1e+307 policies"),
    ("the withdrawals", _set("policy_count", [18], 1.75e306), {}, 18, ("withdrawals", 0),
     ("result_cf", "point_id 18: the claims claims(19, 1) are inf, not a finite number"),
     "point_id 18: the withdrawals withdrawals(0) are inf, not a finite number, from wd_pp(0) "
     "104.16666666666667 on pols_if(0) 1.75e+306 policies"),
    ("the claims", _set("policy_count", [1], 1e308), {}, 1, ("claims", 0, "DEATH"),
     "result_cf",
     "point_id 1: the claims claims(0, 0) are inf, not a finite number, from "
     "claim_pp(0, 0) "),
    ("the expenses", None, {"expense_maint": NET, "inflation_rate": 1.0}, 1, ("expenses", 48),
     "result_cf",
     "point_id 1: the expenses expenses(48) are inf, not a finite number, from expense_maint "
     "1.7e+308 and inflation_rate 1.0"),
    ("the shareholder transfers", _set("policy_count", [8], 1e10),
     {"shareholder_transfer_divisor": 1e-300}, 8, ("shareholder_transfers", 0), "result_cf",
     "point_id 8: the shareholder transfers shareholder_transfers(0) are inf, not a finite "
     "number, from the transfer on the declaration "),
    ("the net cash flow", _set("policy_count", [8], 11.0),
     {"expense_maint": BIG, "shareholder_transfer_divisor": 3.75e-305}, 8, ("net_cf", 0),
     "result_cf",
     "point_id 8: the net cash flow net_cf(0) is -inf, not a finite number, from premiums "
     "0.0, claims "),
    ("the inflation factor", None, {"inflation_rate": 1e200}, 1, ("inflation_factor", 24),
     "result_cf",
     "point_id 1: the inflation factor inflation_factor(24) is past the largest float, under "
     "inflation_rate 1e+200"),
    ("the bonus rule's growth", _set("fund_return", [1], 1e20),
     {"bonus_rule_on": True, "bonus_horizon": 20}, 1, ("bonus_rate", 11), "result_cf",
     "point_id 1: the bonus rule's growth factor (1 + r_e)^m in bonus_supportable(11) is past "
     "the largest float, under fund_return 1e+20, amc_rate 0.01"),
    ("the endowment's discount", None, {"surr_disc_rate": 1e200}, 5,
     ("cost_of_bonus_pp", 11), "result_cf",
     "point_id 5: the endowment's discount on its bonus cost, (1 + surr_disc_rate)^24 in "
     "cost_of_bonus_pp(11), is past the largest float, under surr_disc_rate 1e+200"),
]

# The cells whose month before is in the same policy year's read, so not a month apart.
SAME_YEAR = frozenset({"bonus_rate"})


@pytest.mark.parametrize("case, edit, refs, point, call, report, message", PAST_THE_FLOATS,
                         ids=[c[0] for c in PAST_THE_FLOATS])
def test_a_value_past_the_floats_is_refused_where_it_first_is(tmp_path, case, edit, refs,
                                                              point, call, report, message):
    """A value past the largest float is refused in the cell where it first is.

    ``Data`` and ``proj_len()`` hold each opening amount, count and Reference to a finite
    number, so a value near the largest float reads; a return, a price, a declaration, a
    count, a sum or a power then takes a value the projection computes past the floats,
    where ``WP_UK_S`` would carry an infinite asset share, price or flow, or a NaN, every
    report infinite and its checks NaN or passing, and where Python's power raises
    ``OverflowError``, naming nothing, and C's gives an infinity.  The cell where the value
    first leaves the floats refuses it, naming the point, the month and what makes it
    (:data:`PAST_THE_FLOATS`), and so does the report that reads it first (UKLIB-SEC-PLAN.md
    §6.6, *Carried into M10 and after*; *Record — M11*).  The month before projects, but in
    a cell whose months read one declaration (:data:`SAME_YEAR`).  Each Reference is set on
    a model just read (K7), from an extract labelled otherwise than by position, whose
    label each refusal must name.
    """
    table, relabel = _extract_of(edit)
    model = mx.read_model(_sec_inputs(tmp_path, table), name=_name("past_floats"))
    try:
        for ref, value in refs.items():
            setattr(model.Projection, ref, value)
        p = _point(model, relabel[point])
        name, t, *rest = call
        rest = [_code(p, a) if isinstance(a, str) else a for a in rest]
        if t > p.t_entry() and name not in SAME_YEAR:
            p.cells[name](t - 1, *rest)
        _refused_naming(lambda: p.cells[name](t, *rest), _by_label(message, relabel))
        report, first = report if isinstance(report, tuple) else (report, message)
        _refused_naming(p.cells[report], _by_label(first, relabel))
    finally:
        model.close()


@pytest.mark.parametrize("grid", GRIDS)
def test_a_whole_limit_written_as_a_float_projects_as_the_int_does(grid):
    """``omega_age = 120.0`` projects what 120 projects, cell for cell (§6.5).

    ``proj_len()`` holds ``omega_age``, ``issue_age_min`` and ``bonus_horizon`` to whole
    numbers, which ``120.0``, ``18.0`` and ``10.0`` are, and reads ``omega_age`` and
    ``bonus_horizon`` as the ``int`` each is: a float limit would make ``proj_len()`` the
    float 720.0, on which every report's ``range`` raises ``TypeError``, where the compiled
    model, typing the Reference ``long long``, would project.  So with the three set as
    floats, and the bonus rule on in both models so that its horizon is read, on a model
    just read, rows of each kind are what the model makes of them under the ints in every
    cell, bit for bit, each integer cell an ``int`` in both.

    The twin of the worked example's bond and the endowment issued at the valuation date
    run by default, and the withdrawing bond in its last month and the future row with the
    full grid.
    """
    floats = mx.read_model(model_path(SEC), name=_name("floats"))
    ints = mx.read_model(model_path(SEC), name=_name("ints"))
    try:
        for model in (floats, ints):
            model.Projection.bonus_rule_on = True
        floats.Projection.omega_age = 120.0
        floats.Projection.issue_age_min = 18.0
        floats.Projection.bonus_horizon = 10.0
        cases = ((("twin", 1, 60), ("twin", 5, 0)) if grid == "core"
                 else (("derived", 4, 402), ("future", 7, -13)))
        for case in cases:
            mine, theirs = _row(floats, *case), _row(ints, *case)
            sweep(theirs)
            assert twin_mismatches(theirs, mine, exempt=frozenset(), rtol=0.0,
                                   atol=0.0) == [], case
            for name in ("proj_len", "cover_end_mth", "fund_exhaust_mth", "t_entry",
                         "duration_mth_init"):
                assert type(mine.cells[name]()) is int, (case, name)
    finally:
        ints.close()
        floats.close()


# The extra rows of the edges test, each a committed row under a label of its own with the
# columns changed, and the frame it projects, as {label: ((row_kind, S point, month), the
# columns changed, proj_len)}: the endowment at 11 holding half a cent of attaching bonus,
# rule 13's edge; the declaration row's duration written 71.0; the bond variant issued 120
# months on, the horizon; a bond issued at 18 and at 119, the youngest issue age and the
# last year before the limiting age, and an endowment issued at 18 maturing at it, 102
# years on, the contract's longest cover; a count of 0; the whole original premium
# withdrawn a year, the share's edge, which exhausts the units in the 14th month; a return
# a hair above -1, the return's edge; a bond with no guarantee date; a smoothing account of
# minus the largest float; a bonus rate of 0; the smallest price above 0; and rule 13's
# edges, a payout of 0 beside an asset share of a cent and of half a cent, an extract's to
# the cent of S's £0.006 and £0.0048.
EDGES = {
    25: (("derived", 5, 11), {"attaching_bonus_init": 0.005}, 289),
    26: (("derived", 1, 71), {"duration_mth": 71.0}, 709),
    27: (("future", 7, -13), {"duration_mth": -120}, 387),
    28: (("twin", 7, 0), {"age_at_entry": 18, "wd_rate": 0.0}, LONGEST),
    29: (("twin", 5, 0), {"age_at_entry": 18, "policy_term": 102}, LONGEST),
    30: (("twin", 7, 0), {"age_at_entry": 119, "wd_rate": 0.0}, 12),
    31: (("twin", 1, 60), {"policy_count": 0.0}, 720),
    32: (("twin", 1, 60), {"wd_rate": 1.0}, 13),
    33: (("twin", 2, 60), {"fund_return": math.nextafter(-1.0, 0.0)}, 720),
    34: (("twin", 1, 60), {"guarantee_dates": float("nan")}, 720),
    35: (("derived", 1, 71), {"smoothing_account_init": -BIG}, 709),
    36: (("derived", 1, 71), {"bonus_rate_init": 0.0}, 709),
    37: (("twin", 1, 60), {"unit_price_init": ABOVE_0}, 720),
    38: (("derived", 2, 242), {"asset_share_init": 0.01}, 538),
    39: (("derived", 2, 242), {"asset_share_init": 0.005}, 538),
}


def test_the_edges_of_the_in_force_interface_are_accepted(sec_model, tmp_path):
    """Each edge of the in-force interface is read, and projects its reports (T5).

    An asset share and a payout of 0 in force, the down scenario's at 242 with its asset
    share floored, and a smoothing account below 0, which the endowment's payouts short of
    their asset shares leave, are committed rows, and read.  Then :data:`EDGES`, each a
    committed row under a label of its own with columns changed, in one table: ``Data``
    reads it, and each row projects the frame given, its three reports in finite floats
    over the whole of it.  ``71.0`` is a whole number of months, read back as the ``int``
    the policy clock counts in, and the row projects what the committed row does, bit for
    bit; a count of 0 projects zeros; and the whole withdrawal exhausts the bond in its 14th
    month, a forced encashment.
    """
    committed = _committed()
    assert committed.at[_label(committed, "derived", 2, 242), "asset_share_init"] == 0.0
    assert committed.at[_label(committed, "derived", 2, 242), "smoothed_payout_init"] == 0.0
    assert (committed["smoothing_account_init"] < 0.0).sum() >= 3
    rows = []
    for label, (case, changes, _) in EDGES.items():
        row = committed.loc[[_label(committed, *case)]].assign(**changes)
        rows.append(row.set_axis(pd.Index([label], name="point_id")))
    model = mx.read_model(_sec_inputs(tmp_path, pd.concat([committed, *rows])),
                          name=_name("edges"))
    try:
        assert len(model.Data.model_point_table()) == len(committed) + len(EDGES)
        for label, (case, changes, frame) in EDGES.items():
            p = _point(model, label)
            assert p.proj_len() == frame, (label, p.proj_len())
            for name in REPORTS:
                df = p.cells[name]()
                assert list(df.index) == list(range(frame)), (label, name)
                assert np.isfinite(df.to_numpy(dtype=float)).all(), (label, name)
        whole = _point(model, 26)
        assert type(whole.duration_mth_init()) is int and whole.duration_mth_init() == 71
        shipped = _row(sec_model, "derived", 1, 71)
        for name in REPORTS:
            assert frame_mismatches(shipped.cells[name](), whole.cells[name](), rtol=0.0,
                                    atol=0.0) == [], name
        none = _point(model, 31).result_cf()
        assert (none.drop(columns="asset_share") == 0.0).all().all()
        spent = _point(model, 32)
        assert spent.is_forced_encashment() and spent.fund_exhaust_mth() == 73
    finally:
        model.close()


# The S months a point is restated at by the every-state test, by default: the edges of its
# windows, every month of the first policy year and the first anniversary, the declaration
# and the anniversary of every fifth policy year, the guarantee window from its imminence
# to the guarantee date, policy months 106 to 120, and the last month of the frame; with
# UKLIB_SEC_FULL=1, every month.
def _every_state_months(start, end):
    if SEC_FULL:
        return list(range(start + 1, end))
    months = {*range(1, 14), end - 1, *range(106, 121),
              *(m for a in range(60, end, 60) for m in (a - 1, a))}
    return sorted(m for m in months if start < m < end)


def _states(s):
    """Each ``(S point, month)`` of :func:`_every_state_months` on every point of ``s``."""
    table = s.Data.model_point_table()
    found = []
    for key, point_id in zip(point_keys(s), table.index):
        p = projection(s, key)
        found += [(point_id, d) for d in _every_state_months(p.proj_start(), p.proj_len())]
    return found


def _restated(root, s, states):
    """The twins of ``s``'s points and a row in force at each of ``states``, ``(S point,
    month)``, built by the generator out of ``s`` into a copy of the product directory:
    ``(folder, table)``."""
    spec = dataclasses.replace(SPEC, derived=tuple(states), future=(), derived_refs={})
    table, _ = build_sec_table(spec, s)
    return _sec_inputs(root, table), table


def _states_apart(a, b):
    """The state columns, the count among them, in which two tables of :func:`_restated`
    differ on the states, ``(S policy, month)``, they share, of which there must be some."""
    both = a.index.intersection(b.index)
    assert len(both), "the two tables share no state"
    return {c for c in ("policy_count", *STATE)
            if (a.loc[both, c] - b.loc[both, c]).abs().max() > 1e-9 * max(
                1.0, a.loc[both, c].abs().max())}


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


# The other inputs that move the states S reaches, beside the splice's two sets: the
# guarantee charge doubled and the smoothing cap halved, under which the committed rows'
# own References read the cumulants and the payout.
CHARGE_SET = {"guar_charge_rate_base": 0.002}
SMOOTH_SET = {"smooth_cap": 0.05}


def test_every_state_s_reaches_is_accepted_in_force(s_model, tmp_path):
    """Every state ``WP_UK_S`` reaches is a valid opening state (T5).

    ``Data``'s rules and ``proj_len()``'s hold an opening state to what a policy in force
    can be, so they must accept each state the S model reaches: a rule exercised only on
    the rows the other tests choose could refuse a state S reaches elsewhere (D6).  So each
    point of S is restated in force by the generator at the edges of its windows, or with
    ``UKLIB_SEC_FULL=1`` at every month of its frame (:func:`_every_state_months`), into
    one table beside the twins: ``Data`` reads it, and no row's ``proj_len()`` refuses it
    (USLIB-SEC-PLAN.md §5.2, T5, precised at M10).  It runs on each set of inputs on which
    the states differ (precised at M9):

    * S as shipped, its seven points under its own References (``s_model``);
    * with ``UKLIB_SEC_FULL=1``, the others: the splice's main set, its points and variants
      under :data:`SPLICED_REFS`, the estate distribution on, a woman, the crash and the
      pension basis among them; its second set, under :data:`RULE_REFS`, the bonus rule on;
      the guarantee charge doubled, :data:`CHARGE_SET`, and the smoothing cap halved,
      :data:`SMOOTH_SET`, on S's points, the committed rows' own References.  The default
      run takes S as shipped alone, at the cost of the other sets' states, which the full
      grid's leg asks (the M13 review; UKLIB-SEC-PLAN.md U6, as VA and IUL do).

    Each set but the first is read into an S model of its own, which is closed once its
    states are asked, so that one set's projections are held at a time.

    Between them the sets move every state column and the count away from S's shipped
    states, and the rule moves the unit price, the attaching bonus, the bonus rate and the
    withdrawing bond's units, which no other set moves.  ``WP_UK_SEC`` refuses no state
    ``WP_UK_S`` reaches, so none is set aside.
    """
    variants = temp_inputs(tmp_path / "variants", model_path(TWIN),
                           model_points=_s_table_with_variants())
    sets = {"shipped": (None, {})}
    if SEC_FULL:
        sets.update(main=(variants, SPLICED_REFS), rule=(variants, RULE_REFS),
                    charge=(model_path(TWIN), CHARGE_SET),
                    smooth=(model_path(TWIN), SMOOTH_SET))
    found, states = {}, {}
    for tag, (folder, refs) in sets.items():
        s = s_model if folder is None else mx.read_model(folder, name=_name(tag))
        try:
            for ref, value in refs.items():
                setattr(s.Projection, ref, value)
            reached = _states(s)
            restated, rows = _restated(tmp_path / tag, s, reached)
            assert len(rows) == len(s.Data.model_point_table()) + len(reached)
        finally:
            if folder is not None:
                s.close()
        states[tag] = rows.set_index(["source_policy_id", "source_mth"])
        refused = _refused_in_force(restated, refs)
        if refused:
            found[tag] = f"{len(refused)} refused, first: {refused[:5]}"
    assert not found, found
    if not SEC_FULL:
        return
    apart = {tag: _states_apart(states["shipped"], states[tag]) for tag in sets
             if tag != "shipped"}
    assert set().union(*apart.values()) == {"policy_count", *STATE}, apart
    moved_by_rule = apart["rule"] - set().union(
        *(cols for tag, cols in apart.items() if tag != "rule"))
    assert moved_by_rule >= {"unit_price_init", "attaching_bonus_init", "bonus_rate_init",
                             "units_init"}, apart


# ---------------------------------------------------------------------------
# The assumption tables
#
# Data checks each table before a value of it is read, in the cell the projection takes
# its extent from, reading the file as it stands (UKLIB-SEC-PLAN.md §4; USLIB-SEC-PLAN.md
# §7.1, *Precised at M3*, item 9).  Each case is the shipped tables with one fault, read
# from a copy, refused by its Data cell alone, naming the file, the column and its lines,
# the header line 1, and through a projection of the worked example's bond, which reads
# both tables.  The lines are the shipped files': mort_table.csv holds the men at ages 18 to
# 120 on lines 2 to 104 and the women on lines 105 to 207; lapse_table.csv the bond's one
# policy year on line 2 and the endowment's years 1 to 4 on lines 3 to 6.
MORT, LAPSE = "mort_table.csv", "lapse_table.csv"


def _written(column, value, where):
    """An edit of a table that writes ``value`` into ``column`` on the rows ``where``
    picks."""
    def edit(table):
        cells = table[column].astype(object)
        cells[where(table)] = value
        return table.assign(**{column: cells})
    return edit


def _dropped(where):
    return lambda table: table[~where(table)]


def _repeated(where):
    return lambda table: pd.concat([table, table[where(table)]], ignore_index=True)


def _rate_at(sex, age):
    return lambda t: (t["sex"] == sex) & (t["age"] == age)


def _year(chassis, year):
    return lambda t: (t["chassis"] == chassis) & (t["policy_year"] == year)


MORT_RATE = f"{MORT}: mort_rate must be a number from 0 to 1; it is not on line "
LAPSE_RATE = f"{LAPSE}: lapse_rate must be a number from 0 to 1; it is not on line "
AGES = (f"{MORT}: the ages of each sex must run from 18 to 120, the table's first and last, "
        f"one row an age, none below 0; ")
YEARS = (f"{LAPSE}: the policy years of each chassis must run from 1, one row a year, "
         f"without a gap or a repeat; ")
UNREADABLE = [
    ("a blank mortality rate", MORT, _written("mort_rate", float("nan"), _rate_at("M", 60)),
     "mort_age_first", MORT_RATE + "[44]"),
    ("a mortality rate past 1", MORT, _written("mort_rate", ABOVE_1, _rate_at("F", 80)),
     "mort_age_first", MORT_RATE + "[167]"),
    ("a negative mortality rate", MORT, _written("mort_rate", -0.001, _rate_at("M", 18)),
     "mort_age_first", MORT_RATE + "[2]"),
    ("a text mortality rate", MORT, _written("mort_rate", "high", _rate_at("F", 30)),
     "mort_age_first", MORT_RATE + "[117]"),
    ("an age not whole", MORT, _written("age", 50.5, _rate_at("M", 50)), "mort_age_first",
     f"{MORT}: age must be a whole number; it is not on line [34]"),
    ("an unknown sex", MORT, _written("sex", "X", _rate_at("M", 70)), "mort_age_first",
     f"{MORT}: sex must be M or F; it is not on line [54]"),
    ("an age twice", MORT, _repeated(_rate_at("M", 60)), "mort_age_first",
     AGES + "sex M, age 60 repeats on lines [44, 208]"),
    ("a sex missing", MORT, _dropped(lambda t: t["sex"] == "F"), "mort_age_first",
     AGES + "no line holds sex F, ages 18 to 120"),
    ("a gap in a sex", MORT, _dropped(_rate_at("F", 80)), "mort_age_first",
     AGES + "no line holds sex F, age 80"),
    ("an age below 0", MORT, _written("age", -1, _rate_at("M", 18)), "mort_age_first",
     AGES + "age -1, below 0, is on lines [2]; no line holds sex M, age 18"),
    # numpy casts a float past int64 to the least int64 without a word, and holds an int64
    # past 2**53 inexactly in a float: the table refuses an age of 2**53 before it casts,
    # and reads one of 2**53 - 1, written as an int, which its next rule refuses, the gaps
    # found from the ages each sex holds, so that the far key costs no more than the rows.
    ("an age of 2**53", MORT, _written("age", 2.0 ** 53, _rate_at("M", 60)), "mort_age_first",
     f"{MORT}: age must be below 2**53 in size; it is not on line [44]"),
    ("an age of 2**53 - 1", MORT, _written("age", 2 ** 53 - 1, _rate_at("M", 60)),
     "mort_age_first",
     f"{MORT}: the ages of each sex must run from 18 to 9007199254740991, the table's first "
     f"and last, one row an age, none below 0; no line holds sex M, age 60; no line holds "
     f"sex M, ages 121 to 9007199254740990; no line holds sex F, ages 121 to "
     f"9007199254740991"),
    ("a blank lapse rate", LAPSE, _written("lapse_rate", float("nan"),
                                           _year("CWP_endowment", 2)),
     "lapse_last_year", LAPSE_RATE + "[4]"),
    ("a lapse rate past 1", LAPSE, _written("lapse_rate", 1.5, _year("UWP_bond", 1)),
     "lapse_last_year", LAPSE_RATE + "[2]"),
    ("a negative lapse rate", LAPSE, _written("lapse_rate", -0.1, _year("CWP_endowment", 4)),
     "lapse_last_year", LAPSE_RATE + "[6]"),
    ("a text lapse rate", LAPSE, _written("lapse_rate", "high", _year("CWP_endowment", 1)),
     "lapse_last_year", LAPSE_RATE + "[3]"),
    ("a policy year not whole", LAPSE, _written("policy_year", 2.5,
                                                _year("CWP_endowment", 2)),
     "lapse_last_year", f"{LAPSE}: policy_year must be a whole number; it is not on line [4]"),
    ("an unknown chassis", LAPSE, _written("chassis", "UWP_fund", _year("CWP_endowment", 3)),
     "lapse_last_year",
     f"{LAPSE}: chassis must be UWP_bond or CWP_endowment; it is not on line [5]"),
    ("a policy year missing", LAPSE, _dropped(_year("CWP_endowment", 3)), "lapse_last_year",
     YEARS + "no line holds chassis CWP_endowment, policy_year 3"),
    ("a policy year twice", LAPSE, _repeated(_year("CWP_endowment", 2)), "lapse_last_year",
     YEARS + "chassis CWP_endowment, policy_year 2 repeats on lines [4, 7]"),
    ("no policy year 1", LAPSE, _dropped(_year("UWP_bond", 1)), "lapse_last_year",
     YEARS + "no line holds chassis UWP_bond, policy_year 1"),
    ("a chassis missing", LAPSE, _dropped(lambda t: t["chassis"] == "CWP_endowment"),
     "lapse_last_year", YEARS + "no line holds chassis CWP_endowment, policy_year 1"),
    ("a policy year of 2**53", LAPSE, _written("policy_year", 2.0 ** 53,
                                               _year("CWP_endowment", 2)),
     "lapse_last_year",
     f"{LAPSE}: policy_year must be below 2**53 in size; it is not on line [4]"),
    ("a policy year of 2**53 - 1", LAPSE, _written("policy_year", 2 ** 53 - 1,
                                                   _year("CWP_endowment", 2)),
     "lapse_last_year",
     YEARS + "no line holds chassis CWP_endowment, policy_year 2; no line holds chassis "
     "CWP_endowment, policy years 5 to 9007199254740990"),
]


@pytest.mark.parametrize("case, file, edit, cell, message", UNREADABLE,
                         ids=[c[0] for c in UNREADABLE])
def test_a_table_a_reader_cannot_read_is_refused_naming_its_lines(tmp_path, case, file, edit,
                                                                  cell, message):
    """``Data`` refuses an assumption table before a value of it is read (§4, T5).

    ``WP_UK_S`` reads a blank rate as NaN, which its cap would keep and every flow carry; a
    rate past 1, whose monthly rate has no real value; a negative one, and a key that is not
    whole as one ``int`` truncates; and a gap in a sex or a chassis's years as a
    ``KeyError``, only where a projection reaches it.  Here the cell the projection asks
    first refuses each, naming the file, the column and its lines (:data:`UNREADABLE`), and
    so does a projection of the worked example's bond, which reads both tables:
    ``Data.mort_age_first`` the mortality table and ``Data.lapse_last_year`` the lapse
    table, every chassis's last year at once.  A key of ``2**53`` or more is refused before
    the keys are cast to int64, and one of ``2**53 - 1``, written as an int, reads, and is
    refused by the next rule, its gap found from the keys the group holds.
    """
    model = _read_edited(tmp_path, lambda t: t, edits={file: edit})
    try:
        _refused(model.Data.cells[cell], message)
        _refused(_point(model, 1).result_cf, message)
    finally:
        model.close()


def test_a_read_beyond_the_mortality_table_is_refused_naming_its_point(tmp_path):
    """An attained age the mortality table lacks is refused by the cell that reads it.

    ``proj_len()`` holds the limiting age to a year past the table's last age, and the
    issue age to ``issue_age_min``, 18 as shipped, the shipped table's first, so no frame
    the shipped tables admit reads past them.  On a copy of the mortality table cut to
    start at 20, the bond variant issued at the valuation date at 18 is admitted by the
    frame and reads an age the table lacks: ``mort_rate`` refuses it, naming the point and
    the age, where ``WP_UK_S``'s lookup raised ``KeyError``, and so does every report; at
    20 it reads the table.  A lowered ``issue_age_min`` admits an issue age below the
    shipped table's too, as at the in-force step, but a bond issued below 18 to 120 has a
    cover past the compiled model's caches, which ``proj_len()`` refuses first
    (:data:`CACHE_EDGES`), so the cut table is what admits the point here.
    """
    cut = {MORT: _dropped(lambda t: t["age"] < 20)}
    model = _read_edited(tmp_path, _then(_set("age_at_entry", [7], 18),
                                         _set("wd_rate", [7], 0.0)), edits=cut)
    try:
        p = _point(model, 7)
        assert p.proj_len() == 12 * (120 - 18)
        message = "point_id 7: mort_table.csv has no rate at attained age 18"
        _refused(lambda: p.mort_rate(0), message)
        _refused(p.result_cf, message)
        assert p.mort_rate(24) == min(
            0.6 * model.Data.mort_table_array()[p.mort_schedule(), 20], 1.0)
    finally:
        model.close()


# The rows the float keys are read on, by what they are: the worked example's bond in force,
# the endowment issued at the valuation date and in force, the withdrawing bond in its last
# month and the bond variant issued 13 months on.
FLOAT_KEYED = (("twin", 1, 60), ("twin", 5, 0), ("twin", 6, 240), ("derived", 4, 402),
               ("future", 7, -13))


def test_a_key_written_as_a_float_reads_as_wp_uk_s_reads_it(sec_model, tmp_path):
    """A key written ``70.0`` is the key 70, in every table and in every extent.

    ``WP_UK_S``'s lookups match a float key to the int the projection asks, so a table
    written by a tool that writes every number with a decimal point reads the same.  Each
    assumption table's keys and the model point table's ``duration_mth``, ``age_at_entry``
    and ``policy_term`` are written as floats, and a point of each chassis, issued at the
    valuation date, in force and to be issued later, projects what the committed tables
    project, exactly (:data:`FLOAT_KEYED`): between them they read both tables over the
    ages from 35 to 119 and each chassis's policy years.
    """
    def as_float(*columns):
        return lambda table: table.assign(**{c: table[c].astype(float) for c in columns})

    edits = {MORT: as_float("age"), LAPSE: as_float("policy_year")}
    model = _read_edited(tmp_path, as_float("duration_mth", "age_at_entry", "policy_term"),
                         edits=edits)
    committed = _committed()
    try:
        for case in FLOAT_KEYED:
            point_id = _label(committed, *case)
            for report in REPORTS:
                assert frame_mismatches(_point(sec_model, point_id).cells[report](),
                                        _point(model, point_id).cells[report](),
                                        rtol=0, atol=0) == [], (point_id, report)
    finally:
        model.close()


# ---------------------------------------------------------------------------
# T6 -- regeneration


def test_the_committed_sec_inputs_are_what_s_generates():
    """``model_point_table_sec.csv`` is what WP_UK_S and its table generate today.

    Every row and column, the text cells and the eight opening-state columns included: an
    edit to an S row the table copies or derives from, or to an S formula a row's state is
    read from, fails here until ``python tools/gen_sec_points.py WP_UK_SEC`` regenerates
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

    On the twin of the bond variant issued at the valuation date the two coincide, and its
    policies enter as new business at ``t = 0``, paying the single premium there.  The
    worked example's bond valued 60 months after issue is in policy year 6 at attained age
    60 at ``t = 0``, has 720 months to the limiting age, declares at ``t = 11`` and 23,
    policy months 71 and 83, and meets its guarantee date at ``t = 59``, the end of its
    tenth policy year.  The row at 71 declares in month 0, its price stepping by its rate
    there.  The bond variant issued 13 months on has nothing in force and nothing to do
    before ``t = 13``, where it pays its single premium; its frame of 280 months ends where
    its units run out, at its policy month 267; it declares first at ``t = 24`` and its
    guarantee window opens at ``t = 120``, policy month 107, a year before its guarantee
    date at ``t = 132``.  The twins of S's points in force carry 0 in both cumulants, which
    S restarts where its frame opens, so that they reproduce S.  A timing the model does not
    know is refused rather than answered with another count.
    """
    twin = _row(sec_model, "twin", 7, 0)
    assert [twin.duration_mth(t) for t in (0, 1, 266)] == [0, 1, 266]
    assert (twin.t_entry(), twin.pols_if_init(), twin.pols_new_biz(0), twin.pols_if(0)) == (
        0, 0.0, 1.0, 1.0)
    assert twin.premium_pp(0) == 25000.0 and twin.premium_pp(1) == 0.0
    assert (twin.proj_len(), twin.fund_exhaust_mth()) == (267, 267)
    old = _row(sec_model, "twin", 1, 60)
    assert (old.duration_mth(0), old.duration(0), old.policy_year(0), old.age(0)) == (
        60, 5, 6, 60)
    assert (old.proj_len(), old.t_entry(), old.pols_new_biz(0), old.premium_pp(0)) == (
        720, 0, 0.0, 0.0)
    assert old.is_active(719) and not old.is_active(720)
    assert [t for t in range(30) if old.is_declaration_month(t)] == [11, 23]
    assert [t for t in range(720) if old.is_guarantee_date(t)] == [59]
    assert old.pols_if(0) == old.pols_if_init() == old.policy_count()
    for label in _committed().index[(_committed()["row_kind"] == "twin")
                                    & (_committed()["duration_mth"] > 0)]:
        p = _point(sec_model, label)
        assert (p.guar_charge_cum_pp_init(), p.smoothing_account_init()) == (0.0, 0.0)
    declared = _row(sec_model, "derived", 1, 71)
    assert declared.is_declaration_month(0) and declared.declaration_month(0) == 0
    assert declared.unit_price(0) == declared.unit_price_init() * 1.02
    fut = _row(sec_model, "future", 7, -13)
    assert (fut.duration_mth(0), fut.t_entry(), fut.proj_len()) == (-13, 13, 280)
    assert not fut.is_active(12) and fut.is_active(13)
    assert (fut.pols_if_init(), fut.pols_new_biz(13), fut.pols_if(13)) == (0.0, 1.0, 1.0)
    assert [t for t in range(280) if fut.premium_pp(t) > 0.0] == [13]
    assert [t for t in range(60) if fut.is_declaration_month(t)] == [24, 36, 48]
    assert [t for t in range(280) if fut.is_guarantee_date(t)] == [132]
    assert [t for t in range(140) if fut.guarantee_imminent(t) != 1.0] == list(range(120, 132))
    _refused(lambda: old.pols_if_at(0, "BEF_NOTHING"), "invalid timing")


def _guarantee_years(value):
    """The guarantee dates' policy years as ``WP_UK_S``'s ``guarantee_years`` parses its
    column: ``()`` for a blank, else the int of each part of the text split at ``;``, a
    blank part skipped."""
    if pd.isna(value):
        return ()
    return tuple(int(float(s)) for s in str(value).split(";") if str(s).strip())


def test_the_rebased_reads_run_on_the_policy_clock(sec_model):
    """Every read §6.5 rebases is on the policy clock, on every committed point and month.

    ``WP_UK_S`` reads its clock off ``t``, which on the valuation clock is a month since the
    valuation date: its single premium at ``t == 0``, which every bond in force would pay
    again in month 0; its declarations at ``(t + 1) % 12 == 0``, which would put a bond
    valued mid-year's declarations in the wrong months; its declaration month as the policy
    month ``12 x duration(t) + 11``, which the bonus rate passes back as ``t``; and its
    guarantee window at ``12 g - 1 - t``.  On every committed point, at every month of its
    frame: the single premium falls in the issue month alone, ``duration_mth(t) == 0``; a
    declaration falls where ``(duration_mth(t) + 1) % 12 == 0`` and in no other month, and
    the price or the guarantee moves there and nowhere else; ``declaration_month(t)`` is the
    valuation month of the declaration closing ``t``'s policy year, from ``t`` to 11 months
    on; the guarantee date is the declaration of a guarantee year; and the window shuts
    the year before each guarantee date, on the policy clock.  So a policy month passed as
    ``t`` fails here, on every point not issued at the valuation date (R1a).
    """
    for key, label in zip(point_keys(sec_model), sec_model.Data.model_point_table().index):
        p = projection(sec_model, key)
        years = _guarantee_years(p.model_point()["guarantee_dates"])
        for t in range(p.t_entry(), p.proj_len()):
            m = p.duration_mth(t)
            single = p.premium_single_pp() if m == 0 else 0.0
            assert p.premium_pp(t) == p.premium_regular_pp() / 12.0 + single, (label, t)
            assert p.is_declaration_month(t) == ((m + 1) % 12 == 0), (label, t)
            assert p.declaration_month(t) == t + 11 - m % 12, (label, t)
            assert p.duration(p.declaration_month(t)) == p.duration(t), (label, t)
            assert p.is_guarantee_date(t) == (
                p.is_declaration_month(t) and p.policy_year(t) in years), (label, t)
            assert (p.guarantee_imminent(t) != 1.0) == any(
                0 < 12 * g - 1 - m <= 12 for g in years), (label, t)
        assert p.check_declaration_is_annual() is True, label


def test_the_committed_rows_continue_their_s_points(sec_model, s_model):
    """Each committed row in force, or issued later, is its S point from its month on.

    T6 compares a float to 1e-12, which pins a small count only to that much of itself, so
    each committed row is compared with its S point frame by frame and cell by cell, at the
    shipped assumptions (USLIB-SEC-PLAN.md §7.1, *Precised at M3*, item 11): the twins in
    force from S's own months, the derived rows from theirs, and the row issued 13 months
    on from S's issue month, all to 1e-9 relative with no absolute floor but on the
    residuals, every cell but those expense inflation moves (:func:`_continues_s`), which
    the inflation test holds.  The rows read from S under References of their own are S's
    under them, which the test after this one compares.
    """
    table = sec_model.Data.model_point_table()
    s_table = s_model.Data.model_point_table()
    found = []
    for point_id in table.index:
        kind, month = table.at[point_id, "row_kind"], int(table.at[point_id, "source_mth"])
        if kind == "twin" and month == 0:
            continue
        policy = table.at[point_id, "source_policy_id"]
        if (policy, month) in UNDER_REFS:
            continue
        s_point = int(s_table.index[s_table["policy_id"] == policy][0])
        found += [f"point {point_id}: {line}" for line in _continues_s(
            _point(s_model, s_point), _point(sec_model, point_id), month)]
    assert not found, found[:20]


def test_the_committed_rows_under_references_of_their_own_are_s_under_them(sec_model):
    """Each row read from S under References of its own opens with S's state under them,
    and with those References set in both models is S's through its whole frame (K14).

    At S's References each history is what today's References rebuild, so the spec reads
    five rows from S under References of their own (``derived_refs``): the bond variant at
    60 and the 5% bond at 300 under a guarantee charge doubled, the worked example's bond and
    the endowment at 150 under the bonus rule, and the worked example's bond at 156 under a
    smoothing cap of 5%.  Each row's eight state columns are S's under them at its month,
    as the spec's extractors read them, to 1e-12 relative; and with the row's References
    set in both models the row is S's in every month of its frame, in every cell S
    evaluates and the three reports, to 1e-9 relative with no absolute floor but on the
    residuals, but those expense inflation moves (:func:`_continues_s`).  At the shipped
    References the committed model projects each from that history: the K14 test after
    this one holds what each column moves.  Each Reference is set on a model just read (K7).
    """
    assert len(UNDER_REFS) == 5, UNDER_REFS
    for (policy, d), refs in UNDER_REFS.items():
        s_point = int(policy.rsplit("-", 1)[1])
        row = _row(sec_model, "derived", s_point, d)
        sec = mx.read_model(model_path(SEC), name=_name("under_sec"))
        s = mx.read_model(model_path(TWIN), name=_name("under_s"))
        try:
            for model in (sec, s):
                for ref, value in refs.items():
                    setattr(model.Projection, ref, value)
            sp = _point(s, s_point)
            for column, extract in SPEC.state.items():
                want, got = extract(sp, d), row.cells[column]()
                assert got == pytest.approx(want, rel=1e-12, abs=1e-12), (policy, d, column)
            sweep(sp)
            assert _continues_s(sp, _row(sec, "derived", s_point, d), d) == [], (policy, d)
        finally:
            sec.close()
            s.close()


# Each history column (UKLIB-SEC-PLAN.md K14), as (column, the References S reaches its
# history under, the S point and month it is read at, and what month 0 opens with on that
# row, read off the projection, which must be the column).  Each state departs from what
# today's References reach at the same month: the asset share and the charges taken under a
# guarantee charge doubled, on the 5% bond at 300 and the bond variant at 60, the cases
# §6.5 names where a bond reopened without its cumulants parts from S; the withdrawing
# bond's units, the price, the endowment's attaching bonus and the rate under the bonus
# rule; and the payout and the smoothing account under a smoothing cap of 5%.
HISTORIES = [
    ("asset_share_init", CHARGE_SET, (3, 300),
     lambda p: p.asset_share_at(0, _code(p, "BEF_PREM"))),
    ("units_init", RULE, (4, 150), lambda p: p.guar_benefit_open(0) / p.unit_price_init()),
    ("unit_price_init", RULE, (1, 150), lambda p: p.guar_benefit_open(0) / p.units_init()),
    ("attaching_bonus_init", RULE, (5, 150),
     lambda p: p.guar_benefit_open(0) - p.sum_assured()),
    ("smoothed_payout_init", SMOOTH_SET, (1, 156), lambda p: p.smoothed_payout_open(0)),
    ("bonus_rate_init", RULE, (1, 150), lambda p: p.bonus_rate(0)),
    ("guar_charge_cum_pp_init", CHARGE_SET, (7, 60),
     lambda p: p.guar_charge_cum_pp(0) - p.guar_charge_pp(0)),
    ("smoothing_account_init", SMOOTH_SET, (1, 156),
     lambda p: (p.smoothing_account(0) - p.smoothing_cost(0)) / p.pols_if_init()),
]


@pytest.mark.parametrize("column, refs, source, opened", HISTORIES,
                         ids=[c[0] for c in HISTORIES])
def test_each_history_column_is_read_from_the_model_point(s_model, tmp_path, column, refs,
                                                          source, opened):
    """Each history column is the point's own, read, never rebuilt (K14, D6).

    A model that rebuilt a history from today's References, or dropped it, would pass every
    comparison with S at today's References, since S rebuilds it alike.  So each column is
    read on a state S reaches under References of its own (:data:`HISTORIES`), which
    departs from what today's References reach at the same month by more than 1e-6 of
    itself: the committed row read under them (``derived_refs``), or for the units, which no
    committed row departs in, the row built by the generator out of S under the bonus rule,
    beside a copy holding today's value of that column alone.  At today's References month
    0 opens with the column, to the float's rounding (the history's ``opened``), and the
    two rows' reports part; and with the References set in both models the row is S's
    under them through its whole frame, in every cell and the three reports
    (:func:`_continues_s`), which for a committed row the test before this one asserts.
    And the rate declared before the valuation date is where today's rule starts from (D6):
    with the rule on at today's References, the first declaration in the frame is the
    rule's step from the column, and from today's value another.  For the
    cumulants, what they move: the charges taken stop the charge at the cap where today's
    history, or none, would charge on, and the smoothing account runs the column's distance
    from today's in every month, per policy times the count.  Each Reference is set on a
    model just read (K7).
    """
    s_point, d = source
    committed = UNDER_REFS.get((_s_table().at[s_point, "policy_id"], d)) == refs
    s = None if committed else mx.read_model(model_path(TWIN), name=_name("history_s"))
    sec = today = None
    try:
        theirs = SPEC.state[column](_point(s_model, s_point), d)
        if committed:
            table = _committed()
        else:
            for ref, value in refs.items():
                setattr(s.Projection, ref, value)
            spec = dataclasses.replace(SPEC, derived=((s_point, d),), future=(),
                                       derived_refs={})
            table = build_sec_table(spec, s)[0].set_index("point_id")
        label = _label(table, "derived", s_point, d)
        mine = table.at[label, column]
        assert abs(mine - theirs) > 1e-6 * max(abs(mine), abs(theirs)), (column, mine, theirs)
        twin = table.loc[[label]].assign(**{column: theirs})
        twin.index = pd.Index([table.index.max() + 1], name="point_id")
        folder = _sec_inputs(tmp_path, pd.concat([table, twin]))
        today = mx.read_model(folder, name=_name("history_today"))
        p, q = _point(today, label), _point(today, twin.index[0])
        assert opened(p) == pytest.approx(mine, rel=1e-12, abs=1e-12), (column, opened(p))
        assert opened(q) == pytest.approx(theirs, rel=1e-12, abs=1e-12), column
        assert any(frame_mismatches(q.cells[name](), p.cells[name](), rtol=1e-9, atol=0.0)
                   for name in REPORTS), f"{column} moves no report"
        if column == "guar_charge_cum_pp_init":
            first = [next(t for t in range(x.proj_len()) if x.guar_charge_rate(t) == 0.0)
                     for x in (p, q)]
            assert first[0] < first[1], first
        if column == "smoothing_account_init":
            gap = (mine - theirs) * p.pols_if_init()
            assert all(p.smoothing_account(t) - q.smoothing_account(t)
                       == pytest.approx(gap, rel=1e-9) for t in range(p.proj_len()))
        if column == "bonus_rate_init":
            sec = mx.read_model(folder, name=_name("history_rule"))
            for ref, value in RULE_REFS.items():
                setattr(sec.Projection, ref, value)
            declared = [_rule_from(_point(sec, row), rate)
                        for row, rate in ((label, mine), (twin.index[0], theirs))]
            assert _rule_agrees(*declared[0]), declared
            assert _rule_agrees(*declared[1]), declared
            assert declared[0][0] != declared[1][0], declared
            sec.close()
            sec = None
        if committed:
            return
        sec = mx.read_model(folder, name=_name("history_sec"))
        for ref, value in refs.items():
            setattr(sec.Projection, ref, value)
        sp = _point(s, s_point)
        sweep(sp)
        assert _continues_s(sp, _point(sec, label), d) == [], column
    finally:
        for model in (sec, today, s):
            if model is not None:
                model.close()


def _supportable(p, d):
    """The bonus rule's supportable rate at ``p``'s declaration month ``d``, computed here as
    technical-notes.md states the rule, never read from ``bonus_supportable``.

    From what the month opens with, the projected asset share and the guarantee, each the
    close of the month before, or the opening state in the first month on the books; the
    point's fund return and premium; and the References: the asset share grown ``m``
    years, the bond's ``bonus_horizon`` or the endowment's term less the policy year the
    declaration closes, at the return net of the management charge and of the guarantee
    charge, which stops once the charges taken reach ``guar_charge_cap`` of that asset
    share, with each year's premium, paid at the year's start, accumulated at it to the
    horizon; ``guar_fill_target`` of it; and the level rate that grows the guarantee to
    that.
    """
    first = d == p.t_entry()
    opened = p.asset_share_init() if first else p.asset_share(d - 1)
    if first:
        guarantee = (p.units_init() * p.unit_price_init() if p.is_unitised()
                     else p.sum_assured() + p.attaching_bonus_init())
    else:
        guarantee = p.guar_benefit_pp(d - 1)
    taken = p.guar_charge_cum_pp_init() if first else p.guar_charge_cum_pp(d - 1)
    charge = (0.0 if opened > 0.0 and taken >= p.guar_charge_cap * opened
              else p.guar_charge_rate_base)
    year = (p.duration_mth_init() + d) // 12 + 1
    m = int(p.bonus_horizon) if p.is_unitised() else max(1, p.policy_term() - year)
    net = p.fund_return() - p.amc_rate - charge
    projected = opened * (1.0 + net) ** m + sum(
        p.premium_regular_pp() * (1.0 + net) ** k for k in range(1, m + 1))
    if guarantee <= 0.0 or projected <= 0.0:
        return 0.0
    return (p.guar_fill_target * projected / guarantee) ** (1.0 / m) - 1.0


def _rule_from(p, prev):
    """``(the rate p declares first in its frame, the rule's step from prev at it)``: the
    step a share, ``bonus_speed``, of the gap to the supportable rate (:func:`_supportable`,
    computed here), held within ``bonus_change_cap`` and the rate floored at 0."""
    d = p.declaration_month(0)
    step = p.bonus_speed * (_supportable(p, d) - prev)
    step = max(-p.bonus_change_cap, min(p.bonus_change_cap, step))
    return p.bonus_rate(d), max(0.0, prev + step)


def _rule_agrees(got, want):
    """Whether a declared rate is the rule's computed here: to 1e-12 relative, the sum of
    premiums and the power taken here in their own order."""
    return got == pytest.approx(want, rel=1e-12, abs=0.0)


# Rows on which D6's declarations are asserted under the rule, at today's References, as
# ((row_kind, S point, month), the first declaration's month): the worked example's bond
# valued in a declaration month, 71, its declaration month 0's own event, and the down
# scenario valued mid-year, 68, its year-end declaration at t = 3, whose steps the change
# cap clamps and the floor holds at 0; and two whose steps neither does, so that the rate
# declared moves with the supportable rate itself: the endowment valued in its
# declaration month, 11, and the 5% bond in force at 60, its first declaration at t = 11.
DECLARED = ((("derived", 1, 71), 0), (("derived", 2, 68), 3), (("derived", 5, 11), 0),
            (("twin", 3, 60), 11))


def test_each_declaration_in_the_frame_is_made_at_today_s_references():
    """A declaration at or after the valuation date is the projection's own event (D6).

    With the bonus rule on, set on the committed model just read, every declaration in the
    frame is the rule's at today's References, from this model's own asset share and
    guarantee, and the first starts from ``bonus_rate_init()``, the rate declared before
    the valuation date.  The rule is computed here from the asset share and the guarantee
    the declaration month opens with and the References (:func:`_supportable`), never read
    from the model's own ``bonus_supportable``, so a declaration that read another month's
    asset share, or a rule that drifted from the notes, parts here.  On the row valued in a declaration month (:data:`DECLARED`) that
    declaration is month 0's own event: its rule reads the opening state, the asset share
    the month opens with being ``asset_share_init()`` and the guarantee the units at the
    opening price, and the price steps by it at ``t = 0``.  On the row valued mid-year the
    year-end declaration, at ``t = 3``, is the rule's from the opening rate, and every month
    of the year reads it.  Each differs from the rate the row opens with.  Their steps are
    clamped, by the change cap and the floor, so two more rows take steps no clamp holds,
    the endowment on its declaration and the 5% bond in force: there the rate declared
    moves with the supportable rate, and the model's ``bonus_supportable`` is held to the
    rule computed here on every row.
    """
    model = mx.read_model(model_path(SEC), name=_name("declared"))
    try:
        for ref, value in RULE_REFS.items():
            setattr(model.Projection, ref, value)
        free = 0
        for case, d0 in DECLARED:
            p = _row(model, *case)
            assert p.declaration_month(0) == d0 and p.is_declaration_month(d0), case
            init = p.bonus_rate_init()
            got, want = _rule_from(p, init)
            assert _rule_agrees(got, want) and got != init, (case, got, want, init)
            assert _rule_agrees(p.bonus_supportable(d0), _supportable(p, d0)), case
            assert [p.bonus_rate(t) for t in range(d0 + 1)] == [got] * (d0 + 1), case
            raw = p.bonus_speed * (_supportable(p, d0) - init)
            free += abs(raw) < p.bonus_change_cap and init + raw > 0.0
            if p.is_unitised():
                opened = p.unit_price_init() if d0 == 0 else p.unit_price(d0 - 1)
                assert p.unit_price(d0) == opened * (1.0 + got), case
            else:
                opened = (p.sum_assured() + p.attaching_bonus_init() if d0 == 0
                          else p.guar_benefit_pp(d0 - 1))
                assert p.guar_benefit_pp(d0) == opened * (1.0 + got), case
        assert free == 2, free
        p = _row(model, *DECLARED[0][0])
        assert p.asset_share_at(0, _code(p, "BEF_PREM")) == p.asset_share_init()
        assert p.guar_benefit_open(0) == p.units_init() * p.unit_price_init()
    finally:
        model.close()


def test_under_the_rule_a_first_declaration_s_carries_departs_by_d6(spliced):
    """Where S's first frame year keeps its column, this model declares by the rule (D6).

    ``WP_UK_S``'s first projected year keeps its column under the rule; this model makes
    every declaration in its frame by the rule at today's References.  So under the rule set
    the twin of S's worked example in force at 60 parts from S at its first declaration,
    policy month 71, ``t = 11``: S keeps the 2% it carries, and this model declares the
    rule's step from it, computed here (:func:`_supportable`), which the change cap clamps,
    so the model's ``bonus_supportable`` is held to that rule too.  Before it the row is S's
    in every cell and report but the bonus rate, which every month of the year reads from
    that declaration (T2, :func:`_carried_cut`); the price steps apart there.  The departure
    ``model-sec.md`` records.  At the shipped References the rule is off, and the committed
    twins are S's.
    """
    s, sec = spliced["rule"]
    sp = _point(s, 1)
    assert _carried_cut(sp, 60) == 71
    key = _row_key(sec, "twin", 1, 60)
    p = projection(sec, key)
    try:
        assert sp.bonus_rate(71) == sp.bonus_rate_init() == p.bonus_rate_init() == 0.02
        got, want = _rule_from(p, p.bonus_rate_init())
        assert _rule_agrees(got, want) and got != 0.02, (got, want)
        assert _rule_agrees(p.bonus_supportable(11), _supportable(p, 11))
        assert p.unit_price(10) == sp.unit_price(70)
        assert p.unit_price(11) == sp.unit_price(70) * (1.0 + got) != sp.unit_price(71)
    finally:
        _release(sec, key)


def test_the_bonus_rate_read_is_bounded_by_the_frame(spliced):
    """With the bonus rule on, a frame ending mid-year reads no declaration past it.

    Each month's rate is the one declared at the end of its policy year, the anniversary
    read R2 admits up to 11 months ahead.  Where a forced encashment ends the frame
    mid-year, the year's declaration falls past the frame: ``WP_UK_S`` reads it there, from
    an asset share and a payout it projects past its own last month, which a compiled
    cache sized to the frame does not hold.  This model reads the rate declared before the
    year instead, the recorded departure (``bonus_rate``'s docstring; UKLIB-SEC-PLAN.md
    §6.5): on the withdrawing variant under the rule, restated at its month 302, whose units
    run out at policy month 400, the months of its 34th policy year, from policy month 396
    to the frame's last, hold the rate declared at 395, where S's own read the declaration
    of policy month 407, past its frame, which differs.  And at the bound's edge: the
    variant withdrawing 6%, whose units run out at policy month 287, restated at 280, ends
    its frame the month before its year's declaration, 287, which it does not read.  No
    other cell moves (T2, :func:`_departure`), and no read of the rate lies past the frame.
    """
    s, sec = spliced["rule"]
    for s_point, month, end, first, after in ((12, 302, 400, 396, 407),
                                               (16, 280, 287, 276, 287)):
        sp = _point(s, s_point)
        gone = _departure(sp, month)
        assert gone is not None and sp.proj_len() == end, (s_point, gone, sp.proj_len())
        assert gone[0] == first and sp.declaration_month(first) == after >= end, s_point
        key = _row_key(sec, "derived", s_point, month)
        p = projection(sec, key)
        try:
            assert p.proj_len() == end - month
            months = range(max(first - month, 0), p.proj_len())
            assert [p.bonus_rate(t) for t in months] == [gone[1]] * len(months), s_point
            assert all(sp.bonus_rate(t + month) != gone[1] for t in months), s_point
            if s_point == 16:
                assert p.declaration_month(0) == p.proj_len()
            p.result_payout()
            assert max(p.cells["bonus_rate"].keys()) < p.proj_len(), s_point
        finally:
            _release(sec, key)


def test_the_exhaustion_search_s_never_is_a_month_past_cover(sec_model, s_model):
    """Where the units never run out, ``fund_exhaust_mth()`` is a month past cover.

    ``WP_UK_S``'s search returns 0 for "never", safe there because its month 0 is a bond's
    issue month, which the single premium funds.  On the valuation clock a policy month of 0
    is a real month, and month 0 may be any month of a bond's life, including the one its
    last units are withdrawn in; so this model's "never" is ``cover_end_mth() + 1``, which no
    month of cover reaches.  On every twin, where S's search finds no month this model's
    returns that, and where S's finds one, the bond variant's 267, this model's is the same
    month; and on every committed point the frame ends at the earlier of cover's end and the
    month the units run out.
    """
    table = sec_model.Data.model_point_table()
    for key, label in zip(point_keys(sec_model), table.index):
        p = projection(sec_model, key)
        exhaust, end = p.fund_exhaust_mth(), p.cover_end_mth()
        assert p.proj_len() == min(end, exhaust) - p.duration_mth_init(), label
        assert p.is_forced_encashment() == (exhaust < end), label
        if table.at[label, "row_kind"] == "twin":
            theirs = _point(s_model, label).fund_exhaust_mth()
            assert exhaust == (end + 1 if theirs == 0 else theirs), (label, theirs)
    assert _row(sec_model, "twin", 7, 0).fund_exhaust_mth() == 267


def test_expense_inflation_runs_on_the_valuation_clock(sec_model, s_model):
    """Expense inflation steps on the valuation date's anniversaries, for every point (D7).

    ``WP_UK_S`` inflates the maintenance expense from issue, ``(1 + pi)^duration(t)``, which
    on a policy in force would inflate today's expense by the years the policy has already
    run.  Here the factor is ``(1 + pi)^(t // 12)`` on every committed point, the same for a
    point issued at the valuation date as for one in force 240 months, so the block's
    expenses are in valuation-date pounds; and the expense is the twelfth of
    ``expense_maint`` times it, per policy in force.  On the in-force twins S's expense in
    month ``t + d`` is this model's in month ``t`` times the inflation of the policy years
    before the valuation date, ``1.03^(d // 12)``, and on the twins issued at the valuation
    date the two are the same, bit for bit.
    """
    for key, label in zip(point_keys(sec_model), sec_model.Data.model_point_table().index):
        p = projection(sec_model, key)
        for t in range(p.proj_len()):
            assert p.inflation_factor(t) == (1.0 + INFLATION) ** (t // 12), (label, t)
            assert p.expenses(t) == (p.expense_maint / 12.0 * p.inflation_factor(t)
                                     * p.pols_if(t)), (label, t)
    for s_point, d in ((1, 60), (6, 240)):
        p, sp = _row(sec_model, "twin", s_point, d), _point(s_model, s_point)
        for t in range(0, p.proj_len(), 7):
            assert sp.inflation_factor(t + d) == (1.0 + INFLATION) ** ((t + d) // 12)
            assert sp.expenses(t + d) == pytest.approx(
                p.expenses(t) * (1.0 + INFLATION) ** ((t + d) // 12)
                / (1.0 + INFLATION) ** (t // 12), rel=1e-12), (s_point, t)
    for s_point in (5, 7):
        p, sp = _row(sec_model, "twin", s_point, 0), _point(s_model, s_point)
        assert [p.expenses(t) for t in range(p.proj_len())] == [
            sp.expenses(t) for t in range(sp.proj_len())]


# ---------------------------------------------------------------------------
# The cap on mortality
#
# mort_rate caps the annual rate at 1, the bound second, as WP_UK_S's does: min(q, 1.0).  At
# the shipped mort_be_factor of 0.6 no attained age reaches the cap, so it is held at a
# factor of 2, under which the men's rate passes 1 from attained age 106: on the worked
# example's bond, issued at 55, from policy month 612.
CAP_FACTOR = 2.0
CAP_MONTH, CAP_AGE = 612, 106


def test_an_annual_mortality_past_1_is_capped_in_both_models(tmp_path):
    """Where the annual mortality rate passes 1, both models' rate is 1.

    Under a ``mort_be_factor`` of 2, set with :data:`SPLICED_REFS` in both models, the
    worked example's bond's rate reaches 1 at attained age 106, policy month 612, and stays
    there to the end of the frame, where its uncapped rate passes 1: the capped rate and the
    monthly rate, ``1 - (1 - q)^(1/12)``, are 1.0 in every one of those months, the float,
    not the int 1, which compares equal to it, and S's are floats below 1 in every month
    before.  So every policy in force at the start of the first capped month dies in it,
    none is in force after it, and every report holds finite floats alone.

    Three rows built from S by the generator under the factor: the twin in force at 60,
    restated in force in the month before the cap, opened with S's count and state there,
    each compared with S in every cell, the capped months included, as T2 compares them, to
    1e-9 relative with no absolute floor but for the residuals; and restated five months
    into the capped year, opened with S's state there and one policy, since S's count there
    is 0.  On each, the capped rates are 1.0 from its first capped month, every policy in
    force there dies in it, and the count is 0.0 after it.  This is T2's binding mortality
    cap (UKLIB-SEC-PLAN.md §6.5).
    """
    refs = {**SPLICED_REFS, "mort_be_factor": CAP_FACTOR}
    s = mx.read_model(model_path(TWIN), name=_name("capped_s"))
    sec = None
    try:
        for ref, value in refs.items():
            setattr(s.Projection, ref, value)
        sp = _point(s, 1)
        end = sp.proj_len()
        first = next(t for t in range(sp.proj_start(), end) if sp.mort_rate(t) == 1.0)
        assert (first, sp.age(first)) == (CAP_MONTH, CAP_AGE)
        after = range(CAP_MONTH, end)
        for name in ("mort_rate", "mort_rate_mth"):
            assert all(type(sp.cells[name](t)) is float and sp.cells[name](t) < 1.0
                       for t in range(sp.proj_start(), CAP_MONTH)), name
            assert [(type(sp.cells[name](t)), sp.cells[name](t)) for t in after] == [
                (float, 1.0)] * len(after), name
        _sweep_s(sp)
        assert sp.pols_if(CAP_MONTH) > 0.0
        assert sp.pols_death(CAP_MONTH) == sp.pols_if(CAP_MONTH)
        assert [sp.pols_if(t) for t in range(CAP_MONTH + 1, end)] == [0.0] * (len(after) - 1)
        spec = dataclasses.replace(SPEC, derived=((1, CAP_MONTH - 1), (1, CAP_MONTH + 5)),
                                   future=(), derived_refs={})
        rows, _ = build_sec_table(spec, s)
        emptied = (rows["row_kind"] == "derived") & (rows["policy_count"] == 0.0)
        assert emptied.sum() == 1
        rows.loc[emptied, "policy_count"] = 1.0
        sec = mx.read_model(_sec_inputs(tmp_path, rows), name=_name("capped"))
        for ref, value in refs.items():
            setattr(sec.Projection, ref, value)
        cases = ((("twin", 1, 60), CAP_MONTH - 60, SPLICE_EXEMPT),
                 (("derived", 1, CAP_MONTH - 1), 1, SPLICE_EXEMPT),
                 (("derived", 1, CAP_MONTH + 5), 0, None))
        for case, first, exempt in cases:
            p = _row(sec, *case)
            if exempt is not None:
                assert _continues_s(sp, p, case[2]) == [], case
            capped = range(first, p.proj_len())
            later = range(first + 1, p.proj_len())
            for name in ("mort_rate", "mort_rate_mth"):
                assert [(type(p.cells[name](t)), p.cells[name](t)) for t in capped] == [
                    (float, 1.0)] * len(capped), (case, name)
            assert p.pols_if(first) > 0.0 and p.pols_death(first) == p.pols_if(first)
            assert [p.pols_if(t) for t in later] == [0.0] * len(later), case
            for name in REPORTS:
                frame = p.cells[name]()
                assert (frame.dtypes == "float64").all(), (case, name)
                assert np.isfinite(frame.to_numpy()).all(), (case, name)
    finally:
        if sec is not None:
            sec.close()
        s.close()


def test_a_nan_that_reaches_the_mortality_cap_stays_nan():
    """A NaN that reaches the cap ``min(q, 1.0)`` stays NaN, and is not read as death.

    ``min`` keeps its first argument unless a later one compares smaller, in modelx and
    compiled alike, and no comparison with NaN holds, so with its bound first,
    ``min(1.0, q)``, the cap would turn a NaN into certain death.  It is written with its
    bound second, as ``WP_UK_S`` writes it: ``mort_be_factor`` is set to NaN on a model
    read for the test, and the rate, the monthly rate and the mortality charge, which no
    floor reads before it, must give the float NaN; the asset share, whose floor would read
    a NaN as an exhausted share, refuses it.  The cells are called on their own, without the
    frame: ``proj_len()`` refuses the Reference at NaN before a report reaches the cap (the
    domain test).  The surrender rate's bound keeps ``WP_UK_S``'s order, the bound first,
    and is no cap on a mortality rate; ``Data`` and ``proj_len()`` hold what it reads to
    domains no NaN is in.
    """
    model = mx.read_model(model_path(SEC), name=_name("nan"))
    try:
        model.Projection.mort_be_factor = float("nan")
        p = _row(model, "twin", 1, 60)
        lost = [f"{name}(0) = {value!r}" for name in ("mort_rate", "mort_rate_mth",
                                                      "mort_charge_pp")
                for value in [p.cells[name](0)]
                if not (type(value) is float and math.isnan(value))]
        assert not lost, f"the cap loses a NaN mort_be_factor: {lost}"
        _refused(lambda: p.asset_share(0), "point_id 1: the asset share of month 0 before "
                                           "its floor, asset_share_at(0, 'AFT_MC'), is nan")
    finally:
        model.close()


def test_no_check_passes_a_residual_that_is_not_a_number():
    """No check passes a residual that is NaN (§7.1).

    A check is ``abs(resid) <= tolerance`` over the frame, and no comparison with NaN
    holds, so a NaN residual would fail it, as ``WP_UK_S``'s does (USLIB-SEC-PLAN.md §7.1,
    *Precised at M3*, item 11); and the frame comes first.  With ``mort_be_factor`` NaN, set
    on a model read for the test before it computes anything, the mortality rates and so
    the roll-forward's residual are NaN, and each check, asking ``proj_len()`` for the frame,
    is refused the Reference, by name, before it compares one.  So no check passes; and on
    the shipped References each is the bool True.
    """
    for factor, closes in ((float("nan"), False), (0.6, True)):
        model = mx.read_model(model_path(SEC), name=_name("nan_check"))
        try:
            model.Projection.mort_be_factor = factor
            p = _row(model, "twin", 7, 0)
            assert math.isnan(p.mort_rate_mth(5)) != closes
            for check in ("check_pols_roll_fwd", "check_asset_share_roll_fwd"):
                if closes:
                    assert p.cells[check]() is True, check
                else:
                    _refused(p.cells[check], "point_id 7: mort_be_factor must be a finite "
                                             "number, 0 or more, not nan")
        finally:
            model.close()


@pytest.mark.parametrize("check, resid", [
    ("check_pols_roll_fwd", "check_pols_roll_fwd_resid"),
    ("check_asset_share_roll_fwd", "check_asset_share_roll_fwd_resid")])
def test_a_check_fails_a_residual_that_is_not_a_number(sec_model, check, resid):
    """Each check returns False where its residual is NaN (§7.1, item 11).

    A check is ``abs(resid) <= tolerance`` over the frame, which no NaN passes, as
    ``WP_UK_S``'s are; but no input the frame accepts gives a NaN residual any more, so the
    residual's formula is replaced, on a model read for the test, by one that returns NaN
    in every month.  Then the check is the bool False on every committed point, where with
    its own formula it is True.  A check that asked whether any residual was past its
    tolerance would pass NaN.
    """
    model = mx.read_model(model_path(SEC), name=_name("nan_resid"))
    try:
        model.Projection.cells[resid].formula = lambda t: float("nan")
        for key in point_keys(model):
            p, shipped = projection(model, key), projection(sec_model, key)
            assert math.isnan(p.cells[resid](0)), key
            assert shipped.cells[check]() is True and p.cells[check]() is False, key
    finally:
        model.close()


def _outside_cover_faults(p, where):
    """Where ``p``, an ItemSpace that has evaluated nothing, departs from OUTSIDE_COVER.

    Every cell of :data:`OUTSIDE_COVER`, ``pols_if_at`` and ``asset_share_at`` at each
    timing, and ``claim_pp``, ``smoothing_cost_pp`` and ``claims`` at each kind, the
    claims' total among them, in every
    month before issue and in the first month past cover, ``cover_end_mth()`` on the
    valuation clock, against :data:`OUTSIDE_COVER`; then whether any of
    :data:`IN_COVER_ONLY` was evaluated on the way at a month outside cover, which only a
    fresh ItemSpace can say: the frame's exhaustion search projects the months in cover,
    where they are read.  A cell that raises is reported as a fault too, so the scan goes
    on.
    """
    faults = []
    outside = [*range(p.t_entry()), p.cover_end_mth() - p.duration_mth_init()]
    for t in outside:
        calls = [(name, (t,), want) for name, want in OUTSIDE_COVER.items()]
        calls += [("pols_if_at", (t, _code(p, timing)), 0.0) for timing in TIMINGS]
        calls += [("asset_share_at", (t, _code(p, timing)), 0.0) for timing in AS_TIMINGS]
        calls += [(name, (t, _code(p, kind)), 0.0) for kind in CLAIM_KINDS
                  for name in ("claim_pp", "smoothing_cost_pp")]
        calls += [("claims", (t, _code(p, kind)), 0.0) for kind in (*KINDS, "ALL")]
        for name, args, want in calls:
            try:
                got = p.cells[name](*args)
            except Exception as err:        # reported, so the scan goes on
                faults.append(f"{where}: {name}{args} raised {_raised(err)}")
                continue
            if got != want or type(got) is not type(want):
                faults.append(f"{where}: {name}{args} = {got!r}, not {want!r}")
    read = {name: sorted(t for t in p.cells[name].keys() if not 0 <= p.duration_mth(t) <
                         p.cover_end_mth()) for name in IN_COVER_ONLY}
    read = {name: months for name, months in read.items() if months}
    if read:
        faults.append(f"{where}: evaluated outside cover: {read}")
    return faults


def test_every_guarded_cell_holds_its_outside_cover_value(spliced):
    """Outside cover each cell holds :data:`OUTSIDE_COVER`'s value, and reads no rate.

    On every committed point, in every month before issue and in the first month past
    cover, on a model that evaluates nothing else.  So afterwards none of
    :data:`IN_COVER_ONLY` may hold a value at all: ``is_active``'s docstring promises that
    outside cover every balance, count, flow and charge is 0, every flag False, and no
    table is read at a policy year or an attained age the policy does not have.

    The committed table's one point issued after the valuation date is the bond variant,
    so the same scan runs on the splice's future rows, the core's or, with
    ``UKLIB_SEC_FULL=1``, all of them: the endowment and the variants among them.  Each
    row is made afresh first and released after.

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
    futures = _selected(FUTURES, CORE_FUTURES)
    for s_point, k, refs in futures:
        sec = spliced[refs][1]
        key = _row_key(sec, "future", s_point, -k)
        if key in sec.Projection.itemspaces:
            _release(sec, key)
        try:
            faults += _outside_cover_faults(projection(sec, key),
                                            _case_id("future", s_point, -k, refs))
        finally:
            _release(sec, key)
    assert futures and not faults, (
        f"{len(faults)} faults outside cover, first:\n  " + "\n  ".join(faults[:20]))


def test_the_points_sum_row_by_row_into_a_block(spliced):
    """Row ``t`` is the same month on every point, so a block is its frames summed (D3).

    The bond variant's twin, issued at the valuation date, the variant restated at its
    month 266, its last, and the variant issued a month on, summed as ``run_sec.py --block``
    sums them, are indexed 0..267 and equal S's frame added to itself moved 266 months
    earlier and a month later.  A model whose frames sat on the policy clock would fail it.
    """
    s, sec = spliced["main"]
    cases = (("derived", 7, 266, "main"), ("future", 7, -1, "main"))
    keys = [_row_key(sec, *case[:3]) for case in cases if SEC_FULL or case in CORE_GRID]
    assert len(keys) == 2, "the block's rows are the core's"
    twin = _row_key(sec, "twin", 7, 0)
    try:
        frames = [projection(sec, key).result_cf() for key in (twin, *keys)]
    finally:
        for key in (twin, *keys):
            _release(sec, key)
    block = pd.concat(frames).groupby(level="t").sum()
    sdf = _point(s, 7).result_cf()
    expected = pd.concat([sdf, sdf.set_axis(sdf.index - 266).loc[0:],
                          sdf.set_axis(sdf.index + 1)]).groupby(level=0).sum()
    assert list(block.index) == list(range(268))
    assert frame_mismatches(expected, block) == []


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
    in the three reports, to 1e-12, and ``run_sec.py``, run beside that extract, prints the
    point without saying where it came from.  On every shipped row ``source_mth`` equals
    ``duration_mth``, so a formula that read the one for the other would pass every test
    that leaves ``duration_mth`` as generated.  And a refusal names the extract's label.

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
            for report in REPORTS:
                assert frame_mismatches(base.cells[report](), mine.cells[report](),
                                        rtol=1e-12, atol=1e-12) == [], (key, report)
            _release(model, key)
    finally:
        model.close()
    if grid == "full":
        return
    runner = folder.parent / "run_sec.py"
    shutil.copy(model_path(SEC).parent / "run_sec.py", runner)
    committed = _committed()
    label = EXTRACT_LABELS[list(committed.index).index(_label(committed, "derived", 4, 402))]
    out = _run_sec(runner, str(label))
    row = _row(sec_model, "derived", 4, 402)
    assert out.splitlines()[:3] == [
        f"model point {label}: WP-000004-M402 - UWP_bond M55, single premium 25,000, "
        f"withdrawals 5.0% a year, fund return +5.0% (life_net), bonus 2.00%",
        f"at the valuation date: in force 402 months: policy year 34, attained age 88, "
        f"{row.pols_if(0):.6f} in force, asset share {row.asset_share_init():,.2f}",
        "proj_len = 1 months from the valuation date (t = 0..0); its units run out at "
        "policy month 403, a forced encashment"]
    last = EXTRACT_LABELS[list(committed.index).index(_label(committed, "derived", 1, 779))]
    moved = _set("duration_mth", [last], 780)(extract)
    model = mx.read_model(_sec_inputs(tmp_path / "moved", moved), name=_name("moved"))
    try:
        _refused(_point(model, last).result_cf,
                 f"point_id {last}: duration_mth 780 is at or past the end of cover, policy "
                 f"month 780")
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
            f"{p.age(0)}, {p.pols_if(0):.6f} in force, asset share "
            f"{p.asset_share_init():,.2f}")


def test_run_sec_prints_a_point_and_the_block(sec_model):
    """The runner prints one point, saying where it came from, and the block (D8).

    Each mode in an interpreter of its own, as a user runs it, with exit code 0 and ASCII
    output, so that it prints on a Windows console under any code page.  The numbers are
    the model's.  The worked example's bond, the runner's default, with its lines at the
    valuation date, each asserted whole, so that a longer number cannot pass for the one
    asserted, and its first twelve rows of cash flows and counts.  The endowment in force
    at 240, restated in force at S's month 299 at its maturity, and the bond variant to be
    issued 13 months on: each with the two lines that say where its row came from and where
    it stands, which only the committed table's generator columns can say.  And the block:
    a line for each committed point, in table order, its first twelve rows, which must be
    the committed points' frames summed row by row, as this test sums them, and those
    frames summed into projection years, each year's count the one in force in its first
    month.  Nothing else runs the runner on the committed table.
    """
    runner = model_path(SEC).parent / "run_sec.py"
    out = _run_sec(runner)
    first = _row(sec_model, "twin", 1, 60)
    assert out.splitlines()[:3] == [
        "model point 1: WP-000001 (S's WP-000001) - UWP_bond M55, single premium 25,000, "
        "withdrawals 0.0% a year, fund return +7.0% (life_net), bonus 2.00%",
        f"at the valuation date: in force 60 months: policy year 6, attained age 60, "
        f"{first.pols_if(0):.6f} in force, asset share 30,000.00",
        "proj_len = 720 months from the valuation date (t = 0..719); cover ends at policy "
        "month 780"]
    assert first.result_cf().head(12).round(2).to_string() in out
    assert first.result_pols().head(12).round(6).to_string() in out
    matured = _row(sec_model, "derived", 5, 299)
    for point_id, lines in (
            ("6", ["model point 6: WP-000006 (S's WP-000006) - CWP_endowment M35, premium "
                   "720 a year for 25 years, sum assured 20,000, fund return +5.0% "
                   "(pension_gross), bonus 1.50%",
                   "at the valuation date: in force 240 months: policy year 21, attained "
                   f"age 55, {_row(sec_model, 'twin', 6, 240).pols_if(0):.6f} in force, "
                   "asset share 24,000.00"]),
            ("16", ["model point 16: WP-000005-M299 (S's WP-000005 at its month 299) - "
                    "CWP_endowment M35, premium 720 a year for 25 years, sum assured 20,000, "
                    "fund return +5.0% (life_net), bonus 1.50%",
                    f"at the valuation date: in force 299 months: policy year 25, attained "
                    f"age 59, {matured.pols_if(0):.6f} in force, asset share "
                    f"{matured.asset_share_init():,.2f}"]),
            ("19", ["model point 19: WP-000007-F13 (S's WP-000007, issued 13 months on) - "
                    "UWP_bond M55, single premium 25,000, withdrawals 5.0% a year, fund "
                    "return -15.0% (life_net), bonus 1.00%",
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
    frames = [p.result_cf().drop(columns="asset_share") for p in points]
    block = pd.concat(frames).groupby(level="t").sum()
    assert block.head(12).round(2).to_string() in out
    years = pd.Index(block.index // 12 + 1, name="proj_year")
    annual = block.drop(columns=["pols_if"]).groupby(years).sum()
    annual.insert(0, "pols_if", block["pols_if"].groupby(years).first())
    assert annual.head(12).round(2).to_string() in out


# run_sec.py run as though it sat at /m/products/with_profits, in a products/ folder whose
# parent carries no build tool: the source compiled under that name, so that its own
# __file__ is it.
SHALLOW_RUN = """\
import sys
source = open(sys.argv[1], encoding="utf-8").read()
where = "/m/products/with_profits/run_sec.py"
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
    frames = [projection(sec_model, key).result_cf().drop(columns="asset_share")
              for key in point_keys(sec_model)]
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
    as ``source_refs`` records them, point 20's ``under guar_charge_rate_base 0.002``, and
    no other row's line names any.  ``origin`` is read from the runner, which runs the model
    when imported, and run here on every row of the table the runner reads.
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
    assert space["origin"](20) == (
        " (S's WP-000007 at its month 60, under guar_charge_rate_base 0.002)")


def _defaulted(model_name):
    """The cells of ``model_name``'s Projection with a parameter that has a default, sorted,
    read from its source, as the C step's build reads it."""
    source = (model_path(model_name) / "Projection" / "__init__.py").read_text(
        encoding="utf-8")
    return sorted(node.name for node in ast.parse(source).body
                  if isinstance(node, ast.FunctionDef)
                  and (node.args.defaults or any(node.args.kw_defaults)))


def test_no_cell_takes_a_default():
    """No cell has a defaulted parameter, ``WP_UK_S``'s total among them (R12).

    A compiled model declares a defaulted parameter in its ``.pxd`` as ``long long
    life=*``, which the typing guard would read as a parameter of that name, and mx2cy
    traces a ``None`` default as ``None``.  ``WP_UK_S``'s one, ``claims(t, kind=None)``,
    the total of its three kinds, is ``claims(t, ALL)`` here, the compensated total
    UKLIB-SEC-PLAN.md §6.5's C list names (R12), and running in force and compiling add
    none.
    """
    assert _defaulted(TWIN) == ["claims"]
    assert _defaulted(SEC) == []


# The texts a computed cell may hold, beside a column's name read off the model point: at
# stage "E" the timings and the kinds, and the chassis codes, which the C step made int
# References (R9; §6.5's C list, "the codes"); at stage "EC", none, so that a formula that
# compared a text again would be found.
CODES = frozenset()

# The cells the static check leaves be, each a reporting cell that stays Python (R17): the
# three reports, which build DataFrames, and the three label accessors, which test their
# column's text against a tuple of its codes.  At stage "E" it left the C step the five
# checks that built a generator, the guarantee dates' tuple and the two cells that read
# it, the two readers of the assumption tables and the claims total, each an item of
# UKLIB-SEC-PLAN.md §6.5's C list, which the C step made C.  Each is needed: the test takes
# each away in turn and the scan finds its cell.
STATIC_EXEMPT = frozenset({"result_cf", "result_payout", "result_pols", "chassis", "sex",
                           "tax_basis"})


def _static_findings(exempt):
    """What the C step's static check finds in the Projection source, ``exempt`` aside.

    A tuple, a list, a set, a dict, a comprehension, a generator, an f-string or a lambda,
    a text other than a code (:data:`CODES`) or a column read off ``model_point()``, each
    outside a ``raise``; and a call of a cell that returns a tuple, whose membership test or
    loop no node of the caller shows, as M7's check now flags.  A table read's index,
    ``data.mort_table_array()[mort_schedule(), x]``, is a tuple C5 admits, and so is it
    here.  ``(cells read, findings)``, each finding led by its cell's name.
    """
    source = (model_path(SEC) / "Projection" / "__init__.py").read_text(encoding="utf-8")
    built = (ast.Tuple, ast.List, ast.Set, ast.Dict, ast.GeneratorExp, ast.ListComp,
             ast.SetComp, ast.DictComp, ast.JoinedStr, ast.Lambda)
    cells = [node for node in ast.parse(source).body if isinstance(node, ast.FunctionDef)]
    tuples = {node.name for node in cells for r in ast.walk(node)
              if isinstance(r, ast.Return) and (
                  isinstance(r.value, ast.Tuple)
                  or (isinstance(r.value, ast.Call)
                      and getattr(r.value.func, "id", None) == "tuple"))}
    found = []
    for node in cells:
        if node.name in exempt:
            continue
        raises = {id(n) for r in ast.walk(node) if isinstance(r, ast.Raise)
                  for n in ast.walk(r)}
        columns = {id(n) for s in ast.walk(node)
                   if isinstance(s, ast.Subscript) and isinstance(s.value, ast.Call)
                   and getattr(s.value.func, "id", None) == "model_point"
                   for n in ast.walk(s.slice)}
        indices = {id(s.slice) for s in ast.walk(node)
                   if isinstance(s, ast.Subscript) and isinstance(s.slice, ast.Tuple)}
        body = node.body[1:] if ast.get_docstring(node) is not None else node.body
        for inner in (n for statement in body for n in ast.walk(statement)):
            if id(inner) in raises or id(inner) in indices:
                continue
            if isinstance(inner, built):
                found.append(f"{node.name}: {type(inner).__name__} at line {inner.lineno}")
            elif (isinstance(inner, ast.Constant) and isinstance(inner.value, str)
                  and inner.value not in CODES and id(inner) not in columns):
                found.append(f"{node.name}: the text {inner.value!r} at line "
                             f"{inner.lineno}")
            elif (isinstance(inner, ast.Call) and getattr(inner.func, "id", None) in tuples
                  and node.name not in tuples):
                found.append(f"{node.name}: a call of {inner.func.id}, a tuple, at line "
                             f"{inner.lineno}")
    return {node.name for node in cells}, found


def test_no_computed_cell_builds_a_python_object(sec_model):
    """No computed cell builds a tuple, a text or a generator but to raise (§6.5, *C*).

    A compiled cell holds no Python object (C3, C5), and the C step turned ``WP_UK_S``'s
    own into the C forms UKLIB-SEC-PLAN.md §6.5 lists, so no ``Projection`` cell but the
    reporting cells of :data:`STATIC_EXEMPT` holds a tuple, a list, a set, a dict, a
    comprehension, a generator or an f-string, or a text, a timing, a kind or a chassis
    among them (:data:`CODES`, none at stage ``"EC"``), but the name of a column it reads
    off ``model_point()`` or inside a ``raise`` statement, nor calls a cell that returns a
    tuple, read from the
    source as the build reads it (:func:`_static_findings`; *Record — M11*, and M7's
    check), so that a Python object an edit puts back is found here, in modelx, in seconds.
    ``try`` is allowed: a power that leaves the floats raises Python's ``OverflowError``,
    which the cell names, in either engine.  Every cell of the Space is read, and every
    exemption is a cell of it and needed: with any one exemption taken away, the scan finds
    that cell, so that no exemption is inert, as one was under pandas 3 at M7, where a text
    column reads as ``str``.
    """
    read, found = _static_findings(STATIC_EXEMPT)
    assert read == set(sec_model.Projection.cells)
    assert STATIC_EXEMPT <= read
    assert not found, found
    inert = [name for name in sorted(STATIC_EXEMPT)
             if not any(f.startswith(f"{name}: ")
                        for f in _static_findings(STATIC_EXEMPT - {name})[1])]
    assert not inert, f"exemptions the scan needs none of: {inert}"


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
    outside the parentheses and quotes of the column, ``claims`` of ``claims(t, kind)``.
    """
    lines = doc.splitlines()
    head = next(i for i, line in enumerate(lines) if line.startswith("Notes symbol"))
    start, end = [m.span() for m in re.finditer("=+", lines[head + 1])][1]
    names = set()
    for line in lines[head + 2:]:
        if line.startswith("="):
            break
        bare = re.sub(r"\([^)]*\)|\"[^\"]*\"", "", line[start:end])
        names.update(re.findall(r"[a-z_][a-z0-9_]*", bare))
    return names


_RULE_LINE = re.compile(r"^\s*=+(?:\s+=+)+\s*$")


def _table_overruns(doc):
    """The rows of the RST simple tables in ``doc`` that put text between two columns.

    A simple table's rule lines, runs of ``=`` apart, give its columns' spans, and a row
    whose text runs into the gap between two spans is what docutils rejects as a
    malformed table, dropping the whole table from the page.  Only the last column may run
    past its rule.  Each table runs from a rule line to the blank line that ends it.
    """
    lines, found, i = doc.splitlines(), [], 0
    while i < len(lines):
        if not _RULE_LINE.match(lines[i]):
            i += 1
            continue
        spans = [m.span() for m in re.finditer("=+", lines[i])]
        gaps = set()
        for (_, end), (start, _) in zip(spans, spans[1:]):
            gaps.update(range(end, start))
        i += 1
        while i < len(lines) and lines[i].strip():
            taken = {j for j, ch in enumerate(lines[i]) if ch != " "}
            if not _RULE_LINE.match(lines[i]) and taken & gaps:
                found.append(lines[i].strip())
            i += 1
    return found


# What only WP_UK_S's docstrings may say: a reference into its Spaces, which the SEC pages
# would link to the wrong model; its clock, t counting policy months from issue and t = 0
# the issue month; its frame opening at proj_start(); and its exhaustion's "never", 0.
STALE = re.compile(r"~\.WP_UK_S\.|``t = 0`` is the issue month"
                   r"|``t`` counts \*\*policy months|proj_start\(\)``? is"
                   r"|0 if the units never|``range\(proj_start\(\)")


def test_the_docstrings_describe_the_valuation_clock(sec_model, s_model):
    """The docstrings say what this model is, and none says what only WP_UK_S is.

    Whitespace is collapsed first, as ``test_model_conventions_uk`` collapses it, so that a
    phrase split across a line break still matches.  The model docstring names the
    valuation date, BasicTerm_SE, the policy clock, the SEC table and the product.  The
    symbol map in the Projection docstring maps every cell running in force adds, which are
    exactly the cells ``WP_UK_S`` lacks but the refusals, and names nothing the model lacks:
    every name in it is a cell or a Reference.  No row of a simple table in any docstring
    puts text between two of its columns (:func:`_table_overruns`), which would drop the
    table from the rendered page.  And no docstring says what :data:`STALE` matches.
    """
    flat = {where: re.sub(r"\s+", " ", doc) for where, doc in _docs(sec_model)}
    for phrase in ("valuation date", "BasicTerm_SE", "duration_mth", TABLE, "with-profits"):
        assert phrase in flat["model"], phrase
    added = set(sec_model.Projection.cells) - set(s_model.Projection.cells)
    assert {*NEW_CELLS, *EC_CELLS} == {c for c in added if not c.endswith("_refusal")}, added
    mapped = _mapped_cells(sec_model.Projection.doc)
    missing = [cells for cells in (*NEW_CELLS, *EC_CELLS) if cells not in mapped]
    assert not missing, f"the symbol map does not map {missing}"
    known = set(sec_model.Projection.cells) | set(sec_model.Projection.refs)
    unknown = sorted(mapped - known)
    assert not unknown, f"the symbol map names what the model lacks: {unknown}"
    overruns = {where: rows for where, rows in ((where, _table_overruns(doc))
                                                for where, doc in _docs(sec_model)) if rows}
    assert not overruns, f"table rows that run into a column gap: {overruns}"
    stale = sorted(where for where, doc in flat.items() if STALE.search(doc))
    assert not stale, f"docstrings that describe WP_UK_S: {stale}"


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


# Parameters a formula could confuse, each pair equal somewhere a point or the shipped
# References hold them (*Record — M11*, the template): the withdrawal election and the fund
# return, both 5% on S's withdrawing bond; the bonus rate and the management charge, both
# 1% on the down scenario, and the bonus rate and the charge's cap, both 2% on the worked
# example; the single premium and the units, 25,000 on every bond in force at 60; the asset
# share and the payout, equal while the corridor holds; and the References that ship equal,
# the MVR deterrent and mortality's factor, the guarantee-imminent factor and the
# corridor's floor, the rule's guarantee-fill target and the corridor's floor, and the
# rule's change cap and the management charge.  Each pair as (what, how a row's value of
# each is read).
CONFUSABLE = [
    ("wd_rate and fund_return", lambda p: (p.wd_rate(), p.fund_return())),
    ("bonus_rate_init and amc_rate", lambda p: (p.bonus_rate_init(), p.amc_rate)),
    ("bonus_rate_init and guar_charge_cap", lambda p: (p.bonus_rate_init(),
                                                       p.guar_charge_cap)),
    ("premium_single and units_init", lambda p: (p.premium_single_pp(), p.units_init())),
    ("asset_share_init and smoothed_payout_init",
     lambda p: (p.asset_share_init(), p.smoothed_payout_init())),
    ("mvr_deterrent_factor and mort_be_factor",
     lambda p: (p.mvr_deterrent_factor, p.mort_be_factor)),
    ("guarantee_imminent_factor and corridor_lo",
     lambda p: (p.guarantee_imminent_factor, p.corridor_lo)),
    ("guar_fill_target and corridor_lo", lambda p: (p.guar_fill_target, p.corridor_lo)),
    ("bonus_change_cap and amc_rate", lambda p: (p.bonus_change_cap, p.amc_rate)),
]


def test_parameters_a_formula_could_confuse_differ_on_some_core_row(sec_model, spliced):
    """Each pair of :data:`CONFUSABLE` is equal somewhere and apart on some core T2 row.

    A formula that read one parameter of a pair for the other would pass every comparison
    with S on a row where the two are equal, so each pair that the shipped points or
    References hold equal somewhere must be apart on some row the default run compares
    with S (*Record — M11*): a core T2 or T3 row on the set it runs on, read through the
    projection as the formulas read it.  The rows' own columns are read on the splice's
    model, and nothing is projected.
    """
    rows = []
    for kind, s_point, month, refs in sorted(CORE_GRID):
        sec = spliced[refs][1]
        rows.append(projection(sec, _row_key(sec, kind, s_point, month)))
    shipped = [projection(sec_model, key) for key in point_keys(sec_model)]
    for what, read in CONFUSABLE:
        assert any(len(set(read(p))) == 1 for p in shipped), f"{what} never ship equal"
        assert any(len(set(read(p))) == 2 for p in rows), f"{what} on no core row apart"


def test_the_core_grid_reaches_every_branch(spliced, splice_records):
    """What the default run's T2 and T3 cases reach, which the full grid only multiplies.

    The default run thins the splice to a core (the module docstring), and this test is
    what keeps the thinning from costing a branch.  First, statically, over S's table with
    the variants, each property below holds of some core case: both chassis, both sexes,
    both tax bases, each fund return, a withdrawal election, each set of References, a bond
    and the endowment issued at the valuation date; and each kind of valuation month: the
    first policy year, on an anniversary, in a declaration month, mid-year, on a guarantee
    date, inside the guarantee window, in the last month of a frame.  And of some core
    future case: issued off the valuation anniversaries, more than a year on, a withdrawing
    bond, and under the bonus rule.

    Then, on the splice's model, of some core row, each of :data:`AT_VALUATION` and
    :data:`IN_FRAME`, what no column of the table shows: every opening-state column in use,
    and each kind of valuation month; and every branch and both sides of every ``min`` and
    ``max`` the full grid reaches: a declaration on each chassis, the smoothing cap's floor
    and ceiling and the cap skipped, the corridor's floor and ceiling, the asset share's
    floor, the market value reduction applied and waived, the guarantee exercised and out
    of the money, the imminent window, the charge's cap binding and released, a forced
    encashment and a maturity paid, the limiting age paying nothing, the lapse table inside
    and past its last year, and under the rule a declaration set by it, held to its cap and
    floored at 0.

    Each core row's branches were recorded by the T2 or T3 case that compared it
    (:func:`_settle`), and a row no case has recorded is evaluated here.  With
    ``UKLIB_SEC_FULL=1`` it asks the same of the full grid's rows, which must reach nothing
    the core does not.
    """
    assert set(CORE_SPLICES) <= set(SPLICES + IN_FORCE_TWINS), "a core case off the grid"
    assert set(CORE_FUTURES) <= set(FUTURES), "a core future off the grid"
    s_table = _s_table_with_variants()

    def at(p, column):
        return s_table.at[p, column]

    splices = {
        **{f"the {c} chassis": (lambda k, p, d, r, c=c: at(p, "chassis") == c)
           for c in ("UWP_bond", "CWP_endowment")},
        **{f"sex {x}": (lambda k, p, d, r, x=x: at(p, "sex") == x) for x in ("M", "F")},
        **{f"the {b} basis on a bond": (
            lambda k, p, d, r, b=b: at(p, "tax_basis") == b and at(p, "chassis") == "UWP_bond")
           for b in ("life_net", "pension_gross")},
        **{f"a return of {f:+.0%}": (lambda k, p, d, r, f=f: at(p, "fund_return") == f)
           for f in (0.07, -0.15, 0.05, -0.40)},
        "a withdrawal election": lambda k, p, d, r: at(p, "wd_rate") > 0.0,
        **{f"the {r} set": (lambda k, p, d, r_, r=r: r_ == r) for r in REF_SETS},
        "a bond issued at the valuation date": lambda k, p, d, r: (
            at(p, "chassis") == "UWP_bond" and int(at(p, "duration_inforce")) == 0),
        "the endowment issued at the valuation date": lambda k, p, d, r: (
            at(p, "chassis") == "CWP_endowment" and int(at(p, "duration_inforce")) == 0),
        "in the first policy year": lambda k, p, d, r: d < 12,
        "on an anniversary": lambda k, p, d, r: d % 12 == 0,
        "in a declaration month": lambda k, p, d, r: d % 12 == 11,
        "mid-year": lambda k, p, d, r: d % 12 not in (0, 11),
        "on a guarantee date": lambda k, p, d, r: d == 119 and at(p, "chassis") == "UWP_bond",
        "inside the guarantee window": lambda k, p, d, r: (
            at(p, "chassis") == "UWP_bond" and 107 <= d < 119),
    }
    futures = {
        "issued off the anniversaries": lambda p, k, r: k % 12 != 0,
        "issued more than a year on": lambda p, k, r: k > 12,
        "a withdrawing bond": lambda p, k, r: at(p, "wd_rate") > 0.0,
        "under the bonus rule": lambda p, k, r: r == "rule",
    }
    missing = [what for what, holds in splices.items()
               if not any(holds(*case) for case in CORE_SPLICES)]
    missing += [what for what, holds in futures.items()
                if not any(holds(*case) for case in CORE_FUTURES)]
    assert not missing, f"no core case reaches: {missing}"
    reached = set()
    for case in sorted(CORE_GRID):
        reached |= _record_of(spliced, splice_records, case)["branches"]
    missing = sorted(REACHED - reached)
    assert not missing, f"no core row reaches: {missing}"
    if SEC_FULL:
        beyond = set()
        for case in GRID:
            if case not in CORE_GRID:
                beyond |= _record_of(spliced, splice_records, case)["branches"]
        beyond &= REACHED
        assert beyond <= reached, f"the full grid alone reaches: {sorted(beyond - reached)}"


# ---------------------------------------------------------------------------
# The C step's representation (UKLIB-SEC-PLAN.md §6.5, *C*)
#
# Data decodes each model point's text into the number the projection reads, the guarantee
# dates into a flag by point and policy year, and turns each table into an array indexed by
# integers (USLIB-SEC-PLAN.md R5-R8); a timing and a kind are int codes, and the claims
# total is a code of its own, Neumaier's sum written out (R9, R12); the six chains whose
# value can leave the floats refuse it in a cell of their own; and the eight chains are
# blocked by policy year (K12), which the depth test and the openings' test above hold.
# These tests hold the representation in modelx, with no compiler, in seconds: the compiled
# section after the fingerprint holds the compiled model to modelx on it.


# Whether sum() compensates, Neumaier's way, as it does for floats from Python 3.12 on most
# builds, read from sum() itself as test_model_conventions_uk.py's SUM_COMPENSATES reads it.
# The claims total is WP_UK_S's sum() written out, so it is S's bits only where sum()
# compensates.  Python 3.11's sum() adds left to right, and there S's total, and sum() of
# the kinds, part from this one where the three kinds are of a size (UKLIB-SEC-PLAN.md
# §6.3, *Record -- M8*, *Carried into M15*): the total's bit test holds the rest and skips
# the bits there, with this reason.
SUM_COMPENSATES = sum([0.1] * 10) == 1.0
SUM_311 = ("Python 3.11's sum() adds floats left to right, without the compensation it has "
           "from 3.12, so the total written out here is not its bits; the rest was held")


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


def _left_to_right(kinds):
    """``kinds`` totalled left to right from ``0.0``: ``sum``'s float only where at most
    two of them are non-zero (R12)."""
    total = 0.0
    for x in kinds:
        total = total + x
    return total


def _neumaier(kinds, *, swapped=False, checked=True):
    """``kinds`` totalled as ``sum`` totals them, and whether a later kind outweighed the
    running total, where the carried rounding error takes the second form.

    ``swapped`` carries each such kind's error in the first form, as an earlier kind's;
    ``checked=False`` adds the carried error at the end even where it is not finite.  Each
    is a way to miswrite ``Projection.claims``' total that a comparison sees only on a row
    that reaches it, which the test asserts its rows do (``CI_UK_SEC``'s form,
    UKLIB-SEC-PLAN.md §6.2, *Record -- M4*).
    """
    f, c, taken = 0.0 + kinds[0], 0.0, False
    for x in kinds[1:]:
        s = f + x
        if abs(f) >= abs(x):
            c = c + ((f - s) + x)
        else:
            taken = True
            c = c + (((f - s) + x) if swapped else ((x - s) + f))
        f = s
    if c != 0.0 and (not checked or abs(c) <= sys.float_info.max):
        f = f + c
    return f, taken


def _lapse_at(rate):
    """An edit of *lapse_table.csv* that sets every rate to ``rate``."""
    return lambda table: table.assign(lapse_rate=rate)


# The rows on which the three kinds are of a size, so that a total written left to right
# parts from sum's: each row's last month, the endowment's maturity at 299 (16) and the
# withdrawing bond's forced encashment at 402 (14), under a lapse table of 99% and the
# mortality scaled by mort_be_factor until the deaths, the surrenders and the maturity are
# each a fair share of the month's claims, on copies of the row whose counts,
# COMPARABLE_COUNTS, move where the sum rounds.  Under each row the lower factor makes each
# later kind outweigh the running total, and the higher none: as (the row, mort_be_factor,
# (rows, rows where a total left to right parts from sum's, rows where a later kind
# outweighs the running total, rows where carrying its error in the first form parts from
# sum's)), measured at M14.
COMPARABLE = [(16, 118.3, (60, 9, 60, 4)), (16, 130.0, (60, 9, 0, 0)),
              (14, 8.51, (60, 7, 60, 5)), (14, 9.36, (60, 11, 0, 0))]
COMPARABLE_COUNTS = tuple(1.0 + 0.0137 * k for k in range(60))


def _comparable_rows(base):
    """The committed row ``base`` once for each of :data:`COMPARABLE_COUNTS`, labelled 101
    on."""
    row = _committed().loc[[base]]
    return pd.concat([row.assign(policy_count=count).set_axis([101 + k])
                      for k, count in enumerate(COMPARABLE_COUNTS)]).rename_axis("point_id")


def test_the_all_total_is_s_total_bit_for_bit(sec_model, s_model, tmp_path):
    """``claims(t, ALL)`` is ``WP_UK_S``'s ``claims(t)``, its ``sum``, to the last bit.

    S totals its three kinds with Python's ``sum``, which compensates, Neumaier's way, and
    the total here is that sum written out (``Projection.claims``, ``CI_UK_SEC``'s form):
    the deaths, the surrenders and the maturity are non-zero together in a frame's last
    month, where a total written left to right can part from ``sum``'s in the last bit
    (USLIB-SEC-PLAN.md R12).  So the kinds non-zero together are counted, in every month of
    every committed point's frame and the month after it: three in seven months, each a
    frame's last, two in 6,506 and one in 3,035, which is asserted.  The total is compared
    by ``float.hex`` with ``sum`` of the row's own three kinds there; and on every twin of
    S's points, whose kinds are S's to the last bit, with S's ``claims(t)`` itself.  T1
    compares the totals to 1e-9; this compares their bits.

    On the committed points the maturity outweighs the rest wherever three kinds are paid,
    and a total written left to right is ``sum``'s in every month, so the comparison could
    not fail there.  So the test reads :data:`COMPARABLE`'s rows too, where the three are of
    a size, each row's copies under its factor, and asserts the rows where a total left to
    right parts from ``sum``'s, those where a later kind outweighs the running total, and
    those where carrying its error in the first form parts, each a way to miswrite the
    total, with every kind paid and the total ``sum``'s in every row.  And on the
    endowment's last month on 1e304 policies, where each kind is finite and their sum is
    not, ``sum``'s carried error is NaN, which it leaves out: the total is refused as
    ``inf``, naming the three kinds, where a carried error added unchecked would make it,
    and the refusal, NaN.

    The bits are ``sum``'s where it compensates, from Python 3.12.  Where it does not, on
    Python 3.11 (:data:`SUM_COMPENSATES`), ``sum`` and S with it add left to right, and the
    total here parts from them where the three kinds are of a size: there the kinds counted,
    the rows of :data:`COMPARABLE`, every kind paid and the second form taken on them, and
    the refusal are held, and the bits skip, naming Python 3.11 (:data:`SUM_311`).
    """
    total = _code(sec_model.Projection, "ALL")
    kinds = [_code(sec_model.Projection, kind) for kind in KINDS]
    found, bits, counts, apart = [], [], {0: 0, 1: 0, 2: 0, 3: 0}, 0
    table = sec_model.Data.model_point_table()
    for key, point_id in zip(point_keys(sec_model), table.index):
        p = projection(sec_model, key)
        for t in range(p.proj_len() + 1):
            values = [p.claims(t, kind) for kind in kinds]
            counts[sum(v != 0.0 for v in values)] += 1
            apart += _left_to_right(values).hex() != sum(values).hex()
            if p.claims(t, total).hex() != sum(values).hex():
                bits.append(f"point {point_id}, t = {t}: {p.claims(t, total)!r}, the "
                            f"kinds' sum {sum(values)!r}")
    for point_id in table.index[table["row_kind"] == "twin"]:
        s, p = _point(s_model, point_id), _point(sec_model, point_id)
        month = int(table.at[point_id, "source_mth"])
        for t in range(p.proj_len()):
            if p.claims(t, total).hex() != s.claims(t + month).hex():
                bits.append(f"twin {point_id}, t = {t}: {p.claims(t, total)!r}, S "
                            f"{s.claims(t + month)!r}")
    assert counts == {0: 37, 1: 3035, 2: 6506, 3: 7}, counts
    parts = []
    for base, factor, want in COMPARABLE:
        model = mx.read_model(_sec_inputs(tmp_path / f"rows{base}_{factor}",
                                          _comparable_rows(base), {LAPSE: _lapse_at(0.99)}),
                              name=_name("comparable"))
        try:
            model.Projection.mort_be_factor = factor
            rows = parted = taken = swapped = 0
            for key in point_keys(model):
                p = projection(model, key)
                t = p.proj_len() - 1
                values = [p.claims(t, kind) for kind in kinds]
                rows += 1
                parted += _left_to_right(values).hex() != sum(values).hex()
                taken += _neumaier(values)[1]
                swapped += _neumaier(values, swapped=True)[0].hex() != sum(values).hex()
                if not all(v > 0.0 for v in values):
                    found.append(f"row {base} at {factor}, idx {key}: kinds {values}")
                if p.claims(t, total).hex() != sum(values).hex():
                    bits.append(f"row {base} at {factor}, idx {key}: "
                                f"{p.claims(t, total)!r}, the kinds' sum {sum(values)!r}")
            assert (rows, taken) == (want[0], want[2]), (base, factor, rows, taken)
            parts.append(((base, factor), (parted, swapped), (want[1], want[3])))
        finally:
            model.close()
    model = mx.read_model(_sec_inputs(tmp_path / "infinite",
                                      _committed().loc[[16]].assign(policy_count=1e304),
                                      {LAPSE: _lapse_at(0.99)}), name=_name("infinite"))
    try:
        model.Projection.mort_be_factor = 130.0
        p = _point(model, 16)
        values = [p.claims(0, kind) for kind in kinds]
        assert all(math.isfinite(v) for v in values) and sum(values) == math.inf, values
        assert math.isnan(_neumaier(values, checked=False)[0]), values
        _refused(lambda: p.claims(0, total),
                 f"point_id 16: the claims claims(0, ALL) are inf, not a finite number, "
                 f"from the death, surrender and maturity claims {values[0]}, {values[1]} "
                 f"and {values[2]}")
    finally:
        model.close()
    assert not found, found[:10]
    _hold_the_sums_bits()
    assert apart == 0, apart
    assert all(got == want for _, got, want in parts), parts
    assert not bits, bits[:10]


# The six chains whose refusal of a value past the floats is a cell of its own, which
# computes the value again from the same cells and raises only where the chain would, as
# (the chain, its refusal cell).
REFUSAL_CELLS = (("asset_share", "asset_share_refusal"), ("unit_price", "unit_price_refusal"),
                 ("units", "units_refusal"), ("guar_benefit_pp", "guar_benefit_refusal"),
                 ("guar_charge_cum_pp", "guar_charge_cum_refusal"),
                 ("smoothing_account", "smoothing_account_refusal"))


def _month_kind(p, t):
    """What month ``t`` is to ``p``: its first on the books, a policy year's first after
    it, a declaration month, the twelfth of its policy year, or another, mid-year."""
    if t == p.t_entry():
        return "entry"
    if p.duration_mth(t) % 12 == 0:
        return "anniversary"
    return "declaration" if p.is_declaration_month(t) else "mid-year"


def test_each_refusal_cell_computes_its_chain_s_value_bit_for_bit(sec_model):
    """Each of the six refusal cells returns its chain's value, bit for bit, every month.

    No cell a chain recurses through builds text (the chain-text test), so the asset share,
    the unit price, the units, the guarantee, the cumulant of the charges and the smoothing
    account call a refusal cell of their own on their error paths alone, and each refusal
    cell repeats its chain's formula, branch by branch, to name the value it refuses
    (:data:`REFUSAL_CELLS`).  Nothing else holds the two formulas together: C4 compares two
    engines that share any drift, and a refusal cell is reached only past the floats.  So
    on every committed point, in every month of its frame and the month after it, each
    refusal cell must return its chain's value, by ``float.hex``: its first month on the
    books, every month within a policy year, every declaration month, and every year's
    first month after ``t_entry()``, whose value is the year's opening, each kind of month
    asserted reached.  A refusal that dropped a step, or read the month before where the
    chain reads the year's opening, parts here, though the value it would refuse only ever
    leaves the floats in a test of its own
    (:func:`test_each_chain_past_the_floats_after_its_first_month_is_refused_there`).
    """
    found, months = [], {"entry": 0, "anniversary": 0, "declaration": 0, "mid-year": 0}
    for key, point_id in zip(point_keys(sec_model), sec_model.Data.model_point_table().index):
        p = projection(sec_model, key)
        for t in range(p.proj_len() + 1):
            if t < p.proj_len():
                months[_month_kind(p, t)] += 1
            for chain, refusal in REFUSAL_CELLS:
                want, got = p.cells[chain](t), p.cells[refusal](t)
                if got.hex() != want.hex():
                    found.append(f"point {point_id}: {refusal}({t}) is {got!r}, "
                                 f"{chain}({t}) {want!r}")
    assert min(months.values()) > 10, months
    assert not found, found[:10]


# The References under which the cumulant of the guarantee charges leaves the floats after
# its first month: the whole asset share charged a month, guar_charge_rate_base 1, and no
# management charge, so that the asset share closes every month at nil.  The charge stops
# once the cumulant reaches its cap, a share of the asset share the month opens with, but
# the cap is not tested on a nil asset share, so on the endowment, which pays a premium
# every month, the cumulant grows by each month's premium, charged in full, with no estate
# distribution.
CUMULANT_REFS = {"amc_rate": 0.0, "guar_charge_rate_base": 1.0}


def _cumulant(value):
    """The endowment at 150, its asset share and payout nil, paying 6e307 a year, the
    cumulant of its charges opening at ``value``."""
    return {"asset_share_init": 0.0, "smoothed_payout_init": 0.0,
            "premium_regular": 6e307, "guar_charge_cum_pp_init": value}


# Each chain with a refusal cell of its own taken past the floats after its first month on
# the books, as (case, the committed row, its columns changed, the References, the chain,
# the month, what the month is, the message after the point's label): mid-year, on a
# declaration and on an anniversary where the chain moves there.  The bond at 71 (8) opens
# on a declaration, and its month 1 is an anniversary, 2 mid-year, 12 a declaration and 13
# an anniversary; the down scenario's bond at 92 (10) opens mid-year, and its month 3 is a
# declaration and 4 an anniversary; and the endowment at 150 (23) is mid-year in month 3,
# declares in month 5 and reaches its anniversary in month 6.  The asset share is opened
# near the largest float, and grows past it by its return; the units are bought on by a
# regular premium at a price near the smallest float; the unit price, on a bond holding few
# units, and the endowment's guarantee are raised by a declaration, which alone moves them;
# the bond's guarantee is its units at a price near 1.7e8, bought on by a premium; the
# smoothing account opens near the largest float on 1e305 policies, whose exits add a
# month's cost; and the cumulant is the guarantee charges' on the endowment, each month's
# premium charged in full (CUMULANT_REFS).  Each value is the middle, in log space, of the
# values whose first month past the floats is the one named, measured at M14 by bisection,
# or the middle of that window, read off the charges, for the cumulant, so that each holds a
# few months' growth either side of its edge.  The month 0 refusals are PAST_THE_FLOATS'.
_AS = ("the asset share of month {t} before its floor, asset_share_at({t}, 'AFT_MC'), is "
       "inf, not a finite number, from the opening asset share ")
_UNITS = "the units held units({t}) are inf, not a finite number, from the opening units "
_PRICE = "the unit price unit_price({t}) is inf, not a finite number, from the opening price "
_GUARANTEE = "the guaranteed benefit guar_benefit_pp({t}) is inf, not a finite number, from "
_CUMULANT = ("the cumulative guarantee charge guar_charge_cum_pp({t}) is inf, not a finite "
             "number, from the charges carried in, ")
_ACCOUNT = ("the smoothing account smoothing_account({t}) is inf, not a finite number, from "
            "the account carried in, ")
_CHEAP = {"unit_price_init": 1e-300}
_DEAR = {"unit_price_init": 1.7e8, "units_init": 1e300}
_CROWD = {"policy_count": 1e305}
CHAINS_PAST = [
    ("the asset share mid-year", 8, {"asset_share_init": 1.775e308}, {}, "asset_share", 2,
     "mid-year", _AS),
    ("the asset share on a declaration", 8, {"asset_share_init": 1.6932e308}, {},
     "asset_share", 12, "declaration", _AS),
    ("the asset share on an anniversary", 8, {"asset_share_init": 1.6852e308}, {},
     "asset_share", 13, "anniversary", _AS),
    ("the units mid-year", 8, {**_CHEAP, "premium_regular": 8.91e8}, {}, "units", 2,
     "mid-year", _UNITS),
    ("the units on a declaration", 8, {**_CHEAP, "premium_regular": 1.759e8}, {}, "units", 12,
     "declaration", _UNITS),
    ("the units on an anniversary", 8, {**_CHEAP, "premium_regular": 1.63e8}, {}, "units",
     13, "anniversary", _UNITS),
    ("the unit price on a declaration", 8, {"units_init": 1e-5, "unit_price_init": 1.745e308},
     {}, "unit_price", 12, "declaration", _PRICE),
    ("the bond's guarantee mid-year", 8, {**_DEAR, "premium_regular": 3.09e307}, {},
     "guar_benefit_pp", 2, "mid-year", _GUARANTEE),
    ("the bond's guarantee on a declaration", 8, {**_DEAR, "premium_regular": 4.08e306}, {},
     "guar_benefit_pp", 12, "declaration", _GUARANTEE),
    ("the bond's guarantee on an anniversary", 8, {**_DEAR, "premium_regular": 2.528e306},
     {}, "guar_benefit_pp", 13, "anniversary", _GUARANTEE),
    ("the endowment's guarantee on a declaration", 23, {"sum_assured": 1.792e308}, {},
     "guar_benefit_pp", 5, "declaration", _GUARANTEE),
    ("the cumulant mid-year", 23, _cumulant(1.622e308), CUMULANT_REFS,
     "guar_charge_cum_pp", 3, "mid-year", _CUMULANT),
    ("the cumulant on a declaration", 23, _cumulant(1.5216e308), CUMULANT_REFS,
     "guar_charge_cum_pp", 5, "declaration", _CUMULANT),
    ("the cumulant on an anniversary", 23, _cumulant(1.4714e308), CUMULANT_REFS,
     "guar_charge_cum_pp", 6, "anniversary", _CUMULANT),
    ("the smoothing account mid-year", 10, {**_CROWD, "smoothing_account_init": 1761.9}, {},
     "smoothing_account", 2, "mid-year", _ACCOUNT),
    ("the smoothing account on a declaration", 10,
     {**_CROWD, "smoothing_account_init": 1747.6}, {}, "smoothing_account", 3, "declaration",
     _ACCOUNT),
    ("the smoothing account on an anniversary", 10,
     {**_CROWD, "smoothing_account_init": 1733.0}, {}, "smoothing_account", 4, "anniversary",
     _ACCOUNT),
]


def _chains_past_tables():
    """:data:`CHAINS_PAST`'s rows, each its committed row with its columns changed under a
    label of its own, 201 on, in two tables by the References they are read under: ``{the
    References' items: (table, [(label, case)])}``."""
    committed, tables = _committed(), {}
    for n, case in enumerate(CHAINS_PAST):
        _, row, changes, refs, *_ = case
        label = 201 + n
        rows, cases = tables.setdefault(tuple(refs.items()), ([], []))
        rows.append(committed.loc[[row]].assign(**changes).set_axis([label]))
        cases.append((label, case))
    return {refs: (pd.concat(rows).rename_axis("point_id"), cases)
            for refs, (rows, cases) in tables.items()}


def test_each_chain_past_the_floats_after_its_first_month_is_refused_there(tmp_path):
    """Each chain with a refusal cell refuses a value that first leaves the floats after its
    first month, mid-year, on a declaration and on an anniversary, in that month.

    A chain blocked by policy year reads its month before within a year, and a year's
    opening, which walks the year before, in the year's first month; its refusal cell
    repeats the branch, and a declaration moves a chain in a month of its own.  The
    refusals at ``t_entry()`` are :data:`PAST_THE_FLOATS`'; each case of
    :data:`CHAINS_PAST` takes its chain past the largest float later, from an opening
    state, columns and References each in its domain, under a label of its own on one read
    of its References: the asset share, the units and the cumulant of the guarantee charges
    mid-year, on a declaration and on an anniversary; the unit price on a declaration, which
    alone moves it; the bond's guarantee in all three, and the endowment's on its
    declaration, which alone moves it; and the smoothing account in all three.  Each month's
    kind is asserted of the row, the chain is finite in every month before it, from a cold
    start, and refused in it, naming the point, the month and what makes it, and so is the
    chain's refusal cell, called in that month.
    """
    refusals = dict(REFUSAL_CELLS)
    found = []
    for n, (refs, (table, cases)) in enumerate(_chains_past_tables().items()):
        model = mx.read_model(_sec_inputs(tmp_path / f"case{n}", table), name=_name("past"))
        try:
            for ref, value in refs:
                setattr(model.Projection, ref, value)
            for label, (case, _, _, _, chain, month, kind, message) in cases:
                p = _point(model, label)
                assert p.t_entry() == 0 < month < p.proj_len(), case
                assert _month_kind(p, month) == kind, (case, _month_kind(p, month))
                before = [p.cells[chain](t) for t in range(month)]
                if not all(math.isfinite(v) for v in before):
                    found.append(f"{case}: past the floats before month {month}: {before}")
                text = f"point_id {label}: " + message.format(t=month)
                _refused(lambda: p.cells[chain](month), text)
                _refused(lambda: p.cells[refusals[chain]](month), text)
        finally:
            model.close()
    assert not found, found


# One S point per value a decoded column can hold, as (the S point it changes, the columns
# it changes): S's bond issued at the valuation date (7) and its endowment (5), each as
# shipped, each a woman and each on the pension basis; and the bond's guarantee dates as a
# year written with a fraction of 0, as a spreadsheet saves it, beside a blank and two
# spaces, three years with a blank part between two of them, none at all, and the 70th
# policy year, past the bond's frame, which the flags hold all the same.
DECODED = [
    (7, {}), (5, {}),
    (7, {"sex": "F"}), (5, {"sex": "F"}),
    (7, {"tax_basis": "pension_gross"}), (5, {"tax_basis": "pension_gross"}),
    (7, {"guarantee_dates": " 3.0 "}), (7, {"guarantee_dates": "5;;10; 15"}),
    (7, {"guarantee_dates": float("nan")}), (7, {"guarantee_dates": "70"}),
]

# The cells each decoded point is compared on, WP_UK_S's own, which read the text or the
# number themselves, the labels among them, and those read at a month; and the decodes
# here, each against S's own reading of the text.
DECODING_CELLS = ("chassis", "sex", "tax_basis", "is_unitised", "age_at_entry",
                  "policy_term", "sum_assured", "wd_rate", "fund_return", "proj_len")
MONTHLY_DECODED = ("mort_rate", "surr_rate_base", "is_guarantee_date", "guarantee_imminent",
                   "surr_rate")
DECODES = {"chassis_code": lambda s: ("UWP_bond", "CWP_endowment").index(s.chassis()),
           "mort_schedule": lambda s: ("M", "F").index(s.sex())}


def _decoded_twins(tmp_path):
    """``(S, its table)``: :data:`DECODED`'s points in a copy of S's table, read; and the
    twins of them the generator makes, the SEC table."""
    s_table = _s_table()
    rows = []
    for i, (base, changes) in enumerate(DECODED, start=1):
        row = s_table.loc[[base]].astype({"guarantee_dates": object}).assign(
            **changes, policy_id=f"WP-8{i:05d}")
        row.index = pd.Index([i], name="point_id")
        rows.append(row)
    table = pd.concat(rows)
    s = mx.read_model(temp_inputs(tmp_path / "s", model_path(TWIN), model_points=table),
                      name=_name("decoded_s"))
    spec = dataclasses.replace(SPEC, derived=(), future=(), derived_refs={})
    twins, _ = build_sec_table(spec, s)
    return s, twins


# The guarantee flags' last column, Data.guarantee_year_last, the mortality table's last age
# plus 2, which a frame reads only on a table that rates age 0 and ends at 102 or before,
# issue_age_min lowered to 0: a bond issued at 0 to a year past the table's last age, L + 1,
# reads in its last month the year after its cover's last, L + 2, its guarantee-imminent
# window's.  The decoded case on such a table: the shipped table cut to ages 0 to
# LAST_COLUMN_AGE, each sex's rate at 18 standing at every age below it, and S's bond
# variant issued at the valuation date at 0, withdrawing nothing, its one guarantee date
# that year, read with omega_age at LAST_COLUMN_AGE + 1, and on SEC issue_age_min at 0.
LAST_COLUMN_AGE = 60
LAST_COLUMN_REFS = {"omega_age": LAST_COLUMN_AGE + 1}


def _young_table(last):
    """An edit of *mort_table.csv* that rates ages 0 to ``last``: the shipped rates to
    ``last``, and each sex's rate at 18 at every age below it."""
    def edit(table):
        kept = table[table["age"] <= last]
        young = [kept[kept["age"] == 18].assign(age=a) for a in range(18)]
        return pd.concat([*young, kept], ignore_index=True).sort_values(
            ["sex", "age"], kind="stable", ignore_index=True)
    return edit


def _last_column_pair(tmp_path):
    """``(S, SEC, SEC's table)`` on :func:`_young_table`'s table: S's bond variant issued at
    0 with its one guarantee date at the flags' last column, and its twin, generated from
    it, each read under the References the case needs (:data:`LAST_COLUMN_AGE`)."""
    edits = {MORT: _young_table(LAST_COLUMN_AGE)}
    row = _s_table().loc[[7]].astype({"guarantee_dates": object}).assign(
        age_at_entry=0, wd_rate=0.0, guarantee_dates=str(LAST_COLUMN_AGE + 2),
        policy_id="WP-800099")
    row.index = pd.Index([1], name="point_id")
    s = mx.read_model(temp_inputs(tmp_path / "s", model_path(TWIN), model_points=row,
                                  edits=edits), name=_name("last_column_s"))
    for ref, value in LAST_COLUMN_REFS.items():
        setattr(s.Projection, ref, value)
    spec = dataclasses.replace(SPEC, derived=(), future=(), derived_refs={})
    twins, _ = build_sec_table(spec, s)
    sec = mx.read_model(_sec_inputs(tmp_path / "sec", twins, edits),
                        name=_name("last_column_sec"))
    for ref, value in {**LAST_COLUMN_REFS, "issue_age_min": 0}.items():
        setattr(sec.Projection, ref, value)
    return s, sec, twins


def _decode_mismatches(case, sp, p, s, sec):
    """Where SEC point ``p``, of model ``sec``, reads a decoded value otherwise than S point
    ``sp``, of model ``s``, reads its text: the lines
    :func:`test_every_decode_is_wp_uk_s_own_on_every_value` reports."""
    found = []
    calls = [(cell, ()) for cell in DECODING_CELLS]
    calls += [(cell, (t,)) for cell in MONTHLY_DECODED for t in range(p.proj_len())]
    for cell, args in calls:
        want, got = sp.cells[cell](*args), p.cells[cell](*args)
        if got != want or type(got) is not type(want):
            found.append(f"{case}: {cell}{args} is {got!r}, S {want!r}")
    for cell, read in DECODES.items():
        want, got = read(sp), p.cells[cell]()
        if got != want or type(got) is not type(want):
            found.append(f"{case}: {cell}() is {got!r}, S's text gives {want!r}")
    years = sp.guarantee_years()
    for y in range(sec.Data.guarantee_year_last() + 3):
        got = p.is_guarantee_year(y)
        if got is not (y in years):
            found.append(f"{case}: is_guarantee_year({y}) is {got!r}, S's years {years}")
    rates, mort = s.Data.mort_table()["mort_rate"], sec.Data.mort_table_array()
    row = p.mort_schedule()
    for a in range(sec.Data.mort_age_first(), sec.Data.mort_age_last() + 1):
        want = rates.loc[(sp.sex(), a)]
        if mort[row, a] != want:
            found.append(f"{case}: row {row} at age {a} is {mort[row, a]!r}, S's rate "
                         f"{want!r}")
    lapses, lapse = s.Data.lapse_table()["lapse_rate"], sec.Data.lapse_table_array()
    code, last = p.chassis_code(), p.lapse_last_year()
    assert last == int(lapses.loc[sp.chassis()].index.max()), case
    for y in range(1, last + 1):
        if lapse[code, y] != lapses.loc[(sp.chassis(), y)]:
            found.append(f"{case}: lapse row {code} at year {y} is {lapse[code, y]!r}, "
                         f"S's {lapses.loc[(sp.chassis(), y)]!r}")
    return found


def test_every_decode_is_wp_uk_s_own_on_every_value(tmp_path):
    """``Data`` decodes every value a column can hold as ``WP_UK_S``'s cells read it.

    A point of each case of :data:`DECODED` goes into a copy of S's table, and its twin,
    generated from it, into a copy of SEC's.  On each pair every cell of
    :data:`DECODING_CELLS` agrees exactly, in value and in type, the labels among them, and
    so do the cells of :data:`MONTHLY_DECODED` in every month of the frame: the mortality
    and lapse rates, the guarantee date and its imminent window; each decode of
    :data:`DECODES` is S's reading of the text, as an int; ``is_guarantee_year(y)`` is ``y in
    guarantee_years()``, S's tuple, at every policy year from 0 to two past the flags' last,
    as a bool; the point's row of the mortality table, ``mort_schedule()``, holds S's rate
    for its sex at every age of the table; and its chassis's row of the lapse table,
    ``chassis_code()``, S's rate at every policy year of the chassis's rows, its last year,
    ``lapse_last_year()``, the chassis's own.  T1 and the splice see these through the
    cells that use them, at the values their points carry; this sees every value, on its
    own.  A mortality array off by one age, a lapse clamp a year early, a guarantee flag a
    year off, or a schedule numbered otherwise than ``Data`` numbers it, parts here.

    And the flags' last column, ``Data.guarantee_year_last``, which a frame reaches only on
    a table that rates age 0 and ends at 102 or before, ``issue_age_min`` lowered to 0: on
    a copy of the mortality table cut to ages 0 to :data:`LAST_COLUMN_AGE`, a bond issued at
    0 to a year past the table's last age, its one guarantee date the flags' last year,
    which its last month's guarantee-imminent window waits for, is held to ``WP_UK_S`` as
    every decoded case is, that window among its months.  A flag that stops a year short
    of the array's width parts here, though no shipped table's frame reads that column.
    """
    s, twins = _decoded_twins(tmp_path)
    sec = None
    found = []
    try:
        sec = mx.read_model(_sec_inputs(tmp_path / "sec", twins), name=_name("decoded"))
        labels = s.Data.model_point_table().index
        for (base, changes), key, label in zip(DECODED, point_keys(sec), labels,
                                               strict=True):
            found += _decode_mismatches(f"S point {base} with {changes}", _point(s, label),
                                        projection(sec, key), s, sec)
        assert {p.is_unitised() for p in (projection(sec, k) for k in point_keys(sec))} == {
            True, False}
    finally:
        if sec is not None:
            sec.close()
        s.close()
    s, sec, _ = _last_column_pair(tmp_path / "last_column")
    try:
        sp, p = _point(s, 1), _point(sec, 1)
        end = p.proj_len() - 1
        assert p.proj_len() == 12 * (LAST_COLUMN_AGE + 1) and p.duration_mth(0) == 0
        assert sec.Data.guarantee_year_last() == LAST_COLUMN_AGE + 2
        assert (p.duration_mth(end) + 13) // 12 == sec.Data.guarantee_year_last()
        assert sp.guarantee_imminent(end) == sp.guarantee_imminent_factor != 1.0
        found += _decode_mismatches("the flags' last column", sp, p, s, sec)
    finally:
        sec.close()
        s.close()
    assert not found, found[:20]


# The written forms of one guarantee date, policy year 10, which an extract may carry, as
# the value written into the bond's guarantee_dates: as text with a blank before it and one
# after, as a whole number and as one with a fraction of 0, each of which the check and the
# decode read alike, as WP_UK_S reads it.  (UKLIB-SEC-PLAN.md §6.7, *Record -- M12*: a
# column a projection branches on is checked and decoded by the same reading.)
DATE_FORMS = (" 10", "10 ", 10, "10.0")


def test_each_written_form_of_a_guarantee_date_is_read_as_the_date(sec_model, tmp_path):
    """A guarantee date written as an extract may write it is read as that date, by the
    check and the decode alike, and by ``WP_UK_S``.

    ``WP_UK_SEC`` has no column of flags: the one column whose text the projection branches
    on is ``guarantee_dates``, which ``Data.model_point_table`` checks and
    ``Data.guarantee_flags`` decodes, each part of it read by its value once stripped, as
    ``WP_UK_S``'s ``guarantee_years`` reads it.  So the worked example's bond in force at
    60, whose tenth anniversary is in its frame, is copied once for each form of
    :data:`DATE_FORMS`, its date, year 10, written in that form, a blank before or after
    it, a whole number and one with a fraction of 0: each copy is read, its
    ``is_guarantee_year`` true at 10 and at no other year, and it projects ``result_cf`` and
    ``result_payout`` as the committed row does, bit for bit, the guarantee date's exit
    among them; and S's ``guarantee_years`` is ``(10,)`` from each, on S's point 1 so
    written.  A form one reading accepted and the other refused, or read otherwise, would
    part here.
    """
    shipped = _point(sec_model, 1)
    want = {name: shipped.cells[name]() for name in ("result_cf", "result_payout")}
    row = _committed().loc[[1]].astype({"guarantee_dates": object})
    assert row.at[1, "guarantee_dates"] == 10.0
    copies = pd.concat([row.assign(guarantee_dates=[form]).set_axis([101 + n])
                        for n, form in enumerate(DATE_FORMS)]).rename_axis("point_id")
    s_row = _s_table().loc[[1]].astype({"guarantee_dates": object})
    s_copies = pd.concat([s_row.assign(guarantee_dates=[form], policy_id=f"WP-7{n:05d}")
                          .set_axis([101 + n]) for n, form in enumerate(DATE_FORMS)])
    model = mx.read_model(_sec_inputs(tmp_path / "sec", copies), name=_name("forms"))
    s = mx.read_model(temp_inputs(tmp_path / "s", model_path(TWIN),
                                  model_points=s_copies.rename_axis("point_id")),
                      name=_name("s_forms"))
    try:
        last = model.Data.guarantee_year_last()
        for n, form in enumerate(DATE_FORMS):
            p = _point(model, 101 + n)
            years = [y for y in range(last + 1) if p.is_guarantee_year(y)]
            assert years == [10], (form, years)
            for name, frame in want.items():
                assert p.cells[name]().equals(frame), (form, name)
            assert _point(s, 101 + n).guarantee_years() == (10,), form
    finally:
        s.close()
        model.close()


def _bond_lapses_to(last):
    """An edit of *lapse_table.csv* that runs the bond's rows on to policy year ``last``,
    6% in year 2, 7% in 3, and so on, past the endowment's last year, 4."""
    def edit(table):
        bond = table[table["chassis"] == "UWP_bond"]
        more = [bond.assign(policy_year=y, lapse_rate=0.04 + 0.01 * y)
                for y in range(2, last + 1)]
        return pd.concat([table, *more], ignore_index=True)
    return edit


def test_every_padded_array_holds_nan_and_no_reader_reads_it(sec_model, tmp_path):
    """The padding is NaN, and each table's one reader reads inside its keys alone.

    ``Data`` tables the mortality rates from age 0, a row a sex, and the lapse rates from
    policy year 0, a row a chassis, and pads what no file holds with NaN, as its docstring
    says, so that a read past a check, were one lost, would make every number after it NaN
    rather than another key's value: each sex's ages below the table's first, 18 as
    shipped, year 0 of each chassis and the bond's years past its last, 1.  Inside, nothing
    is NaN.  The bond, whose one row is year 1, reads it at every policy year, as
    ``WP_UK_S``'s ``tbl.index.max()`` on the chassis's own rows does.  On a copy whose bond
    rows run on to policy year 6, past the endowment's 4, the array is seven years wide, as
    wide as the longest chassis, the endowment's row NaN past its own last year, and each
    point reads its own chassis's last year at every later year: the bond in force at 60,
    in its sixth year, reads 6% to 9% over years 2 to 5 of the copy at the right months,
    and year 6 from its sixth year on, and the endowment year 4 from its fourth.  The flags
    of the guarantee dates are 0 but at each bond's year 10, and at year 0 of every point.
    And on the extract labelled otherwise than by position (:func:`_extract`), where a
    label read as ``idx + 1`` would name another point, the mortality rate refuses an
    attained age below the table, naming the point and the age, on a copy of the table cut
    to start at 20, before it reads the array.
    """
    data = sec_model.Data
    mort = data.mort_table_array()
    first, last = data.mort_age_first(), data.mort_age_last()
    assert mort.shape == (2, last + 1) and (first, last) == (18, 120)
    assert np.isnan(mort[:, :first]).all() and not np.isnan(mort[:, first:]).any()
    lapse, lasts = data.lapse_table_array(), data.lapse_last_year()
    assert lapse.shape == (2, 5) and list(lasts) == [1, 4] and lasts.dtype == np.int64
    assert np.isnan(lapse[:, 0]).all() and np.isnan(lapse[0, 2:]).all()
    assert not np.isnan(lapse[0, 1]) and not np.isnan(lapse[1, 1:]).any()
    bond = _row(sec_model, "twin", 1, 60)
    assert {bond.surr_rate_base(t) for t in range(0, 720, 12)} == {lapse[0, 1]}
    flags, table = data.guarantee_flags(), data.model_point_table()
    assert flags.shape == (len(table), data.guarantee_year_last() + 1) == (24, 123)
    bonds = (table["chassis"] == "UWP_bond").to_numpy()
    assert (flags[bonds, 10] == 1).all() and (flags[~bonds, 10] == 0).all()
    assert flags.sum() == bonds.sum() and (flags[:, 0] == 0).all()
    model = _read_edited(tmp_path / "long", lambda t: t, edits={LAPSE: _bond_lapses_to(6)})
    try:
        array = model.Data.lapse_table_array()
        assert list(model.Data.lapse_last_year()) == [6, 4] and array.shape == (2, 7)
        assert np.isnan(array[1, 5:]).all() and not np.isnan(array[0, 1:]).any()
        assert array[0, 2:].tolist() == pytest.approx([0.06, 0.07, 0.08, 0.09, 0.10])
        bond, endowment = _row(model, "twin", 1, 60), _row(model, "twin", 5, 0)
        assert bond.policy_year(0) == 6 and bond.policy_year(12) == 7
        assert [bond.surr_rate_base(t) for t in (0, 11, 12, 120)] == [array[0, 6]] * 4
        assert [endowment.surr_rate_base(t) for t in (0, 12, 24, 36, 48, 240)] == [
            array[1, 1], array[1, 2], array[1, 3], array[1, 4], array[1, 4], array[1, 4]]
    finally:
        model.close()
    extract = _extract()
    anchor = extract.index[extract["policy_id"] == _committed().at[7, "policy_id"]][0]
    cut = {MORT: _dropped(lambda t: t["age"] < 20)}
    model = mx.read_model(_sec_inputs(tmp_path / "cut", _then(
        _set("age_at_entry", [anchor], 18), _set("wd_rate", [anchor], 0.0))(extract), cut),
        name=_name("padded"))
    try:
        p = _point(model, anchor)
        position = list(extract.index).index(anchor)
        assert p.point_id() == anchor != point_keys(model)[position] + 1
        _refused(lambda: p.mort_rate(0),
                 f"point_id {anchor}: mort_table.csv has no rate at attained age 18")
        assert p.mort_rate(24) == min(
            model.Data.mort_table_array()[p.mort_schedule(), 20] * p.mort_be_factor, 1.0)
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
    vector is of R5's kind, int64 for ages, months, years, terms, codes, flags and
    schedules, float64 for counts, amounts, prices, rates and returns, as the table states
    it: a month held as a float64 reads the same numbers, and compiled reads a double
    through ``int()``, Python arithmetic, which neither C3 nor C5 sees.  Every cell is in
    the table, and every cell the table names is a cell; no ``Data`` cell takes a
    parameter.
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
    assert {"point_id", "chassis_code", "mort_schedule", "lapse_last_year", "age_at_entry",
            "policy_term", "duration_mth_init", "t_entry", "cover_end_mth",
            "fund_exhaust_mth", "is_unitised", "proj_len"} <= set(names)
    found = []
    for key in point_keys(sec_model):
        proj = projection(sec_model, key)
        found += [f"{key}: {name} {type(value).__name__}" for name in names
                  if type(value := proj.cells[name]()) not in (int, float, bool)]
    assert not found, found


# Each label and the refusal its own formula makes of a value that is not its column's
# codes, which Data refuses first as it reads the table: as (the column, the refusal).
LABEL_REFUSALS = {"chassis": ("chassis", "invalid chassis"), "sex": ("sex", "invalid sex"),
                  "tax_basis": ("tax_basis", "invalid tax_basis")}


def test_each_label_refuses_a_value_that_is_not_its_codes():
    """The three labels return text or raise, in either engine.

    Each is a reporting cell, which a reader asks for and no projection cell reads, and the
    registry names them (``"reporting"``).  ``Data`` refuses a value other than the
    column's codes as it reads the table, so a label sees only text; but each refuses any
    other value itself, as ``WP_UK_S``'s ``chassis`` and ``tax_basis`` do and the C step
    makes ``sex`` do, so that compiled each may return ``str`` and still raises where
    modelx raises (``uk_sec_support.labels_refusing_non_text``, C3).  So each is called in
    modelx on the committed model whose table is replaced, past ``Data``'s checks, by one
    holding the first point's column blank, as the number 7 and as a text no code is, and
    must refuse each, with its message; and the harness's own reading,
    ``labels_refusing_non_text``, which C3 asks, finds all three refusing.
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


# The code families, each in its numbering: the count's timings and the asset share's, in
# one numbering, the count's first; the claims' kinds and their total, claim_pp's and
# smoothing_cost_pp's the first four; and the chassis, which index no cache.
TIMING_CODES = (*TIMINGS, *AS_TIMINGS)
CLAIM_CODES = (*CLAIM_KINDS, "ALL")
CHASSIS_CODES = ("UWP_BOND", "CWP_ENDOWMENT")


def test_the_spec_sizes_each_cache_as_its_comment_derives():
    """``spec_sec.py`` gives each cache the size its comment derives from the contract.

    The spec check, C3, holds the compiled caches to the spec, and C4 at the contract's
    extremes holds the spec to the largest argument a projection reads; neither sees a
    size above the comment's.  So this reads the spec as mx2cy does, and derives the two
    bounds the caches hold from the model's shipped References and table: the longest
    cover, from issue at ``issue_age_min`` to a year past the mortality table's last age,
    1,236 months, and the longest frame, that cover issued ``Data.future_horizon_mth``
    months on, 1,356.  It holds each size to the comment's derivation from them: ``t`` to
    the frame's bound + 2 and ``y`` to the cover's bound in years + 2; every 2-D cache to
    one inner width, the widest family's, the timings' 10, since gcc refuses two widths
    and MSVC, which builds the Windows leg, accepts them (USLIB-SEC-PLAN.md §7.2, *Record
    -- M15*); and the codes dense from 0, ints, as the caches index them, each family in
    its own numbering, the count's timings then the asset share's in one, and the
    chassis's too.  And it holds each bound where ``proj_len()`` refuses a point past it,
    by point (:data:`CACHE_EDGES`): the frame's own check and message, the cover's, and the
    exhaustion search's last month, the frame's bound, so that a bound moved without its
    size, or a size without its bound, fails here.  A change to either is derived again in
    the comment, in ``proj_len()`` and here.
    """
    source, comment = _comment("spec_sec.py")
    sizes = ast.literal_eval(source)["spaces"]["Projection"]["cells_param_size"]
    proj, data = _references("Projection"), _references("Data")
    for names in (TIMING_CODES, CLAIM_CODES, CHASSIS_CODES):
        values = [proj[name] for name in names]
        assert values == list(range(len(names))), (names, values)
        assert all(type(v) is int for v in values), (names, values)
    model = mx.read_model(model_path(SEC), name=_name("bounds"))
    try:
        last = model.Data.mort_age_last()
        frame_check = model.Projection.proj_len.formula.source
        search = model.Projection.fund_exhaust_mth.formula.source
    finally:
        model.close()
    cover = 12 * (last + 1 - proj["issue_age_min"])
    frame = cover + data["future_horizon_mth"]
    years = cover // 12
    for text in (f"the frame's bound in proj_len, {frame:,}, + 2",
                 f"the cover's bound in proj_len in years, {cover:,} / 12 = {years}, + 2"):
        assert text in comment, text
    t, width = frame + 2, max(len(TIMING_CODES), len(CLAIM_CODES))
    assert sizes == {"t": t, ("t", "timing"): (t, width), ("t", "kind"): (t, width),
                     "y": cover // 12 + 2}, sizes
    assert len({size[1] for size in sizes.values() if isinstance(size, tuple)}) == 1
    assert (t, width, cover // 12 + 2) == (1358, 10, 105)
    for text in (f"if cover_end_mth() > {cover}:", f"longer than {cover} months",
                 f"if n > {frame}:", f"longer than {frame} months"):
        assert text in frame_check, text
    assert f"cover_end_mth() - duration_mth_init(), {frame + 1}))" in search
    assert f"longer than {frame} months" in _PAST_FRAME
    assert f"longer than {cover} months" in _PAST_COVER


def test_the_sample_raises_the_recursion_limit_its_comment_derives():
    """``sample_sec.py`` sets the recursion limit its comment derives, before the import.

    The export does not raise the recursion limit as modelx does (F7), so the sample sets
    it, and its comment records the measured need: the deepest cold call at the longest
    cover needs the limit the comment states in the export, and the reports and checks the
    sample runs in ascending ``t`` less, from a script's top level (measured at M14).  The
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


def test_the_sample_traces_each_cell_no_report_reaches(sec_model):
    """The sample calls every cell no report reaches, with the bonus rule on, on every row.

    A cell the sample never calls compiles as a Python object with a dict cache, which C3
    fails; a code it never calls is typed all the same, but compared only where C4's
    ``also`` asks it.  ``bonus_supportable`` and ``declaration_month`` are read by the rule
    alone, ``policy_value_pp`` and ``smoothed_payout_capped`` by no cell, ``unit_price`` on
    the endowment by none, ``smoothing_cost_pp`` at ``GUARANTEE``, the count at
    ``AFT_DECR`` and the asset share at ``AFT_MC`` by no flow, and the six refusal cells on
    their chains' error paths alone.  So the sample's source must call each, in its loop
    over every month of every row, and set the rule on in one of its two passes, and the
    committed table must hold an endowment, on which it reads ``unit_price``; and with the
    rule off no report or check reaches ``bonus_supportable`` or ``declaration_month``, on
    a bond and on the endowment, each swept on a model just read, as the sample's
    docstring says.
    """
    source = (model_path(SEC).parent / "sample_sec.py").read_text(encoding="utf-8")
    for call in ("p.policy_value_pp(t)", "p.smoothed_payout_capped(t)", "p.unit_price(t)",
                 "p.bonus_supportable(t)", "p.declaration_month(t)",
                 *(f"p.{refusal}(t)" for _, refusal in REFUSAL_CELLS),
                 "for code in timings:", "for code in as_timings:", "for code in kinds:",
                 "for code in claim_kinds:", "for rule in (False, True):",
                 "for t in range(p.proj_len() + 1):"):
        assert call in source, call
    table = sec_model.Data.model_point_table()
    assert (table["chassis"] == "CWP_endowment").any()
    model = mx.read_model(model_path(SEC), name=_name("unread"))
    try:
        for point in (1, 5):
            p = _point(model, point)
            sweep(p)
            assert not list(p.cells["bonus_supportable"].keys()), point
            assert not list(p.cells["declaration_month"].keys()), point
    finally:
        model.close()


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


# Each code inside the one inner width, 10, that its cell does not take, as (call, arguments,
# the refusal): the asset share's timings in the count's cell, the count's in the asset
# share's, the total and the codes past it in claim_pp and smoothing_cost_pp, and GUARANTEE
# and the codes past the total in the claims.  Each slot of a cache a code leaves unused is
# a code some other cell takes, or none does, so the cell must refuse it itself.
CODES_IN_CACHE = [
    *(("pols_if_at", (0, code), "invalid timing") for code in range(4, 10)),
    *(("asset_share_at", (0, code), "invalid timing") for code in range(4)),
    *((cell, (0, code), "invalid kind") for cell in ("claim_pp", "smoothing_cost_pp")
      for code in range(4, 10)),
    *(("claims", (0, code), "invalid kind") for code in (2, *range(5, 10))),
]


def test_each_code_inside_the_caches_a_cell_does_not_take_is_refused_by_it():
    """Each code inside the one inner width, 10, that its cell does not take, it refuses.

    The two families of timings share one numbering, the count's four first and the asset
    share's six after them, and the kinds another, the total last, in one inner width the
    2-D caches share (``spec_sec.py``): so each timing cell takes four or six codes of the
    ten, a payout's cell four kinds and the claims three and the total.  Compiled, each
    code inside the width is inside the cache, which would hold a value for it, so each
    cell must refuse a code it does not take by its own formula, ``ValueError``, as
    ``WP_UK_S``'s refuse a timing or a kind they do not know: every case of
    :data:`CODES_IN_CACHE`, on point 1, on a model just read.  A code from 10 raises
    ``IndexError`` compiled, which the compiled refusal test holds.
    """
    model = mx.read_model(model_path(SEC), name=_name("codes"))
    try:
        p = _point(model, 1)
        for cell, args, message in CODES_IN_CACHE:
            _refused(lambda: p.cells[cell](*args), message)
    finally:
        model.close()


# What the C step's Data cannot hold, as (case, the table's edit, the message): a point_id
# that is not a whole number below 2**53, which Data.point_id refuses when a refusal first
# names a point, here the worked example's bond in the limiting age's last month moved on
# past its cover, a refusal of proj_len()'s.
NOT_HELD = [
    ("a label with a fraction",
     lambda t: _set("duration_mth", [17], 780)(t).rename(index={17: 17.5}),
     "model_point_table_sec.csv: point_id must be a whole number; [17.5] is not"),
    ("a label of 2**53", lambda t: _set("duration_mth", [17], 780)(t).rename(
        index={17: 2 ** 53}),
     f"model_point_table_sec.csv: point_id must be below 2**53 in size; [{2 ** 53}] is "
     f"not"),
]


@pytest.mark.parametrize("case, edit, message", NOT_HELD, ids=[c[0] for c in NOT_HELD])
def test_a_label_the_vectors_cannot_hold_is_refused(tmp_path, case, edit, message):
    """A label the vectors cannot hold is refused when a refusal first names its point.

    ``Data.point_id`` reads each label by value, and refuses one that is not a whole
    number, or is ``2**53`` or more in size, naming every such label, when a refusal first
    names a point: here the worked example's bond in the limiting age's last month, the
    table's seventeenth row, moved on past its cover, a refusal of ``proj_len()``'s, which
    meets the label's own first (:data:`NOT_HELD`).  A projection that names no point reads
    no label, and runs: the worked example's twin projects its 720 months.
    """
    model = _read_edited(tmp_path, edit)
    try:
        keys = point_keys(model)
        _refused(projection(model, keys[16]).result_cf, message)
        assert len(projection(model, keys[0]).result_cf()) == 720
    finally:
        model.close()


# ---------------------------------------------------------------------------
# C2 -- the Phase 1 fingerprint


def test_the_phase_1_fingerprint_is_reproduced(sec_model):
    """Every committed point computes what the model computed when its E step ended (C2).

    The C step changes how the model is represented and no number it computes
    (UKLIB-SEC-PLAN.md U2, after USLIB-SEC-PLAN.md D2), so before it changed anything the
    model as M13 committed it was frozen below (USLIB-SEC-PLAN.md §5.4): for each point,
    each column of ``result_cf()`` and ``result_pols()``, its sum, its largest absolute value
    and its values at five fixed months, the frame's first and last and the three quartiles
    between.  Every later version must reproduce it, to 1e-12 relative, floored at 1e-12 of
    the column's own magnitude (``uk_sec_support.fingerprint_mismatches``), with the same
    points, frames and columns exactly.  ``python tools/gen_sec_fingerprint.py WP_UK_SEC
    --check`` runs the same comparison from the command line.  Until the freeze, which is
    committed alone, the block is empty and the test skips.
    """
    if not FINGERPRINT:
        pytest.skip("the Phase 1 fingerprint is frozen in a commit of its own")
    assert fingerprint_mismatches(FINGERPRINT, sec_model) == []


# WP_UK_SEC's fingerprint, frozen from the model as M13 committed it and committed alone,
# before its C step changed anything; refrozen once, alone, when M13's review set the bonus
# rate's opening state at the last declaration before the valuation date (D6), which moved
# rows 22 and 23, read from S under the bonus rule.  Each point is keyed by its point_id;
# each column holds (its sum over the frame, its largest absolute value, (its values at
# the months)).
# The block is written by tools/gen_sec_fingerprint.py, and is never edited by hand: a
# refreeze goes through the tool's --force, in a commit of its own that says why.
# BEGIN generated fingerprint: WP_UK_SEC -- tools/gen_sec_fingerprint.py
FINGERPRINT = {
    1: {"rows": 720, "months": (0, 179, 359, 539, 719),
        "result_cf": {
            "pols_if": (169.4171172083074, 1.0, (
                1.0, 0.4038313635650291, 0.10213456329837323, 0.0037186395448912794,
                3.625294576735273e-08)),
            "asset_share": (176374586.1835235, 853080.58288399, (
                30141.85174676119, 68535.89428818191, 158065.41525132974,
                366604.94925883715, 853080.58288399)),
            "premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (34538.47415109776, 110.53392118951682, (
                12.542347857716836, 41.84061362285522, 97.58298290906751, 35.81559557012655,
                0.0022963149171459202)),
            "claims_surrender": (45816.29366312256, 128.54316812413578, (
                126.7772979023175, 117.8742908392414, 68.44695812155966, 5.663535809191134,
                0.00012221462670911797)),
            "claims_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (602.2619035819566, 2.5, (
                2.5, 1.5270779277567301, 0.6017169721006952, 0.03413201902806098,
                5.184173976061588e-07)),
            "shareholder_transfers": (5823.422917167304, 59.99685426412443, (
                1.109545750913014, 40.78972977789695, 23.664367379099772, 4.275842400543021,
                0.003078653470465503)),
            "smoothing_cost": (336.9305005939452, 1.779247197762372, (
                -1.779247197762372, 0.41426350121639083, 0.9661681476145356,
                0.35460985712996695, -0.028508154562619903)),
            "net_cf": (-86780.45263496958, 203.36192406909973, (
                -142.92919151094736, -202.0317121677503, -190.29602538182763,
                -45.78910579888876, -0.005497701431718148)),
        },
        "result_pols": {
            "pols_if": (169.4171172083074, 1.0, (
                1.0, 0.4038313635650291, 0.10213456329837323, 0.0037186395448912794,
                3.625294576735273e-08)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.2867621007050729, 0.0007302774405201529, (
                0.00041762458917626866, 0.0006044475023182451, 0.0006112457592815527,
                9.672806050405982e-05, 2.665139931096325e-09)),
            "pols_surr": (0.7132378658503838, 0.00426353747555846, (
                0.00426353747555846, 0.0017198913367001505, 0.0004330293126597397,
                1.5448607065019356e-05, 1.4326269893044545e-10)),
            "pols_maturity": (3.3444543137325954e-08, 3.3444543137325954e-08, (
                0.0, 0.0, 0.0, 0.0, 3.3444543137325954e-08)),
        },
    },
    2: {"rows": 720, "months": (0, 179, 359, 539, 719),
        "result_cf": {
            "pols_if": (201.52322290891985, 1.0, (
                1.0, 0.4996363890338725, 0.17272240898342225, 0.008595714222110085,
                1.145415671750053e-07)),
            "asset_share": (1768943.7845160055, 29569.19661755969, (
                29569.19661755969, 98.35404368239527, 0.0, 0.0, 0.0)),
            "premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (14833.405383912319, 42.30563733625083, (
                12.472311825577485, 24.20446726331924, 38.84144169773767, 9.753814764251421,
                0.0004264661656424322)),
            "claims_surrender": (6481.4303901316725, 1898.0846006015577, (
                126.0693779011222, 0.14926682251876794, 0.0, 0.0, 0.0)),
            "claims_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (755.4104321084428, 2.5, (
                2.5, 1.8893621705408672, 1.0175791778129444, 0.07889688630668652,
                1.6379452735692369e-06)),
            "shareholder_transfers": (573.2387004204923, 29.278237534487335, (
                1.0231832389936963, 17.61374600389099, 7.069146169120992,
                0.40843302426551836, 6.318625408324828e-06)),
            "smoothing_cost": (15603.807610624901, 1104.6344725924396, (
                0.1234882358968066, 24.155791316463333, 38.84144169773767,
                9.753814764251421, 0.0004264661656424322)),
            "net_cf": (-22643.48490657293, 1941.4871720521248, (
                -142.06487296569338, -43.85684226026987, -46.9281670446716,
                -10.241144674823627, -0.0004344227363243263)),
        },
        "result_pols": {
            "pols_if": (201.52322290891985, 1.0, (
                1.0, 0.4996363890338725, 0.17272240898342225, 0.008595714222110085,
                1.145415671750053e-07)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.41843711609978784, 0.0011381946289203192, (
                0.00041762458917626866, 0.0007478467366990415, 0.0010336935569556834,
                0.00022358896454326296, 8.420537917317777e-09)),
            "pols_surr": (0.5815627780482049, 0.06542861872080553, (
                0.00426353747555846, 0.0012647067076094554, 0.00043523924005326565,
                2.1223744529061893e-05, 2.6902196811862335e-10)),
            "pols_maturity": (1.058520072895689e-07, 1.058520072895689e-07, (
                0.0, 0.0, 0.0, 0.0, 1.058520072895689e-07)),
        },
    },
    3: {"rows": 720, "months": (0, 179, 359, 539, 719),
        "result_cf": {
            "pols_if": (169.4171172083074, 1.0, (
                1.0, 0.4038313635650291, 0.10213456329837323, 0.0037186395448912794,
                3.625294576735273e-08)),
            "asset_share": (78103968.40327853, 269400.362367108, (
                30094.494733263495, 51459.78245760187, 88780.3610286598, 154259.84586906506,
                269400.362367108)),
            "premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (20470.131300646026, 59.804931656201774, (
                12.542347857716836, 31.41578434610107, 54.80928537811607,
                15.070468261615567, 0.0007251695598283631)),
            "claims_surrender": (33984.68405689491, 127.71479683555354, (
                126.7772979023175, 88.50523403730384, 38.44449871392409, 2.3830997447416356,
                3.85950230055519e-05)),
            "claims_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (602.2619035819566, 2.5, (
                2.5, 1.5270779277567301, 0.6017169721006952, 0.03413201902806098,
                5.184173976061588e-07)),
            "shareholder_transfers": (2961.12497779776, 59.70373308512943, (
                1.109545750913014, 36.37965533931487, 15.625183492118106, 1.629157281334553,
                0.0007275282060349471)),
            "smoothing_cost": (199.63440549267875, 1.5575613426778345, (
                -1.5575613426778345, 0.3110473697633776, 0.5426661918625382,
                0.14921255704569922, -0.009002792143766022)),
            "net_cf": (-58018.202238920654, 200.42835873639177, (
                -142.92919151094736, -157.82775165047653, -109.48068455625896,
                -19.116857306719815, -0.0014918112062664683)),
        },
        "result_pols": {
            "pols_if": (169.4171172083074, 1.0, (
                1.0, 0.4038313635650291, 0.10213456329837323, 0.0037186395448912794,
                3.625294576735273e-08)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.2867621007050729, 0.0007302774405201529, (
                0.00041762458917626866, 0.0006044475023182451, 0.0006112457592815527,
                9.672806050405982e-05, 2.665139931096325e-09)),
            "pols_surr": (0.7132378658503838, 0.00426353747555846, (
                0.00426353747555846, 0.0017198913367001505, 0.0004330293126597397,
                1.5448607065019356e-05, 1.4326269893044545e-10)),
            "pols_maturity": (3.3444543137325954e-08, 3.3444543137325954e-08, (
                0.0, 0.0, 0.0, 0.0, 3.3444543137325954e-08)),
        },
    },
    4: {"rows": 343, "months": (0, 85, 171, 256, 342),
        "result_cf": {
            "pols_if": (160.62110991928793, 1.0, (
                1.0, 0.6699706399595071, 0.42291707921182636, 0.2467634982975917,
                0.12124010292555126)),
            "asset_share": (9123444.275571682, 29988.22886203022, (
                29988.22886203022, 28582.8319036891, 26827.016739466948, 24749.429672624752,
                22244.875422131485)),
            "premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (5407.080135521979, 18.179968299045637, (
                12.542347857716836, 15.27762687403602, 17.151713756007375,
                17.556584067882007, 14.844204783538334)),
            "claims_surrender": (18761.47798387899, 127.19004042750915, (
                126.7772979023175, 81.61487786795823, 48.32018272702059, 25.975250045377216,
                11.440752606450287)),
            "claims_maturity": (2670.833000679888, 2670.833000679888, (
                0.0, 0.0, 0.0, 0.0, 2670.833000679888)),
            "withdrawals": (16731.365616592495, 104.16666666666667, (
                104.16666666666667, 69.78860832911533, 44.05386241789858, 25.7045310726658,
                12.629177388078258)),
            "expenses": (543.7517163492223, 2.5, (
                2.5, 2.0599484517204325, 1.59925007120386, 1.147631990947639,
                0.6934714672315075)),
            "shareholder_transfers": (1771.3448394441057, 298.50042893117296, (
                1.1637258674029978, 2.4684307741973885, 3.0265562105242187,
                3.1745083580304034, 298.50042893117296)),
            "smoothing_cost": (52.3280763032691, 1.0601135774846462, (
                -1.0601135774846462, 0.15126363241619922, 0.16981894807928033,
                0.17382756502853425, 0.14697232458948772)),
            "net_cf": (-45885.85329246668, 3008.941035856359, (
                -247.15003829410404, -171.2094922970274, -114.15156518265462,
                -73.55850553490308, -3008.941035856359)),
        },
        "result_pols": {
            "pols_if": (160.62110991928793, 1.0, (
                1.0, 0.6699706399595071, 0.42291707921182636, 0.2467634982975917,
                0.12124010292555126)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.20386121912283656, 0.0007302774405201529, (
                0.00041762458917626866, 0.0005292114963481805, 0.000633014657307942,
                0.0007023497806933496, 0.0006607019450568166)),
            "pols_surr": (0.676073689479858, 0.00426353747555846, (
                0.00426353747555846, 0.0028553810953009327, 0.0018011761500090191,
                0.001049529237197265, 0.0005143095831891175)),
            "pols_maturity": (0.12006509139730534, 0.12006509139730534, (
                0.0, 0.0, 0.0, 0.0, 0.12006509139730534)),
        },
    },
    5: {"rows": 300, "months": (0, 74, 149, 224, 299),
        "result_cf": {
            "pols_if": (219.45588410772675, 1.0, (
                1.0, 0.8264302140841789, 0.7231094375512656, 0.6291983814305998,
                0.5421463661838041)),
            "asset_share": (3633592.409251401, 28339.994028334775, (
                59.32946196259077, 4898.715439514098, 11024.844002764356,
                18700.505634424462, 28339.994028334775)),
            "premiums": (13167.353046463606, 60.0, (
                60.0, 49.58581284505074, 43.386566253075934, 37.75190288583599,
                32.528781971028245)),
            "claims_death": (790.5590946952217, 6.046186882174327, (
                0.8621220165849763, 1.3431683226776394, 2.215837025304588,
                3.6360020957261927, 5.999055210680071)),
            "claims_surrender": (3492.4162720004906, 25.835297545617635, (
                0.2530481597819001, 5.447646344045867, 10.726884624870571,
                16.966174702978318, 25.835297545617635)),
            "claims_maturity": (15700.041761930715, 15700.041761930715, (
                0.0, 0.0, 0.0, 0.0, 15700.041761930715)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (772.8758428611177, 2.818478348155215, (
                2.5, 2.4670022376204175, 2.5774528824248355, 2.677920316565223,
                2.7551798450434024)),
            "shareholder_transfers": (455.851914102742, 25.833325164561504, (
                0.0, 0.0, 0.0, 0.0, 25.833325164561504)),
            "smoothing_cost": (110.21440068679111, 367.45133455460837, (
                0.8595645548154718, -0.3196184718216617, -1.4875003175284685,
                -1.786600719860656, 367.45133455460837)),
            "net_cf": (-8044.3918391266825, 15727.93583772559, (
                56.384829823633126, 40.32799594070681, 27.86639172047594,
                14.471805770566254, -15727.93583772559)),
        },
        "result_pols": {
            "pols_if": (219.45588410772675, 1.0, (
                1.0, 0.8264302140841789, 0.7231094375512656, 0.6291983814305998,
                0.5421463661838041)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.031241627767410764, 0.00021147866348074503, (
                4.310610082924882e-05, 6.141920513710805e-05, 9.266491084674341e-05,
                0.00013906100659879408, 0.0002067291918918717)),
            "pols_surr": (0.4277303549650776, 0.004265134916299351, (
                0.004265134916299351, 0.0013900701141221568, 0.0012162172796028822,
                0.0010581674510826507, 0.0009116197244003331)),
            "pols_maturity": (0.5410280172675118, 0.5410280172675118, (
                0.0, 0.0, 0.0, 0.0, 0.5410280172675118)),
        },
    },
    6: {"rows": 60, "months": (0, 14, 29, 44, 59),
        "result_cf": {
            "pols_if": (56.62892433542358, 1.0, (
                1.0, 0.973038456716396, 0.9445202582486653, 0.9163626302194888,
                0.8885319300776782)),
            "asset_share": (1698712.2151229507, 32710.961238423326, (
                24135.052081366084, 26035.67709702561, 28173.320472061856,
                30413.275329274045, 32710.961238423326)),
            "premiums": (3397.735460125414, 60.0, (
                60.0, 58.38230740298376, 56.67121549491991, 54.98175781316933,
                53.31191580466069)),
            "claims_death": (525.1358718657921, 11.08285372497666, (
                7.13022906530113, 7.7121216827806425, 8.459699587128988, 9.703369325563761,
                11.08285372497666)),
            "claims_surrender": (2691.8322718006575, 48.87238210468561, (
                42.50839643803349, 42.6025496256827, 44.74804032939161, 46.86429909062299,
                48.87238210468561)),
            "claims_maturity": (29004.778288042733, 29004.778288042733, (
                0.0, 0.0, 0.0, 0.0, 29004.778288042733)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (150.11203730150248, 2.5575650981705538, (
                2.5, 2.50557402604472, 2.5051038549400224, 2.5033354695796284,
                2.500126288171827)),
            "shareholder_transfers": (581.1263152864415, 410.7270169124913, (
                0.0, 0.0, 0.09658396327932264, 0.4721270446238948, 410.7270169124913)),
            "smoothing_cost": (13.381685244373683, 2.653448479894922, (
                2.653448479894922, 0.35810809969251767, 0.0, 0.0, 0.0)),
            "net_cf": (-29555.24932417171, 29424.648751268396, (
                7.861374496665377, 5.562062068475704, 0.8617877601799735,
                -4.561373117220948, -29424.648751268396)),
        },
        "result_pols": {
            "pols_if": (56.62892433542358, 1.0, (
                1.0, 0.973038456716396, 0.9445202582486653, 0.9163626302194888,
                0.8885319300776782)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.018073427721947363, 0.0003465955999216059, (
                0.0002650642775204881, 0.00028245908703208904, 0.00030027343051444965,
                0.0003190504547934653, 0.0003388116186557792)),
            "pols_surr": (0.09522752125864065, 0.0016816966768391456, (
                0.0016816966768391456, 0.001636314257044989, 0.0015883126156097259,
                0.0015409158856860823, 0.0014940674396103828)),
            "pols_maturity": (0.886699051019412, 0.886699051019412, (
                0.0, 0.0, 0.0, 0.0, 0.886699051019412)),
        },
    },
    7: {"rows": 267, "months": (0, 66, 133, 199, 266),
        "result_cf": {
            "pols_if": (176.81806443734877, 1.0, (
                1.0, 0.827564674470349, 0.625441879030398, 0.49835313021911354,
                0.3803043087036435)),
            "asset_share": (1199274.6289545007, 24640.835756407596, (
                24640.835756407596, 6737.234607094408, 1338.188286663984, 0.0, 0.0)),
            "premiums": (25000.0, 25000.0, (
                25000.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (1354.0810251266332, 7.052668553253777, (
                6.692873007392325, 6.7075220325920535, 6.01119787686019, 3.9030004283098085,
                0.03002770881997718)),
            "claims_surrender": (3929.288337167024, 811.5831805442349, (
                62.44915909803726, 16.953904912495254, 2.5442421171407967, 0.0, 0.0)),
            "claims_maturity": (15.021465621918319, 15.021465621918319, (
                0.0, 0.0, 0.0, 0.0, 15.021465621918319)),
            "withdrawals": (18314.381712223832, 103.87505823536169, (
                0.0, 86.20465359066135, 65.15019573233313, 51.91178439782433,
                39.61503215662953)),
            "expenses": (584.03253707868, 2.5, (
                2.5, 2.3984356797999866, 2.1643945828085465, 1.999276192519121,
                1.8217559557787364)),
            "shareholder_transfers": (232.68760226987862, 25.812004963477875, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "smoothing_cost": (2123.721536521738, 706.6687026405285, (
                0.16146768011913523, 7.204708055059273, 5.831707535131686,
                3.9030004283098085, 15.051493330738296)),
            "net_cf": (570.5073205120334, 24928.35796789457, (
                24928.35796789457, -112.26451621554865, -75.87003030914266,
                -57.814061018653256, -56.48828144314656)),
        },
        "result_pols": {
            "pols_if": (176.81806443734877, 1.0, (
                1.0, 0.827564674470349, 0.625441879030398, 0.49835313021911354,
                0.3803043087036435)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.12381762946594721, 0.0007560989662605337, (
                0.0002650642775204881, 0.000345611357192472, 0.0004510058118128248,
                0.0005670184462445236, 0.0007493088725334534)),
            "pols_surr": (0.49758956107914054, 0.05588617346461286, (
                0.002534376663007382, 0.002097040539284291, 0.0015843822468133556,
                0.0012619119926369662, 0.00096219037619664)),
            "pols_maturity": (0.3785928094549134, 0.3785928094549134, (
                0.0, 0.0, 0.0, 0.0, 0.3785928094549134)),
        },
    },
    8: {"rows": 709, "months": (0, 177, 354, 531, 708),
        "result_cf": {
            "pols_if": (158.67099906140896, 0.9496956793875818, (
                0.9496956793875818, 0.382946994320866, 0.0957424126107081,
                0.0033718785480403237, 3.625294576735273e-08)),
            "asset_share": (176035074.82568115, 853080.58288399, (
                31685.856551934517, 71508.2510754261, 162603.1313460383, 371829.9325730049,
                853080.58288399)),
            "premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (34399.05523710524, 110.53392118951682, (
                12.692797434046508, 45.36604930830424, 103.37367591103212,
                36.631152449478115, 0.0022963149171459202)),
            "claims_surrender": (44407.05566454699, 128.29803317245984, (
                128.29803317245984, 116.60934932518293, 65.96599525160369,
                5.193012412183797, 0.00012221462670911797)),
            "claims_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (560.0471631497766, 2.3742391984689544, (
                2.3742391984689544, 1.448104221934727, 0.5640581675512807,
                0.030949227902482213, 5.184173976061588e-07)),
            "shareholder_transfers": (5805.781204708521, 59.99685426412443, (
                59.99685426412443, 8.623667012632144, 12.951363938739732, 3.77313724022814,
                0.003078653470465503)),
            "smoothing_cost": (340.55617442752043, 1.0943952593021684, (
                0.1256712617232329, 0.44916880503271606, 1.0235017416933845,
                0.3626846777176006, -0.028508154562619903)),
            "net_cf": (-85171.93926951053, 203.36192406909973, (
                -203.36192406909973, -172.04716986805406, -182.8550932689268,
                -45.62825132979253, -0.005497701431718148)),
        },
        "result_pols": {
            "pols_if": (158.67099906140896, 0.9496956793875818, (
                0.9496956793875818, 0.382946994320866, 0.0957424126107081,
                0.0033718785480403237, 3.625294576735273e-08)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.2822742575287348, 0.0007302774405201529, (
                0.0003966162679467162, 0.0006281356322907926, 0.0006294477438538727,
                9.754047373429136e-05, 2.665139931096325e-09)),
            "pols_surr": (0.6674213884143035, 0.004049063119444907, (
                0.004049063119444907, 0.0016307118069799344, 0.0004056871150360592,
                1.3966095672419282e-05, 1.4326269893044545e-10)),
            "pols_maturity": (3.3444543137325954e-08, 3.3444543137325954e-08, (
                0.0, 0.0, 0.0, 0.0, 3.3444543137325954e-08)),
        },
    },
    9: {"rows": 712, "months": (0, 177, 355, 533, 711),
        "result_cf": {
            "pols_if": (193.65307545689353, 0.963158564303706, (
                0.963158564303706, 0.4873317156907075, 0.16662431897291646,
                0.008088772132651474, 1.145415671750053e-07)),
            "asset_share": (1543945.6624436222, 26336.59611973368, (
                26336.59611973368, 0.0, 0.0, 0.0, 0.0)),
            "premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (14738.177158807302, 42.30563733625083, (
                11.213628672344552, 25.87154512898954, 41.1620725420769, 10.207506784339799,
                0.0004264661656424322)),
            "claims_surrender": (5518.869217390825, 1898.0846006015577, (
                67.27244374870833, 0.0, 0.0, 0.0, 0.0)),
            "claims_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (721.4793571713095, 2.4078964107592653, (
                2.4078964107592653, 1.8428323643744422, 0.9816528063846985,
                0.0742438520895634, 1.6379452735692369e-06)),
            "shareholder_transfers": (568.7999987530537, 29.278237534487335, (
                0.0, 0.0, 0.0, 0.0, 6.318625408324828e-06)),
            "smoothing_cost": (15582.544172443002, 1104.6344725924398, (
                3.6144799728173873, 25.87154512898954, 41.1620725420769, 10.207506784339799,
                0.0004264661656424322)),
            "net_cf": (-21547.325732122492, 1941.4871720521248, (
                -80.89396883181215, -27.71437749336398, -42.1437253484616,
                -10.281750636429361, -0.0004344227363243263)),
        },
        "result_pols": {
            "pols_if": (193.65307545689353, 0.963158564303706, (
                0.963158564303706, 0.4873317156907075, 0.16662431897291646,
                0.008088772132651474, 1.145415671750053e-07)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.41515034900337866, 0.0011381946289203192, (
                0.00040223869972893996, 0.000799354531855272, 0.0010954528801685962,
                0.0002339890522468853, 8.420537917317777e-09)),
            "pols_surr": (0.5480081094483199, 0.06542861872080553, (
                0.002440634088684865, 0.0012333831877424392, 0.0004196237225383792,
                1.991225695996752e-05, 2.6902196811862335e-10)),
            "pols_maturity": (1.058520072895689e-07, 1.058520072895689e-07, (
                0.0, 0.0, 0.0, 0.0, 1.058520072895689e-07)),
        },
    },
    10: {"rows": 688, "months": (0, 171, 343, 515, 687),
        "result_cf": {
            "pols_if": (171.31320729291434, 0.8961698603101973, (
                0.8961698603101973, 0.4512281215841987, 0.14903264413831854,
                0.006680024219897696, 1.145415671750053e-07)),
            "asset_share": (1007423.5965837496, 18498.994909893423, (
                18498.994909893423, 0.0, 0.0, 0.0, 0.0)),
            "premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (14445.034079677229, 42.30563733625083, (
                12.767582647212881, 26.780943566751475, 40.8616620629698, 8.429758117293956,
                0.0004264661656424322)),
            "claims_surrender": (4104.056636075628, 1898.0846006015577, (
                50.40671332305741, 0.0, 0.0, 0.0, 0.0)),
            "claims_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (626.6443833628603, 2.240424650775493, (
                2.240424650775493, 1.7063075506848304, 0.8524397777809044,
                0.05779383096623267, 1.5439205142513306e-06)),
            "shareholder_transfers": (510.99378104453467, 27.782516372204807, (
                0.0, 16.226937896365975, 0.0, 0.0, 6.318625408324828e-06)),
            "smoothing_cost": (15373.950448772217, 1104.6344725924396, (
                12.863469996399001, 26.780943566751475, 40.8616620629698, 8.429758117293956,
                0.0004264661656424322)),
            "net_cf": (-19686.728880160255, 1941.3532248468628, (
                -65.41472062104579, -44.71418901380228, -41.7141018407507,
                -8.487551948260188, -0.00043432871156500835)),
        },
        "result_pols": {
            "pols_if": (171.31320729291434, 0.8961698603101973, (
                0.8961698603101973, 0.4512281215841987, 0.14903264413831854,
                0.006680024219897696, 1.145415671750053e-07)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.40476797701454104, 0.0011381946289203192, (
                0.00044895582589454136, 0.0008111481861268627, 0.0010766910966351672,
                0.00019323730605423018, 8.420537917317777e-09)),
            "pols_surr": (0.4914017774436486, 0.06542861872080553, (
                0.002270696037297476, 0.0011418289240612983, 0.00037507553366720553,
                1.6444320174192843e-05, 2.6902196811862335e-10)),
            "pols_maturity": (1.058520072895689e-07, 1.058520072895689e-07, (
                0.0, 0.0, 0.0, 0.0, 1.058520072895689e-07)),
        },
    },
    11: {"rows": 661, "months": (0, 165, 330, 495, 660),
        "result_cf": {
            "pols_if": (148.03174014557936, 0.8292813643338744, (
                0.8292813643338744, 0.40989745668252614, 0.12947723079120413,
                0.0053071238831693, 1.145415671750053e-07)),
            "asset_share": (594115.2506437511, 12256.78634055271, (
                12256.78634055271, 0.0, 0.0, 0.0, 0.0)),
            "premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (14067.727000443356, 42.30563733625083, (
                14.603313364926773, 29.520069697760913, 39.41500132934523,
                7.537619632574057, 0.0004264661656424322)),
            "claims_surrender": (3102.220712716094, 1898.0846006015577, (
                1898.0846006015577, 0.0, 0.0, 0.0, 0.0)),
            "claims_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (530.8568146793378, 2.073203410834686, (
                2.073203410834686, 1.5048705854908553, 0.7190158730704292,
                0.044578499584826826, 1.4552931607609865e-06)),
            "shareholder_transfers": (456.17012234668215, 26.465849381823666, (
                26.465849381823666, 0.0, 0.0, 0.0, 6.318625408324828e-06)),
            "smoothing_cost": (15029.19781366322, 1104.6344725924396, (
                1104.6344725924396, 29.520069697760913, 39.41500132934523,
                7.537619632574057, 0.0004264661656424322)),
            "net_cf": (-18156.974650185468, 1941.226966759143, (
                -1941.226966759143, -31.02494028325177, -40.13401720241566,
                -7.582198132158884, -0.00043424008421151804)),
        },
        "result_pols": {
            "pols_if": (148.03174014557936, 0.8292813643338744, (
                0.8292813643338744, 0.40989745668252614, 0.12947723079120413,
                0.0053071238831693, 1.145415671750053e-07)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.3916789122775514, 0.0011381946289203192, (
                0.000498404800892447, 0.0008852589613848704, 0.0010282891794969572,
                0.00017107584956513317, 8.420537917317777e-09)),
            "pols_surr": (0.43760234620431554, 0.06542861872080553, (
                0.06542861872080553, 0.0010368658048752765, 0.00032562431138154793,
                1.302013144818689e-05, 2.6902196811862335e-10)),
            "pols_maturity": (1.058520072895689e-07, 1.058520072895689e-07, (
                0.0, 0.0, 0.0, 0.0, 1.058520072895689e-07)),
        },
    },
    12: {"rows": 538, "months": (0, 134, 268, 402, 537),
        "result_cf": {
            "pols_if": (70.87109605804426, 0.4934811579670024, (
                0.4934811579670024, 0.24187055787622683, 0.059498572456221414,
                0.0016419539142302243, 1.145415671750053e-07)),
            "asset_share": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (11692.326706492577, 42.30563733625083, (
                26.19800771750338, 39.49385522414838, 30.77555992493588, 2.97623146606729,
                0.0004264661656424322)),
            "claims_surrender": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (229.9178154784163, 1.233702894917506, (
                1.233702894917506, 0.8370135463582264, 0.2850135437642902,
                0.010887530566172103, 1.0513347430223995e-06)),
            "shareholder_transfers": (222.80313103464377, 16.922008966651656, (
                0.0, 0.0, 0.0, 0.0, 6.318625408324828e-06)),
            "smoothing_cost": (11692.326706492577, 42.30563733625083, (
                26.19800771750338, 39.49385522414838, 30.77555992493588, 2.97623146606729,
                0.0004264661656424322)),
            "net_cf": (-12145.047653005638, 47.96117515853352, (
                -27.431710612420886, -40.33086877050661, -31.06057346870017,
                -2.987118996633462, -0.0004338361257937794)),
        },
        "result_pols": {
            "pols_if": (70.87109605804426, 0.4934811579670024, (
                0.4934811579670024, 0.24187055787622683, 0.059498572456221414,
                0.0016419539142302243, 1.145415671750053e-07)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.3146169475487363, 0.0011381946289203192, (
                0.000809441264143918, 0.0010937334457137241, 0.0007639286792323562,
                6.621836352427482e-05, 8.420537917317777e-09)),
            "pols_surr": (0.17886410456625895, 0.001248946752504123, (
                0.001248946752504123, 0.0006103809550165718, 0.00014889517729104777,
                3.994566223590307e-06, 2.6902196811862335e-10)),
            "pols_maturity": (1.058520072895689e-07, 1.058520072895689e-07, (
                0.0, 0.0, 0.0, 0.0, 1.058520072895689e-07)),
        },
    },
    13: {"rows": 293, "months": (0, 73, 146, 219, 292),
        "result_cf": {
            "pols_if": (2.194633684578459, 0.04347590166475625, (
                0.04347590166475625, 0.010891089179282913, 0.0010684394881920515,
                1.3051479791480757e-05, 3.625294576735273e-08)),
            "asset_share": (51981330.30952366, 269400.36236710794, (
                109318.78747037724, 136873.02447561987, 171479.52605424912,
                214957.5755324661, 269400.36236710794)),
            "premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (4475.041273395681, 52.67544456795697, (
                50.77568524035188, 28.74494704007431, 6.662724478704199,
                0.20831023030836077, 0.000725169559828363)),
            "claims_surrender": (1145.6923570016836, 20.05749050575102, (
                20.05749050575102, 6.236902549441265, 0.7533352288019349,
                0.011086701064708077, 3.859502300555189e-05)),
            "claims_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (6.001726952172051, 0.10868975416189061, (
                0.10868975416189061, 0.03251132511556226, 0.003808348080565443,
                5.554817673780334e-05, 1.842369362442582e-07)),
            "shareholder_transfers": (352.94688789662047, 8.680188033269674, (
                3.8685309746948686, 2.104263785556417, 0.4832604589207778,
                0.015291339558952113, 0.000727528206034947)),
            "smoothing_cost": (44.29832936851095, 0.5215390551282857, (
                0.5027295568351661, 0.2846034360403422, 0.06596756909608074,
                0.0020624775278055723, -0.00900279214376602)),
            "net_cf": (-5979.6822452461565, 76.29070605916863, (
                -74.81039647495966, -37.11862470018756, -7.903128514507476,
                -0.23474381910875877, -0.001491477025805106)),
        },
        "result_pols": {
            "pols_if": (2.194633684578459, 0.04347590166475625, (
                0.04347590166475625, 0.010891089179282913, 0.0010684394881920515,
                1.3051479791480757e-05, 3.625294576735273e-08)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.03426119085621411, 0.0004701194813270156, (
                0.0004598748014575215, 0.0002079324520888584, 3.846964743488487e-05,
                9.594812012075593e-07, 2.665139931096325e-09)),
            "pols_surr": (0.009214677363999009, 0.00018347706711608117, (
                0.00018347706711608117, 4.5567068992124126e-05, 4.39314970210269e-06,
                5.1576228645329115e-08, 1.4326269893044545e-10)),
            "pols_maturity": (3.3444543137325954e-08, 3.3444543137325954e-08, (
                0.0, 0.0, 0.0, 0.0, 3.3444543137325954e-08)),
        },
    },
    14: {"rows": 1, "months": (0,),
        "result_cf": {
            "pols_if": (0.12124010292555126, 0.12124010292555126, (
                0.12124010292555126,)),
            "asset_share": (22244.875422131485, 22244.875422131485, (
                22244.875422131485,)),
            "premiums": (0.0, 0.0, (
                0.0,)),
            "claims_death": (14.844204783538334, 14.844204783538334, (
                14.844204783538334,)),
            "claims_surrender": (11.440752606450287, 11.440752606450287, (
                11.440752606450287,)),
            "claims_maturity": (2670.833000679888, 2670.833000679888, (
                2670.833000679888,)),
            "withdrawals": (12.629177388078258, 12.629177388078258, (
                12.629177388078258,)),
            "expenses": (0.30310025731387813, 0.30310025731387813, (
                0.30310025731387813,)),
            "shareholder_transfers": (298.50042893117296, 298.50042893117296, (
                298.50042893117296,)),
            "smoothing_cost": (0.14697232458948772, 0.14697232458948772, (
                0.14697232458948772,)),
            "net_cf": (-3008.5506646464414, 3008.5506646464414, (
                -3008.5506646464414,)),
        },
        "result_pols": {
            "pols_if": (0.12124010292555126, 0.12124010292555126, (
                0.12124010292555126,)),
            "pols_new_biz": (0.0, 0.0, (
                0.0,)),
            "pols_death": (0.0006607019450568166, 0.0006607019450568166, (
                0.0006607019450568166,)),
            "pols_surr": (0.0005143095831891175, 0.0005143095831891175, (
                0.0005143095831891175,)),
            "pols_maturity": (0.12006509139730534, 0.12006509139730534, (
                0.12006509139730534,)),
        },
    },
    15: {"rows": 289, "months": (0, 72, 144, 216, 288),
        "result_cf": {
            "pols_if": (208.68980103843228, 0.9536171193270517, (
                0.9536171193270517, 0.813458210013106, 0.7152915963778248,
                0.625613525923461, 0.5421463661838041)),
            "asset_share": (3629634.6863595597, 28339.994028334775, (
                711.573273690413, 5558.66663972799, 11564.165008255764, 19019.579193403868,
                28339.994028334775)),
            "premiums": (12521.388062305936, 57.2170271596231, (
                57.2170271596231, 48.80749260078636, 42.91749578266949, 37.53681155540766,
                32.528781971028245)),
            "claims_death": (781.2774174488002, 6.046186882174327, (
                0.8344663286736566, 1.3419166556407778, 2.224758886619155,
                3.6695152767134176, 5.999055210680071)),
            "claims_surrender": (3479.244414199263, 25.835297545617635, (
                2.315348809940276, 6.084520843030568, 11.15094975335672, 17.27629610260413,
                25.835297545617635)),
            "claims_maturity": (15700.041761930715, 15700.041761930715, (
                0.0, 0.0, 0.0, 0.0, 15700.041761930715)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (726.0885708992129, 2.7551798450434024, (
                2.3840427983176293, 2.428279109491297, 2.549586952013167, 2.66266287522742,
                2.7551798450434024)),
            "shareholder_transfers": (455.851914102742, 25.833325164561504, (
                12.400883885055329, 14.635586745483398, 17.805505319315085,
                21.546344513656308, 25.833325164561504)),
            "smoothing_cost": (104.32819019866194, 367.45133455460837, (
                0.22637868592855137, -0.5152635410334949, -1.596777904172529,
                -1.6952336389534113, 367.45133455460837)),
            "net_cf": (-8621.116016274798, 15727.93583772559, (
                39.28228533763621, 24.317189247140316, 9.186694871365361, -7.61800721279362,
                -15727.93583772559)),
        },
        "result_pols": {
            "pols_if": (208.68980103843228, 0.9536171193270517, (
                0.9536171193270517, 0.813458210013106, 0.7152915963778248,
                0.625613525923461, 0.5421463661838041)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.03077754390508969, 0.00021147866348074503, (
                4.110671569820969e-05, 6.045514287812647e-05, 9.166307140484077e-05,
                0.00013826870701563163, 0.0002067291918918717)),
            "pols_surr": (0.38181155815445034, 0.004067305672422613, (
                0.004067305672422613, 0.0013682509757700434, 0.0012030682415312343,
                0.001052138545849513, 0.0009116197244003331)),
            "pols_maturity": (0.5410280172675118, 0.5410280172675118, (
                0.0, 0.0, 0.0, 0.0, 0.5410280172675118)),
        },
    },
    16: {"rows": 1, "months": (0,),
        "result_cf": {
            "pols_if": (0.5421463661838041, 0.5421463661838041, (
                0.5421463661838041,)),
            "asset_share": (28339.994028334775, 28339.994028334775, (
                28339.994028334775,)),
            "premiums": (32.528781971028245, 32.528781971028245, (
                32.528781971028245,)),
            "claims_death": (5.999055210680071, 5.999055210680071, (
                5.999055210680071,)),
            "claims_surrender": (25.835297545617635, 25.835297545617635, (
                25.835297545617635,)),
            "claims_maturity": (15700.041761930715, 15700.041761930715, (
                15700.041761930715,)),
            "withdrawals": (0.0, 0.0, (
                0.0,)),
            "expenses": (1.3553659154595101, 1.3553659154595101, (
                1.3553659154595101,)),
            "shareholder_transfers": (25.833325164561504, 25.833325164561504, (
                25.833325164561504,)),
            "smoothing_cost": (367.45133455460837, 367.45133455460837, (
                367.45133455460837,)),
            "net_cf": (-15726.536023796005, 15726.536023796005, (
                -15726.536023796005,)),
        },
        "result_pols": {
            "pols_if": (0.5421463661838041, 0.5421463661838041, (
                0.5421463661838041,)),
            "pols_new_biz": (0.0, 0.0, (
                0.0,)),
            "pols_death": (0.0002067291918918717, 0.0002067291918918717, (
                0.0002067291918918717,)),
            "pols_surr": (0.0009116197244003331, 0.0009116197244003331, (
                0.0009116197244003331,)),
            "pols_maturity": (0.5410280172675118, 0.5410280172675118, (
                0.5410280172675118,)),
        },
    },
    17: {"rows": 1, "months": (0,),
        "result_cf": {
            "pols_if": (3.625294576735273e-08, 3.625294576735273e-08, (
                3.625294576735273e-08,)),
            "asset_share": (853080.58288399, 853080.58288399, (
                853080.58288399,)),
            "premiums": (0.0, 0.0, (
                0.0,)),
            "claims_death": (0.0022963149171459202, 0.0022963149171459202, (
                0.0022963149171459202,)),
            "claims_surrender": (0.00012221462670911797, 0.00012221462670911797, (
                0.00012221462670911797,)),
            "claims_maturity": (0.0, 0.0, (
                0.0,)),
            "withdrawals": (0.0, 0.0, (
                0.0,)),
            "expenses": (9.063236441838182e-08, 9.063236441838182e-08, (
                9.063236441838182e-08,)),
            "shareholder_transfers": (0.003078653470465503, 0.003078653470465503, (
                0.003078653470465503,)),
            "smoothing_cost": (-0.028508154562619903, 0.028508154562619903, (
                -0.028508154562619903,)),
            "net_cf": (-0.0054972736466849595, 0.0054972736466849595, (
                -0.0054972736466849595,)),
        },
        "result_pols": {
            "pols_if": (3.625294576735273e-08, 3.625294576735273e-08, (
                3.625294576735273e-08,)),
            "pols_new_biz": (0.0, 0.0, (
                0.0,)),
            "pols_death": (2.665139931096325e-09, 2.665139931096325e-09, (
                2.665139931096325e-09,)),
            "pols_surr": (1.4326269893044545e-10, 1.4326269893044545e-10, (
                1.4326269893044545e-10,)),
            "pols_maturity": (3.3444543137325954e-08, 3.3444543137325954e-08, (
                3.3444543137325954e-08,)),
        },
    },
    18: {"rows": 167, "months": (0, 41, 83, 124, 166),
        "result_cf": {
            "pols_if": (89.75438761041644, 0.7469373079710191, (
                0.7469373079710191, 0.6093430388420875, 0.5280767516172314,
                0.4531650055469536, 0.3803043087036435)),
            "asset_share": (104772.51463218611, 3174.45925499511, (
                3174.45925499511, 1055.1981639950159, 122.6254307875541, 0.0, 0.0)),
            "premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (688.344710851558, 6.870532020715113, (
                6.707101500516318, 5.486644204787155, 4.656130673302279, 2.70528979330252,
                0.030027708819978894)),
            "claims_surrender": (1007.5655292128696, 811.583180544235, (
                7.209133718284143, 1.95456508522824, 0.1967858561762404, 0.0, 0.0)),
            "claims_maturity": (15.021465621919177, 15.021465621919177, (
                0.0, 0.0, 0.0, 0.0, 15.021465621919177)),
            "withdrawals": (9349.415376085048, 77.8059695803145, (
                77.8059695803145, 63.47323321271745, 55.00799496012828, 47.20468807780767,
                39.61503215662953)),
            "expenses": (267.5266969207925, 1.8673432699275478, (
                1.8673432699275478, 1.6646139770119943, 1.5763781450303238,
                1.5225396837503025, 1.3962242467554797)),
            "shareholder_transfers": (75.38897178958699, 12.652040154537953, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "smoothing_cost": (1391.5352948073523, 706.6687026405286, (
                6.6075699729238355, 5.348754201035283, 4.621679191353547, 2.70528979330252,
                15.051493330739156)),
            "net_cf": (-11403.262750481772, 904.8343482868709, (
                -93.58954806904251, -72.57905647974485, -61.437289634637125,
                -51.43251755486049, -56.06274973412417)),
        },
        "result_pols": {
            "pols_if": (89.75438761041644, 0.7469373079710191, (
                0.7469373079710191, 0.6093430388420875, 0.5280767516172314,
                0.4531650055469536, 0.3803043087036435)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.09138336826370519, 0.0007560989662605337, (
                0.00040985053184284045, 0.0004393969465740117, 0.0005484109145457757,
                0.0006189973441556425, 0.0007493088725334534)),
            "pols_surr": (0.27696113025240193, 0.05588617346461286, (
                0.0018924833961722108, 0.0015436003333473324, 0.0013373099888579112,
                0.0011472261307918293, 0.00096219037619664)),
            "pols_maturity": (0.3785928094549134, 0.3785928094549134, (
                0.0, 0.0, 0.0, 0.0, 0.3785928094549134)),
        },
    },
    19: {"rows": 280, "months": (0, 69, 139, 209, 279),
        "result_cf": {
            "pols_if": (176.81806443734877, 1.0, (
                0.0, 0.8522686211246088, 0.6396357057558408, 0.5038804417143988,
                0.3803043087036435)),
            "asset_share": (1199274.6289545004, 24640.835756407596, (
                0.0, 8289.073986085017, 1641.51754128338, 0.0, 0.0)),
            "premiums": (25000.0, 25000.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (1354.0810251266334, 7.052668553253777, (
                0.0, 6.584282154169498, 5.865987254250775, 4.127239336267641,
                0.03002770881997718)),
            "claims_surrender": (3929.2883371670246, 811.5831805442349, (
                0.0, 21.48248008865471, 3.191977122334086, 0.0, 0.0)),
            "claims_maturity": (15.021465621918319, 15.021465621918319, (
                0.0, 0.0, 0.0, 0.0, 15.021465621918319)),
            "withdrawals": (18314.381712223832, 103.87505823536169, (
                0.0, 88.77798136714675, 66.62871934956675, 52.48754601191655,
                39.61503215662953)),
            "expenses": (603.0165171378162, 2.575, (
                0.0, 2.4700322920229207, 2.213513522079926, 2.082093987589221,
                1.8764086344520987)),
            "shareholder_transfers": (232.68760226987862, 25.812004963477875, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "smoothing_cost": (2123.721536521738, 706.6687026405285, (
                0.0, 7.4708804786375325, 5.706774365982206, 4.127239336267641,
                15.051493330738296)),
            "net_cf": (551.523340452899, 24928.28296789457, (
                0.0, -119.31477590199388, -77.90019724823154, -58.69687933577341,
                -56.542934121819926)),
        },
        "result_pols": {
            "pols_if": (176.81806443734877, 1.0, (
                0.0, 0.8522686211246088, 0.6396357057558408, 0.5038804417143988,
                0.3803043087036435)),
            "pols_new_biz": (1.0, 1.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.12381762946594721, 0.0007560989662605337, (
                0.0, 0.0003249838315067795, 0.0004210793110281634, 0.0005733073353593331,
                0.0007493088725334534)),
            "pols_surr": (0.4975895610791405, 0.05588617346461286, (
                0.0, 0.0021597185367868642, 0.0016204401527130585, 0.0012759080533416996,
                0.00096219037619664)),
            "pols_maturity": (0.3785928094549134, 0.3785928094549134, (
                0.0, 0.0, 0.0, 0.0, 0.3785928094549134)),
        },
    },
    20: {"rows": 207, "months": (0, 51, 103, 154, 206),
        "result_cf": {
            "pols_if": (121.56474856351588, 0.8423731906178802, (
                0.8423731906178802, 0.7233703890711242, 0.5661353151886602,
                0.47109924637740774, 0.3803043087036435)),
            "asset_share": (310863.90256773337, 7581.623646555877, (
                7581.623646555877, 2421.185264822468, 456.535326787749, 0.0, 0.0)),
            "premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (957.8349772286516, 7.052668553253777, (
                7.049618102535108, 6.679408780046974, 5.097818731558662, 3.153626912747302,
                0.03002770881997718)),
            "claims_surrender": (1510.4503059101553, 811.5831805442349, (
                19.420163720321295, 4.247797388659016, 0.7855723976731147, 0.0, 0.0)),
            "claims_maturity": (15.021465621918319, 15.021465621918319, (
                0.0, 0.0, 0.0, 0.0, 15.021465621918319)),
            "withdrawals": (12662.994642032907, 87.7472073560292, (
                87.7472073560292, 75.35108219490877, 58.972428665485445, 49.07283816431331,
                39.61503215662953)),
            "expenses": (377.5256413680194, 2.1059329765447004, (
                2.1059329765447004, 2.0353993644816955, 1.7929081982448574,
                1.679187198269049, 1.5714626904589062)),
            "shareholder_transfers": (121.96641885535044, 17.03227133822366, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "smoothing_cost": (1669.7946375249444, 707.066870727297, (
                7.6191290208517835, 6.3347612094172945, 5.005100926611342,
                3.153626912747302, 15.051493330738296)),
            "net_cf": (-15645.793451017002, 905.0034788018194, (
                -116.32292215543029, -88.31368772809645, -66.64872799296208,
                -53.90565227532966, -56.237988177826736)),
        },
        "result_pols": {
            "pols_if": (121.56474856351588, 0.8423731906178802, (
                0.8423731906178802, 0.7233703890711242, 0.5661353151886602,
                0.47109924637740774, 0.3803043087036435)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.10621604101726997, 0.0007560989662605337, (
                0.00035179575766489487, 0.0004347514489561509, 0.0004898778358872041,
                0.0005872812393119208, 0.0007493088725334534)),
            "pols_surr": (0.35756434014569793, 0.05588617346461286, (
                0.0021345651698612233, 0.0014620240791343995, 0.0014339386818841943,
                0.0011927707050169059, 0.00096219037619664)),
            "pols_maturity": (0.3785928094549134, 0.3785928094549134, (
                0.0, 0.0, 0.0, 0.0, 0.3785928094549134)),
        },
    },
    21: {"rows": 480, "months": (0, 119, 239, 359, 479),
        "result_cf": {
            "pols_if": (28.6500921718857, 0.27572723369715557, (
                0.27572723369715557, 0.10213456329837323, 0.017403362825692808,
                0.0003137605684771608, 3.625294576735273e-08)),
            "asset_share": (67075486.01632072, 267624.7803558709, (
                61237.77383401564, 88086.91016781736, 127372.08695461274,
                184489.86938433343, 267624.7803558709)),
            "premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (14278.086479081943, 59.357067092496074, (
                44.26723548380635, 54.38117779117639, 34.99066465929942, 2.649778190070447,
                0.000720390063564088)),
            "claims_surrender": (9690.346473770398, 71.83263033977693, (
                71.83263033977693, 38.14421416429019, 9.307174755554009,
                0.23571048789047186, 3.834064833444973e-05)),
            "claims_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (87.14580290765875, 0.689318084242889, (
                0.689318084242889, 0.33315609833456994, 0.07629225514687338,
                0.0018484933320479287, 2.870351436029068e-07)),
            "shareholder_transfers": (1390.8976537507592, 27.481017498576293, (
                4.243894240841087, 15.544721997940997, 4.857616077510558, 0.240545439563992,
                0.0007203759751061843)),
            "smoothing_cost": (141.35824227368627, 0.5876937335890685, (
                0.43828946023570464, 0.5384275028829392, 0.3464422243495,
                0.026235427624459913, -0.008943455936342534)),
            "net_cf": (-25446.476409510757, 139.42212136793006, (
                -121.03307814866726, -108.40327005174214, -49.23174774751086,
                -3.1278826108569584, -0.001479393722148325)),
        },
        "result_pols": {
            "pols_if": (28.6500921718857, 0.27572723369715557, (
                0.27572723369715557, 0.10213456329837323, 0.017403362825692808,
                0.0003137605684771608, 3.625294576735273e-08)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.1541830640513052, 0.0007302774405201529, (
                0.0007157174939501974, 0.0006112457592815527, 0.0002719922650501511,
                1.4220524797383665e-05, 2.665139931096325e-09)),
            "pols_surr": (0.12154413620130745, 0.0011730117841069554, (
                0.0011730117841069554, 0.0004330293126597397, 7.307075653765876e-05,
                1.277633772938689e-06, 1.4326269893044545e-10)),
            "pols_maturity": (3.3444543137325954e-08, 3.3444543137325954e-08, (
                0.0, 0.0, 0.0, 0.0, 3.3444543137325954e-08)),
        },
    },
    22: {"rows": 630, "months": (0, 157, 314, 471, 629),
        "result_cf": {
            "pols_if": (95.82133253134698, 0.6532178000042325, (
                0.6532178000042325, 0.2627747414618228, 0.060094329289545265,
                0.0017260190109812433, 4.5117876966103824e-08)),
            "asset_share": (103411577.03625713, 411827.1191117323, (
                44828.85279539066, 87849.61869237697, 171564.63318496157,
                333549.28197779326, 0.0)),
            "premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (29537.859275599396, 97.30366173013704, (
                23.362026296483148, 60.521103907520875, 90.94773012390164,
                18.74374808543255, 0.0023042255844270268)),
            "claims_surrender": (32264.677243578328, 124.80268949203594, (
                124.80268949203594, 98.20785141043015, 43.59161891569407, 2.376440422127904,
                0.0)),
            "claims_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (321.1510635240652, 1.633044500010581, (
                1.633044500010581, 0.9647339172005137, 0.32399726443684373,
                0.013665871950314774, 5.24595244012782e-07)),
            "shareholder_transfers": (4137.743415812702, 151.13264760249294, (
                2.8134388408281126, 2.366538457619104, 1.3883769438737437,
                0.10714651847189918, 0.00018473687967170144)),
            "smoothing_cost": (302.98147197777183, 0.9634025913874924, (
                0.23130719105428732, 0.5992188505695165, 0.9004725754841791,
                0.18558166421220293, 0.0023042255844270268)),
            "net_cf": (-66261.4309985145, 299.87932214147816, (
                -152.61119912935777, -162.06022769277064, -136.2517232479063,
                -21.24100089798267, -0.002489487059342741)),
        },
        "result_pols": {
            "pols_if": (95.82133253134698, 0.6532178000042325, (
                0.6532178000042325, 0.2627747414618228, 0.060094329289545265,
                0.0017260190109812433, 4.5117876966103824e-08)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.2455787211843951, 0.0007302774405201529, (
                0.0005159783858624011, 0.0006820961314218089, 0.0005248590917414703,
                5.5638454117421535e-05, 3.3168464786367896e-09)),
            "pols_surr": (0.407639037124774, 0.0027839813358968724, (
                0.0027839813358968724, 0.0011179086815883016, 0.00025408277980403177,
                7.1247055548634656e-06, 1.0596764439419843e-10)),
            "pols_maturity": (4.1695062843072834e-08, 4.1695062843072834e-08, (
                0.0, 0.0, 0.0, 0.0, 4.1695062843072834e-08)),
        },
    },
    23: {"rows": 150, "months": (0, 37, 74, 111, 149),
        "result_cf": {
            "pols_if": (94.46124186628127, 0.721800555360816, (
                0.721800555360816, 0.6745068393906527, 0.6291983814305998,
                0.5855618581059508, 0.5421463661838041)),
            "asset_share": (2917538.3597850446, 29047.50825167064, (
                11253.97220649939, 14915.588082474042, 19033.753216575158,
                23680.521589141368, 29047.50825167064)),
            "premiums": (5667.674511976877, 43.30803332164896, (
                43.30803332164896, 40.470410363439164, 37.75190288583599, 35.13371148635705,
                32.528781971028245)),
            "claims_death": (521.9541407684952, 6.004967907340347, (
                2.0434120910603233, 2.554439533530583, 3.18784680839438, 3.96938026330924,
                6.004967907340347)),
            "claims_surrender": (2666.671564804548, 26.48028146690439, (
                10.930000375155704, 13.720909259295299, 17.170726627382468,
                21.43735554293309, 26.48028146690439)),
            "claims_maturity": (15715.515795963054, 15715.515795963054, (
                0.0, 0.0, 0.0, 0.0, 15715.515795963054)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (279.1125151843157, 1.952482875990099, (
                1.80450138840204, 1.8426295877170744, 1.8782394307988437,
                1.9100635248246751, 1.932427709626635)),
            "shareholder_transfers": (418.49475073433734, 316.82891799110024, (
                0.0, 0.0, 0.0, 0.0, 316.82891799110024)),
            "smoothing_cost": (-287.06437476477197, 2.477622897523966, (
                -1.730048700402398, -2.3383530577429448, -2.4291775715926653,
                -1.9369915969433973, 0.0)),
            "net_cf": (-13934.074255477875, 16034.233609067, (
                28.530119467030897, 22.35243198289621, 15.515090019260297,
                7.816912155290044, -16034.233609067)),
        },
        "result_pols": {
            "pols_if": (94.46124186628127, 0.721800555360816, (
                0.721800555360816, 0.6745068393906527, 0.6291983814305998,
                0.5855618581059508, 0.5421463661838041)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.021912122879724705, 0.00021147866348074503, (
                9.249718042422586e-05, 0.00011351045314700465, 0.00013906100659879408,
                0.0001699801962602467, 0.0002067291918918717)),
            "pols_surr": (0.15886041521357985, 0.001214015835320285, (
                0.001214015835320285, 0.001134425715889475, 0.0010581674510826507,
                0.00098471258786002, 0.0009116197244003331)),
            "pols_maturity": (0.5410280172675118, 0.5410280172675118, (
                0.0, 0.0, 0.0, 0.0, 0.5410280172675118)),
        },
    },
    24: {"rows": 624, "months": (0, 155, 311, 467, 623),
        "result_cf": {
            "pols_if": (91.95079018351181, 0.6336664272907219, (
                0.6336664272907219, 0.255648365055038, 0.05778766270402682,
                0.0016027749458801008, 3.625294576735273e-08)),
            "asset_share": (172748584.91998482, 853080.58288399, (
                46760.54478803456, 95654.09982820188, 197732.94968756658, 410239.6701781786,
                853080.58288399)),
            "premiums": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims_death": (32818.122737446276, 110.53392118951682, (
                24.32962497834793, 64.1106162381628, 100.79634403569351, 21.407258490503043,
                0.0022963149171459202)),
            "claims_surrender": (33787.46948354499, 124.99852895853245, (
                118.63751279830822, 104.03256825865974, 48.31209983265328,
                2.7141356238835836, 0.00012221462670911797)),
            "claims_maturity": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "withdrawals": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (306.97222546050006, 1.5841660682268046, (
                1.5841660682268046, 0.911233599204117, 0.3024863319399836,
                0.012320464807074572, 4.0924348089930086e-07)),
            "shareholder_transfers": (5087.534210533127, 48.13839653897991, (
                4.184521240420621, 33.7728641542107, 18.766071152464868, 2.4477103025925677,
                0.003078653470465503)),
            "smoothing_cost": (232.44088288797477, 8.946799489834458, (
                -8.946799489834458, 0.6347585766154694, 0.9979836043137978,
                0.21195305436141584, -0.028508154562619903)),
            "net_cf": (-72000.09865698489, 202.82728225023735, (
                -148.7358250853036, -202.82728225023735, -168.17700135275163,
                -26.58142488178627, -0.005497592257801441)),
        },
        "result_pols": {
            "pols_if": (91.95079018351181, 0.6336664272907219, (
                0.6336664272907219, 0.255648365055038, 0.05778766270402682,
                0.0016027749458801008, 3.625294576735273e-08)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.24250130724427826, 0.0007302774405201529, (
                0.0005483126202295124, 0.0006635978779325946, 0.0005047128492700325,
                5.166566516333223e-05, 2.665139931096325e-09)),
            "pols_surr": (0.3911650866018999, 0.0027004505829178447, (
                0.0027004505829178447, 0.001087591315432437, 0.0002443300416495589,
                6.6159755410898185e-06, 1.4326269893044545e-10)),
            "pols_maturity": (3.3444543137325954e-08, 3.3444543137325954e-08, (
                0.0, 0.0, 0.0, 0.0, 3.3444543137325954e-08)),
        },
    },
}
# END generated fingerprint: WP_UK_SEC


# ---------------------------------------------------------------------------
# Compiled (UKLIB-SEC-PLAN.md U2, the C step, after USLIB-SEC-PLAN.md's Phase 2)
#
# These compile the model, once a session, into a temporary directory (conftest.sec_build),
# and run the compiled package in a child process only.  They skip without modelx-cython or
# a C compiler, and the cython_uk CI job, which sets UKLIB_REQUIRE_CYTHON=1, fails a skip.
# test_compiled_conventions_uk.py checks the compiled model's types, its caches and its
# release, and compares it with modelx on the committed points; these hold what is WP's
# own: the comparison on the splice grid under each of its sets of References, at the
# contract's extremes, where the caps and bounds the grid leaves bind, on every value a
# decoded column holds, on keys written as floats, on the committed rows under the
# References they were read from, on the declarations the rule makes in the frame and on
# the bonds whose units run out; the labels; the refusals and the overflows; the deepest
# calls on a 1 MiB stack; a Reference set late; and the runner.


def _as_modelx(have, want):
    """Whether a compiled value is modelx's: identical where ``exact_here()``, as on
    x86-64, and to 1e-12 relative elsewhere, as C4 compares (uk_sec_support)."""
    return have == want if exact_here() else have == pytest.approx(want, rel=1e-12, abs=0)


def _mismatch_lines(found):
    return f"{len(found)} mismatches, first:\n  " + "\n  ".join(found[:50])


# The cells of a timing or a kind, each with the codes it takes, by name: the harness's,
# which its _wp_c4_also, the spec's c4_also, asks at every code in every month of every
# row.  test_the_c4_comparisons_ask_every_code_and_their_rows holds both to modelx, row by
# row.
CODED = _WP_CODED


class _Asked:
    """A stand-in for a point, which records what :func:`_wp_c4_also` asks of each cell of
    :data:`CODED`, as (month, code), and hands every other read to the point itself."""

    def __init__(self, proj):
        self._proj, self.asked = proj, {}
        self.cells = {name: self._cell(name) for name in CODED}

    def _cell(self, name):
        return lambda t, code: self.asked.setdefault(name, set()).add((t, code))

    def __getattr__(self, name):
        return getattr(self._proj, name)


# The committed rows each set of References a committed row was read under (the spec's
# derived_refs) moves, which the comparison under that set reads by default: each set's own
# rows, the rows read under it.  Every set moves every row, the charge, the rule and the cap
# reaching every point, so the default compares the rows the set was read for and the full
# grid the whole committed table, as the cython_uk job's Linux legs run it (UKLIB_SEC_FULL=1).
# A test holds the selection to the spec's own rows (test_the_c4_comparisons_ask_every_code_
# and_their_rows).
OWN_REFS_ROWS = {"guar_charge_rate_base": (20, 21), "bonus_rule_on": (22, 23),
                 "smooth_cap": (24,)}

# The rows of the rule's declarations in the frame, by default (DECLARED's, the bond valued
# on its declaration, the down scenario's valued mid-year, whose year closes at t = 3, the
# endowment valued on its declaration and the 5% bond in force, whose steps no clamp holds),
# and on the full grid every committed row; and the rows whose units run out, by default the
# withdrawing bond and the bond variant in force, and on the full grid every committed
# withdrawing bond: each held in modelx, by its test, to be what it is said to be.
DECLARING_ROWS = (8, 9, 15, 3)
EXHAUSTED_ROWS = (4, 18)


def _c4_rows(labels):
    """The committed table under ``UKLIB_SEC_FULL=1``, and its rows ``labels`` otherwise."""
    rows = _committed()
    return rows if SEC_FULL else rows.loc[list(labels)]


def test_the_c4_comparisons_ask_every_code_and_their_rows(sec_model, spliced):
    """C4's ``also`` asks every code on every row, and each default selection is what
    modelx says of the committed rows.

    Nothing in a comparison shows what it leaves out: dropped from :func:`_wp_c4_also`, a
    code is simply not compared, and dropped from a selection, a row.  So what each cell of
    :data:`CODED` takes is first derived in modelx, not read from :data:`CODED`: on a fresh
    read of the committed model, each such cell is asked every code in the caches' one
    inner width, 0 to 9, on every committed row in its first month on the books, and the
    codes it takes are those it does not refuse, ``invalid timing`` or ``invalid kind``,
    the same on every row; :data:`CODED` must name exactly those, by the model's own
    References.  Then :func:`_wp_c4_also` is run on a stand-in of each row C4 compares here
    (:class:`_Asked`): every committed row, and every row of the splice grid this run
    selects under each of its sets, the twins, the rows restated in force and the future
    rows, both chassis, the one-row frames and the exhausted bonds among them.  On each
    row, one at a time, it must ask every cell of :data:`CODED` at every code that cell
    takes, in every month of the frame and the month after it, and no other: a code left
    out on one kind of row fails here, where a union over the rows would pass it, and a
    code left out of :data:`CODED` fails above.  It must be the spec's ``c4_also``, which
    the conventions' C4 on the committed points passes (``uk_sec_support.spec_c4_also``).
    And each default selection is derived in modelx from the committed rows: the rows of
    :data:`OWN_REFS_ROWS` are those the spec's ``derived_refs`` read under each set; the
    rows of :data:`DECLARING_ROWS` declare in their frame under the rule, one valued on its
    declaration month and one mid-year; and the rows of :data:`EXHAUSTED_ROWS` end their
    frames by the units' exhaustion.
    """
    found, rows = [], 0
    width = max(len(TIMING_CODES), len(CLAIM_CODES))
    fresh = mx.read_model(model_path(SEC), name=_name("codes"))
    try:
        for key, label in zip(point_keys(fresh), fresh.Data.model_point_table().index):
            p = projection(fresh, key)
            for cell, names in CODED.items():
                takes = set()
                for code in range(width):
                    try:
                        p.cells[cell](p.t_entry(), code)
                    except Exception as err:    # a code the cell does not take
                        if not re.search(r"ValueError: invalid (timing|kind)", str(err)):
                            found.append(f"row {label}: {cell}({p.t_entry()}, {code}) "
                                         f"raised {_raised(err)}")
                        continue
                    takes.add(code)
                coded = {_code(p, n) for n in names}
                if takes != coded:
                    found.append(f"row {label}: {cell} takes {sorted(takes)} in modelx, "
                                 f"CODED names {sorted(coded)}")
    finally:
        fresh.close()
    assert not found, found[:10]
    models = [("committed", sec_model)] + [(name, pair[1]) for name, pair in spliced.items()]
    for name, model in models:
        keys = point_keys(model)
        for key, label in zip(keys, model.Data.model_point_table().index):
            p = projection(model, key)
            stand_in = _Asked(p)
            _wp_c4_also(stand_in)
            months = range(p.proj_len() + 1)
            for cell, names in CODED.items():
                want = {(t, _code(p, n)) for t in months for n in names}
                if stand_in.asked.get(cell) != want:
                    found.append(f"{name} row {label}: {cell} asked "
                                 f"{len(stand_in.asked.get(cell, ()))} of {len(want)}")
            rows += 1
            if name != "committed":
                _release(model, key)
    assert rows > len(sec_model.Data.model_point_table()) and not found, (
        rows, found[:10])
    assert SPEC.c4_also is _wp_c4_also, SPEC.c4_also
    table = sec_model.Data.model_point_table()
    own = {}
    for (s_point, month), refs in SPEC.derived_refs.items():
        (ref,) = refs
        own.setdefault(ref, []).append(_label(table, "derived", s_point, month))
    assert {ref: tuple(sorted(labels)) for ref, labels in own.items()} == OWN_REFS_ROWS
    declared = [_label(table, *case) for case, _ in DECLARED]
    assert tuple(declared) == DECLARING_ROWS
    for label in DECLARING_ROWS:
        p = _point(sec_model, label)
        assert p.declaration_month(0) < p.proj_len(), label
    exhausted = sorted(label for label, key in zip(table.index, point_keys(sec_model))
                       if projection(sec_model, key).is_forced_encashment())
    assert set(EXHAUSTED_ROWS) <= set(exhausted), exhausted
    assert {table.at[label, "chassis"] for label in EXHAUSTED_ROWS} == {"UWP_bond"}


# How many months of frame C4 compares at once.  compiled_mismatches sweeps every row of its
# case in one modelx read and keeps every value of every row, in the parent and in the
# child, until it compares them, and the record of a row grows with its frame, a hundred
# cells a month and the dependencies between them.  So the rows of a case are taken in
# chunks of at most this many months of frame between them, each the frame proj_len()
# gives the row at the References the comparison sets, so that a chunk of the longest
# covers holds as much as one of the committed rows (measured at M14).
C4_MONTHS = 6000


def _frames(table, refs, root):
    """``proj_len()`` of each row of ``table``, read under ``refs`` from a copy in
    ``root``, in table order, a ``"Data.<name>"`` Reference set on ``Data``."""
    model = mx.read_model(_sec_inputs(root, table), name=_name("frames"))
    try:
        _set_refs(model, refs or {})
        return [projection(model, key).proj_len() for key in point_keys(model)]
    finally:
        model.close()


def _c4_chunks(build, table, refs, root, months=C4_MONTHS):
    """C4 on ``table`` under ``refs``, its rows in chunks of at most ``months`` months of
    frame between them, each row with :func:`_wp_c4_also`: the mismatch lines.  Each
    chunk's case is read back, and the rows each compared must be its own, every row of
    the table once, in order."""
    frames = _frames(table, refs, root / "frames")
    chunks, chunk, held = [], [], 0
    for position, frame in enumerate(frames):
        if chunk and held + frame > months:
            chunks.append(chunk)
            chunk, held = [], 0
        chunk.append(position)
        held += frame
    chunks.append(chunk)
    labels = list(table["point_id"] if "point_id" in table.columns else table.index)
    found, compared = [], []
    for n, positions in enumerate(chunks):
        rows = table.iloc[positions]
        case = compiled_case(build, root / f"chunk{n}", model_points=rows)
        read = list(pd.read_csv(case.parent / TABLE, index_col="point_id").index)
        own = [labels[position] for position in positions]
        assert read == own, f"chunk {n} holds {read}, not {own}"
        compared += read
        found += [f"chunk {n}: {line}"
                  for line in compiled_mismatches(build, case, refs=refs, also=_wp_c4_also)]
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
    splice grid's rows, S's points and its variants restated in force at T2's months and
    issued later, a woman, the -40% crash, the pension tax basis on a bond, the bonds
    issued at the valuation date to their charge caps and the MVR at its bound among them,
    under each of the splice's sets of References (:data:`REF_SETS`): the main one, with the
    estate distribution on; the bonus rule's, its declarations made in the frame, cut by
    its cap and floored; and the deterrent's, the surrender rate at its bound, each set on
    modelx and on the compiled model before either computes.  The grid is the one this
    run's ``spliced`` selects, the core by default and the full grid under
    ``UKLIB_SEC_FULL=1``, and the test carries no ``sec_full`` mark, since a skipped compile
    test fails the cython_uk job.  Each set's SEC table goes beside the build in chunks of
    :data:`C4_MONTHS` months of frame, modelx sweeps every point fully, and the compiled
    model must agree at every argument modelx caches, identically on x86-64 and to 1e-12
    relative elsewhere, with every raise and every ``Data`` array
    (``uk_sec_support.compiled_mismatches``), ``result_payout``, which C2 does not freeze,
    among them.
    """
    build = sec_build(SEC)
    found = []
    for name, refs in REF_SETS.items():
        folder = spliced[name][1].Data.input_dir()
        table = pd.read_csv(folder / TABLE, index_col="point_id")
        found += [f"{name}: {line}"
                  for line in _c4_chunks(build, table, refs, tmp_path / name)]
    assert not found, _mismatch_lines(found)


# The contract's extremes (held by proj_len(), CACHE_EDGES): each shape of the chains'
# tests at its longest cover, issued at the youngest issue age, 18, to the largest limiting
# age the shipped table admits, 121, as (the S point it changes, its changes): the anchor
# bond, the endowment for 103 years and the bond withdrawing 1% a year at +7%, whose units
# never run out.  Each is made from S's new business, the bond variant (7) and the
# endowment (5).
EXTREMES = {
    31: (7, {"age_at_entry": YOUNGEST, "wd_rate": 0.0, "fund_return": 0.07}),
    32: (5, {"age_at_entry": YOUNGEST, "policy_term": OMEGA_MAX - YOUNGEST}),
    33: (7, {"age_at_entry": YOUNGEST, "wd_rate": 0.01, "fund_return": 0.07}),
}


def _contract_extremes(tmp_path):
    """The rows at the contract's extremes, built by the generator.

    Each of :data:`EXTREMES` in a copy of S's table, read with :data:`LONGEST_REFS` set,
    the bonus rule and the estate's distribution on and the limiting age at 121: its twin
    issued at the valuation date, a frame of 1,236 months; the same issued
    ``future_horizon_mth``, 120 months, after it, a frame of 1,356 months; and the same
    restated in force in the last month of its frame, opened with S's state there.  So
    ``t`` reaches 1,357, the policy year 104 and each code its last, the furthest
    ``spec_sec.py`` sizes for.  S's tables serve: the mortality table runs from 18 to 120.
    Returns the rows.
    """
    s_table = _s_table()
    rows = []
    for point_id, (base, changes) in EXTREMES.items():
        row = s_table.loc[[base]].assign(**changes, policy_id=f"WP-7000{point_id}")
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
    roll-forward's month after the month after the 1,356-month frame; ``y`` to 104, the
    guarantee date the last month's window waits for, and to 103 on each of the eight
    openings; and every timing and kind.  modelx sweeps every row fully, and the compiled
    model must agree everywhere.  A cache one too small for the contract raises
    ``IndexError`` compiled where modelx reads on, and fails here, though the spec check
    passes it, which holds the caches to the spec and not the spec to the contract.
    """
    build = sec_build(SEC)
    rows = _contract_extremes(tmp_path / "s")
    frames = _frames(rows, LONGEST_REFS, tmp_path / "frames")
    assert max(frames) == LONGEST_MAX + 120 == 1356 and frames.count(LONGEST_MAX) == 3
    found = _c4_chunks(build, rows, LONGEST_REFS, tmp_path / "extremes")
    assert not found, _mismatch_lines(found)


@pytest.mark.cython
def test_the_compiled_model_computes_what_modelx_computes_at_the_caches_bounds(
        sec_build, tmp_path):
    """C4 at the two bounds the caches hold, under References that admit past them.

    The rows of :data:`CACHE_EDGES` that project, each a frame of 1,356 months, the longest
    the ``t`` cache holds, under :data:`CACHE_REFS`, a lowered ``issue_age_min`` and a
    horizon of 200 months, which admit longer covers and frames, ``proj_len()`` refusing
    those by point: the bond issued at 18 and 120 months on, whose cover, 1,236 months, is
    the longest the ``y`` cache holds, and the bond issued 200 months on whose units run out
    in month 1,356, the last the exhaustion search reads.  modelx sweeps both fully, every
    Reference, ``Data.future_horizon_mth`` among them, set on both engines before either
    computes, and the compiled model must agree everywhere; a frame a month longer and a
    cover a year longer are refused in both, message for message
    (:func:`test_the_compiled_model_refuses_what_modelx_refuses`).
    """
    build = sec_build(SEC)
    rows = _cache_edges().iloc[[n for n, (*_, outcome) in enumerate(CACHE_EDGES)
                                if isinstance(outcome, int)]]
    assert _frames(rows, CACHE_REFS, tmp_path / "frames") == [1356, 1356]
    found = _c4_chunks(build, rows, CACHE_REFS, tmp_path / "caches")
    assert not found, _mismatch_lines(found)


# Where a cap or a bound the splice grid leaves unbound binds, as (case, the committed rows,
# the References, what must hold in modelx of some row in some month): the mortality cap,
# min(q, 1.0), on the bonds in their last years, under a best-estimate factor of 3, past
# which the shipped table's rates from age 103 or so are past 1; and the surrender rate's
# bound, min(1.0, ...), at 1, on the down scenario's bonds while the MVR applies, under a
# deterrent of 25.  The corridor's floor and ceiling, the smoothing cap's, the guarantee
# charge's cap, the asset share's floor, the MVR's bound and the rule's clamps bind on the
# splice grid's core, whose comparison is the test above.
BINDS = [
    ("the mortality cap", (13, 17), {"mort_be_factor": 3.0},
     lambda p, t: p.mort_rate(t) == 1.0),
    ("the surrender rate's bound", (9, 10), {"mvr_deterrent_factor": 25.0},
     lambda p, t: p.surr_rate(t) == 1.0),
]


@pytest.mark.cython
@pytest.mark.parametrize("case, rows, refs, binds", BINDS, ids=[c[0] for c in BINDS])
def test_the_compiled_model_computes_what_modelx_computes_where_a_bound_binds(
        sec_build, tmp_path, case, rows, refs, binds):
    """C4 where a cap or a bound the splice grid leaves unbound binds: every cell compiled.

    Each case of :data:`BINDS` is first asserted to bind in modelx, on its committed rows,
    under its References, in some month of each row's frame: the capped mortality 1.0, or
    the surrender rate at its bound, 1.0; then modelx sweeps the rows fully under the same
    References, and the compiled model must agree at every argument modelx caches,
    identically on x86-64 and to 1e-12 relative elsewhere.  No other compiled test reaches
    these sides of the ``min``.
    """
    build = sec_build(SEC)
    table = _committed().loc[list(rows)]
    folder = compiled_case(build, tmp_path / "binds", model_points=table)
    model = mx.read_model(folder, name=_name("binds"))
    try:
        for ref, value in refs.items():
            setattr(model.Projection, ref, value)
        bound = [any(binds(p, t) for t in range(p.proj_len()))
                 for p in (projection(model, key) for key in point_keys(model))]
    finally:
        model.close()
    assert bound and all(bound), (case, bound)
    found = compiled_mismatches(build, folder, refs=refs, also=_wp_c4_also)
    assert not found, _mismatch_lines(found)


@pytest.mark.cython
def test_the_compiled_model_computes_what_modelx_computes_on_every_decoded_value(
        sec_build, tmp_path):
    """C4 on every value a decoded column holds: compiled, every cell is modelx's.

    The twins of :data:`DECODED`'s points, each chassis, each sex and each tax basis on
    each chassis, and the guarantee dates written as a year, as three with a blank part
    between them, as none and as one past the frame, built by the generator from a copy of
    S's table, go beside the build: modelx sweeps them fully, and the compiled model must
    agree everywhere, each label's text, each decode's code and the mortality row it
    selects, and the guarantee flags of each year, among them, which the committed points,
    all men, reach only in part.  And the case at the flags' last column, on its cut
    mortality table, under its References (:func:`_last_column_pair`), whose last month
    reads that column.
    """
    build = sec_build(SEC)
    s, twins = _decoded_twins(tmp_path)
    s.close()
    folder = compiled_case(build, tmp_path / "decoded", model_points=twins)
    found = compiled_mismatches(build, folder, also=_wp_c4_also)
    s, sec, twins = _last_column_pair(tmp_path / "last_column")
    sec.close()
    s.close()
    folder = compiled_case(build, tmp_path / "decoded_last", model_points=twins,
                           edits={MORT: _young_table(LAST_COLUMN_AGE)})
    found += compiled_mismatches(build, folder,
                                 refs={**LAST_COLUMN_REFS, "issue_age_min": 0},
                                 also=_wp_c4_also)
    assert not found, _mismatch_lines(found)


@pytest.mark.cython
def test_the_compiled_model_returns_each_label_as_modelx_does(sec_build, tmp_path):
    """The labels, compiled, are modelx's: their text on every committed and decoded point.

    The three labels are reporting cells, which no projection cell calls, so C4's sweep
    compares them only as cells without parameters; this calls each on every point, in
    modelx and compiled (``uk_sec_support.label_mismatches``), on the committed table and
    on the twins of :data:`DECODED`, which carry every value of every labelled column: each
    must be the same text in both engines.  A label refuses what is not its column's codes,
    in either engine (:func:`test_each_label_refuses_a_value_that_is_not_its_codes`), so
    each compiles to ``str``, which C3 admits of a refusing label.
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
            assert values == {"chassis": {"UWP_bond", "CWP_endowment"}, "sex": {"M", "F"},
                              "tax_basis": {"life_net", "pension_gross"}}, values


# The model point table's columns that hold whole numbers, which a spreadsheet may save as
# floats: the months, the age and the term.  And the assumption tables' keys.
FLOAT_COLUMNS = ("duration_mth", "age_at_entry", "policy_term")
FLOAT_KEYS = {MORT: lambda t: t.assign(age=t["age"].astype(float)),
              LAPSE: lambda t: t.assign(policy_year=t["policy_year"].astype(float))}


@pytest.mark.cython
def test_the_compiled_model_reads_keys_written_as_floats_as_modelx_does(sec_build,
                                                                         tmp_path):
    """C4 on keys written as floats: the compiled model reads 60.0 as 60, as modelx does.

    The committed table with its labels written ``1.0`` to ``24.0`` and its whole numbers as
    floats (:data:`FLOAT_COLUMNS`), the guarantee dates already ``10.0``, and the two
    assumption tables' keys as floats (:data:`FLOAT_KEYS`).  ``Data`` reads each by value,
    so first, in seconds, modelx's ``Data`` on the floats is held to its ``Data`` on the
    same rows as written: every array of the same dtype and values, and every check of the
    same type, so that a key read as a float fails here, naming its cell, and not in the
    compiled sweep.  Then modelx sweeps every point, and the compiled model must agree
    everywhere, every ``Data`` array included, in dtype and shape.
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
    found = _c4_chunks(build, floats, {}, tmp_path / "compared")
    assert not found, _mismatch_lines(found)


@pytest.mark.cython
@pytest.mark.parametrize("ref", list(OWN_REFS_ROWS))
def test_the_compiled_model_computes_what_modelx_computes_under_a_row_s_own_references(
        sec_build, tmp_path, ref):
    """C4 on the committed rows under the References each was read from.

    Five committed rows were read from S under References of their own (the spec's
    ``derived_refs``): the bond variant at 60 and the 5% bond at 300 under a guarantee
    charge of 0.2%, the worked example's bond and the endowment at 150 with the bonus rule
    on, and the worked example's bond at 156 under a smoothing cap of 5%.  C4 on the
    committed points compares them at the shipped References; under their own, set on the
    compiled model as on modelx before either computes, each continues S's path, which
    other rows' References leave untaken: so the rows read under each set
    (:data:`OWN_REFS_ROWS`), and the whole committed table with the full grid, are swept
    fully under it, and the compiled model must agree everywhere, the rule's declarations
    in the frame among them.
    """
    build = sec_build(SEC)
    (refs,) = {tuple(r.items()) for r in SPEC.derived_refs.values() if ref in r}
    found = _c4_chunks(build, _c4_rows(OWN_REFS_ROWS[ref]), dict(refs), tmp_path / "own")
    assert not found, _mismatch_lines(found)


@pytest.mark.cython
def test_the_compiled_model_declares_in_the_frame_as_modelx_does(sec_build, tmp_path):
    """C4 on the rule's declarations in the frame, at today's References (D6), compiled.

    The owner's decision (D6): a declaration at or after the valuation date is the
    projection's own event, the rule's at today's References, from this model's own asset
    share and guarantee.  On the row valued in its declaration month, the bond at 71, that
    declaration is month 0's own event, its rule reading the opening state; on the row
    valued mid-year, the down scenario's bond at 68, the year-end declaration at ``t = 3``
    is the rule's from the opening rate; and on the endowment valued on its declaration and
    the 5% bond in force, whose steps no clamp holds, the rate declared moves with the
    supportable rate.  In modelx, under :data:`RULE_REFS`, each row's rate in the
    declaration's month is asserted to be the rule's and not the row's opening rate, as
    ``test_each_declaration_in_the_frame_is_made_at_today_s_references`` holds it; then the
    rows of :data:`DECLARING_ROWS`, the whole committed table with the full grid, are swept
    fully under those References, and the compiled model must agree everywhere, the declared
    rate, the price it steps and every year's declaration after it among it. A compiled
    declaration that read the extract's rate parts here.
    """
    build = sec_build(SEC)
    model = mx.read_model(model_path(SEC), name=_name("declares"))
    try:
        for ref, value in RULE_REFS.items():
            setattr(model.Projection, ref, value)
        for case, d0 in DECLARED:
            p = _row(model, *case)
            got, want = _rule_from(p, p.bonus_rate_init())
            assert p.bonus_rate(d0) == got != p.bonus_rate_init(), case
            assert _rule_agrees(got, want), (case, got, want)
    finally:
        model.close()
    found = _c4_chunks(build, _c4_rows(DECLARING_ROWS), RULE_REFS, tmp_path / "declared")
    assert not found, _mismatch_lines(found)


@pytest.mark.cython
@pytest.mark.parametrize("refs", [pytest.param({}, id="shipped"),
                                  pytest.param(RULE_REFS, id="rule")])
def test_the_compiled_model_exhausts_the_units_as_modelx_does(sec_build, tmp_path, refs):
    """C4 on the bonds whose units run out: the search and the encashment, compiled.

    ``fund_exhaust_mth`` searches the units month by month, ascending, from ``t_entry()``,
    one loop in one cell, and reads the units of the month they run out, one past the
    frame; under the rule the units are bought at a price the declarations step, each read
    from the asset share, so the search runs through the asset share's chain too.  On the
    rows of :data:`EXHAUSTED_ROWS`, the withdrawing bond in force at 60 and the bond variant
    at 100, the whole committed table with the full grid, at the shipped References and
    with the bonus rule on, each row's frame is first asserted to end by the units'
    exhaustion, the forced encashment; then modelx sweeps the rows fully, and the compiled
    model must agree everywhere, the search's month and the maturity it pays among them.
    """
    build = sec_build(SEC)
    rows = _c4_rows(EXHAUSTED_ROWS)
    model = mx.read_model(model_path(SEC), name=_name("exhausted"))
    try:
        for ref, value in refs.items():
            setattr(model.Projection, ref, value)
        for label in EXHAUSTED_ROWS:
            p = _point(model, label)
            assert p.is_forced_encashment(), label
            assert p.fund_exhaust_mth() == p.duration_mth_init() + p.proj_len(), label
    finally:
        model.close()
    found = _c4_chunks(build, rows, refs, tmp_path / "exhausted")
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


# The integer References, which the compiled model holds as long long, and the switch, which
# it holds as a C bint: an integer set to a value that is not a whole number below 2**63
# cannot be held compiled at all, and one with a fraction is truncated as it is set, 120.5
# to 120, where modelx refuses 120.5; and the switch takes any value's truth as it is set, 2
# and "yes" as True and None as False, where modelx refuses each.  So the compiled refusals
# take a domain's cases at whole numbers and at True and False alone, and model-sec.md says
# to set each integer as a whole number and the switch as True or False (UKLIB-SEC-PLAN.md
# §6.1, *Record -- M2*).
INT_REFERENCES = frozenset({"issue_age_min", "omega_age", "bonus_horizon"})
BOOL_REFERENCES = frozenset({"bonus_rule_on"})


def _held_compiled(refs):
    """Whether the compiled model holds every one of ``refs`` as modelx does."""
    return all((math.isfinite(value) and value == value // 1 and abs(value) < 2.0 ** 63)
               if ref in INT_REFERENCES else
               (value is True or value is False) if ref in BOOL_REFERENCES else True
               for ref, value in refs.items())


# Data's integer Reference, which the compiled model holds as a long long, as it holds
# Projection's (INT_REFERENCES), and which the child sets as it sets theirs: the horizon
# is refused at -1 and at 2**53, each as an int and as a float, in both engines, message
# for message, its value printed as a float, as the compiled model prints the long long it
# holds; read at 121 and at 121.0, past the shipped 120, as the in-force step reads it
# (READ_HORIZONS); and a fraction is truncated as it is set, 12.5 to 12, where modelx
# refuses 12.5 (the horizon test), so that compiled, 12.5 does what 12 does in modelx: it
# refuses the point issued 13 months on.  model-sec.md says to set it as a whole number.
DATA_INT_REFERENCES = frozenset({"future_horizon_mth"})
HORIZONS = (-1, -1.0, 12.5, 121, 121.0, 2 ** 53, 2.0 ** 53)
READ_HORIZONS = frozenset({121})


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


# Projection's idx past the extract's last row, 24, and -1, beside the last row, 23, as
# (position, cell, arguments): past the last row the first read of a vector raises
# IndexError in both engines, each in its own words, and -1 reads every vector at its last
# element in both, so it is the last point, under that point's own point_id.
IDX_CASE = "an idx past the table and one before it"
IDX_EDGES = [(24, "point_id", ()), (24, "result_cf", ()), (-1, "point_id", ()),
             (-1, "proj_len", ()), (-1, "net_cf", (0,)), (23, "point_id", ()),
             (23, "proj_len", ()), (23, "net_cf", (0,))]

# Calls past the caches spec_sec.py sizes, which raise IndexError in the compiled model
# alone, as (the committed point, call, arguments, what modelx does), on the extract:
# a month past the t cache, on the worked example's bond in force at 60, and a month before
# it, on the bond variant issued at the valuation date, before its issue, each of which
# modelx answers with 0.0, a month outside cover; a timing and a kind past the one inner
# width, which modelx refuses as codes it does not take; and a policy year past the y
# cache, on each of the eight openings, whose opening modelx computes as it computes any
# year's, the value the year before closes on, 0.0 here, that year long past the worked
# example's cover, and either side of it on the guarantee dates' reader, which reads no
# year there.
OPENINGS_PAST = tuple((1, opening, (105,), ("ok", 0.0)) for opening in OPENINGS)
COMPILED_ONLY = [
    (1, "net_cf", (1358,), ("ok", 0.0)), (7, "net_cf", (-1,), ("ok", 0.0)),
    (1, "pols_if_at", (0, 10), ("raised", "ValueError: invalid timing")),
    (1, "asset_share_at", (0, 10), ("raised", "ValueError: invalid timing")),
    (1, "claim_pp", (0, 10), ("raised", "ValueError: invalid kind")),
    (1, "smoothing_cost_pp", (0, 10), ("raised", "ValueError: invalid kind")),
    (1, "claims", (0, 10), ("raised", "ValueError: invalid kind")),
    *OPENINGS_PAST,
    (1, "is_guarantee_year", (105,), ("ok", False)),
    (1, "is_guarantee_year", (-1,), ("ok", False)),
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

    def extract(edit=None):
        return _extract_of(edit)[0]

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
    for case, (s_point, month), end in PAST_COVER:
        moved = _label(committed, "derived", s_point, month)
        cases.append((case, extract(_set("duration_mth", [moved], end)), None, {},
                      [(at(moved), "result_cf", ()), (at(moved), "proj_len", ())], ()))
    for case, edit, refs, point, _, _ in NOT_ISSUED:
        cases.append((case, extract(edit), None, refs,
                      [(at(point), cell, ()) for cell in ("result_cf", "proj_len")], ()))
    for case, edit, point, _ in SPENT:
        cases.append((case, extract(edit), None, {},
                      [(at(point), cell, ()) for cell in ("result_cf", "proj_len")], ()))
    for case, refs, point, message, report in DOMAINS:
        if not _held_compiled(refs):
            continue
        if message is not None:
            cases.append((f"domain {case}", extract(), None, refs,
                          [(at(point), "result_cf", ()), (at(point), "proj_len", ())], ()))
        elif report is not None:
            cases.append((f"domain {case}, its report", extract(), None, refs,
                          [(at(point), "result_cf", ())], ()))
    for case, edit, refs, point, call, report, _ in PAST_THE_FLOATS:
        name, t, *rest = call
        report = report[0] if isinstance(report, tuple) else report
        calls = [(at(point), name, _codes_of((t, *rest))), (at(point), report, ())]
        cases.append((f"past the floats: {case}", extract(edit), None, refs, calls, ()))
    refusals = dict(REFUSAL_CELLS)
    for refs, (table, past) in _chains_past_tables().items():
        labels = list(table.index)
        calls = []
        for label, (_, _, _, _, chain, month, _, _) in past:
            position = labels.index(label)
            calls += [(position, chain, (month - 1,)), (position, chain, (month,)),
                      (position, refusals[chain], (month,))]
        cases.append(("later: chains past the floats after their first month", table, None,
                      dict(refs), calls, ()))
    cases.append(("the claims total past the floats",
                  _committed().loc[[16]].assign(policy_count=1e304),
                  {LAPSE: _lapse_at(0.99)}, {"mort_be_factor": 130.0},
                  [(0, "claims", _codes_of((0, "ALL")))], ()))
    cut = {MORT: _dropped(lambda t: t["age"] < 20)}
    cases.append(("an age below the mortality table",
                  extract(_then(_set("age_at_entry", [7], 18), _set("wd_rate", [7], 0.0))),
                  cut, {}, [(at(7), "result_cf", ()), (at(7), "mort_rate", (0,))], ()))
    for case, edit, _ in NOT_HELD:
        cases.append((case, edit(committed), None, {}, [(16, "result_cf", ())],
                      ("point_id",)))
    cases.append(("codes no cell takes, inside the caches", extract(), None, {},
                  [(at(1), cell, args) for cell, args, _ in CODES_IN_CACHE], ()))
    for horizon in HORIZONS:
        if horizon in READ_HORIZONS:
            future = _label(committed, "future", 7, -13)
            cases.append((f"accepted: future_horizon_mth at {horizon!r}", extract(), None,
                          {"Data.future_horizon_mth": horizon},
                          [(at(future), "proj_len", ()), (at(1), "net_cf", (0,))], ()))
            continue
        cases.append((f"future_horizon_mth at {horizon!r}", extract(), None,
                      {"Data.future_horizon_mth": horizon}, [(at(1), "result_cf", ())],
                      ("model_point_table",)))
    cases.append(("the caches' bounds", _cache_edges(), None, dict(CACHE_REFS),
                  [(n, cell, ()) for n, (*_, outcome) in enumerate(CACHE_EDGES)
                   if not isinstance(outcome, int) for cell in ("result_cf", "proj_len")],
                  ()))
    cases.append(("accepted: the run-out of a cover the bound refuses", _cache_edges(),
                  None, dict(CACHE_REFS), [(CONSERVATIVE, "fund_exhaust_mth", ())], ()))
    return cases


# The cases of :func:`_refusal_cases` whose every refusal is a projection's, naming its
# point first, ``point_id <label>: ...``: those Data's reader, the assumption tables'
# checks, the vectors' holding and a cell's codes refuse name a list of labels, a file or
# nothing.
NAMING_CASES = frozenset({c[0] for c in PAST_COVER} | {c[0] for c in NOT_ISSUED}
                         | {c[0] for c in SPENT}
                         | {"the claims total past the floats",
                            "an age below the mortality table", "the caches' bounds"})


def _names_its_point(case):
    """Whether every refusal of ``case`` names its point first (:data:`NAMING_CASES`)."""
    return case in NAMING_CASES or case.startswith(("domain ", "past the floats: ",
                                                    "later: "))


@pytest.mark.cython
def test_the_compiled_model_refuses_what_modelx_refuses(sec_build, tmp_path):
    """Compiled, the model refuses what modelx refuses, with modelx's error and message.

    A ``ValueError`` raised in a cell typed ``long long`` or ``double`` propagates out of
    the compiled model as out of modelx.  So, each on its own inputs and References
    (:func:`_refusal_cases`), on an extract labelled otherwise than by position: every case
    of :data:`MALFORMED`, refused by a projection and by ``Data``'s reader, the ``2**53``
    bounds among them; every case of :data:`UNREADABLE`, by a projection, by the ``Data``
    cell that checks the table and by the table's array, so that a compiled ``Data`` cell
    refuses each value its modelx cell refuses; every case of :data:`PAST_COVER`,
    :data:`NOT_ISSUED` and :data:`SPENT`, by ``result_cf`` and ``proj_len``; every case of
    :data:`DOMAINS` that refuses and that the compiled model can hold, its integer
    References whole and its switch True or False (:func:`_held_compiled`), each printed as
    the compiled model types it, by the frame or by the report the value past the floats
    first reaches; each row of :data:`CACHE_EDGES` that refuses, by ``result_cf`` and
    ``proj_len``, under :data:`CACHE_REFS`, set by the child on ``Projection`` and ``Data``
    alike: a frame a month longer than the ``t`` cache holds, a cover a year longer than the
    ``y`` cache holds on either chassis, a bond whose units last past month 1,356, which the
    compiled exhaustion search must not read past the cache to find, and the withdrawing
    bond whose cover is a year longer though its units run out within the caches, which the
    in-force step projects and the cover's bound refuses, its run-out month read alike; each
    value of :data:`PAST_THE_FLOATS` by its cell and by a report, a kind named by its code,
    the three powers past the floats and below the smallest among them, which the compiled
    cells reach through Python's own power where C's gives an infinity or 0, uslib's M22
    form, so that the compiled model raises the cell's refusal as modelx does; each chain of
    :data:`CHAINS_PAST`, finite in the month before and refused in its month, mid-year, on a
    declaration and on an anniversary, by the chain and by its refusal cell; the claims
    total past the floats, its kinds finite; an attained age below a mortality table cut at
    20, by ``mort_rate`` and a report; a label the vectors cannot hold, by
    ``Data.point_id``; each code of :data:`CODES_IN_CACHE`, inside the caches, which the
    cell's own formula refuses; and ``Data.future_horizon_mth`` at each of :data:`HORIZONS`,
    set by the child as every space's References are, refused by a projection and by
    ``Data``'s reader at ``-1`` and ``2**53``, as ints and as floats, as modelx refuses it,
    its value printed as a float in both, and at ``12.5``, which the compiled model
    truncates as it is set, as modelx refuses 12 (:func:`_as_held`); and read at ``121`` and
    ``121.0`` (:data:`READ_HORIZONS`), as modelx reads them, the frame of the point issued
    13 months on and the worked example's first cash flow each modelx's.

    And the refusals that are the compiled model's alone (:data:`COMPILED_ONLY`): a month
    past the ``t`` cache either side, a timing and a kind past their codes, and a policy
    year past the ``y`` cache on each of the eight openings and on the guarantee dates'
    reader, each raising ``IndexError`` compiled, beside what modelx does.  And
    ``Projection``'s ``idx`` at the table's edges (:data:`IDX_EDGES`): one past the last row
    raises ``IndexError`` in both engines, compared by its type, the words being each
    engine's own, and ``-1`` is the last row in both, its every outcome the last row's and
    modelx's, which a build without bounds checks, or without Python's negative indices,
    would part from.

    Comparing the engines alone would pass a refusal that names its point by its position,
    ``idx + 1``, in both: so each refusal a projection makes must also name the extract's
    label first, ``point_id <label>: ...``, every refusal of a case of
    :data:`NAMING_CASES`, the domains', the values' and the chains' past the floats among
    them (:func:`_names_its_point`), and any other that names a point.

    The compiled model runs every case in one child, each on a fresh instance of the model
    that reads the case's own copies of the three files by absolute path
    (:data:`REFUSALS_CHILD`), each path in a message written as the file's name, as modelx
    names it (:func:`_named`), and modelx reads each case afresh.
    """
    build = sec_build(SEC)
    cases = _refusal_cases()
    plain = len(cases)
    committed = _committed()
    relabelled, _ = _extract_of()
    positions = list(committed.index)
    cases.append(("compiled only", relabelled, None, {},
                  [(positions.index(point), cell, args)
                   for point, cell, args, _ in COMPILED_ONLY], ()))
    assert len(relabelled) == 24
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
                          capture_output=True, text=True, timeout=1800)
    assert done.returncode == 0, done.stderr[-4000:]
    got = pickle.loads(result.read_bytes())
    found, refused, computed, edges, named = [], 0, 0, {}, 0
    only = iter(COMPILED_ONLY)
    for (case, table, *_, calls, data), (files, *_), (want, want_data), (
            have, have_data) in zip(cases, jobs, wants, got, strict=True):
        labels = list(table.index)
        have = [_named(did, files) for did in have]
        have_data = [_named(did, files) for did in have_data]
        for n, ((idx, cell, args), modelx_did, compiled_did) in enumerate(
                zip(calls, want, have, strict=True)):
            where = f"{case}: idx {idx}: {cell}{args}"
            if case == IDX_CASE:
                edges[idx, cell, args] = (modelx_did, compiled_did)
                if idx == 24:
                    for engine, did in (("modelx", modelx_did), ("compiled", compiled_did)):
                        if (did[0], str(did[1]).split(":")[0]) != ("raised", "IndexError"):
                            found.append(f"{where}: {engine} {did}, not IndexError")
                elif compiled_did != modelx_did:
                    found.append(f"{where}: compiled {compiled_did}, modelx {modelx_did}")
                continue
            if case == "compiled only":
                *_, does = next(only)
                if modelx_did != does:
                    found.append(f"{where}: modelx {modelx_did}, not {does}")
                if (compiled_did[0], str(compiled_did[1]).split(":")[0]) != (
                        "raised", "IndexError"):
                    found.append(f"{where}: compiled {compiled_did}, not IndexError")
                continue
            if case.startswith("accepted: "):
                computed += 1
                if modelx_did[0] != "ok" or not (
                        compiled_did[0] == "ok" and _as_modelx(compiled_did[1],
                                                               modelx_did[1])):
                    found.append(f"{where}: compiled {compiled_did}, modelx {modelx_did}, "
                                 f"where both read the value")
                continue
            if case.startswith("later: ") and n % 3 == 0:
                computed += 1
                if modelx_did[0] != "ok" or not (
                        compiled_did[0] == "ok" and _as_modelx(compiled_did[1],
                                                               modelx_did[1])):
                    found.append(f"{where}: compiled {compiled_did}, modelx {modelx_did}, "
                                 f"where the month before the overflow computes")
                continue
            refused += 1
            if modelx_did[0] != "raised":
                found.append(f"{where}: modelx returned, where a refusal was meant")
                continue
            if compiled_did != modelx_did:
                found.append(f"{where}: compiled {compiled_did}, modelx {modelx_did}")
            text = str(modelx_did[1])
            if _names_its_point(case) or text.startswith("ValueError: point_id "):
                named += 1
                if not text.startswith(f"ValueError: point_id {labels[idx]}: "):
                    found.append(f"{where}: {text[:120]!r} does not name the extract's "
                                 f"label, {labels[idx]}")
        for name, modelx_did, compiled_did in zip(data, want_data, have_data, strict=True):
            if modelx_did[0] != "raised":
                found.append(f"{case}: Data.{name}: modelx returned, where a refusal was "
                             f"meant")
            elif compiled_did != modelx_did:
                found.append(f"{case}: Data.{name}: compiled {compiled_did}, modelx "
                             f"{modelx_did}")
            refused += 1
    for (idx, cell, args), outcomes in edges.items():
        if idx == -1 and outcomes != edges[23, cell, args]:
            found.append(f"{IDX_CASE}: {cell}{args} at idx -1 is {outcomes}, at the last "
                         f"row {edges[23, cell, args]}")
    assert edges[-1, "point_id", ()][0] == ("ok", EXTRACT_LABELS[-1]), edges
    assert not found, "\n".join(found[:40])
    naming = sum(len(calls) for case, *_, calls, _ in cases[:plain]
                 if _names_its_point(case)) - len(CHAINS_PAST)
    assert named >= naming > 300, (named, naming)
    assert computed == len(CHAINS_PAST) + sum(len(calls) for case, *_, calls, _ in cases
                                              if case.startswith("accepted: "))
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
STACK_KIB = (32, 48, 64, 96, 128, 192, 256, 384, 512, 1024, 2048)

# The chain heads the stack test calls cold, each in an ItemSpace of its own, as (cell, the
# code it takes, or None): net_cf, the count's residual and the claims total, the deepest
# calls a projection makes, through the count's chain and, beneath it, the payout's and
# the guarantee's; and the smoothing account, the deepest call into the asset share's
# chain.  Measured at M14 on the blocked chains, the count's heads needed 64 KiB of C stack
# here and every other head 56, against 216 to 292 KiB one cell a month.  The runner makes
# one ItemSpace for each key of a job and deletes it after the key's calls, so a key with
# two calls would run the second warm, on the first's caches.
STACK_HEADS = (("net_cf", None), ("check_pols_roll_fwd_resid", None), ("claims", "ALL"),
               ("smoothing_account", None))

# How long the stack test waits for each child, in seconds: one runs in a few seconds, more
# under load.  A bracketing size may kill its child on a stack overflow by design, and
# where the overflow hangs instead, as Windows Error Reporting could, the wait ends sooner
# than for the two runs asserted, and the size is recorded as timed out.
BRACKET_TIMEOUT, ASSERTED_TIMEOUT = 120, 300


@pytest.mark.cython
def test_the_longest_cover_runs_cold_on_a_one_megabyte_stack(sec_build, tmp_path):
    """The deepest call the contract allows runs compiled on a 1 MiB stack (F7).

    On the rows of :func:`_longest_cover`, each shape of :data:`SHAPES` at its longest
    cover, issued at 18 now and 120 months on, the limiting age at the largest the shipped
    table admits, 121, 1,236 months from issue: the anchor bond, the endowment for 103 years
    and the bond withdrawing 1% a year, whose exhaustion search runs the units over the
    whole cover.  Each of :data:`STACK_HEADS`, cold in the last month, runs the chains back
    to ``t_entry()``, one cell a month within the policy year and two a year before it, the
    eight chains being blocked by policy year: 216 to 240 cells deep in modelx
    (:func:`test_every_chain_runs_one_cell_a_month_from_a_cold_start`), with every switch
    that ships off on (:data:`LONGEST_REFS`).  Each runs in an ItemSpace of its own, on a
    copy of its row, so that each is cold: in one ItemSpace the second would run on the
    first's caches, a few cells deep.  Compiled they run on the C stack, which the
    interpreter's recursion limit does not count, and one cell a month they needed up to 292
    KiB of it here, the count's, and blocked 64 (UKLIB-SEC-PLAN.md §6.5, *Record -- M14*).
    1 MiB is the stack MSVC gives an executable's main thread unless the executable asks for
    more: a host that embeds Python, where python.exe itself asks for 2,000,000 bytes.  A
    thread whose stack is reserved at 1 MiB stands in for it on every platform
    (``uk_sec_support.run_compiled``), and in one each call runs cold and returns modelx's
    number, identically on x86-64 (``uk_sec_support.exact_here``) and to 1e-12 elsewhere.  A
    stack too small kills the child, and the test fails naming the stack. The thread's stack
    is read back too, from Windows or from glibc, and must be at most 1 MiB and a page: a
    stand-in larger than asked for would stand for nothing.  And the calls run again on the
    child's main thread, which is what ``run_sec.py --cython`` runs on.

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
    folder, frames = _longest_cover(tmp_path / "rows", tuple(SHAPES))
    rows = pd.read_csv(folder.parent / TABLE, index_col="point_id")
    copies = [rows.set_axis(rows.index + 1000 * i, axis=0) for i in range(len(STACK_HEADS))]
    case = compiled_case(build, tmp_path / "longest", model_points=pd.concat(copies))
    model = mx.read_model(case, name=_name("longest"))
    try:
        for ref, value in LONGEST_REFS.items():
            setattr(model.Projection, ref, value)
        calls, want = {}, {}
        for label, _, months, entry in frames:
            for i, (head, code) in enumerate(STACK_HEADS):
                key = _key(model, label + 1000 * i)
                proj = projection(model, key)
                assert (proj.proj_len(), proj.t_entry()) == (months, entry), label
                args = (months - 1,) if code is None else (months - 1, _code(proj, code))
                calls[key] = [(head, args)]
                want[key] = [proj.cells[head](*args)]
                _release(model, key)
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
    record = (f"the compiled cold net_cf, count residual, claims total and smoothing account "
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
    ``Projection``, the worked example's twin at ``idx`` 0, the worked example's bond at 71
    at ``idx`` 7, made before, and the down scenario's bond at 92 at ``idx`` 9, made after,
    so that a modelx-cython that began to clear caches would be seen here, and the advice
    changed with it.  A compiled value meets modelx's as C4 holds it (:func:`_as_modelx`),
    and one the compiled model kept, its own value of before, identically.
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
    modelx's: point 14's description, the withdrawing bond in its last month, and its row
    and counts, point 23's, the endowment at 150, and the block's lines for each point,
    its first twelve rows and its first twelve projection years.

    The same output is what a runner that ignored ``--build`` and ran modelx would print,
    so the runner is also given a directory that holds no build, and must refuse it,
    saying so, rather than print anything.
    """
    build = sec_build(SEC)
    runner = model_path(SEC).parent / "run_sec.py"
    for args in (("14",), ("23",), ("--block",)):
        expected = _run_sec(runner, *args)
        assert _run_sec(runner, *args, "--cython", "--build", str(build.out)) == expected
    empty = tmp_path / "no_build"
    empty.mkdir()
    done = _run_sec(runner, "14", "--build", str(empty), check=False)
    stderr = done.stderr.decode(errors="replace")
    assert done.returncode != 0 and done.stdout == b"", stderr
    assert f"holds no build of {SEC} for this interpreter" in stderr, stderr
