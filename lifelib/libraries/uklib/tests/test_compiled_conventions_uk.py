"""The conventions of stage "EC": what every SEC model that compiles must satisfy.

UKLIB-SEC-PLAN.md's C step, USLIB-SEC-PLAN.md's Phase 2 taken one product at a time (U2),
changes how each ``_SEC`` model is represented, and no number it computes (D2), so that it
compiles under modelx-cython into C-typed code, as ``basiclife/BasicTerm_SC`` does.
``test_model_conventions_uk.py`` holds what every model satisfies at either stage.  This
module holds what compiling adds, uslib's ``test_compiled_conventions.py`` read for this
library (U5), parametrized over the SEC models registered at stage ``"EC"``, so that each
product meets it from the commit that moves it there, Term_UK_SEC first (M2):

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
  builtin by its name there and builds no container, under the two directives the build
  tool writes; and every reporting cell a reader asks for, a label among them, returns
  ``object``.
* C4 on the committed points: the compiled model computes what modelx computes, every cell
  at every argument a full modelx sweep caches, with the codes no swept cell reads, which
  the model's spec adds (its ``c4_also``), every raise and every ``Data`` array, bit for
  bit on x86-64.  A test with no compiler holds the comparison to the spec's ``also``,
  and another, reading the sources, holds every C4 comparison of each product's module,
  and of each harness function the module reaches it through, to the model's own.
* The release: ``run_sec.py --block``, run compiled, holds one point's ItemSpace at a time
  (F5, K2).
* The block's sum: ``run_sec.py``'s running sum is ``groupby``'s, bit for bit, on the
  committed points' frames, run in modelx, with or without a compiler.
* The directives: the library's ``build_sec_cy.py`` writes ``infer_types=True`` and
  ``cpow=True`` and no other, which C3, requiring the two, cannot see.  Read statically.
* The build tool: each runner and each ``model-sec.md`` build with the library's own
  ``build_sec_cy.py``, at its root, where lifelib and every ``lifelib.create()`` copy have
  it too, and the tool is uslib's, byte for byte.  Read statically.

The allowlist of cells that stay Python is R17's, :func:`uk_sec_support.reporting_cells`:
``model_point``, the ``result_*`` reports, the ``check_*`` checks, and the label accessors
the registry entry names under ``"reporting"``, and S's cells of float parameters it
names under ``"engine"``, which no compiled cell calls (R14).  A builtin a compiled cell
still calls, R16's ``round`` of a projected amount, is admitted in that cell alone, by the
registry entry's ``"python_calls"``, which C3 and C5 read.  C3, C4 and the release are
marked ``cython``.  They compile each model once a session, into a temporary directory
(``conftest.sec_build``), never into the tree (D12), and run the compiled package in child
processes only.  Without modelx-cython or a C compiler they skip, and the ``cython_uk`` CI
job, which sets ``UKLIB_REQUIRE_CYTHON=1``, fails a skip (D13).  Each product module adds
what is its own: C4 on its splice grid and at its contract's extremes, its compiled
refusals, its deepest cold call on a 1 MiB stack, and its runner compiled.

The ``cython_uk`` CI job runs these with the product module's in the model's own leg, one
shard to a leg (``uk_sec_support.cython_shards``), and
:func:`test_the_cython_job_runs_every_shard`, which needs no compiler, holds the job's
matrix to the registry, so that no model at stage ``"EC"`` is left out of it (U7).  Four
more read the workflow the same way, each for a job that could otherwise go green and
prove nothing: the ``cython_uk`` job fails a skip and collects uklib's suite alone, the
``test`` job runs ``tools/check_sec_harness.py``, and on Python 3.11 every SEC test that
guards a sum's bits, and the ``sec_uk`` job runs every SEC model's module, which the
``test`` job leaves out.
"""
import ast
import builtins
import itertools
import pathlib
import re
import shlex
import sys
import textwrap
import types

import modelx as mx
import pandas as pd
import pytest

from uk_sec_support import (
    C_CALLS, SEC_SPECS, c_faults, compiled_case, compiled_mismatches, cython_shards,
    release_faults, reporting_cells, spec_c4_also, spec_faults, static_faults,
    typing_faults)
from uk_sec_support import label_faults, reporting_columns_faults
from uk_sec_support import engine_faults
from uk_sec_support import REQUIRED_DIRECTIVES
from uk_sec_support import (
    block_sum_faults, labels_refusing_non_text, object_cells, object_return_faults,
    pxd_declarations, runner_add, sample_engine_faults)
