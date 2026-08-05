# Risk-Based Capital and Capital Adequacy — research notes (U.S. statutory accounting and capital)

**Stream:** Risk-Based Capital and Capital Adequacy
**Access date for every citation below:** 2026-08-04
**Status:** research notes, not yet merged into the frozen reference page.

---

## Scope and numbering note

This file is working research for the U.S. statutory accounting and capital section. New
reference entries created here are numbered **R125–R149 only** — that block is assigned to
this stream. Entries actually used run **R125–R142**; **R143–R149 are deliberately left
unused** and must not be claimed by anyone else.

Entries **R1–R72** live in
`C:/Users/fumito/OneDrive/pyproj/lifelib-products/us/references/regulatory-and-actuarial-references.md`
and are **frozen** — product documentation already cites them. Nothing in this file
renumbers, restates or duplicates them. Where an existing entry already covers part of this
topic it is listed in the next section with a one-line note and cited by its existing
number.

**Citation discipline.** Every factual statement carries `[R#]` pointing at a document that
was actually retrieved and read. Statements from general knowledge, or inferences I drew by
comparing two documents, are tagged `[unverified]`. Fetch failures are recorded.

**Retrieval note.** Most NAIC PDFs return raw compressed streams to the fetch tool; they
were downloaded and text-extracted locally before reading. Entries so retrieved are marked
*fetched: yes (local text extraction)* and their annotations are first-hand. PDF text
extraction drops superscripts, so squared terms in formulas were cross-checked against a
second occurrence in the same document where the exponent survived (see § "The covariance
adjustment" below).

**Paid-publication caveat, stated plainly.** The **NAIC Life and Fraternal Risk-Based
Capital Forecasting and Instructions** is a *sold* NAIC publication, distributed annually
around Nov. 1 from `content.naic.org/publications` and marked "Not for Distribution" on
every page [R139]. It is not published free by the NAIC. The 2024 and 2023 editions were
read from copies **posted publicly by the Indiana Department of Insurance** (R128, R129) —
a state insurance department site, which this library accepts for adopted regulatory text.
Facts below cited to `[R128]`/`[R129]` are first-hand from those copies. The **RBC
forecasting spreadsheet** itself was not obtained and is not cited. The **NAIC Accounting
Practices and Procedures Manual** remains a paid publication (already recorded at R33).

---

## Existing entries (R1–R72) that bear on this stream

| R# | Short title | How it bears on RBC and capital adequacy |
|----|-------------|------------------------------------------|
| R1 | Standard Valuation Law (Model #820) | Fixes the statutory reserve that RBC is measured *against*: C-3 factor charges apply to annual-statement reserves, and the C-3 Phase II charge is an excess over the statutory reserve. |
| R3 | Valuation Manual, 2026 edition | Supplies the reserve definitions (VM-20/VM-21/VM-22) whose outputs feed the RBC reserve bases, and VM-31, whose documentation the C-3 Phase II actuarial memorandum explicitly follows. |
| R29 | ASOP 22 (asset adequacy opinions) | An **unqualified** asset-adequacy opinion is the condition for the one-third reduction in every factor-based C-3 charge; the C-3 Phase I cash flow model *is* the asset-adequacy model with different scenarios. |
| R31 | ASOP 52 (PBR for life) | Governs the VM-20 work whose reserves sit under the C-3 factor charges for life reserves. |
| R32 | ASOP 56 (modeling) | Named as a governing standard for grouping, sampling, scenario count and simplification in the C-3 Phase II calculation. |
| R33 | NAIC AP&P Manual | The statutory accounting basis producing capital and surplus, the AVR, and the Exhibit 5 / Notes-Item-32 reserve splits that the RBC pages read from. Paid publication. |
| R34 | FASB ASU 2018-12 (LDTI) | Not an RBC input; relevant only because the same projection engine serves GAAP, and because deferred tax assets carry an explicit RBC charge outside covariance. |
| R35 | VM-21 (variable annuity PBR) | The *same* stochastic projection produces both the VM-21 aggregate reserve (CTE70 + additional standard projection amount) and the C-3 Phase II capital charge (CTE98 + ASPA − reserve). VM-21 itself states the reserve and RBC requirements are identical except for tax treatment. |
| R36 | VM-22 (non-variable annuity PBR) | Supplies the reserve for fixed/indexed/payout annuities that the factor-based C-3 charges are applied to, and is the reserve basis being aligned with under the C-3 alignment project. |
| R37 | VM-V § 1 (income annuity valuation rates) | Formulaic reserve basis for income annuities, i.e. the exposure base for the new C-2 longevity charge. |
| R38 | AG 43 (CARVM for variable annuities) | C-3 Phase II applies to "all policies and contracts that have been valued following the requirements of AG-43 or VM-21" — AG 43 defines part of that population. |
| R39/R40 | AG 33 / AG 35 | Formulaic CARVM for deferred and equity-indexed annuities; produces the book-value annuity reserves the C-3 risk categories bucket by withdrawal provision. |
| R41 | VM-C actuarial guideline index | Locates AG 48, AG 33, AG 35, AG 43 within the Valuation Manual appendix structure. |
| R11/R12 | AG 48 / Model #787 | The AG 48 Primary Security shortfall enters the RBC formula **directly and dollar-for-dollar**: shortfall × 2, added after covariance, then × 50% to reach Authorized Control Level. |
| R47 | C-3 RBC Instructions package incl. Academy 2005 VA report | The historical (pre-reform) C-3 Phase II mechanics: CTE 90 Total Asset Requirement, RBC = TAR − statutory reserve, Standard Scenario floor, tax adjustment, 35% tax rate. **Superseded in its parameters** by the post-2020 instructions read here (R128) — see § "C-3 Phase II" for the deltas. |
| R48 | Oliver Wyman QIS II (VA reform) | The analytical record behind the 2018–2020 reform that replaced CTE 90/TAR with the CTE-High-minus-reserve construction; QIS II recommended "CTE 95 with a 25% scalar", and the adopted instructions land on **CTE 98 with a 25% scalar** (R128) — the scalar survived, the CTE level did not. |
| R70 | ASOP 54 (pricing) | Cited by the NAIC C-2 instruction supplement as relevant practice guidance for assessing "pricing flexibility". |
| R26 / R28 | ASOP 2 (NGEs) / ASOP 15 (dividends) | Also cited by the C-2 instruction supplement for assessing whether in-force rates can materially be adjusted. |

---

## New entries

### Group A — the model law and the regulatory action levels

#### R125. Risk-Based Capital (RBC) for Insurers Model Act (Model #312)
- **Publisher:** National Association of Insurance Commissioners
- **URL:** https://content.naic.org/sites/default/files/model-law-312.pdf
- **Accessed:** 2026-08-04 · **Fetched:** yes (local text extraction; 14-page PDF; print header "NAIC Model Laws, Regulations, Guidelines and Other Resources—January 2012")
- **Annotation:** The enabling statute. Section 1 defines the four RBC Levels as fixed
  multiples of Authorized Control Level RBC, Total Adjusted Capital, negative trend, RBC
  Report and RBC Plan; Section 2 sets the March 1 filing date and enumerates the risk
  factors the life formula must reflect; Sections 3–6 define the four *Events* and the
  supervisory consequence of each; Section 7 the hearing right; Section 8 the
  confidentiality and no-advertising rules. **Model number verified against the print
  itself** (page footers read "MO-312-1" … "MO-312-14"), not assumed. Note that the model
  act does *not* contain the formula — it delegates entirely to the RBC Instructions
  (R128).

#### R126. Project History — 2011, Risk-Based Capital for Insurers Model Act (#312)
- **Publisher:** NAIC
- **URL:** https://content.naic.org/sites/default/files/model-laws-project-history-312.pdf
- **Accessed:** 2026-08-04 · **Fetched:** yes (local text extraction; 5 pages)
- **Annotation:** Two 2011 amendments documented: (a) adding fraternal benefit societies to
  the life sections, (b) **raising the life trend-test trigger from 2.5× to 3.0×
  Authorized Control Level RBC** to match the P/C and health trend tests. This is exactly
  the kind of multiplier that is easy to misremember — the change was requested by
  Pennsylvania in a March 27, 2007 letter, adopted by the Capital Adequacy (E) Task Force
  Sept. 14, 2011 and by the Financial Condition (E) Committee Sept. 19, 2011.

#### R127. NAIC Insurance Topics — Risk-Based Capital
- **Publisher:** NAIC
- **URL:** https://content.naic.org/insurance-topics/risk-based-capital
- **Accessed:** 2026-08-04 · **Fetched:** yes (web page)
- **Annotation:** Regulator-facing overview: **Model #312** adopted 1993 for life and P/C,
  latest revision 2012; **Model #315** the separate health RBC model act (1998, revised
  2011); three formulas (life/fraternal, P/C, health); the intervention ladder expressed as
  a ratio of Total Adjusted Capital to Authorized Control Level RBC (≥300% none;
  200–300% trend test; <200% graduated intervention; <70% mandatory control). States the
  Capital Adequacy (E) Task Force and its working groups own the formulas and review them
  annually.

### Group B — the operative RBC instructions (the mechanics)

#### R128. NAIC *Risk-Based Capital Forecasting and Instructions — 2024, Life / Fraternal*
- **Publisher:** NAIC (© 2019–2024 NAIC; instruction pages dated 10/14/2024). **Paid NAIC
  publication**; the copy read was posted publicly by the **Indiana Department of Insurance**.
- **URL:** https://www.in.gov/idoi/files/RBCL24-INpdf.pdf
- **Accessed:** 2026-08-04 · **Fetched:** yes (local text extraction; 225 pages; overview,
  LR002, LR025, LR025-A, LR027, LR029, LR030, LR031, LR033, LR034, LR035, LR049, Appendix 1,
  Appendix 1a and the corresponding blank pages read)
- **Annotation:** **The single most load-bearing document for this stream.** It carries the
  operative definitions of every C-risk, the exact covariance formula, the C-1o bond factors
  by all 20 NAIC designation categories, the bond size factor, the current C-2 mortality
  structure keyed to *pricing flexibility*, the C-2 longevity page LR025-A with its guardrail
  and correlation factors, the full C-3 risk-category factor table with the asset-adequacy
  one-third reduction, the C-3 Phase I cash flow testing methodology (Appendix 1/1a) and its
  exemption test (LR049), the post-reform C-3 Phase II seven-step CTE 98 calculation, the
  operational-risk add-on, the AG 48 shortfall add-on, and the Total Adjusted Capital and
  Level-of-Action pages. Every quantitative fact in § "Extracted mechanics" below that is not
  otherwise attributed comes from here.

#### R129. NAIC *Risk-Based Capital Forecasting and Instructions — 2023, Life / Fraternal*
- **Publisher:** NAIC (paid publication; copy posted by the Indiana Department of Insurance)
- **URL:** https://www.in.gov/idoi/files/indrbclf23.pdf
- **Accessed:** 2026-08-04 · **Fetched:** yes (local text extraction; 225 pages; used for
  targeted comparison only)
- **Annotation:** Used solely to date the current structures. The pricing-flexibility C-2
  structure, the LR025-A longevity page, the guardrail/correlation-factor construction and
  the covariance formula are **all already present in the 2023 edition** with the same
  numbers, so those changes were in force no later than year-end 2023 [R129 vs R128]. The
  first year each took effect was **not** established from these two editions alone.
- **Fetch failure recorded:** the 2025 edition at
  `https://www.in.gov/idoi/files/RBCL25-INpdf.pdf` returned a truncated PDF stream and could
  **not** be parsed; no 2025 content is asserted anywhere in this file.

#### R142. NAIC Capital Adequacy (E) Task Force — RBC Proposal Form, Agenda Item 2025-01-L (C-2 Mortality Risk / LR025 annual statement sources)
- **Publisher:** NAIC (proposal dated 02/21/2024, submitted on behalf of the Life RBC (E)
  Working Group, Philip Barlow chair)
- **URL:** https://content.naic.org/sites/default/files/inline-files/2025-01-L%20C-2%20Mortality%20Risk%20(1).pdf
- **Accessed:** 2026-08-04 · **Fetched:** yes (local text extraction; 3 pages)
- **Annotation:** Valuable to an implementer out of proportion to its length: it prints the
  **annual-statement derivation of net amount at risk** that the RBC blank now pulls
  automatically, replacing free-form "Company Records". Also shows the NAIC's own
  change-control artefact (the RBC Proposal Form) and the routing among Blanks (E) Working
  Group, the sponsoring working group, and the Task Force. Adopted by the Task Force at its
  May 15 [2025] meeting [R139].

#### R139. NAIC *Life and Fraternal Risk-Based Capital Newsletter*, Volume 31 (September 2025)
- **Publisher:** NAIC
- **URL:** https://content.naic.org/sites/default/files/inline-files/2025_RBC%20Newsletter_Life%20and%20Fraternal.pdf
- **Accessed:** 2026-08-04 · **Fetched:** yes (local text extraction; 3 pages)
- **Annotation:** The free, public change log for the paid instructions. Lists the proposals
  adopted for the year-end 2025 filing and states the filing mechanics (submit LR001–LR049
  hard copy to any state that requests it; actuarial certifications form part of the
  electronic filing as PDFs; the forecasting spreadsheet cannot be used to file). Confirms
  the Forecasting and Instructions is published around Nov. 1 annually from
  `content.naic.org/publications`.

### Group C — C-1 asset risk and the 20-designation bond structure

#### R130. Moody's Analytics, *Revisions to the RBC C1 Bond Factors* (April/May 2021)
- **Publisher:** Moody's Analytics, commissioned by the ACLI in conjunction with the NAIC;
  posted on content.naic.org
- **URL:** https://content.naic.org/sites/default/files/inline-files/2021%20Revisions%20to%20the%20RBC%20C1%20Bond%20Factors.pdf
- **Accessed:** 2026-08-04 · **Fetched:** yes (local text extraction; 66 pages; executive
  summary, Table 1 base factors, Table 2 portfolio adjustment factors, and the targeted-
  modification narrative read)
- **Annotation:** The study behind the C-1o bond factors now in force. Sets out the
  methodology: default-rate term structures fitted to life insurers' *holdings* rather than
  overall issuance; a correlation model replacing the Academy's "economic state model";
  loss-given-default distribution aligned to empirical patterns; **risk premium set at
  expected loss plus 0.5 standard deviation** of the default-loss distribution, to align
  with reserving standards aimed at moderately adverse conditions; 21% corporate tax rate.
  Table 1's "MA Base Factors" column reproduces exactly the factors that appear on LR002 in
  the adopted instructions from Aaa/1.A (0.158%) through Caa2/5.B (23.798%) [R130][R128].
  Also documents the Academy's competing March 2021 proposal and the current (pre-2021)
  six-category factors, which is useful for dating in-force model assumptions.

### Group D — C-2 insurance risk (mortality and longevity)

#### R131. American Academy of Actuaries, *Academy C-2 Mortality Work Group Recommendation* (presentation to the NAIC Life RBC (E) Working Group, November 9, 2021)
- **Publisher:** American Academy of Actuaries
- **URL:** https://www.actuary.org/wp-content/uploads/2021/11/NAIC_Life_RBC_C2_Recommendation_November_2021_Final.pdf
- **Accessed:** 2026-08-04 · **Fetched:** yes (local text extraction; 26 slides read in full)
- **Annotation:** The calibration record for the modern C-2 mortality charge and the clearest
  statement of *what the risk is*. Defines C-2 mortality as adverse variance in life
  insurance deaths over the remaining lifetime of a block, net of pricing flexibility;
  targets the **95th percentile** in excess of what statutory reserve mortality covers;
  decomposes into volatility, level, trend and catastrophe (pandemic + a new 9/11-type
  terrorism component + a new "unknown sustained risk" component replacing the original HIV
  scenarios); quantifies capital as the **greatest present value of accumulated deficiencies
  (GPVAD)** where loss = death benefits minus reserves released, discounted at 2.765%
  after-tax (3.5% pre-tax); expresses the answer as a factor per $1,000 of net amount at
  risk. Prints the **legacy (pre-restructure) factors** — Individual & Industrial
  2.23/1.46/1.17/0.87 and Group & Credit 1.75/1.16/0.87/0.78 per $1,000 across the old four
  size bands — which an in-force model of a pre-2023 valuation must use.

#### R132. American Academy of Actuaries C-2 Mortality Work Group, report to the NAIC Life RBC (E) Working Group (April 4, 2022)
- **Publisher:** American Academy of Actuaries (posted on content.naic.org)
- **URL:** https://content.naic.org/sites/default/files/inline-files/03_Academy_C2_Mortality_Risk_Work_Group_Report_to_LRBC_Apr2022_Final_0.pdf
- **Accessed:** 2026-08-04 · **Fetched:** yes (local text extraction; 12 pages)
- **Annotation:** Sensitivity analysis defending the November 2021 recommendation
  (zero-mortality-improvement test, catastrophe component sensitivities, support for the
  five-year risk exposure period for products with pricing flexibility) plus the Work
  Group's response to ACLI and regulator comments on tiered charges, definitions,
  annual-statement tie-out, non-participating whole life default category and group permanent
  life. Documents that experience mortality improvement was set to the **SOA 2017 mortality
  improvement scale** used with AG 38 and VM-20.

#### R133. NAIC, *Life RBC—C-2 Mortality Risk: Instruction Supplement for Applying the Newly Adopted Life Insurance C-2 Mortality Instructions* (December 19, 2022)
- **Publisher:** NAIC
- **URL:** https://content.naic.org/sites/default/files/inline-files/lrbc-C-2-mortality-risk-instruction-supplement-dec2022.pdf
- **Accessed:** 2026-08-04 · **Fetched:** yes (local text extraction; 14 pages)
- **Annotation:** The Q&A that makes the pricing-flexibility categorisation operable — and
  therefore the document that tells a model builder what data the C-2 page actually needs.
  Sets the **default categories when the assessment is not performed** (direct individual
  term → Term without Pricing Flexibility; direct individual permanent → Permanent without
  Pricing Flexibility; direct group → Over-36-months; non-affiliated *ceded* individual →
  With Pricing Flexibility; non-affiliated *ceded* group → 36-months-and-under; affiliated
  reinsurance follows the direct categorisation). Confirms size-tier allocation is done
  formulaically by the RBC software, so a model need only supply NAR in aggregate and by
  subcategory. Names ASOP 1, 2, 11, 15, 41 and 54 as relevant standards.

#### R134. NAIC memorandum, *Request for Comment on Longevity Risk Factors and Instructions* (Philip Barlow, chair Life RBC (E) Working Group; Rhonda Ahrens, chair Longevity Risk (E/A) Subgroup; April 30, 2021)
- **Publisher:** NAIC
- **URL:** https://content.naic.org/sites/default/files/inline-files/Longevity%20Risk%20Memo.pdf
- **Accessed:** 2026-08-04 · **Fetched:** yes (local text extraction; 2 pages)
- **Annotation:** The design record for the C-2 **longevity** charge and for the odd
  "guardrail factor / correlation factor" construction that now sits in the C-2 total. Two
  candidate factor sets: the Academy's, assuming reserve adequacy (1.35%/0.85%/0.75%/0.70%),
  and a higher set assuming lower reserves (**1.71%/1.08%/0.95%/0.89%** — the set actually in
  the instructions [R128]). Explains the covariance debate (Academy proposed −0.33; Subgroup
  rounded to −0.30 and offered −0.25 as conservative and consistent with other jurisdictions)
  and the guardrail, settable between 0 and 1, which at 1 guarantees no company's required
  capital falls on introduction of longevity and at 0 lets the pure covariance formula
  govern.

### Group E — C-3 interest rate and market risk

#### R135. *Phase I Report of the American Academy of Actuaries' C-3 Subgroup of the Life Risk Based Capital Task Force to the NAIC's Risk Based Capital Work Group* (October 1999, Atlanta)
- **Publisher:** American Academy of Actuaries
- **URL:** https://www.actuary.org/wp-content/uploads/2025/05/c3_oct99.pdf
- **Accessed:** 2026-08-04 · **Fetched:** yes (local text extraction; 43 pages; executive
  summary and Appendix I scenario-testing methodology read)
- **Annotation:** **The origin document for C-3 Phase I** and still the clearest statement of
  its logic. Recommends, effective 12/31/2000, replacing pure factors with a cash-flow-tested
  C-3 for annuities and single premium life, built on the asset-adequacy model but with
  interest scenarios designed to approximate the **95th percentile** C-3 risk. Prints the
  method Appendix 1a of the current instructions still reproduces almost verbatim: capture
  statutory surplus S(t) by scenario by year; the scenario's C-3 measure is the most negative
  of the present values S(t)·pv(t) discounted at **105% of the after-tax one-year Treasury
  rate** for that scenario; rank descending; take a weighted average over ranks 5–17 of the
  50-scenario set (or, for the 12-scenario set, the average of ranks 2 and 3 floored at half
  the worst). Notes the 12 and 50 scenario sets were *picked* from a randomly generated 200
  as those most likely to reproduce the full-200 answer. Records the original ±(half,
  double) collar — the current instructions retain only the **half** floor [R135 vs R128].
  Explicitly parks equity-indexed and variable products as out of Phase I scope, which is
  why C-3 Phase II exists at all.

#### R136. American Academy of Actuaries Life Risk-Based Capital Committee, *Recommendation on Changes to the Covariance Treatment of Common Stock* (December 2000, Boston)
- **Publisher:** American Academy of Actuaries
- **URL:** https://www.actuary.org/wp-content/uploads/2025/05/Recommendations%20on%20RBC%20formula%2012-01-2000.pdf
- **Accessed:** 2026-08-04 · **Fetched:** yes (local text extraction; 29 pages)
- **Annotation:** The document that created the **C-1cs / C-1o split** and the fifth squared
  term, recommended effective for 2001 filings: unaffiliated common stock (including that
  held in Schedule BA partnerships) and common and preferred stock of *non-insurance*
  affiliates move into C-1cs; everything else stays in C-1o; C-1cs enters the covariance as
  its own squared term because common stock risk was found independent of interest rate risk
  and of other asset risk. Also the source of the beta adjustment (30% base factor scaled by
  portfolio beta, floor 22.5%, cap 45%, non-publicly-traded deemed beta 1) and of the
  common-stock concentration add-on (largest five holdings uplifted 50%). **Caution for
  transcription:** the PDF's formula line extracts as garbled glyphs; do not quote it. The
  *current* published form of the formula is quoted from R128 instead.

#### R137. American Academy of Actuaries Life Investment and Capital Adequacy Committee, *Correlation in Life Risk Based Capital* (presentation to the NAIC Life RBC (E) Working Group)
- **Publisher:** American Academy of Actuaries (© 2025 on the actuary.org re-post; the file
  name carries "4-24", i.e. an April 2024 presentation date [unverified])
- **URL:** https://actuary.org/wp-content/uploads/2025/05/Life-Presentation-LRBC-Correlation-4-24.pdf
  (a copy is also on content.naic.org at
  `https://content.naic.org/sites/default/files/call_materials/Life-Presentation-CorrelationLRBC.pdf`,
  **not fetched**)
- **Accessed:** 2026-08-04 · **Fetched:** yes (local text extraction; 25 slides)
- **Annotation:** A **proposal**, not adopted law, and important to label as such: it would
  replace the square-root covariance expression with an explicit correlation matrix over five
  major categories (Credit = C-1o + C-3b; Equity = C-1cs + C-3c; Interest Rate = C-3a;
  Insurance = C-2a mortality + C-2b longevity; Business = C-4a + C-4b), with recommended
  correlations Credit–Equity 50%, Credit–Interest Rate 25%, Equity–Interest Rate 50%, and
  0% between Insurance/Business and everything else; nested within categories, C-1o–C-3b 25%,
  C-1cs–C-3c 100%, mortality–longevity −25%, C-4a–C-4b 0%. Calibrated to average annual
  correlations over 1982–2019 using proxy data (issuer-weighted corporate bond default rates,
  NCREIF, S&P 500 total return, FBNDX bond-fund total return, U.S. population mortality by
  socioeconomic decile, guaranty-association assessments 1988–2021). It would also move C-4a
  *inside* the matrix, where today it sits outside. The 2024 instructions still carry the
  classic square-root form [R128], so **as of the 2024 filing this is not in force**.

#### R138. American Academy of Actuaries, *C-3 Alignment, Part III* (presentation to the NAIC Life RBC (E) Working Group, September 11, 2025)
- **Publisher:** American Academy of Actuaries
- **URL:** https://actuary.org/wp-content/uploads/2025/09/Life-Presentation-C3AlignmentUpdate.pdf
- **Accessed:** 2026-08-04 · **Fetched:** yes (local text extraction; 65 slides, including
  appended Part II from May 1, 2025)
- **Annotation:** The forward-looking design of a unified C-3. Proposals as stated:
  **all** products currently in C-3 Phase 1 and C-3 Phase 2 move to one methodology, with
  **fixed indexed annuities brought into C-3 Phase 1 scope**; scenarios from the new
  Generator of Economic Scenarios (GOES); discounting on the C-3 Phase 2 basis (net asset
  earned rate or direct iteration); PBR models with prudent-estimate assumptions where
  available, otherwise cash-flow-testing models with moderately adverse assumptions; a
  generic scalar form **YY% × (CTE XX − reserves)** with YY and XX still open; the
  factor-based C-3 floor unchanged for now; a three-year phase-in from a year-end still to be
  determined; and a proposal to raise C-3 Phase 1 default-cost assumptions to **CTE 70** so
  that reserves and capital share one default assumption. Also states plainly why default
  costs are double counted today: C-1 factors were parameterised with a risk premium at
  expected loss plus ½ standard deviation, while PBR reserves cover CTE 70 and C-3 Phase 1
  covers only expected.

### Group F — governance and change control

#### R140. NAIC Capital Adequacy (E) Task Force
- **Publisher:** NAIC · **URL:** https://content.naic.org/cmte_e_capad.htm
- **Accessed:** 2026-08-04 · **Fetched:** yes (web page)
- **Annotation:** The body that owns all three RBC formulas. 2026 charges: monitor RBC
  application to emerging cross-line risks; review company submissions for adjustments to
  Total Adjusted Capital; evaluate historical data toward revising the asset-risk structure;
  continuously refine instructions, blanks and forecasting tools. Four working groups report
  to it: Health RBC, **Life RBC**, Property RBC, and RBC Investment Risk and Evaluation.
  Publishes RBC procedures, the RBC Proposal Form, and adopted proposals.

#### R141. NAIC Life Risk-Based Capital (E) Working Group
- **Publisher:** NAIC · **URL:** https://content.naic.org/committees/e/life-risk-based-capital-wg
- **Accessed:** 2026-08-04 · **Fetched:** yes (web page)
- **Annotation:** The group that actually sets life RBC. 2026 charges include evaluating
  refinements to formulas implemented the prior year and a hard change-control calendar —
  **structural blank changes adopted by May 15, non-structural by June 30**, which is why the
  instructions are dated in October and published around November 1 [R141][R139]. Three
  subgroups report to it: Generator of Economic Scenarios (GOES), **Longevity Risk**, and
  **Variable Annuities Capital and Reserve**. Resources listed include C-2 Mortality Risk
  guidance (updated 2023), C-3 Alignment Field Test Specifications (re-exposed July 30,
  2026), annual Life RBC newsletters, and aggregate life and fraternal RBC results.

---

## Extracted mechanics

### 1. The model act: definitions, report, action levels, trend test

**RBC Levels — the multipliers, verified against the statute [R125]:**

| Level | Definition in Model #312 § 1.K |
|-------|-------------------------------|
| Company Action Level RBC | **2.0 ×** Authorized Control Level RBC |
| Regulatory Action Level RBC | **1.5 ×** Authorized Control Level RBC |
| Authorized Control Level RBC | the number produced by the RBC formula per the RBC Instructions |
| Mandatory Control Level RBC | **0.70 ×** Authorized Control Level RBC |

**Total Adjusted Capital** is defined by the statute only as statutory capital and surplus
plus "such other items, if any, as the RBC instructions may provide" [R125] — i.e. the
statute delegates the AVR and dividend-liability add-backs entirely to the instructions
(§ 4 below).

**The RBC Report [R125]:** every domestic insurer files, on or before **March 1**, a report
of its RBC Levels as of the preceding calendar year end, in the form the RBC Instructions
require; also with the NAIC, and with any other state that requests it in writing (within
the later of 15 days from notice or the filing date). A life/health insurer's RBC "shall be
determined in accordance with the formula set forth in the RBC instructions", which "shall
take into account (and may adjust for the covariance between)" (1) asset risk, (2) risk of
adverse insurance experience, (3) interest rate risk, (4) all other business risks
[R125 § 2.B]. If the commissioner judges a filed report inaccurate, the corrected version is
an **Adjusted RBC Report** [R125 § 2.E].

**The four Events [R125]:**

| Event | Trigger on Total Adjusted Capital (TAC) | Consequence |
|-------|------------------------------------------|-------------|
| Company Action Level | Regulatory Action Level RBC ≤ TAC < Company Action Level RBC; **or**, for a life/health insurer or fraternal society, Company Action Level RBC ≤ TAC < **3.0 ×** Authorized Control Level RBC **and** a negative trend | Insurer files an **RBC Plan** within 45 days; commissioner responds within 60 days |
| Regulatory Action Level | Authorized Control Level RBC ≤ TAC < Regulatory Action Level RBC; also failure to file by the filing date (uncured within 10 days), failure to submit an RBC Plan, an unsatisfactory Plan so designated, or failure to adhere to a Plan with substantial adverse effect | Commissioner requires a Plan/Revised Plan, performs examination or analysis, and issues a **corrective order** |
| Authorized Control Level | Mandatory Control Level RBC ≤ TAC < Authorized Control Level RBC; also failure to respond satisfactorily to a corrective order | Commissioner may take Regulatory-Action-Level actions **or** place the insurer under regulatory control |
| Mandatory Control Level | TAC < Mandatory Control Level RBC | For a life insurer or fraternal society the commissioner **shall** place it under regulatory control; may defer up to 90 days if the event is reasonably expected to be eliminated |

The **RBC Plan** must, among other things, "provide projections of the insurer's financial
results in the current year and at least the four (4) succeeding years, both in the absence
of proposed corrective actions and giving effect to the proposed corrective actions,
including projections of statutory operating income, net income, capital and surplus", may
separate new and renewal business by major line, must identify key assumptions and the
sensitivity of the projections to them [R125 § 3.B]. **This is the multi-year projection
requirement that puts a liability cash flow model on the critical path for RBC, not just a
valuation-date calculation.**

**Trend test mechanics [R128], page LR035:**

- Applies only if TAC < the **Trend Test Safe Harbor = 3.0 × Authorized Control Level RBC**
  *and* the LR034 Level of Action is "None" (i.e. TAC ≥ 2.0 × ACL). So the test bites in the
  200%–300% band [R128][R127].
- Margin in a year = Total Adjusted Capital − Authorized Control Level RBC.
- Decrease from first prior year = prior-year margin − current-year margin, floored at zero.
- Average decrease over the last three years = ⅓ × (third-prior-year margin −
  current-year margin) [derived from LR035 lines (12)–(13); the intermediate line label was
  not legible in extraction, so the exact wording of line (12) is [unverified]].
- **Marginal Difference = the greater of** the one-year decrease and the three-year average
  decrease. The test amount is TAC − Marginal Difference.
- **If that amount is less than 1.9 × Authorized Control Level RBC, the company triggers
  Company Action Level on the trend test** [R128].
- Inputs come from the Five-Year Historical Data page (page 22, lines 30 and 31) for the
  first prior and third prior years [R128].

Historical note: the life trend-test safe harbour was **2.5×** before the 2011 amendment
raised it to **3.0×** to match P/C and health [R126].

### 2. The covariance adjustment — the exact published form

The instructions state the assumption first: "the combined effect of the C–1o, C-1cs, C–2
and C–3 and a portion of the C-4 risks are not equal to their sum but are equal to the
square root calculation described below. It is statistically assumed that the C–1o risk and
a portion of the C–3 risk are correlated, while the C-1cs risk, the C–2 risk, the balance of
the C-3 risk and a portion of the C-4 risk are independent of both" [R128, LR031 Basis of
Factors].

