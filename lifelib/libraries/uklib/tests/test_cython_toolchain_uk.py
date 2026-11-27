"""The compile toolchain end to end: export, trace, translate, compile, run, compare.

UKLIB-SEC-PLAN.md compiles each SEC model at its C step and runs the compile tests in a
``cython_uk`` CI job of their own, on Linux and Windows (U7, after USLIB-SEC-PLAN.md D13).
This module gives that job a test before any uklib model is written for the compiler
(§3 item 4), so that its ``toolchain`` shard proves something real from the start: that
the library's ``build_sec_cy.py``, modelx-cython and the platform's C compiler together
turn a uklib model into a compiled package, and that the package computes what modelx
computes.  It is uslib's ``test_cython_toolchain.py`` read for this library; each SEC
model's own compile tests will stand beside it, from ``Term_UK_SEC``'s at M2.

**What it compiles.**  ``Term_UK_S``, an S model, which mx2cy compiles as it compiles any
export (F2): one whose cells still read pandas, the shape mx2cy handles least well, where
the SEC models' compile tests compile the shape the C step writes for it.  mx2cy's two
inputs are written by the test rather than added to the product directory.  The sample
runs ``result_cf()`` on every point of the shipped table, all eight.  The spec sizes every
cache of integer parameters for the longest frame any contract can have, because a
compiled cache raises ``IndexError`` past its end (F4), and the test reads the generated
declarations to see that it did, since the numbers cannot show it: mx2cy ignores a spec
key or space name it does not know and sizes each cache from the sample instead, and the
sample's own points then fit.  The build goes into ``tmp_path``, and the compiled package
runs in a child process, which raises the recursion limit, as modelx does and the export
does not (F7); a compiled model that overflows the C stack then takes down the child, not
the test session.  Its ``result_cf()`` must equal modelx's on every point to 1e-12
relative, the tolerance of C4 where it is not exact.  With gcc on Linux it is exact.  The
tool tells gcc and clang to fuse no multiply and add into a single rounding, whatever
``-march`` the interpreter's flags give, and to fail on a pointer of the wrong type, as
gcc 14 does, and the test reads the compiler's command lines in the build's log for both.

**The sizes, read off the model.**  ``Term_UK_S``'s frame is ``proj_len() = term_mths() =
12 * policy_term()`` months from issue, and the model bounds the term nowhere, so the
longest frame is the longest term ``product-spec.md`` admits, 50 years: 600 months,
``t = 0 .. 599``.  The cells compile to C arrays by five parameter tuples:

* ``t``, the policy month: 600, one more for the roll-forward's look-ahead
  ``pols_if(t + 1)``, and one of headroom, 602, as uslib's sized its ``t``
  (USLIB-SEC-PLAN.md §6.1, step 6);
* ``k``, ``benefit_sched``'s, which ``benefit_pp`` calls at ``duration_mth(t)``, the month
  ``t`` itself: as ``t``, 602;
* ``m``, ``annuity_certain_factor``'s, which the family income benefit calls at
  ``term_mths() - t``, largest at ``t = 0``, on a term of at most 40 years (product-spec
  again): 480, one to hold it, and one of headroom, 482;
* ``life``, ``age_at_entry``'s, 1 or 2, the two lives of a joint first death, any other
  refused by the formula itself: 3;
* ``(t, life)``, ``age``'s, ``mort_rate_base``'s and ``mort_rate_life``'s: ``(602, 3)``.

Each cell that takes C integers alone and returns a C scalar must keep its cache at its
tuple's size, and each size must be taken, since a spec key no cell takes is a misspelt
one; a cell returning text, as ``sex(life)`` does, keeps a dict, which no spec sizes.  The
sizes rest on the frame being ``12 * policy_term()`` months, so that is asserted on every
shipped point first, with each point's term inside the bounds the sizes are taken from.
The test reads the declarations itself rather than through ``uk_sec_support.spec_faults``:
``Term_UK_S`` gives ``life`` a default, which the declaration writes ``long long life=*``,
and the harness, written for SEC models, which default no integer, would read the
parameter's name as ``life=*``.

**When it skips.**  Without modelx-cython, which no model requires, because it needs a C
compiler; without a C compiler, on a POSIX system; and without the library's
``build_sec_cy.py``, which only a copy that left it behind lacks: it sits at the library's
root, so lifelib and every ``lifelib.create()`` copy carry it.  So the ``test`` CI job and
lifelib's own bare ``pytest`` skip it and stay green (D13).  The compiler is probed on
POSIX only.  There setuptools runs ``CC``, or the compiler the interpreter was built with,
from ``PATH``; on Windows it finds MSVC through vswhere at build time, and ``cl.exe`` is on
no ``PATH`` outside a developer prompt, so a ``PATH`` probe would skip on exactly the
runner the job exists for.  On Windows a missing MSVC fails the build instead, and the
error quotes setuptools saying so.

**In the cython_uk job a skip is a failure.**  A skip there would be a green job that
compiled nothing, so the job sets ``UKLIB_REQUIRE_CYTHON=1``, and each condition above then
fails the test instead of skipping it.  The conditions and the choice between skipping and
failing are ``uk_sec_support.cython_missing`` and ``uk_sec_support.require_cython``, which
every compile test shares.
"""
import os
import pickle
import re
import subprocess
import sys

