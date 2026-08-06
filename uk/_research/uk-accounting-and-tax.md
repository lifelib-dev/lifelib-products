# UK statutory accounts, IFRS 17 and tax — research notes (UK regulatory documentation)

**Stream:** UK statutory accounts, IFRS 17 and tax
**Access date for every citation below:** 2026-08-06
**Status:** research notes, not yet merged into `uk/references/regulatory-and-actuarial-references.md`

---

## Scope and numbering note

This stream owns reference block **R99–R113**. Entries **R1–R38** live in
`uk/references/regulatory-and-actuarial-references.md`, are **frozen**, and are already cited by
the seven UK product documents; nothing below renumbers, restates or duplicates them. Existing
entries that bear on this stream are listed in the next section with a one-line note on how they
bite, and are cited as `[R#]` throughout without being re-created. **All fifteen numbers R99–R113
are used; none are spare.**

Deliberately left to other streams: technical provisions / best estimate / matching adjustment
(stream 1); SCR, MCR and own funds as capital quantities (stream 2); regulatory reporting and
governance — SFCR, QRTs, ORSA, actuarial function (stream 3); per-product application (stream 5).
Two exceptions are inside this stream's brief and are documented here even though the underlying
Parts belong to streams 1/2: **Valuation Part Chapter 11 (deferred taxes)** at R111, and
**SCR – Standard Formula Part Chapter 6 (loss-absorbing capacity of technical provisions and
deferred taxes)** at R112. Both were read *only* for the tax interface. If streams 1/2 create
their own entries for these Parts, cite theirs for TP/SCR content and R111/R112 only for the
deferred-tax rules quoted below.

**Six retrieval facts that change how this material must be documented.**

1. **The UK contrast is not the U.S. contrast, and is close to its mirror image.** The U.S.
   research file opens on SSAP No. 71 — acquisition costs expensed as incurred, no DAC asset,
   first-year surplus strain. In the UK the *statutory accounts* go the other way: **Schedule 3
   paragraph 13 to SI 2008/410 requires** acquisition costs relating to a subsequent financial
   year to be deferred [R105], and **FRS 103.3.7 requires** deferral subject to recoverability
   tests [R99]. So there is no UK accounts analogue of the U.S. statutory new-business strain.
   The UK strain lives in (a) the **Solvency UK** own-funds movement, where there is no DAC asset
   at all because the balance sheet is market-consistent [R1][R111], and (b) historically in the
   **tax** computation, where FA 2012 s.79 spread acquisition expenses over seven years
   independently of the accounts [R17][R18] — a rule now repealed (fact 5 below). Any drafting
   that ports the U.S. framing across will be wrong.

2. **FRS 103 is a grandfathering standard, not a measurement standard.** It is built on IFRS 4
   (as extant in 2013), FRS 27 and the withdrawn ABI SORP [R99 Overview (iii)]. It exempts
   insurers from the FRS 102 hierarchy for insurance-contract policies [R99 ¶2.12], permits
   existing practices to continue [R99 ¶2.6], and allows policy change only if the change makes
   the statements more relevant and no less reliable, or vice versa [R99 ¶2.3]. Consequently
   **there is no single "UK GAAP insurance liability"**: the measurement basis is entity-specific.
   The standard supplies a *benchmark* (Section 3, built on the pre-2016 modified statutory
   solvency basis) plus a floor (the liability adequacy test) plus the Schedule 3 presentation.

3. **FRS 103 is not aligned with IFRS 17 and, on the FRC's own analysis, cannot be under current
   company law.** The FRC states that conflicts between IFRS 17 and UK company law make alignment
   impossible; entities applying FRS 103 are necessarily preparing "Companies Act accounts" under
   s.395(1) CA 2006, whose form and content must comply with Schedule 3 to SI 2008/410, "which
   cannot be adapted"; the FRC concluded in 2019 that IFRS 17's approach is so fundamentally
   different from the Schedule 3 formats that IFRS 17 cannot be applied in Companies Act accounts
   while maintaining compliance with company law [R101]. A UK life insurer's individual-accounts
   choice is therefore **binary and consequential**: Companies Act accounts (FRS 102 + FRS 103,
   or FRS 101) versus IAS individual accounts (IFRS 17) [R103 s.395(1)].

4. **The IFRS 17 standard text is paywalled.** The IFRS Foundation's IFRS 17 page offers an
   overview, standard history and project links, but the standard text itself is behind the IFRS
   Digital subscription / IFRS Foundation shop [R107]. **Every IFRS 17 mechanic below is taken
   from the UK Endorsement Board's own Endorsement Criteria Assessment [R106]**, which quotes
   IFRS 17 paragraph numbers directly and is the UK adopting body's description of the standard
   it adopted. Where R106 quotes an IFRS 17 paragraph, the paragraph number is reliable; where it
   summarises, the summary is R106's and is tagged as such. Nothing here is paraphrased from
   memory of the standard.

5. **The seven-year tax spreading of acquisition expenses is gone.** FA 2012 s.79 is **repealed
   for accounting periods beginning on or after 1 January 2023** by FA 2022 Sch 5 Part 2,
   commenced by SI 2022/1164 [R109][R18 LAM04130]. From that date a deduction is given when
   amounts are recognised in the income statement under GAAP — for all BLAGAB writers, IFRS and
   UK GAAP alike. Unrelieved pre-2023 spread amounts continue to run off under the old rule, and
   FA12 s.77(3) continues to disallow accounts DAC amortisation that was already relieved
   [R18 LAM04130]. Descriptions of "1/7th per year" without a date qualifier are stale.

6. **The HMRC Life Assurance Manual carries a standing currency warning and contains
   demonstrably stale passages.** LAM01000 and LAM08000 both open "This manual has yet to be
   updated for the interest restriction and changes to relief for carried forward losses
   introduced by Finance (No.2) Act 2017" [R18]. LAM01090 still describes EIOPA-driven EU
   regulation and speculates that "The UK leaving the EU may bring branches of EEA companies
   within PRA regulation" [R18]. LAM01160's worked example uses a 19% CT rate and a 20%
   policyholder rate "in 2018" [R18]. LAM05020 notes regulation-making powers "unused as at
   June 2018" [R18]. Use the LAM for *mechanics*; take rates and regulatory framing from R110 and
   from the PRA Rulebook.

**Copyright caution (applies to R99, R100, R102 and anything drawn from them).** FRS 103 and
FRS 102 are FRC copyright and contain IFRS Foundation copyright material reproduced under
licence, with rights reserved and third-party rights granted only as permitted by the FRC terms
of use [R99 front matter]. Product documentation must **paraphrase** and cite the paragraph, not
paste standard text. Everything in "Extracted mechanics" below is paraphrase plus short
attributed quotation.

---

## Existing entries (R1–R38) that bear on this stream

| R# | Short title | How it bears on statutory accounts, IFRS 17 and tax |
|----|-------------|------------------------------------------------------|
| R1 | PRA Rulebook — Technical Provisions Part | The Solvency UK liability the accounts do **not** equal. FRS 103 permits an entity setting insurance-contract policies for the first time to base them on "the rules for the recognition and measurement of technical provisions in the PRA Rulebook" subject to appropriate adjustments [R99 ¶1.5(b)], and names greater alignment with those rules as a legitimate reason to change policy [R99 ¶2.3A]. Valuation 11.2 measures deferred tax off the difference between the Technical Provisions Part value and the tax value [R111]. |
| R2 | PRA Rulebook — Matching Adjustment Part | Regulatory-only discount enhancement. FRS 103 BC55 lists the volatility adjustment, the risk margin, transitional adjustments and surplus funds as items to consider adjusting when building accounting policies off the prudential rules [R99 BC55] — MA is the UK analogue that would need the same treatment. CA 2006 s.833A(5)(e) adds the MA portfolio's asset-over-liability excess back as a **deduction** in the distributable-profits formula [R104]. |
| R3 | PRA Rulebook — Transitional Measure on Technical Provisions | Regulatory-only; FRS 103 BC55(a) flags "transitional adjustments that may be made for regulatory purposes" as something to strip out of an accounts basis [R99]. |
| R4 | Risk Margin Regulations 2023 (SI 2023/1346) | Regulatory-only; FRS 103 BC55(c) flags "the risk margin that is applied for regulatory purposes" as an adjustment item [R99]. The IFRS 17 counterpart is the risk adjustment for non-financial risk [R106 ¶2.48] — a different quantity on a different calibration. |
| R5 / R6 / R7 | PS10/24, PS15/24, PS2/24 | The Solvency UK reform stream that moved the regulatory balance sheet; none of it moved the accounts. |
| R9 | FCA Handbook COBS 20 — With-profits | Supplies the PPFM that FRS 103 IG1.13 requires management actions in a market-consistent stochastic guarantee valuation to be consistent with [R100], and that R106 ¶3.138 identifies as governing the 90:10 attribution of with-profits fund profits [R106]. |
| R10 | FCA Handbook COBS 21.3 — Permitted links | Defines what a linked fund may hold; the accounts counterpart is Schedule 3 liabilities item D "Technical provisions for linked liabilities" [R105 note 26]. |
| R13 | FSMA 2000 | s.843 CA 2006 and Schedule 3 both hang definitions off FSMA — "long-term business" is FSMA s.22 business [R104 s.843(7)], and the actuarial investigation is one carried out under FSMA Part 9A rules [R104 s.843(6)]. |
| R14 | RAO 2001 Sch 1 Part II | Sets which contracts sit in the **long-term business technical account** rather than the general business technical account [R105 para 1; R99 glossary "technical account"]. FA 2012 s.64 borrows the same RAO definitions for tax [R18 LAM01090]. |
| R15 | ITTOIA 2005 Part 4 Ch 9 — chargeable events | **Policyholder-level** tax. Distinct from and additional to the company-level I-E charge; HMRC frames I-E as a proxy for the basic-rate income tax a policyholder would otherwise pay, with credit given at chargeable-event time [R18 LAM02010, LAM01160]. |
| R16 | HMRC IPTM | Policyholder-side manual; the counterpart to the LAM on the company side. |
| R17 | Finance Act 2012, Part 2 | **The operative company tax law for this stream.** Sections read directly this session: s.73 (the six I-E steps) [R17]. Sections read only through HMRC's description: s.57, s.63–66, s.68–72, s.74–85, s.92–94, s.97–101, s.102–105, s.114–115, s.127, s.137. Per the library's rule, specific sections of an Act already carrying a frozen entry stay under that entry — cite `[R17]` for the law and `[R18]` for HMRC's application. |
| R18 | HMRC Life Assurance Manual (LAM) | **Extended heavily by this stream.** Pages read in full on 2026-08-06: LAM01000, 01080, 01090, 01100, 01160; 02000, 02010, 02050, 02060; 03020; 04000, 04010, 04110, 04130; 05000, 05020; 06000, 06010, 06020; 07230; 08000; 11010; 16000, 16010, 16020, 16050, 16060. All LAM content below is cited `[R18 LAM#####]`. |
| R21 | Taxation of Pensions Act 2014 | Pension business is excluded from BLAGAB (FA12 s.57(2)(a)) and taxed on trade profits [R18 LAM01080] — the reason a pension-annuity model needs no I-E engine. |
| R33 / R34 | FRC TAS 100 / TAS 200 | FRS 103 BC40 records that FRC Technical Actuarial Standards "apply to a wide range of actuarial work and may be relevant when implementing aspects of FRS 103" [R99 BC40]. Schedule 3 para 52(3) requires the long-term business provision to be computed annually by a Fellow of the IFoA [R105]. |
| R38 | UKEB — IFRS 17 (UK adoption) | The **adoption record**: adopted 16 May 2022, effective 1 January 2023. R106 (this stream) is the UKEB's technical assessment behind that adoption and is where the mechanics come from. Cite R38 for adoption facts, R106 for measurement mechanics. |

---

## New entries

All URLs below were requested on **2026-08-06** and their HTTP status observed. PDFs were
downloaded and text-extracted locally with `pypdf`; HTML was extracted with BeautifulSoup. A
browser User-Agent was required for `prarulebook.co.uk`. No URL on this page is fabricated.

### A. UK GAAP — the statutory accounts standards

#### R99. FRS 103 *Insurance Contracts* (September 2024 edition)
- **Publisher:** Financial Reporting Council
- **URL:** https://www.frc.org.uk/documents/7669/FRS_103_September_2024_rSi5poe.pdf
  (from the FRC library page at R101)
- **Doc type:** accounting standard. **Accessed:** 2026-08-06.
- **fetched_ok:** yes (PDF, 593,853 bytes → 171,294 chars text; Sections 1–6, Appendix I Glossary,
  Appendix III and the Basis for Conclusions read directly)
- **Annotation:** The operative UK GAAP standard for insurance contracts. Verified structure:
  Section 1 Scope, Section 2 Accounting Policies/Recognition and Measurement, Section 3
  Recognition and Measurement — requirements for entities with long-term insurance business,
  Section 4 Disclosure, Section 5 Disclosure — additional requirements for with-profits business,
  Section 6 Transition; Appendices I Glossary, II Definition of an insurance contract, III Note on
  legal requirements, IV Republic of Ireland references; Basis for Conclusions. Verified content
  load-bearing for this library: applies to entities applying FRS 102, insurer or not, to
  insurance contracts issued, reinsurance held, and other financial instruments issued with a
  discretionary participation feature (¶1.2); effective for periods beginning on or after
  1 January 2015 (¶1.11), with Periodic Review 2024 amendments effective for periods beginning on
  or after 1 January 2026 except the Section 6 amendment, effective 1 January 2024 (¶1.11D);
  policy change permitted only under ¶2.3; alignment with the PRA Rulebook technical-provisions
  rules named as one legitimate basis for change (¶2.3A) and as an alternative starting point for
  first-time policy-setters (¶1.5(b)); liability adequacy test (¶¶2.14–2.18); DPF guaranteed
  element/equity split (¶2.30); shadow accounting (¶2.11); premium and claim recognition
  (¶¶3.3–3.6); **acquisition costs shall be deferred** subject to three carve-outs (¶3.7) and
  amortised over no longer than the recoverability period and "in a similar profile to those
  margins" (¶3.9); **acquisition costs shall not be deferred for with-profits funds** (¶3.10);
  MSSB as the established basis and realistic value of liabilities for with-profits funds
  (¶¶3.11–3.15); VIF (¶¶3.16–3.18); FFA disclosure and negative-FFA explanation (¶¶5.4–5.5).
  Glossary definitions verified: MSSB, realistic value of liabilities, gross premium method, net
  premium method, linked business, technical account, non-technical account, PPFM, DPF, liability
  adequacy test, deferred acquisition costs (long-term business), options and guarantees,
  "Regulations" = SI 2008/410, "Act" = Companies Act 2006. Basis for Conclusions ¶¶43–55 record
  the May 2016 Solvency II amendments, the deliberate decision **not** to require a
  Solvency II-based measurement, and (BC55) the four items to consider adjusting if an entity
  does build policies off the prudential rules.
- **Products:** all seven, for entities preparing Companies Act accounts.

#### R100. Implementation Guidance to accompany FRS 103 *Insurance Contracts* (September 2024)
- **Publisher:** Financial Reporting Council
- **URL:** https://www.frc.org.uk/documents/7663/Implementation_Guidance_to_accompany_FRS_103_Insurance_Contracts_September_2024_HvmQYVX.pdf
- **Doc type:** non-mandatory implementation guidance. **Accessed:** 2026-08-06.
- **fetched_ok:** yes (PDF, 377,687 bytes → 81,231 chars; page 1 text extraction failed, all
  substantive pages extracted; Section 1 (IG1.1–IG1.13) and the long-term parts of Section 2 read)
- **Annotation:** Explicitly "accompanies, but is not part of, FRS 103" and does not carry the
  authority of a standard [R101]. It is nonetheless the only published UK source that says how to
  compute the with-profits adjustments. Verified: IG1.2 — the shareholders' share of projected
  future bonuses is the value of future shareholder transfers on **market-consistent financial
  assumptions**, with non-economic assumptions consistent with the realistic value of liabilities,
  taken to the FFA together with any related tax liability; IG1.3–IG1.9 — recognition and
  measurement of the VIF on non-participating business inside a with-profits fund, including the
  requirement to strip out any release of capital requirements from the VIF because MSSB
  liabilities carry no capital allowance (IG1.7); IG1.10 — realistic-versus-MSSB differences are
  transferred to/from the FFA so there is **generally no effect on profit or equity**, except
  where the FFA goes negative; IG1.11–IG1.13 — options and guarantees measured at fair value or by
  market-consistent stochastic model, deterministic approaches "generally fail to deal
  appropriately with the time value of the option", management actions in each scenario must be
  implementable and consistent with the PPFM. Section 2 verified: IG2.39 — gross premium method
  for every class except those valued by net premium method in the regulatory returns; IG2.41 — no
  policy may have an overall negative provision except as allowed by PRA rules, nor a provision
  below any guaranteed surrender or transfer value; IG2.42 — the long-term business provision may
  be computed on the regulatory basis subject to appropriate adjustments; IG2.43 — the assumption
  categories to disclose (premiums, persistency, mortality and morbidity, interest rates, discount
  rates and risk-margin basis); IG2.44 and IG2.49 — where the provision or the linked-liability
  provision has regard to the timing of tax, that effect must be **excluded from the determination
  of deferred tax**; IG2.45 — with-profits future-bonus allowance disclosure; IG2.47–IG2.48 —
  linked provision not below the fund-referenced surrender/transfer value, and mismatching between
  net linked assets and linked technical provisions must be explained; IG2.50 — an FFA is
  appropriate only where allocation between policyholders and owners is not clear cut; IG2.61 —
  reinsurance assets measured consistently with the related liability.
