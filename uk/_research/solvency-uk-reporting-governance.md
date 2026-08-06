# Solvency UK Regulatory Reporting, Disclosure and Governance — research notes

**Stream:** Regulatory reporting, disclosure and governance (Solvency UK)
**Access date for every citation below:** 2026-08-06
**Status:** research notes, not yet merged into
`uk/references/regulatory-and-actuarial-references.md`

---

## Scope and numbering note

This stream owns reference block **R84–R98**. Entries **R1–R38** live in
`uk/references/regulatory-and-actuarial-references.md`, are **frozen**, and are already cited
by the seven UK product documents; nothing below renumbers, restates or duplicates them.
Existing entries that bear on reporting and governance are listed in the next section with a
one-line note on how they bite, and are cited as `[R#]` throughout without being re-created.
New entries are numbered sequentially from R84. **R84–R98 are all used; no numbers in the
block are left spare.** Where a secondary document was read under the same heading it is
given a lettered sub-id (R88b, R88c, …) following the convention already used in
`us/_research/statutory-accounting.md` (R74b) rather than consuming a new number.

**What this stream owns:** the Reporting Part of the PRA Rulebook (which templates exist, who
must file them, at what frequency and by what deadline), the Solvency and Financial Condition
Report (SFCR) and its external audit, the Conditions Governing Business Part (system of
governance, the four key functions, the actuarial function, ORSA), the Actuaries Part and the
Chief Actuary / With-Profits Actuary senior management functions, the reporting-and-model
governance supervisory statements, and solvent exit planning.

**Deliberately left to other streams.** The *calculation* of technical provisions, best
estimate and matching adjustment is stream 1; SCR / MCR / own funds is stream 2; accounting
and tax is stream 4; per-product application is stream 5. Where a template requires a TP or
SCR number, this file records **what the template demands and at what granularity**, and
points at the owning stream for how the number is produced. The professional layer — FRC
TAS 100 [R33], TAS 200 [R34], IFoA APS L1 [R35] — is cited, not re-created.

**Six retrieval facts that change how this material must be documented**

1. **The Regular Supervisory Report (RSR) no longer exists in the UK.** The Reporting Part as
   read on 2026-08-06 contains **zero occurrences of "regular supervisory report"** in either
   the present (05/08/2026) or future (31/12/2026) view [R84]. PS3/24 records that CP12/23
   proposed "removal of the requirement for all Solvency II firms, including third country
   branches, to submit the RSR", and that "**the requirement to submit the RSR ceased on 31
   December 2023**" following HM Treasury's Risk Margin SI [R86 ¶1.8, ¶1.30] — i.e. the RSR
   was killed a year before the rest of the reporting reforms bit. Any UK reporting
   documentation modelled on the EU three-report architecture (QRTs + RSR + SFCR) is wrong:
   Solvency UK has **QRTs + ORSA report + SFCR**, plus narrative packs attached to specific
   templates (QMC.01, AoC.01, MALIR).
2. **The National Specific Templates (NSTs) no longer exist as a separate category.**
   Reporting Part **Chapter 8 "National Specific Templates" is entirely `[Deleted]` as at
   31/12/2024** (rules 8.0 to 8.13 all deleted) [R84]. The surviving UK-specific life
   templates were renumbered into the main **IR.xx.yy.zz** series and are now required by
   **Article 21A of Chapter 2A** ("Additional Annual and Quarterly Quantitative Templates for
   Individual Firms") and by Article 9(1)(k) [R84]. PS3/24 also **deleted SS6/18 "National
   Specific Templates LOG files"** and **SS36/15 "Solvency II: life insurance product
   reporting codes"** [R86 ¶1.1]; the life product code list survives as the **Appendix to the
   IR.14.01 instruction file** [R89].
3. **Every EU "S." / "SR." / "NS." template code has been re-lettered.** Solvency UK codes are
   `IR.xx.yy.zz` (entity/branch/group), `IRR.xx.yy.zz` (per ring-fenced fund, matching
   adjustment portfolio or remaining part), plus the named returns `MALIR 1–7`, `AoC.01` and
   `QMC.01` [R84]. A drafter must not carry EU template numbers into UK text.
4. **There is no life best-estimate cash-flow-projection template in Solvency UK.** The EU
   S.13.01 (projection of future cash flows, best estimate — life) has **no IR counterpart**:
   `IR.13.01` appears nowhere in the Reporting Part [R84] and no `ir1301` instruction file
   exists in the PRA's published instruction library [R88]. This directly contradicts PS3/24
   ¶4.70, which states that "S.13.01 and SR.22.02 will continue to be collected" [R86]. The
   only surviving prospective liability cash-flow requirements are **IRR.22.02** (annual, MA
   portfolios, by year of due payment) [R91] and **MALIR 3** (annual, MA portfolios, **monthly
   buckets to month 600**) [R91]. See "Gaps and caveats".
5. **The Rulebook is a dated-view system and three views are live at once.** The 05/08/2026
   "present" view, a 30/09/2026 future view (liquidity reporting, PS15/25) and a 31/12/2026
   future view (PS18/26 post-implementation amendments) all differ [R84][R87]. Every rule
   citation in downstream documents must carry the as-of date it was read.
6. **prarulebook.co.uk and bankofengland.co.uk return HTTP 403 to plain fetchers.** All
   Rulebook and Bank of England retrievals below were made with a browser User-Agent and
   returned HTTP 200; each URL cited was actually requested this session and its status
   observed. No URL on this page is fabricated.

---

## Existing entries (R1–R38) that bear on this stream

| R# | Short title | How it bears on reporting, disclosure and governance |
|----|-------------|------------------------------------------------------|
| R1 | PRA Rulebook — Technical Provisions Part | Supplies the numbers that templates IR.12.01 / IRR.12.01 report and that SFCR section D.2 describes; Conditions Governing Business 6.2(1) makes the actuarial function responsible for consistency with this Part [R92]. |
| R2 | PRA Rulebook — Matching Adjustment Part | Generates the whole MALIR return and templates IRR.22.02 / IRR.22.03; the MA attestation is a **mandatory SFCR disclosure** under Reporting 3.4(1)(c) [R84]. |
| R3 | PRA Rulebook — TMTP Part | TMTP components are reported cell-by-cell in IR.12.01 rows R0140–R0180 (Ar, Br, Cr, Wr, Tr) [R89], and its run-off is a line of the excess-capital-generation template IR.05.10 R0070 [R90]. |
| R4 | Risk Margin Regulations 2023 (SI 2023/1346) | The instrument whose making also carried the **abolition of the RSR from 31 December 2023** [R86 ¶1.30]. Risk-margin run-off is IR.05.10 rows R0050/R0060 [R90]. |
| R5 | PS10/24 — Reform of the Matching Adjustment | Introduced the MA asset and liability information return (MALIR) and the MA attestation disclosure; also produced the June 2024 version of SS11/16 [R96]. |
| R6 | PS15/24 — Restatement of assimilated law | **The instrument of this stream.** It restated the EU reporting ITS into Reporting Part Chapters 2A/3A/9/10, and published the November 2024 versions of SS40/15, SS41/15, SS19/16, SS11/16 and SS17/16 — every supervisory statement cited below. |
| R7 | PS2/24 — Adapting to the UK insurance market | Companion policy statement to PS3/24 [R86]; PS3/24 must be read with it (PS3/24 ¶1.1). |
| R8 | SS7/18 — Matching adjustment | MALIR 2 requires each asset to be tagged to **"Component A/B/C of the MAP … as set out in chapter 4 of SS7/18"**, and reinsurance cash flows net of CDA "as per the expectation set out in chapter 2 of SS7/18" [R91]. |
| R9 | FCA Handbook COBS 20 — With-profits | IR.12.05 requires reversionary bonus value to be "calculated in accordance with **COBS 20.2.17R** and any subsequent COBS rules" [R90] — a direct FCA-into-PRA-template cross-reference. |
| R12 | FCA PRIN 2A — Consumer Duty | IR.12.06 row R0080 requires the future cost of **non-contractual commitments** including "liabilities arising from the regulatory duty for firms to treat customers fairly" [R90]. |
| R22–R31 | CMI tables and projection model | IR.12.04 column C0080 requires the **named underlying table** (e.g. "AM92", "AM92 adjusted") and, for annuitant mortality, the CMI projection basis in CMI notation, "e.g. CMI_2018_G [L%; S=Sκ; A=A%]" [R89]. |
| R33 / R34 | FRC TAS 100 / TAS 200 | The professional quality bar for the actuarial function report required by Conditions Governing Business 6.9 [R92] and for the assumption documentation required by 11C.3 [R92]. |
| R35 | IFoA APS L1 | Defines the professional duties of the **Chief Actuary (SMF20)** and **With-Profits Actuary (SMF20a)** whose Rulebook functions are at R94/R95. |
| R36 / R37 | Proxy Modelling / Model Risk working parties | The practitioner literature behind the validation expectations in SS17/16 chapter 7 [R97] and Conditions Governing Business 11B [R92]. |
| R38 | UK-adopted IFRS 17 | IR.05.03 is reported "using financial accounting conventions" on the basis of the accounting standard declared at IR.01.02 row R0120 [R90] — so the IFRS 17 result feeds a Solvency UK template. |

---

## New entries

All URLs below were requested on **2026-08-06** with a browser User-Agent and returned HTTP
200 unless noted. PRA Rulebook Parts were read in the **05/08/2026 "present" view** (and, for
the Reporting Part, additionally in the **31/12/2026 "future" view**); that date segment is
part of the URL and is the version identifier.

### A. The Solvency UK reporting rulebook and the policy that made it

#### R84. PRA Rulebook — **Reporting Part** (as at 05/08/2026, and future view as at 31/12/2026)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URLs:** https://www.prarulebook.co.uk/pra-rules/reporting/05-08-2026 (present view, 989,845 bytes) ;
  https://www.prarulebook.co.uk/pra-rules/reporting/31-12-2026 (future view, 1,071,104 bytes)
- **Doc type:** rulebook part. **Accessed:** 2026-08-06. **fetched_ok:** yes (both views, browser User-Agent; converted to text and read in full)
- **Annotation:** The single most load-bearing source in this stream — the UK counterpart of
  the NAIC Annual Statement Instructions. Structure verified: **Chapter 1** application and
  definitions; **Chapter 2** reporting to the PRA (2.1–2.5B: the inventory of what must be
  submitted and every deadline; 2.6–2.12 and 2.14 all `[Deleted]`; 2.13 electronic format);
  **Chapter 2A** "Reporting to the PRA: Reports and Templates" — Articles 1–4A general,
  Articles 5–21A solo, Articles 22–36 groups, Articles 37–50 third-country branches;
  **Chapter 3** public disclosure: SFCR (3.1–3.10); **Chapter 3A** "Solvency and Financial
  Condition Report: Report and Templates" — Articles 1A (SFCR structure), 2–3B (format,
  materiality, means of disclosure), 4 (solo disclosure templates), 5 (group), 6–8;
  **Chapter 4** permitted non-disclosure; **Chapter 5** updates and major developments;
  **Chapter 6** policy and governing-body approval of the SFCR; **Chapter 7** Lloyd's;
  **Chapter 8 "National Specific Templates" — entirely `[Deleted]` at 31/12/2024**;
  **Chapter 9** the template inventory (rules 9.1 onward, each pointing to an externally
  hosted template file); **Chapter 10** the instruction ("LOG") files, likewise externally
  hosted. Verified that the Chapter 9 inventory contains **99 distinct template code stems**
  (IR.01.01 … IR.36.04 plus the IRR.xx series) — reproduced in "Extracted mechanics" §1.
  Verified that **no IR.13.01 exists**. Verified that the **only** narrative reports required
  are the ORSA report, the third-country-branch resolution report, and the qualitative packs
  supporting QMC.01, AoC.01 and MALIR (rule 2.5A(2)). The 31/12/2026 view adds the liquidity
  reporting Articles 51–54A and rules 2.5B(11A)–(11F), and replaces MALIR 1–7 with templates
  MA.00.01, MA.00.02, MA.01.01, MA.02.01 and MA.03.01 (Article 18A as amended).
- **Products:** all (TA, CI, IP, WOL, WP, ULB, PA).

#### R85. SS40/15 — *Solvency II: reporting and disclosure*
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.bankofengland.co.uk/prudential-regulation/publication/2015/solvency2-reporting-and-public-disclosure-options-provided-to-supervisory-authorities-ss (publication page; current version "published 15 November 2024, effective 31 December 2024, following PS15/24")
- **Doc type:** supervisory statement. **Accessed:** 2026-08-06. **fetched_ok:** yes (publication page fetched this session; the November 2024 PDF text was retrieved and read — 36,029 characters, chapters 1, 4, 8–17 and the update annex)
- **Annotation:** The expectations layer on the Reporting Part. Verified content: chapters 2,
  3, 5, 6, 7 and 10 are `[Deleted]`; the live chapters are 4 (accident vs underwriting year
  election), 8, 9, 11 (group reporting without consolidated financial statements), **12
  (information that should be disclosed in the SFCR)**, 13 (pre-defined events), **14 (firms'
  processes for public disclosure)**, **15 (firms' processes for reporting)**, 16 (quantitative
  reporting and validations) and 17 (SFCR dispensation). §12.10 is the only SFCR technical
  provisions expectation: firms "should describe the significant simplified methods used to
  calculate technical provisions, including those used for calculating the risk margin".
  §15.2 requires **annual QRTs to be approved by the governing body before submission**; §15.3
  requires **quarterly QRTs to be approved by the management body or by persons who effectively
  run the firm**. §16.1–16.2 require firms to follow the Bank's published **data point model**
  and **validation rules**. §13.1 requires immediate written notification of "pre-defined
  events". **Caveat:** the PDF text retrieved carries an unresolved placeholder header on
  page 1 — "This SS is effective from 31 December 2024 and is published as part of **PSX/24**.
  Please see https://www.bankofengland.co.uk/prudential-regulation/publication/2024/**XXXXX**"
  — while the annex records the November 2024 update as following PS15/24. Recorded as an
  observed defect in the published document, not resolved here.
- **Products:** all.

