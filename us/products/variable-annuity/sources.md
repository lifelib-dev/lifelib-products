# Sources — Variable Annuity with Living and Death Benefit Guarantees (United States)

Source ids, titles, publishers, URLs, access dates and fetched/not-fetched markers are
carried over **verbatim** from `us/_research/variable-annuity.md`, the citation ground
truth for the [S#]/[R#] tags used in `product-spec.md` and `technical-notes.md`. **Ids are
never renumbered.** Sources present in the research file but not cited in either document
are dropped; **none were dropped here — all of S1–S8 and R1–R13 are cited.** No new
sources were fetched at drafting, so nothing below is marked "added at drafting".

Access date for all citations: **2026-08-04**, except the frozen R1–R72 cross-product
entries reproduced in full below, whose own access dates (2026-08-03 or 2026-08-04) are
carried over unchanged from `us/regulatory/sources.md`.

Retrieval note carried over from the research file: `sec.gov` and `efts.sec.gov` return
HTTP 403 to a plain fetch. All SEC documents below were retrieved with an explicit declared
User-Agent (SEC's stated requirement for programmatic access) and read in full as text.
Every document marked "Retrieved: YES" was actually downloaded and read.

---

## Primary product sources [S#]

### S1. Jackson National Life Insurance Company — Perspective II® Flexible Premium Variable and Fixed Deferred Annuity — statutory prospectus dated April 28, 2025
- Publisher: Jackson National Life Insurance Company, through Jackson National
  Separate Account – I (CIK 0000927730)
- Doc type: SEC Form N-4 statutory prospectus, filed as Form 485BPOS
  (accession 0000927730-25-000086), ~4.9 MB HTML
- URL fetched: https://www.sec.gov/Archives/edgar/data/927730/000092773025000086/ck0000927730-20250422.htm
- Retrieved: YES (converted to ~1.28 MB plain text and read in relevant part)
- Role in this library: **implementation anchor.** Full GLWB/GMDB algebra (GWB, GAWA,
  Bonus Base, step-up, GWB adjustment, excess-withdrawal proportional reduction), the
  charge-increase/opt-out mechanic, the contract-value-zero regime, and Appendices F–J of
  historical rate tables.

### S2. Jackson National Life Insurance Company — Perspective II® Initial Summary Prospectus (Summary Prospectus for New Investors), April 28, 2025
- Publisher: same as S1; filed as exhibit EX-99.(o)(1) to the S1 registration statement
- Doc type: Rule 498A Initial Summary Prospectus (~16 pages)
- URL fetched: https://www.sec.gov/Archives/edgar/data/927730/000092773025000086/jnlpiiafter6-24x19initials.htm
- Retrieved: YES (full text read)
- Role in this library: the base contract charge stack, withdrawal charge schedule,
  contract maintenance charge, fund expense range and premium limits.

### S3. Jackson National Life Insurance Company — Rate Sheet Prospectus Supplement dated April 27, 2026 (Perspective II)
- Publisher: same as S1; SEC Form 497 (accession 0000927730-26-000157)
- Doc type: rate sheet prospectus supplement (6 pages) — the document that carries
  the *currently offered* rider charges, GAWA percentages, bonus percentages, GWB
  adjustment percentages and GMDB roll-up percentages
- URL fetched: https://www.sec.gov/Archives/edgar/data/927730/000092773026000157/jnlpiiafter6-24x19rateshee.htm
- Retrieved: YES (full text read)
- Role in this library: the **dated current parameter set** (rate-sheet date 2026-04-27) for
  the representative GLWB and GMDB elections.

### S4. American General Life Insurance Company (Corebridge Financial) — Polaris Advisory Variable Annuity — prospectus dated May 1, 2026
- Publisher: American General Life Insurance Company, Variable Separate Account
  (CIK 0000729522); SEC Form 485BPOS, accession 0001193125-26-186414
- URL fetched: https://www.sec.gov/Archives/edgar/data/729522/000119312526186414/d79162d485bpos.htm
- Retrieved: YES (~732 KB plain text; fee table, living-benefit and death-benefit
  sections, Appendix C fee formula and Appendix H examples read)
- Role in this library: the **VIX-linked non-discretionary rider fee formula** variant, the
  Secure Value Account investment requirement, the daily-step-up design, and the cited fact
  that the rider fee stops when contract value falls to zero.

### S5. American General Life Insurance Company (Corebridge) — Rate Sheet Prospectus Supplement dated May 1, 2026 (Polaris Advisory)
- Doc type: SEC Form 497, accession 0001193125-26-164551 (3 pages)
- URL fetched: https://www.sec.gov/Archives/edgar/data/729522/000119312526164551/d113668d497.htm
- Retrieved: YES (full text read)
- Role in this library: cited for the rate-sheet mechanism (current withdrawal and income
  percentages reset by Form 497 filing with a 10-day advance-filing commitment).

### S6. American General Life Insurance Company (Corebridge) — Polaris Choice IV — prospectus dated May 1, 2026
- Doc type: SEC Form 485BPOS, accession 0001193125-26-173379
- URL fetched: https://www.sec.gov/Archives/edgar/data/729522/000119312526173379/d97533d485bpos.htm
- Retrieved: YES (~503 KB plain text; fee table, penalty-free withdrawal, nursing
  home waiver, purchase-payment and issue-age rules read)
- Carried-over note: "This contract is no longer available for purchase by new
  contract Owners." [S6] — it is a recently-sold, currently-in-force design.
- Role in this library: the commission-share charge/withdrawal-charge trade-off, the
  ±0.25%-per-quarter VIX fee band for the commission class, and the GLWB RMD relief rule.

### S7. Equitable Financial Life Insurance Company / Equitable Financial Life Insurance Company of America — Retirement Cornerstone® Series — prospectus dated May 1, 2026
- Publisher: Separate Account No. 70 (CIK 0001537470) and Equitable America
  Variable Account No. 70A; SEC Form 485BPOS, accession 0001193125-26-169230
- URL fetched: https://www.sec.gov/Archives/edgar/data/1537470/000119312526169230/d120089d485bpos.htm
- Retrieved: YES (~1.45 MB plain text; definitions, benefits, GIB mechanics,
  charges and expenses sections read)
- Role in this library: the **unbundled daily charge components** (the source of the 0.30%
  administrative component in the representative charge decomposition), the
  **Treasury-formula roll-up rate** variant (10-year CMT + 1.00%, floored 4%, capped 8%),
  the bifurcated account architecture, and the annual (not quarterly) rider charge
  frequency exception.

### S8. The Lincoln National Life Insurance Company — Lincoln ChoicePlus℠ product suite / Lincoln ChoicePlus Assurance℠ — Form N-4 post-effective amendment filed April 23, 2026 (prospectuses and rate sheets dated May 1, 2026)
- Publisher: Lincoln Life Variable Annuity Account N (CIK 0001048606); SEC Form
  485BPOS, accession 0001104659-26-047599 (~20 MB HTML bundling several rate-sheet
  supplements and prospectuses)
- URL fetched: https://www.sec.gov/Archives/edgar/data/1048606/000110465926047599/tm265235d1_485bpos.htm
- Retrieved: YES (~2.68 MB plain text; the three Lincoln ProtectedPay®/4LATER®/
  i4LIFE® rate sheets, the Key Information and Fee Tables, the ProtectedPay
  Enhancement/Account Value Step-up mechanics, and Appendix C discontinued-rider
  charges were read)
- Role in this library: the **step-up-triggered fee reset** variant with its reversing
  opt-out and the no-opt-out $100,000-premium trigger; the **two-table post-depletion
  payout** variant; the explicit enhancement-vs-step-up mutual-exclusivity rule that
  settles the [std] bonus/step-up ordering; and the GMDB-priced-into-M&E design.
- Carried-over caveat: Lincoln share-class attribution is ambiguous — the accession bundles
  several rate sheets and prospectuses, and the fee table read cannot be attributed with
  certainty to a single named product among the ChoicePlus Assurance share classes.

---

## Regulatory and actuarial references [R#] (product research file numbering)

### R1. NAIC — Valuation Manual, Jan. 1, 2026 Edition — **VM-21: Requirements for Principle-Based Reserves for Variable Annuities**
- Publisher: National Association of Insurance Commissioners
- URL fetched: https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf
- Retrieved: YES (457-page PDF downloaded; VM-21 occupies PDF pages 142–226,
  manual pages 21-1 through 21-76; Sections 1, 2, 3, 4, 6, 7, 10 read)

### R2. NAIC / Oliver Wyman — "Variable Annuity Statutory Reserve and Capital Reform — QIS II Executive Summary", February 12, 2018
- Publisher: NAIC Variable Annuities Issues (E) Working Group (report by Oliver Wyman)
- URL fetched: https://content.naic.org/sites/default/files/committee_related_documents/cmte_e_va_issues_wg_related_qis_ii_executive_summary.pdf
- Retrieved: YES (13-page PDF; background and QIS I/QIS II overview read)

### R3. NAIC — Life Risk-Based Capital instructions, **LR027 Interest Rate Risk and Market Risk** (C-3 Phase II for VAs)
- Publisher: NAIC Capital Adequacy (E) Task Force
- URL fetched: https://content.naic.org/sites/default/files/inline-files/LR027%20mod%20for%20vol%20res%202020.pdf
- Retrieved: YES (5-page PDF; full 7-step process, CTE(98) definition, RBC formula,
  phase-in and smoothing read)

### R4. American Academy of Actuaries — "Implementation of Requirements for Principle-Based Reserves for Variable Annuities – 2022 Edition of VM-21" (Practice Note Supplement), February 2022
- Publisher: Variable Annuity Reserves & Capital Work Group, Life Practice Council, AAA
- URL fetched: https://actuary.org/wp-content/uploads/2022/02/VA_PN_Supplement_Final.pdf
- Retrieved: YES (34-page PDF; introduction, acronym list, background, C-3 Phase 2
  Q&A and disclosures Q&A read)

### R5. American Academy of Actuaries — "Utilization Assumptions of Guaranteed Living Benefits for Deferred Annuities: A Resource and Discussion Guide", May 2024
- Publisher: Life Experience Committee, AAA (Donna Claire, chair)
- URL fetched: https://actuary.org/sites/default/files/2024-05/life-paper-GLBs.pdf
  (note: `www.actuary.org` 301-redirects to `actuary.org`; the redirect target was
  fetched directly)
- Retrieved: YES (18-page PDF, read in full including both sample utilization tables)
- Carried-over caveat: the sample utilization tables are built for a **non-qualified FIA**,
  not a VA, and must be applied with care.

### R6. U.S. Securities and Exchange Commission — **Form N-4** (reference copy, version effective September 23, 2024)
- URL fetched: https://www.sec.gov/files/formn-4.pdf
- Retrieved: YES (65-page PDF; general instructions and item index read)
- Note: this product research file retrieved Form N-4 successfully with a declared
  User-Agent; the cross-product entry [REG-R52] records a **failed** fetch of the same URL
  (HTTP 403). Prefer [R6] for first-hand Form N-4 facts.

### R7. SEC Rule 498A, 17 CFR 230.498A — summary prospectuses for variable annuity and variable life contracts
- URL fetched: https://www.law.cornell.edu/cfr/text/17/230.498A
- Retrieved: YES

### R8. FINRA Rule 2330 — Members' Responsibilities Regarding Deferred Variable Annuities
- URL fetched: https://www.finra.org/rules-guidance/rulebooks/finra-rules/2330
- Retrieved: YES

### R9. Internal Revenue Code § 72 — Annuities; certain proceeds of endowment and life insurance contracts
- URL fetched: https://www.law.cornell.edu/uscode/text/26/72
- Retrieved: YES

### R10. Treas. Reg. § 1.817-5 — Diversification requirements for variable annuity, endowment, and life insurance contracts
- URL fetched: https://www.law.cornell.edu/cfr/text/26/1.817-5
- Retrieved: YES

### R11. Actuarial Standards Board — ASOP No. 52, "Principle-Based Reserves for Life Products under the NAIC Valuation Manual"
- URL fetched: http://www.actuarialstandardsboard.org/asops/principle-based-reserves-life-products-naic-valuation-manual/
- Retrieved: YES
- Carried-over caveat: the retrieved text scopes ASOP 52 to policies "subject to **VM-20**
  requirements". Treat any claim that "ASOP 52 governs VM-21" as [unverified].

### R12. Actuarial Standards Board — Standards of Practice index (titles and effective dates for ASOP Nos. 22, 52, 56)
- URL fetched: http://www.actuarialstandardsboard.org/standards-of-practice/
- Retrieved: YES

### R13. Society of Actuaries Research Institute & LIMRA — "2022–2024 Variable Annuity Guaranteed Living Benefit / Contract Holder Behavior Study"
- URL fetched: https://www.soa.org/resources/experience-studies/2025/2022-24-va-livingbenefit/
- Retrieved: YES (landing page only — the detailed report is a paid data package)

---

## Cross-product regulatory references [REG-R#]

These are cited with the **[REG-R#]** prefix to avoid collision with the product research
file's own R-numbering. They resolve against a **single shared numbering space running
R1–R150**, curated at `us/references/regulatory-and-actuarial-references.md`, with
**R114–R124** and **R143–R149** permanently **unused by design** — block reservations that
let parallel research streams number independently, not losses, and they must never be
back-filled:

- **R1–R34** — research provenance `us/_research/regulatory-actuarial.md` (the original
  life bibliography; several entries also bind annuity models, and that file's companion
  table records how each one applies).
- **R35–R72** — research provenance `us/_research/regulatory-actuarial-annuities.md` (the
  annuity continuation of the same space; it opens at R35 precisely because R1–R34 are
  frozen and must not be renumbered).
- **R73–R142** — the statutory accounting and capital block: `us/_research/statutory-accounting.md`
  (R73–R99), `us/_research/statutory-reserves.md` (R100–R113) and
  `us/_research/risk-based-capital.md` (R125–R142). Its per-entry bibliography is
  `us/regulatory/sources.md`, from which the entries reproduced below are carried verbatim.

Entries from the **R1–R72** blocks cited by the two documents in this directory:

| Tag | Short title | Research file | Retrieval status (per that file) |
|---|---|---|---|
| REG-R15 | 26 U.S.C. §817 (esp. §817(h)) — variable contract diversification | regulatory-actuarial.md | fetched |
| REG-R16 | 26 U.S.C. §807 — tax reserves | regulatory-actuarial.md | fetched |
| REG-R26 | ASOP No. 2 — Nonguaranteed Elements for Life Insurance and Annuity Products | regulatory-actuarial.md | fetched |
| REG-R27 | ASOP No. 7 — Life or Health Cash Flow Analysis | regulatory-actuarial.md | fetched |
| REG-R29 | ASOP No. 22 — Opinions Based on Asset Adequacy Analysis | regulatory-actuarial.md | fetched |
| REG-R31 | ASOP No. 52 — PBR for **Life** Products under the Valuation Manual | regulatory-actuarial.md | fetched |
| REG-R32 | ASOP No. 56 — Modeling | regulatory-actuarial.md | fetched |
| REG-R34 | FASB ASU 2018-12 (LDTI) — market risk benefits | regulatory-actuarial.md | **no (fasb.org 403)** — substance corroborated only from secondary summaries and carried as [unverified] in that file |
| REG-R35 | VM-21 — PBR for Variable Annuities (Valuation Manual, Jan. 1, 2026 ed.) | regulatory-actuarial-annuities.md | yes (local text extraction) |
| REG-R36 | VM-22 — PBR for Non-Variable Annuities (Jan. 1, 2026 ed.) | regulatory-actuarial-annuities.md | yes (local text extraction) |
| REG-R37 | VM-V §1 — Income Annuities, maximum valuation interest rates | regulatory-actuarial-annuities.md | yes (local text extraction) |
| REG-R38 | Actuarial Guideline XLIII (AG 43) — CARVM for Variable Annuities (VAIWG redline) | regulatory-actuarial-annuities.md | yes (local text extraction) |
| REG-R42 | Standard Nonforfeiture Law for Individual Deferred Annuities (Model #805) | regulatory-actuarial-annuities.md | yes (local text extraction) |
| REG-R43 | Variable Annuity Model Regulation (Model #250) | regulatory-actuarial-annuities.md | yes (local text extraction) |
| REG-R44 | Actuarial Guideline LIV (AG 54) — ILVA nonforfeiture | regulatory-actuarial-annuities.md | yes (local text extraction, complete) |
| REG-R45 | Annuity Disclosure Model Regulation (Model **#245**) | regulatory-actuarial-annuities.md | yes (local text extraction) |
| REG-R46 | Suitability in Annuity Transactions Model Regulation (Model #275) | regulatory-actuarial-annuities.md | yes (local text extraction) |
| REG-R47 | C-3 RBC Instructions and Appendices (C-3 Phase II for VAs) | regulatory-actuarial-annuities.md | yes (local text extraction) |
| REG-R48 | Oliver Wyman / VAIWG — QIS II Public Report and Executive Summary | regulatory-actuarial-annuities.md | yes (local text extraction, both) |
| REG-R50 | SEC Release 33-10765 — Rule 498A adopting release | regulatory-actuarial-annuities.md | yes (via govinfo); sec.gov PDF 403 |
| REG-R51 | 17 C.F.R. §230.498A (current text, extended to registered non-variable annuities) | regulatory-actuarial-annuities.md | fetched |
| REG-R52 | SEC Form N-4 | regulatory-actuarial-annuities.md | **no (sec.gov 403)** — but fetched first-hand as [R6] above |
| REG-R54 | FINRA Rule 2330 | regulatory-actuarial-annuities.md | fetched (same rule as [R8] above) |
| REG-R55 | 26 U.S.C. §72 — Annuities | regulatory-actuarial-annuities.md | fetched (same statute as [R9] above) |
| REG-R56 | 26 U.S.C. §1035 — Certain exchanges of insurance policies | regulatory-actuarial-annuities.md | fetched |
| REG-R57 | 26 C.F.R. §1.401(a)(9)-6 — RMDs for annuity contracts (QLAC rules) | regulatory-actuarial-annuities.md | fetched |
| REG-R58 | T.D. 10001 — RMD final regulations (July 19, 2024) | regulatory-actuarial-annuities.md | yes (via govinfo) |
| REG-R59 | Model #821 + VM-M — 2012 IAM / 2012 IAR / Scale G2 annuity mortality | regulatory-actuarial-annuities.md | yes (local text extraction, both) |
| REG-R61 | 2020–2024 Individual Payout Annuity Mortality Experience Study | regulatory-actuarial-annuities.md | yes (landing page) |
| REG-R62 | FIA Policyholder Behavior Experience Studies (2021–22, 2019–20) | regulatory-actuarial-annuities.md | yes (both landing pages) |
| REG-R64 | VA Contract Holder Behavior / GLB Utilization Studies (2022–24 and predecessors) | regulatory-actuarial-annuities.md | yes (2022–24 landing page; same landing page as [R13] above) |
| REG-R66 | AAA — VM-21 Practice Note Supplement (Feb. 2022) | regulatory-actuarial-annuities.md | yes (local text extraction; same document as [R4] above) |
| REG-R67 | AAA — Utilization Assumptions of Guaranteed Living Benefits (May 2024) | regulatory-actuarial-annuities.md | yes (local text extraction; same document as [R5] above) |
| REG-R70 | ASOP No. 54 — Pricing of Life Insurance and Annuity Products | regulatory-actuarial-annuities.md | fetched |
| REG-R71 | ASOP No. 10 — U.S. GAAP for Long-Duration Life, Annuity, and Health Products | regulatory-actuarial-annuities.md | yes (local text extraction) |
| REG-R72 | IRS LB&I §807 directive (AG 43/VM-21 tax reserves) | regulatory-actuarial-annuities.md | **no (irs.gov 404)** — substance [unverified] |

Note on overlaps: [R1]/[REG-R35], [R4]/[REG-R66], [R5]/[REG-R67], [R8]/[REG-R54],
[R9]/[REG-R55], [R11]/[REG-R31] and [R13]/[REG-R64] are the **same documents** reached
through two numbering spaces. Where a fact was extracted first-hand in the product research
file, the [R#] tag is used; where the fact comes from the cross-product annotation, the
[REG-R#] tag is used. Both are given where both apply.

### Statutory accounting and capital entries (R3 and R73–R142) newly cited here

Added when the *Statutory accounting and capital* section was written into
`technical-notes.md` and the corresponding paragraph into `product-spec.md`. Ids, titles,
publishers, URLs, access dates, fetched markers and every carried-forward limit or
[unverified] flag are reproduced **verbatim** from `us/regulatory/sources.md`; **nothing is
renumbered and no flag is upgraded**. No new source was fetched at drafting. Cross-references
*inside* these entries to ids not reproduced here — chiefly **R73**, the AP&P Manual *As of
March 2026*, and R81, R86 and R141 — resolve in `us/regulatory/sources.md` and
`us/references/regulatory-and-actuarial-references.md`.

#### REG-R3. Valuation Manual, Jan. 1, 2026 Edition (VM-01, VM-02, VM-20, VM-31, VM-M, VM-G, VM-C, VM-V, …)
- **Publisher:** NAIC
- **URL:** https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf
- **Accessed:** 2026-08-03 · **Fetched:** yes (457-page PDF retrieved; cover, adoption
  history, and full table of contents read; "NAIC Adoptions through August 13, 2025"). The
  reserves stream additionally read VM-01 definitions and VM-20 §§1, 2, 3.B–3.E, 4, 5, 6,
  7.A/7.B by local text extraction.
- Note for this directory: the same PDF is [R1] (VM-21) and [REG-R35]/[REG-R36]/[REG-R37];
  [REG-R3] is used only where the citation is to the Valuation Manual's **VM-20** half.

#### REG-R75. SSAP No. 71 — Policy Acquisition Costs and Commissions (*As of March 2026*)
- **Publisher:** NAIC (in R73, statement pages 71-1 to 71-3)
- **URL:** https://content.naic.org/sites/default/files/publication-app-manual.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; ¶¶1–7 read in full)

#### REG-R78. SSAP No. 50 — Classifications of Insurance or Managed Care Contracts (*As of March 2026*)
- **Publisher:** NAIC (in R73, statement pages 50-1 onward)
- **URL:** https://content.naic.org/sites/default/files/publication-app-manual.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; ¶¶1–20 read)

#### REG-R79. SSAP No. 51 — Life Contracts (*As of March 2026*; historically cited as SSAP No. 51R)
- **Publisher:** NAIC (in R73, statement pages 51-1 to 51-13)
- **URL:** https://content.naic.org/sites/default/files/publication-app-manual.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; status block, ¶¶1–16 read; section index read)
- **Limit carried forward:** ¶¶17 onward (mean/mid-terminal reserves, dividends, coupons,
  accelerated benefits, disclosures) were read through the **section index and the parallel
  Issue Paper No. 51 text (R81)**, not the SSAP paragraphs. Paragraph numbers differ between
  IP 51 and SSAP No. 51; a precise SSAP No. 51 paragraph cite needs R73 at pages 51-5 to 51-12.

#### REG-R80. SSAP No. 52 — Deposit-Type Contracts (*As of March 2026*)
- **Publisher:** NAIC (in R73, statement pages 52-1 to 52-8)
- **URL:** https://content.naic.org/sites/default/files/publication-app-manual.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; ¶¶1–17 read in full)

#### REG-R83. SSAP No. 56 — Separate Accounts (*As of March 2026*)
- **Publisher:** NAIC (in R73, statement pages 56-1 to 56-14)
- **URL:** https://content.naic.org/sites/default/files/publication-app-manual.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; ¶¶1–31 and the glossary read)

#### REG-R87. INT 23-01 — Net Negative (Disallowed) Interest Maintenance Reserve (revised print, adopted August 11, 2025)
- **Publisher:** NAIC Statutory Accounting Principles (E) Working Group (AP&P Appendix B)
- **URL:** https://content.naic.org/sites/default/files/inline-files/22-19%20-%20INT%2023-01%20-%20Revised%20April%202025.pdf
  (original clean adoption print, August 13, 2023:
  https://content.naic.org/sites/default/files/inline-files/22-19a%20-%20INT%2023-01%20-%20IMR%20clean.pdf — also fetched)
- **Accessed:** 2026-08-04
- **Fetched:** yes, both (local text extraction; 8 pages each; the revised print carries
  visible tracked-change artefacts, which is how the extension is evidenced)

#### REG-R88. SAPWG 2026 Spring National Meeting — Meeting Summary Report (March 23, 2026)
- **Publisher:** NAIC Statutory Accounting Principles (E) Working Group
- **URL:** https://content.naic.org/sites/default/files/national_meeting/2026-spnm-summary-e-sapwg.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; 3 pages, read in full)
- **Limit carried forward:** this is the **most recent SAPWG record retrieved**. The 2026
  Summer National Meeting had not been reported on at the access date, and the exposed
  **revised SSAP No. 7** (the intended replacement for INT 23-01) was **not located or read**.

#### REG-R89. NAIC Annual Statement Instructions — Life, Accident & Health/Fraternal, 2025 reporting year
- **Publisher:** NAIC ("Adopted by the NAIC as of June 2025"; free download from the NAIC
  Resource Center)
- **URL:** https://content.naic.org/sites/default/files/publication-asi-lua-25.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; 1,008 pages; Analysis of Operations pp. 84–96,
  Exhibits 5 / 5A / 6 / 7 pp. 143–157, Exhibit of Life Insurance p. 383, IMR pp. 390–404,
  AVR pp. 405–428 read)
- **Numbers deliberately not transcribed:** the **AVR factor tables** (basic contribution,
  reserve objective, maximum reserve, by NAIC designation and mortgage category) and the
  **IMR grouped-amortisation factor tables**. Neither document in this directory states a
  value for either.
- **Reporting-year caution:** this is the **2025** reporting year. Every page and line
  reference (Page 3 Line 9.4 IMR, Page 3 Line 24.01 AVR, Page 4 Line 41, asset page lines
  15/25, surplus lines 19/34) should be re-verified against the 2026 blank before being
  hard-coded.

#### REG-R90. NAIC Annual Statement Blank — Life, Accident & Health/Fraternal, 2025
- **Publisher:** NAIC (free download)
- **URL:** https://content.naic.org/sites/default/files/publication-asb-life.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; 211 pages; Liabilities page, Summary of
  Operations p. 13, Cash Flow p. 14, Analysis of Operations by LOB pp. 15–20, Analysis of
  Increase in Reserves pp. 21–24, Exhibits 5–7 pp. 29–32, Exhibit of Life Insurance
  pp. 52–53, IMR form p. 55, AVR forms pp. 56–63 read)
- **Cross-stream discrepancy, recorded rather than resolved:** the statutory-reserves stream
  attempted the **same URL** and recorded it as **not retrieved** (unreadable compressed
  streams, not re-attempted with local extraction), which is why that stream describes the
  actuarial opinion page, Exhibits 5/6/7/8, Schedule S and the VM-20 Reserves Supplement only
  through documents that reference them (R100, R108, R103). The statutory-accounting stream
  did retrieve it with local extraction. **R90 is fetched**; the reserves stream's derived
  statements about blank layout remain second-hand.

#### REG-R92. SSAP No. 61 — Life, Deposit-Type and Accident and Health Reinsurance (*As of March 2026*; historically 61R)
- **Publisher:** NAIC (in R73, statement pages 61-1 to 61-29 plus glossary)
- **URL:** https://content.naic.org/sites/default/files/publication-app-manual.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; ¶¶1–20, 36–38, 54–59 read; full section index read)
- **Limit carried forward:** **Appendix A-791** (Life and Health Reinsurance Agreements — the
  prohibited-conditions list that ¶¶17–19 turn on) was **not read**, only cited through this
  entry. It is in R73 Appendix A.

#### REG-R96. SSAP No. 86 — Derivatives (*As of March 2026*)
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
- **[unverified] carried forward:** the paragraph numbers cited (¶¶15–20, including the ¶17
  IMR election) are from the **2010 standalone print** and were **not cross-checked** against
  the March 2026 manual. Exhibits A, B and C were not read.

#### REG-R97. SSAP No. 101 — Income Taxes (*As of March 2026*)
- **Publisher:** NAIC (in R73, statement pages 101-1 onward, with Exhibit A Q&A)
- **URL:** https://content.naic.org/sites/default/files/publication-app-manual.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; status block, ¶¶1–2 and the full admissibility
  section ¶¶11–12 including all three Realization Threshold Limitation Tables read)

#### REG-R100. VM-30: Actuarial Opinion and Memorandum Requirements (Valuation Manual, Jan. 1, 2026 Edition)
- **Publisher:** NAIC
- **URL:** https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf
  (pages 30-1 to 30-15 of the 457-page PDF; same document as R3)
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; **Sections 1, 2 and 3 read in full**, including the
  prescribed opinion wording and the Regulatory Asset Adequacy Issues Summary contents;
  copyright line "© 2025 National Association of Insurance Commissioners")

#### REG-R103. Actuarial Guideline LV — Application of the Valuation Manual for Testing the Adequacy of Reserves Related to Certain Life Reinsurance Treaties (AG 55)
- **Publisher:** NAIC (this print: "Adopted by Life Insurance and Annuities (A) Committee –
  July 14, 2025 / Adopted by Life Actuarial (A) Task Force – June 5, 2025"; © 2025; 14 pages)
- **URL:** https://content.naic.org/sites/default/files/committees-pending-action-aglv.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; **entire guideline read, Sections 1–9 and Appendix
  1**). A guessed URL `.../inline-files/AG%2055.pdf` returned HTTP 404 and is not cited.
- **[unverified] carried forward:** adoption by the NAIC **Executive (EX) Committee and
  Plenary on August 13, 2025** — consistently reported by law firms and consultants, but no
  NAIC document stating that date was retrieved. The **effective** date (reserves reported in
  the December 31, 2025 annual statement) **is** printed in the guideline and is verified.

#### REG-R105. Actuarial Guideline LIII — Application of the Valuation Manual for Testing the Adequacy of Life Insurer Reserves (AG 53)
- **Publisher:** NAIC (print paginated "AG53-1" to "AG53-8" and headed "Appendix C", i.e. the
  AP&P Manual Appendix C text)
- **URL:** https://content.naic.org/sites/default/files/inline-files/AG%2053.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; **entire guideline read, Sections 1–6 and Appendix I**)

#### REG-R108. VM-31: PBR Actuarial Report Requirements for Business Subject to a Principle-Based Valuation (Valuation Manual, Jan. 1, 2026 Edition)
- **Publisher:** NAIC
- **URL:** https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf
  (pages 31-1 to 31-46; same document as R3)
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; Sections 1, 2, 3.A, 3.B, 3.C and 3.D.1–3.D.3 read;
  the full table of contents and section headers of 3.D–3.F reviewed)

#### REG-R109. VM-G: Appendix G — Corporate Governance Guidance for Principle-Based Reserves (Valuation Manual, Jan. 1, 2026 Edition)
- **Publisher:** NAIC
- **URL:** https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf
  (pages G-1 to G-6; same document as R3)
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; **Sections 1–4 read in full**)

#### REG-R125. Risk-Based Capital (RBC) for Insurers Model Act (Model #312)
- **Publisher:** National Association of Insurance Commissioners
- **URL:** https://content.naic.org/sites/default/files/model-law-312.pdf
- **Accessed:** 2026-08-04 · **Fetched:** yes (local text extraction; 14-page PDF; print
  header "NAIC Model Laws, Regulations, Guidelines and Other Resources—January 2012")

#### REG-R128. NAIC *Risk-Based Capital Forecasting and Instructions — 2024, Life / Fraternal*
- **Publisher:** NAIC (© 2019–2024 NAIC; instruction pages dated 10/14/2024). **Paid NAIC
  publication**; the copy read was posted publicly by the **Indiana Department of Insurance**.
- **URL:** https://www.in.gov/idoi/files/RBCL24-INpdf.pdf
- **Accessed:** 2026-08-04 · **Fetched:** yes (local text extraction; 225 pages; overview,
  LR002, LR025, LR025-A, LR027, LR029, LR030, LR031, LR033, LR034, LR035, LR049, Appendix 1,
  Appendix 1a and the corresponding blank pages read)
- **Paid-publication limit, stated plainly:** this document is *sold* by the NAIC, distributed
  annually around Nov. 1 from `content.naic.org/publications`, and marked "Not for
  Distribution" on every page (R139). Anyone rebuilding this work should **buy the current
  edition** rather than rely on a state posting. The **RBC forecasting spreadsheet** was never
  obtained and is not cited.

#### REG-R129. NAIC *Risk-Based Capital Forecasting and Instructions — 2023, Life / Fraternal*
- **Publisher:** NAIC (paid publication; copy posted by the Indiana Department of Insurance)
- **URL:** https://www.in.gov/idoi/files/indrbclf23.pdf
- **Accessed:** 2026-08-04 · **Fetched:** yes (local text extraction; 225 pages; used for
  targeted comparison only)
- **Fetch failure recorded:** the **2025 edition** at
  `https://www.in.gov/idoi/files/RBCL25-INpdf.pdf` returned a truncated PDF stream and could
  **not** be parsed. **No year-end 2025 factor is asserted anywhere in this directory.**

#### REG-R138. American Academy of Actuaries, *C-3 Alignment, Part III* (presentation to the NAIC Life RBC (E) Working Group, September 11, 2025)
- **Publisher:** American Academy of Actuaries
- **URL:** https://actuary.org/wp-content/uploads/2025/09/Life-Presentation-C3AlignmentUpdate.pdf
- **Accessed:** 2026-08-04 · **Fetched:** yes (local text extraction; 65 slides, including
  appended Part II from May 1, 2025)
- **Status and [unverified] carried forward:** a **framework presentation**, not adopted law.
  The field-test specifications document itself was **not retrieved** (only the working group
  page's note of a **July 30, 2026** re-exposure, R141); the reported **December 31, 2025**
  field-test valuation date and **2027** adoption target come from search summaries and are
  **[unverified]**.

#### REG-R139. NAIC *Life and Fraternal Risk-Based Capital Newsletter*, Volume 31 (September 2025)
- **Publisher:** NAIC
- **URL:** https://content.naic.org/sites/default/files/inline-files/2025_RBC%20Newsletter_Life%20and%20Fraternal.pdf
- **Accessed:** 2026-08-04 · **Fetched:** yes (local text extraction; 3 pages)

#### REG-R142. NAIC Capital Adequacy (E) Task Force — RBC Proposal Form, Agenda Item 2025-01-L (C-2 Mortality Risk / LR025 annual statement sources)
- **Publisher:** NAIC (proposal dated 02/21/2024, submitted on behalf of the Life RBC (E)
  Working Group, Philip Barlow chair)
- **URL:** https://content.naic.org/sites/default/files/inline-files/2025-01-L%20C-2%20Mortality%20Risk%20(1).pdf
- **Accessed:** 2026-08-04 · **Fetched:** yes (local text extraction; 3 pages)

**Not restated here, and deliberately so.** No **AVR factor**, **IMR grouped-amortisation
factor** or untranscribed **RBC factor** value appears anywhere in this directory: the
research did not transcribe them [REG-R89][REG-R128]. The **AP&P Manual licence** is personal
and non-commercial and prohibits integration "into any software or other publication" without
NAIC permission, and R89, R90 and R128 carry the same restriction, so SSAP and instruction
mechanics are **paraphrased with a paragraph cite, never pasted** — the one exception being
the C-3 Phase II Macro Tax Adjustment formula, quoted verbatim precisely because its printed
parentheses are unbalanced and the bracketing must not be silently "fixed" [REG-R128].

---

## Provenance note

Extraction details live in `us/_research/variable-annuity.md`: that file records which fact
came from which source, its [unverified] flags, and its "Gaps and caveats" section — in
particular that **no closed-form MVA factor** was found in any of the four prospectuses
read; that **guaranteed annuity purchase rate tables** were not obtained; that the SOA/LIMRA
behavior study detail is **paywalled**, leaving the VM-21 §6.C prescribed tables [R1] and
the AAA sample tables [R5] as the only public numeric behavior anchors; that **rate sheets
are volatile by design**; that fund expense ranges carry lagging as-of dates; and that
**GMAB mechanics, RILA buffer/floor structures and New York Regulation 213** are outside
its scope.

`us/_research/regulatory-actuarial-annuities.md` plays the same role for the R35–R72 half of
the [REG-R#] space, including its own verified corrections carried into these documents:
Model **#245** (not #250) is the Annuity Disclosure Model Regulation; the Model #805 indexed
nonforfeiture rate floor is **15 basis points**, not 1%; VM-22 in the 2026 edition is
entirely the PBR framework with income-annuity valuation rates in VM-V §1; AG 43 is **not**
simply superseded by VM-21; and **there is no ASOP for principle-based reserves for
annuities**. `us/_research/regulatory-actuarial.md` plays that role for R1–R34.

Standardizations marked **[std]** in `product-spec.md` and `technical-notes.md` are
introduced at drafting and are not attributable to any source.