- **Products:** WP and WOL (IG1 series); all (IG2 series); ULB (IG2.47–IG2.49).

#### R101. FRC library page — *FRS 103 Insurance Contracts*
- **Publisher:** Financial Reporting Council
- **URL:** https://www.frc.org.uk/library/standards-codes-policy/accounting-and-reporting/uk-accounting-standards/frs-103/
- **Doc type:** standard-setter web page (edition register + policy statement). **Accessed:** 2026-08-06.
- **fetched_ok:** yes (HTML)
- **Annotation:** A genuinely different document from the standard, and the only place the FRC
  states its position on FRS 103 versus IFRS 17. Verified verbatim: "FRS 103 is not aligned with
  IFRS 17"; the FRC "is likely to wait for several years' implementation experience before
  considering alignment"; "Conflicts between IFRS 17 and UK company law mean that it is not
  currently possible to align FRS 103 with IFRS 17"; entities applying FRS 103 "will necessarily
  be preparing 'Companies Act accounts' as set out in section 395(1) of the Companies Act 2006";
  the form and content of Companies Act individual accounts of insurance companies must comply
  with Schedule 3 to SI 2008/410, "which cannot be adapted"; and the FRC "concluded in 2019 that
  the approach and methodology that underpins IFRS 17 is so fundamentally different to the one
  that underpins the formats of Schedule 3 that for Companies Act accounts it is not possible to
  apply IFRS 17 whilst continuing to maintain compliance with company law." Also verified: the
  current edition is September 2024 (published 10 September 2024, 579.9 KB); superseded editions
  January 2022, March 2018, February 2017, March 2014; the Periodic Review 2024 amendment
  (27 March 2024) is effective 1 January 2026 with early application permitted, except a Section 6
  Transition requirement effective 1 January 2024; a May 2016 "Amendments to FRS 103 – Solvency II"
  amendment exists; and a February 2017 BEIS letter on Solvency II clarification is published here
  (see R113).
- **Products:** all.

#### R102. FRS 102 *The Financial Reporting Standard applicable in the UK and Republic of Ireland* (September 2024 edition)
- **Publisher:** Financial Reporting Council
- **URL:** https://www.frc.org.uk/documents/7668/FRS_102_September_2024_tmKYWO6.pdf
- **Doc type:** accounting standard. **Accessed:** 2026-08-06.
- **fetched_ok:** yes (PDF, 2,829,292 bytes → 1,336,205 chars; Section 1 scope, Section 7.10E,
  Section 29 Income Tax and the Section 29 Basis for Conclusions read; the rest indexed by search)
- **Annotation:** The host standard. Verified: ¶1.6 — an entity **shall apply FRS 103** to
  insurance contracts it issues, reinsurance contracts it holds, and financial instruments with a
  DPF that it issues, so FRS 102 itself contains no insurance measurement model; insurance
  contracts and DPF instruments are carved out of Sections 11, 12, 21, 22 and 23 by cross-
  reference to FRS 103. **Section 29 Income Tax** verified in detail because it is the UK GAAP
  deferred-tax model and differs structurally from IAS 12: ¶29.6 deferred tax is recognised on
  **timing differences** — "differences between taxable profits and total comprehensive income …
  that arise from the inclusion of income and expenses in tax assessments in periods different
  from those in which they are recognised in financial statements" — **not** on balance-sheet
  temporary differences; ¶29.7 deferred tax assets only to the extent probable of recovery;
  ¶29.10 no deferred tax on permanent differences except ¶29.11 business combinations; ¶29.12
  measurement at rates enacted or substantively enacted at the reporting date expected to apply on
  reversal; ¶29.13 average rates where rates are banded; ¶29.16 deferred tax on fair-valued
  investment property; ¶29.2B and ¶29.12A exclude Pillar Two deferred tax from recognition,
  disclosure and measurement. Basis for Conclusions B29.1–B29.7 confirms the FRC deliberately
  adopted a "timing differences plus" approach rather than IAS 12's temporary-difference model.
  ¶7.10E: an insurance financial institution should include the cash flows of its long-term
  business "only to the extent of cash transferred and available to meet the obligations of the
  company or group as a whole" — the cash-flow-statement counterpart of the long-term-fund
  ring-fence.
- **Also fetched, same date (R102b):** FRC library page for FRS 102,
  https://www.frc.org.uk/library/standards-codes-policy/accounting-and-reporting/uk-accounting-standards/frs-102/
  — verified: FRS 102 is periodically reviewed roughly every five years; the Triennial Review 2017
  was effective 1 January 2019; the **Periodic Review 2024 was completed in March 2024 with a
  principal effective date of 1 January 2026**; a further amendment "Adapted formats" published
  18 February 2026 is effective **1 January 2027** and arises from the replacement of IAS 1 by
  IFRS 18, affecting entities that adapt a balance sheet or profit and loss account format.
- **Products:** all, for Companies Act accounts preparers.

### B. Company law — the statutory accounts framework and the distribution gate

#### R103. Companies Act 2006, Part 15 — accounts and reports (s.395 read; s.396 by cross-reference)
- **Publisher:** legislation.gov.uk
- **URL:** https://www.legislation.gov.uk/ukpga/2006/46/section/395
  (Part 15 Chapter 4 also retrieved at https://www.legislation.gov.uk/ukpga/2006/46/part/15/chapter/4)
- **Doc type:** primary legislation. **Accessed:** 2026-08-06.
- **fetched_ok:** yes (s.395 read in full; text "up to date with all changes known to be in force
  on or before 05 August 2026")
- **Annotation:** The provision that makes the UK basis choice binary. Verified: s.395(1) — a
  company's individual accounts may be prepared either "in accordance with section 396
  ('Companies Act individual accounts')" or "in accordance with UK-adopted international
  accounting standards ('IAS individual accounts')"; s.395(3) — after the first IAS year all
  subsequent individual accounts must be IAS accounts **unless there is a relevant change of
  circumstance**, defined in s.395(4) as the company becoming a subsidiary of a non-IAS parent,
  ceasing to be a subsidiary, or the company or its parent ceasing to have securities admitted to
  trading on a UK regulated market. Consequence for this library: the choice between
  FRS 102 + FRS 103 and IFRS 17 is a *company-law* choice at the individual-entity level, is
  effectively one-way absent a listed trigger, and is separate from the group's consolidation
  basis.
- **Products:** all (entity-level).

#### R104. Companies Act 2006, Part 23 — distributions (ss.830, 833A, 843)
- **Publisher:** legislation.gov.uk
- **URLs:** https://www.legislation.gov.uk/ukpga/2006/46/section/830 ,
  https://www.legislation.gov.uk/ukpga/2006/46/section/833A ,
  https://www.legislation.gov.uk/ukpga/2006/46/section/843
- **Doc type:** primary legislation. **Accessed:** 2026-08-06.
- **fetched_ok:** yes (all three sections read in full)
- **Annotation:** **The single most surprising fact in this stream.** Verified: s.830(1)–(2) — a
  company may distribute only out of accumulated realised profits less accumulated realised
  losses; s.830(3) makes this subject to s.833A for "Solvency 2 insurance companies". **s.833A**
  (inserted 30 December 2016 by SI 2016/1194, amended 1 November 2024 by SI 2024/1083) applies to
  any authorised insurance company carrying on long-term business authorised under Article 14 of
  the Solvency 2 Directive, and **replaces** the accounts-based realised profit for s.830(2)
  purposes with the formula **A − L − D**, where A is the total value of assets, L the total value
  of liabilities and D the total of the s.833A(5) deductions, all measured at the balance-sheet
  date: (a) excess of the value of shares in a qualifying investment subsidiary over consideration
  given, (b) any asset representing a defined benefit pension scheme surplus, (c) the excess of
  ring-fenced fund assets over ring-fenced fund liabilities, (d) deferred tax liabilities relating
  to (a)–(c), (e) where the firm has a matching adjustment permission, the excess of the assigned
  asset portfolio over the value of the MA obligations, and (f) paid-in ordinary share capital and
  related share premium, paid-in preference shares that are not liabilities and related share
  premium, capital redemption reserve, and any other non-distributable reserve. s.833A(3) caps
  distributable profits at accumulated profits (realised or not) less accumulated losses.
  s.833A(7) requires assets and liabilities to be valued under **Part 2 of the Insurance and
  Reinsurance Undertakings (Prudential Requirements) Regulations 2023**, PRA rules on the matching
  adjustment, other PRA rules implementing Solvency II Articles 75–85 and 308b–308e, and Delegated
  Regulation (EU) 2015/35 Articles 7–52 and 55–61. s.833A(8) applies the section as if the company
  carried on only long-term business, with just and reasonable apportionment for composites.
  **s.843** (which applies to authorised long-term insurers **other than** those within s.833A and
  other than insurance SPVs) treats an unallocated long-term-fund surplus shown by an actuarial
  investigation as a realised profit and a deficit as a realised loss, and provides that "any
  profit or loss arising in the company's long-term business is to be left out of account"
  otherwise (s.843(5)). Modelling consequence: for a Solvency-UK-authorised UK life insurer,
  **dividend capacity is driven by the Solvency UK balance sheet, capped by accounts accumulated
  profits — it is not the accounts profit**.
- **Products:** all (entity-level).

#### R105. The Large and Medium-sized Companies and Groups (Accounts and Reports) Regulations 2008 (SI 2008/410), **Schedule 3** — insurance companies: form and content of accounts
- **Publisher:** legislation.gov.uk
- **URL:** https://www.legislation.gov.uk/uksi/2008/410/schedule/3
- **Doc type:** statutory instrument (schedule). **Accessed:** 2026-08-06.
- **fetched_ok:** yes (HTML, 300,310 bytes → 116,468 chars; balance sheet format and notes,
  profit and loss account formats, Part 2 Section E provisions rules read)
- **Annotation:** The statutory format an insurer's Companies Act accounts must take — the UK
  counterpart of the NAIC annual statement blank in structural role, though not in content.
  Verified balance sheet liabilities structure: A Capital and reserves; B Subordinated liabilities;
  **Ba Fund for future appropriations** (note 19); C Technical provisions — C.1 unearned premiums,
  **C.2 Long-term business provision** (notes 20, 21, 26), C.3 Claims outstanding, C.4 Provision
  for bonuses and rebates, C.5 Equalisation provision, C.6 Other technical provisions;
  **D Technical provisions for linked liabilities** (note 26); E Provisions for other risks
  (including provisions for taxation); assets item **G.II Deferred acquisition costs** (note 17).
  Verified notes: note 17 — DAC comprises acquisition costs incurred in a financial year but
  relating to a subsequent year, **except** where the long-term business provision already
  recognises them explicitly or implicitly (by anticipation of future income), with disclosure of
  the treatment and of the amount explicitly recognised; note 19 — the FFA comprises "all funds
  the allocation of which either to policyholders or to shareholders has not been determined by
  the end of the financial year", with transfers shown at P&L item II.12a; note 21 — the long-term
  business provision is "the actuarially estimated value of the company's liabilities (excluding
  technical provisions included in liabilities item D), including bonuses already declared and
  after deducting the actuarial value of future premiums", plus IBNR and settlement costs;
  note 26 — linked technical provisions cover liabilities whose benefits are determined by
  reference to the value of, or income from, property or an index, and **any additional provisions
  for death risk, operating expenses or other risks (such as maturity benefits or guaranteed
  surrender values) must go into item C.2**, not item D. Verified special rules: **para 13 — "The
  costs of acquiring insurance policies which are incurred during a financial year but which relate
  to a subsequent financial year must be deferred"**; para 11(1) — every balance sheet of a
  long-term insurer must show separately the aggregate of amounts in capital and reserves that
  s.843 CA 2006 requires **not** to be treated as realised profits; para 11(2) — the total amount
  of assets representing the long-term fund must be shown; para 52(1) — the long-term business
  provision must in principle be computed **separately for each long-term contract**, with
  statistical or mathematical methods permitted where they give approximately the same result;
  para 52(2) — a summary of principal assumptions must be given in the notes; para 52(3) — the
  computation must be made annually by a Fellow of the Institute or Faculty of Actuaries "with due
  regard to generally accepted actuarial principles and on the basis of recognised actuarial
  methods" (the words "with due regard to generally accepted actuarial principles and" were
  **inserted**, and a following phrase omitted, by SI 2019/145 with effect for financial years
  beginning on or after IP completion day — see the conflict recorded at R113). Verified long-term
  business technical account format (Part 1, format II): 1 Earned premiums net of reinsurance
  (gross premiums written / outward reinsurance premiums / change in unearned premiums provision);
  2 Investment income; 3 Unrealised gains on investments; 4 Other technical income; 5 Claims
  incurred net of reinsurance (claims paid gross / reinsurers' share; change in provision for
  claims gross / reinsurers' share); 6 Change in other technical provisions — **6(a) Long-term
  business provision net of reinsurance**, 6(b) other; 7 Bonuses and rebates; 8 Net operating
  expenses — 8(a) acquisition costs, **8(b) change in deferred acquisition costs**, 8(c)
  administrative expenses, 8(d) reinsurance commissions and profit participation; 9 Investment
  expenses and charges; 10 Unrealised losses on investments; 11 Other technical charges;
  **11a Tax attributable to the long-term business**; 12 Allocated investment return transferred to
  the non-technical account; **12a Transfers to or from the fund for future appropriations**;
  13 Sub-total (balance on the technical account — long-term business). The non-technical account
  picks that balance up at item III.2, with **III.2a Tax credit attributable to balance on the
  long-term business technical account**.
- **Products:** all seven, for Companies Act accounts preparers.

### C. IFRS 17 as adopted for use in the UK

#### R106. UK Endorsement Board — *Endorsement Criteria Assessment: IFRS 17 Insurance Contracts* ("ECA — IFRS 17")
- **Publisher:** UK Endorsement Board
- **URL:** https://www.endorsement-board.uk/documents/666/ECA_-_IFRS_17.pdf
  (linked from the UKEB IFRS 17 project page at [R38])
- **Doc type:** endorsement criteria assessment (technical assessment supporting UK adoption).
  **Accessed:** 2026-08-06.
- **fetched_ok:** yes (PDF, 1,840,287 bytes → 478,447 chars; Section 2 "Description of IFRS 17"
  read in full, Section 3 priority issue D "With-profits: inherited estates" read, remainder
  indexed by search; one page failed text extraction)
- **Annotation:** **The substitute for the paywalled standard.** Section 2 is a systematic
  description of IFRS 17 written by the UK adopting body, quoting IFRS 17 paragraph numbers.
  Verified content includes: level of aggregation — portfolios of contracts "subject to similar
  risks and managed together" [IFRS 17:14], divided into a minimum of three sub-groups (onerous at
  initial recognition; no significant possibility of becoming onerous; remainder), with contracts
  issued more than one year apart barred from the same group (the **annual cohorts** requirement),
  groups fixed at initial recognition and never reassessed (¶¶2.14–2.17); measurement as fulfilment
  cash flows plus contractual service margin (¶2.19); **GMM** initial recognition — present value
  of probability-weighted expected cash flows reflecting financial risk, plus an explicit risk
  adjustment for non-financial risk, plus the CSM (¶2.43); contract boundary [IFRS 17:34] (¶2.45);
  discount rate principles [IFRS 17:36] quoted verbatim (¶2.46); risk adjustment definition
  [IFRS 17 Appendix A] quoted verbatim (¶2.48); CSM as a residual measured so there is no income
  or expense on initial recognition, and **zero with an immediate loss for onerous groups**
  (¶2.50); subsequent measurement as liability for remaining coverage (FCF for future service +
  CSM) plus liability for incurred claims (FCF for past service) [IFRS 17:40] (¶2.51); CSM
  released by **coverage units** reflecting the quantity of benefits and expected coverage period
  (¶2.54); acquisition cash flows included in the FCF, recognised as an asset before the group is
  recognised then subsumed into the CSM, with the premium element intended to cover them added
  back to insurance revenue and an equal insurance service expense over the coverage period
  (¶¶2.56–2.59); **VFA** — applies to insurance contracts with direct participation features,
  "substantially investment-related service contracts under which an entity promises an investment
  return based on underlying items" [IFRS 17:B101], the variable fee being the entity's share of
  the fair value of underlying items less FCF that do not vary with underlying item returns,
  eligibility assessed at inception and never reassessed absent modification, reinsurance issued
  and held cannot qualify, the entity's share of the change in fair value of underlying items goes
  to the CSM, and **changes from time value of money and financial risk go to the CSM under VFA but
  straight to insurance finance income or expense under GMM**, with VFA CSM adjustments at
  **current** rates versus GMM's **locked-in** rates, plus an optional risk mitigation election
  (¶¶2.60–2.71); **PAA** — optional, available if it reasonably approximates the GMM or coverage is
  one year or less, initial liability equals premium received, released over the coverage period by
  passage of time unless the risk-release pattern differs significantly, interest accreted only
  where there is a significant financing component, onerousness tested only on indicators, LIC
  measured on the GMM with a one-year discounting expedient (¶¶2.72–2.77); presentation — insurance
  revenue excluding investment components, insurance service expenses, insurance finance income or
  expenses, with a **per-portfolio** accounting policy choice to disaggregate insurance finance
  income/expense between P&L and OCI (¶¶2.26–2.29); transition — retrospective unless
  impracticable, then a free choice between the **modified retrospective approach** and the
  **fair value approach** (CSM = fair value of the group minus FCF at the transition date), chosen
  at group level (¶¶2.33–2.36); reinsurance held accounted for separately with a loss-recovery
  component (¶¶2.37–2.41). **The UKEB's own expectations for the UK market are stated in boxed
  text**: GMM for "life insurance (protection business), annuity contracts and longer-term general
  insurance"; **VFA for "unit-linked contracts and with-profits contracts"**; PAA for "short-term
  general insurance and short-term life contracts". Section 3 priority issue D verified:
  UK inherited estates are not addressed explicitly by IFRS 17; the fund's PPFM (and possibly the
  articles) governs attribution, "typically requiring 90% to be attributed to policyholders", with
  the same 90/10 split typically applying to the distributable estate; an emerging consensus
  requires a liability for the policyholders' share; the shareholders' share is the contested item;
  most UK with-profits funds are closed to new business; a fair value approach on transition is
  expected for a large part of UK with-profits business, and entities are expected to recognise an
  increase in equity on transition.
