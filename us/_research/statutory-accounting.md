# Statutory Accounting Framework and Financial Reporting — research notes (U.S. statutory accounting and capital)

**Stream:** Statutory Accounting Framework and Financial Reporting
**Access date for every citation below:** 2026-08-04
**Status:** research notes, not yet merged into `us/references/regulatory-and-actuarial-references.md`

---

## Scope and numbering note

This stream owns reference block **R73–R99**. Entries **R1–R72** live in
`us/references/regulatory-and-actuarial-references.md`, are **frozen**, and are already
cited by product documentation; nothing below renumbers, restates or duplicates them.
Existing entries that bear on statutory accounting are listed in the next section with a
one-line note on how they bite, and are cited as `[R#]` throughout without being
re-created. New entries are numbered sequentially from R73; R73–R99 are all used.

**Two retrieval facts that change how this stream should be documented:**

1. **The NAIC Accounting Practices and Procedures Manual is no longer a paid
   publication.** The *As of March 2026* edition — Preamble, all SSAPs, and Appendices
   A–G — is offered as a **Free Download** from the NAIC publications catalogue and was
   retrieved in full (2,117 pages) [R73]. R33 (frozen) describes the manual from the
   publications landing page and records it as "a paid publication … not fetched"; that
   note is **superseded in fact** by R73, and the R33 annotation should be flagged when
   the reference page is next revised. R73 is a different document (the manual itself)
   from R33 (the catalogue page), so this is a new entry, not a restatement.
2. **The "R" suffixes have been dropped from SSAP numbers.** In the *As of March 2026*
   manual the statements are printed and indexed as **SSAP No. 5, No. 51, No. 54,
   No. 61, No. 43** — a full-text search of the manual finds **no occurrence of "51R",
   "54R" or "86R"**, and "5R"/"61R"/"43R" survive only inside historical issue-paper and
   interpretation text [R73]. This stream's brief named SSAP Nos. 51R / 54R / 61R / 5R;
   those are the **historical** designations. Cite the unsuffixed numbers for current
   guidance and keep the "R" form only when quoting pre-2024 material. The exact edition
   in which the suffix was removed was not located [unverified].

**Copyright caution (applies to R73 and everything drawn from it).** The AP&P Manual
carries a licence "for personal and non-commercial use only" and prohibits redistribution
or integration "into any software or other publication" without written permission [R73].
Product documentation in this library must therefore **paraphrase** SSAP mechanics and
cite the paragraph, not paste SSAP text. Everything in the "Extracted mechanics" section
below is paraphrase plus short attributed quotation. The Annual Statement Instructions
and Blanks (R89, R90) carry the same NAIC copyright notice.

---

## Existing entries (R1–R72) that bear on this stream

| R# | Short title | How it bears on statutory accounting and financial reporting |
|----|-------------|--------------------------------------------------------------|
| R1 | Standard Valuation Law (Model #820) | The statute behind the reserve that Exhibit 5 reports; SSAP No. 51 ¶16 and SSAP No. 52 ¶8 both defer to AP&P Appendix A-820, which is the excerpt of Model #820 [R78][R80]. |
| R3 | Valuation Manual (VM-20/21/22/30/31/M/V/G/C) | Supplies the reserve number that statutory accounting *reports*; SSAP No. 51 ¶15 expressly contemplates deterministic/stochastic supplements for post-operative-date policies [R78]. INT 23-01 ¶9.e ties admitted negative IMR back into **VM-20 §7.D.7** and **VM-30 §3.B.5** [R87]. |
| R29 | ASOP 22 (asset adequacy opinions) | Exhibit 5's "additional actuarial reserves — asset/liability analysis" line and SSAP No. 52 ¶16.b both point at asset adequacy analysis under AP&P Appendix A-822 [R80][R89]. |
| R31 | ASOP 52 (life PBR) | Governs the reserve feeding the Exhibit 5 "VM-20NPR" and "VM-20 DET/STO" valuation-standard codes [R89]. |
| R33 | NAIC AP&P Manual (catalogue-page description) | Same manual as R73 but cited from the publications page and recorded as paid/unfetched. Keep for the catalogue description; use R73 for anything drawn from the manual text. |
| R34 | FASB ASU 2018-12 (LDTI) | The GAAP counterpart the statutory basis is being contrasted against. **SSAP No. 71 ¶6 and SSAP No. 56 ¶45 expressly *reject* ASU 2018-12 for statutory purposes** [R75][R83] — so a model cannot reuse a GAAP DAC or MRB result in a statutory run. |
| R35 / R36 / R37 | VM-21 / VM-22 / VM-V §1 | Produce the annuity reserve amounts Exhibit 5 requires to be split by **Jumbo / Non-Jumbo and 50-basis-point valuation-interest bands** for VM-22 business [R89]. |
| R38–R41, R44 | AG 43 / AG 33 / AG 35 / VM-C / AG 54 | Live in **AP&P Appendix C**, which is Volume II of the manual now retrievable at R73 — the "could not be read" gap recorded in the R35–R72 gaps section is now closable. |
| R47 | C-3 RBC instructions (incl. Academy C3 Phase II report) | The capital layer above the accounting layer; its Total Asset Requirement is built on projected **statutory** surplus, so it consumes the same statutory income projection this stream specifies. |
| R48 | Oliver Wyman QIS II (VA reform) | Explains why the VA capital charge is measured against a *book-value statutory* reserve — the basis this stream documents. |
| R55 / R16 / R72 | IRC §72, §807, LB&I directive | Tax basis built off the statutory reserve; SSAP No. 101 turns the statutory-vs-tax difference into the deferred tax balances whose admittance is tested at R97. |
| R70 / R71 | ASOP 54 (pricing), ASOP 10 (U.S. GAAP LDTI) | R71's vocabulary (DAC, cohort, MRB, lock-in) is exactly the vocabulary statutory accounting does **not** have; useful as the contrast set. |

---

## New entries

All URLs below were retrieved on **2026-08-04**. NAIC PDFs return raw compressed streams
to the fetch tool (as the R35–R72 retrieval note records); every "fetched: yes (local text
extraction)" entry was downloaded and its text extracted locally with `pypdf` before
reading, so the annotations are first-hand.

### A. The statutory basis itself

#### R73. NAIC Accounting Practices and Procedures Manual, *As of March 2026* (Volumes I and II)
- **Publisher:** National Association of Insurance Commissioners
- **URL:** https://content.naic.org/sites/default/files/publication-app-manual.pdf
  (catalogue entry "APPM-2026 … Free Download" on https://content.naic.org/publications)
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; 2,117 pages; front matter, full SSAP index, and
  the SSAPs listed at R74–R97 read directly)
- **Annotation:** The complete authoritative statutory accounting text — **Volume I**:
  Preamble, all SSAPs, Appendix A (excerpts of NAIC model laws, e.g. A-820 valuation,
  A-822 asset adequacy, A-830 Model #830, A-791 life reinsurance conditions, A-695
  synthetic GICs, A-200 group life separate accounts), Appendix B (interpretations,
  including INT 23-01); **Volume II**: Appendix C (actuarial guidelines — AG 33, 35, 38,
  43, 48, 49-A, 51 live here), Appendix D (GAAP-to-SAP cross-reference), Appendix E
  (statutory issue papers), Appendix F (policy statements), Appendix G (implementation
  guide for the Annual Financial Reporting Model Regulation) [R73]. Completely superseded
  SSAPs are moved out to **Appendix H**, posted separately on the SAPWG web page [R73].
  This entry is the source-of-record for every SSAP paragraph cited below; the per-SSAP
  entries that follow exist so product documentation can cite a specific statement.
  **Licence:** personal / non-commercial use; redistribution or integration into other
  publications prohibited without NAIC permission [R73].

#### R74. AP&P Manual **Preamble** — Statutory Accounting Principles Statement of Concepts and Statutory Hierarchy (*As of March 2026*)
- **Publisher:** NAIC (Preamble, pages P-1 to P-10 of R73)
- **URL:** https://content.naic.org/sites/default/files/publication-app-manual.pdf (Preamble section)
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; §§27–42 read in full)
- **Annotation:** The conceptual charter that makes statutory accounting behave
  differently from GAAP, and the single best short statement of *why* a statutory
  projection has a different earnings shape. "SAP utilizes the framework established by
  GAAP" but integrates "objectives exclusive to statutory accounting"; a GAAP
  pronouncement is **not** part of SAP until the NAIC specifically adopts it [R74 ¶27].
  The objective is solvency: to ensure obligations "are met when they come due" and that
  companies "maintain capital and surplus at all times … to provide an adequate margin of
  safety" [R74 ¶30]. Three concepts — **conservatism** ("valuation procedures should, to
  the extent possible, prevent sharp fluctuations in surplus" [R74 ¶33]), **consistency**
  [¶34], **recognition** (balance-sheet primacy; the income statement is "a secondary
  focus" [¶35]). The two operative rules for a projection model: assets not usable to meet
  policyholder obligations "should not be recognized on the balance sheet but rather
  should be charged against surplus" [¶36]; and "**Accounting treatments which tend to
  defer expense recognition do not generally represent acceptable SAP treatment**"
  [¶38] — the sentence from which the no-DAC rule follows. ¶37 names IMR and AVR as
  examples of statutorily mandated liabilities. §V sets the **statutory hierarchy** with
  SSAPs at Level 1 [¶42].
- **Also useful (fetched, same date):** NAIC insurance-topics page "Statutory Accounting
  Principles", https://content.naic.org/insurance-topics/statutory-accounting-principles
  — plain-language framing that "SAP focuses on the balance sheet and an insurer's ability
  to meet its obligations" while U.S. GAAP "focuses more on providing information to
  investors", and that the AP&P Manual "sets a national framework … but it does not
  override state laws" (prescribed and permitted practices) [R74b].

### B. Acquisition costs — the difference that reshapes statutory earnings

#### R75. SSAP No. 71 — Policy Acquisition Costs and Commissions (*As of March 2026*)
- **Publisher:** NAIC (in R73, statement pages 71-1 to 71-3)
- **URL:** https://content.naic.org/sites/default/files/publication-app-manual.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; ¶¶1–7 read in full)
- **Annotation:** Three paragraphs decide the shape of statutory earnings for every
  product in this library. ¶2 defines acquisition costs as those "incurred in the
  acquisition of new and renewal insurance contracts" that "vary with and are primarily
  related to" acquisition — agent and broker commissions, certain underwriting and policy
  issue costs, medical and inspection fees — and requires that they "**shall be expensed
  as incurred**", with the timing of incurrence set by SSAP No. 5 [R75 ¶2]. **There is no
  DAC asset in statutory accounting.** ¶3 sets contingent-commission liabilities on the
  earned portion of loss-experience formulas. ¶¶4–5 are the anti-avoidance rule: levelized
  commission arrangements, in which a third party fronts first-year commission and the
  insurer repays it in level instalments, are "in fact, funding agreements", and the
  insurer must book **a liability for the full unpaid principal and accrued interest**;
  the full initial sales commission "shall be recognized immediately as the writing of an
  insurance contract is the event that obligates the insurer", regardless of whether a
  third-party structure references policy persistency [R75 ¶¶4–5]. ¶6 **rejects** ASU
  2018-12 (LDTI), ASU 2010-26, FAS 60, FAS 97 and SOP 05-1 — i.e. every GAAP DAC regime.
  Effective January 1, 2001; the March 15, 2021 levelized-commission revisions apply to
  contracts in effect as of December 31, 2021 and new contracts thereafter [R75 ¶7].
  Status block records **no interpretations** of SSAP No. 71 [R75].

#### R76. Statutory Issue Paper No. 71 — Policy Acquisition Costs and Commissions
- **Publisher:** NAIC (finalized March 16, 1998; AP&P Appendix E)
- **URL:** https://content.naic.org/sites/default/files/inline-files/071_H.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; 6 pages, read in full)
- **Annotation:** The reasoning record behind R75, and the cleanest primary statement of
  the SAP-vs-GAAP divergence: "GAAP accounting for policy acquisition costs and
  commissions is driven by the objective of matching revenues and expenses, therefore
  these costs are deferred and amortized to income as the related premium is recognized as
  revenue for FAS 60 products **or in proportion to estimated gross profits for FAS 97
  products**. The primary objective of statutory accounting is to measure solvency"
  [R76 ¶8], followed by the Statement-of-Concepts quotation on deferring expense
  recognition. The paper reproduces FAS 60 ¶¶28–31 and FAS 97 ¶¶22–25 verbatim, so it
  doubles as a free source for the **estimated-gross-profit DAC amortisation mechanics** a
  GAAP comparison run needs [R76 ¶¶16–17]. It also records that the issue paper is
  consistent with Issue Paper No. 50, "which rejects FAS 60 and FAS 97" [R76 ¶9].

#### R77. SAPWG Ref #2019-24 — SSAP No. 71 levelized commission revisions (hearing packet, 2020)
- **Publisher:** NAIC Statutory Accounting Principles (E) Working Group
- **URL:** https://content.naic.org/sites/default/files/call_materials/11-20%20SAPWG%20combined%20Hearing%202%20SSAP%20No%2071.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; 35 pages; Attachment A / Form A and the exposed
  redlines read)
- **Annotation:** The development record for the 2021 SSAP No. 71 revisions, reproducing
  the **pre-2021 text of ¶¶2–5** alongside the exposed redlines — useful for dating a
  model's expense-recognition logic against in-force cohorts. Key drafting principle
  captured in the staff recommendation: commission contracts that include persistency (or
  similar) components "shall not use these clauses to defer recognition of commission
  expense"; a persistency-based commission "shall be accrued based on experience to date"
  [R77]. Confirms the change was categorised **nonsubstantive** — a clarification of
  original intent, not a new principle [R77].

### C. Contract classification and the product liabilities

#### R78. SSAP No. 50 — Classifications of Insurance or Managed Care Contracts (*As of March 2026*)
- **Publisher:** NAIC (in R73, statement pages 50-1 onward)
- **URL:** https://content.naic.org/sites/default/files/publication-app-manual.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; ¶¶1–20 read)
- **Annotation:** The classification gate. Four categories — life, accident and health,
  property and casualty, **deposit-type**. A contract in which the entity "does not assume
  any mortality, morbidity, health benefit costs incurred, or casualty risk and which
  act[s] exclusively as [an] investment vehicle" is a deposit-type contract, and
  critically: "**Such classification shall be made at the inception of the contract and
  shall not change**" [R78 ¶5]. Life contracts are enumerated to include whole life,
  endowment, term, supplementary contracts, group life, franchise, **universal life type**,
  **variable life**, limited payment, credit life and **annuity contracts** [R78 ¶9]. ¶8
  gives the generic reserve as PV(future benefits) − PV(future net premiums) at valuation
  interest and mortality. Paragraphs 10–20 carry the statutory *product definitions*
  (ordinary vs industrial, whole life, endowment, term …) that the annual statement's
  line-of-business columns key off.

