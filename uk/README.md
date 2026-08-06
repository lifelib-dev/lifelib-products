# United Kingdom — Life Insurance Reference Products

**Status:** Draft. Product documents 2026-08-03; the regulatory, accounting and capital
framework 2026-08-06 (cited sources were accessed on each part's draft date).

This section covers the major **individual life insurance products** sold in the UK
market, **plus pension annuities**. Annuities are core long-term insurance business and
the dominant liability of UK life insurers (and the centrepiece of the Solvency UK
matching adjustment), so a UK library without them would misrepresent the market. The
annuity coverage differs in kind from the [U.S. section](../us/README.md), which covers
the U.S. retail deferred and payout families (MYGA, fixed indexed, variable, RILA, SPIA,
DIA/QLAC): the UK retail deferred-annuity market is negligible, and the pension annuity
bought with a pension pot is the product that matters. Group protection, pensions
wrappers (drawdown, SIPPs) and bulk purchase annuities remain out of scope.

## Product taxonomy

| Product type | Folder | Representative design (one line) |
|---|---|---|
| Term assurance | [term-assurance](products/term-assurance/product-spec.md) | Guaranteed-premium term with three benefit shapes (level / decreasing at a client-selected mortgage rate / family income benefit), terminal illness benefit included, optional RPI indexation; expires at end of term — no U.S.-style post-level-term tail |
| Critical illness cover | [critical-illness](products/critical-illness/product-spec.md) | Accelerated life-or-CI level term on the term-assurance chassis: ~40 ABI-aligned full-payment conditions incl. TPD, 25%/£25k additional-payment conditions, 50%/£25k children's cover, 14-day survival period; standalone variant minus the death benefit |
| Income protection | [income-protection](products/income-protection/product-spec.md) | Full-term guaranteed-premium own-occupation IP: two-band earnings cap (65% to £60k, 50% above), deferred periods 4–52 weeks (26 as base cell), RPI escalation in claim, proportionate benefit on partial return to work; three-state (healthy/sick/dead) reference model |
| Whole of life | [whole-of-life](products/whole-of-life/product-spec.md) | Two cells: underwritten guaranteed WOL (protection-only, no cash value — unlike U.S. whole life), and over-50s guaranteed acceptance (fixed cash sum, 12-month moratorium, premiums cease at 90, lapse-supported) |
| With-profits | [with-profits](products/with-profits/product-spec.md) | 90:10 proprietary fund with retrospective asset shares, 80–120% payout target range, smoothing caps, MVR bounded by asset-share shortfall; unitised WP as primary cell, conventional WP endowment as legacy cell, PruFund smoothed funds as the modern variant |
| Unit-linked investment bond | [unit-linked-bond](products/unit-linked-bond/product-spec.md) | Modern clean-charge onshore single-premium bond: 100.1% death uplift, segmented mini-policies, AMC-based charges, 5% p.a. tax-deferred withdrawal machinery; modeled via the classic UK unit vs non-unit cash-flow decomposition |
| Pension annuity | [pension-annuity](products/pension-annuity/product-spec.md) | Immediate lifetime annuity (L&G-pattern chassis): single/joint life, escalation nil/fixed/RPI-floored/LPI, guarantee period XOR value protection, enhanced terms as a mortality-rating overlay; longevity is the model |

Each folder contains `product-spec.md` (representative specification, variations
across insurers, regulatory context), `technical-notes.md` (liability cash flow model:
model points, state variables, assumptions, recursions with processing order, worked
example, sensitivities), and `sources.md` (numbered source list). Citation conventions
are defined in the [top-level README](../README.md).

Chassis relationships: critical-illness states only its deltas against the
[term-assurance](products/term-assurance/technical-notes.md) chassis; the
unit-linked-bond's smoothed-fund (PruFund) variation cross-references the
[with-profits](products/with-profits/technical-notes.md) mechanics.

## Statutory accounting and capital

[regulatory/](regulatory/statutory-accounting-and-capital.md) holds the framework that
sits *on top of* the liability cash flow projections: what the supervisor, the accounts
and the tax computation require of a projection, and how to compute it.

**The UK has no "statutory accounting" in the U.S. sense** — no solvency-purpose
accounting basis, and no annual return that doubles as the accounting ledger. The file
names here mirror [us/regulatory/](../us/regulatory/statutory-accounting-and-capital.md)
for structural parity across the library, and for no other reason. What the UK content
actually covers is three separate measurements built on one cash flow engine: the
**Solvency UK prudential balance sheet** (technical provisions = best estimate + risk
margin, own funds, SCR, MCR), the **statutory accounts** under FRS 102 + FRS 103 or
UK-adopted IFRS 17, and **tax**, which is not a liability measurement at all but is
computed from the accounts with the Finance Act 2012 overlay (BLAGAB I-E versus
non-BLAGAB trade profit).

| File | Role |
|---|---|
| [statutory-accounting-and-capital.md](regulatory/statutory-accounting-and-capital.md) | What the items are, why they exist, which of the seven products they bite, and what the model must produce. Concept-only by design; includes a 74-row product applicability matrix with a note on every non-obvious mark, and the PRA three-digit product reporting codes |
| [technical-notes.md](regulatory/technical-notes.md) | How to calculate them: the best estimate and contract boundaries, the discount curves (basic, matching adjustment, volatility adjustment, TMIR, TMTP), the risk margin, the standard formula SCR module by module, own funds / reconciliation reserve / MCR, ring-fenced funds and with-profits capital, projecting the balance sheet forward, and the accounts-and-tax roll-forward. Worked examples throughout |
| [sources.md](regulatory/sources.md) | The cited entries with their retrieval limits, plus the duplicate-record table |

The framing throughout is the **model hook** — for each rule, what the projection must
produce, at what granularity, on what basis, and at what date. Two consequences dominate,
and both cut against the U.S. intuition. **Acquisition costs are deferred, not expensed:**
SI 2008/410 Schedule 3 para 13 and FRS 103 ¶3.7 each *require* a DAC asset (with-profits
funds excepted), so the U.S. "no DAC, first-year surplus strain" story does not transfer —
while Solvency UK carries no DAC at all and a best estimate that may itself be negative.
And **the dividend comes off the prudential balance sheet, not the accounts:** CA 2006
s.833A makes realised profit for a long-term insurer A − L − D on *prudential* values,
with the ring-fenced-fund and matching-adjustment portfolio surpluses among the
deductions and the accounts setting only a cap — so a UK distributable-earnings pattern
is a projection of the Solvency UK balance sheet.

The couplings run both ways rather than one. Most SCR sub-modules are a full re-run of
the liability model under changed assumptions, not a factor applied to its output; the
matching-adjustment spread stress reaches back into the discount rate the model is using;
the risk margin needs a run-off of a *different* undertaking's notional SCRs; and a
ring-fenced fund's notional SCR feeds back into own funds. That nesting, not the size of
any single stress, is what decides whether a projection engine is fit for purpose.

Each product's `technical-notes.md` carries a **Statutory accounting and capital**
section with its own specifics — contract boundary and line of business, which standard
formula sub-modules bite and in which direction, the reporting product code, the accounts
and tax treatment, and the traps peculiar to that product — cross-referencing this
framework rather than restating it.

## Regulatory and actuarial reference library

[references/regulatory-and-actuarial-references.md](references/regulatory-and-actuarial-references.md)
is the curated cross-product bibliography (numbering **R1–R120**, cited from every
document in this section as `[REG-R#]`), with a product-relevance matrix.

**R1–R38** are the frozen product-origin entries: the prudential framework (Solvency UK:
technical provisions/BEL, risk margin, the matching adjustment and its 2023–24 reforms,
PRA Rulebook and supervisory statements), FCA conduct rules (COBS 20 with-profits/PPFMs,
COBS 21.3 permitted links, Consumer Duty), legislation and tax (FSMA/RAO long-term
business classes, ITTOIA 2005 chargeable events, I-E/BLAGAB, Insurance Act 2015/CIDRA,
pension freedoms), the CMI/ONS mortality and morbidity landscape, FRC Technical Actuarial
Standards and IFoA APS, and IFRS 17. **R39–R120** were added by the regulatory work above:
the Valuation, Technical Provisions, SCR, Own Funds, MCR, Reporting and Surplus Funds
Parts of the PRA Rulebook, the IRPR Regulations 2023 and the 2024 restatement instruments,
the PRA's technical information and supervisory statements, FRS 102/103 with the Companies
Act account formats, and HMRC's Life Assurance Manual. **R50–R52, R74–R76 and R121–R133
are unused by design** — blocks were allocated to parallel research streams that did not
fill them. Unused is not the same as missing: the invariant is that numbers are never
reused or renumbered.

Twelve documents were independently numbered by more than one stream — eleven twice, and
SS15/16 three times. Following the U.S. section's R33/R73 precedent the duplication is
**recorded, not renumbered**, and only the canonical number is ever cited; the table sits
in [regulatory/sources.md](regulatory/sources.md). The page's **Scope note on capital**,
which used to treat the SCR and MCR as *cited-not-specified*, has been revised and the
earlier note superseded: the standard formula module tree, the scenario definitions, the
loss-absorbing-capacity adjustments, the ring-fenced-fund method, own funds tiering and
the MCR corridor are now specified in
[regulatory/](regulatory/statutory-accounting-and-capital.md).

## Provenance

`_research/` holds the raw research notes: one file per product, plus
`regulatory-actuarial.md` for R1–R38 and seven files for the regulatory, accounting and
capital work (`solvency-uk-technical-provisions.md` for R39–R49,
`solvency-uk-discounting-and-transitionals.md` for R53–R60,
`solvency-uk-scr-standard-formula.md` for R61–R73,
`solvency-uk-own-funds-mcr-and-internal-models.md` for R77–R83,
`solvency-uk-reporting-governance.md` for R84–R98, `uk-accounting-and-tax.md` for
R99–R113 and `uk-product-regulatory-applicability.md` for R114–R120). They are the
per-source fact extraction that every citation traces back to, including explicit records
of which documents were actually retrieved and which fetches failed. Do not renumber their
source lists — the product and regulatory documents cite against them.

## Known gaps and caveats

The significant ones, aggregated from the research (each document carries the full list).

**Products**

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

**Regulatory, accounting and capital**

- **No published parameter value is transcribed anywhere in the library.** The PRA
  publishes its monthly technical information as spreadsheets, which the retrieval helper
  cannot open, so **no risk-free curve, ultimate forward rate, fundamental spread,
  volatility adjustment or symmetric adjustment value appears in any file here** — nor do
  the non-GBP last liquid points. An implementation must load them from the PRA for the
  valuation date it is using.
- **The Annexes to the SCR – Standard Formula Part were not retrieved.** With them go the
  Annex XVI inputs to the health catastrophe sub-modules — which therefore cannot be
  computed from this library — and the **numbered line-of-business list**, which is why
  the critical-illness life-versus-health module classification is carried as unsettled
  rather than guessed, and why the line-of-business mapping of all seven products is
  **[unverified]**.
- **Two measurement anchors were never read.** **IFRS 17** itself is paywalled, so every
  paragraph reference is one the UKEB quotes; and **INSPRU 1.3.40 and 1.3.190 as at
  31 December 2015** — the definitions FRS 103 anchors "realistic value of liabilities"
  to — render as a deleted stub in the FCA Handbook. Both are cited, not specified. The
  matching-adjustment asset-and-liability information rules **MALIR 4–7** were likewise
  read only at title level, MALIR 5 carrying the quantitative matching tests a pension
  annuity model must pass.
- **Several rules are in flight at the access date.** The LACDT transitional (SCR-SF 6.5)
  reads as having expired on 30 December 2025 with no confirming instrument retrieved; the
  Own Funds chapters carry live "future version after 31/12/2026" markers; PS18/26
  replaces the matching-adjustment return from the 31 December 2026 reference date; and
  the new liquidity reporting requirements come into force on 30 September 2026. Recheck
  any of these before relying on them.
- **Conflicts are recorded, not resolved.** Live rule text that contradicts itself or a
  supervisory statement (Own Funds Chapter 4 versus 4A on tier limits, MCR 3.1B versus
  3.3 on capital add-ons, the mass-lapse correcting statement's class list against the
  unamended PS15/24), and three product rows where two research streams marked the same
  cell differently, are each flagged where they bite rather than silently reconciled.
