```{module} delib
```

# The **delib** Library

```{warning}
{mod}`delib` is in its draft stage, and its contents are subject to change as development
continues.
```

## Overview

The **delib** library packages **ten reference liability cash flow projection models** for
the individual life, pension and biometric-risk products sold in Germany, built with
modelx, and, for each one, the product specification and technical notes the model was
built from.

The coverage follows the German market rather than a template, and the shape it follows is
the **Drei-Schichten-Modell** the *Alterseinkünftegesetz* imposed on German retirement
saving in 2005. Which layer a contract sits in decides more about it than what it invests
in: **Schicht 1** buys a deductible contribution and a fully taxed pension in exchange for
a product that may not be surrendered, commuted or assigned; **Schicht 2** buys a state
*Zulage* paid into the contract as a real cash flow in exchange for a statutory 100 %
*Beitragsgarantie*; **Schicht 3** buys the light *Ertragsanteil* taxation of a private
annuity and imposes nothing. So [basisrente](products/basisrente/index.md) and
[riester_rente](products/riester_rente/index.md) take a slot each, and four more go to the
Schicht-3 savings forms — the historic
[Kapitallebensversicherung](products/kapitallebensversicherung/index.md), the
[klassische Rentenversicherung](products/klassische_rentenversicherung/index.md) that
replaced it, the [fondsgebundene Rentenversicherung](products/fondsgebundene_rentenversicherung/index.md)
that dominates new business, and the [Indexpolice](products/indexpolice/index.md), a
German construction with no counterpart in the sister libraries. A seventh goes to the
[Sofortrente](products/sofortrente/index.md) they pay out into.

The last three are **Biometrie**, and one of them is the reason a German library looks
different from a French or a British one. The
[Berufsunfähigkeitsversicherung](products/berufsunfaehigkeit/index.md) is the country's
flagship protection product, written against a statutory definition of disability in
§ 172 VVG, and it outsells plain
[Risikolebensversicherung](products/risikolebensversicherung/index.md) in adviser
attention by a wide margin. [Pflegerentenversicherung](products/pflegerentenversicherung/index.md)
completes the set, sitting on top of the *soziale Pflegeversicherung* rather than replacing
it. **Betriebliche Altersversorgung** — *Direktversicherung*, *Pensionskasse*,
*Pensionsfonds*, *Unterstützungskasse* and *Direktzusage* — is out of scope, as is
*Gruppenversicherung*, the substitutive **private Krankenversicherung**, and
*Sterbegeldversicherung*.

The models are the centre of the library. Each is a by-model-point projection of one
product's gross liability cash flows: *Beiträge*, *Leistungen*, *Rückkaufswerte*, charges
and expenses, on the product's own processing order and timing. None of them discounts —
every model publishes the cash flows and leaves discounting, the *Deckungsrückstellung* and
capital to a layer that consumes them.

**Each one of these models reproduces a documented worked example, asserted cell by cell to
the precision the notes display**. The chain is deliberate and complete in both directions:

- `product-spec.md` specifies a *representative* product — a standardized composite built
  from publicly documented real products, not any single insurer's contract. It records
  contractual mechanics, a full parameter set, the observed variation across insurers, and
  the rationale for every representative choice.
- `technical-notes.md` turns that product into a liability cash flow model on paper: model
  point attributes, state variables, assumption inputs, the recursions with their explicit
  processing order, policyholder behaviour, and a numeric worked example.
- The **model** implements those notes, and the library's own `tests/` assert the worked
  example against it. Change an assumption, and the test tells you whether the model and
  the notes have parted company.
- `sources.md` lists every source the first two cite, with URLs where they are known,
  access dates and retrieval status.

Every quantitative parameter in the library is either **source-tagged** or marked
**[std]** — a standardization introduced for the reference implementation, carrying its
rationale and, where available, the observed range across insurers. Facts taken from source
material are never silently mixed with assumptions made to complete a model.

