"""Time a compiled uslib SEC model against its export and modelx (USLIB-SEC-PLAN.md C6).

Phase 2 of USLIB-SEC-PLAN.md makes each ``<Name>_US_SEC`` model compile, and its C6 asks
what that buys: the same block run, timed on three engines, with peak memory beside each
time (§8.1, K2).  This script is that benchmark.  It is a script, not a test, because what
it measures depends on the machine and on what else the machine is doing, so it reports
both, and what it prints goes into the product's ``model-sec.md`` with them.

**The engines.**  ``modelx`` reads the model folder.  ``export`` imports the
``<Model>_nomx`` package that modelx's ``Model.export`` writes, the pure-Python form mx2cy
compiles.  ``compiled`` imports ``<Model>_nomx_cy``, the package ``tools/build_sec_cy.py``
compiles from it.  All three run the same formulas on the same inputs, so they must agree
on every number, and the script checks that they do.

**The blocks.**  The committed model point table, repeated: each copy keeps every cell's
text as committed, and its ``point_id`` is renumbered so that every point has its own.  The
engines differ in speed by two orders of magnitude, so each gets a block of its own size,
by default about 6,000 points compiled, 600 exported and 120 in modelx, and every time is
reported per point beside the total.  A block is a directory holding the product's CSVs,
the repeated table, the model folder and both packages, which read the CSVs of the
directory that holds them (the plan's F6).  A product's SEC companion files keyed by
``point_id``, ``DIA_US_SEC``'s premium schedule and ``IUL_US_SEC``'s in-force ladder, are
repeated with it, copy by copy, each row under the label its point takes in that copy, so
that every point of the block reads its own rows (M24).

**What is timed.**  Each run is a fresh child process, so that no engine inherits another's
caches or memory.  The child imports its engine and reads the model, untimed.  Then:

``Data``
    every cell of ``Data`` evaluated once: the files read, and every vector and array the
    projection reads built.  Timed, and reported on its own line, because it is paid once
    a block whatever its size.
the frames
    the block run as ``run_sec.py --block`` makes it: everything alive frozen
    (``gc.freeze``), every point asked for its frame and released, then everything alive
    frozen again.  Timed, and reported beside the Data.
the loop
    every point projected and then released, ``del model.Projection[i]`` followed by a
    full ``gc.collect()``, as ``run_sec.py --block`` releases it.  This is the time the
    table reports.

The loop is run two ways, each in runs of its own:

``net_cf``
    ``net_cf(t)`` summed over the frame: the projection alone, the counterpart of
    ``basiclife/BasicTerm_SC``'s ``pv_net_cf()``, by which the plan's F2 times that model's
    compiled form against its export.
``result_cf``
    ``result_cf()``, the report ``run_sec.py`` prints, which builds a DataFrame for each
    point.

Every engine, loop and repeat is one run, and the runs go round the engines in turn, so
that a change of load on a shared machine falls on all of them alike.  Each time is the
fastest of its repeats, with the spread beside it.

**Memory.**  Each run reports its peak resident set, and how much the peak grew during the
loop.  A compiled ``Projection`` ItemSpace embeds every cell's cache in its C struct, and
it sits in reference cycles, so deleting it frees nothing until the cyclic collector runs:
a block that left it to Python's own collections would hold hundreds of them.  The
collection after each release keeps the block flat, and ``--no-collect`` leaves it out, in
the frames and in the loop, to show what it saves.  The peak comes from ``resource`` where
it exists, from ``psutil`` where that is installed, and is otherwise reported as unknown,
as on Windows without ``psutil``.

**The checks.**  A run sums ``net_cf`` over every month of every point of its block.  That
sum, divided by the number of copies in the block, must agree across every engine, loop
and repeat to 1e-9 relative, or the script exits 1 without a table.  And the compiled
engine must have imported its extension modules: a package whose build lost one imports
the translated Python beside it and computes the same numbers, uncompiled.

The build is ``tools/build_sec_cy.py``'s, made into a temporary directory and removed at
the end, or a directory a build was made in, given as ``--build``, which the script warns
of when the model, the sample or the spec is newer than it.  The blocks go in a temporary
directory too.  Nothing is written in the repository, unless ``--json`` names a file
there.

Usage::

    python tools/bench_sec_cy.py term_life                    # builds, then benchmarks
    python tools/bench_sec_cy.py term_life --build /tmp/term  # a build made with --out
    python tools/bench_sec_cy.py term_life --repeat 1 --copies 100 --export-copies 10 \\
        --modelx-copies 2                                     # a quick look

It prints a Markdown table, with the machine, the versions, the load and the command, and
exits 0.  It exits 1 when a run fails or the engines disagree, and 2 when it cannot start.
"""
import argparse
import csv
import datetime
import importlib.machinery
import importlib.metadata
import importlib.util
import io
import json
import math
import os
import pathlib
import platform
import shutil
import subprocess
import sys
import sysconfig
import tempfile

