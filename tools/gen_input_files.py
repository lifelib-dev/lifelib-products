"""Regenerate a library test registry's ``INPUT_FILES`` map from a real sweep.

``INPUT_FILES`` records, per model, the exact set of input files a full sweep of the
shipped model point table reads.  The conventions suite asserts that set rather than
merely asserting that whatever was read was read once, because counting only the files
that happen to be read makes the check self-fulfilling: a file that stops being read drops
out of the counter, and the read-once assertion then passes over *less* coverage rather
than failing.

That makes the map load-bearing, and hand-transcribing a load-bearing map is how it goes
stale.  This tool produces it the only way that is honest -- by reading each model,
projecting every model point, and recording the file names ``pandas.read_csv`` was
actually handed out of the model's own input directory.

It prints the literal to paste into the registry, and with ``--write`` it splices it in
place between the ``INPUT_FILES = {`` line and its closing brace.  The map stays
**committed** either way: an expectation computed at run time asserts nothing at all.

Usage::

    python tools/gen_input_files.py lifelib/libraries/delib
    python tools/gen_input_files.py lifelib/libraries/delib --write

The registry module is found as ``<library>/tests/<cc>_registry.py``, where ``cc`` is the
last two letters of the library name -- ``delib`` -> ``de_registry.py``, ``frlib`` ->
``fr_registry.py``.
"""
import importlib.util
import pathlib
import re
import sys
from collections import Counter


def load_registry(library):
    """Import the library's own test registry module by path."""
    cc = library.name.removesuffix("lib")
    path = library / "tests" / f"{cc}_registry.py"
    if not path.is_file():
        sys.exit(f"no registry at {path}")
    spec = importlib.util.spec_from_file_location(f"{cc}_registry", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module, path


def files_read(registry, name):
    """Every input file the model reads over a full sweep of its model point table.

    The counting window is opened *before* ``read_model``, so it spans the model's whole
    life and catches the reads its formulas trigger, not only the ones the reader cells
    make on the way in.  The log is filtered to the model's own input directory, so a
    reader that reaches outside it is visible as an absence rather than being miscounted.

    **The sweep here must be the sweep the conventions suite performs, not a subset of
    it.**  ``test_every_model_point_projects`` calls ``result_cf()`` *and* every
    ``check_*()`` cells on every model point, and a check can reach an input the cash flow
    statement never touches -- ``KLV_DE_A``'s ``deckrv_table.csv``, read by the reserve
    check and by nothing in ``result_cf()``, is the case that found this.  A generator that
    projected the frame alone under-recorded the set, and the map it wrote then failed the
    very test it exists to feed.  So the checks are called here too.
    """
    import modelx as mx
    import pandas as pd

    reads = []
    original = pd.read_csv

    def counting(*args, **kwargs):
        reads.append(str(args[0]).replace("\\", "/"))
        return original(*args, **kwargs)

    folder = registry.model_path(name)
    pd.read_csv = counting
    try:
        model = mx.read_model(folder, name=f"{name}_inputs")
        try:
            checks = [c for c in model.Projection.cells
                      if c.startswith("check_") and not c.endswith("_resid")]
            for point_id in model.Data.model_point_table().index:
                proj = model.Projection[point_id]
                proj.result_cf()
                for check in checks:
                    getattr(proj, check)()
        finally:
            model.close()
    finally:
        pd.read_csv = original

    parent = str(folder.parent).replace("\\", "/")
    counts = Counter(path.rsplit("/", 1)[-1] for path in reads
                     if path.rsplit("/", 1)[0] == parent)
    repeats = {f: n for f, n in counts.items() if n > 1}
    return set(counts), repeats


def render(mapping):
    """The ``INPUT_FILES`` body, wrapped the way the committed registries are."""
    lines = []
    for name in sorted(mapping):
        files = sorted(mapping[name])
        entry = ", ".join(f'"{f}"' for f in files)
        one_line = f'    "{name}": {{{entry}}},'
        if len(one_line) <= 88:
            lines.append(one_line)
            continue
        lines.append(f'    "{name}": {{')
        current = "       "
        for i, f in enumerate(files):
            piece = f' "{f}"' + ("," if i < len(files) - 1 else "")
            if len(current) + len(piece) > 88:
                lines.append(current)
                current = "       " + piece
            else:
                current += piece
        lines.append(current + "},")
    return "\n".join(lines)


def main(argv):
    args = [a for a in argv if not a.startswith("-")]
    library = pathlib.Path(args[0] if args else "lifelib/libraries/delib").resolve()
    registry, registry_path = load_registry(library)

    mapping, problems = {}, []
    for name in sorted(registry.MODELS):
        files, repeats = files_read(registry, name)
        mapping[name] = files
        if repeats:
            problems.append(f"{name}: read more than once {repeats}")
        print(f"  {name:<14} {len(files)} files: {', '.join(sorted(files))}")

    body = render(mapping)
    if "--write" in argv:
        text = registry_path.read_text(encoding="utf-8")
        pattern = re.compile(r"(?m)^INPUT_FILES = \{\n(?:.*\n)*?\}\n|^INPUT_FILES = \{\}\n")
        if not pattern.search(text):
            sys.exit(f"no INPUT_FILES assignment found in {registry_path}")
        registry_path.write_text(
            pattern.sub("INPUT_FILES = {\n" + body + "\n}\n", text, count=1),
            encoding="utf-8")
        print(f"\nwrote INPUT_FILES for {len(mapping)} models into {registry_path}")
    else:
        print("\nINPUT_FILES = {")
        print(body)
        print("}")

    # A file read twice is the very defect the registered set exists to catch, so it must
    # not be quietly baked into the expectation.
    for problem in problems:
        print(f"\nWARNING  {problem}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