(delib-provenance)=

```{admonition} Read this before citing anything in this library
:class: danger

**No document cited anywhere in delib was retrieved.** The build environment blocks direct
HTTP egress to every host outside a package-registry allowlist — `gesetze-im-internet.de`,
`bafin.de`, `aktuar.de`, `gdv.de`, `bundesfinanzministerium.de`, `destatis.de`,
`dejure.org` and `eur-lex.europa.eu` were each tried and each refused at the gateway — and
the session's web-search budget was exhausted partway through the regulatory research.

The consequence is stated plainly rather than buried: **a delib citation is a pointer, not
a certificate.** It names the instrument a claim should be checked against; it does not
assert that anyone read it. The prudential and contract-law research files record, per
fact, what a search corroborated; the rest rests on the authoring model's own knowledge of
German insurance law and practice, and every specific paragraph number, effective date,
monetary amount and market figure that no search confirmed carries **[unverified]**.

This is a weaker provenance than the sister libraries have — frlib could read Légifrance in
full, and says so — and it is the first thing to fix if this library is developed further.
**Re-verify every factual claim against the cited instrument before relying on it.**
```

```{admonition} These are mechanics demonstrations, not pricing or reserving results
:class: warning

**Every biometric basis shipped here is a [std] proxy.** The tables a German insurer
actually prices and reserves on — **DAV 2008 T** for death cover, **DAV 2004 R** and its
*Bestand* variants for annuities, **DAV 1997 I** and **DAV 1997 TI** for *Berufsunfähigkeit*,
**DAV 2008 P** for *Pflege* — are the property of the Deutsche Aktuarvereinigung, are not
published openly, and are **cited by name throughout this library and never redistributed**.
Nor is there a public rate card: German pricing is quote-driven, and what a *Produktinformationsblatt*
must disclose is the contract's own figures rather than a tariff. Replace both with company
data before drawing any conclusion from the numbers.
```

## The models

Model names are `<product>_<country>_<grid>`: the short form the German market itself uses
where there is one — `KLV`, `RLV`, `BU` — a short descriptor where there is none, then
`DE`, then `_A` for an annual step or `_S` for a monthly one. The grid letters follow
lifelib, where `annuallife/TradLife_A` is the annual-step model and `basiclife/BasicTerm_S`
and `savings/CashValue_SE` are the monthly ones. `S` carries a second sense in lifelib —
scalar, one model point at a time, as against the vectorized `_M` models — and that is true
of all ten here, whether or not they carry the letter.

<!-- PRODUCT TABLES -->

(delib-one-shape)=

### One shape, enforced

Every model has the same two Spaces — `Data` reads the input CSVs once per model, and
`Projection` is parameterized by `point_id` — with inputs as **external** CSVs beside
`run.py`, so the model folder holds formulas and nothing else. `Projection`'s docstring
carries the mapping from the technical notes' actuarial symbols to the cells names.

That shape is asserted rather than merely described: `tests/test_model_conventions_de.py`
applies it to every model in the registry, and each model additionally has its own test
module for its worked example and its product-specific invariants — the notes' "Known
modeling pitfalls" sections are written up there as tests.

The pairing of model name to folder is deliberately *not* derivable from the folder name —
`fondsgebundene_rentenversicherung` spelled out is unusable in a model name — so it is
registered once in `tests/de_registry.py`, and the conventions suite asserts that the
registry, the directory on disk and the model's own `_name` all agree, along with the
country and grid tags.