ENGINES = ("compiled", "export", "modelx")
LOOPS = ("net_cf", "result_cf")
TARGET_POINTS = {"compiled": 6000, "export": 600, "modelx": 120}
CHECK_RTOL = 1e-9
VERSIONS = ("modelx", "modelx-cython", "Cython", "numpy", "pandas")

# The child process of one run.  It prints one line of JSON, which the parent reads.
CHILD = r'''
import gc, importlib, importlib.machinery, json, os, sys, time
block, name, engine, loop, collect, data_cells = sys.argv[1:7]
collect, data_cells = collect == "1", json.loads(data_cells)


def peak_mb():
    """The peak resident set of this process so far, in MB, or None."""
    try:
        import resource
    except ImportError:
        try:
            import psutil
        except ImportError:
            return None
        return psutil.Process().memory_info().peak_wset / 2**20
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return peak / 2**20 if sys.platform == "darwin" else peak / 2**10


load = os.getloadavg()[0] if hasattr(os, "getloadavg") else None
sys.path.insert(0, block)
if engine == "modelx":
    import modelx as mx
    model = mx.read_model(os.path.join(block, name), name=f"bench_{os.getpid()}")
else:
    # The export raises no recursion limit, as modelx does (the plan's F7); a cold call
    # can need more than the default, though the loops below run in ascending t.
    sys.setrecursionlimit(10_000)
    package = name + ("_nomx_cy" if engine == "compiled" else "_nomx")
    model = importlib.import_module(package).mx_model
    if engine == "compiled":
        module = sys.modules[type(model.Projection).__module__].__file__
        if not module.endswith(tuple(importlib.machinery.EXTENSION_SUFFIXES)):
            sys.exit(f"{package} imported {module}, not an extension module")
data = model.Data
start = time.perf_counter()
for cell in data_cells:
    getattr(data, cell)()
data_s = time.perf_counter() - start
n = len(data.model_point_table())
projection = model.Projection


def drop(i):
    """run_sec.py's release: the ItemSpace deleted, then a full collection."""
    del projection[i]
    if collect:
        gc.collect()


start = time.perf_counter()
gc.freeze()
for i in range(n):
    projection[i].proj_len()
    drop(i)
gc.freeze()
frames_s = time.perf_counter() - start
before = peak_mb()
total = 0.0
start = time.perf_counter()
for i in range(n):
    p = projection[i]
    if loop == "net_cf":
        s = 0.0
        for t in range(p.proj_len()):
            s += p.net_cf(t)
    else:
        s = float(p.result_cf()["net_cf"].sum())
    total += s
    del p
    drop(i)
loop_s = time.perf_counter() - start
after = peak_mb()
print(json.dumps({"points": n, "data_s": data_s, "frames_s": frames_s, "loop_s": loop_s,
                  "total": total, "peak_mb": after, "load": load,
                  "growth_mb": None if after is None else after - before,
                  "struct_bytes": type(projection).__basicsize__}))
'''


