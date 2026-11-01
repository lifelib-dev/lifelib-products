"""Tests of the SEC harness and row generator in :mod:`sec_support`, on ``Term_US_S``.

Phase 0 of USLIB-SEC-PLAN.md builds the SEC test machinery before any SEC model exists, so
it is tested here on what does exist.  ``Term_US_S`` is compared with a second read of
itself, where the twin identity must hold exactly and must break where a Reference is
changed.  Small synthetic models stand in where a difference of a given kind must be seen.
And a synthetic :class:`SecSpec`, never registered except under ``monkeypatch`` for the
regeneration round trip, generates a table from Term's two points.

What each test pins, against the plan (its §4 item 3 and §5.2):

* T1's comparison, :func:`twin_mismatches`: silent on a true twin, but only after it has
  compared every value the S sweep cached, a tuple argument included; loud, and specific,
  on a changed one; bounded by ``limit``; an SEC error or an uncomparable value reported
  rather than raised or passed; and an offset, or an argument map, turning S's call into
  SEC's.
* T2 and T3's harness: :func:`temp_inputs` copies a product so an added point projects
  exactly as its source, and writes floats the models' reader reads back exactly;
  :func:`shift_months` re-bases a table under both readings; :func:`frame_mismatches`
  compares on an offset and refuses to pass a comparison that compares nothing, or less
  than the whole splice.
* T6's generator: :func:`build_sec_table` writes twins, a derived row and a future row
  with the right counts, durations, sources and ids, and no text that is not S's own or
  composed from S's keys and a month (``CLAUDE.md``); :func:`write_generated` is a no-op on
  a rerun; and :func:`check_generated` reports an edited S row cell by cell, but reads a
  float by its value, so a file written on another platform checks clean.

modelx keeps every model in one registry, and ``conftest.term_life`` already holds the
default name, so every model here is read under a name of its own and closed.
"""
import dataclasses
import io
import itertools
import math
import re

import modelx as mx
import numpy as np
import pandas as pd
import pytest

from sec_support import (
    SEC_SPECS, TWIN_EXEMPT_DEFAULT, SecSpec, build_sec_table, check_generated,
    frame_mismatches, shift_months, sweep, temp_inputs, twin_mismatches, write_generated)
from us_registry import model_path

TERM = "Term_US_S"

_names = itertools.count(1)


def _name(tag):
    """A model name no other read in this process uses."""
    return f"{TERM}_secsup_{tag}_{next(_names)}"


def _read(tag, path=None):
    return mx.read_model(path or model_path(TERM), name=_name(tag))


@pytest.fixture(scope="module")
def s_model():
    """Term_US_S with point 1 swept, the S side of every comparison here."""
    model = _read("s")
    sweep(model.Projection[1])
    yield model
    model.close()


@pytest.fixture
def other():
    """A second, cold read of Term_US_S, free to be changed by the test that holds it."""
    model = _read("other")
    yield model
    model.close()


# The synthetic spec: Term's two points as twins, point 1 restated in force at month 12,
# and point 1 written 3 months after the valuation date.  ``duration_inforce`` is a count of
# years that SEC's ``duration_mth`` replaces (D6), so it is dropped.
SPEC = SecSpec(twin=TERM, column_map={"duration_inforce": None},
               derived=((1, 12),), future=((1, 3),))


# ---------------------------------------------------------------------------
# T1 -- twin_mismatches


def test_a_second_read_of_the_same_model_is_its_twin(s_model, other):
    """The identity holds between two reads of one model, and is not vacuous.

    An empty list could also mean nothing was compared, so the test also asserts that
    the S sweep cached thousands of values and that every one of them was evaluated on the
    other side.
    """
    s_proj, o_proj = s_model.Projection[1], other.Projection[1]
    assert twin_mismatches(s_proj, o_proj) == []
    compared = {name: set(s_proj.cells[name].keys()) for name in s_proj.cells
                if name not in TWIN_EXEMPT_DEFAULT}
    assert sum(len(keys) for keys in compared.values()) > 10_000
    for name, keys in compared.items():
        assert keys <= set(o_proj.cells[name].keys()), f"{name} was not compared"


def _cells_named(lines):
    return {line.split("(", 1)[0] for line in lines}


def test_a_changed_reference_is_found_in_the_cells_it_moves(s_model, other):
    """A higher maintenance expense shows in ``expenses`` and what sums it, and only there.

    ``premiums``, ``claims`` and ``pols_if`` read no expense, so no line may name them.
    """
    other.Projection.expense_maint = 31.0
    lines = twin_mismatches(s_model.Projection[1], other.Projection[1], limit=10_000)
    assert _cells_named(lines) == {"expenses", "net_cf", "result_cf", "result_cf_annual"}
    assert any(line.startswith("expenses(0): S 302.5, SEC 302.58") for line in lines)
    frame_lines = [line for line in lines if line.startswith("result_cf()")]
    assert {re.search(r"column '(\w+)'", line).group(1) for line in frame_lines} == {
        "expenses", "net_cf"}
    assert all("720 of 720 differ" in line for line in frame_lines)


