# Solvency UK — product-specific regulatory treatment and the applicability matrix — research notes

**Stream:** Product-specific regulatory treatment (with-profits, unit-linked, annuities, protection,
income protection, whole of life) and the cross-product applicability judgements
**Access date for every citation below:** 2026-08-06
**Status:** research notes, not yet merged into
`uk/references/regulatory-and-actuarial-references.md`

---

## Scope and numbering note

This stream owns reference block **R114–R133**. Entries **R1–R38** live in
`uk/references/regulatory-and-actuarial-references.md`, are **frozen**, and are already cited by the
seven UK product documents; nothing below renumbers, restates or duplicates them. Six sibling streams
own **R39–R113** and their entries are cited as `[R#]`, never re-created:

| Block | File | Owns |
|---|---|---|
| R39–R49 (R50–R52 unused) | `solvency-uk-technical-provisions.md` | Valuation Part, TPFR Part, risk margin, surplus funds, recoverables |
| R53–R60b | `solvency-uk-discounting-and-transitionals.md` | risk-free curve, VA, MA mechanics, TMTP/TMIR |
| R61–R73 | `solvency-uk-scr-standard-formula.md` | SCR General Provisions and Standard Formula Parts, USP |
| R77–R83d | `solvency-uk-own-funds-mcr-and-internal-models.md` | Own Funds, MCR, RFF/surplus-funds capital chain, internal models |
| R84–R98 | `solvency-uk-reporting-governance.md` | Reporting Part, templates, CGB, ORSA, audit |
| R99–R113 | `uk-accounting-and-tax.md` | FRS 102/103, Sch 3, IFRS 17, FA 2012, deferred tax |

**Numbers used: R114–R120. Numbers R121–R133 are left unused by design.** Almost every source this
stream needed was already numbered by a sibling — that is the expected outcome for a synthesis stream,
and the library's convention is to leave the tail of a block spare rather than mint duplicate numbers
for documents that already carry one. In particular:

- The **With-Profits Part** of the PRA Rulebook is already **[R80]** (own-funds stream). It is cited
  here in depth, not renumbered.
- **SS14/15 *With-profits*** already carries **two** numbers — **[R71]** (SCR stream, chapter 2) and
  **[R80b]** (own-funds stream, chapter 2 plus the full PDF). That collision is a pre-existing defect
  in the library's numbering, recorded in Gaps. This file cites **[R80b]** for the whole supervisory
  statement, because that entry's own metadata claims the full PDF, and **[R71]** where the point is
  the `SCR-SF 9` link. A third number is **not** created.
- The **Surplus Funds Part** is **[R45]/[R79]**; **SS13/15** is **[R46]/[R79b]**; **SS5/24** is
  **[R47]**; **SS18/16** is **[R48]**; the **Glossary** is **[R43]**; the restatement instrument
  PRA2024/13 is **[R42]/[R63]**; the revoked Delegated Regulation is **[R49]/[R66]**.

**What this stream owns.** The product-level questions the generic streams deliberately left open:
which SCR module each UK protection product sits in; how the with-profits benefits reserve heritage
relates to current rule; how the unit/non-unit ("sterling") decomposition maps onto a Solvency UK best
estimate and what unit matching is; which liabilities reach an MA portfolio and by which route; the
direction of the lapse stress per product; whether a negative best estimate is floored, and by which
ledger; contract boundaries per product; and the **full applicability matrix** that the downstream
`uk/regulatory/` explainer and the seven per-product "Statutory accounting and capital" sections are
written from.

**Deliberately left to sibling streams.** All rule *mechanics* — stress sizes, correlation matrices,
the MA calculation, the risk-margin formula, own-funds tiering arithmetic, template row definitions,
IFRS 17 measurement, the I-E computation. This file cites them and applies them to products.

### Five retrieval facts that change how this material must be documented

1. **The line-of-business list the SCR Parts key on is retrievable after all.** The SCR stream
   recorded that "the Annexes to the SCR – Standard Formula Part were NOT retrieved" [R73] and
   therefore marked the UK health/life classification of critical illness `?`. Cross-reading the
   restatement instrument PRA2024/13 [R42] shows the SCR-SF rule text using the **same numbering** as
   **TPFR Annex 1** (`SCR-SF 3.18(3)` cites "lines of business 9, 21 and 28" for credit and suretyship;
   `3A10` cites "lines of business 5 and 17" for motor hail — both exactly the Annex 1 assignments
   [R41]). On the retrieved evidence the numbered lines of business in the SCR Parts **are** the
   TPFR Annex 1 lines. *This is a drafter's inference from consistent cross-references, not a
   statement in any retrieved document; see Gaps.*
2. **The UK Glossary definitions that decide the life/health split were retrieved** from PRA2024/13
   [R42] — `health insurance obligation`, `income protection insurance obligation`, `medical expense
   insurance obligation`, `SLT health`, `NSLT health`. They are transcribed in §12 below. Together
   with (1) they let this file **resolve** the standalone-critical-illness question that [R62] and
   [R89] left open — as a **derivation from the definitions**, with the chain shown, and with the
   honest record that **no retrieved document states the conclusion**.
3. **INSPRU 1.3 is marked "Deleted" in the FCA Handbook**, last updated 31/12/2015 [R116]. The
   with-profits benefits reserve / future policy related liabilities apparatus is therefore **not
   current UK prudential rule**. It survives in exactly two live places: as the anchor of FRS 103's
   *realistic value of liabilities* definition, which points at "rule 1.3.40 of INSPRU **as at
   31 December 2015**" [R99]; and as the vocabulary of the PRA's **IR.12.06** with-profits reporting
   template, whose rows are defined by cross-reference to **Surplus Funds 3.2/3.3/3.4**, not to
   INSPRU [R90]. Any document in this library that describes a WPBR must say which of those two it
   means.
4. **INSPRU 1.2 is still in force but expressly does not apply to a Solvency II firm.** The
   application rule (as at 01/01/2021) reads: "INSPRU 1.2 applies to a long-term insurer unless it
   is: (1) a non-directive friendly society; or (2) [deleted]; (3) [deleted]; **(4) a Solvency II
   firm**" [R115]. The Solvency I guaranteed-surrender-value floor on mathematical reserves
   (INSPRU 1.2.62R) therefore has **no application to any product in this library** as written by a
   UK Solvency II firm — which is the cleanest possible confirmation of the technical-provisions
   stream's finding that Solvency UK floors nothing [R41 §17].
5. **FCA Handbook COBS 20.2 could not be re-fetched this session** (HTTP 500, then a fetch that
   returned COBS 20.3 content). Every COBS 20 statement below is either carried from the frozen
   **[R9]** entry (COBS 20.2 and 20.3 read 2026-08-03) or from the PRA's own cross-reference inside
   the IR.12.05 instruction file [R90]. No COBS 20.2 rule number is asserted from memory.

---

## Existing entries (R1–R38, and sibling-stream entries) that bear on this stream

**Frozen block.**
- **[R1] Technical Provisions Part** — TP 9.1(3) future discretionary bonuses inside TP unless within
  Surplus Funds 2.1; TP 9.2 options and guarantees; TP 10.1 segmentation.
- **[R2] Matching Adjustment Part** — MA 1.2 *eligible element* (with-profits guaranteed annuity
  element; IP in-payment element); MA 2.2 eligibility conditions; MA 2.5 future-premium carve-out.
- **[R3] TMTP Part**, **[R4] SI 2023/1346 risk margin**, **[R5] PS10/24**, **[R6] PS15/24**,
  **[R7] PS2/24**, **[R8] SS7/18** — cited for per-product incidence only.
- **[R9] FCA COBS 20 — With-profits.** The PPFM regime; COBS 20.2 fair-treatment and payout rules;
  COBS 20.3.6 PPFM content table. The conduct constraint that makes with-profits discretion a
  *modellable* management action rather than free judgement, and the rule the PRA's IR.12.05
  reversionary-bonus row points at (COBS 20.2.17R) [R90].
- **[R10] FCA COBS 21.3 — permitted links.** Applies where investment risk is borne by a natural
  person (21.3.-1); benefits may be linked only to an approved index or the listed permitted-property
  categories (21.3.1R), classified by **economic substance over legal form** (21.3.1A).
- **[R12] FCA PRIN 2A Consumer Duty** — the price-and-value overlay behind IR.12.06's
  "non-contractual commitments … including liabilities arising from the regulatory duty for firms to
  treat customers fairly" row [R90].
- **[R14] RAO 2001 Sch 1 Pt II** — the long-term classes: I life and annuity; II marriage and birth;
  **III linked long term**; **IV permanent health**; V tontines; VI capital redemption; **VII pension
  fund management**; VIII collective insurance; IX social insurance. Load-bearing twice over: it
  scopes the **70% mass-lapse limb** (`SCR-SF 3B6.6(1)`, class VII only, after the [R64] correction)
  and it is the fallback line-of-business rule in TPFR 26.4.
- **[R15] ITTOIA 2005 Pt 4 Ch 9 / [R16] IPTM** — chargeable-event gains; the 5% withdrawal pattern
  that drives ULB and WP-bond policyholder behaviour.
- **[R17] FA 2012 Pt 2 / [R18] LAM** — BLAGAB / non-BLAGAB per product.
- **[R22]–[R32] CMI and ONS** — the assumption bases the SCR stresses are applied *to*.
- **[R33]–[R35] TAS 100 / TAS 200 / APS L1** — APS L1 is where the **With-Profits Actuary** role
  sits, alongside Actuaries 5.1 / SMF20a [R93][R94].

**Sibling-stream entries.**
- **[R39] Valuation Part**, **[R41] TPFR Part + Annex 1**, **[R42]/[R63] PRA2024/13**, **[R43]
  Glossary** — definitions, contract boundaries, LoB taxonomy, cash flows in scope, FDB, management
  actions.
- **[R45]/[R79] Surplus Funds Part**, **[R46]/[R79b] SS13/15** — the estate/technical-provisions
  boundary and the retrospective (asset share) vs prospective valuation routes.
- **[R47] SS5/24 funded reinsurance**, **[R48] SS18/16 longevity risk transfers** — annuity-book
  reinsurance.
- **[R49]/[R66] revoked DR (EU) 2015/35** — provenance of the definitions restated in [R42].
- **[R53] IRPR Regulations 2023**, **[R57] TMIR**, **[R60] SoP8/24 MA permissions** — permission layer.
- **[R61] SCR General Provisions**, **[R62] SCR Standard Formula**, **[R64]** the mass-lapse
  correction, **[R65] USP Part**, **[R71] SS14/15 ch.2** — the module structure and every stress size.
- **[R77] Own Funds Part** (3A.1(1)(d) surplus funds as Tier 1; 3L RFF deduction), **[R78] MCR Part**
  (the `TP_l1`–`TP_l4` + CAR linear formula), **[R80] With-Profits Part**, **[R80b] SS14/15**,
  **[R80c] EIOPA RFF guidelines**, **[R81] SCR Internal Models**.
- **[R84] Reporting Part**, **[R89] IR.12.01/12.04/14.01**, **[R90] IR.12.05/12.06/05.03/05.10**,
  **[R91] MA returns** — including the **PRA life product code list** this stream maps products onto.
- **[R92] Conditions Governing Business**, **[R93] Actuaries Part**, **[R94] SMF Parts**,
  **[R95] SS19/16 ORSA**.
- **[R99] FRS 103**, **[R100] FRS 103 Implementation Guidance**, **[R102] FRS 102**,
  **[R105] SI 2008/410 Sch 3**, **[R106] UKEB ECA on IFRS 17**, **[R111] Valuation 11 deferred tax**,
  **[R112] SCR-SF 6 LACTP/LACDT**.

---

## New entries

Numbering runs **R114–R120**. **R121–R133 unused by design.**

### A. The asset side of a product: linked matching and the prudent person principle

#### R114. PRA Rulebook — **Investments Part** (as at 05/08/2026)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.prarulebook.co.uk/pra-rules/investments
- **Doc type:** PRA Rulebook Part. **Accessed:** 2026-08-06.
- **fetched_ok:** yes (9,717 chars, local copy `s5-investments.txt`; browser-UA fetch — plain fetchers
  get HTTP 403 from prarulebook.co.uk). Chapters 1–5 read in full; Chapter 6 (repackaged loans) skimmed.
- **Annotation:** The Part that decides **what assets a unit-linked liability must be backed by**, and
  therefore the whole unit-matching question. Verified rule text:
  **3.1** [01/01/2016] assets held to cover technical provisions must be "invested in a manner
  appropriate to the **nature and duration** of the firm's insurance and reinsurance liabilities and in
  the best interests of all policyholders, taking into account any disclosed policy objectives"
  [Art. 132(2) SII].
  **4.1** the chapter does not apply to a pure reinsurer; **4.2** it applies additionally where a firm
  carries out **linked long-term contracts of insurance**; **4.3** the firm "must cover its technical
  provisions **in respect of its linked long-term liabilities as closely as possible** with (1) where
  the linked benefits are linked to the value of **units**, **those units**; (2) where linked to the
  value of assets in an **internal fund** — (a) the assets represented by the notional units, or (b)
  where notional units are not established, those assets; and (3) where linked to a **share index or
  other reference value**, assets of appropriate security and marketability corresponding as closely as
  possible to the assets on which the reference value is based" [Art. 132(3) SII].
  **5.1** Chapter 5 does **not** apply to assets covering technical provisions for linked long-term
  contracts **unless and to the extent that** the assets are held to cover the technical provisions in
  respect of **any guarantee of investment performance or other guaranteed benefit** provided under
  those contracts [Art. 132(3)–(4) SII]. **5.2** the non-linked requirements: derivatives and
  quasi-derivatives only where they reduce risk or facilitate efficient portfolio management;
  non-regulated-market assets kept to prudent levels; proper diversification avoiding excessive
  reliance on any asset, issuer, group or geographical area and excessive accumulation of risk in the
  portfolio as a whole; no excessive single-issuer concentration.
  Chapter 1 definitions (`original lender`, `originator`, `sponsor`, by cross-reference to
  Securitisation 1.3) are date-stamped 31/12/2024 with a **future version after 01/01/2027** — not
  retrieved.
- **Products:** ULB decisively (4.3(1) is the unit-matching rule; 5.1 is the guarantee carve-out);
  WP and PA via 3.1 and 5.2; all products via Chapters 2–3 at portfolio level.

#### R119. SS1/20 — *Solvency II: Prudent Person Principle* (November 2024, updating June 2024)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/supervisory-statement/2024/ss120-november-2024-update.pdf
  (landing page: https://www.bankofengland.co.uk/prudential-regulation/publication/2020/solvency-ii-prudent-person-principle-ss)
- **Doc type:** supervisory statement (PDF). **Accessed:** 2026-08-06.
- **fetched_ok:** yes (47,081 chars via the browser-UA helper; contents page and chapter 1 read in
  full, chapters 2–8 keyword-searched only).
- **Annotation:** Published **15 November 2024, effective 31 December 2024**. Contents verified:
  1 Introduction; 2 Investment strategy; 3 Investment risk management (investment risk management
  policy, counterparty risk, risk concentration / risk accumulation / lack of diversification);
  4 Outsourcing of investment activities; 5 Exposures to non-traded assets; 6 Valuation uncertainty;
  7 Intragroup loans and participations; 8 Outwards reinsurance; Annex – SS1/20 updates. Verified
  ¶1.6: the PRA rules require that "as regards investment risk, a firm must demonstrate that it
  complies with the Investments Part of the PRA Rulebook" (footnote: **Conditions Governing Business
  3.4** [R92]). Verified ¶1.7: a breach of the PPP may be associated with a failure to meet Conditions
  Governing Business or **Matching Adjustment** Part requirements — "the MA eligibility conditions
  (which firms should comply with at all times) require compliance with the **PPP at the level of both
  the asset and portfolio**" (footnote: **Matching Adjustment 2.2(6) and 13.2**); and where an MA
  eligibility breach "is not rectified for more than two months" the PRA may consider necessary changes
  to the MA permission, "which may be in addition to the reduction to the MA required by **Matching
  Adjustment 13.5**" [R2]. Verified ¶1.8 and footnote 28: the rules apply at different granularities —
  Investments **5.2(1)** requires consideration of **each** derivative and quasi-derivative, while
  Investments **2.1(2)** expressly requires consideration of security, quality, liquidity and
  profitability at **whole-portfolio** level.
  **Negative finding, recorded deliberately:** a keyword search of the retrieved text returns **no**
  occurrence of "unit-linked", "unit linked", "with-profits" or "ring-fenced". SS1/20 contains no
  unit-linked-specific or with-profits-specific guidance.
- **Products:** PA (the MA / PPP link at asset *and* portfolio level, and the two-month rectification
  expectation); ULB and WP through Investments 2–5 generally.

