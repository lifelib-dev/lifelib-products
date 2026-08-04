# Regulatory and Actuarial References — U.S. Individual Life Insurance and Annuities

**Status:** Draft, 2026-08-03; extended to cover individual annuities 2026-08-04.

Curated reference library for the U.S. section of the reference-product library. It
covers the regulatory, tax, experience-study, practice-note, standards, and accounting
sources that the reference cash-flow-model implementations rely on — the six individual
**life** products (term / whole life / UL / IUL / VUL / ULSG) at entries **R1–R34**, and
the six individual **annuity** products (fixed deferred / fixed indexed / variable /
registered index-linked / immediate / deferred income) at entries **R35–R72**. Several
R1–R34 entries also bind annuity models; they are not restated, and the annuity
product-relevance matrix below therefore covers both halves of the numbering. Sections 1–6
carry the life entries, sections 7–13 the annuity entries, and section 14 records the
annuity half's gaps, fetch failures, and unverified points.

Product folders cite entries on this page as **[REG-R#]** (e.g., `[REG-R16]`); the
R1–R72 numbering below is **frozen** — do not renumber or reuse numbers, as product
documentation already cites against it. Within this page, plain `[R#]` refers to the same
entries. Facts drawn from a document that was actually retrieved carry its number; claims
from general knowledge or secondary sources are tagged **[unverified]**; failed or
unfetched links are disclosed per entry — no URL on this page is fabricated. **R1–R34
were accessed 2026-08-03; R35–R72 were accessed 2026-08-04**, unless an entry notes
otherwise.

**Retrieval note for R35–R72:** many primary PDFs (NAIC model laws, the Valuation Manual,
Academy papers) return raw compressed streams to the fetch tool. Where that happened the
PDF was downloaded and its text extracted locally before reading; those entries are marked
**fetched: yes (local text extraction)** and their annotations are first-hand. Domain
blocks encountered on 2026-08-04: **sec.gov returned HTTP 403** to automated clients;
**federalregister.gov and ecfr.gov redirect to a bot-block page**; **irs.gov returned 404**
on the LB&I directive URLs surfaced by search. Where a working alternative existed
(govinfo.gov, law.cornell.edu, gao.gov) it was used and is cited instead.

---

## Product-relevance matrices

`x` = directly relevant per the source annotation; `(x)` = qualified or peripheral
relevance (e.g., "background", "by analogy", "to a lesser degree") per the source
annotation; blank = not indicated by the source.

### Matrix A — individual life products (entries R1–R34)

| R# | Reference (short name) | term | whole-life | universal-life | indexed-ul | variable-ul | guaranteed-ul |
|----|------------------------|------|------------|----------------|------------|-------------|---------------|
| R1 | Standard Valuation Law (Model #820) | x | x | x | x | x | x |
| R2 | Standard Nonforfeiture Law (Model #808) | x | x | | | | |
| R3 | Valuation Manual, 2026 edition | x | x | x | x | x | x |
| R4 | Illustrations Model Reg (Model #582) | x | x | x | x | | |
| R5 | UL Model Regulation (Model #585) | | | x | x | (x) | x |
| R6 | Model #830 ("Regulation XXX") | x | | | | | x |
| R7 | AG 38 | | | x | x | | x |
| R8 | AG 49 (original) | | | | x | | |
| R9 | SOA AG 49 history article | | | | x | | |
| R10 | AG 49-A as revised 2023 ("AG 49-B") | | | | x | | |
| R11 | AG 48 | x | | | | | x |
| R12 | Reserve Financing Model Reg (Model #787) | x | | | | | x |
| R13 | IRC § 7702 | (x) | x | x | x | x | x |
| R14 | IRC § 7702A (MEC) | | x | x | x | x | |
| R15 | IRC § 817 (variable contracts) | | | | | x | |
| R16 | IRC § 807 (tax reserves) | x | x | x | x | x | x |
| R17 | 2017 CSO Tables | x | x | x | x | x | x |
| R18 | 2015 VBT | x | x | x | x | x | x |
| R19 | ILEC 2012–2019 mortality report | x | x | x | x | x | x |
| R20 | 2009–13 persistency study | x | x | x | | x | x |
| R21 | 2015–21 UL persistency/lapse study | | | x | x | (x) | x |
| R22 | Post-level term study (2021) | x | | | | | |
| R23 | AAA VM-20 practice note | x | x | x | x | x | x |
| R24 | AAA illustrations practice note | x | x | x | x | | |
| R25 | AAA PBR assumptions resource manual | x | x | x | x | x | x |
| R26 | ASOP 2 (nonguaranteed elements) | x | x | x | x | x | |
| R27 | ASOP 7 (cash flow analysis) | x | x | x | x | x | x |
| R28 | ASOP 15 (dividends) | | x | | | | |
| R29 | ASOP 22 (asset adequacy opinions) | x | x | x | x | x | x |
| R30 | ASOP 24 (illustrations) | x | x | x | x | | |
| R31 | ASOP 52 (PBR) | x | x | x | x | x | x |
| R32 | ASOP 56 (modeling) | x | x | x | x | x | x |
| R33 | NAIC AP&P Manual | x | x | x | x | x | x |
| R34 | FASB ASU 2018-12 (LDTI) | x | x | x | x | x | x |

### Matrix B — individual annuity products (entries R1–R72)

Covers both halves of the numbering: the R1–R34 entries insofar as they bind — or are
expressly excluded from — annuity models, and the new R35–R72 entries. One extra marker is
used in this matrix only: **`n/a`** = the source states the entry does **not** apply to
annuities, listed so that a life-only rule is not mis-applied (blank still means "not
indicated by the source"). Row-level qualifications are keyed by R# in the notes beneath.

| R# | Reference (short name) | fixed-deferred-annuity | fixed-indexed-annuity | variable-annuity | registered-index-linked-annuity | immediate-annuity | deferred-income-annuity |
|----|------------------------|------------------------|-----------------------|------------------|----------------------------------|-------------------|-------------------------|
| R1 | Standard Valuation Law (Model #820) | x | x | x | x | x | x |
| R2 | Standard Nonforfeiture Law (Model #808) | n/a | n/a | n/a | n/a | n/a | n/a |
| R3 | Valuation Manual, 2026 edition | x | x | x | x | x | x |
| R4 | Illustrations Model Reg (Model #582) | n/a | n/a | n/a | n/a | n/a | n/a |
| R5 | UL Model Regulation (Model #585) | | (x) | | | | |
| R6 | Model #830 ("Regulation XXX") | n/a | n/a | n/a | n/a | n/a | n/a |
| R7 | AG 38 | n/a | n/a | n/a | n/a | n/a | n/a |
| R8–R10 | AG 49 / AG 49-A family | n/a | n/a | n/a | n/a | n/a | n/a |
| R11–R12 | AG 48 / Model #787 | n/a | n/a | n/a | n/a | n/a | n/a |
| R13–R14 | IRC § 7702 / § 7702A | n/a | n/a | n/a | n/a | n/a | n/a |
| R15 | IRC § 817 (variable contracts) | | | x | x | | |
| R16 | IRC § 807 (tax reserves) | x | x | x | x | x | x |
| R17–R19 | 2017 CSO / 2015 VBT / ILEC | n/a | n/a | n/a | n/a | n/a | n/a |
| R20–R22 | Life persistency / post-level term | n/a | n/a | n/a | n/a | n/a | n/a |
| R23 | AAA VM-20 practice note | n/a | n/a | n/a | n/a | n/a | n/a |
| R24 | AAA illustrations practice note | n/a | n/a | n/a | n/a | n/a | n/a |
| R25 | AAA PBR assumptions resource manual | (x) | (x) | (x) | (x) | (x) | (x) |
| R26 | ASOP 2 (nonguaranteed elements) | x | x | x | x | | |
| R27 | ASOP 7 (cash flow analysis) | x | x | x | x | x | x |
| R28 | ASOP 15 (dividends) | (x) | (x) | (x) | (x) | (x) | (x) |
| R29 | ASOP 22 (asset adequacy opinions) | x | x | x | x | x | x |
| R30 | ASOP 24 (illustrations) | n/a | n/a | n/a | n/a | n/a | n/a |
| R31 | ASOP 52 (PBR — life products only) | n/a | n/a | n/a | n/a | n/a | n/a |
| R32 | ASOP 56 (modeling) | x | x | x | x | x | x |
| R33 | NAIC AP&P Manual | x | x | x | x | x | x |
| R34 | FASB ASU 2018-12 (LDTI) | x | x | x | x | x | x |
| R35 | VM-21 (variable annuity PBR) | (x) | (x) | x | x | | |
| R36 | VM-22 (non-variable annuity PBR) | x | x | (x) | | x | x |
| R37 | VM-V § 1 (income annuity valuation rates) | x | | | | x | x |
| R38 | AG 43 (CARVM for variable annuities) | | | x | x | | |
| R39 | AG 33 (CARVM, elective benefits) | x | x | | | | |
| R40 | AG 35 (CARVM, equity indexed) | (x) | x | | | | |
| R41 | VM-C actuarial guideline index | x | x | | | x | x |
| R42 | Model #805 (deferred annuity nonforfeiture) | x | x | n/a | (x) | n/a | n/a |
| R43 | Model #250 (Variable Annuity Model Reg) | | | x | x | n/a | |
| R44 | AG 54 (ILVA nonforfeiture) | | | (x) | x | | |
| R45 | Model #245 (annuity disclosure / illustrations) | x | x | (x) | (x) | (x) | (x) |
| R46 | Model #275 (suitability / best interest) | x | x | x | x | x | x |
| R47 | C-3 Phase II RBC instructions | | | x | x | | |
| R48 | Oliver Wyman QIS II (VA reform) | | | x | x | | |
| R49 | SEC RILA / Form N-4 final rule (2024) | (x) | | x | x | | |
| R50 | SEC Rule 498A adopting release (2020) | | | x | (x) | | |
| R51 | 17 C.F.R. § 230.498A | | | x | x | | |
| R52 | SEC Form N-4 | | | x | x | | |
| R53 | CRS R40656 (Rule 151A / § 989J) | | x | | (x) | | |
| R54 | FINRA Rule 2330 | | | x | (x) | | |
| R55 | IRC § 72 | x | x | x | x | x | x |
| R56 | IRC § 1035 | x | x | x | x | (x) | (x) |
| R57 | Treas. Reg. § 1.401(a)(9)-6 (QLAC) | (x) | (x) | | | x | x |
| R58 | T.D. 10001 (RMD final regs, 2024) | (x) | (x) | (x) | | x | x |
| R59 | Model #821 + VM-M annuity mortality | (x) | (x) | x | | x | x |
| R60 | 2012 IAR development report | (x) | (x) | (x) | | x | x |
| R61 | 2020–24 payout annuity mortality study | (x) | (x) | (x) | | x | x |
| R62 | FIA policyholder behavior studies | (x) | x | | | | |
| R63 | Fixed rate deferred surrender studies | x | | | | | |
| R64 | VA behavior / GLB utilization studies | | (x) | x | x | | |
| R65 | SOA annuity experience studies index | x | x | x | x | x | x |
| R66 | AAA VM-21 practice note supplement | | | x | x | | |
| R67 | AAA GLB utilization resource guide | (x) | (x) | x | x | | |
| R68 | AAA FIA product mechanics paper | (x) | x | | (x) | | |
| R69 | AAA ILVA / RILA policy paper | | | (x) | x | | |
| R70 | ASOP 54 (pricing) | x | x | x | x | x | x |
| R71 | ASOP 10 (U.S. GAAP long-duration) | x | x | x | x | x | x |
| R72 | IRS LB&I § 807 directive [unverified] | | | x | | | |

**Notes on Matrix B**

- **Life-only rows (`n/a` throughout)** are listed to prevent mis-application, not as
  filler. In particular: annuity nonforfeiture runs through Model #805 (R42) and, for
  variable and index-linked contracts, Model #250 § 7 (R43) and AG 54 (R44) — never Model
  #808 (R2); annuity illustrations run through Model #245 (R45), so **do not reuse AG 49 /
  AG 49-A logic (R8–R10) for FIA illustrations**; annuitant longevity uses R59–R61, never
  the CSO/VBT/ILEC life tables (R17–R19); annuity surrender behavior uses R62–R64, not the
  life persistency and post-level-term studies (R20–R22); and **ASOP 52 (R31) is scoped to
  VM-20 life products — there is no annuity-PBR ASOP** covering VM-21 or VM-22.
- **R5:** not applicable to annuities; the interest-indexed-UL provisions are the structural
  analogue of FIA crediting mechanics and are useful for a shared crediting-engine design
  [unverified as to any direct annuity effect].
- **R25:** an assumption-governance framework written for life PBR but directly transferable
  to VM-21/VM-22 assumption setting and documentation [unverified as to explicit annuity
  scope].
- **R28:** titled to include annuities, but relevant only to participating annuity forms —
  rare in the individual market [unverified as to current market relevance].
- **R29:** binding in part because AG 35 expressly requires equity-indexed annuity reserves
  to be asset-adequacy tested [R40], and because SPIA/MYGA/FIA blocks are the classic
  cash-flow-testing exposures.
- **R35:** the deferred-annuity marks are qualified because VM-21's scope includes a
  catch-all for any contract carrying GMDB/VAGLB-like guarantees that has no other explicit
  reserve requirement [R35].
- **R36:** excludes variable annuities (VM-21 governs), but the fixed account of a VA and
  the fixed payout stream after a VA's funds are exhausted fall into VM-22 Reserving
  Categories [R36].
- **R42:** does **not** apply to a RILA if and only if AG 54 (R44) is satisfied; a
  non-compliant ILVA is not a variable annuity and falls back under Model #805 [R44].
- **R43:** § 7.A expressly excludes immediate annuities and deferred annuities already in
  payout [R43].
- **R59 / R60 / R61:** the deferred-annuity and variable-annuity marks are for the
  annuitization and GLWB payout phases; VM-21 prescribes percentages of the 2012 IAM Basic
  Table with Scale G2 for prudent-estimate mortality on contracts with VAGLBs and roll-up
  GMDBs [R35].

---

## 1. NAIC statutory framework — valuation, nonforfeiture, illustrations, actuarial guidelines

### R1. Standard Valuation Law (Model #820)
- **Publisher:** National Association of Insurance Commissioners (NAIC)
- **URL:** https://content.naic.org/sites/default/files/model-law-820.pdf
- **Accessed:** 2026-08-03
- **Fetched:** yes (27-page PDF retrieved and read)
- **Annotation:** The enabling statute for statutory reserve valuation: minimum
  standards by calendar year of issue, the Commissioners Reserve Valuation Method
  (CRVM), and deficiency-reserve treatment when the valuation net premium exceeds the
  gross premium, plus — via the 2009 amendments — the sections creating principle-based
  reserving (Sections 11–14: Valuation Manual applicability, requirements of a
  principle-based valuation, experience reporting, confidentiality) [R1]. It is the
  legal root of every statutory reserve a projection model must reproduce, for all six
  products. The Valuation Manual operative date was January 1, 2017 [unverified —
  widely documented but not stated in this print].

### R2. Standard Nonforfeiture Law for Life Insurance (Model #808)
- **Publisher:** NAIC
- **URL:** https://content.naic.org/sites/default/files/model-law-808.pdf
- **Accessed:** 2026-08-03
- **Fetched:** yes (13-page PDF retrieved and read)
- **Annotation:** Sets minimum cash surrender values and paid-up nonforfeiture
  benefits: the 60-day default/election mechanics, the adjusted-premium method
  (ordinary/industrial variants and the nonforfeiture net level premium method),
  treatment of indeterminate premium plans, and the required smooth progression of cash
  values by duration [R2]. An implementer needs this for whole life's guaranteed CSV
  scale and for why long-duration guaranteed-premium term may generate nonforfeiture
  values; UL/IUL/VUL nonforfeiture is instead governed via Model #585's UL-specific
  adaptation (R5). This 2014 print ties its definitions to the Valuation Manual
  operative date [R2]; minimum nonforfeiture mortality/interest for new issues now
  comes through VM-02 (R3).

### R3. Valuation Manual, Jan. 1, 2026 Edition (VM-01, VM-02, VM-20, VM-31, VM-M, VM-G, VM-C, VM-V, …)
- **Publisher:** NAIC
- **URL:** https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf
- **Accessed:** 2026-08-03
- **Fetched:** yes (457-page PDF retrieved; cover, adoption history, and full table of contents read; "NAIC Adoptions through August 13, 2025")
- **Annotation:** The operative rulebook for statutory valuation of new business. For a
  cash-flow-model implementer the load-bearing sections are VM-20 (life PBR — the net
  premium reserve floor plus deterministic and stochastic reserves, with
  exclusion/exemption tests), VM-31 (the PBR Actuarial Report the model output must
  feed), VM-02 (minimum nonforfeiture mortality and interest), and appendices VM-M
  (mortality tables), VM-V (statutory maximum valuation interest rates for formulaic
  reserves), and VM-C (actuarial guidelines incorporated as an appendix) [R3].
  **Caution:** this edition's table of contents contains **no VM-05 section** — a
  full-text search of the PDF finds no "VM-05" at all [R3]; earlier editions (e.g.,
  2016) did reproduce the SVL as VM-05 [unverified] — use Model #820 (R1) directly for
  the statute.

### R4. Life Insurance Illustrations Model Regulation (Model #582)
- **Publisher:** NAIC
- **URL:** https://content.naic.org/sites/default/files/model-law-582.pdf
- **Accessed:** 2026-08-03
- **Fetched:** yes (14-page PDF retrieved and read)
- **Annotation:** Governs sales illustrations for group and individual life policies
  **except** variable life, annuities, credit life, and policies with illustrated death
  benefits of $10,000 or less [R4]. The modeling-relevant machinery is the disciplined
  current scale and the self-support and lapse-support tests certified annually by an
  illustration actuary (the tests are defined in the regulation's standards and in
  ASOP 24, R30) [R4][unverified as to section numbering detail]. IUL-specific rate
  limits are layered on top by the AG 49 family (R8–R10).

### R5. Universal Life Insurance Model Regulation (Model #585)
- **Publisher:** NAIC
- **URL:** https://content.naic.org/sites/default/files/model-law-585.pdf
- **Accessed:** 2026-08-03
- **Fetched:** yes (14-page PDF retrieved and read)
- **Annotation:** Adapts the life-insurance regulatory framework to flexible-premium
  designs: definitions (flexible vs. fixed premium UL, interest-indexed UL), valuation
  (Section 5), nonforfeiture (Section 6), mandatory policy provisions, the periodic
  (annual) statement to policyowners, and extra requirements for interest-indexed UL
  [R5]. This is where the UL-pattern mechanics a model must honor — account value
  roll-forward disclosure, maturity/nonforfeiture treatment — get their regulatory
  definition. Drafting notes state it applies to individual UL except variable UL
  [R5 per NAIC search summary; scope section read]; VUL is carved out into
  variable-products rules and federal securities law.

### R6. Valuation of Life Insurance Policies Model Regulation (Model #830, "Regulation XXX")
- **Publisher:** NAIC
- **URL:** https://content.naic.org/sites/default/files/model-law-830.pdf
- **Accessed:** 2026-08-03
- **Fetched:** yes (35-page PDF retrieved and read; print: October 2009; regulation adopted March 1999 [R7])
- **Annotation:** The pre-PBR reserve regime for term and secondary-guarantee UL, still
  operative for in-force blocks issued before PBR: tables of select mortality factors
  and rules for their use, Section 6 minimum standards for plans with guaranteed
  nonlevel gross premiums or nonlevel benefits (level-term segmentation — the "XXX"
  term reserves), and Section 7 minimum standards for UL with secondary guarantees
  ("AXXX" reserves) [R6]. Basic reserves under this regulation constitute CRVM for the
  policies in scope [R6]. Its conservatism drove captive reserve financing — hence
  AG 48 (R11) and Model #787 (R12).

### R7. Actuarial Guideline XXXVIII — The Application of the Valuation of Life Insurance Policies Model Regulation (AG 38)
- **Publisher:** NAIC (PDF circulated with the NAIC CIPR newsletter, December 2012)
- **URL:** https://content.naic.org/sites/default/files/inline-files/cipr_ag38_121212.pdf
- **Accessed:** 2026-08-03
- **Fetched:** yes (13-page PDF retrieved and read; confirmed it contains the 2012 revision Sections 8D/8E and the pre-July-2005 / pre-2013 / post-2013 issue-date splits)
- **Annotation:** Interprets Model #830 for products designed around it — above all
  ULSG with shadow accounts — on the principle that reserves must be established for
  the guarantees a policy actually provides, enumerating product designs and the
  reserving approach for each; the 2012 revisions (8D/8E) set separate standards for
  pre-2013 in-force ULSG versus post-2013 issues [R7]. Original guideline created 2003,
  revised 2005 and 2012 [unverified — consistent with the 2012 text but history stated
  from secondary sources]. The official current text lives in the NAIC AP&P Manual
  Appendix C / VM-C [R3][unverified as to AP&P pagination]. Fetch note: the NAIC CIPR
  topic page for AG 38 returned HTTP 403 to automated fetch.

### R8. Actuarial Guideline XLIX (AG 49, original 2015; amended 2016)
- **Publisher:** NAIC
- **URL:** none verified — no official standalone copy of the *original* AG 49 text was
  located on content.naic.org (only a 2019 exposure redline:
  https://content.naic.org/sites/default/files/inline-files/AG%2049%20-%202019%20edits%20-%201st%20exposure.pdf,
  not fetched); official text is in the AP&P Manual Appendix C / VM-C
- **Accessed:** 2026-08-03 (search date; document not fetched)
- **Fetched:** no (link failure disclosed; see R9/R10 for fetched successors and history)
- **Annotation:** First uniform limits on illustrated IUL crediting rates under Model
  #582: a Benchmark Index Account (BIA) whose lookback average caps the illustrated
  scale, plus limits on illustrated policy-loan leverage and disciplined-current-scale
  earned-rate limits [R9][R10]. Adopted 2015, applying to policies sold on/after
  Sept. 1, 2015 [R9 per SOA article; date detail unverified]; superseded for new sales
  by AG 49-A for policies sold on/after Dec. 14, 2020 (R10). Still needed for in-force
  illustrations of pre-2021 IUL sales.

### R9. "Actuarial Guideline XLIX (AG49): Past, Present and Future" (SOA Product Matters!, June 2023)
- **Publisher:** Society of Actuaries, Product Development Section newsletter
- **URL:** https://www.soa.org/sections/product-dev/product-dev-newsletter/2023/june/pm-2023-06-hoffer/
- **Accessed:** 2026-08-03
- **Fetched:** yes
- **Annotation:** Practitioner article (secondary source) tracing the three rounds of
  IUL illustration guidance: AG 49 (2015) capping illustrated index credits via the
  benchmark account; AG 49-A (2020) eliminating illustrated leverage from multipliers
  and fixed bonuses (charges funding enhancements must offset illustrated benefit
  equally); and the 2023 "quick fix" (industry shorthand "AG 49-B") stopping
  volatility-controlled-index hedge-cost savings from funding bonuses that
  out-illustrate the benchmark [R9]. Explains why an IUL illustrated-scale module must
  be version-dependent by sale date.

### R10. Actuarial Guideline XLIX-A — The Application of the Life Illustrations Model Regulation to Policies with Index-Based Interest Sold On or After December 14, 2020 (as revised; the "AG 49-B" changes)
- **Publisher:** NAIC (adopted by LATF 12/11/2022; adopted by Life Insurance and Annuities (A) Committee 2/24/2023)
- **URL:** https://content.naic.org/sites/default/files/committees-pending-action-actuarial-guideline-xlix-a-230224.pdf
- **Accessed:** 2026-08-03
- **Fetched:** yes (6-page PDF retrieved and read)
- **Annotation:** The operative IUL illustration guideline: caps the illustrated annual
  rate of index credits by reference to the Benchmark Index Account, limits illustrated
  policy-loan leverage, and requires a side-by-side alternate-scale illustration plus
  added disclosures [R10]. This print embeds the 2023 revisions — tighter limits for
  non-BIA index accounts for policies sold on/after May 1, 2023 (the change the
  industry calls "AG 49-B") [R10]. The NAIC formally adopted these as revisions to
  AG 49-A rather than a separately numbered guideline; treat "AG 49-B" as a colloquial
  label [R9][R10].

### R11. Actuarial Guideline XLVIII — Actuarial Opinion and Memorandum Requirements for the Reinsurance of Policies Required to be Valued under Sections 6 and 7 of the NAIC Valuation of Life Insurance Policies Model Regulation (AG 48)
- **Publisher:** NAIC (LATF adoption 12/1/2016 revision print)
- **URL:** https://content.naic.org/sites/default/files/inline-files/committees_ex_pbr_implementation_tf_related_actuarial_guideline_ag48.pdf
- **Accessed:** 2026-08-03
- **Fetched:** yes (12-page PDF retrieved and read)
- **Annotation:** Response to XXX/AXXX captive reserve financing: the appointed actuary
  must issue a **qualified** opinion if the ceding insurer (or its holding-company
  system) has a XXX/AXXX reserve-financing arrangement that does not hold the Required
  Level of Primary Security, computed by the prescribed Actuarial Method, in qualifying
  Primary Security assets [R11]. Original AG 48 effective Jan. 1, 2015 [R11]; sunsets
  operationally into Model #787 (R12) as states adopt it [unverified]. Relevant to a
  model's reinsurance/collateral module for reserve-financed term and ULSG blocks, not
  to base cash flows.

### R12. Term and Universal Life Insurance Reserve Financing Model Regulation (Model #787)
- **Publisher:** NAIC
- **URL:** https://content.naic.org/sites/default/files/model-law-787.pdf
- **Accessed:** 2026-08-03
- **Fetched:** yes (10-page PDF retrieved and read; print: Model Regulation Service, 1st Quarter 2017)
- **Annotation:** Codifies the AG 48 framework as a regulation under the Credit for
  Reinsurance Model Law: uniform national standards for reserve-financing reinsurance
  of policies with guaranteed nonlevel gross premiums/benefits (XXX term) and ULSG
  (AXXX), requiring Primary Security and Other Security in prescribed forms and
  amounts, with an Actuarial Method for the required level, remediation mechanics, and
  an anti-avoidance prohibition [R12]. Reinsurance/reserve-financing side only.

---

## 2. Federal tax — product qualification and insurer tax

Historical note [unverified, brief]: the definitional regime arrived in stages — TEFRA
(1982) first imposed temporary corridor/guideline rules for flexible-premium contracts
(former IRC 101(f)); DEFRA (1984) enacted IRC 7702 for all life contracts; TAMRA (1988)
added IRC 7702A's MEC/7-pay regime to curb single-premium tax shelters. The 2021
Consolidated Appropriations Act change is verified at [R13].

### R13. 26 U.S.C. § 7702 — Life insurance contract defined
- **Publisher:** Legal Information Institute, Cornell Law School (U.S. Code)
- **URL:** https://www.law.cornell.edu/uscode/text/26/7702
- **Accessed:** 2026-08-03
- **Fetched:** yes
- **Annotation:** The federal definition of life insurance: a contract must pass either
  the cash value accumulation test (CVAT — CSV may not exceed the net single premium
  for future benefits) or the guideline premium test plus cash value corridor (GPT/CVC)
  [R13]. Subsection (f)(11), added by the Consolidated Appropriations Act, 2021,
  replaces the fixed 4%/6% assumptions with the "insurance interest rate" — the lesser
  of the § 7702 valuation interest rate and the § 7702 applicable federal interest
  rate, with a 2% transition rate for 2021 issues [R13]. A product model needs CVAT/GPT
  logic to police premium limits, corridor death benefits, and funding patterns; for
  term, definitional compliance is trivial without cash value [unverified].

### R14. 26 U.S.C. § 7702A — Modified endowment contract defined
- **Publisher:** Legal Information Institute, Cornell Law School
- **URL:** https://www.law.cornell.edu/uscode/text/26/7702A
- **Accessed:** 2026-08-03
- **Fetched:** yes
- **Annotation:** A contract entered into after June 20, 1988 is a MEC if cumulative
  premiums in the first seven contract years exceed the 7-pay net level premiums, or if
  received in exchange for a MEC [R14]. Material changes restart the 7-pay test (with a
  cash-value adjustment); benefit reductions within the first seven years apply
  retroactively; exclusions exist (e.g., death benefit increases funded by the
  lowest-level death benefit premiums, reinstatement within 90 days) [R14]. MEC status
  changes distribution taxation (LIFO + penalty) [unverified], so illustration and
  in-force systems must test it continuously against funding patterns (WL paid-up
  additions riders; UL/IUL/VUL premium flexibility).

### R15. 26 U.S.C. § 817 — Treatment of variable contracts (esp. § 817(h) diversification)
- **Publisher:** Legal Information Institute, Cornell Law School
- **URL:** https://www.law.cornell.edu/uscode/text/26/817
- **Accessed:** 2026-08-03
- **Fetched:** yes
- **Annotation:** § 817(h): a variable contract based on a segregated asset account is
  not treated as life insurance/annuity unless the account is "adequately diversified"
  per Treasury regulations; safe harbor if it satisfies § 851(b)(3) with no more than
  55% in one issuer or group of related issuers, with look-through rules for
  insurance-dedicated funds and a Treasury-securities special rule [R15]. For a VUL
  model this is background (fund eligibility), not cash-flow mechanics.

### R16. 26 U.S.C. § 807 — Rules for certain reserves (tax reserves)
- **Publisher:** Legal Information Institute, Cornell Law School
- **URL:** https://www.law.cornell.edu/uscode/text/26/807
- **Accessed:** 2026-08-03
- **Fetched:** yes
- **Annotation:** Post-TCJA (tax years beginning after Dec. 31, 2017), the life
  insurance tax reserve is the greater of the contract's net surrender value and 92.81%
  of the reserve computed under the NAIC-prescribed method (CRVM for life, CARVM for
  annuities), capped at the statutory reserve [R16]. Discounting uses the highest rates
  permitted by the NAIC as of the determination date, and § 807(e)(6) requires reserve
  reporting [R16]. This is why a statutory VM-20/CRVM engine is also the natural source
  for a model's tax-reserve output (see group 6).

---

## 3. Mortality tables and experience studies

### R17. 2017 Commissioners Standard Ordinary (CSO) Tables
- **Publisher:** Society of Actuaries (developed jointly with the American Academy of Actuaries for NAIC adoption [unverified])
- **URL:** https://www.soa.org/resources/experience-studies/2015/2017-cso-tables/
- **Accessed:** 2026-08-03
- **Fetched:** yes (landing page; the linked development-report PDF at
  https://www.soa.org/globalassets/assets/files/research/exp-study/research-2017-cso-report.pdf
  was not separately fetched)
- **Annotation:** The statutory valuation/nonforfeiture mortality basis for new issues:
  loaded and unloaded composite, smoker-distinct, and preferred-structure tables, plus
  gender-blended and ultimate variants, each in ANB/ALB forms [R17]. Prescribed via
  VM-20/VM-M for the net premium reserve and used in nonforfeiture calculations for
  post-2017 issues [R3][unverified as to exact VM-M table numbers]. Developed from ILEC
  experience showing significant mortality improvement over the 2001 CSO basis and
  adding a preferred structure [search summary; development detail in the linked
  report].

### R18. 2015 Valuation Basic Table (VBT) — Report and Tables
- **Publisher:** Society of Actuaries
- **URL:** https://www.soa.org/resources/experience-studies/2015/2015-valuation-basic-tables/
- **Accessed:** 2026-08-03
- **Fetched:** yes (landing page; the linked report PDF at
  https://www.soa.org/globalassets/assets/Files/resources/experience-studies/2018/2015-vbt-report.pdf
  — report updated Sept. 2018 — was not separately fetched)
- **Annotation:** The industry experience (unloaded) basis underlying the 2017 CSO:
  primary tables (male/female, smoker/nonsmoker, composite; ANB/ALB) plus 10 nonsmoker
  and 4 smoker Relative Risk (RR) tables for preferred-class fit, with preferred
  wear-off and mortality-improvement factors in appendices, built on 2009–2013 ILEC
  individual life experience [R18]. In VM-20, company prudent-estimate mortality is
  credibility-blended toward industry tables of this family [R3][unverified as to
  current VM-prescribed VBT vintage]. The anchor for best-estimate/prudent-estimate
  mortality in PBR and pricing models.

### R19. 2019 Individual Life Insurance Mortality Experience Report (ILEC, observation years 2012–2019)
- **Publisher:** Society of Actuaries Research Institute — Individual Life Experience Committee (ILEC)
- **URL:** https://www.soa.org/resources/research-reports/2024/ilec-mort-2012-19
- **Accessed:** 2026-08-03
- **Fetched:** yes (landing page; published Oct. 2024; the main report PDF at
  https://www.soa.org/globalassets/assets/files/resources/research-report/2024/ilec-mort-main.pdf
  was not separately fetched)
- **Annotation:** The latest full ILEC mortality study: actual-to-expected experience
  for 2012–2019 against standard industry tables, with trends by key policy
  characteristics, plus underlying data as pivot tables, text files, and Tableau
  dashboards [R19]. Data collection shifted from MIB (2012–17) to the NAIC as
  statistical agent (2018 on) [R19]. The A/E expected basis includes the 2015 VBT
  [search summary; stated expected basis 2015 VBT RR100 — noted on the report itself,
  not the landing page]. The source for mortality assumption setting and VM-20
  experience justification.

### R20. U.S. Individual Life Insurance Persistency Update (LIMRA/SOA, observation years 2009–2013)
- **Publisher:** LIMRA and Society of Actuaries (joint study)
- **URL:** https://www.soa.org/resources/research-reports/2019/2009-13-us-ind-life-persistency-update/
- **Accessed:** 2026-08-03
- **Fetched:** yes (landing page)
- **Annotation:** Lapse experience for whole life, term, UL, and VUL plans issued
  1918–2012, from 16 companies, with analysis by major policy/product factors,
  joint-life plans, and a detailed look at UL with secondary guarantees [R20]. The
  standard public source for base lapse assumptions by product, duration, premium mode,
  and size band [R20][unverified as to full factor list]. The successor UL-focused
  study is R21; older editions (2003–04 through 2007–09) remain on soa.org.

### R21. 2015–2021 Universal Life Premium Persistency and Lapse/Surrender Experience Study
- **Publisher:** LIMRA and SOA Research Institute (joint)
- **URL:** https://www.soa.org/resources/experience-studies/2024/15-21-ulpp-ulls/
- **Accessed:** 2026-08-03
- **Fetched:** yes (landing page)
- **Annotation:** Two-part flexible-premium UL study for calendar years 2015–2021:
  premium persistency (14 companies, ~50% of flexible-premium UL new-sales share,
  11.9M policy-years, ~$4.0T face exposure) and lapse/surrender (24 companies, ~80% of
  market, ~33.5M policy-years, 1.3M lapse terminations) [R21]. Directly relevant to
  modeling flexible-premium payment behavior — the assumption unique to UL-type
  products — and modern surrender bases; VUL by analogy. The landing page does not
  break out IUL/VUL separately [R21].

### R22. U.S. Post-Level Term Lapse and Mortality Experience Report (2021)
- **Publisher:** Society of Actuaries (research by SCOR: Bradfield, Covington, Reppert, Tomas)
- **URL:** https://www.soa.org/resources/experience-studies/2021/us-post-level-term-lapse-mortality/
- **Accessed:** 2026-08-03
- **Fetched:** yes (landing page)
- **Annotation:** The current study of shock lapse at the end of the level premium
  period, post-level-term (PLT) lapse, and PLT mortality deterioration — the
  anti-selection that dominates late-duration term cash flows [R22]. Updates the 2010
  and 2014 PLT studies; a predictive-modeling companion report exists, and an
  ILEC/LIMRA update covering 2009–2024 experience is in progress (data request issued
  2025) [R22][search summaries]. Essential for term models with post-level premium
  structures (jump-to-ART, graded).

---

## 4. American Academy of Actuaries — practice notes

### R23. Life Principle-Based Reserves (PBR) Under VM-20 — Practice Note (April 2020)
- **Publisher:** American Academy of Actuaries, Life Principle-Based Approach Practice Note Work Group (Life Valuation Committee)
- **URL:** https://www.actuary.org/sites/default/files/2020-04/VM-20_PN_2020_Version_0.pdf (301-redirects to http://actuary.org/…; same path)
- **Accessed:** 2026-08-03
- **Fetched:** yes (115-page PDF retrieved and read; title page and front matter verified)
- **Annotation:** Q&A-format guidance on implementing VM-20: scope/exemptions, the net
  premium reserve, deterministic and stochastic reserves, prudent-estimate assumption
  setting (mortality credibility, lapse, premium persistency), asset modeling and
  reinvestment, exclusion tests, and the reporting interplay with VM-31 [R23 front
  matter; topic list partly [unverified] — not every chapter was read]. Explicitly not
  an ASB promulgation and not binding [R23]. The implementation companion to R3 and
  ASOP 52 (R31); updates the 2017 edition for VM changes since the 12/31/2019
  valuation [search summary].

### R24. Life Insurance Illustrations: Application of the NAIC Life Insurance Illustrations Model Regulation and ASOP No. 24 — Practice Note (September 2021)
- **Publisher:** American Academy of Actuaries, Life Illustrations Work Group
- **URL:** https://actuary.org/wp-content/uploads/2021/09/Life_Illustrations_Practice_Note_Update.pdf
- **Accessed:** 2026-08-03
- **Fetched:** yes (137-page PDF retrieved and read; title page verified)
- **Annotation:** Practitioner Q&A on illustration-actuary work under Model #582 and
  ASOP 24: disciplined current scale development, self-support and lapse-support
  testing, certification practice, and application to indexed products under the AG 49
  family [R24 title/front matter; detailed topic list partly [unverified]]. The
  companion to R4/R30 for building illustration logic into product models. Not
  applicable to VUL (outside Model #582 scope [R4]).

### R25. Life Principle-Based Reserves (PBR) Assumptions Resource Manual (January 2019)
- **Publisher:** American Academy of Actuaries, PBR Assumptions Resource Manual Work Group (Life Practice Council)
- **URL:** https://www.actuary.org/sites/default/files/files/publications/PBR_Assumptions_Resource_Manual_012919.pdf (301-redirects to http://actuary.org/…; same path)
- **Accessed:** 2026-08-03
- **Fetched:** yes (86-page PDF retrieved and read; title page verified)
- **Annotation:** "An actuary's step-by-step sample framework for setting, updating,
  and governing life insurance assumptions for PBR and other valuation frameworks"
  [R25] — assumption governance, documentation, and update-cycle patterns that a model
  library's assumption architecture can mirror. Non-binding, non-ASB [R25]. Especially
  useful for ULSG/term assumption governance.
- **Note on UL practice notes:** no current standalone Academy "universal life"
  practice note was located on actuary.org (search performed 2026-08-03); UL-specific
  practice content lives in R23–R25, ASOP 2 (R26), and the illustration materials. The
  Academy's practice-note index is at https://actuary.org/practice-notes/ (not
  fetched).

---

## 5. Actuarial Standards of Practice (ASB)

Current numbers/titles verified against the ASB standards list (fetched 2026-08-03).

### R26. ASOP No. 2 — Nonguaranteed Elements for Life Insurance and Annuity Products
- **Publisher:** Actuarial Standards Board
- **URL:** https://www.actuarialstandardsboard.org/asops/asop-no-2-nonguaranteed-elements-for-life-insurance-and-annuity-products/
- **Accessed:** 2026-08-03
- **Fetched:** yes (adopted Sept. 2021; effective June 1, 2022)
- **Annotation:** Governs determination (and support of illustration) of nonguaranteed
  elements — credited rates, COI charges, expense loads, indeterminate premiums — for
  individual life and annuity forms where NGEs vary at insurer discretion, including UL
  and indeterminate-premium life [R26]. Excludes dividends (ASOP 15, R28) and
  illustrations under ASOP 24 (R30) [R26]. Defines the determination-policy/framework
  discipline a model's NGE re-rating logic should reflect.

### R27. ASOP No. 7 — Life or Health Cash Flow Analysis
- **Publisher:** Actuarial Standards Board
- **URL:** https://www.actuarialstandardsboard.org/asops/life-or-health-cash-flow-analysis/
- **Accessed:** 2026-08-03
- **Fetched:** yes (revision adopted December 2025; effective June 1, 2026)
- **Annotation:** The revised cash-flow-analysis standard (successor to "Analysis of
  Life, Health, or Property/Casualty Insurer Cash Flows"; P/C content moved to ASOP 20)
  [R27]. Applies to actuaries analyzing life/health cash flow risks — the general
  standard for asset/liability cash flow projection work of exactly the kind a
  reference model performs [R27]. Pairs with ASOP 22 (R29) for opinions and ASOP 56
  (R32) for model governance.

### R28. ASOP No. 15 — Dividends for Individual Participating Life Insurance, Annuities, and Disability Insurance
- **Publisher:** Actuarial Standards Board
- **URL:** https://www.actuarialstandardsboard.org/asops/dividends-individual-participating-life-insurance-annuities-disability-insurance/
- **Accessed:** 2026-08-03
- **Fetched:** yes (adopted March 2006; effective Aug. 1, 2006)
- **Annotation:** Guidance on establishing/modifying dividend frameworks and
  determining/illustrating dividends for individual participating business (stock,
  mutual, fraternal), including participating riders [R28]. Excludes divisible-surplus
  aggregate determination and ASOP-24 illustration compliance [R28]. The
  contribution-principle mechanics behind a par whole life model's dividend module (and
  par riders on other products).

### R29. ASOP No. 22 — Statements of Actuarial Opinion Based on Asset Adequacy Analysis for Life Insurance, Annuity, or Health Insurance Reserves and Other Liabilities
- **Publisher:** Actuarial Standards Board
- **URL:** https://www.actuarialstandardsboard.org/asops/asop-no-22-statements-of-actuarial-opinion-based-on-asset-adequacy-analysis-for-life-insurance-annuity-or-health-insurance-reserves-and-other-liabilities/
- **Accessed:** 2026-08-03
- **Fetched:** yes (adopted Sept. 2021; effective June 1, 2022)
- **Annotation:** Standard for the appointed actuary's asset adequacy opinion under the
  SVL/VM-30 framework (and analogous law) [R29]. Cash flow testing is the dominant
  technique [unverified — the standard admits multiple methods]; a liability projection
  model that will feed AAT/CFT must satisfy this standard's analysis and documentation
  expectations, alongside ASOP 7 (R27) and ASOP 56 (R32). Applies at the company/block
  level for all products (ULSG and long-duration guarantees are typical stress points
  [unverified]).

### R30. ASOP No. 24 — NAIC Life Insurance Illustrations Model Regulation
- **Publisher:** Actuarial Standards Board
- **URL:** https://www.actuarialstandardsboard.org/asops/asop-24-naic-life-insurance-illustrations-model-regulation-024-217/
- **Accessed:** 2026-08-03
- **Fetched:** yes (standard's page; Doc. No. 217; the PDF at
  https://www.actuarialstandardsboard.org/wp-content/uploads/2024/09/asop024_217.pdf
  was not separately fetched)
- **Annotation:** Applies when actuaries certify that illustrated scales comply with
  Model #582 or with AG 49/AG 49-A [R30]. Covers illustrated-scale work only;
  currently-payable-scale determination belongs to ASOP 2 (R26) and ASOP 15 (R28)
  [R30]. The revision adopted September 2024 (effective December 1, 2024) is the
  current edition — it postdates and reflects the indexed-product guidelines [R30].

### R31. ASOP No. 52 — Principle-Based Reserves for Life Products under the NAIC Valuation Manual
- **Publisher:** Actuarial Standards Board
- **URL:** https://www.actuarialstandardsboard.org/asops/principle-based-reserves-life-products-naic-valuation-manual/
- **Accessed:** 2026-08-03
- **Fetched:** yes (adopted Sept. 2017; effective Dec. 31, 2017)
- **Annotation:** Standard for actuaries calculating or reviewing VM-20 reserves,
  extending to any actuary participating in the principle-based methodology [R31].
  Notably, if the standard conflicts with the operative Valuation Manual, "the
  provisions of the Valuation Manual shall govern" [R31]. Sets expectations on
  assumptions, margins, model granularity, and documentation that flow into VM-31
  reporting for all VM-20 products.

### R32. ASOP No. 56 — Modeling
- **Publisher:** Actuarial Standards Board
- **URL:** https://www.actuarialstandardsboard.org/asops/modeling-3/
- **Accessed:** 2026-08-03
- **Fetched:** yes (adopted Dec. 2019; effective Oct. 1, 2020)
- **Annotation:** Cross-practice standard for designing, developing, selecting,
  modifying, using, reviewing, or evaluating models where reliance on model output has
  a material effect [R32 scope; component list partly [unverified]]. The governing
  standard for the reference implementation itself: intended purpose, model-risk
  mitigation, validation/testing, reliance on others' models and data, and
  documentation [R32].

---

## 6. Accounting frameworks — why one cash flow model serves several bases

### R33. NAIC Accounting Practices and Procedures Manual (statutory basis)
- **Publisher:** NAIC
- **URL:** https://content.naic.org/publications
- **Accessed:** 2026-08-03
- **Fetched:** yes (publications page describing the manual; the manual itself is a paid publication and was not fetched)
- **Annotation:** The AP&P Manual "includes all statutory accounting guidance that has
  been adopted by the NAIC as of March of the current year," including appendices with
  excerpts of applicable model laws, working-group interpretations, **actuarial
  guidelines** (Appendix C — where AG 38/48/49 officially live), and
  financial-reporting implementation guidance; updated annually [R33]. Statutory
  accounting is the conservative, solvency-oriented frame in which Models 820/830, the
  Valuation Manual, and the AGs operate; a liability model's statutory outputs
  (reserves, nonforfeiture floors) plug into this basis.

### R34. FASB ASU No. 2018-12 — Financial Services—Insurance (Topic 944): Targeted Improvements to the Accounting for Long-Duration Contracts (LDTI)
- **Publisher:** Financial Accounting Standards Board
- **URL:** https://www.fasb.org (fasb.org blocked automated fetch — both
  https://www.fasb.org/insurance and a direct document URL returned HTTP 403; no
  working deep link is cited to avoid fabricating one. An accessible third-party full
  text is PwC Viewpoint:
  https://viewpoint.pwc.com/dt/us/en/fasb_financial_accou/asus_fulltext/2018/asu_201812financial_/asu_201812financial__US/asu_201812financial__US.html
  — fetch failed with redirect loop, likely auth-gated.)
- **Accessed:** 2026-08-03 (fetch attempts on this date; document not retrieved)
- **Fetched:** no (title, scope, and effective dates corroborated across multiple secondary sources: BDO, Deloitte, KPMG, PwC summaries via search)
- **Annotation:** ASU 2018-12 rewrote U.S. GAAP for long-duration contracts: liability
  for future policy benefits with annually reviewed cash flow assumptions and
  discounting at an upper-medium-grade (single-A) rate through OCI, market risk
  benefits at fair value, simplified DAC amortization, and greatly expanded disclosures
  [unverified — consistent across the cited summaries]. Effective for large SEC filers
  Jan. 1, 2023 (2025 for others) [search summaries]. A GAAP valuation run needs the
  same projected cash flows as statutory but different assumption update/locking,
  discounting, and amortization overlays — a key reason to separate cash flow
  projection from measurement in model architecture. Product mapping — term/WL as
  traditional LFPB; UL/IUL/VUL/ULSG as universal-life-type contracts with additional
  liabilities/SOP 03-1-style features and MRBs — is [unverified].

### Tax reserves (cross-reference R16)
IRC § 807 defines tax reserves off the NAIC-prescribed method: the greater of net
surrender value and 92.81% of the CRVM/VM-computed reserve, capped at statutory,
discounted at NAIC-permitted rates [R16]. The same statutory engine, with a scalar
haircut and cap logic, therefore produces the tax basis, while the DEFRA/TEFRA/TAMRA
definitional rules (group 2) decide whether the *contract* is life insurance at all.
Together, statutory (R33), GAAP LDTI (R34), and tax (R16) explain why a single
liability cash flow projection typically feeds at least three measurement wrappers.

---

## 7. NAIC valuation for annuities — VM-21, VM-22, and the CARVM guideline family

Entries R35–R72 support the individual annuity products. Where an annuity-specific
document is a *section of* a document already catalogued (VM-21 and VM-22 inside the
Valuation Manual, R3), a separate entry is created because annuity models cite the section
directly; the parent document is cross-referenced, not restated.

### R35. VM-21: Requirements for Principle-Based Reserves for Variable Annuities (Valuation Manual, Jan. 1, 2026 Edition)
- **Publisher:** NAIC
- **URL:** https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf (pages 21-1 to 21-79 of the 457-page PDF; same document as R3)
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; Sections 1, 2, 3 and the table of contents read in full; "NAIC Adoptions through August 13, 2025")
- **Annotation:** The statutory reserve standard for variable annuities, and it **constitutes
  CARVM** for every contract in its scope — variable deferred and variable immediate
  contracts with or without GMDB/VAGLB, group annuity contracts with similar guarantees, and
  any other contract with GMDB/VAGLB-like guarantees having no other explicit reserve
  requirement (reserved stand-alone and added to the base contract reserve) [R35].
  **Aggregate reserve = the stochastic reserve + the additional standard projection amount +
  any Alternative Methodology reserve**, where the **SR is CTE70** of the scenario reserves
  and each scenario contributes the greatest present value of accumulated deficiency from a
  stochastic asset/liability projection on prudent-estimate assumptions [R35]. Sections 9–13
  carry the machinery an implementer needs — hedges under a Clearly Defined Hedging Strategy
  (§9), contract holder behavior (§10), prudent-estimate mortality (§11), allocation of the
  aggregate reserve to contract level (§13) — and it is effective for valuation dates on or
  after Jan. 1, 2020 with an elective 36-month phase-in (extendable to seven years with
  domiciliary approval) computed as `Reserve = D − (B − A) × C / B`, plus a separate 36-month
  economic scenario generator phase-in beginning Jan. 1, 2026 for the GOES requirements in
  VM-20 Appendix 1 [R35]. Architecturally decisive: VM-21 states its projections are
  anticipated to be used for RBC and that VM-21 §§4.A–4.E and the RBC requirements are
  **identical** except for the elective federal-income-tax treatment [R35] — one projection,
  two outputs (see R47).

### R36. VM-22: Requirements for Principle-Based Reserves for Non-Variable Annuities (Valuation Manual, Jan. 1, 2026 Edition)
- **Publisher:** NAIC
- **URL:** https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf (pages 22-1 to 22-90; same document as R3)
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; Sections 1, 2, 3.A–3.F and the table of contents read in full)
- **Annotation:** In the 2026 edition VM-22 is entirely the *principle-based* framework for
  non-variable annuities and "constitute[s] the Commissioners Annuity Reserve Valuation
  Method (CARVM) and, for some contracts and certificates, the Commissioners Reserve
  Valuation Method (CRVM)"; it applies **for valuation dates on or after January 1, 2026**,
  with an elective transition allowing business issued during the first three years after the
  effective date to stay on VM-A/VM-C/VM-M/VM-V, an irrevocable election once VM-22 PBR is
  chosen for a block, and mandatory prospective application three years after the effective
  date (i.e., Jan. 1, 2029 [unverified — the text states the rule as "three years after the
  effective date"; it does not print the date]) [R36]. Aggregate reserve = SR (**CTE70**) +
  DR for contracts passing the Single Scenario Test + the reserve for contracts passing the
  exclusion test and valued under VM-A/VM-C/VM-M/VM-V; the additional standard projection
  amount is **disclosure-only** under VM-31, and a LATF referral of April 3, 2025 directs the
  VM-22 Subgroup to add attribution analysis and to reiterate that "the SPA is not a safe
  harbor," targeted at the 1/1/2027 Valuation Manual [R36]. **Reserving Categories** — which
  may not be aggregated except under §3.F.2 — are *Payout Annuity* (SPIA, DIA, structured
  settlements, annuitizations of host contracts, supplementary contracts with scheduled
  payments, Model #820 §5.C.2 certificates, pension risk transfer), *Longevity Reinsurance*,
  and *Accumulation* (everything else, including fixed income streams from guaranteed living
  benefits after account exhaustion); risks explicitly to be reflected include
  disintermediation, additional premium dump-ins under high guarantees in low-rate
  environments, annuitization risk, and GLB utilization risk [R36]. **Caution:** VM-22 was
  historically the home of maximum valuation interest rates for income annuities; in this
  edition that content is **not** in VM-22 — it is in VM-V Section 1 (R37), so a model citing
  "VM-22 income annuity interest rates" against a current Valuation Manual is citing the
  wrong section [R36][R37].

### R37. VM-V: Statutory Maximum Valuation Interest Rates for Formulaic Reserves, Section 1 — Income Annuities
- **Publisher:** NAIC
- **URL:** https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf (pages V-1 to V-3+; same document as R3)
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; §1.A Purpose and Scope and §1.B Definitions read)
- **Annotation:** Defines, for SPIAs "and other similar contracts, certificates and contract
  features," the **statutory maximum valuation interest rate complying with Model #820** —
  the maximum interest assumption for CARVM (and for some contracts CRVM) on formulaic
  annuity reserves [R37]. For issues after Dec. 31, 2017 the scope covers immediate
  annuities; **deferred income annuity contracts**; structured settlements in payout or
  deferred status; fixed payouts from settlement options or annuitizations of host contracts;
  supplementary contracts with scheduled payments; fixed income streams from **contingent
  deferred annuities** and from **guaranteed living benefits once contract funds are
  exhausted**; and Model #820 §5.C.2 group annuity certificates [R37]. It applies to
  contracts **not passing the SET covered by VM-22** — i.e., VM-V is the formulaic fallback
  where VM-22 PBR is excluded — with interest set by a "reference period" / Valuation Rate
  Bucket mechanic keyed to the premium determination date and the timing of the first
  life-contingent payment [R37]. Critically, VM-V §1 **supersedes** the interest-rate guidance
  in VM-A and VM-C, expressly including **AG IX-B** and the interest references in **AG IX-C**
  [R37].

### R38. Actuarial Guideline XLIII — CARVM for Variable Annuities (AG 43)
- **Publisher:** NAIC (this print is the VAIWG redlined working copy dated 2016-09-26, showing the 2009 text with the reform-era edits; the official text lives in the AP&P Manual Appendix C, R33)
- **URL:** https://content.naic.org/sites/default/files/inline-files/cmte_e_va_issues_wg_related_redlined_ag43_160926.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; TOC, Section I Background, Section IV Reserve Methodology, and Section V Effective Date read)
- **Annotation:** The predecessor regime to VM-21 and **still operative for in-force**,
  "codif[ying] the basic interpretation of the Commissioners Annuity Reserve Valuation Method
  (CARVM)" under the SVL for variable annuities and contracts with similar guarantees [R38].
  Reserve structure: the **Aggregate Reserve is the Standard Scenario Amount plus the excess,
  if any, of the Conditional Tail Expectation Amount over the Standard Scenario Amount** — a
  floor-plus-excess construct materially different from VM-21's SR + additional standard
  projection amount — with the CTE Amount being **CTE(70)**, the average of the largest 30% of
  scenario greatest present values of accumulated deficiency, and twelve appendices carrying
  projections, reinsurance, standard scenario, Alternative Methodology, scenario calibration,
  hedging, certification, contract holder behavior, prudent-estimate mortality and
  general-account assets [R38]. **The Guideline affects all contracts issued on or after
  January 1, 1981**, effective Dec. 31, 2009 (the redline shows the reform-era change to 2018)
  [R38]. **Not simply superseded:** VM-21 states that contracts subject to VM-21 may be
  aggregated with AG 43 contracts, and that "through reference in AG 43, the reserve
  requirements in VM-21 also apply to those contracts issued prior to Jan. 1, 2017, that would
  not otherwise be encompassed by the scope of VM-21" — so AG 43 is the scoping shell that
  pulls pre-2017 VA business onto the VM-21 calculation, and if the two are aggregated VM-G
  corporate governance applies to the combined valuation [R35].

### R39. Actuarial Guideline XXXIII — Determining CARVM Reserves for Annuity Contracts With Elective Benefits (AG 33)
- **Publisher:** NAIC
- **URL:** none — **no free official standalone text was located**. Title and current status
  verified from the Valuation Manual's VM-C index (page C-1) [R41]; the authoritative text is
  in the **AP&P Manual Appendix C (R33), a paid publication**. A related Academy proposal
  document is public but is *not* the guideline:
  http://actuary.org/wp-content/uploads/2017/11/AG-33_Non-Elective_Incidence_Reserve_Proposal_8-22-13.pdf
  (not fetched)
- **Accessed:** 2026-08-04 (search date; guideline text not retrieved)
- **Fetched:** **no** — title and continued incorporation verified via R41; the substantive description below is from secondary sources and is tagged accordingly
- **Annotation:** The interpretive core of formulaic CARVM for deferred annuities. CARVM sets
  the reserve as the greatest present value, over all elective benefit streams, of future
  guaranteed benefits; AG 33 specifies how to construct and value those **integrated benefit
  streams**, how elective benefits (surrender, partial withdrawal, annuitization at guaranteed
  purchase rates, nursing-home waivers) combine with **non-elective** benefits (death, and
  other non-mortality incidence), and what the "efficient policyholder selection" assumption
  means in practice [unverified — consistent across the Academy proposal document and the
  *Journal of Actuarial Practice* treatment of AG 33/34, neither fetched]. For an implementer
  this is the guideline that turns a deferred-annuity account-value roll-forward into a *set*
  of benefit streams and takes the maximum present value across them — the formulaic reserve
  any pre-VM-22 or VM-22-excluded fixed deferred annuity still requires. AG 35 (R40) layers
  the index feature onto this calculation [R40 context].

### R40. Actuarial Guideline XXXV — The Application of the Commissioners Annuity Reserve Method to Equity Indexed Annuities (AG 35)
- **Publisher:** NAIC
- **URL:** none — **no free official standalone text was located**. Exact title verified from
  the Valuation Manual's VM-C index (page C-2) [R41]; the authoritative text is in the **AP&P
  Manual Appendix C (R33), a paid publication**.
- **Accessed:** 2026-08-04 (search date; guideline text not retrieved)
- **Fetched:** **no** — title and continued incorporation verified via R41
- **Annotation:** The CARVM treatment of the index feature in equity-indexed (now generally
  "fixed indexed") annuities: it does not replace AG 33 but specifies how the index-linked
  benefit is brought into the AG 33 greatest-present-value calculation, offering alternative
  method families (industry shorthand "Type 1" / "Type 2"), imposing certification and
  notification requirements when a method is chosen or changed, and **requiring that
  equity-indexed annuity reserves be asset-adequacy tested** [unverified — from a practitioner
  presentation, not the guideline text]. The asset-adequacy requirement is the modelling
  consequence that matters most: an FIA block cannot rely on the formulaic reserve alone, so
  the same cash flow model must serve CARVM and ASOP 22 cash flow testing (R29).

### R41. VM-C: Appendix C — Actuarial Guidelines (index of guidelines incorporated into the Valuation Manual)
- **Publisher:** NAIC
- **URL:** https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf (pages C-1 to C-2; same document as R3)
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; the complete two-page index read)
- **Annotation:** The authoritative, current list of which actuarial guidelines the Valuation
  Manual incorporates, with their exact titles — the cheapest way to verify a guideline number
  without buying the AP&P Manual (it "references the following requirements from Appendix C of
  the AP&P Manual") [R41]. The **annuity/CARVM family** it lists: **II** (interest rate
  guarantees on active life funds under group annuity contracts); **VIII** (valuation of
  individual single premium deferred annuities); **IX** (form classification of individual
  SPIAs); **IX-A** and **IX-C** (substandard annuity mortality for impaired lives — structured
  settlements and SPIAs respectively); **IX-B** (methods under the SVL for individual SPIAs,
  associated deferred payments, some deferred annuities and structured settlements); **XIII**
  (guideline concerning CARVM); **XXXIII** (R39); **XXXV** (R40); **XL** (valuation rate of
  interest for funding agreements and GICs with bail-out provisions); and **XLI** (projection
  of guaranteed nonforfeiture benefits under CARVM) [R41] — with IX-B and IX-C superseded on
  valuation interest rates by VM-V §1 for in-scope contracts [R37]. **Verified negative
  finding:** the VM-C index contains **no AG XLIII, no AG XLIX/XLIX-A, and no AG LIV** [R41];
  AG 43 sits in AP&P Appendix C but outside VM-C because its remaining work is on pre-VM
  contracts [R35], and AG 54 is a nonforfeiture guideline, not a valuation one [R44]. Do not
  infer a guideline's non-existence from absence here, and do not infer its VM applicability
  from presence elsewhere.

---

## 8. NAIC nonforfeiture and market conduct for annuities

### R42. Standard Nonforfeiture Law for Individual Deferred Annuities (Model #805)
- **Publisher:** NAIC (print: "NAIC Model Laws, Regulations, Guidelines and Other Resources—Fall 2020")
- **URL:** https://content.naic.org/sites/default/files/model-law-805.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; Sections 1–8 read in full)
- **Annotation:** The floor under every fixed deferred annuity's cash value, and the single
  most mechanically precise item in this library. The **minimum nonforfeiture amount**
  accumulates **net considerations = 87.5% of gross considerations** at the Subsection B
  interest rate, **decreased by** prior withdrawals and partial surrenders (accumulated at the
  same rates), an **annual contract charge of $50** (accumulated), premium tax actually paid
  by the company, and any indebtedness with accrued interest [R42]. **The indexed
  nonforfeiture rate (Subsection B)** is the **lesser of 3% and** the **five-year Constant
  Maturity Treasury Rate** reported by the Federal Reserve as of a date, or averaged over a
  period, specified in the contract and no longer than **15 months** before the issue or
  redetermination date, **rounded to the nearest 1/20th of one percent**, **reduced by 125
  basis points**, and **floored at 15 basis points (0.15%)**; **Subsection C** allows that
  125bp reduction to be increased by **up to an additional 100 basis points** during a period
  in which the contract provides "substantive participation in an equity indexed benefit,"
  provided the present value of the additional reduction at issue and at each redetermination
  does not exceed the market value of the equity benefit, demonstrable on the commissioner's
  demand [R42]. **Cash surrender value** must be at least the present value of the accrued
  paid-up annuity at a rate no more than **1% higher** than the contract accumulation rate and
  never less than the minimum nonforfeiture amount, and the death benefit must be at least the
  cash surrender benefit [R42]. **Section 2 scope exclusions:** reinsurance;
  employer/employee-organization group annuities under retirement or deferred compensation
  plans other than those providing IRC §408 IRAs/individual retirement annuities; premium
  deposit funds; **variable annuities**; investment annuities; **immediate annuities**;
  **deferred annuities after annuity payments have commenced**; reversionary annuities; and
  out-of-state deliveries — and Sections 3–8 do not apply to **contingent deferred annuities**,
  for which the commissioner may prescribe nonforfeiture by regulation [R42].

### R43. Variable Annuity Model Regulation (Model #250)
- **Publisher:** NAIC (print: "NAIC Model Laws… — October 2007")
- **URL:** https://content.naic.org/sites/default/files/model-law-250.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; TOC and Section 7 read)
- **Annotation:** **#250 is the Variable Annuity Model Regulation, not the Annuity Disclosure
  Model Regulation** — that is **#245** (R45) — verified from both model-law prints and
  independently from AG 54, which cites "NAIC Model 250, Variable Annuity Model Regulation"
  [R43][R44][R45]. It covers insurer qualification to issue variable annuities, separate
  accounts, contract filing, required contract provisions, nonforfeiture benefits, required
  reports, and agent qualification, with **Section 7 the load-bearing part for modelling**:
  §7.A excludes the same categories as Model #805 (reinsurance, qualifying group retirement
  plans, premium deposit funds, investment annuities, immediate annuities, deferred annuities
  in payout, reversionary annuities, out-of-state deliveries) [R43]. **§7.B is the boundary
  rule:** "To the extent that a variable annuity contract provides benefits that do not vary in
  accordance with the investment performance of a separate account before the annuity
  commencement date, the contract shall contain provisions that satisfy the requirements of
  [Model #805] and shall not otherwise be subject to this section" — so the **fixed account
  inside a VA is tested against Model #805**, assuming 100% of considerations allocated to the
  fixed account; §7.C requires paid-up annuity benefits on cessation of considerations and
  lump-sum surrender provisions where offered [R43]. AG 54 (R44) exists precisely because
  Model #250 defines variable annuities by reference to separate-account investment experience
  and non-unitized ILVA accounts do not automatically satisfy it [R44].

### R44. Actuarial Guideline LIV — Nonforfeiture Requirements for Index-Linked Variable Annuity Products (AG 54)
- **Publisher:** NAIC (adopted by Life Actuarial (A) Task Force 12/11/2022; adopted by Life Insurance and Annuities (A) Committee 2/24/2023)
- **URL:** https://content.naic.org/sites/default/files/committees-pending-action-actuarial-guideline-liv-230224.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; the complete 6-page guideline read, including project history)
- **Annotation:** Its stated purpose is "to specify the conditions under which an Index-Linked
  Variable Annuity (ILVA) is consistent with the definition of a variable annuity and exempt
  from Model 805 and specify nonforfeiture requirements consistent with variable annuities";
  the NAIC deliberately adopts **ILVA** over "RILA"/"structured annuity" to signal that
  compliant designs are variable annuities first [R44]. **The mechanism a model must
  implement:** because an ILVA account is not unitized, **Interim Values** must be materially
  consistent with a **Hypothetical Portfolio = Fixed Income Asset Proxy + Derivative Asset
  Proxy**, less a provision for reasonably expected or actual **Trading Costs** at the time the
  Interim Value is calculated — the Index Strategy Base equals the Strategy Value at term
  start, the Fixed Income Asset Proxy is a hypothetical bond whose book value starts at (Index
  Strategy Base − Derivative Asset Proxy value) and at unchanged yield accretes to the Index
  Strategy Base at term end, and Derivative Asset Proxy assumptions (implied volatilities,
  risk-free rates, dividend yields) must be consistent with observable market prices wherever
  possible and valued by Black-Scholes, Monte Carlo, or other market-consistent techniques
  [R44]. Non-Hypothetical-Portfolio methodologies are permitted **only** on a demonstration of
  material consistency across each Index Strategy / Index Strategy Term combination "under a
  reasonable number of realistic economic scenarios that include index changes that test
  crediting constraints and recognize initial option pricing market conditions," and an
  **actuarial memorandum with certifications is required with each ILVA product filing**
  (equity between contract holder and company, market-consistency of derivative assumptions,
  material consistency of contractual Interim Values, reasonableness of Trading Costs); in-scope
  Index Strategies must comply with **Model #250 Section 7 excluding §7.B** [R44]. **Effective
  for all contracts, riders, endorsements and amendments issued on or after July 1, 2024**;
  whether an MVA is included or excluded, and any MVA formula, is left to the states under the
  equity principle; and an ILVA that fails this guideline is not a variable annuity and falls
  under Model #805 (R42) [R44].

### R45. Annuity Disclosure Model Regulation (Model #245)
- **Publisher:** NAIC (print: "NAIC Model Laws… — Summer 2021")
- **URL:** https://content.naic.org/sites/default/files/model-law-245.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; Sections 1 and 3 read; Section 6 and Appendix A structure confirmed from the TOC)
- **Annotation:** The annuity counterpart to Model #582 — and the correct model number is
  **#245**, not #250 (R43) — setting minimum disclosure for annuity contracts and, in **Section
  6, standards for annuity illustrations**, with **Appendix A providing an annuity illustration
  example** and Sections 5 (disclosure document and Buyer's Guide) and 7 (report to contract
  owners) carrying the rest [R45]. **Scope (Section 3) is what a modeller must read first:** it
  applies to all group and individual annuity contracts and certificates **except** (A)
  immediate and deferred annuities **containing no non-guaranteed elements**; (B) annuities
  funding ERISA plans, 401(a)/401(k)/403(b), 414/457 governmental and church plans, and
  nonqualified deferred compensation arrangements — with a carve-back for
  employee-elective-contribution arrangements involving direct solicitation where two or more
  fixed annuity providers are offered; (C) non-registered variable annuities sold only to
  accredited investors/qualified purchasers in exempt transactions; and (D) transactions in
  variable annuities and other registered products complying with SEC and FINRA
  disclosure/illustration rules — though the **Buyer's Guide is still required in variable
  annuity sales** [R45]. Do not reuse AG 49 / AG 49-A logic (R8–R10) for FIA illustrations:
  indexed-*annuity* illustration limits run through this regulation, and they are constructed
  differently from the IUL guidelines. A drafting note flags NSMIA preemption risk over the
  §3.D(1) sunset language [R45].

### R46. Suitability in Annuity Transactions Model Regulation (Model #275)
- **Publisher:** NAIC (print: "NAIC Model Laws… — Spring 2020"; this print **is** the 2020 best-interest revision)
- **URL:** https://content.naic.org/sites/default/files/model-law-275.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; TOC and Section 1 read)
- **Annotation:** The 2020 best-interest revision, adopted by the NAIC on February 13, 2020
  [unverified as to the exact adoption date — the print carries "Spring 2020" and the
  best-interest text, which confirms the substance]. Section 1.A states the purpose plainly:
  to require producers "to act in the best interest of the consumer when making a
  recommendation of an annuity and to require insurers to establish and maintain a system to
  supervise recommendations," and the structure is Purpose / Scope / Authority / Exemptions /
  Definitions / **Duties of Insurers and Producers (Section 6)** / Producer Training /
  Compliance Mitigation and Penalties / Recordkeeping / Effective Date, with three appendices
  (producer disclosure for annuities, consumer refusal to provide information, consumer
  decision to purchase not based on a recommendation) [R46]. Section 6 organises the
  best-interest obligation into four obligations — care, disclosure, conflict of interest, and
  documentation — aligned with SEC Regulation Best Interest [unverified — from NAIC and
  industry summaries, not read in the section text]. **Modelling relevance is indirect but
  real:** best-interest supervision changes exchange/1035 activity and therefore surrender and
  replacement assumptions, and the producer-disclosure appendix affects distribution cost
  structures; the requirements are intended to supplement, not replace, Model #245 disclosure
  [unverified].

---

## 9. Capital — C-3 Phase II and the variable annuity framework reform

### R47. C-3 RBC Instructions and Appendices (incorporating the Academy's C3 Phase II Report for variable annuities)
- **Publisher:** NAIC RBC instructions, transmitted with a memo from the American Academy of Actuaries C3 Life and Annuity Capital Work Group to the NAIC Life RBC Working Group dated November 24, 2009
- **URL:** https://content.naic.org/sites/default/files/inline-files/committees_e_capad_lrbc_C3_RBC_instructions_package.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; transmittal memo, "Calculation of the Total Asset Requirement," "Application of the Tax Adjustment," and "Calculation of the Standard Scenario Amount" read)
- **Annotation:** The mechanics of **C-3 Phase II** market-risk RBC for variable annuities as
  incorporated into the Life RBC instructions: **Appendix 2 directly incorporates the Academy's
  June 2005 "Recommended Approach for Setting Risk-Based Capital Requirements for Variable
  Annuities and Similar Products"** and Appendix 3 the September 2009 C3 Phase III report for
  life products [R47]. **The calculation a model must reproduce:** run stochastic scenarios on
  prudent best-estimate assumptions with calibrated fund performance distributions; for each
  scenario compute accumulated statutory surplus including federal income tax and take the
  negative of the lowest present value as that scenario's asset requirement, modelling
  statutory reserve as equal to the working reserve; **set the Total Asset Requirement at
  CTE 90**; and **RBC = the excess of the TAR over statutory reserves**, subject to the Standard
  Scenario and the smoothing/transition rules, then combined with C1CS for covariance [R47]. A
  **Tax Adjustment** is required where modelled tax reserves are set equal to Working Reserves
  but actual tax reserves exceed them at the start of the projection, correcting the
  understatement of modelled tax expense via a factor `f` derived from the reserve ratio at the
  worst duration; the **Standard Scenario Amount** is a floor — a single prescribed projection
  of account values with specified returns and prescribed assumptions — and where it exceeds
  the stochastic result it becomes the TAR before tax adjustment [R47]. **Caveat for
  implementers:** this print states a **35% federal income tax rate** and predates both TCJA and
  the 2018–2020 VA framework reform [R47]; use it for structure, and R48 plus the current VM-21
  (R35) and Life RBC instructions for parameters.

### R48. Variable Annuity Statutory Reserve and Capital Reform — QIS II Public Report and Executive Summary
- **Publisher:** Oliver Wyman, for the NAIC Variable Annuity Issues (E) Working Group (VAIWG)
- **URL (public report):** https://content.naic.org/sites/default/files/committee_related_documents/cmte_e_va_issues_wg_related_qis_ii_public_report.pdf
- **URL (executive summary):** https://content.naic.org/sites/default/files/committee_related_documents/cmte_e_va_issues_wg_related_qis_ii_executive_summary.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes, both (local text extraction; background, purpose and recommendation sections read; both documents dated February 12, 2018)
- **Annotation:** The adopting-era analytical documents behind the **2018–2020 NAIC variable
  annuity reserve and capital framework reform** — the reform that produced the 2020 VM-21 and
  the revised C-3 Phase II [R48]. **Diagnosed root causes:** penalties for economic-based
  hedging (fully hedging fair value *increased* capital requirements and RBC ratio volatility);
  structural deficiencies in the Standard Scenario that prevented alignment with the stochastic
  calculation it governs; and lack of harmonization in scenario projection practice — while
  preserving principles-based reserving, a book-value statutory approach, the "time-to-worst"
  accumulated-deficiency measure, real-world capital markets scenarios, and a Standard Scenario
  construct to govern assumptions [R48]. **Key parameterisation outcome:** the C-3 charge is
  computed as the difference between a higher-confidence "CTE High" amount and the statutory
  reserve, both on the same distribution of projected deficiencies; CTE High was provisionally
  CTE 98, and QIS II recommended **CTE 95 with a 25% scalar** under the alternative equity
  scenarios, chosen so that hedging would reduce a company's total funding requirement at a
  typical target RBC ratio, with equity scenario calibration tested over a 1926–2016 window
  [R48]. History as recorded: C3 Phase II enacted 2006 and AG 43 in 2009; Oliver Wyman engaged
  after captive reserve-financing pressure, preliminary report September 10, 2015; **QIS I**
  (fifteen companies, February–July 2016); recommendations to the VAIWG August 23, 2016 with
  redlined AG 43 and C3 Phase II guidance September 26, 2016 (R38 is that redline); a 60-day
  exposure from September 15, 2016; then **QIS II** in 2017 [R48].

---

## 10. Federal securities regulation — registered annuity products

### R49. Registration for Index-Linked Annuities and Registered Market Value Adjustment Annuities; Amendments to Form N-4 for Index-Linked Annuities, Registered Market Value Adjustment Annuities, and Variable Annuities; Other Technical Amendments
- **Publisher:** U.S. Securities and Exchange Commission
- **URL:** https://www.govinfo.gov/content/pkg/FR-2024-07-24/html/2024-14925.htm (89 Fed. Reg. 59978, July 24, 2024). **The SEC's own PDF, https://www.sec.gov/files/rules/final/2024/33-11294.pdf, returned HTTP 403 and was not fetched.**
- **Accessed:** 2026-08-04
- **Fetched:** yes, via govinfo.gov [R49]; publication metadata independently corroborated by GAO's rule report, https://www.gao.gov/products/b-336553 (fetched) [R49b]
- **Annotation:** **Release Nos. 33-11294; 34-100450; IC-35273; File No. S7-16-23; RIN
  3235-AN30**, published at **89 Fed. Reg. 59978 (July 24, 2024)** and **effective September 23,
  2024** [R49][R49b]. The statutory driver is the **Registration for Index-Linked Annuities
  Act**, enacted as Division AA, Title I of the **Consolidated Appropriations Act, 2023**, which
  directed the Commission to adopt a new RILA registration form within 18 months [R49]. **What
  it requires:** RILA and registered MVA issuers must register on **Form N-4** rather than
  S-1/S-3; provide tailored disclosure of **cap rates, participation rates, buffers and
  floors**, contract adjustments and surrender charges; use layered disclosure with a **Key
  Information Table** in prescribed format; optionally use summary prospectuses for continuous
  offerings; pay registration fees annually on net issuances; and comply with Rule 156 on sales
  literature [R49]. **Compliance date: May 1, 2026** — initial registration statements filed on
  or after that date must comply with amended Form N-4, and RILAs previously registered on
  Forms S-1 or S-3 must file a Rule 485(a) post-effective amendment on Form N-4 by that date
  [unverified as to the mechanics — the date is consistently reported across filing-agent and
  law-firm summaries; the release's section II.J was not read in full].

### R50. Updated Disclosure Requirements and Summary Prospectus for Variable Annuity and Variable Life Insurance Contracts (Rule 498A adopting release)
- **Publisher:** U.S. Securities and Exchange Commission
- **URL:** https://www.govinfo.gov/content/pkg/FR-2020-05-01/html/2020-05526.htm (**the SEC's own PDF at https://www.sec.gov/files/rules/final/2020/33-10765.pdf returned HTTP 403 and was not fetched**)
- **Accessed:** 2026-08-04
- **Fetched:** yes, via govinfo.gov
- **Annotation:** **Release Nos. 33-10765; 34-88358; IC-33814; File No. S7-23-18; RIN
  3235-AK60**; **effective July 1, 2020**, with certain provisions effective January 1, 2022
  [R50]. It adopted **Rule 498A**, an optional layered-disclosure framework letting variable
  contract issuers satisfy prospectus delivery through an **Initial Summary Prospectus** for new
  investors and an **Updating Summary Prospectus** for existing investors, with the full
  statutory prospectus and SAI available online free and on request in paper [R50]. The
  mandatory **Key Information Table** consolidates five topics — fees and expenses, risks,
  restrictions on access, taxes, and conflicts of interest — in standardized order to allow
  cross-product comparison, and Forms **N-4 and N-6** were modernized to condense summary
  information, reflect the prevalence of optional benefit riders, and require **Inline XBRL**
  tagging of specified prospectus disclosures [R50]. The Commission's stated rationale was that
  bundled variable contract prospectuses frequently exceed 100 pages [R50].

### R51. 17 C.F.R. § 230.498A — Summary prospectuses for separate accounts offering variable annuity and variable life insurance contracts and for offering registered non-variable annuity contracts
- **Publisher:** U.S. Government (Code of Federal Regulations), via Legal Information Institute, Cornell Law School
- **URL:** https://www.law.cornell.edu/cfr/text/17/230.498A
- **Accessed:** 2026-08-04
- **Fetched:** yes
- **Annotation:** The operative rule text, and the reason to cite it separately from R50: the
  **current title has been extended to "and for offering registered non-variable annuity
  contracts"**, reflecting the 2024 RILA rulemaking (R49) [R51]. It deems a compliant summary
  prospectus a prospectus under Securities Act §10(b) for delivery purposes [R51]. **Delivery
  obligations are satisfied when** the summary prospectus reaches the investor by the time the
  contract is delivered; the summary meets the content requirements; the registrant keeps
  current statutory prospectuses and related documents accessible on a specified website for at
  least 90 days; and paper copies are furnished on request within three business days [R51].
  Applies to registrants on **Forms N-3, N-4 and N-6** [R51].

### R52. SEC Form N-4 — Registration statement for separate accounts organized as unit investment trusts (as amended for RILAs and registered MVA annuities)
- **Publisher:** U.S. Securities and Exchange Commission
- **URL:** https://www.sec.gov/files/formn-4.pdf
- **Accessed:** 2026-08-04 (fetch attempted on this date; document not retrieved)
- **Fetched:** **no — sec.gov returned HTTP 403 to automated fetch on 2026-08-04.** The URL is genuine (it appears in SEC search indexing), but the form text was not retrieved.
- **Annotation:** The form itself is the disclosure schema a variable annuity or RILA product
  must populate, and its current content requirements are described first-hand only through the
  adopting releases that created and amended them — **R50** for the post-2020 structure
  (condensed summary, optional benefits, Key Information Table, Inline XBRL) and **R49** for the
  RILA/MVA extension (cap rates, participation rates, buffers, floors, contract adjustments,
  surrender charges) [R49][R50]. For a modelling library the value is mainly in *reverse*: the
  fee table and Key Information Table define the charge taxonomy — mortality and expense risk
  charge, administrative charge, contract maintenance fee, optional benefit rider charges,
  surrender charges — that a VA/RILA cash flow model must expose as parameters.

### R53. SEC Rule 151A and Annuities: Issues and Legislation (CRS Report R40656)
- **Publisher:** Congressional Research Service (secondary, but authoritative on legislative history)
- **URL:** https://www.everycrsreport.com/reports/R40656.html
- **Accessed:** 2026-08-04
- **Fetched:** yes
- **Annotation:** The clean history of **why fixed indexed annuities are not registered
  securities**, which a product library needs in order to justify treating FIA and RILA as
  different regulatory animals. Rule 151A, finalized **December 17, 2008** and published
  January 16, 2009 after roughly 4,800 comments, would have classified indexed annuities as
  securities where "the amounts payable by the insurer… are more likely than not to exceed" the
  guaranteed minimums, effective January 12, 2011; in **American Equity Investment Life
  Insurance Co. v. SEC** the **U.S. Court of Appeals for the D.C. Circuit** held on July 21,
  2009 that the SEC's classification was reasonable but its analysis of effects on efficiency,
  competition and capital formation inadequate, and **vacated Rule 151A on July 12, 2010**
  [R53]. **Dodd-Frank § 989J** (P.L. 111-203, signed July 21, 2010 — the "Harkin amendment")
  then directed the SEC to treat annuities meeting specified conditions as **exempt securities**,
  returning them to state insurance regulation [R53]. Net effect for a model library: FIAs are
  state-regulated non-registered products governed by Model #805 (R42), Model #245 (R45) and
  AG 33/35 (R39/R40); RILAs, which expose the contract holder to index losses, are registered
  and governed additionally by R49–R52 and AG 54 (R44).

### R54. FINRA Rule 2330 — Members' Responsibilities Regarding Deferred Variable Annuities
- **Publisher:** Financial Industry Regulatory Authority
- **URL:** https://www.finra.org/rules-guidance/rulebooks/finra-rules/2330
- **Accessed:** 2026-08-04
- **Fetched:** yes
- **Annotation:** Governs broker-dealer conduct in **recommended purchases and exchanges of
  deferred variable annuities and recommended initial subaccount allocations**; it does **not**
  reach reallocations among subaccounts, and excludes 401(k)/403(b)/457 tax-qualified plans
  unless an individual participant receives a personalized recommendation [R54]. Before
  recommending, a member must have a reasonable basis to believe the transaction is suitable
  under Rule 2111 and that the customer has been informed of the **surrender period and
  surrender charge** and the **potential tax penalty on redemption before age 59½**, and a
  **registered principal must review and approve the application no later than seven business
  days after an OSJ receives a complete and correct application package**, with written
  supervisory procedures, surveillance for inappropriate exchange rates among associated
  persons, and documented training programs required [R54]. **Modelling relevance:** the
  principal-review window and exchange surveillance are the proximate regulatory brake on 1035
  exchange velocity (R56) and therefore on VA replacement-driven surrender assumptions. Whether
  FINRA applies Rule 2330 to RILAs specifically is [unverified] — the rule text says "deferred
  variable annuities."

---

## 11. Federal tax — annuities

### R55. 26 U.S.C. § 72 — Annuities; certain proceeds of endowment and life insurance contracts
- **Publisher:** Legal Information Institute, Cornell Law School (U.S. Code)
- **URL:** https://www.law.cornell.edu/uscode/text/26/72
- **Accessed:** 2026-08-04
- **Fetched:** yes
- **Annotation:** The core annuity tax section, and the one an illustration or in-force system
  must implement. **§72(b) exclusion ratio:** the excluded portion of each annuity payment bears
  the same ratio to the payment as the **investment in the contract** (premiums paid less prior
  excludable distributions) bears to the **expected return**, capped at unrecovered investment;
  **§72(e)** applies the **LIFO / income-first rule** to pre-annuity-starting-date distributions
  from deferred annuities, in contrast to the ratable basis recovery of annuitized payments
  [R55]. The **aggregation rule** — "all annuity contracts issued by the same company to the
  same policyholder during any calendar year shall be treated as 1 annuity contract" — is a real
  modelling requirement for multi-contract policyholders, and **§72(q)** adds a **10% penalty**
  on the includible portion of distributions from non-qualified annuity contracts (exceptions
  include age 59½, death, disability, substantially equal periodic payments, and amounts
  allocable to investment before August 14, 1982), with **§72(t)** the parallel 10% additional
  tax for qualified plans and IRAs [R55]. **§72(s)** requires that on the holder's death after
  annuitization the remaining interest distribute at least as rapidly as under the pre-death
  method, and on death before annuitization the entire interest within five years subject to a
  beneficiary-life-expectancy exception — the provision that shapes death-benefit payout
  modelling — and **§72(u)** strips deferral from contracts held by non-natural persons,
  treating the **primary annuitant** as the holder [R55].

### R56. 26 U.S.C. § 1035 — Certain exchanges of insurance policies
- **Publisher:** Legal Information Institute, Cornell Law School
- **URL:** https://www.law.cornell.edu/uscode/text/26/1035
- **Accessed:** 2026-08-04
- **Fetched:** yes
- **Annotation:** Tax-free exchange relief, and the asymmetry matters. Permitted: **life → life,
  endowment, annuity, or qualified long-term care**; **endowment → endowment (with payments
  beginning no later than under the original), annuity, or qualified LTC**; **annuity → annuity
  or qualified LTC**; **qualified LTC → qualified LTC** — so **an annuity cannot be exchanged
  tax-free for a life insurance contract**, and relief does not apply to transfers having the
  effect of transferring property to a non-U.S. person [R56]. **Modelling relevance:** 1035
  exchanges are the dominant source of both new-business premium and surrender activity in the
  deferred annuity market, so an exchange assumption is a first-class input, and the
  annuity→life prohibition constrains which replacement flows a model should even contemplate.
  Read with FINRA Rule 2330 (R54) and Model #275 (R46), which together throttle exchange
  velocity in the registered and best-interest channels.

### R57. 26 C.F.R. § 1.401(a)(9)-6 — Required minimum distributions for defined benefit plans and annuity contracts (QLAC rules)
- **Publisher:** Legal Information Institute, Cornell Law School (CFR)
- **URL:** https://www.law.cornell.edu/cfr/text/26/1.401(a)(9)-6
- **Accessed:** 2026-08-04
- **Fetched:** yes
- **Annotation:** The regulation that makes **qualifying longevity annuity contracts** possible
  and constrains their design: QLAC distributions "must commence not later than a specified
  annuity starting date that is no later than the first day of the month next following the
  **85th anniversary**" of the employee's birth, and the contract may not offer "any commutation
  benefit, cash surrender right, or other similar feature" after the required beginning date,
  subject to a 90-day rescission exception [R57]. A QLAC is therefore modelled with **no
  surrender value**, which removes the entire lapse module from the liability; dollar
  limitations sit in paragraph (q)(2) [R57] (see R58 for the current **$200,000** figure and the
  elimination of the 25%-of-account-balance limit). More generally, distributions must be
  **periodic annuity payments for life, joint lives, or a period certain**, at **uniform
  intervals not exceeding one year**, and **nonincreasing** except as permitted — the rule that
  forbids most increasing-payment DIA designs in qualified money — with actuarial increases
  required for employees retiring after age 70½, from April 1 following that birthday until
  commencement, using reasonable actuarial assumptions [R57].

### R58. Required Minimum Distributions — Final Regulations (T.D. 10001)
- **Publisher:** Internal Revenue Service / U.S. Treasury (Federal Register, July 19, 2024)
- **URL:** https://www.govinfo.gov/content/pkg/FR-2024-07-19/html/2024-14542.htm
- **Accessed:** 2026-08-04
- **Fetched:** yes, via govinfo.gov
- **Annotation:** **T.D. 10001; RIN 1545-BP82; published July 19, 2024; effective September 17,
  2024; applicable for calendar years beginning January 1, 2025** (with §1.402(c)-2 applying to
  distributions on or after that date), finalizing regulations under IRC §§401(a)(9), 402(c),
  403(b), 408, 457 and 4974 and incorporating SECURE and SECURE 2.0 changes [R58]. **The
  annuity-relevant content:** SECURE 2.0 **§202** directed amendments to §1.401(a)(9)-6 that
  **eliminate the 25%-of-account-balance limitation on QLAC premiums**, **raise the dollar cap
  from $125,000 to $200,000** (inflation-adjusted), permit joint-and-survivor benefits to
  survive divorce under qualified-domestic-relations-order conditions, and add a **90-day
  free-look rescission** [R58]. The regulations also address **bifurcation** where an annuity is
  purchased with part of an individual account — the annuity payments satisfy §1.401(a)(9)-6
  while the residual account satisfies §1.401(a)(9)-5 — and SECURE 2.0 **§204** adds an elective
  **partial annuitization** alternative under which the required amount is the excess of the
  total required amount for the year over the annuity amount for that year, aggregating the
  annuity contract value with the remaining account balance [R58]. RMD timing is a *behavioral*
  input as well as a tax one: GLWB activation clusters at the RMD age (R64).

---

## 12. Annuitant mortality and annuity experience studies

### R59. NAIC Model Rule (Regulation) for Recognizing a New Annuity Mortality Table for Use in Determining Reserve Liabilities for Annuities (Model #821), with the corresponding VM-M definitions
- **Publisher:** NAIC (model print: "NAIC Model Laws… — January 2013"), plus the Valuation Manual appendix
- **URL (model):** https://content.naic.org/sites/default/files/model-law-821.pdf
- **URL (VM-M definitions):** https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf (VM-M §1.I–§1.M, §2.C; same document as R3)
- **Accessed:** 2026-08-04
- **Fetched:** yes, both (local text extraction)
- **Annotation:** The statutory annuity mortality basis. Model #821 recognizes, for the minimum
  standard of valuation of annuity and pure endowment contracts, the **1983 Table "a"**, the
  **1983 GAM Table**, the **Annuity 2000 Mortality Table**, the **2012 Individual Annuity
  Reserving (2012 IAR) Mortality Table**, and the **1994 GAR Table**, with Appendices I–IV
  printing the **2012 IAM Period Table** (female and male, age nearest birthday) and
  **Projection Scale G2** [R59]. **The 2012 IAR is a generational table:** VM-M §1.J prints
  **q<sub>x</sub><sup>2012+n</sup> = q<sub>x</sub><sup>2012</sup> × (1 − G2<sub>x</sub>)<sup>n</sup>**,
  with the result **rounded to three decimal places per 1,000** and — an implementation trap the
  manual calls out explicitly — the rounding applied **from the 2012 period rate each time,
  never by compounding an already-rounded prior-year rate**; worked example: male age 30,
  q<sup>2012</sup> = 0.741 → q<sup>2014</sup> = 0.741 × 0.99² = 0.7262541 → 0.726 (not 0.727)
  [R59]. VM-M §2.C defines the **2012 IAM Basic Table** as the unloaded table underlying the
  Period Table, developed from the 2002 experience table projected to 2012, and records that the
  underlying **2000–2004 Payout Annuity Mortality Experience Study** covered immediate
  annuities, annuitizations and life settlement options from **16 companies**, **excluding
  substandard annuities, structured settlement annuities and variable payout annuities** [R59] —
  an exclusion that matters when the modelled block includes those. The 2012 IAM/Scale G2 tables
  themselves live in **AP&P Manual Appendix A-821** [R59][R33].

### R60. 2012 Individual Annuity Reserving Table — Report of the joint American Academy of Actuaries / Society of Actuaries Payout Annuity Table Team
- **Publisher:** American Academy of Actuaries and Society of Actuaries (joint subgroup of the Life Experience Subcommittee), presented to the NAIC Life Actuarial Task Force; September 2011 (chair: Mary Bahna-Nolan)
- **URL:** http://actuary.org/wp-content/uploads/2017/11/Payout_Annuity_Report_09-28-11.pdf (https:// redirects to http:// on the same path)
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; title page, TOC, and the margin/loading sections read)
- **Annotation:** The development report behind R59 — what a modeller needs when justifying or
  stress-testing the valuation basis. LATF's charge was to produce a new annuity valuation
  mortality table "including projection scales and margins necessary to make the table suitable
  for standard valuation purposes for individual annuities," and the IAR Table is the composition
  of **three pieces**: the 2012 IAM Basic Table, the margin, and Projection Scale G2 [R60].
  **The margin, as recommended by the Team and agreed by LATF, is 10% at all ages up to and
  including 100, grading down 1% per year above age 100 until the ultimate mortality cap of
  0.40000 is invoked**, producing a zero margin at the cap; LATF concluded there was no
  compelling reason to depart from the approach or level used for the a2000 Table [R60]. The
  report also covers graduation, younger-age and older-age adjustments (Kannisto-form
  extrapolation at the oldest ages), the derivation of improvement from 2002 to 2012, A/E
  analysis against the unloaded 2012 IAM adjusted to January 1, 2007 (the midpoint of the
  underlying experience), and tabulated reserve-impact comparisons against the a2000 Table [R60].

### R61. 2020–2024 Individual Payout Annuity Mortality Experience Study
- **Publisher:** LIMRA and the Society of Actuaries Research Institute (joint)
- **URL:** https://www.soa.org/resources/experience-studies/2026/2020-24-individual-payout/
- **Accessed:** 2026-08-04
- **Fetched:** yes (landing page; the free public report PDF and the paid Standard Data Package were not separately fetched)
- **Annotation:** The current annuitant-longevity experience basis: **23 parent company groups
  covering 26 individual companies, over 80% of industry sales during the study period, 3.1
  million contract-years and $33 billion of annual-income-years of exposure, and 143,190 deaths
  over five years** [R61]. Results are presented against the **2012 IAM Table**, the prior study,
  and U.S. population mortality [R61] — i.e., it is directly usable as the A/E evidence for a
  prudent-estimate or best-estimate deviation from R59. Deliverables are a free public PDF plus a
  purchasable Standard Data Package with executive summary, in-depth analysis and interactive
  dashboards; the predecessor is the **2014–2019 Individual Payout Annuity Mortality Experience
  Study** (December 2022; 25 companies, ~80% of market, ~4.3 million contract-years, ~236,000
  deaths) [R61][R65].

### R62. Fixed Indexed Annuity Policyholder Behavior Experience Studies (2021–2022, with 2019–2020 predecessor)
- **Publisher:** LIMRA and the Society of Actuaries Research Institute (joint)
- **URL (2021–22):** https://www.soa.org/resources/experience-studies/2024/21-22-fia/
- **URL (2019–20):** https://www.soa.org/resources/experience-studies/2023/19-20-fia/
- **Accessed:** 2026-08-04
- **Fetched:** yes, both landing pages (free public report PDFs and paid data packages not separately fetched)
- **Annotation:** The public basis for FIA surrender and withdrawal assumptions. The
  **2021–2022** study covers **12 companies, ~4.8 million contracts of surrender exposure by
  count, $526 billion of contract value exposure, over 227,000 surrenders and $15.9 billion of
  withdrawals**, with comparisons "to several expected bases of policyholder behavior, including
  the current valuation standard"; the **2019–2020** study covers **17 parent company groupings /
  20 individual companies, roughly two-thirds of industry new sales and assets, ~4.9 million
  contracts valued at $503 billion, over 195,000 surrenders and $13.7 billion of withdrawals**
  [R62]. **The headline finding a model must encode** is the interaction between surrender-charge
  expiry and the GLWB rider: in the year the surrender charge expires, the surrender rate was
  about **10% for contracts with a GLWB rider versus about 33% without** [unverified — reported
  consistently in LIMRA/SOA press coverage of the 2019–20 study, not read in the report PDF].
  That is the difference between a shock-lapse assumption and a rider-suppressed one, and it is
  product-design-dependent, not a single industry number.

### R63. Fixed Rate Deferred Surrender Experience Studies (2023–24, with 2015–2022 predecessor)
- **Publisher:** LIMRA and the Society of Actuaries Research Institute (joint)
- **URL (2023–24):** https://www.soa.org/resources/experience-studies/2025/2023-24-fixed-rate-deferred/
- **URL (2015–2022 report PDF):** https://www.soa.org/49c0c1/globalassets/assets/files/resources/experience-studies/2024/15-22-frds.pdf (not fetched)
- **Accessed:** 2026-08-04
- **Fetched:** **partially** — both titles, dates and URLs verified from the SOA's Individual Annuity Experience Studies index (R65) [R65]; neither the landing page nor the report PDF was fetched individually
- **Annotation:** The surrender basis for MYGA / fixed-rate deferred annuities, where the shock at
  surrender-charge expiry is far more violent than in FIA because there is no living-benefit
  rider anchoring the contract holder. Reported surrender rates by contract count in the year the
  surrender charge expired were roughly **51.7% for 2020 and 55.7% for 2021** [unverified — from
  trade-press coverage of the 2015–2022 study, not read in the report]. Compare with the ~10%/~33%
  FIA figures at R62: the same event, three very different assumptions, driven by rider presence
  and rate-differential dynamics.

### R64. Variable Annuity Contract Holder Behavior and Guaranteed Living Benefit Utilization Studies (2022–2024, with the 2019–2021 and the 2013–2018 GLB utilization series)
- **Publisher:** LIMRA and the Society of Actuaries Research Institute (joint)
- **URL (2022–24):** https://www.soa.org/resources/experience-studies/2025/2022-24-va-livingbenefit/
- **URL (2019–21):** https://www.soa.org/resources/experience-studies/2023/19-21-va/ (not fetched; verified via R65)
- **URL (2015-experience GLB utilization report PDF):** https://www.soa.org/globalassets/assets/Files/resources/research-report/2018/variable-annuity-guaranteed-utilization.pdf (not fetched)
- **Accessed:** 2026-08-04
- **Fetched:** yes (2022–24 landing page) [R64]; the others verified via R65 only
- **Annotation:** The public basis for VA and RILA behavior assumptions. The **2022–2024** study
  covers **17 companies representing approximately 48% of new premium for VAs and RILAs**, about
  **11.5 million contracts valued at $1.5 trillion**, with over **625,000 surrender events and
  4 million withdrawal transactions** ($56.7 billion of contract value withdrawn) [R64] — note
  the explicit inclusion of RILAs in the premium-share denominator. **What a GLWB model needs
  from the utilization series** (from the earlier reports): roughly **79% of owners taking
  withdrawals withdrew at or near the maximum permitted amount (up to 110%)**, about **55%
  withdrew between 90% and 110% of the maximum**, most withdrawals run through **systematic
  withdrawal plans** which keep owners inside the guaranteed maximum, owners rarely add premium
  after contract year two, and **activation clusters at the RMD age** [unverified — these figures
  come from SOA/LIMRA summaries of the 2013/2015-experience utilization studies, not read in the
  report PDFs]. The RMD clustering is the reason R58 is a *behavioral* input to a GLWB model, not
  merely a tax one.

### R65. SOA Individual Annuity Experience Studies — index
- **Publisher:** Society of Actuaries Research Institute
- **URL:** https://www.soa.org/research/topics/indiv-ann-exp-study-list/
- **Accessed:** 2026-08-04
- **Fetched:** yes (complete list read)
- **Annotation:** The authoritative index of publicly available individual annuity experience
  studies, and the cheapest way to check whether an assumption source has been superseded [R65].
  It catalogues, by year: payout annuity mortality (2000–04, 2005–08, 2009–13, 2014–19, 2020–24);
  fixed indexed annuity behavior (2013–15, 2016–18, 2019–20, 2021–22); fixed rate deferred
  surrender (2015–22, 2023–24); variable annuity contract owner behavior (2019–21) and the VA
  guaranteed living benefits utilization series (2011 through 2018 experience); **deferred
  annuity mortality (2011–2015)**; **structured settlement mortality (1997, 2000–08, 2009–13,
  2005–17)**; a **Deferred Annuity Persistency Report (2006)**; and "Analysis of Mortality
  Experience Under Variable and Fixed Individual Annuities During the Deferred Period" (2006)
  [R65]. The last two are the only public sources located for **deferred-period**
  (pre-annuitization) annuitant mortality — a distinct and much under-served assumption relative
  to payout mortality.

---

## 13. Professional standards and practice notes — annuities

### R66. Implementation of Requirements for Principle-Based Reserves for Variable Annuities — 2022 Edition of VM-21 (Practice Note Supplement)
- **Publisher:** American Academy of Actuaries, Variable Annuity Reserves & Capital Work Group of the Life Practice Council (chair: Connie Tang); February 2022, 34 pages
- **URL:** https://actuary.org/wp-content/uploads/2022/02/VA_PN_Supplement_Final.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; title page, introduction, acronym list and full table of contents read)
- **Annotation:** The implementation companion to VM-21 (R35), written specifically for the
  **2020 revisions** to VA principle-based reserves and capital. Its eight sections map almost
  exactly onto the decisions a VA cash flow model has to make: **1. Transition; 2. Standard
  Projection** (including product/contractual conflicts); **3. Asset Modeling & Discount Rates;
  4. Scenarios; 5. Hedging; 6. C-3 Phase 2 RBC; 7. Disclosures; 8. Miscellaneous**, and its
  acronym list is itself a useful glossary (CDHS, Company-Specific Market Path, CTE with
  Prescribed Assumptions, Direct Iteration Method, Guarantee Actuarial Present Value, GPVAD, IMR)
  [R66]. **Explicitly not binding:** it "is not a promulgation of the Actuarial Standards Board,
  is not an actuarial standard of practice, is not binding upon any actuary" [R66]. Two cautions
  it states directly: readers must check differences between the VM-21 edition the note was
  written against and the edition applicable to the current valuation, since the Valuation Manual
  is a living document; and the note **does not cover state variations such as New York
  Regulation 213** [R66].

### R67. Utilization Assumptions of Guaranteed Living Benefits for Deferred Annuities — A Resource and Discussion Guide
- **Publisher:** American Academy of Actuaries, Life Experience Committee (chair: Donna Claire); May 2024
- **URL:** https://actuary.org/wp-content/uploads/2024/05/life-paper-GLBs.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; title page and front matter read)
- **Annotation:** The profession's assembled thinking on the single hardest assumption in the
  deferred annuity model — when and how intensely contract holders use a guaranteed living
  benefit. The Academy is explicit about its status: it "is not a promulgation of the Actuarial
  Standards Board, is not an actuarial standard of practice (ASOP), is not binding upon any
  actuary… This document should not be treated as guidance but rather it should be read and
  utilized as a list of considerations and resources on a particular topic" [R67]. Treat it as a
  checklist of drivers — moneyness, age and RMD timing, qualified versus non-qualified,
  distribution channel, systematic withdrawal plan enrolment, rider type — to test a utilization
  assumption against, and as the bridge from the experience data in R64 to a prudent-estimate
  assumption that will satisfy VM-21 §10 (R35) or VM-22 §10 (R36).

### R68. Fixed Indexed Annuities — Product Mechanics and Risk Management
- **Publisher:** American Academy of Actuaries, Life Experience and Assumptions Committee (chair: Kyle Wan); February 2026
- **URL:** https://actuary.org/wp-content/uploads/2026/02/life-FIA-policypaper.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; title page, table of contents and the crediting-method sections read)
- **Annotation:** The most current and most directly implementable public description of FIA
  mechanics, structured as Introduction; **Examples of Index Crediting Methods**; investment
  strategy, ALM and **hedging considerations**; and **Reserves and Regulations** [R68]. It
  defines the crediting levers precisely — **participation rate** (the percentage of index return
  credited: 10% index return at 80% participation with a 6% cap), **cap**, and **spread** (a
  percentage deducted from the index return) — and works a full **annual point-to-point** example
  against the S&P 500 showing a 7% cap and 0% floor binding in a year when the normalized index
  rose 25%, while noting the industry shift toward **custom indices with built-in volatility
  control** and covering averaging and monthly point-to-point variants [R68]. It explains the
  **option budget** framing — the insurer allocates a portion of premium to derivatives to hedge
  the index-linked credits — and links crediting design back to **nonforfeiture limits and the
  nonforfeiture rate** [R68], i.e., to R42.

### R69. Index-Linked Variable Annuity (ILVA) / Registered Index-Linked Annuity (RILA) Policy Paper
- **Publisher:** American Academy of Actuaries, Index-Linked Variable Annuity Subcommittee (chair: Elizabeth Keith); December 2025
- **URL:** https://actuary.org/wp-content/uploads/2025/12/Life-PolicyPaper120225.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; title page, table of contents and the interim-value sections read)
- **Annotation:** The bridge between AG 54's legal text (R44) and an actual RILA implementation.
  It describes the product family — downside protection via a **buffer, dual-direction buffer, or
  floor**, and upside parameters of **cap rate, participation rate, buffer and floor**, with more
  complex strategies adding **trigger rates, dual-direction buffers and performance locks** —
  noting that design complexity constrains the company's ability to hedge and value the strategy
  [R69]. It restates the two AG 54 guiding principles (interim values provide equity between
  contract holder and company; interim values are consistent with the Hypothetical Portfolio over
  the Index Strategy Term) and explains the consequence: a compliant ILVA is exempt from Model
  #805 and subject instead to variable annuity nonforfeiture under **Model #250** [R69]. It
  covers interim values under AG 54 **and** separately under the **Interstate Insurance Compact**
  standards, addresses **U.S. statutory risk-based capital** for ILVAs, and treats practical
  valuation issues such as hedge-cost inference and bid/mid/ask spread treatment in Trading Costs
  [R69].

### R70. ASOP No. 54 — Pricing of Life Insurance and Annuity Products
- **Publisher:** Actuarial Standards Board
- **URL:** https://www.actuarialstandardsboard.org/asops/pricing-of-life-insurance-and-annuity-products/
- **Accessed:** 2026-08-04
- **Fetched:** yes (adopted June 2018; effective December 1, 2018)
- **Annotation:** **Not in R1–R34** and squarely applicable to annuity work: it applies when
  actuaries perform pricing services for life insurance and annuity products at initial
  development or when charges or benefits change for future sales, covering individual policy
  forms and group master contracts with individually-priced certificates, and **excluding the
  pricing of reinsurance contracts** [R70]. It requires the actuary to consider the principal's
  profitability criteria, risk-capital approach and risk-management policies; select
  profitability metrics (it lists IRR, ROE, profit margin, ROA, value of new business, and
  break-even year); develop or select models accommodating product design, time horizon,
  granularity, **dynamic assumptions, economic scenarios, asset returns, accounting bases, risk
  capital frameworks, taxes and risk-mitigation strategies**; set internally consistent
  assumptions with margins where credible data is lacking; perform sensitivity and stochastic
  risk evaluation; and implement governance controls including model validation and independent
  review [R70]. For an annuity reference model this is the standard that justifies a pricing-mode
  output (profit metrics, dynamic lapse, hedge cost) alongside the valuation outputs.

### R71. ASOP No. 10 — U.S. GAAP for Long-Duration Life, Annuity, and Health Products (Revised Edition)
- **Publisher:** Actuarial Standards Board (Revised Edition, adopted by the ASB December 2022, Doc. No. 207)
- **URL:** http://www.actuarialstandardsboard.org/wp-content/uploads/2023/01/asop010_207.pdf
- **Accessed:** 2026-08-04
- **Fetched:** yes (local text extraction; title page, full table of contents, §§1.1–1.4 read)
- **Annotation:** **Not in R1–R34**, and the professional-standards counterpart to the LDTI
  accounting standard already catalogued at R34. **Effective for actuarial services related to
  the preparation or review of insurance company GAAP financial statements applicable to fiscal
  periods ending on or after May 1, 2023**, with scope covering long-duration life, **annuity**,
  or health products and yielding to applicable law and to authoritative GAAP guidance (ASC, SEC
  Staff Accounting Bulletins) where they conflict [R71]. Its definitions section is the working
  vocabulary an LDTI-capable annuity model must implement — **Best-Estimate Assumption, Cohort,
  Deferred Policy Acquisition Cost, Deferred Sales Inducements, GAAP Net Premiums, Liability for
  Future Policy Benefits, Lock-In, Market-Estimate Assumption, Market Risk Benefit, Net GAAP
  Liability, Policy Benefit Liability, Premium Deficiency, Risk of Adverse Deviation, and Value of
  Business Acquired** — and Section 3 covers classification of contracts, features and benefits
  and the best-estimate versus market-estimate assumption split [R71], the classification
  decision that determines whether a GLWB is an MRB or an insurance liability. **Caution:** two
  ASB pages carry ASOP 10 exposure drafts (an April 2022 proposed-revision page was fetched and
  is clearly labelled an exposure draft, not adopted [R71b:
  https://www.actuarialstandardsboard.org/asops/asop-no-10-ssun-u-s-gaap-for-long-duration-life-annuity-and-health-products/]);
  cite the Doc. No. 207 PDF above, which states adoption on its title page.

### R72. IRC Section 807 LB&I Directive Related to Principle-Based Reserves for Variable Annuity Contracts (AG 43/VM-21) and Life Insurance Contracts (VM-20)
- **Publisher:** Internal Revenue Service, Large Business & International Division
- **URL:** https://www.irs.gov/businesses/corporations/irc-section-807-large-business-and-international-lbi-directive-related-to-principle-based-reserves-for-variable-annuity-contracts-ag-43vm-21-and-life-insurance-contracts-vm-20
- **Accessed:** 2026-08-04 (fetch attempted on this date; document not retrieved)
- **Fetched:** **no — irs.gov returned HTTP 404 to automated fetch on 2026-08-04** on this and on a companion §446 hedging-directive URL, both of which appear in irs.gov search indexing. The URL is reproduced as surfaced by search; treat the substance below as unverified.
- **Annotation:** Reported as **LB&I-04-0818-015, issued August 24, 2018**, instructing LB&I
  examiners not to challenge an insurance company's determination of tax reserves for variable
  annuity contracts subject to **AG 43 / VM-21** and life contracts subject to **VM-20**, where
  the company reported its 2017 tax reserves in compliance with the directive; otherwise regular
  audit procedures apply [unverified]. Relevant to a model library because it is the practical
  bridge between the statutory annuity engine (R35, R38) and the §807 tax reserve (R16). A
  companion directive on the timing of hedges of variable annuity guaranteed minimum benefits
  under IRC §446 is also indexed on irs.gov [unverified].

---

## 14. Annuity half (R35–R72) — gaps, fetch failures, and unverified points

**Verified findings that correct assumptions a reader may bring**

1. **Model numbers.** **#245 is the Annuity Disclosure Model Regulation (R45)** and **#250 is
   the Variable Annuity Model Regulation (R43)** — verified against both model-law prints and
   AG 54's own citation [R43][R44][R45].
2. **VM-22's scope in the current edition.** In the Jan. 1, 2026 edition **VM-22 is entirely the
   principle-based framework for non-variable annuities**; the maximum valuation interest rates
   for income annuities are **in VM-V Section 1 (R37)**, not VM-22 [R36][R37].
3. **AG 54 exists and is a *nonforfeiture* guideline.** Actuarial Guideline LIV, effective for
   contracts issued on or after July 1, 2024, and it does **not** appear in the VM-C index
   [R41][R44].
4. **AG 43 is not simply superseded by VM-21.** Through reference in AG 43, VM-21's requirements
   also apply to pre-2017 contracts outside VM-21's own scope, and the two populations may be
   reserved as a single aggregated group [R35] — any statement that AG 43 is "replaced" is wrong
   in a way that changes in-force model scope.
5. **There is no ASOP for principle-based reserves for annuities.** ASOP 52 (R31) is scoped to
   life products under VM-20 and no VM-21 or VM-22 analogue exists (verified against the full ASB
   standards list, fetched 2026-08-04). The nearest professional guidance is the non-binding
   Academy practice note supplement (R66).

**What could not be verified**

- **AG 33 and AG 35 full texts (R39, R40).** No free official standalone copy was located on
  content.naic.org or elsewhere; **the authoritative text is in the AP&P Manual Appendix C (R33),
  a paid publication**. Their exact titles and continued incorporation were verified from the
  Valuation Manual's VM-C index [R41], but **every substantive statement about their mechanics is
  tagged [unverified]**. This is the single largest hole in the annuity half — formulaic CARVM
  for fixed and indexed deferred annuities rests on two guidelines that could not be read.
- **SEC primary documents.** **sec.gov returned HTTP 403** on every attempt (press release
  2024-81, `/files/rules/final/2024/33-11294.pdf`, `/files/formn-4.pdf`). Release metadata and
  substance were recovered from **govinfo.gov** (R49, R50) and **GAO** (R49b), which is why those
  entries are marked fetched. **Form N-4 itself (R52) was never retrieved** — its requirements
  are described only through the adopting releases.
- **The RILA compliance date of May 1, 2026** is consistently reported by filing agents and law
  firms, but section II.J of Release 33-11294 was not read, so the date carries [unverified] in
  R49 even though the effective date (September 23, 2024) is verified twice [R49][R49b].
- **federalregister.gov and ecfr.gov** both 302-redirect to a bot-block page; govinfo.gov and
  law.cornell.edu were substituted throughout.
- **IRS LB&I directives (R72).** **irs.gov returned HTTP 404** on both directive URLs surfaced by
  search; the control number, date and substance are [unverified].
- **A successor to the 2012 IAR valuation table could not be confirmed to exist.** The LATF
  charges page (fetched 2026-08-04) states generally that the Task Force works "with the American
  Academy of Actuaries and the Society of Actuaries… to develop new mortality tables for
  valuation and minimum nonforfeiture requirements," and lists active subgroups (VM-22,
  Experience Reporting, GOES, Longevity Risk, Variable Annuities Capital and Reserve) — **but it
  names no annuity mortality table project and no IAR replacement. No such project is asserted
  here.** The 2012 IAR (R59) remains the recognized valuation table, while the experience
  underneath it has moved materially; the 2020–2024 payout study (R61) measures against the 2012
  IAM basis directly, which is the right place to look for evidence of drift.
- **Quantitative behavior figures.** The FIA shock-lapse split (~10% with GLWB vs ~33% without),
  the fixed-rate-deferred shock lapse (~52%/~56%), and the GLWB withdrawal-efficiency distribution
  (~79% at or near maximum) all come from press summaries and landing pages, not from the study
  PDFs, which sit behind paid data packages. They are tagged [unverified] in R62, R63 and R64 and
  should be treated as order-of-magnitude anchors, not calibration targets.
- **VM-22 mandatory date.** VM-22 §2.B states the rule as "three years after the effective date"
  without printing a date [R36]; Jan. 1, 2029 is arithmetic, not quotation, and is tagged
  accordingly in R36.
- **C-3 Phase II parameters are stale in R47.** The instructions package read carries a **35%
  federal income tax rate** and predates both TCJA and the 2018–2020 reform [R47]. Its *structure*
  (CTE 90 TAR, RBC = TAR − statutory reserve, Standard Scenario floor, tax adjustment) is
  reliable; its *numbers* are not. Current parameters must come from the in-force Life RBC
  instructions, which were not located as a current standalone document.
- **Deferred-period annuitant mortality** is served publicly by only two dated sources — a
  2011–2015 deferred annuity mortality study and a 2006 analysis — both identified via the SOA
  index (R65) but neither fetched. This assumption is materially under-evidenced relative to
  payout mortality.
