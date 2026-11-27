"""Support for the SEC models' tests: the twin and splice comparisons, and the generator.

UKLIB-SEC-PLAN.md puts a ``<Name>_UK_SEC`` model beside each ``<Name>_UK_S``, as
USLIB-SEC-PLAN.md put a ``<Name>_US_SEC`` beside each uslib ``<Name>_US_S`` (its D1): the S
model taught to run in force at a valuation date, and then to compile.  The S model is not
touched.  It stays the reference, and this module is how the SEC suites lean on it rather
than restate it: every S worked example, its intermediate cells included, becomes an SEC
assertion through a comparison instead of through a second copy of the golden.

This is uslib's harness, ``uslib/tests/sec_support.py``, under a name of this library's
own, so that the two libraries' suites can run in one process (UKLIB-SEC-PLAN.md U3).  It
differs from uslib's in three spellings, ``uk_registry``, ``UKLIB_`` and ``_uk_sec``, in
this paragraph, in the few sentences of prose those spellings make uklib's, which name
uklib's jobs and modules where uslib's name its own, ``cython_uk`` and
``test_compiled_conventions_uk.py`` among them, and in its product specs, which are uklib's;
``tools/check_sec_harness.py`` holds everything else to uslib's, function by function.
The docstrings keep uslib's examples and cite USLIB-SEC-PLAN.md, whose design
UKLIB-SEC-PLAN.md adopts by reference: they are the record of why each function is as it
is.

What is here, by the plan's tests (its §5.2):

T1, the twin identity
    :func:`sweep` evaluates on an S model point what the conventions suite's sweep
    evaluates and every other ``result_*`` report, and :func:`twin_mismatches` then
    compares every cell of the S model, at every argument tuple the S cell cached inside
    its frame, less :data:`TWIN_EXEMPT_DEFAULT`; an S cell the SEC model lacks is a
    mismatch.  At stage ``"EC"``, and at stage ``"E"`` for a code a product brings
    forward, as ``FIA_US_SEC`` does its phases, :func:`codes` turns S's timing and phase
    strings into the SEC model's int References for the comparison.
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
C2, the Phase 1 fingerprint
    :func:`fingerprint` takes, in brief, what an SEC model computes on every point,
    :func:`fingerprint_text` writes it out as the literal a product module freezes, and
    :func:`fingerprint_mismatches` holds a later version of the model to it (§5.4).
Compiling, for Phase 2's compile tests
    :func:`require_cython` skips a compile test, or fails it in the ``cython_uk`` job,
    where :func:`cython_missing` finds the toolchain missing; :class:`SecBuilds` compiles
    each SEC model once a session, into a temporary directory; :func:`compiled_case` puts
    a build beside a copy of its inputs; and :func:`run_compiled` runs calls on it in a
    child process, on a stack of a given size.  :func:`cython_shards` and
    :func:`cython_shard` split the compile tests among the ``cython_uk`` job's legs.
C3, C4 and C5, and the release
    :func:`reporting_cells` is R17's allowlist, the cells that may stay Python, and
    :func:`data_readers` the ``Data`` cells that read a file, which stay Python too.
    :func:`typing_faults`, :func:`spec_faults` and :func:`c_faults` read a build's
    declarations, its caches against the spec, and its generated C (C3);
    :func:`compiled_mismatches` holds the compiled model to modelx, cell by cell, after a
    :func:`full_sweep` of every point, bit for bit where :func:`exact_here` (C4);
    :func:`static_faults` reads the formulas, and needs no compiler (C5); and
    :func:`release_faults` runs a product's ``run_sec.py --block`` on a compiled block and
    counts the ItemSpaces it keeps (F5).  :func:`object_return_faults` holds the reporting
    cells of :func:`object_cells` to ``object`` in a build's declarations (C3);
    :func:`sample_engine_faults` reads a ``sample_sec.py`` for a call of every engine
    cell; and :func:`block_sum_faults` holds a runner's running sum, :func:`runner_add`,
    to ``groupby``'s, bit for bit.

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

from uk_registry import MODELS, model_path


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


def codes(proj):
    """The codes an SEC ``Projection`` names, ``{name: int}``: timings, kinds, categories.

    At stage ``"EC"`` an SEC model spells what its S twin spells as text as an int
    Reference named as the text it replaces (USLIB-SEC-PLAN.md R9, R10): a timing,
    ``pols_if_at(t, BEF_DECR)``, and a phase, ``LEVEL``, or a categorical column decoded,
    ``WholeLife_US_SEC``'s premium period, ``TO_100``.  Those are its References whose
    names are all capitals and whose values are ints, bools excepted, and they are what
    this returns.  Passed to :func:`twin_mismatches` as ``codes``, they turn S's strings
    into SEC's ints, in the arguments S cached and in the values S returned.  At stage
    ``"E"`` there are none unless a product brings a code forward, as ``FIA_US_SEC`` does
    its phases (``PRE_ISSUE`` to ``MATURED``, M8); for an S model there are none, and it
    returns ``{}``.

    So every other Reference an SEC model holds is named in lower case, however constant:
    an all-capital int Reference is read as a code.
    """
    return {name: value for name, value in proj.refs.items()
            if name.isupper() and isinstance(value, int) and not isinstance(value, bool)}


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


def _twin_lines(s_proj, sec_proj, exempt, arg_map, t_offset, rtol, atol, codes=None):
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
            sec_args = tuple(codes.get(a, a) if codes and isinstance(a, str) else a
                             for a in sec_args)
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
            if (codes and isinstance(expected, str) and expected in codes
                    and _is_month(actual)):
                code = codes[expected]          # S's label against SEC's code (R10)
                for line in _value_diffs(code, actual, rtol, atol, t_offset):
                    yield f"{label}: S {expected!r} is code {code}; {line}"
                continue
            for line in _value_diffs(expected, actual, rtol, atol, t_offset):
                yield f"{label}: {line}"


def twin_mismatches(s_proj, sec_proj, *, exempt=TWIN_EXEMPT_DEFAULT, arg_map=None,
                    t_offset=0, rtol=1e-9, atol=1e-9, limit=50, codes=None):
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
    arguments for S's (the default is the identity); returning ``None`` skips that key.
    Then, with ``codes``, :func:`codes` of the SEC Space, each string argument that names
    a code is passed as that code: S's ``pols_if_at(t, "BEF_DECR")`` is SEC's
    ``pols_if_at(t, BEF_DECR)`` (R9).  And a string S returned that names a code is
    compared with SEC's value as that code, where SEC returned an int: S's ``"LEVEL"``
    against SEC's ``LEVEL`` (R10).  A string SEC still returns, such as a label accessor's
    ``"M"``, is compared as a string.  Then the argument named ``t``, if the SEC cells has
    one, moves to SEC's clock: SEC month ``t`` is S month ``t + t_offset``, as in
    :func:`frame_mismatches`, so the SEC cells is called at S's ``t - t_offset``, and a
    row passes its ``source_mth`` (``d`` for a row derived from S month ``d``; see the
    module docstring).  A key whose SEC ``t`` falls below 0 is
    skipped: no month precedes the valuation date, and R1 forbids evaluating one.  Under an
    offset a ``t``-indexed Series or DataFrame, such as ``result_cf()``, is relabelled the
    same way before it is compared.  Only the
    parameter named ``t`` moves.  Another that holds a month, such as the creation month
    ``m`` of ``IUL_US_S``'s ``seg_bal_pp(t, m)``, which ``IUL_US_SEC`` keys by slot,
    moves through ``arg_map``.

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
    for line in _twin_lines(s_proj, sec_proj, exempt, arg_map, t_offset, rtol, atol,
                            codes):
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
# write one either: that is the text ``CLAUDE.md`` holds to citing by key.  The three of
# GENERATED_COLUMNS are on every table, and SOURCE_REFS on a table whose spec has
# ``derived_refs`` alone (generated_columns).
GENERATED_COLUMNS = ("row_kind", "source_policy_id", "source_mth")
SOURCE_REFS = "source_refs"
_RESERVED = frozenset({"point_id", "policy_id", "duration_mth", "provenance",
                       *GENERATED_COLUMNS, SOURCE_REFS})


def _issued_at_valuation(row):
    """The default ``duration_of``: the S row is new business, issued at ``t = 0``."""
    return 0


def _reference_settings(refs):
    """``refs``, ``{reference: value}``, as a row of ``derived_refs`` is described: each
    name and its value, ``review_prem_shock 0.1, ci_trend 0.02``, in the spec's order."""
    return ", ".join(f"{name} {_py(value)!r}" for name, value in refs.items())


def generated_columns(spec):
    """The columns the generator writes to ``spec``'s table, in the order it writes them:
    :data:`GENERATED_COLUMNS`, then :data:`SOURCE_REFS` where the spec has
    ``derived_refs``.

    ``source_refs`` records, on each row read from S under References of its own, each
    Reference and its value, in the spec's order and as :func:`_reference_settings`
    describes them, ``review_prem_shock 0.1``; it is blank on every other row.  So such a
    row does not read in its table as a restatement at the shipped References.  No model
    reads it, and an in-force extract needs it no more than the other three.  A spec
    without ``derived_refs`` has no such row, and its table no such column.
    """
    return GENERATED_COLUMNS + ((SOURCE_REFS,) if spec.derived_refs else ())


@dataclasses.dataclass(frozen=True)
class SecSpec:
    """How one product's SEC model point table and its companions derive from S (D6, D8).

    The SEC table has three kinds of row, all generated, none typed (D8), and each row says
    which it is in ``row_kind``:

    ``"twin"``
        every S row, under its own ``point_id`` and ``policy_id``.  A new-business twin is
        what T1 compares; the twin of an S row already in force is a splice case.
    ``"derived"``
        an S row restated in force at S month ``d``, opened with S's own state there, from
        S as it ships or, for a row of ``derived_refs``, from S run under References of the
        row's own.  T2 projects it against S from ``d`` on.
    ``"future"``
        an S new-business row issued ``k`` months after the valuation date (D4), T3's case.

    Every row carries ``policy_count``, ``duration_mth`` (months in force at ``t = 0``,
    negative for future new business), ``row_kind``, ``source_policy_id`` (the S policy it
    comes from) and ``source_mth``, where SEC ``t`` is S ``t + source_mth``; and the table
    of a spec with ``derived_refs`` carries ``source_refs`` too, the References a row was
    read under, blank where they are S's own (:func:`generated_columns`).

    Fields:

    ``twin``
        the S model's name, as registered in ``uk_registry.MODELS``.
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
    ``derived_refs``
        ``{(S point_id, d): {reference: value}}``, more derived rows, written after every
        other row in the spec's order, each restated from S run under References of its
        own: for a history S reaches only under another assumption, such as a review
        change that has moved premiums where S ships it at 0.  Each row is the one
        ``derived`` would make of its pair had S shipped those References, which are set on
        S's ``Projection`` while the row is read and restored after it.  Its
        ``source_refs``, a column the table of such a spec alone carries, names each
        Reference and its value, and so does its ``provenance``, where the S table has
        one.  A pair may not be one of ``derived``'s, whose row would take its
        ``policy_id``; and a name must be one of the References of S's ``Projection``.
        Each companion's rows for such a row are built under the row's References too,
        from the row alone (:func:`build_sec_table`), so that a companion holds the state
        of the run its row was read from; its builder must then be row-local, writing rows
        keyed by the ``point_id`` of the rows it is given and no others, which
        :func:`build_sec_table` checks.  Empty by default.
    ``future``
        ``(S point_id, k)`` pairs; each S point must be new business.
    ``state``
        SEC column to ``callable(s_proj, d)``, the opening-state extractors of D6, for the
        derived rows.  Each returns the value S carries into month ``d``, before any
        month-``d`` event.  ``policy_count`` may be among them: its default,
        ``s_proj.pols_if(d)``, is the wrong count for SPIA, whose ``pols_if`` is a closing
        measure (D5).  The columns the generator owns may not: the two ids,
        ``duration_mth``, ``provenance`` and the four it adds, ``row_kind``,
        ``source_policy_id``, ``source_mth`` and ``source_refs``.
    ``twin_state``
        SEC column to ``callable(s_proj, d)`` for the twin rows, called with ``d`` the
        twin's ``source_mth``: the opening state S itself assumes, so the twin reproduces S.
        UL is the use: S restarts ``cum_prem`` at 0 on its in-force point 3, so that
        point's twin opens with ``cum_prem_init = 0``.  A future row copies its twin's
        values, but for those ``future_state`` sets.  A state column with no
        ``twin_state`` entry is blank on the twins.  And a
        ``twin_state`` column with no ``state`` entry is copied to the derived rows from
        their twin, which is right only for a quantity fixed at issue (a locked rate, a
        solved premium: D6); anything that moves after issue needs a ``state`` entry.
    ``exempt``
        extra cells T1 skips, beyond :data:`TWIN_EXEMPT_DEFAULT`, each for a stated reason,
        an S cell the SEC model drops or renames among them.
    ``twin_arg_map``
        ``callable(name, args)``, or ``None``: the ``arg_map`` T1 passes to
        :func:`twin_mismatches`, for an SEC cell that takes S's arguments otherwise than
        by :func:`codes`, which maps S's strings alone.  At stage ``"EC"``: S's ``None``
        for a total, where SEC's cell takes a code for it, ``claims(t, None)`` as
        ``claims(t, "ALL")``, which ``codes`` then maps (R12); or S's ``(t, m)`` keys
        re-keyed by slot, ``(t, t - m)`` (R15).  ``None``, the default, leaves S's
        arguments as they are.
    ``future_state``
        SEC column to ``callable(s_proj, k)`` for the future rows: S point ``p``'s
        projection and the months ``k`` after the valuation date the row is issued.  A
        future row copies its twin's values, but for these.  FIA is the use: a future
        row's scenario is a copy of S's moved ``k`` months later, ``{id}-F{k}``, which its
        twin's id cannot name.  A column S lacks, and neither ``state`` nor
        ``twin_state`` sets, is blank on the twins and the derived rows.  It may not set
        ``policy_count``, or any column the generator owns.
    ``model_state``
        ``callable(s_model)``, or ``None``: more state columns, whose names the S model's
        inputs give, as SEC column to ``callable(s_proj, d)``.  It is called as the table
        is built, with the S model the generator reads, and each column it gives is set
        on the twins at their ``source_mth`` and on the derived rows at ``d``, as
        ``twin_state`` and ``state`` set theirs, a future row copying its twin's.  Its
        columns come before ``twin_state``'s.  VA is the use: a subaccount value for each
        subaccount S's fund table holds, so that a fund table given a subaccount gives
        the table its column.  It may not set ``policy_count``, a column the generator
        owns, or one ``state`` or ``twin_state`` sets, which is checked as it is called.
    ``companions``
        companion filename to ``callable(s_model, table)``, which builds that file from the
        S model and the finished SEC table (a copy, free to modify): DIA's premium schedule,
        FIA's rate scenarios and RILA's market scenarios re-based to each row, and VA's
        two re-based scenarios (D8).
    ``model_point_file``
        the SEC table's own filename.
    ``c4_also``
        ``callable(proj)``, or ``None``: what C4 compares of a point beyond its full sweep,
        the ``also`` :func:`compiled_mismatches` takes, which the conventions' C4 on the
        committed points passes it (:func:`spec_c4_also`).  The sweep reaches a cell of a
        code only at the codes some swept cell asks of it, so a product whose sweep leaves
        a code unasked, such as a count at the end of the month that no formula reads,
        calls it here, at every month of the frame and the month after it; and its module
        passes the same to its own comparisons.  It is called on a modelx point whose
        ``proj_len()`` has not raised, and must not raise.  ``None``, the default, adds
        nothing.

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
    twin_arg_map: Callable | None = None
    future_state: Mapping[str, Callable] = dataclasses.field(default_factory=dict)
    model_state: Callable | None = None
    derived_refs: Mapping[tuple[int, int], Mapping[str, object]] = dataclasses.field(
        default_factory=dict)
    c4_also: Callable | None = None

    def __post_init__(self):
        if self.c4_also is not None and not callable(self.c4_also):
            raise TypeError(f"c4_also is {self.c4_also!r}: C4's also is a callable of one "
                            f"point, or None")
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
                ("twin_state", self.twin_state, _RESERVED | {"policy_count"}),
                ("future_state", self.future_state, _RESERVED | {"policy_count"})):
            clash = sorted(set(extractors) & reserved)
            if clash:
                raise ValueError(
                    f"{field_name} may not set {clash}: the generator owns them")
        object.__setattr__(self, "derived",
                           tuple((int(p), int(d)) for p, d in self.derived))
        object.__setattr__(self, "future",
                           tuple((int(p), int(k)) for p, k in self.future))
        object.__setattr__(self, "exempt", frozenset(self.exempt))
        object.__setattr__(self, "derived_refs", {
            (int(p), int(d)): dict(refs) for (p, d), refs in self.derived_refs.items()})
        for (p, d), refs in self.derived_refs.items():
            if not refs:
                raise ValueError(f"derived_refs row ({p}, {d}) sets no Reference: a row "
                                 f"read from S at its own References is a derived row")
            if (p, d) in self.derived:
                raise ValueError(
                    f"derived_refs row ({p}, {d}), under {_reference_settings(refs)}, "
                    f"repeats derived row ({p}, {d}), read from S at its own References: "
                    f"the two would take one policy_id")


# >>> product specs: this library's own.  tools/check_sec_harness.py compares the rest.
#
# Each uklib SEC model's SecSpec, and the opening-state extractors it names, are entered
# here with the model's Phase 1 step (UKLIB-SEC-PLAN.md §7).  Everything outside this block
# is uslib's harness, held to uslib/tests/sec_support.py by tools/check_sec_harness.py
# (UKLIB-SEC-PLAN.md U3).


def _term_ledger_per_policy(s, d):
    """``Term_UK_S``'s FIB ledger entering month ``d``, per policy in force then.

    S's ``fib_cum(d)``, the deaths since its frame opened, over its count in force,
    ``pols_if(d)``: per policy, so that the count is the one weight on every flow.  Where
    no policy is in force, as once a capped mortality has taken every life, there is no
    policy to carry it, and the column is 0: such a point projects nothing.
    """
    count = s.pols_if(d)
    return s.fib_cum(d) / count if count > 0 else 0.0


def _term_streams_per_policy(s, d):
    """``Term_UK_S``'s FIB streams in payment entering month ``d``, per policy in force.

    S pays ``(1 - c)`` of every death's stream at the take-up ``c`` it holds throughout, so
    its streams in payment at the start of month ``d`` are ``(1 - c) fib_cum(d)``: over
    ``pols_if(d)``, as the ledger is.  0 off the family income benefit, which pays no
    instalments, and where no policy is in force.
    """
    count = s.pols_if(d)
    if s.shape() != "fib" or count <= 0:
        return 0.0
    return (1.0 - s.fib_commute_rate()) * s.fib_cum(d) / count


def _term_commission_paid(s, d):
    """The initial commission ``Term_UK_S`` paid at issue, per policy, on a row in force
    at ``d``: S's ``comm_init_pp()``, an event of the issue month, so 0 at ``d = 0``."""
    return s.comm_init_pp() if d > 0 else 0.0


def _term_no_indexed_twin_in_force(s, d):
    """Refuse the twin of an indexed ``Term_UK_S`` point S opens in force, at month ``d``.

    S opens an in-force frame on an anniversary only, ``proj_start()``, at index factors of
    1, and takes its first step at the next anniversary.  ``Term_UK_SEC`` takes an
    anniversary at the valuation date as month 0's own step (D6, precised at uslib's M7),
    from the factors before it, which ``Data`` holds to 1 or more: the twin would be one
    step above S in every month of its frame, its cover and premium ``1 + the increase``
    times S's, 154,500 for S's 150,000 on an indexed point 8 at ``t = 0``, and so it is not
    written.  S's own point 8 is not indexed.  A row restated from such a point at a later
    month is S's, its factors read in the month before.
    """
    if d > 0 and s.indexation():
        raise ValueError(
            f"Term_UK_S point {s.point_id}: S opens it in force at month {d}, an "
            f"anniversary, indexed, at factors of 1 and with no step there, where "
            f"Term_UK_SEC makes an anniversary at the valuation date month 0's own step "
            f"(D6): no opening factor of 1 or more gives S's numbers, so no twin is "
            f"written")


def _term_cover_factor(s, d):
    """``Term_UK_S``'s cover indexation factor entering month ``d``, before its own step.

    The opening state is measured before any month-``d`` event, and an anniversary's RPI
    increase is one, the restated row's month 0's, made at the References of its valuation
    date (D6, precised at uslib's M7).  So it is S's ``idx_factor(d - 1)``, the factor of
    the month before: mid-year that of the policy year under way, and on an anniversary
    that of the year it closes.  Where S's frame opens, at issue or at ``proj_start()`` on
    S's point 8, there is no month before it, and it is S's own opening factor,
    ``idx_factor(d)``, 1, but on an indexed point S opens in force, whose twin no factor
    can make S's (:func:`_term_no_indexed_twin_in_force`).
    """
    if d > s.proj_start():
        return s.idx_factor(d - 1)
    _term_no_indexed_twin_in_force(s, d)
    return s.idx_factor(d)


def _term_premium_factor(s, d):
    """``Term_UK_S``'s premium indexation factor entering month ``d``, before its own step,
    at the instant :func:`_term_cover_factor` reads the cover factor: S's
    ``idx_prem_factor(d - 1)``, or where S's frame opens its own opening factor, refused
    as that one is."""
    if d > s.proj_start():
        return s.idx_prem_factor(d - 1)
    _term_no_indexed_twin_in_force(s, d)
    return s.idx_prem_factor(d)


# Term_UK_SEC's opening state (D6; UKLIB-SEC-PLAN.md §6.1): what Term_UK_S carries into
# month d, before any month-d event, each read as S's own formulas read it, each per policy
# in force or a ratio, so that policy_count is the one weight.  The selective-lapse ratio,
# S's lapse_cum(d), a share of the cohort S's frame opened with; the FIB ledger, the deaths
# since S's frame opened, per policy in force (_term_ledger_per_policy), and the streams of
# them in payment (_term_streams_per_policy); the two indexation factors entering month d,
# before its own anniversary's step, S's idx_factor(d - 1) and idx_prem_factor(d - 1)
# (_term_cover_factor, _term_premium_factor); the share of the policies in force whose
# premium is waived, S's wop_waived_frac(d); and the initial commission paid at issue,
# which the clawback recovers (_term_commission_paid).  At a twin's source_mth these are
# what S itself assumes where its frame opens: 0 for the ratio, the ledger, the streams,
# the waived share and the commission, and 1 for the factors, on new business and on S's
# point 8, in force at 60, which S opens with nothing lapsed, no ledger and no waiver, but
# with its commission paid.  The deferred period goes in a companion, built by
# _term_pipeline.
_TERM_STATE = {
    "lapse_cum_init": lambda s, d: s.lapse_cum(d),
    "fib_cum_init": _term_ledger_per_policy,
    "fib_streams_init": _term_streams_per_policy,
    "idx_factor_init": _term_cover_factor,
    "idx_prem_factor_init": _term_premium_factor,
    "wop_waived_frac_init": lambda s, d: s.wop_waived_frac(d),
    "comm_init_pp_init": _term_commission_paid,
}

_TERM_PIPELINE = ("point_id", "lag", "wop_deferred_init")


def _term_pipeline(s_model, table):
    """``wop_pipeline_sec.csv``: each in-force waiver row's deferred period, month by month.

    For each row of the table in force, restated at S month ``d`` or the twin of a point S
    opens in force at ``d``, in the table's order, whose point has the waiver rider: one
    row for each of its last ``min(wop_defer_mths, duration_mth)`` policy months,
    ``duration_mth`` the row's own.  ``lag`` ``k`` is S's month ``m = d - k``, and
    ``wop_deferred_init`` the share still in the deferred period at the start of S's
    month ``d``, the valuation instant, from the incapacity of month ``m``: the incidence
    ``Term_UK_S``'s ``wop_waived_frac`` takes in, the deferred period later, on the lives
    active in month ``m``, ``inc_m act(m)``, S's ``wop_active_frac``, S's own product in
    S's order, after the ``k - 1`` months of recovery since, ``(1 - rec_m)^(k - 1)``.  0
    where ``m`` predates S's frame, which S assumes held no incapacity.  So the SEC row's
    entrants at ``t = wop_defer_mths + 1 - k``, the share times the ``t`` months of
    recovery still to run, are S's to rounding, and so is its active share at ``t = 0``,
    what the waived share and the pipeline leave, S's ``act(d)``.  A month earlier than the
    last ``wop_defer_mths`` has entered the waived share, ``wop_waived_frac_init``,
    already.  The future rows hold none, nor do the new-business twins.  ``point_id`` is
    the only key to a point.

    It reads only the S cells it needs, and releases nothing: the caller owns the S model,
    and one T6 passes in may be one it still compares against.
    """
    point_of = {pol: pid
                for pid, pol in s_model.Data.model_point_table()["policy_id"].items()}
    rows = []
    for row in table.to_dict("records"):
        if (row["row_kind"] not in ("derived", "twin") or int(row["duration_mth"]) <= 0
                or not bool(row["wop"])):
            continue
        s = s_model.Projection[point_of[row["source_policy_id"]]]
        d = int(row["source_mth"])
        for k in range(1, min(s.wop_defer_mths, int(row["duration_mth"])) + 1):
            m = d - k
            incidence = (s.wop_inc_rate_mth() * s.wop_active_frac(m)
                         if m >= s.proj_start() else 0.0)
            rows.append({"point_id": row["point_id"], "lag": k,
                         "wop_deferred_init":
                             incidence * (1.0 - s.wop_rec_rate_mth()) ** (k - 1)})
    return pd.DataFrame(rows, columns=list(_TERM_PIPELINE))