#### R120. SS20/16 — *Solvency II: reinsurance – counterparty credit risk*
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.bankofengland.co.uk/prudential-regulation/publication/2016/solvency2-reinsurance-counterparty-credit-risk-ss
- **Doc type:** supervisory statement (landing page). **Accessed:** 2026-08-06.
- **fetched_ok:** **partial — landing page only (2,306 chars); the PDF was NOT retrieved.**
- **Annotation:** Recorded because UK protection business (TA, CI, IP) is the most heavily reinsured
  business in this library and therefore carries the largest counterparty-default exposure, and because
  two already-numbered documents point at it: SS18/16 ¶2.1 [R48] refers readers to "SS20/16, 'Solvency
  II: reinsurance – **counterparty default risk**'", and SS1/20 footnote 22 [R119] links the May 2024
  version. Verified from the landing page: addressed to all UK Solvency II firms and to Lloyd's; sets
  out PRA expectations "with respect to general issues regarding reinsurance and the management of
  reinsurance counterparty credit risk"; first published **25 November 2016**; **current version
  published 15 November 2024, effective 31 December 2024**, following PS15/24 [R6]; past versions
  23 May 2024 (following PS8/24) and 25 November 2016 (following PS33/16).
  **Everything else about SS20/16 is [unverified]** — no paragraph text was retrieved. Note the title
  discrepancy between the landing page ("counterparty **credit** risk") and SS18/16 ¶2.1 ("counterparty
  **default** risk").
- **Products:** TA, CI, IP (heavy reinsurance); PA via longevity swaps [R48] and funded reinsurance
  [R47].

### B. The with-profits heritage — what is legacy and what is live

#### R115. FCA Handbook — **INSPRU 1.2, *Mathematical reserves***
- **Publisher:** Financial Conduct Authority
- **URL:** https://www.handbook.fca.org.uk/handbook/INSPRU/1/2.html
- **Doc type:** FCA Handbook sourcebook chapter. **Accessed:** 2026-08-06.
- **fetched_ok:** yes (two WebFetch passes; the application rule and rules 1.2.62 / 1.2.62A quoted back
  verbatim; the full chapter was **not** read).
- **Annotation:** The **Solvency I** valuation rules for long-term insurers — still live in the FCA
  Handbook but **expressly disapplied to Solvency II firms**. Verified application rule (rendered with a
  01/01/2021 date-stamp): "INSPRU 1.2 applies to a long-term insurer unless it is: (1) a non-directive
  friendly society; or (2) [deleted]; (3) [deleted]; **(4) a Solvency II firm**." Verified **INSPRU
  1.2.62 R** [31/12/2006]: a firm must include in its mathematical reserves an amount to cover any
  increase in liabilities that might be the direct result of a policyholder exercising an option under
  the contract, and "**Where the surrender value of a contract is guaranteed, the amount of the
  mathematical reserves for that contract at any time must be at least as great as the value guaranteed
  at that time.**" Verified **INSPRU 1.2.62A G** [31/12/2006]: a contract has a guaranteed surrender
  value where the policy wording states a surrender value is payable and either provides a minimum
  amount or a method of calculating one; "For example, where a **unit-linked contract** provides for a
  surrender value equal to the value of the units allocated to the contract, the firm must establish
  mathematical reserves for that contract **greater than or equal to the value of the units allocated
  at the valuation date**." Other rule numbers visible on the page: 1.2.6 / 1.2.6A (Purpose,
  26/06/2026), 1.2.10 (Methods and assumptions, 26/06/2026), 1.2.20–1.2.21 (Record keeping),
  1.2.28–1.2.31 (Cash flows to be valued), 1.2.59–1.2.72, 1.2.86.
- **Products:** ULB and unit-linked WOL (the legacy unit-reserve floor Solvency UK does **not** carry);
  all products, as the historical contrast to TP 3.1 [R1].

#### R116. FCA Handbook — **INSPRU 1.3, *With-profits insurance capital component*** (**Deleted**)
- **Publisher:** Financial Conduct Authority
- **URL:** https://www.handbook.fca.org.uk/handbook/INSPRU/1/3.html
- **Doc type:** FCA Handbook sourcebook chapter, **deleted**. **Accessed:** 2026-08-06.
- **fetched_ok:** yes — but the page carries **no rule text**. It renders as "Deleted", with the note
  that "INSPRU 1.3 With-profits insurance capital component was last updated on **31/12/2015**".
- **Annotation:** The provenance entry for the entire **realistic balance sheet / with-profits benefits
  reserve (WPBR) / future policy related liabilities (FPRL)** vocabulary. Verified: the chapter is
  deleted and its last update was 31/12/2015 — it fell away with Solvency II implementation. **No rule
  text of INSPRU 1.3.40 (realistic value of liabilities), 1.3.190 (realistic current liabilities), or
  any WPBR / FPRL definition was retrieved, and none is asserted anywhere in this file.** The chapter
  nevertheless remains operative in one live place: FRS 103's glossary defines *realistic value of
  liabilities* by reference to "rule 1.3.40 of INSPRU **as at 31 December 2015**", excluding current
  liabilities within rule 1.3.190 as at the same date, and the FRC recorded that it kept the
  INSPRU-anchored definitions deliberately because preparers "would need to refer to INSPRU as at
  31 December 2015 in order to continue with their existing accounting policies" [R99 BC49–BC50].
- **Products:** WP (definitional heritage); WOL and PA written in participating form.

#### R117. SS1/14 — *Mutuality and with-profits funds: a way forward* (November 2024, updating November 2015)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.prarulebook.co.uk/guidance/supervisory-statements/ss01-14-mutuality-and-with-profits-funds-a-way-forward
  (listed as a "Related link — Guidance" on the With-Profits Part page [R80]; local copy `s5-ss114.txt`)
- **Doc type:** supervisory statement (PDF text). **Accessed:** 2026-08-06.
- **fetched_ok:** yes (20,563 chars; Introduction, Background and "Change in regulatory landscape"
  read in full; the waiver-process and "Interaction with Solvency II" sections skimmed). **The exact
  retrieval URL used by the earlier fetch pass is not recorded in the local file — treat the URL above
  as the Rulebook guidance path and re-verify before citing it in a published document.**
- **Annotation:** Verified contents: Introduction; Background; Change in regulatory landscape since
  CP12/38 was issued; Scope of supervisory statement; The PRA and the mutual with-profits waiver
  process; **Interaction with Solvency II**. Verified substance: the statement "is relevant for all
  mutual insurance firms and friendly societies writing new with-profits business or with existing books
  of with-profits business" (¶1.1); it responds to FSA **CP12/38** (December 2012), which proposed that
  COBS 20 explicitly recognise a **mutual members' fund** identified within a common with-profits fund,
  to which COBS 20 would not apply directly, achieved by a waiver under **FSMA s.148** (¶2.2); the
  underlying concern was that COBS **20.2.55R and 20.2.56R** were prescriptive enough that mutuals
  writing with-profits out of a common fund (in which policyholder and member interests are co-mingled)
  risked having to close to new business and go into run-off (¶2.1); after the 1 April 2013 split, most
  of COBS 20 — including 20.2.55R/56R — sits **solely in the FCA Handbook**, while "a limited number
  (including the **definition of a 'with-profits fund'**) also appear in the PRA Rulebook since they
  embody prudential matters relevant to the PRA's objectives" (¶3.2). SS14/15 ¶2.2 cites SS1/14 as the
  origin of the PRA's position that each with-profits fund generally displays RFF characteristics
  [R80b].
- **Products:** WP (mutual and common-fund variants). ¶3.2 is the general authority for *why* some
  with-profits definitions live in the PRA Rulebook and the rest in COBS 20 [R9].

### C. Secondary literature — unit matching

#### R118. Milliman research report — *The benefits of Solvency II unit matching* (July 2018)
- **Publisher:** Milliman (Emma Hutchinson FIA FSAI, Fred Vosvenieks FIA CERA, Magnus Wilson FIA; with
  Paul Turnbull FIA, P Turnbull Financial Management)
- **URL:** **not recorded in the local copy.** The document is a Milliman research report titled "The
  benefits of Solvency II unit matching", July 2018; local copy `s5-milliman-unitmatching.txt`.
  **No URL is asserted here — the retrieving fetch did not preserve one, and this library does not
  fabricate URLs. Re-derive and verify the URL before citing this entry in a published document.**
- **Doc type:** **secondary** — consultancy research report, not a rule or regulator publication.
  **Accessed:** 2026-08-06.
- **fetched_ok:** yes (74,472 chars; executive summary and sections 1–2 read in full; sections 3–4
  skimmed).
- **Annotation:** Cited **only** as evidence of how the UK market reads Investments 4.3 [R114], and for
  the vocabulary of the unit / non-unit split — never as authority for a rule. Verified content: under
  Solvency I "the Mathematical Reserves for unit-linked business had to be at least equal to the
  surrender value of the in-force contracts at the valuation date" (its citation: FCA Handbook **INSPRU
  1.2.62A**) and the unit-linked element of those reserves had to be covered by unit-linked assets (its
  citation: **INSPRU 1.5.35**); under Solvency II "the unit-linked Technical Provisions would normally
  be **less than the surrender value** of policies at the valuation date as credit can be taken for the
  expected value of future charges and **there is no floor related to the surrender value specified in
  the rules**". Its working assumption, "which has also been made by firms in practice", is that
  Investments 4.3 applies to technical provisions **held in respect of linked benefits**, not to all
  liabilities arising from linked contracts (such as administration expenses) — supported by the
  Rulebook definition of *linked long-term liabilities* as "the insurance obligations in respect of
  **linked benefits** under a linked long-term contract of insurance" and by the wording of Art. 132(3)
  SII. Its decomposition: the unit-linked component of the BEL equals the current surrender value (or
  unit-linked benefit) **less** the present value of expected future annual management charges on
  **existing** unit funds (excluding AMCs on units to be bought by future expected premiums), that PV
  computed on the full decrement basis; only that component must be covered with unit-linked assets,
  while non-linked liabilities such as administration expenses "can be backed with alternative and
  perhaps more suitable investments"; the risk margin ideally splits the same way but "in practice it
  may be difficult", and treating all of it as unit-linked "will not lead to a material misstatement as
  **lapse risk is typically the main component of the Risk Margin for unit-linked business**".
  **Conflict recorded, not resolved:** Milliman attributes the Solvency I surrender-value floor to
  **INSPRU 1.2.62A**, which the FCA Handbook renders as **guidance (G)** giving a unit-linked worked
  example; the operative **rule** is **INSPRU 1.2.62 R** [R115]. The substantive point survives; the
  citation is one rule number out.
- **Products:** ULB decisively; unit-linked WOL and the unit-linked element of a unitised with-profits
  contract by extension.

---

## Extracted mechanics

### 1. The master product map — one row per library product

The seven representative designs, as specified in `uk/products/*/product-spec.md` and
`technical-notes.md`, mapped onto every classification a Solvency UK model must carry. **Every cell is
sourced or marked as a derivation.** RAO class is from [R14]; line of business from TPFR Annex 1 [R41]
applying TPFR 26.2/26.3; SCR module from `SCR-SF 3.2A` and `3.10B` [R62][R42] (see §12); PRA product
code from the IR.14.01 appendix [R89]; MCR term from MCR 3C.1 [R78]; tax basis from [R17][R18]; IFRS 17
model from [R106].

| | **TA** term assurance | **CI** critical illness | **IP** income protection | **WOL** whole of life | **WP** with-profits | **ULB** unit-linked bond | **PA** pension annuity |
|---|---|---|---|---|---|---|---|
| Representative design | guaranteed-premium level/decreasing term, no surrender value | accelerated (base) and standalone (variant); guaranteed or reviewable premiums | full-term guaranteed-premium own-occupation, 3-state H/S/D, claims in payment | RefWOL-UW underwritten + RefWOL-O50 over-50s guaranteed acceptance (no surrender value) | unitised WP bond (primary) + conventional WP endowment (legacy) + smoothed fund | single-premium onshore bond, 100.1% of bid value death benefit | single-premium annuity in payment, guarantee period **XOR** value protection |
| RAO Sch 1 Pt II class [R14] | I | I (accelerated, following the life base) / **IV or I** (standalone — see §12) | **IV** permanent health | I (or III if unit-linked) | I | **III** linked long term | I |
| Annex 1 line of business [R41] | **32** | **29** if long-term technical basis (derivation, §12); the base contract's 32 if inseparable | **29** if long-term basis; **2** if general-insurance basis (TPFR 26.3) | **32** non-profit; **30** with-profits; **31** unit-linked | **30** | **31** | **32** |
| SCR module [R62 3.2A] | life `3B` | **health `3C` (SLT)** on the derivation in §12 — *no retrieved document states this* | **health `3C` (SLT)** for individual long-term IP | life `3B` | life `3B` | life `3B` | life `3B` |
| PRA product code [R89] | 404 / 414 / 424 / 434 | 444 / 454 accelerated (guaranteed / reviewable); 464 / 474 standalone | 494 / 504 / 514; **524 claims in payment**; 480 CWP, 481 Holloway UWP | 104 NP; 102 UL; 100 CWP; 101 UWP | 111 SP bond UWP; 100 / 101; 120 / 121 endowment | **112** SP bond UL (113 IL, 114 NP) | 724 NP; 734 enhanced NP; 720 WP; 722 UL |
| MCR linear term [R78 3C.1] | `TP_l4` + `CAR` | `TP_l4` + `CAR` | `TP_l4` (+ `CAR` on the disability limb — see note) | `TP_l4` + `CAR` (non-profit); `TP_l1`/`TP_l2` if WP | `TP_l1` + **`TP_l2` (negative coefficient)** | `TP_l3` | `TP_l4` |
| Discount curve | basic risk-free | basic risk-free | basic risk-free; **MA** on the in-payment element [R2] | basic risk-free | basic risk-free; MA on a guaranteed annuity element [R2] | basic risk-free (non-unit only) | **risk-free + MA** [R2] |
| Fund / perimeter | shareholder fund | shareholder fund | shareholder fund; MA portfolio for claims in payment | shareholder fund, or a WP fund if participating | **ring-fenced with-profits fund** [R80b ¶2.2] | shareholder fund; **not an RFF** [R80c Guideline 2(a)] | **MA portfolio** (not an RFF) [R43 glossary] |
| Tax basis [R17][R18] | non-BLAGAB trade (post-2012) | non-BLAGAB trade (post-2012) | non-BLAGAB trade (post-2012) | BLAGAB I-E | BLAGAB I-E | BLAGAB I-E | **non-BLAGAB** (pension business) |
| IFRS 17 model [R106] | GMM (PAA possible for short-term) | GMM | GMM | GMM (VFA if participating) | **VFA** | **VFA** | GMM; coverage-unit basis **unsettled** [R106 §3 issue A] |

Two cells need immediate qualification, both recorded rather than resolved:

- **CI's RAO class.** [R14] verifies the class list, not the assignment of a UK CI contract to a class.
  An accelerated CI benefit is part of a Class I life contract. A standalone CI lump sum could be
  argued into Class **IV** (permanent health) or Class **I**; the RAO text retrieved does not name
  critical illness. `[unverified]` as to the assignment.
- **IP's MCR capital-at-risk.** MCR 3C.1(5)(a) defines `CAR` by what the firm "would currently pay on
  **death or disability** of the persons insured" [R78]. The disability limb is engaged for IP, but the
  rule does not say how to express an income stream as a "currently payable" amount. Recorded, not
  resolved (this is the own-funds stream's `(x)` on that row [R78 notes], carried forward here).

### 2. With-profits — the fund perimeter, and where each rule lives

**The PRA Rulebook With-Profits Part is four rules long** [R80] (all date-stamped **01/01/2016**;
retrieved in full, 3,632 chars):

- **1.1** the Part applies to a UK Solvency II firm **carrying on with-profits insurance business**;
  **1.2** it does **not** apply to with-profits insurance business consisting of effecting or carrying
  out **Holloway sickness policies**.
- **2.1** a firm "must ensure that it holds assets in each of its **with-profits funds** of a value
  sufficient to cover the **with-profits policy liabilities** in respect of all of the business written
  in, or transferred into, that with-profits fund".
- **3.1** the firm must ensure **at all times** that its strategy for distribution of discretionary
  benefits in respect of each with-profits fund **(1) is affordable and sustainable**; and **(2) cannot
  reasonably be expected to have an adverse effect on the safety and soundness of the firm as a whole,
  or on the benefit security of all policyholders of the firm**.
- **4.1** where a firm is using or intends to use **support arrangements** to contribute to benefit
  security for the policyholders of a with-profits fund, it must ensure (1) all terms and conditions
  governing them — including the circumstances in which they take effect and the terms on which they
  are or may be repayable — are **adequately documented in the firm's records**, and (2) the extent of
  any **restrictions on the firm's use** of those arrangements is clearly identified.

That is the *entire* prudential with-profits rule set. Everything else that governs a UK with-profits
fund sits in one of five other places, and a drafter must not blur them:

| Where | What it governs | Entry |
|---|---|---|
| **FCA COBS 20** | PPFM, fair payouts, target ranges, MVRs, the required percentage, the mutual-fund rules 20.2.55R/56R | [R9], [R117 ¶3.2] |
| **Technical Provisions 9.1(3) + Surplus Funds Part** | which discretionary payments are inside technical provisions and which are excluded as surplus funds | [R1], [R45]/[R79], [R46]/[R79b] |
| **Own Funds 3A.1(1)(d), 3L** | surplus funds as a Tier 1 item; the ring-fenced-fund deduction from the reconciliation reserve | [R77] |
| **SCR-SF 2.2, 9.1** | the notional-SCR-per-RFF machinery and the loss of diversification | [R62], [R71] |
| **SS14/15** | the PRA's expectation that each with-profits fund *is* an RFF; support arrangements; distribution strategy; investment strategy; reattributions | [R80b] |

**SS1/14 ¶3.2 is the sentence that explains the split** [R117]: after the 2013 FSA break-up, the COBS
20 rules aimed at fair treatment sit **solely in the FCA Handbook**, while "a limited number (including
the definition of a 'with-profits fund') also appear in the PRA Rulebook since they embody prudential
matters relevant to the PRA's objectives."