def test_the_limit_stops_the_scan_and_says_so(s_model, other):
    """At most ``limit`` lines, the last one saying that more were found."""
    other.Projection.expense_maint = 31.0
    lines = twin_mismatches(s_model.Projection[1], other.Projection[1], limit=5)
    assert len(lines) == 5
    assert all(line.startswith("expenses(") for line in lines[:4])
    assert "more than 4 mismatches" in lines[-1]
    assert len(twin_mismatches(s_model.Projection[1], other.Projection[1], limit=1)) == 1
    with pytest.raises(ValueError):
        twin_mismatches(s_model.Projection[1], other.Projection[1], limit=0)


def _premium_taxes_failing_at_issue(t):
    if t == 0:
        raise ValueError("no premium tax at issue")
    return premium_tax_rate * premiums(t)                           # noqa: F821


def test_an_error_in_the_sec_model_is_reported_not_raised(s_model, other):
    """One broken cells is a line, and the comparison goes on past it."""
    other.Projection.premium_taxes.formula = _premium_taxes_failing_at_issue
    lines = twin_mismatches(s_model.Projection[1], other.Projection[1], limit=10_000)
    assert "premium_taxes(0): SEC raised ValueError: no premium tax at issue" in lines
    assert "net_cf(0): SEC raised ValueError: no premium tax at issue" in lines
    later = ("premium_taxes(1)", "net_cf(1)")
    assert not [line for line in lines if line.startswith(later)]


# Two synthetic Spaces whose cells return every kind of value the comparison knows, and one
# it does not.  Where S and SEC differ, they differ on purpose.
S_KINDS = {
    "phase": lambda: "LEVEL",
    "flag": lambda: True,
    "legs": lambda: ("call", "put"),
    "ids": lambda: [1, 2],
    "by_mth": lambda: {"a": 1.0, "b": 2.0},
    "blank": lambda: float("nan"),
    "cap": lambda: float("inf"),
    "opaque": lambda: object(),
    "rate": lambda t: 0.01 * t,
    "scalar_array": lambda: np.array(5.0),
    "grid": lambda: np.ones((2, 2)),
}
SEC_KINDS = {
    "phase": lambda: 1,
    "flag": lambda: 1.0,
    "legs": lambda: ("call", "put"),
    "ids": lambda: [1, 2, 3],
    "by_mth": lambda: {"a": 1.0 + 1e-12, "c": 3.0},
    "blank": lambda: float("nan"),
    "cap": lambda: 1e308,
    "opaque": lambda: object(),
    "rate": lambda t: 0.01 * t,
    "scalar_array": lambda: np.array(5.0),
    "grid": lambda: np.array([[1.0, 1.0], [1.0, 2.0]]),
}


def _space(model, formulas):
    space = model.new_space("P")
    space.pd = pd
    space.np = np
    for name, formula in formulas.items():
        space.new_cells(name, formula=formula)
    return space


def test_values_compare_by_kind():
    """Each kind of value is compared as that kind, and an unknown kind is never passed."""
    s, sec = mx.new_model(_name("kinds_s")), mx.new_model(_name("kinds_sec"))
    try:
        s_space, sec_space = _space(s, S_KINDS), _space(sec, SEC_KINDS)
        for name in S_KINDS:
            s_space.cells[name](*([5] if name == "rate" else []))
        lines = twin_mismatches(s_space, sec_space, exempt=frozenset(), limit=100)
    finally:
        s.close()
        sec.close()
    assert sorted(lines) == sorted([
        "phase(): S 'LEVEL' (str), SEC 1 (int)",
        "flag(): S True (bool), SEC 1.0 (float)",
        "ids(): length: S 2, SEC 3",
        "by_mth(): keys only in S: 'b'",
        "by_mth(): keys only in SEC: 'c'",
        "cap(): S inf, SEC 1e+308, diff -inf",
        "opaque(): uncomparable: S object, SEC object",
        "grid(): [1] [1] S 1.0, SEC 2.0, diff +1",
    ])


def test_a_cells_cached_at_a_tuple_argument_is_compared():
    """A one-parameter cells called with a tuple is compared at that tuple.

    modelx caches ``f(("call", "put"))`` under the bare tuple, which ``Cells.items()`` looks
    up again as two arguments, raising ``TypeError`` before anything is compared.
    """
    s, sec = mx.new_model(_name("tuple_s")), mx.new_model(_name("tuple_sec"))
    try:
        s_space = _space(s, {"leg_value": lambda legs: float(len(legs))})
        sec_space = _space(sec, {"leg_value": lambda legs: (
            2.0 if legs[0] == "call" else 0.0)})
        s_space.leg_value(("call", "put"))
        s_space.leg_value(("put", "call"))
        lines = twin_mismatches(s_space, sec_space)
    finally:
        s.close()
        sec.close()
    assert lines == ["leg_value(('put', 'call')): S 2.0, SEC 0.0, diff -2"]


