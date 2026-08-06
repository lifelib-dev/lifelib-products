# UK Regulatory Reporting, Accounting and Capital Requirements for Liability Models

- **Status:** Draft, 2026-08-06 (all cited sources accessed 2026-08-06).

**Scope note.** This file explains the UK prudential, accounting and tax requirements **that bear on how a product is
represented in an actuarial model** — which items exist, why they exist, which of the seven products in `uk/products/`
they bite, and what a projection must produce. It is concept-only by design: formulas, stress sizes, correlation
matrices, algorithms and worked arithmetic live in `uk/regulatory/technical-notes.md`, cross-referenced **by section
name** rather than duplicated. Product mechanics stay in `uk/products/<type>/`.

**Terminology: what "statutory accounting" maps to in the UK.** The file names here mirror `us/regulatory/` for
structural parity across the library. **The UK has no "statutory accounting" in the U.S. sense** — no NAIC-style
solvency-purpose accounting basis, and no annual statement blank that is simultaneously the accounting ledger. What a UK
life insurer runs is three separate measurements:

| Layer | What it is | Instrument |
|---|---|---|
| **The Solvency UK regulatory balance sheet** | The prudential measurement: assets and liabilities at exchange/transfer value, technical provisions = best estimate + risk margin, own funds, SCR and MCR | PRA Rulebook — Valuation, Technical Provisions, Technical Provisions – Further Requirements, Matching Adjustment, SCR and Own Funds Parts [REG-R39][REG-R1][REG-R41][REG-R2][REG-R62][REG-R77] |
| **The statutory accounts** | Companies Act accounts under **FRS 102 + FRS 103**, or **UK-adopted IFRS 17** individual accounts | Companies Act 2006 s.395 [REG-R103]; SI 2008/410 Schedule 3 for the formats [REG-R105]; FRS 103 [REG-R99]; the UKEB assessment of IFRS 17 [REG-R106] |
| **Tax** | Not a liability measurement at all — computed **from the accounts** with the Finance Act 2012 overlay | FA 2012 Part 2 [REG-R17]; HMRC Life Assurance Manual [REG-R18] |

Where this document says "the accounts" it means the second row, never the first; "Solvency UK" means the first, which
is a supervisory return and **not** a set of accounts. The trap a U.S.-trained reader will fall into is set out at the
end of the next section: the U.S. story of *acquisition costs expensed as incurred, no DAC asset, first-year surplus
strain* is **reversed** in the UK statutory accounts.

**Citation conventions** (identical to the rest of the library, non-negotiable). Everything is cited as **[REG-R#]**
against the shared UK numbering in `uk/references/regulatory-and-actuarial-references.md`. **R1–R38** are the frozen
pre-existing entries already cited by the seven product documents. **R39–R120** are added by this effort, with
provenance in `uk/_research/solvency-uk-technical-provisions.md` (R39–R49),
`uk/_research/solvency-uk-discounting-and-transitionals.md` (R53–R60),
`uk/_research/solvency-uk-scr-standard-formula.md` (R61–R73),
`uk/_research/solvency-uk-own-funds-mcr-and-internal-models.md` (R77–R83),
`uk/_research/solvency-uk-reporting-governance.md` (R84–R98), `uk/_research/uk-accounting-and-tax.md` (R99–R113) and
`uk/_research/uk-product-regulatory-applicability.md` (R114–R120). **R50–R52, R74–R76 and R121–R133 are unused by
design** — the streams were allocated parallel blocks and the tails left spare rather than padded; an unused number is
not a missing entry. Twelve documents were independently numbered by more than one stream — eleven twice, and SS15/16
three times; the duplication is **recorded, not renumbered**, and this file cites only the canonical number. The
duplication table and the per-entry bibliography for this directory are in `uk/regulatory/sources.md`.

Every quantitative parameter, factor, stress, correlation, threshold, formula and effective date carries a [REG-R#], or
**[std]** where it is a standardization introduced for this reference implementation, or **[unverified]** where the
research could not confirm it against a retrieved document. **Nothing marked [unverified] in a research file is upgraded
here.** Where two retrieved sources conflict and the research recorded the conflict, the conflict is reproduced rather
than resolved.

**This work removes a stated limitation of the frozen reference page.** `uk/references/regulatory-and-actuarial-references.md`
carries a "Scope note on capital" recording the SCR and MCR as **cited-not-specified**. That is no longer true: the
standard formula module tree, the scenario definitions, the loss-absorbing-capacity adjustments, the ring-fenced-fund
method, own funds tiering and the MCR corridor are specified here and in `uk/regulatory/technical-notes.md`. That scope
note should be read as superseded by this directory.

**Documents that could not be read are named at the point of use.** The largest holes, stated once here and again where
they bite. **The Annexes to the SCR – Standard Formula Part were not retrieved** [REG-R73], taking with them the Annex
XVI inputs to the health catastrophe sub-modules **and the numbered line-of-business list** that would decide whether a
UK critical illness contract is a life or a health obligation. **The four monthly PRA technical-information spreadsheets
were not opened** — the retrieval helper handles HTML and PDF only — so **no ultimate forward rate, no fundamental
spread, no volatility adjustment and no symmetric adjustment value appears anywhere in this library** [REG-R54]; the
symmetric-adjustment (SAECC) spreadsheet, published as part of the same PRA release, was separately not retrieved.
**IFRS 17 itself is paywalled and was never read** [REG-R107]; every IFRS 17 paragraph number here is one the UKEB
quotes [REG-R106]. **INSPRU 1.3.40 and 1.3.190 as at 31 December 2015 — the definitions FRS 103 anchors "realistic value
of liabilities" to — were not retrieved**, the FCA Handbook rendering INSPRU 1.3 as a "Deleted" stub [REG-R116][REG-R99].
And the library's standing **CMI restriction** applies unchanged: the current UK experience tables and the CMI Mortality
Projections Model are available only to CMI authorised users, so every mortality and morbidity basis in `uk/products/`
is an honest **[std]** proxy.

---

## Three balance sheets, one cash flow engine

One projection engine, three simultaneous measurements, each deciding something different [REG-R99][REG-R104][REG-R18].

**Solvency UK decides solvency.** Assets are measured at "the amount for which they could be exchanged between
knowledgeable willing parties in an arm's length transaction", liabilities at "the amount for which they could be
transferred, or settled" on the same basis, with **no adjustment for the firm's own credit standing** (Valuation 2.1,
2.2) [REG-R39]; technical provisions must "correspond to the current amount that the firm would have to pay if it were
to transfer its insurance and reinsurance obligations immediately to another UK Solvency II firm" (TP 2.2) [REG-R1]. It
is a **transfer-value, market-consistent** measurement.

**The statutory accounts decide reported profit.** Under UK GAAP the measurement is an entity-specific basis that FRS
103 largely **grandfathers**: it permits continuation of practices that could not be newly introduced, including
measuring insurance liabilities **undiscounted** and measuring rights to future investment management fees above fair
value (¶2.6); it permits but does not require the elimination of excessive prudence (¶2.7); and it applies a
**rebuttable presumption** that introducing future investment margins makes the statements less relevant and reliable
(¶2.8) [REG-R99]. The modified statutory solvency basis (MSSB) is named as "the established accounting treatment for
long-term insurance business" (¶3.11), with with-profits funds required to use the **realistic value of liabilities**
instead. The only measurement **floor** FRS 103 itself imposes is the liability adequacy test (¶¶2.14–2.18); a second,
non-negative / surrender-value floor comes from the non-mandatory Implementation Guidance (IG2.41, IG2.47), which
accompanies but is not part of the standard [REG-R100][REG-R101]. Under UK-adopted
IFRS 17 the measurement is instead **fulfilment cash flows plus a contractual service margin**, with an explicit risk
adjustment for non-financial risk [REG-R106].

**Tax is computed from the accounts.** Since 1 January 2013 tax trade profits are based on **accounting** profits;
before that date they were based on the insurance regulatory returns [REG-R18 LAM01100]. On top sits the FA 2012
overlay: the **I-E computation** for basic life assurance and general annuity business (BLAGAB), a trade-profit
computation for non-BLAGAB, and a split of the charge between a policyholder rate and the shareholder corporation tax
rate [REG-R17][REG-R18].

**And the fact a U.S.-trained reader will get wrong: Solvency UK owns the dividend.** CA 2006 s.830 restricts
distributions to accumulated realised profits less accumulated realised losses — but **s.830(3) makes that subject to
s.833A**, which applies to any authorised insurance company carrying on long-term business authorised under Article 14
of the Solvency 2 Directive. For such a company the realised profit or loss for s.830(2) purposes is **A − L − D** at
the balance sheet date, where A and L are the **prudential** total value of assets and liabilities and D is a deduction
list including the excess of **ring-fenced fund** assets over ring-fenced fund liabilities, and — where the firm has a
matching adjustment permission — the excess of the **assigned asset portfolio** value over the value of the MA
obligations, together with related deferred tax liabilities, plus paid-in share capital and non-distributable reserves,
an item falling in more than one paragraph being counted once (s.833A(6)) [REG-R104]. **s.833A(3) then caps** profits
available for distribution at accumulated profits (realised **or not**) less accumulated losses — so the accounts bind
the ceiling while the prudential balance sheet sets the amount. A firm outside s.833A falls under **s.843**, where an
unallocated surplus in the long-term fund shown by an annual actuarial investigation is a realised profit, a deficit a
realised loss, and otherwise long-term business profit or loss "is to be left out of account" (s.843(5)) [REG-R104].
Consequence: **a UK distributable-earnings pattern is a projection of the Solvency UK balance sheet, not of the
accounts**, plus a projection of the s.833A(5) deductions — for this library, the with-profits **ring-fenced fund
surplus** and the **MA portfolio surplus** — and then the accounts-based cap.

### Acquisition costs and DAC — the U.S. contrast, reversed

`us/regulatory/statutory-accounting-and-capital.md` opens on SSAP No. 71's rule that acquisition costs "shall be
expensed as incurred", records that there is no DAC asset in statutory accounting, and derives the first-year surplus
strain that dominates U.S. statutory model output. **That story does not transfer. It reverses.**

- **Company law requires deferral.** SI 2008/410 Schedule 3 **para 13**: costs of acquiring insurance policies incurred
  in a financial year but relating to a subsequent financial year **must be deferred**. DAC sits at assets item **G.II**
  and its movement at technical account item **8(b) change in deferred acquisition costs** [REG-R105].
- **The standard requires deferral too.** FRS 103 ¶3.7: acquisition costs "**shall be deferred**", subject to three
  carve-outs — costs already recovered, insufficient net present value of margins, and insufficiently certain future
  premiums or margins. ¶3.9 requires amortisation over no longer than the recoverability period **and in a similar
  profile to those margins**; no amortisation basis is prescribed [REG-R99].
- **The note 17 carve-out is a modelling fork.** DAC is excluded to the extent the long-term business provision (item
  C.2) or the linked provision (item D) **already allows for the costs**, by explicit recognition or implicitly through
  anticipation of future income [REG-R105]. That is how a zillmerised or gross-premium reserve absorbs acquisition costs
  **inside the liability** instead of showing an asset. It must be an explicit model configuration, not an accident of
  the reserve basis.
- **With-profits is the exception, and it is a scoped exception.** FRS 103 ¶3.10: "Acquisition costs shall not be
  deferred for with-profits funds" — so inside such a fund the strain reappears. But ¶3.1(b) applies ¶¶3.10–3.15 only to
  with-profits business and funds to which the PRA **realistic capital regime** (INSPRU section 1.3 as at 31 December
  2015) applied **before 1 January 2016**, while ¶3.7 opens "Except as required by paragraph 3.10" and IG1.1 makes ¶3.12
  optional outside that scope [REG-R99][REG-R100]. **Whether the ¶3.10 prohibition reaches a with-profits fund that was
  never in the realistic regime is not settled by the retrieved text, and neither reading is asserted here.**
- **IFRS 17 has no DAC asset either — for the opposite reason.** Acquisition cash flows sit **inside the fulfilment cash
  flows** and **reduce the CSM at initial recognition**, emerging as reduced revenue over the coverage period rather
  than as a deferred asset; the premium element intended to recover them is added back to insurance revenue with an
  equal insurance service expense. Cash flows paid before a group is recognised sit as an asset until subsumed into the
  CSM, and an asset continues for groups expected to arise from **renewals**. Under the premium allocation approach they
  may be expensed immediately where coverage is one year or less [REG-R106].
- **Solvency UK has no DAC at all.** Acquisition expenses are projected cash outflows inside the best estimate (TPFR
  16.1(4)) [REG-R41]; the Valuation Part recognises no unamortised expense asset and no goodwill (Val 8.1) [REG-R39].

So for the same cash flows a UK model produces **an accounts result with a DAC asset and no U.S.-style year-one strain**,
a **Solvency UK result with acquisition expense inside a best estimate that may itself be negative**, and under IFRS 17
a third pattern in which acquisition costs never appear as an asset but suppress the CSM. Any document in this library
carrying the U.S. "no DAC, first-year strain" framing into UK material is wrong.

---

## The Solvency UK balance sheet a model must populate

**Recognition and valuation.** Assets and liabilities are recognised in conformity with UK-adopted international
accounting standards (Val 5.1) and valued in accordance with them **provided** those standards include methods
consistent with the Article-75 standard in Val 2; where a standard allows more than one method only a Val-2-consistent
method may be used (5.2); where the standards are inconsistent with Val 2, other Val-2-consistent methods must be used
(5.3); individual assets and liabilities are valued **separately** (5.5, 5.6); and valuation is on a **going-concern**
assumption (3.1) [REG-R39].

**The UK GAAP derogation, and its limits.** Val 5.4 lets a firm use its financial-statement method for an item if **all
four** conditions hold: consistency with Val 2; proportionality to the nature, scale and complexity of the firm's risks;
the firm does not value that item under UK-adopted IAS in its financial statements; and using international accounting
standards would impose costs disproportionate to total administrative expenses [REG-R39]. SS38/15 fixes the perimeter
item by item — the derogation reaches Val 5.1, 5.2, the whole of Val 6 and the first sentence of Val 10.1, but **not**
the second sentence of Val 10.1 (the no-own-credit rule, which "cannot be derogated"), not Val 10.2, and not Val 11.2 or
11.3; Val 7, 8, 9 and 12 apply in full [REG-R40]. The verdict that matters most: **FRS 103 is never a permitted
substitute**, because "Chapters 2 to 14 of the Technical Provisions, the Technical Provisions – Further Requirements and
the Matching Adjustment Parts of the PRA Rulebook still apply" [REG-R40].

**What is and is not recognised.** Goodwill is valued at **zero**, other intangibles at zero unless separately saleable
with a value demonstrable from quoted prices in an active market (Val 8.1). **Contingent liabilities must be recognised
where material** — material meaning the information "could influence the decision-making or judgement of the intended
user … including a supervisory authority" — **irrespective of whether IAS would require recognition** (7.1–7.3), and are
measured at the expected present value of settlement cash flows using the **basic** risk-free curve, i.e. with **no MA,
no VA and no transitional**, even for a firm holding an MA permission (10.2). Cost and amortised cost are prohibited for
financial assets and liabilities (12.1). Related undertakings follow a hierarchy: quoted price, then the **adjusted
equity method**, then alternative methods only where neither is possible and the undertaking is not a subsidiary (9.1,
9.3) [REG-R39].

**Own funds.** Basic own funds = **the excess of assets over liabilities, less own shares held by the firm, plus
subordinated liabilities** (Own Funds 2.2); own funds = basic own funds plus permissioned ancillary own funds (2.1, 2.5)
[REG-R77]. Items are then tiered, participations in financial and credit institutions deducted (3K), restricted own
funds above a ring-fenced fund's or MA portfolio's notional SCR struck out (3L), and tier limits applied to give
**eligible own funds** — separately for covering the SCR and the MCR, because the limits differ. The projection model
produces only the **technical provisions leg**; everything else is asset-side or capital-management input.

**The two coverage duties.** Eligible own funds must cover the SCR and must cover the MCR [REG-R61][REG-R78]. The SCR is
calculated and reported **at least annually** (SCR-GP 4.1) and own funds cover the **last reported** SCR (4.2), but the
firm must monitor both **on an ongoing basis** (4.3) and **recalculate without delay** where its risk profile deviates
significantly from the assumptions underlying the last reported SCR (4.4) [REG-R61]. The MCR is calculated **at least
quarterly** (MCR 4.1) [REG-R78].

**There is no prescribed Solvency UK income statement.** This is where the parallel to the U.S. "balance sheet and
income statement a model must populate" breaks down, and it should be said plainly. Solvency UK is a **balance-sheet**
regime: the SCR is the value-at-risk of **basic own funds** at 99.5% over one year (SCR-GP 3.4) [REG-R61], and every
stress is a change in (assets − liabilities). The reporting layer does carry a revenue account — **IR.05.03, life income
and expenditure** — but its instruction file states it is prepared on "**financial accounting conventions**, unless
these instructions state that an item is to be reported on a Solvency II basis", following the published financial
statements with **no new recognition or re-valuation** [REG-R90]. It is a reporting template on an accounting basis, not
a prudential income statement. And the Reporting Part's Article 16, which in the EU regime carried the S.29 variation
analysis, reads "[Note: Provision left blank]" — the variation analysis has been **dropped entirely** [REG-R84]. What
substitutes for an income statement, for a large firm, is **IR.05.10 excess capital generation**, a decomposition of the
movement in *excess capital*, not of profit.

---

## Technical provisions

`technical provisions = best estimate + risk margin` (TP 2.4), valued separately except where the replication rule
applies, calculated so that the calculation "makes use of and is consistent with information provided by the financial
markets and generally available data on underwriting risks (**market consistency**)", in a "prudent, reliable and
objective manner", taking into account the Val 2 principles (TP 2.3) [REG-R1]. On PRA request the firm must demonstrate
the appropriateness of the level of its technical provisions, the applicability and relevance of the methods and the
adequacy of the statistical data (TP 14.1); the best estimate and its assumptions must be **regularly compared against
experience**, and a **systematic deviation** forces a change of method or assumptions (TP 13.1).

**The best estimate.** TP 3.1: the probability-weighted average of future cash flows taking account of the time value of
money — the expected present value using the **relevant risk-free interest rate term structure** — based on up-to-date
and credible information and realistic assumptions, using adequate, applicable and relevant actuarial and statistical
methods, and calculated **gross**, without deduction of reinsurance or ISPV recoverables, which are calculated
separately under TP 11 [REG-R1]. TP 3.2 requires **all** cash in- and out-flows required to settle the obligations over
their lifetime. Four TPFR rules do most of the work [REG-R41]. **TPFR 7.1** defines "realistic" through five conditions,
of which two bind hardest: assumptions must be based on the characteristics of the portfolio "**where possible
regardless of the firm holding the portfolio**", and firm-specific information may be used only where it **better
reflects the portfolio's characteristics** than non-firm-specific information, or where a prudent, reliable and
objective calculation is impossible without it — the rule that decides when own experience may override an industry
table, a live question for UK critical illness and income protection where the industry tables are the CMI's and are
subscriber-restricted. **TPFR 12.1** defines "credible" by consistency, objectivity, source reliability and
transparency. **TPFR 15.1** requires all uncertainties to be reflected explicitly or implicitly, including claims
inflation, expense uncertainty, policyholder behaviour, dependency between causes, and **dependency of cash flows on
circumstances prior to the date of the cash flow** (path dependency). **TPFR 19.4–19.5** force stochastic valuation: the
firm must analyse the extent to which the present value depends on **expected future outcomes and on scenario deviation
from the expected outcome**, and use a method reflecting those dependencies where it does.

**Segmentation: the technical basis, not the product label, decides.** TP 10.1 requires segmentation "into homogenous
risk groups and, as a minimum, by lines of business" [REG-R1]. The lines are those in **Annex 1** to the TPFR Part
(26.1); assignment "must reflect the **nature of the risks**… The **legal form** of the obligation **is not necessarily
determinative**" (26.2); health obligations pursued on a similar technical basis to long-term insurance business go to
the long-term lines, those on a general-insurance basis to the general lines (26.3) [REG-R41]. The four long-term lines
are **29** health insurance (long-term basis), **30** insurance with profit participation, **31** index-linked and
unit-linked insurance and **32** other long-term insurance business, with **33/34** for annuities stemming from general
insurance contracts. A contract covering both long-term and general risks **must** be unbundled (26.5); one spanning
lines, or combining health and other obligations, must be unbundled **where possible** (26.6, 26.7).

Mapping the seven library products onto those lines is **the drafter's inference from TPFR 26.2, 26.3 and the Annex 1
definitions, not a quotation** — Annex 1 names no products [REG-R41]. On that inference non-profit term assurance, whole
of life and pension annuities sit in **LoB 32**; the unit-linked bond and unit-linked whole of life in **LoB 31**;
with-profits business in **LoB 30**; and income protection and critical illness in **LoB 29** on a long-term technical
basis, or **LoB 2 / LoB 1** if not. **No retrieved source gives any test for "similar technical basis to that of
long-term insurance business"**, so two firms writing identical IP or CI books can legitimately land in different lines
— and therefore in different SCR sub-modules and different reporting rows. TPFR 20.1 separately requires long-term
projections **per policy**, or per group only where there are no significant differences in the nature and complexity of
the risks, the grouping does not misrepresent the risk or misstate expenses, and it gives approximately the same result
as a per-policy calculation "**in particular in relation to financial guarantees and contractual options**".

**Contract boundaries, and the carve-out that decides reviewable-rate protection.** Obligations are recognised at **the
earlier of** becoming a party to the contract and cover beginning, and only obligations **within the boundary** are
recognised (TPFR 2.1); all obligations relating to the contract belong to it, **including those relating to unilateral
rights of the firm to renew or extend** (3.2) [REG-R41]. TPFR 3.3 excludes cover after a future date at which the firm
has a unilateral right to terminate, to reject premiums, or to **amend premiums or benefits so that the premiums fully
reflect the risks** — unless the firm can compel payment. Limb (3) is assessed **at portfolio level**, *except* for
long-term insurance business "where an individual risk assessment of the obligations relating to the insured person of
the contract is carried out at the inception of the contract and that assessment cannot be repeated before amending the
premiums or benefits", where the firm "must assess **at the level of the contract**". Because medical underwriting
cannot be repeated at a repricing point, **a reviewable-premium critical illness or income protection policy does not
get its boundary cut at the review date merely because the firm can reprice the book** — the boundary runs to the end of
the term. TPFR 3.7 makes the test demanding in the extreme: premiums fully reflect the risks only "where there is **no
circumstance** under which the amount of the benefits and expenses payable under the portfolio exceeds the amount of the
premiums payable under the portfolio". TPFR 3.5 separately cuts future premiums out of a pure savings wrapper where
**all three** of no compensation for a specified uncertain adverse event, no financial guarantee of benefits, and no
power to compel the premium hold; both 3.3 and 3.5 ignore restrictions with "**no discernible effect on the economics of
the contract**", a phrase for which **no quantitative threshold exists in any retrieved source**. For the representative
single-premium unit-linked bond, 3.5 has nothing to operate on; for a regular-premium variant with a small death uplift
the answer is genuinely open and the matrix marks it `?`. TPFR 23.1 requires reinsurance recoverables to be calculated
**consistently with the boundaries of the underlying contracts**, so a reviewable-rate protection treaty inherits the
full-term boundary of the direct business.

**Cash flows in scope.** TPFR 13.1 requires **eight** streams relating to existing contracts: benefit payments; benefits
paid in kind; expenses; **premiums and any additional cash flows resulting from them**; **payments between the firm and
intermediaries**; **payments between the firm and investment firms in relation to index-linked and unit-linked
benefits**; salvage and subrogation; and **taxation payments which are, or are expected to be, charged to policyholders,
or are required to settle the obligations** [REG-R41]. Three consequences: intermediary payments make **commission and
clawback** an in-scope best-estimate cash flow, not an expense-loading convention; the investment-firm leg makes the
unit-fund stream explicit for the unit-linked bond; and item (8) is **policyholder-charged tax only** — shareholder
corporation tax is **not** a best-estimate cash flow, entering instead through deferred tax under Val 11 [REG-R39].
There is **no item for shareholder transfers**: for with-profits the transfer runs through TP 9.1(3) and the Surplus
Funds Part [REG-R1][REG-R45].

**Expenses, and an unreconciled tension.** TP 9.1(1) requires "all expenses that will be incurred in servicing insurance
and reinsurance obligations" and 9.1(2) requires "inflation, including expenses and claims inflation" [REG-R1]. TPFR
16.1 names four categories — administrative, investment management, claims management and **acquisition** — each
including allocated **overheads**, which must be allocated "in a realistic and objective manner and on a consistent
basis over time" (16.2). Then **TPFR 16.4**: "**Expenses must be projected on the assumption that the firm will write
new business in the future**" — so the per-policy maintenance expense is a **going-concern unit cost**, not a run-off
unit cost with overheads re-spread over a shrinking book [REG-R41]. That sits in unreconciled tension with the risk
margin: the reference undertaking "**assumes no new obligations**" after the transfer (TP 4B.1(5)) [REG-R1]. Both are
correct as printed; a model must carry **two expense bases**, and **no retrieved source explains how the reference
undertaking's expenses should be set given that tension**. Nothing in the rules prescribes an inflation index (RPI, CPI
or national average earnings), an expense-inflation rate, or a per-policy / per-premium split; those are **[std]**
choices made in the per-product technical notes.

