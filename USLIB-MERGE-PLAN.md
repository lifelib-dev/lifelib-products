# Merge plan — `us/` → lifelib as the **uslib** library

**Status:** Plan, 2026-08-15. Branch `uslib-merge-prep`. Nothing in this plan has been
executed; this document is the specification for the prep work, to be reviewed before any
file moves.

**Goal.** Move this repository's `us/` section into
[lifelib](https://github.com/lifelib-dev/lifelib) as a library named **uslib**, such that:

1. each product's **model lives in the same directory as its documents**, under
   `uslib/products/<product>/`;
2. the markdown documents are **rendered as Sphinx pages via MyST**, while physically
   residing under the library directory (`lifelib/libraries/uslib/`), not under `doc/`;
3. **every cross-reference is a working link** — document-to-document links, and the
   `[S#]` / `[R#]` / `[REG-R#]` citation tags, which are plain text today.

The prep work happens **here**, in `lifelib-products`, so that the merge into lifelib is a
directory move plus a small set of lifelib-side configuration edits. `uk/` is untouched and
stays in this repository.

---

## 1. Target layout

```
lifelib/libraries/uslib/
  index.md                          <- from us/README.md; carries the toctree
  products/
    index.md                        <- new: taxonomy landing page + toctree
    term_life/
      index.md                      <- new: per-product landing page + toctree
      product-spec.md
      technical-notes.md
      sources.md
      model.md                      <- from us/models/term-life/README.md
      model-api.md                  <- new: autodoc cells reference (D9)
      run.py
      model_point_table.csv  premium_rates.csv  mort_table.csv
      class_factor_table.csv  shock_lapse_table.csv
      Term_US_A/                    <- the modelx model, formulas only
        __init__.py  _system.json  Data/  Projection/
    whole_life/  universal_life/  indexed_ul/  variable_ul/  guaranteed_ul/
    fixed_deferred_annuity/  fixed_indexed_annuity/  variable_annuity/
    registered_index_linked_annuity/  immediate_annuity/  deferred_income_annuity/
  references/
    regulatory-and-actuarial-references.md
  _research/
    *.md                            <- 19 provenance files, shipped but not in the toctree
```

and on the lifelib documentation side:

```
lifelib/doc/source/libraries/
  index.rst                         <- one new table row + one new toctree entry
  uslib/                            <- GENERATED at build time (gitignored), *.md only
```

Twelve `us/models/<product>/` directories disappear; their contents merge into the
corresponding `us/products/<product>/`.

This shape is the **house layout for a country library**, not a uslib one — `uk/` follows it
as `uklib` (D8), with seven products, no `models/` yet, and therefore product directories
that carry documents but no model. Read `uslib` below as `<lib>` throughout.

---

## 2. Established constraints

Everything in this section was verified against the lifelib checkout at
`C:/Users/fumito/OneDrive/pyproj/lifelib` (v0.13.0) or by building a throwaway Sphinx
project with the installed toolchain (Sphinx 8.2.3, myst-parser 5.1.0, markdown-it-py
4.2.0). None of it is assumed.

| # | Fact | Consequence |
|---|---|---|
| C1 | lifelib's `conf.py` already loads `myst_parser`; `source_suffix = '.rst'` does not block `.md`, because myst registers `.md` itself. `doc/source/libraries/ifrs17a/index.md` and the whole of `economic_curves/` are already MyST. | No new extension is needed. MyST is an established lifelib convention, not a novelty. |
| C2 | Sphinx has exactly one `srcdir`. `sphinx-gallery` already reaches into `lifelib/libraries` and writes into `doc/source/generated_examples`, and `.gitignore` already carries `generated*/`. | Pulling library-resident docs into the doc tree at build time is precedented in this project. |
| C3 | Sphinx **does** discover source files under `_`-prefixed directories (built `_research/note.md` successfully). | `_research/` needs no rename; it needs deliberate *exclusion* instead. |
| C4 | lifelib documents models with real autodoc — `.. automodule:: basiclife.BasicTerm_S.Projection` plus one `.. autofunction::` per cells — importing model folders as implicit namespace packages, with `lifelib/libraries` on `sys.path`. | **Every path component below `libraries/` must be a valid Python identifier.** `term-life` is not. This is the hard constraint behind decision D1. |
| C5 | `setup.py:get_package_data` ships only `py, ipynb, xlsx, csv, json, pickle`. | `.md` is missing — library-resident docs would **not** be installed, so `lifelib.create("uslib", …)` would produce a copy with no documentation. Must be fixed on the lifelib side. |
| C6 | lifelib pins `install_requires=['modelx>=0.31.0']`; these models are serializer v8 and need `modelx>=0.32` (see [requirements.txt](requirements.txt)). | lifelib's floor must be raised as part of the merge. |
| C7 | In CommonMark, `[S1][S2]` is a **full reference link**: text `S1`, target `S2`. Verified — it renders as a single anchor labelled "S1" pointing at S2's target, and the S1 citation vanishes. | The single biggest hazard. There are **2,064** such adjacencies. See D4. |
| C8 | A shortcut reference (`[S1]` with a matching `[S1]: …` definition in the same file) resolves correctly; an *undefined* one is left as literal text. | Safe, incremental migration: files not yet converted render exactly as they do today. |
| C9 | Link reference definitions **do not** propagate through a MyST `{include}`. Verified: `[S1]` stayed literal when its definition came from an included file. | Definitions must be written into each document. No shared-definitions shortcut exists. |
| C10 | Explicit MyST targets (`(name)=`) resolve from any document with no warning. Links to *auto-generated heading anchors* resolved but emitted `myst.xref_missing` warnings, because resolution depends on document read order. | Use explicit targets, not `myst_heading_anchors`. |
| C11 | Duplicate explicit targets across documents produce `WARNING: duplicate label`. `S1` means a different source in each of the 12 products. | Target names must be namespaced per product. |
| C12 | lifelib's MyST config has `enable_extensions=set()` — `dollarmath` is **off**. | Currency (`$100,000`) is safe as written. Do not enable `dollarmath` for this doc set without escaping ~all currency first. |

---

## 3. Decisions

### D1 — Product slugs become underscored identifiers

`term-life` → `term_life`, `fixed-deferred-annuity` → `fixed_deferred_annuity`, etc.

**Why:** C4. `uslib.products.term-life.Term_US_A` is not an importable dotted name, so
hyphenated slugs permanently rule out lifelib-style per-cells API pages for these twelve
models. Underscores also match every other lifelib library.

**Rejected:** keeping hyphens and documenting models only through the hand-written
`model.md`. That works today but forecloses the autodoc route, and the rename is cheap
*now* while all the link rewriting is happening anyway.

*Note:* `uslib`, `products` and each product directory become implicit namespace packages —
no `__init__.py` needed, matching `basiclife`, which has none.

### D2 — Model and documents colocate under `products/<product>/`

The twelve `us/models/<product>/` directories merge into `us/products/<product>/`. The
model's `README.md` becomes `model.md` — a directory cannot hold two `README.md`, and
`README` is a poor Sphinx document name.

The model reads its CSVs through `Data.input_dir()` → `_model.path.parent`, so as long as
the model folder and its CSVs stay siblings, **no formula changes are required**. Verified
by reading `Data/__init__.py`.

Each product directory gains a small `index.md` whose toctree orders the four documents:
product spec → technical notes → model → sources.

### D3 — Docs reach Sphinx by a build-time copy, driven from `conf.py`

Add to lifelib's `doc/source/conf.py`:

```python
def _sync_uslib_docs(app):
    """Mirror uslib's *.md into the doc tree; Sphinx has only one srcdir."""
    src_root = Path(here).parents[1] / "lifelib" / "libraries" / "uslib"
    dst_root = Path(here) / "libraries" / "uslib"
    for src in src_root.rglob("*.md"):
        dst = dst_root / src.relative_to(src_root)
        if not dst.exists() or src.stat().st_mtime > dst.stat().st_mtime:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
    for dst in dst_root.rglob("*.md"):            # prune deletions
        if not (src_root / dst.relative_to(dst_root)).exists():
            dst.unlink()

def setup(app):
    app.add_css_file("custom-style.css")
    app.connect("builder-inited", _sync_uslib_docs)
```

Only `*.md` is copied — never the CSVs, `run.py`, or the model folders. The mtime guard
keeps Sphinx's incremental rebuild working; a blind `rmtree`+`copytree` would force a full
rebuild of ~50 pages every run. `doc/source/libraries/uslib/` goes in `.gitignore`.

**Why not the alternatives:**

- ***`{include}` stubs*** — one stub per document, mirroring the tree. Single source of
  truth and no generated files, but it needs 50+ hand-maintained stubs, source line numbers
  in warnings point at the stub, and per C9 anything document-scoped (the link definitions
  this plan depends on) does not survive the include. Rejected on C9.
- ***Symlink*** `doc/source/libraries/uslib` → the library dir. Cleanest in principle;
  needs Developer Mode or elevation on Windows, and `core.symlinks` cooperation from every
  clone. Rejected as hostile to the primary development platform.

Because the copy preserves the directory structure verbatim, **every relative link between
documents resolves in the built docs exactly as it does on GitHub**. That is the property
that makes decision D4 workable.

### D4 — Citations become links via per-file link reference definitions

The compact `[S6]` form stays in the prose. Each document gains a generated block of link
reference definitions at its foot:

```markdown
<!-- BEGIN generated citation links — regenerate with tools/gen_citation_links.py -->
[S1]: #uslib-term_life-s1
[S2]: #uslib-term_life-s2
[R4]: #uslib-term_life-r4
[REG-R18]: #uslib-reg-r18
[std]: #uslib-std
[unverified]: #uslib-unverified
<!-- END generated citation links -->
```

and the anchors are explicit MyST targets placed above the entry headings they name:

| Target | Placed in | Example |
|---|---|---|
| `uslib-<product>-s<n>` | `products/<p>/sources.md`, above `### S1 — …` | `(uslib-term_life-s1)=` |
| `uslib-<product>-r<n>` | `products/<p>/sources.md`, above `### R1 — …` | `(uslib-term_life-r1)=` |
| `uslib-reg-r<n>` | `references/regulatory-and-actuarial-references.md`, above `### R1. …` | `(uslib-reg-r1)=` |
| `uslib-std`, `uslib-unverified` | `index.md`, on the citation-conventions section | — |

**Why this shape:**

- **The prose is unchanged.** The inline alternative — rewriting all 12,216 tags to
  `[S1](#uslib-term_life-s1)` — adds roughly 230 KB of link syntax to documents that are
  read as much in the editor and on GitHub as in the built HTML.
- **Per-product numbering is handled for free.** `S1` means a different source in each of
  the twelve products (C11); because definitions are per-file, each document's `[S1]`
  simply points at its own product's target.
- **Partial conversion is safe** (C8): a document without the block renders as it does
  today.
- **It is generated, not hand-written**, from the tags each document actually uses — so it
  cannot drift, and a test can assert that every tag used has a definition and every
  definition has a target.

**The mandatory companion edit — de-adjacency.** Per C7, `[S2][S3]` becomes one link the
moment definitions exist. Every adjacency must be separated by a single space
(`[S2] [S3]`), which is also how the rendered output should read:

| Adjacency class | Count | Treatment |
|---|---|---|
| plain tag `][` plain tag | 2,064 | scripted: insert one space |
| cite-ish `][` cite-ish (pinpoint or comma-list operand) | 93 | scripted: insert one space |
| everything else | 3 | manual — `[R22][search summaries]`, `[REG-R31][REG-R70 context]` |

This edit **must land in the same commit as the definition blocks**, never later.

### D5 — Pinpoint cites and comma lists become links too

Neither form becomes a link under D4 alone, because its bracket text is not a bare label.
**Both are in scope** — the goal is *all* cross-references, not most of them.

| Form | Example | us | uk | Treatment |
|---|---|---|---|---|
| Pinpoint cite | `[R1 §4.B]`, `[R13 §3.B(1)(b)]` | 381 | 768 | explicit inline link, scripted from the leading tag: `[R1 §4.B](#uslib-term_life-r1)` |
| Comma list | `[S3, S7]`, `[S3, S5, S7]` | 91 | 1 | split into separate shortcut refs: `[S3], [S7]` — they then link for free under D4 |

These are the only edits in the plan that change the **visible text** of a citation: a
comma list becomes two bracketed tags with a comma between them. The pinpoint form is
untouched on the page; only its target changes from nothing to a link.

Note the asymmetry — pinpoint cites are twice as common in `uk/` as in `us/`, so this is
the part of the pipeline that most needs to be right before it is re-run for `uklib`
(D8).

### D5a — `[std]` and `[unverified]` are links as well

All 1,257 `[std]` and 275 `[unverified]` occurrences in `us/` (684 and 143 in `uk/`) get a
definition pointing at that library's citation-conventions section, exactly like a
citation tag. They are defined terms with a precise meaning that a reader has to know to
read a parameter table correctly, and one definition line per file is a cheap way to keep
that meaning one click away.

Two consequences worth stating, neither blocking:

- `**[std]**` renders as a **bold link**, and `[unverified]` appears inside at least one
  heading, so it will render as a link in a heading. Both are acceptable.
- Variant forms — `[std illustrative]`, `[unverified as to market share]`, 43 occurrences
  across 29 distinct spellings — are *not* bare labels and so do not link. Leave them.
  Normalizing them into `[std]` plus prose would change the author's meaning, which is out
  of scope for a mechanical pass.

### D6 — `_research/` ships but is not rendered

The 19 provenance files stay in the library — they are cited by the product documents and
the README calls them ground truth — and therefore travel into every `create()` copy along
with everything else. **Settled deliberately**, against the alternatives of holding them in
the lifelib repository outside the library directory or teaching `create()` an ignore list:
a copy of this library should carry the evidence for its own documents, not just their
conclusions.

They are **not rendered**, however. They carry their own `[S#]`/`[R#]` numbering that is
deliberately independent of the product `sources.md` numbering (see §7), they are explicitly
"do not renumber" material, and they would roughly double the rendered page count. Exclude
them from the build with `exclude_patterns += ['libraries/uslib/_research/*']`, and refer to
them by repository path rather than by doc link.

### D7 — Tests keep their current shape, with rewritten paths

`tests/` stays a repo-root suite here — 14 files, `conftest.py` plus twelve per-product
modules and `test_model_conventions.py` — with `MODELS` in
[tests/conftest.py](tests/conftest.py) repointed at `us/products/<product_slug>/<Model>`.

**On the lifelib side the suite lands at `lifelib/libraries/uslib/tests/`** — inside the
library, following `ifrs17a`.

lifelib has two test conventions:

| Convention | Used by | Shape |
|---|---|---|
| central, flat | fastlife, nestedlife, simplelife, solvency2, tradlife_a | `lifelib/tests/libraries/test_<lib>.py`, locating models via `Path(__file__).parents[2] / "libraries"` |
| in-library | ifrs17a | `lifelib/libraries/ifrs17a/tests/` with its own `conftest.py` and `expected/` |

**The decision is in-library**, and the deciding argument is the same one that keeps
`_research/` in the library (D6): `lifelib.create()` is a bare `shutil.copytree` of the
library directory, so the copy an actuary receives is complete — the models, the documents
that specify them, the provenance behind those documents, and the assertions that the
models reproduce what the documents claim. The suite is 14 files: `conftest.py`, twelve
per-product modules, and `test_model_conventions.py`.

What this buys, beyond consistency with D2:

- **The copy can check itself.** An actuary who changes an assumption runs one command and
  gets green or red. That is the one programmer tool that survives contact with a
  non-programmer, and it only works if the tests are in the copy.
- **The worked-example guarantee keeps its artifact.** The documents' central claim — every
  model reproduces its technical notes' worked example, cell by cell — is checkable
  wherever the library goes, not only in a lifelib checkout.

Accepted costs:

- **14 files the user did not ask for**, in a copy aimed at actuaries rather than
  programmers. Mitigated by the P6 `model.md` note, which tells the reader what the suite
  is for and how to run it, rather than leaving them to infer it from a directory name.
- **`pytest` is an extra dependency** for anyone who wants to run them; it is absent from
  lifelib's `install_requires` and would stay that way.

**Locator — this is a correctness constraint, not a style choice.** In-library placement
requires `conftest.py` to resolve models *relatively*:

```python
LIB = pathlib.Path(__file__).resolve().parents[1]   # the uslib directory
# MODELS entries read "products/<slug>/<Model>"
```

It must **not** use `lifelib._dirs.TEMPLATES["uslib"]`, which resolves to the *installed*
library. In a `create()` copy that would silently test lifelib's pristine models instead of
the user's edited ones — a green run that proves nothing. (`TEMPLATES` would have been the
right answer for the central-tree placement, where there is no library above the tests.
The two placements need opposite strategies.)

