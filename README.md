# lifelib-products

A library of **product specifications for major life insurance products, organized by
country**, together with the documentation needed to build **reference implementations
of liability cash flow projection models** (lifelib/modelx style), organized by product
type and country.

**Status:** Draft, 2026-08-03. Current coverage: United States (6 individual life
product types) and United Kingdom (7 product types, including pension annuities).
Reference model implementations are a planned follow-on (see Roadmap).

---

## Organization

```
<country>/
  README.md                          country overview and product taxonomy
  products/
    <product-type>/
      product-spec.md                representative product specification
      technical-notes.md             liability cash flow model: design, assumptions, recursions
      sources.md                     numbered source list for this product's documents
  references/
    regulatory-and-actuarial-references.md
                                     curated cross-product bibliography (NAIC, IRC, SOA, AAA, ASB)
  _research/                         raw research notes — citation ground truth / provenance
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
| [United States](us/README.md) | term life, whole life, universal life, indexed UL, variable UL, guaranteed UL | specs + technical notes drafted |
| [United Kingdom](uk/README.md) | term assurance, critical illness, income protection, whole of life, with-profits, unit-linked bond, pension annuity | specs + technical notes drafted |

Scope note: the U.S. section covers individual life insurance only (individual
annuities deferred to a future section); the UK section additionally includes pension
annuities, which are core long-term insurance business for UK life insurers — see
[uk/README.md](uk/README.md) for the rationale.

## Roadmap

- **Reference implementations**: `<country>/models/<product-type>/` — executable
  liability cash flow projection models built from the technical notes.
- **Additional countries** and additional product families (individual annuities,
  group insurance) as separate sections.

## Disclaimer

This library is technical documentation for modeling purposes. The representative
specifications are standardized composites and do not describe any insurer's actual
contract; nothing here is insurance, investment, tax, or legal advice.
