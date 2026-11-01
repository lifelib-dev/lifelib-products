"""Support for the SEC models' tests: the twin and splice comparisons, and the generator.

USLIB-SEC-PLAN.md puts a ``<Name>_US_SEC`` model beside each ``<Name>_US_S`` (its D1): the S
model taught to run in force at a valuation date, and then to compile.  The S model is not
touched.  It stays the reference, and this module is how the SEC suites lean on it rather
than restate it: every S worked example, its intermediate cells included, becomes an SEC
assertion through a comparison instead of through a second copy of the golden.

What is here, by the plan's tests (its §5.2):

T1, the twin identity
    :func:`sweep` evaluates on an S model point what the conventions suite's sweep
    evaluates and every other ``result_*`` report, and :func:`twin_mismatches` then
    compares every cell of the S model, at every argument tuple the S cell cached inside
    its frame, less :data:`TWIN_EXEMPT_DEFAULT`; an S cell the SEC model lacks is a
    mismatch.
T2 and T3, the splice and the future new business
    :func:`temp_inputs` writes a temporary input directory -- the model, its CSVs, extra
    model points and edited tables; :func:`shift_months` re-bases a month-keyed table for
    a point whose valuation date is a later S month; and :func:`frame_mismatches` compares
    two ``result_cf()`` frames on an offset.
T6, regeneration
    :class:`SecSpec` says how one product's SEC model point table derives from its S model,
    :data:`SEC_SPECS` holds one per product, :func:`build_sec_table` builds the table and
    its companions, and :func:`write_generated` and :func:`check_generated` write them, or
    report cell by cell where the committed files have drifted from S.

**Why the generator lives in the tests.**  ``tools/gen_sec_points.py`` is only a command
line over :func:`write_generated` and :func:`check_generated`.  The logic is here because
``lifelib.create()`` copies a library, this ``tests/`` folder with it, but not the
repository's ``tools/``, and T6 has to regenerate inside such a copy too.  A user who edits
an S row in their copy must hear that the SEC table has gone stale from the suite that
ships with the copy, not from a tool they do not have.

**Two clocks, and which way an offset runs.**  Every SEC model point carries
``source_mth``, and SEC month ``t`` is S month ``t + source_mth``: 0 for the twin of an S
new-business row; 108 for the twin of ``WholeLife_US_S`` point 1, which S opens at its own
policy month 108; ``d`` for a row derived from S month ``d``; ``-k`` for a future row
issued ``k`` months after the valuation date.  Both comparisons take their ``t_offset`` in
that one sense, SEC ``t`` against S ``t + t_offset``, so a test passes the row's
``source_mth`` to either: :func:`twin_mismatches` evaluates the SEC cells at S's cached
``t - t_offset``, and :func:`frame_mismatches` reads SEC row ``t`` against S row
``t + t_offset``.  A wrong sign cannot pass quietly: it compares the wrong months, and those
differ.

**What the generator writes.**  The SEC model point table and its companions are input
files as ``CLAUDE.md`` defines them, so none of their cells may name a company or a
product.  The generator copies every text cell from S, where the T6 check keeps it current,
or composes it from S's own keys and a month (``TL-000001-M12``), and it adds no word of its
own beyond a fixed template (D8).  It cannot vouch for S: a name in an S cell is copied.
That is why ``CLAUDE.md``'s pre-commit search still applies to every file it writes.

**Floats in CSV.**  Every file this module writes goes through one writer, for two
properties.  It is deterministic: the same values give the same bytes, so a regeneration
with no S change leaves the committed files alone.  And its floats come back from
``pd.read_csv``, as the models call it, exactly wherever that parser can produce the double
at all, which plain ``repr`` falls well short of.  pandas' default parser keeps at most 17
digits, counts a leading ``0`` among them, and accumulates them in floating point, so it
misreads about a third of the shortest round-trip strings of random doubles (31 to 40 %
over four samples of 20,000 to 30,000) and nearly half of those of counts between 0.9 and
1 (pandas 3.0.5; ``float_precision="round_trip"`` is exact, but no model reader passes it).
So a float is written as its shortest ``repr`` when the default parser reads that back
exactly, and otherwise as the nearest 17-digit string that both the default parser and a
correctly rounding one read as the same double.  For some doubles no such string exists:
the default parser produces them from no text near them.  That is 6 to 9 % of random
doubles, and about one count in six between 0.9 and 1.  Those get the correctly rounded
text the default parser reads closest, which a correct parser reads exactly and the
default parser to within two ulps.  That is far inside the 1e-9 every comparison here
uses, and it never touches a value typed into a table: a short decimal such as ``0.0445``
reads back exactly, so only computed values, a count or a balance carried over from S,
are ever at stake.

**Why T6 reads a float by its value.**  The text chosen for a computed float depends on the
parser it was chosen for, and the float itself on the platform that computed it.  pandas'
parser is C code: a build that contracts its digit loop into fused multiply-adds, as
compilers for arm64 may, reads 15 % of the texts this writer weighs differently and would
pick another text for 7 % of random doubles (measured on a Python model of the parser that
reproduces pandas 3.0.5 on all of 55,000 texts), and a pandas that parses correctly would
pick ``repr`` for every one of them.  And
``pow``, which turns annual rates monthly in every model here, is not rounded alike by
every platform's libm.  So :func:`check_generated` compares a float cell by value, to
1e-12, and :func:`write_generated` leaves a file alone when only such spellings differ: the
suite runs on Linux, Windows and macOS against whichever pandas they install, and a
committed file written on one of them must check clean on the others.
"""
import csv
import dataclasses
import io
import itertools
import math
import numbers
import pathlib
import re
import shutil
from collections.abc import Callable, Mapping

import modelx as mx
import numpy as np
import pandas as pd

from us_registry import MODELS, model_path


# ---------------------------------------------------------------------------
# T1 -- the twin identity


TWIN_EXEMPT_DEFAULT = frozenset({"model_point", "pols_if_init", "input_dir"})
"""The cells whose meaning SEC changes by design, which the twin identity (T1) skips.

``model_point``
    The SEC row carries columns its S twin does not: ``policy_count``, ``duration_mth``,
    ``row_kind``, ``source_policy_id``, ``source_mth`` and any opening state (D5, D6, D8),
    and a renamed column such as ``pols_if_init`` turned ``policy_count``.  The Series
    cannot agree, and nothing is lost by skipping it: whatever the projection reads from it
    reaches T1 through the cells that read it, whether an accessor (``sum_assured``,
    ``age_at_entry``, ...) or a per-``t`` formula that subscripts ``model_point()`` itself,
    as ``WholeLife_US_S.premium_pp_ann(t)`` and ``VUL_US_S.coi_rate(t)`` do.
``pols_if_init``
    SEC's is the count in force *at* the valuation date (D5), so it is 0 for a policy issued
    at ``t = 0``, whose count enters through ``pols_new_biz(0)`` instead.  S's is the count
    at issue.  ``pols_if(0)``, the count that weights row 0, still agrees, and T1 compares
    it.
``input_dir``
    A ``Data`` cell, which T1 meets when it compares two ``Data`` Spaces: two models read
    from two folders resolve it to two directories by construction.  The conventions suite
    asserts it elsewhere, that each model's resolves to its own parent.

A product adds its own exemptions in its :class:`SecSpec`'s ``exempt``, and T1 skips the
union.  Every name added there is a cell T1 no longer checks, so each needs a reason as
specific as these three.  That includes an S cell the SEC model drops or renames, which
:func:`twin_mismatches` otherwise reports as missing.
"""


def sweep(proj):
    """Evaluate on one model point what T1 compares, and return it.

    That is ``result_cf()`` first, then every other ``result_*`` cells, then every
    ``check_*`` cells except the per-``t`` ``*_resid`` ones.  It is the conventions sweep,
    the ``result_cf()`` and checks that
    ``test_model_conventions.test_every_model_point_projects`` calls on every point, plus
    every other ``result_*`` report, such as ``result_cf_annual()``.

    It exists for T1.  :func:`twin_mismatches` enumerates the argument tuples each S cell
    has cached, so what the S sweep evaluates inside its frame is what T1 covers.  A cell
    the sweep never reaches, such as ``Term_US_S.pols_lapse``, which no result column
    reads, holds no keys and is compared nowhere.  A test that wants more calls the extra
    cells on the S side before it compares.

    Returns ``{name: value}`` in evaluation order, so a caller can assert on the checks
    without calling them a second time.
    """
    names = ["result_cf"]
    names += [c for c in proj.cells if c.startswith("result_") and c != "result_cf"]
    names += [c for c in proj.cells
              if c.startswith("check_") and not c.endswith("_resid")]
    return {name: proj.cells[name]() for name in names}


