# Sources — Variable Universal Life Insurance

Source ids, titles, publishers, URLs, access dates, and retrieval markers are
carried over verbatim from `us/_research/variable-ul.md` (sections "Primary
sources" and "Regulatory and actuarial references"); ids are never renumbered.
Access date for all citations: 2026-08-03, **except** the statutory accounting and
capital entries added to the cross-product section below, whose own access dates
(2026-08-04, or 2026-08-03 for frozen R1–R72 entries) are reproduced per entry.
Only sources actually cited in `product-spec.md` or `technical-notes.md` are listed
(unused S5/S6 dropped). No new sources were fetched at drafting — nothing is marked
"added at drafting".

## Primary product sources [S#]

### S1. Pruco Life Insurance Company (Prudential) — "VUL Protector (2015)" statutory prospectus (Form N-6 / 485BPOS)
- Publisher: Pruco Life Insurance Company (Arizona stock company, subsidiary of
  The Prudential Insurance Company of America); registrant is the Pruco Life
  Variable Universal Account (separate account, CIK 0000851693, 1940 Act file
  811-05826).
- Doc type: statutory prospectus (SEC Form N-6, post-effective amendment 485BPOS
  filed 2025-04-15, accession 0000851693-25-000091, prospectus dated May 1, 2025).
- URL fetched: https://www.sec.gov/Archives/edgar/data/851693/000085169325000091/plvulpregtofile.htm
- Retrieved: YES (full ~3.0 MB HTML downloaded and text-extracted).
- Used for: fee-table anchors (premium loads, surrender charge, COI, M&E, admin),
  Type A/B death benefits, fixed option 1% floor, loan mechanics, grace/default,
  age-121 provisions, riders, credits, transfer limits.

### S2. Equitable Financial Life Insurance Company — "VUL Optimizer (Series 166)" statutory prospectus (Form N-6 / 485BPOS)
- Publisher: Equitable Financial Life Insurance Company; registrant Separate
  Account FP (CIK 0000771726).
- Doc type: statutory prospectus (485BPOS filed 2025-04-24, accession
  0001193125-25-093072, prospectus dated May 1, 2025).
- URL fetched: https://www.sec.gov/Archives/edgar/data/771726/000119312525093072/d925311d485bpos.htm
- Retrieved: YES (full ~2.5 MB HTML downloaded and text-extracted).
- Used for: 6%/4% premium charge, 2017 CSO COI maxima, $10 monthly fee, per-$1,000
  charge, 10-year surrender charge, GPT corridor factors and CVAT description, NAAR
  definition, GIO floor, loan mechanics, reinstatement, riders.

### S3. The Lincoln National Life Insurance Company — "Lincoln LifeGoals" VUL statutory prospectus (Form N-6 / 485BPOS)
- Publisher: The Lincoln National Life Insurance Company; registrant Lincoln
  Life Flexible Premium Variable Life Account M (CIK 0001048607, 1940 Act
  811-08557, 1933 Act 333-259297).
- Doc type: statutory prospectus (485BPOS filed 2025-04-10, accession
  0001104659-25-033688, prospectus dated May 1, 2025).
- URL fetched: https://www.sec.gov/Archives/edgar/data/1048607/000110465925033688/tm253642d1_485bpos.htm
- Retrieved: YES (full ~1.7 MB HTML downloaded and text-extracted).
- Used for: the low-load/no-load variation, COI min/max, 0.6% M&E cap, loan-account
  collateral mechanics, DB-during-grace debt offset, Option 2→1 design.

### S4. Pacific Life Insurance Company — "Pacific Select VUL 2" statutory prospectus (Form N-6 / 485BPOS)
- Publisher: Pacific Life Insurance Company; registrant Pacific Select Exec
  Separate Account (CIK 0000832908, 1940 Act 811-05563, 1933 Act 333-231309).
- Doc type: statutory prospectus (485BPOS filed 2025-04-18, accession
  0001104659-25-036303, prospectus dated May 1, 2025).
- URL fetched: https://www.sec.gov/Archives/edgar/data/832908/000110465925036303/tm255241d1_485bpos.htm
- Retrieved: YES (full ~3.4 MB HTML downloaded and text-extracted).
- Used for: 6.50% max load, 2017 CSO COI maxima with the male-45 current/guaranteed
  anchor ($0.04/$0.22), $10 admin + coverage charges, 15-year surrender charge,
  Option C variation, 2% fixed floor, indexed fixed options, FDNLG shadow-fund
  rider (5.5%/10% notional loads), overloan protection, age-121 rule.

## Product-file regulatory and actuarial references [R#]
(numbering of `us/_research/variable-ul.md`)

### R1. SEC — Form N-6 (registration form for variable life insurance separate accounts)
- Publisher: U.S. Securities and Exchange Commission.
- URL fetched: https://www.sec.gov/files/formn-6.pdf (47-page reference copy,
  SEC 2567, 1/22 version)
