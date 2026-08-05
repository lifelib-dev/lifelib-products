# Sources — Single Premium Immediate Annuity (SPIA) (United States)

Source ids, titles, publishers, doc types, URLs, access dates and retrieval markers are
carried over **verbatim** from `us/_research/immediate-annuity.md` (the citation ground truth
for [S#]/[R#] tags). Ids are never renumbered. Sources in the research file that are not
cited in `product-spec.md` or `technical-notes.md` are omitted — **none were dropped: every
S1–S11 and R1–R11 entry is cited.** No new sources were fetched at drafting; nothing is
marked "added at drafting".

Access date for all citations: 2026-08-04.

---

## Primary product sources [S#]

### S1. Massachusetts Mutual Life Insurance Company — "MassMutual RetireEase — A Single Premium Immediate Annuity" (AN1500 526 / MM202905-316012)
- Publisher: Massachusetts Mutual Life Insurance Company (official document served from
  MassMutual's own `compass.massmutual.com` asset service)
- Doc type: consumer product brochure with a formal "Product Highlights" spec section
  (8 pages, © 2026)
- URL fetched: https://compass.massmutual.com/api/public/assets/file/bltd6a32711c1c02d16
- Retrieved: YES (full PDF, text layer extracted; surrender-charge chart re-extracted with
  text-position coordinates to confirm the year→rate mapping)
- Product: MassMutual RetireEase, contract form **#SPIA05; SPIA05 (NC)**
- Role in this library: design anchor — issue ages and age basis, premium limits, the full
  joint-life option inventory with both reduction triggers, the 1–4% Inflation Protector
  COLA, and the **only published SPIA surrender-charge schedule** located in this research.

### S2. Pacific Life Insurance Company — "Pacific Income Provider — A Single-Premium, Immediate Fixed Annuity" fact sheet (FAC0719-00 11/25, item 25-555)
- Publisher: Pacific Life Insurance Company (official; `annuities.pacificlife.com`)
- Doc type: product fact sheet / spec sheet (4 pages)
- URL fetched: https://www.annuities.pacificlife.com/content/dam/paclife/rsd/annuities/public/pdfs/fact-sheets/pacific-income-provider-fact-sheet.pdf
- Retrieved: YES (full PDF read)
- Product: **Pacific Income Provider**, contract form series **ICC10:30-1181, 30-1181OR**
- Role in this library: design anchor — the cleanest published statement of the
  reduce-on-either-death versus reduce-on-primary-death distinction.

### S3. Pacific Life Insurance Company — "Pacific Income Provider — A Single-Premium, Immediate Fixed Annuity" client guide (FAC0718-0224)
- Publisher: Pacific Life Insurance Company (official; `pacificlife.com`)
- Doc type: consumer client guide (16 pages, Feb 2024 version)
- URL fetched: https://www.pacificlife.com/content/dam/paclife/rsd/annuities/public/pdfs/guide/pacific-income-provider-client-guide.pdf
- Retrieved: YES (full PDF read)
- Role: narrative confirmation of the joint-life trigger distinction; the cash-refund
  definition; and the only insurer hypothetical income illustrations located (explicitly
  "For illustrative purposes only").

### S4. Integrity Life Insurance Company / National Integrity Life Insurance Company (Western & Southern Financial Group) — "IncomeSource® Series Product Summary" (CF-51-0075-2406)
- Publisher: Western & Southern Financial Group (official; `westernsouthern.com`)
- Doc type: distributor/producer product summary (2 pages)
- URL fetched: https://www.westernsouthern.com/-/media/files/distributors/toolkits/incomesource-product-summary.pdf
- Retrieved: YES (full PDF read)
- Product: **IncomeSource** SPIA, contract series **ICC16 ENT-01 1701** / **ENT-01 1701 NY**;
  Deceased Commutation Rider **ICC09 ER.02 0901**; Living Commutation Rider **ICC09 ER.01
  0901**

### S5. New York Life Insurance and Annuity Corporation (NYLIAC) — "Just the facts about the New York Life Guaranteed Lifetime Income Annuity II" (1222A.1125 / ML25-006013 / SMRU5817113, exp. 06.27.2028)
- Publisher: New York Life (official; `nylannuities.com`)
- Doc type: client fact sheet / spec sheet (5 pages)
- URL fetched: https://www.nylannuities.com/connectedassets/final-assets/marketing-materials/fact-sheet-products/TPD_Client_FactSheet_GLI_II_Generic.pdf
- Retrieved: YES via direct HTTP with a browser user-agent. (Note: the same URL returned
  **HTTP 403** through the WebFetch tool; recorded as a tool-specific failure, not a dead
  link.)
- Product: **New York Life Guaranteed Lifetime Income Annuity II**, policy form
  **ICC11-P103** (may be **211-P103**)

### S6. Nationwide Life Insurance Company — "INCOME Promise® — A Single-premium Immediate Fixed Annuity" (NFS-0133-C (05/04))
- Publisher: Nationwide Life Insurance Company (PDF hosted on Nationwide's
  retirement-plans site `nrsforu.com`)
- Doc type: consumer brochure with a spec page (8 pages)
- URL fetched: https://www.nrsforu.com/BOA/media/pdf/NFS-0133.pdf
- Retrieved: YES (full PDF read). **Caveat carried over: this is a 2004-vintage document**
  (contracts APO-4834, APO-4834-37, APO-4834-43; Oklahoma APO-4834-36) — retained because it
  documents an older but very typical SPIA option set and terminology.

### S7. TIAA-CREF Life Insurance Company — "Single Premium Immediate Annuities" prospectus (Rule 497(c) filing, Registration No. 333-46414, dated May 1, 2008)
- Publisher: TIAA-CREF Life Insurance Company, filed with the SEC
- Doc type: **registered product prospectus** (SEC EDGAR)
- URL fetched: https://www.sec.gov/Archives/edgar/data/1067490/000119312508102441/d497.htm
- Retrieved: YES (full HTML, 256 KB of text). **Caveats carried over: 2008 filing**, used for
  its contractual precision on immediate-annuity mechanics, not as a currently-sold product
  spec; and these are single premium immediate **variable** annuity contracts with a
  fixed-account option, **not a pure fixed SPIA**.

### S8. Mutual of Omaha / United of Omaha Life Insurance Company — producer product overview (form 135880, updated 9-17)
- Publisher: Mutual of Omaha Insurance Company (official producer site)
- Doc type: producer portfolio overview (16 pages); **for producer use only**
- URL fetched: https://producer.mutualofomaha.com/enterprise/wcm/connect/14033a75-36a8-4542-b987-a96fa72cc5b3/135880.pdf?MOD=AJPERES&ContentCache=NONE
- Retrieved: YES (full PDF read). **Caveat carried over: dated 9-2017**; the current
  Ultra-Income brochure 404s and the product page host does not resolve, so the 6% COLA and
  "age rating" facts should be re-verified before being relied on.

### S9. LifeAnnuities.us — "Best SPIA Rates — July 2026: Top Payouts by Age"
- Publisher: LifeAnnuities.us (**commercial annuity-quote / lead-generation site — NOT an
  insurer, regulator, or actuarial body**)
- Doc type: rate-survey web page
- URL fetched: https://lifeannuities.us/rates/best-spia-rates/
- Retrieved: YES (HTML)
- **Reliability: LOW.** Carried over verbatim: recorded solely as a rate anchor of last
  resort because no insurer- or regulator-published payout-rate table could be retrieved.
  Numbers are indicative order-of-magnitude only and **must not be used as authoritative
  pricing**.

### S10. New York Life — "Annuity rates" page (weekly payout-rate publication)
- Publisher: New York Life (official; `nylannuities.com`)
- Doc type: rates web page
- URL fetched: https://www.nylannuities.com/resources/rates
- Retrieved: **PARTIAL** — page HTML retrieved successfully, but the rate tables are loaded
  client-side via JavaScript and rendered as "Loading…" in the static HTML, so **no numeric
  rates could be extracted**. Only the methodology text is cited.

### S11. The Guardian Life Insurance Company of America — "Single Premium Immediate Annuity (SPIA)" educational page (last updated January 29, 2026)
- Publisher: Guardian Life (official; `guardianlife.com`)
- Doc type: consumer education page (not a product spec sheet)
- URL fetched: https://www.guardianlife.com/annuities/income/single-premium-immediate-spia
- Retrieved: YES (HTML). Low specification content; cited only for the market-size datapoint,
  the timing framing, the premium/annuity-tax note, the 10%-penalty note and the mention of
  participating (dividend-paying) SPIA designs.

### Failed / unusable fetches (carried over for completeness; contents NOT used)

- `https://www.immediateannuities.com/annuity-brochures/massmutual-retireease.pdf` — **HTTP 403**.
- `https://www.immediateannuities.com/annuity-rates/by-age.html` — **HTTP 403** (both WebFetch and direct HTTP).
- `https://legacy.mutualofomaha.com/documents/annuities/lc3146.pdf` (Ultra-Income brochure) — **HTTP 404**.
- `https://webprod3.mutualofomaha.com/annuities/plan-details/ultra-income.php` — **DNS resolution failure**.
- `https://communications.fidelity.com/fili/spia/nyl/docs/new_york_life_lifetime_spia_factsheet.pdf` — HTTP 200 but the PDF has **no extractable text layer** (image-only); no facts taken.
- `https://communications.fidelity.com/fili/docs/ws-spia-factsheet.pdf` — returned a **230-byte stub**, not the document.
- `https://www.nylannuities.com/connectedassets/.../TPD_Client_FactSheet_GLI_II_Generic.pdf` via **WebFetch** — HTTP 403 (succeeded via direct HTTP; see S5).

---

## Regulatory and actuarial references [R#] (product research file numbering)

These [R#] ids are **product-local** to `us/_research/immediate-annuity.md` and are
independent of the cross-product [REG-R#] space below.

### R1. NAIC — *Valuation Manual*, Jan. 1, 2026 Edition, **VM-V: Statutory Maximum Valuation Interest Rates for Formulaic Reserves**, Section 1 "Income Annuities"
- Publisher: National Association of Insurance Commissioners
- URL fetched: https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf
- Retrieved: YES (457-page PDF; VM-V Section 1 at PDF pages 447–457)
- Note carried over: the maximum-valuation-interest-rate machinery for income annuities
  historically labelled VM-22 now sits in **VM-V**; VM-22 has been redefined as the
  principle-based reserve framework for non-variable annuities (R2).

### R2. NAIC — *Valuation Manual*, Jan. 1, 2026 Edition, **VM-22: Requirements for Principle-Based Reserves for Non-Variable Annuities**, and Section II "Reserve Requirements" Subsection 2
- Publisher: NAIC. Same URL as R1 (PDF pages 5, 16–21, 227–318)
- Retrieved: YES
- Contains the Payout Annuity Reserving Category definition, the prescribed Standard
  Projection mortality formula and **Table 6.8** (payout-annuity `F_x` factors, reproduced in
  full in the research file), and the age-basis conversion formula.

### R3. NAIC — *Valuation Manual*, Jan. 1, 2026 Edition, **VM-M Appendix M — Mortality Tables**, §1.J (2012 IAR) and §2.C (2012 IAM Basic)
- Publisher: NAIC. Same URL as R1 (PDF pages 445–446)
- Retrieved: YES
- Source of the generational application formula, the three-decimals-per-1,000 rounding rule
  and its worked example, and the definition of the 2012 IAM Basic table.

### R4. NAIC — **Model #821**, *Model Rule (Regulation) for Recognizing a New Annuity Mortality Table for Use in Determining Reserve Liabilities for Annuities* (January 2013 publication; recommended effective date 1/1/2014)
- Publisher: NAIC
- URL fetched: https://content.naic.org/sites/default/files/model-law-821.pdf
- Retrieved: YES (5 pages)

### R5. NAIC — **Model #805**, *Standard Nonforfeiture Law for Individual Deferred Annuities* (Fall 2020 publication)
- Publisher: NAIC
- URL fetched: https://content.naic.org/sites/default/files/model-law-805.pdf
- Retrieved: YES (5 pages)
- Carries the **verified** §2.A finding that immediate annuities are exempt.

### R6. **26 U.S.C. § 72** — Annuities; certain proceeds of endowment and life insurance contracts
- Publisher: Legal Information Institute, Cornell Law School (mirror of the U.S. Code)
- URL fetched: https://www.law.cornell.edu/uscode/text/26/72
- Retrieved: YES (via WebFetch)

### R7. IRS — **Publication 939, *General Rule for Pensions and Annuities*** (Rev. 12-2025)
- Publisher: Internal Revenue Service
- URL fetched: https://www.irs.gov/pub/irs-pdf/p939.pdf
- Retrieved: YES (85 pages)
- Source of the exclusion-ratio computation steps, the age-nearest convention, the
  expected-return rules by payout form, and the refund-feature adjustment worked example.

### R8. **Treas. Reg. § 1.401(a)(9)-6** — Required minimum distributions for defined benefit plans and annuity contracts
- Publisher: Legal Information Institute, Cornell Law School (mirror of 26 CFR)
- URL fetched: https://www.law.cornell.edu/cfr/text/26/1.401%28a%29%289%29-6
- Retrieved: YES (via WebFetch)

### R9. SOA Research Institute & LIMRA — **2020-2024 Individual Payout Annuity Mortality Experience Study** (study highlights, © 2026)
- Publisher: Society of Actuaries Research Institute (Individual Annuity Experience
  Committee) with LIMRA
- URL fetched: https://www.soa.org/globalassets/assets/files/resources/research-report/2026/2020-24-payout-annuity-exp-study.pdf
- Retrieved: YES (5-page public "Study Highlights"; the detailed report and dashboards are
  behind the paid Experience Studies Pro package — **not retrieved**)

### R10. **26 U.S.C. § 130** — Certain personal injury liability assignments (structured settlements)
- Publisher: Legal Information Institute, Cornell Law School
- URL fetched: https://www.law.cornell.edu/uscode/text/26/130
- Retrieved: YES (via WebFetch)
- Cited only to distinguish structured settlements (no commutation permissible at all) from
  the retail SPIA in scope here.

### R11. Wisconsin Office of the Commissioner of Insurance — **PI-214, *Consumer's Guide to Understanding Annuities*** (R 09/2025)
- Publisher: State of Wisconsin OCI
- URL fetched: https://oci.wi.gov/Documents/Consumers/PI-214.pdf
- Retrieved: YES
- Cited only for the regulator's plain-language framing of the income-start window.

---

## Cross-product regulatory references [REG-R#]

Cited with the [REG-R#] prefix to avoid collision with the product research file's own
R-numbering above. The curated library is
`us/references/regulatory-and-actuarial-references.md`. **[REG-R#] is one shared numbering
space running R1–R157**, with **R114–R124** and **R143–R149** permanently **unused by
design** — block gaps left so three parallel research streams could number independently,
not losses, and they must not be back-filled. Entries **R1–R34** originate in
`us/_research/regulatory-actuarial.md` (the life-origin bibliography, several of whose
entries also bind annuity models); entries **R35–R72** in
`us/_research/regulatory-actuarial-annuities.md` (the annuity-specific continuation, which
opens at R35 and explicitly freezes R1–R34); and entries **R73–R142** in the three statutory
accounting and capital research files (`us/_research/statutory-accounting.md` R73–R99,
`us/_research/statutory-reserves.md` R100–R113, `us/_research/risk-based-capital.md`
R125–R142), whose per-entry bibliography is `us/regulatory/sources.md`. Entries cited by the
two documents in this directory:

| Tag | Half | Short title | Retrieval status (per the research file) |
|---|---|---|---|
| REG-R1 | R1–R34 | Standard Valuation Law (Model #820) | fetched |
| REG-R3 | R1–R34 | NAIC Valuation Manual, Jan. 1, 2026 edition (parent document) | fetched |
| REG-R16 | R1–R34 | 26 U.S.C. §807 — tax reserves | fetched |
| REG-R27 | R1–R34 | ASOP No. 7 — Life or Health Cash Flow Analysis | fetched |
| REG-R29 | R1–R34 | ASOP No. 22 — opinions based on asset adequacy analysis | fetched |
| REG-R31 | R1–R34 | ASOP No. 52 — PBR for **Life** Products under the Valuation Manual (cited for its *non*-applicability to annuities) | fetched |
| REG-R32 | R1–R34 | ASOP No. 56 — Modeling | fetched |
| REG-R33 | R1–R34 | NAIC AP&P Manual (Appendix A-821 holds the 2012 IAM / Scale G2 tables) | fetched |
| REG-R34 | R1–R34 | FASB ASU 2018-12 (LDTI) | fetched |
| REG-R36 | R35–R72 | VM-22: PBR for Non-Variable Annuities (Valuation Manual, 2026 ed.) | yes (local text extraction) |
| REG-R37 | R35–R72 | VM-V §1 — Income Annuities (Valuation Manual, 2026 ed.) | yes (local text extraction) |
| REG-R41 | R35–R72 | VM-C Appendix C — index of incorporated actuarial guidelines (AG IX, IX-A, IX-B, IX-C) | yes (local text extraction) |
| REG-R42 | R35–R72 | Standard Nonforfeiture Law for Individual Deferred Annuities (Model #805) — same document as [R5] above | yes (local text extraction) |
| REG-R43 | R35–R72 | Variable Annuity Model Regulation (Model #250) — §7.A immediate-annuity exclusion | yes (local text extraction) |
| REG-R45 | R35–R72 | Annuity Disclosure Model Regulation (Model **#245**) | yes (local text extraction) |
| REG-R46 | R35–R72 | Suitability in Annuity Transactions Model Regulation (Model #275) | yes (local text extraction) |
| REG-R55 | R35–R72 | 26 U.S.C. §72 (same statute as [R6] above) | yes |
| REG-R56 | R35–R72 | 26 U.S.C. §1035 — exchanges | yes |
| REG-R57 | R35–R72 | 26 C.F.R. §1.401(a)(9)-6 (same regulation as [R8] above) | yes |
| REG-R58 | R35–R72 | RMD Final Regulations (T.D. 10001) | yes (govinfo) |
| REG-R59 | R35–R72 | Model #821 + VM-M annuity mortality definitions (same documents as [R3][R4] above) | yes (local text extraction, both) |
| REG-R60 | R35–R72 | 2012 IAR development report (AAA/SOA Payout Annuity Table Team, Sept 2011) | yes (local text extraction) |
| REG-R61 | R35–R72 | 2020–2024 Individual Payout Annuity Mortality Experience Study (landing page; the highlights PDF is [R9] above) | yes (landing page) |
| REG-R70 | R35–R72 | ASOP No. 54 — Pricing of Life Insurance and Annuity Products | yes |
| REG-R71 | R35–R72 | ASOP No. 10 — U.S. GAAP for Long-Duration Life, Annuity and Health Products (Doc. No. 207) | yes (local text extraction) |

Verified at drafting: the curated page `us/references/regulatory-and-actuarial-references.md`
carries all **139** entries of the R1–R157 numbering (R114–R124 and R143–R149 being unused by
design), so every [REG-R#] tag above and below resolves there. The "Half" column records which
research file each entry's annotation originates in, because the halves were compiled
separately and R1–R34 are frozen against renumbering.

### Entries added at this pass — statutory accounting and capital

Cited by the `## Statutory accounting and capital` section of `technical-notes.md` and by the
statutory paragraph of `product-spec.md`. Id, title, publisher, URL, access date and
fetched marker are carried **verbatim** from `us/regulatory/sources.md` (which in turn carries
them verbatim from the three research files). **Ids are never renumbered.** One frozen R1–R72
entry — **R39** — appears here because it had not previously been cited by this directory.
Access date for every entry below: **2026-08-04**.

#### REG-R39. Actuarial Guideline XXXIII — Determining CARVM Reserves for Annuity Contracts With Elective Benefits (AG 33)
- **Publisher:** NAIC
- **URL:** none — **no free official standalone text was located.** Title and current status
  verified from the Valuation Manual's VM-C index (page C-1) [REG-R41]; the authoritative text
  is in the **AP&P Manual Appendix C**.
- **Accessed:** 2026-08-04 (search date; guideline text not retrieved)
- **Fetched:** **no.** No AG 33 mechanic is quoted anywhere in this library, and every
  document that touches it says so at the point of use.

#### REG-R74. AP&P Manual **Preamble** — Statutory Accounting Principles Statement of Concepts and Statutory Hierarchy (*As of March 2026*)
- **Publisher:** NAIC (Preamble, pages P-1 to P-10 of the *As of March 2026* AP&P Manual)
- **URL:** https://content.naic.org/sites/default/files/publication-app-manual.pdf (Preamble section)
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; §§27–42 read in full)

#### REG-R75. SSAP No. 71 — Policy Acquisition Costs and Commissions (*As of March 2026*)
- **Publisher:** NAIC (statement pages 71-1 to 71-3)
- **URL:** https://content.naic.org/sites/default/files/publication-app-manual.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; ¶¶1–7 read in full)

#### REG-R78. SSAP No. 50 — Classifications of Insurance or Managed Care Contracts (*As of March 2026*)
- **Publisher:** NAIC (statement pages 50-1 onward)
- **URL:** https://content.naic.org/sites/default/files/publication-app-manual.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; ¶¶1–20 read)

#### REG-R79. SSAP No. 51 — Life Contracts (*As of March 2026*; historically cited as SSAP No. 51R)
- **Publisher:** NAIC (statement pages 51-1 to 51-13)
- **URL:** https://content.naic.org/sites/default/files/publication-app-manual.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; status block, ¶¶1–16 read; section index read)
- **Limit carried forward:** ¶¶17 onward (mean/mid-terminal reserves, dividends, coupons,
  accelerated benefits, disclosures) were read through the **section index and the parallel
  Issue Paper No. 51 text**, not the SSAP paragraphs.

#### REG-R80. SSAP No. 52 — Deposit-Type Contracts (*As of March 2026*)
- **Publisher:** NAIC (statement pages 52-1 to 52-8)
- **URL:** https://content.naic.org/sites/default/files/publication-app-manual.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; ¶¶1–17 read in full)

#### REG-R86. Statutory Issue Paper No. 7 — Asset Valuation Reserve and Interest Maintenance Reserve
- **Publisher:** NAIC (finalized March 16, 1998; AP&P Appendix E)
- **URL:** https://content.naic.org/sites/default/files/inline-files/007_G.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; 12 pages, read in full)
- **Vintage caution carried forward:** the AVR/IMR instruction text quoted in this issue paper
  is **1990s vintage**; the current factors, groupings and rules are at REG-R89 and differ in
  detail.

#### REG-R87. INT 23-01 — Net Negative (Disallowed) Interest Maintenance Reserve (revised print, adopted August 11, 2025)
- **Publisher:** NAIC Statutory Accounting Principles (E) Working Group (AP&P Appendix B)
- **URL:** https://content.naic.org/sites/default/files/inline-files/22-19%20-%20INT%2023-01%20-%20Revised%20April%202025.pdf
  (original clean adoption print, August 13, 2023:
  https://content.naic.org/sites/default/files/inline-files/22-19a%20-%20INT%2023-01%20-%20IMR%20clean.pdf — also fetched)
- **Accessed:** 2026-08-04
- **Fetched:** yes, both (local text extraction; 8 pages each)

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
  **IMR grouped-amortisation factor tables**. No value for either is stated anywhere.
- **Reporting-year caution:** this is the **2025** reporting year; every page and line
  reference should be re-verified against the 2026 blank before being hard-coded.

#### REG-R90. NAIC Annual Statement Blank — Life, Accident & Health/Fraternal, 2025
- **Publisher:** NAIC (free download)
- **URL:** https://content.naic.org/sites/default/files/publication-asb-life.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; 211 pages; Liabilities page, Summary of Operations
  p. 13, Cash Flow p. 14, Analysis of Operations by LOB pp. 15–20, Analysis of Increase in
  Reserves pp. 21–24, Exhibits 5–7 pp. 29–32, Exhibit of Life Insurance pp. 52–53, IMR form
  p. 55, AVR forms pp. 56–63 read)

#### REG-R92. SSAP No. 61 — Life, Deposit-Type and Accident and Health Reinsurance (*As of March 2026*; historically 61R)
- **Publisher:** NAIC (statement pages 61-1 to 61-29 plus glossary)
- **URL:** https://content.naic.org/sites/default/files/publication-app-manual.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; ¶¶1–20, 36–38, 54–59 read; full section index read)
- **Limit carried forward:** **Appendix A-791** was **not read**, only cited through this entry.

#### REG-R97. SSAP No. 101 — Income Taxes (*As of March 2026*)
- **Publisher:** NAIC (statement pages 101-1 onward, with Exhibit A Q&A)
- **URL:** https://content.naic.org/sites/default/files/publication-app-manual.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; status block, ¶¶1–2 and the full admissibility
  section ¶¶11–12 including all three Realization Threshold Limitation Tables read)

#### REG-R100. VM-30: Actuarial Opinion and Memorandum Requirements (Valuation Manual, Jan. 1, 2026 Edition)
- **Publisher:** NAIC
- **URL:** https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf
  (pages 30-1 to 30-15 of the 457-page PDF; same document as [REG-R3])
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; **Sections 1, 2 and 3 read in full**, including the
  prescribed opinion wording and the Regulatory Asset Adequacy Issues Summary contents)

#### REG-R103. Actuarial Guideline LV — Application of the Valuation Manual for Testing the Adequacy of Reserves Related to Certain Life Reinsurance Treaties (AG 55)
- **Publisher:** NAIC (print: "Adopted by Life Insurance and Annuities (A) Committee –
  July 14, 2025 / Adopted by Life Actuarial (A) Task Force – June 5, 2025"; © 2025; 14 pages)
- **URL:** https://content.naic.org/sites/default/files/committees-pending-action-aglv.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; **entire guideline read, Sections 1–9 and Appendix 1**)
- **[unverified] carried forward:** adoption by the NAIC **Executive (EX) Committee and Plenary
  on August 13, 2025** — consistently reported by law firms and consultants, but no NAIC
  document stating that date was retrieved. The **effective** date (reserves reported in the
  December 31, 2025 annual statement) **is** printed in the guideline and is verified.

#### REG-R105. Actuarial Guideline LIII — Application of the Valuation Manual for Testing the Adequacy of Life Insurer Reserves (AG 53)
- **Publisher:** NAIC (print paginated "AG53-1" to "AG53-8" and headed "Appendix C")
- **URL:** https://content.naic.org/sites/default/files/inline-files/AG%2053.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; **entire guideline read, Sections 1–6 and Appendix I**)

#### REG-R108. VM-31: PBR Actuarial Report Requirements for Business Subject to a Principle-Based Valuation (Valuation Manual, Jan. 1, 2026 Edition)
- **Publisher:** NAIC
- **URL:** https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf
  (pages 31-1 to 31-46; same document as [REG-R3])
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; Sections 1, 2, 3.A, 3.B, 3.C and 3.D.1–3.D.3 read)

#### REG-R109. VM-G: Appendix G — Corporate Governance Guidance for Principle-Based Reserves (Valuation Manual, Jan. 1, 2026 Edition)
- **Publisher:** NAIC
- **URL:** https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf
  (pages G-1 to G-6; same document as [REG-R3])
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; **Sections 1–4 read in full**)

#### REG-R110. VM-A: Appendix A — Requirements (Valuation Manual, Jan. 1, 2026 Edition)
- **Publisher:** NAIC
- **URL:** https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf
  (pages A-1 to A-2; same document as [REG-R3])
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; the complete two-page index read)
- **Limit carried forward:** VM-A is an **index, not a text**. The requirements it indexes —
  above all **A-820** and **A-830** — live in AP&P Appendix A and **were not retrieved**.

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
- **Paid-publication limit, stated plainly:** this document is *sold* by the NAIC and marked
  "Not for Distribution" on every page. Anyone rebuilding this work should **buy the current
  edition** rather than rely on a state posting. The **RBC forecasting spreadsheet** was never
  obtained and is not cited.

#### REG-R129. NAIC *Risk-Based Capital Forecasting and Instructions — 2023, Life / Fraternal*
- **Publisher:** NAIC (paid publication; copy posted by the Indiana Department of Insurance)
- **URL:** https://www.in.gov/idoi/files/indrbclf23.pdf
- **Accessed:** 2026-08-04 · **Fetched:** yes (local text extraction; 225 pages; used for
  targeted comparison only)
- **Fetch failure recorded:** the **2025 edition** at
  `https://www.in.gov/idoi/files/RBCL25-INpdf.pdf` returned a truncated PDF stream and could
  **not** be parsed. **No year-end 2025 factor is asserted anywhere.**

#### REG-R135. *Phase I Report of the American Academy of Actuaries' C-3 Subgroup of the Life Risk Based Capital Task Force to the NAIC's Risk Based Capital Work Group* (October 1999, Atlanta)
- **Publisher:** American Academy of Actuaries
- **URL:** https://www.actuary.org/wp-content/uploads/2025/05/c3_oct99.pdf
- **Accessed:** 2026-08-04 · **Fetched:** yes (local text extraction; 43 pages; executive
  summary and Appendix I scenario-testing methodology read)

#### REG-R138. American Academy of Actuaries, *C-3 Alignment, Part III* (presentation to the NAIC Life RBC (E) Working Group, September 11, 2025)
- **Publisher:** American Academy of Actuaries
- **URL:** https://actuary.org/wp-content/uploads/2025/09/Life-Presentation-C3AlignmentUpdate.pdf
- **Accessed:** 2026-08-04 · **Fetched:** yes (local text extraction; 65 slides, including
  appended Part II from May 1, 2025)
- **Status and [unverified] carried forward:** a **framework presentation**, not adopted law.
  The field-test specifications document itself was **not retrieved**; the reported
  **December 31, 2025** field-test valuation date and **2027** adoption target come from search
  summaries and are **[unverified]**.

#### REG-R142. NAIC Capital Adequacy (E) Task Force — RBC Proposal Form, Agenda Item 2025-01-L (C-2 Mortality Risk / LR025 annual statement sources)
- **Publisher:** NAIC (proposal dated 02/21/2024, submitted on behalf of the Life RBC (E)
  Working Group, Philip Barlow chair)
- **URL:** https://content.naic.org/sites/default/files/inline-files/2025-01-L%20C-2%20Mortality%20Risk%20(1).pdf
- **Accessed:** 2026-08-04 · **Fetched:** yes (local text extraction; 3 pages)

---

## Provenance note

Extraction details live in `us/_research/immediate-annuity.md`: that file records which facts
came from which source, including every [unverified] flag, the failed/partial fetches (S10 and
the block above), the low-reliability marking on S9, the vintage caveats on S6/S7/S8, and the
research gaps this specification inherits — no specimen contract retrieved; **no published
payout-factor tables or guaranteed annuity purchase rates**; **no published commutation /
interest-rate-adjustment formula from any fixed SPIA issuer**; the 2012 IAM Period, 2012 IAM
Basic and Scale G2 numerical tables not retrieved (they live in Appendices 1–4 of AP&P Manual
Appendix A-821); NAIC-published VM-V rate inputs (Weight Tables 1–4, Table X spreads, VM-20
Table A) not retrieved; the paywalled detail of the SOA payout annuity study; and unresearched
state premium tax rates. The cross-product bibliographies
`us/_research/regulatory-actuarial.md` (R1–R34),
`us/_research/regulatory-actuarial-annuities.md` (R35–R72),
`us/_research/statutory-accounting.md` (R73–R99), `us/_research/statutory-reserves.md`
(R100–R113) and `us/_research/risk-based-capital.md` (R125–R142) play the same role for
[REG-R#] tags; where one of them and a document in this directory disagree, **the research
file governs**. Standardizations marked **[std]** in `product-spec.md` and
`technical-notes.md` are introduced at drafting and are not attributable to any source, and
**[unverified]** flags are carried forward unchanged — none was upgraded at this pass.
