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

### D5 — Two citation forms need an explicit ruling

Neither becomes a link under D4, because their bracket text is not a bare label:

- **Pinpoint cites** — `[R1 §4.B]`, `[R13 §3.B(1)(b)]`: 381 occurrences, 234 distinct.
- **Comma lists** — `[S3, S7]`, `[S3, S5, S7]`: 93 occurrences, 44 distinct.

Recommendation: split the comma lists (`[S3], [S7]` — 93 sites, mechanical, they become
links for free) and convert the pinpoint cites to explicit inline links
(`[R1 §4.B](#uslib-term_life-r1)` — 381 sites, scripted from the leading tag). Both are in
scope for "all cross-references are links"; both are also the most defensible place to
descope if the diff proves too large. **Flagged for your call — see §7.**

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

---

## 4. Prep phases, in this repository

Each phase is a commit on `uslib-merge-prep`, with `python -m pytest tests -q` green at the
end of every one.

**P0 — Structural markdown fixes** *(3 files)*
Independent of everything else; fixes latent rendering bugs that exist today.
- `us/references/regulatory-and-actuarial-references.md:1683` — a `---` line directly
  follows `payout mortality.` with no blank line, so MyST renders that sentence as an
  **H2 heading**. Insert a blank line.
- `us/products/fixed-indexed-annuity/sources.md:324` — H2 → H4 jump
  (`myst.header` warning). Insert the missing level or demote.
- `us/README.md` — `<product-type>`, `<product>`, `<country>`, `<grid>` appear bare in
  prose and parse as raw HTML tags. Wrap in backticks.

**P1 — Directory restructure** *(pure `git mv`, no content edits)*
- Rename the 12 product slugs to underscores (D1) in `us/products/`.
- Move each `us/models/<p>/` into `us/products/<p_>/`; `README.md` → `model.md`.
- Delete the now-empty `us/models/`, and the stray empty `us/regulatory/` (an untracked
  leftover of the framework revert in 832247f — `uk/regulatory/` is the same and can go
  with it).
- Nothing builds or passes at the end of this phase except `git status`; P2 is its
  other half and the two may be squashed if you prefer a single reviewable move.

**P2 — Path rewrites** *(mechanical, scripted)*

| Where | What | Count |
|---|---|---|
| model `*.py` docstrings | `us/models/<hyphen>` and `us/products/<hyphen>` → `uslib/products/<underscore>` | 82 |
| `tests/*.py` | model paths in the `MODELS` registry and per-model tests | 40 |
| `*.md` prose | backticked `` `us/…​.md` `` paths | 478 |
| `*.md` prose | backticked `` `tests/…` `` paths | 16 |
| `*.md` | `python us/models/<p>/run.py` invocations | 20 |
| `*.md` | relative `.md` links — slug rename, plus `../../products/x/` → `../x/` now that models sit inside `products/` | 63 |

The 478 backticked paths are prose references to sibling documents. Per the third goal they
should become **links**, not merely corrected strings — do that here, while the paths are
being touched anyway.

**P3 — Citation anchors** *(targets only; no citation links yet)*
Insert `(uslib-<product>-s<n>)=` / `(uslib-<product>-r<n>)=` above each of the **237** source
entries in the twelve `sources.md`, and `(uslib-reg-r<n>)=` above each of the **90** entries
in `references/regulatory-and-actuarial-references.md` (numbering runs to R157, but the
retired R73–R149 block leaves only 90 live entries — the frozen numbers are what the targets
must carry, not the ordinal position). Add the conventions targets to `us/README.md`.

Watch for this: the entry headings use **two conventions** —
`### S1 — Title` in `term-life`, `### S1. Title` in the other eleven. The insertion script
must match both, and the count above is the check that it did.

**Idempotent and inert** — nothing links to these targets yet, so this phase cannot change
any rendering.

**P4 — De-adjacency** *(2,157 scripted sites + 3 manual)*
Per D4. Still inert — with no definitions in place, `[S2] [S3]` renders as literal text just
as `[S2][S3]` does. This phase is deliberately separate so its diff can be reviewed on its
own; it is the one that would silently corrupt meaning if it were incomplete.

**P5 — Citation link definitions** *(the phase that turns citations into links)*
Add `tools/gen_citation_links.py`, run it over the 36 product documents and the 12
`model.md`, and commit the generated blocks. Add a test asserting round-trip integrity:
every tag used has a definition, every definition has a target, no target is defined twice.
Optionally (D5) split comma lists and linkify pinpoint cites.