- Retrieved: YES (PDF downloaded, full text extracted).

### R2. SEC — Release 33-10765: "Updated Disclosure Requirements and Summary Prospectus for Variable Annuity and Variable Life Insurance Contracts" (rule 498A)
- Publisher: U.S. Securities and Exchange Commission.
- URL fetched: https://www.sec.gov/newsroom/press-releases/2020-57 (press
  release; fetched via curl). Final rule text at
  https://www.sec.gov/files/rules/final/2020/33-10765.pdf and Federal Register
  2020-05526 (both blocked to the fetch tool; not retrieved).
- Retrieved: YES (press release page).

### R3. IRC §7702 — Definition of life insurance contract
- Publisher: Legal Information Institute (Cornell), U.S. Code.
- URL fetched: https://www.law.cornell.edu/uscode/text/26/7702
- Retrieved: YES.

### R4. IRC §7702A — Modified endowment contract (MEC)
- Publisher: Legal Information Institute (Cornell), U.S. Code.
- URL fetched: https://www.law.cornell.edu/uscode/text/26/7702A
- Retrieved: YES.

### R5. IRC §817(h) — Diversification requirements for variable contracts
- Publisher: Legal Information Institute (Cornell), U.S. Code.
- URL fetched: https://www.law.cornell.edu/uscode/text/26/817
- Retrieved: YES.

### R6. Treas. Reg. §1.817-5 — Diversification requirements
- Publisher: Legal Information Institute (Cornell), 26 CFR.
- URL fetched: https://www.law.cornell.edu/cfr/text/26/1.817-5
- Retrieved: YES.

### R7. NAIC — Valuation Manual, Jan. 1, 2025 edition (incl. VM-01, VM-20, VM-A/VM-C appendices)
- Publisher: National Association of Insurance Commissioners.
- URL fetched: https://content.naic.org/sites/default/files/pbr-data-valuation-manual-2025-edition.pdf
  (356-page PDF downloaded, text extracted).
- Retrieved: YES.

### R8. NAIC — Variable Life Insurance Model Regulation (Model #270)
- Publisher: National Association of Insurance Commissioners (January 1996
  printing with comments).
- URL fetched: https://content.naic.org/sites/default/files/model-law-270.pdf
  (66-page PDF downloaded, text extracted).
- Retrieved: YES.

### R9. ASB — ASOP No. 52, "Principle-Based Reserves for Life Products under the NAIC Valuation Manual"
- Publisher: Actuarial Standards Board.
- URL fetched: http://actuarialstandardsboard.org/wp-content/uploads/2017/10/asop052_189.pdf
  (39-page PDF downloaded, text extracted).
- Retrieved: YES.

### R10. American Academy of Actuaries — practice note "Life Principle-Based Reserves (PBR) Under VM-20" (April 2020)
- Publisher: American Academy of Actuaries, Life Valuation Committee work group.
- URL fetched: https://actuary.org/wp-content/uploads/2020/04/VM-20_PN_2020_Version_0.pdf
  (115-page PDF downloaded; title/front matter verified, body used as Q&A
  reference).
- Retrieved: YES.

