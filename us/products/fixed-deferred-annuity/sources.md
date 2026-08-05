# Sources — Fixed Deferred Annuity (MYGA) (United States)

Source ids, titles, publishers, URLs, access dates and retrieval markers are carried over
**verbatim** from `us/_research/fixed-deferred-annuity.md` (the citation ground truth for
[S#]/[R#] tags). Ids are never renumbered. Sources in the research file that are not cited
by `product-spec.md` or `technical-notes.md` are omitted (dropped here: S17, S18, S19, R3,
R10 — see the note at the end of the [R#] section). **No new sources were fetched at
drafting; nothing is marked "added at drafting".**

Access date for all citations: **2026-08-04**, except the frozen [REG-R#] entries reproduced
in full at the end of this file, whose own access dates (2026-08-03 or 2026-08-04) are carried
verbatim from `us/regulatory/sources.md`.

---

## Primary product sources [S#]

### S1. Athene Annuity & Life Assurance Company — "ATHENE MaxRate® Multi-Year Guarantee Annuity (MYGA) CA Version", producer fact sheet AN1007-CA (10/14)
- Publisher: Athene Annuity & Life Assurance Company (Wilmington, DE; main administrative
  office Greenville, SC). PDF hosted on iPipeline's forms repository, which distributes
  carrier-authored producer material.
- Doc type: producer product fact sheet (2 pages), "FOR PRODUCER USE ONLY"
- URL fetched: https://files.ipipeline.com/AALAC/AN1007CA.pdf
- Retrieved: YES (full text extracted)
- Note carried over: this CA version has **no** market value adjustment provision.

### S2. Athene Annuity & Life Assurance Company of New York — "ATHENE MaxRate® Multi-Year Guarantee Annuity (MYG)", producer fact sheet AN1007-NY (06/16)
- Publisher: Athene Annuity & Life Assurance Company of New York (Nyack, NY)
- Doc type: producer product fact sheet (4 pages), New York only
- URL fetched: https://files.ipipeline.com/AALAC/AN1007NY.pdf
- Retrieved: YES (full text extracted)
- Role in this library: source of the **symmetrically capped** MVA (adjustment, positive or
  negative, not greater than the withdrawal charge) and of the renewal 5/4/3/2/1 schedule.

### S3. Voya Retirement Insurance and Annuity Company — "Voya Multi-Rate Annuity (Voya MRA)" prospectus, Form 424B3, dated May 1, 2021
- Publisher: Voya Retirement Insurance and Annuity Company (Windsor, CT), filed with the SEC
- Doc type: statutory prospectus for a single purchase payment, modified guaranteed deferred
  annuity contract (39 pages incl. Appendix I on the MVA); product closed to new sales
- URL fetched: https://www.sec.gov/Archives/edgar/data/837010/000010300521000017/definitivemultirateannuity.pdf
- Retrieved: YES (full text extracted, pages 1–17 and 37–39)
- Role: uncapped geometric Treasury-based MVA; the gross-up example for a net check.

### S4. Nationwide Life Insurance Company — "BOA Platinum Edge", Form S-1 registration statement / prospectus dated May 1, 2023, "Flexible Purchase Payment Modified Guaranteed Annuity Contracts Supporting Guaranteed Periods"
- Publisher: Nationwide Life Insurance Company (Columbus, OH), filed with the SEC
  (filed 2023-04-07)
- Doc type: registration statement containing the full prospectus, including Appendix A with
  MVA worked examples and a sensitivity table
- URL fetched: https://www.sec.gov/Archives/edgar/data/1127203/000119312523095286/d490814ds1.htm
- Retrieved: YES (full text extracted)
- Role in this library: **arithmetic unit-test anchor** for the geometric MVA branch — the
  only retrieved source with fully worked MVA numbers.

### S5. Midland National Life Insurance Company — "Oak ADVantage® multi-year guarantee annuity", consumer brochure 34158Y REV 6-26
- Publisher: Midland National Life Insurance Company (West Des Moines, IA), a Sammons
  Financial Group member. Official insurer domain.
- Doc type: consumer product brochure (8 pages)
- URL fetched: https://www.midlandnational.com/documents/35453/349595425/34158Y+-+Oak+ADVantage+brochure.pdf/57b2f6a9-d3fc-65d4-c613-83f262f42fab?t=1724168079212
- Retrieved: YES (full text extracted)
- Note carried over: features flagged as offered "by current company practice" are
  explicitly **not** contractual guarantees and can be withdrawn at any time.

### S6. Midland National Life Insurance Company — "Oak ADVantage℠ multi-year guarantee annuity" highlight sheet 34199Y REV 11-24
- URL fetched: https://www.midlandnational.com/documents/35453/65313/34199Y+-+Oak+ADVantage+highlight+sheet.pdf/efeb0d27-884d-e0f2-535d-6430a37a58ac?t=1635796256861
- Doc type: 2-page product highlight sheet
- Retrieved: YES

### S7. Midland National Life Insurance Company — "Oak ADVantage® and Oak ADVantage® Care" rate sheet 32400Y REV 7-23-26 (interest rates effective July 23, 2026)
- URL fetched: https://www.midlandnational.com/documents/35453/349595419/32400Y+-+Oak+ADVantage+rate+sheet.pdf/fa83c185-49b5-ef49-afc7-fdf4da62b245?t=1726160212636
- Doc type: 1-page producer rate sheet
- Retrieved: YES
- Caveat carried over: the declared rates 5.45% / 5.60% / 5.50% are certain, but the
  text-extraction order does not unambiguously bind each rate to its guarantee period; the
  3 / 5 / 7-year mapping is **[unverified]**. (No rate from S7 is used in the product
  documents; S7 is cited only for the $50,000 minimum premium and the Care variant.)

### S8. Midland National Life Insurance Company — "Understanding the market value adjustment", 32340Y-2 REV 7-25 (Midland National Capital Income® fixed index annuity)
- URL fetched: https://www.midlandnational.com/documents/35453/9032621/32340Y+-+Understanding+the+MVA/7446bfd5-4e75-8e71-db85-e055f63ea9de
- Doc type: 2-page consumer MVA explainer
- Retrieved: YES
- **Caveat carried over:** written for the Capital Income *fixed index* annuity, not for a
  MYGA. Cited here because it states the Sammons/Midland MVA formula, base and caps
  explicitly, and Oak ADVantage uses the same MVA family [S5][S6]; **the numeric example
  must not be attributed to a MYGA** and is labelled as such wherever used.

### S9. Midland National Life Insurance Company — "Midland National Capital Income® Fixed index annuity — Annuity disclosure statement", 32372Y-5 (8-24)
- URL fetched: https://www.midlandnational.com/documents/35453/9032621/32372Y+-+Capital+Income+disclosure+for+most+states/f334edb5-4545-608e-3e7b-f8558ed021b8
- Doc type: signed annuity disclosure statement (12 pages)
- Retrieved: YES
- **Caveat carried over:** FIA, not a MYGA. Cited for (a) contractually-precise MVA wording,
  (b) the nonforfeiture-floor wording and its **net-of-charges** withdrawal convention, and
  (c) the disclosure-statement structure that Model #245 [R4] drives.

### S10. MassMutual Ascend Life Insurance Company — "SecureGain 5 Annuity — A fixed annuity with a market value adjustment", consumer brochure B1088822NW 4/23
- Publisher: MassMutual Ascend Life Insurance Company (Cincinnati, OH), a wholly owned
  subsidiary of Massachusetts Mutual Life Insurance Company (formerly Great American Life)
- Doc type: consumer brochure (12 pages) with a product-features specification table
- URL fetched: https://mybusiness.massmutualascend.com/docs/default-source/default-document-library/forms/marketing-materials/b1088822nw.pdf?sfvrsn=845c2fde_3
- Retrieved: YES (full text extracted)
- Role: the charge/liquidity anchor — 9/8/7/6/5 early withdrawal charge, 10% free
  withdrawal, extended-care and terminal-illness waivers.

### S11. MassMutual Ascend Life Insurance Company — "SecureGain 5" client rate flier F1089525NW-1 (rates effective 09/22/25)
- URL fetched: https://mybusiness.massmutualascend.com/docs/default-source/default-document-library/forms/marketing-materials/f1089525nw-1.pdf?sfvrsn=7b719de_1
- Doc type: 2-page rate flier with disclosure footnotes
- Retrieved: YES
- Note carried over: **the single best retrieved statement of the nonforfeiture floor in a
  real product** — the GMSV definition, its 2.80% rate, the 0.25% minimum interest rate and
  the express tie to NAIC Model #805.

### S12. MassMutual Ascend Life Insurance Company — "How a market value adjustment works", S6075424NW 8/24
- URL fetched: https://mybusiness.massmutualascend.com/docs/default-source/default-document-library/forms/marketing-materials/s6075424nw.pdf?sfvrsn=d91920de_2
- Doc type: 2-page consumer MVA explainer
- Retrieved: YES
- Role: the **asymmetric** cap design (positive capped at the early withdrawal charge,
  negative floored by the standard nonforfeiture law minimum) and the blended
  Treasury/corporate reference indices.

### S13. New York Life Insurance and Annuity Corporation (NYLIAC) — "Secure Term MVA Fixed Annuity II — Just the facts", client fact sheet ML25-007661 / SMRU5821693 (Exp. 03.20.2028)
- Publisher: New York Life Insurance and Annuity Corporation (a Delaware corporation),
  wholly owned subsidiary of New York Life Insurance Company. Official insurer domain
  (nylannuities.com).
- Doc type: 4-page client fact sheet with full feature table and footnotes
- URL fetched: https://www.nylannuities.com/connectedassets/final-assets/marketing-materials/fact-sheet-products/TPD_Client_FactSheet_ST_MVA_II_Generic.pdf
- Retrieved: YES (full text extracted). An earlier WebFetch of the same URL and of an
  immediateannuities.com copy returned HTTP 403; the direct Python fetch succeeded.
- Role: the **Camp B** renewal architecture (annually redeclared rates, no new surrender
  charge) and the GMIR-floored MVA. Gap carried over: the exact MVA algebra is not in the
  fact sheet — it points to a separate "Examples and Explanation" flyer, not retrieved.

### S14. Symetra Life Insurance Company — "Form of Section 457 Contract Data Page", Exhibit 99.4(i) to Form 485BPOS for Symetra Separate Account C (filed 2009)
- Publisher: Symetra Life Insurance Company (Bellevue, WA), filed with the SEC
- Doc type: **specimen contract data page** (bracketed values), for the Spinnaker Advisor
  Variable Annuity
- URL fetched: https://www.sec.gov/Archives/edgar/data/0000912869/000119312509093761/dex994i.htm
- Retrieved: YES (full text extracted)
- **Caveat carried over:** a VA chassis, not a standalone MYGA, and the values are bracketed
  specimen values. Cited only for the MVA on its Guaranteed Interest Period Fixed Account
  Option — the classic **declared-rate-differential** `W × (Ic − In) × Fs` design with its
  contractual duration-factor table.

### S15. Forethought Life Insurance Company (Global Atlantic) — "SecureFore II Fixed Annuities" product page
- Publisher: Global Atlantic / Forethought Life Insurance Company (Indianapolis, IN)
- Doc type: insurer web page (not a disclosure document)
- URL fetched: https://www.globalatlantic.com/retirement-annuities/fixed-annuities/securefore-ii
- Retrieved: YES (web page)
- Note carried over: withdrawal charge percentages, issue ages, premium minima, death
  benefit and annuitization details were **not** stated on the page.

### S16. Oceanview Life and Annuity Company — "Harbourview Multi-Year Guaranteed Annuity — Product Disclosure", OVLAC-MYGA-DISC Rev. 01/20
- Publisher: Oceanview Life and Annuity Company. A smaller MYGA specialist, not a "major"
  carrier — included because it is a genuine signed **MYGA product disclosure** in the Model
  #245 format, which the majors do not post publicly.
- Doc type: 2-page signed product disclosure with owner/producer signature block
- URL fetched: https://oceanviewlife.com/wp-content/uploads/2020/05/OVLAC-MYGA-DISC.pdf
- Retrieved: YES (full text extracted)

**Dropped (in the research file, not cited here):** S17 (New York Life Secure Term MVA IV
fact sheet via Fidelity — Retrieved: **NO**, HTML interstitial); S18 (American Equity
GuaranteeShield brochure — Retrieved: **NO**, DNS resolution failure); S19 (three
immediateannuities.com brochures — Retrieved: **NO**, HTTP 403). Nothing is asserted from
any of them anywhere in this library.

---

## Regulatory and actuarial references [R#] (product research file numbering)

### R1. NAIC — Model #805, "Standard Nonforfeiture Law for Individual Deferred Annuities" (NAIC Model Laws, Regulations, Guidelines and Other Resources — Fall 2020)
- Publisher: National Association of Insurance Commissioners
- URL fetched: https://content.naic.org/sites/default/files/model-law-805.pdf
- Retrieved: YES (all 5 pages)
- **Correction carried over:** in the retrieved Fall 2020 edition the indexed nonforfeiture
  rate floor is **15 basis points (0.15%)**, not 1%. The corridor is
  `0.15% ≤ i ≤ 3.00%` with `i = round(5-yr CMT, 1/20 of 1%) − 1.25%`. The commonly cited 1%
  floor reflects the 2003 amendment as originally adopted and is **[unverified]**.
- Same document as [REG-R42].

### R2. NAIC — Valuation Manual, Jan. 1, 2026 edition; VM-22: Requirements for Principle-Based Reserves For Non-Variable Annuities
- Publisher: NAIC (© 2025 NAIC). 457-page PDF; VM-22 begins at PDF page 227 (manual page 22-1)
- URL fetched: https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf
- Retrieved: YES (downloaded and text-extracted; VM-22 sections read directly)
- Gaps carried over: VM-22 Table 6.2 (partial withdrawals) was extracted only for the
  **Qualified** column and the attained-age-80-and-over row was truncated; the mandatory
  application date "three years after the effective date" is printed as a rule, not a date,
  so 2029 is arithmetic and carries **[unverified]**.
- Same document as [REG-R36] (and the parent Valuation Manual as [REG-R3]).

### R4. NAIC — Model #245, "Annuity Disclosure Model Regulation" (NAIC Model Laws — Summer 2021)
- Publisher: NAIC
- URL fetched: https://content.naic.org/sites/default/files/model-law-245.pdf
- Retrieved: YES (40 pages; §§1–6 read)
- **Numbering note carried over:** the NAIC Annuity Disclosure Model Regulation is **#245**,
  not #250. (#250 is the Variable Annuity Model Regulation — see [REG-R43].)
- Same document as [REG-R45].

### R5. NAIC — Model #275, "Suitability in Annuity Transactions Model Regulation" (NAIC Model Laws — Spring 2020; the best-interest revision)
- Publisher: NAIC
- URL fetched: https://content.naic.org/sites/default/files/model-law-275.pdf
- Retrieved: YES (20 pages; §§1–6 read)
- Same document as [REG-R46].

### R6. 26 U.S. Code § 72 — "Annuities; certain proceeds of endowment and life insurance contracts" (Cornell Legal Information Institute)
- URL fetched: https://www.law.cornell.edu/uscode/text/26/72
- Retrieved: YES (full section text)
- Same statute as [REG-R55].

### R7. IRS — Rev. Rul. 2002-6, 2002-1 C.B. (Section 807 — Rules for Certain Reserves), used to establish AG 33's identity and effective date
- URL fetched: https://www.irs.gov/pub/irs-drop/rr-02-6.pdf
- Retrieved: YES (3 pages)
- Gap carried over: **the full text of AG 33 was not retrieved.** It is published in the NAIC
  Accounting Practices and Procedures Manual, Appendix C, which is not freely accessible.
  Only AG 33's official title, adoption and effective date are sourced here; its substantive
  mechanics remain **[unverified]**. See also [REG-R39].

### R8. Society of Actuaries Research Institute & LIMRA — "2023-2024 Fixed-Rate Deferred Annuity Surrender Study" (public report), February 2026
- URL fetched: https://www.soa.org/globalassets/assets/files/resources/research-report/2026/2023-24-frda-public-report.pdf
- Retrieved: YES (7 pages — the public highlights report)
- Note carried over: detailed results sit behind the Experience Studies Pro subscription and
  were **not** retrieved; only the qualitative behavioural findings and the exposure
  statistics are cited.
- Related landing page catalogued cross-product as [REG-R63].

### R9. Society of Actuaries — 2012 Individual Annuity Reserving Report & Table; and the 2012 IAM Basic Table on mort.soa.org
- URLs fetched: https://www.soa.org/resources/experience-studies/2011/2012-ind-annuity-reserving-rpt/
  and https://mort.soa.org/ViewTable.aspx?TableIdentity=2581
- Retrieved: YES (web page; table page)
- Related entries in the cross-product library: [REG-R59] (Model #821 + VM-M definitions),
  [REG-R60] (the 2012 IAR development report).

**Dropped (in the research file, not cited here):** R3 (NAIC "Valuation Manual (VM)-22 (A)
Subgroup" committee page — retrieved, but nothing from it is cited; VM-22 facts come from
the manual itself at R2); R10 (SOA "2015-2022 Fixed Rate Deferred Surrender Experience
Study" — Retrieved: **NO**, HTTP 404; nothing asserted from it).

---

## Cross-product regulatory references [REG-R#]

Cited with the [REG-R#] prefix to avoid collision with the product research file's own
R-numbering. **[REG-R#] resolves against a single shared numbering space running R1–R157**,
with **R114–R124 and R143–R149 permanently unused by design** (the block convention lets a
research stream finish with spare numbers so a later pass can extend it without renumbering
anything product documentation already cites). The numbering is curated in
`us/references/regulatory-and-actuarial-references.md`. Research provenance is split across
five files: **R1–R34** (life-origin, several of which also bind annuity models) come from
`us/_research/regulatory-actuarial.md`; **R35–R72** (annuity-specific) come from
`us/_research/regulatory-actuarial-annuities.md`, which also carries the table showing which
of R1–R34 bind annuity models and how; and **R73–R142** (statutory accounting and capital)
come from `us/_research/statutory-accounting.md` (R73–R99),
`us/_research/statutory-reserves.md` (R100–R113) and `us/_research/risk-based-capital.md`
(R125–R142), with the per-entry bibliography at `us/regulatory/sources.md`. **Ids are never
renumbered.** Entries cited by the two documents in this directory:

| Tag | Provenance file | Short title | Retrieval status (per that file) |
|---|---|---|---|
| REG-R2 | life | Standard Nonforfeiture Law for Life Insurance (Model #808) — cited only to record that it does **not** apply to annuities | fetched |
| REG-R16 | life | 26 U.S.C. §807 — tax reserves | fetched |
| REG-R26 | life | ASOP No. 2 — Nonguaranteed Elements for Life Insurance and Annuity Products | fetched |
| REG-R27 | life | ASOP No. 7 — Life or Health Cash Flow Analysis | fetched |
| REG-R29 | life | ASOP No. 22 — Opinions based on asset adequacy analysis | fetched |
| REG-R32 | life | ASOP No. 56 — Modeling | fetched |
| REG-R34 | life | FASB ASU 2018-12 (LDTI) | fetched |
| REG-R36 | annuities | VM-22 — PBR for Non-Variable Annuities (same document as [R2]) | fetched (local text extraction) |
| REG-R37 | annuities | VM-V §1 — statutory maximum valuation interest rates, income annuities | fetched (local text extraction) |
| REG-R39 | annuities | Actuarial Guideline XXXIII (AG 33) | **no** — title verified via REG-R41; mechanics [unverified] |
| REG-R41 | annuities | VM-C — index of actuarial guidelines incorporated into the Valuation Manual | fetched (local text extraction) |
| REG-R42 | annuities | Standard Nonforfeiture Law for Individual Deferred Annuities (Model #805) (same document as [R1]) | fetched (local text extraction) |
| REG-R43 | annuities | Variable Annuity Model Regulation (Model #250) — cited for the #245/#250 numbering correction and the §7.B fixed-account carve-out | fetched (local text extraction) |
| REG-R44 | annuities | Actuarial Guideline LIV (AG 54) — ILVA nonforfeiture; cited for the Model #805 scope boundary | fetched (local text extraction, complete) |
| REG-R45 | annuities | Annuity Disclosure Model Regulation (Model #245) (same document as [R4]) | fetched (local text extraction) |
| REG-R46 | annuities | Suitability in Annuity Transactions Model Regulation (Model #275) (same document as [R5]) | fetched (local text extraction) |
| REG-R49 | annuities | SEC Release 33-11294 — registration for index-linked and **registered MVA** annuities; Form N-4 | fetched via govinfo.gov (sec.gov PDF returned 403); compliance date [unverified] |
| REG-R55 | annuities | 26 U.S.C. §72 (same statute as [R6]) | fetched |
| REG-R56 | annuities | 26 U.S.C. §1035 — exchanges | fetched |
| REG-R59 | annuities | NAIC Model #821 + VM-M annuity mortality definitions (2012 IAM/IAR, Scale G2) | fetched (local text extraction, both) |
| REG-R60 | annuities | 2012 Individual Annuity Reserving Table — AAA/SOA development report | fetched (local text extraction) |
| REG-R61 | annuities | 2020–2024 Individual Payout Annuity Mortality Experience Study | fetched (landing page) |
| REG-R62 | annuities | Fixed Indexed Annuity Policyholder Behavior Experience Studies | fetched (both landing pages); headline shock-lapse split [unverified] |
| REG-R63 | annuities | Fixed Rate Deferred Surrender Experience Studies (2023–24, 2015–2022) | partial (verified via the SOA index REG-R65); quantitative figures [unverified] |
| REG-R64 | annuities | VA contract holder behavior and GLB utilization studies | fetched (2022–24 landing page) |
| REG-R65 | annuities | SOA Individual Annuity Experience Studies — index | fetched |
| REG-R70 | annuities | ASOP No. 54 — Pricing of Life Insurance and Annuity Products | fetched |
| REG-R71 | annuities | ASOP No. 10 — U.S. GAAP for Long-Duration Life, Annuity, and Health Products (Doc. No. 207) | fetched (local text extraction) |

Note on the curated page: `us/references/regulatory-and-actuarial-references.md` carries
**both halves — all of R1–R72** — with the life-origin entries (R1–R34) frozen and the
annuity entries (R35–R72) merged in. Research provenance remains split between
`us/_research/regulatory-actuarial.md` (R1–R34) and
`us/_research/regulatory-actuarial-annuities.md` (R35–R72); the numbering is the same
shared space in every file and is never renumbered.

### Entries added by the "Statutory accounting and capital" section

The entries below are cited by `technical-notes.md`, "Statutory accounting and capital", and
by the corresponding paragraph in `product-spec.md`, "Regulatory context". Id, title,
publisher, URL, access date and fetched marker are carried **verbatim** from
`us/regulatory/sources.md`, which is the per-entry bibliography for that directory and whose
own ground truth is the three research files named above. **No new sources were fetched at
drafting.** Two formatting notes, neither of which changes any id: headings carry the
**`REG-`** prefix used throughout this section, because the shared numbering collides with the
product research file's own `R#` numbering above (this file's `R1` is Model #805; `REG-R1` is
the Standard Valuation Law); and bare `R#` references *inside* a carried-over entry are that
entry's own text and resolve against the **shared [REG-R#] numbering**, not against the `[R#]`
section above.

**Frozen entries (R1–R72) newly cited here.**

### REG-R1. Standard Valuation Law (Model #820)
- **Publisher:** National Association of Insurance Commissioners (NAIC)
- **URL:** https://content.naic.org/sites/default/files/model-law-820.pdf
- **Accessed:** 2026-08-03 · **Fetched:** yes (27-page PDF retrieved and read; re-read for
  the reserves stream at §§3, 4b, 5, 5a, 6, 7, 11, 12)

### REG-R40. Actuarial Guideline XXXV — The Application of the Commissioners Annuity Reserve Method to Equity Indexed Annuities (AG 35)
- **Publisher:** NAIC
- **URL:** none — **no free official standalone text was located.** Exact title verified from
  the VM-C index (page C-2) [R41]; the authoritative text is in the **AP&P Manual Appendix C**.
- **Accessed:** 2026-08-04 (search date; guideline text not retrieved)
- **Fetched:** **no.** Same limit as R39.

**Statutory accounting and capital entries (R73–R142) cited here.**

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

### REG-R81. Statutory Issue Papers Nos. 50, 51, 52 and 110 — the codification record behind SSAP Nos. 50/51/52/56
- **Publisher:** NAIC (AP&P Appendix E; IP 50 finalized June 23, 1998; IP 51 and IP 52
  finalized March 16, 1998; IP 110 finalized September 12, 2000)
- **URLs:**
  - IP 50: https://content.naic.org/sites/default/files/inline-files/050_y.pdf
  - IP 51: https://content.naic.org/sites/default/files/inline-files/051_A.pdf
  - IP 52: https://content.naic.org/sites/default/files/inline-files/052_y.pdf
  - IP 110: https://content.naic.org/sites/default/files/inline-files/110_d.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes, all four (local text extraction; 22 / 26 / 14 / 3 pages)

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

### REG-R88. SAPWG 2026 Spring National Meeting — Meeting Summary Report (March 23, 2026)
- **Publisher:** NAIC Statutory Accounting Principles (E) Working Group
- **URL:** https://content.naic.org/sites/default/files/national_meeting/2026-spnm-summary-e-sapwg.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; 3 pages, read in full)
- **Limit carried forward:** this is the **most recent SAPWG record retrieved**. The 2026
  Summer National Meeting had not been reported on at the access date, and the exposed
  **revised SSAP No. 7** (the intended replacement for INT 23-01) was **not located or read**.

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

### REG-R106. AG 53 Guidance Document — Year-End 2025
- **Publisher:** NAIC, for the Valuation Analysis (E) Working Group (VAWG)
- **URL:** https://content.naic.org/sites/default/files/inline-files/AG-53-guidance-YE-2025%20(1).pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; 5-page document read)

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

Extraction details live in `us/_research/fixed-deferred-annuity.md`: that file records which
facts came from which source, including the [unverified] flags (the Model #805 1% floor, the
Midland rate-to-period mapping, AG 33's mechanics, the pre-2026 content of VM-22, the
absence of a bailout provision, the VM-22 mandatory application date), the failed fetches
(S17, S18, S19, R10), the FIA-not-MYGA caveats on S8/S9, the VA-chassis caveat on S14, and
the "current company practice" caveat on S5/S6. The cross-product bibliographies
`us/_research/regulatory-actuarial.md` (R1–R34),
`us/_research/regulatory-actuarial-annuities.md` (R35–R72),
`us/_research/statutory-accounting.md` (R73–R99), `us/_research/statutory-reserves.md`
(R100–R113) and `us/_research/risk-based-capital.md` (R125–R142) play the same role for
[REG-R#] tags, and `us/regulatory/sources.md` is the per-entry bibliography for R73–R142.
Standardizations marked **[std]** in `product-spec.md` and `technical-notes.md` are
introduced at drafting and are not attributable to any source.
