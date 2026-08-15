# United States — Individual Life Insurance and Annuity Reference Products

**Status:** Draft. Life products 2026-08-03; annuity products 2026-08-04 (each product's
sources were accessed on that product's draft date).

This section covers the major **individual life insurance** and **individual annuity**
product types sold in the U.S. market. Group insurance, structured settlements, and
institutional business (bulk/pension risk transfer) remain out of scope.

```{toctree}
:maxdepth: 2

products/index
references/regulatory-and-actuarial-references
```

## Life product taxonomy

| Product type | Folder | Representative design (one line) |
|---|---|---|
| Level premium term | [term_life](products/term_life/product-spec.md) — **[executable model](products/term_life/model.md)** | Guaranteed level premiums for 10/20/30 years, then jump-to-ART renewal at unchanged face to attained age 95; convertible to permanent until min(end of level period, age 70); no cash value |
| Whole life | [whole_life](products/whole_life/product-spec.md) | Participating level-premium WL on a 2017 CSO / 4% nonforfeiture basis with three-factor contribution dividends and paid-up-additions default; limited-pay variants; plus a non-par simplified-issue final-expense variant |
| Universal life | [universal_life](products/universal_life/product-spec.md) | Flexible-premium current-assumption UL: monthly deductions (per-policy + per-unit + COI on NAAR), declared portfolio crediting over a guaranteed minimum, GPT corridor, DB options A/B — the **base chassis** for the three products below |
| Indexed UL | [indexed_ul](products/indexed_ul/product-spec.md) | UL chassis + S&P 500 (price return) annual point-to-point index account with cap, 100% participation, 0% floor — the AG 49-A benchmark-index-account design |
| Variable UL | [variable_ul](products/variable_ul/product-spec.md) | UL chassis + unitized separate-account subaccounts and a fixed option; SEC-registered, so charges are anchored on EDGAR prospectus fee tables |
| Guaranteed UL (ULSG) | [guaranteed_ul](products/guaranteed_ul/product-spec.md) | UL chassis + shadow-account secondary guarantee (AG 38 §8E Policy Design #1): policy stays in force while the shadow account is positive, funded by a solved level no-lapse premium; lapse-supported economics |

## Annuity product taxonomy

| Product type | Folder | Representative design (one line) |
|---|---|---|
| Fixed deferred (MYGA) | [fixed_deferred_annuity](products/fixed_deferred_annuity/product-spec.md) | Single-premium book-value annuity: declared rate guaranteed for a multi-year period, surrender charge plus market value adjustment, Model #805 minimum guaranteed surrender value, death benefit at full account value — the **deferred base chassis** |
| Fixed indexed (FIA) | [fixed_indexed_annuity](products/fixed_indexed_annuity/product-spec.md) | General-account deferred annuity with index-linked credits at a 0% floor (annual point-to-point with cap), premium bonus with vesting, and a guaranteed lifetime withdrawal benefit whose payments continue after the account value is exhausted |
| Variable annuity | [variable_annuity](products/variable_annuity/product-spec.md) | Separate-account deferred annuity: subaccount units net of M&E and administrative charges, a guaranteed minimum death benefit, and a lifetime withdrawal rider fee-assessed on the benefit base; guarantee cost is inherently stochastic |
| Registered index-linked (RILA) | [registered_index_linked_annuity](products/registered_index_linked_annuity/product-spec.md) | SEC-registered buffered annuity (the NAIC term is **ILVA**): point-to-point terms with a downside buffer and an upside cap, and an AG 54 interim value built from a fixed-income proxy plus a Black-Scholes-priced derivative proxy |
| Immediate (SPIA) | [immediate_annuity](products/immediate_annuity/product-spec.md) | Single premium converted immediately into a payment stream: life only, life with period certain, joint and survivor (both reduction triggers), cash refund and installment refund forms, with fixed compound COLA — the **payout chassis** |
| Deferred income (DIA/QLAC) | [deferred_income_annuity](products/deferred_income_annuity/product-spec.md) | Flexible-premium contract with **no account value**: each premium buys a paid-up income slice at then-current purchase rates, with a return-of-premium deferral death benefit and a QLAC variant meeting the Treasury requirements |

Each folder contains `product-spec.md` (representative specification, variations
across insurers, regulatory context), `technical-notes.md` (liability cash flow model:
model points, state variables, assumptions, recursions with processing order, worked
example, sensitivities), and `sources.md` (numbered source list).

## Citation conventions

Every citation tag in this library is a link: `[S6]` in a product document lands on entry S6
in that product's `sources.md`, and `[REG-R18]` lands on entry R18 of the shared
[reference library](references/regulatory-and-actuarial-references.md). Numbering is
per product — S1 is a different source in each — which is why the tags resolve against the
document's own product rather than a single global list.

| Tag | Meaning |
|---|---|
| `[S#]` | Fact taken from a primary product document (brochure, specimen policy, prospectus, producer guide) listed in the product's `sources.md` |
| `[R#]` | Fact taken from a product-specific regulatory/actuarial reference in the product's `sources.md` |
| `[REG-R#]` | Fact taken from the cross-product reference library `references/regulatory-and-actuarial-references.md` (frozen R-numbering) |

(uslib-std)=

**[std]** — a *standardization introduced for the reference implementation*: a parameter or
convention chosen where sources vary, are proprietary, or are silent. Each carries a
rationale and, where available, the observed range across insurers.

(uslib-unverified)=

**[unverified]** — a claim from general knowledge or a secondary snippet that could **not**
be confirmed against a retrieved document. Treat it as a to-verify item, not an established
fact.

The hard rule throughout: **every quantitative parameter is either source-tagged or
marked [std]** — information taken from source materials is never mixed silently with
assumptions introduced for the representative specification.

## Executable models

Each `products/<product>/` directory holds its reference implementation beside the
documents that specify it — the modelx model folder, its CSV inputs, a `run.py`,
`model.md` mapping every cells back to the notes section it implements, and `model-api.md`
generated from the model's own docstrings.

All twelve products are implemented. Every model reproduces its own technical notes'
worked example, asserted cell by cell to the precision the notes display.

| Product | Model | Grid | Verified against |
|---|---|---|---|
| term_life | [`products/term_life`](products/term_life/model.md) — `Term_US_A` | annual | the notes' 12-row worked example, to the cent |
| whole_life | [`products/whole_life`](products/whole_life/model.md) — `WholeLife_US_A` | annual | all 15 steps of the dividend/PUA worked example, to the cent |
| universal_life | [`products/universal_life`](products/universal_life/model.md) — `UL_US_S` | monthly | all 3 monthiversary rows plus the month-1 trace at full precision |
| indexed_ul | [`products/indexed_ul`](products/indexed_ul/model.md) — `IUL_US_S` | monthly | both index scenarios and both variant credit bases |
| variable_ul | [`products/variable_ul`](products/variable_ul/model.md) — `VUL_US_S` | monthly | the full worked example incl. the 60/40 net premium split and pro-rata deduction |
| guaranteed_ul | [`products/guaranteed_ul`](products/guaranteed_ul/model.md) — `ULSG_US_S` | monthly | all 5 rows across both accounts, plus the forgone-deduction regime |
| fixed_deferred_annuity | [`products/fixed_deferred_annuity`](products/fixed_deferred_annuity/model.md) — `MYGA_US_S` | monthly | the 7-month table, both surrender traces, and the Nationwide geometric-MVA factors |
| fixed_indexed_annuity | [`products/fixed_indexed_annuity`](products/fixed_indexed_annuity/model.md) — `FIA_US_S` | monthly | all 16 rows, the surrender trace, and the GLWB depletion arithmetic |
| variable_annuity | [`products/variable_annuity`](products/variable_annuity/model.md) — `VA_US_S` | monthly | both subaccounts at all 6 steps, plus all three memo lines |
| registered_index_linked_annuity | [`products/registered_index_linked_annuity`](products/registered_index_linked_annuity/model.md) — `RILA_US_S` | monthly | all 6 rows × 13 columns of the AG 54 interim-value table, plus its trace |
| immediate_annuity | [`products/immediate_annuity`](products/immediate_annuity/model.md) — `SPIA_US_S` | monthly | both survivor-reduction trigger columns at 7 payment dates, plus all 5 traces |
| deferred_income_annuity | [`products/deferred_income_annuity`](products/deferred_income_annuity/model.md) — `DIA_US_S` | monthly | both premium slices, the derived guarantee period, and all 9 projection rows |

Model names are `<product>_<country>_<grid>`: the short name the product is actually
known by — the same one the taxonomy tables above use, so `MYGA`, `FIA`, `RILA`, `SPIA`,
`DIA`, `ULSG` — then `US`, then `_A` for an annual step or `_S` for a monthly one. The grid
letters follow lifelib, where `annuallife/TradLife_A` is the annual-step model and
`basiclife/BasicTerm_S` and `savings/CashValue_SE` are the monthly ones; all twelve models
here are scalar single-model-point projections, which is lifelib's other sense of `S`.

The pairing of name to folder is deliberately *not* derivable from the folder slug —
`registered_index_linked_annuity` spelled out is unusable, and the industry says RILA — so
it is registered once in `tests/conftest.py`, and
`tests/test_model_conventions.py` asserts that the registry, the directory on disk and the
model's own `_name` all agree, along with the country and grid tags.

Every model follows the same shape, and that shape is enforced rather than merely
described: two Spaces (`Data` reads the input CSVs once per model, `Projection` is
parameterized by `point_id`), inputs as **external** CSVs beside `run.py` so the model
folder holds nothing but formulas, and a `Projection` docstring carrying the mapping from
the technical notes' actuarial symbols to the cells names.
`tests/test_model_conventions.py` applies that
contract to every model in the registry; each model additionally has its own test module
for its worked example and its product-specific invariants — the notes' "Known modeling
pitfalls" sections are written up there as tests.

### Shared vocabulary

Cells names come from lifelib — `basiclife/BasicTerm_S` first, then `savings/CashValue_SE`
— so that a name means the same thing in every model here and the same thing it means in
lifelib. Where a cross-model review found one concept under two names, the conflict was
settled once and the ruling is now asserted, not merely documented:

| Convention | Settled as |
|---|---|
| In-force count | `pols_if(t)` is the count at the **start** of period `t`, and is the weight on that same `result_cf()` row's cash flows. End-of-period state is reachable through `pols_if_at(t, timing)` |
| Rates | `mort_rate` / `lapse_rate` are **annual**; `mort_rate_mth` / `lapse_rate_mth` are monthly |
| Net cash flow | `net_cf` is **income-positive** in every model. Where a product's notes print the stream outgo-positive (whole life, both payout annuities), that orientation survives verbatim as `liability_cf`, and `net_cf(t) == -liability_cf(t)` |
| Roll-forward checks | `check_*()` takes no argument and returns `bool` over all `t` (the `CashValue_SE` form); a per-`t` residual lives at `check_*_resid(t)` |
| Account value | `av_pp_at(t, timing)` / `av_at(t, timing)` with the `CashValue_SE` timing strings; `prem_to_av_pp` is the premium credited to it |
| Withdrawals | `withdrawals(t)`, in a `withdrawals` column — an owner election, not a claim |
| Benefit columns | `claims_death`, `claims_lapse`, `claims_maturity`, … named for the `kind` argument that produces them |

Absences are product facts, not gaps: a SPIA has no `premiums` and no lapse decrement, the
payout annuities model `lives_if` (annuitant survival) alongside `pols_if` (contracts with
an obligation open), and whole life has a cash value `cv_pp`, not an account value.

Run the suite with `python -m pytest tests -q` from the repository root; see
`requirements.txt` for the modelx version floor.

## Chassis relationships

Products that share machinery point at the file where it is specified rather than
silently restating it, and each such pointer states what it inherits and where it
deviates:

- **Life:** the UL-family documents (indexed, variable, guaranteed) reference the
  [universal-life technical notes](products/universal_life/technical-notes.md) for the
  shared base-chassis recursion, which is anchored on a retrieved specimen policy;
  deviations (e.g., VUL's prospectus-sourced NAAR convention) are explicitly flagged.
- **Annuity, deferred:** the fixed-indexed and variable annuity documents inherit the
  *structure* of the [fixed-deferred-annuity](products/fixed_deferred_annuity/technical-notes.md)
  chassis — surrender benefit composition, nonforfeiture floor, death benefit at account
  value — while carrying their own recursions and parameters.
- **Annuity, payout:** the deferred-income annuity and the annuitization phase of the
  RILA reference the [immediate-annuity](products/immediate_annuity/technical-notes.md)
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

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[std]: #uslib-std
[unverified]: #uslib-unverified
<!-- END generated citation links -->