**Line (69) of LR031, as printed [R128]:**

```
RBC after Covariance Before Operational Risk
  = C-0 + C-4a + Square Root of [ (C-1o + C-3a)² + (C-1cs + C-3c)² + (C-2)² + (C-3b)² + (C-4b)² ]
```

This grouping is confirmed **three independent ways within the retrieved document**, which
matters because the exponents are lost in some extractions:

1. LR031 line (69) blank text, with superscript 2 intact on every term [R128].
2. The LR031 narrative spelled out in words: "'A' equals C-0 plus the C–4a risk-based
   capital and the square root of the sum of the C–1o and C–3a risk-based capital squared,
   the C-1cs and C-3c risk-based capital squared, the C–2 risk-based capital squared, the
   C-3b risk-based capital squared and the C-4b risk-based capital squared" [R128].
3. LR049 line (20), which restates the same expression with line references while stressing
   C-3a [R128].

Points an implementer gets wrong easily, all verified [R128]:

- **C-3a is added to C-1o inside one squared term** (interest rate risk correlated with
  general asset default risk); **C-3c (market risk) is added to C-1cs**, not to C-3a. The
  C-3 Phase II instruction says so explicitly: "The amount reported in Line (37) is to be
  combined with the C-1cs component for covariance purposes."
- **C-0 and C-4a sit outside the square root** and are added dollar-for-dollar. C-4b is
  inside as its own squared term. The C-3/C-4 split exists "for general consistency with the
  health RBC formula".