**SS14/15, chapters other than chapter 2** [R80b] — read for this stream and recorded here because the
sibling entries only annotate chapter 2:

- **¶1.1** the SS is directed to **all UK firms that write with-profits insurance business**. **¶1.2**
  firms must have regard to (a) for Solvency II firms the PRA Rulebook **including ring-fenced fund
  provisions** (and for non-Directive firms any PRA-designated rules in prudential sourcebooks),
  (b) relevant supervisory statements, and (c) the **FCA Handbook**.
- **Chapter 3, support arrangements.** ¶3.2 firms should consider whether support arrangements fall
  within the RFF requirements, having regard to their terms and to "the extent of any restrictions on a
  firm's use of assets associated with support arrangements, and **the expected availability of such
  assets in stressed conditions**". ¶3.3 where the terms state clearly that support is for the
  **exclusive use** of a with-profits fund, the PRA expects that arrangement to be **treated as an RFF**
  and its assets to **form part of the RFF constituted by the with-profits fund receiving support**;
  support is "exclusive" if under the arrangement it **cannot be used to meet losses arising in other
  areas of the business**. ¶3.4 where support is **not** exclusive, the associated assets should not
  generally form part of the RFF, and the extent to which the PRA will permit the firm to recognise and
  use them as financial resources available to the with-profits fund depends on the PRA's view of the
  financial strength of the overall firm, the risks involved, the degree of reliance placed on the
  support, and "the ability of the arrangement to support the with-profits fund **in periods of
  stress**"; in certain circumstances the PRA might expect the firm to **identify specific support
  assets and include them within the RFF in advance of drawing on the arrangement**.
- **Chapter 4, affordability and sustainability.** ¶4.1 the PRA expects firms **not to make
  distributions from with-profits funds which could endanger the safety and soundness of the overall
  firm, or which could have a significant negative impact on the benefit security of any group of
  policyholders**. ¶4.2 firms "should not set with-profits distribution strategies which **accelerate
  the transfer of profits outside the with-profits fund** and which increase shareholder distributions
  while posing increased risk to benefit security and the safety and soundness of the firm", including
  in **special / one-off distributions**. ¶4.3 affordability must give due consideration to
  **With-Profits 2.1** [R80].
- **Chapter 5, investment strategy.** ¶5.1 when setting a with-profits fund's investment strategy the
  PRA expects firms to take into account (a) for Solvency II firms **the prudent person principle in
  Investments 2 to 5** [R114] **and the RFF requirements in Own Funds 3L** [R77]; (b) financial
  resources requirements and the availability of capital resources; (c) applicable FCA conduct rules
  and guidance; and (d) any communication to policyholders complying with those conduct rules.
- Further chapter headings verified but **not read in depth**: Separation of different with-profits
  business; Significant changes in with-profits funds; Reducing new business sales, closing to new
  business and run-off; **Reattributions of inherited estate**; Demutualisation; With-profits mutual
  waivers; Part VII transfers.

### 3. With-profits — future discretionary benefits inside the best estimate

The chain, rule by rule, all verified by the technical-provisions and own-funds streams and restated
here in product terms:

1. **TP 9.1(3)** [R1] — technical provisions must take into account "all payments to policyholders,
   **including future discretionary bonuses**, which firms expect to make, **whether or not those
   payments are contractually guaranteed**, unless those payments fall within **Surplus Funds 2.1**".
2. **TPFR 10.1** [R41] — "a firm must **determine separately the value of future discretionary
   benefits**". FDB is therefore a **required model output**, not a reporting convenience.
3. **TPFR 9.1** [R41] — where FDB depend on the assets held, the best estimate must be based on the
   assets the firm **currently holds**, with future asset-allocation changes assumed only in accordance
   with TPFR 8 (future management actions), and assumed future asset returns **consistent with the
   relevant risk-free interest rate term structure** (including any MA, VA or risk-free transitional)
   and with the Val 2–12 valuation of the assets. *There is no assumed equity risk premium in a
   with-profits best estimate: the return is risk-neutral off the relevant curve, and the asset mix
   starts from the actual portfolio.*
4. **`SCR-SF 3.3A(1)(c)`** [R42][R62] — in any scenario-based module, the scenario **does not change
   the value of future discretionary benefits included in technical provisions**. FDB is *frozen* in
   the gross stress, and its responsiveness is reintroduced only through **`SCR-SF 6.3` LACTP**
   [R112], capped at the FDB amount.
5. **`SCR-SF 9.1(5)`** [R62] — inside an RFF with profit participation, a scenario's effect on RFF
   basic own funds is adjusted for the change in technical provisions caused by the change in FDB, the
   reduction capped at the FDB included in that RFF's technical provisions.
6. **MCR 3C.1(2)** [R78] — `TP_l2`, the FDB term, carries the **only negative coefficient in the whole
   MCR formula** (−0.052). A larger FDB reserve *reduces* MCR_linear.

**What the model must therefore produce for a with-profits contract:** guaranteed benefits and FDB as
**two separately-valued streams**, per fund, per scenario, per period — because they are discounted
together (TP 9.1(3)), reported separately (IR.12.06 [R90]), stressed differently (`3.3A(1)(c)` vs
`6.3`), and enter the MCR with opposite signs.

### 4. With-profits — the surplus-funds boundary (where the estate stops being a liability)

The Surplus Funds Part [R45]/[R79] and SS13/15 [R46]/[R79b] are the sibling streams'; only the
product-facing consequences are restated:

- **Surplus Funds 2.1** — a firm shall **not** treat surplus funds as insurance obligations when
  valuing payments to policyholders in the technical provisions.
- **SS13/15 ¶2.1** — the carve-out operates **only where the surplus funds meet the Tier 1 own funds
  requirements in Own Funds 3.1**; **¶2.3** surplus funds normally meet Tier 1 but are "likely to be
  treated as part of a ring-fenced [fund]"; **¶2.4** the surplus-funds calculation "**does not refer
  to or include a risk margin**", yet the firm must still calculate and recognise the risk margin on
  its with-profits business.
- **Surplus Funds 3.1** — surplus funds = with-profits assets − with-profits policy liabilities − tax
  and other costs on recognition of future shareholder transfers − other liabilities properly
  attributable to the fund − **the value attributable to future shareholder transfers**.
- **Surplus Funds 3.3 (retrospective)** — the regulatory **asset share**: a ten-item roll-up (premiums
  received; investment income and asset value movements; permanent enhancements; past miscellaneous
  surplus/deficit allocated; expenses incurred or deducted; past deductions for cost of guarantees and
  smoothing, options and life cover; partial benefits paid or due; tax paid or payable attributable to
  the policy; reinsurance amounts; past shareholder transfers, **less any implicit allowance for the
  value of future shareholder transfers**).
- **Surplus Funds 3.4 (prospective)** — where 3.3 "does not adequately reflect the value" or is
  impracticable: the NPV of future premiums, expenses, **planned deductions for the cost of guarantees
  and smoothing, options and provision of life cover**, the 3.5 benefits, reinsurance and tax.
  **SS13/15 ¶3.1 names whole-of-life policies** as the example where the retrospective result "might be
  negative or significantly lower than the value calculated using the prospective approach" — so a
  **with-profits whole-of-life is the archetypal prospective-route contract**.
- **SS13/15 ¶3.6** — the PRA "would not expect a firm to include within benefits payable **distributions
  from the estate**" it might make over the life of the policies in run-off. *This is the rule that
  keeps the estate out of the best estimate and inside own funds.*
- **Own Funds 3A.1(1)(d)** [R77] — surplus funds not treated as obligations under Surplus Funds 2.1 are
  a **Tier 1 (unrestricted) own funds item in their own right**.
- **[R80c] EIOPA RFF Guideline 2(g)** — "surplus funds are **not** ring-fenced solely by virtue of
  being surplus funds, but could be if they are **generated within a ring-fenced fund**." Since the PRA
  expects each UK with-profits fund to be an RFF [R80b ¶2.2], UK surplus funds are in practice
  restricted own funds.

**The consequence a model must carry:** the with-profits estate is **simultaneously** (a) excluded from
technical provisions, (b) Tier 1 own funds, and (c) restricted own funds trapped inside an RFF, so
recognised in the reconciliation reserve only up to the RFF's notional SCR (Own Funds 3L.1 [R77]). The
same number therefore appears with three different meanings on three different lines of the balance
sheet, and a with-profits model must be able to produce it once and tag it three ways.

### 5. With-profits — the WPBR heritage, stated honestly

This is the point at which UK with-profits documentation most often drifts into stating legacy practice
as current rule. The retrieved position:

**What is current rule (Solvency UK, in force):**
- Technical provisions = best estimate + risk margin; the best estimate includes FDB per TP 9.1(3),
  less surplus funds [R1][R45].
- With-profits **policy liabilities** are defined by **Surplus Funds 3.2–3.5** — the retrospective
  asset-share route with a prospective fallback [R45].
- The With-Profits Part requires assets in each with-profits fund sufficient to cover the with-profits
  policy liabilities (2.1) [R80].

**What is legacy law, no longer in force for a Solvency UK firm:**
- **INSPRU 1.3 (with-profits insurance capital component) is Deleted, last updated 31/12/2015**
  [R116]. The *realistic balance sheet* it created — with-profits benefits reserve plus future policy
  related liabilities, the WPICC, and the twin-peaks comparison — is **not** part of Solvency UK.
- **INSPRU 1.2 (mathematical reserves) expressly does not apply to a Solvency II firm** [R115]. The
  Solvency I guaranteed-surrender-value floor (1.2.62R) is legacy.

**Where the legacy vocabulary is still legally operative, and only there:**
1. **FRS 103** [R99] defines *realistic value of liabilities* by reference to **INSPRU rule 1.3.40 as
   at 31 December 2015**, and ¶3.11–3.12 require with-profits funds within the ¶3.1(b) scope to carry
   liabilities at that realistic value (adjusted to exclude the shareholders' share of projected future
   bonuses) rather than on the modified statutory solvency basis. UK GAAP therefore **still runs on the
   2015 realistic basis** while the regulatory balance sheet has moved on.
2. **The PRA's own with-profits reporting template IR.12.06** [R90] uses the WPBR/FPRL *vocabulary* but
   **re-anchors it to the live rules**: row R0010 "with-profits benefits reserve … **This item
   corresponds to with-profits policy liabilities (other than future policy-related liabilities) in
   Surplus Funds 3.2**"; R0020 asset shares "calculated retrospectively in accordance with **Surplus
   Funds 3.3**"; R0050 "prospective reserve where asset shares not applicable … in accordance with
   **Surplus Funds 3.4**". The FPRL components (R0070 future cost of contractual guarantees, R0080
   non-contractual commitments, R0090 financial options such as **guaranteed annuity rates**, R0100
   smoothing, R0110 financing, R0120 other, less R0130 planned deductions for guarantees/options/
   smoothing and R0140 planned deductions for other costs) are defined **in the instruction file
   itself**, not by cross-reference to INSPRU. R0150 total = WPBR + FPRL, tied to IR.12.01.01 R0030
   C0010.

**The drafting rule this yields:** in a Solvency UK context, "with-profits benefits reserve" means the
IR.12.06 R0010 item, which *is* Surplus Funds 3.2 policy liabilities. In a UK GAAP context, "realistic
value of liabilities" means the FRS 103 glossary term anchored to INSPRU as at 31/12/2015. These are
**two different definitions with a shared ancestry**, and the retrieved sources do not state that they
give the same number.

Two arithmetic properties of the FPRL rows, verified from the instruction file [R90] and worth carrying
into a model: **"Future cost of guarantees cannot be negative"** (R0070), and **"Future costs of
smoothing can be negative"** (R0100). Both are stated in the instructions.

### 6. With-profits — PPFM-driven management actions inside the best estimate

**TPFR 8.1** [R41] makes an assumed future management action "realistic" only where all five hold:
objectively determined; **consistent with the firm's current business practice and business strategy**
(or with a changed practice where there is sufficient evidence of change); consistent with each other;
**not contrary to any obligations towards policyholders or to legal requirements**; and taking account
of **any public indications by the firm as to the actions it would expect to take or not take**.

For a UK with-profits fund, limbs (4) and (5) are discharged by the **PPFM** [R9]: COBS 20.3 requires a
firm to establish and maintain a PPFM (per fund where appropriate), retain five years of versions,
distinguish enduring **principles** from shorter-term **practices**, and — per the COBS 20.3.6 table —
cover the methods for determining amounts payable, the **bonus-setting approach**, and the **smoothing
of maturity and surrender payments**. A published PPFM is precisely "a public indication by the firm as
to the actions that it would expect to take".

**TPFR 8.3** then demands a board-approved management-actions plan providing for: identification of the
relevant actions; the circumstances in which the firm would reasonably expect to carry out each;
**the specific circumstances in which the firm may not be able to carry out each, and how those
circumstances are reflected in the TP calculation**; the **order** in which actions would be taken and
the applicable governance; ongoing work needed to be in a position to take them; how they are reflected
in the best estimate; and internal reporting procedures. **TPFR 8.4** requires the assumptions to take
account of the **time needed to implement** each action and **any expenses caused by it**. **TPFR 8.5**
requires at least an **annual communication to the governing body**.

For the library's representative with-profits design, the management actions that must be modelled and
mapped to the plan are: **regular (reversionary) bonus declaration**; **final/terminal bonus setting**;
**smoothing**, including the target-range machinery; **market value reduction** application, with the
contractual MVR-free points (the representative design's 10th-anniversary guarantee date and 5% p.a.
MVR-free withdrawals); **investment-mix rebalancing** (constrained by TPFR 9.1 to start from the assets
actually held); and **charge / deduction levels** for the cost of guarantees, options and smoothing
(the Surplus Funds 3.4(3) "planned deductions", reported at IR.12.06 R0130 [R90]).

The **UK GAAP** side imposes the same discipline in almost the same words: FRS 103 IG1.13 [R100]
requires a stochastic with-profits valuation to take into account, **scenario by scenario**, management
actions anticipated in response to market variables (rebalancing between debt and equity, varying
policyholder charges, varying bonus policy) that must be "realistically implementable within the
scenario's timescale and **consistent with the published PPFM**". IG1.11 makes the
fair-value-or-market-consistent-stochastic measurement of options and guarantees **mandatory** for
with-profits business within the ¶3.1(b) scope; IG1.12 records that "any deterministic approach … will
generally fail to deal appropriately with the **time value** of the option".

**Professional ownership.** The With-Profits Actuary (APS L1 [R35]; Actuaries 5.1 / SMF20a [R93][R94])
is the person who advises whether the FDB and discretion assumptions are consistent with the PPFM.

### 7. With-profits — ring-fenced fund treatment and its SCR consequence

- **Glossary** [R43] — a *ring-fenced fund* is "an identifiable unit of assets and liabilities where
  the existence of a restriction on those assets in relation to those liabilities on a going concern
  basis gives rise to **restricted own funds**, **other than a matching adjustment portfolio**".
  *Restricted own funds* excludes "the value of future transfers attributable to shareholders" — which
  is why the expected future shareholder transfer is **not** trapped in the ring fence [R77].
- **SS14/15 ¶2.2** [R80b][R71] — the PRA expects that the restrictions arising from the UK
  with-profits regime "will generally mean that **each with-profits fund displays the characteristics
  of a RFF**"; **¶2.3** where sub-funds must be treated as separate with-profits funds under COBS 20
  [R9], each such sub-fund is expected to be treated as a **separate RFF**. **¶3.3** an *exclusive*
  support arrangement is itself expected to be treated as an RFF and its assets to form part of the
  supported fund's RFF.
- **[R80c] EIOPA Guideline 2(a)** — **conventional unit-linked and index-linked products are generally
  outside the scope of RFF treatment**. This is the authority for marking ULB `--` on every RFF row.
- **Own Funds 3L.1** [R77] — the reconciliation reserve is reduced by
  `max(0, restricted own funds in the RFF or MA portfolio − notional SCR of that RFF or MA portfolio)`.
  **3L.2** — where the RFF's assets, liabilities and risk are **not material**, the firm may instead
  deduct the **total** restricted own funds and (per `SCR-SF 2.2`) then need **no notional SCR**.
- **`SCR-SF 9.1`** [R62] — a notional SCR per RFF, per MA portfolio and for the remaining part; the
  firm's SCR is their **sum**; basic own funds at RFF level include **only restricted own funds**; the
  scenario selection is made so that the basic own funds of the **firm as a whole** are most negatively
  affected (9.1(6)–(7)); and **9.1(9) forbids diversification between RFFs, MA portfolios and the
  remaining part**.
- **[R80c] Guideline 9(d) and Guideline 12** — a negative worst-case notional charge is **set to zero**
  before aggregating; **Guideline 11 ¶1.25** records that the deduction bites on **MCR** coverage as
  well as SCR coverage.

**The two hits, stated separately** (following the own-funds stream): the *numerator* effect strikes
restricted own funds above the fund's notional SCR out of the reconciliation reserve; the *denominator*
effect loses the diversification credit between the with-profits fund and the shareholder fund. **A UK
with-profits insurer with three COBS 20 sub-funds runs at least four complete standard-formula
calculations and adds them.** That, not any single stress, is the architectural fact a with-profits
projection engine must be built for.