def _args(key, n_params):
    """The argument tuple behind one modelx cache key.

    ``Cells.keys()`` does not give tuples throughout (found by experiment, modelx 0.33): a
    cells with no parameter is cached under ``()``, a cells with one under the bare argument
    (``5``, not ``(5,)``), and a cells with two or more under the full tuple, defaults
    filled in, so ``claims(3)`` on ``claims(t, kind=None)`` is cached as ``(3, None)``.

    The bare argument of a one-parameter cells may itself be a tuple: ``f(("call",
    "put"))`` is cached under ``("call", "put")``.  Only the parameter count tells that key
    from a two-argument one, which is why the count is passed in, and why the cached value
    is read by calling the cells with these arguments rather than through
    ``Cells.items()``: that looks each key up again by ``cells[key]``, which takes such a
    tuple for two arguments and raises ``TypeError``.
    """
    if n_params == 0:
        return ()
    if n_params == 1:
        return (key,)
    return tuple(key)


def _py(x):
    """A numpy scalar as the Python scalar it holds, so messages read ``1.5``, not
    ``np.float64(1.5)``."""
    return x.item() if isinstance(x, np.generic) else x


def _call(name, args):
    return f"{name}({', '.join(repr(_py(a)) for a in args)})"


def _typed(x):
    return f"{_py(x)!r} ({type(x).__name__})"


def _error_text(err):
    """One line for an exception, unwrapping modelx's ``FormulaError``.

    modelx re-raises any error inside a formula as ``FormulaError``, whose first line is
    always "Error raised during formula execution" and whose second line is the original
    error, ``ValueError: ...``.  The second line is the informative one.
    """
    lines = [line for line in str(err).splitlines() if line.strip()]
    if type(err).__name__ == "FormulaError" and len(lines) > 1:
        return lines[1]
    return f"{type(err).__name__}: {lines[0] if lines else ''}".rstrip(": ")


def _is_bool(x):
    return isinstance(x, (bool, np.bool_))


def _is_number(x):
    """A real number, Python or numpy, that is not a bool.

    ``bool`` is a ``numbers.Real``, and ``True == 1``.  A cells that returned ``True`` in S
    and ``1`` in SEC has changed type, and the house's ``check_*`` contract is that a check
    returns a bool, so bools are compared as bools, never as numbers.
    """
    return isinstance(x, numbers.Real) and not _is_bool(x)


def _close(a, b, rtol, atol):
    """Whether two numbers agree: symmetric, so S against SEC reads as SEC against S.

    Equal values, infinities included, agree, and so do two NaNs.  An infinity agrees with
    nothing else, which the tolerance alone would get wrong: ``|inf - 5| <= rtol * inf``.
    """
    if a == b or (a != a and b != b):
        return True
    if not (math.isfinite(a) and math.isfinite(b)):
        return False
    return abs(a - b) <= atol + rtol * max(abs(a), abs(b))


def _close_arrays(x, y, rtol, atol):
    """:func:`_close`, element by element, on two float arrays of one shape."""
    with np.errstate(invalid="ignore", over="ignore"):
        same = (x == y) | (np.isnan(x) & np.isnan(y))
        finite = np.isfinite(x) & np.isfinite(y)
        near = np.abs(x - y) <= atol + rtol * np.maximum(np.abs(x), np.abs(y))
    return same | (finite & near)


def _numeric(series):
    dtype = series.dtype
    return pd.api.types.is_numeric_dtype(dtype) and not pd.api.types.is_bool_dtype(dtype)


def _few(labels, show):
    """Up to five labels, and how many more there are."""
    labels = list(labels)
    text = ", ".join(show(v) for v in labels[:5])
    return text + (f" and {len(labels) - 5} more" if len(labels) > 5 else "")


def _column_summary(x, y, rtol, atol, show):
    """How two aligned Series differ, in one line, or ``None`` where they agree.

    Numeric Series compare as arrays.  Anything else (a str column, an object column of
    mixed values such as a ``model_point()`` row) compares element by element, as single
    values do.
    """
    xv, yv = x.to_numpy(), y.to_numpy()
    if not len(xv):
        return None
    if _numeric(x) and _numeric(y):
        xf = x.to_numpy(dtype=float, na_value=np.nan)
        yf = y.to_numpy(dtype=float, na_value=np.nan)
        bad = ~_close_arrays(xf, yf, rtol, atol)
        with np.errstate(invalid="ignore", over="ignore"):
            gap = np.abs(yf - xf)
        gap[np.isnan(gap)] = np.inf      # a NaN against a number is the largest gap
    else:
        bad = np.array([bool(_value_diffs(p, q, rtol, atol)) for p, q in zip(xv, yv)],
                       dtype=bool)
        gap = None
    n = int(bad.sum())
    if not n:
        return None
    i = int(np.flatnonzero(bad)[0])
    text = (f"{n} of {len(xv)} differ, first at {show(x.index[i])}: "
            f"S {_py(xv[i])!r}, SEC {_py(yv[i])!r}")
    if gap is not None and n > 1:
        gap[~bad] = -1.0
        j = int(np.argmax(gap))
        text += f"; largest |diff| {gap[j]:.3g} at {show(x.index[j])}"
    return text


def _on_sec_clock(a, b, t_offset):
    """Relabel S's ``t``-indexed pandas value on SEC's clock, and say how to show a label.

    Under an offset an S row ``t`` is SEC row ``t - t_offset``.  Only SEC months at or
    after ``max(0, -t_offset)`` have a counterpart on both sides: none precedes the
    valuation date, and a future point's months before its issue have none in S.  Both
    sides are cut to those months, so the label sets compare like for like.
    """
    name = a.index.name
    if t_offset and name == "t" and b.index.name == "t":
        start = max(0, -t_offset)
        a = a.copy(deep=False)
        a.index = a.index - t_offset
        a, b = a[a.index >= start], b[b.index >= start]
        return a, b, lambda v: f"t={_py(v)} (S t={_py(v) + t_offset})"
    if name is None:
        return a, b, lambda v: repr(_py(v))
    return a, b, lambda v: f"{name}={_py(v)!r}"


def _pandas_diffs(a, b, rtol, atol, t_offset):
    """How two Series, or two DataFrames, differ: label sets first, then values.

    The values compare on the labels both sides hold, with tolerance.  A label or a
    column present on one side only is reported too, rather than dropped from the
    comparison: on a new-business twin the SEC frame must be the S frame, so a row SEC
    never projects is a difference, not a smaller comparison.
    """
    a, b, show = _on_sec_clock(a, b, t_offset)
    lines = []
    frame = isinstance(a, pd.DataFrame)
    if frame:
        only_s = [c for c in a.columns if c not in b.columns]
        only_sec = [c for c in b.columns if c not in a.columns]
        if only_s:
            lines.append(f"columns only in S: {only_s}")
        if only_sec:
            lines.append(f"columns only in SEC: {only_sec}")
        if not only_s and not only_sec and list(a.columns) != list(b.columns):
            lines.append("the same columns in a different order")
        columns = [c for c in a.columns if c in b.columns]
    if a.index.is_unique and b.index.is_unique:
        only_s = a.index.difference(b.index, sort=False)
        only_sec = b.index.difference(a.index, sort=False)
        if len(only_s):
            lines.append(f"{len(only_s)} labels only in S: {_few(only_s, show)}")
        if len(only_sec):
            lines.append(f"{len(only_sec)} labels only in SEC: {_few(only_sec, show)}")
        shared = a.index.intersection(b.index, sort=False)
        a, b = a.loc[shared], b.loc[shared]
    elif not a.index.equals(b.index):
        return lines + ["cannot align: duplicate labels, and the two indexes differ"]
    if frame:
        for c in columns:
            text = _column_summary(a[c], b[c], rtol, atol, show)
            if text:
                lines.append(f"column {c!r}: {text}")
    else:
        text = _column_summary(a, b, rtol, atol, show)
        if text:
            lines.append(text)
    return lines


