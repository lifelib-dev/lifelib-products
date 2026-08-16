# Individual Income Protection — Representative Product Specification (United Kingdom)

**Status:** Draft, 2026-08-03 (all cited sources accessed 2026-08-03).

**Scope note.** This is a *standardized composite specification* assembled for reference
liability cash-flow modeling. It does not describe any single insurer's product. Facts
carrying a source tag — [S#] (primary product documents) and [R#] (regulatory/actuarial
references), both numbered per `_research/income-protection.md` — resolve against
`sources.md` in this directory (numbering carried over verbatim; never renumbered).
[REG-R#] tags resolve against the cross-product reference library
`references/regulatory-and-actuarial-references.md` (its own R-numbering; research
provenance in `_research/regulatory-actuarial.md`). Values marked **[std]** are
standardizations introduced for the reference implementation; each [std] table row
carries a footnote giving the rationale and the observed range across insurers. Facts
the research file could not verify are flagged [unverified].

---

## Product overview and market role

UK individual income protection (IP) is the long-term "permanent health insurance"
contract: it pays a regular monthly benefit while the insured is incapacitated by
illness or injury, after a chosen deferred period, until recovery, death, the end of a
limited payment term, or policy expiry. Legally it is long-term insurance business —
RAO Class IV "Permanent health" requires contracts "expressed to be in effect for a
period of not less than five years" (or to normal retirement age) and non-cancellable
by the insurer except in contract-specified special circumstances [R6]. All six
sampled products satisfy this (explicit minimum 5-year terms at Aviva [S2], LV= [S4],
The Exeter [S9], Cirencester [S11]; Royal London 5–52 year term band [S6]).

Two structural families exist in the sampled market [S1]–[S12]:

- **Proprietary/mutual insurer products** (Aviva Income Protection+ [S1] [S2], LV=
  Income Protection / Budget IP [S3] [S4], Royal London Personal Menu Plan IP [S5] [S6],
  The Exeter Income First [S7] [S8], Vitality Personal Protection Plan IP Cover [S10]) —
  a monthly benefit chosen in £, financially underwritten against a banded percentage
  of pre-tax earnings.
- **Holloway-style friendly society contracts** (Cirencester Friendly Income Assured
  Enhanced [S11] [S12]) — benefit bought in units with age-costed premiums and optional
  participation in society surpluses accumulating a capital sum.

Own occupation is the primary incapacity definition at all six sampled insurers
[S1] [S3] [S5] [S7] [S10] [S12]. No sampled product has a cash-in or surrender value
([S4] [S5] [S7]; the exception is the Cirencester capital-sum option, which returns the
accumulated Member's Credit less an early-closure penalty [S11]). Waiver of the IP
premium during claim is standard, with mechanics varying by insurer
[S1] [S3] [S5] [S7] [S10] [S11]. Benefits from individual IP bought from taxed personal
income are currently free of income tax ([S4]; no tax or NI deducted [S7]; benefit
"currently free from tax", which motivates the ~60% replacement ceiling [S11]).

Distribution and conduct fall under FCA ICOBS as pure protection business [R9,
fetched_ok=false in the product research pass — verified via the shared library
[REG-R11]]; prudential valuation is under Solvency UK technical provisions [R7], and
the in-payment claims element is Matching Adjustment-eligible [R8].

The representative design specified below is a **full-term, guaranteed-premium,
own-occupation, RPI-escalating monthly-benefit IP on the Aviva/Royal London pattern**
(rationale in Variations across insurers). The 24-month limited-payment-term "budget"
variant, the Holloway unit-priced contract, and Vitality's health-linked premiums are
documented as variations, not the chassis.

---

## Representative specification

### Product identity and issue rules

| Parameter | Representative value | Basis |
|---|---|---|
| Design type | Individual income protection: long-term (Class IV) monthly-benefit contract, full cover to term, non-cancellable by insurer | [R6]; design family [S1] [S3] [S5] [S7] |
| Structural family | Proprietary/mutual monthly-benefit design (benefit chosen in £) | [S1] [S3] [S5] [S7] [S10]; choice **[std]** (1) |
| Incapacity definition | Own occupation: incapacity, caused by illness or injury, to perform the material and substantial duties of the own occupation | [S1] [S3] [S5] [S7] [S10] [S12] |
| Entry ages | 18–59 | [S1] [S2] [S6] [S9]; composite **[std]** (2) |
| Expiry age | Selected at outset, 50–70; base cell 65 | band [S2] [S4] [S6] [S7] [S9]; base-cell pick **[std]** (3) |
| Minimum term | 5 years | [S2] [S4] [S9] [S11]; legal floor [R6] |
| Premium basis | Guaranteed level (changes only via the escalation option) | [S1] [S3] [S5] [S7]; choice **[std]** (4) |
| Cash-in / surrender value | None at any time | [S4] [S5] [S7] |
| Cooling-off | 30 days, full premium refund; thereafter cancel any time without value | [S1] [S4] [S5] [S7] [S11] |
| Base model cell | Male, entry age 35, occupation class 1, earnings £40,000/yr, benefit £2,000/month, deferred period 26 weeks, expiry age 65, RPI escalation on, guaranteed premiums | **[std]** (5) |

Footnotes to [std] rows:

1. The monthly-benefit design is chosen over the Holloway unit-based design: five of
   six sampled products use it, and it is the mainstream adviser-sold chassis. The
   Holloway contract (unit-priced benefit, age-costed premiums, discretionary surplus
   participation) is documented under Variations [S11] [S12].
2. Observed entry-age ranges: 18–59 (Aviva [S1] [S2]; Royal London [S6]; The Exeter
   [S9]), 17–59 (LV= [S3] [S4]), 16 to before the 60th birthday (Cirencester [S11]);
   Vitality's IP entry ages are not stated in the fetched plan provisions (research
   gap) [S10]. 18–59 is the modal band.
3. Observed expiry rules: end between age 50 and the 71st birthday (Aviva [S2]);
   before 70 (LV= [S4]); maximum 70 (Royal London [S6]); selected finishing age 50–70
   (The Exeter [S7] [S9]); selected retirement age 50–70 or state retirement age if
   higher (Cirencester — the only sampled product with a State Pension age link)
   [S11]. The composite takes the common 50–70 band; 65 is a base-cell modeling pick
   inside it.
4. Guaranteed level premiums dominate the sampled mainstream [S1] [S3] [S5] [S7];
   reviewable premiums (fixed 5 years, then reviewed) and age-costed scales are
   documented under Variations [S1] [S4] [S6] [S7] [S10] [S11].
5. Pure modeling cell. £2,000/month = £24,000/yr against £40,000 earnings is a 60%
   replacement ratio, inside the 65%-band cap below (maximum benefit at these
   earnings: 0.65 × £40,000 / 12 = £2,166.67/month). Premium rates are not public
   (see Premiums, footnote 15).

### Benefit amount

| Parameter | Representative value | Basis |
|---|---|---|
| Chosen monthly benefit | Selected at outset; base cell £2,000/month | **[std]** (5); minimum cover £100/month [S6] |
| Maximum benefit (earnings cap) | 65% of the first £60,000 of pre-incapacity gross annual earnings + 50% of the excess | band structure and breakpoint [S1] [S2] [S5] [S7]; upper-band pick **[std]** (6) |
| Absolute cap | £20,000/month (£240,000/yr) | [S1] [S2]; pick **[std]** (7) |
| Earnings definition | Employed: pre-tax PAYE earnings incl. P11D benefits in kind; self-employed: pre-tax share of profits; working shareholders of companies with ≤3 other shareholder-directors may count dividends | [S1] [S3] [S4] [S5] [S11] |
| Earnings reference period | Last 12 months before incapacity | [S1]–[S7]; Royal London applies 3-year averaging for volatile earnings [S5] |
| Minimum benefit guarantee | £1,500/month, conditional on working ≥16 h/week at incapacity | mechanics [S1] [S2]; level pick **[std]** (8) |
| Over-insurance tolerance | Benefit paid in full if the assessed maximum ≥ 90% of the benefit amount | [S1] [S5]; LV= states it as a 10% tolerance [S3] [S4] |
| Offsets at claim | Continuing employer/business income (incl. sick pay and earned dividends), other insurance replacing income, pensions paid due to incapacity; state benefits NOT deducted | [S1] [S3] [S5] [S7] [S10] [S11]; composite list **[std]** (9) |
| Benefit taxation | Free of income tax to the individual under current law | [S4] [S7] [S11] |

6. Observed replacement formulas: 65%/45% around £60,000 (Aviva [S1] [S2]; The Exeter
   Income First [S7]); 65%/50% around £60,000 (Royal London [S5]); 60%/50% around a
   £5,000/month (£60,000/yr-equivalent) breakpoint (Vitality [S10]); flat 60% (LV=
   [S3] [S4]; Cirencester [S11]); the older Exeter generation used 60%/40% around
   £100,000 [S9]. The composite keeps the modal £60,000 breakpoint and 65% first
   band, and picks 50% for the upper band per the research file's representative
   design note (observed upper band 45–50%).
7. Observed absolute caps: £20,000/month = £240,000/yr (Aviva [S1] [S2]);
   £20,833/month level (LV= [S3] [S4]); £250,000/yr including all other IP (Royal
   London [S5] [S6]); £10,000/month (The Exeter [S7]); £16,666/month (Vitality [S10]).
   The Aviva round figure is adopted.
8. Observed minimum benefit guarantees: £1,500/month (Aviva ≥16 h/week [S1] [S2]; LV=
   less offsets, ≥16 h self-employed / ≥25 h employed [S3] [S4]; Vitality, ≥30 h
   employed / ≥20 h self-employed [S10]; Cirencester "up to £1,500" [S11]);
   £1,750/month (Royal London [S5]). Doctors/surgeons get doubled floors — £3,000
   (LV= [S3]; Vitality [S10]) or £3,500 (Royal London [S5]) — excluded from the
   composite. £1,500 with the Aviva ≥16 h/week condition is the market convention.
9. Each insurer's offset list differs in detail (e.g. Vitality deducts only 60% of
   continuing remuneration and explicitly exempts rental income and non-employment
   dividends [S10]; LV= deducts 60% of sick pay/pensions and 100% of other insurance
   [S3]; Aviva deducts other-insurance payments only above £50/month in total,
   taxable income net [S1]). The composite adopts the Aviva-style list headings
   without percentage haircuts. Universally, state benefits are not deducted
   [S3] [S4] [S7] [S9] [S10], though IP payments can reduce means-tested Universal
   Credit [S3] [S4] [S5].

