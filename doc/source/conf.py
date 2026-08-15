"""Sphinx configuration for the country libraries.

This is deliberately close to the configuration these documents will land in.  lifelib's
``doc/source/conf.py`` already loads ``myst_parser``, ``autodoc``, ``autosummary`` and
``napoleon``, already sets ``autodoc_member_order = 'bysource'``, and already puts the
directory holding the libraries on ``sys.path``.  Everything below either mirrors that or is
the one addition the merge needs -- the ``builder-inited`` hook that mirrors each library's
markdown into the doc tree (USLIB-MERGE-PLAN.md D3, MERGE.md step 4).

The only structural difference is where the libraries live.  Here they are top-level
directories (``uslib/``, and ``uklib/`` when it exists); in lifelib they are under
``lifelib/libraries/``.  That is one path in :data:`LIBRARY_ROOT`.

Build it::

    cd doc && make html

or, to fail on anything that would render wrong::

    python tools/doccheck.py uslib
"""
import os
import shutil
import sys
from pathlib import Path


here = Path(__file__).resolve().parent
REPO = here.parents[1]

# Where the country libraries live.  In lifelib this is `lifelib/libraries`.
LIBRARY_ROOT = REPO

# autodoc imports the models to read their cells docstrings, so the library must be
# importable under the name its documents use: `uslib.products.term_life.Term_US_A`.
# lifelib does the same thing one level down, which is why the product slugs are
# underscored -- every component of that path has to be a Python identifier.
sys.path.insert(0, str(LIBRARY_ROOT))


# -- Project ---------------------------------------------------------------------------

project = "lifelib-products"
copyright = "2026, Fumito Hamamura"
author = "Fumito Hamamura"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.mathjax",
    "sphinx_design",
    "myst_parser",
]

# myst_parser registers `.md` itself; this is the RST half, as in lifelib.
source_suffix = ".rst"
master_doc = "index"

exclude_patterns = [
    "_build",
    # _research/ ships with the library -- it is the evidence behind the documents -- but
    # it is not rendered: it carries its own deliberately independent [S#] numbering, and a
    # second, conflicting S1 in front of a reader is worse than not publishing it (D6).
    "libraries/*/_research/**",
]

# Deliberately empty, matching lifelib.  Enabling `dollarmath` would read the corpus's
# currency -- $100,000, $1,000 -- as maths (C12).
myst_enable_extensions = []

add_module_names = False
autodoc_member_order = "bysource"
autosummary_generate = True

# Off by default; `tools/doccheck.py` turns it on with -n.  It must be on for any build
# that claims the cross-references work, because Sphinx does not warn about an unresolved
# :func:/:mod: role -- it drops the role and renders plain text (D9).
nitpicky = False


# -- HTML ------------------------------------------------------------------------------

html_theme = "pydata_sphinx_theme"
html_static_path = ["_static"]
html_title = "lifelib-products"
html_last_updated_fmt = "%b %d, %Y"
html_theme_options = {
    "header_links_before_dropdown": 6,
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/fumitoh/lifelib-products",
            "icon": "fab fa-github-square",
        }
    ],
}


# -- Mirror the library-resident documents ---------------------------------------------

def _sync_library_docs(app):
    """Mirror ``<library>/**/*.md`` into the doc tree.

    Sphinx has a single source directory, and these documents live beside the models they
    describe rather than under ``doc/``.  Any library with an ``index.md`` opts in, so
    adding a second country library needs no change here.

    Only ``*.md`` is copied -- never the CSVs, ``run.py``, the model folders or ``tests/``.
    The mtime guard keeps incremental rebuilds working; copying unconditionally would
    re-render every page on every run.
    """
    for library in sorted(p for p in LIBRARY_ROOT.iterdir() if p.is_dir()):
        if not (library / "index.md").exists():
            continue
        dest = here / "libraries" / library.name
        for src in library.rglob("*.md"):
            target = dest / src.relative_to(library)
            if not target.exists() or src.stat().st_mtime > target.stat().st_mtime:
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, target)
        for target in list(dest.rglob("*.md")):
            if not (library / target.relative_to(dest)).exists():
                target.unlink()          # the source document was deleted or renamed


def setup(app):
    app.connect("builder-inited", _sync_library_docs)
