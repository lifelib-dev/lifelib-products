# Merging `uslib/` into lifelib

Everything in this repository is ready. This file is the lifelib-side half: the steps that
cannot be done here because they touch lifelib's own files.

The design decisions behind each step are in [USLIB-MERGE-PLAN.md](USLIB-MERGE-PLAN.md);
this is the checklist, not the argument.

**Status of the prep:** `uslib/` builds to 75 Sphinx pages with **0 warnings** under
`-n -W --keep-going`, and its 1,010 tests pass. Both are reproducible here:

```bash
python tools/doccheck.py uslib
```

```bash
python -m pytest uslib/tests -q
```

---

## 1. Move the directory

```bash
git mv uslib lifelib/libraries/uslib
```

That is the whole move. `uslib/` is already self-contained: the twelve models sit beside the
documents that specify them, the test suite is inside at `uslib/tests/`, and every internal
path reference is either relative or library-root-relative, so nothing inside it names its
own location. The directory is already called `uslib`, so this is a move and not a rename:
the anchors, the `automodule` paths and the package name all say `uslib` today.

`uk/` stays in lifelib-products until it is given the same treatment (see §7).

## 2. `setup.py` — ship the markdown

`get_package_data` lists the extensions that reach an installed copy:

```python
extensions = ['py', 'ipynb', 'xlsx', 'csv', 'json', 'pickle']
```

**Add `'md'`.** Without it the documents are not installed, so `lifelib.create("uslib", …)`
hands the user a library with no documentation — and for this library the documentation is
the point. `.py` and `.csv` are already covered, so the models, their inputs and the tests
travel as they are.

## 3. `setup.py` — raise the modelx floor

```python
install_requires=['modelx>=0.31.0']       # -> 'modelx>=0.32'
```

The twelve models are serialized with modelx serializer v8. modelx 0.31.1 cannot read them;
`read_model` fails outright rather than degrading. This is a hard requirement of the merge,
not a preference.

## 4. `doc/source/conf.py` — mirror the library's markdown into the doc tree

Sphinx has one source directory and these documents live in the library, so the build has to
bring them in. Written to discover libraries rather than name `uslib`, so a second country
library needs no further edit:

```python
import shutil
from pathlib import Path

def _sync_library_docs(app):
    """Mirror <library>/**/*.md into the doc tree.

    Sphinx has a single srcdir, and the country libraries keep their documents beside the
    models they describe.  Any library with an index.md opts in.
    """
    libraries = Path(here).parents[1] / "lifelib" / "libraries"
    for library in sorted(libraries.iterdir()):
        if not (library / "index.md").exists():
            continue
        dest = Path(here) / "libraries" / library.name
        for src in library.rglob("*.md"):
            target = dest / src.relative_to(library)
            if not target.exists() or src.stat().st_mtime > target.stat().st_mtime:
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, target)
        for target in dest.rglob("*.md"):          # prune deletions
            if not (library / target.relative_to(dest)).exists():
                target.unlink()

def setup(app):
    app.add_css_file("custom-style.css")
    app.connect("builder-inited", _sync_library_docs)
```

Only `*.md` is copied — never the CSVs, `run.py`, the model folders or `tests/`. The mtime
guard keeps incremental rebuilds working; a blind `rmtree` + `copytree` would re-render
every page on every run.

Also add:

```python
exclude_patterns += ['libraries/*/_research/**']
```

`_research/` ships with the library — it is the evidence behind the documents — but it is
not rendered: it carries its own deliberately independent `[S#]` numbering, and putting a
second, conflicting `S1` in front of a reader is worse than not publishing it.

**No autodoc configuration is needed.** `sphinx.ext.autodoc`, `autosummary` and `napoleon`
are already loaded, `autodoc_member_order = 'bysource'` is already set, and
`lifelib/libraries` is already on `sys.path` — which is exactly why the models are
importable as `uslib.products.<slug>.<Model>` and why the product slugs were underscored.

**Do not enable `myst_enable_extensions = ["dollarmath"]`.** These documents are full of
currency: `$100,000`, `$1,000`. lifelib's MyST extension set is empty today and must stay
that way for this library to render.

## 5. `doc/source/libraries/index.rst` — list it

One row in the table:

```
   :doc:`uslib/index`                              U.S. life and annuity reference products and models
```

and one entry in the toctree:

```
   uslib/index.md
```

## 6. `.gitignore` — the mirrored copies are generated

```
doc/source/libraries/uslib/
```

One line per library. This cannot be globbed: `doc/source/libraries/` also holds the
hand-written documentation for `basiclife`, `annuallife` and the rest.

## 7. Verify

```bash
python -m pytest lifelib/libraries/uslib/tests -q
```

CI needs no change: `.github/workflows/tests.yml` and `tox.ini` both run bare `pytest` from
the repository root, which already collects `ifrs17a`'s in-library tests and will collect
these the same way.

Then build the docs and confirm the uslib pages are clean. The equivalent of this
repository's `tools/doccheck.py` is `sphinx-build -n -W --keep-going`; **the `-n` matters**.
Sphinx does not warn about an unresolved `:func:`/`:mod:` role by default — it drops the
role and renders plain text — so a build without nitpicky mode cannot tell you whether the
cross-references survived. During the prep it was the only thing that revealed 38 silently
dead references.

## 8. Not part of this merge

- **`requirements.txt`** in lifelib-products pins the runtime for the models. After the
  merge, `modelx` comes from lifelib's `install_requires` (step 3) and `pandas`/`numpy` are
  already assumed by the other libraries. `pytest` stays a development dependency and is
  deliberately not added to `install_requires`, even though the tests now ship.
- **`uk/` → `uklib`.** Out of scope, but the conventions are already general and the tooling
  is already parameterized: `tools/*.py` all take a library directory. Dry-run against `uk/`
  reproduces the predicted counts — 151 product source entries, 38 reference-library
  entries, ~1,472 bracket adjacencies — so the uklib run should be a re-invocation rather
  than a redesign. The one piece of genuinely new authoring it needs is its own copy of the
  citation-conventions section, for the same reason uslib needed one: the shared root
  `README.md` that defines them for both does not survive the split.
- **The models' autodoc pages** are already written and building
  (`products/<slug>/model-api.md`). Nothing further is required to publish them.
