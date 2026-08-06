# Sources — UK Regulatory Balance Sheet, Statutory Accounts and Tax

Source ids, titles, publishers, URLs, access dates and retrieval markers below are carried
**verbatim** from the seven research files that are the citation ground truth for this
directory (`uk/_research/solvency-uk-technical-provisions.md`,
`uk/_research/solvency-uk-discounting-and-transitionals.md`,
`uk/_research/solvency-uk-scr-standard-formula.md`,
`uk/_research/solvency-uk-own-funds-mcr-and-internal-models.md`,
`uk/_research/solvency-uk-reporting-governance.md`,
`uk/_research/uk-accounting-and-tax.md`,
`uk/_research/uk-product-regulatory-applicability.md`). **Ids are never renumbered.** Entries
created by those research files but **not cited** by `uk/regulatory/statutory-accounting-and-capital.md`,
`uk/regulatory/technical-notes.md` or the seven `uk/products/*/technical-notes.md` documents are
omitted, and every omission is recorded by number in "Entries omitted as uncited" below.
No new sources were fetched at drafting; nothing below is marked "added at drafting".

**Access date for every citation in this directory: 2026-08-06**, except the frozen R1–R38
entries, whose own access date (**2026-08-03**) is reproduced in the last section.

---

## What this directory is measuring, and what the file names mean

The UK has **no "statutory accounting" in the U.S. sense** — there is no single regulator-mandated
ledger that is simultaneously the solvency measurement and the published financial statements. The
file names in `uk/regulatory/` mirror `us/regulatory/` for structural parity across the library,
and for no other reason. What the UK content actually covers is **three separate measurements**
built on one cash flow projection:

| Measurement | What it is | Where the sources sit below |
|---|---|---|
| **Solvency UK regulatory balance sheet** | The prudential measurement: PRA Rulebook Parts made under FSMA and the IRPR Regulations 2023 — technical provisions, discounting, SCR, own funds, MCR, reporting, governance | Sections A–O |
| **Statutory accounts** | Companies Act 2006 accounts: FRS 102 + FRS 103, **or** UK-adopted IFRS 17 — a company-law choice at entity level (s.395) | Sections P–R |
| **Tax** | The corporation tax computation built **on the accounts**, with the Finance Act 2012 overlay (BLAGAB I-E, non-BLAGAB trade profit) | Section S |

**One U.S. framing must not transfer.** The U.S. statutory story — acquisition costs expensed as
incurred, no DAC asset, first-year surplus strain — is **reversed** in the UK statutory accounts:
**SI 2008/410 Schedule 3 para 13 requires** that costs of acquiring insurance policies incurred in
one financial year but relating to a subsequent one **must be deferred** [R105], and FRS 103 ¶3.7
requires deferral subject to recoverability, with ¶3.10 barring deferral **for with-profits funds**
[R99]. The owning research file titles its section 3 "Acquisition costs and DAC — the U.S. contrast,
reversed" (`uk/_research/uk-accounting-and-tax.md` §3). The Solvency UK balance sheet, by contrast,
has no DAC at all — it is an Article-75 economic balance sheet [R39].

---

## Note on the shared numbering

The documents in this directory cite **[REG-R#]** against the single UK reference numbering in
`uk/references/regulatory-and-actuarial-references.md`, which after this work runs **R1–R120**,
with **R50, R51, R52, R74, R75, R76** and **R121–R133** permanently unused **by design**. The
blocks were assigned before drafting so six parallel research streams could number independently
without collision:

| Block | Owner (the citation ground truth) | Created | Deliberately unused |
|---|---|---|---|
| **R1–R38** | pre-existing UK prudential / conduct / tax / CMI / professional-standards stream, `uk/references/regulatory-and-actuarial-references.md` | R1–R38 (**frozen**; already cited by the seven product documents) | — |
| **R39–R52** | `uk/_research/solvency-uk-technical-provisions.md` (Valuation Part, TPFR Part, risk margin, surplus funds, reinsurance recoverables, the revoked Delegated Regulation) | R39–R49 | **R50, R51, R52** |
| **R53–R60** | `uk/_research/solvency-uk-discounting-and-transitionals.md` (IRPR Regulations, risk-free curve, DLT, TMIR, TMTP, MA permissions) | R53–R60, plus the lettered sub-id **R60b** | — |
| **R61–R76** | `uk/_research/solvency-uk-scr-standard-formula.md` (SCR General Provisions and Standard Formula Parts, the mass-lapse correction, USPs, capital add-ons, standard-formula adaptations, the un-retrieved annexes) | R61–R73 | **R74, R75, R76** |
| **R77–R83** | `uk/_research/solvency-uk-own-funds-mcr-and-internal-models.md` (Own Funds, MCR, Undertakings in Difficulty, With-Profits, Surplus Funds, RFF guidelines, Internal Models), plus lettered sub-ids R78b, R79b, R80b, R80c, R81b, R81c, R83b, R83c, R83d | R77–R83 and the sub-ids | — |
| **R84–R98** | `uk/_research/solvency-uk-reporting-governance.md` (Reporting Part, the template and instruction library, the life LOG files, Conditions Governing Business, Actuaries, SMFs, ORSA, external audit, model governance, solvent exit), plus sub-ids R88b, R88c, R95b, R96b, R97b, R97c | R84–R98 and the sub-ids | — |
| **R99–R113** | `uk/_research/uk-accounting-and-tax.md` (FRS 103, FRS 102, Companies Act 2006, SI 2008/410 Sch 3, IFRS 17 as adopted, the IFRS 17 tax transitionals, tax rates, deferred tax and LACDT), plus sub-id R102b | R99–R113 | — |
| **R114–R133** | `uk/_research/uk-product-regulatory-applicability.md` (Investments Part, INSPRU heritage, unit matching, prudent person, reinsurance counterparty risk) | R114–R120 | **R121–R133** |

The gaps are not losses and must not be back-filled: the block convention lets a stream finish with
spare numbers so a later pass can extend it without renumbering anything that product documentation
already cites.

---

## Duplicate records — cite only the left-hand number

Six research streams ran in parallel under block-allocated numbering and, inevitably, several of
them retrieved and independently numbered **the same document**. Following the precedent of the
U.S. section — which recorded the R33/R73 overlap rather than silently resolving it — the
duplication is **recorded, not renumbered**. Every document in this directory cites **only** the
canonical number; the right-hand numbers exist in the research files and must not be cited.

| Document | **Canonical — cite this** | Also recorded as (do not cite) | Why the second record exists |
|---|---|---|---|
| PRA Rulebook — Valuation Part | **R39** | R111 | The accounting stream read the same Part for Chapter 11 (Deferred Taxes) only |
| PRA Rulebook: Solvency II Instrument 2024 (PRA2024/13 = PS15/24 Appendix 6) | **R42** | R63 | The SCR stream cited the instrument for the as-made text of `SCR-SF 3B6.6(1)` |
| The Insurance and Reinsurance Undertakings (Prudential Requirements) Regulations 2023 (SI 2023/1347) | **R44** | R53 | The technical-provisions stream read Part 2 Chapter 2 (risk margin); the discounting stream read Part 2 Chapter 1 (matching adjustment) |
| PRA Rulebook — Surplus Funds Part | **R45** | R79 | Read independently by the technical-provisions stream (the TP boundary) and the own-funds stream (the Tier 1 consequence) |
| SS13/15 — *Solvency II: surplus funds* | **R46** | R79b | Same document, retrieved once as the Bank PDF and once as the Rulebook guidance view |
| Commission Delegated Regulation (EU) 2015/35 — assimilated text, **revoked** | **R49** | R66 | The SCR stream additionally retrieved the point-in-time text of Article 142 |
| PRA "Technical information for Solvency II firms" | **R54** | R67 | The SCR stream read the symmetric-adjustment (SAECC) content of the same publication page |
| PRA Rulebook — SCR – Standard Formula Part | **R62** | R112 | The accounting stream read the same Part for Chapter 6 (LACTP / LACDT) only |
| SS15/16 — model drift and standard formula SCR reporting | **R68** | R81c, R97c | Retrieved by three streams; **three** records of one 8-page supervisory statement |
| SS14/15 — *With-profits*, Chapter 2 (ring-fenced funds) | **R71** | R80b | Same chapter, retrieved once through the SCR stream and once through the own-funds stream |
| SS1/24 — internal model expectations | **R81b** | R97b | The own-funds stream retrieved the PDF; the governance stream retrieved only the publication page |
| PS18/26 | **R87** | R83d | R87 is a two-document entry (PS15/25 **and** PS18/26); R83d records PS18/26's own-funds chapter alone |

Two of these are worth reading twice, because the *retrieval quality* differs between the duplicate
records and the canonical entry carries the better one:

- **R81b vs R97b.** R81b is the SS1/24 **PDF, read in full**. R97b is the **publication page only** —
  its content is `[unverified]` beyond a scope list. Citing R81b is citing the read document.
- **R68 vs R81c vs R97c.** All three read the September 2025 PDF; the extracted character counts
  differ slightly (7,699 / 7,512 / 7,332), which is an extraction artefact, not three documents.

---

## Entries omitted as uncited

Created by the research files, **not cited** by any document in this directory, and therefore not
carried below. Recorded by number so the omission is visible rather than silent:

- **R53, R63, R66, R67, R79, R79b, R80b, R81c, R83d, R97b, R97c, R111, R112** — the duplicate
  records listed in the table above. Their content is cited under the canonical number.
- **R60b** (PS17/25, *Matching Adjustment Investment Accelerator*) — recorded in the research file
  as **fetched_ok: no**; its existence, date and effect are verified only indirectly, and no number
  in this directory comes from it. The MAIA content that *is* used is cited to [R2], [R8] and [R60].
- **R78b** (SS4/15 — *Solvency II: the solvency and minimum capital requirements*) — retrieved
  specifically to establish that its **Chapter 4 on the MCR is `[Deleted]`**, i.e. that there is no
  surviving PRA supervisory guidance on the MCR. The finding is used in the drafted documents; the
  entry itself is not cited, because the MCR Part [R78] is the whole of the authority.
- **R83b** (SoP10/24 — own funds permissions), **R83c** (CP4/26 — own funds updates and fixes) —
  permissions process and a live consultation; neither bears on a calculation this directory
  specifies.
- **R88c** (PRA *Solvency UK regulatory reporting – Questions & Answers*, October 2025) — expressly
  **"not PRA's reporting policy"** on its own cover note; the operative statements it carries are
  cited to [R84] and [R88].
- **R102b** (FRC library page for FRS 102) — an edition register; the standard itself is [R102].
- **R113** (BEIS letter to the FRC, 3 February 2017) — its *premise* is stale (the Schedule 3 text
  it interprets no longer contains the Solvency II reference), and its *conclusion* is
  independently carried by FRS 103 BC45 [R99], which is what the drafted documents cite.
- **R117** (SS1/14 — *Mutuality and with-profits funds: a way forward*) — mutual-specific waiver
  policy; the one proposition this directory needs from it (that each with-profits fund generally
  displays RFF characteristics) is stated in SS14/15 ¶2.2 [R71], which is cited instead. The
  research file also records that **the exact retrieval URL for R117 was not preserved**, which is a
  second reason not to carry it.

**R74, R75, R76, R50, R51, R52 and R121–R133 are unused by design and were never created.** They
are not omissions.

---

## A. The Solvency UK economic balance sheet and the technical provisions

### R39. PRA Rulebook — **Valuation Part** (as at 05/08/2026)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.prarulebook.co.uk/pra-rules/valuation/05-08-2026
- **Accessed:** 2026-08-06
- **Fetched:** yes (browser User-Agent; **prarulebook.co.uk returns HTTP 403 to plain fetchers**.
  Present-view URL re-verified 2026-08-06: HTTP 200, 130,238 bytes). Chapters 1 to 12 read in full.
- **Date-stamp note carried forward:** Chapters 1 and 2 carry 01/01/2016; Chapters 3 to 12 carry
  **31/12/2024**, i.e. they are the restated Delegated-Regulation material.
- **Duplicate record:** the accounting stream separately numbered **Chapter 11 (Deferred Taxes)** of
  this same Part as **R111** (130,226 bytes → 20,494 chars; Chapters 1–12 read). **Cite R39.**

### R40. SS38/15 — *Solvency II: consistency of UK generally accepted accounting principles with Solvency II* (November 2024, updating August 2015)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URLs:** landing page
  https://www.bankofengland.co.uk/prudential-regulation/publication/2015/solvency2-consistency-of-uk-generally-accepted-accounting-principles-with-the-solvency2-directive-ss ;
  PDF read
  https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/supervisory-statement/2024/ss3815-november-2024-update.pdf
- **Accessed:** 2026-08-06
- **Fetched:** yes (supervisory statement, PDF, 11 pages; PDF text extracted; PDF URL re-verified
  2026-08-06: HTTP 200, 991,592 bytes)
- **Vintage caution carried forward:** the November 2024 annex records that the update only
  **re-pointed references from DR (EU) 2015/35 to PRA Rulebook rules** and did **not** refresh the
  underlying UK-GAAP / IFRS analysis in the section 2 table.

### R41. PRA Rulebook — **Technical Provisions – Further Requirements Part** (as at 05/08/2026), including Annex 1
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.prarulebook.co.uk/pra-rules/technical-provisions-further-requirements/05-08-2026
  (the slug uses **single hyphens**, not the triple-hyphen form used by some other Parts; the
  triple-hyphen variant returns HTTP 404)
- **Accessed:** 2026-08-06
- **Fetched:** yes (browser User-Agent; URL re-verified 2026-08-06: HTTP 200, 259,991 bytes).
  **Read in full**, Chapters 1–27 and **Annex 1 Parts A–E (lines of business 1–36)**.
- **Date-stamp note carried forward:** every rule in the Part carries **31/12/2024** and the Part has
  only one history date — it is wholly new.
- **Negative finding carried forward:** the Part contains **no risk-margin simplification, no
  simplified counterparty-default adjustment and no simplified recoverables calculation**; the
  heading "SIMPLIFICATIONS" introduces Chapter 27 (Proportionality) alone.

### R42. **PRA Rulebook: Solvency II Instrument 2024** (PRA2024/13) — Appendix 6 to PS15/24
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/policy-statement/2024/november/ps1524app6.pdf
- **Accessed:** 2026-08-06
- **Fetched:** yes (legal instrument, PDF, 250 pages; PDF text extracted, ~681 KB of text; URL
  re-verified 2026-08-06: HTTP 200, 1,780,845 bytes)
- **Why it is numbered separately from [R6]:** [R6] is the PS15/24 **policy statement** (frozen).
  R42 is the distinct **legal instrument** with its own citation (PRA2024/13), and is what a drafter
  must cite for the *text* of the restated rules.
- **Duplicate record:** the SCR stream separately numbered the same instrument as **R63**, retrieved
  through the PS15/24 publication page (681,045 chars extracted; **searched, not read whole**) and
  cited there for one purpose only — the as-made wording of `SCR-SF 3B6.6(1)`. **Cite R42.**

### R43. PRA Rulebook — **Glossary** (as at 05/08/2026)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.prarulebook.co.uk/glossary (re-verified 2026-08-06: HTTP 200, 76,049 bytes;
  `/pra-rules/glossary` is a **404**)