from uk_registry import LIB, MODELS, is_sec, meta, model_path, point_keys, projection

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
    """``"reporting"`` is a stage-``"EC"`` key, a tuple of cell names (uk_registry).

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
    """``"reporting_columns"``, a stage-``"EC"`` key, names a shape per label (uslib's M23).

    It says what a label accessor of ``"reporting"`` returns where that is not its point's
    column of its own name (uk_registry), so it widens what C5's label check accepts: it
    is declared only where that check runs, each key a label ``"reporting"`` names, each
    value a column, a dict of argument to column, or a pair of a column and a dict of
    value to label (``uk_sec_support.reporting_columns_faults``).  That each entry is
    taken, and each column it names is the table's, the label check holds on the model.
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
    (``uk_sec_support.label_faults``).
    """
    found = static_faults(model, reporting=reporting_cells(name, model.Projection),
                          python_calls=meta(name).get("python_calls", {}))
    found += label_faults(model, name)
    assert not found, f"{name}: {len(found)} faults, first:\n  " + "\n  ".join(found[:20])


@pytest.mark.parametrize("sec_name", SEC_MODELS)
def test_python_calls_are_declared_by_cell(sec_name):
    """``"python_calls"`` admits a Python builtin in a named cell, and each is taken.

    Or a module's function, by its dotted name, ``"math.erf"``: uslib's ``RILA_US_SEC``
    keeps Python's ``math`` in its pricing (uslib's M25), so a name
    ``"<module>.<function>"`` is valid where ``<module>`` is a Reference of ``Projection``
    holding a module with that function.

    R16 keeps one Python call in a projection formula, ``round`` of a projected amount,
    which cannot be precomputed, and the registry's ``"python_calls"`` admits it by cell
    (uk_registry), so that C3 and C5 pass that call in that cell and fault it in every
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
    registry names it under ``"engine"``, and :func:`uk_sec_support.reporting_cells` admits
    it to C3 and C5 as a reporting cell.  So the key is a stage-``"EC"`` one, as
    ``"reporting"`` is, a non-empty tuple of ``Projection`` cell names, none of them in
    ``"reporting"``, whose check that each returns a column would not hold; each takes a
    parameter that no ``spec_sec.py`` size names, since a cell keyed by sized ints compiles
    to C and needs no admission, or takes none and returns a list, a dict or a DataFrame,
    which no C type holds, as uslib's ``DIA_US_SEC``'s ``qlac_flags`` and premium schedule
    do (uslib's M24); and no ``Projection`` formula calls one but another engine cell, as
    uslib's ``mgsv_rate_is_compliant`` calls ``mgsv_rate_statutory``, so that every cell a
    projection runs is C.  Before stage ``"EC"`` nothing compiles, so a model there
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
    cache by name (uslib's M25).  So the sample's code is read, statically, for a call of
    each (``uk_sec_support.sample_engine_faults``): by attribute, by ``getattr`` with its
    name, or by ``getattr`` over a set of names that holds it; and one taking no parameter,
    by the loop that calls every cell of no parameter, too.  A model without the key
    passes.
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
    (``uk_sec_support.block_sum_faults``, uslib's M23).  Every product's runner sums alike,
    so this is one convention.  A plain running sum departs from ``groupby``'s on every
    product's committed points, so the comparison can fail on each, and that is held too.
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


# The one line the library's build_sec_cy.py puts at the top of each translated space
# module.
DIRECTIVE = "# cython: infer_types=True, cpow=True"


def test_the_build_writes_the_two_directives_and_no_other():
    """The library's ``build_sec_cy.py`` writes :data:`DIRECTIVE`, exactly.

    C3 requires both of ``uk_sec_support.REQUIRED_DIRECTIVES`` in each translated module,
    and reads no other, so a third would compile unseen: ``cdivision=True`` makes ``//``
    and ``%`` on C integers truncate where Python floors, which only C4's full sweep met,
    through point 14's ``duration(t)`` before issue, -2 in modelx and -1 compiled;
    ``boundscheck=False`` lets an ``idx`` past the table read past a vector; and
    ``wraparound=False`` makes ``Projection[-1]`` raise where modelx reads the last point.
    So the tool's line is held to the two, read from its source, which needs no compiler,
    and to the harness's own.  The tool is the library's own, at its root, which every
    copy of the library carries, and uslib's, byte for byte
    (:func:`test_the_build_tool_is_uslib_s_byte_for_byte`).
    """
    tool = LIB / "build_sec_cy.py"
    found = [node.value.value for node in ast.parse(tool.read_text(encoding="utf-8")).body
             if isinstance(node, ast.Assign) and len(node.targets) == 1
             and getattr(node.targets[0], "id", None) == "DIRECTIVE"
             and isinstance(node.value, ast.Constant)]
    assert found == [DIRECTIVE], found
    given = dict(part.strip().split("=") for part in DIRECTIVE.split(":", 1)[1].split(","))
    assert given == REQUIRED_DIRECTIVES, (given, REQUIRED_DIRECTIVES)


def test_the_build_tool_is_uslib_s_byte_for_byte():
    """uklib's ``build_sec_cy.py`` is uslib's, byte for byte.

    The tool sits at the root of each library that holds SEC models, so that each carries
    it wherever it goes alone: lifelib takes a library, and ``lifelib.create()`` copies
    one.  So it is a copy, and a fix to one copy that never reached the other would be
    found by nothing, since each library's suite builds with its own.  The tool holds
    nothing of either library's, finding a product by its folder name in the library it
    sits in, so the two are held to one file.  It skips where uslib's copy is absent, as
    from a ``lifelib.create()`` copy of uklib.
    """
    mine, theirs = LIB / "build_sec_cy.py", LIB.parent / "uslib" / "build_sec_cy.py"
    if not theirs.is_file():
        pytest.skip(f"{theirs} is absent, as from a lifelib.create() copy of uklib")
    assert mine.read_bytes() == theirs.read_bytes(), (
        f"{mine} differs from {theirs}: they are one tool, so change both alike")


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
    registry's ``"python_calls"`` admits in a cell is no fault in that cell's C.  A builtin
    is seen where Cython looks it up by its name, ``__pyx_builtin_round``; a call reached
    through a builtin type, ``float.__pow__``, which Cython reaches through
    ``&PyFloat_Type``, is not seen here, and C5 is what confines such a call to a
    ``raise`` statement, where the overflow guards make it.  And the
    reporting cells a reader asks for, ``model_point``, the ``result_*`` reports and the
    label accessors, return ``object`` where they compile: a label the sample traced on
    text alone compiles to ``str``, and raises on a label ``Data`` holds as a number or a
    blank, where modelx returns it (``uk_sec_support.object_return_faults``, uslib's M22).
    A label compiled to ``str`` passes only where its own formula refuses its point's
    column blank and as a number, ``Data``'s checks aside
    (``uk_sec_support.labels_refusing_non_text``), as a label validating its column does,
    which returns text or raises in either engine.
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

    The build goes beside a copy of the committed inputs (``uk_sec_support.compiled_case``),
    where modelx reads them too.  modelx sweeps every point fully, every cell without
    parameters, the reports among them, and then every monthly cell at every month of the
    frame and the month after, and with them what the model's spec adds, its ``c4_also``
    (``uk_sec_support.spec_c4_also``): every cell of a code at every code it takes, in
    every month, the codes no swept cell reads among them, such as the count at the end of
    the month, and on term assurance and critical illness every cell of a life at both
    lives.  Every value modelx caches is compared with the compiled model's at the same
    arguments, to 1e-12 relative, floored at the cell's magnitude, or identically on
    x86-64, where the compiled model does modelx's arithmetic in modelx's order
    (``uk_sec_support.exact_here``); a bool or an int must keep its kind, a raise must
    meet the same raise, and every ``Data`` array must be identical
    (``uk_sec_support.compiled_mismatches``).  The branches the committed points miss are
    each product's splice grid's.
    """
    build = sec_build(name)
    folder = compiled_case(build, tmp_path / "committed")
    found = compiled_mismatches(build, folder, also=spec_c4_also(name))
    assert not found, f"{name}: {len(found)} mismatches, first:\n  " + "\n  ".join(found)


def test_c4_on_the_committed_points_passes_the_spec_s_also(name, monkeypatch, tmp_path):
    """C4 on the committed points hands the comparison its model's ``also``, the spec's
    ``c4_also``, and every uklib spec gives one.

    Nothing in a comparison shows what it leaves out: without its ``also``, C4 compares
    fewer calls, and passes.  So C4 on the committed points,
    :func:`test_the_compiled_model_computes_what_modelx_computes`, is run here with the
    build, the case and the comparison standing in, which compile and compare nothing,
    and what it hands the comparison is held: the model's spec's ``c4_also``, set on every
    model at stage ``"EC"``, so that the codes no swept cell reads are compared on the
    committed points as each product module compares them on its own rows.  Needs no
    compiler.
    """
    handed = []

    def comparison(build, folder, **kwargs):
        handed.append((build.name, kwargs))
        return []

    module = sys.modules[__name__]
    monkeypatch.setattr(module, "compiled_case", lambda build, dest, **kwargs: dest)
    monkeypatch.setattr(module, "compiled_mismatches", comparison)
    test_the_compiled_model_computes_what_modelx_computes(
        name, lambda model: types.SimpleNamespace(name=model), tmp_path)
    assert SEC_SPECS[name].c4_also is not None, f"{name}'s spec gives C4 no also"
    assert handed == [(name, {"also": SEC_SPECS[name].c4_also})], handed


# C4's comparison, and the harness whose functions a module may reach it through, each held
# as the module's own helpers are.
C4 = "compiled_mismatches"
HARNESS = LIB / "tests" / "uk_sec_support.py"


def _calls_of(tree, name):
    """``(call, functions)`` for every call of the function ``name`` in ``tree``, with the
    functions it sits in, outermost first."""
    found = []

    def visit(node, functions):
        for child in ast.iter_child_nodes(node):
            if (isinstance(child, ast.Call) and isinstance(child.func, ast.Name)
                    and child.func.id == name):
                found.append((child, functions))
            visit(child, [*functions, child] if isinstance(child, ast.FunctionDef)
                  else functions)

    visit(tree, [])
    return found


def _parameters(function):
    """The names of ``function``'s parameters, in order, the keyword-only ones last."""
    args = function.args
    return [a.arg for a in (*args.posonlyargs, *args.args, *args.kwonlyargs)]


def _argument(call, function, parameter):
    """What ``call`` passes ``function``'s ``parameter``, by keyword or by place, or its
    default where the call leaves it out: an expression, or ``None`` where there is none.
    A call that unpacks ``*`` or ``**`` is refused before this reads it (:func:`_unpacked`).
    """
    given = {keyword.arg: keyword.value for keyword in call.keywords}
    if parameter in given:
        return given[parameter]
    args = function.args
    placed = [a.arg for a in (*args.posonlyargs, *args.args)]
    if parameter in placed and placed.index(parameter) < len(call.args):
        return call.args[placed.index(parameter)]
    defaults = dict(zip(placed[len(placed) - len(args.defaults):], args.defaults))
    defaults.update((a.arg, d) for a, d in zip(args.kwonlyargs, args.kw_defaults))
    return defaults.get(parameter)


def _calls_any(node, names):
    """Whether ``node`` holds, at any depth, a call of a function named in ``names``."""
    return any(isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
               and n.func.id in names for n in ast.walk(node))


def _reads_any(node, names):
    """Whether ``node`` reads, at any depth, a name of ``names``."""
    return any(isinstance(n, ast.Name) and n.id in names for n in ast.walk(node))


def _reaching(trees, target, reads=()):
    """The names of the functions of ``trees`` that reach the function ``target``: each that
    calls it, or a function that does, at any depth, by name; ``target`` among them.  A
    function that reads a name of ``reads``, as ``target`` itself may, reaches it too."""
    functions = [node for tree in trees for node in ast.walk(tree)
                 if isinstance(node, ast.FunctionDef)]
    names, grown = {target}, True
    names |= {function.name for function in functions if _reads_any(function, reads)}
    while grown:
        grown = False
        for function in functions:
            if function.name not in names and _calls_any(function, names):
                names.add(function.name)
                grown = True
    return names


def _returns_in(node):
    """Whether ``node`` returns, at any depth outside a function or lambda it defines."""
    if isinstance(node, ast.Return):
        return True
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
        return False
    return any(_returns_in(child) for child in ast.iter_child_nodes(node))


def _stands_in(function, own):
    """Whether ``function``, passed as ``also``, asks the model's own of every point it is
    given: a statement of its own body, in no ``if``, loop or ``try``, calls ``own`` on the
    function's first parameter alone, and no statement before it returns."""
    first = _parameters(function)[:1]
    for statement in function.body:
        call = statement.value if isinstance(statement, ast.Expr) else None
        if (isinstance(call, ast.Call) and isinstance(call.func, ast.Name)
                and call.func.id == own and not call.keywords and first
                and [ast.unparse(a) for a in call.args] == first):
            return True
        if _returns_in(statement):
            return False
    return False


def _reaches(trees, own, value, place, none=False, seen=frozenset()):
    """Whether ``value``, an expression at ``place``, ``(tree, the functions it sits in)``,
    is always the model's own ``also``, the function named ``own``, or a function that
    stands in for it (:func:`_stands_in`); with ``none``, ``None`` passes too, as the
    first operand of ``also or own`` may.

    ``trees`` are the module's and the harness's.  ``own`` is ``None`` for the
    conventions, where the model's own is the spec's, which ``spec_c4_also`` of the test's
    model returns.  A parameter of a helper reaches it where every call of the helper, in
    the module, and in the harness for a helper there, passes, or leaves as its default,
    what does; a parameter shadows a function of its name, ``own`` among them.
    """
    tree, functions = place
    if value is None or isinstance(value, ast.Constant) and value.value is None:
        return none
    if isinstance(value, ast.BoolOp) and isinstance(value.op, ast.Or):
        *first, last = value.values
        return (all(_reaches(trees, own, v, place, True, seen) for v in first)
                and _reaches(trees, own, last, place, none, seen))
    if (isinstance(value, ast.Call) and isinstance(value.func, ast.Name)
            and value.func.id == "spec_c4_also"):
        return (own is None and len(value.args) == 1 and isinstance(value.args[0], ast.Name)
                and any(value.args[0].id in _parameters(f) for f in functions))
    if not isinstance(value, ast.Name):
        return False
    for function in reversed(functions):
        if value.id in _parameters(function):
            key = (id(function), value.id)
            callers = trees if tree is not trees[0] else trees[:1]
            return key not in seen and all(
                _reaches(trees, own, _argument(call, function, value.id), (t, outer),
                         none, seen | {key})
                for t in callers for call, outer in _calls_of(t, function.name))
        local = [node for node in ast.walk(function) if isinstance(node, ast.FunctionDef)
                 and node.name == value.id and node is not function]
        if local:
            return _stands_in(local[0], own)
    if value.id == own:
        return True
    top = [node for node in tree.body
           if isinstance(node, ast.FunctionDef) and node.name == value.id]
    return bool(top) and _stands_in(top[0], own)


def _bindings(tree, name):
    """The lines where ``tree`` binds ``name`` but by importing it, as it is, from
    ``uk_sec_support``: as a function or class, a parameter, a target, a deletion, another
    import or alias, an exception's name, or in a ``global`` or ``nonlocal``."""
    lines = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            bound = node.name == name
        elif isinstance(node, ast.arg):
            bound = node.arg == name
        elif isinstance(node, ast.Name):
            bound = node.id == name and not isinstance(node.ctx, ast.Load)
        elif isinstance(node, ast.ExceptHandler):
            bound = node.name == name
        elif isinstance(node, (ast.Global, ast.Nonlocal)):
            bound = name in node.names
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            bound = any((a.asname or a.name.split(".")[0]) == name
                        and not (isinstance(node, ast.ImportFrom)
                                 and node.module == "uk_sec_support"
                                 and a.name == name and a.asname is None)
                        for a in node.names)
        else:
            bound = False
        if bound:
            lines.append(node.lineno)
    return lines


def _unpacked(tree, label, names):
    """A line for each call in ``tree`` of a function named in ``names`` that unpacks ``*``
    or ``**``, whose ``also`` no reading can see."""
    return [f"{label}:{node.lineno}: {node.func.id} is called with * or ** unpacking"
            for node in ast.walk(tree)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
            and node.func.id in names
            and (any(isinstance(a, ast.Starred) for a in node.args)
                 or any(k.arg is None for k in node.keywords))]


def _uncalled(tree, label, names):
    """A line for each use in ``tree`` of a function named in ``names`` but a call of it by
    its name, a reference passed on or reached through an attribute among them."""
    called = {id(node.func) for node in ast.walk(tree) if isinstance(node, ast.Call)}
    return [f"{label}:{node.lineno}: {getattr(node, 'id', None) or node.attr} is used, "
            f"not called by its name"
            for node in ast.walk(tree)
            if isinstance(node, ast.Name) and node.id in names
            and isinstance(node.ctx, ast.Load) and id(node) not in called
            or isinstance(node, ast.Attribute) and node.attr in names]


def _also_faults(path, own, harness):
    """A line for each way a C4 comparison of the module at ``path`` may pass
    ``compiled_mismatches`` an ``also`` other than the model's own; none where it can pass
    no other.

    ``own`` and ``compiled_mismatches`` must be imported from ``uk_sec_support`` as they are
    and bound nowhere else in the module (:func:`_bindings`).  No call of a function that
    reaches C4, in the module or in the harness, ``harness``'s tree, may unpack ``*`` or
    ``**``, and the module may use each only by calling it by its name.  Then every call of
    ``compiled_mismatches`` in the module, and in each function of the harness the module
    reaches it through, must pass ``also`` what is always the model's own
    (:func:`_reaches`).
    """
    module = ast.parse(path.read_text(encoding="utf-8"))
    trees = (module, harness)
    found = []
    for name in (own, C4) if own is not None else (C4,):
        imported = any(isinstance(node, ast.ImportFrom) and node.module == "uk_sec_support"
                       and any(a.name == name and a.asname is None for a in node.names)
                       for node in module.body)
        bound = _bindings(module, name)
        if not imported or bound:
            found.append(f"{path.name}: {name} is not uk_sec_support's alone: imported "
                         f"{imported}, bound at lines {bound}")
    reaching = _reaching(trees, C4)
    found += _unpacked(module, path.name, reaching)
    found += _unpacked(harness, HARNESS.name, reaching)
    found += _uncalled(module, path.name, reaching)
    used = {node.func.id for node in ast.walk(module) if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)}
    helpers = [node for node in harness.body if isinstance(node, ast.FunctionDef)
               and node.name in used & reaching - {C4}]
    sites = [(module, f"{path.name}:{call.lineno}", call, functions)
             for call, functions in _calls_of(module, C4)]
    seen = set()
    while helpers:
        helper = helpers.pop()
        if helper.name in seen:
            continue
        seen.add(helper.name)
        sites += [(harness, f"{HARNESS.name}:{call.lineno}, reached from {path.name}",
                   call, [helper, *functions])
                  for call, functions in _calls_of(helper, C4)]
        helpers += [node for node in harness.body if isinstance(node, ast.FunctionDef)
                    and node.name in reaching - {C4} and _calls_any(helper, {node.name})]
    if not sites:
        found.append(f"{path.name}: no call of {C4}")
    for tree, where, call, functions in sites:
        given = {keyword.arg: keyword.value for keyword in call.keywords}
        if "also" not in given:
            found.append(f"{where}: {C4} is passed no also")
        elif not _reaches(trees, own, given["also"], (tree, functions)):
            found.append(f"{where}: also={ast.unparse(given['also'])} is not always "
                         f"{own or 'spec_c4_also of the model'}")
    return found


def test_every_c4_comparison_passes_the_model_s_own_also():
    """Every C4 comparison of a uklib SEC model hands ``compiled_mismatches`` the model's
    own ``also``, its spec's ``c4_also``, read from the sources.

    Nothing in a comparison shows what it leaves out: a call that drops ``also=``, or
    passes ``None``, compares fewer calls, and passes.  So every call of
    ``compiled_mismatches`` in each SEC model's module, ``test_<product>_uk_sec.py``, and in
    each function of ``uk_sec_support.py`` the module reaches it through, must pass
    ``also`` what is always the model's own, the function its spec names, which the module
    imports from ``uk_sec_support`` and binds nowhere else, as no parameter or local name
    either (:func:`_also_faults`): that name; a function that stands in for it, one the
    module or the call's helper defines, whose own body asks it of the point it is given
    as a statement in no ``if``, loop or ``try``, as income protection's ``_c4`` does;
    ``also or`` it, where every call of the helper leaves ``also`` its default ``None``, as
    the pension annuity's ``_c4_chunks`` has it; or a parameter of a helper, the module's
    or the harness's, every call of which passes one of these (:func:`_reaches`).  No call
    of a function that reaches C4 may unpack ``*`` or ``**``, which would hide what it
    passes, and the module may use one only by calling it by its name.  And C4 on the
    committed points here must pass ``spec_c4_also`` of the model under test, which
    :func:`test_c4_on_the_committed_points_passes_the_spec_s_also` holds to the spec's.
    Read statically, so it needs no compiler.
    """
    harness = ast.parse(HARNESS.read_text(encoding="utf-8"))
    found = []
    for name in SEC_MODELS:
        spec = SEC_SPECS.get(name)
        assert spec is not None and spec.c4_also is not None, f"{name} gives C4 no also"
        module = LIB / "tests" / f"test_{model_path(name).parent.name}_uk_sec.py"
        found += _also_faults(module, spec.c4_also.__name__, harness)
    found += _also_faults(pathlib.Path(__file__), None, harness)
    assert not found, "\n".join(found)


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
    uslib's Term, so a block that kept them would hold the block's worth.  And deleting one
    frees nothing on its own: it refers to itself, as its own ``_space`` and in its own
    ``_mx_roots``, cycles only the cyclic collector frees.  The product's runner, run on
    a block of :data:`RELEASE_POINTS` copied points with ``--build`` on the session's
    build, in an interpreter of its own, must therefore leave no ItemSpace but the base
    alive after each collection it makes once it has frozen what lived before the block,
    make one for every point, and leave none alive at the end, frozen or not
    (``uk_sec_support.release_faults``).  A control then deletes an ItemSpace and finds it
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


# The workflow that runs the cython_uk job, in the repository that holds this library.
WORKFLOW = LIB.parents[2] / ".github" / "workflows" / "tests.yml"

# The job this library's compile tests run in: uslib's are the "cython" job's, and a job's
# legs take one library's variables, so uklib has a copy of its own (UKLIB-SEC-PLAN.md U7).
JOB = "cython_uk"


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


def test_the_cython_job_runs_every_shard():
    """The ``cython_uk`` CI job's matrix lists exactly the shards the registry makes (D13).

    The job runs one shard of the compile tests to a leg, named by ``UKLIB_CYTHON_SHARD``,
    so that no leg compiles every model: ``toolchain``, and for each SEC model at stage
    ``"EC"`` its product directory (``uk_sec_support.cython_shards``), whose module,
    ``test_<shard>_uk_sec.py``, holds the model's own compile tests.  A model moved to
    stage ``"EC"`` without its shard in the matrix would have its compile tests run in no
    leg, and every leg green, so its C step adds the shard, and this fails until it does;
    a shard left in the matrix after its model leaves stage ``"EC"`` would fail its leg
    with nothing selected, and this says so first.  Every leg must pass the shard to
    pytest.  It runs in the ``test`` job, which needs no compiler, and skips where the
    workflow or ``tools/build_sec_cy.py`` is absent, as from a ``lifelib.create()`` copy
    or from lifelib, whose CI runs no ``cython_uk`` job.  It skips too where the workflow
    has no ``cython_uk`` job while the registry holds no model at stage ``"EC"``, whose
    one shard, the toolchain's, compiles an S model; from the first model at stage
    ``"EC"`` on, whose compile tests would otherwise run in no leg, a missing job fails.
    The job is read by its name, so uslib's ``cython`` job, which lists uslib's shards,
    is not this one, and is held to uslib's registry by uslib's copy of this test.
    """
    tool = LIB.parents[2] / "tools" / "build_sec_cy.py"
    if not (WORKFLOW.is_file() and tool.is_file()):
        pytest.skip(f"the {JOB} job's workflow and tools/build_sec_cy.py are this "
                    f"repository's, and one is absent")
    want = list(cython_shards())
    job = _job(WORKFLOW.read_text(encoding="utf-8"), JOB)
    if job is None and not EC_MODELS:
        pytest.skip(f"{WORKFLOW.name} has no {JOB} job, and no uklib model is at stage "
                    f"'EC' yet")
    assert job is not None, (
        f"{WORKFLOW.name} has no {JOB} job, and the registry makes the shards {want}")
    listed = _matrix_list(job, "shard")
    assert listed is not None, f"the {JOB} job's matrix has no shard: [...] list"
    twice = sorted({shard for shard in listed if listed.count(shard) > 1})
    missing = [shard for shard in want if shard not in listed]
    extra = [shard for shard in listed if shard not in want]
    assert not (twice or missing or extra), (
        f"the {JOB} job's matrix lists the shards {listed}, and the registry makes "
        f"{want}: add {missing}, remove {extra}, list once {twice}; a model's shard is "
        f"added in the commit that moves it to stage 'EC'")
    for shard in want[1:]:
        module = LIB / "tests" / f"test_{shard}_uk_sec.py"
        assert module.is_file(), f"shard {shard}: its module {module.name} is absent"
    passed = r"\s+UKLIB_CYTHON_SHARD:\s*\$\{\{\s*matrix\.shard\s*\}\}\s*"
    assert any(re.fullmatch(passed, line) for line in job), (
        f"the {JOB} job does not set UKLIB_CYTHON_SHARD to its matrix's shard")


# uklib's suite: the one tree the cython_uk job collects, and the home of every module the
# sec_uk job runs.
UK_TESTS = "lifelib/libraries/uklib/tests"

# The job uklib's SEC test modules run in, one to a leg, as uslib's run in the "sec" job
# (UKLIB-SEC-PLAN.md U7).  The test job leaves out every test_*_uk_sec.py.
SEC_JOB = "sec_uk"

# What sets a variable to '1' on a sec_uk leg of the full grid alone, as the sec job sets
# uslib's, with its whitespace taken out.
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


def _workflow_env(text):
    """The workflow's own ``env:``, which every job and every step sees, as written: the
    lines of the block at the file's top level, or the mapping written on its line."""
    seen, inside = [], False
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        top = re.fullmatch(r"env:\s*(.*?)\s*", line)
        if top:
            inside = True
            seen += [top.group(1)] if top.group(1) else []
        elif inside and line[0] in " \t":
            seen.append(line.strip())
        else:
            inside = False
    return " ".join(seen)


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


def test_the_cython_job_fails_a_skip_and_collects_uklib_alone():
    """The ``cython_uk`` job runs pytest under ``UKLIB_REQUIRE_CYTHON: '1'``, with ``-m
    cython``, over ``lifelib/libraries/uklib/tests`` and no other library's tests (U7).

    Each is a way its legs could be green and prove nothing.  Without the variable a
    compile test that finds no compiler skips, and ``conftest.py`` fails such a skip only
    under it.  Without ``-m cython`` a leg runs the whole suite beside its shard, the hour
    spent on what the ``test`` job runs already.  Over another library's tests it runs that
    library's compile tests under uklib's variables, which govern none of them, and none of
    uklib's.  The variable is read as the step that runs pytest sees it, the job's or its
    own.  It skips as :func:`test_the_cython_job_runs_every_shard` does.
    """
    tool = LIB.parents[2] / "tools" / "build_sec_cy.py"
    if not (WORKFLOW.is_file() and tool.is_file()):
        pytest.skip(f"the {JOB} job's workflow and tools/build_sec_cy.py are this "
                    f"repository's, and one is absent")
    job = _job(WORKFLOW.read_text(encoding="utf-8"), JOB)
    if job is None and not EC_MODELS:
        pytest.skip(f"{WORKFLOW.name} has no {JOB} job, and no uklib model is at stage "
                    f"'EC' yet")
    assert job is not None, f"{WORKFLOW.name} has no {JOB} job"
    runs = [step for step in _steps(job) if _pytest_args(step.get("run", "")) is not None]
    assert len(runs) == 1, f"the {JOB} job has {len(runs)} steps that run pytest, not one"
    step = runs[0]
    required = _variable(job, step, "UKLIB_REQUIRE_CYTHON")
    assert required is not None and required.strip("'\"") == "1", (
        f"the {JOB} job runs pytest under UKLIB_REQUIRE_CYTHON {required!r}, not '1': a "
        f"compile test that skips there would pass")
    marks, paths = _pytest_args(step["run"])
    assert marks == ["cython"], (
        f"the {JOB} job runs pytest with -m {marks}, not -m cython: {step['run']}")
    other = [path for path in paths
             if path.rstrip("/") != UK_TESTS and not path.startswith(UK_TESTS + "/")]
    assert paths and not other, (
        f"the {JOB} job's pytest collects {paths or 'the repository'}, not {UK_TESTS} "
        f"alone: {step['run']}")


def test_the_test_job_runs_the_harness_check():
    """CI's ``test`` job has a step that runs ``python tools/check_sec_harness.py``, on no
    condition (UKLIB-SEC-PLAN.md U3).

    The check holds uklib's SEC harness to uslib's, and each one's product specs to their
    rules.  Each library's suite passes on its own copy, so without the step two drifted
    copies are green, and so they are with a step that runs it only under ``if:``, unless
    the condition is ``always()``, or that may fail under ``continue-on-error``.  It skips
    where the workflow or the tool is absent, as from a ``lifelib.create()`` copy.
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


# The guard of a sum's bits in each SEC module that holds a total to sum()'s last bit: it
# skips the rest of its test where sum() adds floats left to right, on Python 3.11, and
# the test job runs every test that reaches it on the one leg the condition names.
SUMS_GUARD = "_hold_the_sums_bits"
# What the guard reads to decide, and what its skip says: a test that reads either decides
# the skip as the guard does, and reaches it as surely as a call would.
SUMS_FLAGS = ("SUM_COMPENSATES", "SUM_311")
ON_3_11 =("matrix.python-version=='3.11'&&matrix.os=='ubuntu-latest'",
           "matrix.os=='ubuntu-latest'&&matrix.python-version=='3.11'")

# Each module's test of its guard, which reaches the guard to hold it.
GUARD_TEST = "test_the_sums_bits_skip_only_where_sum_adds_left_to_right"

# How many assertions each test the 3.11 step runs makes before it first reaches the
# guard, by product: what rests on no sum, which on Python 3.11 it holds before it skips,
# saying "the rest was held".  Pinned, so that the guard moved before one of them, or one
# moved past the guard, fails on every Python, as a test given the guard later fails
# until it is pinned here.
HELD_BEFORE_THE_GUARD = {
    "term_assurance": {GUARD_TEST: 1, "test_the_ledger_residual_is_s_own_bit_for_bit": 2},
    "critical_illness": {GUARD_TEST: 1, "test_the_all_total_is_s_total_bit_for_bit": 6},
    "income_protection": {GUARD_TEST: 1, "test_the_all_total_is_s_total_bit_for_bit": 2,
                          "test_the_cohort_sums_are_s_sums_bit_for_bit": 1},
    "with_profits": {GUARD_TEST: 1, "test_the_all_total_is_s_total_bit_for_bit": 5},
}


def _guarded_tests():
    """``{node id: (test, reaches)}`` for every test of a ``test_*_uk_sec.py`` that reaches
    the guard of the sums' bits, :data:`SUMS_GUARD`, directly or through a function of its
    module that does, at any depth (:func:`_reaching`), read from the sources, in file
    order; ``reaches`` are the test's calls of the guard and of those functions, and its
    reads of :data:`SUMS_FLAGS`.  So a test that skips by itself, ``if not
    SUM_COMPENSATES: pytest.skip(SUM_311)``, is a guarded test too."""
    found = {}
    for path in sorted((LIB / "tests").glob("test_*_uk_sec.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        reaching = _reaching((tree,), SUMS_GUARD, SUMS_FLAGS)
        for node in tree.body:
            if not (isinstance(node, ast.FunctionDef) and node.name.startswith("test_")):
                continue
            reaches = [n for n in ast.walk(node)
                       if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                       and n.func.id in reaching
                       or isinstance(n, ast.Name) and n.id in SUMS_FLAGS]
            if reaches:
                found[f"{UK_TESTS}/{path.name}::{node.name}"] = (node, reaches)
    return found


def _held_before(test, reaches):
    """How many assertions ``test`` makes before it first reaches the guard, ``reaches``
    being its calls and reads that do: its ``assert`` statements, at any depth, that come
    first."""
    first = min((call.lineno, call.col_offset) for call in reaches)
    return sum(isinstance(node, ast.Assert) and (node.lineno, node.col_offset) < first
               for node in ast.walk(test))


def _marks(test):
    """The names of the marks ``test`` carries, ``pytest.mark.<name>`` as it is decorated,
    with or without a call."""
    marks = []
    for decorator in test.decorator_list:
        node = decorator.func if isinstance(decorator, ast.Call) else decorator
        if (isinstance(node, ast.Attribute) and isinstance(node.value, ast.Attribute)
                and node.value.attr == "mark"):
            marks.append(node.attr)
    return marks


def test_the_test_job_runs_the_sums_bits_where_sum_adds_left_to_right():
    """CI's ``test`` job has a step that runs, on Python 3.11 on Linux, exactly the tests
    that reach the guard of the sums' bits, by node id, and nothing else
    (UKLIB-SEC-PLAN.md, M15).

    A test that holds a total to ``sum``'s last bit reaches :data:`SUMS_GUARD`, directly
    or through a function of its module, and the guard skips the rest of it where ``sum()``
    adds left to right, as on Python 3.11, and goes on where it compensates; each module's
    test of the guard reaches it too, and so does a test that reads what the guard reads,
    or its skip's message (:data:`SUMS_FLAGS`), as one that skips by itself would.  The modules run in the ``sec_uk`` job alone, on
    3.13, so without this step nothing CI runs takes the skip: an assertion resting on
    ``sum`` moved before the guard would pass in every job.  So the step's condition must
    be ``matrix.python-version == '3.11' && matrix.os == 'ubuntu-latest'``; it must run
    ``pytest`` with ``-q``, ``-rs`` and node ids alone, any other option failing, ``-k``
    and ``--deselect`` among them, and under no ``PYTEST_ADDOPTS`` or ``PYTEST_PLUGINS``,
    the workflow's, the job's or its own, since either could leave a test out; and its node ids must be exactly the tests that
    reach the guard, read from the sources (:func:`_guarded_tests`), each once, so that a
    test given a guard later fails here until its node id is added.  None may carry a
    ``cython`` or ``docutils`` mark, which the job installs nothing for.  And each must
    make before it first reaches the guard as many assertions as
    :data:`HELD_BEFORE_THE_GUARD` pins for it (:func:`_held_before`), so that on 3.11 it
    holds what rests on no ``sum``, as its skip says, and does not skip having held less.
    It skips where the workflow is absent, as from a ``lifelib.create()`` copy.
    """
    if not WORKFLOW.is_file():
        pytest.skip("the test job's workflow is this repository's, and it is absent")
    want = _guarded_tests()
    assert want, f"no test of a test_*_uk_sec.py reaches {SUMS_GUARD}"
    text = WORKFLOW.read_text(encoding="utf-8")
    job = _job(text, "test")
    assert job is not None, f"{WORKFLOW.name} has no test job"
    runs = [step for step in _steps(job)
            if "".join(re.sub(r"\$\{\{(.*?)\}\}", r"\1", step.get("if", "")).split())
            in ON_3_11 and _pytest_args(step.get("run", "")) is not None]
    assert len(runs) == 1, (
        f"the test job has {len(runs)} steps that run pytest on Python 3.11 on Linux "
        f"alone, not one")
    step = runs[0]
    assert step.get("continue-on-error", "false") == "false", step
    everywhere = _workflow_env(text)
    for variable in ("PYTEST_ADDOPTS", "PYTEST_PLUGINS"):
        given = _variable(job, step, variable)
        assert given is None, f"the 3.11 step runs under {variable} {given!r}"
        assert not re.search(rf"(?<!\w){variable}\s*:", everywhere), (
            f"the workflow runs every step under {variable}: env: {everywhere}")
    words = shlex.split(step["run"])
    options = [word for word in words[1:] if word.startswith("-")]
    ids = [word for word in words[1:] if not word.startswith("-")]
    assert words[:1] == ["pytest"] and sorted(options) == ["-q", "-rs"], (
        f"the 3.11 step runs {words[:1]} with the options {options}, not pytest with -q, "
        f"-rs and node ids alone: {step['run']}")
    twice = sorted({node for node in ids if ids.count(node) > 1})
    missing = [node for node in want if node not in ids]
    extra = [node for node in ids if node not in want]
    assert not (twice or missing or extra), (
        f"the 3.11 step runs {ids}, and the tests that reach {SUMS_GUARD} are "
        f"{list(want)}: add {missing}, remove {extra}, list once {twice}")
    marked = {node: _marks(test) for node, (test, _) in want.items()
              if {"cython", "docutils"} & set(_marks(test))}
    assert not marked, f"the 3.11 step runs tests the test job cannot: {marked}"
    pinned = {f"{UK_TESTS}/test_{product}_uk_sec.py::{name}": count
              for product, tests in HELD_BEFORE_THE_GUARD.items()
              for name, count in tests.items()}
    held = {node: _held_before(test, reaches) for node, (test, reaches) in want.items()}
    apart = {node: (held.get(node), pinned.get(node)) for node in {*held, *pinned}
             if held.get(node) != pinned.get(node)}
    assert not apart, (
        f"the assertions each test makes before it reaches {SUMS_GUARD}, and those "
        f"HELD_BEFORE_THE_GUARD pins, part: {apart}")


def test_the_sec_uk_job_runs_every_sec_module():
    """The ``sec_uk`` CI job runs every uklib SEC model's test module, and the full grid
    on Linux, as the ``sec`` job runs uslib's (UKLIB-SEC-PLAN.md U7).

    The ``test`` job leaves out every ``test_*_uk_sec.py``, as it leaves out uslib's
    ``_us_sec`` modules, whose grids took its legs to their timeout; so a module this job
    does not list runs in no CI job, and every leg is green.  The job is uslib's ``sec``
    job read for uklib: a ``module: [...]`` list of product directories, one to a leg, each
    with its ``test_<module>_uk_sec.py``; a ``grid`` whose ``full`` legs set
    ``UKLIB_SEC_FULL`` and ``UKLIB_REQUIRE_DOCUTILS`` to ``'1'`` for the step that runs
    pytest, so that the full splice grid runs there and a docstring parse test that skips
    fails; and that step's pytest names
    ``lifelib/libraries/uklib/tests/test_${{ matrix.module }}_uk_sec.py``.  So the list must
    be exactly the product directories of the registered SEC models, each once, and no
    ``test_*_uk_sec.py`` may lie outside it.  It skips where the workflow or ``tools/`` is
    absent, as from a ``lifelib.create()`` copy or from lifelib, and while the job would
    have nothing to run: no uklib SEC model registered, no ``test_*_uk_sec.py``, and no
    ``sec_uk`` job.  From the first of them on, a missing job fails.
    """
    if not (WORKFLOW.is_file() and (LIB.parents[2] / "tools").is_dir()):
        pytest.skip(f"the {SEC_JOB} job's workflow and tools/ are this repository's, and "
                    f"one is absent")
    job = _job(WORKFLOW.read_text(encoding="utf-8"), SEC_JOB)
    found = sorted(path.name[len("test_"):-len("_uk_sec.py")]
                   for path in (LIB / "tests").glob("test_*_uk_sec.py"))
    want = list(dict.fromkeys(model_path(name).parent.name for name in SEC_MODELS))
    if job is None and not SEC_MODELS and not found:
        pytest.skip(f"no uklib SEC model is registered, no test_*_uk_sec.py exists, and "
                    f"{WORKFLOW.name} has no {SEC_JOB} job")
    assert job is not None, (
        f"{WORKFLOW.name} has no {SEC_JOB} job, and the test job leaves out every "
        f"test_*_uk_sec.py: the modules of {want or found} run in no CI job")
    listed = _matrix_list(job, "module")
    assert listed is not None, f"the {SEC_JOB} job's matrix has no module: [...] list"
    twice = sorted({module for module in listed if listed.count(module) > 1})
    missing = [module for module in want if module not in listed]
    extra = [module for module in listed if module not in want]
    assert not (twice or missing or extra), (
        f"the {SEC_JOB} job's matrix lists the modules {listed}, and the registered SEC "
        f"models' product directories are {want}: add {missing}, remove {extra}, list "
        f"once {twice}; a product's E step adds its module")
    absent = [f"test_{module}_uk_sec.py" for module in listed
              if not (LIB / "tests" / f"test_{module}_uk_sec.py").is_file()]
    assert not absent, f"the {SEC_JOB} job lists modules whose files are absent: {absent}"
    stray = [f"test_{module}_uk_sec.py" for module in found if module not in listed]
    assert not stray, (
        f"{stray} lie outside the {SEC_JOB} job's list {listed}, and the test job leaves "
        f"them out: they run in no CI job")
    assert "full" in (_matrix_list(job, "grid") or []), (
        f"the {SEC_JOB} job's matrix has no full grid, grid: [core, full]")
    path = re.escape(UK_TESTS) + r"/test_\$\{\{\s*matrix\.module\s*\}\}_uk_sec\.py"
    runs = [step for step in _steps(job)
            if re.search(rf"\bpytest\b.*\s{path}(\s|$)", step.get("run", ""))]
    assert runs, (f"no step of the {SEC_JOB} job runs pytest on "
                  f"{UK_TESTS}/test_${{{{ matrix.module }}}}_uk_sec.py")
    for variable in ("UKLIB_SEC_FULL", "UKLIB_REQUIRE_DOCUTILS"):
        given = _variable(job, runs[0], variable)
        assert given is not None and "".join(given.split()) == ON_THE_FULL_GRID, (
            f"the {SEC_JOB} job runs its module under {variable} {given!r}, not "
            f"{ON_THE_FULL_GRID!r}: '1' on the full grid")