#### R79. SSAP No. 51 — Life Contracts (*As of March 2026*; historically cited as SSAP No. 51R)
- **Publisher:** NAIC (in R73, statement pages 51-1 to 51-13)
- **URL:** https://content.naic.org/sites/default/files/publication-app-manual.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; status block, ¶¶1–16 read; section index read)
- **Annotation:** Income recognition and policy reserves for everything SSAP No. 50
  classifies as a life contract, **except** credit contracts (SSAP No. 59) and separate
  account products (SSAP No. 56) [R79 ¶1]. Status: initial draft, "Conceptually revised
  June 9, 2016", conceptual revisions effective **January 1, 2017** — i.e. aligned to the
  Valuation Manual operative date; interpreted by INT 00-03; relevant Appendix A guidance
  A-200, A-225, A-235, A-585, A-620, A-641, A-695, A-812, A-815, A-817, A-820, A-821,
  A-822, A-830 [R79]. Gross/net premium and **loading** definitions at ¶¶2–4. Premium
  income recognised **gross, when due**, including single and flexible premiums when
  received [¶5]; dividends/coupons applied to buy paid-up additions are premium income
  [¶6]; advance premiums excluded [¶7]; increased by assumed and reduced by ceded
  reinsurance premium [¶9]. ¶11 is the loading adjustment on deferred and uncollected
  premium — change in loading is an **expense**, not a reduction of premium. ¶14 is the
  UL-specific carve-out: a flexible-premium UL "waiver of monthly deductions" benefit is
  "not to be considered revenue nor a benefit paid", so no deduction amount need be
  computed [¶14]. ¶15 is the reserve definition and now expressly contemplates that
  formulaic reserves "will be supplemented for some policies with more advanced
  deterministic and/or stochastic reserve methodologies" for post-operative-date issues.
  Further sections (read via the section index and the parallel issue paper at R81):
  mean-reserve vs mid-terminal methods and the deferred-premium asset, advance premiums,
  policyholder dividend liability, coupons, reserve recognition, change in valuation
  basis, supplemental benefits, unearned income, accelerated benefits, additional reserves
  not included elsewhere, and the disclosure set.

#### R80. SSAP No. 52 — Deposit-Type Contracts (*As of March 2026*)
- **Publisher:** NAIC (in R73, statement pages 52-1 to 52-8)
- **URL:** https://content.naic.org/sites/default/files/publication-app-manual.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; ¶¶1–17 read in full)
- **Annotation:** The other side of the classification test, and the reason a
  period-certain-only immediate annuity is **not** an insurance contract for statutory
  purposes. ¶2 defines the risk test: mortality or morbidity risk is present "if, under
  the terms of the contract, the reporting entity is required to make payments or forego
  required premiums contingent upon the death or disability … **or the continued survival
  (in the case of annuity contracts)** of a specific individual or group of individuals"
  [R80 ¶2]. ¶5 lists the candidate categories: supplemental contracts, lottery payouts,
  structured settlements, guaranteed interest contracts, income settlement options,
  dividend and coupon accumulations, **annuities certain**, premium and other deposit
  funds. ¶6 is the income-statement consequence: amounts received "shall not be reported
  as revenues but shall be recorded directly to an appropriate policy reserve account".
  ¶9 splits the reserve into two regimes — **PV of future guaranteed benefits at the
  valuation interest rate** where benefits are fixed and guaranteed, versus **accumulated
  amounts paid plus contractual income accumulation less withdrawals and applicable
  surrender charges** for everything else. ¶13: credited interest is an **expense** in the
  summary of operations; a return of policyholder balance is not an expense, and any
  difference from the recorded reserve is a benefit expense. ¶14 change in valuation basis
  goes **direct to surplus**, measured at beginning of year, no grading unless an actuarial
  guideline prescribes it — and, newly, a voluntary change between allowable Valuation
  Manual methodologies requiring commissioner approval is a change in valuation basis.
  ¶16 additional actuarial liabilities (surrender values in excess of reserves; asset
  adequacy additions per A-822). ¶17 is the FHLB funding-agreement substance test.

#### R81. Statutory Issue Papers Nos. 50, 51, 52 and 110 — the codification record behind SSAP Nos. 50/51/52/56
- **Publisher:** NAIC (AP&P Appendix E; IP 50 finalized June 23, 1998; IP 51 and IP 52
  finalized March 16, 1998; IP 110 finalized September 12, 2000)
- **URLs:**
  - IP 50: https://content.naic.org/sites/default/files/inline-files/050_y.pdf
  - IP 51: https://content.naic.org/sites/default/files/inline-files/051_A.pdf
  - IP 52: https://content.naic.org/sites/default/files/inline-files/052_y.pdf
  - IP 110: https://content.naic.org/sites/default/files/inline-files/110_d.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes, all four (local text extraction; 22 / 26 / 14 / 3 pages)
- **Annotation:** Free-standing, freely available companions to R78–R80 that carry the
  detail a model builder needs and can be quoted more comfortably than the manual.
  **IP 51** is the source for the **mean-reserve / mid-terminal** mechanics and the
  **deferred premium asset**: under the mean reserve method the policy reserve is the
  average of the terminal reserve and the initial reserve (prior terminal plus the current
  net annual valuation premium), assuming the whole annual net premium is collected at the
  start of the policy year and policies are issued ratably over the calendar year; because
  premiums arrive modally the reserve is overstated, so a **deferred premium** asset is set
  up equal to gross modal premiums from the next modal due date to the next anniversary,
  less those actually collected, less loading [R81/IP51 ¶21.a]. Under the mid-terminal
  method reserves are the average of the terminal reserves at the surrounding
  anniversaries plus an unearned premium reserve [¶21.b]. IP 51 ¶19 states CARVM in plain
  terms: "the difference between all possible future guaranteed benefits streams,
  including guaranteed nonforfeiture benefits, over the future considerations is computed
  as of the end of each contract year", discounted at the valuation interest rate, and the
  reserve is the **greatest** such present value. IP 51 ¶28 and IP 52 ¶17 enumerate the
  "additional reserves not included elsewhere" bucket (deficiency reserves; non-deduction
  of deferred fractional premiums / return of premium at death; excess of surrender values
  over reserves; substandard extras, group-conversion extra mortality, guaranteed
  insurability; asset-adequacy/CFT additions; conversion privileges and future contingent
  benefits). IP 51 ¶30 and IP 52 ¶19 give the **withdrawal-characteristics disclosure**
  taxonomy in full (with MVA / at book less current surrender charge where the charge is
  ≥5% and there is no meaningful bail-out / at market / at book without adjustment,
  sub-split by lump sum, instalments ≥5 years, instalments <5 years, fixed charge <5%,
  bail-out waiver where the bail-out rate exceeds the 20-year maximum statutory valuation
  rate for life; then "not subject to discretionary withdrawal", total gross, reinsurance
  ceded, total net). **IP 110** records the amendments that pulled Appendices A-200
  (group life separate accounts), A-695 (synthetic GICs) and A-830 (Model #830 nonlevel
  premium/benefit and secondary-guarantee reserves) into SSAP Nos. 51, 52 and 56, and
  states the effective date of January 1, 2001 with pre-2001 contracts on domiciliary-state
  law [R81/IP110 ¶10].

#### R82. SSAP No. 54 — Individual and Group Accident and Health Contracts (*As of March 2026*; historically 54R)
- **Publisher:** NAIC (in R73, statement pages 54-1 onward)
- **URL:** https://content.naic.org/sites/default/files/publication-app-manual.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; status block, ¶¶1–2 and full section index read)
- **Annotation:** Finalized March 13, 2000, **conceptually revised December 10, 2016**,
  conceptual revisions effective January 1, 2017; interpreted by INT 05-05 and INT 24-02;
  relevant Appendix A guidance A-010, A-225, A-641, A-820, A-822 [R82]. Scope is every
  contract SSAP No. 50 classifies as accident and health except credit A&H [¶1]. Premiums
  recognised gross when due but **no earlier than the effective date of coverage** [¶2].
  The section structure is what matters to this library: **policy reserves**, **additional
  reserves (premium deficiency reserves)**, **claim reserves**, reserve recognition,
  change in valuation basis, supplemental benefits, reserve adequacy, contracts subject to
  redetermination, and an **Exhibit A illustrating the interaction of SSAP No. 54 with
  A-010 and AG 51 (long-term care)** [R82]. For this library SSAP No. 54 bites only through
  A&H riders attached to life products (waiver of premium, disability income, accelerated
  benefits with a health trigger), which the annual statement requires to be reported on
  the *base contract's* line of business [R89].

#### R83. SSAP No. 56 — Separate Accounts (*As of March 2026*)
- **Publisher:** NAIC (in R73, statement pages 56-1 to 56-14)
- **URL:** https://content.naic.org/sites/default/files/publication-app-manual.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; ¶¶1–31 and the glossary read)
- **Annotation:** How variable and index-linked business splits across two balance sheets.
  ¶4: sales, underwriting, contract administration, premium collection, premium tax,
  claims and benefits are **general account** functions. ¶5: for separate account
  contracts classified as *life contracts*, premiums and considerations are income in the
  **general account** summary of operations and simultaneously a **transfer** to the
  separate account statement; separate account **charges** (investment management,
  administration, contract guarantees) and the separate account's net gain from operations
  are general account income; benefits and surrenders on separate-account life contracts,
  net transfers, commissions and premium taxes are general account expenses. ¶7:
  **a GMDB reserve on a variable annuity or variable life contract is held in the general
  account**, and any difference between the benefit paid and the separate account value is
  charged/credited to general account net gain from operations. ¶8: **separate account
  surplus may not become negative** — the general account funds any deficiency. ¶9:
  separate account surplus created by CRVM/CARVM is reported by the general account as an
  unsettled transfer. ¶10: seed money is separate account surplus until repatriated.
  **¶17–18 are the measurement rule and the reason this entry matters for RILA:** separate
  account assets are at **fair value** (SSAP No. 100) *except* the ¶18 categories, which
  are carried "as if the assets were held in the general account" (**book value**) — ¶18.a
  employer-plan fund accumulation GICs with a fixed rate that do not participate in
  portfolio experience, and **¶18.b, with state regulator approval, insulated or
  non-insulated contracts similar to general account contracts that do not pass all
  investment experience through, where the general account "may serve as an overall
  backstop or may provide an implied guarantee", naming pension risk transfer (PRT),
  bank-owned life insurance (BOLI) and *registered index-linked annuity (RILA)* contracts
  as expected examples** [R83 ¶18.b]. ¶¶19–22 govern asset transfers between accounts
  (sales for cash at fair value; for book-value separate accounts the purchaser takes the
  seller's BACV and the fair-value/BACV difference goes to IMR in the purchasing account
  so the two accounts' IMR nets to zero; non-cash transfers need domiciliary approval and
  are at fair value). ¶¶23–28 are the separate account **AVR/IMR** rules (see mechanics
  below). ¶¶29–31 mirror SSAP No. 51's reserve definition and add that where separate
  account contracts have guaranteed elements the liability basis must match the asset
  basis — A-820 valuation interest rates when assets are on a general-account basis,
  **current market-based rates when assets are at fair value** [R83 ¶30]. ¶45 **rejects**
  ASU 2018-12, ASU 2022-05 and SOP 03-1. Glossary defines *Guarantee*, *Insulation*,
  *Risk Charge* and *Total Maximum Guarantee* [R83].

#### R84. SAPWG Ref #2024-10 — SSAP No. 56 book-value separate accounts (December 2024 exposure)
- **Publisher:** NAIC Statutory Accounting Principles (E) Working Group
- **URL:** https://content.naic.org/sites/default/files/inline-files/24-10%20-%20SSAP%20No%2056%20-%20BV_0.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; 38 pages; Form A, staff analysis and both
  redline versions of the SSAP read)
- **Annotation:** The exposure draft that produced the adopted ¶18.b at R83, exposed
  December 17, 2024 with comments due January 31, 2025. Records **why** RILA/PRT/BOLI were
  named: ACLI comments asked to delete the reference to the general account providing
  benefits "not directly tied to the performance of the underlying assets", and staff
  replaced it with the backstop/implied-guarantee language while keeping the examples and
  adding BOLI [R84]. It also carries the open regulator questions that a model builder
  should know are unsettled: whether the glossary definition of *Guarantee* captures the
  implied general-account backstop at all, and whether additional IMR guidance is needed
  for non-cash inter-account transfers [R84]. Useful as the audit trail for why a RILA can
  legitimately sit in a **book-value** separate account rather than a fair-value one.

### D. AVR, IMR and negative IMR

#### R85. SSAP No. 7 — Asset Valuation Reserve and Interest Maintenance Reserve (*As of March 2026*)
- **Publisher:** NAIC (in R73, statement pages 7-1 to 7-2)
- **URL:** https://content.naic.org/sites/default/files/publication-app-manual.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; ¶¶1–4 read in full — the statement is two pages)
- **Annotation:** Deliberately thin, and that thinness is the point: SSAP No. 7 states
  the *principle* and delegates the *arithmetic*. ¶1 scopes it to life and A&H insurers,
  **excluding separate accounts** (separate account AVR/IMR is in SSAP No. 56). ¶2: the
  **AVR** offsets "potential credit-related investment losses on all invested asset
  categories excluding cash, policy loans, premium notes, collateral notes and income
  receivable"; the **IMR** "defers recognition of the realized capital gains and losses
  resulting from changes in the general level of interest rates", amortised into
  **investment income** over "the expected remaining life of the investments sold", and
  also applies to certain **liability** gains/losses related to interest-rate changes,
  amortised over the expected remaining life of the liability released [R85 ¶2]. ¶3
  delegates calculation and reporting to the SSAP for the specific investment type or, if
  silent there, to the **NAIC Annual Statement Instructions** (R89). Effective January 1,
  2001; status block records **"Interpreted by … INT 23-01"** [R85].

