# Solvency UK — the Solvency Capital Requirement and the Standard Formula — research notes

**Stream:** The SCR and the standard formula (Solvency UK)
**Access date for every citation below:** 2026-08-06
**Status:** research notes, not yet merged into
`uk/references/regulatory-and-actuarial-references.md`

---

## Scope and numbering note

This stream owns reference block **R61–R76**. Entries **R1–R38** live in
`uk/references/regulatory-and-actuarial-references.md`, are **frozen**, and are already cited by
the seven UK product documents; nothing below renumbers, restates or duplicates them. Sibling
streams of this same effort own **R84–R98** (reporting, disclosure and governance,
`uk/_research/solvency-uk-reporting-governance.md`) and **R99–R113** (UK accounting and tax,
`uk/_research/uk-accounting-and-tax.md`); their entries are cited as `[R#]` and are not
re-created. New entries here are numbered sequentially from R61. Where a secondary document was
read under the same heading it takes a lettered sub-id (R62b, R63b, …) rather than consuming a
new number, following the convention already used in `us/_research/statutory-accounting.md`
(R74b) and in the sibling UK streams.

**R numbers used: R61–R73. R74, R75 and R76 are left unused by design**, per the library's
convention that a block may finish with spare numbers. They are headroom for the three documents
this stream identified as needed but could not read in substance: the SoP11/24 PDF [R70 is the
landing page only], SS5/15 *Solvency II: the treatment of pension scheme risk*, and SS20/16
*Solvency II: reinsurance – counterparty credit risk* — both of the latter being listed as related
guidance on the SCR Parts and not retrieved. Note that **R73 is deliberately assigned to a
document that was NOT retrieved** (the SCR-SF Annexes), so that the largest gap in this stream has
a citable handle; see Gaps §1.

**What this stream owns.** The *Solvency Capital Requirement – General Provisions* Part
(calibration, modular structure, frequency, capital add-ons, the standard-formula / USP /
internal-model relationship); the *Solvency Capital Requirement – Standard Formula* Part in full
(BSCR aggregation and every correlation matrix; life, health, market, counterparty default,
intangible and operational risk; risk-mitigation; the loss-absorbing-capacity adjustments; the
simplifications; the ring-fenced-fund and matching-adjustment-portfolio SCR treatment); the
*Undertaking Specific Parameters* Part; and the Bank of England symmetric-adjustment technical
information.

**Deliberately left to sibling streams.** Technical provisions, best estimate, contract
boundaries, risk margin and the matching adjustment *as such* are stream A/B — this file records
only how the SCR *consumes* them. The risk-free discount curve and the volatility adjustment are
stream B. **Own funds, the tiering and eligibility limits, the MCR, and internal models are
stream D** — the file references SCR-SF rules that point at the Own Funds Part but does not
specify own funds. Per-product application beyond the applicability matrix is stream F. The
LACDT tax mechanics are shared with the accounting/tax stream and are already numbered there as
**[R112]**; §14 below extends but does not replace that entry.

**Six retrieval facts that change how this material must be documented**

1. **This is no longer EU law with a UK gloss; it is PRA rules, with new rule numbers.**
   Commission Delegated Regulation (EU) 2015/35 Articles 84–221 (the standard formula) have been
   **revoked and restated into the PRA Rulebook** by PS15/24 [R63], effective **31/12/2024**. The
   operative citation for a stress size is now e.g. `SCR-SF 3B1.1`, not `DR Art. 137`. Any UK
   documentation that cites Delegated Regulation article numbers as live law is wrong. The
   assimilated DR text on legislation.gov.uk [R70] is retained here only as a **revoked/historic**
   cross-check.
2. **Rule numbering inside the SF Part is two-level and unusual.** Chapters are `1, 1A–1D, 2, 2A,
   3, 3A–3G, 4, 5, 6, 7, 8, 9`. Within the restated risk-module chapters (3A–3G) each former DR
   article became an *article-style sub-chapter* — `3B6` is "Life Lapse Risk Sub-Module" — whose
   paragraphs render in the rulebook as bare `1.`, `2.`, `3.` but are **cited as `3B6.1`,
   `3B6.6(1)`** and so on. Both forms appear in the retrieved text; the compound form is the
   citable one and is used throughout this file.
3. **The mass-lapse rule was published wrong and corrected a month later.** PS15/24 as published
   put RAO Schedule 1 Part II **class III** ("Linked long-term") inside the 70% mass-lapse limb of
   `SCR-SF 3B6.6(1)`. The PRA declared this an **error** on **20 December 2024** and deleted the
   class III reference by *PRA Rulebook: SII Firms: Solvency II Amendment (No 1) Instrument 2024*,
   effective **31 December 2024** [R64]. The live rule reads **class VII** only. A unit-linked
   bond therefore takes **40%**, not 70%. See §5.3 and Gaps §3.
4. **Tables and correlation matrices survived text extraction, but row labels did not always.**
   The BSCR, life, health, SLT-health, NSLT-health and market matrices all extracted with their
   numeric cells intact and verifiably symmetric. In several matrices the **first row's label is
   absent** in the rendered HTML (the first data row follows immediately after the last column
   header). Each such case is flagged inline in §3–§8. **The Annexes to the SF Part are a separate
   file that was not retrieved** — so Annex XVI (health catastrophe country factors), Annex II
   (lines of business), and the geographical-diversification annex are recorded as **not
   retrieved**, not guessed. See Gaps §1.
5. **The Part has been amended repeatedly and carries future-dated text.** The retrieved view is
   "the Rulebook in the present on 05/08/2026"; the Part shows change dates **01/01/2016,
   31/12/2024, 24/07/2025, 01/01/2026** and **01/01/2027**, and rule 1.2 (definitions) has a
   **future version after 01/01/2027** that was not retrieved. Every rule quoted below is given
   with the date stamp the rulebook attaches to it.
6. **`SCR-SF 3.3A` is the single most consequential rule for model architecture.** It fixes what a
   "scenario" means: risk margin unchanged, deferred taxes unchanged, **future discretionary
   benefits unchanged** and no management actions — in the *gross* run; and `6.3(2)` then defines
   the *net* run in which FDB and management actions **do** move. That two-run structure, not any
   individual stress size, is what determines how a liability projection model must be built. See
   §14 and Model hooks.

---

## Existing entries (R1–R38, and sibling-stream entries) that bear on this stream

- **[R1]** PRA Rulebook — Technical Provisions Part. Every scenario stress is defined as a change
  in "the … rates used for the calculation of technical provisions"; the BEL this Part governs is
  the object every SF stress revalues.
- **[R2]** PRA Rulebook — Matching Adjustment Part. MA portfolios drive the notional-SCR
  requirement in `SCR-SF 9` (§16) and the restriction on diversification across MA portfolios.
- **[R3]** PRA Rulebook — Transitional Measure on Technical Provisions Part. TMTP sits in TP, not
  in the SCR; it changes own funds and hence SCR coverage, not the SCR modules.
- **[R4]** SI 2023/1346 (Risk Margin Regulations). Relevant because `SCR-SF 3.3A(1)(a)` freezes
  the risk margin inside every scenario, and because the risk margin is itself a function of a
  projected SCR run-off.
- **[R5]** PS10/24 — MA reform. Background to the MA portfolio construct that `SCR-SF 9` splits.
- **[R6]** PS15/24 — Restatement of assimilated law. **The instrument that created the SF Part in
  its present form**; also see new entry [R63] for the SF-specific chapters and [R64] for the
  mass-lapse correction.
- **[R7]** PS2/24 — Adapting to the UK insurance market.
- **[R8]** SS7/18 — Matching adjustment.
- **[R22]–[R31]** CMI tables and the CMI projections model. The SF mortality/longevity/morbidity
  stresses are multiplicative shocks **to the firm's own best-estimate rates**, which for UK life
  business are CMI-table based; the stress does not replace the table.
- **[R33]/[R34]** FRC TAS 100 / TAS 200; **[R35]** IFoA APS L1. The professional layer over any SCR
  calculation and its documentation.
- **[R84]** PRA Rulebook — Reporting Part. Determines *which* SCR numbers must be reported and at
  what granularity (per RFF/MA portfolio via the `IRR.` template family).
- **[R85]** SS40/15 — reporting and disclosure; **[R86]** PS3/24. SCR disclosure in the SFCR.
- **[R92]** PRA Rulebook — Conditions Governing Business Part. The actuarial function's duty to
  opine on TP, and the ORSA's own-assessment of overall solvency needs *against* the SCR.
- **[R97]** SS17/16, with SS15/16 and SS1/24 — internal model governance and **standard-formula
  SCR reporting for firms with an approved internal model** (see [R68] for SS15/16 itself).
- **[R111]** PRA Rulebook — Valuation Part Chapter 11 (deferred taxes). The valuation basis
  `SCR-SF 6.4(2)` points at for LACDT.
- **[R112]** PRA Rulebook — SCR-SF Part **Chapter 6** (LACTP/LACDT), already numbered by the
  accounting/tax stream. §14 of this file is the model-architecture reading of the same chapter
  and cites [R112]; it does **not** create a second number for it.

---

## New entries

### A. The two SCR Parts of the PRA Rulebook

#### R61. PRA Rulebook — **Solvency Capital Requirement – General Provisions Part** (as at 05/08/2026)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.prarulebook.co.uk/pra-rules/solvency-capital-requirement---general-provisions/05-08-2026
- **Doc type:** rulebook part (as-at view). **Accessed:** 2026-08-06.
- **fetched_ok:** yes (browser User-Agent required — prarulebook.co.uk returns HTTP 403 to plain
  fetchers; 14,517 chars of extracted text; **read in full**, all 8 chapters)
- **Annotation:** The short constitutional Part sitting above the standard formula. Verified in
  retrieved text, with the rulebook's own date stamps: **1.1** application (UK Solvency II firm;
  the Society; managing agents) [01/01/2016]. **2.1** a firm must hold eligible own funds covering
  its SCR [Art. 100 SII; 01/01/2016]. **3.1** the SCR must be calculated **either** under the
  standard formula **or** using an internal model for which internal model permission has been
  granted [31/12/2024 — this rule was changed at the restatement; a pre-31/12/2024 version exists
  and was not retrieved]. **3.2** going-concern presumption [Art. 101(2)]. **3.3** calibration must
  take account of all quantifiable risks, "including at least" non-life underwriting, **life
  underwriting, health underwriting, market, credit and operational risk**; must cover existing
  business **and new business expected to be written over the following 12 months**; and for
  existing business must cover **only unexpected losses** [Art. 101(3)–(4)]. **3.4** the SCR "must
  correspond to the **value-at-risk of its basic own funds subject to a confidence level of 99.5%
  over a one-year period**" [Art. 101(3)]. **3.5** risk-mitigation techniques may be recognised
  provided the credit and other risks they create are reflected. **3.6** the SCR **must not cover
  the risk of loss of basic own funds resulting from changes to the volatility adjustment** [Art.
  77d(6)]. **4.1** calculate and report at least annually; **4.2** hold own funds covering the
  **last reported** SCR; **4.3** monitor own funds and SCR **on an ongoing basis**; **4.4**
  recalculate **without delay** and report if the risk profile deviates significantly from the
  assumptions underlying the last reported SCR; **4.5** recalculate on PRA request where there is
  evidence of significant alteration [all Art. 102; 01/01/2016]. **5.1/5.1A** duty to remedy
  deficiencies behind a capital add-on and, on request, to submit a progress report [5.1A added
  31/12/2024]; **5.2** SCR before the add-on **plus** the add-on constitutes the firm's SCR; **5.3**
  **for the purpose of calculating the risk margin the SCR must exclude any add-on imposed for a
  significant system-of-governance deviation** [Art. 37(5)]. Chapters **6–8** are Lloyd's-specific
  (Society-level eligible own funds, the central requirement, and syndicate/member **notional
  SCRs** under 8.2–8.4) and are recorded but not material to a UK direct life insurer's model.
- **Products:** all seven UK products.

#### R62. PRA Rulebook — **Solvency Capital Requirement – Standard Formula Part** (as at 05/08/2026)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.prarulebook.co.uk/pra-rules/solvency-capital-requirement---standard-formula/05-08-2026
- **Doc type:** rulebook part (as-at view). **Accessed:** 2026-08-06.
- **fetched_ok:** yes (browser User-Agent required; 452,843 chars raw / 408,900 chars cleaned —
  the single largest document in the UK library). **Read selectively, by chapter**: chapters 2, 2A,
  3, 3B, 3C, 3D (interest rate, equity, symmetric adjustment, property, spread on bonds and loans,
  spread on MA portfolios, concentration, currency), 3E13–3E15, 3F, 4, 5, 6, 7.1–7.16, 8 and 9
  were read in full; chapters 1D, 3A (non-life), 3D18–3D24 (securitisation, credit derivatives,
  specific exposures) and 3G were surveyed only.
- **Annotation:** The operative UK standard formula. This is the same underlying document as the
  local copies `cap-scr-standard-formula.txt`, `s5-scr-sf.txt`, `acct-pra-scr-sf.txt` and
  `pra-scr-sf.txt` (identical byte length, 452,843) — **one source, not four**. Chapter inventory
  as retrieved: `1` Application and Definitions; `1A` General Requirements on the Use of Credit
  Assessments; `1B` Issuers and Issue Credit Assessment; `1C` Double Credit Rating for
  Securitisation Positions; `1D` Allocation of Credit Assessments to Credit Quality Steps; `2`
  Structure of the SCR Standard Formula; `2A` Annexes; `3` The Basic SCR; `3A` Non-life Underwriting
  Risk Module; `3B` Life Underwriting Risk Module; `3C` Health Underwriting Risk Module; `3D`
  Market Risk Module; `3E` Counterparty Default Risk Module; `3F` Intangible Asset Module; `3G`
  Risk Mitigation Techniques; `4` Calculation of the Equity Risk Sub-Module and Application of the
  Symmetric Adjustment Mechanism; `5` Capital Requirement for Operational Risk; `6` Adjustment for
  Loss-Absorbing Capacity of Technical Provisions and Deferred Taxes; `7` Simplification in the
  Standard Formula; `8` Lloyd's; `9` Ring-Fenced Funds and Matching Adjustment Portfolios. The
  Part's change dates are **01/01/2016, 31/12/2024, 24/07/2025, 01/01/2026, 01/01/2027**; rule 1.2
  carries a future version after 01/01/2027 that was **not retrieved**. All operative content is
  transcribed in §2–§17 below with rule references. Chapter 6 is separately numbered [R112] by the
  accounting/tax stream.
- **Products:** all seven UK products.

#### R63. PS15/24 Appendix 6 — **PRA Rulebook: Solvency II Instrument 2024** (the restatement instrument)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.bankofengland.co.uk/prudential-regulation/publication/2024/november/review-of-solvency-ii-restatement-of-assimilated-law-policy-statement
- **Doc type:** rule-making instrument annexed to a policy statement. **Accessed:** 2026-08-06.
- **fetched_ok:** yes (681,045 chars extracted; **searched, not read whole**)
- **Annotation:** Distinct from **[R6]**, which is the policy statement PS15/24 itself; this entry
  is the *legal instrument* appended as Appendix 6, in which Annex O contains the SCR – Standard
  Formula Part as made. It is cited here for one purpose only: it is the published text in which
  rule **SCR-SF 3B6.6(1)** referred to **both RAO Schedule 1 Part II class III and class VII**,
  which the PRA subsequently declared an error [R64]. Read in conjunction with [R6]; do **not**
  cite the instrument for the current wording of any rule — cite [R62], the as-at rulebook view.
- **Products:** all; the class III point bites ULB.

#### R64. PRA statement, 20 December 2024 — *Restatement of Solvency II assimilated law: correction to standard formula mass lapse life underwriting risk rule in PS15/24*, with **PRA Rulebook: SII Firms: Solvency II Amendment (No 1) Instrument 2024**
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.bankofengland.co.uk/prudential-regulation/publication/2024/december/pra-statement-on-restatement-of-solvency-ii-assimilated-law
- **Doc type:** supervisory statement/notice plus rule instrument. **Accessed:** 2026-08-06.
- **fetched_ok:** yes (5,602 chars; **read in full**. The annexed instrument PDF itself was not
  separately retrieved — the statement describes its single operative effect.)
- **Annotation:** Verified, with quoted rule reference. The PRA "identified an error in rule
  **3B6.6(1)**" of the SCR-SF Part as published in PS15/24. In CP5/24 the PRA proposed to restate
  Delegated Regulation **Article 142(6)**, which applies a **70% mass-lapse stress** to the two
  business types in **Solvency II Directive Articles 2(3)(b)(iii) and (iv)** and **40% in all
  other cases**. Using the 2015 UK transposition table, the PRA identified RAO Schedule 1 Part II
  **class II ("Marriage and birth")** and **class VII ("Pension fund management")** as in scope of
  70%; but in the final PS15/24 instrument it wrote **class III and class VII**. The PRA concluded
  the class III reference "is in fact an error"; the correct restatement of DR Art. 142(6)(a)
  "should only require firms to apply a 70% stress … to **RAO class VII(a) and class VII(b)**
  business". The Amendment (No 1) Instrument 2024 **deletes the class III reference in Annex O of
  Appendix 6 of PS15/24** and is the instrument's only change. Published 20 December 2024;
  **effective 31 December 2024**. The statement **supersedes PS15/24 ¶6.16 and ¶6.18** without
  amending their text. Note the residual discrepancy: the statement's own narrative names **class
  II and class VII** as the transposition-table result, while the corrected rule text as read in
  [R62] names **class VII only** — see Gaps §3.
