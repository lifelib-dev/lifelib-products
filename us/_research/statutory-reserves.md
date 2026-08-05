# Statutory Reserves and Asset Adequacy Analysis — research notes (U.S. statutory accounting and capital)

**Stream:** Statutory Reserves and Asset Adequacy Analysis
**Research date / access date for every citation below:** 2026-08-04
**Status:** research notes, not yet merged into the frozen reference library.

---

## Scope and numbering note

This file adds entries **R100–R124 only**. That block is assigned to this stream; parallel
streams own the other blocks. Entries **R1–R72** live in
`us/references/regulatory-and-actuarial-references.md` and are **frozen** — they are already
cited by product documentation as `[REG-R#]`. Nothing in R1–R72 is renumbered, restated, or
duplicated here. Where an existing entry already carries the source document, this file
**reuses its number** and records only the newly extracted mechanics under that number (see
"Existing entries that bear on this stream").

Entries actually created here: **R100–R113**. R114–R124 are left unused, which the block
convention permits.

**Retrieval method.** Most NAIC and Academy PDFs return raw compressed streams to the fetch
tool. Every PDF below was downloaded with `curl` to a scratch directory outside the repository
and its text extracted locally with `pypdf` before reading; those entries are marked
**fetched: yes (local text extraction)** and their annotations are first-hand. Web pages were
read directly. Failures are disclosed per entry.

**What is sold rather than published.** The **NAIC Accounting Practices and Procedures Manual
(AP&P Manual)** is a paid publication [R33]; it is the authoritative home of every actuarial
guideline, including AG 53 and AG 55, and of the Appendix A model-law excerpts that VM-A
indexes [R110]. The **NAIC Annual Statement Blank (Life/Fraternal)** — which carries the
statement of actuarial opinion page, Exhibits 5/6/7/8, Schedule S and the VM-20 Reserves
Supplement — is also a paid publication and was **not** retrieved. Where this file describes
those artifacts it does so through documents that reference them (VM-30, VM-31, AG 53, AG 55),
and says so.

---

## Existing entries (R1–R72) that bear on this stream

| R# | Short title | How it bears on statutory reserves / AAT — and what this stream re-read |
|----|-------------|------------------------------------------------------------------------|
| R1 | Standard Valuation Law (Model #820) | The statute the whole hierarchy hangs from. Re-fetched `model-law-820.pdf` for this stream and read **§3** (annual actuarial opinion, pre- and post-VM operative date; memorandum; confidentiality), **§4b** (calendar-year statutory valuation interest rate — the dynamic formula, weighting factors, plan types, reference rate), **§5** (CRVM), **§5a** (CARVM), **§6** (minimum aggregate reserves, including §6.B: reserves may not be less than what the appointed actuary needs to render the §3 opinion), **§7** (optional higher standards), **§11** (Valuation Manual, what it must specify), **§12** (requirements of a principle-based valuation). Facts extracted below are tagged `[R1]`. |
| R3 | Valuation Manual, Jan. 1, 2026 Edition | The rulebook. This stream read, in full or in the parts cited: **VM-01** definitions (NPR, DR, SR, modeled reserve, model segment, prudent estimate assumption, SET, VM-20 reserving category, asset adequacy analysis, qualified actuary), **VM-20 §§1, 2, 3.B/3.C/3.D/3.E, 4, 5, 6, 7.A/7.B**. Facts from VM-20 and VM-01 are tagged `[R3]`. VM-30, VM-31, VM-G and VM-A are pages of the same PDF but get their own entries (R100, R108, R109, R110) because a reserving model cites them as separate deliverables, exactly as R35/R36/R37 do for VM-21/VM-22/VM-V. |
| R6 | Model #830 ("Regulation XXX") | Deficiency / excess-of-net-premium reserves and segmented basic reserves for term and ULSG; still the operative formulaic standard for pre-PBR in-force. Referenced, **not duplicated**. Its content reaches current valuations through **VM-A item A-830** [R110] and through AG 38 in AP&P Appendix C [R33]. |
| R7 | AG 38 | Sections 8C (stand-alone asset adequacy analysis of the formulaic reserve) and 8D (principle-based reserve) are the two ULSG in-force blocks whose interaction with VM-30 asset adequacy testing the Academy practice note works through [R111]. |
| R16 / R72 | IRC §807 / IRS LB&I directive | Tax reserve = greater of net surrender value and 92.81% of the NAIC-method reserve, capped at statutory. The statutory engine is the tax engine with a haircut and cap; the AAT model, by contrast, projects federal income tax explicitly, which VM-20/VM-21 do not [R111]. Referenced, **not duplicated**. |
| R23 | AAA VM-20 practice note (April 2020) | The implementation companion for the NPR/DR/SR and the exclusion tests. Referenced; this stream's new practice-note entry (R111) is the **asset adequacy** companion, a different document. |
| R25 | AAA PBR Assumptions Resource Manual | Assumption governance that VM-31 §3.D.1.d documentation effectively demands. |
| R27 | ASOP 7 (life/health cash flow analysis) | The general cash-flow-analysis standard; §3.10.1 (range and number of scenarios) is what ASOP 22 and the practice note defer to for scenario selection [R111]. Revision effective June 1, 2026. |
| R29 | ASOP 22 (asset adequacy opinions) | **Re-read in full for this stream** from the Doc. No. 203 PDF, `https://www.actuarialstandardsboard.org/wp-content/uploads/2021/11/asop022_203.pdf` (fetched 2026-08-04, 26 pp.). All ASOP 22 facts below are tagged `[R29]`. No new number is taken. |
| R31 | ASOP 52 (PBR for life products) | Governs the VM-20 calculation itself; yields to the Valuation Manual on conflict. |
| R32 | ASOP 56 (modeling) | The governing standard for the model that produces every number in this file; cited by AG 53 §4.B.ii guidance note [R105]. |
| R33 | NAIC AP&P Manual | Appendix A (model-law excerpts, indexed by VM-A) and **Appendix C (actuarial guidelines — where AG 51, AG 53, AG 55 officially live)**. Paid publication; not fetched. |
| R34 | FASB ASU 2018-12 (LDTI) | Why the same projected cash flows feed a second measurement wrapper. |
| R35 | VM-21 (variable annuity PBR) | The annuity analogue of the VM-20 three-component structure; VM-31 carries the Annuity Summary and Annuity Report for it, and VM-G applies to it. Referenced, **not duplicated**. |
| R36 | VM-22 (non-variable annuity PBR) | Its **Section 7** exclusion tests and **Single Scenario Test** are the annuity counterparts of VM-20 §6, and VM-G §1.A and VM-31 §2.A both name VM-22 alongside VM-20 [R109][R108]. Referenced, **not duplicated**. |
| R37 | VM-V §1 (income annuity valuation rates) | The formulaic maximum valuation interest rate for income annuities, and the point where the **formulaic** track survives inside a PBR-era manual. Re-read for this stream; additional mechanics recorded below under `[R37]`. |
| R38–R41 | AG 43 / AG 33 / AG 35 / VM-C | AG 43 is the scoping shell pulling pre-2017 VA onto VM-21; AG 33/AG 35 are formulaic CARVM for deferred and indexed annuities (texts not public); **VM-C is the index of guidelines the Valuation Manual incorporates** — re-read for this stream, and the **life/CRVM** half of that index is extracted below under `[R41]` (R41's existing annotation catalogues only the annuity/CARVM family). |
| R44 | AG 54 (ILVA nonforfeiture) | Interim-value mechanics; not a valuation guideline, and absent from VM-C [R41]. |
| R47 | C-3 RBC instructions (C-3 Phase II) | The capital analogue: **"modelling statutory reserve as equal to the working reserve"** is the standard device for projecting a reserve forward inside a scenario; RBC = TAR − statutory reserves. Referenced, **not duplicated**; the projected-reserve problem is discussed below. |
| R48 | Oliver Wyman QIS II | The reform that produced the 2020 VM-21 and revised C-3 Phase II. |
| R70 / R71 | ASOP 54 / ASOP 10 | Pricing and GAAP counterparts to the same projection engine. |

---

## New entries (R100–R113)

### Group 1 — The actuarial opinion and asset adequacy analysis

### R100. VM-30: Actuarial Opinion and Memorandum Requirements (Valuation Manual, Jan. 1, 2026 Edition)
- **Publisher:** NAIC
- **URL:** https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf (pages 30-1 to 30-15 of the 457-page PDF; same document as R3)
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; **Sections 1, 2 and 3 read in full**, including the prescribed opinion wording and the Regulatory Asset Adequacy Issues Summary contents; copyright line "© 2025 National Association of Insurance Commissioners")
- **Annotation:** The operative U.S. requirement for the annual **statement of actuarial opinion** and the supporting **actuarial memorandum**, issued under Section 3 of Model #820 and collectively called the **AOM requirements** [R100]. It is short — three sections, fifteen pages — but it is the document that turns a liability cash flow model into a regulatory deliverable, because it (a) requires the opinion to apply to **all in-force business on the annual statement date, whether directly issued or assumed, regardless of when or where issued**; (b) requires that any shortfall found by asset adequacy analysis be **established as an additional reserve**, releasable in later years with disclosure; (c) prescribes the **exact wording** of the identification, scope, reliance and opinion sections plus a **table of key indicators** that must be ticked whenever the wording is changed; (d) prescribes the **asset-adequacy-tested amounts table**, whose columns split every annual statement line into *Formula Reserves*, *Principle-Based Reserves*, *Additional Reserves*, *Other Amount* and *Total*, with a per-line **Analysis Method** symbol; and (e) prescribes the memorandum and RAAIS contents [R100]. **Verified negative finding: VM-30 contains no exemption clause and no prescribed interest scenarios** — the word "exempt" does not appear in it at all, and the New York seven appear in the Valuation Manual only as an *example* inside a VM-20 §6 guidance note [R100][R3]. It expressly makes **AG 48** (XXX/AXXX reserve financing) and **AG 51** (long-term care AAT) applicable for VM-30 purposes [R100].

### R101. Actuarial Opinion and Memorandum Regulation (Model #822)
- **Publisher:** NAIC (print: "NAIC Model Laws, Regulations, Guidelines and Other Resources—April 2010"; © 2010)
- **URL:** https://content.naic.org/sites/default/files/model-law-822.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; 16-page PDF, Sections 1–7 read). A direct WebFetch of the same URL failed — the tool received raw PDF streams — which is why local extraction was used.
- **Annotation:** **Model #822 is confirmed to exist, to be numbered 822, and to be titled "Actuarial Opinion and Memorandum Regulation."** Its seven sections are Purpose / Authority / Scope / Definitions / General Requirements / **Statement of Actuarial Opinion Based On Asset Adequacy Analysis (§6)** / **Description of Actuarial Memorandum Including an Asset Adequacy Analysis and Regulatory Asset Adequacy Issues Summary (§7)** [R101]. **Current status:** it is the *pre-Valuation-Manual* instrument. For companies subject to the Valuation Manual its requirements have been carried into **VM-30**, and VM-30 itself acknowledges the continuity — a guidance note states that "appointment in accordance with the requirements of the Actuarial Opinion and Memorandum Regulation (#822) qualifies as being in accordance with the Valuation Manual," so an appointed actuary need not be re-appointed [R100]. The Academy states plainly that "the AOMR has since been superseded by the Valuation Manual VM-30" [R111]. The **latest NAIC print located is April 2010**; no post-2010 print was found, which is consistent with the model having been frozen once VM-30 took over. **Do not treat #822 as dead text**: it remains the vehicle through which many states adopted asset adequacy analysis, and the state adoptions (R102) are what a company actually complies with where the Valuation Manual is not operative.
- **Differences from VM-30 that matter to an implementer** [R100][R101]: RAAIS due **March 15** under #822 versus **April 1** under VM-30; #822 uses "recommended language" while VM-30 uses **prescribed wording plus a table of key indicators**; #822 has no formal taxonomy of opinion outcomes while VM-30 defines **adverse / qualified / inconclusive** and requires the category to be ticked; VM-30 adds the **IMR/AVR allocation rules**, the **equity-return-volatility requirement**, and a **seven-year documentation retention** rule that #822 does not contain; #822's memorandum-review mechanism (commissioner may designate a reviewing actuary) survives in VM-30 §3.B.3.

### R102. NAIC Model #822 State Page — Actuarial Opinion and Memorandum Regulation
- **Publisher:** NAIC Legal Division (print: "NAIC Model Laws, Regulations, Guidelines and Other Resources—Fall 2024"; © 2024; pages ST-822-1 to ST-822-7)
- **URL:** https://content.naic.org/sites/default/files/model-law-state-page-822.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; key and state chart read)
- **Annotation:** The state-by-state adoption chart for Model #822, and the cheapest public evidence that the model is still tracked. Two things an implementer needs from it. First, most listed state citations are annotated **"does not include 2009 amendment"** — i.e., many states' AOMR predates the PBR-enabling amendments, which is exactly why VM-30 rather than #822 governs where the Valuation Manual is operative [R102]. Second, and decisive for scenario design: **New York's entry for Model #822 is "N.Y. COMP. CODES R. & REGS. tit. 11, §§ 95.1 to 95.12 (Regulation 126)"** [R102] — so *New York Regulation 126 is New York's Actuarial Opinion and Memorandum Regulation*, and the "New York seven" interest scenarios are a **state** requirement layered on top of VM-30, not a Valuation Manual requirement (R112). The chart carries an explicit disclaimer that it "does not reflect a determination as to whether a state meets any applicable accreditation standards" [R102].

### R103. Actuarial Guideline LV — Application of the Valuation Manual for Testing the Adequacy of Reserves Related to Certain Life Reinsurance Treaties (AG 55)
- **Publisher:** NAIC (this print: "Adopted by Life Insurance and Annuities (A) Committee – July 14, 2025 / Adopted by Life Actuarial (A) Task Force – June 5, 2025"; © 2025; 14 pages)
- **URL:** https://content.naic.org/sites/default/files/committees-pending-action-aglv.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; **entire guideline read, Sections 1–9 and Appendix 1**). A guessed URL `.../inline-files/AG%2055.pdf` returned HTTP 404 and is not cited.
- **Annotation:** **This is the recent NAIC asset-adequacy-testing-for-reinsurance framework, and it has been adopted, not merely proposed.** It is **effective for asset adequacy analysis of the reserves reported in the December 31, 2025 annual statement and all subsequent annual statements**, with documentation **due April 1 following the applicable valuation date** — so the first filings are due **April 1, 2026** [R103]. A guidance note states the intent to fold its requirements into **VM-30** later, at which point the guideline ceases to apply [R103]. Its purpose is stated as requiring "that asset adequacy analysis use a cash flow testing methodology that evaluates ceded reinsurance as an integral component of asset-intensive business" [R103]. Mechanics are extracted below; the single most important structural fact for a model is that AG 55 requires a **mandatory cash-flow-testing run whose Starting Asset Amount equals the Post-reinsurance Reserve**, i.e. the ceding company must model the *reinsurer's* asset position [R103]. **Appendix 1 reproduces the New York 7 interest rate scenarios verbatim as an excerpt from §95.10(d) of New York Regulation 126** — this is the only place in the NAIC material read for this stream where the seven scenarios are printed in full [R103].
- **Adoption chain:** LATF **June 5, 2025** and Life Insurance and Annuities (A) Committee **July 14, 2025** are printed on the guideline itself [R103]. Adoption by the NAIC **Executive (EX) Committee and Plenary on August 13, 2025** at the Summer National Meeting is **[unverified]** — it is consistently reported by law firms and consultants but no NAIC document stating that date was retrieved; what *was* retrieved is the Reinsurance (E) Task Force record that A Committee and then EX Committee/Plenary adoption "was expected … at the Summer National Meeting" (R104).

### R104. NAIC Reinsurance (E) Task Force — 2025 Fall National Meeting materials (including the adopted minutes of the Aug. 11, 2025 Summer National Meeting session)
- **Publisher:** NAIC (draft dated 12/4/25; minutes draft dated 8/19/25)
- **URL:** https://content.naic.org/sites/default/files/national_meeting/Materials-RTF-12-9-2025_0.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; 7-page packet; agenda and the Aug. 11, 2025 minutes read)
- **Annotation:** The official NAIC record of AG 55's passage and of how regulators characterise it. It records that LATF "recently adopted" AG 55 and that it "was expected to be adopted by the Life Insurance and Annuities (A) Committee and then Executive (EX) Committee and Plenary at the Summer National Meeting" [R104]. Two statements matter for implementation. (1) **"[O]ne of the key aspects of AG 55 is an emphasis on disclosure rather than mandating additional reserves,"** with companies free to bolster reserves on their own evaluation and regulators retaining the right to request further analysis [R104] — consistent with AG 55 §5.B, which says the guideline "does not include prescriptive guidance as to whether additional reserves should or should not be held" [R103]. (2) The project's objectives were to give regulators tools to assess reserve adequacy when business is ceded, **avoid conflicts with reciprocal jurisdictions**, and avoid burdening companies where risk is minimal; late edits before adoption clarified "required documentation, asset exposure testing, eligibility for exemptions, and aggregation across product lines" [R104]. The packet also confirms AG 55 grew out of an offshore-reinsurance concern and that further work is expected [R104].

### R105. Actuarial Guideline LIII — Application of the Valuation Manual for Testing the Adequacy of Life Insurer Reserves (AG 53)
- **Publisher:** NAIC (print paginated "AG53-1" to "AG53-8" and headed "Appendix C", i.e. the AP&P Manual Appendix C text)
- **URL:** https://content.naic.org/sites/default/files/inline-files/AG%2053.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; **entire guideline read, Sections 1–6 and Appendix I**)
- **Annotation:** The uniform-practice overlay on asset adequacy analysis, aimed squarely at **complex and high-yielding assets** — structured securities, ABS, CLOs, and assets originated by the company or an affiliate [R105]. **Effective for the December 31, 2022 annual statement and all subsequent statements**, with the same "will be folded into VM-30 later" guidance note that AG 55 carries [R105]. Its scope is a **company-level size test**, not a product test: over **$5 billion** of general account actuarial reserves (Exhibits 5, 6, 7, 8) plus non-unitized separate account assets; **or** over **$100 million** of the same *and* over **5% of supporting assets** in Projected High Net Yield Assets — reserves counted **gross of ceded reinsurance**, whether directly written or assumed [R105]. It applies to assets supporting liabilities tested in AAT, excluding unitized separate account assets and policy/contract loans [R105]. Why a liability-model library must care: AG 53 is where the **asset side of the same projection** acquires prescribed definitions, prescribed sensitivity tests and a prescribed benchmark table, and it is the document AG 55 leans on for asset documentation (AG 55's "Similar Memorandum" must include "[r]elevant aspects of Actuarial Guideline 53 documentation and analysis") [R103][R105].

### R106. AG 53 Guidance Document — Year-End 2025
- **Publisher:** NAIC, for the Valuation Analysis (E) Working Group (VAWG)
- **URL:** https://content.naic.org/sites/default/files/inline-files/AG-53-guidance-YE-2025%20(1).pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; 5-page document read)
- **Annotation:** The annual information request sent to every company filing an AG 53 report, and the closest thing to an errata/FAQ for the guideline. It states it has "no substantive changes from what was provided for the prior year-end" [R106]. Four clarifications bear directly on model construction: (1) the **equity-like sensitivity test covers both initial assets and reinvestments**, because equity-like instruments tend to be held rather than to mature [R106]; (2) **a modelling simplification cannot be used to escape the test** — if you model reinvestment as public non-callable bonds but actually reinvest in complex assets, the assumed returns must be reduced to the public-non-callable level, otherwise the reinvestments stay in scope for sensitivity testing and attribution [R106]; (3) companies must report **projected portfolio allocations at projection years 5, 10, 20 and 30 under the NY1 level scenario**, plus any modelled investment allocation limits [R106]; (4) structured-asset reporting is by **position in the capital structure and rating**, with CLOs split between broadly syndicated and middle-market collateral, and separate treatment for Schedule BA assets, feeder funds, collateral loans and **payment-in-kind** assets [R106]. The reporting is done on **AG 53 reporting templates** published under the Documents tab of the LATF web page [R105][R106].

### R107. NAIC Valuation Analysis (E) Working Group — committee page and charges
- **Publisher:** NAIC
- **URL:** https://content.naic.org/committees/e/valuation-analysis-wg
- **Accessed:** 2026-08-04
- **Fetched:** yes (web page)
- **Annotation:** The regulator body that actually reads what the model produces. Its charges include working with NAIC resources to prioritise and respond to **principle-based reserve** issues, coordinating **"PBR reviews/examinations for VM-20, VM-21, and VM-22"** across states, and conducting **targeted reviews of AG 55, AG 53 and AG 51 filings** — the page states all three guideline titles in full, which independently corroborates AG 55's title and AG 53's title [R107]. It also provides "a confidential forum to address questions/issues regarding PBR and asset adequacy analysis" [R107]. AG 53 §6 and AG 55 §9 both name VAWG as the reviewer and say it will publish periodic reports identifying **outliers** [R103][R105].

### Group 2 — PBR documentation and governance

### R108. VM-31: PBR Actuarial Report Requirements for Business Subject to a Principle-Based Valuation (Valuation Manual, Jan. 1, 2026 Edition)
- **Publisher:** NAIC
- **URL:** https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf (pages 31-1 to 31-46; same document as R3)
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; Sections 1, 2, 3.A, 3.B, 3.C and 3.D.1–3.D.3 read; the full table of contents and section headers of 3.D–3.F reviewed)
- **Annotation:** The documentation deliverable — the reason a PBR model must be *evidenced*, not merely run. Its structure is **Executive Summary, Life Summary, Life Report, Annuity Summary, Annuity Report**, with the Life and Annuity Reports each carrying one or more **sub-reports** prepared by the qualified actuary assigned under VM-G [R108]. The governing standard is that "[t]he PBR Actuarial Report must include documentation and disclosure sufficient for another actuary qualified in the same practice area to evaluate the work" [R108]. Filing mechanics: the **Executive Summary, Life Summary and Annuity Summary go to the domiciliary commissioner no later than April 1**; the **entire report on request**, by April 1 or within 30 days if requested later; **searchable PDF**, narrative font ≥ 10 point, with large data arrays supplied as companion spreadsheets that count as part of the report; **seven-year retention** [R108]. A company that computes **no DR or SR** because it passed the exclusion tests **must still file a sub-report** covering the relevant requirements — so passing an exclusion test does not remove the model from the documentation regime [R108]. The report must **retain and follow the order of the requirements** and keep the headers, with an explanatory statement wherever a requirement is not applicable [R108]. Note the routing rule: if only VM-20 policies are included, §§3.E/3.F (annuity) are not applicable; if only VM-21/VM-22 contracts, §§3.C/3.D (life) are not applicable [R108]. Contents most load-bearing on a model are extracted below.

### R109. VM-G: Appendix G — Corporate Governance Guidance for Principle-Based Reserves (Valuation Manual, Jan. 1, 2026 Edition)
- **Publisher:** NAIC
- **URL:** https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf (pages G-1 to G-6; same document as R3)
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; **Sections 1–4 read in full**)
- **Annotation:** Four short sections that decide *who owns the model*. VM-G applies **only to a principle-based valuation calculated under VM-20, VM-21 and VM-22** [R109]. Its **scope carve-out is the practically important part**: a company that computes **no DR or SR** under VM-20 or VM-22 because it passed the exclusion tests, **and** whose entire VM-21 business is on the Alternative Methodology, is generally **exempt from Sections 2 and 3** (board and senior management guidance) but **remains subject to Section 4** (qualified actuary responsibilities) — *unless* it computed the SERT using the DR method of VM-20 §6.A.2.b.i.a, the adjusted-scenario-reserve method of VM-22 §7.C.2.a.i, or the Stochastic Exclusion Demonstration Test of VM-20 §6.A.3 or VM-22 §7.D, in which case Sections 2 and 3 apply again [R109]. In other words, **the way you pass the exclusion test determines your governance burden**. A guidance note adds that if a company aggregates AG 43 business with VM-21 business, VM-G applies to the combined valuation [R109]. **Governance documentation must be retained at least seven years** [R109]. Section 4 requires the qualified actuaries to **certify that non-prescribed, non-stochastically-modelled assumptions are prudent estimates with appropriate margins**, to verify prescribed assumptions are *used as required* (not that they are appropriate), to report to board and senior management, to **prepare the VM-31 report**, and to disclose unresolved PBR issues to external auditors and regulators [R109]. For an exclusion-test-only company, that board reporting shrinks to **notifying senior management if the company is at risk of failing an exclusion test and reporting on readiness to calculate the DR and/or SR** — a concrete requirement that a model must be *able* to compute components it is currently omitting [R109]. VM-G §4.B is explicit that the qualified actuary is **not** thereby opining on reserve adequacy; that is the appointed actuary's job under VM-30 [R109].