#### R86. Statutory Issue Paper No. 7 — Asset Valuation Reserve and Interest Maintenance Reserve
- **Publisher:** NAIC (finalized March 16, 1998; AP&P Appendix E)
- **URL:** https://content.naic.org/sites/default/files/inline-files/007_G.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; 12 pages, read in full)
- **Annotation:** Free and far more detailed than SSAP No. 7 itself, because it reproduces
  the then-current AVR/IMR instruction text at length: the IMR roll-forward, the
  more-than-one-NAIC-designation credit test that separates IMR from AVR, the seriatim and
  grouped amortisation methods and the years-to-expected-maturity groupings, the
  **liability gains/losses** rules (the 5%-of-general-account-liabilities reinsurance
  threshold and the market-value-adjustment materiality test), the negative-IMR
  general/separate-account offset table with rules a–f, and the AVR's two components and
  four sub-components with the annual-contribution formula and the historic 20%
  contribution rate [R86]. It also states the purpose in the terms a modeller needs: the
  IMR exists "to protect surplus from investment transactions that are entered into as a
  reaction to interest rate movements" and to reduce **gains-trading** opportunity [R86
  ¶7]; the AVR "provides a mechanism to absorb unrealized and credit-related realized
  gains and losses" [¶6]. ¶13: "AVR and IMR are not addressed in current GAAP literature",
  and the paper **rejects** FAS 97 ¶28 as amended by FAS 115 for life and A&H insurers
  [¶5]. **Caution:** the instruction text quoted here is 1990s vintage; the current
  factors, groupings and rules are at R89 and differ in detail (e.g. the grouped-method
  bands now begin with a separate "0 calendar years" band).

#### R87. INT 23-01 — Net Negative (Disallowed) Interest Maintenance Reserve (revised print, adopted August 11, 2025)
- **Publisher:** NAIC Statutory Accounting Principles (E) Working Group (AP&P Appendix B)
- **URL:** https://content.naic.org/sites/default/files/inline-files/22-19%20-%20INT%2023-01%20-%20Revised%20April%202025.pdf
  (original clean adoption print, August 13, 2023:
  https://content.naic.org/sites/default/files/inline-files/22-19a%20-%20INT%2023-01%20-%20IMR%20clean.pdf — also fetched)
- **Accessed:** 2026-08-04
- **Fetched:** yes, both (local text extraction; 8 pages each; the revised print carries
  visible tracked-change artefacts, which is how the extension is evidenced)
- **Annotation:** The interpretation that lets a life insurer **admit** net negative
  (disallowed) IMR, as a time-limited exception to SSAP No. 7 and the annual statement
  instructions. Dates discussed: April 10, June 28 and August 13, 2023; June 5 and August
  11, 2025 [R87]. Full conditions and reporting mechanics are in "Extracted mechanics"
  below. **Status as retrieved:** originally a short-term solution to December 31, 2025
  with automatic nullification January 1, 2026; on **August 11, 2025** the Working Group
  **extended it one year to December 31, 2026, with automatic nullification January 1,
  2027**, and added a second, current-period admittance limit in ¶9.a [R87 ¶14]. ¶15
  allows the date to move again in response to SAPWG action on permanent guidance.
  The single most model-relevant clause is ¶9.e, which requires an entity admitting
  negative IMR to **capture the admitted negative IMR in the PBR calculation or asset
  adequacy / cash flow testing under VM-20 §7.D.7 and VM-30 §3.B.5** and to prepare a
  reconciliation of admitted negative IMR to the IMR reflected for PBR/CFT "to ensure
  reserves are not overstated", with an optional NAIC template published as a VM-31
  template on the PBR web page [R87 ¶9.e].

#### R88. SAPWG 2026 Spring National Meeting — Meeting Summary Report (March 23, 2026)
- **Publisher:** NAIC Statutory Accounting Principles (E) Working Group
- **URL:** https://content.naic.org/sites/default/files/national_meeting/2026-spnm-summary-e-sapwg.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; 3 pages, read in full)
- **Annotation:** The currency check for everything in this stream, and the record that
  the negative-IMR question is still open. Adopted at that meeting: revisions to **SSAP
  Nos. 3, 51 and 52** giving "guidance on the optional implementation period for Valuation
  Manual revisions regarding the economic scenario generator and non-variable annuities"
  (Ref #2025-34) — directly relevant to GOES/VM-22 transition in a projection; **SSAP
  No. 7** "proposed concepts for an interest maintenance reserve (IMR) **proof of
  reinvestment**" from the IMR Ad Hoc Group (Ref #2025-23); and **SSAP No. 56** revisions
  on "nonadmittance for assets held under the 'general account basis' in the separate
  account" (Ref #2025-25) [R88]. Exposed for comment to May 1, 2026: **SSAP No. 52**
  disclosures and glossary for **funding agreement-backed notes (FABNs)** (Ref #2026-01);
  **SSAP No. 61** revisions requiring **funds withheld liabilities to equal the BACV of
  the funds withheld assets**, with Schedule S Parts 3/4/5 instruction changes (Ref
  #2026-02); and **a new SSAP and issue paper allowing an amortized cost measurement
  method for a qualifying derivative program** (Ref #2024-15). Status updates: on
  **February 24, 2026** the IMR Ad Hoc Group received an initial version of a **revised
  SSAP No. 7**, with the revised SSAP, a draft issue paper and reporting revisions
  expected to be exposed in the interim after the Spring meeting [R88]. Also records that
  SSAP No. 61 Ref #2025-22 is **deferred** pending a Reinsurance (E) Task Force decision
  on the symmetrical vs asymmetrical approach.

### E. The annual statement as the reporting target

#### R89. NAIC Annual Statement Instructions — Life, Accident & Health/Fraternal, 2025 reporting year
- **Publisher:** NAIC ("Adopted by the NAIC as of June 2025"; free download from the NAIC
  Resource Center)
- **URL:** https://content.naic.org/sites/default/files/publication-asi-lua-25.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; 1,008 pages; Analysis of Operations pp. 84–96,
  Exhibits 5 / 5A / 6 / 7 pp. 143–157, Exhibit of Life Insurance p. 383, IMR pp. 390–404,
  AVR pp. 405–428 read)
- **Annotation:** The operative rulebook for *what the model must output and at what
  granularity*. It is the source of the Exhibit 5 valuation-standard abbreviation set
  (including **VM-20NPR**, **VM-20 DET/STO** and **VM-22**), the requirement that VM-20
  business be reported with the net premium reserve and the excess over it **on separate
  lines**, the requirement that VM-22 annuity business be split **Jumbo / Non-Jumbo in
  50-basis-point valuation interest bands**, the Exhibit 5 footnote (a) rule on
  originally-life-contingent contracts, the Exhibit 7 column taxonomy for deposit-type
  contracts, the Analysis of Operations line-of-business rules, and the complete IMR and
  AVR calculation instructions including the excess-withdrawal exemption. All of these are
  detailed in "Extracted mechanics" below.

#### R90. NAIC Annual Statement Blank — Life, Accident & Health/Fraternal, 2025
- **Publisher:** NAIC (free download)
- **URL:** https://content.naic.org/sites/default/files/publication-asb-life.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; 211 pages; Liabilities page, Summary of
  Operations p. 13, Cash Flow p. 14, Analysis of Operations by LOB pp. 15–20, Analysis of
  Increase in Reserves pp. 21–24, Exhibits 5–7 pp. 29–32, Exhibit of Life Insurance
  pp. 52–53, IMR form p. 55, AVR forms pp. 56–63 read)
- **Annotation:** The blank gives the **column and line vocabulary** a projection must
  produce, which the instructions describe but do not lay out. Individual Life Analysis of
  Operations columns: Total, Industrial Life, **Whole Life, Term Life, Indexed Life,
  Universal Life, Universal Life With Secondary Guarantees, Variable Life, Variable
  Universal Life**, Credit Life, Other Individual Life, YRT Mortality Risk Only. Individual
  Annuities columns: Total, then Deferred — **Fixed Annuities, Indexed Annuities, Variable
  Annuities with Guarantees, Variable Annuities Without Guarantees** — plus **Life
  Contingent Payout (Immediate and Annuitizations)** and Other Annuities. This is very
  nearly a one-to-one map onto the twelve products in this library and should drive the
  model's reporting dimension. The blank also fixes the Summary of Operations line
  sequence (premiums; considerations for supplementary contracts with life contingencies;
  net investment income; **amortization of IMR**; separate accounts net gain from
  operations; commissions and expense allowances on reinsurance ceded; reserve adjustments
  on reinsurance ceded; miscellaneous income including **charges and fees for deposit-type
  contracts**; then death benefits, matured endowments, annuity benefits, disability and
  A&H benefits, coupons/pure endowments, **surrender benefits and withdrawals**, group
  conversions, **interest and adjustments on contract or deposit-type contract funds**,
  payments on supplementary contracts with life contingencies, **increase in aggregate
  reserves**; then commissions, general insurance expenses, insurance taxes/licences/fees,
  **increase in loading on deferred and uncollected premiums**, **net transfers to or from
  separate accounts**, write-ins; net gain from operations before dividends; dividends;
  before FIT; FIT incurred; net gain after tax) and the **Analysis of Increase in Reserves
  During the Year** roll-forward (see mechanics). The IMR form is a 30-year amortisation
  grid plus a "and later" row, with the balance-sheet line at **Page 3, Line 9.4** and the
  AVR at **Page 3, Line 24.01**.

### F. Liabilities, contingencies, and the general recognition rule

#### R91. SSAP No. 5 — Liabilities, Contingencies and Impairments of Assets, with Statutory Issue Paper No. 5 (*As of March 2026*; historically SSAP No. 5R)
- **Publisher:** NAIC (SSAP in R73, statement pages 5-1 onward; issue paper in Appendix E)
- **URLs:** https://content.naic.org/sites/default/files/publication-app-manual.pdf ;
  Issue Paper No. 5: https://content.naic.org/sites/default/files/inline-files/005_J.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes, both (local text extraction; issue paper 8 pages read in full)
- **Annotation:** The statement SSAP No. 71 ¶2 points to for **when** an acquisition cost
  is incurred, and the statement SSAP Nos. 51/52/56 point to for the assertion that a
  policy reserve **is** a liability. A liability is "certain or probable future sacrifices
  of economic benefits arising from present obligations … to transfer assets or to provide
  services … as a result of past transaction(s) or event(s)", with three characteristics —
  present duty, little or no discretion to avoid, obligating event already happened — and
  "**Liabilities shall be recorded on a Company's financial statements when incurred**"
  [R91/IP5 ¶2]. Critically for actuarial output: "estimates of losses utilizing appropriate
  actuarial methodologies meet the definition of liabilities … and are **not** loss
  contingencies" [R91/IP5 ¶3]. The loss-contingency thresholds (probable / reasonably
  possible / remote; accrue when probable **and** reasonably estimable) are at ¶¶4–6, and
  ¶7 makes the accrual mandatory "even though the application of other prescribed statutory
  accounting principles or valuation criteria may not require, or does not address" it —
  the hook for reserves a formula does not otherwise produce. Note the FASB conceptual
  framework has since changed the definitions of asset and liability (Concepts Statement
  No. 8 Chapter 4, December 2021), which SAPWG reviewed under Ref #2022-01 and which fed
  Issue Papers 166 and 168 [R91b:
  https://content.naic.org/sites/default/files/inline-files/22-01%20Conceptual%20Framework.pdf,
  fetched].

### G. Reinsurance and credit for reinsurance (brief — this library models direct business)

#### R92. SSAP No. 61 — Life, Deposit-Type and Accident and Health Reinsurance (*As of March 2026*; historically 61R)
- **Publisher:** NAIC (in R73, statement pages 61-1 to 61-29 plus glossary)
- **URL:** https://content.naic.org/sites/default/files/publication-app-manual.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; ¶¶1–20, 36–38, 54–59 read; full section index read)
- **Annotation:** Scope is life, deposit-type and A&H contracts as classified by SSAP
  No. 50 [¶1]. ¶3: no reserve credit may be taken on business ceded to unauthorized or
  certified reinsurers except to the extent secured by trust, letter of credit, funds
  withheld or other acceptable collateral. ¶¶11–16 define the arrangement types
  (coinsurance, **modified coinsurance** — reserve credit reduced by the modco deposit —
  **YRT**, non-proportional). **¶17 is the risk-transfer gate:** an agreement that limits
  or diminishes risk transfer, or contains "any contractual feature that delays timely
  reimbursement", follows **Deposit Accounting** instead; ¶17.b requires multiple contracts
  to be evaluated **together** where consideration under one depends on performance of
  another and they "achieve one overall planned effect"; ¶17.c addresses combined
  YRT-plus-coinsurance structures with interdependent features — each leg satisfying risk
  transfer on its own basis is "necessary but not sufficient", and in aggregate the
  contract must not deprive the ceding insurer of surplus at the reinsurer's option,
  require payments other than income realized from the reinsured policies, or contain the
  **Appendix A-791** prohibited conditions. ¶19: YRT agreements qualify if they transfer a
  proportionate share of mortality/morbidity risk and avoid A-791 ¶¶2.b, 2.c, 2.d, 2.h,
  2.i, 2.j, 2.k, with income recognised **net of tax as gains emerge on mortality or
  morbidity experience**. ¶¶36–38 govern the **reserve credit**: computed with the same
  methodology and assumptions as the direct reserve, reported as a **reduction of reserves,
  not an asset**; YRT credit is the **one-year term mean reserve** on the amount ceded on
  the original policy's mortality and interest basis (pro rata allowed if not materially
  different); non-proportional credit only where the attachment point has actually been
  penetrated, or prospectively on a demonstrated PV(expected recoveries) > PV(guaranteed
  reinsurance premiums) test. ¶54 sends interest-related gain/loss on reinsuring a **block
  of liabilities** to the IMR per the annual statement instructions. ¶¶55–57: indemnity
  reinsurance gain/loss is net calendar-year experience including any IMR liability
  adjustment; **losses are recognised immediately**; initial-year gains on in-force blocks
  follow A-791 ¶3. ¶58 recaptures and commutations unwind through the original accounts
  with the required IMR adjustment.

#### R93. Statutory Issue Paper No. 74 — Life, Deposit-Type and Accident and Health Reinsurance
- **Publisher:** NAIC (AP&P Appendix E)
- **URL:** https://content.naic.org/sites/default/files/inline-files/074_p.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; 32 pages; risk-transfer, reserve-credit and IMR
  sections read)
- **Annotation:** Free companion to R92 with the fuller rationale, including the
  balance-sheet item lists each party must report (ceding: reserve credits, premiums
  payable, amounts recoverable on claims/surrender values/dividends/experience refunds/
  taxes/commissions, modco reserves, funds withheld; assuming: assumed reserves net of
  modco, premiums receivable, amounts payable, funds withheld) [R93]. It also reproduces
  **FAS 113 ¶¶12–13** — the GAAP long-duration risk-transfer test requiring "the reasonable
  possibility that the reinsurer may realize significant loss" — which is the natural
  contrast to the SAP A-791 condition list [R93].

