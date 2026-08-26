# Technical Notes

**Status:** Draft, 2026-08-26 (all cited sources accessed 2026-08-26).

**Scope note.** These notes specify the reference liability cash-flow projection model
**`EC_FR_A`**, on an **annual** grid, for the standardized composite eurocroissance support
defined in `product-spec.md` (same directory). This is not any single insurer's support.
[S#]/[R#] tags refer to the source list in `sources.md` (numbering carried verbatim from
`_research/eurocroissance.md`); [REG-R#] tags refer to the cross-product reference library
`references/regulatory-and-actuarial-references.md`. **[std]** marks standardizations
introduced for the reference implementation; [unverified] marks claims not confirmed against
a retrieved document. Parameter values are identical to those in `product-spec.md`.

Two facts about the sourcing govern how these notes must be read. First, **no contractual
document for any eurocroissance support was retrieved** [S10]: the mechanics come from the
Code des assurances [R1] [R2] [R3] and from one published actuarial *mémoire* [R13], and
every insurer-level parameter is either a third-party fact-sheet figure [S8] or **[std]**.
Second, this product is a **fund-level** construct — the part value is common to all
engagements of an auxiliary account [R2 R. 134-2](#frlib-eurocroissance-r2), and the PCDD and the *provision pour
garantie à terme* are collective [R8] — so a single-policy projection is an abstraction that
must be handled explicitly; see "Known modeling pitfalls". The sibling euro-fund notes at
`../assurance_vie_euro/technical-notes.md` were drafted in parallel with these, so where the
two products are compared here the comparison is made against the Code des assurances
directly rather than against that document.

---

## Model scope and conventions

- **Purpose.** Project gross best-estimate liability cash flows (premiums in; surrender, death
  and maturity claims out; charges; the insurer's asset contributions) for single-policy
  eurocroissance model points on the two composite chassis — **Chassis A** (1° engagement:
  *provision mathématique* plus parts) and **Chassis B** (2° engagement: parts only, guarantee
  at maturity). Reserves are not computed here.
- **Projection frequency.** **Annual [std]**, matching the model name `EC_FR_A`. The governing
  discretion cycle — the striking of the *compte de participation aux résultats* and the
  allocation of its balance — is annual [R2 R. 134-4](#frlib-eurocroissance-r2). The code additionally requires the
  diversification provision to be re-struck at an **intermediate value at least monthly** in
  every month in which the participation account is not struck [R3 A. 134-5](#frlib-eurocroissance-r3); the annual grid
  compresses that to one striking a year, a simplification recorded under pitfalls.
- **The provisions are state variables, not cash flows.** Policy cash flows are premiums,
  claims, charges and expenses; `pm`, `pd`, `parts` and `part_value` drive claim amounts
  through the surrender, maturity and death formulas [R2 R. 134-5, R. 134-6](#frlib-eurocroissance-r2).
- **Two liability layers.** The savers' layer (`pm`, `pd`) is inside the auxiliary account.
  The insurer's layer (`pgt`, `insurer_contribution`, `pcdd`) is *not* the savers' money: the
  PGT is funded from own funds and sits outside the participation account [R3 A. 134-2](#frlib-eurocroissance-r3)
  [R1 L. 134-3](#frlib-eurocroissance-r1), and the PCDD is collective with no individual rights [R8 R. 343-3 10°](#frlib-eurocroissance-r8). Both
  are reported separately and never enter a benefit.
- **Timing conventions [std].** Charges in number of parts and scheduled premiums at the
  **start** of the policy year (BOY); the asset return accrues over the year; the performance
  levy, the re-striking of `pm`, the determination of `pd` and `part_value`, and any insurer
  contribution at the **end** of the year (EOY), in the processing order below; decrements and
  claims at EOY after the striking.
- **Age basis.** *Âge atteint* (age last birthday) **[std]** — art. A. 335-1 applies the
  homologated tables with the annexed *décalages d'âge* rather than fixing a model age basis
  [REG-R23].
- **Currency and rounding.** EUR; single-policy model points projected on an expected
  (probability-weighted) basis, `pols_if` multiplying per-policy amounts. Intermediate values
  at full precision; currency to the cent, parts and part values to four decimals **[std]**.

---

## Model point attributes

| Attribute | Type | Example (worked configuration) |
|---|---|---|
| `point_id` | int | 1 (Chassis A), 2 (Chassis B) |
| `engagement_modality` | enum {`euro_and_parts`, `parts_only`} | `euro_and_parts` / `parts_only` |
| `issue_age` | int (âge atteint) | 57 |
| `sex` | enum {M, F} | M |
| `policy_term` | int, years to the *échéance* `n` | 10 |
| `duration_ifo` | int, completed policy years at valuation | 0 |
| `premium_gross` | currency, initial *versement* | 10,000.00 |
| `premium_top_up` / `premium_top_up_t` | currency, free additional *versement*, and the policy year at whose end it is paid | 2,000.00 / 3 |
| `guarantee_rate` | %, `g` — share of net premiums guaranteed at `n` | 100 % |
| `entry_charge_rate` | %, base R. 134-3 1° | 2.00 % |
| `parts_charge_rate` | % p.a., base R. 134-3 4° | 0.80 % |
| `perf_charge_rate` | % of positive financial performance, base R. 134-3 5° | 10 % |
| `exit_charge_rate` | %, base R. 134-3 6° | 0.00 % |
| `part_value_init` / `min_part_value` | currency, part value at the account's inception and its contractual floor [R2 R. 134-1](#frlib-eurocroissance-r2) | 10.0000 / 5.0000 |
| `parts_ifo`, `pm_ifo`, `own_assets_ifo` | float / currency / currency — parts, PM and account assets at valuation (in-force cells) | — (new business) |
| `lock_up_years` | int, non-surrender period, capped at `min(n, 8)` [R2 R. 134-5](#frlib-eurocroissance-r2) | 0 |
| `surrender_indemnity_rate` | %, capped at 5 %; R. 132-5-3 lets the contract provide for **no indemnity at all** once ten years have elapsed [R10], and the reference contract charges none at any duration. `EC_FR_A` returns 0 beyond ten years unconditionally **[std]** | 0.00 % |
| `death_floor_flag` | bool — *garantie décès plancher* [S1] [S2] | true |
| `annuity_option_flag` | bool — conversion into a *rente viagère* at `n` [R2 R. 134-6](#frlib-eurocroissance-r2) | false |

---

## State variables

| Variable | Description | Updated |
|---|---|---|
| `mg` | Guaranteed amount payable at the *échéance* = `g ×` cumulative net premiums, run down for exits [R13] | on each *versement* and exit |
| `own_assets` | Auxiliary-account assets attributable to the policy, at realisation value, **excluding** any outstanding insurer contribution [R2 R. 134-8](#frlib-eurocroissance-r2) | annual recursion |
| `pm` | *Provision mathématique* = `mg` discounted at `i_pm` (Chassis A only; identically 0 on Chassis B) [R2 R. 134-2](#frlib-eurocroissance-r2) | EOY re-strike |
| `pd` | *Provision de diversification*, the savers' individualised rights [R8 R. 343-3 9°](#frlib-eurocroissance-r8) | EOY residual, floored |
| `parts` | Number of *parts de provision de diversification* [R2 R. 134-2](#frlib-eurocroissance-r2) | BOY levy; on *versements* and exits |
| `part_value` | *Valeur de la part*, `pd / parts`; common to the whole auxiliary account [R2 R. 134-2](#frlib-eurocroissance-r2) | EOY |
| `insurer_contribution` | Outstanding L. 134-3 asset contribution completing the representation (Chassis A) | EOY |
| `pgt` | *Provision pour garantie à terme*, insurer's own funds (Chassis B) [R3 A. 134-2](#frlib-eurocroissance-r3) | EOY |
| `pcdd` | *Provision collective de diversification différée*, fund-level [R8 R. 343-3 10°](#frlib-eurocroissance-r8) [R9] | EOY, fund extension |
| `pols_if` | In-force probability at the **start** of year `t`; `pols_if(0) = 1`. The end-of-year count `l(t)` is `pols_if_at(t, "AFT_DECR")` | EOY decrements |
| `cum_prem_net` | Cumulative net *versements*, the base of the death floor [S1] [S2] | on each *versement* |

---

## Assumption inputs

Three classes are distinguished. Class (a) is contractual or statutory; class (b) is the
insurer's current discretionary scale, exercised inside the R. 134-4 destinations [R2];
class (c) is the modeler's view of experience.

### (a) Contractual / guaranteed elements (cited)

| Input | Value | Basis |
|---|---|---|
| Guarantee level `g` / maturity `n` | 100 % of net *versements* / 10 years | [S1] [S2]; 80 % and 8–30 [S8]; 80 %–100 % and 8–40 [S7] |
| Guarantee run-down for exits | `mg` reduced pro rata to surrenders and deaths | [R13] |
| PM definition (Chassis A) | `pm(t) = mg(t) × (1 + i_pm(t))^-(n-t)` | [R2 R. 134-2](#frlib-eurocroissance-r2) |
| PM discount rate `i_pm` | ≤ **90 % of the last TEC*n***, linear interpolation between bracketing maturities, longest TEC beyond the curve, **floor 0 %**, method choice irreversible per account. As retrieved, A. 134-1 fixes *n* as the holder's **guarantee maturity** (per-engagement method 1°) or the account's 1°-engagement **duration** (method 2°); this model applies method 1° and re-reads *n* as the **remaining** term `n − t` at each valuation date | haircut, interpolation and floor [R3 A. 134-1](#frlib-eurocroissance-r3); the `n − t` re-reading **[std]**, note below |
| Reference TEC10 | 2.50 % to year 5, 1.00 % from year 6 → `i_pm` 2.25 %, then 0.90 % | **[std]**, product-spec (5) |
| Minimum part value | €5.00 — the part value may not be reduced below it to absorb a debit balance | requirement [R2 R. 134-1, R. 134-4](#frlib-eurocroissance-r2); level **[std]**, product-spec (2) |
| Surrender value | Chassis A `pm + parts × part_value`; Chassis B `parts × part_value`; **no guarantee before maturity on Chassis B** | [R2 R. 134-5](#frlib-eurocroissance-r2) |
| Maturity amount | Chassis A `pm + parts × part_value`; Chassis B `max(parts × part_value, mg)` | [R2 R. 134-6](#frlib-eurocroissance-r2) |
| Death benefit | The current provision value; the maturity guarantee does **not** apply. Any death floor is a complementary guarantee provisioned **outside** the account | [R2 — no death article in Chapter IV, R. 134-7](#frlib-eurocroissance-r2) [R13] [S1] [S2] |
| Surrender indemnity | 0 %; statutory cap 5 % of the present value of the mutual engagements, and the contract **may** provide for none once ten years have elapsed | cap and the ten-year **permission** [R10]; level **[std]**, product-spec (3) |
| Permitted charge bases | The six of R. 134-3 only; base 3° unavailable in a 1° account | [R2 R. 134-3](#frlib-eurocroissance-r2) |
| PGT (Chassis B) | `max( PV(guarantees) − pd − pcdd, 0 )`, A. 132-18 tables, rate ≤ 90 % of TEC, no cash flows other than guarantee maturities and mortality. The shipped per-policy `pgt` omits the **survival factor** on the guarantee maturity **[std]** — see "The PGT's mortality driver" below | article [R3 A. 134-2](#frlib-eurocroissance-r3) [R10]; the omission **[std]** |
| PCDD release horizon / apport d'actifs | 15 years / ≤ 10 % of the PD at the affectation date, endowing the PCDD, re-allocated by year 16 | [R9 A. 132-16](#frlib-eurocroissance-r9); [R7 R. 134-12](#frlib-eurocroissance-r7) |
| Assets at realisation value | R. 343-11 / R. 343-12 | [R2 R. 134-8](#frlib-eurocroissance-r2) |

**The `n − t` re-reading of A. 134-1 — [std].** The article as retrieved gives the index
maturity as the holder's guarantee maturity (method 1°) or the auxiliary account's
1°-engagement duration (method 2°), and says nothing about how that maturity is re-read at
valuation dates after inception [R3 A. 134-1](#frlib-eurocroissance-r3). Two readings are
available: hold *n* fixed at the original term for the life of the engagement, or take the
**remaining** term `n − t`, which is the horizon the guarantee is actually discounted over.
These notes and `EC_FR_A` take the second — the first would discount a one-year promise at a
ten-year constant-maturity rate on the *échéance* row, and A. 134-1's own method 2° keys the
index to a **duration**, which shortens as the engagements run off. The reading is
**[std]**; it is not stated in the article. `product-spec.md` states A. 134-1 as retrieved,
and **these notes are the source of truth for the value `i_pm` takes in the model.** The
choice is numerically invisible on a flat curve — the worked example's TEC is flat, so both
readings give `i_pm` = 2.25 % then 0.90 % — and live on a sloped one, which is why shipped
model point 10 runs the `sloped` scenario.

### (b) Insurer-discretionary current elements

| Input | Value | Basis |
|---|---|---|
| Entry charge (base 1°) | 2.00 % of each *versement* | [R13]; 4.50 % max [S8]; **[std]**, product-spec (7) |
| Parts levy (base 4°) | 0.80 % p.a. of parts, at BOY on the opening part value | [R13]; routing **[std]**, product-spec (8) |
| Performance levy (base 5°) | 10 % of positive financial-management performance; 0 % of negative | [R13]; **[std]**, product-spec (9) |
| Exit charge (base 6°) / conversion charge (base 2°) | 0.00 % / 0.50 % of amounts converted (Chassis A) | **[std]**, product-spec (9); [S8] |
| Credit-balance allocation | Raise the **part value**; no new parts awarded | **[std]**, product-spec (10) |
| PCDD piloting target | Insurer's own euro-fund net rate **+0.30 %**; everything above it to the PCDD | [R13]; **[std]** in the base run (`pcdd = 0`) |
| Apport d'actifs level | 10 % of net premiums for the first three years | [R13]; **[std]** in the base run (0) |
| Credited-return context | 2025 net returns 0.90 %–3.40 % across seven supports; AXA Fonds Croissance 2.50 %–4.50 %, average 3.13 % | [S9] [S3] [S8] |
| Commercial bonus uplift | +2.00 % on new money in the promotion year, subject to a ≥ 45 % unit-linked condition. **Not an input to `EC_FR_A`**, and not held at zero by a switch: there is no uplift Reference, no cells and no model-point column, because a commercial promotion is a marketing device rather than a term of the statutory mechanics these notes specify. Recorded here as market context only | [S3] [S4]; out of scope **[std]** |

### (c) Behavioral / experience assumptions (modeler's view)

The regulatory tables the code points to — TH 00-02 / TF 00-02 for non-annuity contracts
[REG-R22], TGH05 / TGF05 for annuities [REG-R21], applied under art. A. 335-1 with the
annexed *décalages d'âge* [REG-R23] — are **cited by name and never shipped**; A. 132-18 also
permits an insurer's own table certified by an independent approved actuary [R10], so no
single market basis exists. The reference decrement table is a **[std]** proxy built from the
freely redistributable INSEE series [REG-R24].

| Input | Recommended basis | Basis tags |
|---|---|---|
| Base mortality | 80 % × a **[std]** smooth Makeham curve *shaped like* the INSEE *quotients de mortalité* [REG-R24] and anchored so that the 80 % factor gives exactly **0.5000 %** at male 57, the worked example's entry age; sex-distinct, age last birthday; no improvement in the base run. It is **not** the INSEE series itself — `mort_table.csv` carries the same statement in its own provenance column | proxy **[std]**; shape from [REG-R24]; tables cited and never shipped [REG-R22] [REG-R23] |
| Full surrender (*rachat total*) | 2.5 % p.a., level | [R13] observes 2 %–3 % p.a.; level **[std]** |
| Partial surrender (*rachat partiel*) | 6 % of average encours in years 1–2, then 3 %; dynamic multipliers per Policyholder behavior modeling | [R13] observes 6 % then 2 %–4 %; **[std]** |
| Asset return `r(t)` | 4.0 % p.a. base; the worked example uses an explicit shock path | scenario **[std]** |
| Asset management fees | 0.20 % equities, 0.10 % bonds, deducted from the asset return | [R13] |
| Insurer expenses | Acquisition 5 % of premiums; maintenance 0.20 % p.a. of `pm + pd`; acquisition commission 2 % of the initial premium | [R13] |
| Worked-example decrements | `mort_rate = 0`, `lapse_rate = 0`, so `pols_if(t) = 1` | **[std]** — isolates the provision mechanics |

Deterministic single-scenario projection is the base. The maturity guarantee is a put option
on the auxiliary account and its cost requires stochastic market-consistent valuation; the
*mémoire* runs 1 000 risk-neutral scenarios for exactly this reason [R13].

---

## Cash flow components and recursions

### Notation (defined once, used throughout)

| Symbol | Meaning |
|---|---|
| `t`, `x`, `n`, `g` | policy year index (0…`n`); `issue_age`; guarantee maturity in years; guarantee level |
| `P(t)`, `P_net(t)` | gross and net *versement* at time `t`; `P_net = P × (1 − f_e)` |
| `f_e`, `f_p`, `f_perf`, `f_x` | entry 2.00 %, parts levy 0.80 % p.a., performance levy 10 %, exit 0.00 % |
| `mg(t)` | guaranteed amount payable at `n` |
| `i_pm(t)` | PM discount rate = 90 % × TEC(`n−t`), floored at 0 %. The haircut, the interpolation and the floor are [R3 A. 134-1](#frlib-eurocroissance-r3); reading the index maturity as the **remaining** term is **[std]**, see (a) above |
| `A(t)` | `own_assets(t)`, account assets attributable to the policy, excluding any outstanding insurer contribution |
| `pm(t)`, `pd(t)` | *provision mathématique*, *provision de diversification* |
| `N(t)`, `u(t)`, `u_min` | `parts(t)`; `part_value(t)` = `pd(t) / N(t)`; minimum part value €5.00 **[std]** |
| `r(t)` | gross asset return in year `t`, net of asset management fees |
| `L(t)`, `F(t)` | parts levy (BOY) and performance levy (EOY) in year `t` |
| `C(t)`, `G(t)`, `D(t)` | `insurer_contribution(t)` (L. 134-3); `pgt(t)` (Chassis B); `pcdd(t)` (fund-level) |
| `q(x+t)`, `w(t)`, `l(t)` | `mort_rate`, `lapse_rate`, and the **end**-of-year in-force count — `pols_if_at(t, "AFT_DECR")` in the model; `l(0) = 1`. The model's `pols_if(t)` is the **start**-of-year count `l(t−1)`, the weight on year `t`'s flows |

### The guaranteed amount

`mg(0) = g × P_net(0)` and `mg(t) = mg(t−1) + g × P_net(t) − exits(t)`, where `exits(t)` runs
the guarantee down pro rata to surrenders and deaths [R13]. In a single-policy expected-value
projection with no partial surrender, `mg(t)` is constant between *versements*.

### Provision mathématique and the split of a *versement* (Chassis A)

`pm` is **re-struck** every year, never accumulated [R2 R. 134-2](#frlib-eurocroissance-r2):

```
pm(t) = mg(t) × (1 + i_pm(t))^-(n-t)        (Chassis A)
pm(t) = 0                                    (Chassis B)
```

A *versement* `P_net(t)` paid at the end of year `t`, immediately after the striking, splits
as follows and buys parts at the part value just struck:

```
pm_added = g × P_net(t) × (1 + i_pm(t))^-(n-t)   pd_added = P_net(t) − pm_added
parts_added = pd_added / u(t)
```

At `t = n` the discount factor is 1, so `pm(n) = mg(n)` identically: the *provision
mathématique* accumulated at the regulated rate reaches the guarantee exactly at the
*échéance*, which is what makes the Chassis A guarantee pre-funded by construction.

### Account assets, charges and the annual rebalancing

```
L(t)   = f_p × pd(t−1)          (BOY, base 4°)   A_a(t) = A(t−1) − L(t)
I(t)   = A_a(t) × r(t)                           F(t)   = f_perf × max( I(t), 0 )  (EOY, base 5°)
A(t)   = A_a(t) + I(t) − F(t)   (before any versement)
N(t)   = N(t−1) × (1 − f_p)
```

The two provisions are then re-struck, the diversification provision taking the residual and
stopping at its contractual floor [R2 R. 134-4](#frlib-eurocroissance-r2):

```
pd(t) = max( A(t) − pm(t), N(t) × u_min )   u(t) = pd(t) / N(t)
C(t)  = max( pm(t) + pd(t) − A(t), 0 )
G(t)  = max( mg(t) × (1 + i_pm(t))^-(n-t) − pd(t) − D(t), 0 )   (Chassis B) [R3 A. 134-2]
```

`C(t)` is the outstanding contribution the insurer must make to complete the representation
[R1 L. 134-3](#frlib-eurocroissance-r1); it carries no return to the savers and is repaid in full as soon as `A(t)`
covers `pm(t) + N(t) × u_min` **[std]**, product-spec (6). The **surrender value**
`pm(t) + pd(t)` therefore exceeds `A(t)` by exactly `C(t)` while the contribution is
outstanding. On Chassis B, `pm ≡ 0`, so `pd(t) = max(A(t), N(t) × u_min)` and the shortfall
against the guarantee appears instead as the PGT `G(t)`, which is on the **insurer's** balance
sheet, outside the participation account, and is not part of any benefit.

**The PGT's mortality driver is switched off — [std].** A. 134-2 admits exactly two
cash-flow drivers into the present value of the 2° guarantees: guarantee maturities and
mortality [R3 A. 134-2](#frlib-eurocroissance-r3). `G(t)` above, and `pgt()` in the model,
discount the guaranteed amount to `t` and apply **no survival factor**, so the present value
is the amount for a guarantee certain to be reached. The simplification is prudent — it
overstates the provision — and it is invisible on the worked example, where `mort_rate = 0`;
it is live on every decrement-bearing cell. On shipped model point 6 at `t` = 7 the reported
`pgt` is **2,739.35**, against **2,477.36** with the five-year survival factor **0.972660**
that the shipped **[std]** table gives. A fund-level implementation of A. 134-2 should carry
`PV(t) = Σ_i mg_i(t) × (1 + i_pm(t))^-(n_i − t) × (n_i − t)p_(x_i+t)` over the account's 2°
engagements; in this single-policy model the mortality decrement reaches the projection
through `pols_if` in `result_cf()` instead of through the provision.

### Exit and maturity values

```
surrender_value(t) = ( pm(t) + N(t) × u(t) ) × (1 − f_x)   A ;  ( N(t) × u(t) ) × (1 − f_x)   B
maturity_value(n)  = pm(n) + N(n) × u(n)                   A ;  max( N(n) × u(n), mg(n) )     B
death_value(t)     = pm(t) + N(t) × u(t)                   A ;  N(t) × u(t)                   B
death_payout(t)    = max( death_value(t), cum_prem_net(t) )      if death_floor_flag [S1] [S2]
rider_claim(t)     = death_payout(t) − death_value(t)            outside the account [R2 R. 134-7]
```

Surrender and maturity forms are R. 134-5 and R. 134-6 verbatim [R2]; the death forms follow
from Chapter IV containing no death valuation article [R2] [R13]. A surrender is priced on a
**forward** part value in reality — the next striking or the next monthly intermediate value
[R3 A. 134-5](#frlib-eurocroissance-r3); on an annual grid it is priced on the year-end striking, a recorded
simplification.

### Fund-level items (extension, held at zero in the base run)

```
D_open(t)     = D(t−1) + apport(t)                                (PCDD at start of year)
target_use(t) = ( euro_fund_rate(t) + 0.30 % ) × ( pm(t−1) + pd(t−1) ) − Δpm_rate(t)
D_target(t)   = D_open(t) + balance(t) − target_use(t)
D(t)          = max( min( D_open(t), D_target(t) ), 0 )
dotation(t)   = D(t) − D_open(t)
apport(t)     ≤ 0.10 × pd(t)   → credited to D_open(t), never to pd(t)     [R7 R. 134-12]
```

The piloting rule is the *mémoire*'s: run the fund at 30 bp above the insurer's own euro fund
and put everything else in the PCDD [R13]. Note that the first argument of the `min` is the
PCDD at the **start** of the year — last year's close plus the year's *transfert de richesse*
— and not the start-of-year figure plus the participation balance: the `min` is a **cap**
that holds the reserve at its opening level whenever the balance exceeds the target use, and
a version that added the balance inside both arguments would degenerate to
`D_open(t) + balance(t) − max(target_use(t), 0)` and let the PCDD grow without limit [R13].

The PCDD must be used within **fifteen years**
[R9]; the apport must be re-allocated out **no later than the sixteenth year** following
affectation, capped on the way out by the lowest of the affectation-date value plus its share
of net investment income plus the base-5° levies, 10 % of total PD, and total PCDD [R7 II](#frlib-eurocroissance-r7).
**The term "bonus de mutualisation" appears in no retrieved document**; the code calls this
*apport d'actifs* [R7], practitioners *transfert de richesse* [R13] [R21].

### Annual processing order [std]

The order is not free: R. 134-4 and R. 134-12 III both say that asset affectations and
re-affectations completing the account's representation are made **on the dates the
participation account is struck, after its balance has been allocated** [R2] [R7].

1. **BOY** — parts levy `L(t) = f_p × pd(t−1)`; `N(t) = N(t−1) × (1 − f_p)`; assets reduced
   by `L(t)` (base R. 134-3 4°).
2. **BOY** — scheduled *versements* received net of the entry charge (base 1°) and split per
   the *versement* rule; partial surrenders paid (base 6°) and `mg` run down pro rata.
3. Asset return `r(t)` accrues on the balance after steps 1–2.
4. **EOY** — performance levy `F(t) = f_perf × max(I(t), 0)` (base 5°).
5. **EOY** — strike the participation account and allocate its balance: raise `u` (the
   reference route), award new parts, revalue the guarantees subject to the two A. 134-3
   tests, or endow the PCDD [R2 R. 134-4](#frlib-eurocroissance-r2).
6. **EOY** — re-strike `pm(t)` from `mg(t)` and the current `i_pm(t)`; `pd(t)` = residual,
   floored at `N(t) × u_min`; `u(t) = pd(t) / N(t)`.
7. **EOY** — asset affectations: `C(t)` (Chassis A) or `G(t)` (Chassis B), **after** step 5.
8. **EOY** — free *versements* paid at year end (the worked example's year-3 top-up) split at
   the just-struck `i_pm(t)` and `u(t)`.
9. **EOY** — claims: deaths at `q`, surrenders at `w`, maturity at `t = n`;
   `l(t) = l(t−1) × (1 − q(x+t)) × (1 − w(t))`, survivors maturing at `n`.

### Known modeling pitfalls

These are the specific ways an implementation of **this** product can look right and be
wrong. Each should become a test.

1. **Treating the Chassis B surrender value as guaranteed.** The single most important
   product fact. Before the maturity a 2° engagement pays `parts × part value` and **nothing
   else** [R2 R. 134-5](#frlib-eurocroissance-r2); a model that floors the surrender value at `g ×` premiums, or at the
   discounted guarantee, is modelling a contract that does not exist. Test: on the worked
   example's year-6 shock, Chassis B must surrender for **9,899.22**, i.e. **84.18 %** of net
   *versements*, not 11,760.00.
2. **Letting the PGT reach a policyholder.** The PGT is the insurer's own-funds provision,
   outside the participation account [R3 A. 134-2](#frlib-eurocroissance-r3) [R13]. A model that adds `pgt` to a
   benefit, or lets it feed the profit-sharing computation, is wrong. Test: `pgt` appears in
   no benefit column and in no participation balance.
3. **Accumulating the PM instead of re-striking it.** `pm(t)` is `mg(t)` discounted at the
   *current* `i_pm(t)` [R2 R. 134-2](#frlib-eurocroissance-r2). Rolling `pm(t−1)` forward at last year's rate silently
   removes the **rate effect** — +587.44 of the +824.18 year-6 move in the worked example.
4. **Levying an encours charge on the PD in a 1° account.** R. 134-3 3° permits that levy only
   where the auxiliary account holds **no 1° engagements**, and no base permits a levy on the
   PM [R2]. Test: with `engagement_modality = euro_and_parts`, the recurring charge base must
   be the number of parts and the year-1 levy must be **15.64**, not 78.40.
5. **Forgetting that the entry charge cuts the guarantee.** The guarantee is a percentage of
   premiums **net of the R. 134-3 1° charge** [R2 R. 134-2](#frlib-eurocroissance-r2) [R13]. Test: `mg` after the year-3
   top-up is **11,760.00**, not 12,000.00.
6. **Omitting the minimum part value.** A debit balance may reduce the part value only
   **within the limit of its minimum** [R2 R. 134-4](#frlib-eurocroissance-r2). Without the floor, Chassis A's `pd` goes
   negative in year 6 (`A(6) − pm(6) = −1,095.35`). Test: `part_value ≥ 5.0000` in every year
   on both chassis.
7. **Paying the maturity guarantee to a death claim.** Chapter IV has no death valuation
   article; the death benefit is the current provision value [R2] [R13], and a death floor is
   a complementary guarantee provisioned **outside** the account [R2 R. 134-7](#frlib-eurocroissance-r2). Test: the
   year-6 Chassis B death payout with the rider is 11,760.00, of which **1,860.78** is a rider
   claim reported outside the auxiliary-account columns.
8. **Applying the maturity `max(·, mg)` before the maturity, or at all on Chassis A.** The
   `max` exists only at `t = n` and only on Chassis B [R2 R. 134-6](#frlib-eurocroissance-r2). On Chassis A the maturity
   amount is `pm(n) + parts × part value`, **more** than `mg` whenever the parts retain any
   value — 12,765.89 against a guarantee of 11,760.00 here.
9. **Crediting the insurer's contribution to the savers.** `C(t)` completes the representation
   and is releasable when representation permits [R1 L. 134-3](#frlib-eurocroissance-r1); the reference treatment gives
   it no return to the savers **[std]**. A model that rolls the topped-up balance forward as
   savers' assets manufactures return out of the insurer's capital.
10. **Giving per-policy returns inside one auxiliary account.** The part value is **common to
    all engagements of the account** [R2 R. 134-2](#frlib-eurocroissance-r2), so savers with different maturities and
    guarantee levels in one account earn the same rate; differentiation is possible only
    through the number of parts or through differentiated PCDD distribution [R2 R. 134-4](#frlib-eurocroissance-r2)
    [R13]. Test: two model points in the same account share one `part_value` path.
11. **Ignoring the A. 134-3 and A. 134-4 gates.** Revaluing the guarantees out of the
    participation account requires **both** A. 134-3 tests to pass; converting parts into PM
    requires the A. 134-4 15 %-of-PM headroom and a five-year cooling period [R3]. Test: at
    `t = 5` both A. 134-3 tests pass; at `t = 6` the second fails (`pd − N × u_min = 0.00`
    against `10 % × pm = 1,134.60`).
12. **Using the wrong discount article, or a same-day part value.** The PM rate is A. 134-1's
    90 %-of-TEC ceiling with a zero floor [R3] — read here at the remaining maturity, which
    is **[std]** and not the article — not the A. 132-1 maximum technical rate
    [REG-R17] and not the A. 132-3 TMG ceiling [REG-R18]; and the part value used for an exit
    is a **forward** value [R3 A. 134-5](#frlib-eurocroissance-r3), so a monthly variant must not price a surrender on a
    part value struck before the request.

### Cash flow outputs (per policy year `t`, probability-weighted by `pols_if`)

`pols_if(t)` below is the **start**-of-year in-force count — the notes' `l(t−1)` — and is the
exposure every flow on that same `result_cf()` row is weighted by. The end-of-year count `l(t)`
is `pols_if_at(t, "AFT_DECR")` in the model; it weights the maintenance expense and nothing else.

| Output | Formula |
|---|---|
| `premiums` | `P(t) × pols_if(t)` |
| `claims_death` | `mort_rate(t) × pols_if(t) × death_payout(t)` |
| `claims_lapse` | `lapse_rate(t) × pols_if(t) × (1 − mort_rate(t)) × surrender_value(t)` |
| `claims_maturity` | `pols_if(n) × (1 − mort_rate(n)) × maturity_value(n)` at `t = n` |
| `withdrawals` | partial *rachats* — an owner election, not a claim |
| `expenses` | `pols_if(t) × (`acquisition 5 % of *versements*, plus an acquisition commission of 2 % of the initial *versement* at issue`) + l(t) × `maintenance 0.20 % p.a. of `pm + pd` — all three levels [R13], as in the assumption table above |
| `charges_taken` | `L(t) + F(t) + f_e × P(t) + f_x ×` benefits — insurer income, reported separately |
| `insurer_contribution` / `pgt` | own-funds items, reported separately, **never** in a claim column |

`liability_cf` prints outgo-positive; `net_cf(t) = −liability_cf(t)` is income-positive, and
`result_cf()` is indexed by `t` with `pols_if` first. Because `pols_if` is the start-of-year
count, `result_cf()["pols_if"].iloc[0]` equals `pols_if_init()` on every model point, and
dividing any flow on a row by that row's `pols_if` recovers the per-policy amount.

---

## Policyholder behavior modeling

All dynamic formulas are **[std]** — no eurocroissance lapse experience is public, and the
product is too small and too young to have any [R14] [R21]. The shapes are rationalized from
the incentive structure the code creates.

- **Base full surrender** 2.5 % p.a. [R13 observes 2 %–3 %](#frlib-eurocroissance-r13); **partial surrender** 6 % of
  average encours in years 1–2 then 3 % [R13 observes 6 % then 2 %–4 %](#frlib-eurocroissance-r13).
- **Guarantee-imminent suppression (Chassis B).** `w(t) = w_base(t) × 0.5` in the two years
  before the *échéance* whenever the guarantee is in the money, `N(t) × u(t) < mg(t)`
  **[std]**. A saver who surrenders in that state gives up the entire guarantee [R2 R. 134-5](#frlib-eurocroissance-r2)
  — the strongest exit deterrent in the product.
- **Maturity.** 100 % of survivors take the maturity amount in the base run **[std]**, as the
  *mémoire* also assumes; it notes that modelling annuitisation or reinvestment instead could
  amplify or damp its results [R13]. The statutory default is in fact an arbitrage into an
  SRI ≤ 2 support unless the holder decides otherwise [R2 R. 134-6](#frlib-eurocroissance-r2) [R3 A. 134-6](#frlib-eurocroissance-r3), so a "roll
  into a low-risk support" variant is the natural extension.
- **Duration-8 tax spike.** The assurance-vie annual abattement (€4 600 / €9 200) becomes
  available at eight years [REG-R40], so `w(8) = w_base(8) × 1.5` **[std]** where `n > 8`.
- **Lock-up.** Where `lock_up_years > 0`, `w(t) = 0` for `t ≤ lock_up_years`, except for the
  L. 132-23 hardship exits, which are not separately modeled **[std]** [R1] [R2 R. 134-5](#frlib-eurocroissance-r2). The
  thirty-day *renonciation* right [REG-R29] belongs in a monthly variant.
- **No surrender-penalty deterrent** is modeled, because the reference indemnity is zero
  [S2] [S8]; the *mémoire*'s point that the loss of the PCDD share is itself the penalty [R13]
  bites only where the PCDD extension is switched on. Any mass-surrender stress must respect
  the HCSF power to limit surrender payments for up to six consecutive months [REG-R13].

---

## Worked example

**Configuration.** One model point per chassis, same asset path, two separate auxiliary
accounts. Gross initial *versement* **€10 000.00** at `t = 0` and a free additional *versement*
of **€2 000.00** at the end of policy year 3 [R13]; entry charge **2.00 %** [R13], so net
*versements* are 9 800.00 and 1 960.00 and cumulative net *versements* are **11 760.00**;
guarantee level `g` = **100 %** of net *versements* at a maturity `n` = **10 years**
[S1] [S2]; initial part value **€10.0000** [R13]; minimum part value **€5.0000** **[std]**;
parts levy **0.80 % p.a.** and performance levy **10 % of positive financial performance**
[R13]; exit charge and surrender indemnity **0 %** [S2] [S8]; male age 57 [R13].
`mort_rate = 0` and `lapse_rate = 0` throughout, so `pols_if(t) = 1` and the per-policy
provision path is the cash-flow path **[std]**. Gross asset return `r(t)` = 4.00 % for
`t` = 1–5, **−25.00 %** in `t` = 6, 6.00 % for `t` = 7–10; TEC10 = 2.50 % to `t` = 5 and
**1.00 %** from `t` = 6 at every maturity, so the A. 134-1 discount rate `i_pm` = 90 % × TEC = **2.25 %** then
**0.90 %** [R3] **[std]**. The year-6 double shock — equities down and rates down together —
is what makes the rebalancing visible.

### Chassis A (1° engagement: euros and parts)

`L(t) = 0.80 % × pd(t−1)`; `A(t) = (A(t−1) − L(t)) × (1 + r(t)) − 10 % × max((A(t−1) − L(t)) × r(t), 0)`;
`pm(t) = mg(t) × (1 + i_pm(t))^-(10-t)`; `pd(t) = max(A(t) − pm(t), parts(t) × 5.00)`.

| t | r(t) | parts levy | own assets `A` | `pm` | `pd` | parts | part value | insurer contrib. | surrender value |
|---|---|---|---|---|---|---|---|---|---|
| 0 | — | 0.00 | 9,800.00 | 7,845.00 | 1,955.00 | 195.5001 | 10.0000 | 0.00 | 9,800.00 |
| 1 | 4.00 % | 15.64 | 10,136.60 | 8,021.51 | 2,115.09 | 193.9361 | 10.9061 | 0.00 | 10,136.60 |
| 2 | 4.00 % | 16.92 | 10,483.98 | 8,202.00 | 2,281.99 | 192.3846 | 11.8616 | 0.00 | 10,483.98 |
| 3 | 4.00 % | 18.26 | 12,802.49 | 10,063.85 | 2,738.65 | 212.8127 | 12.8688 | 0.00 | 12,802.49 |
| 4 | 4.00 % | 21.91 | 13,240.69 | 10,290.29 | 2,950.40 | 211.1102 | 13.9756 | 0.00 | 13,240.69 |
| 5 | 4.00 % | 23.60 | 13,692.90 | 10,521.82 | 3,171.08 | 209.4213 | 15.1421 | 0.00 | 13,692.90 |
| 6 | −25.00 % | 25.37 | 10,250.65 | 11,346.00 | 1,038.73 | 207.7460 | **5.0000** | 2,134.08 | 12,384.73 |
| 7 | 6.00 % | 8.31 | 10,795.42 | 11,448.11 | 1,030.42 | 206.0840 | 5.0000 | 1,683.11 | 12,478.53 |
| 8 | 6.00 % | 8.24 | 11,369.69 | 11,551.14 | 1,022.18 | 204.4353 | 5.0000 | 1,203.63 | 12,573.32 |
| 9 | 6.00 % | 8.18 | 11,975.03 | 11,655.10 | 1,014.00 | 202.7998 | 5.0000 | 694.07 | 12,669.10 |
| 10 | 6.00 % | 8.11 | 12,613.13 | **11,760.00** | 1,005.89 | 201.1774 | 5.0000 | 152.75 | **12,765.89** |

The `t` = 3 row is stated **after** the year-end *versement*. Immediately before it,
`A = 10,842.49`, `pm = 8,386.54`, `pd = 2,455.95`, `parts = 190.8455`, `u = 12.8688`; the
*versement* then splits as `pm_added = 1 960.00 × 1.0225^-7 = 1,677.31`, `pd_added = 282.69`
and `parts_added = 282.69 / 12.8688 = 21.9672`, and `mg` rises from 9,800.00 to **11,760.00**.
Performance levies are 39.14, 40.48, 41.86, 51.12, 52.87, 0.00, 61.45, 64.72, 68.17, 71.80 for
`t` = 1–10.

### Chassis B (2° engagement: parts only, guarantee at maturity)

`pm ≡ 0`, so `pd(t) = max(A(t), parts(t) × 5.00)` and the shortfall shows as the PGT.

| t | parts levy | `pd` = own assets | parts | part value | `pgt` (own funds) |
|---|---|---|---|---|---|
| 0 | 0.00 | 9,800.00 | 980.0000 | 10.0000 | 0.00 |
| 1 | 78.40 | 10,071.58 | 972.1600 | 10.3600 | 0.00 |
| 2 | 80.57 | 10,350.68 | 964.3827 | 10.7330 | 0.00 |
| 3 | 82.81 | 12,597.52 | 1,132.9370 | 11.1193 | 0.00 |
| 4 | 100.78 | 12,946.62 | 1,123.8735 | 11.5196 | 0.00 |
| 5 | 103.57 | 13,305.40 | 1,114.8825 | 11.9344 | 0.00 |
| 6 | 106.44 | **9,899.22** | 1,105.9635 | **8.9508** | **1,446.78** |
| 7 | 79.19 | 10,350.30 | 1,097.1158 | 9.4341 | 1,097.81 |
| 8 | 82.80 | 10,821.95 | 1,088.3388 | 9.9435 | 729.20 |
| 9 | 86.58 | 11,315.08 | 1,079.6321 | 10.4805 | 340.02 |
| 10 | 90.52 | **11,830.69** | 1,070.9951 | 11.0464 | 0.00 |

Again the `t` = 3 row is post-*versement*: immediately before it `pd = 10,637.52`,
`parts = 956.6677` and `u = 11.1193`, and the whole net 1 960.00 buys
`1 960.00 / 11.1193 = 176.2694` parts. Performance levies are 38.89, 39.96, 41.07, 49.99,
51.37, 0.00, 58.92, 61.61, 64.41, 67.35 for `t` = 1–10.

### Exit values, and what the two chassis pay

| Event | Chassis A | Chassis B |
|---|---|---|
| Surrender at `t` = 6 | 12,384.73 (**105.31 %** of net *versements*) | 9,899.22 (**84.18 %**) |
| Death at `t` = 6, no rider | 12,384.73 | 9,899.22 |
| Death at `t` = 6 with the *garantie décès plancher* | 12,384.73 (rider claim 0.00) | 11,760.00 (rider claim **1,860.78**, outside the account) |
| Maturity at `t` = 10 | 12,765.89 = 11,760.00 + 1,005.89 | 11,830.69 = `max(11,830.69, 11,760.00)` |
| Guarantee binding at maturity? | yes, by construction (`pm(10) = mg`) | no — the account recovered to 0.60 % above `mg` |
| Insurer's own-funds cost, peak | contribution **2,134.08** at `t` = 6 | PGT **1,446.78** at `t` = 6 |
| Social-levy base at maturity [R11] | 12,765.89 − 12,000.00 = **765.89** | 11,830.69 − 12,000.00 < 0, i.e. **nil** |

The social-levy base is the surrender value at the moment the guarantee is reached less the
premiums allocated to those engagements [R11 CSS L. 136-7 II 3° b)](#frlib-eurocroissance-r11); whether "primes versées"
means gross or net of the entry charge was not resolved from the retrieved text, so the table
uses **gross** premiums (12,000.00) and the alternative net figures are 1,005.89 and 70.69
respectively — **[unverified]**.

**Checks.** *(i)* The PM unwinds exactly onto the guarantee: `pm(10) = 11,760.00 × 1.009^0 =
11,760.00 = mg(10)`, and the Chassis A maturity payout is that plus the parts at their floor,
`201.1774 × 5.0000 = 1,005.89`, giving 12,765.89 — reproduced independently of the asset
path. *(ii)* The year-6 PM move decomposes cleanly into its two drivers: at the unchanged
2.25 % rate `pm(6)` would have been `11,760.00 × 1.0225^-4 = 10,758.56`, a **time effect of
+236.74** on `pm(5) = 10,521.82`; re-striking at 0.90 % gives `11,760.00 × 1.009^-4 =
11,346.00`, a **rate effect of +587.44**; the two sum to +824.18, which is exactly
`11,346.00 − 10,521.82`. *(iii)* The year-6 asset roll is `A(6) = (13,692.90 − 25.37) ×
(1 − 0.25) = 10,250.65` with no performance levy, because the financial performance was
negative; `pd(6)` would have been `10,250.65 − 11,346.00 = −1,095.35` without the floor, so
the floor binds at `207.7460 × 5.0000 = 1,038.73` and the insurer's contribution is
`11,346.00 + 1,038.73 − 10,250.65 = 2,134.08`. *(iv)* The parts count closes:
`212.8127 × 0.992^7 = 201.1774` on Chassis A and `1,132.9370 × 0.992^7 = 1,070.9951` on
Chassis B. *(v)* The A. 134-3 gates behave as expected: at `t` = 5, `pd = 3,171.08 >
1.5 × (11,760.00 − 10,521.82) = 1,857.27` and `pd − N × u_min = 2,123.98 > 10 % × pm =
1,052.18`, so revaluing the guarantees is permitted; at `t` = 6 the second test fails,
`0.00 ≤ 1,134.60`. *(vi)* The A. 134-4 conversion headroom at `t` = 5 is the `C` solving
`pd − C − N × u_min = 15 % × (pm + C)`, i.e. **474.52**, on which the 0.50 % *frais de
conversion* [S8] would be 2.37.

**Two sensitivities worth stating in numbers.** At `g` = 80 % — Generali's published level
[S8] — the same path leaves `pm(6) = 9,076.80` and cuts the year-6 Chassis A contribution
from 2,134.08 to **829.17**, a 61 % reduction in the insurer's own-funds cost, which is why
the guarantee level and not the charge scale is the product's real dial. And on Chassis B, an
*apport d'actifs* of the statutory maximum **10 % of the PD** at `t` = 6 — 989.92, credited to
the PCDD, not to the savers' PD [R7 R. 134-12](#frlib-eurocroissance-r7) — would reduce the PGT from 1,446.78 to
**456.86** without changing any policyholder value by one cent.

---

## Valuation and reserve pointers

This library projects gross best-estimate liability cash flows; valuation layers are cited,
not reproduced.

- **French statutory balance sheet.** Inside the auxiliary account only R. 343-3 items 1°, 4°,
  7°, 9°, 10° and 11° are admitted [R2 R. 134-9](#frlib-eurocroissance-r2) [R8] [REG-R6]. Assets are at realisation value
  [R2 R. 134-8](#frlib-eurocroissance-r2), so the *provision pour risque d'exigibilité* [REG-R7] and the *réserve de
  capitalisation* have no role inside it, and the technical result is volatile by construction
  [R13]. The PGT is computed **per auxiliary account**, on the A. 132-18 tables [R10] at a rate
  at most 90 % of the TEC at the account's 2°-engagement duration, counting **no cash flows
  other than guarantee maturities and mortality** [R3 A. 134-2](#frlib-eurocroissance-r3) — a deliberately narrow basis a
  model must not "improve" by adding lapses or expenses. The shipped per-policy `pgt` narrows
  it further, omitting the survival factor on the second of those two drivers **[std]**; see
  "The PGT's mortality driver is switched off" above.
- **Solvabilité II.** Technical provisions are best estimate plus risk margin [REG-R1]
  [REG-R2], discounted on the EIOPA risk-free term structures [REG-R5]; no numeric curve is
  reproduced here and any flat discount rate in this library is **[std]**. Future discretionary
  benefits — the part-value uplift the participation account can deliver — belong in the best
  estimate; the maturity guarantee is an option whose cost needs a stochastic market-consistent
  valuation, which is why the *mémoire* runs 1 000 scenarios [R13]. In the worked example that
  guarantee costs the insurer 2,134.08 (Chassis A) or 1,446.78 (Chassis B) on **one** scenario;
  its cost is convex in the asset shock and in the level of rates, so a deterministic run
  understates it.
- **IFRS 17 and professional standards.** Eurocroissance is an archetypal direct-participating
  contract, so the variable fee approach is the expected measurement model; its mechanics were
  not read from a retrieved text and are [unverified] [REG-R45], and the fulfilment cash flows
  are this same projection. NPA 2, *Modèles actuariels*, is the standard this documentation,
  worked example and test suite sit under [REG-R44].

---

## Key sensitivities and model risks

1. **The guarantee level `g`.** It sets how much of the account is locked into the guaranteed
   leg and therefore how much can bear risk. At `g` = 100 % and `i_pm` = 2.25 %, the PM is
   **80.1 %** of the initial net *versement*; at `g` = 80 % it is 64.0 %. This is the single
   largest dial and the sharpest observed difference across insurers [S1] [S8].
2. **The level of the TEC.** `i_pm` is 90 % of it [R3 A. 134-1](#frlib-eurocroissance-r3), and a 150 bp fall adds
   587.44 to `pm(6)` in the worked example — more than twice the time effect. A model with a
   flat TEC assumption is not modelling this product's dominant risk.
3. **The minimum part value.** Nowhere published for any insurer [R2 R. 134-1](#frlib-eurocroissance-r2); it sets the
   floor of the diversification provision and therefore both the Chassis A maturity payout
   (12,765.89 against a bare guarantee of 11,760.00) and the point at which the insurer must
   start contributing assets. A pure **[std]**.
4. **Asset allocation and the shape of the shock.** The *mémoire* covers the guarantee with
   zero-coupon OATs to the maturity and puts the remainder in equities [R13]; the shape of the
   shock, not just its size, drives the result, because the two provisions respond to
   different risk factors.
5. **The PCDD piloting rule.** Discretionary, unpublished, bounded only by the fifteen-year
   release horizon [R9], and the biggest driver of the credited return [R13]. Held at zero
   here, which understates the smoothing the real product delivers.
6. **Charge structure and its legal base.** The permitted bases differ by chassis
   [R2 R. 134-3](#frlib-eurocroissance-r2), so the same economic charge cannot always be levied the same way; the levels
   are **[std]** because no statutory ceiling on any French life charge appears in the
   retrieved texts [REG-R30].
7. **Unanchored decrements.** No eurocroissance lapse experience is public, so the
   guarantee-imminent suppression and the duration-8 spike are **[std]** shapes; the mortality
   table is an INSEE-based **[std]** proxy [REG-R24], the regulatory tables being cited but
   never shipped [REG-R21] [REG-R22] [REG-R23] and A. 132-18 permitting certified insurer
   tables [R10].
8. **Single-policy abstraction, and the annual grid.** The part value, the PCDD, the PGT and
   the *apport d'actifs* are all **account-level** quantities [R2 R. 134-2](#frlib-eurocroissance-r2) [R3 A. 134-2](#frlib-eurocroissance-r3) [R7],
   which a per-policy model can only approximate — and the *mémoire* records that pooling two
   maturity cohorts in one account produces **no** mutualisation benefit [R13]. The code also
   requires an intermediate valuation at least monthly and prices exits on a forward part value
   [R3 A. 134-5](#frlib-eurocroissance-r3), so the annual grid is a documented simplification, not an equivalence.
9. **Data-provenance limits.** No contractual document exists in the source set [S10], the
   end-2025 market size is not published [R16], ACPR excludes the product from its weekly flows
   [R18], and the A. 134-7 return that would settle every parameter goes to the regulator
   unpublished [R3]. A calibration pass against a real *notice d'information* is required
   before any quantitative use.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #frlib-eurocroissance-r1
[R10]: #frlib-eurocroissance-r10
[R11]: #frlib-eurocroissance-r11
[R13]: #frlib-eurocroissance-r13
[R14]: #frlib-eurocroissance-r14
[R16]: #frlib-eurocroissance-r16
[R18]: #frlib-eurocroissance-r18
[R2]: #frlib-eurocroissance-r2
[R21]: #frlib-eurocroissance-r21
[R3]: #frlib-eurocroissance-r3
[R7]: #frlib-eurocroissance-r7
[R8]: #frlib-eurocroissance-r8
[R9]: #frlib-eurocroissance-r9
[REG-R1]: #frlib-reg-r1
[REG-R13]: #frlib-reg-r13
[REG-R17]: #frlib-reg-r17
[REG-R18]: #frlib-reg-r18
[REG-R2]: #frlib-reg-r2
[REG-R21]: #frlib-reg-r21
[REG-R22]: #frlib-reg-r22
[REG-R23]: #frlib-reg-r23
[REG-R24]: #frlib-reg-r24
[REG-R29]: #frlib-reg-r29
[REG-R30]: #frlib-reg-r30
[REG-R40]: #frlib-reg-r40
[REG-R44]: #frlib-reg-r44
[REG-R45]: #frlib-reg-r45
[REG-R5]: #frlib-reg-r5
[REG-R6]: #frlib-reg-r6
[REG-R7]: #frlib-reg-r7
[std]: #frlib-std
[unverified]: #frlib-unverified
<!-- END generated citation links -->
