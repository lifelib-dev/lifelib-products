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

## Statutory accounting and capital

[regulatory/](regulatory/statutory-accounting-and-capital.md) holds the framework that
sits *on top of* the liability cash flow projections: the statutory accounting rules and
capital requirements a projection has to feed, and how to compute them.

| File | Role |
|---|---|
| [statutory-accounting-and-capital.md](regulatory/statutory-accounting-and-capital.md) | What the items are, why they exist, which products they bite, and what the model must produce. Includes a 12-product applicability matrix, and — under *The reserve hierarchy* — the effective-date timeline and a per-product **formulaic vs principle-based** summary |
| [technical-notes.md](regulatory/technical-notes.md) | How to calculate them: formulaic CRVM/CARVM, the VM-20 three-component structure and its exclusion tests, VM-21/VM-22, reserve projection, the statutory income roll-forward, IMR/AVR, and the RBC components with the covariance adjustment. Worked examples throughout |
| [sources.md](regulatory/sources.md) | The cited entries with their retrieval limits |

The framing throughout is the **model hook** — for each rule, what the projection must
produce, at what granularity, on what basis, and at what date. Two consequences dominate:
acquisition costs are expensed as incurred with no deferred acquisition cost asset, so a
statutory run shows first-year strain and later profit release from the same cash flows
that a GAAP run smooths; and several items couple back into the reserve model rather than
consuming its output one-way (admitted negative IMR feeds VM-20 and asset adequacy
analysis; a variable annuity's reserve and its capital requirement are two order
statistics from a single stochastic run).

Each product's `technical-notes.md` carries a **Statutory accounting and capital**
section with its own specifics — contract classification and reporting exhibit, the
applicable reserve requirement, the RBC components that bite, and the traps peculiar to
that product — cross-referencing this framework rather than restating it.

## Regulatory and actuarial reference library

[references/regulatory-and-actuarial-references.md](references/regulatory-and-actuarial-references.md)
is the curated cross-product bibliography (frozen numbering **R1–R157**, cited from
product documents as `[REG-R#]`), with product-relevance matrices for the life products,
the annuity products, and the statutory/capital entries. R1–R34 are life-origin entries
(several of which also bind annuity models), R35–R72 are annuity-specific, and R73–R142
cover statutory accounting and capital. R114–R124 and R143–R149 are unused by design —
blocks were allocated to parallel research streams that did not fill them. Unused is not
the same as missing: the invariant is that numbers are never reused or renumbered.

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
- **AG 33 and AG 35 texts could not be retrieved.** Their authoritative text sits in the
  paid NAIC AP&P Manual Appendix C, so formulaic CARVM is cited by title and effective
  date only. This is the largest single hole on the annuity side.
- **Behavioral assumptions are order-of-magnitude anchors.** Surrender-charge-expiry shock
  lapse, its suppression when a lifetime-withdrawal rider is in force, and rider
  utilization are the first-order drivers of annuity liability value, yet the calibrating
  studies are paywalled; the shipped values are **[std]** with their evidence quality
  stated.
- **[unverified] items remain** wherever a claim could not be confirmed against a
  retrieved document — including the RILA Form N-4 compliance date, whether any successor
  to the 2012 IAR valuation table exists, and several NAIC guideline mechanics.

**Statutory accounting and capital**

- **RILA capital treatment is genuinely unsettled.** The retrieved RBC instructions never
  mention registered index-linked annuities, index-linked annuities or ILVA at all, so the
  treatment must be inferred from whether the contract is valued under VM-21. The
  documents mark this open rather than inferring a treatment; closing it needs
  primary-source work.
- **Negative IMR guidance is time-limited.** The interpretation admitting negative IMR
  nullifies 1 January 2027 as written, and the revised SSAP that would replace it was
  still in drafting at the access date. Anything resting on admitted negative IMR should
  be re-checked before being treated as current.
- **Some factor tables were deliberately not transcribed.** AVR factors and IMR grouped
  amortisation factors change annually and live in instructions that are sold rather than
  published; the documents describe their role and location and state no values. RBC
  factors that *were* retrievable are cited; the 2025 RBC edition could not be parsed, so
  no year-end 2025 factor is asserted.
- **One closable gap.** The AP&P Manual proved to be a free download after all (see the
  supersession note on R33), which means Appendix C — the actuarial guidelines, including
  AG 33 and AG 35 — and Appendices A-820/A-830 are obtainable. The caveats carried in the
  annuity and reserve material still reflect the earlier paywalled assumption; a
  follow-up pass could close them.