### Deferred period and claim payment

| Parameter | Representative value | Basis |
|---|---|---|
| Deferred period menu | 4 / 8 / 13 / 26 / 52 weeks | [S6]; menu adoption **[std]** (10) |
| Base cell deferred period | 26 weeks | **[std]** (10) |
| Benefit payment | Monthly in arrears from the end of the deferred period (first payment ~1 month later); partial months pro-rated daily | [S1] [S3] [S10] |
| Claim notification | Within 8 weeks of incapacity, or before the deferred period ends if shorter | [S1]; composite **[std]** (11) |
| Payment term | Full term: benefit payable until recovery, death, no further loss of earnings, or expiry | [S1] [S3] [S5] [S7] [S10]; choice **[std]** (12) |
| Linked claims | Recurrence of the same cause within 52 weeks of payments stopping: deferred period waived, payments restart | window pick **[std]** (13) |
| Proportionate / rehabilitation benefit | On partial return to work: reduced benefit = (A − B) / A × C (definitions in Contractual mechanics) | formula [S7]; common structure [S1] [S3] [S5] [S10] [S11] |
| Terminal illness acceleration | Out of scope (variation) | [S5] [S11] |

10. Observed menus: 4/8/13/26/52/104 weeks plus dual deferred (Aviva [S1] [S2]);
    1/2/3/6/12 months (LV= [S4]); 4/8/13/26/52 weeks (Royal London [S6]); Day 1 to 52
    weeks (The Exeter [S7]); 7 days to 60 months plus dual deferred (Vitality [S10]);
    1–52 weeks plus Day One Accident Protection (Cirencester [S11]). The composite
    adopts the Royal London menu — the common core across all six. 26 weeks is chosen
    as the base cell: it aligns with the NHS sick-pay structure of 6 months' full pay
    then 6 months' half pay [S2] and is a directly supported IP11 rate split (DP26)
    [R1]. Dual deferred periods and occupation-specific sick-pay-linked deferreds
    (NHS, teachers) are out of scope [S1] [S3] [S5] [S7] [S10].
