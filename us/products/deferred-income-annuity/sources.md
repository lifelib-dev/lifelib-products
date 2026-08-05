# Sources — Deferred Income Annuity (DIA) and Qualified Longevity Annuity Contract (QLAC) (United States)

Source ids, titles, publishers, URLs, access dates and retrieval markers are carried over
verbatim from `us/_research/deferred-income-annuity.md` (the citation ground truth for
[S#]/[R#] tags). **Ids are never renumbered.** Sources in the research file that are not
cited in `product-spec.md` or `technical-notes.md` are omitted (dropped here: **S7**, NYL
official fact sheet, failed fetch; **S10**, Brighthouse QLAC brochure, failed fetch;
**R17**, IRS PLR 201515001, retrieved but found not relevant to DIAs and unused in the
research file itself). **No new sources were fetched at drafting; nothing is marked
"added at drafting."**

Access date for all citations: **2026-08-04**.

---

## Primary product sources [S#]

### S1. New York Life Insurance and Annuity Corporation (NYLIAC) — "New York Life Guaranteed Future Income Annuity II — Product Overview"
- Publisher: NYLIAC (a Delaware corporation), subsidiary of New York Life Insurance
  Company, 51 Madison Avenue, New York, NY 10010. Document distributed by Fidelity
  Insurance Agency, Inc. (authorized distributor); item numbers `969689.8.0`,
  `NYL-DIA-0626`, `49695-20`; © 2026 FMR LLC.
- Doc type: consumer product overview / fact sheet (4 pages). Current vintage (June 2026
  revision code).
- URL fetched: https://communications.fidelity.com/fili/dia/nyl/docs/new_york_life_dfia_factsheet.pdf
- Retrieved: **YES** (full 4-page PDF text extracted)
- Policy form: `ICC11–P101` in most jurisdictions; `211-P101` in some states; state
  variations apply.

### S2. Massachusetts Mutual Life Insurance Company — "MassMutual RetireEase Choice — A Flexible Premium Deferred Income Annuity" (client guide)
- Publisher: Massachusetts Mutual Life Insurance Company, Springfield, MA. Document code
  `AN4325 219  CRN202011-221296`; © 2019 MassMutual. PDF hosted on a third-party content
  CDN (`static.contentres.com`), but the document itself is MassMutual's own 32-page
  client guide.
- Doc type: detailed client/product guide (32 pages) — the most contractually granular DIA
  document retrieved.
- URL fetched: https://s3.amazonaws.com/static.contentres.com/media/documents/cda42ab0-617b-4977-94dc-221106c82e4f.pdf
- Retrieved: **YES** (all 32 pages text extracted)
- Contract forms: `FPDIA12` and `ICC12-FPDIA12` (in certain states, including North
  Carolina).
- **VINTAGE CAVEAT carried over:** this guide is from 2019 and predates SECURE 1.0/2.0.
  Its QLAC figures ($130,000 limit, 25%-of-balance limit, RMD age 70½) are **superseded**
  — see [R1][R2][R3]. Its *product mechanics* remain the most detailed DIA description
  retrieved and are cited as such. This is the **archetype** for the representative design.

### S3. The Guardian Insurance & Annuity Company, Inc. (GIAC) — "Guardian SecureFuture Income Annuity® — A flexible premium deferred income annuity"
- Publisher: The Guardian Insurance & Annuity Company, Inc. (GIAC), a Delaware
  corporation, 7 Hanover Square, New York, NY 10004; wholly owned subsidiary of The
  Guardian Life Insurance Company of America. Document codes
  `641695.4.0 GSFIA-DIA-0118`, `1/15/2018`, `1.956733.103` (Fidelity-distributed version).
  PDF retrieved from a third-party mirror (`qlacs.net`) after the Fidelity-hosted copy
  failed.
- Doc type: consumer fact sheet / brochure (4 pages).
- URL fetched: https://www.qlacs.net/assets/guardian_dia_factsheet.pdf
- Retrieved: **YES** (all 4 pages text extracted)
- **VINTAGE CAVEAT carried over:** January 2018 document; references "the required minimum
  distribution (RMD) age of **70½**" throughout — superseded by SECURE 1.0/2.0. Product
  mechanics still cited; age references flagged.

### S4. Pacific Life Insurance Company / Pacific Life & Annuity Company — "PACIFIC SECURE INCOME® — A Fixed, Deferred Income Annuity" (fact sheet)
- Publisher: Pacific Life Insurance Company (all states except New York) and Pacific Life
  & Annuity Company (all states). Document codes `24-299C`, `FAC0560-01`, `2/26 E1127`.
  Official Pacific Life domain.
- Doc type: producer/consumer fact sheet (6 pages). **Current vintage (Feb 2026)** — the
  most up-to-date primary source retrieved.
- URL fetched: https://www.annuities.pacificlife.com/content/dam/paclife/rsd/annuities/public/pdfs/fact-sheets/pacific-secure-income-fact-sheet.pdf
- Retrieved: **YES** (all 6 pages text extracted)
- Role in this library: the **extended case** (commutation of the present value of
  remaining guaranteed payments; the unbundled "Life Only with 100% Return of Purchase
  Payments Death Benefit" option) and the independent corroboration of the 2026 QLAC
  premium limit.

### S5. Pacific Life — "Pacific Secure Income — Client Guide"
- Publisher: Pacific Life. Document codes `24-300A`, `FAC0555-2401`, `11/24 E1127`.
- Doc type: client guide (16 pages).
- URL fetched: https://www.pacificlife.com/content/dam/paclife/rsd/annuities/public/pdfs/guide/pacific-secure-income-client-guide.pdf
- Retrieved: **YES** (16 pages text extracted)
- Note carried over: the guide does **not** disclose the interest-rate-adjustment charge
  formula used for withdrawals — the basis for the [std]/[unverified] commutation
  construction in `technical-notes.md`.

### S6. Fidelity Investments — "Compare Deferred Income Annuities" (cross-insurer comparison table)
- Publisher: Fidelity Brokerage Services / Fidelity Insurance Agency (distributor
  comparison of third-party insurer products).
- Doc type: web comparison table (secondary/aggregator, but sourced from the insurers'
  filed product parameters and useful as a cross-check).
- URL fetched: https://www.fidelity.com/annuities/deferred-fixed-income-annuities/compare
- Retrieved: **YES**
- Caveat carried over: this is a **distributor aggregation**. Where it conflicts with an
  insurer's own document, the insurer document governs; where it is the only source (USAA
  Life, Western & Southern), rows are flagged as lower-confidence.

### S8. MassMutual — official RetireEase Choice guide on compass.massmutual.com (FAILED FETCH)
- URL attempted: https://compass.massmutual.com/api/public/assets/file/bltd738363f5d003651
- Retrieved: **NO** — request timed out (60s). A current-vintage MassMutual DIA guide was
  therefore **not** obtained; [S2] is the 2019 edition. Cited only as the reason for the
  vintage caveat on the archetype.

### S9. Fidelity communications-hosted insurer fact sheets (PARTIAL FAILURE)
- URLs attempted: https://communications.fidelity.com/fili/docs/guardian-dia-factsheet.pdf
  and https://communications.fidelity.com/fili/docs/usaa-dia-factsheet.pdf
- Retrieved: **NO** — both returned an HTML interstitial rather than PDF bytes when
  fetched directly. Guardian content was obtained from a mirror [S3]; **no USAA Life
  primary document was retrieved** (USAA parameters come only from [S6]). Cited only as
  the reason the Guardian minimum-deferral conflict could not be resolved.

### S11. Guardian brochure on immediateannuities.com (FAILED FETCH)
- URL attempted: https://www.immediateannuities.com/annuity-brochures/guardian-securefuture-income-annuity.pdf
- Retrieved: **NO** — HTTP 403 Forbidden. Cited only as the second failed route to a
  current Guardian primary document.

---

## Regulatory and actuarial references [R#] (product research file numbering)

### R1. 26 CFR § 1.401(a)(9)-6(q) — Qualifying longevity annuity contract (current text)
- Publisher: U.S. Government (eCFR, current edition), Treasury/IRS.
- Doc type: codified Treasury Regulation.
- URL fetched: https://www.ecfr.gov/api/renderer/v1/content/enhanced/current/title-26?chapter=I&subchapter=A&part=1&section=1.401(a)(9)-6
  (renders 26 CFR 1.401(a)(9)-6; human-readable equivalent
  https://www.ecfr.gov/current/title-26/section-1.401(a)(9)-6)
- Retrieved: **YES** (full section text extracted)
- Credit line carried over: `[T.D. 9130, 69 FR 33293, June 15, 2004; … T.D. 9673, 79 FR
  37639, July 2, 2014; … T.D. 10001, 89 FR 58907, July 19, 2024]` — the paragraph (q)
  QLAC rules were **restructured from the old "A-17" Q&A format into paragraph (q)** by
  the July 2024 final regulations [R6].

### R2. SECURE 2.0 Act of 2022, § 202 ("Qualifying Longevity Annuity Contracts") — Division T of Pub. L. 117-328
- Publisher: U.S. Government Publishing Office (govinfo), enrolled text of Public Law
  117-328 (Consolidated Appropriations Act, 2023), Division T = SECURE 2.0 Act of 2022.
  Statutory note codified at 26 U.S.C. 401 note; text at 136 Stat. 5331–5332.
- Doc type: enacted federal statute.
- URL fetched: https://www.govinfo.gov/content/pkg/PLAW-117publ328/html/PLAW-117publ328.htm
- Retrieved: **YES** (full text downloaded; § 202 located and read)
- Caveat carried over: SECURE 2.0's **enactment date (December 29, 2022) is [unverified]**
  — the statutory text says only "the date of the enactment of this Act". The derived
  base-period quarter (July 1, 2022) *is* confirmed directly by the codified regulation
  [R1 (q)(4)(ii)(A)(1)].

### R3. IRS Notice 2025-67 — "2026 Amounts Relating to Retirement Plans and IRAs, as Adjusted for Changes in Cost-of-Living"
- Publisher: Internal Revenue Service (irs.gov); published in Internal Revenue Bulletin
  2025-49.
- Doc type: IRS notice (annual COLA).
- URL fetched: https://www.irs.gov/pub/irs-drop/n-25-67.pdf
- Retrieved: **YES**
- Fact carried over verbatim: "The limitation on premiums paid for a qualifying longevity
  annuity contract under § 1.401(a)(9)-6(q)(2)(ii) remains $210,000."

### R4. 26 CFR § 1.401(a)(9)-5(b)(4) — Exclusion of QLAC value from the account balance
- Publisher: eCFR (current edition), Treasury/IRS.
- URL fetched: https://www.ecfr.gov/api/renderer/v1/content/enhanced/current/title-26?chapter=I&subchapter=A&part=1&section=1.401(a)(9)-5
- Retrieved: **YES**
- Credit line: `[… T.D. 9673, 79 FR 37639, July 2, 2014; T.D. 9930, 85 FR 72477, Nov. 12,
  2020; T.D. 10001, 89 FR 58907, July 19, 2024]`.

### R5. 26 CFR § 1.408-8(h) — QLACs in the IRA context
- Publisher: eCFR (current edition), Treasury/IRS.
- URL fetched: https://www.ecfr.gov/api/renderer/v1/content/enhanced/current/title-26?chapter=I&subchapter=A&part=1&section=1.408-8
- Retrieved: **YES**
- Credit line: `[… T.D. 9673, 79 FR 37642, July 2, 2014; T.D. 10001, 89 FR 58948,
  July 19, 2024]`. Applicability: for RMDs for calendar years beginning on or after
  January 1, 2025.

### R6. T.D. 10001 — "Required Minimum Distributions", final regulations (Federal Register)
- Publisher: Treasury Department / Internal Revenue Service.
- Doc type: final rule.
- URL fetched (metadata via Federal Register API):
  https://www.federalregister.gov/documents/2024/07/19/2024-14542/required-minimum-distributions
- Retrieved: **YES** (metadata; **full preamble not read** — carried-over caveat: any
  statement about *why* Treasury drafted a particular QLAC provision would be
  unsupported). Document number **2024-14542**; citation **89 FR 58886**; published
  **July 19, 2024**; **effective September 17, 2024**.

### R7. T.D. 9673 — "Longevity Annuity Contracts", final regulations (the original 2014 QLAC rule)
- Publisher: Treasury Department / Internal Revenue Service.
- URL fetched (metadata via Federal Register API):
  https://www.federalregister.gov/documents/2014/07/02/2014-15524/longevity-annuity-contracts
- Retrieved: **YES** (metadata). Document number **2014-15524**; citation **79 FR 37633**;
  published **July 2, 2014**.

### R8. Internal Revenue Code § 72 — Annuities; certain proceeds of endowment and life insurance contracts
- Publisher: Cornell Legal Information Institute (LII) rendering of 26 U.S.C. § 72.
- URL fetched: https://www.law.cornell.edu/uscode/text/26/72
- Retrieved: **YES** (key subsections read; full section is long)

### R9. NAIC — Valuation Manual, January 1, 2026 edition
- Publisher: National Association of Insurance Commissioners.
- Doc type: statutory valuation manual (457 pages).
- URL fetched: https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf
- Retrieved: **YES** (full 457-page text extracted and searched directly)
- Sections used: VM-01 (DIA definition); VM-22 §§2.B, 3.A, 3.F.1.a and the Section 6
  standard-projection tables (mortality, Table 6.8, maintenance expense Table 6.1, lapse,
  annuitization); VM-M §1.J (2012 IAR); VM-V §1 (income annuities, Valuation Rate Buckets,
  premium determination date, prescribed portfolio).
- Caveats carried over: **VM-22 Table 6.8 was captured only through attained age 79**; the
  **seven-basis-point expense provision was truncated at a page break**, so the exact
  present-value base for contracts without an account value is not quoted.

### R10. NAIC — Standard Nonforfeiture Law for Individual Deferred Annuities (Model #805), Fall 2020 edition
- Publisher: National Association of Insurance Commissioners.
- URL fetched: https://content.naic.org/sites/default/files/model-law-805.pdf
- Retrieved: **YES** (all 5 pages)
- Caveat carried over: **Section 4.B (the nonforfeiture interest rate definition) and the
  balance of Section 4.A(1)(c)–(d) were not captured** in this extract; the well-known
  "5-year CMT minus 125 bp" formulation and its floor are therefore **[unverified] in this
  file**. The cross-product entry [REG-R42] read Sections 1–8 in full and settles the
  floor at **15 basis points**, which is the figure used in `product-spec.md`.

### R11. NAIC — Annuity Disclosure Model Regulation (Model #245)
- Publisher: National Association of Insurance Commissioners (© 2015 edition of the model
  text within the Fall compendium).
- URL fetched: https://content.naic.org/sites/default/files/model-law-245.pdf
- Retrieved: **YES** (40 pages)
- Caveat carried over: the Section 3.A characterisation (a non-participating DIA has no
  non-guaranteed elements and is therefore exempt) is a direct reading of the retrieved
  text; **whether individual states apply it the same way to DIAs was not verified**.

### R12. NAIC — Variable Annuity Model Regulation (Model #250)
- Publisher: National Association of Insurance Commissioners (October 2007 edition).
- URL fetched: https://content.naic.org/sites/default/files/model-law-250.pdf
- Retrieved: **YES**
- Role: identifies the mis-numbering — **Model #250 is the Variable Annuity Model
  Regulation**, not an annuity disclosure regulation, and does not apply to a
  general-account DIA. The disclosure model is **#245** [R11].

### R13. IIPRC — "Individual Deferred Paid-Up Non-Variable Annuity Contract Standards (Commonly Marketed as Deferred Income Annuities or Longevity Annuities)", IIPRC-A02-I-LONG
- Publisher: Interstate Insurance Product Regulation Commission (Insurance Compact).
- Doc type: adopted uniform product standard (26 pages). **The single most contractually
  precise DIA reference retrieved**, and the contractual-language authority throughout
  this library, no DIA specimen contract having been located.
- URL fetched: https://www.insurancecompact.org/sites/default/files/2022-12/171120_ind_def_pu_non_var_ann_long_stds.pdf
  (record page: https://www.insurancecompact.org/standards/record-adopted-standards/individual-deferred-paid-non-variable-annuity-contract-standards)
- Retrieved: **YES** (all 26 pages)
- Dates: **Adopted August 5, 2017; Effective November 20, 2017**; amends standards
  originally adopted October 17, 2010; amendments apply only to new filings received after
  the effective date.

### R14. American Academy of Actuaries / SOA Payout Annuity Table Team — "Payout Annuity Report" (September 28, 2011)
- Publisher: American Academy of Actuaries (report prepared by the Joint Academy/SOA
  Payout Annuity Table Team at the request of the NAIC Life Actuarial (A) Task Force).
- URL fetched: https://www.actuary.org/wp-content/uploads/2017/11/Payout_Annuity_Report_09-28-11.pdf
- Retrieved: **YES** (36 pages)

### R15. SOA Research Institute & LIMRA — "2020-24 Payout Annuity Experience Study" (Study Highlights), © 2026
- Publisher: Society of Actuaries Research Institute (with LIMRA).
- URL fetched: https://www.soa.org/globalassets/assets/files/resources/research-report/2026/2020-24-payout-annuity-exp-study.pdf
- Retrieved: **YES** (5-page Study Highlights document; the full results are behind the SOA
  "Experience Studies Pro" subscription)
- Fact of first importance here, carried over verbatim: "The study includes immediate
  annuities, **deferred income annuities**, settlement options, and annuitizations of life
  insurance and annuity death claims."
- Caveat carried over: **no A/E ratios or DIA-specific mortality results are quoted** —
  only the highlights were retrieved.

### R16. SOA — "2012 Individual Annuity Reserving Report & Table" (resource page)
- Publisher: Society of Actuaries.
- URL fetched: https://www.soa.org/resources/experience-studies/2011/2012-ind-annuity-reserving-rpt/
- Retrieved: **YES** (page content; no date stated on the page for the report itself)
- Role here: it identifies **http://mort.soa.org/** as the machine-readable source for the
  2012 IAM Period, 2012 IAM Basic and Scale G2 tables. Caveat carried over: **those
  numerical tables were not downloaded**, which is why the worked example in
  `technical-notes.md` uses illustrative **[std]** survival and annuity factors rather
  than table lookups.

---

## Cross-product regulatory references [REG-R#]

These are cited with the **[REG-R#]** prefix to avoid collision with the product research
file's own R-numbering. They resolve against the curated page
`us/references/regulatory-and-actuarial-references.md`, whose **shared numbering space runs
R1–R142 and is one space, not several**, with **R114–R124 and R143–R149 permanently unused
by design** (the block convention that let three research streams number independently —
the gaps are not losses and must not be back-filled):

- **R1–R34** are of life origin; research provenance `us/_research/regulatory-actuarial.md`.
  Several of them also bind annuity models and are listed as such in the annuity
  bibliography's "Existing entries (R1–R34) that also bind annuity models" table.
- **R35–R72** are annuity-specific; research provenance
  `us/_research/regulatory-actuarial-annuities.md`, which opens the continuation of the
  same numbering space at R35.
- **R73–R142** are the statutory accounting and capital entries; per-entry bibliography at
  `us/regulatory/sources.md`, research provenance `us/_research/statutory-accounting.md`
  (R73–R99), `us/_research/statutory-reserves.md` (R100–R113) and
  `us/_research/risk-based-capital.md` (R125–R142). Cited here only by the
  "Statutory accounting and capital" section of `technical-notes.md` and the corresponding
  paragraph of `product-spec.md`; the full entries are reproduced below.

Entries cited by the product-mechanics sections of the two documents in this directory
(retrieval status as recorded in the originating research file, access date 2026-08-04):

| Tag | Short title | Half | Retrieval status |
|---|---|---|---|
| REG-R16 | 26 U.S.C. § 807 — tax reserves | R1–R34 (life file) | fetched |
| REG-R26 | ASOP No. 2 — Nonguaranteed Elements for Life Insurance and Annuity Products | R1–R34 | fetched |
| REG-R27 | ASOP No. 7 — Life or Health Cash Flow Analysis | R1–R34 | fetched |
| REG-R29 | ASOP No. 22 — Opinions Based on Asset Adequacy Analysis | R1–R34 | fetched |
| REG-R31 | ASOP No. 52 — PBR for **Life** Products under the Valuation Manual (cited to show it does **not** cover VM-22) | R1–R34 | fetched |
| REG-R32 | ASOP No. 56 — Modeling | R1–R34 | fetched |
| REG-R34 | FASB ASU 2018-12 (LDTI) | R1–R34 | fetched |
| REG-R35 | VM-21 — PBR for Variable Annuities (cited to show it does **not** apply) | R35–R72 (annuity file) | fetched (local text extraction) |
| REG-R36 | VM-22 — PBR for Non-Variable Annuities | R35–R72 | fetched (local text extraction) |
| REG-R37 | VM-V Section 1 — Income Annuities (statutory maximum valuation interest rates) | R35–R72 | fetched (local text extraction) |
| REG-R41 | VM-C — Appendix C index of incorporated actuarial guidelines | R35–R72 | fetched (local text extraction) |
| REG-R42 | Standard Nonforfeiture Law for Individual Deferred Annuities (Model #805) — full Sections 1–8, source of the **15 bp** floor correction | R35–R72 | fetched (local text extraction) |
| REG-R43 | Variable Annuity Model Regulation (Model #250) — the numbering correction | R35–R72 | fetched (local text extraction) |
| REG-R44 | Actuarial Guideline LIV (AG 54) — cited only to name the "interim value" concept a DIA does not have | R35–R72 | fetched (local text extraction, complete) |
| REG-R45 | Annuity Disclosure Model Regulation (Model #245) | R35–R72 | fetched (local text extraction) |
| REG-R46 | Suitability in Annuity Transactions Model Regulation (Model #275) | R35–R72 | fetched (local text extraction) |
| REG-R49 | SEC Release 33-11294 — registration for index-linked and registered MVA annuities (contrast case) | R35–R72 | fetched via govinfo; sec.gov PDF returned 403 |
| REG-R52 | SEC Form N-4 (contrast case) | R35–R72 | **not fetched** (sec.gov 403) |
| REG-R53 | CRS Report R40656 — SEC Rule 151A and Annuities (why fixed annuities are not registered securities) | R35–R72 | fetched |
| REG-R55 | 26 U.S.C. § 72 — Annuities (same statute as [R8] above) | R35–R72 | fetched |
| REG-R56 | 26 U.S.C. § 1035 — exchanges | R35–R72 | fetched |
| REG-R57 | 26 C.F.R. § 1.401(a)(9)-6 — QLAC rules (same regulation as [R1] above, LII rendering) | R35–R72 | fetched |
| REG-R58 | T.D. 10001 — RMD final regulations implementing SECURE 2.0 § 202 (same T.D. as [R6] above, govinfo full text) | R35–R72 | fetched via govinfo |
| REG-R59 | Model #821 + VM-M §§1.I–1.M, 2.C — annuity valuation mortality (2012 IAR, 2012 IAM Period/Basic, Scale G2) | R35–R72 | fetched (local text extraction, both) |
| REG-R60 | 2012 IAR development report (Payout Annuity Table Team; same report as [R14] above) | R35–R72 | fetched (local text extraction) |
| REG-R61 | 2020–2024 Individual Payout Annuity Mortality Experience Study (landing page; highlights PDF fetched as [R15] above) | R35–R72 | fetched (landing page) |
| REG-R65 | SOA Individual Annuity Experience Studies index — the only route to the **deferred-period** mortality sources (2011–2015 deferred annuity mortality; 2006 deferred-period analysis) | R35–R72 | fetched |
| REG-R70 | ASOP No. 54 — Pricing of Life Insurance and Annuity Products | R35–R72 | fetched |
| REG-R71 | ASOP No. 10 — U.S. GAAP for Long-Duration Life, Annuity, and Health Products (Doc. No. 207) | R35–R72 | fetched (local text extraction) |

Cross-product note carried over from the annuity bibliography — **the numbers below are
cross-product numbers, i.e. [REG-R#] in this directory, not the product-local [R#] above**:
for the deferred-income-annuity product the binding new entries are **R36, R37, R41, R59,
R60, R61, R55, R56, R57, R58, R70, R71**, plus the existing entries **R1, R3, R16, R27,
R29, R32, R33, R34** [`us/_research/regulatory-actuarial-annuities.md`, cross-reference
table]. (Cross-product R33 is cited by neither document in this directory, so it carries no
[REG-R#] row in the table above; cross-product R1 and R3 are now cited by the statutory
accounting and capital material and appear in full below.)

### Entries newly cited by the statutory accounting and capital section

Ids, titles, publishers, URLs, access dates and fetched markers below are carried **verbatim**
from `us/regulatory/sources.md`, which is the citation ground truth for R73–R142 (and which
itself reproduces the R1–R72 metadata from
`us/references/regulatory-and-actuarial-references.md`). **Nothing is renumbered and nothing is
re-worded**, including the internal cross-references some entries make to ids not listed here
(R41, R73, R81, R139, R141) — those resolve against `us/regulatory/sources.md` and the shared
reference page. Three of these — **R1, R3 and R39** — are frozen R1–R72 entries that this
directory had not previously cited; the rest are R73–R142.

**Read every heading below as a cross-product id, i.e. `[REG-R#]` in this directory, never the
product-local `[R#]` of the section above.** The collision is real and matters: **R1 here is the
Standard Valuation Law**, whereas product-local **[R1] is 26 CFR § 1.401(a)(9)-6(q)**; likewise
cross-product R3 is the Valuation Manual while product-local [R3] is IRS Notice 2025-67. The
headings keep the source ids verbatim rather than being re-prefixed.

### REG-R1. Standard Valuation Law (Model #820)
- **Publisher:** National Association of Insurance Commissioners (NAIC)
- **URL:** https://content.naic.org/sites/default/files/model-law-820.pdf
- **Accessed:** 2026-08-03 · **Fetched:** yes (27-page PDF retrieved and read; re-read for
  the reserves stream at §§3, 4b, 5, 5a, 6, 7, 11, 12)

### REG-R3. Valuation Manual, Jan. 1, 2026 Edition (VM-01, VM-02, VM-20, VM-31, VM-M, VM-G, VM-C, VM-V, …)
- **Publisher:** NAIC
- **URL:** https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf
- **Accessed:** 2026-08-03 · **Fetched:** yes (457-page PDF retrieved; cover, adoption
  history, and full table of contents read; "NAIC Adoptions through August 13, 2025"). The
  reserves stream additionally read VM-01 definitions and VM-20 §§1, 2, 3.B–3.E, 4, 5, 6,
  7.A/7.B by local text extraction.

### REG-R39. Actuarial Guideline XXXIII — Determining CARVM Reserves for Annuity Contracts With Elective Benefits (AG 33)
- **Publisher:** NAIC
- **URL:** none — **no free official standalone text was located.** Title and current status
  verified from the Valuation Manual's VM-C index (page C-1) [R41]; the authoritative text is
  in the **AP&P Manual Appendix C**.
- **Accessed:** 2026-08-04 (search date; guideline text not retrieved)
- **Fetched:** **no.** Neither document in this directory quotes AG 33 mechanics, and both say
  so at the point of use.

### REG-R75. SSAP No. 71 — Policy Acquisition Costs and Commissions (*As of March 2026*)
- **Publisher:** NAIC (in R73, statement pages 71-1 to 71-3)
- **URL:** https://content.naic.org/sites/default/files/publication-app-manual.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; ¶¶1–7 read in full)

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

### REG-R97. SSAP No. 101 — Income Taxes (*As of March 2026*)
- **Publisher:** NAIC (in R73, statement pages 101-1 onward, with Exhibit A Q&A)
- **URL:** https://content.naic.org/sites/default/files/publication-app-manual.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; status block, ¶¶1–2 and the full admissibility
  section ¶¶11–12 including all three Realization Threshold Limitation Tables read)

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

### REG-R111. Asset Adequacy Analysis — Public Policy Practice Note, for companies that file a Life, Accident and Health/Fraternal Statutory Annual Statement
- **Publisher:** American Academy of Actuaries, Asset Adequacy Analysis Practice Note Work
  Group and the Life Valuation Committee; **September 2017, updated September 2024** (the
  Academy's resource page dates the update posting December 24, 2024); 93 pages
- **URL (PDF):** https://actuary.org/wp-content/uploads/2025/03/Life-PracticeNote-2017AATUpdate.pdf
  — **URL (landing page):** https://actuary.org/resources/asset-adequacy-analysis-updated-for-2024/
- **Accessed:** 2026-08-04
- **Fetched:** yes, both (PDF by local text extraction; front matter, complete table of
  contents, and Q12, Q13, Q14, Q17, Q19, Q21, Q22, Q23, Q28, Q29, Q30, Q32, Q33, Q34, Q35,
  Q113, Q115, Q116, Q117, Q118 read)
- **Status and vintage cautions carried forward:** not an ASB promulgation, not an ASOP, not
  binding. Its quantitative statements come from appointed-actuary surveys conducted in
  **2004 and 2012** and are practice indicators, not benchmarks. Its statement that INT 23-01
  was nullified on January 1, 2026 was written in September 2024 and is **superseded** by the
  August 11, 2025 extension recorded at R87.

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

### REG-R134. NAIC memorandum, *Request for Comment on Longevity Risk Factors and Instructions* (Philip Barlow, chair Life RBC (E) Working Group; Rhonda Ahrens, chair Longevity Risk (E/A) Subgroup; April 30, 2021)
- **Publisher:** NAIC
- **URL:** https://content.naic.org/sites/default/files/inline-files/Longevity%20Risk%20Memo.pdf
- **Accessed:** 2026-08-04 · **Fetched:** yes (local text extraction; 2 pages)

### REG-R135. *Phase I Report of the American Academy of Actuaries' C-3 Subgroup of the Life Risk Based Capital Task Force to the NAIC's Risk Based Capital Work Group* (October 1999, Atlanta)
- **Publisher:** American Academy of Actuaries
- **URL:** https://www.actuary.org/wp-content/uploads/2025/05/c3_oct99.pdf
- **Accessed:** 2026-08-04 · **Fetched:** yes (local text extraction; 43 pages; executive
  summary and Appendix I scenario-testing methodology read)

### REG-R138. American Academy of Actuaries, *C-3 Alignment, Part III* (presentation to the NAIC Life RBC (E) Working Group, September 11, 2025)
- **Publisher:** American Academy of Actuaries
- **URL:** https://actuary.org/wp-content/uploads/2025/09/Life-Presentation-C3AlignmentUpdate.pdf
- **Accessed:** 2026-08-04 · **Fetched:** yes (local text extraction; 65 slides, including
  appended Part II from May 1, 2025)
- **Status and [unverified] carried forward:** a **framework presentation**, not adopted law.
  The field-test specifications document itself was **not retrieved** (only the working group
  page's note of a **July 30, 2026** re-exposure, R141); the reported **December 31, 2025**
  field-test valuation date and **2027** adoption target come from search summaries and are
  **[unverified]**.

### REG-R142. NAIC Capital Adequacy (E) Task Force — RBC Proposal Form, Agenda Item 2025-01-L (C-2 Mortality Risk / LR025 annual statement sources)
- **Publisher:** NAIC (proposal dated 02/21/2024, submitted on behalf of the Life RBC (E)
  Working Group, Philip Barlow chair)
- **URL:** https://content.naic.org/sites/default/files/inline-files/2025-01-L%20C-2%20Mortality%20Risk%20(1).pdf
- **Accessed:** 2026-08-04 · **Fetched:** yes (local text extraction; 3 pages)

---

## Provenance note

Extraction details live in `us/_research/deferred-income-annuity.md`: that file records
which facts came from which source, the [unverified] flags, the failed fetches (S7–S11),
the source-vintage caveats (MassMutual 2019 [S2][S8], Guardian January 2018 [S3][S9][S11],
with NYL June 2026 [S1] and Pacific Life February 2026 [S4] the current-vintage primary
sources — the research file's own S4 header calls it "the most up-to-date primary source
retrieved", which its S1 header (June 2026 revision code) does not support), the distributor-mirror
hosting caveat for [S1] and [S3], and the four **regulatory corrections** this library
follows rather than repeating the common misconceptions:

1. **Model #250 is the Variable Annuity Model Regulation, not the Annuity Disclosure Model
   Regulation** — the disclosure model is **#245** [R11][R12][REG-R43][REG-R45].
2. **The QLAC rules live in Treas. Reg. § 1.401(a)(9)-6(q), not in "A-17"** — T.D. 10001
   restructured them out of the Q&A format on July 19, 2024 [R1][R6][REG-R58].
3. **The 25%-of-account-balance QLAC premium limit no longer exists** — SECURE 2.0 § 202
   directed its elimination and the codified text has only a dollar limitation
   [R1][R2][REG-R58].
4. **The Model #805 indexed nonforfeiture rate floor is 15 basis points, not 1%** — the DIA
   research file's own extract did not capture Section 4.B and therefore left the "floored
   at 1%" formulation [unverified] [R10]; the fully fetched text in the cross-product
   bibliography settles it at 0.15% [REG-R42].

The cross-product bibliographies `us/_research/regulatory-actuarial.md` (R1–R34) and
`us/_research/regulatory-actuarial-annuities.md` (R35–R72) play the same role for
[REG-R#] tags. Income-phase mechanics are specified in
`us/products/immediate-annuity/`, whose research provenance is
`us/_research/immediate-annuity.md`. Standardizations marked **[std]** in
`product-spec.md` and `technical-notes.md` are introduced at drafting and are not
attributable to any source.