- **Products:** ULB decisively (40%, not 70%); PA and WOL/WP via the 40% limb.

#### R65. PRA Rulebook — **Solvency Capital Requirement – Undertaking Specific Parameters Part** (as at 05/08/2026)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.prarulebook.co.uk/pra-rules/solvency-capital-requirement---undertaking-specific-parameters/05-08-2026
- **Doc type:** rulebook part (as-at view). **Accessed:** 2026-08-06.
- **fetched_ok:** yes (60,255 chars raw / 54,158 cleaned; chapters 1–3 and 7 read in full,
  chapters 4–6 and 8–10 surveyed). URL independently re-verified on 2026-08-06.
- **Annotation:** Part change dates **31/12/2024** and **24/07/2025**. Chapter inventory:
  `1` Applications and Definitions; `2` Undertaking Specific Parameters; `3` Data Criteria;
  `4` Premium Risk Method; `5` Reserve Risk Method 1; `6` Reserve Risk Method 2; `7` **Revision
  Risk Method**; `8` Non-Proportional Reinsurance Method 1; `9` Non-Proportional Reinsurance
  Method 2; `10` Credibility Factor. Verified: **2.1** a firm must not apply a USP unless it is a
  **USP firm** (i.e. holds a s.138BA USP Permission); **2.2** a USP firm must **not revert** to the
  standard parameter; **2.3** the exhaustive replaceable-parameter table (§18 below); **2.4** where
  alternative methods are available the firm must use the most accurate, or the most conservative
  where greater accuracy cannot be demonstrated; **2.5** two anti-double-counting prohibitions.
  **The only life-relevant USP in the whole Part is the revision-risk parameter** (`3B5` life and
  `3C15` health), and `7.1` bars its use where the annuities are subject to material inflation
  risk. Chapter 3 sets complete/accurate/appropriate data criteria cross-referring to Technical
  Provisions – Further Requirements 4.
- **Products:** PA (revision risk) and IP (health revision risk) only, and then only where the
  benefits can be revised and inflation risk is immaterial; in practice near-empty for UK life.

### B. Historic and instrument-level cross-checks

#### R66. Commission Delegated Regulation (EU) 2015/35 — **REVOKED**; Article 142 (lapse risk sub-module), point-in-time text, on legislation.gov.uk
- **Publisher:** The National Archives / legislation.gov.uk
- **URL:** https://www.legislation.gov.uk/eur/2015/35/article/142 (latest, showing revocation) and
  the point-in-time view of the same article
- **Doc type:** assimilated EU regulation, **revoked**. **Accessed:** 2026-08-06.
- **fetched_ok:** yes via WebFetch/legislation.gov.uk (two files: current view 12,562 chars, and
  a point-in-time view 17,881 chars containing the full Article 142 text; the Regulation's
  contents listing was also retrieved, 58,238 chars)
- **Annotation:** **Historic only — this Regulation is revoked and is NOT operative UK law.** The
  retrieved current view carries the annotation "Regulation revoked (**30.6.2024** for the
  revocation of Arts. 52-54; **31.12.2024** in so far as not already in force)". Retained here as
  the cross-check that establishes the PRA restatement is faithful. Article 142 as read: ¶1 lapse
  capital requirement is the **largest** of up/down/mass; ¶2 **+50%** relative to option exercise
  rates, capped at 100%, only where exercise increases TP without risk margin; ¶3 **−50%** relative,
  capped at **20 percentage points**, only where exercise decreases TP without risk margin; ¶4–5
  the definition of "relevant options" (both discontinuity and continuity rights, and for
  continuity rights the change applies to the *non-exercise* rate); ¶6(a) **70%** discontinuance for
  Directive Art. 2(3)(b)(iii)–(iv) business meeting the non-natural-person / acting-for-beneficiaries
  conditions (with the family-relationship and ≤20-beneficiary carve-outs), ¶6(b) **40%** for all
  other policies, ¶6(c) **40%** decrease in the number of future contracts under reinsurance
  treaties; ¶7 the "same scenario" tie-break against Article 206(2). **Every one of these numbers
  matches the restated PRA rule 3B6 exactly** — the only substantive change is the UK's
  identification of the 70% business population (see [R64]).
- **Products:** all; used only to validate [R62].

#### R67. Bank of England — *Technical information for Solvency II firms* (the **symmetric adjustment / SAECC** publication page)
- **Publisher:** Bank of England / PRA
- **URL:** https://www.bankofengland.co.uk/prudential-regulation/key-initiatives/solvency-ii/technical-information
- **Doc type:** supervisory publication index page. **Accessed:** 2026-08-06.
- **fetched_ok:** yes (32,183 chars; page read in full. **The SAECC spreadsheet itself (XLSX) was
  not retrieved** — no SAECC value is stated anywhere in this file.)
- **Annotation:** Establishes where the symmetric adjustment number comes from operationally.
  Verified: the PRA "publish[es] one key input to this calculation — the **SAECC** — **every
  month**", and it "is based on movements in **four major equity indices over the preceding 36
  months**" (consistent with SCR-SF 3D14, §8.3 below). Also verified: as a temporary measure UK
  insurers used the **EIOPA SAECC for valuations from 31 December 2020 to 30 March 2021**, and
  **from 31 March 2021** firms should use the PRA spreadsheet based on UK insurers' exposures,
  which also restates historical levels on the post-31/03/2021 methodology. Separately verified on
  the same page (relevant to stream B, recorded here because it constrains currency risk):
  **from 1 January 2025 the PRA ceased publishing technical information for AUD, DKK, SEK and NOK**
  and continues to publish for **GBP, USD, EUR and CAD**. Monthly RFR releases are published "on or
  before the **eighth working day** of the following month".
- **Products:** WP and ULB principally (equity exposure); all products for the currency point.

### C. Supervisory statements and statements of policy that bear on the SCR

#### R68. SS15/16 — *Solvency II: Monitoring model drift and standard formula SCR reporting for firms with permission to use an internal model* (September 2025, updating July 2018)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.bankofengland.co.uk/prudential-regulation/publication/2016/solvency2-monitoring-model-drift-and-standard-formula-scr-reporting-ss
- **Doc type:** supervisory statement (PDF). **Accessed:** 2026-08-06.
- **fetched_ok:** yes (7,699 chars; **read in full**, 7 pages)
- **Annotation:** The document that makes the standard formula relevant to internal-model firms.
  Verified: ¶1.1 addressed to firms with **s.138BA FSMA** internal model permission. ¶2.1 "model
  drift" is defined as the risk that internal-model capital requirements "may, over time, become
  less reflective of the risks to which firms are exposed". ¶2.3 the alternative balance-sheet
  measures the PRA monitors against include **standard formula SCR, pre-corridor MCR, net written
  premium and best estimate liabilities**. ¶3.3 **Solvency Capital Requirement – Internal Models
  3.4** requires an internal-model firm to provide the PRA on request with an estimate of the SCR
  determined under the standard formula; ¶3.5 the PRA therefore expects such firms **to maintain
  the ability to calculate their SCR using the standard formula**. ¶3.5A–3.7 the *annual private
  XBRL* standard-formula submission is expected of firms **with material non-life technical
  provisions** only, is **not required to be externally audited**, and must be approved by a
  suitably authorised senior manager; ¶3.8 due **four weeks after** the annual QRT deadline in the
  Reporting Part [R84]; ¶3.11 submitted through **BEEDS** as "occasional submissions". Complements
  [R97] (SS17/16). Note the practical consequence for a UK life insurer: it must be able to run the
  standard formula even if it does not use it for its published SCR.
- **Products:** all; the non-life carve-out means UK life firms face the capability expectation
  (¶3.5) but not the annual submission (¶3.6).

#### R69. Statement of Policy 4/24 — *Solvency II: Capital add-ons* (November 2024, updating February 2024)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.bankofengland.co.uk/prudential-regulation/publication/2024/february/solvency-ii-capital-add-ons-sop
- **Doc type:** statement of policy (PDF). **Accessed:** 2026-08-06.
- **fetched_ok:** yes (41,615 chars; **title page, contents and scope verified from retrieved
  text; the body was surveyed, not transcribed**)
- **Annotation:** The policy layer over SCR – General Provisions Chapter 5 [R61]. Retrieved
  document confirmed as "Solvency II: Capital add-ons, Statement of policy 4/24, November 2024
  (updating February 2024)". **Numerical thresholds not transcribed** — the PRA's quantitative
  thresholds for what counts as a "significant risk profile deviation" were not read out of the
  retrieved text in this pass and must not be stated; see Gaps §5. Recorded for the drafter as the
  place to look, not as a source of numbers here.
- **Products:** all.

#### R70. SoP11/24 — *Solvency II: The PRA's approach to Standard Formula adaptations* (15 November 2024)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.bankofengland.co.uk/prudential-regulation/publication/2024/november/solvency-ii-approach-to-standard-formula-adaptations-sop
- **Doc type:** statement of policy (landing page). **Accessed:** 2026-08-06.
- **fetched_ok:** **partial** — the landing page was retrieved and read in full (2,498 chars); the
  **SoP PDF itself was not retrieved**.
- **Annotation:** Verified from the landing page: the SoP covers the PRA's approach to
  **(a) undertaking specific parameter (USP) and group specific parameter (GSP) permissions;
  (b) investments in a securitisation; and (c) permissions relating to the adjustment for
  loss-absorbing capacity of deferred taxes (LACDT)**; it is to be read with the **SCR – Standard
  Formula** and **SCR – Undertaking Specific Parameters** Parts; published 15 November 2024,
  **effective 31 December 2024**, following PS15/24 [R6]. This is the permissions gateway for
  everything in [R65] and for the LACDT permission in SCR-SF 6.5 [R112]. **No content beyond the
  scope statement was retrieved** — do not attribute detail to it.
- **Products:** PA and IP (USP revision risk); all (LACDT permission).

#### R71. SS14/15 — *With-profits*, **Chapter 2: Solvency II ring-fenced fund (RFF) regime**
- **Publisher:** Prudential Regulation Authority (Bank of England), via the PRA Rulebook guidance view
- **URL:** https://www.prarulebook.co.uk/guidance/supervisory-statements/ss14-15---with-profits/2-solvency-ii-ring-fenced-fund-rff-regime/25-06-2024
- **Doc type:** supervisory statement chapter (rulebook rendering). **Accessed:** 2026-08-06.
- **fetched_ok:** yes (2,058 chars; **chapter 2 read in full**. Printed 05/08/2026, rulebook text
  as at 25/06/2024. Other chapters of SS14/15 were not retrieved in this stream.)
- **Annotation:** The document that connects UK with-profits funds to `SCR-SF 9` [R62]. Verified:
  **¶2.1** the Solvency II Regulations "affect both the determination of own funds and the solvency
  capital requirement (SCR), where RFFs arise", and whether an arrangement gives rise to a RFF turns
  on **restrictions on the use of certain assets or own funds**, which may arise from the
  characteristics of the arrangement, contract or product. **¶2.2** restrictions "result from the
  nature of, and regulatory regime for, with-profits insurance business in the United Kingdom", and
  the PRA expects that such restrictions "will generally mean that **each with-profits fund displays
  the characteristics of a RFF**", so a firm must reflect the unavailability of WP-fund assets and
  own funds to cover the risks of the rest of the firm. **¶2.3** where a firm operates **sub-funds**
  within a with-profits fund it must decide whether each is a separate with-profits fund under FCA
  **COBS 20** [R9]; if so, the PRA expects **each such sub-fund to be treated as a RFF**. All rule
  text date-stamped 20/03/2015.
- **Products:** WP decisively; PA where an MA portfolio exists (parallel treatment under `SCR-SF 9`).

#### R72. PS12/25 — *Restatement of CRR and Solvency II requirements in PRA Rulebook – 2026 implementation* (17 July 2025)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.bankofengland.co.uk/prudential-regulation/publication/2025/july/restatement-of-crr-and-sii-requirements-in-pra-rulebook-policy-statement
- **Doc type:** policy statement. **Accessed:** 2026-08-06.
- **fetched_ok:** yes (59,392 chars; **Chapter 3 (ECAI mapping) read; Chapters 1, 4 and the
  appendix list surveyed; the mapping tables themselves were not transcribed**)
- **Annotation:** The reason the SCR-SF Part carries a **01/01/2026** change date. Verified: the PS
  makes "amendments to the **Solvency Capital Requirement – Standard Formula, Matching Adjustment
  and Glossary Parts** of the PRA Rulebook for Solvency II firms" (Appendix 6, *PRA Rulebook: CRR
  Firms, Solvency II Firms: Credit Quality Steps Mapping Instrument 2025*) [¶1.5-type listing];
  ¶1.7 Chapter 3 on ECAI mapping is relevant to Solvency II firms; ¶3.1 the mappings of external
  credit assessment institution ratings to **credit quality steps** are specified in the capital
  adequacy frameworks and most PRA-authorised firms must apply them; ¶3.4 the PRA originally
  proposed **1 July 2025** for the insurance-related changes; ¶3.33 it then confirmed that the
  Solvency II mapping tables would be implemented on **1 January 2026**; ¶3.14 two changes from
  consultation — the **Banque de France Global ANACOT** long-term issuer scale was added, and the
  **Economist Intelligence Unit** sovereign rating band scale was removed. **The mapping tables
  themselves are not transcribed here** — the CQS *inputs* to `3D17`, `3D25`, `3D29`, `3D30` and
  `3E12` come from this instrument, and a drafter needs the instrument, not this file, for them.
- **Products:** PA principally (MA portfolio spread risk and CQS assignment); all products holding
  rated debt.

#### R73. PRA Rulebook — **Annexes to the SCR – Standard Formula Part** (referenced by SCR-SF 2A.1)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** linked from https://www.prarulebook.co.uk/pra-rules/solvency-capital-requirement---standard-formula/05-08-2026 (rule 2A.1: "The Annexes referred to in 3A, 3C and 7 can be found here")
- **Doc type:** rulebook annex file. **Accessed:** 2026-08-06.
- **fetched_ok:** **NO** — the annexes are a separate linked file that was **not retrieved**; only
  the pointer rule 2A.1 [31/12/2024] was read, in [R62].
- **Annotation:** Numbered deliberately so that the gap has a citable handle. The annexes referred
  to by rules 3A, 3C and 7 include, on the evidence of the cross-references read in [R62]: **Annex
  XVI** (health catastrophe — the country list, the ratio of persons affected `r_s`, the event
  types `e`, the benefit ratios `x_e`, and the healthcare-utilisation types `h` and ratios `H_h`
  for the pandemic sub-module), **Annexes V–VIII and X** (non-life catastrophe risk zones and risk
  weights), and the annex underlying the geographical-diversification factor in `3A5`. **None of
  these values is stated anywhere in this file.** Any downstream document needing a health-CAT
  parameter must retrieve this annex file first.
- **Products:** IP and CI (health catastrophe); non-life annexes are out of scope for the UK life
  library.

---

## Extracted mechanics

Notation: `sqrt(x)` square root, `^2` square, `Sum_{i,j}` double sum over all ordered pairs,
`max(...)`, `min(...)`. All rule references are to the **PRA Rulebook**; `SCR-GP` = Solvency
Capital Requirement – General Provisions Part [R61], `SCR-SF` = Solvency Capital Requirement –
Standard Formula Part [R62], `USP` = Solvency Capital Requirement – Undertaking Specific
Parameters Part [R65]. Bracketed dates are the rulebook's own "in force from" stamps.

### 1. What the SCR is, and the duty to keep holding it [R61]

**1.1 Calibration.** `SCR-GP 3.4`: the SCR "must correspond to the **value-at-risk of its basic
own funds subject to a confidence level of 99.5% over a one-year period**" [01/01/2016]. The same
calibration is imposed module by module by `SCR-SF 3.3` [01/01/2016]. The object is **basic own
funds**, not technical provisions and not assets: every stress is measured as a *loss in basic own
funds*, i.e. the change in (assets − liabilities) on the Solvency UK balance sheet.

**1.2 Scope of risks.** `SCR-GP 3.3(1)`: at least non-life underwriting, **life underwriting**,
**health underwriting**, **market**, **credit** and **operational** risk. `3.3(2)`: the SCR covers
existing business **and new business expected to be written over the following 12 months**.
`3.3(3)`: for existing business it covers **only unexpected losses**.

**1.3 Two carve-outs.** `SCR-GP 3.6`: the SCR **must not cover the risk of loss of basic own funds
resulting from changes to the volatility adjustment** [Art. 77d(6) SII]. There is **no
corresponding carve-out for the matching adjustment**: MA movements *are* in scope, and `SCR-SF
3D25` (§9.1) makes the mechanism explicit. `SCR-GP 3.2`: going-concern presumption.