def _value_diffs(a, b, rtol, atol, t_offset=0):
    """How S's value ``a`` and SEC's value ``b`` differ: descriptions, empty if they agree.

    Numbers, Python or numpy, compare with tolerance; bools, strings, ``None`` and paths
    compare exactly; Series and DataFrames compare on their shared labels with tolerance
    (:func:`_pandas_diffs`); arrays, lists, tuples, dicts and sets compare element by
    element.  Those are every kind of value the twelve S models cache (surveyed over the
    first point of each: floats, ints, bools and strings, Series and DataFrames, one dict
    in ``DIA_US_S``, one tuple in ``RILA_US_S``, a list in ``VA_US_S`` and ``VUL_US_S``).

    Two values of different known kinds, a ``str`` against an ``int``, simply differ.  A
    value of a kind not listed is reported as *uncomparable* rather than passed: a check
    that cannot look at a value has not shown it equal.
    """
    if _is_bool(a) or _is_bool(b):
        if _is_bool(a) and _is_bool(b) and bool(a) == bool(b):
            return []
        return [f"S {_typed(a)}, SEC {_typed(b)}"]
    if _is_number(a) and _is_number(b):
        if _close(a, b, rtol, atol):
            return []
        with np.errstate(invalid="ignore", over="ignore"):
            return [f"S {_py(a)!r}, SEC {_py(b)!r}, diff {_py(b) - _py(a):+.3g}"]
    if isinstance(a, str) and isinstance(b, str):
        return [] if a == b else [f"S {a!r}, SEC {b!r}"]
    if a is None and b is None:
        return []
    if isinstance(a, pathlib.PurePath) and isinstance(b, pathlib.PurePath):
        return [] if a == b else [f"S {str(a)!r}, SEC {str(b)!r}"]
    if isinstance(a, pd.DataFrame) and isinstance(b, pd.DataFrame):
        return _pandas_diffs(a, b, rtol, atol, t_offset)
    if isinstance(a, pd.Series) and isinstance(b, pd.Series):
        return _pandas_diffs(a, b, rtol, atol, t_offset)
    if isinstance(a, np.ndarray) and isinstance(b, np.ndarray):
        if a.shape != b.shape:
            return [f"shape: S {a.shape}, SEC {b.shape}"]
        # As nested lists, or as the scalar a 0-d array holds, each compared as its kind.
        return _value_diffs(a.tolist(), b.tolist(), rtol, atol)
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        if len(a) != len(b):
            return [f"length: S {len(a)}, SEC {len(b)}"]
        return [f"[{i}] {line}" for i, (x, y) in enumerate(zip(a, b))
                for line in _value_diffs(x, y, rtol, atol)]
    if isinstance(a, Mapping) and isinstance(b, Mapping):
        lines = []
        only_s = [k for k in a if k not in b]
        only_sec = [k for k in b if k not in a]
        if only_s:
            lines.append(f"keys only in S: {_few(only_s, repr)}")
        if only_sec:
            lines.append(f"keys only in SEC: {_few(only_sec, repr)}")
        return lines + [f"[{k!r}] {line}" for k in a if k in b
                        for line in _value_diffs(a[k], b[k], rtol, atol)]
    if isinstance(a, (set, frozenset)) and isinstance(b, (set, frozenset)):
        return [] if a == b else [f"S {a!r}, SEC {b!r}"]
    if _known(a) and _known(b):
        return [f"S {_typed(a)}, SEC {_typed(b)}"]
    return [f"uncomparable: S {type(a).__name__}, SEC {type(b).__name__}"]


_KNOWN_KINDS = (str, pathlib.PurePath, pd.DataFrame, pd.Series, np.ndarray, list, tuple,
                Mapping, set, frozenset)


def _known(x):
    """Whether :func:`_value_diffs` knows how to compare a value of this kind."""
    return x is None or _is_bool(x) or _is_number(x) or isinstance(x, _KNOWN_KINDS)


def _frame_end(space):
    """S's ``proj_len()``, the exclusive end of its frame, or ``None`` if it has none.

    Every model's ``Projection`` has the cell, and a ``Data`` Space or a synthetic one need
    not.  It is read, never compared here: a comparison may exempt it, as the splice does.
    """
    cells = space.cells
    if "proj_len" not in cells or cells["proj_len"].parameters:
        return None
    return cells["proj_len"]()


def _is_month(x):
    return isinstance(x, numbers.Integral) and not _is_bool(x)


def _twin_lines(s_proj, sec_proj, exempt, arg_map, t_offset, rtol, atol):
    """Every mismatch line, lazily, so :func:`twin_mismatches` can stop at its limit."""
    sec_cells = sec_proj.cells
    end = _frame_end(s_proj)
    for name in list(s_proj.cells):
        if name in exempt:
            continue
        if name not in sec_cells:
            yield (f"{name}: a cell of S that SEC lacks; a cell SEC drops by design is "
                   f"named in the spec's exempt, with its reason")
            continue
        s_cells, cells = s_proj.cells[name], sec_cells[name]
        n_params = len(s_cells.parameters)
        s_t_pos = s_cells.parameters.index("t") if "t" in s_cells.parameters else None
        params = cells.parameters
        t_pos = params.index("t") if "t" in params else None
        for key in list(s_cells.keys()):
            args = _args(key, n_params)
            if (end is not None and s_t_pos is not None and s_t_pos < len(args)
                    and _is_month(args[s_t_pos]) and args[s_t_pos] >= end):
                continue                        # read ahead of S's frame: not compared
            expected = s_cells(*args)           # a cached key: the cache, not a new value
            sec_args = args if arg_map is None else arg_map(name, args)
            if sec_args is None:
                continue
            sec_args = tuple(sec_args)
            if t_pos is not None and t_pos < len(sec_args):
                t = sec_args[t_pos]
                if _is_month(t):
                    t = int(t) - t_offset
                    if t < 0:
                        continue
                    sec_args = sec_args[:t_pos] + (t,) + sec_args[t_pos + 1:]
            label = _call(name, args)
            if sec_args != args:
                label += f" [SEC {_call(name, sec_args)}]"
            try:
                actual = cells(*sec_args)
            except Exception as err:            # reported, so the sweep goes on
                yield f"{label}: SEC raised {_error_text(err)}"
                continue
            for line in _value_diffs(expected, actual, rtol, atol, t_offset):
                yield f"{label}: {line}"


def twin_mismatches(s_proj, sec_proj, *, exempt=TWIN_EXEMPT_DEFAULT, arg_map=None,
                    t_offset=0, rtol=1e-9, atol=1e-9, limit=50):
    """Where the SEC model differs from its S twin, cell by cell: T1 (§5.2).

    For every cells name of the S Space not in ``exempt``, and for every argument tuple the
    S cells has cached inside S's frame, the SEC cells is evaluated at the same arguments
    and its value compared with the value S cached.  So the S Space must be swept first
    (:func:`sweep`), and what the sweep reached inside the frame is what is compared.  The
    S cache is read, never re-evaluated.  Through this, the S goldens are asserted on the
    SEC model too, with no number restated, wherever they sit on a cells the sweep
    reaches: ``result_cf()``, and intermediate cells such as MYGA's surrender trace.  An S
    cells the SEC Space lacks is reported, one line for the cells, rather than left out of
    the comparison: a cells renamed or dropped would otherwise take its goldens with it
    without a word.  One the SEC model drops by design is named in ``exempt``, with its
    reason, as any other exemption is.

    Only S's own frame is compared.  Where S has a ``proj_len()`` cell, as every model's
    ``Projection`` does, a key whose S ``t`` is at or past it is skipped.  S evaluates such
    a month only when a formula reads ahead of its frame, as ``Term_US_S.jump_ratio()``
    reads ``premium_pp_ann(12n)`` on a point whose cover ends with the level period, or
    ``conv_rate`` reads ``conv_elig(t + 12)`` near expiry, and it answers from its tables
    as though cover went on, where an SEC model answers that the month is outside cover
    (R1).  S's frame ends where cover ends, on either clock, and :func:`frame_mismatches`
    holds the two frames' ends together.

    ``s_proj`` and ``sec_proj`` are usually ItemSpaces, ``Projection[1]`` of each model, but
    any two Spaces work, ``Data`` against ``Data`` included.

    The arguments are mapped before the SEC call.  ``arg_map(name, args)`` returns SEC's
    arguments for S's (the default is the identity, and Phase 2 maps timing strings to the
    int References of the same name, R9); returning ``None`` skips that key.  Then the
    argument named ``t``, if the SEC cells has one, moves to SEC's clock: SEC month ``t`` is
    S month ``t + t_offset``, as in :func:`frame_mismatches`, so the SEC cells is called at
    S's ``t - t_offset``, and a row passes its ``source_mth`` (``d`` for a row derived from
    S month ``d``; see the module docstring).  A key whose SEC ``t`` falls below 0 is
    skipped: no month precedes the valuation date, and R1 forbids evaluating one.  Under an
    offset a ``t``-indexed Series or DataFrame, such as ``result_cf()``, is relabelled the
    same way before it is compared.  Only the
    parameter named ``t`` moves.  Another that holds a month, such as the segment month
    ``m`` of IUL's ``seg_bal_pp(t, m)``, moves through ``arg_map``.

    Values compare by kind (:func:`_value_diffs`): numbers with ``rtol`` and ``atol``,
    symmetrically; bools and strings exactly; pandas values on their shared labels, with
    any label or column found on one side only reported too; containers element by
    element; anything else as *uncomparable*.  An exception the SEC cells raises is
    reported, not propagated, so one broken cells does not hide the rest.

    Returns readable lines, in cells and cache order, empty when the twins agree:
    ``"expenses(0): S 302.5, SEC 302.5833333333333, diff +0.0833"``.  At most ``limit``
    are returned.  When more were found, the scan stops there, so a model that differs
    everywhere fails fast, and the last line says so, unless ``limit`` is 1: then the one
    line is the first mismatch.
    """
    if limit < 1:
        raise ValueError(f"limit must be at least 1, not {limit}")
    found = []
    for line in _twin_lines(s_proj, sec_proj, exempt, arg_map, t_offset, rtol, atol):
        found.append(line)
        if len(found) > limit:
            break
    if len(found) > limit:
        found = found[:limit]
        if limit > 1:
            found[-1] = (f"(more than {limit - 1} mismatches; the scan stopped, and the "
                         f"rest are not listed)")
    return found