def test_an_offset_reads_s_t_as_sec_t_plus_offset():
    """``t_offset`` maps S's ``t`` to SEC's in one sense, for cells and frames alike.

    The SEC cells here is the S one restarted three months on: SEC month ``t`` is S month
    ``t + 3``, so both comparisons take ``3``, the ``source_mth`` of a row derived from S
    month 3.  :func:`twin_mismatches` calls the SEC cells at S's ``t - 3`` and skips the S
    months before 3, which have no SEC month; :func:`frame_mismatches` reads SEC row ``t``
    against S row ``t + 3``.  The wrong sign fails both.
    """
    frame = ("lambda: pd.DataFrame({'x': [rate(t) for t in range(10)]}, "
             "index=pd.Index(range(10), name='t'))")
    s, sec = mx.new_model(_name("off_s")), mx.new_model(_name("off_sec"))
    try:
        s_space = _space(s, {"rate": lambda t: 0.01 * t, "result_x": frame})
        sec_space = _space(sec, {"rate": lambda t: 0.01 * (t + 3), "result_x": (
            "lambda: pd.DataFrame({'x': [rate(t) for t in range(7)]}, "
            "index=pd.Index(range(7), name='t'))")})
        s_df, sec_df = s_space.result_x(), sec_space.result_x()
        assert twin_mismatches(s_space, sec_space, t_offset=3) == []
        assert sorted(sec_space.cells["rate"].keys()) == list(range(7))
        assert frame_mismatches(s_df, sec_df, t_offset=3) == []
        unshifted = twin_mismatches(s_space, sec_space)
        twin_wrong = twin_mismatches(s_space, sec_space, t_offset=-3)
    finally:
        s.close()
        sec.close()
    assert unshifted[0] == "rate(0): S 0.0, SEC 0.03, diff +0.03"
    assert "result_x(): 3 labels only in S: t=7, t=8, t=9" in unshifted
    assert twin_wrong[0] == "rate(0) [SEC rate(3)]: S 0.0, SEC 0.06, diff +0.06"
    shifted_wrong = frame_mismatches(s_df, sec_df, t_offset=-3)
    assert len(shifted_wrong) == 2
    assert shifted_wrong[0] == "the frames end apart: S ends at t=12 (S t=9), SEC at t=6"
    assert shifted_wrong[1].startswith(
        "column 'x': 4 of 4 differ, first at t=3 (S t=0): S 0.0, SEC 0.06; largest")


def test_arg_map_turns_s_arguments_into_sec_ones():
    """Phase 2's mapping: S's timing strings become the int codes the SEC cells take (R9).

    The label shows both calls when they differ, so a wrong code is read off the line, and
    ``None`` from the map skips a key the SEC model has no counterpart for.
    """
    codes = {"BEF_DECR": 2, "AFT_DECR": 3}

    def to_codes(name, args):
        return (args[0], codes[args[1]]) if name == "pols_at" else args

    def bef_decr_only(name, args):
        return to_codes(name, args) if args[1] == "BEF_DECR" else None

    s, sec = mx.new_model(_name("map_s")), mx.new_model(_name("map_sec"))
    try:
        s_space = _space(s, {"pols_at": lambda t, timing: (
            1.0 * t if timing == "BEF_DECR" else 2.0 * t)})
        sec_space = _space(sec, {"pols_at": lambda t, timing: (
            1.0 * t if timing == 2 else 2.0 * t)})
        for args in ((1, "BEF_DECR"), (1, "AFT_DECR"), (2, "BEF_DECR")):
            s_space.pols_at(*args)
        assert twin_mismatches(s_space, sec_space, arg_map=to_codes) == []
        assert twin_mismatches(s_space, sec_space) == [
            "pols_at(1, 'BEF_DECR'): S 1.0, SEC 2.0, diff +1",
            "pols_at(2, 'BEF_DECR'): S 2.0, SEC 4.0, diff +2"]
        codes["BEF_DECR"] = 3
        assert twin_mismatches(s_space, sec_space, arg_map=bef_decr_only) == [
            "pols_at(1, 'BEF_DECR') [SEC pols_at(1, 3)]: S 1.0, SEC 2.0, diff +1",
            "pols_at(2, 'BEF_DECR') [SEC pols_at(2, 3)]: S 2.0, SEC 4.0, diff +2"]
    finally:
        s.close()
        sec.close()


