"""In-force tests for Term_US_SEC: the splice, future business, counts and regeneration.

``Term_US_SEC`` is ``Term_US_S`` taught to run in force at a valuation date
(USLIB-SEC-PLAN.md, milestone M1).  It runs on two clocks: ``t`` counts months from the
valuation date, the same month for every model point, and ``duration_mth(t)`` counts the
months the policy has been in force, ``duration_mth_init() + t``.  A model point may be a
policy already in force at the valuation date, one issued at it, or one to be issued after
it, as in ``basiclife/BasicTerm_SE``.

The worked example is not restated here.  On a point issued at the valuation date the two
clocks coincide and the model is ``Term_US_S``, and ``test_model_conventions.py`` asserts
that cell by cell on the twins of S's two points (T1), so every golden of
``test_term_life_us.py`` holds on this model with no number copied.  The conventions also
hold the SEC family's other rules: every frame opens at ``t = 0``, ``pols_if`` is the
``BEF_DECR`` count, ``BEF_DECR`` is ``BEF_NB`` plus the month's new business, new business
enters once, and nothing happens before issue.  This module holds the rest of the plan's
tests (its §5.2) and the product's own facts:

* T2, the splice: an S point restated in force at month ``d``, opened with the count S
  carries into ``d``, continues S's projection from ``d`` on, in every cell of S's.  The
  months straddle the shock, the first ART premium and expiry, and three variants of S's
  points, in a copy of S's table, add what S's own points cannot reach: the age limit of
  the conversion window, the three premium cycles that are not the anniversary, a level
  period of twenty years, and cover that ends with the level period.
* T3, future new business: a point issued ``k`` months after the valuation date is S's
  projection ``k`` months on, with zeros before issue and no rate evaluated there.
* D11's R1 and R2, and D3's clock: on the splice's grid no cell is called at a negative
  month or reads beyond ``t + 1``; on the committed points no recursion runs backward over
  the frame; and the policy clock is a closed form.
* T4, the count algebra: the count rolls forward through new business and decrements, and
  doubling ``policy_count`` doubles every flow and moves no per-policy value.
* T5, validation: each malformed in-force row is refused as the table is read, naming its
  point; the future horizon is a Reference that bounds future business, and at 0 refuses
  it; and the edges of the interface are accepted.
* T6, regeneration: the committed ``model_point_table_sec.csv`` is what the generator makes
  of ``Term_US_S`` and its table as they stand.
* Then the two clocks on the shipped points, the policy in force mid-ART, expense inflation
  on the valuation clock, acquisition on new business, the values outside cover, the block,
  an in-force extract, the runner, the docstrings and the shared input tables.
* C2, the fingerprint: every committed point computes what the model computed when Phase 1
  ended, frozen at the end of this module before Phase 2 changed anything (§5.4).

SEC month ``t`` is S month ``t + source_mth`` throughout, the direction in which
``sec_support`` takes its ``t_offset``: ``d`` for a point restated at S month ``d``, ``-k``
for one issued ``k`` months on.

Every test keeps four rules.  Each model is read under a name of its own and closed:
``conftest.term_life`` holds S's default name, and reading a model under a name in use
renames the open one.  No test writes inside the library tree: every changed input goes
through ``sec_support.temp_inputs`` into a temporary directory, because a CSV added beside
the models, even briefly, would fail a concurrent
``test_every_csv_beside_the_model_is_actually_read``.  No test indexes ``Projection`` by
hand: the keys come from ``us_registry.point_keys`` and the ItemSpaces from
``us_registry.projection``, and a generated row is found by what it is, its kind, its S
policy and its month (``_row``), so neither a renumbered table nor Phase 2's positions can
point a test at the wrong row.  And a timing is passed as its string, as at stage ``"E"``;
Phase 2 changes the call syntax only (C1).
"""
import dataclasses
import itertools
import re
import shutil
import subprocess
import sys

import modelx as mx
import pandas as pd
import pytest

from sec_support import (
    GENERATED_COLUMNS, SEC_SPECS, TWIN_EXEMPT_DEFAULT, build_sec_table, check_generated,
    fingerprint_mismatches, frame_mismatches, sweep, temp_inputs, twin_mismatches)
from us_registry import model_path, point_keys, projection

SEC, TWIN, TABLE = "Term_US_SEC", "Term_US_S", "model_point_table_sec.csv"

# S's two points, both issued at t = 0.  Point 1 takes M(1) from its override, point 2 from
# the notes' formula through jump_ratio, so the two differ wherever the PLT years are read.
S_POINTS = (1, 2)

# T2's months (USLIB-SEC-PLAN.md §7.1): the second month, the year's premium already paid;
# the first anniversary, a premium due at t = 0; the last level month, 119, which carries
# the shock; 120, the first ART premium, and the month after it; and 719, the last month of
# cover.  T3's: issued one month on, which puts the policy anniversaries a month off the
# valuation years, and twelve, which puts them back on.
SPLICE_MTHS = (1, 12, 119, 120, 121, 719)
FUTURE_MTHS = (1, 12)

# Three more S points, in the splice's copy of S's table and never in the committed one,
# each S's anchor cell changed so as to reach what S's own points cannot.  On those, issued
# at 35 on the ten-year plan and paying annually, the conversion window closes with the
# level period, long before attained age 70, every premium falls due on the anniversary,
# the level period is ten years in every formula that reads it, and cover outlasts it by
# fifty.  Each variant is (the S point it changes, the columns it changes); the policy_id
# keeps the generated ids apart.  T2 restates each at the months given, T3 issues each a
# month on, and each pays in a mode no other point pays in.
#
# 3, S point 1 at 65, quarterly: the window is policy years 1 to 5, closed by age 70, and
#   the premium falls due every third month.  Restated in the second month, between two
#   instalments, at the last month before the final eligible year (47), at the final
#   year's last month (59) and at the first month outside the window (60).
# 4, S point 2 at 45 on a twenty-year plan, semi-annually: the shock in month 239, the jump
#   ratio read at years 20 and 21, and from it M(1) by the notes' rule, as point 2 has no
#   override.  Restated either side of the shock and the first ART premium, at 12n - 2,
#   12n - 1, 12n and 12n + 1.  premium_rates.csv has no T20 scale, so the copies get the
#   one _premium_rates_with_t20 builds.
# 5, S point 1 at 85, monthly: cover ends with the level period, so the shock falls in the
#   last covered month and S's jump ratio reads policy year 11, past S's own frame, where
#   SEC's cells answer that the month is outside cover (sec_support.twin_mismatches compares
#   S's frame alone).  Restated in the second month, then in the last two.
VARIANTS = {
    3: (1, {"policy_id": "TL-000003", "age_at_entry": 65, "premium_mode": "Q"}),
    4: (2, {"policy_id": "TL-000004", "age_at_entry": 45, "plan": "T20",
            "premium_mode": "SA"}),
    5: (1, {"policy_id": "TL-000005", "age_at_entry": 85, "premium_mode": "M"}),
}
VARIANT_SPLICE_MTHS = {3: (1, 47, 59, 60), 4: (238, 239, 240, 241), 5: (1, 118, 119)}
VARIANT_FUTURE_MTHS = {3: (1,), 4: (1,), 5: (1,)}

# T2's cases, as (row_kind, S point, source_mth): each S point restated in force at each of
# its splice months, then the twins of S's own in-force rows.  Those are splice cases too
# (§5.2), aligned at their twin's source_mth, the first row of the S frame.  Term_US_S has
# no in-force row, so the second list is empty here; WholeLife's would hold
# ("twin", 1, 108).  T3's cases, as (S point, k).
SPLICES = (tuple(("derived", p, d) for p in S_POINTS for d in SPLICE_MTHS)
           + tuple(("derived", p, d) for p, mths in VARIANT_SPLICE_MTHS.items()
                   for d in mths))
IN_FORCE_TWINS = ()
FUTURES = (tuple((p, k) for p in S_POINTS for k in FUTURE_MTHS)
           + tuple((p, k) for p, mths in VARIANT_FUTURE_MTHS.items() for k in mths))

# What the splice sets in both models, S and SEC alike, before either evaluates anything.
# Expense inflation is the one input Term reads on the valuation clock (D7): S inflates from
# issue and SEC from the valuation date, so at the shipped 2% the expenses of a point
# opened at d differ by 1.02^(d/12), by design, and at 0 both factors are 1.  The clock
# itself is then asserted on its own, at the shipped rate, because a zero rate hides any
# clock.  Term has no mortality improvement.  Conversion ships at 0, as the worked example
# requires, which multiplies the conversion window, its final-year rule and the conversion
# credit by zero in every month; the notes' own [std] magnitudes, 1% a year while eligible
# and 2% in the final eligible year, make them visible.  The identity does not depend on
# the values, only on both models having the same ones.
SPLICED_REFS = {"inflation_rate": 0.0, "conv_rate_base": 0.01, "conv_rate_final": 0.02}

