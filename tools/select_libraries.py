"""Select the libraries a pull request reaches, for the ``changes`` job of CI's ``Tests``.

CI's gate is a bare ``pytest`` from the repository root, every library's suite collected in
one process, as lifelib's CI will run them, and uslib's and uklib's SEC models have jobs of
their own, ``cython`` and ``sec``, ``cython_uk`` and ``sec_uk``
(``.github/workflows/tests.yml``): more than a hundred jobs in all.  A pull request that
changes one library needs none of the others' tests, so this reads the paths it changes and
names the libraries they reach.  The ``test`` job then collects every library as before and
deselects the tests of the rest, and an SEC library's own jobs run only where it is named.
A push to ``main`` and a manual run ask nothing of this: they run everything.

**What a path reaches** (:func:`reaches`).

* A path in a library's folder, ``lifelib/libraries/<lib>/...``, reaches that library: its
  suite reads the library's models, their inputs, its documents and its tests.
* A file of one library that another library's suite reads reaches that one too, as
  :data:`READ_BY` lists them: uklib's suite holds its ``build_sec_cy.py`` to uslib's, byte
  for byte.  uslib's ``sec_support.py`` is held to uklib's copy by the ``test`` job's step
  ``python tools/check_sec_harness.py``, which runs on every leg of the job, whatever is
  selected, so it needs no entry.
* A path that no test reads and no job runs reaches no library (:func:`inert`): the
  documentation under ``doc/``, which ``tools/doccheck.py`` checks outside CI; the markdown
  at the root, the plans among it, which tests cite and none opens; and ``.gitignore``.
* Every other path reaches every library.  The workflow is read by uslib's and uklib's
  suites, ``tools/`` is loaded by them, the requirements are every job's environment, and
  ``.gitattributes`` decides what a Windows checkout reads; and a path not placed here, a
  folder new to the repository or a file beside the libraries, is taken to reach them all
  until it is.

A library the change reaches that the checkout does not hold, as when the change removes
it, selects every library: there is nothing of it to run, and the rest run rather than
none.

Usage::

    python tools/select_libraries.py <revision>...

The revisions are ``git diff``'s, and name the change: the workflow passes ``HEAD^1 HEAD``,
the pull request's merge commit and its first parent, the tip of the branch it merges into;
from a working copy, ``origin/main...HEAD`` gives what the branch has changed since it left
``main``.  It prints which libraries the change reaches and why, and writes the outputs the
workflow reads to the file ``$GITHUB_OUTPUT`` names, or prints them where it names none:

``libraries``
    The libraries reached, their folder names in order, space-separated; empty for none.
``deselect``
    ``--deselect lifelib/libraries/<lib>/`` for each library of the checkout not reached,
    for the ``test`` job's ``pytest``; empty where every library is reached.
``uslib``, ``uklib``
    ``true`` where the change reaches the library, and ``false`` where it does not: the
    ``cython`` and ``sec`` jobs run on uslib's, ``cython_uk`` and ``sec_uk`` on uklib's.

It writes the same account as markdown to the file ``$GITHUB_STEP_SUMMARY`` names, where
one is.  It exits 0 with a selection, and 2 where it is given no revision, git cannot give
the change, or the checkout holds no library.  It needs the standard library alone.  The
examples in :func:`reaches` are its tests, ``python -m doctest tools/select_libraries.py``,
which the ``changes`` job runs before it selects.
"""
import dataclasses
import os
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

# The folder of the libraries, as git names it: relative to the root, with forward slashes.
LIBRARIES = "lifelib/libraries/"

# A library's folder name.  The names reach the test job's command line, so a folder named
# otherwise is no library here, and a path in one reaches every library.
NAME = re.compile(r"[a-z][a-z0-9_]*")

# The files of one library that another library's suite reads, each with the libraries
# that read it.  A change to one reaches its own library and these.
READ_BY = {
    # uklib's test_the_build_tool_is_uslib_s_byte_for_byte, test_compiled_conventions_uk.py.
    "lifelib/libraries/uslib/build_sec_cy.py": ("uklib",),
}

# The libraries with jobs of their own beside the test job, which run where the change
# reaches the library: each is an output, true or false.
GATED = ("uslib", "uklib")


class Every:
    """What :func:`reaches` gives for a path that reaches every library."""

    def __repr__(self):
        return "EVERY"


EVERY = Every()


def inert(path):
    """Whether no test reads ``path`` and no job runs it: it is under ``doc/``, or it is
    markdown or ``.gitignore`` at the root."""
    top, _, rest = path.partition("/")
    if rest:
        return top == "doc"
    return path.endswith(".md") or path == ".gitignore"