**1.4 Method election.** `SCR-GP 3.1` [31/12/2024]: a firm must calculate its SCR **either** in
accordance with the standard formula **or** using an internal model **for which internal model
permission has been granted**. There is no third option; USPs are not a separate method but a
parameter substitution *inside* the standard formula ([R65]; §18). Partial internal models exist
and are visible in `SCR-SF 6.4(7)(c)`, which requires the LACDT loss allocation to follow the
contribution of the standard formula modules **outside** the partial model's scope.

**1.5 Frequency and the continuous-coverage duty.** `SCR-GP 4.1` calculate and report **at least
once a year**. `4.2` the own funds a firm must hold cover its **last reported** SCR — not a
continuously recomputed one. `4.3` the firm must monitor **both** eligible own funds **and** the
SCR **on an ongoing basis**. `4.4` if the risk profile **deviates significantly** from the
assumptions underlying the last reported SCR, the firm must **recalculate without delay** and
report to the PRA. `4.5` on PRA request where there is evidence of significant alteration. The
annual calculation is the reporting obligation; the *monitoring* obligation is continuous, and it
is `4.4` that forces an intra-year re-run. All [01/01/2016].

**1.6 Capital add-ons.** `SCR-GP 5.2`: the SCR before the add-on **plus** the add-on **is** the
firm's SCR. `5.3`: **for the purpose of calculating the risk margin, the SCR must exclude any
add-on imposed as a result of a significant system of governance deviation** — an add-on for a
*risk profile* deviation is **not** excluded. `5.1`/`5.1A`: duty to remedy, and on request to
submit a progress report [5.1A added 31/12/2024]. The PRA's approach is SoP4/24 [R69]; **its
quantitative significance thresholds were not retrieved and are not stated here**.

**1.7 The standard formula for internal-model firms.** SS15/16 ¶3.3 [R68]: *Solvency Capital
Requirement – Internal Models 3.4* requires an internal-model firm to give the PRA, on request, an
estimate of the SCR under the standard formula; ¶3.5 the PRA therefore expects such firms to
**maintain the ability to calculate the standard formula SCR**. The *annual private XBRL
submission* (¶3.6) is expected only of firms with **material non-life technical provisions**.

### 2. The structure of the standard formula and the BSCR aggregation [R62]

**2.1 Top-level identity.** `SCR-SF 2.1` [01/01/2016]:

```
SCR = BSCR + SCR_operational + Adj
```

where `BSCR` is the basic SCR (`SCR-SF 3`), `SCR_operational` is the operational risk capital
requirement (`SCR-SF 5`), and `Adj` is the **adjustment for the loss-absorbing capacity of
technical provisions and deferred taxes** (`SCR-SF 6`), which is **negative or zero** (see §14).
`SCR-SF 2.2` [31/12/2024]: a firm with a ring-fenced fund or a matching adjustment portfolio must
instead follow the method in `SCR-SF 9` (§16) — with a carve-out for an RFF whose restricted own
funds have been fully deducted from the reconciliation reserve under `Own Funds 3L.2`.

**2.2 BSCR aggregation.** `SCR-SF 3.1(2)` and `3.1(3)` [31/12/2024]:

```
BSCR = sqrt( Sum_{i,j} Corr_{i,j} * SCR_i * SCR_j ) + SCR_intangibles
```

over `i,j` in {Market, Default, Life, Health, Non-life}. The intangible module is **added outside
the square root**, i.e. it receives **no diversification benefit**.

**2.3 The top-level correlation matrix.** `SCR-SF 3.1(2)(d)` [31/12/2024]. Extracted cleanly and
verified symmetric:

|             | Market | Default | Life | Health | Non-life |
|-------------|--------|---------|------|--------|----------|
| Market      | 1      | 0.25    | 0.25 | 0.25   | 0.25     |
| Default     | 0.25   | 1       | 0.25 | 0.25   | 0.5      |
| Life        | 0.25   | 0.25    | 1    | 0.25   | 0        |
| Health      | 0.25   | 0.25    | 0.25 | 1      | 0        |
| Non-life    | 0.25   | 0.5     | 0    | 0      | 1        |

For a UK life insurer the non-life row and column are zero against Life and Health, so in practice
the live block is the 4×4 {Market, Default, Life, Health} with **0.25 everywhere off-diagonal**.

**2.4 Allocation of obligations to modules.** `SCR-SF 3.2` [01/01/2016] allocate to the
underwriting risk that **best reflects the technical nature** of the underlying risks. `3.2A`
[31/12/2024] is prescriptive: the **life** module applies to life insurance and reinsurance
obligations **other than health** obligations; the **health** module applies to **health**
insurance and reinsurance obligations; the non-life module to non-life other than health. The
health/life boundary is decided by whether an obligation is a *health* obligation, and then
`3.10B` decides SLT vs NSLT by line of business (§7.1). **This is the rule that puts UK income
protection and critical illness into the health module, not the life module.**

**2.5 Look-through.** `SCR-SF 2.3` [31/12/2024]: the SCR must be calculated on the basis of **each
of the underlying assets** of collective investment undertakings and other investments packaged as
funds; look-through also applies to indirect exposures to market, underwriting and counterparty
risk. If look-through is impossible, `2.3(3)` permits the **target** asset allocation, or failing
that the **last reported** allocation, subject to the assets being managed to that allocation and
exposures not being expected to vary materially. `2.3(4)` data groupings may be used but **must not
apply to more than 20% of the total value of the firm's assets**; `2.3(5)` that 20% denominator
**excludes underlying assets backing unit-linked or index-linked liabilities where the market risk
is borne by policyholders**. `2.3(6)` look-through does not apply to investments in related
undertakings unless the related undertaking is essentially an asset-holding vehicle for the
participating undertaking.

### 3. What a "scenario" means — the single most important architectural rule

**3.1 The gross run.** `SCR-SF 3.3A(1)` [31/12/2024]: where a module or sub-module is based on the
impact of a scenario on basic own funds, the firm must assume **all** of:

- (a) the scenario **does not change the amount of the risk margin** included in technical
  provisions;
- (b) the scenario **does not change the value of deferred tax assets and liabilities**;
- (c) the scenario **does not change the value of future discretionary benefits** included in
  technical provisions;
- (d) **no management actions are taken** by the firm during the scenario.

**3.2 What still moves inside the gross run.** `3.3A(2)`: in recalculating technical provisions
under the scenario the firm must not change the value of FDB, but **must** take account of
(a) future management actions complying with *Technical Provisions – Further Requirements 8*
("without prejudice to (1)(d)"), and (b) **any material adverse impact of the scenario or of those
management actions on the likelihood that policyholders will exercise options relating to
contracts of insurance**. Limbs (1)(d) and (2)(a) are in tension on their face; **this file
records the tension rather than resolving it** — see Gaps §4.

**3.3 Simplifications inside a scenario.** `3.3A(3)`: simplified methods for the stressed technical
provisions are allowed provided they do not lead to a misstatement of the SCR that could influence
the decision-making or judgement of the user — **unless** the simplified calculation produces an
SCR that **exceeds** the standard-formula SCR (prudence is always permitted).

**3.4 Risk-mitigation instruments and the one-sided floor.** `3.3A(4)`: the impact of the scenario
on the value of relevant risk-mitigation instruments must be taken into account (subject to
`3G2`, `3G3`, `3G5`–`3G9`). `3.3A(5)`: **where the scenario would result in an increase in basic
own funds, the calculation must be based on the assumption that the scenario has no impact** —
i.e. every scenario-based sub-module capital requirement is **floored at zero**.

**3.5 The net run.** `SCR-SF 6.3(2)` [31/12/2024] defines the **net basic SCR (nBSCR)**: the BSCR
recalculated with all of the following modifications — (a) the scenario **may change the value of
future discretionary benefits**; (b) the scenario-based calculations of the **life underwriting
risk module, the SLT health underwriting risk sub-module, the health catastrophe risk sub-module,
the market risk module and the counterparty default risk module** must take into account the impact
on FDB, on the basis of **future management actions complying with Technical Provisions – Further
Requirements 8**; (c) type 1 counterparty default is replaced by an equivalent instantaneous-loss
scenario; (d) the same instantaneous-loss substitution applies where the firm used one of the
listed simplifications (`7.8`, `7.9`, `7.10`, `7.11`, `7.12(1)`, `7.12(2)`, `7.14`, `7.20`,
`7.23(1)(a)`, `7.23(1)(b)`, `7.24`). `6.3(3)`: the firm must take into account **any legal,
regulatory or contractual restrictions on the distribution of future discretionary benefits**.

**3.6 Consequence for model architecture.** The standard formula requires the liability model to be
run **twice per scenario** for any firm with future discretionary benefits: once **gross** (FDB
frozen, `3.3A`) and once **net** (FDB responsive, `6.3(2)`). Firms with no FDB — term assurance,
critical illness, income protection, unit-linked bond, non-profit pension annuity — have
`BSCR = nBSCR` and `Adj_TP = 0`, so one run suffices. **With-profits is the product that forces the
two-run architecture.**

**3.7 The "same scenario" tie-break.** Four sub-modules are defined as the *highest/higher* of
alternative scenarios, and each carries a rule that the choice must be made on the **net** basis:
lapse `3B6.9`, SLT health lapse `3C16.9`, interest rate `3D4.2`, currency `3D32.9`. Each says:
where the highest gross requirement and the highest corresponding **`6.3(2)`** (net) requirement
are **not based on the same scenario**, the capital requirement is the one **whose underlying
scenario produces the highest net requirement**. The *selection* is made net; the *reported gross*
number follows the net selection. This is easy to implement wrongly.

### 4. Life underwriting risk module — structure and stresses [R62 chapter 3B]

**4.1 Sub-modules.** `SCR-SF 3.8(1)` [24/07/2025]: mortality, longevity, disability-morbidity,
life expense, revision, lapse, life catastrophe. Aggregation `3.8(2)`:

```
SCR_life = sqrt( Sum_{i,j} Corr_{i,j} * SCR_i * SCR_j )
```

**4.2 The life correlation matrix.** `SCR-SF 3.8(3)` [24/07/2025]. Extracted and verified
symmetric. **Retrieval note: the "Mortality" ROW label is absent in the rendered HTML** — the
first data row follows immediately after the last column header. The row is identified as Mortality
by symmetry against the first column of every other row, which is consistent in all six cases.

|                 | Mortality | Longevity | Disability | Life expense | Revision | Lapse | Life cat |
|-----------------|-----------|-----------|------------|--------------|----------|-------|----------|
| Mortality       | 1         | −0.25     | 0.25       | 0.25         | 0        | 0     | 0.25     |
| Longevity       | −0.25     | 1         | 0          | 0.25         | 0.25     | 0.25  | 0        |
| Disability      | 0.25      | 0         | 1          | 0.5          | 0        | 0     | 0.25     |
| Life expense    | 0.25      | 0.25      | 0.5        | 1            | 0.5      | 0.5   | 0.25     |
| Revision        | 0         | 0.25      | 0          | 0.5          | 1        | 0     | 0        |
| Lapse           | 0         | 0.25      | 0          | 0.5          | 0        | 1     | 0.25     |
| Life catastrophe| 0.25      | 0         | 0.25       | 0.25         | 0        | 0.25  | 1        |

The **−0.25 mortality/longevity** entry is the only negative correlation anywhere in the standard
formula as retrieved, and it is why a mixed protection-plus-annuity book diversifies.

**4.3 Mortality — `3B1`** [31/12/2024]. `3B1.1`: the loss in basic own funds from an
**instantaneous permanent increase of 15%** in the **mortality rates used for the calculation of
technical provisions**. `3B1.2`: apply the increase **only to those policies for which an increase
in mortality rates leads to an increase in technical provisions without the risk margin**; in
identifying them the firm may (1) treat multiple policies on the same insured person as one, and
(2) work at the level of **groups of policies** as referred to in *Technical Provisions – Further
Requirements 20*, provided the result is not materially different. `3B1.3`: for reinsurance
obligations the identification applies to the **underlying** insurance policies.

**4.4 Longevity — `3B2`** [31/12/2024]. `3B2.1`: **instantaneous permanent decrease of 20%** in the
mortality rates used for the TP calculation; `3B2.2`–`3B2.3` mirror `3B1.2`–`3B1.3` with the
direction reversed (apply only where a *decrease* in mortality increases TP without risk margin).

**4.5 Disability-morbidity — `3B3.1`** [31/12/2024]. A **single combined** instantaneous permanent
scenario, all three limbs simultaneously:
1. **+35%** in the disability and morbidity rates used to reflect experience **in the following 12
   months**;
2. **+25%** in those rates **for all months after the following 12 months**;
3. **−20%** in the **disability and morbidity recovery rates** used in the TP calculation, **in
   respect of the following 12 months and for all years thereafter**.

There is **no** "apply only where TP increases" qualifier in `3B3` (unlike `3B1`/`3B2`), and no
persistency limb (contrast the *health* version, `3C13`, §7.6).

**4.6 Life expense — `3B4.1`** [31/12/2024]. Combined instantaneous permanent changes:
**+10%** in the **amount of expenses** taken into account in the TP calculation, **and**
**+1 percentage point** added to the **expense inflation rate** used in the TP calculation.
`3B4.2`: for reinsurance obligations apply to the firm's own expenses and, where relevant, the
ceding undertakings'.

**4.7 Revision — `3B5.1`** [31/12/2024]. **Instantaneous permanent increase of 3%** in the amount of
**annuity benefits**, **only** on annuity insurance and reinsurance obligations **where the
benefits payable under the underlying policies could increase as a result of changes in the legal
environment or in the state of health of the person insured**. A standard UK level or
fixed-escalation pension annuity has no such revision right, so this sub-module is normally **nil**
for UK PA. Contrast the health version `3C15` (§7.8), which is **4%** and adds **inflation** as a
trigger.

**4.8 Life catastrophe — `3B7.1`** [31/12/2024]. **Instantaneous increase of 0.15 percentage
points** in the mortality rates (**expressed as percentages**) used in the TP calculation to reflect
**the mortality experience in the following 12 months**. This is an *absolute* addition (+0.0015 in
decimal), not a multiplicative shock, and it is a **one-year** shock, not permanent. `3B7.2`–`3B7.3`
carry the same "only where TP without risk margin increases", grouping and reinsurance provisions as
`3B1`.

### 5. Life lapse risk — `3B6`, and the mass-lapse correction

**5.1 The three-way maximum.** `3B6.1` [31/12/2024]: the lapse capital requirement is the
**highest** of (1) permanent increase, (2) permanent decrease, (3) **mass lapse**. The selection is
subject to the net-basis tie-break `3B6.9` (§3.7).

**5.2 Up and down.** `3B6.2`: **instantaneous permanent increase of 50%** (relative) in the
**option exercise rates** of the relevant options, **provided the increased rates do not exceed
100%**, and applying **only to relevant options for which exercise would increase technical
provisions without the risk margin**. `3B6.3`: **instantaneous permanent decrease of 50%**
(relative), **the decrease not to exceed 20 percentage points**, applying only where exercise would
**decrease** TP without risk margin. `3B6.4`: "relevant options" are (1) all rights to fully or
partly **terminate, surrender, decrease, restrict or suspend** cover or permit the policy to lapse,
and (2) all rights to fully or partially **establish, renew, increase, extend or resume** cover —
and for limb (2) **the change in the option exercise rate is applied to the rate reflecting that
the option is NOT exercised**. `3B6.5`: for reinsurance contracts, the relevant options include
those of the reinsurance policyholders, those of the policyholders of the underlying contracts, and
the right of potential policyholders **not to conclude** future contracts covered by the treaty.

**5.3 Mass lapse — `3B6.6`** [**24/07/2025**; a past version before 24/07/2025 exists and was not
retrieved]. A combination of instantaneous events:

- **`3B6.6(1)` — 70%** discontinuance of the insurance policies **falling within the scope of
  operations referred to in Regulated Activities Order Schedule 1, Part II, class VII** [R14] for
  which discontinuance would increase technical provisions without the risk margin, **and** where
  one of the following is met:
  - (a) the **policyholder is not a natural person** and discontinuance is not subject to approval
    by the beneficiaries of the pension fund; or
  - (b) the policyholder **is a natural person acting for the benefit of the beneficiaries**,
    **except** where there is a **family relationship** between that person and the beneficiaries,
    or where the policy is effected for **private estate planning or inheritance** purposes and the
    **number of beneficiaries does not exceed 20**.
- **`3B6.6(2)` — 40%** discontinuance of **all other** policies for which discontinuance would
  increase TP without the risk margin.
- **`3B6.6(3)` — 40%** decrease in the number of **future** contracts used in the TP calculation,
  where reinsurance contracts cover contracts to be written in the future.

**5.4 The correction.** As published in PS15/24 Appendix 6 Annex O [R63], `3B6.6(1)` referred to
**both class III ("Linked long-term") and class VII ("Pension fund management")**. The PRA declared
the class III reference an **error** on 20 December 2024 and deleted it by *PRA Rulebook: SII
Firms: Solvency II Amendment (No 1) Instrument 2024*, **effective 31 December 2024** [R64]. The live
rule reads **class VII only**, which the retrieved as-at-05/08/2026 text confirms [R62]. **A UK
unit-linked bond therefore takes the 40% mass-lapse limb, not 70%.** The EU original
(DR Art. 142(6)(a), now revoked) scoped the 70% limb to Directive Art. 2(3)(b)(iii)–(iv) [R66], and
the PRA's stated policy intent is **RAO class VII(a) and VII(b)** only.