# The cells T2 and T3 skip beyond T1's.  proj_len counts from the valuation date on SEC and
# from issue on S, so it differs by d, or by -k, by design; frame_mismatches asserts what
# it must get right, that both frames end at the same instant.  result_cf_annual groups by
# policy year, and a point opened at d lacks S's earlier years and, opened mid-year, holds
# only the rest of the current one (the mid-ART test compares the later years).  A future
# point's years are all whole once its pre-issue months are dropped, so T3 compares it.
SPLICE_EXEMPT = TWIN_EXEMPT_DEFAULT | {"proj_len", "result_cf_annual"}
FUTURE_EXEMPT = TWIN_EXEMPT_DEFAULT | {"proj_len"}

# The decrement rates, none of which may be evaluated before issue (R1, D4).
DECREMENT_RATES = ("mort_rate_base", "mort_rate", "mort_rate_mth", "lapse_rate",
                   "lapse_rate_mth", "conv_rate", "conv_rate_mth")

# The cells that scale with policy_count.  Every other cell is a per-policy amount, a rate,
# a clock or a flag, and must not move when the count does.
COUNTED = frozenset({
    "policy_count", "pols_if_init", "pols_if", "pols_if_at", "pols_new_biz",
    "pols_death", "pols_surv", "pols_conv", "pols_lapse", "pols_maturity",
    "premiums", "commissions", "premium_taxes", "expenses", "claims", "conv_credits",
    "net_cf", "result_cf", "result_cf_annual", "result_pols"})

# result_pols' columns, in its order: the count, the new business within it, the month's
# decrements in processing order, then the expiries of the last covered month.
RESULT_POLS = ["pols_if", "pols_new_biz", "pols_death", "pols_conv", "pols_lapse",
               "pols_maturity"]
OUTFLOWS = RESULT_POLS[2:]

# What each cell holds outside cover, before issue and from the month cover has ended, as
# its docstring says: no count, so no cash flow, no question about the contract answered
# yes, and no contractual scale read at a policy year the month does not have.  The type
# is part of the value.  A count is a float in every branch and a flag a bool, because
# Phase 2 types a cell by the values it returns (USLIB-SEC-PLAN.md F3).
OUTSIDE_COVER = {
    "is_active": False, "prem_due": False, "conv_elig": False,
    "premium_pp_ann": 0.0, "premium_pp": 0.0, "mort_rate_base": 0.0, "comm_rate": 0.0,
    "pols_if": 0.0, "pols_new_biz": 0.0, "pols_death": 0.0, "pols_surv": 0.0,
    "pols_conv": 0.0, "pols_lapse": 0.0, "pols_maturity": 0.0,
    "premiums": 0.0, "commissions": 0.0, "premium_taxes": 0.0, "expenses": 0.0,
    "claims": 0.0, "conv_credits": 0.0, "net_cf": 0.0}

# The cells a month outside cover may not reach: the decrement rates, and the reads keyed by
# a policy year, a PLT duration or an attained age.  mort_rate_base is the one rate the
# guard test calls itself, and is held by its value instead.
IN_COVER_ONLY = ("age", "premium_pp_ann_py", "conv_elig_py", "plt_mort_factor",
                 *(rate for rate in DECREMENT_RATES if rate != "mort_rate_base"))

# The cells running in force adds to Term_US_S's, each of which the symbol map must name.
NEW_CELLS = ("policy_count", "expiry_mth", "duration_mth_init", "t_entry", "is_active",
             "premium_pp_ann_py", "conv_elig_py", "pols_if_at", "pols_new_biz",
             "result_pols")

INFLATION = 0.02        # the shipped inflation_rate, which the inflation test reads

# The recursion limit, as mx.set_recursion takes it, under which the rules test runs the
# reports on a fresh read (R2, F7).  A report evaluates each column in ascending t, so a
# forward recursion, through t - 1, finds the month before already cached: the committed
# points' reports open chains of 10 formula calls at most, and the splice's grid 13.  A
# backward recursion over the frame, through t + 1, opens a chain as long as the frame.
CALL_DEPTH = 40


# ---------------------------------------------------------------------------
# Helpers

_names = itertools.count(1)


def _name(tag):
    """A model name that no other read in this session uses."""
    return f"{SEC}_{tag}_{next(_names)}"


def _point(model, point_id):
    """The ItemSpace of the row labelled ``point_id``, through the registry's keys."""
    keys = dict(zip(model.Data.model_point_table().index, point_keys(model)))
    return projection(model, keys[point_id])


def _label(table, kind, s_point, month):
    """The ``point_id`` of the one ``kind`` row generated from S point ``s_point``.

    ``month`` is the row's ``source_mth``: 0 for a twin, ``d`` for a derived row, ``-k`` for
    a future one.  The twins keep S's ``point_id`` and ``policy_id``, so the S policy is the
    twin's.
    """
    policy = table.at[s_point, "policy_id"]
    hit = table.index[(table["row_kind"] == kind) & (table["source_policy_id"] == policy)
                      & (table["source_mth"] == month)].tolist()
    assert len(hit) == 1, f"{kind} rows of S point {s_point} at month {month}: {hit}"
    return hit[0]


def _row(model, kind, s_point, month):
    """The ItemSpace of that row of ``model``'s table (:func:`_label`)."""
    return _point(model, _label(model.Data.model_point_table(), kind, s_point, month))


def _committed():
    """The committed SEC table as the file holds it, unvalidated, indexed by point_id."""
    return pd.read_csv(model_path(SEC).parent / TABLE, index_col="point_id")


def _sec_inputs(tmp_path, table):
    """A copy of the product directory whose SEC table is ``table``; its SEC folder."""
    return temp_inputs(tmp_path, model_path(SEC), model_points=table,
                       model_point_file=TABLE)


def _read_edited(tmp_path, edit):
    """Term_US_SEC read from a copy whose SEC table is ``edit(_committed())``."""
    return mx.read_model(_sec_inputs(tmp_path, edit(_committed())), name=_name("edited"))


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
    """Evaluate on an S point what the splice compares: the sweep, and three cells more.

    :func:`sec_support.sweep` reaches neither ``pols_lapse``, ``pols_maturity`` nor
    ``phase``, because no result column reads them on S, and a cell S never evaluates is
    compared nowhere.  They are evaluated here over the frame, so the splice and the future
    comparison see them too.  The month after the frame is not: the comparison is held to
    S's own frame (:func:`sec_support.twin_mismatches`), and ``phase`` reads ``EXPIRED``
    there by the two-clocks test.
    """
    sweep(proj)
    for t in range(proj.proj_len()):
        proj.pols_lapse(t)
        proj.pols_maturity(t)
        proj.phase(t)


def _case_id(kind, s_point, month):
    """A T2 case's id: ``point1-d12`` for a derived row, ``point1-twin108`` for a twin."""
    return f"point{s_point}-" + (f"d{month}" if kind == "derived" else f"{kind}{month}")


# ---------------------------------------------------------------------------
# Fixtures


@pytest.fixture(scope="module")
def sec_model():
    """Term_US_SEC read in place, as committed."""
    model = mx.read_model(model_path(SEC), name=_name("sec"))
    yield model
    model.close()


@pytest.fixture(scope="module")
def s_model():
    """Term_US_S read in place, as committed, with every point swept.

    T6 regenerates the SEC table from it, which would otherwise project every S point again
    (USLIB-SEC-PLAN.md §4, *Carried into Phase 1*), and the in-force tests read S's months
    off it.
    """
    model = mx.read_model(model_path(TWIN), name=_name("s"))
    for key in point_keys(model):
        sweep(projection(model, key))
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


def _premium_rates_with_t20(rates):
    """``premium_rates.csv`` with a T20 scale beside the T10 one, for variant 4 alone.

    T10's level premium for twenty policy years, then T10's renewal premiums from its jump
    on, moved ten years later: the jump falls at year 21, the jump ratio is T10's, and the
    scale runs to year 60 like T10's.  A copy's file only, never the committed one.
    """
    t10 = rates[rates["plan"] == "T10"]
    level, renewal = t10[t10["policy_year"] <= 10], t10[t10["policy_year"].between(11, 50)]
    t20 = pd.concat([level, level.assign(policy_year=level["policy_year"] + 10),
                     renewal.assign(policy_year=renewal["policy_year"] + 10)])
    return pd.concat([rates, t20.assign(plan="T20", provenance="T10 moved on, for a test")],
                     ignore_index=True)