11. Observed notification deadlines scale with the deferred period: before 8 weeks of
    incapacity or before the deferred period ends if shorter (Aviva [S1]); 2 or 8
    weeks by waiting period, late notice restarts the waiting period (LV= [S3]); 2–8
    weeks by band (The Exeter [S7]); immediate to 2 months by band, claims notified
    >90 days after deferred-period end may be declined (Vitality [S10]); 7 days or 1
    month (Cirencester [S12]). The Aviva rule is adopted; notification has no cash
    flow effect in the reference model.
12. Full cover to term is the representative payment term per the research file's
    representative design. Limited payment terms of 12/24/60 months (24 months
    standard) are the budget variant — see Variations [S1] [S2] [S4] [S6] [S7] [S10].
13. Observed linked-claim windows: 12 months from end of the previous claim (Aviva
    [S1]); 6 months from return to work (LV= [S3] [S4]); 52 weeks from payments
    stopping, same cause and occupation (Royal London [S5]); 6 months (The Exeter
    [S7]; Vitality [S10]); 52 weeks from return to work (Cirencester [S11]). The
    composite takes 52 weeks (= the Aviva/Royal London long end of the observed
    6–12 month range), measured from payments stopping [S5].

### Premiums

| Parameter | Representative value | Basis |
|---|---|---|
| Payment method | Monthly Direct Debit | [S1] [S3] [S5] [S11] |
| Representative premium (base cell) | £35/month at issue | **[std]** (14) |
| Minimum premium | £5/month | [S4] [S6] |
| Premium guarantee | Guaranteed: level except for escalation-option increases (and changes in tax/legislation) | [S1] [S3] [S5] [S7] |
| Escalation (increasing cover) option | Benefit rises each policy anniversary by RPI (12-month change), capped 10%/yr, floored at 0; premium rises by 1.5× the benefit increase (max 15%/yr); increases continue during claim | mechanics [S1] [S2]; multiplier pick **[std]** (15) |
| Waiver of premium | Premiums payable during the deferred period; waived from the start of benefit payments until the claim ends | [S5] [S7] [S10] [S11]; convention **[std]** (16) |
| Grace period | 60 days, then cancellation; unpaid premiums deducted from any claim | [S1] [S3]; pick **[std]** (17) |
| Reviewable / age-costed premiums | Out of scope (variation) | [S1] [S4] [S6] [S7] [S10] [S11] |

