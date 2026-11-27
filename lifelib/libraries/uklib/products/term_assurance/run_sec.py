"""Run the Term_UK_SEC model and print a model point's cash flows, or the block's.

    python products/term_assurance/run_sec.py            # point 1, the anchor cell at t = 0
    python products/term_assurance/run_sec.py 8          # the anchor cell in force 5 years
    python products/term_assurance/run_sec.py --block    # every model point, summed by row
    python products/term_assurance/run_sec.py 8 --cython # point 8 on the compiled model

``t`` counts months from the valuation date, which is the same instant for every model
point, so row ``t`` of one point's frame is the same month as row ``t`` of any other's, and
a block is the frames summed row by row.  Points are named by their ``point_id``.  The
runner takes ``Projection``'s key from the model: the label where ``Projection`` takes
``point_id``, as an SEC model does before it compiles, as this one did at its stage
``"E"``, and the position where it takes ``idx``, as this one does from its C step, as
basiclife's BasicTerm_SC is indexed, and as every compiled model is.

``--cython`` runs the compiled model instead of modelx, and prints the same lines.  It is
``Term_UK_SEC_nomx_cy`` beside the model, which the library's ``build_sec_cy.py``, at its
root, builds there the first time, and again whenever it is not built for this interpreter
or the model, ``sample_sec.py``, ``spec_sec.py`` or the tool is newer than it.  The model
compiles from its C step on (UKLIB-SEC-PLAN.md U2, milestone M2), which brought
``sample_sec.py`` and ``spec_sec.py``.  The build is never committed, and ``.gitignore``
covers everything it leaves.  The tool goes wherever the library goes, into lifelib and
into a ``lifelib.create()`` copy, so the runner builds wherever the library is; a product
directory taken out of its library has no tool above it, and there ``--cython`` stops,
saying so, where it would build.  ``--build DIR`` runs the package a build put in ``DIR``
instead, on the CSVs the build copied there, and never builds.  Either way the runner
stops, saying why, if the package imports without its extension modules, which would
compute the same numbers uncompiled.

A block run releases each point's ItemSpace once it is read, so that it holds one point's
cells at a time.  Deleting the ItemSpace is not enough, because it sits in reference
cycles that only Python's cyclic collector frees, so the runner collects after each
release, in both passes.  It freezes everything alive (``gc.freeze``) once the model and
its table are read, and again once it has every point's frame, so that each collection
scans only what the block has made since.  The block's sum is kept as it goes, a frame at
a time, compensated as pandas' ``groupby`` sum is, so that it is the sum of the frames
concatenated and grouped by ``t``, bit for bit.

Output is ASCII-only so it prints on a Windows console under any code page.
"""
import gc
import importlib
import importlib.machinery
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
NAME = "Term_UK_SEC"
SUFFIXES = tuple(importlib.machinery.EXTENSION_SUFFIXES)
USAGE = ("usage: python run_sec.py [point_id | --block] [--cython] [--build DIR]")


def parse(argv):
    """``(point_id or None for the block, cython, build_dir)``, or exit with the usage."""
    point, block, cython, build = None, False, False, None
    args = iter(argv)
    for arg in args:
        if arg == "--block":
            block = True
        elif arg == "--cython":
            cython = True
        elif arg == "--build":
            build = next(args, None)
            if build is None:
                sys.exit(USAGE)
            cython = True
        elif arg.startswith("-") or point is not None or not arg.isdigit():
            sys.exit(USAGE)
        else:
            point = int(arg)
    if block and point is not None:
        sys.exit(USAGE)
    return (None if block else (1 if point is None else point)), cython, build


def _built(package):
    """The compiled space module of ``package`` built for this interpreter, if any."""
    found = [package / f"_mx_classes{suffix}" for suffix in SUFFIXES]
    return [path for path in found if path.is_file()]


def _tool():
    """``build_sec_cy.py`` of the library holding this product, or ``None``.

    The product sits at ``<lib>/products/<product>``, and the library carries its build
    tool at its root, beside ``products/``, wherever the library is: in its source
    repository, in lifelib or in a ``lifelib.create()`` copy, as ``uk_sec_support._tool``
    finds it.  A product directory taken out of its library has no tool above it.
    """
    up = HERE.parents
    if len(up) < 2 or up[0].name != "products":
        return None
    return up[1] / "build_sec_cy.py"


def compiled_model(build_dir):
    """The compiled model: from ``build_dir``, or built in place first where it is stale."""
    if build_dir is None:
        out, tool = HERE, _tool()
        package = out / f"{NAME}_nomx_cy"
        sources = [*(HERE / NAME).rglob("*.py"), HERE / "sample_sec.py",
                   HERE / "spec_sec.py", *([tool] if tool else [])]
        built = _built(package)
        newest = max((path.stat().st_mtime for path in sources if path.is_file()),
                     default=0.0)
        if not built or min(path.stat().st_mtime for path in built) < newest:
            if tool is None or not tool.is_file():
                sys.exit("--cython builds the model with its library's build_sec_cy.py, "
                         "and this product directory is in no library that carries one, "
                         "so it cannot build")
            print(f"building {NAME} with {tool.name}, which takes about a minute ...",
                  file=sys.stderr)
            done = subprocess.run([sys.executable, str(tool), str(HERE)],
                                  stdout=subprocess.DEVNULL)
            if done.returncode:
                sys.exit(f"the build failed; {tool.name} printed why")
    else:
        out = Path(build_dir).resolve()
        package = out / f"{NAME}_nomx_cy"
        if not _built(package):
            sys.exit(f"{package} holds no build of {NAME} for this interpreter")
    sys.path.insert(0, str(out))
    model = importlib.import_module(f"{NAME}_nomx_cy").mx_model
    space = type(model.Projection)
    if not sys.modules[space.__module__].__file__.endswith(SUFFIXES):
        sys.exit(f"{package} imported without its extension modules, so it would run "
                 f"uncompiled; rebuild it with the library's build_sec_cy.py")
    return model