# The input files the splice's copies change, S's and SEC's alike.
SPLICED_EDITS = {"premium_rates.csv": _premium_rates_with_t20}


@pytest.fixture(scope="module")
def spliced(tmp_path_factory):
    """S and SEC on the splice's inputs, with :data:`SPLICED_REFS` set in both.

    S is read from a copy of the product directory whose table has the variants appended,
    and whose premium table has variant 4's T20 scale (:data:`SPLICED_EDITS`).  SEC runs
    on the same premium table, and on a model point table of its own, built by the
    generator from the registered spec with its rows replaced by :data:`SPLICES` and
    :data:`FUTURES`, out of this S model, so each row opens with the count of the very run
    it is compared with.  No input table moves with ``d``: Term's one valuation-clock input
    is the ``inflation_rate`` Reference.
    """
    root = tmp_path_factory.mktemp("spliced")
    s_folder = temp_inputs(root / "s", model_path(TWIN),
                           model_points=_s_table_with_variants(), edits=SPLICED_EDITS)
    s = mx.read_model(s_folder, name=_name("s_spliced"))
    for ref, value in SPLICED_REFS.items():
        setattr(s.Projection, ref, value)
    spec = dataclasses.replace(SEC_SPECS[SEC], derived=tuple((p, d) for _, p, d in SPLICES),
                               future=FUTURES)
    table, companions = build_sec_table(spec, s)
    assert companions == {}
    sec_folder = temp_inputs(root / "sec", model_path(SEC), model_points=table,
                             model_point_file=spec.model_point_file, edits=SPLICED_EDITS)
    sec = mx.read_model(sec_folder, name=_name("sec_spliced"))
    for ref, value in SPLICED_REFS.items():
        setattr(sec.Projection, ref, value)
    for key in point_keys(s):
        _sweep_s(projection(s, key))
    yield s, sec
    sec.close()
    s.close()


# ---------------------------------------------------------------------------
# T2 -- the splice


@pytest.mark.parametrize("kind, s_point, month", SPLICES + IN_FORCE_TWINS,
                         ids=[_case_id(*case) for case in SPLICES + IN_FORCE_TWINS])
def test_an_in_force_point_continues_its_s_projection(spliced, kind, s_point, month):
    """Opened with S's count at month d, the point is S from d on, in every cell of S's.

    This is the test that says the opening state is complete: a state variable the SEC row
    did not carry would make SEC part from S here, and nowhere else, because on a point
    issued at ``t = 0`` the two clocks coincide.  For the same reason it is the test that
    catches a policy month passed as ``t`` (R1a).  The frame comparison reads SEC row ``t``
    against S row ``t + d`` in every ``result_cf`` column and fails frames that end apart;
    the cell comparison then evaluates every cell of S's but :data:`SPLICE_EXEMPT`, at
    every argument S cached inside its own frame from month ``d`` on, moved onto SEC's
    clock, the state cell ``pols_if`` and every result column among them, to 1e-9.  An S
    cell this model lacked would fail it.  The variants' cases, on S points 3 to 5, are the
    only ones that see the conversion window's age limit, a premium cycle shorter than a
    year, a level period other than ten years, and cover that ends with the level period.
    """
    s, sec = spliced
    s_proj, sec_proj = _point(s, s_point), _row(sec, kind, s_point, month)
    assert frame_mismatches(s_proj.result_cf(), sec_proj.result_cf(), t_offset=month) == []
    assert twin_mismatches(s_proj, sec_proj, t_offset=month, exempt=SPLICE_EXEMPT) == []


# ---------------------------------------------------------------------------
# T3 -- future new business


@pytest.mark.parametrize("s_point, k", FUTURES, ids=[f"point{p}-k{k}" for p, k in FUTURES])
def test_future_new_business_is_the_s_projection_k_months_on(spliced, s_point, k):
    """Issued k months after the valuation date, the point is S's projection k months on.

    SEC rows ``k ..`` are S rows ``0 ..``, ending together at the end of cover, and every
    cell of S's but :data:`FUTURE_EXEMPT` agrees at every argument S cached inside its own
    frame, moved ``k`` later, ``result_cf_annual`` included: once its pre-issue months are
    dropped, its policy years are S's.  An S cell this model lacked would fail it.  Before
    issue every ``result_cf`` and ``result_pols`` column is an exact zero, and the policies
    arrive in month ``k`` as new business.

    The last assertion is R1 and D4's base rule made testable.  After every report, no
    decrement rate has been evaluated at a month before issue.  A count recursion based at
    ``t == 0`` rather than at ``t_entry()``, or a decrement count that evaluates its rate
    before asking whether the month is in cover, still gives the right numbers.  This is
    the only test that sees the first, and the guard test sees the second too.

    The pre-issue rows are asserted present before they are asserted zero: a frame that
    opened at issue would have none, and their zeros would hold of nothing.
    """
    s, sec = spliced
    s_proj, sec_proj = _point(s, s_point), _row(sec, "future", s_point, -k)
    df, pols = sec_proj.result_cf(), sec_proj.result_pols()
    sec_proj.result_cf_annual()
    assert frame_mismatches(s_proj.result_cf(), df, t_offset=-k) == []
    assert twin_mismatches(s_proj, sec_proj, t_offset=-k, exempt=FUTURE_EXEMPT) == []
    assert list(df.index[:k]) == list(pols.index[:k]) == list(range(k))
    assert (df.loc[:k - 1] == 0.0).all().all()
    assert (pols.loc[:k - 1] == 0.0).all().all()
    assert sec_proj.pols_new_biz(k) == sec_proj.policy_count() == 1.0
    early = {name: sorted(t for t in sec_proj.cells[name].keys() if t < k)
             for name in DECREMENT_RATES}
    assert not any(early.values()), f"rates evaluated before issue: {early}"


# ---------------------------------------------------------------------------
# D11's R1 and R2, and D3's closed-form clock


def _cached_args(cells):
    """The argument tuple of every key ``cells`` has cached (:func:`sec_support._args`)."""
    n = len(cells.parameters)
    return [() if n == 0 else (key,) if n == 1 else tuple(key)
            for key in list(cells.keys())]


def _month(x):
    return isinstance(x, int) and not isinstance(x, bool)


def test_no_cell_is_called_before_the_valuation_date_or_reads_far_ahead(spliced):
    """R1, R2 and D3, on the splice's grid and on a fresh read of the committed model.

    Each is a rule of how the model computes, not of what, so no number shows a breach,
    and on a point issued at ``t = 0`` the two clocks coincide and hide it from T1 too.
    The splice's grid holds points in force at every month T2 names, the variants among
    them, and points issued later, and on each the three reports are run first:

    * R1: no cell holds a negative argument.  modelx evaluates one without complaint, and
      a compiled cache raises ``IndexError`` below 0 (USLIB-SEC-PLAN.md F4).  A policy
      month turned into ``t`` by subtracting ``duration_mth_init()`` (R1a) goes negative
      on a point in force past it.
    * R2's look-ahead: no cell evaluated at month ``t`` read a cell keyed by month beyond
      ``t + 1``, as modelx's dependency graph records each cached call's precedents.
      ``Term_US_S``'s ``conv_rate`` asked twelve months ahead for the final year.

    The other two need a model on which nothing has been evaluated yet, so they run on a
    fresh read of the committed model:

    * D3: the policy clock is the closed form.  Called first, ``duration_mth(500)``
      evaluates ``duration_mth`` once, where ``BasicTerm_SE``'s recursion would evaluate
      it at all 501 months from 0.
    * R2's recursions run forward: under modelx's recursion limit lowered to
      :data:`CALL_DEPTH`, the three reports run on every committed point, each column in
      ascending ``t``.  A forward recursion, through ``t - 1``, finds the month before
      already cached and stays shallow, which is why D3 is asserted on its own.  A
      backward recursion over the frame, through ``t + 1``, keeps every step within the
      look-ahead but opens a chain as long as the frame, which a compiled model would run
      on the C stack (F7), and fails here.
    """
    sec = spliced[1]
    negative, ahead = set(), set()
    for key in point_keys(sec):
        p = projection(sec, key)
        for report in ("result_cf", "result_pols", "result_cf_annual"):
            p.cells[report]()
        for name, cells in p.cells.items():
            t_pos = cells.parameters.index("t") if "t" in cells.parameters else None
            for args in _cached_args(cells):
                if any(_month(a) and a < 0 for a in args):
                    negative.add(f"{name}{args}")
                if t_pos is None:
                    continue
                for node in cells.preds(*args):
                    params = getattr(node.obj, "parameters", None) or ()
                    u = node.args[params.index("t")] if "t" in params else None
                    if _month(u) and u > args[t_pos] + 1:
                        ahead.add(f"{name}{args} -> {node.obj.name}{node.args}")
    assert not negative, f"called before the valuation date: {sorted(negative)[:10]}"
    assert not ahead, f"read beyond t + 1: {sorted(ahead)[:10]}"
    deep, limit = [], mx.get_recursion()
    fresh = mx.read_model(model_path(SEC), name=_name("fresh"))
    try:
        p = _row(fresh, "twin", 1, 0)
        assert p.duration_mth(500) == 500
        assert list(p.cells["duration_mth"].keys()) == [500]
        labels = fresh.Data.model_point_table().index
        mx.set_recursion(CALL_DEPTH)
        try:
            for key, point_id in zip(point_keys(fresh), labels):
                p = projection(fresh, key)
                for report in ("result_cf", "result_pols", "result_cf_annual"):
                    try:
                        p.cells[report]()
                    except Exception as err:    # reported, so every point is run
                        deep.append(f"point {point_id}: {report}() raised {_raised(err)}")
                        break
        finally:
            mx.set_recursion(limit)
    finally:
        fresh.close()
    assert not deep, f"under a recursion limit of {CALL_DEPTH}: {deep}"