import modelx as mx
import numpy as np
import pytest

from uk_sec_support import require_cython
from uk_registry import model_path, point_keys, projection

pytestmark = pytest.mark.cython

MODEL = "Term_UK_S"

# The longest terms product-spec.md admits: 1 to 50 years on the level and decreasing
# shapes, 5 to 40 on the family income benefit.  The first makes the longest frame, and the
# second the longest annuity-certain the commutation reads.
MAX_TERM_YEARS = 50
MAX_FIB_TERM_YEARS = 40

# Joint first death covers two lives, numbered 1 and 2; a single life is life 1.
LIVES = 2

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
# {model} frame is its longest term, {term} years: {frame} months, t = 0 .. {last}.  Plus
# one for the roll-forward's t + 1 and one of headroom, for t and for k, benefit_sched's
# month, which is t's.  m, annuity_certain_factor's, is term_mths() - t on a family income
# benefit, at most {fib} months, plus one and one of headroom; life is 1 or {lives}.  A
# t past the end raises IndexError in the compiled model, so the sizes come from the
# contract, not from the points the sample happens to run.
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


def cache_sizes():
    """The spec's sizes, ``{parameters: sizes}``, from the contract (module docstring)."""
    t = 12 * MAX_TERM_YEARS + 2
    life = LIVES + 1
    return {("t",): (t,), ("t", "life"): (t, life), ("life",): (life,), ("k",): (t,),
            ("m",): (12 * MAX_FIB_TERM_YEARS + 2,)}


# The C scalars a cell of C integers returns where mx2cy caches it in a C array.  One that
# returns text or an object, as Term_UK_S's sex(life) and smoker(life) do, keeps a dict,
# which no spec sizes.
C_SCALARS = ("bint", "long long", "double")


def compiled_caches(pxd):
    """What the generated declarations give ``Projection``'s cells of C integers alone
    that return a C scalar.

    ``{cell: (parameters, sizes)}``: the names of its parameters, without the ``=*`` the
    declaration writes after one with a default, and the dimensions of its C-array cache,
    ``None`` where it keeps none.
    """
    blocks = re.split(r"^cdef class _c_(\w+)\(", pxd, flags=re.M)
    body = dict(zip(blocks[1::2], blocks[2::2])).get("Projection", "")
    caches = {name: tuple(int(n) for n in re.findall(r"\[(\d+)\]", dims))
              for dims, name in re.findall(r"cdef [\w ]+?((?:\[\d+\])+) _v_(\w+)\b", body)}
    cells = {}
    declared = re.findall(r"cpdef ([\w ]+?) (\w+)\(_c_Projection self([^)]*)\)", body)
    for returns, name, params in declared:
        parts = [part.strip() for part in params.split(",") if part.strip()]
        if (returns in C_SCALARS and parts
                and all(part.startswith("long long ") for part in parts)):
            names = tuple(part.removeprefix("long long ").split("=")[0] for part in parts)
            cells[name] = (names, caches.get(name))
    return cells


@pytest.fixture(scope="module")
def build_sec_cy():
    """The library's ``build_sec_cy.py`` as a module, or a skip, which the cython_uk job
    fails."""
    return require_cython()


