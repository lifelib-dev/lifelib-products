# Regulatory and Actuarial References — UK Life Insurance

**Status:** Draft, 2026-08-03; extended to cover the Solvency UK capital, reporting,
accounting and tax layer 2026-08-06.

Curated reference library for the UK section of the reference-product library. It
covers the prudential (PRA / Solvency UK), conduct (FCA), legislation-and-tax,
mortality/morbidity (CMI and ONS), professional-standards, and accounting sources that
the reference cash-flow-model implementations (term-assurance / critical-illness /
income-protection / whole-of-life / with-profits / unit-linked-bond / pension-annuity)
rely on. Product folders cite entries on this page as **[REG-R#]** (e.g., `[REG-R1]`);
the R1–R38 numbering below is **frozen** — do not renumber or reuse numbers, as
product documentation cites against it. Within this page, plain `[R#]` refers to the
same entries. Facts drawn from a document that was actually retrieved carry its
number; claims from general knowledge or search-result summaries are tagged
**[unverified]**; failed or unfetched links are disclosed per entry — no URL on this
page is fabricated. All URLs accessed **2026-08-03** unless noted otherwise.

The page is now in two parts:

- **R1–R38** — the original bibliography: prudential, conduct, legislation-and-tax,
  mortality/morbidity, professional standards and accounting frames, accessed
  **2026-08-03**. Sections 1–6. **Frozen.**
- **R39–R120** — the Solvency UK balance sheet and technical provisions, discounting
  and transitionals, the SCR and standard formula, own funds / MCR / ring-fenced funds
  / internal models, regulatory reporting and governance, the statutory accounts and
  tax, and product-level regulatory treatment. Sections 7–14, accessed **2026-08-06**.
  Section 15 records that half's gaps, fetch failures and unverified points.

**Regulatory architecture in one line:** the PRA (Bank of England) sets prudential
requirements under the post-Brexit "Solvency UK" regime (Solvency II as onshored,
then reformed in 2023–24 and restated into the PRA Rulebook at end-2024); the FCA
regulates conduct through its Handbook (COBS/ICOBS/PRIN); both act under FSMA 2000.

**Terminology — what these sources actually measure, and what the file names in
`uk/regulatory/` do *not* mean.** The UK has **no "statutory accounting" in the U.S.
sense**: there is no NAIC-style regulator-mandated accounting basis that is
simultaneously the solvency measurement and the published financial statements, and no
annual statement blank that doubles as the accounting ledger. The file names in
`uk/regulatory/` mirror `us/regulatory/` for structural parity across the library and
for no other reason. What the entries below support is **three separate measurements**
built on one cash flow projection:

| Layer | What it is | Entries |
|---|---|---|
| **Solvency UK regulatory balance sheet** | The prudential measurement — Article-75 valuation, technical provisions = best estimate + risk margin, own funds, SCR, MCR, and the supervisory return | [R1]–[R8], [R39]–[R49], [R54]–[R60b], [R61]–[R73], [R77]–[R83c], [R84]–[R98] |
| **Statutory accounts** | Companies Act 2006 individual accounts under **FRS 102 + FRS 103**, *or* **UK-adopted IFRS 17** — a company-law choice at entity level (s.395 [R103]) | [R38], [R99]–[R107] |
| **Tax** | Not a liability measurement at all — the corporation tax computation built **on the accounts**, with the Finance Act 2012 overlay (BLAGAB I-E, non-BLAGAB trade profit) | [R15]–[R18], [R108]–[R110], [R113] |

**One U.S. framing must not transfer.** The U.S. statutory story — acquisition costs
expensed as incurred, no DAC asset, first-year surplus strain — is **reversed** in the
UK statutory accounts. SI 2008/410 Schedule 3 **para 13 requires** that costs of
acquiring insurance policies incurred in one financial year but relating to a subsequent
one **must be deferred** [R105], and FRS 103 ¶3.7 requires deferral subject to
recoverability, with ¶3.10 barring deferral **for with-profits funds** [R99]. The
Solvency UK balance sheet, by contrast, carries no DAC at all — it is an Article-75
economic balance sheet [R39]. The owning research file titles its section 3 "Acquisition
costs and DAC — the U.S. contrast, reversed"
(`uk/_research/uk-accounting-and-tax.md` §3).

**Scope note on capital — revised 2026-08-06; the earlier note is superseded.** This
note previously said that the SCR and MCR were **cited-not-specified** and that this
library produced only best-estimate liability cash flows. **That is no longer the
position.** `uk/regulatory/` now specifies the capital layer:

- `uk/regulatory/statutory-accounting-and-capital.md` — concepts: what each item is,
  why it exists, which of the seven products it bites, and what a projection must
  produce.
- `uk/regulatory/technical-notes.md` — the calculations: the standard formula SCR
  module by module and its aggregation [R61][R62], the risk margin cost-of-capital
  run-off [R1][R4][R44], the MCR linear formula and the 25%–45% corridor with the
  £3,500,000 absolute floor for long-term business [R78], own funds, tiering and the
  reconciliation reserve [R77], ring-fenced funds and matching adjustment portfolios
  and their notional SCRs [R62][R71][R77][R80], the loss-absorbing capacity
  adjustments [R62], the reporting templates a liability model must populate [R89]–[R91],
  and the accounts and tax layers [R99][R102][R105][R106][R108].
- `uk/regulatory/sources.md` — the per-entry bibliography for that directory, carrying
  the duplicate-records table reproduced below.

**What is still deliberately *not* specified, and must not be inferred from this page.**
No risk-free rate, fundamental spread, volatility adjustment, symmetric adjustment,
ultimate forward rate, convergence period or Smith-Wilson parameter is given anywhere:
those are PRA-published technical information under IRPR reg 3, and the monthly data
files were **not opened** [R44][R54]. The **Annexes to the SCR – Standard Formula Part
were not retrieved** [R73], so the health catastrophe sub-module cannot be computed from
this library. The numbered-line-of-business mapping for critical illness and income
protection remains **[unverified]** — not for want of the list, but because no retrieved
document states the classification (see §15). The counterparty-default
probability-of-default table, the loss-given-default definitions, the concentration
aggregation formula and the ECAI-to-credit-quality-step mapping tables were surveyed,
not transcribed [R62][R72]. IFRS 17 itself was **never read** — it is paywalled [R107] — so every
IFRS 17 paragraph reference on this page is one the UK Endorsement Board quotes in
[R106]. Internal models are specified as a set of *requirements* [R81][R81b], not as a
model.

---

## Numbering — blocks, deliberately-unused numbers, and duplicate records

The six research streams that produced R39–R120 ran **in parallel**, so blocks of
numbers were allocated up front and each stream numbered independently inside its own
block. Two consequences follow, and both are recorded here rather than tidied away.

### Block allocation

| Block | Owning research file (the citation ground truth) | Created | Deliberately unused |
|---|---|---|---|
| **R1–R38** | this page's original bibliography (`uk/_research/regulatory-actuarial.md`) | R1–R38 — **frozen**; already cited by the seven product documents | — |
| **R39–R52** | `uk/_research/solvency-uk-technical-provisions.md` | R39–R49 | **R50, R51, R52** |
| **R53–R60** | `uk/_research/solvency-uk-discounting-and-transitionals.md` | R53–R60, plus the lettered sub-id **R60b** | — |
| **R61–R76** | `uk/_research/solvency-uk-scr-standard-formula.md` | R61–R73 | **R74, R75, R76** |
| **R77–R83** | `uk/_research/solvency-uk-own-funds-mcr-and-internal-models.md` | R77–R83, plus sub-ids R78b, R79b, R80b, R80c, R81b, R81c, R83b, R83c, R83d | — |
| **R84–R98** | `uk/_research/solvency-uk-reporting-governance.md` | R84–R98, plus sub-ids R88b, R88c, R95b, R96b, R97b, R97c | — |
| **R99–R113** | `uk/_research/uk-accounting-and-tax.md` | R99–R113, plus sub-id R102b | — |
| **R114–R133** | `uk/_research/uk-product-regulatory-applicability.md` | R114–R120 | **R121–R133** |

**Numbering gaps: R50, R51, R52, R74, R75, R76 and R121–R133 are unused, not missing.**
The blocks were sized before drafting so that streams could run concurrently without
colliding; three streams finished with spare numbers. **Unused is not the same as
missing:** there is no lost, withheld or pending entry behind any of these numbers, and
nothing was deleted. The invariant is that a number, once allocated, is **never reused
for a different document and never renumbered**, so these gaps stay permanently empty.
Do not back-fill them. New entries continue at **R134**.

### Duplicate records — cite only the left-hand number

Inevitably, several streams retrieved and independently numbered **the same document**.
Following the precedent of the U.S. section — which recorded the R33/R73 overlap rather
than silently resolving it — the duplication is **recorded, not renumbered**. Every
document in this library cites **only** the canonical number; the right-hand numbers
exist in the research files and **must not be cited**. They have no entry on this page.

| Document | **Canonical — cite this** | Also recorded as (do not cite) | Why the second record exists |
|---|---|---|---|
| PRA Rulebook — Valuation Part | **R39** | R111 | The accounting stream read the same Part for Chapter 11 (Deferred Taxes) only |
| PRA Rulebook: Solvency II Instrument 2024 (PRA2024/13 = PS15/24 Appendix 6) | **R42** | R63 | The SCR stream cited the instrument for the as-made text of `SCR-SF 3B6.6(1)` |
| Insurance and Reinsurance Undertakings (Prudential Requirements) Regulations 2023 (SI 2023/1347) | **R44** | R53 | The technical-provisions stream read Part 2 Chapter 2 (risk margin); the discounting stream read Part 2 Chapter 1 (matching adjustment) |
| PRA Rulebook — Surplus Funds Part | **R45** | R79 | Read independently by the technical-provisions stream (the TP boundary) and the own-funds stream (the Tier 1 consequence) |
| SS13/15 — *Solvency II: surplus funds* | **R46** | R79b | Same document: once as the Bank PDF, once as the Rulebook guidance view |
| Commission Delegated Regulation (EU) 2015/35 — assimilated text, **revoked** | **R49** | R66 | The SCR stream additionally retrieved the point-in-time text of Article 142 |
| PRA "Technical information for Solvency II firms" | **R54** | R67 | The SCR stream read the symmetric-adjustment (SAECC) content of the same publication page |
| PRA Rulebook — SCR – Standard Formula Part | **R62** | R112 | The accounting stream read the same Part for Chapter 6 (LACTP / LACDT) only |
| SS15/16 — model drift and standard formula SCR reporting | **R68** | R81c, R97c | Retrieved by three streams; **three** records of one 8-page supervisory statement |
| SS14/15 — *With-profits*, Chapter 2 (ring-fenced funds) | **R71** | R80b | Same chapter, once through the SCR stream and once through the own-funds stream |
| SS1/24 — internal model expectations | **R81b** | R97b | The own-funds stream retrieved the PDF; the governance stream retrieved only the publication page |
| PS18/26 | **R87** | R83d | R87 is a two-document entry (PS15/25 **and** PS18/26); R83d records PS18/26's own-funds chapter alone |

Two of these are worth reading twice, because *retrieval quality* differs between the
records and the canonical entry carries the better one. **R81b** is the SS1/24 PDF read
in full, whereas R97b is the publication page only, its content `[unverified]` beyond a
scope list. **R68 / R81c / R97c** all read the same September 2025 PDF; the extracted
character counts differ slightly (7,699 / 7,512 / 7,332), which is an extraction
artefact, not three documents.

---

## Product-relevance matrices

### Matrix A — the frozen entries (R1–R38)

`x` = load-bearing per the source bibliography's cross-reference table; `(x)` =
qualified, conditional, or background relevance (a qualification carried from that
table, or a product named only in the entry's own product annotation); blank = not
indicated by the source. Column key: TA = term-assurance, CI = critical-illness,
IP = income-protection, WOL = whole-of-life, WP = with-profits, ULB =
unit-linked-bond, PA = pension-annuity.

| R# | Reference (short name) | term-assurance | critical-illness | income-protection | whole-of-life | with-profits | unit-linked-bond | pension-annuity |
|----|------------------------|----------------|------------------|-------------------|---------------|--------------|------------------|-----------------|
| R1 | PRA Rulebook: Technical Provisions | x | x | x | x | x | x | x |
| R2 | PRA Rulebook: Matching Adjustment | | | (x) | | (x) | | x |
| R3 | PRA Rulebook: TMTP | | | | x | x | | x |
| R4 | Risk Margin Regulations 2023 (SI 2023/1346) | (x) | (x) | (x) | (x) | (x) | (x) | x |
| R5 | PS10/24 — MA reform | | | (x) | | x | | x |
| R6 | PS15/24 — assimilated-law restatement | (x) | (x) | (x) | (x) | (x) | (x) | x |
| R7 | PS2/24 — TMTP simplification | | | | (x) | (x) | | x |
| R8 | SS7/18 — matching adjustment | | | (x) | | (x) | | x |
| R9 | FCA COBS 20 — with-profits | | | | (x) | x | | |
| R10 | FCA COBS 21.3 — permitted links | | | | | | x | |
| R11 | FCA ICOBS | x | x | x | | | | |
| R12 | FCA PRIN 2A — Consumer Duty | x | x | (x) | (x) | x | x | (x) |
| R13 | FSMA 2000 | (x) | (x) | (x) | (x) | (x) | (x) | (x) |
| R14 | RAO 2001, Sch 1 Pt II (long-term classes) | x | x | x | x | x | x | x |
| R15 | ITTOIA 2005 Pt 4 Ch 9 (chargeable events) | | | | x | x | x | |
| R16 | HMRC IPTM | | | | x | x | x | |
| R17 | Finance Act 2012 Pt 2 (BLAGAB / I-E) | x | x | x | x | x | x | x |
| R18 | HMRC LAM | (x) | (x) | (x) | (x) | x | x | (x) |
| R19 | Insurance Act 2015 | x | (x) | (x) | | | | |
| R20 | CIDRA 2012 | x | x | x | (x) | | | |
| R21 | Taxation of Pensions Act 2014 | | | | | | | x |
| R22 | CMI — role and access model | x | x | x | x | x | x | x |
| R23 | CMI Guide for Authorised Users | (x) | (x) | (x) | (x) | (x) | (x) | (x) |
| R24 | CMI "92" Series tables | x | | | x | (x) | | (x) |
| R25 | CMI "00" Series tables | x | | | x | | | (x) |
| R26 | CMI "16" Series TA / accelerated CI | x | x | | x | | | |
| R27 | CMI "16" Series PMA16/PFA16 | | | | | | | x |
| R28 | CMI SAPS investigation | | | | | | | x |
| R29 | CMI WP185 — S4 Series | | | | | | | x |
| R30 | CMI_2025 projections model | x | (x) | (x) | x | x | | x |
| R31 | CMI Income Protection investigation | | x | x | | | | |
| R32 | ONS national life tables | x | (x) | (x) | x | (x) | x | x |
| R33 | FRC TAS 100 | x | x | x | x | x | x | x |
| R34 | FRC TAS 200 | x | x | x | x | x | x | x |
| R35 | IFoA APS L1 | (x) | (x) | (x) | (x) | x | (x) | (x) |
| R36 | Proxy modelling validation (BAJ 2024) | (x) | (x) | (x) | (x) | (x) | (x) | x |
| R37 | Model risk: illuminating the black box (BAJ) | (x) | (x) | (x) | (x) | (x) | (x) | (x) |
| R38 | UKEB adoption of IFRS 17 | (x) | (x) | (x) | (x) | (x) | (x) | (x) |

### Matrix B — the Solvency UK capital, reporting, accounting and tax layer (R39–R120)

Marks are carried from the owning research file, **not invented here**: where that file
gives a row in its own "Product applicability" table the row is carried; where it gives
only a "Products:" line for the entry, that line is carried. Where a research file
records a question as unsettled the `?` travels with it.

Key: `x` = the entry directly and materially binds · `(x)` = binds conditionally,
partially, or as a secondary driver · `—` = does not apply, or (for provenance-only and
access-record entries) is not a source for any product · `?` = the retrieved sources do
not settle it · blank = not indicated by the owning file. Column key as Matrix A.

| R# | Reference (short name) | TA | CI | IP | WOL | WP | ULB | PA |
|----|------------------------|----|----|----|-----|----|-----|----|
| R39 | PRA Rulebook: Valuation Part | x | x | x | x | x | x | x |
| R40 | SS38/15 — UK GAAP / Solvency II consistency | (x) | (x) | (x) | (x) | (x) | (x) | (x) |
| R41 | PRA Rulebook: Technical Provisions – Further Requirements | x | x | x | x | x | x | x |
| R42 | PRA Rulebook: Solvency II Instrument 2024 (PRA2024/13) | x | x | x | x | x | x | x |
| R43 | PRA Rulebook: Glossary | x | x | x | x | x | x | x |
| R44 | IRPR Regulations 2023 (SI 2023/1347) | x | x | x | x | x | x | x |
| R45 | PRA Rulebook: Surplus Funds Part | — | — | — | (x) | x | — | (x) |
| R46 | SS13/15 — surplus funds | — | — | — | x | x | — | (x) |
| R47 | SS5/24 — funded reinsurance | | | | (x) | (x) | | x |
| R48 | SS18/16 — longevity risk transfers | | | | (x) | (x) | | x |
| R49 | Delegated Regulation (EU) 2015/35 — **revoked** (provenance) | — | — | — | — | — | — | — |
| R54 | PRA "Technical information for Solvency II firms" | x | x | x | x | x | x | x |
| R55 | SoP1/20 — publication of technical information | x | x | x | x | x | x | x |
| R56 | DLT assessment for January 2026 implementation | (x) | (x) | x | x | x | — | x |
| R57 | PRA Rulebook: Transitional Measures Part (TMIR) | (x) | — | (x) | x | x | (x) | — |
| R58 | SoP2/24 — TMTP and TMIR permissions | (x) | — | (x) | x | x | (x) | x |
| R59 | SS17/15 — transitionals on RFR and TP | (x) | — | (x) | x | x | (x) | x |
| R60 | SoP8/24 — MA and MAIA permissions | — | — | (x) | — | (x) | — | x |
| R60b | PS17/25 — Matching Adjustment Investment Accelerator | — | — | (x) | — | (x) | — | x |
| R61 | PRA Rulebook: SCR – General Provisions | x | x | x | x | x | x | x |
| R62 | PRA Rulebook: SCR – Standard Formula | x | x | x | x | x | x | x |
| R64 | PRA statement 20 Dec 2024 — mass-lapse correction | (x) | (x) | (x) | (x) | (x) | x | — |
| R65 | PRA Rulebook: SCR – Undertaking Specific Parameters | — | — | (x) | — | — | — | (x) |
| R68 | SS15/16 — model drift and standard formula SCR reporting | x | x | x | x | x | x | x |
| R69 | SoP4/24 — capital add-ons | x | x | x | x | x | x | x |
| R70 | SoP11/24 — standard formula adaptations | (x) | (x) | x | (x) | (x) | (x) | x |
| R71 | SS14/15 Ch.2 — the ring-fenced fund regime | — | — | — | (x) | x | — | x |
| R72 | PS12/25 — CRR/SII restatement, ECAI→CQS mapping | (x) | (x) | (x) | (x) | (x) | (x) | x |
| R73 | **Annexes to the SCR – Standard Formula Part (NOT retrieved)** | — | ? | x | — | — | — | — |
| R77 | PRA Rulebook: Own Funds Part | x | x | x | x | x | x | x |
| R78 | PRA Rulebook: Minimum Capital Requirement Part | x | x | x | x | x | x | x |
| R78b | SS4/15 — solvency and minimum capital requirements | x | x | x | x | x | x | x |
| R80 | PRA Rulebook: With-Profits Part (+ RFF glossary terms) | — | — | — | (x) | x | — | (x) |
| R80c | EIOPA Guidelines on ring-fenced funds | — | — | (x) | (x) | x | (x) | (x) |
| R81 | PRA Rulebook: SCR – Internal Models Part | x | x | x | x | x | x | x |
| R81b | SS1/24 — internal model expectations | x | x | x | x | x | x | x |
| R82 | PRA Rulebook: Undertakings in Difficulty Part | x | x | x | x | x | x | x |
| R83 | SS2/15 — own funds | x | x | x | x | x | x | x |
| R83b | SoP10/24 — own funds permissions | x | x | x | x | x | x | x |
| R83c | CP4/26 — own funds updates and fixes (consultation) | x | x | x | x | x | x | x |
| R84 | PRA Rulebook: Reporting Part | x | x | x | x | x | x | x |
| R85 | SS40/15 — reporting and disclosure | x | x | x | x | x | x | x |
| R86 | PS3/24 — reporting and disclosure phase 2 | x | x | x | x | x | x | x |
| R87 | PS15/25 and PS18/26 — post-restatement reporting | x | x | x | x | x | x | x |
| R88 | BoE regulatory reporting hub (templates and LOG files) | x | x | x | x | x | x | x |
| R88b | SoP6/24 — regulatory reporting waivers | x | x | x | x | x | x | x |
| R88c | PRA Solvency UK reporting Q&A (**not policy**) | x | x | x | x | x | x | x |
| R89 | IR.12.01 / IR.12.04 / IR.14.01 instruction files | x | x | x | x | x | x | x |
| R90 | IR.12.05 / IR.12.06 / IR.05.03 / IR.05.10 instruction files | (x) | (x) | (x) | (x) | x | (x) | (x) |
| R91 | MALIR 1–7 / IRR.22.02 / IRR.22.03 instruction files | — | — | (x) | — | (x) | — | x |
| R92 | PRA Rulebook: Conditions Governing Business Part | x | x | x | x | x | x | x |
| R93 | PRA Rulebook: Actuaries Part | x | x | x | x | x | x | x |
| R94 | PRA Rulebook: Insurance SMFs / Allocation of Responsibilities | x | x | x | x | x | x | x |
| R95 | SS19/16 — ORSA | x | x | x | x | x | x | x |
| R95b | SS41/15 — applying EIOPA Set 2 / SoG / ORSA guidelines | x | x | x | x | x | x | x |
| R96 | PRA Rulebook: External Audit Part | x | x | x | x | x | x | x |
| R96b | SS11/16 — external audit of the SFCR | x | x | x | x | x | x | x |
| R97 | SS17/16 — internal models: assessment, change, NEDs | x | x | x | x | x | x | x |
| R98 | PRA Rulebook: Preparations for Solvent Exit (+ SS11/24) | x | x | x | x | x | x | x |
| R99 | FRS 103 *Insurance Contracts* | x | x | x | x | x | (x) | x |
| R100 | Implementation Guidance to FRS 103 | x | x | x | x | x | x | x |
| R101 | FRC library page — FRS 103 (edition register + FRC position) | x | x | x | x | x | x | x |
| R102 | FRS 102 | x | x | x | x | x | x | x |
| R102b | FRC library page — FRS 102 (edition register) | x | x | x | x | x | x | x |
| R103 | Companies Act 2006 Part 15, s.395 (basis choice) | x | x | x | x | x | x | x |
| R104 | Companies Act 2006 Part 23, ss.830 / 833A / 843 | x | x | x | x | x | x | x |
| R105 | SI 2008/410 Schedule 3 (insurance accounts formats) | x | x | x | x | x | (x) | x |
| R106 | UKEB Endorsement Criteria Assessment — IFRS 17 | x | x | x | x | x | x | x |
| R107 | IFRS Foundation IFRS 17 page (**paywall record**) | — | — | — | — | — | — | — |
| R108 | SI 2022/1165 — IFRS 17 tax transitional | x | x | x | x | x | x | x |
| R109 | SI 2022/1164 — FA 2022 Sch 5 Pt 2 commencement | (x) | (x) | (x) | x | x | x | — |
| R110 | GOV.UK published Corporation Tax and Income Tax rates | x | x | x | x | x | x | x |
| R113 | BEIS letter to the FRC (2017) — premise stale | (x) | (x) | (x) | (x) | (x) | (x) | (x) |
| R114 | PRA Rulebook: Investments Part | (x) | (x) | (x) | (x) | x | x | x |
| R115 | FCA Handbook INSPRU 1.2 (disapplied to SII firms) | (x) | (x) | (x) | (x) | (x) | x | (x) |
| R116 | FCA Handbook INSPRU 1.3 (**deleted**) | — | — | — | (x) | x | — | (x) |
| R117 | SS1/14 — mutuality and with-profits funds | — | — | — | (x) | x | — | — |
| R118 | Milliman — *The benefits of Solvency II unit matching* (**secondary**) | — | — | — | (x) | (x) | x | — |
| R119 | SS1/20 — Prudent Person Principle | (x) | (x) | (x) | (x) | x | x | x |
| R120 | SS20/16 — reinsurance counterparty credit risk | x | x | x | (x) | (x) | (x) | x |

**Notes on Matrix B** — every mark that is not self-explanatory, and every place a
research file refused to settle a question:

- **R44 is `x` across the board for two different reasons.** IRPR reg 7B is the statutory
  risk-margin requirement (CoC 4%, λ 0.9 for long-term business, floor 0.25), which binds
  every product and bites hardest on long-duration business — PA, WOL and IP; regs 3–7 are
  the authority for the risk-free curve and the matching adjustment, which is PA-dominant.
  The two chapters were read by different streams (see the duplicate-records table).
- **R49 and R107 are `—` across the board and are not sources for any product.** R49 is a
  **revoked** regulation, recorded as provenance so that a legacy or EU-vintage document
  can be read; R107 is an **access record** showing that IFRS 17's text is paywalled and
  was never read.
- **R64 is `x` for ULB alone.** The 20 December 2024 correction deleted the reference to
  RAO Schedule 1 Part II **class III** (linked long-term) from the 70% mass-lapse limb, so
  a unit-linked bond takes the **40%** limb, not 70%. Nothing in the seven-product set is
  class VII (pension fund management) business, so the 70% limb is inapplicable to all
  seven. PA is `—` because a pension annuity in payment has no discontinuance right.
  **Recorded, not resolved:** the PRA statement's own narrative names class **II** and
  class VII as the transposition-table result, while the corrected rule text as read in
  [R62] names class VII only [R64].
- **R73 is the un-retrieved annex file, deliberately numbered so the gap has a citable
  handle.** IP is `x` and CI is `?` because the health catastrophe sub-module lives
  there. **CI's `?` is the single most consequential unresolved classification in this
  half of the page**: whether standalone and accelerated critical illness are life or
  health obligations rests on a derivation that no retrieved document states — see §15
  [R42][R62][R84].
- **R68, R81, R81b and R97 are `x` across the board but are entity-level.** They bind a
  firm holding a s.138BA internal model permission, not a product; the research records
  that in practice these are PA and large WP/WOL books [R97]. SS15/16's *annual XBRL
  standard-formula submission* is expected only of firms with material **non-life**
  technical provisions, so a life-only UK writer faces the maintain-the-capability
  expectation but not the submission [R68].
- **R69's marks carry no numbers.** SoP4/24 is `x` for all products because a capital
  add-on is an entity-level supervisory measure, but **the PRA's quantitative thresholds
  for a "significant risk profile deviation" were not read out of the retrieved text and
  must not be stated** [R69].
- **R70 is `x` for IP and PA** through the USP revision-risk parameter — the only
  life-relevant USP in the whole Part [R65] — and `(x)` elsewhere through the LACDT
  permission limb, which is entity-level. **No content beyond SoP11/24's scope statement
  was retrieved** [R70].
- **R45 / R46 / R80 / R116 / R117 concentrate on WP by construction.** WOL and PA carry
  `(x)` because a whole-of-life or a deferred annuity **written in participating form
  inside a with-profits fund** is inside the calculation, while the same product written
  as a non-profit contract is not. R46 is `x` for WOL because SS13/15 ¶3.1 names
  whole-of-life policies as the example where the retrospective (asset-share) calculation
  may be negative or significantly lower than the prospective one, so the prospective
  route may be necessary [R46].
- **R71 is `x` for PA without PA being a ring-fenced fund.** A matching adjustment
  portfolio is expressly **not** an RFF on the Glossary definition [R80], but it attracts
  the identical Own Funds 3L deduction and the identical `SCR-SF 9` no-diversification
  treatment [R62][R77].
- **R80c travels with a status caveat.** Every article reference in the EIOPA ring-fenced
  funds guidelines is to the Solvency II Directive and Delegated Regulation (EU) 2015/35 —
  **none of which is the operative UK citation any more** after PS15/24 [R6]. ULB carries
  `(x)` for a *negative* reason: Guideline 2(a)–(b) puts conventional unit-linked and
  index-linked products generally **outside** the scope of ring-fenced funds [R80c].
- **R90's `x` is WP; the other six are `(x)` because the triggers are entity-level, not
  product-level.** IR.12.05 / IR.12.06 are triggered by the firm's with-profits net BEL,
  and any of the other products *written in participating form* falls into the
  with-profits fund and so into the WPBR / FPRL decomposition. IR.05.10's scope test is on
  life premiums **excluding unit-linked premiums**, so a pure unit-linked-bond book cannot
  bring a firm into scope — the owning file marks IR.05.10 `—` for ULB on that ground
  while the with-profits templates keep ULB at `(x)` [R84][R90].
- **R91 is the MA reporting set: `x` for PA, `(x)` for IP and WP.** The `(x)` is the
  **eligible element** route [R2]: the guaranteed element of a with-profits immediate or
  deferred annuity, and the **in-payment element of an income protection policy**, may
  enter an MA portfolio even where the whole contract does not qualify. IP claims in
  payment have their own PRA product code (**524**), which makes the split reportable
  [R89].
- **R99 and R105 are `(x)` for ULB because of the insurance-contract fork.** A unit-linked
  bond frequently fails FRS 103's significant-insurance-risk test and is an **investment
  contract**, falling outside FRS 103 into FRS 102 Sections 11/12 and 23. A bond with a
  material death-benefit uplift can pass. **This is a per-design determination, not a
  product-family fact**, and FRS 103 Appendix II (the definition of an insurance contract)
  **was not read** [R99][R102][R18 LAM01100].
- **R106 is `x` for all seven, but the UKEB's expected measurement model differs by
  product:** GMM for protection and annuities (TA, CI, IP, WOL, PA), **VFA for unit-linked
  and with-profits** (ULB, WP), PAA for short-term contracts [R106 boxed text]. Separately,
  **the coverage-unit basis for an annuity is `?`** — R106 records the point as priority
  issue A of the endorsement assessment, with an IFRS Interpretations Committee Tentative
  Agenda Decision and continuing divergence. The *requirement* to identify coverage units
  binds; **the right answer for an annuity is not settled by the retrieved material**.
- **R109 is `—` for PA and `(x)` for TA/CI/IP.** A UK **pension** annuity is pension
  business, excluded from BLAGAB by FA 2012 s.57(2)(a) and taxed on trade profits, so the
  seven-year acquisition-expense spreading never applied to it. Protection business
  written from 1 January 2013 is likewise outside BLAGAB, but **pre-2013 protection
  back-books continue to be taxed as BLAGAB** unless the LAM14040 election was made —
  hence `(x)` rather than `—` [R17][R18][R109].
- **R113 is `(x)` across the board because its premise is stale.** The 3 February 2017
  BEIS letter interprets a version of SI 2008/410 Sch 3 para 52(3) that contained a
  reference to the Solvency II Directive; the text retrieved on 2026-08-06 contains no
  such reference [R105]. Its *conclusion* — that UK GAAP preparers are not required to
  adopt a Solvency II accounting basis — is independently carried by FRS 103 BC45 [R99].
  **Both records are kept; the tension is recorded, not resolved.**
- **R115 and R118 are legacy/secondary and are marked accordingly.** INSPRU 1.2 is
  **Solvency I** law, expressly disapplied to Solvency II firms, retained because its
  guaranteed-surrender-value floor is the *contrast* that shows Solvency UK has no such
  floor. R118 is a consultancy report cited **only** as evidence of how the market reads
  Investments 4.3 [R114], never as authority for a rule — and **its URL was not preserved
  by the retrieving fetch and is not asserted** [R118].

---

## 1. Prudential — PRA / Solvency UK

### R1. PRA Rulebook — Technical Provisions Part
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.prarulebook.co.uk/pra-rules/technical-provisions
- **Accessed:** 2026-08-03
- **Fetched:** yes (read via browser; prarulebook.co.uk blocks plain fetch with HTTP 403)
- **Annotation:** The operative UK rules for valuing insurance liabilities: technical
  provisions equal a best estimate plus a risk margin (rule 2.4); the best estimate is
  the probability-weighted average of future cash flows discounted at the relevant
  risk-free interest rate term structure, on realistic assumptions, gross of
  reinsurance (rule 3.1); the calculation must be market-consistent (rule 2.3), with
  TP set to market value where cash flows are reliably replicable with market
  instruments (rule 2.5) [R1]. The definitions chapter (as amended 31/12/2024) fixes
  the risk-margin cost-of-capital rate at 4% per regulation 7B(b) of the IRPR
  Regulations (R4) and defines the reference-undertaking basis for the notional SCR
  used in the risk margin [R1]. The single most load-bearing prudential source for
  all seven products: it defines exactly what a "best estimate liability" projection
  must produce.

### R2. PRA Rulebook — Matching Adjustment Part
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.prarulebook.co.uk/pra-rules/matching-adjustment
- **Accessed:** 2026-08-03
- **Fetched:** yes (browser)
- **Annotation:** New Part created by PS10/24 (R5), effective 30 June 2024 (verified
  from rule date-stamps): a firm may not apply an MA to the risk-free curve for the
  best estimate without an MA permission (rule 2.1) [R2]. Verified definitions
  include the MA attestation ("attestation reference date"), "highly predictable"
  cash flows (MA 5.3), and "eligible element" — which now lets the guaranteed element
  of a with-profits immediate/deferred annuity and the in-payment element of an
  income protection policy into an MA portfolio even when the whole contract does not
  qualify [R2]. Definitions added 27/10/2025 implement the Matching Adjustment
  Investment Accelerator (MAIA permission, per PS17/25 [unverified — PS17/25 itself
  not fetched; its existence confirmed on the SS7/18 page, R8]). For a
  pension-annuity model this Part governs which liabilities may be discounted at
  risk-free + MA.

### R3. PRA Rulebook — Transitional Measure on Technical Provisions Part
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.prarulebook.co.uk/pra-rules/transitional-measure-on-technical-provisions/31-12-2024
- **Accessed:** 2026-08-03
- **Fetched:** yes (browser, as-at 31/12/2024 view)
- **Annotation:** The streamlined TMTP regime effective 31 December 2024, with
  verified definitions of "base TMTP" and a "dynamic portion" of designated
  obligations (the simplified calculation replaces the legacy Solvency-I-comparison
  approach [unverified as a characterization of the old method]), referencing back to
  INSPRU 7 as at end-2015 for legacy quantities [R3]. Relevant only to legacy WOL /
  WP / PA back-books written before 2016: a reference model needs to know TMTP exists
  (it adjusts technical provisions, not projected cash flows) but does not need to
  implement it. TMTP runs off fully by 2032 [unverified — per search summaries of
  PS2/24, R7].

### R4. The Insurance and Reinsurance Undertakings (Prudential Requirements) (Risk Margin) Regulations 2023 (SI 2023/1346)
- **Publisher:** legislation.gov.uk (HM Treasury statutory instrument)
- **URL:** https://www.legislation.gov.uk/uksi/2023/1346/made
- **Accessed:** 2026-08-03
- **Fetched:** yes
- **Annotation:** The instrument that delivered the Solvency UK risk-margin cut:
  made 7 December 2023, in force 31 December 2023, it changes the cost-of-capital
  rate from 6% to 4% and introduces a risk-tapering factor lambda of 0.9 for life
  business (1.0 for non-life) with a floor of 0.25 [R4]. This pins the risk-margin
  parameters a UK implementation should carry: cost-of-capital method on the
  reference undertaking's notional SCR, 4% CoC, lambda-tapering of projected SCRs for
  life business. Applies to all products, with the largest proportional effect on
  long-duration business (PA, WOL, IP); the risk-margin projection itself requires an
  SCR runoff — cited-not-specified in this library.
- **Correction note appended 2026-08-06:** the closing words "cited-not-specified in this
  library" are superseded — `uk/regulatory/technical-notes.md` now specifies the
  risk-margin cost-of-capital run-off, with the `SCR(t)` drivers approach carried as
  **[std]** (TPFR 27.4 [R41] is the only gate). See the revised Scope note on capital at
  the head of this page.

### R5. PS10/24 — Review of Solvency II: Reform of the Matching Adjustment
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.bankofengland.co.uk/prudential-regulation/publication/2024/june/review-of-solvency-ii-reform-of-the-matching-adjustment-policy-statement
- **Accessed:** 2026-08-03
- **Fetched:** yes (browser; site 403s plain fetch)
- **Annotation:** The instrument of the mid-2024 MA reforms, published 6 June 2024
  (verified): a new Matching Adjustment Part of the Rulebook (R2); amendments to the
  Technical Provisions, Conditions Governing Business and Glossary Parts; updated
  SS7/18 (R8), SS8/18 (internal-model MA modelling), SS3/17, SS1/20, SS11/16; a new
  Statement of Policy on MA permissions; and reporting changes (MA asset & liability
  information return) [R5]. Reform themes verified from the contents: investment
  flexibility (assets with "highly predictable" cash flows), liability-eligibility
  expansion, credit-rating notching, and the new MA attestation regime [R5].
  Implementation 30 June 2024 with some requirements from 31 December 2024
  [unverified — per search summaries]. PA-dominant; WP and IP at the margins via
  liability eligibility.

### R6. PS15/24 — Review of Solvency II: Restatement of assimilated law
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.bankofengland.co.uk/prudential-regulation/publication/2024/november/review-of-solvency-ii-restatement-of-assimilated-law-policy-statement
- **Accessed:** 2026-08-03
- **Fetched:** yes (browser)
- **Annotation:** Completes Solvency UK: published 15 November 2024 (verified), it
  restates the revoked Solvency II assimilated law (including the Delegated
  Regulation layer) into PRA rules effective 31 December 2024, with verified chapters
  covering Technical Provisions: Risk Margin; Technical Provisions: Further
  requirements; Own funds; Standard Formula restatement; ring-fenced funds;
  governance; disclosure; and groups [R6]. A 20 December 2024 correction fixed the
  mass-lapse life underwriting risk rule (SCR-SF 3B6.6(1)) (verified note on page).
  For implementers: after 31/12/2024 the place to look for detailed TP requirements
  (contract boundaries, expense treatment, homogeneous risk groups) is the PRA
  Rulebook, not EU delegated regulation [the specific location of contract-boundary
  rules within the restated Parts: unverified].

### R7. PS2/24 — Review of Solvency II: Adapting to the UK insurance market
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.bankofengland.co.uk/prudential-regulation/publication/2024/february/review-of-solvency-ii-adapting-to-the-uk-insurance-market-policy-statement
- **Accessed:** 2026-08-03
- **Fetched:** no (URL from search results; not retrieved this session)
- **Annotation:** Published February 2024 [unverified — date per search summaries];
  finalized the TMTP simplification implemented in R3, internal-model streamlining,
  and third-country branch changes, with an accompanying Statement of Policy
  "Permissions for transitional measures on technical provisions and risk-free
  interest rates" effective 31 December 2024 [unverified]. Cited here as the
  provenance of the R3 regime — the operative rules themselves are in R3. Relevant
  to legacy back-books (WOL, WP, PA).

### R8. SS7/18 — Solvency II: Matching adjustment (supervisory statement)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.bankofengland.co.uk/prudential-regulation/publication/2018/solvency-2-matching-adjustment-ss
- **Accessed:** 2026-08-03
- **Fetched:** yes (browser)
- **Annotation:** The load-bearing supervisory statement on MA practice: first
  published 13 July 2018; current version published 23 October 2025, effective
  27 October 2025, updated for the MAIA following PS17/25 (verified from the page)
  [R8]. Verified scope: asset and liability eligibility assessment, demonstrating
  compliance with the matching conditions (the PRA matching tests appear as
  Appendix 1 [unverified — appendix title seen only in search results]), calculation
  of the MA benefit, ongoing portfolio management and compliance, and MA/MAIA
  applications [R8]. For an annuity cash flow model this is where the PRA's
  expectations on cash-flow matching tests live — it directly shapes how asset and
  liability cash flows are projected and compared; WP/IP via eligible elements.

---

## 2. Conduct — FCA

### R9. FCA Handbook COBS 20 — With-profits
- **Publisher:** Financial Conduct Authority
- **URL:** https://handbook.fca.org.uk/handbook/COBS/20/3.html (PPFM section; chapter at /handbook/COBS/20/)
- **Accessed:** 2026-08-03
- **Fetched:** yes (browser; COBS 20.2 and 20.3 read directly)
- **Annotation:** The conduct backbone of UK with-profits business. Verified from
  COBS 20.3: a firm must establish and maintain a PPFM (per fund where appropriate),
  retain five years of versions, distinguish enduring "principles" from shorter-term
  "practices", and — per the COBS 20.3.6 table — cover the methods for determining
  amounts payable, the bonus-setting approach, and smoothing of maturity/surrender
  payments; verified from COBS 20.2: fair-treatment rules address
  shareholder-vs-policyholder conflicts and require fair pay-outs on individual
  policies [R9]. A WP cash flow model's bonus/smoothing/estate logic should be
  parameterized the way a PPFM describes these mechanisms. COBS 20.5 covers
  with-profits governance (WP committees) [unverified — section seen only in search
  results].

### R10. FCA Handbook COBS 21.3 — Further rules for firms engaged in linked long-term insurance business (permitted links)
- **Publisher:** Financial Conduct Authority
- **URL:** https://handbook.fca.org.uk/handbook/COBS/21/3.html
- **Accessed:** 2026-08-03
- **Fetched:** yes (browser)
- **Annotation:** Verified: applies to linked long-term contracts where the
  investment risk is borne by a natural-person policyholder (COBS 21.3.-1); an
  insurer may only link benefits to an approved index or to the listed categories of
  permitted property — approved/listed securities, permitted unlisted securities,
  permitted land and property, loans, deposits, scheme interests, money-market
  instruments, cash, permitted units, stock lending, derivatives, and conditional
  permitted links (COBS 21.3.1R) — classified by economic substance over legal form
  (21.3.1A) [R10]. For a unit-linked-bond model this constrains the fund universe
  and legitimizes unit-price linkage mechanics. PS20/4 (March 2020) widened the
  regime for illiquid assets [unverified — from search results;
  https://www.fca.org.uk/publication/policy/ps20-04.pdf].

### R11. FCA Handbook ICOBS — Insurance: Conduct of Business sourcebook
- **Publisher:** Financial Conduct Authority
- **URL:** https://handbook.fca.org.uk/handbook/ICOBS/1/1.html
- **Accessed:** 2026-08-03
- **Fetched:** yes (browser; ICOBS 1.1 read)
- **Annotation:** Verified: ICOBS applies to distribution, effecting and carrying out
  of **non-investment insurance contracts** (ICOBS 1.1.1R) [R11]. Practical split
  for this library: pure protection business (term assurance, standalone CI, IP) is
  conducted under ICOBS, while investment life business (unit-linked bonds,
  with-profits, pensions) falls under COBS; the glossary definition of "pure
  protection contract" and the firm option to apply COBS to protection sales are
  [unverified] details. Modeling impact is indirect (disclosure/cancellation conduct
  rather than cash flows), so one entry suffices.

### R12. FCA Handbook PRIN 2A — The Consumer Duty
- **Publisher:** Financial Conduct Authority
- **URL:** https://handbook.fca.org.uk/handbook/PRIN/2A/1.html
- **Accessed:** 2026-08-03
- **Fetched:** yes (browser; PRIN 2A.1 read)
- **Annotation:** Verified: the Consumer Duty applies to a firm's retail market
  business, and where it applies, Principles 6 and 7 are disapplied (PRIN 2A.1.3G);
  "product" includes services and "retail customer" includes prospective customers
  [R12]. For modeling, the Duty's price-and-value outcome drives the product-level
  value assessments that actuarial cash flow models increasingly support (e.g.,
  charge levels on ULB, premiums on protection) [the price-and-value outcome
  location PRIN 2A.4: unverified]. Effective for open products from 31 July 2023
  [unverified].

---

## 3. Legislation and tax

### R13. Financial Services and Markets Act 2000 (c. 8)
- **Publisher:** legislation.gov.uk
- **URL:** https://www.legislation.gov.uk/ukpga/2000/8/contents
- **Accessed:** 2026-08-03
- **Fetched:** yes
- **Annotation:** The framework statute. Verified: s.19 general prohibition (no
  regulated activity without authorisation or exemption) and Part 4A permissions
  (s.55A ff.); Part 1A establishes the FCA and PRA and their rule-making powers —
  the statutory hook for every Handbook and Rulebook entry above, including the
  s.138BA permissions used for MA/VA (seen in R1/R2 definitions) [R13]. Cite-only
  for modeling purposes.

### R14. FSMA 2000 (Regulated Activities) Order 2001 (SI 2001/544), Schedule 1 Part II
- **Publisher:** legislation.gov.uk
- **URL:** https://www.legislation.gov.uk/uksi/2001/544/schedule/1
- **Accessed:** 2026-08-03
- **Fetched:** yes
- **Annotation:** The legal taxonomy of UK long-term insurance. Verified classes:
  I Life and annuity; II Marriage and birth; III Linked long term; IV Permanent
  health; V Tontines; VI Capital redemption; VII Pension fund management;
  VIII Collective insurance; IX Social insurance [R14]. Maps this library's product
  set onto the legal classes: TA/WOL/WP → Class I (or III if linked), ULB →
  Class III, IP (and long-duration CI riders) → Class IV, PA → Class I annuities.
  Useful for scoping which contracts are "long-term insurance business" for both
  regulatory permissions and tax.

### R15. Income Tax (Trading and Other Income) Act 2005, Part 4 Chapter 9 — Gains from contracts for life insurance etc.
- **Publisher:** legislation.gov.uk
- **URL:** https://www.legislation.gov.uk/ukpga/2005/5/part/4/chapter/9
- **Accessed:** 2026-08-03
- **Fetched:** yes
- **Annotation:** The chargeable-event-gains regime for policyholder taxation.
  Verified: the chapter covers gains on life policies, annuities and capital
  redemption policies; s.498 requires periodic calculations on part
  surrender/assignment and s.507 sets the calculation method; s.500 treats certain
  loans/payments as part surrenders; top-slicing relief sits at ss.535–538 (presence
  confirmed; full text not read) [R15]. Mechanics [brief, unverified as to exact
  statutory expression]: part surrenders within a cumulative 5%-of-premium annual
  allowance are not immediately taxable — excesses over the allowance and gains on
  full surrender/death/maturity are chargeable event gains taxed as savings income,
  with top-slicing spreading relief. Load-bearing for ULB models (also WOL/WP bonds;
  not qualifying protection policies): the 5% withdrawal pattern is a standard
  policyholder-behavior assumption for UK bonds.

### R16. HMRC Insurance Policyholder Taxation Manual (IPTM)
- **Publisher:** HM Revenue & Customs (GOV.UK)
- **URL:** https://www.gov.uk/hmrc-internal-manuals/insurance-policyholder-taxation-manual
- **Accessed:** 2026-08-03
- **Fetched:** yes (landing/contents)
- **Annotation:** HMRC's working interpretation of R15. Verified: IPTM3000 is the
  chargeable-events section; the manual is the practical reference for the 5%
  allowance arithmetic, insurance years, and top-slicing worked examples [specific
  subsection numbers, e.g. IPTM3500s for part surrenders: unverified]. Secondary
  source — use for mechanics, cite R15 for law.

### R17. Finance Act 2012, Part 2 — Insurance companies carrying on long-term business
- **Publisher:** legislation.gov.uk
- **URL:** https://www.legislation.gov.uk/ukpga/2012/14/part/2
- **Accessed:** 2026-08-03
- **Fetched:** yes
- **Annotation:** The company-level life tax regime. Verified: s.57 defines BLAGAB
  (life assurance business excluding pension business, ISA/CTF business, immediate
  needs annuities, overseas life assurance business, protection business, certain
  reinsurance); s.68 charges corporation tax on the "I-E profit" of BLAGAB (per the
  six-step method in s.73, by reference to amounts credited/debited in the accounts
  per s.70); non-BLAGAB long-term business — notably pension business and post-2012
  protection — is instead taxed on trade profits [R17]. Modeling consequence: for
  BLAGAB products (bonds, WP) policyholder-level tax is effectively borne inside the
  fund, whereas pension and protection business is gross — so a UK cash flow model
  needs a per-product tax-basis flag more than a full tax engine. Basis map:
  ULB/WP/WOL → BLAGAB (I-E); PA and pensions → non-BLAGAB; TA/CI/IP written
  post-2012 → protection business, trade basis.

### R18. HMRC Life Assurance Manual (LAM)
- **Publisher:** HM Revenue & Customs (GOV.UK)
- **URL:** https://www.gov.uk/hmrc-internal-manuals/life-assurance
- **Accessed:** 2026-08-03
- **Fetched:** yes (landing/contents)
- **Annotation:** HMRC's manual on the FA 2012 regime. Verified structure: LAM01000
  introduction; LAM02000–LAM06000 the I-E calculation components; later sections
  cover reinsurance, cross-border and friendly societies; the I-E basis as enacted
  applies from 1 January 2013 [R18]. Secondary source — use for how HMRC applies
  BLAGAB/I-E, cite R17 for law. Product relevance as R17.
- **Correction note appended 2026-08-06 (the annotation above is unchanged; two things
  it relies on have since been settled).** Both come from
  `uk/_research/uk-accounting-and-tax.md`, "Corrections to assumptions the library
  currently carries".
  **(1) The seven-year tax spreading of acquisition expenses is repealed.** FA 2022
  Schedule 5 Part 2 came into force on **1 January 2023** and has effect for accounting
  periods of companies beginning on or after that date; paragraphs 2 and 3 of that Part
  **do not apply** to amounts of acquisition expenses adjusted under FA 2012 s.79 that
  are referable to an accounting period beginning before 1 January 2023, so legacy
  1/7ths continue to run off [R109][R18 LAM04130]. A UK tax projection must therefore
  carry a vintage split, not a single spreading rule. The underlying statutory change is
  to FA 2012 Part 2 [R17].
  **(2) HMRC's rate-incentive statement in LAM01160 is out of date.** LAM01160 states
  that, with corporation tax rates below the basic rate of income tax, attributing more
  profit to trade profit no longer increases the tax charge [R18]. At the 2026-08-06
  access date the CT main rate is **25%** and the income tax basic rate **20%** [R110],
  so the relationship is reversed. Record the incentive as **period-dependent**; do not
  restate HMRC's sentence as current. The LAM's worked examples are stated at 2018 rates
  [R18 LAM01160], which is why [R110] exists as a separate citable rate source.

### R19. Insurance Act 2015 (c. 4)
- **Publisher:** legislation.gov.uk
- **URL:** https://www.legislation.gov.uk/ukpga/2015/4/contents
- **Accessed:** 2026-08-03
- **Fetched:** yes (contents)
- **Annotation:** Verified coverage: duty of fair presentation for non-consumer
  insurance (Part 2) with proportionate remedies in Schedule 1 (deliberate/reckless
  vs other breaches), warranties and terms not relevant to actual loss (Part 3),
  remedies for fraudulent claims including group insurance (Part 4), late payment
  (Part 4A), and contracting-out limits [R19]. Commencement August 2016
  [unverified]. Modeling relevance is via claim outcomes — avoidance/proportionate
  reduction affects claim-severity assumptions on group protection (TA/CI/IP group
  schemes) and non-consumer business — background, not a cash flow driver.

### R20. Consumer Insurance (Disclosure and Representations) Act 2012 (c. 6)
- **Publisher:** legislation.gov.uk
- **URL:** https://www.legislation.gov.uk/ukpga/2012/6/contents
- **Accessed:** 2026-08-03
- **Fetched:** yes (contents)
- **Annotation:** Verified: replaces the consumer duty of disclosure with a duty to
  take reasonable care not to make a misrepresentation; Schedule 1 sets graduated
  insurer remedies for qualifying misrepresentations (deliberate/reckless vs
  careless), with specific provisions for group policies and life insurance [R20].
  Underpins underwriting/claims assumptions for consumer protection products
  (declinature and avoidance rates) — TA, CI, IP, and WOL consumer sales.

### R21. Taxation of Pensions Act 2014 (c. 30)
- **Publisher:** legislation.gov.uk
- **URL:** https://www.legislation.gov.uk/ukpga/2014/30/contents
- **Accessed:** 2026-08-03
- **Fetched:** yes (contents)
- **Annotation:** The "pension freedoms" Act, effective 6 April 2015 (verified).
  Verified changes: flexi-access drawdown, uncrystallised funds pension lump sums
  (UFPLS), relaxed annuity design restrictions, reformed death-benefit taxation, and
  the money-purchase annual allowance mechanics [R21]. Modeling relevance: it
  reshaped the UK annuity market (annuitization is now optional), which drives
  take-up, anti-selection and mortality-basis assumptions for pension-annuity models
  and lapse/transfer behavior in the pension wrappers feeding them.

---

## 4. Mortality and morbidity — CMI and ONS

### R22. Continuous Mortality Investigation — main page (role and access model)
- **Publisher:** Institute and Faculty of Actuaries / CMI Ltd
- **URL:** https://www.actuaries.org.uk/learn-and-develop/continuous-mortality-investigation
- **Accessed:** 2026-08-03
- **Fetched:** yes
- **Annotation:** Verified: the CMI researches mortality and morbidity experience
  from data supplied by UK life offices and consultancies and runs five
  investigations — annuities, assurances (mortality and critical illness), income
  protection, SAPS (pension scheme) mortality, and mortality projections [R22].
  Access model, stated honestly: the CMI is funded by subscriptions; current tables
  and the Projections Model are restricted to Authorised Users (subscribers, plus
  academics/researchers for non-commercial use), while older publications and
  working-paper texts are freely available [R22]. A reference implementation
  therefore documents table *names and structure* from public sources but cannot
  redistribute current qx values — model mortality bases should be [std]
  placeholders shaped like the named tables.

### R23. CMI Guide for Authorised Users (2026)
- **Publisher:** Institute and Faculty of Actuaries / CMI Ltd
- **URL:** https://www.actuaries.org.uk/system/files/field/document/CMI%20Guide%20for%20Authorised%20Users%202026_0.pdf
- **Accessed:** 2026-08-03
- **Fetched:** no (URL from search results; not retrieved)
- **Annotation:** The CMI's own guide to who counts as an Authorised User and how
  outputs are accessed [unverified beyond title/existence]. Cited as the canonical
  statement of the access regime summarized in R22.

### R24. CMI "92" Series tables (AM92/AF92 family)
- **Publisher:** Institute and Faculty of Actuaries / CMI
- **URL:** https://www.actuaries.org.uk/learn-and-develop/continuous-mortality-investigation/cmi-mortality-and-morbidity-tables/92-series-tables
- **Accessed:** 2026-08-03
- **Fetched:** yes
- **Annotation:** Verified table names: assured lives AM92 (males) and AF92
  (females); immediate annuitants IML92/IMA92, IFL92/IFA92; retirement annuitants
  RMV92/RFV92; pensioners PML92/PMA92, PFL92/PFA92; complete set published 30 June
  1999 [R24]. Base experience 1991–94 [unverified]. AM92/AF92 remain the canonical
  *teaching* assured-lives tables (IFoA Formulae and Tables) and the natural
  public-domain-adjacent shape for [std] protection-mortality placeholders, though
  modern pricing uses the "16" Series (R26); the annuitant tables are historical
  context for PA.

### R25. CMI "00" Series tables
- **Publisher:** Institute and Faculty of Actuaries / CMI
- **URL:** https://www.actuaries.org.uk/learn-and-develop/continuous-mortality-investigation/cmi-mortality-and-morbidity-tables/00-series-tables
- **Accessed:** 2026-08-03
- **Fetched:** yes
- **Annotation:** Verified families: permanent assurances AMC00/AMS00/AMN00 and
  AFC00/AFS00/AFN00 (combined/smoker/non-smoker); temporary assurances
  TMC00/TMS00/TMN00, TFC00/TFS00/TFN00; annuitants IML00/IFL00 (immediate),
  RMD00/RMV00/RMC00 and female equivalents (retirement), PPMD00/PPMV00 etc.
  (personal pensioners); pensioners PNMA00/PNFA00 (normal), PEMA00 etc. (early),
  PCMA00/PCFA00 (combined), widows WA00/WL00 [R25]. Base experience 1999–2002
  [unverified]. Shows the naming grammar (product/sex/smoker/select) a UK model's
  mortality-basis interface should mirror; the smoker/non-smoker split first matters
  here for protection pricing.

### R26. CMI "16" Series term assurance mortality and accelerated critical illness tables (IFoA blog announcement)
- **Publisher:** Institute and Faculty of Actuaries (blog; tables by CMI Assurances Committee)
- **URL:** https://blog.actuaries.org.uk/cmi-new-16-series-term-assurance-mortality-and-accelerated-critical-illness-tables/
- **Accessed:** 2026-08-03
- **Fetched:** yes
- **Annotation:** Verified: the "16" Series covers term-assurance mortality
  (including terminal illness) and accelerated critical illness, based on 2015–2018
  experience; proposed with Working Paper 150, finalized with Working Paper 154
  (August 2021); WP151 analyzed CI claims by cause and WP152 covered 2019/2020
  experience; the CMI cautions against mechanical application (sum-assured
  differentials, COVID-19) [R26]. Table names in the family include TMNL16/TFNL16
  [unverified — from search summaries, not the fetched blog]. This is the current
  protection base-table family: a UK term/CI reference model should name-check the
  16 Series and use [std] placeholder rates in its shape (smoker status, select
  period); WOL indirectly.

### R27. CMI briefing note — final "16" Series pension annuity in payment mortality tables
- **Publisher:** Institute and Faculty of Actuaries / CMI Annuities Committee
- **URL:** https://www.actuaries.org.uk/documents/final-16-series-pension-annuitant-mortality-tables-briefing-note-v01-2020-07-10
- **Accessed:** 2026-08-03
- **Fetched:** yes
- **Annotation:** Verified: the "16" Series pension annuity in payment tables
  (PMA16/PFA16) are based on 2015–2018 experience of insured pension annuities — the
  current annuitant base-table family, superseding the "00" and "08" Series lineages
  [the "08" Series interim datasets (e.g. WP101, 2011–2014 data): unverified, from
  search summaries]. A pension-annuity model's base mortality should be expressed
  as a percentage of a named PMA/PFA-style table with a projection overlay (R30).

### R28. CMI Self-Administered Pension Schemes (SAPS) mortality investigation
- **Publisher:** Institute and Faculty of Actuaries / CMI
- **URL:** https://www.actuaries.org.uk/learn-and-develop/continuous-mortality-investigation/cmi-investigations/self-administered-pension-scheme-saps-mortality-investigation
- **Accessed:** 2026-08-03
- **Fetched:** yes
- **Annotation:** Verified series history: S1 (October 2008), S2 (February 2014),
  S3 (December 2018), and the current S4 Series released February 2024 alongside
  Working Paper 185; the latest experience analysis (WP209) covers 2017–2024 on data
  to September 2025 [R28]. S4 tables have an effective date of 1 January 2017 and
  are graduated on 2014–2019 data, deliberately excluding pandemic years
  [unverified — per search summaries of WP181]. SAPS tables are the pension-scheme
  (bulk annuity / DB) counterpart to the insured-annuitant PMA/PFA families and
  include amounts-based and socio-economic variants [unverified]; most relevant to
  bulk purchase annuities / buy-ins.

### R29. CMI Working Paper 185 — final "S4" Series mortality tables
- **Publisher:** Institute and Faculty of Actuaries / CMI SAPS Committee
- **URL:** https://www.actuaries.org.uk/learn-and-develop/continuous-mortality-investigation/cmi-working-papers/self-administered-pension-scheme-mortality/cmi-working-paper-185
- **Accessed:** 2026-08-03
- **Fetched:** no (URL from search results; not retrieved)
- **Annotation:** The release document for the S4 Series (February 2024), read
  together with consultation WP181 [unverified beyond existence/dates from R28 and
  search results]. Cited as the primary anchor for S4; the tables themselves are
  Authorised-User-restricted (R22).

### R30. CMI Mortality Projections Model CMI_2025 (announcement, with Working Paper 211)
- **Publisher:** Institute and Faculty of Actuaries / CMI
- **URL:** https://actuaries.org.uk/news-and-media-releases/news-articles/2026/mar/10-mar-26-cmi-model-shows-further-rise-in-cohort-life-expectancy/
- **Accessed:** 2026-08-03
- **Fetched:** yes
- **Annotation:** Verified: CMI_2025, the current version of the Mortality
  Projections Model, was published in March 2026 with Working Paper 211, calibrated
  to England & Wales population mortality data to 31 December 2025; methodology
  carried over from the restructured CMI_2024 (published June 2025 with WP201, which
  added age/period terms); cohort life expectancy at 65 rose ~8 weeks (M) /
  ~6 weeks (F) vs CMI_2024, and 2025 all-age mortality was a record low, about 2%
  below 2024 [R30]. The model is subscriber-restricted; users are expected to
  adjust core parameters (e.g. the long-term rate, which has no default
  recommendation [unverified]) to their portfolio. Any UK projection basis in this
  library should be expressed as "CMI_20xx with long-term rate p% [std]" — PA
  dominant, also WOL/WP and TA/CI/IP improvement bases.

### R31. CMI Income Protection investigation
- **Publisher:** Institute and Faculty of Actuaries / CMI
- **URL:** https://www.actuaries.org.uk/learn-and-develop/continuous-mortality-investigation/cmi-investigations/income-protection-investigation
- **Accessed:** 2026-08-03
- **Fetched:** no (URL from search results; not retrieved)
- **Annotation:** The CMI's morbidity investigation for individual income
  protection: experience is analyzed as claim inceptions and claim terminations
  (recoveries and deaths) — the structure a multi-state IP cash flow model must
  mirror; current methodology per WP59, with recent experience in WP193 (2017–2020)
  and WP203 (2021–2023) [all unverified — from search-result summaries]. The
  critical-illness counterpart lives in the assurances investigation (R26). Historic
  standard bases (e.g. CMIR12 sickness rates) remain the public teaching reference
  [unverified].

### R32. ONS National life tables (UK series)
- **Publisher:** Office for National Statistics
- **URL:** https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/lifeexpectancies/bulletins/nationallifetablesunitedkingdom/2021to2023
- **Accessed:** 2026-08-03
- **Fetched:** yes
- **Annotation:** The fully public mortality reference. Verified from the fetched
  bulletin: period life tables on three consecutive years of data (2021–2023 release
  published 23 October 2024 covering England & Wales, with UK-level figures
  following — the UK 2021–2023 tables were published 18 March 2025 [unverified, from
  search results]); life expectancy at birth 83.0 (F) / 79.1 (M); datasets
  (including qx by single year of age and sex) are freely downloadable under the
  Open Government Licence [R32]. Because CMI tables are restricted (R22), ONS
  tables are the only redistributable UK mortality source — suitable for [std]
  placeholder bases in reference models, with the caveat that population mortality
  is heavier than insured/annuitant experience.

---

## 5. Professional standards

### R33. FRC Technical Actuarial Standard TAS 100: General Actuarial Standards, v2.0
- **Publisher:** Financial Reporting Council
- **URL:** https://www.frc.org.uk/library/standards-codes-policy/actuarial/tas-100/
- **Accessed:** 2026-08-03
- **Fetched:** yes (standard's FRC page; PDF not read)
- **Annotation:** Verified: v2.0 published 3 March 2023, effective 1 July 2023;
  contains the requirements applying to *all* technical actuarial work, with
  supporting guidance including on Principle 5 (Models) and proportionate
  application [R33]. For this library, TAS 100 is the quality bar a reference cash
  flow model's documentation should meet: justified assumptions, data limitations
  stated, models fit for purpose and communicated with their limitations
  [principle-level detail beyond Principle 5: unverified].

### R34. FRC Technical Actuarial Standard TAS 200: Insurance, v2.0
- **Publisher:** Financial Reporting Council
- **URL:** https://www.frc.org.uk/library/standards-codes-policy/actuarial/tas-200/
- **Accessed:** 2026-08-03
- **Fetched:** yes (standard's FRC page; PDF not read)
- **Annotation:** Verified: v2.0 published 20 September 2024, effective 1 January
  2025; contains the requirements for technical actuarial work in insurance [R34].
  The 2024 revision reflects Consumer Duty implications, insurance transformations,
  audit and assumption-setting, and removes provisions now covered by TAS 100
  [unverified — from FRC/IFoA announcement summaries]. Directly in scope for anyone
  using these reference models for actual reserving or capital work in the UK.

### R35. IFoA APS L1: Duties and Responsibilities of Life Assurance Actuaries, v4.0
- **Publisher:** Institute and Faculty of Actuaries
- **URL:** https://actuaries.org.uk/media/04ujhlcm/aps-l1-version-4-0.pdf
- **Accessed:** 2026-08-03
- **Fetched:** yes (PDF downloaded and read)
- **Annotation:** Verified from the document: version 4.0, effective 2 April 2024;
  sets requirements for Members acting as Chief Actuary (long-term business,
  Solvency II firms), Small Insurer Chief Actuary, With-Profits Actuary, and
  Appropriate Actuary (non-Solvency II firms), including predecessor-discussion and
  standpoint-disclosure obligations and the duty to disclose departures from
  generally accepted actuarial practice [R35]. Explains *who* professionally owns
  the with-profits discretion (R9) and the actuarial-function outputs a cash flow
  model feeds — all products, WP especially.

### R36. Proxy Modelling Working Party — "Consideration of the proxy modelling validation framework"
- **Publisher:** British Actuarial Journal (Cambridge University Press), Vol. 29, 2024
- **URL:** https://www.cambridge.org/core/journals/british-actuarial-journal/article/consideration-of-the-proxy-modelling-validation-framework/B499011B84ACEC53C627C15765D33F4B
- **Accessed:** 2026-08-03
- **Fetched:** yes (abstract/landing)
- **Annotation:** Verified: Wollam, Kuona, Thomson, Liu, Paton and the IFoA Proxy
  Model Working Group; BAJ vol. 29 (2024). Covers calibration (OLS, automated
  selection, penalized regression), scenario selection, eleven validation tests and
  roll-forward practice for the proxy models UK life insurers fit to their "heavy"
  cash flow models, informed by the PRA's 2019 thematic review, with an
  annuity-portfolio case study [R36]. Directly load-bearing here: it defines the
  relationship between a full liability cash flow model (what this library
  specifies) and the proxy layer built on top of it — and thus what outputs the
  heavy model must expose.

### R37. Model Risk Working Party — "Model risk: illuminating the black box"
- **Publisher:** British Actuarial Journal (Cambridge University Press), Vol. 23, 2017/18
- **URL:** https://www.cambridge.org/core/journals/british-actuarial-journal/article/model-risk-illuminating-the-black-box/FD2FD9F9DD86CCB611B4ECEF1421A7AA
- **Accessed:** 2026-08-03
- **Fetched:** yes (abstract/landing)
- **Annotation:** Verified: Black, Tsanakas, Smith et al. (IFoA Model Risk Working
  Party), BAJ vol. 23 (published online 2017). A practical model-risk-management
  framework — governance, model inventory and materiality filtering, risk appetite,
  mitigation and communication — with case studies [R37]. The professional frame
  for documenting model limitations and validating liability cash flow models
  (complements TAS 100 Principle 5, R33).

---

## 6. Accounting frames — why one cash flow model serves several bases

### R38. UK Endorsement Board — IFRS 17 Insurance Contracts (UK adoption)
- **Publisher:** UK Endorsement Board
- **URL:** https://www.endorsement-board.uk/projects/ifrs-17-insurance-contracts/
- **Accessed:** 2026-08-03
- **Fetched:** yes
- **Annotation:** Verified: IFRS 17 (as issued May 2017 and amended June 2020 and
  December 2021) was adopted for UK use on 16 May 2022, effective 1 January 2023,
  replacing IFRS 4; the UKEB committed to a post-implementation review reporting by
  1 January 2028 [R38]. UK-listed and other IFRS-reporting life insurers therefore
  account for all the products in this library under UK-adopted IFRS 17.
- **Correction note appended 2026-08-06 (the annotation above is unchanged; what it
  flagged as unverified is now settled).** The IFRS 17 **mechanics** described in "The
  three measurement bases one projection feeds" below were tagged "[mechanics:
  unverified — general knowledge; standard text not fetched]". They are now **verified
  from [R106]**, the UK Endorsement Board's *Endorsement Criteria Assessment: IFRS 17*,
  whose Section 2 is a systematic description of the standard written by the UK adopting
  body and quoting IFRS 17 paragraph numbers. Two things must be carried forward with
  it. **(a) The UKEB's own expected UK measurement-model mapping**, stated in boxed text
  in R106: **GMM** for "life insurance (protection business), annuity contracts and
  longer-term general insurance"; **VFA** for "unit-linked contracts and with-profits
  contracts"; **PAA** for "short-term general insurance and short-term life contracts"
  [R106]. **(b) The retrieval limit stays.** **IFRS 17 itself was never read — the
  standard text is paywalled [R107].** Every IFRS 17 paragraph number in this library is
  one the UKEB quotes in R106; paragraph text R106 only summarises (notably
  IFRS 17:B101–B106 on direct participation features, the full IFRS 17:33 estimate
  criteria, the modified-retrospective specified modifications in IFRS 17:C6–C19A, and
  disclosure requirements beyond IFRS 17:93) is **not** reproduced and must not be
  invented. No confidence level, no coverage-unit formula and no transition proxy is
  stated anywhere. Separately, and independently of IFRS 17: the FRC's own published
  position is that **"FRS 103 is not aligned with IFRS 17"** and that "Conflicts between
  IFRS 17 and UK company law mean that it is not currently possible to align FRS 103
  with IFRS 17" [R101] — so any drafting implying near-term UK GAAP convergence on
  IFRS 17 is wrong.

### The three measurement bases one projection feeds

**IFRS 17 (UK-adopted).** IFRS 17 measures insurance contracts as fulfilment cash
flows (probability-weighted expected cash flows, discounted, plus an explicit risk
adjustment) plus a contractual service margin releasing profit over coverage, with
the variable fee approach for direct-participation business such as unit-linked and
with-profits [mechanics: unverified — general knowledge; standard text not fetched;
adoption facts per R38]. The expected-cash-flow engine is the same projection a
Solvency UK best estimate needs — differences are in discount rates, risk adjustment
vs risk margin, aggregation (groups/cohorts) and the CSM layer, not in the
underlying per-policy cash flows.

**Solvency UK.** The regulatory balance sheet values liabilities as best estimate
[R1] plus risk margin [R4], discounted at PRA-published risk-free curves, with MA
[R2] for eligible annuity-style business — again the same projected premiums,
claims, expenses and options/guarantees cash flows, with regime-specific
discounting and margins. SCR/MCR capital layers consume the same projections but
are cited-not-specified in this library [R6].

**Tax.** The tax result is computed from statutory accounts with the FA 2012
overlay [R17]: I-E for BLAGAB, trade profit for pension and protection business,
plus policyholder-level chargeable event effects [R15] that shape lapse/withdrawal
behavior. A tax projection is therefore a *consumer* of the same cash flow model
output (income, gains, expenses by fund/business line) rather than a separate
model — which is why the reference implementations keep product cash flows
basis-agnostic and apply basis layers (discounting, margins, tax) as configuration.

**Correction note appended 2026-08-06 — the three paragraphs above are preserved as
written; two statements in them are superseded.** (i) The IFRS 17 paragraph's
"[mechanics: unverified]" tag is discharged by [R106]; see the correction note under R38
and the VFA/GMM mapping recorded there. (ii) The Solvency UK paragraph's closing
sentence — "SCR/MCR capital layers consume the same projections but are
cited-not-specified in this library [R6]" — **is no longer true.** `uk/regulatory/` now
specifies the capital layer: the standard formula module by module [R61][R62], own funds
and tiering [R77], the MCR linear formula and corridor [R78], ring-fenced funds and
matching adjustment portfolios [R71][R77][R80], the loss-absorbing capacity adjustments
[R62], and the reporting the whole thing is delivered through [R84][R89]–[R91]. See the
revised "Scope note on capital" at the head of this page for what remains deliberately
unspecified. (iii) A third correction, not about IFRS 17 at all: **the U.S. "no DAC,
first-year surplus strain" story does not transfer to the UK statutory accounts** — SI
2008/410 Sch 3 para 13 *requires* deferral and FRS 103 ¶3.7 requires deferral subject to
recoverability, with ¶3.10 barring it for with-profits funds [R105][R99]. This is
recorded in `uk/_research/uk-accounting-and-tax.md`, "Corrections to assumptions the
library currently carries", item 2, and set out in full in the header of this page.

---

## 7. Prudential — the Solvency UK balance sheet and technical provisions (R39–R49)

Entries R39–R49 come from `uk/_research/solvency-uk-technical-provisions.md`; **R50, R51
and R52 are unused by design.** All accessed **2026-08-06**. `prarulebook.co.uk` returns
HTTP 403 to plain fetchers, so every Rulebook Part below was read with a browser
User-Agent; the "as at" date segment in a Rulebook URL is the version identifier.

### R39. PRA Rulebook — Valuation Part (as at 05/08/2026)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.prarulebook.co.uk/pra-rules/valuation/05-08-2026
- **Accessed:** 2026-08-06
- **Fetched:** yes (browser User-Agent; present-view URL re-verified 2026-08-06: HTTP
  200, 130,238 bytes)
- **Annotation:** The whole Part was read, Chapters 1 to 12. Verified directly: the
  Article-75 standard in **2.1** — assets at the amount for which they could be
  exchanged, liabilities at the amount for which they could be transferred or settled,
  "between knowledgeable willing parties in an arm's length transaction"; the
  **no-own-credit-standing rule in 2.2**; going concern (3.1); the **scope carve-out in
  4.1** — Chapters 5 to 12 apply to the recognition and valuation of assets and
  liabilities **other than technical provisions**; recognition in conformity with
  UK-adopted international accounting standards (5.1) and valuation under them only where
  consistent with Chapter 2 (5.2, 5.3); the **UK-GAAP derogation in 5.4** with its four
  cumulative conditions; separate valuation of individual assets (5.5) and liabilities
  (5.6); the three-level **valuation hierarchy in 6.1–6.7**; contingent liabilities
  (7.1–7.3); goodwill and intangibles at zero (8.1); related undertakings (9.1–9.6,
  including the adjusted equity method in 9.3); specific liabilities (10.1, 10.2);
  **deferred taxes (11.1–11.3)**; and the excluded methods (12.1–12.7). Chapters 1 and 2
  carry the date-stamp 01/01/2016; Chapters 3 to 12 carry 31/12/2024 — they are the
  restated Delegated-Regulation material. The related-links block lists SS9/14, SS38/15
  [R40] and SS1/20 [R119]. **Duplicate record:** the accounting stream separately
  numbered Chapter 11 (Deferred Taxes) of this same Part as R111 — **cite R39.**
  Governs everything on the balance sheet except technical provisions themselves, for
  all seven products.

### R40. SS38/15 — Solvency II: consistency of UK generally accepted accounting principles with Solvency II (November 2024, updating August 2015)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URLs:** landing page
  https://www.bankofengland.co.uk/prudential-regulation/publication/2015/solvency2-consistency-of-uk-generally-accepted-accounting-principles-with-the-solvency2-directive-ss
  ; PDF read
  https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/supervisory-statement/2024/ss3815-november-2024-update.pdf
- **Accessed:** 2026-08-06
- **Fetched:** yes (PDF text extracted, 11 pages; PDF URL re-verified 2026-08-06: HTTP
  200, 991,592 bytes)
- **Annotation:** The operative mapping between UK GAAP and the Valuation Part [R39].
  Verified directly: ¶1.5 restates the Valuation 5.4 derogation as three conditions;
  ¶1.6 — where UK GAAP and IFRS are consistent the PRA expects the derogation **not** to
  apply; ¶1.7 — supporting evidence for conditions 2 and 3 is expected to go to the
  supervisor before use; ¶1.8 — the derogation relates to Valuation 5.1 and 5.2, applies
  to **the whole of Valuation 6**, applies to the *first sentence only* of Valuation 10.1
  (the second sentence restates Valuation 2.2 and "cannot be derogated"), does **not**
  apply to Valuation 10.2, and applies to **Valuation 11.1 but not 11.2 or 11.3**; ¶1.10
  — most UK-GAAP/IFRS differences for insurers are disclosure-level, so the derogation is
  expected to have limited effect. The §2 table gives a standard-by-standard verdict; the
  two rows that matter for a life model are **FRS 102 Chapters 11 and 12 — "Yes, with
  amendments"** and **FRS 103 — "No", because "Chapters 2 to 14 of the Technical
  Provisions, the Technical Provisions – Further Requirements and the Matching Adjustment
  Parts of the PRA Rulebook still apply."** That row is the cleanest statement in the
  retrieved corpus that **FRS 103 insurance-contract measurement is never a permitted
  substitute for the Solvency UK technical provisions.** The November 2024 annex records
  that the update only re-pointed references from DR (EU) 2015/35 to PRA Rulebook rules
  and did **not** refresh the underlying UK-GAAP/IFRS analysis.

### R41. PRA Rulebook — Technical Provisions – Further Requirements Part (as at 05/08/2026), including Annex 1
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.prarulebook.co.uk/pra-rules/technical-provisions-further-requirements/05-08-2026
  (the slug uses single hyphens; the `---` variant returns HTTP 404)
- **Accessed:** 2026-08-06
- **Fetched:** yes (browser User-Agent; re-verified 2026-08-06: HTTP 200, 259,991 bytes)
- **Annotation:** **The single most load-bearing new source in this half of the page** —
  where the operative detail of DR (EU) 2015/35 Articles 17–61 now lives. Read in full:
  Chapter 1 (Application), 2 (Recognition and Derecognition), **3 (Boundary of an
  Insurance or Reinsurance Contract, 3.1–3.7)**, 4 (Data), 5 (Limitations of Data), 6
  (Approximations), 7 (Assumptions), **8 (Future Management Actions)**, 9 (Future
  Discretionary Benefits), 10 (Separate Calculation of FDB), **11 (Policyholder
  Behaviour)**, 12 (Credibility of Information), **13 (Cash-Flows — the eight-item
  in-scope list)**, 14 (Expected Future Developments), 15 (Uncertainty of Cash-Flows),
  **16 (Expenses)**, 17 (Contractual Options and Financial Guarantees), 18 (Currency), 19
  (Calculation Methods), **20 (Homogeneous Risk Groups)**, 21 (General Insurance
  Obligations), **22 (Technical Provisions calculated as a whole)**, 23 (Recoverables),
  **24 (Counterparty Default Adjustment)**, 25 (Currencies Pegged to the Euro), **26
  (Lines of Business)**, **27 (Proportionality)**, and **Annex 1 Parts A–E (lines of
  business 1–36)**. Every rule carries the effective date **31/12/2024** and the Part has
  only one history date — it is wholly new. Its only "Related links" entry is PS15/24
  [R6]. **Note what is absent:** the Part contains **no risk-margin simplification, no
  simplified counterparty-default adjustment and no simplified recoverables
  calculation**; the heading "SIMPLIFICATIONS" introduces Chapter 27 (Proportionality)
  alone. Compare the block of simplifications listed in the revoked Delegated Regulation
  [R49].

### R42. PRA Rulebook: Solvency II Instrument 2024 (PRA2024/13) — Appendix 6 to PS15/24
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/policy-statement/2024/november/ps1524app6.pdf
- **Accessed:** 2026-08-06
- **Fetched:** yes (PDF, 250 pages, text extracted ~681 KB; URL re-verified 2026-08-06:
  HTTP 200, 1,780,845 bytes)
- **Annotation:** Numbered separately from **[R6]** (the PS15/24 policy statement, frozen)
  because it is a distinct legal instrument with its own citation and is the document a
  drafter must cite for the *text* of the restated rules. Verified directly: made under
  FSMA ss.137G, 137T and 192J; the Annex table maps Parts to annexes — **Technical
  Provisions = Annex R, Technical Provisions – Further Requirements = Annex S, Valuation
  = Annex W**, with Glossary A, Actuaries B, Conditions Governing Business C, External
  Audit D, Matching Adjustment J, MCR K, Own Funds L and M, SCR – Standard Formula O,
  SCR – USP P, Surplus Funds Q, Third Country Branches T, Transitional Measures U,
  Undertakings in Difficulty V; **commencement 31 December 2024, except Annex M (Own
  Funds) which comes into force 2 January 2026**; made by order of the Prudential
  Regulation Committee on **5 November 2024**. A header note on page 1 records that
  **SCR – Standard Formula 3B6.6(1) was subsequently amended** to correct an error (the
  mass-lapse correction, [R64]). Also verified from the instrument text: the restated
  **SCR – Standard Formula 3.3A** scenario rules — under 3.3A(1) a scenario "does not
  change the amount of the risk margin included in technical provisions", "does not
  change the value of deferred tax assets and liabilities", "does not change the value of
  future discretionary benefits included in technical provisions", and assumes "no
  management actions are taken by the firm during the scenario"; 3.3A(2) requires the
  post-scenario technical provisions to allow for future management actions complying
  with TPFR 8 [R41] and for any material adverse impact on option take-up; 3.3A(3)
  permits simplified methods subject to a no-material-misstatement test; 3.3A(5) floors
  the scenario impact at zero where the scenario would *increase* basic own funds.
  **Duplicate record:** numbered R63 by the SCR stream — **cite R42.** Do not cite the
  instrument for the current wording of any rule; cite the as-at Rulebook view.

### R43. PRA Rulebook — Glossary (as at 05/08/2026)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.prarulebook.co.uk/glossary (re-verified 2026-08-06: HTTP 200,
  76,049 bytes; `/pra-rules/glossary` is a 404)
- **Accessed:** 2026-08-06
- **Fetched:** yes (browser User-Agent, printable per-letter views). **Retrieval limit:**
  the per-letter exports actually read (letters B, E, F, M, R, T, V) were retrieved in an
  earlier session and **their exact query URLs were not preserved** — treat the base URL
  as the citation and the letter views as navigation.
- **Annotation:** Supplies the defined terms on which every rule in [R1] and [R41] turns.
  Verified definitions include: *best estimate* (calculated in accordance with Technical
  Provisions 3, 01/01/2016); *risk margin* ("the portion of technical provisions
  calculated in accordance with Technical Provisions 4A and 4B", 31/12/2024 — pointing at
  the **new** chapters, not the old Chapter 4); *technical provisions*; *future
  discretionary benefits* (31/12/2024, a two-limb test); *basic relevant risk-free
  interest rate term structure* (the relevant curve **without** MA, VA or the risk-free
  transitional, 30/06/2024); *relevant risk-free interest rate term structure*
  (31/12/2024, pointing at Technical Provisions 5 and 8, the Matching Adjustment Part,
  the TPFR Part, Transitional Measures 10.2, and PRA technical information under IRPR
  reg 3(1)); *matching adjustment*; *volatility adjustment*; *risk-free interest rate
  transitional measure*; *risk-mitigation techniques*; *market value* ("the market value
  as determined in accordance with generally accepted accounting practice" — a
  **UK-GAAP-anchored** definition that sits oddly beside the Article-75 standard in
  Valuation 2.1, **recorded not resolved**); *expense risk* (30/06/2024); *eligible own
  funds*; *exceptional adverse situation*. The Glossary definition of **"surplus funds"
  itself could not be retrieved** (letter S was not retrievable in the session that read
  the Surplus Funds Part) [R45].

### R44. The Insurance and Reinsurance Undertakings (Prudential Requirements) Regulations 2023 (SI 2023/1347) — the "IRPR Regulations"
- **Publisher:** legislation.gov.uk (HM Treasury statutory instrument), as-amended view
- **URL:** https://www.legislation.gov.uk/uksi/2023/1347/contents (re-verified
  2026-08-06: HTTP 200; the discounting stream used
  https://www.legislation.gov.uk/uksi/2023/1347)
- **Accessed:** 2026-08-06
- **Fetched:** yes. **Read in two passes by two streams:** Part 2 Chapter 1 (matching
  adjustment) read in full; Part 2 Chapter 2 (risk margin) read for regulations 7A–7C.
- **Annotation:** The statutory backbone the PRA Rulebook refers to throughout.
  **Distinct from [R4]**, which is SI 2023/**1346**, the Risk Margin Regulations.
  Verified directly: made 7 December 2023, laid 8 December 2023, under FSMA 2023 ss.4,
  84(2) and 86(5); reg 1(2) — in force "for the purposes of regulation 7 on 1st April
  2024 and for all other purposes on 30th June 2024"; **Part 2 Chapter 2 (regulations 7A,
  7B, 7C) was inserted by SI 2024/1083**. **Reg 3(1)** — the PRA must publish, *every
  quarter*, a fundamental spread for each currency, duration, credit quality and asset
  class it considers appropriate, plus such other information as it considers appropriate
  relating to technical provisions and the standard-formula SCR: this is the authority
  for the curve every liability is discounted on [R54][R55]. **Regs 4(2)–(11)** — the PRA
  *must* grant an MA application where the conditions in (3)–(9) and (11) are met (asset
  assignment; assessable credit quality; maintenance over the lifetime; separate
  identification, organisation and management; cash-flow replication in the same
  currency; immateriality of mismatch; fixed asset cash flows subject to three
  carve-outs; and compliance with s.138BA FSMA). **Reg 5** — the MA calculation. **Reg
  6** — the fundamental spread, including the 30%/35% long-term-average-spread floors,
  the 30% recovery assumption and the 30-year data window. **Reg 7** — the rule-making
  powers under which the Matching Adjustment Part adds conditions, the breach reduction,
  notching and the two fundamental-spread additions. **Regulation 7B** is the statutory
  risk-margin requirement: calculated "for the whole portfolio of insurance and
  reinsurance obligations" per the prescribed formula, with (b) CoC = **4%**, (d) SCR(t)
  = the SCR of the reference undertaking after t years, (e) λ = **0.9 for long-term** and
  **1.0 for general** obligations, (g) λ_floor = **0.25**, and (h) r(t+1) = the basic
  relevant risk-free rate for maturity t+1. **Reg 7C** preserves the PRA's s.137G power
  to permit simplified risk-margin methods. Two retrieval facts travel with this entry.
  **(i) The formula itself is an image on legislation.gov.uk and came back empty from
  text extraction** — the transcribed formula in the research file comes from Technical
  Provisions 4A.1 [R1], which the Rulebook renders as LaTeX. **(ii) SI 2024/1083 was not
  separately fetched** (its URL verified HTTP 200 but not read); everything recorded about
  it comes from the textual-amendment notes inside R44 — including a note that reads
  "1.11.2024 for specified purposes and **31.12.20204** otherwise", *a typographical error
  in the legislation.gov.uk amendment note as displayed; the intended date is plainly
  31.12.2024, recorded here as printed rather than silently corrected*. **Duplicate
  record:** numbered R53 by the discounting stream — **cite R44.**

### R45. PRA Rulebook — Surplus Funds Part (as at 05/08/2026)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.prarulebook.co.uk/pra-rules/surplus-funds/05-08-2026 (re-verified
  2026-08-06: HTTP 200, 82,668 bytes)
- **Accessed:** 2026-08-06
- **Fetched:** yes (browser User-Agent; Chapters 1–4 read in full)
- **Annotation:** The **only** carve-out from the "all payments to policyholders,
  including future discretionary bonuses" rule in Technical Provisions 9.1(3) [R1].
  Verified directly: 1.1 applies to a UK Solvency II firm carrying on with-profits
  insurance business; 1.2 defines *with-profits assets* ("the assets in a with-profits
  fund except those meeting liabilities in respect of non-profit insurance", 31/12/2024);
  **2.1** — a firm "shall not treat surplus funds as insurance and reinsurance
  obligations when valuing payments to policyholders and beneficiaries in the calculation
  of technical provisions in accordance with Technical Provisions 2"; 3.1 gives the
  five-limb surplus-funds calculation, **per with-profits fund** (with-profits assets,
  less with-profits policy liabilities, less tax and other costs on future shareholder
  transfers, less other attributable liabilities, less the value of future shareholder
  transfers); **3.2** makes the **retrospective** asset-share-style calculation in 3.3 the
  default and the **prospective** calculation in 3.4 the fallback where the retrospective
  one "does not adequately reflect the value" or is impracticable; 3.3 lists the ten
  retrospective roll-up items; 3.4 lists the six prospective present-value items; 3.5
  admits guaranteed benefits (including guaranteed surrender and paid-up values),
  contractually-entitled declared bonuses, and future discretionary additions only to the
  extent consistent with what the retrospective calculation would have produced; 3.6 bars
  any charge not permitted by the FCA Handbook [R9]; **4.1** requires the surplus-funds
  valuations to be consistent with the technical-provisions methodology under Technical
  Provisions 2. All substantive rules carry 01/01/2016 except the 1.2 definition — the
  Part was **not** rewritten by PS15/24 [R6]. **The Glossary definition of "surplus
  funds" itself could not be retrieved** [R43]. **Duplicate record:** numbered R79 by the
  own-funds stream — **cite R45.**

### R46. SS13/15 — Solvency II: surplus funds (November 2024, updating March 2015)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URLs:** landing page
  https://www.bankofengland.co.uk/prudential-regulation/publication/2015/solvency2-surplus-funds-ss
  ; PDF read
  https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/supervisory-statement/2024/ss1315-november-2024-update.pdf
  ; also rendered as Rulebook guidance at
  https://www.prarulebook.co.uk/guidance/supervisory-statements/ss13-15---solvency-ii-surplus-funds/05-08-2026
- **Accessed:** 2026-08-06
- **Fetched:** yes (PDF text extracted, 7 pages; the Rulebook guidance view was read
  independently by a second stream)
- **Annotation:** Verified directly: ¶2.1 states the interaction expressly — Technical
  Provisions 9.1(3) requires all payments to policyholders including future discretionary
  bonuses to be in technical provisions "unless those payments constitute surplus funds
  that fall within Surplus Funds 2.1", and Surplus Funds 2.1 excludes them only where they
  meet the **Tier 1 own funds** requirements in Own Funds 3.1 [R77]; ¶2.3 — the PRA
  expects surplus funds normally to meet the Tier 1 criteria but warns they are "likely to
  be treated as part of a ring-fenced [fund]"; **¶2.4 — the surplus-funds calculation
  "does not refer to or include a risk margin"**, which does not relieve the firm of
  calculating the risk margin on its business as a whole including with-profits business;
  **¶3.1 — whole-of-life policies**, or policies where the retrospective result "might be
  negative or significantly lower than the value calculated using the prospective
  approach", are examples where the prospective approach may be necessary; ¶3.2 grouping
  conditions; ¶3.3 groupings must be reassessed each time surplus funds are calculated;
  ¶3.4 defines "permanent enhancements" as amounts expected to be permanent "in all but
  the most extreme adverse circumstances"; ¶3.5 defines "miscellaneous surplus" as
  fund-experience surplus or deficit including profits or losses from non-profit business
  inside the with-profits fund; **¶3.6 — the PRA would not expect a firm to include estate
  distributions in benefits payable** for the prospective calculation. ¶2.2 is [DELETED].
  **Duplicate record:** the Rulebook-guidance retrieval is numbered R79b — **cite R46.**

### R47. SS5/24 — Funded reinsurance (October 2025, updating November 2024)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/supervisory-statement/2025/ss524-october-2025.pdf
  (re-verified 2026-08-06: HTTP 200, 370,064 bytes)
- **Accessed:** 2026-08-06
- **Fetched:** yes (PDF text extracted). **Read for its technical-provisions interface
  only** — the risk-management, collateral and internal-model content was not
  transcribed.
- **Annotation:** Verified directly: ¶1.7 tells firms to read it with "Chapter 3 of the
  Conditions Governing Business, **Chapters 6, 7 and 11 of the Technical Provisions**,
  the Solvency Capital Requirement – General Provisions, and the Solvency Capital
  Requirement – Internal Models Parts", plus SS20/16 [R120], SS7/18 [R8], SS8/18 and
  SS1/20 [R119] — **a stale cross-reference**, since Technical Provisions Chapters 6 and
  7 are [Deleted] as at 30/06/2024 [R1] and only Chapter 11 (Recoverables from
  Reinsurance Contracts and ISPVs) is live. **Recorded, not resolved.** Also verified: the
  PRA expects firms to calculate an **"immediate recapture" metric** assuming immediate
  recapture of all business ceded to a counterparty, ignoring the likelihood of the event,
  used **only** for setting internal investment limits and "not for other purposes,
  including to a firm's recapture plan or collateral policy" (¶2.4–¶2.5); firms assuming
  recapture into an MA portfolio must assume a "worst-case" compliant collateral portfolio
  (¶2.7) and must not assume further permissions would be in place at the point of
  recapture (¶2.7A). The operative point for a liability model: recapture risk is **not** a
  best-estimate cash-flow item — it feeds risk management and the counterparty-default
  adjustment, which TPFR 24 requires to be computed separately [R41].

### R48. SS18/16 — Solvency II: longevity risk transfers (November 2024, updating January 2020)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URLs:** landing page
  https://www.bankofengland.co.uk/prudential-regulation/publication/2016/solvency2-longevity-risk-transfers-ss
  ; PDF read
  https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/supervisory-statement/2024/ss1816-november-2024-update.pdf
- **Accessed:** 2026-08-06
- **Fetched:** yes (PDF text extracted). **Read only in part** — grep-level reading for
  the technical-provisions and counterparty-default interface; the transaction-structuring
  and pre-notification content was not transcribed.
- **Annotation:** The companion to [R47] for longevity swaps and reinsurance of annuity
  longevity risk. **Verified:** the statement observes that holding capital under the SCR
  for counterparty default risk "may not be sufficient in and of itself" — the PRA does
  not treat the SCR counterparty-default module as a substitute for a properly calculated
  TPFR 24 counterparty-default adjustment or for collateral and structuring controls.
  **Everything else about this SS is [unverified] here and should be re-read before it is
  cited for anything more.** Its ¶2.1 refers readers to SS20/16 [R120].

### R49. Commission Delegated Regulation (EU) 2015/35 — assimilated text, marked "(revoked)"
- **Publisher:** legislation.gov.uk (assimilated EU law)
- **URLs:** contents https://www.legislation.gov.uk/eur/2015/35/contents ; Article 1
  (definitions) https://www.legislation.gov.uk/eur/2015/35/article/1 ; Article 142
  (lapse risk sub-module), latest and point-in-time views,
  https://www.legislation.gov.uk/eur/2015/35/article/142 (all re-verified 2026-08-06:
  HTTP 200)
- **Accessed:** 2026-08-06
- **Fetched:** yes (table of contents, Article 1 and Article 142 read; **the remaining
  article bodies were not read**)
- **Annotation:** Recorded as a **negative / provenance** source. **This Regulation is
  revoked and is NOT operative UK law.** The title line reads "…(**revoked**)", the page
  states it is "up to date with all changes known to be in force on or before 04 August
  2026", and the revocation annotation reads "Regulation revoked (**30.6.2024** for the
  revocation of Arts. 52-54; **31.12.2024** in so far as not already in force)" — by
  s.1(1) of and Schedule 1 to the Financial Services and Markets Act 2023, as the
  explanatory note to [R4] records. Verified from the table of contents: Article 37
  "Calculation of the risk margin", Article 39 (cost-of-capital rate), Article 57
  "Simplified calculation of recoverables…", **Article 58 "Simplified calculation of the
  risk margin"**, Article 59, Article 60, Article 61 "Simplified calculation of the
  counterparty default adjustment" — **the block of simplifications that was not carried
  into the TPFR Part** [R41][R42]. Verified from Article 1: the **EPIFP** definition —
  "the expected present value of future cash flows which result from the inclusion in
  technical provisions of premiums relating to existing insurance and reinsurance
  contracts that are expected to be received in the future, but that may not be received
  for any reason, other than because the insured event has occurred, regardless of the
  legal or contractual rights of the policyholder to discontinue the policy." **This is
  the only retrieved text of that definition, and it sits in revoked law** — and EPIFP
  has since been removed from all Solvency UK reporting and disclosure [R86]. Verified
  from Article 142 (the SCR cross-check): ¶1 the lapse capital requirement is the
  **largest** of up/down/mass; ¶2 **+50%** relative to option exercise rates capped at
  100%; ¶3 **−50%** relative capped at **20 percentage points**; ¶4–5 the definition of
  "relevant options"; ¶6(a) **70%** discontinuance for Directive Art. 2(3)(b)(iii)–(iv)
  business, ¶6(b) **40%** for all other policies, ¶6(c) **40%** decrease in future
  contracts under reinsurance treaties; ¶7 the "same scenario" tie-break. **Every one of
  those numbers matches the restated PRA rule 3B6 exactly** — the only substantive change
  is the UK's identification of the 70% business population [R64]. **Duplicate record:**
  the Article 142 point-in-time retrieval is numbered R66 — **cite R49.** Cite this entry
  only to explain what a legacy or EU-vintage document is referring to.

---

## 8. Prudential — discounting, the matching adjustment permissions layer, and transitionals (R54–R60b)

Entries from `uk/_research/solvency-uk-discounting-and-transitionals.md`, block R53–R60
plus the lettered sub-id R60b. **R53 has no entry here**: it is that stream's number for
the IRPR Regulations 2023, which are entered above as **[R44]** — cite R44. All accessed
**2026-08-06**.

### R54. Bank of England / PRA — Technical information for Solvency II firms
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.bankofengland.co.uk/prudential-regulation/key-initiatives/solvency-ii/technical-information
- **Accessed:** 2026-08-06
- **Fetched:** yes (page text retrieved with a browser User-Agent; the site 403s plain
  fetchers). **The monthly XLSX data files themselves were NOT opened, and the SAECC
  spreadsheet was not retrieved — no risk-free rate, fundamental spread, volatility
  adjustment or symmetric adjustment value is stated anywhere in this library.**
- **Annotation:** The page through which the PRA discharges IRPR reg 3 [R44]. Verified:
  technical information comprises risk-free rate term structures, fundamental spreads for
  the MA, volatility adjustments per relevant national market, and the symmetric
  adjustment to the equity capital charge (SAECC). Publication is **monthly, on or before
  the eighth working day of the following month**; each release contains four files —
  *Risk-free curves*, *Risk-free Volatility Adjustment portfolios*, *Smith-Wilson
  extrapolation parameters*, and *Risk-free Fundamental Spreads, Probability of Default
  and Cost of Downgrade*. The release index was verified as running to **30 June 2026
  (published 8 July 2026)** at the access date. Verified UK-specific parameters: **from 31
  July 2021 the GBP RFR is based on SONIA overnight index swap rates with a zero credit
  risk adjustment**; USD moved to SOFR swaps with zero CRA from 1 January 2023; the EUR
  CRA from 1 January 2022 uses Euribor and €STR data. **From 1 January 2025 the PRA
  publishes technical information only for GBP, USD, EUR and CAD** (AUD, DKK, SEK and NOK
  ceased after 31 December 2024). CRA "Method 3" was reset from 1 October 2023 to a **15bp
  upward adjustment to the uncapped Euro CRA, constrained to the range 10–35bp**, and the
  PRA states it is not currently used for any PRA relevant currency. VA reference
  portfolios are **updated on 31 March each year**; the PRA disclosed a data error in the
  unit-linked reduction factors used before the 31 March 2026 update, estimated to have
  **overstated published VAs by up to 5bp for GBP and up to 1bp for other currencies**,
  corrected **prospectively only** with no restatement. Two further 2026 changes: removal
  of unit-linked reduction factors for non-GBP currencies, and **exclusion of MA-eligible
  life annuity liabilities from the GBP VA reference portfolio**. On the same page and
  separately verified: the PRA publishes the **SAECC monthly**, "based on movements in
  **four major equity indices over the preceding 36 months**"; as a temporary measure UK
  insurers used the EIOPA SAECC for valuations from **31 December 2020 to 30 March 2021**,
  and from **31 March 2021** should use the PRA spreadsheet based on UK insurers'
  exposures, which also restates historical levels on the new methodology. **Duplicate
  record:** the SCR stream numbered the symmetric-adjustment content of this same page
  R67 — **cite R54.**

### R55. Statement of Policy 1/20 — The PRA's approach to the publication of Solvency II technical information (November 2024, updating June 2024)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.bankofengland.co.uk/prudential-regulation/publication/2020/the-pras-approach-to-publication-of-sii-technical-information
  (verified HTTP 200 on 2026-08-06)
- **Accessed:** 2026-08-06
- **Fetched:** yes (PDF, 11 pages, text extracted in full)
- **Annotation:** The methodology behind [R54]; effective **31 December 2024** for the
  November 2024 changes, which followed PS15/24 [R6]. Verified: ¶1.1 the duty derives from
  **regulation 3 of the IRPR Regulations 2023** [R44]; ¶2.1 the PRA adopted EIOPA's
  end-of-transition-period methodology with exceptions, and **since 31 March 2022 applies
  the 30% long-term-average-spread floor only to UK central government and central bank
  exposures**; ¶2.1C **the VA equals 65% of the risk-corrected currency spread**; ¶3.1–3.5B
  the choice of "PRA relevant currencies" (materiality to 99% of group technical provisions
  **excluding unit-linked**, plus any currency inside a UK firm's MA or VA authorisation;
  three months' notice of addition or removal); ¶3.6ZA1–3.6ZA3 the basic RFR is derived
  from interest rate **swap** rates adjusted for credit risk, falling back to government
  bond rates where swaps are not DLT, with a zero credit adjustment permitted where the
  instrument carries negligible credit risk; ¶3.6A1–3.6A5 extrapolation (the PRA publishes
  *extrapolated* basic curves and firms with MA permission apply the MA to those; where the
  VA applies, **extrapolation is applied after the VA**; the UFR uses the EIOPA UFR-2024
  methodology, is kept stable and **excludes a term premium**); ¶3.6B the long-term average
  spread averages spreads over the RFR applicable at the time, leaving pre-transition
  Libor-based spreads unadjusted; ¶3.6D–3.6F the DLT volume indicators — **average daily
  notional turnover of at least £45 million and an average daily number of trades of at
  least ten**, both over one year, with a **±20% soft buffer**; ¶3.14 the
  reference-portfolio spread formula; ¶3.15 the risk-corrected portion is computed in the
  same manner as the fundamental spread under IRPR regs 6(1)–(8); ¶3.11A regional
  governments and local authorities count as **corporate**, not government, bonds; ¶4.1 the
  SAECC is published monthly under SCR – Standard Formula 3D12–3D14 [R62]. **No numeric
  UFR, alpha or CRA is given in this document.**

### R56. Bank of England / PRA — Deep, liquid and transparent (DLT) assessment for January 2026 implementation
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.bankofengland.co.uk/prudential-regulation/key-initiatives/solvency-ii/dlt-assessments-jan26
  (link taken from [R54] on 2026-08-06; the sibling pages `dlt-assessments-jan22` …
  `dlt-assessments-jan25` hold the earlier annual assessments)
- **Accessed:** 2026-08-06
- **Fetched:** yes (page text; **the tabular maturity grid extracted unreliably** — the
  prose was used, the grid was not)
- **Annotation:** Published 28 November 2025, effective 1 January 2026. The annual
  determination of which swap maturities are DLT and therefore where extrapolation to the
  UFR begins. Verified from prose: the assessment rests primarily on aggregated interest
  rate swap data from the **EMIR Trade Repositories dataset for the 12 months to 31 July
  2025**, applying SoP 1/20 [R55]. Reference instruments: **GBP = SONIA OIS; EUR =
  Euribor; USD = SOFR; CAD = CORRA**. Verified last liquid points: **GBP = 50 years** (the
  50-year maturity failed the average-daily-number-of-trades indicator but the PRA
  retained it on bid-ask evidence, Bank market expertise and year-on-year stability);
  **EUR = 20 years** (the trade data would have supported 50 years but the PRA retained 20
  for stability). **USD and CAD LLPs were not retrieved.** The PRA reserves the right to
  reissue the assessment on sustained structural change.

### R57. PRA Rulebook — Transitional Measures Part (Chapters 10 and 12: the transitional measure on the risk-free interest rate, "TMIR")
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.prarulebook.co.uk/pra-rules/transitional-measures (read in the
  "present on 05/08/2026" view)
- **Accessed:** 2026-08-06
- **Fetched:** yes (browser User-Agent). **Retrieved only for Chapters 10 and 12** —
  Chapters 1–9 are legacy 2016 transitionals and were not transcribed, so **Transitional
  Measures 4.1 grandfathering of pre-2016 own-funds instruments into Tier 1 is
  [unverified]**.
- **Annotation:** The PRA and SoP 2/24 [R58] use the abbreviation "TMIR"; the Rulebook
  Glossary term is *risk-free interest rate transitional measure* [R43]. Verified: **1.2**
  defines *admissible insurance and reinsurance obligations* as obligations whose
  contracts were concluded **before 1 January 2016**, whose technical provisions were
  determined under **INSPRU 1.1.16R of the PRA Handbook as at 31 December 2015**, and
  which are **not subject to an MA permission**; renewal does not create a new contract.
  **10.1** the TMIR may be applied only to admissible obligations and only with a
  **s.138BA FSMA permission**. **10.2** the adjustment is calculated per currency as a
  portion of the difference between (1) the interest rate determined under INSPRU
  3.1.28R–3.1.47R as at 31/12/2015 and (2) the annual effective single discount rate that
  reproduces the Solvency II best estimate of the same obligations. **10.3** that portion
  **decreases linearly from 100% during 2016 to 0% during 2032**. **10.4** where the firm
  uses the VA, leg (2) is computed on the VA-adjusted curve. **10.5** a TMIR firm must
  exclude the admissible obligations from the VA calculation, **must not apply TMTP**
  [R3], and must disclose in its SFCR that it applies the TMIR and the impact of not doing
  so. **Chapter 12** is the phasing-in plan: notify the PRA immediately if the SCR would
  not be met without the TMIR; comply with the SCR by **1 January 2032**; submit a plan
  within two months; report annually. Chapter 11 (Technical Provisions) is **[Deleted]**
  from 31/12/2024, the TMTP having moved to its own Part [R3].

### R58. Statement of Policy 2/24 — Permissions for transitional measures on technical provisions and risk-free interest rates (November 2024, updating February 2024)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.bankofengland.co.uk/prudential-regulation/publication/2024/february/permissions-for-transitional-measures-on-technical-provisions-and-risk-free-interest-rates-sop
  (the same path **without** the trailing `-sop` returns HTTP 404 — verified 2026-08-06;
  the February 2024 PDF sits at
  https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/statement-of-policy/2024/permissions-for-transitional-measures-on-technical-provisions-and-risk-free-interest-rates-feb-2024.pdf)
- **Accessed:** 2026-08-06
- **Fetched:** yes (PDF, 16 pages, November 2024 version, text extracted in full)
- **Annotation:** The Statement of Policy that PS2/24 [R7] flagged but which R7's own
  annotation could not verify; **effective 31 December 2024** (verified). Verified: ¶2.1
  the PRA "generally will not consider new applications for TMTP permission"; ¶2.2 the
  **only** expected route to a new TMTP permission is acquiring a book that already
  benefits from TMTP (Part VII transfer or 100% reinsurance), and such a firm must use the
  TMTP method — the PRA does not expect to allow a new firm the legacy approach.
  ¶2.2A–2.9C the TMIR permission process: the PRA will approve, vary or revoke by
  reference to compliance with **Transitional Measures 10.2–10.5** [R57], and will revoke
  where a Transitional Measures 12.4 report shows SCR compliance by 2032 is unrealistic.
  ¶2.7–2.8 the arithmetic a transferee must perform to derive its own ZA, ZB and C0 from
  the transferor's Ar, Br and C0. ¶3.2 the PRA will consider waiving the amortisation rule
  (TMTP 5.2) where applying it would move the firm's **solvency coverage ratio by five
  percentage points or more**, provided the alternative still amortises consistently to
  zero by 1 January 2032. Chapters 4–5, the legacy approach: from 31 December 2024 **no
  further legacy-approach permissions will be granted**; legacy firms must freeze their
  Solvency I Pillar 2 methodology as at their last pre-31/12/2024 recalculation, may change
  best-estimate assumptions **only** for market conditions and demographics, must cap the
  permission to the business it covered on 31 December 2024, and must amortise to zero by
  1 January 2032 without a cliff edge; the materiality criterion for having been granted
  the legacy approach was again a **five-percentage-point** difference in solvency coverage
  ratio across forward-looking scenarios.

### R59. SS17/15 — Solvency II: transitional measures on risk-free interest rates and technical provisions (November 2024, updating February 2024)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URLs:** PDF read
  https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/supervisory-statement/2024/ss1715-november-2024-update.pdf
  ; landing page
  https://www.bankofengland.co.uk/prudential-regulation/publication/2015/solvency2-transitional-measures-on-risk-free-interest-rates-and-technical-provisions-ss
- **Accessed:** 2026-08-06
- **Fetched:** yes (PDF, 15 pages, text extracted in full)
- **Annotation:** Published 15 November 2024, effective 31 December 2024. Verified: ¶2.1
  for the TMIR the firm must determine the INSPRU leg so the comparison with the Solvency
  II annual effective rate is *meaningful*; ¶2.2 with a VA, the Solvency II leg reflects
  the VA and the obligations are then discounted at **basic RFR plus the transitional
  adjustment, with no VA added on top** (double counting). ¶3.6A the base-TMTP calculation
  must not double-count both actual run-off since the last recalculation and the 1/16
  linear deduction. ¶3.6B designation of MA-eligible obligations to the dynamic portion is
  **optional and partial**. ¶3.6C TMTP is calculated at **overall firm level**, though it
  may be allocated internally (e.g. across ring-fenced funds). ¶3.6D "reporting period"
  means the periods in which TMTP must be reported under the Reporting Part [R84]. ¶3.6E
  the **Chief Actuary** selects the methodology for projecting the risk-margin portion and
  dynamic portion in TMTP 5.2, consistent with TPFR Chapter 27 [R41]. ¶3.7A–3.8A the
  transfer-event mechanics. ¶4.2A–4.2B **TMTP is a range, not a point**: the applied
  deduction may be anywhere between zero and the maximum, and a firm applying less than the
  maximum must disclose both figures and apply the choice consistently across QRTs, ORSA
  and market disclosures. ¶4.2D–4.2E legacy firms must keep the Solvency I Pillar 2 and
  Solvency II best-estimate bases **consistent**, and an assumption change reflecting
  market or demographic experience must not be allowed to increase TMTP benefit. ¶5.1 TMTP
  cannot be applied after 1 January 2032; ¶5.5–5.8 the ORSA must monitor the risk that TMTP
  runs off faster or slower than the underlying liabilities; ¶7.1 the **Chief Actuary
  oversees** the TMTP and TMIR calculation as part of the actuarial function (Conditions
  Governing Business 6.1(b) and (e) [R92]). **This settles the "[unverified]" run-off date
  carried in the frozen R3 and R7 annotations**: the linear decrease to 0% during 2032
  [R57 10.3] and the 1 January 2032 backstop are both verified here.

### R60. Statement of Policy 8/24 — Solvency II: Matching Adjustment Permissions and Matching Adjustment Investment Accelerator Permissions (October 2025, updating June 2024)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URLs:** PDF read
  https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/statement-of-policy/2025/sop824.pdf
  ; landing page
  https://www.bankofengland.co.uk/prudential-regulation/publication/2024/june/solvency-ii-matching-adjustment-permissions-statement-of-policy
- **Accessed:** 2026-08-06
- **Fetched:** yes (PDF, 22 pages, text extracted in full; read closely for Chapters 1, 2,
  2A and 3)
- **Annotation:** How a firm actually obtains, varies and loses the permission that
  Matching Adjustment 2.1 [R2] makes a precondition of applying the MA at all. Verified:
  MA permissions are granted by **waiving or modifying PRA rules under s.138BA FSMA** so
  that the firm may apply the MA in accordance with **IRPR reg 4(1)** [R44] (¶1.2); the
  same power varies a permission to admit assets with new features, grants MAIA
  permissions and revokes either. Verified process facts: where evidence is sufficient and
  the need for clarification limited, the PRA expects to **determine an application no
  later than six months from receipt** (¶2.29, repeated at ¶3.2), with a **streamlined
  review** track for applications limited in extent and novelty in which firms may propose
  safeguards such as exposure limits (Chapter 3). Verified on the MA/MAIA interaction: **a
  MAIA permission is not possible without an MA permission** (¶1.4 fn 1), and the PRA
  **does not expect an initial MAIA application at the same time as an initial MA
  application** (¶2A.5); revocation grounds for MAIA include **failure to apply to
  regularise MAIA assets within 24 months** of inclusion (¶2A.18). Verified on breach:
  where a firm cannot restore compliance with the MA eligibility conditions within two
  months, **the MA is reduced proportionately by 10% for each further month or part-month
  of non-compliance** (¶2.36 — the SoP's plain-English statement of the Matching
  Adjustment 13.5 formula), and the PRA expects to use its revocation power where a breach
  is significant, compliance cannot be restored in a reasonable period after the two-month
  window, **the firm's MA is zero**, or breaches are repeated (¶2.38).

### R60b. PS17/25 — Matching Adjustment Investment Accelerator
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.bankofengland.co.uk/prudential-regulation/publication/2025/october/matching-adjustment-investment-accelerator
- **Accessed:** 2026-08-06
- **Fetched:** **no.** The URL cited in the SS7/18 footnote
  (…/october/matching-adjustment-investment-accelerator-policy-statement) returns
  **HTTP 404**; the URL above was recovered from a web search and **the page body
  extraction failed**.
- **Annotation:** Numbered so that the frozen R2 and R8 annotations' "[unverified —
  PS17/25 itself not fetched]" flag has a citable handle. Its existence, date and effect
  are verified **indirectly and only indirectly**, from primary documents: the Matching
  Adjustment Part Chapters 14–19 all carry the rule date-stamp **27/10/2025** [R2]; the
  SS7/18 October 2025 update annex records that the SS "has been updated to reflect the
  PRA's final policy on Matching Adjustment Investment Accelerator … set out in the
  publication of Policy Statement (PS17/25)", adding paragraphs 1.6–1.7 and a new Chapter
  10 [R8]; and the MA Part's "Legal Instruments that change this Part" panel lists PS17/25
  [R2]. **The PS itself is the source of no number anywhere in this library.** Every MAIA
  number comes from [R2], [R8] or [R60].

---

## 9. Capital — the Solvency Capital Requirement and the standard formula (R61–R73)

Entries from `uk/_research/solvency-uk-scr-standard-formula.md`; **R74, R75 and R76 are
unused by design.** **R63, R66 and R67 have no entry here** — they are that stream's
numbers for documents entered above as [R42], [R49] and [R54]. All accessed
**2026-08-06**.

### R61. PRA Rulebook — Solvency Capital Requirement – General Provisions Part (as at 05/08/2026)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.prarulebook.co.uk/pra-rules/solvency-capital-requirement---general-provisions/05-08-2026
- **Accessed:** 2026-08-06
- **Fetched:** yes (browser User-Agent; 14,517 chars of extracted text; **read in full**,
  all 8 chapters)
- **Annotation:** The short constitutional Part sitting above the standard formula.
  Verified with the Rulebook's own date stamps: **1.1** application [01/01/2016]. **2.1** a
  firm must hold eligible own funds covering its SCR [01/01/2016]. **3.1** the SCR must be
  calculated **either** under the standard formula **or** using an internal model for
  which permission has been granted [31/12/2024 — this rule changed at the restatement;
  the pre-31/12/2024 version **was not retrieved**]. **3.2** going-concern presumption.
  **3.3** calibration must take account of all quantifiable risks, "including at least"
  non-life underwriting, **life underwriting, health underwriting, market, credit and
  operational risk**; must cover existing business **and new business expected to be
  written over the following 12 months**; and for existing business must cover **only
  unexpected losses**. **3.4** the SCR "must correspond to the **value-at-risk of its
  basic own funds subject to a confidence level of 99.5% over a one-year period**".
  **3.5** risk-mitigation techniques may be recognised provided the credit and other risks
  they create are reflected. **3.6** the SCR **must not cover the risk of loss of basic own
  funds resulting from changes to the volatility adjustment**. **4.1** calculate and report
  at least annually; **4.2** hold own funds covering the **last reported** SCR; **4.3**
  monitor own funds and SCR **on an ongoing basis**; **4.4** recalculate **without delay**
  where the risk profile deviates significantly from the assumptions underlying the last
  reported SCR; **4.5** recalculate on PRA request. **5.1/5.1A** duty to remedy the
  deficiencies behind a capital add-on and, on request, submit a progress report; **5.2**
  the SCR before the add-on **plus** the add-on constitutes the firm's SCR; **5.3** **for
  the purpose of calculating the risk margin the SCR must exclude any add-on imposed for a
  significant system-of-governance deviation.** Chapters **6–8** are Lloyd's-specific and
  are recorded but not material to a UK direct life insurer's model.

### R62. PRA Rulebook — Solvency Capital Requirement – Standard Formula Part (as at 05/08/2026)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.prarulebook.co.uk/pra-rules/solvency-capital-requirement---standard-formula/05-08-2026
- **Accessed:** 2026-08-06
- **Fetched:** yes (browser User-Agent; 452,843 chars raw / 408,900 cleaned — **the single
  largest document in the UK library**). **Read selectively, by chapter:** chapters 2, 2A,
  3, 3B, 3C, 3D (interest rate, equity, symmetric adjustment, property, spread on bonds
  and loans, spread on MA portfolios, concentration, currency), 3E13–3E15, 3F, 4, 5, 6,
  7.1–7.16, 8 and 9 read in full; chapters 1D, 3A (non-life), 3D18–3D24 (securitisation,
  credit derivatives, specific exposures) and 3G **surveyed only**.
- **Annotation:** The operative UK standard formula. Chapter inventory as retrieved: `1`
  Application and Definitions; `1A`–`1D` credit assessments and credit quality steps; `2`
  Structure of the SCR Standard Formula; `2A` Annexes; `3` The Basic SCR; `3A` Non-life
  Underwriting Risk; `3B` **Life Underwriting Risk**; `3C` **Health Underwriting Risk**;
  `3D` **Market Risk**; `3E` Counterparty Default Risk; `3F` Intangible Asset; `3G` Risk
  Mitigation Techniques; `4` Equity Risk Sub-Module and the Symmetric Adjustment
  Mechanism; `5` Operational Risk; `6` **Adjustment for Loss-Absorbing Capacity of
  Technical Provisions and Deferred Taxes**; `7` Simplifications; `8` Lloyd's; `9`
  **Ring-Fenced Funds and Matching Adjustment Portfolios**. The Part's change dates are
  **01/01/2016, 31/12/2024, 24/07/2025, 01/01/2026, 01/01/2027**; **rule 1.2 carries a
  future version after 01/01/2027 that was not retrieved.** Chapter 6 (LACTP and LACDT)
  carries the transitional permission in **6.5** stated as running "for a transitional
  period **ending 30 December 2025**"; on its face that period had expired at the access
  date, yet the rule remains printed in the current view, and **no PRA instrument
  confirming its expiry or extension was retrieved** — treat 6.5 as expired for a
  current-date calculation but flag it. **Not transcribed anywhere in this library:** the
  counterparty-default probability-of-default table `3E12` and the loss-given-default
  definitions `3E4`–`3E11`, the concentration aggregation formulas `3D27`/`3D28`, and the
  ECAI-to-credit-quality-step inputs, which come from PS12/25 [R72]. **Duplicate record:**
  the accounting stream numbered Chapter 6 alone as R112 — **cite R62.**

### R64. PRA statement, 20 December 2024 — Restatement of Solvency II assimilated law: correction to standard formula mass lapse life underwriting risk rule in PS15/24, with PRA Rulebook: SII Firms: Solvency II Amendment (No 1) Instrument 2024
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.bankofengland.co.uk/prudential-regulation/publication/2024/december/pra-statement-on-restatement-of-solvency-ii-assimilated-law
- **Accessed:** 2026-08-06
- **Fetched:** yes (5,602 chars; **read in full**). **The annexed instrument PDF was not
  separately retrieved** — the statement describes its single operative effect.
- **Annotation:** Verified, with quoted rule reference. The PRA "identified an error in
  rule **3B6.6(1)**" of the SCR – Standard Formula Part as published in PS15/24. In CP5/24
  the PRA proposed to restate Delegated Regulation **Article 142(6)** [R49], which applies
  a **70% mass-lapse stress** to two business types and **40% in all other cases**. Using
  the 2015 UK transposition table the PRA identified RAO Schedule 1 Part II **class II
  ("Marriage and birth")** and **class VII ("Pension fund management")** as in scope of
  70%; but in the final PS15/24 instrument it wrote **class III and class VII**. The PRA
  concluded the class III reference "is in fact an error" and that the correct restatement
  "should only require firms to apply a 70% stress … to **RAO class VII(a) and class
  VII(b)** business". The Amendment (No 1) Instrument 2024 **deletes the class III
  reference in Annex O of Appendix 6 of PS15/24** [R42] and is that instrument's only
  change. Published 20 December 2024, **effective 31 December 2024**; it **supersedes
  PS15/24 ¶6.16 and ¶6.18** without amending their text. **Residual discrepancy recorded,
  not resolved:** the statement's own narrative names **class II and class VII** as the
  transposition-table result, while the corrected rule text as read in [R62] names **class
  VII only**. Decisive for ULB, which is class III business and therefore takes the 40%
  limb, not 70%.

### R65. PRA Rulebook — Solvency Capital Requirement – Undertaking Specific Parameters Part (as at 05/08/2026)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.prarulebook.co.uk/pra-rules/solvency-capital-requirement---undertaking-specific-parameters/05-08-2026
- **Accessed:** 2026-08-06
- **Fetched:** yes (60,255 chars raw / 54,158 cleaned; chapters 1–3 and 7 read in full,
  chapters 4–6 and 8–10 **surveyed only**; URL independently re-verified 2026-08-06)
- **Annotation:** Part change dates **31/12/2024** and **24/07/2025**. Chapter inventory:
  `1` Applications and Definitions; `2` Undertaking Specific Parameters; `3` Data Criteria;
  `4` Premium Risk Method; `5`/`6` Reserve Risk Methods 1 and 2; `7` **Revision Risk
  Method**; `8`/`9` Non-Proportional Reinsurance Methods 1 and 2; `10` Credibility Factor.
  Verified: **2.1** a firm must not apply a USP unless it is a **USP firm** (i.e. holds a
  s.138BA USP permission); **2.2** a USP firm must **not revert** to the standard
  parameter; **2.3** the exhaustive replaceable-parameter table; **2.4** where alternative
  methods are available the firm must use the most accurate, or the most conservative
  where greater accuracy cannot be demonstrated; **2.5** two anti-double-counting
  prohibitions. **The only life-relevant USP in the whole Part is the revision-risk
  parameter** (`3B5` life and `3C15` health), and `7.1` bars its use where the annuities
  are subject to material inflation risk. Chapter 3 sets complete/accurate/appropriate
  data criteria cross-referring to TPFR 4 [R41]. In practice near-empty for UK life.

### R68. SS15/16 — Solvency II: Monitoring model drift and standard formula SCR reporting for firms with permission to use an internal model (September 2025, updating July 2018)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URLs:** publication page
  https://www.bankofengland.co.uk/prudential-regulation/publication/2016/solvency2-monitoring-model-drift-and-standard-formula-scr-reporting-ss
  ; PDF
  https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/supervisory-statement/2025/ss1516-september-2025-update.pdf
- **Accessed:** 2026-08-06
- **Fetched:** yes (PDF, 7–8 pages, **read in full**). **Retrieved three times by three
  streams** — extracted character counts 7,699 / 7,512 / 7,332, an extraction artefact,
  not three documents.
- **Annotation:** The document that makes the standard formula relevant to internal-model
  firms. Verified: ¶1.1 addressed to firms with **s.138BA FSMA** internal model
  permission. ¶2.1 "model drift" is "the risk that capital requirements calculated using
  an internal model may, over time, become **less reflective of the risks to which firms
  are exposed**". ¶2.3 the alternative balance-sheet measures the PRA monitors against
  include **standard formula SCR, pre-corridor MCR** (i.e. `MCR_linear` before the 25%/45%
  collar [R78]), **net written premium and best estimate liabilities**; ¶2.3A different
  tools may be used for life and general insurance firms. ¶3.3 **Solvency Capital
  Requirement – Internal Models 3.4** [R81] requires an internal-model firm to provide the
  PRA on request with an estimate of the SCR determined under the standard formula; ¶3.5
  the PRA therefore expects such firms **to maintain the ability to calculate their SCR
  using the standard formula**. ¶3.5A–3.7 the *annual private XBRL* standard-formula
  submission is expected of firms **with material non-life technical provisions** only, is
  **not required to be externally audited**, and must be approved by a suitably authorised
  senior manager; ¶3.8 due **four weeks after** the annual QRT deadline in the Reporting
  Part [R84]; ¶3.11 submitted through **BEEDS** as an "occasional submission". Paragraphs
  2.3A, 2.3B, 3.5A and the amendment to 3.6 date from the September 2025 update following
  PS15/25 [R87]. **Practical consequence for a UK life insurer:** it must be able to run
  the standard formula even if it does not use it for its published SCR, but it is not
  caught by the submission expectation. **Duplicate records:** R81c and R97c — **cite
  R68.**

### R69. Statement of Policy 4/24 — Solvency II: Capital add-ons (November 2024, updating February 2024)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.bankofengland.co.uk/prudential-regulation/publication/2024/february/solvency-ii-capital-add-ons-sop
- **Accessed:** 2026-08-06
- **Fetched:** yes (41,615 chars). **Title page, contents and scope verified from the
  retrieved text; the body was surveyed, not transcribed.**
- **Annotation:** The policy layer over SCR – General Provisions Chapter 5 [R61].
  Retrieved document confirmed as "Solvency II: Capital add-ons, Statement of policy 4/24,
  November 2024 (updating February 2024)". **Numerical thresholds not transcribed** — the
  PRA's quantitative thresholds for what counts as a "significant risk profile deviation"
  were **not read out of the retrieved text in this pass and must not be stated**.
  Recorded for the drafter as the place to look, not as a source of numbers.

### R70. Statement of Policy 11/24 — Solvency II: The PRA's approach to Standard Formula adaptations (15 November 2024)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.bankofengland.co.uk/prudential-regulation/publication/2024/november/solvency-ii-approach-to-standard-formula-adaptations-sop
- **Accessed:** 2026-08-06
- **Fetched:** **partial** — the landing page was retrieved and read in full (2,498
  chars); **the SoP PDF itself was not retrieved.**
- **Annotation:** Verified from the landing page only: the SoP covers the PRA's approach to
  **(a) undertaking specific parameter (USP) and group specific parameter (GSP)
  permissions; (b) investments in a securitisation; and (c) permissions relating to the
  adjustment for loss-absorbing capacity of deferred taxes (LACDT)**; it is to be read with
  the SCR – Standard Formula and SCR – Undertaking Specific Parameters Parts; published 15
  November 2024, **effective 31 December 2024**, following PS15/24 [R6]. This is the
  permissions gateway for everything in [R65] and for the LACDT permission in SCR-SF 6.5
  [R62]. **No content beyond the scope statement was retrieved — do not attribute detail
  to it.**

### R71. SS14/15 — With-profits, Chapter 2: Solvency II ring-fenced fund (RFF) regime
- **Publisher:** Prudential Regulation Authority (Bank of England), via the PRA Rulebook
  guidance view
- **URLs:** https://www.prarulebook.co.uk/guidance/supervisory-statements/ss14-15---with-profits/2-solvency-ii-ring-fenced-fund-rff-regime/25-06-2024
  ; also read at
  https://www.prarulebook.co.uk/guidance/supervisory-statements/ss14-15---with-profits/05-08-2026
  and as the full SS PDF text (16,108 chars)
- **Accessed:** 2026-08-06
- **Fetched:** yes (**Chapter 2 read in full**; other chapters of SS14/15 were retrieved
  only for RFF, surplus-funds and inherited-estate references)
- **Annotation:** Three paragraphs that decide the whole UK ring-fenced-fund question for
  life insurers, and the document that connects UK with-profits funds to `SCR-SF 9` [R62].
  Verified: **¶2.1** whether an arrangement gives rise to an RFF "is based on the
  restrictions which apply to the use of certain assets or own funds", which may arise from
  the characteristics of the arrangement, contract or product. **¶2.2** "Restrictions on
  assets and own funds result from the nature of, and regulatory regime for, with-profits
  insurance business in the United Kingdom. As communicated in SS1/14 [R117], the PRA
  expects that **such restrictions will generally mean that each with-profits fund displays
  the characteristics of a RFF**. A Solvency II firm will therefore be required to reflect
  the lack of availability of assets and own funds within the with-profits fund to cover
  the risks of the rest of the firm." **¶2.3** where a firm operates **sub-funds** within a
  with-profits fund it must determine whether any or all are separate with-profits funds
  under FCA **COBS 20** [R9]; if so, the PRA expects **each such sub-fund to be treated as
  a separate RFF**. All three paragraphs are date-stamped 20/03/2015. Chapter 9 of the same
  SS covers **reattributions of inherited estate**. **The EIOPA guidelines on ring-fenced
  funds referenced in the SS's footnote 4 are entered separately at [R80c].** **Duplicate
  record:** R80b — **cite R71.**

### R72. PS12/25 — Restatement of CRR and Solvency II requirements in PRA Rulebook – 2026 implementation (17 July 2025)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.bankofengland.co.uk/prudential-regulation/publication/2025/july/restatement-of-crr-and-sii-requirements-in-pra-rulebook-policy-statement
- **Accessed:** 2026-08-06
- **Fetched:** yes (59,392 chars; **Chapter 3 (ECAI mapping) read; Chapters 1, 4 and the
  appendix list surveyed; the mapping tables themselves were not transcribed**)
- **Annotation:** The reason the SCR – Standard Formula Part carries a **01/01/2026**
  change date. Verified: the PS makes amendments to the **Solvency Capital Requirement –
  Standard Formula, Matching Adjustment and Glossary Parts** (Appendix 6, *PRA Rulebook:
  CRR Firms, Solvency II Firms: Credit Quality Steps Mapping Instrument 2025*); ¶1.7
  Chapter 3 on ECAI mapping is relevant to Solvency II firms; ¶3.1 the mappings of external
  credit assessment institution ratings to **credit quality steps** are specified in the
  capital adequacy frameworks and most PRA-authorised firms must apply them; ¶3.4 the PRA
  originally proposed **1 July 2025** for the insurance-related changes; ¶3.33 it then
  confirmed **1 January 2026**; ¶3.14 two changes from consultation — the **Banque de
  France Global ANACOT** long-term issuer scale was added and the **Economist Intelligence
  Unit** sovereign rating band scale was removed. **The mapping tables themselves are not
  transcribed anywhere in this library** — the CQS *inputs* to `3D17`, `3D25`, `3D29`,
  `3D30` and `3E12` [R62] come from this instrument, and a drafter needs the instrument.

### R73. PRA Rulebook — Annexes to the SCR – Standard Formula Part (referenced by SCR-SF 2A.1) — NOT RETRIEVED
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** linked from
  https://www.prarulebook.co.uk/pra-rules/solvency-capital-requirement---standard-formula/05-08-2026
  (rule 2A.1: "The Annexes referred to in 3A, 3C and 7 can be found here")
- **Accessed:** 2026-08-06
- **Fetched:** **NO.** The annexes are a separate linked file that was **not retrieved**;
  only the pointer rule 2A.1 [31/12/2024] was read, in [R62].
- **Annotation:** **Numbered deliberately so that the gap has a citable handle.** On the
  evidence of the cross-references read in [R62], the annexes referred to by rules 3A, 3C
  and 7 include **Annex XVI** (health catastrophe — the country list, the ratio of persons
  affected `r_s`, the event types `e`, the benefit ratios `x_e`, and the
  healthcare-utilisation types `h` and ratios `H_h` for the pandemic sub-module),
  **Annexes V–VIII and X** (non-life catastrophe risk zones and risk weights), and the
  annex underlying the geographical-diversification factor in `3A5`. **None of those
  values is stated anywhere in this library.** One consequence travels with every citation
  of R73: the **health catastrophe sub-module cannot be computed** from this library.
  **Recorded, not resolved:** the SCR stream additionally recorded the numbered
  line-of-business list as sitting in this un-retrieved file [R62 Gaps §1], but **TPFR
  Annex 1 Parts A–E, lines of business 1–36, was retrieved and read in full** [R41], and
  `uk/_research/uk-product-regulatory-applicability.md` records — as a **drafter's
  inference from consistent cross-references** in [R42] (`SCR-SF 3.18(3)` "lines of
  business 9, 21 and 28"; `3A10` "lines of business 5 and 17", both matching the Annex 1
  assignments), **not as a statement in any retrieved document** — that the SCR-SF
  numbered lines are the TPFR Annex 1 lines. Critical illness still carries `?` on the
  life-versus-health split, but for a different reason: see §15. Any downstream document
  needing a health-CAT parameter must retrieve this annex file first.

---

## 10. Capital — own funds, the MCR, ring-fenced funds and internal models (R77–R83c)

Entries from `uk/_research/solvency-uk-own-funds-mcr-and-internal-models.md`, block
R77–R83 plus lettered sub-ids. **R79, R79b, R80b, R81c and R83d have no entry here** —
they are that stream's numbers for documents entered as [R45], [R46], [R71], [R68] and
[R87]. All accessed **2026-08-06**.

### R77. PRA Rulebook — Own Funds Part (as at 05/08/2026)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.prarulebook.co.uk/pra-rules/own-funds/05-08-2026
- **Accessed:** 2026-08-06
- **Fetched:** yes (browser User-Agent; 74,507 chars, read in full, chapter by chapter).
  **The future view after 31/12/2026 was not retrieved** — live future markers sit on
  3A.1, 3B.1, 3C.1, 3D.1, 3E.1, 3F.1 and 3G.1.
- **Annotation:** The operative UK rules on what counts as capital. Structure: Chapter 1
  (application and definitions), 2 (determination of own funds), 3 (classification into
  tiers), 3A/3B (Tier 1 list / features), **3C (reconciliation reserve)**, 3D/3E (Tier 2
  basic), 3F/3G (Tier 3 basic), 3H/3I (Tier 2 ancillary), 3J (Tier 3 ancillary), 3K
  (participations deduction), **3L (adjustment for ring-fenced funds and matching
  adjustment portfolios)**, 4 (eligibility limits, Art. 98 form), 4A (eligibility limits,
  percentage-of-SCR/MCR form), 5 (pre-issuance notification), 6 (Lloyd's). Verified:
  **own funds = basic own funds + ancillary own funds (2.1)**; **basic own funds = (excess
  of assets over liabilities less own shares held) + subordinated liabilities (2.2)**.
  Ancillary own funds require an *ancillary own funds permission* specifying a monetary
  amount or a method (2.5, 2.6) and may be attributed only an amount reflecting
  loss-absorbency on prudent and realistic assumptions (2.7). The tiering tests are
  permanent availability and subordination (3.5(1),(2)), judged against duration, absence
  of incentives to redeem, absence of mandatory servicing costs and absence of
  encumbrances (3.6). An item not on the *own funds lists* needs a **classification of own
  funds permission** (3.4(2)) and, if classified into Tier 1, must be fully paid in
  (3.4A). Surplus funds are a Tier 1 item at **3A.1(1)(d)** [R45][R46]; net deferred tax
  assets are Tier 3 at **3F.1(1)(c)** [R39]. Rule date-stamps: Chapter 2 and the Chapter 3
  core rules mostly 01/01/2016; the whole of 3A–3L, 3.4A, 4A and Chapter 5 are
  **31/12/2024** (created by PS15/24 [R6]); 1.2 is 02/01/2026 — consistent with the
  instrument's Annex M commencement date [R42]. **Recorded, not resolved:** Chapter 4 and
  Chapter 4A both state eligibility limits; SS2/15 ¶1.3(d) is the PRA's own reconciliation
  of the duplication [R83].

### R83. SS2/15 — Solvency II: Own funds (November 2024, updating September 2019)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/supervisory-statement/2024/ss215-november-2024-update.pdf
- **Accessed:** 2026-08-06
- **Fetched:** yes (PDF, 8 pages, 11,550 chars, read in full)
- **Annotation:** Short, and mostly about instrument mechanics rather than measurement.
  Verified: ¶1.3(b) "Own Funds 3L sets out the adjustments that must be made to own funds
  to reflect the lack of transferability of ring-fenced funds"; ¶1.3(d) Own Funds 4A sets
  the limits **for the purposes of Own Funds 4**; ¶2.1A an ancillary own funds item **must
  be callable on demand** and the firm must demonstrate there is no trigger event or
  restriction affecting when it can be called; **¶2.1B ancillary own funds are not
  emergency capital** — the PRA does not expect firms to apply for AOF when in danger of
  breaching the SCR; ¶¶4.3–4.6 paid-in ordinary shares cease to meet the Tier 1 criteria
  once a dividend is declared unless the firm can cancel it before payment, so the PRA
  suggests firms amend their articles so that **all dividend declarations are
  conditional**. Chapter 3 (own funds transitionals) is **deleted in its entirety**. The
  Annex records the November 2024 update following PS15/24 [R6], which rewrote all
  cross-references from Delegated Regulation (EU) 2015/35 [R49] to PRA Rulebook rules.

### R83b. Statement of Policy 10/24 — Solvency II: The PRA's approach to insurance own funds permissions
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URLs:** PDF
  https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/statement-of-policy/2024/solvency-ii-approach-to-insurance-own-funds-permission-sop.pdf
  ; landing page
  https://www.bankofengland.co.uk/prudential-regulation/publication/2024/november/solvency-ii-approach-to-insurance-own-funds-permission-sop
- **Accessed:** 2026-08-06
- **Fetched:** yes (355,106-byte PDF → 57,487 chars). **Chapters 1, 2 and 7 read in full;
  Chapters 3, 4, 5 and 6 read as headings and scope only — their substantive content is
  [unverified].**
- **Annotation:** Published **15 November 2024, effective 31 December 2024**, following
  PS15/24 [R6]. All Own Funds permissions are granted, varied and revoked under **s.138BA
  FSMA** (¶1.1). Seven chapters: 1 introduction; 2 prior permission for repayment or
  redemption; 3 ancillary own funds permissions; 4 classification of own funds permissions;
  5 prior permission for repayment/redemption **between five and ten years for restricted
  Tier 1 items**; 6 prior permission for **early** repayment or redemption; 7 permissions
  **when not in compliance with the SCR**. Verified details: **¶1.4** "repayment or
  redemption" includes repurchase or buyback and any arrangement with the same economic
  effect — expressly **share buybacks, tender operations, repurchase plans and repayment of
  principal at maturity** — as well as issuer call exercise. **¶2.2 / ¶7.4** every
  application must be supported by the firm's own assessment addressing (a) current and
  short-to-medium term impact on overall solvency, (b) consistency with the firm's
  **medium-term capital management plan and ORSA** [R95], (c) capacity to raise additional
  own funds, and for a non-compliance application (d) the proposed exchange or conversion
  and (e) consistency with the recovery plan required by Undertakings in Difficulty 3.1(2)
  [R82]. **¶2.4 / ¶7.7** applications at least **three months** before the earlier of the
  required contractual notice date and the proposed repayment date; the PRA expects to
  determine within **three months**. **¶2.5(b) / ¶7.8(b)** when excluding a repaid or
  redeemed item, reduce the relevant category of own funds and **make no adjustment to or
  re-calculation of the reconciliation reserve**. **¶2.5(d) / ¶7.8(d)** do not proceed if
  repayment would cause SCR non-compliance even after notice. **¶7.6** permission during
  SCR non-compliance is granted only where the item is exchanged for or converted into an
  item of at least the same quality **and the firm complies with the MCR afterwards**.
  **¶7.2** legacy "exceptional waiver" wording in older instruments is now treated as
  requiring a s.138BA permission. The SoP cites **Own Funds 3B.14, 3B.15, 3E.6, 3E.7, 3G.6
  and 3G.7** — rules that exist in the Part but **were not transcribed** in the research
  [R77].

### R83c. CP4/26 — UK Solvency II Own Funds: Updates and fixes to rules and expectations (consultation)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.bankofengland.co.uk/prudential-regulation/publication/2026/february/uk-solvency-ii-own-funds-updates-and-fixes-to-rules-and-expectations
- **Accessed:** 2026-08-06
- **Fetched:** yes (39,920 chars; overview and proposal chapters read, cost-benefit annexes
  skimmed)
- **Annotation:** Published **25 February 2026**; responses due 24 April 2026. **A
  consultation, not rules.** Records that in PS15/24 "the PRA generally chose not to
  propose significant changes during the restatement to ensure certainty for UK insurers",
  making CP4/26 the first substantive post-restatement own-funds reform. Four proposals,
  verified. **Proposal 1** — remove the requirement for a classification of own funds
  permission for **equity-accounted subordinated instruments** by adding them to the
  recognised lists in Own Funds 3A, 3D and 3F, with consequential Group Supervision
  changes. **Proposal 2** — expectations on compliant sequencing of concurrent tender
  offers and new issuances (revisions to SS3/15). **Proposal 3** — minor corrections, two
  of which bear on measurement: correcting an inconsistency in the reconciliation-reserve
  calculation "that would cancel out the increase in eligible own funds following receipt
  of a classification of own funds permission for an item recognised as a liability on the
  Solvency II balance sheet"; and "clarifying the interaction of **Own Funds 3C and Own
  Funds 3L** when determining the amount of restricted own funds to deduct from the excess
  of assets over liabilities when calculating the reconciliation reserve", with
  consequential amendments to SS2/15 Chapter 1 [R83] and to the SCR – Standard Formula Part
  [R62]. **Proposal 4** — restate the remaining relevant EIOPA guidelines on
  classification of own funds and on ancillary own funds into PRA supervisory statements
  (**it does not name the ring-fenced funds guidelines** [R80c]). **Only Proposal 1 was
  finalised, by PS18/26 [R87]; the retrieved PS18/26 text does not state the outcome of
  Proposals 2, 3 or 4.**

### R78. PRA Rulebook — Minimum Capital Requirement Part (as at 05/08/2026)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.prarulebook.co.uk/pra-rules/minimum-capital-requirement/05-08-2026
- **Accessed:** 2026-08-06
- **Fetched:** yes (16,664 chars; read in full — the Part is short)
- **Annotation:** Short and entirely formulaic. Verified: the firm must hold **eligible own
  funds covering the MCR** (2.1); the MCR is `max(MCR_combined, AMCR)` (3.1A) where
  `MCR_combined = min(max(MCR_linear, 0.25·SCR), 0.45·SCR)` (3.1B); the absolute floor is
  **£3,500,000** for long-term insurance business (3.2(2)); and 3.3 independently restates
  the corridor as "neither below 25% nor above 45% of the firm's SCR … **including any
  capital add-on which has been imposed**" [R61][R69]. The linear component splits into a
  general-insurance and a long-term part (3A.1); the **long-term linear formula (3C.1)** has
  four technical-provision terms — `TP_l1` guaranteed benefits for participating business,
  `TP_l2` future discretionary benefits (with a **negative** coefficient), `TP_l3` linked
  long-term liabilities, `TP_l4` all other long-term — plus a **capital-at-risk** term
  defined by reference to what the firm would pay on death or disability and floored at zero
  per contract. Calculation is **at least quarterly** with reporting under Reporting 2.1–2.5
  (4.1) [R84]; where a corridor limit binds, the firm must give the PRA information allowing
  a proper understanding of why (4.2). Chapter 6 carries the non-life segment factor table
  (α_s, β_s) — **income protection written as general insurance is segment 2, α 13.1% and
  β 8.5%** — transcribed only in outline in the research because it does not bite on
  long-term life products. Old rule 3.1 is `[Deleted]`; 3.1A, 3.1B, 3.2, 3A, 3B, 3C and
  Chapter 6 are date-stamped **31/12/2024**; 2.1, 3.3 and Chapter 5 (Lloyd's) survive from
  01/01/2016; 4.1 from 31/12/2021.

### R78b. SS4/15 — Solvency II: the solvency and minimum capital requirements (as at 05/08/2026)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.prarulebook.co.uk/guidance/supervisory-statements/ss04-15---solvency-ii---the-solvency-and-minimum/05-08-2026
- **Accessed:** 2026-08-06
- **Fetched:** yes (7,750 chars; read in full)
- **Annotation:** **A negative finding, recorded so that a drafter does not go looking.**
  Retrieved specifically to see whether the PRA has any MCR guidance. **It does not any
  more.** Verified: **Chapter 4, "The minimum capital requirement", is `[Deleted]`** — rule
  4.1 is `[Deleted]`, date-stamped **31/12/2024**, with a "past version before 31/12/2024"
  marker. Despite its title the SS now carries only SCR-related expectations; its ¶3.7
  notes that the Solvency II Regulations contain additional requirements relevant to a firm
  seeking a waiver of SCR – Internal Models 12.2 [R81]. **There is therefore no surviving
  PRA supervisory guidance on the MCR: the MCR Part [R78] is the whole of it.**

### R82. PRA Rulebook — Undertakings in Difficulty Part (as at 05/08/2026)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.prarulebook.co.uk/pra-rules/undertakings-in-difficulty/05-08-2026
- **Accessed:** 2026-08-06
- **Fetched:** yes (5,802 chars; read in full)
- **Annotation:** Six short chapters — where an own-funds shortfall becomes a supervisory
  event. Verified: **2.1** procedures to identify deteriorating financial conditions and
  immediate notification to the PRA. **3.1 (SCR breach)** inform the PRA immediately on
  observing non-compliance *or a risk of non-compliance within the next three months*;
  submit a **realistic recovery plan within two months** for PRA approval; restore eligible
  own funds covering the SCR or reduce the risk profile **within six months** (extendable
  under s.138A or s.138BA FSMA). **3.2** where the PRA has extended that period by reason
  of a declared **exceptional adverse situation** [R43], submit a progress report **every
  three months**. **4.1 (MCR breach)** inform the PRA immediately, and **within one month**
  submit a **short-term realistic finance scheme** for approval, to restore eligible own
  funds to at least the MCR or reduce the risk profile **within three months**. **5.1** a
  recovery plan or finance scheme must contain estimates of management expenses and
  commissions; estimates of income and expenditure for direct business, reinsurance
  accepted and reinsurance ceded; a **forecast balance sheet**; estimates of the financial
  resources intended to cover technical provisions, the SCR and the MCR; and the firm's
  overall reinsurance policy. Related guidance named on the Part page: **SoP12/24 — the
  PRA's approach to the permissible recovery period for insurers to restore full cover for
  their SCR (not retrieved)**. **The Part contains no rule withdrawing authorisation on an
  MCR breach**; if that consequence exists in UK law it sits outside this Part and **was
  not located**.

### R80. PRA Rulebook — With-Profits Part (as at 05/08/2026), with the Glossary definitions of *ring-fenced fund* and *restricted own funds*
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.prarulebook.co.uk/pra-rules/with-profits/05-08-2026
- **Accessed:** 2026-08-06
- **Fetched:** yes (3,368 chars; read in full — the Part is four short chapters; Glossary
  letter R page retrieved separately, 18,060 chars). **Glossary letter S was not
  retrievable in that session** — see [R43] and [R45].
- **Annotation:** Verified: applies to a UK Solvency II firm carrying on with-profits
  insurance business, **except Holloway sickness policies** (1.1, 1.2). **2.1** the firm
  must hold assets in **each** with-profits fund of a value sufficient to cover the
  with-profits policy liabilities of all business written in or transferred into that fund.
  **3.1** the distribution strategy for discretionary benefits must be affordable and
  sustainable and must not reasonably be expected to have an adverse effect on the safety
  and soundness of the firm as a whole or on the benefit security of all policyholders.
  **4.1** support arrangements must be documented, including the circumstances in which
  they take effect, the terms of repayment, and the extent of any restriction on their use.
  All four chapters are date-stamped **01/01/2016** — the Part was untouched by PS15/24
  [R6]. **Glossary definitions verified from the letter R page:** *ring-fenced fund*
  (31/12/2024) = "an identifiable unit of assets and liabilities where the existence of a
  restriction on those assets in relation to those liabilities on a going concern basis
  gives rise to **restricted own funds**, **other than a matching adjustment portfolio**";
  *restricted own funds* (31/12/2024) = own funds items with reduced capacity to absorb
  losses on a going-concern basis due to lack of transferability, "**but does not include
  the value of future transfers attributable to shareholders**". Related guidance named on
  the Part page: SS1/14 [R117], SS14/15 [R71], SS22/15 (not retrieved).

### R80c. EIOPA — Guidelines on ring-fenced funds (EIOPA-BoS-14/169 EN), as republished by the Bank of England
- **Publisher:** EIOPA; republished on the Bank of England site and linked from the Own
  Funds Part page as an "Other link"
- **URL:** https://www.bankofengland.co.uk/-/media/boe/files/paper/2020/december/gl-ring-fenced-funds.pdf
- **Accessed:** 2026-08-06
- **Fetched:** yes (172,465-byte PDF → 33,454 chars; 13 pages, read in full)
- **Annotation:** Seventeen guidelines, cited from the Own Funds Part page [R77] and from
  SS14/15 footnote 4 [R71]. **Status caveat, which must travel with every citation:** every
  article reference in this document is to the **Solvency II Directive and Commission
  Delegated Regulation (EU) 2015/35** — Articles 80, 81, 216, 217, 227(2) and 234(b)(ii) DR
  and Articles 99(b), 104, 111(1)(h), 304 SII — **none of which is the operative UK
  citation any more**, because PS15/24 [R6] restated them into the Own Funds and SCR –
  Standard Formula Parts. The document carries a Bank of England application note pointing
  at **SoP1/19 — Interpretation of EU Guidelines and Recommendations (not retrieved)**,
  which is the instrument determining how far they still apply; and CP4/26 Proposal 4
  [R83c] proposes to restate the EIOPA guidelines on *classification of own funds* and
  *ancillary own funds* into PRA supervisory statements but **does not name the ring-fenced
  funds guidelines**, so as at 2026-08-06 these remain guidelines applied via SoP1/19
  rather than PRA text. Most load-bearing items verified: **Guideline 2(a)–(b)** —
  conventional unit-linked and index-linked products are **generally outside** the scope of
  ring-fenced funds; **Guideline 2(g)** — surplus funds are not ring-fenced solely by
  virtue of being surplus funds, but could be if generated within a ring-fenced fund;
  **Guideline 8** — future shareholder transfers are part of the RFF's excess of assets
  over liabilities, not a liability of the RFF; **Guideline 11 ¶1.26** — no adjustment where
  own funds inside the fund do not exceed its notional SCR; **Guideline 12 ¶1.29** — set any
  negative notional SCR to zero before aggregating. ¶1.15 applies Guidelines 6–17 to
  matching adjustment portfolios.

### R81. PRA Rulebook — Solvency Capital Requirement – Internal Models Part (as at 05/08/2026)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.prarulebook.co.uk/pra-rules/solvency-capital-requirement---internal-models/05-08-2026
- **Accessed:** 2026-08-06
- **Fetched:** yes (63,473 chars; read in full, chapter by chapter)
- **Annotation:** Structure: 1 (application and definitions), 2 (permission to use full and
  partial models), 3 (applications), 4 (partial-model applications), 5 (transitional plan
  to *extend* scope), 5A (transitional plan to *reduce* scope), 5B (internal model
  safeguards), 6 (model change and the model change policy), 7 (governing body
  responsibilities), 8 (no reversion to the standard formula), 9 (non-compliance), **10
  (use test)**, **11 (statistical quality standards)**, **12 (calibration standards)**, 13
  (profit and loss attribution — `[Deleted]`), **13A (analysis of change)**, **14
  (validation standards)**, **15 (documentation standards)**, 16 (external models and
  data), 16A (integration of partial internal models), 16B–16G (integration techniques),
  17 (Lloyd's). "Internal model requirements" means **Chapters 10 to 16A** [R81b ¶1.3].
  Three definitions in 1.2 (24/07/2025): *coverage* = the risks reflected in the
  probability distribution forecast; *internal model safeguard* = a limitation or
  requirement imposed by the PRA addressing a residual model limitation; *unit of the
  partial internal model* = a component separately calculated and not aggregated within the
  partial model. Rule **3.4** requires a firm with model permission to provide the PRA, on
  request, with an estimate of the standard formula SCR [R68]. Every substantive chapter is
  date-stamped **31/12/2024** except 12.1–12.3, 11.3, 11.5–11.7, 15.1, 16.1, 7.2 and 17
  (01/01/2016) and 1.2 / 16F.3 (24/07/2025). An internal model is an **entity-level
  permission**, so its demands fall on the firm's whole liability model estate, not on one
  product.

### R81b. SS1/24 — Expectations for meeting the PRA's internal model requirements for insurers under Solvency II (February 2024)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URLs:** PDF read
  https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/supervisory-statement/2024/ss124-february-2024-update.pdf
  ; publication page
  https://www.bankofengland.co.uk/prudential-regulation/publication/2024/february/expectations-for-meeting-the-pra-internal-model-requirements-ss
- **Accessed:** 2026-08-06
- **Fetched:** yes (1,701,124-byte PDF → 14,209 chars; 8 pages, read in full)
- **Annotation:** Published 28 February 2024 as part of PS2/24 [R7]; **effective from 31
  December 2024**. Verified: ¶1.3 defines "internal model requirements" as **SCR – Internal
  Models 10 to 16A** [R81]. The probability distribution forecast of a partial model is
  expected to be calculated **at the highest level of aggregation of the partial model's
  components**, and separately for each component not aggregated within it (¶2.1);
  **including a new risk is expected to be a major model change** with two narrow
  exceptions (¶¶2.2–2.3); accuracy, completeness and appropriateness of data are given
  operational definitions (¶¶2.4–2.6); the validation process must cover SCR-GP 3.2–3.5
  [R61] and SCR-IM 3.2, 10–13A and 15–16A (¶2.7); and the PRA expects **an annual written
  attestation by an appropriate SMF, "in most cases the Chief Risk Officer (SMF4)"**, that
  the firm satisfies SCR-GP 3.3–3.4 and the internal model requirements, or has a credible
  plan to address identified non-compliance (¶2.10). ¶¶2.13–2.15 set the documentation
  standard — an independent knowledgeable third party must be able to understand the model
  and judge compliance, and the PRA expects firms to be able to **reproduce model outputs
  from the documentation plus the inputs** — with a 14-item minimum documentation content
  list. **Duplicate record:** R97b, which is the **publication page only** and whose content
  is `[unverified]` beyond a scope list — **cite R81b**, which is the document read in full.

---

## 11. Regulatory reporting, disclosure and governance (R84–R98)

Entries from `uk/_research/solvency-uk-reporting-governance.md`. **R97b and R97c have no
entry here** — they are that stream's numbers for [R81b] and [R68]. All URLs requested on
**2026-08-06** with a browser User-Agent and returning HTTP 200 unless noted. PRA Rulebook
Parts were read in the **05/08/2026 "present" view** and, for the Reporting Part,
additionally in the **31/12/2026 "future" view**; the date segment in the URL is the
version identifier.

### R84. PRA Rulebook — Reporting Part (as at 05/08/2026, and future view as at 31/12/2026)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URLs:** https://www.prarulebook.co.uk/pra-rules/reporting/05-08-2026 (present view,
  989,845 bytes) ; https://www.prarulebook.co.uk/pra-rules/reporting/31-12-2026 (future
  view, 1,071,104 bytes)
- **Accessed:** 2026-08-06
- **Fetched:** yes (both views; converted to text and read in full)
- **Annotation:** The most load-bearing source in this section — the UK counterpart in
  structural role to the NAIC Annual Statement Instructions, though not in content.
  Structure verified: **Chapter 1** application and definitions; **Chapter 2** reporting to
  the PRA (2.1–2.5B the inventory of what must be submitted and every deadline; 2.6–2.12
  and 2.14 all `[Deleted]`; 2.13 electronic format); **Chapter 2A** "Reports and Templates"
  — Articles 1–4A general, 5–21A solo, 22–36 groups, 37–50 third-country branches;
  **Chapter 3** public disclosure: SFCR (3.1–3.10); **Chapter 3A** SFCR report and
  templates — Articles 1A (SFCR structure), 2–3B (format, materiality, means of
  disclosure), 4 (solo disclosure templates), 5 (group), 6–8; **Chapter 4** permitted
  non-disclosure; **Chapter 5** updates and major developments; **Chapter 6** policy and
  governing-body approval of the SFCR; **Chapter 7** Lloyd's; **Chapter 8 "National
  Specific Templates" — entirely `[Deleted]` at 31/12/2024**; **Chapter 9** the template
  inventory, each rule pointing to an externally hosted template file; **Chapter 10** the
  instruction ("LOG") files, likewise externally hosted [R88]. Verified that the Chapter 9
  inventory contains **99 distinct template code stems** (IR.01.01 … IR.36.04 plus the
  IRR.xx series) and that **no IR.13.01 exists**. Verified that the **only** narrative
  reports required are the ORSA report, the third-country-branch resolution report, and the
  qualitative packs supporting QMC.01, AoC.01 and MALIR (rule 2.5A(2)). The 31/12/2026 view
  adds the liquidity reporting Articles 51–54A and rules 2.5B(11A)–(11F), and replaces
  MALIR 1–7 with templates MA.00.01, MA.00.02, MA.01.01, MA.02.01 and MA.03.01 [R87][R91].
  Note that the Part no longer hard-codes size-based reporting exemptions: Articles
  10(1)(b), (c)(i) and (e) instead say a firm may be "exempted … in accordance with a
  direction given by the PRA under section 138A of FSMA" [R88b].

### R85. SS40/15 — Solvency II: reporting and disclosure
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.bankofengland.co.uk/prudential-regulation/publication/2015/solvency2-reporting-and-public-disclosure-options-provided-to-supervisory-authorities-ss
  (publication page; current version "published 15 November 2024, effective 31 December
  2024, following PS15/24")
- **Accessed:** 2026-08-06
- **Fetched:** yes (publication page; the November 2024 PDF text retrieved and read —
  36,029 characters, chapters 1, 4, 8–17 and the update annex)
- **Annotation:** The expectations layer on the Reporting Part. Verified: chapters 2, 3, 5,
  6, 7 and 10 are `[Deleted]`; the live chapters are 4 (accident vs underwriting year
  election), 8, 9, 11 (group reporting without consolidated financial statements), **12
  (information that should be disclosed in the SFCR)**, 13 (pre-defined events), **14
  (firms' processes for public disclosure)**, **15 (firms' processes for reporting)**, 16
  (quantitative reporting and validations) and 17 (SFCR dispensation). **§12.10 is the only
  SFCR technical-provisions expectation:** firms "should describe the significant
  simplified methods used to calculate technical provisions, including those used for
  calculating the risk margin". §15.2 requires **annual QRTs to be approved by the governing
  body before submission**; §15.3 requires **quarterly QRTs to be approved by the management
  body or by persons who effectively run the firm**. §16.1–16.2 require firms to follow the
  Bank's published **data point model** and **validation rules** [R88]. §13.1 requires
  immediate written notification of "pre-defined events". **Observed defect, recorded not
  resolved:** the retrieved PDF carries an unresolved placeholder header on page 1 — "This
  SS is effective from 31 December 2024 and is published as part of **PSX/24**. Please see
  https://www.bankofengland.co.uk/prudential-regulation/publication/2024/**XXXXX**" — while
  its annex records the November 2024 update as following PS15/24 [R6].

### R86. PS3/24 — Review of Solvency II: Reporting and disclosure phase 2 near-final (29 February 2024)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.bankofengland.co.uk/prudential-regulation/publication/2024/february/review-of-solvency-ii-reporting-disclosure-phase-2-near-final-policy-statement
- **Accessed:** 2026-08-06
- **Fetched:** yes (123,068 characters read)
- **Annotation:** The policy record of how the UK reporting package was cut down, and the
  only place that explains *why* particular templates survive. Responds to CP14/22 and
  CP12/23 chapter 7. Verified changes: **permanent deletion of a number of QRTs, associated
  disclosure templates and relevant NSTs**; frequency reductions from quarterly to
  semi-annual or annual; consolidation of overseas-activity and SCR reporting;
  activity-based reporting thresholds; **three new templates on excess capital generation,
  cyber underwriting risk and non-life product obligations** (the non-life product
  obligations template S.14.02 was **not implemented** — ¶4.4); deletion of SS36/15, SS6/18
  and SS11/15; a new statement of policy on reporting waivers [R88b]; and **removal of the
  RSR for all firms including third-country branches** (¶1.8). **Implementation (¶1.30):**
  "This policy will come into effect on Tuesday 31st December 2024 for triennial, annual,
  semi-annual and quarterly requirements with a reporting or disclosure reference date as
  of 31 December 2024 and onwards. By exception, **the requirement to submit the RSR ceased
  on 31 December 2023**." Life-relevant feedback verified: ¶¶4.10–4.17 excess capital
  generation, proposed as NS.14 for life firms writing **non-unit-linked premiums exceeding
  £1 billion annually**, solo only, not groups, with the PRA declining to fold it into the
  ORSA because ORSAs "are submitted by firms throughout the calendar year, data may be
  received from firms many months apart, compromising comparability"; ¶¶4.35–4.37 life
  obligations analysis, S.14 retained **because "there is no product split in other
  Solvency II templates (eg S.05 or S.12.01)"**; ¶¶4.68–4.70 projection of future cash flows
  in the best estimate, where S.13.01 and SR.22.02 are stated to "continue to be collected"
  — **contradicted by the final Rulebook [R84], which contains no IR.13.01; recorded, not
  resolved**; ¶¶4.74–4.77 the new S/SR.25.04, 25.05 and 25.06 SCR templates. Also the source
  for the removal of **EPIFP** from Solvency UK reporting and disclosure (¶¶4.43–4.44). The
  rules are described throughout as **near-final**; the final instruments are in PS15/24
  [R6][R42].

### R87. PS15/25 and PS18/26 — the post-restatement reporting policy statements
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URLs:** PS15/25 (published 30 September 2025)
  https://www.bankofengland.co.uk/prudential-regulation/publication/2025/september/closing-liquidity-reporting-gaps-and-streamlining-standard-formula-reporting-policy-statement
  ; PS18/26 (published 29 July 2026)
  https://www.bankofengland.co.uk/prudential-regulation/publication/2026/july/solvency-uk-policy-statement
  (also published at
  https://www.bankofengland.co.uk/prudential-regulation/publication/2026/july/solvency-uk-post-implementation-reporting-and-disclosure-amendments-and-own-funds-permissions-update)
- **Accessed:** 2026-08-06
- **Fetched:** yes (PS15/25 110,279 characters; PS18/26 66,992 / 67,062 characters read by
  two streams). **The amended Own Funds rule text in PS18/26 Appendix 3 was not retrieved**
  (separate PDF).
- **Annotation:** **Two documents, one entry** — the two changes to Solvency UK reporting
  since the 31/12/2024 restatement. **PS15/25**, *Closing liquidity reporting gaps and
  streamlining Standard Formula reporting*, responding to CP19/24. Verified: four new
  liquidity templates — a **monthly** "cash flow mismatch"; a **monthly** "cash flow
  mismatch (short form)" with a shorter remittance period, escalable to **every business
  day** in firm-specific or market liquidity stress; an **annual** "committed facilities";
  and a **quarterly** "liquidity market risk sensitivities" (¶1.10). Implementation
  **30 September 2026** (¶1.20), applying only to "a subset of larger UK Solvency II
  firms", **not** to Lloyd's, third-country branches or non-Solvency II firms (¶1.7). It
  also removed the expectation that life internal-model firms submit the annual **SF.01**
  standard-formula SCR template, effective on publication, so "firms in scope … will not be
  expected to submit an SF.01 report to the PRA from 31 December 2025 inclusive", and the
  year-end 2024 SF.01 is also not expected (¶1.22) [R68]. **PS18/26**, *Solvency UK:
  Post-implementation reporting and disclosure amendments and Own Funds permissions
  update*, responding to CP22/25 and CP4/26 Proposal 1 [R83c]. Verified: implementation
  "for reporting reference dates on or after Thursday 31 December 2026" (¶¶1.31–1.32); the
  **MALIR return moves from Excel to XBRL** with a restructured template set including a new
  MA.01.01 (¶1.11) [R91]; NACE 2.1 codes permitted from the 31 December 2026 reference date
  and mandatory later; **IR.14.01's "claims paid" definition is amended to exclude claims
  management expenses**, because "claims management expenses for life insurance business are
  a very small part of total expenses" and firm practice was inconsistent (¶2.41);
  cell-label standardisation across IR.02.01, IR.05.03, IRR.12.01, IR.12.05, IR.12.06,
  IR.25.04, IR.25.05 and the IR.26 series to "Z0020 Ring-fenced fund, matching adjustment
  portfolio or remaining part" and "Z0030 Fund/Portfolio number" (¶2.43); **deletion of
  SS37/15** (internal model reporting codes) (¶1.7). Chapter 3 finalises **CP4/26 Proposal
  1 broadly as consulted** (¶3.7), amending the Own Funds Part (Annex A of Appendix 3) and
  the Group Supervision Part, adopting the label **"equity- and liability-accounted
  subordinated instruments"** in IR.23.01–IR.23.04 (¶3.11), with the changes taking effect
  **31 December 2026** (¶3.19, ¶1.32); ¶3.13 records that the PRA declined to move
  equity-accounted subordinated liabilities into the subordinated-liabilities row of
  IR.02.01, so the two templates will continue to present them differently. **Duplicate
  record:** the own-funds stream numbered PS18/26 alone as R83d — **cite R87.**

### R88. Bank of England — Regulatory reporting: insurance sector (the template and instruction library)
- **Publisher:** Bank of England / PRA
- **URL:** https://www.bankofengland.co.uk/prudential-regulation/regulatory-reporting/regulatory-reporting-insurance-sector
  (page "last updated 01 May 2026"; 71,625 characters of text retrieved)
- **Accessed:** 2026-08-06
- **Fetched:** yes. **The XLSX template files themselves were not retrieved** — only the
  instruction (LOG) PDFs at [R89]–[R91].
- **Annotation:** Where Reporting Part Chapters 9 and 10 actually resolve to. The Rulebook
  text says only "The following IR.xx.yy templates can be found **here**" and "Section
  IR.xx.yy instructions can be found **here**" [R84]; the files live under
  `https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/regulatory-reporting/insurance/<code>-instructions-<title>-15-11-2024`
  (and `…-template-…` for the XLSX). Verified: **83 distinct instruction files, every one
  dated 15-11-2024** — i.e. all issued under PS15/24 [R6]. Verified page statements:
  "**Solvency UK now applies for all insurance regulatory reporting with reporting
  reference dates of 31 December 2024 and later**"; Bank of England Insurance **Taxonomy
  v2.0.1** (10 October 2024) for the 31 December 2024 reference date, **v2.0.2** (2 October
  2025) effective 1 January 2026 for reference dates on or after 31 December 2025,
  **v2.1.0** (16 December 2025) adding four liquidity entry points, and a **v2.2.0 public
  working draft** (21 April 2026) implementing CP22/25 and CP4/26. The page also still
  carries, as an archive, the **complete legacy NST inventory** — NS.00 Basic information,
  **NS.01 With-profits value of bonus**, **NS.02 With-profits assets and liabilities**,
  NS.03 Material pooling arrangements, NS.04 Assessable mutuals, **NS.05 Revenue account
  life**, **NS.06 Business model analysis (life)**, NS.07 and NS.08 non-life variants,
  **NS.09 Best estimate assumptions for life insurance risks**, NS.10, NS.11, NS.12 and
  NS.13 — **superseded** for reference dates from 31 December 2024 but the key to reading
  pre-2025 UK material.
- **R88b. SoP6/24 — Solvency II regulatory reporting waivers.** Publisher: PRA. URL:
  https://www.bankofengland.co.uk/prudential-regulation/publication/2024/february/solvency-ii-regulatory-reporting-waivers-sop
  . Accessed 2026-08-06. **Fetched: publication page only; the SoP PDF itself was not
  retrieved.** Verified from the page: first published 29 February 2024; **current version
  published 15 November 2024, effective 31 December 2024** (following PS15/24); a **future
  version published 21 May 2026, effective 31 December 2026** (following PS13/26). The SoP
  "lists the reporting covered by certain waivers and modifications by consents; and
  explains the steps a firm must take to apply" — which matters because the Reporting Part
  now routes size-based exemptions through a s.138A FSMA direction rather than hard-coding
  them [R84].
- **R88c. PRA — Solvency UK regulatory reporting: Questions & Answers, October 2025.**
  Publisher: PRA. URL:
  https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/regulatory-reporting/insurance/2025/october/solvency-uk-regulatory-reporting-reforms-qa-october-2025.pdf
  . Accessed 2026-08-06. Fetched: yes (20 pages, 33,272 characters). **Expressly "not
  PRA's reporting policy" on its own cover note** — carry that caveat with any citation.
  Verified operationally useful answers: returns are submitted through the **Bank of
  England Electronic Data Submission (BEEDS) portal** (A9); the **DIS (disclosure)
  templates are part of the taxonomy but are not submitted through BEEDS** — "It is the
  responsibility of the firm to publish its SFCR" (A6); where the Data Point Model
  conflicts with the instructions, "**policy and the reporting instructions must take
  precedence over the DPM**" (B4); reporting schedules with actual submission deadlines are
  published separately for December and non-December year ends (A3); interest payable and
  taxation are apportioned between IR.05.03 and IR.05.04 by fund allocation under
  Composites 2.2, or wholly to whichever is the larger part of the business (F9).

### R89. Reporting Part Chapter 10 — life technical provisions and obligations instruction files (IR.12.01, IR.12.04, IR.14.01)
- **Publisher:** Prudential Regulation Authority (Bank of England), all dated 15-11-2024
  (issued under PS15/24 [R6])
- **URLs:**
  IR.12.01 Life technical provisions —
  https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/regulatory-reporting/insurance/ir1201-instructions-life-technical-provisions-15-11-2024 ;
  IR.12.04 Best estimate assumptions for life insurance risks —
  https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/regulatory-reporting/insurance/ir1204-instructions-best-estimate-assumptions-for-life-insurance-risks-15-11-2024 ;
  IR.14.01 Life obligations analysis —
  https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/regulatory-reporting/insurance/ir1401-instructions-life-obligations-analysis-15-11-2024
- **Accessed:** 2026-08-06
- **Fetched:** yes (all three PDFs converted to text and read in full: 13,290 / 15,472 /
  11,920 characters). **The matching `…-template-…` XLSX files were not retrieved.**
- **Annotation:** These three files define, cell by cell, what a UK liability model must
  output. **IR.12.01** (quarterly *and* annual; entity, third-country branch, ring-fenced
  fund, MA portfolio and remaining part) fixes the six line-of-business columns and the
  technical-provision decomposition rows; it expressly permits approximations under TPFR 6
  [R41] and permits **SS8/24 §3.2** to be used to calculate the risk margin during the
  financial year. It carries three **unit-linked-only** rows (surrender value, nominal value
  of units, matching value of units) that no other template collects. **IR.12.04** is the
  assumption-and-experience template: it compares the current valuation basis against the
  prior-year basis and **five years of the firm's own experience**, names the underlying
  mortality/morbidity table, and states the CMI projection parameterisation [R22]–[R31]; its
  stated purpose is "to give an indication of changes in the valuation basis, how the basis
  compares with experience and the variability of the firm's recent experience". Its
  threshold is a **firm-level** test — gross BEL > £50m *or* gross written premiums > £10m
  for long-term business other than reinsurance — not a product test, and once in scope it
  has dedicated rows for term-assurance lapses, critical-illness claim rates,
  income-protection inception and termination, investment-bond surrenders, with-profits
  endowment lapses, annuitant mortality and annuity renewal unit costs. **IR.14.01** is the
  only PRA template with a **product split**, and its Appendix carries the **PRA life
  insurance product reporting code list** (three-digit codes, formerly SS36/15), which maps
  directly onto this library's seven products — reproduced in the product-code table below.

**PRA product-code mapping (from the IR.14.01 appendix, [R89])** — the exact codes each
library product must report under:

| Library product | PRA product ID code(s) |
|---|---|
| term-assurance | **404** level term regular premium; **414** level term single premium; **424** decreasing term regular premium; **434** decreasing term single premium |
| critical-illness | **444 / 454** accelerated critical illness, guaranteed / reviewable premiums; **464 / 474** stand-alone critical illness, guaranteed / reviewable premiums |
| income-protection | **494 / 504** income protection, guaranteed / reviewable premiums; **514** single premium; **524** income protection **claims in payment**; (480 CWP and 481 Holloway UWP for the participating forms) |
| whole-of-life | **104** whole of life OB NP (non-profit); **102** whole of life OB UL; **100 / 101** whole of life OB CWP / UWP; 105 / 106 industrial branch |
| with-profits | **111** single premium bond UWP (the with-profits bond); **100 / 101** whole of life CWP / UWP; **120 / 121** endowment OB CWP / UWP; **200 / 201**, **210 / 211** participating pensions |
| unit-linked-bond | **112** single premium bond UL (**113** if index-linked, **114** if non-profit) |
| pension-annuity | **724** individual pension annuity NP; **734** individual enhanced pension annuity NP; **720 / 722** individual pension annuity WP / UL; (700 / 704 purchased life annuity; 710 / 714 individual deferred annuity; **754** bulk purchase pension annuity — out of this library's scope) |

### R90. Reporting Part Chapter 10 — with-profits and life revenue/capital instruction files (IR.12.05, IR.12.06, IR.05.03, IR.05.10)
- **Publisher:** Prudential Regulation Authority (Bank of England), all dated 15-11-2024
- **URLs:**
  IR.12.05 With-profits value of bonus —
  https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/regulatory-reporting/insurance/ir1205-instructions-with-profits-value-of-bonus-15-11-2024 ;
  IR.12.06 With-profits liabilities and assets —
  https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/regulatory-reporting/insurance/ir1206-instructions-with-profits-liabilities-and-assets-15-11-2024 ;
  IR.05.03 Life income and expenditure —
  https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/regulatory-reporting/insurance/ir0503-instructions-life-income-and-expenditure-15-11-2024 ;
  IR.05.10 Excess capital generation —
  https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/regulatory-reporting/insurance/ir0510-instructions-excess-capital-generation-15-11-2024
- **Accessed:** 2026-08-06
- **Fetched:** yes (all four read in full: 3,046 / 6,677 / 12,238 / 11,201 characters)
- **Annotation:** **IR.12.05** (successor to NS.01) decomposes the year's distribution of
  profits as discretionary benefits into bonuses added at date of claim, clawback of past
  bonuses (market value reductions, entered negative), cash bonuses, reversionary bonuses
  "calculated in accordance with COBS 20.2.17R and any subsequent COBS rules" [R9] and
  other bonuses, then derives the **shareholder transfer** by an explicit formula. It states
  the market convention that "most with-profits funds are either '90:10' (shareholder
  entitled to 10% of surplus) or '100:0' (mutual or other funds where no shareholder
  entitlement)". **IR.12.06** (successor to NS.02) is the full realistic-balance-sheet
  decomposition: the with-profits benefits reserve (retrospective asset shares or
  prospective reserve, cross-referenced to **Surplus Funds 3.2 / 3.3 / 3.4** [R45]), six
  components of future policy related liabilities less two planned-deduction components, and
  the asset mix backing each; its row R0090 "future costs of financial options such as
  **guaranteed annuity rates**" is where a WOL or WP contract's GAR is reported, with the
  take-up assumption reported at IR.12.04 row R1250 [R89]. Its row R0150 must **tie to
  IR.12.01.01 R0030 C0010**. **IR.05.03** (successor to NS.05 "Revenue account life") is the
  life revenue account by line of business, reported on **financial-accounting** conventions
  rather than Solvency UK valuation, covering "all insurance business regardless of the
  possible different classification between investment contracts and insurance contracts
  applicable in the financial statements". **IR.05.10** is a genuine **forward-looking
  projection template**: one actual column plus **three business-plan years**, decomposing
  the movement in excess capital (eligible own funds less SCR); its scope test is on life
  premiums **excluding unit-linked premiums** [R84 Art 9(1)(k)], so a pure unit-linked-bond
  book cannot bring a firm into scope.

### R91. Reporting Part Chapter 10 — matching adjustment reporting instruction files (MALIR 1–7, IRR.22.02, IRR.22.03)
- **Publisher:** Prudential Regulation Authority (Bank of England), all dated 15-11-2024
- **URLs:**
  MALIR (all seven templates in one LOG file) —
  https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/regulatory-reporting/insurance/malir-instructions-15-11-2024 ;
  IRR.22.02 Matching adjustment portfolio projection of future cash flows —
  https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/regulatory-reporting/insurance/irr2202-instructions-matching-adjustment-portfolio-projection-of-future-cash-flows-15-11-2024 ;
  IRR.22.03 Matching adjustment calculation —
  https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/regulatory-reporting/insurance/irr2203-instructions-matching-adjustment-calculation-15-11-2024
- **Accessed:** 2026-08-06
- **Fetched:** yes (MALIR 48,344 characters — **MALIR 1, 2 and 3 read in full; MALIR 4–7
  headers and the appendix only**; IRR.22.02 2,687 and IRR.22.03 5,430 characters read in
  full). **The PS18/26 replacement instruction files (MA.00.01 … MA.03.01) were not
  retrieved** [R87].
- **Annotation:** Where a UK pension-annuity model's cash-flow output is actually consumed,
  and far more demanding than any other UK liability reporting. Verified from the MALIR LOG
  file: seven templates (**MALIR 1 Firm Information, 2 Asset cash flows, 3 Liability cash
  flows, 4 Portfolio Output, 5 Matching Tests, 6 Assets – Further Info, 7 Reconciliation**);
  **all seven apply to all firms with an MA permission**; **a separate MALIR is completed
  for each MA portfolio**; submission through **BEEDS within 130 business days after the
  firm's financial year end** (or twelve weeks after the end of the financial reporting
  period); "**All information in the MALIR should be provided at the effective date of 31
  December**"; amounts in **GBP millions**; every investment in IR.06.02, every derivative
  in IR.08.01 and **every reinsurance treaty** must be captured. MALIR 2 requires each asset
  line to be tagged with the **MA portfolio component A/B/C "as set out in chapter 4 of
  SS7/18"** [R8], the fundamental-spread table used (nine options), the credit quality step,
  the rating method and the notched ratings of Fitch, Moody's, S&P and any other CRA.
  **IRR.22.02** is the annual per-portfolio cash-flow projection. **IRR.22.03** carries the
  MA calculation outputs, including a **mortality-stress eligibility figure** and a
  Macaulay-equivalent liability duration; its row R0050 (increase of fundamental spread for
  sub-investment-grade assets) is expressly dead — "**This adjustment is no longer required
  by the matching adjustment rules and R0050 should be reported as zero from 31 December
  2024**".

### R92. PRA Rulebook — Conditions Governing Business Part (as at 05/08/2026)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.prarulebook.co.uk/pra-rules/conditions-governing-business/05-08-2026
  (355,375 bytes)
- **Accessed:** 2026-08-06
- **Fetched:** yes (browser User-Agent; converted to text and read)
- **Annotation:** The governance charter for anyone who builds or owns a UK liability model.
  Chapter list verified: 1 Application and Definitions; **1A Expert Judgement**; 2 General
  Governance Requirements; 2A System of Governance; **3 Risk Management** (which contains
  the ORSA rules at 3.8–3.12, the MA/VA liquidity plan at 3.1(3), and the MA and VA
  sensitivity requirements including the forced-sale effect at 3.2/3.3); 3A Remuneration
  Policy; **4 Internal Control**; 4A Specific Provisions – Functions; 5 Internal Audit;
  **6 Actuarial Function**; 7 Outsourcing; 8 Finite Reinsurance; 9 Restriction of Business;
  10 Premiums for New Business; 11 Statistical Data; **11A Alternative Methods for
  Valuation**; **11B Valuation of Technical Provisions – Validation**; **11C Valuation of
  Technical Provisions – Documentation**; **11D Internal Control of Valuation of Assets and
  Liabilities**; 11E Risk Management in Firms Providing Loans and/or Mortgage Insurance or
  Reinsurance; 12 Lloyd's. Rule 2.2(3) enumerates the system of governance as compliance
  with, among other things, the risk-management policy (2.5), Chapters 2A–7, Insurance –
  Fitness and Propriety, **Insurance – Allocation of Responsibilities 4** [R94], Chapters
  11A–11F, the risk-management system (3.1), the compliance function (4.1(2)), the internal
  audit function (Chapter 5) and the **actuarial function (Chapter 6)** — i.e. the "four key
  functions" in UK rule terms are risk management, compliance, internal audit and actuarial.
  Rule 2.3 makes the whole system proportionate to "the nature, scale and complexity of its
  operations"; 2.2(4) requires regular internal review. Rule 3.4 is the hook that makes
  compliance with the Investments Part demonstrable [R114][R119]. Most of the substance
  carries a **31/12/2024** date stamp (restated by PS15/24 [R6]); 3.2 carries **30/06/2024**
  (the MA reforms, PS10/24 [R5]); 6.1 and several older rules carry 01/01/2016.

### R93. PRA Rulebook — Actuaries Part (as at 05/08/2026)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.prarulebook.co.uk/pra-rules/actuaries/05-08-2026 (107,831 bytes)
- **Accessed:** 2026-08-06
- **Fetched:** yes
- **Annotation:** Short but load-bearing. Chapters: 1 Application and Definitions; 2
  Appointment of Actuaries; 3 Actuaries' Qualifications; 4 Conflicts of Interest; **5
  With-Profits Actuary Function**; 6 Duties of Actuaries; 7 Lloyd's. Verified: rule **2.1**
  — a firm "must appoint an **external actuary** if it does not have the capability within
  the firm or the firm's group to comply with **Conditions Governing Business 6**" [R92];
  i.e. **the UK does not require an appointed actuary as such** — it requires an effective
  actuarial function, and an external appointment only if the firm cannot staff it. Rule
  **2.2** — a firm carrying on with-profits insurance business "**must appoint one or more
  actuaries to perform the With-Profits Actuary function in respect of all classes of its
  with-profits insurance business**". Rule 2.3 vacancy-notification duties; **2.4** lets the
  PRA appoint an actuary itself, at the firm's expense, where a firm fails to fill a vacancy
  **within 28 days**. Rule **4.1** bars the appointed actuary from performing the Chief
  Executive function, bars the With-Profits Actuary from the governing body, and bars any
  other function giving rise to a significant conflict. Rule **5.1** sets the five
  substantive With-Profits Actuary duties. Rules 6.1–6.3 require objectivity, freedom from
  bias, and "due regard to **generally accepted actuarial practice**" — the rule hook for
  IFoA APS L1 [R35] and the FRC TASs [R33][R34]. Rules 6.4–6.5 require notification to the
  PRA without delay on removal, resignation, non-reappointment or disqualification.

### R94. PRA Rulebook — Insurance – Senior Management Functions Part and Insurance – Allocation of Responsibilities Part (as at 05/08/2026)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URLs:** https://www.prarulebook.co.uk/pra-rules/insurance---senior-management-functions/05-08-2026
  (221,346 bytes) ;
  https://www.prarulebook.co.uk/pra-rules/insurance---allocation-of-responsibilities/05-08-2026
  (190,115 bytes)
- **Accessed:** 2026-08-06
- **Fetched:** yes (both; **two Parts, one entry**)
- **Annotation:** Who is personally accountable for the model output and the return.
  Verified from **Insurance – Senior Management Functions**: rule 2.1 — each of the
  functions in Chapters 3–10 and 12 "is a controlled function and a PRA senior management
  function"; rule 2.2 — each holder must be individually approved by the PRA; rule **7.1** —
  "**The Chief Actuary function (SMF20) is the function of having responsibility for the
  actuarial function specified in Conditions Governing Business 6**" [R92]; rule **8.2** —
  "**The With-Profits Actuary function (SMF20a) is the function of having responsibility for
  advising the governing body of a firm transacting with-profits insurance business on the
  exercise of discretion affecting part or all of that business, as described more fully in
  Actuaries 5.1**" [R93], Chapter 8 applying "only to firms that carry on with-profits
  insurance business" (8.1). Rule 2.3 requires every firm (other than a third-country branch
  undertaking, a firm without a UK establishment, a small run-off firm or a UK ISPV) to have
  a Chief Executive function, a Chief Finance function and a Chair of the Governing Body
  function. Rule 2.4 (as amended 24/04/2026) gives a **12-weeks-in-12-months**
  temporary-cover carve-out. Verified from **Insurance – Allocation of Responsibilities**
  rule 3.1, the prescribed responsibilities: **PR Q — "responsibility for the production and
  integrity of the firm's financial information and its regulatory reporting"** (3.1(4));
  **PR T2 — "responsibility for performance of the firm's ORSA"** (3.1(7)); PR O —
  allocation and maintenance of capital and liquidity (3.1(5)); PR T — development and
  maintenance of the business model (3.1(6)); PR X — outsourcing under Conditions Governing
  Business 7 (3.1(12)). Rule 3A.2 sets the third-country-branch variants (PR AA, PR FF,
  PR EE, PR BB).

### R95. SS19/16 — Solvency II: ORSA (May 2026 version), with SS41/15
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URLs:** publication page
  https://www.bankofengland.co.uk/prudential-regulation/publication/2016/solvency2-orsa ;
  **May 2026 version** (effective 31 December 2026, published as part of PS13/26)
  https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/supervisory-statement/2026/ss1916-may-2026-update ;
  **November 2024 version** (effective 31 December 2024, PS15/24)
  https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/supervisory-statement/2024/ss1916-november-2024-update.pdf
- **Accessed:** 2026-08-06
- **Fetched:** yes (both PDFs retrieved and read: November 2024 14,189 characters, May 2026
  15,287 characters)
- **Annotation:** The PRA's expectations on the ORSA — the only forward-looking solvency
  assessment a UK firm must perform, and therefore the main consumer of a multi-year
  liability projection [R92 CGB 3.8–3.12]. Section list identical in both versions:
  Introduction; ORSA supervisory report; The ORSA policy; Board sign-off and embedding of
  the ORSA; Business strategy; Risks; Capital and solvency; Stress testing; Groups; Internal
  model; Standard formula. **The only material difference located between the two versions
  is scope**: the November 2024 text is addressed to "all UK Solvency II firms, including in
  the context of provisions relating to Solvency II groups, mutuals, **third-country
  branches** and to the Society of Lloyd's and its managing agents"; the **May 2026 text
  drops third-country branches**, consistent with PS13/26. **No paragraph-by-paragraph diff
  was performed — [unverified] beyond the scope sentence.** §10.1 cites **Guideline 10 of
  EIOPA-BoS-14/259** (ORSA) by name, which is live in the UK only through [R95b].
- **R95b. SS41/15 — Solvency II: applying EIOPA's Set 2, System of Governance and ORSA
  Guidelines (November 2024).** Publisher: PRA. URLs: publication page
  https://www.bankofengland.co.uk/prudential-regulation/publication/2015/solvency2-applying-eiopa-set2-system-of-governance-and-orsa-guidelines-ss
  ; PDF
  https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/supervisory-statement/2024/ss4115-november-2024-update.pdf
  . Accessed 2026-08-06. Fetched: yes (10,166 characters read in full). **This is the
  instrument that keeps the EIOPA guidelines alive in the UK:** §2.2 — "The PRA expects
  firms to **comply with all of the Set 2, System of Governance and ORSA Guidelines (as at
  the end of the transition period) that apply to them, in a proportionate manner**." The
  Guidelines are EIOPA's Set 2 (final reports 6 July 2015) and the System of Governance and
  ORSA Guidelines (final reports 3 February 2015). §§3.1–3.3 deal with the **Valuation 5.4
  derogation** [R39], pointing to **SS38/15** [R40] for which financial reporting standards
  are consistent with Article 75. The research file records **§6.1 as a live defect** in the
  published document.

### R96. PRA Rulebook — External Audit Part (as at 05/08/2026), with SS11/16
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.prarulebook.co.uk/pra-rules/external-audit/05-08-2026 (94,830 bytes)
- **Accessed:** 2026-08-06
- **Fetched:** yes
- **Annotation:** The rule that makes part of the SFCR — including the life
  technical-provisions template [R89] — subject to a **reasonable assurance** audit opinion,
  and the rule that decides which firms escape it via a **quantitative score built directly
  out of reported template cells**. Chapters: 1 Application and Definitions (1.3 carries the
  definitions and the score formula, last amended **21/10/2025**); 2 External Audit of
  Relevant Elements of the SFCR; 3 Appointment of Auditors; 4 Duties on the External
  Auditor. Applies to a UK Solvency II firm "that is **not a small firm for external audit
  purposes**" and, at group level, to a group that is not a small group (1.1), in respect of
  financial years ending on or after 15 November 2016 (1.2).
- **R96b. SS11/16 — Solvency II: External audit of, and responsibilities of the governing
  body in relation to, the public disclosure requirement (November 2024, updating June
  2024).** Publisher: PRA. URL: publication page
  https://www.bankofengland.co.uk/prudential-regulation/publication/2016/solvency2-external-audit-of-the-public-disclosure-requirement-ss
  ("Current version published on 15 November 2024. Effective from 31 December 2024.
  Following PS15/24"). Accessed 2026-08-06. Fetched: yes (PDF text 28,604 characters read).
  Verified: §§2.1–2.3 the PRA expects the governing body to take responsibility for the SFCR
  being properly prepared, to be satisfied that the firm complied in all material respects
  throughout the year and that it is reasonable to believe it will continue to comply, and
  to "**acknowledge and evidence in writing its responsibility for the SFCR … by signing the
  SFCR and attaching the written acknowledgment to the SFCR**". §3.1 defines the required
  assurance level as **reasonable assurance** under ISA (UK) 200. §3.4 the auditor "is not
  expected to express an opinion on the validity of an approval, waiver or other supervisory
  determination", and **transitional measures on technical provisions are treated "as part
  of the framework against which the audit opinion is being given"** [R3][R57]. §3.5 applies
  ISA (UK) 720 to the unaudited remainder of the SFCR. §§4.2A–4.2F set the
  matching-adjustment position: **auditors are not required to assess MA eligibility, but
  are expected to consider the scale of the MA claimed**, because "the impact of the MA on
  technical provisions falls within the relevant elements", and the PRA "does not approve
  the firm's calculation methodology as part of [the MA application] process" [R2][R60].

### R97. SS17/16 — Solvency II: internal models – assessment, model change and the role of non-executive directors
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URLs:** publication page
  https://www.bankofengland.co.uk/prudential-regulation/publication/2016/solvency2-internal-models-assessment-model-change-and-the-role-of-non-executive-directors-ss
  ("Current version published on 15 November 2024. Effective from 31 December 2024.
  Following PS15/24") ; **February 2024 version**
  https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/supervisory-statement/2024/ss1716-28-february-2024-update.pdf
- **Accessed:** 2026-08-06
- **Fetched:** **partial.** The publication page was retrieved and read; the **February 2024
  PDF** was retrieved and read (45,926 characters) **but is stamped on every page "31
  December 2024: This document has been superseded"**; the **current November 2024 PDF was
  not retrieved** — two guessed media URLs returned HTTP 404 and the page's PDF links are
  script-rendered.
- **Annotation:** The model-governance expectations a liability-model builder must satisfy
  where the model feeds an internal model [R81][R81b]. Chapter list (February 2024 text): 1
  Introduction; 2 Application for internal model permission; 3 [Deleted]; 4 Modelling of the
  premium provision for general insurance firms; 5 [Deleted]; **6 Role of non-executive
  directors**; **7 Validation of models**; 8 How the PRA uses quantitative analyses as part
  of model permission; **9 Internal model change policy**; **10 Reporting of analysis of
  change in SCR**. Chapter 7 is the substantive part: model **justification** and model
  **validation** are two separate processes that firms must demonstrably demarcate (7.1);
  justification sits under the Statistical Quality Standards in SCR – Internal Models 11 and
  16.2 and "it is **not the aim of the validation process to create a substitute for these
  requirements**" (7.3); validation is "regular and independent (from the development and
  operation of the model)" and reviews specification appropriateness, "the **correspondence
  of its results against experience**" and overall performance over time (7.4); the PRA
  expects "a combination of detailed 'bottom-up' testing and 'top-down' ownership by boards"
  (7.6) and evidence that the board challenged the validation, understood the key
  assumptions and limitations, **considered the possible quantification of those
  limitations** and took mitigating actions (7.8); and validation "should put specific
  attention on those key assumptions and **expert judgments** that have a material impact on
  the model" (7.12). **Because the retrieved text is the superseded February 2024 version,
  paragraph numbers should be re-verified against the November 2024 PDF before citation in a
  product document.**

### R98. PRA Rulebook — Preparations for Solvent Exit Part (as at 05/08/2026), with SS11/24
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URLs:** https://www.prarulebook.co.uk/pra-rules/preparations-for-solvent-exit/05-08-2026
  (55,295 bytes) ; SS11/24 PDF
  https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/supervisory-statement/2024/ss1124-december-2024.pdf
  ; SS11/24 publication page
  https://www.bankofengland.co.uk/prudential-regulation/publication/2024/december/solvent-exit-planning-for-insurers-supervisory-statement
- **Accessed:** 2026-08-06
- **Fetched:** yes (Rulebook Part read in full — three chapters; **SS11/24 PDF text 35,169
  characters read in part** — contents, chapter 1 and the solvent-exit-analysis sections)
- **Annotation:** A **new UK-only planning obligation with no Solvency II ancestor**, and
  the newest rule in this half of the page: every rule in the Part carries the effective
  date **30/06/2026**. Verified from the Part: it applies to a UK Solvency II firm, a
  non-directive insurer and (via Insurance General Application 3) the Society (1.1),
  **excluding passive run-off firms** (1.2); 1.3 defines **solvent exit** as "the process
  through which a firm ceases its insurance business while remaining solvent" and **solvent
  exit analysis** as "a document setting out a firm's preparations for solvent exit". Rule
  **2.1** requires a firm to (1) prepare for solvent exit so it can effect one in an orderly
  manner, (2) **produce a solvent exit analysis and update it whenever a material change has
  taken place … and at least once every three years**, (3) for a UK Solvency II firm in a
  group, take account of group implications and risks, and (4) provide the current version
  to the PRA on request. Verified from SS11/24: it applies to all PRA-regulated insurers
  **except firms in passive run-off, UK branches of overseas insurers and Lloyd's managing
  agents** (1.2); a solvent exit may be achieved by run-off, sale or partial sale, merger, a
  **Part VII FSMA transfer**, a scheme of arrangement and/or restructuring plan, or a
  combination (1.3); the SS is structured as chapter 2 (preparing a solvent exit analysis —
  solvent exit actions, **solvent exit indicators**, potential barriers and risks, resources
  and costs, communications, governance and decision-making, assurance) and chapter 3
  (producing a **solvent exit execution plan (SEEP)** and executing a solvent exit).
  **Document defect, recorded not resolved:** the PDF's cover page is headed "Supervisory
  statement | **SS11/24**" while its page 2 masthead reads "Supervisory statement |
  **SS20/24**"; the Bank's publication page confirms **SS11/24** is the supervisory
  statement and **PS20/24** the accompanying policy statement.

---

## 12. The statutory accounts — UK GAAP, company law, and IFRS 17 as adopted (R99–R107)

Entries from `uk/_research/uk-accounting-and-tax.md`. **R111 and R112 have no entry here**
— they are that stream's numbers for [R39] Chapter 11 and [R62] Chapter 6. All accessed
**2026-08-06**; PDFs were downloaded and text-extracted locally with `pypdf`, HTML with
BeautifulSoup. **This is the "statutory accounts" layer, not a solvency measurement**; see
the terminology table in the header.

### R99. FRS 103 Insurance Contracts (September 2024 edition)
- **Publisher:** Financial Reporting Council
- **URL:** https://www.frc.org.uk/documents/7669/FRS_103_September_2024_rSi5poe.pdf (from
  the FRC library page at [R101])
- **Accessed:** 2026-08-06
- **Fetched:** yes (PDF, 593,853 bytes → 171,294 chars; Sections 1–6, Appendix I Glossary,
  Appendix III and the Basis for Conclusions read directly). **Retrieval limits that must
  travel with citations:** ¶¶2.16 (tail), 2.17 and 2.18 — the alternative
  liability-adequacy measurement where the entity's own test fails the minimum requirements
  — **were read only in part**; and **Appendix II (Definition of an insurance contract) was
  not read at all**, so the significant-insurance-risk test that decides whether a UK
  product is an insurance or an investment contract rests here on the glossary definition
  and on HMRC's description [R18 LAM01100], not on ¶¶A2.1–A2.24.
- **Annotation:** The operative UK GAAP standard for insurance contracts. Structure:
  Section 1 Scope; Section 2 Accounting Policies / Recognition and Measurement; Section 3
  Recognition and Measurement — requirements for entities with long-term insurance business;
  Section 4 Disclosure; Section 5 Disclosure — additional requirements for with-profits
  business; Section 6 Transition; Appendices I Glossary, II Definition of an insurance
  contract, III Note on legal requirements, IV Republic of Ireland references; Basis for
  Conclusions. Verified content load-bearing for this library: applies to entities applying
  FRS 102 [R102], insurer or not, to insurance contracts issued, reinsurance held, and other
  financial instruments issued with a discretionary participation feature (¶1.2); effective
  for periods beginning on or after 1 January 2015 (¶1.11), with **Periodic Review 2024
  amendments effective for periods beginning on or after 1 January 2026 except the Section 6
  amendment, effective 1 January 2024** (¶1.11D); policy change permitted only under ¶2.3,
  with alignment to the PRA Rulebook technical-provisions rules named as one legitimate
  basis for change (¶2.3A) and as an alternative starting point for first-time
  policy-setters (¶1.5(b)); liability adequacy test (¶¶2.14–2.18); DPF guaranteed
  element/equity split (¶2.30); shadow accounting (¶2.11); unbundling of deposit components
  (¶2.23); premium and claim recognition (¶¶3.3–3.6); **acquisition costs shall be
  deferred** subject to three carve-outs (¶3.7) and amortised over no longer than the
  recoverability period and "in a similar profile to those margins" (¶3.9); **acquisition
  costs shall not be deferred for with-profits funds** (¶3.10); MSSB as the established
  basis and realistic value of liabilities for with-profits funds (¶¶3.11–3.15); VIF
  (¶¶3.16–3.18); FFA disclosure and negative-FFA explanation (¶¶5.4–5.5). Glossary
  definitions verified include MSSB, realistic value of liabilities (defined by reference to
  **INSPRU 1.3.40 as at 31 December 2015** [R116]), gross premium method, net premium
  method, linked business, technical account, non-technical account, PPFM, DPF, liability
  adequacy test, deferred acquisition costs (long-term business), options and guarantees,
  "Regulations" = SI 2008/410 [R105] and "Act" = Companies Act 2006 [R103]. Basis for
  Conclusions ¶¶43–55 record the May 2016 Solvency II amendments, the **deliberate decision
  not to require a Solvency II-based measurement** (BC45), the reason the INSPRU-anchored
  definitions were kept (BC49–BC50), and (BC55) the four items to consider adjusting if an
  entity does build policies off the prudential rules. **Conflict recorded, not resolved:**
  ¶3.7 opens "Except as required by paragraph 3.10", but ¶3.1(b) restricts ¶¶3.10–3.15 to
  with-profits business within the **pre-2016 PRA realistic capital regime**, and IG1.1
  makes ¶3.12 optional outside that scope [R100]. **Whether the ¶3.10 DAC prohibition
  reaches a with-profits fund that was never in the realistic regime is not settled by the
  retrieved text. Do not assert either reading.**

### R100. Implementation Guidance to accompany FRS 103 Insurance Contracts (September 2024)
- **Publisher:** Financial Reporting Council
- **URL:** https://www.frc.org.uk/documents/7663/Implementation_Guidance_to_accompany_FRS_103_Insurance_Contracts_September_2024_HvmQYVX.pdf
- **Accessed:** 2026-08-06
- **Fetched:** yes (PDF, 377,687 bytes → 81,231 chars; **page 1 text extraction failed**, so
  the cover page content is not recorded; all substantive pages extracted; Section 1
  (IG1.1–IG1.13) and the long-term parts of Section 2 read). **Section 3 (capital
  disclosures for entities with long-term insurance business) was not read**, beyond the
  cross-reference at IG1.12 to IG3.14(c).
- **Annotation:** Explicitly "accompanies, but is not part of, FRS 103" and **does not carry
  the authority of a standard** [R101]. It is nonetheless the only published UK source that
  says how to compute the with-profits adjustments. Verified: **IG1.2** the shareholders'
  share of projected future bonuses is the value of future shareholder transfers on
  **market-consistent financial assumptions**, with non-economic assumptions consistent with
  the realistic value of liabilities, taken to the FFA together with any related tax
  liability; **IG1.3–IG1.9** recognition and measurement of the VIF on non-participating
  business inside a with-profits fund, including the requirement to strip out any release of
  capital requirements from the VIF because MSSB liabilities carry no capital allowance
  (IG1.7); **IG1.10** realistic-versus-MSSB differences are transferred to and from the FFA
  so there is **generally no effect on profit or equity**, except where the FFA goes
  negative; **IG1.11–IG1.13** options and guarantees measured at fair value or by
  market-consistent stochastic model, deterministic approaches "generally fail to deal
  appropriately with the time value of the option", management actions in each scenario must
  be implementable and consistent with the PPFM [R9]. Section 2 verified: **IG2.39** gross
  premium method for every class except those valued by net premium method in the regulatory
  returns; **IG2.41** no policy may have an overall negative provision except as allowed by
  PRA rules, nor a provision below any guaranteed surrender or transfer value; **IG2.42** the
  long-term business provision may be computed on the regulatory basis subject to appropriate
  adjustments; **IG2.43** the assumption categories to disclose; **IG2.44 and IG2.49** where
  the provision or the linked-liability provision has regard to the timing of tax, that
  effect must be **excluded from the determination of deferred tax**; **IG2.45**
  with-profits future-bonus allowance disclosure; **IG2.47–IG2.48** the linked provision
  must not be below the fund-referenced surrender/transfer value, and mismatching between
  net linked assets and linked technical provisions must be explained; **IG2.50** an FFA is
  appropriate only where allocation between policyholders and owners is not clear cut;
  **IG2.61** reinsurance assets measured consistently with the related liability.

### R101. FRC library page — FRS 103 Insurance Contracts
- **Publisher:** Financial Reporting Council
- **URL:** https://www.frc.org.uk/library/standards-codes-policy/accounting-and-reporting/uk-accounting-standards/frs-103/
- **Accessed:** 2026-08-06
- **Fetched:** yes (HTML)
- **Annotation:** A genuinely different document from the standard, and **the only place the
  FRC states its position on FRS 103 versus IFRS 17**. Verified verbatim: "FRS 103 is not
  aligned with IFRS 17"; the FRC "is likely to wait for several years' implementation
  experience before considering alignment"; "Conflicts between IFRS 17 and UK company law
  mean that it is not currently possible to align FRS 103 with IFRS 17"; entities applying
  FRS 103 "will necessarily be preparing 'Companies Act accounts' as set out in section
  395(1) of the Companies Act 2006" [R103]; the form and content of Companies Act individual
  accounts of insurance companies must comply with **Schedule 3 to SI 2008/410, "which
  cannot be adapted"** [R105]; and the FRC "concluded in 2019 that the approach and
  methodology that underpins IFRS 17 is so fundamentally different to the one that underpins
  the formats of Schedule 3 that for Companies Act accounts it is not possible to apply
  IFRS 17 whilst continuing to maintain compliance with company law." Also verified: the
  current edition is September 2024 (published 10 September 2024, 579.9 KB); superseded
  editions January 2022, March 2018, February 2017, March 2014; the Periodic Review 2024
  amendment (27 March 2024) is effective 1 January 2026 with early application permitted,
  except a Section 6 Transition requirement effective 1 January 2024; a May 2016 "Amendments
  to FRS 103 – Solvency II" amendment exists; and the February 2017 BEIS letter [R113] is
  published here.

### R102. FRS 102 The Financial Reporting Standard applicable in the UK and Republic of Ireland (September 2024 edition)
- **Publisher:** Financial Reporting Council
- **URL:** https://www.frc.org.uk/documents/7668/FRS_102_September_2024_tmKYWO6.pdf
- **Accessed:** 2026-08-06
- **Fetched:** yes (PDF, 2,829,292 bytes → 1,336,205 chars; **Section 1 scope, Section
  7.10E, Section 29 Income Tax and the Section 29 Basis for Conclusions read; the rest
  indexed by search only**)
- **Annotation:** The host standard. Verified: **¶1.6** — an entity **shall apply FRS 103**
  to insurance contracts it issues, reinsurance contracts it holds, and financial instruments
  with a DPF that it issues, so FRS 102 itself contains **no insurance measurement model**;
  insurance contracts and DPF instruments are carved out of Sections 11, 12, 21, 22 and 23 by
  cross-reference to FRS 103 [R99]. **Section 29 Income Tax** verified in detail because it
  is the UK GAAP deferred-tax model and **differs structurally from IAS 12**: ¶29.6 deferred
  tax is recognised on **timing differences** — "differences between taxable profits and
  total comprehensive income … that arise from the inclusion of income and expenses in tax
  assessments in periods different from those in which they are recognised in financial
  statements" — **not** on balance-sheet temporary differences; ¶29.7 deferred tax assets
  only to the extent probable of recovery; ¶29.10 no deferred tax on permanent differences
  except ¶29.11 business combinations; ¶29.12 measurement at rates enacted or substantively
  enacted at the reporting date expected to apply on reversal; ¶29.13 average rates where
  rates are banded; ¶29.16 deferred tax on fair-valued investment property; ¶29.2B and
  ¶29.12A exclude Pillar Two deferred tax from recognition, disclosure and measurement.
  Basis for Conclusions B29.1–B29.7 confirms the FRC deliberately adopted a "timing
  differences plus" approach rather than IAS 12's temporary-difference model — **which is why
  the accounts deferred tax and the Solvency UK deferred tax under Valuation 11 [R39] are not
  the same number.** ¶7.10E: an insurance financial institution should include the cash flows
  of its long-term business "only to the extent of cash transferred and available to meet the
  obligations of the company or group as a whole" — the cash-flow-statement counterpart of the
  long-term-fund ring-fence.
- **R102b. FRC library page — FRS 102.** Publisher: FRC. URL:
  https://www.frc.org.uk/library/standards-codes-policy/accounting-and-reporting/uk-accounting-standards/frs-102/
  . Accessed 2026-08-06. Fetched: yes. Verified: FRS 102 is periodically reviewed roughly
  every five years; the Triennial Review 2017 was effective 1 January 2019; the **Periodic
  Review 2024 was completed in March 2024 with a principal effective date of 1 January
  2026**; a further amendment "Adapted formats" published 18 February 2026 is effective
  **1 January 2027**, arising from the replacement of IAS 1 by IFRS 18 and relating
  "principally to entities which choose to adapt one of the balance sheet formats and/or one
  of the profit and loss account formats". **The Adapted formats amendment document itself
  was not fetched, and whether it touches the Schedule 3 insurance formats [R105] was not
  determined.** A document describing "current UK GAAP" must state which edition it means.

### R103. Companies Act 2006, Part 15 — accounts and reports (s.395 read; s.396 by cross-reference)
- **Publisher:** legislation.gov.uk
- **URLs:** https://www.legislation.gov.uk/ukpga/2006/46/section/395 ; Part 15 Chapter 4 also
  retrieved at https://www.legislation.gov.uk/ukpga/2006/46/part/15/chapter/4
- **Accessed:** 2026-08-06
- **Fetched:** yes (s.395 read in full; text "up to date with all changes known to be in
  force on or before 05 August 2026")
- **Annotation:** The provision that makes the UK basis choice binary. Verified: **s.395(1)**
  — a company's individual accounts may be prepared either "in accordance with section 396
  ('Companies Act individual accounts')" or "in accordance with UK-adopted international
  accounting standards ('IAS individual accounts')"; **s.395(3)** — after the first IAS year
  all subsequent individual accounts must be IAS accounts **unless there is a relevant change
  of circumstance**, defined in s.395(4) as the company becoming a subsidiary of a non-IAS
  parent, ceasing to be a subsidiary, or the company or its parent ceasing to have securities
  admitted to trading on a UK regulated market. Consequence for this library: the choice
  between FRS 102 + FRS 103 [R102][R99] and IFRS 17 [R38][R106] is a **company-law choice at
  the individual-entity level**, is effectively one-way absent a listed trigger, and is
  separate from the group's consolidation basis.

### R104. Companies Act 2006, Part 23 — distributions (ss.830, 833A, 843)
- **Publisher:** legislation.gov.uk
- **URLs:** https://www.legislation.gov.uk/ukpga/2006/46/section/830 ;
  https://www.legislation.gov.uk/ukpga/2006/46/section/833A ;
  https://www.legislation.gov.uk/ukpga/2006/46/section/843
- **Accessed:** 2026-08-06
- **Fetched:** yes (all three sections read in full)
- **Annotation:** **The single most surprising fact in the accounting stream, and the one
  that changes how a UK dividend projection is built.** Verified: s.830(1)–(2) a company may
  distribute only out of accumulated realised profits less accumulated realised losses;
  s.830(3) makes this subject to s.833A for "Solvency 2 insurance companies". **s.833A**
  (inserted 30 December 2016 by SI 2016/1194, amended 1 November 2024 by SI 2024/1083)
  applies to any authorised insurance company carrying on long-term business and **replaces**
  the accounts-based realised profit for s.830(2) purposes with the formula **A − L − D**,
  where A is the total value of assets, L the total value of liabilities and D the total of
  the s.833A(5) deductions, all at the balance-sheet date: (a) excess of the value of shares
  in a qualifying investment subsidiary over consideration given, (b) any asset representing a
  defined benefit pension scheme surplus, **(c) the excess of ring-fenced fund assets over
  ring-fenced fund liabilities** [R71][R80], (d) deferred tax liabilities relating to (a)–(c),
  **(e) where the firm has a matching adjustment permission, the excess of the assigned asset
  portfolio over the value of the MA obligations** [R2][R60], and (f) paid-in ordinary share
  capital and related share premium, paid-in preference shares that are not liabilities and
  related share premium, capital redemption reserve, and any other non-distributable reserve.
  s.833A(3) caps distributable profits at accumulated profits (realised or not) less
  accumulated losses. **s.833A(7) requires assets and liabilities to be valued under Part 2 of
  the IRPR Regulations 2023 [R44], PRA rules on the matching adjustment, other PRA rules
  implementing Solvency II Articles 75–85 and 308b–308e, and Delegated Regulation (EU) 2015/35
  Articles 7–52 and 55–61 [R49]** — note the surviving cross-reference to a revoked
  regulation, recorded as printed. s.833A(8) applies the section as if the company carried on
  only long-term business, with just and reasonable apportionment for composites. **s.843**
  (which applies to authorised long-term insurers **other than** those within s.833A and other
  than insurance SPVs) treats an unallocated long-term-fund surplus shown by an actuarial
  investigation as a realised profit and a deficit as a realised loss, and provides that "any
  profit or loss arising in the company's long-term business is to be left out of account"
  otherwise (s.843(5)). **Modelling consequence: for a Solvency-UK-authorised UK life insurer,
  dividend capacity is driven by the Solvency UK balance sheet, capped by accounts accumulated
  profits — it is not the accounts profit.**

### R105. The Large and Medium-sized Companies and Groups (Accounts and Reports) Regulations 2008 (SI 2008/410), Schedule 3 — insurance companies: form and content of accounts
- **Publisher:** legislation.gov.uk
- **URL:** https://www.legislation.gov.uk/uksi/2008/410/schedule/3
- **Accessed:** 2026-08-06
- **Fetched:** yes (HTML, 300,310 bytes → 116,468 chars; balance sheet format and notes,
  profit and loss account formats, and Part 2 Section E provisions rules read)
- **Annotation:** The statutory format an insurer's Companies Act accounts must take — the UK
  counterpart *in structural role* to the NAIC annual statement blank, though not in content,
  and one the FRC says "cannot be adapted" [R101]. Verified balance-sheet liabilities
  structure: A Capital and reserves; B Subordinated liabilities; **Ba Fund for future
  appropriations** (note 19); C Technical provisions — C.1 unearned premiums, **C.2 Long-term
  business provision** (notes 20, 21, 26), C.3 Claims outstanding, C.4 Provision for bonuses
  and rebates, C.5 Equalisation provision, C.6 Other technical provisions; **D Technical
  provisions for linked liabilities** (note 26); E Provisions for other risks (including
  taxation); assets item **G.II Deferred acquisition costs** (note 17). Verified notes: note
  17 DAC comprises acquisition costs incurred in a financial year but relating to a subsequent
  year, **except** where the long-term business provision already recognises them explicitly
  or implicitly; note 19 the FFA comprises "all funds the allocation of which either to
  policyholders or to shareholders has not been determined by the end of the financial year",
  with transfers shown at P&L item II.12a; note 21 the long-term business provision is "the
  actuarially estimated value of the company's liabilities (excluding technical provisions
  included in liabilities item D), including bonuses already declared and after deducting the
  actuarial value of future premiums", plus IBNR and settlement costs; **note 26** linked
  technical provisions cover liabilities whose benefits are determined by reference to the
  value of, or income from, property or an index, and **any additional provisions for death
  risk, operating expenses or other risks (such as maturity benefits or guaranteed surrender
  values) must go into item C.2**, not item D. Verified special rules: **para 13 — "The costs
  of acquiring insurance policies which are incurred during a financial year but which relate
  to a subsequent financial year must be deferred"** (this is the rule that reverses the U.S.
  framing); para 11(1) every balance sheet of a long-term insurer must show separately the
  aggregate of amounts in capital and reserves that s.843 CA 2006 requires **not** to be
  treated as realised profits [R104]; para 11(2) the total amount of assets representing the
  long-term fund must be shown; **para 52(1)** the long-term business provision must in
  principle be computed **separately for each long-term contract**, with statistical or
  mathematical methods permitted where they give approximately the same result; para 52(2) a
  summary of principal assumptions must be given in the notes; **para 52(3)** the computation
  must be made annually by a Fellow of the Institute or Faculty of Actuaries "with due regard
  to generally accepted actuarial principles and on the basis of recognised actuarial methods"
  — the quoted words were **inserted, and a following phrase omitted, by SI 2019/145 (as
  amended by SI 2020/523)** with effect for financial years beginning on or after IP
  completion day, which is the amendment that makes [R113]'s premise stale. Verified long-term
  business technical account format (Part 1, format II): 1 Earned premiums net of reinsurance;
  2 Investment income; 3 Unrealised gains on investments; 4 Other technical income; 5 Claims
  incurred net of reinsurance; 6 Change in other technical provisions — **6(a) Long-term
  business provision net of reinsurance**, 6(b) other; 7 Bonuses and rebates; 8 Net operating
  expenses — 8(a) acquisition costs, **8(b) change in deferred acquisition costs**, 8(c)
  administrative expenses, 8(d) reinsurance commissions and profit participation; 9 Investment
  expenses and charges; 10 Unrealised losses on investments; 11 Other technical charges;
  **11a Tax attributable to the long-term business**; 12 Allocated investment return
  transferred to the non-technical account; **12a Transfers to or from the fund for future
  appropriations**; 13 Sub-total. The non-technical account picks that balance up at item
  III.2, with **III.2a Tax credit attributable to balance on the long-term business technical
  account**.

### R106. UK Endorsement Board — Endorsement Criteria Assessment: IFRS 17 Insurance Contracts
- **Publisher:** UK Endorsement Board
- **URL:** https://www.endorsement-board.uk/documents/666/ECA_-_IFRS_17.pdf (linked from the
  UKEB IFRS 17 project page at [R38])
- **Accessed:** 2026-08-06
- **Fetched:** yes (PDF, 1,840,287 bytes → 478,447 chars; **Section 2 "Description of IFRS 17"
  read in full, Section 3 priority issue D read, remainder indexed by search; one page failed
  text extraction**)
- **Annotation:** **The substitute for the paywalled standard [R107].** Section 2 is a
  systematic description of IFRS 17 written by the UK adopting body, quoting IFRS 17 paragraph
  numbers. Verified: **level of aggregation** — portfolios "subject to similar risks and
  managed together" [IFRS 17:14], divided into a minimum of three sub-groups (onerous at
  initial recognition; no significant possibility of becoming onerous; remainder), with
  contracts issued more than one year apart barred from the same group (the **annual cohorts**
  requirement), groups fixed at initial recognition and never reassessed (¶¶2.14–2.17);
  measurement as fulfilment cash flows plus contractual service margin (¶2.19); **GMM** initial
  recognition (¶2.43); contract boundary [IFRS 17:34] (¶2.45); discount rate principles
  [IFRS 17:36] quoted verbatim (¶2.46); risk adjustment definition [IFRS 17 Appendix A] quoted
  verbatim (¶2.48); CSM as a residual measured so there is no income or expense on initial
  recognition, and **zero with an immediate loss for onerous groups** (¶2.50); subsequent
  measurement as liability for remaining coverage plus liability for incurred claims (¶2.51);
  CSM released by **coverage units** reflecting the quantity of benefits and expected coverage
  period (¶2.54); acquisition cash flows included in the fulfilment cash flows, recognised as
  an asset before the group is recognised then subsumed into the CSM (¶¶2.56–2.59); **VFA** —
  contracts with direct participation features, "substantially investment-related service
  contracts under which an entity promises an investment return based on underlying items"
  [IFRS 17:B101], eligibility assessed at inception and never reassessed absent modification,
  reinsurance issued and held cannot qualify, and **changes from time value of money and
  financial risk go to the CSM under VFA but straight to insurance finance income or expense
  under GMM**, with VFA CSM adjustments at **current** rates versus GMM's **locked-in** rates,
  plus an optional risk-mitigation election (¶¶2.60–2.71); **PAA** (¶¶2.72–2.77); presentation
  with a **per-portfolio** policy choice to disaggregate insurance finance income/expense
  between P&L and OCI (¶¶2.26–2.29); transition — retrospective unless impracticable, then a
  free choice between the **modified retrospective approach** and the **fair value approach**
  (CSM = fair value of the group minus fulfilment cash flows at transition), chosen at group
  level (¶¶2.33–2.36); reinsurance held accounted for separately with a loss-recovery component
  (¶¶2.37–2.41). **The UKEB's own expectations for the UK market are stated in boxed text:**
  GMM for "life insurance (protection business), annuity contracts and longer-term general
  insurance"; **VFA for "unit-linked contracts and with-profits contracts"**; PAA for
  "short-term general insurance and short-term life contracts". Section 3 **priority issue D
  (with-profits: inherited estates)** verified: UK inherited estates are not addressed
  explicitly by IFRS 17; the fund's PPFM (and possibly the articles) governs attribution,
  "typically requiring 90% to be attributed to policyholders", with the same 90/10 split
  typically applying to the distributable estate; an emerging consensus requires a liability
  for the policyholders' share; the shareholders' share is the contested item; most UK
  with-profits funds are closed to new business; a fair value approach on transition is
  expected for a large part of UK with-profits business, and entities are expected to recognise
  an increase in equity on transition. **Section 3 priority issue A (CSM allocation for
  annuities) was read in outline only**: R106 records an IFRS Interpretations Committee
  Tentative Agenda Decision and continuing divergence on whether investment-return service is a
  separate service and on the weighting of coverage units — **the right coverage-unit basis for
  an annuity is not settled by the retrieved material.**

### R107. IFRS Foundation — IFRS 17 Insurance Contracts standard page (paywall record)
- **Publisher:** IFRS Foundation
- **URL:** https://www.ifrs.org/issued-standards/list-of-standards/ifrs-17-insurance-contracts/
- **Accessed:** 2026-08-06
- **Fetched:** **partial.** Direct HTML extraction returned only 41 characters ("Amendments to
  IFRS 17 Insurance Contracts") — the page is client-rendered; a second retrieval through a
  markdown-converting fetcher succeeded and is the basis of the annotation.
- **Annotation:** **Recorded so that the library is explicit rather than silently
  paraphrasing.** Verified: the page **does not provide the full text of IFRS 17 free of
  charge**; the standard text is available through the IFRS Digital subscription or the IFRS
  Foundation shop. Free material offered: an overview of key principles, standard history from
  IFRS 4 (2004) through IFRS 17 (2017) and the 2020 and 2024 amendments, links to related
  projects, and pointers to implementation support. **No IFRS 17 paragraph text was read from
  this source.** All IFRS 17 mechanics in this library come from [R106]; the adoption facts
  from [R38].

---

## 13. Tax — the instruments that sit on top of FA 2012 (R108–R110, R113)

Entries from `uk/_research/uk-accounting-and-tax.md`, section D. Read with the frozen tax
entries [R15]–[R18] and the correction note appended to [R18]. All accessed **2026-08-06**.

### R108. The Insurance Contracts (Tax) (Change in Accounting Standards) Regulations 2022 (SI 2022/1165)
- **Publisher:** legislation.gov.uk (HM Treasury statutory instrument)
- **URL:** https://www.legislation.gov.uk/uksi/2022/1165/made
- **Accessed:** 2026-08-06
- **Fetched:** yes (regulations 1–8 read in full; regulations 9–12 read in part)
- **Annotation:** The IFRS 17 tax transitional regime. Verified: made under FA 2022; **in
  force 1 January 2023**, with effect for accounting periods beginning on or after that date
  (reg 1). **Reg 3** — on adopting IFRS 17 an insurance company carrying on long-term business
  computes **A − B**, where A is the accumulated profits less accumulated losses shown as a
  closing balance in the **first IFRS 17 balance sheet** (the pre-IFRS 17 balance sheet as
  restated in the first IFRS 17 accounts) and B the same quantity in the **pre-IFRS 17 balance
  sheet**, each subject to adjustments required or authorised by law in computing trade profits
  (reg 3(2)); amounts relating to IFRS 9 adoption, or not solely relating to IFRS 17, are
  excluded (reg 3(3)); the result is apportioned between long-term business and other business
  on the basis shown in the company's IFRS 17 disclosures, failing which on a just and
  reasonable basis (regs 3(4)–(5)); the amount allocated to long-term business is the
  **"transitional amount"** (reg 3(6)). **Reg 4** — where the company has both BLAGAB and
  non-BLAGAB long-term business, the transitional amount is allocated by an **acceptable
  commercial method** fairly representing each business's contribution to accounting profit or
  loss in the period ending immediately before the first IFRS 17 period, consistent with the
  FA 2012 s.98 and s.115 methods for that period [R17]. **Reg 5** — a positive transitional
  amount is a **receipt**, a negative one an **expense**, of the long-term business, taken into
  account in computing BLAGAB trade profit or loss and non-BLAGAB long-term business profits.
  **Reg 6 — the receipt or expense is treated as arising over 10 years** beginning with the
  first day of the first IFRS 17 accounting period, apportioned to accounting periods in
  proportion to days. **Regs 7–8** — on an insurance business transfer scheme the unspread
  balance passes to a transferee within the charge to corporation tax (and not a mutual), with
  part-transfers split by an amount that "fairly represents" the attributable balance;
  otherwise the remaining balance crystallises in the transferor in the period of transfer.
  Regulation 12 introduces a CTA09 s.320A-analogue bringing OCI amounts into account when an
  insurance contract is derecognised — **read through [R18] LAM16060, not from the SI text.**

### R109. The Finance Act 2022, Part 2 of Schedule 5 (Insurance Contracts: Change in Accounting Standards) (Commencement and Savings Provision) Regulations 2022 (SI 2022/1164 (C. 90))
- **Publisher:** legislation.gov.uk (HM Treasury statutory instrument)
- **URL:** https://www.legislation.gov.uk/uksi/2022/1164/made
- **Accessed:** 2026-08-06
- **Fetched:** yes (read in full — the instrument is two regulations plus an explanatory note)
- **Annotation:** **The instrument that killed the seven-year tax spreading of acquisition
  expenses.** Verified: made **9 November 2022** by two Lords Commissioners of HM Treasury
  under FA 2022 Sch 5 paras 4 and 5. **Reg 2(1)** — Part 2 of Schedule 5 to the Finance Act
  2022 **comes into force on 1 January 2023 and has effect for accounting periods of companies
  beginning on or after that date.** **Reg 2(2)** — paragraphs 2 and 3 of that Part **do not
  apply** to amounts of acquisition expenses adjusted under FA 2012 s.79 that are referable to
  an accounting period beginning before 1 January 2023 — the savings provision that keeps
  legacy 1/7ths running. Explanatory note: FA 2022 Sch 5 Part 2 amends CTA 2009 and FA 2012 "in
  connection with the adoption by insurance companies of International Accounting Standard 17".
  See the correction note appended to [R18].

### R110. GOV.UK published tax rates — Corporation Tax and Income Tax
- **Publisher:** HM Government / HMRC (GOV.UK)
- **URLs:** https://www.gov.uk/corporation-tax-rates ; https://www.gov.uk/income-tax-rates
- **Accessed:** 2026-08-06
- **Fetched:** yes (both)
- **Annotation:** The two rates a UK life tax projection needs, taken from a citable source
  rather than memory, because the LAM's worked examples are stated at 2018 rates [R18
  LAM01160]. Verified **at the access date**: **Corporation Tax main rate 25%**, applying where
  profits exceed £250,000; **small profits rate 19%** where profits are £50,000 or less;
  Marginal Relief between £50,000 and £250,000; both thresholds proportionately reduced for
  short accounting periods and by the number of associated companies; a single rate applied
  from 1 April 2015 to 31 March 2023; separate ring-fence rates exist for oil and gas. **Income
  Tax basic rate 20%** on taxable income from £12,571 to £50,270 (personal allowance up to
  £12,570; higher rate 40% to £125,140; additional rate 45% above). The basic rate matters
  because FA 2012 s.102(3) sets the policyholders' rate by reference to the basic rate applying
  in England, Wales and Northern Ireland — expressly **not** the Scottish basic rate [R18
  LAM06010]. **Retrieval limit:** the gov.uk income-tax page does not state the tax year in the
  extracted text — **treat "20%" as the rate published at the access date, not as a rate
  verified for a named tax year.**

### R113. Letter from the Department for Business, Energy and Industrial Strategy to the FRC — Solvency II clarification (3 February 2017)
- **Publisher:** BEIS (published by the FRC)
- **URL:** https://www.frc.org.uk/documents/5738/BEIS_letter_to_FRC_Solvency_II_clarification_February_2017.pdf
- **Accessed:** 2026-08-06
- **Fetched:** yes (PDF, 100,371 bytes → 2,407 chars; one page, read in full)
- **Annotation:** A short but decisive document on whether Solvency II drives the accounts,
  **and the one place in the accounting stream where two retrieved sources are in tension**.
  Verified: Debbie Gillatt (Director, Business Frameworks, BEIS) wrote to Stephen Haddrill
  (CEO, FRC) on 3 February 2017 in response to an FRC query. The letter records that SI
  2008/410 Schedule 3 Part 2 Section E paragraph 52 **then** required the long-term business
  provision computation to be made annually by a Fellow of the IFoA on the basis of recognised
  actuarial methods and with "due regard to the actuarial principles laid down in Directive
  2009/138/EC … (Solvency II)", a reference inserted when the Regulations were updated in 2015.
  BEIS states that this reference "should not be interpreted to mean that insurance companies
  are now required to change their accounting basis to one consistent with Solvency II"; "due
  regard" only requires preparers to consider the Solvency II actuarial requirements **if that
  Directive is relevant to the accounting basis applied**; and "Insurance providers that do not
  report under IFRS should continue to use the relevant UK accounting standard." **Tension
  recorded, not resolved:** the Schedule 3 text retrieved on 2026-08-06 [R105] **no longer
  contains the Solvency II reference** — para 52(3) now reads "with due regard to generally
  accepted actuarial principles and on the basis of recognised actuarial methods", the inserted
  words and an omission both attributed to SI 2019/145 (as amended by SI 2020/523) with effect
  for financial years beginning on or after IP completion day. **The letter therefore
  interprets a version of the law that has since been amended: its conclusion is independently
  confirmed by FRS 103 BC45 [R99]; its premise is stale.** Both records are kept.

---

## 14. Product-level regulatory treatment — assets, unit matching, and the with-profits heritage (R114–R120)

Entries from `uk/_research/uk-product-regulatory-applicability.md`; **R121–R133 are unused
by design.** That file also carries the consolidated seven-product applicability matrix from
which Matrix B's product-level rows are drawn. All accessed **2026-08-06**.

### R114. PRA Rulebook — Investments Part (as at 05/08/2026)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.prarulebook.co.uk/pra-rules/investments
- **Accessed:** 2026-08-06
- **Fetched:** yes (browser User-Agent; 9,717 chars. **Chapters 1–5 read in full; Chapter 6
  (repackaged loans) skimmed.** Chapter 1 definitions carry a **future version after
  01/01/2027 that was not retrieved.**)
- **Annotation:** The Part that decides **what assets a unit-linked liability must be backed
  by**, and therefore the whole unit-matching question. Verified rule text: **3.1**
  [01/01/2016] assets held to cover technical provisions must be "invested in a manner
  appropriate to the **nature and duration** of the firm's insurance and reinsurance
  liabilities and in the best interests of all policyholders, taking into account any
  disclosed policy objectives". **4.1** the chapter does not apply to a pure reinsurer;
  **4.2** it applies additionally where a firm carries out **linked long-term contracts of
  insurance**; **4.3** the firm "must cover its technical provisions **in respect of its
  linked long-term liabilities as closely as possible** with (1) where the linked benefits
  are linked to the value of **units**, **those units**; (2) where linked to the value of
  assets in an **internal fund** — (a) the assets represented by the notional units, or (b)
  where notional units are not established, those assets; and (3) where linked to a **share
  index or other reference value**, assets of appropriate security and marketability
  corresponding as closely as possible to the assets on which the reference value is based".
  **5.1** Chapter 5 does **not** apply to assets covering technical provisions for linked
  long-term contracts **unless and to the extent that** the assets are held to cover the
  technical provisions in respect of **any guarantee of investment performance or other
  guaranteed benefit** provided under those contracts. **5.2** the non-linked requirements:
  derivatives and quasi-derivatives only where they reduce risk or facilitate efficient
  portfolio management; non-regulated-market assets kept to prudent levels; proper
  diversification; no excessive single-issuer concentration.

### R115. FCA Handbook — INSPRU 1.2, Mathematical reserves
- **Publisher:** Financial Conduct Authority
- **URL:** https://www.handbook.fca.org.uk/handbook/INSPRU/1/2.html
- **Accessed:** 2026-08-06
- **Fetched:** yes (two passes; the application rule and rules 1.2.62 / 1.2.62A quoted back
  verbatim). **The full chapter was not read.**
- **Annotation:** The **Solvency I** valuation rules for long-term insurers — still live in
  the FCA Handbook but **expressly disapplied to Solvency II firms**. Verified application
  rule (date-stamped 01/01/2021): "INSPRU 1.2 applies to a long-term insurer unless it is:
  (1) a non-directive friendly society; or (2) [deleted]; (3) [deleted]; **(4) a Solvency II
  firm**." Verified **INSPRU 1.2.62 R** [31/12/2006]: a firm must include in its mathematical
  reserves an amount to cover any increase in liabilities that might be the direct result of
  a policyholder exercising an option, and "**Where the surrender value of a contract is
  guaranteed, the amount of the mathematical reserves for that contract at any time must be
  at least as great as the value guaranteed at that time.**" Verified **INSPRU 1.2.62A G**
  [31/12/2006]: a contract has a guaranteed surrender value where the policy wording states
  one is payable and either provides a minimum amount or a method of calculating one; "For
  example, where a **unit-linked contract** provides for a surrender value equal to the value
  of the units allocated to the contract, the firm must establish mathematical reserves for
  that contract **greater than or equal to the value of the units allocated at the valuation
  date**." Other rule numbers visible on the page: 1.2.6 / 1.2.6A, 1.2.10, 1.2.20–1.2.21,
  1.2.28–1.2.31, 1.2.59–1.2.72, 1.2.86. **Why it is here:** this floor is the *contrast* that
  shows Solvency UK carries no unit-reserve floor and permits a negative best estimate
  [R1][R41].

### R116. FCA Handbook — INSPRU 1.3, With-profits insurance capital component (Deleted)
- **Publisher:** Financial Conduct Authority
- **URL:** https://www.handbook.fca.org.uk/handbook/INSPRU/1/3.html
- **Accessed:** 2026-08-06
- **Fetched:** yes — **but the page carries no rule text.** It renders as "Deleted", with the
  note that "INSPRU 1.3 With-profits insurance capital component was last updated on
  **31/12/2015**".
- **Annotation:** The provenance entry for the entire **realistic balance sheet /
  with-profits benefits reserve (WPBR) / future policy related liabilities (FPRL)**
  vocabulary that IR.12.06 [R90] and FRS 103 [R99] both still use. Verified: the chapter is
  deleted and its last update was 31/12/2015 — it fell away with Solvency II implementation.
  **No rule text of INSPRU 1.3.40 (realistic value of liabilities), 1.3.190 (realistic
  current liabilities), or any WPBR / FPRL definition was retrieved, and none is asserted
  anywhere in this library.** The chapter nevertheless remains operative in one live place:
  FRS 103's glossary defines *realistic value of liabilities* by reference to "rule 1.3.40 of
  INSPRU **as at 31 December 2015**", excluding current liabilities within rule 1.3.190 as at
  the same date, and the FRC recorded that it kept the INSPRU-anchored definitions
  deliberately because preparers "would need to refer to INSPRU as at 31 December 2015 in
  order to continue with their existing accounting policies" [R99 BC49–BC50].

### R117. SS1/14 — Mutuality and with-profits funds: a way forward (November 2024, updating November 2015)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.prarulebook.co.uk/guidance/supervisory-statements/ss01-14-mutuality-and-with-profits-funds-a-way-forward
  (listed as a "Related link — Guidance" on the With-Profits Part page [R80]).
  **Retrieval caveat: the exact URL used by the fetch pass was not preserved in the research
  file — treat the URL above as the Rulebook guidance path and re-verify it before citing
  this entry in a published document.**
- **Accessed:** 2026-08-06
- **Fetched:** yes (20,563 chars; Introduction, Background and "Change in regulatory
  landscape" read in full; the waiver-process and "Interaction with Solvency II" sections
  skimmed)
- **Annotation:** Verified contents: Introduction; Background; Change in regulatory landscape
  since CP12/38 was issued; Scope of supervisory statement; The PRA and the mutual
  with-profits waiver process; Interaction with Solvency II. Verified substance: the
  statement "is relevant for all mutual insurance firms and friendly societies writing new
  with-profits business or with existing books of with-profits business" (¶1.1); it responds
  to FSA **CP12/38** (December 2012), which proposed that COBS 20 explicitly recognise a
  **mutual members' fund** identified within a common with-profits fund, to which COBS 20
  would not apply directly, achieved by a waiver under **FSMA s.148** (¶2.2); the underlying
  concern was that COBS **20.2.55R and 20.2.56R** were prescriptive enough that mutuals
  writing with-profits out of a common fund risked having to close to new business and go
  into run-off (¶2.1); after the 1 April 2013 split, most of COBS 20 — including
  20.2.55R/56R — sits **solely in the FCA Handbook**, while "a limited number (including the
  **definition of a 'with-profits fund'**) also appear in the PRA Rulebook since they embody
  prudential matters relevant to the PRA's objectives" (¶3.2). ¶3.2 is the general authority
  for *why* some with-profits definitions live in the PRA Rulebook and the rest in COBS 20
  [R9]. SS14/15 ¶2.2 cites SS1/14 as the origin of the PRA's position that each with-profits
  fund generally displays RFF characteristics [R71].

### R118. Milliman research report — The benefits of Solvency II unit matching (July 2018)
- **Publisher:** Milliman (Emma Hutchinson FIA FSAI, Fred Vosvenieks FIA CERA, Magnus Wilson
  FIA; with Paul Turnbull FIA, P Turnbull Financial Management)
- **URL:** **not recorded, and deliberately not asserted.** The retrieving fetch did not
  preserve a URL and **this library does not fabricate URLs.** Re-derive and verify the URL
  before citing this entry in a published document.
- **Accessed:** 2026-08-06
- **Fetched:** yes (74,472 chars; executive summary and sections 1–2 read in full; sections
  3–4 skimmed)
- **Annotation:** **Secondary — a consultancy research report, not a rule or regulator
  publication.** Cited **only** as evidence of how the UK market reads Investments 4.3 [R114],
  and for the vocabulary of the unit / non-unit split — **never as authority for a rule.**
  Verified content: under Solvency I "the Mathematical Reserves for unit-linked business had
  to be at least equal to the surrender value of the in-force contracts at the valuation
  date" and the unit-linked element of those reserves had to be covered by unit-linked assets
  (its citations: INSPRU 1.2.62A and INSPRU 1.5.35); under Solvency II "the unit-linked
  Technical Provisions would normally be **less than the surrender value** of policies at the
  valuation date as credit can be taken for the expected value of future charges and **there
  is no floor related to the surrender value specified in the rules**". Its working
  assumption, "which has also been made by firms in practice", is that Investments 4.3
  applies to technical provisions **held in respect of linked benefits**, not to all
  liabilities arising from linked contracts — supported by the Rulebook definition of *linked
  long-term liabilities* [R43]. Its decomposition: the unit-linked component of the BEL
  equals the current surrender value (or unit-linked benefit) **less** the present value of
  expected future annual management charges on **existing** unit funds, computed on the full
  decrement basis; only that component must be covered with unit-linked assets, while
  non-linked liabilities such as administration expenses "can be backed with alternative and
  perhaps more suitable investments"; the risk margin ideally splits the same way but "in
  practice it may be difficult", and treating all of it as unit-linked "will not lead to a
  material misstatement as **lapse risk is typically the main component of the Risk Margin
  for unit-linked business**". **Conflict recorded, not resolved:** Milliman attributes the
  Solvency I surrender-value floor to **INSPRU 1.2.62A**, which the FCA Handbook renders as
  **guidance (G)** giving a unit-linked worked example; the operative **rule** is **INSPRU
  1.2.62 R** [R115]. The substantive point survives; the citation is one rule number out.

### R119. SS1/20 — Solvency II: Prudent Person Principle (November 2024, updating June 2024)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URLs:** PDF
  https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/supervisory-statement/2024/ss120-november-2024-update.pdf
  ; landing page
  https://www.bankofengland.co.uk/prudential-regulation/publication/2020/solvency-ii-prudent-person-principle-ss
- **Accessed:** 2026-08-06
- **Fetched:** yes (47,081 chars; **contents page and chapter 1 read in full; chapters 2–8
  keyword-searched only**)
- **Annotation:** Published **15 November 2024, effective 31 December 2024**. Contents
  verified: 1 Introduction; 2 Investment strategy; 3 Investment risk management; 4
  Outsourcing of investment activities; 5 Exposures to non-traded assets; 6 Valuation
  uncertainty; 7 Intragroup loans and participations; 8 Outwards reinsurance; Annex –
  SS1/20 updates. Verified ¶1.6: the PRA rules require that "as regards investment risk, a
  firm must demonstrate that it complies with the Investments Part of the PRA Rulebook"
  (footnote: **Conditions Governing Business 3.4** [R92]). Verified ¶1.7: a breach of the PPP
  may be associated with a failure to meet Conditions Governing Business or **Matching
  Adjustment** Part requirements — "the MA eligibility conditions (which firms should comply
  with at all times) require compliance with the **PPP at the level of both the asset and
  portfolio**" (footnote: Matching Adjustment 2.2(6) and 13.2); and where an MA eligibility
  breach "is not rectified for more than two months" the PRA may consider necessary changes
  to the MA permission, "which may be in addition to the reduction to the MA required by
  **Matching Adjustment 13.5**" [R2][R60]. Verified ¶1.8 and footnote 28: the rules apply at
  different granularities — Investments **5.2(1)** requires consideration of **each**
  derivative and quasi-derivative, while Investments **2.1(2)** expressly requires
  consideration of security, quality, liquidity and profitability at **whole-portfolio**
  level [R114]. **Negative finding, recorded deliberately:** a keyword search of the
  retrieved text returns **no** occurrence of "unit-linked", "unit linked", "with-profits" or
  "ring-fenced" — **SS1/20 contains no unit-linked-specific or with-profits-specific
  guidance.**

### R120. SS20/16 — Solvency II: reinsurance – counterparty credit risk
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.bankofengland.co.uk/prudential-regulation/publication/2016/solvency2-reinsurance-counterparty-credit-risk-ss
- **Accessed:** 2026-08-06
- **Fetched:** **partial — landing page only (2,306 chars); the PDF was NOT retrieved.**
- **Annotation:** Recorded because UK protection business (TA, CI, IP) is the most heavily
  reinsured business in this library and therefore carries the largest counterparty-default
  exposure [R41 TPFR 24][R62 `3E13`], and because two already-numbered documents point at it:
  SS18/16 ¶2.1 [R48] and SS1/20 footnote 22 [R119]. Verified from the landing page: addressed
  to all UK Solvency II firms and to Lloyd's; sets out PRA expectations "with respect to
  general issues regarding reinsurance and the management of reinsurance counterparty credit
  risk"; first published **25 November 2016**; **current version published 15 November 2024,
  effective 31 December 2024**, following PS15/24 [R6]; past versions 23 May 2024 (following
  PS8/24) and 25 November 2016 (following PS33/16). **Everything else about SS20/16 is
  [unverified] — no paragraph text was retrieved.** Note the title discrepancy between the
  landing page ("counterparty **credit** risk") and SS18/16 ¶2.1 ("counterparty **default**
  risk"), recorded not resolved.

---

## 15. R39–R120 — gaps, fetch failures and unverified points

Every limitation below is also stated at the point of use in the entry it belongs to. This
section exists so that the limitations can be read as a set. **No URL on this page is
fabricated: every URL listed for R39–R120 was actually requested and its HTTP status
observed, except R118, for which no URL is asserted at all because the retrieving fetch did
not preserve one.**

### Fetch behaviour observed on 2026-08-06

- **`prarulebook.co.uk` returns HTTP 403 to plain fetchers.** Every PRA Rulebook Part was
  read with a browser User-Agent. Rulebook URLs carry an "as at" date segment which is the
  version identifier; a Part read at a different date is a different document.
- **`bankofengland.co.uk` 403s plain fetch on publication pages**, and several PDF links on
  those pages are **script-rendered**, which is why R97's current PDF could not be reached
  (two guessed media URLs returned HTTP 404).
- **`ifrs.org` is client-rendered**; direct HTML extraction of the IFRS 17 page returned 41
  characters, and a markdown-converting fetcher was used instead [R107].
- **`legislation.gov.uk` renders the IRPR reg 7B risk-margin formula as an image**, which
  came back empty from text extraction [R44].
- Failures recorded and **not** papered over: the SS7/18-footnote URL for PS17/25 returns
  **HTTP 404** and the recovered URL's body extraction failed [R60b]; the
  `/pra-rules/glossary` path is a **404** (the glossary lives at `/glossary`) [R43]; the
  `---` slug variant of the TPFR Part is a **404** [R41]; the SoP2/24 path without the
  trailing `-sop` is a **404** [R58]; FRS 103 Implementation Guidance page 1 failed `pypdf`
  extraction [R100]; one page of the UKEB assessment failed extraction [R106]; the DLT
  assessment's tabular maturity grid extracted unreliably [R56].

### Documents not retrieved at all

**The Annexes to the SCR – Standard Formula Part [R73]** — the single largest hole. It takes
with it Annex XVI (the mass-accident country list and ratios `r_s`, the event types and
benefit ratios `x_e`, the pandemic healthcare-utilisation ratios `H_h`) and the
geographical-diversification annex behind `3A5`/`3C3.8`. Consequence: the **health
catastrophe sub-module cannot be computed** from this library. **Recorded, not resolved:**
the SCR stream also listed the numbered line-of-business list here, but TPFR Annex 1
Parts A–E (lines 1–36) was read in full [R41] and the applicability stream infers, from
consistent cross-references in [R42], that the SCR Parts key on the same numbering — a
drafter's inference, stated in no retrieved document.

Also not retrieved, each recorded in its own entry: the **PS17/25 body** [R60b]; the
**SoP11/24 PDF** [R70]; the **SoP6/24 PDF** [R88b]; the **SS20/16 PDF** [R120]; the
**current November 2024 SS17/16 PDF** [R97]; **SoP12/24** on the permissible SCR recovery
period [R82]; **SoP1/19** on the interpretation of EU guidelines after withdrawal [R80c];
**SS22/15** [R80]; **SI 2024/1083** [R44]; **PS18/26 Appendix 3** rule text [R87]; the
**PS18/26 replacement MA instruction files** MA.00.01–MA.03.01 [R91]; the **XLSX template
files** behind every LOG file [R88]–[R91]; the **PRA monthly technical-information XLSX
files and the SAECC spreadsheet** [R54]; **IFRS 17 itself**, which is paywalled [R107]; and
the **FRS 102 "Adapted formats" amendment** [R102b].

### Documents retrieved but read only in part

[R47] SS5/24 (technical-provisions interface only) · [R48] SS18/16 (grep-level) · [R49] the
revoked Delegated Regulation (contents, Article 1 and Article 142 only — **the remaining
article bodies were never read**) · [R57] Transitional Measures (Chapters 10 and 12 only) ·
[R62] SCR – Standard Formula (chapters 1D, 3A, 3D18–3D24 and 3G surveyed only) · [R65] USPs
(chapters 4–6 and 8–10 surveyed) · [R69] SoP4/24 (body surveyed) · [R72] PS12/25 (mapping
tables not transcribed) · [R83b] SoP10/24 (Chapters 3–6 scope only — **their substance is
[unverified]**) · [R91] MALIR (4–7 headers and appendix only) · [R95] SS19/16 (**no
paragraph-by-paragraph diff between the November 2024 and May 2026 versions was performed —
[unverified] beyond the scope sentence**) · [R99] FRS 103 (¶¶2.16 tail and 2.17–2.18 partly;
**Appendix II not read**) · [R100] FRS 103 IG (Section 3 not read) · [R102] FRS 102
(Sections 1, 7.10E and 29 only) · [R106] the UKEB assessment (Section 3 priority issue A in
outline only) · [R114] Investments (Chapter 6 skimmed) · [R115] INSPRU 1.2 (three rules
quoted; chapter not read) · [R119] SS1/20 (chapters 2–8 keyword-searched only).

Consequences worth naming: **Transitional Measures 4.1 grandfathering of pre-2016 own-funds
instruments into Tier 1 is [unverified]** [R57][R77]; the counterparty-default
probability-of-default table `3E12`, the loss-given-default definitions `3E4`–`3E11`, the
concentration aggregation formulas `3D27`/`3D28` and the ECAI-to-CQS mapping tables are
**not transcribed anywhere** [R62][R72]; and **SoP4/24's quantitative thresholds for a
"significant risk profile deviation" must not be stated** [R69].

### Version and retrieval-provenance gaps

- **[R43]** the exact per-letter Glossary query URLs were not preserved, and **letter S was
  not retrievable**, so the Glossary definition of "surplus funds" is missing [R45].
- **[R117]** the exact retrieval URL was not recorded.
- **[R118]** no URL is asserted at all.
- **[R61]** the pre-31/12/2024 version of SCR – General Provisions 3.1 was not retrieved.
- **[R62]** rule 1.2 carries a future version after **01/01/2027** that was not retrieved.
- **[R77]** the Own Funds Part's future view after **31/12/2026** was not retrieved, though
  live future markers sit on 3A.1, 3B.1, 3C.1, 3D.1, 3E.1, 3F.1 and 3G.1.
- **[R114]** the Investments Part Chapter 1 definitions carry a future version after
  **01/01/2027** that was not retrieved.
- **[R56]** the USD and CAD last liquid points were not retrieved.
- **[R97]** the text read is stamped "31 December 2024: This document has been superseded" —
  **paragraph numbers must be re-verified against the November 2024 PDF before citation.**

### Conflicts between retrieved sources — recorded, not resolved

1. **SS5/24 ¶1.7 cites dead rules.** It directs firms to "Chapters 6, 7 and 11 of the
   Technical Provisions" [R47]; TP Chapters 6 and 7 are **[Deleted] as at 30/06/2024** [R1],
   the MA material having moved to the Matching Adjustment Part [R2] under PS10/24 [R5].
   Only the Chapter 11 reference is live.
2. **"Market value" has two anchors.** The Glossary defines *market value* as "the market
   value as determined in accordance with **generally accepted accounting practice**" [R43],
   while Valuation 2.1 states the Article-75 exchange/transfer standard [R39].
3. **The mass-lapse correction names two different populations.** The PRA statement's
   narrative names RAO classes **II and VII**; the corrected rule text as read names **class
   VII only** [R64][R62].
4. **PS3/24 says templates survive that the final Rulebook does not contain.** ¶¶4.68–4.70
   state that S.13.01 and SR.22.02 "continue to be collected" [R86]; the Reporting Part
   inventory contains **no IR.13.01** [R84].
5. **SS40/15's published PDF carries an unresolved placeholder header** — "published as part
   of **PSX/24** … /publication/2024/**XXXXX**" — while its annex records the November 2024
   update as following PS15/24 [R85].
6. **SS11/24's cover page and page-2 masthead disagree** (SS11/24 vs SS20/24); the Bank's
   publication page confirms SS11/24 is the supervisory statement and PS20/24 the policy
   statement [R98].
7. **The Own Funds Part states eligibility limits twice**, in Chapter 4 and Chapter 4A; SS2/15
   ¶1.3(d) is the PRA's own reconciliation [R77][R83].
8. **s.833A(7) still cross-refers to a revoked regulation** — Delegated Regulation (EU)
   2015/35 Articles 7–52 and 55–61 [R104][R49]. Recorded as printed.
9. **The IRPR amendment note prints "31.12.20204"** where 31.12.2024 is plainly intended
   [R44]. Recorded as printed rather than silently corrected.
10. **FRS 103 ¶3.7 versus ¶3.1(b).** Whether the ¶3.10 DAC prohibition reaches a with-profits
    fund that was never in the pre-2016 PRA realistic capital regime is **not settled**
    [R99][R100]. **Do not assert either reading.**
11. **The BEIS letter's premise is stale** relative to the current Schedule 3 text
    [R113][R105]; its conclusion is independently corroborated by FRS 103 BC45 [R99].
12. **HMRC's rate-incentive statement in LAM01160 is out of date** at the access date
    [R18][R110] — see the correction note appended to [R18].
13. **Milliman cites INSPRU 1.2.62A** (guidance) where the operative rule is **1.2.62 R**
    [R118][R115]. The substantive point survives; the citation is one rule number out.

### Verified but time-sensitive

- **SCR – Standard Formula 6.5**, the transitional permission to utilise an increase in
  deferred tax assets in the LACDT calculation, is stated in the 05/08/2026 view as running
  "for a transitional period **ending 30 December 2025**". On its face that period has
  expired at the access date, yet the rule remains printed in the current view, and **no PRA
  instrument confirming its expiry or extension was retrieved** [R62]. Treat it as expired
  for a current-date calculation, but flag it.
- **CP4/26 Proposals 2, 3 and 4 have no recorded outcome.** Only Proposal 1 was finalised by
  PS18/26; the retrieved PS18/26 text does not state what happened to the others
  [R83c][R87].
- **FRS 102 and FRS 103 Periodic Review 2024** amendments are effective for periods beginning
  on or after **1 January 2026** (except the FRS 103 Section 6 Transition amendment, 1 January
  2024), and the FRS 102 "Adapted formats" amendment is effective **1 January 2027**
  [R101][R102b]. A document describing "current UK GAAP" must say which edition it means.
- **The UKEB post-implementation review of IFRS 17** is committed to report by 1 January 2028
  [R38]; nothing retrieved indicates it has reported.
- **PS15/25's liquidity templates take effect 30 September 2026**, and **PS18/26's reporting
  and own-funds changes take effect for reference dates on or after 31 December 2026**
  [R87] — both after the access date.

### Unverified points carried forward — these must not be upgraded downstream

- **Whether standalone and accelerated critical illness are life or health obligations** under
  `SCR-SF 3.2A`/`3.10B`, and which numbered line of business each falls in. **Standalone
  CI** is derivable from retrieved material — the Glossary definitions in [R42], TPFR 26.3
  and Annex 1 [R41], and `SCR-SF 3.2A`/`3.10B` [R62] — but **no retrieved document states
  the conclusion**, which is why it stays [unverified]; the derivation is set out at
  `uk/_research/uk-product-regulatory-applicability.md` §12.4. **Accelerated CI** is not
  settled even by derivation: TPFR 26.7 requires unbundling "where possible" and the
  retrieved sources give no bright-line test [R42]. Neither turns on [R73]. Carried as `?`
  in Matrix B, in `uk/regulatory/` and in the product documents.
- **Whether a regular-premium unit-linked bond fails TPFR 3.5 limbs (1) and (2)** and thereby
  loses future premiums from the contract boundary. The library's representative product is a
  **single-premium** bond, for which 3.5 is inert; on a regular-premium variant the question is
  live and **the retrieved sources do not settle it for any particular design** [R41].
- **The right coverage-unit basis for an annuity under IFRS 17** [R106].
- **TMTP materiality by product.** The legal availability of TMTP for TA, IP and ULB is
  verified from TMTP 2.4 [R3]; the judgement that the amounts are immaterial, and that
  standalone CI was not a material pre-2016 UK Solvency I reserve line, is **[unverified] — a
  judgement, not a retrieved fact**, and the rules contain no product exclusion.
- **Everything about SS18/16 beyond one sentence** [R48], **everything about SS20/16 beyond
  its landing page** [R120], **SoP10/24 Chapters 3–6** [R83b], and **SS19/16's
  version-to-version differences beyond the scope sentence** [R95].
- **That a non-MA annuity book could in principle take the volatility adjustment** is
  permitted by the rules but is **not the representative UK case**; the market-practice
  statement is **[unverified]** [R1][R2][R54].