**Options, guarantees, management actions and policyholder behaviour.** TP 9.2(1) requires the value of financial
guarantees and contractual options to be taken into account; 9.2(2) requires assumptions on the likelihood of exercise,
**including lapses and surrenders**, to be realistic and based on current and credible information, and to take into
account "either explicitly or implicitly, the impact that future changes in financial and non-financial conditions may
have on the exercise of those options" [REG-R1]. TPFR 11.1 requires **an analysis of past policyholder behaviour and a
prospective assessment**, taking into account how beneficial exercise was and will be under the circumstances at the
time, past and future economic conditions, past and future management actions, and any other relevant circumstances —
and closes: "**The likelihood shall only be considered to be independent of the elements referred to in (1) to (4) where
there is empirical evidence to support such an assumption**" [REG-R41]. That sentence is **the rule against a flat,
static lapse table**: a constant assumption is permitted only on evidence that behaviour is genuinely independent of
moneyness, economics and management action. For a guaranteed-annuity-option-bearing whole of life or with-profits
contract, or a guarantee-bearing unit-linked bond, that evidence will not exist and a **dynamic lapse function is
required**; for a term assurance with no surrender value, independence is far easier to sustain.

Future management actions are governed by TPFR 8: assumptions are realistic only where determined objectively,
**consistent with current business practice and business strategy**, consistent with each other, **not contrary to any
obligations towards policyholders or to legal requirements**, and taking account of **any public indications by the
firm** as to what it would or would not do [REG-R41]. A **comprehensive future management actions plan approved by the
governing body** is required, covering the actions, the circumstances in which each would be taken, **the circumstances
in which the firm may not be able to take each and how those are reflected in the calculation**, the **order** of
actions, the work needed to be able to carry them out, how they are reflected in the best estimate, and internal
reporting with at least an annual communication to the board (8.3, 8.5); assumptions must take account of **the time
needed to implement** the actions and **any expenses caused by them** (8.4). For with-profits this is where the PPFM
enters the valuation — the With-Profits Actuary must advise the governing body whether the assumptions used to calculate
future discretionary benefits within technical provisions **are consistent with the firm's PPFM** (Actuaries 5.1(2))
[REG-R93][REG-R9].

**Future discretionary benefits are a separate required output.** TPFR 10.1: "a firm must **determine separately the
value of future discretionary benefits**". Where FDB depend on the assets held, the best estimate must be based on **the
assets the firm currently holds**, with allocation changes assumed only per TPFR 8, and assumed future asset returns
consistent with the relevant risk-free curve (including any MA, VA or risk-free transitional) and with the Valuation
Part measurement of the assets (9.1) [REG-R41]. That **forbids an assumed equity risk premium in a with-profits
projection**: returns are risk-neutral off the relevant curve and the asset mix starts from the actual portfolio. The
separately-determined FDB amount is used three more times downstream — as the cap on the loss-absorbing capacity of
technical provisions, in the ring-fenced-fund SCR adjustment, and as the MCR's `TP_l2` term [REG-R62][REG-R78].

**Reinsurance recoverables and the counterparty default adjustment.** TP 11.1 requires recoverables to be calculated on
the **same** apparatus as the gross best estimate, to reflect "the time difference between amounts becoming recoverable
and the actual receipt of those amounts", and to be **adjusted for expected losses due to counterparty default** on an
assessment of probability of default and average loss [REG-R1]. TPFR 23.2 requires recoverables from **SPVs**, from
**finite reinsurance contracts** as defined in Conditions Governing Business 8.1, and from **other reinsurance
contracts** each to be calculated **separately**, with the SPV recoverable capped at that SPV's aggregate maximum risk
exposure [REG-R41][REG-R92]. TPFR 24 governs the adjustment: calculated **separately** from the recoverables (24.1), as
the expected present value of the change in cash flows on default, **ignoring risk-mitigation techniques other than
collateral** (24.2), over the lifetime of the contract and allowing for how the probability of default varies over time,
**separately by counterparty and by line of business** (24.3). And 24.4 is **the only hard numeric floor in the whole
technical-provisions apparatus**: the average loss "**must not be assessed at lower than 50% of the amounts
recoverable** … **unless there is a reliable basis for another assessment**". **What counts as a "reliable basis" is not
settled by any retrieved source.** Two supervisory overlays sit on top: SS5/24 on funded reinsurance, with its
immediate-recapture metric and worst-case collateral assumptions inside an MA portfolio [REG-R47], and SS18/16 on
longevity risk transfers, which observes that SCR counterparty default capital "may not be sufficient in and of itself"
[REG-R48] — **SS18/16 was read only at grep level and everything about it beyond that observation is [unverified]**.
Whether a treaty is admissible as a **risk mitigant in the SCR** is a separate question from the recoverable, governed
by **SCR-SF Chapter 3G** and set out under "The solvency capital requirement" below [REG-R62].

**Technical provisions as a whole are effectively unavailable to life business.** TP 2.5(2) requires TP to be determined
as the market value of replicating financial instruments where cash flows can be **replicated reliably** by instruments
with a **reliable, observable market value** [REG-R1]. TPFR 22.2 supplies the test — replication is reliable only where
the cash flows are replicated "**in amount and timing** … and **in all possible scenarios**" — and declares three
categories non-replicable: cash flows depending on the likelihood that policyholders exercise contractual options,
**including lapses and surrenders**; cash flows depending on the level, trend or volatility of **mortality, disability,
sickness and morbidity rates**; and **all expenses** incurred in servicing the obligations [REG-R41]. Every product here
carries expenses, and every one carries either biometric dependence or an exercisable option, so **TP-as-a-whole is
unavailable for the whole-contract valuation of all seven**. The residual use is for a *component* — the unit-fund
liability of a linked contract, in principle replicable by the units held — while charges, expenses, the mortality
element and any guarantee remain a separate best estimate. The reporting layer expects any TP-as-a-whole amount to be
reported **inside** gross best estimate (IR.12.01 rows R0025/R0026/R0030), so the split is a disclosure attribute, not a
separate liability line [REG-R89]. One conflict is recorded and not resolved: the Glossary defines *market value* by
reference to "generally accepted accounting practice" [REG-R43] while Val 2.1 states the Article-75 standard and Val
12.1 forbids cost and amortised cost [REG-R39]; TPFR 22.3–22.4 use *market value* for the TP-as-a-whole valuation, and
the two anchors are not reconciled in the retrieved text.

### There is no floor on a negative best estimate

Settled from the rules, and the single most important UK/U.S. divergence for protection business. Profitable protection
— term assurance, critical illness, level-premium whole of life in its early years — routinely produces a **negative**
best-estimate liability, because the present value of future premiums inside a full-term boundary exceeds the present
value of future claims and expenses. Nothing floors it [REG-R1][REG-R39][REG-R41]: **TP 3.1** contains no floor, no
minimum and no reference to a surrender value or account value; **TP 2.2** requires a **transfer value**, which for a
profitable portfolio is legitimately negative before the risk margin; **TP 2.4** adds a risk margin that is **always
non-negative by construction**, so it offsets but does not floor; a full-text search for "negative" across the
**Valuation, Technical Provisions and TPFR Parts** returns exactly one hit, TPFR 25.2's EUR-peg currency adjustment,
which "must be negative"; **Val 5.5/5.6** require separate valuation of individual assets and liabilities but **Val 4.1
expressly excludes technical provisions from Chapters 5 to 12**, so no contract-level floor is imported; and the
reporting layer treats **surrender value as a disclosure item**, IR.14.01 carrying "Surrender value — the amount of
surrender value net of taxes" as information rather than a constraint [REG-R89]. Three product-side confirmations were
recorded: the Solvency I floor (INSPRU 1.2.62R) was **expressly not carried over**, INSPRU 1.2 not applying to a
Solvency II firm [REG-R115]; a secondary source states "there is no floor related to the surrender value specified in
the rules" [REG-R118] — **an entry with no recorded URL, cited without one rather than with a guessed one**; and the
reporting treatment above.

**The other two ledgers do floor it, which is why a UK model carries three liability measures.** UK GAAP: FRS 103
implementation guidance **IG2.41** — "no policy may have an overall negative provision except as allowed by PRA rules,
nor a provision less than any guaranteed surrender or transfer value" — and **IG2.47**, the same for a linked provision
measured by reference to the relevant fund or index [REG-R100]. **IFRS 17**: fulfilment cash flows may be negative, but
a group cannot carry a negative CSM — that is what makes a group onerous and creates a loss component [REG-R106]; *this
sentence is a comparison drawn by the drafter, not a claim sourced from retrieved IFRS 17 text*. So a UK insurer reports
**a negative best estimate on the Solvency UK balance sheet and a floored provision on the same business in its
accounts**. Per product, on the Solvency UK ledger [REG-R41][REG-R115]: term assurance and critical illness routinely
negative at issue; income protection negative for the active-life cell, never for claims in payment; whole of life
cell-dependent, the over-50s guaranteed-acceptance cell being the paradigm lapse-supported negative reserve;
with-profits normally not, guaranteed benefits plus FDB dominating; the unit-linked bond's **non-unit ("sterling")
component commonly negative** while the total is positive; and a pension annuity in payment never, having no future
premium inside the boundary. Two things are sometimes mistaken for a floor: the **contract boundary**, which for
reviewable-rate protection generally stays open under the TPFR 3.3 carve-out and so is not a back-door floor; and the
**reconciliation reserve**, which Own Funds 3C.2 states "may be positive or negative" [REG-R77] — a negative best
estimate therefore feeds own funds directly, subject to tiering, the RFF deduction and any MA-portfolio restriction.

**Data quality and proportionality.** Data must be "appropriate, complete and accurate" (TP 12.1), with approximations
including case-by-case approaches permitted where data of appropriate quality is insufficient (TP 12.2) [REG-R1]. TPFR
4.1–4.3 define each term; **complete** requires "sufficient historical information to assess the characteristics of the
underlying risks **and to identify trends**", available per homogeneous risk group. **External data** carries four extra
conditions, two of which bind a UK model directly: the firm must know the **origin** of the data and the assumptions and
methodologies used to process it, and must demonstrate that those **reflect the characteristics of its own portfolio**
(4.4) [REG-R41] — the rule a firm must satisfy to use a CMI table or an industry IP inception basis. TPFR 5.1 requires a
documented **limitations register** with a remediation plan, a named responsible function, and retention of the
pre-adjustment data. TPFR 27 governs proportionality: methods must be proportionate to the nature, scale and complexity
of the risks, and a method is **disproportionate** where the error could influence the intended user's decision-making
— **unless** no method with a smaller error is available and the method is not likely to underestimate, or the method
produces **higher** technical provisions than a proportionate method would. In short, a simplification is permitted
where it is not possible to do better, or where it is demonstrably prudent. **There is no "immaterial, therefore ignore"
limb.**

---

## Discounting: risk-free rates, the matching adjustment, and the transitionals

**One cash flow vector, several curves.** The best estimate is discounted at the *relevant* risk-free interest rate term
structure (TP 3.1) [REG-R1], but "relevant" is a family. A UK model must produce, from a single projection, the best
estimate on the **basic** curve, on **basic + matching adjustment**, on **basic + volatility adjustment** and on
**basic + the transitional adjustment to the risk-free rate**; and separately apply the **transitional measure on
technical provisions** as an adjustment to technical provisions rather than to a discount rate. The discounting step
must be separable from the projection step, with the curve an input parameter rather than a hard-coded assumption.

**The curve is published, not computed by the firm.** IRPR regulation 3(1) obliges the PRA to publish, **every
quarter**, a fundamental spread per currency, duration, credit quality and asset class and such other technical
information as it considers appropriate — the term structure among it; the PRA in fact publishes **monthly, on or
before the eighth working day of the following month**. The statutory frequency and the actual frequency differ and the
difference is recorded here rather than resolved [REG-R44][REG-R54]. A firm has **no discretion
over the curve** for a PRA relevant currency; SoP 1/20 leaves it responsible for proposing technical information only in
a currency the PRA does not publish, and a volatility adjustment may only be applied in a currency for which the PRA
publishes one [REG-R55]. Each release contains the basic curve, a VA-adjusted curve, **fundamental spreads,
probabilities of default and cost of downgrade** by currency, duration, credit quality step and asset class, and
Smith-Wilson extrapolation parameters [REG-R54]. **The matching adjustment is never published**: the PRA publishes the
fundamental spread and the firm computes its own MA from its own assigned assets. The basic curve is derived from
**interest rate swap rates** adjusted for credit risk, falling back to government bond rates for maturities where swaps
are not available from a deep, liquid and transparent (DLT) market, the **credit risk adjustment being permitted to be
zero** where negligible [REG-R55]. For **GBP the reference instrument is SONIA overnight index swaps with a zero credit
risk adjustment** from reference dates in July 2021; for **USD, SOFR swaps with a zero adjustment** from 1 January 2023;
PRA relevant currencies from 1 January 2025 are **GBP, USD, EUR and CAD only** [REG-R54]. **The EUR and CAD credit risk
adjustments were not retrieved and no basis-point value for either is stated here.**