- **Products:** all seven (for IFRS reporters); WP and ULB carry the VFA marks; WP carries the
  inherited-estate issue.

#### R107. IFRS Foundation — *IFRS 17 Insurance Contracts* standard page (paywall record)
- **Publisher:** IFRS Foundation
- **URL:** https://www.ifrs.org/issued-standards/list-of-standards/ifrs-17-insurance-contracts/
- **Doc type:** standard-setter web page. **Accessed:** 2026-08-06.
- **fetched_ok:** **partial.** Direct HTML extraction returned only 41 characters ("Amendments to
  IFRS 17 Insurance Contracts") — the page is client-rendered. A second retrieval through a
  markdown-converting fetcher succeeded and is the basis of the annotation.
- **Annotation:** Recorded so that the library is explicit rather than silently paraphrasing.
  Verified: the page **does not provide the full text of IFRS 17 free of charge**; the standard
  text is available through the IFRS Digital subscription or the IFRS Foundation shop, and
  sign-in is required for some features. Free material offered on the page: an overview of key
  principles, standard history from IFRS 4 (2004) through IFRS 17 (2017) and the 2020 and 2024
  amendments, links to related projects, and pointers to implementation support material. **No
  IFRS 17 paragraph text was read from this source.** All IFRS 17 mechanics in this file come from
  R106; the adoption facts come from R38.
- **Products:** n/a (access record).

### D. Tax — the instruments that sit on top of FA 2012 [R17] and the LAM [R18]

#### R108. The Insurance Contracts (Tax) (Change in Accounting Standards) Regulations 2022 (SI 2022/1165)
- **Publisher:** legislation.gov.uk (HM Treasury statutory instrument)
- **URL:** https://www.legislation.gov.uk/uksi/2022/1165/made
- **Doc type:** statutory instrument. **Accessed:** 2026-08-06.
- **fetched_ok:** yes (regulations 1–8 read in full; regulations 9–12 read in part)
- **Annotation:** The IFRS 17 tax transitional regime. Verified: made under FA 2022; cited as the
  Insurance Contracts (Tax) (Change in Accounting Standards) Regulations 2022; **in force
  1 January 2023**, with effect for accounting periods beginning on or after that date (reg 1).
  Regulation 3 — on adopting IFRS 17 an insurance company carrying on long-term business computes
  **A − B**, where A is the accumulated profits less accumulated losses shown as a closing balance
  in the **first IFRS 17 balance sheet** (the pre-IFRS 17 balance sheet as restated in the first
  IFRS 17 accounts) and B the same quantity in the **pre-IFRS 17 balance sheet**, each subject to
  adjustments required or authorised by law in computing trade profits (reg 3(2)); amounts relating
  to IFRS 9 adoption, or not solely relating to IFRS 17, are excluded (reg 3(3)); the result is
  apportioned between long-term business and other business on the basis shown in the company's
  IFRS 17 disclosures, failing which on a just and reasonable basis (regs 3(4)–(5)); the amount
  allocated to long-term business is the **"transitional amount"** (reg 3(6)). Regulation 4 — where
  the company has both BLAGAB and non-BLAGAB long-term business, the transitional amount is
  allocated by an **acceptable commercial method** fairly representing each business's contribution
  to accounting profit or loss in the period ending immediately before the first IFRS 17 period,
  and that method must be consistent with the FA 2012 s.98 and s.115 methods for that period.
  Regulation 5 — a positive transitional amount is a **receipt**, a negative one an **expense**, of
  the long-term business, taken into account in computing BLAGAB trade profit or loss and non-BLAGAB
  long-term business profits. **Regulation 6 — the receipt or expense is treated as arising over
  10 years** beginning with the first day of the first IFRS 17 accounting period, apportioned to
  accounting periods in proportion to days. Regulations 7–8 — on an insurance business transfer
  scheme the unspread balance passes to a transferee within the charge to corporation tax (and not
  a mutual), with part-transfers split by an amount that "fairly represents" the attributable
  balance; otherwise the remaining balance crystallises in the transferor in the period of transfer.
  Regulation 12 (read through R18 LAM16060, not from the SI text) introduces a CTA09 s.320A-analogue
  bringing OCI amounts into account when an insurance contract is derecognised.
- **Products:** all (entity-level), for IFRS 17 adopters.

#### R109. The Finance Act 2022, Part 2 of Schedule 5 (Insurance Contracts: Change in Accounting Standards) (Commencement and Savings Provision) Regulations 2022 (SI 2022/1164 (C. 90))
- **Publisher:** legislation.gov.uk (HM Treasury statutory instrument)
- **URL:** https://www.legislation.gov.uk/uksi/2022/1164/made
- **Doc type:** commencement statutory instrument. **Accessed:** 2026-08-06.
- **fetched_ok:** yes (read in full — the instrument is two regulations plus an explanatory note)
- **Annotation:** The instrument that killed the seven-year tax spreading of acquisition expenses.
  Verified: made **9 November 2022** by two Lords Commissioners of HM Treasury under FA 2022
  Sch 5 paras 4 and 5. Regulation 2(1) — **Part 2 of Schedule 5 to the Finance Act 2022 comes into
  force on 1 January 2023 and has effect for accounting periods of companies beginning on or after
  that date.** Regulation 2(2) — paragraphs 2 and 3 of that Part **do not apply** to amounts of
  acquisition expenses adjusted under FA 2012 s.79 that are referable to an accounting period
  beginning before 1 January 2023 (the savings provision that keeps legacy 1/7ths running).
  Explanatory note: FA 2022 Sch 5 Part 2 amends CTA 2009 and FA 2012 "in connection with the
  adoption by insurance companies of International Accounting Standard 17".
- **Products:** BLAGAB writers — WOL, WP, ULB, and pre-2013 TA/CI/IP back-books.

#### R110. GOV.UK published tax rates — Corporation Tax and Income Tax
- **Publisher:** HM Government / HMRC (GOV.UK)
- **URLs:** https://www.gov.uk/corporation-tax-rates and https://www.gov.uk/income-tax-rates
- **Doc type:** government guidance pages. **Accessed:** 2026-08-06.
- **fetched_ok:** yes (both)
- **Annotation:** The two rates a UK life tax projection needs, taken from a citable source rather
  than memory, because the LAM's worked examples are stated at 2018 rates [R18 LAM01160].
  Verified at the access date: **Corporation Tax main rate 25%**, applying where profits exceed
  £250,000; **small profits rate 19%** where profits are £50,000 or less; Marginal Relief between
  £50,000 and £250,000; both thresholds proportionately reduced for short accounting periods and by
  the number of associated companies; a single rate applied from 1 April 2015 to 31 March 2023;
  separate ring-fence rates exist for oil and gas. **Income Tax basic rate 20%** on taxable income
  from £12,571 to £50,270 (personal allowance up to £12,570; higher rate 40% to £125,140;
  additional rate 45% above). The basic rate matters because FA 2012 s.102(3) sets the
  policyholders' rate by reference to the basic rate applying in England, Wales and Northern
  Ireland — expressly **not** the Scottish basic rate [R18 LAM06010]. The gov.uk income-tax page
  does not state the tax year on the extracted text; treat "20%" as the rate published at the
  access date, not as a rate verified for a named tax year.
- **Products:** all.

### E. Where tax meets the Solvency UK balance sheet (read for the tax interface only)

#### R111. PRA Rulebook — **Valuation Part**, Chapter 11 (Deferred Taxes), as at 05/08/2026
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.prarulebook.co.uk/pra-rules/valuation/05-08-2026
- **Doc type:** rulebook part (as-at view). **Accessed:** 2026-08-06.
- **fetched_ok:** yes (browser User-Agent required; 130,226 bytes → 20,494 chars; Chapters 1–12
  read)
- **Annotation:** Cross-stream note: stream 1 owns this Part. Read here only for the deferred-tax
  chapter and the two general valuation rules that frame it. Verified: **Valuation 2.1** — a firm
  must value assets at the amount for which they could be exchanged, and liabilities at the amount
  for which they could be transferred or settled, between knowledgeable willing parties in an
  arm's length transaction [Art. 75(1) SII], with **2.2** prohibiting any own-credit-standing
  adjustment; **3.1** going-concern assumption; **4.1** — Chapters 5 to 12 apply to recognition and
  valuation of assets and liabilities **other than technical provisions**. **Valuation 11.1** — a
  firm must recognise and value deferred taxes in relation to **all** assets and liabilities,
  including technical provisions, that are recognised for solvency or tax purposes.
  **Valuation 11.2** — deferred taxes other than DTAs from carried-forward unused tax credits and
  losses must be valued **on the basis of the difference between the values ascribed to assets and
  liabilities under the Valuation Part (and, for technical provisions, under the Technical
  Provisions Part, Matching Adjustment Part, Conditions Governing Business Part and SCR – General
  Provisions Part) and the values ascribed for tax purposes**. **Valuation 11.3** — a positive
  value may be ascribed to a DTA only where it is probable that future taxable profit will be
  available against which it can be used, taking account of legal or regulatory carry-forward time
  limits. All three rules carry a 31/12/2024 date stamp. Chapters 10.1–10.2 (financial liabilities
  at initial recognition with no subsequent own-credit adjustment; contingent liabilities at
  expected present value discounted at the basic risk-free curve) were also read.
- **Products:** all.

#### R112. PRA Rulebook — **Solvency Capital Requirement – Standard Formula Part**, Chapter 6 (Adjustment for Loss-Absorbing Capacity of Technical Provisions and Deferred Taxes), as at 05/08/2026
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.prarulebook.co.uk/pra-rules/solvency-capital-requirement---standard-formula/05-08-2026
- **Doc type:** rulebook part (as-at view). **Accessed:** 2026-08-06.
- **fetched_ok:** yes (browser User-Agent required; 1,673,565 bytes → 426,846 chars; Chapter 6
  read in full, remainder searched only)
- **Annotation:** Cross-stream note: stream 2 owns this Part. Read here only for Chapter 6, which
  is the tax adjustment to the SCR. Verified: **SCR-SF 6.1** — the adjustment must reflect
  potential compensation of unexpected losses through a simultaneous decrease in technical
  provisions or deferred taxes or both, take account of the risk-mitigating effect of future
  discretionary benefits, and equal the sum of the TP adjustment under 6.3 and the deferred-tax
  adjustment under 6.4 (and 6.5 if applicable) [Art. 108 SII]. **6.2** — the FDB risk-mitigating
  effect counts only to the extent the firm can establish that a reduction in future discretionary
  benefits may be used to cover unexpected losses, is capped at the sum of technical provisions and
  deferred taxes relating to those FDB, and is measured by comparing FDB under adverse conditions
  with FDB under the best-estimate assumptions. **6.3(1)** — the TP adjustment is
  `Adj_TP = -max(min(BSCR - nBSCR; FDB); 0)`, where BSCR is the basic SCR, nBSCR the net basic SCR
  and FDB the technical provisions without risk margin in respect of future discretionary benefits.
  **6.4(1)** — the deferred-tax adjustment (LACDT) equals the change in the value of the firm's
  deferred taxes resulting from an **instantaneous loss equal to the sum of (a) the basic SCR,
  (b) the 6.3 TP adjustment and (c) the operational risk capital requirement**; 6.4(2) deferred
  taxes valued under Valuation 11.1 and 11.2 [R111]; **6.4(3) an increase in DTAs arising from that
  loss must not be used** unless 6.5 applies; 6.4(4) future management actions may be assumed
  subject to Technical Provisions – Further Requirements 8; 6.4(5) a decrease in DTLs or an
  increase in DTAs gives a **negative** adjustment; 6.4(6) a positive change of deferred taxes
  gives a nil adjustment; 6.4(7) where the loss must be allocated to causes, allocation follows the
  contribution of standard formula modules and sub-modules to the basic SCR, with a partial-internal-
  model carve-out. **6.5** — a transitional permission, **ending 30 December 2025**, to utilise an
  increase in DTAs subject to probable future taxable profit, documentary evidence, advance written
  notice to the PRA, and constraints including: no new business sales beyond the business plan; no
  new business after the planning horizon, which must not exceed **five years**; investment returns
  after the loss assumed equal to forward rates implied by the risk-free curve unless higher returns
  can be demonstrated; increasing haircuts on profits projected beyond the planning horizon; and no
  assumptions more favourable than those used under Valuation 11. All rules date-stamped
  31/12/2024 except 6.2 (01/01/2016).
- **Products:** all; the TP leg of the adjustment (6.2, 6.3) bites principally on WP through FDB.

#### R113. Letter from the Department for Business, Energy and Industrial Strategy to the FRC — Solvency II clarification (3 February 2017)
- **Publisher:** BEIS (published by the FRC)
- **URL:** https://www.frc.org.uk/documents/5738/BEIS_letter_to_FRC_Solvency_II_clarification_February_2017.pdf
- **Doc type:** government letter. **Accessed:** 2026-08-06.
- **fetched_ok:** yes (PDF, 100,371 bytes → 2,407 chars; one page, read in full)
- **Annotation:** A short but decisive document on whether Solvency II drives the accounts, **and
  the one place in this stream where two retrieved sources are in tension**. Verified: Debbie
  Gillatt (Director, Business Frameworks, BEIS) wrote to Stephen Haddrill (CEO, FRC) on
  3 February 2017 in response to an FRC query. The letter records that Schedule 3 Part 2 Section E
  paragraph 52 then required the long-term business provision computation to be made annually by a
  Fellow of the IFoA on the basis of recognised actuarial methods and with "due regard to the
  actuarial principles laid down in Directive 2009/138/EC … (Solvency II)", a reference inserted
  when the Regulations were updated to transpose the Solvency 2 Regulations in 2015. BEIS states
  that this reference "should not be interpreted to mean that insurance companies are now required
  to change their accounting basis to one consistent with Solvency II"; "due regard" only requires
  preparers to consider the Solvency II actuarial requirements **if that Directive is relevant to
  the accounting basis applied**; and "Insurance providers that do not report under IFRS should
  continue to use the relevant UK accounting standard." **Tension to record, not resolve:** the
  Schedule 3 text retrieved on 2026-08-06 [R105] **no longer contains the Solvency II reference** —
  para 52(3) now reads "with due regard to generally accepted actuarial principles and on the basis
  of recognised actuarial methods", the inserted words and an omission both attributed to
  SI 2019/145 (as amended by SI 2020/523) with effect for financial years beginning on or after
  IP completion day. The letter therefore interprets a version of the law that has since been
  amended. Its *conclusion* — that UK GAAP preparers are not required to adopt a Solvency II
  accounting basis — is independently confirmed by FRS 103 BC45 [R99]; its *premise* is stale.
- **Products:** all, for Companies Act accounts preparers.

---

## Extracted mechanics

### 1. Three ledgers, three answers, one cash flow engine

A UK life insurer runs three simultaneous measurements of the same contracts. The projection
engine is common; the layers differ.

| Ledger | What it measures the liability at | Who mandates it | What it decides |
|---|---|---|---|
| **Statutory accounts** — Companies Act accounts (FRS 102 + FRS 103, or FRS 101) **or** IAS individual accounts (IFRS 17) | Grandfathered entity-specific basis with MSSB as the benchmark and a liability adequacy floor [R99 ¶¶2.3, 2.14, 3.11]; **or** fulfilment cash flows + CSM [R106 ¶2.19] | Companies Act 2006 s.395 [R103]; SI 2008/410 Sch 3 for the formats [R105]; FRC standards [R99][R102] | Reported profit; the accumulated-profits **cap** on distributions [R104 s.833A(3)]; the starting point for the tax trade-profit computation [R18 LAM01100] |
| **Solvency UK** | Best estimate + risk margin, market-consistent, discounted at PRA curves ± MA [R1][R2][R4] | PRA Rulebook | The SCR/MCR coverage position; and — for a Solvency-II-authorised long-term insurer — the **amount** of distributable profits via the A − L − D formula [R104 s.833A] |
| **Tax** | Not a liability measurement at all: the tax result is computed **from the accounts** with the FA 2012 overlay [R18 LAM01100] | Finance Act 2012 Part 2 [R17]; SI 2022/1164 [R109]; SI 2022/1165 [R108] | Corporation tax payable, split between shareholder rate and policyholder rate [R18 LAM06010] |

Two consequences a drafter must not blur:

- **"Statutory accounts" in the UK does not mean the regulatory return.** Since 1 January 2013,
  tax trade profits are based on **accounting** profits; before that date they were based on the
  insurance regulatory returns [R18 LAM01100]. The Solvency UK balance sheet is a *prudential*
  document, not the statutory accounts.
- **Solvency UK nonetheless owns the dividend.** s.833A CA 2006 substitutes the prudential
  balance sheet for the realised-profits test for Solvency-II-authorised long-term insurers
  [R104]. So an insurer can have accounting profit and no dividend capacity, or vice versa,
  subject to the s.833A(3) cap.

### 2. The UK GAAP measurement chassis: what FRS 103 actually fixes

FRS 103 fixes very little of the measurement and a great deal of the presentation.

**What it fixes (mandatory):**
- Scope: insurance contracts issued, reinsurance held, and other financial instruments issued with
  a DPF, for any entity applying FRS 102 (¶1.2) [R99]. FRS 102 ¶1.6 makes the referral mandatory
  and carves these contracts out of Sections 11, 12, 21, 22 and 23 [R102].
- **No provisions for possible future claims** under contracts not in existence at the reporting
  date (catastrophe and equalisation provisions), unless the regulatory framework requires them
  (¶2.13(a)) [R99].
- **Liability adequacy test** (¶¶2.14–2.18) — see §4 below.
- Extinguishment-only derecognition (¶2.13(c)); **no offsetting** of reinsurance assets against
  insurance liabilities or of reinsurance income/expense against insurance expense/income
  (¶2.13(d)); reinsurance asset impairment assessment (¶2.13(e)) [R99].
- All assets and liabilities arising from an insurance contract are treated as **monetary items**
  for FRS 102 Section 30 foreign currency purposes (¶2.26) [R99].
- Unbundling of deposit components: **required** where the deposit component can be measured
  separately *and* the accounting policies would not otherwise recognise all its rights and
  obligations; **permitted** where it can be measured separately but is fully recognised anyway;
  **prohibited** where it cannot be measured separately (¶2.23). On unbundling, FRS 103 applies to
  the insurance component and FRS 102 Section 11 or 12 (or IAS 39/IFRS 9 by policy choice) to the
  deposit component (¶2.25) [R99].
- Explicit and unreserved statement of compliance with FRS 103 in the notes, in addition to the
  FRS 102 compliance statement (¶1.12) [R99].

**What it leaves open (permissive):**
- **Continuation of existing practices** that could not be newly introduced: measuring insurance
  liabilities on an **undiscounted** basis unless the Regulations require otherwise; measuring
  contractual rights to future investment management fees above their fair value; non-uniform
  accounting policies across subsidiaries (¶2.6) [R99].
- **Prudence**: an insurer need not eliminate excessive prudence, but must not introduce
  additional prudence if it already measures with sufficient prudence (¶2.7) [R99].
- **Future investment margins**: need not be eliminated, but there is a **rebuttable presumption**
  that introducing them makes the statements less relevant and reliable, unless the margins affect
  contractual payments. Two named examples of policies reflecting such margins: an asset-return
  discount rate; and projecting asset returns at an estimated rate, discounting at a different rate
  and including the result in the liability (¶2.8). The presumption may be overcome only if other
  components of the change increase relevance and reliability enough to outweigh it — the worked
  illustration is a move from excessively prudent locked-in assumptions and a regulator-prescribed
  discount rate that ignores embedded options, to current estimates, a reasonable but not
  excessively prudent risk adjustment, intrinsic **and time** value of options and guarantees, and
  a current market discount rate (¶2.9). Where the discount rate determines the liability
  **directly** rather than only the emergence of a profit margin, overcoming the presumption is
  "highly unlikely" (¶2.10) [R99].
- **Current market interest rates**: an insurer may designate liabilities to be remeasured at
  current market interest rates with changes in profit or loss, without applying that policy to all
  similar liabilities, but must then apply it consistently in all periods until those liabilities
  are extinguished (¶2.5) [R99].
- **Shadow accounting** (¶2.11): unrealised gains/losses on assets may be permitted to affect the
  insurance liability, DAC or related intangible in the same way realised ones do, with the
  offsetting adjustment recognised in OCI if and only if the unrealised gains/losses are [R99].
- **Solvency-UK-based policies**: an entity setting policies for the first time may either take
  Section 3 as the benchmark (¶1.5(a)) or **establish policies based on the PRA Rulebook technical-
  provisions recognition and measurement rules**, with appropriate adjustments (¶1.5(b)); an
  existing entity may change towards greater consistency with those rules (¶2.3A) [R99]. BC55 lists
  what to consider adjusting: **(a) regulatory transitional adjustments; (b) the volatility
  adjustment; (c) the risk margin; (d) surplus funds where these reflect contractual obligations of
  cash flows to policyholders** [R99].
- Transition from IFRS: an insurer whose previous framework was adopted IFRS (or equivalent) must
  **disregard its existing insurance-contract policies** and apply FRS 103 as if setting policies for
  the first time (¶6.5) [R99].

**Valuation methods named in the glossary [R99]:**
- **Gross premium method** — full contractual premiums brought into account, with explicit cash flow
  estimates for premiums (adjusted for renewals and lapses), expected claims and, for with-profits,
  future *regular* but not occasional or terminal bonuses, costs of maintaining contracts, and future
  renewal expenses; cash flows discounted at the valuation interest rate, which is based on the
  expected return on the assets deemed to back the liabilities, adjusted for further risks. For
  linked business, allowance may be made for the purchase of future units required by the contract
  and credit taken for future permitted charges.
- **Net premium method** — the premium brought into account at any valuation date is that which, on
  the valuation assumptions for interest, mortality and disability, exactly provides for the
  guaranteed benefits; zillmerisation is a named variation; the detailed methodology is the PRA
  Rulebook **as at 31 December 2015**.
- **IG2.39: the gross premium method should be used for every class except those for which the net
  premium method is used in the related regulatory returns** [R100] — i.e. UK GAAP method selection
  historically tracked the pre-2016 regulatory return.

### 3. Acquisition costs and DAC — the U.S. contrast, reversed

**Company law is the binding constraint, not the standard.** SI 2008/410 Schedule 3 **para 13**:
costs of acquiring insurance policies incurred in a financial year but relating to a subsequent
financial year **must be deferred** in the manner specified in balance sheet note 17 [R105]. DAC
sits at assets item **G.II**, and its movement at technical account item **8(b) change in deferred
acquisition costs** [R105].

**Note 17 carve-outs** [R105]: DAC is excluded to the extent that the long-term business provision
(item C.2) or the linked provision (item D) already allows for the costs, either by **explicit
recognition** or by **implicit recognition** through anticipation of future income from which the
costs may prudently be expected to be recovered. Disclosure required: how the deferral has been
treated, and where the actuarial method makes explicit allowance, the amount so recognised. This
is the mechanism by which a UK zillmerised or gross-premium reserve absorbs acquisition costs
inside the liability instead of showing a separate asset — a modelling fork that must be an
explicit configuration choice.

**FRS 103 Section 3** [R99]:
- ¶3.7 — "Except as required by paragraph 3.10, acquisition costs **shall be deferred** except to
  the extent that: (a) the costs have already been recovered (for example where the policy design
  provides for recovery as incurred); (b) the net present value of margins within the insurance
  contracts is not expected to be sufficient to cover DAC after providing for contractual
  liabilities to policyholders and expenses; and (c) the receipt of future premiums or the
  achievement of future margins is insufficiently certain based on estimates of future expected
  discontinuance rates or other experience."
- ¶3.8 — advertising costs shall not be deferred unless directly attributable to acquiring new
  business.
- ¶3.9 — DAC carried forward shall be amortised over a period **no longer than one in which, net of
  any related deferred tax provision, they are expected to be recoverable out of margins on related
  insurance contracts in force at the reporting date, and in a similar profile to those margins.**
  There is no prescribed amortisation basis; the profile follows the margin profile.
- ¶3.10 — **"Acquisition costs shall not be deferred for with-profits funds."**

**Scope trap on ¶3.10.** Section 3.1(a) applies ¶¶3.3–3.9 and 3.16–3.18 to **all** long-term
insurance business; Section 3.1(b) applies **¶¶3.10–3.15** only to with-profits business and
with-profits funds "to which the Prudential Regulation Authority (PRA) **realistic capital regime**
(as set out in section 1.3 of INSPRU as at 31 December 2015) was being applied, either voluntarily
or compulsorily, **prior to 1 January 2016**" [R99]. IG1.1 then says an entity **may, but is not
required to,** adopt ¶3.12 for UK with-profits business outside that scope, and may change policy
only under ¶2.3 [R100]. So a with-profits fund that was never in the realistic regime is **not**
caught by the ¶3.10 DAC prohibition by its own terms, even though ¶3.7 opens with "Except as
required by paragraph 3.10". Record this as an ambiguity; do not assert a resolution.

**Glossary definition of DAC for long-term business** [R99]: costs arising from the conclusion of
insurance contracts relating to contracts in force at the reporting date "in the expectation that
they will be recoverable out of future margins within insurance contracts after providing for
contractual liabilities". **Acquisition costs** are defined as costs arising from the conclusion of
insurance contracts including direct costs and indirect costs connected with processing proposals
and issuing policies, with further detail in Schedule 3 Notes on the P&L format note 6.

**Contrast to carry into the deliverable.** For the same product cash flows:
- U.S. statutory: acquisition costs expensed as incurred, no DAC asset, year-1 statutory strain.
- **UK Companies Act accounts: acquisition costs deferred (required by Sch 3 para 13), amortised in
  the margin profile, no year-1 strain of the U.S. kind — except in a with-profits fund within the
  ¶3.1(b) scope, where deferral is prohibited and the strain reappears inside the fund** [R105][R99].
- **IFRS 17: no DAC asset either, but for the opposite reason** — acquisition cash flows are inside
  the fulfilment cash flows and **reduce the CSM at initial recognition**, so they emerge as reduced
  revenue over the coverage period rather than as a deferred asset. The premium element intended to
  cover them is added back to insurance revenue with an equal insurance service expense over the
  same period [R106 ¶¶2.56–2.59]. Under PAA, acquisition cash flows may be expensed immediately if
  coverage is one year or less [R106 ¶2.76].
- **Solvency UK: no DAC at all**; acquisition expenses are simply projected cash outflows inside the
  best estimate [R1].

### 4. The liability adequacy test (the only UK GAAP measurement floor)

FRS 103 ¶2.14 [R99]: at the end of each reporting period an insurer shall assess whether its
recognised insurance liabilities are adequate **using current estimates of future cash flows**. If
the carrying amount of insurance liabilities **less related DAC and related intangibles** is
inadequate in light of those cash flows, **the entire deficiency shall be recognised in profit or
loss**.

¶2.15 — if the insurer's own test meets the minimum requirements, FRS 103 imposes nothing further.
The minimum requirements are: (a) the test considers current estimates of **all** contractual cash
flows and related cash flows such as claims handling costs, **as well as cash flows resulting from
embedded options and guarantees**; and (b) if the liability is inadequate, the entire deficiency is
recognised in profit or loss.

¶2.16 — if the policies do not require a test meeting those minimums, the insurer must determine the
carrying amount of the relevant insurance liabilities less related DAC and related intangibles
(related reinsurance assets are **not** considered) and compare it to the required alternative
measurement. (The tail of ¶2.16 and ¶¶2.17–2.18 were read only in part; see gaps.)

**Modelling consequence.** The LAT is the point at which a UK GAAP model must run a *current-
assumption, option-and-guarantee-inclusive* projection even if the recognised liability is a
locked-in net-premium reserve. It is the UK GAAP analogue of a gross premium valuation floor, and
it is the mechanism through which adverse experience first hits UK GAAP profit — including by
writing off DAC.

### 5. With-profits under UK GAAP: MSSB, realistic liabilities and the FFA

**MSSB (modified statutory solvency basis)** — glossary [R99]: the statutory solvency basis adjusted
(a) to **defer new business acquisition costs** where the benefit will be obtained in subsequent
reporting periods, and (b) to treat investment, resilience and similar reserves, or reserves held
for general contingencies or the specific contingency that the fund will close to new business, as
**reserves rather than provisions** — included as appropriate within shareholders' capital and
reserves or within the FFA. ¶3.11 states MSSB is "the established accounting treatment for long-term
insurance business" and that FRS 103 requires **with-profits funds** to use the **realistic value of
liabilities** instead.

**Realistic value of liabilities** — glossary [R99]: that element of the amount defined by **rule
1.3.40 of INSPRU as at 31 December 2015**, excluding current liabilities within rule 1.3.190 of
INSPRU as at 31 December 2015 that are recognised separately in the statement of financial position.
The FRC deliberately retained the INSPRU-anchored definitions rather than moving to principles-based
ones, because "in practical terms entities would need to refer to INSPRU as at 31 December 2015 in
order to continue with their existing accounting policies", and the PRA Rulebook can be accessed
"as at" a date [R99 BC49–BC50].

**¶3.12 — the with-profits adjustments** [R99]:
- (a) liabilities to policyholders from with-profits business at the **realistic value of
  liabilities adjusted to exclude the shareholders' share of projected future bonuses**;
- (b) reinsurance recoveries measured consistently with the policyholder liabilities they relate to;
- (c) an amount **may** be recognised for the **present value of future profits on non-participating
  business written in a with-profits fund** if the realistic liability determination takes account
  of that value, directly or indirectly;
- (d) where the fund has an interest in a subsidiary or associate and the realistic liability takes
  account of that interest above the net amounts in the consolidated accounts, the excess may be
  recognised;
- (e) consequential tax effects of (a)–(d) shall be reflected.
- **The adjustments from MSSB, including any (c) or (d) recognition, are included in profit or loss;
  an equal and opposite net amount is transferred to or from the FFA and also included in profit or
  loss.**

**¶3.13** — for a **mutual**, the ¶3.12 adjustments are offset within profit or loss by a transfer to
or from the FFA or retained surplus account, "with the result that overall profit or loss for the
year will be unchanged" [R99]. **IG1.10** generalises: because the realistic-versus-MSSB difference
goes to the FFA, "there will generally be no change in the profit for the reporting period **except
where the adjustments result in a negative balance on the FFA** and the entity determines that this
negative balance should result in a deduction from equity through profit or loss" [R100].

**¶3.14** — the realistic value of liabilities shall exclude the shareholders' share of future
bonuses, with similar adjustment for other amounts otherwise due to shareholders [R99].

**IG1.2 — how to compute the shareholders' share** [R100]: the value of future transfers to
shareholders calculated using **market-consistent financial assumptions**, assuming transfers take
place at a level consistent with the assumptions used for the realistic value of liabilities. Where
no explicit assumption is needed, assume continuation of current profit-sharing arrangements unless
the firm plans to change them. Non-economic projection assumptions must be consistent with those
used for the realistic value of liabilities. The deducted amount goes to the **FFA, together with
any related tax liability**.

**IG1.6–IG1.7 — the VIF on non-participating business in a with-profits fund** [R100]: determined as
the discounted value of future profits from the policies, taking the related liabilities at the
**statutory solvency basis including MSSB adjustments** (for example excluding additional reserves
carried for solvency, or where future income in the VIF covers DAC on the balance sheet), with a
corresponding adjustment to the in-force value for consistency. **Any release of capital
requirements must be stripped out of the VIF asset**, because MSSB liabilities include no allowance
for capital.

**FFA** — Schedule 3 note 19 [R105]: "all funds the allocation of which either to policyholders or
to shareholders has not been determined by the end of the financial year"; transfers shown at P&L
item II.12a. FRS 103 ¶5.4: the FFA must be disclosed **separately** in the statement of financial
position and not combined with technical provisions or other liabilities, and entities consolidating
interests on a combined basis must show the elements separately [R99]. ¶5.5: a negative FFA balance
requires a note explaining its nature, how it arose, and why no eliminating action was considered
necessary [R99]. IG2.50: an FFA is inappropriate where allocation is reasonably certain; it is
appropriate for proprietary and mutual long-term funds where the allocation between equity/disclosed
surplus and policyholder liabilities "is not clear cut" [R100].

**¶5.3 — presentation of the ¶3.12(c)/(d) amounts** [R99]: apportioned as a deduction in arriving at
liabilities to policyholders and at the FFA where apportionment is possible; as a single deduction
from the sub-total where it is not; and **as an asset** where neither presentation complies with the
statutory balance sheet requirements applying to the entity.

**Options and guarantees** [R100]: IG1.11 — entities with with-profits business within the ¶3.1(b)
scope are **required** to measure the option and guarantee liability either at fair value or by a
market-consistent stochastic model. IG1.12 — for all long-term business the best basis includes the
**time value**; "any deterministic approach … will generally fail to deal appropriately with the
time value of the option", so stochastic techniques should be used unless a market value is
available; entities outside the ¶3.1(b) scope are encouraged but not required, with additional
disclosure (IG3.14(c)) where options are not valued this way. IG1.13 — the stochastic valuation must
take into account, scenario by scenario, **management actions** anticipated in response to market
variables (rebalancing between debt and equity, varying policyholder charges, varying bonus policy)
that affect the amount payable, which must be realistically implementable within the scenario's
timescale and **consistent with the published PPFM** [R100] (see COBS 20, [R9]).

**Other with-profits routing rules** [R99]: ¶2.32 — exchange differences on long-term insurance
business go through the **technical account for long-term business**, not the non-technical account,
and where appropriate may be recognised in the FFA. ¶2.34 — the remeasurement of a net defined
benefit liability not attributable to owners is treated as an amount whose allocation between
policyholders and owners is undetermined, shown as a separate line in the long-term technical
account immediately above the FFA transfer line and reflected in that transfer, with separate note
disclosure.

**DPF classification** [R99 ¶2.30]: the issuer may but need not recognise the guaranteed element
separately from the DPF; if not separated, the whole contract is a liability; if separated, the
guaranteed element is a liability and the DPF is classified as either a liability or **a separate
component of equity where the Regulations permit**, possibly split, with a consistent policy — never
an intermediate category. Premiums may be recognised as revenue in full; where part of the DPF is in
equity, the attributable portion of profit or loss is an **allocation** of profit or loss, not
income or expense. ¶2.31 extends this to investment contracts with a DPF, with a floor: where part
or all of the feature is in equity, the recognised liability must not be less than the amount from
applying IAS 39/IFRS 9/FRS 102 Sections 11–12 to the guaranteed element, including the intrinsic
value of a surrender option (time value need not be included if ¶2.22 exempts it).

### 6. Linked business under UK GAAP

**Definition** [R99 glossary]: long-term insurance business where benefits payable are wholly or
partly determined by reference to the value of, or income from, property of any description, or by
reference to fluctuations in or in an index of the value of property of any description.

**Balance sheet** [R105 note 26]: liabilities item **D Technical provisions for linked liabilities**
covers provisions constituted to cover liabilities relating to investment under long-term policies
whose benefits are so determined. **Any additional technical provisions constituted to cover death
risks, operating expenses or other risks (such as benefits payable at maturity or guaranteed
surrender values) must be included under item C.2**, the long-term business provision. A unit-linked
bond model therefore needs a **two-part liability output**: unit reserve (item D) and non-unit
reserve (item C.2).

**Floors and mismatching** [R100]: IG2.47 — the relevant provision for any contract should not be
less than the element of any surrender or transfer value calculated by reference to the relevant
fund(s) or index. IG2.48 — net assets held to cover linked liabilities may differ from the technical
provisions for linked liabilities, and the reasons for any significant mismatching should be
disclosed. IG2.49 — where the linked provision has regard to the timing of the tax obligation, that
effect must be **excluded from the determination of deferred tax**. IG2.41 — no policy may have an
overall negative provision except as allowed by PRA rules, nor a provision less than any guaranteed
surrender or transfer value.

**Premium recognition for linked business** [R99 ¶3.3]: premiums are recognised when due for payment;
"For linked business the due date for payment may be taken as the date when the liability is
established."

**Investment contracts** [R18 LAM01100]: HMRC records that "certain policies, such as unit-linked
bonds, are not regarded as insurance for accounts purposes; these are treated as 'investment
contracts' with premiums from customers generally held on balance sheet as policyholder deposits and
only the fees charged within the policy treated as income." Under FRS 103's glossary an investment
contract is a contract with the legal form of insurance that does not expose the insurer to
significant insurance risk. Such contracts fall **outside** FRS 103 and into FRS 102 Sections 11/12
(and Section 23 for the service element) — so a unit-linked bond's accounts signature is a
**deposit-plus-fee-income** signature, not a premium-and-claims signature. IG1.8 confirms that the
profit recognition profile for non-participating contracts failing the insurance-contract definition
or lacking a DPF is determined by FRS 102 Sections 11, 12 and 23 [R100].

### 7. Premium, claim and bonus recognition under UK GAAP

[R99 ¶¶3.3–3.6]:
- **Premiums**, including inwards reinsurance, recognised **when due for payment**; estimates used
  where the amount due is unknown (the standard names "certain pensions business"); for linked
  business the due date may be taken as the date the liability is established.
- **Outward reinsurance premiums** recognised **when paid or payable**.
- **Maturity claims** recognised when due for payment; **death claims recognised on notification**;
  instalment claims where the policy remains in force recognised when each instalment falls due.
  Claim recognition in the technical account and the calculation of the long-term business provision
  and/or linked provision must be treated **consistently**.
- **Surrenders** included within claims incurred and recognised either when paid, or at the earlier
  date on which, following notification, the policy ceases to be included in the long-term business
  provision and/or the linked provision.

**Bonuses** [R100 IG2.38 area]: bonuses and rebates attributable to the period, other than those
included within claims payable, should be included in technical account line II.6(a) (change in the
long-term business provision) and in balance sheet liabilities item C.2 — the Schedule 3 line
II.7 "Bonuses and rebates, net of reinsurance" **should not be used** for long-term business.
IG2.40: where the valuation is on a net premium method, bonuses go into the long-term business
provision only if **vested or declared as a result of the current valuation**. IG2.45: for each
significant class of with-profits business the insurer should disclose the extent to which the
long-term business provision allows for future bonuses — for example that explicit provision is made
only for vested bonuses and none for future regular or terminal bonuses — and, where allowance is
implicit through a discount-rate adjustment or otherwise, state that fact with a broad description.
IG2.46: the aggregate bonuses added to policies in the period must be disclosed.

### 8. IFRS 17 — the general measurement model (GMM)

All from [R106] unless noted; IFRS 17 paragraph numbers are those the UKEB quotes.

**Aggregation** (¶¶2.14–2.17): identify **portfolios** — "contracts subject to similar risks and
managed together" [IFRS 17:14]. Divide each portfolio into at least three groups: onerous at initial
recognition; no significant possibility of becoming onerous subsequently; the remainder. **Annual
cohorts**: contracts issued more than one year apart may not be in the same group. Groups are
established at initial recognition and **never reassessed**.

**Initial measurement** (¶2.43): a group is measured at the **fulfilment cash flows** plus the
**contractual service margin**, where the FCF comprise (i) the present value of probability-weighted
expected cash flows, reflecting financial risk, and (ii) an **explicit risk adjustment for
non-financial risk**.

**Cash flow estimates** (¶2.44): all cash flows within the contract boundary; incorporate in an
unbiased way all reasonable and supportable information available without undue cost or effort about
amount, timing and uncertainty; reflect the entity's perspective, provided relevant market variables
are consistent with observable market prices; be current and explicit.

**Contract boundary** [IFRS 17:34] (¶2.45): cash flows are within the boundary "if they arise from
substantive rights and obligations that exist during the reporting period in which the entity can
compel the policyholder to pay the premiums or in which the entity has a substantive obligation to
provide the policyholder with insurance contract services."

**Discount rates** [IFRS 17:36] (¶2.46), quoted: the rates shall "(a) reflect the time value of
money, the characteristics of the cash flows and the liquidity characteristics of the insurance
contracts; (b) be consistent with observable current market prices (if any) for financial instruments
with cash flows whose characteristics are consistent with those of the insurance contracts, in terms
of, for example, timing, currency and liquidity; and (c) exclude the effect of factors that
influence such observable market prices but do not affect the future cash flows of the insurance
contracts." **IFRS 17 does not prescribe specific rates** — only these principles. Contrast: the
Solvency UK best estimate is discounted at a PRA-published curve, optionally plus MA [R1][R2].

**Risk adjustment for non-financial risk** [IFRS 17 Appendix A] (¶2.48), quoted: "the compensation
an entity requires for bearing the uncertainty about the amount and timing of the cash flows that
arises from non-financial risk as the entity fulfils insurance contracts." **No confidence level is
prescribed** in the material retrieved; contrast the Solvency UK risk margin, which is a
cost-of-capital calculation at a fixed 4% rate with lambda tapering [R4].

**CSM at initial recognition** (¶2.50): a **residual**, measured so that no income or expense arises
on initial recognition. **For a group onerous at initial recognition, a loss is recognised in profit
or loss immediately and the CSM is zero.**

**Subsequent measurement** [IFRS 17:40] (¶2.51): carrying amount = **liability for remaining
coverage** (FCF related to future service + CSM) + **liability for incurred claims** (FCF related to
past service). Changes are recognised in profit or loss split between insurance revenue, insurance
service expenses and insurance finance income or expenses (¶2.52).

**CSM release** (¶¶2.53–2.55): each period an entity recognises as insurance revenue the amount of
CSM representing services provided in that period, determined by identifying **coverage units** that
reflect the **quantity of benefits provided** under the contracts and their **expected coverage
period**. The residual CSM represents profit relating to future service.

**Insurance contract services** [IFRS 17 Appendix A] (¶2.22): insurance coverage; **investment-return
service** for contracts without direct participation features; **investment-related service** for
contracts with direct participation features. Claims and expenses other than insurance acquisition
expenses are recognised **when incurred** (¶2.23).

**UKEB's UK expectation:** GMM for life protection business, annuity contracts and longer-term
general insurance (boxed text after ¶2.55) [R106].

### 9. IFRS 17 — the variable fee approach (VFA)

[R106 ¶¶2.60–2.71]:
- Applies to **insurance contracts with direct participation features** — [IFRS 17:B101]
  "insurance contracts that are substantially investment-related service contracts under which an
  entity promises an investment return based on underlying items."
- The qualifying conditions ensure the entity's obligation is the **net of** (a) an obligation to pay
  the policyholder an amount equal to the **fair value of the underlying items** and (b) a
  **variable fee for future services**.
- The **variable fee** = the entity's share of the fair value of the underlying items, **less**
  fulfilment cash flows that do not vary based on the returns on underlying items.
- Eligibility is assessed **at inception and never reassessed** unless the contract is modified.
- **Reinsurance issued and reinsurance held can never qualify** for the VFA.
- Mechanically the VFA is the GMM except for **subsequent CSM measurement**: the entity's share of
  the change in fair value of the underlying items is treated as relating to future service and goes
  **into the CSM**, released over time as services are provided.
- **The primary difference from the GMM is the treatment of changes in FCF arising from the time
  value of money and financial risk**: under VFA these are part of the variability of the fee for
  future service and go to the CSM (then to insurance revenue as the CSM releases); under GMM they
  go **immediately** to insurance finance income or expense.
- **VFA CSM adjustments use current discount rates**; **GMM CSM adjustments use locked-in rates**.
- **Risk mitigation option**: subject to criteria, a VFA entity may (not must) present in profit or
  loss the income and expenses arising from financial risk on both the insurance contracts and the
  related risk-mitigation arrangements, reducing accounting mismatches.

**UKEB's UK expectation** (boxed text after ¶2.71): "In the UK, the VFA is expected to be applied to
insurance contracts such as **unit-linked contracts and with-profits contracts**." This is the
single most important product-mapping fact in the IFRS 17 material for this library.

### 10. IFRS 17 — the premium allocation approach (PAA)

[R106 ¶¶2.72–2.77]: **optional**; available only if at inception of the group either the PAA
reasonably approximates the GMM, **or** the coverage period of each contract in the group is one year
or less. Initial liability = **premium received**, with no explicit identification of cash flow
estimates, time value or risk effects unless the group is onerous. The liability for remaining
coverage is released over the coverage period on the basis of **passage of time**, unless the
expected pattern of release from risk differs significantly, in which case on the expected timing of
incurred claims and benefits. Interest is accreted only where there is a significant financing
component. Onerousness is assessed only when facts and circumstances indicate. Acquisition cash flows
may be expensed immediately if coverage is no more than one year, or allocated as under GMM. The
liability for incurred claims uses the GMM, with a practical expedient allowing no discounting where
cash flows are expected within one year of the claim being incurred.

**UKEB's UK expectation** (boxed text after ¶2.77): PAA for short-term general insurance and
short-term life contracts; the PAA is similar to current UK IFRS 4 practice for general insurance.

### 11. IFRS 17 — presentation, OCI option, acquisition cash flows and transition

**Presentation** [R106 ¶¶2.26–2.29, 2.78]: present separately **insurance revenue** (excluding
receipt of any investment component), **insurance service expenses** (excluding repayment of
investment components), and **insurance finance income or expenses**. An **investment component** is
defined as amounts the contract requires the entity to repay to a policyholder in all circumstances,
regardless of whether an insured event occurs. **Accounting policy choice per portfolio**: insurance
finance income or expenses either all in profit or loss, or **disaggregated between profit or loss
and OCI**. Statement of financial position: insurance contract assets, insurance contract
liabilities, reinsurance contract assets, reinsurance contract liabilities, presented separately for
asset and liability positions.

**Acquisition cash flows** [R106 ¶¶2.56–2.59]: costs of selling, underwriting and starting a group,
directly related to the portfolio; an allocation is within the contract boundary and inside the
estimate of future cash flows. Cash flows paid **before** the group is recognised are an **asset**,
then derecognised and subsumed into the CSM at initial recognition; an asset continues for groups
expected to arise from **renewals**. The standard's approach **reduces the CSM at initial
recognition**, so acquisition expenses emerge as a reduction in revenue as the CSM releases; the
premium element intended to recover them is added back to insurance revenue over the coverage period
with an equal insurance service expense. Recoverability of the acquisition cash flow asset must be
assessed each reporting period on impairment indicators.

**Transition** [R106 ¶¶2.33–2.36]: **retrospective unless impracticable**; if impracticable for a
group, a **free choice** between the **modified retrospective approach** (specified modifications
permitting determination of specified matters at the transition date rather than initial recognition,
with specified proxies) and the **fair value approach** (CSM — or loss component for an onerous group
— = fair value of the group minus the fulfilment cash flows at the transition date). The choice is
made **at group level**.

**Reinsurance held** [R106 ¶¶2.37–2.41]: accounted for **separately** from the underlying contracts.
On initial recognition of onerous underlying contracts, if the reinsurance was entered into before or
at the same time, the corresponding **loss recoveries** are recognised in profit or loss at the same
time; the adjusted net gain or cost of purchasing the reinsurance is then recognised over the
reinsurance coverage period. Reinsurance **issued** is measured under GMM or PAA like any other
issued contract. [R18 LAM16060] adds the UK tax observation that the pre-IFRS 17 "mirroring approach"
common in practice is replaced by standalone accounting, and that HMRC introduced no special tax rule
for the change.

**Modification and derecognition** [R106 ¶¶2.24–2.25]: derecognition when and only when the contract
is extinguished or is modified in a way specified in IFRS 17:74. IFRS 17:72 modifications that force
derecognition and recognition of a new contract include a modification taking the contract outside
IFRS 17's scope, causing it to fail the direct-participation definition, or causing it to fail PAA
eligibility. Other modifications are changes in estimates of cash flows [IFRS 17:73].

### 12. IFRS 17 and UK with-profits: the inherited estate

[R106 §3, priority issue D]:
- An **inherited estate** is assets built up in a with-profits fund over time and not paid out to
  policyholders, surplus to current contractual obligations, usable at management's discretion to
  enhance current and/or future policyholders' benefits. The sources are typically unknown — seed
  capital, retained capital, historic decisions not to distribute, and investment return on those.
- Allocation is governed by the fund's **PPFM** and possibly the articles of association and other
  governance sources, "typically requiring **90%** to be attributed to policyholders" (¶3.138). The
  same 90/10 split typically applies to the estate to the extent available for distribution and not
  needed to support current and expected future business. Shareholder surplus is not accessible
  except through declared policyholder bonuses or a **court-approved attribution exercise** (¶3.139).
- **Most UK with-profits funds are now closed to new business** (¶3.140); some closed funds,
  particularly demutualisation legacies, allow no profits to shareholders at all.
- **IFRS 17 does not explicitly address inherited estates** (¶3.141). Application requires judgement
  on the division of the estate between shareholders and policyholders — between equity and
  liabilities — both on transition and on subsequent measurement (¶3.141). There is an emerging
  consensus that a **liability** must be recognised for the policyholders' share; the shareholders'
  share is the contested item (¶3.143). Stakeholders' concern is that profit may be recognised before
  shareholders are unconditionally entitled to it (¶3.144).
- **On transition**, a fully retrospective approach is expected to be impracticable and a **fair
  value approach** is expected for a large part of this business; the analysis between CSM and equity
  is a matter of judgement, and entities are expected to **recognise an increase in equity on
  transition** (¶¶3.155–3.157, read in outline).
- Whether inherited estate assets are **"underlying items"** for VFA purposes is itself an open
  question in the assessment (¶3.161, read in outline).

**Contrast with UK GAAP.** Under FRS 103 the undetermined surplus sits in the **FFA**, a
balance-sheet item that is neither policyholder liability nor equity, and the realistic-versus-MSSB
adjustment is routed through it so that profit is generally unaffected [R99 ¶¶3.12–3.13][R100 IG1.10].
Under IFRS 17 there is no FFA: the estate must be split between liability and equity, and that split
changes reported profit and equity. HMRC records the parallel: UK GAAP has an FFA, IFRS may instead
show an "Unallocated Divisible Surplus" (UDS) [R18 LAM01100]. This is the sharpest UK GAAP / IFRS 17
divergence for the with-profits product.

### 13. Distributable profits — the decision the accounts do *not* drive

Order of operations for a UK life insurer [R104]:

1. **s.830(1)–(2)**: distributions only out of accumulated realised profits less accumulated realised
   losses.
2. **s.830(3)** makes that subject to **s.833A** for Solvency 2 insurance companies.
3. **s.833A** applies to any authorised insurance company carrying on long-term business authorised
   under Article 14 of the Solvency 2 Directive. For s.830(2) purposes its realised profit or loss is
   **A − L − D** at the balance sheet date:
   - **A** = total value of the company's assets
   - **L** = total value of the company's liabilities
   - **D** = the sum of: excess of the value of shares in a qualifying investment subsidiary over the
     consideration given for them; any asset representing a **defined benefit pension scheme
     surplus**; the excess of **ring-fenced fund** assets over ring-fenced fund liabilities; deferred
     tax liabilities relating to any of those three; where the firm has a **matching adjustment**
     permission, the excess of the assigned asset portfolio value over the value of the MA
     obligations; and paid-in ordinary share capital plus related share premium, paid-in preference
     shares that are not liabilities plus related share premium, capital redemption reserve, and any
     other reserve the company is prohibited from distributing. An item falling in more than one
     paragraph is counted once (s.833A(6)).
   - Positive = realised profit; negative = realised loss.
4. **s.833A(3) cap**: profits available for distribution are limited to accumulated profits (realised
   **or not**) less accumulated losses (realised or not) — i.e. **the accounts still bind the
   ceiling**.
5. **s.833A(7)**: A and L are valued under Part 2 of the Insurance and Reinsurance Undertakings
   (Prudential Requirements) Regulations 2023, PRA MA rules, other PRA rules implementing
   Solvency II Articles 75–85 and 308b–308e, and Delegated Regulation (EU) 2015/35 Articles 7–52 and
   55–61.
6. **s.833A(8)**: for a composite, apply s.833A as if the company carried on only long-term business,
   and the rest of Part 23 as if it carried on only the other insurance business, with just and
   reasonable apportionment.
7. **s.843** applies to authorised long-term insurers **outside** s.833A (and not insurance SPVs):
   an unallocated **surplus in the long-term fund shown by an actuarial investigation** is a realised
   profit; a **deficit** is a realised loss; and otherwise "any profit or loss arising in the
   company's long-term business is to be left out of account" (s.843(5)). The actuarial investigation
   is one carried out annually under FSMA Part 9A rules or under a FSMA s.166 requirement, by an
   appointed actuary (s.843(6)).
8. **Schedule 3 para 11(1)** [R105]: the balance sheet must show separately the aggregate of amounts
   in capital and reserves that s.843 requires **not** to be treated as realised profits; para 11(2)
   requires the total assets representing the long-term fund to be shown.

**What this means for a model.** A UK reference model that wants to produce a distributable-earnings
pattern for a Solvency-UK-authorised life insurer must run the **Solvency UK balance sheet forward**,
not the accounts, and must additionally project the s.833A(5) deduction items — in particular the
**ring-fenced fund surplus** (with-profits funds) and the **matching adjustment portfolio surplus**
(pension annuities), both of which are *removed* from distributable profit. It must then apply the
accounts-based cap.

### 14. Tax — the I-E computation for BLAGAB

**Charge.** FA 2012 s.68(1) charges corporation tax on the **I-E profit** of BLAGAB; s.69 excludes
BLAGAB income and gains from any other charge, including CTA 2009 s.35; the calculation is set out in
the sections FA12 s.70(2) calls "the I-E rules" [R17][R18 LAM02050].

**FA 2012 s.73 — the six steps** (read directly from the Act) [R17]:

```
Step 1  Income chargeable for the period referable to BLAGAB (meaning of "income": s.74)
Step 2  BLAGAB chargeable gains for the period as adjusted for allowable losses (s.75)
Step 3  So much of any I-E receipt under s.92 or s.93(5)(a) as is not already in Step 1 or 2
Step 4  I  = Step1 + Step2 + Step3, reduced by the "relievable amount" of any non-trading
             deficit under CTA 2009 s.388 (loan relationships and derivative contracts)
             relievable amount = the deficit capped at (Step1 + Step2 + any s.92 receipt in Step3)
Step 5  E  = adjusted BLAGAB management expenses for the period (s.76)
Step 6  I - E
             positive  -> "I-E profit", chargeable under s.68 (subject to s.95)
             negative  -> "excess BLAGAB expenses", carried forward as an expense to the next
                          accounting period, used at step 5 of s.76
```

The step-4 relievable-amount wording was substituted and inserted by Finance Act 2016 s.67(2) [R17].

HMRC's cross-reference map for the six steps [R18 LAM02060]: Step 1 → LAM03020 (s.74 definition of
income) and LAM05000 (allocation to BLAGAB); Step 2 → LAM03200 (s.75) and LAM05100 (apportionment of
gains); Step 3 → LAM03500 (s.92 receipts) and LAM03310 (s.93–94 minimum profits adjustment); Step 4 →
LAM03060 (CTA09 s.388 deficit); Step 5 → LAM04010 (s.76 steps, with s.77–85 definitions, acquisition
expenses, restrictions and general annuity payments); Step 6 → LAM04400 (carry-forward of excess
BLAGAB expenses).

