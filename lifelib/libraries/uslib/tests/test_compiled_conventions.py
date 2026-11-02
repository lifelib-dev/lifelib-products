"""The conventions of stage "EC": what every SEC model that compiles must satisfy (Phase 2).

USLIB-SEC-PLAN.md's Phase 2 changes how each ``_SEC`` model is represented, and no number
it computes (D2), so that it compiles under modelx-cython into C-typed code, as
``basiclife/BasicTerm_SC`` does.  ``test_model_conventions.py`` holds what every model
satisfies at either stage.  This module holds what compiling adds, parametrized over the
SEC models registered at stage ``"EC"``, so that each product meets it from the commit that
moves it there, Term_US_SEC first (M14):

* C5, no Python machinery in ``Projection``: no pandas, no module, no text, no reporting
  cell, no generator or comprehension, no call but to a cell, a ``Data`` vector or a
  builtin Cython turns into C, no list, dict, set or tuple built, no keyword call that
  would keep a cell a Python method, and every ``Data`` vector a numeric array read by
  element.  Read from the formulas, so it runs in every suite, with or without a
  compiler.
* C3, the typing guard: the generated declarations say every projection cell returns and
  takes a C ``bint``, ``long long`` or ``double`` and caches in a C array of the spec's
  size, every new ``Data`` vector but a reader is a typed memoryview or a C scalar, and
  the generated C keeps no Python object in a projection cell's locals, calls no Python
  builtin there and builds no container, under the two directives the build tool writes.
* C4 on the committed points: the compiled model computes what modelx computes, every cell
  at every argument a full modelx sweep caches, every raise and every ``Data`` array, bit
  for bit on x86-64.
* The release: ``run_sec.py --block``, run compiled, holds one point's ItemSpace at a time
  (F5, K2).

The allowlist of cells that stay Python is R17's, :func:`sec_support.reporting_cells`:
``model_point``, the ``result_*`` reports, the ``check_*`` checks, and the label accessors
the registry entry names under ``"reporting"``.  C3, C4 and the release are marked
``cython``.  They compile each model once a session, into a temporary directory
(``conftest.sec_build``), never into the tree (D12), and run the compiled package in child
processes only.  Without modelx-cython or a C compiler they skip, and the ``cython`` CI job,
which sets ``USLIB_REQUIRE_CYTHON=1``, fails a skip (D13).  Each product module adds what
is its own: C4 on its splice grid and at its contract's extremes, its compiled refusals,
its deepest cold call on a 1 MiB stack, and its runner compiled.
"""
import itertools

import modelx as mx
import pandas as pd
import pytest

from sec_support import (
    SEC_SPECS, c_faults, compiled_case, compiled_mismatches, release_faults,
    reporting_cells, spec_faults, static_faults, typing_faults)
from us_registry import MODELS, is_sec, meta, model_path, point_keys, projection

SEC_MODELS = sorted(n for n in MODELS if is_sec(n))
EC_MODELS = sorted(n for n in SEC_MODELS if meta(n).get("stage") == "EC")

# The points the release test runs: the committed table, copied until the block holds this
# many, so that a runner keeping what it releases is seen to hold a block's worth.  A
# product whose table has companion files keyed by point runs its committed table alone.
RELEASE_POINTS = 120

_names = itertools.count(1)


@pytest.fixture(scope="module", params=EC_MODELS)
def name(request):
    """Each SEC model registered at stage ``"EC"`` in turn."""
    return request.param


@pytest.fixture(scope="module")
def model(name):
    """The model, read in place under a name of its own, and closed afterwards."""
    m = mx.read_model(model_path(name), name=f"{name}_ec_{next(_names)}")
    yield m
    m.close()


