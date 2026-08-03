# United States — Individual Life Insurance Reference Products

**Status:** Draft, 2026-08-03 (all cited sources accessed 2026-08-03).

This section covers the major **individual life insurance** product types sold in the
U.S. market. Individual annuities (fixed, indexed, variable) and group insurance are
out of scope here and are planned as separate sections.

## Product taxonomy

| Product type | Folder | Representative design (one line) |
|---|---|---|
| Level premium term | [term-life](products/term-life/product-spec.md) | Guaranteed level premiums for 10/20/30 years, then jump-to-ART renewal at unchanged face to attained age 95; convertible to permanent until min(end of level period, age 70); no cash value |
| Whole life | [whole-life](products/whole-life/product-spec.md) | Participating level-premium WL on a 2017 CSO / 4% nonforfeiture basis with three-factor contribution dividends and paid-up-additions default; limited-pay variants; plus a non-par simplified-issue final-expense variant |
| Universal life | [universal-life](products/universal-life/product-spec.md) | Flexible-premium current-assumption UL: monthly deductions (per-policy + per-unit + COI on NAAR), declared portfolio crediting over a guaranteed minimum, GPT corridor, DB options A/B — the **base chassis** for the three products below |
| Indexed UL | [indexed-ul](products/indexed-ul/product-spec.md) | UL chassis + S&P 500 (price return) annual point-to-point index account with cap, 100% participation, 0% floor — the AG 49-A benchmark-index-account design |
| Variable UL | [variable-ul](products/variable-ul/product-spec.md) | UL chassis + unitized separate-account subaccounts and a fixed option; SEC-registered, so charges are anchored on EDGAR prospectus fee tables |
| Guaranteed UL (ULSG) | [guaranteed-ul](products/guaranteed-ul/product-spec.md) | UL chassis + shadow-account secondary guarantee (AG 38 §8E Policy Design #1): policy stays in force while the shadow account is positive, funded by a solved level no-lapse premium; lapse-supported economics |

Each folder contains `product-spec.md` (representative specification, variations
across insurers, regulatory context), `technical-notes.md` (liability cash flow model:
model points, state variables, assumptions, recursions with processing order, worked
example, sensitivities), and `sources.md` (numbered source list). Citation conventions
are defined in the [top-level README](../README.md).

The UL-family documents (indexed, variable, guaranteed) reference the
[universal-life technical notes](products/universal-life/technical-notes.md) for the
shared base-chassis recursion, which is anchored on a retrieved specimen policy;
deviations (e.g., VUL's prospectus-sourced NAAR convention) are explicitly flagged
where they occur rather than silently restated.

## Regulatory and actuarial reference library

[references/regulatory-and-actuarial-references.md](references/regulatory-and-actuarial-references.md)
is the curated cross-product bibliography (frozen numbering R1–R34, cited from product
documents as `[REG-R#]`), with a product-relevance matrix. It spans the NAIC statutory
framework (Standard Valuation Law, Standard Nonforfeiture Law, Valuation Manual /
VM-20, Models 582/585/787/830, AG 38/48/49/49-A/49-B), federal tax (IRC §§ 7702,
7702A, 807, 817), mortality tables and experience studies (2017 CSO, 2015 VBT, ILEC
mortality, SOA persistency and post-level-term studies), AAA practice notes, ASOPs
(2, 7, 15, 22, 24, 52, 56), and accounting frames (statutory / GAAP LDTI / tax).

## Provenance

`_research/` holds the raw research notes (one file per product plus
`regulatory-actuarial.md`): the per-source fact extraction that every citation in the
product documents traces back to, including explicit records of which documents were
actually retrieved and which fetches failed. Do not renumber their source lists —
product documents cite against them.

## Known gaps and caveats

The significant ones, aggregated from the per-product research (each product's
documents and research file carry the full list):

- **Current non-guaranteed scales are not public.** Declared crediting rates, current
  COI scales, and IUL caps/participation rates are either producer-portal-only or
  point-in-time snapshots; the reference specs carry **[std]** values calibrated to
  observed ranges. Guaranteed elements (CSO-capped COI, minimum interest, maximum
  loads) are far better sourced.
- **Full rate/charge tables are largely proprietary.** Complete COI tables per $1,000,
  per-unit charge scales, and surrender-charge dollar schedules generally live in
  policy data pages and illustration systems. Exceptions captured here: a complete
  guaranteed COI table and processing order from a UL specimen policy, a complete
  guaranteed premium schedule from a term specimen, final-expense WL premium rates per
  $1,000, and VUL prospectus fee tables.
- **ULSG shadow-account parameters are unobservable.** No public document discloses
  shadow-account loads/credits/charges; the guaranteed-ul reference parametrization is
  wholly **[std]**, calibrated so the solved no-lapse premium resembles observed
  market premiums.
- **Era mixing.** Some retrieved specimen documents are 2001-CSO-era while the
  representative specs are stated on a 2017 CSO basis; the documents disclose this
  wherever it occurs.
- **[unverified] items remain.** Claims that could not be confirmed against a
  retrieved document (e.g., age-121 maturity mechanics for IUL, certain conversion
  window details, the FASB LDTI primary text) are tagged `[unverified]` wherever used.