**What "E" is, and what it is not** [R18 LAM04010]: the deduction is computed broadly like an
investment company's management expenses, tailored for BLAGAB. **Underwriting-related expenses such
as claims are excluded**; expenses are restricted to accounts-based "operational expenses". Relief is
subject to specific exclusions.

**FA 2012 s.76 — the five steps to "adjusted BLAGAB management expenses"** [R18 LAM04010]:

```
Step 1  Ordinary BLAGAB management expenses referable to the period (s.77, s.81, s.82)
        - based on GAAP-compliant accounts
        - must be "expenses of management"
        - excludes claims, reinsurance premiums and other insurance-related items
Step 2  Adjust for the acquisition-expense spreading rule (s.79; s.80 defines acquisition expenses)
Step 3  Deemed management expenses (s.78(3)) - includes certain general annuity business
        annuities, loan relationship deficits carried forward, and brought-forward spread
        acquisition expenses
Step 4  Basic amount = (Step1 as adjusted by Step2) + Step3
        less expenses reversed in the period (s.78(4))
        less any BLAGAB trade loss relieved against other trade profits or surrendered as
        group relief (s.78(5))
Step 5  Add amounts carried forward from the previous period: excess BLAGAB expenses
        (s.73 Step 6) plus minimum profits test amounts (s.93(5)(b))
```