- All terms entering line (69) are **post-tax** (LR031 nets each pre-tax component against
  its tax effect from LR030 before the covariance step). A parallel pre-tax "tax sensitivity
  test" runs the same formula on the pre-tax components at line (76).

**After covariance [R128]:**

```
Gross Basic Operational Risk (line 70)   = 0.03 × line (69)
Net Basic Operational Risk (line 72)     = line (70) − ( C-4a post-tax + C-4a of U.S. life
                                           insurance subsidiaries ),  floored at 0
AG 48 add-on (line 73)                   = Primary Security shortfall for all AG 48 cessions × 2
Total RBC After Covariance (line 74)     = line (69) + line (72) + line (73)
Authorized Control Level RBC (line 75)   = 0.50 × line (74)
Mandatory Control Level RBC              = 0.70 × Authorized Control Level RBC
```

The AG 48 doubling is deliberate: doubling the shortfall then halving to reach Authorized
Control Level produces "a dollar for dollar increase in the Authorized Control Level for the
total of the AG 48 Primary Security shortfall", and it applies even where a state has waived
AG 48 compliance [R128]. See R11/R12 for the underlying guideline and regulation.

A **1% charge on admitted adjusted gross deferred tax assets** (SSAP No. 101 ¶ 11.a and
11.b) is applied **outside the covariance adjustment**, reduced to 0.5% for the ¶ 11.a
component where the insurer filed its own federal return or was in a consolidated return
whose common parent is an insurance company [R128].