def test_frame_mismatches_will_not_pass_a_comparison_of_nothing():
    """An empty overlap, a missing named column or a gap is a line, never a silent pass."""
    df = pd.DataFrame({"pols_if": [1.0, 0.9, 0.8, 0.7], "net_cf": [-5.0, 1.0, 1.0, 1.0]},
                      index=pd.Index(range(4), name="t"))
    assert frame_mismatches(df, df.copy()) == []
    assert frame_mismatches(df, df, t_offset=10) == [
        "no shared rows: S rows 0..3 are SEC t = -10..-7, and SEC has t = 0..3"]
    assert frame_mismatches(df, df, columns=["net_cf", "claims"]) == [
        "columns missing from S: ['claims']", "columns missing from SEC: ['claims']"]
    renamed = df.rename(columns={"pols_if": "lives", "net_cf": "cash"})
    assert frame_mismatches(df, renamed) == ["no column to compare"]
    gapped = df.drop(index=2)
    assert frame_mismatches(df, gapped) == ["1 rows inside the shared range only in S: t=2"]
    moved = df.copy()
    moved.loc[1, "net_cf"] = 1.0 + 1e-6
    assert frame_mismatches(df, moved) == [
        "column 'net_cf': 1 of 4 differ, first at t=1: S 1.0, SEC 1.000001"]
    assert frame_mismatches(df, moved, atol=1e-5) == []


def test_frame_mismatches_reports_a_frame_that_ends_too_soon_or_too_late():
    """The splice must run to the end of cover, which is one instant on both clocks.

    A row derived from S month 120 of a 720-month frame is SEC ``t = 0 .. 599``.  An SEC
    frame cut short by a wrong ``proj_len()``, or run on past the end, agrees with S on
    every row the two share, and must still fail.
    """
    s = pd.DataFrame({"net_cf": np.arange(720.0)}, index=pd.Index(range(720), name="t"))
    good = s.loc[120:].set_axis(pd.Index(range(600), name="t"))
    assert frame_mismatches(s, good, t_offset=120) == []
    assert frame_mismatches(s, good.loc[:479], t_offset=120) == [
        "the frames end apart: S ends at t=599 (S t=719), SEC at t=479"]
    late = pd.concat([good, pd.DataFrame({"net_cf": [0.0] * 30},
                                         index=pd.Index(range(600, 630), name="t"))])
    assert frame_mismatches(s, late, t_offset=120) == [
        "the frames end apart: S ends at t=599 (S t=719), SEC at t=629"]
    # A future point issued 3 months on: SEC t = 3 .. 722 is S t = 0 .. 719, and the
    # pre-issue rows 0 .. 2 are not compared.
    future = pd.concat([pd.DataFrame({"net_cf": [0.0] * 3},
                                     index=pd.Index(range(3), name="t")),
                        s.set_axis(pd.Index(range(3, 723), name="t"))])
    assert frame_mismatches(s, future, t_offset=-3) == []
    assert frame_mismatches(s, future.loc[:700], t_offset=-3) == [
        "the frames end apart: S ends at t=722 (S t=719), SEC at t=700"]


# ---------------------------------------------------------------------------
# T2 and T3 -- temp_inputs and shift_months


def test_temp_inputs_projects_an_added_point_exactly_like_its_source(s_model, tmp_path):
    """Point 99, a copy of point 1 in a copied product, projects exactly as point 1 does."""
    table = s_model.Data.model_point_table()
    points = pd.concat([table, table.loc[[1]].rename(index={1: 99})])
    folder = temp_inputs(tmp_path, model_path(TERM), model_points=points)
    assert folder == tmp_path / TERM
    assert not list(folder.rglob("__pycache__"))
    source = model_path(TERM).parent
    for csv_path in source.glob("*.csv"):
        if csv_path.name != "model_point_table.csv":
            assert (tmp_path / csv_path.name).read_bytes() == csv_path.read_bytes()
    model = _read("tmp", folder)
    try:
        assert model.Data.input_dir() == tmp_path
        pd.testing.assert_frame_equal(model.Data.model_point_table(), points)
        one, copy = model.Projection[1], model.Projection[99]
        assert frame_mismatches(one.result_cf(), copy.result_cf(), rtol=0, atol=0) == []
        assert frame_mismatches(s_model.Projection[1].result_cf(), copy.result_cf(),
                                rtol=0, atol=0) == []
        sweep(one)
        assert twin_mismatches(one, copy, rtol=0, atol=0) == []
    finally:
        model.close()