### 15. Tax — acquisition expenses: the seven-year rule and its repeal

**The rule until 31 December 2022** [R18 LAM04110]: the FA12 s.79 "adjusted amount" of acquisition
expenses referable to an accounting period was spread for tax over **seven years**, deliberately
independent of the accounts spreading. The adjusted amount = acquisition expenses in s.76 Step 1,
**less** any reinsurance commission, repayment or refund forming part of an s.92 I-E receipt for the
period, **less** acquisition expenses incurred and reversed within the same period (s.79(9)). Only
**1/7th** counts as a management expense of the period — s.76 Step 2 deducts **6/7ths**, "regardless
of the length of the accounting period" for the first period. Each of the next six accounting periods
brings a further 1/7th in at Step 3 as deemed management expenses, proportionately reduced if the
period is shorter than a year. Expenses reversed in the period or a preceding period cease to qualify
for relief in that and all later periods, with the cumulative over-relief clawed back at Step 4.

HMRC's worked example [R18 LAM04110], reproduced structurally: adjusted acquisition costs of £70,000
in 20X3 → Step 1 £70,000, Step 2 −£60,000, Step 3 +£10,000 in 20X3 giving net £10,000; £10,000 again
in 20X4; in 20X5 £7,000 is refunded, so the adjusted amount falls to £63,000 and the annual deemed
expense to £9,000, with a Step 4 reversal of £2,000 (the cumulative £1,000 × 2 over-relief for 20X3
and 20X4), giving net £7,000 in 20X5 and £9,000 in each of 20X6 to 20X9.

