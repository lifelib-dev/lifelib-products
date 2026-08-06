# UK Regulatory Reporting and Capital: Calculation Technical Notes

- **Status:** Draft, 2026-08-06 (all cited sources accessed 2026-08-06).

**Scope and division of labour.** This file specifies *how to compute* the three UK measurements that sit on top of a liability cash flow projection: the **Solvency UK regulatory balance sheet** (the PRA Rulebook prudential measurement — technical provisions, SCR, own funds, MCR), the **statutory accounts** (FRS 102 + FRS 103, or UK-adopted IFRS 17), and the **tax** computation built on the accounts with the Finance Act 2012 overlay. The UK has no "statutory accounting" in the U.S. sense; the file names in this directory mirror `us/regulatory/` for structural parity across the library, and nothing else. The companion `uk/regulatory/statutory-accounting-and-capital.md` says what each item is and why it exists — read it first, and read it for concepts; this file does not repeat it and points at it by section name. The product models in `uk/products/` emit cash flows and policy state; this file consumes them. Constructions are lifelib/modelx style: explicit state, explicit recursions, per contract or per model point.

**Citation conventions** (identical to the rest of the library, non-negotiable). **[REG-R#]** cites the shared UK reference numbering in `uk/references/regulatory-and-actuarial-references.md`: **R1–R38** are the frozen pre-existing entries already cited by the seven product documents; **R39–R120** were created by this effort, with **R50, R51, R52, R74, R75, R76 and R121–R133 permanently unused by design** (parallel block allocation — unused is not missing). Every quantitative parameter, factor, stress, correlation, threshold, formula and effective date carries a [REG-R#], or **[std]** where it is a standardization introduced for this reference implementation, or **[unverified]** where the research could not confirm it against a retrieved document. Facts the research marked [unverified] **stay** [unverified]; nothing is upgraded here. Six research streams ran in parallel and independently numbered some of the same documents; the duplication is **recorded, not renumbered** (the precedent is the U.S. section's R33/R73 overlap), and only the canonical number is cited anywhere in this directory. `uk/regulatory/sources.md` carries the duplication table and the per-entry bibliography.

**Documents that could not be read, said plainly at the point of use.**

- **The Annexes to the SCR – Standard Formula Part were not retrieved** [REG-R73]. That removes Annex XVI (the mass-accident country list and ratios `r_s`, the event types and benefit ratios `x_e`, the pandemic healthcare-utilisation ratios `H_h`), the geographical-diversification annex behind `3A5`/`3C3.8`, **and the numbered line-of-business list**. Consequently the health catastrophe sub-module cannot be computed from this library, and the mapping of a UK critical-illness or income-protection contract to a numbered line of business is **[unverified]**.
- **No risk-free rate, fundamental spread, volatility adjustment, symmetric adjustment, ultimate forward rate, convergence period or Smith-Wilson parameter is stated anywhere in this file.** Those are PRA-published technical information under IRPR reg 3 [REG-R44][REG-R54] and were deliberately not transcribed; the SAECC spreadsheet was not retrieved at all [REG-R54], so **no symmetric adjustment value is given at any date**.
- **The counterparty-default probability-of-default table (`3E12`) and the loss-given-default definitions (`3E4`–`3E11`) were surveyed, not transcribed**, as were the concentration aggregation formula (`3D27`, `3D28`) and the ECAI-to-credit-quality-step mapping tables in PS12/25 Appendix 6 [REG-R62][REG-R72]. Every CQS-keyed number below needs a mapping this library does not supply.
- **There is no UK risk-margin simplification hierarchy.** Delegated Regulation Article 58 was **not restated** into Solvency UK [REG-R41][REG-R49], and the Article bodies of the (revoked) Delegated Regulation were never read — only its table of contents and Article 1 [REG-R49]. Any SCR(t) proxy therefore rests on TPFR 27 proportionality alone [REG-R41].
- **SoP4/24's quantitative capital-add-on significance thresholds were not retrieved** [REG-R69]; the SoP11/24 PDF was not fetched [REG-R70]; the Transitional Measures Part was retrieved only for Chapters 10 and 12, so **Transitional Measures 4.1 grandfathering of pre-2016 instruments into Tier 1 is [unverified]** [REG-R57][REG-R77].
- On the accounts side, **FRS 103 ¶¶2.16 (tail) and 2.17–2.18 were read only in part** [REG-R99], and HMRC's with-profits commercial-allocation guidance (LAM05070–LAM05090) was not read [REG-R18].

---

## Notation and conventions

**The two computational modes, and why the UK nesting bites harder.** **Mode V — valuation at a date:** given the in-force at τ and a fixed assumption set and curve, return a *number* — a best estimate, a stressed best estimate, a notional SCR. **Mode P — projection of the balance sheet forward:** return a *time series* of Solvency UK balance sheets, own funds and capital requirements at τ, τ+1, …. Mode P is what the ORSA's multi-year forecast [REG-R92][REG-R95], IR.05.10's three-year plan projection [REG-R90] and a recovery plan's forecast balance sheet [REG-R82] require.

Under a formulaic regime Mode V is a closed form and only Mode P projects. Under Solvency UK **the reserve is itself a projection**: the best estimate is an expected present value of a full cash flow run-off [REG-R1 TP 3.1], and the risk margin needs a whole *run-off of notional SCRs* [REG-R1 TP 4A.1], each of which is itself a re-valuation of that projection. So a single Mode-V technical provision already contains one nesting level (BEL inside SCR(t) inside the risk margin), the SCR contains a second (BEL revalued per stress, gross and net), and Mode P wraps a third around both. Count the levels before writing the loop; the section "Projecting the balance sheet forward" is about nothing else.

| Symbol | Meaning |
|---|---|
| τ, t, m | valuation date; projection index in years from τ (t = 0 at τ); month index where a monthly grid is required |
| j, g, f | contract index; homogeneous risk group [REG-R1 TP 10.1]; fund — a ring-fenced fund, a matching adjustment portfolio, or the remaining part [REG-R62 `9.1`] |
| `CF(t)` | projected best-estimate cash flow at t, signed, **gross of reinsurance** [REG-R1 TP 3.1(2)(c)] |
| `r_basic(t)`, MA, VA, TMIR | basic risk-free spot rate for term t; matching adjustment, volatility adjustment, risk-free transitional adjustment — each a scalar annual effective addition to that curve [REG-R2][REG-R1 TP 8][REG-R57] |
| BEL, RM, TP | best estimate liability; risk margin; technical provisions = BEL + RM [REG-R1 TP 2.4] |
| FDB | technical provisions **without risk margin** in respect of future discretionary benefits, determined separately [REG-R41 TPFR 10.1] |
| BSCR, nBSCR | basic SCR on the gross run; net basic SCR on the FDB-responsive run [REG-R62 `3.1`, `6.3(2)`] |
| Adj_TP, Adj_DT | loss-absorbing capacity of technical provisions; of deferred taxes — both ≤ 0 [REG-R62 `6.1(3)`] |
| SCR(t) | **reference undertaking** notional SCR after t years, for the risk margin only [REG-R1 TP 4B.2] |
| A, L, EAoL | assets and liabilities at Solvency UK value; excess of assets over liabilities = A − L [REG-R77 Own Funds 2.2] |
| BOF, EOF | basic own funds; eligible own funds after tier limits — **different for SCR and MCR coverage** [REG-R77 Own Funds 4A] |

**Three conventions that are not optional.** (1) Every stress is **instantaneous at τ**: the projection restarts from the same in-force with a changed assumption set, never from a rolled-forward state [REG-R62]. (2) Every module measures a **loss in basic own funds**, not a change in technical provisions — so an asset stress and a liability stress enter the same number [REG-R61 `SCR-GP 3.4`]. (3) The best estimate is calculated **separately per currency** [REG-R41 TPFR 18.1] and **gross of reinsurance**, with recoverables an asset computed on the same apparatus [REG-R1 TP 11.1] — a netted cash flow line makes the reporting layer and the counterparty-default adjustment uncomputable. **Precision convention [std]:** worked examples below carry six decimal places on cash flows and best estimates and four on SCR sub-modules, and every aggregation is computed from the *rounded* sub-module figures — rationale: the library's value is checkable arithmetic, not spurious accuracy.

---

## Required model outputs

The contract between `uk/products/` and this file. Anything missing makes something below uncomputable. The three "model hooks" tables in the research files are the source; this is their intersection with what a calculation actually consumes.

| Output | Granularity / basis | Consumed by |
|---|---|---|
| Cash flows by the eight TPFR 13.1 streams: benefits; benefits in kind; expenses; premiums **and cash flows resulting from premiums**; **payments to and from intermediaries**; **payments to and from investment firms for index-linked and unit-linked benefits**; salvage/subrogation; **policyholder-charged taxation** [REG-R41] | per model point per period, **gross and ceded separately, never netted**; separately identifiable, because the reporting layer and the line-of-business split need them apart | every BEL; IR.12.01; IR.05.03 |
| Contract-boundary end date **and the limb that produced it** — 3.3(1) termination right, 3.3(2) premium-rejection right, 3.3(3) repricing right assessed **at contract level** for individually-underwritten long-term business, 3.5 no-insurance-risk-and-no-guarantee, 3.6 unbundled part [REG-R41 TPFR 3] | per contract, re-derived whenever product terms change — never stored as a product constant | BEL scope; reinsurance recoverables (TPFR 23.1) |
| Segmentation keys: Annex 1 line of business, homogeneous risk group, currency, **fund tag** (with-profits fund / other ring-fenced fund / MA portfolio / remaining part), health technical-basis flag, PRA three-digit product ID code [REG-R41 TPFR 26, Annex 1][REG-R89] | per model point, fixed at set-up | TP segmentation; SCR module allocation; IR.14.01; RFF/MA aggregation |
| **Unfloored** best estimate with the sign preserved through every aggregation [REG-R1 TP 3.1] | per homogeneous risk group; the UK GAAP floor is applied downstream, never inside the projection | everything |
| Reinsurance recoverables on the **same** boundaries and apparatus, split SPV / finite reinsurance per CGB 8.1 / other, with a settlement-timing lag; and a separately calculated counterparty-default adjustment [REG-R1 TP 11][REG-R41 TPFR 23–24] | **per counterparty and per line of business**; LGD not below 50% | net BEL; MCR linear terms; IR.12.01 |
| FDB **determined separately**, and both a **frozen-FDB** and a **responsive-FDB** projection mode [REG-R41 TPFR 10.1][REG-R62 `3.3A(1)(c)`, `6.3(2)(a)`] | per fund per period | LACTP; MCR `TP_l2`; RFF adjustment `9.1(5)` |
| Per-policy **worst discontinuance value** — the most negative to basic own funds of surrender, lapse-without-value, **paid-up** and any other discontinuity option [REG-R62 `3B6.8`, `1.2`] | per policy | mass lapse; SLT health mass lapse |
| **Capital at risk** `max(0, A − B)` per contract: A = amount currently payable on death or disability net of reinsurance **plus** the EPV of further amounts payable on immediate death or disability; B = best estimate of the corresponding obligations, net [REG-R78 MCR 3C.1(5)] | **per contract**, floored at zero at contract level, **quarterly** | MCR linear; IR.14.01; the `7.8`/`7.10`/`7.14` simplifications |
| Modified durations of **sub-streams** — death payments, payments to beneficiaries, disability-morbidity payments, all cash flows — and sum-insured-weighted average assumption rates [REG-R62 `7.8`–`7.11`] | per homogeneous risk group | the life simplifications; spread risk on the asset side |
| **Monthly liability cash flows out to month 600**, gross of reinsurance, on the base-MA basis, split **level/fixed-escalation claims, inflation-linked claims, expenses, other**, with the post-50-year tail discounted back to month 600 at the basic risk-free rate; each stream's PV on the basic curve **and** on basic + MA [REG-R91] | **per matching adjustment portfolio**; effective date 31 December regardless of financial year end; a contract with any inflation linkage is reported **wholly** as inflation-linked | MALIR 3; the MA calculation itself |
| Unit-linked's **three distinct quantities**: surrender value net of tax, charges and policy loans (including non-guaranteed values, after duration penalties, assuming deferral clauses do not bite); **nominal value of units allocated** allowing for actuarial funding / discounting of initial and capital units; and **matching value of units held** [REG-R89] | per contract, per reporting date; all three are separate from the BEL and from each other | IR.12.01 C0020; unit matching; Investments 4.3 [REG-R114] |
| Unit-linked **two-part liability**: the component "in respect of linked benefits" and the non-linked remainder; the **PV of future annual management charges on existing units** separately from charges on units bought by future premiums; and **`Exp_ul`**, unit-linked expenses incurred in the previous 12 months [REG-R114 Investments 4.3, 5.1][REG-R118, secondary][REG-R62 `5.4(1)`] | per model point; the AMC decomposition is a **consultancy reading, not a rule** — the rules require only that the split exist | Investments 4.3 coverage; operational risk; Sch 3 items D vs C.2 |
| With-profits **WPBR/FPRL decomposition**: with-profits benefits reserve split retrospective (asset shares, Surplus Funds 3.3) and prospective (3.4), with permanent past and current miscellaneous surplus separated; and the six FPRL components — **future cost of contractual guarantees (cannot be negative)**, non-contractual commitments, financial options (GARs, cash options), **smoothing (may be negative)**, financing costs, other — less planned deductions for guarantees/options/smoothing and for other costs [REG-R90][REG-R45] | per with-profits fund, annual, where with-profits net BEL > £500m; **R0150 must equal IR.12.01.01 R0030/C0010** | IR.12.06; surplus funds |
| With-profits **surplus funds**, the **value of future shareholder transfers** as a separate quantity (never netted into the estate), and the shareholder transfer `= value of bonus × s/(1−s)` [REG-R45 Surplus Funds 3.1][REG-R90] | per with-profits fund; `s` = 0.10 for a 90:10 fund | own funds Tier 1 item 3A.1(1)(d); IR.12.05; restricted own funds |
| Two-year **earned premium history** gross of reinsurance, split life / life-unit-linked / non-life [REG-R62 `5.4(3)`] | last 12 months and the 12 before | operational risk and its growth surcharge |
| Assumption pack in **IR.12.04 shape**: current-year basis, prior-year basis and **five years of own experience**, as percentages of a **named table**, with the CMI projection parameterisation in CMI notation [REG-R89] | annual, where gross BEL > £50m or gross written premiums > £10m | IR.12.04; the actuarial function report |

---

## The best estimate liability

**The computation.** For a homogeneous risk group `g` in currency `c`, on the relevant risk-free curve for that block:

```
BEL(g) = SUM over t of  CF_out(g,t) * disc(t)  -  SUM over t of  CF_in(g,t) * disc(t)

CF_out = benefits + benefits in kind + expenses (all four TPFR 16.1 categories, incl. allocated
         overheads) + intermediary payments + payments to investment firms + policyholder-charged tax
CF_in  = premiums and cash flows resulting from premiums + intermediary receipts
disc(t)= discount factor from the applicable curve (see "Discount curves")
```

The best estimate is the **probability-weighted average of future cash flows**, gross of reinsurance, on up-to-date and credible information and realistic assumptions, using adequate actuarial methods [REG-R1 TP 3.1]. There is **no floor** — no zero floor, no surrender-value floor, no per-contract or per-group non-negativity rule anywhere in the Valuation, Technical Provisions or TPFR Parts; a full-text search across those Parts returns exactly one occurrence of "negative", the EUR-peg currency adjustment at TPFR 25.2, which is inapplicable to sterling [REG-R1][REG-R39][REG-R41]. Grouping is permitted only per policy or on a group satisfying all three limbs of TPFR 20.1(2) — no significant differences in the nature and complexity of risks, no misrepresentation of risk or misstatement of expenses, and approximately the same result as a per-policy calculation **in particular in relation to financial guarantees and contractual options**. No tolerance, test statistic or benchmark is given for "approximately"; the retrieved sources do not settle it [REG-R41].

**Technical provisions as a whole.** Available only where the cash flows can be replicated reliably in amount and timing **in all possible scenarios** by financial instruments with an observable market value on an active, deep, liquid and transparent market [REG-R1 TP 2.5(2)][REG-R41 TPFR 22]. TPFR 22.2 declares three categories non-replicable: option-dependent cash flows including lapses and surrenders; cash flows depending on the level, trend or volatility of mortality, disability, sickness or morbidity; and **all** servicing expenses. Every product in this library carries expenses and either biometric dependence or an exercisable option, so this route is effectively closed for whole-contract valuation across all seven; the residual use is a *component* — the unit-fund leg replicated by the units held — and even there the charges, expenses, mortality element and any guarantee remain a separate best estimate. The reporting layer expects the TP-as-a-whole amount **inside** gross best estimate (IR.12.01 rows R0025/R0026/R0030), so it is a disclosure attribute, not a separate liability line [REG-R89].

**Contract boundary — a decision procedure.** Implement as an ordered list evaluated per contract. The ordering is **[std]** — rationale: the rules state the limbs but no evaluation order, and this order runs the cheapest disqualifying test first and attempts 3.6 unbundling before any limb is applied to a whole contract.

```
0.  RECOGNISE at min( date the firm became a party to the contract , date cover begins )   [TPFR 2.1]
    Derecognise only when the obligation is extinguished, discharged, cancelled or expires.
1.  If the contract can be unbundled into parts (TPFR 3.6, 26.5, 26.6), split it first and run
    steps 2-6 on each part.
2.  INCLUDE everything, including obligations under UNILATERAL RIGHTS OF THE FIRM to renew or
    extend the scope of the contract, and obligations relating to premiums already paid.  [3.2]
    GATE ON STEPS 3-5: the cut applies ONLY where the firm CANNOT compel the policyholder to pay
    the premium for the post-date obligations; where it CAN compel payment, those obligations stay
    inside the contract and no limb of 3.3 cuts the boundary.                  [3.3 chapeau]
3.  Does the firm have a unilateral right to TERMINATE?           -> boundary at that date  [3.3(1)]
4.  Does the firm have a unilateral right to REJECT PREMIUMS?     -> boundary at that date  [3.3(2)]
5.  Does the firm have a unilateral right to AMEND PREMIUMS OR BENEFITS so that premiums fully
    reflect the risks?                                                                     [3.3(3)]
      test level: PORTFOLIO by default;
                  CONTRACT where the business is long-term insurance business AND an individual
                  risk assessment was carried out at inception AND that assessment cannot be
                  repeated before amending premiums or benefits;
      "fully reflect the risks" holds only where there is NO CIRCUMSTANCE under which benefits
      and expenses payable under the portfolio exceed premiums payable under it.          [3.7]
      -> if satisfied, boundary at that date; else no cut.
    In steps 3-5, IGNORE restrictions on the right and limits on the amendment that have
    "no discernible effect on the economics of the contract".  No quantitative threshold for
    that phrase exists in any retrieved source.                                     [unverified]
6.  SAVINGS-CONTRACT CUT: exclude obligations not relating to premiums already paid if ALL of
    (a) the contract provides no compensation for a specified uncertain event adversely affecting
        the insured person, (b) it contains no financial guarantee of benefits, and (c) the firm
        cannot compel payment of the future premium.  Same "no discernible effect" qualifier. [3.5]
7.  RECORD the end date AND the limb that produced it.  Reinsurance recoverables must be computed
    on the SAME boundary as the underlying direct contracts.                        [TPFR 23.1]
```

All limbs [REG-R41]. The step-5 carve-out is the operative rule for individually-underwritten UK protection: because the medical underwriting cannot lawfully be repeated at a review point, a **reviewable-premium** term, critical-illness or income-protection contract is tested contract by contract and its boundary is **not** cut at the review date [REG-R41]. Step 6 is what a unit-linked bond can fail: whether a 100.1%-of-bid death uplift is "compensation for a specified uncertain event" once the no-discernible-effect qualifier bites is **not settled by any retrieved source for any particular design** [REG-R41]. A with-profits contract fails limb (b) outright — it has a financial guarantee — so future regular premiums stay inside [REG-R41].

**Segmentation.** Segment into homogeneous risk groups and, as a minimum, by line of business [REG-R1 TP 10.1]. Assignment reflects the **nature of the risk**; legal form is not determinative, and health obligations pursued on a technical basis similar to long-term insurance business go to the long-term lines [REG-R41 TPFR 26.2, 26.3]. The four long-term lines that matter for this library are **29** health, **30** insurance with profit participation, **31** index-linked and unit-linked and **32** other long-term; Annex 1 Part D also carries **33** and **34** (annuities stemming from general insurance contracts, health and other respectively), and Part E carries **35** and **36** for long-term reinsurance [REG-R41 Annex 1]. The library's working mapping — non-profit term, whole-of-life and pension annuity to 32; unit-linked to 31; with-profits to 30; income protection and critical illness to 29 on a long-term technical basis and to LoB 2 / LoB 1 otherwise — is **the research's inference from TPFR 26.2/26.3 and the Annex 1 definitions, not a quotation**; Annex 1 names no products [REG-R41]. **What counts as "a similar technical basis to that of long-term insurance business" is settled by no retrieved rule or supervisory statement** — no test, no indicia, no examples.

**Expenses.** Project all four TPFR 16.1 categories — administrative, investment management, claims management, acquisition — each including **allocated overheads**, on an allocation rule that is realistic, objective and stable over time, with inflation [REG-R1 TP 9.1][REG-R41 TPFR 16]. The rule most often mis-implemented is **TPFR 16.4: expenses must be projected on the assumption that the firm will write new business in the future** — the per-policy maintenance cost is a *going-concern* unit cost, not a run-off unit cost with overheads re-spread over a shrinking book. This is the exact opposite of the risk-margin reference undertaking, which assumes no new obligations [REG-R1 TP 4B.1(5)]. **Both are correct as printed, no retrieved source reconciles them, and a model must therefore carry two expense bases** [REG-R41][REG-R1]. Nothing in the retrieved rules prescribes an inflation index, an inflation rate, or a per-policy versus per-premium split — those are assumption choices, not sourced parameters.

**Options, guarantees, and when stochastic becomes compulsory.** TPFR 19.4–19.5 require the firm to analyse the extent to which the present value of cash flows depends on **expected future outcomes** and on **scenario deviation from the expected outcome**, and where it does, to use a method reflecting those dependencies [REG-R41]. As a coded gate **[std]** — rationale: the rule states the obligation but no test, so a reference implementation needs a reproducible trigger:

```
force_stochastic(g) := any of
    (a) a benefit is a max/min of two or more quantities at any date (guaranteed sum assured vs
        asset share; unit value vs guarantee; annuity at a guaranteed rate vs the current rate);
    (b) a discretionary benefit depends on asset returns              [TPFR 9.1];
    (c) an option exercise assumption depends on moneyness            [TPFR 11.1];
    (d) a management action is conditional on a market variable       [TPFR 8].
If force_stochastic, the deterministic run is a CONTROL, not the answer: a deterministic result
values asymmetric payoffs at INTRINSIC value only and omits time value entirely.
```

The economic scenario generator must produce asset prices consistent with observed market prices, assume **no arbitrage**, and be calibrated consistently with the relevant risk-free curve used for the best estimate [REG-R41 TPFR 7.3]. Future discretionary benefits must be projected off the **assets the firm currently holds**, with allocation changes only per TPFR 8, and assumed returns consistent with the relevant curve — which forbids an assumed equity risk premium in the with-profits projection [REG-R41 TPFR 9.1]. A **flat static lapse table is permitted only on empirical evidence that behaviour is genuinely independent** of moneyness, economic conditions and management action [REG-R41 TPFR 11.1]; for a guarantee-bearing contract that evidence will not exist. Management actions enter only through a board-approved plan carrying, for each action, its trigger circumstances, **the circumstances in which it cannot be taken**, its position in the **order** of actions, its **implementation lag** and **its expenses** [REG-R41 TPFR 8.3, 8.4].

**Reinsurance recoverables and the counterparty-default adjustment.** Compute the recoverable on the same apparatus as the gross best estimate and the same contract boundaries, allowing for **the time difference between amounts becoming recoverable and actual receipt** [REG-R1 TP 11.1][REG-R41 TPFR 23.1]. SPV, finite-reinsurance (CGB 8.1) and other reinsurance recoverables are each calculated **separately**, and an SPV recoverable is capped at that SPV's aggregate maximum risk exposure [REG-R41 TPFR 23.2]. Two scope rules bound what may enter the recoverable at all. Recoverable cash flows include **only** payments in relation to **compensation of insurance events and unsettled insurance claims** — payments for other events or for already-settled claims are accounted for outside the recoverables and outside the other elements of technical provisions — and where a **deposit** has been made for those cash flows the recoverable must be adjusted **to avoid double counting** [REG-R41 TPFR 23.3]. Where an SPV's cash flows do **not** directly depend on the claims against the ceding firm, recoverables for **future** claims count only to the extent it can be verified "in a prudent, reliable and objective manner" that the **structural mismatch is not material** [REG-R41 TPFR 23.5] — so a parametric or index-triggered SPV structure earns no future-claim recoverable until that verification exists. Then, **separately from the rest of the recoverable** [TPFR 24.1]:

```
CDA = expected present value of the change in the cash flows underlying the recoverable that
      would arise if the counterparty defaults (including through insolvency or dispute) at a
      point in time, taking account of possible default events over the LIFETIME of the contract
      and of how the probability of default varies over time                   [TPFR 24.2, 24.3]
      computed SEPARATELY BY COUNTERPARTY AND BY LINE OF BUSINESS                  [TPFR 24.3]
      ignoring every credit-risk mitigation technique OTHER THAN COLLATERAL HOLDINGS [TPFR 24.2]
      with  average loss given default  >=  50% of the recoverable before the adjustment,
      rebuttable only "where there is a reliable basis for another assessment"       [TPFR 24.4]
      for an SPV counterparty, the PROBABILITY OF DEFAULT is derived from the CREDIT RISK
      INHERENT IN THE ASSETS HELD BY THE SPV                                         [TPFR 24.5]
```

All [REG-R41]. **The 50% LGD floor is the only hard numeric floor in the whole technical-provisions apparatus**, and what constitutes a "reliable basis" for rebutting it is not settled by any retrieved source. No default probabilities or spreads are stated here. Two supervisory overlays change the shape of the calculation without supplying numbers: SS5/24 on funded reinsurance (an immediate-recapture metric and worst-case collateral assumptions inside an MA portfolio) [REG-R47], and SS18/16 on longevity risk transfers, whose only quoted observation is that SCR counterparty-default capital "may not be sufficient in and of itself" — SS18/16 was read only at grep level and everything else about it is **[unverified]** [REG-R48].

**Worked example — the negative best estimate.** A three-year level term assurance. All parameters are **[std]** and chosen so every figure is reproducible by hand; a real valuation uses a CMI-family table under the [REG-R22] access regime and the PRA-published curve. Sum assured `S` = 100,000 payable at end of year of death; level annual premium `G` = 300 at t = 0, 1, 2; maintenance expense 30 at t = 0, 1, 2 while in force; acquisition expense 200 at t = 0; flat `q` = 0.002 at all ages; **flat basic risk-free rate 4%** annual effective; expense inflation 0%. The valuation is struck **at inception, before the initial premium and the acquisition cost are settled**, so both sit inside the projection. Survivorship `l(0) = 1`, `l(1) = 0.998`, `l(2) = 0.996004`; deaths `d(1) = 0.002`, `d(2) = 0.001996`, `d(3) = 0.001992008`.

| Stream | t = 0 | t = 1 | t = 2 | t = 3 | Present value |
|---|---|---|---|---|---|
| Premiums (in) | 300.000000 | 299.400000 | 298.801200 | — | **864.143121** |
| Maintenance expense (out) | 30.000000 | 29.940000 | 29.880120 | — | **86.414312** |
| Acquisition expense (out) | 200.000000 | — | — | — | **200.000000** |
| Death benefits (out) | — | 200.000000 | 199.600000 | 199.200800 | **553.937898** |

`BEL = 553.937898 + 86.414312 + 200.000000 − 864.143121 = 840.352210 − 864.143121 = −23.790911`.

Two self-checks. The maintenance PV is exactly one tenth of the premium PV, because both streams carry the same timing and in-force weights and 30 = 300/10 — a free unit test of the survivorship vector. And `BEL < 0`: the present value of guaranteed premiums inside a full-term boundary exceeds the present value of claims and expenses. **This is the normal case for profitable protection business at issue, and nothing floors it** [REG-R1][REG-R39][REG-R41]. It is a genuine difference from U.S. statutory reserving, where formulaic minimums and the VM-20 net premium reserve floor operate — *that comparison is the drafter's, not a claim sourced to any retrieved UK document*. Per product the sign is: routinely negative at issue for term assurance and critical illness; negative for the income-protection active-life cell but positive for claims in payment; cell-dependent for whole of life (the over-50s guaranteed-acceptance cell is the paradigm lapse-supported negative reserve); commonly negative for the **non-unit component** of a unit-linked bond with a positive total; normally positive for with-profits; and necessarily positive for a pension annuity in payment, which has no future premium inside the boundary [REG-R41][REG-R118].

---

## Discount curves

**What the model must expose.** Not a present value — **the cash flow vector**. The matching adjustment is the difference of two internal rates of return computed on *the same* liability cash flow vector against two different target values [REG-R2 MA 4.3][REG-R44 IRPR reg 5(1)], so a model whose public interface is a scalar BEL cannot compute an MA at all. The interface must be `CF(t) for t = 1..T` per currency, per MA portfolio, plus a solver for `R` in `SUM_t CF(t)/(1+R)^t = V` given an arbitrary target `V`. Discounting must be a **separable step** taking the curve as a parameter, because the same vector has to be discounted at least five ways [REG-R1 TP 3.1, 5, 8][REG-R2][REG-R57]:

| Basis | Construction | Notes |
|---|---|---|
| **basic risk-free** | the PRA-published basic curve for the currency | the only basis for the risk margin discount [REG-R1 TP 4A.1] and for contingent liabilities [REG-R39 Val 10.2] |
| **basic + MA** | MA computed by the firm from its own assigned assets; the PRA never publishes an MA | [REG-R2 MA 4.3] |
| **basic + VA** | VA applied to the **liquid** segment only; the extrapolation is then re-struck on the VA-adjusted forwards | TP 8.2 read alone looks like a flat prohibition on VA in the extrapolated segment; TP 8.3 completes it — **record the two together** [REG-R1] |
| **basic + TMIR adjustment** | the transitional itself embeds any VA, which must **not** be added again | [REG-R57 TM 10.4][REG-R59 ¶2.2] |
| **TMTP** | not a discount basis at all: an adjustment **to technical provisions** | [REG-R3] |

The curve is built from interest rate swap rates in the currency adjusted for credit risk, falling back to government bond rates where swaps are not available from a deep, liquid and transparent market, and is **extrapolated only** beyond the last DLT maturity, with forward rates converging smoothly to an ultimate forward rate [REG-R1 TP 5.1, 5.2][REG-R55]. For GBP the reference instrument is SONIA overnight index swaps with a **zero** credit risk adjustment for reference dates from 31 July 2021, and the **last liquid point is 50 years** on the 2025 assessment (effective 1 January 2026); EUR's is 20 years [REG-R54][REG-R56]. So a sterling annuity or whole-of-life projection is discounted at observed rates over essentially its whole term and the UFR bites only on the tail beyond t = 50 — **a model that hard-codes a last liquid point hard-codes a currency**. USD and CAD last liquid points were not reliably extracted and are not stated [REG-R56]. No UFR value, convergence period or Smith-Wilson alpha was retrieved [REG-R55].

**Exclusivity, as a lookup the model must enforce.** MA and VA on the same obligations: **no** — and the exclusivity is at **obligation** level, not firm level, so one entity may run an MA portfolio and a VA-discounted remainder simultaneously [REG-R1 TP 8.5][REG-R2 MA 13.3]. MA and TMIR: **no** [MA 13.3][REG-R57 TM 1.2]. MA and TMTP: **yes** — TMTP's `X_N` explicitly takes the MA into account [REG-R3 4.2(2)]. VA and TMIR: **yes but only once** — the VA is embedded in the TMIR and must not be added again [REG-R57 TM 10.4][REG-R59 ¶2.2]. VA and TMTP: **yes** [REG-R3]. TMTP and TMIR: **no, in both directions** [REG-R3 2.2][REG-R57 TM 10.5(2)]. **None of the four inside the risk-margin reference undertaking** [REG-R1 TP 4B.1(13)].

**The MA calculation.** Per currency, per portfolio [REG-R2 MA 4.3–4.7]:

```
MA = R_assets - R_liab_basic
R_assets     = the single annual effective rate which, applied to the MA obligation portfolio's
               cash flows, values them at the value of the ASSIGNED ASSETS
R_liab_basic = the single annual effective rate which, applied to the SAME cash flows, values them
               at the BEST ESTIMATE computed on the BASIC curve
```

Assigned assets include **only** assets whose expected cash flows are required to replicate the liability cash flows, excluding any excess [MA 4.4]. Asset cash flows are first de-risked for the probability-of-default element of the fundamental spread [MA 4.5], and the MA must **not** include the fundamental spread, deducting only the portion not already reflected in that de-risking [MA 4.6, 4.7]. The fundamental spread is `PD + cost of downgrade`, floored at **30%** of the long-term average spread for UK central government and Bank of England exposures and **35%** for all other assets, on a **30%** recovery-on-default assumption and 30 years of data [MA 4.10–4.13]; since 31 March 2022 the 30% floor applies only to UK central government and central bank exposures [REG-R55 ¶2.1]. Notching between consecutive credit quality steps 1 to 5 by **linear interpolation of the PRA-published information**, assuming rating notches are evenly spread, has been **mandatory since 31 December 2024** [MA 6.1, 6.4, 6.6]. The fundamental spread is a **term structure per asset**: "simplifications, for example using a single FS based on the duration of the asset, would be inconsistent with the way in which the FSs are intended to be applied" [REG-R8 ¶5.10]. For highly predictable assets the FS addition must reflect all sources of cash flow uncertainty; the PRA expects **10 basis points** to be generally adequate for reinvestment and rebalancing costs in normal conditions and treats it as a **floor**, and the standard approach to event variability adds **at least one quarter of the additional MA above the worst-case MA outcome** — worked in the SS as worst 5bp, best estimate 65bp, provision one quarter of 60bp = **15bp** [REG-R8 ¶¶5.20, 5.24, 5.24C].

**Breach of the eligibility conditions, as a clamp.** If compliance is not restored within two months, then monthly for the duration of non-compliance [REG-R2 MA 13.5]:

```
MA* = MA - (n - 1) * p * max(MA, 0)      n = whole months since non-compliance, CAPPED AT 11
                                          p = 10%
```

so the MA is fully extinguished after ten further months. The two-month clock runs from **detection or confirmation** where a breach is found late, and the MA referenced is dynamic — the factor applies to the current level [REG-R8 ¶¶8.1B–8.3]. **Do not recalculate the SCR for the reduction**: the PRA does not expect it, and the own-funds loss over 12 months continues to be based on balance-sheet movements ignoring the reduction [REG-R8 ¶8.1G].

**The MA eligibility mortality test, as a computation** [REG-R2 MA 2.2(3), 2.4]:

```
stress = the MORE ADVERSE FOR BASIC OWN FUNDS of
   (a) instantaneous permanent +15% (relative) to the mortality rates used for the best estimate
   (b) instantaneous +0.15 PERCENTAGE POINTS to the mortality rates (expressed as percentages)
       used in the technical provisions to reflect experience IN THE FOLLOWING 12 MONTHS
apply ONLY to policies for which the increase increases technical provisions;
multiple policies on one life may be treated as one; group-level identification is permitted
under TPFR 20.1 if not materially different; for reinsurance, identify on the UNDERLYING direct
policies.
PASS iff   ( BEL_stressed - BEL_base ) / BEL_base  <=  5%
```

This is the same pair of shocks as the SCR mortality (`3B1`) and life-catastrophe (`3B7`) sub-modules, so the same stress harness serves both — but the **selection is different** (more adverse for basic own funds, not a correlated aggregate) and the reported statistic is a percentage of the best estimate, disclosed at IRR.22.03.01 [REG-R91]. SS7/18 ¶3.5 expects **quantitative evidence** of ongoing compliance [REG-R8].

**Matching demonstration.** Under the A/B/C decomposition — component A replicating the liability cash flows after the PD adjustment, component B topping A up to the BEL discounted at basic + MA, component C surplus — offered by the PRA as "one possible method", not mandatory [REG-R8 ¶4.5]. Projection conventions are model rules: **assume no future management actions**; assume non-HP asset cash flows arrive on their contractual date; surplus assets **cannot** be assumed reinvested and realised later; **cash used to demonstrate matching is assumed realised in full in year 1**; tests are run **net of reinsurance** in both numerator and denominator [REG-R8 ¶¶4.10, 4.11]. Thresholds: Test 1 accumulated cash flow shortfall **≤ 3%** of the PV of liabilities at the risk-free rate; Test 2 undiversified 99.5% one-year VaR **≤ 1%** of the BEL separately for interest rate, inflation and currency; Test 3 notional swap — no hurdle, but explain a scaling factor above 100% or below 99%; Test 4 (HP assets) maximum loss of MA benefit **≤ 5%** of the MA benefit claimed on the whole portfolio; Test 5 modified accumulated shortfall **≤ 5%**. Tests 1, 2 and 3 apply to all MA firms; 4 and 5 only where HP assets are held. Frequency: monthly if writing new business in the fund, otherwise quarterly; Tests 2 and 3 at least quarterly [REG-R8 Appendix 1, ¶4.6A]. The Appendix opens by warning that **the PRA has described other versions of these tests in previous communications** — date any reference to them.

**TMTP, as arithmetic on balances the model must supply** [REG-R3]. The base calculation is anchored at **31 December 2024**, bounded by `0 <= T0 <= (X_N − Y_N) × (1 − N/16)` where `Y_N` is the same technical provisions computed under **INSPRU 7 as at 31 December 2015** — the only place the old regime survives. Thereafter `0 <= T_r <= A_r + B_r + C_r − W_r`, with `A_r = ZA × (risk margin portion)`, `B_r = ZB × (dynamic portion)`, `C_r = C0 × (1 − M/7)`, and `W_r` a run-off accelerator that linearly amortises the projected 1 January 2032 values of `A` and `B`. `M` runs from 0 on 31 December 2024 in days since 1 January 2025 divided by 365, **excluding 29 February 2028**. `ZA`, `ZB` and `C0` are frozen inputs from the base calculation; the risk margin portion and the dynamic portion are re-struck every period, so **two of the three legs move with markets**. TMTP is a **range, not a point**: a firm applying less than the maximum must disclose both [REG-R59 ¶¶4.2A–4.2B]. **TMTP must not be applied after 1 January 2032** [REG-R3 2.3].

---

## The risk margin

**The formula as printed** [REG-R1 TP 4A.1; identical in substance to IRPR reg 7B(a)–(h), REG-R44]:

```
RM = CoC * SUM over t >= 0 of  [ SCR(t) * max( lambda^t , lambda_floor ) ] / ( 1 + r(t+1) )^(t+1)

CoC          = 4%                                              [TP 1.2; IRPR reg 7B(b)]
t            = all integers including zero
SCR(t)       = the REFERENCE UNDERTAKING notional SCR after t years
lambda       = 0.9 for long-term obligations, 1.0 for general insurance obligations
lambda_floor = 0.25
r(t+1)       = the BASIC risk-free rate for maturity t+1, in the currency of the FIRM'S
               FINANCIAL STATEMENTS - not the currency of the obligations
```

Four traps in the printed form. (a) The discounting is at **t+1**, not t — the term-`t` capital charge is discounted over `t+1` years. (b) The taper is `max(λ^t, λ_floor)`, so with λ = 0.9 it decays until `0.9^t ≤ 0.25`; the arithmetic threshold is `ln 0.25 / ln 0.9 ≈ 13.16`, so **the floor binds from t = 14 onward — this arithmetic is derived from the rule and appears in no retrieved source**, and must never be cited to [REG-R1], [REG-R4] or [REG-R44]. (c) The rate is the **basic** curve: no MA, no VA, no transitional. (d) The calculation is for the **whole portfolio**, not built up from lines of business; the allocation to lines of business under TP 4A.3 must "adequately reflect the contributions of the lines of business to the reference undertaking notional SCR over the lifetime" and **no allocation formula is prescribed** [REG-R1].

**The reference undertaking, as a configuration of the model** [REG-R1 TP 4B.1]. Thirteen assumptions; the ones that change the arithmetic: it starts with **no obligations and no own funds**; after the transfer it **assumes no new obligations**; it holds assets equal to the notional SCR plus technical provisions net of recoverables, **selected to minimise its market-risk SCR**; the notional SCR captures underwriting risk, **material market risk other than interest rate risk**, credit risk on reinsurance, SPVs, intermediaries and policyholders, and operational risk; loss-absorbing capacity of technical provisions carries over **per risk** from the firm; there is **no loss-absorbing capacity of deferred taxes**; management actions carry over per TPFR 8 subject to the no-new-business assumption; and it applies **none of the MA, VA, risk-free transitional or TMTP**. A composite firm assumes its general and long-term business are taken over by **two different** reference undertakings. A firm with internal model permission must use that model for SCR(t) "unless it is inappropriate to do so" [TP 4A.2].

Two consequences worth stating separately. First, **an MA annuity writer's risk margin is not its own SCR run-off**: the reference undertaking discounts on the basic curve, so its liabilities — and the capital needed to support them — are struck on a materially higher-liability basis than the balance sheet the risk margin sits on. Second, the reference undertaking writes **no** new business while the best-estimate expense projection **must** assume the firm does [REG-R41 TPFR 16.4]; how the reference undertaking's expenses are set given that tension is **not explained by any retrieved source**.

**The SCR(t) run-off problem, and what may be done about it.** There is **no UK simplification hierarchy**: Delegated Regulation Article 58 was not restated [REG-R41][REG-R49], no rule text sanctions any driver-based proxy, and what a standard-formula firm may do is governed only by TPFR 27.4 — a method is disproportionate if its error could influence the user's decision-making, **unless** no method with a smaller error is available and the method is not likely to underestimate, **or** it produces technical provisions higher than a proportionate method would [REG-R41]. On that footing, a **drivers approach** is an implementation strategy, and it is **[std]** — rationale: it is the drafter's engineering suggestion, not a restatement of any rule, and it is legally usable only after a documented TPFR 27.4 error assessment.

```
[std] drivers approach
  1. compute SCR(0) fully, module by module, on the reference undertaking configuration;
  2. choose ONE driver per material sub-module that the projection already emits, e.g.
        mortality / catastrophe  -> expected sum assured in force, or capital at risk;
        longevity                -> best estimate of longevity-exposed obligations;
        expense                  -> present value of remaining expense cash flows;
        lapse                    -> surrender strain, signed, summed over policies where positive;
  3. SCR_i(t) = SCR_i(0) * driver_i(t) / driver_i(0);
  4. re-aggregate at each t with the SAME correlation matrices as at t = 0;
  5. validate against a full re-valuation at a small number of forward dates and record the error.
Step 4 is the step most often skipped: scaling the AGGREGATED SCR(0) by a single blended driver
silently freezes the diversification mix, which changes as the book runs off.
```

**Worked example — a short run-off.** Continuing the three-year term assurance. From the SCR section below, the reference undertaking notional SCR at t = 0 is `SCR(0) = 209.6848` (the firm's own SCR coincides with it here, because the [std] illustration has no market or counterparty exposure, no FDB, and no deferred tax — so `Adj = 0` and TP 4B.1(11) has nothing to remove). The driver is the **expected sum assured in force** [std], which is `100,000 × l(t)` while cover is in force and zero once it has expired.

| t | driver `100,000 × l(t)` | `SCR(t)` | `max(0.9^t, 0.25)` | `(1.04)^(t+1)` | contribution |
|---|---|---|---|---|---|
| 0 | 100,000.000 | 209.6848 | 1.00 | 1.040000 | 201.620000 |
| 1 | 99,800.000 | 209.2654 | 0.90 | 1.081600 | 174.129863 |
| 2 | 99,600.400 | 208.8469 | 0.81 | 1.124864 | 150.387948 |
| 3 | 0 | 0 | 0.729 | 1.169859 | 0.000000 |
| | | | | **sum** | **526.137811** |

`RM = 0.04 × 526.137811 = 21.045512`, so **RM = 21.0455** and `TP = BEL + RM = −23.790911 + 21.045512 = −2.745399`. Note that the taper is still in its `λ^t` regime throughout — a three-year contract never reaches the `t = 14` floor — and that the risk margin recovers most, but not all, of the negative best estimate. On a thirty-year protection book the floor binds for more than half the projection and the taper becomes the dominant driver of the answer.

---

## The standard formula SCR

**The identity, and the object being measured** [REG-R62 `SCR-SF 2.1`][REG-R61 `SCR-GP 3.4`]:

```
SCR   = BSCR + SCR_operational + Adj
BSCR  = sqrt( SUM_{i,j} Corr_{i,j} * SCR_i * SCR_j ) + SCR_intangibles      [3.1(2), 3.1(3)]
        over i,j in {Market, Default, Life, Health, Non-life}; INTANGIBLES SIT OUTSIDE THE ROOT
Adj   = Adj_TP + Adj_DT,  each negative or zero                                    [6.1(3)]
```

Every module is calibrated to the **value-at-risk of basic own funds at 99.5% over one year** [REG-R61 `SCR-GP 3.4`], and the SCR covers existing business plus new business expected in the following 12 months, and for existing business **only unexpected losses** [`SCR-GP 3.3`]. There is an explicit carve-out for **changes to the volatility adjustment** — they are not covered — and **no corresponding carve-out for the matching adjustment**, which is why `3D25` below turns spread risk into a liability calculation [`SCR-GP 3.6`][REG-R62].

Top-level correlation matrix, `3.1(2)(d)` [REG-R62], extracted cleanly and verified symmetric:

| | Market | Default | Life | Health | Non-life |
|---|---|---|---|---|---|
| Market | 1 | 0.25 | 0.25 | 0.25 | 0.25 |
| Default | 0.25 | 1 | 0.25 | 0.25 | 0.5 |
| Life | 0.25 | 0.25 | 1 | 0.25 | 0 |
| Health | 0.25 | 0.25 | 0.25 | 1 | 0 |
| Non-life | 0.25 | 0.5 | 0 | 0 | 1 |

For a UK life insurer the live block is the 4×4 {Market, Default, Life, Health} with **0.25 everywhere off-diagonal**.

**What a "scenario" means — the architecture rule.** In the **gross** run a firm must assume the scenario **does not change** the risk margin, the value of deferred tax assets and liabilities, or the value of **future discretionary benefits**, and that **no management actions are taken** [REG-R62 `3.3A(1)`]. It must nevertheless take account of future management actions complying with TPFR 8 and of **any material adverse impact of the scenario or of those actions on the likelihood that policyholders exercise options** [`3.3A(2)`]. **Limbs (1)(d) and (2)(a) are difficult to reconcile on their face; the research recorded the tension rather than resolving it, and the reading that (1)(d) excludes new discretionary responses while (2)(a) preserves the pre-agreed framework is the research's interpretation, not a quoted rule** [REG-R62]. Two further rules bind every scenario: simplified stressed technical provisions are allowed only where they do not misstate the SCR in a way that could influence the user, **unless the simplification produces a higher SCR** [`3.3A(3)`]; and **where a scenario would increase basic own funds the requirement is zero** — every scenario-based sub-module is floored at zero before aggregation [`3.3A(5)`].

The **net** run recalculates the BSCR with FDB **responsive**, with management actions per TPFR 8 live in the life module, the SLT health sub-module, the health catastrophe sub-module, the market module and the counterparty default module, with type 1 counterparty default replaced by an equivalent instantaneous-loss scenario, and with the same substitution where certain simplifications were used [REG-R62 `6.3(2)`]. So:

```
run A (gross):  FDB frozen, no new management actions          -> SCR_i  -> BSCR
run B (net):    FDB responsive, management actions live        -> nSCR_i -> nBSCR
Adj_TP = - max( min( BSCR - nBSCR ; FDB ) ; 0 )                                    [6.3(1)]
Adj_DT = change in deferred taxes from an INSTANTANEOUS LOSS of BSCR + Adj_TP + SCR_op  [6.4(1)]
SCR    = BSCR + SCR_operational + Adj_TP + Adj_DT
```

A firm with **no** future discretionary benefits — term assurance, critical illness, income protection, unit-linked bond, non-profit pension annuity — has `BSCR = nBSCR` and `Adj_TP = 0`, so one run suffices. **With-profits is the product that forces the two-run architecture** [REG-R62]. Four sub-modules are defined as the *highest of* alternatives — lapse `3B6.9`, SLT health lapse `3C16.9`, interest rate `3D4.2`, currency `3D32.9` — and each requires that where the highest gross and the highest net requirements rest on **different** scenarios, the one whose scenario produces the highest **net** requirement is taken. **The selection is made net; the reported gross number follows the net selection.** This is easy to implement wrongly.

**Life underwriting risk** [REG-R62 chapter `3B`]. Correlation matrix `3.8(3)`; **the "Mortality" row label is absent in the rendered HTML and the row is identified by symmetry against the first column of every other row — an inference, not a read label** [REG-R62]:

| | Mortality | Longevity | Disability | Life expense | Revision | Lapse | Life cat |
|---|---|---|---|---|---|---|---|
| Mortality | 1 | −0.25 | 0.25 | 0.25 | 0 | 0 | 0.25 |
| Longevity | −0.25 | 1 | 0 | 0.25 | 0.25 | 0.25 | 0 |
| Disability | 0.25 | 0 | 1 | 0.5 | 0 | 0 | 0.25 |
| Life expense | 0.25 | 0.25 | 0.5 | 1 | 0.5 | 0.5 | 0.25 |
| Revision | 0 | 0.25 | 0 | 0.5 | 1 | 0 | 0 |
| Lapse | 0 | 0.25 | 0 | 0.5 | 0 | 1 | 0.25 |
| Life catastrophe | 0.25 | 0 | 0.25 | 0.25 | 0 | 0.25 | 1 |

The **−0.25 mortality/longevity** entry is the only negative correlation anywhere in the standard formula as retrieved, and it is why a mixed protection-plus-annuity book diversifies. The stresses, all requiring a **full revaluation** of the best estimate:

| Sub-module | Rule | Stress |
|---|---|---|
| Mortality | `3B1.1` | instantaneous **permanent +15%** (relative) to the mortality rates used for the TP calculation |
| Longevity | `3B2.1` | instantaneous **permanent −20%** (relative) |
| Disability-morbidity | `3B3.1` | one combined scenario: **+35%** in the following 12 months, **+25%** thereafter, **−20%** to recovery rates for the following 12 months and all years after |
| Life expense | `3B4.1` | **+10%** to the amount of expenses **and +1 percentage point** to the expense inflation rate |
| Revision | `3B5.1` | **permanent +3%** to annuity benefits, **only** where benefits could increase from changes in the legal environment or the insured's state of health |
| Life catastrophe | `3B7.1` | **+0.15 percentage points** (absolute, i.e. +0.0015 in decimal) to the mortality rates used to reflect experience **in the following 12 months only** |

Mortality, longevity and life catastrophe apply **only to policies for which the stress increases technical provisions without the risk margin**; multiple policies on the same insured person may be treated as one, and group-level identification is permitted under TPFR 20 where not materially different; for reinsurance obligations the identification is made on the **underlying** policies [`3B1.2`, `3B1.3`, `3B2.2`, `3B7.2`]. **`3B3` carries no such qualifier and no persistency limb** — unlike the health version. A standard UK level or fixed-escalation pension annuity has no revision right, so `3B5` is normally nil for it.

**Life lapse** is the **highest of three** [REG-R62 `3B6.1`], subject to the net-basis tie-break: **+50%** relative to option exercise rates, provided the increased rates do not exceed 100%, applied only where exercise increases TP without the risk margin [`3B6.2`]; **−50%** relative, the decrease not to exceed **20 percentage points**, applied only where exercise decreases TP [`3B6.3`]; and **mass lapse** [`3B6.6`] — **70%** discontinuance of policies within Regulated Activities Order Schedule 1 Part II **class VII** meeting the natural-person conditions, **40%** of all other policies, and **40%** off the number of future contracts under forward-looking reinsurance treaties. "Relevant options" include both the termination-side rights and the establish/renew/increase/extend/resume rights, and for the latter **the change in exercise rate is applied to the rate reflecting that the option is not exercised** [`3B6.4`]. **"Discontinuance" includes making a contract paid-up** [`1.2`], and `3B6.8` requires the mass event to be based on **the type of discontinuance that most negatively affects basic own funds on a per policy basis** — mass lapse is not "surrender 40% of policies", it is "for each policy take the worst of surrender, paid-up and lapse-without-value, then apply 40% of that".

**The class III correction, which a drafter reading PS15/24 alone will get wrong.** As published in the PRA Rulebook: Solvency II Instrument 2024 (PRA2024/13 = PS15/24 Appendix 6) Annex O, `3B6.6(1)` referred to **both class III (linked long-term) and class VII (pension fund management)** [REG-R42]. The PRA declared the class III reference an **error** on 20 December 2024 and deleted it, effective **31 December 2024** [REG-R64]. The live rule names **class VII only**, so **a UK unit-linked bond takes the 40% limb, not 70%** [REG-R62]. PS15/24 ¶¶6.16 and 6.18 remain published and unamended. The correction statement also narrates that the 2015 transposition table identified **class II ("Marriage and birth")** and class VII, then concludes on **class VII(a) and VII(b)** — **the discrepancy is unexplained and is recorded, not smoothed over** [REG-R64].

**Health underwriting risk** [REG-R62 chapter `3C`]. `SCR_health` aggregates NSLT, SLT and health catastrophe at `3.10A(3)`: NSLT/SLT **0.5**, each against health catastrophe **0.25**. The SLT/NSLT split is by numbered line of business at `3.10B` — NSLT for lines 1, 2, 3, 13, 14, 15, 25; SLT for lines 29, 33, 35 — but **the line-of-business list was not retrieved**, so the mapping of a UK critical-illness or income-protection contract to a numbered line is **[unverified]** [REG-R73]. What *is* verified: `3C4` names segment 2 as income protection insurance and proportional reinsurance, lines 2 and 14, in the NSLT branch with **σ(premium) = 8.5%** and **σ(reserve) = 14%**; and `3C11.2(2)` restricts the SLT income-protection scenario to obligations "where the underlying business is pursued on a similar technical basis to that of life insurance". So the long-term individual contract is SLT and the annually-renewable one NSLT, on the technical-basis test.

The SLT correlation matrix `3C8.3` is **the life matrix with the life-catastrophe row and column removed — every surviving entry identical** [REG-R62]. Health mortality `3C9.1` is **+15%** and health longevity `3C10.1` **−20%**, identical to life; health expense `3C14.1` is **+10%** and **+1pp**, identical to life. Two differ and both matter for UK income protection:

- **Income-protection disability-morbidity `3C13.1`** — one combined scenario: **+35%** in the following 12 months; **+25%** in the years after; **where recovery rates used in the TP calculation are LOWER THAN 50%, a −20% decrease** in them; and **where persistency rates are EQUAL TO OR LOWER THAN 50%, a +20% increase** in them. Note the two conditional limbs and their asymmetric thresholds. Health disability-morbidity is the **sum** — not a correlated aggregation — of the medical-expense and income-protection requirements [`3C11.1`].
- **Health revision `3C15.1`** — **permanent +4%** to annuity benefits (life is 3%), with **inflation** as an additional trigger alongside the legal environment and the insured's state of health. An index-linked income-protection claim in payment is squarely in scope.

SLT health lapse `3C16` is the **higher of** up ×1.5 (capped at 100%), down ×0.5 (capped at −20pp), and a flat **40%** mass lapse — **there is no 70% limb anywhere in the health module**. NSLT health is a **3-sigma factor model**, `SCR_(NSLT,pr) = 3 × σ_NSLTh × V_NSLTh`, combined with a **40%** NSLT lapse event as `sqrt(pr² + lapse²)` [`3C1.2`, `3C2.1`, `3C7.1`]. **Health catastrophe cannot be computed from this library**: mass accident and accident concentration need the country list, the affected-person ratios `r_s` and the benefit ratios `x_e` from **Annex XVI, which was not retrieved**, and the pandemic sub-module's `L_p = 0.000075 × E + 0.4 × Σ_c (N_c × M_c)` needs the healthcare-utilisation ratios `H_h` from the same annex — **the 0.000075 and 0.4 factors are in the rule text and are verified; the annex inputs are not** [REG-R62][REG-R73]. What the liability model must still emit is the **income-protection pandemic exposure `E`**: benefits payable assuming the insured person is **permanently disabled and will not recover** — a projection run with recovery rates set to zero [`3C20.2`].

**Market risk** [REG-R62 chapter `3D`]. The correlation matrix `3.11A(2)` is **state-dependent**: the coefficient `A` between interest rate and each of equity, property and spread is **0 where the interest-rate charge comes from the UP scenario and 0.5 in all other cases** [`3.11A(3)`].

| | Interest rate | Equity | Property | Spread | Concentration | Currency |
|---|---|---|---|---|---|---|
| Interest rate | 1 | **A** | **A** | **A** | 0 | 0.25 |
| Equity | **A** | 1 | 0.75 | 0.75 | 0 | 0.25 |
| Property | **A** | 0.75 | 1 | 0.5 | 0 | 0.25 |
| Spread | **A** | 0.75 | 0.5 | 1 | 0 | 0.25 |
| Concentration | 0 | 0 | 0 | 0 | 1 | 0 |
| Currency | 0.25 | 0.25 | 0.25 | 0.25 | 0 | 1 |

A typical UK annuity writer's charge comes from the **down** shock and therefore takes 0.5; **the market SCR is a discontinuous function of the balance sheet**, and the model must record which direction won.

Interest rate is the **higher of (i) the sum over all currencies of the up requirements and (ii) the sum over all currencies of the down requirements** — summed within a direction, then maximised across directions, not maximised per currency [`3D4.1`]. Relative shocks to the basic risk-free rates by maturity [`3D5.1`, `3D6.1`], linearly interpolated, with the 1-year figure applying below 1 year and the 90-year figure beyond 90:

| Maturity (yrs) | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 90 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Up** | 70% | 70% | 64% | 59% | 55% | 52% | 49% | 47% | 44% | 42% | 39% | 37% | 35% | 34% | 33% | 31% | 30% | 29% | 27% | 26% | 20% |
| **Down** | 75% | 65% | 56% | 50% | 46% | 42% | 39% | 36% | 33% | 31% | 30% | 29% | 28% | 28% | 27% | 28% | 28% | 28% | 29% | 29% | 20% |

The up shock carries an **absolute floor: the increase at any maturity must be at least one percentage point** [`3D5.3`]. The down shock has **no** absolute floor and **must be nil for negative basic rates** [`3D6.3`]. **The downward table is non-monotonic at maturities 14–20 (28, 27, 28, 28, 28, 29, 29). That is what the source shows; it was not cross-checked against the revoked Delegated Regulation Article 167 table, so whether the shape is genuine or an extraction artefact is [unverified]** [REG-R62].

Equity: type 1 **39% + SA**, type 2 **49% + SA**, qualifying infrastructure **30% + 77%×SA**, qualifying infrastructure corporate **36% + 92%×SA**, with **22%** for strategic participations and for qualifying long-term equity investments [`3D9`]. Aggregation puts type 2 and the two infrastructure buckets together arithmetically and combines them with type 1 at **0.75** [`3D7.6`]. The symmetric adjustment is `SA = 0.5 × ((CI − AI)/AI − 8%)` on a 36-month equally-weighted average, **bounded to ±10%** [`3D12.2`, `3D12.4`], over an index weighted **FTSE All-Share 0.48, S&P 500 0.30, FTSE Developed Europe ex UK 0.15, Nikkei 225 0.07** [`3D14.1`]. **No SAECC value is stated here at any date — the PRA's monthly spreadsheet was not retrieved** [REG-R54]. Property is a flat **−25%** on immovable property [`3D15.1`].

Spread is the arithmetic **sum** of the bonds-and-loans, securitisation and credit-derivative components [`3D16.1`]. The rated bond table keys on **modified duration floored at 1** [`3D17.2`, `3D17.3`]:

| `dur_i` | formula | CQS0 `a/b` | CQS1 `a/b` | CQS2 `a/b` | CQS3 `a/b` | CQS4 `a/b` | CQS5&6 `a/b` |
|---|---|---|---|---|---|---|---|
| up to 5 | `b_i·dur_i` | — / 0.9% | — / 1.1% | — / 1.4% | — / 2.5% | — / 4.5% | — / 7.5% |
| >5 to 10 | `a_i + b_i(dur_i−5)` | 4.5% / 0.5% | 5.5% / 0.6% | 7.0% / 0.7% | 12.5% / 1.5% | 22.5% / 2.5% | 37.5% / 4.2% |
| >10 to 15 | `a_i + b_i(dur_i−10)` | 7.0% / 0.5% | 8.5% / 0.5% | 10.5% / 0.5% | 20.0% / 1.0% | 35.0% / 1.8% | 58.5% / 0.5% |
| >15 to 20 | `a_i + b_i(dur_i−15)` | 9.5% / 0.5% | 11.0% / 0.5% | 13.0% / 0.5% | 25.0% / 1.0% | 44.0% / 0.5% | 61.0% / 0.5% |
| >20 | `min(a_i + b_i(dur_i−20); 1)` | 12.0% / 0.5% | 13.5% / 0.5% | 15.5% / 0.5% | 30.0% / 0.5% | 46.6% / 0.5% | 63.5% / 0.5% |

**Two extraction caveats, recorded rather than fixed:** the ">15 to 20 / CQS1" cell renders as `11 .0%` with a stray space, read as 11.0%; and **whether the PRA genuinely merged CQS 5 and 6 into one column (the revoked Delegated Regulation Article 176 table had seven) was not cross-checked and is [unverified]** [REG-R62]. The unrated uncollateralised table at `3D17.4` reads `15 + 1.7%·(dur_i − 5)` for durations >5 to 10 — **the percent sign after "15" is absent in the source; it is almost certainly 15% but is transcribed as rendered and marked [unverified]** [REG-R62].

**`3D25` — the rule that makes an MA annuity writer's spread risk a liability calculation.** Where a firm applies the matching adjustment it must apply the instantaneous decreases to the assigned assets **and recalculate the technical provisions to take account of the impact on the amount of the matching adjustment**, increasing the fundamental spread on assigned assets by the product of (a) the absolute spread increase which, multiplied by the asset's modified duration, produces the relevant `stress_i`, and (b) a reduction factor by credit quality step [REG-R62 `3D25.1`]:

| CQS | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| Reduction factor | 45% | 50% | 60% | 75% | 100% | 100% | 100% |

A **100%** factor also applies to assigned assets with no ECAI credit assessment and to qualifying infrastructure and qualifying infrastructure corporate assets at CQS 3 [`3D25.2`]. Economically the MA absorbs `(1 − reduction factor)` of the widening: a CQS 0 portfolio passes only 45% through to the fundamental spread; at CQS 4 and below the MA gives **no** offset. **Note this table has seven CQS columns while `3D17.3` has six** — recorded.

Concentration is a factor model on **single-name exposures** with same-group exposures treated as one name: relative excess thresholds `CT_i` of **3%** at CQS 0–2 and **1.5%** at CQS 3–6, risk factors `g_i` of **12%** at CQS 0–1, **21%** at CQS 2, **27%** at CQS 3 and **73%** at CQS 4–6, with covered bonds at CQS 0 or 1 taking `CT_i = 15%` and counting as a distinct name [`3D29.1`, `3D30.1`, `3D31.1`]. **The aggregation formula `3D27` and the excess-exposure definition `3D28` were not transcribed and no substitute is offered.** Currency is the **higher of ±25%** per foreign currency, **summed across currencies with no diversification**, where "foreign" means other than the currency of the **financial statements** [`3D32`].

**Counterparty default** [REG-R62 chapter `3E`]: `SCR_def = sqrt(SCR_def1² + 1.5·SCR_def1·SCR_def2 + SCR_def2²)`, an implied correlation of 0.75 [`3.13`]. Type 1 is a three-branch step function on `σ`, the standard deviation of the loss distribution, against total loss-given-default: `3σ` where `σ ≤ 7%·TLGD`; `5σ` where `7%·TLGD < σ ≤ 20%·TLGD`; and **`TLGD` itself** above that [`3E13`]. Type 2 is **90%** of loss-given-default on intermediary receivables overdue more than three months plus **15%** on all other type 2 exposures [`3E15.1`]. **The probability-of-default table at `3E12` and the loss-given-default definitions at `3E4`–`3E11` were surveyed, not transcribed; no PD or LGD value is stated here.** Two scope points that bite for this library: reinsurance arrangements and SPVs are **type 1**, and **third-party investment guarantees on insurance contracts for which the firm would be liable on the third party's default are treated as derivatives** in this module — directly relevant to a guaranteed unit-linked design [`3.14`, `3.19`].

**Intangible** is `0.8 × V_intangible` added **outside** the BSCR root; normally nil, since goodwill and most intangibles are valued at zero on a Solvency UK balance sheet [REG-R62 `3F1.1`][REG-R39 Val 8.1].

**Operational risk** [REG-R62 `5.4`]:

```
SCR_operational = min( 0.3 * BSCR ; Op ) + 0.25 * Exp_ul
Op              = max( Op_premiums ; Op_provisions )
Op_premiums     = 4% * (Earn_life - Earn_life-ul) + 3% * Earn_non-life
                + a GROWTH SURCHARGE at the same rates on the excess of the last 12 months'
                  premium over 1.2x the preceding 12 months', floored at zero
Op_provisions   = 0.45% * max(0; TP_life - TP_life-ul) + 3% * max(0; TP_non-life)
```

`Exp_ul` is expenses incurred **during the previous 12 months** on long-term contracts where the investment risk is borne by policyholders. Two caps operate: the **30%-of-BSCR cap applies only to `Op`**, and the unit-linked expense term is added on top, **uncapped**. Premiums are **gross of reinsurance**; technical provisions for `Op_provisions` **exclude the risk margin and are gross of reinsurance**. Unit-linked business is excluded from **both** premium and provision legs and charged 25% of one year's expenses instead, so a pure unit-linked writer's operational charge is essentially `0.25 × Exp_ul`, independent of fund size. **The extracted LaTeX for `5.4(3)` has mismatched brackets; the structure above is the reading consistent with the defined terms `5.4(3)(a)`–`(f)`, and the exact bracketing of the second `max` — specifically whether the non-life growth surcharge sits inside or outside the same `max` as the life one — is [unverified]** [REG-R62]. Re-read the rule before coding it.

**Simplifications** convert a full revaluation into a closed form over statistics the projection already emits, but `7.2` makes each legally usable only after a documented proportionality assessment covering the nature, scale and complexity of the risks **and an evaluation of the error introduced** — and forbids the simplification where that error could influence the user's decision-making, **unless it produces an SCR exceeding the standard calculation** [REG-R62]. The life set: mortality `7.8` `= 0.15·q·Σ_k CAR_k·(1−q)^(k−1)/(1+i_k)^(k−0.5)`; longevity `7.9` `= 0.2·q·n·1.1^((n−1)/2)·BE_long`; disability-morbidity `7.10`; expense `7.11`; lapse `7.12` `Lapse_up = 0.5·l_up·n_up·S_up` with `l_up` the higher of the average lapse rate on positive-surrender-strain policies and **67%**, and `Lapse_down` the analogue with **40%**; and life catastrophe `7.14` `= Σ_i 0.0015·CAR_i`, the exact factor equivalent of the `3B7.1` shock. **Surrender strain** is defined at `7.12(3)` as *(amount currently payable on discontinuance, net of amounts recoverable from policyholders or intermediaries) − (technical provisions without the risk margin)*, signed, per policy — the natural diagnostic for which policies fall in which lapse limb. **There is no simplification for mass lapse.** Using `7.8`, `7.9`, `7.10`, `7.11`, `7.12(1)`, `7.12(2)`, `7.14`, `7.20`, `7.23(1)(a)`, `7.23(1)(b)` or `7.24` changes how the **net** run is constructed: those requirements are replaced by an equivalent instantaneous-loss scenario [`6.3(2)(d)`].

**Full revaluation versus formulaic — the master table.** This is the single most important architecture consequence of the standard formula.

| Module / sub-module | Rule | Full revaluation of the BEL? | Driver |
|---|---|---|---|
| Life mortality / longevity / disability / expense / revision | `3B1`–`3B5` | **Yes** | the stressed assumption set |
| Life lapse up / down / mass | `3B6` | **Yes, three runs** | ×1.5 capped at 100%; ×0.5 capped at −20pp; 70% / 40% discontinuance |
| Life catastrophe | `3B7.1` | **Yes** | year-1 mortality +0.15pp absolute |
| SLT health mortality / longevity / expense / revision / disability / lapse | `3C9`–`3C16` | **Yes** | as life, with the `3C13` conditional limbs and `3C15`'s 4% |
| NSLT health premium and reserve | `3C2.1` | **No — factor** | `3σV`; needs premium and claims-provision volumes |
| NSLT health lapse | `3C7.1` | **Yes** | 40% discontinuance |
| Health catastrophe | `3C18`–`3C20` | **No — factor** | **Annex XVI inputs not retrieved; not computable here** |
| Interest rate up / down | `3D5`/`3D6` | **Yes, twice** | rebuild the curve; revalue assets **and** BEL |
| Equity / property | `3D9`/`3D15` | Assets only, **plus** the BEL for unit-linked and with-profits | the stress sizes above |
| Spread — non-MA | `3D17` | Assets only | `stress_i(CQS, dur_i)` |
| Spread — **MA portfolio** | `3D25` | **Yes** | stress assets **and** re-derive the MA via the FS uplift × reduction factor |
| Concentration | `3D26`–`3D31` | **No — factor** | `CT_i`, `g_i` |
| Currency | `3D32` | Assets and any FX-denominated BEL, twice | ±25% per currency, summed |
| Counterparty default type 1 / type 2 | `3E13`/`3E15` | **No — factor** | `3σ / 5σ / TLGD`; 90% / 15% of LGD |
| Intangible / operational | `3F1`/`5.4` | **No — factor** | `0.8 × V`; premiums, TP and `Exp_ul` |
| LACTP (`Adj_TP`) | `6.3` | **Yes — a full second pass of everything above** | FDB responsive, management actions live |
| LACDT (`Adj_DT`) | `6.4` | Balance-sheet revaluation of deferred taxes | instantaneous loss `BSCR + Adj_TP + SCR_op` |
| RFF / MA notional SCRs | `9.1` | **Yes — repeat the whole exercise per fund** | no diversification between funds |

**Counting the runs.** A with-profits insurer with one ring-fenced fund and no MA portfolio, using no simplifications, needs on the order of *(number of scenario-based sub-modules) × 2 (gross/net) × (number of RFFs + MA portfolios + 1)* complete liability revaluations, plus the assumption permutations inside the lapse and interest-rate maxima. **That count, not the size of any single stress, decides whether a projection engine is fit for standard-formula reporting.**

**LACDT, precisely.** `Adj_DT` is the change in the value of deferred taxes resulting from an instantaneous loss of `BSCR + Adj_TP + SCR_operational` — note the ordering: the tax leg is computed on the post-`Adj_TP` loss and **includes** operational risk [REG-R62 `6.4(1)`]. Deferred taxes are valued under Valuation 11.1–11.2 [REG-R39]. **An increase in deferred tax assets arising from that loss must not be utilised** unless the `6.5` transitional applied — and **that transitional ended 30 December 2025** [`6.4(3)`, `6.5`]. A decrease in DTLs or an increase in DTAs gives a **negative** adjustment; a positive change gives a **nil** adjustment [`6.4(5)`, `6.4(6)`]. Where the loss must be allocated to causes, the allocation follows the contribution of the standard formula modules to the BSCR, with a carve-out for a partial internal model's scope [`6.4(7)`].

---

## Own funds, the reconciliation reserve and the minimum capital requirement

**The build-up** [REG-R77 Own Funds 2.1, 2.2, 3C.1]:

```
EAoL = excess of assets over liabilities     (Solvency UK values throughout)
BOF  = ( EAoL - own shares held by the firm ) + subordinated liabilities
OF   = BOF + ancillary own funds (permission required; nothing in a projection produces AOF)

reconciliation reserve
   = EAoL
   - own shares held by the firm                                                    3C.1(1)
   - foreseeable dividends, distributions and charges                               3C.1(2)
   - the basic own funds items in 3A.1(1)(a)-(e), 3D.1(1) and 3F.1(1)               3C.1(3)
   - any item held under a classification of own funds permission                   3C.1(4)
   - restricted own funds that exceed the notional SCR of their MA portfolio or
     ring-fenced fund under 3L.1, or are excluded under 3L.2                        3C.1(5)
   - participations in financial and credit institutions deducted under 3K          3C.1(6)
```

The reconciliation reserve is a **residual**, it **may be positive or negative**, and a firm is **not** required to look through to the features of the underlying assets and liabilities to decide whether it displays the Tier 1 features [3C.2, 3C.3]. That is the rule through which every actuarial modelling decision — assumption setting, contract boundaries, management actions, TMTP — reaches regulatory capital, and it is why the reconciliation reserve, not the technical provisions, is the number to reconcile first. The 3C.1(3) items subtracted are paid-in ordinary share capital and premium; paid-in initial funds or the mutual equivalent; paid-in subordinated mutual member accounts; **surplus funds not treated as insurance obligations under Surplus Funds 2.1**; and paid-in preference shares and premium. So a with-profits estate leaves the reconciliation reserve through 3C.1(3) and re-enters own funds directly as its own Tier 1 unrestricted item under 3A.1(1)(d) [REG-R77][REG-R45]. **Foreseeable dividends are a capital-management input, not a projection output**: the model must accept the figure, never derive it.

**Tiering, and the deduction.** Tier 1 unrestricted for a UK life insurer is share capital and premium, surplus funds and the reconciliation reserve; **restricted Tier 1** is paid-in subordinated mutual member accounts, paid-in preference shares and paid-in subordinated liabilities; Tier 2 is dated subordinated debt meeting the 3E features; Tier 3 is **an amount equal to the value of net deferred tax assets** plus instruments failing the Tier 2 tests [REG-R77 3A.1, 3D.1, 3F.1]. Deduct the **full value** of a participation in a financial or credit institution exceeding **10%** of the sum of 3A.1(1)(a), (b), (d) and (f) — ordinary share capital, initial funds, **surplus funds** and the reconciliation reserve — and the aggregate of all other such participations to the extent it exceeds the same 10% base, pro rata, taken from the corresponding tier [3K.1–3K.5].

**The tier limits, as a clamp.** Two chapters are live simultaneously and **are not arithmetically equivalent** — Chapter 4 (dated 01/01/2016) expresses the limits as shares of *eligible own funds*, Chapter 4A (dated 31/12/2024) as shares of *the requirement*. SS2/15 ¶1.3(d) states that "for the purposes of Own Funds 4, Own Funds 4A sets out the applicable limits", which is the PRA's own reconciliation. **The tension is recorded, not resolved** [REG-R77][REG-R83]. Implement 4A:

```
covering the SCR   [4A.1]:  Tier 1          >= 50% of the SCR
                            Tier 3           < 15% of the SCR
                            Tier 2 + Tier 3 <= 50% of the SCR
covering the MCR   [4A.2]:  Tier 1          >= 80% of the MCR
                            Tier 2          <= 20% of the MCR
                            Tier 3 is NOT ELIGIBLE to cover the MCR at all
sub-limit          [4A.3]:  restricted Tier 1 + items grandfathered under Transitional Measures 4.1
                            <  20% of TOTAL Tier 1 own funds items
```

**Transitional Measures 4.1 was not retrieved and its content is [unverified]** [REG-R57][REG-R77]. Note the consequence of 4A.2: **eligible own funds for the MCR are a different number from eligible own funds for the SCR**, computed from the same stack — carry both, never one.

**The MCR, as a clamp on the SCR** [REG-R78 MCR 3.1A, 3.1B, 3.2, 3.3]:

```
MCR          = max( MCR_combined , AMCR )
MCR_combined = min( max( MCR_linear , 0.25 * SCR ) , 0.45 * SCR )
AMCR         = GBP 3,500,000 for long-term insurance (also for pure reinsurers; GBP 2,400,000 for
               general insurance, GBP 3,500,000 where any of GI classes 10-15 are covered,
               GBP 1,200,000 for captive pure reinsurers; composites take the sum of the two)
```

MCR 3.3 adds, independently of the absolute floor, that the MCR "must neither fall below 25% nor exceed 45% of the firm's SCR **including any capital add-on which has been imposed**"; **3.1B does not repeat the add-on wording and 3.3 is the only place it appears** [REG-R78]. For every product in this library the floor is **£3,500,000**. The linear component for long-term business [3C.1]:

```
MCR_linear_l = 0.037 * TP_l1 - 0.052 * TP_l2 + 0.007 * TP_l3 + 0.021 * TP_l4 + 0.0007 * CAR

TP_l1 = guaranteed benefits for obligations WITH PROFIT PARTICIPATION (plus reinsurance accepted
        where the underlying obligations include profit participation)
TP_l2 = FUTURE DISCRETIONARY BENEFITS for obligations with profit participation
TP_l3 = LINKED long-term liabilities
TP_l4 = ALL OTHER long-term obligations
each: technical provisions WITHOUT the risk margin, net of reinsurance and SPV recoverables,
      FLOORED AT ZERO SEPARATELY FOR EACH TERM
CAR   = total capital at risk, per contract max(0, A - B), floored at zero PER CONTRACT
```

**The −0.052 on `TP_l2` is the only negative coefficient in the formula**: a larger future-discretionary-benefit reserve *reduces* the linear MCR. The recoverables netted off must exclude amounts that cannot be taken into account under TPFR 23.3 and 23.5 and amounts from arrangements failing the `SCR-SF 3G` risk-mitigation criteria [3C.2]. The MCR must be calculated **at least quarterly**, and where **either** corridor limit determines it the firm must give the PRA information allowing a proper understanding of the reasons [4.1, 4.2].

Two implementation points. First, the **per-term zero floor** means a negative best estimate does not offset a positive one across buckets — a protection book with `BEL < 0` contributes `TP_l4 = 0` while its `CAR` term stays large, so **the folk rule that "the MCR is 25% of the SCR" fails for pure protection**; check which limb binds rather than assuming. Second, the second limb of `A` in the capital-at-risk definition — "the expected present value of amounts **not covered in (i)** that the firm would pay in future on the **immediate** death or disability of the persons insured" — requires a "sum payable on immediate death" attribute on every model point that is distinct from the projected death benefit stream [REG-R78 3C.1(5)].

**What a breach costs, as deadlines the projection must respect** [REG-R82]. SCR: notify the PRA immediately (and on a *risk* of breach within three months); a realistic **recovery plan** within two months; restore within **six months**, extendable, with a progress report every three months if extended for an exceptional adverse situation. MCR: notify immediately; a short-term realistic **finance scheme** within **one month**; restore within **three months**. Either plan must contain estimates of management expenses and commissions, estimates of income and expenditure for direct business and reinsurance accepted and ceded, **a forecast balance sheet**, the financial resources intended to cover technical provisions, the SCR **and** the MCR, and the overall reinsurance policy [5.1]. **This is the only place in the retrieved material where a projected solvency balance sheet is required by rule rather than by supervisory expectation.**

**EPIFP does not exist in Solvency UK reporting.** The Own Funds Part has zero occurrences of "expected profit"; PS3/24 ¶4.44 records that the EPIFP requirement is being **removed from all reporting, including disclosure** [REG-R77][REG-R86]. A UK model therefore does **not** need the EPIFP decomposition (re-run the BEL with future premiums nil and take the difference) that an EU model still needs; the economics survive inside the reconciliation reserve, unisolated. Whether the Delegated Regulation's Article 1(46) definition remains operative UK law at all after PS15/24 is **not settled** [REG-R49].

---

## Ring-fenced funds and with-profits capital

**The trigger and the definition.** A firm with a **ring-fenced fund** — other than one whose restricted own funds have been fully deducted from the reconciliation reserve under Own Funds 3L.2 — **or a matching adjustment portfolio** must follow `SCR-SF 9` [REG-R62 `2.2`]. A ring-fenced fund is an identifiable unit of assets and liabilities whose restriction gives rise to **restricted own funds**, **other than a matching adjustment portfolio**; restricted own funds exclude **the value of future transfers attributable to shareholders** [REG-R43]. RFFs and MA portfolios are therefore **disjoint categories receiving the same treatment**, and a with-profits fund's expected future shareholder transfer is *not* trapped in the ring fence. The PRA expects that UK with-profits restrictions "will generally mean that **each with-profits fund displays the characteristics of a RFF**", and that a **sub-fund** required to be treated as a separate with-profits fund under FCA COBS 20 is treated as **a separate RFF** [REG-R71 ¶¶2.2–2.3][REG-R9]. A three-sub-fund with-profits insurer therefore runs **at least four** notional SCRs.

**The numerator effect** [REG-R77 Own Funds 3L]:

```
3L.1  reduce the excess of assets over liabilities, for the reconciliation reserve, by
          max( 0 , restricted own funds within the RFF or MA portfolio
                   - notional SCR of that RFF or MA portfolio )
      standard formula firms: notional SCR under SCR-SF 9.1
      internal model firms:   notional SCR from the internal model, as if the firm pursued only
                              the business in that fund
3L.2  where the assets, liabilities and risk in a ring-fenced fund are NOT MATERIAL, reduce the
      reconciliation reserve by the TOTAL restricted own funds instead - and, per SCR-SF 2.2,
      no notional SCR is then required for that fund
```

**Restricted own funds count towards entity own funds only up to the capital the fund itself needs**; the classic surplus estate above the fund's own SCR is struck out.

**The denominator effect** [REG-R62 `9.1`]. Compute a notional SCR for **each RFF, each MA portfolio and the remaining part**, as if each were a separate firm; **the firm's SCR is the sum of them**; for every scenario-based module compute the impact on basic own funds at each of those levels; **at fund level basic own funds include only restricted own funds**; and — the step most often implemented wrongly — **notwithstanding that each is computed as a separate firm, each notional SCR must use the scenario under which the basic own funds of the FIRM AS A WHOLE are most negatively affected**, found by summing the scenario impacts across all funds and adding the remaining part [`9.1(1)`–`9.1(8)`]. Finally, **no diversification is allowed between ring-fenced funds, matching adjustment portfolios and the remaining part** [`9.1(9)`]. So the correlation matrices are applied **within** each notional SCR and never across them, and a notional SCR can be driven by a scenario that is not the worst for that fund.

**Profit participation inside a ring-fenced fund** [`9.1(5)`]: where the scenario **increases** the fund's basic own funds, reduce the increase by the increase in technical provisions from the increase in FDB the firm would expect to pay; where it **decreases** them, reduce the decrease — **for the purposes of the net basic SCR under 6.3(2)** — by the reduction in FDB; and that reduction **must not exceed the FDB included in the technical provisions for that fund**.

**Surplus funds — how the estate becomes Tier 1.** The chain, rule by rule: TP 9.1(3) requires all payments to policyholders including future discretionary bonuses to be in technical provisions, "**unless those payments fall within Surplus Funds 2.1**" [REG-R1]; Surplus Funds 2.1 says a firm **shall not treat surplus funds as insurance obligations** when valuing payments to policyholders in the technical provisions [REG-R45]; SS13/15 ¶2.1 conditions that carve-out on the surplus funds meeting the **Tier 1** requirements in Own Funds 3.1, and ¶2.3 records that they will normally meet the Tier 1 criteria but are "likely to be treated as part of a ring-fenced fund" [REG-R46]; and Own Funds 3A.1(1)(d) makes them a **Tier 1 unrestricted item in their own right** [REG-R77]. They are therefore Tier 1 **and** restricted, and everything above applies to them. The computation, per with-profits fund [REG-R45 Surplus Funds 3.1]:

```
surplus funds = with-profits assets                                                        3.1(1)
              - with-profits policy liabilities                                            3.1(2)
              - tax and other costs on recognition of future shareholder transfers
                properly attributable to the fund, to the extent not in 3.1(2)              3.1(3)
              - other liabilities properly attributable to the fund                        3.1(4)
              - THE VALUE OF FUTURE SHAREHOLDER TRANSFERS relating to policies in the
                fund which may properly be made out of it under the FCA Handbook           3.1(5)
```

*with-profits assets* excludes assets meeting liabilities in respect of **non-profit** insurance written in the fund [1.2]. With-profits policy liabilities are **retrospective by default** — the regulatory asset share, a ten-item signed roll-up of premiums received; investment income and asset value movements; **permanent enhancements**; past miscellaneous surplus or deficit allocated; expenses incurred or deducted; past deductions for the cost of guarantees, smoothing, options and life cover; partial benefits paid or due; attributable tax; reinsurance amounts; and past shareholder transfers **less any implicit allowance for the value of future shareholder transfers** [3.3]. **This is the one place in the library where a model must carry history rather than a projection.** The **prospective** basis applies only where the retrospective value "does not adequately reflect the value" or is impracticable, and is the net present value of future premiums, expenses, planned deductions for guarantees/smoothing/options/life cover, benefits, reinsurance and tax [3.2, 3.4] — with the benefits limited to guaranteed benefits (including guaranteed surrender and paid-up values), contractually-entitled declared bonuses, and future discretionary additions **only to the extent consistent with what the retrospective calculation would have allowed for** [3.5]. That consistency clamp is what stops the prospective basis being used to inflate policyholder liabilities and shrink the estate.

Four PRA expectations that change the numbers [REG-R46]: **the surplus funds calculation does not refer to or include a risk margin**, which still sits on the technical-provisions side for the business as a whole — so surplus funds and technical provisions are **not a clean partition** of the with-profits fund (¶2.4); **whole-of-life** is the named case for the prospective basis (¶3.1); grouping is permitted where it gives **the same or a higher** result, does not materially misrepresent exposure or misstate the cost of guarantees, options or smoothing, and groups policies with similar attributes **including the status of guarantees** (¶3.2); and **estate distributions in run-off are excluded from projected benefits** (¶3.6) — which is what keeps the estate in own funds rather than technical provisions. **Whether estate distributions belong in the TP 9.1(3) best estimate is not answered by any retrieved source**; ¶3.6 speaks only to the surplus-funds calculation. Surplus-fund valuations must be **consistent with the methodology used for technical provisions** [4.1], and the With-Profits Part additionally requires each fund's assets to cover its with-profits policy liabilities and its distribution strategy to be **affordable and sustainable** [REG-R80].

---

## Projecting the balance sheet forward

**What forces it.** The ORSA requires a forward-looking multi-year projection of overall solvency needs, own funds by tier, the SCR and the MCR, computed **both with and without the MA, VA, risk-free transitional and TMTP**, at least annually and **without delay after any significant change in the risk profile**, reported within **10 business days of concluding the ORSA** [REG-R92 3.8–3.12]; SS19/16 §5.2 describes "a three to five year forecast" [REG-R95]. **IR.05.10 requires one actual year plus three plan years** of own-funds generation and SCR and risk-margin run-off, split current backbook versus planned new business, with TMTP run-off, new-business strain on a discrete-year basis, experience/economic/other variances, management actions, assumption changes, model changes, portfolio transfers, **shareholder transfers from with-profits funds**, debt and equity movements and dividends, closing to eligible own funds and SCR that must reconcile to IR.23.01.01 — for firms with life premiums excluding unit-linked above **£1bn** in any of the three most recent reporting years [REG-R90]. And a recovery plan or finance scheme requires a **forecast balance sheet** by rule [REG-R82].

**The nesting, and its cost.** For each outer path ω and future date t:

```
state(w,t)  <- project the product model from the valuation in-force to t under path w
BEL(w,t)    <- Mode-V valuation at state(w,t) on the curve prevailing in w at t
RM(w,t)     <- CoC * SUM_s SCR_ref(w,t,s) * taper(s) / (1+r(s+1))^(s+1)     <- a run-off INSIDE
SCR(w,t)    <- the whole standard formula at state(w,t), gross and net, per fund
OF(w,t)     <- A(w,t) - BEL(w,t) - RM(w,t) - other liabilities, then tiered and clamped
```

Cost is `N_paths × T × (SCR cost) × (RFFs + MA portfolios + 1)`, and the SCR cost already contains a full BEL revaluation per stress and a risk-margin run-off per date. **Three nesting levels, not one.**

**Mitigations, in the order to try them.**

1. **Formulaic first.** The `7.8`–`7.14` simplifications turn most life sub-modules into closed forms over capital at risk, modified durations, weighted average rates and surrender strain [REG-R62]. These are the cheapest mitigation and the only one with rule text behind it — subject to the `7.2` error assessment, and remembering that `6.3(2)(d)` changes the net run when they are used.
2. **Drivers.** The approach set out under "The risk margin", applied to the whole SCR rather than only to `SCR(t)`. **[std]** — rationale: no rule sanctions it; TPFR 27.4 and `SCR-SF 7.2` are the only gates, and both demand a documented error evaluation.
3. **Proxy or replicating models.** A fitted surface over the risk drivers, refitted at a validation cadence. The reference for how to validate one is the IFoA proxy modelling working party's framework and its **annuity-portfolio case study** [REG-R36], which is directly load-bearing here because it specifies what the heavy model must expose for the proxy to be fitted and tested at all. `SCR-IM 10.10` permits a **simplified SCR calculation using results from the previous calculation** for the remaining part, but requires evidence on request that the carried-forward results would **not be materially different** from a fresh calculation, and it is **not** available for the `SCR-GP 4` duties [REG-R81]. **That "not materially different" demonstration is the model hook: a proxy must carry its own validation-against-full-run evidence.**
4. **Grouping and compression**, only within TPFR 20.1(2) — and note that limb (c) demands approximately the same result **in particular in relation to financial guarantees and contractual options**, which is exactly where compression fails [REG-R41].

**Circularities that must be broken explicitly.** (a) `Adj_DT` depends on `BSCR + Adj_TP + SCR_op`, and the deferred tax balance depends on the Solvency UK balance sheet, which depends on the SCR through nothing — so the LACDT loop terminates by construction *provided* the model computes `Adj_TP` first and does not feed `Adj_DT` back into `BSCR`. Assert the ordering [REG-R62 `6.4(1)`]. (b) The MCR corridor depends on the SCR, and the eligible-own-funds test for the MCR depends on the MCR — resolve by computing the SCR, then the MCR, then both eligibility tests, never iterating. (c) Own Funds 3L.1 deducts restricted own funds **above the fund's notional SCR** from the reconciliation reserve, while the fund's notional SCR is computed on **restricted own funds only**: compute the notional SCR first from the fund's own balance sheet, then apply the deduction; do not iterate. (d) Where a firm elects the 3L.2 materiality simplification, the notional SCR is **not** required at all — take that branch before computing anything [REG-R62 `2.2`][REG-R77 3L.2].

**Two governance outputs that are themselves projections.** The **Analysis of Change** requires a year-on-year walk from the prior financial year end SCR to the current one with reasons and documentary evidence, submitted from the first financial year end on or after **31 December 2025** — so the model must be able to **re-run the prior year end on the prior basis** and step it forward [REG-R81 13A]. And **solvent exit analysis** requires a documented run-off of policyholder liabilities with its resources and costs, updated on material change and **at least every three years**, under rules in force **30 June 2026** [REG-R98].

---

## Statutory accounts and tax roll-forward

**The mapping.** The same cash flow engine produces three different answers: the **Solvency UK regulatory balance sheet** above; the **statutory accounts** — Companies Act accounts under FRS 102 + FRS 103 (or FRS 101), *or* IAS individual accounts under UK-adopted IFRS 17 [REG-R103][REG-R99][REG-R38]; and the **tax** computation, which is not a liability measurement at all but is built from the accounts with the Finance Act 2012 overlay [REG-R17][REG-R18]. Set a per-entity basis flag: the two accounts routes are structurally different and cannot be mixed in one set of individual accounts.

**Acquisition costs and DAC — the U.S. story reversed.** Under U.S. statutory accounting acquisition costs are expensed as incurred, there is no DAC asset, and first-year surplus strain follows. **In the UK the opposite holds by company law**: SI 2008/410 Schedule 3 **para 13** requires costs of acquiring insurance policies incurred in one financial year but relating to a subsequent year to be **deferred**, with DAC at assets item **G.II** and its movement at technical account item **8(b)** [REG-R105]. FRS 103 ¶3.7 requires deferral except to the extent the costs have already been recovered, the net present value of margins is not expected to cover the DAC after providing for contractual liabilities and expenses, or future premiums and margins are insufficiently certain given expected discontinuance; ¶3.9 amortises DAC over a period **no longer than one in which, net of related deferred tax, it is expected to be recoverable out of margins on related contracts in force at the reporting date, and in a similar profile to those margins** — **no amortisation basis is prescribed; the profile follows the margin profile** [REG-R99]. Note 17 to Schedule 3 removes DAC to the extent the long-term business provision (item C.2) or the linked provision (item D) **already allows for the costs**, explicitly or implicitly through anticipation of future income — which is how a zillmerised or gross-premium reserve absorbs acquisition costs inside the liability instead. **Make that a configuration switch, not an accident** [REG-R105].

FRS 103 ¶3.10 says acquisition costs **shall not** be deferred for with-profits funds — but ¶3.1(b) applies ¶¶3.10–3.15 only to with-profits business to which the PRA **realistic capital regime** (INSPRU 1.3 as at 31 December 2015) was applied before 1 January 2016, while ¶3.7 opens "Except as required by paragraph 3.10", and IG1.1 says an entity **may but need not** adopt ¶3.12 outside that scope. **A with-profits fund never in the realistic regime is not caught by the ¶3.10 prohibition on its own terms. Record the ambiguity; do not assert a resolution** [REG-R99][REG-R100]. Three contrasts to carry: **IFRS 17 has no DAC asset either, but for the opposite reason** — acquisition cash flows sit inside the fulfilment cash flows and **reduce the CSM at initial recognition**, emerging as reduced revenue over the coverage period, with the premium element intended to recover them added back to insurance revenue against an equal service expense [REG-R106]; and **Solvency UK has no DAC at all** — acquisition expenses are simply projected outflows inside the best estimate [REG-R1].

**The liability adequacy test — the only UK GAAP measurement floor** [REG-R99 ¶¶2.14–2.16]:

```
carrying amount of recognised insurance liabilities
   LESS related DAC and related intangibles          (related REINSURANCE assets are NOT considered)
compared against a CURRENT-ESTIMATE projection of all contractual and related cash flows,
   INCLUDING cash flows from embedded options and guarantees
if inadequate -> THE ENTIRE DEFICIENCY is recognised in profit or loss
```

This is where a UK GAAP model must run a current-assumption, option-and-guarantee-inclusive projection even when the recognised liability is a locked-in net-premium reserve, and it is the mechanism through which adverse experience first hits UK GAAP profit — including by writing off DAC. Alongside it sit the product-specific floors: **no policy may have an overall negative provision except as allowed by PRA rules, nor a provision less than any guaranteed surrender or transfer value**, and a linked provision may not be less than the fund-referenced surrender or transfer value [REG-R100 IG2.41, IG2.47]. **So the same business carries a negative best estimate on the Solvency UK balance sheet and a floored provision in the statutory accounts.** Linked business is split on the face of the balance sheet: item **D** for provisions relating to linked investment, item **C.2** for additional provisions covering death risks, operating expenses and other risks such as maturity benefits and guaranteed surrender values [REG-R105 note 26].

**With-profits under UK GAAP.** The recognised liability is the **realistic value of liabilities** (defined by reference to INSPRU 1.3.40 as at 31 December 2015) **adjusted to exclude the shareholders' share of projected future bonuses**, with reinsurance measured consistently, optional recognition of the present value of future profits on non-participating business written in the fund, and the consequential tax effects — and **the adjustments from the modified statutory solvency basis go through profit or loss with an equal and opposite net transfer to or from the fund for future appropriations** [REG-R99 ¶¶3.12–3.14]. So there is generally **no change in reported profit**, except where the adjustments produce a **negative FFA balance** and the entity deducts it from equity through profit or loss [REG-R100 IG1.10]. The shareholders' share is valued on **market-consistent financial assumptions**, with non-economic assumptions consistent with the realistic liability [IG1.2]; options and guarantees within the ¶3.1(b) scope **must** be at fair value or by a market-consistent stochastic model, and for all long-term business a deterministic approach "will generally fail to deal appropriately with the time value of the option" [IG1.11, IG1.12].

**IFRS 17, to the level the research supports and no further** [REG-R106]. Aggregation is by **portfolio × profitability bucket × annual cohort**, groups fixed at initial recognition and **never reassessed**. Measurement is fulfilment cash flows — probability-weighted expected cash flows within the boundary, current and explicit, entity perspective, market variables consistent with observable prices, **discounted at an entity-determined curve satisfying IFRS 17:36 (not the PRA curve)** — plus an **explicit risk adjustment for non-financial risk, for which no confidence level is prescribed in the retrieved material**; contrast the Solvency UK risk margin, a cost-of-capital calculation at a fixed 4% with λ tapering [REG-R4]. The CSM at initial recognition is a **residual** set so no income or expense arises, and is **zero with an immediate loss** for a group onerous at initial recognition. The roll-forward:

```
CSM(t) = CSM(t-1)
       + interest accreted            GMM: at LOCKED-IN rates      VFA: at CURRENT rates
       + changes in FCF relating to FUTURE service
         VFA additionally: the entity's SHARE of the change in fair value of the underlying items
       - the amount recognised as insurance revenue for services provided in the period,
         determined by COVERAGE UNITS reflecting the QUANTITY OF BENEFITS provided and the
         expected coverage period
       floored at zero; any shortfall becomes a LOSS COMPONENT
```

**The coverage-unit driver is a required model output, not a reporting-layer choice.** The primary GMM/VFA difference is that changes in fulfilment cash flows from the time value of money and financial risk go to the **CSM** under VFA and **immediately to insurance finance income or expense** under GMM. UKEB's UK expectation is **GMM for protection and annuities, VFA for unit-linked and with-profits, PAA for short-term contracts** [REG-R106]. Nothing beyond this is asserted; the standard text itself was not fetched.

**Tax — the I-E computation, as steps** [REG-R17 FA 2012 s.73][REG-R18 LAM02060]:

```
Step 1  income chargeable for the period referable to BLAGAB (s.74 meaning of "income")
Step 2  BLAGAB chargeable gains as adjusted for allowable losses (s.75)
Step 3  so much of any I-E receipt under s.92 or s.93(5)(a) as is not already in Step 1 or 2
Step 4  I = Step1 + Step2 + Step3, reduced by the RELIEVABLE AMOUNT of any non-trading deficit
            under CTA 2009 s.388, capped at (Step1 + Step2 + any s.92 receipt in Step3)
Step 5  E = adjusted BLAGAB management expenses (s.76)
Step 6  I - E   positive -> I-E PROFIT, chargeable under s.68
                negative -> EXCESS BLAGAB EXPENSES, carried forward into the next period's s.76 Step 5
```

"E" is computed broadly like an investment company's management expenses: **claims, reinsurance premiums and other insurance-related items are excluded** [REG-R18 LAM04010]. The **seven-year acquisition-expense spread** at FA12 s.79 — 1/7th relieved in the period, 6/7ths deducted at s.76 Step 2 and brought back at Step 3 over the next six periods — **is repealed for accounting periods beginning on or after 1 January 2023**, from which date the deduction follows recognition in the income statement under GAAP; two savings survive, the run-off of pre-2023 spread amounts and the s.77(3) disallowance of a deduction for acquisition costs that arose earlier but are recognised after the transition, so relief is given **only once** [REG-R18 LAM04110, LAM04130][REG-R109]. The **minimum profits test** compares the I-E profit (or excess expenses as a negative) with the BLAGAB trade profit after the s.94 adjustment adding non-taxable distributions into "I"; any excess of trade profit becomes an **I-E receipt** at s.73 Step 3 **and the same amount is carried forward as a BLAGAB management expense** at s.76 Step 5 [REG-R18 LAM07230]. The **policyholder/shareholder split**: for a mutual the **whole** I-E profit is policyholders'; otherwise the first slice up to the "adjusted amount" of BLAGAB trade profit is taxed at the main corporation tax rate and the balance at the **policyholders' rate**, which FA12 s.102(3) fixes as the basic rate of income tax **applying in England, Wales and Northern Ireland — the Scottish basic rate does not apply** [REG-R18 LAM06010, LAM06020]. HMRC's own worked illustration uses **2018 rates** under which corporation tax sat below the policyholder rate; at the access date the main rate is **25%** and the basic rate **20%**, so **the direction of the incentive in that example is inverted on current rates** [REG-R18 LAM01160][REG-R110]. Tag every projected cash flow, asset and liability **BLAGAB / non-BLAGAB**, and use one commercial allocation basis consistently for income (s.98), gains (s.101) and trade profits (s.115) — consistency does not require an identical approach, but "the overall effect of the methods taken together must be fair" [REG-R18 LAM05020].

**Deferred tax needs three liability measures, not two.** FRS 102 Section 29 recognises deferred tax on **timing differences** — differences between taxable profits and total comprehensive income arising from items entering tax assessments in different periods — with no deferred tax on permanent differences [REG-R102 ¶29.6, ¶29.10]. Valuation 11 measures it on **all** assets and liabilities **including technical provisions**, as the difference between the **Solvency UK value and the tax value**, recognising a positive value only where future taxable profit is probable, taking account of carry-forward time limits [REG-R39 Val 11.1–11.3]. **These are structurally different numbers for the same company**, so a model that projects deferred tax must carry the accounts liability, the tax liability and the Solvency UK liability per period. Two anti-double-count rules: where the long-term business provision or the linked provision has had regard to the **timing of tax relief or the tax obligation**, that effect must be **excluded from the determination of deferred tax** [REG-R100 IG2.44, IG2.49]. Finally, **distributable profits are owned by the prudential balance sheet, not the accounts**: for a Solvency-II-authorised long-term insurer s.833A CA 2006 substitutes an assets-less-liabilities-less-deductions formula for the realised-profits test, with the accounts' accumulated profits as a **cap**, and the deductions include the **ring-fenced fund surplus** and the **matching adjustment portfolio surplus** — the two largest for a with-profits and an annuity writer respectively [REG-R104].

---

## Worked example — one policy, carried through

The three-year term assurance from "The best estimate liability", carried to a coverage ratio. Every additional assumption is **[std]** with its rationale stated; the point is that a reader can reproduce every figure by hand.

**Additional [std] assumptions.** (i) The firm holds assets of **500** in an instrument assumed to attract **no market and no counterparty charge** — rationale: this isolates the liability-driven modules, and the counterparty PD table, the concentration aggregation formula and the ECAI-to-CQS mapping were all deliberately not transcribed [REG-R62][REG-R72], so any asset charge stated here would be invented. (ii) Earned premium in the previous 12 months equals earned premium in the last 12 months — rationale: suppresses the operational growth surcharge, which on a one-policy start-up would otherwise double the charge and obscure the mechanic. (iii) No deferred tax on the balance sheet, so `Adj_DT = 0` — consistent with `6.4(6)` (a positive change gives nil) and `6.4(3)` (a DTA increase may not be used) [REG-R62]. (iv) No reinsurance, no future discretionary benefits, no ring-fenced fund, no MA portfolio, so `Adj_TP = 0` and one run suffices. (v) In `CAR`, the "best estimate of the corresponding obligations" is read as the best estimate of the **death benefit** obligations — rationale: the rule says "corresponding obligations" and the research transcribed no interpretation; the reading is the drafter's. **The rule forks here and the library records the fork rather than resolving it** [std, reading of MCR 3C.1(5)]: on this **benefit-obligation** reading the deduction is a positive present value and `CAR` sits just *below* the sum assured, as Step 6 computes; on the **whole-contract** reading the deduction is the contract's own best estimate, negative wherever future premiums sit inside the boundary, so `CAR ≈ SA + |BEL|` and sits *above* the sum assured. The two readings move `MCR_linear` in opposite directions and no retrieved source settles which is intended. `uk/products/term-assurance/technical-notes.md` and `uk/products/critical-illness/technical-notes.md` both discuss the whole-contract reading at their own MCR bullets; the worked example below adopts the benefit-obligation reading throughout, so a figure taken from it must not be mixed with one taken on the other basis.

**Step 1 — the stressed best estimates.** Each is a complete re-run of the projection on the stressed assumption set, floored at zero relative to the base [REG-R62 `3.3A(5)`].

| Stress | Rule | Stressed assumption | `BEL_stressed` | `SCR_i = ΔBEL` |
|---|---|---|---|---|
| Mortality | `3B1.1` | `q` = 0.0023 (=0.002 × 1.15) at all durations | 59.340902 | **83.1318** |
| Life catastrophe | `3B7.1` | `q(year 1)` = 0.0035 (=0.002 + 0.0015); later years unchanged | 120.659445 | **144.4504** |
| Life expense | `3B4.1` | expenses × 1.10 and inflation 0% → 1% | 5.778001 | **29.5689** |
| Life lapse — mass | `3B6.6(2)` | 40% discontinuance; surrender value nil, so discontinuance takes the BEL to 0 and **increases** TP by 23.790911 | — | **9.5164** |

Lapse up and lapse down are **nil** here: base lapse rates are zero and `3B6.2`/`3B6.3` are *relative* changes to exercise rates, so the mass event wins the three-way maximum by construction. The mass-lapse figure is `0.4 × 23.790911 = 9.516364`, i.e. 40% of the loss of basic own funds per policy — and it is the clearest illustration of why a negative best estimate is a capital exposure, not a windfall.

**Step 2 — aggregate the life module** on the `3.8(3)` matrix, using the rounded sub-module figures (mortality 83.1318, expense 29.5689, lapse 9.5164, catastrophe 144.4504) and the correlations mortality/expense 0.25, mortality/lapse 0, mortality/cat 0.25, expense/lapse 0.5, expense/cat 0.25, lapse/cat 0.25:

```
sum of squares  = 6910.896171 + 874.319847 + 90.561869 + 20865.918060 = 28741.695947
cross terms     = 2*0.25*mort*exp   = 1229.057941
                + 2*0.00*mort*lapse =    0.000000
                + 2*0.25*mort*cat   = 6004.210881
                + 2*0.50*exp*lapse  =  281.389480
                + 2*0.25*exp*cat    = 2135.619716
                + 2*0.25*lapse*cat  =  687.323893
total           = 39079.297858        SCR_life = sqrt(...) = 197.6848
```

**Step 3 — BSCR, operational risk, SCR.** Market, counterparty, health, non-life and intangible are all nil by assumption (i), so `BSCR = SCR_life = 197.6848`. Operational risk: `Op_premiums = 0.04 × 300 = 12.0000` with the growth surcharge nil by assumption (ii); `Op_provisions = 0.0045 × max(0; −23.790911) = 0` — **the negative best estimate zeroes the provisions leg entirely**; `Op = max(12, 0) = 12`; `min(0.3 × 197.6848; 12) = min(59.3054; 12) = 12`; `Exp_ul = 0`. So `SCR_operational = 12.0000`, and with `Adj_TP = Adj_DT = 0` the requirement is `SCR = 197.6848 + 12.0000 + 0 =` **209.6848**.

**Step 4 — the risk margin** is the run-off computed in "The risk margin": `RM = 21.045512`. `TP = BEL + RM = −23.790911 + 21.045512 = −2.745399`.

**Step 5 — the balance sheet, own funds and the ratio.**

| Item | Value | Source |
|---|---|---|
| Assets | 500.000000 | [std] |
| Technical provisions | −2.745399 | BEL + RM [REG-R1 TP 2.4] |
| Other liabilities | 0.000000 | [std] |
| **Excess of assets over liabilities** | **502.745399** | [REG-R77 2.2] |
| Basic own funds (no own shares, no subordinated liabilities) | 502.745399 | [REG-R77 2.2] |
| — of which paid-in ordinary share capital, Tier 1 unrestricted | 500.000000 | [REG-R77 3A.1(1)(a)] |
| — of which reconciliation reserve, Tier 1 unrestricted | 2.745399 | [REG-R77 3A.1(1)(f), 3C.1] |
| Eligible own funds to cover the SCR | 502.745399 | limits 4A.1 all satisfied |
| **SCR coverage ratio** | **239.8%** | 502.745399 / 209.6848 |

Tier limits, as a clamp: Tier 1 502.745399 ≥ 50% × 209.6848 = 104.842450 ✓; Tier 3 = 0 < 15% × SCR ✓; Tier 2 + Tier 3 = 0 ≤ 50% × SCR ✓; restricted Tier 1 = 0 < 20% of total Tier 1 ✓ [REG-R77 4A.1, 4A.3].

**Step 6 — the MCR.** `TP_l1 = TP_l2 = TP_l3 = 0`; `TP_l4 = max(0, −23.790911) = 0` — floored per term. `CAR = max(0, 100,000 − 553.937898) = 99,446.062102`, so `MCR_linear = 0.0007 × 99,446.062102 = 69.612243`. The corridor: `0.25 × SCR = 52.421200`, `0.45 × SCR = 94.358160`, so `MCR_combined = min(max(69.612243, 52.421200), 94.358160) = 69.612243`. **The linear formula, not the 25% floor, binds** — precisely because the negative best estimate zeroed `TP_l4` while `CAR` stayed at essentially the full sum assured. Then `MCR = max(69.612243, £3,500,000) = £3,500,000`: **on a single policy the absolute floor swallows the entire calculation**, and the corridor arithmetic only becomes visible on a book some tens of thousands of times larger [REG-R78 3.1A, 3.1B, 3.2, 3C.1].

**The reconciliation that must close exactly.** `EAoL = A − TP − other liabilities = 500 − (−2.745399) − 0 = 502.745399`, and independently `share capital + reconciliation reserve = 500 + 2.745399 = 502.745399` ✓. Because there are no other assets or liabilities, **the reconciliation reserve is exactly the negative of the technical provisions** — a one-line unit test of the whole own-funds build for any single-block model.

**The same policy on the other two ledgers.** Solvency UK carries `TP = −2.745399`. UK GAAP carries the 200 acquisition cost as a **DAC asset** (SI 2008/410 Sch 3 para 13, FRS 103 ¶3.7), amortised in the margin profile [REG-R105][REG-R99], and a long-term business provision that **may not be negative** [REG-R100 IG2.41] — so the balance sheet shows a positive provision plus an asset where Solvency UK shows a single negative number. IFRS 17 would carry no DAC asset at all, the 200 having reduced the CSM at initial recognition [REG-R106]. **The U.S. "acquisition costs expensed as incurred, first-year strain" signature does not appear on any of the three UK ledgers.**

---

## Implementation notes and model architecture

**Layering, one direction of dependency [std]** — rationale: the layering is an architectural suggestion, not a rule, but it is the only shape in which the circularities above stay breakable. (1) Product models in `uk/products/` emit cash flows and policy state, **parameterised by assumption set**, never with hard-coded tables. (2) A **valuation layer** turns state plus an assumption set plus a curve into a best estimate — this is the function every stress calls, so its signature is the single most important design decision in the system. (3) A **capital layer** drives the stress harness, aggregates on the correlation matrices, and runs the gross/net pair per fund. (4) A **reporting and ledger layer** produces the templates, the accounts and the tax computation. Two rules on the boundaries: the **discount curve is an input parameter to layer 2, never an assumption inside layer 1**, because the same vector must be discounted five ways; and layer 3 must be able to hold the **risk margin, deferred taxes and (in the gross run) FDB constant** while everything else revalues [REG-R62 `3.3A(1)`] — a real constraint if the risk margin is computed as a by-product of the same projection.

| Once per valuation | Once per stress | Per fund | Per projection path |
|---|---|---|---|
| base BEL per homogeneous risk group, per currency | full BEL revaluation (life, SLT health, interest rate, MA spread) | complete notional SCR, gross and net [REG-R62 `9.1`] | balance sheet, own funds, tiering |
| contract-boundary derivation | zero-floor and TP-increasing-subset selection | restricted own funds and the 3L deduction | SCR and MCR at each date |
| segmentation keys, product codes | scenario-selection bookkeeping (which lapse limb, up or down rates) | FDB balance and its `9.1(5)` adjustment | deferred tax on three bases |
| capital at risk, surrender strain, modified durations | factor-model exposures (concentration, counterparty, operational) | surplus funds and asset shares | DAC, CSM and I-E roll-forwards |

**Practical ordering of a reporting run.** (1) In-force extract; derive contract boundaries and segmentation keys. (2) Base BEL per homogeneous risk group, gross, per currency, on the relevant curve; reinsurance recoverables and the counterparty-default adjustment. (3) Discount the same vector on each required basis and emit the MA internal-rate pair and the matching tests. (4) Stress harness: every scenario-based sub-module, gross run, per fund, floored at zero, with scenario-selection bookkeeping. (5) Factor modules. (6) Aggregate to each notional SCR; **sum across funds with no diversification**. (7) Net run for any fund with FDB; `Adj_TP`. (8) `Adj_DT` from the instantaneous loss `BSCR + Adj_TP + SCR_op`. (9) **Risk margin** — the `SCR(t)` run-off on the reference undertaking configuration, on the basic curve, with no MA/VA/transitional and no LACDT. (10) Technical provisions; TMTP if permitted. (11) Balance sheet, own funds, tiering, the 3L deduction, eligible own funds for the SCR and separately for the MCR. (12) MCR: linear, corridor, absolute floor. (13) Templates, SFCR, accounts and tax. **Step 9 sits after steps 4–8 deliberately**: the reference undertaking's notional SCR reuses the stress harness but on a different configuration, and computing it first invites the harness to be built around the firm's own balance sheet.

**Deadlines the pipeline must meet** [REG-R84][REG-R85][REG-R91][REG-R2][REG-R92]: the SFCR within **70 business days** of financial year end, board-approved before disclosure; MALIR 3 within **130 business days** of year end via BEEDS, on a **31 December** effective date regardless of financial year end; the MA attestation annually at the **SFCR effective date**, delivered within **14 weeks** of year end, and additionally on a **material change in the firm's risk profile** — as soon as reasonably practicable after an attestation reference date no later than **three months** after that change, with the reference date and timescale agreed bilaterally with the PRA [REG-R2 MA 9.1(2), 1.2][REG-R8 ¶5.33]; the ORSA report within **10 business days** of concluding the ORSA; and the MCR at least quarterly [REG-R78 4.1].

---

## Validation and reconciliation checks

Assertable identities. Tolerances are **[std]** — rationale: no retrieved source states one; use exact equality (to floating-point epsilon) for identities that are true by construction, and a stated relative tolerance for anything involving a proxy.

1. **Cash flow inventory completeness.** Every projected amount maps to exactly one of the eight TPFR 13.1 streams, and gross plus ceded reconstruct the direct flows without netting [REG-R41].
2. **Sign preservation.** The unfloored best estimate carries its sign through every aggregation; no stage of the pipeline floors it. Assert `BEL_group = Σ BEL_policy` where grouping is used, and that the group result satisfies the TPFR 20.1(2)(c) comparison against a seriatim run [REG-R41].
3. **Reserve-basis unit test.** Two cash flow streams with identical timing and in-force weights have present values in the ratio of their per-unit amounts — the maintenance-to-premium check in the worked example. Catches a mis-aligned survivorship vector immediately.
4. **Discount separability.** Re-discounting the *same* vector on the basic curve must reproduce `R_liab_basic`, and `MA = R_assets − R_liab_basic` must be recoverable from the two internal rates alone [REG-R2 MA 4.3].
5. **MA eligibility.** The mortality-stress increase in the gross best estimate is **≤ 5%**, and the figure reported at IRR.22.03.01 equals the figure used in the eligibility assessment [REG-R2 MA 2.2(3)][REG-R91].
6. **Zero floor per sub-module.** No scenario-based capital requirement is negative before aggregation [REG-R62 `3.3A(5)`]; and each notional SCR is non-negative before the `9.1(2)` sum.
7. **LACTP bounds.** `0 ≤ BSCR − nBSCR` and `Adj_TP = −max(min(BSCR − nBSCR; FDB); 0)`, so `|Adj_TP| ≤ FDB` always; a violation means the gross and net runs did not come from the same scenario set [REG-R62 `6.3`].
8. **No cross-fund diversification.** `SCR = Σ_f notional SCR(f)` exactly — assert that the sum is a plain sum and that the *same* scenario selection was used in every fund [REG-R62 `9.1(2)`, `9.1(6)`, `9.1(9)`].
9. **Own funds closure.** `EAoL = A − TP − other liabilities` **and** `Σ (own funds items) = BOF`; for a single-block model with no other assets or liabilities the reconciliation reserve equals `−TP`. Both, not either [REG-R77 2.2, 3C.1].
10. **Two eligible-own-funds figures.** The SCR numerator and the MCR numerator are computed separately and differ whenever Tier 2 or Tier 3 is non-zero [REG-R77 4A.1, 4A.2].
11. **MCR corridor.** `0.25 × SCR ≤ MCR_combined ≤ 0.45 × SCR`, `MCR = max(MCR_combined, AMCR)`, each `TP_l` term floored at zero **separately**, and `CAR` floored at zero **per contract** [REG-R78 3.1A, 3.1B, 3C.1].
12. **Template ties.** `IR.12.06 R0150 = IR.12.01.01 R0030/C0010` [REG-R90]; `IR.12.06 R0060 = SUM(R0070:R0120) − R0130 − R0140`; IR.05.03 `R0210:R0270` must sum to `R0180`, and `R0310 = R0150 + R0200 + R0280 + R0290 + R0300` [REG-R90]; IR.05.10 `R0400 = R0180 + R0220 + R0310 + R0320`, with `R0500`/`R0510` reconciling to the prior-year and current-year IR.23.01.01 and the premium block to IR.14.01.01 [REG-R90]. IR.12.01's unit-linked "matching value of units held" ties to IR.02.01 R0220 and R0340 [REG-R89].
13. **Shareholder transfer.** `shareholder transfer = value of bonus × s/(1−s)`, i.e. **one ninth** of the policyholder bonus value in a 90:10 fund [REG-R90].
14. **Surplus-funds boundary.** Surplus funds excluded from technical provisions **only** where Tier 1 eligible, and the surplus-funds calculation contains **no risk margin** — so surplus funds plus technical provisions is *not* the with-profits fund [REG-R45][REG-R46 ¶2.4].
15. **TMTP bounds.** `0 ≤ T_r ≤ A_r + B_r + C_r − W_r`, `C_r` amortising linearly to zero by 1 January 2032, and the applied amount disclosed alongside the maximum where less is taken [REG-R3][REG-R59].
16. **Proxy error.** Any drivers or proxy result is re-validated against a full revaluation at a stated cadence, and the error recorded — this is what `SCR-IM 10.10`'s "not materially different" demonstration and TPFR 27.4 both require [REG-R81][REG-R41]. Suggested tolerance **[std]: 0.5% of the SCR**, chosen only as a starting point for calibration, since no source states one.

---

## Key sensitivities and model risks

- **The reserve is a projection, so proxy error compounds.** A best estimate contains a run-off; the risk margin contains a run-off of SCRs each containing a run-off; the ORSA contains all of it at every future date. An error tolerable at one level is not tolerable cubed [REG-R1 TP 3.1, 4A.1].
- **`3D25` makes spread risk a liability calculation for an MA writer.** Modelling it as an asset-only stress understates the SCR, and the CQS reduction factors give **no** MA offset at CQS 4 and below [REG-R62 `3D25`].
- **The interest-rate direction flips a correlation.** If the charge comes from the up scenario the market matrix carries `A = 0` between interest rate and equity, property and spread; from the down scenario, `A = 0.5`. The market SCR is discontinuous in the balance sheet, and a model that caches the direction across valuations will be wrong at exactly the date it matters [REG-R62 `3.11A(3)`].
- **The net-basis tie-break is easy to get backwards.** In the four "highest of" sub-modules the *scenario* is selected on the net run and the *gross* number reported is the one belonging to that scenario [REG-R62 `3B6.9`, `3C16.9`, `3D4.2`, `3D32.9`].
- **Mass lapse is a per-policy maximum over discontinuance types, including paid-up** — not a blended 40% surrender assumption [REG-R62 `3B6.8`, `1.2`].
- **A unit-linked bond takes 40%, not 70%.** The class III reference in PS15/24 Appendix 6 was declared an error and deleted effective 31 December 2024, but PS15/24 ¶¶6.16 and 6.18 remain published and unamended [REG-R64][REG-R62].
- **Two expense bases, always.** TPFR 16.4 requires the best estimate to assume the firm writes new business; TP 4B.1(5) gives the risk-margin reference undertaking none. Both are printed; no source reconciles them [REG-R41][REG-R1].
- **The risk margin is not the firm's own SCR run-off.** The reference undertaking uses no MA, no VA, no transitional and no TMTP, and has no loss-absorbing capacity of deferred taxes — for an MA annuity book the two bases are materially different [REG-R1 TP 4B.1(11), 4B.1(13)].
- **No UK risk-margin simplification exists.** Delegated Regulation Article 58 was not restated; every proxy stands or falls on TPFR 27.4 alone, and 27.4 has **no "immaterial, therefore ignore" limb** — a simplification is permitted only where nothing better is available and it is not likely to understate, or where it is demonstrably prudent [REG-R41][REG-R49].
- **Ring-fencing costs twice.** Restricted own funds above the fund's notional SCR leave the reconciliation reserve, *and* the entity SCR is a plain sum of notional SCRs with no diversification [REG-R77 3L][REG-R62 `9.1(9)`].
- **The MCR heuristic fails for protection.** A negative best estimate zeroes `TP_l4` while `CAR` stays at nearly the full sum assured, so the linear formula can exceed the 25% corridor floor — the opposite of the usual life shape [REG-R78 3C.1].
- **The 50% LGD floor is rebuttable only on "a reliable basis", which is undefined** in every retrieved source, and it applies per counterparty **and** per line of business [REG-R41 TPFR 24.3, 24.4].
- **A negative best estimate on Solvency UK is a floored provision in the accounts.** IG2.41 forbids an overall negative provision and IG2.47 imposes a fund-referenced surrender-value floor; the two ledgers diverge on the same business by construction [REG-R100][REG-R1].
- **DAC is required in the UK and prohibited in a with-profits fund — with a scope trap.** Schedule 3 para 13 requires deferral; FRS 103 ¶3.10 prohibits it for with-profits funds; ¶3.1(b) limits ¶3.10 to funds inside the pre-2016 realistic capital regime. The interaction is **unresolved in the retrieved text** [REG-R105][REG-R99][REG-R100].
- **Deferred tax is three numbers.** Accounts (timing differences), tax, and Solvency UK (value-versus-tax-value on all items **including technical provisions**). Carrying two guarantees an error somewhere [REG-R102][REG-R39 Val 11.2].
- **The LACDT transitional has expired.** `SCR-SF 6.5` ended **30 December 2025**, so a DTA increase arising from the instantaneous loss **may not be used** [REG-R62 `6.4(3)`, `6.5`].
- **Extraction defects live in this file.** The life correlation matrix's mortality row label is an inference from symmetry; the spread table's merged CQS 5/6 column, the unrated ">5 to 10" missing percent sign, the non-monotonic downward interest-rate shocks at 14–20 years and the bracketing of `Op_premiums` are each **[unverified]** [REG-R62]. Re-read the rule text before hard-coding any of them.
- **Time-sensitive source risk.** TMTP must not be applied after **1 January 2032** [REG-R3 2.3]; PS18/26 changes IR.14.01 from **31 December 2026** [REG-R87]; solvent exit rules commence **30 June 2026** [REG-R98]; `SCR-SF 1.2` has an unretrieved future version after **1 January 2027** [REG-R62]. Re-check all four before relying on anything here for a live submission.