def reaches(path):
    """The libraries a change to ``path`` reaches: a tuple of their names, empty for none,
    or :data:`EVERY`.

    A library's own path reaches it, and the libraries :data:`READ_BY` gives:

    >>> reaches("lifelib/libraries/jplib/products/term_life/model_point_table.csv")
    ('jplib',)
    >>> reaches("lifelib/libraries/uklib/tests/uk_sec_support.py")
    ('uklib',)
    >>> reaches("lifelib/libraries/uslib/build_sec_cy.py")
    ('uslib', 'uklib')

    The documents no test reads reach none:

    >>> reaches("doc/source/libraries/jplib/products/term_life/model.md")
    ()
    >>> reaches("USLIB-SEC-PLAN.md"), reaches(".gitignore")
    ((), ())

    Anything else reaches every library: the workflow, the tools, the requirements, a file
    beside the libraries rather than in one, a folder not named as a library is, and what
    is new:

    >>> reaches(".github/workflows/tests.yml"), reaches("tools/check_sec_harness.py")
    (EVERY, EVERY)
    >>> reaches("requirements.txt"), reaches(".gitattributes")
    (EVERY, EVERY)
    >>> reaches("lifelib/libraries/conftest.py"), reaches("lifelib/libraries/Draft lib/x.py")
    (EVERY, EVERY)
    >>> reaches("lifelib/README.md"), reaches("benchmarks/run.py")
    (EVERY, EVERY)
    """
    if path.startswith(LIBRARIES):
        name, _, rest = path[len(LIBRARIES):].partition("/")
        if rest and NAME.fullmatch(name):
            return (name,) + READ_BY.get(path, ())
        return EVERY
    if inert(path):
        return ()
    return EVERY


@dataclasses.dataclass
class Selection:
    """What a change reaches: the libraries ``selected``, in the checkout's order; the paths
    that reach ``every`` library and those that reach ``none``; the paths that reach each
    library, ``reached``; and the libraries reached that the checkout does not hold,
    ``gone``."""
    selected: list
    every: list
    none: list
    reached: dict
    gone: list


def select(paths, present):
    """The :class:`Selection` a change to ``paths`` makes, in a checkout whose libraries
    are ``present``, in order."""
    every, none, reached = [], [], {}
    for path in paths:
        found = reaches(path)
        if found is EVERY:
            every.append(path)
            continue
        if not found:
            none.append(path)
        for name in found:
            reached.setdefault(name, []).append(path)
    gone = [name for name in reached if name not in present]
    if every or gone:
        selected = list(present)
    else:
        selected = [name for name in present if name in reached]
    return Selection(selected, every, none, reached, gone)


def libraries():
    """The libraries of the checkout: the folders of ``lifelib/libraries/`` named as a
    library is, in order."""
    folder = ROOT / LIBRARIES
    return sorted(path.name for path in folder.iterdir()
                  if path.is_dir() and NAME.fullmatch(path.name))


def outputs(selection, present):
    """The outputs the workflow reads, ``{name: value}``."""
    found = {
        "libraries": " ".join(selection.selected),
        "deselect": " ".join(f"--deselect {LIBRARIES}{name}/" for name in present
                             if name not in selection.selected),
    }
    found.update({name: str(name in selection.selected).lower() for name in GATED})
    return found


def _some(paths, shown=5):
    """Up to ``shown`` of ``paths``, and how many more."""
    text = ", ".join(paths[:shown])
    more = len(paths) - shown
    return f"{text} and {more} more" if more > 0 else text


def account(selection, present):
    """Lines saying what the change reaches and why, and what CI runs of it."""
    lines = []
    if selection.every:
        lines.append(f"Every library is reached by {_some(selection.every)}.")
    for name, paths in sorted(selection.reached.items()):
        lines.append(f"{name} is reached by {_some(paths)}.")
    if selection.gone:
        lines.append(f"The checkout does not hold {', '.join(sorted(selection.gone))}, so "
                     f"every library is selected.")
    if selection.none:
        lines.append(f"No library is reached by {_some(selection.none)}: no test reads "
                     f"them.")
    rest = [name for name in present if name not in selection.selected]
    lines.append(f"Selected: {' '.join(selection.selected) or 'no library'}.")
    if selection.selected and rest:
        lines.append(f"The test job deselects {' '.join(rest)}.")
    for name in GATED:
        runs = "run" if name in selection.selected else "do not run"
        lines.append(f"{name}'s own jobs {runs}.")
    return lines


def main(argv):
    if not argv or any(arg.startswith("-") for arg in argv):
        print("usage: python tools/select_libraries.py <revision>...", file=sys.stderr)
        return 2
    done = subprocess.run(
        ["git", "diff", "-z", "--name-only", "--no-renames", "--no-relative", *argv, "--"],
        cwd=ROOT, capture_output=True)
    if done.returncode:
        error = done.stderr.decode(errors="replace").strip()
        print(f"select_libraries: git diff {' '.join(argv)} failed: {error}",
              file=sys.stderr)
        return 2
    paths = [path for path in done.stdout.decode(errors="surrogateescape").split("\0")
             if path]
    present = libraries()
    if not present:
        print(f"select_libraries: {LIBRARIES} holds no library", file=sys.stderr)
        return 2
    selection = select(paths, present)
    lines = account(selection, present)
    print(f"{len(paths)} {'path' if len(paths) == 1 else 'paths'} changed in "
          f"{' '.join(argv)}.")
    print("\n".join(lines))
    values = [f"{key}={value}" for key, value in outputs(selection, present).items()]
    target = os.environ.get("GITHUB_OUTPUT")
    if target:
        with open(target, "a", encoding="utf-8") as stream:
            stream.write("\n".join(values) + "\n")
    else:
        print("\n".join(values))
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as stream:
            stream.write("### The libraries this pull request reaches\n\n"
                         + "".join(f"- {line}\n" for line in lines))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
