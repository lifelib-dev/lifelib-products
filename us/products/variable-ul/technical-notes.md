# Variable Universal Life Insurance — Liability Cash Flow Model: Technical Notes (United States)

**Status:** Draft, 2026-08-03; cross-product [REG-R#] citations extended 2026-08-06
with the AP&P Manual appendix items read at first hand. Product sources [S#]/[R#] were
accessed 2026-08-03; the [REG-R#] entries carry their own access dates per entry in
`sources.md`. Companion to `product-spec.md` in this
directory; both use identical parameter values. This is a standardized composite for
reference modeling, not any single insurer's product. [S#]/[R#] cite
`us/_research/variable-ul.md`; [REG-R#] cites the cross-product reference library
`us/references/regulatory-and-actuarial-references.md` (research provenance:
`us/_research/regulatory-actuarial.md`, same R-numbering); **[std]** marks standardizations introduced
for the reference implementation. Facts flagged [unverified] in the research notes
stay flagged here.

## Model scope and conventions

- **Scope.** Single-policy seriatim projection of gross liability cash flows for the
  representative VUL contract of `product-spec.md`, baseline without riders or
  no-lapse guarantee **[std]**. Reserve calculations are out of scope (see
  "Valuation and reserve pointers").
- **Base chassis.** The monthiversary processing order (premium → withdrawal/loan →
  DB and NAAR → monthly deduction → growth → EOM decrements, deaths before lapses)
  follows the universal-life reference notes
  (`us/products/universal-life/technical-notes.md`). One sourced deviation from that
  base chassis: the VUL prospectuses define the NAAR as death benefit − account
  value with no one-month discount [S2], so this model omits the one-month
  guaranteed-rate discount used in the fixed-UL base recursion.
- **Projection frequency.** Monthly, on policy monthiversaries; contractual daily
  accruals (M&E, fund expenses, fixed-option interest [S1]) are approximated by
  monthly factors **[std]**.
- **Timing.** Beginning-of-month (BOM) monthiversary processing: premium receipt,
  withdrawals, loan activity, and the monthly deduction occur at the monthiversary;
  investment growth accrues over the month; decrements (death, lapse/surrender) and
  claim/surrender payments occur at end of month (EOM), deaths before lapses
  **[std]**.
- **Age basis.** Age nearest birthday (ANB) **[std]**, consistent with the 2017 CSO
  ultimate ANB tables cited for guaranteed COI maxima [S2][S4]. Attained age
  advances on policy anniversaries.
- **Model points.** One policy per model point; decrements applied as probabilities
  (in-force measure l_t), not stochastic lives **[std]**. Cash flows are
  probability-weighted per unit policy in force at issue (or at the projection start
  for in-force points).
- **Compliance mechanics.** The corridor is enforced in the DB formula [S2][R3].
  Guideline premium limits and 7-pay/MEC testing [R3][R4] are not enforced in the
  baseline; premiums are assumed within limits **[std]**.

## Model point attributes

| Attribute | Type | Example |
|---|---|---|
| policy_id | str | "VUL-000001" |
| issue_age (ANB) | int | 45 |
| sex | enum {M, F} | M |
| risk_class | enum | standard nonsmoker |
| face_amount F_0 | currency | 500,000 |
| db_option | enum {A, B} | A |
| s7702_test | enum {GPT, CVAT} | GPT (baseline **[std]**) |
| planned_premium (annualized) | currency | 6,000 |
| premium_mode | enum | monthly |
| premium_allocation α = (α_1, α_2, α_F) | vector, Σ = 1 | (0.60, 0.40, 0.00) |
| duration_inforce (months, for in-force points) | int | 24 |
| initial_subaccount_values | vector | (30,000, 20,000) |
| initial_fixed_value | currency | 0 |
| initial_loan_balance | currency | 0 |
| nlg_rider | bool | false (baseline **[std]**) |

The two-subaccount lineup (1 = equity, fund expense e_1 = 0.75% p.a.; 2 = bond,
e_2 = 0.55% p.a.) is a **[std]** collapse of observed menus; observed fund-expense
ranges 0.29%–1.18% [S1], 0.55%–2.88% gross [S2], 0.46%–2.54% [S3], 0.08%–1.93% [S4].

## State variables

| Variable | Meaning |
|---|---|
| t | policy month index (t = 0 at issue or projection start) |
| x_t | attained age (ANB), advancing on anniversaries |
| SA_{i,t} | value of subaccount i (separate account) |
| FA_t | fixed-option value (general account) |
| LA_t | loan-account (collateral) value (general account) [S3] |
| D_t | outstanding policy debt (principal + capitalized interest) |
| AV_t | total account value = Σ_i SA_{i,t} + FA_t + LA_t [S1][S2][S3][S4] |
| F_t | face amount (reduced by Option A withdrawals [S1][S2]) |
| DB_t | death benefit per option and corridor |
| NAAR_t | net amount at risk = max(0, DB_t − AV_t) [S2] (floor **[std]**) |
| SC_t | surrender charge (per schedule, **[std]** scale) |
| CSV_t | cash surrender value = AV_t − SC_t − D_t [S1] |
| l_t | probability policy is in force at start of month t |
| status | in force / grace / lapsed / matured (age 121) |

## Assumption inputs

Three classes are distinguished explicitly; a model implementation should keep them
in separate input structures.

### (a) Contractual / guaranteed elements (from the spec; cited)

| Item | Value | Basis |
|---|---|---|
| Premium load ceiling | 6.0% of each premium | [S2] |
| COI guaranteed maxima | 2017 CSO sex-distinct S/NS ultimate ANB, monthly per $1,000 NAAR; cap $83.34 (observed $83.33–$83.34) | [S2][S4][R12]; cap [S1][S2][S3][S4] |
| Per-policy charge | $10.00/month | [S2][S4] |
| Per-$1,000 face charge | $0.20 per $1,000 of F_0 per month (current = guaranteed **[std]**) | [S2] |
| M&E guaranteed max | 0.60% p.a. | **[std]** (spec footnote 8) |
| Fixed-option floor | 1.0% effective annual | [S1] |
| Loan charged/credited rates | 2.0%/1.0% years 1–9; 1.05%/1.0% from year 10 | [S1] |
| Surrender charge | $18.00 per $1,000 initial, linear to 0 over 14 years | **[std]** (spec footnote 10) |
| Corridor factors κ | 250% (≤40), 215% (45), 185% (50), 150% (55), 130% (60), to 100% at 90–95; linear interpolation | [S2][R3]; interpolation **[std]** |
| Grace / default | default when AV − SC − D ≤ 0; 61-day grace | [S1][R8] |
| Age-121 rule | no premiums or monthly deductions after attained age 121; asset charges continue | [S1][S2][S4] |

### (b) Current non-guaranteed scales (insurer-declared; snapshot)

Governed as NGEs under ASOP No. 2 (by class; no recouping of past losses) [R11].

| Item | Value | Basis |
|---|---|---|
| Premium load — current | 4.0% flat | **[std]** (spec footnote 3) |
| COI — current scale | input vector c_t; default placeholder 50% of guaranteed 2017 CSO; disclosed anchor male 45 std NS year 1: current $0.04 (gtd $0.22) | **[std]** (spec footnote 5); anchor [S4] |
| M&E — current | 0.45% p.a. | [S1] |
| Declared fixed rate | 1.0% (= floor; declared rates not public) | **[std]** (spec footnote 13) |
| Credits (persistency credit, expense reductions) | none in baseline | **[std]**; variations [S1][S2] |

### (c) Behavioral / experience assumptions

| Item | Recommended public basis | Basis |
|---|---|---|
| Best-estimate mortality | 2015 VBT (sex/smoker-distinct, RR tables for preferred fit), calibrated with ILEC 2012–2019 A/E experience | [REG-R18][REG-R19] |
| Base lapse/surrender | LIMRA/SOA U.S. Individual Life Persistency (2009–2013, includes VUL plans); 2015–2021 UL lapse/surrender study for modern levels (VUL not broken out separately — applied to VUL by analogy, flagged) | [REG-R20][REG-R21] |
| Premium persistency | 2015–2021 UL premium persistency study (flexible-premium payment behavior); VUL by analogy | [REG-R21] |
| Dynamic behavior | fund-performance-sensitive multipliers, see "Policyholder behavior modeling" | **[std]** |
| Insurer expenses | $75/policy/year maintenance + 2% of premium collection expense (placeholders; internal expense assumptions are not public) | **[std]** |
| Decrement mortality vs COI | Note: the COI charge uses the *current COI scale* (class (b), revenue); the death decrement uses *best-estimate mortality* (this class). They must never be conflated. | **[std]** convention |

VUL-specific policyholder-behavior studies were not retrieved; premium persistency
and dynamic lapse for VUL remain unsourced [unverified] — hence the **[std]**
placeholders below.

## Cash flow components and recursions

### Notation (defined once; used in both documents)

- t: policy month; x_t: attained age; l_t: in-force probability at BOM.
- P_t: premium paid at monthiversary t; γ: premium load rate (current 0.04).
- α_i: allocation share to account i (subaccounts i = 1,2; F = fixed).
- SA_{i,t}, FA_t, LA_t, D_t, AV_t, F_t, DB_t, NAAR_t, SC_t, CSV_t: state above.
- r_{i,t}: gross fund return of subaccount i in month t (scenario input).
- e_i: fund expense ratio (annual); m: M&E rate (annual; current 0.45% = 0.0045);
  i_fix: declared fixed rate; i_L, i_C: loan charged/credited rates.
- c_t: current monthly COI rate per $1,000 NAAR; e_pol = 10; e_face = 0.20.
- κ_t: corridor factor at x_t.
- q^d_t: best-estimate monthly mortality; q^w_t: monthly lapse; ρ_t: premium
  persistency factor.
- Monthly conversions: q^d_t = 1 − (1 − q^d,annual)^{1/12}; likewise lapse
  **[std]**.

### Monthly processing order (monthiversary t → t+1)

1. Advance to monthiversary t; on an anniversary, advance x_t and the policy-year
   dependent parameters (loan tier, SC_t, corridor κ_t). If x_t ≥ 121: skip steps
   2–4 and 6 (no premiums, no monthly deduction) [S1][S2][S4].
2. **Premium.** P_t = ρ_t × planned modal premium. Load: γ·P_t to insurer. Net
   premium allocation: SA_{i,t} += α_i·(1−γ)·P_t; FA_t += α_F·(1−γ)·P_t.
3. **Withdrawal** (if modeled): reduce accounts by withdrawal + $25 fee; Option A
   reduces F_t proportionately [S1][S2]. Baseline: none **[std]**.
4. **Loan activity** (if modeled): new loans/repayments move value between
   investment options and LA_t [S3]; D_t accrues at i_L, LA_t at i_C, monthly
   compounding (1+i)^{1/12} **[std]** (contractually interest is due/capitalized
   annually [S1]).
5. **Death benefit and NAAR** (post-premium values):
   - Option A: DB_t = max(F_t, κ_t·AV_t)
   - Option B: DB_t = max(F_t + AV_t, κ_t·AV_t)
   - NAAR_t = max(0, DB_t − AV_t)
6. **Monthly deduction.**
   - COI_t = c_t · NAAR_t / 1000, with c_t ≤ min(2017 CSO max, 83.34)
     [S2][S4][R12]
   - MD_t = COI_t + e_pol + e_face·F_0/1000
   - Allocated pro rata across unloaned accounts **[std]**: each unloaned account j
     pays MD_t · V_j / Σ_unloaned V (loan account LA is excluded).
7. **Investment growth** over the month:
   - Subaccounts (unit-value dynamics): SA_{i,t+1} = SA'_{i,t} · (1 + r_{i,t}) ·
     (1 − e_i/12) · (1 − m/12), where SA' is the post-deduction value. In the
     contract, fund expenses and (for S1) M&E accrue daily in the unit value
     [S1]; the monthly product form is a **[std]** approximation. Insurers deducting
     M&E monthly [S2][S3][S4] are captured by the same factor.
   - Fixed option: FA_{t+1} = FA'_t · (1 + i_fix)^{1/12}, i_fix ≥ 1.0% [S1].
   - Loan account: LA_{t+1} = LA_t · (1 + i_C)^{1/12}; debt D_{t+1} = D_t ·
     (1 + i_L)^{1/12} **[std]** monthly accrual.
8. **EOM decrements and payments** (deaths before lapses **[std]**; balances here
   are EOM values after step 7, so outstanding debt is D_{t+1}):
   - Death: probability l_t·q^d_t; claim outflow = DB_t^{EOM} − D_{t+1} (debt
     repaid internally) [S1][S3], where DB_t^{EOM} recomputes the option/corridor
     formula on EOM account values **[std]**.
   - Surrender/lapse: probability l_t·(1 − q^d_t)·q^w_t; outflow = CSV_t^{EOM} =
     AV_{t+1} − SC_t − D_{t+1} [S1].
   - Maintenance expense outflow: l_t · (75/12) **[std]**; premium expense 2%·P_t
     at step 2 **[std]**.
   - Survivorship: l_{t+1} = l_t · (1 − q^d_t) · (1 − q^w_t).
9. **Status checks.** If CSV_t ≤ 0 (and no NLG): default → grace; the baseline
   model lapses the policy at the next monthiversary if not cured, collapsing the
   61-day grace and notice mechanics [S1][R8] into a one-month lag **[std]**. At
   x_t = 121, switch to the age-121 regime [S1][S2][S4].

### Scenario requirement

Subaccount gross returns r_{i,t} are exogenous scenario inputs. The reference model
runs either (a) deterministic scenarios (level or path-specified gross returns —
e.g., illustration-style level returns net of specified charges), or (b) stochastic
sets of gross-return paths. For statutory use, VM-20 defines a Deterministic
Reserve (Section 4) and a Stochastic Reserve (Section 5), with economic scenarios
addressed in its Appendix 1 [R7]; GAAP
long-duration (LDTI) measurement consumes the same projected cash flows with
different assumption-update and discounting overlays [REG-R34 — source not fetched;
summary-based, flagged]. Declared fixed-option rates would in practice vary with
general-account yields; the baseline holds i_fix at the 1.0% floor **[std]**.

### Separate-account vs general-account cash flow split

Account location: SA_{i,t} are separate-account assets; FA_t and LA_t are
general-account liabilities/assets [S1][S3]. The model reports two views:

- **Gross (policyholder) view — the reference model's primary projection [std].**
  - Inflow: premiums l_t·P_t (full premium; the net premium is a pass-through into
    the accounts, the load is insurer revenue).
  - Outflows: death claims l_t·q^d_t·(DB_t^{EOM} − D_{t+1}); surrenders
    l_t(1−q^d_t)q^w_t·CSV_t^{EOM}; withdrawals; insurer expenses.
- **Net-of-account (general-account strain) view — derived report.**
  - Insurer margins collected: premium loads γP_t, monthly deductions MD_t, M&E
    collected via unit values, loan spread (i_L − i_C on D_t), surrender charges
    SC_t on surrender.
  - Net mortality cost: l_t·q^d_t·NAAR_t^{EOM} — the general-account cost of a
    death after seizing the account.
  - Account transfers (memo): on death, Σ_i SA_{i,t} moves separate account → general
    account; FA/LA release internally; on surrender the separate account liquidates
    to fund CSV.

Projected output columns (per month t, per scenario; probability-weighted by l_t)
**[std]** naming:

| Column | Definition | View |
|---|---|---|
| prem_gross | l_t · P_t | gross inflow |
| load_income | l_t · γ · P_t | net (margin) |
| md_income | l_t · MD_t (COI + per-policy + per-$1,000) | net (margin) |
| me_income | l_t · M&E collected via unit values | net (margin) |
| loan_spread | l_t · (i_L − i_C) accrual on D_t | net (margin) |
| claim_gross | l_t · q^d_t · (DB_t^{EOM} − D_{t+1}) | gross outflow |
| claim_net | l_t · q^d_t · NAAR_t^{EOM} | net (GA strain) |
| surr_outgo | l_t (1−q^d_t) q^w_t · CSV_t^{EOM} | gross outflow |
| sc_income | l_t (1−q^d_t) q^w_t · SC_t | net (margin) |
| expense | l_t · (maintenance + premium expense) | both |
| sa_transfer | account transfers separate ↔ general (memo) | memo |
| av_eop, naar, l_t | state snapshots for reconciliation | memo |

Reconciliation identity (per month): net GA cash flow = load_income + md_income +
me_income + loan_spread + sc_income − claim_net − expense; the gross view must
reproduce it after adding back the account pass-throughs (net premiums in,
account releases out) **[std]**.

**Warning — a common specification error:** "death benefit paid = DB − AV from the
separate account" is NOT the insurer's claim cash flow. The insurer's liability
outflow is the **full death benefit** (less policy debt); seizing the account value
is the *funding* of part of that outflow, and DB − AV (= NAAR) is the net
general-account strain. Projecting only DB − AV as the claim understates gross
benefit outgo and breaks reconciliation with statutory exhibits; projecting full DB
*and* separately expensing NAAR double counts. The reference model projects the
gross view and derives the net view arithmetically from the same run **[std]**.

## Policyholder behavior modeling

All dynamic formulas are **[std]**: no public VUL-specific dynamic-behavior study
was retrieved [unverified gap], so forms are standardized with rationale, calibrated
to the base tables in assumption class (c).

- **Funding ratio.** φ_t = AV_t / AV*_t, where AV*_t is the account value projected
  at issue under the pricing path (level 6% gross subaccount return, current
  charges, planned premiums) **[std]**. φ_t < 1 means performance/funding shortfall.
- **Dynamic lapse.** q^w_t = q^w,base_t · λ_t, λ_t = min(2.0, max(0.5,
  1 + β·(1 − φ_t))), β = 0.5 **[std]**. Rationale: in a protection-oriented VUL a
  performance shortfall raises the premium required to sustain coverage, pushing
  marginal policyholders to lapse (and underfunded policies drift toward the
  default test of step 9); overfunded policies are stickier. Bounds prevent extreme
  extrapolation.
- **Premium persistency.** ρ_t = ρ^base_t · min(1.3, max(0.7, φ_t^{−δ})), δ = 0.25
  **[std]**; ρ^base_t from the UL premium persistency study levels [REG-R21]
  (placeholder grading: 1.00 year 1 → 0.85 year 5 → 0.80 thereafter **[std]**).
  Rationale: shortfalls induce catch-up funding by retained policyholders
  (φ < 1 ⇒ ρ up); strong performance induces premium holidays (φ > 1 ⇒ ρ down) —
  the signature flexible-premium behavior the UL studies measure [REG-R21].
- **Surrender at surrender-charge cliff.** Optional spike multiplier on q^w in the
  month after SC_t reaches zero (end of year 14) **[std]**; magnitude an input.
- **No dynamic mortality.** Anti-selective lapse interaction (lapse-supported
  effects) is not modeled in the baseline **[std]**.

## Worked example — one month, two subaccounts

Model point: male 45 standard nonsmoker, F_0 = 500,000, Option A, GPT; policy year 3
(SC factor 12/14); planned premium $500/month paid; allocation 60/40; no fixed
balance, no debt; current scales as above (γ = 4%; c = $0.04 per $1,000 [S4] —
illustrative current rate at the disclosed representative point; e_1 = 0.75%,
e_2 = 0.55%, m = 0.45% [S1]); scenario month: r_1 = +1.00%, r_2 = −0.50% gross.
Premium level is illustrative only **[std]**. Corridor κ(45) = 215% [S2].

| Step | Item | SA_1 (equity) | SA_2 (bond) | Total AV |
|---|---|---|---|---|
| 0 | BOM balances | 30,000.00 | 20,000.00 | 50,000.00 |
| 2 | Premium 500.00; load 4% = 20.00; net 480.00 split 60/40 | +288.00 | +192.00 | 50,480.00 |
| 5 | DB = max(500,000; 2.15 × 50,480 = 108,532.00) = 500,000.00; NAAR = 449,520.00 | — | — | — |
| 6 | COI = 0.04 × 449.520 = 17.98; expense = 10.00 + 0.20 × 500 = 110.00; MD = 127.98, pro rata 60/40 | −76.79 | −51.19 | 50,352.02 |
| 7 | Growth factor: (1+r)(1−e/12)(1−m/12) → SA_1: 1.0100 × 0.999375 × 0.999625 = 1.008990; SA_2: 0.9950 × 0.999542 × 0.999625 = 0.994171 | ×1.008990 → 30,482.82 | ×0.994171 → 20,023.41 | 50,506.23 |
| — | Memo: M&E collected via unit values ≈ 11.44 + 7.51 = 18.95; insurer margin this month = 20.00 + 127.98 + 18.95 = 166.93 | — | — | — |
| — | Memo: SC = 18.00 × (12/14) × 500 = 7,714.29; CSV = 50,506.23 − 7,714.29 = 42,791.94 | — | — | — |
| — | Memo: EOM DB = 500,000.00; EOM NAAR = 449,493.77 (net GA strain if death this month; gross claim outflow = 500,000.00) | — | — | — |

EOM decrements (step 8) then weight the claim, surrender, and survivorship flows by
l_t·q^d_t and l_t(1−q^d_t)q^w_t; they are omitted from the table, which tracks the
account recursion per policy in force.

## Statutory accounting and capital

Framework and arithmetic live in `us/regulatory/`: concepts, formulas and factor
tables in `statutory-accounting-and-capital.md`, bibliography in `sources.md`. Only
what is specific to VUL is stated here; the shared [REG-R#] numbering now runs
R1–R157 (R114–R124 and R143–R149 unused by design).

### Contract classification and reporting

SSAP No. 50 ¶9 lists **variable life** among life contracts, and the death benefit
itself carries the mortality risk [REG-R78 ¶9]; classification "shall be made at the
inception of the contract and shall not change" [REG-R78 ¶5] — a per-contract flag set
at issue, never re-derived. No part of the retail VUL of `product-spec.md` is
deposit-type, so SSAP No. 52 and Exhibit 7 do not apply [REG-R80]. Flexible premiums
are therefore **premium income, not a direct credit to reserve**: recognised gross when
received in the general account Summary of Operations [REG-R79 ¶¶2–5] and
*simultaneously* booked as a **transfer** to the separate account statement
[REG-R83 ¶5]; the load γ (current 4.0% **[std]**, guaranteed ≤ 6.0% [S2]) is general
account income, not a deduction from `prem_gross`. Reserves report in **Exhibit 5**,
Liabilities page Line 1, keyed by valuation standard **and year of issue**, VM-20
business on **two lines** — net premium reserve and the excess over it
[REG-R89][REG-R90]; minimum death benefit guarantee reserves in Exhibit 5
**Miscellaneous Reserves**, which names "variable life minimum death benefit
guarantees" [REG-R89]; income and benefits in the **Variable Universal Life** column of
the Analysis of Operations, distinct from Variable Life [REG-R90]; face in force in the
**Exhibit of Life Insurance**, incurred basis, in thousands [REG-R89]; change in
valuation basis in **Exhibit 5A**, direct to surplus at beginning-of-year values
[REG-R79][REG-R89]. Acquisition costs are **expensed as incurred — there is no
statutory DAC** [REG-R75 ¶2], so first-year commission plus the initial reserve strike
surplus against one year of flexible premium while the 14-year surrender charge
(**[std]**, spec footnote 10) is contingent revenue that never becomes an asset. A
flexible-premium contract has no scheduled premium due, so the deferred-premium asset,
the change in loading on it [REG-R79 ¶11] and the VM-20 offset `B` are nil in the
baseline **[std]**. That **[std]** was tested against the AP&P print of the Standard
Valuation Law and **stands**: A-820 gives terminal reserve constructions only and carries
**no mean-reserve, mid-terminal or deferred-premium machinery** at all, so it neither
supports the standardization nor displaces it [REG-R153].

### Reserve basis

- **VM-20 constitutes CRVM** for VUL issued on or after the Valuation Manual operative
  date [REG-R1 §11][REG-R3]: minimum reserve = `Σ NPR` plus the excess of `max(DR,
  SR)` over `Σ NPR` less the due-and-deferred premium asset, per reserving category
  [REG-R3 §2.A]. VUL without secondary guarantees is **All Other** (code 080); with
  them it moves to **ULSG** (code 090) [R7]. In All Other the NPR is "determined
  pursuant to applicable methods in **VM-A and VM-C** for the basic reserve" [REG-R3
  §3.B.6] — the **formulaic CRVM** construction of
  `us/regulatory/statutory-accounting-and-capital.md`, "Formulaic reserves", running
  inside a PBR-era manual [REG-R110]. Both engines are needed before any DR or SR
  arises. **A-820 has since been read at first hand** [REG-R153] and supplies the
  statutory-layer authority that sentence previously took from VM-20's pointer alone:
  ¶¶3–4 split the appendix at the **1 January 2017** operative date — ¶¶5–22 govern
  earlier issues and the principle-based ¶¶23–27 "**shall not apply to any such
  policies and contracts**" — while ¶24.a.i still requires the Valuation Manual to
  specify CRVM for life contracts, ¶24.d.i lets the standard for non-PBR business
  simply "**be consistent with the minimum standard of valuation prior to the
  operative date of the Valuation Manual**", and ¶27 permits a principle-based
  valuation to "**include a prescribed formulaic reserve component**" [REG-R153].
  **A-820 reaches a VUL only through ¶13.a**, which extends CRVM "by a method
  consistent with the principles of paragraphs 11 and 12" to policies "providing for a
  varying amount of insurance or requiring the payment of varying premiums", with ¶21
  as the catch-all for plans whose minimum reserves "cannot be determined by the
  methods described above" [REG-R153]. **Those two paragraphs are the whole of A-820's
  reach here, because A-820 carries no separate account content at all.** Its header
  lists SSAP No. 56 among the relevant SSAPs, but nothing in ¶¶1–28 addresses separate
  accounts, the general/separate split or variable benefits [REG-R153]. That is a
  verified negative, not a gap in this file: everything below about the two balance
  sheets comes from SSAP No. 56 [REG-R83] and VM-20 §2.F [REG-R3], and **the formulaic
  appendix VM-A points at says nothing about this product's defining feature.**
  Whether the **A-585** universal life CRVM adaptation — guaranteed maturity premium,
  guaranteed maturity fund and the funding ratio `r` [REG-R155 ¶8] — reaches a
  *variable* UL is **not answered by the appendix print**: A-585 carries definitions
  and valuation requirements only, prints no applicability threshold of any kind, and
  its ¶7 definition of a universal life insurance policy turns solely on "separately
  identified interest credits … and mortality and expense charges", saying nothing
  about a separate account; the carve-out this product relies on is **Model #585's own
  text** [REG-R5], and Model #585 was not re-read against the appendix print
  [REG-R155]. Recorded as open, not resolved. **A-270** (variable life) was extracted
  in the same pass as A-585 but **no reference id was assigned to it**, so nothing is
  cited from it and the variable-life guaranteed-minimum-death-benefit reserve
  construction stays outside this library; what this product says about reserves for
  variable benefits sitting in the separate account on a basis consistent with the
  Standard Valuation Law continues to rest on **Model #270 itself** [R8][REG-R1].
- **One exclusion-test route is barred for this product.** **Variable life may not use
  the SET Certification Method** [REG-R3 §6.A], so a VUL group must pass the Stochastic
  Exclusion Ratio Test (`(b − a)/c < 6%`) or the Demonstration Test, or compute the SR
  — and the risk they measure is this product's dominant sensitivity, the separate
  account return path. The **DET** stays available (barred only for term, deemed failed
  only for material-secondary-guarantee ULSG [REG-R3 §6.B]), but §6.B.6's guaranteed
  gross premium for a UL-type contract with none specified — the level annual gross
  premium keeping the policy in force for the whole coverage period "on the guarantees"
  [REG-R3] — presumes a guaranteed investment return, and the only contractual
  guarantee here is the fixed-option floor of 1.0% [S1]. **The sources read do not
  resolve how to set it for a variable contract**; recorded, not filled. Either way, a
  company computing no DR or SR still files a VM-31 sub-report and must report
  **readiness** to compute them, and passing by the DR-based SERT or the Demonstration
  Test **re-imposes** VM-G Sections 2 and 3 [REG-R108][REG-R109].
- **The general/separate split is a constraint, not a presentation.** VM-20 §2.F: the
  general account share **may not be less than zero** and must include any liability
  for general-account contractual guarantees; the separate account share is **at least
  Σ CSV and at most Σ AV attributable to the separate account** [REG-R3]. Here
  `CSV_t = AV_t − SC_t − D_t` [S1], so through policy year 14 the lower bound sits
  materially below the subaccount balances, and `LA_t` is **general account** [S3] —
  outside the upper bound entirely.
- **Asset adequacy is part of minimum reserves**: VM-30 covers all in-force business
  and turns any shortfall into an **additional reserve** [REG-R100], which Standard
  Valuation Law §6.B makes a minimum-reserve component [REG-R1] — and the AP&P
  codification of that rule is now sourced rather than assumed. It is **not** in the
  A-820 print, whose ¶16 carries only the aggregate nonforfeiture-basis floor; it sits
  in the separate four-paragraph **A-822**, whose ¶3 requires the additional reserve
  where analysis shows one "should be held in addition to the aggregate reserve held
  and calculated in accordance with methods set forth in Appendix A-820", and whose ¶4
  provides that releasing it "would not be deemed an adoption of a lower standard of
  valuation" [REG-R153]. Read with **A-820 ¶18** — holding additional reserves
  determined by the appointed actuary is not the adoption of a higher standard — that
  pair keeps both the establishment and the release of an asset-adequacy reserve
  **outside** the Exhibit 5A change-in-valuation-basis machinery above, while A-820
  ¶2.c is the underlying requirement that assumptions be consistent with the preceding
  year-end "with any exceptions disclosed in the notes to the financial statements"
  [REG-R153]. **Naming trap:** AP&P Appendix **A-822 is not NAIC Model #822**, the
  Actuarial Opinion and Memorandum Regulation — same number, different instrument, and
  A-822 carries no opinion wording, no scenario requirements and no memorandum contents
  [REG-R153]. VM-30's
  asset-adequacy-tested amounts table carries **separate accounts** rows alongside
  Exhibit 5, and **§3.B.7 forbids cash flow testing that solely projects the
  anticipated long-term average equity return** [REG-R100] — a direct constraint on
  "Scenario requirement" above. Starting assets are capped at the statement value of
  the reserves tested [REG-R29].

### What this product's model must additionally produce

Beyond the shared contract in `us/regulatory/statutory-accounting-and-capital.md`,
"Required model outputs":

| Statutory item | VUL model output |
|---|---|
| Exhibit 5 two-line split and the VM-20 §2.F allocation | NPR (All Other, VM-A/VM-C basic reserve) and excess of max(DR, SR) over Σ NPR by valuation standard and year of issue; apportioned GA/SA per contract, GA share ≥ 0 inclusive of guarantee liabilities, SA share ∈ [Σ CSV_t, Σ_i SA_{i,t}] [REG-R3][REG-R89] |
| Exhibit 5 Miscellaneous Reserves | general-account minimum death benefit guarantee reserve [REG-R83 ¶7][REG-R89] |
| Analysis of Operations, VUL column | every Summary of Operations line for that column, with `sa_transfer` appearing **both** on the transfer line and inside the premium / benefit / withdrawal captions [REG-R89][REG-R90] |
| Analysis of Increase in Reserves | tabular net premium, tabular interest, tabular cost, reserves released — **valuation-basis**, not `l_t`-weighted experience — plus net separate account transfers and the change in DR/SR excess over NPR [REG-R90] |
| Exhibit of Life Insurance | `F_t` roll-forward on an **incurred** basis, in thousands, with policy counts [REG-R89] |
| Separate account statement | SA asset and reserve balances; `load_income`, `md_income`, `me_income`, `sc_income` as **general account** income; SA net gain from operations; SA surplus constrained ≥ 0 [REG-R83] |
| IMR / AVR | disposal-level detail for **general account** assets only (fixed option, loan collateral, guarantee backing); nothing for the fair-value subaccounts except AVR on seed money [REG-R83 ¶¶23–27] |
| RBC exposure bases | NAR on the **annual statement** definition net of reinsurance, not `NAAR_t` [REG-R142]; GA reserve by withdrawal-provision category, unitized SA without guarantees excluded; **separate account liabilities** [REG-R128] |
| Reinsurance, tax | gross and ceded separately, never netted, YRT credit as a one-year term mean reserve on the ceded amount at risk on the original basis [REG-R89][REG-R92 ¶¶36–38]; IRC §807 tax reserve = max(net surrender value, 92.81% × NAIC-method reserve) capped at statutory [REG-R16] |

### Risk-based capital

- **C-2 mortality dominates, and its exposure base is not the model's NAAR.** The
  charge runs on **face amount in force minus life reserves (general account Exhibit 5
  plus Separate Accounts Exhibit 3), net of reinsurance**, taken from the annual
  statement rather than company records [REG-R142]. That is not
  `NAAR_t = max(0, DB_t − AV_t)` [S2]: it deducts the **reserve**, not the account
  value, and starts from statement face in force, not `DB_t`. Produce both and
  reconcile; how an Option B death benefit (`F_t + AV_t`) maps to the Exhibit of Life
  Insurance in-force column is **not addressed by the sources read**.
- **The pricing-flexibility bucket must be earned.** The instructions name **UL
  without secondary guarantees** as a "with pricing flexibility" example and **ULSG**
  in the highest-factor "Permanent without" bucket [REG-R128]. Baseline VUL has the
  former shape, but the test is quantitative — the present value of margin actually
  available from repricing in force over the next **5 policy years** must be at least
  `flexibility factor × NAR` [REG-R128]. That margin is exactly the
  non-guaranteed-element headroom: current COI against the 2017 CSO guaranteed maxima
  [S2][S4][R12], 4.0% load against the 6.0% ceiling [S2], 0.45% M&E against 0.60%
  **[std]** — bounded by ASOP No. 2, which requires scales by class and forbids
  recouping past losses [R11], so headroom is not automatically available margin.
  **The default where no assessment is performed is direct individual permanent →
  Permanent without Pricing Flexibility**, the highest-factor category
  [REG-R128][REG-R133]; the NLG variation lands there anyway. Factors and bands are in
  `us/regulatory/statutory-accounting-and-capital.md`, "Risk-based capital"; a
  **repricing scenario**, not merely a base scenario, is a model requirement.
- **C-3a attaches to the general account leg only, and no C-3 cash flow testing
  applies.** Life insurance reserves fall in the **low** withdrawal-provision category,
  one third lower where the actuarial opinion is unqualified and based on asset
  adequacy testing [REG-R128] — but **unitized separate accounts without guarantees are
  excluded from factor-based C-3 entirely** [REG-R128], so the charge reaches the fixed
  option, the loan account and the guarantee reserves, not the subaccounts. Phase I
  scope is "Certain Annuities" **plus single premium life**, which a flexible-premium
  VUL is not [REG-R128][REG-R135], and Phase II is the AG 43 / VM-21 population; the
  LR049 exemption tests are nonetheless company-level and can pull the block in through
  the aggregate [REG-R128].
- **C-1, and where the separate account *is* charged.** C-1o reads book/adjusted
  carrying value out of the **AVR Default Component** [REG-R128], and a traditional
  variable life separate account carries no AVR except on seed money [REG-R83 ¶¶23–25],
  so fair-value subaccount assets do not enter that base — **an inference from two
  documents, not a statement the RBC instructions make; the instructions read do not
  address unitized separate account assets at all** [unverified]. What is charged is
  the general account: fixed-option and guarantee-backing assets take C-1o by NAIC
  designation with the bond size factor [REG-R128], while policy loans sit outside the
  AVR asset base by SSAP No. 7 ¶2 [REG-R85] and, by the same route, outside C-1o
  [unverified]. **C-4a** is the component that does reach the separate account: the
  2.53% premium factor covers Schedule T life premiums, but **variable business
  premiums are expressly excluded because the 0.06% separate account liability factor
  covers them** [REG-R128] — so C-4a scales with **separate account liabilities**,
  growing with account value rather than premium. Whether the fixed-option share of a
  VUL premium stays in the 2.53% base is **not addressed by the sources read**.
- **Size and mix.** C-2 is largest early on an Option A policy and **shrinks as the
  account value grows** — the corridor mechanics that erode COI revenue erode the
  capital charge, while Option B (DB = F + AV) holds NAR up; C-4a moves the other way;
  C-3a and C-1o track only the general account, so reallocation between the fixed
  option and the subaccounts shifts capital between components. In the covariance C-3a
  joins C-1o inside one squared term, C-2 is a standalone squared term and C-4a sits
  **outside** the radical; Total Adjusted Capital includes the AVR but only the portion
  **not consumed in asset adequacy testing**, so the AAT run must report the AVR it
  used [REG-R128][REG-R29].

### Product-specific interactions and traps

- **Two balance sheets, one income statement — and neither view in "Separate-account vs
  general-account cash flow split" is the statutory one.** SSAP No. 56 ¶¶4–5 keeps
  sales, underwriting, contract administration, premium collection, premium tax, claims
  and benefits as **general account** functions: the full premium is general account
  income *and* a transfer to the separate account; load, monthly deduction and M&E are
  general account income; the full death benefit, surrender, commission and premium tax
  are general account expenses [REG-R83]. The **gross view** is the nearer of the two;
  the net-of-account "general-account strain" view is a management report, not the
  Summary of Operations.
- **The `claim_net` warning above is a statutory rule, and separate account surplus may
  not become negative.** ¶7: any difference between the benefit paid and the separate
  account value is charged or credited to **general account** net gain from operations,
  and a minimum death benefit guarantee reserve on a variable life contract is **held
  in the general account** [REG-R83 ¶7] — `claim_gross` is the benefit, `claim_net`
  (= EOM NAAR) the general account charge, and booking only one breaks the exhibits.
  ¶¶8–9: the general account funds any separate account deficiency and reports
  CRVM-created separate account surplus as an **unsettled transfer** [REG-R83]. Assert
  the non-negativity: a projection that lets the separate account statement run
  negative — a transfer booked ahead of the asset movement, a general-account guarantee
  funded from subaccount assets — is wrong at the accounting layer, not in presentation.
- **Measurement basis is fair value, and the liability basis follows it.** VUL
  subaccounts are fair-value separate account assets; the ¶18.b **book-value** election
  is for contracts that do not pass all investment experience through and names pension
  risk transfer, BOLI and registered index-linked annuities — not retail VUL
  [REG-R83 ¶¶17–18]. Where assets are at fair value the liability uses **current
  market-based rates** [REG-R83 ¶30]. So the separate account needs **no IMR** (required
  only for book-value separate accounts) and **no AVR except on seed money** [REG-R83
  ¶¶23–27].
- **The general account leg is more than the guarantee.** `FA_t` and `LA_t` are general
  account [S1][S3], so a VUL always carries an AVR/IMR-bearing general account block,
  though policy loans themselves are **outside** the AVR asset base [REG-R85 ¶2].
  Negative-IMR admittance under INT 23-01 is an entity-level test with a **300%
  Authorized Control Level RBC gate** and, as currently written, automatic nullification
  on **January 1, 2027** [REG-R87]. Fixed-to-subaccount transfers are **effective
  withdrawals** for the IMR excess-withdrawal exemption, which counts cash transfers to
  separate accounts **other than pass-through transfers of new premium** [REG-R89]: the
  `α_i` allocation of new premium does not count, a later transfer out of the fixed
  option does, capped by the contract at the greater of 25% of the option value or
  $2,000 per contract year [S1].
- **Reinsurance.** VUL cessions are typically YRT on the amount at risk; the credit is a
  **one-year term mean reserve on the ceded amount at risk on the original policy's
  mortality and interest basis** [REG-R92 ¶¶36–38], VM-20 assumes **one half year's cost
  of insurance** on the reinsured net amount at risk [REG-R3 §3.B], and Exhibit 5 needs
  gross and ceded produced separately with **no deduction for modified coinsurance**
  [REG-R89].
- **Limits carried forward, less the appendix items that have since been read.**
  AG XXXVII (variable life GMDB reserves) and
  AG XXIII (separate account investments) are cited through [R7] and their texts were
  **still** not retrieved. Of the three Appendix A items this list used to disclaim,
  **A-820 and A-830 have now been read in full** from the free *As of March 2026* AP&P
  download [REG-R153][REG-R154], and **A-830 turns out never to have been an open item
  for this product**: ¶3.a.iii and ¶3.a.iv exclude variable life and variable universal
  life **outright**, so the appendix does not reach a VUL at all [REG-R154 ¶3.a].
  **A-270 was extracted in the same pass as A-585 but carries no reference id** — read,
  not citable, and nothing here is stated from it. The **AVR factor
  tables and IMR grouped-amortisation factor tables were deliberately not transcribed**
  and no value for either appears in this library [REG-R89]; annual statement page and
  line references come from the **2025** blank and must be re-verified against the 2026
  blank [REG-R89][REG-R90]; the RBC parameters cited here are from the **2024**
  instructions, a sold NAIC publication whose 2025 edition could not be parsed
  [REG-R128].

## Valuation and reserve pointers

Reserve-to-statement mapping, the statutory income and surplus recursion and
capital are in "Statutory accounting and capital" above; this section stays a
pointer list of the reserve layers themselves and the practice guidance behind
them, and does not restate them.

This library projects gross liability cash flows; reserve layers are cited, not
reproduced. Statutory: VM-20 minimum reserve = NPR floor plus excess of max(DR, SR)
over aggregate NPR (less due/deferred premium asset); VUL without secondary
guarantees is in the "All Other" reserving category (product code 080), with
secondary guarantees in the ULSG category (code 090); variable life may not use the
SET certification method [R7]. GMDB reserves per AG XXXVII; separate-account
investment rules per AG XXIII (both texts still unretrieved, cited through [R7]);
**Model 270** requires reserves for variable
benefits held in the separate account on a basis consistent with the Standard
Valuation Law [R7][R8][REG-R1] — its AP&P print, **A-270**, has been read but carries
**no reference id**, so nothing is stated from it. The formulaic appendix items sitting
under the NPR — **A-820** [REG-R153], the **A-585** UL adaptation whose reach to a
variable contract is unresolved [REG-R155], and **A-830**, which excludes VUL by its
own terms [REG-R154] — are treated in "Statutory accounting and capital" above and are
not restated here. Current Valuation Manual edition: Jan. 1, 2026
(VM-01/02/20/31, VM-C/M/G/V) [REG-R3]. Practice guidance: ASOP 52 (VM governs in
conflict) [R9]; AAA VM-20 practice note [R10]; ASOP 7 (cash flow analysis)
[REG-R27]; ASOP 56 (model governance for this implementation itself) [REG-R32]. Tax
reserves: greater of net surrender value and 92.81% of the NAIC-method reserve,
capped at statutory [REG-R16]. GAAP: LDTI (ASU 2018-12) overlays measurement on the
same projected cash flows [REG-R34 — not fetched; summary-based, flagged].

## Key sensitivities and model risks

Dominant assumptions (roughly in order):

1. **Separate-account return scenario** (level and volatility): drives AV, hence
   NAAR, COI revenue, M&E revenue, corridor DB, and the default/lapse dynamics —
   the defining VUL sensitivity. Results are scenario-distributions, not points.
2. **Current COI scale** (the 50%-of-CSO placeholder **[std]**): COI is the largest
   charge; disclosed year-1 current/guaranteed ratios (e.g., 0.04/0.22 [S4]) show
   the placeholder is conservative early and the select-to-ultimate shape matters.
3. **Premium persistency ρ_t**: flexible premiums are the UL-family assumption with
   the widest behavioral range [REG-R21]; funding level feeds back into lapse and
   default.
4. **Lapse and dynamic lapse (λ_t)**: level from dated/analogous studies
   [REG-R20][REG-R21] with the dynamic form unsourced **[std]** [unverified].
5. **Best-estimate mortality** vs 2015 VBT/ILEC [REG-R18][REG-R19]; NAAR-weighted,
   so it interacts with the return scenario.

Known modeling pitfalls:

- Conflating COI-scale mortality (charge) with decrement mortality (experience).
- Projecting DB − AV as the death outflow (see the warning above).
- Forgetting the NAAR floor at zero, or letting corridor factors create
  discontinuous DB jumps at quinquennial ages instead of interpolating **[std]**.
- Applying M&E both in the unit-value factor and as a monthly deduction (double
  counting across insurer conventions — pick one; this model uses the unit-value
  factor **[std]**).
- Pro-rata deduction allocation breaking on zero unloaned balances (guard the
  denominator; deduction shortfall triggers the default test).
- Ignoring the loan account: loaned value earns i_C, not fund returns; debt
  compounds at i_L; DB and CSV are debt-reduced [S1][S3].
- Missing the age-121 regime switch (charges stop; asset drags continue)
  [S1][S2][S4].
- Grace-period collapse **[std]** accelerates lapses by up to two months versus the
  contractual 61-day mechanics [S1][R8] — immaterial for most uses, material for
  short-horizon liquidity studies.
- The NLG variation changes the risk profile qualitatively (lapse floor under poor
  performance → higher NAAR persistence); see
  `us/products/guaranteed-ul/technical-notes.md` for shadow-account mechanics and
  [S4] for the rider's notional-load design.