### 8. Unit-linked — permitted links, and what the fund universe may contain

**COBS 21.3** [R10] applies to linked long-term contracts where the investment risk is borne by a
**natural-person policyholder** (21.3.-1). An insurer may link benefits **only** to an approved index or
to the listed categories of permitted property (21.3.1R): approved securities, listed securities,
permitted unlisted securities, permitted land and property, loans, deposits, permitted scheme
interests, money-market instruments, cash, permitted units, stock lending, derivatives, and conditional
permitted links — classified by **economic substance over legal form** (21.3.1A).

Three consequences for a unit-linked-bond model:

1. The **fund universe is closed** in a way that a US separate-account model's is not; a permitted-link
   breach is a conduct breach, not a modelling assumption.
2. Because links are classified by economic substance, a **look-through** to the underlying assets is
   required for the market-risk sub-modules — consistent with `SCR-SF 2.3(1)` look-through [R62].
3. The natural-person scoping in 21.3.-1 means the rule does **not** reach institutional linked
   business; the library's ULB is retail, so it is squarely in scope.

**Where COBS 21.3 stops and Investments 4.3 starts.** COBS 21.3 says what a benefit may be *linked to*;
Investments 4.3 [R114] says what the *technical provisions in respect of linked benefits* must be
*covered by*. They are different obligations on different regulators' rulebooks and are frequently
conflated.

### 9. Unit-linked — the unit / non-unit ("sterling") decomposition, sourced

**The decomposition is not in any PRA rule.** No retrieved Solvency UK rule creates, requires or names
a "unit reserve", a "non-unit reserve" or a "sterling reserve". What the rules give is:

- **TP 3.1** [R1] — one best estimate: the probability-weighted average of *all* future cash flows,
  discounted. There is no mandated split.
- **TPFR 13.1(6)** [R41] — the cash-flow inventory **does** carry a dedicated item for "payments
  between the firm and **investment firms** in relation to contracts with **index-linked benefits and
  unit linked benefits**", so the unit leg is separately identified as a *cash flow*, not as a reserve.
- **Investments 4.3** [R114] — the **coverage** obligation attaches to "technical provisions **in
  respect of linked long-term liabilities**", and *linked long-term liabilities* is defined as "the
  insurance obligations **in respect of linked benefits** under a linked long-term contract of
  insurance". This is the only rule-level hook that requires the liability to be *decomposable at all*:
  a firm cannot comply with 4.3 without being able to say how much of its technical provisions is "in
  respect of linked benefits".
- **Investments 5.1** [R114] — the non-linked prudent-person requirements bite on assets covering
  linked contracts **only to the extent** they cover technical provisions "in respect of **any guarantee
  of investment performance or other guaranteed benefit**". So the rulebook itself splits a linked
  contract's provisions into a *linked-benefit* part and a *guarantee* part.
- **Sch 3 to SI 2008/410, note 26** [R105] — UK GAAP mandates the split on the face of the balance
  sheet: liabilities item **D Technical provisions for linked liabilities** covers provisions for
  liabilities relating to investment under linked policies, and "**any additional technical provisions
  constituted to cover death risks, operating expenses or other risks (such as benefits payable at
  maturity or guaranteed surrender values) must be included under item C.2**", the long-term business
  provision. **A UK GAAP balance sheet has a two-part linked liability; a Solvency UK balance sheet has
  one number that the firm must be able to split for Investments 4.3.**
- **IR.12.01** rows **R0300 / R0302 / R0304** [R89] — the reporting layer carries dedicated
  index-linked-and-unit-linked rows, so the split is also a reporting requirement.

**Market reading of the split** [R118, secondary]. Milliman's decomposition, offered as the way "firms
in practice" read Investments 4.3:

```
unit-linked component of BEL = current surrender value (or unit-linked benefit)
                             - PV of expected future AMCs on EXISTING units
                               (excluding AMCs on units bought by future premiums),
                               the PV taken over the full decrement basis
non-linked ("sterling") BEL  = PV of non-unit-related cash flows
                               (administration expenses, death strain, non-unit charges)
risk margin                  = ideally split; in practice treated as wholly unit-linked,
                               because lapse risk dominates the unit-linked risk margin
```
Only the unit-linked component must be covered with unit-linked assets; the non-linked part "can be
backed with alternative and perhaps more suitable investments". **This is a consultancy reading, not a
rule**, and the library must tag it as such. What the rules independently support is only: (a) the
split must exist for Investments 4.3/5.1 to be operable, and (b) UK GAAP requires it on the face of the
balance sheet [R105].

**Unit matching** is the practice of holding unit-linked assets equal to the *unit-linked technical
provisions* rather than to the *face value of the units* — the difference arising because the
unit-linked BEL is the surrender value **less** the PV of future charges, and because Solvency UK, unlike
INSPRU 1.2.62R [R115], imposes **no surrender-value floor**. [R118] describes the released assets as
"surplus unit-linked assets" available for disinvestment, and lists the claimed benefits (liquidity and
investment freedom, lower capital requirements, lower own-funds volatility, reduced lapse impact) and
the challenges (solvency-ratio dynamics, asset rebalancing, implementation). **None of the quantitative
claims in sections 3–4 of that paper are transcribed here**; they are consultancy analysis, not
regulatory fact.

**The direct line from legacy to current rule, verified:**

| | Solvency I (legacy) | Solvency UK (current) |
|---|---|---|
| Liability | mathematical reserves, floored at the guaranteed surrender value — for a unit-linked contract, "**greater than or equal to the value of the units allocated at the valuation date**" | best estimate per TP 3.1; **no floor of any kind** [R41 §17] |
| Rule | INSPRU 1.2.62 R, with the unit-linked example at 1.2.62A G | Technical Provisions Part [R1], TPFR [R41] |
| Applies to a Solvency II firm? | **No** — INSPRU 1.2 application rule limb (4) [R115] | Yes |
| Asset coverage | unit-linked element covered by unit-linked assets (INSPRU 1.5.35, per [R118]; **rule text not retrieved**) | Investments 4.3 [R114] |

### 10. Unit-linked — how the liability enters the capital modules

Applying the SCR stream's master table [R62 §17] to the representative single-premium bond:

- **Market risk is mostly *not* a liability revaluation.** Equity `3D9`, property `3D15.1` and spread
  `3D17` hit the unit fund on the asset side, and the linked liability moves with it. The residual
  exposure is the **present value of future charges** (the non-unit BEL), which falls when the fund
  falls. That is why the ULB's own-funds sensitivity to equity is real but is a *fee-income* exposure,
  not a *guarantee* exposure — unless a GMDB or capital-protection option is elected, in which case
  `TPFR 19.4–19.5` scenario-dependent (stochastic) valuation becomes necessary and Investments 5.1
  pulls the guarantee's backing assets into the non-linked prudent-person regime.
- **Interest-rate risk `3D5`/`3D6`** is second-order for the same reason: the unit leg is
  self-immunising, so only the non-unit charge/expense stream is rate-sensitive. The discounting stream
  records that the PRA's own materiality test for relevant currencies **excludes unit-linked technical
  provisions** [R55 ¶3.4], which is independent confirmation.
- **Lapse risk is the dominant sub-module.** All three `3B6` scenarios must be run: up ×1.5 (capped at
  100%), down ×0.5 (capped at −20 percentage points), and **mass lapse at 40%**. For a charge-funded
  bond the *up* scenario destroys future AMC income and is normally the binding one.
- **The 70% mass-lapse limb does not apply.** `3B6.6(1)` as corrected [R64] is scoped to **RAO
  Schedule 1 Part II class VII (pension fund management)** only; the reference to class III (linked
  long term) published in PS15/24 Appendix 6 was declared an **error** on 20 December 2024 and deleted
  effective 31 December 2024. **A UK unit-linked bond takes the 40% limb.** Under the uncorrected text
  it would have taken 70% — a drafter reading PS15/24 alone will get this wrong.
- **"Discontinuance" includes making a contract paid-up** (`SCR-SF 1.2` [R62]), and `3B6.8` requires
  the mass-lapse event to be computed on **the type of discontinuance that most negatively affects
  basic own funds on a per-policy basis**. Mass lapse is not "surrender 40% of policies"; it is "for
  each policy take the worst of surrender / paid-up / lapse-without-value, then apply 40% of that".
- **Operational risk splits the other way.** `SCR-SF 5.4(4)(b)` deducts `TP_life-ul` from the
  provisions leg, so a pure unit-linked book contributes **nothing** to the 0.45% provisions charge;
  instead `5.4(1)` charges **0.25 × Exp_ul**, expenses incurred in respect of unit-linked business
  [R62]. ULB is the only product in the library where the unit-linked expense leg is the operational
  charge.
- **Mortality `3B1` and life catastrophe `3B7`** bite only through the death uplift. On the
  representative 100.1%-of-bid-value design the capital at risk is **0.1% of the fund**, so both are
  immaterial but non-zero; the same arithmetic makes the MCR `CAR` term negligible for ULB.
- **No RFF, no MA, no LACTP.** EIOPA Guideline 2(a) puts conventional unit-linked outside RFF treatment
  [R80c]; MA 2.2 excludes a contract with surrender options and future premiums [R2]; and `SCR-SF 6.3`
  LACTP is capped at FDB, which a non-participating linked bond does not have [R112].

### 11. Annuities — the matching adjustment, longevity, and reinsurance

**MA eligibility is a whole-contract test that only the annuity passes.** The MA Part [R2] requires an
MA permission (2.1) and imposes eligibility conditions (2.2) including no future premiums, restricted
permitted underwriting risks, a mortality-risk exposure cap, and constraints on policyholder options.
The library's representative pension annuity is designed to pass: no premiums after outset, no
surrender value, no account value, and no policyholder options after the cancellation window — the
technical notes call this "the design property that makes the liability MA-eligible".

**Two other products reach an MA portfolio, but only through the *eligible element* route** [R2 MA 1.2]:

- **the guaranteed element of a with-profits policy that is an immediate or deferred annuity**; and
- **the in-payment element of an income protection policy** (and of a group death-in-service
  dependants' annuity, which is outside this library's seven products),

in each case where the element can be **organised and managed separately** under IRPR reg 4(6) [R53]
and would otherwise meet the eligibility conditions. **MA 2.5** disapplies the no-future-premiums
condition to the limb (1)(b) elements — IP in-payment claims — **but not** to the with-profits
guaranteed annuity element, which must still be premium-free [R2].

**SS7/18 supervisory expectations per route** [R8], carried from the discounting stream because they are
product-specific:
- **¶3.5A with-profits guaranteed annuity elements** — the component must be legally established and
  identifiable as guaranteed within the contract, separable under IRPR reg 4(6), with a detailed
  assessment showing that only contractually guaranteed elements, **not dependent on future premiums or
  future investment performance**, are included, and a **clear policy on where future attaching bonuses
  go**.
- **¶3.5B income protection** — *recovery time risk*, "the risk that policyholders in receipt of income
  protection payments take longer to recover from sickness than expected", is a **permitted underwriting
  risk**; in-payment claims under **both group and individual** IP policies may sit in an MA portfolio
  where not subject to future premiums; **there is no exposure limit on recovery time risk** (contrast
  the mortality cap); and the permission is **not** intended to admit any liability type other than IP
  claims in payment.

**Longevity in the SCR.** `3B2.1` [R62] is an instantaneous permanent **−20%** in the mortality rates
used for the technical provisions, applied **only** to policies where a decrease in mortality increases
technical provisions without the risk margin (`3B2.2`). Two product-level notes:
- The **−0.25 mortality/longevity correlation** in the life matrix `3.8(3)` is the only negative entry
  anywhere in the retrieved standard formula, and it is the reason a mixed protection-plus-annuity
  book diversifies. But `SCR-SF 9.1(9)` **removes that diversification wherever the annuity book sits
  in an MA portfolio and the protection book does not** — the two notional SCRs are simply added.
- **Revision risk `3B5.1` is normally nil for a UK pension annuity.** It bites only where benefits
  "could increase as a result of changes in the legal environment or in the state of health of the
  person insured". A level or fixed/RPI/LPI-escalating pension annuity has no such right. The **health**
  version `3C15.1` is **4%** rather than 3% and adds **inflation** as a trigger — which is why an
  index-linked IP claim annuity *is* exposed while a comparably indexed pension annuity is not.
- **Lapse is `--` for a pension annuity in payment.** There is no surrender or discontinuance right, so
  no "relevant option" under `3B6.4` and no "discontinuance" under the `SCR-SF 1.2` definition.

**Spread risk is the annuity-specific market module.** `3D25` [R62] requires an MA portfolio's spread
stress to revalue the **assets and recompute the MA** through the fundamental-spread uplift and
reduction factor — the only market sub-module in the standard formula that is a genuine liability
revaluation for an annuity writer.

**Reinsurance on an annuity book.** Three already-numbered documents govern it, and all three are
product-specific to PA:
- **SS5/24 funded reinsurance** [R47] — verified contents: 1 Introduction; 2 **Ongoing risk management**
  (counterparty internal investment limits, collateral policy, **recapture plan**); 3 **Solvency capital
  requirement** (probability of default, loss given default or downgrade, collateral, **recapture within
  MA portfolio**); 4 **Entering into and structuring** (risk assessment, basis risks, collateral
  mismatch risks, time horizon, contractual mitigations). ¶1.1 scopes it to "UK Solvency II firms that
  are **life insurers** entering into or holding funded reinsurance". *A liability model on an annuity
  book with funded reinsurance must be able to produce a **recapture** projection — the gross liability
  restored to the MA portfolio — not just a net one.*
- **SS18/16 longevity risk transfers** [R48] — ¶1.4 "the main life insurance products exposed to
  [longevity] risk are **immediate and deferred annuities**, although **certain health contracts and
  possibly with-profits funds** may also be exposed"; ¶2.1 concentration to a single or small number of
  counterparties; ¶2.3 residual risks including **basis risk, where the terms of the annuity contract
  and the risk transfer differ**; ¶3.1 the PRA expects **advance notification** of new large and/or
  complex longevity transfers, defined as those larger than business-as-usual, structurally more complex
  (e.g. insurance-linked securities, automatic reinsurance pools), or with a **material incremental
  impact on the firm's ability to meet its SCR**.
- **TPFR 24.4** [R41] — the counterparty-default adjustment carries a **loss-given-default floor of
  50%**, which lands hardest on annuity books because they carry the largest recoverables.

**Bulk purchase annuities are out of this library's scope** (see the repository README), but they are
the reason SS5/24, SS18/16 and PRA product code **754** exist; the individual pension annuity model is
the per-policy engine those books are built from.

### 12. Protection and income protection — which SCR module, and the critical-illness question

**12.1 The rules that decide it.** Three provisions, all verified from the retrieved text of the
restatement instrument PRA2024/13 [R42] and the Rulebook Part [R62]:

- **`SCR-SF 3.2A`** [31/12/2024] — a firm must apply "(1) the **non-life** underwriting risk module to
  non-life insurance and reinsurance obligations **other than health insurance obligations and health
  reinsurance obligations**; (2) the **life** underwriting risk module to life insurance and
  reinsurance obligations **other than health insurance obligations and health reinsurance
  obligations**; and (3) the **health** underwriting risk module to **health insurance obligations and
  health reinsurance obligations**." *The health module is therefore not a residual — it takes
  precedence over both the life and the non-life module.*
- **`SCR-SF 3.10B`** [31/12/2024] — the **NSLT** health sub-module applies to health obligations
  "included in **lines of business 1, 2, 3, 13, 14, 15 and 25**"; the **SLT** health sub-module to those
  "included in **lines of business 29, 33 and 35**"; the **health catastrophe** sub-module to **all**
  health obligations.
- **TPFR 26.3** [R41] — health insurance obligations "pursued on a similar technical basis to that of
  **long-term insurance business** must be assigned to the lines of business for long-term insurance
  business" and those on a general-insurance basis to the general lines, **provided the technical basis
  is consistent with the nature of the risks**. **TPFR 26.2** — assignment "must reflect the **nature of
  the risks**… The **legal form** of the obligation is **not necessarily determinative**."

**12.2 The Glossary definitions, verbatim** [R42 Glossary amendments; the same terms appear in the
revoked DR Art. 1 [R49] in materially identical words]:

- **`health insurance obligation`** — "means an insurance obligation that covers one or both of the
  following: **(1)** the provision of medical treatment or care including preventive or curative
  medical treatment or care **due to illness, accident, disability or infirmity**, or **financial
  compensation for such treatment or care**; or **(2) financial compensation arising from illness,
  accident, disability or infirmity**."
- **`medical expense insurance obligation`** — "an insurance obligation that covers the provision or
  financial compensation referred to in **(1)** of the definition of health insurance obligation."
- **`income protection insurance obligation`** — "an insurance obligation that covers the financial
  compensation referred to in **(2)** of the definition of health insurance obligation, **other than
  the financial compensation referred to in (1)**."
- **`SLT health`** — "means health insurance business that is **pursued on a similar technical basis to
  that of long-term insurance business**."
- **`NSLT health`** — "means health insurance business that is **not SLT health**."
- **`health reinsurance obligation`** — reinsurance arising from accepted reinsurance covering health
  insurance obligations.