def test_compiled_term_reproduces_modelx(build_sec_cy, tmp_path):
    """``Term_UK_S``, compiled, computes modelx's ``result_cf()`` on every model point.

    The reference is read under a name of its own: reading the model under its saved name
    would rename any instance of it that the session already holds open, which is also why
    the build tool exports in a child process.  The compiled package must be loaded from its
    extension modules, not merely importable; every cache of C integers must have the
    spec's size, not the sample's; and every column of every frame must agree.
    """
    reference = mx.read_model(model_path(MODEL), name=MODEL + "_cy_reference")
    try:
        keys = [int(key) for key in point_keys(reference)]
        expected, outside = {}, []
        for key in keys:
            proj = projection(reference, key)
            expected[key] = proj.result_cf()
            term = proj.policy_term()
            longest = MAX_FIB_TERM_YEARS if proj.shape() == "fib" else MAX_TERM_YEARS
            if proj.proj_len() != 12 * term or not 0 < term <= longest:
                outside.append((key, proj.shape(), term, proj.proj_len()))
    finally:
        reference.close()
    # The comparisons below run over these points, so with none they would all pass.
    assert keys, f"{MODEL}'s model point table has no points to compile a sample from"
    assert not outside, (
        f"{MODEL}: the spec's sizes take the frame to be 12 * policy_term() months, on a "
        f"term of at most {MAX_TERM_YEARS} years ({MAX_FIB_TERM_YEARS} on the family "
        f"income benefit); (point, shape, term, proj_len) at odds: {outside}")
    frame = 12 * MAX_TERM_YEARS
    sizes = cache_sizes()

    sample = tmp_path / "sample.py"
    sample.write_text(
        SAMPLE.format(model=MODEL, limit=RECURSION_LIMIT, keys=keys), encoding="utf-8")
    spec = tmp_path / "spec.py"
    given = {(params[0] if len(params) == 1 else params):
             (size[0] if len(size) == 1 else size) for params, size in sizes.items()}
    spec.write_text(
        SPEC.format(model=MODEL, term=MAX_TERM_YEARS, frame=frame, last=frame - 1,
                    fib=12 * MAX_FIB_TERM_YEARS, lives=LIVES,
                    spec={"spaces": {"Projection": {"cells_param_size": given}}}),
        encoding="utf-8")

    out = tmp_path / "out"
    compiled = build_sec_cy.build(
        model_path(MODEL).parent, model=MODEL, out=out, sample=sample, spec=spec)
    assert compiled == (out / f"{MODEL}_nomx_cy").resolve()

    # Off Windows every command that compiles a C file ends its flags with the tool's
    # NO_CONTRACT, so that no -march before it makes gcc or clang fuse a multiply and an
    # add, and the compiled model rounds where modelx rounds; and carries its
    # NO_INCOMPATIBLE_POINTERS, so that a pointer of the wrong type fails the build under
    # any gcc, as gcc 14 fails it.  MSVC reads no CFLAGS.
    if os.name != "nt":
        log = out / "build" / build_sec_cy.LOG
        lines = log.read_text(encoding="utf-8", errors="replace").splitlines()
        compiles = [line for line in lines if re.search(r" -c \S+\.c\b", line)]
        assert compiles, f"no command compiling a C file in {log}"
        for line in compiles:
            assert re.findall(r"-ffp-contract=(\w+)", line)[-1:] == ["off"], line
            assert build_sec_cy.NO_INCOMPATIBLE_POINTERS in line.split(), line

    # The spec reached the C: each Projection cell compiled with C integers alone keeps
    # its values in a C array of the spec's size for its parameters, and each size is
    # some cell's.  The sample alone would have sized them to its own frames, and the
    # comparison below would pass all the same.
    cells = compiled_caches((compiled / "_mx_classes.pxd").read_text(encoding="utf-8"))
    assert cells, f"no Projection cell of the compiled {MODEL} takes C integers alone"
    wrong = {cell: (params, cache) for cell, (params, cache) in sorted(cells.items())
             if cache != sizes.get(params)}
    assert not wrong, (
        f"caches not of the spec's sizes {sizes}, by cell, (parameters, cache): {wrong}")
    untaken = set(sizes) - {params for params, _ in cells.values()}
    assert not untaken, f"the spec sizes {sorted(untaken)}, which no compiled cell takes"

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