#### R94. Credit for Reinsurance Model Law (#785)
- **Publisher:** NAIC (Model Laws, Regulations, Guidelines and Other Resources — Summer 2019)
- **URL:** https://content.naic.org/sites/default/files/model-law-785.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; 18 pages; Sections 1–2 read, full table of
  contents read)
- **Annotation:** The statute that decides whether a cession produces a reserve credit at
  all. Section 2 allows credit only where the assuming insurer is (A) licensed in the
  state, (B) **accredited** (submission to jurisdiction, examination authority, licensed in
  at least one state, annual filings, and surplus of not less than **$20,000,000** as the
  deemed-adequate-capacity test), (C) domiciled in a substantially-similar state with
  surplus not less than $20,000,000, (D) maintaining trust funds, (E) **certified**, (F)
  domiciled in a **reciprocal jurisdiction**, or (G) otherwise; Section 3 gives the
  asset-or-reduction-from-liability route for non-qualifying reinsurers [R94]. The 2019
  revisions implement the U.S.–EU and U.S.–UK Covered Agreements. A drafting note records
  the added commissioner authority over "the valuation of assets or reserve credits" and
  security for reserve-financing arrangements, aimed at life/health captives — the hook
  through which Model #787 (R12) operates [R94].

#### R95. Credit for Reinsurance Model Regulation (#786)
- **Publisher:** NAIC (Model Laws, Regulations, Guidelines and Other Resources — Summer 2019)
- **URL:** https://content.naic.org/sites/default/files/model-law-786.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; 46 pages; table of contents and Sections 1–4 read)
- **Annotation:** The procedural companion to R94: Sections 4–10 set out credit by
  reinsurer status (licensed, accredited, another state, trust funds, **certified**,
  **reciprocal jurisdiction**, required by law); Section 11 the asset-or-reduction-from-
  liability route; Sections 12–14 the qualifying **trust agreements**, **letters of
  credit** and other security; Section 15 the reinsurance contract requirements; and Forms
  AR-1, CR-1, RJ-1, CR-F and CR-S [R95]. For this library it matters only as the rule that
  determines whether the ceded column in Exhibit 5 / Schedule S can be taken.

### H. Derivatives and income taxes

