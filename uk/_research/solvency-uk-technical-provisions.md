# Solvency UK — the balance sheet and technical provisions — research notes

**Stream:** The Solvency UK economic balance sheet, valuation, and technical provisions
(best estimate + risk margin)
**Access date for every citation below:** 2026-08-06
**Status:** research notes, not yet merged into
`uk/references/regulatory-and-actuarial-references.md`

---

## Scope and numbering note

This stream owns reference block **R39–R52**. Entries **R1–R38** live in
`uk/references/regulatory-and-actuarial-references.md`, are **frozen**, and are already cited by
the seven UK product documents; nothing below renumbers, restates or duplicates them. Sibling
streams own **R84–R98** (reporting, disclosure and governance,
`uk/_research/solvency-uk-reporting-governance.md`) and **R99–R113** (accounting and tax,
`uk/_research/uk-accounting-and-tax.md`); their entries are cited as `[R#]` and never re-created.

**Numbers used: R39–R49. Numbers R50, R51 and R52 are left unused by design** — every source
this stream actually retrieved and read is covered by R39–R49, and the library's convention is to
leave the tail of a block spare rather than pad it with entries that were not read.

**What this stream owns**

- The **Valuation Part** of the PRA Rulebook: the Article-75 economic balance sheet, the
  recognition rule, the valuation hierarchy, and the derogation that lets a UK-GAAP preparer
  keep its financial-statement measurement. *Chapter 11 (Deferred Taxes) of the same Part is
  already numbered by the accounting stream as **[R111]** — it is cited here, not duplicated.*
- The **Technical Provisions Part** — frozen as **[R1]**. This file cites [R1] and adds depth
  (rule-by-rule) rather than creating a second number for the same Part.
- The **Technical Provisions – Further Requirements Part** in full, including Annex 1 (lines of
  business): contract boundaries, data quality, assumptions, future management actions, future
  discretionary benefits, policyholder behaviour, cash flows in scope, expenses, options and
  guarantees, currency, calculation methods, homogeneous risk groups, TP-as-a-whole, reinsurance
  recoverables, the counterparty-default adjustment, segmentation, and proportionality.
- The **risk margin**: the cost-of-capital formula as printed in Technical Provisions 4A.1, the
  reference-undertaking assumptions in 4B.1, and the underlying statutory requirement in
  regulation 7B of the IRPR Regulations. **[R4]** is the frozen entry for SI 2023/1346 (the
  instrument that cut the cost-of-capital rate to 4% and introduced lambda); it is cited and
  deepened, not renumbered.
- **Surplus funds**, only where they bite the technical-provisions boundary (Technical
  Provisions 9.1(3) / Surplus Funds 2.1) — the with-profits product stream will need more.

**Deliberately left to sibling streams.** The risk-free curve, the matching adjustment, the
volatility adjustment and the transitional measures (stream B) — this file records only *where the
Technical Provisions Part hands off to them*. The SCR and own funds (streams C and D), except that
the **reference undertaking notional SCR** is documented here because it is an input to the risk
margin. Reporting templates (R84–R98). Accounting and tax (R99–R113). Per-product application
(stream F).

### Eight retrieval facts that change how this material must be documented

1. **The assimilated Commission Delegated Regulation (EU) 2015/35 is marked "(revoked)" on
   legislation.gov.uk** [R49]. Its substance now lives in PRA Rulebook Parts created by the
   PRA Rulebook: Solvency II Instrument 2024 (PRA2024/13) [R42], in force **31 December 2024**.
   A UK document must cite **PRA Rulebook rule numbers**, not Delegated Regulation article
   numbers. Where a legacy source still cites "Article 37 DR", the UK equivalent is
   **Technical Provisions 4A.1** [R1].
2. **The risk-margin *simplifications* were not restated.** DR (EU) 2015/35 contained Article 57
   (simplified calculation of recoverables), **Article 58 (simplified calculation of the risk
   margin)**, Article 59, Article 60 (simplified best estimate for premium-adjustment
   mechanisms) and Article 61 (simplified counterparty-default adjustment) [R49]. In the
   restated **Technical Provisions – Further Requirements Part** the heading "SIMPLIFICATIONS"
   introduces **Chapter 27 (Proportionality) only** — chapters 27.1 to 27.4 and nothing else
   [R41][R42]. The EIOPA "hierarchy of risk-margin methods" (methods 1–4) has **no UK rule
   text**. What survives is (a) the general proportionality test in TPFR 27, and (b) **IRPR
   regulation 7C**, which preserves the PRA's *power* to make rules permitting simplified
   risk-margin methods [R44] — a power that, on the rulebook text retrieved on 2026-08-06, has
   not been exercised in the Technical Provisions Parts.
3. **EPIFP has been removed from the Solvency UK apparatus.** No occurrence of "expected profit"
   appears in the Own Funds Part, in the Technical Provisions or TPFR Parts, in the restatement
   instrument PRA2024/13, or in the Reporting Part text retrieved. PS3/24 records that
   respondents "welcomed the deletion of the expected profits included in future premiums
   (EPIFP) requirement in S.23.01" [R86 ¶4.43]. The only retrieved text of the definition is in
   **Article 1 of the revoked** Delegated Regulation [R49]. **A Solvency UK model does not need
   to produce an EPIFP number**; if a legacy document demands one, it is EU-vintage.
4. **There is no floor on a negative best estimate anywhere in the retrieved rules.** Searched
   for "negative" across the Valuation, Technical Provisions and TPFR Parts: the only hit is
   TPFR 25.2 (the currency-risk adjustment for EUR-pegged currencies must be negative). There is
   no surrender-value floor, no zero floor, and no cell-level or contract-level floor. See
   Extracted mechanics §17 — this is settled from the rules, not left open.
5. **The Technical Provisions Part now stops at the point where the matching adjustment begins.**
   TP Chapters 6 (Matching Adjustment to the Relevant Risk Free Interest Rate Term Structure) and
   7 (Calculation of the Matching Adjustment) are **[Deleted] as at 30/06/2024**; the material
   moved to the Matching Adjustment Part [R2]. Chapter 8 (volatility adjustment) survives in the
   Technical Provisions Part [R1].
6. **A cross-reference conflict, recorded not resolved.** SS5/24 (October 2025 version) ¶1.7 tells
   firms to read it "in conjunction with … Chapters 6, 7 and 11 of the Technical Provisions"
   [R47]. In the Rulebook as at 05/08/2026 those chapters are the **deleted** MA chapters (6 and
   7) and Chapter 11 (Recoverables from Reinsurance Contracts and ISPVs) [R1]. Only the reference
   to Chapter 11 is live.
7. **The risk-margin formula is only retrievable in full from the PRA Rulebook.** Both SI
   2023/1346 [R4] and IRPR regulation 7B [R44] print the formula as an **image**, which comes
   back empty from the text extraction; the symbol definitions (a)–(h) are text and were read.
   The PRA Rulebook renders Technical Provisions 4A.1 as **LaTeX in the page text** and that is
   the version transcribed in §16 below.
8. **Technical Provisions – Further Requirements has one and only one history date: 31/12/2024.**
   Every rule in the Part carries that effective date; it is a wholly new Part with no
   pre-restatement version [R41]. The Valuation Part, by contrast, carries a mix of 01/01/2016
   (Chapters 1 and 2) and 31/12/2024 (Chapters 3 to 12) [R39], and the Technical Provisions Part
   carries 01/01/2016, 31/12/2020, 30/06/2024 and 31/12/2024 date-stamps rule by rule [R1].

---

## Existing entries (R1–R38, and sibling-stream entries) that bear on this stream

- **[R1] PRA Rulebook — Technical Provisions Part.** The core Part this stream deepens: TP = best
  estimate + risk margin (2.4); best estimate definition (3.1); replication / TP-as-a-whole (2.5);
  market consistency (2.3); risk margin (4, 4A, 4B); risk-free curve hand-off (5); volatility
  adjustment (8); other elements — expenses, inflation, discretionary bonuses (9.1); options and
  guarantees (9.2); segmentation (10.1); reinsurance recoverables (11.1); data quality and
  approximations (12); comparison against experience (13); Lloyd's (16).
- **[R2] PRA Rulebook — Matching Adjustment Part.** Where TP Chapters 6 and 7 went on 30/06/2024.
  This file records the hand-off only; MA mechanics are stream B.
- **[R3] PRA Rulebook — Transitional Measure on Technical Provisions Part.** TMTP adjusts
  technical provisions after this stream's calculation; excluded from the reference undertaking
  by TP 4B.1(13)(d).
- **[R4] SI 2023/1346 (Risk Margin Regulations 2023).** Cut CoC 6% → 4%, introduced lambda = 0.9
  (life) / 1.0 (non-life) with a 0.25 floor, in force 31/12/2023. Deepened in §16 below.
- **[R5] PS10/24 — Reform of the Matching Adjustment.** Created the MA Part and deleted TP 6–7.
- **[R6] PS15/24 — Restatement of assimilated law.** The policy statement whose **Appendix 6** is
  the legal instrument catalogued here as [R42].
- **[R7] PS2/24 — Adapting to the UK insurance market.** Not re-read for this stream.
- **[R8] SS7/18 — Matching adjustment.** Stream B.
- **[R9] FCA COBS 20 — With-profits.** The FCA-side constraint referenced by Surplus Funds 3.1(3),
  3.1(5), 3.3(8), 3.3(10) and 3.6 as "any relevant provisions of the FCA Handbook".
- **[R13] FSMA 2000.** Source of the s.138BA permission power used for the volatility adjustment
  permission (TP 1.2) and the TMTP permission, and of the s.137G rule-making power preserved by
  IRPR regulation 7C.
- **[R14] RAO 2001 Schedule 1 Part II.** TPFR 26.4 sends obligations arising from the operations
  in **paragraphs V, VI, VII and VIII of Part II of Schedule 1** to line of business 32 when they
  cannot otherwise be assigned.
- **[R33] FRC TAS 100 / [R34] TAS 200 / [R35] IFoA APS L1.** The professional layer over any
  technical-provisions calculation. Cited, not re-created.
- **[R84] PRA Rulebook — Reporting Part** (sibling). Where the technical provisions this stream
  defines must be reported.
- **[R89] Reporting Part Chapter 10 instruction files IR.12.01 / IR.12.04 / IR.14.01** (sibling).
  IR.12.01 rows R0025/R0026/R0030 are "Gross Best Estimate … **including Technical Provisions as a
  Whole** (no deduction of…)", i.e. the reporting layer expects the TP-as-a-whole amount to be
  reported inside gross best estimate; and IR.14.01 carries a **"Surrender value — the amount of
  surrender value net of taxes"** item, which is a disclosure, not a valuation floor.
- **[R92] PRA Rulebook — Conditions Governing Business Part** (sibling). Actuarial function
  responsibility for the technical provisions; CGB 3.1 (prudent person); CGB 8.1 (finite
  reinsurance) is the definition TPFR 23.2 relies on; CGB 2.2 is the "transmission of
  information" rule TPFR 8.5 qualifies.
- **[R99] FRS 103 / [R102] FRS 102 / [R105] SI 2008/410 Schedule 3** (sibling). The UK GAAP
  measurement basis that SS38/15 [R40] maps against the Valuation Part.
- **[R111] PRA Rulebook — Valuation Part, Chapter 11 (Deferred Taxes)** (sibling). Cited here for
  completeness of the Valuation Part walk-through; **not duplicated**.
- **[R112] PRA Rulebook — SCR Standard Formula Part, Chapter 6 (LACDT/LACTP)** (sibling). TP
  4B.1(10) and 4B.1(11) fix how loss-absorbing capacity is treated inside the reference
  undertaking; the underlying LAC mechanics are [R112]'s.

---

## New entries

Numbering runs R39–R49. R50–R52 unused by design.

### A. The economic balance sheet

#### R39. PRA Rulebook — **Valuation Part** (as at 05/08/2026)

- Publisher: Prudential Regulation Authority (Bank of England)
- URL: https://www.prarulebook.co.uk/pra-rules/valuation/05-08-2026
- Doc type: rulebook part. Accessed: 2026-08-06.
- fetched_ok: yes (browser User-Agent; prarulebook.co.uk returns HTTP 403 to plain fetchers.
  Present-view URL re-verified 2026-08-06: HTTP 200, 130,238 bytes)
- Annotation: The whole Part was read, Chapters 1 to 12. **Verified directly:** the Article-75
  standard in **2.1** — assets at the amount for which they could be exchanged, liabilities at the
  amount for which they could be transferred or settled, "between knowledgeable willing parties in
  an arm's length transaction"; the **no-own-credit-standing rule in 2.2**; going concern (3.1);
  the **scope carve-out in 4.1** — Chapters 5 to 12 apply "to the recognition and valuation of
  assets and liabilities, **other than technical provisions**"; recognition in conformity with
  UK-adopted international accounting standards (5.1) and valuation under them only where they are
  consistent with Chapter 2 (5.2, 5.3); the **UK-GAAP derogation in 5.4** with its four cumulative
  conditions; separate valuation of individual assets (5.5) and liabilities (5.6); the three-level
  **valuation hierarchy in 6.1–6.7**; contingent liabilities (7.1–7.3); goodwill and intangibles
  at zero (8.1); related undertakings (9.1–9.6, including the adjusted equity method in 9.3);
  specific liabilities (10.1, 10.2); deferred taxes (11.1–11.3 — **numbered [R111]** by the
  accounting stream, cited not duplicated); and the excluded methods (12.1–12.7). Chapters 1 and 2
  carry the date-stamp 01/01/2016; Chapters 3 to 12 carry 31/12/2024, i.e. they are the restated
  Delegated-Regulation material. Related-links block lists SS9/14, SS38/15 [R40] and SS1/20.
- Products: all (TA, CI, IP, WOL, WP, ULB, PA) — the Part governs everything on the balance sheet
  except technical provisions themselves.

#### R40. SS38/15 — *Solvency II: consistency of UK generally accepted accounting principles with Solvency II* (November 2024, updating August 2015)

- Publisher: Prudential Regulation Authority (Bank of England)
- URLs: landing page
  https://www.bankofengland.co.uk/prudential-regulation/publication/2015/solvency2-consistency-of-uk-generally-accepted-accounting-principles-with-the-solvency2-directive-ss ;
  PDF read
  https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/supervisory-statement/2024/ss3815-november-2024-update.pdf
- Doc type: supervisory statement (PDF, 11 pages). Accessed: 2026-08-06.
- fetched_ok: yes (PDF text extracted; PDF URL re-verified 2026-08-06: HTTP 200, 991,592 bytes)
- Annotation: The operative mapping between UK GAAP and the Valuation Part [R39]. **Verified
  directly:** ¶1.5 restates the Valuation 5.4 derogation as three conditions (UK GAAP consistent
  with Valuation Chapter 2; proportionate; IFRS would impose disproportionate cost); ¶1.6 — where
  UK GAAP and IFRS are consistent the PRA expects the derogation **not** to apply; ¶1.7 — the PRA
  expects supporting evidence for conditions 2 and 3 to go to the supervisor before use; ¶1.8 — the
  derogation relates to Valuation 5.1 and 5.2, **applies to the whole of Valuation 6**, applies to
  the *first sentence only* of Valuation 10.1 (the second sentence restates Valuation 2.2 and
  "cannot be derogated"), does **not** apply to Valuation 10.2, and applies to **Valuation 11.1 but
  not 11.2 or 11.3**; ¶1.10 — most UK-GAAP/IFRS differences for insurers are disclosure-level, so
  the derogation is expected to have limited effect. The §2 table gives a standard-by-standard
  verdict; the two entries that matter for a life model are **FRS 102 Chapter 11 and Chapter 12 —
  "Yes, with amendments"** (fair-value measurement consistent on initial recognition; thereafter
  the second sentence of Valuation 10.1 bars any own-credit-standing adjustment) and **FRS 103 —
  "No", because "Chapters 2 to 14 of the Technical Provisions, the Technical Provisions – Further
  Requirements and the Matching Adjustment Parts of the PRA Rulebook still apply."** That single
  row is the cleanest statement in the retrieved corpus that **FRS 103 insurance-contract
  measurement is never a permitted substitute for the Solvency UK technical provisions.** The
  November 2024 annex records that the update only re-pointed references from DR (EU) 2015/35 to
  PRA Rulebook rules and did **not** refresh the underlying UK-GAAP/IFRS analysis.