**Risk-category definitions as published [R128, Overview]:** C-0 = declining value of
insurance subsidiaries plus off-balance-sheet and miscellaneous accounts (e.g. DTAs);
C-1 = asset default of principal and interest or fluctuation in fair value; C-2 = risk of
underestimating liabilities on business already written or inadequately pricing business to
be written in the coming year; C-3 = losses from changes in interest rate levels, health
benefits prepaid to providers reverting to the insurer, and losses from changes in market
levels associated with variable products with guarantees; C-4 = general business risk.
Authorized Control Level RBC is "50% of the sum of the RBC for the categories, adjusted for
covariance" [R128].

### 3. Risk components, page by page

#### C-0 (LR031 lines 1–12) [R128]
Directly and indirectly owned health, P/C and life insurance affiliates, affiliated alien
insurers, and off-balance-sheet and other items. For a life affiliate the charge is the
affiliate's **Total Risk-Based Capital After Covariance before Basic Operational Risk
(LR031 line 69) plus twice its AG 48 Primary Security shortfall (line 73)**, prorated by
percentage ownership; for a health affiliate XR024 line 41 and for a P/C affiliate PR032
line 60 [R128]. For equity-method affiliates the C-0 charge is capped at the lesser of that
prorated Total RBC After Covariance and the book/adjusted carrying value. Alien Insurance
Subsidiaries — Other are excluded from both C-0 and Total Adjusted Capital.

#### C-1o bonds (LR002) — the 20 NAIC designation categories [R128]

Pre-tax factors applied to book/adjusted carrying value, sourced from the AVR Default
Component (annual statement page 30):

| Designation | Factor | Designation | Factor |
|-------------|--------|-------------|--------|
| Exempt obligations | 0.0000 | 3.A | 0.03151 |
| 1.A | 0.00158 | 3.B | 0.04537 |
| 1.B | 0.00271 | 3.C | 0.06017 |
| 1.C | 0.00419 | 4.A | 0.07386 |
| 1.D | 0.00523 | 4.B | 0.09535 |
| 1.E | 0.00657 | 4.C | 0.12428 |
| 1.F | 0.00816 | 5.A | 0.16942 |
| 1.G | 0.01016 | 5.B | 0.23798 |
| 2.A | 0.01261 | 5.C | 0.30000 |
| 2.B | 0.01523 | NAIC 6 | 0.30000 |
| 2.C | 0.02168 | | |

Long-term and short-term bonds are each split across the seven NAIC classes on separate
line groups; short-term classifications come from AVR Default Component lines 18–24 [R128].

**Bond size factor (portfolio adjustment) [R128]:** bonds are aggregated by issuer (first six
CUSIP digits); exempt U.S. government bonds and the "Class 1 U.S. agency not full-faith-and-
credit" line are excluded from the issuer count and from the base the size factor applies to.
Weighted issuers = 2.40 × first 50 + 1.53 × next 50 + 0.85 × next 100 + 0.85 × next 300 +
0.82 × over 500; **size factor = total weighted issuers ÷ total number of issuers**;
portfolios above 1,300 issuers receive a discount; **if the issuer count is left blank the
maximum 2.40 is applied**. Asset concentration (LR010) is computed on the risk category
*before* the size factor, with an overall 45% RBC cap [R128].

**Provenance and a live caveat.** The LR002 factors above reproduce the "MA Base Factors"
column of the Moody's Analytics study exactly through 5.B, with 5.C and NAIC 6 capped at
30% [R130][R128]. But LR002's *Basis of Factors* narrative still describes the pre-2021
calibration — 2,000 trials, a 400-bond portfolio, a 10-year modelling period, surplus
sufficient in 92% of trials by category and 96% for the portfolio [R128] — which does not
describe the Moody's methodology (correlation model, risk premium at expected loss + ½ s.d.,
21% tax) [R130]. **Treat the narrative as stale relative to the factors** [unverified as to
whether the NAIC intends to update it]. Search results (not a retrieved primary document)
place NAIC adoption of the 20-designation factors in **June 2021, effective for year-end 2021
filings** — recorded here as **[unverified]**; what *is* verified is that they are in force in
both the 2023 and 2024 instructions [R129][R128].

#### C-1cs (LR031 lines 13–21) [R128]
Schedule D unaffiliated common stock, Schedule BA unaffiliated and affiliated common stock,
the **common stock concentration factor** (LR011), holding company in excess of indirect
subsidiaries, and affiliated non-insurers. The category and its independent squared term
originate in R136.

#### C-2 insurance risk — life mortality (LR025) [R128]

**Exposure base: net amount at risk (NAR), net of reinsurance throughout.** Since proposal
2025-01-L the blank derives it from the annual statement rather than free-form company
records [R142]:

```
Total Individual & Industrial Life NAR
  = (Exhibit of Life Insurance, sum of Columns 2 and 4, Line 23 × 1000)
  − [ (Exhibit 5, sum of Columns 3 and 4, Line 0199999)
    + (Separate Accounts Exhibit 3, Column 3, Line 0199999)
    + (General Interrogatories Part 2, Column 1, Line 10.01)
    − (General Interrogatories Part 2, Column 1, Line 10.02) ]
```

i.e. **face amount in force minus life reserves (general account plus separate account),
with a reinsurance adjustment** [R142]. The subcategory NARs come from new General
Interrogatories Part 2 lines (10.08, 10.14 for individual; 10.22, 10.28, 10.34 for group)
[R142].

**Size bands [R128]:** band 1 up to $500 million NAR; band 2 above $500 million to $25
billion; band 3 above $25 billion. Bands apply to the **total** for individual & industrial
life and, separately, to the total for group & credit life, then are **allocated
proportionately** to each factor category [R128][R133].

**Pre-tax factors in force (per dollar of NAR) [R128]:**