def frame_mismatches(s_df, sec_df, *, t_offset=0, columns=None, rtol=1e-9, atol=1e-9):
    """Where two ``result_cf()`` frames differ, SEC row ``t`` being S row ``t + t_offset``.

    The splice (T2) and future new business (T3) compare whole frames on an offset: a row
    derived from S month ``d`` reproduces S from ``d`` on, so its row ``t`` is S's row
    ``t + d``, and ``t_offset=d``.  That is the direction of ``source_mth``, and the one
    :func:`twin_mismatches` takes too, so a test passes a row's ``source_mth`` to both.

    The comparison runs over ``columns``, or by default every column both frames hold, and
    over the shared ``t`` range: from the later first row to the earlier last row, on SEC's
    labels.  Rows before that range are not compared, because they are the part one side
    does not project by design: S's months before the splice, or the pre-issue zeros of a
    future point.  The two frames' *ends* have no such excuse.  Each runs to the end of
    cover, which is one instant on both clocks: S's last row ``L - 1`` is SEC's ``L - 1 -
    d`` for a row derived at ``d``, and ``L - 1 + k`` for one issued ``k`` months late.  So
    frames that end apart are reported, as an SEC ``proj_len()`` that is wrong, even though
    the rows they share agree.  So is a row *inside* the range that one frame lacks, an
    empty range, an explicitly named column either frame lacks, or a comparison left with
    no column at all: a comparison that compares less than the whole splice cannot pass.
    To compare part of a frame, cut both frames to it.

    Returns one line per column that differs, with the count, the first differing row and
    the largest gap, after any line about the frames' shape; empty when the frames agree.
    """
    s_view = s_df.copy(deep=False)
    s_view.index = s_df.index - t_offset
    lines = []
    if columns is None:
        columns = [c for c in s_df.columns if c in sec_df.columns]
    else:
        columns = list(columns)
        for side, df in (("S", s_df), ("SEC", sec_df)):
            missing = [c for c in columns if c not in df.columns]
            if missing:
                lines.append(f"columns missing from {side}: {missing}")
        columns = [c for c in columns if c in s_df.columns and c in sec_df.columns]
    if not columns:
        return lines + ["no column to compare"]
    if not len(s_view) or not len(sec_df):
        return lines + [f"no rows to compare: S has {len(s_df)}, SEC {len(sec_df)}"]
    lo = max(s_view.index.min(), sec_df.index.min())
    hi = min(s_view.index.max(), sec_df.index.max())
    if lo > hi:
        return lines + [
            f"no shared rows: S rows {s_df.index.min()}..{s_df.index.max()} are SEC "
            f"t = {s_view.index.min()}..{s_view.index.max()}, and SEC has "
            f"t = {sec_df.index.min()}..{sec_df.index.max()}"]

    def show(t):
        t = _py(t)
        return f"t={t} (S t={t + t_offset})" if t_offset else f"t={t}"

    if s_view.index.max() != sec_df.index.max():
        lines.append(f"the frames end apart: S ends at {show(s_view.index.max())}, SEC at "
                     f"t={_py(sec_df.index.max())}")
    a = s_view[(s_view.index >= lo) & (s_view.index <= hi)]
    b = sec_df[(sec_df.index >= lo) & (sec_df.index <= hi)]
    for side, mine, other in (("S", a, b), ("SEC", b, a)):
        gaps = mine.index.difference(other.index, sort=False)
        if len(gaps):
            lines.append(f"{len(gaps)} rows inside the shared range only in {side}: "
                         f"{_few(gaps, show)}")
    shared = a.index.intersection(b.index, sort=False)
    for c in columns:
        text = _column_summary(a.loc[shared, c], b.loc[shared, c], rtol, atol, show)
        if text:
            lines.append(f"column {c!r}: {text}")
    return lines


# ---------------------------------------------------------------------------
# Writing CSV -- deterministic, and exact for the models' own reader


def _default_reads(texts):
    """The doubles ``pd.read_csv``'s default parser makes of some float texts.

    The models read every input with a plain ``pd.read_csv(path, index_col=...)``, the C
    parser at its default ``float_precision``, so this is the reading that matters.
    """
    if not texts:
        return []
    buf = io.StringIO("v\n" + "\n".join(texts) + "\n")
    return pd.read_csv(buf, dtype={"v": "float64"})["v"].tolist()


def _candidates(v):
    """17-digit texts near ``v`` that a correctly rounding parser reads as ``v``.

    The nearest first.  Each keeps all 17 digits and no leading zero, so pandas' parser,
    which counts at most 17 digits, leading zeros included, sees every one of them: fixed
    notation from 1 up to 1e16, scientific otherwise.  Which of them the default parser
    also reads as ``v`` is for :func:`_float_texts` to find out.
    """
    sign = "-" if v < 0 else ""
    mantissa, exponent = f"{abs(v):.16e}".split("e")
    n0, e10 = int(mantissa.replace(".", "")), int(exponent)
    out = []
    for j in sorted(range(-12, 13), key=lambda j: (abs(j), j)):
        digits = str(n0 + j)
        if len(digits) != 17:
            continue
        if 0 <= e10 < 16:
            body = digits[:e10 + 1] + "." + digits[e10 + 1:]
        else:
            body = f"{digits[0]}.{digits[1:]}e{e10:+03d}"
        if float(sign + body) == v:
            out.append(sign + body)
    return out


def _float_texts(values):
    """The text written for each float: exact for the models' reader wherever possible.

    The shortest ``repr`` where pandas' default parser reads it back exactly, which covers
    every value that came from a short decimal.  Otherwise the nearest 17-digit text that
    both that parser and a correctly rounding one read as the same double, found by
    asking pandas.  Where none exists, whichever of these correctly rounded texts the
    default parser reads closest.  That is rarely the ``repr``: a fixed-notation ``repr``
    such as ``0.00012345678901234567`` spends four of pandas' 17 digits on leading zeros,
    and reads thousands of ulps off, where its 17-digit scientific form reads within a
    few.
    """
    values = [float(v) for v in values]
    texts = [repr(v) for v in values]
    probe = [i for i, v in enumerate(values) if math.isfinite(v) and v != 0.0]
    first = dict(zip(probe, _default_reads([texts[i] for i in probe])))
    misread = [i for i in probe if first[i] != values[i]]
    if misread:
        options = {i: _candidates(values[i]) for i in misread}
        reads = iter(_default_reads([c for i in misread for c in options[i]]))
        for i in misread:
            v = values[i]
            read = [(texts[i], first[i])] + [(c, next(reads)) for c in options[i]]
            exact = [c for c, r in read[1:] if r == v]
            texts[i] = exact[0] if exact else min(read, key=lambda cr: abs(cr[1] - v))[0]
    return texts


def _csv_text(df):
    """The CSV text of ``df``, exactly as every file this module writes is written.

    The index is written as leading columns when it is named, as a table the models read
    with ``index_col="point_id"`` is, and left out when it is a default, unnamed one.  The
    rest is the house's CSV dialect: a header, ``\\n`` line ends, a blank for a missing
    value, ``True`` and ``False``, integers as integers, and floats from
    :func:`_float_texts`.
    """
    frame = df.reset_index() if any(n is not None for n in df.index.names) else df
    cells = frame.to_numpy(dtype=object)
    rows = [["" for _ in range(cells.shape[1])] for _ in range(cells.shape[0])]
    floats = []
    for i, j in itertools.product(range(cells.shape[0]), range(cells.shape[1])):
        v = cells[i, j]
        if v is None or v is pd.NA or v is pd.NaT:
            continue
        if _is_bool(v):
            rows[i][j] = "True" if v else "False"
        elif isinstance(v, numbers.Integral):
            rows[i][j] = str(int(v))
        elif isinstance(v, numbers.Real):
            if v == v:                          # a NaN stays blank
                floats.append((i, j))
        else:
            rows[i][j] = str(v)
    for (i, j), text in zip(floats, _float_texts([cells[i, j] for i, j in floats])):
        rows[i][j] = text
    buf = io.StringIO()
    writer = csv.writer(buf, lineterminator="\n")
    writer.writerow([str(c) for c in frame.columns])
    writer.writerows(rows)
    return buf.getvalue()