**5.5 Definitions that make the lapse module work.** `SCR-SF 1.2` [31/12/2024]: **"discontinuance"**
means, in relation to an insurance policy, **surrender, lapse without value, making a contract
paid-up, automatic non-forfeiture provisions or exercising other discontinuity options or not
exercising continuity options**; **"discontinuity options"** are the termination-side rights;
**"continuity options"** are the establish/renew/increase/extend/resume rights; **"lapse risk"** is
"the risk of loss, or of adverse change, in the value of insurance obligations, resulting from
changes in the level or volatility of the rates of policy lapses, terminations, renewals and
surrenders". **Making a contract paid-up is a discontinuance event**, which matters for WOL and WP.

**5.6 The per-policy worst-discontinuance rule.** `3B6.8`: for the mass-lapse events in `3B6.6(1)`
and `(2)` the firm must base the calculation on **the type of discontinuance that most negatively
affects its basic own funds on a per policy basis**. `3B6.7`: the events must be applied
**uniformly** to all relevant contracts, and for reinsurance the `3B6.6(1)` event applies to the
underlying insurance contracts. Mass lapse is therefore not "surrender 40% of policies" — it is
"for each policy take the worst of surrender / paid-up / lapse-without-value, then apply 40% of
that".

### 6. Health underwriting risk module — structure, and the NSLT branch [R62 chapter 3C]

**6.1 Structure.** `SCR-SF 3.10A(1)` [24/07/2025]: NSLT health underwriting risk, **SLT** health
underwriting risk, and health catastrophe risk. `3.10A(2)`:

```
SCR_health = sqrt( Sum_{i,j} CorrH_{i,j} * SCR_i * SCR_j )
```

`3.10A(3)` correlation matrix (extracted cleanly, symmetric, all row labels present):

|                        | NSLT health | SLT health | Health cat |
|------------------------|-------------|------------|------------|
| NSLT health underwriting | 1         | 0.5        | 0.25       |
| SLT health underwriting  | 0.5       | 1          | 0.25       |
| Health catastrophe       | 0.25      | 0.25       | 1          |

**6.2 The SLT/NSLT split is by line of business.** `SCR-SF 3.10B` [31/12/2024]: the **NSLT** health
sub-module applies to health obligations in **lines of business 1, 2, 3, 13, 14, 15 and 25**; the
**SLT** health sub-module applies to health obligations in **lines of business 29, 33 and 35**; the
health catastrophe sub-module applies to **all** health obligations. **The line-of-business list
(Annex II/III equivalent) was NOT retrieved** — see [R73] and Gaps §1 — so the mapping of a UK
product to a numbered line of business is **[unverified]** in this file. What *is* verified is that
`3C4` names segment 2 as **"Income protection insurance and proportional reinsurance"**, consisting
of **lines of business 2 and 14**, which sits in the NSLT branch; and that `3C11.2(2)` restricts the
SLT income-protection scenario to income protection obligations "where the underlying business is
**pursued on a similar technical basis to that of life insurance**". So a UK long-term individual
income protection contract falls in the **SLT** branch and a short-term/annually-renewable one in
the **NSLT** branch, on the "similar technical basis" test — but the numbered line of business that
effects that split could not be confirmed from retrieved text.

**6.3 NSLT health, in outline** (relevant only to short-term/renewable UK health business).
`3C1.2`: `SCR_NSLTh = sqrt( SCR_(NSLTh,pr)^2 + SCR_(NSLTh,lapse)^2 )` — an **uncorrelated**
combination. `3C2.1`: `SCR_(NSLT,pr) = 3 * sigma_NSLTh * V_NSLTh`, i.e. a **3-sigma factor
model**, not a scenario. `3C3.2`: `V_s = (V_(prem,s) + V_(res,s)) * (0.75 + 0.25 * DIV_s)`, so the
geographical-diversification factor `DIV_s` can reduce the volume measure by at most 25%
(`3C3.8`: `DIV_s` is either 1 or computed per `3A5` — **`3A5` and its annex were not retrieved**).
`3C3.3`: `V_(prem,s) = max(P_s ; P_(last,s)) + FP_(existing,s) + FP_(future,s)`, with
`FP_(future,s)` = full expected present value of premiums for new contracts with initial term ≤ 1
year (excluding the first 12 months) and **30%** of the expected present value beyond the following
12 months for contracts with initial term > 1 year. `3C3.4` permits the softer
`V_(prem,s) = P_s + FP_(existing,s) + FP_(future,s)` where the governing body has decided earned
premiums will not exceed `P_s`, effective control mechanisms exist, and **the PRA has been informed
in writing**. `3C3.7`: the reserve-risk volume measure is the **best estimate of the provision for
claims outstanding**, net of reinsurance/SPV recoverables, floored at zero.

**6.4 NSLT segments and standard deviations — `3C4`** [31/12/2024]. Table extracted cleanly:

| Segment | Lines of business | sigma gross premium | sigma reserve |
|---------|-------------------|---------------------|---------------|
| 1 Medical expense insurance and proportional reinsurance | 1 and 13 | 5% | 5.7% |
| 2 **Income protection** insurance and proportional reinsurance | 2 and 14 | **8.5%** | **14%** |
| 3 Workers' compensation insurance and proportional reinsurance | 3 and 15 | 9.6% | 11% |
| 4 Non-proportional health reinsurance | 25 | 17% | 17% |

`3C5.1`: `sigma_NSLTh = (1/V_NSLTh) * sqrt( Sum_{s,t} CorrHS_(s,t) * sigma_s * V_s * sigma_t * V_t )`.
`3C5.2` combines premium and reserve standard deviations within a segment as
`sigma_s = sqrt( sp^2*Vp^2 + sp*Vp*sr*Vr + sr^2*Vr^2 ) / (Vp + Vr)` (the 0.5-correlation form).
`3C5.3`: the standard deviation for NSLT health premium risk is the **gross** figure times the
adjustment factor for non-proportional reinsurance, **which for all segments in `3C4` must equal
100%** — i.e. the non-proportional adjustment is switched off in the UK standard parameters and can
only be changed by a USP [R65].
`3C6.1` [24/07/2025] correlation matrix across the four segments: **1 on the diagonal and 0.5
everywhere off-diagonal** (extracted cleanly).

**6.5 NSLT health lapse — `3C7.1`** [31/12/2024]: discontinuance of **40%** of the policies for
which discontinuance increases TP without risk margin, plus a **40%** decrease in the number of
future contracts under forward-looking reinsurance treaties. `3C7.3` carries the same per-policy
worst-discontinuance rule as `3B6.8`. There is **no up/down lapse scenario** in the NSLT branch —
only the mass event.

### 7. SLT health underwriting risk — where UK income protection and critical illness sit

**7.1 Structure.** `3C8.1` [31/12/2024]: health mortality, health longevity, health
disability-morbidity, health expense, health revision, SLT health lapse. `3C8.2`:
`SCR_SLTh = sqrt( Sum_{i,j} CorrSLTH_(i,j) * SCR_i * SCR_j )`.

**7.2 SLT health correlation matrix — `3C8.3`** [31/12/2024]. Extracted cleanly with **all row
labels present** (unlike the life matrix), and verified symmetric:

|                            | H mortality | H longevity | H disab-morb | H expense | H revision | SLT h lapse |
|----------------------------|-------------|-------------|--------------|-----------|------------|-------------|
| Health mortality           | 1           | −0.25       | 0.25         | 0.25      | 0          | 0           |
| Health longevity           | −0.25       | 1           | 0            | 0.25      | 0.25       | 0.25        |
| Health disability-morbidity| 0.25        | 0           | 1            | 0.5       | 0          | 0           |
| Health expense             | 0.25        | 0.25        | 0.5          | 1         | 0.5        | 0.5         |
| Health revision            | 0           | 0.25        | 0            | 0.5       | 1          | 0           |
| SLT health lapse           | 0           | 0.25        | 0            | 0.5       | 0          | 1           |

This is **the life matrix of §4.2 with the life-catastrophe row and column removed** — every
surviving entry is identical. Health catastrophe is instead handled one level up, at 0.25 against
both SLT and NSLT (§6.1).

**7.3 Health mortality — `3C9.1`**: **+15%** instantaneous permanent increase in mortality rates
used for the TP calculation, with the same "only where TP without risk margin increases",
same-life-grouping and reinsurance provisions as `3B1` (`3C9.2`, `3C9.3`). Identical to the life
stress.

**7.4 Health longevity — `3C10.1`**: **−20%** instantaneous permanent decrease. Identical to `3B2`.

**7.5 Health disability-morbidity — `3C11.1`**: the **sum** (not a correlated aggregation) of
(1) the capital requirement for **medical expense** disability-morbidity risk and (2) the capital
requirement for **income protection** disability-morbidity risk. `3C11.2` restricts each scenario
to the corresponding obligations **"where the underlying business is pursued on a similar technical
basis to that of life insurance"**.

**7.6 Income protection disability-morbidity — `3C13.1`** [31/12/2024]. A **single combined**
instantaneous permanent scenario:
1. **+35%** in the disability and morbidity rates used to reflect experience **in the following 12
   months**;
2. **+25%** in those rates **in the years after the following 12 months**;
3. **where the disability and morbidity RECOVERY rates used in the TP calculation are lower than
   50%, a −20% decrease** in those rates;
4. **where the disability and morbidity PERSISTENCY rates used in the TP calculation are equal to
   or lower than 50%, a +20% increase** in those rates.

Note the two conditional limbs, and their asymmetric thresholds ("**lower than** 50%" for recovery,
"**equal to or lower than** 50%" for persistency). This differs from the *life* disability stress
`3B3.1`, which has no conditionality and no persistency limb. Both are transcribed as read.

**7.7 Medical expense disability-morbidity — `3C12`**: the **higher** of an increase and a decrease
scenario. `3C12.2` increase: **+5%** in the amount of medical payments in the TP calculation **and**
**+1 percentage point** in the **inflation rate of medical payments**. `3C12.3` decrease: **−5%**
and **−1 percentage point** respectively. Not material to the seven UK products in the library.

**7.8 Health expense — `3C14.1`**: **+10%** in the amount of expenses **and** **+1 percentage
point** in the expense inflation rate — identical to the life expense stress `3B4.1`.

**7.9 Health revision — `3C15.1`**: **instantaneous permanent increase of 4%** in the amount of
annuity benefits, only on annuity obligations where benefits could increase as a result of changes
in **inflation**, the legal environment or the state of health of the insured. **Two differences
from the life version `3B5.1`: 4% not 3%, and inflation is an additional trigger.** A UK
income-protection claim-in-payment annuity with an index-linked escalation is squarely in scope.

**7.10 SLT health lapse — `3C16`**. `3C16.1`: the **higher** of up / down / **SLT health mass
lapse**. `3C16.2`: **+50%** relative to option exercise rates, capped at 100%. `3C16.3`: **−50%**
relative, the decrease capped at **20 percentage points**. `3C16.4`–`3C16.5`: the same relevant-
options definitions as `3B6.4`–`3B6.5`. `3C16.6`: **SLT health mass lapse is a flat 40%**
discontinuance of the policies whose discontinuance increases TP without the risk margin, plus
**40%** off future reinsured contracts — **there is no 70% limb in the health module at all**.
`3C16.8` per-policy worst discontinuance; `3C16.9` the net-basis tie-break (§3.7).

**7.11 Health catastrophe — `3C17`–`3C20`.** `3C17.1`:
`SCR_healthCAT = sqrt( SCR_ma^2 + SCR_ac^2 + SCR_p^2 )` — **uncorrelated** across mass accident,
accident concentration and pandemic. `3C17.2` scope: mass accident applies to all health
obligations **other than workers' compensation**; accident concentration to **workers' compensation
and GROUP income protection**; pandemic to all health obligations other than workers'
compensation.
- **Mass accident `3C18`**: `SCR_ma = sqrt( Sum_s SCR_(ma,s)^2 )` over countries in **Annex XVI**;
  `L_(ma,s) = r_s * Sum_e x_e * E_(e,s)` where `r_s` is the ratio of persons affected in country
  `s` and `x_e` the ratio receiving benefits for event type `e`, **both set out in Annex XVI, which
  was NOT retrieved [R73]**. `3C18.4` the value of benefits is the sum insured, or for recurring
  benefits the **best estimate of the benefit payments**, and where benefits depend on the nature
  or extent of injury, **the maximum benefits payable consistent with the event**. `3C18.5` permits
  homogeneous risk groups.
- **Accident concentration `3C19`**: `SCR_ac = sqrt( Sum_c SCR_(ac,c)^2 )`;
  `L_(ac,c) = C_c * Sum_e x_e * CE_(e,c)`, where `C_c` is the **largest accident risk
  concentration** in country `c`, defined by `3C19.3` as the **highest number of persons working in
  the same building** for whom the firm has a workers' compensation or **group income protection**
  obligation covering at least one Annex XVI event. `CE_(e,c)` is the average benefit over that
  concentration (`3C19.4`).
- **Pandemic `3C20.1`**: `L_p = 0.000075 * E + 0.4 * Sum_c (N_c * M_c)`, where **E** is the
  **income protection pandemic exposure** (`3C20.2`: the sum over insured persons of the value of
  benefits payable **in case of permanent work disability caused by an infectious disease**, taken
  as the sum insured or, for recurring benefits, the best estimate assuming the person is
  **permanently disabled and will not recover**), `N_c` the number of medical-expense insured
  persons in country `c`, and `M_c` the expected average pandemic payment per person
  (`3C20.3`: `M_c = Sum_h H_h * CH_(h,c)`, with healthcare-utilisation types `h` and ratios `H_h`
  **in Annex XVI, not retrieved**). **The 0.000075 and 0.4 factors are in the rule itself and are
  verified**; the Annex XVI inputs are not.

### 8. Market risk — structure, interest rate, equity, property [R62 chapter 3D]

**8.1 Structure and the state-dependent correlation.** `SCR-SF 3.11(2)` [31/12/2024]: interest
rate, equity, property, spread, currency, market risk concentrations. `3.11A(1)`:
`SCR_market = sqrt( Sum_{i,j} Corr_(i,j) * SCR_i * SCR_j )`. `3.11A(2)` [24/07/2025] matrix,
extracted cleanly and symmetric:

|               | Interest rate | Equity | Property | Spread | Concentration | Currency |
|---------------|---------------|--------|----------|--------|---------------|----------|
| Interest rate | 1             | **A**  | **A**    | **A**  | 0             | 0.25     |
| Equity        | **A**         | 1      | 0.75     | 0.75   | 0             | 0.25     |
| Property      | **A**         | 0.75   | 1        | 0.5    | 0             | 0.25     |
| Spread        | **A**         | 0.75   | 0.5      | 1      | 0             | 0.25     |
| Concentration | 0             | 0      | 0        | 0      | 1             | 0        |
| Currency      | 0.25          | 0.25   | 0.25     | 0.25   | 0             | 1        |

`3.11A(3)`: **the coefficient `A` equals 0 where the interest-rate capital requirement under `3D4`
is the one referred to in `3D4.1(1)` — i.e. the INCREASE (up) scenario — and 0.5 in all other
cases** (i.e. when the *down* scenario bites). This is the "which interest scenario bites" rule:
a firm whose interest-rate charge comes from the **up** shock gets **zero** correlation between
interest rate and each of equity, property and spread; a firm whose charge comes from the **down**
shock (the typical UK annuity writer) gets **0.5**. The market SCR is therefore a **discontinuous**
function of the balance sheet.

**8.2 Interest rate — `3D4`–`3D6`.** `3D4.1` [31/12/2024]: the capital requirement is the **higher**
of (1) the **sum over all currencies** of the up requirements and (2) the **sum over all
currencies** of the down requirements. Note the aggregation: **summed across currencies within each
direction, then max across directions** — not max per currency. `3D4.2` applies the net-basis
tie-break (§3.7).

`3D5.1` **relative upward** shocks to basic risk-free rates by maturity [31/12/2024]:

| Maturity (yrs) | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 90 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Increase | 70% | 70% | 64% | 59% | 55% | 52% | 49% | 47% | 44% | 42% | 39% | 37% | 35% | 34% | 33% | 31% | 30% | 29% | 27% | 26% | 20% |

`3D5.2`: **linear interpolation** for unspecified maturities; **70%** below 1 year; **20%** beyond
90 years. `3D5.3`: **the increase at any maturity must be at least one percentage point** (an
absolute floor on top of the relative shock). `3D5.4` restricts the effect on participations in
financial and credit institutions to the part not deducted under `Own Funds 3K`.

`3D6.1` **relative downward** shocks [31/12/2024]:

| Maturity (yrs) | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 90 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Decrease | 75% | 65% | 56% | 50% | 46% | 42% | 39% | 36% | 33% | 31% | 30% | 29% | 28% | 28% | 27% | 28% | 28% | 28% | 29% | 29% | 20% |