**P6 — Sphinx scaffolding, authored in the library tree**
- `us/README.md` → `us/index.md` with a MyST toctree.
- New `us/products/index.md` (the two taxonomy tables from the README, plus a toctree).
- New `us/products/<p>/index.md` × 12.
- **Each of the twelve `model.md`: a "Verification" note** saying which module in `tests/`
  asserts that model's worked example, what it covers, and the one command that runs it
  against *this* copy. Required by D7: the suite ships with the library, so a reader who
  edits an assumption has a way to find out whether they broke the documented example —
  but only if the documents tell them it exists.
- A `doc-check` harness: a throwaway `conf.py` mirroring lifelib's MyST settings, so the
  whole set can be built **here** with `-W --keep-going` and land in lifelib warning-clean.
  This is the acceptance test for the whole plan.

**P7 — Merge dossier**
A short `MERGE.md` recording the lifelib-side edits that are *not* in scope for this repo:

1. `setup.py` — add `'md'` to `get_package_data`'s extension list (C5). Without this the
   docs never reach an installed copy.
2. `setup.py` — raise `install_requires` to `modelx>=0.32` (C6).
3. `doc/source/conf.py` — the `_sync_uslib_docs` hook (D3) and
   `exclude_patterns += ['libraries/uslib/_research/*']` (D6).
4. `doc/source/libraries/index.rst` — one table row and one toctree entry, `uslib/index.md`.
5. `.gitignore` — `doc/source/libraries/uslib/`.
6. Move `tests/` → `lifelib/libraries/uslib/tests/` (D7) — inside the library, following
   `ifrs17a`. No CI or `tox.ini` change is needed.
7. Decide whether the twelve models also get lifelib-style autodoc pages
   (`.. automodule:: uslib.products.term_life.Term_US_A.Projection`). D1 keeps the door
   open; nothing else in this plan depends on it.

---

## 5. What this is worth checking against

The acceptance criteria for the prep branch, in order of how much they would hurt if wrong:

1. `sphinx-build -W --keep-going` over the uslib tree is clean (P6).
2. `python -m pytest tests -q` is green — all twelve worked examples still reproduce.
3. Every `[S#]`/`[R#]`/`[REG-R#]` in a rendered page is a link, and it lands on the entry
   with that number **in that product's** `sources.md`. Spot-check across products, since
   C11 is where a namespacing slip would show up as a plausible-looking wrong link.
4. No `][` adjacency survives in any document that carries a definition block.
5. `git log --follow` still works on the moved documents (use `git mv`, keep P1 rename-only).

---

## 6. Inventory

Measured across the 69 markdown files under `us/`, with fenced code blocks excluded.

| Quantity | Count |
|---|---|
| markdown files | 69 (36 product docs, 12 model READMEs, 19 `_research`, `us/README.md`, references) |
| modelx models | 12 |
| `[S#]` | 7,587 |
| `[R#]` | 2,089 |
| `[REG-R#]` | 1,008 |
| `[std]` | 1,257 |
| `[unverified]` | 275 |
| source entries needing a target (12 × `sources.md`) | 237 |
| reference-library entries needing a target | 90 (numbered within R1–R157) |
| distinct bracket tokens (all kinds) | 683 |
| bracket adjacencies `][` | 2,894 in 52 files |
| existing relative `.md` links | 63 |
| existing link reference definitions | **0** — no collision risk |
| backticked `us/….md` paths in prose | 478 |
| path strings in model `*.py` | 82 |
| path strings in `tests/*.py` | 40 |

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

## 8. Open questions

1. **D5 — pinpoint cites and comma lists.** Linkifying `[R1 §4.B]` (381 sites) and
   splitting `[S3, S7]` (93 sites) is the difference between "most cross-references are
   links" and "all of them are". It is also the only part of the plan that alters the
   *visible* text of a citation. Include, or leave as plain text?
2. **`[std]` / `[unverified]` as links.** 1,532 occurrences would become links to the
   conventions section. Consistent, and one definition line per file — but noisy. Link
   them, or keep them as plain markers and link only true citations?
3. **`uk/`.** Out of scope here. Worth deciding now whether it is destined to become
   `uklib` on the same pattern, because if so, the `uslib-` target prefix and the
   `products/<product>/` shape should be chosen as a house convention rather than a
   one-off.

*Settled since the first draft:* tests and `_research/` both stay inside the library, so a
`create()` copy is self-contained — see D6 and D7.