def _write_csv(df, path):
    """Write ``df`` as :func:`_csv_text` renders it, byte for byte on every platform."""
    pathlib.Path(path).write_bytes(_csv_text(df).encode("utf-8"))


# ---------------------------------------------------------------------------
# T2 and T3 -- the splice harness


def temp_inputs(tmp_dir, model_dir, *, model_points=None,
                model_point_file="model_point_table.csv", edits=None):
    """Copy a model and its inputs into ``tmp_dir``, with changes; return the model folder.

    The uslib layout puts a model's inputs beside it, as CSVs in the model folder's parent,
    and ``Data.input_dir()`` resolves to wherever the model was read from.  So a model read
    from a temporary folder reads that folder's CSVs, and a test can project against
    changed inputs without touching the tree.  The splice (T2) needs exactly that: extra
    model points opened with S's state at ``d``, and valuation-clock inputs shifted by
    ``d`` (:func:`shift_months`).

    The model folder is copied without ``__pycache__``, and every CSV in its parent
    directory beside it, byte for byte.  Then:

    ``model_points``
        a DataFrame written over ``model_point_file`` (which may be new: an SEC test can
        write an SEC table that is not committed yet).  Index it by ``point_id``, as the
        models' readers do, or give ``point_id`` as a column on a default index; a named
        index is written as columns, a default one is left out.
    ``edits``
        ``{filename: DataFrame}`` written over that file, or ``{filename: callable}``,
        which receives the file as ``pd.read_csv(path)`` reads it, a plain table on a
        default index, and returns the table to write.  An edit must name a file the copy
        holds, so a misspelt name raises instead of writing a file no model reads.  Edits
        apply after ``model_points``.

    What is written comes back as the models read it.  The writer chooses float texts that
    pandas' default parser reads as the same double wherever that parser can produce it,
    and within two ulps where it cannot, which for a computed count just below 1 is about
    one value in six (module docstring).  It writes integers, bools, blanks and strings as
    plain text, which reads back as itself.  The one exception is a string pandas takes for
    a missing value, such as ``NA`` or the empty string, which it takes for one in any CSV.
    A file that is not written is a byte copy.

    Returns the copied model folder, ready for ``mx.read_model``.  modelx keeps models in
    one registry, so read it under a name of its own, and close it.
    """
    tmp_dir, model_dir = pathlib.Path(tmp_dir), pathlib.Path(model_dir)
    tmp_dir.mkdir(parents=True, exist_ok=True)
    dest = tmp_dir / model_dir.name
    shutil.copytree(model_dir, dest, ignore=shutil.ignore_patterns("__pycache__"),
                    dirs_exist_ok=True)
    for csv_path in sorted(model_dir.parent.glob("*.csv")):
        if csv_path.is_file():
            shutil.copy2(csv_path, tmp_dir / csv_path.name)
    if model_points is not None:
        _write_csv(model_points, tmp_dir / model_point_file)
    for name, edit in (edits or {}).items():
        path = tmp_dir / name
        if not path.is_file():
            raise FileNotFoundError(
                f"edits names {name!r}, but the copy of {model_dir.parent} holds no such "
                f"file")
        frame = edit(pd.read_csv(path)) if callable(edit) else edit
        if not isinstance(frame, pd.DataFrame):
            raise TypeError(f"the edit for {name!r} produced a "
                            f"{type(frame).__name__}, not a DataFrame")
        _write_csv(frame, path)
    return dest


def shift_months(df, month_col, d, *, by=(), step=True):
    """Re-base a month-keyed table for a point whose SEC ``t = 0`` is S month ``d``.

    S reads such a table at its own month ``m``; the SEC point reads it at ``t = m - d``.
    So rows at months ``m >= d`` move to ``m - d``.  What happens to the rows before ``d``
    depends on how the model reads the table, and there are two readings.

    ``step=True``, a step function
        The row in force at ``t`` is the last one at or before ``t``: a rate or return
        scenario declared from a month on, a step-filled schedule.  Then the row in force at
        month ``d`` must survive the cut, or the re-based table holds nothing in force from
        month 0 up to its next row.  So where no row sits at exactly ``d``, the last rows
        before ``d`` become month 0.  "Rows", because several share that month when the
        table has another key not named in ``by``, and all of them were in force.  That
        holds only while those keys step on the same months: "a row at exactly ``d``" is
        asked of the whole group, so a scenario with a row at ``d`` would cost another
        scenario, which has none there, its row in force.  A key that steps on months of
        its own is named in ``by``.
    ``step=False``, exact months
        A row applies in its own month only: a transaction schedule, a premium or a
        withdrawal at month ``m``.  Rows before ``d`` have already happened, and their
        effect is in the opening state, not the table, so they are dropped.

    ``by`` names grouping columns, such as a scenario id or a subaccount, whose rows are
    re-based separately, each with its own row in force.  The month column must be a
    column, not the index; rows keep their order and their index labels.

    A negative ``d`` re-bases for a future point issued ``-d`` months after the valuation
    date (T3): every row moves later by ``-d``, and months ``0 .. -d - 1`` are left without
    a row.  They are the point's pre-issue months, which no formula may read (D4), so a read
    there fails loudly rather than finding a value invented for it.
    """
    by = [by] if isinstance(by, str) else list(by)
    months = df[month_col]
    if months.isna().any():
        raise ValueError(f"{month_col!r} has a blank month; a month-keyed table cannot "
                         f"be re-based around one")
    m = months.to_numpy()
    keep = m >= d
    new = m - d
    if step:
        groups = (df.groupby(by, sort=False, dropna=False).indices.values() if by
                  else [np.arange(len(df))])
        for positions in groups:
            mine = m[positions]
            if (mine == d).any():
                continue
            before = positions[mine < d]
            if len(before):
                carried = before[m[before] == m[before].max()]
                keep[carried] = True
                new[carried] = 0
    out = df.iloc[np.flatnonzero(keep)].copy()
    out[month_col] = new[keep]
    return out


# ---------------------------------------------------------------------------
# T6 -- the generated SEC inputs


# The columns the generator writes, and only the generator: neither an S table nor a spec's
# state may supply them.  ``duration_mth`` is the twin's, from ``duration_of``, moved on by
# ``d - source_mth`` for a derived row and set to ``-k`` for a future one.  ``provenance``
# is S's on a twin and composed from S's keys on the other rows (D8), so no extractor may
# write one either: that is the text ``CLAUDE.md`` holds to citing by key.
GENERATED_COLUMNS = ("row_kind", "source_policy_id", "source_mth")
_RESERVED = frozenset({"point_id", "policy_id", "duration_mth", "provenance",
                       *GENERATED_COLUMNS})


def _issued_at_valuation(row):
    """The default ``duration_of``: the S row is new business, issued at ``t = 0``."""
    return 0


