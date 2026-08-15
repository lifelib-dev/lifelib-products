"""Build the country library's documents exactly as lifelib will, and fail on any warning.

lifelib has one Sphinx source directory, and these documents live in the library rather
than under ``doc/``, so the real build mirrors ``<lib>/**/*.md`` into the doc tree at
``builder-inited`` (USLIB-MERGE-PLAN.md D3).  This reproduces that here -- same mirror,
same MyST settings, same autodoc configuration -- so the set can be brought to
warning-clean *before* the merge rather than after.

**``-n`` is not optional.** Sphinx does not warn about an unresolved ``:func:``/``:mod:``
by default; it drops the role and renders plain text.  Since the entire point of this work
is that cross-references are links, a build without nitpicky mode cannot tell us whether it
succeeded (D9).

``_research/`` is excluded, matching D6.

Usage::

    python tools/doccheck.py uslib
    python tools/doccheck.py uslib --keep      # leave the build tree for inspection
"""
import os
import shutil
import subprocess
import sys
import pathlib


CONF = '''\
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "pkg")))

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.mathjax",
    "myst_parser",
]
source_suffix = ".rst"
master_doc = "index"
project = "{lib}"
add_module_names = False
autodoc_member_order = "bysource"
# Mirrors lifelib: MyST extensions are off, so currency like $100,000 is not maths.
myst_enable_extensions = []
exclude_patterns = ["_build", "_research/**"]
nitpicky = True
html_theme = "basic"
'''

ROOT_INDEX = '''\
{lib}
{underline}

.. toctree::
   :glob:
   :maxdepth: 2

   */index
   **
'''


def mirror(library, dest):
    """Copy the library's markdown into the build source tree, as D3's hook does."""
    copied = 0
    for src in library.rglob("*.md"):
        if "_research" in src.parts:
            continue
        target = dest / src.relative_to(library)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, target)
        copied += 1
    return copied


def main(argv):
    args = [a for a in argv if not a.startswith("-")]
    library = pathlib.Path(args[0] if args else "uslib")
    # The directory *is* the library: uslib/ here, lifelib/libraries/uslib/ after the
    # merge, and uklib/ when the UK section follows.  Deriving the name any other way
    # would make the anchors and module paths disagree with where the files actually are.
    lib = library.name

    build = pathlib.Path(".doccheck")
    # autodoc imports the models, which leaves __pycache__ behind; on Windows those can
    # still be held when the next run starts, so removal must not be fatal.
    for _ in range(3):
        shutil.rmtree(build, ignore_errors=True)
        if not build.exists():
            break
    src = build / "src"
    src.mkdir(parents=True, exist_ok=True)

    # autodoc imports the models, and importing writes __pycache__ into the model
    # folders, so it works on a copy rather than the source tree.  The directory name
    # is already the package name, so this is a copy and not a rename.
    pkg = build / "pkg" / lib
    pkg.parent.mkdir(parents=True, exist_ok=True)
    if pkg.exists():
        shutil.rmtree(pkg, ignore_errors=True)
    shutil.copytree(library, pkg, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("__pycache__", "_research", "tests"))

    copied = mirror(library, src)
    (src / "conf.py").write_text(CONF.format(lib=lib), encoding="utf-8")
    if not (src / "index.md").exists():
        (src / "index.rst").write_text(
            ROOT_INDEX.format(lib=lib, underline="=" * len(lib)), encoding="utf-8")

    print(f"mirrored {copied} documents; building with -n -W --keep-going\n")
    result = subprocess.run(
        [sys.executable, "-m", "sphinx", "-b", "html", "-n", "-W", "--keep-going",
         str(src), str(build / "html")],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        env={**os.environ, "PYTHONIOENCODING": "utf-8"})

    lines = [ln for ln in (result.stdout + result.stderr).splitlines()
             if "WARNING" in ln or "ERROR" in ln]
    for ln in lines[:60]:
        print(ln.replace(str(src.resolve()), "<src>"))
    if len(lines) > 60:
        print(f"... and {len(lines) - 60} more")
    print(f"\n{len(lines)} warnings/errors")

    if "--keep" not in argv:
        shutil.rmtree(build, ignore_errors=True)
    return 1 if lines else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