Unaffected by the choice: CI (`tests.yml` and `tox.ini` both run bare `pytest` from the
repository root, which collects either location — verified against `ifrs17a`, whose
in-library tests are already collected this way), and packaging (`py` is already in
`get_package_data`).

`test_model_conventions.py` asserts that the registry name, the directory on disk and the
model's `_name` agree — that assertion is what will catch a missed rename in D1, so it
should be run first after the rename, not last.

### D8 — These are house conventions, parameterized by library

`uk/` is destined to become **uklib** on the same pattern, so nothing below may hardcode
"us". The uk section is the same shape, verified: 31 markdown files, 7 products, the same
tag vocabulary including `[REG-R#]`, the same two entry-heading conventions, 151 source
entries, 38 reference-library entries, 1,947 bracket adjacencies. It has **no `models/`
directory** — UK models are a roadmap item — so D2's merge is a no-op there and a product
directory with documents but no model must be legal.

| Item | uslib-only form | House form |
|---|---|---|
| Target names | `uslib-term_life-s1` | `<lib>-<product>-s<n>`, `<lib>-reg-r<n>`, `<lib>-std` |
| conf.py sync hook | hardcoded `uslib` | discover every `libraries/*/index.md` and sync that tree — adding uklib then needs no `conf.py` edit at all |
| `exclude_patterns` | `libraries/uslib/_research/*` | `libraries/*/_research/*` |
| `.gitignore` | `doc/source/libraries/uslib/` | one line per library, listed explicitly — `doc/source/libraries/` also holds hand-written dirs, so it cannot be globbed |
| P3/P4/P5 and D5 tooling | — | every script takes `--library` and derives its product list from disk; no slug is hardcoded |
| Model names | `<Product>_US_<grid>` | `<Product>_<CC>_<grid>` — the country tag already separates `Term_US_A` from a future `Term_UK_A` |