#### R96. SSAP No. 86 — Derivatives (*As of March 2026*)
- **Publisher:** NAIC (in R73, statement pages 86-1 onward, with Exhibits A–C)
- **URL:** https://content.naic.org/sites/default/files/publication-app-manual.pdf
  (an older standalone print of the statement, "SSAP No. 86 — Accounting for Derivative
  Instruments and Hedging Activities", is hosted by the CFTC as part of an NAIC Dodd-Frank
  submission and was also fetched:
  https://www.cftc.gov/sites/default/files/idc/groups/public/@swaps/documents/dfsubmission/dfsubmission21_110910-naic7.pdf)
- **Accessed:** 2026-08-04
- **Fetched:** yes, both (local text extraction; scope and definitions, hedge-designation,
  fair-value-hedge, cash-flow-hedge, effectiveness, income-generation and replication
  sections read; hedge-accounting measurement paragraphs read in both prints)
- **Annotation:** The statement that decides whether the option budget backing an IUL,
  FIA or RILA index credit — or the macro hedge backing a VA guarantee — shows up as
  balance-sheet noise or as a matched item. Built on "selected concepts" of FAS 133 [¶1].
  **Measurement rule:** derivatives in hedging transactions that meet the highly-effective
  criteria "shall be considered an effective hedge and valued and reported in a manner that
  is consistent with the hedged asset or liability (referred to as hedge accounting)"; a
  derivative that does not meet, or ceases to meet, those criteria is **at fair value with
  changes to unrealized gains/losses** [R96 ¶15 (2010 print numbering)]. **No
  bifurcation** — a derivative is either an effective hedge or not [¶16], and hedge
  accounting is discontinued prospectively on failure of any criterion, expiry/sale/
  termination/exercise, removal of designation, or impairment. On termination of a
  qualifying hedge the gain or loss adjusts the basis of the hedged item and is recognised
  consistently with it — "alternatively, **if the item being hedged is subject to IMR, the
  gain or loss on the hedging derivative may be realized and shall be subject to IMR upon
  termination**", applied consistently thereafter [¶17]. **Highly effective** means the
  change in fair value (or in cash flows / PV of cash flows for a cash flow hedge) of the
  derivative is within **80% to 125%** of the opposite change in the hedged item, or an
  **R² of 0.80 or higher** under regression; effectiveness must be assessed whenever
  financial statements or earnings are reported and **at least every three months**
  [¶¶19–20]. Exhibits A and B give the effectiveness discussion and assessment guidance;
  Exhibit C the specific hedge accounting procedures. **Open project:** a new SSAP and
  issue paper permitting an **amortized cost measurement method for a qualifying
  derivative program** — targeted at interest-rate ALM/macro hedges that fail SSAP No. 86
  effectiveness — was exposed by SAPWG in March 2026 (Ref #2024-15) [R88]; until adopted,
  ALM macro hedges sit at fair value through unrealized gains/losses.

#### R97. SSAP No. 101 — Income Taxes (*As of March 2026*)
- **Publisher:** NAIC (in R73, statement pages 101-1 onward, with Exhibit A Q&A)
- **URL:** https://content.naic.org/sites/default/files/publication-app-manual.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; status block, ¶¶1–2 and the full admissibility
  section ¶¶11–12 including all three Realization Threshold Limitation Tables read)
- **Annotation:** Issued August 31, 2011, effective **January 1, 2012**, superseding SSAP
  Nos. 10 and 10R; interpreted by INT 01-18, 06-12, 18-03, 22-02 and 23-03 [R97]. Adopts
  FAS 109 with modifications for state income taxes, the **realization criteria for
  deferred tax assets**, and the recording of changes in deferred tax balances [¶2]. The
  **admittance test** is at ¶11: net admitted DTA may not exceed adjusted gross DTA over
  gross DTL, and adjusted gross DTAs are admitted as the sum of three components — see
  "Extracted mechanics" for the full test and the RBC table. The clause that matters most
  for a **life** insurer: footnote 8 records that under the Internal Revenue Code entities
  taxed as life insurance companies **may not carry back ordinary losses arising in tax
  years after 2017**, so admittance of ordinary DTAs for such entities is limited to
  components 11.b and 11.c for reporting periods ending on and after December 31, 2017
  [R97 ¶11 fn.8].

#### R98. "NAIC Adopts SSAP No. 101—Income Taxes", *Taxing Times* Vol. 8 Iss. 1 (February 2012)
- **Publisher:** Society of Actuaries, Taxation Section (authors Richard Burness and
  Steven Sutcliffe, Deloitte Tax LLP)
- **URL:** https://www.soa.org/globalassets/assets/library/newsletters/taxing-times/2012/february/tax-2012-vol8-iss1-burness.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; 5 pages, read in full)
- **Annotation:** **Secondary source** (practitioner article), retained because it
  independently reproduces all three Realization Threshold Limitation Tables and explains
  the transition from SSAP No. 10 / 10R — the one-year/10% versus three-year/15%
  election — that a model of an older in-force block may need to reproduce. It also
  records the SSAP No. 101 changes a projection's tax module should reflect: the statutory
  **valuation allowance** now reduces gross DTAs rather than being non-admitted; formal
  adoption of prudent-and-feasible **tax planning strategies**; the move of tax
  contingency reserves from a "probable" to a "**more likely than not**" threshold under
  SSAP No. 5; and repeal of the SSAP No. 10R requirement to hold the extra surplus as
  appropriated [R98]. Where R97 and R98 differ, R97 governs.

#### R99. NAIC "Statutory Accounting Principles" — insurance-topics briefing page
- **Publisher:** NAIC
- **URL:** https://content.naic.org/insurance-topics/statutory-accounting-principles
- **Accessed:** 2026-08-04
- **Fetched:** yes (HTML)
- **Annotation:** Short, citable framing for a product-documentation introduction: SAP
  "focuses on the balance sheet and an insurer's ability to meet its obligations" while
  U.S. GAAP "focuses more on providing information to investors"; the three concepts of
  conservatism, recognition and consistency; the AP&P Manual "sets a national framework
  for statutory accounting, but it does not override state laws", preserving **prescribed
  and permitted practices**; and SAPWG's maintenance role [R99]. Use R74 for anything
  requiring the authoritative wording.

---

## Extracted mechanics

Every statement below is tagged with the entry it was read from. Anything not so tagged
is marked **[unverified]**.

### 1. Why statutory earnings have a different shape from GAAP

- Statutory accounting is a **solvency** measurement basis; the balance sheet is primary
  and "the income statement is a secondary focus of statutory accounting" [R74 ¶35].
  GAAP's objective, by contrast, is matching revenues and expenses [R76 ¶8].
- Assets not usable to meet policyholder obligations are **non-admitted** — charged
  against surplus rather than carried [R74 ¶36]. Liabilities are recognised **when
  incurred** [R74 ¶37; R91/IP5 ¶2].
- "Accounting treatments which tend to defer expense recognition do not generally
  represent acceptable SAP treatment" [R74 ¶38]. This is the concept from which SSAP
  No. 71 follows.
- **Acquisition costs are expensed as incurred; there is no DAC asset** [R75 ¶2]. The
  consequence for a projection: **first-year statutory strain** — commission, underwriting
  and issue expense plus the initial reserve all hit surplus in the issue year against a
  single year's gross premium, and profit emerges later as the reserve releases. This is
  the single largest structural difference between a statutory and a GAAP earnings
  projection for the same cash flows [R75][R76].
- SSAP No. 71 **rejects** ASU 2018-12 (LDTI), ASU 2010-26, FAS 60, FAS 97 and SOP 05-1
  [R75 ¶6]; SSAP No. 56 rejects ASU 2018-12, ASU 2022-05 and SOP 03-1 [R83 ¶45]; Issue
  Paper No. 50 rejects FAS 60 and FAS 97 [R76 ¶9]; Issue Paper No. 7 rejects FAS 97 ¶28
  as amended by FAS 115 for life and A&H insurers [R86 ¶5]. **A statutory run may not
  reuse a GAAP DAC, EGP-based amortisation, LFPB or MRB measurement.**
- A GAAP pronouncement is not part of SAP until the NAIC specifically adopts it [R74 ¶27];
  the statutory hierarchy places SSAPs at Level 1 [R74 ¶42].
- **Anti-avoidance on commission timing:** a levelized commission arrangement funded by a
  third party is a funding agreement; the insurer must recognise a liability for the full
  unpaid principal and accrued interest, and the **full initial sales commission is
  recognised immediately**, because "the writing of an insurance contract is the event that
  obligates the insurer"; persistency-linked structures cannot recharacterise or delay this
  [R75 ¶¶4–5]. A persistency-based commission is accrued **based on experience to date**
  [R77].

### 2. Classification: life contract versus deposit-type contract

- Test: does the entity assume mortality or morbidity risk? Mortality/morbidity risk is
  present if the entity must make payments or forego required premiums **contingent upon
  death or disability, or upon continued survival in the case of annuity contracts**, of a
  specific individual or group [R80 ¶2].
- Contracts with **no** mortality, morbidity, health-cost or casualty risk that act
  exclusively as investment vehicles are **deposit-type contracts** [R78 ¶5].
- **The classification is made at inception and cannot change** [R78 ¶5].
- Deposit-type categories: supplemental contracts, lottery payouts, structured settlements,
  guaranteed interest contracts, income settlement options, dividend and coupon
  accumulations, **annuities certain**, premium and other deposit funds [R80 ¶5].
- **Consequence for a period-certain-only immediate annuity:** it is a deposit-type
  contract. Considerations received are **not premium income** — they go directly to a
  policy reserve account [R80 ¶6]; the reserve is the **PV of future guaranteed benefits at
  the valuation interest rate** [R80 ¶9]; credited interest is an **expense** in the
  summary of operations, and a payment that returns policyholder balance is **not** an
  expense [R80 ¶13]. It is reported in **Exhibit 7**, column 3 "Annuities Certain", not
  Exhibit 5, and its activity flows through the deposit-type lines of the Summary of
  Operations ("Charges and fees for deposit-type contracts"; "Interest and adjustments on
  contract or deposit-type contract funds"), not the premium line [R89][R90].
- **The reverse asymmetry is explicit and is a modelling trap.** Exhibit 5 footnote (a):
  a contract that carried a mortality risk **at issue** stays in Exhibit 5 even after the
  risk disappears. The instruction's own example is a supplemental contract providing a
  life-contingent payout with a certain period — "Because the contract was life-contingent
  at issue, it is reported in Exhibit 5 **and remains in Exhibit 5 after the death of the
  annuitant** as remaining guaranteed payments continue to the beneficiary". State
  departments may also approve or require a contract to be classified as a life contract
  [R89]. So a life-contingent SPIA with period certain is a **life contract** for its whole
  life, including the residual certain payments.
- Reserve for "all other" deposit-type contracts (premium and other deposit funds, dividend
  and matured coupon accumulations) is **accumulated amounts paid plus contractual income
  accumulation, less withdrawals and applicable surrender charges** [R80 ¶9].

### 3. Life contract income recognition and reserve mechanics

- Gross premium is the amount charged; net premium is computed on the reserve interest and
  mortality basis; the difference is **loading**, which "generally includes allowances for
  acquisition costs and other expenses" **and** the difference between pricing and
  valuation mortality/interest [R79 ¶¶2–4].
- Premium recognised **gross, when due**; single and flexible premiums when received; the
  contractual due date is set by the agreed billing procedure; recognition of premium income
  and the change in loading must be **consistent with the assumptions used in the reserve**
  [R79 ¶5].
- Deferred and uncollected premium: the change in gross deferred and uncollected premium is
  premium income, and the **change in loading is an expense** in the summary of operations,
  not a reduction of premium [R79 ¶11]. Uncollected premium less than 90 days past due is
  admitted [R79 ¶12].
- **Mean reserve method:** reserve = average of the terminal reserve at end of policy year
  and the initial reserve (prior terminal + current year net annual valuation premium);
  assumes annual net premium collected at the start of the policy year and issues spread
  ratably over the calendar year. Because premiums actually arrive modally, the reserve is
  overstated, so a **deferred premium asset** is set up: gross premiums from the modal due
  dates after the valuation date to the next anniversary, less those actually collected,
  less loading [R81/IP51 ¶21.a].
- **Mid-terminal method:** reserve = average of terminal reserves at the previous and next
  anniversaries, plus an unearned premium reserve for the portion of valuation premiums
  covering valuation date to next anniversary [R81/IP51 ¶21.b].
- **Advance premiums** (received before the valuation date but due on/after the next
  anniversary) are a **liability at the gross amount**, not premium income; any discount for
  early payment unwinds as interest in the summary of operations [R81/IP51 ¶22].
- **Change in valuation basis** — a change in interest, mortality, or reserving method (or,
  for deposit-type, interest or other factor) — goes **direct to surplus**, measured as the
  difference between old and new reserve **as of the beginning of the year**, and is **not
  graded in** unless an NAIC actuarial guideline prescribes a transition [R79 (Change in
  Valuation Basis section); R80 ¶14; R81/IP51 ¶24]. SSAP No. 52 ¶14 adds that a voluntary
  election between allowable Valuation Manual methodologies requiring commissioner approval
  is a change in valuation basis [R80 ¶14].
- **Accelerated benefits** that reduce the policy "shall not be deferred but shall be
  charged to the Summary of Operations as a benefit expense when paid" [R81/IP51 ¶27].
- **Additional reserves not included elsewhere:** deficiency reserves (valuation net
  premiums in excess of gross); non-deduction of deferred fractional premiums or return of
  premium at death; surrender values in excess of reserves otherwise carried; substandard
  extras, group-conversion extra mortality, guaranteed insurability; **additional reserves
  from cash flow testing / asset-liability matching**; conversion privileges and future
  contingent benefits [R81/IP51 ¶28; R80 ¶16].
- UL specifics: a flexible-premium UL "waiver of monthly deductions" benefit is neither
  revenue nor a benefit paid, and the deduction amount need not be computed [R79 ¶14].

### 4. Separate accounts — where a variable or index-linked liability sits

- General account keeps: sales, underwriting, contract administration, premium collection,
  premium taxes, claims and benefits [R83 ¶4].
- For separate-account **life contracts**: premium and considerations are **general account
  income** and simultaneously a transfer to the separate account; charges and the separate
  account net gain from operations are general account income; benefits, surrenders, net
  transfers, commissions and premium taxes are general account expenses [R83 ¶5].
  Deposit-type contracts in a separate account follow SSAP No. 52 in the general account
  [R83 ¶5].
- **GMDB reserves on VA and VL contracts are held in the general account**, and the
  difference between benefit paid and separate account value is charged/credited to general
  account net gain from operations [R83 ¶7].
- **Separate account surplus may not become negative**; a mortality deficiency on annuitized
  contracts is funded by a general account expense with matching separate account revenue,
  and mortality gains run the other way [R83 ¶8].
- CRVM/CARVM-generated separate account surplus is reported by the general account as an
  **unsettled transfer**, with the net change in net gain from operations [R83 ¶9].
- **Measurement:** separate account assets are at **fair value** except the ¶18 categories,
  which use **book value** (measured as if held in the general account, with general-account
  admissibility applied). ¶18.a: employer-plan fixed-rate fund accumulation GICs that do not
  participate in portfolio experience. **¶18.b: with state regulator approval, insulated or
  non-insulated contracts similar to general account contracts that do not pass all
  investment experience through, where the general account "may serve as an overall backstop
  or may provide an implied guarantee" — expressly including PRT, BOLI and RILA contracts**
  [R83 ¶¶17–18]. Anything else needs a permitted or prescribed practice.
- **Liability basis must follow asset basis** for separate account contracts with guaranteed
  elements: A-820 valuation interest rates when assets are on a general-account (book) basis;
  **current market-based interest rates when assets are at fair value** [R83 ¶30].
- **Inter-account asset transfers:** sales for cash occur at fair value. Selling from the
  general account produces a realized gain/loss versus BACV; if interest-related it goes to
  general account IMR and amortises as if sold to a third party, and **may not be deferred**
  under SSAP No. 25; credit-related losses go to AVR. Selling from a fair-value separate
  account produces no gain or loss. For **book-value** separate accounts the purchaser
  records the seller's BACV and the fair-value/BACV difference is reported to IMR in the
  purchasing account, so the two accounts' IMR movements are equal and offsetting and net to
  **zero** [R83 ¶¶19–21]. Non-cash transfers (asset swaps, contributions to cover separate
  account deficiencies, dividends of assets to the general account) require domiciliary
  approval, are recorded at fair value, and are separately disclosed [R83 ¶22].

### 5. AVR — what it absorbs and how it moves

- The AVR offsets **credit-related** (default) and equity investment losses on all invested
  asset categories **excluding cash, policy loans, premium notes, collateral notes and
  income receivable** [R85 ¶2].
- Two components, four sub-components: **Default Component** (bond and preferred stock
  sub-component, including derivative counterparty exposure; mortgage sub-component) and
  **Equity Component** (common stock; real estate and other invested assets) [R86 ¶11(B)].
- Movements are **charged or credited directly to surplus**, not through the summary of
  operations [R86 (Chapter 16B extract)].
- The IMR/AVR split for a bond turns on the **NAIC designation change over the holding
  period**: a realized gain/loss is **interest-related (IMR)** if the designation at end of
  holding period differs from the beginning designation by **one or less** NAIC designation;
  otherwise it is **credit-related (AVR)**; a security ever designated **"6"** during the
  holding period always goes to AVR [R89; R86]. The current instructions add an override:
  even within one designation, if there was an **acute credit event** between purchase and
  sale not yet reflected in CRP ratings or the SVO feed and the resulting gain/loss was
  predominantly credit-related, it is **excluded from IMR** [R89].
- Mortgage loans default to **AVR** if sold with an established SSAP No. 37 valuation
  allowance, or interest more than 90 days past due, or in foreclosure, or in course of
  voluntary conveyance, or restructured within the prior two years [R89].
- **OTTI bifurcation:** non-interest-related OTTI goes through AVR, interest-related OTTI
  through IMR, with the analysis performed **as of the date the OTTI is determined**;
  subsequent sales are bifurcated again as of the sale date, and prior AVR/IMR allocations
  are **not** adjusted [R89].
- **Derivatives:** for hedging derivatives the AVR/IMR allocation follows the treatment of
  the **underlying hedged asset**; portfolio/general hedges are included with the hedged
  asset; specific hedges only when the specific hedged asset is sold or disposed. For income
  generation transactions it follows the underlying interest (put) or covering asset (call,
  cap, floor) [R89].
- U.S. government and full-faith-and-credit agency securities are **exempt from AVR** [R89].
- **AVR roll-forward per sub-component** (annual statement form, general account): prior
  year balance; ± realized capital gains/losses net of tax (general account and separate
  accounts on separate lines); ± unrealized gains/losses net of deferred tax (SSAP No. 101
  basis), also split general/separate; **less capital gains credited or losses charged to
  contract benefits, payments or reserves** (an explicit anti-double-count line); **plus the
  basic contribution**; balance before transfers; ± **transfers**; plus **voluntary
  contribution**; **adjustment down to maximum / up to zero**; ending balance [R89][R90].
- **Accumulation formula:** the annual accumulation line is "**20% of (Reserve Objective −
  accumulated balance)**", positive when the objective exceeds the accumulated balance and
  negative when it is exceeded [R89, AVR Line 11].
- **Factor definitions:** the **basic contribution factor** produces, on average, an amount
  approximating expected annual losses; the **reserve objective factor** targets an
  accumulation covering, in the aggregate, **about 85% of the distribution of losses** for
  each asset category; the **maximum reserve factor** caps the accumulation [R89]. Factors
  are tabulated by NAIC designation (bonds, preferred stock, short-term, derivative
  counterparty exposure) and by mortgage category using the **Life RBC** classification
  methodology; the numeric factor tables were not transcribed here [R89].
- **Transfers:** an excess over a sub-component maximum must be transferred to its "sister"
  sub-component if that sister is below its maximum; excess over a whole component's maximum
  may be transferred to the other component or **released to surplus**; a negative
  sub-component balance is transferred to its sister only to the extent the transfer does not
  reduce the sister's positive pre-transfer balance below **50%**. No other transfers without
  commissioner approval, and **no transfers between AVR and IMR** [R89].
- Each sub-component is floored at **zero** and capped at its maximum [R89]. Voluntary
  contributions are permanent [R86; R89]. Affiliated life insurers maintaining their own AVR
  carry a **0% maximum reserve factor**, so their unrealized gains/losses are excluded [R89].
- Balance sheet line: **Page 3, Line 24.01** [R89].

### 6. IMR — the amortisation that a statutory income projection must carry

- The IMR "defers recognition of the realized capital gains and losses resulting from changes
  in the general level of interest rates", amortised into **investment income** over the
  expected remaining life of the investments sold; and applies to certain **liability**
  gains/losses from interest-rate changes, amortised over the expected remaining life of the
  **liability released** [R85 ¶2].
- Purpose, in the codifiers' words: "to protect surplus from investment transactions that are
  entered into as a reaction to interest rate movements", minimising the effect of
  interest-driven realized gains and losses on current-year operations, and reducing
  **gains-trading** opportunity [R86 ¶7].
- **Annual statement IMR form** [R90]:
  1. Reserve as of December 31, prior year
  2. + current year's realized **pre-tax** capital gains/(losses) transferred into the
     reserve **net of taxes**
  3. ± adjustment for current year's **liability** gains/(losses) released from the reserve
  4. = balance before reduction (1+2+3)
  5. − current year's **amortization released to Summary of Operations**
  6. = reserve as of December 31, current year
  The supporting Amortization schedule is a grid by year of amortisation running **30 future
  calendar years plus an "and later" row**, with columns for prior-year reserve, current-year
  gains transferred, liability adjustment, and balance before current-year amortisation
  [R90].
- The amortisation is reported on **Summary of Operations Line 4, "Amortization of Interest
  Maintenance Reserve (IMR)"**, and is allocated by line of business in the Analysis of
  Operations (Line 4 in every LOB page) [R90].
- Balance sheet line: **Page 3, Line 9.4** (general account) and Line 3 (separate accounts)
  [R89].
- **What goes in:** interest-rate-related realized gains/losses on fixed income investments,
  net of capital gains tax. Excluded: non-interest (default) realized gains/losses, realized
  gains/losses on equity investments, and all unrealized gains/losses. A realized gain/loss
  must be classified as **either** interest (IMR) **or** non-interest (AVR), not a
  combination, "except as specified in SSAP No. 43—Asset-Backed Securities". Purchase lots
  with the same CUSIP are treated as individual assets for IMR/AVR purposes [R89].
- **Anti-double-count exclusion:** capital gains and losses that, per contract terms, have
  been used to directly increase or decrease **contract benefit payments or reserves** during
  the period are excluded from IMR [R89].
- Capital gains tax is allocated by the company's own statutory tax-allocation method, and
  the tax attached to a gain amortises **in proportion to the pre-tax amortisation** [R89].
- **Two amortisation methods**, and once selected for a given year's gains the amortisation is
  **locked in** and cannot be changed without commissioner approval [R89]:
  - **Seriatim:** for each gain/loss, the annual amortisation is the excess of the income that
    would have been reported had the asset **not** been disposed of, over the income that
    would have been reported had the asset been **repurchased at its sale price**. For
    MBS/ABS, use an amortisation schedule built on anticipated future cash flows consistent
    with the prepayment assumptions that would have been used had the security been purchased
    at its sale price [R89].
  - **Grouped:** gains/losses net of tax are grouped by **calendar years to expected
    maturity** — 0, 1, 2–5, 6–10, 11–15, 16–20, 21–25, over 25 — and multiplied by the
    published amortisation factors for the year of sale. "Calendar years to expected maturity"
    = calendar year of maturity − calendar year of sale. **Each year's gains use that year's
    published table** for all future years; current-year gains use the prior year's factors
    until the current table is published [R89].
- **Expected maturity date** rules: fixed-repayment instruments use the contractual
  retirement date producing the lowest amortisation value (**yield to worst**) across all call
  dates and the maturity date; scheduled sinking funds add a yield-to-average-life calculation
  (average life = 50% repaid); **puttable** instruments use the put or maturity date producing
  the **highest** IRR; SVO Identified Funds designated for systematic value use the
  weighted-average life of the underlying bonds; **perpetuals use 30 years**. A callable bond
  bought at a premium and called or sold **after** the expected maturity date has **no**
  amortisation — the gain or loss is taken into income immediately; same for a convertible
  disposed of after its expected maturity date. Fixed income without a maturity date or
  sinking fund schedule uses **30 years**; MBS/ABS use remaining weighted average life on the
  repurchase-price prepayment assumptions [R89].
- **Liability gains/losses in IMR** [R86; R89; R92 ¶54]:
  - *Reinsurance:* the interest-rate-related gain/loss net of tax on the sale, transfer or
    reinsurance of a **block of liabilities** is credited/charged to IMR and amortised,
    provided the portion reinsured exceeds **5% of the company's general account liabilities**
    (Page 3, Line 26), the transaction is **irrevocable and to a non-affiliate**, and it
    completed in the current year. The amount is derived by identifying the IMR balance and
    future amortisation from past and present dispositions of the block's associated assets,
    plus the IMR balance and amortisation that would arise if the remaining associated assets
    were sold, and taking the **negative of the sum** [R86].
  - *Market value adjustments:* material gains/losses from **MVAs on policies and contracts
    backed by assets carried at book**, including the marginal tax impact, are captured by IMR
    and amortised in the same manner as fixed-income gains, on a schedule consistent with the
    determination of the associated MVA. Material = in excess of **both 0.01% of liabilities
    and $1,000,000** [R86].
- **Excess-withdrawal exemption from IMR** [R89]:
  - *Withdrawable reserves* = reserves/liabilities net of policy loans on any policy or
    contract subject to withdrawal or surrender **without an MVA** at the discretion of the
    contract holder or plan participant — expressly including ordinary and industrial life,
    **SPDAs**, and benefit-sensitive GICs.
  - *Effective withdrawals* = unscheduled withdrawals and surrenders calculated without market
    adjustment, plus the net increase in policy loans, plus cash transfers to separate accounts
    other than pass-through transfers of new premium.
  - *Withdrawal rate* = effective withdrawals for the calendar year ÷ withdrawable reserves at
    the beginning of the year.
  - *Threshold withdrawal level* = **150% × (lower of the withdrawal rate in the preceding or
    next preceding calendar year) × withdrawable reserves at the beginning of the year**.
  - *Excess withdrawal activity* = effective withdrawals − threshold withdrawal level.
  - Gains/losses on the investments required to fund excess withdrawal activity are **excluded
    from IMR and flow straight to net income** — identified specifically if possible, otherwise
    pro rata across the year's sales. Both withdrawable reserves and effective withdrawals are
    computed **net of reinsurance** [R89].
- **Separate account IMR:** an IMR is required for separate accounts whose assets are recorded
  at **book value**, and is **not** required where assets are at fair value — so traditional VA
  and VL separate accounts have none. The requirement is applied **account by account**: once
  required for an account, all of that account's investments are subject to it [R83 ¶¶26–27;
  R86; R89]. Separate account IMR is kept **separate** from general account IMR and reported
  in the separate account statement [R83 ¶27].