14. Premium rates are not public: all sampled products are individually quoted and no
    insurer publishes IP rate tables (research file gap). £35/month for the base cell
    is a pure modeling placeholder consistent with the published minimum premium
    structure (£5/month minimum incl. a £3/month admin charge at LV= [S4]; £5/month
    or £60/yr at Royal London [S6]).
15. Observed escalation designs: RPI capped 10%, premium ×1.5, in-claim increases
    continue (Aviva [S1] [S2]); RPI, premium ×1.5, in-claim increases capped 12%
    (LV= [S3]); fixed 2–5% or RPI min 2% max 10%, premium ×1.2 (Royal London
    [S5] [S6]); CPIH capped 10%, premium ×1.5 capped 15% (The Exeter [S7]); RPI capped
    10% with a stepped RPI-plus premium loading (Vitality [S10]); CPI capped 10%
    (Cirencester [S11] [S12]). The composite adopts the Aviva design: RPI index, 10%
    benefit cap, 1.5× premium multiplier, escalation continuing in claim.
16. Observed waiver mechanics: premiums waived while benefit is paid, with premiums
    payable only during the deferred period (The Exeter [S7]; Cirencester [S11];
    similarly Royal London and Vitality [S5] [S10]); waived from the earlier of
    deferred-period end and 13 weeks of incapacity (Aviva [S1]); LV= is the outlier —
    premiums remain payable in claim unless a separate Waiver of Premium policy is
    bought [S3] [S4]. The composite standardizes on the majority pattern: premiums
    payable through the deferred period, waived from benefit-payment start.
17. Observed grace/lapse: 60 days (Aviva, unpaid premium deducted from claims [S1];
    LV=, reinstatement within 6 months [S3]); 5 weeks (Royal London [S5]); 2 months
    (The Exeter [S7]); 4 months (Cirencester [S11]). 60 days is modal.

---

## Contractual mechanics

### Maximum benefit and the amount payable at claim