Product slugs convert cleanly under D1 in both (`term-assurance` → `term_assurance`, …),
and the per-library link definitions of D4 mean `[S1]` can safely mean a different source
in uslib and uklib, exactly as it already does across products.

**The one substantive new item is the shared conventions text.** The citation conventions —
`[S#]`, `[R#]`, `[REG-R#]`, `[std]`, `[unverified]` — are defined **once**, in this
repository's root `README.md`, which both `us/README.md` and `uk/README.md` point at. That
shared parent does not survive the split into two independent lifelib libraries. Combined
with D5a, which turns `[std]` and `[unverified]` into links, **each library needs its own
copy of the conventions section, carrying its own anchors** (`uslib-std` / `uklib-std`).

Duplicating it rather than hosting it once under `doc/source/` is the consistent answer
under D6/D7: a `create()` copy must be self-contained, and a page in the doc tree is not in
the copy.

**Sequencing.** Do uslib first as the pathfinder, but write every script with `--library`
from the outset and **dry-run it against `uk/`** at the end of P3, P4 and P5. The uk counts
above and in §6 are the expected output; a script that cannot reproduce them is not general
enough, and finding that out on the uklib run instead is the expensive way.

### D9 — The twelve models get autodoc API pages

Settled: yes. The raw material is unusually good — **1,581 cells, 100% of them carrying a
docstring**, and all 24 Spaces documented too. That is a complete API reference already
written; it is currently just unreachable.

