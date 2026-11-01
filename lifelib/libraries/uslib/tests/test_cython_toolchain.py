"""The compile toolchain end to end: export, trace, translate, compile, run, compare.

USLIB-SEC-PLAN.md compiles each SEC model in its Phase 2 and runs the compile tests in a
``cython`` CI job of their own, on Linux and Windows (D13).  This module is what that job
runs in the meantime, so that it proves something real before any model is written for the
compiler: that ``tools/build_sec_cy.py``, modelx-cython and the platform's C compiler
together turn a uslib model into a compiled package, and that the package computes what
modelx computes.  A job with nothing to run would stay green on a Windows runner where no
MSVC build had ever succeeded, and Phase 2 would find that out on its first model.

**What it compiles.**  ``Term_US_S``.  No SEC model exists yet, and mx2cy compiles any
export, an S model's included (F2); typing a model well is Phase 2's representation work,
while compiling one at all is what is proved here.  mx2cy's two inputs are written by the
test rather than added to the product directory.  The sample runs ``result_cf()`` on every
point of the shipped table, both of them.  The spec sizes the ``t`` caches for the longest
frame any issue age can have, because a compiled cache raises ``IndexError`` past its end
(F4), and the test reads the generated declarations to see that it did.  The numbers
cannot show it: mx2cy ignores a spec key or space name it does not know and sizes each
cache from the sample instead, and the sample's own points then fit.  With the key
misspelled, every ``t`` cache came out ``[720]``, and the compiled model still matched
modelx exactly.  The build goes into ``tmp_path``, and the compiled package runs in a
child process, which raises the recursion limit, as modelx does and the export does not
(F7); a compiled model that overflows the C stack then takes down the child, not the test
session.  Its ``result_cf()`` must equal modelx's on both points to 1e-12 relative, the
tolerance of Phase 2's C4.  With gcc on Linux it is exact; the tolerance is for a compiler
that fuses a multiply and an add into a single rounding.

**When it skips.**  Without modelx-cython, which ``requirements.txt`` leaves out because it
needs a C compiler; without a C compiler, on a POSIX system; and without
``tools/build_sec_cy.py``, which a ``lifelib.create()`` copy lacks, since it copies the
library and not this repository's ``tools/``.  So the ``test`` CI job and lifelib's own bare
``pytest`` skip it and stay green (D13).  The compiler is probed on POSIX only.  There
setuptools runs ``CC``, or the compiler the interpreter was built with, from ``PATH``; on
Windows it finds MSVC through vswhere at build time, and ``cl.exe`` is on no ``PATH``
outside a developer prompt, so a ``PATH`` probe would skip on exactly the runner the job
exists for.  On Windows a missing MSVC fails the build instead, and the error quotes
setuptools saying so.

**In the cython job a skip is a failure.**  A skip there would be a green job that compiled
nothing, so the job sets ``USLIB_REQUIRE_CYTHON=1``, and each condition above then fails
the test instead of skipping it.
"""
import importlib.util
import os
import pickle
import re
import shlex
import shutil
import subprocess
import sys
import sysconfig

import modelx as mx
import numpy as np
import pytest

from us_registry import LIB, model_path, point_keys, projection

pytestmark = pytest.mark.cython

MODEL = "Term_US_S"

# The repository root holds tools/.  A lifelib.create() copy of the library has no such
# root above it, and so no tool.
REPO = LIB.parents[2] if LIB.parent.name == "libraries" else None
TOOL = REPO / "tools" / "build_sec_cy.py" if REPO is not None else None

# The youngest issue age product-spec.md admits on any Term plan.  With expiry at attained
# age 95 it makes the longest frame, which the spec sizes the caches for.
MIN_ISSUE_AGE = 18

# Raised in both children, the sample run and the compiled run, because the export leaves
# the interpreter's default of 1,000 in place (F7).
RECURSION_LIMIT = 100_000

SAMPLE = '''\
"""mx2cy's sample run: result_cf() on every point of {model}'s shipped table.

mx2cy types each cell from what this run passes it and gets back.  The export does not
raise the recursion limit as modelx does, so the sample does.
"""
import sys

sys.setrecursionlimit({limit})

from {model}_nomx import mx_model  # noqa: E402

for point_id in {keys!r}:
    mx_model.Projection[point_id].result_cf()
'''

SPEC = '''\
# mx2cy's spec: the length of each C-array cache in Projection, by parameter.  The longest
# {model} frame runs from issue age {age} to expiry at attained age {expiry}: {frame}
# months, t = 0 .. {last}.  Plus one for a t + 1 look-ahead and one of headroom (the plan's
# section 6.1, step 6).  A t past the end raises IndexError in the compiled model, so the
# size comes from the contract, not from the points the sample happens to run.
{spec!r}
'''

RUNNER = '''\
"""Run a compiled package on model points, and pickle what it computed.

    python runner.py <out> <package> <recursion limit> <result file> <point_id> ...
"""
import importlib
import importlib.machinery
import pickle
import sys

out, package, limit, dest, *keys = sys.argv[1:]
sys.setrecursionlimit(int(limit))
sys.path.insert(0, out)
mx_model = importlib.import_module(package).mx_model

# Whether each space's class came from an extension module.  A package whose build lost an
# extension still imports, from the translated .py beside it, and computes the same numbers
# uncompiled, so the numbers alone cannot show that anything was compiled.
suffixes = tuple(importlib.machinery.EXTENSION_SUFFIXES)
compiled = {}
for space in (mx_model.Data, mx_model.Projection):
    cls = type(space)
    compiled[cls.__name__] = sys.modules[cls.__module__].__file__.endswith(suffixes)

frames = {int(key): mx_model.Projection[int(key)].result_cf() for key in keys}
with open(dest, "wb") as f:
    pickle.dump({"compiled": compiled, "frames": frames}, f)
'''