# ---------------------------------------------------------------------------
# T4 -- the count algebra
#
# BEF_DECR == BEF_NB + pols_new_biz, at every t of every point, is a convention
# (test_new_business_joins_the_count_before_decrements), and is not repeated here.


def test_the_count_rolls_forward_through_new_business_and_decrements(sec_model):
    """The count leaves month t by its deaths, conversions, lapses and expiries alone.

    On every committed point and at every ``t`` of its frame, the count weighting month
    ``t``, ``pols_if_at(t, "BEF_DECR")``, less the count carried into ``t + 1``,
    ``pols_if_at(t + 1, "BEF_NB")``, is the four outflows of month ``t``, to 1e-12.  The
    step from the last row to ``t = proj_len()`` is what catches cover that runs a month too
    long: the expiries would then leave a month late, and the count would carry over.

    ``result_pols()`` sets the same movement out row by row, in :data:`RESULT_POLS`'s
    columns, indexed by ``t`` over the frame: ``pols_if`` at ``t + 1`` is ``pols_if`` less
    the outflows at ``t``, plus the new business of ``t + 1``, and row 0 opens from
    ``pols_if_init()``.
    """
    table = sec_model.Data.model_point_table()
    for key, point_id in zip(point_keys(sec_model), table.index):
        p = projection(sec_model, key)
        for t in range(p.proj_len()):
            out = p.pols_death(t) + p.pols_conv(t) + p.pols_lapse(t) + p.pols_maturity(t)
            moved = p.pols_if_at(t, "BEF_DECR") - p.pols_if_at(t + 1, "BEF_NB")
            assert moved == pytest.approx(out, abs=1e-12), (point_id, t)
        pols = p.result_pols()
        assert list(pols.columns) == RESULT_POLS, point_id
        assert pols.index.name == "t" and list(pols.index) == list(range(p.proj_len()))
        carried = (pols["pols_if"] - pols[OUTFLOWS].sum(axis=1)).shift(1)
        expected = carried.fillna(p.pols_if_init()) + pols["pols_new_biz"]
        assert ((pols["pols_if"] - expected).abs() <= 1e-12).all(), point_id


def test_doubling_the_count_doubles_every_flow_and_no_per_policy_value(sec_model, tmp_path):
    """``policy_count`` is a weight: twice the count, twice every flow, the same per policy.

    The committed table with every count doubled is read from a copy.  On every point
    ``result_cf``, ``result_pols`` and ``result_cf_annual`` are twice the committed model's,
    element by element, to 1e-12 relative: a doubled count is a computed float, which may
    come back from the CSV within two ulps (``sec_support``'s module docstring).  And every
    cell outside :data:`COUNTED` (the premium per policy, the face amount, the rates, both
    clocks, the flags) agrees with the committed model at every argument the committed
    model's sweep cached.
    """
    table = _committed()
    doubled = mx.read_model(_sec_inputs(tmp_path, table.assign(
        policy_count=2 * table["policy_count"])), name=_name("doubled"))
    try:
        for key, two_key in zip(point_keys(sec_model), point_keys(doubled)):
            base, two = projection(sec_model, key), projection(doubled, two_key)
            sweep(base)
            for report in ("result_cf", "result_pols", "result_cf_annual"):
                b, d = base.cells[report](), two.cells[report]()
                assert d.index.equals(b.index) and list(d.columns) == list(b.columns)
                bad = ((d - 2 * b).abs() > 1e-12 * (2 * b).abs()).any()
                assert not bad.any(), (key, report, list(bad[bad].index))
            assert twin_mismatches(base, two, exempt=TWIN_EXEMPT_DEFAULT | COUNTED) == []
    finally:
        doubled.close()


# ---------------------------------------------------------------------------
# T5 -- validation
#
# Each malformed table is the committed one with one fault, read from a copy.  The checks
# run over the whole table as it is read, in Data, and the message names the column or
# every point at fault.  A blank cell reads as NaN, and so does a text cell once the checks
# coerce the column to numbers, so each is refused as a count, or a duration, that is not a
# number.  The repeated point_id holds another policy under the same label, as a bad
# extract would, so that the check must look at the labels and not at whole rows.

MALFORMED = [
    ("a negative count", _set("policy_count", [4], -0.1),
     "policy_count must be a number, zero or more; it is not at point_id [4]"),
    ("a blank count", _set("policy_count", [3], float("nan")),
     "policy_count must be a number, zero or more; it is not at point_id [3]"),
    ("two bad counts", _set("policy_count", [3, 5], -1.0),
     "policy_count must be a number, zero or more; it is not at point_id [3, 5]"),
    ("a text count", _set("policy_count", [4], "abc"),
     "policy_count must be a number, zero or more; it is not at point_id [4]"),
    ("an infinite count", _set("policy_count", [4], float("inf")),
     "policy_count must be a number, zero or more; it is not at point_id [4]"),
    ("a fractional duration", _set("duration_mth", [4], 126.5),
     "duration_mth must be a whole number of months; it is not at point_id [4]"),
    ("a blank duration", _set("duration_mth", [6], float("nan")),
     "duration_mth must be a whole number of months; it is not at point_id [6]"),
    ("a text duration", _set("duration_mth", [4], "x12"),
     "duration_mth must be a whole number of months; it is not at point_id [4]"),
    ("issued beyond the horizon", _set("duration_mth", [6], -121),
     "duration_mth must be -120 or more, a policy issued at most 120 months after the "
     "valuation date; it is not at point_id [6]"),
    ("no duration column", lambda t: t.drop(columns="duration_mth"),
     "model_point_table_sec.csv has no duration_mth column"),
    ("no count column", lambda t: t.drop(columns="policy_count"),
     "model_point_table_sec.csv has no policy_count column"),
    ("a repeated point_id",
     lambda t: pd.concat([t, t.loc[[3]].assign(policy_id="TL-000009")]),
     "model_point_table_sec.csv: point_id [3] appears more than once"),
]


@pytest.mark.parametrize("case, edit, message", MALFORMED, ids=[c[0] for c in MALFORMED])
def test_a_malformed_in_force_row_is_refused_naming_its_point(tmp_path, case, edit,
                                                               message):
    """``Data.model_point_table()`` refuses the table, naming the fault (D6, T5)."""
    model = _read_edited(tmp_path, edit)
    try:
        _refused(model.Data.model_point_table, message)
    finally:
        model.close()