@pytest.mark.parametrize("sec_name", SEC_MODELS)
def test_only_a_compiled_model_declares_reporting_cells(sec_name):
    """``"reporting"`` is a stage-``"EC"`` key, a tuple of cell names (us_registry).

    It widens the typing guard's allowlist, so it is declared only where the guard runs,
    and only as names; :func:`test_no_projection_formula_holds_python_machinery` checks
    that each is a ``Projection`` cell.
    """
    entry = meta(sec_name)
    if "reporting" not in entry:
        return
    assert entry.get("stage") == "EC", (
        f"{sec_name} declares reporting cells at stage {entry.get('stage')!r}; they are "
        f"the compiled model's allowlist, and the key belongs to stage 'EC'")
    declared = entry["reporting"]
    assert isinstance(declared, tuple) and all(isinstance(c, str) for c in declared), (
        f"{sec_name}: reporting is {declared!r}, not a tuple of cell names")


def test_no_projection_formula_holds_python_machinery(name, model):
    """C5: no ``Projection`` formula outside R17's allowlist holds what C cannot run.

    Each is parsed, and none may refer to ``pd``, ``np`` or another module, read
    ``.loc``, ``.iloc``, ``.values`` and the like, call a reporting cell, hold text
    outside its docstring and its ``raise`` messages, read a Reference holding text, call
    ``len()``, or hold a generator, a comprehension, a ``lambda`` or a nested ``def``
    (R10-R13).  Outside its refusals none may call anything but a cell, a ``Data``
    vector and the builtins Cython turns into C, ``int``, ``float``, ``bool``, ``abs``,
    ``min``, ``max`` and ``range``, or build a list, a dict, a set or a tuple: a
    ``round`` or a ``sum`` is a call into Python in a cell its declaration types as C
    (R12, R16).  Every ``Data`` cell such a formula calls must return an int64 or float64
    array or a Python int or float, found by evaluating it on the committed inputs, and
    an array must be read at once, by element; so must every ``Data`` array another
    ``Data`` cell reads (R5, R13).  And no cell may share its name with what a call with
    keywords calls anywhere in the model, pandas' and numpy's methods included, because
    mx2cy keeps every cell of such a name a Python method (R12).  The typing guard sees
    most of these only once compiled; this sees them in every suite.

    The registry's ``"reporting"`` widens the allowlist, so each cell it names must be
    what R17 admits, a label accessor: a ``Projection`` cell returning the model point's
    column of its own name, exactly as the table holds it, on every committed point.
    """
    found = static_faults(model, reporting=reporting_cells(name, model.Projection))
    labels = [cell for cell in meta(name).get("reporting", ())
              if cell in model.Projection.cells]
    for key, point_id in zip(point_keys(model), model.Data.model_point_table().index):
        proj = projection(model, key)
        row = proj.model_point()
        for cell in labels:
            got = proj.cells[cell]()
            want = row[cell] if cell in row.index else "no such column"
            if not (isinstance(got, str) and got == want):
                found.append(f"Projection.{cell} returns {got!r} at point {point_id}, "
                             f"where the label accessor returns the point's {cell!r} "
                             f"column, {want!r} (R17)")
    assert not found, f"{name}: {len(found)} faults, first:\n  " + "\n  ".join(found[:20])


@pytest.mark.cython
def test_every_projection_cell_compiles_to_a_c_type(name, model, sec_build):
    """C3: the compiled model's declarations, and its generated C, are C.

    Read from the build's ``_mx_classes.pxd``: every ``Projection`` cell outside R17's
    allowlist is compiled, returns a C ``bint``, ``long long`` or ``double``, takes only
    those, and keeps no Python dict for a cache; every ``Data`` cell the S twin does not
    have returns a typed memoryview of int64 or float64, or a C scalar (R5), but a reader
    of an input file, which stays Python as the S model's do.  Then the spec: every
    compiled cell taking C integers has a size for its parameters in ``spec_sec.py``, a
    cache of exactly that size, and every size is taken, since mx2cy ignores a misspelt
    key without a word (F4).  And the generated C, which no declaration shows: no
    projection formula keeps a Python object among its locals, calls a Python builtin
    other than an exception it raises, or builds a list, dict or set, and every translated
    space module begins with ``infer_types=True`` and ``cpow=True``, without which an
    integer local is a Python object and a power drifts from modelx's.
    """
    build = sec_build(name)
    twin = mx.read_model(model_path(meta(name)["twin"]), name=f"{name}_ec_twin_"
                         f"{next(_names)}")
    try:
        new_data = set(model.Data.cells) - set(twin.Data.cells)
    finally:
        twin.close()
    reporting = reporting_cells(name, model.Projection)
    found = (typing_faults(build, model, reporting=reporting, new_data=new_data)
             + spec_faults(build, model_path(name).parent / "spec_sec.py")
             + c_faults(build, reporting=reporting))
    assert not found, f"{name}: {len(found)} faults, first:\n  " + "\n  ".join(found[:20])


