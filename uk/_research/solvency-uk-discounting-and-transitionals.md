# Solvency UK discounting: risk-free rates, matching adjustment, volatility adjustment and transitionals — research notes

**Stream:** Discounting — the relevant risk-free interest rate term structure, the matching
adjustment (MA), the volatility adjustment (VA), the transitional measure on technical
provisions (TMTP) and the transitional measure on the risk-free interest rate (TMIR)
**Access date for every citation below:** 2026-08-06
**Status:** research notes, not yet merged into
`uk/references/regulatory-and-actuarial-references.md`

---

## Scope and numbering note

This stream owns reference block **R53–R60**. Entries **R1–R38** live in
`uk/references/regulatory-and-actuarial-references.md`, are **frozen**, and are already cited by
the seven UK product documents; nothing below renumbers, restates or duplicates them. Sibling
streams own **R84–R98** (reporting and governance,
`uk/_research/solvency-uk-reporting-governance.md`) and **R99–R113** (accounting and tax,
`uk/_research/uk-accounting-and-tax.md`); where their sources bear on discounting they are cited
as `[R#]` and not re-created.

**Numbers used: R53, R54, R55, R56, R57, R58, R59, R60 — all eight are used. R60b is a lettered
sub-id under R60** (the convention already used as R74b in `us/_research/statutory-accounting.md`
and R88b/R96b in the reporting stream), not a new number. No numbers in the block are spare.

**What this stream owns.** The *discounting* layer only: who produces the risk-free curve and on
what basis; the credit risk adjustment, deep-liquid-transparent (DLT) assessment, last liquid
point and extrapolation to an ultimate forward rate; the matching adjustment in full operative
depth (permission, matching conditions, liability and asset eligibility, "highly predictable"
cash flows, the fundamental spread, notching, attestation, the MA Investment Accelerator, the
breach formula); the volatility adjustment and its mutual exclusivity with the MA; the TMTP
under the simplified regime effective 31 December 2024 and the TMIR. The unifying model hook is
that **one projected liability cash flow vector is discounted on several different curves** and a
model must therefore expose the vector, not only a present value.

**Deliberately left to sibling streams.** The best-estimate cash flow rules themselves —
contract boundaries, expenses, future management actions, policyholder behaviour, segmentation
— belong to stream A (Technical Provisions Part [R1], Technical Provisions – Further
Requirements Part). The SCR, own funds, MCR and the risk margin's own SCR run-off belong to
streams C/D. The reporting templates that carry MA/VA/TMTP figures (IR.12.01 TMTP components
Ar/Br/Cr/Wr/Tr, the MALIR matching-adjustment return, SFCR MA-to-zero disclosure) belong to the
reporting stream and are recorded there [R84][R89][R91]. Accounting treatment of the MA and
transitionals in FRS 103 / distributable-profits terms belongs to the accounting stream
[R99][R104].

**Six retrieval facts that change how this material must be documented**

1. **The MA is now governed by three layers, not one.** HM Treasury's **IRPR Regulations 2023
   (SI 2023/1347)** [R53] set the MA eligibility conditions (reg 4(3)–(9), (11)), the MA
   calculation (reg 5) and the fundamental spread (reg 6), and give the PRA power to add
   conditions (reg 7). The **Matching Adjustment Part** [R2] then adds further conditions and
   replicates regs 5 and 6 verbatim in its Chapter 4 (the Part carries an explicit `[Note:]` to
   that effect). **SS7/18** [R8] carries the supervisory expectation. A drafter must cite the
   *rule* (Matching Adjustment 4.x) for firm-facing obligations, and the *regulation* (IRPR reg
   5/6) where the statutory source matters — the two texts are near-identical and it is easy to
   cite the wrong one. **SI 2023/1347 is a different instrument from SI 2023/1346** [R4], which
   is the Risk Margin SI only.
2. **The Technical Provisions Part no longer contains the MA.** Technical Provisions Chapters 6
   ("Matching Adjustment to the Relevant Risk Free Interest Rate Term Structure") and 7
   ("Calculation of the Matching Adjustment") are **entirely `[Deleted]` with effect from
   30/06/2024** [R1, read as at 05/08/2026]. Any UK text that cites "Technical Provisions 6/7"
   for the MA is describing a repealed rule. What survives in the Technical Provisions Part is
   Chapter 5 (risk-free term structure and extrapolation) and Chapter 8 (volatility adjustment).
3. **The statutory publication duty is quarterly; the PRA in fact publishes monthly.** IRPR reg
   3(1) requires the PRA to publish fundamental spreads and other technical information
   "[e]very quarter" [R53]; the PRA's own technical-information page states it publishes
   monthly, "on or before the eighth working day of the month" [R54]. Record both; do not
   silently harmonise them.
4. **Only two last liquid points can be stated as verified.** The January-2026 DLT assessment
   [R56] verifies in prose that the LLP is **50 years for GBP** and **20 years for EUR**. The
   per-maturity D/L grid in that page did not survive text extraction with a reliable
   column alignment (the GBP row yielded 18 marks against a 20-column maturity header), so the
   **USD and CAD LLPs are recorded as not retrieved**, and no per-maturity DLT flags are
   transcribed. See Gaps.
5. **No UFR value was retrieved.** SoP 1/20 [R55] describes the UFR methodology (¶3.6A4: the PRA
   uses the same methodology as EIOPA's *Report on the Calculation of the UFR for 2024*, takes
   account of long-term real rate and expected inflation, maintains stability, ¶3.6A5: no term
   premium) but states **no numeric UFR**. The numbers live in the monthly "Smith-Wilson
   extrapolation parameters" XLSX [R54], which is a spreadsheet and was not opened. **No UFR,
   alpha/convergence parameter or CRA basis-point value is stated anywhere in this file.**
6. **The TMTP regime that a model must know about is the one effective 31 December 2024.** The
   Transitional Measure on Technical Provisions Part [R3] replaced the legacy
   Solvency-I-comparison recalculation with a deterministic run-off formula in rules 4.2 and
   5.1–5.2, and PS2/24 [R7] **removed the requirement to seek PRA permission for a
   recalculation** and removed the financial resource requirement test (verified from the SS17/15
   update annex [R59]). Firms with a permission variation may still use the "legacy approach"
   [R58 ch.4–5]. TMTP **cannot be applied after 1 January 2032** (TMTP 2.3).

---

## Existing entries (R1–R38, and sibling-stream entries) that bear on this stream

- **[R1] PRA Rulebook — Technical Provisions Part.** Owns the discounting *frame*: best estimate
  = probability-weighted future cash flows discounted at the *relevant risk-free interest rate
  term structure* (3.1). Chapter 5 sets the DLT/extrapolation rules; Chapter 8 the VA; Chapters
  6 and 7 (old MA rules) are deleted. Depth added in "Extracted mechanics" §1 and §7.
- **[R2] PRA Rulebook — Matching Adjustment Part.** The operative MA rulebook (Chapters 1–19 as
  at 05/08/2026, including Chapters 14–19 for the MAIA added 27/10/2025). All MA rule citations
  in this file are to this Part. Depth in §3–§6.
- **[R3] PRA Rulebook — Transitional Measure on Technical Provisions Part.** The TMTP formulae.
  Depth in §9.
- **[R4] SI 2023/1346 (Risk Margin Regulations 2023).** Cost of capital 4%, lambda 0.9, floor
  0.25. Bears on this stream only because the risk margin is the one technical-provisions
  component that TMTP splits out separately (the "risk margin portion", ZA).
- **[R5] PS10/24 — Reform of the Matching Adjustment.** The instrument that created [R2] and
  introduced highly-predictable assets, the eligible element, notching and the attestation.
  Effective 30 June 2024. The deletion of Technical Provisions Chapters 6 and 7 carries the
  date-stamp **30/06/2024** in the Rulebook [R1], so is attributed to PS10/24 — an inference from
  the date, not a statement read in PS10/24 itself.
- **[R6] PS15/24 — Restatement of assimilated law.** Restated the Delegated Regulation into the
  Rulebook; updated SS7/18, SS17/15 and SoP 1/20 and SoP 2/24 to the 31/12/2024 versions used
  here.
- **[R7] PS2/24 — Adapting to the UK insurance market.** The TMTP simplification (default TMTP
  method, no recalculation permission, no FRR test) and the February 2024 SS17/15.
- **[R8] SS7/18 — Solvency II: Matching adjustment.** The version read here is the **October 2025
  PDF** (`.../supervisory-statement/2025/ss718-october-2025.pdf`), published 23 October 2025,
  **effective 27 October 2025**, 81 pages including Appendix 1 "PRA Matching Tests". The single
  densest source for this stream; almost all of §5–§10 below is SS7/18 depth cited to [R8].
  **A future version already exists**: published 29 July 2026, **effective 31 December 2026**,
  following **PS18/26 — Solvency UK: Post-implementation reporting and disclosure amendments and
  Own Funds permissions update**. That future version was **not** read; anything in this file
  could be superseded on 31/12/2026.
- **[R84] PRA Rulebook — Reporting Part** (reporting stream). Reporting 3.4 requires SFCR
  disclosure of the impact of setting the MA (and VA) to zero.
- **[R89] IR.12.01 life technical provisions instruction file** (reporting stream). Requires the
  five TMTP components Ar/Br/Cr/Wr/Tr and the six MA/VA/TMIR sensitivity amounts by line of
  business — i.e. the template is the concrete statement of what "Model hooks" H12 demands.
- **[R91] MALIR (matching adjustment asset and liability information return)** (reporting
  stream). The MA portfolio's asset-and-liability reporting set.
- **[R92] PRA Rulebook — Conditions Governing Business Part** (reporting stream). CGB 3.2(2)
  requires the sensitivity of technical provisions and eligible own funds to *the assumptions
  underlying the MA*; CGB 3.2(2)(c) defines the scenario used to measure "MA benefit" in
  Matching Adjustment 5.5; CGB 1A.1–1A.2 are the expert-judgement controls invoked by Matching
  Adjustment 5.4(3).
- **[R99] FRS 103 / [R104] Companies Act 2006 s.833A** (accounting stream). FRS 103 BC55 lists
  the VA, risk margin and transitional adjustments as prudential items to consider adjusting for
  when building an accounting policy; s.833A(5)(e) deducts the MA portfolio's asset-over-
  liability excess in the distributable-profits formula.

---

## New entries

### A. The statutory layer

#### R53. The Insurance and Reinsurance Undertakings (Prudential Requirements) Regulations 2023 (SI 2023/1347)
- Publisher: legislation.gov.uk (HM Treasury statutory instrument)
- URL: https://www.legislation.gov.uk/uksi/2023/1347
- Doc type: statutory instrument (as amended). Accessed: 2026-08-06. fetched_ok: yes (retrieved
  and read in full for Part 2 Chapter 1; Chapter 2 (risk margin) skimmed only)
- Annotation: The statutory backbone of UK MA law, made 7 December 2023, laid 8 December 2023,
  in force **1 April 2024 for regulation 7 and 30 June 2024 for all other purposes** (reg 1(2))
  — verified from the text, together with the Part/Chapter headings inserted by **SI 2024/1083**
  (The Insurance and Reinsurance Undertakings (Prudential Requirements) (Amendment and
  Miscellaneous Provisions) Regulations 2024) with effect from 1 November 2024 / 31 December
  2024. Verified content: **reg 3(1)** — the PRA must publish, *every quarter*, a fundamental
  spread for each currency, duration, credit quality and asset class it considers appropriate,
  plus such other information as it considers appropriate relating to technical provisions and
  the standard-formula SCR; **reg 4(2)–(11)** — the PRA *must* grant an MA application where the
  conditions in (3)–(9) and (11) are met, being asset assignment (4(3)), assessable credit
  quality (4(4)), maintenance of the assignment over the lifetime (4(5)), separate
  identification/organisation/management (4(6)), cash-flow replication in the same currency
  (4(7)), immateriality of mismatch (4(8)), fixed asset cash flows subject to three carve-outs
  (4(9)(a) non-material risk to matching in a limited proportion, (b) inflation-linked matching
  inflation-linked liabilities, (c) sufficient compensation on a change of cash flows), and
  compliance with s138BA FSMA (4(11)); **reg 5** — the MA calculation (see §4 below); **reg 6** —
  the fundamental spread, including the 30%/35% long-term-average-spread floors, the 30% recovery
  assumption and the 30-year data window; **reg 7** — the rule-making powers under which the
  Matching Adjustment Part adds conditions, the breach reduction, notching adjustments and the
  two fundamental-spread additions. The whole of Matching Adjustment Chapter 4 replicates regs 5
  and 6.
- Products: PA (dominant); WP and IP via the eligible-element route; all products indirectly,
  because reg 3 is the authority for the risk-free curve every liability is discounted on.

### B. The risk-free interest rate term structure

#### R54. Bank of England / PRA — *Technical information for Solvency II firms*
- Publisher: Prudential Regulation Authority (Bank of England)
- URL: https://www.bankofengland.co.uk/prudential-regulation/key-initiatives/solvency-ii/technical-information
- Doc type: standing web publication plus monthly data releases (XLSX). Accessed: 2026-08-06.
  fetched_ok: yes (page text retrieved with a browser User-Agent; the site 403s plain fetchers).
  **The XLSX data files themselves were NOT opened** — see Gaps.
- Annotation: The page through which the PRA discharges IRPR reg 3 [R53]. Verified: technical
  information comprises risk-free rate term structures, fundamental spreads for the MA, and
  volatility adjustments per relevant national market, plus the symmetric adjustment to the
  equity capital charge (SAECC). Publication is **monthly, on or before the eighth working day
  of the following month**; each monthly release contains four files — *Risk-free curves*,
  *Risk-free Volatility Adjustment portfolios*, *Smith-Wilson extrapolation parameters*, and
  *Risk-free Fundamental Spreads, Probability of Default and Cost of Downgrade*. The release
  index was verified as running to **30 June 2026 (published 8 July 2026)** at the access date.
  Verified UK-specific parameters: **from 31 July 2021 the GBP RFR is based on SONIA overnight
  index swap rates with a zero credit risk adjustment**; USD moved to SOFR swaps with zero CRA
  from 1 January 2023; EUR CRA from 1 January 2022 uses Euribor and €STR data. **From 1 January
  2025 the PRA publishes technical information only for GBP, USD, EUR and CAD** (AUD, DKK, SEK
  and NOK ceased after 31 December 2024). CRA "Method 3" (for currencies with insufficient
  IBOR/OIS data and outside the EEA) was reset from 1 October 2023 to a **15bp upward adjustment
  to the uncapped Euro CRA, constrained to the range 10–35bp**; the PRA states Method 3 is not
  currently used for any PRA relevant currency. VA reference portfolios are **updated on 31
  March each year**, with the 31 March 2026 portfolios published; the PRA disclosed a data error
  in the unit-linked reduction factors used before the 31 March 2026 update, estimated to have
  **overstated published VAs by up to 5bp for GBP and up to 1bp for other currencies**, which it
  has corrected prospectively only and has decided not to restate. Two further 2026 changes:
  removal of unit-linked reduction factors for non-GBP currencies (data no longer available
  under the reformed IR.12.01), and **exclusion of MA-eligible life annuity liabilities from the
  GBP VA reference portfolio**.
- Products: all (the curve); PA (fundamental spreads); ULB/WP (VA reference portfolio
  composition and the SAECC).

#### R55. Statement of Policy 1/20 — *The PRA's approach to the publication of Solvency II technical information* (November 2024, updating June 2024)
- Publisher: Prudential Regulation Authority (Bank of England)
- URL: https://www.bankofengland.co.uk/prudential-regulation/publication/2020/the-pras-approach-to-publication-of-sii-technical-information
  (verified to return HTTP 200 on 2026-08-06)
- Doc type: statement of policy (PDF, 11 pages). Accessed: 2026-08-06. fetched_ok: yes (PDF text
  extracted in full)