**Extrapolation and the last liquid point.** TP 5.1 requires the curve to take account of maturities where markets for
the relevant instruments *and for bonds* are DLT and to be **extrapolated only** where they are not; TP 5.2 requires
forward rates converging smoothly to an **ultimate forward rate** [REG-R1]. The DLT assessment fixes that boundary on
verified quantitative criteria — average daily notional turnover of at least **GBP 45 million** and an average of at
least **10 trades per day**, each over one year, with a 20% hysteresis band in both directions, all treated as soft
thresholds alongside other metrics and expert opinion [REG-R55]. The 2025 assessment (EMIR trade repository data to 31
July 2025, published 28 November 2025, effective 1 January 2026) retained **GBP LLP = 50 years** — despite failing the
trade-count indicator, on bid-ask evidence and stability grounds — and **EUR LLP = 20 years** [REG-R56]. **The USD and
CAD last liquid points were not reliably extracted from the published table and are not stated here**, nor is any
per-maturity DLT flag for any currency. So GBP liabilities are discounted at observed rates over essentially their whole
term, the UFR biting only beyond year 50, whereas a EUR book extrapolates from year 20: **a model that hard-codes a last
liquid point hard-codes a currency**. The UFR methodology is described in SoP 1/20 — long-term real rate expectations
plus expected inflation, kept stable, EIOPA's UFR-2024 methodology, **no term premium** — but **no numeric UFR,
convergence period or Smith-Wilson alpha was retrieved and none is stated anywhere in this library** [REG-R55][REG-R54].

### The matching adjustment

**Permission.** A firm must not apply an MA without a **matching adjustment permission** (MA 2.1) and, having applied it
to a portfolio, **must not revert** (3.2) [REG-R2]; the permission is a s.138BA FSMA waiver granted so the firm may
apply the MA in accordance with IRPR regulation 4(1) [REG-R44][REG-R60].

**Matching conditions (IRPR reg 4)** [REG-R44]: assign a portfolio of **bonds or other assets with similar cash flow
characteristics** to cover the best estimate; assess asset credit quality by a credit rating or an internal assessment
of comparable standard; **maintain the assignment over the lifetime** of the obligations; **identify** the obligation
portfolio and assigned assets and **organise and manage them separately**; ensure asset cash flows **replicate each of**
the obligation cash flows **in the same currency**; keep any mismatch immaterial; and ensure asset cash flows are
**fixed and not changeable** by issuers or third parties, subject to three exceptions — immaterial matching-quality risk
affecting only a limited proportion, inflation-linked assets matching inflation-linked liabilities, and **sufficient
compensation** permitting reinvestment in an asset of equivalent or better quality.

**Liability conditions (MA 2.2)** [REG-R2]: **no future premium payments**; the only underwriting risks connected to the
portfolio are **longevity, expense, revision, mortality or recovery time risk**; where mortality risk is present the
best estimate **must not increase by more than 5%** under the prescribed mortality stress; **no policyholder options, or
only a surrender option whose surrender value does not exceed the value of the covering assets**; the assigned assets
cannot be used to cover losses from other activities; and the portfolio **and every individual asset in it** satisfies
the prudent person principle. Obligations of a contract **must not be split** other than for an **eligible element**
(2.3), and SS7/18 adds that outside those cases the PRA regards no notional splitting as compatible with 2.3 [REG-R8].

**The eligible-element route is what lets non-annuity products in.** An *eligible element* is a portion of obligations
within a wider contract which is either **the guaranteed element of a with-profits immediate or deferred annuity** or
**the in-payment element of a group death-in-service dependants' annuity or an income protection policy**, separately
organisable and manageable under IRPR reg 4(6), and otherwise MA-eligible but for forming part of a non-complying
contract (MA 1.2) [REG-R2]. The "no future premiums" condition is **disapplied for the in-payment limb** (2.5) but
**not** for the with-profits guaranteed annuity element, which must still be premium-free. SS7/18 adds that **recovery
time risk** — "the risk that policyholders in receipt of income protection payments take longer to recover from sickness
than expected" — is a permitted underwriting risk; that in-payment claims under **both group and individual** IP
policies may sit in an MA portfolio where not subject to future premiums; that **there is no exposure limit on recovery
time risk**, in contrast to the 5% mortality cap; and that the recovery-time permission is **not** intended to admit any
liability type other than IP claims in payment [REG-R8]. For a with-profits guaranteed annuity element the PRA expects a
detailed assessment that only contractually guaranteed elements are included and are not dependent on future premiums or
investment performance, plus **a clear policy on where future attaching bonuses go** [REG-R8]. **How a firm allocates a
single liability cash flow vector between MA and non-MA portfolios when only an eligible element qualifies is not
prescribed by any retrieved source** — for a with-profits model this is the crux, and the sources do not say how the
asset share follows the guaranteed element.

**Asset eligibility has no closed list.** It turns on the asset's features plus the firm's ability to identify, measure
and manage its risks under the prudent person principle: "there is no prescribed 'closed list' of eligible assets for MA
purposes", and firms must test **all** features against **all** conditions [REG-R8]. Outside the highly-predictable
carve-out the firm must show cash flows are fixed in timing and amount — "it is not sufficient for a portfolio of assets
to provide cash flows that are predictable in aggregate to a very high degree" [REG-R8]. **Highly predictable (HP)** is
the 2024 reform's addition: cash flows are highly predictable where the contractual terms provide a **bounded range of
variability** in timing and amount and **failure to meet those terms is a default** (MA 5.3), and **no more than 10% of
the MA benefit** may be attributable to HP assets individually or in aggregate (5.2) [REG-R2]. "MA benefit" for that cap
is defined by 5.5 as the impact on the best estimate of the Conditions Governing Business 3.2(2)(c) scenario — **a
different quantity from the basis-point "MA benefit" SS7/18 uses in its matching tests, and a drafter must say which is
meant** [REG-R2][REG-R8]. **Decomposing a single asset into fixed and HP components is not permitted.** Equity release
mortgages get an explicit warning: the typical combination of longevity, morbidity, realisable property value under a
no-negative-equity guarantee and prepayment risk is "unlikely to be compatible with the general requirement for fixed
cash flows", leaving restructuring, pairing or the HP route inside the 10% cap [REG-R8].

**The calculation, and the fundamental spread.** MA 4.3, replicating IRPR reg 5(1), makes the MA **the difference of two
internal rates of return on the same liability cash flow vector**: the single annual effective rate that values the
obligations at the value of the **assigned assets**, minus the rate that values them at the best estimate on the
**basic** curve [REG-R2][REG-R44]. Assigned assets include **only** assets required to replicate the liability cash
flows, excluding any excess (4.4). Asset cash flows are **de-risked first** for probability of default (4.5), and the
**fundamental spread** — compensation for risks the firm retains — is then deducted, only to the extent not already
reflected in the cash-flow adjustment, so the default element is not double-counted (4.6–4.7). The fundamental spread is
a probability-of-default spread plus a cost-of-downgrade spread, subject to a long-term-average-spread floor of **30% of
the average spread for UK central government and Bank of England exposures and 35% for all other assets**; SoP 1/20
records the UK deviation that since 31 March 2022 the 30% floor applies **only** to UK central government and central
bank exposures, no longer to EEA exposures [REG-R2][REG-R55]. Fundamental spreads must be **notched** within a credit
quality step by linear interpolation between consecutive CQS pairs, assuming intermediate notches are evenly spread, for
assets mapping to CQS 1 to 5; notching has been **mandatory since 31 December 2024**, a derogation having run only from
30 June 2024 to that date [REG-R2]. **Fundamental spreads vary by maturity of cash flow for a given asset**, and SS7/18
states expressly that "simplifications, for example using a single FS based on the duration of the asset, would be
inconsistent with the way in which the FSs are intended to be applied in practice" [REG-R8]. **No fundamental spread,
probability of default or cost-of-downgrade figure appears anywhere in this library** — they are the contents of a
monthly spreadsheet that was not opened [REG-R54].

**Demonstrating matching.** For IRPR reg 4(7) the firm runs a quantitative cash-flow projection measuring the surplus or
deficit **in each future period**; for reg 4(8) a quantitative assessment of the interest rate, currency, inflation and
other mismatch risks [REG-R8]. SS7/18 offers a component **A/B/C** decomposition as "one possible method", not a
mandate, and sets projection conventions that are model rules: **assume no future management actions**; assume all
non-HP asset cash flows arrive on their contractual dates; surplus assets may **not** be assumed reinvested and realised
later; **cash used to demonstrate matching is assumed realised in full in year 1**; and tests are run **net of
reinsurance** in both numerator and denominator [REG-R8]. The **five PRA Matching Tests** then apply — Tests 1–3 to all
MA firms, Tests 4 and 5 additionally where HP assets are held — with statistics, thresholds and frequencies in
`uk/regulatory/technical-notes.md`, "Discount curves". Two cautions the SS itself records: the Appendix warns that the
PRA "has described other versions of these tests in previous communications", so any reference must be dated; and the
profile minimising MA benefit under Test 4 need not be the profile producing the greatest reinvestment risk. **Whether
the risk-free rate used in the accumulation step of Tests 1 and 5 is the basic curve or basic-plus-MA is not stated** —
the natural reading is basic, since Test 2's denominator is explicitly basic-plus-MA, but the Appendix does not say so.

**The attestation.** A firm with an MA permission must attest, **in respect of each relevant portfolio of assets as a
whole**, that the fundamental spread used **reflects compensation for all retained risks** and that the MA **can be
earned with a high degree of confidence** from the assets held (MA 9.1) [REG-R2]. Timing: **annually, no later than 14
weeks after financial year-end**, the reference date being the effective date of the SFCR; and additionally on a
**material change in the firm's risk profile**. The attestor is the senior manager holding the prescribed responsibility
for the production and integrity of financial information and regulatory reporting — SS7/18 says "in many cases, this
will be SMF 2, the Chief Financial Officer", and where more than one senior manager holds it **all of them are expected
to attest** [REG-R8]. A governing-body-approved **attestation policy** is required (10.3), and the supporting report
must list the evidence relied on and, for any **voluntary fundamental-spread increases**, the assets affected, the
reasons, the amount and the resulting MA (12.3). The PRA expects the FS and the MA to be **reviewed independently of
each other**, so the MA acts as a market-based check on the FS, and expects analysis at the level of the **individual
asset** — "a firm must not assume prudence on one asset can offset an insufficient FS on another" [REG-R8]. Four of the
SS's materiality metrics for that review are left as **bracketed placeholders `[w]`, `[x]`, `[y]`, `[z]` which the PRA
does not fill in**; no value is invented here. The firm must disclose in its SFCR **whether or not it has attested**
(11.1), while the report's content goes to the PRA and is **not** publicly disclosed.

**MAIA and breach.** The Matching Adjustment Investment Accelerator, effective **27 October 2025**, lets a firm holding
both an MA permission and a **MAIA permission** place assets with features outside the scope of its MA permission into
the portfolio and claim MA benefit immediately, before applying to vary the permission; only a *qualifying new asset*
may go in, and within **24 months** the firm must apply to vary the permission or remove the asset, supported by a
written **contingency plan for each and every new asset**, a board-approved MAIA policy and an annual **use report**
[REG-R2][REG-R8]. The exposure limit is **absolute**, assessed on total nominal investment amount, and the PRA expects
it to be the lower of **5% of the MA portfolio's best estimate liabilities net of reinsurance** and **an amount proposed
by the firm no greater than GBP 2 billion**, aggregated across a group [REG-R8]. Separately, the MA eligibility
conditions and permission terms must be met **at all times**; if compliance is not restored **within two months** a
monthly reduction formula bites, extinguishing the MA after ten further months (MA 13.2–13.5) [REG-R2] — the formula is
in `uk/regulatory/technical-notes.md`. One capital-modelling point: **where the MA is reduced for a breach, the PRA does
not expect the firm to recalculate the SCR or alter internal-model management actions**; the own-funds loss over twelve
months continues to be based on balance-sheet movements ignoring the reduction [REG-R8].

### The volatility adjustment

A firm may apply a VA **only** where it holds a **volatility adjustment permission**, the VA has been published by the
PRA under IRPR reg 3, and only to the extent of that permission (TP 8.1) [REG-R1][REG-R44]. The VA **must not be applied
to extrapolated rates** (8.2), while the extrapolation itself **must be based on the VA-adjusted rates** where a VA
applies (8.3). Read with SoP 1/20's statement that the PRA "will apply extrapolation after applying the volatility
adjustment to the basic RFR", the operative meaning is that the VA is added to the liquid segment and the extrapolation
converges to the UFR from the VA-adjusted forwards — **the Rulebook never says so in terms, and 8.2 quoted in isolation
reads as a flat prohibition it is not** [REG-R55]. The VA and MA are **mutually exclusive at the level of the
obligation, not the firm**: TP 8.5 bars the VA where the curve already includes an MA, and MA 13.3 bars a VA or a
risk-free transitional on MA obligations [REG-R1][REG-R2] — so one entity may run an MA portfolio and a VA-discounted
remainder simultaneously. The PRA derives the VA per currency as **0.65 × the risk-corrected currency spread** on a
reference portfolio, the risk correction computed in the same manner as the fundamental spread under IRPR regs 6(1)–(8)
[REG-R55][REG-R44]. **No VA value for any currency or date is stated in this library.** Two 2026 changes are recorded:
for **GBP the PRA now excludes MA-eligible life annuity liabilities from the VA reference portfolio**, since firms
cannot use the VA and MA simultaneously; and the PRA identified an **error in the unit-linked reduction factors** used
in reference-portfolio derivation, estimating on 31 March 2025 data that correction would have **reduced published VAs
by up to 5bp (GBP) and up to 1bp (other currencies)**, judged the effect immaterial, corrected prospectively from 31
March 2026 and **will not restate** earlier published VAs [REG-R54].

### The transitionals

**TMTP.** Applicable only with a **TMTP permission**; a firm with one **must not apply** the risk-free transitional; and
**a firm must not apply TMTP after 1 January 2032** (2.1–2.3) [REG-R3]. It reaches only obligations that were the firm's
*qualifying* obligations **on 31 December 2024**, or obligations assumed after that date through a **transfer event**
(2.4), and the firm must disclose in its SFCR that it applies TMTP and **quantify the impact of not applying it** (3.1).
Structurally it splits into a **risk-margin portion**, a **dynamic portion** (the best estimate of designated MA-eligible
obligations, net of recoverables) and a **non-dynamic portion**, with a one-off base calculation anchored at 31 December
2024 against a **Solvency I INSPRU 7** comparator — the only place the old regime survives — and a running calculation
in which the non-dynamic part amortises deterministically and linearly over seven years while the risk-margin and
dynamic parts are re-struck each period as constant proportions of the then-current risk margin and dynamic best
estimate, so they **move with markets and with the liability run-off**; a run-off accelerator forces those two parts to
zero by 1 January 2032 [REG-R3]. **TMTP is a range, not a point**: the rule caps but does not fix the amount, and a firm
applying less than the maximum must **disclose both the maximum and the actual amount**, apply the choice consistently
across templates, ORSA, risk management and market disclosures, and never disclose a solvency ratio allowing for more
than the maximum [REG-R59]. The arithmetic is in `uk/regulatory/technical-notes.md`, "Discount curves". The calculation
is **overseen by the Chief Actuary**, who also selects the methodology for **projecting** the risk-margin and dynamic
portions to 2032, consistent with TPFR Chapter 27 [REG-R59].

**TMIR.** Applies only to *admissible* obligations — contracts concluded **before 1 January 2016**, whose technical
provisions were determined under INSPRU 1.1.16R as at 31 December 2015, and which are **not subject to an MA
permission** — and requires a s.138BA permission [REG-R57]. The adjustment is a linearly-decreasing portion of the
difference between an INSPRU-basis rate frozen on the 31 December 2015 basis and the annual effective rate reproducing
the Solvency II best estimate, so a TMIR firm runs a **dual-basis valuation**. Where the firm applies the VA, the
Solvency II leg is computed on the VA-adjusted curve and **the VA is not added again on top** [REG-R57][REG-R59]. A TMIR
firm must exclude the admissible obligations from the VA calculation, **must not apply TMTP**, and must make the same
SFCR disclosure and impact quantification. Both transitionals carry a phasing-in duty: notify the PRA immediately on
observing that the SCR would not be met without the measure, comply with the SCR **by 1 January 2032**, submit a plan
within two months, and report annually [REG-R3][REG-R57].

**The exclusivity map**, all verified from rule text [REG-R1][REG-R2][REG-R3][REG-R57][REG-R59]: MA and VA — no; MA and
TMIR — no; MA and TMTP — **yes**, the TMTP base calculation explicitly takes the MA into account; VA and TMIR — yes but
only once, the VA being embedded in the TMIR calculation; VA and TMTP — yes; TMTP and TMIR — no, in both directions;
and **none of the four inside the risk-margin reference undertaking**.

---

## The risk margin

**The concept.** TP 4.1: the risk margin is "an amount equal to the cost that a UK Solvency II firm would incur in order
to hold eligible own funds to cover the SCR necessary to support the insurance and reinsurance obligations over their
lifetime", determined using the cost-of-capital rate; TP 4.2 requires the technical provisions to equal what such a firm
"would be expected to require in order to take over and meet" the obligations [REG-R1]. The cost-of-capital rate is
**4%**, stated in TP 1.2 by reference to IRPR reg 7B(b) [REG-R1][REG-R44], and the formula carries a **tapering factor
λ = 0.9 for long-term obligations and 1.0 for general insurance obligations, floored at 0.25** [REG-R4]. Those
parameters arrived with SI 2023/1346, in force **31 December 2023**, which cut the cost-of-capital rate from 6% to 4%
and introduced the taper [REG-R4]. The formula as printed in TP 4A.1, its discounting convention and its currency rule —
the **basic** curve in the currency of the firm's **financial statements**, not of the obligations — are in
`uk/regulatory/technical-notes.md`, "The risk margin".

**The reference undertaking's thirteen assumptions, and what they exclude.** TP 4B.1 defines a hypothetical firm taking
over the whole portfolio; a **composite splits into two reference undertakings**. It has **no obligations and no own
funds before the transfer**; **assumes no new obligations after it**; raises eligible own funds equal to its notional
SCR; holds assets equal to that notional SCR plus its technical provisions net of recoverables; and selects those assets
"in such a way that they **minimise the reference undertaking notional SCR for market risk**" [REG-R1]. Its notional SCR
captures **underwriting risk** on the transferred business, **market risk other than interest rate risk** where
material, **credit risk** on reinsurance, SPVs, intermediaries, policyholders and other closely-related exposures, and
**operational risk** — and nothing else. It carries the **loss-absorbing capacity of technical provisions** matching the
firm's, per risk, but **no loss-absorbing capacity of deferred taxes**. It adopts future management actions consistent
with the firm's under TPFR 8, subject to writing no new business. And it applies **none of** the MA, the VA, the
risk-free transitional or the TMTP.

