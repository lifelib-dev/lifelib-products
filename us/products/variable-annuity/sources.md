# Sources — Variable Annuity with Living and Death Benefit Guarantees (United States)

Source ids, titles, publishers, URLs, access dates and fetched/not-fetched markers are
carried over **verbatim** from `us/_research/variable-annuity.md`, the citation ground
truth for the [S#]/[R#] tags used in `product-spec.md` and `technical-notes.md`. **Ids are
never renumbered.** Sources present in the research file but not cited in either document
are dropped; **none were dropped here — all of S1–S8 and R1–R13 are cited.** No new
sources were fetched at drafting, so nothing below is marked "added at drafting".

Access date for all citations: **2026-08-04**.

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
R1–R72**, curated at `us/references/regulatory-and-actuarial-references.md`:

- **R1–R34** — research provenance `us/_research/regulatory-actuarial.md` (the original
  life bibliography; several entries also bind annuity models, and that file's companion
  table records how each one applies).
- **R35–R72** — research provenance `us/_research/regulatory-actuarial-annuities.md` (the
  annuity continuation of the same space; it opens at R35 precisely because R1–R34 are
  frozen and must not be renumbered).

Entries cited by the two documents in this directory:

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