Each product directory gains a `model-api.md` beside its `model.md`: MyST prose framing an
`{eval-rst}` block that hosts the autodoc directives. `model.md` stays the narrative — why
the model is shaped as it is, what is **[std]**, what the tests cover — and `model-api.md`
is the generated cells reference, in the spirit of lifelib's `BasicTerm_S.rst` but without
hand-listing 150 `.. autofunction::` entries per model:

````markdown
```{eval-rst}
.. automodule:: uslib.products.term_life.Term_US_A.Projection
   :members:
```
````

with `autodoc_member_order = 'bysource'`, which lifelib already sets, so cells appear in the
order the notes derive them.

**Verified by spike, in this order:**

1. The model folders **import cleanly at the target depth** as implicit namespace packages —
   `uslib.products.term_life.Term_US_A.Projection` imports and carries its docstring. The
   serialized files say they are importable; they are.
2. A **MyST page can host `automodule`**. The docstrings are RST — roles and simple tables —
   and they render correctly inside `{eval-rst}`: cells emitted, tables as real `<table>`,
   py links resolving, and ordinary MyST links in the same page still working. **So the API
   page is a `.md` in the library tree and D3's existing `*.md` sync carries it. No new
   mechanism.**

**What breaks, and must be fixed first:**

| Issue | Count | Cause |
|---|---|---|
| `:mod:`<Model>`` — bare model name | 91 | role resolution is relative to the current module, which becomes `uslib.products.<slug>.<Model>`; a bare `Term_US_A` names nothing |
| `:mod:`<Model>.<Space>`` | 72 | same |
| cross-Space `:func:` (e.g. `input_dir`, in `Data`, cited from `Projection`) | 2 | resolves only within the current module |
| malformed RST simple table in a docstring | ≥1 of ~54 | in `Term_US_A.Projection`, `plt_mort_factor_init_formula` is 28 characters and overflows its 26-character column rule |