@pytest.mark.cython
def test_the_compiled_model_computes_what_modelx_computes(name, sec_build, tmp_path):
    """C4 on the committed points: compiled, every cell is modelx's, at every argument.

    The build goes beside a copy of the committed inputs (``sec_support.compiled_case``),
    where modelx reads them too.  modelx sweeps every point fully, every cell without
    parameters, the reports among them, and then every monthly cell at every month of the
    frame and the month after, and every value it caches is compared with the compiled
    model's at the same arguments, every timing included, to 1e-12 relative, floored at
    the cell's magnitude, or identically on x86-64, where the compiled model does modelx's
    arithmetic in modelx's order (``sec_support.exact_here``); a bool or an int must keep
    its kind, a raise must meet the same raise, and every ``Data`` array must be identical
    (``sec_support.compiled_mismatches``).  The branches the committed points miss are
    each product's splice grid's.
    """
    build = sec_build(name)
    folder = compiled_case(build, tmp_path / "committed")
    found = compiled_mismatches(build, folder)
    assert not found, f"{name}: {len(found)} mismatches, first:\n  " + "\n  ".join(found)


def _block(name, points):
    """The committed SEC table, copied until it holds ``points`` rows, renumbered from 1.

    A product whose table has companion files keyed by point keeps its committed table,
    which the companions describe.
    """
    spec = SEC_SPECS.get(name)
    filename = spec.model_point_file if spec is not None else "model_point_table_sec.csv"
    table = pd.read_csv(model_path(name).parent / filename, index_col="point_id")
    if spec is not None and spec.companions:
        return table
    copies = -(-points // len(table))
    block = pd.concat([table] * copies)
    block.index = pd.Index(range(1, len(block) + 1), name="point_id")
    return block


@pytest.mark.cython
def test_a_block_run_releases_each_compiled_point(name, sec_build, tmp_path):
    """``run_sec.py --block``, compiled, holds one point's ItemSpace at a time (F5, K2).

    A compiled ItemSpace carries every cell's cache in its C struct, about 430 KB for
    Term, so a block that kept them would hold the block's worth.  And deleting one frees
    nothing on its own: it refers to itself, as its own ``_space`` and in its own
    ``_mx_roots``, cycles only the cyclic collector frees.  The product's runner, run on
    a block of :data:`RELEASE_POINTS` copied points with ``--build`` on the session's
    build, in an interpreter of its own, must therefore leave no ItemSpace but the base
    alive after each collection it makes once it has frozen what lived before the block,
    make one for every point, and leave none alive at the end, frozen or not
    (``sec_support.release_faults``).  A control then deletes an ItemSpace and finds it
    alive until a collection: if modelx-cython stops holding it in a cycle, that fails,
    and says the collection can go.
    """
    build = sec_build(name)
    block = _block(name, RELEASE_POINTS)
    case = tmp_path / "block"
    compiled_case(build, case, model_points=block)
    runner = model_path(name).parent / "run_sec.py"
    found = release_faults(case, build.package.name, runner, points=len(block))
    assert not found, f"{name}: " + "\n  ".join(found)