**The repeal** [R18 LAM04130][R109]: FA12 s.79 is repealed with effect for **accounting periods
beginning on or after 1 January 2023** (FA 2022 Sch 5 Part 2, commenced by SI 2022/1164 reg 2(1)).
HMRC's stated reasons: the commercial need for spreading has reduced, and the spreading calculation
is "more complex for life insurers writing BLAGAB … under IFRS 17 as there is added complexity in
identifying the amounts." From that date, **a deduction is given when amounts are recognised in the
company's income statement according to generally accepted accounting practice**, for all BLAGAB
writers regardless of IFRS or UK GAAP. Two savings survive: (a) s.76 Step 2 and s.77(3) continue to
apply to pre-2023 acquisition expenses not yet fully relieved, so legacy 1/7ths keep running
(SI 2022/1164 reg 2(2)); and (b) **any deduction for acquisition costs such as DAC that arose in an
earlier period but is recognised in an income statement in a period beginning on or after
1 January 2023 continues to be disallowed by FA12 s.77(3)** — i.e. relief is given only once across
the transition.

**Modelling consequence.** For a BLAGAB product model, the tax expense line diverges from the
accounts expense line in two distinct ways depending on the period: pre-2023, by the mechanical 1/7th
spread; post-2023, only by the s.77(3) transition disallowance and the ordinary exclusions (claims,
reinsurance premiums).

### 16. Tax — the minimum profits test (FA 2012 s.93–94)

[R18 LAM07230]. **Objective**: ensure the taxable income of an insurance company is at least equal to
the BLAGAB trade profit (excluding dividends) for the period, even where the I-E profit would
otherwise be lower. **Rationale**: all profit attributable to shareholders must be taxed.

**Mechanics:**
1. Compare the I-E profit (or excess BLAGAB expense, taken as a **negative** amount) with the BLAGAB
   trade profit.
2. **s.94 dividend adjustment first**: because portfolio shareholdings are trading stock of the
   insurance business, exempt dividends are inside the BLAGAB trade profit but outside the I-E "I"
   (which only includes taxable dividends). s.94 therefore requires, **for this purpose only**, the
   total amount of non-taxable distributions referable to BLAGAB to be included as part of "I"
   computed at s.73 Step 4.
3. If adjusted BLAGAB trade profits (after losses brought forward) exceed the adjusted I-E profit or
   excess BLAGAB expenses, an amount equal to the difference is an **I-E receipt** of the company
   (entering at s.73 Step 3 via s.93(5)(a)) and **the same amount is carried forward to the next
   accounting period as a BLAGAB management expense** (via s.93(5)(b), entering at s.76 Step 5).

**HMRC's two examples** [R18 LAM07230], reproduced:
- Example 1: BLAGAB trade profit £50 (after losses b/f); BLAGAB non-taxable distributions £15; I-E
  profit £25. Minimum profits charge = £50 − (£25 + £15) = **£10**. Total I-E profit becomes £35, and
  £10 is carried forward as a BLAGAB management expense.
- Example 2: BLAGAB trade profit £50 (after losses b/f); BLAGAB non-taxable distributions £15; excess
  BLAGAB expenses £5, giving net £10 before the test. Minimum profits charge = £50 − £10 = **£40**.
  Total I-E profit becomes £35, and £40 is carried forward as a BLAGAB management expense.
  (Both examples land at total I-E profits of £35 as printed; the arithmetic of example 2 is
  reproduced as HMRC prints it.)

### 17. Tax — the policyholder / shareholder split

**Two rates on one profit** [R18 LAM06010]. FA12 s.68 charges the I-E profit; s.69 stops any other
charge. The **policyholder rate** is charged on the policyholders' share as a proxy for the tax the
policyholder would pay holding the investment directly; the **main corporation tax rate** is charged
on the shareholders' share. **FA12 s.102(3)** fixes the policyholders' rate as the rate at which
income tax at the **basic rate** is charged for the tax year beginning 6 April **that applies in
England, Wales and Northern Ireland**, regardless of where the company or policyholders are resident
— **the Scottish basic rate does not apply**.

**FA12 s.103 — determining the policyholders' share** [R18 LAM06020]:
- **Mutual life insurance company (s.103(2)): the whole I-E profit is attributable to policyholders.**
- Otherwise compare the I-E profit with "the adjusted amount" of BLAGAB trade profit for the period
  (defined by s.104):
  - no BLAGAB trade profit → the policyholders' share is the **whole** I-E profit;
  - adjusted amount **<** I-E profit → the **difference** is the policyholders' share;
  - adjusted amount **≥** I-E profit → **no policyholders' share**.
- Where the profit splits, the **first slice** of the I-E profit up to the adjusted amount of BLAGAB
  trade profit is charged at the main shareholder CT rate; the **balance** at the policyholder rate.
- The s.103 calculation is also used for FA12 s.95 (use of non-BLAGAB allowable losses to reduce I-E
  profit).
- FA12 s.105 deals with the shareholders' share of BLAGAB non-taxable distributions; FA12 s.127
  provides that **no reliefs are given against the policyholders' share** of I-E profits
  [R18 LAM06000 index].

**HMRC's illustrative arithmetic** [R18 LAM01160] — reproduced with its rates, which are **2018
rates**, not current ones: total profits £1,000m, of which £600m allocated to pension business by
commercial allocation; BLAGAB investment income and gains less expenses £1,250m. I-E profit £1,250m;
£400m taxable at the then normal CT rate of 19% = £76m; £850m taxable at the then policyholder rate
of 20% = £170m; tax on I-E profit £246m; non-BLAGAB profits £600m at 19% = £114m; total £360m. At the
access date the main CT rate is **25%** and the basic rate of income tax **20%** [R110], so the
example's rate relationship (CT below the policyholder rate) is **inverted** on current rates. HMRC
itself notes: "In the past the CT rate was higher than the policyholder rate and attributing more
profit to trade profit would result in a higher tax charge. With CT rates below the basic rate of
income tax this is no longer the case" — a statement that was true when written and is **not** true
at the access date. Record the direction of the incentive as period-dependent.

**The conceptual decomposition** [R18 LAM01160], reproduced as HMRC sets it out — the same components
allocated two ways:

| Component | Company / shareholder profit | Policyholder return |
|---|---|---|
| Premium | P | (P) |
| Investment return | | I |
| Claims | (C) | C |
| Expenses | (E) | |
| Opening liabilities | OL | (OL) |
| Closing liabilities | (CL) | CL |
| Bonuses | (B) | B |
| **Total** | **Trade profit** | **Policyholder net return** |

with the two columns summing to the I-E quantity. This is the single clearest statement of why one
projection engine serves both the trade-profit and I-E computations, and why a UK model needs
opening/closing liability, bonus and expense outputs **split by BLAGAB / non-BLAGAB**.

### 18. Tax — BLAGAB / non-BLAGAB apportionment ("commercial allocation")

[R18 LAM05020]. Two separate apportionment regimes with an overriding consistency requirement:
- **I-E apportionment**: FA12 **s.97–101** determine the income/credits, losses/debits, chargeable
  gains/allowable losses and expenses apportioned to BLAGAB and brought into s.73 Steps 1–5.
- **Trade profits apportionment**: FA12 **s.114–115** split the accounting profits and tax
  adjustments between the BLAGAB and non-BLAGAB trade computations.
- Both are called **"commercial allocation"** (s.98 and s.101 for I-E; s.115 for profits). A method
  is an "acceptable commercial method" if it fairly reflects: the amounts referable to BLAGAB for the
  period of account (income, losses, expenses) — s.98(3); the contribution of the assets to the
  company's BLAGAB chargeable gains — s.101(3); and the contribution made by each of BLAGAB and other
  long-term business to overall accounting profits and tax adjustments — s.115(2).
- **Overriding consistency**: s.98(5)(a), s.101(5)(a) and s.115(4) require consistency between the
  methods. Consistency does not require an identical approach, but "the overall effect of the methods
  taken together must be fair." HMRC's worked illustration: if income from assets held to support
  guarantees is allocated to a particular group of policies for I-E purposes, the BLAGAB element of
  chargeable gains on disposal of those assets should have regard to the same subset of policies,
  **rather than a less granular basis such as mean policyholder liabilities**.
- HMRC notes that income and gains may not contribute to trade profit because of an offsetting
  movement in liabilities, yet would still be included in the I-E computation — the structural reason
  the two results are not reconcilable line by line.
- Regulation-making powers in s.98(4), s.101(4) and s.115(3) allow specified methods to be prohibited
  or required; HMRC records them as **unused as at June 2018**.
- Specific allocation guidance exists for **with-profits funds** at FA12 s.98 (LAM05070–LAM05080) and
  for business outside a with-profits fund (LAM05090) — **not read in this session** (see gaps).

**Modelling consequence.** A UK model must tag every projected cash flow, asset and liability with a
**BLAGAB / non-BLAGAB flag** and must be able to produce an allocation basis (typically driven by
policyholder liabilities or by an asset-to-policy mapping) that is used **consistently** for income,
gains and trade profits.

### 19. Tax — the IFRS 17 transitional amount

[R108][R18 LAM16010–LAM16050]. Applies to the **long-term business** of insurance companies and of
composite insurers reporting under IAS; it does **not** apply to entities writing only general
insurance or to the general business of composites, which use the normal change-of-accounting-practice
rules. **UK GAAP reporters are unaffected by the IFRS 17 change** [R18 LAM16010].

**Computation** [R108 reg 3][R18 LAM16020]:
```
Transitional amount (before apportionment)
  = accumulated profits less accumulated losses, closing balance, in the FIRST IFRS 17
    BALANCE SHEET (the pre-IFRS 17 balance sheet as restated in the first IFRS 17 accounts)
  - accumulated profits less accumulated losses, closing balance, in the PRE-IFRS 17
    BALANCE SHEET (the last balance sheet before adoption; IFRS or UK GAAP)
  each subject to any adjustment required or authorised by law in computing trade profits
  then EXCLUDING amounts relating to IFRS 9 adoption, or not solely relating to IFRS 17
```
For a calendar-year insurer adopting on 1 January 2023, the comparison is between the **restated
31 December 2022 balance sheet inside the 2023 accounts** and the **31 December 2022 balance sheet in
the 2022 accounts** — deliberately **not** the accounting transition date of 1 January 2022
[R18 LAM16020].

**Apportionment**: first between long-term business and other business, on the basis shown in the
company's IFRS 17 disclosures for the first IFRS 17 period, failing which just and reasonable; the
long-term slice is the "transitional amount". Then, where the company has both BLAGAB and non-BLAGAB
long-term business, between the two by an **acceptable commercial method** fairly representing each
business's contribution to accounting profit or loss in the period immediately before adoption, and
**consistent with the FA12 s.98 and s.115 methods for that period** [R108 regs 3–4].

**Treatment**: positive = a **receipt** of the long-term business; negative = an **expense**
[R108 reg 5]. **Spread over 10 years** beginning with the first day of the first IFRS 17 accounting
period, apportioned to accounting periods in proportion to days [R108 reg 6], and taken into account
in computing the BLAGAB trade profit or loss **and** the non-BLAGAB long-term business profits for
periods beginning on or after 1 January 2023 (or the first IFRS 17 period if later).