The other **823** `:func:`/`:attr:` roles are fine: they are same-Space and resolve relative
to the current module at any depth.

**Two things implementation added to this picture.**

*Sixty-six of the 163 module roles are cross-model* — the variable annuity naming the MYGA
deferred chassis, the DIA naming the SPIA payout chassis, FIA and VA both naming
`Term_US_A`. They are the chassis relationships the documents describe, restated in the
docstrings, and they break in exactly the same way. The leading dot fixes them the same way
too: refspecific search matches any module whose path ends that way, so a sibling reference
resolves without either model knowing where the other sits. A fixer that only knew its own
model's name would have silently left a third of the work undone.

*Importing a model leaves `__pycache__` inside its folder*, and `test_round_trip_is_stable`
compares the source and written file sets with `rglob("*")`. Under D9 the models are
imported as a matter of course — that is what autodoc does — so the test failed for anyone
who had built the docs. The comparison now ignores `__pycache__`, through a shared
`model_files()` helper in each of the four modules that makes it. This is the first place
where documenting the models changed what the tests must assert, and it is a consequence of
D9 rather than incidental tidying.

**The fix is one character.** Prefix the failing roles with a dot — `:mod:`.Term_US_A``,
`:func:`.input_dir``. The leading dot makes the lookup *refspecific*, matching any module
whose path ends that way. Verified: it resolves to
`#module-uslib.products.term_life.Term_US_A`, and the dot is stripped from the rendered
text, so the page reads exactly as before. It is also **library-agnostic**, which
`.. currentmodule::` would have been too — except that it does not work: tested, and
`:mod:` roles stay unresolved under it. 165 mechanical edits, no docstring rewritten.

**This is the phase's real hazard: the failures are silent.** Sphinx's Python domain does
not warn on an unresolved `:func:`/`:mod:` by default — it drops the role and renders plain
text. Building the *broken* state reports **1 warning** (the malformed table) and says
nothing about 163 dead module references; the same build with `-n` reports them all.
**So the P6 doc-check harness must run `sphinx-build -n -W --keep-going`.** Nitpicky, not
merely warnings-as-errors. Verified both ways.

---

## 4. Prep phases, in this repository

Each phase is a commit on `uslib-merge-prep`, with `python -m pytest tests -q` green at the
end of every one.

**P0 — Structural markdown fixes** *(2 files)* — **done**
Independent of everything else; fixes latent rendering bugs that exist today.
- `us/references/regulatory-and-actuarial-references.md:1683` — a `---` line directly
  follows `payout mortality.` with no blank line, so MyST renders that sentence as an
  **H2 heading**. Blank line inserted.
- `us/products/fixed-indexed-annuity/sources.md:324` — H2 → H4 jump
  (`myst.header` warning). `#### R110.` demoted to `### R110.`: it is the one entry in that
  section not part of the AP&P group below it, so giving it its own H3 is the minimal fix
  and invents no editorial content.
- ~~`us/README.md` — bare `<product-type>`, `<product>`, `<country>`, `<grid>`~~ —
  **withdrawn, false positive.** All four are already inside backticks. The scan that
  flagged them blanked fenced code blocks but not inline code spans. Rechecked with spans
  stripped: **zero** bare angle-bracket tokens in `us/`.

Adds `tools/md_lint.py`, which is what re-checks this and gates P4: it reports setext
rules, heading-level jumps, missing/duplicate H1, and bracket adjacencies. Structural checks
apply to every file; the adjacency check applies only to *rendered* documents, since
`_research/` never receives the definitions that make an adjacency dangerous.

**P1 — Directory restructure** *(pure `git mv`, no content edits)*
- Rename the 12 product slugs to underscores (D1) in `us/products/`.
- Move each `us/models/<p>/` into `us/products/<p_>/`; `README.md` → `model.md`.
- Delete the now-empty `us/models/`, and the stray empty `us/regulatory/` (an untracked
  leftover of the framework revert in 832247f — `uk/regulatory/` is the same and can go
  with it).
- Nothing builds or passes at the end of this phase except `git status`; P2 is its
  other half and the two may be squashed if you prefer a single reviewable move.

**P2 — Path rewrites** *(mechanical, scripted)* — **done**

**The suite moved into the library first.** `tests/` is now `us/tests/`, not a repo-root
directory moved at merge time as P7 item 6 originally said. This is the same D7 decision
executed earlier, and it earns two things: `us/` is now the complete library, so the merge
is a single directory move with nothing left behind; and `conftest.py` can already carry its
final form — `LIB = Path(__file__).resolve().parents[1]` with `MODELS` entries reading
`products/<slug>/<Model>`. Zero merge-time edits, and the relative locator D7 requires is
correct from today rather than promised.

**Paths became library-root-relative, not `uslib/`-prefixed.** `us/_research/term-life.md`
is now `_research/term-life.md`. A path relative to the library root is correct in this
repository *and* after the move into `lifelib/libraries/uslib/`, and it is the same string
uklib wants — so it survives both moves untouched, which the `uslib/` prefix this plan first
proposed would not. `tools/rewrite_paths.py`, 641 replacements across 118 files:

| Where | What | Count |
|---|---|---|
| model `*.py` and `*.md` | `us/models/<hyphen>` and `us/products/<hyphen>` → `products/<underscore>` | 641 across all rules |
| `*.md` | relative link targets — resolved against the filesystem, repaired, then normalised to the shortest path that reaches the file (`tools/fix_relative_links.py`) | 69, of which 66 were broken |
| model `*.py` docstrings | **D9:** leading dot on `:mod:` roles — 97 own-model, 66 cross-model | 163 |
| model `*.py` docstrings | **D9:** leading dot on cross-Space `:func:`/`:attr:` roles | 2 |
| `us/tests/*.py` | `REPO` → `LIB`, registry paths, and two contract assertions (below) | — |

`us/regulatory/*` references are deliberately **not** rewritten. All 39 sit in `_research/`
and name a statutory-framework stream removed from the library in 832247f; there is nothing
to point them at, and editing them would falsify a provenance record.

The link repair resolves every relative target against the filesystem rather than
pattern-matching the breakage, so an unfixable link is reported instead of mangled. It
reports **0 unresolved**, and a second run is a no-op.

Two test contracts changed, both because the world they assert about changed:
`test_the_model_ships_with_its_inputs_and_a_runner` now expects `model.md` rather than
`README.md`, and the round-trip file-set comparison ignores `__pycache__` (see D9).
One hardcoded hyphenated slug — `assert MODEL_PATH.parent.name == "fixed-indexed-annuity"` —
was caught by the suite exactly as D7 predicted, being the one thing a path rewriter cannot
see because it is a bare directory name rather than a path.

*Not done here:* the malformed docstring tables. They are only observable through the
autodoc build, so they are handled in P6 where that build lives.

**P3 — Citation anchors** *(targets only; no citation links yet)*
Insert `(uslib-<product>-s<n>)=` / `(uslib-<product>-r<n>)=` above each of the **237** source
entries in the twelve `sources.md`, and `(uslib-reg-r<n>)=` above each of the **90** entries
in `references/regulatory-and-actuarial-references.md` (numbering runs to R157, but the
retired R73–R149 block leaves only 90 live entries — the frozen numbers are what the targets
must carry, not the ordinal position).

**Then the conventions section.** `us/README.md` currently *points at* the repository root
`README.md` for the citation conventions; per D8 that shared parent does not survive the
split, and per D5a `[std]` and `[unverified]` now need anchors. So copy the conventions
table into `us/README.md` and give it the `(uslib-std)=` / `(uslib-unverified)=` targets.
This must happen here, before P5 generates definitions that point at them.

Watch for this: the entry headings use **two conventions** —
`### S1 — Title` in `term-life` and `whole-life`, `### S1. Title` in the other ten (and the
same split exists in `uk/`). The insertion script must match both, and the count above is
the check that it did.

**Idempotent and inert** — nothing links to these targets yet, so this phase cannot change
any rendering.

**P4 — De-adjacency** *(2,244 separators in rendered documents)*
Per D4. Still inert — with no definitions in place, `[S2] [S3]` renders as literal text just
as `[S2][S3]` does. This phase is deliberately separate so its diff can be reviewed on its
own; it is the one that would silently corrupt meaning if it were incomplete.

**Scope: rendered documents only.** `_research/` is left alone — 650 further adjacencies
that stay literal because D6 keeps those files out of the build and P5 gives them no
definitions. The hazard is created by the definitions, not by the adjacency, so touching
2,700 lines of provenance for no rendering benefit would be churn. `tools/md_lint.py`
enforces exactly this scope, and 2,244 → 0 is the phase's completion test.

*(The 2,157 in an earlier draft counted non-overlapping tag **pairs**; 2,244 counts every
`][` **separator to insert**, which is what the edit actually does — a run of three tags is
one pair-match short of two separators.)*

**P5 — Citation link definitions** *(the phase that turns citations into links)*
Add `tools/gen_citation_links.py --library us`, run it over the 36 product documents and the
12 `model.md`, and commit the generated blocks — including the `[std]` and `[unverified]`
definitions of D5a. Then the two D5 forms, in this order:

1. split comma lists (91 sites) — they become links for free once split;
2. linkify pinpoint cites (381 sites) as explicit inline links, scripted from the leading
   tag.

Add a test asserting round-trip integrity: every tag used has a definition, every definition
has a target, no target is defined twice, and no `][` adjacency survives in a file that
carries a definition block. Dry-run the whole pipeline against `uk/` (D8) and check the
output against the §6 uk column.

**P6 — Sphinx scaffolding, authored in the library tree**
- `us/README.md` → `us/index.md` with a MyST toctree.
- New `us/products/index.md` (the two taxonomy tables from the README, plus a toctree).
- New `us/products/<p>/index.md` × 12.
- **Each of the twelve `model.md`: a "Verification" note** saying which module in `tests/`
  asserts that model's worked example, what it covers, and the one command that runs it
  against *this* copy. Required by D7: the suite ships with the library, so a reader who
  edits an assumption has a way to find out whether they broke the documented example —
  but only if the documents tell them it exists.
- **New `us/products/<p>/model-api.md` × 12** (D9) — MyST prose framing an `{eval-rst}`
  block with `.. automodule:: uslib.products.<slug>.<Model>.Projection :members:` and the
  same for `Data`. Short and near-identical across the twelve, so generate them from a
  template rather than hand-writing.
- A `doc-check` harness: a throwaway `conf.py` mirroring lifelib's MyST settings **plus
  `autodoc`, `napoleon` and `libraries/` on `sys.path`**, so the whole set can be built
  **here** with **`-n -W --keep-going`** and land in lifelib clean. This is the acceptance
  test for the whole plan. The `-n` is not optional: per D9, unresolved Python roles are
  silent without it, and the entire point of the exercise is that cross-references are
  links.