| Category | First $500M | Next $24,500M | Over $25,000M |
|----------|-------------|---------------|---------------|
| Individual & Industrial Life **with** Pricing Flexibility | 0.00220 | 0.00105 | 0.00080 |
| Individual & Industrial **Term** Life **without** Pricing Flexibility | 0.00280 | 0.00120 | 0.00085 |
| Individual & Industrial **Permanent** Life **without** Pricing Flexibility | 0.00400 | 0.00175 | 0.00120 |
| Group & Credit Term Life, remaining rate terms ≤ 36 months | 0.00140 | 0.00055 | 0.00040 |
| Group & Credit Term Life, remaining rate terms > 36 months | 0.00190 | 0.00080 | 0.00055 |

FEGLI/SGLI take a separate 0.0004 factor applied to **amount in force**, not NAR [R142].
Group & credit permanent life has its own with/without pricing-flexibility split; the
"without" category is a residual computed as line (6) − (7) − (8) − (9) [R128][R142].

**Product examples the instructions themselves give [R128]:** *with pricing flexibility* —
participating whole life, universal life **without** secondary guarantees, YRT where
scheduled premiums may change annually from issue; *term without pricing flexibility* —
level term with guaranteed level premiums, YRT where scheduled premiums may not be changed;
*permanent without pricing flexibility* — **universal life with secondary guarantees** and
**non-participating whole life**, and this is the **default bucket with the highest factors**
for anything not otherwise recorded.

**Pricing flexibility, defined [R128]:** the ability to *materially* adjust rates on in-force
contracts through premiums and/or non-guaranteed elements as of the valuation date and within
the next **5 policy years**, reflecting typical business practices. A "material rate
adjustment" is the ability to recover, **on a present value basis**, the difference in
mortality risk provided for in the factors for contracts with and without pricing
flexibility: *flexibility factor × NAR = the minimum dollar margin needed*, compared against
margins actually available. Grouping may be at contract or pricing-cohort level. Contracts
may move between categories at successive valuation dates. Insurers may elect the "without"
categories if the evaluation is not completed. Ceded amounts follow the terms of each treaty;
affiliated reinsurers follow the direct categorisation [R128][R133].

**Calibration behind the factors [R131]:** 95th-percentile capital in excess of reserve
mortality, from stochastic simulation of statutory losses (death benefits minus reserves
released) measured as the greatest present value of accumulated deficiencies, discounted at
2.765% after tax; components volatility, level, trend, catastrophe (pandemic; a terrorism
component at 5% annual probability of an extra 0.05 deaths per 1,000; an "unknown sustained
risk" at 2.5% annual probability of a 5% sustained mortality increase persisting up to 10
years). Risk-exposure periods behind the recommended categories: **20 years for ULSG, 10
years for term, 5 years for products with in-force pricing flexibility**; 5 and 3 years for
the two group categories [R131]. The Academy's recommended factors (per $1,000:
ULSG 3.90/1.65/1.10; Term 2.70/1.10/0.75; All Other 1.90/0.75/0.50; group 1.80/0.70/0.45 and
1.30/0.45/0.30) [R131] are **close to but not identical with** the adopted factors above,
and the categories were renamed from product labels to pricing-flexibility labels; the
reconciliation between recommendation and adoption is **[unverified]** — no document
recording that final step was retrieved.

**Legacy factors, for in-force models valuing an earlier year [R131]:** Individual &
Industrial 2.23 / 1.46 / 1.17 / 0.87 and Group & Credit 1.75 / 1.16 / 0.87 / 0.78 per $1,000
of NAR across the old bands (first $500M, next $4.5B, next $20B, over $25B).

#### C-2 insurance risk — longevity (LR025-A) [R128]

**Exposure base: statutory reserve**, not NAR — chosen as "a consistent measure of the
economic exposure to increased longevity" [R128]. Calibrated to the 95th percentile assuming
aggregate reserves already provide an 85th-percentile outcome; trend risk applies equally to
all portfolios while level and volatility risk decline with size. Factors are pre-tax,
developed assuming a 21% tax adjustment is applied afterwards.

| Life-contingent annuity reserves | Factor |
|---|---|
| First $250 million | 0.0171 |
| Next $250 million | 0.0108 |
| Next $500 million | 0.0095 |
| Over $1,000 million | 0.0089 |

**Scope, stated precisely [R128]:** annuity products with life-contingent payments where
benefits are distributed as an annuity — SPIAs and other payout annuities in pay status;
**deferred income annuities that will enter pay status in future**; structured settlements
with any life-contingent benefit; group annuities including pension risk transfer, both
immediate and deferred. The **entire** reserve of an in-scope contract is included, including
the period-certain portion of a certain-and-life annuity. **Variable immediate annuity
reserves under VM-21 are in scope** where payments are life contingent. **Out of scope:**
non-life-contingent annuities; deferred annuities where the policyholder has a right but not
an obligation to annuitize; a certain-and-life annuity reduced to certain payments only after
the annuitant's death; **variable deferred annuity contract reserves under VM-21, including
reserves for contracts whose account value has reached zero but a lifetime benefit remains
payable**.

**Total C-2, with the guardrail and correlation [R128], LR031 line (49):**

```
Total (C-2) Pre-Tax
  = TotalHealthClaimReserves + PremiumStabilizationCredit
  + Greatest of [ GF × (IndivLifeC2 + GroupLifeC2),
                  GF × LongevityC2,
                  sqrt( (IndivLifeC2 + GroupLifeC2)² + LongevityC2²
                        + 2 × ρ × (IndivLifeC2 + GroupLifeC2) × LongevityC2 ) ]
```