**Transfers and moves** [R108 regs 7–8][R18 LAM16040, LAM16050]: on an insurance business transfer
scheme, an unspread balance passes to a transferee within the charge to corporation tax and not a
mutual, running over the remainder of the transitional period; otherwise it crystallises in the
transferor in the period of transfer, with part-transfers split by an amount "fairly representing" the
attributable balance. A UK GAAP insurer moving to IAS on or after 1 January 2023 gets the **full
10-year spread**; an entity moving back from IAS to UK GAAP before the spread unwinds continues to
bring it in the same way.

**Other IFRS 17 tax points** [R18 LAM16060]: **insurance finance income or expenses** as defined in
IFRS 17 ¶87 "should not, and are not expected to, be included within the I-E calculation as they
represent movements in the value of an insurance contract asset or liability." Amounts recognised in
**OCI** are generally not taxed until recycled; SI 2022/1165 **regulation 12** (an analogue of CTA09
s.320A) ensures that where an insurance contract ceases to be recognised, any amounts remaining in
OCI are brought into account for tax; regulation 12 applies to all IFRS 17 reporters including
general insurers and non-insurers.

### 20. Deferred tax — two different models on two different balance sheets

| | **UK GAAP (FRS 102 Section 29)** [R102] | **Solvency UK (Valuation 11)** [R111] |
|---|---|---|
| Trigger | **Timing differences** — differences between taxable profits and total comprehensive income arising from income and expenses entering tax assessments in different periods (¶29.6) | **All** assets and liabilities, **including technical provisions**, recognised for solvency or tax purposes (11.1) |
| Measurement base | Not a balance-sheet comparison; "timing differences plus" (BC B29.1–B29.7) | The **difference between the Solvency UK value and the tax value**, where the Solvency UK value comes from the Valuation Part and, for technical provisions, from the Technical Provisions, Matching Adjustment, Conditions Governing Business and SCR – General Provisions Parts (11.2) |
| Permanent differences | No deferred tax except business combinations (¶29.10, ¶29.11) | Not carved out |
| DTA recognition | Only to the extent probable of recovery against reversal of DTLs or other future taxable profits (¶29.7) | Positive value only where probable that future taxable profit will be available, taking account of carry-forward time limits (11.3) |
| Rate | Enacted or substantively enacted at the reporting date, expected to apply on reversal; average rates where banded (¶¶29.12–29.13) | Not specified in the rules read |
| Pillar Two | Neither recognised nor disclosed (¶29.2B); excluded from measurement (¶29.12A) | Not addressed in the rules read |

**The gap that matters.** Because Valuation 11.2 measures deferred tax off the **Solvency UK versus
tax** difference while FRS 102 measures it off timing differences in the **accounts**, the two
deferred tax balances are structurally different numbers for the same company. A UK model that
projects deferred tax must therefore carry **three** liability measures per period — accounts, tax,
and Solvency UK — not two.

**Two UK GAAP anti-double-count rules** [R100]: IG2.44 — where the long-term business provision has,
in assessing future net cash flows, had regard to the **timing of tax relief** where assumed expenses
exceed attributable income, that relief must be **excluded from the determination of deferred tax**.
IG2.49 — the same for the linked-liability provision where it has regard to the timing of the tax
obligation. A model that puts a tax-timing allowance inside the reserve must suppress the
corresponding deferred tax.

### 21. LACDT — the adjustment for the loss-absorbing capacity of deferred taxes

[R112]. `Adj = Adj_TP + Adj_DT` (SCR-SF 6.1(3)).

**TP leg (SCR-SF 6.3(1)):**
```
Adj_TP = - max( min( BSCR - nBSCR ; FDB ) ; 0 )
  BSCR  = basic SCR
  nBSCR = net basic SCR
  FDB   = technical provisions WITHOUT risk margin in respect of future discretionary benefits
```
The FDB risk-mitigating effect counts only to the extent the firm can establish a reduction in future
discretionary benefits may be used to cover unexpected losses, is capped at the sum of technical
provisions and deferred taxes relating to those FDB, and is measured by comparing FDB under adverse
circumstances against FDB under the best-estimate assumptions (6.2).

**Deferred tax leg (SCR-SF 6.4(1)):**
```
Adj_DT = change in the value of the firm's deferred taxes resulting from an INSTANTANEOUS LOSS of
         BSCR + Adj_TP + SCR_operational
```
with: deferred taxes valued under Valuation 11.1–11.2 (6.4(2)) [R111]; **an increase in DTAs arising
from that loss may not be used** unless 6.5 applies (6.4(3)); future management actions may be assumed
subject to Technical Provisions – Further Requirements 8 (6.4(4)); a decrease in DTLs or an increase
in DTAs gives a **negative** adjustment (6.4(5)); a positive change of deferred taxes gives a **nil**
adjustment (6.4(6)); and where the loss must be allocated to causes, the allocation follows the
contribution of standard formula modules and sub-modules to the basic SCR, with a partial-internal-
model carve-out (6.4(7)).

**6.5** is a transitional permission **ending 30 December 2025** allowing the DTA increase to be used
subject to: probable future taxable profit; an assessment covering carry-forward time limits, the
magnitude of the loss and its impact on the firm's financial situation, pricing, market profitability,
demand, reinsurance coverage and macro-economic variables, and increasing uncertainty with horizon;
documentary evidence available to the PRA; advance written notice to the PRA; **no new business sales
in excess of the business plan**; **no new business after the planning horizon, which must not exceed
five years**; post-loss investment returns assumed equal to forward rates implied by the risk-free
curve unless higher returns can be demonstrated; increasing haircuts on new-business profits projected
beyond the planning horizon within a finite horizon; and no assumptions more favourable than those
used under Valuation 11.

**Modelling consequence.** LACDT requires a **post-stress tax balance sheet**: the model must be able
to re-run the Solvency UK versus tax comparison after an instantaneous loss of
`BSCR + Adj_TP + SCR_op` and report the change in net deferred taxes, floored at zero benefit. For a
with-profits product the TP leg is computed first and feeds the size of the loss used for the DT leg.

---

## Model hooks

What a liability cash flow projection must produce, for whom, at what granularity, on what basis and
at what date.

| Item | What the liability model must produce | Granularity / basis / timing |
|---|---|---|
| **Basis flag (accounts)** [R103][R101] | A per-entity flag: **Companies Act accounts** (FRS 102 + FRS 103, or FRS 101) vs **IAS individual accounts** (IFRS 17). The two produce structurally different outputs from the same cash flows and cannot be mixed in one set of individual accounts | Entity level, set once; effectively one-way after the first IAS year absent an s.395(4) trigger |
| **UK GAAP insurance liability** [R99 ¶¶3.11, 2.14][R105 note 21] | The recognised long-term business provision on the entity's grandfathered basis (net premium or gross premium method), **plus** a separate current-assumption, option-and-guarantee-inclusive projection to run the liability adequacy test | Per contract in principle (Sch 3 para 52(1)), statistical methods permitted; at each reporting date; annual computation signed off by a Fellow of the IFoA |
| **UK GAAP DAC** [R105 para 13, note 17][R99 ¶¶3.7–3.10] | Acquisition costs incurred, split into deferrable and non-deferrable; a **recoverability test** against NPV of margins after providing for contractual liabilities and expenses, allowing for discontinuance; an **amortisation profile matching the margin profile**; and a flag for whether the reserve already recognises the costs explicitly or implicitly | Per model point per period; **suppressed entirely for a with-profits fund within FRS 103 ¶3.1(b) scope**; feeds assets item G.II and technical account item 8(b) |
| **Linked liability split** [R105 note 26][R100 IG2.47] | **Unit reserve** (Sch 3 item D) separate from **non-unit reserve** for death risk, expenses, maturity guarantees and guaranteed surrender values (Sch 3 item C.2); a floor at the fund-referenced surrender/transfer value; and the net linked assets held, so mismatching can be explained | Per contract per period; two liability lines, not one |
| **With-profits realistic liability** [R99 ¶¶3.12–3.14][R100 IG1.2] | Realistic value of liabilities; the **shareholders' share of projected future bonuses** on market-consistent financial assumptions with non-economic assumptions consistent with the realistic liability; the MSSB liability for comparison; the **FFA transfer** equal and opposite to the net adjustment; the related tax effect | Per fund per period; both the realistic and MSSB numbers are needed because the difference is the FFA transfer |
| **With-profits options and guarantees** [R100 IG1.11–IG1.13] | Time value **and** intrinsic value, by market-consistent stochastic model unless a market value exists; per-scenario **management actions** (asset mix, charges, bonus policy) that are implementable and PPFM-consistent | Per fund, per scenario, per period; a deterministic result is explicitly inadequate |
| **VIF on non-participating business in a with-profits fund** [R99 ¶3.12(c)][R100 IG1.6–IG1.7] | Discounted future profits on the non-participating business, with liabilities at the statutory solvency basis **including** MSSB adjustments, and with any **release of capital requirements stripped out** | Per fund; recognised only where the realistic liability takes account of the value directly or indirectly |
| **Schedule 3 technical account** [R105] | Every long-term technical account line by period: gross premiums written; outward reinsurance premiums; investment income; realised and unrealised gains and losses; claims paid gross and reinsurers' share; change in the provision for claims; **change in the long-term business provision gross and reinsurers' share**; bonuses and rebates; acquisition costs; **change in DAC**; administrative expenses; reinsurance commissions and profit participation; investment expenses and charges; **tax attributable to the long-term business**; allocated investment return transferred to the non-technical account; **transfers to/from the FFA** | Annual, per technical account; gross and reinsurers' share must be produced separately, never netted |
| **IFRS 17 fulfilment cash flows** [R106 ¶¶2.43–2.48] | Probability-weighted expected cash flows within the contract boundary, current and explicit, entity perspective, market variables consistent with observable prices; **discounted at an entity-determined curve satisfying IFRS 17:36** (not the PRA curve); plus an explicit **risk adjustment for non-financial risk** | Per **group** (portfolio × profitability bucket × annual cohort), each reporting date |
| **IFRS 17 CSM roll-forward** [R106 ¶¶2.49–2.55, 2.66–2.68] | CSM at initial recognition as a residual (zero with an immediate loss if onerous); **coverage units** by period reflecting the quantity of benefits and expected coverage period; interest accretion at **locked-in** rates under GMM and adjustment at **current** rates under VFA; the entity's share of the change in fair value of underlying items under VFA | Per group per period; the coverage-unit driver is a required model output, not a reporting-layer choice |
| **IFRS 17 loss component** [R106 ¶2.50] | Identification of groups onerous at initial recognition and groups becoming onerous, with the loss recognised immediately | Per group, at initial recognition and each reporting date |
| **IFRS 17 acquisition cash flow asset** [R106 ¶¶2.56–2.59] | Acquisition cash flows allocated to groups, an asset for amounts paid before a group is recognised (including expected **renewals**), a recoverability/impairment assessment, and the **premium element intended to recover acquisition costs** for the revenue add-back | Per group per period; the add-back and the equal insurance service expense must be produced separately |
| **IFRS 17 VFA underlying items** [R106 ¶¶2.62–2.63] | Fair value of the underlying items; the entity's **share** of that fair value; and the fulfilment cash flows that **do not** vary with underlying item returns, so the variable fee can be struck | Per group per period, for unit-linked and with-profits |
| **IFRS 17 OCI disaggregation** [R106 ¶2.29] | Insurance finance income or expense split between P&L and OCI where the portfolio-level policy elects disaggregation | Per **portfolio**, per period |
| **Distributable profits (s.833A)** [R104] | A projected Solvency UK balance sheet (A, L) **plus** the s.833A(5) deductions: qualifying investment subsidiary excess, DB pension surplus, **ring-fenced fund surplus**, related DTLs, **matching adjustment portfolio surplus**, and non-distributable capital items; and, separately, the accounts accumulated profits/losses for the s.833A(3) cap | Entity level, at each balance sheet date; the WP and PA products drive the two largest deductions |
| **Distributable profits (s.843)** [R104][R105 para 11] | For a non-s.833A authorised long-term insurer: the **unallocated surplus in the long-term fund shown by an actuarial investigation**, and the aggregate of capital-and-reserves amounts not treated as realised profits (a required balance sheet line) | Entity level, annually, from the actuarial investigation |
| **I-E "I"** [R17 s.73][R18 LAM05020] | BLAGAB-referable **income** (s.74 meaning) and **chargeable gains net of allowable losses**, produced on a commercial allocation basis consistent with the gains and trade-profit allocations, plus any s.92/s.93(5)(a) receipts and the relievable CTA09 s.388 deficit | Per accounting period, per fund, with a BLAGAB/non-BLAGAB tag on every asset and cash flow |
| **I-E "E"** [R18 LAM04010, LAM04110, LAM04130] | **Ordinary BLAGAB management expenses** on a GAAP basis, **excluding claims and reinsurance premiums**; acquisition expenses identified separately; the pre-2023 seven-year spread run-off; deemed management expenses; reversed expenses; BLAGAB trade losses relieved elsewhere; excess BLAGAB expenses and minimum-profits amounts brought forward | Per accounting period; the acquisition-expense stream must be a distinct output because its tax profile differs from its accounts profile in every period before 2023 and by the s.77(3) disallowance after |
| **BLAGAB trade profit** [R18 LAM01160, LAM06020] | The accounts trade result apportioned to BLAGAB under FA12 s.114–115, plus the s.104 "adjusted amount" and the BLAGAB non-taxable distributions for the s.94 adjustment | Per accounting period; needed for both the minimum profits test and the policyholder/shareholder split |
| **Policyholder / shareholder tax split** [R18 LAM06010, LAM06020][R110] | I-E profit; adjusted BLAGAB trade profit; the split of I-E profit into a first slice at the CT main rate and a balance at the basic rate of income tax; and a **mutual flag** (whole I-E profit is policyholders') | Per accounting period, entity level; rates from R110, not from the LAM examples |
| **IFRS 17 transitional amount** [R108] | Accumulated profits less accumulated losses on both the first IFRS 17 balance sheet and the pre-IFRS 17 balance sheet, with trade-profit adjustments and IFRS 9 amounts excluded; the long-term/other apportionment; the BLAGAB/non-BLAGAB commercial allocation; and a **10-year day-proportioned spread** | Entity level, once at adoption, then per period for 10 years; transfers and cessations crystallise or transfer the unspread balance |
| **Deferred tax (three bases)** [R102 ¶29.6][R111 11.1–11.3][R100 IG2.44, IG2.49] | Accounts liability, tax liability and Solvency UK liability by period, so timing differences (UK GAAP) and Solvency-versus-tax differences (Valuation 11.2) can both be struck; DTA recoverability evidence; and suppression of deferred tax where the reserve already allows for tax timing | Per period, entity level; **three** liability measures, not two |
| **LACDT** [R112 6.3–6.5] | Post-stress deferred taxes after an instantaneous loss of `BSCR + Adj_TP + SCR_op`; the FDB quantity (technical provisions without risk margin in respect of future discretionary benefits) for the TP leg; and a flag for whether any DTA increase may be used | At each SCR calculation date; the DT leg depends on the TP leg, so the order of computation is fixed |

---

## Product applicability

`x` = the item directly binds; `(x)` = qualified or conditional; `—` = expressly does not apply;
`?` = retrieved sources do not settle it; blank = not indicated.

Product key: TA = term-assurance, CI = critical-illness, IP = income-protection, WOL = whole-of-life,
WP = with-profits, ULB = unit-linked-bond, PA = pension-annuity.

| Item [R#] | TA | CI | IP | WOL | WP | ULB | PA |
|---|---|---|---|---|---|---|---|
| FRS 103 scope — insurance contract [R99 ¶1.2] | x | x | x | x | x | (x) | x |
| FRS 103 liability adequacy test [R99 ¶¶2.14–2.18] | x | x | x | x | x | (x) | x |
| FRS 103 ¶¶3.3–3.6 premium/claim recognition [R99] | x | x | x | x | x | (x) | x |
| **FRS 103 ¶¶3.7–3.9 DAC required** [R99][R105 para 13] | x | x | x | x | — | (x) | x |
| **FRS 103 ¶3.10 no DAC in with-profits funds** [R99] | | | | (x) | **x** | | (x) |
| FRS 103 ¶¶3.11–3.15 MSSB / realistic liabilities / FFA [R99] | | | | (x) | **x** | | (x) |
| FRS 103 Section 5 with-profits disclosures [R99] | | | | (x) | **x** | | (x) |
| FRS 103 ¶2.30 DPF guaranteed element / equity split [R99] | | | | (x) | **x** | (x) | (x) |
| FRS 103 ¶2.11 shadow accounting [R99] | (x) | (x) | (x) | (x) | (x) | (x) | (x) |
| FRS 103 ¶2.23 unbundling of deposit components [R99] | | | | (x) | (x) | **x** | |
| IG1.11–IG1.13 stochastic options and guarantees [R100] | | | | (x) | **x** | (x) | (x) |
| Sch 3 liabilities C.2 long-term business provision [R105] | x | x | x | x | x | (x) | x |
| **Sch 3 liabilities D linked liabilities** [R105 note 26] | | | | (x) | (x) | **x** | |
| **Sch 3 liabilities Ba fund for future appropriations** [R105 note 19] | | | | (x) | **x** | | |
| Sch 3 assets G.II deferred acquisition costs [R105 note 17] | x | x | x | x | — | (x) | x |
| Sch 3 para 52 long-term business provision computation [R105] | x | x | x | x | x | (x) | x |
| **IFRS 17 general measurement model** [R106] | **x** | **x** | **x** | **x** | | | **x** |
| **IFRS 17 variable fee approach** [R106 boxed text] | | | | (x) | **x** | **x** | |
| IFRS 17 premium allocation approach [R106] | (x) | (x) | (x) | | | | |
| IFRS 17 annual cohorts / profitability buckets [R106 ¶¶2.14–2.17] | x | x | x | x | x | x | x |
| IFRS 17 coverage units [R106 ¶2.54] | x | x | x | x | x | x | **?** |
| IFRS 17 onerous group / loss component [R106 ¶2.50] | x | x | x | x | x | x | x |
| IFRS 17 acquisition cash flows into CSM [R106 ¶¶2.56–2.59] | x | x | x | x | x | x | x |
| IFRS 17 inherited estate judgement [R106 §3 issue D] | | | | (x) | **x** | | |
| CA 2006 s.395 basis choice [R103] | x | x | x | x | x | x | x |
| **CA 2006 s.833A distributable profits formula** [R104] | x | x | x | x | **x** | x | **x** |
| CA 2006 s.843 realised profits (non-s.833A insurers) [R104] | (x) | (x) | (x) | (x) | (x) | (x) | (x) |
| **FA 2012 BLAGAB / I-E basis** [R17][R18 LAM01080] | (x) | (x) | (x) | **x** | **x** | **x** | — |
| FA 2012 non-BLAGAB trade basis [R17][R18 LAM01080] | **x** | **x** | **x** | (x) | (x) | | **x** |
| FA 2012 s.79 seven-year spreading (pre-2023) [R18][R109] | (x) | (x) | (x) | x | x | x | — |
| FA 2012 s.93 minimum profits test [R18 LAM07230] | (x) | (x) | (x) | x | x | x | — |
| FA 2012 s.102–103 policyholder / shareholder split [R18] | (x) | (x) | (x) | x | x | x | — |
| FA 2012 s.97–101 / s.114–115 commercial allocation [R18 LAM05020] | x | x | x | x | x | x | x |
| SI 2022/1165 IFRS 17 transitional amount [R108] | x | x | x | x | x | x | x |
| FRS 102 s.29 deferred tax (accounts) [R102] | x | x | x | x | x | x | x |
| Valuation 11 deferred tax (Solvency UK) [R111] | x | x | x | x | x | x | x |
| SCR-SF 6.3 LACTP (future discretionary benefits) [R112] | | | | (x) | **x** | | |
| SCR-SF 6.4 LACDT [R112] | x | x | x | x | x | x | x |

**Notes on the matrix**

- **ULB and the insurance-contract test.** A unit-linked bond frequently fails FRS 103's significant-
  insurance-risk test and is an **investment contract** — "not regarded as insurance for accounts
  purposes … treated as 'investment contracts' with premiums from customers generally held on balance
  sheet as policyholder deposits and only the fees charged within the policy treated as income"
  [R18 LAM01100]. Such contracts fall outside FRS 103 into FRS 102 Sections 11/12 and 23, hence the
  `(x)` marks on the FRS 103 rows. A bond with a material death benefit uplift can pass the test; the
  representative product's classification is a per-design determination, not a product-family fact.
  The same fork does **not** exist under IFRS 17 in the same place, but IFRS 17 has its own
  investment-component exclusion from revenue [R106 ¶2.26].
- **WP and DAC.** The `—` on the DAC rows for WP is the FRS 103 ¶3.10 prohibition, but it is scoped by
  ¶3.1(b) to funds within the pre-2016 PRA realistic capital regime, and IG1.1 makes ¶3.12 optional
  outside that scope [R99][R100]. A with-profits fund never in the realistic regime is not, on the
  text retrieved, caught by ¶3.10 — see gaps.
- **WOL and WP marks.** WOL carries `(x)` on every with-profits row because a whole-of-life contract
  may be written either as a non-profit contract in the main fund or as a with-profits contract in a
  with-profits fund; the marks apply in the second case only.
- **PA and the IFRS 17 coverage-unit question is marked `?` deliberately.** R106 identifies CSM
  allocation for **annuities** as priority issue A of the endorsement assessment, records that the
  IFRS Interpretations Committee had issued a Tentative Agenda Decision on the point, and notes
  continuing divergence on whether investment-return service is a separate service and on the
  weighting of coverage units [R106 §3 issue A, read in outline]. The *requirement* to identify
  coverage units binds; the *right answer for an annuity* is not settled by the retrieved material.
- **PA and BLAGAB.** A UK **pension** annuity is pension business, excluded from BLAGAB by FA12
  s.57(2)(a), and is taxed on **trade profits**, not I-E [R18 LAM01080][R17]. Hence `—` on the BLAGAB
  rows. Note that "general annuity business" *is* inside BLAGAB — a purchased life annuity bought with
  non-pension money would flip these marks. The library's representative PA is pension business.
- **TA / CI / IP tax marks.** Protection business written from **1 January 2013** is excluded from
  BLAGAB and taxed on a trading basis like general insurance; policies written before that date
  **continue to be taxed as BLAGAB** unless the LAM14040 election has been made [R18 LAM01080]. Hence
  `(x)` on the BLAGAB rows (legacy back-books) and `x` on the non-BLAGAB trade row.
- **s.833A vs s.843.** Every UK life insurer in this library's scope is expected to be Solvency-UK
  authorised, so s.833A governs and s.843 is the residual path — hence `x` throughout on the s.833A
  row and `(x)` on the s.843 row. The **WP** and **PA** emphases on the s.833A row reflect that the
  ring-fenced-fund surplus deduction (s.833A(5)(c)) and the matching-adjustment portfolio surplus
  deduction (s.833A(5)(e)) are the two product-specific deductions in the formula.
- **LACTP.** SCR-SF 6.3 works through **future discretionary benefits**, which in this library exist
  only in with-profits (and in a with-profits WOL) — hence the concentration of marks there [R112].

---

## Gaps and caveats

### Corrections to assumptions the library currently carries

1. **The R38 narrative paragraph in `uk/_research/regulatory-actuarial.md` is now substantiated and
   partly extended.** That file's "Why one cash flow model serves several bases" paragraph describes
   IFRS 17 mechanics and tags them "[mechanics: unverified — general knowledge; standard text not
   fetched]". Those mechanics are now **verified from R106**, with the addition that the UKEB's own
   expectation is **VFA for unit-linked and with-profits, GMM for protection and annuities**. When the
   reference page is next revised, that paragraph should be re-tagged to [R106] and the VFA/GMM
   mapping added.
2. **The library should not assume any UK statutory-accounts new-business strain.** Schedule 3 para 13
   **requires** DAC [R105]; FRS 103 ¶3.7 **requires** deferral subject to recoverability [R99]. The
   U.S. no-DAC framing does not transfer.
3. **FRS 103 cannot be aligned with IFRS 17 under current company law**, on the FRC's own published
   analysis [R101]. Any drafting implying that UK GAAP will converge on IFRS 17 in the near term is
   wrong; the FRC says sufficient implementation experience is "unlikely to be available before two
   full cycles of reporting have been completed but it may be later still" [R101].
4. **The 7-year tax spreading of acquisition expenses is repealed** for accounting periods beginning
   on or after 1 January 2023 [R109][R18 LAM04130], with legacy amounts running off.

### Conflicts recorded, not resolved

- **BEIS letter vs current Schedule 3 text.** The 3 February 2017 BEIS letter [R113] interprets a
  version of Schedule 3 para 52(3) that contained a reference to the Solvency II Directive. The text
  retrieved on 2026-08-06 [R105] contains no such reference — the words "with due regard to generally
  accepted actuarial principles and" were inserted and other words omitted by SI 2019/145 (as amended
  by SI 2020/523) with effect for financial years beginning on or after IP completion day. The
  letter's conclusion is corroborated independently by FRS 103 BC45 [R99]; its premise is stale. Both
  are recorded.
