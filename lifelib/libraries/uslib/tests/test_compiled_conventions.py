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
  element, at no negative literal index.  Read from the formulas, so it runs in every
  suite, with or without a compiler.
* The sample: ``sample_sec.py`` calls every cell the registry names under ``"engine"``,
  which no compiled cell calls, so that each is traced.  Read statically.
* C3, the typing guard: the generated declarations say every projection cell returns and
  takes a C ``bint``, ``long long`` or ``double`` and caches in a C array of the spec's
  size, every new ``Data`` vector but a reader is a typed memoryview or a C scalar, and
  the generated C keeps no Python object in a projection cell's locals, calls no Python
  builtin there and builds no container, under the two directives the build tool writes;
  and every reporting cell a reader asks for, a label among them, returns ``object``.
* C4 on the committed points: the compiled model computes what modelx computes, every cell
  at every argument a full modelx sweep caches, every raise and every ``Data`` array, bit
  for bit on x86-64.
* The release: ``run_sec.py --block``, run compiled, holds one point's ItemSpace at a time
  (F5, K2).
* The block's sum: ``run_sec.py``'s running sum is ``groupby``'s, bit for bit, on the
  committed points' frames, run in modelx, with or without a compiler.
* The build tool: each runner and each ``model-sec.md`` build with the library's own
  ``build_sec_cy.py``, at its root, where lifelib and every ``lifelib.create()`` copy have
  it too, and the tool names the modelx-cython ``requirements-cython.txt`` pins.  Read
  statically.

The allowlist of cells that stay Python is R17's, :func:`sec_support.reporting_cells`:
``model_point``, the ``result_*`` reports, the ``check_*`` checks, and the label accessors
the registry entry names under ``"reporting"``, and S's cells of float parameters it
names under ``"engine"``, which no compiled cell calls (R14).  A builtin a compiled cell
still calls, R16's ``round`` of a projected amount, is admitted in that cell alone, by the
registry entry's ``"python_calls"``, which C3 and C5 read.  C3, C4 and the release are
marked ``cython``.  They compile each model once a session, into a temporary directory
(``conftest.sec_build``), never into the tree (D12), and run the compiled package in child
processes only.  Without modelx-cython or a C compiler they skip, and the ``cython`` CI job,
which sets ``USLIB_REQUIRE_CYTHON=1``, fails a skip (D13).  Each product module adds what
is its own: C4 on its splice grid and at its contract's extremes, its compiled refusals,
its deepest cold call on a 1 MiB stack, and its runner compiled.

The ``cython`` CI job runs these with the product module's in the model's own leg, one
shard to a leg (``sec_support.cython_shards``), and
:func:`test_the_cython_job_runs_every_shard`, which needs no compiler, holds the job's
matrix to the registry, so that no model at stage ``"EC"`` is left out of it.  Three more
read the workflow the same way, each for a job that could otherwise go green and prove
nothing: the ``cython`` job fails a skip and collects uslib's suite alone, the ``test`` job
runs ``tools/check_sec_harness.py``, and the ``sec`` job runs every SEC model's module,
which the ``test`` job leaves out.
"""
import ast
import builtins
import itertools
import re
import shlex
import textwrap
import types

import modelx as mx
import pandas as pd
import pytest

from sec_support import (
    C_CALLS, SEC_SPECS, c_faults, compiled_case, compiled_mismatches, cython_shards,
    release_faults, reporting_cells, spec_faults, static_faults, typing_faults)
from sec_support import label_faults, reporting_columns_faults
from sec_support import engine_faults
from sec_support import (
    block_sum_faults, labels_refusing_non_text, object_cells, object_return_faults,
    pxd_declarations, runner_add, sample_engine_faults)
from us_registry import LIB, MODELS, is_sec, meta, model_path, point_keys, projection

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


@pytest.mark.parametrize("sec_name", SEC_MODELS)
def test_reporting_columns_name_a_shape_for_a_declared_label(sec_name):
    """``"reporting_columns"`` is a stage-``"EC"`` key naming a shape per label (M23).

    It says what a label accessor of ``"reporting"`` returns where that is not its point's
    column of its own name (us_registry), so it widens what C5's label check accepts: it
    is declared only where that check runs, each key a label ``"reporting"`` names, each
    value a column, a dict of argument to column, or a pair of a column and a dict of
    value to label (``sec_support.reporting_columns_faults``).  That each entry is taken,
    and each column it names is the table's, the label check holds on the model.
    """
    found = reporting_columns_faults(meta(sec_name))
    assert not found, f"{sec_name}: " + "; ".join(found)


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
    most of these only once compiled; this sees them in every suite.  A builtin the
    registry's ``"python_calls"`` admits in a cell, R16's ``round``, is no fault there
    (:func:`test_python_calls_are_declared_by_cell`).

    The registry's ``"reporting"`` widens the allowlist, so each cell it names must be
    what R17 admits, a label accessor: a ``Projection`` cell returning the model point's
    column of its own name, exactly as the table holds it, on every committed point, or
    the column the entry's ``"reporting_columns"`` names for it, a blank column being the
    label's value where the label returns it as read; and each such entry must be taken
    (``sec_support.label_faults``).
    """
    found = static_faults(model, reporting=reporting_cells(name, model.Projection),
                          python_calls=meta(name).get("python_calls", {}))
    found += label_faults(model, name)
    assert not found, f"{name}: {len(found)} faults, first:\n  " + "\n  ".join(found[:20])


