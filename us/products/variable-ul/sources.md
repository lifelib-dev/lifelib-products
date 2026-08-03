# Sources — Variable Universal Life Insurance

Source ids, titles, publishers, URLs, access dates, and retrieval markers are
carried over verbatim from `us/_research/variable-ul.md` (sections "Primary
sources" and "Regulatory and actuarial references"); ids are never renumbered.
Access date for all citations: 2026-08-03. Only sources actually cited in
`product-spec.md` or `technical-notes.md` are listed (unused S5/S6 dropped). No new
sources were fetched at drafting — nothing is marked "added at drafting".

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
`us/references/regulatory-and-actuarial-references.md` (same R-numbering). Entries
cited in the two documents:

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

## Provenance note

Extraction details live in `us/_research/variable-ul.md`: that file records which
facts came from which source, the retrieval status of every document, and the gaps
and caveats (non-public COI scales and surrender-charge schedules, current declared
rates, unretrieved AG texts, and the [unverified] items) that the drafted documents
inherit. The cross-product regulatory annotations live in
`us/_research/regulatory-actuarial.md`.