- **FRS 103 ¶3.7 vs ¶3.1(b).** ¶3.7 opens "Except as required by paragraph 3.10", but ¶3.1(b)
  restricts ¶¶3.10–3.15 to with-profits business within the pre-2016 PRA realistic capital regime, and
  IG1.1 makes ¶3.12 optional outside that scope [R99][R100]. Whether the DAC prohibition in ¶3.10
  reaches a with-profits fund that was never in the realistic regime is **not settled** by the text
  retrieved. Do not assert either reading.
- **HMRC's rate-incentive statement is out of date.** LAM01160 states that with CT rates below the
  basic rate of income tax, attributing more profit to trade profit no longer increases the tax charge
  [R18]. At the access date the CT main rate is 25% and the basic rate 20% [R110], so the relationship
  is reversed. Record the incentive as period-dependent; do not restate HMRC's sentence as current.

### Verified but time-sensitive

- **SCR-SF 6.5** — the transitional permission to utilise an increase in deferred tax assets in the
  LACDT calculation is stated in the 05/08/2026 rulebook view as running "For a transitional period
  **ending 30 December 2025**" [R112]. On its face that period has expired at the access date, yet the
  rule remains printed in the current view. **No PRA instrument confirming its expiry or extension was
  retrieved.** Treat 6.5 as expired for a current-date calculation but flag it; stream 2 should check.
- **FRS 102 / FRS 103 Periodic Review 2024** amendments are effective for periods beginning on or
  after **1 January 2026** [R101][R102b], except the FRS 103 Section 6 Transition amendment (1 January
  2024). A model or document describing "current UK GAAP" must state which edition it means.
- **FRS 102 "Adapted formats" amendment** published 18 February 2026 is effective **1 January 2027**
  and arises from the replacement of IAS 1 by IFRS 18; it "relate[s] principally to entities which
  choose to adapt one of the balance sheet formats and/or one of the profit and loss account formats"
  [R102b]. **The amendment document itself was not fetched**, and whether it touches the Schedule 3
  insurance formats was not determined.
- **The UKEB post-implementation review of IFRS 17** is committed to report by 1 January 2028 [R38].
  Nothing in this stream's retrieval indicates it has reported.

### Not retrieved / deliberately not asserted

- **IFRS 17 itself was never read.** The standard text is paywalled [R107]. Every IFRS 17 paragraph
  number in this file is one the UKEB quotes in R106. Paragraph numbers for which R106 gives only a
  summary (e.g. the detailed conditions for direct participation features in IFRS 17:B101–B106, the
  full IFRS 17:33 estimate criteria, the modified retrospective specified modifications in
  IFRS 17:C6–C19A, the disclosure requirements beyond IFRS 17:93) are **not** reproduced here and must
  not be invented. **No confidence level, no coverage-unit formula and no transition proxy is stated
  anywhere in this file**, because none was read.
- **FRS 103 ¶¶2.16(b) onward, 2.17 and 2.18** (the alternative liability adequacy measurement where
  the entity's own test fails the minimum requirements) were read only in part; the tail of ¶2.16 and
  the whole of ¶¶2.17–2.18 were **not** read. The LAT *trigger* and *minimum requirements* above are
  verified; the fallback measurement is not.
- **FRS 103 Appendix II (Definition of an insurance contract) was not read.** The significant-
  insurance-risk test that decides whether a UK product is an insurance contract or an investment
  contract — the single most consequential classification for a unit-linked bond — rests here on the
  glossary definition and on HMRC's description [R18 LAM01100], not on ¶¶A2.1–A2.24. A follow-up pass
  should read Appendix II in full.
- **FRS 103 Implementation Guidance Section 3 (capital disclosures for entities with long-term
  insurance business) was not read**, beyond the cross-reference at IG1.12 to IG3.14(c). The capital
  statement disclosures are therefore undocumented here.
- **The FRS 103 IG page-1 text extraction failed** (pypdf error); the cover page content is not
  recorded. All substantive pages extracted cleanly.
- **INSPRU as at 31 December 2015** — rules **1.3.40** (realistic value of liabilities), **1.3.190**
  (current liabilities) and **1.3.33(3)** (subsidiary capital requirement deduction) are the operative
  definitions behind the FRS 103 with-profits requirements [R99 glossary][R100 IG1.9], and **none of
  them was retrieved**. They are reachable through the PRA Rulebook's as-at-date view. Until they are
  read, the *content* of "realistic value of liabilities" is a citation, not a specification. This is
  the largest single hole in the UK GAAP with-profits material.
- **The pre-2016 "statutory solvency basis"** referenced by the MSSB definition [R99] was likewise not
  retrieved; the net premium method's "detailed methodology … in regulations contained in the PRA
  Rulebook as at 31 December 2015" [R99 glossary] was not read. **No valuation interest rate,
  zillmer limit or mortality basis from that regime is stated anywhere in this file.**
- **HMRC LAM pages not read** that a fuller pass should cover: LAM03010, LAM03060, LAM03200, LAM03310,
  LAM03410, LAM03500, LAM03510 (the "I" and gains chapters); LAM04020–LAM04040, LAM04100, LAM04200,
  LAM04210, LAM04300, LAM04400, LAM04500 (the "E" detail and the s.76 worked example); LAM05010,
  LAM05030–LAM05060, **LAM05070 and LAM05080 (with-profits fund allocation, FA12 s.98)**, LAM05090,
  LAM05100, LAM05110, LAM05120; LAM06030–LAM06060 (the "adjusted amount", BNTD, the worked
  policyholder-share example, and FA12 s.127); LAM07010 and the rest of the trade-profits chapter;
  **LAM08000's actual schedules A1–A9, B1–B3 and G — only its index was read**, so the fully worked
  life tax computation HMRC publishes is available but untranscribed; LAM09000–LAM15000 (double tax
  relief, reinsurance, fixed capital detail, cross-border, transfers of business, FA 2012 transitional
  provisions including **LAM14040**, the protection-business election, and excess expenses/losses);
  LAM17000 (friendly societies). **LAM05070/LAM05080 and LAM08000's schedules are the two most
  valuable unread items in the tax material.**
- **Finance Act 2012 sections read directly: only s.73.** Everything else attributed to FA 2012 in
  this file is HMRC's account of the section [R18], not the enacted words. Before any product document
  quotes a FA 2012 subsection, read the section on legislation.gov.uk.
- **FA 2022 Schedule 5 itself was not fetched** — only its commencement instrument [R109] and HMRC's
  description [R18 LAM04130]. The precise amendments Part 2 makes to CTA 2009 and FA 2012 are
  therefore [unverified] beyond the repeal of s.79 and the survival of s.76 Step 2 / s.77(3).
- **SI 2022/1165 regulations 9–12** were read only in part; **regulation 12** (the OCI
  bring-into-account rule) is documented from HMRC's description [R18 LAM16060], not from the SI text.
- **The Insurance and Reinsurance Undertakings (Prudential Requirements) Regulations 2023, Part 2**
  — the valuation authority s.833A(7)(a) points at — was **not retrieved**. Neither were the retained
  Delegated Regulation (EU) 2015/35 Articles 7–52 and 55–61 that s.833A(7)(d) invokes. The s.833A
  formula is verified; the valuation rules it depends on are cited, not read.
- **Companies Act 2006 s.396** (the content requirements for Companies Act individual accounts) was
  not read directly; s.395's cross-reference to it is verified. **s.831** (public company net asset
  restriction) and **s.836** (relevant accounts) were not read.
- **FRS 101 Reduced Disclosure Framework** was not retrieved. HMRC records it as one of the three
  bases a UK insurer's entity accounts may use — "essentially IFRS recognition and measurement
  requirements but with reduced disclosures and presented in the format required by the Companies Act"
  [R18 LAM01100]. Whether an FRS 101 preparer applies IFRS 17 recognition and measurement inside
  Schedule 3 formats — which would sit awkwardly with the FRC's company-law analysis at R101 — is
  **not settled by anything retrieved** and is a genuine open question for a UK reference model.
- **No FRS 103 or FRS 102 numerical parameter is transcribed anywhere in this file** because neither
  standard contains any; the parameters live in the entity's grandfathered basis and in INSPRU as at
  31 December 2015, neither of which was read.
- **Schedule 3 Part 2 Sections A–D and F**, and the disclosure paragraphs 85–86 and the segmental
  premium-analysis paragraphs, were read only where quoted above. **Schedule 6 Part 3** (overseas
  subsidiary local-basis policyholder liabilities, referenced at IG2.39) was not read.

### Fetch behaviour observed on 2026-08-06

- `frc.org.uk` served all standard and guidance PDFs on first request with a browser User-Agent; the
  library pages are server-rendered and extracted cleanly.
- `legislation.gov.uk` served every section and schedule requested; the retrieved pages state they are
  "up to date with all changes known to be in force on or before 05 August 2026", and each carries
  outstanding-changes notices (s.843's page flags a Schedule 11A substitution by 2026 c. 23 Sch 36
  para 35 not yet applied).
- `gov.uk` HMRC manual pages extracted cleanly; the table layouts in LAM04110 and LAM01160 flatten to
  a linear list and were reconstructed by hand above.
- `endorsement-board.uk` served the ECA PDF (1.84 MB) on first request; one page failed text
  extraction.
- `prarulebook.co.uk` required the browser User-Agent (as the frozen R1/R2 notes record); both Parts
  returned HTTP 200 with it. The SCR – Standard Formula Part extracts to ~427,000 characters and was
  searched, not read whole.
- `ifrs.org` returned HTTP 200 but the page is client-rendered; direct HTML extraction yielded
  41 characters. A markdown-converting fetcher retrieved the readable content.
- `www.gov.uk/guidance/corporation-tax-rates-and-allowances` returned **HTTP 404**;
  `www.gov.uk/corporation-tax-rates` returned 200 and is the URL recorded at R110.
- No URL on this page is fabricated; every URL listed was actually requested and its HTTP status
  observed.