Three consequences a model owner must not blur. **The risk margin is not the firm's own SCR run-off** — it is a
*different* undertaking's SCR run-off on the basic curve with a deliberately restricted risk scope, so for an MA-heavy
annuity book the risk margin is struck on a materially higher-liability basis than the balance sheet it sits on. The
exclusion of interest rate risk and of deferred-tax loss absorbency, combined with the minimise-market-risk asset
selection, means it **cannot be produced by re-running the firm's own SCR on a different curve**. And the calculation is
for the **whole portfolio**, then **allocated** to lines of business so as to "adequately reflect the contributions of
the lines of business to the reference undertaking notional SCR over the lifetime of the whole portfolio" (TP 4A.3) —
**no allocation formula is prescribed** [REG-R1]. A firm with internal model permission must use that model for the
notional SCR "**unless it is inappropriate to do so**" (TP 4A.2).

**Why it is a projection problem.** The formula sums a discounted, tapered stream of notional SCRs indexed by integer
year, so the model must produce `SCR(0), SCR(1), SCR(2), …` — a **projected run-off of a capital requirement**, not a
valuation-date number.

**And the Delegated Regulation's simplification hierarchy was NOT restated into UK rules.** The revoked DR (EU) 2015/35
contained Article 57 (simplified recoverables), **Article 58 (simplified calculation of the risk margin)**, Article 59,
Article 60 and Article 61 [REG-R49]. In the restated TPFR Part the heading "SIMPLIFICATIONS" introduces **Chapter 27
(Proportionality) only** — 27.1 to 27.4 and nothing else [REG-R41][REG-R42]. **The EIOPA hierarchy of risk-margin
methods (methods 1 to 4) has no UK rule text.** What survives is the general proportionality test in TPFR 27 and **IRPR
regulation 7C**, which preserves the PRA's *power* to make rules permitting simplified risk-margin methods — a power
that, on the Rulebook text retrieved on 2026-08-06, **has not been exercised in the Technical Provisions Parts**
[REG-R44]. A UK model that needs `SCR(t)` must therefore project the reference undertaking notional SCR directly or
justify its own driver-based proxy against TPFR 27.4. **No rule text sanctions any specific proxy**, and how `SCR(t)`
should be projected in practice is a question the retrieved sources do not settle.

Two smaller points. A **capital add-on** imposed for a significant *system of governance* deviation is **excluded** from
the SCR for risk-margin purposes; an add-on for a *risk profile* deviation is **not** (SCR-GP 5.3) [REG-R61]. And the
IR.12.01 instruction file permits **SS8/24 §3.2** to be applied to calculate the risk margin during the financial year
[REG-R89] — **SS8/24 was not retrieved and its title is not asserted here**.

---

## The solvency capital requirement

**Calibration and scope.** The SCR "must correspond to the **value-at-risk of its basic own funds subject to a
confidence level of 99.5% over a one-year period**" (SCR-GP 3.4), imposed module by module by SCR-SF 3.3
[REG-R61][REG-R62]. The object is **basic own funds**: every stress is a loss in (assets − liabilities). The SCR covers
at least non-life, **life**, **health**, **market**, **credit** and **operational** risk, covers existing business **and
new business expected to be written over the following 12 months**, and for existing business covers **only unexpected
losses** (3.3). Two carve-outs: it **must not cover the risk of loss of basic own funds resulting from changes to the
volatility adjustment** (3.6) — and there is **no corresponding carve-out for the matching adjustment**, MA movements
being expressly in scope. A firm calculates the SCR **either** by the standard formula **or** by a permissioned internal
model (3.1); there is no third option, and undertaking-specific parameters are a parameter substitution *inside* the
standard formula [REG-R61][REG-R65].

**Risk mitigation has to earn its recognition — the UK analogue of the U.S. risk-transfer gate.** Risk-mitigation
techniques may be recognised in the SCR **only where the credit and other risks they create are reflected** (SCR-GP 3.5)
[REG-R61], and the conditions a reinsurance arrangement, SPV or financial technique must satisfy sit in **SCR-SF Chapter
3G** — `3G2` qualitative criteria, `3G3` effective transfer of risk, `3G4` material basis risk, `3G5` reinsurance and
SPVs, `3G6` financial risk-mitigation techniques, `3G7` status of the counterparties, `3G8` collateral arrangements,
`3G9` guarantees [REG-R62]. Two operative points are verified. Where a reinsurance contract or SPV **meeting `3G2`,
`3G5` and `3G7`** protects across several of the `3A`–`3C` scenario calculations, its risk-mitigating effect must be
**allocated across those calculations without double-counting**, the economic effect captured in each determination of
the loss in basic own funds (`3G1.1`). And **finite reinsurance** is recognised in the `3A`–`3C` scenarios only to the
extent underwriting risk is actually transferred, and **must not be taken into account at all** in the `3A2` / `3C3`
premium and reserve volume measures or in calculating USPs (`3G1.2`) [REG-R62][REG-R65]. **The detailed criteria in
`3G2`–`3G9` were surveyed and not transcribed, so no `SCR-SF 3G` test is stated in this library** — a treaty that fails
them reduces neither the SCR nor, under MCR 3C.2, the recoverables netted in the linear MCR [REG-R78].

**The module tree.** `SCR = BSCR + SCR_operational + Adj`, `Adj` being the adjustment for the loss-absorbing capacity of
technical provisions and deferred taxes, **negative or zero** (SCR-SF 2.1) [REG-R62]. The BSCR aggregates market,
counterparty default, life, health and non-life through a correlation matrix, with **intangible asset risk added outside
the square root** and receiving no diversification credit (3.1). Life holds mortality, longevity, disability-morbidity,
expense, revision, lapse and catastrophe; health holds an NSLT branch, an **SLT** branch mirroring the life sub-modules,
and a catastrophe branch; market holds interest rate, equity, property, spread, currency and concentration; counterparty
default splits into type 1 (reinsurance, cash at bank, derivatives, guarantees) and type 2 (receivables, policyholder
debtors, qualifying mortgage loans). Every correlation, stress size and factor is in
`uk/regulatory/technical-notes.md`, "The standard formula SCR".

**Module allocation is decided by rule, not by product name.** SCR-SF 3.2A: the **non-life** module applies to non-life
obligations **other than health obligations**; the **life** module to life obligations **other than health
obligations**; the **health** module to **health obligations** [REG-R62]. The health module is **not a residual — it
takes precedence over both**. SCR-SF 3.10B then splits health into NSLT and SLT by numbered line of business. For
**income protection** the chain is settled: an individual long-term UK IP contract pays financial compensation arising
from illness or disability, hence a health insurance obligation and specifically an *income protection insurance
obligation*; on a long-term technical basis it is **SLT health**, LoB 29, taking the SLT sub-modules including the
income-protection disability-morbidity scenario, health revision — which, unlike its life counterpart, adds
**inflation** to its triggers — and the health catastrophe sub-modules [REG-R62]. An annually-renewable or group scheme
lands in **NSLT segment 2** and is charged by a factor formula on premium and reserve volumes rather than by scenario.

**For critical illness the classification is not settled, and the matrix says so.** The SCR and reporting streams both
left it `?`. A textual chain exists — a CI lump sum is financial compensation arising from illness, hence a health
insurance obligation, hence excluded from the life module by 3.2A(2) and routed to health by 3.2A(3); underwritten,
multi-year and reserved on a life-office basis it is SLT health, hence LoB 29; and inside the SLT branch the Glossary's
*income protection insurance obligation* is a **residual** category capturing all limb-(2) compensation, so a CI lump
sum falls inside the sub-module the Rulebook **labels** "income protection" [REG-R62][REG-R42]. **That chain is a
derivation by the drafter; no retrieved document states the conclusion.** It is uncomfortable on its face: the
recovery-rate and persistency limbs of that scenario are conditional on recovery rates below 50% and persistency rates
at or below 50%, and a lump-sum CI contract has no recovery or persistency rates at all, so both limbs are vacuous —
itself evidence the rule was not
drafted with CI in mind. Two things remain genuinely open: whether an **accelerated** CI contract can be unbundled under
TPFR 26.7 into a death leg in the life module and an illness leg in the health module, when the benefit pays **once** on
the earlier of two events and the legs are not additive; and the **numbered line of business** a standalone CI policy
belongs to, which cannot be checked because **the line-of-business list behind 3.10B sits in the unretrieved Annexes**
[REG-R73]. The reporting layer pulls the other way on unbundling: IR.12.04 instructs that "where **accelerated**
critical illness is the main product the basis should be the percentage of **combined** mortality and critical illness
claims", presuming a single combined decrement [REG-R89]. The matrix marks the CI life/health rows `?`.

### What a "scenario" means, and which stresses need a full revaluation

SCR-SF 3.3A(1) fixes four assumptions for every scenario-based module: the scenario **does not change the risk margin**;
**does not change the value of deferred tax assets and liabilities**; **does not change the value of future
discretionary benefits**; and **no management actions are taken during the scenario** [REG-R62]. Yet 3.3A(2) requires
the recalculated technical provisions to take account of future management actions complying with TPFR 8 and of any
material adverse impact of the scenario or those actions on policyholder option exercise. **Limbs (1)(d) and (2)(a) are
in tension on their face; the research recorded the tension rather than resolving it, and so does this document** — a
reading exists (that (1)(d) excludes new discretionary responses while (2)(a) preserves the pre-agreed framework) but it
is the research file's interpretation, not a quoted rule, and it sits awkwardly with 6.3(2)(b), which switches
management actions on for the *net* run and would be redundant if they were already on in the gross run. Two universal
rules follow: simplified methods for the stressed technical provisions are permitted unless the error could influence
the user, **unless the simplification produces an SCR exceeding the standard-formula SCR** — prudence is always
permitted (3.3A(3)); and **where a scenario would increase basic own funds, the calculation must assume it has no
impact** (3.3A(5)), so every scenario-based sub-module requirement is **floored at zero**.

**The full-revaluation / formulaic split is the dominant architectural consequence of the standard formula.** "Full
revaluation" means the liability model must be **re-run end to end under changed assumptions**; "formulaic" means a
closed form over exposure statistics the projection produces but does not re-project [REG-R62].

| Module / sub-module | Full revaluation of the BEL? | What drives it |
|---|---|---|
| Life mortality, longevity, disability-morbidity, expense, revision, catastrophe | **Yes** | shocks to the rates or amounts **used in the technical provisions**; mortality, longevity and catastrophe apply only to the TP-increasing subset |
| Life lapse — up, down, mass | **Yes, three times** | exercise rates up, exercise rates down, and an instantaneous mass discontinuance; the charge is the **highest** of the three |
| SLT health mortality / longevity / expense / disability-morbidity / revision / lapse | **Yes** | as life, with health-specific disability-morbidity and revision scenarios and three lapse scenarios |
| NSLT health premium and reserve | **No — factor** | a multiple of a standard deviation on premium and claims-provision volumes |
| Health catastrophe — mass accident, accident concentration, pandemic | **No — factor**, but the pandemic leg needs a **permanent-disability benefit valuation** an ordinary IP projection does not produce | sums insured and benefit ratios by event type and country. **The Annex XVI inputs were not retrieved by any stream, so these sub-modules cannot be computed from this library's material even though their structure is known** [REG-R73] |
| Interest rate up / down | **Yes, twice** | rebuild the curve and revalue **assets and** the best estimate; the charge is the higher direction, summed across currencies within each direction |
| Equity, property | Assets only — **but the best estimate too** for unit-linked and with-profits | instantaneous falls, with a symmetric adjustment on the equity charge |
| Spread — non-MA | Assets only | duration- and credit-quality-dependent factors |
| **Spread on a matching adjustment portfolio** | **Yes** | stress the assets **and recalculate technical provisions to take account of the impact on the amount of the matching adjustment**, by increasing the fundamental spread on assigned assets by a credit-quality-dependent proportion of the widening |
| Concentration, currency, counterparty default type 1 and 2, intangible, operational | **No — factor** (currency also revalues FX-denominated BEL) | single-name exposures, FX positions, PDs and LGDs, intangible value, earned premiums, technical provisions and unit-linked expenses |
| **LACTP (`Adj_TP`)** | **Yes — a full second pass of everything above** | FDB responsive, management actions live |
| **LACDT (`Adj_DT`)** | Balance-sheet revaluation of deferred taxes | an instantaneous loss of `BSCR + Adj_TP + SCR_operational` |
| **Ring-fenced fund / MA portfolio notional SCRs** | **Yes — repeat the whole exercise per perimeter** | no diversification between perimeters |

On the MA spread row: the fundamental spread on assigned assets is increased by the spread widening implied by the
stress multiplied by a **reduction factor varying by credit quality step**, so the MA absorbs the complement — a
high-quality portfolio retains most of the widening inside the MA while low-quality assets get **no offset at all**. The
factor table is in `uk/regulatory/technical-notes.md`.

**The two-run structure, and why with-profits forces it.** `Adj = Adj_TP + Adj_DT` (6.1(3)) [REG-R62]. The TP leg is
`Adj_TP = −max(min(BSCR − nBSCR; FDB); 0)`, where `nBSCR` is the **net basic SCR** — the whole BSCR recalculated with
the scenario permitted to change the value of future discretionary benefits, with the scenario-based calculations in the
life module, the SLT health sub-module, the health catastrophe sub-module, the market module and the counterparty
default module taking account of the FDB impact **on the basis of future management actions complying with TPFR 8**, and
taking into account any legal, regulatory or contractual restrictions on distributing FDB (6.3). `BSCR − nBSCR` is
therefore **exactly a second complete pass of the liability model**, and the FDB risk-mitigating effect counts only to
the extent the firm can establish that a reduction in FDB may be used to cover unexpected losses (6.2). The DT leg is
the change in deferred taxes resulting from an **instantaneous loss equal to `BSCR + Adj_TP + SCR_operational`** — note
the ordering: computed on the post-`Adj_TP` loss and **including** operational risk. An **increase in deferred tax
assets arising from that loss must not be utilised**, a transitional permitting otherwise having run only to **30
December 2025**; a decrease in DTLs or increase in DTAs gives a negative adjustment; a positive change gives a nil
adjustment [REG-R62]. **That transitional is still printed in the 05/08/2026 Rulebook view and no PRA instrument
confirming its expiry or extension was retrieved** — treat it as expired for a current-date calculation and flag it.

Firms with **no** future discretionary benefits — term assurance, critical illness, income protection, the unit-linked
bond, a non-profit pension annuity — have `BSCR = nBSCR` and `Adj_TP = 0`, so one run suffices. **With-profits is the
product that forces the two-run architecture.** A further trap: four sub-modules are defined as the *highest* of
alternative scenarios (life lapse, SLT health lapse, interest rate, currency), and each carries a rule that where the
highest gross requirement and the highest corresponding net requirement rest on different scenarios, the charge is **the
one whose underlying scenario produces the highest net requirement** [REG-R62]. **The selection is made on the net run;
the reported gross number follows the net selection.** This is easy to implement wrongly.

**Ring-fenced funds and MA portfolios remove diversification credit.** A firm with a ring-fenced fund — other than one
whose restricted own funds are fully deducted under Own Funds 3L.2 — **or a matching adjustment portfolio** must follow
SCR-SF Chapter 9 instead of the ordinary aggregation (2.2) [REG-R62]. Under 9.1 the firm computes a **notional SCR for
each RFF, each MA portfolio and the remaining part, as if each were a separate firm**; **the firm's SCR is the sum of
those notional SCRs**; scenario impacts are measured **at each perimeter**, with basic own funds there **including only
restricted own funds**; profit-participation arrangements inside an RFF get an FDB adjustment capped at that fund's FDB;
and — **notwithstanding the ordinary rule — the firm must not allow for diversification effects between its ring-fenced
funds, its matching adjustment portfolios, or the remaining part**. One subtlety catches implementers: the *scenario
choice* is made **firm-wide**, each notional SCR using the scenario under which the basic own funds of the **firm as a
whole** are most negatively affected, so a notional SCR can be driven by a scenario that is not the worst for that fund.
**How a firm performs that firm-wide search in practice is not prescribed by any retrieved source.** A *ring-fenced
fund* is defined by the Glossary as an identifiable unit of assets and liabilities whose restriction gives rise to
**restricted own funds**, "**other than a matching adjustment portfolio**" — RFFs and MA portfolios are **disjoint
categories receiving the same treatment** [REG-R80]. For UK with-profits the application is categorical: SS14/15 states
the PRA expects the with-profits restrictions "will generally mean that **each with-profits fund displays the
characteristics of a RFF**", and that a **sub-fund** required to be treated as a separate with-profits fund under FCA
COBS 20 should be treated as a **separate RFF** [REG-R71][REG-R9]. A with-profits insurer with three sub-funds therefore
runs **at least four** complete notional SCRs and adds them.

**Simplifications exist, and they change the net run.** SCR-SF Chapter 7 permits a simplified calculation for a module
or sub-module where the nature, scale and complexity of the risks justifies it, subject to a documented proportionality
assessment covering the error introduced; it **must not be used** where that error could lead to a misstatement
influencing the user — **unless it produces an SCR exceeding the standard calculation** [REG-R62]. The life
simplifications convert full revaluations into closed forms over summary statistics — capital at risk, modified
duration, weighted-average rates, surrender strain — and are set out with their formulas in
`uk/regulatory/technical-notes.md`. Two architectural notes: **there is no simplification for mass lapse**; and using
certain listed simplifications forces an **instantaneous-loss substitution** in the net run (6.3(2)(d)), so electing one
changes how `nBSCR` is constructed.

**Undertaking-specific parameters reach exactly one thing here.** USPs require a **USP permission**, and a firm that
adopts one **must not revert** (USP 2.1, 2.2) [REG-R65]. The replaceable parameters are an **exhaustive list** covering
non-life and NSLT health premium and reserve risk, the non-proportional reinsurance adjustment factor, and **the
increase in the amount of annuity benefits** for life revision risk and for health revision risk. **Nothing else in the
standard formula may be replaced** — no USP for any mortality, longevity, lapse, expense or catastrophe parameter, and
none for any market or counterparty parameter. For the seven UK products the regime reduces to the **revision-risk
parameter** for pension annuities (life) and income protection (health), and only where the annuities in scope are
**not subject to material inflation risk**.