#### R86. PS3/24 — *Review of Solvency II: Reporting and disclosure phase 2 near-final*
- **Publisher:** Prudential Regulation Authority (Bank of England), published 29 February 2024
- **URL:** https://www.bankofengland.co.uk/prudential-regulation/publication/2024/february/review-of-solvency-ii-reporting-disclosure-phase-2-near-final-policy-statement
- **Doc type:** policy statement. **Accessed:** 2026-08-06. **fetched_ok:** yes (123,068 characters read)
- **Annotation:** The policy record of how the UK reporting package was cut down, and the only
  place that explains *why* particular templates survive. Verified: it responds to CP14/22
  (reporting phase 2) and CP12/23 chapter 7. Verified changes: **permanent deletion of a number
  of QRTs, associated disclosure templates and relevant NSTs**; frequency reductions from
  quarterly to semi-annual or annual; consolidation of overseas-activity and SCR reporting;
  activity-based reporting thresholds; **three new templates on excess capital generation,
  cyber underwriting risk and non-life product obligations** (of which the non-life product
  obligations template S.14.02 was **not implemented** — ¶4.4); deletion of SS36/15, SS6/18 and
  SS11/15; a new statement of policy on reporting waivers [R88b]; and **removal of the RSR for
  all firms including third-country branches** (¶1.8). **Implementation (¶1.30):** "This policy
  will come into effect on Tuesday 31st December 2024 for triennial, annual, semi-annual and
  quarterly requirements with a reporting or disclosure reference date as of 31 December 2024
  and onwards. By exception, **the requirement to submit the RSR ceased on 31 December 2023**
  following the publication by HMT of the [Risk Margin] Regulations 2023 Statutory Instrument."
  Life-relevant feedback verified: ¶4.10–4.17 excess capital generation (proposed as NS.14 for
  life firms writing **non-unit-linked premiums exceeding £1 billion annually**, solo only, not
  groups; the PRA declined to fold it into the ORSA because ORSAs "are submitted by firms
  throughout the calendar year, data may be received from firms many months apart, compromising
  comparability"); ¶4.35–4.37 life obligations analysis (S.14 retained **because "there is no
  product split in other Solvency II templates (eg S.05 or S.12.01)"** and "the product codes in
  S.14 are at a granular level"); ¶4.68–4.70 projection of future cash flows in the best estimate
  (S.13.01 and SR.22.02 stated to "continue to be collected" — **contradicted by the final
  Rulebook, see Gaps**); ¶4.74–4.77 the new S/SR.25.04, 25.05 and 25.06 SCR templates. The rules
  are described throughout as **near-final**; the final instruments are in PS15/24 [R6].
- **Products:** all.

#### R87. PS15/25 and PS18/26 — the post-restatement reporting policy statements
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URLs:** PS15/25 (published 30 September 2025) https://www.bankofengland.co.uk/prudential-regulation/publication/2025/september/closing-liquidity-reporting-gaps-and-streamlining-standard-formula-reporting-policy-statement ;
  PS18/26 (published 29 July 2026) https://www.bankofengland.co.uk/prudential-regulation/publication/2026/july/solvency-uk-policy-statement
- **Doc type:** policy statements (two documents, one entry). **Accessed:** 2026-08-06. **fetched_ok:** yes (PS15/25 110,279 characters; PS18/26 66,992 characters)
- **Annotation:** The two changes to Solvency UK reporting since the 31/12/2024 restatement.
  **PS15/25** — *Closing liquidity reporting gaps and streamlining Standard Formula reporting*,
  responding to CP19/24. Verified: four new liquidity templates — a **monthly** "cash flow
  mismatch" template; a **monthly** "cash flow mismatch (short form)" with a shorter remittance
  period, escalable to **every business day** in firm-specific or market liquidity stress; an
  **annual** "committed facilities" template; and a **quarterly** "liquidity market risk
  sensitivities" template (¶1.10). Implementation date **30 September 2026** (¶1.20), applying
  only to "a subset of larger UK Solvency II firms", **not** to Lloyd's, third-country branches
  or non-Solvency II firms (¶1.7). Also removed the expectation that life internal-model firms
  submit the annual **SF.01** standard-formula SCR template — effective on publication, so "firms
  in scope … will not be expected to submit an SF.01 report to the PRA from 31 December 2025
  inclusive", and the year-end 2024 SF.01 is also not expected (¶1.22). **PS18/26** — *Solvency
  UK: Post-implementation reporting and disclosure amendments and Own Funds permissions update*,
  responding to CP22/25 and CP4/26 Proposal 1. Verified: implementation "for reporting reference
  dates on or after Thursday 31 December 2026" (¶1.31–1.32); the **MALIR return moves from Excel
  to XBRL** with a restructured template set including a new MA.01.01 (¶1.11); NACE 2.1 codes
  permitted from the 31 December 2026 reference date and mandatory later (¶2.1 changes list);
  **IR.14.01's "claims paid" definition is amended to exclude claims management expenses**,
  because "claims management expenses for life insurance business are a very small part of total
  expenses" and firm practice was inconsistent (¶2.41); cell-label standardisation across
  IR.02.01, IR.05.03, IRR.12.01, **IR.12.05, IR.12.06**, IR.25.04, IR.25.05 and the IR.26 series
  to "Z0020 Ring-fenced fund, matching adjustment portfolio or remaining part" and "Z0030
  Fund/Portfolio number" (¶2.43); and **deletion of SS37/15** (internal model reporting codes)
  (¶1.7).
- **Products:** all; the excess-capital-generation and MALIR changes bite hardest on PA and WP.

### B. The template library and how to read it

#### R88. Bank of England — *Regulatory reporting – insurance sector* (the template and instruction library)
- **Publisher:** Bank of England / PRA
- **URL:** https://www.bankofengland.co.uk/prudential-regulation/regulatory-reporting/regulatory-reporting-insurance-sector (page "last updated 01 May 2026"; 71,625 characters of text retrieved)
- **Doc type:** reporting hub page with linked template (XLSX) and instruction (PDF) files. **Accessed:** 2026-08-06. **fetched_ok:** yes
- **Annotation:** Where Reporting Part Chapters 9 and 10 actually resolve to. The Rulebook text
  says only "The following IR.xx.yy templates can be found **here**" and "Section IR.xx.yy
  instructions can be found **here**" [R84]; the files themselves live under
  `https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/regulatory-reporting/insurance/<code>-instructions-<title>-15-11-2024`
  (and `…-template-…` for the XLSX). Verified: **83 distinct instruction files**, every one
  dated **15-11-2024** (i.e. all issued under PS15/24 [R6]); their slugs are enumerated in
  "Extracted mechanics" §2. Verified page statements: "**Solvency UK now applies for all
  insurance regulatory reporting with reporting reference dates of 31 December 2024 and
  later**"; Bank of England Insurance **Taxonomy v2.0.1** (10 October 2024) for the 31 December
  2024 reference date, **v2.0.2** (2 October 2025) effective 1 January 2026 for reference dates
  on or after 31 December 2025, **v2.1.0** (16 December 2025) adding four liquidity entry
  points, and a **v2.2.0 public working draft** (21 April 2026) implementing CP22/25 and
  CP4/26. The page also still carries, as an archive section, the **complete legacy NST
  inventory**: NS.00 Basic information, **NS.01 With-profits value of bonus**, **NS.02
  With-profits assets and liabilities**, NS.03 Material pooling arrangements, NS.04 Assessable
  mutuals, **NS.05 Revenue account life**, **NS.06 Business model analysis (life)**, NS.07
  Business model analysis non-life, NS.08 Business model analysis – financial guarantee
  insurers, **NS.09 Best estimate assumptions for life insurance risks**, NS.10 Projection of
  future cash flows (best estimate – non-life: liability claim types), NS.11 Non-life claim
  development information, NS.12 and NS.13 the Society of Lloyd's SCR and MCR. This inventory
  is **superseded** for reference dates from 31 December 2024 but is the key to reading
  pre-2025 UK material.
- **Also fetched (same date):**
  - **R88b. SoP6/24 — *Solvency II regulatory reporting waivers*.** Publisher: PRA. URL:
    https://www.bankofengland.co.uk/prudential-regulation/publication/2024/february/solvency-ii-regulatory-reporting-waivers-sop . fetched_ok: yes (**publication page only; the SoP PDF itself was not retrieved**). Verified from the page: first published 29 February 2024; **current version published 15 November 2024, effective 31 December 2024** (following PS15/24); a **future version published 21 May 2026, effective 31 December 2026** (following PS13/26). The SoP "lists the reporting covered by certain waivers and modifications by consents; and explains the steps a firm must take to apply". This matters because the Reporting Part no longer hard-codes size-based reporting exemptions: Articles 10(1)(b), (c)(i) and (e) instead say a firm may be "**exempted … in accordance with a direction given by the PRA under section 138A of FSMA**" [R84].
  - **R88c. PRA *Solvency UK regulatory reporting – Questions & Answers*, October 2025.**
    Publisher: PRA. URL: https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/regulatory-reporting/insurance/2025/october/solvency-uk-regulatory-reporting-reforms-qa-october-2025.pdf . fetched_ok: yes (20 pages, 33,272 characters). Explicitly **"not PRA's reporting policy"** (cover note). Verified operationally useful answers: returns are submitted through the **Bank of England Electronic Data Submission (BEEDS) portal** (A9); the **DIS (disclosure) templates are part of the taxonomy but are not submitted through BEEDS** — "It is the responsibility of the firm to publish its SFCR" (A6); where the Data Point Model conflicts with the instructions, "**policy and the reporting instructions must take precedence over the DPM**" (B4); reporting schedules listing actual submission deadlines are published separately for December and non-December year ends (A3); and interest payable and taxation are apportioned between IR.05.03 and IR.05.04 by fund allocation under Composites 2.2, or wholly to whichever is the larger part of the business (F9).
- **Products:** all.

### C. The life reporting templates a liability model must populate (Reporting Part Chapter 10 instruction files)

#### R89. Reporting Part Chapter 10 — **life technical provisions and obligations** instruction files (IR.12.01, IR.12.04, IR.14.01)
- **Publisher:** Prudential Regulation Authority (Bank of England), all dated 15-11-2024 (issued under PS15/24, [R6])
- **URLs:**
  IR.12.01 Life technical provisions — https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/regulatory-reporting/insurance/ir1201-instructions-life-technical-provisions-15-11-2024
  IR.12.04 Best estimate assumptions for life insurance risks — https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/regulatory-reporting/insurance/ir1204-instructions-best-estimate-assumptions-for-life-insurance-risks-15-11-2024
  IR.14.01 Life obligations analysis — https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/regulatory-reporting/insurance/ir1401-instructions-life-obligations-analysis-15-11-2024
  (matching `…-template-…` XLSX files exist at the same path pattern; **the XLSX templates themselves were not retrieved**)
- **Doc type:** template instruction ("LOG") files. **Accessed:** 2026-08-06. **fetched_ok:** yes (all three PDFs converted to text and read in full: 13,290 / 15,472 / 11,920 characters)
- **Annotation:** These three files are the UK equivalent of the NAIC Exhibit 5 / Analysis of
  Operations instructions — they define, cell by cell, what a liability model must output.
  **IR.12.01** (quarterly *and* annual; entity, third-country branch, RFF, MA portfolio and
  remaining part) fixes the six line-of-business columns and the technical-provision
  decomposition rows; it expressly permits approximations under Technical Provisions – Further
  Requirements 6 and permits **SS8/24 §3.2** to be used to calculate the risk margin during the
  financial year. It carries three **unit-linked-only** rows (surrender value, nominal value of
  units, matching value of units) that no other template collects. **IR.12.04** is the
  assumption-and-experience template: it compares the current valuation basis against the
  prior-year basis and **five years of the firm's own experience**, names the underlying
  mortality/morbidity table, and states the CMI projection parameterisation [R22]–[R31]; its
  stated purpose is "to give an indication of changes in the valuation basis, how the basis
  compares with experience and the variability of the firm's recent experience". **IR.14.01**
  is the only PRA template with a **product split**, and its Appendix carries the **PRA life
  insurance product reporting code list** (three-digit codes, formerly SS36/15) which maps
  directly onto the seven products in this library — see "Extracted mechanics" §5 and "Product
  applicability". Full detail is transcribed in "Extracted mechanics" §§3–5.
- **Products:** all seven; IR.14.01's product codes give the exact mapping.

#### R90. Reporting Part Chapter 10 — **with-profits and life revenue/capital** instruction files (IR.12.05, IR.12.06, IR.05.03, IR.05.10)
- **Publisher:** Prudential Regulation Authority (Bank of England), all dated 15-11-2024
- **URLs:**
  IR.12.05 With-profits value of bonus — https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/regulatory-reporting/insurance/ir1205-instructions-with-profits-value-of-bonus-15-11-2024
  IR.12.06 With-profits liabilities and assets — https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/regulatory-reporting/insurance/ir1206-instructions-with-profits-liabilities-and-assets-15-11-2024
  IR.05.03 Life income and expenditure — https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/regulatory-reporting/insurance/ir0503-instructions-life-income-and-expenditure-15-11-2024
  IR.05.10 Excess capital generation — https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/regulatory-reporting/insurance/ir0510-instructions-excess-capital-generation-15-11-2024
- **Doc type:** template instruction files. **Accessed:** 2026-08-06. **fetched_ok:** yes (all four read in full: 3,046 / 6,677 / 12,238 / 11,201 characters)
- **Annotation:** **IR.12.05** (successor to NS.01) decomposes the year's distribution of
  profits as discretionary benefits into bonuses added at date of claim, clawback of past
  bonuses (market value reductions, entered negative), cash bonuses, reversionary bonuses
  "calculated in accordance with COBS 20.2.17R and any subsequent COBS rules" [R9] and other
  bonuses, then derives the **shareholder transfer** by an explicit formula (Extracted
  mechanics §6). It states the market convention that "most with-profits funds are either
  '90:10' (shareholder entitled to 10% of surplus) or '100:0' (mutual or other funds where no
  shareholder entitlement)". **IR.12.06** (successor to NS.02) is the full realistic-balance-
  sheet decomposition: the with-profits benefits reserve (retrospective asset shares or
  prospective reserve, cross-referenced to **Surplus Funds 3.2 / 3.3 / 3.4**), six components
  of future policy related liabilities less two planned-deduction components, and the asset mix
  backing each. Its row R0150 must **tie to IR.12.01.01 R0030 C0010**. **IR.05.03** (successor
  to NS.05 "Revenue account life") is the life revenue account by line of business, reported on
  **financial-accounting** conventions rather than Solvency UK valuation, and covering "all
  insurance business regardless of the possible different classification between investment
  contracts and insurance contracts applicable in the financial statements". **IR.05.10** is a
  genuine **forward-looking projection template**: one actual column plus **three business-plan
  years**, decomposing the movement in excess capital (eligible own funds less SCR). Full
  detail in "Extracted mechanics" §§6–8.
- **Products:** WP (IR.12.05 / IR.12.06); all life (IR.05.03); large life writers (IR.05.10).

#### R91. Reporting Part Chapter 10 — **matching adjustment** reporting instruction files (MALIR 1–7, IRR.22.02, IRR.22.03)
- **Publisher:** Prudential Regulation Authority (Bank of England), all dated 15-11-2024
- **URLs:**
  MALIR (all seven templates in one log file) — https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/regulatory-reporting/insurance/malir-instructions-15-11-2024
  IRR.22.02 Matching adjustment portfolio projection of future cash flows — https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/regulatory-reporting/insurance/irr2202-instructions-matching-adjustment-portfolio-projection-of-future-cash-flows-15-11-2024
  IRR.22.03 Matching adjustment calculation — https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/regulatory-reporting/insurance/irr2203-instructions-matching-adjustment-calculation-15-11-2024
- **Doc type:** template instruction files. **Accessed:** 2026-08-06. **fetched_ok:** yes (MALIR 48,344 characters — MALIR 1, 2 and 3 read in full, MALIR 4–7 headers and the appendix only; IRR.22.02 2,687 characters and IRR.22.03 5,430 characters read in full)
- **Annotation:** The MA reporting set is where a UK pension-annuity model's cash-flow output is
  actually consumed, and it is far more demanding than any other UK liability reporting.
  Verified from the MALIR log file: seven templates (**MALIR 1 Firm Information, 2 Asset cash
  flows, 3 Liability cash flows, 4 Portfolio Output, 5 Matching Tests, 6 Assets – Further Info,
  7 Reconciliation**); **all seven apply to all firms with an MA permission**; **a separate
  MALIR is completed for each MA portfolio (MAP)**; submission is through the **Bank of England
  Electronic Data Submission (BEEDS) portal within 130 business days after the firm's financial
  year end (or twelve weeks after the end of the financial reporting period)**; "**All
  information in the MALIR should be provided at the effective date of 31 December**"; amounts
  in **GBP millions**; every investment in IR.06.02, every derivative in IR.08.01 and **every
  reinsurance treaty** must be captured. MALIR 2 requires each asset line to be tagged with the
  **MAP component A/B/C "as set out in chapter 4 of SS7/18"** [R8], the fundamental-spread table
  used (nine options: government and central bank; corporate financial / non-financial in EUR,
  USD, GBP and other currency), the credit quality step, the rating method (externally rated /
  internally rated / internal rating applied as overlay) and the notched ratings of Fitch,
  Moody's, S&P and any other CRA. MALIR 3 is the liability-model hook and is transcribed in
  "Extracted mechanics" §9. **IRR.22.02** is the annual per-MA-portfolio cash-flow projection.
  **IRR.22.03** carries the MA calculation outputs, including a **mortality-stress eligibility
  figure** and a Macaulay-equivalent liability duration; its row R0050 (increase of fundamental
  spread for sub-investment-grade assets) is expressly dead — "**This adjustment is no longer
  required by the matching adjustment rules and R0050 should be reported as zero from 31
  December 2024**". Note PS18/26 [R87] replaces MALIR 1–7 with MA.00.01 / MA.00.02 / MA.01.01 /
  MA.02.01 / MA.03.01 in XBRL from the 31 December 2026 reference date; **the replacement
  instruction files were not retrieved**.
- **Products:** PA (dominant); WP and IP only via the MA "eligible element" route [R2].

### D. Governance: the system of governance, the actuarial function, the ORSA and audit

#### R92. PRA Rulebook — **Conditions Governing Business Part** (as at 05/08/2026)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.prarulebook.co.uk/pra-rules/conditions-governing-business/05-08-2026 (355,375 bytes)
- **Doc type:** rulebook part. **Accessed:** 2026-08-06. **fetched_ok:** yes (browser User-Agent; converted to text and read)
- **Annotation:** The governance charter for anyone who builds or owns a UK liability model.
  Chapter list verified: 1 Application and Definitions; **1A Expert Judgement**; 2 General
  Governance Requirements; 2A System of Governance; **3 Risk Management** (which contains the
  ORSA rules at 3.8–3.12); 3A Remuneration Policy; **4 Internal Control**; 4A Specific
  Provisions – Functions; 5 Internal Audit; **6 Actuarial Function**; 7 Outsourcing; 8 Finite
  Reinsurance; 9 Restriction of Business; 10 Premiums for New Business; 11 Statistical Data;
  **11A Alternative Methods for Valuation**; **11B Valuation of Technical Provisions –
  Validation**; **11C Valuation of Technical Provisions – Documentation**; **11D Internal
  Control of Valuation of Assets and Liabilities**; 11E Risk Management in Firms Providing
  Loans and/or Mortgage Insurance or Reinsurance; 12 Lloyd's. Rule 2.2(3) enumerates the
  system of governance as compliance with, among other things, the risk-management policy
  (2.5), Chapters 2A–7, Insurance – Fitness and Propriety, **Insurance – Allocation of
  Responsibilities 4**, Chapters 11A–11F, the risk-management system (3.1), the compliance
  function (4.1(2)), the internal audit function (Chapter 5) and the **actuarial function
  (Chapter 6)** — i.e. the "four key functions" in UK rule terms are risk management,
  compliance, internal audit and actuarial. Rule 2.3 makes the whole system proportionate to
  "the nature, scale and complexity of its operations"; 2.2(4) requires regular internal
  review. Chapters 1A, 3, 4, 6, 11A–11D are transcribed in "Extracted mechanics" §§11–14.
  Most of the substance carries a **31/12/2024** effective date stamp (restated from the EU
  Delegated Regulation by PS15/24 [R6]); 3.2 carries **30/06/2024** (the MA reforms, PS10/24
  [R5]); 6.1 and several older rules carry **01/01/2016**.
- **Products:** all.

#### R93. PRA Rulebook — **Actuaries Part** (as at 05/08/2026)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.prarulebook.co.uk/pra-rules/actuaries/05-08-2026 (107,831 bytes)
- **Doc type:** rulebook part. **Accessed:** 2026-08-06. **fetched_ok:** yes
- **Annotation:** Short but load-bearing. Chapters: 1 Application and Definitions; 2
  Appointment of Actuaries; 3 Actuaries' Qualifications; 4 Conflicts of Interest; **5
  With-Profits Actuary Function**; 6 Duties of Actuaries; 7 Lloyd's. Verified: rule **2.1** — a
  firm "must appoint an **external actuary** if it does not have the capability within the firm
  or the firm's group to comply with **Conditions Governing Business 6**" (i.e. the UK does not
  require an appointed actuary as such; it requires an effective actuarial function, and an
  external appointment only if the firm cannot staff it). Rule **2.2** — a firm carrying on
  with-profits insurance business "**must appoint one or more actuaries to perform the
  With-Profits Actuary function in respect of all classes of its with-profits insurance
  business**". Rule 2.3 sets vacancy-notification duties; **2.4** lets the PRA appoint an
  actuary itself, at the firm's expense, where a firm fails to fill a vacancy **within 28
  days**. Rule **4.1** bars the appointed actuary from performing the Chief Executive function,
  bars the With-Profits Actuary from the governing body, and bars any other function giving
  rise to a significant conflict. Rule **5.1** sets the five substantive With-Profits Actuary
  duties (transcribed at "Extracted mechanics" §15). Rules 6.1–6.3 require objectivity, freedom
  from bias, and "due regard to **generally accepted actuarial practice**" — the hook for IFoA
  APS L1 [R35] and the FRC TASs [R33][R34]. Rules 6.4–6.5 require the actuary to notify the PRA
  without delay on removal, resignation, non-reappointment or disqualification, and to say
  whether there is any matter that ought to be drawn to the PRA's attention.
- **Products:** all; WP especially (Chapter 5 applies only to with-profits business).

#### R94. PRA Rulebook — **Insurance – Senior Management Functions Part** and **Insurance – Allocation of Responsibilities Part** (as at 05/08/2026)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URLs:** https://www.prarulebook.co.uk/pra-rules/insurance---senior-management-functions/05-08-2026 (221,346 bytes) ;
  https://www.prarulebook.co.uk/pra-rules/insurance---allocation-of-responsibilities/05-08-2026 (190,115 bytes)
- **Doc type:** rulebook parts (two Parts, one entry). **Accessed:** 2026-08-06. **fetched_ok:** yes (both)
- **Annotation:** Who is personally accountable for the model output and the return. Verified
  from **Insurance – Senior Management Functions**: rule 2.1 — each of the functions in
  Chapters 3–10 and 12 "is a controlled function and a PRA senior management function"; rule
  2.2 — each holder must be individually approved by the PRA; rule **7.1** — "**The Chief
  Actuary function (SMF20) is the function of having responsibility for the actuarial function
  specified in Conditions Governing Business 6**"; rule **8.2** — "**The With-Profits Actuary
  function (SMF20a) is the function of having responsibility for advising the governing body of
  a firm transacting with-profits insurance business on the exercise of discretion affecting
  part or all of that business, as described more fully in Actuaries 5.1**", Chapter 8 applying
  "only to firms that carry on with-profits insurance business" (8.1). Rule 2.3 requires every
  firm (other than a third-country branch undertaking, a firm without a UK establishment, a
  small run-off firm or a UK ISPV) to have a Chief Executive function, a Chief Finance function
  and a Chair of the Governing Body function. Rule 2.4 (as amended 24/04/2026) gives a
  **12-weeks-in-12-months** temporary-cover carve-out. Verified from **Insurance – Allocation
  of Responsibilities** rule 3.1, the prescribed responsibilities: **PR Q — "responsibility for
  the production and integrity of the firm's financial information and its regulatory
  reporting"** (3.1(4)); **PR T2 — "responsibility for performance of the firm's ORSA"**
  (3.1(7)); PR O — allocation and maintenance of capital and liquidity (3.1(5)); PR T —
  development and maintenance of the business model (3.1(6)); PR X — outsourcing under
  Conditions Governing Business 7 (3.1(12)). Rule 3A.2 sets the third-country-branch variants
  (PR AA, PR FF, PR EE, PR BB).
- **Products:** all; SMF20a and Actuaries 5.1 bite only on WP.

#### R95. SS19/16 — *Solvency II: ORSA* (May 2026 version), with SS41/15
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URLs:** publication page https://www.bankofengland.co.uk/prudential-regulation/publication/2016/solvency2-orsa ;
  **May 2026 version** (effective 31 December 2026, published as part of PS13/26) https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/supervisory-statement/2026/ss1916-may-2026-update ;
  **November 2024 version** (effective 31 December 2024, PS15/24) https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/supervisory-statement/2024/ss1916-november-2024-update.pdf