**12.3 Income protection — settled.** An individual long-term UK IP contract pays financial
compensation arising from illness or disability, so it is a **health insurance obligation** (limb (2)),
and specifically an **income protection insurance obligation**. Written on a long-term technical basis
it is **SLT health**, line of business **29**, and takes:
`3C9` health mortality +15%; `3C10` health longevity −20%; `3C13` income-protection
disability-morbidity; `3C14` health expense +10% / +1pp inflation; `3C15` health revision +4%;
`3C16` SLT health lapse (up ×1.5 / down ×0.5 / **40% mass**, with **no 70% limb anywhere in the health
module**); plus `3C17`–`3C20` health catastrophe (mass accident, accident concentration — which for
income protection catches **group** schemes via `3C19.3` — and pandemic).
`3C11.2(2)` confirms the scope: the income-protection disability-morbidity scenarios apply "**only to
income protection insurance obligations and income protection reinsurance obligations where the
underlying business is pursued on a similar technical basis to that of life insurance**". An
annually-renewable or short-term IP contract instead lands in **NSLT** segment 2 ("Income protection
insurance and proportional reinsurance", lines of business 2 and 14, `sigma_prem` 8.5%, `sigma_res` 14%
[R62 `3C4`]) and is charged by the **3-sigma factor formula** `3C2.1`, not by scenario.

**12.4 Critical illness — the derivation, and what it does and does not settle.** Both the SCR stream
[R62] and the reporting stream [R89] left this `?`, the former because it believed the numbered
line-of-business list had not been retrieved. Cross-reading resolves the classification question as
follows. **This is a chain of textual reasoning by the drafter. No retrieved document states the
conclusion, and it must be tagged as a derivation wherever it is used.**

1. A critical illness benefit is a lump sum payable on diagnosis of a defined condition. It is
   **financial compensation arising from illness** — limb **(2)** of `health insurance obligation`.
   (It is not limb (1): it is not compensation *for medical treatment or care*.)
2. Therefore it is a **health insurance obligation**, and by `SCR-SF 3.2A(2)` it is **excluded from the
   life underwriting risk module**, which reaches life obligations "other than health insurance
   obligations".
3. By `SCR-SF 3.2A(3)` it goes to the **health underwriting risk module**.
4. A UK individual CI contract is underwritten, level-premium or reviewable, multi-year, and reserved
   on a life-office technical basis, so it is **SLT health** on the Glossary definition, hence line of
   business **29** under TPFR 26.3, hence the **SLT branch** by `SCR-SF 3.10B(2)`.
5. Inside the SLT branch, `3C11.1` computes health disability-morbidity as the **sum** of the
   medical-expense and the income-protection charges, and `3C11.2` scopes each to the corresponding
   *obligations*. Because the Glossary's `income protection insurance obligation` is defined as **all**
   limb-(2) compensation other than limb-(1) compensation, a CI lump sum falls inside it. The stress
   that would therefore apply is **`3C13.1`**: +35% inception in the following 12 months, +25%
   thereafter, **−20% recovery rates where those rates are lower than 50%**, and **+20% persistency
   rates where those rates are equal to or lower than 50%**.

**Why this is uncomfortable, and recorded rather than smoothed over.** Step 5 produces the result that
a UK critical illness contract is charged under a sub-module the rulebook labels "**income
protection**". That is a consequence of the Glossary drafting (`income protection insurance obligation`
is a residual category, not a product name), not of any market convention. The recovery-rate and
persistency limbs of `3C13.1` are conditional on rates being at or below 50%, and a CI lump-sum
contract has no recovery or persistency rates at all, so both conditional limbs are vacuous and only
the +35%/+25% inception limbs bite. **The retrieved sources do not confirm that this is the intended
treatment.**

**What remains genuinely unsettled, and stays `?` in the matrix:**

- **Accelerated critical illness.** An accelerated CI benefit accelerates the death benefit of a term
  assurance: one contract covering both a **life** obligation (death) and a **health** obligation
  (illness). **TPFR 26.7** requires that "where a contract of insurance includes (1) health insurance
  obligations or health reinsurance obligations; and (2) other insurance or reinsurance obligations,
  those obligations must, **where possible**, be unbundled" [R42]. Where unbundling is possible the
  death leg goes to `3B` and the CI leg to `3C`; where it is not, **TPFR 26.2** sends the whole
  obligation to whichever module reflects "the nature of the risks", and the sources give **no
  bright-line test**. Since an accelerated benefit pays **once**, on the earlier of death and
  diagnosis, the two legs are not additive and unbundling is not obviously "possible" — which is
  exactly why this cannot be resolved from the retrieved text.
- **The RAO class** of standalone CI (see §1). Not settled by [R14].
- **The reporting line of business.** IR.14.01 column C0030 is a **closed list** the firm applies
  itself — 29 health insurance / 30 with profit participation / 31 index-linked and unit-linked /
  32 other life insurance / 33 / 34 / 35 / 36 [R89] — and the PRA product code list gives CI **four
  dedicated codes** (444/454 accelerated guaranteed/reviewable, 464/474 standalone
  guaranteed/reviewable) **without stating a line of business for any of them**. Two firms can
  legitimately report the same standalone CI book on different rows.
- Note the reporting layer's own asymmetry: **IR.12.04** [R89] places "critical illness claim rates"
  in a **mortality-and-morbidity assumption block** whose guidance says "where **accelerated** critical
  illness is the main product the basis should be **the percentage of combined mortality and critical
  illness claims**" — i.e. the template presumes the accelerated product is modelled as a single
  combined decrement, which pulls towards *not* unbundling.

**12.5 Term assurance — settled and simple.** A death benefit is not financial compensation arising
from illness, accident, disability or infirmity in the limb-(2) sense; it is a life obligation.
`3.2A(2)` sends it to the **life module `3B`**: mortality +15% (`3B1.1`), life catastrophe +0.15
percentage points on year-1 mortality rates (`3B7.1`), life expense (`3B4.1`), and the three lapse
scenarios (`3B6`). **Terminal illness benefit**, which the library's representative term assurance
carries, is an acceleration of the death benefit on diagnosis of terminal illness — the same
unbundling question as accelerated CI, at a much smaller materiality. Recorded, not resolved.

**12.6 Counterparty default is the protection-specific market-side module.** UK protection business is
heavily reinsured, so `3E13` type 1 exposure on reinsurance recoverables is the dominant counterparty
charge for TA, CI and IP, sitting alongside the **TPFR 24.4 LGD floor of 50%** on the
counterparty-default adjustment inside the best estimate [R41] and the PRA's expectations in **SS20/16**
[R120, landing page only].

### 13. Whole of life — lapse direction, mass lapse, and the over-50s cell

**13.1 The two cells behave oppositely.** The library specifies **RefWOL-UW** (underwritten guaranteed
whole of life) and **RefWOL-O50** (over-50s guaranteed acceptance, **no surrender value at any time**,
premiums typically ceasing at a stated age). A legacy unit-linked reviewable design with a surrender
value is documented as a closed-book variation.

**13.2 The lapse stress runs the *other* way for a lapse-supported product.** `SCR-SF 3B6.1` [R62]
takes the **highest** of three scenarios, and `3B6.2`/`3B6.3` each carry a directional filter:

- `3B6.2` **lapse up** — permanent **+50% relative** increase in option exercise rates, capped so the
  increased rates do not exceed 100%, applying **only to relevant options for which exercise would
  *increase* technical provisions without the risk margin**;
- `3B6.3` **lapse down** — permanent **−50% relative** decrease, the decrease not to exceed **20
  percentage points**, applying **only where exercise would *decrease* technical provisions without the
  risk margin**.

For the O50 cell, a lapse is pure profit to the insurer: the policyholder has paid premiums, there is
**no surrender value**, and the future claim disappears. Lapsing therefore **decreases** technical
provisions, so the policy is filtered **out** of `3B6.2` and **into** `3B6.3`. **The binding stress on a
lapse-supported whole of life is lapse *down*, not lapse up.** The same logic applies to any cell whose
best estimate is negative because expected future premiums exceed expected future claims.

This has a direct model consequence flagged in the product's own technical notes: a best estimate on
realistic assumptions **embeds the lapse-support profit**, so *raising* the assumed lapse rate *lowers*
the best estimate. The lapse assumption is therefore the assumption to govern hardest under TAS 100
[R33] — and TPFR 11.1 [R41] independently forbids a static lapse table unless there is empirical
evidence that behaviour is independent of moneyness, economics and management action.

**13.3 Mass lapse still applies, at 40%.** `3B6.6(2)` [R62] is a **40%** instantaneous discontinuance
of all policies (other than the RAO class VII business in `3B6.6(1)`) **for which discontinuance would
increase technical provisions without the risk margin**. For the O50 cell that filter is not satisfied
either, so the mass-lapse charge on a purely lapse-supported cell is **nil** — the whole `3B6` maximum
collapses onto the lapse-down scenario. For the underwritten cell with a surrender value the ordinary
picture returns. **`SCR-SF 1.2` defines discontinuance to include making a contract paid-up**, which
matters for both cells: the O50 designs observed in the product spec include paid-up-style promises,
and `3B6.8` requires the **worst discontinuance type per policy**.

**13.4 Longevity, not mortality, can be the binding biometric stress.** A whole of life has no
maturity, so a *decrease* in mortality defers the claim. Where a cell's reserve is high relative to the
sum assured — a mature underwritten policy, or a with-profits WOL — the `3B2` longevity stress can
increase technical provisions, and the `3B2.2` filter admits it. Both `3B1` (+15%) and `3B2` (−20%)
must therefore be evaluated policy-by-policy under their respective filters; a whole-of-life book will
generally split between them.

**13.5 Where a WOL sits determines half its regulatory treatment.** A **non-profit** WOL in the
shareholder fund: LoB 32, `TP_l4` + `CAR` in the MCR, no RFF, no LACTP, DAC required under FRS 103
¶3.7–3.9. A **with-profits** WOL inside a with-profits fund: LoB 30, `TP_l1`/`TP_l2`, inside the RFF,
LACTP available, **no DAC** (FRS 103 ¶3.10), surplus funds computed over it, and — per **SS13/15 ¶3.1**
[R46] — the **prospective** Surplus Funds 3.4 valuation route rather than the retrospective one. A
**unit-linked** WOL: LoB 31, `TP_l3`, Investments 4.3 coverage, IR.12.01 unit-linked rows. The product
name decides none of this.

### 14. Negative technical provisions — is there a floor, and on which ledger?

**Solvency UK: no floor. Settled.** The technical-provisions stream searched the Valuation, Technical
Provisions and TPFR Parts in full and found no zero floor, no surrender-value floor and no
contract-level or group-level non-negativity rule; the single occurrence of "negative" is TPFR 25.2
(the EUR-peg currency adjustment, which "must be negative") [R41 §17]. This stream adds three
independent confirmations from the product side:

1. **The Solvency I floor was expressly not carried over.** INSPRU 1.2.62R imposed exactly such a
   floor, and INSPRU 1.2 **does not apply to a Solvency II firm** [R115].
2. **The market reads it the same way.** "[T]here is **no floor related to the surrender value
   specified in the rules**" [R118, secondary].
3. **The reporting layer treats surrender value as a disclosure.** IR.14.01 carries "Surrender value —
   the amount of surrender value net of taxes" as an information item, not a constraint [R89].

**UK GAAP: there is a floor, and it is product-specific.** FRS 103 Implementation Guidance [R100]
**IG2.41** — "**no policy may have an overall negative provision except as allowed by PRA rules, nor a
provision less than any guaranteed surrender or transfer value**"; **IG2.47** — the provision for any
contract "should not be less than the element of any surrender or transfer value calculated by
reference to the relevant fund(s) or index". The FRS 103 **liability adequacy test** (¶¶2.14–2.18)
operates in the same direction. *A UK insurer therefore reports a negative best estimate on the
Solvency UK balance sheet and, on the same business, a floored provision in its statutory accounts.*

**IFRS 17: the fulfilment cash flows may be negative; the CSM may not.** A group of contracts cannot
carry a negative CSM — that is what makes a group onerous and creates a loss component [R106 ¶2.50] —
but the fulfilment cash flows themselves are unconstrained. *This sentence is a drafter's comparison,
not a claim sourced to retrieved IFRS 17 text.*

**Per product, on the Solvency UK ledger:**

| Product | Negative best estimate? | Why |
|---|---|---|
| TA | **Yes, routinely at issue** | PV(guaranteed premiums) > PV(claims + expenses) inside a full-term boundary |
| CI | **Yes, routinely at issue** | same, with the reviewable-premium boundary question of §15 |
| IP | **Yes for the active-life cell**; **no for claims in payment** | the claims-in-payment cell is a pure annuity |
| WOL | **Cell-dependent** — yes for RefWOL-O50 early on, less so for RefWOL-UW | the O50 cell is the paradigm lapse-supported negative reserve |
| WP | Normally no | guaranteed benefits plus FDB dominate; the estate sits outside TP anyway |
| ULB | **The non-unit ("sterling") component is commonly negative**; the total is positive | PV of future charges exceeds PV of non-unit outgo |
| PA | **No** | a single-premium annuity in payment has no future premium inside the boundary |

The row "negative best estimate permitted" is therefore `x` for TA and CI, split for IP and WOL, and
`--` for PA — matching the technical-provisions stream's marks, with the IP and ULB refinements added
here.

### 15. Contract boundaries, product by product

