# Technical Notes

**Status:** Draft, 2026-08-26 (all cited sources accessed 2026-08-26).

**Scope note.** These notes specify a reference liability cash-flow projection model for
the standardized composite PER individuel assurantiel defined in `product-spec.md` (same
directory). This is not any single insurer's contract. [S#] / [R#] tags refer to the
source list in `sources.md` (numbering carried from `_research/per-assurance.md`);
[REG-R#] tags refer to the cross-product reference library
`references/regulatory-and-actuarial-references.md` (its own frozen R-numbering).
**[std]** marks standardizations introduced for the reference implementation;
[unverified] marks claims not confirmed against a retrieved document. Parameter values
are identical to those in `product-spec.md`. The model is **PER_FR_A**, on an **annual**
grid; the annuity that a liquidating plan buys is projected by `Rente_FR_S` and is
specified in `products/rente_viagere/technical-notes.md`, not here.

---

## Model scope and conventions

- **Purpose.** Project gross best-estimate liability cash flows for single-policy PER
  model points in the **accumulation phase**: *versements* in; death, early-release,
  transfer-out and maturity benefits out; expenses. The account value and its two supports
  are state variables and the glide path drives their split. Reserves are not computed here
  (see *Valuation and reserve pointers*). At `t = proj_len` the account is settled — a
  capital payment, a conversion to a *rente viagère*, or both; the annuity's own cash flows
  belong to `Rente_FR_S`, and this model hands over an amount and records it.
- **Projection frequency.** Annual **[std]**. The governing cycles are annual — euro-fund
  crediting at 31 December [S3] [S7], the annual statement [R5 R. 224-2](#frlib-per_assurance-r5) — and the shortest
  sub-annual mechanic in the sample, quarterly rebalancing [S7], is compressed to one
  rebalancing per year (product-spec footnote 8).
- **Timing conventions [std].** *Versement* and glide-path rebalancing at the start of
  the plan year (BOY); investment return over the year; management charges on the
  end-of-year balance after crediting (the [S3] convention); decrements and benefit
  payments at the end of the year (EOY), in the processing order below.
- **Currency and basis.** EUR; single-policy model points projected on an expected
  basis, `pols_if` multiplying per-policy amounts. Account quantities are per policy
  (`av_pp`, `av_euro_pp`, …) and cash-flow outputs are aggregate — never multiply a claims
  column by `pols_if` twice.
- **Age basis.** Attained age at the valuation date, integer, incremented once per plan
  year **[std]**. No retrieved French document fixes a model age basis; the regulatory
  non-annuity tables are applied with the annexed *décalage d'âge* age shifts [REG-R23],
  which the shipped proxy does not reproduce.
- **Tax is outside the projection.** The deductibility election changes the holder's exit
  taxation, not the insurer's gross benefit [R13] [R19] [R20] [R21]. `deduction_elected`
  is carried and never enters a cash flow.
- **Rounding.** Intermediate values at full precision; reported cash flows to the cent
  **[std]**.

---

## Model point attributes

| Attribute | Type | Example (worked configuration) |
|---|---|---|
| `point_id` | int | 1 |
| `sex` | enum {M, F} | M |
| `age` | int, attained age at t = 0 | 52 |
| `retirement_age` | int, the declared *horizon* [R5 D. 224-3](#frlib-per_assurance-r5) | 64 |
| `duration_ifo` | int, completed years since the first *versement* | 2 |
| `compartment` | enum {c1, c2, c3} [R3 L. 224-2](#frlib-per_assurance-r3) | c1 |
| `allocation_profile` | enum {prudent, equilibre, dynamique, offensif} [R6] | equilibre |
| `premium` | currency p.a., paid BOY to the horizon | 3 000.00 |
| `av_euro_init` | currency, euro support at t = 0 | 0.00 |
| `av_uc_init` | currency, UC bucket at t = 0 | 16 600.00 |
| `death_floor_init` | currency, *garantie plancher* base at t = 0 | 16 000.00 |
| `death_floor_flag` | bool, floor in force to the 70th birthday [S1] [S3] | True |
| `exit_form` | enum {capital_single, capital_staged, annuity, mixed} [R3 L. 224-5](#frlib-per_assurance-r3) | mixed |
| `annuity_share` | float in [0, 1], share of the balance converted to a *rente* | 0.30 |
| `capital_instalments` | int, annual instalments under `capital_staged` | 1 |
| `deduction_elected` | bool — recorded, never used in a cash flow | True |

`compartment` earns its place because it changes two operative rules, not one: **c3**
rights may be delivered **only** as a life annuity [R3 L. 224-5](#frlib-per_assurance-r3) [S2], and they are
**excluded** from the main-residence early-release case [R3 L. 224-4 I 6°](#frlib-per_assurance-r3). A c3 model
point must therefore force `exit_form = annuity` and use a reduced early-release rate.

---

## State variables

| Variable | Description | Updated |
|---|---|---|
| `av_euro_pp(t, timing)` | Per-policy euro-support balance, `timing` ∈ {BOY, EOY} | BOY rebalance, EOY crediting and charge |
| `av_uc_pp(t, timing)` | Per-policy UC balance | same |
| `av_pp(t, timing)` | `av_euro_pp + av_uc_pp` | derived |
| `death_floor_pp(t)` | *Garantie plancher* base: *versements* net of loading, less all charges taken, less benefits paid — the [S1] drafting, **not** the [S3] one, which adds euro-fund interest | annual |
| `alloc_euro(t)` | Target euro (low-risk) share for plan year `t`, from the grid [R6] | BOY, from `years_to_horizon` |
| `switch_pp(t)` | Gross amount switched between supports at the BOY rebalancing | BOY |
| `arbitrage_charge_pp(t)` | `arb_rate × |switch_pp(t)|` [S1] | BOY |
| `years_to_horizon(t)` | `retirement_age − age(t−1)` at the start of plan year `t` | BOY |
| `duration(t)` | `duration_ifo + t`, completed years since the first *versement* | EOY |
| `l(t)` | In-force probability at the **end** of year `t`; `l(0) = 1`. The model publishes it as `pols_if_at(t, "AFT_DECR")` and as the `pols_if_eoy` column of `result_state()` — **not** as `pols_if`, which is the start-of-year count `l(t−1)`; see *The exposure convention* below | EOY decrements |

---

## Assumption inputs

Three classes are distinguished. Class (a) is contractual or statutory; class (b) is the
insurer's current discretionary scale; class (c) is the modeler's view of experience.

### (a) Contractual / guaranteed elements (cited)

| Input | Value | Basis |
|---|---|---|
| Guaranteed technical rate on the euro support | **0,00 %** — the maximum a PER tariff may use | [R9 A. 142-1](#frlib-per_assurance-r9) [S1] [S7] |
| Euro-support capital floor | *Versements* net of loading, less charges levied, less benefits paid; **not** a floor at gross premiums. [S3] drafts the same floor **with** euro-fund interest net of charges added — see the *garantie plancher* recursion below | [S1] [S7] |
| UC guarantee | None; the number of units is guaranteed, not their value | [S1] [S2] |
| Glide-path minimum (équilibré) | euro share 0 % / 20 % / 50 % / 70 % by band; band edges **[std]** (product-spec footnote 7) | [R6 art. 1](#frlib-per_assurance-r6) [S2] [S7] |
| Right to release early | Only on the seven L. 224-4 cases, no surrender right otherwise; paid as a single payment of all or part of the eligible rights, no charge | [R3 L. 224-4](#frlib-per_assurance-r3) [R5 D. 224-4](#frlib-per_assurance-r5) [S2] [S3] [S4] [S7] |
| Transfer-out indemnity | 1 % of acquired rights while `duration < 5`, nil thereafter; plus an optional reduction of up to 15 % of euro-denominated rights, **off** in the base | [R3 L. 224-6](#frlib-per_assurance-r3) [R5 R. 224-6](#frlib-per_assurance-r5) [S1]–[S8] |
| Death closes the plan | Benefit = account value, floored by the *garantie plancher* to the 70th birthday, capped €762 245 | [R3 L. 224-4 II](#frlib-per_assurance-r3) [S1] [S3] |
| Exit menu | Capital in one payment or *fractionné*, annuity, or a mix; c3 annuity only | [R3 L. 224-5](#frlib-per_assurance-r3) |
| Annuity basis | Technical rate **0 %**; TGF05 / TGH05 or a certified experience table that may not be cheaper | [R9 A. 142-1](#frlib-per_assurance-r9) [R11] [R12] [REG-R21] [REG-R23] |
| Small-annuity commutation | Monthly *quittance* ≤ €110, scaled by the months in the payment period | [R10 A. 160-2](#frlib-per_assurance-r10) |

### (b) Insurer-discretionary current elements (snapshot; maxima disclosed, levels not capped [REG-R30])

| Input | Symbol | Value | Basis |
|---|---|---|---|
| Entry loading on each *versement* | `load` | 2,50 % | [S8] [S10]; adoption **[std]**, product-spec (10) |
| Euro management charge | `c_eu` | 0,70 % p.a. | [S8] [S9]; adoption **[std]** (11) |
| UC management charge | `c_uc` | 0,70 % p.a. | [S8] [S9]; adoption **[std]** (11) |
| Arbitrage charge on the rebalancing | `arb_rate` | 0,30 % of the amount switched | [S1]; adoption **[std]** (9) |
| *Frais d'arrérages* | `c_arr` | 1,50 % of each gross instalment | [S8]; adoption **[std]** (13) |
| Euro-fund gross asset return | `r_eu` | 3,38 % p.a. | [S9]; adoption **[std]**, product-spec (5) |
| UC gross return, net of fund-level charges | `r_uc` | 5,00 % p.a. | **[std]**, product-spec (5) |
| Annuity conversion factor, male 64, annual in arrears, no reversion | `a_x` | 22,0000 | **[std]**, product-spec (17) |
| PPB stock and release policy | — | not modelled | simplification **[std]** (1) |

1. The euro credit is set at the asset return and the charge taken on the post-crediting
   balance; no *provision pour participation aux bénéfices* stock is carried. The only
   retrieved gross-charge-net triple shows the served rate exceeding asset return less
   charge by 7 basis points [S9], i.e. a PPB release, and a PER's PPB horizon is fifteen
   years rather than eight because the commitments sit in a *comptabilité auxiliaire
   d'affectation* [REG-R16] [R8 L. 142-4](#frlib-per_assurance-r8). Modelling that stock is a scenario extension:
   four of the seven sampled contracts have **no** contractual PB clause at all
   [S4] [S5] [S6] [S7]. The machinery this replaces — the *compte de participation aux
   résultats*, the PPB dotation-and-release lever and its vintage clock — is specified in
   `products/assurance_vie_euro/technical-notes.md`; see *The euro leg is
   cross-referenced, not re-implemented* below for what to take from it and what not to.

### (c) Behavioral / experience assumptions (modeler's view)

The homologated tables are cited, never shipped: TH 00-02 / TF 00-02 for the death
benefit during accumulation and TGH05 / TGF05 for the annuity [REG-R21] [REG-R22]
[REG-R23].

| Input | Recommended basis | Basis tags |
|---|---|---|
| `mort_rate` | INSEE-derived proxy, sex-distinct; **0,00500 flat** in the worked example | **[std]** (2); source [REG-R24]; regulatory basis [REG-R22] [REG-R23] |
| `early_release_rate` | 1,60 % p.a., flat | **[std]** (3) |
| `transfer_out_rate` | 1,00 % p.a., flat | **[std]** (3) |
| `lapse_rate` | **does not exist** — there is no surrender right | [R3 L. 224-4](#frlib-per_assurance-r3) [S2] [S3] [S4] [S7] |
| Maintenance expense | €30 per plan p.a., inflating 1,80 % p.a. | **[std]** (4) |
| Annuity election at the horizon | `annuity_share = 0,30` | **[std]**, product-spec (16) |
| Profile-change and horizon-change behavior | not modelled | **[std]** (5) |

2. TH 00-02 / TF 00-02 are homologated and public but are not redistributed here
   [REG-R22] [REG-R23]; the shipped CSV is an INSEE-derived proxy [REG-R24] anchored so
   that the model reproduces the flat 0,00500 used in the worked example. Population
   mortality is heavier than insured experience, and the *décalage d'âge* age shifts the
   regulatory tables carry [REG-R23] are not reproduced. No observed range exists: no
   sampled contract publishes a mortality basis, and the one published rate card [S7] is
   a gross premium scale, not a set of decrement rates.
3. No public split of accumulation-phase exits exists [research §18]. The one citable
   anchor is aggregate: early releases and transfers together were €1 651 m against
   €63,0 bn of accumulation-phase provisions in 2024, i.e. **2,62 %** [R22], which the
   split 1,60 % / 1,00 % reproduces to 2,60 %. Two caveats travel with it: it is an
   *amount* ratio adopted as a *policy* decrement rate, which assumes exiting plans carry
   the average balance; and it is contaminated by the market's growth phase — the book was
   growing 18,7 % a year [R22] — so it is not a steady-state rate.
4. No insurer's unit cost is public; only the charge cap is [research §18] [REG-R30]. The
   €20 association fee [S8] is a one-off at adhesion, nil for in-force cells.
5. The declared retirement date may be changed at any time [R5 D. 224-3](#frlib-per_assurance-r5), re-allocating
   the whole balance immediately [S3] [S4]. The base model holds `retirement_age` fixed;
   a scenario overlay can shift it and re-read the grid.

**Why the exit decrements are not called lapses.** The house vocabulary reserves
`lapse_rate` and `claims_lapse` for a contractual surrender right, and this contract has
none — the accumulation phase carries **no surrender right except in the statutory cases**
[S2] [S3] [S4] [S7], the plan being blocked until the L. 224-1 maturity [R3 L. 224-1](#frlib-per_assurance-r3). The
two exit decrements are named for what they are.

- **`early_release_rate`** — *déblocage anticipé* under one of the seven L. 224-4 cases
  [R3]. Not a lapse in four respects: it requires a listed triggering event; it bears
  **no charge** [S2] [S3] [S7]; it may be **partial**, leaving the plan in force
  [R5 D. 224-4](#frlib-per_assurance-r5); and its main-residence limb is closed to compartment 3
  [R3 L. 224-4 I 6°](#frlib-per_assurance-r3). The base model treats it as a full exit paying the whole account
  value, the partial case being a documented extension.
- **`transfer_out_rate`** — a transfer of acquired rights to another PER [R3 L. 224-6](#frlib-per_assurance-r3).
  The plan ends for this insurer but the savings do not leave the regime: the blocage,
  the compartments and the exit conditions travel with the money. It pays a transfer
  value, not a surrender value, and its formula differs from the early-release one by the
  1 % indemnity in the first five years.

Using one decrement for both, or naming either `lapse_rate`, silently attaches the wrong
payment formula to half the exits.

---

## Cash flow components and recursions

### Notation (defined once, used throughout)

| Symbol | Meaning |
|---|---|
| `t` | plan year index 1, 2, …, `n`; `n = proj_len = retirement_age − age(0)` |
| `k(t)` | years to the horizon at the start of year `t`: `k(t) = n − t + 1` |
| `a(t)` | target euro (low-risk) share for year `t`, read from the grid at `k(t)` |
| `V` | *versement* received at BOY; `V_net = V · (1 − load)` |
| `load`, `c_eu`, `c_uc`, `arb_rate`, `c_arr` | 2,50 %, 0,70 %, 0,70 %, 0,30 %, 1,50 % |
| `r_eu`, `r_uc` | euro and UC gross returns, 3,38 % and 5,00 % |
| `E_eu(t)`, `E_uc(t)` | per-policy support balances after the BOY steps |
| `A(t)` | per-policy total account value at EOY `t`, `= av_pp(t, EOY)` |
| `A⁻(t)` | per-policy total carried into year `t`, `= A(t−1)` |
| `m(t)` | gross amount switched at the BOY rebalance |
| `g(t)` | *garantie plancher* base, `death_floor_pp(t)` |
| `q(t)` | `mort_rate` for year `t` |
| `w_e(t)`, `w_r(t)` | `early_release_rate`, `transfer_out_rate` for year `t` |
| `ι(t)` | transfer indemnity rate: 1 % while `duration(t) < 5`, else 0 |
| `l(t)` | in force at the **end** of year `t`; `l(0) = 1`. In cells names `pols_if_at(t, "AFT_DECR")`; the start-of-year count `l(t−1)` is `pols_if(t)` |
| `a_x` | annuity conversion factor at the horizon, 22,0000 **[std]**, product-spec (17) |
| `θ` | `annuity_share`; `C_thr` = €110 monthly commutation threshold [R10] |
| `E(t)` | maintenance expense, `30 · 1,018^(t−1)` **[std]**, assumption footnote (4) |

### The glide path

```
k(t)  = n - t + 1
a(t)  = grid[allocation_profile, k(t)]
```

with the *équilibré* grid `a = 0 %` for `k > 10`, `20 %` for `10 ≥ k > 5`, `50 %` for
`5 ≥ k > 2`, `70 %` for `k ≤ 2` [R6 art. 1](#frlib-per_assurance-r6) **[std]** band edges. The grid is an **input
table**, not a formula: the model reads `allocation_grid.csv`, keyed by
(`allocation_profile`, `years_to_horizon`) with columns `euro_share` and `uc_share`, so
that the other three profiles and any insurer ladder finer than the four regulatory bands
[S1] substitute without touching the code.

### BOY rebalancing and the *versement*

```
m(t)      = a(t) · A⁻(t) − av_euro_pp(t−1, EOY)
arb(t)    = arb_rate · |m(t)|
E_eu(t)   = av_euro_pp(t−1) + m(t)              + a(t) · V_net
E_uc(t)   = av_uc_pp(t−1)   − m(t) − arb(t) + (1 − a(t)) · V_net      (m ≥ 0)
```

with the roles of the two supports exchanged when `m(t) < 0`. Two conventions, both
**[std]**: the arbitrage charge is taken from the **source** support, so the destination
receives the full switch and the post-rebalancing euro share lands **at or just above**
the regulatory minimum rather than just below it; and the *versement* is allocated
directly at the target mix and bears no arbitrage charge, which is what "allocation of
both contributions and existing balance" means in the one contract publishing its ladder
[S1]. Under a de-risking profile `a(t)` is non-decreasing, so `m(t)` is normally positive
(UC → euro); it can turn negative after a UC fall, and the formula is symmetric.

### Crediting and charges

```
av_euro_pp(t, EOY) = E_eu(t) · (1 + r_eu) · (1 − c_eu)
av_uc_pp(t, EOY)   = E_uc(t) · (1 + r_uc) · (1 − c_uc)
A(t)               = av_euro_pp(t, EOY) + av_uc_pp(t, EOY)
```

The euro support rises in the base run, but it is **not monotone by construction**, and
the difference matters. A. 142-1 caps the *tariff's* technical rate at 0 % — "un taux
d'intérêt technique **au plus égal à** 0 %" [R9 A. 142-1](#frlib-per_assurance-r9) — which is a
maximum, not a floor on what is credited; a PER euro fund has **no guaranteed
accumulation rate at all**, only a capital floor gross of charges plus profit sharing
[S1] [S7] (product-spec, *Euro-fund crediting*). Since the charge is taken on the
post-crediting balance, `av_euro_pp` grows only while `r_eu > c_eu / (1 − c_eu)`, which is
**0,7049 %** at `c_eu = 0,70 %`. The base run's 3,38 % clears that comfortably; at a
credited 0 % the support would fall by the charge each year. The effective euro rate net
of charge is `1,0338 × 0,9930 − 1 = 2,6563 %` — not `3,38 − 0,70 = 2,68 %`, and not the
`2,75 %` actually served in 2025, whose extra seven basis points came from a PPB release
[S9] the base model does not carry.

### The euro leg is cross-referenced, not re-implemented

`r_eu` above is a **flat credited rate**, and the *participation aux bénéfices* machinery
that would produce one is deliberately absent from this model. What it replaces is
specified, with the same citation discipline, in
`products/assurance_vie_euro/technical-notes.md` — sections *The `compte de participation
aux résultats`*, *The crediting rule, the TMG and the PPB lever* and *The PPB and its
eight-year clock*. In outline: the minimum PB is built each year on the two accounts of
art. A. 132-11 [REG-R14] [REG-R15] — 85 % of the financial account plus the technical
account less the insurer's share — and the rate actually served is then moved above or
below that statutory floor by dotations to and releases from the *provision pour
participation aux bénéfices*, with a *taux minimum garanti* as a hard floor underneath and
each PPB vintage due to be spent within eight years [REG-R16].

Three things a reader should take from those notes rather than from these.

- **The crediting rate is an output of a fund-level system, not an input.** Here it is an
  input, at a single observed figure carried flat, which is the (b)-table's
  "PPB stock and release policy — not modelled **[std]**" and assumption footnote (1).
  Nothing in this model produces `r_eu`, and no sensitivity run on it is a projection of
  what an insurer would credit.
- **The PPB is a two-way lever, and its clock is longer here.** The eight-year release
  deadline the euro-fund notes model is **fifteen** years for PER commitments, which sit
  in a *comptabilité auxiliaire d'affectation* [REG-R16] [R8 L. 142-4](#frlib-per_assurance-r8).
  A PPB layer lifted from `Euro_FR_A` onto this product has to have that clock changed.
- **A PER euro fund and an assurance vie euro fund are not the same contract.** Four of
  the seven sampled PER contracts have **no** contractual PB clause at all [S4] [S5] [S6]
  [S7], and the *garantie plancher* and glide path specified here have no counterpart in
  the euro-fund product. Take the crediting chassis from those notes; do not take the
  liability.

The one number in this model that a PPB would have changed is visible: [S9]'s triple is a
3,38 % asset return, a 0,70 % charge and a **2,75 %** rate served, and the seven basis
points between `2,6563 %` and `2,75 %` are the release this model does not carry.

### The garantie plancher base

```
g(t) = g(t−1) + V_net − arb(t) − charges taken in year t
```

where the charges taken are `E_eu(t)·(1+r_eu)·c_eu + E_uc(t)·(1+r_uc)·c_uc`.

**Two contractual draftings exist and this is [S1]'s, not [S3]'s.** [S1] guarantees a
death benefit "not less than premiums net of charges minus benefits already paid" — no
interest limb — and [S7] states expressly that its guarantee is **not** a floor at gross
premiums. [S3] drafts the same guarantee the other way: the settled amount "cannot be less
than contributions net of loading **plus euro-fund interest net of management charges**".
The recursion above is [S1]'s alone. **These notes are the source of truth for the
modelled quantity**, and `product-spec.md`'s *Death benefit during accumulation* table
carries the same drafting for that reason.

The difference is not cosmetic. Under [S1]'s drafting

```
A(t) − g(t) = [A(0) − g(0)] + Σ gross investment return credited to date
```

so the floor bites only where cumulative investment return is negative, which is what
`check_floor_identity()` asserts. Under [S3]'s drafting the euro leg of that return
accrues to the floor as well, so on an all-euro plan the floor would track the account
value and the identity above would fail by construction. Implementing [S3] means adding
the euro credit net of its charge to `g(t)` and dropping the identity, not adjusting a
parameter.

The cover ceases at the member's 70th birthday [S1] [S3] and is capped at €762 245 across
contracts [S3].

### Decrements and benefits at EOY

```
d_death(t)    = l(t−1) · q(t)
d_release(t)  = l(t−1) · (1 − q(t)) · w_e(t)
d_transfer(t) = l(t−1) · (1 − q(t)) · (1 − w_e(t)) · w_r(t)
l(t)          = l(t−1) · (1 − q(t)) · (1 − w_e(t)) · (1 − w_r(t))
```

An ordered dependent-decrement convention **[std]**, matching the library's house
treatment. Per-policy benefit amounts: `max(A(t), g(t))` on death while the floor is in
force, else `A(t)` [R3 L. 224-4 II](#frlib-per_assurance-r3) [S1] [S3]; the whole of `A(t)` on early release, with
no charge [R5 D. 224-4](#frlib-per_assurance-r5) [S2] [S3] [S7]; and `A(t) · (1 − ι(t))` on transfer out
[R3 L. 224-6](#frlib-per_assurance-r3).

### The exposure convention

These notes index the in-force probability at the **end** of the year, as `l(t)`. The
library indexes the published exposure at the **start** of the period, because that is the
weight the period's own cash flows carry. Both live in the model, under different names:

| Notes | Cells | Meaning |
|---|---|---|
| `l(t−1)` | `pols_if(t)` | in force at the **start** of year `t`; `pols_if(1) = 1`. The weight on row `t` of `result_cf()`, and the exposure every decrement of year `t` is taken against |
| — | `pols_if_at(t, "BEF_RELEASE")`, `pols_if_at(t, "BEF_TRANSFER")` | the intra-year steps of the ordered decrement |
| `l(t)` | `pols_if_at(t, "AFT_DECR")` | in force at the **end** of year `t`; the `pols_if_eoy` column of `result_state()` and the column the worked-example table below prints |

The two series are one period apart, `pols_if_at(t, "AFT_DECR") = pols_if(t+1)`, and the
one rule worth carrying away is that **`result_cf()["pols_if"]` weights its own row**: a
cash flow divided by that row's `pols_if` is a per-policy amount for the same year. The
survivors who settle at the horizon are `l(n) = pols_if_at(n, "AFT_DECR")`, after the
final year's decrements, which is why `claims_maturity` does not carry the same weight as
`premiums` in the same row.

### Settlement at the horizon

At `t = n` the survivors `l(n)` settle. With `θ = annuity_share`:

```
capital_leg   = (1 − θ) · A(n)                        no exit charge  [S1][S2][S3][S7][S8]
annuity_cap   = θ · A(n)
rente_gross   = annuity_cap / a_x                     0 % technical rate  [R9]
rente_net     = rente_gross · (1 − c_arr)             frais d'arrérages   [S8]
commute if      rente_net / 12 ≤ C_thr                                    [R10]
commuted      = rente_net · a_x
claims_maturity = capital_leg + ( commuted  if commuted else 0 )
annuity_conversion = 0 if commuted else annuity_cap
```

Two things follow from the 0 % technical rate. First, `a_x` is an **undiscounted**
expected-instalment count — the tariff table's curtate expectation of life at the annuity
age, not a discounted annuity factor. Second, commuting at the conversion basis returns
the converted capital less the *arrérage* charge exactly:
`rente_net · a_x = annuity_cap · (1 − c_arr)`. Commutation is therefore nearly
value-neutral, which is why it is common — €272 m of 2024 individual-PER benefits at an
average €16 200 [R22]. Where the annuity is not commuted, `annuity_conversion` is handed
to `Rente_FR_S`; the annuity reserve, the 0,80 % p.a. charge on annuity reserves [S7],
reversion, *annuités garanties* and revaluation through the profit-sharing account are
specified in `products/rente_viagere/technical-notes.md`.

### Annual processing order [std]

1. **BOY** — read `k(t)` and `a(t)` from the allocation grid.
2. **BOY** — receive `V`; deduct the entry loading; `V_net` is available to allocate.
3. **BOY** — rebalance the carried-in balance to `a(t)`: compute `m(t)`, take
   `arb(t)` from the source support, move `m(t)` to the destination.
4. **BOY** — allocate `V_net` at the target mix, `a(t)` to euro and `1 − a(t)` to UC.
5. Investment return accrues over the year on each support.
6. **EOY** — take the management charge on each post-crediting support balance.
7. **EOY** — update `g(t)` with `V_net`, less `arb(t)`, less the charges of step 6.
8. **EOY** — decrements in the order death, early release, transfer out; pay
   `claims_death`, `claims_early_release`, `claims_transfer` on the exiting probabilities.
9. **EOY** — maintenance expense `E(t)` on the in-force at the start of the year.
10. **EOY, `t = n` only** — settle the survivors: capital leg, annuity conversion,
    commutation test.
11. Roll `l(t)`, `age`, `duration(t)`.

### Known modeling pitfalls

These are the ways an implementation of *this* product looks right and is wrong. Each is
a test.

1. **Off-by-one on the glide-path band.** Bands are read on years *remaining*, and the
   boundary values 10, 5 and 2 belong to the tighter band **[std]**. Assert `a = 20 %` at
   `k = 10`, `50 %` at `k = 5`, `70 %` at `k = 2`; the looser reading understates the euro
   share for a full year at each of three transitions.
2. **Charging arbitrage on the *versement*.** New money is allocated at the target mix and
   is not a switch. Assert `arbitrage_charge_pp(t) = 0` in a year where the account opens
   exactly on target, even though a *versement* was paid.
3. **Taking the arbitrage charge from the destination**, which leaves the post-rebalancing
   euro share **below** the regulatory minimum. The assertion has to be stated by
   direction, because the source-charging convention above and a share at or above the
   line cannot both hold on a reverse switch. Assert
   `av_euro_pp(t, BOY) ≥ a(t) · av_pp(t, BOY)` where `m(t) ≥ 0` — the ordinary de-risking
   switch, where the UC bucket is the source and the euro destination receives the switch
   in full — and `av_euro_pp(t, BOY) ≥ a(t) · av_pp(t, BOY) − (1 − a(t)) · arb(t)` where
   `m(t) < 0`, the euro support being the source and so bearing the charge out of the
   balance being measured. `check_euro_share_min()` tests exactly that pair, against
   `euro_share_min_bound(t)`. **An unconditional `≥ a(t)` is wrong** and one shipped model
   point breaks it: point 2 opens 40 % euro against a 20 % minimum, sells euro down to the
   grid, and lands at `3 988 / 19 988 = 19,95 %`. That is the gap these notes leave open,
   not a defect in the model; a firm that resolves it by charging the UC side in both
   directions changes one branch of the rebalancing and nothing else.
4. **Testing the minimum at the wrong moment.** It binds at the rebalancing date; between
   dates the mix drifts with relative performance — in the worked example 70,00 % after
   the year-12 rebalance, 69,67 % at the year end. Re-imposing the target continuously
   invents a rebalancing frequency the annual grid lacks.
5. **Setting the capital floor at gross premiums.** The guarantee is *versements* net of
   loading and net of charges taken [S1] [S3] [S7]. Assert
   `av_pp(t) − death_floor_pp(t) = [av_pp(0) − death_floor_pp(0)] + Σ` gross investment return,
   and that the floor stops at the 70th birthday and caps at €762 245 [S1] [S3].
6. **Calling either exit a lapse.** There is no surrender right [R3 L. 224-4](#frlib-per_assurance-r3), no surrender
   charge and no market value adjustment. Assert `claims_early_release(t)` is the **whole**
   account value and that no `lapse_rate` or `claims_lapse` exists.
7. **Getting the transfer indemnity window wrong.** It runs to the fifth anniversary of the
   **first *versement***, not of the projection start [R3 L. 224-6](#frlib-per_assurance-r3). Assert
   `claims_transfer(t) / (d_transfer(t) · av_pp(t))` equals 0,99 while
   `duration_ifo + t < 5` and 1,00 afterwards.
8. **Double-counting exits.** Assert `d_death(t) + d_release(t) + d_transfer(t) + l(t) =
   l(t−1)` exactly, every year — in cells names, `pols_if(t)` less the three decrements
   equals `pols_if_at(t, "AFT_DECR")`. Reading `pols_if` as the *end*-of-year count here
   is the second pitfall hiding inside the first: see *The exposure convention*.
9. **Discounting the annuity conversion.** A PER tariff may not use a positive technical
   rate [R9 A. 142-1](#frlib-per_assurance-r9). Assert `a_x` equals the undiscounted sum of survival probabilities
   on the tariff table. A 2 % rate would shorten the factor from 22,0000 to
   `(1 − 1,02⁻²²) / 0,02 = 17,658` — a fall of **19,7 %** — and so inflate the annuity,
   which is `annuity_cap / a_x`, by `22 / 17,658 − 1 =` **24,6 %**. Quoting the fall in
   the factor as the rise in the annuity is itself the arithmetic slip; the two are not
   the same number.
10. **Commuting on a different basis from the conversion, or testing the threshold
    annually.** Assert `commuted = annuity_cap · (1 − c_arr)` exactly — commuting at a book
    value manufactures a gain out of nothing — and remember €110 is a **monthly**
    *quittance* scaled by the months in the payment period [R10], so an annual frequency
    tests against €1 320.
11. **Mixing per-policy and aggregate.** `av_pp` is per policy and already excludes
    decrements; multiplying a claims column by `pols_if` again understates every benefit by
    the square of the survival factor.
12. **Running the plan past the horizon, or putting tax in it.** `proj_len` ends at the
    declared retirement age, `k(t)` never goes negative and no *versement* arrives after
    settlement; and the deduction election, the age-graded fractions and the social levies
    change what the holder keeps, never what the insurer pays [R19] [R20] [R21].

---

## Policyholder behavior modeling

All dynamic formulas are **[std]**: no public French experience exists for PER lapse,
early-release, transfer or annuitisation rates by duration or age [research §18].

- **Base rates.** `early_release_rate` 1,60 % and `transfer_out_rate` 1,00 %, flat,
  anchored on the 2,62 % aggregate of [R22] — assumption footnote (3).
- **Transfer-out step at the five-year point.** The indemnity falls from 1 % to nil at the
  fifth anniversary [R3 L. 224-6](#frlib-per_assurance-r3) and a rational holder waits. A multiplier of **0,7**
  in the years before the anniversary and **1,3** in the anniversary year is the reference
  shape **[std]** — off in the base run so the worked example stays transparent. The pair
  is chosen so that the two adjacent years average to exactly 1,00 and turning the shape
  on does not quietly move the flat 1,00 % calibration; note that it is mean-preserving
  over **those two years only**, and that a run with several pre-anniversary years at 0,7
  averages below 1 and would have to be rescaled.
- **Early release is event-driven, not price-driven.** Its causes are death of a spouse,
  invalidity, serious illness of a dependent child, over-indebtedness, exhaustion of
  unemployment rights, business liquidation and purchase of the main residence
  [R3 L. 224-4](#frlib-per_assurance-r3). Only the last is discretionary, and none responds to investment
  performance; a dynamic moneyness multiplier would be a category error here.
- **The horizon is the behavioral variable.** The holder may move the declared retirement
  date at any time [R5 D. 224-3](#frlib-per_assurance-r5), re-cutting the whole allocation immediately [S3] [S4].
  That is the largest behavioral lever on this product and it has no public calibration.
- **Annuity election.** `annuity_share = 0,30` **[std]**; the 2024 payment-phase amounts
  split 47 % annuity, 28 % capital, 25 % commuted small annuity [R22], the third being an
  annuity election that reverses at settlement. **Commutation** is the insurer's option
  exercised with the annuitant's agreement [R10 A. 160-2](#frlib-per_assurance-r10); the base model commutes
  deterministically whenever the test passes, and a `commutation_agreement_rate`
  **[std]** is the natural refinement.

---

## Worked example

Anchor cell (product-spec, *Anchor model cell*): male, `age` 52 at t = 0, retirement age
64, so `proj_len = 12` and `k(1) = 12`; `duration_ifo = 2`; compartment c1; *équilibré*
profile; `av_euro_init = 0,00`, `av_uc_init = 16 600,00` [R22],
`death_floor_init = 16 000,00` **[std]**; `premium = 3 000,00` paid BOY every year to
the horizon, `V_net = 2 925,00` after the 2,50 % loading [S8]. Assumptions:
`r_eu = 3,38 %` [S9] carried flat **[std]**, `c_eu = c_uc = 0,70 %` [S8] [S9],
`r_uc = 5,00 %` **[std]**, `arb_rate = 0,30 %`
[S1], `q = 0,00500` flat **[std]**, `w_e = 1,60 %` and `w_r = 1,00 %` **[std]**, transfer
indemnity 1 % while `duration < 5` [R3 L. 224-6](#frlib-per_assurance-r3). Account columns are **per policy**, in
euros, to the cent; `l(t)` to six decimals.

The last column is `l(t)`, the in force at the **end** of the year — the `pols_if_eoy`
column of `result_state()`, not `result_cf()`'s `pols_if`, which on row `t` carries
`l(t−1)`. See *The exposure convention*.

| t | k | a(t) | V_net | arb | av_euro_pp | av_uc_pp | av_pp | l(t) |
|---|---|---|---|---|---|---|---|---|
| 1 | 12 | 0 % | 2 925.00 | 0.00 | 0.00 | 20 357.74 | 20 357.74 | 0.969289 |
| 2 | 11 | 0 % | 2 925.00 | 0.00 | 0.00 | 24 275.75 | 24 275.75 | 0.939522 |
| 3 | 10 | 20 % | 2 925.00 | 14.57 | 5 584.66 | 22 673.50 | 28 258.16 | 0.910668 |
| 4 | 9 | 20 % | 2 925.00 | 0.20 | 6 402.30 | 26 010.29 | 32 412.59 | 0.882701 |
| 5 | 8 | 20 % | 2 925.00 | 0.24 | 7 255.25 | 29 475.54 | 36 730.79 | 0.855592 |
| 6 | 7 | 20 % | 2 925.00 | 0.27 | 8 141.84 | 33 077.41 | 41 219.24 | 0.829316 |
| 7 | 6 | 20 % | 2 925.00 | 0.31 | 9 063.37 | 36 821.28 | 45 884.65 | 0.803847 |
| 8 | 5 | 50 % | 2 925.00 | 41.64 | 25 053.10 | 25 402.28 | 50 455.38 | 0.779161 |
| 9 | 4 | 50 % | 2 925.00 | 0.52 | 27 399.17 | 27 827.98 | 55 227.15 | 0.755232 |
| 10 | 3 | 50 % | 2 925.00 | 0.64 | 29 848.43 | 30 315.50 | 60 163.93 | 0.732038 |
| 11 | 2 | 70 % | 2 925.00 | 36.80 | 45 335.35 | 19 695.53 | 65 030.89 | 0.709557 |
| 12 | 1 | 70 % | 2 925.00 | 0.56 | 48 832.72 | 21 255.68 | 70 088.40 | 0.687766 |

Settlement of the survivors at the end of year 12, with `annuity_share = 0,30`,
`a_x = 22,0000` **[std]** and `c_arr = 1,50 %` [S8]:

| Quantity | Value |
|---|---|
| `av_pp(12)` | 70 088.40 |
| `capital_leg = 0,70 · av_pp(12)` | 49 061.88 |
| `annuity_cap = 0,30 · av_pp(12)` | 21 026.52 |
| `rente_gross = annuity_cap / 22` | 955.75 |
| `rente_net = rente_gross · 0,985` | 941.41 |
| monthly equivalent `rente_net / 12` | 78.45 |
| commutation test against €110 [R10] | 78.45 ≤ 110 → **commute** |
| `commuted = rente_net · 22` | 20 711.12 |
| `claims_maturity` per policy | 69 773.00 |
| `claims_maturity` aggregate, `× l(12) = 0,687766` | 47 987.47 |
| `death_floor_pp(12)` | 47 267.36 |

Aggregate benefits over the twelve years, per model point:
`claims_death` 2 160.30, `claims_early_release` 6 878.40, `claims_transfer` 4 225.92.

**Checks.** *(i) The floor identity.* `av_pp(12) − death_floor_pp(12) = 70 088.40 −
47 267.36 = 22 821.04`, and the opening gap `16 600.00 − 16 000.00 = 600.00` plus the
gross investment return credited over the twelve years, `22 221.04`, is the same number.
The *garantie plancher* is therefore 32,6 % below the account value and never bites in
this scenario [S1] [S3]. *(ii) The year-8 band crossing, re-derived.* Year 8 opens with
`av_pp = 45 884.65` and `k = 5`, so the target euro share steps from 20 % to 50 %: the
target euro balance is `0,50 × 45 884.65 = 22 942.32` against `9 063.37` held, a switch of
`13 878.95`, an arbitrage charge of `0,003 × 13 878.95 = 41.64` taken from the UC side,
and a BOY euro balance of `9 063.37 + 13 878.95 + 0,50 × 2 925.00 = 24 404.82`. Crediting
and charging gives `24 404.82 × 1,0338 × 0,9930 = 25 053.09`, one cent below the table's
`25 053.10` because the model carries the year-7 balance unrounded — intermediates are at
full precision and only reported cash flows are rounded. The BOY euro share is
`24 404.82 / 48 768.01 = 50,04 %`, at or just above the regulatory minimum as the
source-charging convention requires. By year end relative performance has moved
it: the year-12 euro share is `48 832.72 / 70 088.40 = 69,67 %`, below the 70 % target
that held at the rebalancing date. *(iii) The commutation identity.* `941.414625 × 22 =
20 711.12`, which is also `21 026.52 × 0,985` — commuting at the conversion basis returns
the converted capital less the *arrérage* charge, and the total maturity claim of
69 773.00 is `av_pp(12)` less `0,015 × 21 026.52 = 315.40`. The anchor cell's annuity, at
€78.45 a month, is a live instance of the market pattern: the average PER annuity in
payment is €1 300 a year, about €108 a month, just under the €110 threshold [R22] [R10],
and the cliff for this cell sits at `annuity_share = 42,06 %` — at 50 % the annuity would
be €1 569.02 a year, €130.75 a month, above the threshold and paid as a *rente*.

Per-policy expenses run `E(t) = 30 · 1,018^(t−1)` **[std]**, so `E(12) = 36.50` and the
undiscounted twelve-year total before survivorship is `397.87`.

### Cash flow outputs (per plan year `t`)

`l(t−1)` below is the count the year opens with, which is the `pols_if` column of
`result_cf()` on the same row; `l(n)` is the count the final year closes with,
`pols_if_at(n, "AFT_DECR")`.

| Output | Formula |
|---|---|
| `premiums` | `V · l(t−1)` |
| `claims_death` | `d_death(t) · max( A(t), g(t) )` |
| `claims_early_release` | `d_release(t) · A(t)` |
| `claims_transfer` | `d_transfer(t) · A(t) · (1 − ι(t))` |
| `claims_maturity` | `l(n) · (capital_leg + commuted)` at `t = n`, else 0 |
| `annuity_conversion` | `l(n) · annuity_cap` at `t = n` where not commuted, else 0 |
| `expenses` | `E(t) · l(t−1)` |
| `liability_cf` | claims + `annuity_conversion` + expenses − premiums (outgo-positive) |
| `net_cf` | `− liability_cf` (income-positive, per the house sign convention) |

---

## Valuation and reserve pointers

This library projects gross best-estimate liability cash flows; valuation layers are
cited, not reproduced.

- **The French statutory provision.** The *provision mathématique* is the difference
  between the actuarial present values of the two parties' commitments, **including
  future management costs** [REG-R6] — not a net-premium reserve. For the annuity phase,
  one contract states it as "la valeur des engagements de rente, fonction de la table de
  mortalité et du taux d'intérêt technique à 0 %" [S3], which at a 0 % rate is a pure
  life-contingent instalment count with no interest offset.
- **Profit sharing.** The statutory minimum PB is determined globally, not contract by
  contract, from a *compte de participation aux résultats* credited with 85 % of the
  financial balance and the technical balance less the insurer's share [REG-R14]
  [REG-R15]; sums parked in the PPB must be released within eight years — **fifteen** for
  commitments under a *comptabilité auxiliaire d'affectation*, which is what a PER is
  [REG-R16] [R8 L. 142-4](#frlib-per_assurance-r8). UC commitments are outside that machinery [REG-R15]. The
  ring fence itself carries a policyholder priority claim and an ACPR-supervised recovery
  plan on under-coverage [R8 L. 142-4 to L. 142-6](#frlib-per_assurance-r8) [REG-R10] — a constraint a
  single-policy model cannot see and a fund-level projection must.
- **Solvency II and IFRS 17 — cited, not specified.** Technical provisions, SCR and risk
  margin [REG-R1] [REG-R2] and the risk-free term structure used to discount [REG-R5]
  were not researched for this product [unverified]; IFRS 17 measures fulfilment cash
  flows plus a contractual service margin from 2023 [REG-R45], its variable fee approach
  for direct participating contracts being [unverified] here. The engine is this same
  projection.
- **Tax, plainly.** Deductibility at entry under CGI art. 163 quatervicies [R13]
  [REG-R42] changes the taxation of the exit — pension regime with the 10 % abatement, or
  *rente viagère à titre onéreux* on an age-graded fraction, or the flat levy on gains
  [R19] [R20] [R21] — but **not the gross liability cash flows**. The insurer pays the same
  euro amount either way; the difference is withheld or assessed downstream. Tax therefore
  appears in no recursion above, and `deduction_elected` is carried solely so a downstream
  tax layer can find it. The same applies to the death-benefit levies, where the trigger
  is the **age at death**, not the age at which premiums were paid, and a PER pays
  inheritance duty on the **whole** benefit after 70 [R15] [REG-R41].
- **Professional standards.** NPA 1 and NPA 2 are *pratiques recommandées* of the Institut
  des actuaires; NPA 2 applies to any actuarial model under a proportionality principle
  [REG-R43] [REG-R44].

---

## Key sensitivities and model risks

1. **The glide path is the product's dominant financial lever.** Moving the *équilibré*
   grid to the *prudent* one raises the euro share from 0/20/50/70 to 30/60/80/90 [R6],
   replacing most of a 5,00 % UC return with a 3,38 % euro return over the anchor cell's
   twelve years. The grid is an input table for exactly this reason. Annual rebalancing
   also understates tracking: real contracts rebalance quarterly to semi-annually
   [S1] [S3] [S7], and the annual grid concentrates each step into one switch.
2. **The declared horizon.** Changing `retirement_age` re-cuts the whole allocation
   instantly [R5 D. 224-3](#frlib-per_assurance-r5) [S3] [S4] and changes the number of years the plan compounds.
   No public data exists on how often holders move it [research §18].
3. **The two exit decrements dominate the run-off.** At 2,60 % a year combined they remove
   about a quarter of the book over twelve years — far more than mortality. Both rates are
   **[std]** on a single aggregate anchor [R22] contaminated by the market's growth phase.
4. **Charge levels, not charge structure, drive the outcome.** The sampled entry loading
   spans 0 % to 4,80 % and the euro management charge 0,50 % to 2,30 % [S1]–[S8]; the
   composite sits near the middle. The *encadré* discloses maxima and caps nothing
   [REG-R30], so a charge level is never a contractual constant.
5. **The annuity factor is a placeholder.** `a_x = 22,0000` is **[std]**; no sampled
   insurer publishes a rate card and TGH05 / TGF05 were not extracted [R12] [REG-R21].
   The commutation cliff at `annuity_share = 42,06 %` moves directly with `a_x`.
6. **Mortality is a proxy.** The shipped decrement CSV is an INSEE-derived **[std]** proxy
   [REG-R24]; the regulatory tables are cited, not shipped [REG-R22] [REG-R23]. The only
   published rate card in the sample is a *gross premium* scale on a no-underwriting death
   rider [S7] and must not be read as a mortality basis.
7. **No PPB stock.** The base model credits the asset return directly, so `r_eu` is an
   assumption rather than an output. Where an insurer smooths — and the one retrieved
   triple shows seven basis points of it [S9] — the crediting path and the PPB balance are
   one two-lever system, with a fifteen-year release horizon here against the general eight
   [REG-R16]. That system is specified in
   `products/assurance_vie_euro/technical-notes.md` and summarised above under *The euro
   leg is cross-referenced, not re-implemented*.
8. **Two options are outside the base run.** The 15 % transfer-value reduction dominates
   the 1 % indemnity by an order of magnitude in a rising-rate scenario [R5 R. 224-6](#frlib-per_assurance-r5)
   [S8], and one contract's annuity table frozen at adhesion for deductible C1 sums [S1]
   is a long-dated longevity option given away for nothing. Neither is visible in a base
   run; valuing either needs a stochastic layer.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R10]: #frlib-per_assurance-r10
[R11]: #frlib-per_assurance-r11
[R12]: #frlib-per_assurance-r12
[R13]: #frlib-per_assurance-r13
[R15]: #frlib-per_assurance-r15
[R19]: #frlib-per_assurance-r19
[R20]: #frlib-per_assurance-r20
[R21]: #frlib-per_assurance-r21
[R22]: #frlib-per_assurance-r22
[R3]: #frlib-per_assurance-r3
[R6]: #frlib-per_assurance-r6
[REG-R1]: #frlib-reg-r1
[REG-R10]: #frlib-reg-r10
[REG-R14]: #frlib-reg-r14
[REG-R15]: #frlib-reg-r15
[REG-R16]: #frlib-reg-r16
[REG-R2]: #frlib-reg-r2
[REG-R21]: #frlib-reg-r21
[REG-R22]: #frlib-reg-r22
[REG-R23]: #frlib-reg-r23
[REG-R24]: #frlib-reg-r24
[REG-R30]: #frlib-reg-r30
[REG-R41]: #frlib-reg-r41
[REG-R42]: #frlib-reg-r42
[REG-R43]: #frlib-reg-r43
[REG-R44]: #frlib-reg-r44
[REG-R45]: #frlib-reg-r45
[REG-R5]: #frlib-reg-r5
[REG-R6]: #frlib-reg-r6
[std]: #frlib-std
[unverified]: #frlib-unverified
<!-- END generated citation links -->
