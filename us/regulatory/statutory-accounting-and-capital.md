# U.S. Statutory Accounting and Capital Requirements for Liability Models

- **Status:** Draft, 2026-08-04 (all cited sources accessed 2026-08-04).

**Scope note.** This file explains the U.S. statutory accounting rules and capital requirements **that bear on how a
product is represented in an actuarial model** — which items exist, why they exist, which of the twelve products in
`us/products/` they bite, and what a projection must produce. It is concept-only by design: formulas, factor tables,
algorithms and worked arithmetic live in `us/regulatory/technical-notes.md`, cross-referenced by section rather than
duplicated. Product mechanics stay in `us/products/<type>/`.

**Citation conventions** (identical to the rest of the library, non-negotiable). Everything is cited as **[REG-R#]**
against the shared U.S. numbering in `us/references/regulatory-and-actuarial-references.md`, which after this work runs
R1–R142 with permanently unused gaps at **R114–R124** and **R143–R149**. R1–R72 are the frozen pre-existing entries;
R73–R142 are the statutory accounting and capital entries added now, with provenance in
`us/_research/statutory-accounting.md` (R73–R99), `us/_research/statutory-reserves.md` (R100–R113) and
`us/_research/risk-based-capital.md` (R125–R142). Every quantitative parameter, factor, threshold, formula and effective
date carries a [REG-R#] tag, or **[std]** where it is a standardization for the reference implementation, or
**[unverified]** where the research could not confirm it. **Nothing marked [unverified] is upgraded here** — this is a
subject on which plausible recollections of factor values and formula structure are easy to get wrong. The per-entry
bibliography for this directory — every [REG-R#] the two documents actually cite, with publisher, URL, access date and
fetched/not-fetched marker carried verbatim from the research files — is `us/regulatory/sources.md`.

**Documents that could not be read are named at the point of use.** The **NAIC Life and Fraternal RBC Forecasting and
Instructions is a sold NAIC publication** marked "Not for Distribution"; the 2024 and 2023 editions used here were read
from copies posted by a state insurance department, and the **2025 edition could not be parsed**, so nothing below is
asserted about year-end 2025 factors [REG-R128][REG-R129][REG-R139]. The **AP&P Manual's status is recorded
inconsistently across streams**: the *As of March 2026* edition was retrieved free and in full [REG-R73], superseding
the earlier record of it as a paid publication not fetched [REG-R33] — but the reserves stream worked under the paid
assumption and **did not read Appendix A items A-820 and A-830, nor Appendix C items AG 33 and AG 35**
[REG-R110][REG-R39][REG-R40], so formulaic CRVM and CARVM detail rests on the Standard Valuation Law [REG-R1] and Model
#830 [REG-R6]. The **AVR factor tables and IMR grouped-amortisation factor tables were deliberately not transcribed**
[REG-R89]; this file describes their role and location and **states no factor value for either**.

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

## The statutory balance sheet and income statement a model must populate

**The balance sheet.** Assets count only to the extent **admitted**; anything not usable to meet policyholder
obligations is non-admitted and charged against surplus, with the *change* flowing through the Capital and Surplus
Account rather than net income [REG-R74 ¶36]. Liabilities are recorded **when incurred**, and "estimates of losses
utilizing appropriate actuarial methodologies meet the definition of liabilities … and are **not** loss contingencies"
[REG-R91/IP5 ¶¶2–3] — the sentence that makes an actuarial reserve a liability rather than a disclosure, reinforced by
**Issue Paper No. 5 ¶7**'s requirement to accrue even where other valuation criteria do not address the item. (Those
paragraph numbers are the *issue paper*'s; the research read Issue Paper No. 5 in full and SSAP No. 5 only alongside it,
so an SSAP-paragraph cite would be unsupported [REG-R91].) Aggregate reserves for life contracts sit on Liabilities page
Line 1 and tie to Exhibit 5; the IMR sits at Page 3 Line 9.4 and the AVR at Page 3 Line 24.01 [REG-R89][REG-R90]. **Those references come from the 2025 reporting-year blank and instructions and should
be re-verified against the 2026 blank before being hard-coded** [REG-R89][REG-R90].

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
  valuation-assumption movement in parallel. Definitions and the roll-forward are in
  `us/regulatory/technical-notes.md`, "Statutory income and surplus roll-forward".

**Change in valuation basis** — interest, mortality or method — goes **direct to surplus**, measured at the **beginning
of the year**, is **not graded in** unless an actuarial guideline prescribes a transition, and is **excluded** from the
Summary and Analysis of Operations [REG-R79][REG-R80 ¶14][REG-R89]. For deposit-type contracts a voluntary election
between allowable Valuation Manual methodologies requiring commissioner approval is itself a change in basis [REG-R80].

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

**Formulaic versus principle-based.** CRVM is a modified-net-premium construction and CARVM a greatest-present-value
construction; both are contractual-guarantee calculations on prescribed mortality and a calendar-year-of-issue valuation
interest rate [REG-R1]. The principle-based regime replaces them for post-operative-date business: **VM-20** constitutes
CRVM for individual life subject to a principle-based valuation, with a net premium reserve floor [REG-R3]; **VM-21**
constitutes CARVM for variable annuities, with AG 43 pulling pre-2017 business onto it [REG-R35][REG-R38]; **VM-22**
covers non-variable annuities [REG-R36]. SSAP No. 51 ¶15 now expressly contemplates formulaic reserves being
"supplemented for some policies with more advanced deterministic and/or stochastic reserve methodologies" [REG-R79].

**The boundary is not clean, and a model must build both engines.** VM-20's net premium reserve for the *All Other*
reserving category — and for indexed UL where no deterministic or stochastic reserve is computed — is determined
"pursuant to applicable methods in **VM-A and VM-C** for the basic reserve" [REG-R3]. VM-A is an *index* of formulaic
requirements carried in AP&P Appendix A, headed by **A-820** (minimum life and annuity reserve standards) and **A-830**
(Model #830, "Regulation XXX"), with A-585 universal life, A-250 variable annuities, A-255 modified guaranteed
annuities, A-270 variable life and A-791 reinsurance among the rest [REG-R110]; VM-C is the parallel index of actuarial
guidelines [REG-R41]. So whole life, ordinary UL, VUL and un-modelled IUL run the **old CRVM calculation** inside a
PBR-era manual. Income annuities keep a formulaic track of their own, VM-V §1 setting market-linked maximum valuation
rates by bucket, jumbo rates published daily and non-jumbo quarterly [REG-R37]. **Deficiency reserves** — valuation net
premiums in excess of gross — survive as a distinct item under Actuarial Guideline I via VM-C [REG-R41] and Model #830
via A-830 [REG-R6][REG-R110], reported in Exhibit 5 Miscellaneous Reserves [REG-R89]. **Neither the AG I text nor A-820
and A-830 as printed in the manual was retrieved** [REG-R33][REG-R110], and **AG 33 and AG 35 — formulaic CARVM for
deferred and indexed annuities — remain unread**, so this library cannot quote their mechanics [REG-R39][REG-R40].

**Two obligations around the calculation are not calculations.** **VM-31** requires a PBR Actuarial Report documented so
"another actuary qualified in the same practice area [can] evaluate the work", Summaries filed by April 1; a company
computing no deterministic or stochastic reserve because it passed the exclusion tests **must still file a sub-report**
[REG-R108]. **VM-G** decides who owns the model, with a counter-intuitive edge: passing an exclusion test by the
deterministic-reserve method, the VM-22 adjusted-scenario-reserve method or the Stochastic Exclusion Demonstration Test
**re-imposes** the board and senior management sections a pure exclusion-test company would escape, and that company's
actuary must still report **readiness to calculate the deterministic and/or stochastic reserve** — a requirement that
the model be *able* to compute components it currently omits [REG-R109]. Mechanics and the exclusion tests as decision
procedures are in `us/regulatory/technical-notes.md`, "Formulaic reserves", "VM-20" and "VM-21 and VM-22"; practice
guidance is at [REG-R23], [REG-R31] and [REG-R25].

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
the numbering is **[unverified]** even though the rule is first-hand [REG-R96]. **This file
states no AVR factor and no IMR amortisation factor: the research explicitly did not transcribe them** [REG-R89].
Algorithms are in `us/regulatory/technical-notes.md`, "Interest maintenance reserve and asset valuation reserve".

**Negative IMR, and the current admittance treatment.** The baseline rule is that a positive net IMR is a liability and
a **negative net IMR is a non-admitted write-in asset**, the change running through the Capital and Surplus Account
[REG-R87][REG-R89]. **INT 23-01** provides limited-time, optional exception guidance permitting a life insurer to
**admit** net negative (disallowed) IMR, on conditions a projection must test at each reporting date: an admittance cap
as a percentage of **adjusted** general account capital and surplus (excluding goodwill, EDP equipment and software, net
deferred tax assets and the admitted negative IMR itself), joined since August 2025 by a second cap on **current-period
unadjusted** surplus; an **RBC gate** requiring the company to sit above a stated multiple of Authorized Control Level
on a similarly adjusted Total Adjusted Capital; a **derivative symmetry** condition requiring documented evidence that
unrealized *gains* from fair-value derivatives were historically reversed into IMR before losses may be included; a
**disclosure** condition whose failure forces non-admittance of the whole balance; and an ordering rule admitting
general account negative IMR first, with the admitted amount mirrored into **special surplus funds** expressly "to
preclude the ability for admitted negative IMR to be reported as funds available to dividend" [REG-R87]. Threshold
values are in `us/regulatory/technical-notes.md`, "Interest maintenance reserve and asset valuation reserve".

The condition that makes this a *modelling* problem rather than a disclosure problem is **¶9.e**: an entity admitting
negative IMR must **capture the admitted negative IMR in the PBR calculation or in asset adequacy / cash flow testing
under VM-20 §7.D.7 and VM-30 §3.B.5**, and reconcile it to the IMR reflected there "to ensure reserves are not
overstated" [REG-R87]. VM-30 §3.B.5 independently requires an allocation of assets in the amount of the IMR, **positive
or negative**, in any asset adequacy analysis; requires any non-admitted portion to be removed first; and requires **the
full amount of any admitted negative IMR to be used**, reducing allocated assets by its absolute value [REG-R100]. The
IMR has **no cash flows** of its own — it is a sign-aware, non-cash-flow adjustment to starting assets [REG-R111].

**Status, stated honestly.** INT 23-01 was adopted August 13, 2023 through December 31, 2025 with automatic
nullification January 1, 2026, and was **extended on August 11, 2025 by one year to December 31, 2026, with automatic
nullification January 1, 2027**; the date may move again [REG-R87]. The replacement is a **substantially revised SSAP
No. 7** absorbing the AVR/IMR guidance from the annual statement instructions, with a supporting issue paper: an initial
version reached the IMR Ad Hoc Group on February 24, 2026 and exposure was expected after the March 2026 Spring National
Meeting, at which an "IMR **proof of reinvestment**" concept was adopted [REG-R88]. **The exposed revised SSAP No. 7 was
not located or read**, and the 2026 Summer National Meeting had not been reported on at the research access date
[REG-R88]. Note that the Academy practice note, written September 2024, states the interim solution was nullified
January 1, 2026 — **superseded by the August 2025 extension** [REG-R111][REG-R87].

---

## Separate accounts

**Two balance sheets, one income statement.** SSAP No. 56 keeps sales, underwriting, contract administration, premium
collection, premium tax, claims and benefits as **general account** functions [REG-R83 ¶4]. For separate account
contracts classified as life contracts, premiums and considerations are income in the **general account** summary of
operations and simultaneously a **transfer** to the separate account statement; separate account charges — investment
management, administration, contract guarantees — and the separate account's net gain from operations are general
account income; benefits, surrenders, net transfers, commissions and premium taxes are general account expenses
[REG-R83 ¶5]. The annual statement reinforces this: every transfer reported on the separate accounts transfer line must
**also** appear in the premium, benefit, withdrawal or other captioned lines of the Analysis of Operations [REG-R89].

**General-account guarantee reserves and the surplus floor.** A **GMDB reserve on a variable annuity or variable life
contract is held in the general account**, and any difference between the benefit paid and the separate account value is
charged or credited to general account net gain from operations [REG-R83 ¶7]. VM-20's split rule is the mirror image:
the general account share may not be **less than zero** and must include any liability for general-account contractual
guarantees, while the separate account share must be at least the sum of cash surrender values and at most the sum of
account values [REG-R3]. And **"separate account surplus may not become negative"** — the general account funds any
deficiency, a mortality deficiency on annuitized contracts being funded by a general account expense matched by separate
account revenue, with mortality gains running the other way [REG-R83 ¶8]. Surplus created by CRVM or CARVM is reported
by the general account as an **unsettled transfer** [¶9]; seed money is separate account surplus until repatriated [¶10].

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
assets are at fair value** [REG-R83 ¶30]. **Separate account IMR is required where assets are at book value and not
where they are at fair value**, applied account by account [¶¶26–27]. **Separate account AVR** is required where the
reporting entity rather than the policyholder bears default and fair-value loss — so traditional VA and VL separate
accounts need none except on the **seed money** portion, while book-value separate accounts, modified guaranteed
contracts, MVA contracts and contracts with book-value guarantees do — and it is **combined with the general account
AVR** for reporting [¶¶11, 23–25]. A RILA statutory model may therefore need a **book-value separate account carrying
its own AVR and IMR**, unlike a traditional VA. Open regulator questions on the glossary definition of *Guarantee* and
on non-cash-transfer IMR guidance are at [REG-R84], and a March 2026 revision on nonadmittance for general-account-basis
assets in the separate account at [REG-R88].

---

## Reinsurance and taxes

**Reinsurance.** Exhibit 5 reserves are computed **gross**, with a **ceded deduction computed using the same mortality,
interest and valuation method** but reflecting the actual mode of reinsurance; because the assuming reinsurer may value
differently, the ceded deduction need not equal the assumed reserve, and **no deduction is taken for modified
coinsurance** [REG-R89]. The ceding entity's reserve credit is **a reduction of reserves, not an asset**; YRT credit is
the one-year term mean reserve on the amount ceded on the *original policy's* mortality and interest basis
[REG-R92 ¶¶36–38]. Credit exists only where the assuming insurer qualifies under Credit for Reinsurance Model Law #785
or the asset-or-reduction-from-liability route, with Model Regulation #786 supplying trust and letter-of-credit
mechanics [REG-R94][REG-R95]. **Risk transfer is the gate**: an agreement that limits or diminishes risk transfer or
"contains any contractual feature that delays timely reimbursement" follows **deposit accounting** instead, multiple
contracts achieving "one overall planned effect" are evaluated together, and combined structures must in aggregate avoid
the Appendix A-791 prohibited conditions [REG-R92 ¶17] — **A-791 itself was cited only through SSAP No. 61 and not
read**. For a model the requirement is that gross and ceded be produced **separately, not netted**, so Exhibit 5 and
Schedule S can be filled; losses are recognised immediately, and recaptures unwind through the original accounts with
the required IMR adjustment [REG-R92 ¶¶55–58]. A March 2026 exposure would require **funds withheld liabilities to equal
the carrying value of the funds withheld assets**, adoption unknown [REG-R88].

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
**1.5×**, and Mandatory Control Level **0.70×** Authorized Control Level RBC. A **Company Action Level Event** occurs
when Total Adjusted Capital falls between Regulatory and Company Action Level RBC — or, for a life or fraternal insurer,
between Company Action Level RBC and **3.0×** Authorized Control Level **with a negative trend** — and requires an **RBC
Plan** within 45 days. A **Regulatory Action Level Event** adds a corrective order and examination, and is also
triggered by failure to file, to submit a Plan, or to adhere to one. An **Authorized Control Level Event** permits the
commissioner to place the insurer under regulatory control; a **Mandatory Control Level Event** requires it for a life
insurer. The **RBC Plan must project statutory operating income, net income, capital and surplus for the current year
and at least four succeeding years, both with and without proposed corrective actions** [REG-R125] — the only place the
model act itself mandates projection output, and the reason a liability cash flow model sits on the critical path for
RBC rather than only at the valuation date.

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
  **pre-reform** package and is **superseded in its parameters** — never read a CTE level, a scalar or a tax rate off it.
  [REG-R48] is the reform analysis behind the change, and recommended CTE 95 with a 25% scalar where the adopted
  instructions land on CTE 98 with that scalar: the scalar survived, the CTE level did not [REG-R48][REG-R128].
- **C-4a** is business risk on premiums and separate account liabilities, referenced to guaranty fund assessment
  exposure; **C-3b** and **C-4b** are health-related and immaterial here [REG-R128].

**The covariance adjustment and its rationale.** The instructions state the assumption before the arithmetic: "the
combined effect of the C-1o, C-1cs, C-2 and C-3 and a portion of the C-4 risks are not equal to their sum but are equal
to the square root calculation described below. It is statistically assumed that the C-1o risk and a portion of the C-3
risk are correlated, while the C-1cs risk, the C-2 risk, the balance of the C-3 risk and a portion of the C-4 risk are
independent of both" [REG-R128]. Three structural facts an implementer gets wrong easily, each verified three
independent ways within the retrieved instructions: **C-3a is added to C-1o inside one squared term**; **C-3c is added
to C-1cs**, not to C-3a; and **C-0 and C-4a sit outside the radical**, added dollar-for-dollar, while C-4b sits inside
as its own squared term [REG-R128]. All terms entering the combination are post-tax. Outside covariance sit the
operational risk add-on, a charge on admitted adjusted gross deferred tax assets, and the **AG 48 Primary Security
shortfall**, doubled before the halving that produces Authorized Control Level so that it lands dollar-for-dollar
[REG-R128][REG-R11][REG-R12]. A **proposal** to replace the square-root form with an explicit correlation matrix exists
but is **not in the instructions read** [REG-R137]. The published expression is reproduced in
`us/regulatory/technical-notes.md`, "Risk-based capital".

**Total Adjusted Capital and the role of the AVR.** TAC is statutory capital and surplus plus **the AVR**, plus half of
apportioned and unapportioned dividend liabilities, plus prorated life-subsidiary AVR and dividend liability, less
specified items, plus limited credit for capital notes, less the XXX/AXXX reinsurance shortfall [REG-R128]. The reason
the AVR counts as capital is stated in the instructions: "In determining the C-1 risk factors, availability of the AVR
and voluntary investment reserves to absorb specific losses was not assumed. Therefore, the AVR is counted as capital
for the purposes of the formula although it represents a liability and is not usable against general contingencies"
[REG-R128]. **The portion that counts is limited to the amount not utilized in asset adequacy testing in support of the
actuarial opinion** — a direct coupling from the appointed actuary's work into the numerator of the RBC ratio, requiring
the asset adequacy model to *report how much AVR it consumed* [REG-R128][REG-R29]. The headline ratio is **Total
Adjusted Capital ÷ Authorized Control Level RBC**.

**The trend test.** It bites only in the band above Company Action Level but below the **3.0× Authorized Control Level**
safe harbour, where the mechanical Level of Action would otherwise read "None" [REG-R128][REG-R127]. It compares the
margin of Total Adjusted Capital over Authorized Control Level RBC across years, takes the greater of the one-year
decrease and a three-year average decrease, subtracts it from current Total Adjusted Capital, and triggers Company
Action Level if the result falls below a stated multiple of Authorized Control Level [REG-R128]. The life safe harbour
was **2.5× before a 2011 amendment raised it to 3.0×** [REG-R126]. The arithmetic, including the trigger multiple, is in
`us/regulatory/technical-notes.md`, "Risk-based capital". Change control runs through the Capital Adequacy
(E) Task Force and the Life RBC (E) Working Group on a fixed calendar — structural blank changes by May 15,
non-structural by June 30, instructions published around November 1 [REG-R140][REG-R141][REG-R139].

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
  adequacy analysis supporting the opinion, so the capital numerator depends on a CFT model output [REG-R128][REG-R29].
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

Architecture guidance, the reserve roll-forward recursion and reconciliation checks are in
`us/regulatory/technical-notes.md`, "Implementation notes and model architecture" and "Validation and reconciliation
checks".

---

## Product applicability

`x` = the item directly binds the product; `(x)` = binds conditionally, partially, or only through one component;
`—` = expressly excluded by the cited source; `?` = treatment genuinely unsettled in the documents retrieved; blank =
not indicated by the sources read. Derived from the product-applicability sections of the three research files. Columns
are `us/products/` names abbreviated: TERM = term-life, WL = whole-life, UL = universal-life, IUL = indexed-ul,
VUL = variable-ul, GUL = guaranteed-ul, FDA = fixed-deferred-annuity, FIA = fixed-indexed-annuity, VA = variable-annuity,
RILA = registered-index-linked-annuity, SPIA = immediate-annuity, DIA = deferred-income-annuity.

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
| Formulaic CRVM — SVL §5 via VM-A/VM-C [REG-R1][REG-R110][REG-R41] | x | x | x | x | x | x | | | | | (x) | (x) |
| Formulaic CARVM — SVL §5a, AG 33/AG 35 [REG-R1][REG-R39][REG-R40] | | | | | | | x | x | x | x | x | x |
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
[REG-R128][REG-R135]; the scope statement is set out in `us/regulatory/technical-notes.md`, "Risk-based capital".

**RILA's capital treatment is genuinely unsettled, and the `?` marks say so rather than guessing.** The RBC instructions
read **never mention registered index-linked annuities, ILVA, or index-linked annuities at all** [REG-R128]. Whether a
RILA lands in C-3 Phase II depends on whether the contract is valued under AG 43 / VM-21; otherwise it would take
factor-based C-3, presumably on the equity-indexed convention. **Neither reading is sourced, and the research records
the inference as [unverified]** [REG-R128]. The same silence affects its VM-21 and VM-22 rows. This is a real hole for
one of the twelve products, not an artefact of incomplete reading.

---

## Known gaps and caveats

**Paid or unretrieved publications, named at the point of use.** The **NAIC Life and Fraternal RBC Forecasting and
Instructions is a sold publication** marked "Not for Distribution"; the 2024 and 2023 editions were read from state
insurance department postings, **the 2025 edition could not be parsed**, and the RBC forecasting spreadsheet was never
obtained — so nothing here is asserted about year-end 2025 factors beyond the public newsletter's change list
[REG-R128][REG-R129][REG-R139]. The **AP&P Manual** was retrieved free in its *As of March 2026* edition [REG-R73],
superseding the earlier paid/unfetched record [REG-R33] — but the reserves stream, working under the paid assumption,
**did not read A-820, A-830, AG 33 or AG 35** [REG-R110][REG-R39][REG-R40], so formulaic CRVM detail rests on the
Standard Valuation Law and Model #830 [REG-R1][REG-R6] and formulaic CARVM for deferred and indexed annuities on the
statutory text alone; **Appendix A-791** was likewise cited only through SSAP No. 61 [REG-R92]. The **Annual Statement
Instructions and Blank were retrieved** free but are the **2025** reporting year editions, so every page and line
reference should be re-verified against the 2026 blank [REG-R89][REG-R90]; the reserves stream separately failed to
retrieve the blank and knows the opinion page, Schedule S and the VM-20 Reserves Supplement only through documents
referencing them [REG-R100][REG-R108][REG-R103]. The AP&P licence is personal and non-commercial and prohibits
integration "into any software or other publication" without permission, and the Instructions and Blank carry the same
NAIC copyright, so this library **paraphrases and cites paragraphs rather than pasting text** [REG-R73][REG-R89].

**Numbers deliberately not stated.** **No AVR factor value appears anywhere in this library** — the instructions
describe the basic contribution, reserve objective and maximum reserve factors and where they are tabulated, but the
numeric factors by NAIC designation and mortgage category **were not transcribed** [REG-R89]. **No IMR
grouped-amortisation factor value appears here** either; those tables are published annually and change by year of sale,
and none was captured [REG-R89]. RBC factor tables that *were* captured are left to `us/regulatory/technical-notes.md`
and the cited instructions, since this file states concepts and drivers, not arithmetic.

**Pending guidance.** **INT 23-01 sunsets December 31, 2026 with automatic nullification January 1, 2027** as currently
written, and the date may move again; the replacement revised **SSAP No. 7** with a supporting issue paper was in
drafting with exposure expected after March 2026, and **the exposed text was not located or read** [REG-R87][REG-R88] —
the largest open item on the accounting side. Also open: **SSAP No. 61 funds-withheld revisions** and **SSAP No. 52
funding-agreement-backed-note disclosures**, exposed with comments due May 1, 2026, adoption unknown; an
**amortized-cost measurement method for a qualifying derivative program**, at exposure in March 2026, whose documents
were not fetched [REG-R88]; **C-3 alignment**, which would merge Phase I and Phase II into one methodology and bring
fixed indexed annuities into scope, field test specifications re-exposed July 30, 2026 [REG-R138][REG-R141]; and the
**correlation-matrix replacement for the covariance formula**, a proposal not in the instructions read [REG-R137]. The
**2026 Summer National Meeting had not been reported on** at the research access date [REG-R88].

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