- **Separate account AVR:** required when the reporting entity, rather than the
  policyholder, suffers the loss on asset default or fair value loss — i.e. **not** required
  where the policyholder bears the risk directly, or where the regulatory authority for the
  separate account already provides an equivalent asset-default reserve. Traditional VA and VL
  separate accounts do not require an AVR **except for the seed money portion** (including
  accumulated earnings on it). **Book-value separate accounts, typical modified guaranteed
  contracts, MVA contracts and contracts with book-value guarantees do require an AVR** [R83
  ¶¶23–25]. Separate account AVR is **combined with the general account AVR** and reported in
  the general account financial statements [R83 ¶11].

### 7. Negative IMR — INT 23-01

Baseline rule (SSAP No. 7 and the annual statement instructions): a **positive** net IMR is a
liability on Page 3 Line 9.4; a **negative** net IMR ("disallowed IMR") is reported as a
miscellaneous other-than-invested write-in asset and **non-admitted**, with the change in the
disallowed portion charged or credited to the Capital and Surplus Account on Page 4, Line 41
[R87 ¶¶3–4; R89]. A negative balance in one statement is allowable as a negative liability only
to the extent covered by a positive IMR liability in the other statement, per the six-case
general/separate account table with rules a–f [R87 ¶4; R89].

INT 23-01 provides "limited-time, optional" exception guidance that overrides rules b, d and f
of that table [R87 ¶8]. Conditions and mechanics [R87 ¶¶9–13]:

- **¶9.a — admittance limit.** Admit net negative (disallowed) IMR up to **10% of the reporting
  entity's adjusted general account capital and surplus** shown on the statutory balance sheet
  of the **most recently filed statement** with the domiciliary commissioner. "Adjusted" means
  excluding **net positive goodwill, EDP equipment and operating system software, net deferred
  tax assets, and admitted net negative (disallowed) IMR**. General account capital and surplus
  already includes separate account surplus, so no aggregation is needed. The **August 2025
  revision adds a second cap**: admittance must also not exceed **10% of the current period
  unadjusted capital and surplus**, to guard against a decline in surplus or a large in-period
  increase in admitted negative IMR.
- **¶9.b — RBC gate.** The entity must have **RBC greater than 300% of Authorized Control
  Level** after adjusting Total Adjusted Capital to remove net positive goodwill, EDP
  equipment/operating system software, net DTAs and admitted net negative IMR. Compliance must
  be **affirmed for every quarterly and annual statement** in which admitted negative IMR is
  reported, with documentation on regulator request. At or below 300% ACL on the adjusted
  calculation, **no** admittance in the general account and **no** IMR asset in the separate
  accounts.
- **¶9.c — derivative symmetry.** Losses from derivatives that were reported at **fair value**
  prior to termination may be included only where the entity has **documented historical
  evidence** that unrealized **gains** from fair-value derivatives were reversed to IMR as a
  liability and amortised. Without that history, such derivative losses must be **removed**
  from the balance eligible for admittance. Starting a new symmetric process prospectively is
  not sufficient. Evidence is required **separately** for the general account, the insulated
  separate account and the non-insulated separate account.
- **¶9.d — disclosure condition.** An entity admitting any amount must **fully complete the
  data-captured disclosures** of ¶13 (or provide equivalent narrative); failure means it must
  **non-admit all** net negative IMR.
- **¶9.e — actuarial condition.** Admitted negative IMR must be **captured in the PBR
  calculation or in asset adequacy / cash flow testing under VM-20 §7.D.7 and VM-30 §3.B.5**,
  with a **reconciliation** of admitted negative IMR to the IMR reflected for PBR and CFT "to
  ensure reserves are not overstated"; an optional NAIC reconciliation template is published as
  a VM-31 template on the NAIC PBR web page.
- **¶10 — ordering.** Admit **all** general account net negative IMR first, up to the ¶9.a
  limit; only if the limit is not yet reached may the entity recognise an IMR **asset** in the
  separate accounts, allocated **proportionately** between insulated and non-insulated
  statements.
- **¶11 — general account reporting.** Report as an aggregate write-in to **miscellaneous
  other-than-invested assets, asset page line 25**, captioned "Admitted Disallowed IMR", with
  the remainder non-admitted; and allocate an equal amount from unassigned funds to an
  aggregate write-in for **special surplus funds, line 34**, same caption — explicitly "to
  preclude the ability for admitted negative IMR to be reported as funds available to
  dividend".
- **¶12 — separate account reporting.** Asset page **line 15** "Recognized Disallowed IMR", with
  an equal amount to special surplus funds **line 19**.
- **¶13 — disclosures.** (a) roll-forward of unamortised IMR balances arising from **fair-value
  derivative** gains and losses, shown separately for gains and losses; (b) note disclosure of
  total net negative IMR in aggregate and split general / insulated separate / non-insulated
  separate, amounts admitted or recognised in each, the calculated adjusted capital and surplus,
  and the **percentage** of adjusted capital and surplus admitted; (c) an attestation that the
  fixed income investments generating IMR losses comply with documented investment or liability
  management policies; that IMR losses on fixed-income derivatives follow prudent documented
  risk management and derivative use plans and reflect symmetry with historical gain treatment;
  that any deviation was temporary/transitory or event-driven (e.g. a reinsurance transaction);
  and that **asset sales generating admitted negative IMR were not compelled by liquidity
  pressures** (excess withdrawals, collateral calls).
- **Sunset.** Adopted August 13, 2023 as a short-term solution through December 31, 2025 with
  automatic nullification January 1, 2026; **extended on August 11, 2025 by one year to December
  31, 2026, with automatic nullification January 1, 2027**; the date may move again in response
  to SAPWG action on permanent guidance [R87 ¶¶14–15]. As of the 2026 Spring National Meeting a
  **revised SSAP No. 7** incorporating AVR/IMR guidance from the annual statement instructions
  was in drafting with the IMR Ad Hoc Group, with exposure expected after March 2026, and an
  "IMR proof of reinvestment" concept was adopted (Ref #2025-23) [R88].

### 8. The annual statement as the reporting target

**Exhibit 5 — Aggregate Reserves for Life Contracts** [R89][R90]

- Reserves are computed **gross** (direct plus reinsurance assumed), then a deduction for
  reinsurance ceded is computed **using the same mortality, interest and valuation method**
  but reflecting the actual mode of reinsurance. Because the assuming reinsurer may value
  differently, the ceded deduction need not equal the assumed reserve. **No deduction is taken
  for modified coinsurance.**
- **Column 1, Valuation Standard** must state the mortality/disability table, interest rate,
  valuation method and age basis **by years of issue**, and for annuities state whether
  immediate, deferred or both. The prescribed abbreviations include mortality tables from the
  American Experience Table through **2017 CSO** and **2012 IAR**; valuation methods **NLP,
  CRVM, NJ, ILL, CARVM, MOD**, and — the PBR-era additions — **VM-20NPR** (net premium reserve
  component), **VM-20 DET/STO** (deterministic/stochastic excess over NPR), and **VM-22** (any
  CARVM reserve using VM-22 valuation interest rates); age bases **ANB / ALB / (-1)**; and
  function codes **CRF, CNF, CP, IDB**. Worked example given: `2017 CSO VM-20 4% NPR … 2017`
  and `VM-20 DET/STO … 2017`.
- **Life insurance valued under VM-20 must be reported as two separate lines** — the Net
  Premium Reserve identifying its valuation basis, and the balance of the total required
  (excess over NPR).
- **Annuities valued using VM-22 valuation interest rates must be split into Jumbo and
  Non-Jumbo contracts on separate lines, in 50-basis-point valuation interest rate intervals.**
  Worked example: `2012 IAR VM-22 Jumbo 2% - 2.49%`, `… Jumbo 2.5% - 2.99%`, `… Non-Jumbo 2% -
  2.49%`, `… Non-Jumbo 2.5% - 2.99%`.
- **Miscellaneous Reserves** section carries: variable life minimum death benefit guarantee
  reserves; the excess of valuation net premiums over gross premiums (**deficiency reserves**);
  non-deduction of deferred fractional premiums or return of premium at death; surrender values
  in excess of reserves otherwise carried; and **additional actuarial reserves — asset/liability
  analysis**.
- Total (line 9999999) must agree with **Liabilities, Surplus and Other Funds page, Line 1**.
- Footnote (a) captures amounts in Exhibit 5 for deposit-type-like contracts that carried
  mortality risk at issue but no longer do (see §2 above).
- **Exhibit 5 Interrogatories** require, for participating business, an actuarial opinion on
  dividend determination including the **contribution principle**, investment-income allocation
  approach (portfolio average vs investment generation vs combination), and termination
  dividends; and, for **nonguaranteed elements** on individual life and annuity contracts
  (single/periodic premium deferred annuities, UL with fixed and/or flexible premiums,
  indeterminate premium life, single/periodic premium life, renewable and convertible term
  without guaranteed renewal premiums), an actuarial opinion covering NGE determination and
  redetermination. "Nonguaranteed" does **not** apply to charges or benefits that contractually
  follow a separate account result or a **defined index** [R89]. Interrogatories 7, 8 and 9
  define **synthetic GIC**, **Contingent Deferred Annuity**, and **Guaranteed Lifetime Income
  Benefit** for footnote disclosure.

**Exhibit 5A — Changes in Bases of Valuation During the Year** [R89]

- Captures the increase/(decrease) in reserves in Exhibits 5, 6 or 7 from valuation-basis
  changes applicable to contracts issued **before January 1 of the current year**, shown
  separately **by line of business**. The total is **excluded** from the income section of the
  Summary of Operations and of the Analysis of Operations by Line of Business. The Life
  Contract subtotal must agree with the **Analysis of Increase in Reserves During the Year**
  line "Increase in Reserve on Account of Change in Valuation Basis". Deposit-type changes flow
  from Exhibit 7.

**Exhibit 6 — Aggregate Reserves for Accident and Health Contracts** [R89]

- References SSAP No. 50 and **SSAP No. 54**. Line 2 **Additional Contract Reserves** must carry
  a reserve for any contract or block with level premiums, or where the gross premium structure
  at issue means the value of future benefits exceeds the value of appropriate future valuation
  net premiums. Line 3 is **Additional Actuarial Reserves — Asset/Liability Analysis**, which
  expressly includes **premium deficiency reserves**. Line 10 is the **present value of amounts
  not yet due on claims** (including unaccrued benefits on IBNR). Line 18 is **tabular fund
  interest**.

**Exhibit 7 — Deposit-Type Contracts** [R89]

- Captures activity before and after reinsurance for supplementary contracts without life
  contingencies, annuities certain, income settlement options, premium and deposit funds and
  other SSAP No. 52 contracts.
- Columns: 2 Guaranteed Interest Contracts; 3 **Annuities Certain** (amounts settled under
  contracts without any mortality or morbidity risk, "e.g., **certain immediate annuity
  contracts**", lottery payouts, structured settlements, income settlement options, or other
  fixed-period/fixed-amount payments); 4 Supplemental Contracts (without life contingencies);
  5 Dividend Accumulations or Refunds; 6 Premium and Other Deposit Funds.
- Line structure is a **fund roll-forward**: 1 balance at prior year end; 2 deposits received;
  3 investment earnings credited (method described in Notes to Financial Statements, Actuarial
  Reserve Note 32); 4 other net changes in reserves (the difference where the reserve held
  differs from the accumulated account balance, plus the Exhibit 5A line 0399999 amount, plus
  foreign currency adjustment); 5 fees and other charges assessed; 6 **surrender charges**;
  7 net surrender or withdrawal payments; … through to the ending balance, which ties to the
  liability page.

**Analysis of Operations by Lines of Business** [R89][R90]

- Summary page columns: Total, **Individual Life, Group Life, Individual Annuities, Group
  Annuities, Accident and Health**, Fraternal, Other Lines, **YRT Mortality Risk Only**.
- Individual Life detail columns: Total, Industrial Life, **Whole Life, Term Life, Indexed
  Life, Universal Life, Universal Life With Secondary Guarantees, Variable Life, Variable
  Universal Life**, Credit Life, Other Individual Life, YRT Mortality Risk Only. **Indexed Life
  excludes indexed UL with secondary guarantees, which goes in the ULSG column** [R89].
- Individual Annuities detail columns: Total; Deferred — **Fixed Annuities, Indexed Annuities,
  Variable Annuities with Guarantees, Variable Annuities Without Guarantees**; **Life Contingent
  Payout (Immediate and Annuitizations)**; Other Annuities [R90].
- Reporting must be **consistent with the policy type language in the product contract**.
  Policies issued with secondary guarantees that have since expired continue to be reported as
  ULSG [R89].
- **All separate account transactions transferred to or from the separate accounts statement on
  Line 26 must also be reported in the premium, benefit, withdrawal or other captioned lines of
  the Analysis of Operations**, and again in the separate accounts statement's own Analysis of
  Operations [R89].
- **Supplementary contracts with life contingencies are reported on the annuities pages;
  supplementary contracts without life contingencies go in Exhibit 7** [R89].
- Riders/endorsements/floaters: if the rider acts like a separate policy with its own premium,
  deductible and limit and benefits not tied to the underlying contract, it is reported on its
  own line of business; **otherwise on the base policy's line**. Incidental benefits (total and
  permanent disability including waiver of premium and disability income, accidental death,
  AD&D) go on the **base contract's** line [R89].
- Run-off blocks below **5% of premiums and 5% of reserve and loans liability** as of December
  31, 2019 may be grouped with material blocks, with a footnote naming the affected columns
  [R89].

**Analysis of Increase in Reserves During the Year** [R90]

By the same product columns as the Analysis of Operations, the reserve roll-forward is:
1 reserve at prior year end; 2 **tabular net premiums or considerations**; 3 present value of
disability claims incurred; 4 **tabular interest**; 5 **tabular less actual reserve released**;
6 increase in reserve on account of **change in valuation basis**; **6.1 change in excess of
VM-20 deterministic/stochastic reserve over net premium reserve**; 7 other increases (net);
8 totals; **9 tabular cost**; 10 reserves released by death; 11 reserves released by other
terminations (net); 12 annuity, supplementary contract and disability payments involving life
contingencies; 13 net transfers to or from separate accounts; 14 total deductions;
15 reserve at current year end; then **16 cash surrender value ending balance** and 17 amount
available for policy loans based on that CSV.