- Products: all; bites hardest where a firm reports under FRS 102/103 rather than IFRS.

### B. Technical provisions — the restated detail

#### R41. PRA Rulebook — **Technical Provisions – Further Requirements Part** (as at 05/08/2026), including Annex 1

- Publisher: Prudential Regulation Authority (Bank of England)
- URL: https://www.prarulebook.co.uk/pra-rules/technical-provisions-further-requirements/05-08-2026
  (note the slug uses single hyphens, not the `---` form used by some other Parts; the `---`
  variant returns HTTP 404)
- Doc type: rulebook part. Accessed: 2026-08-06.
- fetched_ok: yes (browser User-Agent; URL re-verified 2026-08-06: HTTP 200, 259,991 bytes)
- Annotation: **The single most load-bearing new source in this stream.** This is where the
  operative detail of DR (EU) 2015/35 Articles 17–61 now lives. Read in full: Chapter 1
  (Application), **2 (Recognition and Derecognition)**, **3 (Boundary of an Insurance or
  Reinsurance Contract, 3.1–3.7)**, 4 (Data used in the Calculation, 4.1–4.4), 5 (Limitations of
  Data), 6 (Appropriate Use of Approximations), 7 (Assumptions, 7.1–7.3), **8 (Future Management
  Actions, 8.1–8.5)**, 9 (Future Discretionary Benefits), 10 (Separate Calculation of the Future
  Discretionary Benefits), **11 (Policyholder Behaviour)**, 12 (Credibility of Information),
  **13 (Cash-Flows, the eight-item in-scope list)**, 14 (Expected Future Developments in the
  External Environment), 15 (Uncertainty of Cash-Flows), **16 (Expenses, 16.1–16.4)**, 17
  (Contractual Options and Financial Guarantees), 18 (Currency of the Obligation), 19 (Calculation
  Methods, 19.1–19.5), **20 (Homogeneous Risk Groups of Long-Term Insurance Business
  Obligations)**, 21 (General Insurance Business Obligations), **22 (Circumstances in which
  Technical Provisions are to be calculated as a whole)**, 23 (Recoverables — General Provisions),
  **24 (Counterparty Default Adjustment, 24.1–24.5)**, 25 (Currencies Pegged to the Euro), **26
  (Lines of Business)**, **27 (Proportionality)**, and **Annex 1 Parts A–E (lines of business
  1–36)**. Every rule in the Part carries the effective date **31/12/2024** and the Part has only
  one history date — it is wholly new. The Part's only "Related links" entry is PS15/24 [R6].
  **Note what is absent:** the Part contains no risk-margin simplification, no simplified
  counterparty-default adjustment, and no simplified recoverables calculation; the heading
  "SIMPLIFICATIONS" introduces Chapter 27 (Proportionality) alone.
- Products: all.

#### R42. **PRA Rulebook: Solvency II Instrument 2024** (PRA2024/13) — Appendix 6 to PS15/24

- Publisher: Prudential Regulation Authority (Bank of England)
- URL: https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/policy-statement/2024/november/ps1524app6.pdf
- Doc type: legal instrument / rule-making instrument (PDF, 250 pages). Accessed: 2026-08-06.
- fetched_ok: yes (PDF text extracted, ~681 KB of text; URL re-verified 2026-08-06: HTTP 200,
  1,780,845 bytes)
- Annotation: Numbered separately from **[R6]** (the PS15/24 policy statement, frozen) because it
  is a distinct legal instrument with its own citation (PRA2024/13) and is the document a drafter
  must cite for the *text* of the restated rules. **Verified directly:** it makes rules under FSMA
  ss.137G, 137T and 192J; the Annex table maps Parts to annexes — **Technical Provisions = Annex
  R, Technical Provisions – Further Requirements = Annex S, Valuation = Annex W**, with Glossary A,
  Actuaries B, Conditions Governing Business C, External Audit D, Matching Adjustment J, MCR K,
  Own Funds L and M, SCR – Standard Formula O, SCR – USP P, Surplus Funds Q, Third Country Branches
  T, Transitional Measures U, Undertakings in Difficulty V; **commencement 31 December 2024, except
  Annex M (Own Funds) which comes into force 2 January 2026**; made by order of the Prudential
  Regulation Committee on **5 November 2024**. A header note on page 1 records that **SCR –
  Standard Formula 3B6.6(1) was subsequently amended by the PRA Rulebook: SII Firms: Solvency II
  Amendment (No 1) Instrument 2024 to correct an error** (the mass-lapse correction; the correction
  itself is stream C's). Also verified from the instrument text: the restated **SCR – Standard
  Formula 3.3A** scenario rules, which are the bridge between this stream and the SCR — under
  3.3A(1) a scenario "does not change the amount of the risk margin included in technical
  provisions", "does not change the value of deferred tax assets and liabilities", "does not change
  the value of future discretionary benefits included in technical provisions", and assumes "no
  management actions are taken by the firm during the scenario"; 3.3A(2) then requires the
  post-scenario technical provisions to allow for future management actions complying with
  **Technical Provisions – Further Requirements 8** and for any material adverse impact on option
  take-up; 3.3A(3) permits simplified methods for the post-scenario technical provisions subject to
  a no-material-misstatement test; 3.3A(5) floors the scenario impact at zero where the scenario
  would *increase* basic own funds.
- Products: all.

#### R43. PRA Rulebook — **Glossary** (as at 05/08/2026)

- Publisher: Prudential Regulation Authority (Bank of England)
- URL: https://www.prarulebook.co.uk/glossary (re-verified 2026-08-06: HTTP 200, 76,049 bytes;
  `/pra-rules/glossary` is a 404). The per-letter printable exports actually read (letters B, E, F,
  M, R, T, V) were retrieved in an earlier session and their exact query URLs were not preserved —
  treat the base URL as the citation and the letter views as navigation.