point_id, cython, build_dir = parse(sys.argv[1:])
if cython:
    model = compiled_model(build_dir)
else:
    import modelx as mx
    model = mx.read_model(HERE / NAME)
table = model.Data.model_point_table()
# Projection's key for each point_id: its position, or the label itself (the docstring).
if cython or tuple(model.Projection.parameters) == ("idx",):
    key = {label: i for i, label in enumerate(table.index)}
else:
    key = {label: label for label in table.index}


def release(label):
    """Drop a point's ItemSpace once read, and collect it (the module docstring)."""
    del model.Projection[key[label]]
    gc.collect()


def add(total, compensation, frame):
    """Add ``frame``'s rows to the running sum's first rows, compensated (Kahan), as
    pandas' ``groupby`` sum adds each group's values in turn."""
    rows = len(frame)
    y = frame - compensation[:rows]
    t = total[:rows] + y
    compensation[:rows] = (t - total[:rows]) - y
    total[:rows] = t


def describe(proj):
    """One line on where the point stands at the valuation date."""
    d = proj.duration_mth_init()
    if d < 0:
        return "to be issued at t = {}, {} months after the valuation date".format(-d, -d)
    if d == 0:
        return "issued at the valuation date, t = 0"
    return "in force {} months: policy year {}, attained age {}, {:.6f} in force".format(
        d, proj.policy_year(0), proj.age(0, 1), proj.pols_if(0))


def origin(label):
    """Where the generator took the row from, where the table records it."""
    if "row_kind" not in table.columns:
        return ""
    kind, source, m = (table.at[label, c]
                       for c in ("row_kind", "source_policy_id", "source_mth"))
    if kind == "derived":
        return " (S's {} at its month {})".format(source, m)
    if kind == "future":
        return " (S's {}, issued {} months on)".format(source, -m)
    return " (S's {})".format(source)


def product(proj):
    """The point's product in one line: its life, shape, term, cover and options."""
    cover = ("income {:,.0f}/month".format(proj.fib_income()) if proj.shape() == "fib"
             else "cover {:,.0f}".format(proj.sum_assured()))
    options = [option for option, held in (("indexed", proj.indexation()),
                                           ("waiver", proj.wop())) if held]
    if proj.is_joint():
        options.append("joint with {}{} smoker {}".format(
            proj.sex(2), proj.age_at_entry(2), proj.smoker(2)))
    return "{}{} smoker {} {} shape, {}-year term, {}, {} mode, {} basis{}".format(
        proj.sex(1), proj.age_at_entry(1), proj.smoker(1), proj.shape(), proj.policy_term(),
        cover, proj.premium_mode(), proj.mort_basis(),
        "".join(", " + option for option in options))


if point_id is None:
    # Every point's frame first.  The table checks itself as it is read, but whether a
    # point is still in cover, whether the contract issues it, and whether its waiver
    # pipeline is whole, are the product's rules, which proj_len() applies, so such a point
    # would otherwise stop the run part-way, after the points before it.  The model and its
    # table are frozen first, so that the collection after each release scans only what the
    # release left.
    rows = {}
    gc.freeze()
    for label in table.index:
        rows[label] = model.Projection[key[label]].proj_len()
        release(label)
    gc.freeze()
    total, columns = np.zeros((max(rows.values(), default=0), 0)), None
    print("model points, t = 0 the valuation date for each:")
    for label in table.index:
        proj = model.Projection[key[label]]
        df = proj.result_cf()
        if columns is None:
            columns = list(df.columns)
            total = np.zeros((len(total), len(columns)))
            compensation = np.zeros_like(total)
        add(total, compensation, df[columns].to_numpy())
        print("  {:>2}  {:<15} {}; proj_len {}".format(
            label, table.at[label, "policy_id"], describe(proj), rows[label]))
        del proj, df
        release(label)                          # each point is read once, then released
    block = pd.DataFrame(total, columns=columns,
                         index=pd.RangeIndex(len(total), name="t"))
    print()
    print("the block, first 12 rows, t = 0..11 (months from the valuation date):")
    print(block.head(12).round(2).to_string())
    print()
    print("the block summed into projection years 1-12, year = t // 12 + 1:")
    years = pd.Index(block.index // 12 + 1, name="proj_year")
    annual = block.drop(columns="pols_if").groupby(years).sum()
    annual.insert(0, "pols_if", block["pols_if"].groupby(years).first())
    print(annual.head(12).round(2).to_string())
else:
    if point_id not in key:
        sys.exit(f"no model point {point_id} in the table: {list(key)}")
    proj = model.Projection[key[point_id]]
    print("model point {}: {}{} - {}".format(
        point_id, table.at[point_id, "policy_id"], origin(point_id), product(proj)))
    print("at the valuation date: {}".format(describe(proj)))
    print("proj_len = {} months from the valuation date (t = 0..{}); cover ends at policy "
          "month {}".format(proj.proj_len(), proj.proj_len() - 1, proj.term_mths()))
    print()
    print("first 12 rows, t = 0..11 (months from the valuation date):")
    print(proj.result_cf().head(12).round(2).to_string())
    print()
    print("policy counts, t = 0..11:")
    print(proj.result_pols().head(12).round(6).to_string())

if not cython:
    model.close()