### R11. ASB — ASOP No. 2, "Nonguaranteed Elements for Life Insurance and Annuity Products"
- Publisher: Actuarial Standards Board.
- URL fetched: https://www.actuarialstandardsboard.org/asops/asop-no-2-nonguaranteed-elements-for-life-insurance-and-annuity-products/
- Retrieved: YES (standard's landing page/summary).

### R12. Society of Actuaries — 2017 Commissioners Standard Ordinary (CSO) Tables
- Publisher: Society of Actuaries.
- URL fetched: https://www.soa.org/resources/experience-studies/2015/2017-cso-tables/
- Retrieved: YES.

### R13. FINRA — "Insurance" investor product page (variable life / VUL)
- Publisher: FINRA.
- URL fetched: https://www.finra.org/investors/investing/investment-products/insurance
- Retrieved: YES.

## Cross-product regulatory references [REG-R#]

These use the R# numbering of the cross-product bibliography
`us/_research/regulatory-actuarial.md` (accessed 2026-08-03), cited here as
[REG-R#] to avoid collision with the product-file R# ids above. Full annotations
live in that file; the shared reference library is
`us/references/regulatory-and-actuarial-references.md` (same R-numbering, which now runs
**R1–R157**, with **R114–R124** and **R143–R149** permanently unused **by design** —
the gaps are block-assignment spares, not losses, and must not be back-filled).
R1–R72 are the pre-existing life and annuity entries; R73–R142 are the statutory
accounting and capital entries, whose provenance is `us/_research/statutory-accounting.md`
(R73–R99), `us/_research/statutory-reserves.md` (R100–R113) and
`us/_research/risk-based-capital.md` (R125–R142), with the per-entry bibliography at
`us/regulatory/sources.md`. **Ids are never renumbered.** Entries cited in the two
documents:

- REG-R1. Standard Valuation Law (Model #820) — NAIC.
  https://content.naic.org/sites/default/files/model-law-820.pdf — Fetched: yes.
- REG-R3. Valuation Manual, Jan. 1, 2026 Edition (VM-01, VM-02, VM-20, VM-31,
  VM-M, VM-G, VM-C, VM-V, …) — NAIC.
  https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf
  — Fetched: yes.
- REG-R4. Life Insurance Illustrations Model Regulation (Model #582) — NAIC.
  https://content.naic.org/sites/default/files/model-law-582.pdf — Fetched: yes.
- REG-R5. Universal Life Insurance Model Regulation (Model #585) — NAIC.
  https://content.naic.org/sites/default/files/model-law-585.pdf — Fetched: yes.
- REG-R16. 26 U.S.C. § 807 — Rules for certain reserves (tax reserves) — Legal
  Information Institute, Cornell Law School.
  https://www.law.cornell.edu/uscode/text/26/807 — Fetched: yes.
- REG-R18. 2015 Valuation Basic Table (VBT) — Report and Tables — Society of
  Actuaries.
  https://www.soa.org/resources/experience-studies/2015/2015-valuation-basic-tables/
  — Fetched: yes (landing page).
- REG-R19. 2019 Individual Life Insurance Mortality Experience Report (ILEC,
  observation years 2012–2019) — SOA Research Institute, ILEC.
  https://www.soa.org/resources/research-reports/2024/ilec-mort-2012-19 —
  Fetched: yes (landing page).
- REG-R20. U.S. Individual Life Insurance Persistency Update (LIMRA/SOA,
  observation years 2009–2013) — LIMRA and Society of Actuaries.
  https://www.soa.org/resources/research-reports/2019/2009-13-us-ind-life-persistency-update/
  — Fetched: yes (landing page).
- REG-R21. 2015–2021 Universal Life Premium Persistency and Lapse/Surrender
  Experience Study — LIMRA and SOA Research Institute.
  https://www.soa.org/resources/experience-studies/2024/15-21-ulpp-ulls/ —
  Fetched: yes (landing page).
- REG-R27. ASOP No. 7 — Life or Health Cash Flow Analysis (revision adopted
  December 2025; effective June 1, 2026) — Actuarial Standards Board.
  https://www.actuarialstandardsboard.org/asops/life-or-health-cash-flow-analysis/
  — Fetched: yes.
- REG-R32. ASOP No. 56 — Modeling — Actuarial Standards Board.
  https://www.actuarialstandardsboard.org/asops/modeling-3/ — Fetched: yes.
- REG-R34. FASB ASU No. 2018-12 — Financial Services—Insurance (Topic 944):
  Targeted Improvements to the Accounting for Long-Duration Contracts (LDTI) —
  FASB. https://www.fasb.org (fasb.org blocked automated fetch; no working deep
  link cited) — Fetched: NO (title, scope, and effective dates corroborated across
  secondary sources); cited only with an explicit not-fetched flag.

### Statutory accounting and capital entries

Cited by the "Statutory accounting and capital" section of `technical-notes.md` and
the corresponding paragraph of `product-spec.md`. Id, title, publisher, URL, access
date and fetched marker are carried **verbatim** from `us/regulatory/sources.md`;
nothing is renumbered and no [unverified] flag or retrieval limit is upgraded.
Several SSAP entries locate themselves "in R73", the NAIC *Accounting Practices and
Procedures Manual, As of March 2026*, whose own entry is in `us/regulatory/sources.md`;
it is not repeated here because no document in this directory cites it directly.

- REG-R29. ASOP No. 22 — Statements of Actuarial Opinion Based on Asset Adequacy
  Analysis for Life Insurance, Annuity, or Health Insurance Reserves and Other
  Liabilities — Actuarial Standards Board.
  https://www.actuarialstandardsboard.org/asops/asop-no-22-statements-of-actuarial-opinion-based-on-asset-adequacy-analysis-for-life-insurance-annuity-or-health-insurance-reserves-and-other-liabilities/
  — Accessed: 2026-08-03 · Fetched: yes (adopted Sept. 2021; effective June 1, 2022).
  **Re-read in full for the reserves stream** on 2026-08-04 from Doc. No. 203,
  https://www.actuarialstandardsboard.org/wp-content/uploads/2021/11/asop022_203.pdf (26 pp.).
- REG-R75. SSAP No. 71 — Policy Acquisition Costs and Commissions (*As of March
  2026*) — NAIC (in R73, statement pages 71-1 to 71-3).
  https://content.naic.org/sites/default/files/publication-app-manual.pdf —
  Accessed: 2026-08-04 · Fetched: yes (local text extraction; ¶¶1–7 read in full).
- REG-R78. SSAP No. 50 — Classifications of Insurance or Managed Care Contracts
  (*As of March 2026*) — NAIC (in R73, statement pages 50-1 onward).
  https://content.naic.org/sites/default/files/publication-app-manual.pdf —
  Accessed: 2026-08-04 · Fetched: yes (local text extraction; ¶¶1–20 read).
- REG-R79. SSAP No. 51 — Life Contracts (*As of March 2026*; historically cited as
  SSAP No. 51R) — NAIC (in R73, statement pages 51-1 to 51-13).
  https://content.naic.org/sites/default/files/publication-app-manual.pdf —
  Accessed: 2026-08-04 · Fetched: yes (local text extraction; status block, ¶¶1–16
  read; section index read). **Limit carried forward:** ¶¶17 onward (mean/mid-terminal
  reserves, dividends, coupons, accelerated benefits, disclosures) were read through
  the **section index and the parallel Issue Paper No. 51 text (R81)**, not the SSAP
  paragraphs; a precise SSAP No. 51 paragraph cite needs R73 at pages 51-5 to 51-12.
- REG-R80. SSAP No. 52 — Deposit-Type Contracts (*As of March 2026*) — NAIC (in R73,
  statement pages 52-1 to 52-8).
  https://content.naic.org/sites/default/files/publication-app-manual.pdf —
  Accessed: 2026-08-04 · Fetched: yes (local text extraction; ¶¶1–17 read in full).
- REG-R83. SSAP No. 56 — Separate Accounts (*As of March 2026*) — NAIC (in R73,
  statement pages 56-1 to 56-14).
  https://content.naic.org/sites/default/files/publication-app-manual.pdf —
  Accessed: 2026-08-04 · Fetched: yes (local text extraction; ¶¶1–31 and the glossary
  read).
- REG-R85. SSAP No. 7 — Asset Valuation Reserve and Interest Maintenance Reserve
  (*As of March 2026*) — NAIC (in R73, statement pages 7-1 to 7-2).
  https://content.naic.org/sites/default/files/publication-app-manual.pdf —
  Accessed: 2026-08-04 · Fetched: yes (local text extraction; ¶¶1–4 read in full — the
  statement is two pages).
- REG-R87. INT 23-01 — Net Negative (Disallowed) Interest Maintenance Reserve
  (revised print, adopted August 11, 2025) — NAIC Statutory Accounting Principles (E)
  Working Group (AP&P Appendix B).
  https://content.naic.org/sites/default/files/inline-files/22-19%20-%20INT%2023-01%20-%20Revised%20April%202025.pdf
  (original clean adoption print, August 13, 2023:
  https://content.naic.org/sites/default/files/inline-files/22-19a%20-%20INT%2023-01%20-%20IMR%20clean.pdf
  — also fetched) — Accessed: 2026-08-04 · Fetched: yes, both (local text extraction;
  8 pages each; the revised print carries visible tracked-change artefacts, which is how
  the extension is evidenced).
- REG-R89. NAIC Annual Statement Instructions — Life, Accident & Health/Fraternal,
  2025 reporting year — NAIC ("Adopted by the NAIC as of June 2025"; free download
  from the NAIC Resource Center).
  https://content.naic.org/sites/default/files/publication-asi-lua-25.pdf —
  Accessed: 2026-08-04 · Fetched: yes (local text extraction; 1,008 pages; Analysis of
  Operations pp. 84–96, Exhibits 5 / 5A / 6 / 7 pp. 143–157, Exhibit of Life Insurance
  p. 383, IMR pp. 390–404, AVR pp. 405–428 read). **Numbers deliberately not
  transcribed:** the **AVR factor tables** (basic contribution, reserve objective,
  maximum reserve, by NAIC designation and mortgage category) and the **IMR
  grouped-amortisation factor tables** — no value for either is stated anywhere in this
  library. **Reporting-year caution:** this is the **2025** reporting year; every page
  and line reference should be re-verified against the 2026 blank before being
  hard-coded.
- REG-R90. NAIC Annual Statement Blank — Life, Accident & Health/Fraternal, 2025 —
  NAIC (free download).
  https://content.naic.org/sites/default/files/publication-asb-life.pdf —
  Accessed: 2026-08-04 · Fetched: yes (local text extraction; 211 pages; Liabilities
  page, Summary of Operations p. 13, Cash Flow p. 14, Analysis of Operations by LOB
  pp. 15–20, Analysis of Increase in Reserves pp. 21–24, Exhibits 5–7 pp. 29–32,
  Exhibit of Life Insurance pp. 52–53, IMR form p. 55, AVR forms pp. 56–63 read).
- REG-R92. SSAP No. 61 — Life, Deposit-Type and Accident and Health Reinsurance
  (*As of March 2026*; historically 61R) — NAIC (in R73, statement pages 61-1 to 61-29
  plus glossary).
  https://content.naic.org/sites/default/files/publication-app-manual.pdf —
  Accessed: 2026-08-04 · Fetched: yes (local text extraction; ¶¶1–20, 36–38, 54–59
  read; full section index read). **Limit carried forward:** **Appendix A-791** was
  **not read**, only cited through this entry.
- REG-R100. VM-30: Actuarial Opinion and Memorandum Requirements (Valuation Manual,
  Jan. 1, 2026 Edition) — NAIC.
  https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf
  (pages 30-1 to 30-15 of the 457-page PDF; same document as REG-R3) —
  Accessed: 2026-08-04 · Fetched: yes (local text extraction; **Sections 1, 2 and 3
  read in full**, including the prescribed opinion wording and the Regulatory Asset
  Adequacy Issues Summary contents).
- REG-R108. VM-31: PBR Actuarial Report Requirements for Business Subject to a
  Principle-Based Valuation (Valuation Manual, Jan. 1, 2026 Edition) — NAIC.
  https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf
  (pages 31-1 to 31-46; same document as REG-R3) — Accessed: 2026-08-04 · Fetched: yes
  (local text extraction; Sections 1, 2, 3.A, 3.B, 3.C and 3.D.1–3.D.3 read; the full
  table of contents and section headers of 3.D–3.F reviewed).
- REG-R109. VM-G: Appendix G — Corporate Governance Guidance for Principle-Based
  Reserves (Valuation Manual, Jan. 1, 2026 Edition) — NAIC.
  https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf
  (pages G-1 to G-6; same document as REG-R3) — Accessed: 2026-08-04 · Fetched: yes
  (local text extraction; **Sections 1–4 read in full**).
- REG-R110. VM-A: Appendix A — Requirements (Valuation Manual, Jan. 1, 2026 Edition)
  — NAIC.
  https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf
  (pages A-1 to A-2; same document as REG-R3) — Accessed: 2026-08-04 · Fetched: yes
  (local text extraction; the complete two-page index read). **Limit carried forward:**
  VM-A is an **index, not a text**; the requirements it indexes — above all **A-820**
  (minimum life and annuity reserve standards) and **A-830** (valuation of life
  insurance policies) — live in AP&P Appendix A and **were not retrieved**.
- REG-R128. NAIC *Risk-Based Capital Forecasting and Instructions — 2024,
  Life / Fraternal* — NAIC (© 2019–2024 NAIC; instruction pages dated 10/14/2024).
  **Paid NAIC publication**; the copy read was posted publicly by the **Indiana
  Department of Insurance**. https://www.in.gov/idoi/files/RBCL24-INpdf.pdf —
  Accessed: 2026-08-04 · Fetched: yes (local text extraction; 225 pages; overview,
  LR002, LR025, LR025-A, LR027, LR029, LR030, LR031, LR033, LR034, LR035, LR049,
  Appendix 1, Appendix 1a and the corresponding blank pages read). **Paid-publication
  limit, stated plainly:** this document is *sold* by the NAIC and marked "Not for
  Distribution" on every page; anyone rebuilding this work should **buy the current
  edition**. The **2025 edition could not be parsed**, so **no year-end 2025 factor is
  asserted**, and the RBC forecasting spreadsheet was never obtained.
- REG-R133. NAIC, *Life RBC—C-2 Mortality Risk: Instruction Supplement for Applying
  the Newly Adopted Life Insurance C-2 Mortality Instructions* (December 19, 2022) —
  NAIC.
  https://content.naic.org/sites/default/files/inline-files/lrbc-C-2-mortality-risk-instruction-supplement-dec2022.pdf
  — Accessed: 2026-08-04 · Fetched: yes (local text extraction; 14 pages).
  **[unverified] carried forward:** the **first year** the current pricing-flexibility
  C-2 structure and the LR025-A longevity page applied.
- REG-R135. *Phase I Report of the American Academy of Actuaries' C-3 Subgroup of the
  Life Risk Based Capital Task Force to the NAIC's Risk Based Capital Work Group*
  (October 1999, Atlanta) — American Academy of Actuaries.
  https://www.actuary.org/wp-content/uploads/2025/05/c3_oct99.pdf —
  Accessed: 2026-08-04 · Fetched: yes (local text extraction; 43 pages; executive
  summary and Appendix I scenario-testing methodology read).
- REG-R142. NAIC Capital Adequacy (E) Task Force — RBC Proposal Form, Agenda Item
  2025-01-L (C-2 Mortality Risk / LR025 annual statement sources) — NAIC (proposal
  dated 02/21/2024, submitted on behalf of the Life RBC (E) Working Group, Philip
  Barlow chair).
  https://content.naic.org/sites/default/files/inline-files/2025-01-L%20C-2%20Mortality%20Risk%20(1).pdf
  — Accessed: 2026-08-04 · Fetched: yes (local text extraction; 3 pages).

## Provenance note

Extraction details live in `us/_research/variable-ul.md`: that file records which
facts came from which source, the retrieval status of every document, and the gaps
and caveats (non-public COI scales and surrender-charge schedules, current declared
rates, unretrieved AG texts, and the [unverified] items) that the drafted documents
inherit. The cross-product regulatory annotations live in
`us/_research/regulatory-actuarial.md`.