- **Accessed:** 2026-08-06
- **Fetched:** yes (browser User-Agent, printable letter views)
- **Retrieval limit carried forward:** the per-letter printable exports actually read (letters
  **B, E, F, M, R, T, V**) were retrieved in an earlier session and **their exact query URLs were
  not preserved** — treat the base URL as the citation and the letter views as navigation. The
  own-funds stream separately records that **glossary letter S was not retrievable** in its session,
  which is why the Glossary definition of *surplus funds* itself is nowhere quoted in this directory.

---

## B. The risk margin — the statutory layer

### R44. The Insurance and Reinsurance Undertakings (Prudential Requirements) Regulations 2023 (SI 2023/1347)
- **Publisher:** legislation.gov.uk (HM Treasury statutory instrument), as-amended view
- **URLs:** contents https://www.legislation.gov.uk/uksi/2023/1347/contents (re-verified
  2026-08-06: HTTP 200) ; instrument https://www.legislation.gov.uk/uksi/2023/1347
- **Accessed:** 2026-08-06
- **Fetched:** yes. The technical-provisions stream read **Part 2 Chapter 2 (regulations 7A–7C)**;
  the discounting stream read **Part 2 Chapter 1 in full** (regulations 3–7, the matching-adjustment
  layer) and **skimmed Chapter 2**.