@pytest.mark.parametrize("sec_name", SEC_MODELS)
def test_python_calls_are_declared_by_cell(sec_name):
    """``"python_calls"`` admits a Python builtin in a named cell, and each is taken.

    Or a module's function, by its dotted name, ``"math.erf"``: ``RILA_US_SEC``'s pricing
    keeps Python's ``math`` (M25), so a name ``"<module>.<function>"`` is valid where
    ``<module>`` is a Reference of ``Projection`` holding a module with that function.

    R16 keeps one Python call in a projection formula, ``round`` of a projected amount,
    which cannot be precomputed, and the registry's ``"python_calls"`` admits it by cell
    (us_registry), so that C3 and C5 pass that call in that cell and fault it in every
    other.  So the key is a stage-``"EC"`` one, as ``"reporting"`` is, a dict of
    ``Projection`` cell names, none of them reporting, since a reporting cell may call
    Python already, each to a non-empty tuple of Python builtins, none of which C3 and C5
    admit everywhere already.  And each admitted name is called in its cell's formula, so
    that no admission outlives the call it was made for, as every size in a spec must be
    taken.

    The other way round, which holds for a model without the key too: at stage ``"EC"``,
    no other compiled formula calls a builtin outside ``C_CALLS``, outside its ``raise``
    statements, so that no admission is missing, and a model without the key needs none.
    Before stage ``"EC"`` nothing compiles, so a model there declares no admission.
    """
    entry = meta(sec_name)
    declared = entry.get("python_calls", {})
    if "python_calls" in entry:
        assert entry.get("stage") == "EC", (
            f"{sec_name} declares python_calls at stage {entry.get('stage')!r}; they widen "
            f"the compiled model's checks, and the key belongs to stage 'EC'")
        assert isinstance(declared, dict) and declared, (
            f"{sec_name}: python_calls is {declared!r}, not a dict of cells to builtins")
    if entry.get("stage") != "EC":
        assert declared == {}, declared
        return
    model = mx.read_model(model_path(sec_name), name=f"{sec_name}_calls_{next(_names)}")
    try:
        proj = model.Projection
        reporting = reporting_cells(sec_name, proj)
        found = []
        for cell in sorted(set(proj.cells) - set(reporting) - set(declared)):
            tree = ast.parse(textwrap.dedent(proj.cells[cell].formula.source))
            raised = {id(node) for statement in ast.walk(tree)
                      if isinstance(statement, ast.Raise) for node in ast.walk(statement)}
            for node in ast.walk(tree):
                if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                        and id(node) not in raised and hasattr(builtins, node.func.id)
                        and node.func.id not in C_CALLS
                        and node.func.id not in proj.cells):
                    found.append(f"{cell} calls {node.func.id}(), which no admission names")
        for cell, names in declared.items():
            if cell not in proj.cells:
                found.append(f"{cell} is not a Projection cell")
                continue
            if cell in reporting:
                found.append(f"{cell} is a reporting cell, which may call Python already")
            if not (isinstance(names, tuple) and names
                    and all(isinstance(n, str) for n in names)):
                found.append(f"{cell}: {names!r} is not a non-empty tuple of names")
                continue
            tree = ast.parse(textwrap.dedent(proj.cells[cell].formula.source))
            called = {node.func.id for node in ast.walk(tree)
                      if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)}
            called |= {f"{node.func.value.id}.{node.func.attr}" for node in ast.walk(tree)
                       if isinstance(node, ast.Call)
                       and isinstance(node.func, ast.Attribute)
                       and isinstance(node.func.value, ast.Name)}
            for n in names:
                head, _, tail = n.partition(".")
                module = proj.refs.get(head) if tail else None
                if tail and not (isinstance(module, types.ModuleType)
                                 and callable(getattr(module, tail, None))):
                    found.append(f"{cell}: {n} is not a function of a module Projection "
                                 f"holds as a Reference")
                elif not tail and (not hasattr(builtins, n) or n in C_CALLS):
                    found.append(f"{cell}: {n} is not a Python builtin outside C_CALLS")
                elif n not in called:
                    found.append(f"{cell}: its formula calls no {n}(), so the admission "
                                 f"is stale")
    finally:
        model.close()
    assert not found, f"{sec_name}: python_calls: " + "; ".join(found)


