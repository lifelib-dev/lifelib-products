# Sources — Universal Life Insurance (current assumption)

Source ids, titles, publishers, URLs, access dates, and retrieval markers are carried
over verbatim from `us/_research/universal-life.md` (the citation ground truth for
[S#]/[R#] tags). Ids are never renumbered. Sources from the research file that are not
cited in `product-spec.md` or `technical-notes.md` are omitted (dropped here: R9).
No new sources were fetched at drafting; nothing is marked "added at drafting".

Access date for all citations: 2026-08-03.

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
`us/references/regulatory-and-actuarial-references.md` (same R-numbering).
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
