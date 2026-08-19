# Merging `uslib/` and `uklib/` into lifelib

Everything in this repository is ready. This file is the lifelib-side half: the steps that
cannot be done here because they touch lifelib's own files.

The design decisions behind each step are in [USLIB-MERGE-PLAN.md](USLIB-MERGE-PLAN.md);
this is the checklist, not the argument. The plan was written for `uslib` and executed
there first; `uklib` was then put through the same phases, and [§9](#what-the-uklib-run-changed)
records where the second run contradicted the first.

**Status of the prep:** the documentation builds to **161 pages with 0 warnings** under
`-n -W --keep-going -E`, **16,794 internal anchor links resolve with 0 broken**, and the two
libraries' **1,576 tests pass**. All three are reproducible here:

```bash
python tools/doccheck.py
```

```bash
python -m pytest lifelib/libraries/uslib/tests lifelib/libraries/uklib/tests -q
```

```bash
python tools/doccheck.py --keep && python tools/check_anchors.py doc/build/check
```

---

## 1. Copy the two library directories

```bash
cp -r lifelib/libraries/uslib lifelib/libraries/uklib <lifelib>/lifelib/libraries/
```

That is the whole step, and it is a copy with no path rewriting because **the libraries
already sit at `lifelib/libraries/<lib>/` in this repository too**. That is deliberate: it
is what lets the page tree in §4 be copied verbatim rather than regenerated on this side.

Each library is self-contained: the models sit beside the documents that specify them, the
test suite is inside at `<lib>/tests/`, and every internal path reference is either
relative or library-root-relative, so nothing inside names its own location. Each directory
is already called by its library name — the anchors, the `automodule` paths and the package
names all say `uslib` and `uklib` today.

**Take them together.** `uklib/index.md` links to `../uslib/index.md` and to two explicit
targets on it — `#uslib-one-shape` and `#uslib-shared-vocabulary` — because D8 makes the
enforced model shape and the settled cells vocabulary rulings for *both* libraries, stated
once. The relative path holds inside `libraries/`, but only once both are there. Merging
`uklib` alone would break four cross-references and fail the `-n` build.

## 2. `setup.py` — ship the markdown

`get_package_data` lists the extensions that reach an installed copy:

```python
extensions = ['py', 'ipynb', 'xlsx', 'csv', 'json', 'pickle']
```

**Add `'md'`.** Without it the documents are not installed, so `lifelib.create("uslib", …)`
hands the user a library with no documentation — and for these libraries the documentation
is the point. `.py` and `.csv` are already covered, so the models, their inputs and the
tests travel as they are.

## 3. `setup.py` — raise the modelx floor

```python
install_requires=['modelx>=0.31.0']       # -> 'modelx>=0.32'
```

The nineteen models are serialized with modelx serializer v8. modelx 0.31.1 cannot read
them; `read_model` fails outright rather than degrading. This is a hard requirement of the
merge, not a preference.

## 4. `doc/source/conf.py` — nothing to add, one thing to keep

**No configuration change is needed at all**, but one existing workaround becomes load-
bearing — see the end of this section. lifelib already loads `myst_parser`,
`sphinx.ext.autodoc`, `autosummary` and `napoleon`, already sets
`autodoc_member_order = 'bysource'`, and already puts `lifelib/libraries` on `sys.path` —
which is why the models are importable as `<lib>.products.<slug>.<Model>` and why the
product slugs were underscored.

The documents reach the build through the **page tree**, not through configuration. Each
page under `doc/source/libraries/<lib>/` is a one-line `{include}` of the corresponding
library document, and the page tree mirrors the library tree so the authored relative links
keep resolving. Nothing is copied and nothing is generated at build time.

Copy `doc/source/libraries/uslib/` (98 files) and `doc/source/libraries/uklib/` (58 files)
from this repository into lifelib's `doc/source/libraries/` as they stand. All of them come
from `python tools/gen_scaffolding.py lifelib/libraries/<lib>`, and every include path they
carry is already the one lifelib needs — `../../../../../../lifelib/libraries/uslib/…`,
counted from the stub by `os.path.relpath` rather than written by hand — because the
libraries sit at that same path in this repository. Nothing here needs regenerating.

Those trees also carry the autodoc pages — `<Model>.rst` and one `<Space>.rst` per Space,
following `annuallife/TradLife_A.rst` — which deliberately do **not** live in the libraries:
they are Sphinx plumbing, and a `lifelib.create()` copy is better without them.

`_research/` is excluded by simply having no pages, so there is no `exclude_patterns` entry
to add either. It still ships with each library — it is the evidence behind the documents —
but it carries its own deliberately independent `[S#]` numbering, and a second, conflicting
`S1` in front of a reader is worse than not publishing it.

**Do not enable `myst_enable_extensions = ["dollarmath"]`.** These documents are full of
currency: `$100,000`, `£100,000`. lifelib's MyST extension set is empty today and must stay
that way for these libraries to render.

**`_scope_nbsphinx_link_rewriting_to_notebooks()` is now mandatory.** lifelib's `conf.py`
already carries it (it is defined around line 289 and called from `setup`), and it must
stay. nbsphinx registers `RewriteLocalLinks` with `app.add_transform`, so the transform
runs over *every* document rather than only notebooks: given a link that is nothing but a
fragment, it substitutes the current document's own filename and emits a `std:ref` to
`/<docname>.md#fragment`, which no explicit MyST target matches. The node is replaced during
the read phase, so myst-parser's own resolver never sees it.

Every `[R#]`, `[REG-R#]`, `[std]` and `[unverified]` citation is exactly such a bare
`#fragment` link: **5,300** of them as authored — 2,735 regulatory, 2,229 convention
markers and 336 inline pinpoint links. (Do not read the 16,794 from the status block as
this number: that counts every internal anchor link in the built site, most of which are
heading permalinks and autodoc cross-references, which this transform cannot touch. Nor
does the built HTML show the exposure, because Sphinx has by then rewritten every
cross-page citation to a full relative URL — the transform runs during the read phase,
while they are all still bare fragments.)

They are produced by **link reference definitions**, for which there is no `{ref}`-role
equivalent, because a shortcut reference is Markdown link syntax by construction. There is
no version of these documents that avoids the problem.

This repository cannot reproduce the failure: it does not load nbsphinx, so its build is
clean either way. That is exactly the trap — the check that passes here is not the check
that matters there.

## 5. `doc/source/libraries/index.rst` — list them

Two rows in the table:

```
   :doc:`uslib/index`                              U.S. life and annuity reference products and models
   :doc:`uklib/index`                              UK life and pension annuity reference products and models
```

and two entries in the toctree:

```
   uslib/index.md
   uklib/index.md
```

## 6. `.gitignore` — nothing to add

The page trees are committed source, not build output, so there is nothing to ignore beyond
what lifelib already ignores.

## 7. Verify

```bash
python -m pytest lifelib/libraries/uslib/tests lifelib/libraries/uklib/tests -q
```

CI needs no change: `.github/workflows/tests.yml` and `tox.ini` both run bare `pytest` from
the repository root, which already collects `ifrs17a`'s in-library tests and will collect
these the same way. **That is precisely why §9's first item matters** — a bare `pytest` at
the lifelib root collects both suites in one process.

Then build the docs and confirm the pages are clean, with
`sphinx-build -n -W --keep-going -E`; **the `-n` matters**.
Sphinx does not warn about an unresolved `:func:`/`:mod:` role by default — it drops the
role and renders plain text — so a build without nitpicky mode cannot tell you whether the
cross-references survived. During the uslib prep it was the only thing that revealed 38
silently dead references; during the uklib prep, 63 problems of which one warned.

Finally, confirm the links **arrive** rather than merely exist:

```bash
python tools/check_anchors.py <build tree>
```

Sphinx normalises label underscores to hyphens when it emits ids —
`uklib-term_assurance-s1` becomes `id="uklib-term-assurance-s1"` — so a check written
against the label text passes while every link goes nowhere. `check_anchors.py` reads the
ids out of the built pages instead.

## 8. Not part of this merge

- **`requirements.txt`** in lifelib-products pins the runtime for the models. After the
  merge, `modelx` comes from lifelib's `install_requires` (step 3) and `pandas`/`numpy` are
  already assumed by the other libraries. `pytest` stays a development dependency and is
  deliberately not added to `install_requires`, even though the tests now ship.
- **The models' autodoc pages** are already written and building, at
  `doc/source/libraries/<lib>/products/<slug>/<Model>.rst` and one `<Space>.rst` beside
  each. Nothing further is required to publish them.

---

## 9. What the uklib run changed

The plan's D8 fixed the conventions as house conventions and required the tooling to be
parameterized, so the uklib run was meant to be a re-invocation rather than a redesign. It
mostly was: the counts P3 predicted came out exactly, and P4 and P5 needed no new decisions.
What follows is everything that did not go to plan, because that is the part worth reading.

### The tests could not both be collected

`conftest.py` is a name pytest fixes. With two in-library suites, `pytest lifelib/libraries/uslib/tests
lifelib/libraries/uklib/tests` puts two files called `conftest` on `sys.path`; one wins `sys.modules`, and
every `from conftest import LIB` in *either* suite resolves to the other library. It
surfaced as a `FileNotFoundError` naming a uslib product under `uklib/`. The quiet version
of the same fault is a suite that locates the wrong library's models and passes.

`MODELS`, `LIB` and `model_path` now live in `us_registry.py` / `uk_registry.py`;
`conftest.py` re-exports them for its fixtures. **This is a merge-blocking item, not a
tidy-up:** CI runs bare `pytest` from the lifelib root, which collects both.

### The citation tools did not know where the code was

`separate_citations.py` and `gen_citation_links.py` excluded *fenced* code and nothing else.
CommonMark also has indented code — a four-space run after a blank line — which is how these
technical notes lay out their recursions, and 47 such blocks carry citation tags.

In uslib all but one of them is a bare `[S1]`, inert whether it is processed or not, so the
gap all but never showed. The exception found it: P5 had already written a literal
`(#uslib-immediate_annuity-s5)` into an indented block in
`immediate_annuity/technical-notes.md`, and that page printed the raw markup at the reader
until the S-citation reversal took it back out. In uklib they carry pinpoint cites
throughout, and the pinpoint pass is the one that *rewrites* text, so the same fault would
have landed in a rendered formula block on every product. This is the D5 asymmetry the plan
predicted — uk has roughly twice the pinpoint cites of us despite being half the size —
arriving in a form the inventory could not show.

New `tools/mdspans.py` answers where-is-the-code with markdown-it, MyST's own parser, rather
than a heuristic. Verified byte-neutral on uslib.

### `fix_doc_roles.py` could not see a cross-library reference

It collected model names from the library it was fixing, so uklib's five chassis pointers at
uslib models — `PA_UK_S` → `SPIA_US_S`, `Term_UK_A` → `Term_US_A`, `WOL_UK_S` →
`WholeLife_US_A` — were invisible to it and it reported 0. These are the same sibling
pointers the plan describes *inside* uslib, one level out. It now collects from every
sibling library. The leading dot is refspecific, so a UK model's chassis pointer lands on the
US model's page without either library naming the other's location — and that is the second
reason the two libraries want to be in one build.

### Two docstring conventions uslib does not have

- **`:data:` roles on modelx References**, 32 of them. A Reference is a module-level
  assignment, not a cells, so autodoc documents no target and the role is always dead.
  uslib has no `:data:` roles at all — it spells References as inline literals — so these
  were made to match.
- **Aligned two-column blocks**, 19 of them across seven `Projection` docstrings.
  `` ``"BEF_DECR"``  the start of the month`` has no RST construct behind it: docutils reads
  it as a paragraph plus an over-indented block. New `tools/fix_docstring_lists.py` converts
  them to the definition lists the rest of the corpus uses.

### Open: uslib has five of those blocks left

`python tools/fix_docstring_lists.py lifelib/libraries/uslib --dry-run` reports **5 blocks, in five
`Projection` docstrings**. **None of them warns**, which is why a build at zero warnings did
not find them: they are all the silent kind, one term with a wrapped description, which
docutils parses as a definition list whose *term* is the whole first line — description
included. They render wrongly and always have. Left alone here rather than changing a
finished library on the way past; the tool is in the repository and the fix is one command.

### `_research/` inflates the plan's §6 inventory

That inventory counted the whole `uk/` tree. `_research/` is out of the build under D6 and
receives no definitions, so the numbers for *rendered* documents are lower and the shortfall
is not a miss:

| | §6 predicted for uk | rendered | in `_research/` |
|---|---|---|---|
| pinpoint cites | 768 | 518 | 321 |
| comma lists | 1 | 0 | 1 (`[S1,S2]`) |
| bracket adjacencies | 1,947 | 1,515 | 472 |

The 1,515 is 1,505 separated by the tool, 8 inside indented code blocks where an adjacency
is displayed and never resolved, and 2 by hand. The §6 column was measured on the `uk/` tree
as it stood before the models landed; measuring the same way today gives 1,987 rather than
1,947, so it is a moving figure and only the split matters.

### Four citations that needed a hand

The tools reported two adjacencies they declined to guess at, and the P5 output showed two
more of the same shape that nothing had flagged. All four are a bare citation nested inside
another citation's brackets — `[R10, …; verified via [REG-R33][REG-R34]]` — where, once the
outer bracket becomes a link, CommonMark will not put a link inside link text. Fixed by
unnesting: the annotation becomes a parenthetical and all three citations are siblings.

uslib has 19 more of that shape and uklib five, but every one of those swallows a `[std]` or
`[unverified]` marker rather than a citation, which is the accepted D5a behaviour for
qualified forms. Only these four lost a cross-reference.

### `uslib/index.md` had drifted

Its generated definition block was missing: P5 ran before P6 rewrote that page, and it was
never regenerated, so the eight `[std]` and two `[unverified]` markers on the page that
*states* every citation tag is a link were the only ones that were not. Regenerated here.
The same thing happened to `uklib/index.md` during its own P6 and was caught by
`check_anchors.py`, which is the check that exists to catch it.

### Smaller notes

- **uk has models now.** The plan assumed the UK section had none and that a product
  directory carrying documents but no model had to be legal. PR #14 landed all seven, so D2
  colocation and D9 autodoc apply to uklib exactly as to uslib.
- **No generated "Verifying this copy" block in uklib's `model.md`.** uslib carries one per
  product from an earlier version of `gen_scaffolding.py`, which no longer emits it. uklib's
  hand-written `## Tests` sections already name the test module, say what it asserts and
  give the command, so D7's requirement is met without a near-duplicate beside it.
- **`gen_scaffolding.py`'s `TITLES`** gains the seven UK slugs. One map serves both
  libraries, since slugs are unique across them.
- **28 document H1s retitled** to `Product Specification` / `Technical Notes` /
  `Implementation Notes` / `Sources`, matching uslib: the toctree shows the H1, and
  repeating the product name under a page already titled for the product reads badly.
- **Cross-document target links need no path.** `[text](../uslib/index.md#uslib-one-shape)`
  makes MyST look for a local *id* in that document rather than a label, and an explicit
  `(target)=` does not match. Bare `#target` resolves project-wide.