def test_the_future_horizon_is_a_reference_that_bounds_future_business(tmp_path):
    """``Data.future_horizon_mth`` refuses a policy issued later than it, and 0 refuses all.

    The committed table's one future point is issued three months on.  It reads at the
    shipped 120 months and at 3, the shortest horizon that admits it, and is refused at 2,
    by name.  At 0 the model takes no future new business, D4's fallback for a product
    that cannot support it, and the message says so.  A negative horizon is itself
    refused.  Setting the Reference clears the table, so each value is read afresh.
    """
    future = _label(_committed(), "future", 1, -3)
    later = (f"model_point_table_sec.csv: duration_mth must be -2 or more, a policy issued "
             f"at most 2 months after the valuation date; it is not at point_id [{future}]")
    no_future = (f"model_point_table_sec.csv: duration_mth must be 0 or more: this model "
                 f"takes no future new business; it is not at point_id [{future}]")
    model = mx.read_model(_sec_inputs(tmp_path, _committed()), name=_name("horizon"))
    try:
        assert model.Data.future_horizon_mth == 120
        negative = "future_horizon_mth must be 0 months or more, not -1"
        for horizon, refusal in ((3, None), (2, later), (0, no_future), (-1, negative),
                                 (120, None)):
            model.Data.future_horizon_mth = horizon
            if refusal is None:
                assert len(model.Data.model_point_table()) == len(_committed()), horizon
            else:
                _refused(model.Data.model_point_table, refusal)
    finally:
        model.close()


def test_a_point_past_its_cover_is_refused_by_proj_len(tmp_path):
    """A point whose cover has ended has no frame, and ``proj_len()`` refuses it by name.

    The point in its last covered month is moved on to ``duration_mth`` 720, the month
    cover ends.  That is a rule of the product, not of the table: it needs ``expiry_age``,
    a Projection Reference, so the table reads, and the point is refused where its frame is
    defined, on its first projection, rather than projecting nothing.  A loop over the
    block would meet it only at that point, after projecting the points before it, so
    ``run_sec.py --block``, run beside the table, asks every point for its frame first: it
    fails naming the point, and prints nothing before.
    """
    last = _label(_committed(), "derived", 1, 719)
    model = _read_edited(tmp_path, _set("duration_mth", [last], 720))
    message = (f"point_id {last}: duration_mth 720 is at or past the end of cover, "
               f"policy month 720")
    try:
        assert len(model.Data.model_point_table()) == len(_committed())
        _refused(_row(model, "derived", 1, 719).result_cf, message)
    finally:
        model.close()
    runner = tmp_path / "run_sec.py"
    shutil.copy(model_path(SEC).parent / "run_sec.py", runner)
    done = _run_sec(runner, "--block", check=False)
    assert done.returncode != 0 and done.stdout == b""
    assert message in done.stderr.decode(errors="replace")


def test_the_edges_of_the_in_force_interface_are_accepted(tmp_path):
    """A zero count, durations written as floats and the horizon itself read and project.

    A count of 0 is a point that projects zeros; ``12.0`` is a whole number of months, read
    back as the int the policy clock counts in; and a policy issued 120 months after the
    valuation date, the shipped ``future_horizon_mth``, is the last one the table admits,
    with a frame of 840 months, 720 of cover after 120 before issue.
    """
    committed = _committed()
    last = _label(committed, "derived", 1, 719)
    future = _label(committed, "future", 1, -3)

    def edit(table):
        table = _set("policy_count", [last], 0.0)(table)
        table = table.assign(duration_mth=table["duration_mth"].astype(float))
        return _set("duration_mth", [future], -120.0)(table)

    model = _read_edited(tmp_path, edit)
    try:
        assert model.Data.model_point_table()["duration_mth"].dtype == float
        df = _row(model, "derived", 1, 719).result_cf()
        assert len(df) == 1 and (df == 0.0).all().all()
        mid = _row(model, "derived", 1, 126)
        assert mid.duration_mth(0) == 126 and type(mid.duration_mth(0)) is int
        late = _row(model, "future", 1, -3)
        assert (late.t_entry(), late.proj_len(), late.pols_new_biz(120)) == (120, 840, 1.0)
    finally:
        model.close()


# ---------------------------------------------------------------------------
# T6 -- regeneration


def test_the_committed_sec_table_is_what_s_generates(s_model):
    """``model_point_table_sec.csv`` is what ``Term_US_S`` and its table generate today.

    Every row and column, the text cells included: an edit to an S row the table copies or
    derives from fails here until ``python tools/gen_sec_points.py Term_US_SEC`` regenerates
    it, in the same commit.  Text and integers compare exactly, and a float by its value, to
    1e-12, because the text the writer picks for a computed float depends on the platform's
    parser (§5.2).
    """
    assert check_generated(SEC, s_model=s_model) == []


# ---------------------------------------------------------------------------
# The product's own facts


def test_the_two_clocks_on_the_shipped_points(sec_model):
    """``t`` counts from the valuation date; ``duration_mth(t)`` from issue (D3, D4).

    On a twin the two coincide, and its policies enter as new business at ``t = 0``.  The
    point in force 126 months is in policy year 11 at attained age 45 at ``t = 0``, has 594
    months of cover left, and expires at ``t = 594``.  The point issued three months on has
    nothing in force and nothing to do before ``t = 3``, its phase reading ``PRE_ISSUE``,
    and a frame of 723 months.  The point in its last covered month has a one-month frame,
    in which its survivors expire.  And ``pols_if_at`` knows its two timings alone:
    ``basiclife.BasicTerm_SE``'s ``"BEF_MAT"``, which a formula ported from it might ask
    for, is refused rather than answered with another count.
    """
    twin = _row(sec_model, "twin", 1, 0)
    assert [twin.duration_mth(t) for t in (0, 1, 719)] == [0, 1, 719]
    assert (twin.t_entry(), twin.pols_if_init(), twin.pols_new_biz(0), twin.pols_if(0)) == (
        0, 0.0, 1.0, 1.0)
    mid = _row(sec_model, "derived", 1, 126)
    assert (mid.duration_mth(0), mid.duration(0), mid.policy_year(0), mid.age(0)) == (
        126, 10, 11, 45)
    assert (mid.duration_mth(6), mid.policy_year(6), mid.age(6)) == (132, 12, 46)
    assert (mid.t_entry(), mid.expiry_mth(), mid.proj_len()) == (0, 720, 594)
    assert mid.is_active(593) and not mid.is_active(594)
    assert (mid.phase(0), mid.phase(594)) == ("PLT", "EXPIRED")
    fut = _row(sec_model, "future", 1, -3)
    assert (fut.duration_mth(0), fut.t_entry(), fut.proj_len()) == (-3, 3, 723)
    assert not fut.is_active(2) and fut.is_active(3)
    assert [fut.phase(t) for t in (0, 2, 3, 722, 723)] == [
        "PRE_ISSUE", "PRE_ISSUE", "LEVEL", "PLT", "EXPIRED"]
    assert (fut.pols_if_init(), fut.pols_new_biz(3), fut.pols_if(3)) == (0.0, 1.0, 1.0)
    last = _row(sec_model, "derived", 1, 719)
    assert (last.proj_len(), last.age(0), last.policy_year(0)) == (1, 94, 60)
    assert last.pols_maturity(0) > 0.0 and last.pols_if(1) == 0.0
    assert last.pols_if(0) - last.pols_maturity(0) == pytest.approx(
        last.pols_death(0) + last.pols_lapse(0) + last.pols_conv(0), abs=1e-15)
    _refused(lambda: twin.pols_if_at(0, "BEF_MAT"), "invalid timing")


def test_a_policy_in_force_mid_art_pays_its_next_premium_on_its_anniversary(sec_model,
                                                                            s_model):
    """In force 126 months, the anchor cell is midway through its first ART year, year 11.

    It opens with the count S carries into month 126, which is ``pols_if_init()`` and the
    count of row 0.  The year's premium fell due on the tenth anniversary, six months before
    the valuation date, so none falls due until ``t = 6``, the eleventh anniversary, which
    collects policy year 12's 830.0.  Mortality is policy year 11's, at M(1), then year
    12's, at M(2); the lapse rate and the commission are the ART years'.  Every column that
    does not carry inflation is S's from month 126 on.  Summed into policy years, the table
    opens at year 11 with the rest of that year, which holds no premium and counts the
    policies in force at the valuation date, and from year 12 on it is S's.

    The opening count is S's, read back from the CSV, so it is compared with S's value to
    1e-12; among the SEC model's own cells the equality is exact.
    """
    p, s = _row(sec_model, "derived", 1, 126), _point(s_model, 1)
    assert p.policy_count() == pytest.approx(s.pols_if(126), rel=1e-12)
    assert p.pols_if(0) == p.pols_if_init() == p.policy_count()
    assert [p.premium_pp(t) for t in range(7)] == [0.0] * 6 + [830.0]
    assert p.mort_rate(0) == pytest.approx(0.0018 * 3.50, rel=1e-12)
    assert p.mort_rate(6) == pytest.approx(0.0020 * 3.35, rel=1e-12)
    assert (p.lapse_rate(0), p.lapse_rate(6), p.comm_rate(6)) == (0.30, 0.15, 0.02)
    cols = ["pols_if", "premiums", "claims", "commissions", "premium_taxes",
            "conv_credits"]
    assert frame_mismatches(s.result_cf(), p.result_cf(), t_offset=126,
                            columns=cols) == []
    ann, s_ann = p.result_cf_annual(), s.result_cf_annual()
    assert list(ann.index) == list(range(11, 61))
    assert ann.loc[11, "pols_if"] == p.pols_if(0) and ann.loc[11, "premiums"] == 0.0
    pd.testing.assert_frame_equal(ann.loc[12:, cols], s_ann.loc[12:, cols],
                                  rtol=1e-9, atol=1e-9)