@dataclasses.dataclass(frozen=True)
class SecSpec:
    """How one product's SEC model point table and its companions derive from S (D6, D8).

    The SEC table has three kinds of row, all generated, none typed (D8), and each row says
    which it is in ``row_kind``:

    ``"twin"``
        every S row, under its own ``point_id`` and ``policy_id``.  A new-business twin is
        what T1 compares; the twin of an S row already in force is a splice case.
    ``"derived"``
        an S row restated in force at S month ``d``, opened with S's own state there.  T2
        projects it against S from ``d`` on.
    ``"future"``
        an S new-business row issued ``k`` months after the valuation date (D4), T3's case.

    Every row carries ``policy_count``, ``duration_mth`` (months in force at ``t = 0``,
    negative for future new business), ``row_kind``, ``source_policy_id`` (the S policy it
    comes from) and ``source_mth``, where SEC ``t`` is S ``t + source_mth``.

    Fields:

    ``twin``
        the S model's name, as registered in ``us_registry.MODELS``.
    ``column_map``
        S column to SEC column, merged over the default ``{"pols_if_init":
        "policy_count"}`` (D5).  ``None`` drops a column whose meaning an SEC column takes
        over, such as ``Term_US_S``'s ``duration_inforce``, a count of years that
        ``duration_mth`` replaces (D6).  ``point_id`` and ``policy_id`` are never renamed.
    ``duration_of``
        S row (a Series, S column names, named by its ``point_id``) to its twin's
        ``duration_mth``: ``12 * row["duration_inforce"]`` on WholeLife,
        ``row["duration_mth"]`` on UL.  The default says every S row is new business.
    ``derived``
        ``(S point_id, d)`` pairs, in the order the rows are written.
    ``future``
        ``(S point_id, k)`` pairs; each S point must be new business.
    ``state``
        SEC column to ``callable(s_proj, d)``, the opening-state extractors of D6, for the
        derived rows.  Each returns the value S carries into month ``d``, before any
        month-``d`` event.  ``policy_count`` may be among them: its default,
        ``s_proj.pols_if(d)``, is the wrong count for SPIA, whose ``pols_if`` is a closing
        measure (D5).  The columns the generator owns may not: the two ids,
        ``duration_mth``, ``provenance`` and the three it adds, ``row_kind``,
        ``source_policy_id`` and ``source_mth``.
    ``twin_state``
        SEC column to ``callable(s_proj, d)`` for the twin rows, called with ``d`` the
        twin's ``source_mth``: the opening state S itself assumes, so the twin reproduces S.
        UL is the use: S restarts ``cum_prem`` at 0 on its in-force point 3, so that
        point's twin opens with ``cum_prem_init = 0``.  A future row copies its twin's
        values.  A state column with no ``twin_state`` entry is blank on the twins.  And a
        ``twin_state`` column with no ``state`` entry is copied to the derived rows from
        their twin, which is right only for a quantity fixed at issue (a locked rate, a
        solved premium: D6); anything that moves after issue needs a ``state`` entry.
    ``exempt``
        extra cells T1 skips, beyond :data:`TWIN_EXEMPT_DEFAULT`, each for a stated reason,
        an S cell the SEC model drops or renames among them.
    ``companions``
        companion filename to ``callable(s_model, table)``, which builds that file from the
        S model and the finished SEC table (a copy, free to modify): DIA's premium schedule,
        VA's re-based scenario (D8).
    ``model_point_file``
        the SEC table's own filename.

    Every file the spec writes ends ``_sec.csv``, which is checked here.  The SEC model
    shares its directory with the S model's inputs, and the suffix is what guarantees the
    generator can never write over one of them (D8: "never into the shared S inputs").
    And no companion may take the table's own name, which would silently replace the
    table with the companion.
    """
    twin: str
    column_map: Mapping[str, str | None] = dataclasses.field(default_factory=dict)
    duration_of: Callable[[pd.Series], int] = _issued_at_valuation
    derived: tuple[tuple[int, int], ...] = ()
    future: tuple[tuple[int, int], ...] = ()
    state: Mapping[str, Callable] = dataclasses.field(default_factory=dict)
    twin_state: Mapping[str, Callable] = dataclasses.field(default_factory=dict)
    exempt: frozenset[str] = frozenset()
    companions: Mapping[str, Callable] = dataclasses.field(default_factory=dict)
    model_point_file: str = "model_point_table_sec.csv"

    def __post_init__(self):
        for filename in (self.model_point_file, *self.companions):
            if not str(filename).endswith("_sec.csv"):
                raise ValueError(
                    f"{filename!r}: a generated SEC input is named *_sec.csv, so that it "
                    f"can never overwrite an S input in the same directory")
        if self.model_point_file in self.companions:
            raise ValueError(
                f"{self.model_point_file!r} is both the SEC table and a companion; the "
                f"companion would replace the table")
        for field_name, extractors, reserved in (
                ("state", self.state, _RESERVED),
                ("twin_state", self.twin_state, _RESERVED | {"policy_count"})):
            clash = sorted(set(extractors) & reserved)
            if clash:
                raise ValueError(
                    f"{field_name} may not set {clash}: the generator owns them")
        object.__setattr__(self, "derived",
                           tuple((int(p), int(d)) for p, d in self.derived))
        object.__setattr__(self, "future",
                           tuple((int(p), int(k)) for p, k in self.future))
        object.__setattr__(self, "exempt", frozenset(self.exempt))


def _wl_entering(name, opening):
    """What ``WholeLife_US_S`` carries into month ``d`` in cells ``name``.

    The closing value of month ``d - 1``, or, where month ``d`` opens S's frame, the
    opening value S's own formulas read there: ``pua_face(t - 1) if t > proj_start() else
    puaf_inforce()``, and the same for the loan and the accumulation balance.
    """
    def extract(s, d):
        return getattr(s, name)(d - 1) if d > s.proj_start() else opening(s)
    return extract


def _wl_at_prev_anniv(name, opening):
    """``WholeLife_US_S``'s cells ``name`` at the anniversary on or before month ``d``.

    The close of S's month ``anniv_mth(d) - 12``, the month whose end opened the policy year
    containing ``d``, or S's opening value where that month is before S's frame: S's own
    ``x(t - 12) if t - 12 >= proj_start() else <opening>``, read at the year's anniversary.
    """
    def extract(s, d):
        m = s.anniv_mth(d) - 12
        return getattr(s, name)(m) if m >= s.proj_start() else opening(s)
    return extract


# WholeLife_US_SEC's opening state (D6): what WholeLife_US_S carries into month d, each read
# as S's own formulas read it.  The paid-up additions, the loan and the accumulation balance
# entering the month; the additions and the loan at the anniversary that opened its policy
# year, which the year's dividend, OYT gap and loan interest read; the dividend credited
# there, S's div_prev_anniv(d); and the gross premiums since issue, which S's prem_cum sums
# from issue whatever its frame.  S's accumulation balance opens its frame at 0.
_WL_STATE = {
    "pua_face_init": _wl_entering("pua_face", lambda s: s.puaf_inforce()),
    "loan_bal_init": _wl_entering("loan_bal", lambda s: s.loan_inforce()),
    "pua_face_prev_anniv_init": _wl_at_prev_anniv("pua_face", lambda s: s.puaf_inforce()),
    "loan_bal_prev_anniv_init": _wl_at_prev_anniv("loan_bal", lambda s: s.loan_inforce()),
    "div_accum_init": _wl_entering("div_accum", lambda s: 0.0),
    "div_prev_anniv_init": lambda s, d: s.div_prev_anniv(d),
    "prem_cum_init": lambda s, d: s.prem_cum(d - 1) if d > 0 else 0.0,
}


# SEC model name -> its SecSpec.  Phase 1 registers each product's spec here as its SEC
# model lands, Term first (§5.3).  The conventions suite reads ``exempt`` from it for T1,
# the product module's T6 calls :func:`check_generated` with the name, and
# ``tools/gen_sec_points.py`` writes the files from it.
SEC_SPECS: dict[str, SecSpec] = {
    # Term's only state is the count, which the default extractor reads (s_proj.pols_if(d)),
    # so the spec names rows and nothing else.  The derived rows are an anniversary in the
    # level period, the middle of the first ART year and the last covered month; the
    # future row is issued off a valuation anniversary.  T2's splice grid is built from
    # this spec in a temporary table, not committed.  T1, and T3 on the future rows, hold
    # on Term only while each S point counts one policy, as both do: SEC charges
    # acquisition per policy issued, S once per model point (§7.1), so on a row issued at
    # or after the valuation date from a point of any other count, expenses and net_cf
    # differ in the issue month by design, and no exemption can take that out without
    # taking those cells.
    "Term_US_SEC": SecSpec(
        twin="Term_US_S",
        column_map={"duration_inforce": None},
        derived=((2, 12), (1, 126), (1, 719)),
        future=((1, 3),),
    ),
    # WholeLife's state is seven columns (_WL_STATE above).  S's own columns are renamed in
    # place, puaf_inforce and loan_inforce to pua_face_init and loan_bal_init, and
    # duration_inforce, S's elapsed policy years, is dropped for duration_mth, 108 on S's
    # in-force point 1.  On the twins the five columns S has no column for take what S
    # itself assumes, so each twin reproduces S: on point 1 the paid-up additions at the
    # anniversary are its 4,100, the loan 0, the accumulation balance and last year's
    # dividend 0, S's "before the frame", and the premiums since issue S's prem_cum(107).
    # The derived rows are the two S points that do not reproduce from S's own in-force
    # state (§7.2), REDUCE_PREM and ACCUM, on the anniversary that opens policy year 10;
    # the funded term blend mid-year before its crossover and the loan variant mid-year,
    # whose anniversary values differ from their current ones; the graded final-expense
    # point inside its graded years; and REDUCE_PREM in the last covered month.  The future
    # row is issued off a valuation anniversary.  T2's splice grid is built from this spec
    # in a temporary table, not committed.
    #
    # T1 holds on WholeLife at any count: S already weights its acquisition by the count
    # issued, as SEC charges it.  It skips five S cells besides the default three:
    #   puaf_inforce, loan_inforce: renamed pua_face_init and loan_bal_init, one name for
    #     each opening-state column (D6, §7.2).  Every cell that read them reads the
    #     renamed cells, which T1 compares, and both are 0 on S's new business.
    #   proj_start: S's first projected month on the policy clock, 108 on S's point 1.
    #     Every SEC frame opens at t = 0 (D3), which the conventions assert.
    #   duration_inforce: S's elapsed policy years, which duration_mth replaces (D6).
    #   result_pols: SEC's gains pols_new_biz, the count D5 puts there, so the frame has a
    #     column S's lacks and cannot agree as a whole.  Each column it shares with S is a
    #     cell T1 compares at every month, and test_whole_life_us_sec.py compares the
    #     report itself with S's, on every column both hold.
    "WholeLife_US_SEC": SecSpec(
        twin="WholeLife_US_S",
        column_map={"duration_inforce": None, "puaf_inforce": "pua_face_init",
                    "loan_inforce": "loan_bal_init"},
        duration_of=lambda row: 12 * int(row["duration_inforce"]),
        derived=((5, 108), (4, 108), (8, 78), (6, 114), (12, 18), (5, 659)),
        future=((2, 3),),
        state=_WL_STATE,
        twin_state={c: f for c, f in _WL_STATE.items()
                    if c not in ("pua_face_init", "loan_bal_init")},
        exempt=frozenset({"puaf_inforce", "loan_inforce", "proj_start",
                          "duration_inforce", "result_pols"}),
    ),
}