def _term_claims_total(name, args):
    """``Term_UK_S``'s ``claims`` keys as ``Term_UK_SEC`` takes them at stage ``"EC"`` (R9,
    R12).

    S's ``claims(t, kind=None)`` is cached under ``(t, None)`` where S asks for the total,
    which its ``net_cf`` does: SEC's code ``ALL``, so ``None`` is mapped to ``"ALL"``, which
    :func:`codes` then turns into the int, as it turns S's kinds and timings.  Every other
    key, and every other cell's arguments, pass as they are, SEC's own codes among them,
    where a comparison of two SEC models passes it SEC's keys.
    """
    if name == "claims" and len(args) == 2 and args[1] is None:
        return (args[0], "ALL")
    return args


def _ci_reviews_made(s, d):
    """The reviews ``CI_UK_S`` made before month ``d``: S's ``reviews_passed(d - 1)``, the
    reviews passed in the month before, or none at issue.  The opening state is measured
    before any month-``d`` event, and a review that falls in month ``d`` is one, the
    restated row's month 0's, made at the References of its valuation date (D6, precised
    at uslib's M7)."""
    return s.reviews_passed(d - 1) if d > 0 else 0


def _ci_review_factor(s, d):
    """The premium factor ``CI_UK_S``'s reviews before month ``d`` have given, which S has
    no cell for: ``(1 + review_prem_shock)`` to the power of the reviews made
    (:func:`_ci_reviews_made`), as S's ``premium_pp`` multiplies by it, and 1 before the
    first review or on a guaranteed point, which makes none.  On a review month, the
    factor of the period it closes."""
    return (1.0 + s.review_prem_shock) ** _ci_reviews_made(s, d)


def _ci_review_change(s, d):
    """The premium change ``CI_UK_S``'s last review before month ``d`` made: its one
    ``review_prem_shock``, once a review has been made (:func:`_ci_reviews_made`), and 0
    before the first, or on a guaranteed point.  On a review month, the change of the
    review before it, whose window has closed."""
    return float(s.review_prem_shock) if _ci_reviews_made(s, d) >= 1 else 0.0


def _ci_latched(s, d):
    """Whether ``CI_UK_S``'s select latch closed before month ``d``, 1 or 0, which S has no
    cell for: S's ``ci_sel_factor`` takes ``1 + sel_lapse_ci_loading`` on a reviewable
    point once a review has been made (:func:`_ci_reviews_made`) and
    ``review_prem_shock`` is past the threshold, and those are its branches here.  The
    factor alone cannot say it: at a loading of 0 a closed latch's factor is 1.  On a
    review month, the latch before that month's review, which closes it at the restated
    row's ``t = 0`` if it does."""
    return int(s.premium_guarantee() == "reviewable" and _ci_reviews_made(s, d) >= 1
               and s.review_prem_shock > s.review_lapse_threshold)


def _ci_cover_factor(s, d):
    """``CI_UK_S``'s cover indexation factor entering month ``d``, before its own step:
    S's ``idx_factor(d - 1)``, the factor of the month before, which on an anniversary is
    that of the policy year it closes, the step at ``d`` being the restated row's month
    0's (D6, precised at uslib's M7); at issue, S's ``idx_factor(0)``, 1."""
    return s.idx_factor(d - 1) if d > 0 else s.idx_factor(d)


def _ci_premium_factor(s, d):
    """``CI_UK_S``'s premium indexation factor entering month ``d``, before its own step,
    at the instant :func:`_ci_cover_factor` reads the cover factor."""
    return s.idx_prem_factor(d - 1) if d > 0 else s.idx_prem_factor(d)


def _ci_select_factor(s, d):
    """``CI_UK_S``'s select-latch factor entering month ``d``, before that month's review:
    S's ``ci_sel_factor(d - 1)``, or at issue S's ``ci_sel_factor(0)``, 1.  Read only where
    the latch closed before (:func:`_ci_latched`)."""
    return s.ci_sel_factor(d - 1) if d > 0 else s.ci_sel_factor(d)


def _ci_claims_total(name, args):
    """``CI_UK_S``'s ``claims`` keys as ``CI_UK_SEC`` takes them at stage ``"EC"`` (R9,
    R12).

    S's ``claims(t, kind=None)`` is cached under ``(t, None)`` where S asks for the total,
    which its ``net_cf`` does: SEC's code ``ALL``, so ``None`` is mapped to ``"ALL"``, which
    :func:`codes` then turns into the int, as it turns S's kinds and timings.  Every other
    key, and every other cell's arguments, pass as they are, SEC's own codes among them,
    where a comparison of two SEC models passes it SEC's keys.
    """
    if name == "claims" and len(args) == 2 and args[1] is None:
        return (args[0], "ALL")
    return args


# CI_UK_SEC's opening state (D6; UKLIB-SEC-PLAN.md §6.2): the facts of the contract
# CI_UK_S recomputes from flat References, each read as S's own formulas read it, each a
# factor, a rate or a flag, so that policy_count is the one weight, and each before any
# month-d event: an anniversary or a review that falls in month d is the restated row's
# month 0's, made at the References of its valuation date (D6, precised at uslib's M7).
# The two indexation factors entering month d, S's idx_factor(d - 1) and
# idx_prem_factor(d - 1) (_ci_cover_factor, _ci_premium_factor); the premium factor the
# reviews before month d have given (_ci_review_factor); the select latch, whether it
# closed before month d (_ci_latched) and its factor, S's ci_sel_factor(d - 1)
# (_ci_select_factor); and the premium change the last review before month d made
# (_ci_review_change), which the SEC model reads while that review's shock window runs.
# At a twin's source_mth, 0 on every S point, these are the issue values: 1 for the four
# factors, and 0 for the latch and the change.
_CI_STATE = {
    "idx_factor_init": _ci_cover_factor,
    "idx_prem_factor_init": _ci_premium_factor,
    "review_prem_factor_init": _ci_review_factor,
    "ci_sel_latched_init": _ci_latched,
    "ci_sel_factor_init": _ci_select_factor,
    "review_prem_shock_init": _ci_review_change,
}


def _ulb_withdrawn(s, d):
    """``ULB_UK_S``'s withdrawals and adviser charges entering month ``d``, per policy.

    S's ``wd_cum_pp(d - 1)``, the running total to the end of the month before, which
    ``wd_cum_pp(d)`` carries on and ``gmdb_guarantee_pp(d)`` reads: the total entering
    month ``d``, before its cancellations.  0 at issue, where S's total starts.
    """
    return s.wd_cum_pp(d - 1) if d > 0 else 0.0


def _ulb_allowed(s, d):
    """``ULB_UK_S``'s 5% allowance accrued entering month ``d``, per policy.

    S's ``allowance_cum_pp(d - 1)``: the allowable element of every policy year to the one
    month ``d - 1`` falls in, each accrued at its start.  The opening state is measured
    before any month-0 event (D6, precised at M7), and a policy year's accrual at its start
    is one: mid-year it is the year under way, and on an anniversary the year before it,
    the new year accruing in the restated row's month 0, at the References of its valuation
    date.  0 at issue, where the first year's accrual is month 0's own.
    """
    return s.allowance_cum_pp(d - 1) if d > 0 else 0.0


# ULB_UK_SEC's opening state (D6; UKLIB-SEC-PLAN.md §6.6): what ULB_UK_S carries into month
# d, each per policy, so that policy_count is the one weight.  The unit fund at the start of
# month d, S's av_pp(d), the column S calls uf_init, renamed; the withdrawals and adviser
# charges since issue, S's wd_cum_pp(d - 1) (_ulb_withdrawn), which open the GMDB; and the
# allowance accrued entering month d, S's allowance_cum_pp(d - 1) (_ulb_allowed), which
# the excess gain is measured against.  At a twin's source_mth, 0 on every S point, these are what S itself
# assumes at issue: the fund at outset, S's uf_init, nothing withdrawn and nothing accrued.
_ULB_STATE = {
    "av_pp_init": lambda s, d: s.av_pp(d),
    "wd_cum_pp_init": _ulb_withdrawn,
    "allowance_cum_pp_init": _ulb_allowed,
}


def _ulb_claims_total(name, args):
    """``ULB_UK_S``'s ``claims`` keys as ``ULB_UK_SEC`` takes them at stage ``"EC"`` (R9,
    R12).

    S's ``claims(t, kind=None)`` is cached under ``(t, None)`` where S asks for the total,
    which its ``check_unit_funding_resid`` does: SEC's code ``ALL``, so ``None`` is mapped to
    ``"ALL"``, which :func:`codes` then turns into the int, as it turns S's kinds and
    timings.  Every other key, and every other cell's arguments, pass as they are, SEC's
    own codes among them, where a comparison of two SEC models passes it SEC's keys.
    """
    if name == "claims" and len(args) == 2 and args[1] is None:
        return (args[0], "ALL")
    return args


def _wol_claims_total(name, args):
    """``WOL_UK_S``'s ``claims`` keys as ``WOL_UK_SEC`` takes them at stage ``"EC"`` (R9,
    R12).

    S's ``claims(t, kind=None)`` is cached under ``(t, None)`` where S asks for the total,
    which its ``net_cf`` does: SEC's code ``ALL``, so ``None`` is mapped to ``"ALL"``,
    which :func:`codes` then turns into the int, as it turns S's kinds, benefits and
    timings.  Every other key, and every other cell's arguments, pass as they are, SEC's
    own codes among them, where a comparison of two SEC models passes it SEC's keys.
    """
    if name == "claims" and len(args) == 2 and args[1] is None:
        return (args[0], "ALL")
    return args


def _wol_paid_up_cover(s, d):
    """``WOL_UK_S``'s paid-up cover entering month ``d``, per paid-up policy.

    S's ``pu_benefit(d)``, the summed paid-up cash sums, over its paid-up count,
    ``pols_pu(d)``: per policy, so that the counts are the only weights.  Where no paid-up
    policy is in force, as on a point without the variant, before the first conversion or
    once a capped mortality has taken every life, there is no policy to carry it, and the
    column is 0.
    """
    count = s.pols_pu(d)
    return s.pu_benefit(d) / count if count > 0 else 0.0


def _wol_premiums_paid(s, d):
    """``WOL_UK_S``'s premiums paid per policy entering month ``d``.

    S's ``prem_cum_pp(d - 1)``, the running total to the end of the month before, which
    ``prem_cum_pp(d)`` carries on: the total entering month ``d``, before its premium.  0
    at issue, where S's total starts.
    """
    return s.prem_cum_pp(d - 1) if d > 0 else 0.0


def _wol_cover(s, d):
    """``WOL_UK_S``'s cover before month ``d``'s events: that of month ``d - 1``.

    The opening state is measured at the start of month 0, before any month-0 event, so on
    a point valued on an anniversary the cover is the year the anniversary closes, and its
    increase is the in-force model's first event (USLIB-SEC-PLAN.md D6, as precised at
    uslib's M7).  Off an anniversary it is month ``d``'s cover; at issue, S's at 0.
    """
    return s.cover_pp(d - 1 if d > 0 else 0)


def _wol_premium(s, d):
    """``WOL_UK_S``'s monthly premium before month ``d``'s events: that of month ``d - 1``.

    S's ``premium_pp(d - 1)`` while premiums were payable then, at the same instant as the
    cover (:func:`_wol_cover`), and once they have ceased, the last one paid, S's
    ``premium_pp`` of the last premium-paying month.  At issue, S's ``premium_pp(0)``.
    """
    if d <= 0:
        return s.premium_pp(0)
    cessation = s.cessation_mths()
    return s.premium_pp(min(d, cessation) - 1 if cessation > 0 else d - 1)


def _wol_crossover(s, d):
    """``WOL_UK_S``'s crossover, a policy month, where it fell before month ``d``; else -1.

    S's ``crossover_mth()``, searched from issue at S's References: history once it falls
    before the month the row is valued at, which the in-force model reports and never
    searches for again; -1 where it falls in month ``d`` or later, the projection's, or
    never, which the in-force model searches for forward from ``d``.  -1 on a twin.
    """
    month = s.crossover_mth()
    return month if 0 <= month < d else -1


# WOL_UK_SEC's opening state (D6; UKLIB-SEC-PLAN.md §6.4): what WOL_UK_S carries into month
# d, each per policy or a count, so that policy_count and the paid-up count are the only
# weights.  The paid-up strand, S's pols_pu(d) and its cover per paid-up policy
# (_wol_paid_up_cover); the premiums paid to the end of month d - 1 (_wol_premiums_paid);
# the cover and premium before month d's events, S's of month d - 1 (_wol_cover,
# _wol_premium), the history of increases S rebuilds from issue at today's rpi_rate,
# esc_fixed_cover and esc_take_up, an anniversary at month d being the in-force model's
# first event, at today's References; and the crossover, where it fell before month d
# (_wol_crossover), which S searches for again from issue.  At a twin's source_mth, 0 on
# every S point, these are what S itself assumes at issue: no paid-up policy, nothing
# paid, the sum assured and the premium at issue, and no crossover.
_WOL_STATE = {
    "pols_pu_init": lambda s, d: s.pols_pu(d),
    "pu_benefit_pp_init": _wol_paid_up_cover,
    "prem_cum_pp_init": _wol_premiums_paid,
    "cover_pp_init": _wol_cover,
    "premium_pp_init": _wol_premium,
    "crossover_mth_init": _wol_crossover,
}


def _pa_rpi_linked(s):
    """Whether ``PA_UK_S``'s point ``s`` escalates with the RPI: ``lpi5`` or
    ``rpi_catchup``."""
    return s.escalation_type() in ("lpi5", "rpi_catchup")


def _pa_year(d):
    """The policy year under way at the start of S's month ``d``, before any month-``d``
    event: the year of month ``d - 1``, and 1 at the start date.  On an anniversary, the
    year the anniversary closes, whose escalation is the restated row's month-0 event."""
    return max(d - 1, 0) // 12 + 1


def _pa_income(s, d):
    """``PA_UK_S``'s income of the policy year under way entering month ``d``, on RPI-linked
    escalation: ``annual_income`` of :func:`_pa_year`, before any month-``d`` anniversary.
    Blank, NaN, on level and fixed escalation, whose schedule the SEC model re-derives."""
    return s.annual_income(_pa_year(d)) if _pa_rpi_linked(s) else math.nan


def _pa_peak(s, d):
    """``PA_UK_S``'s ratchet peak over the latest index entering month ``d``, on
    ``rpi_catchup``: ``rpi_peak(a0) / rpi_index(a0)``, ``a0`` the anniversary that opened
    the year under way, so 1 while the index has never fallen.  Blank elsewhere."""
    if s.escalation_type() != "rpi_catchup":
        return math.nan
    a0 = _pa_year(d) - 1
    return s.rpi_peak(a0) / s.rpi_index(a0)


def _pa_paid(s, d):
    """``PA_UK_S``'s as-if-alive annuitant instalments by time ``d``, ``cum_annuity_pp(d,
    "ANNUITANT")``, where the SEC model reads them: on RPI-linked escalation with value
    protection on the first death.  Blank elsewhere, where the SEC model sums the
    schedule."""
    if not (_pa_rpi_linked(s) and s.vp_pct() > 0.0 and s.vp_basis() == "first_death"):
        return math.nan
    return s.cum_annuity_pp(d, "ANNUITANT")


# PA_UK_SEC's opening state (D6; UKLIB-SEC-PLAN.md §6.7): what PA_UK_S carries into month d,
# each per contract, so that policy_count is the one weight.  Each life's survival to time d,
# before month d's deaths; the payments made by time d on every stream, S's
# cum_annuity_pp(d, "ALL"); and on RPI-linked escalation the history no flat rpi_rate
# re-derives: the income of the policy year under way before any month-d anniversary
# (_pa_income), the ratchet's peak over the latest index (_pa_peak), and where value
# protection is on the first death the annuitant's as-if-alive instalments by time d
# (_pa_paid).  The count is S's pols_if_init, the contracts the point stands for, and not
# S's pols_if, which is a closing measure (D5): mortality decrements each life, never the
# count.  At a twin's source_mth, 0 on every S point, these are the start date's values:
# each covered life 1, life 2 at 0 on a single-life contract, nothing paid, the first
# year's income and a peak of 1.
_PA_STATE = {
    "policy_count": lambda s, d: s.pols_if_init(),
    "lives_if_init_1": lambda s, d: s.lives_if(d, 1),
    "lives_if_init_2": lambda s, d: s.lives_if(d, 2),
    "cum_annuity_all_init": lambda s, d: s.cum_annuity_pp(d, "ALL"),
    "annual_income_init": _pa_income,
    "rpi_peak_init": _pa_peak,
    "cum_annuity_pp_init": _pa_paid,
}


def _pa_claims_total(name, args):
    """``PA_UK_S``'s ``claims`` keys as ``PA_UK_SEC`` takes them at stage ``"EC"`` (R9,
    R12).

    S's ``claims(t, kind=None)`` is cached under ``(t, None)`` where S asks for the total,
    which its ``liability_cf`` does: SEC's code ``ALL``, so ``None`` is mapped to
    ``"ALL"``, which :func:`codes` then turns into the int, as it turns S's kinds and
    timings, ``cum_annuity_pp``'s ``"ANNUITANT"`` and ``"ALL"`` among them.  Every other
    key, and every other cell's arguments, pass as they are, SEC's own codes among them,
    where a comparison of two SEC models passes it SEC's keys.
    """
    if name == "claims" and len(args) == 2 and args[1] is None:
        return (args[0], "ALL")
    return args