### R110. VM-A: Appendix A — Requirements (Valuation Manual, Jan. 1, 2026 Edition)
- **Publisher:** NAIC
- **URL:** https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf (pages A-1 to A-2; same document as R3)
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; the complete two-page index read)
- **Annotation:** The counterpart to VM-C (R41) and, like it, an **index rather than a text**: "Unless otherwise noted, this appendix references the following requirements from Appendix A of the AP&P Manual" [R110]. This is where the **formulaic** requirements the Valuation Manual still relies on are carried. Full index as printed: **A-200** separate accounts funding guaranteed minimum benefits under group contracts; **A-235** interest-indexed annuity contracts; **A-250** variable annuities; **A-255** modified guaranteed annuities; **A-270** variable life insurance; **A-585** universal life insurance; **A-588** modified guaranteed life insurance; **A-620** accelerated benefits; **A-641** long-term care; **A-695** synthetic GICs; **A-785** credit for reinsurance; **A-791** life and health reinsurance agreements; **A-812** smoker/nonsmoker mortality tables; **VM-A-814** recognition of the 2001 CSO (Model #814); **A-815** preferred mortality tables; **A-817** preneed life minimum standards; **A-820** minimum life and annuities reserve standards; **A-821** annuity mortality table (Model #821); **A-830** valuation of life insurance policies, including new select mortality factors [R110]. **Why this matters to a model:** VM-20 §3.B.6 sends the NPR for the entire *All Other* reserving category — and for IUL policies where no DR or SR is computed — to "applicable methods in **VM-A and VM-C** for the basic reserve" [R3]. So an implementer cannot build a VM-20 engine without also building a **CRVM formulaic engine driven by A-820 and A-830**, and the authoritative text for those sits in the **paid** AP&P Manual [R33][R110].

### Group 3 — Practice guidance and standards

### R111. Asset Adequacy Analysis — Public Policy Practice Note, for companies that file a Life, Accident and Health/Fraternal Statutory Annual Statement
- **Publisher:** American Academy of Actuaries, Asset Adequacy Analysis Practice Note Work Group and the Life Valuation Committee; **September 2017, updated September 2024** (the Academy's resource page dates the update posting December 24, 2024); 93 pages
- **URL (PDF):** https://actuary.org/wp-content/uploads/2025/03/Life-PracticeNote-2017AATUpdate.pdf — **URL (landing page):** https://actuary.org/resources/asset-adequacy-analysis-updated-for-2024/
- **Accessed:** 2026-08-04
- **Fetched:** yes, both (PDF by local text extraction; front matter, complete table of contents, and Q12, Q13, Q14, Q17, Q19, Q21, Q22, Q23, Q28, Q29, Q30, Q32, Q33, Q34, Q35, Q113, Q115, Q116, Q117, Q118 read)
- **Annotation:** The single most useful public description of what U.S. cash flow testing actually *is* as a modelling exercise — 118 questions organised as Introduction / Appointed-actuary procedures / General considerations / Modeling: General, Economic Scenarios, Assets, Policy Cash Flow Risk, Expenses / … / **Section L: Impact of AG 43, PBR, and Other Nonformulaic Valuation Standards** [R111]. Standard Academy disclaimer: not an ASB promulgation, not an ASOP, not binding, and events after publication may make it obsolete [R111]. **Read the caution about vintage:** many of its quantitative statements come from **appointed-actuary surveys conducted in 2004 and 2012**, and the note itself warns the reader "as to the applicability and appropriateness of the responses" [R111] — treat the percentages below as historical practice indicators, not current benchmarks. Its most valuable content for this library is Section L, which is the only public source located that works through **how a PBR reserve is treated inside VM-30 asset adequacy analysis** (see Extracted mechanics).

### R112. N.Y. Comp. Codes R. & Regs. tit. 11, § 95.10 — Additional considerations for analysis (New York Insurance Regulation 126)
- **Publisher:** State of New York (New York Codes, Rules and Regulations), via Legal Information Institute, Cornell Law School
- **URL:** https://www.law.cornell.edu/regulations/new-york/11-NYCRR-95.10 (Part 95 index: https://www.law.cornell.edu/regulations/new-york/title-11/chapter-IV/subchapter-B/part-95, titled "REGULATIONS GOVERNING AN ACTUARIAL OPINION AND MEMORANDUM")
- **Accessed:** 2026-08-04
- **Fetched:** yes (section read via LII)
- **Annotation:** The source of the **"New York 7."** Part 95 is New York's adoption of the Actuarial Opinion and Memorandum Regulation [R102], and **§95.10 is the section that adds requirements the NAIC model does not contain**. Its five subdivisions are **(a) Aggregation**, **(b) Selection of Assets for Analysis**, **(c) Use of Assets Supporting Reserves** (IMR/AVR allocation), **(d) Required Interest Scenarios**, and **(e) Withdrawal or Lapse Rates** [R112]. Three requirements bind a model directly: liability cash flows **must be projected separately for at least products with cash settlement options and products without cash settlement options** [R112]; **the annual statement value of the assets held in support of the specified reserves may not exceed the annual statement value of the specified reserves** [R112] — the New York statement of the same rule ASOP 22 §3.1 states nationally [R29]; and the **seven prescribed interest scenarios** of subdivision (d), reproduced verbatim at R103's Appendix 1. Note that Part 95 also contains **§95.7 "Statement of actuarial opinion not including an asset adequacy analysis"** and **§95.8 "…based on an asset adequacy analysis"** — the two-track structure that ASOP 57 (R113) and ASOP 22 (R29) respectively serve [R112].

### R113. ASOP No. 57 — Statements of Actuarial Opinion Not Based on an Asset Adequacy Analysis for Life Insurance, Annuity, or Health Insurance Reserves and Related Actuarial Items
- **Publisher:** Actuarial Standards Board (Doc. No. 208; **adopted January 2023, effective June 15, 2023**)
- **URL (standard page):** https://www.actuarialstandardsboard.org/asops/asop-no-57-statements-of-actuarial-opinion-not-based-on-an-asset-adequacy-analysis-for-life-insurance-annuity-or-health-insurance-reserves-and-related-actuarial-items/ — **URL (PDF):** https://www.actuarialstandardsboard.org/wp-content/uploads/2024/02/asop057_208.pdf (PDF not separately fetched)
- **Accessed:** 2026-08-04
- **Fetched:** yes (standard page)
- **Annotation:** **Not in R1–R72**, and the missing half of the opinion framework the library already covers through ASOP 22 (R29). ASOP 57 is the conversion of **Actuarial Compliance Guideline No. 4** — the last remaining ACG — into ASOP form, governing the opinion given by an actuary for a company that has **received an exemption from asset adequacy analysis**; the conversion was expressly "not intended to raise or lower the requirements" [R113]. ASOP 22's own history section corroborates the split: ASOP 22 was scoped to opinions under §8 of the 1991 model AOMR (asset adequacy) and ACG No. 4 to §7 (not) [R29]. Modelling relevance is narrow but real: an exempt company's opinion rests on the **formulaic** reserve alone, so no projection model is required — which is exactly the boundary a reference library should mark, since **VM-30 itself grants no exemption** [R100] and the exemption therefore lives in state law.

---

## Extracted mechanics

Every fact below is tagged with the entry whose document it was read from. Anything not so
tagged is marked `[unverified]`.

### 1. The reserve hierarchy a model must be able to produce

**Statutory floor stack, from the statute down** [R1]:

1. **§4 / §4a / §4b — minimum standard**: mortality table, interest rate and method, by calendar year of issue [R1].
2. **§5 — CRVM** for life insurance and endowment benefits; **§5a — CARVM** for annuity and pure endowment benefits [R1].
3. **§6.A — aggregate reserves may not be less than** the aggregate reserves computed on the **mortality table(s) and interest rate(s) used in calculating nonforfeiture benefits** [R1]. (This is the classic "nonforfeiture-basis aggregate floor.")
4. **§6.B — aggregate reserves for all policies, contracts and benefits may not be less than the aggregate reserves determined by the appointed actuary to be necessary to render the §3 opinion** [R1]. **This single sentence is what makes asset adequacy analysis part of minimum statutory reserves rather than a disclosure exercise**, and it is the statutory authority behind VM-30 §2.C.2's requirement to establish an additional reserve [R100].
5. **§7 — optional higher standards**, with a company permitted to adopt and later lower back to the minimum with commissioner approval [R1].
6. **§11 — for issues on or after the Valuation Manual operative date, the Valuation Manual standard is the minimum standard** [R1].

**What the Valuation Manual must contain**, per §11.D [R1]: CRVM for life contracts, CARVM for annuity contracts, minimum reserves for everything else; which contracts are subject to a **principle-based valuation** under §12.A; for PBR contracts, the **report format** (→ VM-31), **prescribed assumptions for risks the company does not control or influence**, and **corporate governance procedures** (→ VM-G); and for non-PBR contracts a standard that is either consistent with the pre-operative-date standard **or** develops reserves "at a level of conservatism that reflects conditions that include unfavorable events that have a reasonable probability of occurring" [R1].

**§12.A conditions of a principle-based valuation** [R1]: quantify benefits, guarantees and funding at a level of conservatism reflecting unfavourable events with a reasonable probability of occurring over the contract lifetime, and for **significant tail risk**, conditions appropriately adverse to quantify that tail risk; use assumptions, risk analysis methods and models **consistent with, but not necessarily identical to,** the company's own risk assessment process; and use assumptions that are either prescribed in the Valuation Manual or established from the company's own relevant, statistically credible experience.

### 2. Formulaic reserve mechanics

**CRVM — §5.A** [R1]. Reserve = excess, if any, of the present value at the valuation date of future guaranteed benefits over the present value of future **modified net premiums**. Modified net premiums are the **uniform percentage of the respective contract premiums** such that their present value at issue equals the present value of benefits **plus the excess of (1) over (2)**, where

- **(1)** = a net level annual premium equal to (PV at issue of benefits provided **after the first policy year**) ÷ (PV at issue of an annuity-due of 1 payable on the first and each subsequent premium-paying anniversary), **capped at the net level annual premium on the nineteen-year premium whole life plan for the same amount at an age one year higher than the issue age**; and
- **(2)** = a **net one-year term premium** for the benefits provided in the first policy year [R1].

That cap is the whole of the "CRVM expense allowance" and is the one piece implementers most often get wrong: the limit is the **19-pay whole life** net level premium at **age x+1**, not at age x [R1].

**CRVM — §5.B, the excess-first-year-premium rule** [R1]. For policies issued on or after the date the state inserted for the 1980 amendments, where the **first-year contract premium exceeds the second-year premium** with no comparable additional first-year benefit, and the policy provides an endowment or cash surrender value greater than that excess, the reserve at any anniversary on or before the **assumed ending date** (the first anniversary at which endowment plus available cash surrender value exceeds the excess premium) is the **greater** of (i) the §5.A reserve and (ii) the §5.A reserve recomputed with the §5.A(1) value **reduced by 15% of the excess first-year premium**, all present values determined ignoring premiums and benefits after the assumed ending date, the policy assumed to mature as an endowment on that date, and the cash surrender value then available treated as the endowment benefit [R1]. The comparison uses the mortality and interest bases of §§4 and 4b [R1].

**CRVM — §5.C** extends the same principles to varying amounts of insurance or varying premiums, to qualifying group annuity/pure endowment contracts, to disability and accidental death benefits in all policies and contracts, and to all other benefits [R1].

**CARVM — §5a.B** [R1], the definitive statement of the greatest-present-value construction:

> reserves are "the greatest of the respective excesses of the present values, at the date of valuation, of the future guaranteed benefits, **including guaranteed nonforfeiture benefits**, provided for by the contracts **at the end of each respective contract year**, over the present value, at the date of valuation, of any future **valuation considerations** derived from future gross considerations, required by the terms of the contract, that become payable **prior to the end of the respective contract year**" [R1].

Future guaranteed benefits use **the mortality table (if any) and interest rate(s) specified in the contract for determining guaranteed benefits**; **valuation considerations are the portions of the respective gross considerations applied under the contract to determine nonforfeiture values** [R1]. §5a.A excludes qualifying employer/employee-organization group annuity and deferred compensation contracts other than IRC §408 arrangements [R1]. AG 33 (R39) and AG 35 (R40) are the interpretive layers on this calculation and their texts are **not public** [R41][R33].

**Deficiency / excess-of-net-premium reserves.** The Valuation Manual's VM-C index carries **Actuarial Guideline I — "Interpretation of the Standard Valuation Law With Respect to the Valuation of Policies Whose Valuation Net Premiums Exceed the Actual Gross Premium Collected"** [R41]; the substantive current standard for term and ULSG deficiency reserves is **Model #830** (R6), reached through **VM-A item A-830** [R110]. Neither the AG I text nor A-830 as printed in the AP&P Manual was retrieved — both live in the **paid** manual [R33].

**The CRVM guidelines an implementer will actually need**, from the VM-C index (the life half of the same index whose annuity half is already catalogued at R41) [R41]: **I** (valuation net premium exceeds gross), **IV** (minimum reserves for certain forms of term life), **V** (acceptable approximations for continuous functions), **VI** (single vs. joint life tables), **VII** (equivalent level amounts), **XIV** (surveillance procedure for review of the actuarial opinion), **XVI** (CRVM on select mortality and/or split interest), **XVII** (CRVM when death benefits are not level), **XVIII** (CRVM on semi-continuous, fully continuous or discounted continuous basis), **XIX** (1980 CSO with ten-year select factors), **XX** (joint life functions for 1980 CSO), **XXI** (CRVM when (b) is greater than (a), and rules for determining (a)), **XXV** (minimum reserves and nonforfeiture values for guaranteed increasing death benefits based on an index), **XXVI** (election of operative dates under the SVL and SNFL), **XXVII** (accelerated benefits), **XXXII** (reserve for immediate payment of claims), **XXXVI** (CRVM applied to equity indexed life), **XXXVII** (variable life reserves for guaranteed minimum death benefits), **XLII** (preferred mortality tables), **XLVI** (segment length when valuation mortality rates change after issue), plus **"AG App"**, the New York State Insurance Department appendix of maximum reserve valuation and maximum life policy nonforfeiture interest rates [R41]. **Verified negative finding: AG 53 and AG 55 do not appear in the VM-C index** — a full-text search of the 2026 Valuation Manual finds no "AG 53", "AG 55", "Guideline LIII" or "Guideline LV" anywhere [R3][R41]; both live in AP&P Appendix C [R105][R103].

### 3. Maximum valuation interest rate — the dynamic formula

**Life insurance (SVL §4b.B(1)(a); reproduced cleanly in VM-20 §3.C.2.a.i)** [R1][R3]:

```
I = 0.03 + W · (R1 − 0.03) + (W / 2) · (R2 − 0.09)
```

where **R1 = min(R, 0.09)**, **R2 = max(R, 0.09)**, **R** is the reference interest rate and **W** the weighting factor. Rounded to the **nearer one-quarter of 1%** [R1]; VM-20 specifies that ties round **down** to the lower quarter for this rate [R3].

**Single premium immediate annuities and life-contingent annuity benefits arising from other annuities and GICs with cash settlement options (§4b.B(1)(b))** [R1]:

```
I = 0.03 + W · (R − 0.03)          with W = 0.80
```

**Routing rules** [R1]: for *other* annuities and GICs **with** cash settlement options valued on an **issue year** basis, the **life** formula applies where the guarantee duration exceeds 10 years and the **SPIA** formula where it is 10 years or less; for annuities and GICs **without** cash settlement options, the SPIA formula; for annuities and GICs with cash settlement options valued on a **change in fund** basis, the SPIA formula.

**Weighting factors, life (§4b.C(1)(a))** [R1], identical to the VM-20 NPR table [R3]:

| Guarantee duration (years) | Weighting factor W |
|---|---|
| 10 or less | 0.50 |
| More than 10 but not more than 20 | 0.45 |
| More than 20 | 0.35 |

Guarantee duration for life insurance is "the maximum number of years the life insurance can remain in force on a basis guaranteed in the policy or under options to convert to plans of life insurance with premium rates or nonforfeiture values or both which are guaranteed in the original policy" [R1][R3].

**Weighting factors, other annuities and GICs (§4b.C(1)(c))** [R1], by **Plan Type** A/B/C and guarantee duration, on an **issue year** basis: 5 years or less 0.80/0.60/0.50; more than 5 but not more than 10 0.75/0.60/0.50; more than 10 but not more than 20 0.65/0.50/0.45; more than 20 0.45/0.35/0.35. On a **change in fund** basis those factors are increased by **+0.15 / +0.25 / +0.05** for Plan Types A/B/C respectively. A further **+0.05 for all three plan types** applies to issue-year contracts (other than those with no cash settlement options) that do not guarantee interest on considerations received more than one year after issue, and to change-in-fund contracts that do not guarantee rates on considerations received more than twelve months beyond the valuation date [R1].

**Plan Types** [R1]: **A** — withdrawal only with a market-value-type adjustment, or without adjustment in installments over five years or more, or as an immediate life annuity, or no withdrawal permitted. **B** — the same restrictions before expiry of the interest rate guarantee, with unadjusted single-sum or short-installment withdrawal permitted at the end of the guarantee. **C** — withdrawal before expiry of the guarantee in a single sum or installments over less than five years either without adjustment or subject only to a **fixed surrender charge stipulated as a percentage of the fund**.

**Guarantee duration for other annuities with cash settlement options** is "the number of years for which the contract guarantees interest rates **in excess of the calendar year statutory valuation interest rate for life insurance policies with guarantee duration in excess of twenty (20) years**"; for contracts with **no** cash settlement options it is the number of years from issue/purchase to scheduled annuity commencement [R1].

**Reference interest rate R (§4b.D)** [R1]: always the **monthly average of the composite yield on seasoned corporate bonds as published by Moody's Investors Service**, averaged as follows —

- **life**: the **lesser** of the 36-month average and the 12-month average ending **June 30 of the calendar year preceding the year of issue** [R1][R3];
- **SPIA and life-contingent annuity benefits**: the **12-month** average ending June 30 of the **calendar year of issue or purchase** [R1];
- other annuities/GICs with cash settlement options, issue-year basis, guarantee duration **> 10 years**: lesser of 36-month and 12-month averages ending June 30 of the year of issue/purchase; **≤ 10 years**: 12-month average [R1];
- no cash settlement options: 12-month average; change-in-fund basis: 12-month average ending June 30 of the **year of the change in the fund** [R1].

**Stability rule (§4b.B(2))** [R1][R3]: if the life rate computed without reference to the rule differs from the prior calendar year's actual rate by **less than one-half of 1%**, the rate is **set equal to the prior year's rate**. The rate is determined for 1980 using the 1979 reference rate and for every year thereafter regardless of the SNFL §5c operative date [R1].

**Fallback (§4b.E)** [R1]: if Moody's ceases publishing the composite yield, or the NAIC determines it is no longer appropriate, an **alternative method adopted by the NAIC and approved by regulation** may be substituted. A model should therefore treat the reference-rate series as a **configurable input**, not a hard-coded Moody's feed.

**The VM-20 NPR interest rate is the same machinery, plus a deficiency-style uplift** [R3]. For ULSG NPR amounts under §3.B.5.d the calendar-year NPR rate is the §3.C.2.a rate rounded to the nearest one-quarter of 1% (ties down). For **term** NPR amounts under §3.B.4 and for ULSG amounts under §3.B.5.c the rate is that rate **increased by 1.5%, but in no event greater than 125% of it**, rounded to the nearest one-quarter of 1% with **ties rounding up** [R3].

**Income annuities are on a different, market-linked mechanic (VM-V §1)** [R37]. Contracts in scope are assigned to one of **four Valuation Rate Buckets A–D**. With **no life contingencies**, the bucket is set by the **reference period (RP)** alone: RP ≤ 5y → A; 5 < RP ≤ 10 → B; 10 < RP ≤ 15 → C; RP > 15 → D. **With** life contingencies the bucket depends on RP **and initial age**: age 90+ follows the no-life-contingency mapping; ages 80–89 shift the first cell to B; ages 70–79 give C for RP ≤ 15 and D above; **ages under 70 are bucket D at every reference period** [R37]. A **jumbo contract** is one with initial consideration ≥ **$250 million** (contracts to the same holder within 90 days are combined, and if the combination qualifies each contract is jumbo); **jumbo rates are published daily** by the NAIC and **non-jumbo rates quarterly**, by the third business day of the quarter, on the Industry tab of the NAIC website [R37]. The underlying spread machinery uses **Table X spreads** (built like VM-20 Appendix 2.D Table F but averaging JP Morgan and Bank of America spreads over the quarter), **VM-20 Table A** expected default costs, and a **prescribed portfolio credit quality distribution of 5% Treasuries / 15% Aa (5% each of Aa1, Aa2, Aa3) / 40% A (13.33% each of A1, A2, A3) / 40% Baa (13.33% each of Baa1, Baa2, Baa3)**, with 40%/3 used unrounded [R37]. A change in consideration is **immaterial** — leaving the premium determination date unchanged — if it is a change in present value of **less than 10% and less than $1 million** [R37].

### 4. VM-20's three components and the formulaic/PBR boundary

**Scope.** VM-20 "constitute[s] the Commissioners Reserve Valuation Method (CRVM) for policies of individual life insurance" issued on or after the Valuation Manual operative date and subject to a principle-based valuation **with an NPR floor** under Model #820 [R3]. Individual certificates under a group life contract are pulled in — and VM-20 constitutes CRVM for them — only if **all** of five conditions hold, of which the first is an **individual risk selection process** based on characteristics beyond sex, gender, age, tobacco use and group membership; the Valuation Manual is explicit that **"[t]he use of evidence of insurability does not by itself constitute an individual risk selection process"** and that census-based rating does not qualify [R3].

**Three reserving categories** (VM-01 definition; VM-20 §2.A) [R3]: **Term**, **ULSG**, and **All Other VM-20**. The Term category also sweeps in term riders valued separately from any VM-20 base policy, riders and supplemental benefits valued *with* a term policy, and **life coverage of any kind assumed on a YRT basis that would have been VM-20 business if written direct** [R3]. The ULSG category includes directly written ULSG policies **even beyond the end of the contractual secondary guarantee period**, but excludes policies in extended term or reduced paid-up status [R3].

**Minimum reserve formula, per category** [R3]:

- Where the company computed **neither DR nor SR** (permitted only for ULSG with a *non-material secondary guarantee* passing both tests, or for All Other): **Σ policy minimum NPR**.
- Where the company computed the **DR but not the SR**: `Σ NPR + max(0, DR − (A − B))`, where **A = Σ policy minimum NPRs** for those policies and **B = any due and deferred premium asset** held on account of them.
- Where the company computed **all three**: `Σ NPR + max(0, max(DR, SR) − (A − B))`.
- **Total minimum reserve = the sum across the three categories** [R3].

Note the asymmetry a model must honour: **the DR/SR excess is measured net of the due-and-deferred premium asset**, and for the Term category the **valuation net premium is zero in the first policy year**, so the due-and-deferred premium asset and the unearned premium reserve are also zero in year 1 [R3].

**Allocation to policy level (§2.C)** [R3]: the category reserve is allocated to each policy **in proportion to that policy's minimum NPR**, with an explicit instruction to "make best efforts to minimize allocating the deterministic or SR in excess of the net premium reserve … to policies which did not produce this excess."

**Timing (§2.E)** [R3]: the **DR and SR may be computed as of a date no earlier than three months before the valuation date**, using relevant company data, provided an appropriate method rolls them to the valuation date. The three-month limit does **not** apply to experience-study data used to set prudent estimate assumptions.

**Separate account split (§2.F)** [R3]: the general account share may not be **less than zero** and must include any liability for general-account contractual guarantees; the separate account share must be **at least the sum of cash surrender values and at most the sum of account values** attributable to the separate account.

**Simplification discipline (§2.G, §2.H, §2.I)** [R3]: simplifications, approximations and modelling efficiency techniques are allowed only on a demonstration that they do not materially understate the reserve **and** that the expected value of the simplified reserve is not less than that of the unsimplified reserve; model segmentation for net asset earned rates is exempt from the demonstration. The company must establish a **materiality standard** for the DR and SR — stated as an impact relative to the **size of the NPR, DR and SR**, not relative to total company reserves or surplus — and that standard also governs the **exclusion tests** [R3]. §2.I lists things that are **not** valid simplifications: not computing even a simplified NPR; not computing a simplified DR or SR without passing the relevant test; omitting prescribed mortality margins; establishing no lapse margins; not building even a simplified asset model for the DR; using the alternative investment strategy without first showing it produces a higher reserve; and **ignoring post-level term losses** [R3].

**Economic scenario generator phase-in (§2.J)** [R3]: a company may phase the 2026 Appendix 1 (GOES) economic scenario requirements in over **36 months beginning Jan. 1, 2026**, elected before the Dec. 31, 2026 valuation and applied consistently to §4 and §5. The mechanics are `DR = D − (B − A)·(DR1 − DR2)/B` and `SR = S − (B − A)·(SR1 − SR2)/B`, where **B = 36**, **A = months elapsed since Dec. 31, 2025**, DR1/SR1 are computed on the 2026 scenario basis and DR2/SR2 on the 2025 basis, both as of Jan. 1, 2026 on the same in-force (including reinsurance expected to be recaptured during 2026) and **ignoring exclusion tests**; if the company passes the SET (or DET) before phase-in, the SR (or DR) phase-in amount is **deemed zero**; a material decrease in the book by sale or reinsurance scales the phase-in amount down proportionately [R3]. This mirrors the VM-21 phase-in already recorded at R35.

**The NPR (§3)** [R3]. Determined **seriatim**. Its structure by category:

- **Term** — §3.B.4 method, with prescribed shock-lapse structure.
- **ULSG** — §3.B.5, using the **fully funded / actual / level secondary guarantee** triple (FFSG, ASG, LSG) and shadow-account or cumulative-premium mechanics.
- **All Other VM-20, and IUL where no DR or SR was computed** — **"the NPR shall be determined pursuant to applicable methods in VM-A and VM-C for the basic reserve,"** using the mortality tables of §3.C.1 and VM-M §1.H [R3]. **This is the formulaic/PBR boundary**: for whole life, ordinary UL, VUL and un-modelled IUL the NPR *is* the old CRVM calculation.
- **Assumed YRT** — the reinsurer's NPR is **one half year's cost of insurance on the reinsured net amount at risk** [R3].

**NPR lapse assumptions (§3.C.3)** [R3]:

- ULSG under §3.B.5.d: **0% per year during and after the premium paying period**.
- Term under §3.B.4: **10%** during any level premium period of **less than five years**; **6%** during any level premium period of **five or more years**; for policies with an endowment at the end of the initial level period materially less than the face amount (e.g. return of premium), **6% for the first half of the initial level premium period and 0% for the remainder except the final year**; **10%** during any premium paying period after an initial level period of less than five years; **0%** for any policy whose final premium has already been payable.
- **Prescribed shock lapse table for the final year of a level premium period**, applied after benefits assumed payable in that year and before the increased premium takes effect [R3]:

| Level period before increase | Level period after increase | Gross premium increase per $1,000 | Shock lapse |
|---|---|---|---|
| 1 < PP ≤ 5 | 1 | any | 50% |
| 1 < PP ≤ 5 | 1 < PP | any | 25% |
| 5 < PP ≤ 10 | 1 | < 400% | 70% |
| 5 < PP ≤ 10 | 1 | ≥ 400% | 80% |
| 5 < PP ≤ 10 | 1 < PP ≤ 5 | any | 50% |
| 5 < PP ≤ 10 | 5 < PP | any | 25% |
| 10 < PP | 1 | < 400% | 70% |
| 10 < PP | 1 | ≥ 400% | 80% |
| 10 < PP | 1 < PP ≤ 5 | any | 70% |
| 10 < PP | 5 < PP | any | 50% |

- ULSG under §3.B.5.c uses a **level lapse rate computed at the valuation date and held constant for the whole projection**: `R(x+t) = (FFSG − ASG) / (FFSG − LSG)`, capped to [0, 1], then `L(x+t) = R(x+t)·0.01 + (1 − R(x+t))·0.005·r(x+t)` [R3]. At issue (ASG = 0) this gives a **1% level lapse rate** [R3].

**NPR floors (§3.D)** [R3]. For non-UL policies the NPR may not be less than the greater of (a) the **cost of insurance to the next paid-to-date**, based on the policy year containing the valuation date and the §3.C mortality tables, and (b) the **cash surrender value** at the valuation date computed consistently with the NPR. For a UL policy, (a) becomes the amount needed to cover the cost of insurance **to the next processing date on which COI charges are deducted**, based on the **net amount at risk**, with the Valuation Manual warning that "cost of insurance" here means the **valuation mortality rate, not the UL policy's contractual cost of insurance or expense charges" [R3]. **§3.E: the policy minimum NPR is the NPR less the credit for reinsurance ceded defined in §8** [R3].

**The NPR must reflect continuous deaths and immediate payment of death claims**, including on riders and supplemental benefits for which the NPR is being computed [R3].

**The DR (§4)** [R3]. Two permitted constructions, and a model should be able to do both because **VM-31 §3.D.2.h requires the company to state which one it used for each model segment** [R108]:

- **§4.A (gross premium valuation form)**: `DR = APV(benefits, expenses and related amounts) − APV(premiums and related amounts) − PIMR allocated at the valuation date + separate account asset balance + policy loan balance` (the last with due/accrued/unearned loan interest if loans are explicitly modelled). Cash flows are projected under **economic scenario 12** of §7.G.1 / Appendix 1.E, discounted on the **path of discount rates for the corresponding model segment** determined under §7.H.3. The APV of premiums and related amounts includes future gross premiums and other revenue, net separate-account-to-general-account flows, net policy loan cash flows, **net reinsurance cash flows under §8**, and **net cash flows of the derivative liability program** allocated to the group. Federal income taxes are **excluded** from projected expenses.
- **§4.B (direct iteration form)**: `DR = a − b` where **a** is the aggregate annual statement value of the starting assets which, projected with all premium and investment income, exactly liquidates all projected future benefits and expenses by the end of the horizon, and **b** is the allocated PIMR.
- **§4.C**: if a DR group spans more than one reserving category, a DR is computed for each single-category subgroup (the group's NAER may be used for discounting each), and if the subgroup DRs do not sum to the group DR the difference is allocated **proportionally** [R3].
- **§4.A.5**: a group excluded from the SR requirement **may not include future non-hedging derivative program transactions in its DR** [R3].

**The SR (§5)** [R3]. Project cash flows under the stochastic scenarios of §7.G.2. For **each** scenario: for each model segment, at the model start date and the end of each projection year, discount **the negative of the projected statement value of general account and separate account assets** on the §7.H.4 discount path from the projection start date; sum across model segments at each of those dates; the **scenario reserve = the statement value of starting assets across all model segments plus the maximum of those summed amounts**. Rank the scenario reserves low to high, take **CTE 70**, add any additional amount needed to capture material risks not reflected in the cash flow models, then subtract the allocated PIMR. If a subgroup used for aggregation spans reserving categories, **the SR must also be computed stand-alone for each category** [R3]. Aggregation subgroups must be consistent with how the company **actually manages risk** across products with significantly different risk profiles, reflecting distributional shifts between product types [R3].

**Cash-flow model requirements (§7.A, §7.B)** [R3]: model segments consistent with the company's **asset segmentation plan / investment strategies / statutory investment income allocation**; each policy assigned to **exactly one** model segment with a separate cash flow model per segment; the projection must extend "far enough into the future so that no obligations remain"; **federal income taxes are ignored** in both the DR and every SR scenario; all material product features, guaranteed and non-guaranteed, must be reflected; for ULSG with multiple secondary guarantees, **all** secondary guarantees must be taken into account; all due premiums as of the projection start date are assumed collected after the start date with a company-determined timing assumption, and — because the projection reflects premium mode directly — **deferred premiums are zero in the projection** [R3].

### 5. The exclusion tests — what determines the model's required capability

**Stochastic Exclusion Test (§6.A)** — three alternative routes to passing [R3]:

1. **Stochastic Exclusion Ratio Test (SERT)** — annually, and within 12 months before the valuation date.
2. **Stochastic Exclusion Demonstration Test** — in the first year and **at least once every three calendar years** thereafter, documented in the **PBR Actuarial Report**.
3. **SET Certification Method** — a qualified actuary certifies, in the first year and at least every third calendar year, that the group is **not subject to material interest rate risk or asset return volatility risk**. This route is **not available for variable life or ULSG** [R3].

**SERT arithmetic (§6.A.2)** [R3]. Pass if `(b − a) / c < 6%`, where

- **a** = the adjusted DR under **economic scenario 9, the baseline scenario** (Appendix 1.E);
- **b** = the **largest** adjusted DR under **any of the other 15** of the 16 prescribed scenarios;
- **c** = the present value of **benefits** for the policies under the baseline scenario, **adjusted for reinsurance by subtracting ceded benefits**, using the benefit cash flows from quantity "a" and the same discount path. The Valuation Manual is explicit that **premium, ceded premium, expense, reinsurance expense allowance, modified coinsurance reserve adjustment and reinsurance experience refund cash flows are not "benefits"**, while death benefits, surrender or withdrawal benefits **and policyholder dividends** are [R3].

A guidance note warns that the numerator is the **largest adjusted DR minus the baseline adjusted DR** — not the largest difference, and not the largest absolute difference, "both of which could lead to an incorrect test result" [R3].

**The adjusted DR may be built two ways (§6.A.2.b.i)** [R3], and this is architecturally decisive:

- (a) the §4.A DR, but with **scenario-specific interest rates and equity returns** and **scenario-specific NAER and discount rates** under §7.H; **or**
- (b) **"[t]he gross premium reserve developed from the cash flows from the company's asset adequacy analysis models, using the experience assumptions of the company's cash-flow analysis,"** with scenario-specific rates and §7.H discounting methodology but **the company's cash-flow-testing assumptions for default costs and reinvestment earnings** — provided the CFT model carries explicit margins and/or sensitivities such that **moderately adverse conditions** are reflected for risks other than the economic scenarios [R3].

So the Valuation Manual **explicitly contemplates one model serving both VM-30 cash flow testing and the VM-20 exclusion test**. VM-22 §7 carries an analogous "adjusted scenario reserve" route [R36][R109].

Companies must use the **most current baseline and 15 other economic scenarios published by the NAIC**, dynamically adjust assumptions for consistency within each scenario, and **may not group contract types with significantly different risk profiles** for the ratio [R3].

**YRT relief (§6.A.2.c)** [R3]: if the ratio is < 6% **gross of YRT** but > 6% **net of YRT**, the group still passes if the company demonstrates comparable economic sensitivity pre- and post-YRT. The stated acceptable demonstration: with "gross of YRT" meaning net of all non-YRT reinsurance but ignoring the YRT treaties and "net of YRT" meaning net of everything, compute the **largest percent increase in reserve** `LPIR = (b − a)/a` on both bases; the block passes if `SERT_gy × LPIR_ny / LPIR_gy < 0.060`. A more qualitative alternative is to show a similar pattern of sensitivity across the 16 scenarios gross and net [R3].

**Blocking rule (§6.A.2.d)** [R3]: the SERT **may not be used** if, with the current year's data, the Demonstration Test was already attempted under §6.A.3.b.i or .ii and failed, or if the qualified actuary actively undertook the certification method and concluded the certification could not legitimately be made.

**Demonstration Test (§6.A.3)** [R3]. Must give "reasonable assurance that if the SR was calculated on a stand-alone basis … the minimum reserve for those groups of policies would not increase," taking into account whether conditions over the current and **two subsequent** calendar years would change that conclusion; must **effectively evaluate residual risk after risk mitigation** such as derivative programs and reinsurance; and the exclusion **must be discontinued (and the SERT deemed failed) if at any year-end the minimum reserve no longer adequately provides for all material risks**. The four listed methods all compare `max(DR, NPR − due-and-deferred-premium-asset)` against either the stand-alone SR, the scenario reserve from **a sufficient number of adverse deterministic scenarios**, the SR on a **representative sample**, or a demonstration that the risk characteristics that would drive the SR above that maximum "are not present or have been substantially eliminated through actions such as hedging, investment strategy, reinsurance or passing the risk on to the policyholder by contract provision" [R3].

**Hedging bar (§6.A.1.b)** [R3]: a company **may not exclude from the SR** a group of policies for which there is one or more future hedging strategy, except where all such strategies relate solely to product features determined not to be material under §7.B.1 **due to low utilization**.

**Certification-method evidence (§6.A.1.a.iii guidance note)** [R3]: acceptable supports include showing the NPRs are at least as great as the assets required to support the policies **under each of the 16 SERT scenarios or, alternatively, each of the New York seven scenarios**; showing the SERT was passed within 36 months with no material change in interest rate risk; or a qualitative risk assessment covering product guarantees, the NGE policy, backing assets and investment strategy.

**Deterministic Exclusion Test (§6.B)** [R3]:

- **Deemed failures**: a ULSG group that does **not** meet the definition of a "non-material secondary guarantee", **or** any group not excluded from the SR requirement, **is deemed to fail the DET** and must compute the DR.
- **The DET may not be used at all for term insurance policies or term riders** [R3].
- **Deterministic Net Premium Test**: pass if the **sum of the valuation net premiums for all future years ≤ the sum of the corresponding guaranteed gross premiums**, performed on a **direct or assumed** basis [R3].
- **DET Certification Method**: for a group where all policyholders have converted to a product other than term, variable, indexed life or ULSG with a material secondary guarantee, a qualified actuary certifies (first year and at least every third calendar year) that the policy's total reserve includes a prudent provision for **excess conversion mortality** and reasonably exceeds the DR that would otherwise have been computed [R3].
- **Valuation net premium conventions for the test (§6.B.5)** [R3]: if the NPR comes from **VM-A/VM-C**, the valuation net premiums follow those minimum reserve requirements; if from §3.B.4 or §3.B.5, **lapse rates are set to 0% at all durations for the test**; for shock-lapse products the comparison is performed **considering only the initial premium period**; and if the **anticipated experience mortality plus §9.C.6 margins exceeds the prescribed CSO rates**, the company must use anticipated-experience-plus-margin mortality to determine the valuation net premium, mortality being measured as the **present value of future death claims at the valuation date discounted at the NPR valuation interest rate** [R3].
- **Guaranteed gross premium (§6.B.6)** [R3]: for UL, the premium specified in the contract inclusive of policy fee, or **if none is specified, the level annual gross premium at issue that would keep the policy in force for the entire coverage period on the policy guarantees of mortality, interest and expenses**; for non-UL, the guaranteed premium specified in the contract inclusive of policy fee.
- **Frequency relief (§6.B.4)** [R3]: a group closed to new issues that has passed three consecutive years passes until determined otherwise, and thereafter must be tested **at least once every five years**.
- **Grouping bar (§6.B.3)**: no grouping of contract types with significantly different risk profiles [R3].

### 6. VM-30 — the opinion and the memorandum

**Scope and standing** [R100]:
- Applies to companies filing the **life, A&H or fraternal** annual statement; P/C and health filers follow their own annual statement instructions unless those instructions point back to VM-30.
- The requirements must be applied so the appointed actuary can exercise professional judgment conforming to relevant ASOPs, **but a commissioner may specify methods of analysis and assumptions** when necessary for an acceptable opinion.
- **AG 48 and AG 51 are expressly made applicable for VM-30 purposes** [R100].
- An opinion and supporting memorandum are required **each year**, for annual statements with a year-ending date on or after the Valuation Manual operative date, **per company — not per holding company or group**, and **a single opinion is required for the company** [R100].

**Definitions of opinion outcomes** [R100]:
- **Adverse opinion** — the appointed actuary determines the reserves and liabilities are **not adequate** (fails the §3.A.7.e "include provision for all reserves and related actuarial items that ought to be established" statement).
- **Qualified opinion** — reserves for a certain item cannot be reasonably estimated or the actuary cannot opine on them; the opinion states whether the remainder makes adequate provision **except for** the qualified item. **No qualified opinion is required if the actuary reasonably believes the items are not likely to be material.**
- **Inconclusive opinion** — the actuary cannot reach a conclusion due to deficiencies or limitations in data, analyses, assumptions or related information, and must describe why.

**Appointment mechanics** [R100]: notice to the domiciliary commissioner **within five business days** of appointment; on replacement by board action, notice **within five business days** plus a separate letter **within 10 business days** stating whether there were **material disagreements with the former appointed actuary in the preceding 24 months** (resolved or not), the insurer must request a responsive letter from the former actuary and furnish it to the commissioner.

**Structure of the opinion** [R100]: **table of key indicators**, identification, scope, reliance, opinion, relevant comments. Each section has **prescribed wording**; any change or addition requires ticking the corresponding box and giving, in relevant comments, a description of the revised wording, the rationale, and **the impact on the opinion**. The table of key indicators carries one box per section (Prescribed Wording Only / Prescribed Wording with Additional Wording / Revised Wording), a box for whether the **actuarial memorandum includes "Deviation from Standard" wording** regarding conformity with an ASOP, a box for whether relevant comments are included, and the **Category of Opinion**: Unqualified / Adverse / Qualified / Inconclusive [R100].

**The asset-adequacy-tested amounts table** [R100] is the reporting granularity a model must be able to hit. Rows are annual statement lines: **Exhibit 5** (A Life Insurance, B Annuities, C Supplementary Contracts Involving Life Contingencies, D Accidental Death Benefits, E Disability—Active, F Disability—Disabled, G Miscellaneous), **Exhibit 6** (Active Life Reserve, Claim Reserve), **Exhibit 7** (Guaranteed Interest Contracts, Annuities Certain, Supplemental Contracts, Dividend Accumulations or Refunds, Premium and Other Deposit Funds), **Exhibit 8 Part 1** (Life, Health), **Separate Accounts** (page 3 of the separate accounts statement, lines 1 and 2), plus free-text "Other Reserves and Related Actuarial Items Tested" and **TOTAL RESERVES**; below the table, **IMR** (general account and separate accounts, by page/line), **AVR** (allocated amount, by page/line) and **Net Deferred and Uncollected Premium** [R100]. Columns: **(1) Formula Reserves, (2) Principle-Based Reserves, (3) Additional Reserves, Analysis Method, (4) Other Amount, (5) Total = (1)+(2)+(3)+(4)** — **every line even if zero**, and if more than one analysis method is used on a line, **an additional line per method** [R100].

**IMR and AVR in the analysis (§3.B.5, §3.B.6)** [R100]:
- **An appropriate allocation of assets in the amount of the IMR, positive or negative, shall be used in any asset adequacy analysis.**
- Any portion of the **total company IMR balance that is not admitted** under statutory accounting must be **removed first**.
- **The full amount of any admitted negative IMR balance must be used**; in the negative case **the allocated assets are reduced by the absolute value of the negative IMR**.
- Asset default risk analysis **may** include an appropriate allocation of assets supporting the **AVR**, and those AVR assets **may not be applied for any other risks** with respect to reserve adequacy.
- **The amount of assets used for the AVR must be disclosed** both in the opinion's reserve table and in the memorandum, and the method for selecting particular assets or allocated portions must be disclosed in the memorandum.

**Equity return volatility (§3.B.7)** [R100] — the newest substantive modelling requirement in VM-30, and one that changes what a CFT engine must support. When the form of asset adequacy analysis is **cash flow testing**, the actuary "should reflect how the volatility of investment returns for equity-like instruments may affect the asset adequacy results under moderately adverse conditions and **shall not solely project the anticipated long-term average return** (e.g., a single level assumption set to the long-term average)." The four listed acceptable approaches are: **(i)** stochastic modelling of equity returns with accompanying risk-metric analysis; **(ii)** including up, down and/or volatile equity return scenarios **for each given set of interest rate paths**; **(iii)** projecting one or more **market drops**, considering future points at which CFT results could be vulnerable; **(iv)** a **level return assumption set to a tail risk metric, for example the average of the worst 30% of future scenarios, i.e. CTE70** [R100]. A qualitative description of why the chosen equity scenario is moderately adverse in light of the current or reinvestment portfolio should be provided [R100]. (The Academy notes this came in via **APF 2023-12**, adopted 2024, effective 2025 [R111].)

**Memorandum contents (§3.B.10 – §3.B.13)** [R100]. **For reserves**: product descriptions including market, underwriting and risk profile and the specific risks the actuary deems significant; source of liability in force; **reserve method and basis**; investment reserves; **reinsurance arrangements**; identification of explicit or implied **general account guarantees supporting separate account benefits** and how they were provided for; and documentation of assumptions for **lapse rates (base and excess), interest crediting rate strategy, mortality (including base and future improvement or deterioration), policyholder dividend strategy, competitor or market interest rate, annuitization rates, commissions and expenses, and morbidity** — documented such that a reviewing actuary could conclude on their reasonableness **and on whether they contribute to the conclusion that reserves make provision for "moderately adverse conditions"** [R100]. **For assets**: portfolio descriptions with quality/distribution/type risk profile; investment and disinvestment assumptions; source of asset data; asset valuation bases; and documented assumptions for **default costs, bond call function, mortgage prepayment function, market value for assets sold under the disinvestment strategy, and yield on assets acquired under the investment strategy** [R100]. **For the analysis basis**: methodology; rationale for inclusion/exclusion of blocks and how pertinent risks were analysed; **rationale for the degree of rigor, including the materiality level used**; **criteria for determining asset adequacy, including the precise basis for determining adequacy under "moderately adverse conditions"**; and **whether federal income taxes were considered and the method of treating reinsurance** [R100]. Plus a summary of material changes from the prior year, a summary of results, and conclusions [R100]. **Seven-year retention of documentation sufficient to determine procedures followed, analyses performed, bases for assumptions and results obtained** [R100].

**Regulatory Asset Adequacy Issues Summary (§3.B.14)** [R100]. Due to the **domiciliary commissioner no later than April 1** of the following year (contrast **March 15** under Model #822 [R101]), available to other commissioners on request, confidential to the same extent as the memorandum. Contents:

- key indicator **"This opinion is unqualified: Yes / No"**, with an explanation if "No";
- **descriptions of the scenarios tested, including whether stochastic or deterministic**, and the sensitivity testing relative to them;
- if negative ending surplus results in the aggregate under certain tests, a description of those tests and **the amount of additional reserve as of the valuation date that would eliminate the negative aggregate surplus**;
- **ending surplus values must be determined either by extending the projection until the in-force and associated assets and liabilities are immaterial, or by adjusting the end-of-projection surplus by an amount that appropriately estimates the value expected to arise from what remains in force** — this is the operative definition of "ending surplus" for a CFT engine [R100];
- a tabular or other summary of testing results sufficient to give a clear understanding of the basis for the opinion;
- the extent to which assumptions are **materially different from the previous analysis**;
- the amount of reserves and **identity of product lines tested in the prior opinion but not in the current one**;
- comments on **interim results** of significant concern;
- **the methods used to recognize the impact of reinsurance on the company's cash flows, assets and liabilities, under each scenario tested**;
- confirmation that **all options, explicit or embedded, in any asset or liability (including those affecting cash flows embedded in fixed income securities) and equity-like features in any investments** have been appropriately considered [R100].

### 7. ASOP 22 — the analysis standard behind the opinion

**Definitions that a model must implement, not merely quote** [R29]:
- **Asset adequacy analysis** — "[a]n analysis of the adequacy of reserves and other liabilities being tested, in light of the assets supporting such reserves and other liabilities, as specified in the statement of actuarial opinion."
- **Cash flow testing** — "[t]he projection and comparison of the timing and amount of cash flows under one or more scenarios in order to evaluate cash flow risks."
- **Gross premium reserve** — "[t]he actuarial present value of future benefits, expenses, and related amounts less the actuarial present value of future gross premiums and related amounts." (Note this is the same construction as the VM-20 §4.A DR [R3].)
- **Moderately adverse conditions** — "[c]onditions that include one or more unfavorable, but not extreme, events that have a reasonable probability of occurring during the testing period."
- **Scenario** — "[a] set of economic and other assumptions used in asset adequacy analysis."

**The starting-asset rule (§3.1)** [R29] — the most important single sentence for a model's initialisation:

> "the actuary should choose a block of assets such that the statement value of those assets is **no greater than** the statement value of the reserves and other liabilities being tested."

If additional assets are needed under moderately adverse conditions, the actuary **establishes an additional reserve equal to the statement value of those additional assets and re-tests including them** [R29]. Assets must not be ones supporting other liabilities [R29]. New York states the same constraint in §95.10(b) [R112].

**Analysis methods (§3.1.1)** [R29], in order of the standard's own listing: cash flow testing (generally appropriate where cash flows vary under different economic scenarios), **gross premium reserve test** (e.g. term backed by non-callable bonds), **demonstration of conservatism**, **demonstration of immaterial variation** (e.g. a non-life-contingent payout annuity backed by a cash-flow-matched portfolio), **risk theory techniques**, **loss ratio methods**.

**Assumptions** [R29]: consider **trends** (differing by product — mortality improvement may differ between life and annuity; source and credibility of data; effect of future economic conditions on policyholder elections); consider **margins**, taking into account level of uncertainty and sparsity of data, degree of adverse deviation covered, whether margins vary over time, individual versus aggregate margins, interaction between assumptions, and **the possibility that more than one adverse condition could occur at once**; choose **discount rates consistent with the yield on the chosen assets, the investment strategy used, and the testing horizon**; and consider **sensitivity testing** of individual assumptions and combinations [R29].

**Reinsurance ceded (§3.1.3)** [R29]: consider reflecting ceded cash flows whether the company is a direct writer or a reinsurer, soliciting information from management on the extent of reinsurance, the associated cash flows, **their collectability**, disputes with reinsurers, and provisioning practice — while noting that this does not imply an opinion on any reinsurer's financial condition.

**Aggregation (§3.1.4, §3.2.4)** [R29]: blocks may be aggregated **if the assets or cash flows from the blocks are available to support the aggregated liabilities**, and assets or cash flows from one block may not be used to discharge another's liabilities if they cannot legally be used for that purpose. When offsetting deficiencies against sufficiencies at the reporting stage, take into account the **type and timing of cash flows, the related cash flow risks, and the comparability of analysis methods, scenarios, discount rates and assumption sensitivity**.

**Use of cash flows from other financial calculations (§3.1.5)** [R29] — the explicit bridge between a PBR/capital model and an AAT model. If PBR or capital-model cash flows are reused, the actuary must take into account differences in **starting assets; assumptions including margins; sensitivities; any interim shortfalls in accumulated cash flows; any legally-required aggregation of results; distribution of surplus; and taxes**, and must confirm the underlying assumptions are appropriate for an analysis **under moderately adverse conditions**.

**Separate account assets (§3.1.6)** [R29]: separate account assets **in excess of** separate account reserves and other liabilities may be included, which reduces the general account assets used; legal restrictions on chargeability must be taken into account.

**Management action (§3.1.7)** [R29]: reflect in-force management actions only in light of the insurer's **capacity and intent**, documented procedures and historical practice, policy provisions, consistency with policyholder behaviour assumptions, **impediments to the implementation timeline such as the need for regulatory approval**, and compliance with applicable law; consider quantifying their impact.

**Testing horizon (§3.1.9)** [R29]: extend "to a point at which, in the actuary's professional judgment, the use of a longer period would not materially affect the results."

**Completeness (§3.1.11)** [R29]: take into account renewal premiums, guaranteed **and non-guaranteed** benefits and charges, expenses and **taxes**; take into account the company's asset segmentation system; and confirm that any reserves reported as "not analyzed" are immaterial.

**Forming the opinion** [R29]: a failing scenario **does not automatically require an additional reserve** — "if a large number of scenarios were run, the failure of a small percentage of them may not indicate the need for additional reserves"; and holding reserves great enough to withstand **any conceivable** circumstance may imply an excessive reserve level.

**Section 4 disclosures** [R29] read as a specification for a model's output artefacts: intended purpose and adequacy statement; whether additional reserves were established; **the assets chosen, the methodology for their selection, and their appropriateness**; the analysis methods and the support for their appropriateness; **the material risks analysed, the sensitivity tests performed and their results**; assumptions and trends; **margins, disclosed even where the actuary concludes no margin is necessary**; **discount rates used**; whether and how ceded reinsurance was reflected; whether aggregation was done during testing or during analysis of results; **the use of cash flows from other financial calculations**; separate account treatment; management actions; use of prior-period data; **testing horizon**; material changes in methods, models or assumptions; the basis for judging "not analyzed" amounts immaterial; reliance on others; subsequent events; **the criteria used to form the adequacy opinion**; and any deficiencies or limitations.

### 8. AG 53 — asset-side discipline inside asset adequacy analysis

**Definitions** [R105]:
- **Equity-Like Instruments** — assets in the **common stock** category for RBC C-1 reporting (a **30% or higher** RBC charge), **any asset captured on Schedule A or Schedule BA**, and **bond funds**.
- **Net Market Spread** — for each asset grouping, the spread over comparable Treasuries that **equates the fair value at the valuation date with the modelled cash flows**, less the default assumption used in the analysis. Market conventions and approximations are acceptable.
- **Investment Grade Net Spread Benchmark** — the Appendix I spread for the asset's **weighted average life (WAL)**.
- **Guideline Excess Spread** — Net Market Spread minus the Investment Grade Net Spread Benchmark, for non-equity-like instruments, **excluding investment expenses**.
- **Projected High Net Yield Assets** — currently held **or reinvestment** assets that are either (i) an **equity-like instrument assumed to have a higher value at projection year 10 or later than under an assumption of annual total returns, before investment expenses, of 4% for the first 10 projection years and 5% from projection year 11 on**, or (ii) non-equity-like assets whose assumed **Guideline Excess Spread is above zero**. Aggregation for both tests must be at a granularity **consistent with or more granular than** the asset grouping used in the AAT model [R105].

**Appendix I — Investment Grade Net Spread Benchmark** [R105]:

| WAL (weighted average life) | Benchmark (bps) |
|---|---|
| 1–10 | **170** |
| 11–20 | **175** |
| 21–30 | **185** |

**Excluded asset types** (out of scope of §§4.A.ii–5) [R105]: cash and cash equivalents; Treasuries and agency bonds; **public non-convertible, fixed-rate corporate bonds with no or immaterial callability**.

**Documentation (§4)** [R105]: for **all** assets, identify the assumed **gross** yield and the key components deducted (e.g. default, investment expenses) to reach the assumed **net** yield, and explain any future reinvestment strategy assumption that materially differs from current practice. For **Projected High Net Yield Assets**, additionally explain the relationship between expected gross returns and risk, including, for any excess return **not** assumed to be associated with higher risk, how such "overperforming assets with expected returns lying outside the risk-return spectrum can be assumed to persist and be available for reinvestments throughout the projection period in moderately adverse conditions"; comment on margins for assets with substantial return volatility; identify which **major product categories** these assets support (the guideline names "individual fixed annuities and pension risk transfers"); and explain why complex-asset assumptions did or did not change from the prior year [R105].

**Model rigor (§4.B)** [R105]: where traditional techniques do not capture the risks, use **multi-scenario testing specific to complex assets**; project asset cash flows to reflect **anticipated liquidity under adverse conditions**, or apply sufficient additional conservatism; apply an **additional margin where the modelling process is complex and the potential disconnect between reality and modelling increases**, always in the direction of **less favourable** results; and consider the **full distribution** of risk. Simplifications are allowed only where they do not make results more favourable, and become less appropriate as complex high-yielding assets become a higher percentage of total assets [R105].

**Fair value (§4.C)** [R105]: fair value should be determined **internally only when a market-based value cannot be obtained or expected in a projected scenario**; where a material portion of supporting assets is internally valued, the memorandum must contain a **step-by-step description** of the approach, the **total fair value** so determined, and a **sensitivity test applying a haircut** to internally derived fair values.

**Non-publicly traded and affiliate-originated assets (§4.D)** [R105]: document valuation practices, give the **total fair value**, and **disclose contractual agreements and revenue sharing (e.g. performance fees)** between the entity providing investment services and the insurer where they affect the investment income in the analysis. Assumed net asset cash flows must be **net of all explicit or implicit fees or expenses, including origination fees**, and reflect credit, illiquidity and other market risks [R105]. **§4.E**: assumed investment expenses, internal or external, must be commensurate with the complexity of the assets. **§4.G**: identify any modelled **borrowing** other than for very short-term liquidity, and verify borrowing and reinvestment rates so that projections do not materially benefit from **arbitrage**.

**The two prescribed sensitivity tests (§5.A)** [R105], to be performed and disclosed **separately**:

- **(a)** for reinvestment assets **other than** equity-like instruments, assume the **Net Market Spreads (before investment expenses) for Projected High Net Yield Assets do not exceed the Investment Grade Net Spread Benchmark**, applied against a **baseline of a level Treasury rate scenario**. For this purpose such assets may be aggregated among themselves but **not with assets that are not Projected High Net Yield Assets**.
- **(b)** for reinvestment assets that **are** equity-like instruments, assume annual total returns before investment expenses of **4% for the first 10 projection years and 5% from projection year 11 on**.

The guideline is explicit that these sensitivity tests **do not themselves constitute a statement about moderately adverse conditions**, but the volatility and impact they show must be contemplated in the §4.A.ii(b) margin discussion [R105].

**Attribution analysis (§5.B)** [R105]: for non-equity-like Projected High Net Yield Assets, held and reinvested, state the assumed **Guideline Excess Spread** and estimate the proportion attributable to **credit risk, illiquidity risk, deviation of current spreads from the Appendix I long-term spreads, and volatility and other risks**, with commentary and rationale.

**Filing (§6)** [R105]: a **separate, easily identifiable section of the VM-30 actuarial memorandum or a standalone document**, due **April 1** following the valuation date, hardship extensions at the domiciliary commissioner's discretion, available to other states on request, and covered by the **Model #820 confidentiality provisions** for the actuarial memorandum. Templates (asset summary; components of net asset yield by asset class, separately for initial and reinvestment assets; sensitivity test aspects; sensitivity test results; attribution analysis) are published under the LATF web page's Documents tab [R105].

### 9. AG 55 — asset adequacy testing for reinsurance

**Effective date and deliverable** [R103]: effective for the asset adequacy analysis of reserves reported in the **December 31, 2025** annual statement and all subsequent ones; documentation, sensitivity test results and attribution analysis go in a **separate, easily identifiable section of the VM-30 memorandum or a standalone document, due April 1** following the valuation date, with the same confidentiality and hardship-extension provisions as AG 53 [R103].

**Scope (§2)** [R103]. Applies to life insurers with **Asset Intensive Reinsurance Transactions ceded to entities not required to submit a VM-30 memorandum to U.S. state regulators**, where either:

- **A.** the transaction was **established 1/1/2016 or later** and, **by counterparty**, meets any of: reserve credit or modco reserve **over $5 billion**; or combined reserve credit and modco reserve over **$1 billion and 5%**; or over **$500 million and 10%**; or over **$100 million and 20%** — the percentage in each case measured against **ceding company Exhibit 5 gross life plus Exhibit 5 gross annuity reserves plus Exhibit 7 reserves and separate account reserves**, to the extent those reserves are included in the combined reserve credit and modco reserve; **or**
- **B.** regardless of establishment date, the transaction "results in significant reinsurance collectability risk as determined according to the judgment of the ceding company's **appointed actuary**."
- **C.** For transactions established **1/1/2016 through 12/31/2019** otherwise in scope under A, exemption may be requested from the domestic regulator on the §5.H criteria or where the reinsured policies are **primarily older business issued earlier than 2010** [R103].

**Asset Intensive Reinsurance Transactions** are "[c]oinsurance arrangements involving life insurance products that transfer significant, inherent investment risk including credit quality, reinvestment, or disintermediation risk **as determined by Appendix A-791** of the Life and Health Reinsurance Agreements Model Regulation" [R103] — i.e. the same A-791 that VM-A indexes [R110].

**The reserve definitions that drive the whole guideline** [R103]:
- **Pre-reinsurance Reserve** — the U.S. statutory reserve the ceding company **would** hold for the reinsured business **in the absence of the transaction**.
- **Post-reinsurance Reserve** — reserves held by the **ceding** company **plus** reserves held by the **assuming** company **minus** reserves held by the assuming company **supported with Guideline Excluded Assets**.
- **Reserve Decrease** — the excess of the Pre- over the Post-reinsurance Reserve.
- **Guideline Excluded Assets** — non-admitted assets; assets permitted to be admitted by the ceding company's domiciliary regulator but otherwise non-admitted; **letters of credit; contingent notes; credit-linked notes; excess of loss (XOL) reinsurance; parental and affiliate guarantees**.
- **Deficient Block / Sufficient Block** — negative / positive present value of ending surplus in CFT scenarios using reasonable assumptions under moderately adverse conditions, **with negative interim surplus values considered** in the determination.
- **Excess Capital** — assets available to support a block over and above the Post-reinsurance Reserve.
- **Starting Asset Amount** — the amount of assets inserted into the CFT model at the beginning of the projection.

**Risk-graded rigor (§4)** [R103]: "[t]he higher the risk, the more rigorous and frequent the analysis and documentation." The named risks are: **no VM-30 memorandum from the assuming company to a U.S. regulator**; a **significant Reserve Decrease** relative to the Pre-reinsurance Reserve; **significant use of Guideline Excluded Assets**; and **collectability risk** evidenced by counterparty rating, capital position and trend, regulatory actions, liquidity ratios, late payments, or decline in invested-asset quality. Risk mitigants such as **trusts or funds withheld** may be considered [R103].

**Cash flow testing mechanics (§6)** [R103]:
- **One mandatory run with Starting Asset Amount equal to the Post-reinsurance Reserve.** The Starting Asset Amount basis (book value or market value) must be **consistent with the basis used in the assuming company's balance sheet**.
- An **Alternative Run** with a higher Starting Asset Amount is optional and must be justified; the principles that would support a higher amount are dedicated non-excluded assets, demonstrably available non-excluded assets, an explanation of any Guideline Excluded Assets used, and demonstrated **appropriate Excess Capital** — with the pointed caveat that if little or no Excess Capital is available, the **Starting Asset Amount should be reduced** so that appropriate Excess Capital remains to support the block beyond moderately adverse conditions (conditions "contemplated in the US risk-based capital (RBC) system") [R103].
- **Captive retrocession rule:** where business ceded to an affiliated captive is retroceded to an affiliated reinsurer and the captive does not file, **the mandatory-run Starting Asset Amount is the Post-Reinsurance Reserve held by the affiliated reinsurer for the captive** [R103].
- **Scenarios:** "[p]rojection on interest rate scenarios, **such as the New York 7** as described in Appendix 1, that allow for easy to review impact of **reinvestment and disintermediation** risks should be performed"; if the ceding company already projects the New York 7 for its VM-30 filing, it is "highly encouraged" to present them here too [R103].
- **Assets:** if the ceding company knows the actual supporting assets, **model them**; if not, use **reasonably conservative assets and asset-related assumptions**, explain why they are conservative, and say what the ceding company does know about the assets or investment strategy [R103].
- **PBR shortcut (§6.G):** for business valued under PBR, **documentation of the pre-reinsurance PBR reserve for the ceded block (computed per VM-20, VM-21 or VM-22), reflecting both liabilities and supporting assets under moderately adverse conditions, is appropriate in lieu of separate cash flow testing**; that pre-reinsurance PBR reserve is then compared with the Post-reinsurance Reserve to judge deficiency or sufficiency [R103]. **This is a direct instruction to run the PBR engine gross of the ceded treaty** — a capability many production models do not have.

**Attribution Analysis (§7)** [R103]: start from the Pre-reinsurance Reserve and document step-by-step adjustments to the Post-reinsurance Reserve. Named adjustment categories: differences in **policyholder behavior**, **mortality or longevity**, **investment return assumptions versus U.S. statutory discount rates**, and other key assumptions such as taxes; plus other reserve adjustments for **removal of the cash surrender value floor**, **market value / book value difference due to change in interest rates**, **conversion from moderately adverse to less adverse (or best estimate)**, and other changes to fair value or future cash flows [R103]. The order of adjustments must be commented on where a different order would change the picture. **Attribution analysis is required** where a treaty otherwise in scope is exempted under §2.C or §5.H, unless supporting analysis concludes the §4 risks are immaterial; where compliant CFT is already performed, attribution is **preferred but not required** [R103].

**Aggregation (§8)** [R103]: CFT is performed **separately by counterparty**; for **year-end 2026 and later**, also **separately by significant product line** consistent with the VM-20/VM-21/VM-22 aggregation standards, **and separately for PBR versus non-PBR business**. Subsidy of a Deficient Block by a Sufficient Block is permitted **only within a counterparty**, and the company must explain the **stability and reliability** of the subsidising block and why no additional AAT reserve was posted [R103].

**Reporting (§9)** [R103] requires, among other things, **Schedule S** information per treaty (assuming company name and jurisdiction; type — coinsurance, ModCo, etc.; reserve credit, trust amount, ModCo account amount, funds withheld account amount; type of insurance covered), the Pre- and Post-reinsurance Reserves, the Alternative Run Starting Asset Amount with justification, assumption overviews (net asset yields; **mortality as a percentage of a common industry table**; **base and dynamic lapse rates affecting reinvestment risk in falling rates and disintermediation risk in rising rates**; benefit utilization and other behaviour; margins), CFT results (**present value of ending surplus for the level scenario and a range of others**, including the New York 7; sensitivity tests on mortality, lapse, benefit utilization and asset underperformance; **interim negative results with negative surplus by year where significant and how they are addressed**), attribution analysis, and risk identification [R103].

**Appendix 1 — the New York 7, verbatim** [R103], quoted as an excerpt from §95.10(d) of New York Regulation 126 [R112]:

1. level with no deviation;
2. uniformly increasing over 10 years at 0.5% per year and then level;
3. uniformly increasing at 1% per year over five years, then uniformly decreasing at 1% per year to the original level at the end of 10 years, then level;
4. an immediate increase of 3% and then level;
5. uniformly decreasing over 10 years at 0.5% per year and then level;
6. uniformly decreasing at 1% per year over five years, then uniformly increasing at 1% per year to the original level at the end of 10 years, then level;
7. an immediate decrease of 3% and then level.

With the floor: "[f]or these and other scenarios which may be used, **projected interest rates for a five-year treasury note need not be reduced beyond the point where such five-year treasury note yield would be at 50 percent of its initial level**" [R103][R112].

### 10. VM-31 — what the model must be able to evidence

**Filing and form** [R108]: Executive Summary + Life Summary + Annuity Summary by **April 1**; entire report on request by April 1 or within 30 days if requested later; **searchable PDF, ≥ 10 pt narrative**, spreadsheets for large data arrays counting as part of the report; **seven-year retention from the date of filing**; the report must keep the prescribed order and headers and explain any non-applicable requirement.

**Executive Summary (§3.B)** [R108]: identification and qualifications of each sub-report's qualified actuary; the groups of policies and contracts covered by each sub-report; **a summary of base policies within each VM-20 reserving category using PBR Actuarial Report Template A**, with descriptions of each product type and **underwriting process (the process, the period in which it was used, and the level of any additional margin)** and a breakdown of **policy count and face amount** by product type and underwriting process, plus target market, primary distribution system and **key product features that affect risk, including conversion privileges**; a description of VM-21 and VM-22 contracts by Reserving Category with their guarantees; **High-Level Results** — a table of final reported reserves, policy/contract counts, face amounts (VM-20) or in-force account values (VM-21/VM-22), for **current and prior year and on both a pre- and post-reinsurance-ceded basis**; and a statement that governance documentation under VM-G §§2.A.5, 3.A.6 and 4.A.3 is available on request. A guidance note confirms **AG 43 contracts are documented as VM-21 business** [R108].

**Life Summary (§3.C)** [R108]: the **VM-20 §2.H materiality standard**; a summary of **material risks and of risks subject to close monitoring** by the board, company, qualified actuary or any state regulator; any **significant unresolved issues** under VM-G §4.A.5; a description of **changes in reserve amounts from the prior year and why they are reasonable**; changes in methods used to model cash flows or determine assumptions and margins, with rationale; a description of the asset portfolio and of the approach to **hedging and other derivative programs, including any future hedging strategies and material changes to them**; **any material differences in methods, assumptions or risk management practices between groups of policies covered in separate sub-reports, to the extent not explained by product features**; a closing signature block; **copies of Parts 1 and 2 of the VM-20 Reserves Supplement from the annual statement blank**; and a **reconciliation of reported values** between the High-Level Results, the VM-20 Reserves Supplement Parts 1A and 1B, and the Annual Statement (Exhibit 3 for separate account, Exhibit 5 for general account).

**Life Report (§3.D)** [R108], the parts that constrain model design:
- **§3.D.1 Assumptions and Margins** — for each material risk, the **anticipated experience assumption, the margin, and the prudent estimate assumption used in the model, provided in Excel format**; changes since the last report; for each risk factor, via **Template C**, the policy types by reserving category, the year of the most recent experience study, its observation calendar years, the policy issue years included, and **the lag time allowed for events reported after the study period**; and, for each risk factor, the methods used to develop anticipated experience and margins, the sources of experience, how changes are monitored, **any adjustments increasing mortality margins above the prescribed margin (e.g. for newer underwriting approaches)**, and any other considerations such as conversion features.
- **§3.D.2 Cash-Flow Models** — description of the **modelling system(s) for assets and liabilities**, naming the **vendor and model version number**, the degree of customisation, the extent and function of **pre- and post-processing tools**, and how multiple systems interact; description and rationale for **model segments**; the approach and rationale for **grouping (compression) of assets and policies separately for the DR and, if different, for the SR**, with a clear indication of how §2.G was met and documentation that, on request, information can be produced to permit an **audit of any subgroup against a seriatim model**; **calculation and model validation** — how the model was evaluated for appropriateness, **how the model results compare with actual historical experience**, **tables of numerical static and dynamic validation results with commentary**, which risks are not modelled, and any model limitations that could materially impact the NPR, DR or SR; **projection period** length with support for the conclusion that no obligations remain, for both deterministic and stochastic models; how **reinsurance cash flows** are modelled; and **which DR method was used for each model segment — gross premium valuation (§4.A) or direct iteration (§4.B)**.
- **§3.D.3 Mortality** — mortality segments and rationale; company experience by segment; the **industry basic table** used per segment with rationale; documentation where more aggregate company experience is used under §9.C.2.d; **description, rationale and results of applying the Relative Risk Tool** and the analysis relating it to anticipated mortality; alternative data sources with **number of deaths and death claim amounts by age, gender, risk class and policy duration**; and rationale and published-study citations for any adjustments to company experience mortality.
- Certifications by an **Investment Officer on Investments** and a **Qualified Actuary on Investments** are required at §§3.D.14.a/b and 3.F.19.a/b and must be reported to the board through VM-G §3.A.6.d.ii [R109].

### 11. Projecting statutory reserves forward — what the different frameworks actually require

This is the practical question a projection model must answer, and the frameworks answer it
differently. What was verified:

- **VM-20 DR and SR do not project future statutory reserves at all.** The DR is either a gross premium valuation (§4.A) or an amount of starting assets found by **direct iteration** (§4.B); the SR is built from **the projected statement value of general and separate account assets**, discounted, maximised over projection years, added to starting assets [R3]. There is no future-reserve term anywhere in either construction. Federal income taxes are excluded [R3].
- **Cash flow testing does need a reserve-like quantity, but at the end, not throughout.** VM-30 defines **ending surplus** operationally: extend the projection until the remaining in-force and associated assets and liabilities are immaterial, **or** adjust the end-of-projection surplus by an amount that appropriately estimates the value expected to arise from what remains [R100]. So a CFT engine needs either a long enough horizon or a terminal-value routine — **not** a full statutory reserve roll-forward.
- **The discount rate for the present value of ending surplus is a modelling choice, not a prescription.** Reported practice includes the pre- or after-tax **portfolio earnings rate** over the projection (with or without policy loan interest), **Treasury spot rates** for the projection length, and **re-running the scenario with additional initial assets and inferring the discount factor from the change in ending surplus**; the 2012 survey distribution was after-tax earned rate including policy loan interest 36%, after-tax excluding 24%, other 16%, with smaller shares for the remaining methods, and about **15% of respondents did not compute a present value of ending surplus at all** [R111]. Some actuaries avoid discounting entirely by **iterating the starting asset amount until ending surplus is immaterial** — which the practice note itself observes "is much like the **direct iteration approach used in VM-20 and VM-21**" [R111]. **A single direct-iteration routine therefore serves the VM-20 §4.B DR, the VM-21 reserve, and the CFT ending-surplus problem.**
- **The starting asset amount is the real constraint, and it is a reserve.** ASOP 22 §3.1 caps the statement value of chosen assets at the statement value of the reserves being tested [R29]; NY Reg 126 §95.10(b) states the same [R112]; AG 55 §6.B fixes the mandatory-run Starting Asset Amount at the **Post-reinsurance Reserve** [R103]; C-3 Phase II models the statutory reserve **as equal to the working reserve** [R47].
- **Where statutory reserves genuinely must be projected**, it is on the capital and distributable-earnings side: the C-3 Phase II scenario asset requirement is the negative of the lowest present value of **accumulated statutory surplus including federal income tax**, which requires a projected statutory balance sheet [R47]. A **Tax Adjustment** is then required where modelled tax reserves are set to Working Reserves but actual tax reserves exceed them at the projection start [R47].
- **Reported projection horizons** (2012 survey, treat as historical) [R111]: about 45% of respondents used the **same horizon for all products**, of whom 50% used 21–30 years, 12% used 31–40 and 23% used more than 40. By product, the most common horizon for individual traditional life (term and permanent, par or non-par) was 21–30 years (39%), with 28% beyond 40; individual **fixed deferred annuities** 21–30 years (41%) or 11–20 (32%); **payout annuities** more than 40 years (39%) or 21–30 (33%); **structured settlements** more than 40 years (73%); **ULSG** more than 40 years (46%); other UL 21+ years (85%), spread fairly evenly across 21–30, 31–40 and 40+. Of those using a materiality criterion for the horizon, 75% used a **90%** run-off level [R111].
- **Interaction of PBR reserves with VM-30** [R111]. **All in-force and assumed business is subject to asset adequacy testing under VM-30 regardless of the reserve method.** Two practices are described: treat the PBR reserve as satisfying "moderately adverse conditions" via the **Demonstration of Conservatism** method (sometimes with simplified or single-scenario confirmation), or **continue to include PBR business in full cash flow testing**, in which case any excess conservatism in the PBR reserve **becomes available as additional sufficiency in the aggregate** (and any insufficiency likewise flows through). Cautions the practice note raises: a reserve conservative at one valuation date may see **margins deteriorate later** under the same method and assumptions; **only some** of a company's reserves are PBR, which can constrain aggregation; and **federal income taxes are not included in VM-20 and VM-21 calculations but would be included in asset adequacy analysis** [R111]. Where VA results are included in aggregate company results, the **AG 43/VM-21 reserve must be determined first, since it is the initial reserve tested** [R111]. The 2012 survey split was **45%** treating AG 43 as meeting the adequacy requirement versus **55%** including the business in CFT [R111]. The same two-track logic is applied to **AG 38 §8C** (formulaic reserve subjected to a stand-alone AAT) and **AG 38 §8D** (principle-based reserve, potentially Demonstration of Conservatism) [R111], with the important asymmetry that **an AG 38 8C insufficiency cannot be ignored by declining to aggregate** — the additional reserve becomes part of the initial reserve tested [R111].
- **IMR in projections** [R111]: unlike bonds and unlike CRVM/PBR reserves, **the IMR has no cash flows**; a positive IMR increases assets available in CFT and improves results, while an admitted negative IMR worsens them. **INT 23-01** governed admitted net negative IMR for year-ends 2023–2025 and was **automatically nullified on January 1, 2026**; **APF 2023-08** put the non-admitted-IMR handling into VM-20 and VM-30, and NAIC staff guidance said companies **are not required** to allocate any non-admitted portion of IMR (or PIMR) for VM-20/VM-21/VM-30 purposes, but **any admitted negative IMR should be allocated** [R111]. A model must therefore treat IMR/PIMR as an **allocated non-cash-flow adjustment to starting assets**, sign-aware. **Caution:** the practice note's statement that the interim solution "is set to expire after 2025 with the expectation that a final solution will be adopted by then" was written in September 2024; **what replaced it as of the 2026 statutory year was not verified in this research** [R111] — see Gaps.

---

## Model hooks

| Accounting / capital item | What the liability cash flow model must produce | Granularity / basis / timing |
|---|---|---|
| **CRVM formulaic reserve (SVL §5; VM-A A-820/A-830)** [R1][R110] | Modified net premium reserve: PV(future guaranteed benefits) − PV(modified net premiums), with the 19-pay-whole-life-at-age-x+1 expense allowance cap and the §5.B 15%-of-excess-first-year-premium test | **Seriatim**, per policy; contractual guarantees only; prescribed mortality and calendar-year-of-issue valuation interest; valuation date |
| **CARVM formulaic reserve (SVL §5a)** [R1] | For each contract year end, PV(future guaranteed benefits including guaranteed nonforfeiture benefits) at that year end minus PV(future valuation considerations payable before that year end); take the **greatest** excess | **Seriatim**; one benefit stream per elective-benefit path; contract-specified mortality/interest for guaranteed benefits; valuation date |
| **Maximum valuation interest rate (SVL §4b; VM-20 §3.C.2)** [R1][R3] | Not a model output — a **model input** that must be parameterised: weighting factor by guarantee duration and plan type, reference rate from a configurable Moody's-composite series with 12/36-month averaging to June 30, ±0.5% stability rule, quarter-percent rounding with direction depending on which NPR method applies | **By calendar year of issue** (or year of change in fund); per product and guarantee duration; annual refresh |
| **Income annuity maximum valuation rate (VM-V §1)** [R37] | Bucket assignment logic (reference period × initial age), jumbo/non-jumbo classification, premium determination date derivation per contract type | **Per contract / per certificate**; daily rate table for jumbo, quarterly for non-jumbo; premium determination date |
| **VM-20 net premium reserve** [R3] | Seriatim NPR by reserving category: §3.B.4 term method, §3.B.5 ULSG method driven by FFSG/ASG/LSG, or **VM-A/VM-C basic reserve** for All Other and un-modelled IUL; prescribed lapse and shock-lapse tables; COI-to-next-date and CSV floors; less §8 reinsurance credit | **Seriatim**, then summed by reserving category; prescribed assumptions only; valuation date |
| **VM-20 deterministic reserve** [R3] | Either a gross premium valuation (APV benefits + expenses − APV premiums − PIMR + SA assets + policy loans) or a **direct iteration** starting-asset solve, both under **economic scenario 12**, discounted on the model segment's NAER path, **excluding federal income tax**, including net reinsurance and derivative-liability cash flows | **Group of policies within a model segment**, then split by reserving category; prudent estimate assumptions; valuation date, or up to **3 months earlier** with roll-forward |
| **VM-20 stochastic reserve** [R3] | Per scenario: discounted negative projected statement value of GA + SA assets at model start and each projection year-end, summed across model segments, maximised, added to starting assets → scenario reserve; then **CTE 70** across scenarios, plus any additional amount for unmodelled material risks, less PIMR | **Aggregation subgroups consistent with actual risk management**; also stand-alone per reserving category; valuation date (or up to 3 months earlier) |
| **Stochastic Exclusion Ratio Test** [R3] | Sixteen adjusted DRs — either scenario-specific §4.A DRs or **gross premium reserves out of the AAT/CFT model** — plus the baseline PV of benefits net of ceded benefits; ratio `(b − a)/c` against 6%; optionally the YRT gross/net LPIR comparison | **Group of policies with homogeneous risk profile**; annually, within 12 months before the valuation date |
| **Stochastic Exclusion Demonstration Test** [R3] | `max(DR, NPR − due-and-deferred-premium-asset)` versus stand-alone SR, versus adverse deterministic scenario reserves, or versus a representative-sample SR; plus a residual-risk-after-mitigation evaluation | Group level; **first year and at least every third calendar year**; documented in the VM-31 report |
| **Deterministic Exclusion Test** [R3] | Σ future valuation net premiums versus Σ guaranteed gross premiums, with **0% lapse**, initial-premium-period-only comparison for shock-lapse designs, and an anticipated-experience-mortality-plus-margin override where it exceeds prescribed CSO | Group level, **direct or assumed basis**; annually, or every 5 years for closed blocks with 3 consecutive passes; **never for term** |
| **VM-30 asset-adequacy-tested amounts table** [R100] | Reserve totals split into **Formula / Principle-Based / Additional / Other** columns, per annual statement exhibit line, with an **analysis method symbol per line** and an extra line where a line uses more than one method; plus allocated IMR and AVR amounts | **By annual statement exhibit line** (Exhibits 5, 6, 7, 8 Pt 1, separate accounts); every line printed even when zero; **December 31 valuation date** |
| **Additional reserve from asset adequacy analysis** [R100][R29][R1] | The amount by which assets must be increased so the block is adequate under **moderately adverse conditions**; and, in the RAAIS, the additional reserve at the valuation date that would eliminate negative **aggregate** ending surplus | Company aggregate for the opinion; **by block for the RAAIS scenario discussion**; established as a statutory liability under SVL §6.B |
| **Cash flow testing engine** [R29][R100][R111] | Projection of asset and liability cash flows under multiple scenarios; **present value of ending surplus**; a terminal-value routine or a horizon long enough that the remaining in-force is immaterial; interim surplus by year | **By product line / business unit / model segment**, aggregated per ASOP 22 §3.1.4; assets initialised at **no more than the statement value of the reserves tested**; annually at December 31 |
| **Equity return volatility in CFT (VM-30 §3.B.7)** [R100] | One of: stochastic equity returns with risk metrics; up/down/volatile equity paths **crossed with each interest rate path**; explicit market-drop scenarios; or a **level return set to a tail metric such as CTE70** — plus a qualitative moderately-adverse justification | Per block with material equity-like exposure; each valuation |
| **AG 53 sensitivity tests** [R105][R106] | Two separate reruns: (a) non-equity-like **reinvestment** spreads capped at the WAL benchmark (170/175/185 bps) against a **level Treasury** baseline; (b) equity-like **initial and reinvestment** assets at **4% for 10 years then 5%** | Asset grouping at least as granular as the AAT model's compression; **company level scope test**; filed by April 1 |
| **AG 53 attribution analysis** [R105] | Guideline Excess Spread by asset type, decomposed into credit, illiquidity, current-versus-long-term-spread deviation, and volatility/other | By asset type, separately for **initial and reinvestment** assets; annually |
| **AG 53 asset reporting** [R106] | **Projected portfolio allocations at years 5, 10, 20 and 30 under the NY1 level scenario**; modelled allocation limits by asset class; structured-asset detail by capital-structure position and rating; PIK and liquidity commentary | Per asset class per the reporting templates; annually |
| **AG 55 mandatory CFT run** [R103] | A cash flow test of the ceded block with **Starting Asset Amount = Post-reinsurance Reserve**, on the assuming company's balance-sheet basis (book or market), producing **PV of ending surplus for a level scenario and the New York 7**, sensitivity results, and interim negative surplus by year | **Per counterparty**; from **YE2026 also per significant product line and separately PBR vs non-PBR**; due April 1 |
| **AG 55 pre-reinsurance PBR reserve (§6.G)** [R103] | The VM-20 / VM-21 / VM-22 reserve for the ceded block **as if the treaty did not exist** — i.e. the PBR engine must run **gross of a specific treaty** | Ceded block; same valuation date; may substitute for the CFT run |
| **AG 55 attribution analysis** [R103] | A stepwise bridge from **Pre-reinsurance Reserve** to **Post-reinsurance Reserve**, split by policyholder behaviour, mortality/longevity, investment return versus statutory discount rate, taxes, **removal of the CSV floor**, market-versus-book interest effects, and moderately-adverse-to-best-estimate conversion | Per treaty (or per counterparty where aggregated); annually |
| **VM-31 evidence pack** [R108] | Assumption tables (anticipated / margin / prudent estimate) **in Excel**; experience study metadata per risk factor; modelling system name, version and customisation; grouping/compression rationale with a seriatim-audit commitment; **static and dynamic validation tables**; projection-period support; DR method per model segment; pre- and post-reinsurance reserve, count, face amount and account value for current and prior year | Per sub-report per group of policies; **Summaries filed April 1**, full report on request |
| **VM-G governance** [R109] | Evidence that the model can compute components currently omitted — an exclusion-test-only company must report **readiness to calculate the DR and/or SR**; qualified actuary certification that non-prescribed, non-stochastic assumptions are **prudent estimates with appropriate margins** | Per group of policies; annual board reporting; **seven-year** documentation retention |
| **Tax reserve (IRC §807)** [R16] | max(net surrender value, 92.81% × NAIC-method reserve), capped at statutory | Seriatim; same valuation date; from the same statutory engine |

---

## Product applicability

`x` = the item directly binds the product; `(x)` = binds conditionally or peripherally;
blank = not indicated by the sources read.

### Life products

| Item | term | whole-life | universal-life | indexed-ul | variable-ul | guaranteed-ul |
|---|---|---|---|---|---|---|
| VM-30 opinion + AAT (R100) | x | x | x | x | x | x |
| Model #822 / state AOMR (R101, R102) | x | x | x | x | x | x |
| NY Reg 126 §95.10 — NY 7 (R112) | x | x | x | x | x | x |
| ASOP 22 (R29) / ASOP 57 (R113) | x | x | x | x | x | x |
| AG 53 (R105, R106) | (x) | (x) | (x) | (x) | (x) | (x) |
| AG 55 (R103, R104) | (x) | (x) | (x) | (x) | (x) | (x) |
| VM-31 PBR Actuarial Report (R108) | x | x | x | x | x | x |
| VM-G governance (R109) | x | x | x | x | x | x |
| VM-A formulaic index (R110) | (x) | x | x | x | x | (x) |
| CRVM (SVL §5) | x | x | x | x | x | x |
| CARVM (SVL §5a) | | | | | | |
| VM-20 NPR | x | x | x | x | x | x |
| VM-20 DR | x | x | x | x | x | x |
| VM-20 SR | x | (x) | (x) | x | x | x |
| SET (R3 §6.A) | x | x | x | x | x | x |
| DET (R3 §6.B) | **n/a** | x | x | x | x | (x) |
| VM-V §1 income annuity rates (R37) | | | | | | |

Notes on the life matrix. **Term is barred from the DET entirely** — "[t]he DET may not be
used for term insurance policies, or term riders … and these policies may not be excluded
from the DR requirements" [R3]. **ULSG is deemed to fail the DET** unless its secondary
guarantee is a "non-material secondary guarantee" [R3]. **Variable life and ULSG may not use
the SET Certification Method** [R3]. Whole life, ordinary UL and VUL sit in the **All Other**
reserving category, so their NPR is the **VM-A/VM-C formulaic basic reserve** [R3][R110] —
which is why the CRVM row is marked for them; IUL takes the same route where no DR or SR is
computed [R3]. VM-31 and VM-G bind every life product because a company that computes an
exclusion test at all must file a sub-report [R108] and Section 4 of VM-G always applies
[R109]. AG 53 and AG 55 are marked `(x)` throughout because their triggers are
**company-level and treaty-level, not product-level** — a small term writer is out of AG 53
scope, and a large ULSG block ceded to an offshore affiliate is squarely in AG 55 scope.

### Annuity products

| Item | fixed-deferred | fixed-indexed | variable | RILA | immediate | deferred-income |
|---|---|---|---|---|---|---|
| VM-30 opinion + AAT (R100) | x | x | x | x | x | x |
| Model #822 / state AOMR (R101, R102) | x | x | x | x | x | x |
| NY Reg 126 §95.10 — NY 7 (R112) | x | x | x | x | x | x |
| ASOP 22 (R29) / ASOP 57 (R113) | x | x | x | x | x | x |
| AG 53 (R105, R106) | x | x | (x) | (x) | x | x |
| AG 55 (R103, R104) | x | x | (x) | (x) | x | x |
| VM-31 PBR Actuarial Report (R108) | x | x | x | x | x | x |
| VM-G governance (R109) | x | x | x | x | x | x |
| VM-A formulaic index (R110) | x | x | x | x | x | x |
| CRVM (SVL §5) | | | | | (x) | (x) |
| CARVM (SVL §5a) | x | x | x | x | x | x |
| VM-20 NPR / DR / SR | | | | | | |
| SET / DET (VM-20 §6) | | | | | | |
| VM-V §1 income annuity rates (R37) | (x) | (x) | (x) | | x | x |

Notes on the annuity matrix. The **VM-20** rows are blank for annuities by construction —
VM-20 is CRVM for individual **life** [R3]; the annuity analogues are VM-21 (R35) and VM-22
(R36), whose own exclusion tests and Single Scenario Test are outside this stream's block but
are named alongside VM-20 in **VM-G §1.A** and **VM-31 §2.A** [R109][R108], which is why those
two rows are marked for annuities. **CARVM** is marked for variable annuities and RILAs
because VM-21 *constitutes* CARVM for contracts in its scope [R35] and AG 43 does the same for
pre-2017 business [R38]; the mark records the legal method, not a formulaic calculation.
**VM-V §1** marks the deferred and variable products at `(x)` because its scope reaches fixed
payout streams arising from **settlement options, annuitizations of host contracts, contingent
deferred annuities and guaranteed living benefits once contract funds are exhausted** [R37].
**AG 53 and AG 55 are marked `x` for the general-account annuity products** because the
guidelines' own text names their target: AG 53 was prompted by complex-asset activity "in
support of general account annuity blocks" [R105], and AG 55 targets "asset-intensive"
coinsurance measured against **Exhibit 5 gross annuity reserves plus Exhibit 7 reserves**
[R103]. Variable and RILA business is `(x)` — separate account assets are outside AG 53's
scope where unitized [R105], but the general account guarantees and the fixed account are not.
**Immediate and deferred income annuities carry a `(x)` for CRVM** because VM-V §1 states its
rates are the maximum interest assumption "to be used in the CARVM and for some contracts,
CRVM" [R37] — the CRVM route exists for certain in-scope certificates and contract features.

---

## Gaps and caveats

**Things that could not be verified and must not be presented as sourced**

1. **AG 55's Executive (EX) Committee and Plenary adoption date.** LATF (**June 5, 2025**) and
   Life Insurance and Annuities (A) Committee (**July 14, 2025**) are printed on the guideline
   [R103], and the Reinsurance (E) Task Force minutes record that EX/Plenary adoption "was
   expected … at the Summer National Meeting" [R104]. The commonly reported date of
   **August 13, 2025** appears only in law-firm and consultant summaries and is
   **[unverified]** here. The *effective* date — reserves reported in the **December 31, 2025**
   annual statement — is printed in the guideline and is verified [R103].
2. **The AP&P Manual is a paid publication** [R33]. AG 51, AG 53 and AG 55 officially live in
   its **Appendix C**, and the Appendix A items that VM-A indexes — above all **A-820**
   (minimum life and annuity reserve standards) and **A-830** (valuation of life insurance
   policies) — live in its **Appendix A** [R110]. AG 53's text was retrieved from a free NAIC
   inline file and AG 55 from the pending-action print, so both are first-hand here; **A-820
   and A-830 as printed in the manual were not retrieved**, and the formulaic CRVM detail this
   stream reports therefore comes from the **Standard Valuation Law itself** [R1] plus Model
   #830 (R6), not from the manual.
3. **The NAIC Annual Statement Blank (Life/Fraternal) was not retrieved.** A fetch of the NAIC
   publication page `https://content.naic.org/sites/default/files/publication-asb-life.pdf`
   returned unreadable compressed streams to the fetch tool and was not re-attempted with
   local extraction. Consequently the exact layout of the **statement of actuarial opinion
   page**, of **Exhibits 5/6/7/8**, of **Schedule S**, and of the **VM-20 Reserves Supplement
   Parts 1A/1B/2** is known here only through the documents that reference them — VM-30's
   tested-amounts table [R100], VM-31 §§3.C.8–3.C.10 [R108], and AG 55 §9.B.i(a) [R103]. A web
   search indicated the VM-20 Reserves Supplement is listed as **Supp456** in the 2025 blank
   and reports NPR and, as applicable, DR and SR for business issued on or after **January 1,
   2017**, with Part 1B detailing Part 1A — that is a **search summary, [unverified]**.
4. **AG 33 and AG 35 remain unread** (already flagged at R39/R40). Formulaic CARVM for fixed
   and indexed deferred annuities therefore rests on the SVL §5a text [R1] plus two guidelines
   whose mechanics this library cannot quote.
5. **AG 51 (long-term care AAT)** is made applicable for VM-30 purposes [R100] and is reviewed
   by VAWG [R107], but its text was not retrieved and long-term care is outside this library's
   twelve products.
6. **The IMR end-state after 2025 was not verified.** The Academy note (written September 2024)
   states **INT 23-01** governed admitted net negative IMR for year-ends 2023–2025 and is
   "automatically nullified on January 1, 2026," with a long-term solution expected [R111].
   **What the permanent statutory guidance is for the 2026 statutory year was not researched**
   and is a live gap for any model that allocates IMR into asset adequacy analysis. Note this
   matters directly: VM-30 §3.B.5 requires an IMR allocation, sign-aware, in **any** asset
   adequacy analysis [R100].
7. **VM-21 and VM-22 exclusion/Single-Scenario-Test mechanics** are referenced here only
   through VM-G §1.A and VM-31 §2.A [R109][R108]; their substance belongs to R35/R36 and was
   not re-derived.
8. **ASOP 57's PDF was not fetched** — only the ASB standard page, which gave title, Doc. No.
   208, adoption January 2023 and effective June 15, 2023 [R113]. Its section-level content is
   therefore not quoted.
9. **The AG 53 and AG 55 reporting templates** are referenced by both guidelines as living
   under the Documents tab of the LATF web page [R103][R105]; the templates themselves were
   not retrieved, and AG 55's §9.C template list is printed in the adopted text with the
   placeholder "{To be discussed following the adoption of the base Guideline}" [R103] — so the
   **final AG 55 template set may differ from the ten worksheet names listed there**.
10. **Quantitative practice figures from the Academy practice note are dated.** Every
    percentage reproduced above (analysis method mix, projection horizons, discount-rate
    methods) comes from **2004 and 2012 surveys** of appointed actuaries, and the note itself
    cautions the reader on their current applicability [R111]. They are indicative of practice
    shape, not calibration targets.

**Verified findings that correct assumptions a reader may bring**

1. **The "New York 7" is not an NAIC requirement.** It is **New York Regulation 126
   §95.10(d)** [R112], New York's adoption of Model #822 [R102]. Nationally it appears only as
   an *example* in a VM-20 §6 guidance note [R3] and as a *recommended* scenario set in
   AG 55 §6.D and Appendix 1 [R103]. **VM-30 prescribes no interest scenarios at all** [R100].
2. **VM-30 grants no exemption from the opinion or from asset adequacy analysis.** The word
   "exempt" does not occur in VM-30 [R100]; exemptions live in state law, which is why
   ASOP 57 (successor to ACG No. 4) still exists [R113][R29].
3. **Model #822 is not repealed.** It is the pre-Valuation-Manual instrument, still tracked by
   the NAIC (Fall 2024 state page) [R102], still the basis of many state regulations, and
   expressly recognised by VM-30 for appointed-actuary appointment continuity [R100][R101].
4. **AG 55 is adopted, effective for year-end 2025, and its first filings are due April 1,
   2026** [R103] — this is not a proposal.
5. **AG 55 is disclosure-led, not reserve-led.** It "does not include prescriptive guidance as
   to whether additional reserves should or should not be held" [R103], a point regulators
   made explicitly on the record [R104].
6. **The VM-20 exclusion tests are not merely a way to avoid work — how you pass one changes
   your governance obligations.** Passing via the DR-based SERT method, the VM-22 adjusted
   scenario reserve method, or the Stochastic Exclusion Demonstration Test **re-imposes VM-G
   Sections 2 and 3** on a company that would otherwise be exempt from them [R109].
7. **A company that computes no DR or SR still files a VM-31 sub-report** [R108] and its
   qualified actuary must still report **readiness to compute the DR and/or SR** [R109]. There
   is no such thing as a VM-20 company with no PBR documentation obligation.
8. **The Valuation Manual explicitly permits the VM-20 exclusion-test reserve to be built from
   the company's asset adequacy analysis models** [R3]. One cash flow engine, correctly
   parameterised, can serve VM-30 cash flow testing, the VM-20 SERT, the VM-20 DR (via direct
   iteration), and — per AG 55 §6.G — the pre-reinsurance PBR reserve of a ceded block
   [R3][R103].
9. **AG 53's scope test is company-level, on gross reserves.** It does not care what products
   you write; it cares that you have more than **$5 billion** of general account actuarial
   reserves plus non-unitized separate account assets, or more than **$100 million** with more
   than **5%** of supporting assets in Projected High Net Yield Assets — reserves measured
   **before any ceded reinsurance credit** [R105].
