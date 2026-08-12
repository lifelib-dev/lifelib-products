# U.S. Statutory Accounting and Capital Requirements for Liability Models

- **Status:** Draft, 2026-08-04 (all cited sources accessed 2026-08-04).

**Scope note.** This file covers the U.S. statutory accounting rules and capital requirements **that bear on how a
product is represented in an actuarial model** — which items exist, why they exist, which of the twelve products in
`us/products/` they bite, what a projection must produce, and **how to compute each of them**. Concept and calculation
sit in the same section throughout, so a reader following one subject does not change documents halfway. Product
mechanics stay in `us/products/<type>/`: the product models there emit cash flows and policy state, and this file
consumes them to produce reserves, an IMR/AVR pair, a statutory income statement and surplus roll-forward, and an RBC
calculation. Constructions are lifelib/modelx style: explicit state, explicit recursions, per contract or per model
point.

**Citation conventions** (identical to the rest of the library, non-negotiable). Everything is cited as **[REG-R#]**
against the shared U.S. numbering in `us/references/regulatory-and-actuarial-references.md`, which after this work runs
R1–R157 with permanently unused gaps at **R114–R124** and **R143–R149**. R1–R72 are the frozen pre-existing entries;
R73–R142 are the statutory accounting and capital entries added now, with provenance in
`us/_research/statutory-accounting.md` (R73–R99), `us/_research/statutory-reserves.md` (R100–R113) and
`us/_research/risk-based-capital.md` (R125–R142); **R151–R157 are the seven AP&P Manual appendix items subsequently read
at first hand** — R151 AG 33, R152 AG 35, R153 A-820 with A-821 and A-822, R154 A-830, R155 A-585, R156 A-250, R157
A-255 — with provenance in `us/_research/appp-ag33.md`, `us/_research/appp-ag35.md`,
`us/_research/appp-a820-a821-a822.md`, `us/_research/appp-a830.md` and `us/_research/appp-a585-a250-a255-a270.md`. Every
quantitative parameter, factor, threshold, formula and effective date carries a [REG-R#] tag, or **[std]** where it is a
standardization for the reference implementation, or **[unverified]** where the research could not confirm it. **Nothing
marked [unverified] is upgraded on recollection** — this is a subject on which plausible recollections of factor values
and formula structure are easy to get wrong. An [unverified] item leaves that state **only when the primary text is
read**, which is what happened to the AG 33 and AG 35 mechanics on 2026-08-06 [REG-R151][REG-R152]; every [unverified]
flag not closed that way still stands, and the ones that reading **opened** are listed at the end of this file. The
per-entry bibliography for this directory — every [REG-R#] this document cites, with publisher, URL, access date and
fetched/not-fetched marker carried verbatim from the research files — is `us/regulatory/sources.md`.

**Documents that could not be read, said plainly at the point of use.** (a) The **NAIC Life and Fraternal Risk-Based
Capital Forecasting and Instructions is a sold NAIC publication** marked "Not for Distribution"; the 2024 and 2023
editions used here were read from copies posted by the Indiana Department of Insurance, and the **2025 edition could not
be parsed at all** [REG-R128][REG-R129][REG-R139] — nothing here is asserted about year-end 2025 factors, and the
forecasting spreadsheet was never obtained. (b) The **AP&P Manual is no longer paid** (the *As of March 2026* edition
was retrieved in full [REG-R73], superseding R33's "paid, not fetched" note), and **seven of its appendix items have now
been read in full** and are cited below at first hand: **A-820** with A-821 and A-822 [REG-R153], **A-830** [REG-R154],
**A-585** [REG-R155], **A-250** [REG-R156], **A-255** [REG-R157], **AG 33** [REG-R151] and **AG 35** [REG-R152].
Formulaic CRVM and CARVM below therefore no longer rest on the Standard Valuation Law [REG-R1] and Model #830 [REG-R6]
alone. **What is still unread and named at the point of use:** **Actuarial Guideline I** (the deficiency-reserve
interpretive vehicle) [REG-R41]; **A-791** (reinsurance), cited only through SSAP No. 61 [REG-R92]; **A-270** (variable
life), extracted but with **no reference id assigned**, so nothing is cited from it here; and the mortality-table items
**A-812, A-815, VM-A-814, A-817** [REG-R110]. Note also that neither A-820 nor A-830 prints any of the mortality tables
it names, and A-821 prints only the 2012 IAM Period Table and Projection Scale G2 — the 1994 GAR, Annuity 2000 and 1983
Table "a" are named and **not printed** [REG-R153]. (c) The **AVR factor tables and the IMR grouped-amortisation factor
tables were deliberately not transcribed** [REG-R89]: their role and location are described and **no factor value is
stated for either**. (d) **VM-21 and VM-22 internals were not re-derived**; they are reached through VM-G §1.A, VM-31
§2.A and the RBC instructions' restatement [REG-R109][REG-R108][REG-R128], so that section is an interface
specification, not a transcription [REG-R35][REG-R36].

---

## Why statutory differs from GAAP

Statutory accounting measures **solvency**: obligations must be "met when they come due", with capital and surplus
maintained "at all times … to provide an adequate margin of safety" [REG-R74 ¶30]. Three concepts carry it —
**conservatism**, since "valuation procedures should, to the extent possible, prevent sharp fluctuations in surplus"
[¶33]; **consistency** [¶34]; and **recognition**, under which the balance sheet is primary and "the income statement is
a secondary focus of statutory accounting" [¶35]. A GAAP pronouncement is not part of SAP until the NAIC adopts it
[¶27]; SSAPs sit at Level 1 of the hierarchy [¶42]; the manual does not override state law, hence prescribed and
permitted practices [REG-R99]. Two operative rules follow: assets not usable to meet policyholder obligations are
charged against surplus rather than recognised [¶36]; and "**accounting treatments which tend to defer expense
recognition do not generally represent acceptable SAP treatment**" [¶38].

**The consequence that dominates model output.** SSAP No. 71 ¶2 defines acquisition costs as those incurred in acquiring
new and renewal contracts that "vary with and are primarily related to" acquisition — commissions, certain underwriting
and issue costs, medical and inspection fees — and requires they "**shall be expensed as incurred**", with timing set by
SSAP No. 5 [REG-R75][REG-R91]. **There is no deferred acquisition cost asset in statutory accounting.**

The GAAP contrast is stated precisely in the codification record: "GAAP accounting for policy acquisition costs and
commissions is driven by the objective of matching revenues and expenses, therefore these costs are deferred and
amortized to income as the related premium is recognized as revenue for FAS 60 products **or in proportion to estimated
gross profits for FAS 97 products**. The primary objective of statutory accounting is to measure solvency" [REG-R76 ¶8].
SAP does not merely differ, it **rejects**: SSAP No. 71 ¶6 rejects ASU 2018-12 (LDTI), ASU 2010-26, FAS 60, FAS 97 and
SOP 05-1 [REG-R75][REG-R34]; SSAP No. 56 ¶45 rejects ASU 2018-12, ASU 2022-05 and SOP 03-1 [REG-R83]; Issue Paper No. 50
rejects FAS 60 and FAS 97 [REG-R76 ¶9]; Issue Paper No. 7 rejects FAS 97 ¶28 as amended by FAS 115 [REG-R86 ¶5]. **A
statutory run may not reuse a GAAP DAC, an EGP-based amortisation, an LFPB or an MRB measurement** — the prohibition
rests on those rejection paragraphs [REG-R75 ¶6][REG-R83 ¶45][REG-R76 ¶9][REG-R86 ¶5], not on any GAAP standard;
[REG-R71] is cited only for the GAAP vocabulary (DAC, cohort, MRB, lock-in) that statutory accounting does not have.

The projection consequence is structural: commission, underwriting and issue expense plus the initial reserve all hit
surplus in the issue year against a single year's gross premium, so **a statutory run shows first-year surplus strain
and later profit release from exactly the same cash flows a GAAP run would smooth** [REG-R74][REG-R75][REG-R76]. It is
anti-avoidance-protected: a levelized commission fronted by a third party is "in fact, [a] funding agreement", the
insurer books a liability for the full unpaid principal and accrued interest, and the full initial commission "shall be
recognized immediately as the writing of an insurance contract is the event that obligates the insurer" [REG-R75 ¶¶4–5];
a persistency-based commission accrues **on experience to date** [REG-R77]. SSAP No. 71 was effective January 1, 2001,
its levelized-commission revisions applying to contracts in effect as of December 31, 2021 and new contracts thereafter,
and categorised **nonsubstantive** [REG-R75 ¶7][REG-R77].

---

## Notation and conventions

**The two computational modes.** Most confusion in statutory modelling comes from conflating them; keep them separate in
code, and never let a Mode V routine mutate Mode P state. **Mode V — valuation at a date:** given the in-force at
valuation date τ and a fixed assumption/scenario set, return a *number* — a CRVM or CARVM reserve, a VM-20 NPR/DR/SR, a
VM-21 CTE statistic. Any projection inside Mode V is an instrument of the calculation, discarded once the statistic is
taken; Mode V feeds the annual statement and the RBC pages. **Mode P — projection of statutory quantities forward:**
return a *time series* of statutory balance sheets and income statements at τ, τ+1, …. Mode P feeds cash flow testing,
C-3 Phase I, distributable earnings, and the Model #312 RBC Plan, which requires projected statutory operating income,
net income and capital and surplus for the current year and **at least four succeeding years** [REG-R125 §3.B]. Mode P
contains a Mode V call at every future date; that nesting is the dominant runtime cost and has its own section below.

| Symbol | Meaning |
|---|---|
| τ, t | valuation date (a December 31 unless stated); projection index in integer years from τ, t = 0 at τ (m for months) |
| j, K, G | contract index; VM-20 reserving category ∈ {Term, ULSG, All Other}; model segment or aggregation subgroup [REG-R3] |
| x, s | issue age; policy duration in years (s = 0 at issue) |
| ω, N | scenario index; number of scenarios |
| l_j(t) | in-force / survivorship weight for contract j at t (per policy issued, or a count) |
| F, AV, CSV, NAR | face amount; account value; cash surrender value; net amount at risk (the C-2 definition differs — see below) |
| i_v, i_e, NAER | maximum valuation interest rate **by calendar year of issue** [REG-R1 §4b]; earned rate; net asset earned rate path [REG-R3 §7.H] |
| d_ω(t) | scenario-ω discount factor from t back to 0 on the applicable prescribed path |
| V(τ) | reserve at τ; superscripts **gr** gross of reinsurance, **ced** ceded credit, **net** = gr − ced [REG-R89] |
| A, L, S | admitted assets; liabilities; statutory capital and surplus, S = A − L |
| pre/after tax | RBC components are built pre-tax then tax-adjusted on LR030 before covariance [REG-R128]; VM-20 DR/SR **exclude federal income tax entirely** [REG-R3 §7.A]; cash flow testing **includes** it [REG-R111] |

**Per-contract versus aggregate.** NPR, CRVM and CARVM are seriatim [REG-R1][REG-R3 §3]. The DR and SR are computed for
a *group* within a model segment and allocated to policies in proportion to each policy's minimum NPR, with an explicit
duty to avoid allocating excess to policies that did not produce it [REG-R3 §2.C]. RBC factors read **annual statement
values**, not model quantities [REG-R128] — so a projected RBC ratio needs a projected annual statement, not merely
projected cash flows (inferred from the blank's line sources; **[unverified]** as a stated requirement).

---

## The statutory balance sheet and income statement a model must populate

**The balance sheet.** Assets count only to the extent **admitted**; anything not usable to meet policyholder
obligations is non-admitted and charged against surplus, with the *change* flowing through the Capital and Surplus
Account rather than net income [REG-R74 ¶36]. Liabilities are recorded **when incurred**, and "estimates of losses
utilizing appropriate actuarial methodologies meet the definition of liabilities … and are **not** loss contingencies"
[REG-R91/IP5 ¶¶2–3] — the sentence that makes an actuarial reserve a liability rather than a disclosure, reinforced by
**Issue Paper No. 5 ¶7**'s requirement to accrue even where other valuation criteria do not address the item. (Those
paragraph numbers are the *issue paper*'s; the research read Issue Paper No. 5 in full and SSAP No. 5 only alongside it,
so an SSAP-paragraph cite would be unsupported [REG-R91].) Aggregate reserves for life contracts sit on Liabilities page
Line 1 and tie to Exhibit 5; the IMR sits at Page 3 Line 9.4 and the AVR at Page 3 Line 24.01 [REG-R89][REG-R90].
**Those references come from the 2025 reporting-year blank and instructions and should be re-verified against the 2026
blank before being hard-coded** [REG-R89][REG-R90].

**The income statement.** Life-contract premium is recognised **gross, when due**, including single and flexible
premiums when received; the gross-to-net difference is **loading**, and the change in loading on deferred and
uncollected premium is an **expense**, not a reduction of premium [REG-R79 ¶¶2–5, ¶11]. Beyond premiums and benefits,
the Summary of Operations carries lines a liability model must supply specifically: **amortization of IMR**, separate
accounts net gain from operations, **interest and adjustments on contract or deposit-type contract funds**, **increase
in aggregate reserves**, **increase in loading on deferred and uncollected premiums** and **net transfers to or from
separate accounts** [REG-R90]. A separate **Cash Flow** statement requires a genuinely cash view [REG-R90].

**The four reporting targets.**

- **Exhibit 5 — Aggregate Reserves for Life Contracts.** Reserves **gross** (direct plus assumed) with a separately
  computed **ceded deduction**; Column 1 states the valuation standard **by years of issue**, with PBR-era abbreviations
  **VM-20NPR**, **VM-20 DET/STO** and **VM-22**. VM-20 business reports on **two separate lines**, the net premium
  reserve and the excess over it; VM-22 annuity business splits **Jumbo / Non-Jumbo in 50-basis-point valuation interest
  bands**. Miscellaneous Reserves carries variable life minimum death benefit guarantees, deficiency reserves, excess
  surrender values and **additional actuarial reserves — asset/liability analysis**; valuation-basis changes go to
  Exhibit 5A [REG-R89][REG-R90].
- **Exhibit 7 — Deposit-Type Contracts.** A fund roll-forward per column (guaranteed interest contracts, **annuities
  certain**, supplemental contracts, dividend accumulations, premium and deposit funds): opening balance, deposits,
  investment earnings credited, other net reserve changes, fees and charges assessed, **surrender charges**, net
  surrender and withdrawal payments, closing balance [REG-R89].
- **Analysis of Operations by Lines of Business.** Individual Life columns include **Whole Life, Term Life, Indexed
  Life, Universal Life, Universal Life With Secondary Guarantees, Variable Life, Variable Universal Life**; Individual
  Annuities columns include Deferred **Fixed, Indexed, Variable With Guarantees, Variable Without Guarantees** plus
  **Life Contingent Payout (Immediate and Annuitizations)** [REG-R90] — nearly one-to-one with the twelve products, and
  it should drive the model's reporting dimension. Indexed UL **with** secondary guarantees reports in the ULSG column,
  expired guarantees still report as ULSG, and incidental riders report on the **base contract's** line [REG-R89].
- **Analysis of Increase in Reserves During the Year.** By the same columns: opening reserve, **tabular net premiums or
  considerations**, disability claims incurred, **tabular interest**, **tabular less actual reserve released**, increase
  from **change in valuation basis**, **change in excess of VM-20 deterministic/stochastic reserve over net premium
  reserve**, other increases; then **tabular cost**, reserves released by death and other terminations, life-contingent
  payments, net separate account transfers, closing reserve and ending cash surrender value [REG-R90]. **This exhibit is
  denominated in valuation-basis quantities — tabular net premiums, tabular interest, tabular cost, reserves released —
  not experience quantities.** A model producing only experience cash flows cannot fill it; it must carry the
  valuation-assumption movement in parallel. Definitions and the roll-forward are in "Statutory income and surplus
  roll-forward" below, which needs the reserve `V(t)` fixed by the reserve sections first.

**Change in valuation basis** — interest, mortality or method — goes **direct to surplus**, measured at the **beginning
of the year**, is **not graded in** unless an actuarial guideline prescribes a transition, and is **excluded** from the
Summary and Analysis of Operations [REG-R79][REG-R80 ¶14][REG-R89]. For deposit-type contracts a voluntary election
between allowable Valuation Manual methodologies requiring commissioner approval is itself a change in basis [REG-R80].

---

## Required model outputs

The contract between `us/products/` and this section. Anything missing makes something below uncomputable.

| Output | Granularity / basis | Consumed by |
|---|---|---|
| Cash flows by type: gross premium/consideration, death, surrender and withdrawal, annuity and supplementary-contract payments, commission, other acquisition expense, maintenance expense, premium tax, policy loan flows | per contract per period, **gross and ceded separately, never netted** [REG-R89] | every reserve; income statement; Exhibits 5 and 7 |
| Reinsurance cash flows and reserve credit; modco deposit and funds withheld balances | per treaty per period; credit on the **same method and assumptions** as the direct reserve [REG-R92 ¶37] | Exhibit 5 ceded column; VM-20 §8; AG 55 [REG-R103] |
| Face amount in force, policy counts, in-force roll-forward on an **incurred** basis | per product column, in thousands [REG-R89] | Exhibit of Life Insurance; C-2 NAR |
| Net amount at risk | per policy; for C-2, **face in force − statutory reserve (GA + SA), net of reinsurance** [REG-R142] | C-2 mortality |
| Account value, cash surrender value, surrender charge state, MVA state | per contract per period | CARVM; NPR floors; C-3a bucketing |
| Guaranteed benefit streams **by elective path** (surrender, annuitization by option, withdrawal, guarantee election), each with its own timing; each path's **non-elective** leg computed *on the contract state that path leaves behind*, not on a standalone roll-forward; a **benefit-component tag per payment** (surrender/withdrawal, annuitization, non-elective) | per contract, one stream per path | CARVM greatest present value [REG-R1 §5a.B][REG-R153 ¶15]; AG 33's integrated benefit stream and its per-payment valuation rate [REG-R151] |
| **Accumulation fund** — the policy value used to purchase an annuity option — carried **separately from the cash value**, which it may exceed | per annuity contract per period [REG-R151] | AG 33 annuitization streams; the 7% expense-allowance floor |
| Secondary-guarantee state: FFSG, ASG, LSG; shadow account | per ULSG contract per period [REG-R3 §3.B.5] | VM-20 NPR (ULSG); §3.C.3 lapse |
| **Guaranteed maturity premium and guaranteed maturity fund**, held **per $1 of face amount** so a face change rescales them, plus the policy value | per universal life contract per duration [REG-R155 ¶¶8.c, 8.e, 11] | the A-585 CRVM adaptation and its alternative minimum reserve |
| Reserves by category and basis: CRVM/CARVM, VM-20 NPR/DR/SR, VM-21/VM-22, additional AAT reserve, deficiency reserve | per policy then per reserving category, keyed by **valuation standard and year of issue** [REG-R89] | Exhibit 5; minimum reserve; RBC exposure bases |
| Valuation-basis ("tabular") quantities: valuation net premium, valuation mortality, tabular interest, tabular cost | per policy per year, on the **reserve** basis, distinct from experience | Analysis of Increase in Reserves [REG-R90] |
| Separate account asset and reserve balances, GA transfers, SA charges, GA guarantee reserves, fair-value vs ¶18 book-value flag | per contract; SA surplus constrained non-negative [REG-R83 ¶8] | SSAP No. 56 split; C-4a; C-3c |
| **Asset-side interface**: starting-asset block and its statement value; BACV by NAIC designation and issuer; NAER and discount paths per segment; reinvestment/disinvestment strategy; realized gains split interest- vs credit-related; allocated PIMR/IMR (sign-aware) and allocated AVR | per model segment per period | DR/SR; AAT; C-1; C-3 Phase I; IMR/AVR |
| Tax reserve per IRC §807 = max(net surrender value, 92.81% × NAIC-method reserve), capped at statutory [REG-R16][REG-R72] | seriatim, same valuation date | FIT; DTA scheduling; C-3 Phase II tax adjustment |

---

## Contract classification: life contract versus deposit-type

**The test.** Mortality or morbidity risk is present "if, under the terms of the contract, the reporting entity is
required to make payments or forego required premiums contingent upon the death or disability … **or the continued
survival (in the case of annuity contracts)** of a specific individual or group of individuals" [REG-R80 ¶2]. A contract
assuming none of it that "act[s] exclusively as [an] investment vehicle" is a **deposit-type contract** [REG-R78 ¶5].
Life contracts include whole life, endowment, term, supplementary contracts, **universal life type**, **variable life**
and **annuity contracts** [REG-R78 ¶9]; deposit-type candidates include supplemental contracts, structured settlements,
guaranteed interest contracts, income settlement options, dividend accumulations and **annuities certain** [REG-R80 ¶5].

**It is decided at inception and it is immutable**: "such classification shall be made at the inception of the contract
and shall not change" [REG-R78 ¶5]. In a model this is a per-contract flag set at issue, never re-derived.

**Consequences.** For a deposit-type contract, amounts received "shall not be reported as revenues but shall be recorded
directly to an appropriate policy reserve account" [REG-R80 ¶6]; the reserve is the **present value of future guaranteed
benefits at the valuation interest rate** where benefits are fixed and guaranteed, otherwise the accumulated balance net
of withdrawals and surrender charges [¶9]; **credited interest is an expense** in the summary of operations, while a
payment returning policyholder balance is not [¶13]; and the balance reports in **Exhibit 7**, not Exhibit 5, running
through the deposit-type lines rather than the premium line [REG-R89][REG-R90]. Additional actuarial liabilities —
surrender values in excess of reserves, asset adequacy additions — still attach [¶16].

**Product-level consequences.** A **period-certain-only** immediate or deferred income annuity is deposit-type, sitting
in Exhibit 7 column 3, "Annuities Certain", whose instruction names "certain immediate annuity contracts" expressly
[REG-R80][REG-R89]. The reverse asymmetry is the modelling trap: Exhibit 5 footnote (a) keeps a contract that carried
mortality risk **at issue** in Exhibit 5 after the risk disappears, its own example being a life-contingent payout with
a certain period — "Because the contract was life-contingent at issue, it is reported in Exhibit 5 **and remains in
Exhibit 5 after the death of the annuitant** as remaining guaranteed payments continue to the beneficiary" [REG-R89]. So
a life-contingent SPIA or DIA with a period certain is a **life contract for its whole life**, including the residual
certain payments. Deferred annuities pick up deposit-type balances peripherally through settlement options and dividend
accumulations [REG-R80]. For universal life, a "waiver of monthly deductions" benefit is "not to be considered revenue
nor a benefit paid" [REG-R79 ¶14].

---

## The reserve hierarchy

**The statutory floor stack.** The Standard Valuation Law sets the minimum standard by mortality table, interest rate
and method by calendar year of issue (§§4, 4a, 4b); **CRVM** for life and endowment benefits (§5) and **CARVM** for
annuity and pure endowment benefits (§5a); an aggregate floor on the nonforfeiture basis (§6.A); a second aggregate
floor at "the aggregate reserves determined by the appointed actuary to be necessary to render the §3 opinion" (§6.B);
optional higher standards (§7); and, for issues on or after the Valuation Manual operative date, the **Valuation Manual
standard as the minimum** (§11) [REG-R1]. §6.B is what makes asset adequacy analysis part of *minimum reserves* rather
than a disclosure exercise, and is the authority behind VM-30's additional reserve [REG-R1][REG-R100].

**A citation correction on that last floor.** The AP&P codification of the Standard Valuation Law is Appendix **A-820**,
and **A-820 as printed contains no §6.B analogue** — its ¶16 carries only the aggregate nonforfeiture-basis floor
[REG-R153 ¶16]. In the manual the asset adequacy requirement sits in a separate four-paragraph appendix, **A-822 ¶3**:
where analysis shows a reserve is needed in addition to the aggregate reserve computed under A-820, "the company **shall
establish** the additional reserve", with ¶4 permitting release in later years and providing that the release "would
**not** be deemed an adoption of a lower standard of valuation" [REG-R153]. Read with A-820 ¶18 — holding additional
reserves determined by the appointed actuary is not the adoption of a higher standard — that pair keeps both the
establishment and the release of the asset adequacy reserve **outside the change-in-valuation-basis machinery**. **A
naming trap the library should carry explicitly:** AP&P **Appendix A-822** is an excerpt of the Standard Valuation Law's
asset adequacy provisions and is **not** NAIC **Model #822**, the Actuarial Opinion and Memorandum Regulation discussed
later in this file. Same number, different instrument; A-822 contains no opinion wording, no scenarios, no memorandum
requirements and no exemption clause [REG-R153][REG-R101][REG-R102].

**Formulaic versus principle-based.** CRVM is a modified-net-premium construction and CARVM a greatest-present-value
construction; both are contractual-guarantee calculations on prescribed mortality and a calendar-year-of-issue valuation
interest rate [REG-R1][REG-R153 ¶¶11, 15]. **"CRVM" names more than one construction, and the appendix prints say so** —
A-830 ¶2 declares its own segmented/unitary method to *constitute* CRVM for the policies it reaches, and A-585 ¶8
prescribes a different adaptation again for universal life [REG-R154 ¶2][REG-R155 ¶8]. A model that has one CRVM routine
has the wrong number of them; all four formulaic engines are set out in "Formulaic reserves" below. The principle-based
regime replaces them for post-operative-date business: **VM-20** constitutes CRVM for individual life subject to a
principle-based valuation, with a net premium reserve floor [REG-R3]; **VM-21** constitutes CARVM for variable
annuities, with AG 43 pulling pre-2017 business onto it [REG-R35][REG-R38]; **VM-22** covers non-variable annuities
[REG-R36]. SSAP No. 51 ¶15 now expressly contemplates formulaic reserves being "supplemented for some policies with more
advanced deterministic and/or stochastic reserve methodologies" [REG-R79].

**When each regime applies — and note the triggers are not all of a kind.** The Standard Valuation Law §11 names no
date; it says the Valuation Manual standard is the minimum *for issues on or after the Valuation Manual operative date*
[REG-R1]. That operative date is **1 January 2017**. It is no longer carried by a topic page alone: **A-820, the AP&P
codification of the Standard Valuation Law, prints the date twice in operative rules** — ¶3 applies the
principle-based-valuation provisions "to all policies and contracts issued on or after the **January 1, 2017, operative
date of the Valuation Manual**", and ¶4 grandfathers earlier issues onto ¶¶5–22 in the same words, adding that the PBR
provisions "**shall not apply to any such policies and contracts**" [REG-R153 ¶¶3–4]. The NAIC principle-based-reserving
topic page states it in the same terms — *"Effective Jan. 1, 2017, the Valuation Manual became operative"* [REG-R150] —
and the Standard Valuation Law print itself still never gives the date, but **[REG-R153] is now the primary citation for
it** and [REG-R150] the corroborating one. Life and annuity business then diverge:

| Business | Trigger | Timeline |
|---|---|---|
| **Individual life** (VM-20) | **Year of issue** | Issued before 1/1/2017 → formulaic CRVM remains the minimum standard, fixed by year of issue [REG-R1 §11], now stated verbatim in the appendix print: the PBR provisions "shall not apply to any such policies and contracts" [REG-R153 ¶4]; a later voluntary move of such a cohort onto another allowable basis is a **change in valuation basis**, direct to surplus, not an automatic conversion [REG-R79][REG-R89]. **PBR became an accreditation standard on 1/1/2020** — verbatim at [REG-R150], and note that accreditation binds *states*, not an insurer's reserve election. **Two claims commonly attached to this timeline are NOT sourced here and stay [unverified]:** that issues in **2017–2019** fell in an elective transition between the formulaic basis and VM-20, and that **VM-20 became mandatory for new issues on 1/1/2020**. [REG-R150] was fetched and checked for both and states neither; [REG-R153] was read in full and states neither, and contains **no elective-transition window, no phase-in and no company election** anywhere. That is now positive evidence about *where such an election is not*: A-820 ¶3 applies the Valuation Manual standard to all post-1/1/2017 issues without carve-out, and ¶24.e delegates "**transition rules**" to the Valuation Manual, so if the election exists it lives in VM-20/VM-01, not in the statutory-law layer [REG-R153 ¶¶3, 24.e] |
| **Variable annuities** (VM-21) | **Valuation date**, with the pre-date block pulled in by AG 43 | VM-21 applies for **valuation dates on or after 1 January 2020**, with an elective 36-month phase-in and a separate economic-scenario-generator phase-in of 36 months from 1 January 2026 [REG-R35]; and **AG 43 carries the VM-21 requirements back to contracts issued before 1/1/2017**, the two populations being aggregable [REG-R35][REG-R38] — so there is no preserved formulaic-only cohort as there is for life, back to AG 43's own scope of contracts issued on or after **1 January 1981** [REG-R38] |
| **Non-variable annuities** (VM-22) | **Valuation date** | Effective for **valuation dates on or after 1 January 2026**, with an elective three-year transition on VM-A/VM-C/VM-M/VM-V for business issued in the first three years — an irrevocable election once VM-22 PBR is chosen for a block — and mandatory prospective application three years after [REG-R36]. That endpoint is **January 2029**, printed only by [REG-R150] ("a three-year implementation period before becoming mandatory for all new issues in January 2029"); VM-22 itself leaves it to arithmetic. [REG-R150] states it prospectively as of an August 2025 page update, so re-check it against [REG-R36] before relying on it |

The consequence is worth stating plainly for anyone sizing a model build. **VM-20 is the only one of the three keyed to
year of issue**, so it splits a life block into a pre-2017 formulaic cohort and a post-2020 VM-20 cohort that must both
be valued for decades. VM-21 and VM-22 are keyed to the valuation date and so reach business already on the books. That
does **not** collapse an annuity block to a single basis: through VM-22's three-year transition both bases coexist, and
the reserve must still be keyed on `(valuation standard, year of issue)` rather than on product, because Exhibit 5
Column 1 states the standard by years of issue [REG-R36][REG-R89]. Whether an elective move from CARVM onto VM-22 is
itself a change in valuation basis **is resolved nowhere in this library** — AG 33 says nothing about VM-22 and predates
it [REG-R151] — and the March 2026 SSAP Nos. 3/51/52 guidance on the optional implementation period was not read
[REG-R79][REG-R88].

**One tension the appendix print creates, recorded rather than smoothed over.** A-820 ¶4 says the Valuation Manual
provisions "shall not apply to **any**" policy or contract issued before 1/1/2017, with no life/annuity distinction
[REG-R153 ¶4]. Yet AG 43 carries VM-21 requirements back to contracts issued before that date, and VM-21 and VM-22 are
keyed to the valuation date [REG-R35][REG-R36][REG-R38]. These reconcile only because AG 43 and VM-21 are separate
instruments — Appendix C and the Valuation Manual — operating alongside A-820, **not** because A-820 or §11 authorises
the reach-back. A-820/§11 is the authority for the *issue-date* trigger and for nothing else; the library should stop
implying otherwise [REG-R153 ¶4][REG-R1 §11].

**Which basis applies to which product.** Assembled from the twelve product files; each row's authority and mechanics
are in that product's own "Statutory accounting and capital" section.

| Product | Formulaic (pre-date issues, and the floor) | Principle-based | What a post-date block actually computes |
|---|---|---|---|
| Term life | The **A-830** CRVM — `max(segmented, unitary)` under the contract segmentation method, with deficiency reserves as quantity A less the basic reserve and X-factor relief [REG-R154 ¶¶2, 21, 17] | VM-20, **Term** category | DR in every case — the deterministic exclusion test is **not available at all** for term [REG-R3 §6.B] |
| Whole life | CRVM | VM-20, **All Other** — but a term-blend rider component sits in **Term**, and the categories are summed, never offset | NPR only where both tests pass — and that NPR *is* the formulaic CRVM via VM-A/VM-C; the deterministic test is unavailable to a term-rider component, so that component still produces a DR |
| Universal life | The **A-585** CRVM adaptation — guaranteed maturity premium, guaranteed maturity fund and the funding ratio [REG-R155 ¶8] | VM-20, **All Other** | NPR only where both tests pass; NPR routes through VM-A item **A-585**, and the A-585 print attributes itself to the **Standard Valuation Law (#820)** — it does not name Model #585 anywhere, so "A-585 *is* Model #585 §5" should be softened to "A-585 carries the UL CRVM adaptation" [REG-R155][REG-R5] |
| Indexed UL | The **A-585** adaptation, with the index stripped out of the guaranteed maturity premium solve: the GMP is computed on policy guarantees at issue "excluding guarantees linked to an external referent" [REG-R155 ¶8.c] | VM-20, category depends on whether a secondary guarantee is material | VM-20 §3.B.6 names indexed UL expressly: where no DR or SR is computed, the NPR follows VM-A/VM-C. But that path is not the expected one — §6.A.1.b's **hedging bar** blocks excluding a group with future hedging strategies from the SR, and §6.B then **deems the DET failed** for any group not excluded from the SR, pulling the DR in with it (**[std, derived]** from the cited rules; no source names indexed UL) [REG-R3] |
| Variable UL | CRVM. **A-830 is out of scope for VUL by its own terms** — ¶3.a.iii and ¶3.a.iv exclude variable life and variable universal life outright, so the open formulaic item for VUL is A-270 and A-820, not A-830 [REG-R154 ¶3.a] | VM-20, **All Other**, moving to **ULSG** where secondary guarantees are present | **Barred from the stochastic exclusion certification method**; the DET stays available |
| Guaranteed UL (ULSG) | The **A-830 ¶¶29–32** secondary-guarantee construction — segmented reserves over the secondary guarantee period on specified (else minimum) premiums, with **no unitary leg**, and where several guarantees coexist the **greatest of the stand-alone reserves for each unexpired guarantee, each valued ignoring the others** [REG-R154]; AG 38 on top. A-830 also carries a scope test the library did not have: a UL policy is **outside the appendix entirely** where the secondary guarantee period is **five years or less**, the specified premium is at least the net level reserve premium for that period, and the initial surrender charge is at least **100% of the first-year annualized specified premium** [REG-R154 ¶3.a.ii] | VM-20, **ULSG** category | Full machinery — **deemed to fail** the deterministic test where the secondary guarantee is material, and barred from the stochastic certification method |
| Fixed deferred (MYGA) | CARVM (SVL §5a / A-820 ¶15); **AG 33** as the interpretive layer, now read in full [REG-R151] — elective benefits are maximised over rather than assumed, the accumulation fund drives annuitization streams, and the **7% expense-allowance floor** bites on any contract guaranteeing better-of-current purchase rates | VM-22, **Accumulation** category | VM-22 §7 exclusion tests and Single Scenario Test — its own, not VM-20's. **AG 35 does not reach a book-value MYGA**, now on primary authority rather than inference: its scope is "all equity indexed annuity contracts … subject to CARVM", and a MYGA is not index-linked [REG-R152] |
| Fixed indexed (FIA) | CARVM; **AG 33** (elective benefits) and **AG 35** (how the index feature enters), **both now read** [REG-R151][REG-R152]. AG 35 supplies four constructions — CARVM-UMV, MVRM, the Black-Scholes Projection Method adaptation and EDIM — each ending by handing the resulting guaranteed benefit amounts to AG 33 for the greatest-present-value step | VM-22, **Accumulation** category, which expressly covers the post-exhaustion GLB income stream; SR = CTE 70 | VM-22 §7 tests; VM-20's bars and categories **do not transfer**, VM-20 being CRVM for individual *life*, so neither the term bar nor the ULSG deemed failure has an FIA analogue |
| Variable annuity | CARVM is the standard, but **VM-21 constitutes it** and AG 43 reaches back — no separate formulaic cohort survives | **VM-21** constitutes CARVM | Stochastic in practice: no exclusion test and no formulaic escape. VM-21's **only** relief is the **Alternative Methodology**, available solely for variable deferred contracts with no guaranteed benefits or **only GMDBs** — never a GLWB block, hence "always" for the representative design but **not** for the product as a class [REG-R35] |
| RILA (ILVA) | CARVM is the floor and never goes away | **VM-21 where VM-21 §2.A reaches the contract**: §2.A.1 covers guarantees similar in nature to GMDBs or VAGLBs, while **§2.A.3 excludes** separate account contracts that guarantee an index and offer no GMDB/VAGLB — so a GMDB-bearing design is in and a bare accumulation RILA falls back to formulaic CARVM. **VM-22 is not the RILA standard**, being the non-variable annuity requirement [REG-R35][REG-R36][REG-R44] | **There is no exclusion test on any route** — VM-20's are life-only, VM-21 has none at all, VM-22 §7's reach only non-variable annuities — so an in-scope contract computes CTE 70 every year [REG-R3][REG-R35][REG-R36]. See the caveat below; the applicability matrix marks RILA `?` on the VM-21/AG 43 and VM-22 rows |
| Immediate (SPIA) | CARVM; maximum valuation rate under **VM-V §1**. **AG 33 does not reach a no-option SPIA**: its applicability sentence requires that "any elective benefits … are available", and its non-elective definition expressly covers "benefits payable under either a deferred or immediate annuity contract (with or without life contingencies), **where no benefit options are available**". A life-only SPIA with no commutation, no acceleration and no elective option is inside CARVM and outside AG 33; add any one of those options and it is inside both [REG-R151] | VM-22, **Payout Annuity** category; SR = CTE 70 | VM-22 §7 exclusion tests and the **Single Scenario Test**, plus the small-company **Annuity PBR Exemption** keyed to $1.0bn of exemption reserves ($2.0bn at group level); **VM-20 never applies**, it being CRVM for individual *life* |
| Deferred income (DIA) | CARVM; maximum valuation rate under **VM-V §1**, not VM-22. A DIA's start-date adjustment, acceleration and commutation rights are **elective benefits** under AG 33, so the contract is in AG 33's scope: those options are maximised over as trial sets rather than assumed from experience, and because the annuitization portion's guarantee duration runs from issue to the **assumed** commencement date, moving the elected start date moves the contract across valuation-rate bands [REG-R151] | VM-22, which **names DIA contracts explicitly** in the Payout Annuity category | VM-22 §7 exclusion tests and the Single Scenario Test. **VM-20 and VM-21 are both out of scope**, so neither the term bar nor the ULSG deemed failure reaches this product |

Three caveats on that table, one of which has changed shape entirely. **The formulaic annuity half is no longer stated
by scope and authority alone** — AG 33 and AG 35 have been read, and the mechanics they supply are set out in "Formulaic
reserves" below. **RILA remains unsettled, but for a better-understood reason.** AG 33 applies to *all* annuity
contracts subject to CARVM where elective benefits are available, with no product list, no separate-account exception
and no size or premium threshold [REG-R151] — so a RILA carrying elective benefits is inside AG 33 and gets its stream
construction, its incidence rules and its benefit-level rate determination. AG 35 is a different matter: **it was
retrieved and it does not address the design.** It defines no term "equity indexed annuity"; it says nothing about
separate accounts, registered products, index-linked variable annuities, buffers, floors or AG 54; and its Background
describes contracts carrying "a minimum guaranteed interest accumulation rate on a portion of all premium payments",
which a buffer/floor RILA generally does not have. Record it as **neither including nor excluding RILA** [REG-R152].
**And the two VM-A items the library called "the closest formulaic items to a RILA" turn out not to be reserve methods
at all.** **A-250** (variable annuities) is three sentences: a definition, a requirement that each separate account hold
assets at least equal to the reserves and other contract liabilities of that account, and a delegation of the reserve
itself to **Appendix A-820** "in accordance with actuarial procedures that recognize the variable nature of the benefits
provided and any mortality guarantees" [REG-R156]. **A-255** (modified guaranteed annuities) is the same delegation plus
three operative rules: the separate account liability must be at least the surrender value produced by **the contract's
own market-value-adjustment formula**, a shortfall against the market value of the separate account assets must be made
good by a transfer into that account, and "any additional reserve that is needed to cover future guaranteed benefits
shall be established" [REG-R157]. **Neither item contains a formula, a symbol, a factor, a table, an elective-path rule,
an interim-value rule, or the word CARVM.** Calling them the closest formulaic items is defensible only as *nearest by
subject matter*; they add nothing to a RILA formulaic CARVM run beyond the MVA floor, so **a RILA CARVM run does still
rest on the SVL text as read through AG 33 — reading A-250 and A-255 did not change that.** That was an open question
and it is now closed, negatively. Finally, the **exclusion-test outcomes** above describe what a compliant block
typically computes, not a guarantee — the tests are run per company and per block, and passing them still leaves the
VM-31 and VM-G obligations described below.

**The boundary is not clean, and a model must build both engines.** VM-20's net premium reserve for the *All Other*
reserving category — and for indexed UL where no deterministic or stochastic reserve is computed — is determined
"pursuant to applicable methods in **VM-A and VM-C** for the basic reserve" [REG-R3]. VM-A is an *index* of formulaic
requirements carried in AP&P Appendix A, headed by **A-820** (minimum life and annuity reserve standards) [REG-R153] and
**A-830** (valuation of life insurance policies; the appendix prints neither "Model #830" nor "Regulation XXX" anywhere
in its own text, and is numbered as a flat sequence of paragraphs with **no sections**, so citations must use paragraph
numbers) [REG-R154], with A-585 universal life [REG-R155], A-250 variable annuities [REG-R156], A-255 modified
guaranteed annuities [REG-R157], A-270 variable life and A-791 reinsurance among the rest [REG-R110]; VM-C is the
parallel index of actuarial guidelines [REG-R41]. So whole life, ordinary UL, VUL and un-modelled IUL run the **old CRVM
calculation** inside a PBR-era manual — and A-820 supplies the statutory-layer authority for that sentence, which
previously rested only on VM-20 §3.B.6's pointer: the Valuation Manual **must** specify CRVM for life contracts and
CARVM for annuity contracts (¶24.a.i–ii); for policies not subject to a principle-based valuation the minimum standard
may simply "**be consistent with the minimum standard of valuation prior to the operative date of the Valuation
Manual**" (¶24.d.i); and "**a principle-based valuation may include a prescribed formulaic reserve component**" (¶27)
[REG-R153]. Income annuities keep a formulaic track of their own, VM-V §1 setting market-linked maximum valuation rates
by bucket, jumbo rates published daily and non-jumbo quarterly [REG-R37]. **Deficiency reserves** survive as a distinct
item under Actuarial Guideline I via VM-C [REG-R41] and Model #830 via A-830 [REG-R6][REG-R154], reported in Exhibit 5
Miscellaneous Reserves [REG-R89] — and the library's shorthand for them, "valuation net premiums in excess of gross",
**needs correcting on two counts**: A-820 ¶19 makes the deficiency a **floor on the policy reserve** rather than an
additive item, and A-830 keys its test to the **guaranteed** gross premium rather than to premium collected [REG-R153
¶19][REG-R154 ¶¶7, 17]. Both constructions, which are not the same construction as each other, are set out with their
arithmetic in "Formulaic reserves" below. **Of the items this paragraph used to disclaim, A-585, A-820 and A-830 have
now been read** [REG-R155][REG-R153] [REG-R154], as have **AG 33 and AG 35** [REG-R151][REG-R152]. **The AG I text was
not retrieved** and is still the one piece of the deficiency-reserve chain the library cannot quote [REG-R41][REG-R33].

**Two obligations around the calculation are not calculations.** **VM-31** requires a PBR Actuarial Report documented so
"another actuary qualified in the same practice area [can] evaluate the work", Summaries filed by April 1; a company
computing no deterministic or stochastic reserve because it passed the exclusion tests **must still file a sub-report**
[REG-R108]. **VM-G** decides who owns the model, with a counter-intuitive edge: passing an exclusion test by the
deterministic-reserve method, the VM-22 adjusted-scenario-reserve method or the Stochastic Exclusion Demonstration Test
**re-imposes** the board and senior management sections a pure exclusion-test company would escape, and that company's
actuary must still report **readiness to calculate the deterministic and/or stochastic reserve** — a requirement that
the model be *able* to compute components it currently omits [REG-R109]. Mechanics and the exclusion tests as decision
procedures are in "Formulaic reserves", "VM-20" and "VM-21 and VM-22" below; practice guidance is at [REG-R23],
[REG-R31] and [REG-R25].

---

## Formulaic reserves

There are **four** formulaic engines here, not one, and they are not interchangeable. (1) The **SVL §5.A / A-820 ¶11**
modified-net-premium CRVM, for level-amount level-premium life. (2) The **A-830** segmented/unitary CRVM, which by its
own ¶2 *constitutes* CRVM for the policies it reaches — nonlevel-premium or nonlevel-benefit non-UL designs and
universal life with secondary guarantees. (3) The **A-585** guaranteed-maturity-premium CRVM adaptation for universal
life. (4) The **A-820 ¶15 / AG 33** greatest-present-value CARVM for annuities. Routing a term or ULSG block through
engine (1) alone, or a universal life block through engine (1) instead of (3), is not a simplification — it computes a
different quantity [REG-R153][REG-R154][REG-R155].

**CRVM — the modified net premium construction.** For contract j issued at age x with guaranteed benefit stream B and
**contract** gross premiums G_k at durations k = 0, 1, 2, … [REG-R1 §5.A][REG-R153 ¶11]:

```
E   = α − β                                              (the CRVM expense allowance)
α   = min( APV_0(benefits provided after the first policy year) / ä_0 , P19(x+1) )
ä_0 = APV at issue of an annuity-due of 1 payable on the first and each subsequent premium-paying anniversary
β   = net one-year term premium for the benefits provided in the first policy year
P19(x+1) = net level annual premium on the NINETEEN-year premium whole life plan, same amount, at age x+1
k*  : APV_0( k*·G ) = APV_0(B) + E     ⇒     k* = ( APV_0(B) + E ) / APV_0(G)
V_CRVM(s) = max( 0 , APV_s(B) − k*·APV_s(G) )
```

The modified net premiums are that **uniform percentage k\*** of the respective contract premiums, and the reserve is
"the excess, **if any**" — floored at zero. **A-820 ¶11 as printed in the manual confirms every element of that
construction independently of the SVL print**: the uniform percentage of the *respective contract premiums*; α as the
APV of benefits provided **after the first policy year** over the premium-paying annuity-due; the cap at the
**nineteen-year premium whole life** net level annual premium **at an age one year higher than the issue age**; β as the
**net one-year term premium** for first-year benefits; and the excess-if-any floor [REG-R153 ¶11]. **No discrepancy was
found between the two prints**, so `[REG-R1 §5.A]` and `[REG-R153 ¶11]` are two independent citations for the same
machinery. Two traps: the cap is the 19-pay whole life premium at age **x+1**, not x; and V(0) = −E before flooring, so
`−V(0)` pre-floor is a free unit test of the allowance. Under **§5.B / A-820 ¶12**, where the first-year contract
premium exceeds the second-year premium with no comparable extra first-year benefit and the policy provides an endowment
or CSV greater than that excess, the reserve at any anniversary on or before the **assumed ending date** (first
anniversary at which endowment plus available CSV exceeds the excess premium) is `max(V_5A, V_5A')`, where V_5A' repeats
§5.A with α reduced by **15% of the excess first-year premium**, all present values ignoring premiums and benefits after
that date, the policy assumed to mature as an endowment then with the CSV then available as the endowment benefit, the
comparison run on the ¶5 mortality and ¶¶7–10 interest bases [REG-R1][REG-R153 ¶12]. **One ambiguity to record rather
than resolve:** A-820 ¶12 as printed says the 15% reduces "the value defined in **that paragraph**" after referring to
"**those paragraphs**", a singular/plural mismatch left by renumbering from the model law's "Subsection A / Subsection
A(1)". **The reading that the 15% attaches specifically to α — item a. — comes from the model law, not from A-820's own
text** [REG-R153 ¶12]; an implementation built from A-820 alone cannot derive it. Under the **mean reserve** method the
reserve is ½ (terminal reserve + initial reserve), the initial reserve being the prior terminal plus the current-year
net annual valuation premium, assuming the whole annual net premium at the start of the policy year and issues spread
ratably over the calendar year; because premiums arrive modally the reserve is overstated, so a **deferred premium
asset** = gross modal premiums from the next modal due date to the next anniversary, less those collected, less loading.
The mid-terminal method instead averages terminal reserves at the surrounding anniversaries and adds an unearned premium
reserve [REG-R81/IP51 ¶21]. Inside a VM-20 projection **deferred premiums are zero**, because the projection reflects
premium mode directly [REG-R3 §7.B].

**CRVM for nonlevel designs — the A-830 segmented and unitary construction.** A-830 ¶2 states that "the method for
calculating basic reserves defined in this appendix will constitute the Commissioners' Reserve Valuation Method for
policies to which this appendix is applicable", so for a policy inside its scope the engine above is **not** the
statutory method [REG-R154 ¶2]. Scope is *all* life insurance policies issued on or after the appendix's effective date,
less six exceptions — reentry policies descending from a pre-effective-date policy (the carve-out **propagates** down
the reentry chain, so applicability is inherited at issue rather than derived from the issue date),
short-secondary-guarantee UL meeting **all three** of ¶3.a.ii, variable life, variable universal life, most group
certificates, and preneed (which follows A-817) [REG-R154 ¶3.a]. Routing: nonlevel guaranteed gross premiums or nonlevel
guaranteed benefits (non-UL) → ¶¶21–28; flexible or fixed premium UL with a secondary guarantee → ¶¶29–32 [REG-R154
¶3.b]. **Cite A-830 by paragraph: the appendix is a flat sequence ¶¶1–32 plus an Attachment and has no Sections at
all**, so a "Model 830 §7" citation does not resolve against this print [REG-R154].

Segment determination, `x` = issue age, `k` = years from issue to the start of the segment, `t` = 1, 2, … **reset to 1
at each segment boundary** [REG-R154 ¶5]:

```
G(t) = GP(x+k+t) / GP(x+k+t−1)      GP = guaranteed gross premium PER THOUSAND of face,
                                          ignoring policy fees only if level for the premium-paying period
R(t) = q(x+k+t) / q(x+k+t−1)        q  = the valuation mortality rate for DEFICIENCY reserves in policy year k+t,
                                          but on the UNMODIFIED select rates where modified select rates are
                                          used in the deficiency reserve itself
segment length = min{ t : G(t) > R(t) }      (if G never exceeds R, the segment runs to mandatory expiration)
company option  : R(t) may be moved ±1% in any policy year, but R(t) ≥ 1
degenerate cases: GP(x+k+t) > 0 and GP(x+k+t−1) = 0  ⇒  G(t) := 1000   (segment always ends here)
                  GP(x+k+t) = GP(x+k+t−1) = 0        ⇒  G(t) := 0      (zero-premium years never break a segment)
```

The ±1% tolerance exists "to prevent irrational segment lengths due to such things as premium rounding" and is elected
**per policy year**, not once [REG-R154 ¶5]. **Segmented reserves** (¶11) are the PV of all future guaranteed benefits
less the PV of all future net premiums **to mandatory expiration**, with net premiums a uniform percentage of guaranteed
gross premiums **within each segment** — one percentage per segment, set so that at the start of the segment the PV of
net premiums in the segment equals the PV of death benefits in the segment, plus any unusual guaranteed CSV at the
segment end, less any unusual guaranteed CSV at the segment start, plus — **first segment only** — an expense allowance
of the same `α − β` shape as ¶11 above **with both the benefit numerator and the annuity denominator restricted to the
first segment**. The 19-pay whole life cap at age **x+1** is printed identically in the segmented and unitary versions,
so one expense-allowance routine can serve all three engines **only if its horizon is a parameter** [REG-R154 ¶¶11, 14].
Present values include the current segment **and all subsequent segments** (¶11.d) — a valuation inside segment 3 is not
a segment-3-only calculation. The interest cap uses a guarantee duration equal to the **sum of the lengths of all
segments** (¶11.c), which spans the same period as the unitary rule's "issue to mandatory expiration" (¶14.b). **Unitary
reserves** (¶14) use a **single** uniform percentage of guaranteed gross premiums to mandatory expiration, with the
expense allowance run over the whole policy. **Basic reserves = max(segmented, unitary)** (¶21.a), both legs on the same
valuation mortality table and selection factors; at the insurer's option **one** of two adjustments may be made inside
the segmented leg — treat the positive unitary reserve at each segment end as a pure endowment and subtract the positive
unitary reserve at each segment start, or do the same with the guaranteed cash surrender value in its place (¶21.b). All
[REG-R154].

Four further A-830 constraints an implementation needs. **Select mortality factors may be used only in the first
segment**, except that where the first segment is under ten years the ten-year select factors of A-820 may run **through
the tenth policy year from issue** (¶18). **Floors** (¶23): basic reserves ≥ the tabular cost of insurance for the
balance of the policy year (mean reserves) or of the current modal period, or to the paid-to-date if later but not
beyond the next anniversary (mid-terminal); and **total** reserves — basic plus deficiency plus reserves for
supplemental benefits expiring on termination — may never be less than what the policyowner would receive on
termination, **exclusive of any deduction for policy loans**. **Unusual guaranteed cash surrender values** (¶24) impose
an independent floor applied *after* the max of segmented and unitary: a future guaranteed CSV is "unusual" if it
exceeds the prior year's by more than `110%·(scheduled gross premium) + 110%·(one year's accrued interest on [prior
guaranteed CSV + scheduled gross premium] at the nonforfeiture interest rate used for the guaranteed CSVs) + 5%·(first
policy year surrender charge)`, and reserves before the first unusual value are floored by treating it as a **pure
endowment** on an n-year term-plus-pure-endowment policy. **Post-issue unilateral guarantee changes** (¶20) are valued
as the **greatest of three** parallel valuations — ignoring the guarantee, assuming it was made at issue, and assuming
the policy was issued on the date of the guarantee. Mortality: **effective 1 January 2004 the 2001 CSO Mortality Table
is the minimum standard** for basic reserves (¶16), deficiency reserves (¶17), the tabular cost of insurance (¶23, on
**ultimate** rates) and all four exemption calculations (¶¶25–28); the complete pre-2004
1980-CSO-with-elective-select-factors branch is **retained in full** in the print, so a model valuing pre-2004 issues
needs it. **A-830 prints no calendar effective date for itself** — the phrase "the effective date of this appendix" is
an unresolved placeholder used eleven times — so no date may be attributed to it beyond the 1/1/2004 cutover. All
[REG-R154].

**ULSG under A-830 ¶¶29–32.** A policy has a secondary guarantee if it guarantees to stay in force at the original
schedule of benefits **subject only to payment of specified premiums**, or (from 1/1/2004, on ultimate 2001 CSO rates)
if its **minimum premium at any duration is less than the corresponding one-year valuation premium** — the second limb
sweeps in policies with **no explicit guarantee clause** at all. Then [REG-R154 ¶¶29–32]:

```
gross premiums := specified premiums, if any, else minimum premiums
minimum premium for a policy year = the premium that, paid into a policy with a ZERO account value at the start
        of the year, produces a ZERO account value at the end, on cost factors and crediting rate GUARANTEED AT ISSUE
one-year valuation premium = the net one-year premium on the original benefit schedule, computed FOR ALL POLICY
        YEARS AT ISSUE; the ¶17 select mortality factors MAY NOT be used in it
BasicReserve  = segmented reserves over the secondary guarantee period, segments per ¶5 on the substituted premiums
                    -- there is NO unitary leg here
DeficiencyReserve = the ¶22 construction on the same substituted premiums
MinReserve(SG) = max( BasicReserve + DeficiencyReserve ,
                      the minimum reserve required by "other appendices governing universal life plans" )
several unexpired secondary guarantees: value EACH stand-alone, IGNORING all the others, and take the greatest
```

Two cautions. The ¶32.b limb is an **unnamed cross-reference** — A-830 does not say which appendix item it means, and it
must **not** be resolved to A-585 on this text [REG-R154 ¶32]. And a secondary guarantee **unilaterally changed by the
insurer after issue is deemed to have been made at issue**, forcing recalculation of the ¶30/¶31 reserves **from issue**
[REG-R154 ¶29.b].

**CRVM for universal life — the A-585 guaranteed-maturity-premium adaptation.** A-585 ¶8 states that "the minimum
valuation standard for universal life insurance policies shall be the Commissioners Reserve Valuation Method, **as
described below for such policies**", and what is described below has no `k*` and no contract gross premiums in it. With
`x` = issue age and `t` = duration [REG-R155 ¶8]:

```
V(t) = ( (A) − (B) )·r  −  (C)  −  (D)

(A) = PV at the DATE OF VALUATION of all future guaranteed benefits
(B) = ( PVFB / ä_x ) · ä_{x+t}
      PVFB = PV of all benefits guaranteed AT ISSUE, assuming future guaranteed maturity premiums are paid and
             taking into account all guarantees in the policy or declared by the insurer  -- fixed AT ISSUE
(C) = ( (a) − (b) ) · ( ä_{x+t} / ä_x ) · r
(D) = Σ additional quantities analogous to (C) arising from STRUCTURAL CHANGES, each on the maturity date in
      effect at the time of the change

ä_x, ä_{x+t} = annuities of 1 per year on policy anniversaries, continuing until the HIGHEST ATTAINED AGE AT WHICH
               A PREMIUM MAY BE PAID -- the PREMIUM-PAYING period, not the coverage period
r = 1                                    if the policy is a FIXED premium universal life policy  (unconditionally)
r = min( 1 , PolicyValue(t) / GMF(t) )   if the policy is a FLEXIBLE premium universal life policy
```

`(A) − (B)` is an ordinary prospective net level premium reserve, `PVFB/ä_x` being the net level valuation premium.
Three implementation points the print settles. **The r-ratio is flexible-premium-only**: A-585 ¶8.d makes r "equal to
one, **unless** the policy is a flexible premium policy and the policy value is less than the guaranteed maturity fund",
so a blanket `r = min(1, PV/GMF)` is **wrong for fixed premium UL** [REG-R155 ¶8.d]. **The r-ratio pairs with the
projection rule**: future guaranteed benefits are determined by projecting the **greater** of the guaranteed maturity
fund and the policy value, using all guarantees in the policy or declared by the insurer, plus any benefits not
depending on the policy value (¶8.i) — so an underfunded flexible-premium policy is projected as if fully funded and the
resulting reserve is then **scaled down by r**. **Declared guarantees more favourable than the contractual ones are
applicable** to the determination of future guaranteed benefits (¶9). All [REG-R155].

The two objects that engine needs are both **solves**, per contract [REG-R155 ¶¶8.c, 8.e]:

```
GMP (flexible premium) = the level gross premium, paid at issue and periodically over the period during which
      premiums are ALLOWED to be paid, that matures the policy on the latest maturity date permitted (otherwise at
      the highest age in the valuation mortality table) for the maturity amount, computed on ALL POLICY GUARANTEES
      AT ISSUE, EXCLUDING GUARANTEES LINKED TO AN EXTERNAL REFERENT, and adjusted for death benefit corridors
      maturity amount = the INITIAL DEATH BENEFIT for a level death benefit design (corridor ignored), or the
                        SPECIFIED AMOUNT for a specified-amount-plus-value design (corridor ignored)
GMP (fixed premium)    = the premium defined in the policy which at issue provides the minimum policy guarantees
GMF(t) = the amount which, together with future guaranteed maturity premiums, will mature the policy on all policy
         guarantees at issue -- a prospective guarantee-basis fund path, one solve per duration
```

The GMP **may be less than the premium needed to pay all charges**, "especially … in the first year for policies with
large first year expense charges", so a negative-margin first year is expected behaviour rather than a solve failure
[REG-R155 ¶8.c fn. 2]. **For indexed UL this is the only index-specific reserve rule in the item**: because
interest-indexed UL is defined as a policy "where the interest credits are linked to an external referent" (¶4) and the
GMP excludes guarantees so linked (¶8.c), **the index crediting is stripped out of the GMP solve entirely** [REG-R155].
**Structural changes** — changes separate from the automatic workings of the policy, usually policyholder-initiated:
changes in guaranteed benefits, in the latest maturity date, or in the allowable premium payment period — force
recalculation of GMP, GMF and (B) (¶8.h); the sanctioned simplification is to hold **GMP and GMF per $1 of face amount
and multiply by the new face amount**, offered permissively as "perhaps the simplest such method", not prescribed (¶11)
[REG-R155].

**Where (a) − (b) comes from, and a cross-reference that does not resolve.** A-585 ¶8.f defines `(a) − (b)` as
"described in **paragraph 9 of Appendix A-820**". **A-820 ¶9 as printed in the same manual is the
reference-interest-rate paragraph** — the Moody's composite yield definition — not an expense allowance [REG-R153 ¶9].
The quantities labelled **a.** and **b.** in A-820 are at **¶11.a and ¶11.b**: the capped net level annual premium α and
the net one-year term premium β, i.e. the CRVM expense allowance reproduced at the top of this section. That
identification is **structural, not textual** — it is what `(a) − (b)` must be for the A-585 reserve to be a CRVM
reserve — and the printed pointer is recorded here as **not resolving against the March 2026 print of A-820**, not
silently repaired. Everything else A-585 needs is delegated outright: "all present values shall be determined using (i)
an interest rate (or rates) specified by Appendix A-820 for policies issued in the same year; (ii) the mortality rates
specified by Appendix A-820 for policies issued in the same year" (¶8.j), reinforced at ¶10. **A-585 prints no rate, no
table, no factor and no number of any kind** [REG-R155].

**The A-585 alternative minimum reserve — not a deficiency reserve.** Its comparator is the **guaranteed maturity
premium**, not the contract gross premium [REG-R155 ¶¶12–13]:

```
VNP(k) = valuation net premium on the METHOD ACTUALLY USED, on MINIMUM mortality and interest standards
         = PVFB / ä_x                          on a net level premium basis                        [¶13]
         = PVFB / ä_x + ((a) − (b)) / ä_x      on a Commissioners Reserve Valuation Method basis    [¶13]

if GMP < VNP(k) in ANY policy year k:
    AMR_b = the reserve on the METHOD ACTUALLY USED, on MINIMUM mortality and interest, with VNP(k) REPLACED BY
            GMP in EACH policy year k for which VNP(k) > GMP        (year by year, not all years)
    MinimumReserve = max( reserve on the method, table and rate ACTUALLY USED , AMR_b )
```

The trigger is per policy year and the substitution is per policy year, so a policy can be inside the test with the
substitution active in only some years; both legs run on the **method actually used**, only the mortality and interest
basis being forced to the minimum standards [REG-R155 ¶12].

**CARVM — the greatest-present-value construction.** For each contract-year end k = 1 … H [REG-R1 §5a.B][REG-R153 ¶15]:

```
X(k) = APV_τ( guaranteed benefits, INCLUDING guaranteed nonforfeiture benefits, provided at the end of contract year k )
     − APV_τ( future valuation considerations required by the contract that become payable BEFORE the end of year k )
V_CARVM(τ) = max over k of X(k)
```

Future guaranteed benefits use the mortality table (if any) and interest rate(s) **specified in the contract for
determining guaranteed benefits** — the *contractual* guarantee basis, not the valuation basis, which enters through the
discounting; valuation considerations are the portions of the gross considerations applied under the contract to
determine nonforfeiture values [REG-R1 §5a.B][REG-R153 ¶15]. **A-820 ¶15 confirms the construction word for word** and
adds the scope gate the library did not carry: ¶15 applies to all annuity and pure endowment contracts **other than**
group annuity and pure endowment contracts purchased under an employer or employee-organization retirement or deferred
compensation plan (IRA/§408 plans excepted), which ¶13.b routes instead to a **CRVM-consistent** method [REG-R153
¶¶13.b, 14]. The implementation obligation is **path enumeration** — one benefit stream per elective path; missing a
path can only understate the reserve. **A-820 supplies the principle and no path list**; that is AG 33's subject, and AG
33 has now been read [REG-R151].

**AG 33 — what CARVM's maximisation actually ranges over.** The guideline "codif[ies] the basic interpretation of CARVM
and does not constitute a change of method or basis"; it applies "to all annuity contracts subject to CARVM, where any
elective benefits … are available to the contract owner under the terms of the contract", and where a product-specific
guideline or regulation exists **that guideline takes precedence** [REG-R151]. It contains **no algebra at all** — no
formula, no symbol, no table, no factor except the 7% expense allowance and the run-off phase-in percentages — so every
symbolic rendering below is marked as this library's restatement of the guideline's prose. Every contract's benefits
must first be sorted into two categories [REG-R151]:

- **Non-elective** — payable only on a contingent or scheduled event independent of an owner election, "including (but
  not limited to) death benefits, accidental death benefits, disability benefits, **nursing home benefits**, and
  benefits payable under either a deferred or immediate annuity contract (with or without life contingencies), **where
  no benefit options are available** under the terms of the contract".
- **Elective** — the complement: "benefit options that may be freely elected", including "full surrenders, partial
  withdrawals, and full and partial annuitizations".
- Both lists are non-exhaustive, and the only tie-breaker offered is behavioural: judge "the degree to which contract
  owner actions would be influenced by the availability of each benefit". Note the classification consequence —
  **nursing-home benefits are non-elective, not elective**.

The two sides then take **completely different incidence rules**, and this is the part a projection engine gets wrong
most easily [REG-R151]:

```
NON-ELECTIVE
  incidence from the tables PRESCRIBED BY THE SVL where one exists;
  where none exists, company or industry experience WITH MARGINS FOR CONSERVATISM (unquantified);
  the SVL-prescribed ANNUITY MORTALITY table discounts EVERY payment in EVERY integrated benefit stream for
      survivorship -- including the purely elective surrender and withdrawal streams.
      A cash-value stream is NOT valued on a mortality-free basis under AG 33.

  hard cut-off, non-mortality non-elective waiver-type benefits           [std, restatement of AG 33 prose]
      ι(t) = 0  for all t > T ,   T = min( SCP1 , T_depletion )
      SCP1        = end of the surrender charge period applicable immediately after the FIRST premium is paid
                    (a later premium restarting a surrender charge schedule does NOT extend T)
      T_depletion = first projection time at which the projected cash value is depleted

ELECTIVE
  incidence "should not be based on tables reflecting past company experience, industry experience or other
  expectations" -- experience-based lapse, withdrawal and annuitization assumptions are PROHIBITED in a CARVM
  valuation. The elective assumption is a DECISION VARIABLE maximised over, not an assumption:
      consider trial sets, "all possible elective benefit incidence rates between 0% and 100%",
      the greatest present value "will typically occur by assuming an incidence rate of either 0% or 100%"
      -- stated as a typicality, NOT as permission to restrict the search.
```

The object being maximised is the **integrated benefit stream**, and its asymmetry is the whole point: for a candidate
elective incidence set `e`, there is exactly **one** non-elective leg per elective leg, computed on the contract state
that elective leg leaves behind [REG-R151]:

```
IBS(e) = A(e) ⊕ B(e)                                        [std, restatement]
A(e)   = the guaranteed ELECTIVE payments implied by e -- one blend across benefit TYPES, not one type at a time
B(e)   = the guaranteed NON-ELECTIVE payments, "recognizing the guaranteed elective benefit stream under
         consideration in A above", on the non-elective incidence rates
both legs survivorship-discounted on the SVL-prescribed annuity mortality

V_CARVM(τ) = max over e of Σ over payments p in IBS(e) of  payment(p)·survivorship(p)·v_{rate(p)}(time(p))
rate(p)    = the valuation rate for the BENEFIT COMPONENT that payment p belongs to  (see below)
```

Three families of stream are **mandatory**, notwithstanding that the heading calls them examples [REG-R151]: **(A) cash
value streams** — "any possible blend of future guaranteed partial withdrawals and full surrenders … **accumulated at
the guaranteed credited interest rate(s) and discounted at the valuation rate(s) of interest**", which is exactly the
construction of Worked example 2 below; **(B) annuitization streams** — full *or partial* elections at each election
date required by CARVM, valued on **the guaranteed purchase rates contained in the contract, "excluding any current
purchase rates which may be applicable", applied to the accumulation fund**; and **(C) all other guaranteed elective
benefits, including blends of more than one type**. "Accumulation fund" is a defined term — "the policy value which is
used to purchase an annuity option under the terms of the contract" — and the guideline's point in defining it is that
**it may exceed the cash value**, so a model carrying a single account value cannot value stream B correctly.

**Which valuation rate attaches to which payment.** AG 33 does not supply rates; it supplies the level at which each SVL
§4b parameter is determined, and the answer is *not* elective-versus-non-elective [REG-R151]:

| SVL §4b parameter | Determined at | Consequence |
|---|---|---|
| A — issue year vs change in fund basis | **contract** level | one basis for the whole contract, applied **consistently to every portion of every stream** |
| B — cash settlement options present | **contract** level | one answer per contract |
| C — interest guaranteed on considerations received >12 months after issue | **contract** level | one answer per contract |
| D — guarantee duration | **benefit** level | varies by benefit component, and for annuitization by the **assumed election date** |
| E — Plan Type | **benefit** level | A / B / C per benefit component |

so the rate varies **inside** one integrated benefit stream, "resulting in potentially different valuation rates for
each benefit type". The per-component rules: for **surrender and partial withdrawal** portions, Plan Type follows the
contract's withdrawal characteristics (A, B or C) and **guarantee duration is the number of years for which interest
rates are guaranteed in excess of the calendar year statutory valuation interest rate for life insurance policies with
guarantee duration over twenty years** — a comparison against an externally published series, recomputed by calendar
year of issue, not simply the length of the rate guarantee. For **annuitization** portions, **guarantee duration = years
from original issue or purchase to the date annuitization is assumed to commence**, so the valuation rate is a *function
of the candidate election date* and moves across §4b guarantee-duration bands as the candidate moves; Plan Type **A
generally** for an immediate life annuity or instalments over five years or more, and Plan Type **C** ("shall") for a
non-life-contingent payout period under five years. For **non-elective** portions, Plan Type A generally, guarantee
duration from issue to the date non-elective benefits may first be paid, usually under five years. These rules apply
**to each separate payment**, and there is an anti-rate-shopping rider: a portion that looks like a life annuity or a
five-year-plus instalment stream but "can be changed **directly or indirectly** by exercise of contract owner withdrawal
options" **may not** take the annuitization treatment. All [REG-R151].

The guideline's one extended illustration is a classification, not arithmetic: a **guaranteed lifetime income benefit**
on a fixed deferred annuity — "whether traditional or **indexed to an external referent such as an equity index**" —
splits at account exhaustion. Payments that reduce or deplete the annuity's defined values, plus any residual
withdrawals after election, take the withdrawal rule (Plan Type A, B or C by the contract's withdrawal provisions); the
remaining payments are "a life annuity without option to take or receive additional amounts" and take the annuitization
rule, **Plan Type A generally, with guarantee duration measured from contract issue to the commencement of that second
portion** [REG-R151].

**Two hard constraints and one sanctioned approximation** [REG-R151]:

```
CHANGE IN FUND / ISSUE YEAR ELECTION
  contracts with NO cash settlement options MUST be valued on an issue year basis;
  the basis is a CONTRACT-level attribute, applied consistently to all portions of all streams;
  it is elected AT ISSUANCE and locked -- changeable only with the commissioner's PRIOR WRITTEN approval.
  In a model this is a per-contract immutable flag of the same character as the life/deposit-type classification.

THE 7% EXPENSE-ALLOWANCE FLOOR                                            [std, restatement]
  V(τ) ≥ AF(τ)·(1 − EA),  EA ≤ 0.07      AF(τ) = the contract's accumulation fund value at the valuation date
  Trigger 1: the contract guarantees the use of FUTURE UNKNOWN purchase rates (e.g. "the better of guaranteed
             and then-current rates") -- and in exchange the company need NOT build current-rate annuitization
             streams at all.
  Trigger 2: the contract provides ADDITIONAL AMOUNTS DURING THE PAYOUT PERIOD over those guaranteed at
             commencement -- then the floor applies DURING THE DEFERRED PERIOD.
  EA is a CAP, not a value: 7% is the maximum allowance, so AF·0.93 is the LOWEST permitted floor, and the
  guideline gives no rule for setting EA below the cap. The base is the ACCUMULATION FUND, not the cash value.
```

and the escape from combinatorial explosion: the guideline "requires that the actuary **consider, not necessarily
test**, all potential integrated benefit streams to determine to what extent each contract owner option has a material
impact on the reserve", permitting elimination of streams by analytical means and demonstrated approximations — naming,
as its own example, "a CARVM reserve ignoring non-elective benefits, plus an **'add-on' reserve for non-elective
benefits**". That decomposition is therefore a **blessed approximation requiring demonstration**, not an alternative
method; substantially consistent alternative methods need **prior regulatory approval** [REG-R151].

**What AG 33 does not do, and this is load-bearing.** It never cites SVL §5a by number, and its operative *Text* block
never restates the "end of each respective contract year" indexing or the deduction of future valuation considerations —
those appear only in a Background paraphrase. **How the stream maximisation composes with §5a's per-contract-year-end
excess is not stated by AG 33**, and this file does not assert a composition [REG-R151][REG-R1 §5a.B][REG-R153 ¶15]. The
guideline also contains no asset adequacy requirement, no mention of the Valuation Manual, VM-21, VM-22 or PBR, no
mention of AG 35 or any other guideline by name, no aggregation or grouping guidance, and no quantification of the
"margins for conservatism" [REG-R151].

**AG 35 — how an index-linked benefit becomes a guaranteed benefit amount.** AG 35 applies "to all equity indexed
annuity contracts, **regardless of the date of issue**, that are subject to CARVM" — a valuation-date requirement
reaching the whole in-force block, with a second cumulative limb (the contract must be subject to CARVM). **The single
most important structural fact is that AG 35 does not perform the CARVM maximisation**: each of its four constructions
ends with the same Step 4 — perform the CARVM calculation in accordance with **AG XXXIII** and any other applicable
guideline. Its job is to convert an unknown future index path into deterministic guaranteed benefit amounts at each
duration; AG 33 then takes the greatest present value. Two classes, four calculations, and the set is closed —
"variations from the MVRM and EDIM … are not acceptable interpretations of CARVM", the BSPM being the one sanctioned
adaptation (of the MVRM specifically) [REG-R152].

```
TYPE 2 -- CARVM with Updated Market Values (CARVM-UMV)
  1  for each duration t and each benefit b at which an index-based benefit is available:
         O(t,b) = market value of the call option that EXACTLY hedges the floor of that benefit -- payoff exactly
                  equal to [benefit b at t, reflecting all relevant contract features] − F(t,b) -- valued by
                  "an appropriate option pricing technique, such as Black-Scholes or a stochastic scenario method"
  2  A(t,b) = O(t,b)·(1 + i_v)^(expiry − valuation date)        accumulate at the VALUATION interest rate
  3  GB(t,b) = F(t,b) + A(t,b)                                  the index enters as an ADDITION to the guaranteed
                                                                benefit, benefit by benefit -- not a separate reserve
  4  run CARVM on {GB(t,b)} per AG 33

TYPE 2 -- Market Value Reserve Method (MVRM)
  1  solve for the projected index level I(T) at the end of the TERM such that the benefit at T equals the contract
     guarantee at T plus the current market value of the call option(s) that would FULLY hedge the index-based
     benefit, accumulated at the valuation interest rate; options "with maturity dates coterminous with the setting
     of participation rates, spread, or any other method of determining index-based benefits"
  2  g = ( I(T)/I(0) )^(1/T) − 1 ;  I(t) = I(0)·(1+g)^t
     -- prescribed: "assuming EQUAL ANNUAL PERCENTAGE INCREASES in the index", i.e. one constant compound rate,
        not a stochastic set and not a scenario ensemble. The g expression is this library's restatement; the
        guideline prints no formula.
  3  determine all annuity benefits from the projected index levels     4  run CARVM per AG 33

TYPE 2 adaptation -- MVRM using the Black-Scholes Projection Method (BSPM), for benefit determinations
                     redetermined during the term (particularly annually) -- the annual-reset / annual-ratchet chassis
  1  per successive period p over which the benefit determination is guaranteed:
         c(p) = cost of a FULL hedging call option as a PERCENTAGE OF THE ACCOUNT VALUE for that period,
                accumulated to the end of the period at the RISK-FREE INTEREST RATE, and used as the projected
                GROWTH RATE OF THE ACCOUNT VALUE during p, recognising benefit guarantees, forward interest rates,
                forward index volatility and index dividend levels
  2  INVERT the crediting formula: back the index level out of the projected account level on each anniversary
  3  determine benefits    4  run CARVM per AG 33

TYPE 1 -- Enhanced Discounted Intrinsic Method (EDIM); permitted ONLY while the "Hedged as Required" criteria are met
  Reserve = FixedComponent + EquityComponent
  FC(0) = the formula reserve produced by EITHER CARVM-UMV OR MVRM   -- EDIM cannot stand alone at issue
  FC(T) = the FLOOR of the benefit actually being hedged, which may be a WEIGHTED BLEND over the maturity benefits
          assumed when the hedge was bought
  FC(0)·(1+j)^T = FC(T)  ⇒  FC(t) = FC(0)·(1+j)^t                    -- the "enhancement" is this j accumulation
  EC(t) = [ INTRINSIC value of the options at the valuation date ]·(1 + i_v)^−(T − t)
          -- intrinsic value only, no time value, discounted rather than projected: the omitted time value is
             assumed to be carried by the hedge, which is why the method is gated on being hedged
```

Two differences an implementer will otherwise get wrong: **BSPM accumulates at the risk-free rate** where CARVM-UMV step
2, MVRM step 1 and EDIM's equity component all use the **valuation** interest rate; and **BSPM projects the account
value first and derives the index from it**, where MVRM projects the index first and derives benefits from it — the
mapping runs in opposite directions [REG-R152]. The guideline's own worked passage is qualitative: purchase options
assuming 90% surrender and 10% annuitization at maturity, and the Fixed Component becomes `FC(t) = 0.90·FC_surr(t) +
0.10·FC_ann(t)`, each sub-component accumulating from its own share of FC(0) to its own terminal floor — **the 90/10
split is illustrative and tied to the option-purchase assumption, not prescribed** [REG-R152].

**MVRM, BSPM and EDIM all need a "term"; CARVM-UMV does not.** The term's terminal point is "the point in time
associated with the **single dominant benefit** most likely to be provided under the contract", determined on product
features including "the pattern of guaranteed participation rates, surrender charges, vesting rates, spread deductions,
and **marketing/advertising material**" — a prescribed input to a statutory reserve — and the appointed actuary must
have demonstrated compliance to the satisfaction of the regulator in **each state** in which a statutory statement is
filed **before** using MVRM or EDIM. CARVM-UMV needs no term, no dominant-benefit test and no prior demonstration, but
requires an option valuation on a full **duration × benefit** grid. **Because EDIM's initial reserve must be at least
the initial reserve produced by CARVM-UMV or MVRM, a model cannot implement EDIM alone** [REG-R152].

**AG 35's Plan Type rule closes a hole in the §4b table above.** Design features unique to equity indexed annuities —
equity-enhanced surrender values, vesting schedules, participation rates — **may not** be used to determine Plan Type;
"only those design features specifically identified in Section 4b. Paragraph C of the NAIC Model SVL may be used". And
the Plan Type A/B phrase "with an adjustment to reflect changes in interest rates **or asset values**" is expressly
ruled not to include "changes in policy values due to changes in the equity index underlying the policy form". **An
FIA's index-linked features are therefore invisible to the Plan Type determination**; Plan Type is decided on withdrawal
and adjustment features alone [REG-R152]. The valuation interest rate itself must be "consistent with … **Actuarial
Guideline XXXIII or Actuarial Guideline IX-B**" — stated once per method that needs it, so an FIA CARVM run has to
resolve **AG IX-B**, which this library holds only as a VM-C index entry [REG-R41][REG-R152].

**The Type 1 gate, in numbers.** The "Hedged as Required" criteria come in two alternative sets, certified quarterly by
the appointed actuary [REG-R152]:

```
BASIC (long-dated options)                       hedge sizing measured AT ISSUE
  hedge purchased at or near issue ≥ SP% of the product's account value at issue
  SP% = (1 − d)^n ,  d ≤ 0.03 per year of elective decrements unless the Commissioner agrees a higher limit,
        n = length of the OPTION GUARANTEE in years -- for an annual-ratchet product with a multi-year policy
        term but one-year participation-rate guarantees, "the 'term' for this purpose is 1 YEAR"
  printed example: five-year point-to-point ⇒ SP% = (1 - .03) ^ 5 = 86%      (0.97^5 = 0.8587)
        -- SP% = (1 − d)^n is this library's generalisation; the guideline prints only the example

OPTION REPLICATION (dynamic hedging)             notional test measured EVERY QUARTER, on the REMAINING guarantee
  at each quarter end: notional of the replication target ≥ Σ over contracts of SP%·(account value)
  same 1-year rule for annual ratchet, same 3%/year elective decrement cap, and additionally "appropriate
  assumptions for NON-ELECTIVE decrements such as mortality may be added to the assumption for elective decrements"

  compliance evaluation = a RETROSPECTIVE CORRELATION TEST run AT LEAST WEEKLY
      D = Δ(market value of the HEDGE portfolio since the start of the calendar quarter)
        − Δ(market value of the OPTIONS EMBEDDED IN THE LIABILITIES over the same period)
      V = beginning-of-period market value of the options embedded in the liabilities
      maximum permitted |D| = 10% of V
      10% < |D| < 25%, occurring a SECOND TIME in a quarter → notify the Commissioner in each state licensed,
                                                              stating the dollar reserves being hedged
      |D| > 25% at ANY weekly interval                      → same notification, plus the IMPACT ON SURPLUS of
                                                              reporting the reserves on the CARVM-UMV basis
      |D| > 35% at ANY POINT IN TIME during the quarter     → DEEMED OUT OF COMPLIANCE, same notification content
  over-hedged: "the excess hedging instruments are excluded from the measurements" -- the test runs on the matched
      portion only, so over-hedging cannot mask a correlation failure
```

The escalation triggers are **not stated on a uniform basis** — "a second time during a quarter", "at any of the weekly
intervals", "at any point in time during the quarter" — and the last is broader than the weekly observation grid the
test otherwise runs on; the guideline does not say how a between-observation breach is detected [REG-R152]. Note that
**CARVM-UMV is the guideline's implicit reference method**: it is what surplus impact is measured against when a hedge
drifts, and one of the two permitted bases for the EDIM initial reserve.

**What AG 35 does not settle, stated plainly because it bears on RILA.** It defines **no** term "equity indexed
annuity"; it says nothing about separate accounts, registered products, index-linked variable annuities, buffers, floors
or AG 54; and its Background describes designs carrying "a minimum guaranteed interest accumulation rate on a portion of
all premium payments", which a buffer/floor RILA generally does not have. **AG 35 was retrieved and does not address
that design** — it neither includes nor excludes it. It prints no effective date, adoption date, operative date,
transition, phase-in or sunset of any kind; the only temporal language in it is "regardless of the date of issue", and
the `© 1999-2026` footer is a copyright span, not an adoption date. It prescribes no volatility, no dividend yield, no
risk-free curve and no option pricing model — assumption discipline is enforced **by appointed-actuary certification,
not by prescription**. It says nothing about the Valuation Manual, VM-21, VM-22 or PBR, and prints no precedence rule
for a conflict with AG 33. All [REG-R152].

**Valuation interest rate, by calendar year of issue.** A **step function of calendar year of issue** (or of the year of
the change in fund), not a projection variable [REG-R1 §4b][REG-R153 ¶¶7–10]. Life, also at VM-20 §3.C.2.a.i: `I = 0.03 +
W·(R1 − 0.03) + (W/2)·(R2 − 0.09)` with `R1 = min(R, 0.09)`, `R2 = max(R, 0.09)`; SPIAs and life-contingent annuity
benefits use `I = 0.03 + W·(R − 0.03)` with **W = 0.80** [REG-R1 §4b.B][REG-R3][REG-R153 ¶7.a.i]. Rounding is to the
nearer quarter of 1%. **Correction on the tie-break:** A-820 ¶7.a.i prescribes the quarter-percent rounding and
**prescribes no tie rule at all**; the "ties **down**" convention this file records belongs to **VM-20 §3.C.2.a**
[REG-R3] and must not be read off [REG-R1]/[REG-R153]. For a pre-2017 formulaic rate the tie convention is **unresolved
in the primary text** [REG-R153 ¶7.a.i]. Life weighting factors by guarantee duration: **0.50** for 10 years or less,
**0.45** over 10 to 20, **0.35** over 20 [REG-R1 §4b.C(1)(a)][REG-R153 ¶8.a]. Other annuities and GICs use the Plan Type
A/B/C table on an issue-year basis (≤5 years 0.80/0.60/0.50; >5–10 0.75/0.60/0.50; >10–20 0.65/0.50/0.45; >20
0.45/0.35/0.35) with change-in-fund increments **+0.15/+0.25/+0.05** and a further **+0.05** for all three plan types in
the stated no-forward-guarantee cases [REG-R1 §4b.C(1)(c)][REG-R153 ¶8.c]. **Every one of those parameters was
re-verified against the A-820 print and no discrepancy was found**, including the non-monotone change-in-fund
increments, which are the model law's own pattern and not a transcription error [REG-R153 ¶8.c.ii]. R is the monthly
average of the **Moody's composite yield on seasoned corporate bonds**: for life, the **lesser** of the 36-month and
12-month averages ending June 30 of the year *preceding* issue; for SPIAs and life-contingent annuity benefits, the
12-month average ending June 30 of the year *of* issue; for other annuities and GICs with cash settlement options on an
issue-year basis, the **lesser** of the 36- and 12-month averages where the guarantee duration exceeds ten years and the
12-month average where it does not; and for a change-in-fund basis, the 12-month average ending June 30 of **the
calendar year of the change in the fund** [REG-R1 §4b.D][REG-R3][REG-R153 ¶9]. **Stability rule:** if the life rate
differs from the prior calendar year's actual rate by **less than one-half of 1%**, it is set equal to the prior year's
rate — a **life-only** rule, recursing on the *published* prior-year series rather than a freshly recomputed one [REG-R1
§4b.B(2)][REG-R3][REG-R153 ¶7.a.ii]. Because §4b.E / A-820 ¶10 permits an NAIC-adopted alternative if Moody's ceases
publication, implement the reference series as a **configurable table keyed by calendar year**, never a hard-coded feed.
**Guarantee duration for annuities and GICs** is itself defined twice: with cash settlement options, "the number of
years for which the contract guarantees interest rates in excess of the calendar year statutory valuation interest rate
for life insurance policies with guarantee duration in excess of twenty (20) years"; with none, the number of years from
issue or purchase to the scheduled commencement of annuity benefits [REG-R153 ¶8.c.iv]. **The issue-year /
change-in-fund election is per contract, recorded at issue, and forced to issue-year where there are no cash settlement
options** [REG-R153 ¶8.c.vi][REG-R151]; on a change-in-fund basis the valuation rate becomes a function of **the year
each increment of fund arose**, i.e. a per-layer attribute rather than a per-contract scalar.

**Two annuity-specific overlays on that machinery.** AG 33 fixes **at what level** each §4b parameter is determined — A,
B and C at contract level, guarantee duration and Plan Type at **benefit** level, so one integrated benefit stream can
carry several rates and the annuitization rate moves with the assumed election date [REG-R151]; the detail is in the
CARVM material above. AG 35 fixes **how an indexed contract is classified**: index-linked design features may not be
used to determine Plan Type, and index-driven changes in policy values are not the "changes in … asset values" of the
Plan Type A and B definitions [REG-R152]. VM-20's NPR rate is the same machinery plus a deficiency-style uplift: for
term amounts under §3.B.4 and ULSG amounts under §3.B.5.c the rate is **increased by 1.5% but in no event greater than
125% of it**, rounded to the nearest quarter with **ties up**; §3.B.5.d uses the unuplifted rate with ties down
[REG-R3]. Income annuities run on a market-linked mechanic instead: four Valuation Rate Buckets A–D keyed to reference
period and, with life contingencies, initial age, with **jumbo = initial consideration ≥ $250 million** (contracts to
the same holder within 90 days combined), jumbo rates published daily and non-jumbo quarterly [REG-R37].

**Valuation mortality** is the other prescribed input and is keyed the same way. The NPR uses the tables of VM-20 §3.C.1
together with VM-M §1.H [REG-R3]; VM-A indexes the requirements that fix which table applies — A-812 smoker/nonsmoker
tables, VM-A-814 recognition of the 2001 CSO (Model #814), A-815 preferred tables and A-821 the annuity table (Model
#821) [REG-R110]; and Exhibit 5 Column 1 requires the mortality or disability table actually used to be stated **by
years of issue**, its prescribed abbreviation set running from the American Experience Table through **2017 CSO** and
**2012 IAR** [REG-R89]. Model it as a lookup keyed by (year of issue, product, sex, smoker, risk class, age basis
ANB/ALB), not as a single global table.

**Life mortality by issue year, from the A-820 print** [REG-R153 ¶5]: ordinary policies on the standard basis issued
**on or after 1 January 2004** → the **2001 CSO**, or at company election for specified plans the 2001 CSO with
**25-Year Select Mortality Factors**, or any ordinary table adopted subsequently by the NAIC; ordinary policies issued
**before** that date, and preneed issued on or after 1 January 2012 (which follow A-817) → the **1980 CSO**, or at
election the 1980 CSO with **Ten-Year Select Mortality Factors**; industrial → the **1961 CSI**; total and permanent
disability benefits → the Period 2 disablement rates and 1930–1950 termination rates of the **1952 Disability Study**,
combined with a permitted life table for active lives; accidental death benefits → the **1959 Accidental Death Benefits
Table**, likewise combined; group life, substandard and other special benefits → simply "tables which provide for an
adequate reserve". **The 2017 CSO is nowhere in A-820's printed text** — it can enter only through ¶5.a's forward
reference to tables adopted subsequently, and in practice reaches post-2017 issues through the Valuation Manual under
¶23 instead [REG-R153].

**Annuity mortality by issue year — a gap the library did not know it had, now closed** [REG-R153, A-821]. **Annuity
2000** for any individual annuity or pure endowment contract issued **1 January 2001 through 31 December 2014**; the
**2012 IAR** for issues **on or after 1 January 2015**; **1983 Table "a" without projection** solely for contracts on
life contingencies funding periodic benefits from court or out-of-court **tort settlements**, similar actions such as
workers' compensation claims, and long-term disability claims settled with a temporary or life annuity — the
structured-settlement carve-out; and the **1994 GAR** for any annuity or pure endowment purchased under a **group**
annuity or pure endowment contract, for which **A-821 prints no effective date at all**. **No standard is printed for
individual annuities issued before 1 January 2001.** The 2012 IAR and 1994 GAR are **generational**, so the valuation
rate is a function of *(age, calendar year)*, and the rounding convention is prescribed and non-obvious:

```
q_x^(2012+n) = q_x^2012 · (1 − G2_x)^n            2012 IAM Period Table × Projection Scale G2      [A-821 ¶13]
q_x^(1994+n) = q_x^1994 · (1 − AA_x)^n            1994 GAR                                         [A-821 ¶16]

round each result to THREE DECIMAL PLACES PER 1,000, evaluating the formula FROM THE 2012 BASE EVERY TIME:
    male age 30:  q^2012 = 0.741, G2 = 0.010
                  q^2013 = 0.741·(1−0.010)^1 = 0.73359    → 0.734
                  q^2014 = 0.741·(1−0.010)^2 = 0.7262541  → 0.726
    the recursive shortcut is EXPRESSLY WRONG: 0.734·0.99 = 0.727 ≠ 0.726.
    "It is incorrect to use the already rounded q_x^2013 to calculate q_x^2014."                    [A-821 ¶14]
```

Implement as `q(x, 2012+n) = round3(q2012[x] · (1 − G2[x])**n)` with `n` recomputed at each projection step; **a
single-vector `q[x]` array cannot represent this basis**, and the female and male Scale G2 vectors differ (notably the
whole 60–80 plateau, 0.013 female against 0.015 male), so they must not share one array [REG-R153]. **A-821 prints only
the 2012 IAM Period Table and Scale G2**; the 1994 GAR table and its `AA_x` factors, the Annuity 2000 table and 1983
Table "a" are **named and not printed**, so the ¶16 formula is not computable from library sources.

**Deficiency and other additional reserves.** The library previously defined a deficiency as arising "where the
valuation net premium exceeds the **actual gross premium collected**". **Both retrieved constructions key it to a
contractual premium, not to a premium collected, and they are not the same construction as each other.** A-820 ¶19
expresses it as a **floor on the policy reserve**, triggered by the gross premium *charged* falling below the valuation
net premium computed by the method actually used on the **minimum** standards of mortality (¶5) and interest (¶¶7–10)
[REG-R153 ¶19]:

```
TRIGGER   in any contract year k:  G(k) < π_min(k)
          π_min(k) = valuation net premium by the METHOD ACTUALLY USED, on the MINIMUM mortality and interest
V_actual  = reserve on the mortality table, rate of interest and method ACTUALLY USED
V_def     = reserve by the METHOD ACTUALLY USED on the MINIMUM standards, with the valuation net premium
            REPLACED BY the actual gross premium G(k) in EACH contract year for which π_min(k) > G(k)
MinimumReserve = max( V_actual , V_def )
```

There is **no separate additive "deficiency reserve" quantity in A-820 ¶19** — the deficiency is a floor. For an
excess-first-year-premium design, ¶20 substitutes **¶11 CRVM** as "the method actually used" inside that test and takes
`max(min-reserve per ¶¶11–12, min-reserve per ¶¶19–20)` [REG-R153 ¶20]. A-830 instead defines a **separate quantity**
for the policies it reaches [REG-R154 ¶¶6, 17, 22]:

```
quantity A = a FULL RE-RUN of the basic reserve using GUARANTEED gross premiums in place of net premiums,
             duration by duration, WHEREVER the guaranteed gross premium is the SMALLER of the two
             ("guaranteed gross premium" = guaranteed and determined AT ISSUE -- ¶7 -- not premium collected)
DeficiencyReserve = max( 0 , A − BasicReserve ) , taken for the current and all remaining periods
basis      : unitary if the ¶21 basic reserve was unitary, segmented if segmented, SEGMENTED on a tie
trigger    : any duration where the guaranteed gross premium < the corresponding modified net premium computed
             by the basic-reserve method BUT on the MINIMUM valuation standards of mortality (¶17) and interest
             -- so the comparison net premium need not be on the basic reserve's own standard
segments   : NOT re-derived on the deficiency mortality basis -- segment lengths equal those of the basic reserve
policy fees: may be INCLUDED in guaranteed gross premiums for the deficiency reserve even where EXCLUDED from the
             basic reserve (¶19) -- an asymmetry worth coding explicitly
```

The substitution is **one-sided**: where the gross premium exceeds the net premium the net premium stands. The
**X-factor** relief is a **two-limb** test, not one: X must satisfy both an aggregate present-value limb — the APV of
future death benefits on the X-adjusted rates at least the APV on anticipated experience **without recognition of
mortality improvement beyond the valuation date**, discounted at the basic-reserve valuation rate — **and** a
year-by-year floor requiring the X-adjusted rates to be at least anticipated experience **in each of the first five
years after the valuation date**. Passing the PV limb alone is insufficient. X may vary by policy year, form,
underwriting class, issue age or any other factor expected to affect mortality; the appointed actuary **shall increase**
X where needed and **may decrease** it; and **A-830 prescribes no X table, no floor and no cap** — X may exceed 100 as
well as fall below. Any X below 100% at any duration for any policy triggers an annual actuarial opinion and memorandum
under the **A-822** asset adequacy requirements, disclosure in the **Regulatory Asset Adequacy Issues Summary**, and an
annual opinion supported by an actuarial report [REG-R154 ¶17.c]. Select factors are usable **only in the first
segment**, with the ten-year carve-back noted above [REG-R154 ¶18]. **Actuarial Guideline I, the interpretive vehicle in
the VM-C index, was still not retrieved** [REG-R41], and the **A-585 alternative minimum reserve above is a different
item** — its comparator is the guaranteed maturity premium, not any gross premium [REG-R155 ¶12]. The Exhibit 5
Miscellaneous Reserves block carries these and their siblings: variable life minimum death benefit guarantee reserves;
excess of valuation net premiums over gross premiums; non-deduction of deferred fractional premiums or return of premium
at death; **surrender values in excess of reserves otherwise carried**; and **additional actuarial reserves —
asset/liability analysis** [REG-R89][REG-R81/IP51 ¶28][REG-R80 ¶16]. The fourth catches a CARVM result falling below the
immediately available surrender value.

**The aggregate floors and the asset adequacy additional reserve, as the A-820/A-822 print states them.** A-820 ¶16 is
an **aggregate** test across all life insurance policies (excluding disability and accidental death benefits), **not
seriatim**: aggregate reserves may not be less than the aggregate reserves computed by the **same methods** (¶¶11–15,
¶¶19–21) on **the mortality table(s) and interest rate(s) used in calculating the nonforfeiture benefits** [REG-R153
¶16]. ¶17 permits any standard producing **greater** aggregate reserves for a category, with a constraint the library
was missing: for policies and contracts **other than annuity and pure endowment contracts**, the interest rate used may
not exceed the corresponding rate used in calculating any nonforfeiture benefits [REG-R153 ¶17]. **The asset adequacy
additional reserve is in A-822, not A-820**: ¶3 requires that where asset adequacy analysis shows a reserve is needed in
addition to the aggregate reserve computed under A-820, "the company **shall establish** the additional reserve", and ¶4
permits release in later years, expressly providing that the release "would **not** be deemed an adoption of a lower
standard of valuation" [REG-R153, A-822 ¶¶3–4]. Read with A-820 ¶18 — the holding of additional reserves previously
determined by the appointed actuary is **not** the adoption of a higher standard — that pair keeps establishment *and*
release of the AAT reserve **outside the change-in-valuation-basis machinery in both directions**, which is what stops
it flowing through Exhibit 5A [REG-R153 ¶18][REG-R89].

**Worked example 1 — CRVM.** Three-year endowment: face 1,000 payable at end of year of death, endowment 1,000 at end of
year 3, level annual contract gross premium **G = 320** at the start of each of three years. Valuation basis: flat **q =
0.010**, **i_v = 4%**, and **P19(x+1) = 25.00** per 1,000 so the cap binds — all three **[std]**, chosen so the
arithmetic is checkable by hand; a real valuation uses the prescribed table and the calendar-year-of-issue rate above.
**The primary text does not disturb this example**: A-820 ¶11 confirms the construction element by element, so only the
parameter values remain **[std]** [REG-R153 ¶11].

| Quantity | Value | | Quantity | Value |
|---|---|---|---|---|
| APV₀(B) = 9.615385 + 9.153107 + 8.713053 + 862.592278 | **890.073822** | | β = 1000·0.01·v | **9.615385** |
| ä₀ = 1 + 0.99·v + 0.9801·v² | **2.858080621** | | E = α − β | **15.384615** |
| APV₀(benefits after year 1) | 880.458438 | | APV₀(G) = 320·ä₀ | 914.585799 |
| uncapped α = 880.458438 / 2.858080621 = 308.059343, capped | **α = 25.000000** | | k\* = 905.458438 / 914.585799 | **0.9900202** |
| V(1) = 924.926036 − k\*·624.615385 | **306.544172** | | V(2) = 961.538462 − k\*·320 | **644.731990** |

Self-check: `APV₀(B) − k*·APV₀(G) = −15.384615 = −E`, so the reserve at issue floors to zero and the expense allowance
is exactly E [REG-R1 §5.A].

**Worked example 2 — CARVM.** Single premium deferred annuity: consideration 10,000, guaranteed rate **3.0%**, surrender
charges **5/4/3/2/1/0%** in years 1–6, **i_v = 4.25%**, mortality ignored for the surrender stream — all **[std]**. A
single premium contract has no future valuation considerations, so `X(k)` is the discounted `CSV(k) = 10,000·1.03^k·(1 −
sc_k)`.

| k | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| CSV(k) | 9,785.00 | 10,184.64 | 10,599.45 | 11,029.99 | 11,476.81 | 11,940.52 |
| v^k | 0.9592326 | 0.9201272 | 0.8826160 | 0.8466341 | 0.8121190 | 0.7790111 |
| X(k) | **9,386.09** | 9,371.16 | 9,355.25 | 9,338.36 | 9,320.54 | 9,301.80 |

`V_CARVM = max_k X(k) = 9,386.09` at k = 1, because the valuation rate exceeds the guarantee. It sits **below** the
immediately available surrender value of 9,500; that gap is picked up separately as "surrender values in excess of
reserves otherwise carried" in Exhibit 5 [REG-R89][REG-R81/IP51 ¶28].

**What AG 33 confirms in that example, and what it shows to be wrong.** The *construction* is now primary-sourced:
*Text* 2.A requires the cash value stream to be "accumulated at the guaranteed credited interest rate(s) and discounted
at the valuation rate(s) of interest", which is exactly the roll-forward-and-discount above [REG-R151]. The arithmetic
is unchanged and the parameter values remain **[std]**. But **two of the example's simplifications are not merely
stylised, they are non-compliant, and the example must not be read as a compliant CARVM** [REG-R151]:

1. **"Mortality ignored for the surrender stream" is contrary to AG 33.** The SVL-prescribed annuity mortality table
   discounts *every* payment in *every* integrated benefit stream for survivorship, the elective cash-value stream
   included. A compliant run multiplies each `CSV(k)` by the survivorship factor to k on that table. The example keeps
   the mortality-free form because it is a hand-checkable teaching device; a production engine that does the same is
   wrong.
2. **The path set is too small.** Enumerating "full surrender at each duration k" is not the AG 33 search space, which
   is "any possible blend of future guaranteed partial withdrawals and full surrenders", plus the mandatory
   annuitization streams on **guaranteed** purchase rates applied to the **accumulation fund**, plus any other elective
   benefits and blends across types — each with its non-elective leg computed on the state that path leaves. Since
   omitting a path can only understate the reserve, the tabulated 9,386.09 is a **lower bound** for a contract with any
   of those features, not the reserve.

The 7% expense-allowance floor does **not** bite on this contract as specified, because no better-of-current
purchase-rate guarantee and no payout-period excess-amount provision was assumed; had one been present the floor would
be `AF(0)·(1 − EA) ≥ 10,000 × 0.93 = 9,300`, still below 9,386.09 at issue, so the floor would not bind here either —
but it will bind on designs where the greatest present value falls further below the accumulation fund [REG-R151].

---

## VM-20

**The three components and their combination**, per reserving category K ∈ {Term, ULSG, All Other VM-20} [REG-R3 §2.A,
VM-01]:

```
neither DR nor SR computed :  MinRes(K) = Σ_j NPR_j
DR but not SR              :  MinRes(K) = Σ_j NPR_j + max(0, DR − (A − B))
DR and SR                  :  MinRes(K) = Σ_j NPR_j + max(0, max(DR, SR) − (A − B))
A = Σ_j policy minimum NPR for those policies ;  B = due and deferred premium asset held
Total minimum reserve = Σ over the three categories
```

Computing "neither" is permitted only for ULSG with a **non-material secondary guarantee** passing both exclusion tests,
or for All Other. Two asymmetries: the DR/SR excess is measured **net of the due-and-deferred premium asset**, and for
Term the valuation net premium is zero in policy year 1, so B and the unearned premium reserve are zero in year 1. DR
and SR may be computed as of a date **no earlier than three months before τ** with a roll-forward [§2.E]. The
general-account share may not be less than zero and the separate-account share is bounded below by Σ CSV and above by Σ
AV attributable to the separate account [§2.F]. **Reserving-category dependence is structural:** the minimum reserve is
a *sum* of three per-category results, so a Term excess cannot be offset against All Other slack; if a DR group spans
categories a DR is computed for each single-category subgroup with any difference allocated **proportionally** [§4.C];
if an SR aggregation subgroup spans categories the **SR must also be computed stand-alone for each category** [§5]. All
[REG-R3].

**Net premium reserve (§3), seriatim.** **Term** uses §3.B.4 with prescribed lapses — **10%** during a level premium
period under five years, **6%** for five or more, **0%** once the final premium has been payable — plus the prescribed
shock-lapse table for the final year of a level premium period, applied after benefits assumed payable that year and
before the increased premium takes effect, ranging **25% to 80%** by the before/after period lengths and whether the
gross premium increase per $1,000 reaches **400%** [§3.C.3]. **ULSG** under §3.B.5.d uses **0%** lapse throughout; under
§3.B.5.c a level rate fixed at τ, `R = clip((FFSG − ASG)/(FFSG − LSG), 0, 1)` then `L = R·0.01 + (1 − R)·0.005·r`,
giving a **1% level lapse at issue** where ASG = 0. **All Other, and IUL where no DR or SR is computed, take the
VM-A/VM-C formulaic basic reserve** [§3.B.6][REG-R110] — **which CRVM engine that is depends on the policy**: the SVL
§5.A / A-820 ¶11 engine for level whole life, the **A-585** guaranteed-maturity-premium engine for universal life and
indexed UL, and the **A-830** segmented/unitary engine for anything A-830 reaches. Sending a UL or IUL policy through
the §5.A engine because "All Other routes to CRVM" computes the wrong quantity [REG-R155 ¶8][REG-R154 ¶2]. Assumed YRT
is **one half year's cost of insurance on the reinsured net amount at risk**. Floors [§3.D]: for non-UL, the greater of
the cost of insurance to the next paid-to-date and the CSV; for UL, the amount needed to cover the cost of insurance to
the next processing date on which COI charges are deducted, **based on the net amount at risk and on the valuation
mortality rate, not the contractual COI or expense charges**. **Policy minimum NPR = NPR less the §8 ceded reinsurance
credit** [§3.E]; the NPR must reflect continuous deaths and immediate payment of claims. All [REG-R3].

**Deterministic reserve (§4) — both forms**, since VM-31 §3.D.2.h requires the company to state which was used **for
each model segment** [REG-R108]:

```
§4.A gross premium valuation form
  DR = APV(benefits, expenses and related amounts) − APV(premiums and related amounts)
     − PIMR allocated at the valuation date + separate account asset balance + policy loan balance
§4.B direct iteration form
  DR = a − b ,  a = aggregate annual statement value of the starting assets which, projected with all premium and
       investment income, exactly liquidates all projected future benefits and expenses by the end of the horizon;
       b = the allocated PIMR
```

**Prescribed scenario: economic scenario 12** of §7.G.1 / Appendix 1.E, discounted on the **path of discount rates for
the corresponding model segment** determined under §7.H.3 — a net asset earned rate construction. The APV of premiums
and related amounts includes future gross premiums and other revenue, net separate-account-to-general-account flows, net
policy loan flows, net §8 reinsurance flows and net derivative-liability-program flows allocated to the group. **Federal
income taxes are excluded from projected expenses** [§4.A, §7.A]. A group excluded from the SR requirement **may not
include future non-hedging derivative program transactions in its DR** [§4.A.5]. All [REG-R3].

**Stochastic reserve (§5).** Per scenario ω, for each model segment, at the model start date and each projection year
end, discount **the negative of the projected statement value of general and separate account assets** back to the start
on the §7.H.4 path; sum across model segments at each date; then [REG-R3 §5]:

```
ScenRes(ω) = statement value of starting assets across all model segments
           + max over dates d of  Σ_segments ( − AssetStatementValue_ω(d) · discount_ω(d) )
SR         = CTE70({ScenRes(ω)}) + any additional amount for material risks not reflected in the models − allocated PIMR
CTE_a(X)   = mean of the worst (1 − a) fraction of the ranked sample; rank low to high, average the largest 30% for CTE 70
```

Aggregation subgroups must be consistent with how the company **actually manages risk**, and contract types with
significantly different risk profiles may not be grouped [§5]. The 2026 GOES phase-in, if elected before the Dec. 31,
2026 valuation, applies `DR = D − (B − A)·(DR1 − DR2)/B` and `SR = S − (B − A)·(SR1 − SR2)/B` with **B = 36 months**, A
= months elapsed since Dec. 31, 2025, DR1/SR1 on the 2026 scenario basis and DR2/SR2 on the 2025 basis, both as of Jan.
1, 2026 on the same in-force and **ignoring exclusion tests**; the phase-in amount is deemed zero for a component whose
exclusion test is passed [§2.J].

**Exclusion tests as decision procedures.** They determine what the model must be *capable* of, so implement them as
gates. **Stochastic Exclusion Test** [REG-R3 §6.A], three alternative routes:

```
route 1  SERT — annually, within 12 months before τ:
         a = adjusted DR under economic scenario 9 (the baseline, Appendix 1.E)
         b = the LARGEST adjusted DR under any of the OTHER 15 of the 16 prescribed scenarios
         c = PV of BENEFITS under the baseline, adjusted for reinsurance by subtracting ceded benefits, using the
             benefit cash flows from "a" and the same discount path
         PASS iff (b − a) / c < 6%
route 2  Stochastic Exclusion Demonstration Test — first year and at least every third calendar year: compare
         max(DR, NPR − due-and-deferred-premium-asset) against the stand-alone SR, or against scenario reserves from a
         sufficient number of adverse deterministic scenarios, or against an SR on a representative sample, or
         demonstrate the driving risks are absent or substantially eliminated
route 3  SET Certification Method — first year and at least every third calendar year; NOT available for variable life
         or ULSG
```

The numerator is `b − a` — **not** the largest difference and **not** the largest absolute difference, both of which the
guidance note says give an incorrect result. Benefits for "c" are death benefits, surrender or withdrawal benefits and
**policyholder dividends**; premium, ceded premium, expense, reinsurance expense allowance, modco reserve adjustment and
experience refund flows are **not** benefits. The adjusted DR may be built either as the §4.A DR with scenario-specific
interest rates, equity returns, NAER and discount rates, **or** as the gross premium reserve developed from the
company's own asset adequacy analysis models using its cash-flow-testing assumptions, provided that model carries
explicit margins or sensitivities reflecting moderately adverse conditions for the non-economic risks [§6.A.2.b.i] — the
Valuation Manual therefore explicitly contemplates one engine serving both VM-30 cash flow testing and the VM-20 test.
**YRT relief:** passing gross of YRT but failing net still passes if `SERT_gy × LPIR_ny / LPIR_gy < 0.060` with `LPIR =
(b − a)/a` on each basis [§6.A.2.c]. **Blocking rule:** the SERT may not be used if the Demonstration Test was attempted
on current-year data and failed, or the qualified actuary actively undertook the certification and concluded it could
not legitimately be made [§6.A.2.d]. **Hedging bar:** a group with one or more future hedging strategies may not be
excluded from the SR except where all such strategies relate solely to features immaterial under §7.B.1 due to low
utilization [§6.A.1.b]. All [REG-R3]. **Deterministic Exclusion Test** [§6.B]:

```
DEEMED FAIL    ULSG that does not meet the "non-material secondary guarantee" definition, or any group not excluded
               from the SR requirement
NOT AVAILABLE  at all for term insurance policies or term riders
otherwise      Deterministic Net Premium Test: PASS iff Σ future valuation net premiums ≤ Σ corresponding guaranteed
               gross premiums, on a direct or assumed basis
```

Test conventions [§6.B.5]: lapse rates set to **0% at all durations** where the NPR comes from §3.B.4 or §3.B.5; for
shock-lapse designs the comparison considers **only the initial premium period**; and where anticipated experience
mortality plus §9.C.6 margins exceeds prescribed CSO, that basis must be used, mortality measured as the PV of future
death claims discounted at the NPR valuation rate. Guaranteed gross premium for UL with none specified is the level
annual gross premium at issue that would keep the policy in force for the whole coverage period on the guarantees
[§6.B.6]. A closed group passing three consecutive years is thereafter tested **at least once every five years**
[§6.B.4]. **Governance consequence:** passing via the DR-based SERT method, the VM-22 adjusted-scenario-reserve method
or the Demonstration Test **re-imposes VM-G Sections 2 and 3** on a company otherwise exempt, and a company computing no
DR or SR still files a VM-31 sub-report and must report **readiness to compute the DR and/or SR** [REG-R109][REG-R108].

---

## VM-21 and VM-22

**VM-21 (variable annuities), as an interface.** Scenario Reserves come from one stochastic run over the VM-21 §4
accumulated-deficiency construction. The reserve is **CTE 70** of the Scenario Reserves plus the **Additional Standard
Projection Amount** of VM-21 Section 6; the capital requirement is built from **CTE 98** of the *same* Scenario Reserves
plus the *same* ASPA [REG-R128][REG-R35]. Grouping, sampling, scenario count and simplification "should be identical to
those used in calculating the company's statutory reserves following VM-21", and certification and documentation follow
VM-31 [REG-R128][REG-R108]. AG 43 contracts are documented as VM-21 business, and where AG 43 business is aggregated
with VM-21 business VM-G applies to the combined valuation [REG-R108][REG-R109].

**The efficiency point, as an architectural requirement.** The variable annuity reserve and its capital requirement are
**two order statistics from a single stochastic run** [REG-R128][REG-R35]. Compute the Scenario Reserve vector once,
retain it, and read CTE 70 and CTE 98 off it; compute the ASPA once under VM-21 §6 and use it in both. Any design that
reruns the projection for capital is slower *and* can produce a CTE 70 > CTE 98 inconsistency that is undetectable
without the shared vector. VM-21 records the elective federal income tax treatment as the only substantive difference
between the reserve and RBC projections [REG-R35].

**VM-22 (non-variable annuities).** Its **Section 7 exclusion tests and Single Scenario Test** are the annuity
counterparts of VM-20 §6, and VM-G §1.A and VM-31 §2.A name VM-22 alongside VM-20 [REG-R36][REG-R109][REG-R108]. The
adjusted-scenario-reserve route of VM-22 §7.C.2.a.i carries the same VM-G Section 2/3 consequence as the VM-20 SERT DR
method [REG-R109]. The formulaic track survives inside VM-22 through VM-V §1 income annuity rates [REG-R37]. **This
research did not re-derive VM-22's internals** — build them from R36 directly. Reporting consequence: annuities valued
using VM-22 valuation interest rates are reported in Exhibit 5 split **Jumbo / Non-Jumbo in 50-basis-point valuation
interest bands** [REG-R89]. Transition: SSAP Nos. 3, 51 and 52 were revised in March 2026 to give guidance on the
**optional implementation period** for Valuation Manual revisions regarding the economic scenario generator and
non-variable annuities [REG-R88].

---

## Asset adequacy analysis and the actuarial opinion

**VM-30** is the operative requirement for the annual **statement of actuarial opinion** and supporting **actuarial
memorandum**, issued under Standard Valuation Law §3 [REG-R100]. The opinion covers **all in-force business on the
annual statement date, whether directly issued or assumed, regardless of when or where issued**; any shortfall found by
asset adequacy analysis must be **established as an additional reserve**, releasable later with disclosure; the
identification, scope, reliance and opinion sections carry **prescribed wording**, with a **table of key indicators**
ticked whenever wording changes and a **Category of Opinion** — Unqualified, Adverse, Qualified, Inconclusive. The
reporting granularity is an **asset-adequacy-tested amounts table** whose rows are annual statement lines (Exhibits 5,
6, 7, 8 Part 1 and separate accounts) and whose columns split every line into **Formula Reserves / Principle-Based
Reserves / Additional Reserves / Other Amount / Total**, with an **Analysis Method** symbol per line, every line printed
even when zero. **VM-30 contains no exemption clause and prescribes no interest scenarios** — the word "exempt" does not
appear in it [REG-R100].

**What the opinion asserts, and why a projection is therefore a statutory deliverable.** ASOP 22 defines asset adequacy
analysis as an analysis of reserve adequacy "in light of the assets supporting" the reserves, cash flow testing as the
projection and comparison of cash flows under one or more scenarios, and the operative threshold as **moderately adverse
conditions** — "one or more unfavorable, but not extreme, events that have a reasonable probability of occurring during
the testing period" [REG-R29]. Its starting-asset rule is the key sentence for model initialisation: "the actuary should
choose a block of assets such that the statement value of those assets is **no greater than** the statement value of the
reserves and other liabilities being tested" [REG-R29], restated by New York in Regulation 126 §95.10(b) [REG-R112].
Because Standard Valuation Law §6.B makes the actuary's required amount part of minimum reserves [REG-R1], the
multi-year projection is not a planning convenience — it is how a statutory number is determined. Analysis need not
always be cash flow testing (ASOP 22 also permits a gross premium reserve test, demonstrations of conservatism or of
immaterial variation, risk theory techniques and loss ratio methods), and a failing scenario does not automatically
require an additional reserve, since "the failure of a small percentage of them may not indicate the need for additional
reserves" [REG-R29].

**The state layer, and a correction the library should carry.** Model #822, the Actuarial Opinion and Memorandum
Regulation, is the pre-Valuation-Manual instrument; it is **not repealed**, remains the basis of many state regulations,
and VM-30 recognises appointments made under it [REG-R101][REG-R102][REG-R100]. The **"New York 7" interest scenarios
are a New York requirement**, from Regulation 126 §95.10(d) — not an NAIC requirement; nationally they appear only as an
*example* in a VM-20 §6 guidance note and as a *recommended* set in AG 55 [REG-R112][REG-R3][REG-R103]. Where a state
grants an exemption from asset adequacy analysis, the opinion rests on the formulaic reserve alone under **ASOP 57**
[REG-R113].

**Two overlays now sit on the analysis.** **AG 53** applies uniform practice to **complex and high-yielding assets** —
structured securities, CLOs, affiliate-originated assets — effective from the December 31, 2022 statement and scoped by
a **company-level size test** rather than by product; it is where the *asset side* of the same projection acquires
prescribed definitions, sensitivity tests and a benchmark table [REG-R105][REG-R106]. **AG 55** is the reinsurance
overlay: adopted, **effective for reserves reported in the December 31, 2025 annual statement**, first filings due April
1, 2026, disclosure-led rather than reserve-led, and requiring a mandatory cash-flow-testing run whose starting assets
equal the **post-reinsurance reserve** — the ceding company models the *reinsurer's* asset position; its §6.G accepts
documentation of the **pre-reinsurance PBR reserve** for a ceded block in lieu of that run, a direct instruction to
operate the PBR engine **gross of a specific treaty** [REG-R103][REG-R104]. Both are reviewed by the Valuation Analysis
(E) Working Group [REG-R107]. VM-30 §3.B.7 separately requires that cash flow testing **not solely project the
anticipated long-term average equity return** [REG-R100]. The Academy practice note is the fullest public description of
U.S. cash flow testing as a modelling exercise, with the caution that its quantitative statements come from **2004 and
2012 surveys** and are practice indicators, not benchmarks [REG-R111].

---

## Projecting reserves forward — the nested-valuation problem

**What actually requires it.** VM-20's DR and SR **do not project future statutory reserves at all**: the DR is a gross
premium valuation or a direct-iteration starting-asset solve, and the SR is built from projected *asset* statement
values [REG-R3]. Cash flow testing needs a reserve-like quantity at the **end**, not throughout: VM-30 defines ending
surplus operationally as either extending the projection until the remaining in-force and associated assets and
liabilities are immaterial, **or** adjusting end-of-projection surplus by an amount estimating the value expected to
arise from what remains in force [REG-R100]. Where reserves genuinely must be projected at every date is the capital and
distributable-earnings side: **C-3 Phase I requires S(t) = statutory assets − statutory liabilities at every calendar
year end of every scenario** [REG-R128], C-3 Phase II requires a projected statutory balance sheet including federal
income tax [REG-R47], and the RBC Plan requires five years of projected statutory income and surplus [REG-R125].
**[REG-R47] is the *pre-reform* C-3 Phase II package and is superseded in its parameters by the current instructions
[REG-R128]** — read it for the shape of the projection requirement, never for a CTE level, a scalar or a tax rate.

**The algorithm and its cost.** For each outer scenario ω and future date t the reserve at t is itself a valuation on
the in-force projected to t: `state(ω,t) ← project(product model, ω, t)`; `V(ω,t) ← Mode-V valuation at state(ω,t)`;
`S(ω,t) ← A(ω,t) − V(ω,t) − IMR(ω,t) − AVR(ω,t) − other liabilities`. Cost is `N_out × T × (inner cost)`, and if the
inner valuation is itself stochastic the inner cost is `N_in × T` and the run blows up quadratically.

**Mitigations, in the order to try them.** (1) **Formulaic reserves need no nesting** — CRVM, CARVM and the VM-20 NPR
are functions of projected policy state under prescribed assumptions, computable by a duration recursion at each date;
write the reserve routine to take a state vector, not a valuation date. (2) **Working-reserve proxy:** C-3 Phase II's
own standard device is **modelling the statutory reserve as equal to the working reserve** inside the projection
[REG-R47], with a **Tax Adjustment** required under Specific Tax Recognition where actual tax reserves exceed projected
tax reserves at the projection start [REG-R47][REG-R128]. The device and the tax adjustment both survive in the current
instructions [REG-R128]; the surrounding [REG-R47] parameters do not. (3) **One direct-iteration routine, three uses** —
iterating the starting asset amount until ending surplus is immaterial serves the VM-20 §4.B DR, the VM-21 reserve and
the CFT ending-surplus problem; the Academy practice note makes exactly this observation [REG-R111][REG-R3]. (4)
**Terminal value instead of a long horizon**, per VM-30's explicit alternative [REG-R100]; the discount rate for a PV of
ending surplus is a modelling choice, not a prescription — reported practice includes the after-tax portfolio earned
rate, Treasury spot rates, and inferring the factor by re-running with additional initial assets, from a **2012 survey,
indicative of practice shape, not a calibration target** [REG-R111]. (5) **Grouping and compression**, permitted only on
a demonstration that the simplification does not materially understate the reserve **and** that the expected value of
the simplified reserve is not less than the unsimplified one, model segmentation for net asset earned rates being exempt
from that demonstration [REG-R3 §2.G]; VM-31 §3.D.2 requires the grouping rationale and a commitment that any subgroup
can be audited against a seriatim model [REG-R108]. (6) **Proxy functions or fitted reserve surfaces** are an
engineering option **[std]**; no cited document sanctions them, and §2.G and §2.I still apply. **§2.I explicitly
disallows** the tempting shortcuts: not computing even a simplified NPR; not computing a simplified DR or SR without
passing the relevant test; omitting prescribed mortality margins; establishing no lapse margins; not building even a
simplified asset model for the DR; using the alternative investment strategy without first showing it produces a higher
reserve; and **ignoring post-level-term losses** [REG-R3].

---

## Statutory income and surplus roll-forward

**The recursion**, on the Summary of Operations line sequence [REG-R90]:

```
Income(t)       = Prem(t) + ConsiderationsSupplContractsLifeCont(t) + NII(t) + IMRamort(t) + SA_NetGainFromOps(t)
                + CommAndExpAllowancesOnCeded(t) + ReserveAdjustmentsOnCeded(t) + MiscIncome(t)   # incl. deposit-type fees
Benefits(t)     = Death(t) + MaturedEndowments(t) + AnnuityBenefits(t) + DisabilityAndAH(t) + Coupons(t)
                + SurrenderAndWithdrawal(t) + GroupConversions(t) + InterestOnContractAndDepositFunds(t)
                + PaymentsSupplContractsLifeCont(t) + ΔV(t)              # ΔV = increase in aggregate reserves, Line 19
Expenses(t)     = Commissions(t) + GeneralExpenses(t) + InsuranceTaxesLicencesFees(t) + ΔLoading(t)
                + NetTransfersToSeparateAccounts(t) + WriteIns(t)
GainPreTax(t)   = Income(t) − Benefits(t) − Expenses(t) − PolicyholderDividends(t)
GainAfterTax(t) = GainPreTax(t) − FIT(t)
S(t) = S(t−1) + GainAfterTax(t) + NetRealizedCapitalGains(t) + ΔUnrealizedCapitalGains(t) − ΔAVR(t)
     − ΔNonAdmittedAssets(t) + ChangeInValuationBasis(t) + CapitalAndSurplusPaidIn(t) − StockholderDividends(t)
     + OtherSurplusAdjustments(t)
```

with `ΔV(t) = V(t) − V(t−1)` on the **statutory** reserve and `ΔLoading(t)` the change in loading on deferred and
uncollected premium, which is an **expense**, not a reduction of premium [REG-R79 ¶11]. Acquisition costs enter
`Commissions` and `GeneralExpenses` **in the period incurred, with no deferral and no DAC asset** [REG-R75 ¶2]; why that
reshapes the earnings signature relative to GAAP is in "Why statutory differs from GAAP" above. The lower recursion is
the Capital and Surplus Account, which several items reach without passing through income: the change in valuation basis
is measured as old-basis minus new-basis reserve **as of the beginning of the year**, goes **direct to surplus**, is
**not** graded in unless an NAIC actuarial guideline prescribes a transition, and is **excluded** from both the Summary
of Operations and the Analysis of Operations, appearing in Exhibit 5A [REG-R79][REG-R80 ¶14][REG-R89]; AVR movements go
directly to surplus [REG-R86]; non-admitted assets are charged against surplus rather than carried [REG-R74 ¶36]; and
the change in non-admitted disallowed IMR runs through the same account [REG-R87][REG-R89].

**Analysis of Increase in Reserves During the Year** [REG-R90], by the same product columns as the Analysis of
Operations. Additions: 1 opening reserve; 2 **tabular net premiums or considerations**; 3 PV of disability claims
incurred; 4 **tabular interest**; 5 **tabular less actual reserve released**; 6 increase on account of **change in
valuation basis**; **6.1 change in excess of VM-20 deterministic/stochastic reserve over net premium reserve**; 7 other
increases (net); 8 totals. Deductions: 9 **tabular cost**; 10 reserves released by death; 11 reserves released by other
terminations (net); 12 annuity, supplementary contract and disability payments involving life contingencies; 13 net
transfers to or from separate accounts; 14 total deductions; 15 closing reserve; then 16 ending CSV and 17 the amount
available for policy loans on that CSV. These are **reserve-basis** quantities, not experience quantities. The
instructions' precise definitions were **not transcribed by the research** [REG-R89]; the reference implementation uses
**[std]** `TabNetPrem(t) = Σ_j π_j·l_j(t−1)`, `TabInterest(t) = i_v·(V(t−1) + TabNetPrem(t))`, `TabCost(t) = Σ_j
q^val·(B_j − V_j(t))·l_j(t−1)` and `ReservesReleasedByDeath(t) = Σ_j q^val·V_j(t)·l_j(t−1)`, so that `TabCost +
ReservesReleasedByDeath` equals expected death benefits on the valuation basis — which is why the statement can deduct
both without double counting **[std, derived]**. Read the operative definitions from [REG-R89] before filing.

**The reconciliation identity that must hold**, at every t: `S(t) = A(t) − L(t)` with `L(t) = V(t) + IMR(t) + AVR(t) +
other statutory liabilities`, **and** `S(t) − S(t−1)` = after-tax gain plus the direct-to-surplus items above. Assert
both: the first catches a reserve or asset booking error, the second catches an item routed to the wrong statement.

---

## Asset valuation reserve and interest maintenance reserve

SSAP No. 7 is deliberately thin — it states the principle and delegates the arithmetic to the SSAP for the specific
investment type or, failing that, to the **Annual Statement Instructions** [REG-R85]. It scopes both reserves to life
and A&H insurers **excluding separate accounts**, whose AVR and IMR live in SSAP No. 56 [REG-R85][REG-R83]. Both are
named in the Statement of Concepts as statutorily mandated liabilities [REG-R74 ¶37], and both are absent from GAAP:
"AVR and IMR are not addressed in current GAAP literature" [REG-R86 ¶13].

**What each absorbs.** The **AVR** offsets "potential credit-related investment losses on all invested asset categories
excluding cash, policy loans, premium notes, collateral notes and income receivable" [REG-R85 ¶2] — a mechanism "to
absorb unrealized and credit-related realized gains and losses" [REG-R86 ¶6] — across two components and four
sub-components (bond and preferred stock including derivative counterparty exposure; mortgage; common stock; real estate
and other invested assets), with movements charged or credited **directly to surplus**, not through the summary of
operations [REG-R86]. The **IMR** "defers recognition of the realized capital gains and losses resulting from changes in
the general level of interest rates", amortising them into **investment income** over "the expected remaining life of
the investments sold", and also captures certain **liability** gains and losses from interest rate changes, amortised
over the expected remaining life of the liability released [REG-R85 ¶2].

**Why the IMR amortises rather than releasing.** In the codifiers' words it exists "to protect surplus from investment
transactions that are entered into as a reaction to interest rate movements" and to reduce **gains-trading** opportunity
[REG-R86 ¶7]; without it an insurer could realise interest-driven gains at will and book them as current income. The
IMR/AVR split for a bond turns on the **change in NAIC designation over the holding period** — interest-related if the
designation moved by one or less, credit-related otherwise, with anything ever designated "6" going to AVR, plus an
override for acute credit events [REG-R89][REG-R86]. Reporting is a 30-year amortisation grid plus an "and later" row,
released annually to **Summary of Operations Line 4** and allocated by line of business [REG-R90].

**The asset-side interface with no GAAP analogue.** A model producing only liability cash flows cannot produce either
reserve. Both need the **asset** projection to yield disposal-level detail: for the IMR, projected interest-related
realized gains and losses net of tax with an expected maturity date per disposal lot; for the AVR, projected
credit-related realized and unrealized movements by sub-component with book values by NAIC designation and mortgage
category [REG-R89][REG-R90]. Two liability-side legs matter here: the IMR captures interest-related gain or loss on
**reinsuring a block of liabilities** [REG-R86][REG-R92 ¶54] and on **market value adjustments** on contracts backed by
assets carried at book [REG-R86] — where MVA-bearing fixed deferred annuities and RILAs meet the IMR. There is also an
**excess-withdrawal exemption** routing gains and losses on investments funding withdrawal activity above a threshold
straight to net income, an anti-double-count exclusion for gains already used to adjust contract benefits or reserves
[REG-R89], and an election on hedge termination to route derivative gain or loss into IMR [REG-R96 ¶17] — a paragraph
number taken from the **2010 standalone print** of SSAP No. 86 and never cross-checked against the March 2026 manual, so
the numbering is **[unverified]** even though the rule is first-hand [REG-R96]. **This document states no AVR factor and
no IMR amortisation factor: the research explicitly did not transcribe them** [REG-R89].

**IMR — the amortisation algorithm.** The operative scope rule the algorithm needs is the one stated above: the IMR
carries interest-rate-driven realized gains and losses on investments sold **and** certain liability gains and losses,
each amortised over the expected remaining life of the item released [REG-R85 ¶2]. Balance recursion, per the annual
statement form [REG-R90]: `IMR(y) = IMR(y−1) + Σ_d g_net(d) ± LiabilityAdjustment(y) − Amort(y)`, where `g_net(d)` is
the current-year realized pre-tax gain transferred **net of taxes** and `Amort(y)` is released to **Summary of
Operations Line 4**. The supporting schedule is a grid of **30 future calendar years plus an "and later" row**; the
balance sits at Page 3 Line 9.4 and the amortisation is allocated by line of business [REG-R89][REG-R90]. Per disposal
d:

1. **Classify.** Interest-related (→ IMR) if the NAIC designation at the end of the holding period differs from the
   beginning designation by **one or less**; otherwise credit-related (→ AVR); anything ever designated **"6"** during
   the holding period always goes to AVR; and an **acute credit event** not yet in CRP ratings or the SVO feed that
   predominantly drove the gain/loss excludes it from IMR. A gain is **either** interest or non-interest, never a blend,
   except as SSAP No. 43 specifies; same-CUSIP purchase lots are treated as individual assets [REG-R89].
2. **Exclude** gains and losses that per contract terms directly increased or decreased **contract benefit payments or
   reserves** in the period, and those funding **excess withdrawal activity** (below) [REG-R89].
3. **Net of tax.** Capital gains tax follows the company's own statutory allocation method, and the attached tax
   amortises **in proportion to the pre-tax amortisation** [REG-R89].
4. **Set the expected maturity date.** Fixed-repayment instruments use the contractual retirement date producing the
   lowest amortisation value (**yield to worst**) across all call dates and maturity; scheduled sinking funds add a
   yield-to-average-life calculation at 50% repaid; **puttable** instruments use the put or maturity date producing the
   **highest IRR**; SVO Identified Funds on systematic value use the WAL of the underlying bonds; **perpetuals, and
   fixed income with no maturity date or sinking fund schedule, use 30 years**; MBS/ABS use remaining WAL on
   repurchase-price prepayment assumptions. A callable bond bought at a premium and called or sold **after** its
   expected maturity date has **no amortisation** — the gain or loss goes straight to income, likewise a convertible
   disposed of after its expected maturity date [REG-R89].
5. **Amortise by one of two methods, locked in for that year's gains once chosen and not changeable without commissioner
   approval** [REG-R89]. **Seriatim:** the annual amortisation is the excess of the income that would have been reported
   had the asset **not** been disposed of over the income that would have been reported had it been **repurchased at its
   sale price**; for MBS/ABS on a schedule built from the prepayment assumptions that would have applied at the
   repurchase price. **Grouped:** group net-of-tax gains by **calendar years to expected maturity** in the bands **0, 1,
   2–5, 6–10, 11–15, 16–20, 21–25, over 25** (calendar year of maturity minus calendar year of sale) and multiply by the
   **published amortisation factors for the year of sale**, each year's gains using that year's table for all future
   years, current-year gains on the prior year's factors until the current table is published. **Those factor tables are
   published annually and were not transcribed by the research; no value is stated here** [REG-R89]. The current bands
   begin with a separate "0 calendar years" band, unlike the 1990s text in the issue paper [REG-R86].

**Liability leg.** The interest-rate-related gain/loss net of tax on the sale, transfer or reinsurance of a **block of
liabilities** enters IMR only where the portion reinsured exceeds **5% of general account liabilities** (Page 3, Line
26), the transaction is **irrevocable and to a non-affiliate**, and it completed in the current year; the amount is the
**negative of the sum** of the IMR balance and future amortisation from past and present dispositions of the block's
associated assets plus the IMR that would arise if the remaining associated assets were sold [REG-R86][REG-R92 ¶54].
Material **market value adjustments** on contracts backed by assets carried at book also enter IMR, amortised
consistently with the MVA determination; **material = in excess of both 0.01% of liabilities and $1,000,000** [REG-R86].

**Excess-withdrawal exemption, as a procedure** [REG-R89]:

```
WR(y−1) = withdrawable reserves at BOY: reserves and liabilities net of policy loans on any policy or contract subject
          to withdrawal or surrender WITHOUT an MVA at the holder's discretion (ordinary and industrial life, SPDAs,
          benefit-sensitive GICs), NET OF REINSURANCE
EW(y)   = effective withdrawals: unscheduled withdrawals and surrenders computed without market adjustment + net
          increase in policy loans + cash transfers to separate accounts other than pass-through transfers of new
          premium, NET OF REINSURANCE
wr(y)   = EW(y) / WR(y−1) ;   TWL(y) = 1.50 × min( wr(y−1), wr(y−2) ) × WR(y−1) ;   XS(y) = max(0, EW(y) − TWL(y))
```

Gains and losses on the investments required to fund XS(y) are **excluded from IMR and flow straight to net income**,
identified specifically where possible and otherwise pro rata across the year's sales [REG-R89].

**AVR — the accumulation mechanic.** Purpose and scope are above; what the algorithm needs is the sub-component
structure — Default (bond and preferred stock including derivative counterparty exposure; mortgage) and Equity (common
stock; real estate and other invested assets) — over the SSAP No. 7 ¶2 asset base, which excludes cash, policy loans,
premium notes, collateral notes and income receivable [REG-R85 ¶2][REG-R86 ¶11(B)]. Per sub-component c per year
[REG-R89][REG-R90]:

```
Bal_c(y) = Bal_c(y−1) ± RealizedGains_c(y) net of tax          # general and separate accounts on separate lines
         ± UnrealizedGains_c(y) net of deferred tax on an SSAP No. 101 basis
         − GainsCreditedOrLossesChargedToContractBenefitsOrReserves_c(y)          # anti-double-count line
         + BasicContribution_c(y) + Accumulation_c(y) ± Transfers_c(y) + VoluntaryContribution_c(y)
Accumulation_c(y) = 0.20 × ( ReserveObjective_c(y) − accumulated balance )        # negative when the objective is exceeded
then floor at 0 and cap at Maximum_c(y)
```

The **20% of the shortfall to the reserve objective** is the only numeric parameter of this mechanic the research
captured [REG-R89, AVR Line 11]. The three factor families have stated *roles*: the **basic contribution factor**
produces on average an amount approximating expected annual losses; the **reserve objective factor** targets an
accumulation covering, in the aggregate, **about 85% of the distribution of losses** for the asset category; the
**maximum reserve factor** caps the accumulation. They are tabulated by NAIC designation (bonds, preferred stock,
short-term, derivative counterparty exposure) and by mortgage category using the **Life RBC classification
methodology**, on the AVR supporting forms — **the numeric factors were not transcribed and no value is stated here**
[REG-R89][REG-R90]. Transfers: an excess over a sub-component maximum goes to its sister sub-component if that sister is
below its maximum; an excess over a whole component's maximum may move to the other component or be **released to
surplus**; a negative sub-component balance transfers to its sister only to the extent it does not reduce the sister's
positive pre-transfer balance below **50%**; and there are **no transfers between AVR and IMR** [REG-R89]. U.S.
government and full-faith-and-credit agency securities are exempt from AVR, and affiliated life insurers maintaining
their own AVR carry a **0% maximum reserve factor** [REG-R89]. Movements go direct to surplus; the balance sits at Page
3 Line 24.01 [REG-R86][REG-R89]. Separate account IMR and AVR follow their own rules, set out in "Separate accounts"
below [REG-R83].

**Negative IMR admittance — the gates, as a computable test.** Baseline: a positive net IMR is a liability at Page 3
Line 9.4; a **negative** net IMR ("disallowed IMR") is a miscellaneous other-than-invested write-in asset and
**non-admitted**, the change running through the Capital and Surplus Account [REG-R87 ¶¶3–4][REG-R89]. INT 23-01 gives a
limited-time, optional exception [REG-R87]:

```
cap    = min( 0.10 × AdjCapSurplus(most recently filed statement), 0.10 × CapSurplus(current period, unadjusted) )
         # ¶9.a; the second cap was added in the August 2025 revision. AdjCapSurplus excludes net positive goodwill,
         # EDP equipment and operating system software, net deferred tax assets, and admitted net negative IMR
gate 1 : adjusted RBC greater than 300% of Authorized Control Level, TAC adjusted for the same four items, AFFIRMED
         for every quarterly and annual statement in which admitted negative IMR is reported            # ¶9.b
gate 2 : derivative losses carried at fair value before termination are eligible ONLY with documented historical
         evidence that fair-value derivative GAINS were reversed to IMR and amortised — evidence required separately
         for the general account, the insulated separate account and the non-insulated separate account  # ¶9.c
gate 3 : the ¶13 data-captured disclosures are fully completed, else NON-ADMIT ALL                       # ¶9.d
gate 4 : admitted negative IMR is captured in the PBR calculation or in asset adequacy / cash flow testing under
         VM-20 §7.D.7 and VM-30 §3.B.5, with a reconciliation to the IMR reflected there                 # ¶9.e
order  : admit ALL general account net negative IMR first, up to cap; only if the cap is not reached may a separate
         account IMR ASSET be recognised, allocated proportionately between insulated and non-insulated  # ¶10
```

Reporting: a general account write-in to miscellaneous other-than-invested assets, **asset page line 25**, captioned
"Admitted Disallowed IMR", with an **equal amount allocated from unassigned funds to special surplus funds line 34**,
expressly "to preclude the ability for admitted negative IMR to be reported as funds available to dividend"; separate
accounts use asset page line 15 and special surplus line 19 [REG-R87 ¶¶11–12].

The condition that makes this a *modelling* problem rather than a disclosure problem is **¶9.e**: an entity admitting
negative IMR must **capture the admitted negative IMR in the PBR calculation or in asset adequacy / cash flow testing
under VM-20 §7.D.7 and VM-30 §3.B.5**, and reconcile it to the IMR reflected there "to ensure reserves are not
overstated" [REG-R87]. An accounting admittance decision therefore changes a reserve. VM-30 §3.B.5 independently
requires an appropriate allocation of assets in the amount of the IMR, **positive or negative**, in *any* asset adequacy
analysis; requires any portion of the total company IMR **not admitted** to be removed first; and requires **the full
amount of any admitted negative IMR to be used**, in which case the allocated assets are reduced by its absolute value
[REG-R100]. The IMR has **no cash flows** of its own — it is a sign-aware, non-cash-flow adjustment to starting assets
[REG-R111]. Assets supporting the **AVR** may be allocated for **asset default risk only**, may not be applied to any
other risk, and the amount used must be disclosed in both the opinion's reserve table and the memorandum [REG-R100];
because that consumed AVR is also removed from Total Adjusted Capital, the asset adequacy routine must **report how much
AVR it used** — an input to the capital numerator, not a by-product ([REG-R128]; see "Risk-based capital" below).

**Status, stated honestly.** INT 23-01 was adopted August 13, 2023 through December 31, 2025 with automatic
nullification January 1, 2026, and was **extended on August 11, 2025 by one year to December 31, 2026, with automatic
nullification January 1, 2027**; the date may move again [REG-R87 ¶¶14–15]. The replacement is a **substantially revised
SSAP No. 7** absorbing the AVR/IMR guidance from the annual statement instructions, with a supporting issue paper: an
initial version reached the IMR Ad Hoc Group on February 24, 2026 and exposure was expected after the March 2026 Spring
National Meeting, at which an "IMR **proof of reinvestment**" concept was adopted [REG-R88]. **The exposed revised SSAP
No. 7 was not located or read**, and the 2026 Summer National Meeting had not been reported on at the research access
date [REG-R88]. Note that the Academy practice note, written September 2024, states the interim solution was nullified
January 1, 2026 — **superseded by the August 2025 extension** [REG-R111][REG-R87].

---

## Separate accounts

**Two balance sheets, one income statement.** SSAP No. 56 keeps sales, underwriting, contract administration, premium
collection, premium tax, claims and benefits as **general account** functions [REG-R83 ¶4]. For separate account
contracts classified as life contracts, premiums and considerations are income in the **general account** summary of
operations and simultaneously a **transfer** to the separate account statement; separate account charges — investment
management, administration, contract guarantees — and the separate account's net gain from operations are general
account income; benefits, surrenders, net transfers, commissions and premium taxes are general account expenses [REG-R83
¶5]. The annual statement reinforces this: every transfer reported on the separate accounts transfer line must **also**
appear in the premium, benefit, withdrawal or other captioned lines of the Analysis of Operations [REG-R89].

**General-account guarantee reserves and the surplus floor.** A **GMDB reserve on a variable annuity or variable life
contract is held in the general account**, and any difference between the benefit paid and the separate account value is
charged or credited to general account net gain from operations [REG-R83 ¶7]. VM-20's split rule is the mirror image:
the general account share may not be **less than zero** and must include any liability for general-account contractual
guarantees, while the separate account share must be at least the sum of cash surrender values and at most the sum of
account values [REG-R3]. And **"separate account surplus may not become negative"** — the general account funds any
deficiency, a mortality deficiency on annuitized contracts being funded by a general account expense matched by separate
account revenue, with mortality gains running the other way [REG-R83 ¶8]. Surplus created by CRVM or CARVM is reported
by the general account as an **unsettled transfer** [¶9]; seed money is separate account surplus until repatriated
[¶10].

**Fair value versus book value, and which products are now eligible for book value.** Separate account assets are at
**fair value** *except* the ¶18 categories, carried "as if the assets were held in the general account", i.e. at **book
value**: ¶18.a employer-plan fixed-rate fund accumulation GICs that do not participate in portfolio experience, and
**¶18.b, with state regulator approval, insulated or non-insulated contracts similar to general account contracts that
do not pass all investment experience through, where the general account "may serve as an overall backstop or may
provide an implied guarantee" — naming pension risk transfer, bank-owned life insurance and *registered index-linked
annuity* contracts as expected examples** [REG-R83 ¶¶17–18]. The exposure draft records why: the ACLI asked to delete a
reference to general-account benefits "not directly tied to the performance of the underlying assets", and staff
substituted the backstop / implied-guarantee language while keeping the examples [REG-R84]. **Any assumption that a RILA
separate account must be at fair value is wrong** — this is the accounting counterpart to the product-side treatment at
[REG-R44] and [REG-R43].

The measurement basis then propagates three ways a model must follow. **The liability basis must follow the asset
basis**: A-820 valuation interest rates where assets are on a general-account basis, **current market-based rates where
assets are at fair value** [REG-R83 ¶30][REG-R153]. **The reserve-side counterpart for MVA business is now sourced.**
A-255 ¶5 requires that the separate account liability be **at least the surrender value produced by the contract's own
market-value-adjustment formula** — the formula is the contract's, not a prescribed one, and A-255 prints neither a
formula nor a parameter for one — that any shortfall against the market value of the separate account assets be made
good by a **transfer into that account**, and that "any additional reserve that is needed to cover future guaranteed
benefits shall be established", with ¶6 requiring the MVA formula, the interest guarantees and asset/liability cash flow
matching to be considered and an affirmative company determination of asset adequacy for all guaranteed benefits
[REG-R157]. A-250 imposes the parallel asset-coverage floor for variable annuity separate accounts and delegates the
reserve itself to A-820 [REG-R156]. **A-255 ¶1 also carries a definition with load-bearing use elsewhere**: VM-21 §2.A.2
excludes contracts falling under VM-A item A-255, and the test for that exclusion is A-255's own four-element definition
— a deferred annuity, individual or group; underlying assets held in a separate account; values guaranteed if held for
specified periods; nonforfeiture values on an MVA formula if held for shorter periods — plus the requirement that the
assets be in a separate account "during the period or periods when the contract holder can surrender the contract".
**The exclusion is VM-21's text, not A-255's; A-255 supplies only the definition** [REG-R157][REG-R35]. **Separate
account IMR is required where assets are at book value and not where they are at fair value**, applied account by
account [¶¶26–27]. **Separate account AVR** is required where the reporting entity rather than the policyholder bears
default and fair-value loss — so traditional VA and VL separate accounts need none except on the **seed money** portion,
while book-value separate accounts, modified guaranteed contracts, MVA contracts and contracts with book-value
guarantees do — and it is **combined with the general account AVR** for reporting [¶¶11, 23–25]. A RILA statutory model
may therefore need a **book-value separate account carrying its own AVR and IMR**, unlike a traditional VA. Open
regulator questions on the glossary definition of *Guarantee* and on non-cash-transfer IMR guidance are at [REG-R84],
and a March 2026 revision on nonadmittance for general-account-basis assets in the separate account at [REG-R88].

---

## Reinsurance and taxes

**Reinsurance.** Exhibit 5 reserves are computed **gross**, with a **ceded deduction computed using the same mortality,
interest and valuation method** but reflecting the actual mode of reinsurance; because the assuming reinsurer may value
differently, the ceded deduction need not equal the assumed reserve, and **no deduction is taken for modified
coinsurance** [REG-R89]. The ceding entity's reserve credit is **a reduction of reserves, not an asset**; YRT credit is
the one-year term mean reserve on the amount ceded on the *original policy's* mortality and interest basis [REG-R92
¶¶36–38]. Credit exists only where the assuming insurer qualifies under Credit for Reinsurance Model Law #785 or the
asset-or-reduction-from-liability route, with Model Regulation #786 supplying trust and letter-of-credit mechanics
[REG-R94][REG-R95]. **Risk transfer is the gate**: an agreement that limits or diminishes risk transfer or "contains any
contractual feature that delays timely reimbursement" follows **deposit accounting** instead, multiple contracts
achieving "one overall planned effect" are evaluated together, and combined structures must in aggregate avoid the
Appendix A-791 prohibited conditions [REG-R92 ¶17] — **A-791 itself was cited only through SSAP No. 61 and not read**.
For a model the requirement is that gross and ceded be produced **separately, not netted**, so Exhibit 5 and Schedule S
can be filled; losses are recognised immediately, and recaptures unwind through the original accounts with the required
IMR adjustment [REG-R92 ¶¶55–58]. A March 2026 exposure would require **funds withheld liabilities to equal the carrying
value of the funds withheld assets**, adoption unknown [REG-R88].

**Taxes.** SSAP No. 101 adopts FAS 109 with modifications for state income taxes, deferred tax asset **realization
criteria**, and the recording of changes in deferred tax balances, effective January 1, 2012 [REG-R97]. Net admitted
deferred tax assets may not exceed adjusted gross DTAs less gross DTLs, and adjusted gross DTAs are admitted as the sum
of three components: recovery through **loss carryback**; an amount realizable within a period and capped at a
percentage of adjusted capital and surplus, both driven by the company's **ExDTA Authorized Control Level RBC ratio**;
and the remainder offsettable against existing DTLs respecting character [REG-R97]. The life-specific point: entities
taxed as life insurance companies **may not carry back ordinary losses arising in tax years after 2017**, so ordinary
DTA admittance runs entirely through the RBC-band and DTL-offset components [REG-R97]. Entering a model, this means
carrying the **statutory reserve and the tax reserve** — the latter built off the former with a haircut and a cap under
IRC §807 [REG-R16][REG-R72] — so temporary differences, their reversal pattern and their character can be scheduled,
alongside projected surplus and a projected ExDTA RBC ratio. The Realization Threshold Limitation Tables themselves are
in SSAP No. 101 ¶11 [REG-R97]; a practitioner source independently reproducing them is at [REG-R98].

---

## Risk-based capital

**Purpose and instrument.** RBC is a solvency early-warning and intervention tool sitting above the accounting layer.
Its enabling statute, the **Risk-Based Capital (RBC) for Insurers Model Act (#312)**, defines the four RBC Levels as
fixed multiples of **Authorized Control Level RBC**, sets the filing date, enumerates the risk factors the life formula
must reflect, and defines four supervisory *Events* — but **contains no formula**, delegating entirely to the RBC
Instructions [REG-R125][REG-R127]. The **RBC Report** is filed by every domestic insurer on or before March 1 for the
preceding calendar year end; a report the commissioner judges inaccurate becomes an **Adjusted RBC Report** [REG-R125].

**The action levels and what triggers each** [REG-R125]. Company Action Level RBC is **2.0×**, Regulatory Action Level
**1.5×**, and Mandatory Control Level **0.70×** Authorized Control Level RBC, which is **1.0×** by definition; the
headline **Authorized Control Level RBC Ratio is Total Adjusted Capital ÷ Authorized Control Level RBC**
[REG-R125][REG-R128][REG-R127]. A **Company Action Level Event** occurs when Total Adjusted Capital falls between
Regulatory and Company Action Level RBC — or, for a life or fraternal insurer, between Company Action Level RBC and
**3.0×** Authorized Control Level **with a negative trend** — and requires an **RBC Plan** within 45 days. A
**Regulatory Action Level Event** adds a corrective order and examination, and is also triggered by failure to file, to
submit a Plan, or to adhere to one. An **Authorized Control Level Event** permits the commissioner to place the insurer
under regulatory control; a **Mandatory Control Level Event** requires it for a life insurer. The **RBC Plan must
project statutory operating income, net income, capital and surplus for the current year and at least four succeeding
years, both with and without proposed corrective actions** [REG-R125] — the only place the model act itself mandates
projection output, and the reason a liability cash flow model sits on the critical path for RBC rather than only at the
valuation date.

**Read every number in this section against its source limit.** All of it comes from the **2024** *Life and Fraternal
Risk-Based Capital Forecasting and Instructions*, a **sold NAIC publication marked "Not for Distribution"**, read from a
copy posted by the Indiana Department of Insurance [REG-R128]; the 2023 edition was used only to date the structures
[REG-R129]; **the 2025 edition could not be parsed, so nothing here is a year-end 2025 factor** [REG-R129][REG-R139].
Buy the current edition before filing.

**The risk components and what drives each** [REG-R128]. As published: **C-0** is the declining value of insurance
subsidiaries plus off-balance-sheet and miscellaneous items; **C-1** is asset default or fluctuation in fair value;
**C-2** is the risk of underestimating liabilities on business already written or inadequately pricing business to be
written in the coming year; **C-3** is loss from changes in interest rate levels and from changes in market levels
associated with variable products with guarantees; **C-4** is general business risk. Within them:

- **C-1o** applies designation-level factors to book/adjusted carrying value sourced from the AVR Default Component
  across **20 NAIC designation categories**, modified by a **bond size factor** keyed to weighted issuer count; the
  calibration — default-rate term structures fitted to insurers' holdings, a correlation model, a risk premium at
  **expected loss plus half a standard deviation** — is at [REG-R130]. **C-1cs** carries unaffiliated common stock and
  non-insurance affiliates separately, because that risk was found independent of the others [REG-R136].
- **C-2 mortality** is driven by **net amount at risk**, net of reinsurance, now derived from the annual statement
  rather than company records [REG-R142], bucketed **not by product code but by pricing flexibility** — the ability to
  *materially* adjust rates on in-force contracts within the next five policy years — with the **worst bucket as the
  default where the assessment is not performed** [REG-R128][REG-R133]. Calibration targets the 95th percentile in
  excess of reserve mortality [REG-R131][REG-R132].
- **C-2 longevity** is driven by the **statutory reserve** for life-contingent annuity benefits — payout annuities in
  pay status, deferred income annuities that will enter it, structured settlements, pension risk transfer, variable
  *immediate* annuity reserves — including the period-certain portion of a certain-and-life contract, and expressly
  **excluding** deferred annuities where annuitization is a right not an obligation and variable *deferred* reserves
  under VM-21 even after account exhaustion [REG-R128]. Design record at [REG-R134].
- **C-3a** is the surplus needed for lack of synchronization of asset and liability cash flows, so **risk categories
  vary by withdrawal provision** — fair-value-adjusted, not withdrawable, book value less a surrender charge, book value
  without adjustment [REG-R128]. A company either applies factors or performs **C-3 Phase I cash flow testing** on the
  year-end asset adequacy model with prescribed scenarios and a different measurement; two exemption tests decide
  whether testing is mandatory, and once elected the method must continue absent regulator approval [REG-R128]
  [REG-R135]. **Equity-indexed products take the same factors as their non-indexed counterparts, "based on guaranteed
  values ignoring those related to the index", and are excluded from C-3 cash flow testing** [REG-R128].
- **C-3c** is **C-3 Phase II** for the AG 43 / VM-21 population, built on **CTE 98** of the same Scenario Reserves used
  for the reserve, plus the Additional Standard Projection Amount, less the statutory reserve, with a scalar and a tax
  step [REG-R128]. It replaces the CTE 90 / Total Asset Requirement construction recorded at [REG-R47], which is the
  **pre-reform** package and is **superseded in its parameters** — never read a CTE level, a scalar or a tax rate off
  it. [REG-R48] is the reform analysis behind the change, and recommended CTE 95 with a 25% scalar where the adopted
  instructions land on CTE 98 with that scalar: the scalar survived, the CTE level did not [REG-R48][REG-R128].
- **C-4a** is business risk on premiums and separate account liabilities, referenced to guaranty fund assessment
  exposure; **C-3b** and **C-4b** are health-related and immaterial here [REG-R128].

**Where each lands on the RBC pages, and the numbers behind the drivers.**

| Component | Driver | Page |
|---|---|---|
| **C-0** | insurance subsidiaries plus off-balance-sheet and miscellaneous items; a life affiliate contributes its own **line (69) plus twice its AG 48 shortfall**, prorated by ownership | LR031 [REG-R128] |
| **C-1o** | asset default on bonds, mortgages and other non-common-stock assets: BACV × factor by NAIC designation × **bond size factor** | LR002 etc. [REG-R128] |
| **C-1cs** | unaffiliated common stock, Schedule BA common stock, the concentration factor, affiliated non-insurers | LR031 [REG-R128][REG-R136] |
| **C-2** | mortality on business written (**NAR**-based) and **longevity** (**reserve**-based), plus health claim reserves and the premium stabilization credit | LR025, LR025-A [REG-R128] |
| **C-3a** | interest rate risk: factor charges by **withdrawal provision**, or C-3 Phase I cash flow testing, plus the interest component from Phase II | LR027 [REG-R128] |
| **C-3b / C-3c** | health credit risk / market risk from variable products with guarantees (C-3 Phase II) | LR028, LR027 line 37 [REG-R128] |
| **C-4a / C-4b** | general business risk: **2.53%** of Schedule T life premiums and annuity considerations, **0.63%** of A&H premiums, **0.06%** of separate account liabilities / health administrative expense | LR029 [REG-R128] |

C-1o bond factors run across **20 designation categories**, from 1.A at **0.00158** to 5.C and NAIC 6 both at
**0.30000** [REG-R128][REG-R130]. The **bond size factor** aggregates by issuer (first six CUSIP digits): weighted
issuers = 2.40 × first 50 + 1.53 × next 50 + 0.85 × next 100 + 0.85 × next 300 + 0.82 × over 500; size factor = total
weighted issuers ÷ total issuers; **a blank issuer count is charged the maximum 2.40** [REG-R128]. LR002's published
*Basis of Factors* narrative still describes the pre-2021 calibration while the factors are the 2021 Moody's set — an
observation from comparing two documents, **[unverified]** as to NAIC intent [REG-R128][REG-R130].

**C-2 mortality: the NAR definition and the pricing-flexibility test.** Exposure base, **net of reinsurance
throughout**, now derived from the annual statement rather than free-form company records [REG-R142]:

```
Total Individual & Industrial Life NAR
  = (Exhibit of Life Insurance, sum of Columns 2 and 4, Line 23 × 1000)
  − [ (Exhibit 5, sum of Columns 3 and 4, Line 0199999) + (Separate Accounts Exhibit 3, Column 3, Line 0199999)
    + (General Interrogatories Part 2, Column 1, Line 10.01) − (General Interrogatories Part 2, Column 1, Line 10.02) ]
```

i.e. **face amount in force minus life reserves, general account plus separate account, with a reinsurance adjustment**
[REG-R142]. Size bands apply to the *total* for individual and industrial life and separately to the total for group and
credit life, then are allocated proportionately to each factor category: band 1 up to **$500 million** NAR, band 2 above
$500 million to **$25 billion**, band 3 above $25 billion [REG-R128][REG-R133].

| Category (pre-tax, per dollar of NAR) | First $500M | Next $24,500M | Over $25,000M |
|---|---|---|---|
| Individual & Industrial **with** Pricing Flexibility | 0.00220 | 0.00105 | 0.00080 |
| Individual & Industrial **Term without** Pricing Flexibility | 0.00280 | 0.00120 | 0.00085 |
| Individual & Industrial **Permanent without** Pricing Flexibility | 0.00400 | 0.00175 | 0.00120 |
| Group & Credit Term Life, remaining rate terms ≤ 36 months | 0.00140 | 0.00055 | 0.00040 |
| Group & Credit Term Life, remaining rate terms > 36 months | 0.00190 | 0.00080 | 0.00055 |

FEGLI/SGLI take a separate **0.0004** factor applied to **amount in force**, not NAR [REG-R142]. **Pricing flexibility
is a categorisation the model must earn, not a product code**: it is the ability to *materially* adjust rates on
in-force contracts through premiums and/or non-guaranteed elements as of the valuation date and within the next **5
policy years**, reflecting typical business practices, tested on a present value basis — `minimum dollar margin needed =
flexibility factor × NAR`, the flexibility factor being the difference in mortality risk provided for in the factors for
contracts with and without pricing flexibility, and the contract passes into the "with" category only if the margin
actually available from repricing over those 5 policy years, **on a present value basis**, is at least that amount
[REG-R128]. Grouping may be at contract or pricing-cohort level; contracts may move between categories at successive
valuation dates; and **an insurer may simply elect the "without" categories if the evaluation is not completed**
[REG-R128][REG-R133]. Defaults where no assessment is performed: direct individual term → Term without; direct
individual permanent → Permanent without; direct group → over-36-months; non-affiliated **ceded** individual → With
Pricing Flexibility; non-affiliated ceded group → 36-months-and-under; affiliated reinsurance follows the direct
categorisation [REG-R133]. Product examples in the instructions: *with* — participating whole life, UL **without**
secondary guarantees, annually repriceable YRT; *term without* — level term with guaranteed level premiums; *permanent
without* — **ULSG and non-participating whole life**, also the **default bucket with the highest factors** [REG-R128]. A
model must therefore be able to run a **repricing scenario**, not merely a base scenario.

**C-2 longevity** is reserve-based: **0.0171 / 0.0108 / 0.0095 / 0.0089** on the first $250 million, next $250 million,
next $500 million and over $1,000 million of life-contingent annuity reserves [REG-R128]. In scope: payout annuities in
pay status, **deferred income annuities that will enter pay status**, structured settlements with any life-contingent
benefit, group annuities including pension risk transfer, and **variable immediate** annuity reserves under VM-21 — the
**entire** reserve of an in-scope contract, including the period-certain portion of a certain-and-life annuity. Out of
scope: non-life-contingent annuities; deferred annuities with a right but no obligation to annuitize; a certain-and-life
annuity reduced to certain payments only after the annuitant's death; and **variable deferred annuity reserves under
VM-21, including contracts whose account value has reached zero but a lifetime benefit remains payable** [REG-R128].

```
Total C-2 pre-tax = TotalHealthClaimReserves + PremiumStabilizationCredit
  + greatest of [ GF × (IndivLifeC2 + GroupLifeC2),  GF × LongevityC2,
                  sqrt( (IndivLifeC2 + GroupLifeC2)² + LongevityC2² + 2·ρ·(IndivLifeC2 + GroupLifeC2)·LongevityC2 ) ]
```

with **guardrail factor GF = 0** and **correlation ρ = −0.25** as stated on LR025-A, so the "greatest of" collapses to
the square-root term in every non-degenerate case — the guardrail is present but switched off and the −25%
mortality/longevity diversification credit applies in full [REG-R128][REG-R134]. Group life and health premium
stabilization reserves give a **50% credit** against C-2, limited to the RBC otherwise calculated [REG-R128].

**C-3a: withdrawal-provision bucketing.** The operative table follows from the drivers just described. Factors were
built assuming well-matched durations and then loaded 50% for less well-matched portfolios [REG-R128]. The second figure
applies where the company submits an **unqualified actuarial opinion based on asset adequacy testing** (or one qualified
solely because of AG 48 direction) — a **one-third reduction** [REG-R128]:

| Risk category | Contents | Factor (pre-tax) |
|---|---|---|
| Low | annuity reserve **with fair value adjustment** (excluding unitized separate accounts); annuity reserve **not withdrawable** (excluding structured settlements); GIC reserve within 1 year of maturity; single premium life and life insurance reserves | 0.0095 → 0.0063 |
| Medium | annuity reserve at **book value less a surrender charge of 5% or more**; Exhibit 7 reserves not included elsewhere; **structured settlements**; additional actuarial reserves from asset/liability analysis; supplementary contracts without life contingencies and dividend accumulations | 0.0190 → 0.0127 |
| High | annuity reserve at **book value without adjustment** (minimal or no charge); debt with GIC-like characteristics | 0.0380 → 0.0253 |

The low-risk derivation is published: an assumed asset/liability duration mismatch of **0.125** with a possible **4%
one-year interest rate swing** gives **0.0063**, loaded 50% for less well-matched portfolios to **0.0095**.
**Equity-indexed products take the same factors as their non-indexed counterparts, based on guaranteed values ignoring
those related to the index, and are excluded from C-3 cash flow testing.** Callable/pre-payable assets add an after-tax
charge of **50% of the excess of BACV over current call price**, asset by asset, zero for assets used in C-3 cash flow
testing or Phase II. All [REG-R128]. **When cash flow testing is compelled — LR049**, either test forces it [REG-R128]:

```
test 1 (significance): C-3a% = (factor-based C-3a on single premium and annuity reserves, excluding equity-indexed,
        + C-3a on all other reserves) ÷ (C-0 + C-1cs + C-1o + C-2 + both C-3a pieces + C-3b + C-3c + C-4a + C-4b)
        REQUIRED if C-3a% exceeds 40%
test 2 (stress): recompute the covariance formula substituting adjusted C-3a
        = [ line(17)×0.79 + line(16)×(1 − t) ] + [ line(17) × 6.5 × (1 − t) ] + all-other C-3a
        REQUIRED if Total Adjusted Capital ÷ that stressed RBC-after-covariance is less than 100% and non-zero
```

**The whole formula must therefore be computable before you know whether cash flow testing is required.** Companies with
less than **$100 million** in admitted assets need not complete the line unless a test triggers, and once the cash flow
method is elected it must be continued unless the domiciliary regulator approves reverting [REG-R128].

**The C-3 Phase I procedure** [REG-R128][REG-R135]. *Model:* the year-end asset adequacy cash flow testing model, or a
consistent one, with the **same assumptions and "as-of" date**, but different interest scenarios and a different
measurement. *Scope*, "Certain Annuities": deferred and immediate annuities, structured settlements, guaranteed separate
accounts (excluding guaranteed indexed separate accounts on a Class II strategy), GICs including synthetic GICs and
funding agreements, plus single premium life; **variable annuities are excluded, including guaranteed fixed options
within them** (they go through Phase II). *Initial asset basis:* **initial assets = reserves** with no surplus assets;
**AVR-related assets excluded** and future AVR contributions not modelled, though *expected* credit losses stay in the
cash flows; **IMR assets are used**; profits retained, no stockholder dividends withdrawn, policyholder dividends and
credited rates modelled realistically. *Scenarios:* the standard **50-scenario** set or the more conservative
**12-scenario** set, different sets permitted for different products, horizon until surplus contributions on a closed
block are immaterial, rates held constant at the year-30 level beyond the generator's 30 years. *Per-scenario
statistic:* capture `S(t) = statutory assets − statutory liabilities` at every calendar year end; the scenario's C-3
measure is the **most negative of the series of present values S(t)·pv(t)**, discounting at **105% of the after-tax
one-year U.S. Treasury rate** for that scenario. *Ranking and weighting:* rank descending, rank 1 = worst; for the
50-scenario set apply weights to ranks **17, 16, …, 5** of **0.02, 0.04, 0.06, 0.08, 0.10, 0.12, 0.16, 0.12, 0.10, 0.08,
0.06, 0.04, 0.02** (peaking at rank 11) and sum the products; for the 12-scenario set take the **average of ranks 2 and
3, floored at half the worst**. *Assembly:* total C-3 = cash-flow-tested annuities and single premium life +
equity-indexed on factors + all other on factors + the callable/pre-payable add-on, **but not less than half the C-3
component computed entirely on factors** (the 1999 design collared the result between half and double; only the half
floor survives [REG-R135]). *Certification:* an appointed actuary **C-3 Assumption Statement** accompanies the filing,
key assumptions must be stress tested (e.g. **lapses increased by 50%**), and if the actual result exceeds the year-end
estimate by more than **5%**, or triggers regulatory action, a revised filing is due by **June 15**.

**C-3 Phase II for variable annuities.** Scope is "all policies and contracts that have been valued following the
requirements of AG-43 or VM-21". Seven steps: (1) determine **CTE 98**, "the numerical average of the 2% largest values
of the Scenario Reserves, as defined by Section 4 of VM-21", using the same process and methods as the reserve; (2)
convert to a C-3 RBC amount by the formula below, floored at $0; (3) for **Alternative Methodology** contracts compute
under Appendix 2 of the instructions; (4) C-3 RBC = (2) + (3) ≥ 0, and **Total Asset Requirement = the VM-21 reserve
before any phase-in plus the C-3 RBC amount**; (5) phase in if a VM-21 §2.B reserve phase-in was elected; (6) smooth if
elected — ratio = 0.4 × prior-year (C-3 RBC ÷ reserve) + 0.6 × current-year ratio, applied to the current-year aggregate
reserve with voluntary reserves stripped from both years; (7) divide by (1 − enacted maximum federal corporate income
tax rate) to reach a pre-tax amount and **split it into an interest rate component (→ C-3a, line 35) and a market risk
component (→ C-3c, line 37)**, neither negative. All [REG-R128]. Two permitted tax methods. **Macro Tax Adjustment** —
modelled cash flows ignore federal income tax so each Scenario Reserve is numerically identical to the VM-21 reserve
calculation's, and tax enters through the formula, **reproduced exactly as printed**:

> `25% x ((CTE (98) + Additional Standard Projection Amount – Statutory Reserve) x (1 – Federal Income Tax Rate) – (Statutory Reserve – Tax Reserve) x Federal Income Tax Rate`

**The parentheses in the published text are unbalanced, so the intended bracketing of the second term is [unverified]**
and is reproduced rather than silently resolved. The instruction's own gloss — that "the difference between statutory
reserves and tax reserves multiplied by the Federal Income Tax Rate … may not exceed the portion of the company's
non-admitted deferred tax assets attributable to the same portfolio of contracts to which VM-21 is applied" — supports
reading it as a separate deduction with its own cap, but that is a reading, not the text [REG-R128]. Confirm against the
RBC software or a current Academy practice note before coding. **Specific Tax Recognition** — tax is reflected inside
the projection of Accumulated Deficiencies (VM-21 §4.A) with after-tax discounting, and `25% x (CTEAT (98) + Additional
Standard Projection Amount – Statutory Reserve)`, with a **tax adjustment** where actual tax reserves exceed projected
tax reserves at the projection start: increase CTEAT(98) by *corporate tax rate × f × (actual − projected tax reserves
at t = 0)*, where **f = 1 − the average, across the CTE(98) scenarios, of the ratio of contracts in force at the
scenario's greatest-present-value duration to contracts in force at the start**; under the Alternative Method **f ≈
0.5** [REG-R128]. Switching from STR back to MTA requires prominent disclosure, and under STR the company must still
disclose the TAR and C-3 RBC that MTA would have produced.

**The covariance adjustment and its rationale.** The instructions state the assumption before the arithmetic: "the
combined effect of the C-1o, C-1cs, C-2 and C-3 and a portion of the C-4 risks are not equal to their sum but are equal
to the square root calculation described below. It is statistically assumed that the C-1o risk and a portion of the C-3
risk are correlated, while the C-1cs risk, the C-2 risk, the balance of the C-3 risk and a portion of the C-4 risk are
independent of both" [REG-R128].

**The covariance combination, exactly as published** [REG-R128, LR031 line (69)]:

```
RBC after Covariance Before Operational Risk
  = C-0 + C-4a + Square Root of [ (C-1o + C-3a)² + (C-1cs + C-3c)² + (C-2)² + (C-3b)² + (C-4b)² ]

Gross Basic Operational Risk (70) = 0.03 × line (69)
Net Basic Operational Risk (72)   = (70) − ( C-4a post-tax + C-4a of U.S. life insurance subsidiaries ), floored at 0
AG 48 add-on (73)                 = Primary Security shortfall for all AG 48 cessions × 2
Total RBC After Covariance (74)   = (69) + (72) + (73)
Authorized Control Level RBC (75) = 0.50 × (74) ;   Mandatory Control Level RBC = 0.70 × Authorized Control Level RBC
```

The grouping is confirmed three ways inside that document — the blank line with superscripts intact, the narrative
spelled out in words, and LR049 line (20). **C-3a is added to C-1o inside one squared term; C-3c is added to C-1cs (the
Phase II instruction says the line (37) amount "is to be combined with the C-1cs component for covariance purposes");
C-2, C-3b and C-4b are standalone squared terms; C-0 and C-4a sit outside the radical.** All terms entering line (69)
are post-tax, each pre-tax component having been netted against its tax effect on LR030; a parallel pre-tax
tax-sensitivity test runs the same formula at line (76). The AG 48 doubling followed by the halving produces a
**dollar-for-dollar** increase in Authorized Control Level for the shortfall, and applies even where a state has waived
AG 48 compliance [REG-R128][REG-R11][REG-R12]. A **1% charge on admitted adjusted gross deferred tax assets** (SSAP No.
101 ¶¶11.a and 11.b) is applied **outside** the covariance adjustment, reduced to **0.5%** for the ¶11.a component where
the insurer filed its own federal return or was in a consolidated return whose common parent is an insurance company
[REG-R128]. A proposal to replace the square-root form with an explicit five-category correlation matrix exists but **is
not in force** as of the 2024 instructions [REG-R137][REG-R128], as does a C-3 alignment project that would unify Phase
I and Phase II and bring fixed indexed annuities into scope [REG-R138].

**Total Adjusted Capital and the role of the AVR.** TAC is statutory capital and surplus plus **the AVR**, plus half of
apportioned and unapportioned dividend liabilities, plus prorated life-subsidiary AVR and dividend liability, less
specified items, plus limited credit for capital notes, less the XXX/AXXX reinsurance shortfall [REG-R128]. The reason
the AVR counts as capital is stated in the instructions: "In determining the C-1 risk factors, availability of the AVR
and voluntary investment reserves to absorb specific losses was not assumed. Therefore, the AVR is counted as capital
for the purposes of the formula although it represents a liability and is not usable against general contingencies"
[REG-R128]. **The portion that counts is limited to the amount not utilized in asset adequacy testing in support of the
actuarial opinion for reserves** — a direct coupling from the appointed actuary's work into the numerator of the RBC
ratio, requiring the asset adequacy model to *report how much AVR it consumed* [REG-R128][REG-R29]. The headline ratio
is **Total Adjusted Capital ÷ Authorized Control Level RBC**.

**The LR033 build** [REG-R128]: (1) Capital and Surplus (Page 3, Col 1, Line 38) × 1.000; (2) **Asset Valuation
Reserve** (Line 24.01) × 1.000; (3) Dividends Apportioned for Payment (Line 6.1) × 0.500; (4) Dividends Not Yet
Apportioned (Line 6.2) × 0.500; (5) Hedging Fair Value Adjustment × −1.000; (6) life subsidiary AVR prorated × 1.000;
(7) life subsidiary dividend liability prorated × 0.500; (8) carrying value of non-admitted insurance affiliates ×
1.000; (9) less non-tabular discount and/or Alien Insurance Subsidiaries–Other; (10) subtotal before capital notes;
(11.4) plus the limited credit for capital notes; (12) less the XXX/AXXX Reinsurance RBC Shortfall; (13) **TOTAL
ADJUSTED CAPITAL**.

**The trend test.** It bites only in the band above Company Action Level but below the **3.0× Authorized Control Level**
safe harbour, where the mechanical Level of Action would otherwise read "None" [REG-R128][REG-R127]. The life safe
harbour was **2.5× before a 2011 amendment raised it to 3.0×** [REG-R126]. The arithmetic: margin in a year = TAC − ACL
RBC; the one-year decrease is prior-year margin − current-year margin floored at zero; the three-year average decrease
is **⅓ × (third-prior-year margin − current-year margin)** (the exact wording of the intermediate line is
**[unverified]** — it did not survive text extraction); **Marginal Difference = the greater of the two**; and **if TAC −
Marginal Difference is less than 1.9 × ACL RBC the company triggers Company Action Level** [REG-R128]. Change control
runs through the Capital Adequacy (E) Task Force and the Life RBC (E) Working Group on a fixed calendar — structural
blank changes by May 15, non-structural by June 30, instructions published around November 1
[REG-R140][REG-R141][REG-R139].

---

## What this means for a liability cash flow model

Consolidating, statutory reporting and capital need the following from the projection.

1. **A statutory income and surplus recursion, not just cash flows** — premium gross when due, acquisition expense in
   the issue period with no DAC stream, benefits, change in aggregate reserves, change in loading, separate account
   transfers, IMR amortisation, AVR movement direct to surplus, tax [REG-R74][REG-R75][REG-R79][REG-R90].
2. **Two parallel reserve bases** — formulaic CRVM and CARVM for pre-operative-date and *All Other* business, and VM-20
   / VM-21 / VM-22 for principle-based business, with the Exhibit 5 net-premium-reserve split and the VM-22
   Jumbo/Non-Jumbo band split [REG-R1][REG-R3][REG-R35][REG-R36][REG-R89].
3. **Valuation-basis movement in parallel with experience movement** — tabular net premiums, tabular interest, tabular
   cost and reserves released are reserve-basis quantities [REG-R90].
4. **An immutable per-contract classification flag** driving premium-income versus direct-to-reserve treatment and
   Exhibit 5 versus Exhibit 7 [REG-R78][REG-R80][REG-R89].
5. **A gross-and-ceded pair everywhere**, never netted, plus modco and funds-withheld balances [REG-R89][REG-R92].
6. **An asset projection with disposal-level detail**, without which neither IMR nor AVR can be produced [REG-R89].
7. **Multi-scenario cash flow testing** with a present value of ending surplus, terminal-value handling, interim surplus
   by year, and starting assets capped at the statement value of the reserves tested [REG-R29][REG-R100][REG-R111].
8. **Annual-statement-shaped output.** The RBC formula reads **statement values**, not model quantities, so projecting a
   capital ratio forward requires projecting an annual statement — an inference from the blank line sources rather than
   a published requirement, recorded as **[unverified]** in that form [REG-R128].

**The couplings are what make this harder than a one-way hand-off.**

- **Admitted negative IMR feeds back into the reserve models.** INT 23-01 ¶9.e requires it to be captured in the PBR
  calculation or in asset adequacy testing under VM-20 §7.D.7 and VM-30 §3.B.5, with a reconciliation to the IMR
  reflected there [REG-R87], while VM-30 §3.B.5 independently mandates a sign-aware IMR allocation in any asset adequacy
  analysis [REG-R100]. An accounting admittance decision therefore changes a reserve.
- **VM-21 reserves and variable annuity capital come out of one stochastic run.** The same Scenario Reserves are
  averaged at **CTE 70** for the reserve and **CTE 98** for capital; the Additional Standard Projection Amount is
  computed once and used in both; grouping, sampling and simplification "should be identical to those used in
  calculating the company's statutory reserves following VM-21" [REG-R128][REG-R35]. **One stochastic run, two order
  statistics** — a model computing reserve and capital in separate engines will not reconcile.
- **The AVR sits on both sides** — a liability that counts as capital, but only to the extent not consumed by the asset
  adequacy analysis supporting the opinion, so the capital numerator depends on a cash-flow-testing model output; the
  operative rule is at "Risk-based capital", Total Adjusted Capital [REG-R128][REG-R29].
- **One cash flow engine can serve several regimes, and the Valuation Manual says so.** The VM-20 stochastic exclusion
  ratio test may be built from "the gross premium reserve developed from the cash flows from the company's asset
  adequacy analysis models" [REG-R3]; C-3 Phase I uses the year-end asset adequacy model with different scenarios and a
  different measurement [REG-R128][REG-R135]; AG 55 §6.G accepts a pre-reinsurance PBR reserve in lieu of separate cash
  flow testing [REG-R103]; and one direct-iteration routine serves the VM-20 deterministic reserve, the VM-21 reserve
  and the ending-surplus problem [REG-R111]. ASOP 22 §3.1.5 sets the conditions for reuse — differences in starting
  assets, margins, sensitivities, interim shortfalls, required aggregation, surplus distribution and **taxes**, the last
  mattering because VM-20 and VM-21 exclude federal income tax [REG-R3][REG-R111] while asset adequacy analysis includes
  it [REG-R29][REG-R111]. (VM-21's exclusion is the *elective* Macro Tax Adjustment position rather than an absolute
  rule — under Specific Tax Recognition tax is projected inside the accumulated deficiencies [REG-R35][REG-R128].)

**Layering**, four layers with one direction of dependency: (1) product models in `us/products/` emit cash flows and
policy state; (2) a **valuation layer** turns state into reserves — CRVM, CARVM, NPR, DR, SR, VM-21/VM-22; (3) a
**statutory ledger** turns cash flows plus reserve movements into Exhibits 5/6/7, the Analysis of Operations, the
Analysis of Increase in Reserves, IMR, AVR and surplus; (4) a **capital layer** reads the ledger's statement values.
Layer 4 reads statement values, not model values [REG-R128] — do not let it reach back into layer 1.

| Once per valuation | Once per scenario | Per projection path |
|---|---|---|
| CRVM/CARVM/NPR — prescribed assumptions, no scenario dependence [REG-R1][REG-R3] | SR scenario reserves [REG-R3 §5] | AVR and IMR balances |
| DR — a single prescribed scenario 12 [REG-R3 §4] | VM-21 Scenario Reserves: computed **once**, read **twice** at CTE 70 and CTE 98 [REG-R128] | statutory income and surplus |
| Additional Standard Projection Amount [REG-R128] | C-3 Phase I S(t) series [REG-R128] | projected annual statement for a forward RBC ratio |
| RBC factors, size bands, action-level multipliers | — | tax reserves and DTA scheduling |

**Practical ordering of a statutory reporting run.** (1) In-force extract and cash flow projection. (2) Formulaic
reserves: CRVM, CARVM, deficiency, NPR. (3) Exclusion tests — SERT/DET and the VM-22 analogues — recording *how* each
was passed, because that drives VM-G scope [REG-R109]. (4) DR and/or SR where required, per reserving category and
aggregation subgroup. (5) Minimum reserve per category, allocated to policy in proportion to policy minimum NPR [REG-R3
§2.C]. (6) VM-21/VM-22 stochastic run, retaining the Scenario Reserve vector. (7) Exhibit 5/6/7 assembly with
valuation-standard and year-of-issue keys, VM-20 business split NPR versus excess, VM-22 business split Jumbo/Non-Jumbo
× 50bp bands [REG-R89]. (8) Asset adequacy analysis: starting assets whose statement value is **no greater than** the
statement value of the reserves tested [REG-R29 §3.1][REG-R112], sign-aware IMR allocation and disclosed AVR allocation
[REG-R100], producing any **additional reserve** — then **iterate**, because the additional reserve changes the reserves
being tested and therefore the permitted starting assets. (9) IMR and AVR balances and the negative-IMR admittance test.
(10) Income statement, Analysis of Increase in Reserves, surplus roll-forward. (11) Tax: tax reserves, temporary
differences, DTA admittance. (12) RBC — which needs the AVR consumed in AAT and the opinion-qualification flag from step
8, and whose LR049 test needs the entire formula before you know whether C-3 cash flow testing was required. (13) Trend
test and level of action. **Two circularities to break explicitly:** the DTA admittance percentage depends on the
**ExDTA ACL RBC ratio**, computed *without* net deferred tax assets precisely so the loop terminates [REG-R97 ¶11]; and
the AAT additional reserve depends on the reserve it is added to, so iterate to a fixed point with a stated tolerance
**[std]**.

---

## Worked example — one policy, carried through

Worked Example 1's endowment, on an expected (survivorship-weighted) basis per policy issued. Additional **[std]**
assumptions: first-year commission **60% of premium**; maintenance expense **25** at BOY; earned rate **4.0%**; tax rate
**21%**; net surrender value **0**; tax reserve per IRC §807 = max(NSV, 92.81% × statutory) capped at statutory
[REG-R16].

| Year-1 item | Value | Year-1 item | Value |
|---|---|---|---|
| Premium (BOY) | 320.000000 | Closing statutory reserve = 306.544172 × 0.99 | 303.478731 |
| Acquisition expense 0.60 × 320, **expensed as incurred** [REG-R75 ¶2] | 192.000000 | Increase in aggregate reserves [REG-R90 Line 19] | 303.478731 |
| Maintenance expense (BOY) **[std]** | 25.000000 | **Pre-tax gain** = 320 + 4.12 − 10 − 217 − 303.478731 | **−206.358731** |
| Invested assets after BOY flows = 320 − 217 | 103.000000 | Tax reserve = 0.9281 × 303.478731 [REG-R16] | 281.658610 |
| Net investment income = 4.0% × 103 **[std]** | 4.120000 | Taxable income = 320 + 4.12 − 10 − 217 − 281.658610 | −184.538610 |
| Expected death benefits = 1,000 × 0.01 | 10.000000 | FIT at 21% (a benefit, assumed realizable **[std]**) | −38.753108 |
| | | **After-tax gain = end-of-year-1 surplus** | **−167.605623** |

Reconciliation, which must close exactly: assets = 0 + 320 − 217 − 10 + 4.12 + 38.753108 = 135.873108; surplus = assets
− reserve = 135.873108 − 303.478731 = **−167.605623** ✓. RBC at the same date: NAR = face in force − reserve = (0.99 ×
1,000) − 303.478731 = **686.521269**, and a non-participating endowment falls in **Permanent without Pricing
Flexibility**, band 1 [REG-R128].

| RBC item | Calculation | Pre-tax | Tax factor **[std]** | Post-tax |
|---|---|---|---|---|
| C-2 mortality | 686.521269 × 0.00400 | 2.746085 | × 0.79 | 2.169407 |
| C-3a (low risk, life reserves, unqualified AAT opinion) | 303.478731 × 0.0063 | 1.911916 | × 0.79 | 1.510414 |
| C-4a | 320 × 0.0253 | 8.096000 | × 0.79 | 6.395840 |
| C-1o (assets 135.873108 at designation 1.A, size factor 1.00 **[std]**) | 135.873108 × 0.00158 | 0.214680 | × 0.79 | 0.169597 |

Covariance, with C-0 = C-1cs = C-3b = C-3c = C-4b = 0: `0 + 6.395840 + sqrt((0.169597 + 1.510414)² + 0² + 2.169407² + 0² +
0²) = 6.395840 + sqrt(2.822435 + 4.706328) = 6.395840 + 2.743859 = 9.139699`. Operational risk = 0.03 × 9.139699 =
0.274191, less C-4a post-tax 6.395840 → floored at **0**. Total RBC after covariance = 9.139699, so **Authorized Control
Level RBC = 0.50 × 9.139699 = 4.569850** [REG-R128]. Two honesty flags: the **0.79 tax factor is [std]** — the
per-component tax factors live on LR030 and were not transcribed by the research [REG-R128] — and the size factor of
1.00 is a toy, since a blank issuer count is charged **2.40** [REG-R128].

---

## Validation and reconciliation checks

1. **CRVM construction.** `APV₀(B) − k*·APV₀(G) = −E` exactly, so the reserve at issue floors to zero and the expense
   allowance equals E [REG-R1 §5.A].
2. **Reserve roll-forward closure.** Analysis of Increase in Reserves line 15 = line 8 − line 14, and that closing
   reserve equals an independent Mode-V valuation at t [REG-R90]; Exhibit 5A's life contract subtotal must agree with
   the "increase in reserve on account of change in valuation basis" line [REG-R89].
3. **Surplus reconciliation.** `S(t) = A(t) − L(t)` **and** `S(t) − S(t−1)` = after-tax gain plus the direct-to-surplus
   items — both, not either.
4. **Gross minus ceded.** `V_net = V_gr − V_ced`, the ceded credit on the **same mortality, interest and valuation
   method** reflecting the actual mode of reinsurance, with **no deduction for modified coinsurance** [REG-R89][REG-R92
   ¶37]. The ceded column must be produced, not inferred by subtraction.
5. **CTE monotonicity.** From one Scenario Reserve vector, `CTE 70 ≤ CTE 98 ≤ max(ScenRes)`; a violation means reserve
   and capital did not come from the same run [REG-R128][REG-R35].
6. **VM-20 floors.** Minimum reserve ≥ Σ NPR in every category by construction; each NPR ≥ its §3.D floors; the total is
   the **sum** of the three category results, never a company-level maximum [REG-R3].
7. **TAC composition.** TAC ties to LR033 line by line; the AVR included is net of the amount consumed in asset adequacy
   testing; `ACL = 0.50 × total RBC after covariance` and `MCL = 0.70 × ACL` [REG-R128].
8. **Statement ties.** Exhibit 5 total → Liabilities page Line 1; IMR → Page 3 Line 9.4; AVR → Page 3 Line 24.01; change
   in non-admitted disallowed IMR → Page 4 Line 41 [REG-R89][REG-R87]. These are **2025** blank references and should be
   re-verified against the 2026 blank before being hard-coded [REG-R89][REG-R90].
9. **IMR grid.** The 30-year amortisation grid plus the "and later" row must sum to the balance before current-year
   amortisation [REG-R90].
10. **Classification immutability.** The life-versus-deposit-type flag is set at inception and **cannot change**
    [REG-R78 ¶5]; assert it never does, and assert the Exhibit 5 footnote (a) asymmetry — a contract life-contingent at
    issue stays in Exhibit 5 even after the mortality risk disappears [REG-R89].
11. **AAT starting assets.** Statement value of the chosen assets ≤ statement value of the reserves and other
    liabilities being tested [REG-R29 §3.1][REG-R112].

---

## Product applicability

`x` = the item directly binds the product; `(x)` = binds conditionally, partially, or only through one component; `—` =
expressly excluded by the cited source; `?` = treatment genuinely unsettled in the documents retrieved; blank = not
indicated by the sources read. Derived from the product-applicability sections of the three research files. Columns are
`us/products/` names abbreviated: TERM = term-life, WL = whole-life, UL = universal-life, IUL = indexed-ul, VUL =
variable-ul, GUL = guaranteed-ul, FDA = fixed-deferred-annuity, FIA = fixed-indexed-annuity, VA = variable-annuity, RILA
= registered-index-linked-annuity, SPIA = immediate-annuity, DIA = deferred-income-annuity.

| Statutory / capital item | TERM | WL | UL | IUL | VUL | GUL | FDA | FIA | VA | RILA | SPIA | DIA |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Acquisition costs expensed, no DAC — SSAP No. 71 [REG-R75][REG-R76] | x | x | x | x | x | x | x | x | x | x | x | x |
| Life-contract classification — SSAP Nos. 50/51 [REG-R78][REG-R79] | x | x | x | x | x | x | x | x | x | x | (x) | (x) |
| Deposit-type classification — SSAP No. 52 [REG-R80] | | | | | | | (x) | (x) | (x) | (x) | x | x |
| Exhibit 5 [REG-R89][REG-R90] | x | x | x | x | x | x | x | x | x | x | (x) | (x) |
| Exhibit 7 [REG-R89] | | | | | | | (x) | (x) | (x) | (x) | x | x |
| Analysis of Increase in Reserves — tabular quantities [REG-R90] | x | x | x | x | x | x | x | x | x | x | x | x |
| Exhibit of Life Insurance — face amount in force [REG-R89] | x | x | x | x | x | x | | | | | | |
| A&H rider reserves — SSAP No. 54, base-contract line [REG-R82][REG-R89] | (x) | (x) | (x) | (x) | (x) | (x) | | | | | | |
| Separate accounts — SSAP No. 56 [REG-R83][REG-R84] | | | | | x | | | | x | x | | |
| AVR [REG-R85][REG-R86][REG-R89] | x | x | x | x | (x) | x | x | x | (x) | x | x | x |
| IMR, incl. the MVA liability leg [REG-R85][REG-R86][REG-R89] | x | x | x | x | (x) | x | x | x | (x) | x | x | x |
| Negative-IMR admittance — INT 23-01 [REG-R87] | x | x | x | x | (x) | x | x | x | (x) | x | x | x |
| Derivatives — SSAP No. 86 [REG-R96] | | (x) | (x) | x | (x) | (x) | (x) | x | x | x | (x) | (x) |
| Reinsurance credit — SSAP No. 61, Models #785/#786 [REG-R92][REG-R94][REG-R95] | x | x | x | x | x | x | x | x | x | x | x | x |
| Deferred tax admittance — SSAP No. 101 [REG-R97][REG-R98] | x | x | x | x | x | x | x | x | x | x | x | x |
| Formulaic CRVM — SVL §5 / A-820 ¶11 via VM-A/VM-C [REG-R1][REG-R153][REG-R110][REG-R41] | x | x | x | x | x | x | | | | | (x) | (x) |
| — of which the **A-830** segmented/unitary CRVM [REG-R154] | x | | | | — | x | | | | | | |
| — of which the **A-585** GMP/GMF CRVM adaptation [REG-R155] | | | x | x | | | | | | | | |
| Formulaic CARVM — SVL §5a / A-820 ¶15 [REG-R1][REG-R153] | | | | | | | x | x | x | x | x | x |
| — **AG 33** elective-benefit interpretation [REG-R151] | | | | | | | x | x | x | x | (x) | x |
| — **AG 35** equity-indexed CARVM [REG-R152] | | | | | | | — | x | | ? | | |
| VM-20 NPR / DR / SR [REG-R3] | x | x | x | x | x | x | | | | | | |
| VM-20 deterministic exclusion test [REG-R3] | — | x | x | x | x | (x) | | | | | | |
| VM-21 / AG 43 population [REG-R35][REG-R38] | | | | | | | | | x | ? | (x) | |
| VM-22 non-variable annuity PBR [REG-R36] | | | | | | | x | x | | ? | x | x |
| VM-V §1 income annuity valuation rates [REG-R37] | | | | | | | (x) | (x) | (x) | | x | x |
| VM-30 opinion and asset adequacy analysis [REG-R100][REG-R29] | x | x | x | x | x | x | x | x | x | x | x | x |
| VM-31 report / VM-G governance [REG-R108][REG-R109] | x | x | x | x | x | x | x | x | x | x | x | x |
| AG 53 complex-asset discipline [REG-R105][REG-R106] | (x) | (x) | (x) | (x) | (x) | (x) | x | x | (x) | (x) | x | x |
| AG 55 reinsurance asset adequacy testing [REG-R103][REG-R104] | (x) | (x) | (x) | (x) | (x) | (x) | x | x | (x) | (x) | x | x |
| RBC action levels and trend test — Model #312 [REG-R125][REG-R126] | x | x | x | x | x | x | x | x | x | x | x | x |
| C-2 mortality, NAR-based [REG-R128][REG-R133] | x | x | x | x | x | x | | | | | | |
| C-2 longevity, life-contingent annuity reserves [REG-R128] | | | | | | | (x) | (x) | (x) | | x | x |
| C-3a factor charge by withdrawal provision [REG-R128] | x | x | x | x | (x) | x | x | x | (x) | (x) | x | x |
| C-3 Phase I cash flow testing [REG-R128][REG-R135] | | | | | | | x | — | — | ? | x | x |
| C-3 Phase II, CTE 98 [REG-R128][REG-R35] | | | | | | | | | x | ? | (x) | |
| C-1cs / separate account capital interactions [REG-R128][REG-R136] | | | | | x | | | | x | (x) | | |
| C-4a business risk [REG-R128] | x | x | x | x | x | x | x | x | x | x | x | x |
| AG 48 shortfall doubled into ACL [REG-R128][REG-R11][REG-R12] | x | | | | | x | | | | | | |
| TAC: AVR included, limited by asset adequacy usage [REG-R128][REG-R29] | x | x | x | x | x | x | x | x | x | x | x | x |

**Notes on the matrix.** A **life-contingent** SPIA or DIA is a life contract in Exhibit 5 and stays there after the
annuitant's death while certain payments continue, while a **period-certain-only** contract is deposit-type in Exhibit 7
[REG-R80][REG-R89]; the `(x)` on the deferred columns records settlement options and dividend accumulations spawning
deposit balances. **VUL and VA carry `(x)` on AVR and IMR** because a fair-value separate account requires neither
(except AVR on seed money) while the general account backing the guarantees requires both, whereas **RILA is `x` because
SSAP No. 56 ¶18.b makes a book-value separate account available to it** [REG-R83][REG-R84]. **VM-20 rows are blank for
annuities by construction** — VM-20 is CRVM for individual *life*; within it the deterministic exclusion test is
**barred entirely for term**, ULSG is **deemed to fail** it unless its secondary guarantee is non-material, and variable
life and ULSG may not use the stochastic exclusion certification method [REG-R3]; formulaic CRVM carries `(x)` for SPIA
and DIA because VM-V §1 states its rates are the maximum interest assumption for CARVM "and for some contracts, CRVM"
[REG-R37]. **AG 53 and AG 55 are `(x)` across the life products** because their triggers are **company-level and
treaty-level, not product-level** [REG-R105][REG-R103]. **C-2 mortality marks do not follow product codes**: level term
with guaranteed premiums is "term without pricing flexibility", participating whole life and UL without secondary
guarantees are "with", and **non-participating whole life and ULSG sit in the highest-factor "permanent without"
bucket** [REG-R128][REG-R133] — modelling C-2 off a product code alone will misclassify. The `—` marks on C-3 Phase I
are **express exclusions**: equity-indexed products take factors on guaranteed values ignoring the index, and variable
annuities go through Phase II [REG-R128]. The **life columns on that row are blank rather than `x`** because C-3 Phase I
scope is "Certain Annuities" **plus single premium life**, so it reaches a life product only in a single-premium design
[REG-R128][REG-R135]; the scope statement is set out at "Risk-based capital" above.

**Notes on the four formulaic rows, which are new.** They split what used to be two rows, because "CRVM" and "CARVM"
each name more than one instrument. **A-830** carries `—` for VUL because ¶3.a.iii and ¶3.a.iv exclude variable life and
variable universal life **outright**, and blanks for whole life and ordinary UL because nothing in ¶3.b routes a
level-premium, level-benefit non-UL policy or a UL policy without a secondary guarantee to any calculation paragraph —
such a policy is inside the ¶3 scope sentence and inside ¶2's declaration but has no printed construction, which is an
observation about the print and **not** a licence to infer an outcome [REG-R154]. **A-585** carries `x` only for UL and
IUL; the tempting `(x)` for ULSG is withheld because A-830 ¶32.b floors the ULSG reserve by "the minimum reserves
required by **other appendices governing universal life plans**" **without naming the item**, and that cross-reference
must not be resolved to A-585 on the A-830 text [REG-R154 ¶32]. **AG 33** carries `(x)` rather than `x` for SPIA for the
reason set out in the basis table above — a no-option life-only SPIA is outside its applicability sentence, and any
elective option puts it inside [REG-R151]. **AG 35** carries `—` for a book-value MYGA, `?` for RILA (retrieved, and it
neither includes nor excludes the design), and blanks for the payout products only because the library's representative
SPIA and DIA are not index-linked — **AG 35 does in fact reach equity indexed *immediate* annuities**, its Background
describing designs with "a minimum guaranteed annuitization rate and an opportunity to receive larger periodic payments
based on the growth … in an equity index", and its Attachment 4 certification covering "all equity indexed annuity
products" where Attachment 3 is confined to deferred ones [REG-R152]. An index-linked payout design would take `x`.

**One date the library must stop repeating without qualification.** AG 33's printed *Effective Date* block reads: "This
guideline shall be effective on **December 31, 1998**, affecting all contracts issued on or after January 1, 1981",
followed by a grade-in that reached 100% by December 31, 2000 and therefore has **no live effect on any current
valuation** [REG-R151]. The library elsewhere carries "effective December 31, **1995**" under a different title, sourced
from IRS Rev. Rul. 2002-6. Both are facts about their own documents; the extracted AG 33 pages carry **no amendment
history**, so the natural reconciliation — that the guideline was later revised and the manual prints the revised text —
is an **inference this library does not assert**. The issue-date reach of 1 January 1981 is common to both. AG 35, by
contrast, prints **no effective date, adoption date, operative date, transition, phase-in or sunset at all**; its only
temporal language is "regardless of the date of issue", and the `© 1999-2026` footer is a copyright span, not an
adoption date [REG-R152]. A-830 likewise prints **no calendar effective date for itself** — "the effective date of this
appendix" appears eleven times as an unresolved placeholder — and A-585, A-250 and A-255 print none either [REG-R154]
[REG-R155][REG-R156][REG-R157]. **No date may be attributed to any of those five items from these sources.**

**RILA's capital treatment is genuinely unsettled, and the `?` marks say so rather than guessing.** The RBC instructions
read **never mention registered index-linked annuities, ILVA, or index-linked annuities at all** [REG-R128]. Whether a
RILA lands in C-3 Phase II depends on whether the contract is valued under AG 43 / VM-21; otherwise it would take
factor-based C-3, presumably on the equity-indexed convention. **Neither reading is sourced, and the research records
the inference as [unverified]** [REG-R128]. The same silence affects its VM-21 and VM-22 rows. This is a real hole for
one of the twelve products, not an artefact of incomplete reading.

---

## Key sensitivities and model risks

- **Calendar-year-of-issue rate tables.** The valuation interest rate is a step function of issue year with a ±0.5%
  stability rule; one mis-set year silently misvalues an entire cohort [REG-R1 §4b].
- **The CRVM expense allowance cap** is the 19-pay whole life premium at age **x+1**, not x, and binds more often than
  intuition suggests on short endowments and high-premium designs [REG-R1].
- **CARVM path enumeration.** Omitting an elective-benefit path can only understate the reserve, and the interpretive
  guidance is now first-hand: AG 33 requires **blends across benefit types**, not one path per benefit type, and forbids
  experience-based elective incidence altogether [REG-R151]. Three specific traps: the **accumulation fund may exceed
  the cash value**, so a single-account-value model cannot value an annuitization stream; the **valuation rate varies
  within one stream**, by benefit component and, for annuitization, by assumed election date; and the elective
  **cash-value stream is still survivorship-discounted** on the prescribed annuity mortality [REG-R151].
- **The CRVM engine is not one engine.** A term or ULSG block valued on the SVL §5.A routine alone is not computing
  A-830 CRVM (`max(segmented, unitary)`, with a segment-scoped expense allowance), and a universal life block valued
  that way is not computing the A-585 GMP/GMF reserve [REG-R154 ¶2][REG-R155 ¶8]. Both mistakes are silent — they
  produce a number.
- **Generational annuity mortality.** The 2012 IAR and 1994 GAR are functions of *(age, calendar year)*, and A-821 ¶14
  **expressly forbids** the recursive `q(y+1) = q(y)·(1 − G2)` shortcut: every rate is recomputed from the 2012 base and
  rounded to three decimals per 1,000 [REG-R153].
- **Exclusion tests are cliffs.** A 6% SERT ratio drifting to 6.01% turns on the whole SR machinery and, depending on
  the route taken, VM-G Sections 2 and 3 as well [REG-R3][REG-R109].
- **Tail estimation.** CTE 70 and especially CTE 98 are averages of the worst 30% and worst 2%; at small scenario counts
  the CTE 98 estimate rests on a handful of paths [REG-R128][REG-R3].
- **Negative IMR is doubly cliff-edged** — a **300% ACL RBC** gate and a **10%** cap breachable by a surplus decline
  alone — and carries an **automatic nullification on January 1, 2027** as currently written [REG-R87]. Test admittance
  at every reporting date, not once.
- **AVR and IMR factor tables are not in this library.** They are published annually and were deliberately not
  transcribed [REG-R89]; a model that hard-codes remembered values will be wrong.
- **C-2 misclassification.** Modelling pricing flexibility off a product code misclassifies, and the default where the
  assessment is not performed is the **highest-factor** bucket [REG-R128][REG-R133].
- **Published-formula ambiguity.** The C-3 Phase II Macro Tax Adjustment formula has unbalanced parentheses in the
  source; the bracketing is **[unverified]** and must be confirmed before coding [REG-R128].
- **Double-counted default costs.** C-1 factors were parameterised at expected loss plus ½ standard deviation while PBR
  reserves cover CTE 70 and C-3 Phase I covers only expected — part of what the C-3 alignment project exists to fix
  [REG-R138].
- **Nested-valuation proxy error** is invisible in a base run and appears in the tail; §2.G requires a demonstration
  that the expected simplified reserve is not below the unsimplified one [REG-R3].
- **RILA has no RBC treatment to code.** The instructions read **never name registered index-linked annuities, ILVA or
  index-linked annuities at all** [REG-R128]. Whether a RILA lands in C-3 Phase II turns on whether it is valued under
  AG 43 / VM-21; otherwise it would take factor-based C-3, presumably on the equity-indexed convention. **Neither
  reading is sourced and both are [unverified]** [REG-R128] — see "Product applicability" above, where the `?` marks
  record the same hole.

---

## Known gaps and caveats

**Paid or unretrieved publications, named at the point of use.** The **NAIC Life and Fraternal RBC Forecasting and
Instructions is a sold publication** marked "Not for Distribution"; the 2024 and 2023 editions were read from state
insurance department postings, **the 2025 edition could not be parsed**, and the RBC forecasting spreadsheet was never
obtained — so nothing here is asserted about year-end 2025 factors beyond the public newsletter's change list
[REG-R128][REG-R129][REG-R139]. The **AP&P Manual** was retrieved free in its *As of March 2026* edition [REG-R73],
superseding the earlier paid/unfetched record [REG-R33]. The reserves stream originally worked under the paid assumption
and read none of the appendix items, but **A-820 (with A-821 and A-822), A-830, A-585, A-250, A-255, AG 33 and AG 35
have since been read in full** [REG-R153][REG-R154][REG-R155][REG-R156][REG-R157][REG-R151][REG-R152], so formulaic CRVM
and CARVM detail no longer rests on the Standard Valuation Law and Model #830 alone [REG-R1][REG-R6]. **What is still
unread in that chain:** **Actuarial Guideline I**, so the deficiency-reserve interpretive layer remains second-hand
[REG-R41]; **Appendix A-791**, cited only through SSAP No. 61 [REG-R92]; **A-270**, extracted alongside A-585 but with
**no reference id assigned**, so nothing is cited from it and the variable-life guaranteed-minimum-death-benefit reserve
stays outside this library; **A-812, A-815, VM-A-814 and A-817**, the mortality-table items [REG-R110]; and **AG IX-B**,
which AG 35 names three times as an alternative source of the valuation interest rate for an indexed contract and which
this library holds only as a VM-C index entry [REG-R152][REG-R41]. Note also that the appendices **print far fewer
numbers than their subject matter suggests**: A-820 names its mortality tables without printing them, A-821 prints only
the 2012 IAM Period Table and Projection Scale G2 (the 1994 GAR, Annuity 2000 and 1983 Table "a" are named and not
printed), A-585 prints no number at all, and AG 33's only numeric parameters are the 7% expense allowance and the
run-off phase-in percentages [REG-R153][REG-R155][REG-R151]. The **Annual Statement Instructions and Blank were
retrieved** free but are the **2025** reporting year editions, so every page and line reference should be re-verified
against the 2026 blank [REG-R89][REG-R90]; the reserves stream separately failed to retrieve the blank and knows the
opinion page, Schedule S and the VM-20 Reserves Supplement only through documents referencing them
[REG-R100][REG-R108][REG-R103]. The AP&P licence is personal and non-commercial and prohibits integration "into any
software or other publication" without permission, and the Instructions and Blank carry the same NAIC copyright, so this
library **paraphrases and cites paragraphs rather than pasting text** [REG-R73][REG-R89].

**Numbers deliberately not stated.** **No AVR factor value appears anywhere in this library** — the instructions
describe the basic contribution, reserve objective and maximum reserve factors and where they are tabulated, but the
numeric factors by NAIC designation and mortgage category **were not transcribed** [REG-R89]. **No IMR
grouped-amortisation factor value appears here** either; those tables are published annually and change by year of sale,
and none was captured [REG-R89]. RBC factor tables that *were* captured are set out at "Risk-based capital" above,
within the source limits stated there.

**Pending guidance.** **INT 23-01 sunsets December 31, 2026 with automatic nullification January 1, 2027** as currently
written, and the date may move again; the replacement revised **SSAP No. 7** with a supporting issue paper was in
drafting with exposure expected after March 2026, and **the exposed text was not located or read** [REG-R87][REG-R88] —
the largest open item on the accounting side. Also open: **SSAP No. 61 funds-withheld revisions** and **SSAP No. 52
funding-agreement-backed-note disclosures**, exposed with comments due May 1, 2026, adoption unknown; an
**amortized-cost measurement method for a qualifying derivative program**, at exposure in March 2026, whose documents
were not fetched [REG-R88]; **C-3 alignment**, which would merge Phase I and Phase II into one methodology and bring
fixed indexed annuities into scope, field test specifications re-exposed July 30, 2026 [REG-R138][REG-R141]; and the
**correlation-matrix replacement for the covariance formula**, a proposal not in the instructions read [REG-R137]. The
**2026 Summer National Meeting had not been reported on** at the research access date [REG-R88]. Four of these are live
model risks rather than bibliography: the 2025 RBC instructions could not be parsed [REG-R129], the revised SSAP No. 7
was not located [REG-R88], and the correlation-matrix and C-3 alignment proposals are **not in force**
[REG-R137][REG-R138] — **re-check all four before relying on any parameter in this file for a current filing**.

**[unverified] items carried forward and not upgraded.** The AP&P Manual edition in which the SSAP "R" suffixes were
dropped [REG-R73]; the note numbering for the annual statement's withdrawal-characteristics disclosure, content verified
but note number not [REG-R89][REG-R81]; SSAP No. 86's paragraph numbering, quoted from a 2010 standalone print and not
cross-checked against the March 2026 manual, and the "Clearly Defined Hedging Strategy" phrasing attached to the pending
derivative-program project [REG-R96][REG-R88]; AG 55's Executive Committee and Plenary adoption date, only its LATF and
A Committee dates being printed and its December 31, 2025 effective date verified [REG-R103][REG-R104]; the VM-20
Reserves Supplement's supplement number and contents, known only from a search summary [REG-R108]; the first year in
which the current C-2 pricing-flexibility structure, the longevity page and the 20-designation C-1 bond factors each
took effect, all present in both instruction editions read but with no primary adoption record retrieved [REG-R128]
[REG-R129][REG-R130][REG-R131]; the reconciliation between the Academy's recommended C-2 factors and the adopted ones
[REG-R131]; the bracketing of the C-3 Phase II macro tax adjustment formula, whose published parentheses are unbalanced,
and the wording of one trend-test intermediate line [REG-R128]; whether the C-1cs beta adjustment survives in the
current instructions, the relevant page not having been read [REG-R136]; whether the stale C-1 "Basis of Factors"
narrative reflects NAIC intent [REG-R130]; the C-3 alignment field test valuation date and adoption target [REG-R138];
**RILA's RBC treatment**, which the instructions never address [REG-R128]; and whether permanent statutory IMR guidance
exists for the 2026 statutory year — a live gap for any model allocating IMR into asset adequacy analysis, since VM-30
§3.B.5 requires that allocation regardless of what the accounting guidance says [REG-R111][REG-R100].

**New [unverified] items opened by the appendix reading, recorded rather than resolved.** (i) **AG 33's effective
date.** The manual prints 31 December 1998; IRS Rev. Rul. 2002-6, the library's earlier source, said 31 December 1995 of
a differently-titled instrument. The extracted pages carry **no amendment history**, so the reconciliation is unsourced
and neither date may be presented as settled [REG-R151]. (ii) **AG 33's own vintage.** Its
guaranteed-lifetime-income-benefit material is plainly later in subject matter than a 1998 effective-date line, and
nothing in the extracted pages dates it [REG-R151]. (iii) **The A-585 → A-820 cross-reference does not resolve.** A-585
¶8.f sources its CRVM expense allowance to "paragraph 9 of Appendix A-820", but **A-820 ¶9 as printed is the
reference-interest-rate paragraph**; the quantities labelled a. and b. are at ¶11.a and ¶11.b. The identification is
structural, not textual, and is flagged as such at "Formulaic reserves" above rather than silently repaired
[REG-R155][REG-R153]. (iv) **A-830 ¶32.b's "other appendices governing universal life plans" is unnamed** and must not
be resolved to A-585 on that text [REG-R154]. (v) **A-820 ¶22 posits an empty window** — contracts "issued on or after
January 1, 2017, and prior to the operative date of the Valuation Manual", where ¶¶3–4 fix that date *at* 1 January 2017
— recorded as printed and not reconciled [REG-R153]. (vi) **A-820 ¶7's "effective date of the Codification"** is an
applicability threshold expressed by reference to an event whose date A-820 never prints; **no date is supplied for it
here** [REG-R153]. (vii) **Whether A-585 as printed differs from Model #585 §5, and whether A-830 as printed differs
from the separately published Model #830**, was not tested — neither model law was re-read against the appendix print
[REG-R155][REG-R154][REG-R5][REG-R6].