`3D6.2`: linear interpolation; **75%** below 1 year; **20%** beyond 90 years. `3D6.3`:
**for negative basic risk-free interest rates the decrease must be nil**. Note the **non-monotonic
shape at 14–20 years** (28, 27, 28, 28, 28, 29, 29) — this is as extracted and is checked against
the shape of the EU original in Gaps §2. There is **no absolute floor** on the downward shock,
unlike the 1-percentage-point floor on the upward shock.

**8.3 Equity — `3D7`–`3D14`.** `3D7.1`: four buckets — **type 1**, **type 2**, qualifying
infrastructure equities, qualifying infrastructure **corporate** equities. `3D7.2` [24/07/2025]
type 1 = the equities listed in `3D7.8` plus equities listed on regulated markets in **OECD**
member countries, or traded on multilateral trading facilities (RAO Article 3) whose registered or
head office is in an **EU Member State**. `3D7.3` type 2 = everything else, including commodities
and other alternative investments, **and all assets not covered by the interest-rate, property or
spread sub-modules, including look-through failures under `2.3(1)`/`(2)` where the firm does not
use the `2.3(3)`/`(4)` fallbacks**. `3D7.6` aggregation:

```
SCR_equity = sqrt( SCR_equ1^2
                 + 2 * 0.75 * SCR_equ1 * (SCR_equ2 + SCR_quinf + SCR_quinfc)
                 + (SCR_equ2 + SCR_quinf + SCR_quinfc)^2 )
```

i.e. type 2 and the two infrastructure buckets are **added arithmetically** and then combined with
type 1 at correlation **0.75**.

`3D9` stress sizes [`3D9.1`, `3D9.3`, `3D9.4` 31/12/2024; `3D9.2` 24/07/2025]:

| Bucket | Strategic (`3D10`) | Long-term equity (`3D11`) | Other |
|--------|--------------------|---------------------------|-------|
| Type 1 | **22%** | **22%** | **39% + SA** |
| Type 2 | **22%** | **22%** | **49% + SA** |
| Qualifying infrastructure equity | **22%** | **22%** | **30% + 77% × SA** |
| Qualifying infrastructure corporate equity | **22%** | **22%** | **36% + 92% × SA** |

`3D10.1` "strategic" requires the firm to demonstrate materially lower 12-month volatility **and**
strategic nature (decisive long-hold strategy, consistency with policies, ability to continue
holding, a durable link, group consistency). `3D11.1` "long-term equity investments" requires
**eight** cumulative conditions plus **written notification to the PRA**, including: the sub-set and
each holding period clearly identified; the sub-set inside a **ring-fenced-like** assigned asset
portfolio backing identified business, managed and organised separately and unavailable to cover
other losses; those TP being **only part** of total TP; **average holding period exceeding five
years** (or no sales until it does); **only UK-listed equities or unlisted equities of companies
headquartered in the UK**; solvency, liquidity and ALM such that **forced sales can be avoided for
at least 10 years** under stress; and consistency of the risk-management/ALM/investment policies.
`3D11.3`: a firm that adopts LTEI **must not revert**, and if it ceases to comply it must inform
the PRA immediately and **cease applying the 22% treatment for 36 months**. `3D11.4` grandfathering
notification deadline **31 January 2025** for firms that used DR Art. 171a immediately before
31 December 2024.

**8.4 The symmetric adjustment — `3D12`, `3D13`, `3D14`, and chapter 4.** `SCR-SF 4.1`
[01/01/2016]: a symmetric adjustment **must** be applied to the standard equity capital charge
[Art. 106(1) SII]. `3D12.2` [31/12/2024]:

```
SA = 0.5 * ( (CI - AI) / AI  -  8% )
```

where `CI` is the **current level** of the equity index and `AI` the **weighted average of the
daily levels of the equity index over the last 36 months**. `3D12.3`: **all daily weights are
equal**, and days on which the index was not determined are **excluded** from the average.
`3D12.4`: **the symmetric adjustment must not be lower than −10% or higher than +10%.** `3D12.1`
sets the index criteria (diversified, representative of equities typically held by UK Solvency II
undertakings, publicly available, published frequently enough to determine the current level and
the 36-month average).

`3D13`: the index level is determined for **each working day** (Saturdays and Sundays excluded) as
the **sum of the contributions** of the constituent indices, each contribution being its
**normalised level** (last level on the day divided by its last level on the first day of the
36-month period, with the most recent prior level carried forward when a day is missing) times its
weight. `3D14.1` the constituent indices and weights, extracted cleanly:

| Equity index (price indices) | Weight |
|------------------------------|--------|
| **FTSE All-Share Index** | **0.48** |
| Nikkei 225 | 0.07 |
| S&P 500 | 0.30 |
| FTSE Developed Europe ex UK (local currency) | 0.15 |

(Weights sum to 1.00.) Operationally, the PRA publishes the **SAECC** monthly [R67]; firms used the
**EIOPA** SAECC for valuations from 31/12/2020 to 30/03/2021 and the PRA's UK-exposure-based
spreadsheet from **31/03/2021**. **No SAECC value is stated in this file** — the spreadsheet was not
retrieved.

**8.5 Property — `3D15.1`** [31/12/2024]: the loss in basic own funds from an **instantaneous
decrease of 25%** in the value of **immovable property**. A single unconditional factor.

### 9. Market risk — spread, concentration, currency

**9.1 Spread scope — `3D16.1`**: `SCR_spread = SCR_bonds + SCR_securitisation + SCR_cd`, an
**arithmetic sum** of the bonds-and-loans, securitisation and credit-derivative components.

**9.2 Spread on bonds and loans — `3D17`** [31/12/2024]. `3D17.1`: an instantaneous **relative
decrease of `stress_i`** in the value of each bond or loan `i` (excluding qualifying mortgage loans
under `3E3`, but **including bank deposits other than cash at bank**). `3D17.2`: `stress_i` depends
on the **modified duration `dur_i` in years, floored at 1**; for variable-rate instruments `dur_i`
is that of a fixed-rate instrument of the same maturity with coupons equal to the forward rate.
`3D17.3` rated table — the extraction is internally consistent (six `a_i`/`b_i` column-pairs, six
values in every data row) and the header row reads `0 / 1 / 2 / 3 / 4 / 5 and 6`:

| dur_i | formula | CQS0 a/b | CQS1 a/b | CQS2 a/b | CQS3 a/b | CQS4 a/b | CQS5&6 a/b |
|-------|---------|----------|----------|----------|----------|----------|------------|
| up to 5 | `b_i * dur_i` | — / 0.9% | — / 1.1% | — / 1.4% | — / 2.5% | — / 4.5% | — / 7.5% |
| >5 to 10 | `a_i + b_i*(dur_i-5)` | 4.5% / 0.5% | 5.5% / 0.6% | 7.0% / 0.7% | 12.5% / 1.5% | 22.5% / 2.5% | 37.5% / 4.2% |
| >10 to 15 | `a_i + b_i*(dur_i-10)` | 7.0% / 0.5% | 8.5% / 0.5% | 10.5% / 0.5% | 20.0% / 1.0% | 35.0% / 1.8% | 58.5% / 0.5% |
| >15 to 20 | `a_i + b_i*(dur_i-15)` | 9.5% / 0.5% | 11.0% / 0.5% | 13.0% / 0.5% | 25.0% / 1.0% | 44.0% / 0.5% | 61.0% / 0.5% |
| >20 | `min(a_i + b_i*(dur_i-20); 1)` | 12.0% / 0.5% | 13.5% / 0.5% | 15.5% / 0.5% | 30.0% / 0.5% | 46.6% / 0.5% | 63.5% / 0.5% |

**Extraction caveats, flagged not silently fixed:** the ">15 to 20 / CQS1" cell renders as
`11 .0%` with a stray space (read as 11.0%); and the merging of CQS 5 and 6 into a single column is
what the retrieved HTML shows but was **not cross-checked against the revoked DR Art. 176 table**,
so whether the PRA genuinely merged them is **[unverified]** — see Gaps §2.

`3D17.4` [24/07/2025] unrated, uncollateralised: `stress_i` = `3% * dur_i` up to 5;
`15 + 1.7% * (dur_i - 5)` for >5 to 10 (**the "15" is transcribed exactly as rendered — the
percent sign is missing in the source text and this is almost certainly meant to be 15%; recorded,
not corrected**); `23.5% + 1.2% * (dur_i - 10)` for >10 to 20; `min(35.5% + 0.5% * (dur_i - 20); 1)`
for >20. `3D17.5`: instruments assigned a CQS under `3D18.1`, `3D18.2` or `3D20.1` (internal
assessment or approved-internal-model assessment) use the **rated** table instead. `3D17.6`:
collateralised unrated exposures get **half** the `3D17.4` factor where the risk-adjusted collateral
value is at least the exposure, and an averaging rule otherwise.

**9.3 Spread scenarios applied to matching adjustment portfolios — `3D25`** [31/12/2024]. **The
rule that makes an MA annuity writer's SCR a full-revaluation calculation.** `3D25.1`: where a firm
applies the matching adjustment it must (1) apply the `3D17`/`3D21`/`3D24` instantaneous decreases
to the **relevant portfolio of assets**, and (2) **recalculate the technical provisions to take
account of the impact on the amount of the matching adjustment**, and in particular **increase the
fundamental spread on assigned assets** by an absolute amount equal to the product of
- (a) the **absolute increase in spread** which, multiplied by the asset's modified duration, would
  produce the relevant `stress_i`; and
- (b) a **reduction factor** by credit quality step:

| CQS | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|-----|---|---|---|---|---|---|---|
| Reduction factor | **45%** | **50%** | **60%** | **75%** | **100%** | **100%** | **100%** |

`3D25.2`: **a 100% reduction factor applies** to assigned assets with **no ECAI credit assessment**,
and to **qualifying infrastructure and qualifying infrastructure corporate assets assigned CQS 3**.
Economically: the MA absorbs `(1 − reduction factor)` of the spread widening, so a CQS 0 portfolio
retains 55% of the widening in the MA and passes only 45% through to the fundamental spread; at
CQS 4 and below the MA gives **no** offset. Note this table has **seven** CQS columns, in contrast
to the six-column `3D17.3` table.

**9.4 Market risk concentrations — `3D26`–`3D31`.** `3D26.1`: computed on **single name
exposures**, with same-corporate-group exposures treated as one name and properties in the same
building treated as one property. `3D29.1` **relative excess exposure thresholds `CT_i`** by
weighted average CQS (extracted cleanly, seven columns):

| CQS | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|-----|---|---|---|---|---|---|---|
| `CT_i` | 3% | 3% | 3% | **1.5%** | 1.5% | 1.5% | 1.5% |

`3D30.1` **risk factor `g_i`**:

| CQS | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|-----|---|---|---|---|---|---|---|
| `g_i` | 12% | 12% | **21%** | **27%** | **73%** | 73% | 73% |

`3D31.1`: **covered bonds** assigned CQS 0 or 1 get `CT_i = 15%` and are treated as a **distinct**
single name exposure from other exposures to the same issuer. (`3D27` and `3D28`, the aggregation
and excess-exposure definition, were read but their formulas are not transcribed here — see
Gaps §5.)

**9.5 Currency — `3D32`** [31/12/2024]. `3D32.2`: foreign currencies are those other than the
currency used to prepare the **financial statements** ("the local currency"). `3D32.1` assignment
rules: multi-listed type 1 and type 2 equities are sensitive to the **currency of their main
listing**; unlisted type 2 equities to the currency of the country of the issuer's **main
operations**; **immovable property to the currency of the country in which it is located**.
`3D32.3`: for each foreign currency, the **higher** of an increase and a decrease scenario;
`3D32.4`/`3D32.5`: **instantaneous ±25%** change in the value of the foreign currency against the
local currency. `3D32.1` opening words: the requirement is the **sum** of the per-currency
requirements — **no diversification across currencies**. `3D32.6` permits an adjusted factor for
currencies **pegged to the euro** subject to `3D33`/`3D34` and three conditions (the peg must
constrain one-year relative changes to within the adjusted factor at the 99.5% calibration, plus
ERM II participation, a European Council decision, or establishment of the peg by the law of the
issuing country). `3D32.9` the net-basis tie-break (§3.7).

### 10. Counterparty default risk [R62 chapter 3E]

**10.1 Aggregation — `SCR-SF 3.13`** [31/12/2024]:

```
SCR_def = sqrt( SCR_def1^2 + 1.5 * SCR_def1 * SCR_def2 + SCR_def2^2 )
```

i.e. type 1 and type 2 combined at an implied correlation of **0.75**.

**10.2 Type 1 vs type 2 — `3.14`, `3.15`.** Type 1: **risk-mitigation contracts including
reinsurance arrangements, SPVs and insurance securitisations**; **cash at bank** (as defined by
reference to Schedule 3 to SI 2008/410 [R105]); deposits with ceding undertakings **where the
number of single name exposures does not exceed 15**; called-up-but-unpaid commitments (same ≤15
test); legally binding commitments the firm has provided (guarantees, letters of credit, letters of
comfort); and **derivatives other than credit derivatives covered in the spread sub-module**.
Type 2: everything else not in the spread sub-module, **including receivables from intermediaries,
policyholder debtors**, qualifying mortgage loans, and the >15-name versions of the deposit and
commitment categories. `3.16` gives an election to treat the >15-name items as type 1 anyway.
`3.17` lets a fully-securing letter of credit / guarantee provider be substituted as the
counterparty for counting single names. `3.18` excludes five credit risks from the module,
including credit risk transferred by a credit derivative, SPV debt issuance, credit and suretyship
underwriting risk (lines 9, 21, 28), non-qualifying mortgage loans and collateral posted to a CCP
or clearing member that is **bankruptcy remote**. `3.19`: **third-party investment guarantees on
insurance contracts for which the firm would be liable on the third party's default are treated as
derivatives** in this module — directly relevant to unit-linked guarantees.

**10.3 Type 1 charge — `3E13`** [31/12/2024], a three-branch step function on `sigma`, the standard
deviation of the loss distribution, relative to total loss-given-default (`TLGD`) on all type 1
exposures:
- `sigma <= 7% * TLGD` → `SCR_def1 = 3 * sigma`;
- `7% * TLGD < sigma <= 20% * TLGD` → `SCR_def1 = 5 * sigma`;
- `sigma > 20% * TLGD` → `SCR_def1 = TLGD` (the whole loss-given-default).

`3E13.4`: `sigma = sqrt(V)`. `3E14.1`: `V = V_inter + V_intra`, with
`V_inter = Sum_{j,k} [ PD_k(1-PD_k) PD_j(1-PD_j) / (1.25 (PD_k + PD_j) - PD_k PD_j) ] * TLGD_j * TLGD_k`
and `V_intra = Sum_j [ 1.5 PD_j (1-PD_j) / (2.5 - PD_j) ] * Sum_{PD_j} LGD_i^2`. (The PD table in
`3E12` and the LGD definitions in `3E4`–`3E11` were surveyed, not transcribed — Gaps §5.)

**10.4 Type 2 charge — `3E15.1`**: the loss from an instantaneous decrease of
`90% * LGD_(receivables > 3 months) + Sum_i 15% * LGD_i`, i.e. **90%** on intermediary receivables
overdue more than three months and **15%** on all other type 2 exposures.

### 11. Intangible asset risk — `3F1.1` [31/12/2024]

`SCR_intangible = 0.8 * V_intangible`, where `V_intangible` is the amount of intangible assets
recognised and valued under `Valuation 8.1(2)`. Added **outside** the BSCR square root (§2.2), so
no diversification. Normally nil for a Solvency UK life balance sheet, since goodwill and most
intangibles are valued at zero.

### 12. Operational risk — `SCR-SF 5` [R62]

**12.1 Principles.** `5.1` [01/01/2016]: the operational risk charge must reflect operational risks
**to the extent not already reflected in the BSCR risk modules** and be calibrated to the
`SCR-GP 3.3`–`3.4` 99.5%/one-year standard. `5.2`: **for linked long-term contracts, the
calculation must take account of the amount of annual expenses incurred** in respect of those
obligations. `5.3` [31/12/2024]: for other business the calculation takes account of **earned
premiums and technical provisions** and **must not exceed 30% of the basic SCR relating to those
operations**.

**12.2 The formula — `5.4(1)`** [31/12/2024]:

```
SCR_Operational = min( 0.3 * BSCR ; Op ) + 0.25 * Exp_ul
```

where `Exp_ul` is the amount of expenses incurred **during the previous 12 months** in respect of
long-term insurance contracts **where the investment risk is borne by policyholders**. Two caps
therefore operate: the **30% of BSCR cap applies only to the `Op` term**, and the unit-linked
expense term `0.25 * Exp_ul` is **added on top, uncapped**.

**12.3 The basic charge — `5.4(2)`**: `Op = max( Op_premiums ; Op_provisions )`.