**Internal models, and capital add-ons.** A firm may use a full or partial internal model **only** with permission and
**only to the extent of** that permission, must use it, and **must not revert** to the standard formula for any part of
the SCR (SCR – Internal Models 2.1, 2.2, 8.1) [REG-R81]. Yet the same Part requires the firm to be able, **on PRA
request, to provide an estimate of the SCR under the standard formula** (3.4), which SS15/16 turns into a standing
capability expectation [REG-R68]. **An internal model firm must therefore operate two complete calculation paths over
the same liability cash flows, only one of which may be used.** The *submission* expectation is narrower and easy to
over-read: only insurers **with material non-life technical provisions** are expected to report a non-life standard
formula SCR privately via XBRL, so **a life-only internal model firm is not caught by the submission expectation** but
is caught by the capability expectation [REG-R68]. The model must produce a full **probability distribution forecast**
of the change in basic own funds over one year, from which the SCR is the 99.5% value-at-risk; must pass a **use test**
— it is not widely used or important "where the quantifications of risks and the risk ranking produced by the internal
model **do not trigger timely and appropriate risk management actions**"; must be validated regularly and
independently; and must support an **Analysis of Change** walking the prior year-end SCR to the current one with reasons
and documentary evidence, the duty applying for financial years ending on or after 31 December 2024 and first submitted
for the first financial year end on or after **31 December 2025** [REG-R81]. **Profit and loss attribution has been
deleted and the Analysis of Change replaces it.** SS1/24 adds that including a **new risk** is expected to be a **major
model change**, and that the PRA expects an appropriate senior manager — "in most cases the Chief Risk Officer (SMF4)" —
to **attest annually in writing** to compliance or to a credible remediation plan [REG-R81b]; **whether that attestation
must be submitted to the PRA or merely held is not stated**. Finally, a **capital add-on** plus the pre-add-on SCR **is**
the firm's SCR (SCR-GP 5.2); the PRA's approach is SoP4/24, **whose quantitative significance thresholds were not
retrieved and are not stated here** [REG-R61][REG-R69].

---

## Own funds, ring-fenced funds and the minimum capital requirement

**Tiering.** Tier 1 requires an item of *basic* own funds substantially possessing both **permanent availability** —
available or callable on demand to fully absorb losses on a going-concern basis as well as in winding up — and
**subordination**, meaning that in winding up the total amount absorbs losses and repayment is refused until all other
obligations, **including insurance obligations to policyholders**, have been met (Own Funds 3.5) [REG-R77]. Tier 2
requires subordination only for basic own funds; Tier 3 is the residual. The assessment must consider **sufficient
duration**, **absence of incentives to redeem**, **absence of mandatory servicing costs** and **absence of
encumbrances** (3.6). Practically, for a UK life insurer: **Tier 1 unrestricted = share capital and premium + surplus
funds + the reconciliation reserve; Tier 1 restricted = perpetual subordinated debt and preference shares meeting the
fifteen Tier 1 features; Tier 2 = dated subordinated debt; Tier 3 = net deferred tax assets** and dated subordinated
debt failing the Tier 2 tests. Ancillary own funds need a permission specifying an amount or a method and must be
**callable on demand**; SS2/15 records that AOF **is not emergency capital** and that a firm at risk of breaching its
SCR should raise basic own funds instead [REG-R83]. For a liability model AOF is out of scope.

**The eligibility limits are stated twice, on two denominators, and both chapters are live.** Own Funds Chapter 4 (dated
01/01/2016) expresses them as fractions of **eligible own funds**; Chapter 4A (dated 31/12/2024) expresses them as
percentages of **the SCR and the MCR**, with a sub-limit capping restricted Tier 1 plus transitionally-grandfathered
items at less than 20% of total Tier 1 [REG-R77]. The two are **not arithmetically equivalent**. SS2/15 supplies the
PRA's reconciliation — "For the purposes of Own Funds 4, Own Funds 4A sets out the applicable limits" — which reads as
treating 4A as operative and 4 as enabling, but **no retrieved rule says Chapter 4 is disapplied** [REG-R83]. Recorded,
not resolved; the numeric limits are in `uk/regulatory/technical-notes.md`.

**The reconciliation reserve is where every actuarial modelling decision reaches regulatory capital.** It is a
**residual**: the total excess of assets over liabilities reduced by own shares held, by **foreseeable dividends,
distributions and charges**, by the listed basic own funds items (share capital, initial funds, subordinated mutual
member accounts, **surplus funds**, preference shares), by any permissioned item, by **restricted own funds exceeding
the notional SCR of an MA portfolio or ring-fenced fund** or excluded under the immateriality simplification, and by the
participations deduction (3C.1) [REG-R77]. It **may be positive or negative** (3C.2), and a firm is **not required to
determine whether it displays the Tier 1 features** by looking through to the underlying assets and liabilities (3C.3) —
which is what lets the whole residual sit in Tier 1 unrestricted, and therefore why best-estimate assumptions, contract
boundaries, management actions and TMTP land directly in the highest tier of capital. Two defects here are admitted by
the PRA: CP4/26 proposed "removing unnecessary text and **clarifying the interaction of Own Funds 3C and Own Funds 3L**"
and separately proposed correcting an inconsistency that would cancel out an increase in eligible own funds following a
classification permission — but **PS18/26 finalised only the first of that consultation's proposals**, so as at
2026-08-06 both defects remain in the live rule text [REG-R83c][REG-R87]. **"Foreseeable dividends, distributions and
charges" is not defined in the Own Funds Part**, and whether the deduction requires a board-approved dividend, a
policy-consistent
dividend, or something else, is unresolved.

**The with-profits estate is Tier 1 capital, not a technical provision.** Rule by rule
[REG-R1][REG-R45][REG-R46][REG-R77]: **TP 9.1(3)** requires technical provisions to include all payments to
policyholders, **including future discretionary bonuses**, whether or not contractually guaranteed — **"unless those
payments fall within Surplus Funds 2.1"**; **Surplus Funds 2.1** says a firm "shall **not treat surplus funds as
insurance and reinsurance obligations**" in calculating technical provisions; **SS13/15 ¶2.1** makes that carve-out
conditional on the surplus funds meeting the **Tier 1** requirements; **Own Funds 3A.1(1)(d)** then makes them a **Tier
1 unrestricted own funds item in their own right**; and **SS13/15 ¶2.3** adds that surplus funds "will normally meet the
criteria for classification as Tier 1 own funds" **but**, because of FCA policyholder-fairness rules, are "likely to be
treated as part of a ring-fenced [fund]" — so they are Tier 1 **and** restricted.

Surplus funds are computed per with-profits fund as **with-profits assets less with-profits policy liabilities less tax
and other costs on future shareholder transfers less other attributable liabilities less the value of future shareholder
transfers** (Surplus Funds 3.1) [REG-R45]. With-profits policy liabilities are valued **retrospectively by default** —
the regulatory asset-share definition, a ten-item signed accumulation per policy — and **prospectively only** where the
retrospective value "does not adequately reflect the value" or is impracticable, with prospective benefits clamped so
that future discretionary additions count "**only to the extent they are consistent with what the retrospective
calculation would have allowed for**" (3.3–3.5). Four PRA expectations change the numbers materially [REG-R46]: **there
is no risk margin in the surplus funds calculation** — the Part "does not refer to or include a risk margin", which the
firm must still hold on its business as a whole, so **surplus funds and technical provisions are not a clean partition
of the with-profits fund**; **whole-of-life policies are the named example** where the retrospective result "might be
negative or significantly lower than the value calculated using the prospective approach"; grouping is permitted only
where it gives the **same or a higher** result and groups policies with similar attributes "**including the status of
guarantees**"; and the PRA "would not expect a firm to include within benefits payable **distributions from the
estate**" it might make in run-off — which is what keeps the estate in own funds rather than in technical provisions.
**The PRA Rulebook Glossary definition of "surplus funds" could not be retrieved** — ten URL forms were tried and all
failed — so everything here rests on the Surplus Funds Part calculation and Own Funds 3A.1(1)(d), not on a definition,
and **the scope of the defined term is [unverified]** [REG-R45][REG-R77].

**The ring-fencing hit is taken twice.** The *numerator* effect is Own Funds 3L: reduce the excess of assets over
liabilities, for reconciliation-reserve purposes, by `max(0, restricted own funds within the RFF or MA portfolio − that
perimeter's notional SCR)`, computed under SCR-SF 9.1 for standard formula firms and using the internal model "as if the
firm pursued only the business included in the ring-fenced fund or matching adjustment portfolio" for internal model
firms; where the assets, liabilities and risk in an RFF are **not material** the firm may instead deduct the **total**
restricted own funds and skip the notional SCR (3L.2), which is also the trigger for the SCR-SF 2.2 carve-out
[REG-R77][REG-R62]. **Restricted own funds therefore count towards entity own funds only up to the capital the fund
itself needs**; the classic surplus estate above the fund's own SCR is struck out. The *denominator* effect is the loss
of diversification described in the previous section. **Whether the RFF deduction also bites the MCR coverage test is
not settled**: Own Funds 3L operates textually on the reconciliation reserve, while EIOPA's ring-fenced funds guideline
is explicit that only own funds equal to the notional SCR contribute to coverage of the SCR **and the MCR**, and no
retrieved PRA rule says so [REG-R77][REG-R80c]. Those EIOPA guidelines carry their own status caveat — they cite the
Solvency II Directive and the Delegated Regulation rather than PRA rules, and their continued UK application rests on
SoP1/19, **which was not retrieved**. Read subject to that, they supply two facts the PRA rules do not: **conventional
unit-linked and conventional index-linked products are generally outside RFF scope**, and **surplus funds are not
ring-fenced merely by being surplus funds — only by arising inside a ring-fenced fund** [REG-R80c].

**EPIFP has gone from Solvency UK, and the frozen reference page does not know it.** There is **no EPIFP rule in the Own
Funds Part** — the retrieved Part, read in full, has **zero occurrences of "expected profit"** — nor in the Technical
Provisions Part, the TPFR Part, the restatement instrument, or the Reporting Part
[REG-R77][REG-R1][REG-R41][REG-R42][REG-R84]. PS3/24 is decisive on the reporting position: eight respondents "welcomed
the deletion of the expected profits included in future premiums (EPIFP) requirement in S.23.01", and "the PRA has
amended the template instructions to clarify that the **EPIFP requirement is being removed from all reporting, including
disclosure**" [REG-R86]. The only live retrieved text of the concept is the definition in **Article 1(46) of the revoked
Delegated Regulation** [REG-R49] — and **whether that Article survives as operative UK law was not established**, the
standard-formula stream recording that Articles 84–221 were revoked and restated while the legislation.gov.uk page for
Article 1 carries no revocation annotation. The practical conclusion does not depend on that: **a Solvency UK model does
not need to produce the EPIFP decomposition** — recompute the best estimate with future premiums set to nil and take the
difference — that an EU model still needs. The economics survive inside the reconciliation reserve; no rule requires
them to be isolated. A UK document describing an EPIFP disclosure is describing the EU regime.

**The minimum capital requirement.** `MCR = max(MCR_combined, AMCR)` with
`MCR_combined = min(max(MCR_linear, 0.25 × SCR), 0.45 × SCR)` (MCR 3.1A, 3.1B) [REG-R78]. The **absolute floor for
long-term insurance is £3,500,000**, which is the relevant floor for every product here. Rule 3.3 independently restates
the corridor in words and adds that it applies to the SCR "**including any capital add-on which has been imposed**" —
**3.1B does not say so on its face, and a drafter must apply the add-on inclusion from 3.3**. `MCR_linear` for long-term
business is a five-term linear formula over technical provisions **without the risk margin**, net of reinsurance and
**floored at zero term by term**: guaranteed benefits of with-profit business; **future discretionary benefits of
with-profit business, carrying the formula's only negative coefficient**, so a larger FDB reserve *reduces* the linear
MCR; linked liabilities; all other long-term obligations; and **capital at risk**, defined per contract as the amount
the firm would currently pay on **death or disability** plus the expected present value of further amounts payable on
immediate death or disability, less the best estimate of the corresponding obligations, **floored at zero per contract
rather than on the portfolio sum**. The coefficients are in `uk/regulatory/technical-notes.md`. For a UK life book
`MCR_linear` is almost always far below 25% of the SCR, so **the MCR is normally the 25% collar** — **but not for pure
protection**: a negative best estimate zeroes `TP_l4` under the per-term floor while `CAR` stays at nearly the full sum
assured, so `MCR_linear` can exceed `0.25 × SCR`, as the worked example in `uk/regulatory/technical-notes.md` shows;
check which limb binds rather than assuming the collar [REG-R78 3C.1]. The linear formula matters mainly as the
"**pre-corridor MCR**" the PRA uses as an internal-model drift metric [REG-R68] and for very small
or run-off entities where the £3.5m floor or the 45% cap binds. Eligible own funds covering the MCR face tighter limits,
and **Tier 3 is not eligible to cover the MCR at all** [REG-R77]. Two things the sources do not settle: **how capital at
risk is computed for a disability income benefit**, the rule being drafted around an amount currently payable while an
income stream is an expected present value; and **how the MCR interacts with ring-fenced funds at all**, MCR 3C.1
aggregating technical provisions across the firm with no RFF split and the MCR Part containing no RFF rule.

**What a breach costs.** On an SCR breach the firm notifies the PRA immediately — and also on becoming aware of a risk
of breach within three months — submits a **realistic recovery plan within two months**, and must restore compliance
**within six months**, extendable by the PRA, with progress reports every three months where extended for an exceptional
adverse situation. On an MCR breach the notification duty is the same, a **short-term realistic finance scheme** is due
**within one month**, and compliance must be restored **within three months** [REG-R82]. Either plan must contain
estimates of management expenses and commissions, estimates of income and expenditure for direct business and inwards
and ceded reinsurance, **a forecast balance sheet**, estimates of the financial resources intended to cover technical
provisions, the SCR **and** the MCR, and the firm's overall reinsurance policy. **This is the only place in the
retrieved material where a projected solvency balance sheet is required by rule rather than by supervisory
expectation**, and it is what forces a liability model to roll own funds and both capital requirements forward over a
multi-year horizon. **Whether an MCR breach can lead to withdrawal of authorisation is not stated by any retrieved
source** — the Undertakings in Difficulty Part contains no such rule and the UK analogue of the EU provision, if any,
was not located. Do not assert it.

---

## Regulatory reporting, disclosure and governance

**The IR./IRR. template family is the UK analogue of the U.S. annual statement exhibits.** Reporting 2.5A lists what a
UK Solvency II firm submits: the **SFCR**; the **ORSA report**; for internal model firms the qualitative information
supporting the quarterly model-change return and the qualitative analysis supporting the **Analysis of Change**; for MA
firms the **MALIR 1–7** returns; and annual, semi-annual and quarterly **quantitative templates** [REG-R84]. **There is
no Regular Supervisory Report** — the RSR requirement ceased on 31 December 2023 [REG-R86], and the Reporting Part
carries no narrative supervisory report at all. Chapter 9 inventories 99 template code stems; **there is no IR.13.01 and
no IR.29.xx**, so the EU's life best-estimate cash-flow projection template and the whole variation-analysis series are
absent. On IR.13.01 a conflict is recorded and not resolved: **PS3/24 ¶4.70 states that "S.13.01 and SR.22.02 will
continue to be collected"**, yet the final Reporting Part contains no IR.13.01 in any Article or in the Chapter 9
inventory and the PRA's published instruction library contains no `ir1301` file [REG-R86][REG-R84][REG-R88]. **PS15/24
itself was not fetched in the reporting stream and its appendices were not read**, so this must be checked before any
document asserts that the UK collects no life BEL cash-flow projection.

The templates a liability model must populate, and what each demands beyond the balance sheet [REG-R89][REG-R90][REG-R91]:

- **IR.12.01 / IRR.12.01 — life technical provisions.** Quarterly and annual, and **per ring-fenced fund, per MA
  portfolio and for the remaining part**. Gross best estimate split **direct business vs reinsurance accepted**,
  including technical provisions as a whole; recoverables **before and after** the counterparty default adjustment,
  split traditional / SPV / finite; risk margin; the **five TMTP components**; and six sensitivity amounts — best
  estimate subject to, and technical provisions without, the interest-rate transitional, the volatility adjustment and
  the matching adjustment. Segmentation "shall reflect the **nature of the risks underlying the contract (substance),
  rather than the legal form of the contract (form)**". Unit-linked-only rows require **surrender value**, **nominal
  value of units** (allowing for actuarial funding or discounting of capital units subject to a higher charge) and
  **matching value of units**. Quarterly submissions **may apply simplified methods**.
- **IR.12.04 — best estimate assumptions for life insurance risks.** Triggered where gross BEL for long-term business
  other than reinsurance exceeds **£50 million** or gross written premiums exceed **£10 million**. Its purpose is "to
  give an indication of **changes in the valuation basis**, how the basis **compares with experience** and the
  **variability of the firm's recent experience**", so it requires the current and prior year bases **and five years of
  own experience**, by assumption type, with up to three subcategories each and an experience-credibility guideline of
  **200 claims per annum** per line. It names the **underlying table** as a required field, with the instruction that
  where the CMI Mortality Projections Model is used the description must be "consistent with latest guidance from the
  CMI" — the direct regulatory hook for the CMI references this library can only proxy.
- **IR.14.01 — life obligations analysis**, keyed on the **PRA three-digit product codes** (the former SS36/15 content
  and the best public map from UK product taxonomy to regulatory reporting). It requires contract counts, new contracts,
  written premiums, claims paid, best estimate and **capital at risk** per product code, and states that "**all
  insurance contracts shall be reported even if classified as investment contract on accounting basis**". The codes for
  this library's products are listed under "Product applicability".
- **IR.12.05 / IR.12.06 (and their IRR. per-fund variants) — with-profits value of bonus, and with-profits liabilities
  and assets.** Triggered where net BEL for with-profits business exceeds **£500 million**. IR.12.05 requires the value
  of bonus split into bonuses added at claim, **clawback of past bonuses shown negative**, cash bonuses, reversionary
  bonuses **valued in accordance with COBS 20.2.17R**, and other bonuses, plus a shareholder-transfer block whose
  formula the model must reproduce. IR.12.06 is the UK realistic-balance-sheet decomposition inside the Solvency UK best
  estimate: **with-profits benefits reserve** (retrospective asset shares and/or prospective reserve, tied by the
  instruction to Surplus Funds 3.2–3.4) plus **future policy related liabilities** — guarantees (which "**cannot be
  negative**"), non-contractual commitments, **financial options such as guaranteed annuity rates**, smoothing (which
  **can** be negative), financing and other costs, less planned deductions — with an explicit tie that the total "should
  correspond to IR.12.01.01 R0030 C0010".
