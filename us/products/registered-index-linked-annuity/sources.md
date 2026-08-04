# Sources — Registered Index-Linked Annuity (RILA) (United States)

Source ids, titles, publishers, URLs, access dates, and fetched/not-fetched markers are
carried over **verbatim** from `us/_research/registered-index-linked-annuity.md` (the
citation ground truth for [S#]/[R#] tags). Ids are never renumbered. Sources from the
research file that are not cited in `product-spec.md` or `technical-notes.md` are omitted
— **none were dropped**: all of S1–S6 and R1–R6 are cited. **No new sources were fetched
at drafting**; nothing below is marked "added at drafting".

Access date for all citations: **2026-08-04** (cross-product entries R1–R34 carry their
own access date of 2026-08-03 — see the [REG-R#] section).

---

## Primary product sources [S#]

### S1. Brighthouse Life Insurance Company of NY — "Brighthouse Shield Level Select 6-Year Annuity", Form S-3 registration statement
- Publisher: Brighthouse Life Insurance Company of NY ("BLNY"), CIK 0001167609
- Doc type: Securities Act registration statement / statutory prospectus (Form S-3, the
  pre-2024 RILA registration form). Filed 2019-02-06, accession 0001193125-19-030795.
- URL fetched: https://www.sec.gov/Archives/edgar/data/1167609/000119312519030795/d695141ds3.htm
- Retrieved: YES (full document downloaded and read; note sec.gov rejects generic fetchers
  with HTTP 403 — a declared User-Agent is required)
- Product: Brighthouse Shield Level Select 6-Year Annuity — "an individual single premium
  deferred index-linked separate account annuity contract". New York version only.
  Separate Account: Brighthouse Separate Account SA II.
- Role in this library: documents the **older, pro-rata "accrued rate" interim value
  design**, retained as the legacy contrast module and first implementation target; also
  the source for issue rules, free-withdrawal and withdrawal-charge mechanics, the
  return-of-premium death benefit, the Transfer Period, and the Cap/Step crediting
  worked examples.

### S2. Brighthouse Life Insurance Company — "Brighthouse Shield Level II 6-Year Annuity", Rule 424(b)(3) prospectus
- Publisher: Brighthouse Life Insurance Company ("BLIC"), CIK 0000733076
- Doc type: statutory prospectus filed under Rule 424(b)(3), filed 2024-07-26, accession
  0001193125-24-180915
- URL fetched: https://www.sec.gov/Archives/edgar/data/733076/000119312524180915/d747348d424b3.htm
- Retrieved: YES (full document downloaded and read)
- Product: Brighthouse Shield Level II 6-Year Annuity — individual single premium deferred
  index-linked separate account annuity contract.
- Role in this library: **the mechanics anchor**. Appendix F "Interim Value of Shield
  Options" carries the complete Fixed Income Asset Proxy / Derivative Asset Proxy algebra,
  the per-crediting-type replicating option portfolios, and the worked proportional
  Investment Amount reduction on withdrawal.

### S3. Pruco Life Insurance Company — "PRUDENTIAL FlexGuard — Flexible Premium Deferred Index-Linked and Variable Annuity ('B Series')", prospectus supplement
- Publisher: Pruco Life Insurance Company (Prudential)
- Doc type: prospectus supplement dated September 14, 2022 to the prospectus dated
  August 15, 2022, containing full amended-and-restated text of the index-strategy
  sections, the Interim Value discussion, and Appendix B (57 pages)
- URL fetched: https://www.prudential.com/content/dam/us/sites/pru-com/pru/opt2/annuities/annuity-prospectuses/S3-flex-guard-prosp-B-plaz.pdf
- Retrieved: YES (full PDF text extracted and read)
- Product: Prudential FlexGuard indexed variable annuity, B Series — a *combination*
  contract offering index strategies alongside variable investment subaccounts.
- Caveat carried over: this is a 2022 supplement, not the current prospectus. Numbers are
  as of that document; **do not treat as current pricing.** FlexGuard has since been
  re-registered on Form N-4 under the 2024 rule [R1], so strategy menus, buffers and rates
  will have changed.

### S4. Equitable Financial Life Insurance Company — "Structured Capital Strategies PLUS 26", Form N-4 registration statement
- Publisher: Equitable Financial Life Insurance Company, CIK 0002039145 (a parallel,
  essentially identical filing exists for Equitable Financial Life Insurance Company of
  America, CIK 0002038891)
- Doc type: Form N-4 registration statement (the post-2024 RILA form), filed 2026-06-18,
  accession 0001193125-26-275133
- URL fetched: https://www.sec.gov/Archives/edgar/data/2039145/000119312526275133/d59590dn4.htm
- Retrieved: YES (full document downloaded and read)
- Product: Structured Capital Strategies PLUS (SCS PLUS 26) — index-linked annuity with a
  Structured Investment Option (SIO) of "Segments" plus a Guaranteed Interest Option
  (GIO). Non-unitized Separate Account No. 68 (NY) / 68A and 68E (AZ).
- Role in this library: the richest **segment-type menu** publicly documented (Standard,
  Annual Lock, Step Up, Dual Direction, Dual Step Up, Optimal Mix) with the exact Segment
  Rate of Return decision table for each, and the most detailed **Segment Interim Value**
  description including the Cap Calculation Factor and the implied-volatility
  interpolation procedure.

### S5. Allianz Life Insurance Company of North America / Allianz Life Variable Account B — "Allianz Index Advantage+ Select Income Annuity", Form N-4 initial registration statement
- Publisher: Allianz Life Insurance Company of North America (CIK 0000072499) / Allianz
  Life Variable Account B (CIK 0000836346)
- Doc type: Form N-4 initial registration statement, filed 2025-07-22, accession
  0000836346-25-000047
- URL fetched: https://www.sec.gov/Archives/edgar/data/836346/000083634625000047/iaplusselectincomn4july2025.htm
- Retrieved: YES (full document downloaded and read)
- Product: Allianz Index Advantage+ Select Income Annuity.
- Role in this library: the structurally different presentation — a **"Daily Adjustment"**
  applied to an "Index Option Base" rather than a self-contained interim value — and the
  only retrieved source offering both **buffer** and **floor** crediting side by side
  (Index Guard Strategy = −10% Floor). Appendix C gives the Proxy Value formula for each
  of six crediting methods.
- Caveat carried over: this is an *initial* N-4 filing; several fee-table cells are marked
  "[To be updated by amendment]" and the prospectus date is "[December XX, 2025]". **Fee
  figures from this document are preliminary** and should be re-verified against the
  effective prospectus.

### S6. Lincoln Life & Annuity Company of New York — "Lincoln Level Advantage 2 B-Share Index-Linked Annuity", Form N-4/A
- Publisher: Lincoln Life & Annuity Company of New York, CIK 0001022095
- Doc type: Form N-4/A (pre-effective amendment), filed 2026-04-16, accession
  0001104659-26-044336. Includes the SAI text with the Interim Value appendix and worked
  examples.
- URL fetched: https://www.sec.gov/Archives/edgar/data/1022095/000110465926044336/tm265270d1_n4a.htm
- Retrieved: YES (full document downloaded and read)
- Product: Lincoln Level Advantage 2 B-Share (and Advisory) Index-Linked Annuity Contracts.
- Role in this library: a **third algebraic form of the fixed income asset proxy** and a
  full grid of **worked Interim Value numeric examples** across index moves of
  −30%/−10%/+20%/+40% for 1-year and 6-year terms and for cap, trigger and dual-trigger
  accounts — the best available regression test vectors.

### Failed / blocked retrievals (carried over; **not** sources, and nothing is cited from them)
- Brighthouse "Understanding Interim Value" educational PDF —
  https://www.brighthousefinancial.com/content/dam/brighthouse-financial/public/pdfs/shield/Shield-Interim-Value-Educational-Resource.pdf
  — HTTP 403. fetched_ok = false.
- Brighthouse Shield current rate page —
  https://www.brighthousefinancial.com/products/annuities/shield-annuities/shield-rates/
  — HTTP 403. fetched_ok = false. **No current declared cap/step/edge rates captured** —
  this is why every declared-rate value in `product-spec.md` is **[std]**.
- Equitable performance cap rate page —
  https://equitable.com/annuities/variable-annuities/performance-cap-rates
  — request rejected by WAF. fetched_ok = false.
- Federal Register HTML of the RILA adopting release — redirects off-host to
  unblock.federalregister.gov. fetched_ok = false; the SEC PDF (R1) was used instead and
  is authoritative.

---

## Regulatory and actuarial references [R#] (product research file numbering)

These are the local R-numbers used inside
`us/_research/registered-index-linked-annuity.md`. They are **independent of** the shared
[REG-R#] space; several documents appear in both (noted per entry).

### R1. U.S. Securities and Exchange Commission — Final rule, "Registration for Index-Linked Annuities and Registered Market Value Adjustment Annuities; Amendments to Form N-4 …; Other Technical Amendments"
- Publisher: SEC
- Release Nos. 33-11294; 34-100450; IC-35273; File No. S7-16-23; RIN 3235-AN30. 17 CFR
  Parts 230, 232, 239, 274. 467 pages (conformed to Federal Register version).
- URL fetched: https://www.sec.gov/files/rules/final/2024/33-11294.pdf
- Retrieved: YES (full PDF; introduction and effective/compliance-date sections read in
  detail)
- Cross-reference: the same rulemaking is catalogued at **[REG-R49]**, which was fetched
  via govinfo.gov (89 Fed. Reg. 59978) because sec.gov returned HTTP 403 there, and which
  flags the **May 1, 2026 compliance date as [unverified]** (section II.J not read).
  Both documents in this directory carry that [unverified] flag.

### R2. NAIC — Actuarial Guideline LIV, "Nonforfeiture Requirements for Index-Linked Variable Annuity Products" (AG 54)
- Publisher: National Association of Insurance Commissioners
- Doc type: adopted actuarial guideline plus project history (6 pages)
- URL fetched: https://content.naic.org/sites/default/files/committees-pending-action-actuarial-guideline-liv-230224.pdf
- Retrieved: YES (full text read)
- Adoption trail printed on the document: adopted by Life Actuarial (A) Task Force
  12/11/2022; adopted by Life Insurance and Annuities (A) Committee 2/24/2023. NAIC
  Executive (EX) Committee and Plenary adoption is **[unverified]** — not stamped on the
  retrieved document. The July 1, 2024 effective date **is** stated in the retrieved text.
- Cross-reference: the same guideline is **[REG-R44]**.

### R3. NAIC — Valuation Manual, Jan. 1, 2026 edition, VM-21 "Requirements for Principle-Based Reserves for Variable Annuities"
- Publisher: NAIC
- URL fetched: https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf
- Retrieved: YES (457 pages; VM-21 Sections 1 and 2 read in detail)
- Cross-reference: **[REG-R35]** (VM-21 as a section) and **[REG-R3]** (the parent
  Valuation Manual).

### R4. NAIC — Model #250, "Variable Annuity Model Regulation"
- Publisher: NAIC (October 2007 edition of the NAIC Model Laws compilation)
- URL fetched: https://content.naic.org/sites/default/files/model-law-250.pdf
- Retrieved: YES (13 pages; Sections 2, 3 and 7 read)
- Cross-reference: **[REG-R43]**. Note the model-number correction recorded there and in
  `product-spec.md`: **#250 is the Variable Annuity Model Regulation; the Annuity
  Disclosure Model Regulation is #245** ([REG-R45]).

### R5. Actuarial Standards Board — ASOP No. 2, "Nonguaranteed Elements for Life Insurance and Annuity Products" (Doc. No. 204)
- Publisher: Actuarial Standards Board
- URL fetched: http://www.actuarialstandardsboard.org/wp-content/uploads/2021/12/asop002_204-2.pdf
- Retrieved: YES (33 pages; Sections 1 and 2 read)
- Note carried over: the title has changed from the older "Nonguaranteed Charges or
  Benefits for Life Insurance Policies and Annuity Contracts".
- Cross-reference: **[REG-R26]**.

### R6. American Academy of Actuaries — "Index-Linked Variable Annuity (ILVA) / Registered Index-Linked Annuity (RILA)" policy paper
- Publisher: American Academy of Actuaries, Life Practice Council
- Doc type: policy paper, 26 pages, dated December 2025 (file name Life-PolicyPaper120225.pdf)
- URL fetched: https://actuary.org/wp-content/uploads/2025/12/Life-PolicyPaper120225.pdf
- Retrieved: YES (full PDF text extracted and read)
- Role in this library: the **fully worked numeric hypothetical-portfolio interim value
  example** (6-year, 10% buffer, Black-Scholes inputs disclosed), the survey of common
  ILVA product features used to calibrate the composite, and the open-source Excel Lambda
  library reproducing the AG 54 calculation.
- Cross-reference: **[REG-R69]**.
- Caveat carried over: the Interstate Compact standard IIPRC-03-I-ILVA is quoted **only
  second-hand** through this paper; the Compact standard itself was not retrieved
  [unverified].

---

## Cross-product regulatory references [REG-R#]

[REG-R#] tags resolve against the **single shared numbering space R1–R72** curated at
`us/references/regulatory-and-actuarial-references.md`. It is one space in two halves:

- **R1–R34** — life-origin entries, several of which also bind annuity models. Research
  provenance: `us/_research/regulatory-actuarial.md`. Access date **2026-08-03**.
- **R35–R72** — annuity-specific entries. Research provenance:
  `us/_research/regulatory-actuarial-annuities.md`, which also carries the table of which
  R1–R34 entries bind annuity models. Access date **2026-08-04**.

Entries cited by the two documents in this directory:

| Tag | Half | Short title | Retrieval status (per the research files) |
|---|---|---|---|
| REG-R15 | R1–R34 | 26 U.S.C. §817 (esp. §817(h) diversification) | fetched |
| REG-R16 | R1–R34 | 26 U.S.C. §807 — tax reserves | fetched |
| REG-R26 | R1–R34 | ASOP No. 2 — Nonguaranteed Elements (same standard as [R5] above) | fetched |
| REG-R27 | R1–R34 | ASOP No. 7 — Life or Health Cash Flow Analysis (rev. Dec 2025) | fetched |
| REG-R29 | R1–R34 | ASOP No. 22 — Opinions based on asset adequacy analysis | fetched |
| REG-R31 | R1–R34 | ASOP No. 52 — PBR for **Life** Products under the Valuation Manual | fetched (cited only to record that it does **not** cover VM-21/VM-22) |
| REG-R32 | R1–R34 | ASOP No. 56 — Modeling | fetched |
| REG-R34 | R1–R34 | FASB ASU 2018-12 (LDTI; market risk benefits) | fasb.org blocked (HTTP 403); annotated from an accessible third-party full text |
| REG-R35 | R35–R72 | VM-21, Valuation Manual Jan. 1, 2026 ed. (same document as [R3] above) | yes (local text extraction; §§1–3 and TOC read) |
| REG-R38 | R35–R72 | Actuarial Guideline XLIII (AG 43), VAIWG redline | yes (local text extraction) |
| REG-R42 | R35–R72 | Standard Nonforfeiture Law for Individual Deferred Annuities (Model #805) | yes (local text extraction; §§1–8 read in full) |
| REG-R43 | R35–R72 | Variable Annuity Model Regulation (Model #250) (same document as [R4] above) | yes (local text extraction; TOC and §7 read) |
| REG-R44 | R35–R72 | Actuarial Guideline LIV (AG 54) (same document as [R2] above) | yes (local text extraction; **complete guideline read**) |
| REG-R45 | R35–R72 | Annuity Disclosure Model Regulation (Model #245) | yes (local text extraction; §§1 and 3 read) |
| REG-R46 | R35–R72 | Suitability in Annuity Transactions Model Regulation (Model #275) | yes (local text extraction; TOC and §1 read) |
| REG-R47 | R35–R72 | C-3 RBC Instructions and Appendices (C-3 Phase II) | yes (local text extraction) |
| REG-R48 | R35–R72 | Oliver Wyman QIS II public report and executive summary (VA framework reform) | yes, both (local text extraction) |
| REG-R49 | R35–R72 | SEC Release 33-11294 — RILA registration / Form N-4 (same rulemaking as [R1] above) | yes, via govinfo.gov (89 Fed. Reg. 59978); **sec.gov PDF returned HTTP 403 there**; compliance date May 1, 2026 flagged [unverified] |
| REG-R49b | R35–R72 | GAO rule report B-336553 (corroborates R49 publication metadata) | yes |
| REG-R51 | R35–R72 | 17 C.F.R. §230.498A — summary prospectuses, extended to registered non-variable annuities | yes |
| REG-R52 | R35–R72 | SEC Form N-4 | **no — sec.gov returned HTTP 403**; content described only through the adopting releases |
| REG-R53 | R35–R72 | CRS Report R40656 — SEC Rule 151A and annuities (why FIAs are not registered) | yes |
| REG-R54 | R35–R72 | FINRA Rule 2330 — deferred variable annuities | yes; **[unverified]** whether FINRA applies it to RILAs specifically |
| REG-R55 | R35–R72 | 26 U.S.C. §72 — Annuities | yes |
| REG-R56 | R35–R72 | 26 U.S.C. §1035 — exchanges | yes |
| REG-R58 | R35–R72 | T.D. 10001 — RMD final regulations (2024) | yes, via govinfo.gov |
| REG-R59 | R35–R72 | Model #821 + VM-M annuity mortality definitions (2012 IAM / IAR, Scale G2) | yes, both (local text extraction) |
| REG-R60 | R35–R72 | 2012 Individual Annuity Reserving Table — Academy/SOA Payout Annuity Table Team report (source of the 10% margin loaded into the Period / IAR table) | yes (local text extraction; margin/loading sections read) |
| REG-R61 | R35–R72 | 2020–2024 Individual Payout Annuity Mortality Experience Study | yes (landing page; full report PDF and paid data package not retrieved) |
| REG-R62 | R35–R72 | FIA policyholder behavior experience studies (2021–22, 2019–20) | yes (both landing pages); the ~10%/~33% shock-lapse split is **[unverified]** |
| REG-R63 | R35–R72 | Fixed rate deferred surrender experience studies (2023–24, 2015–22) | partial (verified via the SOA index R65); the ~52%/~56% figures are **[unverified]** |
| REG-R64 | R35–R72 | VA / RILA contract holder behavior and GLB utilization studies (2022–24) | yes (2022–24 landing page); detailed tables behind a paid data package |
| REG-R65 | R35–R72 | SOA Individual Annuity Experience Studies — index | yes (complete list read) |
| REG-R66 | R35–R72 | AAA VM-21 practice note supplement (Feb 2022) | yes (local text extraction) |
| REG-R69 | R35–R72 | AAA ILVA / RILA policy paper (same document as [R6] above; listed as the cross-reference for [R6], which is the tag actually used in the two documents) | yes (local text extraction) |
| REG-R70 | R35–R72 | ASOP No. 54 — Pricing of Life Insurance and Annuity Products | yes |
| REG-R71 | R35–R72 | ASOP No. 10 — U.S. GAAP for Long-Duration Life, Annuity, and Health Products (Doc. No. 207) | yes (local text extraction) |

Corrections carried forward from the research files and made explicit in
`product-spec.md`, rather than repeating the common misstatements:

1. **Model #805's indexed nonforfeiture rate floor is 15 basis points (0.15%), not 1%** —
   the rate is the lesser of 3% and the five-year CMT (rounded to the nearest 1/20 of one
   percent) reduced by 125 basis points, subject to that 15 bp floor [REG-R42].
2. **The Annuity Disclosure Model Regulation is #245, not #250** — #250 is the Variable
   Annuity Model Regulation, verified from both model-law prints and from AG 54's own
   citation [REG-R43][REG-R44][REG-R45].
3. **Model #805 does not apply to a RILA if and only if AG 54 is satisfied**
   [REG-R42][REG-R44].
4. **VM-21 does not automatically apply to a RILA**: §2.A.3 excludes separate-account
   contracts that guarantee an index and offer no GMDB/VAGLB [R3][REG-R35].
5. **AG 43 is not simply superseded by VM-21** — through reference in AG 43, VM-21's
   requirements reach pre-2017 contracts outside VM-21's own scope [REG-R35][REG-R38].
6. **VM-22 is not the RILA reserve standard** and, in the Jan. 1, 2026 edition, no longer
   holds the income-annuity maximum valuation interest rates (those are in VM-V §1) — see
   the VM-22 and VM-V entries in `us/_research/regulatory-actuarial-annuities.md`. Noted
   here only to prevent mis-application; neither entry is cited by the documents in this
   directory and neither is listed in the table above.

---

## Provenance note

Extraction details live in `us/_research/registered-index-linked-annuity.md`: that file
records which facts came from which source, the [unverified] flags, the per-insurer
interim-value algebra, the failed/blocked retrievals listed above, and the twelve
documented gaps — most consequentially that **no current declared rate sheet was
retrievable** (gap 1), that **annuity purchase rate tables were not found** (gap 2), that
**Trading Costs are required by AG 54 but quantified nowhere** (gap 8), and that **no
specimen contract or policy form was located for any of these products** (gap 7), so all
product facts come from prospectuses rather than from the contracts themselves. The
cross-product bibliographies `us/_research/regulatory-actuarial.md` (R1–R34) and
`us/_research/regulatory-actuarial-annuities.md` (R35–R72) play the same role for
[REG-R#] tags. Standardizations marked **[std]** in `product-spec.md` and
`technical-notes.md` — including the entire declared-rate snapshot, the trading-cost
factor, the market-data assumptions used in the worked example, and every behavioral
assumption — are introduced at drafting and are not attributable to any source.