def _missing():
    """What this machine lacks to compile a model, or ``None`` when it lacks nothing."""
    if TOOL is None or not TOOL.is_file():
        return "tools/build_sec_cy.py is absent, as it is from a lifelib.create() copy"
    if importlib.util.find_spec("modelx_cython") is None:
        return "modelx-cython is not installed: pip install -r requirements-cython.txt"
    if os.name == "posix":
        command = os.environ.get("CC") or sysconfig.get_config_var("CC") or "cc"
        compiler = (shlex.split(command) or ["cc"])[0]
        if shutil.which(compiler) is None:
            return f"no C compiler: setuptools would run {compiler!r}, which is not on PATH"
    return None


@pytest.fixture(scope="module")
def build_sec_cy():
    """``tools/build_sec_cy.py`` as a module, or a skip, which the cython job fails."""
    missing = _missing()
    if missing is not None:
        if os.environ.get("USLIB_REQUIRE_CYTHON") == "1":
            pytest.fail(f"USLIB_REQUIRE_CYTHON=1 forbids a skip, and {missing}")
        pytest.skip(missing)
    spec = importlib.util.spec_from_file_location("build_sec_cy", TOOL)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_compiled_term_reproduces_modelx(build_sec_cy, tmp_path):
    """``Term_US_S``, compiled, computes modelx's ``result_cf()`` on every model point.

    The reference is read under a name of its own: reading the model under its saved name
    would rename any instance of it that the session already holds open, which is also why
    the build tool exports in a child process.  The compiled package must be loaded from its
    extension modules, not merely importable; its ``t`` caches must have the spec's size,
    not the sample's; and every column of every frame must agree.
    """
    reference = mx.read_model(model_path(MODEL), name=MODEL + "_cy_reference")
    try:
        keys = [int(key) for key in point_keys(reference)]
        expected = {key: projection(reference, key).result_cf() for key in keys}
        expiry = int(reference.Projection.expiry_age)
    finally:
        reference.close()
    # The comparisons below run over these points, so with none they would all pass.
    assert keys, f"{MODEL}'s model point table has no points to compile a sample from"
    frame = 12 * (expiry - MIN_ISSUE_AGE)

    sample = tmp_path / "sample.py"
    sample.write_text(
        SAMPLE.format(model=MODEL, limit=RECURSION_LIMIT, keys=keys), encoding="utf-8")
    spec = tmp_path / "spec.py"
    sizes = {"spaces": {"Projection": {"cells_param_size": {"t": frame + 2}}}}
    spec.write_text(
        SPEC.format(model=MODEL, age=MIN_ISSUE_AGE, expiry=expiry, frame=frame,
                    last=frame - 1, spec=sizes),
        encoding="utf-8")

    out = tmp_path / "out"
    compiled = build_sec_cy.build(
        model_path(MODEL).parent, model=MODEL, out=out, sample=sample, spec=spec)
    assert compiled == (out / f"{MODEL}_nomx_cy").resolve()

    # The spec reached the C: each Projection cell compiled with a C integer t keeps its
    # values in a C array of the spec's size.  The sample alone would have sized them to
    # its own frame, and the comparison below would pass all the same.
    pxd = (compiled / "_mx_classes.pxd").read_text(encoding="utf-8")
    t_cells = re.findall(r"cpdef [\w ]+? (\w+)\(_c_Projection self, long long t\)", pxd)
    caches = {name: int(size)
              for size, name in re.findall(r"cdef [\w ]+?\[(\d+)\] _v_(\w+)\b", pxd)}
    assert t_cells, f"no Projection cell of the compiled {MODEL} takes a C integer t"
    assert {cell: caches.get(cell) for cell in t_cells} == dict.fromkeys(t_cells, frame + 2)

    runner = tmp_path / "runner.py"
    runner.write_text(RUNNER, encoding="utf-8")
    result = tmp_path / "result.pickle"
    done = subprocess.run(
        [sys.executable, "-P", str(runner), str(out), compiled.name, str(RECURSION_LIMIT),
         str(result), *(str(key) for key in keys)],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    assert done.returncode == 0, (
        f"the compiled {MODEL} failed with exit code {done.returncode}:\n"
        f"{done.stdout[-2000:]}\n{done.stderr[-4000:]}")
    with result.open("rb") as stream:
        got = pickle.load(stream)

    assert got["compiled"] and all(got["compiled"].values()), (
        f"not every space was loaded from an extension module: {got['compiled']}")
    assert list(got["frames"]) == keys
    for key in keys:
        actual, wanted = got["frames"][key], expected[key]
        assert list(actual.columns) == list(wanted.columns), f"point {key}"
        assert actual.index.equals(wanted.index), f"point {key}"
        for column in wanted.columns:
            np.testing.assert_allclose(
                actual[column].to_numpy(dtype=float), wanted[column].to_numpy(dtype=float),
                rtol=1e-12, atol=0, err_msg=f"{MODEL} point {key}, column {column}")
