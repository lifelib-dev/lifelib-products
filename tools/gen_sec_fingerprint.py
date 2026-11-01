"""Freeze an SEC model's Phase 1 fingerprint into its test module, or check it (C2).

USLIB-SEC-PLAN.md's Phase 2 changes how an SEC model is represented and no number it
computes (D2).  So before a product's Phase 2 changes anything, what its Phase 1 model
computes is frozen, in brief and in a form a reviewer can read: for every point of the
committed SEC table, each column of ``result_cf()`` and ``result_pols()``, its sum, its
largest absolute value and its values at five fixed months (§5.4).  C2 then holds every
later version of the model to it, to 1e-12 relative.

The freeze is a literal, ``FINGERPRINT = {...}``, in the product's own test module, between
two marker lines that name the model::

    # BEGIN generated fingerprint: Term_US_SEC -- tools/gen_sec_fingerprint.py
    FINGERPRINT = {}
    # END generated fingerprint: Term_US_SEC

The tool finds the one module of ``lifelib/libraries/uslib/tests`` that holds the model's
markers, and refuses unless exactly one does.  It fills an empty block only.  A freeze is
made once, from the Phase 1 model as committed, and committed alone, so a filled block is
refused unless ``--force`` is given: a refreeze, after an assumption table has changed the
numbers, is a reviewed change of its own, which changes the input and the freeze together
and says why.

This is a thin command line over ``sec_support.fingerprint``, ``fingerprint_text`` and
``fingerprint_mismatches``, which live in the library's tests, as the T6 generator does
(``tools/gen_sec_points.py``), because C2 must run in a ``lifelib.create()`` copy, which
carries ``tests/`` and not this repository's ``tools/``.

Usage::

    python tools/gen_sec_fingerprint.py Term_US_SEC            # freeze into the empty block
    python tools/gen_sec_fingerprint.py Term_US_SEC --check    # C2: does the model match?
    python tools/gen_sec_fingerprint.py Term_US_SEC --force    # refreeze a filled block

``--check`` writes nothing, prints each departure, and exits 1 if there is any.  A model
the registry does not know, markers missing or found in more than one module, a filled
block without ``--force``, or a malformed command line exit 2.
"""
import argparse
import pathlib
import re
import sys

TESTS = pathlib.Path(__file__).resolve().parents[1] / "lifelib/libraries/uslib/tests"
sys.path.insert(0, str(TESTS))

import modelx as mx  # noqa: E402

import sec_support  # noqa: E402  (it is found through the path inserted above)
from us_registry import MODELS, model_path  # noqa: E402


def find_block(name):
    """``(path, text, start, stop)``: the module holding ``name``'s markers, and the span
    from the start of its BEGIN line to the end of its END line, or an error message."""
    begin = re.compile(rf"^# BEGIN generated fingerprint: {re.escape(name)} .*$", re.M)
    end = re.compile(rf"^# END generated fingerprint: {re.escape(name)}\n", re.M)
    found = []
    for path in sorted(TESTS.glob("test_*.py")):
        text = path.read_text(encoding="utf-8")
        b = begin.search(text)
        if b is None:
            continue
        e = end.search(text, b.end())
        if e is None:
            return f"{path.name}: the BEGIN marker for {name} has no END marker after it"
        found.append((path, text, b.start(), e.end()))
    if len(found) != 1:
        where = ", ".join(path.name for path, *_ in found) or "none"
        return (f"{len(found)} test modules in {TESTS} hold {name}'s fingerprint markers "
                f"({where}); exactly one must")
    return found[0]


def main(argv):
    parser = argparse.ArgumentParser(
        prog="python tools/gen_sec_fingerprint.py",
        description="Freeze an SEC model's fingerprint, or check it "
                    "(USLIB-SEC-PLAN.md C2).")
    parser.add_argument("model", help="the SEC model, as us_registry.MODELS names it")
    parser.add_argument("--check", action="store_true",
                        help="compare the model with its frozen fingerprint; write nothing")
    parser.add_argument("--force", action="store_true",
                        help="refreeze a block that already holds a fingerprint")
    args = parser.parse_args(argv)
    if args.model not in MODELS:
        print(f"{args.model!r} is not a model us_registry.MODELS registers")
        return 2
    block = find_block(args.model)
    if isinstance(block, str):
        print(block)
        return 2
    path, text, start, stop = block
    namespace = {}
    exec(text[start:stop], namespace)           # the block between the two marker lines
    frozen = namespace.get("FINGERPRINT")
    if not isinstance(frozen, dict):
        print(f"{path.name}: the block for {args.model} assigns no FINGERPRINT dict")
        return 2
    if frozen and not (args.check or args.force):
        print(f"{path.name} already holds {args.model}'s fingerprint, which is frozen "
              f"once; --force refreezes it, as a reviewed change of its own")
        return 2

    model = mx.read_model(model_path(args.model), name=f"{args.model}_fingerprint")
    try:
        if args.check:
            lines = sec_support.fingerprint_mismatches(frozen, model)
            for line in lines:
                print(line)
            print(f"{args.model}: {len(lines)} departures from its fingerprint" if lines
                  else f"{args.model} reproduces its fingerprint")
            return 1 if lines else 0
        new = sec_support.fingerprint_text(args.model, sec_support.fingerprint(model))
    finally:
        model.close()
    path.write_text(text[:start] + new + text[stop:], encoding="utf-8")
    print(f"froze {args.model}'s fingerprint into {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