Let `E` be pre-incapacity gross annual earnings (defined above), `B` the escalated
monthly benefit at the claim date, `OFF` the monthly total of offset income, and
`G = £1,500` the minimum benefit guarantee. The assessed maximum is:

    MB_annual = 0.65 x min(E, 60000) + 0.50 x max(E - 60000, 0)
    MB = min(MB_annual / 12, 20000)                    (£/month)

with band structure per [S1] [S2] [S5] [S7] and [std] picks per footnotes 6–7. The
amount payable per month of full incapacity, following the Aviva guarantee mechanics
[S1] [S2] with the [std] composite parameters:

    AP = B                                  if B <= G (paid in full)
    AP = B                                  if MB - OFF >= 0.9 x B (90% tolerance)
    AP = min(B, max(G, MB - OFF))           otherwise

The guarantee requires the insured to have been working ≥16 h/week at incapacity
[S1] [S2]. Because underwriting sets `B` against the same formula at outset, the
guarantee and tolerance bite only where earnings have fallen since outset. Premiums
are not refunded when `AP < B` [unverified — not located in the research extracts].

### Deferred period

Benefit becomes payable after `d` weeks (base cell: 26) of continuous incapacity
under the own-occupation definition; payments are monthly in arrears from the end of
the deferred period, with partial months pro-rated daily [S1] [S3] [S10]. Premiums
remain payable during the deferred period and are waived from benefit-payment start
(**[std]** convention, footnote 16). Payments stop on the earliest of: ceasing to
meet the incapacity definition (recovery), no further loss of earnings, death, and
the policy end date [S1] [S3] [S5] [S7] [S10].

### Escalation

With escalation elected (base cell), at each policy anniversary `y`:

    j(y) = min(max(RPI_y, 0), 0.10)         (no change if RPI <= 0 [S1])
    B(y+1) = B(y) x (1 + j(y))
    P(y+1) = P(y) x (1 + 1.5 x j(y))        (premium multiplier [S1][S2]; pick [std])

Escalation of `B` continues during claim [S1] [S2]. Without the option, `B` and `P`
are level for the term [S1] [S5].

### Proportionate and rehabilitation benefit

On a partial return to work — reduced hours in the own occupation (rehabilitation) or
a different, lower-paid occupation (proportionate) — a reduced benefit is paid on the
formula, stated per The Exeter's lettered form [S7] and structurally common to all
six sampled products [S1] [S3] [S5] [S10] [S11]:

    reduced benefit = (A - B) / A x C

where, exactly as the research records for [S7]: `A` = pre-incapacity earnings (as
financially assessed), `B` = earnings in the new or reduced occupation, and `C` = the
benefit that would otherwise be in payment. Worked example from the source: a 50%
earnings loss against a £1,000/month assessed benefit pays £500/month [S7]. (The `B`
in this contractual formula is earnings, not the sum assured; the technical notes use
distinct symbols.)

### Linked claims

If the insured, having returned to work, suffers a recurrence of the same cause
within 52 weeks of payments stopping (**[std]** pick, footnote 13), benefit payments
restart without a new deferred period [S1] [S3] [S5] [S7] [S10] [S11]. Returning to work
against medical advice voids the linkage at some insurers [S5] [S7].

### Premiums, grace, lapse

Premiums are guaranteed: apart from escalation-option increases, they change only for
reasons such as tax or legislation ([S3]; level "won't change" [S5]; [S1] [S7]). If a
premium is unpaid, cover continues for a 60-day grace period; at its end the policy
is cancelled without value, and premiums due are deducted from any claim then in
payment [S1] [S3] (**[std]** pick, footnote 17). There is no surrender value at any
time [S4] [S5] [S7], so lapse generates no cash flow.

### Alterations and increase options (not modeled)

Sampled products allow benefit/term/deferred-period alterations (decreases without
underwriting; increases with) [S1] [S3] [S5] [S7] and guaranteed insurability increases
on life events (marriage, mortgage, childbirth, salary rise) without medical
underwriting, capped per event and in lifetime total — e.g. 50%-of-cover/£9,000-yr
per event (Aviva [S1]), £10,000/yr per event with a £35,000/yr lifetime total (LV=
[S3]), £12,000/yr per event / £24,000/yr lifetime (Royal London [S5]), 50% or
£833.33/month (The Exeter [S7]), 10% per event (Cirencester [S11]). These are
documented for completeness; the reference model holds cover changes at zero.

