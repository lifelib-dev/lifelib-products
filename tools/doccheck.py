"""Build the documentation the way it has to survive, and fail on anything at all.

This runs the **real** configuration in ``doc/source/conf.py`` -- the same one that goes to
lifelib -- rather than a copy of its settings, so there is no second place for the two to
drift apart.  What it adds is the strictness a routine ``make html`` does not have:

``-n``
    Nitpicky.  **Not optional.** Sphinx does not warn about an unresolved ``:func:`` or
    ``:mod:`` role by default; it drops the role and renders plain text.  Since the point of
    this library is that every cross-reference is a link, a build without ``-n`` cannot tell
    you whether it worked.  During the prep it was the only thing that revealed 38 silently
    dead references (USLIB-MERGE-PLAN.md D9).

``-W --keep-going``
    Every warning is an error, but the build runs to the end so one pass lists them all.

``-E``
    Read everything fresh.  A cached environment hides warnings from documents Sphinx
    decides it need not re-read, which is exactly the wrong behaviour for a gate.

Usage::

    python tools/doccheck.py              # build and report
    python tools/doccheck.py --keep       # leave doc/build/check for inspection
"""
import collections
import os
import re
import shutil
import subprocess
import sys
import pathlib


REPO = pathlib.Path(__file__).resolve().parents[1]
SOURCE = REPO / "doc" / "source"
BUILD = REPO / "doc" / "build" / "check"


def summarise(output):
    """Group the warnings by kind, since they arrive in file order and repeat."""
    kinds = collections.Counter()
    lines = []
    for line in output.splitlines():
        line = re.sub(r'\x1b\[[0-9;]*m', '', line).strip()
        if "WARNING:" not in line and "ERROR:" not in line:
            continue
        lines.append(line.replace(str(REPO) + os.sep, ""))
        message = re.search(r'(?:WARNING|ERROR): (.*)', line).group(1)
        message = re.sub(r'\s*\[[\w.]+\]\s*$', '', message)
        message = re.sub(r'(not found): \S+', r'\1: ...', message)
        message = re.sub(r"'[^']*'", "'...'", message)
        kinds[message[:70]] += 1
    return lines, kinds


def main(argv):
    if not SOURCE.exists():
        print(f"no Sphinx source at {SOURCE}")
        return 2

    result = subprocess.run(
        [sys.executable, "-m", "sphinx", "-b", "html", "-n", "-W", "--keep-going", "-E",
         str(SOURCE), str(BUILD)],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        env={**os.environ, "PYTHONIOENCODING": "utf-8"})

    lines, kinds = summarise(result.stdout + result.stderr)
    for line in lines[:40]:
        print(line)
    if len(lines) > 40:
        print(f"... and {len(lines) - 40} more")
    if kinds:
        print()
        for kind, n in kinds.most_common():
            print(f"{n:4}  {kind}")

    pages = len(list(BUILD.rglob("*.html"))) if BUILD.exists() else 0
    print(f"\n{pages} pages, {len(lines)} warnings/errors")

    if "--keep" not in argv:
        shutil.rmtree(BUILD, ignore_errors=True)
    # A gate that cannot run must not report success.  With no Sphinx installed the
    # build emits no warnings and writes no pages, and the count above reads
    # "0 pages, 0 warnings" -- the exact silent pass this script exists to prevent
    # elsewhere.  Sphinx is a documentation dependency and is deliberately absent from
    # requirements.txt, which covers the models, so this is a normal thing to hit.
    if not pages:
        print("\nnothing was built, so nothing was checked -- this is not a pass.")
        print(result.stderr.strip()[-500:] or result.stdout.strip()[-500:])
        print("\npip install sphinx myst-parser sphinx-design pydata-sphinx-theme")
        return 2
    return 1 if lines else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