- **Doc type:** supervisory statement. **Accessed:** 2026-08-06. **fetched_ok:** yes (both PDFs retrieved and read: November 2024 14,189 characters, May 2026 15,287 characters)
- **Annotation:** The PRA's expectations on the ORSA — the only forward-looking solvency
  assessment a UK firm must perform, and therefore the main consumer of a multi-year liability
  projection. Section list identical in both versions: Introduction; ORSA supervisory report;
  The ORSA policy; Board sign-off and embedding of the ORSA; Business strategy; Risks; Capital
  and solvency; Stress testing; Groups; Internal model; Standard formula. Substance transcribed
  at "Extracted mechanics" §13.4. The only material difference located between the two versions
  is scope: the November 2024 text is addressed to "all UK Solvency II firms, including in the
  context of provisions relating to Solvency II groups, mutuals, **third-country branches** and
  to the Society of Lloyd's and its managing agents"; the **May 2026 text drops third-country
  branches** ("all UK Solvency II firms, including in the context of provisions relating to
  Solvency II groups, mutuals and to the Socie[ty]…"), consistent with PS13/26. No
  paragraph-by-paragraph diff was performed [unverified beyond the scope sentence].
- **Also fetched (same date):**
  - **R95b. SS41/15 — *Solvency II: applying EIOPA's Set 2, System of Governance and ORSA
    Guidelines* (November 2024).** Publisher: PRA. URLs: publication page
    https://www.bankofengland.co.uk/prudential-regulation/publication/2015/solvency2-applying-eiopa-set2-system-of-governance-and-orsa-guidelines-ss ;
    PDF https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/supervisory-statement/2024/ss4115-november-2024-update.pdf . fetched_ok: yes (10,166 characters read in full). **This is the rule that keeps the EIOPA guidelines alive in the UK:** §2.2 — "The PRA expects firms to **comply with all of the Set 2, System of Governance and ORSA Guidelines (as at the end of the transition period) that apply to them, in a proportionate manner**." The Guidelines referred to are EIOPA's Set 2 (final reports 6 July 2015) and the System of Governance and ORSA Guidelines (final reports 3 February 2015), and SS19/16 §10.1 cites **Guideline 10 of EIOPA-BoS-14/259** (ORSA) by name [R95]. §3.1–3.3 deal with the **Valuation 5.4 derogation** (recognising and valuing an asset or liability on the financial-statements basis), pointing to **SS38/15** for which financial reporting standards are consistent with Article 75. §6.1 is a live defect — see "Gaps and caveats".
- **Products:** all.

#### R96. PRA Rulebook — **External Audit Part** (as at 05/08/2026), with SS11/16
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.prarulebook.co.uk/pra-rules/external-audit/05-08-2026 (94,830 bytes)
- **Doc type:** rulebook part. **Accessed:** 2026-08-06. **fetched_ok:** yes
- **Annotation:** The rule that makes part of the SFCR — including the life technical provisions
  template — subject to a **reasonable assurance** audit opinion, and the rule that decides
  which firms escape it via a **quantitative score built directly out of reported template
  cells**. Chapters: 1 Application and Definitions (1.3 carries the definitions and the score
  formula, last amended **21/10/2025**); 2 External Audit of Relevant Elements of the SFCR; 3
  Appointment of Auditors; 4 Duties on the External Auditor. Applies to a UK Solvency II firm
  "that is **not a small firm for external audit purposes**" and, at group level, to a group
  that is not a small group (1.1), in respect of financial years ending on or after 15 November
  2016 (1.2). The score formula, the definitions of life insurance BEL and life GWP by template
  cell reference, and the audited scope are transcribed at "Extracted mechanics" §16.
- **Also fetched (same date):**
  - **R96b. SS11/16 — *Solvency II: External audit of, and responsibilities of the governing
    body in relation to, the public disclosure requirement* (November 2024, updating June
    2024).** Publisher: PRA. URL: publication page
    https://www.bankofengland.co.uk/prudential-regulation/publication/2016/solvency2-external-audit-of-the-public-disclosure-requirement-ss ("Current version published on 15 November 2024. Effective from 31 December 2024. Following PS15/24"). fetched_ok: yes (PDF text 28,604 characters read). Verified: §2.1–2.3 — the PRA expects the governing body to take responsibility for the SFCR being properly prepared, to be satisfied that the firm complied in all material respects throughout the year and that it is reasonable to believe it will continue to comply, and to "**acknowledge and evidence in writing its responsibility for the SFCR … by signing the SFCR and attaching the written acknowledgment to the SFCR**". §3.1 defines the required assurance level as **reasonable assurance** under ISA (UK) 200. §3.4 — the auditor "is not expected to express an opinion on the validity of an approval, waiver or other supervisory determination"; **transitional measures on technical provisions are treated "as part of the framework against which the audit opinion is being given"**. §3.5 applies ISA (UK) 720 to the unaudited remainder of the SFCR. §§4.2A–4.2F set the matching-adjustment position: **auditors are not required to assess MA eligibility, but are expected to consider the scale of the MA claimed**, because "the impact of the MA on technical provisions falls within the relevant elements", and the PRA "does not approve the firm's calculation methodology as part of [the MA application] process".
- **Products:** all; the MA audit carve-out bites on PA.

#### R97. SS17/16 — *Solvency II: internal models – assessment, model change and the role of non-executive directors*, with SS1/24 and SS15/16
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URLs:** publication page https://www.bankofengland.co.uk/prudential-regulation/publication/2016/solvency2-internal-models-assessment-model-change-and-the-role-of-non-executive-directors-ss ("Current version published on 15 November 2024. Effective from 31 December 2024. Following PS15/24") ;
  **February 2024 version** https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/supervisory-statement/2024/ss1716-28-february-2024-update.pdf
- **Doc type:** supervisory statement. **Accessed:** 2026-08-06. **fetched_ok:** **partial** — the publication page was retrieved and read; the **February 2024 PDF** was retrieved and read (45,926 characters) but is stamped on every page "31 December 2024: This document has been superseded"; **the current November 2024 PDF was not retrieved** (two guessed media URLs returned HTTP 404 and the page's PDF links are script-rendered)
- **Annotation:** The model-governance expectations a liability-model builder must satisfy where
  the model feeds an internal model. Chapter list (February 2024 text): 1 Introduction; 2
  Application for internal model permission; 3 [Deleted]; 4 Modelling of the premium provision
  for general insurance firms; 5 [Deleted]; **6 Role of non-executive directors**; **7
  Validation of models**; 8 How the PRA uses quantitative analyses as part of model permission;
  **9 Internal model change policy**; **10 Reporting of analysis of change in SCR**. Chapter 7
  is the substantive part for this library and is transcribed at "Extracted mechanics" §17:
  model **justification** and model **validation** are two separate processes that firms must
  demonstrably demarcate (7.1); justification sits under the Statistical Quality Standards in
  Solvency Capital Requirement – Internal Models 11 and 16.2 and "it is **not the aim of the
  validation process to create a substitute for these requirements**" (7.3); validation is
  "regular and independent (from the development and operation of the model)" and reviews
  specification appropriateness, "the **correspondence of its results against experience**" and
  overall performance over time (7.4); the PRA expects "a combination of detailed 'bottom-up'
  testing and 'top-down' ownership by boards" (7.6) and evidence that the board challenged the
  validation, understood the key assumptions and limitations, **considered the possible
  quantification of those limitations** and took mitigating actions (7.8); and validation
  "should put specific attention on those key assumptions and **expert judgments** that have a
  material impact on the model and should also articulate how the sensitivity to the key
  assumptions and expert judgement are being assessed and taken into account in the decision
  process" (7.12). **Because the retrieved text is the superseded February 2024 version,
  paragraph numbers should be re-verified against the November 2024 PDF before citation in a
  product document.**
- **Also fetched / located (same date):**
  - **R97b. SS1/24 — *Expectations for meeting the PRA's internal model requirements for
    insurers under Solvency II*.** Publisher: PRA, first published 28 February 2024. URL:
    https://www.bankofengland.co.uk/prudential-regulation/publication/2024/february/expectations-for-meeting-the-pra-internal-model-requirements-ss . fetched_ok: **publication page only; the SS PDF was not retrieved.** Verified from the page: it sets expectations for the requirements arising from **Solvency Capital Requirement – Internal Models 10 to 16A**, covering the probability distribution forecast for a partial internal model, including new risks, **data used in the internal model**, **the model validation process**, **validation tools**, **documentation standards** and **minimum content of the documentation**. Directly relevant to model-governance drafting; **its content is [unverified] beyond this scope list**.
  - **R97c. SS15/16 — *Solvency II: Monitoring model drift and standard formula SCR reporting
    for firms with permission to use an internal model* (September 2025, updating July 2018).**
    Publisher: PRA. URL:
    https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/supervisory-statement/2025/ss1516-september-2025-update.pdf
    (verified HTTP 200 this session). fetched_ok: yes (PDF text 7,332 characters read).
    Verified: the PRA defines
    model drift as "the risk that capital requirements calculated using an internal model may,
    over time, become **less reflective of the risks to which firms are exposed**" (2.1); its
    monitoring tools include the internal-model SCR measured against **standard formula SCR,
    pre-corridor MCR, net written premium and best estimate liabilities** (2.3); different tools
    may be used for life and general insurance firms (2.3A); Solvency Capital Requirement –
    Internal Models **3.4** requires a firm with internal model permission to provide the PRA,
    **on request**, with an estimate of the standard formula SCR (3.3). Read alongside PS15/25
    [R87 ¶1.22], which removed the routine annual SF.01 submission for life internal-model
    firms from the 31 December 2025 reference date.
- **Products:** all, where an internal model is used (in practice PA and large WP/WOL books).

#### R98. PRA Rulebook — **Preparations for Solvent Exit Part** (as at 05/08/2026), with SS11/24
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URLs:** https://www.prarulebook.co.uk/pra-rules/preparations-for-solvent-exit/05-08-2026 (55,295 bytes) ;
  SS11/24 PDF https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/supervisory-statement/2024/ss1124-december-2024.pdf ;
  SS11/24 publication page https://www.bankofengland.co.uk/prudential-regulation/publication/2024/december/solvent-exit-planning-for-insurers-supervisory-statement
- **Doc type:** rulebook part + supervisory statement. **Accessed:** 2026-08-06. **fetched_ok:** yes (Rulebook Part read in full — it is only three chapters; SS11/24 PDF text 35,169 characters read in part — contents, chapter 1 and the solvent exit analysis sections)
- **Annotation:** A **new UK-only** planning obligation with no Solvency II ancestor, and the
  newest rule in this stream: every rule in the Part carries the effective date **30/06/2026**.
  Verified from the Part: it applies to a UK Solvency II firm, a non-directive insurer and (via
  Insurance General Application 3) the Society (1.1), **excluding passive run-off firms** (1.2);
  1.3 defines **solvent exit** as "the process through which a firm ceases its insurance
  business while remaining solvent" and **solvent exit analysis** as "a document setting out a
  firm's preparations for solvent exit". Rule **2.1** requires a firm to (1) prepare for solvent
  exit so it can effect one in an orderly manner, (2) **produce a solvent exit analysis and
  update it whenever a material change has taken place … and at least once every three years**,
  (3) for a UK Solvency II firm in a group, take account of group implications and risks, and
  (4) provide the current version to the PRA on request. Verified from SS11/24: it applies to
  all PRA-regulated insurers **except firms in passive run-off, UK branches of overseas insurers
  and Lloyd's managing agents** (1.2); a solvent exit may be achieved by run-off, sale or partial
  sale, merger, a **Part VII FSMA transfer**, a scheme of arrangement and/or restructuring plan,
  or a combination (1.3); the SS is structured as chapter 2 (preparing a solvent exit analysis —
  solvent exit actions, **solvent exit indicators**, potential barriers and risks, resources and
  costs, communications, governance and decision-making, assurance) and chapter 3 (producing a
  **solvent exit execution plan (SEEP)** and executing a solvent exit). **Document defect:** the
  PDF's cover page is headed "Supervisory statement | **SS11/24**" while its page 2 masthead
  reads "Supervisory statement | **SS20/24**"; the Bank's publication page confirms **SS11/24**
  is the supervisory statement and **PS20/24** the accompanying policy statement.
- **Products:** all; most material for closed/run-off WOL and WP back-books.

---

## Extracted mechanics

Everything below was read from the retrieved documents. Rule and article references are to the
Reporting Part unless another Part is named. Formulas are reproduced in plain text.

### 1. The Solvency UK reporting inventory — what exists, who files it, when

**1.1 The complete list of things a UK Solvency II firm submits (Reporting 2.5A)** [R84]

Rule 2.5A says that, as part of the information required by 2.1, a firm must submit to the PRA
on a regular basis:

1. the **SFCR** (if applicable), disclosed under Chapters 3–6 and/or Group Supervision 18,
   together with any equivalent information disclosed publicly under other legal or regulatory
   requirements to which the SFCR refers;
2. the following **reports**:
   (a) a report comprising the results of each **ORSA**, in accordance with Conditions
   Governing Business 3.12;
   (b) for a third country branch undertaking, a **resolution report** (Article 49);
   (c) for internal model firms, the qualitative information supporting **QMC.01**
   (Article 6(3));
   (d) for internal model firms, the qualitative analysis supporting **AoC.01** (Articles 19
   and 35);
   (e) for firms with a matching adjustment permission, the **MALIR 1–7** templates
   (Articles 18A, 42A, 47A);
3. **annual, semi-annual and quarterly quantitative templates** in accordance with Chapters 2A
   and 7.

There is **no RSR** and no other narrative supervisory report. In the 31/12/2026 view, 2.5A(3)
becomes "annual, semi-annual, quarterly **and monthly** quantitative templates", 2.5A(2)(c)–(e)
are recast as "supporting **narrative documentation**", and 2.5A(2)(e) names the new MA
templates MA.00.01, MA.00.02, MA.01.01, MA.02.01 and MA.03.01.

**1.2 Deadlines (Reporting 2.5B, present view as at 05/08/2026)** [R84]

| Submission | Deadline | Rule |
|---|---|---|
| ORSA report | **within 10 business days after concluding the ORSA** | 2.5B(1) |
| Quarterly QRTs (Arts 6(1), 21A(6), 37) | **≤ 30 business days** after the end of each quarter of the firm's financial year | 2.5B(2) |
| Quarterly QMC.01 + supporting qualitative information (Art 6(3)) | **≤ 55 business days** after quarter end | 2.5B(3) |
| Semi-annual template (Art 7A) | **≤ 30 business days** after the end of each half of the financial year | 2.5B(4) |
| **Annual solo QRTs (Arts 8–18, 20, 21A, 38–48, 50)** | **≤ 70 business days after the firm's financial year end** | 2.5B(5) |
| Group quarterly QRTs (Art 23) | **≤ 55 business days** after group quarter end | 2.5B(6) |
| **Group annual QRTs (Arts 25–34)** | **≤ 100 business days after the group's financial year end** | 2.5B(7) |
| AoC.01 solo (Art 19) incl. supporting qualitative analysis | **≤ 70 business days**, commencing with the first financial year end **on or after 31 December 2025** (or, if internal model permission took effect later, the first financial year end after that) | 2.5B(8) |
| AoC.01 group (Art 35) | **≤ 100 business days**, same commencement rule | 2.5B(9) |
| Third-country-branch resolution report (Art 49(1)) | **≤ 70 business days** after (i) the first financial year end on or after 31 December 2024 and (ii) **every third financial year end thereafter** | 2.5B(10) |
| **MALIR 1–7 (Arts 18A, 42A, 47A)** | **≤ 130 business days after the firm's financial year end**, commencing with (i) the first financial year end on or after 31 December 2024 or (ii) if later, the first financial year end after the MA permission took effect | 2.5B(11) |
| **SFCR disclosure** | **≤ 70 business days after the firm's financial year end** | 2.5B(12)(a) |
| Group SFCR under Group Supervision 18 | **≤ 100 business days after the firm's financial year end** (rule text says *firm's*) | 2.5B(12)(b) |

Additions in the 31/12/2026 view (liquidity reporting; PS15/25 states the requirements come
into force **30 September 2026** [R87 ¶1.20]):

| Submission | Deadline | Rule |
|---|---|---|
| Annual committed facilities templates (Arts 51, 51A) | ≤ 70 business days after financial year end | 2.5B(11A) |
| Quarterly liquidity market risk sensitivities (Art 52) | ≤ 30 business days after quarter end | 2.5B(11B) |
| **Monthly cash-flow mismatch (Arts 53, 53A)** | **≤ 10 business days after the end of each month** | 2.5B(11C) |
| **Monthly cash-flow mismatch (short form) (Arts 54, 54A)** | **≤ 1 business day after the end of each month** | 2.5B(11D) |
| Cash-flow mismatch (short form) in stress | **every business day** while there is an actual or potential firm-specific or market liquidity stress | 2.5B(11E) |
| Standing capability | a firm "must ensure that it would be able **at all times** to meet the requirements for daily reporting under (11E) even if there is no … stress and none is expected" | 2.5B(11F) |

Submission is in electronic format (2.13(1)); a **friendly society** may alternatively submit by
post or by hand to the Regulatory Data Group, Statistics and Regulatory Data Division, Bank of
England, Threadneedle Street, London EC2R 8AH (2.13(2)). The electronic channel is the **BEEDS
portal** [R88c A9].

**1.3 Formatting rules (Chapter 2A Articles 2–4A; Chapter 3A Articles 2–3A)** [R84]

- Monetary data points: **units, no decimals**, except templates **IR.06.02, IR.08.01 and
  IR.11.01, which are in units with two decimals** (Art 2(1)(a)).
- Percentages: **per unit with four decimals** (Art 2(1)(b)). Integers: no decimals (Art 2(1)(c)).
- All data points positive except where the item is "of an opposite nature from the natural
  amount of the item", where the nature of the data point allows both signs, or where the
  instructions require otherwise (Art 2(1)(d)).
- Reporting currency = the currency of the firm's financial statements (solo) or consolidated
  financial statements (group) (Art 3(1)); balance-sheet items convert at the **closing rate on
  the last day for which the appropriate rate is available in the reporting period** (Art 3(3));
  income and expense convert on the accounting basis (Art 4(a)); the exchange-rate source must
  be the same as used for the financial statements (Art 5).
- **Re-submission:** firms must re-submit "as soon as practicable" where information originally
  reported "**has materially changed** in relation to the same reporting period after the last
  submission" (Art 4). Article 21A(7) adds a specific correction duty for the Article 21A
  templates: on the firm's or the PRA's notification of inaccuracy or incompleteness, the firm
  "must **promptly** make any appropriate corrections or adjustments and if necessary re-submit".
- **Materiality:** information is material "where its omission or misstatement could influence
  the decision-making or judgement of the PRA" (Chapter 2A Art 4A) / "of the users of that
  information, including the PRA" (Chapter 3A Art 3A). Articles 4 and 4A do **not** apply to the
  Article 21A templates or the Article 50 third-country-branch templates (Chapter 2A Art 1(4)).
- **SFCR presentation:** monetary amounts are disclosed **in thousands of units** (Chapter 3A
  Art 2) — different from the supervisory templates.

**1.4 Solo annual template list by Article** [R84]

- **Art 8** (basic information): IR.01.01.01 content of submission; IR.01.02.01 basic
  information on the firm; **IR.01.03.01 basic information on the ring-fenced funds and
  matching adjustment portfolios**.
- **Art 9** (balance sheet and general): IR.02.01.01 balance sheet on **both** the Valuation
  Part basis **and** the financial-statements basis; IR.02.02.01 assets and liabilities by
  currency; IR.03.01.01 off-balance-sheet items (only where guarantees/collateral/contingent
  liabilities exceed **2% of total assets** per IR.02.01.01, or where an unlimited guarantee has
  been given or received); IR.03.02.01 and IR.03.03.01 unlimited guarantees received/provided;
  IR.05.02.01 premiums, claims and expenses by country on the financial-statements basis;
  **IR.05.03.01 life income and expenditure**; IR.05.04.01 non-life income, expenditure and
  business model analysis; IR.05.05.01 life premiums and claims by country; IR.05.06.01 non-life
  premiums and claims by country; and **IR.05.10.01 excess capital generation, "where life
  premiums (excluding unit-linked premiums) written in the most recent reporting year exceed
  £1 billion"** (Art 9(1)(k)).
- **Art 10** (investments): IR.06.02.01 item-by-item list of assets and IR.08.01.01 open
  derivatives where the firm is exempted from the Q4 quarterly submission by a **s.138A FSMA
  direction**; IR.06.03.01 collective-investment look-through where exempted or where the
  collective-investment ratio is not above 30%; **IR.09.01.01 income, gains and losses in the
  reporting period by asset category**. (Chapter 9 also lists IR.10.01 securities lending and
  repos and IR.11.01 assets held as collateral; the Article 10 sub-paragraphs requiring them
  were not individually transcribed.)
- **Art 11** (technical provisions): **IR.12.01.01 life technical provisions**; **IR.12.03.01
  life best estimate liabilities by country**; **IR.14.01.01 life obligations analysis … by
  product issued by the firm**; IR.16.01.01 annuities stemming from non-life obligations;
  IR.16.02.01 projection of best estimate future cash flows of annuities stemming from non-life
  business; IR.17.01.01 and IR.17.03.01 non-life technical provisions and BEL by country;
  IR.18.01.01 projection of future cash flows based on best estimate of the **non-life**
  business; IR.19.01.01 non-life claims development triangles; IR.20.01.01 development of the
  distribution of claims incurred; IR.21.02.01 non-life underwriting risks; IR.21.04.01 cyber
  underwriting risk.
- **Art 12** (long-term guarantees): IR.22.01.01 impact of the long-term guarantee measures and
  transitionals; IR.22.04.01 interest-rate transitional; IR.22.07.01 best estimate subject to
  volatility adjustment by currency.
- **Art 13** (own funds and participations): IR.23.01.01; IR.23.02.01 by tiers; IR.23.03.01
  annual movements; IR.23.04.01 list of items; IR.24.01.01 participations.
- **Art 14** (SCR): IR.25.04.01 (all firms, all bases of calculation); IR.25.05.01 (full or
  partial internal model firms); IR.25.06.01 loss-absorbing capacity of deferred taxes;
  IR.26.01.01 market risk; IR.26.02.01 counterparty default; **IR.26.03.01 life underwriting
  risk**; IR.26.04.01 health underwriting risk; IR.26.05.01 non-life underwriting risk;
  IR.26.06.01 operational risk; IR.26.07.01 simplifications used; IR.27.01.01 non-life and
  health catastrophe risk.
- **Art 15** (MCR): **IR.28.01.01** where the firm carries on **only** long-term insurance
  business (or only general/reinsurance business); **IR.28.02.01** where it carries on **both**.
- **Art 16** (variation analysis): "[Note: Provision left blank]" — i.e. the EU S.29 variation
  analysis series has been dropped entirely.
- **Art 17** (reinsurance and SPVs): IR.30.05.01 reinsurer and collateral provider entity
  information; IR.30.03.01 and IR.30.04.01 outwards reinsurance contracts and reinsurer
  participations for the **next** reporting year; IR.31.01.01 outwards reinsurance balance-sheet
  exposures; **IR.30.06.01 life outwards reinsurance summary; IR.30.07.01 life outwards
  reinsurance proportional cover; IR.30.08.01 life outwards reinsurance non-proportional cover**.
- **Art 18** (per ring-fenced fund, per matching adjustment portfolio, and the remaining part):
  IRR.01.01.01; IRR.02.01.01 balance sheet; **IRR.12.01.01 life technical provisions**;
  IRR.17.01.01; **IRR.22.02.01 projection of future cash flows for the best estimate calculation
  by each matching adjustment portfolio**; **IRR.22.03.01 information on each matching
  adjustment portfolio**; IRR.25.04.01 notional SCR; IRR.25.05.01 (internal model firms);
  IRR.26.01.01–IRR.26.07.01 notional SCR by risk module; IRR.27.01.01.
- **Art 18A:** MALIR 1–7 for firms with an MA permission. **Art 19:** AoC.01 for internal model
  firms, the analysis of change referred to in Solvency Capital Requirement – Internal Models
  13A. **Art 20:** IR.36.01.01, IR.36.02.01, IR.36.04.01 intra-group transactions.
- **Art 21A** (the "additional" templates — the former NSTs), verbatim conditions:
  - **21A(1):** IR.05.07.01 where the firm writes suretyship business improving the credit
    rating of the underlying security; IR.05.08.01 where the firm manages a material pooling
    agreement; IR.05.09.01 where the firm is an assessable mutual that has called an additional
    contribution after 1 January 2006 or has ancillary-own-funds approval under Own Funds 2.3(4).
  - **21A(3)** — *long-term insurers*: **(a) IR.12.04.01 best estimate assumptions for life
    insurance risks, "where the firm's gross best estimate liabilities for long-term insurance
    business, other than reinsurance, are more than £50 million **or** the firm's gross written
    premiums for long-term insurance business, other than reinsurance, are more than £10
    million"**; **(b) where the firm's net best estimate liabilities for with-profits insurance
    business are more than £500 million **and the firm is a single with-profits fund**:
    (i) IR.12.05.01 value of bonus; (ii) IR.12.06.01 liabilities and assets**.
  - **21A(4):** where net BEL for with-profits business exceeds **£500 million for the firm as a
    whole**, **IRR.12.05.01 and IRR.12.06.01 for each ring-fenced fund which is also a
    with-profits fund, and for the remaining part where that is a with-profits fund**.
  - **21A(5)** — *general insurers*: IR.18.02.01 and IR.19.02.01 on named classes.
  - **21A(6):** the Society submits IR.23.05.03 annually **and** quarterly.

**1.5 Solo quarterly templates (Art 6(1))** [R84]

IR.01.01.02 content of submission; IR.01.02.01 basic information; IR.02.01.02 balance sheet on
the Valuation Part basis only; **IR.05.03.02 life income and expenditure**; IR.05.04.02 non-life
income and expenditure; IR.06.02.01 list of assets (subject to Art 10(1)(b)); IR.08.01.01 open
derivatives (subject to Art 10(1)(e)); **IR.12.01.02 life technical provisions**; IR.17.01.02
non-life technical provisions by line of business; **IR.23.01.01 own funds**. Sub-paragraphs
(j), (l) and (m) are blank. Article 6(3) adds **QMC.01** (quarterly model change) for internal
model firms.

Article 6(2) is the quarterly-simplification permission that matters to a model owner: when
submitting the quarterly **technical provisions** templates (IR.12.01.02 and IR.17.01.02),
"firms **may apply simplified methods** in accordance with the Technical Provisions and
Technical Provisions – Further Requirements Parts of the PRA Rulebook in the calculation of the
technical provisions". Article 7(1) adds that quarterly balance-sheet measurements "may rely on
estimates and estimation methods to a greater extent than measurements of annual financial
data", provided the result is reliable and all material information relevant to understanding
the data is reported.

**1.6 Semi-annual (Art 7A)** [R84] — a single template: **IR.06.03.01** (look-through of all
collective investments) where the ratio of collective investments to total investments exceeds
**30%**, the ratio being (IR.02.01.02 C0010/R0180 + collective investment undertakings within
C0010/R0220 + collective investment undertakings within C0010/R0090) ÷ (C0010/R0070 +
C0010/R0220).

**1.7 The Chapter 9 template inventory (99 code stems)** [R84]

IR.01.01, IR.01.02, IR.01.03, IR.01.04, IR.02.01, IR.02.02, IR.02.03, IR.03.01, IR.03.02,
IR.03.03, IR.05.02, **IR.05.03**, IR.05.04, IR.05.05, IR.05.06, IR.05.07, IR.05.08, IR.05.09,
**IR.05.10**, IR.06.02, IR.06.03, IR.08.01, IR.09.01, IR.10.01, IR.11.01, **IR.12.01**,
**IR.12.03**, **IR.12.04**, **IR.12.05**, **IR.12.06**, **IR.14.01**, IR.16.01, IR.16.02,
IR.17.01, IR.17.03, IR.18.01, IR.18.02, IR.19.01, IR.19.02, IR.20.01, IR.21.02, IR.21.04,
IR.22.01, IR.22.02, IR.22.03, IR.22.04, IR.22.07, IR.23.01, IR.23.02, IR.23.03, IR.23.04,
IR.23.05, IR.24.01, IR.25.04, IR.25.05, IR.25.06, IR.26.01, IR.26.02, IR.26.03, IR.26.04,
IR.26.05, IR.26.06, IR.26.07, IR.27.01, IR.28.01, IR.28.02, IR.30.03, IR.30.04, IR.30.05,
IR.30.06, IR.30.07, IR.30.08, IR.31.01, IR.32.01, IR.33.01, IR.34.01, IR.35.01, IR.36.01,
IR.36.02, IR.36.04, IRR.01.01, IRR.02.01, **IRR.05.03**, IRR.12.01, **IRR.12.05**,
**IRR.12.06**, IRR.17.01, **IRR.22.02**, **IRR.22.03**, IRR.25.04, IRR.25.05, IRR.26.01,
IRR.26.02, IRR.26.03, IRR.26.04, IRR.26.05, IRR.26.06, IRR.26.07, IRR.27.01.

Plus the named returns **MALIR 1–7**, **AoC.01**, **QMC.01** and (Lloyd's) the annual and
quarterly solvency and asset data returns defined as "Lloyd's templates" in rule 1.2.
**There is no IR.13.01 and no IR.29.xx.**

### 2. The instruction ("LOG") file library [R88]

Chapter 10 of the Reporting Part contains only pointers ("Section IR.xx.yy instructions can be
found **here**"); the operative text is 83 PDF files under
`https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/regulatory-reporting/insurance/`,
**every one dated `15-11-2024`**, with a parallel `…-template-…` XLSX for each. The life-side
slugs (each prefixed by the base URL above, each suffixed `-15-11-2024`):

`ir0503-instructions-life-income-and-expenditure`,
`ir0505-instructions-life-premiums-and-claims-by-country`,
`ir0510-instructions-excess-capital-generation`,
`ir1201-instructions-life-technical-provisions`,
`ir1203-instructions-life-best-estimate-liabilities-by-country`,
`ir1204-instructions-best-estimate-assumptions-for-life-insurance-risks`,
`ir1205-instructions-with-profits-value-of-bonus`,
`ir1206-instructions-with-profits-liabilities-and-assets`,
`ir1401-instructions-life-obligations-analysis`,
`ir2603-instructions-solvency-capital-requirement-life-underwriting-risk`,
`ir3006-instructions-life-outwards-reinsurance-summary`,
`ir3007-instructions-life-outwards-proportional-reinsurance`,
`ir3008-instructions-life-outwards-non-proportional-reinsurance`,
`irr2202-instructions-matching-adjustment-portfolio-projection-of-future-cash-flows`,
`irr2203-instructions-matching-adjustment-calculation`,
`malir-instructions`,
`aoc01-instructions-analysis-of-change-in-solvency-capital-requirement`.

Where the Data Point Model and the instruction files disagree, "**policy and the reporting
instructions must take precedence over the DPM**" [R88c B4].

### 3. IR.12.01 / IRR.12.01 — life technical provisions [R89]

**Scope and basis.** Quarterly and annual, for individual entities, third country branches,
**ring-fenced funds, matching adjustment portfolios and the remaining part**. Approximations
under Technical Provisions – Further Requirements 6 are allowed, and **SS8/24 §3.2 may be
applied to calculate the risk margin during the financial year**. Segmentation uses the lines
of business in **Technical Provisions – Further Requirements Annex 1** and "shall reflect the
**nature of the risks underlying the contract (substance), rather than the legal form of the
contract (form)**"; a contract covering risks across lines of business must, where possible, be
**unbundled** (TP–FR 26.5). Information is reported **gross of reinsurance**, with recoverables
in dedicated rows. Rows R0010–R0100 are **after** the volatility adjustment, matching adjustment
and the risk-free-rate transitional (where applied) but **before** the TMTP, which is reported
separately at R0140–R0180.

**Columns.** C0010 insurance with profit participation; C0020 index-linked and unit-linked
insurance; **C0030 life annuities — "annuities and deferred annuities which would be included in
the line of business 'other life insurance'"** (i.e. annuities get their own column even though
they are not a separate LoB); C0040 annuities stemming from non-life contracts (health and
non-health combined); C0050 other life insurance **excluding** annuities and deferred annuities;
C0060 health insurance; C0070 total life and health. Reinsurance accepted is a **separate row**
for the underlying line of business, not a separate column.

**Rows.**
- R0025 gross best estimate, direct business; R0026 gross best estimate, reinsurance accepted;
  R0030 gross best estimate (both), each **including technical provisions calculated as a whole**
  and with no deduction for reinsurance, SPVs or finite reinsurance (Technical Provisions 3).
- R0040 total recoverables from reinsurance/SPV/finite re **before** the counterparty-default
  adjustment; R0050 traditional reinsurance; R0060 SPVs; R0070 finite reinsurance — each
  "calculated consistently with the boundaries of the contracts to which they relate, **including
  ceded intra group reinsurance**".
- R0080 total recoverables **after** the adjustment for expected losses due to counterparty
  default (Technical Provisions 11.1); R0090 best estimate minus recoverables; **R0100 risk
  margin** (Technical Provisions 4.2) — "**does not apply to third country branches**".
- TMTP block: R0140 TMTP attributable to the risk margin = **Ar**; R0150 TMTP best estimate
  **dynamic** component = **Br**; R0160 TMTP best estimate **non-dynamic** component = **Cr**;
  R0170 **amortisation adjustment** (adjustment to increase the rate of run-off) = **Wr**;
  **R0180 = max(0, R0140 + R0150 + R0160 − R0170) = Tr**, reported positive. All refer to
  Transitional Measure on Technical Provisions 5.1 [R3]. Firms on the **legacy approach** (per
  the Statement of Policy "Permissions for transitional measures on technical provisions and
  risk-free interest rates") report only R0140 and R0150, which then mean the risk-margin and
  best-estimate portions of the legacy TMTP; R0160 and R0170 do not apply to them.
- R0200 total technical provisions after the transitional deduction; R0210 the same minus
  recoverables.
- **Unit-linked-only rows (C0020 only):**
  - **R0300 surrender value** — "the amount, defined contractually, to be paid to the
    policyholder in case of early termination … **net of charges and policy loans**", net of
    taxes, "**includes surrender values guaranteed and not guaranteed**", allowing for
    "duration based penalties" and **assuming that any clause deferring the availability of the
    surrender value does not apply**.
  - **R0302 nominal value of units** — "value of units allocated. The amount **should allow for
    actuarial funding / discounting where these are 'initial' or 'capital' units subject to a
    higher management charge**".
  - **R0304 matching value of units** — the value of units held (included in IR.02.01 R0220 and
    R0340) which match the unit liability in R0302.
- Sensitivity/attribution rows: R0310 best estimate subject to the interest-rate transitional;
  R0320 TP without that transitional (but retaining the volatility adjustment where both
  applied); R0330 best estimate subject to the volatility adjustment; R0340 TP without the
  volatility adjustment and without other transitionals; **R0350 best estimate subject to the
  matching adjustment**; R0360 TP without the matching adjustment and without all the others.
- **IRR.12.01** (per RFF / MA portfolio / remaining part) requires only rows **R0025–R0030,
  R0080–R0100 and R0140–R0200**. Z0020 flags "1 – RFF/MAP" or "2 – Remaining part"; Z0030 is the
  fund/portfolio number, which "**must be consistent over time and with the fund/portfolio number
  reported in other templates**".

### 4. IR.12.04 — best estimate assumptions for life insurance risks [R89]

**Scope.** Applicable to life insurers. **Assumptions are not required for reinsurance.** Not
required if the only long-term business other than reinsurance is annuities stemming from
non-life contracts. Threshold: gross BEL for long-term insurance business (other than
reinsurance) **> £50m** *or* gross written premiums for that business **> £10m** (Article
21A(3)(a), [R84]).

**Purpose (quoted):** "to give an indication of **changes in the valuation basis**, how the
basis **compares with experience** and the **variability of the firm's recent experience**".

**Column structure.** C0010 valuation year Y basis; C0020 valuation year Y−1 basis; C0030–C0070
the firm's own experience in years Y−1, Y−2, Y−3, Y−4, Y−5; **C0080 underlying table**; C0090
subcategory description.

**Row-block structure.** Each assumption type occupies a block of **four rows spaced 40 apart**:
a total row (e.g. R0730) plus **three subcategory rows** (R0740, R0750, R0760) — "Three rows are
provided for each assumption type". Where assumptions vary by source of business, the firm shows
"the **largest 3 categories by number of policies**", in descending order of size; "Data is not
required for subcategories 2 and 3 where the previous line(s) already cover **at least 50% of the
business** for that product". Experience need not be shown where it is of **low credibility**,
with a stated guideline of "**less than 200 claims per annum** for an individual line of the
template". Items R0010–R1320 are entered as **percentages to 2 decimal places**; items
R1330–R2100 to 2 decimal places.

**The assumption rows (total rows only).**
- Mortality: R0010 male non-smoker, R0050 male aggregate, R0090 male smoker, R0130 female
  non-smoker, R0170 female aggregate, R0210 female smoker; **R0250 assurance mortality change
  per annum** — "increase (decrease) in mortality rates per annum applied each year after the
  valuation date … where the rate varies by year firms should calculate the **equivalent annual
  rate over ten years**", left blank where there is no allowance for change.
- Annuitant mortality: R0290 **individual pension annuitant, male**; R0330 individual pension
  annuitant, female — both "for standard lives (i.e. **not enhanced / impaired annuities**)";
  R0370 **bulk pension annuitant, male**; R0410 bulk pension annuitant, female — "for bulk
  buyouts of occupational pension schemes".
- Critical illness: R0450 male non-smoker, R0490 female non-smoker — "**where accelerated
  critical illness is the main product the basis should be the percentage of combined mortality
  and critical illness claims**"; R0530 critical illness change per annum (same ten-year
  equivalent-rate convention).
- Income protection: R0570 inception male, R0610 inception female, R0650 termination male,
  R0690 termination female.
- Lapse/surrender: R0730 with-profits endowment years 11+; R0770 unit-linked endowment years
  11+; **R0810 / R0850 / R0890 level term years 1–5 / 6–10 / 11+**; R0930 / R0970 / R1010
  decreasing term years 1–5 / 6–10 / 11+; **R1050 / R1090 / R1130 investment bond years 1–5 /
  6–10 / 11+, "including both part surrenders and full surrenders"**. For basis cells
  [C0010:C0020] the PRA expects the **arithmetic average** of the annual rates, "removing years
  which are not applicable or immaterial"; for experience cells [C0030:C0070] firms may choose
  arithmetic or weighted averaging "provided this is applied consistently".
- Transfers: R1170 pre-retirement transfer rate per annum, individual defined contribution
  pensions ("e.g. below age 55"); R1210 the same for group defined contribution pensions.
- **R1250 guaranteed annuity rate take-up** — "proportion of policyholders taking the guaranteed
  annuity rate which is in the money and where they are entitled [to take] the policy value
  either partly or fully in cash".
- **Expectation of life** (all "complete" expectation of life, i.e. "allowing for the exact
  period from the valuation date to the date of death"), each in a no-improvement and a
  with-improvement version: R1330 / R1370 male 50 (**for deferred annuities**); R1410 / R1450
  male 65 (**for pension annuities**); R1490 / R1530 male 80; R1570 / R1610 female 50; R1650 /
  R1690 female 65; R1730 / R1770 female 80. For R1380–R1800 "firms should use whichever of
  individual or bulk business is more significant".
- **Renewal management expense unit costs** ("per policy renewal management expense unit cost in
  the year following the valuation date"): R1810 with-profits endowment; R1850 unit-linked
  endowment; **R1890 term assurance**; **R1930 investment bond**; R1970 with-profits individual
  pension; R2010 unit-linked individual pension; **R2050 annuity — "for pension annuities in
  payment"**.
- **R1290 expense inflation after valuation date per annum** — the annual rate applied to the
  unit-cost subcategory rows, with the same ten-year equivalent-rate convention. (Note: R1290 is
  printed out of numerical order, between R2050 and R2090.)
- **R2090 aggregate renewal unit costs for the year following valuation** — "the total amount of
  renewal management expenses implied for the year following the valuation date arising from the
  renewal management unit costs. **Includes claims management expenses but excludes investment
  management expenses.** This line is only required for subcategory 1 and comprises the entire
  business."

**C0080 underlying table (quoted):** "Mortality / morbidity table, **e.g. AM92**. Where firms
use a percentage of the table which varies by age firms should append '**adjusted**' to the
table name, e.g. AM92 adjusted. Firms should show '**reinsurer**' where the basis uses the
reinsurer's rates. For annuitant mortality tables (R0300–R0440) firms should include the basis
for future improvements. **Where the CMI Mortality Projection Model is used for mortality
improvements, provide a description consistent with latest guidance from the CMI, e.g.
CMI_2018_G [L%; S=Sκ; A=A%].** Where an array of parameters is used in place of a single
parameter, provide a single equivalent value where possible." This is the direct regulatory hook
for CMI references [R22]–[R31]. General instruction: "For the lines relating to
mortality / morbidity tables firms should calculate an **approximate equivalent constant
percentage** if the percentage of the table varies by age or where there are adjustments to
age", and prior-year basis and experience must be converted to a percentage of the C0010 table
"using approximations as necessary to enable them to be compared". Firms "are **not required to
undertake any additional analysis of past claims**" to complete the template.

### 5. IR.14.01 — life obligations analysis, and the PRA life product code list [R89]

**Scope.** Annual, individual entities and third country branches. Covers life insurance
contracts (direct and accepted reinsurance) plus annuities stemming from non-life contracts.
"**All insurance contracts shall be reported even if classified as investment contract on
accounting basis.** In case of products unbundled, the different parts of the product shall be
reported in different rows, using different ID codes." **Reinsurance ceded is not reported in
IR.14.01.**

**Counting conventions.** Multiple policies issued as part of the same premium, identifiable
increments and rider benefits count as **a single contract**. For scheme contracts covering
multiple lives where the insurer provides protection or annuity benefits defined at member
level, the count is **the number of members**; for corporate pensions it is **the number of
schemes**. Contracts with more than one policyholder count as one. Inactive (paid-up) contracts
are still reported unless cancelled. Where technical provisions are calculated for a combination
of products (the instruction's own example is **with-profits guarantee costs**) or the product
code is uncertain, "firms should use an **approximation to apportion** between product codes".

**Columns.** C0001 line identification (unique numeric reference per row); **C0010 product ID
code** (three-digit; where the same product appears in more than one row the pattern is
`{ID code}/+/{name or number of version}`, e.g. `AB222/+/3`, and Master Trust business is shown
separately, e.g. `212/+/Master Trust`); C0020 fund number (for ring-fenced or other internal
funds, consistent across templates and never re-used); **C0030 line of business**, a closed list
— 29 health insurance, 30 insurance with profit participation, 31 index-linked and unit-linked
insurance, 32 other life insurance, 33 annuities from non-life relating to health, 34 annuities
from non-life other than health, 35 health reinsurance, 36 life reinsurance; **C0040 number of
contracts at the end of the year**; **C0050 number of new contracts during the year**; **C0060
written premiums** (gross); **C0070 claims paid** (gross, during the year, **including claims
management expenses** — *note PS18/26 removes claims management expenses from this definition
from the 31 December 2026 reference date* [R87 ¶2.41]); C0080 country (ISO 3166-1 alpha-2 of the
country where the contract was entered into, individually for countries above **10%** of
technical provisions or written premiums for that product, otherwise as a list); **C0180 best
estimate** (gross, including technical provisions as a whole); **C0190 capital at risk**, "as
defined in **Solvency Capital Requirement – Standard Formula 7.8 and 7.10**", zero for annuities
stemming from non-life unless they have positive risk.

**The PRA life insurance product reporting code list (Appendix to the IR.14.01 log file)** —
this is the former SS36/15 content, and it is the single best map from UK product taxonomy to
regulatory reporting.

*Savings and investments:* 100 Whole of life OB CWP · 101 Whole of life OB UWP · 102 Whole of
life OB UL · 104 Whole of life OB NP · 105 Whole of life IB CWP · 106 Whole of life IB NP ·
**111 Single premium bond UWP** · **112 Single premium bond UL** · **113 Single premium bond
IL** · **114 Single premium bond NP** · 120 Endowment OB CWP · 121 Endowment OB UWP · 122
Endowment OB UL · 124 Endowment OB NP · 125 Endowment IB CWP · 126 Endowment IB NP · 131
Investment only reinsurance UWP · 132 Investment only reinsurance UL.

*Individual pensions:* 200/201/202/204 individual defined contribution pensions CWP/UWP/UL/NP ·
210/211/212/214 workplace defined contribution pensions CWP/UWP/UL/NP · 221/222/224 income
drawdown UWP/UL/NP · 231/232 individual pensions investment-only reinsurance UWP/UL.

*Corporate pensions:* 300/301/302/304 corporate defined benefit pensions CWP/UWP/UL/NP ·
310/311/312/314 corporate defined contribution pensions WP/UWP/UL/NP · 321/322 corporate
pensions investment-only reinsurance UWP/UL.

*Protection:* **404 Level term regular premium** · **414 Level term single premium** · **424
Decreasing term regular premium** · **434 Decreasing term single premium** · **444 Accelerated
critical illness (guaranteed premiums)** · **454 Accelerated critical illness (reviewable
premiums)** · **464 Stand-alone critical illness (guaranteed premiums)** · **474 Stand-alone
critical illness (reviewable premiums)** · 480 Income protection CWP · 481 Income protection
Holloway accounts UWP · **494 Income protection (guaranteed premiums)** · **504 Income
protection (reviewable premiums)** · **514 Income protection single premium** · **524 Income
protection claims in payment** · 534 Group life · 544 Group death in service dependants'
annuities · 554 Collective life · 564 Group income protection · 574 Group income protection
claims in payment · 584 Group critical illness · 594 Risk premium mortality reinsurance · 604
Risk premium critical illness reinsurance · 614 Risk premium income protection reinsurance ·
620/621/622/624 Miscellaneous protection CWP/UWP/UL/NP.

*Annuities:* 700 Purchased life annuity WP · 704 Purchased life annuity NP · 710 Individual
deferred annuity WP · 714 Individual deferred annuity NP · **720 Individual pension annuity
WP** · **722 Individual pension annuity UL** · **724 Individual pension annuity NP** · **734
Individual enhanced pension annuity NP** · 740 Bulk purchase deferred annuity WP · 744 Bulk
purchase deferred annuity NP · 754 Bulk purchase pension annuity NP · 764 Purchased temporary
annuity NP · 774 Pension temporary annuity NP · 784 Annuity stemming from non-life · 794
Longevity swap accepted.

**Category notes (verbatim substance).** Whole life and endowment codes are **regular premium
business only**, include paid-up policies, and **exclude single premium bonds "which are
technically whole of life"**. "Single premium bond" **includes 'investment bond' and
'with-profits bond'**. Individual DC pensions are "pensions savings before retirement, excludes
deferred annuity buyouts, but contract may be written as deferred annuity with-profits,
endowment with-profits, UWP or UL. Individual means there is no employer involvement." Workplace
DC covers group pensions where "the insurer has a separate record for each employee covered …
The firm calculates liabilities at **member level**." Corporate pensions covers trust-based
arrangements where the insurer holds no individual records and "calculates liabilities at
**scheme level**". Miscellaneous protection is for protection that does not fit the named
categories, "e.g. long term care". Bulk purchase annuity is "for annuity liabilities arising
from occupational pension schemes including where members hold individual policies after winding
up of the scheme".

**Abbreviations (verbatim).** OB ordinary branch; IB industrial branch ("business sold in the
past where premiums were collected door to door"); **WP** with-profits — "a contract of
long-term insurance which provides benefits through eligibility to participate in discretionary
distributions based on profits"; **CWP** conventional with-profits — "the traditional style …
where the policy specifies the regular premium payable and the initial guaranteed benefit, to
which reversionary (annual bonuses) are added"; **UWP** unitised with-profits (includes
accumulating with-profits) — "where each premium is invested in units or to an account at the
face value of the amount invested. This amount grows with 'bonus' and any further premiums";
**UL** unit-linked — "the same as the legal term '**property linked**' in the PRA annual
returns"; **IL** index-linked — "includes policies linked to a stock market index or the value
of specific securities. **It excludes RPI / CPI linked policies**"; **NP** non-profit — "all
policies covered by the 'Other' Solvency II line of business and including life health
business".

### 6. IR.12.05 / IRR.12.05 — with-profits value of bonus [R90]

**Scope.** Where the firm as a whole is a **single** with-profits fund it completes IR.12.05.01;
otherwise it completes **IRR.12.05.01 for each ring-fenced fund which is also a with-profits
fund, and for the remaining part where that is a with-profits fund** (Article 21A(3)(b) and
(4)). Threshold: net BEL for with-profits business **> £500 million** [R84].

**Column convention.** "Most with-profits funds are either '**90:10**' (shareholder entitled to
10% of surplus) or '**100:0**' (mutual or other funds where no shareholder entitlement)." Where
the shareholder is entitled to a share of surplus the value of bonus goes in
**C0040[R0010:R0050]**; for mutual or other funds with no shareholder entitlement it goes in
**C0030[R0010:R0050]**.

**Rows R0010–R0060 (value of bonus).**
- R0010 **bonuses added at date of claim** — "value of additions to nominal amount of benefit at
  date of claim, e.g. '**interim bonus**', '**terminal / final bonus**'".
- R0020 **clawback of past bonuses at date of claim** — "**market value reductions** to the
  extent these are clawbacks of previous bonus additions or bonus added at date of claim
  included in R0010", **shown as a negative amount**.
- R0030 **cash bonuses** — "amounts paid directly to policyholders as a result of distribution of
  profits following the year end valuation".
- R0040 **reversionary bonuses** — "**discounted value** of additions to guaranteed benefits as a
  result of distribution of profits following the year end valuation. Reversionary bonuses are
  also known as annual bonuses. **The value must be calculated in accordance with COBS 20.2.17R**
  and any subsequent COBS rules" [R9].
- R0050 other bonuses.
- R0060 total distribution of profits as discretionary benefits = `SUM(R0010:R0050)` in each of
  C0030, C0040 and C0050.

**Rows R0080–R0120 (shareholder transfer).**
- R0080/C0050 **shareholder proportion (bonuses)** — "shareholder proportion of profits
  distributed as discretionary benefits where eligible to participate, **e.g. 10.00%**".
- **R0090/C0050 shareholder transfer accruing during the financial year** — stated formula:

  ```
  R0090/C0050 = R0060/C0040 * R0080/C0050 / (1 - R0080/C0050)
  ```

  i.e. `shareholder transfer = (policyholder value of bonus) * s / (1 - s)` where `s` is the
  shareholder proportion. For a 90:10 fund, `s = 0.10`, so the transfer is one ninth of the
  policyholder bonus value. "Shareholder transfer in respect of distribution of profits as
  discretionary benefits is **derived from** the value of these discretionary benefits."
- R0100/C0050 amount brought forward — "total shareholder transfers **deferred from previous
  years**, for example due to restrictions relating to capital position of the fund".
- R0110/C0050 amount transferred — "**the maximum is R0090/C0050 + R0100/C0050**".
- R0120/C0050 amount carried forward = `R0090/C0050 + R0100/C0050 - R0110/C0050`.

### 7. IR.12.06 / IRR.12.06 — with-profits liabilities and assets [R90]

Same scope trigger as IR.12.05. This is the UK realistic-balance-sheet decomposition inside the
Solvency UK best estimate.

- **R0010 with-profits benefits reserve (WPBR)** — "for all policies, whether calculated
  retrospectively or prospectively, **excluding Holloway sickness policies**. This item
  corresponds to **with-profits policy liabilities (other than future policy-related liabilities)
  in Surplus Funds 3.2**."
- R0020 **asset shares where applicable** — the part of the WPBR calculated **retrospectively**
  in accordance with **Surplus Funds 3.3**.
- R0050 **prospective reserve where asset shares not applicable** — the part calculated
  **prospectively** in accordance with **Surplus Funds 3.4**.
- R0030 total **past** miscellaneous surplus included in the WPBR which is **permanent** per
  Surplus Funds 3.3(3) and 3.3(4); R0040 miscellaneous surplus **added at the valuation date**
  which is permanent. "**Provisional allocations should be excluded**" from both.
- **Future policy related liabilities (FPRL) components:**
  - R0070 **future costs of contractual guarantees** — "expected cost of paying **excess claim
    amounts due to the guaranteed benefits exceeding the with-profits benefit reserve at the date
    of claim**. Future cost of guarantees **cannot be negative**. Examples are guaranteed sums
    assured and bonuses on maturity or retirement, guarantees at a point in time and guaranteed
    minimum bonus rates, but **exclude cost of financial options**. With-profits benefits reserve
    is **after** allowing for past deductions for guarantees, options, smoothing and other costs."
  - R0080 **future costs of non-contractual commitments** — amounts the firm expects to pay "to
    meet non-contractual commitments **including liabilities arising from the regulatory duty for
    firms to treat customers fairly**. This includes amounts such as a **mortgage endowment
    promise** and **excludes any requirement to distribute the estate in a closed fund**" [R12].
  - R0090 **future costs of financial options** — "such as **guaranteed annuity rates and cash
    option rates**".
  - R0100 **future costs of smoothing** — "the present value of the difference between projected
    claims and the projected with-profits benefit reserve after enhancements, other than payouts
    on guarantees. **Future costs of smoothing can be negative.**"
  - R0110 financing costs; R0120 other with-profits insurance liabilities.
  - R0130 **planned deductions for guarantees, options and smoothing** — "expected future charges
    from the with-profits benefits reserve to cover the costs of guarantees, options or
    smoothing"; R0140 planned deductions for other costs.
  - **R0060 future policy related liabilities = SUM(R0070:R0120) − R0130 − R0140.**
- **R0150 total with-profits best estimate liabilities = WPBR + FPRL**, and "**Amounts should
  correspond to IR.12.01.01 R0030 C0010**" — an explicit cross-template tie.
- Investment return rows (percentages to 2 dp): R0160 overall investment return **post
  investment costs but pre-tax** ("If the firm identifies a portfolio of assets to back asset
  shares the returns must be based on these assets. If there are several asset share portfolios
  the returns … must be based on the **largest**"); R0170 return allocated to **non-taxable**
  (e.g. pensions) asset shares; R0180 return allocated to **taxable** (e.g. endowment) asset
  shares; R0190 miscellaneous surplus adjustment to investment return in the valuation year.
- Asset mix, by **CIC code**, split between the assets backing the WPBR (R0200 government bonds
  CIC 1, R0210 corporate bonds CIC 2, R0220 equity CIC 3, R0230 property CIC 9, R0240 cash CIC 7,
  R0250 other = WPBR less the preceding) and the assets backing the FPRL (R0260–R0310 on the same
  categories). "**Any investment fund assets (CIC code 4) should be allocated to the underlying
  asset type.**"

### 8. IR.05.03 (life income and expenditure) and IR.05.10 (excess capital generation) [R90]

**8.1 IR.05.03 — the life revenue account.** Quarterly and annual; individual entities, groups,
third country branches, ring-fenced funds and the remaining part; "in this template figures for
the remaining part **incorporate any embedded matching adjustment portfolios**". Basis:
"**financial accounting conventions**, unless these instructions state that an item is to be
reported on a Solvency II basis" — following the recognition and valuation basis of the published
financial statements with **no new recognition or re-valuation**, and following the accounting
standard declared at IR.01.02 row R0120 [R38]. Written premiums use the **Glossary** definition
"regardless of the accounting standard used". "**Claims incurred shall comprise all claim
payments paid in the reporting period plus change in provision for claims outstanding.**"
Year-to-date basis. Columns mirror IR.12.01 (C0010 with-profit participation, C0020 index-linked
and unit-linked, C0030 life annuities, C0040 annuities from non-life, C0050 other life, C0060
health, C0070 total).

Row sequence: R0010/R0020/R0030 gross written premiums direct / reinsurance accepted / both;
R0040 reinsurers' share; R0050 net. **R0060 investment income before tax** and **R0070 realised
and unrealised gains/(losses)** are required **only for C0020 and C0070** — "firms are **not
required to attribute investment income between lines of business other than to index-linked and
unit-linked**". R0080 other income; R0090 total income net of reinsurance = SUM(R0050:R0080).
R0110–R0150 claims incurred gross direct / accepted / gross / reinsurers' share / net.
R0160–R0200 expenses incurred on the same five-way split, "**on accrual basis** and excluding
other technical expenses not allocated to lines of business reported in R0300". R0210–R0270
analyse gross expenses, and **must sum to R0180**: R0210 acquisition commission; R0220
acquisition costs – other ("**includes movements in deferred acquisition costs**"); R0230 renewal
commission; R0240 administrative expenses; R0250 investment management expenses; R0260 claims
management expenses ("**shall include the movement in provisions in claims management
expenses**"); R0270 overhead expenses (including "expenses related to the **development of new
insurance and reinsurance business**, advertising insurance products, improvement of the internal
processes such as investment in system required to support insurance and reinsurance business").
R0280 interest payable; R0290 taxation (may be negative); R0300 other expenses; **R0310 total
expenditure = R0150 + R0200 + R0280 + R0290 + R0300**. R0410 business transfers-in; R0420
business transfers-out; **R0430 transfers to (from) other funds — "shareholder transfers arising
from with-profits business, transfers of unit management charges and capital movements between
funds. This item only applies to IRR.05.03.01"**; R0440 dividends paid (including foreseeable
dividends at the end of the previous period, excluding those at the end of the current period).
For quarterly solo, quarterly group and annual group reporting only rows R0010–R0050,
R0110–R0200, R0300 and R0440 are completed; R0080–R0090 and R0280–R0440 are required only for the
total column C0070.

**8.2 IR.05.10 — excess capital generation.** The only Solvency UK template that requires a
**multi-year forward projection**.

Scope per the instruction file: "required for **all life insurers, composite insurers, and
reinsurers that have reported life premiums (including health business that is similar to
long-term business, but excluding unit-linked premiums) greater than £1bn during any of the three
most recent reporting years (this reporting year inclusive)**". Firms may round to the nearest
£m but must still show amounts in units. **Purpose:** "to understand changes in firms' excess
capital under Solvency II, both historically and to understand drivers of **forecast** changes to
excess capital."

Columns: **C0010** the most recently completed financial year (actual); **C0020, C0030, C0040**
plan years 1, 2 and 3, "forward looking figures **based on your business plan**". Where
assumptions have changed materially between the business-plan date and the reporting date, "please
include the most up to date business plan data that is available".

Row structure:
- Existing business: **R0010 own funds generation – current backbook** (business written before
  C0010; "annuity writers are **expected to include earning the non-illiquid portion of its
  assets' total spread**"); **R0020 own funds generation – planned new business** (cumulative
  across years written in C0010…C0030; zero for C0010); **R0030 SCR run-off – current backbook**
  ("we'd typically expect this to be a reduction in capital required to be held as claims are
  paid, a year of a policy has elapsed, and policies are surrendered, mature or lapse");
  **R0040 SCR run-off – planned new business**; **R0050 risk margin run-off – current backbook**
  ("report this **gross of any movement in TMTP**"); **R0060 risk margin run-off – planned new
  business**; **R0070 TMTP run-off** ("the impact of changes in the **TMTP asset (within technical
  provisions)** on excess capital"); **R0080 total = R0010+R0020+R0030+R0040+R0050+R0060+R0070**.
- New business (**discrete year, not cumulative**): R0090 change in own funds; R0100 change in
  risk margin; R0110 change in SCR; **R0120 total = R0090+R0100+R0110**.
- **R0130 underlying capital generation = R0080 + R0120.**
- Variances (normally only in C0010): R0140 **experience variance** — "non-economic variances
  versus what was forecast … differences between actual experience and assumptions for
  **longevity, mortality and expenses**"; R0150 **economic variance** — "risk free interest rates,
  credit spreads, inflation, equities performance, changes in the book value of a subsidiary";
  R0160 other operating variance; **R0170 total = R0140+R0150+R0160**.
- **R0180 organic capital generation = R0130 + R0170.**
- R0190 **management actions** (investment strategy/asset portfolio reallocation, asset/liability
  matching, reinsurance programmes, hedging arrangements); R0200 **assumption changes**
  (including economic; "changes to forecast longevity expectations and credit default rates");
  R0210 **model changes**; **R0220 total = R0190+R0200+R0210**.
- R0230 portfolio transfers; **R0240 shareholder transfers from with-profit funds during the
  year**; R0250 debt raise; R0260 debt repayment; R0270 net equity issuance; R0280 debt interest
  expense; R0290 dividends paid; **R0310 total = R0230+…+R0290**.
- R0320 other inorganic changes ("changes in capital restricted due to **tiering limits** or
  changes in the value of a **deferred tax asset**").
- **R0400 total change in excess capital = R0180 + R0220 + R0310 + R0320.**
- Reconciliation block: R0500/R0510 eligible own funds to meet the SCR at the start/end of the
  period (expected to reconcile to the prior-year and current-year **IR.23.01.01**); R0520/R0530
  SCR at start/end; **R0540 excess capital at start = R0500 − R0520**; **R0550 excess capital at
  end = R0510 − R0530**.
- Premium block, "presented on the same basis as what is reported in the current year
  **IR.14.01.01** submission", using the IR.14.01 appendix to allocate individual product types
  to the high-level categories: **R0600 savings & investments; R0610 individual pensions; R0620
  corporate pensions; R0630 protection; R0640 annuities; R0650 total**.

### 9. The matching adjustment reporting set [R91]

**9.1 MALIR 3 — liability cash flows.** The most demanding liability-model output in Solvency UK.
Four liability streams, each reported three ways:

| Stream | Column |
|---|---|
| Level or fixed-escalation claim cash flows | C01 |
| **Inflation-linked** claim cash flows | C02 |
| Expense cash flows | C03 |
| Other liability-related cash flows | C04 |

- **MALIR 3 §3.1_C01–C04:** the **present value** of the monthly liability cash flows, **gross of
  reinsurance**, used in the calculation of the **base MA**, **discounted at the basic risk-free
  rate**, positive, in £m.
- **MALIR 3 §3.2_C01–C04:** the same present values **discounted at basic RFR + MA**.
- **MALIR 3 §3.3_C01–C04:** the **monthly gross liability cash flows themselves**, "for cash flows
  which extend beyond 50 years the portion beyond year 50 should be **discounted back to month
  600 at the basic risk-free rate** and reflected in the **month 600 row**". Positive, £m.
- Classification rule, repeated in every cell: "**For liabilities with a combination of fixed and
  inflation-linked characteristics the full set of liability cash flows should be reflected as
  inflation-linked**" (i.e. C02 absorbs the whole contract, not a split).
- Inflation-linked cash flows use "the **best estimate assumptions regarding future inflation**".
- Free-text descriptions of what is included in the expense stream and the "other" stream are
  required at MALIR 3 §3.5 and §3.4 respectively.

So the model must be able to emit, per MA portfolio: **600 monthly buckets × 4 liability streams,
gross of reinsurance, on the base-MA basis**, plus their present values on two discount bases.

**9.2 MALIR 2 — asset cash flows (relevant constraints).** Asset cash flows "should be consistent
with overall metrics (eg yield and spread) for each asset"; nominal cash flows are shown for
inflation-linked assets "based on the best estimate assumptions regarding future inflation";
inflation-linked derivative exposures are shown **net** based on projected future inflation; where
an asset is paired with a derivative (e.g. a currency swap) "the eventual £m cash flow from the
pairing should be reflected"; the same **month-600 truncation and discounting rule** applies;
"**the cash flows attributed to reinsurance, net of any Counterparty Default Adjustment (CDA),
should be provided as per the expectation set out in chapter 2 of SS7/18**" [R8]; and "if only a
part of the asset cash flows are MA eligible, **only include the eligible portion**".

**9.3 IRR.22.02 — MA portfolio projection of future cash flows.** Annual, individual entities,
"**reported by each matching portfolio approved by the PRA**". Rows R0010–R0450 are years, "split
by year of due payment of the cash flow, **counting the periods of 12 months from the date of
reference of the reporting**". Columns: **C0020 longevity, mortality and revision obligations cash
outflows**; **C0030 expenses cash outflows**; **C0040 de-risked asset cash flows** — "these flows
shall be appropriately corrected to take into account the probability of default or the portion of
the long term average of the spread over the risk-free interest rate as set out in **Matching
Adjustment 4**"; **C0050 positive undiscounted mismatch (inflows > outflows)**; **C0060 negative
undiscounted mismatch (inflows < outflows)**. Critically: "If the frequency is lower than yearly
then report the **sum** of the positive/negative undiscounted mismatches through the year of each
row. **Positive mismatches for some periods shall not be netted off of negative mismatches.**"

**9.4 IRR.22.03 — matching adjustment calculation.** Annual, per approved matching portfolio.
- C0010/R0010 **annual effective rate applied to the cash flows of the obligations** — "the single
  discount rate that, where applied to the cash flows of the portfolio of … obligations, results
  in a value that is equal to the value in accordance with **Valuation 2.1** of the portfolio of
  assigned assets".
- C0010/R0020 **annual effective rate of the best estimate** — the single discount rate producing
  the best estimate on the **basic risk-free** term structure.
- C0010/R0030 probability of default used to de-risk asset cash flows; C0010/R0040 the portion of
  the fundamental spread **not** reflected in the asset cash-flow adjustment (both as financial
  percentages, both excluding R0050).
- **C0010/R0050 increase of fundamental spread for sub-investment-grade assets — "This adjustment
  is no longer required by the matching adjustment rules and R0050 should be reported as zero from
  31 December 2024."**
- C0010/R0060 **matching adjustment to the risk free rate**, "reported in basis points using
  decimal notation, e.g. 100bp reported as 0.01".
- **C0010/R0070 mortality risk stress for the purpose of the matching adjustment** — "increase of
  the gross best estimate calculated with the basic risk free rate following a mortality risk
  stress compared to the gross best estimate calculated with the basic risk rate, as set out in
  Matching Adjustment 4 and **Matching Adjustment 2.4**" (the eligibility test).
- Portfolio block: R0080 market value of portfolio assets (Solvency II value); R0090 market value
  of assets with inflation-linked return; **R0100 best estimate of cash flows of the obligations
  that depend on inflation**; R0110 market value of assets where a third party can change the cash
  flows; R0120 **de-risked internal rate of return** of the assets.
- Surrender block (annual experience): R0130 market value (best estimate) of obligations
  **surrendered during the reporting period**; **R0140 number of surrender options exercised**;
  R0150 market value of the assets covering those obligations at the time of exercise; R0160
  amount actually paid to policyholders, which "differs from row R0130 and R0150 where the
  surrender clause of the contract does not give the policyholder the right to receive the full
  amount".
- Liabilities block: **R0170 duration** — "measure equivalent to **Macaulay duration** for
  liabilities considering all cash flows of insurance or reinsurance obligations arising from
  portfolios where the matching adjustment has been used".

### 10. The Solvency and Financial Condition Report [R84][R85]

**10.1 The obligation and the shape.** A firm "must disclose publicly, on an annual basis, a
SFCR" (Reporting 3.1). The disclosure must follow the structure in Chapter 3A Article 1A,
include the information in 3.3–3.7C and 3.10, and include the 2.3 content and comply with the
2.4 principles (3.2). **Chapter 3A Article 1A fixes the headings verbatim:**

```
Summary
A  Business and Performance      A.1 Business · A.2 Underwriting Performance ·
                                 A.3 Investment Performance · A.4 Performance of other
                                 activities · A.5 Any other information
B  System of Governance          B.1 General information on the system of governance ·
                                 B.2 Fit and proper requirements ·
                                 B.3 Risk management system including the own risk and
                                     solvency assessment ·
                                 B.4 Internal control system · B.5 Internal audit function ·
                                 B.6 Actuarial function · B.7 Outsourcing ·
                                 B.8 Any other information
C  Risk Profile                  C.1 Underwriting risk · C.2 Market risk · C.3 Credit risk ·
                                 C.4 Liquidity risk · C.5 Operational risk ·
                                 C.6 Other material risks · C.7 Any other information
D  Valuation for Solvency        D.1 Assets · D.2 Technical provisions · D.3 Other liabilities ·
   Purposes                      D.4 Alternative methods for valuation ·
                                 D.5 Any other information
E  Capital Management            E.1 Own funds ·
                                 E.2 Solvency Capital Requirement and Minimum Capital
                                     Requirement ·
                                 E.3 Differences between the standard formula and any internal
                                     model used ·
                                 E.4 Non-compliance with the Minimum Capital Requirement and
                                     non-compliance with the Solvency Capital Requirement ·
                                 E.5 Any other information
```

Rule 3.3(6) requires "**a clear and concise summary understandable to policyholders**", which
"shall highlight any **material changes** to the matters described in 3.3(1), (2), (4), and (5)
over the reporting period".

**10.2 Section D.2 — the technical provisions disclosure (Reporting 3.4A(2)).** For each
**material line of business**: the value of technical provisions **including the amount of the
best estimate and the risk margin separately**, with the bases, methods and main assumptions;
**a description of the level of uncertainty associated with the value of technical provisions**;
a quantitative and qualitative explanation of material differences between the solvency basis and
the financial-statements basis; a statement on whether the risk-free-rate transitional or the
TMTP is applied together with **a quantification of the impact of not applying it on technical
provisions, SCR, MCR, basic own funds and eligible own funds to cover the MCR and SCR**; a
description of reinsurance and SPV recoverables; and "**any material changes in the relevant
assumptions made in the calculation of technical provisions compared to the previous reporting
period**". SS40/15 §12.10 adds only that firms "should describe the **significant simplified
methods** used to calculate technical provisions, including those used for calculating the risk
margin" [R85].

**10.3 Matching adjustment and volatility adjustment disclosure (Reporting 3.4, effective
24/07/2025).** Where a firm applies a **matching adjustment**, the SFCR must include (a) a
description of the MA and of the relevant portfolio of obligations and portfolio of assets to
which it is applied; (b) **a quantification of the impact of a change to zero of the MA on the
firm's financial position including technical provisions, SCR, MCR, basic own funds and eligible
own funds to cover the MCR and the SCR**; and (c) **the disclosure in respect of the firm's
attestation required by Chapter 11 of the Matching Adjustment Part** [R2]. Where a **volatility
adjustment** is applied: a statement that it is used, and the same change-to-zero quantification.

**10.4 Section B disclosures relevant to a model owner (Reporting 3.3B).** B.1 requires a
description of "the main roles and responsibilities of **key functions**"; B.3 requires a
description of the risk-management system and "**how the risk management system, including the
risk management function, are implemented and integrated into the organisational structure and
decision-making processes**", plus the ORSA process, "a statement detailing **how often the ORSA
is reviewed and approved by the firm's governing body**", and "a statement explaining **how the
firm has determined its own solvency needs** given its risk profile and how its capital
management activities and its risk management system interact"; B.6 requires "a description of
**how the actuarial function of the firm is implemented**"; B.7 the outsourcing policy and the
jurisdiction of service providers; B.9 an assessment of the adequacy of the system of governance
to the nature, scale and complexity of the risks. SS40/15 §12.5 adds, for internal model firms,
a description of internal model governance including "**a description of the validation process
(used to monitor the performance and on-going appropriateness of the internal model)**" [R85].

**10.5 Section C (Reporting 3.3C).** Qualitative and quantitative risk-profile information
separately for underwriting, market, credit, liquidity, operational and other material risks,
covering exposure (including off-balance-sheet and risk transferred to SPVs), concentrations,
risk-mitigation techniques and the processes for monitoring their continued effectiveness, and —
directly relevant to a projection model — "**With regard to risk sensitivity, a description of
the methods used, the assumptions made and the outcome of stress testing and sensitivity analysis
for material risks and events**" (3.3C(5)).

**10.6 Section E (Reporting 3.5, 3.5A, 3.6, 3.6A, 3.6B, 3.7, 3.7A–3.7C).** Own funds by tier at
this and the previous reporting date with an analysis of significant changes; eligible own funds
to cover the SCR and the MCR classified by tier; the reconciliation between financial-statements
equity and the excess of assets over liabilities; deferred tax information including, "where the
amount of deferred tax assets is material, a description of the **underlying assumptions used for
the projection of probable future taxable profit** for the purposes of Valuation 11" (3.5A(9)(c)(iii));
the amounts of SCR and MCR at period end; **the SCR split by risk module (standard formula) or by
risk category (internal model)**; whether simplified calculations or undertaking-specific
parameters are used and for which modules; the inputs used to calculate the MCR; **any material
change to the SCR and MCR over the period and the reasons**; and the loss-absorbing capacity of
deferred taxes. Rule 3.7 requires the SCR disclosure to be accompanied "where applicable, with a
statement indicating that **the final amount of the SCR is subject to supervisory assessment**".
Rule 3.6(2) requires disclosure of **any capital add-on** (other than one imposed for internal
model residual deviation) with the PRA's justification.

**10.7 SFCR disclosure templates (Chapter 3A Article 4(1))** — the twelve templates a solo firm
must publish inside its SFCR: **IR.02.01.02** (balance sheet on the Valuation Part basis);
IR.05.02.01 (premiums, claims and expenses by country); **IR.05.03.02** (life income and
expenditure); IR.05.04.02; **IR.12.01.02** (life technical provisions); IR.17.01.02;
IR.19.01.21; **IR.22.01.21** (impact of long-term guarantee and transitional measures);
**IR.23.01.01** (own funds); **IR.25.04.21** (SCR); IR.28.01.01 and IR.28.02.01 (MCR).
Sub-paragraph (k) is blank. Note the **disclosure variants are different template variants from
the supervisory ones** (`.02` and `.21` suffixes), and are published in **thousands** (Art 2).

**10.8 Means and timing of disclosure (Chapter 3A Article 3B).** The SFCR must be disclosed on
the firm's own website if it maintains one, or on its trade association's website if permitted;
it must **remain available for at least five years** after the disclosure date; a firm not using
a website must send an electronic copy to anyone requesting it **within 10 business days**, for
five years; and any firm must send a **printed** copy on request made within two years, **within
20 business days**. The SFCR and any updated version must be submitted to the PRA in electronic
form (Art 3B(6)) and "**as soon as the SFCR … is disclosed by a firm it shall be submitted to the
PRA**" (Reporting 3.9).

**10.9 Non-disclosure, updates and breach disclosure (Chapters 4 and 5).** A PRA waiver may
permit non-disclosure of information required by 3.3(1)–(4) and 3.4, but only where disclosure
"would enable competitors of the firm to gain a **significant, undue advantage**" or the firm is
bound to secrecy or confidentiality by policyholder or counterparty obligations; the firm must
say in its SFCR which limb applies (4.1) and notify the PRA when the reason ceases (4.2).
"**Major developments**" require an updated SFCR "as soon as possible" (5.1, 5.1A, 5.1B), or
supplementary amendments (5.1C). Rule 5.2 deems two events major: **MCR non-compliance** where
the PRA does not receive a finance scheme within one month, and **significant SCR non-compliance**
where no recovery plan is received within two months. Rule 5.3 requires immediate public
disclosure of the amount, origin, consequences and remedial measures; **5.4** requires further
public disclosure at the end of **three months** if MCR compliance is not restored; **5.5** at
the end of **six months** if SCR compliance is not restored.

**10.10 Policy and approval (Chapter 6).** A firm must have appropriate systems and structures
and **"a written policy ensuring the ongoing appropriateness of any information disclosed"**,
including voluntary information (6.1); and "**A firm must ensure that its SFCR is (1) subject to
approval by its governing body; and (2) not publicly disclosed until the approval … is
received**" (6.2). SS11/16 §2.3 adds the expectation that the governing body **signs the SFCR and
attaches a written acknowledgment of its responsibility** [R96b]. SS40/15 §14.1 sets the required
content of the **public disclosure policy** (who prepares and reviews, the completion process,
the governing-body review and approval process, what public-domain information is being relied on
as equivalent, what is being withheld under a Reporting 4.1 waiver, and what is disclosed
voluntarily); §15.1 sets the equivalent content for the **supervisory reporting policy** (who
drafts and reviews, "processes and timelines for completion … review and approval", and
"**explanation of processes and controls for ensuring the reliability, completeness and
consistency of the data provided**") [R85].

### 11. Conditions Governing Business — the actuarial function [R92]

**11.1 The nine statutory tasks (CGB 6.1(1)).** A firm must provide for an effective actuarial
function to:
(a) **coordinate the calculation of technical provisions**;
(b) **ensure the appropriateness of the methodologies and underlying models used, as well as the
assumptions made** in the calculation of technical provisions;
(c) **assess the sufficiency and quality of the data** used in that calculation;
(d) **compare the best estimate against experience**;
(e) **inform the governing body of the reliability and adequacy** of the calculation;
(f) oversee the calculation in the cases set out in Technical Provisions 12;
(g) **express an opinion on the overall underwriting policy**;
(h) **express an opinion on the adequacy of reinsurance arrangements**; and
(i) contribute to the effective implementation of the risk-management system, "in particular with
respect to the **risk modelling underlying the calculation of the SCR and MCR** and to the firm's
**ORSA**".
CGB 6.1(2) requires the function to be carried out by persons with knowledge of actuarial and
financial mathematics commensurate with the nature, scale and complexity of the risks, "and who
are able to demonstrate their relevant experience with **applicable professional and other
standards**" — the hook for TAS 100/200 [R33][R34] and APS L1 [R35].

**11.2 What "coordinating the calculation" means (CGB 6.2).** Eight sub-tasks: (1) apply
methodologies and procedures to assess the **sufficiency** of technical provisions and ensure
consistency with the Technical Provisions Part and the Valuation Part; (2) **assess the
uncertainty** associated with the estimates; (3) ensure any **limitations of data** are properly
dealt with; (4) ensure the **most appropriate approximations** are used where Technical
Provisions – Further Requirements 12.2 applies; (5) ensure **homogeneous risk groups** are
identified "for an appropriate assessment of the underlying risks"; (6) consider relevant
financial-market information and generally available underwriting-risk data and ensure it is
integrated; (7) **compare and justify any material differences in the calculation of technical
provisions from year to year**; and (8) ensure "an appropriate assessment is provided of
**options and guarantees** included in contracts of insurance".

**11.3 Appropriateness, systems and experience (CGB 6.3–6.5).** The function must assess whether
the methodologies and assumptions are appropriate "**for the specific lines of business of the
firm and for the way the business of the firm is managed, having regard to the available data**"
(6.3), and whether "the **information technology systems** used in the calculation of technical
provisions sufficiently support the actuarial and statistical procedures" (6.4). On experience
comparison (6.5): the function must "review the quality of **past** best estimates and use the
insights gained … to improve the quality of **current** calculations", and the comparison "must
include comparisons between **observed values** and the **estimates underlying the calculation of
the best estimate**, in order to draw conclusions on the appropriateness, accuracy and
completeness of the **data and assumptions** used, as well as on the **methodologies** applied".

**11.4 Reporting to the board (CGB 6.6).** Information submitted to the governing body on the
calculation of technical provisions must include **at least a reasoned analysis on the reliability
and adequacy of the calculations and on the sources and degree of uncertainty**; that analysis
"**is supported by a sensitivity analysis that includes an investigation of the sensitivity of the
technical provisions to each of the major risks underlying the obligations**"; and the function
"clearly states and explains any concerns it may have concerning the adequacy of technical
provisions".

**11.5 The underwriting-policy opinion (CGB 6.7)** must at least conclude on: (1) **sufficiency
of the premiums to be earned to cover future claims and expenses**, taking into account the
underlying risks "and the impact of **options and guarantees** included in contracts of insurance
on the sufficiency of premiums"; (2) the effect of **inflation**, legal risk, change in portfolio
composition, and bonus-malus or similar systems within homogeneous risk groups; and (3) "**the
progressive tendency of a portfolio of contracts of insurance to attract or retain policyholders
with a higher risk profile (anti-selection)**".

**11.6 The reinsurance opinion (CGB 6.8)** must analyse the adequacy of: (1) the firm's risk
profile and underwriting policy; (2) reinsurance providers **taking into account their credit
standing**; (3) **the expected cover under stress scenarios** in relation to the underwriting
policy; and (4) **the calculation of the amounts recoverable** from reinsurance contracts and
SPVs.

**11.7 The annual report (CGB 6.9).** The actuarial function "must produce a **written report to
be submitted to the governing body, at least annually**", which must "**document all tasks that
have been undertaken by the actuarial function and their results**" and "**clearly identify any
deficiencies and give recommendations as to how such deficiencies should be remedied**".

### 12. Conditions Governing Business — expert judgement, risk management, internal control [R92]

**12.1 Expert judgement (CGB 1A).** "Where a firm makes assumptions about rules relating to the
valuation of assets and liabilities, technical provisions, own funds, SCR and MCR and the rules
set out in the Investments Part, these assumptions **must be based on the expertise of persons
with relevant knowledge, experience and understanding of the risks inherent in the firm's
insurance and reinsurance business**" (1A.1). And (1A.2), taking due account of proportionality,
a firm "must ensure that **internal users of the relevant assumptions are informed about their
relevant content, their degree of reliability and their limitations**. For that purpose, **service
providers to whom functions or activities have been outsourced must be considered to be internal
users**."

**12.2 The system of governance (CGB 2.2).** Must provide for sound and prudent management, and
include at least "an adequate transparent organisational structure with a clear allocation and
appropriate segregation of responsibilities" and "an effective system for ensuring the
transmission of information" (2.2(2)); must comply with the written risk-management policy
(2.5), Chapters 2A–7, Insurance – Fitness and Propriety, **Insurance – Allocation of
Responsibilities 4**, Chapters 11A–11F, the risk-management system (3.1), the compliance function
(4.1(2)), internal audit (Chapter 5) and the **actuarial function (Chapter 6)** (2.2(3)); and
"**must be subject to regular internal review**" (2.2(4)). Proportionate to nature, scale and
complexity (2.3).

**12.3 The risk-management system (CGB 3.1, 3.1A).** Must comprise "strategies, processes and
reporting procedures necessary to identify, measure, monitor, manage and report **on a continuous
basis** the risks, at an individual and at an aggregated level … **and their interdependencies**"
(3.1(1)), with a documented risk-management strategy, risk tolerance limits and assignment of
responsibilities (3.1(1A)(a)), a defined decision-making procedure (b), written policies defining
and categorising material risks with approved tolerance limits (c), and reporting procedures (d).
It must be "**well integrated into the organisational structure and decision-making processes**"
(3.1(2)(a)) and must cover **both** the risks in the SCR calculation **and "the risks which are
not, or not fully, included in the calculation thereof"** (3.1(2)(b)). The mandatory policy areas
(3.1(2)(c) and 3.1A) are: **underwriting and reserving** — including "actions … to assess and
manage the risk of loss or of adverse change in the values of insurance and reinsurance
liabilities, resulting from **inadequate pricing and provisioning assumptions**" and "the
sufficiency and quality of relevant data … as set out in Technical Provisions – Further
Requirements 4"; **asset-liability management** — structural mismatch "and in particular the
**duration mismatch**", dependencies between asset and liability classes and between obligations,
off-balance-sheet exposures, and the effect of risk-mitigation techniques; **investment risk
management**; **liquidity risk management** — including "**a plan to deal with changes in
expected cash in-flows and out-flows**"; **concentration risk**; **operational risk**;
**reinsurance and other risk-mitigation techniques**; and **deferred taxes** — where the
assessment of the methods and assumptions demonstrating the amount and recoverability of the
loss-absorbing capacity of deferred taxes, including "the assessment of the underlying assumptions
applied for the **projection of future taxable profit**", "must be carried out in each case by
**either the actuarial function or the risk-management function**" (3.1A(8)(b)).
CGB 3.1(2A) requires stress tests and scenario analysis "where appropriate … with regard to all
relevant risks"; 3.1(2B) requires the firm to take the reported information into account in its
decision-making.

**12.4 Long-term-guarantee sensitivities that must be produced regularly (CGB 3.2, 3.3).** A firm
must **regularly** assess (1) the sensitivity of its technical provisions and eligible own funds
to **the assumptions underlying the extrapolation of the risk-free curve** (Technical Provisions
5); (2) where the matching adjustment applies — the sensitivity of technical provisions and
eligible own funds to **the assumptions underlying the MA calculation, including the fundamental
spread** (Matching Adjustment 4), "**and the possible effect of a forced sale of assets on its
eligible own funds**"; the sensitivity to **changes in the composition of the assigned asset
portfolio**; and **the impact of a reduction of the matching adjustment to zero**; (3) the
equivalent for the volatility adjustment. These assessments "must [be] submit[ted] … as part of
the information reported annually in accordance with Reporting 2" (3.3), and where the reduction
to zero would breach the SCR, the firm must also submit **an analysis of the measures it could
apply to restore compliance** (3.3). CGB 3.1(3) separately requires a firm applying the MA or VA
to "**set up a liquidity plan projecting the incoming and outgoing cash-flows in relation to the
assets and liabilities subject to those adjustments**".

**12.5 The risk-management function (CGB 3.5).** Tasks: assist the governing body and other
functions; monitor the risk-management system; monitor the general risk profile; report in detail
on risk exposures and advise the board including on strategy, M&A and major projects; and
identify and assess emerging risks. It must "**liaise closely with the users of the outputs of the
internal model**" and "**co-operate closely with the actuarial function**" (3.5(3)).

**12.6 Internal control (CGB 4).** The internal control system must include administrative and
accounting procedures, an internal control framework, "appropriate reporting arrangements at all
levels of the firm" and a compliance function (4.1(2)); and must ensure compliance with law, the
effectiveness and efficiency of operations, and "**the availability and reliability of financial
and non-financial information**" (4.1(3)). The compliance function must have a compliance policy
and a compliance plan (4.1A) and must advise the board, "**assess the adequacy of the measures
adopted by the firm to prevent non-compliance**" and assess the impact of legal-environment
changes (4.2).

### 13. Conditions Governing Business — the ORSA [R92][R95]

**13.1 The rule (CGB 3.8).** A firm must conduct an ORSA as part of its risk-management system,
covering **at least**:
(a) **the firm's overall solvency needs** taking into account its specific risk profile, approved
risk tolerance limits and business strategy;
(b) **compliance, on a continuous basis, with (i) the SCR and MCR and (ii) the technical
provisions requirements in the Technical Provisions and Matching Adjustment Parts**; and
(c) **the significance with which the risk profile of the firm deviates from the assumptions
underlying the SCR**.
For (a) the firm must have proportionate processes enabling it "**to properly identify and assess
the risks it faces in the short and long term**" and "**demonstrate the methods used in that
assessment**" (3.8(3)).
**CGB 3.8(4) is the key computational requirement for a UK life model:** where a firm applies the
**matching adjustment, the volatility adjustment, the risk-free-rate transitional or the TMTP**,
it "must perform the assessment of compliance with the capital requirements referred to in
3.8(2)(b) **with and without taking into account those adjustments and transitional measures**".
Where an internal model is used, the 3.8(2)(c) assessment "must be performed together with the
recalibration that transforms the internal risk numbers into the SCR risk measure and
calibration" (3.8(5)).

**13.2 The forward-looking requirement (CGB 3.8A).** The ORSA must be **forward-looking** and
include (a) "risks the firm is or could be exposed to, taking into account **potential future
changes in its risk profile due to its business strategy or the economic and financial
environment**, including operational risks" and (b) "the nature and quality of own funds items or
other resources appropriate to cover the risks identified". These must take into account "(a) the
**time periods that are relevant for taking into account the risks the firm faces in the long
term**; (b) **valuation and recognition bases that are appropriate for the firm's business and
risk profile**; and (c) the firm's internal control and risk-management systems and approved risk
tolerance limits."

**13.3 Embedding, frequency and reporting (CGB 3.9–3.12).** The ORSA must be "an **integral part**
of its business strategy" and taken into account "**on an ongoing basis in its strategic
decisions**" (3.9). It must be performed "**regularly and without delay following any significant
change in its risk profile**" (3.10). The firm must inform the PRA of the results in an **ORSA
report** (3.11), which must include (1) the qualitative and quantitative results and the firm's
conclusions; (2) **the methods and main assumptions used**; (3) the overall solvency needs and
**a comparison between those solvency needs, the regulatory capital requirements and the firm's
own funds**; and (4) qualitative information on — and, where significant deviations are
identified, **a quantification of** — the extent to which quantifiable risks are not reflected in
the SCR calculation (3.12). Deadline: **within 10 business days after concluding the ORSA**
(Reporting 2.5B(1)) [R84].

**13.4 PRA expectations (SS19/16)** [R95]. "It is **fundamental** to the ORSA that it is forward
looking. The PRA expects firms to find ways to **estimate their future solvency position** while
assessing their current risk profile and how it is likely to change with the proposed business
strategy" (2.1). Good reports "include a clear summary; highlight the key outcomes of the
process; are not too long; and clearly signpost supporting documentation" (2.3). The **ORSA
policy is a standalone document, not part of the ORSA report** (3.1), and should state scope,
the entity list (including exclusions), how the ORSA incorporates strategic and business
planning, timing and frequency "**including, for example, its detailed elements such as stress
tests, sensitivity analyses and reverse stress tests**", triggers for an ad hoc ORSA,
**information on data quality standards**, the report structure and key ORSA records, roles and
responsibilities including the board's, and "a requirement for the **board to approve the ORSA
policy at least annually**". The board owns the process and the report must evidence board
sign-off, key conclusions and agreed management actions (4.1–4.2); some firms use an "**ORSA
dashboard**" to keep the board engaged between cycles (4.3). On strategy: "Good examples include a
high-level summary of firms' most recent performance as well as a **three to five year
forecast**", which "may include some granular data (e.g. class of business breakdown)" (5.2). On
capital and solvency: "**The PRA expects the assessment of firms' solvency over the business
planning period to form part of the ORSA process and report**", articulating current SCR and MCR
and the firm's own view of capital, why capital buffers are appropriate, a capital contingency
plan, the impact of stress testing, and "**key aspects of the methodology used and any deviations
from the standard formula or internal model calculations**" (7.1); the report must state the
quality of own funds and how it is likely to change over the planning period, with **dividend
policy "a key point in this assessment"** (7.2). On stress testing (8.1–8.4): "a sufficiently wide
range of **plausible** stress tests derived from the strategy and key risks"; "**The PRA expects
firms to apply reverse stress testing as part of their ORSA process. The ORSA report should define
what constitutes business failure and then detail what events could drive that outcome**"; firms
are expected to perform sensitivity tests and to "**identify key model assumptions and parameters
used, given changes in parameters and its impact on capital**"; and to consider the quality and
volatility of own funds and their loss-absorbing capacity under different scenarios. Internal
model firms' ORSA reports must, per EIOPA ORSA **Guideline 10**, "**confirm and evidence the
continued adequacy of the model to calculate the solvency capital requirement**" and confirm that
all identified risks are in the model, with justification for any exclusions (10.1). Standard
formula firms must "**explain clearly within the ORSA report where the firm's own risk profile
deviates from the standard formula assumptions**" and conclude whether the standard formula is
appropriate (11.1). SS41/15 §2.2 requires proportionate compliance with the whole EIOPA Set 2,
System of Governance and ORSA Guidelines as at the end of the transition period [R95b].

### 14. Conditions Governing Business — valuation validation, documentation and control [R92]

**14.1 Alternative valuation methods (CGB 11A.1).** Where used, a firm must (1) identify the
assets and liabilities concerned; (2) **justify** the use of the approach for them; (3) **document
the assumptions** underlying it; (4) **assess the valuation uncertainty**; and (5) "**regularly
compare the adequacy of the valuation … against experience**". Reporting 3.4A(4) requires SFCR
disclosure of the CGB 11A areas.

**14.2 Validation of technical provisions (CGB 11B).** A firm must validate the calculation "in
particular by **comparison against experience** as referred to in 4.4 and Technical Provisions 13,
**at least once a year** and **when there are indications that the data, assumptions or methods
used in the calculation or the level of the technical provisions are no longer appropriate**"
(11B.1(1)). The validation must cover: (a) the appropriateness, completeness and accuracy of
**data** (TP–FR 4); (b) the appropriateness of any **grouping of policies** (TP–FR 19); (c) the
**remedies to data limitations** (TP–FR 5); (d) the appropriateness of **approximations** (TP–FR
6); (e) "the **adequacy and realism of assumptions**" used for TP–FR 7 to 11; (f) "the adequacy,
applicability and relevance of the **actuarial and statistical methods** applied"; and (g) the
appropriateness of the level of technical provisions (Technical Provisions Chapter 14) for
compliance with Technical Provisions 2.1–2.3.
**CGB 11B.2 is the management-actions rule:** "a firm must assess the impact of changes in the
assumptions on **future management actions** on the valuation of the technical provisions. Where
changes in an assumption on future management action have a **significant impact**, a firm must be
able to explain the reasons for this impact and **how the impact is taken into account in its
decision-making process**."
**CGB 11B.3 fixes the granularity of validation:** separately for **homogeneous risk groups**;
separately for the **best estimate**, the **risk margin** and technical provisions calculated as
the market value of replicating financial instruments (TP–FR 22); **separately for technical
provisions where the matching adjustment is applied**; separately for the **gross best estimate**
and the **reinsurance/SPV recoverables**; and (non-life) separately for premium provisions and
provisions for claims outstanding.

**14.3 Documentation of technical provisions (CGB 11C).** A firm must document (1) the collection
of data and analysis of its quality; (2) **the choice of assumptions, "in particular the choice of
relevant assumptions about the allocation of expenses"**; (3) the selection and application of
actuarial and statistical methods; and (4) the validation (11C.1). For data (11C.2) the
documentation must include "**a directory of the data used in the calculation of the technical
provisions, specifying their source, characteristics and usage**", the collection/processing/
application specification required by TP–FR 4.3(5), and, where data is not used consistently over
time, "a description of the inconsistent use and **its justification**". For assumptions (11C.3)
it must include "(1) **a directory of all the relevant assumptions** … this must include
assumptions on **future management actions**; (2) a **justification** for the choice; (3) a
description of the **inputs** on which the choice is based; (4) the **objectives** of the choice
and the **criteria** used for determining appropriateness; (5) **any material limitations** in the
choice made; (6) a description of the **processes in place to review** the choice; (7) a
**justification for the changes of assumptions from one period to another and an estimation of the
impact of material changes**; and (8) the relevant deviations from assumptions about future
management actions referred to in TP–FR 8.2."

**14.4 Internal control of valuation (CGB 11D).** Effective systems and controls to ensure
valuation estimates are reliable and Valuation-Part-compliant, and "**a process for regularly
verifying that market prices or valuation model inputs are appropriate and reliable**" (11D.1);
documented policies and procedures for the valuation process "including the description and
definition of **roles and responsibilities of the personnel involved with the valuation, the
relevant models, and the sources of information** to be used" (11D.2); the ability, **on PRA
request, to undertake an external, independent valuation or verification** of material assets and
liabilities (11D.3); sufficient resources "to develop, calibrate, approve and review valuation
approaches used for solvency purposes"; and internal control processes providing "**an independent
review and verification on a regular basis of the information, data, and assumptions which are
used in the valuation approach, its results, and the suitability of the valuation approach**",
plus oversight by the persons who effectively run the firm (11D.4).

### 15. The With-Profits Actuary and the actuarial senior management functions [R93][R94]

**15.1 With-Profits Actuary duties (Actuaries 5.1).** An actuary appointed to the With-Profits
Actuary function must: (1) **advise the firm's management, at an appropriate level of seniority,
on key aspects of the discretion to be exercised** affecting the classes of with-profits business
for which appointed; (2) **advise the firm's governing body as to whether the assumptions used to
calculate the future discretionary benefits within the technical provisions under Technical
Provisions 9.1 are consistent with the firm's PPFM**; (3) **at least once a year, report to the
governing body on key aspects (including the firm's application of its PPFM) of the discretion
exercised** in the period; (4) request such information and explanations as reasonably necessary;
(5) **advise the firm as to the data and systems he reasonably considers necessary to be kept and
maintained**; and (6) for certain friendly societies, act as appropriate actuary under the
Friendly Societies Acts.

**15.2 The functions.** **Chief Actuary function = SMF20**, "the function of having responsibility
for **the actuarial function specified in Conditions Governing Business 6**" (Insurance – Senior
Management Functions 7.1). **With-Profits Actuary function = SMF20a**, "the function of having
responsibility for advising the governing body of a firm transacting with-profits insurance
business on **the exercise of discretion** affecting part or all of that business, as described
more fully in **Actuaries 5.1**" (8.2), applying only to firms carrying on with-profits business
(8.1). Both are PRA senior management functions requiring individual PRA approval (2.1, 2.2).
Conflicts: the appointed actuary must not perform the Chief Executive function; the With-Profits
Actuary must not be a member of the governing body; and neither may perform any other function
giving rise to a significant conflict of interest (Actuaries 4.1).

**15.3 Prescribed responsibilities (Insurance – Allocation of Responsibilities 3.1).** The two
that bind this stream: **PR Q — "responsibility for the production and integrity of the firm's
financial information and its regulatory reporting"** (3.1(4)); and **PR T2 — "responsibility for
performance of the firm's ORSA"** (3.1(7)). Each must be allocated to an approved senior manager.

### 16. External audit of the SFCR [R96][R96b]

**16.1 Scope of the audit (External Audit 2.2).** The "relevant elements of the SFCR" are:
(1) the information disclosed under **Reporting 3.3(5)(d), 3.4, 3.4A, 3.5A, 3.5B, 3.6B, 3.7A to
3.7C**, and Chapter 3A Articles 7A(1)(d) and 7A(1)(e); and (2) the templates **IR.02.01.02,
IR.12.01.02, IR.17.01.02, IR.22.01.21, IR.22.01.22, IR.23.01.01, IR.23.01.04, IR.25.04.21,
IR.25.04.22, IR.28.01.01, IR.28.02.01 and IR.32.01.22**. Two carve-outs: information that "is, or
derives from, the SCR" is audited **only for firms using the standard formula** (2.2(3)), and the
same for the group SCR (2.2(4)). So a **life internal model firm's SCR disclosures are not
audited**, but **IR.12.01.02 (life technical provisions) and the section D.2 narrative are**.

**16.2 The auditor's duties (External Audit 4.1).** (1) undertake a **reasonable assurance
engagement**; (2) produce a report including "an opinion addressed to the **governing body**
confirming that the relevant elements of the SFCR are prepared **in all material respects** in
accordance with the PRA rules on which it is based"; and (3) read and consider the rest of the
SFCR "to identify **material inconsistencies** with the relevant elements … and any knowledge
obtained during the course of the audit". The report must be prepared "with due skill, care and
diligence" (4.3), submitted to the PRA and **disclosed publicly with the firm's SFCR** (3.1(2)).

**16.3 The small-firm exemption and its arithmetic (External Audit 1.3).** The Part applies only
to a firm that is **not** a "small firm for external audit purposes". That term is defined by a
**score**:

```
score = general_insurance_GWP  * 6.71e-7
      + general_insurance_BEL  * 3.97e-8
      + life_insurance_GWP     * 3.11e-7
      + life_insurance_BEL     * 1.18e-8
```

with each of the four components **floored at zero** and all four inputs expressed in **pounds
sterling** (non-sterling reporters convert at the Bank of England daily spot rate applicable on
the "as at date" of the reporting). For financial years ending on or after 15 November 2019, a
firm is a **small firm for external audit purposes** where "(a) its score is **less than 100 for
its two most recent financial year ends**; or (b) its score is greater than 100, if the financial
year end to which the score relates **immediately follows** a financial year end in which that
firm met the condition in (a)" — i.e. a one-year grace period on first crossing the threshold. A
**small group** is one in which every UK Solvency II firm is a small firm. The definitions in 1.3
were last amended **21/10/2025**.

The two life inputs are defined **by template cell**:
- **life insurance best estimate liability** = `IR.12.01.01 R0030/C0070` **minus**
  `IR.12.01.01 R0030/C0040` (annuities stemming from non-life) **minus** corporate pensions
  business reported under `IR.14.01.01 C0180`;
- **life insurance gross written premium** = `IR.05.03.01 R0030/C0070` **minus** corporate
  pensions business under `IR.14.01.01 C0060`;
where "**corporate pensions business**" means "one or more pension schemes managed by an insurer
on behalf of an employer and for which **liabilities are calculated by the insurer only at scheme
level**" (1.3). This is a rare instance of a UK prudential threshold defined directly on
liability-model output cells.

**16.4 SS11/16 expectations** [R96b]. Governing body: must take responsibility for the SFCR being
properly prepared, be satisfied the firm complied in all material respects throughout the year and
that it is reasonable to believe it will continue to comply, and **sign the SFCR with a written
acknowledgment of responsibility attached** (§§2.1–2.3). Assurance level: **reasonable assurance**
per ISA (UK) 200 (§3.1); ISA (UK) 720 applies to the unaudited remainder (§3.5); compliance with
ISAs (UK) is "the primary means by which auditors will be able to demonstrate that they have
complied with the External Audit Part" (§4.1). Approvals, waivers and supervisory determinations
are **not** opined on but are "part of the framework against which the audit opinion is being
given", and "**for the purposes of transitional measures on technical provisions, Pillar 1 and 2
assets, liabilities and capital calculated in accordance with the previous regime, should be
treated as part of the framework**" (§3.4). On the matching adjustment (§§4.2A–4.2F): the **scale**
of the MA is in scope because "the impact of the MA on technical provisions falls within the
relevant elements", and because Reporting 3.4(1)(b)'s change-to-zero quantification is itself a
relevant element; but **auditors "are not required to assess whether a firm meets the eligibility
conditions for use of the MA"**. The SS also records that the PRA "**does not approve the firm's
calculation methodology**" as part of the MA application process and may review it under s55M
FSMA.

### 17. Model governance and validation expectations [R97]

From SS17/16 (February 2024 text; **superseded from 31/12/2024 — re-verify paragraph numbers**):
- **Justification and validation are distinct** and the demarcation must be visible in
  implementation (7.1). Justification sits under the Statistical Quality Standards in Solvency
  Capital Requirement – Internal Models 11 and 16.2; "**it is not the aim of the validation
  process to create a substitute for these requirements**" (7.3), and justification may be
  discharged by the first or the second line.
- **Validation** is "a **regular and independent** (from the development and operation of the
  model) process which includes reviewing the model in terms of the **appropriateness of its
  specifications, the correspondence of its results against experience and its overall performance
  over time**" (7.4, citing Internal Models 14).
- The PRA expects "**a combination of detailed 'bottom-up' testing and 'top-down' ownership by
  boards**" (7.6) with clear evidence of how boards oversee and influence the design of the
  validation process, how findings are summarised and reported to them, and how they track
  validation issues to resolution.
- Boards must evidence that they have "**challenged the validation process and its results;
  understood and satisfied itself on the key assumptions and limitations of the model; considered
  the possible quantification of these limitations; and taken appropriate mitigating actions**"
  (7.8), and must actively track progress on key issues (7.9).
- "A comprehensive validation process should put specific attention on those **key assumptions and
  expert judgments that have a material impact on the model** and should also articulate **how the
  sensitivity to the key assumptions and expert judgement are being assessed and taken into account
  in the decision process**" (7.12).
- SS1/24 covers, per its publication page, the probability distribution forecast for partial
  internal models, including new risks, **data used in the internal model**, the **model validation
  process**, **validation tools**, **documentation standards** and **minimum content of the
  documentation** (Solvency Capital Requirement – Internal Models 10 to 16A) [R97b] — content
  otherwise **[unverified]**.
- **Model drift** [R97c]: defined as "the risk that capital requirements calculated using an
  internal model may, over time, become **less reflective of the risks to which firms are
  exposed**" (SS15/16 §2.1); monitored against **standard formula SCR, pre-corridor MCR, net
  written premium and best estimate liabilities** (§2.3), with different tools for life and
  general insurance (§2.3A). Solvency Capital Requirement – Internal Models **3.4** requires an
  estimate of the standard formula SCR **on PRA request** (§3.3); the routine annual SF.01 return
  was withdrawn for life internal model firms from the 31 December 2025 reference date [R87 ¶1.22].

### 18. Solvent exit planning [R98]

- **The rule (Preparations for Solvent Exit 2.1, in force 30/06/2026):** a firm must (1) prepare
  for solvent exit so that, if the need arises, it can effect one in an orderly manner;
  (2) **produce a "solvent exit analysis" and update it whenever a material change has taken place
  that may affect its preparations, and at least once every three years**; (3) if a UK Solvency II
  firm in a group, take into account the implications of, and any risk arising from, being part of
  the group; and (4) be able to provide the current version to the PRA **on request**.
- **Definitions (1.3):** "**solvent exit**" = "the process through which a firm ceases its
  insurance business **while remaining solvent**"; "**solvent exit analysis**" = "a document
  setting out a firm's preparations for solvent exit"; a "**passive run-off firm**" (excluded by
  1.2) is one that has ceased effecting contracts of insurance, whose Part 4A permission for
  effecting contracts has been cancelled, and which is not a run-off acquirer.
- **SS11/24:** applies to all PRA-regulated insurers except passive run-off firms, UK branches of
  overseas insurers and Lloyd's managing agents (1.2). Routes to solvent exit include run-off, sale
  or partial sale, merger, **a Part VII FSMA transfer**, a scheme of arrangement and/or
  restructuring plan, or a combination (1.3). Chapter 2 covers the content of the solvent exit
  analysis — solvent exit actions, **solvent exit indicators**, potential barriers and risks,
  resources and costs, communications, governance and decision-making, and assurance; chapter 3
  covers producing a **solvent exit execution plan (SEEP)** and executing an exit. HM Treasury
  indicated in August 2023 that it planned to legislate for an **Insurance Resolution Regime**, and
  "the PRA will consider the need for amendments to this policy when an IRR is enacted" (1.2).

---

## Model hooks

What a UK liability cash flow projection must produce for each reporting, disclosure or
governance requirement — at what granularity, on what basis, at what date.

| Requirement [R#] | What the liability model must produce | Granularity / basis / timing |
|---|---|---|
| **IR.12.01.01 / .02 life technical provisions** [R84 Art 11(1)(a), Art 6(1)(h)][R89] | Gross best estimate split **direct business vs reinsurance accepted**, including technical provisions as a whole; reinsurance/SPV/finite-re recoverables **before and after** the counterparty-default adjustment; risk margin; the five TMTP components Ar/Br/Cr/Wr/Tr; and six sensitivity amounts (BE subject to, and TP without, the interest-rate transitional, the volatility adjustment and the matching adjustment) | Six line-of-business columns (**with-profit participation / index-linked and unit-linked / life annuities / annuities from non-life / other life / health**) plus total; segmentation by **substance not legal form**, unbundling multi-risk contracts; **gross of reinsurance**; **quarterly and annual**; quarterly may use simplified methods (Art 6(2)) |
| **IRR.12.01.01** [R84 Art 18(1)(c)] | The same, but only rows R0025–R0030, R0080–R0100, R0140–R0200 | **Per ring-fenced fund, per matching adjustment portfolio, and for the remaining part**, each with a stable fund/portfolio number used consistently across all templates; annual |
| **IR.12.01 unit-linked rows** [R89] | **Surrender value** net of tax, charges and policy loans, including non-guaranteed surrender values, after duration-based penalties and **assuming deferral clauses do not bite**; **nominal value of units allocated, allowing for actuarial funding / discounting of initial/capital units**; **matching value of units held** (tying to IR.02.01 R0220 and R0340) | C0020 (index-linked and unit-linked) only; per reporting date; three distinct quantities the model must carry separately from the BEL |
| **IR.14.01.01 life obligations analysis** [R89] | Per product: number of contracts in force at year end, number of new contracts in year, gross written premiums, gross claims paid, gross best estimate, and **capital at risk per SCR–SF 7.8 / 7.10** | **Per three-digit PRA product code**, per fund, per Solvency II line of business, per country above 10% of TP or premiums; annual; direct + accepted reinsurance, **ceded excluded**; scheme business counted per member (workplace) or per scheme (corporate) |
| **IR.12.04.01 assumptions** [R89] | The **current-year valuation basis, the prior-year valuation basis and five years of the firm's own experience** for: mortality by sex and smoker status; mortality trend; individual and bulk annuitant mortality by sex; critical illness claim rates; income-protection inception and termination rates; lapse/surrender by product and duration band; pension transfer rates; **GAR take-up**; complete expectation of life at 50/65/80 by sex with and without improvements; **per-policy renewal expense unit costs by product**; expense inflation; and total implied renewal expense for the following year | Percentages of a **named table** (e.g. "AM92", "AM92 adjusted", "reinsurer"), with the **CMI projection parameterisation in CMI notation**; up to three sub-categories by source of business, largest first, subject to a **≥200 claims p.a.** credibility guideline; annual; only if gross BEL > £50m or gross written premiums > £10m |
| **IR.12.05 / IRR.12.05 value of bonus** [R90] | Bonuses added at date of claim (interim/terminal), **market value reductions as negative clawback**, cash bonuses, **discounted value of reversionary bonus additions computed per COBS 20.2.17R**, other bonuses; and the derived shareholder transfer `bonus × s/(1−s)` with brought-forward and carried-forward deferred transfers | Split policyholder / shareholder columns; **whole firm if a single WP fund, else per with-profits ring-fenced fund and the remaining part**; annual; only if net WP BEL > £500m |
| **IR.12.06 / IRR.12.06 WP liabilities and assets** [R90] | **With-profits benefits reserve** (retrospective asset shares and prospective reserve, separately, with permanent past and current miscellaneous surplus); the six FPRL components — **future cost of contractual guarantees (floored at zero), non-contractual commitments, financial options (GARs, cash options), smoothing (may be negative), financing costs, other** — less **planned deductions for guarantees/options/smoothing** and for other costs; total WP BEL; achieved investment returns split taxable/non-taxable; and the asset mix by CIC code backing WPBR and FPRL separately | Per with-profits fund; annual; **R0150 must equal IR.12.01.01 R0030/C0010** |
| **IR.05.03.01 / .02 life income and expenditure** [R90] | The full life revenue account: written premiums gross/ceded/net; **investment income and realised+unrealised gains for index-linked and unit-linked business only**; claims incurred = claims paid + change in outstanding-claims provision; expenses split **acquisition commission, other acquisition (incl. DAC movement), renewal commission, administrative, investment management, claims management, overhead**; interest payable; taxation; transfers in/out; **shareholder transfers and unit management charge transfers (IRR only)**; dividends | **Financial-accounting basis**, not Solvency UK; same six LoB columns; **year to date**; quarterly (reduced row set) and annual; per ring-fenced fund and remaining part on IRR.05.03 |
| **IR.05.10.01 excess capital generation** [R90] | A **three-year forward projection on the business plan** of: own funds generation and SCR run-off and risk margin run-off, each split **current backbook vs planned new business**; TMTP run-off; new-business own funds / risk margin / SCR strain on a discrete-year basis; experience, economic and other operating variances; management actions, assumption changes and model changes; portfolio transfers, **shareholder transfers from with-profits funds**, debt and equity movements and dividends; opening and closing own funds, SCR and excess capital; and premiums split savings & investments / individual pensions / corporate pensions / protection / annuities | Entity level; **one actual year + three plan years**; annual; only if life premiums excluding unit-linked exceed £1bn; must reconcile to IR.23.01.01 and to IR.14.01.01 premium categories |
| **MALIR 3 liability cash flows** [R91] | **Monthly liability cash flows out to month 600**, gross of reinsurance, on the base-MA basis, split into **level/fixed-escalation claims, inflation-linked claims, expenses and other**, with the post-50-year tail discounted back to month 600 at the basic risk-free rate; plus each stream's present value **on the basic RFR** and **on basic RFR + MA** | **Per matching adjustment portfolio**; effective date **31 December** regardless of financial year end; £m; 130 business days after year end via BEEDS; contracts with any inflation linkage are reported **wholly** as inflation-linked |
| **IRR.22.02.01 MA cash-flow projection** [R91] | Annual buckets R0010–R0450 of **longevity/mortality/revision benefit outflows**, **expense outflows**, **de-risked asset cash flows**, and **positive and negative undiscounted mismatches reported separately without netting** | Per PRA-approved matching portfolio; years counted as 12-month periods from the reporting reference date; annual |
| **IRR.22.03.01 MA calculation** [R91] | Single effective discount rates on the assigned-asset value basis and on the basic-RFR basis; the MA in basis points as a decimal; **the increase in gross best estimate under the mortality stress used for the MA eligibility test**; best estimate of inflation-dependent cash flows; **Macaulay-equivalent liability duration**; and the surrender experience block (BE of contracts surrendered in the year, number of surrender options exercised, value of covering assets, amount actually paid) | Per matching portfolio; annual; R0050 (sub-investment-grade FS uplift) **zero from 31 December 2024** |
| **SFCR section D.2** [R84 3.4A(2)][R85] | Technical provisions **by material line of business** with best estimate and risk margin shown separately; the bases, methods and main assumptions; **a description of the level of uncertainty**; the Solvency-UK-vs-accounts difference explanation; the **without-transitional / without-TMTP quantification** on TP, SCR, MCR, basic own funds and eligible own funds; reinsurance recoverables; **material assumption changes since the prior period**; and the significant simplified methods used, including for the risk margin | Annual public disclosure; **thousands of units**; ≤ 70 business days after financial year end; governing-body approved before disclosure |
| **SFCR MA/VA disclosure** [R84 3.4] | **The impact of setting the matching adjustment (and volatility adjustment) to zero** on technical provisions, SCR, MCR, basic own funds and eligible own funds — i.e. a full re-run of the liability valuation and capital stack with MA = 0 | Annual; plus the **MA attestation disclosure** required by Matching Adjustment Chapter 11 [R2] |
| **SFCR section C.7 risk sensitivity** [R84 3.3C(5)] | The methods, assumptions and **outcome of stress testing and sensitivity analysis for material risks and events** | Annual, per risk category |
| **CGB 3.2 / 3.3 long-term-guarantee sensitivities** [R92] | Regular re-runs giving the sensitivity of technical provisions and eligible own funds to (a) the **risk-free curve extrapolation assumptions**, (b) the **MA calculation assumptions including the fundamental spread**, (c) **changes in the assigned asset portfolio composition**, (d) **the effect of a forced sale of assets on eligible own funds**, and (e) **MA (and VA) reduced to zero**; plus, where zeroing would breach the SCR, an analysis of restorative measures | Submitted **annually** as part of Reporting 2 information; the model must therefore support re-valuation under alternative discount bases and alternative asset assignments |
| **CGB 3.1(3) liquidity plan** [R92] | A **liquidity plan projecting incoming and outgoing cash flows** for the assets and liabilities subject to the MA or VA | Any firm using MA or VA; ongoing |
| **ORSA** [R92 3.8–3.12][R95] | A **forward-looking multi-year projection** (SS19/16 §5.2: "a three to five year forecast") of overall solvency needs, own funds by tier, SCR and MCR, **computed both with and without the MA, VA, risk-free-rate transitional and TMTP** (3.8(4)); the deviation of the risk profile from the SCR assumptions; a wide range of **plausible stress tests**, **sensitivity tests identifying key model assumptions and parameters**, and **reverse stress tests defining what constitutes business failure**; the methods and main assumptions used; and a quantification of significant risks not in the SCR | Solo (and group where applicable); at least annually and **without delay after any significant change in risk profile**; report to the PRA **within 10 business days of concluding the ORSA**; board-approved; PR T2 accountable |
| **Actuarial function report** [R92 6.6, 6.9] | A **reasoned analysis of the reliability and adequacy of the technical provisions and of the sources and degree of uncertainty**, **supported by a sensitivity analysis of the technical provisions to each major underlying risk**; a comparison of **best estimate against experience** (observed values vs the estimates underlying the best estimate); an explanation of **material year-on-year differences** in the technical provisions calculation; an opinion on premium sufficiency including the impact of options and guarantees and anti-selection; and an opinion on reinsurance adequacy including **expected cover under stress scenarios** and the recoverables calculation | To the governing body, **at least annually**; must document all tasks and results and identify deficiencies with remedies; SMF20 accountable |
| **Technical provisions validation** [R92 11B] | Validation of data, grouping, data-limitation remedies, approximations, assumption adequacy and realism, method adequacy, and the level of technical provisions — **separately for each homogeneous risk group, separately for best estimate vs risk margin vs replicating-portfolio TP, separately for MA business, and separately for gross BE vs reinsurance recoverables**; plus an assessment of the impact of **changes in future-management-action assumptions** | **At least annually**, and whenever there are indications that data, assumptions, methods or the level of TP are no longer appropriate |
| **Technical provisions documentation** [R92 11C] | A **data directory** (source, characteristics, usage); the collection/processing/application specification; a justification of any inconsistent use of data over time; **a directory of all relevant assumptions including future management actions**, with justification, inputs, objectives and appropriateness criteria, **material limitations**, review processes, and **a justification of period-on-period assumption changes with an estimate of the impact of material changes** | Maintained continuously; the natural home of a reference model's assumption register |
| **External audit inputs** [R96] | `IR.12.01.01 R0030/C0070`, `IR.12.01.01 R0030/C0040`, `IR.14.01.01 C0180` (corporate pensions), `IR.05.03.01 R0030/C0070` and `IR.14.01.01 C0060` (corporate pensions) — the five cells that drive the **audit-exemption score** | Annual, in GBP; the model must be able to isolate **corporate pensions business** (liabilities calculated only at scheme level) from the rest |
| **Solvent exit analysis** [R98] | A documented analysis of solvent exit options including **run-off of policyholder liabilities**, solvent exit actions and indicators, barriers and risks, **resources and costs**, and how all other liabilities are met while policyholder liabilities run off | Updated on material change and **at least every three years**; available to the PRA on request; rules in force **30 June 2026** |

---

## Product applicability

`x` = the item directly binds; `(x)` = qualified or conditional; `?` = the source does not settle
it; `—` = expressly does not apply; blank = not indicated.
Products: TA = term-assurance, CI = critical-illness, IP = income-protection, WOL = whole-of-life,
WP = with-profits, ULB = unit-linked-bond, PA = pension-annuity.

| Item [R#] | TA | CI | IP | WOL | WP | ULB | PA |
|---|---|---|---|---|---|---|---|
| Reporting Part generally — annual + quarterly QRTs, deadlines [R84] | x | x | x | x | x | x | x |
| IR.12.01 / IRR.12.01 life technical provisions [R84][R89] | x | x | x | x | x | x | x |
| IR.12.01 unit-linked rows R0300 / R0302 / R0304 [R89] | — | — | — | (x) | (x) | **x** | (x) |
| IR.12.03 life BEL by country [R84] | x | x | x | x | x | x | x |
| **IR.12.04 best estimate assumptions** [R84 Art 21A(3)(a)][R89] | **x** | **x** | **x** | **x** | **x** | **x** | **x** |
| **IR.12.05 / IRR.12.05 value of bonus** [R84 Art 21A(3)(b),(4)][R90] | — | — | (x) | (x) | **x** | (x) | (x) |
| **IR.12.06 / IRR.12.06 WP liabilities and assets** [R84][R90] | — | — | (x) | (x) | **x** | (x) | (x) |
| **IR.14.01 life obligations analysis (product codes)** [R89] | x | x | x | x | x | x | x |
| IR.05.03 / IRR.05.03 life income and expenditure [R90] | x | x | x | x | x | x | x |
| IR.05.05 life premiums and claims by country [R84] | x | x | x | x | x | x | x |
| **IR.05.10 excess capital generation** [R84 Art 9(1)(k)][R90] | (x) | (x) | (x) | (x) | (x) | — | (x) |
| IR.22.01 long-term guarantee and transitional impact [R84] | (x) | (x) | (x) | x | x | (x) | **x** |
| IR.22.04 interest-rate transitional; IR.22.07 VA by currency [R84] | (x) | (x) | (x) | (x) | (x) | (x) | (x) |
| **IRR.22.02 / IRR.22.03 MA portfolio cash flows and calculation** [R91] | — | — | (x) | — | (x) | — | **x** |
| **MALIR 1–7 (MA asset and liability information return)** [R84 Art 18A][R91] | — | — | (x) | — | (x) | — | **x** |
| IR.26.03 SCR life underwriting risk [R84] *(stream 2 owns the calculation)* | x | (x) | (x) | x | x | x | x |
| IR.26.04 SCR health underwriting risk [R84] *(stream 2)* | — | ? | **x** | — | — | — | — |
| IR.30.06 / IR.30.07 / IR.30.08 life outwards reinsurance [R84] | x | x | x | x | (x) | (x) | (x) |
| IR.28.01 MCR (long-term business only) [R84 Art 15] | x | x | x | x | x | x | x |
| SFCR disclosure templates (Ch 3A Art 4) [R84] | x | x | x | x | x | x | x |
| SFCR D.2 technical provisions narrative [R84 3.4A(2)][R85] | x | x | x | x | x | x | x |
| **SFCR 3.4 MA/VA zero-impact and MA attestation disclosure** [R84] | — | — | (x) | — | (x) | — | **x** |
| External audit of relevant SFCR elements [R96][R96b] | x | x | x | x | x | x | x |
| CGB 6 actuarial function (all nine tasks) [R92] | x | x | x | x | x | x | x |
| CGB 11B / 11C validation and documentation of TP [R92] | x | x | x | x | x | x | x |
| CGB 1A expert judgement [R92] | x | x | x | x | x | x | x |
| **CGB 3.2 / 3.3 MA and VA sensitivities incl. forced-sale effect** [R92] | — | — | (x) | — | (x) | — | **x** |
| **CGB 3.1(3) MA/VA liquidity plan** [R92] | — | — | (x) | — | (x) | — | **x** |
| CGB 3.8–3.12 ORSA [R92][R95] | x | x | x | x | x | x | x |
| **Actuaries 5.1 / SMF20a With-Profits Actuary** [R93][R94] | — | — | (x) | (x) | **x** | (x) | (x) |
| Actuaries 2.1 / SMF20 Chief Actuary [R93][R94] | x | x | x | x | x | x | x |
| Preparations for Solvent Exit + SS11/24 [R98] | x | x | x | x | x | x | x |

**PRA product-code mapping (from the IR.14.01 appendix, [R89])** — the exact codes each library
product must report under:

| Library product | PRA product ID code(s) |
|---|---|
| term-assurance | **404** level term regular premium; **414** level term single premium; **424** decreasing term regular premium; **434** decreasing term single premium |
| critical-illness | **444 / 454** accelerated critical illness, guaranteed / reviewable premiums; **464 / 474** stand-alone critical illness, guaranteed / reviewable premiums |
| income-protection | **494 / 504** income protection, guaranteed / reviewable premiums; **514** single premium; **524** income protection **claims in payment**; (480 CWP and 481 Holloway UWP for the participating forms) |
| whole-of-life | **104** whole of life OB NP (non-profit); **102** whole of life OB UL; **100 / 101** whole of life OB CWP / UWP; 105 / 106 industrial branch |
| with-profits | **111** single premium bond UWP (the with-profits bond); **100 / 101** whole of life CWP / UWP; **120 / 121** endowment OB CWP / UWP; **200 / 201**, **210 / 211** participating pensions |
| unit-linked-bond | **112** single premium bond UL (**113** if index-linked, **114** if non-profit) |
| pension-annuity | **724** individual pension annuity NP; **734** individual enhanced pension annuity NP; **720 / 722** individual pension annuity WP / UL; (700 / 704 purchased life annuity; 710 / 714 individual deferred annuity; **754** bulk purchase pension annuity — out of this library's scope) |

**Notes on the matrix**

- **IR.12.04 is marked `x` for every product** because the threshold in Article 21A(3)(a) is a
  **firm-level** test (gross BEL > £50m *or* gross written premiums > £10m for long-term business
  other than reinsurance), not a product test — and once in scope, the template has dedicated
  rows for term assurance lapses, critical illness claim rates, income-protection inception and
  termination, investment-bond surrenders, with-profits endowment lapses, annuitant mortality and
  annuity renewal unit costs. Every one of the seven products has at least one row of its own.
- **The with-profits templates carry `(x)` outside WP** because IR.12.05 / IR.12.06 are triggered
  by the firm's **with-profits** net BEL, and any of the other products **written in participating
  form** (whole of life CWP/UWP, participating income protection, unit-linked-bond's UWP sibling,
  with-profits pension annuities, code 720) falls into the with-profits fund and therefore into
  the WPBR and FPRL decomposition. The IR.12.06 row R0090 "future costs of financial options such
  as **guaranteed annuity rates**" is the specific place a WOL/WP contract's GAR is reported, and
  IR.12.04 row R1250 is where its take-up assumption is reported.
- **IR.05.10 is `—` for ULB** because the scope test is on "life premiums **excluding unit-linked
  premiums**" [R84 Art 9(1)(k)]; a pure unit-linked-bond book cannot bring a firm into scope, even
  though — once in scope for other reasons — the template covers the whole entity. The `(x)` marks
  on the other products record that the trigger is entity-level, not product-level.
- **MA-related rows (`IRR.22.02`, `IRR.22.03`, MALIR, SFCR 3.4, CGB 3.1(3), CGB 3.2)** are `x` for
  PA and `(x)` for IP and WP. The `(x)` is the **eligible element** route recorded at [R2]: the
  guaranteed element of a with-profits immediate or deferred annuity and the **in-payment element
  of an income protection policy** may enter an MA portfolio even where the whole contract does
  not qualify. IP claims in payment have their own product code (**524**), which makes the split
  reportable.
- **IR.26.04 SCR health underwriting risk is `?` for CI.** The instruction files verified here do
  not settle whether stand-alone critical illness is a health (SLT) or "other life insurance"
  obligation; IR.12.01 requires segmentation by **substance not form** and IR.14.01's line-of-
  business list is a closed list the firm applies itself. Accelerated critical illness written as
  a rider on a life contract will normally follow the base contract into "other life insurance",
  which is why CI carries `(x)` on IR.26.03. **Not resolved by any retrieved document.**
- **IR.22.01 (long-term guarantee and transitional impact) is `x` for PA, WOL and WP** because
  those are the books that carry MA, TMTP and the interest-rate transitional; `(x)` elsewhere
  records that the template is entity-level and will still be filed.
- **Actuaries 5.1 / SMF20a is `(x)` rather than `—`** for WOL, IP, ULB and PA because the
  With-Profits Actuary's remit is "all classes of its with-profits insurance business", so any of
  those products written in participating form is within it.
- **Preparations for Solvent Exit is `x` across the board** — it is a firm-level obligation with
  no product carve-out, excluded only for passive run-off firms [R98].

---

## Gaps and caveats

### Conflicts between retrieved sources — recorded, not resolved

1. **S.13.01 / IR.13.01.** PS3/24 ¶4.70 states, of the life best-estimate cash-flow projection
   template, "The data in these templates remains important to the PRA and **S.13.01 and SR.22.02
   will continue to be collected**" [R86]. But the final Reporting Part contains **no IR.13.01**
   in Chapter 9's inventory, no IR.13.01 requirement in any Article, and no `Section IR.13.01
   instructions` pointer in Chapter 10 [R84]; and the PRA's published instruction library contains
   **no `ir1301` file** among its 83 instruction files [R88]. SR.22.02 *did* survive, as
   IRR.22.02 [R91]. The most likely reading is that S.13.01 was dropped between the near-final
   PS3/24 package and the final PS15/24 instruments, but **PS15/24 itself was not fetched in this
   stream** (it is frozen entry [R6]) and its appendices were not read. **This must be checked
   against PS15/24 Appendix 2 before any downstream document asserts that the UK collects no life
   BEL cash-flow projection.**
2. **The IR.05.10 scope test.** Reporting Part Article 9(1)(k) says the template is required
   "where **life premiums (excluding unit-linked premiums) written in the most recent reporting
   year** exceed £1 billion" [R84]. The IR.05.10 instruction file says it is "required for all
   life insurers, composite insurers, and reinsurers that have reported life premiums (**including
   health business that is similar to long-term business**, but excluding unit-linked premiums)
   greater than £1bn **during any of the three most recent reporting years (this reporting year
   inclusive)**" [R90]. These differ on **both** the measurement window (one year vs three) **and**
   the inclusion of SLT health business. PS3/24 ¶4.10 describes the original proposal as applying
   to "life firms writing non-unit linked premiums exceeding £1 billion **on an annual basis**"
   [R86]. Per the PRA's own hierarchy the Rulebook prevails over the instruction file, but the
   reporting Q&A says only that instructions prevail over the **data point model** [R88c B4] — it
   does not address rule-versus-instruction conflicts. **Unresolved.**
3. **SS41/15 still refers to the abolished RSR.** SS41/15 §6.1 (November 2024 version) instructs
   composite firms to submit their notional-MCR own-funds statement "on an annual basis, **within
   Section E Capital Management of the Regular Supervisory Report, as described in Annex XX of the
   Delegated Regulation**" [R95b]. The RSR requirement **ceased on 31 December 2023** [R86 ¶1.30]
   and the Delegated Regulation was revoked and restated into the Rulebook at 31 December 2024
   [R6]. This is a live, unamended stale cross-reference in a current supervisory statement. Where
   a composite firm should now put that statement is **not settled by any document retrieved**.
4. **SS40/15 carries an unresolved placeholder.** The current (November 2024) SS40/15 PDF is
   headed "This SS is effective from 31 December 2024 and is published as part of **PSX/24**.
   Please see https://www.bankofengland.co.uk/prudential-regulation/publication/2024/**XXXXX**"
   [R85], while its own update annex attributes the November 2024 revision to PS15/24. A drafter
   should cite PS15/24 and note the defect.
5. **SS11/24 internal numbering.** The solvent-exit supervisory statement PDF is headed
   "SS11/24" on its cover and "**SS20/24**" on its page-2 masthead [R98]. The Bank's publication
   pages confirm SS11/24 is the supervisory statement and PS20/24 the policy statement.
6. **Reporting 2.5B(12)(b)** expresses the **group** SFCR disclosure deadline as "100 business
   days after **the firm's** financial year end", whereas the parallel group reporting deadlines
   at 2.5B(6), (7) and (9) are measured from **the group's** financial year end [R84]. Recorded as
   read; not resolved.
7. **SS19/16 version divergence.** Two versions are simultaneously live: November 2024 (effective
   31 December 2024, PS15/24) and May 2026 (effective 31 December 2026, PS13/26) [R95]. Both were
   retrieved. Only the scope sentence was diffed; **a paragraph-level diff was not performed**, so
   any paragraph number cited from SS19/16 should be checked against the version whose effective
   date applies.

### Not retrieved, or retrieved only in part

- **The XLSX template files themselves were not retrieved for any template.** Everything in
  "Extracted mechanics" comes from the instruction ("LOG") PDFs [R89][R90][R91]. Column and row
  *labels* are therefore verified, but the **physical grid** (which cells are blocked out, the
  exact column count of IR.12.05/12.06, the row list of IR.05.03's C-columns) is not. The
  reporting Q&A notes that "there are some cells in IR.05.04 which are blocked out in the Rulebook
  template which are open in the taxonomy" and that firms need not populate blocked cells [R88c
  F2] — so template-vs-taxonomy divergence is real and unquantified here.
- **MALIR 4 (Portfolio Output), MALIR 5 (Matching Tests), MALIR 6 (Assets – Further Info) and
  MALIR 7 (Reconciliation) were not read** beyond their titles and the common header material
  [R91]. MALIR 5 in particular will contain the quantitative matching tests a PA model must pass;
  **this is the single largest unread block in the stream.**
- **The PS18/26 replacement MALIR instruction files (MA.00.01, MA.00.02, MA.01.01, MA.02.01,
  MA.03.01) were not retrieved** [R87]. Everything said about MALIR here describes the
  **2024–2026** form of the return; from the 31 December 2026 reference date the structure
  changes and moves to XBRL.
- **The current (November 2024) SS17/16 PDF was not retrieved.** Two guessed media URLs returned
  HTTP 404 and the publication page's PDF links are script-rendered. The chapter-7 validation text
  quoted is from the **February 2024** version, which is stamped superseded from 31 December 2024
  [R97]. Paragraph numbers must be re-verified.
- **SS1/24 was retrieved only as a publication page**; its substantive expectations on data used
  in internal models, validation tools, documentation standards and minimum documentation content
  are **[unverified]** [R97b].
- **SoP6/24 (reporting waivers) was retrieved only as a publication page** [R88b]. The actual
  waiver categories, the application process and the templates most commonly waived are
  **[unverified]**. This matters: the Reporting Part no longer carries size-based quarterly
  exemptions in the rule text and instead defers to **s.138A FSMA directions**, so the practical
  reporting burden on a small UK life insurer **cannot be stated from the Rulebook alone**.
- **PS15/24 [R6] and its appendices were not fetched in this stream.** It is the instrument that
  created Reporting Part Chapters 2A/3A/9/10 and published all five supervisory statements cited
  here. Anything in this file about *why* a template exists rests on PS3/24 [R86], which is
  **near-final**, not final.
- **The Bank of England Insurance Taxonomy artefacts** (data point model, annotated templates,
  data dictionary, validation deny lists, known-issues log) were **not retrieved**, only their
  version history from the hub page [R88]. Reporting 16.1–16.2 of SS40/15 makes the DPM and the
  published validation rules binding expectations [R85], so a model that must actually file will
  need them.
- **The PRA Solvency UK reporting schedules** (December and non-December year-end calendars,
  referenced at [R88c A3]) were **not retrieved**; only the business-day counts in Reporting 2.5B
  are stated here, never a calendar date.
- **Third-country branch reporting (Articles 37–50), group reporting (Articles 22–36), Lloyd's
  reporting (Chapter 7, Article 21A(6)) and the liquidity templates (Articles 51–54A) were read
  only at the article-title and template-code level.** They are out of scope for this library's
  seven UK retail products but are not fully documented here.
- **IR.12.03 (life best estimate liabilities by country), IR.16.01 / IR.16.02 (annuities stemming
  from non-life), IR.26.03 (SCR life underwriting risk), IR.30.06 / IR.30.07 / IR.30.08 (life
  outwards reinsurance), IR.23.01 (own funds) and IR.25.04 (SCR) instruction files were not
  retrieved** — their URLs are recorded at "Extracted mechanics" §2 but their contents are
  **[unverified]**. IR.26.03 and IR.25.04 belong to stream 2; IR.30.06–08 would matter to any
  reinsurance-ceded modelling.
- **Conditions Governing Business Chapters 2A, 5, 7, 8, 9, 10, 11, 11E and 12 were not read.**
  Chapter 5 (internal audit) and Chapter 7 (outsourcing) in particular are part of the "system of
  governance" a full treatment would cover.
- **The Insurance – Fitness and Propriety Part was not retrieved**, though CGB 2.2(3)(c) makes it
  part of the system of governance and SFCR section B.2 requires disclosure against it.
- **The EIOPA Set 2, System of Governance and ORSA Guidelines themselves were not retrieved**,
  only the PRA's instruction to comply with them proportionately [R95b] and SS19/16's citation of
  **Guideline 10** [R95]. Since SS41/15 §2.2 makes the whole guideline set a live UK expectation,
  the underlying guidelines are a genuine hole.
- **PPFM requirements** are referenced by Actuaries 5.1(2) [R93] but the PPFM rules themselves sit
  in FCA COBS 20 [R9] and were not re-read in this stream.
- **SS8/24** is cross-referenced by the IR.12.01 instructions as the source of a permitted
  in-year risk-margin calculation approach [R89]; **SS8/24 was not retrieved** and its title is
  not asserted here.
- **SS26/15** (ORSA and the ultimate time horizon, non-life) and **SS38/15** (consistency of UK
  GAAP with the Solvency II Directive) are cross-referenced by SS19/16 and SS41/15 respectively
  [R95][R95b]; neither was retrieved.

### Numbers deliberately not transcribed

- **No template cell values, validation rule identifiers or taxonomy entry-point names** are
  stated in this file beyond those quoted verbatim from the instruction files. The single
  validation rule mentioned in the Q&A (BV0237, on the IR.05.04 / IR.16.01 tie) is recorded as an
  example of a **known defect** under review [R88c C1], not as a rule to implement.
- **The liquidity reporting thresholds** in PS15/25 Chapter 2 — which decide the "subset of larger
  UK Solvency II firms" in scope — were **not transcribed**; only the scope statement and the
  30 September 2026 implementation date are recorded [R87].
- **Fee tiers, taxonomy version numbers beyond those listed, and any BEEDS operational parameters**
  are not stated.

### Questions the retrieved documents do not settle

1. **What UK line of business stand-alone critical illness belongs to** (health vs other life),
   and therefore whether IR.26.04 or IR.26.03 applies. The templates require segmentation "by
   substance" and leave the classification to the firm [R89].
2. **Whether a firm must file IR.12.05/IR.12.06 (entity level) or IRR.12.05/IRR.12.06 (fund
   level) when it has exactly one with-profits ring-fenced fund but is not itself a single
   with-profits fund.** Article 21A(3)(b) requires the entity-level templates only where "the firm
   **is** a single with-profits fund"; Article 21A(4) requires the fund-level ones where the
   firm-wide net WP BEL exceeds £500m [R84]. The instruction files say the same thing in different
   words [R90]. The boundary case is not addressed.
3. **What replaces the RSR for narrative supervisory information** that the RSR used to carry
   (e.g. the composite own-funds statement at SS41/15 §6.1). Nothing retrieved answers this.
4. **Whether the "base MA" used in MALIR 3 is the same MA reported at IRR.22.03 C0010/R0060.** The
   MALIR instructions consistently say "used in the calculation of the **base MA**" without
   defining "base"; IRR.22.03 says "matching adjustment to the risk free rate for the reported
   portfolio" [R91]. The relationship (and any MAIA-related second MA) is **not defined in any
   retrieved document**; SS7/18 [R8] is the likely home.
5. **Whether the excess-capital-generation template's "own funds generation" is intended to be
   net or gross of tax**, and how it interacts with the IR.05.03 taxation line. The instructions
   give qualitative examples only [R90].
6. **The exact scope change made to SS19/16 by PS13/26** beyond the removal of third-country
   branches from the addressee list [R95].

### Fetch behaviour observed on 2026-08-06

- **prarulebook.co.uk** served all eight requested Parts at HTTP 200 with a browser User-Agent
  (Reporting 989,845 bytes present view / 1,071,104 bytes future view; Conditions Governing
  Business 355,375; Insurance – Senior Management Functions 221,346; Insurance – Allocation of
  Responsibilities 190,115; Actuaries 107,831; External Audit 94,830; Preparations for Solvent
  Exit 55,295).
- **bankofengland.co.uk** served all requested instruction PDFs, policy statements and
  publication pages at HTTP 200 with the same User-Agent. **HTTP 404s were returned** for four
  guessed media URLs (`.../supervisory-statement/2024/ss1716-november-2024.pdf`,
  `.../2016/ss1716-november-2024.pdf`, `.../2024/ss1916-november-2024.pdf` and
  `.../2024/ss1516-september-2025.pdf`) and for three guessed publication-page slugs
  (`solvency2-orsa-ss`, `solvency2-applying-eiopas-set2-…`,
  `solvency-uk-post-implementation-reporting-and-disclosure-amendments-policy-statement`); the
  correct URLs were then located by search and re-requested. Every URL printed in this file
  returned **HTTP 200 when requested this session**, except where the entry says otherwise.
- The Bank's publication pages render their PDF links via script, so PDF URLs cannot be harvested
  from the fetched HTML; they must be found by search or guessed and verified.
- No URL on this page is fabricated.