- **IR.05.03 — life income and expenditure**, on **financial accounting conventions** (see "The Solvency UK balance
  sheet a model must populate"), and **IR.05.10 — excess capital generation**, the **only Solvency UK template requiring
  a multi-year forward projection**: one actual year plus **three plan years** decomposing the movement in excess
  capital into own funds generation, SCR run-off, risk margin run-off (**gross of any movement in TMTP**), TMTP run-off,
  new business, experience and economic variances, management actions, assumption changes, model changes and capital
  actions, reconciling to eligible own funds and the SCR at start and end. **Its scope test is stated inconsistently**:
  the Rulebook triggers it on life premiums excluding unit-linked premiums exceeding **£1 billion in the most recent
  reporting year**, while the instruction file says **any of the three most recent years** and **includes SLT health
  business**. Per the PRA's own hierarchy the Rulebook prevails, but the published Q&A addresses only
  instruction-versus-data-point-model conflicts. **Unresolved.**
- **MALIR 1–7 and IRR.22.02 / IRR.22.03 — the matching adjustment set.** MALIR 3 is the most demanding liability output
  in Solvency UK: **monthly** gross liability cash flows per MA portfolio out to month 600, in four streams — level or
  fixed-escalation claims, **inflation-linked** claims, expenses, and other — plus their present values on the basic
  curve and on basic-plus-MA, with the rule that "for liabilities with a combination of fixed and inflation-linked
  characteristics the **full set** of liability cash flows should be reflected as inflation-linked". IRR.22.02 requires
  annual liability outflows, expense outflows and **de-risked asset cash flows** with positive and negative
  undiscounted mismatches reported **separately and never netted**; IRR.22.03 requires both annual effective rates, the
  MA in basis points, the **mortality stress result for MA eligibility**, and a Macaulay-equivalent liability duration.
  **MALIR 4–7 were not read beyond their titles**, and MALIR 5 in particular contains the quantitative matching tests a
  pension annuity model must pass — **the single largest unread block in the reporting stream** [REG-R91]. From the 31
  December 2026 reference date PS18/26 replaces MALIR with a new MA template set moving to XBRL, **whose instruction
  files were not retrieved** [REG-R87].

**The SFCR.** Disclosed annually within **70 business days** of financial year-end, on a **fixed structure** — Summary;
A Business and Performance; B System of Governance; C Risk Profile; D Valuation for Solvency Purposes; E Capital
Management — with a "**clear and concise summary understandable to policyholders**" highlighting material changes
[REG-R84]. Section **D.2** is the technical provisions disclosure and is where a model owner's work surfaces: per
material line of business, the value of technical provisions **with the best estimate and risk margin separately**, the
bases, methods and main assumptions, **a description of the level of uncertainty**, a quantitative and qualitative
explanation of material differences from the financial-statements basis, a statement whether the risk-free transitional
or TMTP is applied **with a quantification of the impact of not applying it** on technical provisions, SCR, MCR, basic
own funds and eligible own funds, and "**any material changes in the relevant assumptions … compared to the previous
reporting period**"; SS40/15 adds that firms should describe the **significant simplified methods** used, including for
the risk margin [REG-R84][REG-R85]. Where a matching adjustment is applied the SFCR must also carry **a quantification
of the impact of a change to zero of the MA** on the same five quantities, and **the attestation disclosure**; the same
change-to-zero quantification applies to the volatility adjustment [REG-R84]. Section C requires "a description of the
methods used, the assumptions made and the outcome of **stress testing and sensitivity analysis** for material risks".
The SFCR must be **approved by the governing body** before disclosure, and SS11/16 expects the body to **sign it with a
written acknowledgment of responsibility attached** [REG-R84][REG-R96b].

**External audit.** The **relevant elements** of the SFCR are audited to a **reasonable assurance** standard, the
auditor opining to the **governing body** that they are prepared in all material respects in accordance with the PRA
rules, and reading the rest of the SFCR for **material inconsistencies** [REG-R96]. Two carve-outs matter: information
that "is, or derives from, the SCR" is audited **only for standard formula firms**, so **a life internal model firm's
SCR disclosures are not audited — but IR.12.01.02 and the section D.2 narrative are**. The Part applies only to firms
that are not "small firms for external audit purposes", a status decided by a **score** whose two life inputs are
defined **directly on liability-model output cells** — life BEL from IR.12.01 less annuities from non-life less
corporate pensions business, and life gross written premium from IR.05.03 less corporate pensions [REG-R96]. On the
matching adjustment, SS11/16 states that the **scale** of the MA is in scope because its impact on technical provisions
falls within the relevant elements, but that auditors "**are not required to assess whether a firm meets the eligibility
conditions for use of the MA**" [REG-R96b].

**The ORSA is the requirement that forces the whole stack to be projected.** CGB 3.8 requires an assessment of the
firm's **overall solvency needs**, of **compliance on a continuous basis with the SCR, the MCR and the technical
provisions requirements**, and of **the significance with which the risk profile deviates from the assumptions
underlying the SCR** [REG-R92]. **CGB 3.8(4) is the key computational requirement for a UK life model**: where a firm
applies the **matching adjustment, the volatility adjustment, the risk-free transitional or the TMTP**, it "must perform
the assessment of compliance with the capital requirements … **with and without taking into account those adjustments
and transitional measures**". CGB 3.8A requires the assessment to be **forward-looking**, covering potential future
changes in risk profile from business strategy or the economic environment, over "the **time periods that are relevant
for taking into account the risks the firm faces in the long term**". SS19/16 adds that it is "**fundamental** to the
ORSA that it is forward looking", that the PRA expects firms "to find ways to **estimate their future solvency
position**", that good reports include a **three to five year forecast**, that the assessment of solvency **over the
business planning period** forms part of the process and report with **dividend policy "a key point"**, and that
**reverse stress testing** is expected with the report defining what constitutes business failure [REG-R95]. The report
is due **within 10 business days after concluding the ORSA** [REG-R84]. Standard formula firms must "**explain clearly
within the ORSA report where the firm's own risk profile deviates from the standard formula assumptions**" and conclude
whether the standard formula is appropriate; internal model firms must confirm and evidence the model's continued
adequacy [REG-R95].

**The actuarial function, validation and documentation.** CGB 6.1 gives the actuarial function nine tasks: **coordinate
the calculation of technical provisions**; **ensure the appropriateness of the methodologies, models and assumptions**;
**assess the sufficiency and quality of the data**; **compare the best estimate against experience**; **inform the
governing body of the reliability and adequacy** of the calculation; oversee the calculation where approximations are
used; **express an opinion on the overall underwriting policy**; **express an opinion on the adequacy of reinsurance**;
and contribute to the risk-management system, "in particular with respect to the **risk modelling underlying the
calculation of the SCR and MCR** and to the firm's **ORSA**" [REG-R92]. Reporting to the board must include "at least a
reasoned analysis on the reliability and adequacy of the calculations and on the sources and degree of uncertainty",
**supported by a sensitivity analysis investigating the sensitivity of the technical provisions to each of the major
risks** (6.6). CGB 11B requires validation of the technical provisions **at least once a year and whenever there are
indications that the data, assumptions, methods or level are no longer appropriate**, covering data, grouping, data
limitations, approximations, "the **adequacy and realism of assumptions**", the actuarial and statistical methods, and
the level of the provisions — and **separately for homogeneous risk groups, separately for the best estimate, the risk
margin and any TP-as-a-whole, separately where the matching adjustment is applied, and separately for the gross best
estimate and the recoverables** (11B.3). 11B.2 adds that the firm must assess the impact of changes in **future
management action assumptions** and, where significant, explain **how the impact is taken into account in its
decision-making process**. CGB 11C requires documentation including "**a directory of the data used … specifying their
source, characteristics and usage**" and "**a directory of all the relevant assumptions**" with justification, inputs,
objectives and criteria, **material limitations**, review processes, and **a justification for changes of assumptions
from one period to another with an estimate of the impact of material changes** [REG-R92]. The professional layer over
all of this is FRC TAS 100 and TAS 200 and IFoA APS L1 [REG-R33][REG-R34][REG-R35]; the **Chief Actuary function is
SMF20** and the **With-Profits Actuary function SMF20a**, the latter applying only to firms carrying on with-profits
business [REG-R94][REG-R93].

**Solvent exit.** In force **30 June 2026**, the Preparations for Solvent Exit Part requires every insurer other than a
passive run-off firm to prepare so that it could effect a **solvent exit** — "the process through which a firm ceases
its insurance business **while remaining solvent**" — in an orderly manner, and to **produce a solvent exit analysis,
update it on any material change and at least every three years**, and provide the current version to the PRA on request
[REG-R98].

---

## Statutory accounts and tax

### UK GAAP: what FRS 103 actually fixes

FRS 103 fixes very little of the measurement and a great deal of the presentation, and that is the point. **Mandatory:**
its scope (insurance contracts issued, reinsurance held, and other financial instruments issued with a discretionary
participation feature, for any entity applying FRS 102, insurer or not — FRS 102 ¶1.6 makes the referral mandatory and
carves these contracts out of Sections 11, 12, 21, 22 and 23); **no provisions for possible future claims** under
contracts not in existence at the reporting date; the **liability adequacy test**; extinguishment-only derecognition;
**no offsetting** of reinsurance assets against insurance liabilities; treatment of all insurance-contract assets and
liabilities as **monetary items**; and rules on unbundling deposit components [REG-R99][REG-R102]. **Permissive:**
continuation of practices that could not be newly introduced — including **undiscounted** measurement of insurance
liabilities and measuring rights to future investment management fees above fair value (¶2.6); retention of excessive
prudence (¶2.7); retention of future investment margins, subject to a **rebuttable presumption** that introducing them
makes the statements less relevant and reliable, with the presumption "highly unlikely" to be overcome where the
discount rate determines the liability **directly** rather than only the emergence of a profit margin (¶¶2.8–2.10); and
**shadow accounting** (¶2.11). An entity setting policies for the first time may take Section 3 as the benchmark **or
build policies on the PRA Rulebook technical-provisions recognition and measurement rules with appropriate
adjustments** (¶1.5(b)), and an existing entity may change towards greater consistency with those rules (¶2.3A); the
Basis for Conclusions lists what to consider adjusting — **regulatory transitional adjustments, the volatility
adjustment, the risk margin, and surplus funds where these reflect contractual obligations of cash flows to
policyholders** [REG-R99]. **The FRC's own published position is that FRS 103 "is not aligned with IFRS 17" and that
"conflicts between IFRS 17 and UK company law mean that it is not currently possible to align" them** — so any drafting
implying near-term convergence is wrong [REG-R101].

**The liability adequacy test is the only measurement floor FRS 103 itself imposes** — a second, non-negative /
surrender-value floor comes from the non-mandatory Implementation Guidance (IG2.41, IG2.47), which accompanies but is
not part of the standard [REG-R100][REG-R101]. At each reporting date the insurer assesses whether recognised insurance
liabilities are adequate **using current estimates of future cash flows**; if the carrying
amount **less related DAC and related intangibles** is inadequate, **the entire deficiency is recognised in profit or
loss** (¶2.14). The minimum requirements are that the test considers current estimates of **all** contractual and
related cash flows "**as well as cash flows resulting from embedded options and guarantees**", and that the entire
deficiency goes to profit or loss (¶2.15) [REG-R99]. This is the point at which a UK GAAP model must run a
current-assumption, option-and-guarantee-inclusive projection **even if the recognised liability is a locked-in
net-premium reserve** — and it is the mechanism through which adverse experience first hits UK GAAP profit, including by
writing off DAC. **The fallback measurement where the entity's own test fails the minimum requirements (¶2.16 tail and
¶¶2.17–2.18) was read only in part and is not specified here** [REG-R99].

**With-profits under UK GAAP** runs on the **realistic value of liabilities** rather than MSSB, adjusted to **exclude
the shareholders' share of projected future bonuses**, with the difference from MSSB routed through the **fund for
future appropriations** so that "there will generally be no change in the profit for the reporting period **except where
the adjustments result in a negative balance on the FFA**" [REG-R99][REG-R100]. The FFA is "all funds the allocation of
which either to policyholders or to shareholders has not been determined by the end of the financial year", disclosed
**separately** and never combined with technical provisions [REG-R105][REG-R99]. Implementation guidance requires the
options and guarantees liability of in-scope with-profits business to be measured **at fair value or by a
market-consistent stochastic model**, states that "any deterministic approach … will generally fail to deal
appropriately with the time value of the option", and requires the stochastic valuation to reflect, scenario by
scenario, **management actions consistent with the published PPFM** [REG-R100][REG-R9]. **The definitions the whole
apparatus rests on — INSPRU 1.3.40 (realistic value of liabilities) and 1.3.190 (current liabilities) as at 31 December
2015 — were not retrieved**, so "realistic value of liabilities" is a citation here, not a specification [REG-R99][REG-R116].
Linked business splits across two balance sheet lines: item **D technical provisions for linked liabilities** for the
unit element, with **any additional provisions for death risks, operating expenses or other risks such as maturity
benefits or guaranteed surrender values included under item C.2**, the long-term business provision — so a unit-linked
bond model needs a **two-part liability output**, unit reserve and non-unit reserve [REG-R105]. And a unit-linked bond
may fall outside FRS 103 altogether: HMRC records that such policies "are not regarded as insurance for accounts
purposes; these are treated as '**investment contracts**' with premiums from customers generally held on balance sheet
as **policyholder deposits** and only the fees charged within the policy treated as income" [REG-R18 LAM01100]. **FRS
103 Appendix II, the significant-insurance-risk test that decides this, was not read** [REG-R99].

### IFRS 17, and the UKEB's expected UK mapping

Under UK-adopted IFRS 17 a group of contracts is measured at **fulfilment cash flows plus a contractual service
margin**, the fulfilment cash flows being the present value of probability-weighted expected cash flows reflecting
financial risk plus an **explicit risk adjustment for non-financial risk**; contracts are aggregated into portfolios
"subject to similar risks and managed together", divided into at least three groups by onerousness, with **annual
cohorts** — contracts issued more than one year apart may not share a group — and groups are established at initial
recognition and **never reassessed** [REG-R106]. **IFRS 17 does not prescribe discount rates**, only that they reflect
the time value of money, the characteristics and **liquidity characteristics** of the cash flows, be consistent with
observable market prices, and exclude factors that do not affect the contract cash flows — the sharpest contrast with
Solvency UK, where the curve is published by the PRA [REG-R106][REG-R54]. **No confidence level, no coverage-unit
formula and no transition proxy is stated anywhere in this library**, because IFRS 17 itself was never read [REG-R107].
The **variable fee approach** applies to contracts with direct participation features and differs from the general
measurement model principally in that changes in fulfilment cash flows arising from the time value of money and
financial risk go **into the CSM** rather than immediately to insurance finance income or expense, with VFA CSM
adjustments at **current** discount rates and GMM CSM adjustments at **locked-in** rates; eligibility is assessed at
inception and **never reassessed**, and **reinsurance issued and held can never qualify** [REG-R106]. The **premium
allocation approach** is optional and available only where it reasonably approximates the GMM or the coverage period is
one year or less. **The UKEB's expectation for the UK is explicit: the VFA "is expected to be applied to insurance
contracts such as unit-linked contracts and with-profits contracts"**, the PAA to short-term general insurance and
short-term life contracts — leaving the **GMM for protection and annuities** [REG-R106]. The **inherited estate** is the
open UK issue: IFRS 17 does not explicitly address it, there is an emerging consensus that a liability must be
recognised for the policyholders' share while the shareholders' share is contested, and entities are expected to
recognise an **increase in equity on transition** under a fair value approach [REG-R106]. Under FRS 103 that same
undetermined surplus sits in the FFA, which is neither policyholder liability nor equity — **the sharpest UK GAAP /
IFRS 17 divergence for the with-profits product**.

### Tax

**BLAGAB is taxed on the I-E basis; everything else on a trade-profit basis.** FA 2012 s.68 charges corporation tax on
the **I-E profit** of basic life assurance and general annuity business and s.69 excludes BLAGAB income and gains from
any other charge [REG-R17]. The six-step computation in s.73 runs: income referable to BLAGAB; BLAGAB chargeable gains
as adjusted for allowable losses; certain I-E receipts; `I` as the sum of those three reduced by the relievable amount
of any non-trading loan-relationship deficit; `E` as adjusted BLAGAB management expenses; and `I − E`, a positive result
being the I-E profit and a negative result **carried forward as excess BLAGAB expenses** [REG-R17]. What `E` is **not**
matters for a model: **underwriting-related expenses such as claims are excluded**, expenses being restricted to
accounts-based operational expenses [REG-R18 LAM04010]. Protection business written from **1 January 2013 is excluded
from BLAGAB** and taxed on a trading basis, but earlier policies continue as BLAGAB unless an election is made
[REG-R18 LAM01080] — which is why the applicability matrix marks the BLAGAB row `(x)` rather than `—` for protection.
The **minimum profits test** (s.93–94) then ensures taxable income is at least the BLAGAB trade profit excluding
dividends, creating an I-E receipt and an equal carried-forward management expense where it bites [REG-R18 LAM07230].

**Acquisition expenses: the seven-year spread is repealed.** Until 31 December 2022 the adjusted amount of BLAGAB
acquisition expenses was spread for tax over **seven years**, deliberately independently of the accounts. FA 2012 s.79
is **repealed for accounting periods beginning on or after 1 January 2023**, and from that date a deduction is given
when amounts are recognised in the income statement under generally accepted accounting practice; two savings survive —
legacy pre-2023 sevenths keep running, and any deduction for acquisition costs such as DAC arising earlier but
recognised in a post-2023 income statement **continues to be disallowed**, so relief is given only once across the
transition [REG-R18 LAM04130][REG-R109]. A model's tax expense line therefore diverges from its accounts expense line in
two different ways depending on the period.

**The policyholder / shareholder split.** The I-E profit is charged at two rates: the **policyholders' rate**, fixed by
FA 2012 s.102(3) as the rate of income tax at the **basic rate** applying in England, Wales and Northern Ireland —
**the Scottish basic rate does not apply** — and the **main corporation tax rate** on the shareholders' share
[REG-R18 LAM06010]. s.103 determines the split: for a **mutual, the whole I-E profit is attributable to policyholders**;
otherwise the I-E profit is compared with the adjusted amount of BLAGAB trade profit, the first slice up to that amount
being charged at the shareholder rate and the balance at the policyholder rate, with no policyholders' share where the
adjusted amount equals or exceeds the I-E profit [REG-R18 LAM06020]. HMRC's own worked illustration uses **2018 rates**
and states that "with CT rates below the basic rate of income tax" attributing more profit to trade profit no longer
increases the tax charge — **a statement that was true when written and is not true at the access date**, the main CT
rate being 25% and the basic rate 20% [REG-R18 LAM01160][REG-R110]. Record the direction of the incentive as
period-dependent; do not restate HMRC's sentence as current. Allocation between BLAGAB and non-BLAGAB runs through two
separate "**commercial allocation**" regimes — one for I-E items, one for trade profits — with an **overriding
consistency requirement** that "the overall effect of the methods taken together must be fair" [REG-R18 LAM05020]. A UK
model must therefore tag every projected cash flow, asset and liability with a **BLAGAB / non-BLAGAB flag** and produce
an allocation basis used consistently across income, gains and trade profits.

