# Sources — Fixed Indexed Annuity (FIA) with Guaranteed Lifetime Withdrawal Benefit (United States)

Source ids, titles, publishers, URLs, access dates and retrieval markers are carried over
verbatim from `us/_research/fixed-indexed-annuity.md` (the citation ground truth for [S#]/[R#]
tags). Ids are never renumbered. Sources in the research file that are not cited in
`product-spec.md` or `technical-notes.md` are omitted (dropped here: **S12**, the Athene Ascent
Pro producer landing page, and **S-f2**, the Athene Ascent Series spec-sheet mirror that returned
HTTP 403). **No new sources were fetched at drafting; nothing is marked "added at drafting."**
Two cross-product entries — **REG-R8** and **REG-R10** (AG 49 / AG 49-A) — were added to the
[REG-R#] table at review to carry the FIA-versus-IUL illustration-scope statement in
`product-spec.md`; both are pre-existing entries in `us/_research/regulatory-actuarial.md`, not new
retrievals. A further **30 cross-product entries in the R73–R142 block** were added when the
statutory accounting and capital material was written; they are carried verbatim from
`us/regulatory/sources.md` and are likewise **not** new retrievals — see the subsection under
"Cross-product regulatory references".

Access date for all citations: **2026-08-04**.

Note on the two R-numberings: the **[R#]** ids below are local to
`us/_research/fixed-indexed-annuity.md` and are unrelated to the **[REG-R#]** ids in the
cross-product section further down. For example [R3] here is NAIC Model #806, while [REG-R3] is
the NAIC Valuation Manual.

---

## Primary product sources [S#]

### S1. Athene Annuity and Life Company — "Athene Ascent<sup>SM</sup> Pro 10 — For income that lasts as long as your retirement." (consumer brochure, form 65178 (04/26/24))
- Publisher: Athene Annuity and Life Company, West Des Moines, IA (insurer's own consumer
  brochure; PDF mirrored by an authorized distributor site)
- Doc type: consumer product brochure (16 pages)
- URL fetched: https://annuityeducator.com/storage/59206/athene-ascent-pro-10.pdf
- Retrieved: YES (full PDF text-extracted locally)
- Role in this library: reference for the simple-rollup-plus-stacking income rider, the three
  income-phase definitions, the Extended Income Guarantee (post-depletion) rule, and the
  income-doubler trigger.

### S2. Athene Annuity and Life Company — "Athene Ascent<sup>SM</sup> Pro 10 Bonus — Product Guide, Rates effective July 1, 2022" (form 65220 (07/01/22))
- Publisher: Athene Annuity and Life Company (insurer product guide / rate-and-spec sheet; PDF
  mirrored by a distributor site)
- Doc type: producer product guide + declared rate sheet (6 pages)
- URL fetched: https://iamsascend.com/wp-content/uploads/2023/01/Ascent-Pro-Fact-Sheet.pdf
- Retrieved: YES (full PDF text-extracted locally)
- Caveat carried over: declared rates are as of 07/01/2022 and are non-guaranteed; Athene's
  current rate sheets could not be fetched (see S-f1).

### S3. Allianz Life Insurance Company of North America — "Allianz Benefit Control® — Fixed Index Annuity" (consumer brochure, ABC-001 (R-11/2025))
- Publisher: Allianz Life Insurance Company of North America (official allianzlife.com URL)
- Doc type: consumer product brochure (16 pages)
- URL fetched: https://www.allianzlife.com/-/media/Files/Global/documents/2020/02/24/20/53/ABC-001.pdf
- Retrieved: YES (full PDF text-extracted locally)
- Role in this library: source of the representative lifetime-withdrawal age-band table, and the
  reference case for the benefit-base-only bonus and pure-stacking benefit-base design.

### S4. Allianz Life Insurance Company of North America — "Allianz 222® Annuity — Guide to current rates as of 8/4/2026" (form M-7246 (R-8/2026))
- Publisher: Allianz Life Insurance Company of North America (official allianzlife.com URL)
- Doc type: declared-rate sheet (3 pages)
- URL fetched: https://www.allianzlife.com/what-we-offer/annuities/fixed-index-annuities/222/rates/-/media/Files/Allianz/PDFs/declared-rates/fixed-index-annuity/M-7246-Declared.pdf
- Retrieved: YES (full PDF text-extracted locally)
- Role in this library: the guaranteed minimum index parameters (minimum annual cap, minimum
  monthly cap, minimum participation rate, minimum fixed rate) that bound the non-guaranteed
  scale.

### S5. American Equity Investment Life Insurance Company — "IncomeShield 10 with Optional Lifetime Income Benefit Rider" (consumer brochure, 01SB1164-10 10.16.19)
- Publisher: American Equity Investment Life Insurance Company (insurer brochure; the official
  media.american-equity.com URL failed DNS from this environment, so a distributor mirror of the
  same form number was used — see S-f3)
- Doc type: consumer product brochure (12 pages)
- URL fetched: https://www.annuityresources.com/assets/brochures/americanequityincomeshield10.pdf
- Retrieved: YES (full PDF text-extracted locally)
- Role in this library: source of the representative premium bonus rate, bonus vesting vector and
  surrender charge schedule, and of the at-exercise step-up of the income base to contract value.
- Caveat carried over: 2019 brochure; current IAV rates, the rider fee percentage and its base,
  and the Minimum Guaranteed IAV Rate are undocumented.

### S6. Midland National Life Insurance Company — "IndexMax ADV® 5 Fixed index annuity — Annuity disclosure statement" (form 32908Y-1, 8-24)
- Publisher: Midland National Life Insurance Company (Sammons Financial) — official
  midlandnational.com document library URL
- Doc type: **signed annuity disclosure statement** (12-page form; the most contractually precise
  consumer-facing document short of the contract itself)
- URL fetched: https://www.midlandnational.com/documents/35453/9032621/32908Y+IndexMax+ADV+5+disclosure/e1927985-0db5-24cb-257c-61b46011487e
- Retrieved: YES (full PDF text-extracted locally)
- Role in this library: the "not a registered security" and dividend-exclusion statements, the
  Interest Credit Basis definition, the linear MVA form and collar, and the 87.5% minimum
  surrender value.

### S7. Midland National Life Insurance Company — "Midland National Capital Income® fixed index annuity — Understanding the market value adjustment" (form 32340Y-CA, REV 10-24, for use in California only)
- Publisher: Midland National Life Insurance Company — official midlandnational.com URL
- Doc type: contract-feature explanatory disclosure (2 pages)
- URL fetched: https://www.midlandnational.com/documents/35453/9032621/32340Y-04+-+Understanding+the+MVA+CA/e6de4768-02a1-cdef-4370-aa8c1896db2d
- Retrieved: YES (full PDF text-extracted locally)
- Role in this library: the California MVA collar, and the explicit statement that rider and
  strategy charges can exceed interest credited — i.e. that the 0% floor applies to the index
  credit and not to the account value.

### S8. Midland National Life Insurance Company — "MNL IncomeVantage® fixed index annuity — quick reference guide" (form 25665Y REV 1-20)
- Publisher: Midland National Life Insurance Company — official midlandnational.com URL
- Doc type: producer quick reference guide (1 page; "FOR FINANCIAL PROFESSIONAL ONLY")
- URL fetched: https://www.midlandnational.com/documents/35445/8312558/25665Y.pdf/dcf404b7-a1fd-037e-b188-60cfacb0c537
- Retrieved: YES (full PDF text-extracted locally)
- Role in this library: the 150% stacking factor, the index-margin (spread) crediting method, and
  the disclosure that a built-in GLWB is funded through lower caps, participation rates and
  higher index margins rather than an explicit charge.

### S9. Nassau Life and Annuity Company — "Indexed Annuity Rider Disclosure Document — Amplified Income Plus" (form OL5370B, 8/25; rider forms 19GLWB3, ICC19GLWB3.1) — SAMPLE
- Publisher: Nassau Life and Annuity Company (Nassau Financial Group) — official assets.nfg.com
  document
- Doc type: **signed rider disclosure document (specimen)** — the most contractually precise GLWB
  description retrieved
- URL fetched: https://assets.nfg.com/documents/salesnet/NGARider-OL5370-sample.pdf
- Retrieved: YES (full PDF text-extracted locally)
- Role in this library: the primary GLWB mechanics anchor — simple roll-up on the adjusted initial
  base, the 150% Echo stacking credit, the 0.95%-of-benefit-base rider fee and its 1.50% cap, the
  verbatim excess-withdrawal reduction formula, and the cause-dependent post-depletion rule.

### S10. Nassau Life and Annuity Company — "Indexed Annuity Disclosure Document — Nassau Athos Annuity<sup>SM</sup>, Single Premium Fixed Indexed Annuity (Bonus)" (form OL5719, 6/26; contract form 25FIA-XT) — SAMPLE
- Publisher: Nassau Life and Annuity Company — official assets.nfg.com document
- Doc type: **signed base-contract disclosure document (specimen)**, 34 pages
- URL fetched: https://assets.nfg.com/documents/salesnet/OL5719.pdf
- Retrieved: YES (full PDF text-extracted locally)
- Role in this library: the base-contract mechanics anchor — the verbatim non-vested premium bonus
  recovery formula `(1 − A) × [B/(1+B)] × C`, the ratio-form MVA and its limit, the surrender
  charge base, and the Total Guaranteed Value at 87.5% of premium excluding the bonus accumulated
  at 0.15%–3%.

### S11. Nationwide Life and Annuity Insurance Company — "Nationwide New Heights® fixed indexed annuities — Index and Strategy Growth Opportunities" (form FAM-0475AO.2 (1/17))
- Publisher: Nationwide Life and Annuity Insurance Company (Nationwide-operated marketing asset
  host `s3.amazonaws.com/nh3`)
- Doc type: consumer strategy brochure (6 pages)
- URL fetched: https://s3.amazonaws.com/nh3/FAM-0475AO.2_Strategy_Brochure.pdf
- Retrieved: YES (full PDF text-extracted locally)
- Note carried over: a 2017-vintage document retained because it documents a structurally
  different FIA design (the Balanced Allocation Strategy / Balanced Allocation Value) that is
  worth modeling as a variation. Current New Heights Select rates were not retrieved (see S-f4);
  the design is described qualitatively only, with no numeric parameters.

### Documents attempted but NOT retrieved (no content asserted from these)

| ID | Document | URL | Failure |
|---|---|---|---|
| S-f1 | Athene Ascent Pro 10 "Rates and Availability" | https://athenecentral.widen.net/s/lhw7bjvvzz/65219 | Widen viewer / password-protected PDF; no text |
| S-f3 | American Equity IncomeShield 10 brochure (official) | https://media.american-equity.com/Documents/1164-SB-10.pdf | DNS resolution failure (`getaddrinfo ENOTFOUND`) from this environment; content obtained from the mirror at S5 instead |
| S-f4 | Nationwide New Heights Select 10 product brochure | https://nationwidefinancial.com/media/pdf/FAM-1606AO.pdf | HTTP 403 |

These three are cited in `product-spec.md` and `technical-notes.md` only as the *reason* certain
declared-rate parameters are stale or absent.

---

## Regulatory and actuarial references [R#] (product research file numbering)

### R1. American Academy of Actuaries, Life Experience Committee — "Fixed Indexed Annuities—Product Mechanics and Risk Management" (February 2026)
- Publisher: American Academy of Actuaries
- URL fetched: https://actuary.org/wp-content/uploads/2026/02/life-FIA-policypaper.pdf
- Retrieved: YES (31-page PDF text-extracted locally)
- Status disclaimer carried over: not an ASOP, not binding, "a list of considerations and
  resources."
- Same document as [REG-R68] in the cross-product library.

### R2. NAIC — "Standard Nonforfeiture Law for Individual Deferred Annuities" (Model #805), NAIC Model Laws, Regulations, Guidelines and Other Resources — Fall 2020
- Publisher: National Association of Insurance Commissioners
- URL fetched: https://content.naic.org/sites/default/files/model-law-805.pdf
- Retrieved: YES (5-page PDF text-extracted locally)
- Same document as [REG-R42].

### R3. NAIC — "Annuity Nonforfeiture Model Regulation" (Model #806), October 2007 edition
- Publisher: National Association of Insurance Commissioners
- URL fetched: https://content.naic.org/sites/default/files/model-law-806.pdf
- Retrieved: YES (12-page PDF text-extracted locally)
- No counterpart entry exists in the cross-product library; cite [R3] for the §7 substantive-
  participation option-cost test.

### R4. NAIC — "Suitability in Annuity Transactions Model Regulation" (Model #275), Spring 2020 edition
- Publisher: National Association of Insurance Commissioners
- URL fetched: https://content.naic.org/sites/default/files/model-law-275.pdf
- Retrieved: YES (20-page PDF; sections 1–5 text-extracted locally)
- Same document as [REG-R46].

### R5. NAIC — "Variable Annuity Model Regulation" (Model #250), October 2007 edition
- Publisher: National Association of Insurance Commissioners
- URL fetched: https://content.naic.org/sites/default/files/model-law-250.pdf
- Retrieved: YES (13-page PDF; sections 1–3 text-extracted locally)
- Cited only for the correction carried into `product-spec.md`: #250 is the Variable Annuity Model
  Regulation and does not reach general-account FIAs; the Annuity Disclosure Model Regulation is
  **#245**. Same document as [REG-R43].

### R6. Actuarial Standards Board — ASOP No. 2, "Nonguaranteed Elements for Life Insurance and Annuity Products" (Doc. No. 204)
- Publisher: Actuarial Standards Board
- URL fetched: http://www.actuarialstandardsboard.org/wp-content/uploads/2021/12/asop002_204-2.pdf
- Retrieved: YES (33-page PDF; front matter and sections 1–3.4 text-extracted locally)
- Same standard as [REG-R26].

### R7. NAIC — Valuation Manual (VM)-22 (A) Subgroup
- Publisher: National Association of Insurance Commissioners
- URL fetched: https://content.naic.org/committees/a/valuation-manual-22-sg
- Retrieved: YES (HTML page)

### R8. Society of Actuaries Research Institute / LIMRA — "2019-20 Fixed Indexed Annuity Contract Owner Behavior Study" (announcement page)
- Publisher: Society of Actuaries Research Institute (joint with LIMRA)
- URL fetched: https://www.soa.org/resources/announcements/press-releases/2023/fixed-indexed-annuity/
- Retrieved: YES (HTML page). The report PDF at
  https://www.soa.org/4a3268/globalassets/assets/files/resources/experience-studies/2023/19-20-fia-contract-owner.pdf
  returned **HTTP 404** and was not retrieved.
- Role in this library: the retrieved source for the 10%-with-GLWB versus 33%-without shock-lapse
  contrast, the 37% versus <30% withdrawal-incidence contrast, and the subsequent-premium rates.
  Related landing pages are catalogued as [REG-R62], where the same shock-lapse figures are
  tagged [unverified].

### R9. Society of Actuaries Research Institute / LIMRA — "2023 Fixed Indexed Annuity Contract Owner Behavior Experience Study" (study landing page, 2025)
- Publisher: Society of Actuaries Research Institute
- URL fetched: https://www.soa.org/resources/experience-studies/2025/2023-fixed-index-annuity/
- Retrieved: YES (HTML page). Detailed results are behind a paid Experience Studies Pro
  subscription and were **not** retrieved; the report PDF is listed at
  https://www.soa.org/globalassets/assets/files/research/exp-study/2025/2023-fixed-indexed-anuity-study.pdf
  (not fetched).
- Cited for study scope only.

### R10. SEC — Final Rule, "Indexed Annuities," Release No. 33-9152 (removal of Rule 151A)
- Publisher: U.S. Securities and Exchange Commission
- URLs attempted:
  - https://www.sec.gov/files/rules/final/2010/33-9152.pdf → **HTTP 403** (not retrieved)
  - https://www.federalregister.gov/documents/2010/10/20/2010-26347/indexed-annuities →
    **302 redirect to an interstitial host** (not retrieved)
- Retrieved: **NO**
- Everything cited to [R10] is tagged [unverified]: the *American Equity Investment Life
  Insurance Co. v. SEC* vacatur and the specific conditions of Dodd-Frank §989J. What **is**
  verified is Model #275's own drafting note [R4] and the not-a-security statements in
  [S6][S9][S10].

### R11. NAIC Actuarial Guidelines XXXIII and XXXV (AG 33, AG 35)
- Retrieved: **NO** — the guidelines live in the NAIC Accounting Practices & Procedures Manual,
  which is not freely served in text form; no primary copy was successfully fetched.
- Everything this library says about AG 33 / AG 35 derives from [R1] (the Academy FIA paper), a
  secondary but authoritative professional source, and is tagged accordingly. The "Type 1" /
  "Type 2" naming is [unverified]. Titles and continued incorporation into the Valuation Manual
  are independently verifiable via [REG-R41]; the authoritative text sits in [REG-R33].

---

## Cross-product regulatory references [REG-R#]

Cited with the **[REG-R#]** prefix to avoid collision with the product research file's own
R-numbering. The curated page these resolve to is
`us/references/regulatory-and-actuarial-references.md`. That page carries **one shared numbering
space, now running R1–R157, with R114–R124 and R143–R149 permanently unused by design**: entries
**R1–R34** originate in `us/_research/regulatory-actuarial.md` (the life bibliography, several
entries of which also bind annuity models), entries **R35–R72** in
`us/_research/regulatory-actuarial-annuities.md` (the annuity extension), and entries **R73–R142**
in the statutory accounting and capital research behind `us/regulatory/`. The gaps are not losses
and must not be back-filled — the block convention lets a stream finish with spare numbers so a
later pass can extend it without renumbering anything already cited. Retrieval markers below are
those recorded in the originating research file.

| Tag | Short title | Research file | Retrieval status per that file |
|---|---|---|---|
| REG-R1 | Standard Valuation Law (Model #820) | life (R1–R34) | see the reference page's per-entry marker |
| REG-R2 | Standard Nonforfeiture Law for Life Insurance (Model #808) | life | see the reference page; cited here only to prevent mis-application to annuities |
| REG-R3 | NAIC Valuation Manual, Jan. 1, 2026 edition | life | fetched |
| REG-R8 | Actuarial Guideline XLIX (AG 49) — IUL illustrations under Model #582 | life | see the reference page (no standalone official text located) |
| REG-R10 | Actuarial Guideline XLIX-A (AG 49-A, incl. the 2023 "AG 49-B" revisions) — IUL illustrations | life | fetched |
| REG-R16 | 26 U.S.C. §807 — tax reserves | life | fetched |
| REG-R26 | ASOP No. 2 — Nonguaranteed Elements (same standard as [R6]) | life | fetched |
| REG-R27 | ASOP No. 7 — Life or Health Cash Flow Analysis | life | fetched |
| REG-R29 | ASOP No. 22 — Opinions based on asset adequacy analysis | life | see the reference page |
| REG-R32 | ASOP No. 56 — Modeling | life | fetched |
| REG-R33 | NAIC AP&P Manual (home of AG 33 / AG 35, Appendix C) | life | see the reference page (paid publication) |
| REG-R34 | FASB ASU 2018-12 (LDTI) — market risk benefits | life | see the reference page |
| REG-R36 | VM-22 — PBR for non-variable annuities (2026 edition) | annuities (R35–R72) | yes (local text extraction) |
| REG-R37 | VM-V Section 1 — income annuity maximum valuation interest rates | annuities | yes (local text extraction) |
| REG-R39 | Actuarial Guideline XXXIII (AG 33) | annuities | **no** (title verified via REG-R41) |
| REG-R40 | Actuarial Guideline XXXV (AG 35) | annuities | **no** (title verified via REG-R41) |
| REG-R41 | VM-C — index of actuarial guidelines incorporated | annuities | yes (local text extraction) |
| REG-R42 | Model #805 nonforfeiture (same document as [R2]) | annuities | yes (local text extraction) |
| REG-R43 | Model #250 Variable Annuity Model Reg (same document as [R5]) | annuities | yes (local text extraction) |
| REG-R45 | Model #245 Annuity Disclosure Model Regulation | annuities | yes (local text extraction) |
| REG-R46 | Model #275 Suitability (same document as [R4]) | annuities | yes (local text extraction) |
| REG-R49 | SEC Release 33-11294 — RILA registration, Form N-4 | annuities | yes (govinfo); sec.gov PDF 403 |
| REG-R53 | CRS Report R40656 — Rule 151A and Dodd-Frank §989J | annuities | yes |
| REG-R55 | 26 U.S.C. §72 — annuity taxation | annuities | yes |
| REG-R56 | 26 U.S.C. §1035 — exchanges | annuities | yes |
| REG-R57 | 26 C.F.R. §1.401(a)(9)-6 — RMDs for annuity contracts / QLACs | annuities | yes |
| REG-R58 | T.D. 10001 — RMD final regulations (2024) | annuities | yes (govinfo) |
| REG-R59 | Model #821 + VM-M — 2012 IAM / 2012 IAR, Scale G2 | annuities | yes (local text extraction, both) |
| REG-R60 | 2012 IAR development report (AAA/SOA) | annuities | yes (local text extraction) |
| REG-R61 | 2020–2024 Individual Payout Annuity Mortality Experience Study | annuities | yes (landing page) |
| REG-R62 | FIA policyholder behavior studies 2021–22 and 2019–20 | annuities | yes (both landing pages); the shock-lapse figures are [unverified] there |
| REG-R63 | Fixed rate deferred surrender studies (2023–24, 2015–2022) | annuities | partial (via the REG-R65 index) |
| REG-R64 | VA contract holder behavior / GLB utilization studies | annuities | yes (2022–24 landing page); utilization figures [unverified] |
| REG-R65 | SOA Individual Annuity Experience Studies — index | annuities | yes |
| REG-R67 | AAA — Utilization Assumptions of Guaranteed Living Benefits (May 2024) | annuities | yes (local text extraction) |
| REG-R68 | AAA — Fixed Indexed Annuities: Product Mechanics and Risk Management (same paper as [R1]) | annuities | yes (local text extraction) |
| REG-R70 | ASOP No. 54 — Pricing of Life Insurance and Annuity Products | annuities | yes |
| REG-R71 | ASOP No. 10 — U.S. GAAP for Long-Duration Products (Doc. No. 207) | annuities | yes (local text extraction) |

### Statutory accounting and capital entries (R73–R142) cited by the "Statutory accounting and capital" section

Added when `technical-notes.md` gained its "Statutory accounting and capital" section and
`product-spec.md` its statutory-accounting paragraph. **Id, title, publisher, URL, access date,
fetched marker and every carried-forward limit below are reproduced verbatim from
`us/regulatory/sources.md`**, which in turn carries them verbatim from
`us/_research/statutory-accounting.md` (R73–R99), `us/_research/statutory-reserves.md` (R100–R113)
and `us/_research/risk-based-capital.md` (R125–R142). **Ids are never renumbered.** No new sources
were fetched. Several entries locate themselves "in R73" — the NAIC *Accounting Practices and
Procedures Manual, As of March 2026*, retrieved in full and catalogued in `us/regulatory/sources.md`;
it is not cited directly in this product's documents and so is not repeated here.

**Access date for every entry in this subsection: 2026-08-04.**

#### R74. AP&P Manual **Preamble** — Statutory Accounting Principles Statement of Concepts and Statutory Hierarchy (*As of March 2026*)
- **Publisher:** NAIC (Preamble, pages P-1 to P-10 of R73)
- **URL:** https://content.naic.org/sites/default/files/publication-app-manual.pdf (Preamble section)
- **Accessed:** 2026-08-04 · **Fetched:** yes (local text extraction; §§27–42 read in full)

#### R75. SSAP No. 71 — Policy Acquisition Costs and Commissions (*As of March 2026*)
- **Publisher:** NAIC (in R73, statement pages 71-1 to 71-3)
- **URL:** https://content.naic.org/sites/default/files/publication-app-manual.pdf
- **Accessed:** 2026-08-04 · **Fetched:** yes (local text extraction; ¶¶1–7 read in full)

#### R78. SSAP No. 50 — Classifications of Insurance or Managed Care Contracts (*As of March 2026*)
- **Publisher:** NAIC (in R73, statement pages 50-1 onward)
- **URL:** https://content.naic.org/sites/default/files/publication-app-manual.pdf
- **Accessed:** 2026-08-04 · **Fetched:** yes (local text extraction; ¶¶1–20 read)

#### R79. SSAP No. 51 — Life Contracts (*As of March 2026*; historically cited as SSAP No. 51R)
- **Publisher:** NAIC (in R73, statement pages 51-1 to 51-13)
- **URL:** https://content.naic.org/sites/default/files/publication-app-manual.pdf
- **Accessed:** 2026-08-04 · **Fetched:** yes (local text extraction; status block, ¶¶1–16 read;
  section index read)
- **Limit carried forward:** ¶¶17 onward (mean/mid-terminal reserves, dividends, coupons,
  accelerated benefits, disclosures) were read through the **section index and the parallel
  Issue Paper No. 51 text (R81)**, not the SSAP paragraphs. Paragraph numbers differ between
  IP 51 and SSAP No. 51; a precise SSAP No. 51 paragraph cite needs R73 at pages 51-5 to 51-12.

#### R80. SSAP No. 52 — Deposit-Type Contracts (*As of March 2026*)
- **Publisher:** NAIC (in R73, statement pages 52-1 to 52-8)
- **URL:** https://content.naic.org/sites/default/files/publication-app-manual.pdf
- **Accessed:** 2026-08-04 · **Fetched:** yes (local text extraction; ¶¶1–17 read in full)

#### R83. SSAP No. 56 — Separate Accounts (*As of March 2026*)
- **Publisher:** NAIC (in R73, statement pages 56-1 to 56-14)
- **URL:** https://content.naic.org/sites/default/files/publication-app-manual.pdf
- **Accessed:** 2026-08-04 · **Fetched:** yes (local text extraction; ¶¶1–31 and the glossary read)

#### R86. Statutory Issue Paper No. 7 — Asset Valuation Reserve and Interest Maintenance Reserve
- **Publisher:** NAIC (finalized March 16, 1998; AP&P Appendix E)
- **URL:** https://content.naic.org/sites/default/files/inline-files/007_G.pdf
- **Accessed:** 2026-08-04 · **Fetched:** yes (local text extraction; 12 pages, read in full)
- **Vintage caution carried forward:** the AVR/IMR instruction text quoted in this issue
  paper is **1990s vintage**; the current factors, groupings and rules are at R89 and differ
  in detail (e.g. the grouped-method bands now begin with a separate "0 calendar years" band).

#### R87. INT 23-01 — Net Negative (Disallowed) Interest Maintenance Reserve (revised print, adopted August 11, 2025)
- **Publisher:** NAIC Statutory Accounting Principles (E) Working Group (AP&P Appendix B)
- **URL:** https://content.naic.org/sites/default/files/inline-files/22-19%20-%20INT%2023-01%20-%20Revised%20April%202025.pdf
  (original clean adoption print, August 13, 2023:
  https://content.naic.org/sites/default/files/inline-files/22-19a%20-%20INT%2023-01%20-%20IMR%20clean.pdf — also fetched)
- **Accessed:** 2026-08-04 · **Fetched:** yes, both (local text extraction; 8 pages each; the
  revised print carries visible tracked-change artefacts, which is how the extension is evidenced)

#### R88. SAPWG 2026 Spring National Meeting — Meeting Summary Report (March 23, 2026)
- **Publisher:** NAIC Statutory Accounting Principles (E) Working Group
- **URL:** https://content.naic.org/sites/default/files/national_meeting/2026-spnm-summary-e-sapwg.pdf
- **Accessed:** 2026-08-04 · **Fetched:** yes (local text extraction; 3 pages, read in full)
- **Limit carried forward:** this is the **most recent SAPWG record retrieved**. The 2026
  Summer National Meeting had not been reported on at the access date, and the exposed
  **revised SSAP No. 7** (the intended replacement for INT 23-01) was **not located or read**.

#### R89. NAIC Annual Statement Instructions — Life, Accident & Health/Fraternal, 2025 reporting year
- **Publisher:** NAIC ("Adopted by the NAIC as of June 2025"; free download from the NAIC
  Resource Center)
- **URL:** https://content.naic.org/sites/default/files/publication-asi-lua-25.pdf
- **Accessed:** 2026-08-04 · **Fetched:** yes (local text extraction; 1,008 pages; Analysis of
  Operations pp. 84–96, Exhibits 5 / 5A / 6 / 7 pp. 143–157, Exhibit of Life Insurance p. 383,
  IMR pp. 390–404, AVR pp. 405–428 read)
- **Numbers deliberately not transcribed:** the **AVR factor tables** (basic contribution,
  reserve objective, maximum reserve, by NAIC designation and mortgage category) and the
  **IMR grouped-amortisation factor tables**. No value for either is stated anywhere in this library.
- **Reporting-year caution:** this is the **2025** reporting year. Every page and line
  reference should be re-verified against the 2026 blank before being hard-coded.

#### R90. NAIC Annual Statement Blank — Life, Accident & Health/Fraternal, 2025
- **Publisher:** NAIC (free download)
- **URL:** https://content.naic.org/sites/default/files/publication-asb-life.pdf
- **Accessed:** 2026-08-04 · **Fetched:** yes (local text extraction; 211 pages; Liabilities page,
  Summary of Operations p. 13, Cash Flow p. 14, Analysis of Operations by LOB pp. 15–20, Analysis of
  Increase in Reserves pp. 21–24, Exhibits 5–7 pp. 29–32, Exhibit of Life Insurance pp. 52–53,
  IMR form p. 55, AVR forms pp. 56–63 read)

#### R91. SSAP No. 5 — Liabilities, Contingencies and Impairments of Assets, with Statutory Issue Paper No. 5 (*As of March 2026*; historically SSAP No. 5R)
- **Publisher:** NAIC (SSAP in R73, statement pages 5-1 onward; issue paper in Appendix E)
- **URLs:** https://content.naic.org/sites/default/files/publication-app-manual.pdf ;
  Issue Paper No. 5: https://content.naic.org/sites/default/files/inline-files/005_J.pdf
- **Accessed:** 2026-08-04 · **Fetched:** yes, both (local text extraction; issue paper 8 pages
  read in full)
- **Note on paragraph cites:** the ¶ numbers used are **Issue Paper No. 5's**, tagged
  `[REG-R91/IP5 ¶n]`, because the issue paper is what was read in full.

#### R92. SSAP No. 61 — Life, Deposit-Type and Accident and Health Reinsurance (*As of March 2026*; historically 61R)
- **Publisher:** NAIC (in R73, statement pages 61-1 to 61-29 plus glossary)
- **URL:** https://content.naic.org/sites/default/files/publication-app-manual.pdf
- **Accessed:** 2026-08-04 · **Fetched:** yes (local text extraction; ¶¶1–20, 36–38, 54–59 read;
  full section index read)
- **Limit carried forward:** **Appendix A-791** (Life and Health Reinsurance Agreements — the
  prohibited-conditions list that ¶¶17–19 turn on) was **not read**, only cited through this
  entry. It is in R73 Appendix A.

#### R96. SSAP No. 86 — Derivatives (*As of March 2026*)
- **Publisher:** NAIC (in R73, statement pages 86-1 onward, with Exhibits A–C)
- **URL:** https://content.naic.org/sites/default/files/publication-app-manual.pdf
  (an older standalone print of the statement, "SSAP No. 86 — Accounting for Derivative
  Instruments and Hedging Activities", is hosted by the CFTC as part of an NAIC Dodd-Frank
  submission and was also fetched:
  https://www.cftc.gov/sites/default/files/idc/groups/public/@swaps/documents/dfsubmission/dfsubmission21_110910-naic7.pdf)
- **Accessed:** 2026-08-04 · **Fetched:** yes, both (local text extraction; scope and definitions,
  hedge-designation, fair-value-hedge, cash-flow-hedge, effectiveness, income-generation and
  replication sections read; hedge-accounting measurement paragraphs read in both prints)
- **[unverified] carried forward:** the paragraph numbers cited (¶¶15–20, including the ¶17
  IMR election) are from the **2010 standalone print** and were **not cross-checked** against
  the March 2026 manual. Exhibits A, B and C were not read.

#### R97. SSAP No. 101 — Income Taxes (*As of March 2026*)
- **Publisher:** NAIC (in R73, statement pages 101-1 onward, with Exhibit A Q&A)
- **URL:** https://content.naic.org/sites/default/files/publication-app-manual.pdf
- **Accessed:** 2026-08-04 · **Fetched:** yes (local text extraction; status block, ¶¶1–2 and the
  full admissibility section ¶¶11–12 including all three Realization Threshold Limitation Tables read)

#### R100. VM-30: Actuarial Opinion and Memorandum Requirements (Valuation Manual, Jan. 1, 2026 Edition)
- **Publisher:** NAIC
- **URL:** https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf
  (pages 30-1 to 30-15 of the 457-page PDF; same document as REG-R3)
- **Accessed:** 2026-08-04 · **Fetched:** yes (local text extraction; **Sections 1, 2 and 3 read in
  full**, including the prescribed opinion wording and the Regulatory Asset Adequacy Issues Summary
  contents; copyright line "© 2025 National Association of Insurance Commissioners")

#### R103. Actuarial Guideline LV — Application of the Valuation Manual for Testing the Adequacy of Reserves Related to Certain Life Reinsurance Treaties (AG 55)
- **Publisher:** NAIC (this print: "Adopted by Life Insurance and Annuities (A) Committee –
  July 14, 2025 / Adopted by Life Actuarial (A) Task Force – June 5, 2025"; © 2025; 14 pages)
- **URL:** https://content.naic.org/sites/default/files/committees-pending-action-aglv.pdf
- **Accessed:** 2026-08-04 · **Fetched:** yes (local text extraction; **entire guideline read,
  Sections 1–9 and Appendix 1**). A guessed URL `.../inline-files/AG%2055.pdf` returned HTTP 404
  and is not cited.
- **[unverified] carried forward:** adoption by the NAIC **Executive (EX) Committee and
  Plenary on August 13, 2025**. The **effective** date (reserves reported in the December 31, 2025
  annual statement) **is** printed in the guideline and is verified.

#### R104. NAIC Reinsurance (E) Task Force — 2025 Fall National Meeting materials (including the adopted minutes of the Aug. 11, 2025 Summer National Meeting session)
- **Publisher:** NAIC (draft dated 12/4/25; minutes draft dated 8/19/25)
- **URL:** https://content.naic.org/sites/default/files/national_meeting/Materials-RTF-12-9-2025_0.pdf
- **Accessed:** 2026-08-04 · **Fetched:** yes (local text extraction; 7-page packet; agenda and the
  Aug. 11, 2025 minutes read)

#### R105. Actuarial Guideline LIII — Application of the Valuation Manual for Testing the Adequacy of Life Insurer Reserves (AG 53)
- **Publisher:** NAIC (print paginated "AG53-1" to "AG53-8" and headed "Appendix C", i.e. the
  AP&P Manual Appendix C text)
- **URL:** https://content.naic.org/sites/default/files/inline-files/AG%2053.pdf
- **Accessed:** 2026-08-04 · **Fetched:** yes (local text extraction; **entire guideline read,
  Sections 1–6 and Appendix I**)

#### R106. AG 53 Guidance Document — Year-End 2025
- **Publisher:** NAIC, for the Valuation Analysis (E) Working Group (VAWG)
- **URL:** https://content.naic.org/sites/default/files/inline-files/AG-53-guidance-YE-2025%20(1).pdf
- **Accessed:** 2026-08-04 · **Fetched:** yes (local text extraction; 5-page document read)

#### R108. VM-31: PBR Actuarial Report Requirements for Business Subject to a Principle-Based Valuation (Valuation Manual, Jan. 1, 2026 Edition)
- **Publisher:** NAIC
- **URL:** https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf
  (pages 31-1 to 31-46; same document as REG-R3)
- **Accessed:** 2026-08-04 · **Fetched:** yes (local text extraction; Sections 1, 2, 3.A, 3.B, 3.C
  and 3.D.1–3.D.3 read; the full table of contents and section headers of 3.D–3.F reviewed)

#### R109. VM-G: Appendix G — Corporate Governance Guidance for Principle-Based Reserves (Valuation Manual, Jan. 1, 2026 Edition)
- **Publisher:** NAIC
- **URL:** https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf
  (pages G-1 to G-6; same document as REG-R3)
- **Accessed:** 2026-08-04 · **Fetched:** yes (local text extraction; **Sections 1–4 read in full**)

#### R110. VM-A: Appendix A — Requirements (Valuation Manual, Jan. 1, 2026 Edition)
- **Publisher:** NAIC
- **URL:** https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf
  (pages A-1 to A-2; same document as REG-R3)
- **Accessed:** 2026-08-04 · **Fetched:** yes (local text extraction; the complete two-page index read)
- **Limit carried forward:** VM-A is an **index, not a text**. The requirements it indexes —
  above all **A-820** (minimum life and annuity reserve standards) and **A-830** (valuation of
  life insurance policies) — live in AP&P Appendix A and **were not retrieved**.

#### R111. Asset Adequacy Analysis — Public Policy Practice Note, for companies that file a Life, Accident and Health/Fraternal Statutory Annual Statement
- **Publisher:** American Academy of Actuaries, Asset Adequacy Analysis Practice Note Work
  Group and the Life Valuation Committee; **September 2017, updated September 2024**; 93 pages
- **URL (PDF):** https://actuary.org/wp-content/uploads/2025/03/Life-PracticeNote-2017AATUpdate.pdf
  — **URL (landing page):** https://actuary.org/resources/asset-adequacy-analysis-updated-for-2024/
- **Accessed:** 2026-08-04 · **Fetched:** yes, both (PDF by local text extraction)
- **Status and vintage cautions carried forward:** not an ASB promulgation, not an ASOP, not
  binding. Its quantitative statements come from appointed-actuary surveys conducted in
  **2004 and 2012** and are practice indicators, not benchmarks. Its statement that INT 23-01
  was nullified on January 1, 2026 was written in September 2024 and is **superseded** by the
  August 11, 2025 extension recorded at R87.

#### R125. Risk-Based Capital (RBC) for Insurers Model Act (Model #312)
- **Publisher:** National Association of Insurance Commissioners
- **URL:** https://content.naic.org/sites/default/files/model-law-312.pdf
- **Accessed:** 2026-08-04 · **Fetched:** yes (local text extraction; 14-page PDF; print
  header "NAIC Model Laws, Regulations, Guidelines and Other Resources—January 2012")

#### R128. NAIC *Risk-Based Capital Forecasting and Instructions — 2024, Life / Fraternal*
- **Publisher:** NAIC (© 2019–2024 NAIC; instruction pages dated 10/14/2024). **Paid NAIC
  publication**; the copy read was posted publicly by the **Indiana Department of Insurance**.
- **URL:** https://www.in.gov/idoi/files/RBCL24-INpdf.pdf
- **Accessed:** 2026-08-04 · **Fetched:** yes (local text extraction; 225 pages; overview,
  LR002, LR025, LR025-A, LR027, LR029, LR030, LR031, LR033, LR034, LR035, LR049, Appendix 1,
  Appendix 1a and the corresponding blank pages read)
- **Paid-publication limit, stated plainly:** this document is *sold* by the NAIC and marked "Not
  for Distribution" on every page. Anyone rebuilding this work should **buy the current edition**
  rather than rely on a state posting. The **2025 edition could not be parsed**, so no year-end
  2025 factor is asserted anywhere in this library, and the **RBC forecasting spreadsheet** was
  never obtained.

#### R135. *Phase I Report of the American Academy of Actuaries' C-3 Subgroup of the Life Risk Based Capital Task Force to the NAIC's Risk Based Capital Work Group* (October 1999, Atlanta)
- **Publisher:** American Academy of Actuaries
- **URL:** https://www.actuary.org/wp-content/uploads/2025/05/c3_oct99.pdf
- **Accessed:** 2026-08-04 · **Fetched:** yes (local text extraction; 43 pages; executive
  summary and Appendix I scenario-testing methodology read)

#### R137. American Academy of Actuaries Life Investment and Capital Adequacy Committee, *Correlation in Life Risk Based Capital* (presentation to the NAIC Life RBC (E) Working Group)
- **Publisher:** American Academy of Actuaries (© 2025 on the actuary.org re-post; the file
  name carries "4-24", i.e. an April 2024 presentation date [unverified])
- **URL:** https://actuary.org/wp-content/uploads/2025/05/Life-Presentation-LRBC-Correlation-4-24.pdf
- **Accessed:** 2026-08-04 · **Fetched:** yes (local text extraction; 25 slides)
- **Status:** a **proposal, not adopted law**. It is **not** in the 2024 instructions (R128);
  whether it has since been adopted was not established.

#### R138. American Academy of Actuaries, *C-3 Alignment, Part III* (presentation to the NAIC Life RBC (E) Working Group, September 11, 2025)
- **Publisher:** American Academy of Actuaries
- **URL:** https://actuary.org/wp-content/uploads/2025/09/Life-Presentation-C3AlignmentUpdate.pdf
- **Accessed:** 2026-08-04 · **Fetched:** yes (local text extraction; 65 slides, including
  appended Part II from May 1, 2025)
- **Status and [unverified] carried forward:** a **framework presentation**, not adopted law.
  The field-test specifications document itself was **not retrieved** (only the working group
  page's note of a **July 30, 2026** re-exposure, R141); the reported **December 31, 2025**
  field-test valuation date and **2027** adoption target come from search summaries and are
  **[unverified]**.

#### R141. NAIC Life Risk-Based Capital (E) Working Group
- **Publisher:** NAIC · **URL:** https://content.naic.org/committees/e/life-risk-based-capital-wg
- **Accessed:** 2026-08-04 · **Fetched:** yes (web page)

---

## Provenance note

Extraction details live in `us/_research/fixed-indexed-annuity.md`: that file records which facts
came from which source, including every [unverified] flag, the failed fetches (S-f1 through S-f4,
R10, R11), the mirror-hosting caveat for S1, S2 and S5 (fetched from authorized-distributor
mirrors carrying the insurers' own form numbers), the retrieval method note (several publisher
PDFs were downloaded and text-extracted locally with `pypdf`, and nothing is asserted from a
document marked Retrieved: NO), and the vintage caveat that all declared rates are non-guaranteed
elements captured only as of the dates stamped on their documents. The cross-product
bibliographies `us/_research/regulatory-actuarial.md` (R1–R34),
`us/_research/regulatory-actuarial-annuities.md` (R35–R72),
`us/_research/statutory-accounting.md` (R73–R99), `us/_research/statutory-reserves.md` (R100–R113)
and `us/_research/risk-based-capital.md` (R125–R142) play the same role for [REG-R#] tags,
and `us/references/regulatory-and-actuarial-references.md` is the curated page those tags resolve
to; where this file and a research file disagree, **the research file governs**. Standardizations
marked **[std]** in `product-spec.md` and `technical-notes.md` are introduced at drafting and are
not attributable to any source; **[unverified]** flags are carried forward unchanged and none was
upgraded.