def _derived_policy_id(policy_id, d):
    return f"{policy_id}-M{d}"


def _future_policy_id(policy_id, k):
    return f"{policy_id}-F{k}"


def _derived_provenance(point_id, policy_id, d):
    return f"S point {point_id} ({policy_id}) restated in force at S month {d}"


def _future_provenance(point_id, policy_id, k):
    months = "month" if k == 1 else "months"
    return f"S point {point_id} ({policy_id}) issued {k} {months} after the valuation date"


def _sec_columns(spec, s_table, rename):
    """The SEC table's columns, in order.

    S's columns in S's order, renamed or dropped by ``rename``; then ``policy_count`` and
    ``duration_mth``, each where S has no column of that name; then the state columns S
    lacks, in the order the spec names them; then the generator's own columns; and
    ``provenance`` last, where the S table has one, as every table in the library keeps it.
    """
    columns = [rename.get(c, c) for c in ["point_id", *s_table.columns]]
    columns = [c for c in columns if c is not None]
    provenance = "provenance" in columns
    if provenance:
        columns.remove("provenance")
    for c in ("policy_count", "duration_mth", *spec.twin_state, *spec.state):
        if c not in columns:
            columns.append(c)
    for c in GENERATED_COLUMNS:
        if c in columns:
            raise ValueError(f"{spec.twin}'s table has a {c!r} column, which the generator "
                             f"writes itself")
        columns.append(c)
    if provenance:
        columns.append("provenance")
    if len(set(columns)) != len(columns):
        dupes = sorted({c for c in columns if columns.count(c) > 1})
        raise ValueError(f"column_map gives two columns one name: {dupes}")
    return columns


def build_sec_table(spec, s_model):
    """Build the SEC model point table and its companions from the S model as it stands.

    ``s_model`` is the S model, read from the product directory whose files are wanted; its
    ``Data.model_point_table()`` is the S table, and its ``Projection`` supplies the
    counts and the opening state.

    The rows, in order (see :class:`SecSpec` for the kinds):

    twins
        every S row, with the same ``point_id`` and ``policy_id``, renamed by
        ``column_map``.  ``policy_count`` is the S count; ``duration_mth`` comes from
        ``duration_of``; ``source_mth`` is the first row of the S point's own
        ``result_cf()``: 0 when S projects it from the valuation date, its entry month (108
        for WholeLife point 1) when S keeps the policy clock.  Any other first row means
        ``duration_of`` is wrong, and raises here, before a misaligned twin can reach T1.
    derived rows, for each ``(p, d)``
        the twin of S point ``p``, opened at S month ``d``: ``policy_count`` is
        ``pols_if(d)``, the count S carries into month ``d``; ``duration_mth`` is the twin's
        moved on by ``d - source_mth``, which is ``d`` on new business; ``source_mth`` is
        ``d``; and then ``state`` sets the opening state.  ``d`` must fall inside S's frame,
        after the twin's own entry month.
    future rows, for each ``(p, k)``
        the twin of new-business point ``p``, issued ``k`` months after the valuation
        date: ``duration_mth`` and ``source_mth`` are ``-k``, and the count is S's.

    Derived and future rows take fresh ``point_id`` s after the largest S one, in the
    spec's order, so the numbering is fixed by the spec, never by a dict or a filesystem.
    Their ``policy_id`` is composed from S's and the month (``TL-000001-M120``,
    ``TL-000001-F3``), and where the S table has a ``provenance`` column theirs is composed
    the same way, citing S's point and policy and the month.  Every other text cell is
    copied from S.  That is D8's rule under ``CLAUDE.md``: the generator adds no name, and
    a reworded S cell reaches the SEC table through T6.

    Returns ``(table, companions)``: the table on a default index, ``point_id`` its first
    column, exactly as the file is written; and ``{filename: DataFrame}`` from the spec's
    companion builders.

    Every S point's ``result_cf()`` is projected, to find its first row.  Pass a model whose
    points are already swept, the instance T1 swept, and that costs nothing.
    """
    s_table = s_model.Data.model_point_table()
    if s_table.index.name != "point_id" or "policy_id" not in s_table.columns:
        raise ValueError(f"{spec.twin}: the S table is not indexed by point_id with a "
                         f"policy_id column")
    ids = [int(i) for i in s_table.index]
    if len(set(ids)) != len(ids):
        raise ValueError(f"{spec.twin}: the S table repeats a point_id")
    rename = {"pols_if_init": "policy_count", **spec.column_map}
    unknown = [c for c in rename if c not in s_table.columns]
    if unknown:
        raise ValueError(f"column_map names {unknown}, which {spec.twin}'s table lacks")
    if "point_id" in rename or "policy_id" in rename:
        raise ValueError("point_id and policy_id carry over unchanged")
    if "policy_count" not in rename.values():
        raise ValueError("no S column becomes policy_count")
    columns = _sec_columns(spec, s_table, rename)
    projs = {pid: s_model.Projection[pid] for pid in ids}
    provenance = "provenance" in columns

    twins = {}
    for record in s_table.reset_index().to_dict("records"):
        pid = int(record["point_id"])
        duration = int(spec.duration_of(s_table.loc[pid]))
        source = int(projs[pid].result_cf().index[0])
        if duration < 0:
            raise ValueError(f"{spec.twin} point {pid}: duration_of gives {duration}; an S "
                             f"row is in force or new business, never future business")
        if source not in (0, duration):
            raise ValueError(
                f"{spec.twin} point {pid}: S opens its frame at t = {source}, which is "
                f"neither the valuation date (0) nor its duration_mth ({duration}); "
                f"duration_of does not describe this row")
        row = {rename.get(c, c): v for c, v in record.items()
               if rename.get(c, c) is not None}
        row["point_id"] = pid
        row["duration_mth"] = duration
        for column, extract in spec.twin_state.items():
            row[column] = extract(projs[pid], source)
        row.update(row_kind="twin", source_policy_id=record["policy_id"],
                   source_mth=source)
        twins[pid] = row

    def twin_of(p, kind):
        if p not in twins:
            raise ValueError(f"a {kind} row names point {p}, which {spec.twin}'s table "
                             f"lacks")
        return twins[p]

    rows = list(twins.values())
    fresh = itertools.count(max(ids) + 1)
    for p, d in spec.derived:
        twin = twin_of(p, "derived")
        proj, source = projs[p], twin["source_mth"]
        if not source < d < proj.proj_len():
            raise ValueError(
                f"derived row ({p}, {d}): d must fall after the twin's entry month "
                f"({source}) and inside S's frame, which ends at {proj.proj_len() - 1}")
        row = dict(twin, point_id=next(fresh),
                   policy_id=_derived_policy_id(twin["policy_id"], d),
                   policy_count=proj.pols_if(d),
                   duration_mth=twin["duration_mth"] + d - source)
        if provenance:
            row["provenance"] = _derived_provenance(p, twin["policy_id"], d)
        for column, extract in spec.state.items():
            row[column] = extract(proj, d)
        row.update(row_kind="derived", source_policy_id=twin["policy_id"], source_mth=d)
        rows.append(row)
    for p, k in spec.future:
        twin = twin_of(p, "future")
        if twin["duration_mth"] != 0 or twin["source_mth"] != 0:
            raise ValueError(f"future row ({p}, {k}): point {p} is in force in S, and only "
                             f"new business can be written later")
        if k < 1:
            raise ValueError(f"future row ({p}, {k}): k counts months after the valuation "
                             f"date, so it is at least 1")
        row = dict(twin, point_id=next(fresh),
                   policy_id=_future_policy_id(twin["policy_id"], k), duration_mth=-k)
        if provenance:
            row["provenance"] = _future_provenance(p, twin["policy_id"], k)
        row.update(row_kind="future", source_policy_id=twin["policy_id"], source_mth=-k)
        rows.append(row)

    table = pd.DataFrame(rows, columns=columns)
    for key in ("point_id", "policy_id"):
        dupes = sorted(table.loc[table[key].duplicated(), key].astype(str))
        if dupes:
            raise ValueError(f"the SEC table repeats {key} {dupes}; is a (point, month) "
                             f"pair listed twice?")
    companions = {}
    for filename, build in spec.companions.items():
        frame = build(s_model, table.copy())
        if not isinstance(frame, pd.DataFrame):
            raise TypeError(f"the builder of {filename} returned a "
                            f"{type(frame).__name__}, not a DataFrame")
        companions[filename] = frame
    return table, companions