---

## Riders and options

**In scope (modeled):**

- **Escalation (increasing cover) option** — RPI-linked, as specified above
  [S1] [S2]; on in the base cell.
- **Waiver of premium** — standard feature, premiums waived while benefit is paid
  [S5] [S7] [S10] [S11]; modeled as zero premium income from claims in payment.
- **Proportionate/rehabilitation benefit** — built into all sampled contracts
  [S1] [S3] [S5] [S7] [S10] [S11]; carried structurally as a claim-severity factor in the
  model (technical notes), default off.

**Out of scope (listed for completeness; no charges or benefits projected):**
fracture cover (£650–£6,000 per schedule) [S1] [S3] [S5]; hospitalisation benefit
(£100/night after 6 nights, max 90) [S1] [S5] [S10]; trauma lump sum (6× monthly
benefit capped £40,000) [S1]; death benefits (£5,000–£10,000) [S3] [S5]; children's
illness/hospitalisation benefits [S3] [S5] [S10]; terminal-illness acceleration
[S5] [S11]; rehabilitation support services and Vitality Recovery Benefit [S3] [S10];
Aviva Global Treatment [S1]; guaranteed insurability options (above)
[S1] [S3] [S5] [S7] [S11]; dual deferred periods [S1] [S10]; Day One accident cover
[S11]; NHS/teacher sick-pay-linked deferred periods [S1] [S3] [S5] [S7] [S10]; career
breaks and policy breaks [S5] [S7] [S11]; Vitality Income Boost and Optimiser [S10];
LV= unemployment premium waiver and "Pay my mortgage" facility [S3] [S4]; Cirencester
capital-sum (surplus participation) option [S11] [S12].

---

## Variations across insurers

1. **Incapacity definition.** Own occupation is universal as the primary definition —
   none of the six sampled products uses suited or any-occupation as the primary
   basis for standard risks [S1] [S3] [S5] [S7] [S10] [S12]. Variation is in the fallback
   for those not in (full) work: LV= homemaker (meal/housework test) [S3]; Royal
   London three-tier (Serious Illness list, then 3-of-9 Everyday Tasks) [S5];
   Vitality houseperson on 3-of-6 ADLs, capped £1,500/month [S10]; The Exeter
   going-outdoors/household-duties tests [S7]; Aviva a separate 12-month restricted
   benefit [S1]; Cirencester houseperson definition capped £2,730/yr [S11].
   Cirencester alone sells an Own/Own Suited hybrid and tapers own-occupation benefit
   to 75% after 52 weeks and 50% after 104 weeks of claim [S11]. Representative
   choice: pure own occupation, no fallback tier — the standard-risk working insured
   is the model cell.
2. **Benefit formula.** Two-band percentages of earnings around £60,000 — 65%/45%
   (Aviva [S1]; Exeter [S7]), 65%/50% (Royal London [S5]), 60%/50% (Vitality [S10])
   — vs flat 60% (LV= [S3]; Cirencester [S11]). Caps £120,000/yr to £250,000/yr
   [S5] [S7]. Representative: 65%/50% at £60,000, cap £240,000/yr (footnotes 6–7).
3. **Deferred periods.** 4/8/13/26/52 weeks is the common core [S6]; Day 1 / 1-week
   short deferreds are the friendly-society and specialist niche [S7] [S11] [S10];
   Aviva adds 104 weeks and Vitality 24/60 months at the long end [S1] [S10]; dual
   deferreds [S1] [S10] and public-sector sick-pay-linked deferreds (all except
   Cirencester) are established features. Representative: the common core, base 26.
4. **Payment terms.** Full term vs limited: 24 months is the standard budget variant
   (Aviva limited payment term [S1] [S2]; LV= Budget 12/24 [S4]); Royal London 1/2/5
   years [S6]; The Exeter 2/5 years [S7]; Vitality 12/24/60 months [S10]. All pair
   the limit with a 6-month back-at-work requirement before a same-cause re-claim
   (26 weeks at Royal London) [S1] [S4] [S5] [S7] [S10]. Representative: full term; the
   24-month variant is the documented budget alternative.
