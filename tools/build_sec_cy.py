"""Compile a uslib SEC model with modelx-cython: export, trace, translate, build.

USLIB-SEC-PLAN.md's Phase 2 makes each ``<Name>_US_SEC`` model compile (its D12).  The
compiler is mx2cy, the command modelx-cython installs, and it does not compile a modelx
model: it compiles the model's **export**, the self-contained Python package that
``Model.export`` writes.  So a build is three steps, and this tool runs them in order:

1. export the model to ``<out>/<Model>_nomx/``;
2. copy the product's CSVs to ``<out>``, unless ``<out>`` is the product directory, where
   they already are;
3. run mx2cy on the export with the product's ``sample_sec.py`` and ``spec_sec.py``.  It
   traces the sample's run of the export to learn each cell's types, translates a copy of
   the package to ``<out>/<Model>_nomx_cy/``, writes ``<out>/setup.py`` and compiles in
   place, which leaves setuptools' ``<out>/build/`` tree behind.

:func:`build` returns the path of ``<Model>_nomx_cy/``, the compiled package.  It is
imported as the export is -- ``from Term_US_SEC_nomx_cy import mx_model``, with ``<out>``
on ``sys.path`` -- and its spaces are C extension types.

**The sample and the spec.**  mx2cy types a cell from the values the sample run passes it
and gets back, so a cell the sample never calls compiles untyped, and the spec sizes each
cell's C-array cache, which raises ``IndexError`` past its end (the plan's F3 and F4).
Both are written in Phase 2, one pair per product (§6.1, step 6).  Until then no product
has them and the tool is inert, exercised only by ``test_cython_toolchain.py``, which
compiles ``Term_US_S`` with a sample and a spec of its own.  The sample must raise the
recursion limit itself: modelx raises it, and the export does not (F7).

**Why each step runs in a child process.**  Neither leaves its caller as it found it.
mx2cy traces under ``sys.setprofile``, configures the root logger, and imports the export
by name, and ``sys.modules`` keeps it: a second build in the same process would trace the
first build's package.  The export reads the model fresh from disk, and modelx keeps one
session per process, in which reading a model whose name is already open renames the open
one to ``<name>_BAK1`` (with a warning, in modelx 0.33.0).  A test session that holds the
S suite's model open would find it renamed under it.  In a child, the export reads the
model under its own name, which the exported package keeps, and the caller's session is
untouched.

**Why the CSVs travel.**  An exported package defines its model's ``path`` as its own
directory, compiled or not, so ``Data.input_dir()``, which is ``_model.path.parent``,
resolves to the directory that **contains** the package (F6).  The CSVs must sit there,
beside both packages, for mx2cy's sample run and for whatever imports the result later.
In the product directory they already do.  Anywhere else, every CSV of the product
directory is copied, as ``test_round_trip_is_stable`` copies them: an SEC model reads its
twin's tables as well as its own (D1), so the directory's set is the one to copy.

**Why nothing it writes is ever committed (D12).**  All of it derives from committed
files -- the model, ``sample_sec.py`` and ``spec_sec.py`` -- so it is rebuilt, never kept.
None of it is portable either: an extension module is built for one operating system,
processor and CPython ABI (``.cpython-313-x86_64-linux-gnu.so``,
``.cp313-win_amd64.pyd``).  The translated modules are a second, annotated copy of every
formula, which would drift from the model the first time a formula changed, and lifelib's
wheel must carry none of it (§8.1, K8).  The default ``<out>`` is the product directory,
and ``.gitignore`` covers everything a build leaves there: ``*_nomx/``, ``*_nomx_cy/``,
``build/``, ``setup.py`` and ``*.so``.  Any other ``<out>`` receives a copy of every CSV,
over any file of the same name, so the tool refuses two kinds of it.  One holding a model
is a product directory, whose own inputs the copies would replace: pointed at WholeLife's,
a build of Term overwrote three of its tables and exited 0.  And one inside this
repository would hold untracked inputs that no pattern can tell from real ones.

**A rebuild starts clean.**  The previous ``<Model>_nomx/`` and ``<Model>_nomx_cy/`` are
removed first.  modelx's exporter writes into an existing folder without clearing it, so a
cell deleted from the model would survive in a stale export; and mx2cy, finding an old
compiled package, moves it aside to ``<Model>_nomx_cy_BAK1/`` rather than replacing it.

**Output.**  Everything the two children print goes to ``<out>/build/build_sec_cy.log``,
since a compile prints hundreds of lines and the one that matters on failure is near the
end.  A failure raises :class:`BuildError`, which names the step and quotes the log's last
lines, and the first error of a chained traceback when they leave it out
(:func:`_quote`).  modelx-cython needs a C compiler, so ``requirements.txt`` leaves it
out; without it the tool raises before writing anything (``pip install -r
requirements-cython.txt``).

Usage::

    python tools/build_sec_cy.py term_life                  # Term_US_SEC, in place
    python tools/build_sec_cy.py term_life --out /tmp/term  # elsewhere, with the CSVs
    python tools/build_sec_cy.py lifelib/libraries/uslib/products/term_life \\
        --model Term_US_S --sample my_sample.py --spec my_spec.py

The product is a product directory, or the folder name of a uslib product.  The tool
prints the compiled package's path and exits 0.  It exits 1 when a step fails, and 2 when
it cannot start: a malformed command line, no modelx-cython, a missing model, sample or
spec, or an ``--out`` it refuses.
"""
import argparse
import importlib.machinery
import importlib.util
import os
import pathlib
import shutil
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
PRODUCTS = REPO / "lifelib" / "libraries" / "uslib" / "products"