def test_expense_inflation_runs_on_the_valuation_clock(sec_model, s_model):
    """Maintenance is in valuation-date dollars, for every point alike (D7).

    At the shipped 2%, the factor at ``t`` is ``1.02^(t/12)`` on the point in force 126
    months and on the point issued three months on alike, whatever their durations.  So the
    point in force pays S's month-``126 + t`` maintenance deflated by ``1.02^(126/12)``, the
    inflation S had already applied since issue, and the future point pays S's month-``t``
    maintenance inflated by ``1.02^(3/12)``, the inflation of the months before its issue.
    Acquisition is not inflated on either.  This is the only test that sees inflation run on
    the policy clock: the splice sets the rate to 0, and on a point issued at ``t = 0`` the
    clocks agree.
    """
    assert sec_model.Projection.inflation_rate == INFLATION
    mid, fut = _row(sec_model, "derived", 1, 126), _row(sec_model, "future", 1, -3)
    s = _point(s_model, 1)
    for t in (0, 6, 12):
        assert mid.inflation_factor(t) == fut.inflation_factor(t) == (
            (1 + INFLATION) ** (t / 12))
    for t in range(mid.proj_len()):
        assert mid.expenses(t) == pytest.approx(
            s.expenses(126 + t) / (1 + INFLATION) ** (126 / 12), rel=1e-12), t
    for t in range(s.proj_len()):
        acq = s.expense_acq if t == 0 else 0.0
        assert fut.expenses(3 + t) - acq == pytest.approx(
            (s.expenses(t) - acq) * (1 + INFLATION) ** (3 / 12), rel=1e-12), t


def test_acquisition_is_charged_on_new_business_only(sec_model):
    """``expense_acq`` per policy issued, in the issue month, never on a policy in force.

    On every committed point, what ``expenses(t)`` holds beyond its maintenance part is
    ``expense_acq * policy_count()`` in the issue month, ``t = -duration_mth``, and 0 in
    every other month, to 1e-9: the twins bear it at ``t = 0``, the points already in force
    never, and the point issued three months on at ``t = 3``.

    ``Term_US_S`` charges it once per model point, whatever the count, so the twins (T1)
    and the future rows (T3) agree with S cell by cell only while each S point counts
    one policy, as S's points do.  That is asserted first, so that an S table with
    another count fails here, saying why, beside T1 and T3 failing on the issue month's
    ``expenses``.
    """
    table = sec_model.Data.model_point_table()
    twins = table[table["row_kind"] == "twin"]
    assert (twins["policy_count"] == 1.0).all(), (
        f"T1 and T3 hold on Term only while each S point counts one policy (sec_support's "
        f"SecSpec comment); the twins count {twins['policy_count'].tolist()}")
    for key, point_id in zip(point_keys(sec_model), table.index):
        p = projection(sec_model, key)
        ts = range(p.proj_len())
        acq = [p.expenses(t) - p.expense_maint / 12 * p.inflation_factor(t) * p.pols_if(t)
               for t in ts]
        issue = -table.at[point_id, "duration_mth"]
        expected = [p.expense_acq * p.policy_count() if t == issue else 0.0 for t in ts]
        assert acq == pytest.approx(expected, abs=1e-9), point_id


def test_every_guarded_cell_holds_its_outside_cover_value():
    """Outside cover each cell holds :data:`OUTSIDE_COVER`'s value, and reads no rate.

    On every committed point, in every month before issue and in the first month after
    cover, ``t = proj_len()``, which the count's look-ahead reads, on a model that evaluates
    nothing else.  So afterwards none of :data:`IN_COVER_ONLY` may hold a value at all:
    ``is_active``'s docstring promises that outside cover no count evaluates a rate, and no
    table is read at a policy year or an attained age the policy does not have.

    Several of these guards change no number the frame shows: once the counts are zero
    outside cover, nothing reads ``mort_rate_base`` or ``conv_elig`` there, and an unguarded
    count multiplies its rate by zero.  They are held here because they are what the
    docstrings promise a caller, and because Phase 2 needs them: a table read at a policy
    year or an age the policy does not have would wrap round in a compiled model rather than
    fail (USLIB-SEC-PLAN.md F4, R1).  A cell that raises instead is reported as a fault too.
    """
    model = mx.read_model(model_path(SEC), name=_name("cover"))
    try:
        faults = []
        table = model.Data.model_point_table()
        for key, point_id in zip(point_keys(model), table.index):
            p = projection(model, key)
            for t in [*range(p.t_entry()), p.proj_len()]:
                calls = [(name, (t,), want) for name, want in OUTSIDE_COVER.items()]
                calls += [("pols_if_at", (t, timing), 0.0)
                          for timing in ("BEF_NB", "BEF_DECR")]
                for name, args, want in calls:
                    where = f"point {point_id}: {name}{args}"
                    try:
                        got = p.cells[name](*args)
                    except Exception as err:        # reported, so the scan goes on
                        faults.append(f"{where} raised {_raised(err)}")
                        continue
                    if got != want or type(got) is not type(want):
                        faults.append(f"{where} = {got!r}, not {want!r}")
            read = {name: sorted(p.cells[name].keys()) for name in IN_COVER_ONLY
                    if len(p.cells[name].keys())}
            if read:
                faults.append(f"point {point_id}: evaluated outside cover: {read}")
    finally:
        model.close()
    assert not faults, f"{len(faults)} faults outside cover, first:\n  " + "\n  ".join(
        faults[:20])


def test_the_points_sum_row_by_row_into_a_block(spliced):
    """Row ``t`` is the same month on every point, so a block is its frames summed (D3).

    For each S point, the frames of its twin, of the point restated at month 12 and of the
    point issued 12 months on, summed as ``run_sec.py --block`` sums them, are indexed
    0..731 and equal S's frame added to itself moved 12 months earlier and 12 months later.
    A model whose frames sat on the policy clock would fail it.
    """
    s, sec = spliced
    for s_point in S_POINTS:
        frames = [_row(sec, "twin", s_point, 0).result_cf(),
                  _row(sec, "derived", s_point, 12).result_cf(),
                  _row(sec, "future", s_point, -12).result_cf()]
        block = pd.concat(frames).groupby(level="t").sum()
        sdf = _point(s, s_point).result_cf()
        expected = pd.concat([sdf, sdf.set_axis(sdf.index - 12).loc[0:],
                              sdf.set_axis(sdf.index + 12)]).groupby(level=0).sum()
        assert list(block.index) == list(range(732))
        assert frame_mismatches(expected, block) == [], s_point


def _run_sec(script, arg, check=True):
    """Run ``script``, a ``run_sec.py``, with one argument; its output, checked ASCII.

    With ``check=False`` the finished process is returned instead, whatever its exit code,
    for a test that expects the runner to fail.
    """
    done = subprocess.run([sys.executable, str(script), arg], capture_output=True,
                          timeout=300)
    if not check:
        return done
    assert done.returncode == 0, done.stderr.decode(errors="replace")
    assert done.stdout.isascii(), "run_sec.py printed a non-ASCII character"
    return done.stdout.decode("ascii")