The registry is per library; the contract it enforces is the one
[uslib is held to](#uslib-one-shape), and cells names come from lifelib —
`basiclife/BasicTerm_S` first, then `savings/CashValue_SE` — so a name means the same thing
here, in uslib, in uklib, in frlib and in lifelib. The
[shared vocabulary table](#uslib-shared-vocabulary) is the settled ruling across the
libraries, and delib takes frlib's reading of `proj_len()` with it: **`proj_len()` is the
last projected period index**, so `result_cf()` ends at `proj_len()` whether the frame is
0-based or 1-based.

(delib-own-rulings)=

### The two rulings this library added

Each library in this repository settles a convention of its own and asserts it rather than
describing it. delib settled two, and both are enforced by the conventions suite.

**`check_net_cf()` is required of every model.** A cash flow model's headline number is
`net_cf`, and until now it was the one quantity nothing checked: the roll-forward identities
the models publish check policy counts and account values, and the statement that reconciles
them into `net_cf` lived in prose. Every delib model publishes `check_net_cf()`, a bool over
all `t` that reconstructs `net_cf(t)` from the statement's own published parts, with the
per-period residual at `check_net_cf_resid(t)`. The *identity* is a product fact — a term
cover reconciles premiums less claims less expenses, a unit-linked contract has to cross the
unit / non-unit boundary to do it, and a payout annuity has no premium term at all — so each
`model.md` states its own in one line and the conventions suite asserts only that the cells
exists, has the `CashValue_SE` signature, and returns `True` on every model point. frlib
carried the name on five of its nine models; here it is the contract.

**Every assumption CSV carries a `provenance` column.** The hard rule of all five libraries
is that every quantitative parameter is either source-tagged or marked **[std]**. In the
prose that rule is enforced by review; in the shipped input files it was enforced by habit,
and habit is what a table added in a hurry escapes. Here it is a property of the library:
each row of each input CSV carries its own tag — `[S3]`, `[REG-R21]`, `[std]` with a short
rationale — and a file without a populated `provenance` column fails the suite.
`model_point_table.csv` is the single exemption, because a model point is a *configuration*
rather than an assumption: its columns are one policy's own terms, and tagging them row by
row would repeat the same fact once per policy while saying nothing about any assumption.

Given the retrieval conditions above, the second ruling earns its keep twice over. When a
citation is a pointer rather than a certificate, the least a library can do is put the
pointer next to the number.

(delib-germany-specific)=

### What is German about these models

<!-- GERMANY SPECIFIC -->

### Chassis relationships

<!-- CHASSIS -->

## How to use the library

Create your own copy of the *delib* library, as described in the
{ref}`create-a-project` section. For example, to copy it to *C:\\path\\to\\your\\delib*:

```python
>>> import lifelib

>>> lifelib.create("delib", r"C:\path\to\your\delib")
```

Each model reads from its own directory, so run one directly:

```bash
python products/klassische_rentenversicherung/run.py
```

or read it and take the cash flow statement:

```python
>>> import modelx as mx

>>> model = mx.read_model("products/klassische_rentenversicherung/RV_DE_A")

>>> model.Projection[1].result_cf()
```

`Projection` takes a `point_id`; `Projection[1]` is each model's worked-example anchor cell.
`result_cf()` returns a tidy `DataFrame` indexed by `t` with one column per cash flow line.

The tests ship inside the library and run against *your* copy:

```bash
python -m pytest tests -q
```

## Library contents

```{list-table}
:header-rows: 1
:widths: 28 72

* - File or folder
  - Description
* - `products/<product>/`
  - One directory per product, holding its documents *and* its model together. Ten of them.
* - `products/<product>/product-spec.md`
  - The representative product specification: mechanics, parameters, variation across insurers.
* - `products/<product>/technical-notes.md`
  - The liability cash flow model on paper: state variables, recursions, processing order, worked example.
* - `products/<product>/model.md`
  - How the model implements those notes — what was standardized, what diverges, what the tests cover.
* - `products/<product>/sources.md`
  - Every source the product's documents cite, with URLs where known, access dates and retrieval status.
* - `products/<product>/<Model>/`
  - The modelx model itself. Formulas only — no embedded data.
* - `products/<product>/*.csv`
  - The model's inputs, external to the model folder so they can be edited or swapped in place. Every assumption file carries a `provenance` column.
* - `products/<product>/run.py`
  - Reads the model and prints its cash flow statement.
* - `references/`
  - The cross-product regulatory and actuarial bibliography, cited as `[REG-R#]`.
* - `tests/`
  - One module per model for its worked example and invariants, plus `test_model_conventions_de.py` for the house style, and `de_registry.py` carrying the model registry.
* - `_research/`
  - The raw research notes every citation traces back to. Provenance, not documentation — shipped but not rendered.
```

`_research/` carries one file per product plus `regulatory-actuarial.md`, and records what
each source is and what could be established about it. Its source lists are **never
renumbered**: the product documents cite against them.

(delib-citation-conventions)=

## Citation conventions

Whether a citation tag is a link tells you what kind of source it is. `[R1]` and
`[REG-R18]` are links: the first lands on entry R1 in **that product's** `sources.md`, the
second on entry R18 of the shared
[reference library](references/regulatory-and-actuarial-references.md). `[S6]` is not a
link. It stays on the page as you see it, brackets and all, and names entry S6 in that
product's `sources.md` for you to look up.

That asymmetry is deliberate, and it is the same line the `sources.md` files draw between
their own sections. A regulatory or actuarial reference is an **authority** the model is
held to, and following it is part of reading the document. A primary product source is a
**specification** citation — the *Allgemeine Versicherungsbedingungen*,
*Produktinformationsblatt* or *Basisinformationsblatt* a number was taken from — which says
where a figure came from rather than what the model must obey. So one reads as a tag on the
page and the other as a link off it.

Numbering is per product — S1 is a different source in each — so tags resolve against the
document's own product rather than one global list.

| Tag | On the page | Meaning |
|---|---|---|
| `[S#]` | bracketed text | Fact taken from a primary product document (*Allgemeine Versicherungsbedingungen*, *Produktinformationsblatt*, *Basisinformationsblatt* (PRIIP-KID), *Verbraucherinformation*, *Tarifblatt*, *Musterrechnung*) listed in the product's `sources.md` |
| `[R#]` | link | Fact taken from a product-specific regulatory/actuarial reference in the product's `sources.md` |
| `[REG-R#]` | link | Fact taken from the cross-product reference library (frozen R-numbering) |

(delib-std)=

**[std]** — a *standardization introduced for the reference implementation*: a parameter or
convention chosen where sources vary, are proprietary, or are silent. Each carries a
rationale and, where available, the observed range across insurers.

(delib-unverified)=

**[unverified]** — a claim from general knowledge or a secondary snippet that could **not**
be confirmed against a retrieved document. Treat it as a to-verify item, not an established
fact. Under this library's [retrieval conditions](#delib-provenance) the tag does more work
than it does in the sister libraries, and it is applied to every specific paragraph number,
effective date, monetary amount and market figure that no web search corroborated.

The hard rule throughout: **every quantitative parameter is either source-tagged or marked
[std]**. In this library that rule does most of its work on the biometric bases, which are
**[std]** proxies throughout because the DAV tables are proprietary, and on the charge and
premium levels, because German pricing is quote-driven and no public rate card exists.

## Regulatory and actuarial reference library

<!-- REFERENCE LIBRARY PARAGRAPH -->

## Known gaps and caveats

<!-- GAPS -->

```{toctree}
:hidden:
:maxdepth: 1
:caption: Products

products/kapitallebensversicherung/index
products/klassische_rentenversicherung/index
products/fondsgebundene_rentenversicherung/index
products/indexpolice/index
products/basisrente/index
products/riester_rente/index
products/sofortrente/index
products/risikolebensversicherung/index
products/berufsunfaehigkeit/index
products/pflegerentenversicherung/index
```

```{toctree}
:hidden:
:maxdepth: 1
:titlesonly:
:caption: Reference

references/regulatory-and-actuarial-references
```
