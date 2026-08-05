# Sources — Universal Life Insurance (current assumption)

Source ids, titles, publishers, URLs, access dates, and retrieval markers are carried
over verbatim from `us/_research/universal-life.md` (the citation ground truth for
[S#]/[R#] tags). Ids are never renumbered. Sources from the research file that are not
cited in `product-spec.md` or `technical-notes.md` are omitted (dropped here: R9).
No new sources were fetched at drafting; nothing is marked "added at drafting".

Access date for all citations: 2026-08-03 — except the [REG-R#] entries added for the
statutory accounting and capital section, which carry their own access dates (2026-08-03
or 2026-08-04) reproduced verbatim in that subsection.

---

## Primary product sources [S#]

### S1. Symetra Life Insurance Company — "Symetra CAUL Universal Life Insurance — Fact Sheet" (LIM-1286 10/23)
- Publisher: Symetra Life Insurance Company (document distributed via Financial
  Markets Inc., an authorized distributor; PDF is the insurer's own fact sheet)
- Doc type: consumer/product fact sheet (2 pages)
- URL fetched: https://www.fmiagent.com/wp-content/uploads/2024-05-22_Symetra_CAUL_Product_Highlights_LIM-1286_10-23.pdf
- Retrieved: YES (full PDF read)

### S2. Protective Life Insurance Company — "Protective Advantage Choice UL — Producer Guide" (PLAG.3459 (01.15))
- Publisher: Protective Life Insurance Company (distributed via MRW Financial,
  an authorized distributor; PDF is the insurer's producer guide)
- Doc type: producer/agent guide (8 pages)
- URL fetched: https://www.mrwfinancial.com/wp-content/uploads/Advantage-Choice-UL.pdf
- Retrieved: YES (full PDF read)

### S3. Pacific Life Insurance Company — Sample (specimen) policy "Versa-Flex PRO" — FLEXIBLE PREMIUM ADJUSTABLE LIFE INSURANCE, policy form P08VP1 (8/08)
- Publisher: Pacific Life Insurance Company (official sample policy on
  pacificlife.com)
- Doc type: specimen policy (full contract, 19+ pages incl. policy specifications
  for a Male 35 Standard Nonsmoker, $100,000 basic coverage + riders, policy date
  Nov 1, 2007)
- URL fetched: https://www.pacificlife.com/content/dam/paclife/lid/public/sample-policies/Sample_Policy_VF%20PRO%20II.pdf
- Retrieved: YES (full PDF read)
- Role in this library: implementation anchor for monthly-deduction mechanics,
  GPT corridor table, guaranteed maximum COI table, surrender charge amortization,
  loan/withdrawal/grace/reinstatement provisions.

### S4. Nationwide Life and Annuity Insurance Company — "Nationwide No-Lapse Guarantee UL II" producer presentation (FLM-1167AO.3 (06/22))
- Publisher: Nationwide (distributed via Krause Agency portal mirror)
- Doc type: producer marketing deck / product highlights (19 slides)
- URL fetched: https://portal.krauseagency.com/wp-content/uploads/2025/02/Nationwide-No-Lapse-Guarantee-Universal-Life.pdf
- Retrieved: YES (full PDF read)
- Role in this library: contrast case (guaranteed UL) for the current-assumption
  design; cited for market-role and out-of-scope rider/guarantee context.

### S5. Symetra — CAUL product page, symetra.com (FAILED FETCH)
- URL attempted: https://www.symetra.com/IndividualsFamilies/Products/LifeInsurance/PermanentLifeInsurance/SymetraCAULUniversalLife/
- Retrieved: NO — HTTP 403 Forbidden. Current declared crediting rates
  (symetra.com/liferates) therefore not captured. Nothing cited from this source
  except the fact of the failed fetch (used to document why current-scale
  assumptions are [std]).

---

## Regulatory and actuarial references [R#] (product research file numbering)

### R1. NAIC — Universal Life Insurance Model Regulation (Model 585), January 2001 reprint
- Publisher: National Association of Insurance Commissioners
- URL fetched: https://content.naic.org/sites/default/files/model-law-585.pdf
- Retrieved: YES (full PDF read, 14 pages)

### R2. IRC §7702 — Life insurance contract defined
- Publisher: Legal Information Institute, Cornell Law School (U.S. Code)
- URL fetched: https://www.law.cornell.edu/uscode/text/26/7702
- Retrieved: YES (fetched and summarized)
- Caveat carried over: the fetch was summarized by an automated reader; exact
  subsection text should be re-verified before quoting in a formal document.

### R3. IRC §7702A — Modified endowment contract defined
- Publisher: Legal Information Institute, Cornell Law School (U.S. Code)
- URL fetched: https://www.law.cornell.edu/uscode/text/26/7702A
- Retrieved: YES (fetched and summarized)

### R4. Society of Actuaries — 2017 Commissioners Standard Ordinary (CSO) Tables (resource page)
- Publisher: Society of Actuaries
- URL fetched: https://www.soa.org/resources/experience-studies/2015/2017-cso-tables/
- Retrieved: YES (page fetched; it is chiefly a download index)
- Caveat carried over: 2017 CSO adoption-timeline and usage claims (mandatory from
  2020-01-01; UL guaranteed COI cap; terminal age 121) come from search-result
  context, not a fetched primary document, and remain [unverified].

### R5. NAIC — Principle-Based Reserving (insurance topic page; gateway to Valuation Manual / VM-20)
- Publisher: National Association of Insurance Commissioners
- URL fetched: https://content.naic.org/insurance-topics/principle-based-reserving
- Retrieved: YES

### R6. American Academy of Actuaries — Life Illustrations Practice Note (September 2021 update)
- Publisher: American Academy of Actuaries, Life Illustrations Work Group
- URL fetched: https://actuary.org/wp-content/uploads/2021/09/Life_Illustrations_Practice_Note_Update.pdf
- Retrieved: YES (fetched and summarized)

### R7. SOA Research Institute & LIMRA — "2015-2021 Universal Life Premium Persistency and Lapse Rate Experience Study" (July 2024, revised December 2024) — Study Highlights
- Publisher: Society of Actuaries Research Institute and LIMRA
- URL fetched: https://www.soa.org/globalassets/assets/files/resources/experience-studies/2024/15-21-ulpp-ulls.pdf
- Retrieved: YES (full highlights PDF read)
- Note carried over: detailed tables are behind the paid Experience Studies Pro
  package (not retrieved).

### R8. Actuarial Standards Board — ASOP No. 2 (Revised Edition, Doc. No. 204): "Nonguaranteed Elements for Life Insurance and Annuity Products" (adopted September 2021)
- Publisher: Actuarial Standards Board
- URL fetched: https://www.actuarialstandardsboard.org/wp-content/uploads/2021/12/asop002_204-2.pdf
- Retrieved: YES (full PDF read)

### R10. IIPRC (Interstate Insurance Product Regulation Commission) — Standards for Individual Flexible Premium Adjustable Life Insurance Policies (5-year review revision, 2014)
- Publisher: Interstate Insurance Product Regulation Commission
  (insurancecompact.org)
- URL: https://www.insurancecompact.org/sites/default/files/2023-08/140815-iiprc-l-09-i-5-yr-rev.pdf
- Retrieved: PARTIAL — PDF binary was downloaded but its text was not read;
  NO facts are cited from it. Cited in this library only as a located reference
  for the uniform product standards under which multi-state UL forms (e.g., the
  "ICC14"-prefixed Symetra form in [S1]) are filed.

Dropped (in the research file but not cited in these documents): R9 (NAIC Valuation
Manual, located but not fetched in the product research; Valuation Manual facts are
cited instead from the fetched cross-product entry [REG-R3] below).

---

## Cross-product regulatory references [REG-R#]

These are cited with the [REG-R#] prefix to avoid collision with the product research
file's own R-numbering. Full annotated entries (titles, publishers, URLs, retrieval
markers, access date 2026-08-03) live in `us/_research/regulatory-actuarial.md`;
the shared reference library is
`us/references/regulatory-and-actuarial-references.md` (same R-numbering, which now runs
**R1–R150**, with **R114–R124** and **R143–R149** permanently unused **by design**;
R1–R72 are the frozen pre-existing life and annuity entries, of which R35–R72 are
annuity-specific and only R41 is cited here, and R73–R142 are the statutory accounting
and capital entries, whose per-entry bibliography is `us/regulatory/sources.md`).
Entries cited by the two documents in this directory:

| Tag | Short title | Retrieval status (per that file) |
|---|---|---|
| REG-R3 | NAIC Valuation Manual, Jan. 1, 2026 edition (VM-01/02/20/31, VM-M/G/C/V) | fetched (cover, adoption history, full TOC read) |
| REG-R5 | NAIC Universal Life Insurance Model Regulation (Model #585) | fetched (same document as [R1] above) |
| REG-R6 | NAIC Valuation of Life Insurance Policies Model Regulation (Model #830, "XXX") | fetched |
| REG-R7 | Actuarial Guideline XXXVIII (AG 38), 2012 text incl. 8D/8E | fetched |
| REG-R13 | 26 U.S.C. §7702 (same statute as [R2] above) | fetched |
| REG-R14 | 26 U.S.C. §7702A (same statute as [R3] above) | fetched |
| REG-R16 | 26 U.S.C. §807 — tax reserves | fetched |
| REG-R17 | 2017 CSO tables (SOA landing page; same page as [R4] above) | fetched (landing page) |
| REG-R18 | 2015 Valuation Basic Table (VBT) — SOA landing page | fetched (landing page) |
| REG-R19 | ILEC 2012–2019 Individual Life Mortality Experience Report (landing page) | fetched (landing page) |
| REG-R20 | LIMRA/SOA U.S. Individual Life Persistency Update (2009–2013) | fetched (landing page) |
| REG-R21 | LIMRA/SOA 2015–2021 UL Premium Persistency and Lapse/Surrender Study (landing page; highlights PDF fetched as [R7] above) | fetched (landing page) |
| REG-R23 | AAA — Life PBR Under VM-20 Practice Note (April 2020) | fetched |
| REG-R26 | ASOP No. 2 — Nonguaranteed Elements (same standard as [R8] above) | fetched |
| REG-R27 | ASOP No. 7 — Life or Health Cash Flow Analysis (rev. Dec 2025) | fetched |
| REG-R31 | ASOP No. 52 — Principle-Based Reserves for Life Products under the NAIC Valuation Manual | fetched |
| REG-R32 | ASOP No. 56 — Modeling | fetched |

### Entries added for the "Statutory accounting and capital" section

Newly cited by that section of `technical-notes.md` and by the corresponding paragraph
of `product-spec.md`. Id, title, publisher, URL, access date and fetched marker are
carried **verbatim** from `us/regulatory/sources.md`, which is the per-entry
bibliography for the shared R73–R142 block and reproduces the frozen R1–R72 metadata.
**Ids are never renumbered**; nothing below was fetched at drafting.

### REG-R1. Standard Valuation Law (Model #820)
- **Publisher:** National Association of Insurance Commissioners (NAIC)
- **URL:** https://content.naic.org/sites/default/files/model-law-820.pdf
- **Accessed:** 2026-08-03 · **Fetched:** yes (27-page PDF retrieved and read; re-read for
  the reserves stream at §§3, 4b, 5, 5a, 6, 7, 11, 12)

### REG-R11. Actuarial Guideline XLVIII — Actuarial Opinion and Memorandum Requirements for the Reinsurance of Policies Required to be Valued under Sections 6 and 7 of the NAIC Valuation of Life Insurance Policies Model Regulation (AG 48)
- **Publisher:** NAIC (LATF adoption 12/1/2016 revision print)
- **URL:** https://content.naic.org/sites/default/files/inline-files/committees_ex_pbr_implementation_tf_related_actuarial_guideline_ag48.pdf
- **Accessed:** 2026-08-03 · **Fetched:** yes (12-page PDF retrieved and read)

### REG-R12. Term and Universal Life Insurance Reserve Financing Model Regulation (Model #787)
- **Publisher:** NAIC
- **URL:** https://content.naic.org/sites/default/files/model-law-787.pdf
- **Accessed:** 2026-08-03 · **Fetched:** yes (10-page PDF retrieved and read; print: Model
  Regulation Service, 1st Quarter 2017)

### REG-R29. ASOP No. 22 — Statements of Actuarial Opinion Based on Asset Adequacy Analysis for Life Insurance, Annuity, or Health Insurance Reserves and Other Liabilities
- **Publisher:** Actuarial Standards Board
- **URL:** https://www.actuarialstandardsboard.org/asops/asop-no-22-statements-of-actuarial-opinion-based-on-asset-adequacy-analysis-for-life-insurance-annuity-or-health-insurance-reserves-and-other-liabilities/
- **Accessed:** 2026-08-03 · **Fetched:** yes (adopted Sept. 2021; effective June 1, 2022).
  **Re-read in full for the reserves stream** on 2026-08-04 from Doc. No. 203,
  https://www.actuarialstandardsboard.org/wp-content/uploads/2021/11/asop022_203.pdf (26 pp.).

### REG-R41. VM-C: Appendix C — Actuarial Guidelines (index of guidelines incorporated into the Valuation Manual)
- **Publisher:** NAIC
- **URL:** https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf
  (pages C-1 to C-2; same document as R3)
- **Accessed:** 2026-08-04 · **Fetched:** yes (local text extraction; the complete two-page
  index read; the **life/CRVM half** of the index was extracted for the reserves stream)

### REG-R75. SSAP No. 71 — Policy Acquisition Costs and Commissions (*As of March 2026*)
- **Publisher:** NAIC (in R73, statement pages 71-1 to 71-3)
- **URL:** https://content.naic.org/sites/default/files/publication-app-manual.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; ¶¶1–7 read in full)

### REG-R76. Statutory Issue Paper No. 71 — Policy Acquisition Costs and Commissions
- **Publisher:** NAIC (finalized March 16, 1998; AP&P Appendix E)
- **URL:** https://content.naic.org/sites/default/files/inline-files/071_H.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; 6 pages, read in full)

### REG-R78. SSAP No. 50 — Classifications of Insurance or Managed Care Contracts (*As of March 2026*)
- **Publisher:** NAIC (in R73, statement pages 50-1 onward)
- **URL:** https://content.naic.org/sites/default/files/publication-app-manual.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; ¶¶1–20 read)

### REG-R79. SSAP No. 51 — Life Contracts (*As of March 2026*; historically cited as SSAP No. 51R)
- **Publisher:** NAIC (in R73, statement pages 51-1 to 51-13)
- **URL:** https://content.naic.org/sites/default/files/publication-app-manual.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; status block, ¶¶1–16 read; section index read)
- **Limit carried forward:** ¶¶17 onward (mean/mid-terminal reserves, dividends, coupons,
  accelerated benefits, disclosures) were read through the **section index and the parallel
  Issue Paper No. 51 text (R81)**, not the SSAP paragraphs. Paragraph numbers differ between
  IP 51 and SSAP No. 51; a precise SSAP No. 51 paragraph cite needs R73 at pages 51-5 to 51-12.

### REG-R80. SSAP No. 52 — Deposit-Type Contracts (*As of March 2026*)
- **Publisher:** NAIC (in R73, statement pages 52-1 to 52-8)
- **URL:** https://content.naic.org/sites/default/files/publication-app-manual.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; ¶¶1–17 read in full)

### REG-R82. SSAP No. 54 — Individual and Group Accident and Health Contracts (*As of March 2026*; historically 54R)
- **Publisher:** NAIC (in R73, statement pages 54-1 onward)
- **URL:** https://content.naic.org/sites/default/files/publication-app-manual.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; status block, ¶¶1–2 and full section index read)
- **Limit carried forward:** the premium-deficiency and claim-reserve mechanics were **not**
  read in detail — adequate for this library's rider-only exposure, not for an A&H product.

### REG-R83. SSAP No. 56 — Separate Accounts (*As of March 2026*)
- **Publisher:** NAIC (in R73, statement pages 56-1 to 56-14)
- **URL:** https://content.naic.org/sites/default/files/publication-app-manual.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; ¶¶1–31 and the glossary read)

### REG-R85. SSAP No. 7 — Asset Valuation Reserve and Interest Maintenance Reserve (*As of March 2026*)
- **Publisher:** NAIC (in R73, statement pages 7-1 to 7-2)
- **URL:** https://content.naic.org/sites/default/files/publication-app-manual.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; ¶¶1–4 read in full — the statement is two pages)

### REG-R86. Statutory Issue Paper No. 7 — Asset Valuation Reserve and Interest Maintenance Reserve
- **Publisher:** NAIC (finalized March 16, 1998; AP&P Appendix E)
- **URL:** https://content.naic.org/sites/default/files/inline-files/007_G.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; 12 pages, read in full)
- **Vintage caution carried forward:** the AVR/IMR instruction text quoted in this issue
  paper is **1990s vintage**; the current factors, groupings and rules are at R89 and differ
  in detail (e.g. the grouped-method bands now begin with a separate "0 calendar years" band).

### REG-R87. INT 23-01 — Net Negative (Disallowed) Interest Maintenance Reserve (revised print, adopted August 11, 2025)
- **Publisher:** NAIC Statutory Accounting Principles (E) Working Group (AP&P Appendix B)
- **URL:** https://content.naic.org/sites/default/files/inline-files/22-19%20-%20INT%2023-01%20-%20Revised%20April%202025.pdf
  (original clean adoption print, August 13, 2023:
  https://content.naic.org/sites/default/files/inline-files/22-19a%20-%20INT%2023-01%20-%20IMR%20clean.pdf — also fetched)
- **Accessed:** 2026-08-04
- **Fetched:** yes, both (local text extraction; 8 pages each; the revised print carries
  visible tracked-change artefacts, which is how the extension is evidenced)

### REG-R89. NAIC Annual Statement Instructions — Life, Accident & Health/Fraternal, 2025 reporting year
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

### REG-R90. NAIC Annual Statement Blank — Life, Accident & Health/Fraternal, 2025
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

### REG-R92. SSAP No. 61 — Life, Deposit-Type and Accident and Health Reinsurance (*As of March 2026*; historically 61R)
- **Publisher:** NAIC (in R73, statement pages 61-1 to 61-29 plus glossary)
- **URL:** https://content.naic.org/sites/default/files/publication-app-manual.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; ¶¶1–20, 36–38, 54–59 read; full section index read)
- **Limit carried forward:** **Appendix A-791** (Life and Health Reinsurance Agreements — the
  prohibited-conditions list that ¶¶17–19 turn on) was **not read**, only cited through this
  entry. It is in R73 Appendix A.

### REG-R100. VM-30: Actuarial Opinion and Memorandum Requirements (Valuation Manual, Jan. 1, 2026 Edition)
- **Publisher:** NAIC
- **URL:** https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf
  (pages 30-1 to 30-15 of the 457-page PDF; same document as R3)
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; **Sections 1, 2 and 3 read in full**, including the
  prescribed opinion wording and the Regulatory Asset Adequacy Issues Summary contents;
  copyright line "© 2025 National Association of Insurance Commissioners")

### REG-R103. Actuarial Guideline LV — Application of the Valuation Manual for Testing the Adequacy of Reserves Related to Certain Life Reinsurance Treaties (AG 55)
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

### REG-R105. Actuarial Guideline LIII — Application of the Valuation Manual for Testing the Adequacy of Life Insurer Reserves (AG 53)
- **Publisher:** NAIC (print paginated "AG53-1" to "AG53-8" and headed "Appendix C", i.e. the
  AP&P Manual Appendix C text)
- **URL:** https://content.naic.org/sites/default/files/inline-files/AG%2053.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; **entire guideline read, Sections 1–6 and Appendix I**)

### REG-R108. VM-31: PBR Actuarial Report Requirements for Business Subject to a Principle-Based Valuation (Valuation Manual, Jan. 1, 2026 Edition)
- **Publisher:** NAIC
- **URL:** https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf
  (pages 31-1 to 31-46; same document as R3)
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; Sections 1, 2, 3.A, 3.B, 3.C and 3.D.1–3.D.3 read;
  the full table of contents and section headers of 3.D–3.F reviewed)

### REG-R109. VM-G: Appendix G — Corporate Governance Guidance for Principle-Based Reserves (Valuation Manual, Jan. 1, 2026 Edition)
- **Publisher:** NAIC
- **URL:** https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf
  (pages G-1 to G-6; same document as R3)
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; **Sections 1–4 read in full**)

### REG-R110. VM-A: Appendix A — Requirements (Valuation Manual, Jan. 1, 2026 Edition)
- **Publisher:** NAIC
- **URL:** https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf
  (pages A-1 to A-2; same document as R3)
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; the complete two-page index read)
- **Limit carried forward:** VM-A is an **index, not a text**. The requirements it indexes —
  above all **A-820** (minimum life and annuity reserve standards) and **A-830** (valuation of
  life insurance policies) — live in AP&P Appendix A and **were not retrieved**, because the
  reserves stream worked under R33's "paid publication" assumption. Formulaic CRVM detail in
  this directory therefore rests on the Standard Valuation Law itself (R1) and Model #830 (R6).

### REG-R125. Risk-Based Capital (RBC) for Insurers Model Act (Model #312)
- **Publisher:** National Association of Insurance Commissioners
- **URL:** https://content.naic.org/sites/default/files/model-law-312.pdf
- **Accessed:** 2026-08-04 · **Fetched:** yes (local text extraction; 14-page PDF; print
  header "NAIC Model Laws, Regulations, Guidelines and Other Resources—January 2012")

### REG-R128. NAIC *Risk-Based Capital Forecasting and Instructions — 2024, Life / Fraternal*
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

### REG-R129. NAIC *Risk-Based Capital Forecasting and Instructions — 2023, Life / Fraternal*
- **Publisher:** NAIC (paid publication; copy posted by the Indiana Department of Insurance)
- **URL:** https://www.in.gov/idoi/files/indrbclf23.pdf
- **Accessed:** 2026-08-04 · **Fetched:** yes (local text extraction; 225 pages; used for
  targeted comparison only)
- **Fetch failure recorded:** the **2025 edition** at
  `https://www.in.gov/idoi/files/RBCL25-INpdf.pdf` returned a truncated PDF stream and could
  **not** be parsed. **No year-end 2025 factor is asserted anywhere in this directory.**

### REG-R133. NAIC, *Life RBC—C-2 Mortality Risk: Instruction Supplement for Applying the Newly Adopted Life Insurance C-2 Mortality Instructions* (December 19, 2022)
- **Publisher:** NAIC
- **URL:** https://content.naic.org/sites/default/files/inline-files/lrbc-C-2-mortality-risk-instruction-supplement-dec2022.pdf
- **Accessed:** 2026-08-04 · **Fetched:** yes (local text extraction; 14 pages)
- **[unverified] carried forward:** the **first year** the current pricing-flexibility C-2
  structure and the LR025-A longevity page applied. Both are present in the 2023 and 2024
  editions with identical numbers (R129, R128); this supplement's December 19, 2022 date and
  "newly adopted" description are *consistent with* year-end 2023 but do not prove it.

### REG-R135. *Phase I Report of the American Academy of Actuaries' C-3 Subgroup of the Life Risk Based Capital Task Force to the NAIC's Risk Based Capital Work Group* (October 1999, Atlanta)
- **Publisher:** American Academy of Actuaries
- **URL:** https://www.actuary.org/wp-content/uploads/2025/05/c3_oct99.pdf
- **Accessed:** 2026-08-04 · **Fetched:** yes (local text extraction; 43 pages; executive
  summary and Appendix I scenario-testing methodology read)

### REG-R142. NAIC Capital Adequacy (E) Task Force — RBC Proposal Form, Agenda Item 2025-01-L (C-2 Mortality Risk / LR025 annual statement sources)
- **Publisher:** NAIC (proposal dated 02/21/2024, submitted on behalf of the Life RBC (E)
  Working Group, Philip Barlow chair)
- **URL:** https://content.naic.org/sites/default/files/inline-files/2025-01-L%20C-2%20Mortality%20Risk%20(1).pdf
- **Accessed:** 2026-08-04 · **Fetched:** yes (local text extraction; 3 pages)

### REG-R150. NAIC — Principle-Based Reserving (insurance topic page)
- **Publisher:** NAIC
- **URL:** https://content.naic.org/insurance-topics/principle-based-reserving
- **Accessed:** 2026-08-06 · **Fetched:** yes (page shows "Last Updated: 8/1/2025")
- **Note:** the shared-library entry for **this file's local [R5]** — the same document,
  now addressable from the cross-product bibliography. Cited for two verbatim statements:
  *"Effective Jan. 1, 2017, the Valuation Manual became operative"* and *"PBR which became
  an accreditation standard Jan. 1, 2020."* Do not confuse with **[REG-R5]**, which is the
  Universal Life Insurance Model Regulation (Model #585) — a different document that this
  file also cites.

---

## Provenance note

Extraction details live in `us/_research/universal-life.md`: that file records which
facts came from which source, including the [unverified] flags, the failed/partial
fetches (S5, R10), the mirror-hosting caveat for S1/S2/S4 (fetched from
authorized-distributor mirrors carrying the insurers' own form numbers), and the
vintage caveat that parameter levels are era-representative while mechanics are
stable. The cross-product bibliography `us/_research/regulatory-actuarial.md` plays
the same role for [REG-R#] tags. Standardizations marked **[std]** in
`product-spec.md` and `technical-notes.md` are introduced at drafting and are not
attributable to any source.