5. **Premium bases.** Guaranteed level premiums dominate [S1] [S3] [S5] [S7];
   reviewable premiums follow a common pattern — no change for 5 years, then
   reviews with no cap on changes [S1] [S4] [S6] [S10]; age-costed guaranteed scales
   are the friendly-society hallmark (The Exeter [S7]; Cirencester [S11]). Vitality
   uniquely links premiums to measured health engagement (Optimiser: +2.5%/+1.5%/
   +0.5%/0% p.a. by Vitality Status) [S10]. Representative: guaranteed level.
6. **Minimum benefit guarantees.** £1,500/month is the market convention
   [S1] [S3] [S10] [S11]; Royal London £1,750 [S5]; doctors/surgeons get doubled floors
   [S3] [S5] [S10]. Representative: £1,500 (footnote 8).
7. **Escalation.** RPI is the modal index (Aviva, LV=, Vitality [S1] [S3] [S10]);
   The Exeter uses CPIH [S7] and Cirencester CPI [S11]; all cap benefit increases
   at 10%/yr; premium multipliers 1.2× (Royal London [S5]) to 1.5× (Aviva, LV=,
   Exeter [S1] [S3] [S7]). Representative: RPI, 10% cap, 1.5×.
8. **Structural outliers.** (a) The Holloway contract: benefit in units (£10.50/week
   per unit, 5–75 units), age-costed guaranteed premiums, optional capital sum
   accumulating discretionary Surplus/Bonus Allocations on With-Profits Actuary
   advice, fortnightly benefit payment, standard exclusion list [S11] [S12] — the
   only sampled product with an exclusion list and the only one with a
   savings-like element. (b) Vitality's status-linked premiums and Income Boost
   [S10]. Neither is the representative chassis; both matter for model-generality
   arguments (a Holloway model needs a capital-account state; a Vitality model needs
   premium paths contingent on engagement status).
9. **Expiry-age linkage.** Only Cirencester links expiry to state retirement age
   ("or state retirement age, whichever is higher") [S11]; none of the other five
   products' documents link expiry to State Pension age — expiry is a selected age
   in a 50–70/71 band [S2] [S4] [S6] [S7]. The composite therefore uses a fixed
   selected expiry age.

---

## Regulatory context

**Prudential (PRA / Solvency UK).** IP liabilities are valued under the PRA Rulebook
Technical Provisions Part: technical provisions = best estimate + risk margin, where
the best estimate is the probability-weighted average of future cash flows discounted
at the relevant risk-free interest rate term structure [R7] [REG-R1]. The risk-margin
cost-of-capital rate is 4% with a life risk-tapering factor λ = 0.9 [REG-R4]. Under
the Matching Adjustment Part, the in-payment element of an income protection policy
is an "eligible element" that can enter an MA portfolio where organised and managed
separately, even though the whole contract does not qualify [R8] [REG-R2]. Contract
design itself is constrained by RAO Class IV: at least five years or to normal
retirement age, non-cancellable by the insurer [R6] [REG-R14].

**Conduct (FCA).** IP is a pure protection contract conducted under ICOBS rather
than COBS, even though it is long-term (Class IV) business prudentially [R9,
fetched_ok=false in the product research pass; verified via [REG-R11]]. The Consumer
Duty applies to this retail business; its price-and-value outcome drives the
product-level value assessments that cash flow models increasingly support
[REG-R12]. Consumer disclosure duties at underwriting are governed by CIDRA 2012
(duty to take reasonable care not to misrepresent; graduated remedies), which
underpins claim declinature/avoidance assumptions [REG-R20].

**Tax.** Benefits from individual IP funded from taxed personal income are free of
income tax to the policyholder under current law [S4] [S7] [S11]; benefit payments can
however reduce means-tested Universal Credit [S3] [S4] [S5]. At company level,
post-2012 protection business is non-BLAGAB long-term business taxed on trade
profits (not I-E) under Finance Act 2012 Part 2, so a UK IP model carries a
trade-basis tax flag rather than a policyholder tax engine [REG-R17].

**Actuarial standards.** UK technical actuarial work on IP pricing, reserving and
experience analysis is subject to FRC TAS 100 (general) and TAS 200 (insurance)
[R10] (fetched_ok=false in the product research pass; verified via
[REG-R33] [REG-R34]).