SAMPLE = "sample_sec.py"
SPEC = "spec_sec.py"
LOG = "build_sec_cy.log"

# One line, so that it passes through any platform's command line unchanged.  The model is
# closed by the child's exit, whether or not the export succeeded.
_EXPORT = ("import sys, modelx; model = modelx.read_model(sys.argv[1]); "
           "model.export(sys.argv[2]); model.close()")


class BuildError(RuntimeError):
    """A build step failed.  The message names the step and quotes the end of its log."""


def find_model(product_dir, model=None):
    """The folder of the model to compile: ``model``, or the product's one ``*_SEC`` model.

    A model folder is one holding a ``_system.json``, as ``tools/gen_scaffolding.py``
    recognizes it, so an export beside the model -- a Python package, but not a modelx
    model -- is never taken for one.  ``model`` is a folder name in ``product_dir``, never
    a path: the CSVs come from ``product_dir``, and a model from anywhere else would be
    built against tables it was not written for.  With no ``model``, several ``*_SEC``
    folders are an error, not a choice to make by directory order (the plan's F8).
    """
    product_dir = pathlib.Path(product_dir)
    if model is not None:
        if pathlib.PurePath(model).name != str(model):
            raise ValueError(
                f"model names a model folder in {product_dir}; {model!r} is a path")
        folder = product_dir / model
        if not (folder / "_system.json").is_file():
            raise FileNotFoundError(
                f"{folder} is not a modelx model folder: it holds no _system.json")
        return folder
    found = [d for d in sorted(product_dir.iterdir())
             if d.is_dir() and d.name.endswith("_SEC") and (d / "_system.json").is_file()]
    if len(found) == 1:
        return found[0]
    if not found:
        raise FileNotFoundError(
            f"no *_SEC model in {product_dir}: Phase 1 of USLIB-SEC-PLAN.md adds one per "
            "product.  Name the model to compile with model= (--model)")
    names = ", ".join(d.name for d in found)
    raise ValueError(
        f"{len(found)} *_SEC models in {product_dir} ({names}); name one with model= "
        "(--model)")


def _script(given, default, role):
    """The sample's or the spec's absolute path, which must exist before anything runs."""
    path = default if given is None else pathlib.Path(given).resolve()
    if not path.is_file():
        hint = (f"; each product's {default.name} is written in Phase 2 of "
                "USLIB-SEC-PLAN.md (section 6.1, step 6)" if given is None else "")
        raise FileNotFoundError(f"no {role} {path}{hint}")
    return path


def _remove(path):
    """Delete a previous build's folder, explaining the one failure that is not a bug."""
    if not path.exists():
        return
    try:
        shutil.rmtree(path)
    except OSError as err:
        raise BuildError(
            f"cannot remove the previous build {path}: {err}.  On Windows a compiled "
            "package cannot be deleted while a Python process has it imported") from err


# The line Python prints between the exceptions of a chained traceback, the first error
# first.
_CHAINED = ("During handling of the above exception, another exception occurred:",
            "The above exception was the direct cause of the following exception:")


