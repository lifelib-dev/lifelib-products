# United Kingdom — Life Insurance Reference Products

**Status:** Draft, 2026-08-03 (all cited sources accessed 2026-08-03).

This section covers the major **individual life insurance products** sold in the UK
market, **plus pension annuities**. Annuities are core long-term insurance business and
the dominant liability of UK life insurers (and the centrepiece of the Solvency UK
matching adjustment), so a UK library without them would misrepresent the market. The
annuity coverage differs in kind from the [U.S. section](../uslib/index.md), which covers
the U.S. retail deferred and payout families (MYGA, fixed indexed, variable, RILA, SPIA,
DIA/QLAC): the UK retail deferred-annuity market is negligible, and the pension annuity
bought with a pension pot is the product that matters. Group protection, pensions
wrappers (drawdown, SIPPs) and bulk purchase annuities remain out of scope.

## Product taxonomy

| Product type | Folder | Representative design (one line) |
|---|---|---|
| Term assurance | [term_assurance](products/term_assurance/product-spec.md) | Guaranteed-premium term with three benefit shapes (level / decreasing at a client-selected mortgage rate / family income benefit), terminal illness benefit included, optional RPI indexation; expires at end of term — no U.S.-style post-level-term tail |
| Critical illness cover | [critical_illness](products/critical_illness/product-spec.md) | Accelerated life-or-CI level term on the term-assurance chassis: ~40 ABI-aligned full-payment conditions incl. TPD, 25%/£25k additional-payment conditions, 50%/£25k children's cover, 14-day survival period; standalone variant minus the death benefit |
| Income protection | [income_protection](products/income_protection/product-spec.md) | Full-term guaranteed-premium own-occupation IP: two-band earnings cap (65% to £60k, 50% above), deferred periods 4–52 weeks (26 as base cell), RPI escalation in claim, proportionate benefit on partial return to work; three-state (healthy/sick/dead) reference model |
| Whole of life | [whole_of_life](products/whole_of_life/product-spec.md) | Two cells: underwritten guaranteed WOL (protection-only, no cash value — unlike U.S. whole life), and over-50s guaranteed acceptance (fixed cash sum, 12-month moratorium, premiums cease at 90, lapse-supported) |
| With-profits | [with_profits](products/with_profits/product-spec.md) | 90:10 proprietary fund with retrospective asset shares, 80–120% payout target range, smoothing caps, MVR bounded by asset-share shortfall; unitised WP as primary cell, conventional WP endowment as legacy cell, PruFund smoothed funds as the modern variant |
| Unit-linked investment bond | [unit_linked_bond](products/unit_linked_bond/product-spec.md) | Modern clean-charge onshore single-premium bond: 100.1% death uplift, segmented mini-policies, AMC-based charges, 5% p.a. tax-deferred withdrawal machinery; modeled via the classic UK unit vs non-unit cash-flow decomposition |
| Pension annuity | [pension_annuity](products/pension_annuity/product-spec.md) | Immediate lifetime annuity (L&G-pattern chassis): single/joint life, escalation nil/fixed/RPI-floored/LPI, guarantee period XOR value protection, enhanced terms as a mortality-rating overlay; longevity is the model |

Each folder contains `product-spec.md` (representative specification, variations
across insurers, regulatory context), `technical-notes.md` (liability cash flow model:
model points, state variables, assumptions, recursions with processing order, worked
example, sensitivities), and `sources.md` (numbered source list). Citation conventions
are defined in the [top-level README](../README.md).

Chassis relationships: critical-illness states only its deltas against the
[term-assurance](products/term_assurance/technical-notes.md) chassis; the
unit-linked-bond's smoothed-fund (PruFund) variation cross-references the
[with-profits](products/with_profits/technical-notes.md) mechanics.

## Regulatory and actuarial reference library

[references/regulatory-and-actuarial-references.md](references/regulatory-and-actuarial-references.md)
is the curated cross-product bibliography (frozen numbering R1–R38, cited from product
documents as `[REG-R#]`), with a product-relevance matrix. It spans the prudential
framework (Solvency UK: technical provisions/BEL, risk margin, the matching adjustment
and its 2023–24 reforms, PRA Rulebook and supervisory statements), FCA conduct rules
(COBS 20 with-profits/PPFMs, COBS 21.3 permitted links, Consumer Duty), legislation
and tax (FSMA/RAO long-term business classes, ITTOIA 2005 chargeable events, I-E/
BLAGAB, Insurance Act 2015/CIDRA, pension freedoms), the CMI/ONS mortality and
morbidity landscape, FRC Technical Actuarial Standards and IFoA APS, and IFRS 17.

## Provenance

`_research/` holds the raw research notes (one file per product plus
`regulatory-actuarial.md`): the per-source fact extraction that every citation in the
product documents traces back to, including explicit records of which documents were
actually retrieved and which fetches failed. Do not renumber their source lists —
product documents cite against them.

## Known gaps and caveats

Aggregated from the per-product research (each product's documents carry the full list):

- **CMI tables are subscriber-restricted.** The current UK experience tables (the "16"
  Series assured-lives tables, SAPS S3/S4 annuitant tables, IP11 income-protection
  rates, CI diagnosis tables) and the CMI Mortality Projections Model are available
  only to CMI authorised users. The reference bases here are honest **[std]** proxies
  built from public materials (ONS national life tables, older public table families),
  with the CMI framework cited by name for structure. A production implementation
  must license the real tables.
- **No public premium rate cards.** UK protection and annuity pricing is quote-driven;
  no insurer publishes rate tables. Pricing anchors are example quotes captured from
  KFDs (e.g., £100,000 at 65 buying £6,657 p.a. with 50% value protection, January
  2026), with **[std]** rate scales constructed around them.
- **Bot-blocked primary sources.** The ABI Guide to Minimum Standards for Critical
  Illness Cover, parts of the FCA Handbook (JS-rendered), PRA PS10/24 and SS7/18, and
  Scottish Widows PPFMs could not be machine-fetched; facts relying on them are
  triangulated from secondary material and tagged accordingly.
- **Vintage issues.** Some retrieved documents are older editions (Aviva pension
  annuity terms 2019/20 via a mirror; Aviva over-50s pages dated 2016); structural
  mechanics are stable but parameter details may be stale — disclosed wherever used.
- **[unverified] items remain** wherever a claim could not be confirmed against a
  retrieved document (e.g., ICOBS chapter mapping for pure protection, market-share
  claims, the L&G funeral benefit partner option).