@pytest.mark.parametrize("sec_name", SEC_MODELS)
def test_engine_cells_are_declared_by_name(sec_name):
    """``"engine"`` admits S's cells of float parameters by name, none called by C (R14).

    R14 lets an SEC model keep a cell of S's that takes a float, for a reader and for T1,
    where no projection cell calls it: compiled, it keeps a Python dict for a cache, so the
    registry names it under ``"engine"``, and :func:`sec_support.reporting_cells` admits it
    to C3 and C5 as a reporting cell.  So the key is a stage-``"EC"`` one, as
    ``"reporting"`` is, a non-empty tuple of ``Projection`` cell names, none of them in
    ``"reporting"``, whose check that each returns a column would not hold; each takes a
    parameter that no ``spec_sec.py`` size names, since a cell keyed by sized ints compiles
    to C and needs no admission, or takes none and returns a list, a dict or a DataFrame,
    which no C type holds, as ``DIA_US_SEC``'s ``qlac_flags`` and premium schedule do
    (M24); and no ``Projection`` formula calls one but another
    engine cell, as ``mgsv_rate_is_compliant`` calls ``mgsv_rate_statutory``, so that every
    cell a projection runs is C.  Before stage ``"EC"`` nothing compiles, so a model there
    declares none.
    """
    entry = meta(sec_name)
    if "engine" not in entry:
        return
    assert entry.get("stage") == "EC", (
        f"{sec_name} declares engine cells at stage {entry.get('stage')!r}; they widen the "
        f"compiled model's allowlist, and the key belongs to stage 'EC'")
    declared = entry["engine"]
    assert isinstance(declared, tuple) and declared and all(
        isinstance(c, str) for c in declared), (
        f"{sec_name}: engine is {declared!r}, not a non-empty tuple of cell names")
    spec = ast.literal_eval(
        (model_path(sec_name).parent / "spec_sec.py").read_text(encoding="utf-8"))
    sized = set()
    for key in spec["spaces"]["Projection"]["cells_param_size"]:
        sized.update(key if isinstance(key, tuple) else (key,))
    model = mx.read_model(model_path(sec_name), name=f"{sec_name}_engine_{next(_names)}")
    try:
        found = engine_faults(model.Projection, declared, sized,
                              entry.get("reporting", ()))
    finally:
        model.close()
    assert not found, f"{sec_name}: engine: " + "; ".join(found)


def test_the_sample_calls_every_engine_cell(name, model):
    """``sample_sec.py`` calls every cell the registry names under ``"engine"`` (R14).

    No compiled cell calls an engine cell, so only the sample's own call types one: an
    engine cell the sample stops calling is traced at nothing and compiles with object
    parameters, and the typing guard still passes, since it admits an engine cell's dict
    cache by name (M25).  So the sample's code is read, statically, for a call of each
    (``sec_support.sample_engine_faults``): by attribute, by ``getattr`` with its name,
    or by ``getattr`` over a set of names that holds it; and one taking no parameter, by
    the loop that calls every cell of no parameter, too.  A model without the key passes.
    """
    engine = meta(name).get("engine", ())
    source = (model_path(name).parent / "sample_sec.py").read_text(encoding="utf-8")
    parameterless = [cell for cell in engine if cell in model.Projection.cells
                     and not model.Projection.cells[cell].parameters]
    found = sample_engine_faults(source, engine, parameterless)
    assert not found, f"{name}: " + "; ".join(found)