The rules are TPFR 2.1 (recognition at the earlier of becoming a party and cover starting), TPFR 3.2
(inclusion, including unilateral renewal/extension rights), TPFR 3.3 (the three exclusion triggers),
TPFR 3.5 (the savings-contract cut), TPFR 3.6 (unbundled parts) and TPFR 3.7 (the "premiums fully
reflect the risks" test) [R41]. Applied to the seven representative designs:

| Product | Boundary | Governing limb |
|---|---|---|
| **TA** (guaranteed premiums) | **full term** — all `n` years of premiums and benefits inside | no unilateral repricing right exists, so 3.3(3) never engages |
| **CI**, guaranteed premiums | full term | as TA |
| **CI**, reviewable premiums | **full term, not the review date** | TPFR 3.3(3) long-term carve-out: where an **individual risk assessment is made at inception and cannot be repeated before amending premiums**, the "premiums fully reflect the risks" test is applied **at the level of the contract**, not the portfolio. Individually-underwritten UK protection cannot re-underwrite at review, so the boundary is **not** cut |
| **IP**, guaranteed premiums | full term (to the ceasing age) | as TA |
| **IP**, reviewable premiums | full term | as reviewable CI |
| **IP**, claims in payment | the remaining claim payment period | recognition is already complete; no future premiums |
| **WOL RefWOL-UW** | to the end of premium payment / death | guaranteed rates; 3.3 does not engage |
| **WOL RefWOL-O50** | to death (premiums ceasing at the stated age) | guaranteed acceptance and guaranteed premium; no repricing right |
| **WP unitised bond / conventional endowment** | to maturity or death, **including future regular premiums** | TPFR 3.5 cannot cut them: a with-profits contract **includes a financial guarantee of benefits**, so limb 3.5(2) fails |
| **ULB (representative single-premium bond)** | the contract; **there are no future premiums to cut** | 3.5 has nothing to operate on. Top-ups are new contracts with their own boundaries |
| **ULB regular-premium variant** | **genuinely open** | 3.5 requires all three of: no compensation for a specified uncertain adverse event; no financial guarantee of benefits; and no power to compel the premium. A 100.1% death uplift may or may not be "a specified uncertain event that adversely affects the insured person" once the "**no discernible effect on the economics of the contract**" qualifier is applied. **The retrieved sources do not settle it for any particular design** |
| **PA** | the contract; single premium already paid | no future premiums; no unilateral rights |

Two general points a drafter must not lose. **TPFR 3.7** makes the "fully reflect the risks" test
demanding in the extreme: premiums fully reflect the risks only "where there is **no circumstance**
under which the amount of the benefits and expenses payable under the portfolio exceeds the amount of
the premiums payable" — any loss-making scenario defeats it. And **TPFR 23.1** requires reinsurance
recoverables to be calculated **consistently with the boundaries of the underlying contracts** — so a
reviewable-rate protection treaty inherits the full-term boundary of the direct business.

### 16. Reporting — which templates each product triggers, and under which product codes

The reporting stream owns the templates [R84][R89][R90][R91]. The product-facing summary:

**Product code mapping** (from the IR.14.01 appendix [R89]; the appendix is the former SS36/15 content
and is the single best map from UK product taxonomy to regulatory reporting):

| Library product | PRA product ID code(s) |
|---|---|
| term-assurance | **404** level term regular premium; **414** level term single premium; **424** decreasing term regular premium; **434** decreasing term single premium |
| critical-illness | **444 / 454** accelerated CI, guaranteed / reviewable premiums; **464 / 474** standalone CI, guaranteed / reviewable premiums |
| income-protection | **494 / 504** guaranteed / reviewable premiums; **514** single premium; **524 claims in payment**; 480 CWP; 481 Holloway UWP |
| whole-of-life | **104** WOL OB NP; **102** WOL OB UL; **100 / 101** WOL OB CWP / UWP; 105 / 106 industrial branch |
| with-profits | **111** single premium bond UWP; **100 / 101**; **120 / 121** endowment OB CWP / UWP; **200 / 201**, **210 / 211** participating pensions |
| unit-linked-bond | **112** single premium bond UL (**113** index-linked, **114** non-profit) |
| pension-annuity | **724** individual pension annuity NP; **734** enhanced NP; **720 / 722** WP / UL; (700/704, 710/714, **754** bulk — out of scope) |

Verified conventions that bear on a model [R89]: "Single premium bond" **includes 'investment bond' and
'with-profits bond'**, and the whole-life/endowment codes **exclude single premium bonds "which are
technically whole of life"** — so the library's with-profits **bond** reports under 111, not under the
whole-of-life codes. **UL** is "the same as the legal term '**property linked**'"; **IL** "includes
policies linked to a stock market index or the value of specific securities. **It excludes RPI / CPI
linked policies**" — an RPI-linked annuity is **not** index-linked business for reporting. **NP** is
"all policies covered by the 'Other' Solvency II line of business **and including life health
business**" — which is the one place the reporting layer hints that health business may be reported as
NP rather than as LoB 29, and it does not resolve §12.4. Where technical provisions are calculated for
a combination of products — "the instruction's own example is **with-profits guarantee costs**" — or
the product code is uncertain, firms "should use an **approximation to apportion** between product
codes".

**Template triggers.** IR.12.01 (life technical provisions), IR.12.03, IR.12.04 (best-estimate
assumptions), IR.14.01, IR.05.03, IR.05.05, IR.28.01 (MCR) and the SFCR templates apply to every
product, subject to **entity-level** thresholds. Product-triggered templates:
**IR.12.05 / IRR.12.05 (with-profits value of bonus)** and **IR.12.06 / IRR.12.06 (with-profits
liabilities and assets)** — with-profits business only, threshold net BEL for with-profits business
**> £500 million**, completed **per ring-fenced fund which is also a with-profits fund** [R90];
**IRR.22.02 / IRR.22.03 and MALIR 1–7** — MA portfolios only [R91]; **IR.26.04 (SCR health underwriting
risk)** — IP certainly, CI **unresolved** (§12.4); **IR.05.10 (excess capital generation)** — scoped on
life premiums **excluding unit-linked premiums**, so a pure unit-linked book cannot bring a firm into
scope [R84 Art 9(1)(k)].

**The shareholder-transfer formula** a with-profits model must reproduce, verified from the IR.12.05
instruction [R90]:
```
R0090/C0050 = R0060/C0040 * R0080/C0050 / (1 - R0080/C0050)
```
i.e. `shareholder transfer = (policyholder value of bonus) * s / (1 - s)`, where `s` is the shareholder
proportion. For a **90:10** fund `s = 0.10`, so the transfer is **one ninth** of the policyholder bonus
value. The instruction records that "most with-profits funds are either '90:10' … or '100:0'".

### 17. Effective dates that bear on product treatment

| Date | Event | Source |
|---|---|---|
| 01/01/2016 | With-Profits Part, Investments Part and Surplus Funds Part rule date-stamps; SS14/15 ch.2 text stamped 20/03/2015 | [R80][R114][R45][R80b] |
| **31/12/2015** | **INSPRU 1.3 last updated, then Deleted** — the realistic-basis regime ends; FRS 103 freezes its definitions at this date | [R116][R99] |
| 01/01/2021 | INSPRU 1.2 application rule re-stamped, excluding Solvency II firms | [R115] |
| 30/06/2024 | Matching Adjustment Part created; TP chapters 6–7 deleted; the **eligible element** route begins | [R2][R5] |
| **31/12/2024** | PRA2024/13 in force: TPFR Part, `SCR-SF 3.2A`, `3.10B`, `3B`, `3C`, Glossary health definitions; SS1/14, SS14/15, SS20/16 and SS1/20 November 2024 versions effective | [R42][R62][R117][R80b][R120][R119] |
| **20/12/2024 → 31/12/2024** | The **mass-lapse correction**: class III deleted from `3B6.6(1)`, leaving class VII only. **The single most product-consequential correction in Solvency UK for a unit-linked writer** | [R64][R63] |
| 24/07/2025 | `SCR-SF 3.8(1)`, `3.8(3)`, `3.10A`, `3B6.6`, `9.1` re-stamped (past versions not retrieved) | [R62] |
| 27/10/2025 | MAIA definitions added to the MA Part | [R2] |
| 31/12/2026 | PS18/26 removes claims management expenses from IR.14.01 C0070 | [R87 ¶2.41] |
| 05/08/2026 | "Present" Rulebook view read for this file | [R80][R114][R43] |

---

## Model hooks

The generic hooks are the sibling streams' (`solvency-uk-technical-provisions.md` §Model hooks is the
master list). What follows is only what is **product-specific** — the outputs a projection must expose
*because of what the product is*, and which a generic liability engine will not produce unless it is
designed to.

| Product | Model must produce | Granularity / basis / timing | Rule |
|---|---|---|---|
| **All** | A **line-of-business tag** and a **technical-basis flag** on every model point | fixed at set-up, revisited when the product changes; LoB drives both the TP segmentation and the SCR module | TP 10.1 [R1]; TPFR 26.2/26.3, Annex 1 [R41]; `SCR-SF 3.2A`, `3.10B` [R62] |
| **All** | A **PRA product ID code** per model point, and the ability to **apportion** a model point across codes by approximation where TP are calculated for a product combination | annual, per IR.14.01 row; codes are three-digit, with the `{code}/+/{version}` pattern where one product spans rows | [R89] |
| **All** | A **fund / perimeter tag**: shareholder fund, named with-profits fund (per COBS 20 sub-fund), MA portfolio, or remaining part | per model point; drives whether the whole SCR is re-run for that perimeter | `SCR-SF 2.2`, `9.1` [R62]; [R80b ¶2.2–2.3] |
| **All** | A **contract-boundary end date and the limb that produced it** (3.3(1)/(2)/(3) contract-level, 3.5, 3.6) | per contract, re-derived when terms change — never stored as a product constant | TPFR 3 [R41] |
| **All** | The **best estimate unfloored**, with the sign preserved through every aggregation | per homogeneous risk group; the UK GAAP floor is applied *downstream*, never in the projection | TP 3.1 [R1]; IG2.41/IG2.47 [R100] |
| **WP** | **Guaranteed benefits and future discretionary benefits as two separately-valued streams** | per with-profits fund, per scenario, per period; FDB frozen in gross SCR scenarios, released only via LACTP | TPFR 10.1 [R41]; `3.3A(1)(c)`, `6.3` [R62][R112] |
| **WP** | The **asset share** on the Surplus Funds 3.3 ten-item retrospective basis, **and** the 3.4 six-item prospective basis where 3.3 is inadequate (the PRA names whole-of-life as that case) | per specimen policy or compliant group, per valuation date; consistent with the TP methodology; **no risk margin inside** | Surplus Funds 3.2–3.5 [R45]; SS13/15 ¶3.1–3.2 [R46] |
| **WP** | **Surplus funds**, and the **value of future shareholder transfers** as a separate quantity | per with-profits fund; the transfer is excluded from restricted own funds by the Glossary definition, so it must not be netted into the estate | Surplus Funds 3.1 [R45]; Glossary *restricted own funds* [R43]; [R80c Guideline 8] |
| **WP** | The **IR.12.06 decomposition**: WPBR (split retrospective/prospective, with permanent miscellaneous surplus separated) and FPRL (guarantees ≥ 0, non-contractual commitments, financial options such as **GARs**, smoothing which **may be negative**, financing, other, less planned deductions) | annual, per RFF that is a with-profits fund, where WP net BEL > £500m; must tie to IR.12.01.01 R0030 C0010 | [R90] |
| **WP** | The **shareholder transfer** `= value of bonus × s/(1−s)`, plus brought-forward and carried-forward deferred transfer balances | annual per fund; `s` = 0.10 for a 90:10 fund | [R90] |
| **WP** | A **management-actions plan mapped into the model**: bonus declaration, terminal bonus, smoothing, MVR (with contractual MVR-free points), investment rebalancing, and charge levels — each with trigger circumstances, the circumstances in which it **cannot** be taken, its **order**, its **implementation lag** and **its expenses** | per fund, per scenario, per period; consistent with the published PPFM | TPFR 8 [R41]; COBS 20.3 [R9]; IG1.13 [R100] |
| **WP / WOL(WP)** | A complete **standard-formula (or internal-model) run per ring-fenced fund plus one for the remaining part**, with the scenario chosen at **entity** level and **no diversification** between perimeters | at each SCR date; negative notional SCRs set to zero before summing | `SCR-SF 9.1` [R62]; [R80c Guidelines 9, 12] |
| **ULB** | A **two-part liability**: the component "in respect of linked benefits" (which must be covered by linked assets) and the non-linked remainder | per fund per valuation date; required for Investments 4.3 compliance and for Sch 3 items D vs C.2 | Investments 4.3, 5.1 [R114]; Sch 3 note 26 [R105] |
| **ULB** | The **PV of future annual management charges on existing units**, separately from charges on units bought by future premiums | per model point; it is the quantity that makes the unit-linked BEL less than the surrender value | [R118, secondary] |
| **ULB** | **Unit-fund cash flows to and from investment firms** as a named cash-flow stream | per model point per period; TPFR 13.1(6) makes it an in-scope best-estimate cash flow, not an internal transfer | TPFR 13.1(6) [R41] |
| **ULB** | **Unit-linked expenses `Exp_ul`** as a separately tagged expense total | annual; it is the operational-risk driver for linked business, and `TP_life-ul` is deducted from the provisions leg | `SCR-SF 5.4(1)`, `5.4(4)(b)` [R62] |
| **ULB** | Three **complete lapse revaluations** (up ×1.5 capped at 100%, down ×0.5 capped at −20pp, mass **40%**), each computed on the **worst discontinuance type per policy** including **paid-up** | at each SCR date | `SCR-SF 3B6` [R62]; `1.2` definition |
| **PA** | Cash flows split into the **MA portfolio** and the remaining part, with the portfolio's own notional SCR | per portfolio; no diversification with the rest of the firm | `SCR-SF 9.1(1)–(2), (9)` [R62]; Own Funds 3L [R77] |
| **PA** | A **risk margin computed without the MA** — the reference undertaking may not use it | annual integer steps from t = 0; materially higher liability basis than the balance sheet it sits on | TP 4B.1(13) [R1] |
| **PA** | A **spread-stress revaluation that recomputes the MA**, not just the assets | at each SCR date | `SCR-SF 3D25` [R62] |
| **PA** | A **recapture projection** for any funded reinsurance — the gross liability restored to the MA portfolio | per treaty; SS5/24 §3 has a dedicated "recapture within MA portfolio" section | [R47] |
| **PA / IP / WP** | For any **eligible element** placed in an MA portfolio: the element valued **separately** and demonstrably organisable and manageable separately | per element; IP in-payment claims have their own product code (524), which makes the split reportable | MA 1.2, 2.5 [R2]; SS7/18 ¶3.5A–3.5B [R8]; [R89] |
| **IP** | **Claim inception and claim termination (recovery / death) rates**, duration-dependent, as separate assumption objects — because `3C13.1` stresses them separately and conditionally | per model point per period; the conditional limbs test recovery rates **< 50%** and persistency rates **≤ 50%** | `SCR-SF 3C13.1` [R62] |
| **IP** | An **index-linked escalation** flag on claims in payment — it is what brings `3C15` health revision into scope | per claim cell | `SCR-SF 3C15.1` [R62] |
| **IP** | **Group-scheme concentration data**: the highest number of insured persons **working in the same building** | per country; drives `3C19` accident concentration | `SCR-SF 3C19.3` [R62] |
| **IP** | An **income-protection pandemic exposure `E`**: the sum over insured persons of the value of benefits payable on **permanent work disability caused by an infectious disease**, taken for recurring benefits as the best estimate **assuming the person is permanently disabled and will not recover** | per valuation date | `SCR-SF 3C20.2` [R62] |
| **TA / CI / IP** | **Reinsurance recoverables on the same contract boundary as the direct business**, with a settlement lag and a counterparty-default adjustment at **LGD ≥ 50%** | per counterparty **and** per line of business | TPFR 23.1, 24.4 [R41] |
| **WOL** | A **directional filter on every lapse-sensitive policy**: does discontinuance increase or decrease TP without the risk margin? | per policy, recomputed each valuation — the answer flips as a policy matures | `3B6.2`, `3B6.3`, `3B6.6(2)` [R62] |
| **WOL / TA / CI** | **Capital at risk** as `max(0, A − B)` **per contract** (not per portfolio), where A is what the firm would currently pay on death or disability plus the EPV of amounts not so covered, and B the corresponding best estimate | per contract, netted for reinsurance, floored at zero **per contract** | MCR 3C.1(5) [R78] |
| **All** | An **assumption pack in IR.12.04 shape**: current-year and prior-year valuation bases plus **five years of own experience**, expressed as percentages of a **named table** with the **CMI projection parameterisation in CMI notation** | annual, where gross BEL > £50m or GWP > £10m | [R89] |

---

## Product applicability

**This is the matrix the downstream `uk/regulatory/` explainer and the seven per-product "Statutory
accounting and capital" sections are written from.** It consolidates the sibling streams' matrices and
resolves them at product level; where this stream's mark differs from a sibling's, the difference is
called out in the notes.

**Marks.** `x` = applies materially and directly · `(x)` = applies but conditionally, partially, or as
a secondary driver · `--` = does not apply · `?` = the retrieved sources do not settle it ·
blank = not applicable by construction.

**Products.** TA = term-assurance · CI = critical-illness · IP = income-protection ·
WOL = whole-of-life · WP = with-profits · ULB = unit-linked-bond · PA = pension-annuity.
Marks are for the **representative design specified in this library**, not for every UK contract that
carries the product name; where a product has two cells (WOL) or two chassis (WP), the mark covers both
unless a note splits them.

### A. Valuation of technical provisions