def _quote(log, lines=40):
    """What a :class:`BuildError` quotes from the log: its end, and its first error.

    The end is the last ``lines`` lines, which is where a compiler's error lands.  A Python
    traceback prints a chain's first error first, though, and the end can leave it out.
    When a sample fails before it imports the export -- a misspelled package name, say --
    mx2cy's tracer fails again on its way out, looking up a module the sample never
    imported, and that second traceback fills the end: a ``KeyError`` naming
    ``<Model>_nomx._mx_model``, with the sample's ``ModuleNotFoundError`` above it, out of
    sight.  So the last error before the failed step's first chaining line is quoted too,
    unless the end already shows it.  The log is decoded whatever the compiler's code page.
    """
    rows = log.read_bytes().decode("utf-8", errors="replace").splitlines()
    end = max(len(rows) - lines, 0)
    step = max((i for i, row in enumerate(rows) if row.startswith("=== ")), default=0)
    first = ""
    for i in range(step, len(rows)):
        if rows[i].strip() in _CHAINED:
            cause = next((j for j in range(i - 1, step, -1) if rows[j].strip()), None)
            if cause is not None and cause < end:
                first = ("The first error in the log, which its end leaves out:\n\n"
                         f"    {rows[cause].strip()}\n\n")
            break
    return f"{first}The end of {log}:\n\n" + "\n".join(rows[end:])