- Annotation: The methodology behind [R54]. Effective from **31 December 2024** for the November
  2024 changes (which followed PS15/24 [R6] and added the extrapolation and risk-corrected-
  currency-spread sections). Verified content: ¶1.1 the duty derives from **regulation 3 of the
  IRPR Regulations 2023** [R53]; ¶2.1 the PRA adopted EIOPA's end-of-transition-period
  methodology with exceptions, and **since 31 March 2022 applies the 30% long-term-average-
  spread floor only to UK central government and central bank exposures** (no longer to EEA
  exposures); ¶2.1C **the VA equals 65% of the risk-corrected currency spread**; ¶3.1–3.5B the
  choice of "PRA relevant currencies" (materiality to 99% of group technical provisions
  excluding unit-linked, plus any currency inside a UK firm's MA or VA authorisation; three
  months' notice of addition or removal); ¶3.6ZA1–3.6ZA3 the basic RFR is derived from interest
  rate **swap** rates adjusted for credit risk, falling back to government bond rates where swaps
  are not DLT, and the credit adjustment may be zero where the instrument carries negligible
  credit risk; ¶3.6A1–3.6A5 extrapolation (same principles in all currencies; the PRA publishes
  *extrapolated* basic curves and firms with MA permission apply the MA to those; where the VA
  applies, **extrapolation is applied after the VA**; the UFR reflects long-term real rate and
  expected inflation, is kept stable, uses the EIOPA UFR-2024 methodology, and **excludes a term
  premium**); ¶3.6B the long-term average spread averages spreads over the RFR applicable at the
  time, so pre-transition Libor-based spreads are left unadjusted; ¶3.6D–3.6F the DLT volume
  indicators — **average daily notional turnover of at least £45 million and an average daily
  number of trades of at least ten, both measured over one year**, with a ±20% soft buffer to
  damp flip-flopping; ¶3.14 the reference-portfolio spread formula (see §2 below); ¶3.15 the
  risk-corrected portion is computed in the same manner as the fundamental spread under IRPR
  regs 6(1)–(8); ¶3.11A regional governments and local authorities count as **corporate** bonds,
  not government bonds; ¶4.1 the SAECC is published monthly under SCR – Standard Formula 3D12–
  3D14. **No numeric UFR, alpha or CRA is given in this document.**
- Products: all.

#### R56. Bank of England / PRA — *Deep, liquid, and transparent (DLT) assessment for January 2026 implementation*
- Publisher: Prudential Regulation Authority (Bank of England)
- URL: https://www.bankofengland.co.uk/prudential-regulation/key-initiatives/solvency-ii/dlt-assessments-jan26
  (link taken from the technical-information page [R54] on 2026-08-06; the sibling pages
  `dlt-assessments-jan22` … `dlt-assessments-jan25` hold the earlier annual assessments)
- Doc type: web publication with a per-currency maturity table. Published 28 November 2025;
  effective 1 January 2026. Accessed: 2026-08-06. fetched_ok: yes (page text; the tabular grid
  extracted unreliably — see Gaps)
- Annotation: The annual determination of which swap maturities are DLT and therefore where
  extrapolation to the UFR begins. Verified from prose: the assessment rests primarily on
  aggregated interest rate swap data from the **EMIR Trade Repositories dataset for the 12
  months to 31 July 2025**, applying SoP 1/20 [R55]. Reference instruments verified: **GBP =
  SONIA OIS; EUR = Euribor; USD = SOFR; CAD = CORRA**. Verified LLPs: **GBP last liquid point =
  50 years** — the 50-year maturity failed the average-daily-number-of-trades indicator, but the
  PRA retained it on bid-ask evidence, Bank market expertise and year-on-year stability; **EUR
  last liquid point = 20 years** — the trade data would have supported 50 years but the PRA
  retained 20 for stability. USD and CAD LLPs **not retrieved**. The PRA reserves the right to
  reissue the assessment on sustained structural change.
- Products: all (the LLP is where the projected liability cash flows of long-dated business —
  PA, WOL, IP — stop being discounted at market rates and start being discounted at an
  extrapolated rate).

### C. Transitionals

#### R57. PRA Rulebook — Transitional Measures Part (Chapters 10 and 12: the transitional measure on the risk-free interest rate)
- Publisher: Prudential Regulation Authority (Bank of England)
- URL: https://www.prarulebook.co.uk/pra-rules/transitional-measures
- Doc type: rulebook part, read in the "present on 05/08/2026" view. Accessed: 2026-08-06.
  fetched_ok: yes (browser User-Agent; prarulebook.co.uk 403s plain fetchers)
- Annotation: The Part that houses the **TMIR** (the PRA and SoP 2/24 [R58] use the abbreviation
  "TMIR"; the Rulebook glossary term is *risk-free interest rate transitional measure*). Verified
  content: **1.2** defines *admissible insurance and reinsurance obligations* as obligations
  whose contracts were concluded **before 1 January 2016**, whose technical provisions were
  determined under **INSPRU 1.1.16R of the PRA Handbook as at 31 December 2015**, and which are
  **not subject to an MA permission**; renewal of a contract does not create a new contract.
  **10.1** the TMIR may be applied only to admissible obligations and only with a **s138BA FSMA
  permission**. **10.2** the adjustment is calculated per currency as a portion of the difference
  between (1) the interest rate determined under INSPRU 3.1.28R–3.1.47R as at 31/12/2015 and (2)
  the annual effective single discount rate that reproduces the Solvency II best estimate of the
  same obligations. **10.3** that portion **decreases linearly from 100% during 2016 to 0% during
  2032**. **10.4** where the firm uses the VA, leg (2) is computed on the VA-adjusted curve.
  **10.5** a TMIR firm must exclude the admissible obligations from the VA calculation, **must
  not apply TMTP**, and must disclose in its SFCR that it applies the TMIR and the impact of not
  doing so. **Chapter 12** is the phasing-in plan (notify the PRA immediately if the SCR would
  not be met without the TMIR; comply with the SCR by **1 January 2032**; submit a plan within
  two months; report annually). Chapter 11 (Technical Provisions) is **[Deleted]** from
  31/12/2024, the TMTP having moved to its own Part [R3]. Chapters 1–9 are legacy 2016
  transitionals (run-off firms, SFCR deadlines, own-funds grandfathering) and are not relevant to
  a cash flow model.
- Products: pre-2016 back-books only, and only where the firm has no MA permission for them —
  in practice legacy WOL, WP and non-MA annuity business; excluded from PA MA portfolios by
  definition.

#### R58. Statement of Policy 2/24 — *Permissions for transitional measures on technical provisions and risk-free interest rates* (November 2024, updating February 2024)
- Publisher: Prudential Regulation Authority (Bank of England)
- URL: https://www.bankofengland.co.uk/prudential-regulation/publication/2024/february/permissions-for-transitional-measures-on-technical-provisions-and-risk-free-interest-rates-sop
  (the same path **without** the trailing `-sop` returns HTTP 404 — verified 2026-08-06; the
  February 2024 PDF sits at
  https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/statement-of-policy/2024/permissions-for-transitional-measures-on-technical-provisions-and-risk-free-interest-rates-feb-2024.pdf)
- Doc type: statement of policy (PDF, 16 pages). Accessed: 2026-08-06. fetched_ok: yes (PDF text
  extracted in full — the November 2024 version)
- Annotation: Effective **31 December 2024**. Verified: ¶2.1 the PRA "generally will not consider
  new applications for TMTP permission"; ¶2.2 the **only** expected route to a new TMTP
  permission is acquiring a book that already benefits from TMTP (Part VII transfer or 100%
  reinsurance), and such a firm must use the TMTP method — the PRA does not expect to allow a new
  firm the legacy approach. ¶2.2A–2.9C the TMIR permission process: the PRA will approve, vary or
  revoke a TMIR permission by reference to compliance with **Transitional Measures 10.2–10.5**
  [R57], and will revoke where a Transitional Measures 12.4 report shows SCR compliance by 2032
  is unrealistic. ¶2.7–2.8 the arithmetic a transferee must perform to derive its own ZA, ZB and
  C0 from the transferor's Ar, Br and C0 (see §9.4). ¶3.2 the PRA will consider waiving the
  amortisation rule (TMTP 5.2) where applying it would move the firm's **solvency coverage ratio
  by five percentage points or more**, provided the alternative still amortises consistently to
  zero by 1 January 2032. Chapters 4–5 the legacy approach: from 31 December 2024 **no further
  legacy-approach permissions will be granted**; legacy firms must freeze their Solvency I Pillar
  2 methodology as at their last pre-31/12/2024 recalculation, may change best-estimate
  assumptions **only** for market conditions and demographics, must cap the permission to the
  business it covered on 31 December 2024, and must amortise to zero by 1 January 2032 without a
  cliff edge; the materiality criterion for having been granted the legacy approach was again a
  **five-percentage-point** difference in solvency coverage ratio across forward-looking
  scenarios.
- Products: legacy WOL, WP, PA back-books; irrelevant to new business.

#### R59. SS17/15 — *Solvency II: transitional measures on risk-free interest rates and technical provisions* (November 2024, updating February 2024)
- Publisher: Prudential Regulation Authority (Bank of England)
- URL: https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/supervisory-statement/2024/ss1715-november-2024-update.pdf
  (landing page: https://www.bankofengland.co.uk/prudential-regulation/publication/2015/solvency2-transitional-measures-on-risk-free-interest-rates-and-technical-provisions-ss)
- Doc type: supervisory statement (PDF, 15 pages). Published 15 November 2024, effective 31
  December 2024. Accessed: 2026-08-06. fetched_ok: yes (PDF text extracted in full)
- Annotation: The supervisory expectation on both transitionals. Verified: ¶2.1 for the TMIR the
  firm must determine the INSPRU leg so the comparison with the Solvency II annual effective rate
  is *meaningful* — e.g. as the annual effective rate reproducing the INSPRU 1 value as at
  31/12/2015; ¶2.2 with a VA, the Solvency II leg reflects the VA and the obligations are then
  discounted at **basic RFR plus the transitional adjustment, with no VA added on top** (double
  counting). ¶3.6A the base-TMTP calculation must not double-count both actual run-off since the
  last recalculation and the 1/16 linear deduction. ¶3.6B designation of MA-eligible obligations
  to the dynamic portion is **optional and partial** — a firm may designate some, all or none.
  ¶3.6C TMTP is calculated at **overall firm level**, though it may be allocated internally (e.g.
  across ring-fenced funds). ¶3.6D "reporting period" means the periods in which TMTP must be
  reported under the Reporting Part [R84]. ¶3.6E the **Chief Actuary** selects the methodology for
  projecting the risk margin portion and dynamic portion in TMTP 5.2, consistent with Technical
  Provisions – Further Requirements Chapter 27. ¶3.7A–3.8A the transfer-event mechanics and the
  meaning the PRA attaches to ZA, ZB and C0 after a transfer. ¶4.2A–4.2B TMTP is a **range**, not
  a point: the applied deduction may be anywhere between zero and the maximum, and a firm
  applying less than the maximum must disclose both figures and apply the choice consistently
  across QRTs, ORSA and market disclosures. ¶4.2D–4.2E legacy firms must keep the Solvency I
  Pillar 2 and Solvency II best-estimate bases **consistent**, and an assumption change reflecting
  market or demographic experience must not be allowed to increase TMTP benefit. ¶5.1 TMTP
  cannot be applied after 1 January 2032; ¶5.5–5.8 the ORSA must monitor the risk that TMTP runs
  off faster or slower than the underlying liabilities; ¶7.1 the **Chief Actuary oversees** the
  TMTP and TMIR calculation as part of the actuarial function (Conditions Governing Business
  6.1(b) and (e) [R92]).
- Products: legacy WOL, WP, PA back-books.

### D. Matching adjustment — permissions layer

#### R60. Statement of Policy 8/24 — *Solvency II: Matching Adjustment Permissions and Matching Adjustment Investment Accelerator Permissions* (October 2025, updating June 2024)
- Publisher: Prudential Regulation Authority (Bank of England)
- URL: https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/statement-of-policy/2025/sop824.pdf
  (landing page: https://www.bankofengland.co.uk/prudential-regulation/publication/2024/june/solvency-ii-matching-adjustment-permissions-statement-of-policy)
- Doc type: statement of policy (PDF, 22 pages). Accessed: 2026-08-06. fetched_ok: yes (PDF text
  extracted in full; read closely for Chapters 1, 2, 2A, 3)
- Annotation: How a firm actually obtains, varies and loses the permission that Matching
  Adjustment 2.1 [R2] makes a precondition of applying the MA at all. Verified: MA permissions
  are granted by **waiving or modifying PRA rules under s138BA FSMA** so that the firm may apply
  the MA in accordance with **IRPR reg 4(1)** [R53] (¶1.2); the same power varies a permission to
  admit assets with new features, grants MAIA permissions and revokes either. Verified process
  facts: where evidence is sufficient and the need for clarification limited, the PRA expects to
  **determine an application no later than six months from the date of receipt** (¶2.29, repeated
  at ¶3.2), with a **streamlined review** track for applications limited in extent and novelty, in
  which the PRA limits its review to specified items and firms may propose safeguards such as
  exposure limits (Chapter 3); firms are expected to use the published s138BA permission
  application form. Verified on the MA/MAIA interaction: **a MAIA permission is not possible
  without an MA permission** (¶1.4 fn 1), and the PRA **does not expect an initial MAIA
  application to be submitted at the same time as an initial MA application**, because such a firm
  would have no experience of managing an MA portfolio (¶2A.5); revocation grounds for MAIA
  include **failure to apply to regularise MAIA assets within 24 months** of inclusion (¶2A.18).
  Verified on breach: where a firm cannot restore compliance with the MA eligibility conditions
  within two months, **the MA is reduced proportionately by 10% for each further month or
  part-month of non-compliance** (¶2.36 — the SoP's plain-English statement of the Matching
  Adjustment 13.5 formula), and the PRA expects to use its revocation power where a breach is
  significant, compliance cannot be restored in a reasonable period after the two-month window,
  **the firm's MA is zero**, or breaches are repeated (¶2.38).
- Products: PA primarily; WP and IP where an eligible element is placed in the portfolio.

#### R60b. PS17/25 — *Matching Adjustment Investment Accelerator*
- Publisher: Prudential Regulation Authority (Bank of England)
- URL: https://www.bankofengland.co.uk/prudential-regulation/publication/2025/october/matching-adjustment-investment-accelerator
- Doc type: policy statement. Accessed: 2026-08-06. fetched_ok: **no** — the URL cited in the
  SS7/18 footnote (…/october/matching-adjustment-investment-accelerator-policy-statement)
  returns HTTP 404; the URL above was recovered from a web search and the page body extraction
  failed. Its existence, date and effect are nevertheless verified from primary documents.
- Annotation: Verified indirectly and reliably: the **MA Part Chapters 14–19 all carry the rule
  date-stamp 27/10/2025** [R2], the SS7/18 October 2025 update annex records that the SS "has
  been updated to reflect the PRA's final policy on Matching Adjustment Investment Accelerator …
  set out in the publication of Policy Statement (PS17/25)", adding paragraphs 1.6–1.7 and a new
  Chapter 10 [R8], and the MA Part's "Legal Instruments that change this Part" panel lists
  PS17/25 [R2]. The PS itself is **not** the source of any number in this file; every MAIA
  number below comes from [R2], [R8] or [R60].
- Products: PA.

---

## Extracted mechanics

Notation throughout is plain text. `CF(t)` is the projected best-estimate liability cash flow at
time `t`; `r_basic(t)` the basic (unadjusted) risk-free spot rate for term `t`; `MA`, `VA`, `TMIR`
scalar additions to that curve expressed as annual effective rates.

### 1. The relevant risk-free interest rate term structure

**1.1 Where the requirement sits.** Technical Provisions 3.1 [R1] requires the best estimate to
be "the probability-weighted average of future cash-flows … discounted at the *relevant risk-free
interest rate term structure*". The Rulebook does not compute that structure: IRPR reg 3(1)
[R53] obliges the PRA to publish it, and the PRA does so through the technical-information
release [R54]. A UK firm has **no discretion over the curve** for a PRA relevant currency; SoP
1/20 ¶3.6 [R55] leaves the firm responsible for proposing technical information only where it
has liabilities in a currency the PRA does not publish, and **a VA can only be applied in a
currency for which the PRA publishes a VA**.

**1.2 The three published curve variants.** Each monthly release [R54] contains:
- the **basic risk-free curve** per currency — this is the "basic relevant risk-free interest rate
  term structure" referred to in Matching Adjustment 4.3(2) [R2];
- a **VA-adjusted curve** per currency, for firms with a VA permission;
- **fundamental spreads, probabilities of default and cost of downgrade** by currency, duration,
  credit quality step and asset class — the inputs a firm needs to compute its own MA; and
- **Smith-Wilson extrapolation parameters** (the file name is verified; its contents were not
  opened).
The MA is *never* published: the PRA publishes the FS, and the firm computes its own MA from its
own assigned assets (§4).

**1.3 Construction of the basic curve** [R55 ¶2.1A–2.1B, ¶3.6ZA1–3.6ZA3]:
1. Derive rates from **interest rate swap rates** in the currency, adjusted for credit risk.
2. Where swap rates are not available from a DLT market for a maturity, use **government bond
   rates**, adjusted for credit risk, where those are DLT.
3. The **credit risk adjustment (CRA)** reflects the credit risk inherent in the reference
   instrument and **may be zero** where that risk is negligible.
4. The curve is built separately for each currency and maturity, on the assumptions that firms
   can earn the rates risk-free in practice and that the rates come from DLT markets.

**1.4 UK-specific reference instruments and CRAs** [R54][R56], all verified:

| Currency | Reference instrument | CRA | Effective from |
|---|---|---|---|
| GBP | SONIA overnight index swaps | **zero** | reference dates from 31 July 2021 |
| USD | SOFR swaps | **zero** | 1 January 2023 |
| EUR | Euribor / €STR data | not retrieved | 1 January 2022 |
| CAD | CORRA | not retrieved | (DLT assessment for 1 January 2026) |

"Method 3" CRA (currencies with insufficient IBOR/OIS data, outside the EEA) = **uncapped Euro
CRA + 15bp, floored at 10bp and capped at 35bp**, from 1 October 2023; the PRA states no PRA
relevant currency currently uses Method 3 [R54]. PRA relevant currencies from 1 January 2025 are
**GBP, USD, EUR, CAD only** [R54].

**1.5 The DLT assessment and the last liquid point.** Technical Provisions 5.1 [R1] requires the
curve to take account of instruments of maturities where the markets for those instruments *and
for bonds* are deep, liquid and transparent, and to be **extrapolated only** for maturities where
they are not. The **DLT assessment** determines that boundary. Verified quantitative criteria
[R55 ¶3.6D–3.6E]:
- average **daily notional turnover >= GBP 45 million** measured over one year; and
- average **daily number of trades >= 10** measured over one year;
- a previously liquid maturity must fall **at least 20% below** one threshold to be reclassified
  illiquid; a previously illiquid maturity must meet **both** thresholds and exceed one by
  **at least 20%** to be reclassified liquid. These are soft thresholds; the PRA may also use
  other metrics and expert opinion.
The 2025 assessment [R56] was run on EMIR Trade Repository swap data for the 12 months to
**31 July 2025**, published **28 November 2025**, effective **1 January 2026**. Verified outcomes:
**GBP LLP = 50 years** (retained despite failing the trade-count indicator, on bid-ask evidence
and stability grounds); **EUR LLP = 20 years** (retained, although the data would have supported
50). USD and CAD LLPs were **not reliably extracted** and are not stated here.

**1.6 Extrapolation.** Technical Provisions 5.2 [R1]: beyond the last observable DLT maturity the
curve is built from **forward rates converging smoothly** from the forward rates at the longest
observable maturities **to an ultimate forward rate (UFR)**. SoP 1/20 [R55] adds: the same
principles apply in every currency (¶3.6A1); the PRA publishes **already-extrapolated** basic
curves and firms with MA permission apply the MA to those (¶3.6A2); where the VA is used,
**extrapolation is applied after the VA** (¶3.6A3); the UFR reflects long-term real interest rate
expectations plus expected inflation, is kept stable and changed only when long-term expectations
change, and uses **EIOPA's UFR-2024 methodology** (¶3.6A4); the UFR **contains no term premium**
(¶3.6A5). **No numeric UFR, convergence period or Smith-Wilson alpha was retrieved** — see Gaps.

**1.7 Consequence for a UK annuity model.** For GBP the market-rate region runs to 50 years, so a
pension-annuity or whole-of-life projection is discounted at observed rates over essentially its
whole term and the UFR bites only on the small tail beyond t = 50. Conversely a EUR-denominated
book is extrapolated from t = 20. A model that hard-codes an LLP therefore hard-codes a currency.

### 2. The volatility adjustment

**2.1 Permission and scope.** Technical Provisions 8.1 [R1]: a firm may apply a VA to the relevant
risk-free curve for the best estimate **only** if (1) it holds a **volatility adjustment
permission** (defined in Technical Provisions 1.2 as a s138BA FSMA permission), (2) the VA has
been published by the PRA under **IRPR reg 3** [R53], and (3) only to the extent of that
permission.

**2.2 Interaction with extrapolation.** Technical Provisions 8.2: the VA **must not be applied to
the risk-free rates derived by extrapolation** under Chapter 5. Technical Provisions 8.3: where a
firm applies a VA, **the extrapolation itself must be based on the VA-adjusted rates**. Read
together with SoP 1/20 ¶3.6A3 ("the PRA will apply extrapolation *after* applying the volatility
adjustment to the basic RFR") the operative meaning is: the VA is added to the *liquid* segment,
and the extrapolation then converges to the UFR from the VA-adjusted liquid forwards — the VA is
not superimposed on the extrapolated segment. **Record 8.2 and 8.3 together; quoted in isolation
8.2 reads as a flat prohibition it is not.**

**2.3 Mutual exclusivity with the MA.** Technical Provisions 8.5 [R1]: a firm with a VA permission
**must not apply the VA to obligations whose relevant risk-free curve already includes an MA**.
The mirror rule is Matching Adjustment 13.3 [R2]: a firm applying the MA to a portfolio of
obligations **must not apply a risk-free interest rate transitional measure or a volatility
adjustment in respect of those obligations**. The two adjustments are therefore mutually
exclusive **at the level of the obligation**, not the firm — one entity may run an MA portfolio
and a VA-discounted remainder simultaneously.

**2.4 How the PRA derives the VA** [R55]. For each relevant currency:

```
VA  =  0.65 * risk_corrected_currency_spread                                   (SoP 1/20 2.1C(b))

risk_corrected_currency_spread
    =  S  -  (portion of S attributable to expected loss, unexpected credit
              risk or other risk of the assets)                               (3.13)

S   =  w_gov  * max(S_gov, 0)  +  w_corp * max(S_corp, 0)                      (3.14)
```
where `w_gov` is the value share of government bonds (**central governments and central banks
only**) in the currency's reference portfolio, `S_gov` the average currency spread on those,
`w_corp` the value share of non-government bonds, loans and securitisations, and `S_corp` their
average currency spread. The deducted portion is computed **in the same manner as the fundamental
spread under IRPR regs 6(1)–(8)** [R55 ¶3.15][R53] — i.e. the VA and the MA share a
risk-correction concept. Bonds issued by **regional governments and local authorities are treated
as corporate**, not government (¶3.11A).

**2.5 The VA reference portfolio (RP)** [R55 ¶3.7A–3.12][R54]. The RP is representative of the
assets, denominated in that currency, in which firms invest to cover the best estimate for
obligations in that currency. It must contain bonds, securitisations and loans (including
mortgage loans), equity and property; collective investment undertakings are looked through, with
the simplifying assumption that duration, sector and rating inside CIUs match those outside
(¶3.10). GBP RPs are derived from **UK solo QRT data**; non-GBP RPs are a market-value-weighted
average of EIOPA's published RPs and RPs derived from UK parent-undertaking plus Lloyd's QRT
data (¶3.9). **The PRA publishes no country-specific VA RPs** (¶3.11). RPs are updated
**annually, effective the 31 March following publication**, with at least three months' notice
(¶3.12).

**2.6 Two 2026 changes and one admitted error** [R54], all verified:
- the PRA identified an error in the **unit-linked reduction factors** used in VA RP derivation
  before the 31 March 2026 update; on 31 March 2025 data it estimates correction would have
  **reduced published VAs by up to 5bp (GBP) and up to 1bp (other currencies)**. It judged the
  effect immaterial, corrected prospectively from 31 March 2026, and **will not restate** earlier
  published VAs (including 31 January and 28 February 2026, which still use the 2025 RPs);
- for **non-GBP** currencies the PRA removed unit-linked reduction factors entirely and now
  approximates non-linked reduction factors using data covering both unit-linked and non-linked
  liabilities, because reformed template IR.12.01 [R89] no longer supplies the split;
- for **GBP** the PRA now **excludes MA-eligible life annuity liabilities** from the VA RP, on
  the ground that firms cannot use the VA and MA simultaneously.

### 3. Matching adjustment — permission and eligibility conditions

**3.1 The permission gate.** Matching Adjustment 2.1 [R2]: "A *firm* must not apply a *matching
adjustment* to the *relevant risk-free interest rate term structure* to calculate the *best
estimate* … unless it has a *matching adjustment permission*." The permission is a **s138BA FSMA
waiver/modification** of the technical-provisions rules, granted so the firm may apply the MA in
accordance with **IRPR reg 4(1)** [R60 ¶1.2][R53]. Matching Adjustment 3.2: a firm that applies
the MA to a portfolio **must not revert** to the non-MA approach. Matching Adjustment 3.1: the
application must confirm and evidence that the asset portfolio, the obligation portfolio and,
where relevant, the firm satisfy the MA eligibility conditions.

**3.2 The statutory conditions** — IRPR reg 4 [R53], which the PRA **must** grant on:

| Reg | Condition |
|---|---|
| 4(3) | assign a portfolio of assets consisting of **bonds or other assets with similar cash flow characteristics** to cover the best estimate of the obligation portfolio |
| 4(4) | asset credit quality must be **assessable via a credit rating or an internal credit assessment of comparable standard** |
| 4(5) | **maintain the assignment over the lifetime** of the obligations, except to maintain replication where expected cash flows have materially changed |
| 4(6) | the obligation portfolio and the assigned assets must be **identified**, and **organised and managed separately** from the firm's other activities |
| 4(7) | the assets' expected cash flows must **replicate each of** the obligations' expected cash flows **in the same currency** |
| 4(8) | any mismatch must **not give rise to risks material** relative to the risks inherent in the business |
| 4(9) | asset cash flows must be **fixed and not changeable** by issuers or third parties, except (a) where risks to matching quality are not material and only a limited proportion the PRA determines is affected, (b) inflation-linked assets matching inflation-linked liabilities, (c) where **sufficient compensation** is paid to secure an equivalent cash flow by reinvesting in an asset of equivalent or better quality |
| 4(11) | the application must comply with s138BA FSMA and the firm with the rules made under reg 7(a) |

**3.3 The additional rulebook conditions** — Matching Adjustment 2.2 [R2], made under IRPR reg
7(a):
1. **2.2(1)** the underlying contracts **do not give rise to future premium payments** (disapplied
   for an income-protection / group-dependant-annuity eligible element by 2.5);
2. **2.2(2)** the only underwriting risks connected to the portfolio are **longevity, expense,
   revision, mortality or recovery time risk**;
3. **2.2(3)** where mortality risk is present, the best estimate **must not increase by more than
   5%** under the mortality stress in 2.4;
4. **2.2(4)** the contracts contain **no policyholder options**, or **only a surrender option
   whose surrender value does not exceed the value of the covering assets** (valued under
   Valuation 2.1–2.2) at the time of exercise;
5. **2.2(5)** the assigned assets **cannot be used to cover losses from other activities**;
6. **2.2(6)** the portfolio and every individual asset in it must satisfy the **prudent person
   principle** (Investments Chapters 2 and 3).

**3.4 The 5% mortality test in full** — Matching Adjustment 2.4 [R2], as amended 31/12/2024. The
stress is the **more adverse for basic own funds** of:
- (a) an instantaneous **permanent increase of 15%** in the mortality rates used for the best
  estimate; or
- (b) an instantaneous increase of **0.15 percentage points** in the mortality rates (expressed as
  percentages) used in the technical provisions to reflect mortality experience **in the following
  12 months**.

The increase applies **only to policies for which it increases technical provisions**; multiple
policies on the same life may be treated as one; and where technical provisions are computed on
groups of policies under Technical Provisions – Further Requirements 20.1, the identification may
be done at group level if not materially different. For reinsurance obligations, the
identification is carried out on the underlying **direct** policies. SS7/18 ¶3.5 [R8] expects
**quantitative evidence** of compliance.

**3.5 Whole-contract rule and its one exception.** Matching Adjustment 2.3 [R2]: obligations of a
contract **must not be split into different parts** when composing the MA obligation portfolio,
**other than in the case of an eligible element**. SS7/18 ¶3.6 [R8] extends the point: outside the
three eligible-element cases the PRA does not regard *any* notional splitting of a contract as
compatible with 2.3, and considers it would undermine separate management under IRPR reg 4(6)(b).

### 4. Liability eligibility, and the "eligible element" route

**4.1 The definition** — Matching Adjustment 1.2 [R2]. An **eligible element** is a portion of
obligations forming part of a wider contract which:
- (1) comprises either
  - (a) **the guaranteed element of a with-profits policy that is either an immediate annuity or
    a deferred annuity**; or
  - (b) **the in-payment element of a group death-in-service dependants' annuity or an income
    protection policy**,
  in each case where the element **can be organised and managed separately** in accordance with
  **IRPR reg 4(6)** [R53]; and
- (2) **would otherwise meet the MA eligibility conditions** but for forming part of a contract
  that does not comply when taken as a whole.

**4.2 The future-premium carve-out.** Matching Adjustment 2.5 [R2]: the "no future premiums"
condition in 2.2(1) **does not apply** to an eligible element under limb (1)(b) — i.e. to
**income protection in-payment claims and group death-in-service dependants' annuities**, but
**not** to the with-profits guaranteed annuity element, which must still be premium-free.

**4.3 Supervisory expectations per route** [R8]:
- **With-profits guaranteed annuity elements (¶3.5A).** The component must be **legally
  established and identifiable as guaranteed within the contract**, separable under IRPR reg
  4(6), and otherwise MA-eligible. The firm must give a **detailed assessment** showing that the
  only elements included are contractually guaranteed and **not dependent on future premiums or
  future investment performance**, and must set out a **clear policy on where future attaching
  bonuses go** (inside the MA portfolio or elsewhere).
- **Income protection (¶3.5B).** *Recovery time risk* — "the risk that policyholders in receipt of
  income protection payments take longer to recover from sickness than expected" — is a permitted
  underwriting risk under 2.2(2). In-payment claims under **both group and individual** IP
  policies may sit in an MA portfolio where the claims are **not subject to future premiums**.
  **There is no exposure limit on recovery time risk** (contrast the 5% cap on mortality risk).
  The PRA states the recovery-time permission is **not** intended to admit any liability type
  other than IP claims in payment.
- **Group dependant annuities (¶3.5C).** In-payment annuities under group death-in-service
  dependants' policies, where separately identifiable, separately manageable and not subject to
  future premiums.

**4.4 Surrender options** [R8 ¶3.8–3.13]. Strong quantitative evidence is expected for 2.2(4). In
assessing surrender risk the PRA expects firms to consider processes and controls, the likelihood
and drivers of peaks and troughs, historical experience, the effect on cash flow matching, and the
liquidity strain. For **deferred annuities with a pre-vesting surrender right**, the absence of a
contract-level surrender basis is **not automatically disqualifying**, but the firm must: identify
contracts whose surrender basis is **non-discretionary or of limited discretion** (footnote 24
defines both) and consider excluding them; demonstrate that no contract could cause a surrender
loss material to the portfolio **including under stress and allowing for correlation between
contracts**; evidence that management of the surrender basis has not historically produced
portfolio-level losses; and describe how the basis is set and controlled. Where one contract
covers many scheme members the assessment is expected **per member/beneficiary**. **¶3.13 — the
PRA's preferred comparison for "surrender value does not exceed the value of the assets" is
surrender value against the BEL**; comparison against BEL + risk margin requires the firm to show
that the MA portfolio's contribution to any surrender pay-out is capped at the assets it holds for
that contract; including the contract's SCR contribution in the cost-neutrality test is
appropriate "only in exceptional circumstances".

**4.5 Premium adjustment clauses** [R8 ¶3.7]. A clause permitting post-inception adjustment of the
initial premium does **not necessarily** create "future premium payments" for 2.2(1), provided it
only corrects an over- or under-payment of a defined premium arising from inaccurate inception
data and does not vary the contract.

### 5. Asset eligibility: fixed, highly predictable, and the exceptions

**5.1 No closed list** [R8 ¶2.2–2.4]. Eligibility is determined by the asset's **features** plus
the firm's ability to identify, measure and manage its risks under the prudent person principle
— **"there is no prescribed 'closed list' of eligible assets for MA purposes"**. Each portfolio is
reviewed case by case in the permission process. Firms must test **all** features against **all**
conditions, not only the ones they judge most material, and must run a **screening process** over
terms, conditions and prospectuses, validating third-party data (¶2.5–2.6).

**5.2 Fixed cash flows** [R8 ¶2.13]. Outside the HP carve-out, the firm must show the remaining
portfolio's cash flows are fixed in timing and amount and cannot be changed by issuers or third
parties. **"[I]t is not sufficient for a portfolio of assets to provide cash flows that are
predictable in aggregate to a very high degree."**

**5.3 Redemption / termination rights** [R8 ¶2.17–2.23]. Early redemption at the issuer's option
does not automatically disqualify an asset. Rights **entirely at the issuer's discretion** do
(subject to the reg 4(9)(c) compensation route). Rights are acceptable where triggered only by
events that are (i) **outside** the issuer's control, (ii) **cannot be avoided** by it, and (iii)
would **materially change the nature or substance** of the obligations — the worked examples are
tax-change redemption on corporate bonds and index-unavailability redemption on index-linked
bonds. Extension-on-default clauses are assessed on the same basis. Reinvestment risk from such
rights is an **ORSA** item.

**5.4 Sufficient compensation — Spens clauses** [R8 ¶2.37–2.44]. For a **standard Spens** clause
(defined in footnote 22 as one where the remaining cash flows are discounted at a **reference gilt
rate**) the firm must show the reference gilt is suitable for the asset's term and that the cash
flows discounted correspond to those used in the matching demonstration. For a **modified Spens /
make-whole** clause, one acceptable method is to set a **maximum make-whole spread**, above which
the asset's cash flows are **not treated as fixed** for matching purposes. Supporting
expectations: assess adequacy at a granular level (asset class alone needs strong justification;
material individual holdings are assessed asset by asset); test explicitly **spread-narrowing and
gilt-spread-widening** scenarios extreme enough to show **negligible risk** of insufficiency;
demonstrate market liquidity, in stress, to buy a same-class same-quality replacement; and
sense-check with a scenario in which **spreads return to historically low levels** over the
available data period. Changes to the sufficiency criteria must be notified to supervision.

**5.5 "Highly predictable" (HP) cash flows** — the operative definition and its cap.
- **Matching Adjustment 5.1** [R2]: assets with cash flows that are not fixed can be included
  without giving rise to material risks to matching quality **only if those cash flows are
  highly predictable**.
- **Matching Adjustment 5.3**: cash flows are *highly predictable* where **(1) the contractual
  terms provide for a bounded range of variability in respect of the timing and amount of the
  cash flows, and (2) failure to meet those contractual terms is a *default***.
- **Matching Adjustment 5.4**: in assessing them the firm must base the best estimate on the
  **contractual payments**, use assumptions **consistent with the economics of the asset**, and
  subject any expert judgement to the controls in **Conditions Governing Business 1A.1–1A.2**
  [R92].
- **Matching Adjustment 5.2 — the cap**: **no more than 10% of the MA benefit** may be
  attributable to an HP asset, on its own or taken together with other HP assets in the portfolio;
  plus any applicable **exposure limit** in the permission.
- **Matching Adjustment 5.5 — what "MA benefit" means for that cap**: the impact on the firm's
  best estimate of the scenario set out in **Conditions Governing Business 3.2(2)(c)** [R92],
  ignoring any reduction under 13.5.
- **SS7/18 ¶2.12A–2.12E** [R8]: contractual bounding means the legal documentation sets a
  **finite range** for timings and amounts — the cash flow profile, the circumstances in which it
  may or must vary, and the amount/timing when it does. An asset can be contractually bounded and
  still be unsuitable: "where very significant variations in cash flows are contractually
  permitted, the asset may not be suitable to match annuity liabilities." Contracts with **no
  upper bound** (e.g. leases with upward-only rent increases) may be bounded by an assumed
  escalation rate, but assuming increases above the contractual minimum requires a matching-risk
  assessment. **Decomposing a single asset into fixed and HP components is not permitted**; an
  asset is treated wholly as one or the other, and moving an asset between the two treatments
  requires permission cover, an FS addition when moving to HP, attestation consideration,
  governance, justification of frequent switching, and consideration of operational consequences
  where holdings of the same asset would be treated differently.
- **SS7/18 ¶8.4** [R8]: exceeding the 10% limit **is a breach of Matching Adjustment 5.2**.
  Remediation may include moving assets between components or in/out of the MA portfolio, or
  applying further FS additions — but **routinely** using FS additions to stay under 10% "may be
  evidence of a failure of the firm's risk management framework".

**5.6 Partial recognition** [R8 ¶2.15–2.16A]. Where an asset produces both fixed and non-fixed
cash flows the firm may treat it as fixed by recognising **only the fixed cash flows** for
matching — the worked example is a callable bond recognised up to first call date. But **the full
market value of the asset is attributed to the MA portfolio and taken into account in the MA
calculation**. Where the full investment is not made at purchase, MA benefit is recognised only if
the portfolio provisions for the future investment sums and those sums enter the liquidity plan
and the matching-risk assessment.

**5.7 Pairing and grouping** [R8 ¶2.8–2.11]. IRPR reg 4(7)'s "same currency" test does not require
each individual asset to be in the liability currency provided replication holds **in aggregate**;
reg 4(3)'s "bonds or other assets with similar cash flow characteristics" can be satisfied by a
pairing — the worked example is a foreign-currency bond plus a currency swap. Firms must be able
to explain whether the elements were de-risked and mapped to fundamental spreads **separately or
as a combined asset** (¶4.12 gives the FRN-plus-swap example), and must consider break clauses
that let a counterparty change cash flows.

**5.8 Reinsurance assets** [R8 ¶2.24–2.26] may be included as assets with **fixed** cash flows —
without using the HP carve-out — where variation in timing/duration/quantum is **solely
attributable to** the underlying obligations covered, replication is without material mismatch
risk, the underlying obligations are themselves properly in the MA portfolio, all other conditions
are met, and inclusion is consistent with the hold-to-maturity assumption. Reinsurance cash flows
are risk-adjusted **on the basis of Technical Provisions 11.1**, using the same adjustment as for
the reinsurance recoverable, and **are not mapped to a fundamental spread**.

**5.9 Equity release mortgages** [R8 ¶2.47]. No general view is possible, but the typical ERM
combination — cash flows depending on **longevity, morbidity, realisable property value (where
there is a No Negative Equity Guarantee) and prepayment risk** — is "unlikely to be compatible
with the general requirement for fixed cash flows (regulation 4(9))". The routes are: satisfy the
HP conditions and sit inside the 10% cap, or **restructure / pair / group** the ERM into an
eligible format. The PRA expresses no preference between restructuring approaches.

**5.10 Cash** [R8 ¶2.48, ¶4.10]. Cash items may be compatible, but **expected future cash
interest** is not, unless paired or grouped with a suitable contract. For matching-test purposes,
**where cash is used to demonstrate matching the cash balance must be assumed realised in full in
year 1** of the projection.

**5.11 Assets whose cash flows depend on other risks** [R8 ¶2.27]. Assets whose cash flows depend
on risks outside the permitted underwriting-risk list are unlikely to qualify as fixed; to be
included at all they must satisfy the HP conditions.

### 6. The MA calculation and the fundamental spread

**6.1 The MA itself** — Matching Adjustment 4.3 [R2], replicating IRPR reg 5(1) [R53]. **Per
currency**:

```
MA  =  R_assets  -  R_liab_basic

R_assets     = the single annual effective discount rate which, applied to the cash flows of the
               MA obligation portfolio, produces a value equal to the value of the portfolio of
               ASSIGNED ASSETS                                                   (4.3(1))

R_liab_basic = the single annual effective discount rate which, applied to the SAME liability
               cash flows, produces a value equal to the BEST ESTIMATE computed on the
               BASIC relevant risk-free interest rate term structure             (4.3(2))
```
Both legs are **internal rates of return on the same liability cash flow vector**; only the target
value differs. Hence the first entry under "Model hooks": the MA cannot be computed from a present
value alone — the model must expose the vector.

**6.2 Which assets count** — Matching Adjustment 4.4 [R2]: *assigned assets* includes **only**
assets whose expected cash flows are **required to replicate** the liability cash flows —
**excluding any assets in excess of that** — and valuations follow the Valuation Part.

**6.3 Asset cash flows are de-risked first** — Matching Adjustment 4.5: the "expected cash-flow"
of an asset is its cash flow **adjusted to allow for the probability of default** corresponding to
the FS element in 4.10(1), or, where no reliable credit spread can be derived from default
statistics, the LTAS portion under 4.11/4.12.

**6.4 The fundamental spread is deducted** — Matching Adjustment 4.6–4.7: the MA **must not
include** the fundamental spread reflecting risks retained by the firm; and the deduction must
include **only the portion of the FS not already reflected** in the adjustment to the assigned
assets' cash flows under 4.3–4.5 (i.e. no double count of the PD element). 4.8: the FS must be
calculated in a **transparent, prudent, reliable and objective** manner, consistent over time,
based on relevant indices where available.

**6.5 The fundamental spread** — Matching Adjustment 4.10–4.15 [R2] = IRPR reg 6 [R53]:

```
FS  =  credit spread for PROBABILITY OF DEFAULT (PD)
     + credit spread for EXPECTED LOSS FROM DOWNGRADE (Cost of Downgrade, CoD)          (4.10)

subject to the long-term-average-spread (LTAS) floor:
  FS >= 30% * average_spread   for exposures to UK central government and the Bank of England (4.11)
  FS >= 35% * average_spread   for all other assets                                          (4.12)
```
where `average_spread` is the long-term average of the spread over the risk-free rate for assets
of the **same duration, credit quality and asset class** as observed in financial markets.
Calculation assumptions, 4.13:
- **(1) recovery on default = 30% of the market value of the assets**;
- (2) PD based on **long-term default statistics** relevant to the asset's duration, credit
  quality and asset class;
- (3) expected loss based on long-term credit-migration statistics; it is the probability-weighted
  loss on downgrade with **immediate replacement**, the replacement asset assumed to have **the
  same cash flow pattern, the same asset class, and the same or higher credit quality**;
- (4) the long-term average spread is based on data for **the previous 30 years**;
- (5) methods must be the same for each currency and country, but may differ between government
  and other bonds.
4.14: where no reliable credit spread can be derived, FS = the 30%/35% LTAS portion. 4.15:
constructed data on prudent assumptions may fill gaps, but must be based on available reliable
data for the previous 30 years. 4.16: the firm **must** add the HP-asset addition under 8.2.
4.17: the firm **may** add further amounts where necessary to cover all retained risks.
SoP 1/20 ¶2.1 [R55] records the UK deviation: **since 31 March 2022 the 30% floor applies only
to UK central government and central bank exposures**, no longer to EEA exposures.

**6.6 The three-layer structure of the FS** — SS7/18 ¶5.7A–5.7C [R8]:
1. the **basic FS** = PD + CoD + LTAS floor, taken from PRA technical information per CQS [R54]
   and **notched by the firm**;
2. **HP FS additions** (Matching Adjustment 4.16 and Chapter 8) — mandatory for HP assets;
3. **firm FS additions** (Matching Adjustment 4.17), including voluntary additions arising from
   the attestation process; these may be applied on top of the basic FS and/or on top of the HP
   addition.
Figure 1 of the SS labels the first layer "technical information published by the PRA and
'notched' by firms" and the second and third "values calculated by firms in line with PRA rules
and expectations", with the LTAS floor applied by **taking the maximum** against PD + CoD. Where
the SS refers to "the FS" it means all three layers unless stated otherwise.

**6.7 Applying the FS in practice** [R8 ¶5.5–5.16]:
- The PRA has **no preferred approach** to reflecting the FS in the MA calculation; one method is
  to extend the 4.3 annual-effective-rate approach so that **all** components (PD, CoD, LTAS
  floor) are allowed for in the same way, not only the PD.
- Assets are mapped to asset classes and CQSs on the **issue rating**; where none exists, an
  internal rating broadly consistent with the issue rating a CRA would have produced, following
  SS3/17.
- **Fundamental spreads vary by maturity of cash flow for a given asset.** "Simplifications, for
  example using a single FS based on the duration of the asset, would be inconsistent with the way
  in which the FSs are intended to be applied in practice" (¶5.10). This applies to both the
  default adjustment and the residual-FS (CoD subject to LTAS floor) deduction.
- Hedging assets in component A are included in **both** the matching tests and the MA
  calculation and are mapped to an FS; but **net payments due from the MA portfolio to a
  counterparty (e.g. under a swap) are not adjusted for default** (¶5.9).
- Where an asset does not correspond exactly to a published class, use the **closest** class and
  justify it in the application (¶5.11).
- Reinsurance: the **cedant must not take credit for MA benefit available to the reinsurer**; MA
  permission does not travel with a cession; a reinsurer needs its own permission (¶5.12–5.13).
- Groups: BEL and consolidated own funds are net of intra-group transactions (Group Supervision
  11.1C); the PRA does **not** consider Group Supervision 11.1D–11.1F to require re-assessment of
  MA eligibility at group level where permission exists at solo level, and considers an adjustment
  to consolidated BEL appropriate to preserve a reinsurer's MA benefit that netting would
  otherwise destroy, provided no intra-group capital creation or double counting results
  (¶5.14–5.16).

**6.8 Notching** — Matching Adjustment Chapter 6 [R2]:
- **6.1**: where an assigned asset has a credit rating (or comparable internal assessment) mapping
  to **credit quality steps 1 to 5 inclusive**, the firm **must** adjust the FS derived from that
  CQS to reflect the corresponding **rating notch**.
- **6.3**: the adjustment must be derived for at least (1) the probability of default referred to
  in 4.5 and (2) the **overall FS**.
- **6.4**: derive it by **linear interpolation of the information published by the PRA** under
  IRPR reg 3(1), interpolating **for each consecutive credit quality step pair**, and assuming
  each intermediate rating notch is **evenly spread** between the two steps.
- **6.5**: where **no rating notch is available**, the firm must **not** adjust the FS (other than
  for the 4.16/4.17 additions) and must consider the appropriateness of the FS and MA for that
  asset in its Chapter 10 analysis for the attestation.
- **6.6**: a derogation allowed non-compliance with 6.1 **from 30 June 2024 to (excluding) 31
  December 2024** only — notching has been mandatory since 31/12/2024.
- **7.4** (effective 01/01/2026): the use of credit ratings in the MA calculation follows **SCR –
  Standard Formula 1A to 1D**.
- SS7/18 ¶5.7B [R8]: the **preferred** implementation is to notch the **CoD and LTAS floor**
  components as well as the PD; the alternative is to notch the basic FS directly, in which case
  the non-PD "residual FS" is a balancing item and cannot be split into CoD and LTAS. ¶5.7A: the
  PRA expects **most (if not all) assets to have a rating available on a notched basis within six
  months** of the asset becoming an assigned asset; where not, the firm must explain why, and the
  attestation must explicitly consider (i) potential bias toward the lower notch within a CQS and
  (ii) whether the lack of notching reflects greater credit uncertainty the FS does not capture.

**6.9 Internal credit assessments** — Matching Adjustment Chapter 7 [R2]. Where used, the firm
must ensure on an ongoing basis that the assessment is of a standard **comparable to a credit
rating** (IRPR reg 4(4)) and that its process and outcomes are appropriate. Minimum requirements
(7.2): all sources of credit risk considered, qualitative and quantitative, and their interaction;
outcomes lying within a **plausible range of issue ratings a CRA could have produced**; broad
consistency and **no bias** at both portfolio and asset-type level; validation and ongoing
appropriateness assessment; **proportionate independent external assurance** of 7.2(2); and an
**independent** internal credit assessment function with conflict-of-interest controls. 7.3: the
firm must be able to demonstrate compliance to the PRA on request.

**6.10 FS additions for HP assets** — Matching Adjustment Chapter 8 [R2] and SS7/18 ¶5.17–5.30
[R8]:
- **8.1** identify **all** sources of uncertainty in the timing and amount of cash flows from every
  HP asset; **8.2** add to the FS an amount reflecting those risks so that the FS covers retained
  risks per 4.6.
- The addition must be set so that the part of the credit spread arising from **borrower
  optionality does not result in recognition of further MA benefit** (¶5.19); for a diversified HP
  portfolio, targeting a percentile of the loss distribution can be an adequate allowance.
- **Minimum allowance for reinvestment/rebalancing costs: the PRA expects 10 basis points to be
  generally adequate in normal market conditions**, and treats this as a **floor**, not a specific
  increment; firms may justify an alternative from their own trading-cost experience (¶5.20).
- Firms **should model a term structure** for the addition unless a uniform allowance can be shown
  not to materially affect adequacy, the matching assessment or the PRA Matching Tests (¶5.21).
- **Standard approach, economic variability** (¶5.23): assume the cash flow pattern giving the
  investor the **minimum yield** ("yield to worst"), retaining economic rationality of the issuer,
  plus the de minimis reinvestment allowance.
- **Standard approach, event variability** (¶5.24–5.25): increase the FS by **at least one quarter
  of the additional MA above the minimum ("worst") MA outcome**, subject to the
  reinvestment/rebalancing floor. The PRA states that one quarter of the median-to-worst
  difference is **broadly equivalent to targeting the 85th percentile of a fatter-tailed
  distribution**. A lower proportion requires credible data. **Worked example (¶5.24C): worst MA
  5bp, best-estimate MA 65bp -> provision = one quarter of 60bp = 15bp**, where that exceeds the
  minimum reinvestment/rebalancing allowance. The minimum MA benefit "would not generally be
  expected to be less than zero".
- Where the worst-case cash flows arrive **earlier** than best estimate, the firm may assume
  reinvestment for the balance of the original term in assets of the **same FS sector and credit
  quality** at a **prudent reinvestment spread**, capped at the spread used for modified-Spens
  adequacy (¶2.39), **less the FS the replacement assets would incur** (¶5.24A, ¶4.10A).
- A firm may express the addition as a fixed number of bps at origination, but must have a
  framework for reassessing adequacy as conditions change; the PRA does **not** expect automatic
  adjustment at every valuation date (¶5.24B).
- More sophisticated methods are permitted, but the PRA **would not expect** a modelled approach
  substantially reliant on expert judgement (¶5.28); a firm may use an advanced method for some HP
  assets and the standard method for others, with justification (¶5.29).
- Under the "sub-portfolio" approach the FS addition may be captured in component A **or**
  component B assets (¶5.30).

### 7. Demonstration of matching: components A/B/C and the five PRA Matching Tests

**7.1 What the firm must demonstrate** [R8 ¶4.2–4.4]. For **IRPR reg 4(7)** (replication) the firm
carries out a **quantitative cash flow-based projection** measuring the surplus or deficit **in
each future period**. For **reg 4(8)** (immateriality of mismatch) it undertakes a quantitative
assessment of the **interest rate, currency exchange rate, inflation rate and other relevant
risks** arising from the mismatch and of their materiality against the risks of the MA portfolio
as a whole. For HP assets it must also demonstrate compliance with **reg 4(9)(a)(i)** — that risks
to matching quality are not material — by quantitatively assessing the mismatch that could arise
from changes in HP payment amounts and/or timing (¶4.3A–4.3B); such mismatches crystallise as
**reinvestment risk or liquidity risk** and must feed the liquidity plan and MA management policy
(¶4.3C). Where liabilities are **significantly longer-dated than available assets, or increase
with an inflation index for which no matching assets exist**, the firm must evidence how it
nonetheless matches under regs 4(7)–4(8) (¶4.4) — this is the standing UK annuity problem.

**7.2 The A/B/C decomposition** [R8 ¶4.5] — "one possible method", not mandatory:
- **component A** — assets whose cash flows replicate the expected liability cash flows **after
  adjustment for the component of the FS corresponding to the probability of default** (taking
  account of differences in credit quality by rating notch where possible and appropriate);
- **component B** — additional assets which, added to A, make the value of A + B equal to the
  **BEL within the MA portfolio when discounted at the risk-free rate plus MA**;
- **component C** — further assets deemed 'surplus' for meeting the best estimate liabilities,
  which may or may not still be needed to demonstrate the other eligibility conditions.
Defaulted assets **should not** be used to match liabilities within component A, and may be
inappropriate in B (¶4.13); firms must develop their own definitions of default and its
consequences, distinguishing e.g. payment default from a technical event of default.

**7.3 Projection conventions for the matching demonstration** [R8 ¶4.10] — these are the model
rules:
- **assume no future management actions** — no entering into derivative contracts at a future
  point, no selling assets to meet cash flow eligibility conditions;
- for assets other than HP assets, **assume all asset cash flows arrive on their contractual
  date**; surplus assets **cannot** be assumed to be reinvested and realised at a future date;
  **cash used to demonstrate matching is assumed realised in full in year 1**;
- for HP assets, use **the same best-estimate projection as in the MA calculation**;
- tests are run **net of reinsurance** in both numerator and denominator, with the matching of the
  portfolio's reinsurance assets and liabilities considered separately (¶4.11);
- the **time-interval frequency must be consistent with the firm's own matching method**;
- the firm must explain its treatment of every asset type (including reinsurance and derivatives)
  and any reinvestment assumptions.

**7.4 The five PRA Matching Tests** — SS7/18 Appendix 1 [R8]. **All firms with MA portfolios apply
Tests 1, 2 and 3; firms holding HP assets in their MA portfolios also apply Tests 4 and 5**
(¶4.6A). Where a firm does not fall within the threshold on any one test it must **notify the PRA
immediately** and show how it will restore compliance with regs 4(7)–4(8) (¶4.8).

| # | Test | Statistic | Threshold | Frequency |
|---|---|---|---|---|
| 1 | **Accumulated Cash Flow Shortfall** | project BEL cash flows and component-A asset cash flows (adjusted for the PD part of the FS) at annual or more frequent intervals; accumulate period surpluses/shortfalls **at the risk-free rate**; take the **highest accumulated shortfall** over all future intervals; compare with the PV of the portfolio's liabilities at the valuation date discounted at the **risk-free rate** | max accumulated shortfall in any interval **<= 3%** of PV of liabilities | monthly if writing new business in the fund, otherwise quarterly |
| 2 | **99.5th percentile 1-year VaR** | undiversified 99.5% one-year VaR of the MA portfolio separately for **interest rate, inflation and currency** risk, capturing the change in value of **both assets and liabilities**; HP assets stressed with cash flows consistent with the scenario; components of a risk aggregated into one number per risk; assets included are those hypothecated to **components A and B**; denominator is the BEL discounted at **basic risk-free rate + MA**; six statistics reported (three capital amounts and three ratios) | each of the three undiversified capital requirements **<= 1%** of the calculated BEL | at least quarterly, in line with SCR calculations |
| 3 | **Notional Swap** | report (a) the notional MA using only the actual component-A assets, in bps; (b) the notional MA after scaling component-A market values **and** PD-adjusted cash flows by a single factor until the PV of future surpluses and shortfalls **discounted at the basic risk-free rate is zero**; and (c) the scaled market value | **no specific hurdle**; the PRA expects an explanation where the scaling factor is **above 100% or below 99%** | at least quarterly |
| 4 | **MA Loss Test for HP assets** | for each HP asset determine the cash flow profile consistent with the contractual terms that gives the **lowest MA benefit**; optionally assume early proceeds are reinvested for the balance of the original term in the same FS sector and credit quality at a prudent spread less the replacement FS; sum the potential MA loss across the portfolio and divide by the MA benefit claimed on **the entire MA portfolio** | max loss of MA benefit **<= 5%** of the MA benefit claimed | monthly if writing new business, otherwise quarterly |
| 5 | **Modified Accumulated Cash Flow Shortfall** | as Test 1, but HP cash flows are **extended to the latest date possible under the contract**, taking credit for any coupons (including coupon step-ups) arising from the extension | max accumulated shortfall in any period **<= 5%** of PV of liabilities | monthly if writing new business, otherwise quarterly |

What the suite is designed to assess (¶4.7): the extent to which firms may be **forced sellers**;
the materiality of mismatch in interest rate, currency or inflation risk; whether firms are
**materially under-matched**; the MA impact if cash flows are received in a manner that reduces
the benefit earnable; and the increase in forced-seller risk where cash flows arrive later or
smaller than expected. ¶4.10B records a known limitation: **the profile minimising MA benefit
under Test 4 need not be the profile producing the greatest reinvestment risk**, and firms should
consider whether a further matching assessment is required. The Appendix opens with a warning that
the PRA has described **other versions of these tests in previous communications** and that the
versions in Appendix 1 are the most recent — so a drafter must date any reference to them.

### 8. The attestation

**8.1 The rule** — Matching Adjustment 9.1 [R2]. A firm with an MA permission must provide the
PRA, **in respect of each relevant portfolio of assets as a whole**, an attestation that as at the
**attestation reference date**:
- (a) the **fundamental spread used in calculating the MA reflects compensation for all retained
  risks** in accordance with 4.6; and
- (b) the **MA can be earned with a high degree of confidence** from the assets held in the
  portfolio.

**8.2 Timing** — 9.1(2): **annually, no later than 14 weeks after the firm's financial year-end**,
commencing with the first year-end after the permission took effect; **and**, where there is a
**material change in the firm's risk profile**, as soon as reasonably practicable after the
applicable reference date. The **attestation reference date** (definition, Matching Adjustment
1.2) is **the effective date of the firm's SFCR** for the annual attestation, or **a date no later
than three months after the date of the material change** for an out-of-cycle attestation. 9.2:
firms whose MA permission took effect **before 31 December 2024** were **not required** (but could
elect) to attest for any reference date falling in the period from 30 June 2024 to (excluding)
31 December 2024.

**8.3 Who signs** — 9.1(3): the **PRA senior management function holder responsible for the
prescribed responsibility for the production and integrity of the firm's financial information and
its regulatory reporting (PR Q)** under **Insurance – Allocation of Responsibilities 3.1(4)**.
SS7/18 ¶5.32 [R8]: "In many cases, this will be **SMF 2, the Chief Financial Officer**", but it may
be another SMF depending on allocation; where **more than one SMF holds PR Q, all of them are
expected to attest**; SS35/15 ¶2.19A on sharing prescribed responsibilities applies. The rationale
given is that the attestor must have ultimate governance responsibility for the FS and MA
calculation and so be able to implement an FS increase.

**8.4 Governance and the policy** — Matching Adjustment Chapter 10 [R2]: before attesting, the firm
must **analyse and justify** both limbs (10.1), have appropriate internal processes, systems and
controls to produce that analysis (10.2), and maintain a **governing-body-approved attestation
policy** (10.3). SS7/18 ¶5.31 [R8] expects the policy to cover: how the attesting SMF was
determined; the **triggers** that may constitute a material change in risk profile for an
out-of-cycle attestation; the process by which the attestor reviews the FS and MA, including
criteria for subjecting assets to more detailed review; and the approach to determining any FS
addition. Example triggers (¶5.33): **a large bulk purchase annuity transaction where the
transferred assets have a materially different profile**; **the merger of two MA portfolios**; **a
significant shift in the economic outlook for assets comprising a material proportion of the
portfolio**. The firm is expected to discuss with the PRA before concluding whether a material
change has occurred and to **agree the reference date and timescale bilaterally**.

**8.5 Form and content** — Matching Adjustment Chapter 12 [R2]. The **attestation document**
contains the 9.1 attestation, the name and role of the attesting SMF, the portfolio it applies to,
and the date of the attestation (12.2). The **supporting attestation report** contains: a copy of
the current attestation policy or confirmation it has not been updated; confirmation that firm and
attestor complied with the policy, or details of the alternative approach and why; **a list
detailing the evidence relied on**; and, for any **voluntary FS increases under 4.17**, a list of
the assets affected, the reasons for the increase, and **the amount of the increase and the MA
resulting from those assets**, as at the reference date (12.3).

**8.6 The review process the PRA expects** — SS7/18 ¶5.35 [R8], a three-step example, with the
overarching instruction that **the FS and the MA must be reviewed independently of each other** so
that the MA acts as a market-based check on the level of FS, and that focus is proportionate,
concentrating on assets with a comparatively high level of MA:
- **Step 1 — assets with a risk profile consistent with the MA assumptions** (e.g. corporate bonds
  or private placements with the same risk characteristics as bonds but untraded). Reliance on the
  basic FS is generally appropriate and an increase is not generally expected, particularly for
  portfolios broadly reflecting the FS calibration data; exceptions to consider are concentration
  relative to that data, idiosyncratic characteristics not represented in it (the SS gives **bonds
  with a maturity exceeding 30 years** as an example), currency differences, rating lags and
  inaccuracies, and factors raising downgrade probability (watchlists, un-notched assets subject
  to potential bias toward the lower notch, materially adverse sector outlook).
- **Step 2 — assets with a risk profile not consistent with the MA assumptions** (internally
  rated, internally valued, privately placed, restructured, or HP rather than fixed). Consider
  retained risks common to Step 1; risks not captured in the rating or arising from high
  uncertainty (political, reputational, conduct, legal, complex or novel features); cash flow
  variability risks against the ¶5.17–5.29 guidance; and, where credit is taken for collateral,
  the collateral's performance risks including illiquidity and reinvestment risk.
- **Step 3 — review all assets and explain (or modify) the MA on material contributors**, using
  clearly articulated metrics. The SS leaves the calibration to the firm with bracketed
  placeholders: the **[w]** biggest contributors to total MA; corporate bonds whose spread is more
  than **[x]** standard deviations from the index mean; illiquid assets with an MA more than
  **[y]** bps greater than an equivalent corporate bond; and corporate bonds or illiquid assets
  where the MA exceeds **[z]%** of the spread. **The PRA does not fill in w, x, y or z.**

**8.7 Granularity and offsetting** [R8 ¶5.36–5.36A]. The FS and MA are considered **asset by
asset**; a firm must **not assume prudence on one asset can offset an insufficient FS on another**.
Initial analysis may group assets into homogeneous risk groups, but HRGs must be defined by at
least: **asset type, sector (financial/non-financial), sub-sector (retail, healthcare, industrial
etc), rating method (internal/external), rating (potentially including notches where the FS
difference is material), broad collateralisation levels and broad maturity bands**.
Portfolio-level considerations include **reduced diversification and increased risk from
concentration** by risk type, asset class or sector, and **rebalancing risk** where the associated
costs deviate from those assumed in the basic FS.

**8.8 Rationalising the residual spread** [R8 ¶5.37–5.39]. The firm must have a **high degree of
confidence that all the residual spread will be earned**, treating the MA as an addition to the
risk-free discount rate of liabilities reflecting **only non-retained risks, e.g. liquidity
risks**, and must target **the same level of certainty across asset types, including HP assets, as
it would for a portfolio of liquid fixed-cash-flow corporate bonds**. Where high residual spreads
are attributed to **origination expertise** (access to private markets, structuring skills), the
firm should consider whether the established asset could achieve a market price reflecting that
value-added, assuming buyers with the same illiquid liability profile. Where attributed to
**ongoing management expertise**, the residual spread may be considered **net of an investment
expense allowance**; where the adjusted residual spread remains materially above the average for
corporate bonds of the same credit quality (the technical information being calibrated on
corporate bonds), the firm must explain the **"relative excess spread"** by reference to
non-retained risks, and consider whether it instead signals additional unidentified risk or
greater uncertainty. The PRA expressly acknowledges "significant judgement and uncertainty in
spread decomposition" and "room for the role of judgement and reasonable differences in views".

**8.9 Consequences and disclosure.** ¶5.34: the PRA does **not** expect its policy to produce a
general increase in the FS applied to all assets, but expects the attestation to narrow the
dispersion of MA where risk and return characteristics do not justify it — and **a voluntary FS
addition applied by a firm would not automatically result in a reduction to its SCR**. Matching
Adjustment 11.1 [R2]: the firm must disclose **in its SFCR whether or not it has provided the
attestation** in respect of that financial year. ¶5.41: the **content** of the attestation report
is directed to the PRA and is **not** publicly disclosed, and the PRA does **not expect auditors
to take the attestation requirement into account** when considering the amount of MA claimed.

### 9. The Matching Adjustment Investment Accelerator (MAIA)

**9.1 What it is.** Effective **27 October 2025** (all MA Part Chapters 14–19 carry that
date-stamp) [R2]. The MAIA lets a firm with an MA permission put assets with features **outside
the scope of that permission** ("new assets") into the MA portfolio and claim MA benefit
immediately, before applying to vary the MA permission [R8 ¶1.1].

**9.2 The rules** [R2]:
- **14.1** a firm must not include any new assets in its portfolio unless it has a **MAIA
  permission** (a s138BA FSMA permission, defined in 1.2).
- **15.2** only a **qualifying new asset** may be included. *Qualifying new asset* (1.2) = a new
  asset that (1) satisfies **all** applicable MA eligibility conditions, (2) has **not previously
  been included in and removed from** the portfolio, and (3) has **not previously been included in
  an MA permission application (or variation) that the PRA refused**.
- **15.3** if a non-qualifying new asset is included, inform the PRA and remove it as soon as
  possible. **15.4** comply with the **MAIA exposure limit** at all times, and ensure ordinary MA
  exposure limits still hold after inclusion. **15.5** notify and remedy any MAIA limit breach.
- **16.2 — regularisation**: within **24 months** of first including a new asset the firm must
  either apply to vary its MA permission to cover it, or remove it as soon as possible. **16.3**
  if the variation application is refused or withdrawn, remove the asset as soon as possible.
- **16.4** where removal or restoration of the limit has not happened **within two months**, the
  firm must inform the PRA, keep remediating, and **apply the 13.5 MA reduction formula monthly**
  for the duration of non-compliance.
- **17.2–17.3** a written **contingency plan for each and every new asset**, kept up to date and
  implemented when removal is required. **18.2–18.4** a **MAIA policy** covering Chapters 14–17
  and 19, including how contingency plans are reviewed, **approved by the governing body**.
  **19.2** a **MAIA use report** to the PRA **annually, no later than 18 weeks after financial
  year-end**, setting out the types of new assets included and how the firm complied with its MAIA
  policy.

**9.3 The exposure limit** — SS7/18 ¶10.20–10.29 [R8]:
- the limit is **absolute**, assessed against the **total nominal investment amount** of MAIA
  assets held (not market value);
- the PRA expects an appropriate limit to be the **lower of (i) 5% of the best estimate liabilities
  of the MA portfolio (after application of the MA), net of reinsurance, at the point of the most
  recent application, and (ii) an amount proposed by the firm no greater than GBP 2 billion**;
- the overall exposure across a group must be **no more than GBP 2 billion or 5% of BEL**;
- "net of reinsurance" excludes reinsured liabilities, including where premium or collateral is
  subject to a **deposit-back** arrangement restricting use of the assets;
- the limit should be **updated with each subsequent MA application** and on significant changes
  in portfolio size; a higher limit is **not generally expected** to be appropriate;
- firms with multiple MA portfolios should consider an **aggregate** limit, whose sum would not
  generally exceed the standard limits; groups containing more than one MA firm are assessed on a
  **cumulative** basis;
- both **amounts invested and amounts committed** count, converted at the **exchange rate at the
  time of initial investment**.

**9.4 Breach and reporting** [R8 ¶10.30–10.35][R60 ¶2A.18]. Breaches of MA 15.2, 15.4 and 16.2
trigger the 16.4 / 13.5 MA reduction from two months after non-compliance. Persistent
inappropriate use may lead the PRA to restrict or remove the MAIA permission; failure to apply to
regularise within 24 months is an express revocation ground. The MAIA use report must cover actual
and expected inflows by asset class, consistency with the MAIA policy, **whether and how the firm
considers the assets productive to the UK economy and/or supportive of the net zero transition**,
applications made and planned, whether contingency plans were implemented, breaches of the policy,
and the circumstances of any non-regularisation outflows. MAIA use also feeds the **MALIR** [R91].

### 10. Breach of the MA eligibility conditions — the reduction formula

**10.1 The rules** — Matching Adjustment 13.2–13.5 [R2]. A firm must comply with the eligibility
conditions and the permission terms, including exposure limits, **at all times** (13.2). On
non-compliance it must **immediately** inform the PRA and take the necessary measures to restore
compliance as soon as possible (13.4). If compliance is not restored **within two months**, then
**monthly, for the duration of non-compliance** (13.5):

```
MA*  =  MA  -  (n - 1) * p * max(MA, 0)

MA*  reduced matching adjustment actually applied
MA   the matching adjustment calculated assuming no restriction from the breach
n    whole number of MONTHS since the date of non-compliance, capped at 11
p    10%
```
With n capped at 11, the maximum reduction is `10 * 0.10 = 100%` — i.e. the MA is fully
extinguished after ten further months of non-compliance.

**10.2 Supervisory gloss** — SS7/18 ¶8.1B–8.1G [R8]: the reduction starts **two months from the
date of non-compliance**, and where a breach is only identified later, **the two-month clock runs
from detection or confirmation** (¶8.3). The MA referenced is **dynamic** — the firm applies the
factor to the current level of MA. The PRA may determine a **higher** monthly factor case by case,
or take a more flexible approach. **Where the MA is reduced by 100% the PRA expects to revoke the
MA permission** (¶8.1C), and a new application under SoP 8/24 [R60] would be needed. Regular or
frequent breaches, even if cured inside two months, may evidence a risk-management failure
(¶8.1D); a significant breach — the example given is failing to address a PRA breach notification
in a timely manner — may itself lead to revocation (¶8.1E). Importantly for capital modelling:
**where the MA is reduced for a breach, the PRA does not expect the firm to recalculate the SCR or
alter internal-model management actions; the own-funds loss over 12 months continues to be based
on balance-sheet movements ignoring the reduction** (¶8.1G).

**10.3 Liquidity plan and portfolio management** [R8 ch. 6–7]. A firm is expected to have a
**liquidity plan for each MA portfolio**; liquidity may be managed at entity level provided the
firm can demonstrate processes ensuring sufficient liquidity is available to the MA portfolio,
taking account of any lack of fungibility.

### 11. The transitional measure on technical provisions (TMTP)

**11.1 Gate and scope** — Transitional Measure on Technical Provisions Part [R3]:
- **2.1** TMTP may be applied only with a **TMTP Permission** and only to its extent.
- **2.2** a firm with a TMTP Permission **must not apply the TMIR**.
- **2.3** **a firm must not apply TMTP after 1 January 2032.**
- **2.4** TMTP may be applied only to technical provisions for obligations that were the firm's
  *qualifying insurance and reinsurance obligations* **on 31 December 2024**, or obligations
  assumed after that date as a result of a **transfer event**.
- **2.5** TMTP must be calculated using the **TMTP method** (rule 5.1, as updated after any
  transfer event under Chapter 6).
- **3.1** the firm must disclose in its **SFCR** that it applies TMTP and **quantify the impact of
  not applying it** on its financial position.

**11.2 Definitions that drive the split** [R3 1.2]:
- *qualifying insurance and reinsurance obligations* — obligations whose technical provisions are
  subject to a TMTP Permission.
- *MA-eligible insurance and reinsurance obligations* — qualifying obligations whose technical
  provisions are calculated under **Technical Provisions 2.5(1)** and which comply with **Matching
  Adjustment 2.2(1) to 2.2(4), 2.3 and 2.4** for that firm (references to "relevant portfolio of
  insurance or reinsurance obligations" being read as references to qualifying obligations). Note
  this is an eligibility test only — the obligations need not actually be in an MA portfolio.
- *dynamic insurance and reinsurance obligations* — the MA-eligible qualifying obligations the
  firm **designates** under 4.2(1) (or 6.1(1) after a transfer).
- *dynamic portion* — the **best estimate** (which may be negative) for those designated
  obligations, **less reinsurance/SPV recoverables** on them.
- *non-dynamic portion* — the sum of (1) the best estimate (may be negative) for qualifying
  obligations valued under Technical Provisions 2.5(1) **other than** dynamic obligations, and
  (2) any technical provisions covered by the permission calculated under Technical Provisions
  2.5(2) (i.e. technical provisions as a whole), both **less recoverables**.
- *risk margin portion* — the **risk margin** within the technical provisions under Technical
  Provisions 2.5(1) covered by the permission.
- *INSPRU 7* — the individual capital assessment rules and guidance in the PRA's Prudential
  Sourcebook for Insurers **as at 31 December 2015**.
- *transfer event* — (1) a transfer of qualifying obligations; (2) transfer of risk under a
  *qualifying reinsurance contract*; (3) an amendment to such a contract changing the volume of
  risk ceded; or (4) its cancellation, expiration, termination or commutation. A *qualifying
  reinsurance contract* is a **proportional contract between two UK Solvency II firms transferring
  a 100% share** of the ceding firm's risk, where the cedant has TMTP Permission for that business
  and the contract is legally binding and enforceable in all relevant jurisdictions.

**11.3 The one-off base calculation** — TMTP 4.2 [R3], performed **in sequence** the first time the
method is applied:

```
(1)  optionally designate MA-eligible obligations for the dynamic portion

(2)  base TMTP T0 must satisfy      0 <= T0 <= (X_N - Y_N) * (1 - N/16)

     X_N = technical provisions covered by the permission as calculated at 31/12/2024,
           less reinsurance/SPV recoverables; where an MA or VA is applied to those
           technical provisions, X_N takes the MA or VA into account as at 31/12/2024
     Y_N = the same technical provisions calculated at 31/12/2024 in accordance with
           INSPRU 7 applied as at 31/12/2024, less reinsurance recoverables
     N   = years from 2016 to 2032, integer 0..16 (2016 = 0, ..., 2032 = 16)

(3)  express      base TMTP = A0 + B0 + C0
     A0 = part attributable to the risk margin portion
     B0 = part attributable to the dynamic portion
     C0 = part attributable to the non-dynamic portion

(4)  ZA = A0 / D0        D0 = risk margin portion at 31/12/2024
(5)  ZB = B0 / E0        E0 = dynamic portion at 31/12/2024
```
Note the base calculation is **anchored at 31 December 2024** and uses the **Solvency I INSPRU 7**
measure as the comparator — this is the only place the old regime survives. SS17/15 ¶3.6A [R59]:
the base calculation must **not double-count** both the actual run-off of liabilities since the
last recalculation and the 1/16 linear deduction; firms use the methodology agreed at their last
pre-31/12/2024 recalculation to avoid that.

**11.4 The running calculation** — TMTP 5.1–5.2 [R3]:

```
0 <= T_r <= (A_r + B_r + C_r - W_r)

T_r = TMTP at the final day of the relevant reporting period
A_r = ZA * (risk margin portion at the final day of the reporting period)
B_r = ZB * (dynamic portion at the final day of the reporting period)
C_r = C0 * (1 - M/7)
M   = 0 on 31/12/2024; thereafter x / 365, where x = days since 1 January 2025
      EXCLUDING 29 February 2028, so that 1 January 2025 is x = 0.
      M is updated at least at each year-end reporting date and on 1 January 2032.
W_r = the run-off accelerator in 5.2

W_r = ((A_7 + B_7 - W_q) / (7 - M_q)) * (M - M_q) + W_q          (as amended 23/12/2025)

A_7 = projected risk margin portion at 1 January 2032, multiplied by ZA
B_7 = projected dynamic portion at 1 January 2032, multiplied by ZB
M_q = value of M at the final day of the previous reporting period
W_q = value of W_r at the final day of the previous reporting period
```
Reading: the **non-dynamic** part `C_r` amortises **deterministically and linearly over seven
years** from 1 January 2025 to 1 January 2032 (M runs 0 to 7). The **risk-margin** and **dynamic**
parts are *not* fixed — they are re-struck each period as a constant proportion (ZA, ZB) of the
then-current risk margin and dynamic best estimate, so they **move with markets and with the
liability run-off**. `W_r` is the term that forces those two market-sensitive parts to zero by
1 January 2032 by linearly amortising their projected 2032 value. TMTP is a **range, not a point**:
5.1 caps but does not fix `T_r`, and SS17/15 ¶4.2A–4.2B [R59] requires a firm applying less than
the maximum to **disclose both the maximum and the actual amount**, apply the choice consistently
across QRTs, ORSA, risk management and market disclosures, and never disclose a solvency ratio
allowing for more than the maximum.

**11.5 Transfer events** — TMTP Chapter 6 [R3]. Within **two months** of the effective date the
firm must (6.1) optionally re-designate dynamic obligations among the acquired qualifying
obligations that are MA-eligible for it, update **ZA, ZB and C0**, and recompute `W_r` at the
effective date. 6.2: the updates must **not increase the aggregate TMTP** across the parties —
where the firm's technical provisions increase, the positive difference under 6.3(3) must be **no
greater** than the TMTP that applied to the transferred obligations immediately before; where they
decrease, **no less**. 6.3: compute the TMTP method output immediately before and at the effective
date and take the positive difference; 6.4: use the **same M** in both. 6.5: submit an explanation
of the re-designation, the update methods and the 6.3 calculations **no later than three months**
after the transfer event. SoP 2/24 ¶2.7–2.8 [R58] gives the transferee's arithmetic: take the
transferor's `A_r`, `B_r`, `C0`; derive `ZA = A_r_transferor / D0_transferee`; derive `ZB`
similarly from `B_r` and its own `E0` (pro-rating `B_r` and `C0` if it re-designates dynamic
business); and ensure the initial TMTP does not exceed the TMTP that applied immediately before,
adjusting `ZB` or `C0` if necessary. SS17/15 ¶3.7B–3.7E [R59] states the *meaning* the PRA
attaches: after the transfer, ZA should still represent the risk-margin portion of total TMTP as a
percentage of the risk margin on the underlying business, and ZB the dynamic portion as a
percentage of the dynamic BEL.

**11.6 Phasing-in plan** — TMTP Chapter 7 [R3]: **immediately** inform the PRA on observing that
the SCR would not be met without TMTP; take measures to comply with the SCR **by 1 January 2032**;
submit a phasing-in plan **within two months** of that observation; and report annually on
progress. SoP 2/24 ¶2.9 [R58]: the PRA may revoke the permission where a 7.4 report shows SCR
compliance by 2032 is unrealistic.

**11.7 Legacy approach** [R58 ch. 4–5][R59 ¶4.2C–4.2E, ¶3.16]. From 31 December 2024 **no new
legacy permissions** are granted. A legacy firm must: recalculate at each reporting period
(without further approval); apply the **Solvency I Pillar 2 methodology it used at its last
recalculation before 31/12/2024** and make no further methodology changes or simplifications;
change Solvency I Pillar 2 best-estimate assumptions **only** for market conditions and/or
demographic assumptions; where it holds MA permission and buys an MA-eligible asset class it did
not hold before 2016, assume that class carries the **same Solvency I illiquidity premium benefit**
as the rest of the relevant portfolio; **cap the permission to the technical provisions it covered
on 31 December 2024**; and amortise to zero by 1 January 2032 **without a cliff edge**. The PRA
also will not conduct further Individual Capital Guidance reviews (¶4.3). Consistency rule
[R59 ¶4.2D–4.2E]: both Solvency I Pillar 2 and Solvency II bases are best-estimate bases, must be
updated for market and demographic experience, and a material assumption change must be made
**consistently in both** so that it does **not** flow through into extra TMTP benefit. Granularity
limits for legacy firms [R59 ¶3.16]: an HRG must not be split between in-scope and out-of-scope;
corresponding HRGs must be identifiable and reliably calculable on the Solvency I Pillar 2 basis;
and HRG-level technical provisions must reconcile to the entity total.

**11.8 Governance and ORSA** [R59]: the calculation is **overseen by the Chief Actuary** as part
of the actuarial function, and Conditions Governing Business 6.1(b) and (e) [R92] responsibilities
extend to assurance over the TMTP calculation; at year-end the Chief Actuary confirms only that
TMTP was calculated per the permitted methodology and appropriately reduced (¶7.1). The Chief
Actuary also selects the methodology for **projecting** the risk margin portion and dynamic portion
in 5.2, consistent with Technical Provisions – Further Requirements Chapter 27 (¶3.6E). The ORSA
must monitor TMTP against remaining technical provisions and the risk that TMTP becomes
disproportionately large or that emerging surplus cannot support the run-off, with mitigants such
as restricting the TMTP or setting up a provision (¶5.5–5.8). TMTP reliance **does not** by itself
prevent dividends or capital releases, but a firm relying on TMTP to cover its SCR must evidence
sustainability, stress testing and a medium-term capital plan first (¶5.3–5.4).

### 12. The transitional measure on the risk-free interest rate (TMIR)

**12.1 Scope** — Transitional Measures 10.1 and 1.2 [R57]. Applies only to **admissible insurance
and reinsurance obligations**: contracts concluded **before 1 January 2016** (renewal is not a new
contract), whose technical provisions were determined under **INSPRU 1.1.16R as at 31 December
2015**, and which are **not subject to an MA permission**. A **s138BA FSMA permission** is
required.

**12.2 The calculation** — Transitional Measures 10.2–10.3 [R57]:

```
TMIR_adjustment(currency)  =  portion(year) * ( i_INSPRU  -  R_SII )

i_INSPRU = the interest rate determined by the firm under INSPRU 3.1.28R to 3.1.47R of the
           PRA Handbook as at 31 December 2015
R_SII    = the annual effective rate, i.e. the single discount rate which, applied to the cash
           flows of the admissible obligations, gives a value equal to their Solvency II best
           estimate computed on the relevant risk-free interest rate term structure
portion  = decreases LINEARLY at the end of each year from 100% during 2016 to 0% during 2032
```
SS17/15 ¶2.1 [R59]: the firm must construct `i_INSPRU` so the comparison is **meaningful** — e.g.
as the annual effective rate reproducing the INSPRU 1 value of the same obligations as at
31/12/2015 — and must explain and justify the method in its application.

**12.3 Interaction with the VA** — Transitional Measures 10.4 [R57]: where the firm applies the VA,
`R_SII` is computed on the **VA-adjusted** curve. SS17/15 ¶2.2 [R59] completes the picture: the
admissible obligations are then discounted at **basic risk-free rate + TMIR adjustment**, and
**the VA is not added on top** — the VA is already inside the transitional adjustment, and adding
it again would double count.

**12.4 Exclusions and disclosure** — Transitional Measures 10.5 [R57]: a TMIR firm must (1)
**exclude the admissible obligations from the VA calculation**, (2) **not apply TMTP**, and (3)
disclose in its **SFCR** that it applies the TMIR and quantify the impact of not applying it.
Chapter 12 mirrors the TMTP phasing-in plan: notify immediately if the SCR would not be met
without the TMIR, comply with the SCR **by 1 January 2032**, submit a plan within two months, and
report annually. SoP 2/24 ¶2.2A, ¶2.9A–2.9C [R58]: the PRA approves, varies or revokes a TMIR
permission by reference to compliance with Transitional Measures 10.2–10.5, and will revoke where
a 12.4 report shows SCR compliance by 2032 is unrealistic.

### 13. Which adjustments may be combined — the exclusivity map

All verified from the rule texts cited:

| Pair | Permitted together on the same obligations? | Source |
|---|---|---|
| MA and VA | **No** | Technical Provisions 8.5 [R1]; Matching Adjustment 13.3 [R2] |
| MA and TMIR | **No** | Matching Adjustment 13.3 [R2]; TMIR is only for obligations **not** subject to an MA permission, Transitional Measures 1.2 [R57] |
| MA and TMTP | **Yes** — TMTP's `X_N` explicitly takes the MA into account, and the *dynamic portion* is defined by reference to **MA-eligible** obligations | TMTP 4.2(2), 1.2 [R3] |
| VA and TMIR | **Yes, but only once** — the VA is embedded in the TMIR calculation and must not be added again | Transitional Measures 10.4 [R57]; SS17/15 ¶2.2 [R59] |
| VA and TMTP | **Yes** — `X_N` takes the VA into account | TMTP 4.2(2) [R3] |
| TMTP and TMIR | **No, in both directions** | TMTP 2.2 [R3]; Transitional Measures 10.5(2) [R57] |
| MA/VA/TMIR/TMTP and the **risk margin reference undertaking** | **No** — the reference undertaking applies **none** of them | Technical Provisions 4B.1(13) [R1] |

The last row matters for a projection model: the notional SCR used in the risk margin is computed
for an undertaking that discounts on the **basic** curve, so an MA firm's risk margin is not simply
its own SCR run-off.

---

## Model hooks

What a liability cash flow projection must produce, at what granularity, on what basis, at what
date, for each rule above.

**H1 — Expose the cash flow vector, not a present value.** *Rule:* Matching Adjustment 4.3 [R2] /
IRPR reg 5(1) [R53]. The MA is the difference of two internal rates of return computed on **the
same** liability cash flow vector against two different target values. *Requirement:* the model
must return `CF(t)` for `t = 1..T` (or finer), per currency, per MA portfolio, and must be able to
solve `sum_t CF(t) / (1+R)^t = V` for `R` given an arbitrary target `V`. A model whose public
interface is a scalar BEL cannot compute an MA at all. *Granularity:* per MA portfolio, per
currency. *Basis:* best estimate, gross of reinsurance for the TP, but the matching tests are run
**net of reinsurance** [R8 ¶4.11]. *Date:* valuation date; monthly or quarterly per the test
frequencies in §7.4.

**H2 — Discount the same vector on at least five curves.** *Rule:* Technical Provisions 3.1, 5,
8 [R1]; Matching Adjustment 4.3 [R2]; Transitional Measures 10 [R57]. The model must be able to
produce, from one projection, the BEL on: (a) **basic risk-free**; (b) **basic + MA**; (c) **basic
+ VA** (with extrapolation re-struck on the VA-adjusted forwards, §2.2); (d) **basic + TMIR
adjustment** (which itself embeds any VA); and (e) the same vector after **TMTP** is applied as an
adjustment to technical provisions rather than to the discount rate. *Requirement:* a curve is an
input parameter, not a hard-coded assumption; the discounting step must be separable from the
projection step. *Granularity:* per currency and per MA portfolio / non-MA remainder /
ring-fenced fund. *Date:* month-end (the PRA publishes monthly [R54]).

**H3 — Split the liability book on the MA eligibility conditions, at contract level and at
eligible-element level.** *Rule:* Matching Adjustment 2.2, 2.3, 2.5, 1.2 "eligible element" [R2].
*Requirement:* every model point needs flags for: future premiums payable (2.2(1)); underwriting
risks present, restricted to longevity / expense / revision / mortality / recovery time (2.2(2));
policyholder options, and if a surrender option, its surrender value (2.2(4)); and, for WP and IP,
whether a **guaranteed annuity element** or an **in-payment element** is separately identifiable
and separately manageable. The eligible-element route requires the model to project the
**guaranteed element of a with-profits annuity separately from future attaching bonus**, and
**IP claims in payment separately from active lives**.

**H4 — Run the 5% mortality test as a stress on the same projection.** *Rule:* Matching Adjustment
2.2(3), 2.4 [R2]. *Requirement:* the model must compute the best estimate of the MA obligation
portfolio under (a) mortality rates x 1.15 permanently and (b) mortality rates + 0.15pp for the
next 12 months, take the more adverse for basic own funds, apply the increase **only to policies
where it increases technical provisions**, and report the percentage increase in the best estimate.
Multiple policies on one life may be collapsed; group-level identification is permitted under
Technical Provisions – Further Requirements 20.1 if not materially different. *Threshold:* the
increase must be **<= 5%**. *Date:* at application and on an ongoing basis with quantitative
evidence [R8 ¶3.5].

**H5 — Produce a paired asset/liability cash flow grid for the matching tests.** *Rule:* SS7/18
Appendix 1 and ¶4.5, ¶4.10 [R8]. *Requirement:* at annual or finer intervals, consistent with the
firm's matching method: liability BEL cash flows; component-A asset cash flows **after PD
adjustment (notched where possible)**; per-interval surplus/shortfall; **accumulation at the
risk-free rate**; running maximum accumulated shortfall; and the PV of liabilities at the
risk-free rate. Plus the ability to re-run with **HP cash flows pushed to the latest contractual
date with step-up coupons** (Test 5) and with **HP cash flows on their minimum-MA profile**
(Test 4). No future management actions; contractual dates for non-HP assets; cash realised in full
in year 1. *Thresholds:* 3% (Test 1), 1% of BEL per risk (Test 2), 99%–100% scaling band (Test 3),
5% of MA benefit (Test 4), 5% (Test 5). *Frequency:* monthly when writing new business in the
fund, otherwise quarterly; Tests 2 and 3 at least quarterly.

**H6 — Support three market stresses on the matched position.** *Rule:* Test 2 [R8]. The model
must produce a 99.5th percentile one-year VaR **for interest rate, inflation and currency risk
separately, undiversified**, on assets and liabilities together, with HP asset cash flows stressed
consistently with each scenario. This is a discounting-layer requirement even though the SCR
itself is another stream's: the denominator is the BEL at **basic + MA**.

**H7 — Carry a fundamental spread by asset, by cash flow maturity, by CQS and by notch.** *Rule:*
Matching Adjustment 4.10–4.15, Chapter 6 [R2]; SS7/18 ¶5.10 [R8]. *Requirement:* the asset side of
the model must hold FS as a **term structure per asset**, not a single duration-based number; must
apply linear interpolation between consecutive CQS pairs for notching; must keep the PD component
separate from the CoD + LTAS "residual FS", since the PD is applied to the asset cash flows and the
residual is deducted from the MA; and must hold the two FS addition layers (HP, firm/voluntary)
separately so that MA 12.3(4) reporting of voluntary additions is possible.

**H8 — Compute "MA benefit" the way the 10% HP cap defines it.** *Rule:* Matching Adjustment 5.2,
5.5 [R2]. The cap is not measured on spread or on market value: it is measured on **the impact on
the best estimate of the Conditions Governing Business 3.2(2)(c) scenario** [R92], ignoring any
13.5 reduction, attributed to HP assets individually and in aggregate. A model must therefore be
able to attribute the change in BEL under that scenario **to individual assets**.

**H9 — Attestation feed.** *Rule:* Matching Adjustment 9–12 [R2]; SS7/18 ¶5.35–5.40 [R8].
*Requirement:* per-asset MA contribution and per-asset FS, aggregable to homogeneous risk groups
defined by asset type, sector, sub-sector, rating method, rating (with notch where material),
collateralisation and maturity band; a ranking of assets by MA contribution; residual spread net
of an investment expense allowance; and a register of voluntary FS additions with amount and
resulting MA per asset. *Date:* the **SFCR effective date** annually, delivered within **14 weeks**
of year-end; or within three months of a material change in risk profile.

**H10 — TMTP is a balance-sheet adjustment, not a cash flow adjustment, but it needs projections.**
*Rule:* TMTP 4.2, 5.1–5.2 [R3]. *Requirement:* the model must be able to produce, at each reporting
date, (a) the **risk margin portion** and (b) the **dynamic portion** (best estimate of the
designated MA-eligible obligations, net of recoverables) for the qualifying block; and, once, the
**projected** values of both **as at 1 January 2032** for `W_r`. The projections are the Chief
Actuary's methodology choice, consistent with Technical Provisions – Further Requirements Chapter
27 [R59 ¶3.6E]. `C0` and the ratios `ZA`, `ZB` are frozen inputs from the 31/12/2024 base
calculation. *Granularity:* firm level (TMTP is computed at overall firm level, allocation is
internal only [R59 ¶3.6C]). *Date:* each reporting period; M measured in days since 1 January 2025
excluding 29 February 2028.

**H11 — TMIR needs a Solvency I comparator run.** *Rule:* Transitional Measures 10.2 [R57]. The
model must produce, for pre-2016 non-MA obligations, both the Solvency II best estimate (annual
effective rate `R_SII`) **and** an INSPRU-basis rate `i_INSPRU` frozen on the 31/12/2015 basis. In
practice this makes the TMIR a dual-basis valuation, which is why a reference implementation should
treat it as **cited, not specified**.

**H12 — Report what the templates demand.** *Rule:* IR.12.01 [R89]; Reporting 3.4 [R84]. The model
must be able to emit, by line of business: TP with and without the **interest-rate transitional**,
best estimate subject to and TP without the **VA**, best estimate subject to and TP without the
**MA**, and the five TMTP components **Ar, Br, Cr, Wr, Tr**. The SFCR additionally requires the
impact of **setting the MA (and VA) to zero** on technical provisions, SCR, MCR, basic own funds
and eligible own funds — i.e. a full re-run of the liability valuation on the basic curve.

---

## Product applicability

Key: `x` = directly and materially applies; `(x)` = applies in a limited or conditional way;
`--` = does not apply; `?` = the retrieved sources do not settle it. TA = term assurance,
CI = critical illness, IP = income protection, WOL = whole of life, WP = with-profits,
ULB = unit-linked bond, PA = pension annuity.

| Item | TA | CI | IP | WOL | WP | ULB | PA |
|---|---|---|---|---|---|---|---|
| Basic risk-free curve, GBP, PRA-published [R54][R55] | x | x | x | x | x | x | x |
| LLP / extrapolation to UFR bites materially [R56] | (x) | (x) | x | x | x | -- | x |
| Volatility adjustment [R1 ch.8][R55] | (x) | (x) | (x) | (x) | (x) | (x) | -- |
| MA — whole-contract eligibility [R2 2.2] | -- | -- | -- | -- | -- | -- | x |
| MA — eligible-element route [R2 1.2, 2.3, 2.5] | -- | -- | x | -- | x | -- | -- |
| 5% mortality-risk cap [R2 2.2(3), 2.4] | -- | -- | (x) | -- | (x) | -- | x |
| Recovery time risk as a permitted risk [R2 2.2(2)][R8 ¶3.5B] | -- | -- | x | -- | -- | -- | -- |
| Surrender-option condition [R2 2.2(4)][R8 ¶3.8–3.13] | -- | -- | (x) | -- | (x) | -- | x |
| Fundamental spread and notching [R2 ch.4, ch.6] | -- | -- | (x) | -- | (x) | -- | x |
| HP assets and the 10% cap [R2 5.2, 5.3] | -- | -- | (x) | -- | (x) | -- | x |
| PRA Matching Tests 1–3 [R8 App.1] | -- | -- | (x) | -- | (x) | -- | x |
| PRA Matching Tests 4–5 (HP assets) [R8 App.1] | -- | -- | (x) | -- | (x) | -- | (x) |
| MA attestation [R2 ch.9–12] | -- | -- | (x) | -- | (x) | -- | x |
| MAIA [R2 ch.14–19][R8 ch.10] | -- | -- | (x) | -- | (x) | -- | x |
| MA breach reduction formula [R2 13.5] | -- | -- | (x) | -- | (x) | -- | x |
| TMTP [R3] | (x) | -- | (x) | x | x | (x) | x |
| TMIR [R57] | (x) | -- | (x) | x | x | (x) | -- |
| Risk-margin reference undertaking uses none of them [R1 4B.1(13)] | x | x | x | x | x | x | x |

Notes on every non-obvious mark:
- **LLP / extrapolation, TA and CI `(x)`.** Term assurance and standalone CI are typically written
  to terms well inside the GBP 50-year last liquid point [R56], so extrapolation affects only
  the tail of very long single-premium or whole-of-term contracts. ULB `--`: unit-linked
  liabilities are dominated by unit value, and the PRA's own materiality test for relevant
  currencies **excludes unit-linked technical provisions** [R55 ¶3.4], confirming that the curve
  bites on the non-unit reserve only.
- **VA `(x)` for six products, `--` for PA.** The VA requires a firm-level permission and is
  applied to the non-MA business; it is available in principle to any non-MA obligation in a
  currency for which the PRA publishes a VA. It is marked `(x)` rather than `x` because it is
  **permission-dependent, not automatic**. It is `--` for PA because MA-discounted annuity
  obligations cannot also take the VA (Technical Provisions 8.5 [R1]; Matching Adjustment 13.3
  [R2]) — and the PRA has now **excluded MA-eligible annuity liabilities from the GBP VA reference
  portfolio** [R54]. A non-MA annuity book could take the VA, but that is not the representative
  UK case (`[unverified]` as a market-practice statement; the rules do not forbid it).
- **MA whole-contract `x` only for PA.** Matching Adjustment 2.2(1) (no future premiums), 2.2(2)
  (permitted risks) and 2.2(4) (options) exclude protection and savings contracts as a whole.
  Pension annuities in payment are the paradigm case.
- **MA eligible element `x` for IP and WP.** Matching Adjustment 1.2 admits **the guaranteed
  element of a with-profits immediate or deferred annuity** and **the in-payment element of an
  income protection policy** (and of a group death-in-service dependants' annuity, which is not
  one of this library's seven products). All downstream MA rows for IP and WP are therefore `(x)`:
  they apply **only to the in-payment / guaranteed element inside an MA portfolio**, not to the
  product as written.
- **5% mortality cap `(x)` for IP and WP.** It applies only where mortality risk is connected to
  the eligible element that has been placed in the portfolio — for IP claims in payment and WP
  guaranteed annuities, mortality is present, so the cap must be tested on the element.
- **Surrender-option condition `(x)` for IP and WP** for the same reason, and because an in-payment
  IP claim generally has no surrender value at all; the SS7/18 ¶3.11–3.13 deferred-annuity guidance
  bites hardest on **deferred** annuity elements, i.e. WP deferred annuities and PA deferred
  business.
- **Matching Tests 4–5 `(x)` for PA.** Mandatory only for firms that actually hold assets with HP
  cash flows in the MA portfolio [R8 ¶4.6A]; a purely fixed-cash-flow annuity portfolio runs Tests
  1–3 only.
- **TMTP `(x)` for TA, IP and ULB; `x` for WOL, WP, PA; `--` for CI.** TMTP is available only for
  obligations that were qualifying obligations on 31 December 2024 [R3 2.4] — i.e. business in
  force pre-2016 and covered by an existing permission. Long-duration WOL, WP and annuity
  back-books are where it is material. TA and ULB in-force from before 2016 can be inside a
  permission but the amounts are typically small relative to the reserve. **CI is marked `--`
  because standalone CI is taken not to have been a material pre-2016 UK Solvency I reserve line
  for the representative products in this library — `[unverified]`: this is a judgement, not a
  retrieved fact, and the rules themselves contain no product exclusion.** The `(x)` marks for TA,
  IP and ULB rest on the same reasoning and are likewise `[unverified]` as to materiality; the
  *legal* availability of TMTP for them is verified from TMTP 2.4 [R3].
- **TMIR mirrors TMTP but excludes PA `--`** wherever the annuity book sits in an MA portfolio:
  *admissible obligations* are by definition **not subject to an MA permission** [R57 1.2], and no
  firm may apply both TMTP and TMIR [R3 2.2; R57 10.5(2)].
- **Risk-margin reference undertaking `x` for all.** Technical Provisions 4B.1(13) [R1] makes the
  reference undertaking apply no MA, VA, TMIR or TMTP, so the row is universal even though the
  risk margin itself belongs to another stream.

---

## Gaps and caveats

### Not retrieved

Everything in "Extracted mechanics" above was read from a retrieved document; the file contains no
`[unverified]` quantitative claim. The `[unverified]` tags that do appear are confined to two
market-practice judgements in "Product applicability". What follows is what could **not** be
retrieved at all.

1. **No ultimate forward rate value, convergence period or Smith-Wilson alpha.** SoP 1/20 [R55]
   describes the UFR methodology but gives no number. The values sit in the monthly *Smith-Wilson
   extrapolation parameters* XLSX [R54], which was **not opened** (the helper converts HTML and
   PDF only). **Do not state a UK UFR.** The referenced EIOPA *Report on the Calculation of the
   UFR for 2024* was not fetched either.
2. **No credit risk adjustment values in basis points**, other than the verified statement that
   **GBP and USD CRAs are zero** and the Method 3 construction (Euro CRA + 15bp, bounded 10–35bp)
   [R54]. The EUR and CAD CRAs were not retrieved.
3. **No published fundamental spread, PD or CoD figures.** These are the contents of the monthly
   *Risk-free Fundamental Spreads, Probability of Default and Cost of Downgrade* XLSX [R54], not
   opened. No FS number by CQS, asset class or maturity appears anywhere in this file.
4. **No VA value for any currency or date.** The 65% factor and the reference-portfolio spread
   formula are verified [R55]; the resulting VA is not.
5. **USD and CAD last liquid points not retrieved.** The DLT table's D/L grid did not survive text
   extraction with reliable column alignment: the GBP row produced 18 cell values against a
   20-column maturity header (1–15, 20, 25, 30, 40, 50), so the mapping of cells to maturities is
   ambiguous. Only the two LLPs stated in prose (GBP 50, EUR 20) are recorded. **No per-maturity
   DLT flags are transcribed for any currency.** Re-retrieval should target the HTML table
   directly, or the PDF version of the page.
6. **PS17/25 body not retrieved** (R60b). The URL in the SS7/18 footnote 404s; the landing page
   found by search returned HTML whose extraction failed. Everything attributed to the MAIA in
   this file comes from the MA Part [R2], SS7/18 [R8] or SoP 8/24 [R60], never from the PS.
7. **SS8/18 (internal models — modelling of the matching adjustment) not retrieved.** It is
   referenced by SoP 8/24 ¶1.4 and PS10/24 [R5] and governs how internal-model firms model MA
   dynamics under stress. A UK internal-model annuity write-up would need it; a standard-formula
   reference model does not.
8. **SS1/20 (Prudent Person Principle), SS3/17 (illiquid unrated assets) and SS35/15 not
   retrieved.** All three are cross-referenced by SS7/18 and SoP 8/24 for, respectively, PPP
   compliance of MA assets, internal ratings, and the sharing of prescribed responsibilities for
   the attestation. Their content is described here only as SS7/18 describes it.
9. **The IRPR Regulations 2023 Chapter 2 (risk margin) was skimmed, not read.** The risk-margin
   parameters (4% cost of capital, lambda 0.9) are already verified under [R4] from SI 2023/1346;
   reg 7B of SI 2023/1347 was not read in this stream.
10. **PS12/21** ("Solvency II: Deep, liquid and transparent assessments, and GBP transition to
    SONIA") was not fetched; the SONIA/zero-CRA facts attributed to it are taken from the PRA's
    technical-information page [R54], which states them directly.
11. **SS7/18 sections read in full: 1A, 2 (¶2.1–2.27, 2.37–2.48), 3, 4, 5, 8, 10 (MAIA exposure
    limits and reporting) and Appendix 1.** Sections **6 (liquidity plan, beyond ¶6.1–6.2), 7
    (management of an MA portfolio — collateral, rebalancing, surplus extraction, transferability,
    new business) and 9 (changes to MA portfolios / variations)** were **not** read in detail.
    Section 7 in particular contains the PRA's expectations on **rebalancing and extraction of
    surplus from an MA portfolio**, which a full pension-annuity write-up would want.

### Conflicts and tensions between retrieved sources — recorded, not resolved

12. **Quarterly duty vs monthly practice.** IRPR reg 3(1) [R53] says the PRA "must publish" the
    technical information **every quarter**; the PRA's page [R54] says it publishes **monthly**.
    Both are verified from primary text. The statutory duty is a floor, not a cap, but the
    documents do not say so.
13. **Technical Provisions 8.2 vs 8.3 vs SoP 1/20 ¶3.6A3.** 8.2 says the VA "must not be applied
    to the risk-free interest rates … that are derived by means of extrapolation"; 8.3 says the
    extrapolation "shall be based on the risk-free interest rates adjusted with the volatility
    adjustment"; ¶3.6A3 says the PRA "will apply extrapolation **after** applying the volatility
    adjustment". These are reconcilable (add the VA to the liquid segment, then extrapolate from
    the VA-adjusted forwards) but the Rulebook never says so in terms.
14. **"MA benefit" has two different meanings in the same Part.** Under Matching Adjustment 5.5
    [R2] it is the CGB 3.2(2)(c) scenario impact on the best estimate (used for the 10% HP cap);
    under SS7/18 Appendix 1 Test 4 and ¶5.24 [R8] it is a spread quantity in basis points
    ("worst MA 5bp, best-estimate MA 65bp"). A drafter must say which is meant.
15. **The MAIA exposure limit test refers to "the best estimate liabilities of the MA portfolio"
    footnoted "after the application of the MA"** [R8 ¶10.21 fn 38], but the MA exposure-limit
    concept elsewhere in the Part is defined by permission terms, not by BEL. The two limit
    regimes (MA `exposure limit`, MAIA `MAIA exposure limit`) are separately defined in Matching
    Adjustment 1.2 and must not be conflated.
16. **SS17/15 ¶1.2 and ¶1.3 refer to "chapters 10 and 12" of the Transitional Measures Part**,
    while the SS17/15 landing page [R59 landing text] still refers to "chapters 10 and 11". Chapter
    11 is `[Deleted]` as at 31/12/2024 [R57]. The landing page is stale; the SS text is right.
17. **SoP 2/24 ¶3.2 and ¶5.3 both use a "five percentage points" solvency-coverage-ratio
    materiality threshold** [R58], but for two different purposes (waiving the amortisation rule;
    qualifying for the legacy approach). They are not the same test and should not be merged.

### Numbers deliberately not transcribed

18. Any per-maturity DLT flag from [R56] (see gap 5).
19. Any figure from the four monthly XLSX releases [R54].
20. The `[w] [x] [y] [z]` attestation materiality metrics in SS7/18 ¶5.35 Step 3 — **the PRA leaves
    them blank**; they are firm calibrations, and inventing values here would be the exact failure
    mode this library guards against.
21. Risk-margin parameters, SCR stresses and correlation matrices — other streams' property.

### Questions the retrieved sources do not settle

22. **How a firm allocates a single liability cash flow vector between MA and non-MA portfolios
    when only an eligible element qualifies.** Matching Adjustment 2.3 forbids splitting a contract
    except for an eligible element, and SS7/18 ¶3.5A requires a "clear policy regarding the
    addition of future attaching bonuses in the MA portfolio or elsewhere" — but neither prescribes
    the allocation mechanics. For a WP model this is the crux: the guaranteed annuity element goes
    in, future bonus does not, and the sources do not say how the asset share follows.
23. **Whether the "annual effective rate" in Matching Adjustment 4.3 is computed on gross or net
    of reinsurance liability cash flows.** 4.3 refers to "the cash-flows of the relevant portfolio
    of insurance or reinsurance obligations" without qualification, while the PRA Matching Tests
    are explicitly net of reinsurance [R8 ¶4.11] and reinsurance assets can themselves sit in the
    portfolio [R8 ¶2.24]. The retrieved text does not resolve the basis for the MA calculation
    itself.
24. **The interaction between a TMTP `dynamic portion` designation and actual MA portfolio
    membership.** TMTP 1.2 defines *MA-eligible* obligations by reference to compliance with
    Matching Adjustment 2.2(1)–(4), 2.3 and 2.4 — an eligibility test that does not require the
    obligations to be in an MA portfolio, and reads across to "relevant portfolio" as "qualifying
    obligations". Whether obligations that are MA-eligible but sit outside any MA portfolio may be
    designated dynamic is not stated.
25. **Whether the risk-free-rate curve used in the accumulation step of Matching Tests 1 and 5 is
    the basic curve or the basic-plus-MA curve.** Appendix 1 says "accumulate them at the risk-free
    rate" and, separately, discount the liabilities "at the risk-free rate" — while Test 2's
    denominator is explicitly "the relevant basic risk-free interest rate plus the MA". The natural
    reading is basic for Tests 1 and 5, but the Appendix does not say "basic" there.
26. **No UK-specific statement of what happens to the MA on a currency for which the PRA ceases to
    publish technical information.** SoP 1/20 ¶3.5A–3.5B [R55] covers removal of a currency with
    three months' notice, and ¶3.6 leaves the firm to propose compliant technical information — but
    the MA depends on published fundamental spreads (Matching Adjustment 5.11 / 6.4), and the
    sources do not say how a firm computes an MA in a de-listed currency.

### Fetch behaviour observed on 2026-08-06

- `prarulebook.co.uk` and `bankofengland.co.uk` return **HTTP 403** to plain fetchers and **200**
  to a browser User-Agent; all Rulebook and PRA sources here were retrieved with the latter.
- `legislation.gov.uk` fetches cleanly; note that its HTML carries a large navigation preamble
  before the operative text.
- PRA Rulebook pages extract as one rule fragment per line with the rule number, effective date
  and "Legal Instruments that change this rule" boilerplate interleaved — usable, but a rule's
  effective date appears **after** its text, which is easy to mis-attribute.
- Bank of England **PDF** publications extract reliably (SS7/18, SoP 1/20, SoP 2/24, SoP 8/24,
  SS17/15 all read in full). Bank of England **HTML tables** do not (see gap 5), and **XLSX** is
  not handled at all.