def _build_tool():
    """``tools/build_sec_cy.py``, beside this script, as a module."""
    spec = importlib.util.spec_from_file_location(
        "build_sec_cy", pathlib.Path(__file__).with_name("build_sec_cy.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def describe_model(model_dir):
    """``(model point file, Data cells taking no parameter)``, read from the model.

    The model is read once, under a name of its own, and closed.
    """
    import modelx as mx
    model = mx.read_model(model_dir, name=f"bench_describe_{os.getpid()}")
    try:
        data = model.Data
        cells = [name for name, cell in data.cells.items() if not cell.parameters]
        return data.model_point_file, cells
    finally:
        model.close()


def read_table(path):
    """The model point table's header and rows, as text, exactly as committed."""
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    if not rows or "point_id" not in rows[0]:
        raise ValueError(f"{path} has no point_id column")
    return rows[0], rows[1:]


def block_text(header, rows, copies):
    """The table repeated ``copies`` times, ``point_id`` renumbered from 1 and every other
    cell's text as it is."""
    col = header.index("point_id")
    out = io.StringIO()
    writer = csv.writer(out, lineterminator="\n")
    writer.writerow(header)
    label = 0
    for _ in range(copies):
        for row in rows:
            label += 1
            writer.writerow([str(label) if j == col else v for j, v in enumerate(row)])
    return out.getvalue()


def companions(product_dir, table_file):
    """The product's SEC companion files keyed by ``point_id``, which a block repeats with
    the model point table."""
    found = []
    for path in sorted(product_dir.glob("*_sec.csv")):
        if path.name == table_file:
            continue
        with open(path, newline="", encoding="utf-8") as f:
            header = next(csv.reader(f), [])
        if "point_id" in header:
            found.append(path)
    return found


def companion_text(path, header, rows, copies):
    """The companion at ``path`` repeated ``copies`` times as :func:`block_text` repeats
    the table, ``header`` and ``rows``: in each copy, each of its rows in its own order,
    under the label :func:`block_text` gives its point in that copy, the point's position
    in the table, from 1, plus the rows of the copies before; every other cell's text as it
    is.  A label is matched by value, so that ``3.0`` is point 3, and one the table lacks
    is refused, naming it, rather than timed.
    """
    col = header.index("point_id")
    position = {}
    for i, row in enumerate(rows):
        position[float(row[col])] = i
    with open(path, newline="", encoding="utf-8") as f:
        table = list(csv.reader(f))
    own = table[0].index("point_id")
    missing = sorted({row[own] for row in table[1:] if float(row[own]) not in position})
    if missing:
        raise ValueError(f"{path.name}: point_id {missing} is no point of the table")
    out = io.StringIO()
    writer = csv.writer(out, lineterminator="\n")
    writer.writerow(table[0])
    for copy in range(copies):
        for row in table[1:]:
            label = copy * len(rows) + position[float(row[own])] + 1
            writer.writerow([str(label) if j == own else v for j, v in enumerate(row)])
    return out.getvalue()


def make_block(dest, product_dir, model_dir, build_out, name, table_file, header, rows,
               copies):
    """A block directory: the CSVs, the repeated table, the model and both packages."""
    dest.mkdir(parents=True)
    for path in sorted(product_dir.glob("*.csv")):
        shutil.copy2(path, dest / path.name)
    (dest / table_file).write_text(block_text(header, rows, copies), encoding="utf-8")
    for path in companions(product_dir, table_file):
        (dest / path.name).write_text(companion_text(path, header, rows, copies),
                                      encoding="utf-8")
    skip = shutil.ignore_patterns("__pycache__", "*.c", "*.html")
    shutil.copytree(model_dir, dest / name, ignore=skip)
    for package in (f"{name}_nomx", f"{name}_nomx_cy"):
        shutil.copytree(build_out / package, dest / package, ignore=skip)


def run(block, name, engine, loop, collect, data_cells):
    """One run in a fresh child process: what it reports, or exit naming the failure."""
    done = subprocess.run(
        [sys.executable, "-P", "-c", CHILD, str(block), name, engine, loop,
         "1" if collect else "0", json.dumps(data_cells)],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    if done.returncode:
        sys.exit(f"the {engine} run of {loop} failed with exit code {done.returncode}:\n"
                 f"{done.stderr[-4000:]}")
    return json.loads(done.stdout.strip().splitlines()[-1])


def cpu_model():
    """The processor's name, where the platform says it."""
    try:
        with open("/proc/cpuinfo", encoding="utf-8") as f:
            for line in f:
                if line.startswith("model name"):
                    return line.split(":", 1)[1].strip()
    except OSError:
        pass
    return platform.processor() or "unknown processor"


def compiler():
    """The C compiler setuptools builds an extension with, and its version line."""
    command = os.environ.get("CC") or sysconfig.get_config_var("CC")
    if not command:
        return f"the platform's default (Python built with {platform.python_compiler()})"
    try:
        done = subprocess.run([command.split()[0], "--version"], capture_output=True,
                              text=True, timeout=30)
        first = done.stdout.splitlines()[0] if done.stdout else command
    except (OSError, subprocess.SubprocessError):
        first = command
    return first


def version(dist):
    try:
        return importlib.metadata.version(dist)
    except importlib.metadata.PackageNotFoundError:
        return "not installed"


def loadavg():
    """The 1, 5 and 15 minute load averages, where the platform has them."""
    return os.getloadavg() if hasattr(os, "getloadavg") else None


def _load_text(load):
    return ", ".join(f"{x:.2f}" for x in load) if load is not None else "unknown"


def _per_point(seconds, points):
    return f"{1000 * seconds / points:.3g} ms"


def report(name, results, engines, loops, copies, argv, collect, loads):
    """The Markdown table and the lines around it, as one string."""
    runs = [r for key in results for r in results[key]]
    repeat = len(results[(engines[0], loops[0])])
    lines = [
        f"{name}, {datetime.date.today().isoformat()}: {os.cpu_count()} CPUs, "
        f"{cpu_model()}; {platform.platform()}; Python {platform.python_version()}; "
        f"{compiler()}.",
        ", ".join(f"{d} {version(d)}" for d in VERSIONS) + ".",
    ]
    starts = [r["load"] for r in runs if r["load"] is not None]
    if starts:
        lines.append(f"Load average (1, 5, 15 minutes) {_load_text(loads[0])} before the "
                     f"runs and {_load_text(loads[1])} after; the 1-minute load was "
                     f"{min(starts):.2f} to {max(starts):.2f} as each run started.")
    lines.append(f"Each time is the fastest of {repeat} run{'s' * (repeat > 1)}, each in a "
                 f"process of its own; the spread is the loop's, in seconds"
                 f"{'' if collect else '; WITHOUT the collection after each release'}.")
    lines.append("")
    head = ["engine", "points"] + [f"`{loop}`, a point" for loop in loops]
    head += ["`Data`, s", "frames, s", "peak RSS, MB", "growth in the loop, MB"]
    lines.append("| " + " | ".join(head) + " |")
    lines.append("|" + "---|" * len(head))
    for engine in engines:
        mine = [r for loop in loops for r in results[(engine, loop)]]
        points = mine[0]["points"]
        row = [engine, f"{points:,}"]
        for loop in loops:
            times = [r["loop_s"] for r in results[(engine, loop)]]
            row.append(f"{_per_point(min(times), points)} "
                       f"({min(times):.2f}-{max(times):.2f})")
        row.append(f"{min(r['data_s'] for r in mine):.3f}")
        row.append(f"{min(r['frames_s'] for r in mine):.2f}")
        peaks = [r["peak_mb"] for r in mine if r["peak_mb"] is not None]
        growth = [r["growth_mb"] for r in mine if r["growth_mb"] is not None]
        row.append(f"{max(peaks):.0f}" if peaks else "unknown")
        row.append(f"{max(growth):.1f}" if growth else "unknown")
        lines.append("| " + " | ".join(row) + " |")
    lines.append("")
    best = {(e, loop): min(r["loop_s"] for r in results[(e, loop)])
            / results[(e, loop)][0]["points"] for e in engines for loop in loops}
    pairs = (("compiled", "export"), ("compiled", "modelx"), ("export", "modelx"))
    for fast, slow in pairs:
        if fast in engines and slow in engines:
            ratios = " and ".join(f"{best[(slow, loop)] / best[(fast, loop)]:.1f} on "
                                  f"`{loop}`" for loop in loops)
            lines.append(f"- {fast} against {slow}, a point: {ratios}.")
    if "compiled" in engines:
        size = results[("compiled", loops[0])][0]["struct_bytes"]
        lines.append(f"- A compiled `Projection` ItemSpace's C struct is {size:,} bytes.")
    first = results[(engines[0], loops[0])][0]
    lines.append(f"- `net_cf` summed over a copy of the table: "
                 f"{first['total'] / copies[engines[0]]:.10g}, on every engine, loop and "
                 f"run, to {CHECK_RTOL:g} relative.")
    lines.append("")
    lines.append("    python tools/bench_sec_cy.py " + " ".join(argv))
    return "\n".join(lines)


def main(argv):
    parser = argparse.ArgumentParser(
        prog="python tools/bench_sec_cy.py",
        description="Time a compiled uslib SEC model against its export and modelx "
                    "(USLIB-SEC-PLAN.md C6).")
    parser.add_argument(
        "product", help="a product directory, or the folder name of a uslib product")
    parser.add_argument(
        "--model", help="the model folder to time (default: the product's *_SEC model)")
    parser.add_argument(
        "--build", help="a directory tools/build_sec_cy.py built the model in, with --out "
                        "(default: build into a temporary directory)")
    for engine in ENGINES:
        flag = "--copies" if engine == "compiled" else f"--{engine}-copies"
        parser.add_argument(
            flag, type=int, dest=f"{engine}_copies",
            help=f"copies of the table in the {engine} block (default: about "
                 f"{TARGET_POINTS[engine]:,} points)")
    parser.add_argument("--repeat", type=int, default=3, help="runs of each (default: 3)")
    parser.add_argument("--engines", default=",".join(ENGINES),
                        help=f"a comma-separated subset of {', '.join(ENGINES)}")
    parser.add_argument("--loops", default=",".join(LOOPS),
                        help=f"a comma-separated subset of {', '.join(LOOPS)}")
    parser.add_argument("--no-collect", dest="collect", action="store_false",
                        help="delete each ItemSpace without collecting it, to show what "
                             "the collection saves")
    parser.add_argument("--json", help="also write every run's measurements to this file")
    args = parser.parse_args(argv)
    engines = [e for e in ENGINES if e in args.engines.split(",")]
    loops = [loop for loop in LOOPS if loop in args.loops.split(",")]
    if not engines or not loops or args.repeat < 1:
        parser.error("name at least one engine and one loop, and repeat at least once")
    for engine in engines:
        given = getattr(args, f"{engine}_copies")
        if given is not None and given < 1:
            parser.error("copies must be 1 or more")

    tool = _build_tool()
    product = tool.product_directory(args.product)
    if product is None:
        parser.error(f"{args.product!r} is neither a directory nor a uslib product")
    product = product.resolve()
    try:
        model_dir = tool.find_model(product, args.model).resolve()
    except (FileNotFoundError, ValueError) as err:
        print(err, file=sys.stderr)
        return 2
    name = model_dir.name
    if args.build is None:
        try:
            tool.settle(product, model=name)
        except (ModuleNotFoundError, FileNotFoundError, ValueError) as err:
            print(err, file=sys.stderr)
            return 2
    else:
        build_out = pathlib.Path(args.build).resolve()
        missing = [p for p in (f"{name}_nomx", f"{name}_nomx_cy")
                   if not (build_out / p).is_dir()]
        if missing:
            print(f"{build_out} holds no {' or '.join(missing)}: build there with "
                  f"python tools/build_sec_cy.py {args.product} --out {build_out}",
                  file=sys.stderr)
            return 2
        sources = [*model_dir.rglob("*.py"), product / tool.SAMPLE, product / tool.SPEC]
        modules = [path for path in (build_out / f"{name}_nomx_cy").iterdir()
                   if path.name.endswith(tuple(importlib.machinery.EXTENSION_SUFFIXES))]
        built = min((path.stat().st_mtime for path in modules), default=0)
        newer = [str(path.relative_to(product)) for path in sources
                 if path.is_file() and path.stat().st_mtime > built]
        if newer:
            print(f"warning: {', '.join(newer)} changed after the build in {build_out}, "
                  f"so the export and the compiled model may not be the model's",
                  file=sys.stderr)
    table_file, data_cells = describe_model(model_dir)
    try:
        header, rows = read_table(product / table_file)
        for path in companions(product, table_file):
            companion_text(path, header, rows, 1)
    except ValueError as err:
        print(err, file=sys.stderr)
        return 2
    copies = {e: getattr(args, f"{e}_copies") or math.ceil(TARGET_POINTS[e] / len(rows))
              for e in engines}

    work = pathlib.Path(tempfile.mkdtemp(prefix="bench_sec_cy_"))
    try:
        if args.build is None:
            print(f"building {name} in {work / 'build'}, which takes a minute or more",
                  file=sys.stderr)
            try:
                tool.build(product, model=name, out=work / "build")
            except tool.BuildError as err:
                print(err, file=sys.stderr)
                return 1
            build_out = work / "build"
        blocks = {}
        for engine in engines:
            blocks[engine] = work / f"block_{engine}"
            make_block(blocks[engine], product, model_dir, build_out, name, table_file,
                       header, rows, copies[engine])
        before = loadavg()
        results = {(e, loop): [] for e in engines for loop in loops}
        for i in range(args.repeat):
            for engine in engines:
                for loop in loops:
                    print(f"run {i + 1} of {args.repeat}: {engine}, {loop}, "
                          f"{copies[engine] * len(rows):,} points", file=sys.stderr)
                    results[(engine, loop)].append(
                        run(blocks[engine], name, engine, loop, args.collect, data_cells))
        after = loadavg()
    finally:
        shutil.rmtree(work, ignore_errors=True)

    if args.json:
        pathlib.Path(args.json).write_text(json.dumps(
            {f"{e} {loop}": runs for (e, loop), runs in results.items()}, indent=1))
    first = results[(engines[0], loops[0])][0]["total"] / copies[engines[0]]
    off = [(key, r["total"] / copies[key[0]]) for key, runs in results.items()
           for r in runs
           if abs(r["total"] / copies[key[0]] - first)
           > CHECK_RTOL * max(abs(first), abs(r["total"] / copies[key[0]]))]
    for (engine, loop), value in off:
        print(f"{engine}, {loop}: net_cf summed over a copy of the table is {value!r}, not "
              f"{first!r} as in the first run", file=sys.stderr)
    if off:
        return 1
    print(report(name, results, engines, loops, copies, argv, args.collect,
                 (before, after)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