with **guardrail factor GF = 0 and correlation factor ρ = −0.25** as stated on LR025-A
[R128]. Because GF = 0, the "greatest of" collapses to the square-root term in every
non-degenerate case — the guardrail is present but switched off [derived from R128; the
NAIC's design intent for GF is documented at R134]. The mortality/longevity diversification
credit is therefore live at −25%. Design history: the Academy proposed −0.33, the Longevity
Risk Subgroup rounded to −0.30 and offered −0.25 as conservative and consistent with other
jurisdictions; GF = 1 would have guaranteed no company's C-2 fell on introduction of the
longevity charge [R134].

Group life and health premium stabilization reserves give a **50% credit** against C-2,
limited to the RBC otherwise calculated [R128].

#### C-3a interest rate risk (LR027) — the C-3 Phase I framework [R128]

**Basis:** the surplus needed for lack of synchronization of asset and liability cash flows.
"The impact of interest rate changes will be greatest on those products where the guarantees
are most in favor of the policyholder and where the policyholder is most likely to be
responsive to changes in interest rates. Therefore, **risk categories vary by withdrawal
provision**." Factors were built assuming well-matched durations, then loaded 50% for less
well-matched portfolios [R128].

**Low-risk derivation, as published [R128]:** assumed asset/liability duration mismatch of
**0.125**, combined with a possible **4% one-year swing in interest rates** (the maximum
historical swing 95% of the time) → pre-tax factor **0.0063**; with the 50% loading,
**0.0095**. Medium and high factors were derived by measuring the additional risk of more
discretionary withdrawal provisions using policyholder-behaviour assumptions and **1,000
random interest rate scenarios**.

**Factor table (pre-tax) [R128].** The second figure applies where the company submits an
**unqualified actuarial opinion based on asset adequacy testing** (or one qualified solely
because of AG 48 direction) — the factors are reduced by **one-third**:

| Risk category | Contents | Factor |
|---|---|---|
| **Low** | annuity reserve **with fair value adjustment** (excluding unitized separate accounts); annuity reserve **not withdrawable** (excluding structured settlements); GIC reserve within 1 year of maturity; single premium life / life insurance reserves | 0.0095 → 0.0063 |
| **Medium** | annuity reserve at **book value less a surrender charge of 5% or more**; Exhibit 7 reserves not included elsewhere; **structured settlements**; additional actuarial reserves from asset/liability analysis | 0.0190 → 0.0127 |
| **High** | annuity reserve at **book value without adjustment** (minimal or no charge or adjustment); debt with GIC-like characteristics | 0.0380 → 0.0253 |

Supplementary contracts not involving life contingencies and dividend accumulations sit in
**medium** risk, "due to the historical tendency of these policyholders to be relatively
insensitive to interest rate changes" [R128].

**Callable/pre-payable assets:** an additional after-tax C-3 requirement of **50% of the
excess, if any, of book/adjusted carrying value above current call price**, computed
asset by asset. Zero for assets used in C-3 cash flow testing or C-3 Phase II testing [R128].

**Equity-indexed products [R128]:** "The same C-3 factors are to be applied for
equity-indexed products as for their non-indexed counterparts; i.e., based on **guaranteed
values ignoring those related to the index**." Equity-indexed products are **excluded from
C-3 cash flow testing** and use the factors (Appendix 1(b)), and are backed out of the LR049
exemption-test amounts by manual entry.

**Exclusions from factor-based C-3 [R128]:** unitized separate accounts without guarantees;
separate accounts guaranteeing an index and following a Class II investment strategy;
non-indexed separate account business with guarantees ≤4% that is subject to a qualifying
fair value adjustment; and experience-rated group and individual pension business meeting
four stated conditions (general account funded; reserve interest rate ≤4% and long-term
guarantee ≤4%; immediate participation/retroactive-credit experience rating; not subject to
discretionary withdrawal or subject to a qualifying fair value adjustment). Guaranteed
indexed separate accounts on a **Class I** strategy are reported in the low-risk category.

**When cash flow testing is required — LR049 exemption test [R128].** Two tests, either of
which forces C-3 cash flow testing:

1. **C-3 significance test.** Compute C-3a percentage = (factor-based C-3a on single premium
   and annuity reserves, excluding equity-indexed, plus C-3a on all other reserves) ÷ (sum of
   C-0, C-1cs, C-1o, C-2, both C-3a pieces, C-3b, C-3c, C-4a, C-4b). **If that percentage
   exceeds 40%, cash flow testing is required.**
2. **C-3 stress test.** Recompute the covariance formula substituting an *adjusted* C-3a =
   [line (17) × 0.79 + line (16) × (1 − t)] + [line (17) × **6.5** × (1 − t)] + all-other
   C-3a — i.e. stressing the annuity/single-premium factor-based charge by a factor of 6.5.
   Take Total Adjusted Capital ÷ that stressed RBC-after-covariance. **If the ratio is less
   than 100% and non-zero, cash flow testing is required.**

Otherwise a company may elect the cash flow method. Companies with **less than $100 million
in admitted assets** at year end are not required to complete line (33) unless a test
triggers. **Once elected, the method must be continued unless the domiciliary regulator
approves reverting to factors** [R128].

**The cash flow method itself (Appendix 1 / 1a) [R128], unchanged in substance from R135:**

- Use the year-end asset adequacy analysis cash flow testing model, or a consistent model,
  with the same assumptions and "as-of" date, but different interest scenarios and a
  different measurement.
- Scope, "Certain Annuities": products with the characteristics of deferred and immediate
  annuities, structured settlements, guaranteed separate accounts (excluding guaranteed
  indexed separate accounts on a Class II strategy) and GICs including synthetic GICs and
  funding agreements; debt incurred for funding an investment account if the domiciliary
  state requires it to be cash flow tested. **Variable annuity products are excluded,
  including guaranteed fixed options within them**, because they go through C-3 Phase II.
- Run either the standard **50-scenario** set or the more conservative **12-scenario** set;
  a company may use the smaller set for some products and the larger for others.
- Capture statutory capital and surplus S(t) = statutory assets − statutory liabilities, by
  scenario, at every calendar year end of the testing horizon.
- Per scenario the C-3 measure is the **most negative of the series of present values
  S(t)·pv(t)**, where pv(t) = ∏ 1/(1+i) over t years using **105% of the after-tax one-year
  U.S. Treasury rate** for that scenario.
- Rank descending (rank 1 = worst). For the **50-scenario** set apply weights to ranks
  **17,16,…,5** of **0.02, 0.04, 0.06, 0.08, 0.10, 0.12, 0.16, 0.12, 0.10, 0.08, 0.06, 0.04,
  0.02** (peaking at rank 11) and sum the products. For the **12-scenario** set take the
  average of ranks 2 and 3, floored at half the worst scenario score.
- Aggregation across portfolios: either sum S(t) across portfolios by scenario then rank, or
  compute C-3 scores by product by scenario, sum by scenario, then rank and weight.
- Modelling conventions: **initial assets = reserves** (no surplus assets); **AVR-related
  assets excluded** from initial assets and future AVR contributions not modelled, though
  *expected* credit losses are in the cash flows; **IMR assets are used**; interim measure is
  retained statutory surplus; horizon extends until surplus contributions on a closed block
  are immaterial, holding scenario rates constant at the year-30 level beyond the generator's
  30 years; profits-retained (no stockholder dividends withdrawn, but policyholder dividends
  and credited rates modelled realistically); reinvestment and disinvestment strategy as in
  asset adequacy analysis; **key assumptions must be stress tested (e.g. lapses increased by
  50%)**; the actuary must avoid double counting margins already credited against C-1o.
- **Result assembly (Appendix 1):** total C-3 = (a) cash-flow-tested annuities and single
  premium life + (b) equity-indexed on factors + (c) all other on factors + (d) callable/
  pre-payable add-on, **but not less than half the C-3 component computed entirely on
  factors** [R128]. On the blank this is LR027 line (34): if line (33) = 0 then line (34) =
  line (32); otherwise line (34) = line (32) + line (33) − line (16) − line (17), subject to
  a minimum of 0.5 × line (32).
- Reporting: results may be estimated for the year-end annual statement, but the RBC
  electronic filing carries the actual results; **if the actual exceeds the estimate by more
  than 5%, or if the actual triggers regulatory action, a revised filing is required by
  June 15**. The submission is accompanied by an **appointed actuary C-3 Assumption
  Statement** certifying the assumptions are not unreasonable, required even where a
  different actuary did the work [R128].

Original-design note [R135]: the 1999 recommendation collared the result between **half and
double** the factor answer; the current instructions retain only the half floor. The 12/50
scenario sets were selected from a randomly generated set of 200 as those most likely to
reproduce the full-200 result.

#### C-3c market risk — C-3 Phase II for variable annuities (LR027 line 37) [R128]

**This section adds to R47, which carries the pre-reform version. Where they differ, R128 is
current and R47 is historical.** Deltas from R47: the confidence level moved from **CTE 90**
to **CTE 98**; a **25% scalar** now sits in front; the Standard Scenario has been replaced by
the **Additional Standard Projection Amount** of VM-21 Section 6; the federal income tax rate
is the enacted maximum, not 35%; and the calculation is expressed as a seven-step process
tied to VM-21 rather than to the 2005 Academy report.

**Scope:** "all policies and contracts that have been valued following the requirements of
AG-43 or VM-21" [R128].

**The seven steps [R128]:**

1. Determine **CTE 98** — "the numerical average of the 2% largest values of the Scenario
   Reserves, as defined by Section 4 of VM-21", using the same process and methods as the
   reserve calculation.
2. Convert to a C-3 RBC amount by the paragraph-B formula, floored at $0.
3. For contracts reserved under the **Alternative Methodology** (VM-21 Section 7), determine
   C-3 RBC under Appendix 2 of the instructions.
4. C-3 RBC = step 2 + step 3, not less than zero. **Total Asset Requirement = the VM-21
   Reserve before any phase-in, plus the C-3 RBC amount.**
5. If a VM-21 § 2.B reserve phase-in was elected, phase in C-3 RBC over the same period.
6. Apply smoothing if elected.
7. Divide by (1 − enacted maximum federal corporate income tax rate) to reach a pre-tax
   amount and **split it into an interest rate component (→ line 35, C-3a) and a market risk
   component (→ line 37, C-3c)**; neither may be negative.

**Tax treatment — two permitted methods [R128]:**

- **Macro Tax Adjustment (MTA):** modelled cash flows ignore federal income tax, so each
  scenario reserve is numerically identical to the VM-21 aggregate reserve calculation's, and
  tax enters through the formula:

  > `25% x ((CTE (98) + Additional Standard Projection Amount – Statutory Reserve) x (1 – Federal Income Tax Rate) – (Statutory Reserve – Tax Reserve) x Federal Income Tax Rate`

  reproduced exactly as printed; **the parentheses in the published text are unbalanced**, so
  the intended bracketing of the second term is **[unverified]**. The instruction's own gloss
  — "in the second term – i.e., the difference between statutory reserves and tax reserves
  multiplied by the Federal Income Tax Rate – may not exceed the portion of the company's
  non-admitted deferred tax assets attributable to the same portfolio of contracts to which
  VM-21 is applied" — supports reading it as a separate deduction with its own cap [R128].
- **Specific Tax Recognition (STR):** tax is reflected inside the projection of Accumulated
  Deficiencies (VM-21 § 4.A), discounting at projected after-tax rates, and

  > `25% x (CTEAT (98) + Additional Standard Projection Amount – Statutory Reserve)`

  A **tax adjustment** is required where actual tax reserves exceed projected tax reserves at
  the start of the projection: increase CTEAT(98) by *corporate tax rate × f × (actual tax
  reserves − projected tax reserves at t=0)*, where **f = 1 − the average, across the CTE(98)
  scenarios, of the ratio of contracts in force at the scenario's greatest-present-value
  duration to contracts in force at the start**. Under the Alternative Method, **f ≈ 0.5**
  [R128]. Switching from STR back to MTA requires prominent disclosure.

**Smoothing [R128]:** optional, with domiciliary approval required to change the election
year over year or to smooth after a material change in the Clearly Defined Hedging Strategy
(materiality judged against VM-21 § 1.D.2). Mechanics: ratio = 0.4 × prior-year
(C-3 RBC ÷ reserve) + 0.6 × current-year (C-3 RBC ÷ reserve); current-year RBC = ratio ×
current-year aggregate reserve. Voluntary reserves are stripped out of both years.

**Phase-in [R128]:** where a VM-21 § 2.B reserve phase-in was elected, the C-3 RBC effect is
phased over the same period — compute a phase-in amount PIA as the excess of the restated
12/31/2019 C-3 RBC on the new basis over the 2019 reported amount, then subtract PIA × ⅔ at
12/31/2020 and PIA × ⅓ at 12/31/2021, adjusted proportionately for phase-ins longer than
three years.

**Governance [R128]:** grouping, sampling, scenario count and simplification are the
company's responsibility but are "subject to Actuarial Standards of Practice, supporting
documentation and justification, and **should be identical to those used in calculating the
company's statutory reserves following VM-21**." Certification requirements are **the same as
for reserves under VM-31**; the C-3 RBC actuarial memorandum may incorporate the VM-21 VA
Report by reference and must identify the basis for tax treatment, whether smoothing and
phase-in were used, the Alternative Methodology documentation, and how the amount was
allocated between the interest and market components. Under STR the company must still
disclose the TAR and C-3 RBC that MTA would have produced.

**Separate accounts that guarantee an index [R128]:** a distinct CTE-90 style calculation on
60 months of net tracking error, with a K adjustment for variance including serial
correlation (covariance set to 0 where serial correlation < 0.20), the sample standard
deviation increased 15% and constrained to 50%–150% of the uncorrelated figure; order the
transformed series ascending, set positives to zero, average the first six values and change
sign to obtain the CTE 90 capital for C-1 and C-3; a 4% charge applies with fewer than 30
months of history, phasing thereafter, subject to a 0.4% minimum factor.

#### C-3b health credit risk (LR028) and C-4b (LR029) [R128]
Not material to individual life and annuity products; both carry a 0.0000 tax factor and
enter the covariance as separate squared terms.

#### C-4a business risk (LR029) [R128]
Pre-tax **2.53% of Schedule T life premiums and annuity considerations**; **0.63%** of
Schedule T accident and health premiums; **0.06% of separate account liabilities**. Factors
were set by reference to guaranty fund assessment exposure without mirroring the assessment
formulas, plus other general business exposures such as litigation. Deposit-type funds on
Schedule T are excluded. Variable and other premiums and considerations — all variable
business life, annuity and health, and other business ultimately reserved in the separate
account — are excluded from the premium factors because the separate account liability
factor covers them. C-4a is also the offset against the operational-risk add-on.

### 4. Total Adjusted Capital, and how RBC connects to the reserve basis [R128, LR033]

```
(1) Capital and Surplus (Page 3, Col 1, Line 38)                     × 1.000
(2) Asset Valuation Reserve (Page 3, Col 1, Line 24.01)              × 1.000
(3) Dividends Apportioned for Payment (Page 3, Col 1, Line 6.1)      × 0.500
(4) Dividends Not Yet Apportioned (Page 3, Col 1, Line 6.2)          × 0.500
(5) Hedging Fair Value Adjustment                                    × −1.000
(6) Life subsidiary AVR (prorated by ownership)                      × 1.000
(7) Life subsidiary dividend liability (prorated)                    × 0.500
(8) Carrying value of non-admitted insurance affiliates              × 1.000
(9) less Non-tabular discount and/or Alien Insurance Subsidiaries–Other
(10) Total Adjusted Capital Before Capital Notes = (1)…(8) − (9)
(11.4) plus Credit for Capital Notes (limited)
(12) less XXX/AXXX Reinsurance RBC Shortfall
(13) TOTAL ADJUSTED CAPITAL
```

**Why the AVR is capital [R128]:** "In determining the C–1 risk factors, availability of the
AVR and voluntary investment reserves to absorb specific losses was not assumed. Therefore,
the AVR is counted as capital for the purposes of the formula although it represents a
liability and is not usable against general contingencies." **The portion of the AVR that
counts is limited to the amount not utilized in asset adequacy testing in support of the
Actuarial Opinion for reserves** — a direct coupling between the appointed actuary's AAT work
(R29) and the numerator of the RBC ratio. Voluntary investment reserves were removed from TAC
in the 1997 formula.

**Dividend liability:** 50% of the annual statement dividend liability is included as a
general cushion; **no credit to either party where a block is reinsured unless the company
has total control over the dividend decision and the full benefit of a scale change**; the
sensitivity test uses 25% [R128].

**Capital notes:** credited subject to a schedule by years to maturity (0.0 to 1.0 in
LR032) and an overall limitation that capital and surplus notes together do not exceed
one-half of TAC from other sources — equivalently one-third of TAC from all sources. Issuance
conditions include subordination to policyholders, commissioner approval, a ≤25% of TAC
aggregate cap at issuance, minimum five-year term, maturity concentration limits (5% in any
one year, 12% in any three-year period), and **mandatory deferral of interest/principal if
payment would drop TAC below Company Action Level RBC, or below 125% of Company Action Level
RBC where the trend test shows a negative trend** [R128].

**Sensitivity tests reported alongside [R128]:** a tax sensitivity test removing deferred tax
assets and liabilities from TAC and recomputing all levels on pre-tax factors, and an
**Ex-DTA ACL RBC Ratio** = (TAC − company deferred tax assets) ÷ Authorized Control Level RBC.

**Level of Action page (LR034) [R128]:** trigger points are computed mechanically as 2.0×,
1.5×, 1.0× and 0.7× Authorized Control Level RBC, and the **Authorized Control Level RBC
Ratio = Total Adjusted Capital ÷ Authorized Control Level RBC** — this is "the RBC ratio"
that market participants quote. An indicator of None is shown if TAC exceeds Company Action
Level RBC **unless the trend test triggers Company Action Level**.

**The VM-21 / C-3 Phase II identity.** VM-21 states that its projections are anticipated to
be used for RBC and that VM-21 §§ 4.A–4.E and the RBC requirements are identical except for
the elective federal income tax treatment [R35]. The instructions close the loop from the
capital side: the same VM-21 Scenario Reserves are averaged at CTE 70 for the reserve and at
CTE 98 for capital; the Additional Standard Projection Amount is computed once under VM-21
§ 6 and used in both; grouping, sampling and simplification "should be identical to those
used in calculating the company's statutory reserves following VM-21"; and the certification
and documentation follow VM-31 [R128][R35]. **One stochastic run, two order statistics.**

### 5. Change control and what is coming

- Structural changes to the RBC blanks are adopted by **May 15**, non-structural by
  **June 30**, and the instructions publish around **November 1** for that year end
  [R141][R139].
- Adopted for the year-end 2025 filing [R139]: tax credit investments (2024-21-L MOD);
  principle-based bond definition conformity across LR002/005/008/009/010/011/012/017/029/
  031/033/038/042-048 (2024-24-L MOD); LR025 annual-statement sourcing (2025-01-L, see R142);
  LR008 reorganization to separate C-1o from C-1cs Schedule BA assets (2025-04-L MOD);
  LR010 asset concentration for SVO-designated non-bond debt securities (2025-05-L);
  **trend test labelling across LR034/LR035 (2025-07-CA MOD)**; and modco/funds-withheld
  clarifications (2025-10-L).
- **Correlation matrix proposal** to replace the square-root covariance formula — proposed,
  not adopted as of the 2024 instructions [R137][R128].
- **C-3 alignment** — a single C-3 methodology absorbing both Phase 1 and Phase 2, with FIA
  brought into scope, GOES scenarios, PBR models with prudent estimate assumptions, a scalar
  of the generic form YY% × (CTE XX − reserves), a three-year phase-in, and CTE 70 default
  costs in C-3 Phase 1 [R138]. Field test specifications were re-exposed **July 30, 2026**
  [R141]. Search results place the field test at a **December 31, 2025 valuation date** with
  adoption targeted around 2027 — **[unverified]**, no primary NAIC exposure document was
  retrieved.

---

## Model hooks

What a liability cash flow projection model must produce for each capital item.

| Accounting / capital item | What the liability cash flow model must produce | Granularity / basis / timing |
|---|---|---|
| **C-2 mortality NAR** [R128][R142] | Face amount in force **minus** statutory reserve, net of reinsurance, at the valuation date | Per policy, then summed to: individual & industrial with pricing flexibility / term without / permanent without; and group ≤36-month / >36-month rate terms. Statutory reserve basis (general account Exhibit 5 + separate account Exhibit 3). Valuation date = Dec 31. |
| **C-2 pricing-flexibility classification** [R128][R133] | For each contract or pricing cohort: the **present value of margin available** from repricing NGEs/premiums over the next 5 policy years, compared with *flexibility factor × NAR* | Contract or pricing-cohort level; re-assessed each valuation date (contracts may move categories); ceded amounts assessed per treaty. Model must be able to run a repricing scenario, not just a base scenario. |
| **C-2 longevity exposure** [R128] | Statutory reserve for **life-contingent** annuity benefits, including the certain portion of certain-and-life contracts, general account and separate account | By contract, flagged life-contingent vs not; DIA reserves in deferral count; VA deferred reserves under VM-21 do **not**, even post-account-exhaustion; variable *immediate* annuity reserves do. Valuation-date reserve. |
| **C-3a factor-based charge** [R128] | Annual-statement reserves bucketed **by withdrawal provision**: with fair value adjustment / not withdrawable / book value less ≥5% surrender charge / book value without adjustment; separately life reserves and single premium life reserves | Reserve level by product and by surrender-charge state at the valuation date. Net of reinsurance, less policy loans, plus modco assumed less modco ceded. Indexed products use **guaranteed values ignoring the index**. |
| **C-3a cash flow tested charge (Phase I)** [R128][R135] | For each of 12 or 50 prescribed interest scenarios and each projection year end: **S(t) = statutory assets − statutory liabilities** for the tested portfolio, on the asset adequacy model, initial assets = reserves, AVR excluded, IMR included, profits retained | Portfolio/segment level, annual time step, horizon to immateriality (rates flat past year 30). Discount at 105% of that scenario's after-tax 1-year Treasury. Same "as-of" date as AAT; if not 12/31, scale by the C-3-to-reserve ratio. Plus a lapse +50% sensitivity run. |
| **C-3 exemption test** [R128] | All nine C-risk components and Total Adjusted Capital, so the 40% significance test and the ×6.5 stress test can be evaluated | Company level, at the valuation date. Requires the whole formula to be computable before knowing whether cash flow testing is needed. |
| **C-3c / C-3a from Phase II** [R128][R35] | The full VM-21 stochastic run: Scenario Reserves by scenario; **CTE 70** for the reserve and **CTE 98** for capital; the Additional Standard Projection Amount under VM-21 § 6; the Alternative Methodology amount for in-scope contracts | Same seriatim/grouped model, same scenario set, same assumptions as the reserve. Also: tax reserves at t=0 and projected, and (for STR) tax inside the accumulated-deficiency projection with after-tax discounting; contracts-in-force ratios at each scenario's greatest-present-value duration to compute *f*. Allocation of the pre-tax total between interest and market components. |
| **Total Adjusted Capital** [R128] | Statutory capital and surplus; AVR; the **portion of AVR not used in asset adequacy testing**; dividend liability; hedging fair value adjustment | Company level. The AVR limitation requires the AAT model to report how much AVR it consumed — a direct dependency of the capital numerator on the projection model. |
| **RBC Plan projections** [R125] | Projected statutory operating income, net income, capital and surplus for the current year and **at least four succeeding years**, both with and without proposed corrective actions, optionally split new vs renewal by major line, with identified key assumptions and sensitivities | Multi-year deterministic projection, statutory basis, at least 5 years. This is the only place the model act itself mandates projection output. |
| **Projected capital requirement (business planning)** [R128, derived] | To project an RBC ratio forward, the model must roll forward, per future year end: NAR by C-2 category; reserves by C-3 risk category; life-contingent annuity reserves; the VM-21 CTE 70 / CTE 98 pair; supporting-asset book values by NAIC designation category and issuer count; premiums and annuity considerations; separate account liabilities; and statutory surplus and AVR | Annual, statutory basis, over the planning horizon. Note the RBC formula reads **statement values**, not model quantities — so the projection must produce a projected *annual statement*, not just cash flows. This mapping is an inference from the blank line sources, not a published requirement — **[unverified]** as a stated requirement. |
| **AG 48 / Model #787 shortfall** [R128][R11][R12] | Required Level of Primary Security under the AG 48 Actuarial Method, versus Primary Security actually held, per cession | Per cession (LR036), consistent with Supplemental Term and Universal Life Insurance Reinsurance Exhibit Part 2B Column 19. Enters ACL dollar-for-dollar. |
| **C-4a exposure** [R128] | Schedule T life premiums and annuity considerations; separate account liabilities | Company level, excluding deposit-type funds and variable/other premiums. |

---

## Product applicability

Against the twelve U.S. products in this library. `x` = the item directly determines a
capital charge for that product; `(x)` = qualified/indirect.

| Item | term | whole-life | universal-life | indexed-ul | variable-ul | guaranteed-ul | fixed-def-annuity | fixed-indexed-annuity | variable-annuity | RILA | immediate-annuity | deferred-income-annuity |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Model #312 action levels, trend test [R125][R126] | x | x | x | x | x | x | x | x | x | x | x | x |
| C-2 mortality, NAR-based [R128] | x | x | x | x | x | x | | | | | | |
| — with pricing flexibility [R128] | (x) YRT repriceable | x par WL | x UL w/o SG | x IUL w/o SG | (x) | | | | | | | |
| — term without pricing flexibility [R128] | x level term | | | | | | | | | | | |
| — permanent without pricing flexibility (highest factors) [R128] | | x non-par WL | (x) | (x) | (x) VUL w/ SG | x ULSG | | | | | | |
| C-2 longevity, reserve-based [R128] | | | | | | | (x) only after annuitization | (x) only after annuitization | (x) variable **immediate** only | | x | x |
| C-3a factor charge, low risk (0.0095/0.0063) [R128] | x life reserves | x | x | x | (x) | x | x MVA contracts | x MVA contracts | (x) fixed account | (x) | x not withdrawable | x |
| C-3a factor charge, medium (0.0190/0.0127) [R128] | | | | | | | x SC ≥5% | x SC ≥5% | (x) | (x) | x structured settlements | |
| C-3a factor charge, high (0.0380/0.0253) [R128] | | | | | | | x book value, no adjustment | x book value, no adjustment | | (x) | | |
| Indexed treatment: guaranteed values ignoring index; excluded from CFT [R128] | | | | x | | | | x | | (x) | | |
| C-3 Phase I cash flow testing scope ("Certain Annuities" + single premium life) [R128] | | | | | | | x | excluded as equity-indexed | excluded (Phase II) | [unverified] | x | x |
| C-3 Phase II, CTE 98 (AG 43 / VM-21 population) [R128][R35][R38] | | | | | | | | | x | (x) if VM-21-valued | (x) variable immediate | |
| C-1cs / separate account interactions [R128][R136] | | | | | x | | | | x | (x) | | |
| C-4a: 2.53% premium factor [R128] | x | x | x | x | (x) | x | x | x | (x) | (x) | x | x |
| C-4a: 0.06% separate account liability factor [R128] | | | | | x | | | | x | (x) | | |
| AG 48 shortfall × 2 into ACL [R128][R11][R12] | x | | | | | | x ULSG-financed | | | | | |
| TAC: 50% dividend liability credit [R128] | (x) | x par | (x) | | | | | | | | | |
| TAC: AVR limited by AAT usage [R128][R29] | x | x | x | x | x | x | x | x | x | x | x | x |
| Prospective: FIA into C-3 Phase 1 scope [R138] | | | | | | | | x | | (x) | | |

**Notes on the matrix**

- **guaranteed-ul (ULSG)** is the single product most exposed by the C-2 restructure: it sits
  in the highest-factor bucket (0.00400 / 0.00175 / 0.00120), which was calibrated on a
  **20-year** risk exposure period [R131], and it is simultaneously the product that drives
  AG 48 Primary Security shortfalls into Authorized Control Level dollar-for-dollar [R128].
- **term-life** splits by design: level term with guaranteed premiums is "Term without
  Pricing Flexibility" (10-year exposure period calibration), while repriceable YRT can
  qualify as "with Pricing Flexibility" (5-year) [R128][R131]. Reserve-financed term also
  picks up the AG 48 add-on.
- **whole-life** splits by participation: participating whole life is expressly named as a
  "with pricing flexibility" example; **non-participating whole life is expressly named in the
  permanent-without-pricing-flexibility bucket** [R128]. Par whole life also earns the 50%
  dividend-liability credit in Total Adjusted Capital [R128].
- **indexed-ul and fixed-indexed-annuity** both take C-3 factors "based on guaranteed values
  ignoring those related to the index" and are carved out of C-3 cash flow testing [R128].
  This changes prospectively for FIA under C-3 alignment [R138].
- **variable-annuity** is the only product where reserve and capital are two order statistics
  of one stochastic run [R128][R35]; note also that its *deferred* reserves are expressly
  **out** of the longevity charge even after account exhaustion, while variable *immediate*
  annuity reserves are **in** [R128].
- **registered-index-linked-annuity** marks are qualified throughout: the 2024 instructions
  **never name RILA, ILVA or index-linked variable annuities**. Whether a RILA lands in C-3
  Phase II depends on whether it is valued under AG 43/VM-21; otherwise it takes factor-based
  C-3, presumably on the equity-indexed convention. **This inference is [unverified]** — see
  Gaps.
- **immediate-annuity and deferred-income-annuity** are the products the new C-2 longevity
  charge was built for, and both are explicitly enumerated in the LR025-A scope [R128].

---

## Gaps and caveats

**Things verified that correct plausible-sounding recollections**

1. **The covariance formula's grouping.** C-3a pairs with **C-1o**; C-3c pairs with
   **C-1cs**; C-2, C-3b and C-4b are standalone squared terms; **C-0 and C-4a are outside the
   radical**. Verified three ways inside R128. Any version that puts C-3 wholly with C-1, or
   omits the C-1cs+C-3c pairing, or brings C-4a inside, is wrong for the current formula.
2. **The multipliers.** Company Action = 2.0×, Regulatory Action = 1.5×, Authorized Control =
   1.0×, Mandatory Control = **0.70×** ACL, and the **life trend-test safe harbour is 3.0×**,
   raised from 2.5× in 2011 [R125][R126]. The trend test trips at **1.9×** ACL after
   subtracting the marginal difference [R128].
3. **C-3 Phase II is no longer CTE 90.** The current instruction is **CTE 98 with a 25%
   scalar** against the statutory reserve plus the Additional Standard Projection Amount
   [R128]. R47 records the older CTE 90 / TAR construction, and R48 records QIS II's CTE 95 +
   25% scalar recommendation — three different numbers in three documents, all of them real
   at different dates.
4. **The C-2 life categories are not product categories.** They are *pricing flexibility*
   categories with product examples attached, and the default when the assessment is not
   performed is the worst bucket [R128][R133]. Modelling C-2 off a product code alone will
   misclassify.
5. **There is no "C-1 bond factor" in the singular.** There are 20 designation-category
   factors plus a portfolio size factor keyed to weighted issuer count, which defaults to the
   punitive 2.40 if the issuer count is not supplied [R128].
6. **The longevity guardrail is currently switched off** (guardrail factor 0), so the −0.25
   mortality/longevity correlation credit applies in full [R128].

**What could not be verified or retrieved**

- **The NAIC RBC Forecasting and Instructions is a paid publication.** No free NAIC-hosted
  copy exists; the 2024 and 2023 editions were read from Indiana Department of Insurance
  postings (R128, R129), both marked "Not for Distribution". Anyone rebuilding this work
  should buy the current edition from `content.naic.org/publications` rather than rely on a
  state posting. **The 2025 edition could not be parsed** —
  `https://www.in.gov/idoi/files/RBCL25-INpdf.pdf` returned a truncated PDF stream — so
  nothing here is asserted about year-end 2025 factors beyond the newsletter's change list
  (R139).
- **The RBC forecasting spreadsheet** was not obtained. Any statement about how the software
  performs the size-band allocation or the "greatest of" C-2 selection rests on the printed
  instructions, not on the tool.
- **Effective dates of the current C-2 and longevity structures.** Both are present in the
  2023 and 2024 editions with identical numbers [R129][R128]. The *first* year each applied
  was not established from a primary document; the C-2 instruction supplement is dated
  December 19, 2022 and describes the structure as "newly adopted" [R133], which is
  consistent with year-end 2023 but does not prove it. **[unverified]**
- **Effective date and adoption date of the 20-designation C-1 bond factors.** Search results
  say June 11, 2021 adoption, effective for year-end 2021 filings; **no primary NAIC
  adoption record was retrieved**, so that date is **[unverified]**. What is verified is the
  factor set and its match to the Moody's Analytics study [R128][R130].
- **Reconciliation between the Academy's recommended C-2 factors and the adopted ones.** The
  adopted factors sit slightly above the Academy's November 2021 recommendation in every cell
  and the category names changed from product labels to pricing-flexibility labels
  [R131][R128]. The document recording that final regulator decision was not found.
  **[unverified]**
- **The MTA C-3 Phase II formula's bracketing.** The published parentheses are unbalanced
  [R128]; the intended grouping of the `(Statutory Reserve − Tax Reserve) × tax rate` term is
  **[unverified]**. An implementer should confirm against the RBC software or a current
  Academy practice note before coding it.
- **LR035 trend-test line (12).** The label for the third-prior-year decrease line did not
  survive text extraction cleanly; the three-year average is stated as ⅓ of that line, so the
  arithmetic is clear but the exact wording is **[unverified]**.
- **RILA / index-linked variable annuity treatment.** The 2024 instructions contain no
  mention of RILA, ILVA, index-linked or registered index-linked annuities [R128]. This is a
  genuine hole for one of the twelve products in this library — the capital treatment has to
  be inferred from whether the contract is valued under VM-21 (→ C-3 Phase II) or not
  (→ factor-based C-3 with the equity-indexed convention). Neither reading is sourced.
- **No Academy RBC practice note was located.** Unlike VM-20 (R23) and VM-21 (R66), no
  practice note covering RBC mechanics was found on actuary.org during this session. The
  nearest substitutes are the work-group reports catalogued here (R131, R132, R135, R136,
  R137, R138), which are recommendations to regulators, not practice guidance.
- **C-3 alignment field test details.** The field-test specifications document itself was not
  retrieved; only the Academy's framework presentation (R138) and the working group page's
  note of a July 30, 2026 re-exposure (R141). The reported December 31, 2025 valuation date
  and 2027 adoption target come from search summaries and are **[unverified]**.
- **The correlation-matrix proposal's status.** R137 is a proposal. It is **not** in the 2024
  instructions [R128]. Whether it has since been adopted was not established.
- **The C-1cs beta adjustment.** R136 recommended a beta-scaled common stock factor (30%
  base, 22.5% floor, 45% cap). Whether the current instructions retain it was **not
  verified** — the LR005 unaffiliated common stock page was not read in this session.
- **LR002's Basis of Factors narrative is stale relative to its own factors** — it still
  describes the pre-2021 calibration while the factors are the 2021 Moody's set
  [R128][R130]. That mismatch is my observation from comparing the two documents, not a
  statement either document makes. **[unverified]** as to NAIC intent.