def _run(step, cmd, cwd, log):
    """Run one step in a child process, appending its output to the log.

    The child writes straight into the file, as bytes, so nothing here decodes a
    compiler's output until a failure has to quote it.  It writes unbuffered, so that its
    own messages and the compiler's, which reach the file by separate routes, land in the
    order they happened: the failure is quoted from the end.  ``-P`` keeps the working
    directory off the child's ``sys.path``; mx2cy puts ``<out>`` there itself, and only
    while the sample runs.
    """
    shown = " ".join("<script>" if arg == _EXPORT else arg for arg in cmd)
    env = {**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONUNBUFFERED": "1"}
    with log.open("ab") as stream:
        stream.write(f"\n=== {step}\n$ {shown}\n".encode())
        stream.flush()
        done = subprocess.run(cmd, cwd=cwd, env=env, stdout=stream,
                              stderr=subprocess.STDOUT)
    if done.returncode:
        raise BuildError(
            f"{step} failed with exit code {done.returncode}.  {_quote(log)}")


def _check_compiled(compiled, log):
    """Fail unless every space module of the package was compiled to an extension module.

    mx2cy exits 0 once setuptools does, and a package can import with an extension
    missing: the translated ``.py`` sits beside it and imports in its place, computing the
    same numbers uncompiled.  So the build is checked for the extension modules themselves.
    """
    sources = sorted(compiled.rglob("_mx_classes.py")) if compiled.is_dir() else []
    suffixes = importlib.machinery.EXTENSION_SUFFIXES
    missing = [s for s in sources
               if not any(s.with_name(s.stem + x).is_file() for x in suffixes)]
    if not sources or missing:
        what = ", ".join(str(s.relative_to(compiled)) for s in missing) or "anything"
        raise BuildError(
            f"mx2cy reported success, but {compiled} has no extension module for {what}.  "
            f"{_quote(log)}")


def _check_out(out, model_dir):
    """Refuse an ``out``, other than the product directory, that the CSVs must not go to.

    A build anywhere but the product directory copies every CSV of the product there, over
    any file of the same name.  An ``out`` that holds a model is a product directory, and
    the copies would replace that model's own inputs.  One inside this repository would
    hold untracked inputs that no ``.gitignore`` pattern can tell from real ones, beside a
    model or not.  And one inside the model folder, or a file, cannot take a build at all.
    """
    if out == model_dir or model_dir in out.parents:
        raise ValueError(f"out {out} is inside the model folder {model_dir}")
    if out.exists() and not out.is_dir():
        raise ValueError(f"out {out} is a file, not a directory")
    if out == REPO or REPO in out.parents:
        raise ValueError(
            f"out {out} is inside the repository {REPO}, where the CSVs a build copies "
            "would be untracked inputs that no .gitignore pattern can tell from real "
            "ones.  Build in place, without out (--out), or outside the repository")
    held = sorted(d.name for d in out.iterdir()
                  if (d / "_system.json").is_file()) if out.is_dir() else []
    if held:
        raise ValueError(
            f"out {out} holds the model {', '.join(held)}: it is a product directory, and "
            "the CSVs a build copies there would overwrite that model's own inputs")


def settle(product_dir, model=None, out=None, sample=None, spec=None):
    """:func:`build`'s arguments, checked and made absolute, before anything is written.

    Returns ``(product_dir, model_dir, out, sample, spec)``, with the defaults filled in.
    Raises ``ModuleNotFoundError`` without modelx-cython, ``FileNotFoundError`` or
    ``ValueError`` for a missing or ambiguous model, sample or spec, and ``ValueError`` for
    an ``out`` the product's CSVs must not be copied to (:func:`_check_out`).
    :func:`build` calls it first; the command line calls it too, to name the build before
    it starts.
    """
    product_dir = pathlib.Path(product_dir).resolve()
    if not product_dir.is_dir():
        raise FileNotFoundError(f"no product directory {product_dir}")
    model_dir = find_model(product_dir, model).resolve()
    sample = _script(sample, product_dir / SAMPLE, "sample")
    spec = _script(spec, product_dir / SPEC, "spec")
    out = product_dir if out is None else pathlib.Path(out).resolve()
    if out != product_dir:
        _check_out(out, model_dir)
    if importlib.util.find_spec("modelx_cython") is None:
        raise ModuleNotFoundError(
            f"modelx-cython is not installed for {sys.executable}.  It needs a C "
            "compiler, so requirements.txt leaves it out: pip install -r "
            "requirements-cython.txt", name="modelx_cython")
    return product_dir, model_dir, out, sample, spec


def build(product_dir, model=None, out=None, sample=None, spec=None):
    """Export, translate and compile one model; return the compiled package's path.

    ``product_dir`` is the product directory, which holds the model and its CSVs.
    ``model`` is the folder name of the model to compile, by default the product's one
    ``*_SEC`` model (:func:`find_model`).  ``out`` is where the build goes, by default
    ``product_dir``; any other directory is created if need be and receives a copy of every
    CSV, so it must hold no model and lie outside this repository (:func:`_check_out`).
    ``sample`` and ``spec`` are mx2cy's two inputs, by default ``sample_sec.py`` and
    ``spec_sec.py`` in ``product_dir``.

    Returns ``<out>/<model>_nomx_cy``.  Raises what :func:`settle` raises, before writing
    anything, and :class:`BuildError` when a step fails.
    """
    product_dir, model_dir, out, sample, spec = settle(
        product_dir, model, out, sample, spec)

    name = model_dir.name
    exported = out / f"{name}_nomx"
    compiled = out / f"{name}_nomx_cy"
    log = out / "build" / LOG
    _remove(exported)
    _remove(compiled)
    log.parent.mkdir(parents=True, exist_ok=True)
    log.write_bytes(b"")

    _run(f"exporting {name}", [sys.executable, "-P", "-c", _EXPORT, str(model_dir),
                               str(exported)], out, log)
    if out != product_dir:
        for csv in sorted(product_dir.glob("*.csv")):
            shutil.copy2(csv, out / csv.name)
    _run(f"mx2cy on {exported.name}",
         [sys.executable, "-P", "-m", "modelx_cython", str(exported),
          "--sample", str(sample), "--spec", str(spec), "--setup", str(out / "setup.py")],
         out, log)
    _check_compiled(compiled, log)
    return compiled


def product_directory(arg):
    """The product directory a command-line argument names, or ``None``.

    An existing directory is taken as it is; anything else is looked up as the folder name
    of a uslib product, so ``term_life`` works from any working directory.
    """
    path = pathlib.Path(arg)
    if path.is_dir():
        return path
    if (PRODUCTS / arg).is_dir():
        return PRODUCTS / arg
    return None


def main(argv):
    parser = argparse.ArgumentParser(
        prog="python tools/build_sec_cy.py",
        description="Compile a uslib SEC model with modelx-cython (USLIB-SEC-PLAN.md D12).")
    parser.add_argument(
        "product", help="a product directory, or the folder name of a uslib product")
    parser.add_argument(
        "--model", help="the model folder to compile (default: the product's *_SEC model)")
    parser.add_argument(
        "--out", help="the directory to build in (default: the product directory)")
    parser.add_argument(
        "--sample", help=f"mx2cy's sample script (default: <product>/{SAMPLE})")
    parser.add_argument(
        "--spec", help=f"mx2cy's spec file (default: <product>/{SPEC})")
    args = parser.parse_args(argv)

    product = product_directory(args.product)
    if product is None:
        parser.error(f"{args.product!r} is neither a directory nor a product in {PRODUCTS}")
    given = (product, args.model, args.out, args.sample, args.spec)
    try:
        _, model_dir, out, _, _ = settle(*given)
    except (ModuleNotFoundError, FileNotFoundError, ValueError) as err:
        print(err, file=sys.stderr)
        return 2
    print(f"building {model_dir.name} in {out}, which takes a minute or more; the "
          f"compiler's output goes to {out / 'build' / LOG}")
    try:
        compiled = build(*given)
    except BuildError as err:
        print(err, file=sys.stderr)
        return 1
    print(f"compiled: {compiled}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