_read_names = itertools.count(1)


def _spec(spec_name):
    try:
        return SEC_SPECS[spec_name]
    except KeyError:
        known = ", ".join(sorted(SEC_SPECS)) or "none yet"
        raise KeyError(f"no SecSpec is registered for {spec_name!r} "
                       f"(registered: {known})") from None


def _generated_texts(spec_name, product_dir, s_model):
    """Build one spec's files and render them: ``(product_dir, {filename: text})``."""
    spec = _spec(spec_name)
    if product_dir is None:
        if spec.twin not in MODELS:
            raise ValueError(f"{spec.twin} is not a registered model, so its product "
                             f"directory is unknown; pass product_dir")
        product_dir = model_path(spec.twin).parent
    product_dir = pathlib.Path(product_dir)
    own = s_model is None
    if own:
        s_model = mx.read_model(product_dir / spec.twin,
                                name=f"{spec.twin}_secgen_{next(_read_names)}")
    try:
        table, companions = build_sec_table(spec, s_model)
    finally:
        if own:
            s_model.close()
    texts = {spec.model_point_file: _csv_text(table)}
    texts.update({name: _csv_text(frame) for name, frame in companions.items()})
    return product_dir, texts


def write_generated(spec_name, product_dir=None, *, s_model=None):
    """Write one SEC model's generated input files from its S model as it stands.

    ``spec_name`` is the SEC model's name in :data:`SEC_SPECS`.  ``product_dir`` is the
    product directory the S model and its inputs are read from, and the files written to,
    by default the S model's own in the registry.  ``s_model`` may pass an S model already
    read from that directory, and swept, to save reading and projecting it again; one read
    here is read under a name of its own and closed.

    The writing is deterministic, so a rewrite with no S change is a no-op: a file that
    :func:`check_generated` finds current is not touched, its bytes and its modification
    time left alone.  That includes a file whose floats are spelled otherwise but agree in
    value, as a file written on another platform may (module docstring), so regenerating
    on a second platform does not churn the committed files.

    Returns ``{path: changed}`` for every file the spec generates.
    """
    product_dir, texts = _generated_texts(spec_name, product_dir, s_model)
    changed = {}
    for name, text in texts.items():
        path = product_dir / name
        changed[path] = bool(_file_drift(name, path, text))
        if changed[path]:
            path.write_bytes(text.encode("utf-8"))
    return changed


# T6 reads a float cell by its value, to these tolerances, not by its spelling (module
# docstring).  Far tighter than the 1e-9 of every comparison above, so nothing T2 could see
# passes here; far looser than the last-bit differences between platforms' parsers and
# libms, so none of those fails here.
_DRIFT_RTOL = 1e-12
_DRIFT_ATOL = 1e-12

# A float as the writer spells one: with a decimal point or an exponent, so that ``1`` and
# ``1.0``, which pandas reads into columns of different dtypes, stay different cells.
_FLOAT_TEXT = re.compile(r"[+-]?(?:\d+\.\d*|\.\d+|\d+(?=[eE]))(?:[eE][+-]?\d+)?")


def _same_cell(committed, generated):
    """Whether a committed cell says what the generated one says.

    The same text, or two float spellings whose values agree to ``_DRIFT_RTOL`` and
    ``_DRIFT_ATOL``.  ``None`` stands for a cell a committed row is missing, and matches
    nothing.
    """
    if committed == generated:
        return True
    if committed is None or generated is None:
        return False
    if _FLOAT_TEXT.fullmatch(committed) and _FLOAT_TEXT.fullmatch(generated):
        return _close(float(committed), float(generated), _DRIFT_RTOL, _DRIFT_ATOL)
    return False


def _rows_text(rows):
    """The CSV text of parsed rows, in the dialect :func:`_csv_text` writes."""
    buf = io.StringIO()
    csv.writer(buf, lineterminator="\n").writerows(rows)
    return buf.getvalue()


def _file_drift(name, path, generated):
    """:func:`_csv_drift` against the committed file at ``path``, which may be missing."""
    if not path.is_file():
        return [f"{name}: generated, but not committed"]
    try:
        committed = path.read_bytes().decode("utf-8")
    except UnicodeDecodeError:
        return [f"{name}: the committed file is not UTF-8; regenerate it"]
    return _csv_drift(name, committed, generated)


def _csv_drift(name, committed, generated):
    """The cell-by-cell differences between a committed CSV text and the generated one.

    Cells compare by :func:`_same_cell`: as text, but a float by its value.  So two files
    that differ only in how their floats are spelled have no drift.  A file whose cells
    agree but whose text is not what the writer writes (other quoting, CRLF line ends, no
    final newline) is reported, so that it is rewritten.
    """
    if committed == generated:
        return []
    old = list(csv.reader(io.StringIO(committed)))
    new = list(csv.reader(io.StringIO(generated)))
    old_head, old_rows = (old[0], old[1:]) if old else ([], [])
    new_head, new_rows = (new[0], new[1:]) if new else ([], [])
    lines = []
    added = [c for c in new_head if c not in old_head]
    removed = [c for c in old_head if c not in new_head]
    if added:
        lines.append(f"{name}: columns the generator now writes: {added}")
    if removed:
        lines.append(f"{name}: columns the generator no longer writes: {removed}")
    if not added and not removed and old_head != new_head:
        lines.append(f"{name}: the columns are in a different order")
    key = new_head[0] if new_head else "row"

    def ident(row):
        return f"{key} {row[0]}" if row else "a blank line"

    for i in range(max(len(old_rows), len(new_rows))):
        if i >= len(old_rows):
            lines.append(f"{name}: row {i + 1} ({ident(new_rows[i])}) is generated but "
                         f"not committed")
            continue
        if i >= len(new_rows):
            lines.append(f"{name}: committed row {i + 1} ({ident(old_rows[i])}) is no "
                         f"longer generated")
            continue
        if len(old_rows[i]) > len(old_head):
            lines.append(f"{name}: committed row {i + 1} ({ident(old_rows[i])}) has cells "
                         f"beyond its header: {old_rows[i][len(old_head):]}")
        # zip_longest, not zip: a committed row cut short must show its missing cells as
        # missing (None), not drop them from the comparison.
        was = dict(itertools.zip_longest(old_head, old_rows[i]))
        now = dict(itertools.zip_longest(new_head, new_rows[i]))
        for c in new_head:
            if c in old_head and not _same_cell(was.get(c), now.get(c)):
                lines.append(f"{name}: row {i + 1} ({ident(new_rows[i])}), {c}: "
                             f"committed {was.get(c)!r}, generated {now.get(c)!r}")
    if not lines and _rows_text(old) != committed:
        lines.append(f"{name}: the cells agree, but the text differs (quoting or line "
                     f"ends); regenerate it")
    return lines


def check_generated(spec_name, product_dir=None, *, s_model=None):
    """T6: where the committed generated files differ from what S now generates.

    Builds the files as :func:`write_generated` would and compares each with the committed
    one, cell by cell: ``"model_point_table_sec.csv: row 3 (point_id 3), policy_id:
    committed 'TL-000001-M12', generated 'TL-900001-M12'"``.  A cell compares as text,
    except that a float compares by value, to 1e-12 relative or absolute.  The spelling
    the writer picks, and the last bits of a computed value, can differ from one platform
    or pandas to another (module docstring), and a file committed from one must check
    clean on the rest.  ``1`` against ``1.0`` is still drift, since it changes the column's
    dtype.  A file whose cells agree but whose text is not the writer's (quoting, line
    ends) is reported, and so is a missing file.

    So an edit to an S row that an SEC file copies or derives from, such as a reworded
    ``provenance`` cell or a renamed lookup key, fails T6 until the files are regenerated,
    in the same commit (§5.2).  The fix is ``python tools/gen_sec_points.py <name>``, or
    :func:`write_generated` where ``tools/`` is absent, as in a ``lifelib.create()`` copy.

    Takes the same arguments as :func:`write_generated`, and returns the drift lines, empty
    when the committed files are current.
    """
    product_dir, texts = _generated_texts(spec_name, product_dir, s_model)
    lines = []
    for name, text in texts.items():
        lines += _file_drift(name, product_dir / name, text)
    return lines