**Deferred tax exists on two balance sheets, on two different models, and that is what drives LACDT.** FRS 102 Section
29 recognises deferred tax on **timing differences** — differences between taxable profits and total comprehensive
income arising from income and expenses entering tax assessments in different periods — expressly **not** on
balance-sheet temporary differences, with no deferred tax on permanent differences and measurement at rates enacted or
substantively enacted at the reporting date [REG-R102]. Valuation 11 recognises deferred tax on **all** assets and
liabilities, **including technical provisions**, measured as **the difference between the Solvency UK value and the tax
value**, with a positive deferred tax asset recognised only where future taxable profit is probable, taking account of
carry-forward time limits [REG-R39]. **The two balances are structurally different numbers for the same company**, so a
UK model that projects deferred tax must carry **three liability measures per period — accounts, tax and Solvency UK —
not two**. Two UK GAAP anti-double-count rules bind alongside: where the long-term business provision or the linked
provision has had regard to **the timing of tax relief or the tax obligation**, that effect must be **excluded from the
determination of deferred tax** [REG-R100]. The consequence downstream is `Adj_DT`: LACDT requires a **post-stress tax
balance sheet**, re-running the Solvency-UK-versus-tax comparison after an instantaneous loss of
`BSCR + Adj_TP + SCR_operational` and reporting the change in net deferred taxes, with **no benefit taken for an
increase in deferred tax assets** [REG-R62]. Separately, an **IFRS 17 transitional amount** — the difference between
accumulated profits in the first IFRS 17 balance sheet and in the last pre-IFRS 17 balance sheet, apportioned between
long-term and other business and then between BLAGAB and non-BLAGAB by a commercial method consistent with the s.98 and
s.115 methods — is **spread over 10 years** from the first day of the first IFRS 17 accounting period [REG-R108]. **UK
GAAP reporters are unaffected by that change** [REG-R18 LAM16010].

---

## What this means for a liability cash flow model

Consolidating, UK regulatory reporting, accounting and capital need the following from the projection.

1. **A cash flow vector, not a present value.** The matching adjustment is the difference of two internal rates of
   return on the same liability cash flows, and MALIR 3 requires **600 monthly buckets in four streams per MA
   portfolio**. A model whose public interface is a scalar best estimate cannot compute an MA at all
   [REG-R2][REG-R44][REG-R91].
2. **The same vector discounted on at least five bases** — basic, basic + MA, basic + VA (with extrapolation re-struck
   on the VA-adjusted forwards), basic + TMIR adjustment, and the post-TMTP technical provisions — plus the SFCR's
   change-to-zero re-runs. The curve is an input, not an assumption [REG-R1][REG-R2][REG-R57][REG-R84].
3. **Eight separately-identifiable cash flow streams**, never netted into one line, including intermediary payments,
   payments to and from investment firms for linked benefits, and policyholder-charged tax [REG-R41].
4. **Two expense bases** — the going-concern basis TPFR 16.4 requires for the best estimate, and whatever the
   no-new-business reference undertaking uses for the risk margin, which no source specifies [REG-R41][REG-R1].
5. **A per-contract boundary flag with the test that produced it**, re-derived when product terms change rather than
   stored as a product constant; and reinsurance recoverables computed on the **same** boundaries [REG-R41].
6. **A re-runnable best estimate parameterised by assumption set** — mortality, morbidity, recovery, persistency, lapse,
   expense, expense inflation, benefit escalation and discount curve all arguments, not hard-coded tables — returning
   the best estimate **without the risk margin**, plus a per-policy or per-group flag for **which direction of each
   stress increases technical provisions**, because most stresses apply only to that subset [REG-R62].
7. **A separately determined future discretionary benefits amount**, per fund and in total, used three times: the LACTP
   cap, the ring-fenced-fund SCR adjustment, and the MCR's negative-coefficient term [REG-R41][REG-R62][REG-R78].
8. **Gross and ceded produced separately, never netted**, with recoverables split SPV / finite / other, a settlement
   timing lag, and a counterparty default adjustment per counterparty and per line of business with an LGD **not below
   50%** [REG-R1][REG-R41].
9. **Per-contract capital at risk** — the amount currently payable on death or disability plus the EPV of further
   amounts on immediate death or disability, less the best estimate, **floored at zero per contract** — which requires a
   "sum payable on immediate death or disability" attribute on every model point, distinct from the projected death
   benefit [REG-R78].
10. **For with-profits, a retrospective asset-share roll-up as well as a projection.** The Surplus Funds default basis
    is a ten-item cumulative accumulation per policy to the valuation date — **the one place in this library where a
    model must carry history rather than project forward** — with a prospective fallback clamped to what the
    retrospective calculation would have allowed [REG-R45][REG-R46].
11. **A multi-year projection of the whole stack**: own funds, SCR, MCR, risk margin run-off and TMTP run-off, for the
    ORSA, for IR.05.10, and — the only rule-mandated case — for a recovery plan or finance scheme
    [REG-R92][REG-R90][REG-R82].
12. **Three liability measures per period, not two** — Solvency UK, the accounts, and tax — because deferred tax under
    Valuation 11 is measured on the Solvency-UK-versus-tax difference while FRS 102 measures it on accounts timing
    differences [REG-R39][REG-R102].

**The couplings are what make this harder than a one-way hand-off.** In each of these a regulatory item feeds *back*
into the liability model rather than consuming its output.

- **Most SCR stresses are a re-run of the liability model, not a factor on its output.** Every life and SLT health
  sub-module, the interest rate sub-module and the MA spread sub-module require a full revaluation of the best estimate
  under changed assumptions [REG-R62]. The count is multiplicative: (scenario-based sub-modules) × 2 for gross and net ×
  (ring-fenced funds + MA portfolios + 1), plus the assumption permutations inside the lapse and interest-rate maxima.
  **That, not the size of any single stress, decides whether a projection engine is fit for standard-formula
  reporting.**
- **The MA spread scenario changes the discount rate the model is using.** `3D25` requires the technical provisions to
  be **recalculated to take account of the impact on the amount of the matching adjustment**, so the stress reaches
  back into the discounting layer rather than only into asset values [REG-R62].
- **The risk margin needs a projected SCR, and the projected SCR is a different undertaking's.** `SCR(t)` must be the
  reference undertaking's notional SCR — basic curve, no interest rate risk, no LACDT, minimise-market-risk assets — and
  **the Delegated Regulation's simplification hierarchy was not restated**, so there is no sanctioned proxy
  [REG-R1][REG-R41][REG-R44].
- **LACTP is a second complete pass, and LACDT is a post-stress tax balance sheet.** `BSCR − nBSCR` is the whole BSCR
  recomputed with FDB responsive and management actions live; `Adj_DT` then requires the Solvency-UK-versus-tax
  comparison to be re-struck after an instantaneous loss that itself depends on `Adj_TP` [REG-R62].
- **Scenario selection in four sub-modules is made on the net run and the gross number follows it** — so the two runs
  are not independent and cannot be parallelised naively [REG-R62].
- **MA eligibility testing needs a mortality-stressed best estimate.** The 5% cap in MA 2.2(3) is tested by running the
  prescribed mortality stress on the MA obligation portfolio, applying it **only to policies where it increases
  technical provisions**, and reporting the percentage increase — a valuation-layer stress that decides a *discounting*
  question, and one that IRR.22.03 requires to be reported annually [REG-R2][REG-R91].
- **The ring-fenced fund notional SCR is the whole exercise repeated per perimeter, with the scenario chosen
  firm-wide.** A fund's notional SCR can be driven by a scenario that is not the worst for that fund, and the resulting
  notional SCR then feeds *back* into own funds through the Own Funds 3L deduction — so a capital-structure number
  depends on a per-fund model run [REG-R62][REG-R77].
- **TMTP is a balance-sheet adjustment that nonetheless needs projections**: the risk-margin and dynamic portions must
  be projected to 1 January 2032 to compute the run-off accelerator, and that projection is the Chief Actuary's
  methodology choice under TPFR 27 [REG-R3][REG-R59].
- **The ORSA requires the entire stack projected twice** — with and without the MA, VA, risk-free transitional and TMTP
  (CGB 3.8(4)) — over a horizon the PRA describes as a three-to-five-year forecast, including reverse stress testing
  [REG-R92][REG-R95].
- **The distributable-earnings pattern comes off the prudential balance sheet, not the accounts**, and the s.833A(5)
  deductions require the **ring-fenced fund surplus and the MA portfolio surplus** to be projected as separate
  quantities [REG-R104].

Architecture guidance, the recursions and the reconciliation checks are in `uk/regulatory/technical-notes.md`,
"Implementation notes and model architecture" and "Validation and reconciliation checks".

---

## Product applicability

`x` = the item directly binds the product; `(x)` = binds conditionally, partially, or only through one component;
`—` = expressly excluded by the cited source; `?` = treatment genuinely unsettled in the documents retrieved; blank =
not indicated by the sources read, or not applicable by construction. Marks are for the **representative design
specified in this library**, not for every UK contract carrying the product name. Columns are `uk/products/` names
abbreviated: TA = term-assurance, CI = critical-illness, IP = income-protection, WOL = whole-of-life, WP = with-profits,
ULB = unit-linked-bond, PA = pension-annuity. Assembled from the applicability sections of all seven research files,
resolved at product level by `uk/_research/uk-product-regulatory-applicability.md`.

| Item | TA | CI | IP | WOL | WP | ULB | PA |
|---|---|---|---|---|---|---|---|
| Best estimate, TP 3.1 [REG-R1] | x | x | x | x | x | x | x |
| Technical provisions as a whole, TP 2.5(2) / TPFR 22 [REG-R1][REG-R41] | — | — | — | — | — | (x) | — |
| Contract-level repricing test, TPFR 3.3(3) [REG-R41] | (x) | x | x | (x) | (x) | | — |
| TPFR 3.5 savings-contract boundary cut [REG-R41] | — | — | — | — | — | ? | — |
| TPFR 3.6 / 26.7 unbundling [REG-R41] | (x) | ? | (x) | (x) | (x) | (x) | — |
| Going-concern expense basis, TPFR 16.4 [REG-R41] | x | x | x | x | x | x | x |
| Options and guarantees, TP 9.2 / TPFR 17 [REG-R1][REG-R41] | (x) | (x) | (x) | x | x | x | (x) |
| Scenario-dependent (stochastic) method, TPFR 19.4–19.5 [REG-R41] | — | — | (x) | (x) | x | (x) | (x) |
| Dynamic policyholder behaviour, TPFR 11.1 [REG-R41] | (x) | (x) | (x) | x | x | x | — |
| Future management actions, TPFR 8 [REG-R41] | (x) | (x) | (x) | (x) | x | x | (x) |
| FDB determined separately, TPFR 10.1 [REG-R41] | | | | (x) | x | | (x) |
| Reinsurance recoverables + CDA, 50% LGD floor, TPFR 23–24 [REG-R41] | x | x | x | x | (x) | (x) | x |
| Surplus-funds carve-out from TP, TP 9.1(3) / SF 2.1 [REG-R1][REG-R45] | — | — | — | (x) | x | — | (x) |
| **Negative best estimate permitted (no floor)** [REG-R41][REG-R115] | x | x | (x) | (x) | — | (x) | — |
| Risk margin, CoC 4%, λ = 0.9 floored at 0.25 [REG-R1][REG-R4] | x | x | x | x | x | x | x |
| Reference undertaking applies no MA/VA/TMIR/TMTP [REG-R1] | (x) | (x) | (x) | (x) | (x) | (x) | x |
| Basic GBP risk-free curve [REG-R54][REG-R55] | x | x | x | x | x | x | x |
| Extrapolation beyond the last liquid point bites [REG-R56] | (x) | (x) | x | x | x | — | x |
| Volatility adjustment (permission-dependent) [REG-R1] | (x) | (x) | (x) | (x) | (x) | (x) | — |
| **MA — whole-contract eligibility, MA 2.2** [REG-R2] | — | — | — | — | — | — | x |
| **MA — eligible-element route, MA 1.2 / 2.5** [REG-R2] | — | — | x | — | x | — | — |
| 5% mortality-risk cap, MA 2.2(3) / 2.4 [REG-R2] | — | — | (x) | — | (x) | — | x |
| MA attestation; MAIA; MA breach reduction [REG-R2][REG-R8] | — | — | (x) | — | (x) | — | x |
| TMTP [REG-R3] | (x) | — | (x) | x | x | (x) | x |
| TMIR [REG-R57] | (x) | — | (x) | x | x | (x) | — |
| **Life underwriting module `3B` applies at all** [REG-R62] | x | ? | — | x | x | x | x |
| **Health underwriting module `3C` applies at all** [REG-R62] | — | ? | x | — | — | — | — |
| Mortality `3B1` [REG-R62] | x | | — | x | x | (x) | — |
| Longevity `3B2` [REG-R62] | — | | — | (x) | (x) | — | x |
| Lapse **up** `3B6.2` / `3C16.2` [REG-R62] | x | x | x | (x) | x | x | — |
| Lapse **down** `3B6.3` / `3C16.3` [REG-R62] | (x) | (x) | (x) | x | x | (x) | — |
| Mass lapse, 40% limb `3B6.6(2)` / `3C16.6` [REG-R62] | x | x | x | (x) | x | x | — |
| Mass lapse, 70% limb `3B6.6(1)` (RAO class VII only) [REG-R62][REG-R64] | — | — | — | — | — | — | — |
| Life catastrophe `3B7.1` [REG-R62] | x | | — | x | x | (x) | — |
| Health disability-morbidity `3C13.1` [REG-R62] | | ? | x | | | | |
| Health revision `3C15.1` (inflation trigger) [REG-R62] | | — | x | | | | |
| Health catastrophe — pandemic `3C20` [REG-R62][REG-R73] | | (x) | x | | | | |
| Interest rate up / down `3D5` / `3D6` [REG-R62] | x | x | x | x | x | (x) | x |
| Equity `3D9` + symmetric adjustment [REG-R62] | — | — | — | (x) | x | x | (x) |
| **Spread on an MA portfolio `3D25` (recomputes the MA)** [REG-R62] | — | — | (x) | — | (x) | — | x |
| Counterparty default type 1 `3E13` [REG-R62] | x | x | x | (x) | (x) | (x) | x |
| Operational — `Op_provisions` 0.45% leg [REG-R62] | x | x | x | x | x | — | x |
| Operational — `0.25 × Exp_ul` leg [REG-R62] | — | — | — | (x) | (x) | x | — |
| **LACTP `Adj_TP`** [REG-R62] | — | — | — | (x) | x | — | — |
| LACDT `Adj_DT` [REG-R62] | x | x | x | x | x | x | x |
| **RFF notional SCR** [REG-R62][REG-R71] | — | — | — | (x) | x | — | — |
| **MA-portfolio notional SCR** [REG-R62] | — | — | (x) | — | (x) | — | x |
| No diversification between perimeters, `9.1(9)` [REG-R62] | — | — | (x) | (x) | x | — | x |
| USP available (revision risk only) [REG-R65] | — | — | (x) | — | — | — | (x) |
| Reconciliation reserve [REG-R77] | x | x | x | x | x | x | x |
| **Surplus funds as a Tier 1 unrestricted item** [REG-R77] | — | — | — | (x) | x | — | (x) |
| **RFF / MA deduction from the reconciliation reserve, 3L** [REG-R77] | — | — | (x) | (x) | x | — | x |
| **EPIFP** [REG-R77][REG-R86] | — | — | — | — | — | — | — |
| MCR corridor; AMCR £3.5m (long-term) [REG-R78] | x | x | x | x | x | x | x |
| MCR `TP_l2` FDB, the negative coefficient [REG-R78] | — | — | — | (x) | x | — | (x) |
| MCR `TP_l3` linked liabilities [REG-R78] | — | — | — | (x) | (x) | x | — |
| MCR capital at risk, floored at zero **per contract** [REG-R78] | x | x | (x) | x | (x) | (x) | (x) |
| IR.12.01 / IR.12.04 / IR.14.01 [REG-R89] | x | x | x | x | x | x | x |
| **IR.12.05 / IR.12.06 with-profits templates** [REG-R90] | — | — | (x) | (x) | x | (x) | (x) |
| IR.05.10 excess capital generation [REG-R84][REG-R90] | (x) | (x) | (x) | (x) | (x) | — | (x) |
| **IRR.22.02 / IRR.22.03 / MALIR 1–7** [REG-R91] | — | — | (x) | — | (x) | — | x |
| IR.26.03 / IR.26.04 SCR underwriting risk [REG-R84] | x / — | ? / ? | — / x | x / — | x / — | x / — | x / — |
| **ORSA with and without MA/VA/transitionals** [REG-R92][REG-R95] | x | x | x | x | x | x | x |
| With-Profits Actuary, SMF20a [REG-R93][REG-R94] | — | — | (x) | (x) | x | (x) | (x) |
| FRS 103 insurance-contract scope [REG-R99] | x | x | x | x | x | (x) | x |
| **FRS 103 ¶3.7 DAC required** [REG-R99][REG-R105] | x | x | x | x | — | (x) | x |
| FRS 103 ¶3.10 no DAC in with-profits funds [REG-R99] | | | | (x) | x | | (x) |
| **UK GAAP surrender-value / non-negative floor** [REG-R100] | x | x | x | x | x | x | x |
| **IFRS 17 general measurement model** [REG-R106] | x | x | x | x | | | x |
| **IFRS 17 variable fee approach** [REG-R106] | | | | (x) | x | x | |
| IFRS 17 coverage-unit basis settled? [REG-R106] | x | x | x | x | x | x | ? |
| **Tax — BLAGAB / I-E** [REG-R17][REG-R18] | (x) | (x) | (x) | x | x | x | — |
| **Tax — non-BLAGAB trade basis** [REG-R17][REG-R18] | x | x | x | (x) | (x) | | x |
| **CA 2006 s.833A distributable profits** [REG-R104] | x | x | x | x | x | x | x |

**PRA product reporting codes** for IR.14.01 [REG-R89]: TA **404 / 414 / 424 / 434**; CI **444 / 454** (accelerated,
guaranteed / reviewable) and **464 / 474** (standalone); IP **494 / 504 / 514 / 524**, the last being claims in payment;
WOL **104 / 102 / 100 / 101**; WP **111 / 100 / 101 / 120 / 121**; ULB **112** (113 index-linked, 114 non-profit); PA
**724 / 734 / 720 / 722**. Two conventions bite: "single premium bond" **includes 'investment bond' and 'with-profits
bond'**, and the whole-life and endowment codes **exclude single premium bonds "which are technically whole of life"**,
so this library's with-profits **bond** reports under 111 rather than a whole-of-life code; and **IL "excludes RPI / CPI
linked policies"**, so an RPI-linked annuity is **not** index-linked business for reporting.

**Notes on every non-obvious mark.**

- **TPFR 3.3(3) is `x` for CI and IP but `(x)` for TA and WOL.** The long-term-underwriting carve-out only does work
  where the firm actually has a repricing right — i.e. on **reviewable-premium** CI and IP, where it is the difference
  between a boundary stopping at the next review and one running to the end of the term. On guaranteed-premium TA and
  WOL there is no repricing right, so the rule is engaged only in confirming a full-term boundary. **The
  technical-provisions stream bolded TA as well; this is a refinement, and the divergence is recorded rather than
  silently resolved** [REG-R41].
- **TPFR 3.5 is `?` for ULB.** For the representative **single-premium** bond there are no future premiums for the rule
  to cut, so it is inert as specified; on a regular-premium variant it becomes live and genuinely unsettled, because
  whether a 100.1% death uplift is "a specified uncertain event that adversely affects the insured person" turns on the
  undefined "no discernible effect on the economics of the contract" qualifier. Marked `?` to force a drafter to state
  which variant is meant [REG-R41].
