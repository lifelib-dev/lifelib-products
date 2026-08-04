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
retrievals.

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
`us/references/regulatory-and-actuarial-references.md`. That page carries **one shared R1–R72
numbering space**: entries **R1–R34** originate in `us/_research/regulatory-actuarial.md` (the
life bibliography, several entries of which also bind annuity models) and entries **R35–R72**
originate in `us/_research/regulatory-actuarial-annuities.md` (the annuity extension). Retrieval
markers below are those recorded in the originating research file.

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

---

## Provenance note

Extraction details live in `us/_research/fixed-indexed-annuity.md`: that file records which facts
came from which source, including every [unverified] flag, the failed fetches (S-f1 through S-f4,
R10, R11), the mirror-hosting caveat for S1, S2 and S5 (fetched from authorized-distributor
mirrors carrying the insurers' own form numbers), the retrieval method note (several publisher
PDFs were downloaded and text-extracted locally with `pypdf`, and nothing is asserted from a
document marked Retrieved: NO), and the vintage caveat that all declared rates are non-guaranteed
elements captured only as of the dates stamped on their documents. The cross-product
bibliographies `us/_research/regulatory-actuarial.md` (R1–R34) and
`us/_research/regulatory-actuarial-annuities.md` (R35–R72) play the same role for [REG-R#] tags,
and `us/references/regulatory-and-actuarial-references.md` is the curated page those tags resolve
to. Standardizations marked **[std]** in `product-spec.md` and `technical-notes.md` are introduced
at drafting and are not attributable to any source.