def _ip_twin_years(point_id, status, z0, escalation):
    """n: the whole policy years the twin of ``IP_UK_S``'s point has run at the valuation
    date.

    0 on an ``active`` cell, which S issues at the valuation date.  An ``in_claim`` cell S
    opens at the valuation date with its claim in payment, cohort ``z0 + 1``, and its
    policy clock restarted there, so its twin is issued ``n`` whole years before it, the
    least that holds the claim: cohort ``z0 + 1`` incepted at the end of the month
    ``z0 + 1`` months before the valuation date, a month the policy was in force, so
    ``12n >= z0 + 1``, ``n = ceil((z0 + 1) / 12)`` (UKLIB-SEC-PLAN.md §6.3, §9 item 11).
    On whole years the twin's anniversaries are S's, a year apart, and its attained ages
    S's.  But its valuation month is then an anniversary, whose escalation is the
    projection's first event (D6), where S takes no step at the month its frame opens: so
    an ``in_claim`` cell with RPI escalation has no twin, and this refuses it, naming the
    point, rather than write a twin the splice would fail.  No shipped S point is one.
    """
    if status != "in_claim":
        return 0
    if escalation == "RPI":
        raise ValueError(
            f"IP_UK_S point {point_id} is in claim with RPI escalation: S takes no "
            f"escalation at its month 0, where it restarts its policy clock, and the twin, "
            f"valued on an anniversary, would take one there, so IP_UK_SEC has no twin of it")
    return -(-(int(z0) + 1) // 12)


def _ip_duration(row):
    """The twin's ``duration_mth``: ``12n``, :func:`_ip_twin_years` of the S row, 0 on an
    ``active`` cell."""
    return 12 * _ip_twin_years(row.name, row["status"], row["claim_duration_months"],
                               row["escalation"])


def _ip_issue_age(s, d):
    """The twin's ``entry_age``: S's less :func:`_ip_twin_years`, the age the twin was
    issued at, so that its attained age at the valuation date is S's ``entry_age``, which
    ``IP_UK_S`` reads as that on an ``in_claim`` cell."""
    return s.age_at_entry() - _ip_twin_years(s.point_id, s.status(),
                                             s.claim_duration_months(), s.escalation())


def _ip_healthy_share(s, d):
    """``IP_UK_S``'s healthy share of the count at the start of month ``d``: S's
    ``pols_active(d)`` over its ``pols_if(d)``, the recoveries of month ``d - 1`` already back
    in health, before any month-``d`` event.  At a twin's ``source_mth``, 0, it is what S
    assumes where its frame opens: 1 on an ``active`` cell and 0 on an ``in_claim`` one.
    Where S's count is 0, as on a claim on the exit basis whose every life has recovered,
    the row is a point of no policies, all healthy, as one without claim cohorts is, its
    share 1: it carries nothing, as S does."""
    count = s.pols_if(d)
    return s.pols_active(d) / count if count != 0.0 else 1.0


def _ip_benefit(s, d):
    """``IP_UK_S``'s monthly benefit entering month ``d``: S's ``benefit_pp(d - 1)``.

    The opening state is measured before any month-``d`` event, so on a point valued on an
    anniversary the benefit is the year the anniversary closes, and its escalation is the
    in-force model's first event (USLIB-SEC-PLAN.md D6, as precised at uslib's M7).  At a
    twin's ``source_mth``, 0, it is S's ``benefit_pp(0)``, what S pays where its frame
    opens: the benefit at issue, and on an ``in_claim`` cell the benefit in payment.
    """
    return s.benefit_pp(d - 1 if d > 0 else 0)


def _ip_premium(s, d):
    """``IP_UK_S``'s monthly premium entering month ``d``: S's ``premium_pp(d - 1)``, at the
    instant :func:`_ip_benefit` reads the benefit, and S's ``premium_pp(0)`` on a twin."""
    return s.premium_pp(d - 1 if d > 0 else 0)


# IP_UK_SEC's opening state (D6; UKLIB-SEC-PLAN.md §6.3): what IP_UK_S carries into month d,
# each a share of the count or an amount per policy, so that policy_count is the one weight.
# The healthy share (_ip_healthy_share); the monthly benefit and premium before month d's
# events, S's of month d - 1 (_ip_benefit, _ip_premium), the history of escalations S
# rebuilds from issue at today's rpi_rate, an anniversary at month d being the in-force
# model's first event, at today's References; and the claim cohorts, in a companion built by
# _ip_cohorts.  On a twin, the entry age less the whole years it has run (_ip_issue_age).
_IP_STATE = {
    "pols_active_init": _ip_healthy_share,
    "benefit_pp_init": _ip_benefit,
    "premium_pp_init": _ip_premium,
}
_IP_TWIN_STATE = {"entry_age": _ip_issue_age, **_IP_STATE}

_IP_COHORTS = ("point_id", "z", "pols_sick_dur_init")


def _ip_cohorts(s_model, table):
    """``inforce_cohorts_sec.csv``: each in-force row's claim cohorts, claim duration by
    claim duration.

    For each row of the table in force, restated at S month ``d`` or the twin of an
    ``in_claim`` cell, in the table's order: one row for each claim duration ``z`` at
    which ``IP_UK_S``'s ``sick_cohorts(d)`` holds lives, its share of S's ``pols_if(d)``,
    the count the row carries, at the start of S's month ``d``, the valuation instant,
    before any month-``d`` event: cohort 1 holding the claims that incepted at the end of
    month ``d - 1``, not yet paid, and cohort ``z`` those that incepted at the end of
    month ``d - z``.  So the SEC row's cohorts at ``t = 0``, the count times each share,
    are S's to rounding.  A claim duration S holds no lives at is no row: the file is
    sparse.  The future rows hold none, nor do the twins issued at the valuation date,
    which open healthy, nor a row of no policies, all healthy (:func:`_ip_healthy_share`).
    ``point_id`` is the only key to a point.

    It reads only the S cells it needs, and releases nothing: the caller owns the S model,
    and one T6 passes in may be one it still compares against.
    """
    point_of = {pol: pid
                for pid, pol in s_model.Data.model_point_table()["policy_id"].items()}
    rows = []
    for row in table.to_dict("records"):
        if int(row["duration_mth"]) <= 0:
            continue
        s = s_model.Projection[point_of[row["source_policy_id"]]]
        d = int(row["source_mth"])
        count = s.pols_if(d)
        if count == 0.0:
            continue
        for z, held in enumerate(s.sick_cohorts(d), start=1):
            if held != 0.0:
                rows.append({"point_id": row["point_id"], "z": z,
                             "pols_sick_dur_init": held / count})
    return pd.DataFrame(rows, columns=list(_IP_COHORTS))


def _ip_claims_total(name, args):
    """``IP_UK_S``'s ``claims`` keys as ``IP_UK_SEC`` takes them at stage ``"EC"`` (R9,
    R12).

    S's ``claims(t, kind=None)`` is cached under ``(t, None)`` where S asks for the total,
    which its ``net_cf`` does: SEC's code ``ALL``, so ``None`` is mapped to ``"ALL"``,
    which :func:`codes` then turns into the int, as it turns S's kinds and timings.  Every
    other key, and every other cell's arguments, pass as they are, SEC's own codes among
    them, where a comparison of two SEC models passes it SEC's keys.
    """
    if name == "claims" and len(args) == 2 and args[1] is None:
        return (args[0], "ALL")
    return args


def _wp_units(s, d):
    """``WP_UK_S``'s units held entering month ``d``: its ``units(d - 1)``, the close of the
    month before, or where S's frame opens, at ``proj_start()``, its own opening units, the
    ``units`` column.  0 on the endowment, which holds none."""
    return s.units(d - 1) if d > s.proj_start() else s.units_init()


def _wp_price(s, d):
    """``WP_UK_S``'s unit price entering month ``d``: its ``unit_price(d - 1)``, which the
    declarations before month ``d`` have raised, or where S's frame opens its own
    ``unit_price_init``, the seed price on new business."""
    return s.unit_price(d - 1) if d > s.proj_start() else s.unit_price_init()


def _wp_attaching(s, d):
    """``WP_UK_S``'s attaching bonus entering month ``d``, on the endowment: the guarantee
    month ``d`` opens with, its ``guar_benefit_open(d)``, less the sum assured, every
    declaration before month ``d`` in it.  0 on the bond, whose bonus is in its price."""
    if s.is_unitised():
        return 0.0
    return s.guar_benefit_open(d) - s.sum_assured()


def _wp_charges(s, d):
    """``WP_UK_S``'s guarantee charges taken per policy before month ``d``: its
    ``guar_charge_cum_pp(d - 1)``, the cumulant the charge's cap reads in month ``d``, or 0
    where S's frame opens, where S restarts it, on new business and on its points in
    force alike."""
    return s.guar_charge_cum_pp(d - 1) if d > s.proj_start() else 0.0


def _wp_rate(s, d):
    """``WP_UK_S``'s bonus rate declared at the last declaration before month ``d``, at the
    end of policy month ``12 x duration(d) - 1`` (D6): the declarations from month ``d`` on
    are the SEC model's, at today's References, and start from it.  S's own declaration
    where its frame has made it by its rule, past its first frame year, and S's carried
    column otherwise, which its first frame year keeps.  With the rule off the two are
    the column."""
    last = 12 * s.duration(d) - 1
    return s.bonus_rate(last) if last > s.proj_start() + 11 else s.bonus_rate_init()


def _wp_smoothing(s, d):
    """``WP_UK_S``'s smoothing account entering month ``d``, per policy in force then.

    S's ``smoothing_account(d - 1)``, the estate's cost on the exits before month ``d``,
    over its count in force, ``pols_if(d)``: per policy, so that the count is the one
    weight.  0 where S's frame opens, where S restarts the account, and where no policy
    is in force, which has no policy to carry it.
    """
    count = s.pols_if(d)
    if d <= s.proj_start() or count <= 0:
        return 0.0
    return s.smoothing_account(d - 1) / count


# WP_UK_SEC's opening state (D6; UKLIB-SEC-PLAN.md §6.5): what WP_UK_S carries into month d,
# its close of month d - 1, each per policy, so that policy_count is the one weight.  The
# asset share, S's asset_share_at(d, "BEF_PREM"); the units and the unit price, S's of month
# d - 1 (_wp_units, _wp_price); on the endowment the attaching bonus, the guarantee month d
# opens with less the sum assured (_wp_attaching); the smoothed payout month d opens with,
# S's smoothed_payout_open(d); the bonus rate declared at the last declaration before
# month d, from which the SEC model's own declarations start (_wp_rate); and the two
# cumulants S restarts at 0 where its frame opens, the
# guarantee charges taken (_wp_charges) and the smoothing account per policy in force
# (_wp_smoothing).  At a twin's source_mth, S's frame opening, these are what S itself
# assumes there: its own columns, the units, the price, the attaching bonus, the asset
# share and the payout carried in, its bonus_rate, and 0 for both cumulants, on new
# business and on S's points in force at 60 and 240 alike.
_WP_STATE = {
    "asset_share_init": lambda s, d: s.asset_share_at(d, "BEF_PREM"),
    "units_init": _wp_units,
    "unit_price_init": _wp_price,
    "attaching_bonus_init": _wp_attaching,
    "smoothed_payout_init": lambda s, d: s.smoothed_payout_open(d),
    "bonus_rate_init": _wp_rate,
    "guar_charge_cum_pp_init": _wp_charges,
    "smoothing_account_init": _wp_smoothing,
}


def _wp_claims_total(name, args):
    """``WP_UK_S``'s ``claims`` keys as ``WP_UK_SEC`` takes them at stage ``"EC"`` (R9,
    R12).

    S's ``claims(t, kind=None)`` is cached under ``(t, None)`` where S asks for the total,
    which its ``net_cf`` does: SEC's code ``ALL``, so ``None`` is mapped to ``"ALL"``,
    which :func:`codes` then turns into the int, as it turns S's kinds and timings.  Every
    other key, and every other cell's arguments, pass as they are, SEC's own codes among
    them, where a comparison of two SEC models passes it SEC's keys.
    """
    if name == "claims" and len(args) == 2 and args[1] is None:
        return (args[0], "ALL")
    return args


# C4's also, each model's SecSpec c4_also (UKLIB-SEC-PLAN.md, M15).  full_sweep evaluates
# every cell without parameters and every cell of t alone, at every month of the frame and
# the month after it, but it reaches a cell of a code or of a life only at the arguments
# some swept cell asks of it: no formula reads the count at AFT_DECR, the end of the month,
# for one, nor a life's labels.  So each model's also asks what no swept cell reads.  Six
# ask every cell that takes a timing or a kind at every code it takes, in every month of
# the frame and the month after it, on every row, as each sample_sec.py calls them, IP's
# the cohorts besides, and Term's and CI's every cell of a life at both lives
# (_ask_every_life); PA's, whose sweep reaches every timing and kind but the payments to
# date's, asks those and the cells of a life no swept cell reads.  Each cell of a model's
# _*_CODED takes a code of the names it lists, read from the point's own References
# (_code_of); each code is one its cell takes, so no call raises.  The conventions' C4 on
# the committed points passes each through the spec (uk_sec_support.spec_c4_also), and
# each product module passes the same to its own C4 comparisons, and holds it, row by row,
# to the codes and lives each cell takes in modelx (test_..._uk_sec.py's test of C4's
# codes).


def _code_of(proj, label):
    """The argument that selects timing or kind ``label`` on ``proj``: the model's int
    Reference of that name where it has one, as at stage ``"EC"``, else the string, as at
    ``"E"``; each product module's ``_code``."""
    value = proj.refs.get(label) if label in proj.refs else None
    return value if isinstance(value, int) and not isinstance(value, bool) else label


def _ask_every_code(proj, coded):
    """Ask each cell of ``coded``, ``{cell: names of the codes it takes}``, at every code it
    takes, in every month of ``proj``'s frame and the month after it, ``t = 0 ..
    proj_len()``: the ``also`` of a model whose cells of a code take nothing else."""
    for t in range(proj.proj_len() + 1):
        for cell, names in coded.items():
            for name in names:
                proj.cells[cell](t, _code_of(proj, name))


# The lives of a model of two, which every call of a cell of a life passes.
_LIVES = (1, 2)


def _ask_every_life(proj, alone, monthly):
    """Ask each cell of a life at both lives, :data:`_LIVES`: each of ``alone``, a cell of
    a life alone, once, and each of ``monthly``, a cell of a month and a life, in every
    month of ``proj``'s frame and the month after it, ``t = 0 .. proj_len()``, as
    :func:`_ask_every_code` asks the cells of a code.

    A single life's point refuses its second life, ``invalid life``, wherever a cell reads
    it: its issue age, its row of the table and its attained age always, and its rates in
    cover, which are 0 outside it before they read a life.  Such a call is passed over,
    and no other: the refusal at life 2 on a point that is a single life by its own
    reading, ``is_joint()``.  It caches nothing, so it enters no expectation, and the
    compiled run, which makes only the calls expected, never makes it.  Any other raise
    is raised, that refusal at life 1 or on a joint point among them, since an ``also``
    must not raise; ``test_sec_support_uk.py`` holds each.
    """
    def ask(name, args):
        try:
            proj.cells[name](*args)
        except Exception as err:            # a second life a single life refuses
            if not (args[-1] == 2 and _error_text(err) == "ValueError: invalid life"
                    and not proj.is_joint()):
                raise

    for name in alone:
        for life in _LIVES:
            ask(name, (life,))
    for t in range(proj.proj_len() + 1):
        for name in monthly:
            for life in _LIVES:
                ask(name, (t, life))


# Term_UK_SEC's cells of a code: the count's four timings and the claims' three kinds and
# their total.  No formula reads the count at AFT_DECR, nor at BEF_LAPSE in the month after
# the frame or before issue; the reports reach every kind.
_TERM_CODED = {"pols_if_at": ("BEF_NB", "BEF_DECR", "BEF_LAPSE", "AFT_DECR"),
               "claims": ("DEATH", "FIB", "LAPSE", "ALL")}

# Term_UK_SEC's cells of a life, as (those of a life alone, those of a month and a life):
# each life's issue age, labels and row of the mortality table, and its attained age and
# two rates.  No formula reads a label, nor the age outside cover, nor on a single life the
# rates' second life, 0 outside cover.
_TERM_LIVES = (("age_at_entry", "sex", "smoker", "mort_group"),
               ("age", "mort_rate_base", "mort_rate_life"))


def _term_c4_also(proj):
    """What C4 compares of a ``Term_UK_SEC`` point beyond its full sweep (M15): every cell
    of :data:`_TERM_CODED` at every code it takes, and every cell of a life,
    :data:`_TERM_LIVES`, at both lives, at ``t = 0 .. proj_len()``, the count at
    ``AFT_DECR`` and each life's labels among them, as ``sample_sec.py`` calls them."""
    _ask_every_code(proj, _TERM_CODED)
    _ask_every_life(proj, *_TERM_LIVES)


# CI_UK_SEC's cells of a code: the count's four timings, the three benefits per policy and
# the claims' four kinds and their total.  No formula reads the count at BEF_LAPSE or
# AFT_DECR, nor a benefit per policy, in the month after the frame, nor the count at
# BEF_LAPSE or a benefit before issue.
_CI_CODED = {"pols_if_at": ("BEF_NB", "BEF_DECR", "BEF_LAPSE", "AFT_DECR"),
             "benefit_pp": ("MAIN", "AP", "CHILD"),
             "claims": ("MAIN", "AP", "CHILD", "LAPSE", "ALL")}

# CI_UK_SEC's cells of a life, as (those of a life alone, those of a month and a life):
# each life's issue age, labels and row of the rate tables, and its attained age and four
# rates.  No formula reads a label, nor the age outside cover, nor on a single life the
# rates' second life, 0 outside cover.
_CI_LIVES = (("age_at_entry", "sex", "smoker", "rate_group"),
             ("age", "ci_rate_base", "mort_rate", "ci_rate", "claim_rate_life"))


def _ci_c4_also(proj):
    """What C4 compares of a ``CI_UK_SEC`` point beyond its full sweep (M15): every cell of
    :data:`_CI_CODED` at every code it takes, and every cell of a life,
    :data:`_CI_LIVES`, at both lives, at ``t = 0 .. proj_len()``, each benefit per policy in
    the month after the frame and each life's labels among them."""
    _ask_every_code(proj, _CI_CODED)
    _ask_every_life(proj, *_CI_LIVES)


# ULB_UK_SEC's cells of a code: the count's four timings and the fund's four, which share
# the caches' inner width of 8 and refuse each other's, and the claims' two kinds and their
# total.  No formula reads the fund at BEF_GROWTH, the count at AFT_DECR but at the end of
# a policy year's walk, nor the count at BEF_SURR in the month after the frame or before
# issue.
_ULB_CODED = {"pols_if_at": ("BEF_NB", "BEF_DECR", "BEF_SURR", "AFT_DECR"),
              "av_pp_at": ("BEF_GROWTH", "AFT_GROWTH", "AFT_CHARGE", "AFT_WD"),
              "claims": ("DEATH", "SURRENDER", "ALL")}


def _ulb_c4_also(proj):
    """What C4 compares of a ``ULB_UK_SEC`` point beyond its full sweep (M15): every cell
    of :data:`_ULB_CODED` at every code it takes, at ``t = 0 .. proj_len()``, the fund at
    ``BEF_GROWTH`` and the count at ``AFT_DECR`` among them."""
    _ask_every_code(proj, _ULB_CODED)


# WOL_UK_SEC's cells of a code: the count's four timings, the four benefits per policy and
# the claims' three kinds and their total; every code inside the one inner width is one its
# cell takes.
_WOL_CODED = {"pols_if_at": ("BEF_NB", "BEF_DECR", "BEF_LAPSE", "AFT_DECR"),
              "benefit_pp": ("NON_ACC", "ACC", "DEATH", "PAID_UP"),
              "claims": ("DEATH", "DEATH_PU", "LAPSE", "ALL")}


def _wol_c4_also(proj):
    """What C4 compares of a ``WOL_UK_SEC`` point beyond its full sweep (M6).

    ``full_sweep`` reaches a cell of more than ``t`` only at the codes some swept cell asks
    of it: no cell reads the count at ``AFT_DECR``, the end of the month, and on the
    underwritten cell none reads ``benefit_pp`` at ``NON_ACC`` or ``ACC``, which only the
    over-50s blend reads.  So, as ``sample_sec.py`` does, this calls every timing, every
    benefit and every kind, the claims total among them (:data:`_WOL_CODED`), at ``t = 0
    .. proj_len()``; every code inside the one inner width is one its cell takes, so none
    raises.
    """
    _ask_every_code(proj, _WOL_CODED)


def _pa_c4_also(proj):
    """C4's ``also`` on every ``PA_UK_SEC`` row it compares: the cells and codes no swept
    cell reads (M12).

    A sweep evaluates every cell without parameters and every cell of ``t`` alone, at every
    month of the frame and the month after, the payments to date on every stream and their
    refusal among them, and every other cell only where those read it.  So it calls,
    besides: each life's death density, ``lives_death(t, life)``, at every month, which the
    last-death density replaces in every flow but the claim on the first death, and so the
    dependant's on every row and the annuitant's on a single life; the payments to date at
    ``ALL`` at every key the frame reads, which no cell reads; where value protection is on
    the first death, the annuitant's, ``ANNUITANT``, there and its refusal, which only an
    overflow calls; the income's refusal in every policy year the frame reads; and each
    life's label.  A row whose annuitant's payments to date no projection reads is not
    asked them: on RPI-linked escalation they open from ``cum_annuity_pp_init``, which such
    a row leaves blank, so they are NaN there, refused past the first key in both engines,
    and never read.  ``test_pension_annuity_uk_sec.py``'s
    ``test_c4_asks_every_cell_at_every_code`` holds the sweep and this to every code.
    """
    end = proj.proj_len()
    for t in range(end + 1):
        for life in (1, 2):
            proj.lives_death(t, life)
    annuitant = proj.vp_pct() > 0.0 and proj.is_first_death()
    for k in range(max(proj.duration_mth_init(), 0), proj.duration_mth(end) + 1):
        proj.cum_annuity_pp(k, _code_of(proj, "ALL"))
        if annuitant:
            proj.cum_annuity_pp(k, _code_of(proj, "ANNUITANT"))
            proj.cum_annuity_pp_refusal(k)
    for y in range(proj.policy_year_init(), proj.policy_year(end - 1) + 1):
        proj.annual_income_refusal(y)
    for life in (1, 2):
        proj.sex(life)


# IP_UK_SEC's cells C4 asks at every code: the count's three timings and the claims' three
# kinds and their total.  What each takes is derived in modelx, row by row, on every row
# test_income_protection_uk_sec.py's C4 compares, and this must name exactly that (M8's
# review, after M14's).
_IP_CODED = {"pols_if_at": ("BEF_NB", "BEF_DECR", "AFT_DECR"),
             "claims": ("BENEFIT", "DEATH", "LAPSE", "ALL")}


def _ip_c4_also(proj):
    """What C4 compares of an ``IP_UK_SEC`` point beyond its full sweep (M8).

    ``full_sweep`` calls every cell without parameters, ``pv_benefits``, ``annuity_dis``
    and ``premium_basis`` among them, which no report reads, and every cell of ``t`` alone
    at ``t = 0 .. proj_len()``, ``disc_factor`` among them; it reaches a cell of more only
    at the arguments some swept cell asks of it.  No cell reads the count at ``BEF_DECR`` or
    ``AFT_DECR``, a claim duration's survival where no cohort holds lives, nor a cohort past
    the ones that can hold lives, ``claim_dur_live(t)``, where the sums stop.  So, as
    ``sample_sec.py`` does, this calls every timing and every kind, the claims total among
    them (:data:`_IP_CODED`), in every month of the frame and the month after it, and the
    survival of every claim duration from 1 to ``max_dur()``; and the cohorts past the live
    ones: claim duration 0 and the first past the live ones in every month, and every claim
    duration from 0 to ``max_dur()`` in the month the point is first on the books, the
    month after it, the frame's last month and the month after the frame, where the live
    triangle's edges meet the cache's.  Every other cohort is the zero of one asked here,
    down its diagonal: the sample traces the whole rectangle in the export, where a cohort
    costs a C double, and modelx, whose cache entry costs a thousand times that, forms the
    triangle and its edges.  Every claim duration asked is inside the ``z`` cache, so none
    raises.
    """
    last, top, entry = proj.proj_len(), proj.max_dur(), proj.t_entry()
    edges = {entry, entry + 1, last - 1, last}
    for t in range(last + 1):
        for cell, names in _IP_CODED.items():
            for name in names:
                proj.cells[cell](t, _code_of(proj, name))
        live = proj.cells["claim_dur_live"](t)
        zs = (range(top + 1) if t in edges
              else (0, *range(live + 1, min(live + 1, top) + 1)))
        for z in zs:
            proj.cells["pols_sick_dur"](t, z)
    for z in range(1, top + 1):
        proj.cells["claim_surv_step"](z)


# WP_UK_SEC's cells of a timing or a kind, each with the codes it takes, by name: the
# count's four timings and the asset share's six, one numbering in one inner width of 10,
# the payouts' four kinds and the claims' three and their total.
_WP_CODED = {"pols_if_at": ("BEF_NB", "BEF_DECR", "BEF_SURR", "AFT_DECR"),
             "asset_share_at": ("BEF_PREM", "BEF_RETURN", "AFT_RETURN", "AFT_CHARGE",
                                "AFT_ST", "AFT_MC"),
             "claim_pp": ("DEATH", "SURRENDER", "GUARANTEE", "MATURITY"),
             "smoothing_cost_pp": ("DEATH", "SURRENDER", "GUARANTEE", "MATURITY"),
             "claims": ("DEATH", "SURRENDER", "MATURITY", "ALL")}


def _wp_c4_also(proj):
    """What C4 compares of a ``WP_UK_SEC`` point beyond its full sweep (M14).

    ``full_sweep`` evaluates every cell without parameters and every cell of ``t`` alone,
    at every month of the frame and the month after it, ``unit_price`` on the endowment,
    ``policy_value_pp``, ``smoothed_payout_capped``, ``bonus_supportable``,
    ``declaration_month`` and the six refusal cells among them; but it reaches a cell of a
    code only at the codes some swept cell asks of it: no cell reads the count at
    ``AFT_DECR``, the end of the month, nor ``smoothing_cost_pp`` at ``GUARANTEE``, and only
    the asset share's refusal reads ``asset_share_at(t, AFT_MC)``.  So, as
    ``sample_sec.py`` does, this calls every cell of :data:`_WP_CODED` at every code it
    takes, the count's four timings and the asset share's six, the payouts' four kinds and
    the claims' three and their total, at ``t = 0 .. proj_len()``, on every row, whatever
    its chassis; each call is of a code its cell takes, so none raises.
    """
    _ask_every_code(proj, _WP_CODED)


SEC_SPECS: dict[str, SecSpec] = {
    # Term's state is seven columns (_TERM_STATE above) and the waiver pipeline, a long
    # companion, wop_pipeline_sec.csv, keyed (point_id, lag), lag the months before the
    # valuation date of an incapacity still in the deferred period there, measured at the
    # valuation instant (UKLIB-SEC-PLAN.md §6.1, precised at M1), built by _term_pipeline.
    # pols_if_init becomes policy_count (the default), and
    # duration_inforce, S's elapsed policy years, is dropped for duration_mth, 60 on S's
    # point 8.  The derived rows are the indexed point on its fifth anniversary, 60, the
    # factors of policy year 5 carried in and the anniversary's step its month 0's; the
    # family income benefit point mid-year at 66, its ledger in payment; the waiver point
    # at 66, after the select period's end, its pipeline full and a share waived, and at
    # 4, inside its deferred period, its pipeline four months deep and nothing waived yet;
    # and the anchor cell in its last covered month, 299, a one-row frame.  The future row
    # is the waiver point issued 13 months after the valuation date: more than a year on
    # and off a valuation anniversary, so that the months before issue read policy years -1
    # and 0, where a missing guard would show.  T2's splice grid is built from this spec in
    # a temporary table, not committed.
    #
    # T1 holds on Term at any count: S charges acquisition and the initial commission on
    # the count in force at t = 0, which on a point issued then is the count issued, as SEC
    # charges them on pols_new_biz.  It skips three S cells besides the default three:
    #   proj_start: S's first projected month on the policy clock, 60 on S's point 8.
    #     Every SEC frame opens at t = 0 (D3), which the conventions assert.
    #   duration_inforce: S's elapsed policy years, which duration_mth replaces (D6).
    #   result_pols: SEC's gains pols_new_biz, the count D5 puts there, so the frame has a
    #     column S's lacks and cannot agree as a whole.  Each column it shares with S is a
    #     cell T1 compares at every month, and test_term_assurance_uk_sec.py compares the
    #     report itself with S's, on every column both hold.
    # At stage EC (M2), S's timings and kinds are SEC's int codes, BEF_NB to AFT_DECR and
    # DEATH to LAPSE, which codes maps, and S's claims(t, None) keys, the kind=None total
    # its net_cf caches, are SEC's code ALL: the spec's twin_arg_map, _term_claims_total,
    # maps None to "ALL", and codes maps it and the rest.  S's label accessors stay S's,
    # called by reporting and T1 alone: shape(), premium_mode() and mort_basis() return
    # the column of their own name, and the registry's "reporting_columns" names what the
    # other two return, sex(life) "sex" or "joint_sex" by life and smoker(life) "smoker" or
    # "joint_smoker".  T1 compares each at the arguments S cached.
    #
    # Phase 2 sizes its caches from the contract (spec_sec.py holds each derivation):
    #   t 0..721: policy_term_max, 50 years, the longest term, issued future_horizon_mth,
    #     120 months, after the valuation date, a frame of 720 months, its month after, and
    #     the roll-forward's t + 1 there;
    #   k 0..599, the policy months of cover, where benefit_sched is read, and the
    #     pipeline's lags, fewer than the months in force;
    #   m 1..480, the months the family income benefit's commuted value is read at, on
    #     policy_term_max_fib's 40 years;
    #   life 1..2, the lives of a joint first death.
    # proj_len() refuses a term above either maximum, an issue age below issue_age_min, 18,
    # and cover past expiry_age_max, 90, or expiry_age_max_fib, 70, each naming the point.
    "Term_UK_SEC": SecSpec(
        twin="Term_UK_S",
        column_map={"duration_inforce": None},
        duration_of=lambda row: 12 * int(row["duration_inforce"]),
        derived=((5, 60), (3, 66), (7, 66), (7, 4), (1, 299)),
        future=((7, 13),),
        state=_TERM_STATE,
        twin_state=_TERM_STATE,
        exempt=frozenset({"proj_start", "duration_inforce", "result_pols"}),
        companions={"wop_pipeline_sec.csv": _term_pipeline},
        twin_arg_map=_term_claims_total,
        c4_also=_term_c4_also,
    ),
    # CI's state is six columns (_CI_STATE above), with no companion: the reviews, the
    # latch and the factors are closed forms on the policy clock, and the count is the one
    # chain.  pols_if_init becomes policy_count (the default), and every S point is new
    # business, so duration_of is the default too.  The derived rows are the indexed point
    # on its third anniversary, 36, the factors of policy year 3 carried in and the
    # anniversary's step its month 0's; the reviewable point on its first review, 60, no
    # review before it and that review its month 0's, inside the review's twelve-month
    # shock window, 66, which a review before the valuation date opened, and mid-year after
    # it, 78, the window closed; and the anchor cell in its last covered month, 299, a
    # one-row frame.  The future row is the indexed point issued 13 months after the
    # valuation date: more than a year on and off a valuation anniversary, so that the
    # months before issue read policy years -1 and 0, where a missing guard would show, and
    # its index steps fall a month after the valuation anniversaries.  T2's splice grid is
    # built from this spec in a temporary table, not committed.
    #
    # And one row S reaches only under a review change of its own (derived_refs).  At the
    # shipped change of 0 no S point has a shock month, a closed latch or a review factor
    # other than 1, so no other committed row carries a review history, and C2 would
    # freeze no review path.  So the reviewable point is restated at S month 124 from S
    # run under a change of 10%: inside the window its second review opened, at policy
    # month 120, its latch closed at its first, its review factor 1.1 squared.  At the
    # shipped change of 0 the committed model projects S under 10% from there to its next
    # review, at policy month 180, and today's change from then on.
    #
    # T1 holds on CI at any count: S charges the initial expense on the count in force at
    # t = 0, which on a point issued then is the count issued, as SEC charges it on
    # pols_new_biz.  It skips two S cells besides the default three:
    #   result_pols: SEC's gains pols_new_biz, the count D5 puts there, so the frame has a
    #     column S's lacks and cannot agree as a whole.  Each column it shares with S is a
    #     cell T1 compares at every month, and test_critical_illness_uk_sec.py compares the
    #     report itself with S's, on every column both hold.
    #   pivot_interp: S's interpolation of the pivot table, a .loc, a sorted generator and
    #     text keys per call, keyed by a sex and a smoker status as text, which no C cell
    #     takes.  From stage EC (M4) Data makes it once, by S's own formula, element by
    #     element, at every attained age the contract admits, Data.i_ci_array and
    #     q_d_array, which ci_rate_base and mort_rate read; T1 compares those two at every
    #     month S evaluates, and test_critical_illness_uk_sec.py holds each array to S's
    #     pivot_interp at every group and age, bit for bit.
    # At stage EC (M4), S's timings and kinds are SEC's int codes, BEF_NB to AFT_DECR and
    # MAIN to LAPSE, which codes maps, and S's claims(t, None) keys, the kind=None total its
    # net_cf caches, are SEC's code ALL: the spec's twin_arg_map, _ci_claims_total, maps
    # None to "ALL", and codes maps it and the rest.  S's label accessors stay S's, called
    # by reporting and T1 alone: contract_type(), life_basis(), cover_basis(),
    # premium_guarantee() and premium_mode() return the column of their own name, and the
    # registry's "reporting_columns" names what the other two return, sex(life) "sex" or
    # "joint_sex" by life and smoker(life) "smoker" or "joint_smoker".  T1 compares each at
    # the arguments S cached.
    #
    # Phase 2 sizes its caches from the contract (spec_sec.py holds each derivation):
    #   t 0..721: policy_term_max, 50 years, the longest term, issued future_horizon_mth,
    #     120 months, after the valuation date, a frame of 720 months, its month after, and
    #     the roll-forward's t + 1 there;
    #   life 1..2, the lives of a joint first event.
    # proj_len() refuses a term outside policy_term_min to policy_term_max, a life issued
    # outside issue_age_min to issue_age_max, and cover past expiry_age_max, 75, each naming
    # the point; the pivot arrays hold the attained ages 18 to 74 between them.
    "CI_UK_SEC": SecSpec(
        twin="CI_UK_S",
        derived=((4, 36), (3, 60), (3, 66), (3, 78), (1, 299)),
        future=((4, 13),),
        state=_CI_STATE,
        twin_state=_CI_STATE,
        exempt=frozenset({"result_pols", "pivot_interp"}),
        derived_refs={(3, 124): {"review_prem_shock": 0.10}},
        twin_arg_map=_ci_claims_total,
        c4_also=_ci_c4_also,
    ),
    # ULB's state is three columns (_ULB_STATE above): the unit fund, S's uf_init renamed
    # av_pp_init; the withdrawals and adviser charges since issue, wd_cum_pp_init, which
    # open the GMDB; and the allowance accrued, allowance_cum_pp_init.  pols_if_init
    # becomes policy_count (the default).  Every S point is new
    # business.  The derived rows are the anchor cell at 30, mid-year in the 5% surrender
    # band; the adviser-charge point at 66, mid-year in the 8% band, its excess gain already
    # above 0, since its charges consume the allowance beside its withdrawals; the GMDB
    # point at 240, the first month of policy year 21, where the allowance-exhaustion step
    # applies and the guarantee has just run out; and the anchor cell at 352, the last month
    # before its fund is exhausted, a one-row frame.  The future row is the GMDB point issued 13
    # months after the valuation date: more than a year on and off a valuation anniversary,
    # so that the months before issue read policy years -1 and 0, where a missing guard
    # would show.  T2's splice grid is built from this spec in a temporary table, not
    # committed.
    #
    # And one row S reaches only under a fund return of its own (derived_refs).  At S's
    # References no state has the rider charging: S point 4's guarantee is in the money in
    # its issue month alone, by 82.88 pounds on the death benefit and never on the charge,
    # which reads the fund before the month's withdrawal, so the twin of point 4 at t = 0
    # and the future row at t = 13 are in it there, and no committed row after, and C2
    # would freeze no rider charge.  So the GMDB point is restated at S month 66, mid-way
    # through policy year 6, from S run under a fund_return of 0, a fund that has earned
    # nothing since issue: 0.7298 policies, as at the shipped return, since no decrement
    # reads it, a fund of 67,232.39 and a guarantee of 72,500, the premium less 66
    # withdrawals, above the uplifted fund after charges, so that the rider charges from
    # the row's first month.  At the shipped return the committed model grows that fund at
    # 5% from the valuation date, so the two paths part in month 0's growth; the guarantee
    # stays in the money on the charge for the frame's first 36 months, and on the death
    # benefit for 39.  The splice's variants reach the charge on their own grid.
    #
    # T1 holds at any count: S charges acquisition on the count in force at t = 0, which on a
    # point issued then is the count issued, as SEC charges it on pols_new_biz.  It skips one
    # S cell besides the default three:
    #   av_init_pp: S's accessor of uf_init, the fund at outset, which av_pp_init replaces,
    #     reading the same column renamed, D6's name for the fund entering month 0.
    # SEC ends a frame where the fund opens at or below depletion_threshold, half a pence,
    # where S ends it where the fund opens on exactly 0 or less (UKLIB-SEC-PLAN.md §6.6, §9
    # item 10).  On S point 3, whose adviser charge closes its fund on a rounding of 3.4e-15
    # at the end of month 322, S projects month 323 and SEC does not; the conventions' T1
    # compares that twin over the months the two frames run alike (TWIN_FRAME_ENDS there),
    # and test_unit_linked_bond_uk_sec.py the rest.
    # At stage EC (M10), S's timings and kinds are SEC's int codes, BEF_NB to AFT_WD and
    # DEATH to SURRENDER, which codes maps, and S's claims(t, None) keys, the kind=None
    # total its check_unit_funding_resid caches, are SEC's code ALL: the spec's
    # twin_arg_map, _ulb_claims_total, maps None to "ALL", and codes maps it and the rest.
    # S's label accessors stay S's, called by reporting and T1 alone, sex() now refusing
    # any value but M and F as lives() and wd_pattern() refuse theirs: each returns the
    # column of its own name.
    #
    # Phase 2 sizes its caches from the contract (spec_sec.py holds each derivation):
    #   t 0..1,357: a bond issued at issue_age_min, 18, whose fund lasts to omega_age_max,
    #     121, the shipped table's last age plus one, a cover of 1,236 months, issued
    #     future_horizon_mth, 120 months, after the valuation date, a frame of 1,356 months,
    #     its month after, and the roll-forward's t + 1 there;
    #   y 2..103, the policy years whose openings the fund, the withdrawals since issue and
    #     the count are blocked by, to the policy year of the longest cover's last month.
    # proj_len() refuses an issue age below issue_age_min, an omega_age above
    # omega_age_max, one at or past omega_age, and a bond in force whose fund is at or below
    # depletion_threshold, each naming the point.
    "ULB_UK_SEC": SecSpec(
        twin="ULB_UK_S",
        column_map={"uf_init": "av_pp_init"},
        derived=((1, 30), (3, 66), (4, 240), (1, 352)),
        future=((4, 13),),
        state=_ULB_STATE,
        twin_state=_ULB_STATE,
        exempt=frozenset({"av_init_pp"}),
        derived_refs={(4, 66): {"fund_return": 0.0}},
        twin_arg_map=_ulb_claims_total,
        c4_also=_ulb_c4_also,
    ),
    # WOL's state is six columns (_WOL_STATE above), with no companion: the paid-up
    # strand's count and its cover per paid-up policy, which need no cohort of conversion
    # months, since paid-up policies neither lapse nor escalate; the premiums paid; the
    # cover and premium before month 0's events, the year an anniversary at the valuation
    # date closes; and the crossover, if it fell before the valuation date.  pols_if_init becomes
    # policy_count (the default), the full-cover count, and every S point is new business.
    # The derived rows are the anchor cell at 6, inside its moratorium and its first
    # policy year, its refund reading the premiums paid and its commission still due; the
    # anchor cell at 166, its crossover month; the pro-rata paid-up point at 200, its
    # paid-up strand in force beside full cover; the RPI point at 186, past its own
    # crossover, the increases of fifteen anniversaries carried in; the underwritten
    # increasing point at 12, on its first anniversary, its first increase at t = 0 and its
    # suicide window just closed; and point 7 at 300, the month its premiums cease.  The
    # future row is the RPI point issued 13 months after the valuation date: more than a
    # year on and off a valuation anniversary, so that the months before issue read policy
    # years -1 and 0, where a missing guard would show, and its increases fall a month
    # after the valuation anniversaries.  T2's splice grid is built from this spec in a
    # temporary table, not committed.
    #
    # And three rows S reaches only under References of its own (derived_refs), since at
    # S's References each history is what today's References rebuild, so that C2 would
    # freeze no path that reads a column rather than a Reference: the RPI point at 120,
    # from S under an RPI of 5%, its cover and premium 1.05 and 1.075 to the ninth power,
    # the year its tenth anniversary, at the valuation date, closes; the underwritten
    # increasing point at 120, from S under a take-up of a half, its increases 2.5% and 5% a
    # year; and the pro-rata paid-up point at 180, from S under a
    # crossover stress of 100, which lapses every policy past its crossover at policy month
    # 166 and so converts the whole full-cover strand to paid-up there: a point paid-up
    # entirely, its policy_count 0.  At the shipped References the committed model
    # projects each from that history at today's References.
    #
    # T1 holds on WOL at any count: S charges acquisition on the count in force at t = 0,
    # which on a point issued then is the count issued, as SEC charges it on pols_new_biz.
    # It skips one S cell besides the default three:
    #   result_pols: SEC's gains pols_new_biz, the count D5 puts there, and the paid-up
    #     deaths and the truncation residual, so the frame has columns S's lacks and cannot
    #     agree as a whole.  Each column it shares with S is a cell T1 compares at every
    #     month, and test_whole_of_life_uk_sec.py compares the report itself with S's, on
    #     every column both hold.
    # At stage EC (M6), S's timings and kinds are SEC's int codes, BEF_NB to AFT_DECR,
    # DEATH to PAID_UP for the benefits and DEATH to LAPSE for the claims, DEATH one code in
    # both, which codes maps, and S's claims(t, None) keys, the kind=None total its net_cf
    # caches, are SEC's code ALL: the spec's twin_arg_map, _wol_claims_total, maps None to
    # "ALL", and codes maps it and the rest.  S's label accessors stay S's, called by
    # reporting and T1 alone, sex() and smoker() now refusing any value but their codes as
    # cell() and escalation() refuse theirs: each returns the column of its own name, and
    # mort_basis() the cell's through the registry's "reporting_columns" map.
    #
    # Phase 2 sizes its caches from the contract (spec_sec.py holds each derivation):
    #   t 0..1,357: a policy issued at issue_age_min, 18, to omega_age_max, 121, the largest
    #     omega_age proj_len() accepts, a year past mort_table.csv's last age, a cover of
    #     1,236 months, issued future_horizon_mth, 120 months, after the valuation date: a
    #     frame of 1,356 months, t 0..1,355, its month after, and the roll-forward's t + 1
    #     there;
    #   y 2..103, the policy years whose openings the four blocked chains read, to the
    #     policy year of the longest cover's last month.
    # proj_len() refuses an issue age below issue_age_min, an omega_age above
    # omega_age_max, one at or past omega_age, and a point at or past the limiting age at
    # the valuation date, each naming the point.
    "WOL_UK_SEC": SecSpec(
        twin="WOL_UK_S",
        derived=((1, 6), (1, 166), (3, 200), (4, 186), (6, 12), (7, 300)),
        future=((4, 13),),
        state=_WOL_STATE,
        twin_state=_WOL_STATE,
        exempt=frozenset({"result_pols"}),
        derived_refs={(4, 120): {"rpi_rate": 0.05}, (6, 120): {"esc_take_up": 0.5},
                      (3, 180): {"lapse_crossover_beta": 100.0}},
        twin_arg_map=_wol_claims_total,
        c4_also=_wol_c4_also,
    ),
    # PA's state is six columns per contract (_PA_STATE above), with no companion: each
    # life's survival, the payments made to date on every stream, and on RPI-linked
    # escalation the income of the year under way, the ratchet's peak over the latest
    # index and the annuitant's payments to date, the last three blank where the SEC model
    # does not read them.  pols_if_init becomes policy_count (the default), set by
    # _PA_STATE to S's count and not S's pols_if, a closing measure (D5).  Every S point is
    # new business.  The derived rows are the worked example at 17, the month after the
    # annuitant's death, the dependant's first instalment at t = 0; the proportionate
    # payment's point at 16, the month of the death, value protection and the proportionate
    # payment both at t = 0; the guarantee's point at 120, the guarantee ended and the
    # dependant's income starting without overlap; the LPI point at 24, its second
    # anniversary in month 0; the RPI catch-up point at 30, mid-year; the first-death value
    # protection at 101, the last month its balance opens above 0; the last-survivor value
    # protection at 170, likewise; the rated single life at 575, the month before its
    # mortality cap binds; and the table basis's joint point at 635, a one-row frame.  The
    # future row is the RPI catch-up point starting 13 months after the valuation date: more
    # than a year on and off every payment step, so that the months before the start read
    # policy years -1 and 0, where a missing guard would show.  T2's splice grid is built
    # from this spec in a temporary table, not committed.
    #
    # And three rows S reaches only under an RPI of their own (derived_refs).  At the
    # shipped flat 3% the index never falls, so no state S reaches holds a ratchet's peak
    # above its index, nor an LPI increase capped or floored, and C2 would freeze no such
    # history.  So the catch-up point is restated at S month 60, its fifth anniversary in
    # month 0, from S run under an RPI of -2%: its income frozen at the first year's and its
    # peak 1 / 0.98^4 over the latest index, so that at the shipped 3% from the valuation
    # date its income stays frozen through two anniversaries and catches up at the third.
    # The LPI point at S month 42 from S run under 8%: its income raised by the cap's 5% a
    # year, where the shipped 3% would have raised it by 3%.  And the LPI point at S month
    # 54 from S run under -2%: its income held at the first year's by the floor.  C2
    # projects every row at the shipped References, under which the LPI's step is 3% on
    # every row, so it freezes the cap's and the floor's history, not the bounds
    # themselves; test_pension_annuity_uk_sec.py projects the two LPI rows under their own
    # RPI, where each bound binds.
    #
    # T1 holds on PA at any count: neither model charges acquisition, and every flow is the
    # count times a per-contract amount.  It skips one S cell besides the default three:
    #   result_pols: SEC's gains pols_new_biz and puts pols_if first, so the frame has a
    #     column S's lacks and cannot agree as a whole.  Each column it shares with S is a
    #     cell T1 compares at every month, and test_pension_annuity_uk_sec.py compares the
    #     report itself with S's, column by column.
    # S's annual_income_init, the first year's income, is SEC's annual_income_first; SEC's
    # annual_income_init is the income of the year under way at the valuation date, which on
    # a point starting at the valuation date is the first year's, so T1 compares the two.
    #
    # At stage EC (M12), S's timings and kinds are SEC's int codes, BEF_NB and BEF_DECR, VP,
    # PROP, ANNUITANT and ALL, which codes maps, and S's claims(t, None) keys, the kind=None
    # total its liability_cf caches, are SEC's code ALL: the spec's twin_arg_map,
    # _pa_claims_total, maps None to "ALL", and codes maps it and the rest.  S's label
    # accessors stay S's, called by reporting and T1 alone; payment_timing() returns the
    # timing column and sex(life) the annuitant's or the dependant's, which uk_registry's
    # "reporting_columns" names.
    #
    # Phase 2 sizes its caches from the contract (spec_sec.py holds each derivation):
    #   t 0..1,513: a life issued at issue_age_min, 0, the youngest issue age of every
    #     life, since S projects any age on the scenario basis, to the age stop at the
    #     contract's largest limiting age, omega_age_max, 116, the shipped table's last age
    #     plus one, or a guarantee of as many months, 12 x (116 - 0) = 1,392, the longest
    #     frame proj_len() admits, starting future_horizon_mth, 120 months, after the
    #     valuation date, a frame of 1,512 months, its closing time point t = proj_len(),
    #     which lives_if and cum_annuity_all read, and one of headroom;
    #   k 0..1,393, the policy time points to the stop rule's, 1,392; y 0..117, whose
    #     openings survival and the payments to date are blocked by, to the policy year of
    #     the closing time point; a 0..116 and x 0..116, the anniversaries and the ages read;
    #     and every 2-D cache 4 wide, the kinds' VP, PROP, ANNUITANT and ALL.
    # proj_len() refuses an issue age of any life below issue_age_min, on the table basis an
    # omega_age above omega_age_max, a guarantee above 12 x (omega_age - issue_age_min)
    # months, the longest frame from the start date, and on either basis a frame above
    # 12 x (omega_age_max - issue_age_min) months, 1,392, the table basis's longest, each
    # naming the point.  The scenario basis's omega_age is bounded by nothing, as at stage
    # E, but its frame is, by that rule, which refuses there a frame stage E projected.
    "PA_UK_SEC": SecSpec(
        twin="PA_UK_S",
        derived=((1, 17), (9, 16), (3, 120), (7, 24), (6, 30), (2, 101), (10, 170),
                 (8, 575), (2, 635)),
        future=((6, 13),),
        state=_PA_STATE,
        twin_state={c: f for c, f in _PA_STATE.items() if c != "policy_count"},
        exempt=frozenset({"result_pols"}),
        derived_refs={(6, 60): {"rpi_rate": -0.02}, (7, 42): {"rpi_rate": 0.08},
                      (7, 54): {"rpi_rate": -0.02}},
        twin_arg_map=_pa_claims_total,
        c4_also=_pa_c4_also,
    ),
    # IP's state is three columns (_IP_STATE above), the healthy share of the count and the
    # benefit and premium entering month 0, and the claim cohorts, a sparse companion,
    # inforce_cohorts_sec.csv, keyed (point_id, z), z the claim duration of the lives in
    # claim at the valuation instant, each a share of the count, built by _ip_cohorts
    # (UKLIB-SEC-PLAN.md §6.3).  pols_if_init becomes policy_count (the default), the lives
    # in health and in claim together, and claim_duration_months, S's one in-force claim
    # duration, which the cohorts replace, is dropped.  IP_UK_S's in_claim cells, points
    # 2, 5 and 7, are in force with their policy clock restarted at the valuation date:
    # their twins are issued n whole years before it, the least that holds the claim,
    # duration_mth 12n, at their entry age less n (_ip_twin_years), so that their ages,
    # claims and counts are S's and only their policy clocks differ.  The derived rows are
    # the anchor cell on its first anniversary, 12, its first escalation at t = 0; at 60,
    # policy year 6, the lapse table's last, and attained age 40, an inception pivot; and at
    # 359, its last covered month, its cohort vector 359 long; the claims-in-payment cell at
    # 24, claim duration 25, in duration year 3; the claim at duration 30 at 6, claim
    # duration 37, in year 4; the claim on the active-lives basis at 12, its recoveries
    # back in health and claiming again; the female cell at 13, after its first
    # anniversary; the older male cell at 118, in its last two months; and the level cell
    # mid-year at 30.  The future row is the female cell issued 13 months after the
    # valuation date: more than a year on and off a valuation anniversary, so that the
    # months before issue read policy years -1 and 0, where a missing guard would show.
    # T2's splice grid is built from this spec in a temporary table, not committed.
    #
    # And two rows S reaches only under an RPI of their own (derived_refs), each with its
    # cohorts read from S under it too.  At the shipped 3% the premium grows 4.5% a year,
    # below the escalation lapse shock's 5% threshold, and escalation never reaches its
    # 10% cap, so no state S reaches holds a lapse shocked by escalation or an escalation
    # capped, and C2 would freeze no such history.  So the anchor cell is restated at S
    # month 40 from S run under an RPI of 5%, its lapses shocked by 1.05 from policy year
    # 2, its benefit and premium 1.05 and 1.075 to the third power; and the female cell at
    # month 30 from S run under 12%, its benefit 1.1 and its premium 1.15 to the second
    # power, the cap's.  At the shipped References the committed model projects each from
    # that history at today's 3%.
    #
    # T1 holds on IP at any count: neither model charges acquisition, and every flow is a
    # count times an amount per policy.  It skips three S cells besides the default three:
    #   claim_duration_months: S's claim duration on an in_claim cell, which the claim
    #     cohorts replace (D6); 0 on every twin T1 compares.
    #   sick_cohorts and claim_rate_vectors: S's tuples, a month's cohorts and the rates of
    #     each claim duration, which a compiled cell cannot hold.  SEC carries each element
    #     in a cell of its own, the cohort at claim duration z of month t in
    #     pols_sick_dur(t, z), a recursion of two parameters, and the rates in rec_rate_mth,
    #     mort_rate_sick_mth and claim_surv_step, S's cells of one claim duration, which
    #     T1 compares where S's sweep reaches them; and S's four sums of the tuple,
    #     pols_sick, pols_sick_surv, pols_recovery and pols_death_sick, which T1 compares in
    #     every month, read every element.  test_income_protection_uk_sec.py maps the two
    #     onto SEC's cells on every row it compares, element by element, and holds the four
    #     sums to S's sum by their bits.  Kept as engine cells, they would need the key to
    #     admit a cell of a parameter spec_sec.py sizes, returning a tuple, which no C type
    #     holds, and would rebuild a vector of up to 625 floats a month from the recursion
    #     for every comparison.
    # S's status, the row's kind there, is kept as a label no formula reads.  S's claims(t,
    # None), the total, is SEC's claims(t, ALL) (_ip_claims_total).
    #
    # Phase 2 sizes its caches from the contract (UKLIB-SEC-PLAN.md §6.3's C list,
    # spec_sec.py): t 746, a policy issued at issue_age_min, 18, expiring at expiry_age_max,
    # 70, a cover of 624 months, issued future_horizon_mth, 120 months, after the valuation
    # date, a frame of 744, and the roll-forward's t + 1; and z 626, max_dur(), the cover
    # from issue and one cohort of headroom, which does not grow with the horizon.
    # proj_len() refuses an issue age outside issue_age_min to issue_age_max, an expiry age
    # outside expiry_age_min to expiry_age_max, a point at or past its policy end date at
    # the valuation date, and a cover longer than 624 months or a frame longer than 744,
    # each naming the point.
    "IP_UK_SEC": SecSpec(
        twin="IP_UK_S",
        column_map={"claim_duration_months": None},
        duration_of=_ip_duration,
        derived=((1, 12), (1, 60), (1, 359), (2, 24), (5, 6), (7, 12), (4, 13), (6, 118),
                 (3, 30)),
        future=((4, 13),),
        state=_IP_STATE,
        twin_state=_IP_TWIN_STATE,
        exempt=frozenset({"claim_duration_months", "sick_cohorts", "claim_rate_vectors"}),
        companions={"inforce_cohorts_sec.csv": _ip_cohorts},
        derived_refs={(1, 40): {"rpi_rate": 0.05}, (4, 30): {"rpi_rate": 0.12}},
        twin_arg_map=_ip_claims_total,
        c4_also=_ip_c4_also,
    ),
    # WP's state is eight columns per policy (_WP_STATE above), with no companion: the asset
    # share, the units and the unit price, the endowment's attaching bonus, the smoothed
    # payout and the bonus rate of the year under way, S's columns of those names under D6's
    # (units, attaching_bonus and bonus_rate become units_init, attaching_bonus_init and
    # bonus_rate_init), and the two cumulants S restarts at 0 where its frame opens, the
    # guarantee charges taken and the smoothing account.  pols_if_init becomes policy_count
    # (the default), and duration_inforce, S's elapsed policy years, is dropped for
    # duration_mth, 60 on S's bonds 1 to 4 and 240 on its endowment 6, whose twins are T2's
    # in-force twins.  S's point 7, the down scenario's bond issued at the valuation date
    # with the withdrawal election, is the bond variant the future row and T1 on a bond
    # need (UKLIB-SEC-PLAN.md §6.5): S's other new business is the endowment, which the
    # product closes to new business.  The derived rows reach the product's months on both
    # cells: the bond's declaration in month 0, 71; the down scenario as its market value
    # reduction turns on, 68, the smoothing cap's floor binding, as its corridor's ceiling
    # binds, 92, on its guarantee date, 119, the encashment in month 0, and with its asset
    # share floored at 0, 242, its payout 0 with it; the 5% bond in a month its charge cap
    # binds, 487; the withdrawing bond in its last month, 402, a one-row frame ended by
    # forced encashment; the endowment at its first declaration, 11, and at maturity, 299,
    # a one-row frame; the worked example's bond at the limiting age, 779, a one-row frame;
    # and the bond variant past its charge cap, 100, its charges stopped at 88.  The future
    # row is the bond variant issued 13 months after the valuation date: more than a year
    # on and off a valuation anniversary, so that the months before issue read policy years
    # -1 and 0, where a missing guard would show.  T2's splice grid is built from this spec
    # in a temporary table, not committed.
    #
    # And five rows S reaches only under References of their own (derived_refs), since at
    # S's References each history is what today's References rebuild, and C2 would freeze
    # no path that reads a column rather than a Reference.  The cumulants under the -15%
    # and +5% cells: the bond variant at 60 and the 5% bond at 300, each from S under a
    # guarantee charge of 0.2%, twice today's, so that the variant's charges stop at 62
    # where today's would at 88, and the 5% bond's at 207 where today's would at 487.  The
    # bond and the endowment at 150 from S under the bonus rule, its unit price 1.48623 and
    # its guarantee 22,091.61 where the rates held level give 1.268242 and 23,912.36, and the
    # rate the rule declared at the last declaration before 150, at policy month 143, 5.66%
    # and 0.62%, from which the SEC model's own declarations start (D6).  And the worked
    # example's bond at 156
    # from S under a smoothing cap of 5%, its payout held below its asset share and its
    # smoothing account run below 0.  At the shipped References the committed model projects
    # each from that history at today's.
    #
    # T1 holds on WP at any count: S charges no acquisition expense, and every flow is the
    # count times a per-policy amount.  It skips four S cells besides the default three:
    #   proj_start: S's first projected month on the policy clock, 60 on S's bonds in force.
    #     Every SEC frame opens at t = 0 (D3), which the conventions assert.
    #   duration_inforce: S's elapsed policy years, which duration_mth replaces (D6).
    #   attaching_bonus: S's accessor of the endowment's bonuses at its frame's opening,
    #     which attaching_bonus_init replaces, reading the same column renamed.
    #   fund_exhaust_mth: S returns 0 where a bond's units never run out, which on the
    #     valuation clock is a real month; SEC returns a month past cover, so the two differ
    #     on every point that never exhausts, the endowment among them.  Where the units do
    #     run out, on point 7, both return the policy month, 267;
    #     test_with_profits_uk_sec.py compares it there and holds the new "never".
    # At stage EC (M14) a fifth: guarantee_years, S's tuple of the guarantee dates' policy
    # years, which no C type holds, gives way to is_guarantee_year(y), the one reader of
    # Data's flag array by point and policy year; is_guarantee_date and guarantee_imminent,
    # which read it, are compared at every month.  S's timings and kinds are SEC's int
    # codes, BEF_NB to AFT_DECR and BEF_PREM to AFT_MC for the count's and the asset
    # share's timings, DEATH to MATURITY for the kinds, which codes maps, and S's
    # claims(t, None) keys, the kind=None total its net_cf caches, are SEC's code ALL: the
    # spec's twin_arg_map, _wp_claims_total, maps None to "ALL", and codes maps it and the
    # rest.  S's label accessors stay S's, called by reporting and T1 alone, sex() now
    # refusing any value but its codes as chassis() and tax_basis() refuse theirs: each
    # returns the column of its own name.
    #
    # Phase 2 sizes its caches from the shipped References and table (spec_sec.py holds
    # each derivation):
    #   t 0..1,357: a bond issued at issue_age_min, 18, to 121, the largest omega_age
    #     proj_len() accepts on the shipped table, a year past its last age, or an
    #     endowment maturing there, a cover of 1,236 months, issued future_horizon_mth, 120
    #     months, after the valuation date: a frame of 1,356 months, t 0..1,355, its month
    #     after, and the roll-forward's t + 1 there.  The exhaustion search reads the units
    #     in the months of cover to month 1,356 alone;
    #   y 1..104: the policy years whose openings the eight blocked chains read, 2 to 103,
    #     and the guarantee year the longest cover's last month waits for, 104.
    # proj_len() refuses an issue age below issue_age_min, an omega_age past the table, a
    # bond issued at or past omega_age, an endowment maturing past it, and a policy at or
    # past the end of cover, each naming the point; and, by point, in both engines, a cover
    # longer than 1,236 months and a frame longer than 1,356, the two bounds the caches
    # hold, each Reference keeping its in-force domain.
    "WP_UK_SEC": SecSpec(
        twin="WP_UK_S",
        column_map={"duration_inforce": None, "units": "units_init",
                    "attaching_bonus": "attaching_bonus_init",
                    "bonus_rate": "bonus_rate_init"},
        duration_of=lambda row: 12 * int(row["duration_inforce"]),
        derived=((1, 71), (2, 68), (2, 92), (2, 119), (2, 242), (3, 487), (4, 402),
                 (5, 11), (5, 299), (1, 779), (7, 100)),
        future=((7, 13),),
        state=_WP_STATE,
        twin_state=_WP_STATE,
        exempt=frozenset({"proj_start", "duration_inforce", "attaching_bonus",
                          "fund_exhaust_mth", "guarantee_years"}),
        derived_refs={(7, 60): {"guar_charge_rate_base": 0.002},
                      (3, 300): {"guar_charge_rate_base": 0.002},
                      (1, 150): {"bonus_rule_on": True},
                      (5, 150): {"bonus_rule_on": True},
                      (1, 156): {"smooth_cap": 0.05}},
        twin_arg_map=_wp_claims_total,
        c4_also=_wp_c4_also,
    ),
}

# <<< product specs


def _derived_policy_id(policy_id, d):
    return f"{policy_id}-M{d}"


def _future_policy_id(policy_id, k):
    return f"{policy_id}-F{k}"


def _derived_provenance(point_id, policy_id, d):
    return f"S point {point_id} ({policy_id}) restated in force at S month {d}"


def _future_provenance(point_id, policy_id, k):
    months = "month" if k == 1 else "months"
    return f"S point {point_id} ({policy_id}) issued {k} {months} after the valuation date"


def _sec_columns(spec, s_table, rename, added=()):
    """The SEC table's columns, in order.

    S's columns in S's order, renamed or dropped by ``rename``; then ``policy_count`` and
    ``duration_mth``, each where S has no column of that name; then the state columns S
    lacks, in the order the spec names them: ``added``, those ``model_state`` gave, then
    ``twin_state``'s, ``state``'s and ``future_state``'s; then the generator's own columns,
    :func:`generated_columns`; and ``provenance`` last, where the S table has one, as every
    table in the library keeps it.
    """
    columns = [rename.get(c, c) for c in ["point_id", *s_table.columns]]
    columns = [c for c in columns if c is not None]
    provenance = "provenance" in columns
    if provenance:
        columns.remove("provenance")
    for c in ("policy_count", "duration_mth", *added, *spec.twin_state, *spec.state,
              *spec.future_state):
        if c not in columns:
            columns.append(c)
    for c in (*GENERATED_COLUMNS, SOURCE_REFS):
        if c in columns:
            raise ValueError(f"{spec.twin}'s table has a {c!r} column, which the generator "
                             f"writes itself")
    columns += generated_columns(spec)
    if provenance:
        columns.append("provenance")
    if len(set(columns)) != len(columns):
        dupes = sorted({c for c in columns if columns.count(c) > 1})
        raise ValueError(f"column_map gives two columns one name: {dupes}")
    return columns


def _model_state(spec, s_model):
    """The columns ``spec.model_state`` gives for ``s_model``, checked; ``{}`` if none."""
    if spec.model_state is None:
        return {}
    added = dict(spec.model_state(s_model))
    clash = sorted(set(added) & (_RESERVED | {"policy_count"}))
    if clash:
        raise ValueError(f"model_state may not set {clash}: the generator owns them")
    twice = sorted(set(added) & (set(spec.state) | set(spec.twin_state)))
    if twice:
        raise ValueError(f"model_state sets {twice}, which state or twin_state sets too")
    return added


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
        ``d``; and then ``model_state`` and ``state`` set the opening state.  ``d`` must
        fall inside S's frame, after the twin's own entry month.
    future rows, for each ``(p, k)``
        the twin of new-business point ``p``, issued ``k`` months after the valuation
        date: ``duration_mth`` and ``source_mth`` are ``-k``, and the count is S's; then
        ``future_state`` sets the columns it names.
    derived rows under References of their own, for each ``(p, d)`` of ``derived_refs``
        made as a derived row is, from S run under the row's References: each is set on
        S's ``Projection`` before the row is read, and restored after it in a ``finally``,
        whatever the row raised.  Setting a Reference drops every ItemSpace of S's
        ``Projection`` and every value they hold, each made afresh when next asked, so
        these rows are read after every other, and written after them, so that adding one
        renumbers no row before it.  A caller that swept S, to spare this function
        projecting it, sweeps it again.

    Derived, future and ``derived_refs`` rows take fresh ``point_id`` s after the largest
    S one, in that order and each in the order the spec gives, so the numbering is fixed
    by the spec, never by a hash or a filesystem.  Their ``policy_id`` is composed from S's
    and the month (``TL-000001-M120``, ``TL-000001-F3``), and where the S table has a
    ``provenance`` column theirs is composed the same way, citing S's point and policy and
    the month, and for a ``derived_refs`` row each Reference and its value.  A
    ``derived_refs`` row names its References in ``source_refs`` too, as
    :func:`_reference_settings` describes them, a column the table carries only where the
    spec has such rows, blank on every other row (:func:`generated_columns`), so that the
    table records them whether or not S's has a ``provenance``.  Every other text cell is
    copied from S.  That is D8's rule under ``CLAUDE.md``: the generator adds no name, and
    a reworded S cell reaches the SEC table through T6.

    Returns ``(table, companions)``: the table on a default index, ``point_id`` its first
    column, exactly as the file is written; and ``{filename: DataFrame}`` from the spec's
    companion builders.  Each builder is given the rows read from S as it ships, and then
    each ``derived_refs`` row alone, under that row's References, set on S's
    ``Projection`` and restored after it in a ``finally`` as for the row itself; its
    frames are joined in that order, an empty one left out, on a default index.  So a
    companion gives each row the state of the run the row was read from.  Joined, the
    frames must hold no row twice, so each builder must be row-local: every row it writes
    carries the ``point_id`` of a row it was given (:func:`_check_row_local`).  A builder
    that writes rows of its own on every call, as uslib's re-based scenario sets write
    every scenario, would write them again for each ``derived_refs`` row, and is refused,
    by its name, rather than joined.  A spec with no ``derived_refs`` calls each builder
    once, on the whole table, as it always has, and holds it to nothing more.

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
    added = _model_state(spec, s_model)
    columns = _sec_columns(spec, s_table, rename, added)
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
        for column, extract in {**added, **spec.twin_state}.items():
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
        for column, extract in {**added, **spec.state}.items():
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
        for column, extract in spec.future_state.items():
            row[column] = extract(projs[p], k)
        row.update(row_kind="future", source_policy_id=twin["policy_id"], source_mth=-k)
        rows.append(row)
    space = s_model.Projection
    for (p, d), refs in spec.derived_refs.items():
        twin_of(p, "derived_refs")
        unknown = [name for name in refs if name not in space.refs]
        if unknown:
            raise ValueError(f"derived_refs row ({p}, {d}) sets {unknown}, which "
                             f"{spec.twin}'s Projection has no Reference of")
    for (p, d), refs in spec.derived_refs.items():
        twin, shipped = twins[p], {name: space.refs[name] for name in refs}
        try:
            for name, value in refs.items():
                setattr(space, name, value)
            proj, source = space[p], twin["source_mth"]
            if not source < d < proj.proj_len():
                raise ValueError(
                    f"derived_refs row ({p}, {d}), under {_reference_settings(refs)}: d "
                    f"must fall after the twin's entry month ({source}) and inside S's "
                    f"frame, which ends at {proj.proj_len() - 1}")
            row = dict(twin, point_id=next(fresh),
                       policy_id=_derived_policy_id(twin["policy_id"], d),
                       policy_count=proj.pols_if(d),
                       duration_mth=twin["duration_mth"] + d - source)
            if provenance:
                row["provenance"] = (f"{_derived_provenance(p, twin['policy_id'], d)} "
                                     f"under {_reference_settings(refs)}")
            for column, extract in {**added, **spec.state}.items():
                row[column] = extract(proj, d)
        finally:
            for name, value in shipped.items():
                setattr(space, name, value)
        row.update(row_kind="derived", source_policy_id=twin["policy_id"], source_mth=d)
        row[SOURCE_REFS] = _reference_settings(refs)
        rows.append(row)

    table = pd.DataFrame(rows, columns=columns)
    for key in ("point_id", "policy_id"):
        dupes = sorted(table.loc[table[key].duplicated(), key].astype(str))
        if dupes:
            raise ValueError(f"the SEC table repeats {key} {dupes}; is a (point, month) "
                             f"pair listed twice?")
    companions = {}
    shipped = len(table) - len(spec.derived_refs)
    for filename, build in spec.companions.items():
        parts = [build(s_model, table.iloc[:shipped].copy())]
        for i, refs in enumerate(spec.derived_refs.values()):
            saved = {name: space.refs[name] for name in refs}
            try:
                for name, value in refs.items():
                    setattr(space, name, value)
                parts.append(build(s_model, table.iloc[[shipped + i]].copy()))
            finally:
                for name, value in saved.items():
                    setattr(space, name, value)
        for frame in parts:
            if not isinstance(frame, pd.DataFrame):
                raise TypeError(f"the builder of {filename} returned a "
                                f"{type(frame).__name__}, not a DataFrame")
        if spec.derived_refs:
            _check_row_local(filename, build, parts, table, shipped)
        kept = [frame for frame in parts if len(frame)]
        frame = parts[0]
        if len(parts) > 1 and kept:
            frame = pd.concat(kept, ignore_index=True)
        companions[filename] = frame
    return table, companions


def _check_row_local(filename, build, parts, table, shipped):
    """Refuse a companion builder that writes rows beyond those it is given.

    ``parts`` are the frames ``build`` wrote for ``filename``: the first for the rows read
    from S as it ships, ``table.iloc[:shipped]``, then one for each ``derived_refs`` row
    alone, in the table's order (:func:`build_sec_table`).  Joined, they must hold no row
    twice.  So each row of each frame must carry a ``point_id``, and it must be one of the
    rows that frame was built for: the frames' rows then belong to different points.  A
    builder that writes rows of its own on every call, keyed by anything else or by points
    it was not given, would write them once more for each ``derived_refs`` row; it raises
    ``ValueError``, naming the file, the builder and the rows at fault.  An empty frame
    holds nothing to repeat.
    """
    name = getattr(build, "__name__", repr(build))
    given = [table.iloc[:shipped]] + [table.iloc[[i]] for i in range(shipped, len(table))]
    for frame, rows in zip(parts, given):
        if not len(frame):
            continue
        if "point_id" not in frame.columns:
            raise ValueError(
                f"{filename}: its builder {name} is not row-local: it wrote rows without "
                f"a point_id.  A spec with derived_refs builds each such row's companion "
                f"rows from that row alone, under its References, and joins them to the "
                f"rest, so a builder must write rows only for the point_ids it is given; "
                f"one that writes rows of its own on every call would write them again "
                f"for each derived_refs row")
        stray = sorted(set(frame["point_id"].tolist()) - set(rows["point_id"].tolist()))
        if stray:
            raise ValueError(
                f"{filename}: its builder {name} is not row-local: given {len(rows)} "
                f"rows, it wrote rows of point_id {stray}, which it was not given.  A spec "
                f"with derived_refs builds each such row's companion rows from that row "
                f"alone, under its References, and joins them to the rest, so a builder "
                f"must write rows only for the point_ids it is given")


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


# ---------------------------------------------------------------------------
# C2 -- the Phase 1 fingerprint


FINGERPRINT_REPORTS = ("result_cf", "result_pols")
"""The reports a fingerprint freezes: the cash flows, and the counts behind them (§5.4).

``result_pols`` carries what no ``result_cf`` column shows, the decrements one by one and
the expiries, and it is cheap, so it is frozen beside the cash flows.
"""

FINGERPRINT_RTOL = 1e-12
"""C2's tolerance: relative, floored at the same fraction of the column's own magnitude."""


def fingerprint_months(rows):
    """The months a fingerprint holds a column's values at, for a frame of ``rows`` months.

    The first and the last month of the frame and the three quartiles between them,
    ``(k * (rows - 1)) // 4`` for ``k = 0 .. 4``, without repeats: ``(0, 179, 359, 539,
    719)`` for a 720-month frame, ``(0,)`` for a one-month frame.  The rule knows nothing
    of the product, so every SEC model freezes its points the same way.
    """
    return tuple(sorted({(k * (rows - 1)) // 4 for k in range(5)}))


def _report_print(df, months):
    """``{column: (sum, scale, values)}`` for one report frame, at ``months``."""
    return {column: (float(df[column].sum()), float(df[column].abs().max()),
                     tuple(float(df[column].iloc[t]) for t in months))
            for column in df.columns}


def _point_frames(model):
    """``(label, {report: frame})`` for every model point of ``model``, in table order."""
    from uk_registry import point_keys, projection
    labels = model.Data.model_point_table().index
    for key, label in zip(point_keys(model), labels):
        proj = projection(model, key)
        yield int(label), {name: proj.cells[name]() for name in FINGERPRINT_REPORTS}


def fingerprint(model):
    """What ``model`` computes on each model point, in brief: ``{point_id: {...}}`` (§5.4).

    Each point is keyed by its table label, which names the same point whether
    ``Projection`` is indexed by label or by position.  Its entry holds ``"rows"``, the
    frame's length; ``"months"``, :func:`fingerprint_months` of it; and, for each report
    of :data:`FINGERPRINT_REPORTS`, ``{column: (sum, scale, values)}`` in the report's
    column order: the column's sum over the frame, its largest absolute value, which is the
    magnitude its tolerance is measured against, and its values at the months, each a
    Python float.  A report must be indexed ``t = 0 .. rows - 1``, as every SEC frame is.
    """
    out = {}
    for label, frames in _point_frames(model):
        rows = len(frames[FINGERPRINT_REPORTS[0]])
        months = fingerprint_months(rows)
        entry = {"rows": rows, "months": months}
        for name, df in frames.items():
            if list(df.index) != list(range(rows)):
                raise ValueError(f"{model.name} point {label}: {name}() is not indexed "
                                 f"t = 0 .. {rows - 1}")
            entry[name] = _report_print(df, months)
        out[label] = entry
    return out


def _wrapped(text, indent, width=92):
    """``text`` wrapped at its spaces alone, within ``width`` columns, under ``indent``.

    Never inside a word: ``textwrap`` would break ``1.99e-05`` at its hyphen, and the
    literal would no longer read back as the number.
    """
    import textwrap
    return textwrap.wrap(text, width=width, initial_indent=indent,
                         subsequent_indent=indent, break_long_words=False,
                         break_on_hyphens=False)


def fingerprint_text(name, frozen):
    """``frozen`` written out as the literal a product module holds, its markers included.

    One entry per point, one item per column: ``(sum, scale, (values at the months))``,
    the values wrapped beneath within the house's 92 columns.  Every float is its shortest
    ``repr``, which Python reads back as the same double, so the literal is the freeze
    exactly; that is checked here, by reading the text back, before it is returned.
    """
    out = [f"# BEGIN generated fingerprint: {name} -- tools/gen_sec_fingerprint.py",
           "FINGERPRINT = {"]
    for label, entry in frozen.items():
        out.append(f"    {label}: {{\"rows\": {entry['rows']}, "
                   f"\"months\": {entry['months']!r},")
        for report in (k for k in entry if k not in ("rows", "months")):
            out.append(f"        \"{report}\": {{")
            for column, (total, scale, values) in entry[report].items():
                out.append(f"            \"{column}\": ({total!r}, {scale!r}, (")
                text = ", ".join(repr(v) for v in values)
                out += _wrapped(text + (",)),"  if len(values) == 1 else ")),"), " " * 16)
            out.append("        },")
        out.append("    },")
    out += ["}", f"# END generated fingerprint: {name}"]
    text = "\n".join(out) + "\n"
    long = [line for line in out if len(line) > 92]
    namespace = {}
    exec(text, namespace)                       # the text this function has just written
    if long or namespace["FINGERPRINT"] != frozen:
        raise ValueError(f"the fingerprint of {name} does not write out exactly: "
                         f"{len(long)} lines over 92 columns, or a value that reads back "
                         f"as another")
    return text


def _fp_close(a, b, floor):
    """C2's comparison: within :data:`FINGERPRINT_RTOL` of the larger, or of ``floor``."""
    return abs(a - b) <= FINGERPRINT_RTOL * max(abs(a), abs(b), floor)


def fingerprint_mismatches(frozen, model):
    """C2: where ``model`` departs from the fingerprint ``frozen``, a line per departure.

    The same points in the same order, frames of the same length, and the same reports
    with the same columns in the same order, exactly.  Then each column, at the months the
    freeze names: its values, each held to ``1e-12 * scale``, its scale held the same way,
    so that a spike in a month the freeze does not name is still seen, and its sum to
    ``1e-12 * rows * scale``; and each to 1e-12 of the larger of the two where that is
    larger still (:data:`FINGERPRINT_RTOL`).  So a frozen zero is compared as finely as
    the column's own magnitude allows and no finer, and a column whose scale is 0, such as
    the conversion credits at the shipped zero conversion rates, must stay exactly 0.

    Returns readable lines, empty when the model reproduces the freeze.
    """
    lines = []
    found = list(_point_frames(model))
    if [label for label, _ in found] != list(frozen):
        return [f"points: frozen {list(frozen)}, now {[label for label, _ in found]}"]
    for label, frames in found:
        entry = frozen[label]
        rows = len(frames[FINGERPRINT_REPORTS[0]])
        if rows != entry["rows"]:
            lines.append(f"point {label}: {rows} rows, frozen {entry['rows']}")
            continue
        for report in (k for k in entry if k not in ("rows", "months")):
            df = frames.get(report)
            if df is None or list(df.columns) != list(entry[report]):
                got = None if df is None else list(df.columns)
                lines.append(f"point {label}: {report} columns {got}, frozen "
                             f"{list(entry[report])}")
                continue
            if list(df.index) != list(range(rows)):
                lines.append(f"point {label}: {report} is not indexed t = 0 .. {rows - 1}")
                continue
            now = _report_print(df, entry["months"])
            for column, (total, scale, values) in entry[report].items():
                where = f"point {label}: {report}[{column!r}]"
                n_total, n_scale, n_values = now[column]
                if not _fp_close(total, n_total, rows * scale):
                    lines.append(f"{where} sums to {n_total!r}, frozen {total!r}")
                if not _fp_close(scale, n_scale, scale):
                    lines.append(f"{where} reaches {n_scale!r}, frozen {scale!r}")
                for t, want, have in zip(entry["months"], values, n_values):
                    if not _fp_close(want, have, scale):
                        lines.append(f"{where} at t={t} is {have!r}, frozen {want!r}")
    return lines


# ---------------------------------------------------------------------------
# Compiling an SEC model, for the compile tests (Phase 2, D12, D13)
#
# A compile test builds the model with the library's build_sec_cy.py into a temporary
# directory, never into the tree (D12), and runs the compiled package in a child process
# only: a compiled model that overflows the C stack takes down the child and not the
# session, and on Windows a .pyd that a process holds open cannot be deleted.


def _tool():
    """The library's build tool, ``build_sec_cy.py`` at its root, beside ``tests/``.

    The library carries it, so lifelib has it and so does every ``lifelib.create()`` copy,
    wherever it is put, as each product's ``run_sec.py`` finds it there.
    """
    return pathlib.Path(__file__).resolve().parents[1] / "build_sec_cy.py"


def cython_missing():
    """What this machine lacks to compile a model, or ``None`` when it lacks nothing.

    The library's build tool, which only a copy that left it behind lacks; modelx-cython,
    which no model requires, because it needs a C compiler; and, on POSIX, the C
    compiler setuptools would run, ``CC`` or the one the interpreter was built with, on
    ``PATH``.  On Windows setuptools finds MSVC through vswhere at build time, and
    ``cl.exe`` is on no ``PATH`` outside a developer prompt, so no probe is made there: a
    missing MSVC fails the build instead, and the error quotes setuptools saying so.
    """
    import importlib.util
    import os
    import shlex
    import shutil as _shutil
    import sysconfig
    if not _tool().is_file():
        return "the library's build_sec_cy.py is absent, which it carries at its root"
    if importlib.util.find_spec("modelx_cython") is None:
        return ("modelx-cython is not installed, and it needs a C compiler: pip install "
                "modelx-cython")
    if os.name == "posix":
        command = os.environ.get("CC") or sysconfig.get_config_var("CC") or "cc"
        compiler = (shlex.split(command) or ["cc"])[0]
        if _shutil.which(compiler) is None:
            return f"no C compiler: setuptools would run {compiler!r}, which is not on PATH"
    return None


def require_cython():
    """The library's ``build_sec_cy.py`` as a module, or a skip, which
    ``UKLIB_REQUIRE_CYTHON=1`` turns into a failure.

    The compile tests skip where :func:`cython_missing` finds something missing, so the
    ``test`` CI job and lifelib's own bare ``pytest`` stay green without modelx-cython or a
    compiler (D13).  The ``cython_uk`` job installs both and sets
    ``UKLIB_REQUIRE_CYTHON=1``, and there a skip would be a green run that compiled
    nothing, so it fails instead.
    ``pytest`` is imported here, not at the top, because ``tools/gen_sec_points.py``
    imports this module without it.
    """
    import importlib.util
    import os
    import pytest
    missing = cython_missing()
    if missing is not None:
        if os.environ.get("UKLIB_REQUIRE_CYTHON") == "1":
            pytest.fail(f"UKLIB_REQUIRE_CYTHON=1 forbids a skip, and {missing}")
        pytest.skip(missing)
    spec = importlib.util.spec_from_file_location("build_sec_cy", _tool())
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# The cython_uk CI job's shards (D13, decided at M16)
#
# The job runs one shard to a leg, chosen by UKLIB_CYTHON_SHARD, so that no leg compiles
# every model: "toolchain", test_cython_toolchain_uk.py and any compile test tied to no one
# SEC model, and one shard for each SEC model at stage "EC", its product module's compile
# tests with its cases of test_compiled_conventions_uk.py, in one session, so that it
# compiles once.  conftest.py deselects the compile tests outside the shard.

CYTHON_SHARD = "UKLIB_CYTHON_SHARD"
TOOLCHAIN_SHARD = "toolchain"


def cython_shards():
    """The ``cython_uk`` job's shards, ``{shard: model}``: ``"toolchain"``, to ``None``,
    first.

    Then, in the registry's order, the product directory of each SEC model at stage
    ``"EC"``, to the model: ``"term_assurance"`` to ``"Term_UK_SEC"``.  The directory names
    the product's test module, ``test_term_assurance_uk_sec.py``, as it does in the
    ``sec_uk`` job's matrix.  Read from the registry, so a model gains its shard in the
    commit that moves it to stage ``"EC"``, and ``test_compiled_conventions_uk.py`` holds
    the workflow's matrix to these.
    """
    from uk_registry import is_sec, meta
    shards = {TOOLCHAIN_SHARD: None}
    for name in MODELS:
        if is_sec(name) and meta(name).get("stage") == "EC":
            shards[model_path(name).parent.name] = name
    return shards


def cython_shard(item, shards):
    """The shard among ``shards`` (:func:`cython_shards`) that runs the test ``item``.

    A test parametrized over a stage-``"EC"`` model is that model's, as each case of
    ``test_compiled_conventions_uk.py`` is; else a test in a shard's product module,
    ``test_<shard>_uk_sec.py``, is that shard's; and every other is ``"toolchain"``'s.  So
    no compile test falls outside every shard: one tied to no model, or to a model not yet
    at stage ``"EC"``, runs in the toolchain's.
    """
    by_model = {model: shard for shard, model in shards.items() if model is not None}
    params = getattr(item, "callspec", None)
    for value in (params.params.values() if params is not None else ()):
        if isinstance(value, str) and value in by_model:
            return by_model[value]
    found = re.fullmatch(r"test_(\w+)_uk_sec\.py", item.path.name)
    if found and found.group(1) in by_model.values():
        return found.group(1)
    return TOOLCHAIN_SHARD


@dataclasses.dataclass(frozen=True)
class Build:
    """One compiled SEC model: its name, the directory it was built in, its compiled
    package, ``<name>_nomx_cy``, and the text of that package's ``_mx_classes.pxd``, the
    declarations a typing guard reads."""
    name: str
    out: pathlib.Path
    package: pathlib.Path
    pxd: str


class SecBuilds:
    """The SEC models compiled in this test session, each once: ``builds(name)``.

    Each is built by the library's ``build_sec_cy.py`` into a directory of the session's
    own (``tmp_path_factory.mktemp``), from the committed model, sample and spec, and kept
    as a :class:`Build` for the rest of the session.  A build that fails is kept too, and
    its error raised again to every test that asks for it, so a broken build reports itself
    in each test that needs it without being compiled again.  Without the toolchain,
    :func:`require_cython` skips, or fails in the ``cython_uk`` job.
    ``conftest.sec_build`` is the session's one instance.
    """

    def __init__(self, tmp_path_factory):
        self._factory = tmp_path_factory
        self._done = {}

    def __call__(self, name):
        if name not in self._done:
            tool = require_cython()
            try:
                out = self._factory.mktemp(name)
                package = tool.build(model_path(name).parent, model=name, out=out)
                pxd = (package / "_mx_classes.pxd").read_text(encoding="utf-8")
                self._done[name] = Build(name, out, package, pxd)
            except Exception as err:            # kept, and raised to every asker
                self._done[name] = err
        built = self._done[name]
        if isinstance(built, Exception):
            raise built
        return built


def compiled_case(build, dest, *, model_points=None, model_point_file=None, edits=None):
    """A directory where modelx and the compiled model read the same inputs; its model.

    :func:`temp_inputs` copies the model and its CSVs into ``dest``, with
    ``model_points`` and ``edits`` as it takes them, and the compiled package of ``build``
    is copied beside them.  The package reads the CSVs of the directory that holds it
    (USLIB-SEC-PLAN.md F6), so it reads the copies, as the model folder returned does.
    ``model_point_file`` defaults to the SEC table's name in the model's spec.
    """
    if model_point_file is None:
        spec = SEC_SPECS.get(build.name)
        model_point_file = (spec.model_point_file if spec is not None
                            else "model_point_table_sec.csv")
    folder = temp_inputs(dest, model_path(build.name), model_points=model_points,
                         model_point_file=model_point_file, edits=edits)
    shutil.copytree(build.package, pathlib.Path(dest) / build.package.name,
                    ignore=shutil.ignore_patterns("__pycache__", "*.c", "*.html"))
    return folder


COMPILED_RUNNER = '''\
"""Run calls on a compiled SEC package in a child process, and pickle what they returned.

    python runner.py <case dir> <package> <job> <result> <stack KiB> <thread | main>
"""
import ctypes
import importlib
import importlib.machinery
import os
import pickle
import sys
import threading

import numpy as np

case, package, job_path, result_path, kib, where = sys.argv[1:7]
sys.path.insert(0, case)
with open(job_path, "rb") as f:
    job = pickle.load(f)
model = importlib.import_module(package).mx_model
for ref, value in job["refs"].items():
    if ref.startswith("Data."):
        setattr(model.Data, ref[len("Data."):], value)
    else:
        setattr(model.Projection, ref, value)

# Whether each space's class came from an extension module: a package whose build lost one
# still imports, from the translated .py beside it, and computes the same numbers.
suffixes = tuple(importlib.machinery.EXTENSION_SUFFIXES)
compiled = {type(space).__name__: sys.modules[type(space).__module__].__file__.endswith(
    suffixes) for space in (model.Data, model.Projection)}
values, stack = {}, {}


def reservation():
    """The calling thread's stack in bytes, as reserved: from Windows, or from glibc's
    pthread_getattr_np; None elsewhere, as on macOS."""
    if os.name == "nt":
        low, high = ctypes.c_size_t(), ctypes.c_size_t()
        ctypes.windll.kernel32.GetCurrentThreadStackLimits(ctypes.byref(low),
                                                            ctypes.byref(high))
        return high.value - low.value
    try:
        libc = ctypes.CDLL(None)
        libc.pthread_self.restype = ctypes.c_ulong
        attr, size = ctypes.create_string_buffer(256), ctypes.c_size_t()
        if libc.pthread_getattr_np(ctypes.c_ulong(libc.pthread_self()), attr):
            return None
        libc.pthread_attr_getstacksize(attr, ctypes.byref(size))
        libc.pthread_attr_destroy(attr)
        return size.value
    except (AttributeError, OSError):       # no glibc
        return None


def called(call):
    """``("ok", value)`` or ``("raised", "Type: message")``, a memoryview as an array."""
    try:
        value = call()
    except Exception as err:
        return ("raised", f"{type(err).__name__}: {err}")
    if type(value).__name__ == "_memoryviewslice":
        value = np.asarray(value)
    return ("ok", value)


def run():
    stack["reserved"] = reservation()
    for idx, calls in job["calls"].items():
        proj = model.Projection[idx]
        values[idx] = [called(lambda: getattr(proj, name)(*args)) for name, args in calls]
        del proj
        del model.Projection[idx]
    for name in job.get("data", ()):
        data[name] = called(getattr(model.Data, name))


def on_stack(kib):
    """Run :func:`run` in a thread whose stack is ``kib`` KiB, reserved.

    The reservation is what bounds a recursion.  On Windows ``threading.stack_size`` sets
    the stack a thread commits, and the thread reserves the executable's own, 2,000,000
    bytes for python.exe, so the thread is made by CreateThread with
    STACK_SIZE_PARAM_IS_A_RESERVATION instead.
    """
    if os.name != "nt":
        threading.stack_size(kib * 1024)
        thread = threading.Thread(target=run)
        thread.start()
        thread.join()
        return
    from ctypes import wintypes
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    start = ctypes.WINFUNCTYPE(wintypes.DWORD, wintypes.LPVOID)
    kernel32.CreateThread.argtypes = (wintypes.LPVOID, ctypes.c_size_t, start,
                                      wintypes.LPVOID, wintypes.DWORD, wintypes.LPDWORD)
    kernel32.CreateThread.restype = wintypes.HANDLE
    kernel32.WaitForSingleObject.argtypes = (wintypes.HANDLE, wintypes.DWORD)
    kernel32.CloseHandle.argtypes = (wintypes.HANDLE,)
    failed = []

    def body(_):
        try:
            run()
        except BaseException as err:
            failed.append(err)
        return 0

    entry = start(body)
    handle = kernel32.CreateThread(None, kib * 1024, entry, None, 0x00010000, None)
    if not handle:
        raise ctypes.WinError(ctypes.get_last_error())
    kernel32.WaitForSingleObject(handle, 0xFFFFFFFF)
    kernel32.CloseHandle(handle)
    if failed:
        raise failed[0]


data = {}
if where == "main":
    run()
else:
    on_stack(int(kib))
with open(result_path, "wb") as f:
    pickle.dump({"compiled": compiled, "values": values, "data": data, "stack": stack}, f)
'''
"""The child that :func:`run_compiled` starts: it imports the compiled package, sets the
References, and makes the calls, in a thread of the stack asked for or on its main
thread."""


def run_compiled(case_dir, package, job, *, stack_kib=1024, main_thread=False,
                 timeout=600):
    """Run ``job`` on the compiled ``package`` in ``case_dir``, in a child; what it found.

    ``job`` is ``{"refs": {name: value}, "calls": {idx: [(cell, args), ...]}}``, and may
    name ``"data"``, a list of ``Data`` cells to read once the calls are made.  The child
    sets each Reference on the base ``Projection``, or one named ``"Data.<name>"`` on
    ``Data``, before any ItemSpace is made or any cell computed, then makes each point's
    calls in order, on ``Projection[idx]``, in a thread whose stack is ``stack_kib`` KiB or,
    with ``main_thread``, on its main thread, which is what ``run_sec.py --cython`` runs on.
    A compiled chain of cells runs on the C stack, which the interpreter's recursion limit
    does not count (F7).  The thread's stack is reserved at that size on every platform:
    ``threading.stack_size`` sets it on POSIX, and on Windows, where that sets only the
    stack a thread commits, the child makes the thread itself (``COMPILED_RUNNER``).

    Returns ``{"exit": code, "stderr": its last lines}``, and when the child exited 0:
    ``"compiled"``, whether each space's class came from an extension module; ``"values"``,
    ``{idx: [("ok", value) or ("raised", "Type: message"), ...]}`` in the calls' order,
    an array returned as a numpy array; ``"data"``, ``{cell: ("ok", value) or ("raised",
    ...)}`` for the ``Data`` cells named; and ``"stack"``, ``{"reserved": bytes}``, the
    stack the thread that made the calls has, read back from Windows or glibc, ``None``
    where neither tells.  A child that dies on its stack has a nonzero exit and no values.
    """
    import os
    import pickle
    import subprocess
    import sys
    import tempfile
    case_dir = pathlib.Path(case_dir)
    work = pathlib.Path(tempfile.mkdtemp(prefix="run_", dir=case_dir.parent))
    runner, job_path, result = work / "runner.py", work / "job.pickle", work / "got.pickle"
    runner.write_text(COMPILED_RUNNER, encoding="utf-8")
    job_path.write_bytes(pickle.dumps(job))
    done = subprocess.run(
        [sys.executable, "-P", str(runner), str(case_dir), package, str(job_path),
         str(result), str(stack_kib), "main" if main_thread else "thread"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        env={**os.environ, "PYTHONIOENCODING": "utf-8"}, timeout=timeout)
    found = {"exit": done.returncode, "stderr": done.stderr[-4000:]}
    if done.returncode == 0:
        found.update(pickle.loads(result.read_bytes()))
    return found


# ---------------------------------------------------------------------------
# What may stay Python (R17)


def reporting_cells(name, space):
    """The cells of SEC model ``name``'s ``Projection`` that may stay Python (R17).

    ``model_point``, every ``result_*`` report, every ``check_*`` check but the per-``t``
    ``*_resid`` cells a check reads, and the label accessors the registry entry names
    under ``"reporting"`` (:mod:`uk_registry`): cells that hand a reader a table row, text,
    a DataFrame or a verdict.  And the engine cells it names under ``"engine"``: S's cells
    of float parameters, or of no parameter returning a list, a dict or a DataFrame (M24),
    kept for a reader and for T1, which no compiled cell calls (R14).
    They are the typing guard's allowlist (:func:`typing_faults`), and no other cell may
    call one (:func:`static_faults`), so every cell a projection runs compiles to C; an
    engine cell may call another.  ``space`` is the model's ``Projection``.
    """
    from uk_registry import meta
    declared = set(meta(name).get("reporting", ())) | set(meta(name).get("engine", ()))
    return frozenset(
        cell for cell in space.cells
        if cell == "model_point" or cell.startswith("result_") or cell in declared
        or (cell.startswith("check_") and not cell.endswith("_resid")))


def engine_faults(space, declared, sized, reporting=()):
    """Where the cells an entry's ``"engine"`` names are not what R14 admits, a line each.

    Each must be a cell of ``space``, the model's ``Projection``, and none a reporting
    cell, ``reporting`` being the entry's ``"reporting"``.  Each must take a parameter
    that no ``spec_sec.py`` size names, ``sized`` holding the names it sizes, since a cell
    keyed by sized ints compiles to C and needs no admission; or take none and return
    what no C type holds, a list, a dict or a DataFrame, found by calling it on the
    space's first point, as ``DIA_US_SEC``'s ``qlac_flags`` and premium schedule do (M24).
    And no other formula of ``space`` may call one, an engine cell excepted, so that every
    cell a projection runs is C.
    """
    import ast
    import textwrap
    point = space[0] if space.parameters else space
    found = []
    for cell in declared:
        if cell not in space.cells:
            found.append(f"{cell} is not a Projection cell")
        elif cell in reporting:
            found.append(f"{cell} is a reporting cell too")
        elif not set(space.cells[cell].parameters) - sized:
            if not space.cells[cell].parameters and isinstance(
                    point.cells[cell](), (list, dict, pd.DataFrame)):
                continue
            found.append(f"{cell} takes only parameters spec_sec.py sizes, "
                         f"{space.cells[cell].parameters}, so it compiles to C")
    for name, cells in space.cells.items():
        if name in declared:
            continue
        tree = ast.parse(textwrap.dedent(cells.formula.source))
        for node in ast.walk(tree):
            if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                    and node.func.id in declared):
                found.append(f"{name} calls the engine cell {node.func.id}")
    return found


def _names_bound(node, tree):
    """The text constants a sample's loop variable ``node`` can take, or ``None``.

    ``node`` is the name a ``getattr`` call reads its attribute from, as in ``for label in
    LABELS: getattr(p, label)()``.  It is resolved through the ``for`` loop that binds it:
    over a literal tuple, list or set of text, or a module-level name assigned one; or,
    where the loop binds it first of a pair, over ``.items()`` of a dict literal, or of a
    module-level name assigned one, its keys.  Any other loop, one over names the sample
    computes, is not resolved.
    """
    import ast
    assigned = {}
    for statement in tree.body:
        if isinstance(statement, ast.Assign):
            for target in statement.targets:
                if isinstance(target, ast.Name):
                    assigned[target.id] = statement.value

    def texts(value):
        if isinstance(value, ast.Name):
            value = assigned.get(value.id)
        if isinstance(value, (ast.Tuple, ast.List, ast.Set)):
            found = [e.value for e in value.elts
                     if isinstance(e, ast.Constant) and isinstance(e.value, str)]
            return set(found) if len(found) == len(value.elts) else None
        return None

    def keys(value):
        if isinstance(value, ast.Name):
            value = assigned.get(value.id)
        if isinstance(value, ast.Dict):
            found = [k.value for k in value.keys
                     if isinstance(k, ast.Constant) and isinstance(k.value, str)]
            return set(found) if len(found) == len(value.keys) else None
        return None

    for loop in ast.walk(tree):
        if not isinstance(loop, ast.For):
            continue
        if isinstance(loop.target, ast.Name) and loop.target.id == node.id:
            if any(child is node for child in ast.walk(loop)):
                return texts(loop.iter)
        if (isinstance(loop.target, ast.Tuple) and loop.target.elts
                and isinstance(loop.target.elts[0], ast.Name)
                and loop.target.elts[0].id == node.id
                and any(child is node for child in ast.walk(loop))):
            it = loop.iter
            if (isinstance(it, ast.Call) and isinstance(it.func, ast.Attribute)
                    and it.func.attr == "items" and not it.args):
                return keys(it.func.value)
            return None
    return None


def sample_engine_faults(source, engine, parameterless=()):
    """Where a ``sample_sec.py`` calls an ``"engine"`` cell of the registry's nowhere.

    No compiled cell calls an engine cell (:func:`engine_faults`), so the sample's own
    call is the only trace mx2cy types it from: one the sample stops calling compiles with
    object parameters, and C3 still passes, since it admits an engine cell's dict cache by
    name (R14, M25).  So each cell of ``engine`` must be called in ``source``, the
    sample's code, read statically: as an attribute, ``p.bs_call(...)``, through
    ``getattr`` with its name as text, or through ``getattr`` with a loop variable that
    :func:`_names_bound` resolves to a set of names holding it.  A cell of
    ``parameterless``, the engine cells taking no parameter, is called too by a loop that
    calls ``getattr(p, name)()`` over names the sample computes, as a sample that calls
    every cell of no parameter does: such a cell returns a list, a dict or a DataFrame,
    an object traced or not.  Returns a line per cell not called.
    """
    import ast
    tree = ast.parse(source)
    parents = {child: node for node in ast.walk(tree)
               for child in ast.iter_child_nodes(node)}
    called, computed = set(), False
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if isinstance(node.func, ast.Attribute):
            called.add(node.func.attr)
        if not (isinstance(node.func, ast.Name) and node.func.id == "getattr"
                and len(node.args) >= 2):
            continue
        name = node.args[1]
        if isinstance(name, ast.Constant) and isinstance(name.value, str):
            called.add(name.value)
        elif isinstance(name, ast.Name):
            bound = _names_bound(name, tree)
            if bound is not None:
                called |= bound
            else:
                up = parents.get(node)
                if (isinstance(up, ast.Call) and up.func is node and not up.args
                        and not up.keywords):
                    computed = True
    return [f"sample_sec.py calls no engine cell {cell}(): untraced, it compiles taking "
            f"objects, which C3 admits in an engine cell (R14)"
            for cell in engine
            if cell not in called and not (computed and cell in parameterless)]


def reporting_columns_faults(entry):
    """Where a registry entry's ``"reporting_columns"`` is not what R17 lets it say (M23).

    The key says what a label accessor returns where that is not its point's column of
    the label's own name (:mod:`uk_registry`).  It is a stage-``"EC"`` key, as
    ``"reporting"`` is, a dict whose every key is a label ``"reporting"`` names, each
    mapped to one of three shapes: a column name; a non-empty dict of argument to column
    name, for a label taking one argument; or a pair of a column name and a non-empty
    dict of value to label, for a label returning the column's value through the dict.
    ``entry`` is a :func:`uk_registry.meta` dict.  Returns a line per fault.
    """
    if "reporting_columns" not in entry:
        return []
    columns = entry["reporting_columns"]
    if entry.get("stage") != "EC":
        return [f"reporting_columns is declared at stage {entry.get('stage')!r}; it widens "
                f"the compiled model's label check, and the key belongs to stage 'EC'"]
    if not (isinstance(columns, dict) and columns):
        return [f"reporting_columns is {columns!r}, not a non-empty dict of labels"]
    lines = []
    reporting = entry.get("reporting", ())
    for label, shape in columns.items():
        if label not in reporting:
            lines.append(f"reporting_columns names {label!r}, which reporting does not")
        if isinstance(shape, str):
            continue
        if isinstance(shape, dict):
            if not (shape and all(isinstance(c, str) for c in shape.values())):
                lines.append(f"reporting_columns[{label!r}] is {shape!r}, not a non-empty "
                             f"dict of argument to column")
            continue
        if (isinstance(shape, tuple) and len(shape) == 2 and isinstance(shape[0], str)
                and isinstance(shape[1], dict) and shape[1]):
            continue
        lines.append(f"reporting_columns[{label!r}] is {shape!r}: neither a column, a dict "
                     f"of argument to column, nor a pair of a column and a dict of value "
                     f"to label")
    return lines


def _label_calls(shape):
    """``[(args, column, mapping)]``: how :func:`label_faults` calls a label of ``shape``,
    its ``"reporting_columns"`` entry or its own name."""
    if isinstance(shape, dict):
        return [((arg,), column, None) for arg, column in shape.items()]
    if isinstance(shape, tuple):
        return [((), shape[0], shape[1])]
    return [((), shape, None)]


def label_faults(model, name, entry=None):
    """C5's check of the label accessors: each returns its point's column (R17), a line
    per fault.

    For each label SEC model ``name``'s registry entry names under ``"reporting"`` and
    ``model``'s ``Projection`` holds, on every point of the table: called as the entry's
    ``"reporting_columns"`` says (:func:`reporting_columns_faults`), or bare where it says
    nothing, the label must return its point's column as the table holds it, through the
    pair's dict where the shape is a pair, a value the dict lacks as it is.  Text must
    equal the column's text; a blank column, NaN, is the label's value where the label
    returns NaN, as ``SPIA_US_SEC``'s ``sex(2)`` does on a single-life point; anything else,
    a raise among them, is a fault, as is a column the table lacks.  And an entry must be
    needed: a label the entry names as a column or a pair, whose own name is also a
    column, must not return that column, its default, on every point, which would leave
    the entry stale.  ``entry`` stands in for the registry's, as a harness test's does.
    """
    from uk_registry import meta, point_keys, projection
    entry = meta(name) if entry is None else entry
    columns = entry.get("reporting_columns", {})
    labels = [cell for cell in entry.get("reporting", ()) if cell in model.Projection.cells]
    found, own, points = [], {cell: 0 for cell in columns}, 0
    table = model.Data.model_point_table()
    for key, point_id in zip(point_keys(model), table.index):
        points += 1
        proj = projection(model, key)
        row = proj.model_point()
        for cell in labels:
            for args, column, mapping in _label_calls(columns.get(cell, cell)):
                call = f"Projection.{cell}({', '.join(repr(a) for a in args)})"
                try:
                    got = proj.cells[cell](*args)
                except Exception as err:            # reported, so the scan goes on
                    found.append(f"{call} raised {_error_text(err)} at point {point_id}, "
                                 f"where the label returns the point's {column!r} column "
                                 f"(R17)")
                    continue
                if column not in row.index:
                    found.append(f"{call}: the table has no {column!r} column, which the "
                                 f"registry says it returns (R17)")
                    continue
                want = row[column]
                if mapping is not None and isinstance(want, str):
                    want = mapping.get(want, want)
                blank = (isinstance(want, float) and want != want
                         and isinstance(got, float) and got != got)
                if not ((isinstance(got, str) and got == want) or blank):
                    found.append(f"{call} returns {got!r} at point {point_id}, where the "
                                 f"label returns the point's {column!r} column, {want!r} "
                                 f"(R17)")
            if (cell in own and not isinstance(columns[cell], dict) and cell in row.index
                    and isinstance(row[cell], str)):
                try:
                    if proj.cells[cell]() == row[cell]:
                        own[cell] += 1
                except Exception:                   # a fault above already
                    pass
    for cell, n in own.items():
        if points and n == points:
            found.append(f"reporting_columns[{cell!r}] is stale: {cell}() returns its own "
                         f"{cell!r} column on every point, its default without the entry")
    return found


# ---------------------------------------------------------------------------
# C3 -- the typing guard, read from what the compiler generated


C_SCALARS = frozenset({"bint", "long long", "double"})
"""The C types a compiled cell returns and takes: a flag, an integer, a real (F3)."""

_MEMORYVIEW = re.compile(r"const (?:double|long long)\[:(?:, :)*\]")
_PXD_CLASS = re.compile(r"^cdef class _c_(\w+)\(", re.M)
_PXD_CPDEF = re.compile(r"\s+cpdef (.+?) (\w+)\(_c_\w+ self((?:, [^)]*)?)\)\s*")
_PXD_CACHE = re.compile(r"\s+cdef (.+?)((?:\[\d+\])*) _v_(\w+)\s*")


def pxd_declarations(pxd, space):
    """What a generated ``_mx_classes.pxd`` declares for the cells of one space.

    Returns ``(cells, caches)``: ``{cell: (return type, ((type, parameter), ...))}`` for
    each cell compiled to a ``cpdef`` method, and ``{cell: (type, sizes)}`` for each cell's
    cache, ``sizes`` being the dimensions of its C array, ``()`` for a single value.  A
    cell missing from ``cells`` stayed a Python method.  ``space`` is the space's name,
    ``"Projection"``; a space the file does not declare has neither.
    """
    blocks = _PXD_CLASS.split(pxd)
    body = dict(zip(blocks[1::2], blocks[2::2])).get(space, "")
    cells, caches = {}, {}
    for line in body.splitlines():
        found = _PXD_CPDEF.fullmatch(line)
        if found and not found.group(2).startswith("_mx"):
            params = tuple(tuple(part.strip().rsplit(" ", 1))
                           for part in found.group(3).split(",") if part.strip())
            cells[found.group(2)] = (found.group(1), params)
            continue
        found = _PXD_CACHE.fullmatch(line)
        if found:
            sizes = tuple(int(n) for n in re.findall(r"\[(\d+)\]", found.group(2)))
            caches[found.group(3)] = (found.group(1), sizes)
    return cells, caches


def data_readers(model):
    """The ``Data`` cells of ``model`` that read an input file: its readers (R5).

    A reader is a cell whose formula names a ``Data`` Reference ending ``_file`` outside
    its ``raise`` statements, as ``model_point_table()`` names ``model_point_file``.  R5
    keeps the S model's readers as they are, Python objects returning DataFrames, and a
    reader of an SEC-only companion file is one too (D8): IUL's in-force ladder, DIA's
    premium schedule.  A cell that only quotes a file's name in a refusal is not one.
    """
    import ast
    files = {ref for ref in model.Data.refs if ref.endswith("_file")}
    found = set()
    for name, cells in model.Data.cells.items():
        tree, _, _, exempt = _syntax(cells)
        if any(isinstance(node, ast.Name) and node.id in files and node not in exempt
               for node in ast.walk(tree)):
            found.add(name)
    return frozenset(found)


def typing_faults(build, model, *, reporting, new_data):
    """C3: what the compiled model holds as Python objects, from its declarations.

    Every ``Projection`` cell of ``model`` outside ``reporting`` (:func:`reporting_cells`)
    must compile to a method returning one of :data:`C_SCALARS` and taking only them, and
    none of their caches may be a Python dict.  Every ``Data`` cell of ``new_data``, the
    ones the S twin lacks, must return a typed memoryview of int64 or float64, or a C
    scalar (R5), but for the readers among them (:func:`data_readers`), which stay
    Python, as the S model's own do.  ``model`` is the modelx model ``build`` was
    compiled from.  Returns a line per fault, empty when the declarations are all C.
    """
    lines = []
    cells, caches = pxd_declarations(build.pxd, "Projection")
    for name in sorted(set(model.Projection.cells) - set(reporting)):
        if name not in cells:
            lines.append(f"Projection.{name} did not compile: it stays a Python method, as "
                         f"one does whose name a call with keywords uses, and an uncached "
                         f"one whose formula holds a generator, a lambda or a nested def "
                         f"(F3)")
            continue
        returns, params = cells[name]
        if returns not in C_SCALARS:
            lines.append(f"Projection.{name} returns {returns}, not a C scalar: a cell "
                         f"mx2cy has no trace of, one the sample never calls or an "
                         f"uncached one, whose formula modelx-cython 0.1.0 never traces "
                         f"(R14), or one returning what mx2cy cannot type, a numpy bool, "
                         f"text, a tuple or a DataFrame (F3)")
        for kind, param in params:
            if kind not in C_SCALARS:
                lines.append(f"Projection.{name} takes {param} as {kind}: a timing or a "
                             f"kind passed as text, not as an int code (R9), or a cell "
                             f"mx2cy has no trace of, as above")
        if caches.get(name, ("",))[0] == "dict":
            lines.append(f"Projection.{name} caches its values in a Python dict")
    data_cells, _ = pxd_declarations(build.pxd, "Data")
    for name in sorted(set(new_data) - data_readers(model)):
        if name not in data_cells:
            lines.append(f"Data.{name} did not compile: it stays a Python method")
            continue
        returns = data_cells[name][0]
        if returns not in C_SCALARS and not _MEMORYVIEW.fullmatch(returns):
            lines.append(f"Data.{name} returns {returns}, not a typed memoryview or a C "
                         f"scalar: an array of bools, objects or text, or one a cell uses "
                         f"whole (R5, R13)")
    return lines


def object_cells(name, space):
    """The cells of SEC model ``name``'s ``Projection`` that must compile to ``object``.

    ``model_point``, every ``result_*`` report and the label accessors the registry entry
    names under ``"reporting"``: the reporting cells that hand a reader a table row, a
    DataFrame or a point's column as read, which ``Data`` may hold as text, a number or a
    blank.  The other reporting cells of :func:`reporting_cells` are typed: a ``check_*``
    returns a ``bint``, and an ``"engine"`` cell a C scalar.  ``space`` is the model's
    ``Projection``.
    """
    from uk_registry import meta
    labels = set(meta(name).get("reporting", ()))
    return frozenset(cell for cell in space.cells
                     if cell == "model_point" or cell.startswith("result_")
                     or cell in labels)


def object_return_faults(build, cells, refusing=frozenset()):
    """C3 of the reporting cells: each of ``cells`` that compiled returns ``object``.

    A label accessor returns its point's column as read, and ``Data`` accepts a label that
    is not text, a blank or a number.  mx2cy types a cell from what the sample's calls
    return, so an accessor the sample traces on text alone compiles to ``str``, and the
    compiled model raises ``TypeError`` where modelx returns the value.  The sample
    therefore calls each on a point whose label is not text too, and this holds what it
    makes of that: every cell of ``cells`` (:func:`object_cells`) that ``build``'s
    ``_mx_classes.pxd`` declares returns ``object``, but a label of ``refusing``, which
    modelx refuses wherever its column is not text (:func:`labels_refusing_non_text`), as
    a label validating its column does: it returns text or raises, in either engine.  One
    left a Python method is not declared, and returns what modelx does.  Returns a line
    per fault.
    """
    declared, _ = pxd_declarations(build.pxd, "Projection")
    return [f"Projection.{name} returns {declared[name][0]}, where a reporting cell "
            f"returns object: a label the sample traced on text alone, which raises "
            f"TypeError compiled on a label Data holds as a number or a blank, where "
            f"modelx returns it (R17)"
            for name in sorted(cells)
            if name in declared and declared[name][0] != "object" and name not in refusing]


def labels_refusing_non_text(name, labels):
    """The labels of ``labels`` that SEC model ``name`` refuses, in their own formula,
    wherever they are not text.

    Each label is called, in modelx, on the committed model whose table,
    ``Data.model_point_table()``, is replaced by an input value holding the first point's
    column blank, and then the number 7, past every check ``Data``'s reader makes; called
    as the registry's ``"reporting_columns"`` says (:func:`label_faults`), at each
    argument.  A label is refusing where every such call raises, as a label validating
    its column does.  A refusal of ``Data``'s is not the label's, and is not sought: a
    key label returns a number where its tables are keyed by numbers.  A refusing label
    returns text or raises, so it may compile to ``str`` (:func:`object_return_faults`).
    """
    from uk_registry import meta, point_keys, projection
    columns = meta(name).get("reporting_columns", {})
    refusing = set()
    for label in sorted(labels):
        refused = True
        for args, column, _ in _label_calls(columns.get(label, label)):
            for value in (None, 7):
                if not refused:
                    break
                model = mx.read_model(model_path(name),
                                      name=f"{name}_text_{next(_c4_names)}")
                try:
                    table = model.Data.model_point_table().astype({column: object})
                    table.iloc[0, table.columns.get_loc(column)] = value
                    model.Data.model_point_table[()] = table
                    proj = projection(model, point_keys(model)[0])
                    try:
                        proj.cells[label](*args)
                        refused = False
                    except Exception:       # the label's own refusal, which is sought
                        pass
                finally:
                    model.close()
        if refused:
            refusing.add(label)
    return frozenset(refusing)


def spec_faults(build, spec_path):
    """C3's check of the spec: each C-array cache is the size ``spec_path`` gives (F4).

    mx2cy sizes the cache of every cell with integer parameters from the spec's
    ``cells_param_size``, keyed by the parameters' names, and it ignores without a word a
    key that no cell takes, a misspelt one, sizing those caches from the sample's largest
    argument instead, which the committed points fit.  So the spec is read here as mx2cy
    reads it, with ``ast.literal_eval``, and every compiled ``Projection`` cell taking
    only C integers must have a size for its parameters and a cache of exactly that size,
    and every size must be taken by some cell.  A sample argument beyond the size, which
    enlarges the cache, is reported too.  Returns a line per fault.
    """
    import ast
    spec = ast.literal_eval(pathlib.Path(spec_path).read_text(encoding="utf-8"))
    given = spec.get("spaces", {}).get("Projection", {}).get("cells_param_size", {})
    sizes = {(key if isinstance(key, tuple) else (key,)):
             (tuple(size) if isinstance(size, (tuple, list)) else (size,))
             for key, size in given.items()}
    cells, caches = pxd_declarations(build.pxd, "Projection")
    lines, taken, spec_name = [], set(), pathlib.Path(spec_path).name
    for name, (_, params) in sorted(cells.items()):
        if not params or any(kind != "long long" for kind, _ in params):
            continue
        key = tuple(param for _, param in params)
        kind, cache = caches.get(name, ("", ()))
        if key in sizes:
            taken.add(key)
        if kind == "dict":
            continue                        # typing_faults reports a dict cache
        if key not in sizes:
            lines.append(f"Projection.{name}: {spec_name} gives no size for {key}, so the "
                         f"sample sized its cache, {cache}")
        elif cache != sizes[key]:
            lines.append(f"Projection.{name}: a cache of {cache}, where {spec_name} gives "
                         f"{sizes[key]}")
    for key in sorted(set(sizes) - taken):
        lines.append(f"{spec_name} sizes {key}, which no compiled cell takes: mx2cy "
                     f"ignores the size, as it ignores a misspelt name")
    return lines


# The C function Cython writes for one Projection formula, and its body: the definition at
# the start of a line, up to the closing brace that ends its own line.
_C_FORMULA = re.compile(
    r"^static [^\n;{]*?__pyx_f_\w+?_c_Projection__f_(\w+)\([^)]*\) \{\n(.*?)\n\}\n",
    re.S | re.M)

REQUIRED_DIRECTIVES = {"infer_types": "True", "cpow": "True"}
"""The directives the library's ``build_sec_cy.py`` puts at the top of each translated
space module, which C3 requires: without ``infer_types`` an integer local stays a Python
object, and without ``cpow`` a power is complex, and drifts from modelx in its last bits
(M14)."""

# What a formula's C does that is Python's work: a builtin it looks up and calls, other
# than an exception a refusal raises, and a list, dict or set it builds.
_C_BUILTIN = re.compile(r"__pyx_builtin_(\w+)")
_C_CONTAINER = re.compile(r"\b(PyList_New|PyDict_New|__Pyx_PyDict_NewPresized|PySet_New)\b")


def _directives(line):
    """The directives of a ``# cython: a=b, c=d`` line, ``{name: value}``, or ``None``."""
    head, _, body = line.partition(":")
    if head.replace(" ", "") != "#cython":
        return None
    pairs = [part.split("=", 1) for part in body.split(",") if part.strip()]
    return {k.strip(): v.strip() for k, v in (p for p in pairs if len(p) == 2)}


def c_faults(build, *, reporting, python_calls=None):
    """C3 on the generated C: the Python a compiled formula still runs.

    A cell typed ``double`` can compute in Python all the same, and its declaration does
    not show it.  So the C of every ``Projection`` formula outside ``reporting`` must
    declare no ``PyObject`` local, which turns every operation on it into a call into the
    interpreter; call no Python builtin, such as ``round`` or ``sum``, but the exceptions a
    refusal raises and those ``python_calls``, the registry's ``"python_calls"``
    (:mod:`uk_registry`), admits in that cell, ``{cell: (builtin, ...)}``; and build no
    list, dict or set.  Under Cython's default inference an
    integer local used in arithmetic, and any loop counter, is a Python object, and a
    power of two doubles is complex, so every translated space module must begin with the
    directives of :data:`REQUIRED_DIRECTIVES`, which the library's ``build_sec_cy.py``
    writes.
    An uncached cell has no ``_f_`` formula, its public method being its formula, so its
    body is not read here; mx2cy types no such cell, and :func:`typing_faults` and
    :func:`static_faults` refuse it.  Returns a line per fault.
    """
    lines, python_calls = [], python_calls or {}
    for module in sorted(build.package.rglob("_mx_classes.py")):
        first = module.read_text(encoding="utf-8").split("\n", 1)[0]
        given = _directives(first) or {}
        missing = [f"{k}={v}" for k, v in REQUIRED_DIRECTIVES.items() if given.get(k) != v]
        if missing:
            lines.append(f"{module.name} begins {first!r}, without {', '.join(missing)}: "
                         f"build_sec_cy.py puts them on its first line")
    source = build.package / "_mx_classes.c"
    if not source.is_file():
        return lines + [f"no generated C at {source}"]
    found = 0
    for match in _C_FORMULA.finditer(source.read_text(encoding="utf-8", errors="replace")):
        found += 1
        name, body = match.group(1), match.group(2)
        if name in reporting:
            continue
        objects = sorted(set(re.findall(r"PyObject \*__pyx_v_(\w+)", body)))
        if objects:
            lines.append(f"Projection.{name} keeps Python objects in its C locals: "
                         f"{', '.join(objects)}")
        builtins = sorted({b for b in _C_BUILTIN.findall(body)
                           if not b.endswith(("Error", "Exception", "Warning"))}
                          - set(python_calls.get(name, ())))
        if builtins:
            lines.append(f"Projection.{name} calls the Python builtin "
                         f"{', '.join(builtins)} (R12, R16)")
        built = sorted({kind for kind in _C_CONTAINER.findall(body)})
        if built:
            lines.append(f"Projection.{name} builds a Python list, dict or set "
                         f"({', '.join(built)}) (R10, R12)")
    if not found:
        lines.append(f"no Projection formula in {source.name}: its layout has changed "
                     f"under this check")
    return lines


# ---------------------------------------------------------------------------
# C4 -- the compiled model against modelx, cell by cell


COMPILED_RTOL = 1e-12
"""C4's tolerance where it is not exact: relative, floored at the same fraction of the
cell's magnitude (:func:`exact_here`)."""


def exact_here():
    """Whether C4 holds the compiled model to modelx bit for bit on this machine.

    On x86-64 it does.  The library's ``build_sec_cy.py`` compiles with
    ``-ffp-contract=off`` there, after any ``-march`` the interpreter's flags or ``CFLAGS``
    give, so that gcc and clang fuse no multiply and add into one rounding, which they do
    by default wherever the target has fused multiply-add; MSVC, on Windows, emits none for
    x64 without ``/arch:AVX2``, which setuptools does not pass.  And with ``cpow=True`` the
    compiled power is the C ``pow`` that Python's float power calls.  So a compiled cell
    does modelx's arithmetic in modelx's order, and every value Term's tables reach is
    identical (M14).  Elsewhere, on arm64 among others, no run has shown it yet, and C4
    compares to :data:`COMPILED_RTOL` instead.
    """
    import platform
    return platform.machine().lower() in ("x86_64", "amd64")

_c4_names = itertools.count(1)


def full_sweep(proj):
    """Evaluate on one point every value C4 compares, and return what raised.

    Every cell without parameters, the reports among them, and then, for ``t = 0 ..
    proj_len()`` in ascending order, every cell whose one parameter is ``t``: the frame,
    and the month after it, which the count's roll-forward reads.  What those reach is
    evaluated with them: a cell keyed by a timing, a policy year or a duration, at every
    argument the frame asks of it.  A call that raises is recorded, ``{(cell, args):
    "Type: message"}``, and the sweep goes on, unless it is ``proj_len()`` itself.
    """
    raised = {}

    def call(name, args):
        try:
            proj.cells[name](*args)
        except Exception as err:            # recorded, for a raise to meet a raise
            raised[(name, args)] = _error_text(err)

    for name, cells in proj.cells.items():
        if not cells.parameters:
            call(name, ())
    if "proj_len" not in proj.cells or ("proj_len", ()) in raised:
        return raised
    monthly = [name for name, cells in proj.cells.items()
               if tuple(cells.parameters) == ("t",)]
    for t in range(proj.proj_len() + 1):
        for name in monthly:
            call(name, (t,))
    return raised


def _cached_values(proj):
    """``{(cell, args): value}`` for every value ``proj`` has cached, in cache order."""
    found = {}
    for name, cells in proj.cells.items():
        n_params = len(cells.parameters)
        for key in list(cells.keys()):
            args = _args(key, n_params)
            found[(name, args)] = cells(*args)
    return found


# The kinds of value most cells return, which C4 compares at once when they are identical.
_PLAIN = (float, int, bool, str)


def _kind(x):
    """C4's kind of a value: a bool, an int and a real stay apart, numpy's or Python's."""
    kind = type(x)
    if kind is float:
        return "float"
    if kind is bool or isinstance(x, np.bool_):
        return "bool"
    if isinstance(x, numbers.Integral):
        return "int"
    if isinstance(x, numbers.Real):
        return "float"
    return kind.__name__


def _scaled_close(a, b, scale, rtol=COMPILED_RTOL):
    """Within ``rtol`` of the larger of the two, or of ``scale``; at 0, identical."""
    if a == b or (a != a and b != b):
        return True
    if not (math.isfinite(a) and math.isfinite(b)):
        return False
    return abs(a - b) <= rtol * max(abs(a), abs(b), scale)


def _magnitude(values):
    """The largest finite absolute value among the numbers of ``values``; 0.0 if none."""
    found = [abs(float(v)) for v in values if _kind(v) in ("int", "float")]
    return max((v for v in found if math.isfinite(v)), default=0.0)


def _series_text(want, have, rtol=COMPILED_RTOL):
    """How two Series on the same labels differ, value by value, or ``None``."""
    a, b = want.tolist(), have.tolist()
    scale = _magnitude(a)
    bad = [i for i, (x, y) in enumerate(zip(a, b)) if _value_text(x, y, scale, rtol)]
    if not bad:
        return None
    first = bad[0]
    return (f"{len(bad)} of {len(a)} differ, first at {_py(want.index[first])!r}: "
            f"{_value_text(a[first], b[first], scale, rtol)}")


def _value_text(want, have, scale, rtol=COMPILED_RTOL):
    """Why ``have``, a compiled value, is not ``want``, modelx's; ``None`` when it is.

    A bool, an int and a real must stay what they are, and ints compare exactly; reals
    compare within ``rtol``, floored at ``scale``, the cell's magnitude, and at ``rtol``
    0 must be identical, NaN meeting NaN.  A DataFrame compares column by column on the
    same labels, a Series value by value, each against its own magnitude, an array
    exactly, and anything else by equality.
    """
    kind = _kind(want)
    if kind != _kind(have):
        return f"modelx {_typed(want)}, compiled {_typed(have)}"
    if kind in ("bool", "int", "float"):
        same = (_scaled_close(float(want), float(have), scale, rtol) if kind == "float"
                else want == have)
        return None if same else f"modelx {_py(want)!r}, compiled {_py(have)!r}"
    if isinstance(want, pd.DataFrame):
        if list(want.columns) != list(have.columns) or not want.index.equals(have.index):
            return (f"modelx's frame has columns {list(want.columns)} and {len(want)} "
                    f"rows, the compiled one {list(have.columns)} and {len(have)}")
        parts = [f"column {column!r}: {text}" for column in want.columns
                 if (text := _series_text(want[column], have[column], rtol))]
        return "; ".join(parts) or None
    if isinstance(want, pd.Series):
        if not want.index.equals(have.index):
            return "the two Series have different labels"
        return _series_text(want, have, rtol)
    if isinstance(want, np.ndarray):
        same = (want.shape == have.shape and want.dtype == have.dtype
                and np.array_equal(want, have, equal_nan=want.dtype.kind == "f"))
        return None if same else f"modelx {want!r}, compiled {have!r}"
    return None if want == have else f"modelx {want!r}, compiled {have!r}"


def _outcome_text(want, have, scale, rtol=COMPILED_RTOL):
    """Why the compiled outcome is not modelx's, each ``("ok", value)`` or ``("raised",
    "Type: message")``; ``None`` when they agree.  A raise must meet the same raise."""
    if have is None:
        return "the compiled run returned nothing for it"
    if want[0] == have[0] == "ok":
        return _value_text(want[1], have[1], scale, rtol)
    if want[0] == have[0] == "raised" and want[1] == have[1]:
        return None
    show = {"ok": lambda v: f"returned {_typed(v)}" if _kind(v) in ("bool", "int", "float")
            else f"returned a {type(v).__name__}", "raised": lambda v: f"raised {v}"}
    return f"modelx {show[want[0]](want[1])}, compiled {show[have[0]](have[1])}"


def c4_expected(proj, also=None):
    """What C4 expects of one modelx point: ``{(cell, args): ("ok", value) | ("raised",
    "Type: message")}``.

    :func:`full_sweep` first, then, unless the point's ``proj_len()`` raised, ``also(proj)``
    where it is given, a product's calls of the cells and codes no swept cell reaches, the
    pricing path's closes or a timing no formula passes; then every value the point has
    cached, at every argument, and every raise the sweep recorded.  So what ``also`` calls
    enters the expectation, and the compiled run, which repeats every expected call, makes
    it too.  ``also`` must not raise: it calls only what the point computes.
    """
    raised = full_sweep(proj)
    if also is not None and ("proj_len", ()) not in raised:
        also(proj)
    found = {call: ("ok", value) for call, value in _cached_values(proj).items()}
    found.update((call, ("raised", text)) for call, text in raised.items())
    return found


def compiled_mismatches(build, folder, *, refs=None, stack_kib=65536, limit=50,
                        exact=None, also=None):
    """C4: where the compiled model departs from modelx on the model in ``folder``, cell
    by cell.

    ``folder`` is the model folder of a case :func:`compiled_case` made, so modelx and the
    compiled package beside it read the same CSVs.  The model is read from it afresh, under
    a name of its own, ``refs`` are set on its ``Projection``, a name ``"Data.<name>"`` on
    its ``Data``, and every point is swept (:func:`full_sweep`): every value modelx then
    holds in a cache, at every argument, is the expectation, and so is every raise.  A fresh
    read, because the sweep evaluates what no projection asks for, a rate before issue among
    them, which a test of the same model's instance may forbid.  The compiled package then
    makes the same calls on the same points with the same ``refs``, in a child
    (:func:`run_compiled`), on a thread of ``stack_kib`` KiB, and reads every ``Data`` cell
    whose modelx value is an array or a number.  ``also``, a callable of one modelx point,
    adds what it calls to the expectation, and so to the compiled run's calls
    (:func:`c4_expected`); a model's spec gives its own as ``c4_also``
    (:func:`spec_c4_also`).

    They must agree: a number identical where ``exact`` holds, by default where
    :func:`exact_here` does, and elsewhere within :data:`COMPILED_RTOL` relative, floored
    at the cell's largest magnitude on the point; a bool and an int keeping their kind, a
    frame column by column, text exactly, a raise with the same type and message, and
    every ``Data`` array exactly, in dtype and shape too.  Both spaces must come from
    extension modules.  Returns readable lines, ``"point 4: premiums(6): modelx 89.6,
    compiled 89.7"``, empty when the compiled model computes what modelx computes; at
    most ``limit``, the last saying when more were found.
    """
    from uk_registry import point_keys, projection
    folder, refs = pathlib.Path(folder), dict(refs or {})
    rtol = 0.0 if (exact_here() if exact is None else exact) else COMPILED_RTOL
    model = mx.read_model(folder, name=f"{build.name}_c4_{next(_c4_names)}")
    try:
        for ref, value in refs.items():
            if ref.startswith("Data."):
                setattr(model.Data, ref[len("Data."):], value)
            else:
                setattr(model.Projection, ref, value)
        labels = list(model.Data.model_point_table().index)
        keys, expected = point_keys(model), {}
        for key in keys:
            expected[key] = c4_expected(projection(model, key), also)
        data = {}
        for name, cells in model.Data.cells.items():
            try:
                value = cells()
            except Exception as err:            # a raise must meet the same raise
                data[name] = ("raised", _error_text(err))
                continue
            if isinstance(value, np.ndarray) or _kind(value) in ("int", "float"):
                data[name] = ("ok", value)
    finally:
        model.close()
    job = {"refs": refs, "calls": {key: list(found) for key, found in expected.items()},
           "data": list(data)}
    got = run_compiled(folder.parent, build.package.name, job, stack_kib=stack_kib)
    if got["exit"]:
        return [f"the compiled run failed with exit code {got['exit']}:\n{got['stderr']}"]
    lines = [f"{space} was not loaded from an extension module"
             for space, compiled in got["compiled"].items() if not compiled]
    compared = 0
    for key, label in zip(keys, labels):
        found, scales = expected[key], {}
        for (name, _), (status, value) in found.items():
            if status == "ok" and _kind(value) == "float":
                scales[name] = max(scales.get(name, 0.0), _magnitude([value]))
        for ((name, args), want), have in zip(found.items(), got["values"][key]):
            compared += 1
            if (have is not None and want[0] == have[0] == "ok"
                    and type(want[1]) is type(have[1]) and type(want[1]) in _PLAIN
                    and want[1] == have[1]):
                continue                        # identical, the usual case
            text = _outcome_text(want, have, scales.get(name, 0.0), rtol)
            if text:
                lines.append(f"point {label}: {_call(name, args)}: {text}")
    for name, want in data.items():
        compared += 1
        text = _outcome_text(want, got["data"].get(name), 0.0)
        if text:
            lines.append(f"Data.{name}(): {text}")
    if not compared:
        lines.append(f"nothing was compared: {folder} holds no model point")
    if len(lines) > limit:
        lines = lines[:limit - 1] + [f"(and {len(lines) - limit + 1} more)"]
    return lines


def spec_c4_also(name):
    """The ``also`` of SEC model ``name``'s spec, its :class:`SecSpec` ``c4_also``:
    ``None`` where the model has no spec or its spec gives none.

    The conventions' C4 on the committed points passes it to :func:`compiled_mismatches`,
    so that every cell of a code no swept cell reads is compared there too, as each
    product's own comparisons compare it.
    """
    spec = SEC_SPECS.get(name)
    return None if spec is None else spec.c4_also


# ---------------------------------------------------------------------------
# C5 -- what a compiled Projection formula may not hold


PANDAS_ATTRIBUTES = frozenset({
    "loc", "iloc", "at", "iat", "iterrows", "itertuples", "apply", "values", "to_numpy"})
"""The pandas reads C5 looks for in a ``Projection`` formula, beside the modules."""

C_CALLS = frozenset({"int", "float", "bool", "abs", "min", "max", "range"})
"""The builtins a compiled formula may call, beside cells and ``Data`` vectors: Cython
turns each into C on C numbers, where any other builtin, ``round`` and ``sum`` among them,
is a call into the interpreter, which no declaration shows (R12, R16).  But for ``int`` of
a double: Cython makes it a Python int, converted back to a C integer where it is
returned or used, exact below ``2**63`` and raising ``OverflowError`` past it, a call into
Python that :func:`c_faults` sees only when the int is held in a local, and not as the
temporary of an expression.  A model records each such call (UL's and VUL's
``model-sec.md``, *No Python call kept*), and holds its input below ``2**53`` in
``Data``."""


def _spaces(model):
    """``(name, space)`` for every space of ``model``, the spaces within them included."""
    pending = list(model.spaces.items())
    while pending:
        name, space = pending.pop(0)
        yield name, space
        pending += [(f"{name}.{child}", sub) for child, sub in space.spaces.items()]


def _syntax(cells):
    """A cell's formula parsed: ``(tree, top, parents, exempt)``.

    ``top`` is the formula's own ``def`` or ``lambda``; ``parents`` maps every node to the
    node holding it; ``exempt`` holds the nodes that may hold text, the docstring and
    whatever a ``raise`` holds, its message.
    """
    import ast
    import textwrap
    tree = ast.parse(textwrap.dedent(cells.formula.source))
    first = tree.body[0] if tree.body else None
    top = first.value if isinstance(first, ast.Expr) else first
    parents = {child: node for node in ast.walk(tree)
               for child in ast.iter_child_nodes(node)}
    exempt = set()
    if isinstance(top, ast.FunctionDef) and top.body:
        head = top.body[0]
        if (isinstance(head, ast.Expr) and isinstance(head.value, ast.Constant)
                and isinstance(head.value.value, str)):
            exempt.add(head.value)
    for node in ast.walk(tree):
        if isinstance(node, ast.Raise):
            exempt.update(ast.walk(node))
    return tree, top, parents, exempt


def _element_read(call, parents, ndim):
    """Whether ``call``'s array is read as one element: subscripted at once, by ``ndim``
    indices in all, none a slice, and not written to (mx2cy's usage analysis, F3)."""
    import ast
    remaining, node = ndim, call
    while remaining > 0:
        up = parents.get(node)
        if not (isinstance(up, ast.Subscript) and up.value is node):
            return False
        index = up.slice
        items = index.elts if isinstance(index, ast.Tuple) else [index]
        if len(items) > remaining or any(isinstance(i, (ast.Slice, ast.Starred))
                                         for i in items):
            return False
        remaining -= len(items)
        node = up
    return not isinstance(getattr(node, "ctx", None), (ast.Store, ast.Del))


def _negative_index(call, parents, ndim):
    """The first negative literal among the indices ``call``'s array is read at, as
    written, ``"-1"``, or ``None``: Python and compiled Cython both wrap it to the end of
    the array, so a fault that reads one passes C4 (M23)."""
    import ast
    remaining, node = ndim, call
    while remaining > 0:
        up = parents.get(node)
        if not (isinstance(up, ast.Subscript) and up.value is node):
            return None
        items = up.slice.elts if isinstance(up.slice, ast.Tuple) else [up.slice]
        for item in items:
            value = item
            sign = 1
            while isinstance(value, ast.UnaryOp) and isinstance(value.op,
                                                                (ast.USub, ast.UAdd)):
                sign *= -1 if isinstance(value.op, ast.USub) else 1
                value = value.operand
            if (isinstance(value, ast.Constant) and isinstance(value.value, numbers.Real)
                    and not isinstance(value.value, bool) and sign * value.value < 0):
                return ast.unparse(item)
        remaining -= len(items)
        node = up
    return None


def _vector_text(value):
    """What is wrong with a ``Data`` value a compiled cell reads, or ``None``: it must be
    an int64 or float64 array, a memoryview compiled, or a Python int or float (R5)."""
    if isinstance(value, np.ndarray):
        if value.dtype in (np.dtype("int64"), np.dtype("float64")):
            return None
        return f"an array of {value.dtype}"
    if _kind(value) in ("int", "float") and not isinstance(value, np.generic):
        return None
    return f"a {type(value).__module__.split('.')[0]} {type(value).__name__}"


def _admitted_call(node, parents, cell, python_calls):
    """Whether module name ``node`` heads a call ``python_calls`` admits in ``cell``.

    ``math.erf(x)`` is admitted where the cell's admission names ``"math.erf"``, and only
    as the one argument of a ``float(...)``, which Cython turns into a C double at once, so
    that the call keeps no Python object among the cell's locals or temporaries (R16,
    M25).  A module attribute read but not called, ``math.inf``, is no call, and stays a
    fault; so does an admitted call left unwrapped.
    """
    import ast
    attr = parents.get(node)
    call = parents.get(attr)
    wrap = parents.get(call)
    return (isinstance(attr, ast.Attribute) and attr.value is node
            and isinstance(call, ast.Call) and call.func is attr
            and f"{node.id}.{attr.attr}" in python_calls.get(cell, ())
            and isinstance(wrap, ast.Call) and isinstance(wrap.func, ast.Name)
            and wrap.func.id == "float" and wrap.args == [call] and not wrap.keywords)


def static_faults(model, *, reporting, python_calls=None):
    """C5: what a formula of ``model`` holds that a compiled cell cannot run in C.

    Read from the formulas, so it needs no compiler and runs in the default suite.  Every
    ``Projection`` formula outside ``reporting`` (:func:`reporting_cells`) may refer to no
    module, ``pd`` and ``np`` among them, read no pandas attribute
    (:data:`PANDAS_ATTRIBUTES`), refer to no reporting cell, ``model_point`` among them,
    hold no text outside its docstring and its ``raise`` messages, read no Reference that
    holds text, call ``len()`` nowhere, and hold no generator, comprehension, ``lambda`` or
    nested ``def`` (R10-R13).  Outside its ``raise`` statements it calls no function but
    a cell, a ``Data`` vector and the builtins of :data:`C_CALLS`, and no method, and it
    builds no list, dict, set or tuple, but the index of a table read, ``[s, y]``: each is
    a call into Python inside a cell its declaration types as C (R10, R12).  Every
    ``Data`` cell it calls must return an int64 or float64 array or a Python int or float,
    found by evaluating it, and an array must be read at once by element (R5, R13), at no
    negative literal index, ``[-1]``, which C wraps as Python does, so that C4 cannot see
    a read from the wrong end (:func:`_negative_index`, M23); every ``Data`` array another
    ``Data`` cell calls must be read by element too.  No ``Projection`` cell outside
    the allowlist may be uncached, ``is_cached`` False: mx2cy traces a cell's ``_f_``
    formula, which an uncached cell has none of, so it compiles untyped (R14).  And no
    cell outside the allowlist, in any space, may share its name with a function or a
    method that a call with keywords calls anywhere in the model, the reporting cells
    included, because mx2cy keeps every cell of such a name a Python method (R12).  The
    registry's ``reporting`` must name ``Projection`` cells.  ``python_calls``, the
    registry's ``"python_calls"``, ``{cell: (builtin, ...)}``, admits each builtin it names
    in that cell's formula alone, R16's ``round`` of a projected amount, and each module's
    function it names by its dotted name, ``"math.erf"``, where the call is the one
    argument of a ``float(...)`` (:func:`_admitted_call`, M25).  Returns a line
    per fault, ``"Projection.mort_rate_base, line 9: reads .loc"``, the line counted in the
    formula.
    """
    import ast
    import types
    proj, data = model.Projection, model.Data
    python_calls = python_calls or {}
    lines = [f"the registry's reporting names {name}, which is not a Projection cell"
             for name in sorted(set(reporting) - set(proj.cells))]
    values = {}
    for name, cells in data.cells.items():
        try:
            values[name] = cells()
        except Exception as err:            # reported, and the formulas still read
            lines.append(f"Data.{name} raised {_error_text(err)}")
    arrays = {name: value.ndim for name, value in values.items()
              if isinstance(value, np.ndarray)}
    trees = {(space_name, name): _syntax(cells) for space_name, space in _spaces(model)
             for name, cells in space.cells.items()}
    keyworded = {}
    for (space_name, name), (tree, _, _, _) in trees.items():
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and node.keywords:
                func = node.func
                callee = (func.id if isinstance(func, ast.Name)
                          else getattr(func, "attr", ""))
                keyworded.setdefault(callee, f"{space_name}.{name}, line {node.lineno}")
    for space_name, name in trees:
        if name in keyworded and not (space_name == "Projection" and name in reporting):
            lines.append(f"{space_name}.{name} shares its name with what a call with "
                         f"keywords calls, at {keyworded[name]}: mx2cy keeps every cell "
                         f"of that name a Python method (R12)")
    refs = {ref: value for ref, value in proj.refs.items() if not ref.startswith("__")}
    modules = {ref for ref, value in refs.items() if isinstance(value, types.ModuleType)}
    modules |= {"pd", "np"}
    texts = {ref for ref, value in refs.items() if isinstance(value, str)}
    interfaces = {ref for ref, value in refs.items() if value is data} or {"data"}
    banned = (ast.GeneratorExp, ast.ListComp, ast.SetComp, ast.DictComp, ast.Yield,
              ast.YieldFrom, ast.Lambda, ast.FunctionDef)
    displays = {ast.List: "list", ast.Dict: "dict", ast.Set: "set", ast.Tuple: "tuple"}
    for name in proj.cells:
        if name in reporting:
            continue
        if not proj.cells[name].is_cached:
            lines.append(f"Projection.{name} is uncached: modelx-cython 0.1.0 traces only "
                         f"a cached cell's formula, so an uncached one compiles taking and "
                         f"returning Python objects (R14)")
        tree, top, parents, exempt = trees[("Projection", name)]
        for node in ast.walk(tree):
            where = f"Projection.{name}, line {getattr(node, 'lineno', '?')}"
            kind = displays.get(type(node))
            if kind and node not in exempt and not (
                    isinstance(parents.get(node), ast.Subscript)
                    and parents[node].slice is node):
                lines.append(f"{where}: builds a {kind}, a Python object")
            if isinstance(node, ast.Name):
                if node.id in modules and not _admitted_call(node, parents, name,
                                                             python_calls):
                    lines.append(f"{where}: refers to the module {node.id}")
                elif node.id in reporting:
                    lines.append(f"{where}: refers to the reporting cell {node.id}")
                elif node.id in texts:
                    lines.append(f"{where}: reads {node.id}, a Reference holding text")
            elif isinstance(node, ast.Attribute) and node.attr in PANDAS_ATTRIBUTES:
                lines.append(f"{where}: reads .{node.attr}")
            elif (isinstance(node, ast.Constant) and isinstance(node.value, str)
                  and node not in exempt):
                lines.append(f"{where}: holds the text {node.value!r}")
            elif isinstance(node, banned) and node is not top:
                lines.append(f"{where}: holds a {type(node).__name__}")
            elif isinstance(node, ast.Call) and node not in exempt:
                func = node.func
                if isinstance(func, ast.Name) and func.id == "len":
                    lines.append(f"{where}: calls len()")
                elif isinstance(func, ast.Name):
                    if (func.id not in proj.cells and func.id not in C_CALLS
                            and func.id not in python_calls.get(name, ())):
                        lines.append(f"{where}: calls {func.id}(), a call into Python: a "
                                     f"compiled formula calls cells, Data vectors and "
                                     f"{', '.join(sorted(C_CALLS))} alone")
                elif not (isinstance(func, ast.Attribute)
                          and isinstance(func.value, ast.Name)
                          and func.value.id in interfaces | modules):
                    lines.append(f"{where}: calls the method "
                                 f".{getattr(func, 'attr', '?')}(), a call into Python")
                elif (isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name)
                      and func.value.id in interfaces and func.attr in values):
                    text = _vector_text(values[func.attr])
                    if text:
                        lines.append(f"{where}: reads data.{func.attr}(), {text}, where a "
                                     f"Data vector is an int64 or float64 array or an int")
                    elif (func.attr in arrays
                          and not _element_read(node, parents, arrays[func.attr])):
                        lines.append(f"{where}: uses data.{func.attr}() other than by one "
                                     f"element")
                    elif func.attr in arrays:
                        negative = _negative_index(node, parents, arrays[func.attr])
                        if negative:
                            lines.append(f"{where}: reads data.{func.attr}() at the "
                                         f"negative index {negative}, which wraps to the "
                                         f"array's end in Python and in C alike")
    for name in data.cells:
        tree, _, parents, _ = trees[("Data", name)]
        for node in ast.walk(tree):
            if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                    and node.func.id in arrays
                    and not _element_read(node, parents, arrays[node.func.id])):
                lines.append(f"Data.{name}, line {node.lineno}: uses {node.func.id}() "
                             f"other than by one element, which compiles it as a Python "
                             f"object (R13)")
    return lines


# ---------------------------------------------------------------------------
# A compiled block run, and what it keeps (F5, K2)


RELEASE_RUNNER = '''\
"""Run an SEC model's run_sec.py over a block, compiled, counting its ItemSpaces.

    python probe.py <run_sec.py> <case dir> <package> <result>

After each collection the runner makes once it has frozen what was alive, the Projection
ItemSpaces still alive are counted.  When the runner is done, what it froze is unfrozen
and they are counted again, so that one kept since before the freeze is seen too.  Then,
if none is, a control: an ItemSpace made and deleted, counted before a collection and
after it.
"""
import contextlib
import gc
import io
import pickle
import runpy
import sys

runner, case, package, result_path = sys.argv[1:5]
collect, after = gc.collect, []


def alive():
    """The ItemSpaces of the base Projection's class alive and not frozen, less the base."""
    module = sys.modules.get(package)
    if module is None:
        return 0
    base = module.mx_model.Projection
    return sum(1 for o in gc.get_objects() if type(o) is type(base) and o is not base)


def counted(*args, **kwargs):
    found = collect(*args, **kwargs)
    if gc.get_freeze_count():
        after.append(alive())
    return found


gc.collect = counted
sys.argv = [runner, "--block", "--build", case]
printed, stopped = io.StringIO(), None
try:
    with contextlib.redirect_stdout(printed):
        runpy.run_path(runner, run_name="__main__")
except SystemExit as stop:
    stopped = stop.code
gc.collect = collect
gc.unfreeze()
kept = alive()
held = freed = None
if stopped in (None, 0) and not kept:
    gc.disable()
    model = sys.modules[package].mx_model
    proj = model.Projection[0]
    proj.proj_len()
    del proj
    del model.Projection[0]
    held = alive()
    collect()
    freed = alive()
    gc.enable()
with open(result_path, "wb") as f:
    pickle.dump({"stopped": stopped, "printed": printed.getvalue(), "after": after,
                 "kept": kept, "held": held, "freed": freed}, f)
'''
"""The child that :func:`release_faults` starts around the product's own runner."""


def release_faults(case_dir, package, runner, *, points, timeout=600):
    """Where a compiled block run keeps what it has released (F5, K2), a line each.

    ``runner`` is a product's ``run_sec.py``, run with ``--block --build case_dir`` on
    the compiled ``package`` there, in a child, as a user runs it, ``points`` the number
    of points in the case's table.  A compiled ItemSpace holds every cell's cache in its
    C struct, about 430 KB for Term, and a deleted one is not freed: it refers to
    itself, as its own ``_space`` and in its own ``_mx_roots``, cycles only the cyclic
    collector frees.  So the runner releases each point once read, deleting it and
    collecting, in its frame pass and in its projections, after freezing what was alive
    before the block.  So, counting the ``Projection`` ItemSpaces alive besides the
    base: none may be alive after any collection the runner makes once frozen, and there
    must be at least one such collection for every point; none may be alive when the
    block ends, frozen or not; and then the control must still find the cycle, a deleted
    ItemSpace alive until a collection frees it.  If the control fails, modelx-cython
    frees an ItemSpace on its own, and the collection can go.
    """
    import os
    import pickle
    import subprocess
    import sys
    import tempfile
    case_dir = pathlib.Path(case_dir)
    work = pathlib.Path(tempfile.mkdtemp(prefix="release_", dir=case_dir.parent))
    probe, result = work / "probe.py", work / "found.pickle"
    probe.write_text(RELEASE_RUNNER, encoding="utf-8")
    done = subprocess.run(
        [sys.executable, "-P", str(probe), str(runner), str(case_dir), package,
         str(result)], capture_output=True, text=True, encoding="utf-8", errors="replace",
        env={**os.environ, "PYTHONIOENCODING": "utf-8"}, timeout=timeout)
    if done.returncode:
        return [f"the block run failed with exit code {done.returncode}:\n"
                f"{done.stderr[-4000:]}"]
    found = pickle.loads(result.read_bytes())
    if found["stopped"] not in (None, 0):
        return [f"run_sec.py --block stopped: {found['stopped']}"]
    lines, after = [], found["after"]
    if len(after) < points:
        lines.append(f"the runner collected {len(after)} times once frozen, over "
                     f"{points} points: it does not collect after each release")
    worst = max(after, default=0)
    if worst:
        first = next(i for i, n in enumerate(after) if n) + 1
        lines.append(f"up to {worst} ItemSpaces were alive after a release and its "
                     f"collection, the first time at collection {first}: the runner keeps "
                     f"a point it has read")
    if found["kept"]:
        lines.append(f"{found['kept']} ItemSpaces were still alive when the block ended")
    if found["held"] not in (None, 1):
        lines.append(f"the control: a deleted ItemSpace left {found['held']} alive before "
                     f"a collection, not 1; if modelx-cython no longer holds it in a "
                     f"cycle, the runner's collection can go")
    if found["freed"]:
        lines.append(f"the control: a collection left {found['freed']} deleted ItemSpaces "
                     f"alive")
    return lines


def runner_add(runner):
    """The running sum ``add(total, compensation, frame)`` of a product's ``run_sec.py``.

    The runner runs the model when imported, so the function is read from its source and
    run alone, as every product's runner defines it, at the module's top level.
    """
    import ast
    tree = ast.parse(pathlib.Path(runner).read_text(encoding="utf-8"))
    found = [node for node in tree.body
             if isinstance(node, ast.FunctionDef) and node.name == "add"]
    if len(found) != 1:
        raise ValueError(f"{runner} defines add() {len(found)} times, not once")
    space = {}
    exec(compile(ast.Module(found, []), str(runner), "exec"), space)
    return space["add"]


def block_sum_faults(add, frames):
    """Where a runner's running sum of ``frames`` is not pandas' ``groupby`` sum, a line.

    A block run keeps one point's frame at a time, so it sums the frames as it goes, with
    ``add``, compensated, so that its block is the frames concatenated and summed by
    ``t``, bit for bit; the printed block, to two decimals, cannot show a last bit.  So
    ``add`` (:func:`runner_add`) sums ``frames``, each a ``result_cf()`` indexed by ``t``
    from 0, into arrays as long as the longest, as the runner does, and the sum must equal
    ``pd.concat(frames).groupby(level=0).sum()`` by ``np.array_equal``.  The frames must
    be finite: ``groupby`` skips a NaN, which the runner's sum carries.  Returns a line
    per fault.
    """
    if not frames:
        return ["no frames to sum"]
    columns = list(frames[0].columns)
    lines = []
    for i, frame in enumerate(frames):
        if list(frame.index) != list(range(len(frame))):
            lines.append(f"frame {i} is not indexed by t = 0, 1, ...")
        if list(frame.columns) != columns:
            lines.append(f"frame {i} has the columns {list(frame.columns)}, not {columns}")
        elif not np.isfinite(frame.to_numpy(dtype=float)).all():
            lines.append(f"frame {i} is not finite, where groupby skips a NaN")
    if lines:
        return lines
    rows = max(len(frame) for frame in frames)
    total = np.zeros((rows, len(columns)))
    compensation = np.zeros_like(total)
    for frame in frames:
        add(total, compensation, frame[columns].to_numpy())
    want = pd.concat(frames).groupby(level=0).sum()[columns].to_numpy()
    if want.shape != total.shape:
        return [f"the sum is {total.shape}, groupby's {want.shape}"]
    if not np.array_equal(total, want):
        bad = np.argwhere(total != want)
        t, c = bad[0]
        lines.append(f"the running sum departs from groupby's in {len(bad)} values, first "
                     f"{columns[c]} at t = {t}: {float(total[t, c])!r}, where groupby "
                     f"gives {float(want[t, c])!r}")
    return lines


def label_mismatches(build, folder, labels):
    """C4 on label accessors alone: ``(modelx's values, a line per mismatch)``.

    ``folder`` is a :func:`compiled_case` of ``build``, and ``labels`` names label
    accessors of no parameter.  Each is called on every point, in modelx and, in a child,
    compiled (:func:`run_compiled`), and the two must agree: a value of the same kind,
    equal, or NaN on both sides, or the same raise.  A label that is not text, a blank or
    a number ``Data`` accepts, is where an accessor typed ``str`` compiled departs, raising
    ``TypeError`` where modelx returns the value (C3, M22).  The values modelx returned
    are ``{point_id: {label: ("ok", value) or ("raised", text)}}``, for the caller's
    assertions on what the case holds.
    """
    from uk_registry import point_keys, projection
    model = mx.read_model(folder, name=f"{build.name}_labels_{next(_c4_names)}")
    try:
        ids = list(model.Data.model_point_table().index)
        keys = point_keys(model)
        want = {}
        for point_id, key in zip(ids, keys):
            proj = projection(model, key)
            want[point_id] = {}
            for label in labels:
                try:
                    want[point_id][label] = ("ok", proj.cells[label]())
                except Exception as err:            # compared with the compiled raise
                    want[point_id][label] = ("raised", _error_text(err))
    finally:
        model.close()
    job = {"refs": {}, "calls": {i: [(label, ()) for label in labels]
                                 for i in range(len(ids))}}
    got = run_compiled(folder.parent, build.package.name, job)
    if got["exit"]:
        return want, [f"the compiled run failed: {got['stderr']}"]
    lines = [f"{space} is not compiled" for space, done in got["compiled"].items()
             if not done]
    for i, point_id in enumerate(ids):
        for label, have in zip(labels, got["values"][i]):
            mine = want[point_id][label]
            same = mine[0] == have[0] and (
                (mine[0] == "raised" and mine[1] == have[1])
                or (mine[0] == "ok" and _kind(mine[1]) == _kind(have[1])
                    and (mine[1] == have[1]
                         or (_kind(mine[1]) == "float" and mine[1] != mine[1]
                             and have[1] != have[1]))))
            if not same:
                lines.append(f"point {point_id}: {label}() is {have!r} compiled, "
                             f"{mine!r} in modelx")
    return want, lines