# Floats plain ``repr`` writes and pandas' default parser reads back wrong, by 1 to 1,685
# ulps, but for which a 17-digit text exists that it reads exactly.  Measured on pandas
# 3.0.5; the last two lose digits to leading zeros, which pandas counts among its 17.
HARD_FLOATS = [0.17893481367543618, 0.9051438366771739, 0.29830276735556926,
               0.9669622001623905, 0.9955002834343927, 0.00012345678901234567,
               0.0012345678901234567]
# Floats no decimal text near them makes the default parser produce: read to within an ulp.
UNREACHABLE_FLOATS = [0.22733602246716966, 0.22520718999059186]


def test_temp_inputs_writes_floats_the_models_read_back_exactly(tmp_path):
    """Written values come back from ``pd.read_csv`` as the models call it, exactly.

    The control half shows the test has teeth: written as plain ``repr``, every one of
    the hard floats comes back wrong.  It applies where the installed pandas has the
    defect, as 3.0.5 does; a pandas whose parser rounds correctly reads every text right,
    and the exactness asserted below then holds with no workaround to test.
    """
    values = HARD_FLOATS + UNREACHABLE_FLOATS + [53730.123456789123, 0.0445, 100000.0]
    plain = pd.read_csv(io.StringIO("v\n" + "\n".join(map(repr, HARD_FLOATS)) + "\n"))
    if plain["v"].tolist() != HARD_FLOATS:
        assert all(a != b for a, b in zip(plain["v"], HARD_FLOATS))

    frame = pd.DataFrame({"point_id": range(1, len(values) + 1), "value": values,
                          "label": "x", "flag": True, "count": 3})
    frame.loc[0, "label"] = None
    temp_inputs(tmp_path, model_path(TERM), model_points=frame,
                model_point_file="floats_sec.csv")
    back = pd.read_csv(tmp_path / "floats_sec.csv", index_col="point_id")
    assert back["value"].tolist()[:len(HARD_FLOATS)] == HARD_FLOATS
    reached = back["value"].tolist()[len(HARD_FLOATS):len(HARD_FLOATS) + 2]
    for got, want in zip(reached, UNREACHABLE_FLOATS):
        assert abs(got - want) <= np.spacing(want)
    assert back["value"].tolist()[-3:] == [53730.123456789123, 0.0445, 100000.0]
    texts = pd.read_csv(tmp_path / "floats_sec.csv", dtype=str)["value"]
    assert [float(t) for t in texts] == values, "a text a correct parser misreads"
    assert pd.isna(back["label"].iloc[0]) and (back["label"].iloc[1:] == "x").all()
    assert back["flag"].tolist() == [True] * len(values)
    assert back["count"].dtype == np.int64


def test_temp_inputs_edits_by_value_or_by_function_and_refuses_a_missing_file(tmp_path):
    """An edit replaces a file or transforms it; one naming a file the copy lacks raises."""
    def double(df):
        return df.assign(factor=df["factor"] * 2)

    temp_inputs(tmp_path, model_path(TERM), edits={"class_factor_table.csv": double})
    edited = pd.read_csv(tmp_path / "class_factor_table.csv")
    shipped = pd.read_csv(model_path(TERM).parent / "class_factor_table.csv")
    assert edited["factor"].tolist() == (shipped["factor"] * 2).tolist()
    assert list(edited.columns) == list(shipped.columns)
    with pytest.raises(FileNotFoundError, match="class_factors.csv"):
        temp_inputs(tmp_path, model_path(TERM), edits={"class_factors.csv": shipped})


def _table(rows, columns=("month", "rate")):
    return pd.DataFrame(rows, columns=list(columns))


def test_shift_months_reads_a_step_table_and_an_exact_one():
    """Step: the row in force at ``d`` becomes month 0.  Exact: earlier rows are dropped."""
    table = _table([(0, 0.01), (12, 0.02), (24, 0.03)])
    step = shift_months(table, "month", 18)
    assert step.values.tolist() == [[0, 0.02], [6, 0.03]]
    exact = shift_months(table, "month", 18, step=False)
    assert exact.values.tolist() == [[6, 0.03]]
    at_a_row = shift_months(table, "month", 12)
    assert at_a_row.values.tolist() == [[0, 0.02], [12, 0.03]]
    assert shift_months(table, "month", 0).equals(table)
    assert list(step.index) == [1, 2], "rows keep their labels"
    assert step["month"].dtype == table["month"].dtype


def test_shift_months_re_bases_each_group_and_every_row_in_force():
    """Each ``by`` group keeps its own row in force; rows sharing that month all survive."""
    table = _table([("A", 0, 0.01), ("A", 12, 0.02), ("A", 24, 0.03),
                    ("B", 0, 0.05), ("B", 6, 0.06)], columns=("scenario_id", "month", "r"))
    shifted = shift_months(table, "month", 12, by="scenario_id")
    assert shifted.values.tolist() == [["A", 0, 0.02], ["A", 12, 0.03], ["B", 0, 0.06]]
    ungrouped = shift_months(table, "month", 12)
    assert ungrouped.values.tolist() == [["A", 0, 0.02], ["A", 12, 0.03]]
    two_keys = shift_months(table.drop(index=[1, 2]), "month", 3)
    assert two_keys.values.tolist() == [["A", 0, 0.01], ["B", 0, 0.05], ["B", 3, 0.06]]