def test_the_runner_sums_the_block_as_groupby_does(name):
    """``run_sec.py --block``'s running sum is pandas' ``groupby`` sum, bit for bit.

    A block run keeps one point's frame at a time, so it sums the frames as it goes,
    compensated, with its ``add``, so that the block is the committed points' frames
    concatenated and summed by ``t``, to the last bit, which the printed block cannot
    show.  So ``add`` is read from the runner and run on the committed points' frames,
    which must be finite, and its sum compared with ``groupby``'s by ``np.array_equal``
    (``sec_support.block_sum_faults``, M23).  Every product's runner sums alike, so this
    is one convention.  A plain running sum departs from ``groupby``'s on every product's
    committed points, so the comparison can fail on each, and that is held too.
    """
    def plain(total, compensation, frame):
        total[:len(frame)] += frame

    add = runner_add(model_path(name).parent / "run_sec.py")
    model = mx.read_model(model_path(name), name=f"{name}_block_{next(_names)}")
    try:
        frames = [projection(model, key).result_cf() for key in point_keys(model)]
        found = block_sum_faults(add, frames)
        naive = block_sum_faults(plain, frames)
    finally:
        model.close()
    assert not found, f"{name}: " + "; ".join(found)
    assert naive and naive[0].startswith("the running sum departs"), (
        f"{name}: a plain running sum is groupby's on the committed points, so the "
        f"comparison cannot fail there: {naive}")


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
    integer local is a Python object and a power drifts from modelx's.  A builtin the
    registry's ``"python_calls"`` admits in a cell is no fault in that cell's C.  And the
    reporting cells a reader asks for, ``model_point``, the ``result_*`` reports and the
    label accessors, return ``object`` where they compile: a label the sample traced on
    text alone compiles to ``str``, and raises on a label ``Data`` holds as a number or a
    blank, where modelx returns it (``sec_support.object_return_faults``, M22).  A label
    compiled to ``str`` passes only where its own formula refuses its point's column blank
    and as a number, ``Data``'s checks aside (``sec_support.labels_refusing_non_text``),
    as a label validating its column does, which returns text or raises in either
    engine.
    """
    build = sec_build(name)
    twin = mx.read_model(model_path(meta(name)["twin"]), name=f"{name}_ec_twin_"
                         f"{next(_names)}")
    try:
        new_data = set(model.Data.cells) - set(twin.Data.cells)
    finally:
        twin.close()
    reporting = reporting_cells(name, model.Projection)
    readers = object_cells(name, model.Projection)
    declared, _ = pxd_declarations(build.pxd, "Projection")
    as_text = {cell for cell in readers & set(meta(name).get("reporting", ()))
               if cell in declared and declared[cell][0] != "object"}
    refusing = labels_refusing_non_text(name, as_text)
    found = (typing_faults(build, model, reporting=reporting, new_data=new_data)
             + object_return_faults(build, readers, refusing)
             + spec_faults(build, model_path(name).parent / "spec_sec.py")
             + c_faults(build, reporting=reporting,
                        python_calls=meta(name).get("python_calls", {})))
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


# The workflow that runs the cython job, in the repository that holds this library.
WORKFLOW = LIB.parents[2] / ".github" / "workflows" / "tests.yml"


def _job(text, job):
    """The lines of ``job`` in the workflow ``text``, or ``None`` where it has no such job.

    Read as text, since the suite's requirements hold no YAML parser: a job is a key
    indented two spaces under ``jobs:``, and runs to the next key indented two spaces or
    fewer.
    """
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.rstrip() == f"  {job}:":
            end = next((j for j in range(i + 1, len(lines))
                        if re.match(r"\s{0,2}[^\s#]", lines[j])), len(lines))
            return lines[i + 1:end]
    return None


def _matrix_list(job, key):
    """The flow sequence ``key: [a, b, ...]`` in ``job``'s lines, which may wrap, or
    ``None``."""
    for i, line in enumerate(job):
        found = re.match(rf"\s+{key}:\s*\[(.*)", line)
        if found:
            text = found.group(1)
            for more in job[i + 1:]:
                if "]" in text:
                    break
                text += more
            items = text.split("]")[0].split(",")
            return [item.strip().strip("'\"") for item in items if item.strip()]
    return None


@pytest.mark.parametrize("sec_name", EC_MODELS)
def test_the_runner_and_its_page_build_with_the_library_s_own_tool(sec_name):
    """``run_sec.py --cython`` builds with the library's own ``build_sec_cy.py``, and the
    product's ``model-sec.md`` builds with it too (lifelib-dev/lifelib issue 195).

    The tool sits at the library's root, beside ``products/``, so that it goes wherever the
    library goes.  While it lived in the source repository's ``tools/``, which lifelib
    does not take, every runner looked for it there and every page built with it there,
    and in lifelib neither could build.  So the runner's ``_tool`` is read from its source,
    which runs the model when imported, and run on the product directory: it must give the
    library's tool, which must be there.  And the page must build with that tool, from the
    library's folder, ``python build_sec_cy.py <product>``, and name no ``tools/`` copy of
    it.  Read statically, so it runs in every suite, with or without a compiler.
    """
    product = model_path(sec_name).parent
    tree = ast.parse((product / "run_sec.py").read_text(encoding="utf-8"))
    found = [node for node in tree.body
             if isinstance(node, ast.FunctionDef) and node.name == "_tool"]
    assert len(found) == 1, f"{sec_name}'s run_sec.py defines _tool {len(found)} times"
    space = {"HERE": product}
    exec(compile(ast.Module(found, []), "run_sec.py", "exec"), space)
    tool = space["_tool"]()
    assert tool == LIB / "build_sec_cy.py" and tool.is_file(), (sec_name, tool)
    page = (product / "model-sec.md").read_text(encoding="utf-8")
    assert f"python build_sec_cy.py {product.name}" in page, (
        f"{sec_name}'s model-sec.md builds with no python build_sec_cy.py {product.name}")
    assert "tools/build_sec_cy.py" not in page, (
        f"{sec_name}'s model-sec.md names tools/build_sec_cy.py, which lifelib has not")


def test_the_build_tool_names_the_modelx_cython_the_requirements_pin():
    """``build_sec_cy.py``'s ``MODELX_CYTHON`` is what ``requirements-cython.txt`` pins.

    The tool names that release where modelx-cython is missing, so that a library away from
    its source repository, in lifelib or in a ``lifelib.create()`` copy, where there is no
    requirements file, still installs the release the compile tests run.  The source
    repository pins it in ``requirements-cython.txt``, and moves the pin on purpose (the
    plan's K1); the tool's line must move with it.  Both are read statically.  It skips
    where the requirements file is absent, as in lifelib; uklib's tool is this one, byte
    for byte, which uklib's suite holds.
    """
    requirements = LIB.parents[2] / "requirements-cython.txt"
    if not requirements.is_file():
        pytest.skip("requirements-cython.txt is the source repository's, and it is absent")
    pins = [line.split("#", 1)[0].strip()
            for line in requirements.read_text(encoding="utf-8").splitlines()]
    pins = [pin for pin in pins if pin.startswith("modelx-cython")]
    tool = ast.parse((LIB / "build_sec_cy.py").read_text(encoding="utf-8"))
    named = [node.value.value for node in tool.body
             if isinstance(node, ast.Assign) and len(node.targets) == 1
             and getattr(node.targets[0], "id", None) == "MODELX_CYTHON"
             and isinstance(node.value, ast.Constant)]
    assert len(pins) == 1 and named == pins, (pins, named)


def test_the_cython_job_runs_every_shard():
    """The ``cython`` CI job's matrix lists exactly the shards the registry makes (D13).

    The job runs one shard of the compile tests to a leg, named by ``USLIB_CYTHON_SHARD``,
    so that no leg compiles every model: ``toolchain``, and for each SEC model at stage
    ``"EC"`` its product directory (``sec_support.cython_shards``), whose module,
    ``test_<shard>_us_sec.py``, holds the model's own compile tests.  A model moved to
    stage ``"EC"`` without its shard in the matrix would have its compile tests run in no
    leg, and every leg green, so its C step adds the shard, and this fails until it does;
    a shard left in the matrix after its model leaves stage ``"EC"`` would fail its leg
    with nothing selected, and this says so first.  Every leg must pass the shard to
    pytest.  It runs in the ``test`` job, which needs no compiler, and skips where the
    workflow or ``tools/build_sec_cy.py`` is absent, as from a ``lifelib.create()`` copy
    or from lifelib, whose CI runs no ``cython`` job.
    """
    tool = LIB.parents[2] / "tools" / "build_sec_cy.py"
    if not (WORKFLOW.is_file() and tool.is_file()):
        pytest.skip("the cython job's workflow and tools/build_sec_cy.py are this "
                    "repository's, and one is absent")
    job = _job(WORKFLOW.read_text(encoding="utf-8"), "cython")
    assert job is not None, f"{WORKFLOW.name} has no cython job"
    listed = _matrix_list(job, "shard")
    assert listed is not None, "the cython job's matrix has no shard: [...] list"
    want = list(cython_shards())
    twice = sorted({shard for shard in listed if listed.count(shard) > 1})
    missing = [shard for shard in want if shard not in listed]
    extra = [shard for shard in listed if shard not in want]
    assert not (twice or missing or extra), (
        f"the cython job's matrix lists the shards {listed}, and the registry makes "
        f"{want}: add {missing}, remove {extra}, list once {twice}; a model's shard is "
        f"added in the commit that moves it to stage 'EC'")
    for shard in want[1:]:
        module = LIB / "tests" / f"test_{shard}_us_sec.py"
        assert module.is_file(), f"shard {shard}: its module {module.name} is absent"
    passed = r"\s+USLIB_CYTHON_SHARD:\s*\$\{\{\s*matrix\.shard\s*\}\}\s*"
    assert any(re.fullmatch(passed, line) for line in job), (
        "the cython job does not set USLIB_CYTHON_SHARD to its matrix's shard")


# uslib's suite: the one tree the cython job collects, and the home of every module the sec
# job runs.
US_TESTS = "lifelib/libraries/uslib/tests"

# What sets a variable to '1' on a sec leg of the full grid alone, with its whitespace taken
# out.
ON_THE_FULL_GRID = "${{matrix.grid=='full'&&'1'||''}}"


def _steps(job):
    """The steps of ``job``'s lines, each ``{key: value}`` at the step's own level.

    A block scalar, ``run: |`` or ``run: >-``, has its lines joined by spaces, and so do a
    step's ``env:`` variables, one ``NAME: value`` after another; comments and blank lines
    are left out.  Read as text, as :func:`_job` reads the job.
    """
    lines = [line for line in job if line.strip() and not line.lstrip().startswith("#")]
    start = next((i for i, line in enumerate(lines)
                  if re.fullmatch(r"\s+steps:\s*", line)), None)
    if start is None or start + 1 == len(lines) or not lines[start + 1].lstrip().startswith(
            "- "):
        return []
    level = len(lines[start + 1]) - len(lines[start + 1].lstrip())
    items = []
    for line in lines[start + 1:]:
        indent = len(line) - len(line.lstrip())
        if indent < level or (indent == level and not line.lstrip().startswith("- ")):
            break
        if indent == level:
            items.append([" " * (level + 2) + line.lstrip()[2:]])
        else:
            items[-1].append(line)
    steps = []
    for item in items:
        keys, key = {}, None
        for line in item:
            found = re.fullmatch(rf" {{{level + 2}}}([\w-]+):\s*(.*?)\s*", line)
            if found:
                key, value = found.groups()
                keys[key] = "" if value in ("|", "|-", ">", ">-") else value
            elif key is not None:
                keys[key] = f"{keys[key]} {line.strip()}".strip()
        steps.append(keys)
    return steps


def _variable(job, step, name):
    """The value ``step`` of ``job`` runs ``name`` under, as written, or ``None``: the
    step's own ``env:`` where it sets it, and else the job's, which every step sees."""
    seen, inside = [], False
    for line in job:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if re.fullmatch(r"    env:\s*", line):
            inside = True
        elif inside and len(line) - len(line.lstrip()) > 4:
            seen.append(line.strip())
        else:
            inside = False
    value = r"(\$\{\{.*?\}\}|'[^']*'|\"[^\"]*\"|\S+)"
    given = re.findall(rf"(?<!\w){re.escape(name)}:\s*{value}",
                       " ".join(seen + [step.get("env", "")]))
    return given[-1] if given else None


def _pytest_args(command):
    """``(marks, paths)`` of the ``pytest`` a step's ``run`` runs, or ``None`` where it
    runs none: each ``-m`` expression, and each path pytest collects from."""
    words = shlex.split(re.sub(r"\$\{\{.*?\}\}", lambda m: "".join(m.group(0).split()),
                               command))
    if "pytest" not in words:
        return None
    valued = {"-k", "-p", "-c", "-o", "-n", "--rootdir", "--ignore", "--ignore-glob",
              "--deselect", "--durations", "--maxfail", "--confcutdir"}
    marks, paths = [], []
    rest = iter(words[words.index("pytest") + 1:])
    for word in rest:
        if word == "-m":
            marks.append(next(rest, ""))
        elif word.startswith("-m") and not word.startswith("--"):
            marks.append(word[2:])
        elif word in valued:
            next(rest, None)
        elif not word.startswith("-"):
            paths.append(word)
    return marks, paths


def test_the_cython_job_fails_a_skip_and_collects_uslib_alone():
    """The ``cython`` job runs pytest under ``USLIB_REQUIRE_CYTHON: '1'``, with ``-m
    cython``, over ``lifelib/libraries/uslib/tests`` and no other library's tests (D13).

    Each is a way its legs could be green and prove nothing.  Without the variable a
    compile test that finds no compiler skips, and ``conftest.py`` fails such a skip only
    under it.  Without ``-m cython`` a leg runs the rest of the suite beside its shard, the
    ``_us_sec`` grids among them, which took the ``test`` job's legs to their timeout.
    Over another library's tests it runs that library's compile tests under uslib's
    variables, which govern none of them, and none of uslib's.  The variable is read as
    the step that runs pytest sees it, the job's or its own.  It skips as
    :func:`test_the_cython_job_runs_every_shard` does.
    """
    tool = LIB.parents[2] / "tools" / "build_sec_cy.py"
    if not (WORKFLOW.is_file() and tool.is_file()):
        pytest.skip("the cython job's workflow and tools/build_sec_cy.py are this "
                    "repository's, and one is absent")
    job = _job(WORKFLOW.read_text(encoding="utf-8"), "cython")
    assert job is not None, f"{WORKFLOW.name} has no cython job"
    runs = [step for step in _steps(job) if _pytest_args(step.get("run", "")) is not None]
    assert len(runs) == 1, f"the cython job has {len(runs)} steps that run pytest, not one"
    step = runs[0]
    required = _variable(job, step, "USLIB_REQUIRE_CYTHON")
    assert required is not None and required.strip("'\"") == "1", (
        f"the cython job runs pytest under USLIB_REQUIRE_CYTHON {required!r}, not '1': a "
        f"compile test that skips there would pass")
    marks, paths = _pytest_args(step["run"])
    assert marks == ["cython"], (
        f"the cython job runs pytest with -m {marks}, not -m cython: {step['run']}")
    other = [path for path in paths
             if path.rstrip("/") != US_TESTS and not path.startswith(US_TESTS + "/")]
    assert paths and not other, (
        f"the cython job's pytest collects {paths or 'the repository'}, not {US_TESTS} "
        f"alone: {step['run']}")


def test_the_test_job_holds_sec_support_to_uklib_s_copy():
    """CI's ``test`` job has a step that runs ``python tools/check_sec_harness.py``, on no
    condition (UKLIB-SEC-PLAN.md U3).

    The check holds this suite's harness, ``sec_support.py``, to uklib's copy,
    ``uk_sec_support.py``, in every function, class and constant the two share, and each
    one's product specs to their rules.  Each library's suite passes on its own copy, so
    without the step a fix to one that never reaches the other is green, and so it is with
    a step that a condition other than ``always()`` or the default ``success()`` can skip,
    or that may fail under ``continue-on-error``.  uklib's suite holds the same step; this
    holds it in uslib's, so that uslib's suite run alone holds it too.  It skips where the
    workflow or the tool is absent, as from a ``lifelib.create()`` copy or from lifelib.
    """
    tool = LIB.parents[2] / "tools" / "check_sec_harness.py"
    if not (WORKFLOW.is_file() and tool.is_file()):
        pytest.skip("the test job's workflow and tools/check_sec_harness.py are this "
                    "repository's, and one is absent")
    job = _job(WORKFLOW.read_text(encoding="utf-8"), "test")
    assert job is not None, f"{WORKFLOW.name} has no test job"
    runs = [step for step in _steps(job)
            if re.fullmatch(r"python3?\s+tools/check_sec_harness\.py", step.get("run", ""))]
    assert runs, "no step of the test job runs python tools/check_sec_harness.py"

    def gates(step):
        condition = re.sub(r"\$\{\{\s*(.*?)\s*\}\}", r"\1", step.get("if", "")).strip()
        return (condition in ("", "always()", "success()")
                and step.get("continue-on-error", "false") == "false")

    assert any(gates(step) for step in runs), (
        f"the test job runs tools/check_sec_harness.py only conditionally: {runs}")


def test_the_sec_job_runs_every_sec_module():
    """The ``sec`` CI job runs every SEC model's test module, and the full grid on Linux
    (USLIB-SEC-PLAN.md K6, M13).

    The ``test`` job leaves out every ``test_*_us_sec.py``, whose grids took each of its
    legs to its timeout (Tests run 14); so a module this job does not list runs in no CI
    job, and every leg is green.  The job runs one module to a leg: a ``module: [...]``
    list of product directories, each with its ``test_<module>_us_sec.py``; a ``grid``
    whose ``full`` legs set ``USLIB_SEC_FULL`` and ``USLIB_REQUIRE_DOCUTILS`` to ``'1'`` for
    the step that runs pytest, so that the full splice grid runs there and a docstring
    parse test that skips fails; and that step's pytest names
    ``lifelib/libraries/uslib/tests/test_${{ matrix.module }}_us_sec.py``.  So the list must
    be exactly the product directories of the registered SEC models, each once, and no
    ``test_*_us_sec.py`` may lie outside it.  The variables are read as that step sees
    them, the job's or its own.  It skips where the workflow or ``tools/`` is absent, as
    from a ``lifelib.create()`` copy or from lifelib, whose CI runs no ``sec`` job.
    """
    if not (WORKFLOW.is_file() and (LIB.parents[2] / "tools").is_dir()):
        pytest.skip("the sec job's workflow and tools/ are this repository's, and one is "
                    "absent")
    job = _job(WORKFLOW.read_text(encoding="utf-8"), "sec")
    assert job is not None, (
        f"{WORKFLOW.name} has no sec job, and the test job leaves out every "
        f"test_*_us_sec.py: they run in no CI job")
    found = sorted(path.name[len("test_"):-len("_us_sec.py")]
                   for path in (LIB / "tests").glob("test_*_us_sec.py"))
    want = list(dict.fromkeys(model_path(name).parent.name for name in SEC_MODELS))
    listed = _matrix_list(job, "module")
    assert listed is not None, "the sec job's matrix has no module: [...] list"
    twice = sorted({module for module in listed if listed.count(module) > 1})
    missing = [module for module in want if module not in listed]
    extra = [module for module in listed if module not in want]
    assert not (twice or missing or extra), (
        f"the sec job's matrix lists the modules {listed}, and the registered SEC models' "
        f"product directories are {want}: add {missing}, remove {extra}, list once "
        f"{twice}; a model's module is added in the commit that registers it")
    absent = [f"test_{module}_us_sec.py" for module in listed
              if not (LIB / "tests" / f"test_{module}_us_sec.py").is_file()]
    assert not absent, f"the sec job lists modules whose files are absent: {absent}"
    stray = [f"test_{module}_us_sec.py" for module in found if module not in listed]
    assert not stray, (
        f"{stray} lie outside the sec job's list {listed}, and the test job leaves them "
        f"out: they run in no CI job")
    assert "full" in (_matrix_list(job, "grid") or []), (
        "the sec job's matrix has no full grid, grid: [core, full]")
    path = re.escape(US_TESTS) + r"/test_\$\{\{\s*matrix\.module\s*\}\}_us_sec\.py"
    runs = [step for step in _steps(job)
            if re.search(rf"\bpytest\b.*\s{path}(\s|$)", step.get("run", ""))]
    assert runs, (f"no step of the sec job runs pytest on "
                  f"{US_TESTS}/test_${{{{ matrix.module }}}}_us_sec.py")
    for variable in ("USLIB_SEC_FULL", "USLIB_REQUIRE_DOCUTILS"):
        given = _variable(job, runs[0], variable)
        assert given is not None and "".join(given.split()) == ON_THE_FULL_GRID, (
            f"the sec job runs its module under {variable} {given!r}, not "
            f"{ON_THE_FULL_GRID!r}: '1' on the full grid")