- **Distinct from [R4]**, which is SI 2023/**1346**, the Risk Margin Regulations. The two are easily
  confused; they are different instruments.
- **Extraction failure carried forward:** **the risk-margin formula in regulation 7B is an image on
  legislation.gov.uk and came back empty from text extraction.** The symbol definitions (a)–(h) are
  text and were read. The transcribed formula in the drafted documents therefore comes from
  **Technical Provisions 4A.1 [R1]**, which the Rulebook renders as LaTeX in the page text. [R4]
  prints the same formula as an image and is equally unreadable.
- **Typographical defect recorded, not corrected:** the legislation.gov.uk textual-amendment note
  displays the SI 2024/1083 commencement as "1.11.2024 for specified purposes and **31.12.20204**
  otherwise". The intended date is plainly 31.12.2024; it is recorded here as printed.
- **Not read:** **SI 2024/1083** itself (https://www.legislation.gov.uk/uksi/2024/1083/contents
  verified HTTP 200 but **not read**) — everything recorded about it comes from the
  textual-amendment notes inside R44.
- **Duplicate record:** numbered **R53** by the discounting stream. **Cite R44.**

---

## C. With-profits — surplus funds and the technical-provisions boundary

### R45. PRA Rulebook — **Surplus Funds Part** (as at 05/08/2026)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.prarulebook.co.uk/pra-rules/surplus-funds/05-08-2026 (re-verified 2026-08-06:
  HTTP 200, 82,668 bytes; the own-funds stream records the same retrieval as 8,907 chars of
  extracted text)
- **Accessed:** 2026-08-06
- **Fetched:** yes (browser User-Agent). **Read in full**, Chapters 1–4.
- **Date-stamp note carried forward:** all substantive rules are date-stamped **01/01/2016** except
  the 1.2 definition of *with-profits assets* (31/12/2024) — the Surplus Funds Part was **not**
  rewritten by PS15/24 [R6].
- **Glossary limit carried forward:** the Glossary definition of "**surplus funds**" itself **could
  not be retrieved** (see R43). Nothing in this directory quotes it.
- **Duplicate record:** numbered **R79** by the own-funds stream. **Cite R45.**

### R46. SS13/15 — *Solvency II: surplus funds* (November 2024, updating March 2015)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URLs:** landing page
  https://www.bankofengland.co.uk/prudential-regulation/publication/2015/solvency2-surplus-funds-ss ;
  PDF read
  https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/supervisory-statement/2024/ss1315-november-2024-update.pdf ;
  Rulebook guidance view
  https://www.prarulebook.co.uk/guidance/supervisory-statements/ss13-15---solvency-ii-surplus-funds/05-08-2026
- **Accessed:** 2026-08-06
- **Fetched:** yes (supervisory statement, PDF, 7 pages, text extracted; the own-funds stream
  separately retrieved the Rulebook guidance view, 9,646 chars, read in full)
- **Note carried forward:** **¶2.2 is [DELETED]**. Paragraphs 1.1–1.5, 2.1, 2.3 and 3.6 are
  date-stamped 31/12/2024; the rest 20/03/2015.
- **Duplicate record:** the own-funds stream's Rulebook-guidance retrieval is numbered **R79b**.
  **Cite R46.**

---

## D. Reinsurance recoverables — the two supervisory statements that bite

### R47. SS5/24 — *Funded reinsurance* (October 2025, updating November 2024)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/supervisory-statement/2025/ss524-october-2025.pdf
  (re-verified 2026-08-06: HTTP 200, 370,064 bytes)
- **Accessed:** 2026-08-06
- **Fetched:** yes (supervisory statement, PDF text extracted)
- **Retrieval limit carried forward:** **read for its technical-provisions interface only.** The
  risk-management, collateral and internal-model content belongs to other streams and was not
  transcribed.
- **Cross-reference conflict recorded, not resolved:** ¶1.7 tells firms to read SS5/24 "in
  conjunction with … **Chapters 6, 7 and 11 of the Technical Provisions**". In the Rulebook as at
  05/08/2026 those chapters are the **[Deleted]** matching-adjustment chapters (6 and 7, deleted as
  at 30/06/2024) and Chapter 11 (Recoverables from Reinsurance Contracts and ISPVs) [R1]; only the
  reference to Chapter 11 is live. Reproduced as a conflict, not harmonised.

### R48. SS18/16 — *Solvency II: longevity risk transfers* (November 2024, updating January 2020)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URLs:** landing page
  https://www.bankofengland.co.uk/prudential-regulation/publication/2016/solvency2-longevity-risk-transfers-ss ;
  PDF read
  https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/supervisory-statement/2024/ss1816-november-2024-update.pdf
- **Accessed:** 2026-08-06
- **Fetched:** yes (PDF text extracted). **Read only in part — grep-level reading** for the
  technical-provisions and counterparty-default interface; the transaction-structuring and
  pre-notification content was **not transcribed**.
- **[unverified] carried forward:** apart from the single verified observation that holding SCR
  counterparty-default capital "may not be sufficient in and of itself", **everything else about
  SS18/16 is [unverified]** and should be re-read before it is cited for anything more.

---

## E. Provenance of the superseded law

### R49. Commission Delegated Regulation (EU) 2015/35 — assimilated text, **marked "(revoked)"**
- **Publisher:** legislation.gov.uk (assimilated EU law) / The National Archives
- **URLs:** contents https://www.legislation.gov.uk/eur/2015/35/contents (re-verified 2026-08-06:
  HTTP 200) ; Article 1 (definitions) https://www.legislation.gov.uk/eur/2015/35/article/1
  (re-verified 2026-08-06: HTTP 200)
- **Accessed:** 2026-08-06
- **Fetched:** yes — **table of contents and Article 1 read; the article bodies were NOT read.**
- **Status, and it matters:** the title line reads "… **(revoked)**", and the page states it "is up
  to date with all changes known to be in force on or before 04 August 2026". This is a **negative /
  provenance** source: cite it only to explain what a legacy or EU-vintage document is referring to,
  never as operative UK law.
- **Duplicate record:** the SCR stream separately retrieved **Article 142** (lapse risk sub-module)
  in a **point-in-time view** and numbered it **R66** (current view 12,562 chars; point-in-time view
  17,881 chars, containing the full Article 142 text; contents listing 58,238 chars). That record
  carries the revocation annotation "Regulation revoked (**30.6.2024** for the revocation of
  Arts. 52-54; **31.12.2024** in so far as not already in force)". **Cite R49.**

---

## F. Discounting — the risk-free interest rate term structure

### R54. Bank of England / PRA — *Technical information for Solvency II firms*
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.bankofengland.co.uk/prudential-regulation/key-initiatives/solvency-ii/technical-information
- **Doc type:** standing web publication plus monthly data releases (XLSX)
- **Accessed:** 2026-08-06
- **Fetched:** yes (page text retrieved with a browser User-Agent; **the site 403s plain fetchers**;
  the SCR stream records the same page as 32,183 chars, read in full)
- **Retrieval limit carried forward, and it is the load-bearing one:** **the XLSX data files
  themselves were NOT opened.** Consequently **no risk-free rate, no fundamental spread, no
  volatility adjustment value, no ultimate forward rate, no alpha / convergence parameter, no credit
  risk adjustment in basis points and no symmetric adjustment (SAECC) value is stated anywhere in
  this directory.** The four monthly files are named on the page (*Risk-free curves*, *Risk-free
  Volatility Adjustment portfolios*, *Smith-Wilson extrapolation parameters*, *Risk-free Fundamental
  Spreads, Probability of Default and Cost of Downgrade*); none was opened.
- **Release index verified** as running to **30 June 2026 (published 8 July 2026)** at the access
  date.
- **Duplicate record:** the SCR stream numbered the **symmetric-adjustment / SAECC content of the
  same publication page** as **R67**, and records equally that **the SAECC spreadsheet (XLSX) was
  not retrieved**. **Cite R54.**

### R55. Statement of Policy 1/20 — *The PRA's approach to the publication of Solvency II technical information* (November 2024, updating June 2024)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.bankofengland.co.uk/prudential-regulation/publication/2020/the-pras-approach-to-publication-of-sii-technical-information
  (verified to return HTTP 200 on 2026-08-06)
- **Accessed:** 2026-08-06
- **Fetched:** yes (statement of policy, PDF, 11 pages; **PDF text extracted in full**)
- **Negative finding carried forward, stated in the research file's own words:** "**No numeric UFR,
  alpha or CRA is given in this document.**" The methodology is described (¶3.6A4–3.6A5); the
  numbers live in the monthly XLSX files at R54, which were not opened.

### R56. Bank of England / PRA — *Deep, liquid, and transparent (DLT) assessment for January 2026 implementation*
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.bankofengland.co.uk/prudential-regulation/key-initiatives/solvency-ii/dlt-assessments-jan26
  (link taken from the technical-information page [R54] on 2026-08-06; the sibling pages
  `dlt-assessments-jan22` … `dlt-assessments-jan25` hold the earlier annual assessments)
- **Doc type:** web publication with a per-currency maturity table. Published 28 November 2025;
  effective 1 January 2026.
- **Accessed:** 2026-08-06
- **Fetched:** yes (page text; **the tabular grid extracted unreliably**)
- **Extraction defect carried forward, with its consequence:** the per-maturity D/L grid **did not
  survive text extraction with a reliable column alignment** — the GBP row yielded **18 marks against
  a 20-column maturity header**. Therefore: the **GBP last liquid point (50 years) and the EUR last
  liquid point (20 years) are verified from prose**, the **USD and CAD LLPs are recorded as not
  retrieved**, and **no per-maturity DLT flag is transcribed anywhere in this directory.**

---

## G. Discounting — transitionals, and the matching-adjustment permissions layer

### R57. PRA Rulebook — **Transitional Measures Part** (Chapters 10 and 12: the transitional measure on the risk-free interest rate)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.prarulebook.co.uk/pra-rules/transitional-measures
- **Accessed:** 2026-08-06
- **Fetched:** yes (browser User-Agent; **prarulebook.co.uk 403s plain fetchers**), read in the
  "present on 05/08/2026" view
- **Retrieval limit carried forward:** **retrieved for Chapters 10 and 12 only.** Chapter 11
  (Technical Provisions) is **[Deleted]** from 31/12/2024, the TMTP having moved to its own Part
  [R3]; Chapters 1–9 are legacy 2016 transitionals and were **not** read for content. The drafted
  documents therefore record **Transitional Measures 4.1 grandfathering of pre-2016 own-funds
  instruments into Tier 1 as [unverified]**.

### R58. Statement of Policy 2/24 — *Permissions for transitional measures on technical provisions and risk-free interest rates* (November 2024, updating February 2024)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.bankofengland.co.uk/prudential-regulation/publication/2024/february/permissions-for-transitional-measures-on-technical-provisions-and-risk-free-interest-rates-sop
  (**the same path without the trailing `-sop` returns HTTP 404 — verified 2026-08-06**; the
  February 2024 PDF sits at
  https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/statement-of-policy/2024/permissions-for-transitional-measures-on-technical-provisions-and-risk-free-interest-rates-feb-2024.pdf)
- **Accessed:** 2026-08-06
- **Fetched:** yes (statement of policy, PDF, 16 pages; **PDF text extracted in full — the November
  2024 version**). Effective **31 December 2024**.

### R59. SS17/15 — *Solvency II: transitional measures on risk-free interest rates and technical provisions* (November 2024, updating February 2024)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URLs:** PDF read
  https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/supervisory-statement/2024/ss1715-november-2024-update.pdf ;
  landing page
  https://www.bankofengland.co.uk/prudential-regulation/publication/2015/solvency2-transitional-measures-on-risk-free-interest-rates-and-technical-provisions-ss
- **Accessed:** 2026-08-06
- **Fetched:** yes (supervisory statement, PDF, 15 pages; **PDF text extracted in full**). Published
  15 November 2024, effective 31 December 2024.

### R60. Statement of Policy 8/24 — *Solvency II: Matching Adjustment Permissions and Matching Adjustment Investment Accelerator Permissions* (October 2025, updating June 2024)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URLs:** PDF read
  https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/statement-of-policy/2025/sop824.pdf ;
  landing page
  https://www.bankofengland.co.uk/prudential-regulation/publication/2024/june/solvency-ii-matching-adjustment-permissions-statement-of-policy
- **Accessed:** 2026-08-06
- **Fetched:** yes (statement of policy, PDF, 22 pages; **PDF text extracted in full; read closely
  for Chapters 1, 2, 2A and 3**)
- **Companion entry not carried:** **R60b (PS17/25, *Matching Adjustment Investment Accelerator*)**
  is recorded in the research file as **fetched_ok: no** — the URL cited in the SS7/18 footnote
  returns HTTP 404 and the recovered page's body extraction failed. **No MAIA number in this
  directory comes from PS17/25**; every one is cited to [R2], [R8] or R60. See "Entries omitted as
  uncited".

---

## H. The Solvency Capital Requirement — the two Rulebook Parts and the correction

### R61. PRA Rulebook — **Solvency Capital Requirement – General Provisions Part** (as at 05/08/2026)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.prarulebook.co.uk/pra-rules/solvency-capital-requirement---general-provisions/05-08-2026
- **Accessed:** 2026-08-06
- **Fetched:** yes (browser User-Agent required — **prarulebook.co.uk returns HTTP 403 to plain
  fetchers**; 14,517 chars of extracted text; **read in full**, all 8 chapters)
- **Limit carried forward:** rule **3.1** carries the 31/12/2024 restatement date and **a
  pre-31/12/2024 version exists and was not retrieved**.

### R62. PRA Rulebook — **Solvency Capital Requirement – Standard Formula Part** (as at 05/08/2026)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.prarulebook.co.uk/pra-rules/solvency-capital-requirement---standard-formula/05-08-2026
- **Accessed:** 2026-08-06
- **Fetched:** yes (browser User-Agent required; **452,843 chars raw / 408,900 chars cleaned — the
  single largest document in the UK library**). **Read selectively, by chapter:** chapters 2, 2A, 3,
  3B, 3C, 3D (interest rate, equity, symmetric adjustment, property, spread on bonds and loans,
  spread on MA portfolios, concentration, currency), 3E13–3E15, 3F, 4, 5, 6, 7.1–7.16, 8 and 9 read
  in full; **chapters 1D, 3A (non-life), 3D18–3D24 (securitisation, credit derivatives, specific
  exposures) and 3G were surveyed only.**
- **One source, not four:** the local copies `cap-scr-standard-formula.txt`, `s5-scr-sf.txt`,
  `acct-pra-scr-sf.txt` and `pra-scr-sf.txt` are byte-identical (452,843) — one document.
- **Future version not retrieved:** the Part's change dates are **01/01/2016, 31/12/2024,
  24/07/2025, 01/01/2026, 01/01/2027**; **rule 1.2 carries a future version after 01/01/2027 that was
  not retrieved.**
- **Duplicate record:** the accounting stream separately numbered **Chapter 6 (Adjustment for
  Loss-Absorbing Capacity of Technical Provisions and Deferred Taxes)** of this same Part as
  **R112** (1,673,565 bytes → 426,846 chars; **Chapter 6 read in full, remainder searched only**).
  **Cite R62.**

### R64. PRA statement, 20 December 2024 — *Restatement of Solvency II assimilated law: correction to standard formula mass lapse life underwriting risk rule in PS15/24*, with **PRA Rulebook: SII Firms: Solvency II Amendment (No 1) Instrument 2024**
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.bankofengland.co.uk/prudential-regulation/publication/2024/december/pra-statement-on-restatement-of-solvency-ii-assimilated-law
- **Accessed:** 2026-08-06
- **Fetched:** yes (5,602 chars; **read in full**). **The annexed instrument PDF itself was not
  separately retrieved** — the statement describes its single operative effect.
- **Residual discrepancy recorded, not resolved:** the statement's own narrative names **RAO Schedule
  1 Part II class II and class VII** as the transposition-table result, while the corrected rule text
  as read in [R62] names **class VII only**.

### R65. PRA Rulebook — **Solvency Capital Requirement – Undertaking Specific Parameters Part** (as at 05/08/2026)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.prarulebook.co.uk/pra-rules/solvency-capital-requirement---undertaking-specific-parameters/05-08-2026
- **Accessed:** 2026-08-06
- **Fetched:** yes (60,255 chars raw / 54,158 cleaned; **chapters 1–3 and 7 read in full, chapters
  4–6 and 8–10 surveyed**; URL independently re-verified on 2026-08-06). Part change dates
  **31/12/2024** and **24/07/2025**.

### R73. PRA Rulebook — **Annexes to the SCR – Standard Formula Part** (referenced by `SCR-SF 2A.1`)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** linked from
  https://www.prarulebook.co.uk/pra-rules/solvency-capital-requirement---standard-formula/05-08-2026
  (rule 2A.1: "The Annexes referred to in 3A, 3C and 7 can be found here")
- **Accessed:** 2026-08-06
- **Fetched:** **NO** — the annexes are a separate linked file that was **not retrieved**; only the
  pointer rule 2A.1 [31/12/2024] was read, in [R62].
- **Why the number exists at all:** it was assigned deliberately **so the gap has a citable handle**.
  What is missing with it: **Annex XVI** (health catastrophe — the country list, the ratio of persons
  affected `r_s`, the event types `e`, the benefit ratios `x_e`, and the healthcare-utilisation types
  `h` and ratios `H_h` for the pandemic sub-module), **Annexes V–VIII and X** (non-life catastrophe
  zones and risk weights), and the annex behind the geographical-diversification factor in `3A5`.
  **None of these values is stated anywhere in this directory**, and the health catastrophe
  sub-module cannot be computed from this library.
- **Conflict recorded, not resolved — the numbered line-of-business list.** The SCR stream recorded
  the numbered line-of-business list as un-retrieved along with these annexes. It is not
  un-retrieved: **TPFR Annex 1 Parts A–E (lines of business 1–36) was read in full** [R41], and
  `uk/_research/uk-product-regulatory-applicability.md` treats the numbering the SCR Parts key on
  and the TPFR Annex 1 numbering as **the same list**, on cross-references in the restatement
  instrument [R42] — but expressly as **a drafter's inference from consistent cross-references, not
  a statement in any retrieved document**. The mapping of a UK critical-illness or
  income-protection contract to a numbered line of business therefore remains **[unverified]** —
  not because the list was never retrieved, but because **no retrieved document states the
  conclusion**.

---

## I. The SCR — supervisory statements and statements of policy

### R68. SS15/16 — *Solvency II: Monitoring model drift and standard formula SCR reporting for firms with permission to use an internal model* (September 2025, updating July 2018)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URLs:** landing page
  https://www.bankofengland.co.uk/prudential-regulation/publication/2016/solvency2-monitoring-model-drift-and-standard-formula-scr-reporting-ss ;
  PDF
  https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/supervisory-statement/2025/ss1516-september-2025-update.pdf
  (verified HTTP 200)
- **Accessed:** 2026-08-06
- **Fetched:** yes (supervisory statement, PDF, 7–8 pages; **read in full**)
- **Triple record, recorded not resolved:** three streams retrieved the same September 2025 PDF and
  numbered it **R68 / R81c / R97c**, with extracted character counts of **7,699 / 7,512 / 7,332**.
  That spread is a text-extraction artefact of one document, not evidence of three. **Cite R68.**

### R69. Statement of Policy 4/24 — *Solvency II: Capital add-ons* (November 2024, updating February 2024)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.bankofengland.co.uk/prudential-regulation/publication/2024/february/solvency-ii-capital-add-ons-sop
- **Accessed:** 2026-08-06
- **Fetched:** yes (41,615 chars; **title page, contents and scope verified from retrieved text; the
  body was surveyed, not transcribed**)
- **Numbers deliberately not transcribed:** the PRA's **quantitative thresholds for what counts as a
  "significant risk profile deviation" were not read out of the retrieved text** and **must not be
  stated**. The drafted documents say so at the point of use. Recorded for the drafter as the place
  to look, not as a source of numbers.

### R70. SoP11/24 — *Solvency II: The PRA's approach to Standard Formula adaptations* (15 November 2024)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.bankofengland.co.uk/prudential-regulation/publication/2024/november/solvency-ii-approach-to-standard-formula-adaptations-sop
- **Accessed:** 2026-08-06
- **Fetched:** **partial** — the **landing page** was retrieved and read in full (2,498 chars); **the
  SoP PDF itself was not retrieved.**
- **Limit carried forward:** **no content beyond the scope statement was retrieved — do not
  attribute detail to it.** Effective 31 December 2024, following PS15/24 [R6].

### R71. SS14/15 — *With-profits*, **Chapter 2: Solvency II ring-fenced fund (RFF) regime**
- **Publisher:** Prudential Regulation Authority (Bank of England), via the PRA Rulebook guidance view
- **URL:** https://www.prarulebook.co.uk/guidance/supervisory-statements/ss14-15---with-profits/2-solvency-ii-ring-fenced-fund-rff-regime/25-06-2024
- **Accessed:** 2026-08-06
- **Fetched:** yes (2,058 chars; **Chapter 2 read in full**. Printed 05/08/2026, rulebook text as at
  25/06/2024. **Other chapters of SS14/15 were not retrieved in this stream.**) All three paragraphs
  date-stamped 20/03/2015.
- **Duplicate record:** the own-funds stream numbered the same chapter **R80b**, retrieved as a
  Rulebook chapter view (1,997 chars, read in full) **plus the full SS PDF text (16,108 chars)** read
  for RFF, surplus-funds and inherited-estate references. That record adds Chapter 9
  (reattributions of inherited estate) and notes that **the EIOPA guidelines on ring-fenced funds
  referenced in SS14/15 footnote 4 were not retrieved from that path** — they were retrieved
  separately as [R80c]. **Cite R71.**

### R72. PS12/25 — *Restatement of CRR and Solvency II requirements in PRA Rulebook – 2026 implementation* (17 July 2025)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.bankofengland.co.uk/prudential-regulation/publication/2025/july/restatement-of-crr-and-sii-requirements-in-pra-rulebook-policy-statement
- **Accessed:** 2026-08-06
- **Fetched:** yes (59,392 chars; **Chapter 3 (ECAI mapping) read; Chapters 1, 4 and the appendix
  list surveyed**)
- **Numbers deliberately not transcribed:** **the ECAI-to-credit-quality-step mapping tables
  themselves are not transcribed.** The CQS *inputs* to `3D17`, `3D25`, `3D29`, `3D30` and `3E12`
  come from this instrument (Appendix 6, *PRA Rulebook: CRR Firms, Solvency II Firms: Credit Quality
  Steps Mapping Instrument 2025*), and a drafter needs the instrument, not this library, for them.

---

## J. Own funds, the MCR, and what a breach costs

### R77. PRA Rulebook — **Own Funds Part** (as at 05/08/2026)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.prarulebook.co.uk/pra-rules/own-funds/05-08-2026
- **Accessed:** 2026-08-06
- **Fetched:** yes (browser User-Agent required; **plain fetchers get HTTP 403**. 74,507 chars of
  extracted text; **read in full, chapter by chapter**)
- **Future view not retrieved, and it matters:** the Part carries **live future markers after
  31/12/2026 on rules 3A.1, 3B.1, 3C.1, 3D.1, 3E.1, 3F.1 and 3G.1** — the Tier 1 / Tier 2 / Tier 3
  lists and the reconciliation reserve. **That future text was not retrieved.** Rule 1.2 is
  02/01/2026; Chapter 2 and the Chapter 3 core rules are mostly 01/01/2016; 3A–3L, 3.4A, 4A and
  Chapter 5 are **31/12/2024**.

### R78. PRA Rulebook — **Minimum Capital Requirement Part** (as at 05/08/2026)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.prarulebook.co.uk/pra-rules/minimum-capital-requirement/05-08-2026
- **Accessed:** 2026-08-06
- **Fetched:** yes (16,664 chars; **read in full — the Part is short**)
- **Transcription limit carried forward:** **Chapter 6, the non-life segment factor table
  (`alpha_s`, `beta_s`), is transcribed only in outline** in the research file, because it does not
  bite on life products. No non-life segment factor is stated in this directory.
- **Companion entry not carried:** the Part page names **SS4/15 — *Solvency II: the solvency and
  minimum capital requirements*** as related guidance. It was retrieved by the own-funds stream as
  **R78b** (Rulebook guidance view, 7,750 chars, read in full) **for one purpose: to establish that
  its Chapter 4 on the MCR is `[Deleted]` as at 31/12/2024.** There is therefore **no surviving PRA
  supervisory guidance on the MCR**; the MCR Part is the whole of it. R78b is not cited — see
  "Entries omitted as uncited".

### R82. PRA Rulebook — **Undertakings in Difficulty Part** (as at 05/08/2026)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.prarulebook.co.uk/pra-rules/undertakings-in-difficulty/05-08-2026
- **Accessed:** 2026-08-06
- **Fetched:** yes (5,802 chars; **read in full** — six short chapters)
- **Negative finding carried forward:** **the Part contains no rule withdrawing authorisation on an
  MCR breach.** If that consequence exists in UK law it sits outside this Part and **was not
  located**. Related guidance named on the Part page — **SoP12/24**, on the permissible recovery
  period to restore full SCR cover — was **not retrieved**.

### R83. SS2/15 — *Solvency II: Own funds* (November 2024, updating September 2019)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/supervisory-statement/2024/ss215-november-2024-update.pdf
- **Accessed:** 2026-08-06
- **Fetched:** yes (supervisory statement, PDF, 8 pages; 11,550 chars; **read in full**)
- **Note carried forward:** **Chapter 3 (own funds transitionals) is deleted in its entirety.** The
  Annex records the November 2024 update following PS15/24 [R6], which rewrote all cross-references
  from Commission Delegated Regulation (EU) 2015/35 to PRA Rulebook rules.
- **Companion entries not carried:** **R83b** (SoP10/24, own funds permissions — PDF read for
  Chapters 1, 2 and 7; **Chapters 3–6 substantive content is `[unverified]`**, and the SoP cites Own
  Funds 3B.14, 3B.15, 3E.6, 3E.7, 3G.6 and 3G.7, **rules that exist in the Part but were not
  transcribed**), **R83c** (CP4/26, a live consultation published 25 February 2026) and **R83d**
  (PS18/26 Chapter 3, the own-funds chapter, whose **amended Own Funds rule text in Appendix 3 was
  not retrieved**). None is cited; PS18/26 is cited as **[R87]**.

---

## K. Ring-fenced funds and the with-profits capital perimeter

### R80. PRA Rulebook — **With-Profits Part** (as at 05/08/2026), with the Glossary definitions of *ring-fenced fund* and *restricted own funds*
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.prarulebook.co.uk/pra-rules/with-profits/05-08-2026
- **Accessed:** 2026-08-06
- **Fetched:** yes (3,368 chars; **read in full** — the Part is four short chapters). **Glossary
  letter R page retrieved separately in the same effort (18,060 chars); glossary letter S was NOT
  retrievable this session.** All four chapters are date-stamped **01/01/2016** — the Part was
  untouched by PS15/24 [R6].
- **Related guidance named on the Part page:** SS1/14, SS14/15, SS22/15 — **SS1/14 not retrieved
  from this path** (it was retrieved separately by the product-applicability stream as R117, which is
  not cited here; see "Entries omitted as uncited").

### R80c. EIOPA — *Guidelines on ring-fenced funds* (EIOPA-BoS-14/169 EN), as republished by the Bank of England
- **Publisher:** EIOPA; republished on the Bank of England site and linked from the Own Funds Part
  page as an "Other link"
- **URL:** https://www.bankofengland.co.uk/-/media/boe/files/paper/2020/december/gl-ring-fenced-funds.pdf
- **Accessed:** 2026-08-06
- **Fetched:** yes (EIOPA guidelines, PDF, 13 pages; 172,465-byte PDF → 33,454 chars; **read in
  full**). Seventeen guidelines.
- **Status caveat, which must travel with every citation:** **every article reference in this
  document is to the Solvency II Directive and Commission Delegated Regulation (EU) 2015/35** —
  Articles 80, 81, 216, 217, 227(2) and 234(b)(ii) DR and Articles 99(b), 104, 111(1)(h), 304 SII —
  **none of which is the operative UK citation any more**, because PS15/24 [R6] restated them into
  the Own Funds and SCR – Standard Formula Parts. The document carries a Bank of England
  copyright/application note pointing at **SoP1/19 — *Interpretation of EU Guidelines and
  Recommendations: Bank of England and PRA approach after the UK's withdrawal from the EU*
  (not retrieved)**, which is the instrument determining how far the guidelines still apply.
  **CP4/26 Proposal 4 does not name the ring-fenced funds guidelines**, so as at 2026-08-06 they
  remain guidelines applied via SoP1/19 rather than PRA rule text.

---

## L. Internal models

### R81. PRA Rulebook — **Solvency Capital Requirement – Internal Models Part** (as at 05/08/2026)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.prarulebook.co.uk/pra-rules/solvency-capital-requirement---internal-models/05-08-2026
- **Accessed:** 2026-08-06
- **Fetched:** yes (63,473 chars; **read in full, chapter by chapter**)
- **Note carried forward:** **Chapter 13 (profit and loss attribution) is `[Deleted]`** and Chapter
  13A (analysis of change) replaces it. Every substantive chapter is date-stamped **31/12/2024**
  except 12.1–12.3, 11.3, 11.5–11.7, 15.1, 16.1, 7.2 and 17 (01/01/2016) and 1.2 / 16F.3
  (24/07/2025).

### R81b. SS1/24 — *Expectations for meeting the PRA's internal model requirements for insurers under Solvency II* (February 2024)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/supervisory-statement/2024/ss124-february-2024-update.pdf
- **Accessed:** 2026-08-06
- **Fetched:** yes (supervisory statement, PDF, 8 pages; 1,701,124-byte PDF → 14,209 chars; **read
  in full**). Published 28 February 2024 as part of PS2/24 [R7]; **effective from 31 December 2024**.
- **Duplicate record, and why this one is canonical:** the governance stream numbered the same SS
  **R97b** but retrieved **the publication page only — the SS PDF was not retrieved**, and its
  record is explicitly "**[unverified] beyond this scope list**". R81b is the read document.
  **Cite R81b.**

---

## M. Regulatory reporting — the rulebook and the policy that made it

### R84. PRA Rulebook — **Reporting Part** (as at 05/08/2026, and future view as at 31/12/2026)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URLs:** https://www.prarulebook.co.uk/pra-rules/reporting/05-08-2026 (present view,
  989,845 bytes) ; https://www.prarulebook.co.uk/pra-rules/reporting/31-12-2026 (future view,
  1,071,104 bytes)
- **Accessed:** 2026-08-06
- **Fetched:** yes (**both views**, browser User-Agent; converted to text and **read in full**)
- **Note:** the date segment in the URL is the version identifier. The 31/12/2026 view adds the
  liquidity reporting Articles 51–54A and rules 2.5B(11A)–(11F), and **replaces MALIR 1–7 with
  MA.00.01, MA.00.02, MA.01.01, MA.02.01 and MA.03.01**. **Chapter 8 (National Specific Templates)
  is entirely `[Deleted]` at 31/12/2024.**

### R85. SS40/15 — *Solvency II: reporting and disclosure*
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.bankofengland.co.uk/prudential-regulation/publication/2015/solvency2-reporting-and-public-disclosure-options-provided-to-supervisory-authorities-ss
  (publication page; current version "published 15 November 2024, effective 31 December 2024,
  following PS15/24")
- **Accessed:** 2026-08-06
- **Fetched:** yes (publication page fetched this session; **the November 2024 PDF text was
  retrieved and read — 36,029 characters, chapters 1, 4, 8–17 and the update annex**). Chapters 2,
  3, 5, 6, 7 and 10 are `[Deleted]`.
- **Document defect recorded, not resolved:** the retrieved PDF **carries an unresolved placeholder
  header on page 1** — "This SS is effective from 31 December 2024 and is published as part of
  **PSX/24**. Please see https://www.bankofengland.co.uk/prudential-regulation/publication/2024/**XXXXX**"
  — while the annex records the November 2024 update as following PS15/24. Recorded as an observed
  defect in the published document.

### R86. PS3/24 — *Review of Solvency II: Reporting and disclosure phase 2 near-final*
- **Publisher:** Prudential Regulation Authority (Bank of England), published 29 February 2024
- **URL:** https://www.bankofengland.co.uk/prudential-regulation/publication/2024/february/review-of-solvency-ii-reporting-disclosure-phase-2-near-final-policy-statement
- **Accessed:** 2026-08-06
- **Fetched:** yes (**123,068 characters read**)
- **Status caveat carried forward:** the rules are described throughout as **near-final**; the final
  instruments are in PS15/24 [R6].
- **Conflict recorded, not resolved:** ¶¶4.68–4.70 state that S.13.01 and SR.22.02 (projection of
  future cash flows in the best estimate) "continue to be collected" — **contradicted by the final
  Rulebook** [R84]. The research file records the contradiction rather than picking a side.

### R87. PS15/25 and PS18/26 — the post-restatement reporting policy statements
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URLs:** PS15/25 (published 30 September 2025)
  https://www.bankofengland.co.uk/prudential-regulation/publication/2025/september/closing-liquidity-reporting-gaps-and-streamlining-standard-formula-reporting-policy-statement ;
  PS18/26 (published 29 July 2026)
  https://www.bankofengland.co.uk/prudential-regulation/publication/2026/july/solvency-uk-policy-statement
- **Doc type:** policy statements — **two documents, one entry**
- **Accessed:** 2026-08-06
- **Fetched:** yes (PS15/25 110,279 characters; PS18/26 66,992 characters)
- **Numbers deliberately not transcribed:** **the liquidity reporting thresholds in PS15/25 Chapter
  2** — which decide the "subset of larger UK Solvency II firms" in scope — were **not
  transcribed**; only the scope statement and the 30 September 2026 implementation date are
  recorded.
- **Duplicate record:** the own-funds stream separately numbered **PS18/26** as **R83d** (67,062
  chars; Chapters 1 and 3 read; **the amended Own Funds rule text in Appendix 3 was not
  retrieved**). **Cite R87.**

---

## N. The template library and the life instruction ("LOG") files

### R88. Bank of England — *Regulatory reporting – insurance sector* (the template and instruction library)
- **Publisher:** Bank of England / PRA
- **URL:** https://www.bankofengland.co.uk/prudential-regulation/regulatory-reporting/regulatory-reporting-insurance-sector
  (page "last updated 01 May 2026"; **71,625 characters of text retrieved**)
- **Accessed:** 2026-08-06
- **Fetched:** yes
- **Note:** this is where Reporting Part Chapters 9 and 10 actually resolve to — the Rulebook text
  says only "can be found **here**". **83 distinct instruction files** were verified, every one dated
  **15-11-2024**. The page also carries, as an archive section, the complete legacy NST inventory
  (NS.00–NS.13), **superseded** for reference dates from 31 December 2024.

### R88b. SoP6/24 — *Solvency II regulatory reporting waivers*
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.bankofengland.co.uk/prudential-regulation/publication/2024/february/solvency-ii-regulatory-reporting-waivers-sop
- **Accessed:** 2026-08-06
- **Fetched:** yes — **publication page only; the SoP PDF itself was NOT retrieved.** Verified from
  the page: first published 29 February 2024; current version published 15 November 2024, effective
  31 December 2024 (following PS15/24); a future version published 21 May 2026, effective
  31 December 2026 (following PS13/26).
- **Why it is cited:** the Reporting Part **no longer hard-codes size-based reporting exemptions** —
  Articles 10(1)(b), (c)(i) and (e) instead say a firm may be "exempted … in accordance with a
  direction given by the PRA under section 138A of FSMA" [R84]. **Nothing about the substance of any
  individual waiver is asserted**, because the SoP was not read.

### R89. Reporting Part Chapter 10 — **life technical provisions and obligations** instruction files (IR.12.01, IR.12.04, IR.14.01)
- **Publisher:** Prudential Regulation Authority (Bank of England), all dated 15-11-2024 (issued
  under PS15/24, [R6])
- **URLs:**
  - IR.12.01 Life technical provisions — https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/regulatory-reporting/insurance/ir1201-instructions-life-technical-provisions-15-11-2024
  - IR.12.04 Best estimate assumptions for life insurance risks — https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/regulatory-reporting/insurance/ir1204-instructions-best-estimate-assumptions-for-life-insurance-risks-15-11-2024
  - IR.14.01 Life obligations analysis — https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/regulatory-reporting/insurance/ir1401-instructions-life-obligations-analysis-15-11-2024
- **Accessed:** 2026-08-06
- **Fetched:** yes (**all three PDFs converted to text and read in full: 13,290 / 15,472 / 11,920
  characters**)
- **Retrieval limit carried forward:** the matching `…-template-…` **XLSX files exist at the same
  path pattern but were NOT retrieved.** Everything this directory says about these templates comes
  from the instruction files, not from the workbooks.

### R90. Reporting Part Chapter 10 — **with-profits and life revenue/capital** instruction files (IR.12.05, IR.12.06, IR.05.03, IR.05.10)
- **Publisher:** Prudential Regulation Authority (Bank of England), all dated 15-11-2024
- **URLs:**
  - IR.12.05 With-profits value of bonus — https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/regulatory-reporting/insurance/ir1205-instructions-with-profits-value-of-bonus-15-11-2024
  - IR.12.06 With-profits liabilities and assets — https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/regulatory-reporting/insurance/ir1206-instructions-with-profits-liabilities-and-assets-15-11-2024
  - IR.05.03 Life income and expenditure — https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/regulatory-reporting/insurance/ir0503-instructions-life-income-and-expenditure-15-11-2024
  - IR.05.10 Excess capital generation — https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/regulatory-reporting/insurance/ir0510-instructions-excess-capital-generation-15-11-2024
- **Accessed:** 2026-08-06
- **Fetched:** yes (**all four read in full: 3,046 / 6,677 / 12,238 / 11,201 characters**)

### R91. Reporting Part Chapter 10 — **matching adjustment** reporting instruction files (MALIR 1–7, IRR.22.02, IRR.22.03)
- **Publisher:** Prudential Regulation Authority (Bank of England), all dated 15-11-2024
- **URLs:**
  - MALIR (all seven templates in one log file) — https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/regulatory-reporting/insurance/malir-instructions-15-11-2024
  - IRR.22.02 Matching adjustment portfolio projection of future cash flows — https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/regulatory-reporting/insurance/irr2202-instructions-matching-adjustment-portfolio-projection-of-future-cash-flows-15-11-2024
  - IRR.22.03 Matching adjustment calculation — https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/regulatory-reporting/insurance/irr2203-instructions-matching-adjustment-calculation-15-11-2024
- **Accessed:** 2026-08-06
- **Fetched:** yes, with a **partial read recorded explicitly**: MALIR 48,344 characters — **MALIR 1,
  2 and 3 read in full; MALIR 4–7 headers and the appendix only**. IRR.22.02 (2,687 characters) and
  IRR.22.03 (5,430 characters) read in full.
- **Successor files not retrieved:** PS18/26 [R87] replaces MALIR 1–7 with MA.00.01 / MA.00.02 /
  MA.01.01 / MA.02.01 / MA.03.01 in XBRL from the 31 December 2026 reference date; **the replacement
  instruction files were not retrieved.**

---

## O. Governance — the system of governance, the actuarial function, the ORSA, audit and solvent exit

### R92. PRA Rulebook — **Conditions Governing Business Part** (as at 05/08/2026)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.prarulebook.co.uk/pra-rules/conditions-governing-business/05-08-2026
  (355,375 bytes)
- **Accessed:** 2026-08-06
- **Fetched:** yes (browser User-Agent; converted to text and read). Chapters 1A, 3, 4, 6 and
  11A–11D transcribed; the remainder read at chapter-inventory level.
- **Date-stamp note carried forward:** most of the substance carries **31/12/2024** (restated from
  the EU Delegated Regulation by PS15/24 [R6]); rule 3.2 carries **30/06/2024** (the MA reforms,
  PS10/24 [R5]); rule 6.1 and several older rules carry 01/01/2016.

### R93. PRA Rulebook — **Actuaries Part** (as at 05/08/2026)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.prarulebook.co.uk/pra-rules/actuaries/05-08-2026 (107,831 bytes)
- **Accessed:** 2026-08-06
- **Fetched:** yes

### R94. PRA Rulebook — **Insurance – Senior Management Functions Part** and **Insurance – Allocation of Responsibilities Part** (as at 05/08/2026)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URLs:** https://www.prarulebook.co.uk/pra-rules/insurance---senior-management-functions/05-08-2026
  (221,346 bytes) ;
  https://www.prarulebook.co.uk/pra-rules/insurance---allocation-of-responsibilities/05-08-2026
  (190,115 bytes)
- **Doc type:** **two Parts, one entry**
- **Accessed:** 2026-08-06
- **Fetched:** yes (both)

### R95. SS19/16 — *Solvency II: ORSA* (May 2026 version), with SS41/15
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URLs:** publication page
  https://www.bankofengland.co.uk/prudential-regulation/publication/2016/solvency2-orsa ;
  **May 2026 version** (effective 31 December 2026, published as part of PS13/26)
  https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/supervisory-statement/2026/ss1916-may-2026-update ;
  **November 2024 version** (effective 31 December 2024, PS15/24)
  https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/supervisory-statement/2024/ss1916-november-2024-update.pdf
- **Accessed:** 2026-08-06
- **Fetched:** yes (**both PDFs retrieved and read: November 2024 14,189 characters, May 2026 15,287
  characters**)
- **[unverified] carried forward:** the only material difference located between the two versions is
  scope — the **May 2026 text drops third-country branches**. **No paragraph-by-paragraph diff was
  performed [unverified beyond the scope sentence].**

### R95b. SS41/15 — *Solvency II: applying EIOPA's Set 2, System of Governance and ORSA Guidelines* (November 2024)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URLs:** publication page
  https://www.bankofengland.co.uk/prudential-regulation/publication/2015/solvency2-applying-eiopa-set2-system-of-governance-and-orsa-guidelines-ss ;
  PDF
  https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/supervisory-statement/2024/ss4115-november-2024-update.pdf
- **Accessed:** 2026-08-06
- **Fetched:** yes (**10,166 characters read in full**)
- **Why it matters:** this is the instrument that keeps the **EIOPA guidelines alive in the UK** —
  §2.2 expects firms to comply with all of the Set 2, System of Governance and ORSA Guidelines as at
  the end of the transition period, proportionately. The research file additionally records **§6.1 as
  a live defect** in the published document.

### R96. PRA Rulebook — **External Audit Part** (as at 05/08/2026)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.prarulebook.co.uk/pra-rules/external-audit/05-08-2026 (94,830 bytes)
- **Accessed:** 2026-08-06
- **Fetched:** yes. Rule 1.3 (definitions and the small-firm score formula) **last amended
  21/10/2025**.

### R96b. SS11/16 — *Solvency II: External audit of, and responsibilities of the governing body in relation to, the public disclosure requirement* (November 2024, updating June 2024)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** publication page
  https://www.bankofengland.co.uk/prudential-regulation/publication/2016/solvency2-external-audit-of-the-public-disclosure-requirement-ss
  ("Current version published on 15 November 2024. Effective from 31 December 2024. Following
  PS15/24")
- **Accessed:** 2026-08-06
- **Fetched:** yes (**PDF text 28,604 characters read**)

### R97. SS17/16 — *Solvency II: internal models – assessment, model change and the role of non-executive directors*
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URLs:** publication page
  https://www.bankofengland.co.uk/prudential-regulation/publication/2016/solvency2-internal-models-assessment-model-change-and-the-role-of-non-executive-directors-ss
  ("Current version published on 15 November 2024. Effective from 31 December 2024. Following
  PS15/24") ; **February 2024 version**
  https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/supervisory-statement/2024/ss1716-28-february-2024-update.pdf
- **Accessed:** 2026-08-06
- **Fetched:** **partial** — the publication page was retrieved and read; the **February 2024 PDF**
  was retrieved and read (45,926 characters) but is **stamped on every page "31 December 2024: This
  document has been superseded"**; **the current November 2024 PDF was NOT retrieved** (two guessed
  media URLs returned HTTP 404 and the page's PDF links are script-rendered).
- **Consequence carried forward, verbatim in substance:** "**Because the retrieved text is the
  superseded February 2024 version, paragraph numbers should be re-verified against the November
  2024 PDF before citation in a product document.**"

### R98. PRA Rulebook — **Preparations for Solvent Exit Part** (as at 05/08/2026), with SS11/24
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URLs:** https://www.prarulebook.co.uk/pra-rules/preparations-for-solvent-exit/05-08-2026
  (55,295 bytes) ; SS11/24 PDF
  https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/supervisory-statement/2024/ss1124-december-2024.pdf ;
  SS11/24 publication page
  https://www.bankofengland.co.uk/prudential-regulation/publication/2024/december/solvent-exit-planning-for-insurers-supervisory-statement
- **Accessed:** 2026-08-06
- **Fetched:** yes (**Rulebook Part read in full — it is only three chapters; SS11/24 PDF text
  35,169 characters read in part — contents, chapter 1 and the solvent exit analysis sections**)
- **Newest rule in the Solvency UK corpus:** every rule in the Part carries the effective date
  **30/06/2026**. A **UK-only** obligation with no Solvency II ancestor.
- **Document defect recorded, not resolved:** the PDF's cover page is headed "Supervisory statement |
  **SS11/24**" while its page 2 masthead reads "Supervisory statement | **SS20/24**"; the Bank's
  publication page confirms **SS11/24** is the supervisory statement and **PS20/24** the accompanying
  policy statement.

---

## P. The statutory accounts — UK GAAP

### R99. FRS 103 *Insurance Contracts* (September 2024 edition)
- **Publisher:** Financial Reporting Council
- **URL:** https://www.frc.org.uk/documents/7669/FRS_103_September_2024_rSi5poe.pdf
  (from the FRC library page at R101)
- **Accessed:** 2026-08-06
- **Fetched:** yes (PDF, 593,853 bytes → 171,294 chars text; **Sections 1–6, Appendix I Glossary,
  Appendix III and the Basis for Conclusions read directly**)
- **Retrieval limits carried forward:** **¶¶2.16 (tail), 2.17 and 2.18** — the alternative
  liability-adequacy measurement where the entity's own test fails the minimum requirements —
  **were read only in part**; and **Appendix II (Definition of an insurance contract) was not read
  at all**, so the significant-insurance-risk test that decides whether a UK product is an
  insurance or an investment contract rests on the Appendix I glossary definition and on HMRC's
  description [R18 LAM01100], not on ¶¶A2.1–A2.24. The drafted documents say so at the point of
  use.
- **This is the entry that reverses the U.S. framing:** ¶3.7 — **acquisition costs shall be
  deferred**, subject to three carve-outs; ¶3.9 — amortised over no longer than the recoverability
  period; **¶3.10 — acquisition costs shall not be deferred for with-profits funds**.

### R100. Implementation Guidance to accompany FRS 103 *Insurance Contracts* (September 2024)
- **Publisher:** Financial Reporting Council
- **URL:** https://www.frc.org.uk/documents/7663/Implementation_Guidance_to_accompany_FRS_103_Insurance_Contracts_September_2024_HvmQYVX.pdf
- **Doc type:** **non-mandatory implementation guidance** — "accompanies, but is not part of,
  FRS 103" and does not carry the authority of a standard [R101]
- **Accessed:** 2026-08-06
- **Fetched:** yes (PDF, 377,687 bytes → 81,231 chars; **page 1 text extraction failed**, all
  substantive pages extracted; Section 1 (IG1.1–IG1.13) and the long-term parts of Section 2 read)
- **Status:** it is nonetheless the **only published UK source that says how to compute the
  with-profits adjustments**. Where it and FRS 103 [R99] differ, R99 governs.

### R101. FRC library page — *FRS 103 Insurance Contracts*
- **Publisher:** Financial Reporting Council
- **URL:** https://www.frc.org.uk/library/standards-codes-policy/accounting-and-reporting/uk-accounting-standards/frs-103/
- **Doc type:** standard-setter web page (edition register plus policy statement)
- **Accessed:** 2026-08-06
- **Fetched:** yes (HTML)
- **Why it is a separate entry, not a link:** it is the **only place the FRC states its position on
  FRS 103 versus IFRS 17** — that FRS 103 is not aligned with IFRS 17, that conflicts between
  IFRS 17 and UK company law make alignment currently impossible, and that Schedule 3 to SI 2008/410
  "cannot be adapted".

### R102. FRS 102 *The Financial Reporting Standard applicable in the UK and Republic of Ireland* (September 2024 edition)
- **Publisher:** Financial Reporting Council
- **URL:** https://www.frc.org.uk/documents/7668/FRS_102_September_2024_tmKYWO6.pdf
- **Accessed:** 2026-08-06
- **Fetched:** yes (PDF, 2,829,292 bytes → 1,336,205 chars; **Section 1 scope, Section 7.10E,
  Section 29 Income Tax and the Section 29 Basis for Conclusions read; the rest indexed by search
  only**)
- **Companion record not carried:** the FRC library page for FRS 102 was also fetched, as **R102b**
  (Periodic Review 2024 effective 1 January 2026; "Adapted formats" amendment of 18 February 2026
  effective **1 January 2027**, arising from the replacement of IAS 1 by IFRS 18). It is an edition
  register and is not cited — see "Entries omitted as uncited".

---

## Q. Company law — the accounts framework and the distribution gate

### R103. Companies Act 2006, Part 15 — accounts and reports (s.395 read; s.396 by cross-reference)
- **Publisher:** legislation.gov.uk
- **URL:** https://www.legislation.gov.uk/ukpga/2006/46/section/395
  (Part 15 Chapter 4 also retrieved at
  https://www.legislation.gov.uk/ukpga/2006/46/part/15/chapter/4)
- **Accessed:** 2026-08-06
- **Fetched:** yes (**s.395 read in full**; text "up to date with all changes known to be in force on
  or before 05 August 2026"). **s.396 was reached by cross-reference, not read.**

### R104. Companies Act 2006, Part 23 — distributions (ss.830, 833A, 843)
- **Publisher:** legislation.gov.uk
- **URLs:** https://www.legislation.gov.uk/ukpga/2006/46/section/830 ;
  https://www.legislation.gov.uk/ukpga/2006/46/section/833A ;
  https://www.legislation.gov.uk/ukpga/2006/46/section/843
- **Accessed:** 2026-08-06
- **Fetched:** yes (**all three sections read in full**)
- **Why it is load-bearing:** s.833A **replaces** the accounts-based realised profit for s.830(2)
  purposes with **A − L − D** measured on the Solvency UK balance sheet — so for a Solvency-UK
  authorised UK life insurer **dividend capacity is driven by the prudential balance sheet, capped
  by accounts accumulated profits; it is not the accounts profit.** The research file records this
  as "the single most surprising fact in this stream".

### R105. The Large and Medium-sized Companies and Groups (Accounts and Reports) Regulations 2008 (SI 2008/410), **Schedule 3** — insurance companies: form and content of accounts
- **Publisher:** legislation.gov.uk
- **URL:** https://www.legislation.gov.uk/uksi/2008/410/schedule/3
- **Accessed:** 2026-08-06
- **Fetched:** yes (HTML, 300,310 bytes → 116,468 chars; **balance sheet format and notes, profit
  and loss account formats, and Part 2 Section E provisions rules read**)
- **Amendment history recorded, not resolved:** in para 52(3) the words "with due regard to
  generally accepted actuarial principles and" were **inserted**, and a following phrase omitted, by
  **SI 2019/145** (as amended by SI 2020/523) with effect for financial years beginning on or after
  IP completion day. The consequence is that the Schedule 3 text retrieved on 2026-08-06 **no longer
  contains the Solvency II reference** that the 2017 BEIS letter (R113, not cited) interprets. The
  tension is recorded in the research file, not resolved.

---

## R. IFRS 17 as adopted for use in the UK

### R106. UK Endorsement Board — *Endorsement Criteria Assessment: IFRS 17 Insurance Contracts* ("ECA — IFRS 17")
- **Publisher:** UK Endorsement Board
- **URL:** https://www.endorsement-board.uk/documents/666/ECA_-_IFRS_17.pdf
  (linked from the UKEB IFRS 17 project page at [R38])
- **Accessed:** 2026-08-06
- **Fetched:** yes (PDF, 1,840,287 bytes → 478,447 chars; **Section 2 "Description of IFRS 17" read
  in full, Section 3 priority issue D "With-profits: inherited estates" read, remainder indexed by
  search; one page failed text extraction**)
- **Status, and why it exists as an entry at all:** it is **the substitute for the paywalled
  standard**. Section 2 is a systematic description of IFRS 17 written by the UK adopting body,
  quoting IFRS 17 paragraph numbers. **All IFRS 17 mechanics in this directory come from R106**; the
  adoption facts come from [R38]. It is a **secondary description of a standard whose text was never
  read** — treat it accordingly.

### R107. IFRS Foundation — *IFRS 17 Insurance Contracts* standard page (paywall record)
- **Publisher:** IFRS Foundation
- **URL:** https://www.ifrs.org/issued-standards/list-of-standards/ifrs-17-insurance-contracts/
- **Accessed:** 2026-08-06
- **Fetched:** **partial.** Direct HTML extraction returned **only 41 characters** ("Amendments to
  IFRS 17 Insurance Contracts") — the page is client-rendered. A second retrieval through a
  markdown-converting fetcher succeeded and is the basis of the annotation.
- **Why it is recorded:** so that the library is **explicit rather than silently paraphrasing**. The
  page **does not provide the full text of IFRS 17 free of charge**; the standard is behind the IFRS
  Digital subscription or the IFRS Foundation shop. **No IFRS 17 paragraph text was read from this
  source.**

---

## S. Tax — the instruments on top of FA 2012 and the LAM

### R108. The Insurance Contracts (Tax) (Change in Accounting Standards) Regulations 2022 (SI 2022/1165)
- **Publisher:** legislation.gov.uk (HM Treasury statutory instrument)
- **URL:** https://www.legislation.gov.uk/uksi/2022/1165/made
- **Accessed:** 2026-08-06
- **Fetched:** yes (**regulations 1–8 read in full; regulations 9–12 read in part**)
- **Second-hand reading flagged:** **regulation 12** (the CTA09 s.320A-analogue bringing OCI amounts
  into account on derecognition of an insurance contract) was read **through [R18] LAM16060, not
  from the SI text.**

### R109. The Finance Act 2022, Part 2 of Schedule 5 (Insurance Contracts: Change in Accounting Standards) (Commencement and Savings Provision) Regulations 2022 (SI 2022/1164 (C. 90))
- **Publisher:** legislation.gov.uk (HM Treasury statutory instrument)
- **URL:** https://www.legislation.gov.uk/uksi/2022/1164/made
- **Accessed:** 2026-08-06
- **Fetched:** yes (**read in full** — the instrument is two regulations plus an explanatory note)

### R110. GOV.UK published tax rates — Corporation Tax and Income Tax
- **Publisher:** HM Government / HMRC (GOV.UK)
- **URLs:** https://www.gov.uk/corporation-tax-rates ; https://www.gov.uk/income-tax-rates
- **Accessed:** 2026-08-06
- **Fetched:** yes (both)
- **Why it exists:** so the two rates a UK life tax projection needs come **from a citable source
  rather than memory** — the LAM's worked examples are stated at 2018 rates [R18 LAM01160].
- **Caution carried forward:** **the gov.uk income-tax page does not state the tax year in the
  extracted text; treat "20%" as the rate published at the access date, not as a rate verified for a
  named tax year.**

---

## T. Product-specific treatment — investments, the INSPRU heritage, and unit matching

### R114. PRA Rulebook — **Investments Part** (as at 05/08/2026)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.prarulebook.co.uk/pra-rules/investments
- **Accessed:** 2026-08-06
- **Fetched:** yes (9,717 chars, local copy `s5-investments.txt`; browser-UA fetch — **plain fetchers
  get HTTP 403 from prarulebook.co.uk**). **Chapters 1–5 read in full; Chapter 6 (repackaged loans)
  skimmed.**
- **Future version not retrieved:** the Chapter 1 definitions are date-stamped 31/12/2024 with a
  **future version after 01/01/2027 — not retrieved.**

### R115. FCA Handbook — **INSPRU 1.2, *Mathematical reserves***
- **Publisher:** Financial Conduct Authority
- **URL:** https://www.handbook.fca.org.uk/handbook/INSPRU/1/2.html
- **Accessed:** 2026-08-06
- **Fetched:** yes (**two WebFetch passes; the application rule and rules 1.2.62 / 1.2.62A quoted
  back verbatim; the full chapter was NOT read**)
- **Status:** the **Solvency I** valuation rules — still live in the FCA Handbook but **expressly
  disapplied to Solvency II firms** by the application rule. Cited as the historical contrast to
  TP 3.1 [R1], never as live prudential law for a Solvency UK firm.

### R116. FCA Handbook — **INSPRU 1.3, *With-profits insurance capital component*** (**Deleted**)
- **Publisher:** Financial Conduct Authority
- **URL:** https://www.handbook.fca.org.uk/handbook/INSPRU/1/3.html
- **Accessed:** 2026-08-06
- **Fetched:** yes — **but the page carries no rule text.** It renders as "Deleted", with the note
  that INSPRU 1.3 "was last updated on **31/12/2015**".
- **Retrieval limit carried forward, and it is the point of the entry:** **no rule text of INSPRU
  1.3.40 (realistic value of liabilities), 1.3.190 (realistic current liabilities), or any WPBR /
  FPRL definition was retrieved, and none is asserted anywhere in this directory.** The chapter
  nevertheless remains operative in one live place: FRS 103's glossary defines *realistic value of
  liabilities* by reference to INSPRU 1.3.40 **as at 31 December 2015** [R99 BC49–BC50].

### R118. Milliman research report — *The benefits of Solvency II unit matching* (July 2018)
- **Publisher:** Milliman (Emma Hutchinson FIA FSAI, Fred Vosvenieks FIA CERA, Magnus Wilson FIA;
  with Paul Turnbull FIA, P Turnbull Financial Management)
- **URL:** **none asserted.** The research file records: "**not recorded in the local copy … No URL
  is asserted here — the retrieving fetch did not preserve one, and this library does not fabricate
  URLs. Re-derive and verify the URL before citing this entry in a published document.**" Local copy
  `s5-milliman-unitmatching.txt`.
- **Accessed:** 2026-08-06
- **Fetched:** yes (74,472 chars; **executive summary and sections 1–2 read in full; sections 3–4
  skimmed**)
- **Status:** **secondary** — a consultancy research report, not a rule or a regulator publication.
  Cited **only** as evidence of how the UK market reads Investments 4.3 [R114] and for the
  vocabulary of the unit / non-unit split, **never as authority for a rule.**
- **Conflict recorded, not resolved:** Milliman attributes the Solvency I surrender-value floor to
  **INSPRU 1.2.62A**, which the FCA Handbook renders as **guidance (G)**; the operative **rule** is
  **INSPRU 1.2.62 R** [R115]. The substantive point survives; the citation is one rule number out.

### R119. SS1/20 — *Solvency II: Prudent Person Principle* (November 2024, updating June 2024)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/supervisory-statement/2024/ss120-november-2024-update.pdf
  (landing page:
  https://www.bankofengland.co.uk/prudential-regulation/publication/2020/solvency-ii-prudent-person-principle-ss)
- **Accessed:** 2026-08-06
- **Fetched:** yes (47,081 chars via the browser-UA helper; **contents page and chapter 1 read in
  full, chapters 2–8 keyword-searched only**). Published 15 November 2024, effective 31 December
  2024.
- **Negative finding recorded deliberately:** a keyword search of the retrieved text returns **no
  occurrence of "unit-linked", "unit linked", "with-profits" or "ring-fenced"**. SS1/20 contains no
  unit-linked-specific or with-profits-specific guidance.

### R120. SS20/16 — *Solvency II: reinsurance – counterparty credit risk*
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.bankofengland.co.uk/prudential-regulation/publication/2016/solvency2-reinsurance-counterparty-credit-risk-ss
- **Accessed:** 2026-08-06
- **Fetched:** **partial — landing page only (2,306 chars); the PDF was NOT retrieved.**
- **[unverified] carried forward:** **"Everything else about SS20/16 is [unverified]" — no paragraph
  text was retrieved.** Only the publication history and addressee scope are verified.
- **Title discrepancy recorded, not resolved:** the landing page reads "counterparty **credit**
  risk"; SS18/16 ¶2.1 [R48] refers to the same document as "counterparty **default** risk".

---

## U. Frozen entries (R1–R38) cited by this directory

These predate this work, are **frozen**, and are already cited by the seven product documents. The
seven research files carry only a one-line "how it bears on this stream" note for each; the full
annotated entries — from which the metadata below is reproduced — live in
`uk/references/regulatory-and-actuarial-references.md`. **Access date 2026-08-03 for every entry in
this section**, per that file's header ("All URLs accessed 2026-08-03 unless noted otherwise").

### R1. PRA Rulebook — Technical Provisions Part
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.prarulebook.co.uk/pra-rules/technical-provisions
- **Accessed:** 2026-08-03 · **Fetched:** yes (read via browser; **prarulebook.co.uk blocks plain
  fetch with HTTP 403**). Re-read rule by rule for the technical-provisions stream on 2026-08-06 in
  the 05/08/2026 view; that re-read is what established that **Chapters 6 and 7 are `[Deleted]` as at
  30/06/2024**.

### R2. PRA Rulebook — Matching Adjustment Part
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.prarulebook.co.uk/pra-rules/matching-adjustment
- **Accessed:** 2026-08-03 · **Fetched:** yes (browser). Re-read for the discounting stream as at
  05/08/2026, Chapters 1–19 **including Chapters 14–19 for the MAIA, added 27/10/2025**.
- **[unverified] carried forward from the frozen entry:** the frozen annotation records **PS17/25
  itself as not fetched**; its existence is confirmed on the SS7/18 page [R8]. That flag stands.

### R3. PRA Rulebook — Transitional Measure on Technical Provisions Part
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.prarulebook.co.uk/pra-rules/transitional-measure-on-technical-provisions/31-12-2024
- **Accessed:** 2026-08-03 · **Fetched:** yes (browser, as-at 31/12/2024 view)
- **[unverified] carried forward:** the frozen annotation flags the characterisation of the legacy
  method, and "TMTP runs off fully by 2032" as **[unverified — per search summaries of PS2/24, R7]**.
  The discounting stream subsequently verified the 1 January 2032 end date from **Transitional
  Measures 10.3 and TMTP 2.3** and from SS17/15 ¶5.1 [R59]; the *frozen entry's own flag* is
  nonetheless reproduced here unchanged.

### R4. The Insurance and Reinsurance Undertakings (Prudential Requirements) (Risk Margin) Regulations 2023 (SI 2023/1346)
- **Publisher:** legislation.gov.uk (HM Treasury statutory instrument)
- **URL:** https://www.legislation.gov.uk/uksi/2023/1346/made
- **Accessed:** 2026-08-03 · **Fetched:** yes
- **Extraction limit carried forward:** like [R44], **this instrument prints the risk-margin formula
  as an image**, which comes back empty from text extraction.

### R5. PS10/24 — Review of Solvency II: Reform of the Matching Adjustment
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.bankofengland.co.uk/prudential-regulation/publication/2024/june/review-of-solvency-ii-reform-of-the-matching-adjustment-policy-statement
- **Accessed:** 2026-08-03 · **Fetched:** yes (browser; **site 403s plain fetch**)
- **[unverified] carried forward:** "Implementation 30 June 2024 with some requirements from
  31 December 2024 [unverified — per search summaries]".

### R6. PS15/24 — Review of Solvency II: Restatement of assimilated law
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.bankofengland.co.uk/prudential-regulation/publication/2024/november/review-of-solvency-ii-restatement-of-assimilated-law-policy-statement
- **Accessed:** 2026-08-03 · **Fetched:** yes (browser)
- **[unverified] carried forward:** "the specific location of contract-boundary rules within the
  restated Parts: unverified". **[R41] subsequently supplies that location (TPFR Chapter 3); the
  frozen flag is reproduced as written.**
- **Its Appendix 6 is [R42]** — the legal instrument, numbered separately.

### R7. PS2/24 — Review of Solvency II: Adapting to the UK insurance market
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.bankofengland.co.uk/prudential-regulation/publication/2024/february/review-of-solvency-ii-adapting-to-the-uk-insurance-market-policy-statement
- **Accessed:** 2026-08-03 · **Fetched:** no (URL from search results; not retrieved this session)
- **[unverified] carried forward:** the frozen entry flags its own publication date as
  "[unverified — date per search summaries]" and the accompanying Statement of Policy detail as
  [unverified]. Cited here only as the policy statement under which SS1/24 [R81b] was published;
  the 28 February 2024 date at [R81b] comes from the SS1/24 PDF read in full, not from this record.

### R8. SS7/18 — Solvency II: Matching adjustment (supervisory statement)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.bankofengland.co.uk/prudential-regulation/publication/2018/solvency-2-matching-adjustment-ss
- **Accessed:** 2026-08-03 · **Fetched:** yes (browser). Current version published 23 October 2025,
  effective 27 October 2025.
- **[unverified] carried forward:** "the PRA matching tests appear as Appendix 1 [unverified —
  appendix title seen only in search results]".

### R9. FCA Handbook COBS 20 — With-profits
- **Publisher:** Financial Conduct Authority
- **URL:** https://handbook.fca.org.uk/handbook/COBS/20/3.html (PPFM section; chapter at
  /handbook/COBS/20/)
- **Accessed:** 2026-08-03 · **Fetched:** yes (browser; **COBS 20.2 and 20.3 read directly**)
- **[unverified] carried forward:** "COBS 20.5 covers with-profits governance (WP committees)
  [unverified — section seen only in search results]".

### R10. FCA Handbook COBS 21.3 — Further rules for firms engaged in linked long-term insurance business (permitted links)
- **Publisher:** Financial Conduct Authority
- **URL:** https://handbook.fca.org.uk/handbook/COBS/21/3.html
- **Accessed:** 2026-08-03 · **Fetched:** yes (browser)
- **[unverified] carried forward:** "PS20/4 (March 2020) widened the regime for illiquid assets
  [unverified — from search results]".

### R11. FCA Handbook ICOBS — Insurance: Conduct of Business sourcebook
- **Publisher:** Financial Conduct Authority
- **URL:** https://handbook.fca.org.uk/handbook/ICOBS/1/1.html
- **Accessed:** 2026-08-03 · **Fetched:** yes (browser; **ICOBS 1.1 read**)
- **[unverified] carried forward:** the glossary definition of "pure protection contract" and the
  firm option to apply COBS to protection sales.

### R12. FCA Handbook PRIN 2A — The Consumer Duty
- **Publisher:** Financial Conduct Authority
- **URL:** https://handbook.fca.org.uk/handbook/PRIN/2A/1.html
- **Accessed:** 2026-08-03 · **Fetched:** yes (browser; **PRIN 2A.1 read**)
- **[unverified] carried forward:** the location of the price-and-value outcome (PRIN 2A.4), and
  "Effective for open products from 31 July 2023 [unverified]".

### R14. FSMA 2000 (Regulated Activities) Order 2001 (SI 2001/544), Schedule 1 Part II
- **Publisher:** legislation.gov.uk
- **URL:** https://www.legislation.gov.uk/uksi/2001/544/schedule/1
- **Accessed:** 2026-08-03 · **Fetched:** yes

### R15. Income Tax (Trading and Other Income) Act 2005, Part 4 Chapter 9 — Gains from contracts for life insurance etc.
- **Publisher:** legislation.gov.uk
- **URL:** https://www.legislation.gov.uk/ukpga/2005/5/part/4/chapter/9
- **Accessed:** 2026-08-03 · **Fetched:** yes (**top-slicing relief at ss.535–538: presence
  confirmed, full text not read**)
- **[unverified] carried forward:** the 5%-allowance mechanics as to their exact statutory
  expression.

### R16. HMRC Insurance Policyholder Taxation Manual (IPTM)
- **Publisher:** HM Revenue & Customs (GOV.UK)
- **URL:** https://www.gov.uk/hmrc-internal-manuals/insurance-policyholder-taxation-manual
- **Accessed:** 2026-08-03 · **Fetched:** yes (**landing / contents only**)
- **Status:** **secondary source** — use for mechanics, cite [R15] for law.
- **[unverified] carried forward:** specific subsection numbers, e.g. IPTM3500s for part surrenders.

### R17. Finance Act 2012, Part 2 — Insurance companies carrying on long-term business
- **Publisher:** legislation.gov.uk
- **URL:** https://www.legislation.gov.uk/ukpga/2012/14/part/2
- **Accessed:** 2026-08-03 · **Fetched:** yes

### R18. HMRC Life Assurance Manual (LAM)
- **Publisher:** HM Revenue & Customs (GOV.UK)
- **URL:** https://www.gov.uk/hmrc-internal-manuals/life-assurance
- **Accessed:** 2026-08-03 · **Fetched:** yes (**landing / contents**; individual LAM pages read
  ad hoc for the accounting-and-tax stream)
- **Status:** **secondary source** — use for how HMRC applies BLAGAB / I-E, cite [R17] for law.
- **Retrieval limit carried forward:** **HMRC's with-profits commercial-allocation guidance
  (LAM05070–LAM05090) was not read**, and the drafted documents say so at the point of use. The
  LAM's worked examples are stated at **2018 rates** (LAM01160), which is why [R110] exists.

### R22. Continuous Mortality Investigation — main page (role and access model)
- **Publisher:** Institute and Faculty of Actuaries / CMI Ltd
- **URL:** https://www.actuaries.org.uk/learn-and-develop/continuous-mortality-investigation
- **Accessed:** 2026-08-03 · **Fetched:** yes
- **Access restriction that governs every CMI citation in this library:** current tables and the
  Projections Model are **restricted to Authorised Users**. This library documents **table names and
  structure** from public sources and **cannot redistribute current qx values**; model mortality
  bases are **[std]** placeholders shaped like the named tables.

### R24. CMI "92" Series tables (AM92/AF92 family)
- **Publisher:** Institute and Faculty of Actuaries / CMI
- **URL:** https://www.actuaries.org.uk/learn-and-develop/continuous-mortality-investigation/cmi-mortality-and-morbidity-tables/92-series-tables
- **Accessed:** 2026-08-03 · **Fetched:** yes
- **[unverified] carried forward:** base experience 1991–94.

### R26. CMI "16" Series term assurance mortality and accelerated critical illness tables (IFoA blog announcement)
- **Publisher:** Institute and Faculty of Actuaries (blog; tables by the CMI Assurances Committee)
- **URL:** https://blog.actuaries.org.uk/cmi-new-16-series-term-assurance-mortality-and-accelerated-critical-illness-tables/
- **Accessed:** 2026-08-03 · **Fetched:** yes
- **[unverified] carried forward:** the table names TMNL16/TFNL16 — "from search summaries, not the
  fetched blog".

### R27. CMI briefing note — final "16" Series pension annuity in payment mortality tables
- **Publisher:** Institute and Faculty of Actuaries / CMI Annuities Committee
- **URL:** https://www.actuaries.org.uk/documents/final-16-series-pension-annuitant-mortality-tables-briefing-note-v01-2020-07-10
- **Accessed:** 2026-08-03 · **Fetched:** yes
- **[unverified] carried forward:** the "08" Series interim datasets, from search summaries.

### R30. CMI Mortality Projections Model CMI_2025 (announcement, with Working Paper 211)
- **Publisher:** Institute and Faculty of Actuaries / CMI
- **URL:** https://actuaries.org.uk/news-and-media-releases/news-articles/2026/mar/10-mar-26-cmi-model-shows-further-rise-in-cohort-life-expectancy/
- **Accessed:** 2026-08-03 · **Fetched:** yes
- **[unverified] carried forward:** that the long-term rate has no default recommendation. The model
  itself is **subscriber-restricted** [R22].

### R32. ONS National life tables (UK series)
- **Publisher:** Office for National Statistics
- **URL:** https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/lifeexpectancies/bulletins/nationallifetablesunitedkingdom/2021to2023
- **Accessed:** 2026-08-03 · **Fetched:** yes
- **[unverified] carried forward:** the 18 March 2025 publication date of the UK-level 2021–2023
  tables, from search results.
- **Why it matters:** because CMI tables are restricted [R22], **ONS tables are the only
  redistributable UK mortality source**, under the Open Government Licence.

### R33. FRC Technical Actuarial Standard TAS 100: General Actuarial Standards, v2.0
- **Publisher:** Financial Reporting Council
- **URL:** https://www.frc.org.uk/library/standards-codes-policy/actuarial/tas-100/
- **Accessed:** 2026-08-03 · **Fetched:** yes (**the standard's FRC page; the PDF was not read**)
- **[unverified] carried forward:** principle-level detail beyond Principle 5 (Models).

### R34. FRC Technical Actuarial Standard TAS 200: Insurance, v2.0
- **Publisher:** Financial Reporting Council
- **URL:** https://www.frc.org.uk/library/standards-codes-policy/actuarial/tas-200/
- **Accessed:** 2026-08-03 · **Fetched:** yes (**the standard's FRC page; the PDF was not read**)
- **[unverified] carried forward:** the content of the 2024 revision, from FRC/IFoA announcement
  summaries.

### R35. IFoA APS L1: Duties and Responsibilities of Life Assurance Actuaries, v4.0
- **Publisher:** Institute and Faculty of Actuaries
- **URL:** https://actuaries.org.uk/media/04ujhlcm/aps-l1-version-4-0.pdf
- **Accessed:** 2026-08-03 · **Fetched:** yes (**PDF downloaded and read**). Version 4.0, effective
  2 April 2024.

### R36. Proxy Modelling Working Party — "Consideration of the proxy modelling validation framework"
- **Publisher:** British Actuarial Journal (Cambridge University Press), Vol. 29, 2024
- **URL:** https://www.cambridge.org/core/journals/british-actuarial-journal/article/consideration-of-the-proxy-modelling-validation-framework/B499011B84ACEC53C627C15765D33F4B
- **Accessed:** 2026-08-03 · **Fetched:** yes (**abstract / landing page only**)
- **Status:** **secondary** — an actuarial working-party paper, not a rule. The proxy-modelling
  suggestions in `uk/regulatory/technical-notes.md` are **[std]** engineering suggestions, not
  restatements of this paper.

### R38. UK Endorsement Board — IFRS 17 Insurance Contracts (UK adoption)
- **Publisher:** UK Endorsement Board
- **URL:** https://www.endorsement-board.uk/projects/ifrs-17-insurance-contracts/
- **Accessed:** 2026-08-03 · **Fetched:** yes
- **Role here:** the **adoption facts only** — IFRS 17 adopted for UK use on 16 May 2022, effective
  1 January 2023. **All IFRS 17 mechanics come from [R106]**, because the standard text is
  paywalled [R107].

---

## Provenance note

The **citation ground truth** for everything in this directory is the seven research files:

| File | Owns | Carries |
|---|---|---|
| `uk/_research/solvency-uk-technical-provisions.md` | R39–R49 (R50–R52 unused) | The Valuation Part and the Article-75 balance sheet, the UK-GAAP derogation, the TPFR Part in full (contract boundaries, cash flows, expenses, management actions, FDB, policyholder behaviour, segmentation, HRGs, TP-as-a-whole, recoverables, the counterparty-default adjustment, proportionality, Annex 1), the risk margin, surplus funds at the TP boundary, and the revoked Delegated Regulation — plus "Extracted mechanics", "Model hooks", "Product applicability" and "Gaps and caveats" |
| `uk/_research/solvency-uk-discounting-and-transitionals.md` | R53–R60 (+R60b) | The risk-free curve and its publication, DLT and extrapolation, the matching adjustment in operative depth (permission, eligibility, fundamental spread, attestation, MAIA, breach), the volatility adjustment, TMTP and TMIR — plus the same four sections |
| `uk/_research/solvency-uk-scr-standard-formula.md` | R61–R73 (R74–R76 unused) | The SCR General Provisions and Standard Formula Parts, the scenario rules, life / health / market / counterparty / intangible / operational modules, the mass-lapse correction, USPs, LACTP and LACDT, simplifications, ring-fenced funds and MA portfolios in the SCR — plus the same four sections |
| `uk/_research/solvency-uk-own-funds-mcr-and-internal-models.md` | R77–R83 (+R78b, R79, R79b, R80b, R80c, R81b, R81c, R83b, R83c, R83d) | The own funds stack and tiering, the reconciliation reserve, EPIFP's removal, the MCR and the corridor, breach consequences, ring-fenced funds and surplus funds as capital, and the internal model Part in full — plus the same four sections |
| `uk/_research/solvency-uk-reporting-governance.md` | R84–R98 (+R88b, R88c, R95b, R96b, R97b, R97c) | The Reporting Part and its 99 template stems, the instruction-file library, the life and with-profits and MA templates cell by cell, the SFCR, Conditions Governing Business and the actuarial function, the ORSA, senior management functions, external audit, model governance, solvent exit — plus the same four sections |
| `uk/_research/uk-accounting-and-tax.md` | R99–R113 (+R102b) | FRS 103 and FRS 102, the Companies Act accounts choice and the s.833A distribution gate, SI 2008/410 Schedule 3 formats, IFRS 17 as adopted, the I-E computation and the FA 2012 overlay, the IFRS 17 tax transitionals, deferred tax on two balance sheets — plus the same four sections |
| `uk/_research/uk-product-regulatory-applicability.md` | R114–R120 (R121–R133 unused) | The per-product applicability matrix, the Investments Part and unit matching, the with-profits fund perimeter and its INSPRU heritage, negative technical provisions, contract boundaries product by product, and which templates each product triggers — plus the same four sections |

Those files record **which fact came from which document**, every `[unverified]` flag, every fetch
failure, and every number the research **deliberately did not transcribe**. The largest of those
deliberate omissions, restated so they are visible from this page:

- **The Annexes to the SCR – Standard Formula Part were never retrieved by any stream** [R73] — so
  Annex XVI's `r_s`, `x_e` and `H_h` and the geographical-diversification annex are unavailable, and
  the health catastrophe sub-modules cannot be computed from this library's material. The SCR stream
  additionally recorded the **numbered line-of-business list** as un-retrieved with them; that part
  of its record conflicts with [R41], where **TPFR Annex 1 Parts A–E (lines of business 1–36) was
  read in full**. The conflict is recorded at R73 in Section H above, not resolved.
- **No PRA-published technical information value of any kind is stated** — no risk-free rate,
  fundamental spread, volatility adjustment, symmetric adjustment, ultimate forward rate,
  convergence parameter or credit risk adjustment [R54][R55][R56].
- **The counterparty-default probability-of-default table (`3E12`), the loss-given-default
  definitions (`3E4`–`3E11`), the concentration aggregation formula (`3D27`, `3D28`) and the
  ECAI-to-credit-quality-step mapping tables were not transcribed** [R62][R72].
- **SoP4/24's quantitative capital add-on significance thresholds were not retrieved** [R69], and
  the SoP11/24 PDF was not fetched [R70].
- **The MCR Chapter 6 non-life segment factor table is not transcribed** beyond the one
  life-adjacent row [R78].
- **No COBS 20 target range, market value reduction bound or required percentage is given**, and no
  IFRS 17 measurement mechanic is restated from the standard itself [R106][R107].

Where this file, `uk/regulatory/statutory-accounting-and-capital.md` or
`uk/regulatory/technical-notes.md` and a research file disagree, **the research file governs** — it
is the provenance record. Where a research file and the frozen
`uk/references/regulatory-and-actuarial-references.md` disagree on an R1–R38 annotation, the
disagreement is **recorded rather than silently resolved** (see R2, R3 and R6 in Section U above).

---

## Standardizations and unverified items

Values marked **[std]** in `uk/regulatory/technical-notes.md` are **standardizations introduced at
drafting for the reference implementation and are attributable to no source.** They are, in order of
appearance:

1. The **precision convention** — six decimal places on cash flows and best estimates, four on SCR
   sub-modules, aggregation computed from the rounded sub-module figures.
2. The **evaluation order of the contract-boundary decision procedure** — the rules state the limbs
   but no order.
3. The **coded gate for when a stochastic method becomes compulsory** — TPFR 19.4–19.5 state the
   obligation but no test.
4. The **entire parameter set of the three-year term assurance worked example** (sum assured,
   premium, expenses, `q`, the flat 4% rate, zero expense inflation) and every figure derived from
   it, including the `SCR(0) = 209.6848` used in the run-off illustration.
5. The **drivers approach to the risk-margin `SCR(t)` run-off**, and the **expected-sum-assured-in-force
   driver** used in the worked example — no rule sanctions either; TPFR 27.4 is the only gate.
6. The **drivers approach applied to the whole SCR** in the projection section.
7. The **additional assumptions of the SCR worked example** — assets of 500 attracting no market or
   counterparty charge, flat earned premium, no deferred tax, no reinsurance / FDB / RFF / MA
   portfolio, and the reading of "the best estimate of the corresponding obligations" in `CAR` as
   the death-benefit obligations.
8. The **balance-sheet lines of the worked example** shown as [std] in its table (assets 500.000000;
   other liabilities 0.000000).
9. The **four-layer architecture** (product models → valuation layer → capital layer → reporting and
   ledger layer) and its one-directional dependency rule — an architectural suggestion, not a rule.
10. The **validation tolerances** — exact equality for identities true by construction, a stated
    relative tolerance otherwise; and the **0.5% of SCR proxy-error tolerance**, "chosen only as a
    starting point for calibration, since no source states one".

Each carries its one-line rationale at the point of use. A **[std]** is never a substitute for a
number that could have been looked up: where a number exists in a retrieved document it carries a
[REG-R#], and where the research recorded that it was not retrieved, the drafted documents say so
at the point of use rather than standardising a value.

Values marked **[unverified]** were carried forward from the research files unchanged; **none was
upgraded during drafting.** The flags that travel furthest are worth naming: the **line-of-business
mapping of the seven library products** (Annex 1 was read in full [R41] but does not name products,
and **no retrieved document states the mapping**); **everything about SS18/16 beyond one
sentence** [R48]; **everything about SS20/16
beyond its publication history** [R120]; the **USD and CAD last liquid points** [R56]; **SS17/16's
paragraph numbers**, which come from a print stamped "superseded" [R97]; **Transitional Measures 4.1
grandfathering into Tier 1** [R57][R77]; and the frozen R1–R38 flags reproduced in Section U.