**Exhibit of Life Insurance** [R89][R90]

- Face-amount in-force roll-forward on an **incurred** basis: policies are issued when the first
  premium is paid and terminated as close as possible to the event rather than the cash payment.
  Line 1 in force end of prior year; 2 issued during year; 3 reinsurance assumed; 4 revived;
  5 increased (net); 7 dividend additions; then terminations (death, maturity, disability,
  expiry, surrender, lapse, conversion, decreased, reinsurance ceded) to line 21 in force end of
  year, plus a policy/certificate **count** section. For riders providing a level amount payable
  in instalments on death, the **commuted value** of the instalments is the amount of insurance.
  Amounts are reported in **thousands** [R89]. Variable life is included.

**Summary of Operations and balance sheet ties** [R89][R90]

- Summary of Operations line sequence is given at R90 above. Note in particular Line 4
  amortization of IMR; Line 8.2 charges and fees for deposit-type contracts; Line 17 interest
  and adjustments on contract or deposit-type contract funds; Line 19 increase in aggregate
  reserves; Line 25 increase in loading on deferred and uncollected premiums; Line 26 net
  transfers to or from separate accounts net of reinsurance.
- Key ties: Exhibit 5 total → Liabilities page Line 1; Exhibit 6 Line 17 Col.1 less Line 5 →
  Liabilities page Line 2; IMR → Page 3 Line 9.4; AVR → Page 3 Line 24.01; change in
  non-admitted disallowed IMR → Page 4 Line 41 [R89][R87].
- Separately, the **Cash Flow** statement requires premiums collected net of reinsurance,
  benefit and loss related payments, **net transfers to separate accounts**, commissions and
  expenses paid, dividends paid and federal income taxes paid — i.e. a **cash** view distinct
  from the accrual Summary of Operations [R90].

### 9. Reinsurance — how ceded business enters the liability model

- Reserves in Exhibit 5 are computed **gross** and a **ceded deduction** computed on the same
  assumptions and method, reflecting the actual mode of reinsurance; **no deduction for modco**
  [R89].
- The ceding entity's reserve credit is **a reduction of reserves, not an asset** [R92 ¶37].
  Modco reserve credit is reduced by the modco deposit retained [R92 ¶14, ¶36]. **YRT** reserve
  credit and the assuming entity's reserve are the **one-year term mean reserve** on the amount
  ceded, on the **original policy's** mortality and interest basis (pro rata permitted if not
  materially different) [R92 ¶37].
- **Risk transfer** must be present or the arrangement is deposit-accounted; any feature that
  delays timely reimbursement violates the conditions; multiple contracts achieving "one overall
  planned effect" are evaluated together; combined YRT-and-coinsurance structures with
  interdependent features must in aggregate avoid depriving the ceding insurer of surplus at the
  reinsurer's option, requiring payments other than income realized from the reinsured policies,
  or the Appendix A-791 prohibited conditions [R92 ¶17]. YRT has its own reduced condition list
  (A-791 ¶¶2.b, 2.c, 2.d, 2.h, 2.i, 2.j, 2.k) and recognises income **net of tax as mortality or
  morbidity gains emerge** [R92 ¶19].
- No reserve credit is available on cessions to unauthorized or certified reinsurers except to
  the extent secured by trust, letter of credit, funds withheld or other acceptable collateral
  [R92 ¶3], and credit at all requires the assuming insurer to satisfy Model #785 Section 2
  (licensed / accredited with ≥$20,000,000 surplus / substantially-similar state / trust /
  certified / reciprocal jurisdiction) or the Section 3 asset-or-reduction route [R94][R95].
- **IMR interaction:** the interest-rate-related gain/loss net of tax on reinsuring a block of
  liabilities is credited/charged to IMR per the annual statement instructions [R92 ¶54], subject
  to the 5%-of-general-account-liabilities, irrevocable, non-affiliate, current-year conditions
  [R86]. Recaptures and commutations unwind through the original accounts with the required IMR
  adjustment, with net gain or loss in the summary of operations [R92 ¶58].
- Indemnity reinsurance gain/loss is **net calendar-year experience** including ceded premiums,
  claims, expense allowances, reserve adjustments, any IMR liability adjustment, and experience
  refunds/dividends; **losses recognised immediately**; initial-year gains on **in-force block**
  cessions follow Appendix A-791 ¶3 [R92 ¶¶55–57].