| Item [R#] | TA | CI | IP | WOL | WP | ULB | PA |
|---|---|---|---|---|---|---|---|
| Best estimate, TP 3.1 [R1] | x | x | x | x | x | x | x |
| Technical provisions as a whole, TP 2.5(2) / TPFR 22 [R1][R41] | -- | -- | -- | -- | -- | (x) | -- |
| Contract boundary — full term, no cut [R41 TPFR 3] | x | x | x | x | x | x | x |
| Contract boundary — **contract-level** repricing test, TPFR 3.3(3) [R41] | (x) | **x** | **x** | (x) | (x) | | -- |
| Contract boundary — TPFR 3.5 savings-contract cut [R41] | -- | -- | -- | -- | -- | **?** | -- |
| Contract boundary — TPFR 3.6/26.7 unbundling [R41] | (x) | **?** | (x) | (x) | (x) | (x) | -- |
| Expenses, four categories + overheads, TPFR 16.1–16.2 [R41] | x | x | x | x | x | x | x |
| **Going-concern expense basis (new business assumed), TPFR 16.4** [R41] | x | x | x | x | x | x | x |
| Unit-linked expenses identified separately | -- | -- | -- | (x) | (x) | **x** | -- |
| Options and guarantees, TP 9.2 / TPFR 17 [R1][R41] | (x) | (x) | (x) | x | **x** | **x** | (x) |
| Stochastic / scenario-dependent method, TPFR 19.4–19.5 [R41] | -- | -- | (x) | (x) | **x** | (x) | (x) |
| Dynamic policyholder behaviour, TPFR 11.1 [R41] | (x) | (x) | (x) | x | **x** | **x** | -- |
| Future management actions, TPFR 8 [R41] | (x) | (x) | (x) | (x) | **x** | **x** | (x) |
| **Future discretionary benefits valued separately, TPFR 10.1** [R41] | | | | (x) | **x** | | (x) |
| FDB off currently-held assets, TPFR 9.1 [R41] | | | | (x) | **x** | | (x) |
| Payments to/from investment firms, TPFR 13.1(6) [R41] | | | | (x) | (x) | **x** | |
| Policyholder-charged taxation, TPFR 13.1(8) [R41] | (x) | (x) | (x) | (x) | **x** | **x** | -- |
| Reinsurance recoverables + CDA, LGD floor 50%, TPFR 23–24 [R41] | **x** | **x** | **x** | x | (x) | (x) | **x** |
| Surplus-funds carve-out from TP, TP 9.1(3) / SF 2.1 [R1][R45] | -- | -- | -- | (x) | **x** | -- | (x) |
| Retrospective (asset share) route, SF 3.3 [R45] | | | | (x) | **x** | | (x) |
| **Prospective route, SF 3.4 / SS13/15 ¶3.1** [R45][R46] | | | | **x** | **x** | | (x) |
| **Negative best estimate permitted (no floor)** [R41 §17][R115] | **x** | **x** | (x) | (x) | -- | (x) | -- |
| Risk margin, CoC 4%, λ = 0.9 floor 0.25 [R1][R4][R44] | x | x | x | x | x | x | **x** |
| Risk margin reference undertaking uses **no** MA/VA/TMIR/TMTP [R1 4B.1(13)] | (x) | (x) | (x) | (x) | (x) | (x) | **x** |

### B. Discounting, adjustments and transitionals

| Item [R#] | TA | CI | IP | WOL | WP | ULB | PA |
|---|---|---|---|---|---|---|---|
| Basic GBP risk-free curve [R54][R55] | x | x | x | x | x | x | x |
| Extrapolation beyond the last liquid point bites [R56] | (x) | (x) | x | x | x | -- | x |
| Volatility adjustment (permission-dependent) [R1 ch.8] | (x) | (x) | (x) | (x) | (x) | (x) | -- |
| **MA — whole-contract eligibility, MA 2.2** [R2] | -- | -- | -- | -- | -- | -- | **x** |
| **MA — eligible-element route, MA 1.2** [R2] | -- | -- | **x** | -- | **x** | -- | -- |
| MA 2.5 future-premium carve-out (limb (1)(b) only) [R2] | -- | -- | **x** | -- | -- | -- | -- |
| Recovery time risk as a permitted MA risk [R8 ¶3.5B] | -- | -- | **x** | -- | -- | -- | -- |
| 5% mortality-risk cap [R2 2.2(3)] | -- | -- | (x) | -- | (x) | -- | x |
| MA attestation; MAIA; MA breach reduction [R2] | -- | -- | (x) | -- | (x) | -- | x |
| PPP compliance at asset **and** portfolio level for MA [R119 ¶1.7] | -- | -- | (x) | -- | (x) | -- | **x** |
| TMTP [R3] | (x) | -- | (x) | x | x | (x) | x |
| TMIR [R57] | (x) | -- | (x) | x | x | (x) | -- |

### C. SCR — module and sub-module incidence

| Sub-module [R62 unless noted] | TA | CI | IP | WOL | WP | ULB | PA |
|---|---|---|---|---|---|---|---|
| **Life underwriting module `3B` applies at all** (`3.2A(2)`) | x | **--** (derivation §12.4) | -- | x | x | x | x |
| **Health underwriting module `3C` applies at all** (`3.2A(3)`) | -- | **x** (derivation §12.4) | x | -- | -- | -- | -- |
| SLT vs NSLT branch (`3.10B`) | | **SLT** | **SLT** | | | | |
| Mortality +15% `3B1.1` | **x** | | -- | **x** | x | (x) | -- |
| Longevity −20% `3B2.1` | -- | | -- | (x) | (x) | -- | **x** |
| Life disability-morbidity `3B3.1` | -- | | -- | -- | -- | -- | -- |
| Life expense +10% / +1pp `3B4.1` | x | | | x | x | x | x |
| Life revision +3% `3B5.1` | -- | | | -- | -- | -- | (x) |
| Lapse up ×1.5 `3B6.2` / `3C16.2` | **x** | x | x | (x) | x | **x** | -- |
| **Lapse down ×0.5 `3B6.3` / `3C16.3`** | (x) | (x) | (x) | **x** | x | (x) | -- |
| Mass lapse **70%** limb `3B6.6(1)` (RAO class VII only) | -- | -- | -- | -- | -- | **--** | -- |
| Mass lapse **40%** limb `3B6.6(2)` / `3C16.6` | x | x | x | (x) | x | **x** | -- |
| Life catastrophe +0.15pp `3B7.1` | **x** | | -- | x | x | (x) | -- |
| Health mortality +15% `3C9.1` | | (x) | (x) | | | | |
| Health longevity −20% `3C10.1` | | -- | (x) | | | | |
| Health disability-morbidity `3C13.1` (income protection scenario) | | **x** (derivation; conditional limbs vacuous) | **x** | | | | |
| Health expense `3C14.1` | | x | x | | | | |
| Health revision +4% (inflation trigger) `3C15.1` | | -- | **x** | | | | |
| SLT health lapse `3C16` (three scenarios, 40% mass) | | x | x | | | | |
| Health CAT mass accident `3C18` | | (x) | x | | | | |
| Health CAT accident concentration `3C19` (group IP) | | -- | (x) | | | | |
| Health CAT pandemic `3C20` | | (x) | **x** | | | | |
| NSLT premium & reserve 3-sigma `3C2.1` | | ? | (x) | | | | |
| Interest rate up/down `3D5`/`3D6` | x | x | x | x | x | (x) | **x** |
| Equity `3D9` + symmetric adjustment | -- | -- | -- | (x) | **x** | **x** | (x) |
| Property −25% `3D15.1` | -- | -- | -- | (x) | x | (x) | (x) |
| Spread `3D17` (non-MA) | (x) | (x) | (x) | x | x | (x) | x |
| **Spread on an MA portfolio `3D25` (recomputes the MA)** | -- | -- | (x) | -- | (x) | -- | **x** |
| Concentration `3D26`–`3D31` | (x) | (x) | (x) | (x) | x | (x) | x |
| Currency ±25% `3D32` | (x) | (x) | (x) | (x) | x | (x) | (x) |
| Counterparty default type 1 `3E13` (reinsurance) | **x** | **x** | **x** | (x) | (x) | (x) | **x** |
| Counterparty default type 2 `3E15` | (x) | (x) | (x) | (x) | (x) | (x) | (x) |
| Intangible asset risk `3F1.1` | (x) | (x) | (x) | (x) | (x) | (x) | (x) |
| Operational — `Op_provisions` 0.45% leg `5.4(4)` | x | x | x | x | x | **--** | x |
| Operational — `0.25 × Exp_ul` leg `5.4(1)` | -- | -- | -- | (x) | (x) | **x** | -- |
| **LACTP `Adj_TP` `6.3`** [R112] | -- | -- | -- | (x) | **x** | -- | -- |
| LACDT `Adj_DT` `6.4` [R112] | x | x | x | x | x | x | x |
| **RFF notional SCR `9.1`** [R71][R80b] | -- | -- | -- | (x) | **x** | **--** | -- |
| **MA-portfolio notional SCR `9.1`** | -- | -- | (x) | -- | (x) | -- | **x** |
| No diversification between perimeters `9.1(9)` | -- | -- | (x) | (x) | **x** | -- | **x** |
| USP available (revision risk only) `USP 2.3` [R65] | -- | -- | (x) | -- | -- | -- | (x) |

### D. Own funds, MCR and the ring fence

| Item [R#] | TA | CI | IP | WOL | WP | ULB | PA |
|---|---|---|---|---|---|---|---|
| Own funds = basic + ancillary; tiering; eligibility limits [R77] | x | x | x | x | x | x | x |
| Reconciliation reserve [R77 3C] | x | x | x | x | x | x | x |
| **Surplus funds as a Tier 1 unrestricted item, 3A.1(1)(d)** [R77] | -- | -- | -- | (x) | **x** | -- | (x) |
| **RFF deduction from the reconciliation reserve, Own Funds 3L** [R77] | -- | -- | -- | (x) | **x** | **--** | (x) |
| Immaterial-RFF simplification, 3L.2 (no notional SCR) [R77] | -- | -- | -- | (x) | (x) | -- | -- |
| Net deferred tax assets as Tier 3 [R77][R111] | x | x | x | x | x | x | x |
| **EPIFP** [R77][R86 ¶4.43] | -- | -- | -- | -- | -- | -- | -- |
| MCR corridor 25%–45% of SCR; AMCR £3.5m (long-term) [R78] | x | x | x | x | x | x | x |
| MCR `TP_l1` guaranteed benefits, participating [R78 3C.1(1)] | -- | -- | -- | (x) | **x** | -- | (x) |
| **MCR `TP_l2` FDB, coefficient −0.052** [R78 3C.1(2)] | -- | -- | -- | (x) | **x** | -- | (x) |
| MCR `TP_l3` linked liabilities [R78 3C.1(3)] | -- | -- | -- | (x) | (x) | **x** | -- |
| MCR `TP_l4` all other long-term [R78 3C.1(4)] | **x** | **x** | **x** | **x** | (x) | (x) | **x** |
| MCR capital at risk, floored at zero **per contract** [R78 3C.1(5)] | **x** | **x** | (x) | **x** | (x) | (x) | (x) |
| MCR general-insurance segment 2 (α 13.1%, β 8.5%) [R78 6.1] | -- | -- | (x) | -- | -- | -- | -- |
| With-Profits Part 2.1 asset cover [R80] | -- | -- | -- | (x) | **x** | -- | (x) |
| With-Profits Part 3.1 distribution strategy [R80][R80b ch.4] | -- | -- | -- | (x) | **x** | -- | (x) |
| **With-Profits Part 4.1 support arrangements** [R80][R80b ch.3] | -- | -- | -- | (x) | **x** | -- | -- |
| Investments 4.3 linked-asset coverage [R114] | -- | -- | -- | (x) | (x) | **x** | -- |
| Investments 5.1 guarantee carve-back into the non-linked regime [R114] | -- | -- | -- | (x) | (x) | (x) | -- |
| Investments 3.1 nature-and-duration matching [R114] | x | x | x | x | x | (x) | **x** |

### E. Reporting, governance and the other two ledgers

| Item [R#] | TA | CI | IP | WOL | WP | ULB | PA |
|---|---|---|---|---|---|---|---|
| IR.12.01 life technical provisions [R89] | x | x | x | x | x | x | x |
| IR.12.01 unit-linked rows R0300/R0302/R0304 [R89] | -- | -- | -- | (x) | (x) | **x** | -- |
| IR.12.04 best-estimate assumptions (own dedicated rows) [R89] | **x** | **x** | **x** | **x** | **x** | **x** | **x** |
| **IR.12.05 with-profits value of bonus** [R90] | -- | -- | (x) | (x) | **x** | (x) | (x) |
| **IR.12.06 with-profits liabilities and assets (WPBR/FPRL)** [R90] | -- | -- | (x) | (x) | **x** | (x) | (x) |
| IR.14.01 life obligations analysis + **PRA product codes** [R89] | x | x | x | x | x | x | x |
| PRA product codes assigned (§16) | 404/414/424/434 | 444/454/464/474 | 494/504/514/**524** | 104/102/100/101 | 111/100/101/120/121 | **112** | 724/734/720/722 |
| IR.05.10 excess capital generation (excludes UL premiums) [R84] | (x) | (x) | (x) | (x) | (x) | **--** | (x) |
| IR.22.01 long-term guarantee and transitional impact [R84] | (x) | (x) | (x) | x | x | (x) | **x** |
| **IRR.22.02 / IRR.22.03 / MALIR 1–7** [R91] | -- | -- | (x) | -- | (x) | -- | **x** |
| IR.26.03 SCR life underwriting risk [R84] | x | **?** | -- | x | x | x | x |
| **IR.26.04 SCR health underwriting risk** [R84] | -- | **?** | **x** | -- | -- | -- | -- |
| IR.28.01 MCR [R84] | x | x | x | x | x | x | x |
| SFCR templates and D.2 narrative [R84][R85] | x | x | x | x | x | x | x |
| SFCR MA/VA zero-impact and attestation disclosure [R84] | -- | -- | (x) | -- | (x) | -- | **x** |
| CGB 6 actuarial function; CGB 11B/11C validation [R92] | x | x | x | x | x | x | x |
| **CGB 3.1(3) MA/VA liquidity plan; CGB 3.2/3.3 sensitivities** [R92] | -- | -- | (x) | -- | (x) | -- | **x** |
| **ORSA — CGB 3.8–3.12, SS19/16** [R92][R95] | x | x | x | x | x | x | x |
| **With-Profits Actuary — Actuaries 5.1 / SMF20a** [R93][R94][R35] | -- | -- | (x) | (x) | **x** | (x) | (x) |
| External audit of the SFCR [R96] | x | x | x | x | x | x | x |
| Preparations for solvent exit [R98] | x | x | x | x | x | x | x |
| **FRS 103 insurance-contract scope** [R99] | x | x | x | x | x | **(x)** | x |
| FRS 103 realistic liabilities / MSSB / FFA [R99 ¶¶3.11–3.15] | | | | (x) | **x** | | (x) |
| FRS 103 ¶3.10 **no DAC** in with-profits funds [R99] | | | | (x) | **x** | | (x) |
| FRS 103 ¶¶3.7–3.9 **DAC required** [R99] | x | x | x | x | -- | (x) | x |
| Sch 3 item **D linked liabilities** vs **C.2** split [R105 note 26] | | | | (x) | (x) | **x** | |
| Sch 3 item **Ba fund for future appropriations** [R105 note 19] | | | | (x) | **x** | | |
| **UK GAAP surrender-value / non-negative floor** [R100 IG2.41, IG2.47] | **x** | **x** | x | x | x | **x** | x |
| **IFRS 17 general measurement model** [R106] | **x** | **x** | **x** | **x** | | | **x** |
| **IFRS 17 variable fee approach** [R106] | | | | (x) | **x** | **x** | |
| IFRS 17 premium allocation approach [R106] | (x) | (x) | (x) | | | | |
| IFRS 17 coverage-unit basis settled? [R106 §3 issue A] | x | x | x | x | x | x | **?** |
| **Tax — BLAGAB / I-E** [R17][R18] | (x) | (x) | (x) | **x** | **x** | **x** | -- |
| **Tax — non-BLAGAB trade basis** [R17][R18] | **x** | **x** | **x** | (x) | (x) | | **x** |
| Tax — chargeable event gains drive policyholder behaviour [R15][R16] | -- | -- | -- | (x) | **x** | **x** | -- |
| **CA 2006 s.833A distributable profits, RFF and MA deductions** [R104] | x | x | x | x | **x** | x | **x** |

### Notes on every non-obvious mark

**Contract boundaries.**
- **TPFR 3.3(3) is bold for CI and IP, `(x)` for TA.** The long-term-underwriting carve-out only *does
  work* where the firm actually has a repricing right — i.e. on **reviewable-premium** CI and IP, where
  it is the difference between a boundary that stops at the next review and one that runs to the end of
  the term. On guaranteed-premium TA there is no repricing right at all, so the rule is engaged only in
  the sense of confirming a full-term boundary. **This is a refinement of the technical-provisions
  stream's mark**, which bolded TA as well [R41 matrix].
- **TPFR 3.5 is `?` for ULB, not `(x)`.** The technical-provisions stream marked it bold-`(x)` on the
  general unit-linked case. For **this library's representative product — a single-premium bond — there
  are no future premiums for 3.5 to cut**, so the rule is inert as specified. It becomes live, and
  genuinely unsettled, on a regular-premium variant. Marked `?` to force the drafter to state which
  variant is meant.
- **TPFR 3.6/26.7 unbundling is `?` for CI.** Accelerated CI is a single contract carrying a life
  obligation and a health obligation that pay **once**, on the earlier of two events. Whether they can
  be unbundled "where possible" is not settled by any retrieved source — see §12.4.

**Technical provisions.**
- **TP-as-a-whole is `(x)` for ULB alone.** TPFR 22.2 declares option-dependent cash flows,
  biometric-dependent cash flows and **all** servicing expenses non-replicable; only the unit-fund
  component of a linked contract is in principle replicable by the units held.
- **Stochastic valuation `--` for TA and CI, `(x)` for IP and PA.** A level-premium term or standalone
  CI contract with no surrender value and no financial option has no scenario-dependent asymmetry. IP
  earns `(x)` through index-linked escalation and economic dependence of claim inceptions; PA through
  inflation-linked escalation. **ULB is `(x)` rather than `x`** because the base design has no
  guarantee — electing a GMDB or capital-protection option makes it `x`.
- **Policyholder-charged taxation `--` for PA.** A pension annuity is pension business; no policyholder
  fund tax enters the projection [R17][R18]. This is a **change from the technical-provisions stream's
  `(x)`**, justified by the tax stream's `--` on the BLAGAB rows for PA [R18 LAM01080].
- **The prospective surplus-funds route is bold `x` for WOL.** SS13/15 ¶3.1 names **whole-of-life
  policies** as the example where the retrospective calculation "might be negative or significantly
  lower than the value calculated using the prospective approach" [R46].
- **Negative best estimate: `(x)` for IP, `--` for WP.** IP splits — the active-life cell can be
  negative, the claims-in-payment cell cannot. WP is `--` rather than `(x)` because guaranteed benefits
  plus FDB dominate and the estate is carved out of technical provisions entirely; **the
  technical-provisions stream marked WP `(x)`**, and this file narrows it on product grounds. ULB is
  `(x)` because the *non-unit* component is routinely negative while the total is not.

**SCR.**
- **CI's life/health marks are a derivation, not a citation.** `3B` is `--` and `3C` is `x` on the chain
  set out in §12.4, which no retrieved document states. The SCR stream marked both `?` [R62 matrix].
  **A drafter who is not willing to carry the derivation should revert to `?` on both rows** — but must
  then also mark IR.26.03 and IR.26.04 `?`, which is what the reporting stream did.
- **Mortality `(x)` for ULB, `--` for IP and PA.** ULB carries a 100.1%-of-fund death benefit, so the
  capital at risk is 0.1% of the fund — non-zero but immaterial. IP's mortality exposure runs through
  the **health** module (`3C9`), not `3B1`. PA is `--` because higher mortality *reduces* annuity
  provisions, so the `3B1.2` filter excludes it.
- **Longevity `(x)` for WOL and WP.** A whole of life has no maturity, so lower mortality defers the
  claim and can increase provisions for policies with high reserves relative to sum assured; WP funds
  commonly contain annuity liabilities. Neither is the primary driver.
- **Lapse down is bold for WOL and lapse up is bold for TA and ULB.** This is the directional point of
  §13.2: the `3B6.2` and `3B6.3` filters route a policy to one scenario or the other according to
  whether discontinuance increases or decreases technical provisions without the risk margin. A
  **lapse-supported** cell — the over-50s whole of life, and profitable protection early in its life —
  is stressed by lapse **down**. **This is a refinement the SCR stream's matrix does not make: it
  marked lapse up `x` for TA, CI, IP, WOL, WP and ULB uniformly.**
- **Mass lapse `(x)` for WOL.** The 40% event applies "for which discontinuance would increase
  technical provisions without the risk margin"; on the O50 cell that filter is not satisfied and the
  charge is nil, so the mark is conditional on the cell.
- **Mass lapse 70% is `--` everywhere, and bold `--` for ULB.** `3B6.6(1)` as corrected [R64] reaches
  **RAO Schedule 1 Part II class VII (pension fund management)** only. Under PS15/24 as originally
  published [R63] the ULB cell would have read `x` at 70%. Nothing in the seven-product set is class VII
  business.
- **Health revision `x` for IP, life revision `(x)` for PA.** `3C15.1` (4%) adds **inflation** to the
  legal-environment and state-of-health triggers, and an index-linked IP claim annuity has exactly that
  exposure. `3B5.1` (3%) has no inflation trigger, so a level or RPI/LPI-escalating pension annuity is
  normally **nil**; impaired-life annuities with a review mechanism, or an Ogden-style legal change,
  would bring it in.
- **Health CAT pandemic is bold for IP** because `3C20.2` requires a **permanent-disability benefit
  valuation** (`E`) that an ordinary IP projection does not produce. Accident concentration is `(x)`
  for IP because `3C19.3` is scoped to workers' compensation and **group** income protection, and this
  library's IP is individual.
- **NSLT `(x)` for IP, `?` for CI.** An annually-renewable or group IP scheme falls in NSLT segment 2;
  the library's individual full-term design does not. For CI the NSLT/SLT split follows the unresolved
  classification.
- **Interest rate `(x)` for ULB.** The unit leg self-immunises; only the non-unit charge and expense
  stream is rate-sensitive. Independently confirmed by the PRA's exclusion of unit-linked technical
  provisions from its relevant-currency materiality test [R55 ¶3.4].
- **Equity `x` for ULB and WP; `(x)` for WOL and PA.** Direct for the two fund-backed products; WOL
  where a non-profit fund holds some equity, PA where an MA portfolio holds equity-like assets.
- **Spread `(x)` for the MA-portfolio row for IP and WP.** Only the **eligible element** placed in an
  MA portfolio attracts `3D25`; the rest of the contract does not.
- **Operational is a clean split.** `5.4(4)(b)` deducts `TP_life-ul`, so a pure unit-linked book
  contributes nothing to the provisions leg (`--` for ULB); the `0.25 × Exp_ul` leg is `x` for ULB and
  `(x)` for WOL and WP where unit-linked business is written alongside.
- **LACTP `x` for WP only.** `Adj_TP` is capped at future discretionary benefits (`6.3(1)`), which only
  participating business carries. `(x)` for WOL means a **with-profits** whole of life.
- **RFF is bold `--` for ULB** on the strength of EIOPA Guideline 2(a): "conventional unit-linked
  products" and "conventional index-linked products" are generally outside RFF scope [R80c]. `(x)` for
  WOL means a with-profits WOL inside a with-profits fund.
- **MA portfolio is not an RFF** — the Glossary excludes it expressly [R43] — but it attracts the
  identical Own Funds 3L deduction and `SCR-SF 9.1` no-diversification treatment. That is why PA carries
  `--` on the RFF rows and `x` on the MA-portfolio rows.

**Own funds and MCR.**
- **Surplus funds `(x)` for WOL and PA** because the Surplus Funds Part applies per **with-profits
  fund**: a with-profits WOL or a with-profits deferred annuity written inside one is in the
  calculation; the same product written non-profit is not. Non-profit business written *inside* a
  with-profits fund is excluded from *with-profits assets* by the 1.2 definition [R79].
- **MCR `TP_l1`/`TP_l2` `(x)` for WOL and PA** for the same reason: the terms turn on "long-term
  insurance obligations **with profit participation**", not on the product name.
- **MCR capital at risk `(x)` for IP, WP, ULB and PA.** `CAR` is defined by what the firm "would
  currently pay on **death or disability**" [R78 3C.1(5)(a)]. IP engages the disability limb but the
  rule does not say how to express an income stream as a currently-payable amount. ULB and WP carry it
  only through the death benefit in excess of the fund or asset share. PA carries it only where there
  is a death benefit (guarantee period, value protection, spouse's reversion), where the sign is
  typically negative and the **per-contract** zero floor bites.
- **EPIFP `--` for every product** is not a product judgement: the requirement has been removed from
  Solvency UK reporting and disclosure altogether [R86 ¶¶4.43–4.44][R77].
- **Investments 3.1 bold for PA** because nature-and-duration matching is the substantive constraint on
  an annuity portfolio, and SS1/20 ¶1.7 ties PPP compliance directly to MA eligibility at **asset and
  portfolio** level [R119].

**Reporting, accounting and tax.**
- **The with-profits templates carry `(x)` outside WP** because IR.12.05/IR.12.06 are triggered by the
  firm's **with-profits net BEL > £500m**, and any of the other products **written in participating
  form** (WOL CWP/UWP, participating IP code 480/481, the UWP sibling of the unit-linked bond, WP
  pension annuities code 720) falls into a with-profits fund and therefore into the WPBR/FPRL
  decomposition. IR.12.06 **R0090 "future costs of financial options such as guaranteed annuity rates"**
  is the specific row a WOL or WP contract's GAR is reported in [R90].
- **IR.26.03 / IR.26.04 are both `?` for CI** — carried unchanged from the reporting stream, because the
  §12.4 derivation is this file's reasoning and not something a firm can point a supervisor at.
- **FRS 103 scope `(x)` for ULB.** A unit-linked bond frequently fails the significant-insurance-risk
  test and is an **investment contract** outside FRS 103, in FRS 102 Sections 11/12 and 23 — HMRC
  records exactly this: premiums held as **policyholder deposits** with only the fees treated as income
  [R18 LAM01100]. On the representative 100.1% death uplift the classification is a per-design
  determination, not a product-family fact.
- **The UK GAAP floor row is bold for TA, CI and ULB** because those are the three products where the
  Solvency UK number is routinely negative (TA, CI) or has a routinely negative component (ULB), so the
  IG2.41 non-negative / surrender-value floor produces the **largest divergence between the two
  ledgers**.
- **IFRS 17 VFA `(x)` for WOL** means a participating or unit-linked WOL; a non-profit WOL is GMM.
- **PA's IFRS 17 coverage-unit row is `?` deliberately.** The *requirement* to identify coverage units
  binds; the right answer for an annuity is an identified priority issue with continuing divergence
  [R106 §3 issue A].
- **Tax `(x)` on the BLAGAB row for TA, CI and IP** covers pre-2013 back-books: protection business
  written from **1 January 2013** is excluded from BLAGAB and taxed on a trading basis, but earlier
  policies continue as BLAGAB unless an election is made [R18 LAM01080].
- **s.833A bold for WP and PA** because the ring-fenced-fund surplus deduction (s.833A(5)(c)) and the
  matching-adjustment-portfolio surplus deduction (s.833A(5)(e)) are the two product-specific
  deductions in the distributable-profits formula [R104].

---

## Gaps and caveats

### 1. Fetch failures and things not retrieved

- **FCA Handbook COBS 20.2 could not be re-fetched.** The first attempt returned **HTTP 500**; the
  second returned a page whose content was **COBS 20.3**, not 20.2. Every COBS 20.2 statement in this
  file is therefore carried from the frozen **[R9]** entry (COBS 20.2 and 20.3 read 2026-08-03), from
  **SS1/14 ¶2.1–3.2** [R117] (which names 20.2.55R and 20.2.56R), or from the PRA's own cross-reference
  in the IR.12.05 instruction [R90] (which names **COBS 20.2.17R** as the basis for valuing
  reversionary bonuses). **No COBS 20.2 rule text is quoted anywhere in this file, and the
  target-range / MVR / required-percentage rule numbers are not asserted.**
- **SS20/16 [R120]: landing page only, 2,306 chars. The PDF was not retrieved.** Nothing about its
  content is claimed beyond publication dates and the one-sentence scope statement. The title itself is
  in conflict between two sources (see §3).
- **INSPRU 1.3 [R116] carries no rule text** — the page renders as "Deleted". **INSPRU 1.3.40 and
  1.3.190 have not been read by anyone in this library**, and nothing is asserted about what they said.
  Every statement about the WPBR/FPRL apparatus in this file comes from IR.12.06's instruction file
  [R90] or from FRS 103's glossary [R99], both of which are live documents.
- **INSPRU 1.2 [R115] was read only through two targeted WebFetch queries.** The application rule and
  rules 1.2.62/1.2.62A were quoted back verbatim; the rest of the chapter was not read. **INSPRU 1.5.35**
  — the Solvency I linked-asset coverage rule, cited by [R118] — was **not retrieved at all**, and its
  content is [unverified].
- **The Investments Part [R114] Chapter 1 future version (after 01/01/2027) was not retrieved**, nor
  was Chapter 6 (repackaged loans) read closely. The definitions of *linked long-term liabilities*,
  *linked benefits*, *units* and *with-profits fund* are Glossary terms and were **not** read from the
  Glossary itself in this stream; the *linked long-term liabilities* wording used in §9 is quoted from
  **[R118]**, a secondary source quoting the Rulebook. **Re-verify it against [R43] before publishing.**
- **SS1/20 [R119] chapters 2–8 were keyword-searched, not read.** No paragraph from chapters 2–8 is
  cited.
- **SS1/14 [R117]: the "Interaction with Solvency II" section was skimmed, not read closely**, and no
  paragraph from it is cited. The **URL is uncertain** (see the entry).
- **[R118] has no recorded URL.** The local text file preserves the document's title, publisher,
  authors and date but not the retrieval URL. It is cited without one rather than with a guessed one.
- **SS14/15 chapters 6–12** (separation of different with-profits business; significant changes;
  reducing new business / closing / run-off; **reattributions of inherited estate**; demutualisation;
  with-profits mutual waivers; Part VII transfers) — **headings verified, content not read**. A
  reattribution or Part VII section of a with-profits document must not be written from this file.
- **The PRA's Life Insurance Stress Test material, and any PRA publication on bulk purchase annuity
  pricing or market practice, were not sought.** Bulk annuities are out of the library's scope.

### 2. Numbers and text deliberately not transcribed

- **No stress size, correlation, factor or threshold is originated in this file.** Every one restated
  here (+15% mortality, −20% longevity, +35%/+25% inception, ±50% lapse, 40%/70% mass lapse, 4% CoC,
  λ 0.9/0.25, LGD 50%, MCR coefficients 0.037/−0.052/0.007/0.021/0.0007, AMCR £3.5m, 8.5%/14% NSLT
  sigmas, £500m and £50m/£10m reporting thresholds) is carried from the sibling stream that read the
  rule text, with its citation attached. **Nothing was recalled.**
- **The Annex XVI inputs to the health-catastrophe sub-modules were not retrieved by any stream** — the
  ratios `r_s`, `x_e` and `H_h` are unavailable, so `3C18`, `3C19` and `3C20` cannot be computed from
  this library's material even though their formulae are known [R62; R73 not retrieved].
- **COBS 20.2 rule numbers other than 20.2.17R, 20.2.55R and 20.2.56R are not stated**, and no
  target-range percentage, MVR bound or required percentage is given.
- **No IFRS 17 measurement mechanics are restated**; the VFA/GMM/PAA marks are classification marks
  taken from [R106].
- **The product design parameters** quoted in §1 and §13 (100.1% death uplift, 101% WP bond death
  benefit, 10th-anniversary MVR-free date, 5% MVR-free withdrawals, 1–30 year guarantee period,
  value protection, 3% escalation) are from the library's own `product-spec.md` files and carry the
  `[S#]` / `[std]` tags recorded there. **They are representative-design choices, not market facts.**

### 3. Conflicts between sources — recorded, not resolved

1. **SS14/15 is numbered twice** — **[R71]** (SCR stream) and **[R80b]** (own-funds stream), both
   scoped to chapter 2. This is a numbering defect in the library that a merge into
   `regulatory-and-actuarial-references.md` will have to resolve. This file does not add a third
   number and cites [R80b] for the whole document.
2. **SS20/16's title.** The Bank of England landing page reads "Solvency II: reinsurance –
   **counterparty credit risk**" [R120]; SS18/16 ¶2.1 refers to it as "Solvency II: reinsurance –
   **counterparty default risk**" [R48]. Both retrieved 2026-08-06.
3. **[R118] cites the Solvency I unit-linked reserve floor as INSPRU 1.2.62A**, which the FCA Handbook
   renders as **guidance**; the operative **rule** is INSPRU 1.2.62 R [R115].
4. **The technical-provisions stream marks TPFR 3.3(3) bold for TA; this file marks it `(x)`.** Both
   readings are defensible: the rule is *engaged* for TA (it confirms a full-term boundary) but does no
   work absent a repricing right. Recorded so the divergence is visible rather than silent.
5. **The technical-provisions stream marks WP `(x)` on the negative-best-estimate row; this file marks
   it `--`.** Same kind of divergence, on product grounds.
6. **The SCR stream marks lapse-up `x` uniformly across TA/CI/IP/WOL/WP/ULB; this file splits the
   direction per product** (§13.2). The underlying rule text (`3B6.2`/`3B6.3` filters) is the same in
   both; the difference is that this stream applied it to the representative designs.
7. **The SCR stream and the reporting stream both mark CI `?`; this file marks the SCR module rows on a
   derivation.** The derivation is set out step by step in §12.4 so that a reviewer can reject it.
   **If it is rejected, the CI column reverts to `?` on `3B`, `3C`, `3.10B`, IR.26.03 and IR.26.04.**
8. **`SS5/24 ¶1.7`** [R47] directs firms to read it with "Chapters 6, 7 and 11 of the Technical
   Provisions", but chapters 6 and 7 are the **deleted** MA chapters as at 05/08/2026 — a stale
   cross-reference recorded by the technical-provisions stream and repeated here because it bears
   directly on annuity documentation.

### 4. Questions the retrieved sources do not settle

1. **Whether an accelerated critical illness contract is unbundled under TPFR 26.7.** "Where possible"
   is not defined, and a benefit payable **once** on the earlier of two events resists unbundling. This
   determines whether the CI leg goes to `3C` and the death leg to `3B`, or the whole contract to one
   module. It also determines whether IR.26.03 or IR.26.04 is populated. **The single most consequential
   open question in this stream.**
2. **Whether a standalone critical illness lump sum is intended to be charged under `3C13` (the
   sub-module the Rulebook labels "income protection disability-morbidity").** §12.4 shows the textual
   chain; no retrieved document confirms the intent, and the conditional recovery/persistency limbs are
   vacuous for a lump-sum benefit, which is itself evidence the rule was not drafted with CI in mind.
3. **Which RAO Schedule 1 Part II class a standalone CI contract falls in** (I or IV). [R14] verifies
   the class list only.
4. **What "similar technical basis to that of long-term insurance business" means operationally.** It
   is the hinge of TPFR 26.3, the `SLT health` / `NSLT health` Glossary definitions and `3C11.2`, and
   no retrieved source gives a test. Two firms writing identical IP or CI books can land in different
   modules.
5. **Whether a regular-premium unit-linked contract with a small death uplift fails TPFR 3.5(1).** The
   "no discernible effect on the economics of the contract" qualifier is undefined and the answer
   changes the boundary — and therefore the sign of the best estimate — completely.
6. **How MCR capital at risk is computed for a disability income benefit** (MCR 3C.1(5)(a)).
7. **Whether the FRS 103 "realistic value of liabilities" (INSPRU 1.3.40 as at 31/12/2015) and the
   IR.12.06 with-profits benefits reserve (Surplus Funds 3.2) give the same number.** They share an
   ancestry; no retrieved source says they coincide, and §5 deliberately treats them as two definitions.
8. **Whether FRS 103 ¶3.10's DAC prohibition reaches a with-profits fund that was never in the pre-2016
   realistic capital regime** — flagged by the accounting stream [R99 ¶3.1(b), R100 IG1.1] and carried
   here because it changes the WP DAC mark.
9. **Whether the numbered lines of business used in the SCR Parts are formally the TPFR Annex 1 lines.**
   TPFR 26.1 scopes Annex 1 to "the lines of business referred to in 10.1 of the Technical Provisions
   Part". The SCR Parts use the same numbering (retrieval fact 1), and no other numbered list was
   found, but no retrieved rule says so. **If a separate SCR annex exists with different numbering, the
   entire `3.10B` mapping in §12 is wrong.**
10. **The IFRS 17 coverage-unit basis for an annuity** [R106 §3 issue A].
11. **Whether SS1/20's silence on unit-linked matching is deliberate.** No PRA supervisory statement
    retrieved by any stream addresses unit matching. The only source in the library is [R118], a
    consultancy paper. **A UK unit-linked document must say that the PRA has published no guidance on
    the practice, rather than implying supervisory endorsement.**

### 5. Fetch behaviour observed on 2026-08-06

- `prarulebook.co.uk` — HTTP 403 to plain fetchers, HTTP 200 to the browser-UA helper. All Rulebook
  Parts in this file came from local copies retrieved that way.
- `bankofengland.co.uk` — same; SS1/20 (47,081 chars) and the SS20/16 landing page (2,306 chars) were
  retrieved with the helper.
- `handbook.fca.org.uk` — WebFetch works. INSPRU 1.2 returned content on both attempts; **INSPRU 1.3
  returns a "Deleted" stub**; **COBS 20.2 returned HTTP 500 once and COBS 20.3 content once** — treat
  the COBS 20 chapter pages as unreliable and prefer the frozen [R9] record.
- `legislation.gov.uk`, `gov.uk`, `frc.org.uk` — not exercised in this stream; the sibling streams'
  observations stand.