def test_shift_months_moves_a_future_point_later_and_refuses_a_blank_month():
    """``d = -k`` moves every row ``k`` months on and invents nothing before it."""
    table = _table([(0, 0.01), (12, 0.02)])
    assert shift_months(table, "month", -3).values.tolist() == [[3, 0.01], [15, 0.02]]
    with pytest.raises(ValueError, match="blank month"):
        shift_months(_table([(0, 0.01), (None, 0.02)]), "month", 1)


# ---------------------------------------------------------------------------
# T6 -- build_sec_table, write_generated, check_generated


# The words the generator composes ids and provenance from, beside S's keys and a month:
# ``TL-000001-M12``, ``TL-000001-F3``, "S point 1 (TL-000001) restated in force at S month
# 12", "... issued 3 months after the valuation date".  A word outside this set in a
# generated text cell is one the generator added, which ``CLAUDE.md`` forbids.
TEMPLATE_WORDS = {"M", "F", "S", "point", "restated", "in", "force", "at", "month",
                  "months", "issued", "after", "the", "valuation", "date"}
ROW_KINDS = {"twin", "derived", "future"}


def _foreign_text(table, s_table, rename):
    """Every text cell that is neither copied from its S row nor composed from S's keys.

    A cell passes if it equals its source S row's value in the same column, renamed back;
    or, with that row's ``policy_id``, ``point_id`` and the row's month taken out, if
    what is left is template words and punctuation only.
    """
    s_rows = {r["policy_id"]: r for r in s_table.reset_index().to_dict("records")}
    s_column = {new: old for old, new in rename.items() if new is not None}
    foreign = []
    for record in table.to_dict("records"):
        source = s_rows[record["source_policy_id"]]
        for column, value in record.items():
            if not isinstance(value, str):
                continue
            if column == "row_kind" and value in ROW_KINDS:
                continue
            if source.get(s_column.get(column, column)) == value:
                continue
            rest = value
            keys = (source["policy_id"], str(abs(record["source_mth"])),
                    str(source["point_id"]))
            for key in sorted(keys, key=len, reverse=True):
                rest = rest.replace(key, " ")
            words = set(re.findall(r"[A-Za-z]+", rest))
            if not words <= TEMPLATE_WORDS or re.search(r"\d", rest):
                foreign.append((record["point_id"], column, value))
    return foreign


SEC_COLUMNS = ["point_id", "policy_id", "age_at_entry", "sex", "rate_class", "plan",
               "sum_assured", "premium_mode", "policy_count", "plt_mort_factor_override",
               "duration_mth", "row_kind", "source_policy_id", "source_mth"]


def test_build_sec_table_writes_twins_a_derived_and_a_future_row(s_model):
    """The table of D8 from Term's two points: every column and every generated cell."""
    table, companions = build_sec_table(SPEC, s_model)
    s_table = s_model.Data.model_point_table()
    assert companions == {}
    assert list(table.columns) == SEC_COLUMNS
    assert table["row_kind"].tolist() == ["twin", "twin", "derived", "future"]
    assert table["point_id"].tolist() == [1, 2, 3, 4]
    assert table["policy_id"].tolist() == [
        "TL-000001", "TL-000002", "TL-000001-M12", "TL-000001-F3"]
    assert table["point_id"].is_unique and table["policy_id"].is_unique
    assert table["duration_mth"].tolist() == [0, 0, 12, -3]
    assert table["source_mth"].tolist() == [0, 0, 12, -3]
    assert table["source_policy_id"].tolist() == [
        "TL-000001", "TL-000002", "TL-000001", "TL-000001"]
    assert table["policy_count"].tolist() == [
        1.0, 1.0, s_model.Projection[1].pols_if(12), 1.0]
    assert s_model.Projection[1].pols_if(12) < 1.0
    # Every column S has is S's value for the source row, renamed where it was renamed.
    for record in table.to_dict("records"):
        source = s_table.loc[1 if record["source_policy_id"] == "TL-000001" else 2]
        for column in ("age_at_entry", "sex", "rate_class", "plan", "sum_assured",
                       "premium_mode", "plt_mort_factor_override"):
            assert record[column] == source[column] or (
                pd.isna(record[column]) and pd.isna(source[column]))
    assert _foreign_text(table, s_table, {"pols_if_init": "policy_count"}) == []