**Result: 75 documents, 0 warnings.** The first build reported 61 problems, every one of
which was real and invisible without `-n`. What they were, since the mix is the useful part:

| Found | Count | What it actually was |
|---|---|---|
| Unresolved `:func:` roles | 38 | Roles written as a path through a model, `Term_US_A.Projection.pols_if`. The P2 fixer only knew bare `:mod:` names. |
| Double-dotted roles | 38 | **Self-inflicted.** The P2 fixer was not idempotent — it re-dotted its own `~.` output — and I ran it twice. `~..X` resolves to nothing, silently. |
| Malformed RST tables | 4 | Cells names outgrew their column rules. Docutils rejects the *whole* table, so each one lost the notes-symbol-to-cells mapping that is the most useful thing on the page. |
| Aligned two-column blocks | 6 | `` ``"IN FORCE"``  the account value… `` reads as a paragraph plus a block quote. Converted to RST definition lists, which is the construct for it. |
| Links to non-documents | 3 | `tests/conftest.py`, `requirements.txt` — real files, not Sphinx pages. Now inline code. |
| Directory links | 3 | `../universal_life` is not a document; MyST needs the page. |
| Heading-anchor links | 4 | Slug links in `whole_life/model.md`. Replaced with explicit targets — a slug dies silently when its heading is reworded. |
| `:func:` on a Reference | 1 | `trigger_rate` is a module-level assignment, not a cells; the corpus spells References as inline literals. |
| `\|legs\|` | 1 | Read by RST as a substitution reference. |
| Inline literal | 1 | `` ``AV + M >= `` `` — a literal may not have whitespace before its closing backticks. |

The 38 double dots are the lesson worth keeping: a non-idempotent fixer plus a silent
failure mode meant that running the tool *twice* was worse than not running it at all, and
nothing but `-n` would have said so.

**P7 — Merge dossier** — **done**, as [MERGE.md](MERGE.md), with the code for each step.

The D8 dry-run against `uk/` ran at the end of this phase and is the evidence that the
conventions generalize: `add_citation_anchors.py uk` reports **151 product entries + 38
reference-library entries**, matching §6's prediction exactly, and `separate_citations.py uk`
handles **1,472** adjacencies with nothing left for manual review — the nesting-aware scanner
and the widened separator set, both of which the uslib run forced, cover uk's cases too.

The lifelib-side edits, none of which are in scope for this repo:

1. `setup.py` — add `'md'` to `get_package_data`'s extension list (C5). Without this the
   docs never reach an installed copy.
2. `setup.py` — raise `install_requires` to `modelx>=0.32` (C6).
3. `doc/source/conf.py` — the doc-sync hook (D3), written to discover **every**
   `libraries/*/index.md` rather than naming `uslib` (D8), plus
   `exclude_patterns += ['libraries/*/_research/*']` (D6).
4. `doc/source/libraries/index.rst` — one table row and one toctree entry, `uslib/index.md`.
5. `.gitignore` — `doc/source/libraries/uslib/`, one line per library (D8: this one cannot
   be globbed, because hand-written library doc dirs live in the same parent).
6. ~~Move `tests/` → `lifelib/libraries/uslib/tests/`~~ — **already done in P2.** The suite
   is at `us/tests/` and travels with the directory, so the merge has nothing to do here.
   No CI or `tox.ini` change is needed either: both run bare `pytest` from the repository
   root, which already collects `ifrs17a`'s in-library tests.
7. `doc/source/conf.py` — nothing further for D9: `autodoc`, `autosummary` and `napoleon`
   are already loaded, `autodoc_member_order = 'bysource'` is already set, and
   `lifelib/libraries` is already on `sys.path`. The twelve `model-api.md` arrive through
   the same `*.md` sync as every other document.

Items 1–3 are **one-time, library-agnostic** work: once done, uklib needs only items 4 and 5
plus its own content — and, when its models are written, nothing at all for D9.

---

## 5. What this is worth checking against

The acceptance criteria for the prep branch, in order of how much they would hurt if wrong,
with what each returned:

| # | Criterion | Result |
|---|---|---|
| 1 | `sphinx-build -n -W --keep-going` over the uslib tree is clean (P6) — the `-n` is what makes 3 and 6 enforceable rather than aspirational | **75 documents, 0 warnings** |
| 2 | `pytest` is green — all twelve worked examples still reproduce | **1,010 passed, 14 skipped** |
| 3 | Every `[S#]`/`[R#]`/`[REG-R#]` in a rendered page is a link landing on that number **in that product's** `sources.md` — C11 is where a namespacing slip shows up as a plausible-looking *wrong* link | **12,576 internal anchor links resolve, 0 broken**, checked by walking the built HTML end to end rather than spot-checking |
| 4 | No `][` adjacency survives in any document carrying a definition block | **0**, per `tools/md_lint.py` |
| 5 | `git log --follow` still works on the moved documents | Pass, with one exception — below |
| 6 | All twelve `model-api.md` render and every `:mod:`/`:func:` role in the 1,581 cells docstrings resolves | Pass; under `-n` this is criterion 1 |

Criterion 3 is worth a note on method. Spot-checking would have confirmed that the links
*exist*; walking every `href="…#anchor"` in the built HTML against the ids actually present
on the target page confirms they **arrive**. Sphinx normalises label underscores to hyphens
when it emits ids — `uslib-term_life-s6` becomes `uslib-term-life-s6` — so a check written
against the label text rather than the rendered id would have reported a false failure, and
a subtler normalisation mismatch would have produced 12,576 links that all looked right and
went nowhere.