- **TP-as-a-whole is `(x)` for ULB alone** because only the unit-fund component of a linked contract is in principle
  replicable by the units held; TPFR 22.2 declares option-dependent cash flows, biometric-dependent cash flows and
  **all** servicing expenses non-replicable, which disposes of every other product and of the rest of ULB [REG-R41].
- **Stochastic valuation is `—` for TA and CI.** A level-premium term or standalone CI contract with no surrender value
  and no financial option has no scenario-dependent asymmetry. IP earns `(x)` through index-linked escalation and
  economic dependence of claim inceptions, PA through inflation-linked escalation, and **ULB is `(x)` rather than `x`**
  because the base design carries no guarantee — electing a GMDB or capital protection makes it `x` [REG-R41].
- **The negative-best-estimate row splits.** `x` for TA and CI, routinely negative at issue; `(x)` for IP because the
  active-life cell can be negative while the claims-in-payment cell cannot; `(x)` for WOL because the over-50s
  guaranteed-acceptance cell is the paradigm lapse-supported negative reserve while the underwritten cell is not; `(x)`
  for ULB because the **non-unit** component is routinely negative while the total is not; `—` for PA, a single-premium
  annuity in payment having no future premium inside the boundary. **WP is `—` here, narrowing the technical-provisions
  stream's `(x)` on product grounds: guaranteed benefits plus FDB dominate and the estate is carved out of technical
  provisions entirely. The divergence between the two research streams is recorded, not resolved** [REG-R41][REG-R115].
- **CI's life/health rows are `?`, and IR.26.03 / IR.26.04 follow.** The derivation set out under "The solvency capital
  requirement" would put CI in the health module, but no retrieved document states it and the line-of-business list that
  would settle it sits in the unretrieved Annexes [REG-R73]. `?` is carried rather than a guess, and the reporting rows
  are marked `?` to match — a firm cannot point a supervisor at a derivation.
- **Mortality is `(x)` for ULB and `—` for IP and PA.** The bond carries a 100.1%-of-fund death benefit, so capital at
  risk is 0.1% of the fund — non-zero but immaterial. IP's mortality exposure runs through the **health** module, not
  `3B1`. PA is `—` because higher mortality *reduces* annuity provisions, so the sub-module's own filter excludes it.
- **Lapse direction is product-specific, and this is where a uniform mark misleads.** The `3B6.2` and `3B6.3` filters
  route a policy to one scenario or the other according to whether discontinuance increases or decreases technical
  provisions without the risk margin. A cell whose discontinuance **decreases** technical provisions without the risk
  margin — the over-50s whole of life once its provision has turned positive — is stressed by lapse **down**, and its
  40% mass charge is nil. A cell with a **negative** best estimate and no surrender value is the opposite case:
  discontinuance increases technical provisions, so it takes lapse **up** and the 40% mass event. **The SCR stream's
  matrix marked lapse up `x` uniformly across TA, CI, IP, WOL, WP and ULB; this matrix splits the direction per
  product, and the divergence is recorded**
  [REG-R62].
- **Mass lapse 70% is `—` everywhere.** The rule as corrected on 20 December 2024, effective 31 December 2024, reaches
  **RAO Schedule 1 Part II class VII (pension fund management) only**; under PS15/24 as originally published the ULB
  cell would have read `x` at 70%. Nothing in the seven-product set is class VII business. **The correcting statement
  conflicts with itself on the class list** — its narrative mentions class II and class VII while its conclusion and the
  live rule text name class VII only — and **PS15/24 ¶¶6.16 and 6.18 remain published and unamended**, so anyone reading
  PS15/24 alone gets the wrong scope [REG-R64][REG-R62][REG-R42].
- **Health revision is `x` for IP while life revision is `(x)` at best for PA.** The health scenario adds **inflation**
  to the legal-environment and state-of-health triggers, which an index-linked IP claim annuity has; the life scenario
  has no inflation trigger, so a level or RPI/LPI-escalating pension annuity is normally nil [REG-R62].
- **Health catastrophe pandemic is `x` for IP** because the sub-module requires a **permanent-disability benefit
  valuation** an ordinary IP projection does not produce — and it cannot be computed from this library's material
  because **the Annex XVI inputs were not retrieved** [REG-R62][REG-R73].
- **Interest rate is `(x)` for ULB.** The unit leg self-immunises; only the non-unit charge and expense stream is
  rate-sensitive. Independently corroborated by the PRA's exclusion of unit-linked technical provisions from its
  relevant-currency materiality test [REG-R55].
- **Operational risk is a clean split.** The provisions leg deducts unit-linked technical provisions, so a pure
  unit-linked book contributes nothing to it (`—` for ULB), while the unit-linked expense leg is `x` for ULB and `(x)`
  for WOL and WP where unit-linked business is written alongside [REG-R62].
- **LACTP is `x` for WP only** because `Adj_TP` is capped at future discretionary benefits, which only participating
  business carries; `(x)` for WOL means a **with-profits** whole of life. **RFF rows are `—` for ULB** on the strength
  of the EIOPA guideline that conventional unit-linked and index-linked products are generally outside RFF scope
  [REG-R80c]. **An MA portfolio is not an RFF** — the Glossary excludes it expressly — but it attracts the identical Own
  Funds 3L deduction and the identical no-diversification treatment, which is why PA carries `—` on the RFF rows and `x`
  on the MA-portfolio and 3L rows [REG-R80][REG-R62][REG-R77].
- **Surplus funds and the MCR participating terms are `(x)` for WOL and PA** because they turn on **"long-term insurance
  obligations with profit participation"**, not on the product name: a with-profits WOL or a with-profits deferred
  annuity written inside a with-profits fund is in; the same product written non-profit is not [REG-R45][REG-R78].
- **MCR capital at risk is `(x)` for IP, WP, ULB and PA.** The term is defined by what the firm "would currently pay on
  **death or disability**". IP engages the disability limb but **the rule does not say how to express an income stream
  as a currently-payable amount**. ULB and WP carry it only through the death benefit in excess of the fund or asset
  share. PA carries it only where there is a death benefit (guarantee period, value protection, spouse's reversion),
  where the sign is typically negative and the **per-contract** zero floor bites [REG-R78].
- **EPIFP is `—` for every product, and that is not a product judgement**: the requirement has been removed from
  Solvency UK reporting and disclosure altogether [REG-R86][REG-R77].
- **TMTP and TMIR marks below `x` are materiality judgements, not legal ones.** The *legal* availability of TMTP turns
  only on whether the obligations were qualifying obligations on 31 December 2024 [REG-R3]. The `(x)` marks for TA, IP
  and ULB, and the `—` for CI, rest on a judgement that those pre-2016 blocks are small relative to the reserve; **the
  research records those marks as [unverified] and they are carried forward as such**.
- **The with-profits templates carry `(x)` outside WP** because IR.12.05 / IR.12.06 are triggered by the firm's
  with-profits net BEL exceeding £500m, and any of the other products **written in participating form** falls into a
  with-profits fund and therefore into the WPBR/FPRL decomposition; IR.12.06's row for "future costs of financial
  options such as guaranteed annuity rates" is where a WOL or WP contract's GAR is reported [REG-R90].
- **FRS 103 scope is `(x)` for ULB** because a unit-linked bond frequently fails the significant-insurance-risk test and
  is an **investment contract** outside FRS 103, in FRS 102 Sections 11/12 and 23 — HMRC records exactly that treatment
  [REG-R18 LAM01100]. On the representative 100.1% death uplift the classification is a per-design determination, not a
  product-family fact, and **FRS 103 Appendix II was not read** [REG-R99].
- **The UK GAAP floor row matters most for TA, CI and ULB**, because those are the products where the Solvency UK number
  is routinely negative (TA, CI) or has a routinely negative component (ULB), so the non-negative / surrender-value
  floor produces the **largest divergence between the two ledgers** [REG-R100]. The row is `x` for all seven because
  the floor bites the reported provision on every product — but **its source is the non-mandatory Implementation
  Guidance** (IG2.41, IG2.47), which accompanies but is not part of FRS 103; the floor the standard itself imposes is
  the liability adequacy test [REG-R100][REG-R101].
- **IFRS 17 VFA is `(x)` for WOL** meaning a participating or unit-linked WOL; a non-profit WOL is GMM. **PA's
  coverage-unit row is `?` deliberately**: the requirement to identify coverage units binds, but the right answer for an
  annuity is an identified priority issue with continuing divergence [REG-R106].
- **Tax is `(x)` on the BLAGAB row for TA, CI and IP** to cover pre-2013 back-books: protection business written from
  1 January 2013 is excluded from BLAGAB and taxed on a trading basis, but earlier policies continue as BLAGAB unless an
  election is made [REG-R18 LAM01080]. **`—` for PA** because a pension annuity is pension business and no policyholder
  fund tax enters the projection — **a change from the technical-provisions stream's `(x)` on the policyholder-tax row,
  justified by the tax stream's `—` on the BLAGAB rows for PA, and recorded as a divergence** [REG-R18][REG-R41].

---

## Known gaps and caveats

**Documents not retrieved, named at the point of use above and collected here.** The **Annexes to the SCR – Standard
Formula Part** [REG-R73] — with them go the Annex XVI ratios for the health catastrophe sub-modules, the geographical
diversification annex, and **the numbered line-of-business list**, without which the CI life/health classification
cannot be settled. The **four monthly PRA technical-information spreadsheets** [REG-R54], which is why **no UFR, no
fundamental spread, no probability of default, no cost of downgrade, no VA and no symmetric adjustment value appears
anywhere in this library**, and why the USD and CAD last liquid points and the per-maturity DLT flags are absent
[REG-R56]. **IFRS 17 itself**, paywalled [REG-R107]. **INSPRU 1.3.40 and 1.3.190 as at 31 December 2015**, the
definitions behind FRS 103's "realistic value of liabilities" — INSPRU 1.3 renders as a "Deleted" stub, and **nobody in
this library has read them**, so that term is a citation rather than a specification [REG-R116][REG-R99]. **The PRA
Rulebook Glossary definition of "surplus funds"**, after ten URL forms all failed [REG-R45][REG-R77]. **MALIR 4–7**,
read only at title level, MALIR 5 containing the quantitative matching tests a pension annuity model must pass — **the
single largest unread block in the reporting stream** [REG-R91]. **PS15/24 and its appendices** were not fetched in the
reporting stream, so statements about *why* a template exists rest on the near-final PS3/24 rather than the final
instrument [REG-R86][REG-R6]. **SS8/24**, cross-referenced by the IR.12.01 instructions as the source of a permitted
in-year risk-margin approach, was not retrieved and its title is not asserted [REG-R89]. **SoP4/24** (capital add-on
thresholds), **SoP11/24** (USP permissions), **SoP6/24** (reporting waivers), **SoP1/19** (which determines how far the
EIOPA ring-fenced funds guidelines apply in the UK), **SS8/18** (internal-model modelling of the MA), **SS1/20 chapters
2–8**, **SS3/17**, **SS20/16** (whose title conflicts between two retrieved sources — "counterparty credit risk" on the
Bank's landing page, "counterparty default risk" in SS18/16 ¶2.1), **SS9/14**, **SS22/15**, **SS41/15's underlying EIOPA
guideline sets**, **FRS 103 Appendix II** (the significant-insurance-risk test) and **FRS 103 IG Section 3** were all
either not retrieved or retrieved only as landing pages [REG-R69][REG-R70][REG-R88b][REG-R80c][REG-R119][REG-R120][REG-R48][REG-R99][REG-R100].
**SS18/16 was read only at grep level**; everything about it beyond one quoted observation is **[unverified]**
[REG-R48]. **The current November 2024 SS17/16 PDF could not be retrieved**, so its validation paragraph numbers come
from the superseded February 2024 version and must be re-verified [REG-R97]. **SS1/24 was retrieved only as a
publication page in the reporting stream**, though the own-funds stream retrieved its substance [REG-R81b].

**Numbers deliberately not transcribed.** No risk-free rate, fundamental spread, matching adjustment, volatility
adjustment, symmetric adjustment or ultimate forward rate value appears in this file or anywhere in this directory. No
SCR stress size, correlation coefficient, spread factor, concentration threshold or MCR coefficient is *originated*
here: every such number lives in `uk/regulatory/technical-notes.md` with its rule reference, and this file states
concepts and drivers only. The **Annex XVI health-catastrophe ratios cannot be stated at all** because they were not
retrieved by any stream. **COBS 20 target-range percentages, market value reduction bounds and required percentages are
not stated**: COBS 20.2 could not be re-fetched — one attempt returned HTTP 500 and another returned COBS 20.3 content —
so only COBS 20.2.17R, 20.2.55R and 20.2.56R are named, from the frozen [REG-R9] record and from the PRA's own
cross-reference in the IR.12.05 instruction [REG-R9][REG-R90]. The **`[w]`, `[x]`, `[y]`, `[z]` attestation materiality
metrics are left blank by the PRA** and are not invented [REG-R8]. **No IFRS 17 confidence level, coverage-unit formula
or transition proxy is stated**, because the standard was never read [REG-R107][REG-R106]. And no **INSPRU-as-at-2015**
valuation interest rate, zillmer limit or mortality basis is stated anywhere [REG-R99]. And the **risk-mitigation
qualitative criteria in `SCR-SF 3G2`–`3G9`** — effective transfer, material basis risk, counterparty status, collateral
and guarantee conditions — **were surveyed and not transcribed**, so no `SCR-SF 3G` admissibility test is stated
anywhere in this library; only `3G1.1` and `3G1.2` are carried [REG-R62].

**Conflicts recorded and not resolved.** SS5/24 ¶1.7 directs firms to "Chapters 6, 7 and 11 of the Technical
Provisions", but Chapters 6 and 7 are the **deleted** matching-adjustment chapters as at 05/08/2026 — only the Chapter
11 reference is live [REG-R47][REG-R1]. **"Market value" has two anchors**, the Glossary's generally-accepted-accounting-practice
definition and Valuation 2.1's Article-75 standard, and TPFR 22 uses the term for TP-as-a-whole [REG-R43][REG-R39][REG-R41].
**TPFR 16.4 versus TP 4B.1(5)** — new business assumed for expenses, no new business in the reference undertaking — with
no source explaining how to set the reference undertaking's expenses [REG-R41][REG-R1]. **IRPR reg 3(1) versus PRA
practice on publication frequency** — the regulation requires publication every quarter, the technical-information page
states monthly publication; both are verified from primary text and neither document says the statutory duty is a floor
rather than a cap [REG-R44][REG-R54]. **SCR-SF 3.3A(1)(d) versus
3.3A(2)(a)** on management actions inside a scenario [REG-R62]. **Own Funds Chapter 4 versus Chapter 4A**, two
non-equivalent statements of the tier limits, both live, reconciled only by a supervisory statement [REG-R77][REG-R83].
**MCR 3.1B versus MCR 3.3** on whether the corridor SCR includes capital add-ons [REG-R78]. **PS3/24 ¶4.70 versus the
final Reporting Part** on whether S.13.01 survives as IR.13.01 [REG-R86][REG-R84][REG-R88]. **The IR.05.10 scope test**,
stated differently in the Rulebook and in the instruction file on both the measurement window and the inclusion of SLT
health business [REG-R84][REG-R90]. **SS41/15 still refers to the abolished RSR** [REG-R95b][REG-R86]. **The mass-lapse
correcting statement conflicts with itself on the class list**, and PS15/24 ¶¶6.16 and 6.18 remain unamended
[REG-R64][REG-R42]. **The three inter-stream matrix divergences** — TPFR 3.3(3) for TA, the negative-best-estimate mark
for WP, and the lapse direction across six products — are each recorded in the notes to the applicability matrix rather
than silently resolved.

**[unverified] items carried forward and not upgraded.** The **line-of-business mapping of the seven library products**,
which is a drafter's inference from TPFR 26.2, 26.3 and the Annex 1 definitions, Annex 1 naming no products [REG-R41].
The **CI module derivation**, explicitly a chain of textual reasoning that no retrieved document states [REG-R62].
The **TMTP and TMIR materiality marks** for TA, CI, IP and ULB, which are judgements about the size of pre-2016 blocks,
not legal conclusions [REG-R3][REG-R57]. **SS18/16's content** beyond one quoted observation [REG-R48]. The **CQS 5-and-6
merger in the spread table**, the **missing percent sign in the unrated-bond formula**, the **non-monotonic downward
interest-rate shocks at maturities 14–20** and the **bracketing of the operational-risk premium formula** — all
transcribed as rendered, flagged as extraction defects and not silently corrected [REG-R62]. The statement that a
non-MA annuity book *could* take the volatility adjustment, which is a market-practice judgement rather than a rule
[REG-R55][REG-R1]. And the library's standing **[unverified]** items — the ICOBS chapter mapping for pure protection,
market-share claims — remain as recorded on the frozen reference page.

**Time-sensitive items to recheck before relying on this file.** **SCR-SF 6.5**, the LACDT transitional permitting an
increase in deferred tax assets to be used, is printed in the 05/08/2026 Rulebook view as running "for a transitional
period **ending 30 December 2025**", which on its face has expired, and **no PRA instrument confirming expiry or
extension was retrieved** [REG-R62]. **Own Funds rules 3A.1, 3B.1, 3C.1, 3D.1, 3E.1, 3F.1 and 3G.1 all carry live
"future version after 31/12/2026" markers**, and PS18/26's amended rule text sits in an appendix that **was not
retrieved** [REG-R77][REG-R87]. **CP4/26 Proposals 2, 3 and 4 have no recorded outcome**, so the admitted Own Funds
3C / 3L interaction defect stands [REG-R83c][REG-R87]. **PS18/26 replaces the MALIR return with a new MA template set
from the 31 December 2026 reference date**, moving to XBRL, and **removes claims management expenses from IR.14.01's
claims-paid
definition** from the same date; the replacement instruction files were not retrieved [REG-R87]. **Liquidity reporting
requirements come into force on 30 September 2026**, including a **monthly cash-flow mismatch template due within 10
business days of month end** and a short-form version due **within one business day**, with a standing capability to
report **daily** in stress — **the thresholds deciding which firms are in scope were not transcribed** [REG-R87][REG-R84].
**The Preparations for Solvent Exit Part came into force 30 June 2026** [REG-R98]. **FRS 102 and FRS 103 Periodic Review
2024 amendments are effective for periods beginning on or after 1 January 2026**, and an FRS 102 "Adapted formats"
amendment published 18 February 2026 is effective 1 January 2027 — **that amendment document was not fetched and whether
it touches the Schedule 3 insurance formats was not determined** [REG-R101][REG-R102]. **The UKEB post-implementation
review of IFRS 17 is committed to report by 1 January 2028** and had not reported at the access date [REG-R38].

**Two corrections this directory makes to assumptions the library previously carried.** First, the **"cited-not-specified"
scope note on capital** in `uk/references/regulatory-and-actuarial-references.md` is superseded, as stated in the front
matter. Second, and more consequentially for anyone porting U.S. framings across, **the library must not assume any UK
statutory-accounts new-business strain**: SI 2008/410 Schedule 3 para 13 **requires** DAC and FRS 103 ¶3.7 **requires**
deferral subject to recoverability, so the U.S. no-DAC story does not transfer [REG-R105][REG-R99].