`5.4(3)`: `Op_premiums = 0.04 * (Earn_life - Earn_life-ul) + 0.03 * Earn_non-life`
` + max(0; 0.04 * ((Earn_life - 1.2*pEarn_life) - (Earn_life-ul - 1.2*pEarn_life-ul)))`
` + max(0; 0.03 * (Earn_non-life - 1.2*pEarn_non-life))`
— i.e. **4%** of non-unit-linked life earned premium, **3%** of non-life earned premium, plus a
**growth surcharge** at the same rates on the excess of the last 12 months' premium over **1.2×**
the preceding 12 months'. All premiums are **gross, without deduction of reinsurance premiums**.
(The extracted LaTeX for `5.4(3)` has mismatched brackets in the rendering; the structure above is
the reading consistent with the defined terms in `5.4(3)(a)`–`(f)`, and is flagged in Gaps §2.)

`5.4(4)`: `Op_provisions = 0.0045 * max(0; TP_life - TP_life-ul) + 0.03 * max(0; TP_non-life)` —
i.e. **0.45%** of non-unit-linked life technical provisions and **3%** of non-life. **Technical
provisions for this purpose exclude the risk margin and are gross of reinsurance and SPV
recoverables.**

**12.4 The unit-linked asymmetry.** Unit-linked business is excluded from **both** `Op_premiums`
(via `Earn_life-ul`) and `Op_provisions` (via `TP_life-ul`), and is instead charged **25% of one
year's unit-linked expenses**. For a pure unit-linked bond writer the operational charge is
therefore essentially `0.25 * Exp_ul`, independent of fund size.

### 13. Risk-mitigation techniques — `SCR-SF 3G` [R62], in outline

Chapter 3G (`3G1` Methods and Assumptions; `3G2` Qualitative Criteria; `3G3` Effective Transfer of
Risk; `3G4` Material Basis Risk; `3G5` Reinsurance and SPVs; `3G6` Financial Risk-Mitigation
Techniques; `3G7` Status of the Counterparties; `3G8` Collateral Arrangements; `3G9` Guarantees)
was **surveyed, not transcribed**. Two verified points bear directly on modelling: `3G1.1`
[31/12/2024] — where a reinsurance contract or SPV meeting `3G2`, `3G5` and `3G7` provides
protection across **several** of the scenario-based calculations in sections 3A–3C, the firm must
**allocate its risk-mitigating effects across those scenario calculations without double-counting**,
capturing the economic effect in each determination of the loss in basic own funds. `3G1.2` —
**finite reinsurance** may be recognised in the 3A–3C scenario calculations only to the extent
underwriting risk is actually transferred, and **must not be taken into account at all** in the
`3A2`/`3C3` premium and reserve volume measures or in calculating USPs [R65]. The detailed
criteria in `3G2`–`3G9` are recorded as not transcribed (Gaps §5).

### 14. Loss-absorbing capacity of technical provisions and deferred taxes — `SCR-SF 6` [R112]

This chapter is numbered **[R112]** by the accounting/tax stream; the entry there carries the
rule-by-rule tax detail. What follows is the **model-architecture** reading, and does not restate it.

**14.1 The adjustment is a sum of two legs.** `6.1(3)`: `Adj = Adj_TP + Adj_DT`, where `Adj_TP` is
the loss-absorbing capacity of **technical provisions** (`6.3`) and `Adj_DT` that of **deferred
taxes** (`6.4`, and `6.5` where applicable). `6.1(1)`: the adjustment reflects potential
compensation of unexpected losses through a **simultaneous decrease in technical provisions or
deferred taxes or both**; `6.1(2)`: it takes account of the **risk-mitigating effect of future
discretionary benefits**.

**14.2 The FDB constraint.** `6.2` [01/01/2016]: the FDB risk-mitigating effect counts **only to
the extent the firm can establish that a reduction in FDB may be used to cover unexpected losses
when they arise**; it **must be no higher than the sum of technical provisions and deferred taxes
relating to those FDB**; and it is measured by **comparing the value of FDB under adverse
circumstances with their value under the best-estimate assumptions**.

**14.3 The TP leg — `6.3(1)`:**

```
Adj_TP = - max( min( BSCR - nBSCR ; FDB ) ; 0 )
```

with `FDB` the **technical provisions without risk margin in respect of future discretionary
benefits**. So `Adj_TP` is **negative or zero**, and is **capped at the FDB balance**. `nBSCR` is
the net basic SCR defined by `6.3(2)` (§3.5). **`BSCR - nBSCR` is exactly the "second run" of the
whole liability model** — the entire BSCR recomputed with FDB responsive and management actions
live.

**14.4 The DT leg — `6.4(1)`:** `Adj_DT` equals the change in the value of the firm's deferred
taxes resulting from an **instantaneous loss equal to `BSCR + Adj_TP + SCR_operational`**. Note the
ordering: the tax leg is computed on the post-`Adj_TP` loss and **includes** operational risk.
`6.4(3)`: an increase in **deferred tax assets** arising from that loss **must not be utilised**
unless the `6.5` transitional applied (that transitional **ended 30 December 2025** — [R112]).
`6.4(5)`: a decrease in DTLs or increase in DTAs gives a **negative** adjustment. `6.4(6)`: a
positive change of deferred taxes gives a **nil** adjustment. `6.4(7)`: where the loss must be
allocated to causes, the allocation follows the **contribution of the standard formula modules and
sub-modules to the BSCR**, with the partial-internal-model carve-out.

**14.5 The two-run structure, stated plainly.** For a firm with FDB, every scenario-based
sub-module in the life module, the SLT health sub-module, the health catastrophe sub-module, the
market module and the counterparty default module must be evaluated **twice**:

```
run A (gross):  FDB frozen (3.3A(1)(c)), no new management actions (3.3A(1)(d))  -> SCR_i  -> BSCR
run B (net):    FDB responsive, management actions per TPFR 8 (6.3(2))           -> nSCR_i -> nBSCR
Adj_TP = -max(min(BSCR - nBSCR; FDB); 0)
SCR    = BSCR + SCR_operational + Adj_TP + Adj_DT
```

and the *scenario selection* in the four "highest of" sub-modules (§3.7) is made on **run B**.

### 15. Simplifications — `SCR-SF 7` [R62]

**15.1 The gate.** `7.1` [01/01/2016]: a simplified calculation may be used for a specific module
or sub-module **where the nature, scale and complexity of the risks justifies it**, and must still
be calibrated to `SCR-GP 3.3`–`3.4`. `7.2` [31/12/2024] requires a documented proportionality
assessment covering (a) the nature, scale and complexity of the risks in the module and (b) an
evaluation, qualitative or quantitative, of the **error** introduced; and if that error would
**lead to a misstatement of the SCR that could influence the decision-making or judgement of the
user**, the simplification **must not be used — unless it produces an SCR that exceeds the standard
calculation**.