**The exception to criterion 5:** `us/tests/conftest.py` needs
`git log --follow -M20%` to trace its history, because P2 moved and substantially rewrote it
in the same commit and the default 50% similarity threshold does not recognise the rename.
The rename *is* recorded — `git show --stat` prints `{tests => us/tests}/conftest.py` — so
nothing is lost, but the move and the rewrite should have been separate commits. Every other
moved file follows at the default threshold.

---

## 6. Inventory

Measured with fenced code blocks excluded. The `uk/` column is not scope for this branch —
it is the **expected output of the same tooling** when D8's dry-run is performed, and the
check that no script has hardcoded "us".

| Quantity | `us/` | `uk/` |
|---|---|---|
| markdown files | 69 | 31 |
| — of which product docs | 36 (12 × 3) | 21 (7 × 3) |
| — model READMEs | 12 | 0 |
| — `_research` | 19 | 8 |
| modelx models | 12 | 0 (roadmap) |
| `[S#]` | 7,587 | 3,700 |
| `[R#]` | 2,089 | 619 |
| `[REG-R#]` | 1,008 | 159 |
| `[std]` | 1,257 | 684 |
| `[unverified]` | 275 | 143 |
| source entries needing a target | 237 | 151 |
| reference-library entries needing a target | 90 (within a frozen R1–R157) | 38 |
| bracket adjacencies `][` | 2,894 in 52 files | 1,947 |
| — plain tag ` ][ ` plain tag (scripted) | 2,064 | 1,109 |
| — cite-ish (scripted) | 93 | 275 |
| — needing manual review | 3 | 9 |
| pinpoint cites to linkify (D5) | 381 | 768 |
| comma lists to split (D5) | 91 | 1 |
| existing relative `.md` links | 63 | 12 |
| existing link reference definitions | **0** | **0** — no collision risk either side |
| backticked `…/….md` paths in prose | 478 | — |
| path strings in model `*.py` | 82 | 0 |
| path strings in `tests/*.py` | 40 | 0 |

Two asymmetries matter. `uk/` has **twice the pinpoint cites** of `us/` despite being half
the size, so D5 is the part of the pipeline most likely to be under-tested by the uslib run
alone. And `uk/` has three times the proportion of adjacencies needing manual review (9
versus 3) — small in absolute terms, but it means the manual-review bucket is a real step in
the process, not a rounding error to be scripted away.

---

## 7. The three citation layers

The library carries three distinct layers, and several decisions above turn on telling them
apart. All three use `S#`/`R#` identifiers; only the third is globally unique.

| Layer | Role | Per entry | Files | Entries |
|---|---|---|---|---|
| `_research/<product>.md` | **provenance** — where each fact came from | metadata **+ extracted facts**, plus "Extracted specifications", insurer variations, gaps | 19, 1.6 MB | 247 |
| `products/<product>/sources.md` | **bibliography** — what the two published documents cite | metadata only: publisher, doc type, URL, retrieved yes/no | 12, 344 KB | 237 |
| `references/regulatory-and-actuarial-references.md` | **cross-product library**, cited as `[REG-R#]` | full annotations, relevance matrices | 1 | 90 live, numbered within a frozen R1–R157 |

Numbering is **inherited, never reassigned**. A `[S6]` in `technical-notes.md` resolves to
S6 in that product's `sources.md` for *what the document is*, and to S6 in
`_research/<product>.md` for *what was extracted from it*. The `sources.md` entry is the
same entry with the facts block removed, and uncited sources dropped (each named as
dropped). The 247 → 237 difference is those drops, partly offset by `REG-R` entries added
at review from the cross-product library.

Three consequences for this plan:

- **Anchors go in the second and third layers** — 237 targets in the twelve `sources.md`,
  90 in the reference library (P3). The first layer gets none.
- **Targets must be namespaced per product** (D4/C11): `S1` is Protective Life in
  `term_life` and Symetra in `universal_life`.
- **`_research/` is not rendered** (D6): a second, deliberately independent `S1` in front of
  a reader is worse than no page at all.

One wrinkle for the P3 script, present in both of the first two layers: entry headings use
two conventions — `### S1 — Title` in `term-life` and `whole-life`, `### S1. Title` in the
other ten.

---

## 8. Decisions taken, and what is left

All questions raised in the first draft are now settled:

| Question | Ruling | Where |
|---|---|---|
| Do pinpoint cites and comma lists become links? | Yes, both | D5 |
| Do `[std]` / `[unverified]` become links? | Yes | D5a |
| Is `uk/` destined for `uklib`? | Yes — so every convention here is a house convention and every script is parameterized | D8 |
| Where do the tests live? | Inside the library, `libraries/uslib/tests/` | D7 |
| Does `_research/` ship? | Yes, in the library; not rendered | D6 |
| Do the models get autodoc API pages? | Yes — a `model-api.md` per product | D9 |

Nothing is blocking. One item is deliberately deferred rather than open:

1. **The uklib migration itself.** Out of scope for this branch. D8 fixes the conventions
   and requires the tooling to be general, and §6 gives the numbers its dry-run must
   reproduce — so the uklib run should be a re-invocation, not a redesign. The one piece of
   genuinely new authoring it will need is its own copy of the citation-conventions section,
   for the same reason uslib needs one: the shared root `README.md` that currently defines
   them for both does not survive the split.