def test_generated_text_is_s_text_or_composed_from_s_keys(tmp_path):
    """With a ``provenance`` column in S: twins copy it, the generated rows cite S by key.

    Term's table has no ``provenance`` column, so one is added in a copy.  The words it
    holds cite sources by key, as ``CLAUDE.md`` requires of any provenance cell.
    """
    provenance = ["worked example anchor cell [S5]", "[std] variant without the override"]
    folder = temp_inputs(tmp_path, model_path(TERM), edits={
        "model_point_table.csv": lambda df: df.assign(provenance=provenance)})
    model = _read("prov", folder)
    try:
        table, _ = build_sec_table(SPEC, model)
        s_table = model.Data.model_point_table()
    finally:
        model.close()
    assert list(table.columns) == SEC_COLUMNS + ["provenance"]
    assert table["provenance"].tolist() == provenance + [
        "S point 1 (TL-000001) restated in force at S month 12",
        "S point 1 (TL-000001) issued 3 months after the valuation date"]
    assert _foreign_text(table, s_table, {"pols_if_init": "policy_count"}) == []
    planted = table.copy()
    planted.loc[2, "provenance"] = "S point 1 restated by Example Mutual at S month 12"
    assert _foreign_text(planted, s_table, {"pols_if_init": "policy_count"}) == [
        (3, "provenance", "S point 1 restated by Example Mutual at S month 12")]


@pytest.mark.parametrize("change, error", [
    ({"model_point_file": "model_point_table.csv"}, "never overwrite"),
    ({"companions": {"premium_rates.csv": lambda m, t: t}}, "never overwrite"),
    ({"state": {"policy_id": lambda s, d: "x"}}, "the generator owns them"),
    ({"twin_state": {"policy_count": lambda s, d: 2.0}}, "the generator owns them"),
    ({"state": {"provenance": lambda s, d: "x"}}, "the generator owns them"),
    ({"companions": {"model_point_table_sec.csv": lambda m, t: t}}, "would replace"),
])
def test_a_spec_that_could_clobber_s_or_the_generator_is_refused(change, error):
    with pytest.raises(ValueError, match=error):
        dataclasses.replace(SPEC, **change)


@pytest.mark.parametrize("change, error", [
    ({"derived": ((1, 0),)}, "after the twin's entry month"),
    ({"derived": ((1, 720),)}, "inside S's frame"),
    ({"derived": ((7, 12),)}, "point 7"),
    ({"derived": ((1, 12), (1, 12))}, "repeats policy_id"),
    ({"future": ((1, 0),)}, "at least 1"),
    ({"column_map": {"no_such_column": None}}, "no_such_column"),
    ({"column_map": {"sex": "plan"}}, "two columns one name"),
    ({"duration_of": lambda row: -1}, "never future business"),
])
def test_build_sec_table_rejects_a_spec_that_does_not_fit_the_s_table(s_model, change,
                                                                    error):
    with pytest.raises(ValueError, match=error):
        build_sec_table(dataclasses.replace(SPEC, **change), s_model)


def _policy_ids(s_model, table):
    """A companion built from the SEC table: one row per SEC point and its policy."""
    return table[["point_id", "policy_id", "source_mth"]]


def test_regeneration_is_stable_and_reports_an_edited_s_row(tmp_path, monkeypatch):
    """T6's round trip, in a copy of the product directory.

    Written, the files check clean and a rewrite touches nothing.  Then a reworded S
    ``policy_id`` reaches every cell that copies or composes it, in the table and in its
    companion, and nothing else.
    """
    temp_inputs(tmp_path, model_path(TERM))
    spec = dataclasses.replace(SPEC, companions={"policy_ids_sec.csv": _policy_ids})
    monkeypatch.setitem(SEC_SPECS, "Term_US_SEC_selftest", spec)
    table_path = tmp_path / "model_point_table_sec.csv"
    companion_path = tmp_path / "policy_ids_sec.csv"

    assert write_generated("Term_US_SEC_selftest", tmp_path) == {
        table_path: True, companion_path: True}
    assert check_generated("Term_US_SEC_selftest", tmp_path) == []
    written, stamp = table_path.read_bytes(), table_path.stat().st_mtime_ns
    assert write_generated("Term_US_SEC_selftest", tmp_path) == {
        table_path: False, companion_path: False}
    assert table_path.read_bytes() == written and table_path.stat().st_mtime_ns == stamp
    assert written.decode().splitlines()[3] == (
        "3,TL-000001-M12,35,M,StdNT,T10,100000.0,A,0.939248,3.5,12,derived,TL-000001,12")

    s_csv = tmp_path / "model_point_table.csv"
    s_csv.write_bytes(s_csv.read_bytes().replace(b"TL-000001", b"TL-900001"))
    drift = check_generated("Term_US_SEC_selftest", tmp_path)
    found = [re.match(r"(\S+): row \d+ \(point_id (\d+)\), (\w+): committed", line)
             for line in drift]
    assert all(found), drift
    assert {m.groups() for m in found} == {
        ("model_point_table_sec.csv", point, column)
        for point in ("1", "3", "4") for column in ("policy_id", "source_policy_id")
    } | {("policy_ids_sec.csv", point, "policy_id") for point in ("1", "3", "4")}
    assert ("model_point_table_sec.csv: row 3 (point_id 3), policy_id: committed "
            "'TL-000001-M12', generated 'TL-900001-M12'") in drift

    write_generated("Term_US_SEC_selftest", tmp_path)
    assert check_generated("Term_US_SEC_selftest", tmp_path) == []
    companion_path.unlink()
    assert check_generated("Term_US_SEC_selftest", tmp_path) == [
        "policy_ids_sec.csv: generated, but not committed"]

    # A committed row cut short shows its missing cells, and a stray line is a row too.
    write_generated("Term_US_SEC_selftest", tmp_path)
    text = table_path.read_bytes()
    table_path.write_bytes(text.replace(b",TL-900001,-3\n", b"\n") + b"\n")
    assert check_generated("Term_US_SEC_selftest", tmp_path) == [
        "model_point_table_sec.csv: row 4 (point_id 4), source_policy_id: committed None, "
        "generated 'TL-900001'",
        "model_point_table_sec.csv: row 4 (point_id 4), source_mth: committed None, "
        "generated '-3'",
        "model_point_table_sec.csv: committed row 5 (a blank line) is no longer generated"]