def test_an_in_force_extract_needs_none_of_the_generator_columns(sec_model, tmp_path):
    """The model reads the in-force interface and S's columns, never where a row came from.

    ``row_kind``, ``source_policy_id`` and ``source_mth`` record how the generator made each
    shipped row, and an administration extract carries none of them.  Read without them,
    every point projects what the committed table projects, in ``result_cf`` and
    ``result_pols``, to 1e-12, and ``run_sec.py``, run beside that extract, prints the point
    without saying where it came from.  On the shipped rows ``source_mth`` equals
    ``duration_mth``, so a formula that read the one for the other would pass every test
    that leaves ``duration_mth`` as generated.
    """
    extract = _committed().drop(columns=list(GENERATED_COLUMNS))
    folder = _sec_inputs(tmp_path, extract)
    model = mx.read_model(folder, name=_name("extract"))
    try:
        table = model.Data.model_point_table()
        assert not set(GENERATED_COLUMNS) & set(table.columns)
        assert list(table.index) == list(sec_model.Data.model_point_table().index)
        for key, base_key in zip(point_keys(model), point_keys(sec_model)):
            mine, base = projection(model, key), projection(sec_model, base_key)
            for report in ("result_cf", "result_pols"):
                assert frame_mismatches(base.cells[report](), mine.cells[report](),
                                        rtol=1e-12, atol=1e-12) == [], (key, report)
    finally:
        model.close()
    runner = folder.parent / "run_sec.py"
    shutil.copy(model_path(SEC).parent / "run_sec.py", runner)
    out = _run_sec(runner, "4")
    assert "model point 4: TL-000001-M126 - M35" in out
    assert "in force 126 months" in out


def test_run_sec_prints_a_point_and_the_block(sec_model):
    """The runner prints one point, saying where it came from, and the block (D8).

    Each mode in an interpreter of its own, as a user runs it, with exit code 0 and ASCII
    output, so that it prints on a Windows console under any code page.  The numbers are
    the model's: point 4's line at the valuation date and its first twelve rows, and the
    block's first twelve rows, which must be the committed points' frames summed row by
    row, as this test sums them.  Nothing else runs the runner on the committed table.
    """
    runner = model_path(SEC).parent / "run_sec.py"
    out = _run_sec(runner, "4")
    assert "TL-000001-M126 (S's TL-000001 at its month 126)" in out
    assert "in force 126 months: policy year 11, attained age 45, 0.108385 in force" in out
    mid = _row(sec_model, "derived", 1, 126)
    assert mid.result_cf().head(12).round(2).to_string() in out
    out = _run_sec(runner, "--block")
    assert "the block" in out and "TL-000001-F3" in out
    frames = [projection(sec_model, key).result_cf() for key in point_keys(sec_model)]
    block = pd.concat(frames).groupby(level="t").sum()
    assert block.head(12).round(2).to_string() in out


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
    opens the column, ``age`` of ``age(t)``.
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


def test_the_docstrings_describe_the_valuation_clock(sec_model):
    """The docstrings say what this model is, and none says what only Term_US_S is.

    Whitespace is collapsed first, as ``test_model_conventions`` collapses it, so that a
    phrase split across a line break still matches.  The model docstring names the
    valuation date, BasicTerm_SE, the policy clock, the SEC table and the product.  The
    symbol map in the Projection docstring maps every cell running in force adds, and names
    no cell the model lacks.  And no docstring carries a reference into the twin's Spaces
    (``~.Term_US_S.``), which the SEC pages would link to the wrong model, or S's
    "``t = 0`` is the issue month".
    """
    flat = {where: re.sub(r"\s+", " ", doc) for where, doc in _docs(sec_model)}
    for phrase in ("valuation date", "BasicTerm_SE", "duration_mth", TABLE,
                   "level premium term life insurance"):
        assert phrase in flat["model"], phrase
    mapped = _mapped_cells(sec_model.Projection.doc)
    missing = [cells for cells in NEW_CELLS if cells not in mapped]
    assert not missing, f"the symbol map does not map {missing}"
    unknown = sorted(mapped - set(sec_model.Projection.cells))
    assert not unknown, f"the symbol map names cells the model lacks: {unknown}"
    stale = sorted(where for where, doc in flat.items()
                   if re.search(r"~\.Term_US_S\.|t = 0`` is the issue month", doc))
    assert not stale, f"docstrings that describe Term_US_S: {stale}"


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


# ---------------------------------------------------------------------------
# C2 -- the Phase 1 fingerprint


def test_the_phase_1_fingerprint_is_reproduced(sec_model):
    """Every committed point computes what the model computed when Phase 1 ended (C2).

    Phase 2 changes how the model is represented and no number it computes (D2), so before
    it changed anything the model as M1 committed it was frozen below
    (USLIB-SEC-PLAN.md §5.4): for each point, each column of ``result_cf()`` and
    ``result_pols()``, its sum, its largest absolute value and its values at five fixed
    months, the frame's first and last and the three quartiles between.  Every later
    version must reproduce it, to 1e-12 relative, floored at 1e-12 of the column's own
    magnitude (``sec_support.fingerprint_mismatches``), with the same points, frames and
    columns exactly.  ``python tools/gen_sec_fingerprint.py Term_US_SEC --check`` runs the
    same comparison from the command line.
    """
    assert fingerprint_mismatches(FINGERPRINT, sec_model) == []


