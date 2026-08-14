# United States — Individual Life Insurance and Annuity Reference Products

**Status:** Draft. Life products 2026-08-03; annuity products 2026-08-04 (each product's
sources were accessed on that product's draft date).

This section covers the major **individual life insurance** and **individual annuity**
product types sold in the U.S. market. Group insurance, structured settlements, and
institutional business (bulk/pension risk transfer) remain out of scope.

## Life product taxonomy

| Product type | Folder | Representative design (one line) |
|---|---|---|
| Level premium term | [term-life](products/term-life/product-spec.md) — **[executable model](models/term-life/README.md)** | Guaranteed level premiums for 10/20/30 years, then jump-to-ART renewal at unchanged face to attained age 95; convertible to permanent until min(end of level period, age 70); no cash value |
| Whole life | [whole-life](products/whole-life/product-spec.md) | Participating level-premium WL on a 2017 CSO / 4% nonforfeiture basis with three-factor contribution dividends and paid-up-additions default; limited-pay variants; plus a non-par simplified-issue final-expense variant |
| Universal life | [universal-life](products/universal-life/product-spec.md) | Flexible-premium current-assumption UL: monthly deductions (per-policy + per-unit + COI on NAAR), declared portfolio crediting over a guaranteed minimum, GPT corridor, DB options A/B — the **base chassis** for the three products below |
| Indexed UL | [indexed-ul](products/indexed-ul/product-spec.md) | UL chassis + S&P 500 (price return) annual point-to-point index account with cap, 100% participation, 0% floor — the AG 49-A benchmark-index-account design |
| Variable UL | [variable-ul](products/variable-ul/product-spec.md) | UL chassis + unitized separate-account subaccounts and a fixed option; SEC-registered, so charges are anchored on EDGAR prospectus fee tables |
| Guaranteed UL (ULSG) | [guaranteed-ul](products/guaranteed-ul/product-spec.md) | UL chassis + shadow-account secondary guarantee (AG 38 §8E Policy Design #1): policy stays in force while the shadow account is positive, funded by a solved level no-lapse premium; lapse-supported economics |

## Annuity product taxonomy

| Product type | Folder | Representative design (one line) |
|---|---|---|
| Fixed deferred (MYGA) | [fixed-deferred-annuity](products/fixed-deferred-annuity/product-spec.md) | Single-premium book-value annuity: declared rate guaranteed for a multi-year period, surrender charge plus market value adjustment, Model #805 minimum guaranteed surrender value, death benefit at full account value — the **deferred base chassis** |
| Fixed indexed (FIA) | [fixed-indexed-annuity](products/fixed-indexed-annuity/product-spec.md) | General-account deferred annuity with index-linked credits at a 0% floor (annual point-to-point with cap), premium bonus with vesting, and a guaranteed lifetime withdrawal benefit whose payments continue after the account value is exhausted |
| Variable annuity | [variable-annuity](products/variable-annuity/product-spec.md) | Separate-account deferred annuity: subaccount units net of M&E and administrative charges, a guaranteed minimum death benefit, and a lifetime withdrawal rider fee-assessed on the benefit base; guarantee cost is inherently stochastic |
| Registered index-linked (RILA) | [registered-index-linked-annuity](products/registered-index-linked-annuity/product-spec.md) | SEC-registered buffered annuity (the NAIC term is **ILVA**): point-to-point terms with a downside buffer and an upside cap, and an AG 54 interim value built from a fixed-income proxy plus a Black-Scholes-priced derivative proxy |
| Immediate (SPIA) | [immediate-annuity](products/immediate-annuity/product-spec.md) | Single premium converted immediately into a payment stream: life only, life with period certain, joint and survivor (both reduction triggers), cash refund and installment refund forms, with fixed compound COLA — the **payout chassis** |
| Deferred income (DIA/QLAC) | [deferred-income-annuity](products/deferred-income-annuity/product-spec.md) | Flexible-premium contract with **no account value**: each premium buys a paid-up income slice at then-current purchase rates, with a return-of-premium deferral death benefit and a QLAC variant meeting the Treasury requirements |

Each folder contains `product-spec.md` (representative specification, variations
across insurers, regulatory context), `technical-notes.md` (liability cash flow model:
model points, state variables, assumptions, recursions with processing order, worked
example, sensitivities), and `sources.md` (numbered source list). Citation conventions
are defined in the [top-level README](../README.md).

## Executable models

`models/<product-type>/` holds reference implementations built from the technical notes —
modelx model folders, CSV inputs, a `run.py`, and a README mapping every cells back to the
notes section it implements.

| Product | Model | Verified against |
|---|---|---|
| term-life | [`models/term-life`](models/term-life/README.md) — `TermLifeUS` | the notes' 12-row worked example, asserted to the cent |

The remaining products are not yet implemented. Run the suite with
`python -m pytest tests -q` from the repository root; see
[requirements.txt](../requirements.txt) for the modelx version floor.

## Chassis relationships

Products that share machinery point at the file where it is specified rather than
silently restating it, and each such pointer states what it inherits and where it
deviates:

- **Life:** the UL-family documents (indexed, variable, guaranteed) reference the
  [universal-life technical notes](products/universal-life/technical-notes.md) for the
  shared base-chassis recursion, which is anchored on a retrieved specimen policy;
  deviations (e.g., VUL's prospectus-sourced NAAR convention) are explicitly flagged.
- **Annuity, deferred:** the fixed-indexed and variable annuity documents inherit the
  *structure* of the [fixed-deferred-annuity](products/fixed-deferred-annuity/technical-notes.md)
  chassis — surrender benefit composition, nonforfeiture floor, death benefit at account
  value — while carrying their own recursions and parameters.
- **Annuity, payout:** the deferred-income annuity and the annuitization phase of the
  RILA reference the [immediate-annuity](products/immediate-annuity/technical-notes.md)
  payout chassis symbol-for-symbol, stating their deltas.
- **Across families:** where an annuity document borrows from a life document (index
  segment bookkeeping from indexed-UL, separate-account mechanics from variable-UL) it
  states the differences explicitly — an annuity has no cost of insurance, no net amount
  at risk, and no death benefit corridor.

## Regulatory and actuarial reference library

[references/regulatory-and-actuarial-references.md](references/regulatory-and-actuarial-references.md)
is the curated cross-product bibliography (frozen numbering **R1–R157**, cited from
product documents as `[REG-R#]`), with separate product-relevance matrices for the life
and annuity products. R1–R34 are life-origin entries (several of which also bind annuity
models), R35–R72 are annuity-specific, R150 is the NAIC principle-based reserving topic
page, and R151–R157 are the seven AP&P Manual appendix items read at first hand on
2026-08-06 — AG 33, AG 35, A-820 with A-821/A-822, A-830, A-585, A-250 and A-255. Most of
the R73–R149 block is unused: it was allocated to a statutory accounting and capital
research stream since retired from the library, and only the handful of entries the AP&P
extractions cite remain. Unused is not the same as missing: the invariant is that numbers
are never reused or renumbered.

- **Life:** NAIC statutory framework (Standard Valuation Law, Standard Nonforfeiture Law,
  Valuation Manual / VM-20, Models 582/585/787/830, AG 38/48/49/49-A/49-B), federal tax
  (IRC §§ 7702, 7702A, 807, 817), mortality tables and experience studies (2017 CSO,
  2015 VBT, ILEC mortality, SOA persistency and post-level-term studies), AAA practice
  notes, ASOPs, and accounting frames.
- **Annuity:** VM-21 (variable annuity PBR) and VM-22 (effective for valuation dates on
  or after 1 January 2026, with a three-year transition), formulaic CARVM under AG 33 and
  AG 35, AG 54 for index-linked variable annuity interim values, Model #805 nonforfeiture
  and Models #245/#250/#275, C-3 Phase II capital, SEC Form N-4 and the 2024 rule bringing
  RILAs onto it, IRC § 72 and the QLAC regulations as amended by SECURE 2.0, and the
  2012 IAM/IAR annuity mortality tables with Projection Scale G2.

## Provenance

`_research/` holds the raw research notes (one file per product, plus
`regulatory-actuarial.md` for R1–R34 and `regulatory-actuarial-annuities.md` for
R35–R72): the per-source fact extraction that every citation in the product documents
traces back to, including explicit records of which documents were actually retrieved
and which fetches failed. Do not renumber their source lists — product documents cite
against them.

## Known gaps and caveats

The significant ones, aggregated from the per-product research (each product's documents
and research file carry the full list).

**Life products**

- **Current non-guaranteed scales are not public.** Declared crediting rates, current
  COI scales, and IUL caps/participation rates are either producer-portal-only or
  point-in-time snapshots; the reference specs carry **[std]** values calibrated to
  observed ranges. Guaranteed elements are far better sourced.
- **Full rate/charge tables are largely proprietary.** Exceptions captured here: a
  complete guaranteed COI table and processing order from a UL specimen policy, a
  complete guaranteed premium schedule from a term specimen, final-expense WL premium
  rates per $1,000, and VUL prospectus fee tables.
- **ULSG shadow-account parameters are unobservable**, so that parametrization is wholly
  **[std]**, calibrated so the solved no-lapse premium resembles observed market premiums.
- **Era mixing.** Some retrieved specimens are 2001-CSO-era while the representative
  specs are stated on a 2017 CSO basis; disclosed wherever it occurs.

**Annuity products**

- **No public payout factors or purchase rates.** No insurer publishes annuity purchase
  rate tables or the mortality/interest/expense basis behind them — for SPIAs, DIAs, or
  the annuitization option of any deferred product. Income figures in these documents are
  captured illustrations, never derived rates, and no pricing test is possible against
  public data. The 2012 IAM/IAR numerical tables live at the SOA's mortality table site
  and must be loaded by an implementation.
- **Market value adjustment algebra is thinly sourced.** Three distinct MVA families were
  retrieved (geometric ratio, linear duration-times-rate-change, declared-rate
  differential) with sharply differing cap treatments, but no retrieved *MYGA* document
  states its own MVA algebra — the representative formula is inferred from same-family
  documents and says so.
- **Commutation and interim-value formulas are unpublished** for fixed SPIAs and DIAs;
  insurers name an interest-rate adjustment without giving its formula, so any
  implementation must assume one and flag it. RILA interim values are the exception —
  AG 54 mandates their structure, and prospectus formulas were retrieved.
- **AG 33 and AG 35 have been read at first hand.** Earlier passes carried them as
  unobtainable behind the paid AP&P Manual; the manual's *As of March 2026* edition turned
  out to be a free download, and both guidelines — with A-820 (and A-821/A-822), A-830,
  A-585, A-250 and A-255 — were read in full on 2026-08-06 as entries **R151–R157**, with
  extractions in `_research/appp-*.md`. The residual holes are the documents those texts
  point at but which remain unread: AG IX-B, Actuarial Guideline I, and the
  Interest-Indexed Annuity Contracts Model Regulation.
- **Behavioral assumptions are order-of-magnitude anchors.** Surrender-charge-expiry shock
  lapse, its suppression when a lifetime-withdrawal rider is in force, and rider
  utilization are the first-order drivers of annuity liability value, yet the calibrating
  studies are paywalled; the shipped values are **[std]** with their evidence quality
  stated.
- **[unverified] items remain** wherever a claim could not be confirmed against a
  retrieved document — including the RILA Form N-4 compliance date, whether any successor
  to the 2012 IAR valuation table exists, and several NAIC guideline mechanics.