def test_regeneration_reads_a_float_by_its_value_not_its_spelling(tmp_path, monkeypatch):
    """A committed float spelled otherwise, or a last bit off, is current and left alone.

    Another platform's pandas may spell a computed float otherwise, and its libm may compute
    it a last bit apart (``sec_support``'s module docstring), so neither is drift and
    neither is rewritten.  A real change of value is drift, and so is ``1`` for ``1.0``,
    which changes the dtype pandas reads; so are cells beyond the header, and text that is
    not the writer's own once its cells agree.
    """
    model = _read("respell", temp_inputs(tmp_path, model_path(TERM)))
    monkeypatch.setitem(SEC_SPECS, "Term_US_SEC_selftest", SPEC)
    path = tmp_path / "model_point_table_sec.csv"
    try:
        _respellings(model, path, tmp_path)
    finally:
        model.close()


def _respellings(model, path, product_dir):
    """The body of the test above, on an S model read once from ``product_dir``."""
    def check():
        return check_generated("Term_US_SEC_selftest", product_dir, s_model=model)

    def write():
        return write_generated("Term_US_SEC_selftest", product_dir, s_model=model)[path]

    write()
    written = path.read_bytes().decode("utf-8")
    row = written.splitlines()[3].split(",")
    count = float(row[8])
    assert row[:3] == ["3", "TL-000001-M12", "35"] and 0.9 < count < 1.0

    def with_count(text):
        """The committed table with the derived row's policy_count spelled ``text``."""
        lines = written.splitlines()
        cells = lines[3].split(",")
        cells[8] = text
        lines[3] = ",".join(cells)
        return "\n".join(lines) + "\n"

    def committed(text):
        path.write_bytes(text.encode("utf-8"))
        stamp = path.stat().st_mtime_ns
        drift = check()
        rewritten = write()
        assert rewritten == bool(drift)
        assert rewritten or path.stat().st_mtime_ns == stamp
        return drift

    spelled = f"{count:.16e}"
    assert spelled != row[8] and float(spelled) == count
    assert committed(with_count(spelled)) == []
    assert committed(with_count(repr(math.nextafter(count, 2.0)))) == []
    moved = repr(count * (1 + 1e-9))
    assert committed(with_count(moved)) == [
        f"model_point_table_sec.csv: row 3 (point_id 3), policy_count: committed "
        f"{moved!r}, generated {row[8]!r}"]
    assert committed(written.replace("\n3,", "\n3.0,")) == [
        "model_point_table_sec.csv: row 3 (point_id 3), point_id: committed '3.0', "
        "generated '3'"]
    assert committed(written.replace(",twin,TL-000002,0\n", ",twin,TL-000002,0,x\n")) == [
        "model_point_table_sec.csv: committed row 2 (point_id 2) has cells beyond its "
        "header: ['x']"]
    assert committed(written.replace("\n", "\r\n")) == [
        "model_point_table_sec.csv: the cells agree, but the text differs (quoting or line "
        "ends); regenerate it"]
    assert path.read_bytes().decode("utf-8") == written


def test_an_unregistered_spec_name_is_refused():
    with pytest.raises(KeyError, match="Term_US_SEC_nonesuch"):
        check_generated("Term_US_SEC_nonesuch")