- Doc type: rulebook glossary. Accessed: 2026-08-06.
- fetched_ok: yes (browser User-Agent, printable letter views)
- Annotation: Supplies the defined terms on which every rule in [R1] and [R41] turns.
  **Verified definitions** (transcribed in Extracted mechanics §0): *best estimate* ("the best
  estimate of future cash-flows, calculated in accordance with Technical Provisions 3", 01/01/2016);
  *risk margin* ("the portion of technical provisions calculated in accordance with Technical
  Provisions 4A and 4B", 31/12/2024 — note this points at the **new** chapters, not the old
  Chapter 4); *technical provisions* (Solvency II Firms sector: established in accordance with
  Technical Provisions 2.1); *future discretionary benefits* (31/12/2024 — a two-limb test);
  *basic relevant risk-free interest rate term structure* (the relevant curve **without** MA, VA or
  the risk-free transitional, 30/06/2024); *relevant risk-free interest rate term structure*
  (31/12/2024, pointing at Technical Provisions 5 and 8, the Matching Adjustment Part, the TPFR
  Part, Transitional Measures 10.2, and PRA technical information under IRPR reg 3(1));
  *matching adjustment* and *volatility adjustment*; *risk-free interest rate transitional
  measure*; *risk-mitigation techniques*; *market value* ("the market value as determined in
  accordance with generally accepted accounting practice" — a **UK-GAAP-anchored** definition that
  sits oddly beside the Article-75 standard, recorded not resolved); *expense risk* (30/06/2024);
  *eligible own funds*; *exceptional adverse situation*.
- Products: all.

### C. The risk margin

#### R44. The Insurance and Reinsurance Undertakings (Prudential Requirements) Regulations 2023 (SI 2023/1347), Part 2 Chapter 2 (regulations 7A–7C)

- Publisher: legislation.gov.uk (HM Treasury statutory instrument), as-amended view
- URL: https://www.legislation.gov.uk/uksi/2023/1347/contents (re-verified 2026-08-06: HTTP 200)
- Doc type: statutory instrument, as amended. Accessed: 2026-08-06.
- fetched_ok: yes
- Annotation: The "IRPR Regulations" referred to throughout the PRA Rulebook. **Distinct from
  [R4]**, which is SI 2023/**1346** (the Risk Margin Regulations). **Verified directly:** made
  7 December 2023, laid 8 December 2023, made under FSMA 2023 ss.4, 84(2) and 86(5); reg 1(2) —
  "come into force for the purposes of regulation 7 on 1st April 2024 and for all other purposes on
  30th June 2024"; **Part 2 Chapter 2 (regulations 7A, 7B, 7C) was inserted by SI 2024/1083** (The
  Insurance and Reinsurance Undertakings (Prudential Requirements) (Amendment and Miscellaneous
  Provisions) Regulations 2024), "1.11.2024 for specified purposes and 31.12.20204 otherwise"
  — *the "31.12.20204" is a typographical error in the legislation.gov.uk textual-amendment note as
  displayed; the intended date is plainly 31.12.2024, but it is recorded here as printed rather
  than silently corrected*. **Regulation 7B** is the statutory risk-margin requirement: where PRA
  rules provide for a risk margin calculated separately from the best estimate, it must be
  calculated "for the whole portfolio of insurance and reinsurance obligations" per the prescribed
  formula, with (b) CoC = **4%**, (d) SCR(t) = the SCR of the reference undertaking after t years
  calculated in accordance with PRA rules, (e) λ = **0.9 for long-term** and **1.0 for general**
  insurance and reinsurance obligations, (g) λ_floor = **0.25**, and (h) r(t+1) = the basic relevant
  risk-free rate for maturity t+1. **The formula itself is an image on legislation.gov.uk and came
  back empty from text extraction** — the transcribed formula in §16 comes from Technical
  Provisions 4A.1 [R1], which the Rulebook renders as LaTeX. **Regulation 7C** preserves the PRA's
  s.137G power to make rules "permitting an insurance or reinsurance undertaking to use simplified
  methods to calculate risk margin which are proportionate to the nature, scale and complexity of
  the risk". Regulation 8 applies FSMA with modifications to regulations 5 (matching adjustment),
  6 (fundamental spread) and 7B (risk margin). SI 2024/1083 was **not** separately fetched
  (https://www.legislation.gov.uk/uksi/2024/1083/contents verified HTTP 200 but not read) —
  everything recorded about it here comes from the textual-amendment notes inside [R44].
- Products: all; the λ taper and the 4% rate bite hardest on long-duration business (PA, WOL, IP).

### D. With-profits: surplus funds and the technical-provisions boundary

#### R45. PRA Rulebook — **Surplus Funds Part** (as at 05/08/2026)

- Publisher: Prudential Regulation Authority (Bank of England)
- URL: https://www.prarulebook.co.uk/pra-rules/surplus-funds/05-08-2026 (re-verified 2026-08-06:
  HTTP 200, 82,668 bytes)
- Doc type: rulebook part. Accessed: 2026-08-06.
- fetched_ok: yes (browser User-Agent)
- Annotation: Read in full (Chapters 1–4). This Part is the **only** carve-out from the "all
  payments to policyholders, including future discretionary bonuses" rule in Technical Provisions
  9.1(3) [R1]. **Verified directly:** 1.1 — applies to a UK Solvency II firm carrying on
  with-profits insurance business; 1.2 defines *with-profits assets*; **2.1** — a firm "shall not
  treat surplus funds as insurance and reinsurance obligations when valuing payments to
  policyholders and beneficiaries in the calculation of technical provisions in accordance with
  Technical Provisions 2" [Note: Art. 78(3) and Art. 91(2) SII Directive]; 3.1 gives the five-limb
  surplus-funds calculation (with-profits assets less with-profits policy liabilities less tax/costs
  on future shareholder transfers less other attributable liabilities less the value of future
  shareholder transfers); **3.2** makes the **retrospective** asset-share-style calculation in 3.3
  the default and the **prospective** calculation in 3.4 the fallback where the retrospective one
  "does not adequately reflect the value" or is impracticable; 3.3 lists the ten retrospective
  roll-up items (premiums, investment return, permanent enhancements, past miscellaneous surplus,
  expenses, past deductions for guarantees/smoothing/options/life cover, partial benefits, tax,
  reinsurance, past shareholder transfers); 3.4 lists the six prospective present-value items; 3.5
  defines the benefits in 3.4(4) as guaranteed benefits (including guaranteed surrender and paid-up
  values), contractually-entitled declared bonuses, and future discretionary additions only to the
  extent consistent with what the retrospective calculation would have produced; **4.1** requires
  the surplus-funds valuations to be consistent with the technical-provisions methodology under
  Technical Provisions 2. Chapters 1 to 4 carry 01/01/2016 except the 1.2 definition (31/12/2024).
- Products: WP only (and any with-profits fund inside a composite writing WOL or PA business).

#### R46. SS13/15 — *Solvency II: surplus funds* (November 2024, updating March 2015)

- Publisher: Prudential Regulation Authority (Bank of England)
- URLs: landing page
  https://www.bankofengland.co.uk/prudential-regulation/publication/2015/solvency2-surplus-funds-ss ;
  PDF read
  https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/supervisory-statement/2024/ss1315-november-2024-update.pdf ;
  rulebook guidance view https://www.prarulebook.co.uk/pra-rules/surplus-funds/05-08-2026 lists it
  under "Related links"
- Doc type: supervisory statement (PDF, 7 pages). Accessed: 2026-08-06.
- fetched_ok: yes (PDF text extracted)
- Annotation: **Verified directly:** ¶2.1 states the interaction expressly — Technical Provisions
  9.1(3) requires all payments to policyholders including future discretionary bonuses to be in
  technical provisions "unless those payments constitute surplus funds that fall within Surplus
  Funds 2.1", and Surplus Funds 2.1 excludes them only where they meet the **Tier 1 own funds**
  requirements in Own Funds 3.1; ¶2.3 — the PRA expects surplus funds normally to meet the Tier 1
  criteria but warns they are "likely to be treated as part of a ring-fenced [fund]"; **¶2.4 — the
  surplus-funds calculation "does not refer to or include a risk margin"**, but this does not
  relieve the firm of calculating the risk margin on its business as a whole including with-profits
  business; ¶3.1 — whole-of-life policies, or policies where the retrospective result "might be
  negative or significantly lower than the value calculated using the prospective approach", are
  examples where the prospective approach may be necessary; ¶3.2 — grouping is allowed if it
  produces the same or a higher result, does not misstate guarantee/option/smoothing costs, and
  groups policies with similar attributes "including the status of guarantees"; ¶3.4 defines
  "permanent enhancements" as amounts expected to be permanent "in all but the most extreme adverse
  circumstances"; ¶3.5 defines "miscellaneous surplus" as fund-experience surplus/deficit including
  profits or losses from non-profit business inside the with-profits fund; **¶3.6 — the PRA would
  not expect a firm to include estate distributions in benefits payable** for the prospective
  calculation. ¶2.2 is [DELETED].
- Products: WP.

### E. Reinsurance recoverables — the two supervisory statements that bite

#### R47. SS5/24 — *Funded reinsurance* (October 2025, updating November 2024)

- Publisher: Prudential Regulation Authority (Bank of England)
- URL: https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/supervisory-statement/2025/ss524-october-2025.pdf
  (re-verified 2026-08-06: HTTP 200, 370,064 bytes)
- Doc type: supervisory statement (PDF). Accessed: 2026-08-06.
- fetched_ok: yes (PDF text extracted)
- Annotation: Read for its **technical-provisions interface only**; the risk-management, collateral
  and internal-model content belongs to other streams. **Verified directly:** ¶1.7 tells firms to
  read it with "Chapter 3 of the Conditions Governing Business, **Chapters 6, 7 and 11 of the
  Technical Provisions**, the Solvency Capital Requirement – General Provisions, and the Solvency
  Capital Requirement – Internal Models Parts", plus SS20/16, SS7/18 [R8], SS8/18 and SS1/20 —
  **a stale cross-reference**, since Technical Provisions Chapters 6 and 7 are [Deleted] as at
  30/06/2024 [R1]; only Chapter 11 (Recoverables from Reinsurance Contracts and ISPVs) is live.
  Recorded, not resolved. Also verified: the PRA expects firms to calculate an **"immediate
  recapture" metric** assuming immediate recapture of all business ceded to a counterparty,
  ignoring the likelihood of the event, used **only** for setting internal investment limits and
  "not for other purposes, including to a firm's recapture plan or collateral policy" (¶2.4–¶2.5);
  firms assuming recapture into an MA portfolio must assume a "worst-case" compliant collateral
  portfolio (¶2.7) and must not assume further permissions would be in place at the point of
  recapture (¶2.7A). For this stream the operative point is that recapture risk is **not** a
  best-estimate cash-flow item: it feeds risk management and the counterparty-default adjustment,
  which TPFR 24 requires to be computed separately.
- Products: PA principally (bulk annuity / funded-reinsurance structures); WOL and WP at the
  margins.

#### R48. SS18/16 — *Solvency II: longevity risk transfers* (November 2024, updating January 2020)

- Publisher: Prudential Regulation Authority (Bank of England)
- URLs: landing page
  https://www.bankofengland.co.uk/prudential-regulation/publication/2016/solvency2-longevity-risk-transfers-ss ;
  PDF read
  https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/supervisory-statement/2024/ss1816-november-2024-update.pdf
- Doc type: supervisory statement (PDF). Accessed: 2026-08-06.
- fetched_ok: yes (PDF text extracted). **Read only in part** — grep-level reading for the
  technical-provisions and counterparty-default interface; the transaction-structuring and
  pre-notification content was not transcribed.
- Annotation: Retained as the companion to [R47] for longevity swaps and reinsurance of annuity
  longevity risk. **Verified:** the statement observes that holding capital under the SCR for
  counterparty default risk "may not be sufficient in and of itself" — i.e. the PRA does not treat
  the SCR counterparty-default module as a substitute for a properly calculated TPFR 24
  counterparty-default adjustment or for collateral and structuring controls. Everything else about
  this SS is **[unverified]** here and should be re-read before it is cited for anything more.
- Products: PA (dominant), WOL back-books.

### F. Provenance of the superseded law

#### R49. Commission Delegated Regulation (EU) 2015/35 — assimilated text, **marked "(revoked)"**

- Publisher: legislation.gov.uk (assimilated EU law)
- URLs: contents https://www.legislation.gov.uk/eur/2015/35/contents (re-verified 2026-08-06:
  HTTP 200) ; Article 1 (definitions) https://www.legislation.gov.uk/eur/2015/35/article/1
  (re-verified 2026-08-06: HTTP 200)
- Doc type: assimilated EU regulation, revoked. Accessed: 2026-08-06.
- fetched_ok: yes (table of contents and Article 1 read; the article bodies were **not** read)
- Annotation: Recorded as a **negative / provenance** source. The title line on legislation.gov.uk
  reads: Commission Delegated Regulation (EU) 2015/35 of 10 October 2014 supplementing Directive
  2009/138/EC … "**(revoked)**", and the page states it "is up to date with all changes known to be
  in force on or before 04 August 2026". Its revocation is by s.1(1) of and Schedule 1 to the
  Financial Services and Markets Act 2023, as the explanatory note to [R4] records. **Verified from
  the table of contents:** Article 37 "Calculation of the risk margin", Article 39
  "[cost-of-capital rate]", Article 57 "Simplified calculation of recoverables from reinsurance
  contracts and special purpose vehicles", **Article 58 "Simplified calculation of the risk
  margin"**, Article 59, Article 60 "Simplified calculation of the best estimate for insurance
  obligations with premium adjustment mechanism", Article 61 "Simplified calculation of the
  counterparty default adjustment" — the block of simplifications that was **not** carried into the
  TPFR Part [R41][R42]. **Verified from Article 1:** the EPIFP definition — "'the expected profit
  included in future premiums' means the expected present value of future cash flows which result
  from the inclusion in technical provisions of premiums relating to existing insurance and
  reinsurance contracts that are expected to be received in the future, but that may not be
  received for any reason, other than because the insured event has occurred, regardless of the
  legal or contractual rights of the policyholder to discontinue the policy." This is the **only**
  retrieved text of that definition, and it sits in revoked law.
- Products: none directly; cite only to explain what a legacy or EU-vintage document is referring
  to.

---

## Extracted mechanics

Rule references are to the PRA Rulebook Part named. "TP n" = Technical Provisions Part [R1];
"TPFR n" = Technical Provisions – Further Requirements Part [R41]; "Val n" = Valuation Part [R39].
All rule text below was read on 2026-08-06 from the present view (05/08/2026) unless a different
as-at date is stated.

### 0. Defined terms a model must key on [R43]

| Term | Definition as printed | Date-stamp |
|---|---|---|
| best estimate | "the best estimate of future cash-flows, calculated in accordance with Technical Provisions 3" | 01/01/2016 |
| risk margin | "the portion of technical provisions calculated in accordance with **Technical Provisions 4A and 4B**" | 31/12/2024 |
| technical provisions | (SII Firms sector) "the technical provisions established in accordance with Technical Provisions 2.1" | 01/01/2016 |
| future discretionary benefits | future benefits of contracts of insurance, **other than linked benefits**, which either (1) are legally or contractually based on (a) the performance of a specified contract/group/type of contract, (b) the realised or unrealised investment return on a specified pool of assets held by the firm, or (c) the profit or loss of the firm or fund corresponding to the contract; **or** (2) are based on a declaration of the firm — and in either case the **timing or amount is at the firm's full or partial discretion** | 31/12/2024 |
| basic relevant risk-free interest rate term structure | the relevant curve **without** (1) a matching adjustment, (2) a volatility adjustment, or (3) a risk-free interest rate transitional measure | 30/06/2024 |
| relevant risk-free interest rate term structure | the curve in accordance with (1) TP 5 and 8, the Matching Adjustment Part, the TPFR Part and Transitional Measures 10.2; and (4) the relevant technical information published by the PRA under IRPR reg 3(1) | 31/12/2024 |
| cost-of-capital rate | the rate above the relevant risk-free rate for holding eligible own funds equal to the SCR necessary to support the obligations over their lifetime, "which, as specified in regulation 7B(b) of the IRPR Regulations, **equals 4%**" (TP 1.2) | 31/12/2024 |
| reference undertaking | the hypothetical firm assumed, for the purpose of calculating the risk margin, to take over the whole portfolio of obligations (a **composite** splits general and long-term), on the assumptions in TP 4B (TP 1.2) | 31/12/2024 |
| reference undertaking notional SCR | the hypothetical SCR of the reference undertaking, calculated in accordance with TP 4B.1 (TP 1.2) | 31/12/2024 |
| volatility adjustment permission | the s.138BA FSMA permission to apply a VA for the purposes of calculating the best estimate (TP 1.2) | 31/12/2024 |
| market value | "the market value as determined in accordance with **generally accepted accounting practice**" | 01/01/2016 |
| expense risk | risk of loss/adverse change in the value of insurance obligations from changes in the **level, trend or volatility** of expenses incurred in servicing contracts | 30/06/2024 |
| risk-mitigation techniques | all techniques which enable a UK Solvency II firm to transfer part or all of its risks to another party | 31/12/2020 |

*Recorded conflict:* the glossary anchors *market value* in "generally accepted accounting
practice" while Val 2.1 states the Article-75 exchange/transfer standard and Val 12.1 forbids cost
or amortised cost. TPFR 22.3 uses *market value* for the TP-as-a-whole test. The two are not
reconciled in the retrieved text.

### 1. The economic balance sheet: Valuation 2 [R39]

- **Val 2.1(1)** — assets at "the amount for which they could be exchanged between knowledgeable
  willing parties in an arm's length transaction".
- **Val 2.1(2)** — liabilities at "the amount for which they could be transferred, or settled,
  between knowledgeable willing parties in an arm's length transaction". [Note: Art. 75(1) SII
  Directive]
- **Val 2.2** — when valuing liabilities "**no adjustment must be made to take account of the own
  credit standing of the firm**".
- **Val 3.1** — value on a going-concern assumption (31/12/2024).
- **Val 4.1** — Chapters 5 to 12 apply to recognition and valuation of assets and liabilities
  **other than technical provisions**. Technical provisions are governed by TP + TPFR + MA Part +
  CGB + SCR-GP, per the cross-references in Val 9.4(2)(a) and Val 11.2.

Consequence for a model: the balance sheet is `own funds = assets (Val 2, 5–12) − technical
provisions (TP + TPFR) − other liabilities (Val 2, 5–12)`. There is no deferred acquisition cost
asset, no unamortised expense asset, and no goodwill (Val 8.1). The projection model produces only
the technical-provisions leg.

### 2. The valuation hierarchy and the IFRS / UK GAAP relationship [R39][R40]

Recognition and measurement default (Val 5.1, 5.2, 5.3):

1. **Recognise** assets and liabilities in conformity with **UK-adopted international accounting
   standards** (Val 5.1).
2. **Value** them in accordance with those standards **provided** the standards include valuation
   methods consistent with Val 2; where a standard allows more than one method, only a Val-2
   consistent method may be used (Val 5.2).
3. Where the standards are inconsistent with Val 2 "either temporarily or permanently", use other
   Val-2 consistent methods (Val 5.3).
4. **Val 5.5 / 5.6** — value individual assets and individual liabilities **separately**.

**The UK GAAP derogation (Val 5.4)** — a firm may recognise and value an asset or liability using
the method it uses for its annual or consolidated financial statements if **all four** hold:
(1) the method is consistent with Val 2; (2) it is proportionate to the nature, scale and
complexity of the firm's risks; (3) the firm does not value that item under UK-adopted IAS in its
financial statements; and (4) using international accounting standards "would impose costs on the
firm that would be disproportionate with respect to the total administrative expenses".

SS38/15 [R40] then fixes the perimeter of that derogation:

| Provision | Derogation applies? |
|---|---|
| Val 5.1, 5.2 | yes (that is what it derogates from) |
| Val 6 (whole chapter) | yes |
| Val 10.1 first sentence | yes |
| Val 10.1 second sentence (no own-credit adjustment) | **no — "cannot be derogated"** |
| Val 10.2 (contingent liabilities) | no |
| Val 11.1 | yes |
| Val 11.2, 11.3 | **no** |
| Val 7, 8, 9, 12 | not derogated (SS38/15 ¶1.9: remaining valuation requirements apply in full) |

FRS-by-FRS verdicts that matter to a life model [R40 §2 table]: **FRS 102 Chapter 11 (basic
financial instruments) — yes, with amendments**; **Chapter 12 (other financial instruments) — yes,
with amendments** (in both cases fair value on initial recognition is consistent, but thereafter
the second sentence of Val 10.1 bars own-credit adjustment); **Chapter 16 investment property —
yes, fair-value model only**; **Chapter 17 PPE — yes, revaluation model only**; **Chapter 18
intangibles — no (Val 8.1 applies)**; **Chapter 20 leases — no (Val 12.4)**; **Chapter 21
provisions/contingencies — no**; **Chapter 25 borrowing costs — no (cost model)**; **Chapter 27
impairment — no (cost model)**; **Chapter 28 employee benefits — yes**; **Chapter 29 income tax —
no** (deferred tax consistent with IFRS for Val 11.1 but Val 11.2/11.3 still apply); **FRS 103 —
no**, because "Chapters 2 to 14 of the Technical Provisions, the Technical Provisions – Further
Requirements and the Matching Adjustment Parts of the PRA Rulebook still apply".

**The valuation hierarchy (Val 6.1–6.7)** — applies when valuing under Val 5.1/5.2/5.3, taking
account of characteristics market participants would price in (condition, location, restrictions on
sale or use):

1. **Val 6.2** — default: quoted market prices in active markets for the **same** assets or
   liabilities.
2. **Val 6.3** — else quoted market prices in active markets for **similar** assets/liabilities
   with adjustments for (1) condition or location, (2) comparability of the inputs, (3) volume or
   level of market activity.
3. **Val 6.4** — "active market" per UK-adopted international accounting standards.
4. **Val 6.5** — where 6.4 is not satisfied, use **alternative valuation methods**.
5. **Val 6.6** — alternative methods must rely "as little as possible on undertaking-specific
   inputs" and make maximum use of relevant market inputs: (1) quoted prices for identical/similar
   items in markets that are not active; (2) observable non-price inputs — interest rates and yield
   curves at commonly quoted intervals, implied volatilities, credit spreads; (3)
   market-corroborated inputs. All market inputs must be adjusted for the Val 6.3 factors.
   Unobservable inputs may be used to the extent relevant observable inputs are unavailable, and
   undertaking-specific data must be adjusted where other market participants would use different
   data. Risk assumptions must cover both the risk inherent in the technique and in its inputs.
6. **Val 6.7** — alternative methods must be consistent with one or more of: **market approach**
   (including matrix pricing), **income approach** (present value techniques, option pricing
   models, multi-period excess earnings method), **cost / current replacement cost approach**.

### 3. What is and is not recognised on the Solvency UK balance sheet [R39]

- **Contingent liabilities (Val 7.1–7.3)** — must be recognised as liabilities where **material**,
  material meaning the information "could influence the decision-making or judgement of the
  intended user … including a supervisory authority" (7.2), and **irrespective of whether IAS would
  require recognition** (7.3). **Val 10.2** measures them at the **expected present value of future
  cash-flows required to settle the contingent liability over its lifetime, using the *basic*
  relevant risk-free interest rate term structure** — i.e. **no MA, no VA, no transitional**, even
  for a firm with an MA permission.
- **Goodwill and other intangibles (Val 8.1)** — goodwill at **zero**; other intangibles at zero
  **unless** the asset can be sold separately **and** the firm can demonstrate a value for the same
  or similar assets derived under Val 6.2 (quoted prices in an active market for the same asset), in
  which case value it under Val 6.
- **Related undertakings (Val 9.1)** — hierarchy: (1) Val 6.2 quoted price; (2) the **adjusted
  equity method** (Val 9.3: the participating undertaking's share of the excess of assets over
  liabilities of the related undertaking); (3) Val 6.3 or alternative methods under Val 6.5, but
  **only** if neither (1) nor (2) is possible **and** the undertaking is not a subsidiary
  undertaking. Val 9.2 forces a **zero** value for undertakings excluded from group supervision
  under Group Supervision 2.3 and undertakings deducted from group own funds under Group
  Supervision 10.6. Val 9.4 requires the excess of assets over liabilities of an insurance /
  reinsurance related undertaking or SPV to be computed on **Val 2 + TP + MA + CGB + SCR-GP** bases.
  Val 9.5 permits the IAS equity method for non-insurance related undertakings where Val 9.4 is
  impracticable, with a deduction for goodwill and other Val-8.1 intangibles; Val 9.6 permits the
  financial-statements method where Val 5.4 conditions are met, again with the intangibles
  deduction.
- **Financial liabilities (Val 10.1)** — valued under Val 5 on initial recognition, with **no
  subsequent adjustment for change in own credit standing**.
- **Excluded methods (Val 12.1–12.7)** — no cost or amortised cost for financial assets or
  liabilities (12.1); no lower-of-carrying-amount-and-fair-value-less-costs-to-sell models (12.2);
  no cost-less-depreciation-and-impairment for property, investment property, plant and equipment
  (12.3); finance-lease assets at fair value with market-consistent inputs for minimum lease
  payments and no depreciated cost (12.4); inventories adjusted for material completion and selling
  costs, never at cost (12.5); no nominal-amount valuation of non-monetary grants (12.6); biological
  assets adjusted by material estimated costs to sell (12.7).

### 4. Technical provisions: the top-level requirement [R1]

- **TP 2.1** — establish adequate technical provisions for **all** insurance and reinsurance
  obligations towards policyholders. [Art. 76(1)]
- **TP 2.2** — the value "must correspond to the **current amount that the firm would have to pay
  if it were to transfer its insurance and reinsurance obligations immediately to another UK
  Solvency II firm**". [Art. 76(2)] (date-stamp 31/12/2020 — the post-Brexit substitution of "UK
  Solvency II firm" for "insurance or reinsurance undertaking".)
- **TP 2.3** — calculate technical provisions (1) so the calculation "makes use of and is consistent
  with information provided by the financial markets and generally available data on underwriting
  risks (**market consistency**)"; (2) in a "prudent, reliable and objective manner"; (3) taking
  into account the principles in **Valuation 2**; (4) in accordance with TP 2.4 to 12.2. [Art.
  76(3)–(5)]
- **TP 2.4** — `technical provisions = best estimate + risk margin`, calculated per TP 2.5, 3 and
  4. [Art. 77(1)]
- **TP 14.1** — on PRA request the firm must demonstrate the appropriateness of the level of its
  technical provisions, the applicability and relevance of the methods, and the adequacy of the
  underlying statistical data. [Art. 84]
- **TP 13.1** — the best estimate and its underlying assumptions must be **regularly compared
  against experience**, and where a **systematic deviation** exists the firm must adjust the
  actuarial methods and/or assumptions. [Art. 83]

### 5. The best estimate [R1]

**TP 3.1** — the best estimate must:

1. "correspond to the **probability-weighted average of future cash-flows**, taking into account
   the **time value of money** (expected present value of future cash-flows) using the **relevant
   risk-free interest rate term structure**"; and
2. be calculated (a) "based upon **up-to-date and credible information and realistic
   assumptions**"; (b) "using **adequate, applicable and relevant actuarial and statistical
   methods**"; and (c) **gross**, without deduction of amounts recoverable from reinsurance
   contracts and UK ISPVs, which must be calculated separately under TP 11. [Art. 77(2)]

**TP 3.2** — the cash-flow projection "must take into account **all the cash in- and out-flows
required to settle the insurance and reinsurance obligations over their lifetime**". This applies
whether the best estimate is valued separately **or** the technical provisions are determined on the
basis of financial instruments under TP 2.5.

Qualifying rules in TPFR [R41]:

- **TPFR 12.1** — information is "credible" for TP 3.1 only where the firm can evidence
  credibility, taking into account consistency and objectivity of the information, reliability of
  the source, and transparency of how it is generated and processed.
- **TPFR 7.1** — assumptions are "realistic" for TP 3.1(2)(a) only where **all five** hold: (1) the
  firm can explain and justify each assumption, taking account of its significance, the uncertainty
  involved and relevant alternatives; (2) the circumstances under which the assumption would be
  false "can be clearly identified"; (3) unless otherwise provided, assumptions are based on the
  characteristics of the portfolio **"where possible regardless of the firm holding the
  portfolio"**; (4) assumptions are used consistently over time and within homogeneous risk groups
  and lines of business, without arbitrary changes; (5) assumptions adequately reflect the
  uncertainty underlying the cash flows. The closing paragraph of 7.1 restricts firm-specific
  information (including on claims management and expenses) to cases where it **better reflects the
  portfolio's characteristics** than non-firm-specific information, or where a prudent, reliable
  and objective calculation is impossible without it. **This is the rule that decides when own
  experience may override an industry table** — a live question for CI and IP.
- **TPFR 7.3** — assumptions on future financial market parameters or scenarios must be consistent
  with Val 2 to 12; an economic scenario generator must (1) generate asset prices consistent with
  observed market prices, (2) assume **no arbitrage**, and (3) be calibrated consistently with the
  relevant risk-free interest rate term structure used for the best estimate under TP 3.
- **TPFR 19.1** — the best estimate must be calculated transparently and so that method and results
  are "capable of review by a qualified expert".
- **TPFR 19.2** — method choice must be based on appropriateness to the risks affecting the
  underlying cash flows and the nature of the obligations, and must use all relevant available data.
- **TPFR 19.4 / 19.5** — the firm must analyse the extent to which the present value of cash flows
  depends on expected future outcomes **and** on scenario deviation from the expected outcome; where
  it does, a method reflecting those dependencies must be used. **This is the rule that forces
  stochastic valuation of asymmetric contracts** (with-profits guarantees, GAOs, unit-linked
  maturity guarantees) rather than a single deterministic run.
- **TPFR 15.1** — the projection must, explicitly or implicitly, take account of **all**
  uncertainties, including (1) timing, frequency and severity of insured events; (2) claim amounts
  including claims inflation and the settlement period; (3) expense amounts; (4) expected future
  developments (TPFR 14) so far as practicable; (5) policyholder behaviour; (6) dependency between
  two or more causes of uncertainty; (7) **dependency of cash-flows on circumstances prior to the
  date of the cash-flow** (i.e. path dependency).
- **TPFR 14.1** — the calculation must allow for expected future developments with a material
  impact, "demographic, legal, medical, technological, social, environmental and economic
  developments **including inflation** as referred to in TP 9.1(2)".

### 6. Technical provisions calculated as a whole — the replication rule [R1][R41]

**TP 2.5(1)** — value the best estimate and the risk margin **separately**, except where 2.5(2)
applies. **TP 2.5(2)** — where **(a)** the future cash flows can be **replicated reliably**, **(b)**
the replication is provided using **financial instruments**, and **(c)** those instruments have a
**reliable market value which is observable**, then the technical provisions for those cash flows
"must be determined on the basis of the market value of those financial instruments". [Art. 77(4)]

**TPFR 22** supplies the test:

- **22.2** — replication is reliable only where the cash flows are "replicated **in amount and
  timing** in relation to the underlying risks … and **in all possible scenarios**". Three
  categories **cannot** be reliably replicated:
  1. cash flows depending on the likelihood that policyholders exercise contractual options,
     **including lapses and surrenders**;
  2. cash flows depending on the **level, trend, or volatility of mortality, disability, sickness
     and morbidity rates**;
  3. **all expenses** that will be incurred in servicing insurance and reinsurance obligations.
- **22.3** — financial instruments have a reliable observable market value where traded on an
  "active, deep, liquid and transparent" market; active markets must also comply with **Val 6.4**.
- **22.4** — value the technical provisions at the **market price of the replicating instruments**.

**Practical consequence.** For all seven UK products in this library, 22.2(1)–(3) bite: every
contract carries expenses, and every one carries either mortality/morbidity dependence or a
lapse/surrender option. **TP-as-a-whole is therefore effectively unavailable for the whole-contract
valuation of TA, CI, IP, WOL, WP, ULB and PA.** The residual use is for a *component* — the classic
case being unit-linked benefits where the unit-fund liability is exactly replicated by the units
held — but even there the charges, expenses and mortality element must be valued as a separate
best estimate. Note that the reporting layer expects a TP-as-a-whole amount to be reported
**inside** gross best estimate (IR.12.01 rows R0025/R0026/R0030, [R89]), so the split is a
disclosure attribute, not a separate liability line.

### 7. Recognition, derecognition and contract boundaries [R41]

**TPFR 2.1 (recognition)** — for both the best estimate and the risk margin, recognise an obligation
at **the earlier of** (a) the date the firm becomes a party to the contract giving rise to the
obligation, and (b) the date the insurance or reinsurance **cover begins**. "A firm must only
recognise the obligations **within the boundary of the contract**." Derecognise "only when it is
extinguished, discharged, cancelled or expires".

**TPFR 3 (contract boundary)**:

- **3.2 (the inclusion rule)** — all obligations relating to the contract belong to it, **including
  obligations relating to unilateral rights of the firm to renew or extend the scope of the
  contract** and obligations relating to paid premiums, unless 3.3 to 3.6 say otherwise.
- **3.3 (the exclusion rule)** — obligations relating to cover provided **after** any of the
  following dates do **not** belong to the contract, **unless the firm can compel the policyholder
  to pay the premium** for those obligations:
  1. the future date where the firm has a unilateral right to **terminate** the contract;
  2. the future date where the firm has a unilateral right to **reject premiums** payable under the
     contract;
  3. the future date where the firm has a unilateral right to **amend the premiums or the benefits
     … in such a way that the premiums fully reflect the risks**.
  Limb (3) is assessed **at portfolio level** ("a portfolio of insurance or reinsurance obligations
  in such a way that the premiums of the portfolio fully reflect the risks covered by the
  portfolio"), **except** for long-term insurance business where "an individual risk assessment of
  the obligations relating to the insured person of the contract is carried out at the inception of
  the contract and that assessment cannot be repeated before amending the premiums or benefits" —
  in which case the firm "must assess **at the level of the contract**". *This carve-out is the
  operative rule for individually-underwritten UK protection business (TA, CI, IP, WOL): because
  the medical underwriting cannot lawfully be repeated at a repricing point, the reviewable-rate
  right is tested contract-by-contract, and a reviewable-premium protection policy therefore does
  **not** get its boundary cut at the review date merely because the firm can reprice the book.*
  Final paragraph of 3.3: restrictions on the unilateral right, and limitations on how far premiums
  or benefits can be amended, are ignored where they "have **no discernible effect on the economics
  of the contract**".
- **3.4** — where a unilateral right relates only to **part** of a contract, apply the 3.3
  principles to that part.
- **3.5 (the savings-contract rule)** — obligations that do **not** relate to premiums already paid
  do not belong to the contract if **all three**: (1) the contract does not provide compensation for
  a specified uncertain event that adversely affects the insured person; (2) the contract does not
  include a **financial guarantee of benefits**; and (3) the firm cannot compel payment of the
  future premium. For (1) and (2), events and guarantees with "no discernible effect on the
  economics of the contract" are ignored. *This is the rule that cuts future regular premiums out of
  a pure investment wrapper — but a unit-linked bond with any death-benefit uplift or any
  guarantee fails limbs (1)/(2) and keeps the boundary open.*
- **3.6** — where a contract can be **unbundled** into two parts and one part meets 3.5(1)–(3), the
  obligations not relating to already-paid premiums of that part fall outside the contract.
- **3.7** — premiums "fully reflect the risks" for the purposes of 3.3 only "where there is **no
  circumstance under which the amount of the benefits and expenses payable under the portfolio
  exceeds the amount of the premiums payable** under the portfolio". *A demanding test: any
  scenario in which the portfolio runs at a loss defeats it.*
- **TPFR 23.1** — amounts recoverable from reinsurance contracts and SPVs must be calculated
  **consistently with the boundaries of the contracts of insurance to which they relate**.

### 8. Cash flows in scope [R41]

**TPFR 13.1** — the projection must include **all** of the following, to the extent they relate to
**existing contracts of insurance**:

1. **benefit payments to policyholders**;
2. **payments the firm will incur in providing contractual benefits paid in kind**;
3. **payments of expenses** as referred to in TP 9.1(1);
4. **premium payments and any additional cash-flows that result from those premiums**;
5. **payments between the firm and intermediaries** related to insurance or reinsurance obligations;
6. **payments between the firm and investment firms** in relation to contracts with **index-linked
   benefits and unit linked benefits**;
7. **payments for salvage and subrogation** to the extent they do not qualify as separate assets or
   liabilities under UK-adopted international accounting standards;
8. **taxation payments which are, or are expected to be, charged to policyholders, or are required
   to settle the insurance or reinsurance obligations**.

Notes for a model. Item (5) makes **commission and clawback** an in-scope best-estimate cash flow,
not an expense-loading convention. Item (6) makes the **unit-fund / investment-manager leg**
explicit for ULB and unit-linked WOL. Item (8) is **policyholder-charged tax only** (plus tax needed
to settle obligations) — shareholder corporation tax is **not** a best-estimate cash flow; it enters
through deferred tax under Val 11 [R111]. Item (7) is a general-insurance item with no UK life
application. There is no item for **shareholder transfers**: for with-profits the transfer is
handled through TP 9.1(3) / the Surplus Funds Part [R45] (see §18).

### 9. Expenses and expense inflation [R1][R41]

- **TP 9.1(1)** — when calculating technical provisions, take into account "**all expenses that will
  be incurred in servicing insurance and reinsurance obligations**". [Art. 78]
- **TP 9.1(2)** — take into account "**inflation, including expenses and claims inflation**".
- **TPFR 16.1** — the projection must take into account all four categories of expense relating to
  recognised obligations: **(1) administrative expenses; (2) investment management expenses;
  (3) claims management expenses; (4) acquisition expenses** — and "the expenses referred to in (1)
  to (4) must take into account **overhead expenses** incurred in servicing insurance and
  reinsurance obligations".
- **TPFR 16.2** — overheads "must be allocated in a **realistic and objective manner and on a
  consistent basis over time** to the parts of the best estimate to which they relate".
- **TPFR 16.3** — expenses in respect of reinsurance contracts and SPVs are taken into account in
  the **gross** calculation of the best estimate.
- **TPFR 16.4** — **"Expenses must be projected on the assumption that the firm will write new
  business in the future."** *This is the going-concern expense rule and the single most commonly
  mis-implemented expense requirement: the per-policy maintenance expense is a going-concern unit
  cost, not a run-off unit cost with overheads re-spread over a shrinking book. It is the opposite
  of the risk-margin reference undertaking, which by TP 4B.1(5) writes no new business.*
- **TPFR 15.1(3)** — uncertainty in the amount of TP 9.1(1) expenses must be taken into account.
- **TPFR 14.1** — expected future economic developments **including inflation** must be reflected
  where material.

Nothing in the retrieved rules prescribes an inflation **index** (RPI vs CPI vs national average
earnings), an expense-inflation **rate**, or a **split** between per-policy and per-premium
expenses. Those are assumption choices for the drafter, not sourced parameters.

### 10. Contractual options, financial guarantees and policyholder behaviour [R1][R41]

- **TP 9.2(1)** — take account of "the value of financial guarantees and any contractual options
  included in contracts of insurance and reinsurance contracts". [Art. 79]
- **TP 9.2(2)** — assumptions on the likelihood that policyholders will exercise contractual
  options, **including lapses and surrenders**, must (a) "be **realistic and based on current and
  credible information**" and (b) "take into account, **either explicitly or implicitly, the impact
  that future changes in financial and non-financial conditions may have on the exercise of those
  options**".
- **TPFR 17.1** — the best estimate must take into account **both** (1) all financial guarantees and
  contractual options in the contracts, **and** (2) "**all factors which may affect the likelihood
  that policyholders will exercise contractual options or realise the value of financial
  guarantees**".
- **TPFR 11.1 (policyholder behaviour)** — when determining the likelihood of option exercise
  including lapses and surrenders, the firm must conduct **an analysis of past policyholder
  behaviour and a prospective assessment of expected policyholder behaviour**, taking into account
  **all four** of: (1) "**how beneficial the exercise of the options was and will be to the
  policyholders under circumstances at the time of exercising the option**"; (2) the influence of
  past and future economic conditions; (3) the impact of past and future management actions; (4) any
  other circumstances likely to influence policyholder decisions. Closing sentence: "**The
  likelihood shall only be considered to be independent of the elements referred to in (1) to (4)
  where there is empirical evidence to support such an assumption.**"

*The closing sentence of TPFR 11.1 is the operative rule against a flat, static lapse table. A
constant lapse assumption is permitted only on evidence that behaviour is genuinely independent of
moneyness, economics and management action. For a GAO-bearing WOL/WP contract or a
guarantee-bearing ULB, that evidence will not exist, and a **dynamic lapse function** is required.
For a term assurance with no surrender value the evidence for independence is much easier to
sustain.*

### 11. Future management actions and future discretionary benefits [R41]

**TPFR 8 (future management actions).** Assumptions on future management actions are "realistic" for
TP 3.1(2)(a) only where **all five** of TPFR 8.1 hold:

1. determined in an **objective manner**;
2. **consistent with the firm's current business practice and business strategy**, including the use
   of risk-mitigation techniques — but where "there is sufficient evidence that the firm will change
   its practices or strategy", consistent with the changed practice/strategy;
3. **consistent with each other**;
4. **not contrary to any obligations towards policyholders or to legal requirements** applicable to
   the firm;
5. take account of "**any public indications by the firm as to the actions that it would expect to
   take or not take**".

**TPFR 8.2** — assumptions must include (1) a comparison of assumed future management actions with
**actions actually taken previously**; (2) a comparison with the actions taken into account in
**current and past** best-estimate calculations; (3) an **assessment of the impact of changes** in
those assumptions on the value of the technical provisions. Relevant deviations in (1) and (2) must
be explicable to the PRA, and where a change has a significant impact, the reasons for the
sensitivity and how it is reflected in decision-making must be explicable.

**TPFR 8.3** — the firm must maintain a **comprehensive future management actions plan approved by
the governing body**, providing for all seven of: (1) identification of the relevant actions;
(2) the specific circumstances in which the firm would reasonably expect to carry out each;
(3) **the specific circumstances in which the firm may not be able to carry out each, and how those
circumstances are reflected in the TP calculation**; (4) the **order** in which the actions would be
carried out and the applicable governance requirements; (5) any ongoing work needed to be in a
position to carry them out; (6) how they have been reflected in the best-estimate calculation;
(7) the internal reporting procedures covering them.

**TPFR 8.4** — assumptions "must take account of the **time needed to implement** the management
actions and **any expenses caused by them**".

**TPFR 8.5** — the CGB 2.2 "transmission of information" system is effective only where the TPFR
8.3(7) reporting procedures include **at least an annual communication to the governing body**.

**TPFR 9.1 (future discretionary benefits)** — where future discretionary benefits depend on the
assets held, the best estimate must be based on **the assets the firm currently holds**, with future
changes of asset allocation assumed **in accordance with TPFR 8**; assumed future asset returns must
be consistent with the relevant risk-free interest rate term structure (including, where applicable,
an MA, a VA or the risk-free interest rate transitional measure) and with the Val 2–12 valuation of
the assets. *This is the rule that forbids an assumed equity risk premium in the with-profits
projection: returns are risk-neutral off the relevant curve, and the asset mix starts from the
actual portfolio.*

**TPFR 10.1** — "When calculating technical provisions, a firm must **determine separately the value
of future discretionary benefits**." (A separately-identified FDB quantity is therefore a required
model output, not just a reporting convenience; it is also the quantity SCR-SF 3.3A(1)(c) freezes in
a stress and the basis of loss-absorbing capacity of technical provisions [R112].)

### 12. Segmentation, homogeneous risk groups and lines of business [R1][R41]

- **TP 10.1** — when calculating technical provisions, firms "must segment their insurance and
  reinsurance obligations into **homogenous risk groups and, as a minimum, by lines of business**".
  [Art. 80] (date-stamp 31/12/2024)
- **TPFR 26.1** — the lines of business are those in **Annex 1** to the TPFR Part.
- **TPFR 26.2** — assignment "must reflect the **nature of the risks** relating to the obligation.
  The **legal form** of the obligation **is not necessarily determinative** of the nature of the
  risk."
- **TPFR 26.3** — health insurance obligations pursued on a similar technical basis to **long-term
  insurance business** go to the long-term lines; those on a general-insurance technical basis go to
  the general lines (provided the technical basis is consistent with the nature of the risks).
- **TPFR 26.4** — obligations from the operations in **paragraph V, VI, VII or VIII of Part II of
  Schedule 1 to the Regulated Activities Order** [R14] that cannot clearly be assigned on the basis
  of their nature go to **line of business 32**.
- **TPFR 26.5** — a contract covering both long-term and general insurance business risks **must**
  be unbundled into its two parts.
- **TPFR 26.6** — a contract covering risks across lines of business must, **where possible**, be
  unbundled into the appropriate lines.
- **TPFR 26.7** — a contract including both health obligations and other obligations must, **where
  possible**, be unbundled.
- **TPFR 19.3** — where a calculation method uses grouped policy data, the grouping "creates
  homogeneous risk groups that appropriately reflect the risks of the individual policies included
  in those groups".
- **TPFR 20.1 (the model-point rule for life)** — subject to TPFR 27, cash-flow projections for
  **long-term insurance business** obligations must be made **(1) separately for each policy**, or
  **(2)** for **groups of policies** provided **all three**: (a) "there are **no significant
  differences in the nature and complexity of the risks** underlying the policies that belong to the
  same group"; (b) the grouping "does **not misrepresent the risk** underlying the policies and does
  **not misstate their expenses**"; (c) the grouping "is likely to give **approximately the same
  results** for the best estimate calculation as a calculation on a per policy basis, **in particular
  in relation to financial guarantees and contractual options** included in the policies".
- **TPFR 21** (general insurance only, recorded for completeness) — the best estimate is split
  between a **premium provision** (future claim events within the contract boundary; cash flows
  include benefits, expenses and premiums relating to those events, 21.2) and a **provision for
  claims outstanding** (claim events that have already occurred, reported or not, 21.3–21.4). **No
  equivalent split is imposed on long-term business.** Note that a UK IP or CI writer whose business
  is written on a general-insurance technical basis lands in LoB 2 or 1 and inherits this split.

**Annex 1 — lines of business (the taxonomy a UK life model must key on).**
Part A (general insurance business obligations): **1** medical expense insurance; **2** income
protection insurance; **3** workers' compensation insurance; **4** motor vehicle liability; **5**
other motor; **6** marine, aviation and transport; **7** fire and other damage to property; **8**
general liability; **9** credit and suretyship; **10** legal expenses; **11** assistance; **12**
miscellaneous financial loss. LoB 1 and 2 are expressly "where the underlying business is **not**
pursued on a similar technical basis to that of long-term insurance business".
Part B: **13–24** proportional general reinsurance corresponding to 1–12 respectively.
Part C: **25** non-proportional health reinsurance (relating to LoB 1–3); **26** non-proportional
casualty (LoB 4 and 8); **27** non-proportional marine, aviation and transport (LoB 6); **28**
non-proportional property (LoB 5, 7 and 9–12).
**Part D (long-term insurance business obligations) — the four that matter here:**

| LoB | Title | Definition as printed |
|---|---|---|
| **29** | Health insurance | health insurance obligations where the underlying business **is** pursued on a similar technical basis to that of long-term insurance business, other than those in LoB 33 |
| **30** | Insurance with profit participation | insurance obligations with profit participation other than those in LoB 33 and 34 |
| **31** | Index-linked and unit-linked insurance | insurance obligations with index-linked benefits and unit linked benefits other than those in LoB 33 and 34 |
| **32** | Other long-term insurance business | long-term insurance business obligations other than those in LoB 29 to 31, 33 and 34 |
| **33** | — | annuities stemming from **general insurance business** contracts and relating to health insurance obligations |
| **34** | — | annuities stemming from **general insurance business** contracts and relating to obligations other than health insurance obligations |

Part E (long-term reinsurance): **35** health reinsurance (relating to LoB 29 and 33); **36**
long-term reinsurance (relating to LoB 30 to 32 and 34).

**Mapping the seven library products** (this mapping is the drafter's inference from TPFR 26.2/26.3
and the Annex 1 definitions, **not** a quotation): non-profit TA, WOL and PA sit in **LoB 32**;
unit-linked ULB and unit-linked WOL sit in **LoB 31**; with-profits business sits in **LoB 30**;
IP and CI sit in **LoB 29** if written on a long-term technical basis and in **LoB 2 / LoB 1**
respectively if not — TPFR 26.3 makes the technical basis, not the product label, decisive. A
with-profits contract with unit-linked elements or a unit-linked contract with a with-profits
element must be unbundled under TPFR 26.6 "where possible".

### 13. Currency [R41]

**TPFR 18.1** — "The best estimate **must be calculated separately for cash-flows in different
currencies**." **TPFR 25** permits the EUR basic curve, adjusted for currency risk, for obligations
in a currency pegged to the EUR, subject to four conditions (25.1: the peg keeps the exchange rate
within a range not wider than **20% of the upper limit of the range**; sufficiently similar economic
situations; the peg holds over one year under extreme events at the SCR-GP 3.3/3.4 confidence level,
taking into account the financial resources of the parties guaranteeing the peg; and one of ERM II
participation, a Council of the European Union decision recognising the peg, or the peg established
by the law of the country establishing the currency). **TPFR 25.2** — the currency-risk adjustment
"**must be negative**" and must correspond to the cost of hedging the risk that the pegged-currency
value of a EUR-denominated investment falls. GBP is not pegged to the EUR; TPFR 25 is inapplicable
to a sterling UK book and is recorded only so a drafter does not mistake it for a general
currency rule.

### 14. Reinsurance recoverables and the counterparty-default adjustment [R1][R41]

**TP 11.1** — (1) calculate amounts recoverable from reinsurance contracts and UK ISPVs **in
accordance with TP 2 to 10** (i.e. the same valuation apparatus as the gross best estimate); (2)
take into account "**the time difference between amounts becoming recoverable and the actual receipt
of those amounts**"; (3) **adjust** the calculation "to take into account **expected losses due to
the default of the counterparty**", based on "an assessment of the **probability of default** of the
counterparty and the **average loss that would result from that default (loss-given-default)**".
[Art. 81]

**TPFR 23 (general provisions)**:

- **23.1** — recoverables calculated **consistently with the contract boundaries** of the underlying
  insurance contracts.
- **23.2** — recoverables from **SPVs**, from **finite reinsurance contracts** as referred to in
  **CGB 8.1** [R92], and from **other reinsurance contracts** must **each be calculated
  separately**; amounts recoverable from an SPV must not exceed that SPV's **aggregate maximum risk
  exposure** to the firm.
- **23.3** — recoverable cash flows include **only** payments in relation to compensation of
  insurance events and unsettled insurance claims; payments for other events or settled claims are
  accounted for outside the recoverables and outside the other elements of technical provisions;
  where a **deposit** has been made for the cash flows, the recoverables must be adjusted to avoid
  double counting.
- **23.4** — (general insurance) recoverables split between premium provisions and provisions for
  claims outstanding.
- **23.5** — where SPV cash flows do not directly depend on the claims against the ceding firm,
  recoverables for future claims count **only** to the extent it can be verified "in a prudent,
  reliable and objective manner" that the **structural mismatch** is not material.

**TPFR 24 (counterparty default adjustment)**:

- **24.1** — the adjustment must be **calculated separately** from the rest of the amounts
  recoverable.
- **24.2** — it "must be calculated as the **expected present value of the change in cash-flows
  underlying the amounts recoverable from that counterparty, that would arise if the counterparty
  defaults, including as a result of insolvency or dispute, at a certain point in time**". The change
  in cash flows **must not** take into account the effect of any risk-mitigation technique that
  mitigates the counterparty's credit risk, **other than risk-mitigation techniques based on
  collateral holdings**; the excluded techniques are recognised separately, without increasing the
  recoverable.
- **24.3** — the calculation must take into account **possible default events over the lifetime of
  the contract** and **whether and how the probability of default varies over time**, and must be
  carried out **separately by each counterparty and for each line of business**.
- **24.4** — **"The average loss resulting from a default of a counterparty … must not be assessed
  at lower than 50% of the amounts recoverable excluding the adjustment referred to in 24.1, unless
  there is a reliable basis for another assessment."** *This is the only hard numeric floor in the
  whole technical-provisions apparatus: an LGD floor of **50%**, rebuttable only on a reliable
  basis.*
- **24.5** — the probability of default of an SPV is calculated on the basis of the **credit risk
  inherent in the assets held by the SPV**.

Supervisory overlay: SS5/24 [R47] on funded reinsurance (immediate-recapture metric, worst-case
collateral assumptions inside an MA portfolio) and SS18/16 [R48] on longevity risk transfers (SCR
counterparty-default capital "may not be sufficient in and of itself").

### 15. Data quality, approximations and proportionality [R1][R41]

- **TP 12.1** — data used in the calculation of technical provisions must be "**appropriate,
  complete and accurate**".
- **TP 12.2** — where data of appropriate quality is insufficient to apply a reliable actuarial
  method to a set or subset of obligations or recoverables, firms **may use appropriate
  approximations, including case-by-case approaches**, in the calculation of the best estimate.
  [Art. 82]
- **TPFR 4.1 (complete)** — the data (1) "include sufficient historical information to assess the
  characteristics of the underlying risks **and to identify trends** in the risks"; and (2) "are
  available **for each of the relevant homogeneous risk groups**" and no relevant data is excluded
  without justification.
- **TPFR 4.2 (accurate)** — (1) free from material errors; (2) data from different time periods used
  for the same estimation are **consistent**; (3) recorded in a **timely** manner and consistently
  over time.
- **TPFR 4.3 (appropriate)** — six conditions: (1) consistent with the purposes for which they will
  be used; (2) amount and nature ensure no **material estimation error** (material = could influence
  the decision-making or judgement of the users, including a supervisory authority); (3) consistent
  with the assumptions underlying the techniques applied; (4) appropriately reflect the risks;
  (5) collected, processed and applied "in a transparent and structured manner, based on a
  documented process" comprising (a) data-quality criteria and an assessment including specific
  qualitative and quantitative standards for different data sets, (b) the use and setting of
  assumptions in collection/processing/application, (c) the update process including **frequency of
  updates and the circumstances that trigger additional updates**; and (6) data used **consistently
  over time**.
- **TPFR 4.4 (external data)** — permitted only if, in addition to 4.1–4.3: (1) the firm can
  demonstrate external data is **more suitable** than exclusively internal data; (2) the firm knows
  the **origin** of the data and the assumptions/methodologies used to process it; (3) the firm
  identifies trends in the data and variation over time or across data in those assumptions or
  methodologies; and (4) the firm can demonstrate those assumptions and methodologies **reflect the
  characteristics of its own portfolio**. *This is the rule a UK model must satisfy to use a CMI
  table or an industry IP inception basis: the firm must know how the table was built and evidence
  that it fits its portfolio.*
- **TPFR 5.1 (limitations)** — where data does not comply with TPFR 4, the firm must document the
  limitations, "including a description of whether and how such limitations will be remedied and of
  the functions within the system of governance … responsible for that process", and the
  **pre-adjustment data must be recorded and stored**.
- **TPFR 6.1 (approximations)** — approximations may be used only where **all three**: (1) the data
  insufficiency "is not due to inadequate internal processes and procedures of collecting, storing
  or validating data"; (2) it cannot be remedied by external data; (3) it would not be practicable
  to adjust the data to remedy it.
- **TPFR 27 (proportionality)** — 27.1: methods must be **proportionate to the nature, scale and
  complexity** of the risks. 27.2: the proportionality assessment comprises (1) an assessment of the
  nature, scale and complexity of the risks, and (2) an evaluation, qualitative or quantitative, of
  the **error** introduced by deviation between the method's assumptions about the risks and the
  results of that assessment. 27.3: the assessment must include **all risks which affect the amount,
  timing or value** of the cash flows over their lifetime; **for the risk margin, over the lifetime
  of the underlying obligations**; restricted to the risks relevant to the part of the calculation to
  which the method is applied. 27.4: a method is **disproportionate** if the error leads to a
  misstatement of technical provisions or their components that could influence the intended user's
  decision-making or judgement — **unless** (1) no other method with a smaller error is available
  and the method is not likely to result in an underestimation, or (2) the method produces technical
  provisions **higher** than a proportionate method would and does not underestimate the risk.
  *In short: a simplification is permitted where it is not available to do better, or where it is
  demonstrably prudent. There is no "immaterial, therefore ignore" limb.*

### 16. The risk margin [R1][R4][R44]

**TP 4.1** — where a firm values the best estimate and the risk margin separately, the risk margin is
"an amount equal to the **cost that a UK Solvency II firm would incur in order to hold eligible own
funds to cover the SCR necessary to support the insurance and reinsurance obligations over their
lifetime**, determined using the cost-of-capital rate". [Art. 77(5)]
**TP 4.2** — the risk margin must ensure the technical provisions equal the amount a UK Solvency II
firm "would be expected to require in order to take over and meet" the obligations over their
lifetime. [Art. 77(3)]

**TP 4A.1 — the formula, transcribed from the Rulebook LaTeX.** In plain-text notation:

```
RM = CoC * SUM over t >= 0 of  [ SCR(t) * max( lambda^t , lambda_floor ) ] / ( 1 + r(t+1) )^(t+1)
```

where (TP 4A.1(1)–(8), identical in substance to IRPR reg 7B(a)–(h) [R44]):

| Symbol | Meaning | Value |
|---|---|---|
| RM | risk margin | — |
| CoC | the cost-of-capital rate | **4%** (TP 1.2, citing IRPR reg 7B(b)) |
| t | the sum "covers all integers including zero" | 0, 1, 2, … |
| SCR(t) | the **reference undertaking notional SCR** after t years | model output |
| lambda | the risk **tapering factor** | **0.9** for long-term insurance and reinsurance obligations; **1.0** for general insurance and reinsurance obligations |
| lambda^t | the tapering factor to the power of t years | — |
| lambda_floor | the floor of the tapering factor | **0.25** |
| r(t+1) | the **basic** relevant risk-free interest rate for maturity t+1 years, "derived from the basic relevant risk-free interest rate term structure and **selected in accordance with the currency used for the firm's financial statements**" | published curve |

Notes on the formula as printed. (a) The discounting is at **t+1**, not t — the term-t capital charge
is discounted over t+1 years. (b) The taper is `max(lambda^t, lambda_floor)`, so with lambda = 0.9
the taper decays until `0.9^t = 0.25`, i.e. **the floor binds from the first integer t with
0.9^t <= 0.25** (the arithmetic threshold is t = ln 0.25 / ln 0.9 ≈ 13.16, so the floor binds from
**t = 14** onward; this arithmetic is the drafter's, derived from the rule, and is **not** stated in
any retrieved source). (c) The rate is the **basic** curve — **no MA, no VA, no transitional** —
consistent with TP 4B.1(13). (d) The currency is that of the **financial statements**, not of the
obligations. (e) The calculation is for "the **whole portfolio** of insurance and reinsurance
obligations" (TP 4A.1 opening words and IRPR reg 7B) — the risk margin is not built bottom-up from
lines of business.

**TP 4A.2** — a firm with **internal model permission** must, "**unless it is inappropriate to do
so**", use that internal model to calculate the reference undertaking notional SCR.

**TP 4A.3 (allocation)** — the firm "must **allocate** the risk margin for the whole portfolio … to
**each relevant line of business**" and the allocation "must adequately reflect the **contributions
of the lines of business to the reference undertaking notional SCR over the lifetime** of the whole
portfolio". *No allocation formula is prescribed.*

**TP 4B.1 — the reference undertaking assumptions.** The risk margin must be based on all thirteen:

1. the whole portfolio of obligations is taken over by a **reference undertaking**;
2. a **composite firm** must assume its general insurance business and its long-term insurance
   business are each taken over **separately by two different reference undertakings**;
3. the transfer **includes any reinsurance contracts and SPV arrangements** relating to those
   obligations;
4. the reference undertaking has **no** obligations and **no own funds** before the transfer;
5. after the transfer the reference undertaking **assumes no new obligations**;
6. after the transfer it **raises eligible own funds equal to the reference undertaking notional
   SCR** necessary to support the obligations over their lifetime;
7. after the transfer it holds **assets equal to the notional SCR plus its technical provisions net
   of reinsurance and SPV recoverables**;
8. those assets are selected "in such a way that they **minimise the reference undertaking notional
   SCR for market risk**" to which it is exposed;
9. the notional SCR captures **all** of: (a) **underwriting risk** on the transferred business;
   (b) where material, the **market risk** in (8) **other than interest rate risk**; (c) **credit
   risk** on reinsurance contracts, SPV arrangements, intermediaries, policyholders and any other
   material exposures closely related to the obligations; (d) **operational risk**;
10. the **loss-absorbing capacity of technical provisions** for the reference undertaking
    corresponds, per risk, to that of the firm;
11. there is **no loss-absorbing capacity of deferred taxes** for the reference undertaking;
12. the reference undertaking adopts **future management actions consistent with the firm's** assumed
    future management actions per **TPFR 8**, subject to (5) and (6);
13. the reference undertaking applies **none** of: (a) matching adjustment; (b) volatility
    adjustment; (c) risk-free interest rate transitional measure; (d) TMTP.

**TP 4B.2** — over the lifetime of the obligations, the SCR referred to in TP 4.1 "must be assumed
to be equal to the reference undertaking notional SCR". **TP 4B.3** — a risk is "material" for
4B.1(9) where its impact on the risk margin "could influence the decision-making or the judgment of
the users of that information, including the PRA and FCA".

**Lloyd's variant** — TP 16.2: managing agents read "SCR" in TP 4.1 as the **notional syndicate
SCR** required by SCR – General Provisions 8.2.

**No simplification hierarchy exists in UK rules.** See Scope note 2 and §19 below.

**Statutory provenance:** SI 2023/1346 [R4] amended DR (EU) 2015/35 Article 37(1) — substituting the
formula and inserting sub-paragraphs (e) λ = 0.9 life / 1.0 non-life, (f) λ^t, (g) λ_floor = 0.25 —
and Article 39, substituting "**4%**" for "**6%**"; made 7 December 2023, laid 8 December 2023, in
force **31 December 2023**. It also amended DR Article 312 (omitting paragraphs 1(a) and 3, and
truncating paragraph 2) and regulation 54(9) of the Solvency 2 Regulations 2015 (SI 2015/575),
omitting sub-paragraph (b). Its explanatory note records that DR 2015/35 and SI 2015/575 "are
revoked by section 1(1) of, and Schedule 1 to, the Financial Services and Markets Act 2023". The
substance now sits in **IRPR regs 7A–7C** [R44] and **TP 4A/4B** [R1].

### 17. Is there a floor on a negative best estimate? — settled: **no** [R1][R39][R41]

This matters because profitable protection business (TA, CI, and level-premium WOL in the early
years) commonly produces a **negative** best-estimate liability: the present value of future
premiums exceeds the present value of future claims and expenses inside the contract boundary.

What the retrieved rules say:

1. **TP 3.1** defines the best estimate as the probability-weighted average of future cash-flows,
   discounted. It contains **no floor, no minimum, and no reference to a surrender value or account
   value**.
2. **TP 2.2** requires the technical provisions to correspond to a **transfer value**. A transfer
   value of a profitable portfolio is legitimately negative before the risk margin.
3. **TP 2.4** adds a risk margin, which is **always non-negative** by construction (CoC, SCR(t),
   max(λ^t, λ_floor) and the discount factor are all non-negative). So the risk margin partially
   offsets, but does not floor, a negative best estimate.
4. A full-text search for "negative" across the **Valuation, Technical Provisions and
   Technical Provisions – Further Requirements Parts** returns exactly **one** hit: TPFR 25.2 (the
   EUR-peg currency-risk adjustment "must be negative"). There is no zero floor, no surrender-value
   floor, and no per-contract or per-homogeneous-risk-group non-negativity rule.
5. **Val 5.5 and 5.6** require individual assets and liabilities to be valued separately, but
   Val 4.1 expressly excludes technical provisions from Chapters 5 to 12 — so the separate-valuation
   rule does **not** import a contract-level floor into the best estimate.
6. **TPFR 20.1** permits grouping only where the group gives approximately the same result as a
   per-policy calculation. This constrains **offsetting inside a group** (a group mixing profitable
   and loss-making policies must not misrepresent the risk or misstate expenses) but again imposes
   no floor.
7. The reporting layer treats a **surrender value** as a **disclosure item** in IR.14.01, described
   as "the amount of surrender value net of taxes" [R89] — not as a valuation constraint on the
   best estimate.

**Conclusion for the library:** under Solvency UK the best estimate may be, and for new protection
business normally will be, negative; nothing in the Technical Provisions, TPFR or Valuation Parts
floors it. This is a genuine difference from U.S. statutory reserving (see `us/regulatory/`, where
formulaic minimums and, under PBR, the net premium reserve floor operate) and from IFRS 17, where a
group of contracts cannot carry a negative liability *for the contractual service margin* (the
fulfilment cash flows themselves can be negative). **This paragraph is a comparison drawn by the
drafter, not a claim sourced from any retrieved UK document.**

Two things that *do* constrain the number and are sometimes mistaken for a floor:

- **The contract boundary (TPFR 3.3, 3.5, 3.7)** — the more aggressively the boundary cuts future
  premiums, the less negative the best estimate can be. For a reviewable-rate protection contract
  the 3.3 long-term carve-out generally keeps the boundary open (see §7), so this is not a
  back-door floor either.
- **Own funds tiering and the reconciliation reserve** — the Own Funds Part records that "**the
  reconciliation reserve may be positive or negative**" (Own Funds 3C, read incidentally in
  `cap-own-funds.txt`; the Own Funds Part is owned by the capital stream and is cited here only for
  this one sentence). A negative best estimate therefore feeds own funds, subject to tiering
  limits, ring-fenced-fund restrictions (Own Funds 3L) and any MA-portfolio restriction — all of
  which are the capital stream's, not this one's.

### 18. With-profits: the surplus-funds boundary of technical provisions [R1][R45][R46]

- **TP 9.1(3)** — when calculating technical provisions, take into account "all payments to
  policyholders, **including future discretionary bonuses**, which firms expect to make, **whether
  or not those payments are contractually guaranteed**, **unless** those payments fall within
  **Surplus Funds 2.1**". [Art. 78]
- **Surplus Funds 2.1** — a firm "shall **not treat surplus funds as insurance and reinsurance
  obligations** when valuing payments to policyholders and beneficiaries in the calculation of
  technical provisions in accordance with Technical Provisions 2". [Art. 78(3) and Art. 91(2)]
- **Surplus Funds 2.2** — to comply, the firm must calculate the amount of its surplus funds under
  Surplus Funds 3.
- **SS13/15 ¶2.1** [R46] — the exclusion operates only where the surplus funds meet the **Tier 1 own
  funds** requirements in **Own Funds 3.1**. ¶2.3 — surplus funds will normally meet the Tier 1
  criteria but are "likely to be treated as part of a ring-fenced [fund]".
- **SS13/15 ¶2.4** — the surplus-funds calculation "**does not refer to or include a risk margin**";
  the firm must still calculate and recognise the risk margin on its business as a whole, including
  with-profits business.
- **Surplus Funds 3.1** — surplus funds = with-profits assets − with-profits policy liabilities − tax
  and other costs arising on recognition of future shareholder transfers attributable to the fund
  (to the extent not in the second item) − other liabilities properly attributable to the fund −
  the value attributable to **future shareholder transfers** (computed by reference to the
  3.5(3) benefits and consistently with the 3.4 method).
- **Surplus Funds 3.2/3.3 (retrospective default)** — value with-profits policy liabilities (other
  than **future policy-related liabilities**) as the aggregate **retrospective** value per policy of
  ten items: premiums received; investment income and asset value movements; permanent enhancements;
  past miscellaneous surplus/deficit allocated; expenses incurred or deducted; past deductions for
  cost of guarantees and smoothing, options and life cover; partial benefits paid or due; tax paid
  or payable attributable to the policy; reinsurance amounts; past shareholder transfers, **less any
  implicit allowance for the value of future shareholder transfers**. (This is the regulatory
  asset-share definition.)
- **Surplus Funds 3.4 (prospective fallback)** — where 3.3 "does not adequately reflect the value" or
  is impracticable, value as the aggregate net present value of six expected future cash flows:
  future premiums; expenses expected to be incurred or deducted; **planned deductions for the cost
  of guarantees and smoothing, options and provision of life cover and any other benefits**;
  benefits of the 3.5 type; reinsurance amounts (excluding those already allowed for); tax payable.
- **Surplus Funds 3.5** — the 3.4(4) benefits are (1) **all guaranteed benefits**, including amounts
  guaranteed on death and maturity or other events, **guaranteed surrender values and paid-up
  values**; (2) **declared bonuses to which the policyholder is contractually entitled**; and (3)
  future discretionary additions and discretionary payments expected when benefits become payable,
  **only to the extent they are consistent with what the retrospective calculation would have
  allowed for**.
- **Surplus Funds 3.6** — no charge may be attributed to a with-profits policy unless permitted by
  the FCA Handbook [R9].
- **Surplus Funds 4.1** — the surplus-funds valuations must be **consistent with the valuation
  methodologies adopted for the technical provisions under TP 2**.
- **SS13/15 ¶3.1** — whole-of-life policies, or policies where the retrospective result "might be
  negative or significantly lower than the value calculated using the prospective approach", are
  examples where the prospective approach may be necessary. **¶3.2** — grouping is permitted where
  it gives the same or a higher result, does not materially misrepresent exposure or misstate the
  costs of guarantees, options or smoothing, and groups policies with similar attributes "including
  the status of guarantees". **¶3.4** — "permanent enhancements" means amounts expected to be
  permanent "in all but the most extreme adverse circumstances". **¶3.5** — "miscellaneous surplus"
  captures fund experience surplus/deficit, e.g. mortality or expense experience relative to
  expectations, or profits or losses from **non-profit business inside the with-profits fund**.
  **¶3.6** — the PRA "would not expect a firm to include within benefits payable **distributions from
  the estate**" it might make over the life of the policies in run-off.

Also relevant to a with-profits model: the **With-Profits Part** (read incidentally,
https://www.prarulebook.co.uk/pra-rules/with-profits/05-08-2026, HTTP 200 verified 2026-08-06,
all rules date-stamped 01/01/2016) requires assets in each with-profits fund sufficient to cover the
with-profits policy liabilities (2.1), a distribution strategy that is "affordable and sustainable"
and cannot reasonably be expected to have an adverse effect on safety and soundness or benefit
security (3.1), and documentation of support arrangements (4.1). It is **not** numbered here; the
with-profits product stream should number it if it cites it.

### 19. What Solvency UK did *not* carry over from the Delegated Regulation [R41][R42][R49]

| DR (EU) 2015/35 provision | Status in Solvency UK |
|---|---|
| Art. 17–36 (TP methodology detail) | restated as **TPFR 2–22** [R41] |
| Art. 37 (calculation of the risk margin) | restated as **TP 4A.1**; statutory basis **IRPR reg 7B** |
| Art. 38 (reference undertaking assumptions) | restated as **TP 4B.1** |
| Art. 39 (cost-of-capital rate) | **4%** in TP 1.2 and IRPR reg 7B(b) |
| Art. 40–56 (recoverables, LoB, proportionality) | restated as **TPFR 23–27** and **Annex 1** |
| **Art. 57** simplified recoverables | **not restated** |
| **Art. 58** simplified risk margin | **not restated** — no UK method hierarchy exists |
| **Art. 59** | **not restated** |
| **Art. 60** simplified best estimate, premium-adjustment mechanism | **not restated** |
| **Art. 61** simplified counterparty-default adjustment | **not restated** |
| Art. 1(*) EPIFP definition | **not restated**; EPIFP deleted from S.23.01 per PS3/24 [R86 ¶4.43] |
| Art. 312 (reporting deadlines) | amended by [R4]; reporting is [R84]'s |

What a firm may rely on instead: **TPFR 27 proportionality** for the technical provisions generally;
**TP 12.2 / TPFR 6.1** for data-driven approximations; **SCR-SF 3.3A(3)** [R42] for simplified
post-scenario technical provisions inside an SCR module; and, prospectively, any rule the PRA makes
under the power preserved by **IRPR reg 7C** [R44]. The absence of a codified risk-margin
simplification means a UK model that needs SCR(t) must either project the reference undertaking
notional SCR directly or justify its own proxy (a driver-based run-off) against TPFR 27.4 — there is
no rule text sanctioning a specific proxy.

### 20. Effective dates — the timeline a drafter must not blur

| Date | Event | Source |
|---|---|---|
| 01/01/2016 | Solvency II onshored start; Valuation Ch. 1–2, TP 2.1/2.3/2.4/2.5/3.2/5/9/10/12.1/13/14/16, Surplus Funds Ch. 1–4, With-Profits Part date-stamps | [R39][R1][R45] |
| 31/12/2020 | End of the EU transition period; TP 2.2, 3.1, 4.1, 4.2, 11.1, 12.2 re-stamped (UK-specific wording) | [R1] |
| 31/12/2023 | **SI 2023/1346 in force** — CoC 6% → 4%, λ = 0.9/1.0 with 0.25 floor | [R4] |
| 01/04/2024 | IRPR Regulations 2023 in force **for the purposes of reg 7** (fundamental spread rule-making) | [R44 reg 1(2)] |
| 30/06/2024 | IRPR Regulations 2023 in force for all other purposes; **TP Chapters 6 and 7 deleted**; MA Part created; *basic relevant risk-free interest rate term structure*, *matching adjustment*, *expense risk* glossary entries re-stamped | [R44][R1][R2][R5][R43] |
| 01/11/2024 | SI 2024/1083 in force "for specified purposes" — inserting IRPR Part 2 Chapter 2 (regs 7A–7C) | [R44] textual amendment note |
| 05/11/2024 | PRA Rulebook: Solvency II Instrument 2024 (PRA2024/13) made by the PRC | [R42] |
| 15/11/2024 | SS38/15, SS13/15, SS18/16 updated alongside PS15/24 | [R40][R46][R48] |
| **31/12/2024** | **PRA2024/13 in force** — Valuation Ch. 3–12, the whole TPFR Part, TP 1.2/4A/4B/10.1, and the 31/12/2024 glossary entries all take effect. The single most important date in this stream. | [R42][R39][R41][R1][R43] |
| 20/12/2024 | PRA statement correcting SCR-SF 3B6.6(1) (mass lapse) in PS15/24 | note on p.1 of [R42] |
| 02/01/2026 | Annex M (Own Funds) of PRA2024/13 comes into force | [R42] |
| 05/08/2026 | "Present" view of the Rulebook read for this file | [R1][R39][R41][R43][R45] |

### 21. Where the technical-provisions rules hand off to sibling streams

- **Discount rate** — TP 3.1(1) uses the *relevant* risk-free interest rate term structure. TP 5.1
  requires it to be derived from relevant financial instruments, to take account of maturities where
  markets for those instruments and for bonds are "deep, liquid and transparent", and to be
  extrapolated only where they are not; TP 5.2 requires forward rates converging smoothly to an
  **ultimate forward rate** [Art. 77a]. The curve itself, its published technical information, the
  MA and the VA are **stream B**. TP 8.1 permits a VA only with a **volatility adjustment
  permission** under FSMA s.138BA, only where the VA has been published by the PRA under IRPR reg 3,
  and only to the extent of the permission; TP 8.2 bars the VA from extrapolated rates; TP 8.3 bases
  the extrapolation on VA-adjusted rates where a VA applies; **TP 8.5 bars the VA where the curve
  already includes a matching adjustment**. TP 4B.1(13) excludes MA, VA, the risk-free transitional
  and TMTP from the **reference undertaking**.
- **SCR(t)** — the reference undertaking notional SCR is defined here (TP 4B.1) but computed under
  the SCR Parts (**stream C**), including the internal-model route in TP 4A.2.
- **Own funds and the reconciliation reserve** — **stream D**.
- **Reporting granularity** — IR.12.01 / IR.12.04 / IR.12.05 / IR.12.06 / IR.14.01 and the MA returns
  are **[R89]–[R91]**.
- **Governance** — the actuarial function's responsibility for the technical provisions, expert
  judgement, and validation are **[R92]**; TPFR 8.5 explicitly qualifies **CGB 2.2**.
- **Accounting** — the FRS 102 / FRS 103 / IFRS 17 measurement bases and the deferred-tax
  interaction are **[R99]–[R113]**; Val 11 is **[R111]**.

---

## Model hooks

What a liability cash flow projection must produce, at what granularity, on what basis, at what date.

| Item | What the liability model must produce | Granularity / basis / timing |
|---|---|---|
| **Best-estimate liability (gross)** [R1 TP 3.1] | Probability-weighted expected present value of all in-scope cash flows, **gross of reinsurance**, discounted on the relevant risk-free curve | Per homogeneous risk group, minimum per line of business (TP 10.1); per policy or per compliant group (TPFR 20.1); at each valuation date |
| **Cash-flow inventory** [R41 TPFR 13.1] | Eight streams, separately identifiable: benefits; benefits paid in kind; expenses; premiums **and cash flows resulting from premiums**; **intermediary payments**; **payments to/from investment firms for index-linked and unit-linked benefits**; salvage/subrogation; **policyholder-charged taxation** | Per model point per projection period; never netted into a single "net cash flow" line, because the reporting layer [R89] and the LoB split need them apart |
| **Contract-boundary flag** [R41 TPFR 2.1, 3.1–3.7] | Per contract: recognition date = earlier of party-to-contract and cover-start; a boundary end-date; and the test that produced it (3.3(1) termination right / 3.3(2) premium-rejection right / 3.3(3) repricing right assessed **at contract level** for individually-underwritten long-term business / 3.5 no-insurance-risk-and-no-guarantee / 3.6 unbundled part) | Per contract; must be re-derived whenever product terms change, not stored as a product constant |
| **Expense model** [R1 TP 9.1(1)-(2)][R41 TPFR 16] | Four expense categories (administrative, investment management, claims management, acquisition), each including allocated **overheads**; an overhead allocation rule stable over time; an expense-inflation series; **on a going-concern basis assuming future new business is written** | Per model point per period; the going-concern unit cost differs from the run-off unit cost used inside the reference undertaking |
| **Option and guarantee valuation** [R1 TP 9.2][R41 TPFR 17, 19.4–19.5] | Time value as well as intrinsic value wherever the present value depends on scenario deviation; a market-consistent, arbitrage-free, curve-calibrated ESG (TPFR 7.3) | Per contract or compliant group, stochastic where asymmetric; per scenario per period |
| **Policyholder behaviour** [R1 TP 9.2(2)][R41 TPFR 11.1] | A lapse/surrender/option-take-up function conditioned on **moneyness, economic conditions and management actions**, backed by an analysis of past behaviour and a prospective assessment; a static assumption only with empirical evidence of independence | Per homogeneous risk group; the dependency structure is an input, not a scalar |
| **Future management actions** [R41 TPFR 8] | A board-approved management-actions plan mapped into the model: the actions, their trigger circumstances, the circumstances in which they **cannot** be taken, their **order**, their **implementation lag** and **their expenses** | Per fund/portfolio; applied per scenario per period; frozen out of SCR scenarios except as SCR-SF 3.3A(2)(a) allows [R42] |
| **Future discretionary benefits** [R41 TPFR 9.1, 10.1] | The FDB amount **determined separately**; asset-dependent FDB projected off the **currently held** assets with allocation changes only per TPFR 8, and asset returns consistent with the relevant curve | Per with-profits fund per period; also the LACTP input [R112] |
| **Reinsurance recoverables** [R1 TP 11.1][R41 TPFR 23, 24] | Recoverables on the **same** basis as the gross best estimate, on the **same contract boundaries**, with a **settlement-timing lag**; split three ways (SPVs / finite reinsurance per CGB 8.1 / other reinsurance); and a **separately calculated counterparty-default adjustment** with PD term structure and **LGD not below 50%** | Per counterparty **and** per line of business; SPV recoverable capped at the SPV's aggregate maximum risk exposure |
| **Risk margin** [R1 TP 4A, 4B][R44] | A projected **reference undertaking notional SCR** run-off SCR(0), SCR(1), …; the CoC discount at the **basic** curve in the **financial-statements currency**; the taper `max(0.9^t, 0.25)` for long-term obligations; and an **allocation to lines of business** reflecting their contribution to SCR(t) over the lifetime | Whole portfolio (composites: two portfolios); annual integer time steps from t = 0; no MA/VA/transitional/TMTP inside |
| **TP-as-a-whole flag** [R1 TP 2.5(2)][R41 TPFR 22] | For any component whose cash flows are reliably replicable by market-valued instruments, the market value of the replicating instruments — and evidence the TPFR 22.2 exclusions (option-dependence, mortality/morbidity-dependence, expenses) do not apply | Per component; reported **inside** gross best estimate per IR.12.01 [R89] |
| **Segmentation keys** [R1 TP 10.1][R41 TPFR 20, 26, Annex 1] | Every model point tagged with (a) a line of business from Annex 1 (29/30/31/32 for long-term; 1/2 for GI-basis health), (b) a homogeneous risk group, (c) a currency, (d) a fund (with-profits fund / ring-fenced fund / MA portfolio / remaining part), (e) a technical-basis flag for health business per TPFR 26.3 | Per model point, fixed at set-up, revisited when products change |
| **Currency split** [R41 TPFR 18.1] | Separate best-estimate calculations per currency of cash flow | Per currency; not a post-hoc FX translation of a single-currency result |
| **Data-quality artefacts** [R1 TP 12][R41 TPFR 4, 5, 6] | Evidence of completeness (history sufficient for trends; data per homogeneous risk group), accuracy and appropriateness; documented data process with update frequency and triggers; external-data justification; a documented **limitations register** with remediation plan, owner and pre-adjustment data retained | Per data set per valuation cycle |
| **Experience monitoring** [R1 TP 13.1] | A regular comparison of best estimate and its assumptions against experience, and a trigger to change methods/assumptions on **systematic deviation** | At least per reporting cycle; the trigger must be defined, not ad hoc |
| **Surplus funds** [R45][R46] | For each with-profits fund: with-profits policy liabilities on the **retrospective** basis (ten roll-up items) or, where justified, the **prospective** basis (six PV items); the value of future shareholder transfers; and the surplus-funds amount excluded from technical provisions **only if Tier 1 eligible** | Per with-profits fund per valuation date; consistent with the TP methodology (Surplus Funds 4.1); **no risk margin inside** (SS13/15 ¶2.4) |
| **Proportionality evidence** [R41 TPFR 27] | For each simplification: the nature/scale/complexity assessment, the error evaluation, and the 27.4(1) or 27.4(2) justification | Per method per valuation cycle |

---

## Product applicability

`x` = the rule directly binds; `(x)` = qualified or conditional; `—` = expressly does not apply;
`?` = the retrieved sources do not settle it; blank = not indicated.

Product key: TA = term-assurance, CI = critical-illness, IP = income-protection, WOL = whole-of-life,
WP = with-profits, ULB = unit-linked-bond, PA = pension-annuity.

| Rule [R#] | TA | CI | IP | WOL | WP | ULB | PA |
|---|---|---|---|---|---|---|---|
| Val 2.1/2.2 Article-75 balance sheet [R39] | x | x | x | x | x | x | x |
| Val 5.4 UK-GAAP derogation [R39][R40] | (x) | (x) | (x) | (x) | (x) | (x) | (x) |
| Val 6 valuation hierarchy [R39] | x | x | x | x | x | **x** | x |
| Val 8.1 goodwill / intangibles at zero [R39] | x | x | x | x | x | x | x |
| Val 10.2 contingent liabilities at the **basic** curve [R39] | (x) | (x) | (x) | (x) | (x) | (x) | (x) |
| TP 2.4 TP = BE + RM [R1] | x | x | x | x | x | x | x |
| TP 2.5(2) / TPFR 22 TP as a whole [R1][R41] | — | — | — | — | — | (x) | — |
| TP 3.1 best estimate definition [R1] | x | x | x | x | x | x | x |
| TP 9.1(3) future discretionary bonuses in TP [R1] | | | | (x) | **x** | | (x) |
| TP 9.2 / TPFR 17 options and guarantees [R1][R41] | (x) | (x) | (x) | x | **x** | **x** | (x) |
| TPFR 3.3(3) **contract-level** repricing test (long-term underwriting carve-out) [R41] | **x** | **x** | **x** | (x) | (x) | | — |
| TPFR 3.5 no-insurance-risk / no-guarantee boundary cut [R41] | — | — | — | — | (x) | **(x)** | — |
| TPFR 3.6 unbundling of a contract [R41] | | | (x) | (x) | (x) | (x) | (x) |
| TPFR 8 future management actions [R41] | (x) | (x) | (x) | (x) | **x** | **x** | (x) |
| TPFR 9.1 FDB off currently-held assets [R41] | | | | (x) | **x** | | |
| TPFR 10.1 FDB determined separately [R41] | | | | (x) | **x** | | |
| TPFR 11.1 dynamic policyholder behaviour [R41] | (x) | (x) | (x) | x | **x** | **x** | — |
| TPFR 13.1(5) intermediary payments [R41] | x | x | x | x | x | x | (x) |
| TPFR 13.1(6) payments to/from investment firms [R41] | | | | (x) | | **x** | |
| TPFR 13.1(8) policyholder-charged taxation [R41] | (x) | (x) | (x) | (x) | **x** | **x** | (x) |
| TPFR 16.4 expenses on a going-concern (new business) basis [R41] | x | x | x | x | x | x | x |
| TPFR 18.1 separate calculation per currency [R41] | (x) | (x) | (x) | (x) | (x) | (x) | (x) |
| TPFR 19.4–19.5 scenario-dependent method (stochastic) [R41] | — | — | (x) | (x) | **x** | **x** | (x) |
| TPFR 20.1 per-policy or compliant grouping [R41] | x | x | x | x | x | x | x |
| TPFR 21 premium provision / claims outstanding split [R41] | — | (x) | **(x)** | — | — | — | — |
| TPFR 24.4 **LGD floor 50%** on the CDA [R41] | (x) | (x) | (x) | (x) | (x) | | **x** |
| TPFR 26.3 technical-basis test for health obligations [R41] | | **x** | **x** | | | | |
| Annex 1 LoB 29 health (long-term basis) [R41] | | (x) | (x) | | | | |
| Annex 1 LoB 30 insurance with profit participation [R41] | | | | (x) | **x** | | (x) |
| Annex 1 LoB 31 index-linked and unit-linked [R41] | | | | (x) | | **x** | |
| Annex 1 LoB 32 other long-term [R41] | **x** | (x) | (x) | **x** | | | **x** |
| Annex 1 LoB 1 / 2 (GI-basis medical expense / income protection) [R41] | | (x) | **(x)** | | | | |
| TP 4A/4B risk margin, λ = 0.9, floor 0.25 [R1][R4][R44] | x | x | x | x | x | x | **x** |
| TP 4B.1(2) composite splits into two reference undertakings [R1] | (x) | (x) | (x) | (x) | (x) | (x) | (x) |
| TP 4B.1(13) no MA/VA/transitional/TMTP in the reference undertaking [R1] | (x) | (x) | (x) | (x) | (x) | (x) | **x** |
| TP 11 / TPFR 23–24 reinsurance recoverables [R1][R41] | **x** | **x** | **x** | x | (x) | (x) | **x** |
| SS5/24 funded reinsurance interface [R47] | | | | (x) | (x) | | **x** |
| SS18/16 longevity risk transfers [R48] | | | | (x) | (x) | | **x** |
| Surplus Funds Part / TP 9.1(3) carve-out [R45][R46] | — | — | — | (x) | **x** | — | (x) |
| TPFR 27 proportionality [R41] | x | x | x | x | x | x | x |
| **Negative best estimate permitted (no floor)** [§17] | **x** | **x** | **x** | (x) | (x) | (x) | — |

**Notes on the matrix**

- **TP-as-a-whole is `—` for six of seven products.** TPFR 22.2 declares option-dependent cash flows,
  mortality/disability/sickness/morbidity-dependent cash flows and **all** servicing expenses
  non-replicable. Every product here has expenses; every one has either biometric dependence or an
  exercisable option. ULB carries `(x)` only because the **unit-fund component** can in principle be
  replicated by the units held, while the charges, expenses, mortality element and any guarantee
  cannot.
- **TPFR 3.3(3) is bold for TA, CI and IP** because of the long-term-insurance-business carve-out:
  where an individual risk assessment is made at inception and cannot be repeated before repricing,
  the "premiums fully reflect the risks" test is applied **at contract level**, not portfolio level.
  For reviewable-rate CI and IP this is the difference between a boundary that stops at the next
  review date and one that runs to the end of the term. WOL and WP carry `(x)` because guaranteed
  premium rates make the question largely moot; PA is `—` because a single-premium annuity in payment
  has no future premium to cut.
- **TPFR 3.5 is bold-`(x)` for ULB** because a unit-linked bond is precisely the contract that can
  fail limbs (1) and (2) — no compensation for a specified uncertain adverse event, no financial
  guarantee of benefits — and thereby lose future premiums from the boundary. Whether the
  representative product fails those limbs turns on the size of the death-benefit uplift and the
  presence of any guarantee, and on the "no discernible effect on the economics of the contract"
  qualifier. **The retrieved sources do not settle it for any particular design.** WP carries `(x)`
  because a with-profits contract has a financial guarantee and so fails limb (2).
- **TPFR 19.4–19.5 is `—` for TA and CI** because a level-premium term or standalone CI contract with
  no surrender value and no financial option has essentially no scenario-dependent asymmetry; a
  deterministic projection satisfies the rule. IP carries `(x)` because escalation linked to an index
  and claim-inception dependence on economic conditions can introduce asymmetry.
- **TPFR 21 is `(x)` for IP and CI** only in the case where the business is written on a
  general-insurance technical basis (TPFR 26.3), which pulls it into LoB 2 or LoB 1 and imposes the
  premium-provision / claims-outstanding split. On a long-term technical basis it is LoB 29 and the
  split does not apply. **The technical basis, not the product name, decides** — and the retrieved
  rules give no bright-line test for "similar technical basis", so both rows carry parentheses.
- **TPFR 24.4 is bold for PA** because bulk annuity and funded-reinsurance structures put the largest
  recoverables, and therefore the largest 50%-floored counterparty-default adjustment, on annuity
  books.
- **TP 4B.1(13) is bold for PA** because the reference undertaking may not use the matching
  adjustment. For an MA-heavy annuity book the risk margin is therefore computed on a materially
  higher-liability basis than the balance sheet it sits on. The mechanics of the MA itself are
  stream B's.
- **The negative-best-estimate row** is `x` for TA, CI and IP (new profitable protection business
  routinely produces one), `(x)` for WOL, WP and ULB (charge-funded or guarantee-bearing designs may
  or may not), and `—` for PA (a single-premium annuity in payment has no future premium inside the
  boundary, so the best estimate is necessarily positive).
- **Val 5.4 / SS38/15** carries `(x)` across the board because the derogation is entity-level and
  conditional, and in any event SS38/15 confirms that **FRS 103 is never a permitted substitute** for
  the technical-provisions Parts.

---

## Gaps and caveats

### Conflicts between retrieved sources — recorded, not resolved

1. **SS5/24 ¶1.7 cites dead rules.** It directs firms to "Chapters 6, 7 and 11 of the Technical
   Provisions" [R47]. TP Chapters 6 and 7 are **[Deleted] as at 30/06/2024** [R1]; the MA material
   moved to the Matching Adjustment Part [R2] under PS10/24 [R5]. The October 2025 version of the SS
   was not updated for this. Only the Chapter 11 reference is live.
2. **"Market value" has two anchors.** The Glossary defines *market value* as "the market value as
   determined in accordance with **generally accepted accounting practice**" [R43], while Val 2.1
   states the Article-75 exchange/transfer standard and Val 12.1 forbids cost and amortised cost
   [R39]. TPFR 22.3–22.4 use *market value* for the TP-as-a-whole valuation [R41]. Whether a
   TP-as-a-whole amount is a GAAP market value or an Article-75 value is not resolved in the
   retrieved text.
3. **A date typo in the legislation.** The textual-amendment notes on SI 2023/1347 as displayed on
   legislation.gov.uk record insertions by SI 2024/1083 as taking effect "1.11.2024 for specified
   purposes and **31.12.20204** otherwise" [R44]. Recorded as printed. The intended date is
   evidently 31.12.2024 (consistent with PRA2024/13 commencement [R42]), but SI 2024/1083 itself was
   not read, so the correction is not verified.
4. **TPFR 16.4 versus TP 4B.1(5).** The best estimate must assume the firm **writes future new
   business** for the purposes of expense projection [R41 TPFR 16.4], while the risk-margin reference
   undertaking "**does not assume any new insurance or reinsurance obligations**" [R1 TP 4B.1(5)].
   Both are correct as printed; a model must carry **two** expense bases. No retrieved source
   explains how the reference undertaking's expenses should be set given that tension.

### Not retrieved, or retrieved only in part

- **SS9/14 "Valuation risk for insurers"** — listed in the Valuation Part's related links [R39] but
  **not fetched**. It is the PRA's expectations document on valuation uncertainty and would be the
  natural companion to Val 6.5–6.7. Flagged for a later pass.
- **SS5/14** (calculation of technical provisions and the use of internal models **for general
  insurers**) — listed in the TP Part's related links [R1]; not fetched, and out of scope for a life
  library.
- **SS3/17 "Illiquid unrated assets"**, **SS4/17 "Cyber insurance underwriting risk"**, **SS8/18**
  (internal-model MA modelling), **SS22/15** (EIOPA Set 1 Guidelines), **SS20/16** — all referenced
  by retrieved documents; none fetched.
- **SS18/16** [R48] was read only at grep level. Everything about it beyond the single quoted
  observation is **[unverified]**.
- **SS1/14 "Mutuality and with-profits funds"** and **SS14/15 "With-profits"** are on disk
  (`s5-ss114.txt`, `s5-ss1415.txt`) but were **not read for this stream** — they belong to the
  with-profits product stream.
- **SI 2024/1083** (the instrument that inserted IRPR regs 7A–7C) — URL verified HTTP 200, **not
  read**. All statements about it derive from the amendment notes inside [R44].
- **The Own Funds Part** was read only for the single sentence "the reconciliation reserve may be
  positive or negative" and to confirm the absence of EPIFP. The Part belongs to the capital stream.
- **The Conditions Governing Business Part** was not re-read here; CGB 2.2, 3.1 and 8.1 are cited
  from the cross-references in TPFR 8.5, SS5/24 ¶1.7 and TPFR 23.2 respectively, and from [R92].
- **Article bodies of DR (EU) 2015/35** were not read — only the table of contents and Article 1
  [R49]. The article titles are therefore verified; their content is not.
- **The per-letter Glossary export URLs** were not preserved by the earlier session; only the base
  glossary URL is verifiable [R43].
- **The "as at 31/12/2024" and "as at 30/06/2024" historical views** of the Technical Provisions and
  Valuation Parts were not separately retrieved. Rule *date-stamps* in the present view were read and
  are reported; the superseded *text* behind a "Past version of X before DATE" link was not.

### Numbers deliberately not transcribed

- **No risk-free rates, no fundamental spreads, no matching adjustments, no volatility adjustments.**
  Those are published technical information under IRPR reg 3 and belong to stream B. This file states
  only which curve applies where (basic vs relevant).
- **No SCR stresses, correlations or shocks.** The reference undertaking notional SCR is defined by
  its risk coverage (TP 4B.1(9)) and nothing more is transcribed here. The one SCR-adjacent number
  recorded — the SCR-SF 3B6.6(1) mass-lapse correction — is recorded only as *the existence of a
  correction*, with no rate.
- **No expense-inflation rate, no lapse rate, no mortality basis.** The rules impose requirements on
  assumptions, not values.
- **No default probabilities or spreads for the counterparty-default adjustment.** Only the **50%
  LGD floor** in TPFR 24.4 is a rule-set number and it is transcribed.
- **The "t = 14" point at which the λ floor binds** (§16 note (b)) is arithmetic performed by the
  drafter from λ = 0.9 and λ_floor = 0.25. It appears in **no** retrieved source and must be labelled
  as derived, never cited to [R1], [R4] or [R44].
- **The LoB mapping of the seven library products** (§12) is the drafter's inference from TPFR 26.2,
  26.3 and the Annex 1 definitions. Annex 1 does not name products. Treat the mapping as a working
  assumption to be confirmed per product design.

### Questions the retrieved sources do not settle

1. **What counts as a "similar technical basis to that of long-term insurance business"** for TPFR
   26.3, and therefore whether a given UK IP or CI contract is LoB 29 or LoB 1/2. No test, no
   indicia, no examples in any retrieved rule or SS.
2. **How the reference undertaking's expenses are set** given TPFR 16.4 (assume new business) versus
   TP 4B.1(5) (reference undertaking writes none).
3. **How SCR(t) should be projected in practice.** TP 4A.2 mandates internal-model use where a firm
   has one "unless it is inappropriate to do so"; no rule text sanctions any driver-based proxy, and
   the DR simplification hierarchy was not restated. What a standard-formula firm may do is
   governed only by TPFR 27.4.
4. **How the risk margin is allocated to lines of business.** TP 4A.3 states the objective
   ("adequately reflect the contributions of the lines of business to the reference undertaking
   notional SCR over the lifetime") and prescribes no method.
5. **Whether a with-profits fund's estate distributions belong in the technical provisions.** SS13/15
   ¶3.6 excludes them from the **surplus-funds** prospective calculation [R46]; it does not say what
   happens to them in the TP 9.1(3) best estimate.
6. **The interaction of TPFR 20.1(2)(c) with stochastic valuation.** Grouping must give
   "approximately the same results … in particular in relation to financial guarantees and
   contractual options". No tolerance, no test statistic, no benchmark is given.
7. **Whether "no discernible effect on the economics of the contract"** (TPFR 3.3 final paragraph and
   TPFR 3.5 final paragraph) has any quantitative threshold. It does not, in any retrieved source.
8. **What a "reliable basis" is for rebutting the 50% LGD floor** in TPFR 24.4.
9. **Whether the Article-75 transfer value in TP 2.2 is intended to differ from an IFRS 17
   fulfilment value**, and if so how. The retrieved UK sources assert the transfer standard and stop;
   SS38/15 [R40] only says FRS 103 does not substitute for the TP Parts.
10. **Whether any PRA rule has yet been made under the IRPR reg 7C simplified-risk-margin power.**
    None was found in the Technical Provisions or TPFR Parts as at 05/08/2026, but the whole Rulebook
    was not searched.

### Fetch behaviour observed on 2026-08-06

- **prarulebook.co.uk** serves HTTP 403 to plain fetchers and HTTP 200 with a browser User-Agent.
  URL slugs use `/pra-rules/<slug>/<DD-MM-YYYY>`. **The slug for the TPFR Part is
  `technical-provisions-further-requirements` (single hyphens)**; the `---` form used by
  `insurance---senior-management-functions` and
  `solvency-capital-requirement---standard-formula` returns **HTTP 404** for this Part. The Glossary
  lives at `/glossary`, **not** `/pra-rules/glossary` (404).
- Re-verified live on 2026-08-06: valuation/05-08-2026 → 200 (130,238 B);
  technical-provisions/05-08-2026 → 200 (189,410 B);
  technical-provisions-further-requirements/05-08-2026 → 200 (259,991 B);
  surplus-funds/05-08-2026 → 200 (82,668 B); with-profits/05-08-2026 → 200 (62,684 B);
  /glossary → 200 (76,049 B).
- **bankofengland.co.uk** likewise 403s plain fetchers. PDFs re-verified 2026-08-06:
  ps1524app6.pdf → 200 (1,780,845 B); ss3815-november-2024-update.pdf → 200 (991,592 B);
  ss524-october-2025.pdf → 200 (370,064 B). The SS13/15 and SS18/16 PDF filenames both end
  `-update.pdf`; the non-`-update` forms return 404.
- **legislation.gov.uk** serves plain fetchers. Formulae are rendered as **images** and are lost in
  text extraction — this affected both SI 2023/1346 [R4] and IRPR reg 7B [R44]. The PRA Rulebook
  renders the same formula as LaTeX in page text, which is why §16 transcribes TP 4A.1 rather than
  the statutory original.
- Re-verified 2026-08-06: uksi/2023/1347/contents → 200; eur/2015/35/contents → 200;
  eur/2015/35/article/1 → 200; uksi/2024/1083/contents → 200.
- **No URL on this page is fabricated.** Every URL cited was either the URL an on-disk retrieval came
  from or was re-issued and its status code recorded above.

