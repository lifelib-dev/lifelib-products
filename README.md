# lifelib-products

A library of **product specifications for major life insurance products, organized by
country**, together with the documentation needed to build **reference implementations
of liability cash flow projection models** (lifelib/modelx style), organized by product
type and country.

**Status:** Draft, 2026-08-14. Current coverage: United States (6 individual life and
6 individual annuity product types) and United Kingdom (7 product types, including
pension annuities). **All twelve U.S. products now ship an executable reference model**
in `uslib/products/<product>/`, beside the documents that specify it; the UK models are
a planned follow-on (see Roadmap).

---

## Organization

```
<library>/                           uslib/ — a country library, named for the lifelib library it becomes
  index.md                           country overview, product taxonomy, citation conventions
  products/
    index.md
    <product>/                       each product's documents and its executable model, together
      product-spec.md                representative product specification
      technical-notes.md             liability cash flow model: design, assumptions, recursions
      model.md                       how the model implements the notes, and what is [std]
      model-api.md                   cells reference, generated from the model's docstrings
      sources.md                     numbered source list for this product's documents
      run.py  *.csv  <Model>/        the modelx model and its inputs
  references/
    regulatory-and-actuarial-references.md
                                     curated cross-product bibliography (NAIC, IRC, SOA, AAA, ASB)
  tests/                             one module per model, plus the shared conventions suite
  _research/                         raw research notes — citation ground truth / provenance
```

`uslib/` is in this shape and ready to merge into lifelib — see
[USLIB-MERGE-PLAN.md](USLIB-MERGE-PLAN.md) and [MERGE.md](MERGE.md). `uk/` is still a country
section in the older layout (`products/<product-type>/` with hyphenated slugs, no models) and
becomes `uklib/` on the same pattern.

## Building the documentation

The documents live beside the models they describe rather than under `doc/`, and are
mirrored into the doc tree at build time by a hook in `doc/source/conf.py` — the same
arrangement they will have inside lifelib. Any library with an `index.md` is picked up.

```bash
cd doc && make html
```

To hold the documents to the standard they have to meet — every warning an error, and
**nitpicky**, without which an unresolved `:func:`/`:mod:` role is dropped silently rather
than reported:

```bash
python tools/doccheck.py
```

That is 80 pages, and it should report zero. Run the model suite with:

```bash
python -m pytest uslib/tests -q
```

- **`product-spec.md`** defines a *representative* product: a standardized composite
  built from publicly available documentation of real products, not any single
  insurer's contract. It records contractual mechanics, a full parameter set, observed
  variations across insurers, and the rationale for each representative choice.
- **`technical-notes.md`** specifies the liability cash flow projection model for that
  product: model point attributes, state variables, assumption inputs, cash flow
  recursions with explicit processing order, policyholder behavior, a numeric worked
  example, valuation pointers, and key sensitivities.
- **`sources.md`** lists every source cited by that product's documents, with URLs,
  access dates, and whether the document was actually retrieved.
- **`_research/`** holds the underlying research notes. Every sourced fact in the
  product documents traces back to a source entry in these files. They are provenance:
  keep them, do not renumber their source lists.

## Citation conventions

Used uniformly across the library:

| Tag | Meaning |
|---|---|
| `[S#]` | Fact taken from a primary product document (brochure, specimen policy, prospectus, producer guide) listed in the product's `sources.md` |
| `[R#]` | Fact taken from a product-specific regulatory/actuarial reference in the product's `sources.md` |
| `[REG-R#]` | Fact taken from the cross-product reference library `references/regulatory-and-actuarial-references.md` (frozen R-numbering) |
| **[std]** | A *standardization introduced for the reference implementation* — a parameter or convention chosen where sources vary, are proprietary, or are silent. Each carries a rationale and, where available, the observed range across insurers |
| `[unverified]` | A claim from general knowledge or a secondary snippet that could **not** be confirmed against a retrieved document — treat as a to-verify item, not an established fact |

The hard rule throughout: **every quantitative parameter is either source-tagged or
marked [std]** — information taken from source materials is never mixed silently with
assumptions introduced for the representative specification.

## Methodology

Each country section is built in three passes:

1. **Research** — per product type, collect primary product documentation (insurer
   brochures and product guides, specimen policy forms, SEC prospectuses where the
   product is registered) and the governing actuarial/regulatory references (NAIC
   model laws and actuarial guidelines, the Valuation Manual, IRC provisions, SOA
   experience studies, AAA practice notes, ASOPs). Everything lands in `_research/`
   with per-source fact extraction and explicit fetch-failure notes.
2. **Drafting** — write the product spec and technical notes from the research files
   under the citation discipline above, choosing and justifying a representative
   design where insurers differ.
3. **Review** — an adversarial pass per product (citation integrity against the
   research files, recomputation of all formulas and worked examples, internal
   consistency), then a cross-product consistency pass (shared terminology, shared
   base-chassis mechanics, link and tag integrity).

## Coverage

| Country | Products | Status |
|---|---|---|
| [United States](uslib/index.md) | **Life:** term life, whole life, universal life, indexed UL, variable UL, guaranteed UL<br>**Annuity:** fixed deferred (MYGA), fixed indexed, variable, registered index-linked (RILA), immediate (SPIA), deferred income (DIA/QLAC) | specs + technical notes drafted |
| [United Kingdom](uk/README.md) | term assurance, critical illness, income protection, whole of life, with-profits, unit-linked bond, pension annuity | specs + technical notes drafted |

Scope note: both country sections cover individual life insurance and annuities, but
the annuity coverage differs by market. The U.S. section covers the individual deferred
and payout annuity families sold at retail; the UK section covers pension annuities,
which are the dominant UK annuity form and the centrepiece of the Solvency UK matching
adjustment — see [uk/README.md](uk/README.md). Group insurance and institutional
business (bulk purchase annuities, pension risk transfer) are out of scope in both.

## Roadmap

- **Reference implementations**: `<library>/products/<product>/` — executable liability
  cash flow projection models built from the technical notes. **All twelve U.S. products
  are shipped** (modelx; each one's worked example is asserted cell by cell by the
  library's own `tests/`, and a shared conventions suite enforces the house style across
  the set — see [uslib/index.md](uslib/index.md#executable-models)). The seven UK products
  follow the same pattern.
- **Additional countries**, and additional product families (group insurance,
  institutional/pension risk transfer business) as coverage grows.

## Disclaimer

This library is technical documentation for modeling purposes. The representative
specifications are standardized composites and do not describe any insurer's actual
contract; nothing here is insurance, investment, tax, or legal advice.