**15.2 The life simplifications a UK liability model may use** [all 31/12/2024, all "subject to
7.2"]:
- **Mortality `7.8`**:
  `SCR_mortality = 0.15 * q * Sum_{k=1..n} CAR_k * (1-q)^(k-1) / (1+i_k)^(k-0.5)`,
  where `CAR_k` is total capital at risk in year `k` (per-contract: max(0, (death payment in year
  `k` net of reinsurance + EPV of further amounts payable after year `k` on immediate death) − best
  estimate of the corresponding obligations in year `k`)), `q` the **sum-insured-weighted expected
  average mortality rate over all insured persons and all future years**, `n` the **modified
  duration in years of the death payments** in the best estimate, and `i_k` the annualised spot
  rate at maturity `k` of the relevant risk-free curve.
- **Longevity `7.9`**: `SCR_longevity = 0.2 * q * n * 1.1^((n-1)/2) * BE_long`, with `q` the
  sum-insured-weighted expected average mortality rate **during the following 12 months**, `n` the
  modified duration of payments to beneficiaries, `BE_long` the best estimate of obligations
  subject to longevity risk.
- **Disability-morbidity `7.10`**:
  `SCR_dis-morb = 0.35 * CAR_1 * d_1 + 0.25 * 1.1^((n-3)/2) * (n-1) * CAR_2 * d_2
   + 0.2 * 1.1^((n-1)/2) * t * n * BE_dis`, where `CAR_1` is current total capital at risk (death
  **or disability**), `CAR_2` the same after 12 months, `d_1`/`d_2` the sum-insured-weighted
  expected average disability-morbidity rates in the next 12 months and the 12 months after that,
  `n` the modified duration of disability-morbidity payments, `t` the expected **termination** rates
  during the following 12 months, `BE_dis` the best estimate of obligations subject to
  disability-morbidity risk.
- **Expense `7.11`**:
  `SCR_expenses = 0.1*EI*n + EI * ( (1/(i+0.01)) * ((1+i+0.01)^n - 1) - (1/i) * ((1+i)^n - 1) )`,
  with `EI` last year's expenses servicing long-term non-health obligations, `n` the modified
  duration of the best-estimate cash flows, `i` the **present-value-weighted average expense
  inflation rate** in the best estimate.
- **Lapse `7.12`**: `Lapse_up = 0.5 * l_up * n_up * S_up` and
  `Lapse_down = 0.5 * l_down * n_down * S_down`, where `l_up` is **the higher of the average lapse
  rate of policies with positive surrender strains and 67%**, `l_down` **the higher of the average
  lapse rate of policies with negative surrender strains and 40%**, `n_up`/`n_down` the average
  run-off period in years of the respective policies, and `S_up`/`S_down` the sums of positive and
  negative surrender strains. `7.12(3)`: **surrender strain = (amount currently payable on
  discontinuance, net of amounts recoverable from policyholders or intermediaries) − (technical
  provisions without the risk margin)**. Note there is **no simplification for mass lapse**.
- **Lapse grouping `7.13`**: all three lapse requirements (`3B6.2`, `3B6.3`, `3B6.6`) may be
  computed on **groups of policies** complying with *Technical Provisions – Further Requirements
  20.1(2)*.
- **Life catastrophe `7.14`**: `SCR_life-catastrophe = Sum_i 0.0015 * CAR_i` over all policies with
  positive capital at risk — the exact factor-model equivalent of the `3B7.1` +0.15pp shock.

`7.16` onwards give the health analogues (health mortality etc.); `7.20`, `7.23` and `7.24` are
named in `6.3(2)(d)` as simplifications requiring the instantaneous-loss substitution in the net
run. Chapters `7.3`–`7.7` are captive- and non-life-specific.

**15.3 Why this matters architecturally.** Every one of `7.8`–`7.14` converts a **full
revaluation** into a **closed-form factor calculation** driven by summary statistics (capital at
risk, modified duration, weighted average rates, surrender strain). A reference implementation can
therefore offer both paths — but `7.2` makes the closed form legally usable only after a
documented error assessment, and `6.3(2)(d)` means that using one changes how the **net** run is
constructed.

### 16. Ring-fenced funds and matching adjustment portfolios — `SCR-SF 9` [R62], with [R71]

**16.1 Trigger.** `SCR-SF 2.2` [31/12/2024]: a firm with a **ring-fenced fund** (other than one
whose restricted own funds have been fully deducted from the reconciliation reserve under
`Own Funds 3L.2`) **or a matching adjustment portfolio** must adjust its SCR calculation per
`SCR-SF 9`. **Glossary definition (PRA Rulebook Glossary, retrieved; deliberately not given an
R number here to avoid colliding with the technical-provisions stream):** a *ring-fenced fund* is
"an identifiable unit of assets and liabilities where the existence of a restriction on those
assets in relation to those liabilities on a going concern basis gives rise to **restricted own
funds**, **other than a matching adjustment portfolio**" [31/12/2024]. RFFs and MA portfolios are
therefore **disjoint** categories that receive the **same** SCR treatment.

**16.2 The method — `9.1`** [24/07/2025; a past version exists and was not retrieved]:
1. `9.1(1)` compute a **notional SCR for each RFF, each MA portfolio, and the remaining part of the
   firm**, "in the same manner as if each … were separate firms";
2. `9.1(2)` **the firm's SCR is the SUM of those notional SCRs**;
3. `9.1(3)` for every scenario-based module or sub-module, compute the impact on basic own funds
   **at the level of each RFF, each MA portfolio and the remaining part**;
4. `9.1(4)` **at RFF/MA-portfolio level the basic own funds must include only restricted own
   funds**;
5. `9.1(5)` where **profit participation arrangements** exist in an RFF: (a) where the scenario
   would **increase** RFF basic own funds, the estimated increase must be **reduced by the increase
   in technical provisions resulting from the increase in future discretionary benefits** the firm
   would expect to pay in that scenario; (b) where the scenario would **decrease** RFF basic own
   funds, the estimated decrease **for the purposes of the net basic SCR under `6.3(2)`** must be
   **reduced by the reduction in FDB** the firm would expect; (c) that reduction **must not exceed
   the FDB included in the firm's technical provisions for that RFF**;
6. `9.1(6)`–`9.1(7)` **notwithstanding (1)**, the notional SCR for each RFF and MA portfolio must
   use **the scenario-based calculations under which the basic own funds of the FIRM AS A WHOLE are
   most negatively affected** — determined by summing the scenario impacts across all RFFs and MA
   portfolios and adding the impact on the remaining part;
7. `9.1(8)` the notional SCR is then determined by aggregating the capital requirements for each
   sub-module and risk module of the BSCR;
8. `9.1(9)` **notwithstanding `3.4`, the firm must NOT allow for diversification effects between
   its ring-fenced funds, its matching adjustment portfolios, or the remaining part of the firm.**

**16.3 Consequences.** (a) The correlation matrices of §2.3, §4.2, §7.2 and §8.1 are applied
**within** each notional SCR, never across them. (b) An MA annuity portfolio's SCR is computed
standalone and **added** to the rest — an annuity writer with a single MA portfolio and a small
remaining part gets essentially no diversification between them. (c) `9.1(6)` means the *scenario
choice* (up vs down interest rates, which lapse scenario) is made **firm-wide**, not per fund, so a
notional SCR can be driven by a scenario that is not the worst for that fund. (d) `9.1(4)` means
only restricted own funds are at risk inside the RFF, which is what caps the RFF's contribution.

**16.4 With-profits.** SS14/15 chapter 2 [R71]: the PRA expects that the restrictions arising from
the UK with-profits regime "will generally mean that **each with-profits fund displays the
characteristics of a RFF**" (¶2.2), and where **sub-funds** must be treated as separate
with-profits funds under FCA COBS 20 [R9], the PRA expects **each such sub-fund to be treated as a
RFF** (¶2.3). So a UK with-profits insurer with three sub-funds runs **at least four** notional
SCRs and adds them. Own funds and surplus funds inside the RFF are stream D's.

### 17. Full revaluation versus formulaic — the master table

The single most important model-architecture consequence of the standard formula. "Full
revaluation" means the liability cash flow model must be **re-run end to end under changed
assumptions** and the resulting best estimate revalued; "formulaic" means the charge is a closed
form over exposure statistics that the projection produces but does not itself re-project.

| Module / sub-module | Rule | Full revaluation of the BEL? | What drives it |
|---|---|---|---|
| Life mortality | `3B1.1` | **Yes** | mortality rates ×1.15, on the TP-increasing subset |
| Life longevity | `3B2.1` | **Yes** | mortality rates ×0.80, on the TP-increasing subset |
| Life disability-morbidity | `3B3.1` | **Yes** | inception ×1.35 yr1 / ×1.25 thereafter, recovery ×0.80 |
| Life expense | `3B4.1` | **Yes** | expenses ×1.10 and inflation +1pp |
| Life revision | `3B5.1` | **Yes** (narrow) | annuity benefits ×1.03, revisable annuities only |
| Life lapse up / down | `3B6.2`/`3B6.3` | **Yes**, twice | option exercise rates ×1.5 (cap 100%) / ×0.5 (cap −20pp) |
| Life mass lapse | `3B6.6` | **Yes**, third run | 70% (RAO class VII) / 40% instantaneous discontinuance |
| Life catastrophe | `3B7.1` | **Yes** | year-1 mortality rates +0.15pp absolute |
| SLT health mortality / longevity / expense | `3C9`/`3C10`/`3C14` | **Yes** | as life |
| SLT health disability-morbidity (IP) | `3C13.1` | **Yes** | +35%/+25% inception, conditional −20% recovery, conditional +20% persistency |
| SLT health revision | `3C15.1` | **Yes** | annuity benefits ×1.04 |
| SLT health lapse (3 scenarios) | `3C16` | **Yes**, three runs | ×1.5 / ×0.5 / 40% mass |
| NSLT health premium & reserve | `3C2.1` | **No — factor** | `3 * sigma * V`; needs premium and claims-provision volumes |
| NSLT health lapse | `3C7.1` | **Yes** | 40% instantaneous discontinuance |
| Health CAT: mass accident, accident concentration | `3C18`/`3C19` | **No — factor** | sums insured by event type and country; **Annex XVI inputs not retrieved** |
| Health CAT: pandemic | `3C20` | **No — factor** | `0.000075*E + 0.4*Sum N_c M_c`; `E` needs a permanent-disability benefit valuation |
| Interest rate up / down | `3D5`/`3D6` | **Yes**, twice | rebuild the discount curve and revalue assets **and** BEL |
| Equity | `3D9` | Assets only, **but** BEL for unit-linked and WP | 22% / (39%+SA) / (49%+SA) / (30%+0.77·SA) / (36%+0.92·SA) |
| Property | `3D15.1` | Assets only, plus unit-linked/WP BEL | −25% |
| Spread — non-MA | `3D17` | Assets only | `stress_i(CQS, dur_i)` |
| Spread — **MA portfolio** | `3D25` | **Yes** | stress assets **and** recompute the MA via the fundamental-spread uplift × reduction factor |
| Concentration | `3D26`–`3D31` | **No — factor** | `CT_i`, `g_i` by weighted-average CQS |
| Currency | `3D32` | Assets and any FX-denominated BEL, twice | ±25% |
| Counterparty default type 1 | `3E13` | **No — factor** | `3σ / 5σ / TLGD` step function on PD and LGD |
| Counterparty default type 2 | `3E15.1` | **No — factor** | 90% / 15% of LGD |
| Intangible | `3F1.1` | **No — factor** | `0.8 × V_intangible` |
| Operational | `5.4` | **No — factor** | earned premiums, TP, and unit-linked expenses |
| LACTP (`Adj_TP`) | `6.3` | **Yes — a full second pass of everything above** | FDB responsive, management actions live |
| LACDT (`Adj_DT`) | `6.4` | Balance-sheet revaluation of deferred taxes | instantaneous loss `BSCR + Adj_TP + SCR_op` |
| RFF / MA notional SCRs | `9.1` | **Yes — repeat the whole exercise per fund** | no diversification between funds |

**Counting the runs.** A with-profits insurer with one RFF and no MA portfolio, using no
simplifications, needs on the order of **(number of scenario-based sub-modules) × 2 (gross/net) ×
(number of RFFs + MA portfolios + 1)** complete liability revaluations, plus the assumption-set
permutations inside the lapse and interest-rate maxima. This, not the size of any single stress, is
what determines whether a projection engine is fit for standard-formula reporting.

### 18. Undertaking specific parameters — `USP` Part [R65]

**18.1 Gate.** `USP 2.1` [31/12/2024]: a firm **must not** apply a USP unless it is a **USP firm**,
i.e. holds a **USP Permission** (granted under **s.138BA FSMA**; the permissions policy is SoP11/24
[R70]). `USP 2.2`: a USP firm **must not revert** to the standard parameter it replaced.

**18.2 The exhaustive list of replaceable parameters — `USP 2.3`** [31/12/2024]:

| Standard parameter | Sub-module | Corresponding USP method |
|---|---|---|
| standard deviation for non-life premium risk | `3A1` / segments in `3A3` | premium risk method (`USP 4`) |
| standard deviation for non-life **gross** premium risk | `3A1` / `3A3` | premium risk method |
| adjustment factor for non-proportional reinsurance (non-life) | `3A1` / `3A3` | non-proportional method 1 (excess of loss) or 2 (stop loss) |
| standard deviation for non-life reserve risk | `3A1` / `3A3` | reserve risk method 1 (`USP 5`) or 2 (`USP 6`) |
| **the increase in the amount of annuity benefits (life)** | **`3B5`** | **revision risk method (`USP 7`)** |
| standard deviation for NSLT health premium risk | `3C2` / segments in `3C4` | premium risk method |
| standard deviation for NSLT health **gross** premium risk | `3C2` / `3C4` | premium risk method |
| adjustment factor for non-proportional reinsurance (NSLT health) | `3C2` / `3C4` | non-proportional method 1 or 2 |
| standard deviation for NSLT health reserve risk | `3C2` / `3C4` | reserve risk method 1 or 2 |
| **the increase in the amount of annuity benefits (health)** | **`3C15`** | **revision risk method (`USP 7`)** |

**Nothing else in the standard formula may be replaced by a USP.** In particular there is **no** USP
for any mortality, longevity, lapse, expense or catastrophe parameter, and none for any market or
counterparty parameter. For the seven UK products in this library the USP regime reduces to a
single possibility: the **revision-risk** parameter for PA (life `3B5`) and IP (health `3C15`).

**18.3 Choice among alternative methods — `USP 2.4`**: where `2.3` offers alternatives the firm must
use the method producing **the most accurate** result for the `SCR-GP 3.3`/`3.4` calibration, and
**the most conservative** where it cannot demonstrate greater accuracy of one over another.
`USP 2.5` prohibits replacing **both** the gross premium risk standard deviation **and** the
non-proportional adjustment factor for the same segment (two limbs, non-life and NSLT health).

**18.4 The revision risk method — `USP 7`** [31/12/2024]. `7.1(1)`: available **only** for `3B5`
(life) or `3C15` (health), **and only if the annuities within scope are not subject to material
inflation risk**; `7.1(2)` treats inflation risk as material where ignoring it could influence the
decision-making or judgement of users, including supervisors. `7.2`: data must be **annual amounts
of annuity benefits of annuity obligations whose benefits could increase as a result of changes in
the legal environment or in the state of health of the insured, separately for consecutive
financial years and each beneficiary**. `7.3` data requirements: representative of the next 12
months' revision risk; **at least five consecutive financial years**; benefits **gross** of
reinsurance and SPV recoveries; benefits **including the expenses of servicing** the annuity
obligations; and consistent with the stochastic assumptions that (a) the **annual number** of
increases follows a **negative binomial** distribution including in the tail, (b) the **amount** of
an increase follows a **lognormal** distribution including in the tail, and (c) number and amount
are **mutually stochastically independent**. `7.4` notation: `A_(i,t)` the annuity benefits of
beneficiary `i` in financial year `t`, `D_(i,t) = A_(i,t) − A_(i,t−1)`, `T` the latest year with
data. `7.5` the parameter is credibility-weighted:

```
S_USP = c * ( VaR_0.995(R) - mean(R) ) / mean(R)  +  (1 - c) * S
```

where `c` is the credibility factor (`USP 10`) and `S` the standard parameter (3% life / 4%
health). `7.6`–`7.9` (the derivation of `R` and its VaR) and `USP 10` (the credibility factor
table) were **not transcribed** — Gaps §5.

**18.5 Data criteria — `USP 3`**: data must be **complete, accurate and appropriate** (`3.1`), which
`3.2` defines by cross-reference to *Technical Provisions – Further Requirements 4(1)–(4)* read as
applying to the USP rather than to technical provisions, plus incorporability into the method,
non-obstruction of the `SCR-GP 3.3`/`3.4` calibration, method-specific requirements, and thorough
documentation of collection, assumptions, method selection and validation. `3.3` adds seven further
criteria for **external** data, including that it comes only from firms with a **similar risk
profile** and that there is **sufficient statistical evidence that the underlying probability
distributions have a high degree of similarity, in particular as to the level of volatility**.

---

## Model hooks

What a liability cash flow projection must produce, at what granularity, on what basis, at what
date, for each rule. "Valuation date" throughout means the SCR reference date; every stress is
**instantaneous at that date**, so the projection restarts from the same in-force.

1. **A re-runnable best estimate, parameterised by assumption set** — `3B1`–`3B7`, `3C9`–`3C16`,
   `3D5`/`3D6`, `3D25`. The model must accept mortality, morbidity, recovery, persistency, lapse,
   expense, expense-inflation, benefit-escalation and discount-curve inputs **as arguments**, not
   as hard-coded tables, and return the BEL **without the risk margin**. Granularity: policy or
   `TPFR 20` homogeneous risk group. Basis: Solvency UK best estimate, gross and net of
   reinsurance. Date: valuation date.
2. **A TP-without-risk-margin sensitivity flag per policy/group, per stress direction** — `3B1.2`,
   `3B2.2`, `3B6.2`, `3B6.3`, `3B6.6(1)`, `3B6.6(2)`, `3B7.2`, `3C7.1`, `3C9.2`, `3C10.2`,
   `3C16.2`, `3C16.3`, `3C16.6`. Most stresses apply **only to the subset whose TP without risk
   margin increases**. The model must therefore be able to evaluate the stress **per unit** and
   select, not apply the stress globally and net off. `3B1.2(1)` permits aggregating multiple
   policies on the same insured life; `3B1.2(2)`/`7.13` permit group-level selection where not
   materially different.
3. **A per-policy worst-discontinuance value** — `3B6.8`, `3C7.3`, `3C16.8`. For each policy the
   model must value **surrender, lapse-without-value, paid-up and any other discontinuity option**
   and take the one most negative to basic own funds, before applying the 40% / 70% factor.
   Granularity: policy. This is a *maximum over discontinuance types*, not a blended assumption.
4. **Surrender strain** — `7.12(3)`: (amount currently payable on discontinuance, net of amounts
   recoverable from policyholders or intermediaries) **minus** TP without risk margin, **signed**,
   per policy. Needed only if the lapse simplification is used, but it is also the natural
   diagnostic for which policies fall in which limb of hook 2.
5. **Capital at risk by future year** — `7.8(a)`, `7.10(a)`, `7.14(b)`: `max(0, (immediate death
   or disability payment net of reinsurance + EPV of later amounts payable on immediate death) −
   best estimate of the corresponding obligations)`. Granularity: policy, **and by projection year
   `k`** for `7.8`. Needed for the mortality, disability and life-catastrophe simplifications and
   for reconciling to the full-revaluation answer.
6. **Modified duration of specified cash flow streams** — `7.8(c)` death payments, `7.9(b)`
   payments to beneficiaries, `7.10(e)` disability-morbidity payments, `7.11(b)` all best-estimate
   cash flows. Also `3D17.2` on the asset side. The projection must be able to emit modified
   durations of **sub-streams**, not just of the total liability.
7. **Sum-insured-weighted average assumption rates** — `7.8(b)` `q` over all lives and all future
   years; `7.9(a)` `q` over the next 12 months; `7.10(c)/(d)` `d_1`, `d_2`; `7.10(f)` termination
   rate `t`; `7.11(c)` present-value-weighted average expense inflation `i`.
8. **A future-discretionary-benefits balance and a management-action framework** — `6.2`, `6.3`,
   `9.1(5)`. The model must (a) report **TP without risk margin in respect of FDB** as a separate
   figure, since it caps `Adj_TP`; (b) support a **frozen-FDB** mode (`3.3A(1)(c)`) and a
   **responsive-FDB** mode (`6.3(2)(a)`); and (c) implement management actions compliant with
   *Technical Provisions – Further Requirements 8*, switchable off for the gross run. Granularity:
   per ring-fenced fund. Date: valuation date.
9. **Dynamic policyholder behaviour under stress** — `3.3A(2)(b)`: the model must reflect **any
   material adverse impact of the scenario, or of the management actions taken, on the likelihood
   that policyholders exercise options**. This is a *conditional* behaviour model, and it operates
   even in the gross run where FDB is frozen.
10. **Unit-linked and index-linked identification** — `2.3(5)`, `5.4(1)`, `5.4(3)(b)/(e)`,
    `5.4(4)(b)`. The model must tag technical provisions and earned premiums **where the investment
    risk is borne by policyholders**, and separately report **unit-linked expenses incurred in the
    previous 12 months**. Granularity: contract. Basis: last 12 months actuals for `Exp_ul`, and
    the 12 months before that for the operational growth surcharge.
11. **Earned premium history, two years** — `5.4(3)`: `Earn_life`, `Earn_life-ul`,
    `Earn_non-life` for the last 12 months and `pEarn_*` for the 12 months before, **gross of
    reinsurance premiums**.
12. **A ring-fenced-fund / MA-portfolio dimension on every output** — `9.1`. Every BEL, every
    stressed BEL, every FDB balance and every own-funds impact must be attributable to **a specific
    RFF, a specific MA portfolio, or the remaining part**. `9.1(4)`: at fund level only **restricted
    own funds** count. `9.1(9)`: **no cross-fund diversification** — the aggregation is a plain sum.
13. **The MA recomputation hook** — `3D25`. For an MA portfolio the model must be able to (a) apply
    an asset-value stress, (b) translate `stress_i` back into an **absolute spread increase** given
    the asset's modified duration, (c) multiply by the CQS **reduction factor** (45/50/60/75/100%),
    (d) add that to the fundamental spread on assigned assets, and (e) **re-derive the matching
    adjustment and re-discount the BEL**. This makes spread risk a liability-model calculation for
    a UK annuity writer, not an asset-only one.
14. **Scenario-selection bookkeeping** — `3B6.9`, `3C16.9`, `3D4.2`, `3D32.9`. For each "highest of"
    sub-module the model must retain **which scenario won on the NET basis** and report the gross
    number belonging to that scenario. It must also record, for `3.11A(3)`, **whether the
    interest-rate charge came from the up or the down scenario**, since that flips the coefficient
    `A` between 0 and 0.5 in the market correlation matrix.
15. **Zero-floor per sub-module** — `3.3A(5)`: any scenario that increases basic own funds
    contributes **zero**, not a negative amount. Apply before aggregation, per sub-module, per
    fund.
16. **Frozen items inside every scenario** — `3.3A(1)`: risk margin, deferred taxes and (gross run)
    FDB **must not move**. The model must be able to hold these constant while everything else
    revalues; this is a real implementation constraint if the risk margin is computed as a
    by-product of the same projection.
17. **Line-of-business and SLT/NSLT tagging** — `3.2A`, `3.10B`, `3C4`. Every obligation must carry
    the tag that decides life vs health module and, within health, SLT vs NSLT. For income
    protection the tag turns on whether the business is "pursued on a similar technical basis to
    that of life insurance" (`3C11.2`).
18. **Health-catastrophe exposure extracts** — `3C18.3`, `3C19.4`, `3C20.2`: sums insured by event
    type and country; number of insured lives per country; the value of benefits payable **assuming
    permanent work disability with no recovery** for the income-protection pandemic exposure `E`.
    These are exposure extracts, not projections, but the "no recovery" valuation is a projection
    run with recovery rates set to zero.
19. **Annual production plus an on-demand recalculation path** — `SCR-GP 4.1`, `4.3`, `4.4`. The
    model must be runnable **on demand** at any date, not only at year end, because `4.4` compels
    recalculation "without delay" on a significant risk-profile deviation.
20. **A standard-formula path even for internal-model firms** — SS15/16 ¶3.5 [R68]. The
    standard-formula stress harness must be maintained as a supported configuration.

---

## Product applicability

Products: **TA** term assurance, **CI** critical illness, **IP** income protection, **WOL** whole
of life, **WP** with-profits, **ULB** unit-linked bond, **PA** pension annuity.
Marks: `x` applies materially; `(x)` applies but secondary or conditional; `--` does not apply;
`?` cannot be determined from retrieved text; blank = not applicable by construction.

| Rule / item | TA | CI | IP | WOL | WP | ULB | PA |
|---|---|---|---|---|---|---|---|
| Life module `3B` applies at all [3.2A] | x | ? | -- | x | x | x | x |
| Health module `3C` applies at all [3.2A, 3.10B] | -- | ? | x | -- | -- | -- | -- |
| SLT vs NSLT branch [3.10B, 3C11.2] | | ? | SLT | | | | |
| Mortality +15% `3B1.1` | x | (x) | -- | x | x | (x) | -- |
| Longevity −20% `3B2.1` | -- | -- | -- | (x) | (x) | -- | x |
| Life disability-morbidity `3B3.1` | -- | ? | -- | -- | -- | -- | -- |
| Health mortality +15% `3C9.1` | | ? | (x) | | | | |
| Health longevity −20% `3C10.1` | | -- | (x) | | | | |
| Health IP disability-morbidity `3C13.1` | | ? | x | | | | |
| Expense +10% / inflation +1pp `3B4.1` / `3C14.1` | x | x | x | x | x | x | x |
| Life revision +3% `3B5.1` | -- | -- | -- | -- | -- | -- | (x) |
| Health revision +4% `3C15.1` | | -- | (x) | | | | |
| Lapse up ×1.5 `3B6.2` / `3C16.2` | x | x | x | x | x | x | -- |
| Lapse down ×0.5 `3B6.3` / `3C16.3` | (x) | (x) | (x) | x | x | x | -- |
| Mass lapse **70%** limb `3B6.6(1)` (RAO class VII) | -- | -- | -- | -- | -- | **--** | -- |
| Mass lapse **40%** limb `3B6.6(2)` / `3C16.6` | x | x | x | x | x | x | -- |
| Life catastrophe +0.15pp `3B7.1` | x | (x) | -- | x | x | (x) | -- |
| Health catastrophe `3C17`–`3C20` | | ? | x | | | | |
| Interest rate up/down `3D5`/`3D6` | x | x | x | x | x | (x) | x |
| Equity `3D9` + symmetric adjustment `3D12` | -- | -- | -- | (x) | x | x | (x) |
| Property −25% `3D15.1` | -- | -- | -- | (x) | x | (x) | (x) |
| Spread `3D17` (non-MA) | (x) | (x) | (x) | x | x | (x) | x |
| Spread on MA portfolio `3D25` | -- | -- | -- | -- | -- | -- | **x** |
| Concentration `3D26`–`3D31` | (x) | (x) | (x) | (x) | x | (x) | x |
| Currency ±25% `3D32` | (x) | (x) | (x) | (x) | x | (x) | (x) |
| Counterparty default type 1 `3E13` (reinsurance) | x | x | x | (x) | (x) | (x) | (x) |
| Counterparty default type 2 `3E15` | (x) | (x) | (x) | (x) | (x) | (x) | (x) |
| Operational — `Op_provisions` 0.45% leg `5.4(4)` | x | x | x | x | x | -- | x |
| Operational — `0.25 * Exp_ul` leg `5.4(1)` | -- | -- | -- | -- | (x) | **x** | -- |
| LACTP `Adj_TP` `6.3` | -- | -- | -- | (x) | **x** | -- | -- |
| LACDT `Adj_DT` `6.4` | x | x | x | x | x | x | x |
| Ring-fenced fund notional SCR `9.1` [R71] | -- | -- | -- | (x) | **x** | -- | -- |
| MA portfolio notional SCR `9.1` | -- | -- | -- | -- | -- | -- | **x** |
| USP available `2.3` [R65] | -- | -- | (x) | -- | -- | -- | (x) |

**Notes on every non-obvious mark.**

- **CI is marked `?` throughout the life/health split.** `3.2A` and `3.10B` decide the module by
  whether the obligation is a *health* obligation and by numbered line of business, and **the
  line-of-business list was not retrieved** [R73]. An accelerated critical illness rider on a term
  assurance and a standalone CI policy may fall differently. This is the single most consequential
  unresolved classification in this file; see Gaps §1.
- **IP marked SLT.** Justified from `3C11.2(2)`, which restricts the income-protection scenario to
  obligations "pursued on a similar technical basis to that of life insurance", and from `3C4`
  placing short-term income protection in NSLT segment 2. A UK long-term individual IP contract is
  SLT; an annually-renewable group scheme may be NSLT. The numbered line of business effecting the
  split is `?`.
- **Mortality `(x)` for CI and ULB.** For CI because a death benefit may be attached; for ULB
  because bonds typically carry a small (e.g. 100.1% of fund) death uplift, giving a small positive
  capital at risk. Life catastrophe carries the same reasoning.
- **Longevity `(x)` for WOL and WP.** WOL has no maturity, so lower mortality defers the claim and
  can increase TP for policies with high reserves relative to sum assured; WP funds commonly
  contain annuity liabilities. Neither is the primary driver.
- **Life revision `(x)` for PA, not `x`.** `3B5.1` bites **only** where benefits "could increase as
  a result of changes in the legal environment or in the state of health of the person insured". A
  standard UK level or RPI-escalating pension annuity has no such right, so the sub-module is
  normally **nil**; impaired-life annuities with a review mechanism, or annuities exposed to a
  Ogden-style legal change, would be in scope. Health revision `(x)` for IP for the analogous
  reason, but the health limb also catches **inflation**, which an index-linked IP claim annuity
  has.
- **Lapse `--` for PA.** A pension annuity in payment has no surrender or discontinuance right, so
  there is no "relevant option" under `3B6.4` and no discontinuance under the `1.2` definition.
- **Mass lapse 70% is `--` for ULB — this is the corrected rule.** `3B6.6(1)` as corrected [R64]
  covers **RAO Schedule 1 Part II class VII (pension fund management)** only; class III (linked
  long-term), which is where a unit-linked bond sits, was removed. Under PS15/24 as originally
  published [R63] this cell would have read `x` at 70%. Nothing in the seven-product set is class
  VII business, so the 70% limb is `--` across the whole table.
- **Interest rate `(x)` for ULB.** Unit-linked liabilities move with the unit fund, so the BEL is
  largely immunised; the exposure is in the present value of future charges and expenses, which is
  rate-sensitive but second-order.
- **Equity `(x)` for WOL and PA.** WOL where a non-profit fund holds some equity backing;
  PA because MA-eligible annuity portfolios are predominantly fixed income but may hold equity
  release or equity-like assets. `x` for WP and ULB is direct.
- **Spread `x` for PA and WOL, `(x)` elsewhere.** Protection business holds short assets and small
  reserves; annuity and WOL funds hold long credit. `3D25` is `x` for PA alone because only PA
  operates a matching adjustment portfolio in this library's product set.
- **Counterparty default type 1 `x` for TA/CI/IP.** UK protection business is heavily reinsured, so
  the reinsurance recoverable is the dominant type 1 exposure. `(x)` elsewhere.
- **Operational.** The `0.25 * Exp_ul` leg is `x` for ULB and `(x)` for WP, since a with-profits
  fund may write unit-linked business alongside; the `Op_provisions` 0.45% leg is `--` for ULB
  because `5.4(4)(b)` deducts `TP_life-ul`.
- **LACTP `x` for WP only, `(x)` for WOL.** `Adj_TP` is capped at FDB (`6.3(1)`), and only
  with-profits business carries material future discretionary benefits. WOL is `(x)` because a
  with-profits whole-of-life contract does, while a non-profit one does not.
- **LACDT `x` for all.** `6.4` operates at firm level, on the whole `BSCR + Adj_TP + SCR_op` loss.
- **RFF `(x)` for WOL.** Only if the WOL contract sits inside a with-profits fund [R71 ¶2.2].
- **USP `(x)` for IP and PA.** The revision-risk parameter only, and only where inflation risk is
  immaterial (`USP 7.1`) — which for an index-linked IP claim annuity it generally is not.

---

## Gaps and caveats

### 1. Not retrieved — the annexes, and what they take with them

- **The Annexes to the SCR – Standard Formula Part were NOT retrieved** [R73]. Rule `2A.1` says
  only "The Annexes referred to in **3A, 3C and 7** can be found here". Consequently the following
  are **not stated anywhere in this file and must not be inferred**: **Annex XVI** — the country
  list, the ratio of persons affected by a mass accident `r_s`, the event types `e`, the benefit
  ratios `x_e`, the healthcare-utilisation types `h` and the ratios `H_h` for the pandemic
  sub-module; the **geographical diversification** annex behind `3A5` and `3C3.8`; and Annexes V,
  VI, VII, VIII and X (non-life catastrophe risk zones and weights).
- **The line-of-business list was NOT retrieved.** `3.10B` allocates health obligations to NSLT
  (lines 1, 2, 3, 13, 14, 15, 25) and SLT (lines **29, 33, 35**) by number, and `3.18(3)` excludes
  lines 9, 21 and 28. Without the list, **the mapping of a UK critical illness or income protection
  contract to a numbered line of business is `[unverified]`**. This is why CI is marked `?` in the
  applicability matrix.
- **`SCR-SF 1.2` has a future version after 01/01/2027 that was not retrieved.** Definitions
  including "symmetric adjustment", "standard equity capital charge" and "health underwriting risk"
  may change; nothing in this file describes the post-01/01/2027 position.
- **Past versions not retrieved:** `SCR-GP 3.1`, `6.5`, `6.6`; `SCR-SF 1.2`, `3.1`, `3.6`, `3.8`,
  `3.9`, `3.10`, `3.10A`, `3.11`, `3.11A`, `3D7.2`, `3D9.2`, `3D17.4`, `3B6.6`, `3C6.1`, `5.3`,
  `6.1`, `9.1` all show "Past version before …" links that were not followed. Anyone documenting
  the position **before 31/12/2024** cannot rely on this file.
- **The SAECC spreadsheet (XLSX) was not retrieved** [R67]. **No symmetric adjustment value is
  stated in this file**, at any date.
- **SoP4/24 [R69] and SoP11/24 [R70] were not read in substance.** For SoP4/24 only the title page
  and scope were verified; the **quantitative thresholds for a significant risk profile deviation
  are not transcribed**. For SoP11/24 only the landing-page scope statement was retrieved; **the
  SoP PDF itself was not fetched**.
- **The mapping tables in PS12/25 Appendix 6 were not transcribed** [R72]. Every CQS-dependent
  number in §9 (`3D17.3`, `3D25`, `3D29`, `3D30`) needs an ECAI-to-CQS mapping this file does not
  supply.
- **SS5/15 (pension scheme risk) and SS20/16 (reinsurance counterparty credit risk)** are listed as
  related guidance on both SCR Parts and were **not retrieved**.

### 2. Extraction defects — recorded, not silently corrected

- **Life correlation matrix `3.8(3)`: the "Mortality" ROW label is missing** in the rendered HTML.
  Verified in both the raw and cleaned extractions. The row is identified by symmetry (its values
  match the first column of every other row in all six cases). **Confidence: high, but it is an
  inference, not a read label.**
- **Spread table `3D17.3`: the rated table has SIX credit-quality-step column pairs**, with the
  last headed "5 and 6". The `a_i`/`b_i` header repeats exactly six times and every data row has
  exactly six pairs, so the extraction is internally consistent. **Whether the PRA genuinely merged
  CQS 5 and 6 (the revoked DR Art. 176 table had seven columns) was NOT cross-checked** — the
  legislation.gov.uk retrieval covered Art. 142 only, not Art. 176. Marked `[unverified]`.
- **`3D17.3`, row ">15 to 20", CQS 1: renders as `11 .0%`** with a stray space. Read as 11.0%.
- **`3D17.4`, unrated bonds, row ">5 to 10: `15 + 1.7% * (dur_i - 5)`"** — the percent sign after
  "15" is **absent in the source text**. Every neighbouring expression uses percentages, so this is
  almost certainly `15%`, but it is transcribed as rendered and marked `[unverified]`.
- **`3D6.1` downward interest-rate shocks are non-monotonic at maturities 14–20** (28, 27, 28, 28,
  28, 29, 29). This is what the source shows. **It was not cross-checked against the revoked DR
  Art. 167 table**, so whether the shape is genuine or an extraction artefact is `[unverified]`.
  Note the upward table is monotonically decreasing throughout, which makes the downward table's
  shape conspicuous.
- **`5.4(3)` `Op_premiums`: the extracted LaTeX has mismatched brackets.** The reading in §12.3 is
  reconstructed from the defined terms `5.4(3)(a)`–`(f)` and the standard structure (base rates plus
  a 1.2× growth surcharge). **The exact bracketing of the second `max` term is `[unverified]`** —
  specifically, whether the non-life growth surcharge sits inside or outside the same `max` as the
  life one. A drafter must re-read `5.4(3)` before restating the formula.
- **`3C3` paragraph numbering skips from 5 to 7** in the retrieved text (there is no `3C3.6`), and
  `3C3.5` cross-refers to "`3C3.3`(a), (c) and (d)" where `3C3.3` has limbs (1)–(4). Both are as
  rendered; whether a paragraph was deleted or lost in extraction is `[unverified]`.
- **`3C5.2` cross-refers to `3C5.3` for `sigma_(prem,s)` and to `3C4` for `sigma_(res,s)`**, but
  `3C5.3` in turn refers back to `3C4` — recorded as read.
- **`USP 7.5` opens "A USP firm using RESERVE risk method must calculate the increase in the amount
  of annuity benefits"** — plainly a drafting slip for *revision* risk method, since the whole of
  chapter 7 is the revision risk method. Recorded, not corrected.

### 3. Conflicts between sources — recorded, not resolved

- **The mass-lapse correction statement conflicts with itself on the class list.** [R64] narrates
  that the 2015 transposition table "identified business in **class II ('Marriage and birth') and
  class VII ('Pension fund management')**" as within scope of the 70% stress, but then says the
  correct restatement "should only require firms to apply a 70% stress … to **RAO class VII(a) and
  class VII(b)** business". The live rule text in [R62] names **class VII only** — no class II. The
  operative position is therefore class VII only, but the discrepancy between the statement's
  narrative and its conclusion is unexplained and is recorded here rather than smoothed over.
- **`3.3A(1)(d)` says "no management actions are taken by the firm during the scenario";
  `3.3A(2)(a)` says the firm must take account of "future management actions following the
  scenario, provided they comply with Technical Provisions – Further Requirements 8", expressly
  "without prejudice to (1)(d)".** The two are difficult to reconcile on their face. The reading
  offered in §3.2 (that (1)(d) excludes new discretionary responses while (2)(a) preserves the
  pre-agreed framework) is **this file's interpretation, not a quoted rule**, and is flagged as
  such. It is also *not* what `6.3(2)(b)` does — that rule switches management actions on for the
  net run, which would be redundant if they were already on in the gross run.
- **PS15/24 ¶6.16 and ¶6.18 remain published and unamended** even though [R64] states it
  "supersedes the feedback previously provided" in them. Anyone reading PS15/24 alone will get the
  wrong mass-lapse scope.
- **`3D25` uses a seven-column CQS table (0–6) while `3D17.3` uses six (0–4, "5 and 6")** in the
  same chapter. Recorded; see §2 above.

### 4. Numbers deliberately not transcribed

- SoP4/24 capital add-on significance thresholds [R69].
- The ECAI-to-CQS mapping tables in PS12/25 Appendix 6 [R72].
- `3E4`–`3E12`: the loss-given-default definitions, the risk-adjusted collateral and mortgage
  values, and the **probability-of-default table by credit quality step**. Only the `3E13`
  step-function and the `3E14` variance formulas were transcribed.
- `3D27`, `3D28`: the concentration aggregation formula and the excess-exposure definition. Only
  the `CT_i` and `g_i` tables were transcribed.
- `3D18`–`3D24`: internal credit assessment, securitisation spread risk (a very long sub-chapter),
  credit derivatives, and the specific-exposure carve-outs. Surveyed only.
- `3D33`, `3D34`: the adjusted currency factors for euro-pegged currencies. Not applicable to a
  GBP-functional UK life insurer, and not transcribed.
- `3A`: the entire non-life underwriting risk module, including the `3A3` segment standard
  deviations and all catastrophe sub-modules. Out of scope for this library; only the `3.6A`
  non-life correlation matrix (premium&reserve / catastrophe / lapse = 1, 0.25, 0; 0.25, 1, 0;
  0, 0, 1) was read.
- `3G2`–`3G9`: the risk-mitigation qualitative criteria, effective transfer, basis risk,
  counterparty status, collateral and guarantee conditions.
- `USP 4`, `5`, `6`, `8`, `9`, `10`: the premium, reserve, non-proportional and credibility-factor
  methods. Only chapter 7 (revision risk) was transcribed, and even there `7.6`–`7.9` and the
  credibility-factor table in `USP 10` were not.
- `7.16`–`7.27`: the health and remaining simplifications.

### 5. Questions the retrieved sources do not settle

1. **Which numbered line of business a UK accelerated critical illness rider, a standalone CI
   policy, and a long-term individual income protection policy fall into** — and therefore whether
   CI is a life or a health obligation under `3.2A`/`3.10B`. Requires the line-of-business annex
   [R73].
2. **Whether a UK unit-linked bond can ever be class VII business.** The corrected rule turns
   entirely on RAO Schedule 1 Part II class VII [R14]; nothing retrieved addresses hybrid
   pension-linked bonds.
3. **How `9.1(6)`'s firm-wide worst-scenario selection interacts with `3.11A(3)`'s coefficient
   `A`.** If the firm-wide worst interest-rate scenario is "down" but a particular RFF's worst is
   "up", it is not stated whether `A` is set once firm-wide or per notional SCR. Nothing retrieved
   resolves this.
4. **Whether `3.3A(1)(a)`'s frozen risk margin survives into the `6.3(2)` net run.** `6.3(2)` lists
   four modifications to the BSCR and freezing the risk margin is not among the things it unfreezes,
   which implies it stays frozen — but the rule does not say so.
5. **Whether the `5.3(2)` "30% of the basic SCR relating to those operations" cap is the same
   constraint as the `min(0.3 * BSCR; Op)` term in `5.4(1)`.** `5.3` speaks of the BSCR *relating
   to those operations* (i.e. excluding unit-linked); `5.4(1)` applies 0.3 to the whole BSCR.
   Recorded as an apparent inconsistency between the principle and the formula.
6. **What "the mortality rates used for the calculation of technical provisions" means when the
   best estimate uses a CMI projection model** [R30] — whether the 15%/20% shock applies to the
   base table, to the projected rates, or to both, and whether the projection parameters themselves
   are shocked. No retrieved source addresses this, and it materially changes the longevity charge
   for a pension annuity book.
7. **Whether the `3B6.2` 100% cap and the `3B6.3` 20-percentage-point cap are applied before or
   after the per-policy TP-increase selection.** The rule text orders them as cap-then-select;
   whether that is intended is not stated.
8. **The treatment of the transitional measure on technical provisions [R3] inside a stress.**
   `3.3A` freezes the risk margin and FDB but says nothing about TMTP. Stream A/B territory, flagged
   here because it changes the loss in basic own funds.

### 6. Fetch behaviour observed on 2026-08-06

- `prarulebook.co.uk` returns **HTTP 403** to plain fetchers and **200** to a browser User-Agent.
  Both rulebook URLs used here ([R61] general provisions, [R65] USP) were **independently
  re-verified** during this pass and resolved correctly at the `/05-08-2026` as-at path.
- `bankofengland.co.uk` behaves the same way; PDFs extract to text acceptably (SS15/16, SoP4/24)
  but XLSX attachments do not and were not attempted.
- `legislation.gov.uk` responds to plain fetchers. Its **point-in-time** view is the one that
  carries the operative Article text for a revoked regulation; the "latest" view carries the
  revocation annotation and little else.
- The SCR – Standard Formula Part is **452,843 characters** and exists on disk under four different
  filenames from four different retrieval passes. They are the **same document**; a drafter should
  not treat them as corroborating sources.