# Term_US_SEC's fingerprint, frozen from the model as M1 committed it and committed alone,
# before Phase 2 changed anything.  Each point is keyed by its point_id; each column holds
# (its sum over the frame, its largest absolute value, (its values at the months)).  The
# block is written by tools/gen_sec_fingerprint.py, and is never edited by hand: a refreeze
# goes through the tool's --force, in a commit of its own that says why.
# BEGIN generated fingerprint: Term_US_SEC -- tools/gen_sec_fingerprint.py
FINGERPRINT = {
    1: {"rows": 720, "months": (0, 179, 359, 539, 719),
        "result_cf": {
            "pols_if": (105.59274191106616, 1.0, (
                1.0, 0.054952074038946065, 0.009515879529071392, 0.001060527490604866,
                1.9988090701711986e-05)),
            "premiums": (2933.563917599938, 140.0, (
                140.0, 0.0, 0.0, 0.0, 0.0)),
            "claims": (1777.4074173656409, 8.683890549777864, (
                6.669112361223917, 3.4515200335473395, 1.5093493485977232,
                0.6274185006943673, 0.047422578259039394)),
            "commissions": (197.7504899909903, 112.0, (
                112.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (598.2770514570509, 302.5, (
                302.5, 0.18459077476354582, 0.04302069437037088, 0.006452871065825871,
                0.0001636835158481863)),
            "premium_taxes": (58.67127835199876, 2.8000000000000003, (
                2.8000000000000003, 0.0, 0.0, 0.0, 0.0)),
            "conv_credits": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (301.45768043425727, 283.96911236122395, (
                -283.96911236122395, -3.6361108083108853, -1.552370042968094,
                -0.6338713717601931, -0.04758626177488758)),
        },
        "result_pols": {
            "pols_if": (105.59274191106616, 1.0, (
                1.0, 0.054952074038946065, 0.009515879529071392, 0.001060527490604866,
                1.9988090701711986e-05)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.01777407417365641, 8.683890549777864e-05, (
                6.669112361223917e-05, 3.4515200335473394e-05, 1.5093493485977232e-05,
                6.2741850069436735e-06, 4.7422578259039396e-07)),
            "pols_conv": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_lapse": (0.9822065825440406, 0.5198181893620692, (
                0.0051426698385184395, 0.00048006793394880006, 8.30521752869031e-05,
                9.215872245240029e-06, 1.7058261534546534e-07)),
            "pols_maturity": (1.9343282303776128e-05, 1.9343282303776128e-05, (
                0.0, 0.0, 0.0, 0.0, 1.9343282303776128e-05)),
        },
    },
    2: {"rows": 720, "months": (0, 179, 359, 539, 719),
        "result_cf": {
            "pols_if": (105.59998511193011, 1.0, (
                1.0, 0.05498092222353764, 0.009528856477903377, 0.0010619737479832247,
                2.0015348763301852e-05)),
            "premiums": (2935.430014774729, 140.0, (
                140.0, 0.0, 0.0, 0.0, 0.0)),
            "claims": (1770.8267607074974, 8.683890549777864, (
                6.669112361223917, 3.3952959396970543, 1.51140767113181, 0.6282741207928435,
                0.04748724914623046)),
            "commissions": (197.78781193448611, 112.0, (
                112.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (598.3055823777179, 302.5, (
                302.5, 0.1846876793633705, 0.04307936234192886, 0.006461670943691577,
                0.00016390673353429845)),
            "premium_taxes": (58.70860029549458, 2.8000000000000003, (
                2.8000000000000003, 0.0, 0.0, 0.0, 0.0)),
            "conv_credits": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (309.80125945953284, 283.96911236122395, (
                -283.96911236122395, -3.5799836190604246, -1.5544870334737388,
                -0.634735791736535, -0.04765115587976476)),
        },
        "result_pols": {
            "pols_if": (105.59998511193011, 1.0, (
                1.0, 0.05498092222353764, 0.009528856477903377, 0.0010619737479832247,
                2.0015348763301852e-05)),
            "pols_new_biz": (1.0, 1.0, (
                1.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.017708267607074973, 8.683890549777864e-05, (
                6.669112361223917e-05, 3.395295939697054e-05, 1.51140767113181e-05,
                6.282741207928435e-06, 4.748724914623046e-07)),
            "pols_conv": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_lapse": (0.9822723627318951, 0.5198181893620692, (
                0.0051426698385184395, 0.00048032502844679617, 8.31654347944232e-05,
                9.228440069601742e-06, 1.7081524143790395e-07)),
            "pols_maturity": (1.9369661030401644e-05, 1.9369661030401644e-05, (
                0.0, 0.0, 0.0, 0.0, 1.9369661030401644e-05)),
        },
    },
    3: {"rows": 708, "months": (0, 176, 353, 530, 707),
        "result_cf": {
            "pols_if": (93.93790209606017, 0.939248, (
                0.939248, 0.05051368421473739, 0.00894771579513133, 0.001014988594739213,
                2.0015348763301852e-05)),
            "premiums": (2795.430014774729, 131.49472, (
                131.49472, 0.0, 0.0, 0.0, 0.0)),
            "claims": (1693.0510187087393, 8.683890549777864, (
                6.65559997559641, 3.2216594091379847, 1.5481856181263005,
                0.6564953448394129, 0.04748724914623046)),
            "commissions": (85.78781193448613, 6.574736000000001, (
                6.574736000000001, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (263.61479994630275, 2.3481199999999998, (
                2.3481199999999998, 0.16884371768849551, 0.04005350957296639,
                0.0060847409066405725, 0.00016069287601401807)),
            "premium_taxes": (55.90860029549458, 2.6298944, (
                2.6298944, 0.0, 0.0, 0.0, 0.0)),
            "conv_credits": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (697.0677838897054, 113.28636962440359, (
                113.28636962440359, -3.3905031268264803, -1.588239127699267,
                -0.6625800857460534, -0.047647942022244476)),
        },
        "result_pols": {
            "pols_if": (93.93790209606017, 0.939248, (
                0.939248, 0.05051368421473739, 0.00894771579513133, 0.001014988594739213,
                2.0015348763301852e-05)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.016930510187087397, 8.683890549777864e-05, (
                6.65559997559641e-05, 3.221659409137985e-05, 1.5481856181263006e-05,
                6.564953448394129e-06, 4.748724914623046e-07)),
            "pols_conv": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_lapse": (0.9222981201518827, 0.5198181893620692, (
                0.0040059082486307625, 0.000441289350361807, 7.808211405063976e-05,
                8.81524714968298e-06, 1.7081524143790395e-07)),
            "pols_maturity": (1.9369661030401644e-05, 1.9369661030401644e-05, (
                0.0, 0.0, 0.0, 0.0, 1.9369661030401644e-05)),
        },
    },
    4: {"rows": 594, "months": (0, 148, 296, 444, 593),
        "result_cf": {
            "pols_if": (9.443086927428597, 0.10838474140322372, (
                0.10838474140322372, 0.022280560582628582, 0.00479811532002715,
                0.0006511542334572065, 1.9988090701711986e-05)),
            "premiums": (1698.3049221320648, 75.02791937521008, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims": (876.632544940142, 5.706695810923936, (
                5.706695810923936, 1.9255703644708833, 1.2840075283835228,
                0.5038665726999406, 0.047422578259039394)),
            "commissions": (33.9660984426413, 1.5005583875042015, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (27.907390849740615, 0.2709618535080593, (
                0.2709618535080593, 0.07111069239013718, 0.019550067471678468,
                0.0033871172630724564, 0.00013295453070536796)),
            "premium_taxes": (33.9660984426413, 1.5005583875042015, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "conv_credits": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (725.8327894568995, 66.7359420231921, (
                -5.977657664431995, -1.9966810568610205, -1.3035575958552013,
                -0.5072536899630131, -0.04755553278974476)),
        },
        "result_pols": {
            "pols_if": (9.443086927428597, 0.10838474140322372, (
                0.10838474140322372, 0.022280560582628582, 0.00479811532002715,
                0.0006511542334572065, 1.9988090701711986e-05)),
            "pols_new_biz": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.008766325449401419, 5.706695810923936e-05, (
                5.706695810923936e-05, 1.9255703644708832e-05, 1.2840075283835229e-05,
                5.038665726999407e-06, 4.7422578259039396e-07)),
            "pols_conv": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_lapse": (0.09959907267151849, 0.0031724334006080763, (
                0.0031724334006080763, 0.00019459966659596901, 4.18310145006872e-05,
                5.648090924870469e-06, 1.7058261534546534e-07)),
            "pols_maturity": (1.9343282303776128e-05, 1.9343282303776128e-05, (
                0.0, 0.0, 0.0, 0.0, 1.9343282303776128e-05)),
        },
    },
    5: {"rows": 1, "months": (0,),
        "result_cf": {
            "pols_if": (1.9988090701711986e-05, 1.9988090701711986e-05, (
                1.9988090701711986e-05,)),
            "premiums": (0.0, 0.0, (
                0.0,)),
            "claims": (0.047422578259039394, 0.047422578259039394, (
                0.047422578259039394,)),
            "commissions": (0.0, 0.0, (
                0.0,)),
            "expenses": (4.997022675427996e-05, 4.997022675427996e-05, (
                4.997022675427996e-05,)),
            "premium_taxes": (0.0, 0.0, (
                0.0,)),
            "conv_credits": (0.0, 0.0, (
                0.0,)),
            "net_cf": (-0.04747254848579367, 0.04747254848579367, (
                -0.04747254848579367,)),
        },
        "result_pols": {
            "pols_if": (1.9988090701711986e-05, 1.9988090701711986e-05, (
                1.9988090701711986e-05,)),
            "pols_new_biz": (0.0, 0.0, (
                0.0,)),
            "pols_death": (4.7422578259039396e-07, 4.7422578259039396e-07, (
                4.7422578259039396e-07,)),
            "pols_conv": (0.0, 0.0, (
                0.0,)),
            "pols_lapse": (1.7058261534546534e-07, 1.7058261534546534e-07, (
                1.7058261534546534e-07,)),
            "pols_maturity": (1.9343282303776128e-05, 1.9343282303776128e-05, (
                1.9343282303776128e-05,)),
        },
    },
    6: {"rows": 723, "months": (0, 180, 361, 541, 722),
        "result_cf": {
            "pols_if": (105.59274191106614, 1.0, (
                0.0, 0.05599587894051132, 0.00961504800996041, 0.0010762471490809084,
                1.9988090701711986e-05)),
            "premiums": (2933.563917599938, 140.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "claims": (1777.4074173656406, 8.683890549777864, (
                0.0, 3.5170810445168987, 1.5250788333578011, 0.6367184053548686,
                0.047422578259039394)),
            "commissions": (197.7504899909903, 112.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "expenses": (599.7573800532894, 302.512407328933, (
                0.0, 0.18840770135666277, 0.04361273269301639, 0.006570167369371906,
                0.00016449586593700227)),
            "premium_taxes": (58.67127835199876, 2.8000000000000003, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "conv_credits": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "net_cf": (299.97735183801893, 283.981519690157, (
                0.0, -3.7054887458735615, -1.5686915660508176, -0.6432885727242404,
                -0.0475870741249764)),
        },
        "result_pols": {
            "pols_if": (105.59274191106614, 1.0, (
                0.0, 0.05599587894051132, 0.00961504800996041, 0.0010762471490809084,
                1.9988090701711986e-05)),
            "pols_new_biz": (1.0, 1.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_death": (0.01777407417365641, 8.683890549777864e-05, (
                0.0, 3.5170810445168987e-05, 1.525078833357801e-05, 6.367184053548686e-06,
                4.7422578259039396e-07)),
            "pols_conv": (0.0, 0.0, (
                0.0, 0.0, 0.0, 0.0, 0.0)),
            "pols_lapse": (0.9822065825440406, 0.5198181893620692, (
                0.0, 0.0004891867392223722, 8.391769255544026e-05, 9.352474422493713e-06,
                1.7058261534546534e-07)),
            "pols_maturity": (1.9343282303776128e-05, 1.9343282303776128e-05, (
                0.0, 0.0, 0.0, 0.0, 1.9343282303776128e-05)),
        },
    },
}
# END generated fingerprint: Term_US_SEC