- **Pending:** SAPWG exposed revisions in March 2026 requiring **funds withheld liabilities to
  equal the BACV of the funds withheld assets**, with corresponding Schedule S Parts 3/4/5
  instruction changes (Ref #2026-02) [R88].

### 10. Income taxes and the DTA admittance test

- SSAP No. 101 adopts FAS 109 with modifications for state income taxes, DTA **realization
  criteria**, and the recording of changes in deferred tax balances [R97 ¶2].
- **Admittance test [R97 ¶11]:** net admitted DTA may not exceed adjusted gross DTA less gross
  DTL; adjusted gross DTAs are admitted as the **sum of three components**:
  - **11.a** — federal income taxes paid in prior years recoverable through **loss carrybacks**
    for existing temporary differences reversing within the IRS carryback window, **not to exceed
    three years**, including SSAP No. 5 amounts for those periods.
  - **11.b** — for an RBC filer, the **Realization Threshold Limitation Table – RBC Reporting
    Entities**, driven by the **ExDTA ACL RBC ratio**:

    | ExDTA ACL RBC | 11.b.i (realization years) | 11.b.ii (surplus limitation) |
    |---|---|---|
    | Greater than 300% | 3 years | 15% |
    | 200% – 300% | 1 year | 10% |
    | Less than 200% | 0 years | 0% |

    Admit adjusted gross DTAs (after 11.a) expected to be realized within the applicable period,
    limited to the applicable percentage of **statutory capital and surplus for the current
    reporting period as filed with the domiciliary commissioner, adjusted to exclude net DTAs,
    EDP equipment and operating system software, and net positive goodwill**. The **ExDTA ACL
    RBC ratio** is the December 31 RBC ratio based on Authorized Control Level RBC for the
    current reporting period being filed, computed **without net deferred tax assets**; interim
    quarters use current-quarter TAC ExDTA over the most recently filed annual ACL RBC [R97 ¶11
    fn.5]. Separate tables exist for financial/mortgage guaranty non-RBC filers (>115% / 100–115%
    / <100%) and other non-RBC filers (adjusted gross DTA ÷ adjusted capital and surplus: <50% /
    50–75% / >75%).
  - **11.c** — remaining adjusted gross DTAs offsettable against existing gross DTLs, respecting
    **character** (ordinary vs capital) as the tax return would permit, and considering reversal
    patterns without requiring scheduling beyond ¶7.e.
- **Life-company specific:** entities taxed as life insurance companies **cannot carry back
  ordinary losses arising in tax years after 2017**, so admittance of ordinary DTAs is confined
  to components 11.b and 11.c for periods ending on and after December 31, 2017 [R97 ¶11 fn.8].
  Capital losses remain carryback-eligible for three years for both life and non-life [R97 ¶11
  fn.4].
- Under SSAP No. 101 the statutory **valuation allowance reduces gross DTAs** rather than being
  non-admitted; prudent-and-feasible **tax planning strategies** are formally adopted; and tax
  contingency reserves use a **more-likely-than-not** (not "probable") threshold under SSAP
  No. 5 [R98].
- Deferred taxes on **unrealized** gains/losses feeding the AVR must be determined consistently
  with SSAP No. 101 [R89].

### 11. Derivatives — hedging index-linked and variable guarantees

- Effective hedges are "valued and reported in a manner that is consistent with the hedged asset
  or liability"; failed or discontinued hedges go to **fair value with changes through unrealized
  gains/losses** [R96 ¶15]. **No bifurcation** of effectiveness [R96 ¶16].
- Highly effective = derivative change within **80%–125%** of the opposite change in the hedged
  item (fair value or cash flows / PV of cash flows), or **R² ≥ 0.80** by regression; assessed
  whenever financial statements or earnings are reported and **at least quarterly**, consistently
  with the documented risk management strategy [R96 ¶¶19–20].
- On termination of a qualifying hedge, the gain/loss adjusts the basis of the hedged item and is
  recognised consistently with it; **alternatively, where the hedged item is subject to IMR, the
  derivative gain/loss may be realized and subjected to IMR upon termination**, applied
  consistently thereafter [R96 ¶17].
- AVR/IMR allocation of derivative gains/losses follows the **underlying hedged asset** (portfolio
  or general hedges with the hedged asset; specific hedges only when the specific asset is sold)
  or, for income generation, the underlying interest / covering asset [R89].
- **Consequence for indexed products:** where the option budget backing an IUL/FIA/RILA index
  credit is designated and documented as an effective hedge of the index-credit liability, the
  options can be carried consistently with that liability; where the programme is a macro/ALM
  hedge failing the 80–125% test, the derivatives sit at fair value through unrealized
  gains/losses and inject surplus volatility that a statutory projection must show. The
  SAPWG project to allow **amortized cost for a qualifying derivative program** under a Clearly
  Defined Hedging Strategy was still at exposure stage in March 2026 (Ref #2024-15) [R88].
- INT 23-01 ¶9.c bears directly on hedging programmes: derivative losses that were carried at
  fair value before termination may only be included in admitted negative IMR where the entity
  can evidence that it **historically reversed unrealized derivative gains into IMR** as well
  [R87 ¶9.c].

---

## Model hooks

What a liability cash flow projection model must produce for each accounting or capital item.

| Accounting / capital item | What the liability model must produce | Granularity / basis / timing |
|---|---|---|
| **Acquisition expense (SSAP No. 71)** [R75] | Commission, underwriting, policy-issue, medical/inspection cost **cash amounts in the period incurred**, with **no deferral and no DAC amortisation schedule**; separately, a persistency-linked commission accrual based on experience to date, and any levelized-commission funding liability at full unpaid principal plus accrued interest | Per policy per projection period, statutory basis, recognised in the issue period; must be a distinct output from any GAAP DAC stream so the two bases can be run off one cash flow engine |
| **First-year surplus strain** [R74][R75] | Statutory profit signature = gross premium − acquisition expense − maintenance expense − benefits − Δ reserve − Δ AVR − tax; a deliberately negative year-1 result for most products | Per policy / per model point per year; cumulative to a distributable-earnings pattern |
| **Contract classification (SSAP Nos. 50/52)** [R78][R80] | A per-contract flag `life_contract` vs `deposit_type`, **set at issue and immutable**, derived from whether any payment or premium waiver is contingent on death, disability or continued survival | Set once at inception; drives whether considerations are premium income or a direct credit to reserve, and whether Exhibit 5 or Exhibit 7 receives the balance |
| **Exhibit 5 reserve (life contracts)** [R89] | Reserve **gross of reinsurance**, plus a **ceded deduction** computed on the same mortality/interest/method reflecting the actual reinsurance mode; VM-20 business split into **NPR** and **excess over NPR**; VM-22 annuity business split **Jumbo/Non-Jumbo × 50bp valuation-interest band** | Aggregated by valuation standard **and year of issue**; year-end statutory valuation date; ties to Liabilities page Line 1 |
| **Exhibit 7 deposit-type roll-forward** [R89] | Opening fund balance; deposits received; **investment earnings credited**; other net changes in reserve where the reserve differs from the accumulated balance; fees and charges assessed; **surrender charges**; net surrender/withdrawal payments; closing balance | Per deposit-type column (GIC / annuities certain / supplemental / dividend accumulations / premium and deposit funds), annually, before and after reinsurance |
| **Analysis of Increase in Reserves** [R90] | **Tabular net premiums, tabular interest, tabular less actual reserve released, tabular cost, reserves released by death, reserves released by other terminations**, annuity/supplementary/disability payments with life contingencies, net separate account transfers, change in valuation basis, **change in excess of VM-20 DET/STO over NPR**, plus ending **CSV** | Per product column, per year; these are *reserve-basis* quantities, not experience quantities — the model must produce tabular (valuation-assumption) as well as actual movements |
| **Analysis of Operations by line of business** [R89][R90] | Every Summary of Operations line, decomposed by product column: Individual Life — whole life / term / indexed life / UL / **ULSG (including indexed UL with secondary guarantees)** / variable life / VUL; Individual Annuities — fixed deferred / indexed deferred / **VA with guarantees** / VA without guarantees / **life-contingent payout** / other | Annual, by product column; separate-account transfers must appear both in the captioned lines and on the transfer line |
| **Exhibit of Life Insurance** [R89] | Face amount in force roll-forward on an **incurred** basis — issued, revived, increased, dividend additions, and terminations by death / maturity / disability / expiry / surrender / lapse / conversion — plus policy counts; commuted value for instalment death benefits | Annual, in **thousands**, by ordinary / credit / group / industrial |
| **AVR** [R85][R86][R89] | Projected **credit-related** realized and unrealized gains/losses by asset sub-component net of tax; projected book/adjusted carrying value by NAIC designation and mortgage category to drive basic contribution, reserve objective and maximum; the anti-double-count amount of gains/losses credited to contract benefits or reserves | Sub-component level (bond & preferred incl. derivative counterparty; mortgage; common stock; real estate & other), annually; movement is **direct to surplus**, floored at zero, capped at maximum, with the 20%-of-shortfall accumulation |
| **IMR — asset leg** [R89][R90] | Projected **interest-related** realized gains/losses net of tax on each disposal, with an **expected maturity date** (yield-to-worst / put-highest-IRR / 30-year perpetual / WAL for MBS-ABS), fed into either a seriatim schedule or the grouped bands (0, 1, 2–5, 6–10, 11–15, 16–20, 21–25, >25 years) | Per disposal lot (same-CUSIP purchase lots treated separately), locked to the sale-year factor table; amortisation released annually to **Summary of Operations Line 4** and allocated by line of business |
| **IMR — liability leg** [R86][R89][R92] | Interest-related gain/loss net of tax on **block reinsurance** (only if >5% of general account liabilities, irrevocable, non-affiliate, current year) and on **market value adjustments** on book-value-backed contracts (material = >0.01% of liabilities **and** >$1,000,000), with an amortisation schedule consistent with the MVA determination or assets transferred | Per transaction; amortised over the expected remaining life of the **liability released** |
| **IMR excess-withdrawal exemption** [R89] | Projected **withdrawable reserves** (net of policy loans, on contracts surrenderable without MVA — ordinary/industrial life, SPDAs, benefit-sensitive GICs) and **effective withdrawals** (unscheduled withdrawals and surrenders without market adjustment, plus net policy loan increase, plus non-pass-through cash transfers to separate accounts), both **net of reinsurance** | Company aggregate, annual; drives the 150% × lower-of-prior-two-years threshold; gains/losses on sales funding the excess bypass IMR and go straight to net income |
| **Negative IMR admittance (INT 23-01)** [R87] | Projected net negative IMR by account (general / insulated separate / non-insulated separate); projected **adjusted capital and surplus** excluding goodwill, EDP/software, net DTAs and admitted negative IMR; projected **ExDTA-style adjusted RBC ratio**; the split of IMR attributable to **fair-value derivative** losses; and a **reconciliation of admitted negative IMR to the IMR reflected in the PBR / AAT / CFT model** | Quarterly and annually; the 10%-of-adjusted-surplus and 10%-of-current-unadjusted-surplus caps and the >300% ACL RBC gate must be tested each reporting date; the PBR/CFT tie-back is a **VM-20 §7.D.7 / VM-30 §3.B.5** model input, not just a disclosure |
| **Separate account split (SSAP No. 56)** [R83] | For VUL / VL / VA / RILA: separate account asset and reserve balances; general account **GMDB / guarantee reserves**; the **transfer** amounts to and from the separate account; separate account charges (M&E, admin, guarantee risk charges) as general account income; a non-negative separate account surplus constraint | Per contract per period; measurement basis flag **fair value vs book value** per ¶18 (RILA/PRT/BOLI eligible for book value with regulator approval), and liability discount basis must follow the asset basis |
| **Reinsurance ceded** [R89][R92] | Gross reserve and **ceded reserve credit on the same assumptions and method**; YRT credit as a **one-year term mean reserve** on the ceded amount at risk on the original basis; ceded premiums, allowances, reserve adjustments, claims recoveries; modco deposit; funds withheld | Per treaty per period; the ceded column must be produced separately, not netted, so Exhibit 5 and Schedule S can be filled |
| **Income tax / DTA** [R97] | Statutory reserve and tax reserve (IRC §807, R16) by period so temporary differences and their **reversal pattern and character** (ordinary vs capital) can be scheduled; projected statutory capital and surplus and projected **ExDTA ACL RBC ratio** | Annual, entity level; for a **life** entity, component 11.a is unavailable for ordinary DTAs post-2017, so the model must show admittance driven by 11.b (RBC band) and 11.c (DTL offset) |
| **Derivative hedge results** [R96] | Projected derivative fair values **and** the hedged-item measurement, so the 80%–125% (or R² ≥ 0.80) test can be evaluated at least quarterly; a designation flag per hedge relationship; termination gain/loss with an election flag for basis adjustment vs IMR | Per hedge relationship, at least quarterly; failure of the test flips the derivative to fair value through unrealized gains/losses, which the surplus projection must show |
| **Change in valuation basis** [R79][R80][R89] | The reserve under the old and the new basis **as of the beginning of the year**, by line of business | Annual; routed **direct to surplus** and **excluded** from the Summary of Operations and Analysis of Operations, and reported in Exhibit 5A |
| **Non-admitted assets** [R74] | Any projected asset not usable to meet policyholder obligations (e.g. over-90-day uncollected premium, disallowed IMR beyond the cap) | Charged against surplus rather than carried; the **change** flows through the Capital and Surplus Account, not net income |

---

## Product applicability

`x` = the item directly binds; `(x)` = qualified or conditional; blank = not indicated.

| Item [R#] | term | whole-life | universal-life | indexed-ul | variable-ul | guaranteed-ul | fixed-def-annuity | fixed-indexed-annuity | variable-annuity | RILA | immediate-annuity | deferred-income-annuity |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| AP&P Manual / Preamble [R73][R74] | x | x | x | x | x | x | x | x | x | x | x | x |
| SSAP No. 71 — no DAC [R75][R76][R77] | x | x | x | x | x | x | x | x | x | x | x | x |
| SSAP No. 50 classification [R78] | x | x | x | x | x | x | x | x | x | x | x | x |
| SSAP No. 51 — life contracts [R79][R81] | x | x | x | x | x | x | x | x | x | x | (x) | (x) |
| SSAP No. 52 — deposit-type [R80][R81] | | | | | | | (x) | (x) | (x) | (x) | **x** | **x** |
| SSAP No. 54 — A&H [R82] | (x) | (x) | (x) | (x) | (x) | (x) | | | | | | |
| SSAP No. 56 — separate accounts [R83][R84] | | | | | **x** | | | | **x** | **x** | | |
| SSAP No. 7 / AVR [R85][R86][R89] | x | x | x | x | (x) | x | x | x | (x) | x | x | x |
| SSAP No. 7 / IMR [R85][R86][R89] | x | x | x | x | (x) | x | **x** | **x** | (x) | **x** | **x** | **x** |
| INT 23-01 negative IMR [R87] | x | x | x | x | (x) | x | **x** | **x** | (x) | x | **x** | **x** |
| Exhibit 5 [R89][R90] | x | x | x | x | x | x | x | x | x | x | (x) | (x) |
| Exhibit 7 [R89] | | | | | | | (x) | (x) | (x) | (x) | **x** | **x** |
| Analysis of Operations by LOB [R89][R90] | x | x | x | x | x | x | x | x | x | x | x | x |
| Analysis of Increase in Reserves [R90] | x | x | x | x | x | x | x | x | x | x | x | x |
| Exhibit of Life Insurance [R89] | x | x | x | x | x | x | | | | | | |
| SSAP No. 5 liabilities [R91] | x | x | x | x | x | x | x | x | x | x | x | x |
| SSAP No. 61 / Models #785, #786 [R92]–[R95] | x | x | x | x | x | x | x | x | x | x | x | x |
| SSAP No. 86 derivatives [R96] | | (x) | (x) | **x** | (x) | (x) | (x) | **x** | **x** | **x** | (x) | (x) |
| SSAP No. 101 income taxes [R97][R98] | x | x | x | x | x | x | x | x | x | x | x | x |

**Notes on the matrix**

- **SSAP No. 52 and the immediate/deferred income annuities.** A **period-certain-only** SPIA or
  DIA is a deposit-type contract — considerations are not premium income, the reserve is PV of
  guaranteed benefits at the valuation rate, credited interest is an expense, and the balance sits
  in Exhibit 7 column 3 [R80][R89]. A **life-contingent** SPIA or DIA, including one with a period
  certain, is a life contract and stays in Exhibit 5 for its whole life, including after the
  annuitant's death while certain payments continue [R89, Exhibit 5 footnote (a)]. A deferred
  annuity's settlement options and dividend accumulations can also spawn deposit-type balances,
  hence the `(x)` marks on the deferred products.
- **SSAP No. 56 and RILA.** The March 2026 manual expressly names **registered index-linked
  annuity** contracts, alongside PRT and BOLI, as contracts expected to qualify for **book value**
  measurement in a separate account with regulator approval [R83 ¶18.b]. This is the accounting
  counterpart to AG 54 (R44) and Model #250 (R43) on the product side, and it means a RILA
  statutory model may need a **book-value separate account with its own AVR and IMR** — unlike a
  traditional VA separate account, which has neither (except AVR on seed money) [R83 ¶¶23–27].
- **IMR marks.** The IMR is emphasised for spread products (MYGA, FIA, RILA, SPIA, DIA) because
  their statutory income is investment-income-driven and asset turnover is the norm; the
  **market-value-adjustment** liability leg of IMR bites specifically on MVA-bearing MYGA and RILA
  designs [R86]. VUL/VA carry `(x)` because a fair-value separate account requires no IMR, but the
  general account backing the guarantees does [R83 ¶26].
- **SSAP No. 86.** Marked `x` where an option or swap programme is intrinsic to the product design
  — IUL, FIA, VA guarantee hedging, RILA — and `(x)` where derivatives appear only through general
  ALM.
- **SSAP No. 54.** Applies to this library only through A&H riders on life products (waiver of
  premium, disability income, health-triggered accelerated benefits), which the annual statement
  requires to be reported on the **base contract's** line of business [R89].
- **Exhibit of Life Insurance** is a face-amount exhibit and therefore does not apply to annuities;
  the parallel annuity exhibit is the "Exhibit of Number of Policies, Contracts, Certificates,
  Income Payable and Account Values in Force for Supplementary Contracts, Annuities, Accident and
  Health…" [R89].

---

## Gaps and caveats

**Corrections to assumptions the library currently carries**

1. **The AP&P Manual is free, not paid.** R33's annotation ("the manual itself is a paid
   publication and was not fetched") is factually superseded: the *As of March 2026* edition is a
   free download and was retrieved in full [R73]. The R35–R72 gaps section records AG 33 and AG 35
   as "the single largest hole in the annuity half" because "the authoritative text is in the AP&P
   Manual Appendix C (R33), a paid publication" — **that hole is now closable** from R73 Volume II.
   This note does not itself read AG 33 or AG 35; a follow-up pass should.
2. **SSAP "R" suffixes are gone.** The current manual prints SSAP Nos. 5, 51, 54 and 61 without the
   "R" [R73]. Citations in product documentation should use the unsuffixed numbers; the "R" forms
   remain correct only for pre-2024 material. The edition in which the change took effect was not
   identified [unverified].
3. **RILA is named in SSAP No. 56.** The adopted March 2026 text names RILA contracts as expected
   examples of book-value separate account business [R83 ¶18.b]. Any assumption that a RILA
   separate account must be at fair value is wrong.

**Verified but time-sensitive**

- **INT 23-01 sunsets on January 1, 2027** as currently written [R87 ¶14]. Any model or
  documentation relying on admitted negative IMR must carry the date. As of the 2026 Spring
  National Meeting the replacement — a substantially rewritten **SSAP No. 7** absorbing the
  AVR/IMR guidance from the annual statement instructions, with a supporting issue paper — was in
  drafting and expected to be exposed after March 2026 [R88]. **The exposed revised SSAP No. 7 was
  not located or read**; the SAPWG comment-letter compilation surfaced by search
  (`https://content.naic.org/sites/default/files/inline-files/imr-comment-letters-combined.pdf`
  and `…_2.pdf`, labelled "2026 Summer National Meeting Comment Letters Received") was **not
  fetched**. This is the largest open item in the stream and should be re-checked before the file
  is merged.
- **The 2026 Summer National Meeting had not been reported on** at the access date; the most
  recent SAPWG summary retrieved is the **March 23, 2026** Spring meeting [R88].
- **SSAP No. 61 funds-withheld revisions** (Ref #2026-02) and the **SSAP No. 52 FABN disclosures**
  (Ref #2026-01) were exposed with comments due May 1, 2026; adoption status unknown [R88].
- **The amortized-cost derivative-program SSAP** (Ref #2024-15) was at exposure in March 2026; if
  adopted it materially changes how ALM macro hedges affect projected statutory surplus [R88].
  The exposure documents themselves were **not fetched**; the description here rests on R88 plus
  search summaries, and the "Clearly Defined Hedging Strategy" phrasing is [unverified].

**Not retrieved / deliberately not asserted**

- **AVR factor tables.** The instructions describe the basic contribution, reserve objective (≈85%
  of the loss distribution) and maximum reserve factors and the pages on which they are tabulated,
  but the **numeric factors by NAIC designation and mortgage category were not transcribed** [R89].
  Any model needing them must read the AVR supporting forms in R89/R90 directly. No factor values
  are stated in this file.
- **IMR grouped amortisation factor tables** ("Table 1", Grouped Amortization Schedule) are
  published annually and change by year of sale; **no factor values are stated here** [R89].
- **SSAP No. 51 paragraphs 17 onward** (mean/mid-terminal, dividends, coupons, accelerated
  benefits, disclosures) were read through the section index and the **parallel Issue Paper No. 51
  text** rather than the SSAP paragraphs themselves; the substance is materially identical but
  paragraph numbers differ between IP 51 and SSAP No. 51 [R79][R81]. Where a product document needs
  a precise SSAP No. 51 paragraph cite, re-read R73 at statement pages 51-5 to 51-12.
- **SSAP No. 54** was read only at the status block, scope and premium-recognition paragraphs plus
  the section index; the premium-deficiency and claim-reserve mechanics were **not** read in detail
  [R82]. Adequate for this library's rider-only exposure; not adequate for an A&H product.
- **SSAP No. 86 Exhibits A, B and C** (effectiveness discussion, effectiveness assessment, specific
  hedge accounting procedures) were **not read**; the current-manual paragraph numbering for the
  hedging measurement rules was not cross-checked against the 2010 print, so the paragraph numbers
  quoted (¶¶15–20) are from the **2010 standalone print** and may differ in the March 2026 manual
  [R96].
- **Appendix A-791** (Life and Health Reinsurance Agreements — the prohibited-conditions list that
  SSAP No. 61 ¶¶17–19 turn on) was **not read**, only cited through SSAP No. 61 [R92]. It is in
  R73 Appendix A.
- **Model #786** was read at the table of contents and Sections 1–4 only; the trust, letter of
  credit and certified/reciprocal reinsurer mechanics were **not** read in detail [R95].
- **Notes to Financial Statements** — the withdrawal-characteristics disclosure appears in the 2025
  instructions around pages 344–356 under "Analysis of Annuity Actuarial Reserves and Deposit
  Liabilities by Withdrawal Characteristics"; the **note number** was not confirmed against the
  current instructions (Exhibit 7 line 3 references "Actuarial Reserve Note 32", and Exhibit 5
  references "Note 31" for valuation-basis overflow) [R89]. The disclosure **content** is verified
  from R81/IP51 ¶30 and R81/IP52 ¶19; the current note numbering is [unverified].
- **The 2025 vs 2026 annual statement year.** R89/R90 are the **2025 reporting year** instructions
  and blank (the 2026 blank was not separately retrieved). Line and page references above (Page 3
  Line 9.4 IMR, Page 3 Line 24.01 AVR, Page 4 Line 41, asset page lines 15/25, surplus lines 19/34)
  are as printed for 2025 and should be re-verified against the 2026 blank before being hard-coded.

**Fetch behaviour observed on 2026-08-04**

- content.naic.org served every PDF requested, but the fetch tool receives raw compressed streams;
  all NAIC PDFs above were downloaded and text-extracted locally. No NAIC 403s were encountered in
  this stream (contrast the R35–R72 note, where sec.gov, federalregister.gov, ecfr.gov and irs.gov
  blocked automated clients).
- soa.org and cftc.gov served PDFs normally.
- No URL on this page is fabricated; every URL listed was actually requested and its HTTP status
  observed.
