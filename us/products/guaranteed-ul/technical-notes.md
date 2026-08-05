# Guaranteed Universal Life (UL with Secondary Guarantees) — Liability Cash Flow Model: Technical Notes (United States)

**Status:** Draft, 2026-08-03 (all cited sources accessed 2026-08-03).

Scope note: these notes standardize a liability cash flow projection model for the
representative GUL product defined in `product-spec.md` (same directory). They use the
same representative parameter values as the specification. Tags: [S#]/[R#] cite
`us/_research/guaranteed-ul.md`; [REG-R#] cites the cross-product reference library
`us/references/regulatory-and-actuarial-references.md` (research provenance:
`us/_research/regulatory-actuarial.md`, same R-numbering); **[std]** marks standardizations introduced
for the reference implementation; [unverified] flags facts the research file could not
verify from a retrieved document.

---

## Model scope and conventions

- **Product**: flexible-premium UL, level death benefit only, single shadow-account
  secondary guarantee (AG 38 8E Policy Design #1 [R1]; VM-01 shadow-account
  definition [R2]). The cumulative-premium-test variation is handled by a documented
  swap (see "Cumulative-premium variation").
- **Base chassis**: the monthiversary processing order and the NAAR discount
  convention (DB discounted one month at the guaranteed rate, floored at zero)
  follow the universal-life reference notes
  (`us/products/universal-life/technical-notes.md`); the shadow account runs the
  same recursion with its own parameter set. Documented deviation **[std]**: these
  notes measure the account value for the NAAR after the expense charges but before
  COI (the UL base measures AV before the entire monthly deduction) — immaterial at
  the modeled charge levels, but kept explicit for reconciliation.
- **Projection frequency**: monthly, on policy monthiversaries, from issue (or
  in-force date) to attained age 121, at which point charges and premiums cease and
  coverage continues [S7]. Maximum projection length: (121 − issue age) × 12 months.
- **Timing** **[std]**: monthiversary (BOM) processing — premium receipt, expense
  charges, COI deduction in that order at the start of the policy month; interest
  credited over the month; decrements (death, lapse/surrender, ROP exercise) at end
  of month (EOM) after interest. Deaths are processed before lapses at EOM.
- **Age basis**: age nearest birthday (ANB) **[std]** — chosen because the sourced
  products underwrite on ANB [S2, S4, S6] and the 2017 CSO / 2015 VBT are published
  in ANB variants [REG-R17, REG-R18]. Attained age advances on policy anniversaries.
- **Model points**: single-policy model points; results are expected (probability-
  weighted) cash flows per policy in force at projection start. No stochastic
  decrement simulation in the base model **[std]**.
- **Rate conversions** **[std]**: annual effective interest i → monthly factor
  (1+i)^(1/12). Contractual COI: monthly rate per $1,000 = annual q per $1,000 / 12
  (simple-twelfth; see "Pitfalls"). Experience decrements: monthly rate
  = 1 − (1 − annual rate)^(1/12).
- **Currency/rounding**: USD; internal calculations unrounded, cash flows reported to
  the cent **[std]**.

## Model point attributes

| Attribute | Type | Example (used throughout these notes) |
|---|---|---|
| `policy_id` | str | "GUL-000001" |
| `issue_age` | int (ANB) | 60 |
| `sex` | enum {M, F} | M |
| `risk_class` | enum (4 NT + 2 T classes [S4]) | NT Standard |
| `face_amount` | float (≥ 100,000 [S4, S6]) | 500,000 |
| `guarantee_age` | int in [90, 121] [S1, S2, S9] | 121 (lifetime) |
| `premium_pattern` | enum {level, single_pay, ten_pay} **[std]** | level |
| `annual_premium` | float — solved no-lapse premium P* for level pattern | 10,800.00 **[std]** (illustrative solve output) |
| `premium_mode` | enum {A, S, Q, M-EFT} [S2] | A |
| `duration_months` | int — elapsed policy months at projection start | 300 |
| `av_init` | float — base account value at projection start | 2,400.00 |
| `sg_init` | float — shadow account value at projection start | 118,000.00 |
| `loan_init` | float | 0.00 |
| `rop_elected` | bool (built-in endorsement [S1]) | True |

Premium pattern is a first-class model point attribute because funding pattern drives
both MEC status [R5] and observed lapse behavior (higher lapses for level-pay, lower
for single-pay [R8]; premium persistency study basis [REG-R21]).

## State variables

| Variable | Meaning | Initial value |
|---|---|---|
| `t` | policy month index (1, 2, …) | `duration_months` + 1 |
| `AV_t` | base account value, EOM, floored at 0 | `av_init` |
| `SG_t` | shadow account value, EOM, NOT floored (negative = catch-up shortfall) | `sg_init` |
| `L_t` | loan balance including accrued interest | `loan_init` |
| `DB_t` | death benefit = max(F, κ(x_t)·AV_t) [S2, S4; R4 corridor] | — |
| `l_t` | in-force probability (survivorship from all decrements) | 1.0 |
| `g_t` | grace-period counter, months (0 = not in grace) [S7] | 0 |
| `D_t` | monthly deduction forgone because AV = 0 under active guarantee | 0 |
| `CumPrem_t` | cumulative premiums paid (drives ROP refund [S1] and MEC testing [R5]) | per model point |
| `SC_t` | surrender charge = 18/1000 · F · max(0, (180 − t)/180) **[std]** | — |
| `C_t` | catch-up premium required to restore guarantee = max(0, −(SG_t − L_t))/(1 − π^g) **[std]** | 0 |

## Assumption inputs

The model distinguishes three assumption classes. Class (a) is contractual and fixed;
class (b) is a snapshot of insurer-declared scales; class (c) is behavioral/experience
and belongs to the assumption-governance layer (see [REG-R25] for governance
patterns; ASOP 2 governs insurer NGE determination itself [REG-R26]).

### (a) Contractual / guaranteed elements (from the specification)

| Element | Value | Basis |
|---|---|---|
| Base premium load π | 25% | [S3], [S7] |
| Base per-policy charge | $5.50/month to age 121 | [S3], [S7] |
| Base per-unit charge | $0.20 per $1,000 initial face /month | **[std]** (spec note) |
| Guaranteed max COI | 2017 CSO sex/smoker-distinct ANB, monthly = annual/12 | **[std]** structure; [R3] (stated maxima required); [REG-R17] |
| Guaranteed credited rate | 2.0% annual effective | [S3], [S5], [S7] |
| Shadow premium load π^g | 8% | **[std]** |
| Shadow credited rate i^g | 5.5% annual effective (guaranteed) | **[std]**; AG 38 8E cap context [R1] |
| Shadow COI | 55% of 2017 CSO maximum | **[std]** |
| Shadow per-unit charge | $0.05 per $1,000 initial face /month; no per-policy charge | **[std]** |
| Loan rates | 5.0% charged in arrears / 3.0% credited on loaned AV, guaranteed | [S4] |
| Surrender charge | 15-year linear schedule, $18/$1,000 initial level | **[std]** (spec note) |
| ROP endorsement | 50% of CumPrem at anniversary 20, 100% at 25; cap 40% of face; 60-day windows | [S1]; [S3], [S4] (windows) |
| Grace period | 61 days | [S7] |

### (b) Current non-guaranteed scales (insurer-declared snapshot)

| Element | Value | Basis |
|---|---|---|
| Current COI scale | 65% of guaranteed maximum, all durations | **[std]** (spec note; scales not published — research Gaps) |
| Current credited rate i^c | 3.5% annual effective | **[std]** (spec note) |
| Current loan credited rate | 3.0% (= guaranteed [S4]) | [S4] |

The base model holds current scales level for the projection **[std]**; re-rating
logic (current scales moving within guaranteed bounds) is out of scope but the
guaranteed bounds above define the admissible envelope [R3; REG-R26].

### (c) Behavioral / experience assumptions

| Assumption | Recommended public basis | Reference model values |
|---|---|---|
| Best-estimate mortality | 2015 VBT primary tables (sex/smoker-distinct, ANB) [REG-R18], with company A/E positioning informed by the ILEC 2012–2019 study [REG-R19] | 100% of 2015 VBT **[std]** |
| Mortality improvement | — | 1.0%/yr to attained age 85, grading linearly to 0% at 95, applied for max 20 years **[std]** |
| Base lapse (annual) | SOA/LIMRA UL lapse studies: 2009–2013 persistency update [REG-R20]; 2015–2021 UL lapse/surrender study ([R7]; [REG-R21]) | Duration 1: 4.0%; 2: 3.0%; 3: 2.5%; 4–5: 2.0%; 6–10: 1.5%; 11–20: 1.0%; 21+: 0.75% **[std]** |
| Lifetime-guarantee lapse multiplier | Lifetime-SG lapse rates are 45% lower than non-lifetime-SG rates (count and amount bases, 2015–2021) [R7] | 0.55 × base at all durations when `guarantee_age` = 121 **[std]** (level derived from the [R7] finding; duration shape [std]) |
| Dynamic lapse | 63% of surveyed ULSG writers use dynamic lapse; lapse and tail investment returns rated the most critical ULSG assumptions [R8] | formulas below, **[std]** |
| Premium persistency | 2015–2021 UL premium persistency study [REG-R21]; premium-pattern-dependent lapse [R8] | level-pay: scheduled premium paid with 98% annual probability, missed premiums not made up **[std]**; single-pay/ten-pay: as scheduled |
| ROP exercise | no public study in research file | 5% of eligible in-force exercise in the year-20 window; 10% in the year-25 window **[std]** |
| Loan/withdrawal utilization | — | 0 in the base model point **[std]** (sensitivity only) |
| Maintenance expense | — | $75/policy/year, inflated 2.5%/yr **[std]** |
| Acquisition expense | — | year 1: $300/policy + 90% of first-year premium (commissions + issue) **[std]** |
| Claim expense | — | $300 per death **[std]** |

The detailed duration-by-duration ULSG lapse tables sit in the paid SOA/LIMRA
Standard Data Package [R7]; all lapse levels above are therefore **[std]** shapes
anchored to the public highlights findings.

---

## Cash flow components and recursions

### Notation (defined once, used throughout)

| Symbol | Meaning |
|---|---|
| `F` | face amount |
| `P_t` | premium received at BOM of month t (0 in non-premium months) |
| `π`, `π^g` | base (0.25) and shadow (0.08) premium loads |
| `e_pol` | per-policy charge, $5.50/month |
| `e_u`, `e_u^g` | per-unit charges: 0.20 and 0.05 per $1,000 initial face /month |
| `m_t^max` | guaranteed max monthly COI rate per $1,000 (2017 CSO annual/12) |
| `m_t = 0.65·m_t^max` | current monthly COI rate per $1,000 |
| `m_t^g = 0.55·m_t^max` | shadow monthly COI rate per $1,000 |
| `j_c, j_g, j^g` | monthly factors − 1 for current 3.5%, guaranteed 2.0%, shadow 5.5%: 0.0028709, 0.0016516, 0.0044717 |
| `NAAR_t` | base net amount at risk |
| `AV_t', AV_t''` | base AV after premium+expenses; after COI |
| `SG_t', SG_t''` | shadow analogues |
| `W_t` | withdrawal amount (plus $25 fee) |
| `q_t^d, w_t` | monthly best-estimate death and lapse rates (converted from annual) |
| `l_t` | in-force probability at BOM of month t |
| `κ(x)` | GPT corridor factor at attained age x [R4; REG-R13] |

### Monthly processing order **[std]**

1. **Status check.** If `g_{t−1} > 0` (in grace) and cumulative grace ≥ 61 days
   without the required payment, the policy lapses at BOM with no value
   (`CSV ≤ 0` in grace by construction) [S7].
2. **Premium.** `CumPrem_t = CumPrem_{t−1} + P_t`. Base credit `(1 − π)·P_t`; shadow
   credit `(1 − π^g)·P_t`. (Catch-up premiums route identically **[std]**.)
3. **Expense charges.**
   `AV_t' = AV_{t−1} + (1−π)P_t − e_pol − e_u·F/1000 − W_t − 25·1{W_t>0}`
   `SG_t' = SG_{t−1} + (1−π^g)P_t − e_u^g·F/1000 − W_t`  (withdrawal reduces shadow
   dollar-for-dollar **[std]**, spec note).
4. **Death benefit and NAAR.** `DB_t = max(F, κ(x_t)·max(AV_t',0))`;
   `NAAR_t = max(DB_t/(1+j_g) − max(AV_t', 0), 0)`;
   `NAAR_t^g = max(DB_t/(1+j^g) − max(SG_t', 0), 0)` **[std]** (discount convention;
   the account inputs are floored at zero so that a deficit — AV in the
   guarantee-support regime, SG in catch-up territory — never inflates NAAR above the
   discounted DB).
5. **COI.** `COI_t = m_t · NAAR_t/1000`; `COI_t^g = m_t^g · NAAR_t^g/1000`.
   `AV_t'' = AV_t' − COI_t`; `SG_t'' = SG_t' − COI_t^g`.
6. **Insufficiency handling (the low-AV regime).** If `AV_t'' < 0`:
   - if the guarantee is active (`SG_t'' − L_{t−1} > 0`): set `D_t = −AV_t''`,
     `AV_t'' = 0`. The forgone deduction `D_t` is NOT a receivable — the insurer
     funds the negative "account" economics; coverage continues with `AV = 0` and
     `NAAR ≈ DB` [S2, S3, S9 guarantee behavior; accounting treatment **[std]**].
   - else: enter/continue grace, `g_t = g_{t−1} + 1`; required grace payment =
     amount curing the deduction shortfall **[std]**.
7. **Interest.** Unloaned base AV grows at `j_c` (floor `j_g`); loaned AV at the
   loaned credited monthly rate (3.0% annual [S4]):
   `AV_t = AV_t''·(1+j_c)` (split loaned/unloaned when `L > 0`).
   `SG_t = SG_t''·(1+j^g)` — no floor at zero.
8. **Loan interest.** `L_t = L_{t−1}·(1 + (1.05)^{1/12} − 1)` (5% in arrears [S4],
   accrued monthly **[std]**).
9. **In-force test.** Guarantee active iff `SG_t − L_t > 0` [S4; S2, S9]. The policy
   is in force iff (base account can cover deductions, i.e., not in expired grace)
   OR the guarantee is active. Lapse occurs ONLY if all three hold: (i) base AV net
   of charges failed (step 6 else-branch), (ii) `SG_t − L_t ≤ 0`, (iii) the 61-day
   grace expires without cure [S7; S2, S9 mechanics; conjunction **[std]**].
10. **Catch-up requirement.** `C_t = max(0, −(SG_t − L_t))/(1 − π^g)` **[std]**;
    paying `C_t` restores `SG − L` to 0⁺ and the guarantee with it [S7; R1 ex. 7].
11. **Decrements (EOM), deaths first.** With monthly rates `q_t^d` then `w_t`
    applied to `l_t`:
    - death CF: `l_t·q_t^d·(DB_t − L_t)` + claim expense
    - surrender CF: `l_t·(1−q_t^d)·w_t·CSV_t`, `CSV_t = max(AV_t − SC_t − L_t, 0)`
    - ROP exercise (window months only): rate `w^ROP` **[std]**, benefit
      `min(ρ·CumPrem_t, 0.40·F) − L_t`, ρ ∈ {50%, 100%} [S1]; exercise is a full
      surrender [S1, S3].
    - `l_{t+1} = l_t·(1−q_t^d)·(1−w_t)·(1−w_t^ROP)`
12. **Age/duration update**; at attained age 121 all charges and premiums cease,
    recursion continues with `COI = expenses = P = 0` and interest only [S7].

### Cash flow outputs (per month, expected per initial policy)

- Premium income: `l_t·φ_t·P_t` where `φ_t` = premium persistency probability
  (class (c)).
- Death claims: as step 11 (net of loan repayment from proceeds — standard UL
  treatment **[std]**; see spec, "Loans").
- Surrender/ROP benefits: as step 11.
- Expenses: acquisition (month 1), maintenance /12 monthly, claim expense.
- Loan cash flows (drawdown/repayment): 0 in base model point **[std]**.
- Internal transfers (loads, COI, expense charges, interest credits, shadow-account
  entries) are NOT external cash flows; they drive `AV`, `CSV` and the in-force test
  only. This is the gross-liability convention of the library **[std]**.

### Funding-premium solve (level no-lapse premium P*)

Objective: the smallest level annual premium such that the guarantee never fails
before the elected guarantee age:

```
g(P) = min over t in [1, (guarantee_age − issue_age)·12] of (SG_t(P) − L_t)
P*   = min { P : g(P) > 0 }
```

`SG_t(P)` is monotone non-decreasing in P (every premium enters the shadow account
at `(1 − π^g)` and accumulates at `i^g` net of charges that do not increase with P
while `DB = F`; at extreme funding levels a corridor-driven DB increase would raise
shadow COI, so cap the search domain at the guideline premium limitation [R4],
inside which the corridor does not bind for this thin-AV design), so `g` is
monotone and bisection is safe on that domain **[std]**:

1. Bracket: `P_lo = 0` (g < 0 for any nontrivial guarantee), `P_hi` = the premium
   that funds the guarantee as a single-pay net single premium on shadow parameters
   (guaranteed sufficient); double `P_hi` until `g(P_hi) > 0`.
2. Bisect on `g(P) > 0` to tolerance $0.01 of annual premium **[std]**; ~40
   iterations. A secant step on `g` accelerates convergence near the root; fall back
   to bisection when the secant iterate leaves the bracket **[std]**.
3. Full-projection evaluation of `g` per iterate (steps 1–12 with decrements off —
   the solve is contractual, not behavioral **[std]**).

Shorter guarantee ages solve the same way with the earlier stopping time; single-pay
and n-pay premiums solve identically over their premium vectors.

### Calibration **[std]**

No public document discloses shadow-account parameters (research Gaps). The [std]
shadow parametrization (π^g = 8%, i^g = 5.5%, COI^g = 55% CSO, $0.05/unit) is
calibrated so that solved level lifetime premiums fall in the range of observed
market premiums for lifetime GUL. The research file records competitive positioning
but no premium tables [S2]; the calibration target is therefore itself a
standardization, and implementations should re-calibrate against current market
quotes before using outputs comparatively. The illustrative solve output used in
these notes (P* = $10,800 for male 60 NT Standard, $500,000, lifetime) is **[std]**.

### Cumulative-premium variation (main design alternative)

To model the cumulative-premium-test design [R1 8E Design #2; S4 initial NLG; S5]:
replace `SG_t` with the pair (`CumPrem_t^net`, `ReqPrem_t`), where
`CumPrem_t^net = Σ premiums − Σ withdrawals − L_t` [S4] and `ReqPrem_t` is the
contractual required accumulated premium schedule; guarantee active iff
`CumPrem_t^net ≥ ReqPrem_t` [S4, S5]. All other machinery (grace, catch-up = the
schedule shortfall, solve on the required schedule) is unchanged. Note the harsher
observed loan treatment in this family: one design voids the guarantee entirely on
any loan [S5].

---

## Policyholder behavior modeling

All dynamic formulas are **[std]**; the empirical anchors are [R7] (lifetime-SG
lapse 45% lower), [R8] (dynamic lapse used by 63% of writers; premium-pattern
dependence; median 40% of policies assumed sustained by the guarantee after 31 years
in tail scenarios) and [REG-R20]/[REG-R21] (public study bases).

Total monthly lapse: `w_t = min(0.5, b(d) · G · Φ(pattern) · Ψ_t) /12-converted`,
where `b(d)` is the base annual table (class (c)), and:

- `G` (guarantee-duration factor): 0.55 if `guarantee_age` = 121 [R7-anchored],
  1.0 otherwise **[std]**.
- `Φ` (premium pattern): single-pay 0.6; ten-pay 0.8; level 1.0 **[std]**
  (direction per [R8]: higher lapses for level-pay, lower for single-pay).
- `Ψ_t` (funding-status dynamic factor) **[std]**:
  - guarantee active and AV > 0: 1.0
  - guarantee active and AV = 0 (pure guarantee support): 0.6 — the policy is
    deep in the money to the policyholder; empirical anchor: sustained-by-guarantee
    fractions in tail scenarios [R8]
  - guarantee terminated (`SG − L ≤ 0`) and policy surviving on AV: 2.0 (shock)
  - annual floor after the dynamic factor: 0.3% **[std]**
- ROP windows: additional exercise rates 5% (year-20 window) / 10% (year-25
  window) **[std]** applied as full surrenders at the window months; rationale: the
  100% refund dominates CSV for a thin-AV product, but exercising forfeits a
  now-cheap guarantee, so observed exercise should stay modest. No public exercise
  study was found (research file has none).
- Premium persistency: level-pay premiums paid with annual probability 98%
  **[std]**; a missed premium permanently reduces `SG` trajectory (no automatic
  catch-up); catch-up behavior is not modeled in the base run **[std]**.

Anti-selective interaction: mortality of lapsers vs. persisters is NOT adjusted in
the base model **[std]** (no selective-lapse load); this understates claims if
healthy lives disproportionately lapse or exercise ROP — flagged under model risks.

---

## Worked example **[std]** (all figures illustrative)

Model point: male 60 ANB NT Standard, F = $500,000, lifetime guarantee, level
P* = $10,800 paid annually; projection months 301–305 (policy year 26, attained age
85, anniversary premium in month 301). Illustrative COI rates at age 85: guaranteed
max monthly `m^max` = 8.615 per $1,000 **[std]**; current `m` = 5.60 (65%); shadow
`m^g` = 4.74 (55%). Monthly interest factors: base current 1.0028709; shadow
1.0044717. Opening: AV = 2,400.00; SG = 118,000.00; L = 0. Deductions column =
expenses + COI. Decrements are suppressed for clarity (contract-mechanics view).

| Mo. | Prem | Base net prem | Base deductions | Base int. | AV (EOM) | Shdw net prem | Shdw deductions | Shdw int. | SG (EOM) | Status |
|----:|-----:|-----:|-----:|-----:|-----:|-----:|-----:|-----:|-----:|---|
| 301 | 10,800.00 | 8,100.00 | 2,842.68 | 21.98 | 7,679.30 | 9,936.00 | 1,778.15 | 564.13 | 126,721.98 | in force |
| 302 | 0 | 0 | 2,858.47 | 13.84 | 4,834.67 | 0 | 1,783.90 | 558.66 | 125,496.74 | in force |
| 303 | 0 | 0 | 2,874.40 | 5.63 | 1,965.90 | 0 | 1,789.71 | 553.16 | 124,260.19 | in force |
| 304 | 0 | 0 | 2,890.47 → 1,965.90 taken; 924.57 forgone | 0.00 | **0.00** | 0 | 1,795.57 | 547.62 | 123,012.24 | in force — guarantee |
| 305 | 0 | 0 | 2,900.89 forgone (AV = 0) | 0.00 | 0.00 | 0 | 1,801.49 | 542.01 | 121,752.76 | in force — guarantee |

Reading the table: the base account exhausts in month 304 — monthly deductions
(~$2,900, dominated by COI on a ~$497K NAAR) exceed the annual net premium spread
over the year, and the residual $924.57 of month-304 deductions is forgone by the
insurer (`D_304`), not carried as a receivable. The policy does NOT enter grace:
the shadow account, charged at the lighter [std] shadow parameter set and credited
at 5.5%, stands at ~$123K, so the in-force test `SG − L > 0` holds and coverage
continues with `NAAR ≈ DB = $500,000`. From month 305 onward the insurer is funding
the full mortality cost of the guarantee — the "negative account economics" regime
that dominates late-duration GUL liability cash flows. Arithmetic: net premium =
P × (1 − load); deductions = per-policy 5.50 + per-unit 100.00 + COI m·NAAR/1000
(base; shadow analogues 0/25.00/m^g·NAAR^g/1000); NAAR = 499,176 − max(AV′, 0)
(base — the floor binds in month 305, where AV′ = −105.50 but COI is charged on the
full 499,176 NAAR), 497,774 − SG′ (shadow; SG′ > 0 throughout); interest = balance
after deductions × monthly factor − 1.
Independent recomputation may differ by cents due to rounding.

---

## Statutory accounting and capital

Framework — no DAC, the exhibits, AVR/IMR, asset adequacy analysis, RBC — is in
`us/regulatory/statutory-accounting-and-capital.md` (concepts) and
`us/regulatory/technical-notes.md` (formulas, factors, algorithms); only ULSG-specific
material is stated here. [REG-R#] cites the shared U.S. numbering, now R1–R157 with
R114–R124 and R143–R149 unused by design; [R#]/[S#] stay the product numbering of
`sources.md`.

### Contract classification and reporting

**Life contract, permanently.** A benefit contingent on death carries mortality risk, so this
is a **life contract** under the SSAP No. 50 ¶5 test, never deposit-type [REG-R78 ¶¶5, 9], and the
classification is made at inception and **cannot change** [REG-R78 ¶5] — it survives
account-value exhaustion, guarantee expiry and the pure guarantee-support regime. **Premiums
are premium income**, gross when due, flexible premiums when received: `l_t·φ_t·P_t` and
catch-up premiums `C_t` are the Summary of Operations premium line, not a direct credit to
reserve, and the change in loading on deferred and uncollected premium is an **expense**, not
a premium offset [REG-R79 ¶¶2–5, ¶11].

**Where it reports.** Reserves sit in **Exhibit 5**, gross with a separately computed ceded
deduction, Column 1 stating the valuation standard **by years of issue** — PBR-era business as
**VM-20NPR** and **VM-20 DET/STO** on **two lines**, the net premium reserve and the excess
over it [REG-R89][REG-R90]. The Analysis of Operations gives the product its own column,
**Universal Life With Secondary Guarantees**, with three rules that bite: **indexed UL with
secondary guarantees reports there, not under Indexed Life**; **expired guarantees still report
as ULSG**; incidental riders (waiver of monthly deductions, terminal illness acceleration,
children's term) report on the **base contract's** line [REG-R89]. Face in force feeds the
**Exhibit of Life Insurance**, thousands, incurred basis [REG-R89]. A waived monthly deduction
is "not to be considered revenue nor a benefit paid" [REG-R79 ¶14] — an internal transfer as in
step 5; the observed design waiving deductions but **not** the full no-lapse premium [S4] can
still let the guarantee fail.

**General account only**, so no SSAP No. 56 split, no separate account AVR or IMR, no C-4a
separate account liability charge [REG-R83][REG-R128]. **No DAC**: acquisition cost is expensed
as incurred [REG-R75 ¶2], so the reference 90%-of-first-year-premium + $300 **[std]** assumption
hits surplus in the issue year against one year of a level no-lapse premium while the closing
reserve already sits at the VM-20 ULSG minimum — first-year strain is structural here, not an
artefact [REG-R74][REG-R75].

### Reserve basis

**Post-operative-date issues: VM-20, own reserving category.** VM-20 constitutes CRVM [REG-R3].
**ULSG is one of the three reserving categories**, keeping directly written policies **beyond
the end of the contractual secondary guarantee period** and excluding extended term and reduced
paid-up [REG-R3]; the three category results are **summed**, so an ULSG excess never offsets
All Other slack [REG-R3 §2.A, §4.C, §5]. Carry two distinct keys per policy — the **reserving
category** (Valuation Manual definition [REG-R3]) and the **statement column** (which also
collects indexed UL with secondary guarantees [REG-R89]).

**Both exclusion routes are closed or near-closed.** ULSG that is not a "non-material secondary
guarantee" is **deemed to fail the deterministic exclusion test** [REG-R3 §6.B], and **variable
life and ULSG may not use the stochastic exclusion certification method** [REG-R3 §6.A]. The
representative lifetime guarantee is material on any reading, so the **DR is compulsory** and
the SR is escapable only via the SERT ratio test or the Demonstration Test — both of which
**re-impose VM-G Sections 2 and 3**, with a VM-31 sub-report and a report of **readiness to
compute** DR and/or SR required even where neither is computed [REG-R109][REG-R108]. The full
VM-20 machinery is therefore not optional for GUL as it is for whole life or ordinary UL. Rate
detail: §3.B.5.c amounts uplift the calendar-year NPR rate by **1.5%, capped at 125% of it**,
nearest quarter of 1%, **ties up**; §3.B.5.d uses the unuplifted rate, **ties down**, with **0%
lapse throughout** [REG-R3].

**Pre-PBR issues and in-force.** Formulaic CRVM reaches current valuations through **VM-A item
A-830** and **AG 38** via the VM-C index [REG-R110][REG-R41][REG-R6]; deficiency
reserves survive under Actuarial Guideline I in Exhibit 5 **Miscellaneous Reserves**
[REG-R41][REG-R89]. **A-830 as printed in the AP&P Manual has now been read in full and is cited
here at first hand as [REG-R154]** — the manual is a free download, not the paid publication the
library once recorded [REG-R73] — and so has **A-820** [REG-R153], the appendix A-830 leans on for
what a basic reserve *is* (¶4 → A-820 ¶¶11–13), for the minimum reserves whose excess is the
deficiency reserve (¶6 → A-820 ¶¶19–20) and for the maximum valuation interest rates
(¶8 → A-820 ¶¶7–10). **The AG I text was still not retrieved** [REG-R41], so the deficiency-reserve
*interpretive* layer stays second-hand even though the construction beneath it no longer is:
A-820 ¶19 states the deficiency as a **floor on the policy reserve** rather than as an additive
item, while A-830 defines a **separate** quantity — quantity A, a full re-run of the basic reserve
with the **guaranteed** gross premium substituted for the net premium duration by duration wherever
the gross is the smaller — less the basic reserve [REG-R153 ¶19][REG-R154 ¶¶6, 17]. The key is the
**guaranteed** gross premium, "guaranteed and determined at issue" [REG-R154 ¶7], not premium
actually collected — for a flexible-premium GUL those are different things. A real block carries
**both** bases in one Exhibit 5 column keyed
by year of issue [REG-R89]; moving between them is a **change in valuation basis** — direct to
surplus at the **beginning of the year**, not graded in, shown in Exhibit 5A [REG-R79][REG-R89].

**What A-830 prescribes for this contract — ¶¶29–32, and a citation correction.** The appendix is
a **flat sequence of paragraphs ¶¶1–32 plus an unnumbered Attachment, with no Sections at all**,
and the words "Model #830" and "Regulation XXX" appear **nowhere** in it, so a "Model 830 Section
7" citation does not resolve against this print; the ULSG material is at **¶¶29–32** [REG-R154].
Scope first, because A-830 carries a ULSG carve-out this library did not have: a UL policy is
**outside the appendix entirely** where **all three** limbs of ¶3.a.ii hold — secondary guarantee
period **five (5) years or less**, specified premium **not less than** the net level reserve
premium for that period (ultimate 2001 CSO rates from 1/1/2004), and initial surrender charge
**not less than 100% of the first-year annualized specified premium** [REG-R154 ¶3.a.ii]. The test
is on the **policy**, so the representative lifetime guarantee fails the first limb outright, and
so does the observed design layering a 5-year cumulative-premium guarantee *underneath* a lifetime
shadow-account guarantee [S4] — its policy-level secondary guarantee period is still lifetime. (At
the worked model point the third limb fails too: the **[std]** initial surrender charge
$18/$1,000 × $500,000 = $9,000 is below the **[std]** $10,800 annual premium.) A standalone
short-guarantee UL is the design the carve-out is aimed at, and needs all three limbs tested.
Inside the appendix [REG-R154 ¶¶29–32]:

- **A secondary guarantee (¶29.a) is wider than the contract clause.** It is a guarantee that the
  policy stays in force at the original schedule of benefits **subject only to payment of specified
  premiums**, **or** (from 1/1/2004, on ultimate 2001 CSO rates) a policy whose **minimum premium
  at any duration is less than the corresponding one-year valuation premium** — the second limb
  sweeps in policies with no explicit guarantee clause at all.
- **Premium substitution and segmentation (¶30).** Basic reserves for the secondary guarantee are
  the **segmented reserves for the secondary guarantee period**, with gross premiums **set equal to
  the specified premiums, if any, or otherwise to the minimum premiums**, and the segments
  determined by the ¶5 contract segmentation method run on those substituted premiums. **There is
  no unitary leg** — ¶30 says "segmented reserves", where ¶21 says `max(segmented, unitary)` for
  the nonlevel non-UL business.
- **The two premium definitions the model must be able to produce.** *Specified premiums* are the
  premiums whose payment guarantees the original benefit schedule but which would otherwise be
  insufficient to keep the policy in force absent the guarantee **if maximum mortality and expense
  charges and minimum interest credits were made and any applicable surrender charges were
  assessed**. The *minimum premium* for a policy year is the premium that, paid into a policy with
  a **zero account value at the start of the year, produces a zero account value at the end**, on
  the policy cost factors and crediting rate **guaranteed at issue** [¶29.c–e]. Both are
  **base-account, guaranteed-basis** quantities: neither is `SG_t`, and neither is the solved `P*`,
  which is a shadow-account solve on **[std]** parameters.
- **Deficiency and the floor.** ¶31 runs the ¶22 deficiency construction over the secondary
  guarantee period on the same substitution; ¶32 makes the minimum reserve during the guarantee
  period the **greater** of (a) basic plus deficiency for the secondary guarantee and (b) "the
  minimum reserves required by other appendices governing universal life plans". Limb (b) is an
  **unnamed cross-reference — A-830 does not say which appendix item it means, and it must not be
  resolved to A-585 on this text** [REG-R154 ¶32]. That gap stays open here.
- **More than one guarantee (¶29.b).** The minimum reserve is the **greatest of the respective
  minimum reserves of each unexpired secondary guarantee, each valued ignoring all the others** —
  not a combined valuation, which bears directly on the layered design at [S4]. And a guarantee
  **unilaterally changed by the insurer after issue is deemed to have been made at issue**, forcing
  recalculation of the ¶30/¶31 reserves **from issue**.

**What A-830 does not say, stated so it is not read into it.** It prints **no calendar effective
date for itself** — "the effective date of this appendix" is an unresolved placeholder used eleven
times — so no XXX commencement date may be attributed to [REG-R154]. The only calendar dates it
prints are the **1 January 2004** cutover to the 2001 CSO Mortality Table for basic reserves (¶16),
deficiency reserves (¶17) and the tabular cost of insurance (¶23, on **ultimate** rates), with the
pre-2004 1980-CSO-with-elective-select-factors branch **retained in full** for older issues. And it
contains **no AG 38 content whatever** — no shadow account, no funding ratio, no
minimum-gross-premium definition, no 8C/8D/8E analogue — and no mention of the 2017 CSO, the
Valuation Manual, VM-20 or PBR [REG-R154]. The funding-ratio interpolation this model computes is
**AG 38's** contribution [R1; REG-R7]; it must not be attributed to A-830.

**Asset adequacy analysis is part of the minimum reserve.** SVL §6.B makes the actuary's
required amount part of minimum reserves [REG-R1] and VM-30 requires any shortfall to be
**established as an additional reserve**, reported as "additional actuarial reserves —
asset/liability analysis" in Exhibit 5 Miscellaneous Reserves [REG-R100][REG-R89]. **Citation
detail, now that the appendix print has been read:** in the AP&P codification that requirement
does not sit in A-820 at all — A-820 as printed has **no §6.B analogue**, its ¶16 carrying only
the aggregate nonforfeiture-basis floor — but in the four-paragraph **A-822 ¶3**, which makes
the additional reserve mandatory on top of the A-820 aggregate, with ¶4 providing that its
release "would **not** be deemed an adoption of a lower standard of valuation" [REG-R153]. A
reader sent to A-820 for §6.B will not find it. It bites
hardest here — the projection must reach run-off of a lifetime guarantee, and the Academy survey
found **ULSG the longest-horizon life product, 46% of companies projecting beyond 40 years**
against 28% for individual traditional life (longer periods still are reported for structured
settlements and long-term care, which are not life products) (**2012 survey, a
practice indicator, not a benchmark**) [REG-R111]; starting assets are capped at the statement
value of the reserves tested [REG-R29], and the "New York 7" is a **New York** requirement, not
an NAIC one [REG-R112].

### What this product's model must additionally produce

Shared contract: `us/regulatory/technical-notes.md`, "Required model outputs", not restated.
ULSG adds:

| Statutory item | Additional output this model must emit |
|---|---|
| Exhibit 5, ULSG line, two-line VM-20 split [REG-R89][REG-R90] | NPR seriatim and the excess of max(DR, SR) over Σ NPR, keyed by **year of issue** and **reserving category**, policies past the guarantee expiry still in the ULSG category [REG-R3] |
| VM-20 §3.B.5 net premium reserve [REG-R3] | **FFSG, ASG, LSG** per policy per period — `SG_t` *is* ASG, FFSG is a backward solve on the same shadow recursion, and the funding ratio `R` drives the §3.B.5.c level lapse |
| A-830 ¶¶29–32 formulaic ULSG reserve, pre-PBR issues [REG-R154] | **Specified premiums** by policy year, or **minimum premiums** where none are specified (the premium taking a **zero** account value at the start of a policy year to **zero** at the end, on cost factors and crediting rate guaranteed at issue), and the **¶5 segment boundaries derived from those premiums** — base-account, guaranteed-basis quantities, *not* `SG_t` and *not* the solved `P*`. Also the **guaranteed** gross premium series for the quantity-A deficiency run [REG-R154 ¶¶7, 17] |
| Analysis of Increase in Reserves, ULSG column [REG-R90] | Tabular net premiums, tabular interest at the **NPR valuation rate** (uplifted or not per §3.B.5.c/d), tabular cost, reserves released — **valuation-basis** quantities on prescribed mortality and the prescribed §3.B.5 lapse, not best-estimate decrements |
| Exhibit of Life Insurance [REG-R89] | Face in force by year, incurred basis, net of elected decreases, withdrawal-driven reductions and ROP surrenders |
| C-2 net amount at risk [REG-R142] | **Face in force − statutory reserve, net of reinsurance** — a statement quantity, *not* the contractual `NAAR_t` of step 4 (see traps) |
| AG 48 Primary Security [REG-R11][REG-R12] | VM-20 components on a **pre-financing** basis per ceded cohort so the shortfall is measurable per cession; gross and ceded never netted, the ceded credit on the **same mortality, interest and method** [REG-R89][REG-R92 ¶37] |
| Tax reserve [REG-R16]; DTA scheduling [REG-R97] | max(net surrender value, 92.81% × NAIC-method reserve) capped at statutory — the 92.81% leg binds almost everywhere on a thin-AV GUL; the issue-year ordinary loss **cannot be carried back** post-2017, so admittance runs through the RBC-band and DTL-offset components |

### Risk-based capital

**C-2 mortality dominates and ULSG sits in the worst bucket.** Exposure is net amount at risk
net of reinsurance, now derived from annual statement lines rather than company records
[REG-R142]. Categories are **pricing-flexibility** categories, not product codes, and the
instructions name **ULSG and non-participating whole life** as the examples of **Permanent
without Pricing Flexibility** — the highest-factor bucket, **0.00400 / 0.00175 / 0.00120** per
dollar of NAR on the first $500M, next $24,500M and over $25,000M [REG-R128][REG-R133];
calibration used a **20-year risk exposure period for ULSG** against 10 for term and 5 with
in-force pricing flexibility [REG-R131]. The test asks whether in-force rates can be
*materially* adjusted within **5 policy years**, present-valued against
`flexibility factor × NAR` [REG-R128]; here the levers — current COI at 65% of the guaranteed
maximum, the declared credited rate — reach the **base** account only while the guarantee runs
on the contractual shadow parameter set, so repricing moves account value and lapse but not the
guarantee (**[std]** inference, consistent with the instructions' placement of ULSG). Where the
assessment is not performed the default is the **same** bucket [REG-R128][REG-R133] — a
defensible baseline, not an assessment. **Size and mix set the marginal rate, not the block**:
the NAR bands apply to the company's *total* individual and industrial life NAR [REG-R128].

**C-3a is the low bucket, and single-pay is the exception.** Life insurance reserves and single
premium life take **0.0095** pre-tax, cut by one third to **0.0063** on an unqualified
asset-adequacy opinion — **or one qualified solely because of AG 48 direction**, exactly the
qualification an AXXX-financed ULSG writer may carry [REG-R128]. But C-3 Phase I scope is
"Certain Annuities" **plus single premium life** [REG-R128][REG-R135], so a level-pay GUL is
outside C-3 cash flow testing while the **single-pay / 1035 "sweet spot" design** [S1, S2] falls
inside it — a funding-pattern dependency, and `premium_pattern` is already a model point
attribute. Whether testing is compelled is decided by the LR049 significance and stress tests,
which need the whole formula computed first [REG-R128].

**What does not apply.** **C-2 longevity** is reserve-based on life-contingent annuity benefits
and the base contract has none — the out-of-scope income-conversion rider [S1] would enter that
base if brought in, while a guaranteed installment payout [S4, S7] is a supplementary contract
**without** life contingencies: Exhibit 7, deposit-type, out of it [REG-R128][REG-R89][REG-R80 ¶5]
(the shared applicability matrix leaves GUL blank on the deposit-type and Exhibit 7 rows because
the research did not consider a GUL settlement option, not because one is excluded).
**C-3 Phase II** (CTE 98) covers only the AG 43 / VM-21 population, **C-1cs** and the separate
account charges do not apply, and the **50% dividend liability credit** in TAC does not reach a
non-participating design [REG-R128].

**C-4a, covariance and AG 48.** C-4a is **2.53%** of Schedule T life premiums and annuity
considerations [REG-R128], so it tracks the funding pattern — single-pay concentrates it in one
year, level-pay spreads it. **C-2 is a standalone squared term** in the covariance combination
while C-0 and C-4a sit outside the radical [REG-R128], so for a monoline ULSG writer C-2
dominates. **AXXX financing hits both sides of the ratio, through two distinct quantities**:
ULSG (AXXX) and term (XXX) are the only two products AG 48 and Model #787 reach
[REG-R11][REG-R12]; the **AG 48 Primary Security shortfall is doubled after covariance** then
halved into Authorized Control Level, landing **dollar for dollar** and applying **even where a
state has waived AG 48 compliance**, while Total Adjusted Capital is separately reduced by the
**XXX/AXXX reinsurance RBC shortfall** — a different figure, computed on the captive
consolidated exhibit rather than as a Primary Security shortfall by cession
[REG-R128]. TAC includes the AVR only to the extent **not consumed in asset
adequacy testing** [REG-R128][REG-R29], so the AAT run must report the AVR it used; action
levels, the trend test and the RBC Plan's five-year projection are at [REG-R125].

### Product-specific interactions and traps

- **The shadow account is not a statutory reserve.** `SG_t` is a notional in-force test input,
  never payable [S2, S3]: not an asset, not a liability, not admitted. It enters statutory
  reporting only as the **ASG** input to the VM-20 §3.B.5 NPR [REG-R3] and the AG 38
  funding-ratio numerator [R1]. Never book it, and never let it reduce a reserve. It is also
  **not** the A-830 premium input: ¶30 substitutes **specified premiums, if any, or otherwise
  minimum premiums** — base-account, issue-guaranteed quantities — for gross premiums, and runs
  the ¶5 segmentation on those [REG-R154 ¶¶29.c–e, 30].
- **Forgone monthly deductions are not a receivable.** `D_t` creates no admitted asset and no
  accrual against future premium — the guarantee cost emerges through the reserve. That
  treatment is **[std]**; no retrieved source addresses it, and an invented accrual would
  understate the guarantee cost.
- **Two net amounts at risk, and they are not the same number.** `NAAR_t` is a **COI charge
  base**; the C-2 exposure is **face in force less statutory reserve**, net of reinsurance, off
  the annual statement [REG-R142]. In the guarantee-support regime `AV = 0` drives the COI NAAR
  to ≈ DB while the reserve is largest, so they diverge maximally where the block is riskiest.
- **AG 38 and VM-20 coexist in one column** — 8C/8D for pre-PBR in-force, 8E fixing minimum
  gross premiums by policy design and capping guaranteed shadow credits [R1; REG-R7]; VM-20 for
  post-operative-date issues [REG-R3]; two standards, one column, keyed by year of issue
  [REG-R89]. AG 38 is an *interpretation*, and the text it interprets is **A-830 ¶¶29–32**
  [REG-R154] — never "Model 830 Section 7": the AP&P print is a flat ¶¶1–32 with no Sections and
  never uses the names "Model #830" or "Regulation XXX". And the exclusion tests are a **wall
  here, not a cliff**: deemed DET failure plus
  the SET certification bar leaves no configuration of this contract without a DR
  [REG-R3][REG-R109].
- **AXXX financing, AG 53 and AG 55.** The Model #787 / AG 48 Required Level of Primary Security
  is VM-20-based — greater of DR and NPR, greatest of DR/SR/NPR where the stochastic exclusion
  fails — with reserve credit disallowed on non-compliance [R6; REG-R11][REG-R12], so the engine
  must also run **gross of the financing structure**. AG 53 and AG 55 triggers are
  **company-level and treaty-level, not product-level** [REG-R105][REG-R103], but a large ULSG
  block ceded offshore is squarely in AG 55 scope, whose §6.G accepts the **pre-reinsurance PBR
  reserve** in lieu of the mandatory cash flow testing run — the PBR engine run gross of a
  specific treaty [REG-R103].
- **Negative-IMR admittance reaches back into this block's reserve.** The INT 23-01 gates are
  company-level, but ¶9.e requires admitted negative IMR to be captured in the PBR calculation
  (VM-20 §7.D.7) or in asset adequacy testing (VM-30 §3.B.5), with a reconciliation
  [REG-R87][REG-R100]. It sunsets **December 31, 2026 with automatic nullification January 1,
  2027** as written, and the date may move again [REG-R87].
- **No AVR or IMR factor value exists anywhere in this library** — those tables were
  **deliberately not transcribed** [REG-R85][REG-R89]; a model hard-coding remembered values will
  be wrong. Likewise **RBC reads statement values, not model values** [REG-R128], so a forward
  capital ratio needs a projected annual statement — carried as **[unverified]** as a stated
  requirement in `us/regulatory/technical-notes.md`.

## Valuation and reserve pointers

Statutory classification, the reporting exhibits, which reserve basis applies and the
capital consequences are in "Statutory accounting and capital" immediately above; this
section is the product-mechanics pointer list. This library projects **gross liability
cash flows**; reserve layers consume those cash flows and are cited, not reproduced:

- **VM-20 (PBR, post-2017 issues)**: ULSG is its own reserving category; reserve =
  NPR floor plus excesses of deterministic (DR) and stochastic (SR) reserves. The
  ULSG NPR during the SG period is the greater of a non-SG amount and
  `min(ASG/FFSG, 1)·NSP − E` with the amortized expense allowance
  (x1 = level gross premium; y2–5 = 10% of it; z1 = $2.50/$1,000) and the prescribed
  funding-ratio-driven lapse `L = R·1% + (1−R)·0.5%·r` [R2]. Note the model's
  `SG_t` IS the "actual secondary guarantee" (ASG) input, and the fully-funded
  value FFSG is a backward solve on the same shadow recursion [R2]. See also the
  Academy practice note [R9; REG-R23] and the Valuation Manual itself [REG-R3].
  Material-SG business cannot use the life PBR exemption [R2; R9].
- **AG 38 / A-830 (pre-PBR issues and in-force)**: the formulaic layer underneath
  AG 38 is now sourced at first hand. A-830 **¶¶29–32** — not "Section 7"; the AP&P
  print is a flat ¶¶1–32 with no Sections — makes the basic reserve the **segmented
  reserve over the secondary guarantee period** computed on specified (else minimum)
  premiums with **no unitary leg**, the ¶22 deficiency on the same substitution, and a
  floor at the greater of that sum and an **unnamed** "other appendices governing
  universal life plans" limb; several unexpired guarantees are valued **stand-alone and
  the greatest taken** [REG-R154 ¶¶29–32]. A-830's own basic reserves, deficiency
  comparator and maximum valuation interest rates are cross-references into **A-820
  ¶¶11–13, ¶¶19–20 and ¶¶7–10** [REG-R153]. On top of that, AG 38 supplies what A-830
  contains nothing of: funding-ratio interpolation between basic+deficiency reserves
  and the net single premium for the guarantee, prescribed lapse caps and
  surrender-charge offsets; Section 8E Method I
  defines minimum gross premiums off this very shadow recursion [R1; REG-R6;
  REG-R7]. Detail in "Statutory accounting and capital", "Reserve basis" above.
- **Reserve financing**: Model 787 / AG 48 Primary Security requirements are
  VM-20-based (greater of DR and NPR; greatest of DR/SR/NPR if the stochastic
  exclusion fails) [R6; REG-R11; REG-R12].
- **Tax reserves**: greater of net surrender value and 92.81% of the NAIC-method
  reserve, capped at statutory [REG-R16].
- **Professional standards**: ASOP 52 (PBR work) [R10; REG-R31]; ASOP 7 (cash flow
  analysis) [REG-R27]; ASOP 56 (model governance — applies to this reference
  implementation itself) [REG-R32].

## Key sensitivities and model risks

**Dominant assumptions (in order):**

1. **Lapse.** First-order by a wide margin: GUL is lapse-supported. Every lapse of a
   funded guarantee releases the insurer from a deeply in-the-money claim; lifetime-SG
   experience already runs 45% below non-lifetime SG [R7], insurers rate lapse among
   the two most critical tail assumptions, and the median tail assumption keeps 40%
   of policies in force purely on the guarantee after 31 years [R8]. PV of claims is
   convex in the ultimate lapse rate near zero — sensitivity runs must include
   ultimate lapse 0% **[std]** recommendation.
2. **Mortality level and improvement at high attained ages.** With `NAAR ≈ DB` for
   decades in the guarantee-support regime, claims PV moves nearly linearly with
   85+ mortality; improvement assumptions compound [REG-R18, REG-R19 bases].
3. **Premium persistency / funding pattern mix.** Single-pay vs. level-pay changes
   both the guarantee trajectory and lapse behavior [R8; REG-R21]; a 98% vs. 100%
   payment probability materially shifts guarantee failure times for exactly-funded
   level payers **[std]** observation.
4. **ROP exercise.** Exercise at the 100% window is an option against the insurer
   whose cost depends on cumulative premiums vs. reserve released; mis-set exercise
   rates distort years 20–26 cash flows [S1 design; rates [std]].

**Known modeling pitfalls:**

- **NAAR discount convention.** `DB/(1+j_g)` vs. `DB` un-discounted changes COI by
  ~0.17% per month at 2%; be consistent between base and shadow accounts and
  against any carrier illustration being matched **[std]** convention here.
- **Monthly COI conversion.** annual/12 vs. 1−(1−q)^(1/12) differs materially at
  ages 85+ (q > 0.10); this model fixes annual/12 **[std]** — do not mix.
- **Flooring.** `AV` floors at 0 only while the guarantee is active; `SG` never
  floors (its negative part is the catch-up requirement). Flooring `SG` at 0
  destroys the catch-up computation and misprices restoration [R1 ex. 7 logic].
- **Forgone deductions are not receivables.** `D_t` must not accrue against future
  premiums or `AV` recoveries **[std]**; treating it as a receivable understates
  the guarantee cost.
- **Order of tests.** Run the guarantee test AFTER the full monthly deduction
  attempt; testing before deductions lets a policy lapse a month early (or late)
  and shifts claim timing at exactly the durations where NAAR ≈ DB.
- **ANB/ALB mismatch.** 2017 CSO and 2015 VBT each exist in ANB and ALB variants
  [REG-R17, REG-R18]; this model is ANB throughout **[std]** — a mixed basis shifts
  COI and expected claims by up to half a year of mortality.
- **Guarantee-age grid.** The solve target `SG > 0` strictly; a `≥ 0` target with
  monthly grids can leave the guarantee failing on the final monthiversary.
- **Shadow parameters are standardized.** All shadow-account parameters are [std]
  calibrations, not observed contract values (research Gaps: no specimen policy
  form retrieved; no carrier publishes shadow parameters). Conclusions that depend
  on the shadow parametrization (funding ratios, catch-up costs, VM-20 ASG/FFSG
  inputs) carry that calibration risk.
- **Out-of-model features.** 7702/7702A testing (GPT premium limits, MEC status
  [R4, R5]), terminal-illness acceleration (treated as CF-neutral **[std]**),
  selective-lapse mortality adjustment, and NGE re-rating are not modeled in the
  base run; each is a documented extension point.
