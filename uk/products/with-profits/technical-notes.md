# With-Profits Business — Liability Cash Flow Model: Technical Notes (United Kingdom)

**Status:** Draft, 2026-08-03 (all cited sources accessed 2026-08-03).

**Scope note.** These notes specify a reference liability cash-flow projection model
for the standardized composite product defined in `product-spec.md` (same directory).
This is not any single insurer's fund. [S#]/[R#] tags refer to the source list in
`sources.md` (numbering carried from `uk/_research/with-profits.md`); [REG-R#] tags
refer to the cross-product reference library
`uk/references/regulatory-and-actuarial-references.md` (its own R-numbering; research
provenance in `uk/_research/regulatory-actuarial.md`). **[std]** marks
standardizations introduced for the reference implementation; [unverified] marks
claims not confirmed against a retrieved document. Parameter values are identical to
those in `product-spec.md`. Mechanics anchors: PAC PPFM [S1], Phoenix PPFM [S4],
Aviva PPFM [S5]; regulatory codification of the asset-share item list: PRA Surplus
Funds Part [R8]; canonical methodology literature: Needleman & Roff (1995) on asset
shares and Hibbert & Turnbull (2003) on guarantee costs, as listed on the IFoA SA2
resources page [R13].

---

## Model scope and conventions

- **Purpose.** Project gross best-estimate liability cash flows (premiums in; death,
  maturity and surrender claims out; expenses; shareholder transfers) for
  single-policy with-profits model points on the two composite chassis (unitised bond,
  conventional endowment), with the smoothed-fund (PruFund-style) variation as an
  alternative crediting module. Reserves are not computed here (see Valuation and
  reserve pointers).
- **The asset share is a state variable, not a cash flow.** Policy cash flows are
  premiums, claims (paid at smoothed payouts), expenses and shareholder transfers;
  the asset share [S1][R8] drives claim amounts through the bonus, smoothing and MVR
  machinery. The estate absorbs payout-vs-asset-share differences [S1][S5].
- **Projection frequency.** Annual **[std]**. Rationale: bonus declarations, the
  governing discretion cycle, are annual [S1][S4][S7]; sub-annual mechanics (daily
  unit pricing [S4], PruFund daily/quarterly smoothing [S9][S11]) are compressed to
  annual equivalents in the base model, with the PruFund module noting its native
  daily/quarterly grid.
- **Timing conventions [std].** Premiums and partial withdrawals at the start of the
  policy year (BOY); fund return accrues over the year; proportional charges, bonus
  declaration, shareholder transfer and mortality charge at end of year (EOY), in the
  processing order below; claims and decrements at EOY after declaration.
- **Age basis.** Age nearest birthday **[std]** — no retrieved UK document fixes a
  model age basis; ANB is chosen for symmetry with the library's US convention (its
  traditional use in UK assured-lives tables is [unverified]; the currently marketed
  bond quotes its issue-age limit on an age-next-birthday basis [S10]).
- **Currency.** GBP. Single-policy model points, projected on an expected
  (probability-weighted) basis: survivorship factors multiply per-policy cash flows.
- **Specimen-policy convention.** Firms compute asset shares for specimen policies or
  groups, not necessarily per policy [S1][S4][S5][R1 COBS 20.2.5R(2)]; the reference
  model computes a per-model-point asset share and treats it as the specimen.
- **Rounding.** Intermediate values at full precision; cash flows reported to pence
  **[std]**.

---

## Model point attributes

| Attribute | Type | Example (anchor cells, product-spec) |
|---|---|---|
| `chassis` | enum {UWP_bond, CWP_endowment, SF_prufund} | UWP_bond |
| `issue_age` | int (ANB) | 55 (UWP) / 35 (CWP) |
| `sex` | enum {M, F} | M |
| `duration_ifo` | int, completed policy years at valuation | 5 |
| `premium_single` | currency (UWP bond) | 25,000 |
| `premium_regular` | currency p.a. (CWP: £60/month → 720 p.a.) | 720 |
| `sum_assured` | currency (CWP basic SA) | 20,000 |
| `term_years` | int (CWP; UWP bond whole-of-life → none) | 25 |
| `units` | float (UWP) | 25,000 |
| `unit_price` | currency (UWP `Q`; £1.0000 at seed) | 1.104081 |
| `attaching_bonus` | currency (CWP `G − SA`) | — |
| `asset_share_0` | currency (in-force cells) | 30,000 |
| `smoothed_payout_0` | currency (`S(0)` benchmark for the y/y cap) | 29,500 |
| `guarantee_dates` | list of anniversaries (MVR-free) | {10} |
| `mvr_free_wd_rate` | % of original premium p.a. | 5% |
| `tax_basis` | enum {life_net, pension_gross} [S1][REG-R17] | life_net |
| `gao_flag` / `gao_rate` | bool / annuity per £1 cash | false / — |
| `profitshare_flag` | bool (mutual variation [S6]) | false |

---

## State variables

| Variable | Description | Updated |
|---|---|---|
| `AS(t)` | Asset share at end of year t [S1][R8] | annual recursion |
| `Q(t)` | With-profits unit price (UWP); never decreases | EOY declaration |
| `FV(t)` | Unit face value `U(t)·Q(t)` (UWP) | EOY |
| `G(t)` | Guaranteed benefit `SA` + attaching reversionary bonuses (CWP) | EOY declaration |
| `b(t)` | Declared regular bonus rate for year t | EOY, setting rule |
| `S(t)` | Smoothed target payout (after y/y cap and corridor) | EOY |
| `FB(t)` | Final (terminal) bonus payable on claim in year t | EOY |
| `MVR(t)` | Market value reduction on non-guaranteed exits | EOY |
| `CB(t)` | Cost of bonus recognized in year t | EOY |
| `ST(t)` | Shareholder transfer = `CB(t)/9` (90:10) | EOY |
| `SM(t)` | Smoothing account balance (within estate) | on exits |
| `CumGC(t)` | Cumulative guarantee-charge deductions (for the 2% lifetime cap [S1]) | annual |
| `l(t)` | In-force probability at end of year t | EOY decrements |

---

## Assumption inputs

Three classes are distinguished explicitly. Class (a) is contractual/guaranteed;
class (b) is the insurer's current discretionary scale (PPFM-governed discretion
[R2], advised by the With-Profits Actuary [R5]); class (c) is the modeler's view of
experience.

### (a) Contractual / guaranteed elements (cited)

| Input | Value | Basis |
|---|---|---|
| Basic sum assured / premium / term (CWP) | £20,000 / £720 p.a. / 25 years | anchor **[std]**, product-spec (15) |
| Bonus hardening | declared regular bonus increases the guaranteed benefit; contractual once added; guaranteed at death/maturity only | [S1][S8] |
| Unit-price floor (UWP) | `Q(t) ≥ Q(t−1)`, i.e. `b(t) ≥ 0` | [S1][S4] |
| Guarantee events (UWP) | death; contractual guarantee dates (10th anniversary); face value + FB payable without MVR | [S4][S5]; date choice **[std]**, product-spec (12) |
| Death benefit factor (UWP) | `g_db = 101%` of (FV + FB); MVR never on death | 101% **[std]**, product-spec (11); no-MVR [S5] |
| MVR-free withdrawals | ≤ 5% p.a. of original premium | **[std]**, product-spec (13) |
| MVR contractual bound | MVR ≤ excess of unit value over underlying asset value | [R1 COBS 20.2.16R] |
| PruFund smoothing limits (variation) | daily 5.0% / quarterly 10.0% / gap 2.5% (growth funds); contractual defined terms | [S9][S11] |

### (b) Insurer-discretionary current elements (snapshot; revisable under PPFM discipline [R2][R5])

| Input | Value | Basis |
|---|---|---|
| Regular bonus rate `b` — UWP | 2.00% p.a. | **[std]**, product-spec (8) — declarations not public in PPFMs |
| Reversionary bonus rate `b_rev` — CWP | 1.50% p.a. compound | **[std]**, product-spec (16) |
| Bonus change cap | ±1.00% p.a. in normal circumstances; floor 0 | [S1][S7]; adoption **[std]**, product-spec (20) |
| Guarantee-fill target `θ` | 80% of projected maturity asset share | **[std]**, product-spec (21); philosophy [S1] |
| Smoothing y/y cap `σ` | ±10% | [S1]; adoption **[std]**, product-spec (23) |
| Target corridor | 80%–120% of asset share | [S1][R1]; adoption **[std]**, product-spec (22) |
| AMC `c_amc` (UWP) | 1.00% p.a. | **[std]**, product-spec (9) |
| Guarantee/smoothing charge `c_g` | 0.10% p.a. of asset share; lifetime cap: deductions cease once `CumGC ≥ 2% ×` current asset share | cap [S1]; rate and cap mechanics **[std]**, product-spec (10) |
| Interim bonus rate | = last declared regular bonus rate | practice [S1][S7]; equality **[std]**, product-spec (17) |
| MVR scale | derived each year from the formulas below (no tabulated scale) | [S5][S6]; derivation **[std]** |
| EGR (smoothed-fund variation) | 5.0% p.a. | **[std]**, product-spec (25) |
| ProfitShare (mutual variation) | 0 in base | [S6]; base choice **[std]** |

### (c) Behavioral / experience assumptions (modeler's view)

CMI tables issued after 1 March 2013 are subscriber-restricted [R10][REG-R22], so no
current CMI rates can be reproduced here: the reference basis is a **[std]** proxy on
the freely redistributable ONS national life tables [REG-R32] (population mortality
is heavier than insured experience [REG-R32]). AM92/AF92 (published 1999) remain the
canonical assured-lives *shape* reference [REG-R24]; their use in historical
with-profits work is [unverified] convention [R10].

| Input | Recommended basis | Basis tags |
|---|---|---|
| Base mortality | 60% × ONS National Life Tables (UK, 2021–2023) qx, sex-distinct | proxy **[std]**; source [REG-R32]; shape cross-check AM92 [REG-R24] |
| Mortality improvement | CMI_2025 projections model, long-term rate 1.25% p.a. — *named, not reproduced* (subscriber-restricted) | model existence [REG-R30]; LTR choice **[std]** |
| Base surrender rate — UWP bond | 5% p.a. flat | **[std]** |
| Base lapse rate — CWP endowment | 5% yr 1, 4% yr 2, 3% yr 3, 2% yrs 4+ | **[std]** |
| Dynamic surrender multipliers | see Policyholder behavior modeling | **[std]** |
| Paid-up conversion (CWP) | excluded from base model; flag for extension | option exists [S4]; exclusion **[std]** |
| Maintenance expense | £30 per policy p.a., inflating 3.0% p.a. | **[std]** |
| Fund return `r(t)` | 5.0% p.a. deterministic base scenario, net of dealing costs [S5]; net of life-fund tax for `tax_basis = life_net` cells [S1][REG-R17] | scenario level **[std]** |
| GAO take-up (legacy flag) | 90% when in-the-money by >10%, else 30% | **[std]** [unverified — no public experience retrieved] |

Deterministic single-scenario projection is the base; the cost of guarantees requires
stochastic valuation (see Cash flow components, cost-of-guarantees note).

---

## Cash flow components and recursions

### Notation (defined once, used throughout)

| Symbol | Meaning |
|---|---|
| `t` | policy year index (1, 2, …); `x` = age at entry (ANB) |
| `P(t)` | premium received at BOY t |
| `W(t)` | partial withdrawals paid at BOY t |
| `E(t)` | insurer maintenance expense in year t (£30 × 1.03^(t−1) **[std]**) |
| `r(t)` | earned fund return in year t (net basis per `tax_basis`) |
| `c_amc`, `c_g` | AMC 1.00% p.a.; guarantee/smoothing charge 0.10% p.a. **[std]** |
| `q(x+t−1)` | mortality rate for year t (class (c) basis) |
| `w(t)` | surrender/lapse rate for year t (incl. dynamic multipliers) |
| `MC(t)` | mortality charge to the asset share in year t [S1] |
| `b(t)`, `b_rev(t)` | declared regular / reversionary bonus rate for year t |
| `Q(t)`, `U(t)`, `FV(t)` | unit price, units, face value (UWP); `FV = U·Q` |
| `G(t)` | guaranteed benefit (CWP): SA + attaching bonuses |
| `S(t)` | smoothed target payout after cap and corridor |
| `FB(t)`, `MVR(t)`, `TB(t)` | final bonus, market value reduction, terminal bonus |
| `CB(t)`, `ST(t)` | cost of bonus; shareholder transfer = CB/9 |
| `θ, κ, σ` | guarantee-fill target 0.80; bonus-smoothing speed 0.5; y/y cap 10% **[std]** |
| `g_db` | UWP death benefit factor 1.01 **[std]** |
| `i_sv` | CWP surrender-basis discount rate 4.0% **[std]**; `v_sv = 1/(1+i_sv)` |
| `n` | CWP term (25); `h` = UWP bonus-setting horizon (10 years **[std]**) |
| `l(t)` | in-force probability at end of year t; `l(0) = 1` |

### Annual processing order [std]

1. **BOY**: premium `P(t)` received; UWP units purchased: `U(t) = U(t−1) + α·P(t)/Q(t−1)`
   with allocation `α = 100%` (product-spec (7)).
2. **BOY**: partial withdrawals `W(t)` paid (MVR applies if outside the MVR-free
   allowance); asset share reduced pro rata to the pre-MVR policy value [S1].
3. Fund return `r(t)` accrues on the asset share balance.
4. **EOY**: proportional charges: multiply by `(1 − c_amc − c_g)`; accumulate
   `CumGC`; set `c_g = 0` once `CumGC ≥ 2% × AS(t)` [S1 cap; mechanics **[std]**].
5. **EOY**: regular bonus `b(t)` declared per the setting rule below;
   `Q(t) = Q(t−1)(1+b(t))` (UWP) or `G(t) = G(t−1)(1+b_rev(t))` (CWP);
   cost of bonus `CB(t)` computed on pre-declaration values; shareholder transfer
   `ST(t) = CB(t)/9` deducted from the asset share [S5][R8]; product-spec (2).
6. **EOY**: mortality charge `MC(t) = q(x+t−1) · max(0, DB_g(t) − AS_pre(t))`
   deducted, where `DB_g` is the guaranteed death benefit (`g_db·FV(t)` UWP; `G(t)`
   CWP) and `AS_pre` the balance after step 5 [S1 formula: mortality rate × (death
   benefit − policy value); guaranteed-only DB in the sum at risk **[std]**].
7. **EOY**: smoothed payout `S(t)` computed (cap, then corridor); `FB`/`TB`/`MVR`
   derived.
8. **EOY**: claims paid — deaths at `q`, surrenders at `w`, maturity at `t = n`;
   smoothing account posts `(payout − AS(t))` per exiting unit of probability.
9. Survivorship: `l(t) = l(t−1) · (1 − q(x+t−1)) · (1 − w(t))` (maturity year:
   survivors mature).

### Asset share recursion (core)

```
AS(t) = [ AS(t−1) + P(t) − W_AS(t) ] · (1 + r(t)) · (1 − c_amc − c_g)
        − ST(t) − MC(t) + M(t)
```

Component bases (each item as recorded for the retrospective accumulation
[S1][S2][S4][S5][S6][S7] and codified in PRA Surplus Funds 3.3 [R8]):

- **Premiums `P(t)`** — accumulated in full; explicit charges are taken via `c_amc`
  rather than allocation deductions **[std]** (product-spec (7)).
- **`W_AS(t)`** — asset-share reduction for BOY withdrawals, pro rata to the pre-MVR
  policy value [S1].
- **Investment return `r(t)`** — actual return on the backing asset pool including
  unrealised gains [S1][S5][R8]; net of dealing costs [S5]; net of life-fund tax for
  BLAGAB cells, gross for pensions [S1][S2][REG-R17]; asset shares are not credited
  with return earned on the estate [S1][S2].
- **Expenses/charges `c_amc`** — percentage-of-asset-share expense charge; observed
  1% caps [S1][S5]; excess actual expenses over charges fall to the estate [S1].
- **Cost of guarantees and smoothing `c_g`** — deduction from credited return
  [S1][S4][S6]; lifetime cap 2% of asset shares [S1].
- **Shareholder transfer `ST(t)`** — charged to asset shares [S5][R8]; one-ninth
  formulation **[std]** (product-spec (2)).
- **Mortality charge `MC(t)`** — rate × sum at risk; actual-vs-charged differences
  accrue to the estate [S1].
- **Miscellaneous surplus / estate distributions `M(t)`** — allocated annually where
  applicable [S1][S5][R8]; `M(t) = 0` in the base model **[std]** (product-spec (3)).

### Regular bonus setting rule [std]

The PPFM principles are: rates set from projections; gradual changes (±1% p.a.
normal); keep a substantial proportion of the payout in final-bonus form; full
discretion to declare zero [S1][S7]. The reference parametrization:

1. Project the asset share to the horizon at the expected net return
   `r_e = r_base − c_amc − c_g` **[std]**:
   `AS_proj = AS(t) · (1+r_e)^(m) + future premiums accumulated to the horizon at r_e`,
   with `m = n − t` (CWP) or `m = h = 10` (UWP whole-of-life bond).
2. Supportable rate: the level bonus rate that grows the guarantee to the
   guarantee-fill target θ = 80% of the projected asset share:
   - UWP: `b_supp = [ θ·AS_proj / FV(t) ]^(1/m) − 1`
   - CWP: `b_supp = [ θ·AS_proj / G(t) ]^(1/m) − 1`
3. Smoothed declaration with the ±1% discipline [S1][S7]:
   `b(t) = max( 0, b(t−1) + clamp( κ·(b_supp − b(t−1)), −0.01, +0.01 ) )`, κ = 0.5
   **[std]**.

The base projection holds the snapshot rates (2.00% UWP / 1.50% CWP) level; the rule
above is the revision module for scenario work.

### Smoothed payout, final bonus, terminal bonus

Raw target = the unsmoothed asset share (payout target 100% of asset share
[S5][S7][S8][R1]). Apply the year-on-year cap, then the corridor:

```
S_raw(t)  = AS(t)
S_cap(t)  = clamp( S_raw(t), (1−σ)·S(t−1), (1+σ)·S(t−1) )      σ = 10%  [S1]
S(t)      = clamp( S_cap(t), 0.80·AS(t), 1.20·AS(t) )                    [S1][R1]
```

The corridor implements the 80–120% target range deterministically at model-point
level; the ≥90%-of-policies test [S1][R1] is a portfolio property, out of scope for a
single-policy model **[std]**.

- UWP final bonus: `FB(t) = max(0, S(t) − FV(t))`; guarantee-event payout
  `FV(t) + FB(t)`; death payout `g_db · (FV(t) + FB(t))` [S5: no MVR on death].
- CWP terminal bonus: `TB(t) = max(0, S(t) − G(t))`; maturity payout `G(n) + TB(n)`;
  death payout `G(t) + interim accrual + FB per the same scale` [S1][S4][S8].
- When the guarantee bites (`S(t) < FV(t)` or `S(t) < G(t)`), the excess of the
  guaranteed payout over the asset share is charged to the smoothing/guarantee
  account within the estate [S1][S4].

### MVR (unitised, non-guaranteed exits)

```
MVR(t) = min( max(0, FV(t) − S(t)),  max(0, FV(t) − AS(t)) )
Surrender payout = FV(t) + FB(t) − MVR(t)
```

The first argument recovers the smoothed-payout shortfall below face value (post-MVR
payouts target 100% of asset share, here its smoothed image [S5]); the second is the
COBS 20.2.16R bound — the MVR may not exceed the excess of unit value over the
underlying asset value [R1]. Because `FB > 0` requires `S > FV` and `MVR > 0`
requires `S < FV`, final bonus and MVR are never simultaneous (observed Phoenix WPF
rule [S4]; adoption product-spec (24)). MVR-free events: death [S5], guarantee dates
[S4][S5], withdrawals within the 5% allowance **[std]** (product-spec (13)).

### Cost of bonus and shareholder transfer (90:10 mechanics)

`ST(t) = CB(t) / 9` — one-ninth of the cost of bonus, so that shareholders receive
10% of each 90:10 distribution (product-spec (2); components [S1][S5][S8][R1]).
Measurement of `CB` **[std]**:

- UWP regular bonus: `CB_reg(t) = b(t) · FV(t−1)` — the face-value uplift delivered
  by the declaration.
- CWP reversionary bonus: `CB_reg(t) = ΔG(t) · v_sv^(n−t)` with
  `ΔG(t) = G(t) − G(t−1)` — the declared addition discounted to the declaration date
  (survivorship discount omitted **[std]** simplification).
- Final/terminal bonus: `CB_fb(t) = (FB or TB paid on claims in year t)`, recognized
  at payment.

`ST` is a cash outflow from the fund (distribution to shareholders), reported
separately in the model output; per COBS 20.2.17AR, adjustments reducing policyholder
distributions below the required percentage require proportionate
shareholder-transfer reductions [R1] — modeled
implicitly by tying `ST` to actually-declared/paid bonus.

### Smoothing account

On each exit, post the smoothing cost `(payout − AS(t))` weighted by the exiting
probability to `SM(t)` (within the estate). Intended broadly neutral over time
[S1][S2][S5][S6]; the base model tracks the balance without recycling. Optional
module: Aviva-style year-end recycling into credited returns (maximum deduction
currently 2.5% of asset shares p.a.) [S5].

### Cost of guarantees — cited, not specified

The deterministic charge `c_g` is a *charging* proxy, not a valuation. The economic
cost of the guarantees (unit-price floor, guarantee-date face value, CWP sum assured
plus hardened bonuses, GAO) requires stochastic market-consistent valuation: PRA
Technical Provisions 9.2 requires guarantees and options to be valued with realistic
dynamic assumptions [R7], and the canonical methodology is market-consistent
stochastic simulation of the bonus/smoothing/MVR rules (Hibbert & Turnbull 2003; Hare
et al. 2000 [R13]). This model produces the per-scenario cash flows such a valuation
consumes; the stochastic layer itself is out of scope.

### GAO module (legacy flag)

Where `gao_flag` is set (CWP pension cells), the retirement benefit is
`max( CashFund(T) · OMR(T), CashFund(T) · gao_rate )` — the guaranteed annuity rate
floors the open-market conversion. GAOs are present in several closed funds, backed
by fixed-interest assets, with interest-rate risk identified as a fund business risk
[S4]; the Equitable Life history is [unverified] context. `gao_rate` = £0.09 p.a. per
£1 of cash fund **[std]** [unverified as typical]; take-up per class (c). The GAO is
a valuation-critical option (stochastic interest-rate exposure) — cited, not
fully specified.

### Cash flow outputs (per policy year t, probability-weighted by `l`)

| Output | Formula |
|---|---|
| Premium income | `P(t) · l(t−1)` |
| Death claims | `q(x+t−1) · l(t−1) · DeathPayout(t)` |
| Surrender claims | `w(t) · l(t−1) · (1 − q) · SurrenderPayout(t)` |
| Maturity claims | `l(n) · (G(n) + TB(n))` (CWP, year n) |
| Partial withdrawals | `W(t) · l(t−1)` |
| Maintenance expenses | `E(t) · l(t−1)` |
| Shareholder transfers | `ST(t) · l(t−1)` plus `CB_fb/9` on claims |

---

## Policyholder behavior modeling

All dynamic formulas are **[std]** — no public UK with-profits lapse experience was
retrieved; the shapes are rationalized from the product's incentive structure, and
dynamic option-exercise modeling is a regulatory expectation for the BEL [R7].

- **Base surrender**: UWP bond 5% p.a. flat; CWP 5%/4%/3%/2%+ (class (c) table).
- **MVR deterrent**: `w(t) = w_base(t) · 0.6` while `MVR(t) > 0` **[std]** — an
  active MVR penalizes exit, and firms may consider exit volumes in setting MVRs
  within the COBS bound [R1 COBS 20.2.16AR].
- **Guarantee-date spike**: `w(t) = w_base(t) · 2.5` in a guarantee-date year
  **[std]** — MVR-free encashment is rationally exercised when `FV(t) > AS(t)`
  (guarantee in the money); apply the multiplier only in that state.
- **Guarantee-imminent suppression**: `w(t) = w_base(t) · 0.8` in the year before a
  guarantee date **[std]** (waiting for the MVR-free window).
- **Withdrawal utilisation**: withdrawing bond cells take the full 5%
  MVR-free/tax-deferred allowance; utilisation 30% of policies **[std]**
  (allowance context [S10][REG-R15]).
- **GAO take-up**: 90% when in-the-money by >10%, else 30% **[std]** [unverified].
- **Paid-up conversion (CWP)**: excluded from base **[std]**; where modeled, benefits
  reduce per policy terms and future bonuses may or may not accrue [S4], and asset
  shares may need separate treatment for altered policies [S6].

---

## Worked example

Anchor UWP bond cell (product-spec (14)): £25,000 single premium; `U = 25,000`
units at `Q(0) = £1.0000`; five declarations at 2.00% give
`Q(5) = 1.02^5 = 1.104081`, `FV(5) = £27,602.02`. Worked-example state **[std]**:
`AS(5) = £30,000.00`, `S(5) = £29,500.00`. Year-6 parameters: `c_amc = 1.00%`,
`c_g = 0.10%`, `q(60) = 0.005` (illustrative of the class (c) proxy **[std]**),
`g_db = 1.01`, `σ = 10%`. No premium, no withdrawals in year 6. Two return
scenarios **[std]**: A: `r = +7.0%`; B: `r = −15.0%` (declared bonus cut to 1.00%,
the maximum normal reduction [S1][S7]).

| Step | Quantity | Scenario A (r = +7.0%) | Scenario B (r = −15.0%) |
|---|---|---|---|
| 0 | `AS(5)` / `FV(5)` | 30,000.00 / 27,602.02 | 30,000.00 / 27,602.02 |
| 3 | After fund return: `30,000 · (1+r)` | 32,100.00 | 25,500.00 |
| 4 | After charges `× (1 − 0.011)` | 31,746.90 | 25,219.50 |
| 5 | Declared bonus `b(6)` | 2.00% | 1.00% |
| 5 | `Q(6)`; `FV(6) = 25,000 · Q(6)` | 1.126162; 28,154.06 | 1.115122; 27,878.04 |
| 5 | Cost of bonus `CB = b(6) · FV(5)` | 552.04 | 276.02 |
| 5 | Shareholder transfer `ST = CB/9` | 61.34 | 30.67 |
| 5 | Asset share after `ST` | 31,685.56 | 25,188.83 |
| 6 | `MC = q · max(0, 1.01·FV(6) − AS)` | 0.00 | 0.005 × 2,967.99 = 14.84 |
| 6 | **`AS(6)`** | **31,685.56** | **25,173.99** |
| 7 | `S_cap`: clamp(AS, 0.9·29,500, 1.1·29,500) | 31,685.56 (within) | 26,550.00 (floor binds) |
| 7 | `S(6)`: corridor clamp to [0.8, 1.2]·AS | 31,685.56 | 26,550.00 (within corridor) |
| 7 | Final bonus `FB = max(0, S − FV)` | 3,531.50 | 0.00 |
| 7 | `MVR = min(max(0, FV−S), max(0, FV−AS))` | 0.00 | min(1,328.04, 2,704.05) = 1,328.04 |
| 8 | Guarantee-date payout `FV + FB` (no MVR) | 31,685.56 | 27,878.04 (guarantee bites) |
| 8 | Surrender payout `FV + FB − MVR` | 31,685.56 | 26,550.00 |
| 8 | Death payout `1.01 · (FV + FB)` | 32,002.42 | 28,156.82 |
| 8 | Smoothing/guarantee cost on exit (payout − AS): guarantee-date / surrender | 0.00 / 0.00 | 2,704.05 / 1,376.01 |

Checks: scenario B surrender pays exactly the smoothed target (−10.0% y/y, the [S1]
cap); the MVR (1,328.04) is below the COBS bound `FV − AS = 2,704.05` [R1]; the
guarantee-date exit pays full face value with the 2,704.05 excess over asset share
borne by the estate's guarantee/smoothing account [S1][S4]. On the scenario A
guarantee-date claim an additional shareholder transfer of `FB/9 = 392.39` accrues at
payment (90:10 on the final bonus, ST section). Scenario A pays 100.0% of `AS(6)`;
scenario B's surrender pays 105.5% of `AS(6)` — both within the 80–120% corridor
[S1][R1].

CWP maturity illustration (one line): at `n = 25`, `G(25) = 20,000 · 1.015^25 =
£29,018.91`; with smoothed maturity target `S(25) = £34,000.00` **[std]**,
`TB = 34,000.00 − 29,018.91 = £4,981.09` — 14.7% of the payout in non-guaranteed
form, consistent with the substantial-final-bonus philosophy [S1]; the associated
shareholder transfer at payment is `TB/9 = £553.45` **[std]** measurement.

---

## Statutory accounting and capital

Framework and the shared model-output contract are in
`uk/regulatory/statutory-accounting-and-capital.md` and `uk/regulatory/technical-notes.md`;
this section states only what is specific to the composite with-profits fund defined in
`product-spec.md`. [REG-R#] resolves against the shared UK numbering used throughout
`uk/references/regulatory-and-actuarial-references.md`, which now runs **R1–R120**, with
**R50–R52, R74–R76 and R121–R133 unused by design** — the research streams were allocated
parallel blocks and the tails left spare, so an unused number is not a missing entry. [S#] and
[R#] continue to resolve against `sources.md` in this directory.

**The file name is structural parity, not a claim about UK practice.** There is no "statutory
accounting" in the U.S. sense here. A UK with-profits writer runs three separate measurements off
one projection: the **Solvency UK regulatory balance sheet** (PRA Rulebook — the prudential
measurement, a supervisory return and not a set of accounts) [REG-R39][REG-R1]; the **statutory
accounts** under FRS 102 + FRS 103 or UK-adopted IFRS 17 [REG-R99][REG-R105][REG-R106]; and
**tax**, which is not a liability measurement at all but is computed from the accounts with the
Finance Act 2012 overlay [REG-R17][REG-R18]. Where this section says "the accounts" it means the
second; "Solvency UK" means the first.

### Contract classification and reporting

- **RAO class.** Conventional with-profits assurances and annuities are **Class I** (life and
  annuity) long-term business; unitised/linked structures typically involve **Class III** (linked
  long term) [REG-R14; per-product allocation [unverified], as recorded in `product-spec.md`] —
  the same instrument the product documents cite locally as [R9]. The class matters exactly once
  in the capital calculation: the **70% mass-lapse limb** reaches Regulated Activities Order
  Schedule 1 Part II **class VII (pension fund management) only** after the PRA's 20 December 2024
  correction, effective 31 December 2024, so **no cell of this composite takes it and the 40% limb
  applies** [REG-R62][REG-R64].
- **Solvency UK line of business: 30, insurance with profit participation.** Segmentation is into
  homogeneous risk groups and, as a minimum, by the Annex 1 lines (TP 10.1), with assignment
  reflecting **the nature of the risks — the legal form is not necessarily determinative**
  (TPFR 26.2) [REG-R1][REG-R41]. **Annex 1 names no products**: the library's mapping of this
  product onto LoB 30 is the research's inference from TPFR 26.2/26.3 and the Annex 1 definitions,
  not a quotation [REG-R41]. IR.12.01 repeats the same rule in template language — segmentation
  "shall reflect the nature of the risks underlying the contract (**substance**), rather than the
  legal form of the contract (**form**)" [REG-R89].
- **PRA three-digit product codes for IR.14.01** [REG-R89]. Chassis A (unitised with-profits bond)
  reports under **111**, single-premium bond UWP. Chassis B (conventional endowment) reports under
  **120** (endowment, ordinary branch, CWP), its unitised sibling under **121**; **100 / 101** are
  the whole-of-life CWP / UWP codes and **200 / 201, 210 / 211** the participating-pension codes
  that the `gao_flag` cells would use. Two verified conventions decide chassis A: "single premium
  bond" **includes 'investment bond' and 'with-profits bond'**, and the whole-life and endowment
  codes **exclude single premium bonds "which are technically whole of life"** — so this
  whole-of-life bond reports under 111 and *not* under a whole-of-life code [REG-R89]. IR.14.01
  requires contract counts, new contracts, written premiums, claims paid, best estimate and
  **capital at risk** per code, and "all insurance contracts shall be reported even if classified
  as investment contract on accounting basis" [REG-R89]. Where technical provisions are computed
  for a combination of products the instruction's **own worked example is with-profits guarantee
  costs**, and firms "should use an **approximation to apportion**" between product codes
  [REG-R89] — which is the reporting layer conceding that this model's fund-level guarantee and
  smoothing costs cannot be attributed to a product code exactly.
- **IR.12.01 — column C0010, and the unit-linked rows are not this product's.** With-profits
  business reports in **C0010, insurance with profit participation**; rows **R0300 surrender
  value, R0302 nominal value of units and R0304 matching value of units are C0020 (index-linked
  and unit-linked) only** [REG-R89]. Despite the unit vocabulary of chassis A — `U(t)`, `Q(t)`,
  `FV(t)` — a with-profits unit is not a linked benefit, and none of those three rows is due for
  it. Because the PRA expects each with-profits fund to be a ring-fenced fund, the per-fund
  **IRR.12.01** (rows R0025–R0030, R0080–R0100, R0140–R0200) is also due, with a fund number that
  must stay consistent over time and across templates [REG-R89][REG-R71].
- **IR.12.04 — the assumption rows this product owns.** Triggered where gross BEL for long-term
  business other than reinsurance exceeds **£50 million** or gross written premiums exceed
  **£10 million**; its purpose is to show **changes in the valuation basis, how the basis compares
  with experience and the variability of recent experience**, so it wants the current-year basis,
  the prior-year basis and **five years of the firm's own experience**, with a credibility
  guideline of **200 claims per annum** for a line [REG-R89]. This product's own rows: **R0730**
  lapse/surrender, with-profits endowment years 11+ (chassis B); **R1810** per-policy renewal
  management expense unit cost, with-profits endowment; **R1970** the same for a with-profits
  individual pension; and **R1250 guaranteed annuity rate take-up** — "proportion of policyholders
  taking the guaranteed annuity rate which is in the money" — which is the reporting home of the
  GAO take-up assumption that these notes carry as **[std]** and **[unverified]** (no public
  experience retrieved). The bond's `w(t)` and 5% withdrawal utilisation belong naturally in the
  **investment bond** rows R1050 / R1090 / R1130 (years 1–5 / 6–10 / 11+, "including both part
  surrenders and full surrenders"), but **the IR.12.04 instruction does not say whether
  "investment bond" carries the IR.14.01 convention that a single-premium bond includes a
  with-profits bond, so which row chassis A's surrenders belong in is not settled by the retrieved
  instructions** [REG-R89]. Column **C0080 requires the named underlying table** ("e.g. AM92",
  with "adjusted" appended where the percentage varies by age) and, where the CMI Mortality
  Projections Model is used, a description "consistent with latest guidance from the CMI"
  [REG-R89] — which the **[std]** 60%-of-ONS proxy in the class (c) table above cannot supply
  honestly, the CMI material being subscriber-restricted [R10][REG-R22].
- **IR.12.05 and IR.12.06 — the two templates that exist for this product and no other.**
  Triggered where **net BEL for with-profits business exceeds £500 million**, completed for the
  whole firm where the firm *is* a single with-profits fund and otherwise **per ring-fenced fund
  which is also a with-profits fund**, plus the remaining part where that is a with-profits fund
  [REG-R84][REG-R90].

  *IR.12.05, value of bonus* [REG-R90]: **R0010** bonuses added at date of claim (interim, terminal
  or final) — the model's `FB`/`TB` at payment; **R0020 clawback of past bonuses, which is where
  market value reductions go, shown as a negative amount** — the model's `MVR(t)`; **R0030** cash
  bonuses; **R0040 reversionary bonuses, as a discounted value "calculated in accordance with
  COBS 20.2.17R"** — the model's `ΔG(t)`; **R0050** other. Then **R0080** shareholder proportion
  ("e.g. 10.00%") and the stated formula
  `R0090/C0050 = R0060/C0040 × R0080/C0050 / (1 − R0080/C0050)`, i.e.
  `shareholder transfer = policyholder value of bonus × s/(1 − s)`, which for a 90:10 fund with
  `s = 0.10` is **one ninth** [REG-R90]. **That is regulatory corroboration of the one-ninth rule
  this library carried as a pure arithmetic restatement of 90:10** (product-spec (2)); the
  instruction also records that "most with-profits funds are either '90:10' … or '100:0'". Two
  mismatches with the model remain: the template measures the transfer on the **decomposed value of
  bonus**, whereas `CB(t)` here is measured as `b(t)·FV(t−1)` on the unitised leg and
  `ΔG(t)·v_sv^(n−t)` at `i_sv = 4.0%` with survivorship omitted on the conventional leg — both
  **[std]**, and **COBS 20.2.17R itself could not be re-fetched in this effort** (one attempt
  returned HTTP 500, another returned COBS 20.3 content), so the required discounting basis is
  **named, not specified** [REG-R9][REG-R90]; and rows **R0100–R0120** carry shareholder transfers
  **deferred from previous years** ("for example due to restrictions relating to capital position
  of the fund"), a deferral mechanism the base model does not have — it transfers `ST(t)` in full
  each year **[std]**.

  *IR.12.06, with-profits liabilities and assets* [REG-R90][REG-R45]: this is where the model's
  state variables land. **R0010** with-profits benefits reserve, which "corresponds to
  with-profits policy liabilities … in **Surplus Funds 3.2**"; **R0020 asset shares calculated
  retrospectively in accordance with Surplus Funds 3.3** — `AS(t)`; **R0050** prospective reserve
  where asset shares are not applicable (Surplus Funds 3.4); **R0030 / R0040** past and
  valuation-date miscellaneous surplus that is **permanent**, with **provisional allocations
  excluded** — the model's `M(t)`, zero in the base run **[std]** (product-spec (3)); **R0070
  future cost of contractual guarantees, which "cannot be negative"** — the unit-price floor, the
  10th-anniversary face value and the CWP guaranteed benefit stack; **R0090 future costs of
  financial options "such as guaranteed annuity rates"** — the `gao_flag` cells; **R0100 future
  costs of smoothing, which "can be negative"** — `SM(t)`; **R0130 planned deductions for
  guarantees, options and smoothing** — `c_g` and its 2%-of-asset-shares lifetime cap; and
  **R0150 = WPBR + FPRL, which must equal IR.12.01.01 R0030/C0010**. Two further rows bear on
  assumptions in these notes: **R0160 overall investment return is post investment costs but
  *pre-tax***, split at **R0170 non-taxable (e.g. pensions)** and **R0180 taxable (e.g.
  endowment)** asset shares — which is exactly the model's `tax_basis` enum, but on a pre-tax
  measurement, so the practice of crediting `r(t)` net of life-fund tax to BLAGAB asset shares
  [S1][S2][REG-R17] needs an explicit reconciliation before it can populate R0160. The asset-mix
  rows (CIC code, split between the assets backing the WPBR and those backing the FPRL) are a
  fund-level output a single-policy model does not produce [REG-R90].
- **IR.05.10 excess capital generation** names **shareholder transfers from with-profits funds** as
  a decomposition line, over one actual and three plan years [REG-R90]. **Its scope test is stated
  inconsistently** — the Rulebook triggers on life premiums excluding unit-linked exceeding £1
  billion in the most recent reporting year, the instruction file on any of the three most recent
  years and including SLT health business — and that conflict is **recorded, not resolved**
  [REG-R84][REG-R90].
- **Not settled by the retrieved instructions, at the point of use.** Whether the UK collects any
  life best-estimate cash-flow projection template at all: **PS3/24 ¶4.70 states that "S.13.01 and
  SR.22.02 will continue to be collected", yet the final Reporting Part contains no IR.13.01 in
  any Article or in the Chapter 9 inventory and the PRA's instruction library holds no `ir1301`
  file** [REG-R86][REG-R84][REG-R88]. And from the **31 December 2026** reference date PS18/26
  **removes claims management expenses from IR.14.01's claims-paid definition**; the replacement
  instruction files were not retrieved [REG-R87].

### Technical provisions

- **The contract boundary is decided by the guarantee, and it keeps future premiums in.** TPFR
  3.5 cuts future premiums out of a contract only where **all three** of no compensation for a
  specified uncertain adverse event, **no financial guarantee of benefits**, and no power to
  compel the premium hold [REG-R41]. **A with-profits contract fails the guarantee limb
  outright**, so chassis B's whole 25-year `£60`-per-month stream sits inside the boundary
  [REG-R41]. On chassis A there are no future premiums for 3.5 to operate on, and top-ups are new
  contracts with their own boundaries [REG-R41][S10]. Neither chassis gives the firm a unilateral
  right to terminate, to reject premiums, or to amend premiums or benefits so that premiums fully
  reflect the risks — **bonus discretion is not a repricing right** — so TPFR 3.3(1)–(3) cut
  nothing, and the long-term individual-underwriting carve-out in 3.3(3) (which pushes the
  assessment from portfolio level to **contract level** where an inception underwriting assessment
  cannot be repeated) is engaged here only in the confirming sense; the framework matrix marks it
  `(x)` for this product [REG-R41]. The boundary and **the limb that produced it** are both
  required outputs [REG-R41].
- **Cash flows in scope — and two that look like cash flows and are not.** TPFR 13.1 lists eight
  streams, each separately identifiable [REG-R41]. Premiums `P(t)`, death, surrender, maturity and
  partial-withdrawal claims, and maintenance expense `E(t)` are ordinary. Two are not:
  - **Policyholder-charged tax is its own stream, item (8)** — "taxation payments which are, or
    are expected to be, charged to policyholders" [REG-R41]. This model nets life-fund tax into
    `r(t)` for `tax_basis = life_net` cells [S1][S2][REG-R17]; that is a *charging* convention for
    the asset share and it collapses an item the best estimate must be able to show separately.
    **Shareholder corporation tax is not a best-estimate cash flow at all** — it enters through
    deferred tax under Valuation 11 [REG-R41][REG-R39].
  - **There is no TPFR 13.1 item for shareholder transfers.** `ST(t)` is not a best-estimate cash
    flow stream: the transfer runs through TP 9.1(3) and the Surplus Funds Part, entering as
    Surplus Funds **3.1(5)**, "the value of future shareholder transfers relating to policies in
    the fund which may properly be made out of it under the FCA Handbook", deducted in arriving at
    surplus funds [REG-R1][REG-R41][REG-R45].
  - **Payments to and from intermediaries are an in-scope stream**, so commission and clawback are
    best-estimate cash flows rather than an expense-loading convention [REG-R41]. The base model
    has **no commission stream** — 100% allocation with an explicit AMC **[std]** (product-spec
    (7)) — which is a known omission against this requirement, not a modelling simplification that
    survives into reporting.
- **Expenses.** The two-expense-bases problem (TPFR 16.4's going-concern basis against the risk
  margin's no-new-business reference undertaking) is generic and is in the framework
  [REG-R41][REG-R1]; the `£30` p.a. inflating 3.0% **[std]** here is a going-concern figure by
  construction. What is product-specific is the asymmetry the model already records: where actual
  expenses exceed the 1% charge cap the excess falls to the estate [S1][S5] — **the best estimate
  needs the actual expense, not the capped charge**, so the charge and the expense are two
  different projected quantities on this product and not one.
- **The best estimate is not normally negative here, and the two research streams disagree about
  how firmly to say so.** Nothing in the Valuation, Technical Provisions or TPFR Parts floors a
  best estimate [REG-R1][REG-R39][REG-R41]. But guaranteed benefits plus future discretionary
  benefits dominate on both chassis — chassis A has no future premium at all and carries a face
  value payable in full at guarantee events, chassis B's guaranteed benefit stack `G(t)` outgrows
  the discounted remaining premium stream from an early duration — and **the estate is carved out
  of technical provisions entirely**, so the framework applicability matrix marks with-profits
  `—` on the no-floor row. **The technical-provisions research stream marked it `(x)`; the
  divergence is recorded, not resolved** [REG-R41][REG-R115].
- **Future discretionary benefits are a separately required output, used four times.** TPFR 10.1:
  "a firm must determine separately the value of future discretionary benefits" [REG-R41]. In this
  model's terms the guaranteed leg is `FV(t)` (chassis A) or `G(t)` (chassis B) and the FDB leg is
  the expected future `b(t)`/`b_rev(t)` declarations plus `FB`/`TB`. The two must be valued
  separately because they are discounted together under TP 9.1(3), **reported separately** at
  IR.12.06, **stressed differently** — SCR-SF 3.3A(1)(c) freezes FDB in the gross run while 6.3
  makes it responsive in the net run — and enter the MCR **with opposite signs**
  [REG-R1][REG-R41][REG-R62][REG-R78].
- **TPFR 9.1 forbids an assumed equity risk premium.** Where FDB depend on the assets held, the
  best estimate must be based on **the assets the firm currently holds**, allocation changes
  assumed only under TPFR 8, and **assumed future asset returns consistent with the relevant
  risk-free curve** and with the Valuation Part measurement of those assets [REG-R41].
  **Consequence for these notes: the 5.0% p.a. fund return is a deterministic scenario level
  [std], not a valuation basis.** A best-estimate run replaces it with risk-neutral returns off
  the PRA-published curve; the observed benchmark equity backing ratio ceiling of 75% [S5] then
  drives the *volatility* of the guarantee cost, never its expected return.
- **The options and guarantees this design actually contains, and why they force a stochastic
  valuation.** The unit-price floor `Q(t) ≥ Q(t−1)`; the MVR-free 10th-anniversary guarantee date
  paying `FV(t) + FB(t)` in full; the CWP guaranteed benefit `G(n)` at maturity and `G(t)` at
  death; the death benefit `g_db·(FV + FB)` with no MVR ever; the 5% p.a. MVR-free withdrawal
  allowance; and, on `gao_flag` cells, the guaranteed annuity option. TP 9.2(1) requires the value
  of financial guarantees and contractual options to be taken into account and 9.2(2) requires
  realistic exercise assumptions reflecting future financial and non-financial conditions
  [REG-R1]; TPFR 19.4–19.5 require the firm to analyse the dependence of the present value on
  **expected future outcomes and on scenario deviation from the expected outcome** and to use a
  method reflecting it [REG-R41]. **With-profits is the only product in this library the framework
  matrix marks `x` — unqualified — on the scenario-dependent-method row** [REG-R41]. Under the
  framework's **[std]** `force_stochastic` gate all four limbs fire here: a benefit is a max/min of
  two quantities (`max(0, S − FV)`; `max(cash·OMR, cash·gao_rate)`); a discretionary benefit
  depends on asset returns; exercise depends on moneyness (the guarantee-date spike); and
  management actions are conditional on market variables. **The deterministic projection specified
  in these notes is therefore a control, not the answer**, and this is the same conclusion the
  "Cost of guarantees — cited, not specified" section reaches from PRA Technical Provisions 9.2
  [R7][R13].
- **Management actions: the PPFM is what makes this product's discretion admissible, and also what
  constrains it.** TPFR 8.1's fifth limb requires account to be taken of **any public indications
  by the firm** as to what it would or would not do, and its fourth forbids assumptions **contrary
  to any obligations towards policyholders** [REG-R41] — a published PPFM is precisely such a
  public indication and such an obligation [REG-R9]. The actions this design must name in the
  board-approved TPFR 8.3 plan are exactly the discretion modelled above: the regular and
  reversionary bonus declarations with the ±1% p.a. discipline; final and terminal bonus setting;
  smoothing (the ±10% y/y cap and the 80–120% corridor); MVR application subject to the contractual
  MVR-free points (10th anniversary, death, the 5% allowance); investment-mix rebalancing,
  constrained by TPFR 9.1 to start from the assets actually held; and the `c_g` charge level with
  its 2% lifetime cap — which is also the Surplus Funds 3.4(3) "planned deductions" reported at
  IR.12.06 R0130 [REG-R41][REG-R45][REG-R90]. The plan must state **the circumstances in which the
  firm may not be able to take each action and how those are reflected in the calculation**, the
  **order** of actions, and (8.4) the **time needed to implement** each and **the expenses it
  causes** [REG-R41] — so the annual declaration cycle [S1][S4][S7] and the observed review buffer
  before an extra MVR review [S4] are implementation-lag inputs, not commentary. The **With-Profits
  Actuary (SMF20a)** must advise the governing body whether the assumptions used to calculate FDB
  within technical provisions **are consistent with the firm's PPFM** [REG-R93][REG-R94][R5].
- **A flat lapse table is not available to this product.** TPFR 11.1 closes: "**the likelihood
  shall only be considered to be independent of the elements referred to in (1) to (4) where there
  is empirical evidence to support such an assumption**" [REG-R41], and for a guarantee-bearing
  contract that evidence will not exist. Every dynamic multiplier in "Policyholder behavior
  modeling" above is **[std]** with no retrieved UK with-profits experience behind it, so the model
  satisfies the *form* of TPFR 11.1 and not its evidential requirement — an open gap, not a solved
  one.
- **Grouping is not the specimen-policy convention.** TPFR 20.1 permits grouping only where it
  gives approximately the same result as a per-policy calculation "**in particular in relation to
  financial guarantees and contractual options**", with **no tolerance or test statistic given in
  any retrieved source** [REG-R41]. The specimen-policy convention used for asset shares
  [S1][S4][S5][R1 COBS 20.2.5R(2)] is a *fairness* convention and is not automatically compliant —
  the guarantee-date cohort in particular cannot be pooled with a cohort past its guarantee date.
- **Matching adjustment: the eligible-element route only, and only for the annuity forms.** MA 1.2
  defines an *eligible element* to include **the guaranteed element of a with-profits immediate or
  deferred annuity**, separately organisable and manageable, and MA 2.3 forbids splitting a
  contract's obligations other than for an eligible element [REG-R2]. The "**no future premium
  payments**" condition in MA 2.2(1) is **disapplied only for the in-payment limb** by 2.5 —
  **not** for the with-profits guaranteed annuity element, which must still be premium-free
  [REG-R2]. SS7/18 adds that the PRA expects a detailed assessment that **only contractually
  guaranteed elements** are included and are not dependent on future premiums or investment
  performance, plus **a clear policy on where future attaching bonuses go** [REG-R8]. So this
  route reaches the with-profits deferred-annuity form and the `gao_flag` cells, **not the two
  composite chassis**. And the crux for a with-profits model is unresolved: **how a firm allocates
  a single liability cash flow vector between MA and non-MA portfolios when only an eligible
  element qualifies is not prescribed by any retrieved source — the sources do not say how the
  asset share follows the guaranteed element** [REG-R8]. Where an element is placed in an MA
  portfolio, the **5% mortality-risk cap** in MA 2.2(3) and the annual attestation (no later than
  **14 weeks** after financial year-end) attach to it [REG-R2][REG-R8].
- **Transitionals — and a correction to the wording this file previously carried.** The
  applicability matrix marks both TMTP and TMIR `x` for with-profits [REG-R3][REG-R57]. They are
  keyed to **different dates**, and the pointer list below previously said "TMTP may apply to
  pre-2016 back-books", which describes TMIR's admissibility test rather than TMTP's. **TMTP**
  requires a permission, reaches obligations that were the firm's *qualifying* obligations on
  **31 December 2024** (or assumed later through a transfer event), and **must not be applied after
  1 January 2032** [REG-R3]. **TMIR** applies only to contracts concluded **before 1 January 2016**
  whose technical provisions were determined under INSPRU 1.1.16R as at 31 December 2015 and which
  are not subject to an MA permission, and a firm applying TMTP **must not** apply it [REG-R57].
  The legacy conventional block is the natural carrier of either; **its size is a firm fact this
  library does not have**.

### The risk margin

The formula, the 4% cost-of-capital rate, the λ = 0.9 taper floored at 0.25 and the reference
undertaking's thirteen assumptions are in `uk/regulatory/technical-notes.md`, "The risk margin"
[REG-R1][REG-R4][REG-R44]. Four things change for this product and nothing else does.

- **The FDB loss-absorbency carries into the reference undertaking; the deferred-tax absorbency
  does not.** TP 4B.1 gives the reference undertaking loss-absorbing capacity of technical
  provisions **matching the firm's, per risk**, and **no** loss-absorbing capacity of deferred
  taxes [REG-R1]. For a participating fund that is the single largest product-specific fact about
  the risk margin: the same FDB responsiveness that produces `Adj_TP` on the balance sheet also
  suppresses `SCR(t)` inside the risk margin. **No retrieved source quantifies the effect and none
  is asserted here.**
- **The runoff shape is the taper's, not the product's.** Chassis A is whole-of-life with no
  maturity date (product-spec (5)), so `SCR(t)` runs off only by decrement at the **[std]** 5% p.a.
  base surrender rate — a long tail over which `max(0.9^t, 0.25)` sits at its floor for most of the
  projection. **The `t = 14` threshold at which the taper stops decaying is derived arithmetic,
  recorded as such in `uk/regulatory/technical-notes.md`, "The risk margin"; it appears in no
  retrieved source and must never be cited to [REG-R1], [REG-R4] or [REG-R44].**
- **Surplus funds carry no risk margin, so the estate is not `fund assets − technical
  provisions`.** SS13/15 ¶2.4: the surplus-funds calculation "does not refer to or include a risk
  margin", which the firm must nevertheless hold on the business as a whole — **surplus funds and
  technical provisions are not a clean partition of the with-profits fund** [REG-R46]. A model that
  derives the estate as a residual after technical provisions is wrong by the risk margin.
- **Allocation to LoB 30 is a methodology choice.** The risk margin is calculated for the **whole
  portfolio** and then allocated to lines of business so as to "adequately reflect the
  contributions of the lines of business to the reference undertaking notional SCR over the
  lifetime of the whole portfolio" (TP 4A.3) — **no allocation formula is prescribed** [REG-R1],
  yet IR.12.01 C0010 R0100 needs a LoB 30 number. Two further gaps bite here: the reference
  undertaking selects assets to **minimise its market-risk notional SCR** [REG-R1], which pulls
  against TPFR 9.1's requirement that FDB be projected off the assets actually held [REG-R41], and
  the IR.12.01 instruction permits **SS8/24 §3.2** to be applied to calculate the risk margin
  during the financial year — **SS8/24 was not retrieved and its title is not asserted** [REG-R89].

### SCR — the modules that bite

**With-profits is the product that forces the two-run architecture, and the only one in this
library that does** [REG-R62]. A firm with no future discretionary benefits has `BSCR = nBSCR` and
`Adj_TP = 0`; here `BSCR − nBSCR` is a complete second pass of the liability model. Every stress
size, correlation matrix and simplification is in `uk/regulatory/technical-notes.md`, "The standard
formula SCR"; what follows is which of them reach this product, and how.

| Sub-module | Reaches this product? | Product-specific note |
|---|---|---|
| Mortality `3B1` (**+15%** relative, permanent) | Yes, full revaluation | Bites the CWP sum at risk `G(t) − AS(t)`; on chassis A only through `g_db·(FV + FB) − AS` (≈1% plus any guarantee excess). Applies **only to policies where the stress increases TP without the risk margin** [REG-R62] |
| Longevity `3B2` (**−20%**) | `(x)` | Not a driver for either chassis; with-profits funds commonly contain annuity liabilities and deferred annuities with GAOs [S4], which is what earns the mark [REG-R62] |
| Disability-morbidity `3B3`, revision `3B5` | Revision nil; `3B3` not engaged | `3B5`'s **+3%** reaches only annuity benefits that could increase from legal-environment or state-of-health changes; neither chassis has such a right [REG-R62] |
| Life expense `3B4` (**+10%** to amounts, **+1 percentage point** to expense inflation) | Yes, full revaluation | Applies to `E(t)` and to the 3.0% **[std]** inflation assumption [REG-R62] |
| Life catastrophe `3B7.1` (**+0.15 percentage points** absolute, year 1 only) | Yes, full revaluation | Same TP-increasing filter as mortality [REG-R62] |
| **Life lapse `3B6` — highest of up, down and mass** | Yes, **three revaluations**, and the direction splits by cell (below) | **No simplification exists for mass lapse** [REG-R62] |
| Interest rate `3D5` / `3D6` | Yes, **twice** | Higher of the up and down totals, summed within a direction across currencies; the up shock carries a **1 percentage point absolute floor**, the down shock has none and is **nil for negative basic rates**; the down table is **non-monotonic at maturities 14–20 and that shape is [unverified]** as a possible extraction artefact [REG-R62]. The GAO cells key off the down scenario |
| Equity `3D9` (**39% + SA** type 1, **49% + SA** type 2; **22%** strategic and qualifying long-term equity) | Yes — and it is **a liability revaluation, not only an asset hit** | The dominant module here: a fall cuts asset shares, cuts FDB and raises guarantee cost simultaneously, and the observed benchmark EBR ceiling is **75%** [S5]. The symmetric adjustment is bounded **±10%**, but **no SAECC value appears anywhere in this library — the PRA's monthly spreadsheet was not retrieved** [REG-R62][REG-R54] |
| Property `3D15` (**−25%**) | Yes, same treatment as equity | [REG-R62] |
| Spread `3D17` | Assets only | `3D25`, which recomputes the matching adjustment, reaches only an **eligible element actually placed in an MA portfolio** — `(x)`, and never the composite chassis [REG-R62] |
| Counterparty default `3E`, concentration, currency | Factor-based | `(x)`; the composite specifies no reinsurance [REG-R62] |
| Operational — `Op_provisions` **0.45%** leg | **Yes** | The leg is `0.45% × max(0, TP_life − TP_life-ul)`. **With-profits technical provisions are not unit-linked technical provisions**, so chassis A's "units" do not remove them from it [REG-R62] |
| Operational — `0.25 × Exp_ul` leg | `(x)` | Only where unit-linked business is written alongside in the same entity [REG-R62] |
| **Health module `3C` in its entirety** | **No** | The health module does not reach this product on any row — no NSLT factor model, no health revision, no health catastrophe [REG-R62] |
| **LACTP `Adj_TP`** | **Yes — the only product here where it is unqualified** | Below |
| LACDT `Adj_DT` | Yes | Below |
| **Ring-fenced fund notional SCRs** | **Yes — the whole exercise, per fund** | Below |

**Lapse direction — the classic error, and this design's answer.** `3B6.2` (exercise rates **×1.5**,
capped at 100%) applies **only where exercise increases** technical provisions without the risk
margin; `3B6.3` (**×0.5**, the decrease capped at 20 percentage points) applies **only where
exercise decreases** them; the charge is the **highest of up, down and mass** [REG-R62]. The
routing statistic is *surrender strain*, defined at `7.12(3)` as (amount currently payable on
discontinuance, net of amounts recoverable from policyholders or intermediaries) − (technical
provisions without the risk margin), **signed, per policy** [REG-R62]. Note what that compares:
the payout against **technical provisions**, a best-estimate quantity this projection feeds but
does not itself produce. What the model emits directly is the smoothing-account posting
`payout − AS(t)`, and using its sign as the routing diagnostic is a **[std]** substitution —
rationale: the asset share is the model's own state variable and the retrieved sources state no
with-profits lapse direction, so the substitution has to be declared rather than assumed away.

On this design's own formulas, final bonus and MVR are never simultaneous (`FB > 0` requires
`S > FV`; `MVR > 0` requires `S < FV`, product-spec (24)), so the surrender payout
`FV(t) + FB(t) − MVR(t)` collapses to three cases: **`S(t)`** where `S(t) ≥ FV(t)`;
**`max(S(t), AS(t))`** where `FV(t) > S(t)` and `FV(t) > AS(t)`, the MVR being capped at the COBS
20.2.16R bound `FV − AS` [R1]; and **`FV(t)`** where `AS(t) ≥ FV(t) > S(t)`, the bound leaving no
room for an MVR at all. The sign of `payout − AS(t)` is therefore **not constant across the book**:

- **Positive — the lapse-up limb.** Where the ±10% y/y floor or the corridor lifts `S(t)` above
  `AS(t)`, discontinuance costs the fund: worked-example scenario B pays 26,550.00 against
  `AS(6) = 25,173.99`, a posting of **+1,376.01**. Scenario A pays exactly `AS(6)` and posts zero.
- **Negative — the lapse-down limb.** Two routes. The corridor can leave a smoothed payout below
  the asset share (`S ≥ 0.8·AS`), and — the larger effect — an in-the-money guarantee may be
  payable **only on persistency**: the MVR-free 10th-anniversary face value costs the fund
  2,704.05 in scenario B (27,878.04 against 25,173.99) but **only if the policy is still there**,
  against 1,376.01 if it surrenders first, and the CWP maturity guarantee `G(n)` behaves the same
  way. For those cells earlier discontinuance *avoids* cost, so `3B6.3` is the binding limb. This
  is the with-profits analogue of a lapse-supported design, and it is why "with-profits is stressed
  by lapse up" is wrong as a general statement.

The framework applicability matrix marks **both** `3B6.2` and `3B6.3` `x` for with-profits, and
records that the SCR research stream had marked lapse up `x` uniformly across six products before
the product stream split the direction per product [REG-R62]. **The derivation in the two bullets
above is [std]** — rationale: it is read off this reference design's own formulas and worked
example, and no retrieved source states the lapse direction for any with-profits design.

**Mass lapse is 40%, and it includes making a contract paid-up.** The **70%** limb reaches RAO
Schedule 1 Part II **class VII only** after the correction effective 31 December 2024, so **40%**
applies to every cell here [REG-R62][REG-R64] — and a drafter reading PS15/24 alone gets this wrong,
since ¶¶6.16 and 6.18 remain published and unamended [REG-R42][REG-R64]. `3B6.8` requires the event
to be based on **the type of discontinuance that most negatively affects basic own funds on a
per-policy basis**, and "discontinuance" **includes making a contract paid-up** [REG-R62]. The CWP
**paid-up option** is excluded from the base model **[std]** but is recorded as existing [S4] and
altered policies may need separate asset-share treatment [S6] — so it must be modellable for the
mass-lapse run even though it is switched off in the base projection.

**LACTP, and why it is a second complete pass.** `Adj_TP = −max(min(BSCR − nBSCR; FDB); 0)`, where
`nBSCR` recalculates the whole BSCR with the scenario permitted to change the value of future
discretionary benefits and with future management actions complying with TPFR 8 live in the life,
SLT health, health catastrophe, market and counterparty default modules, **taking into account any
legal, regulatory or contractual restrictions on distributing FDB** [REG-R62]. The
risk-mitigating effect counts only to the extent the firm can establish that a reduction in FDB may
be used to cover unexpected losses (6.2) [REG-R62] — for this product that is a COBS 20 and PPFM
question, not a modelling one [R1][R2][REG-R9]. Two implementation traps follow. First, **SCR-SF
3.3A(1)(d) freezes FDB in the gross run while 3.3A(2)(a) requires management actions complying with
TPFR 8 to be taken into account; the two limbs are in tension on their face and the framework
records the tension rather than resolving it** [REG-R62]. Second, **four sub-modules are defined as
the highest of alternative scenarios — life lapse, SLT health lapse, interest rate and currency —
and where the highest gross requirement and the highest corresponding net requirement rest on
different scenarios the charge is the one whose scenario produces the highest *net* requirement**
[REG-R62]. Both the lapse maximum and the interest-rate maximum are live for this product, so
**the selection is made on the net run and the reported gross number follows it** — not a
theoretical trap here.

**LACDT.** `Adj_DT` is the change in deferred taxes from an instantaneous loss of
`BSCR + Adj_TP + SCR_operational` — computed on the **post-`Adj_TP`** loss and **including**
operational risk — with **no benefit taken for an increase in deferred tax assets**; the SCR-SF 6.5
transitional permitting otherwise is printed as running "for a transitional period ending
**30 December 2025**", and **no PRA instrument confirming its expiry or extension was retrieved**:
treat it as expired and flag it [REG-R62].

**Ring-fenced funds multiply everything.** SS14/15 ¶2.2 records the PRA's expectation that the UK
with-profits restrictions "will generally mean that **each with-profits fund displays the
characteristics of a RFF**", and ¶2.3 that a **sub-fund** required to be treated as a separate
with-profits fund under FCA COBS 20 is treated as a **separate RFF** [REG-R71][REG-R9]. SCR-SF 9.1
then requires a notional SCR for **each RFF, each MA portfolio and the remaining part, as if each
were a separate firm**; **the firm's SCR is the sum**; basic own funds at fund level include **only
restricted own funds**; and **no diversification is allowed between ring-fenced funds, matching
adjustment portfolios and the remaining part** [REG-R62]. Two subtleties: the **scenario choice is
made firm-wide** — each notional SCR uses the scenario under which the basic own funds of the *firm
as a whole* are most negatively affected, so a fund's notional SCR can be driven by a scenario that
is not the worst for that fund, and **how a firm performs that firm-wide search is not prescribed by
any retrieved source** [REG-R62]; and `9.1(5)` adjusts a scenario's effect on RFF basic own funds
for the change in technical provisions caused by the change in FDB, **capped at the FDB included in
that fund's technical provisions** [REG-R62]. The scale is the point: the run count is on the order
of *(scenario-based sub-modules) × 2 (gross and net) × (RFFs + MA portfolios + 1)*, plus the
permutations inside the lapse and interest-rate maxima [REG-R62] — and a consolidator running many
internally segregated funds [S4] multiplies the middle factor accordingly.

**Undertaking-specific parameters are unavailable to this product.** The replaceable-parameter list
is exhaustive and covers only non-life and NSLT health premium and reserve risk, the
non-proportional reinsurance adjustment factor, and the **increase in the amount of annuity
benefits** for life and health revision risk — nothing in mortality, lapse, expense, catastrophe,
market or counterparty risk may be replaced [REG-R65].

### Own funds, the ring fence and the estate

- **The estate is Tier 1 capital, not a technical provision — by a five-rule chain.** TP 9.1(3)
  requires technical provisions to include all payments to policyholders including future
  discretionary bonuses, whether or not contractually guaranteed, "**unless those payments fall
  within Surplus Funds 2.1**"; **Surplus Funds 2.1** says a firm shall **not treat surplus funds as
  insurance and reinsurance obligations**; **SS13/15 ¶2.1** conditions that carve-out on the
  surplus funds meeting the **Tier 1** requirements in Own Funds 3.1; **Own Funds 3A.1(1)(d)** then
  makes them a **Tier 1 unrestricted own funds item in their own right**; and **SS13/15 ¶2.3** adds
  that they will normally meet the Tier 1 criteria **but**, because of the FCA policyholder-fairness
  rules, are "likely to be treated as part of a ring-fenced [fund]"
  [REG-R1][REG-R45][REG-R46][REG-R77]. **The PRA Rulebook Glossary definition of "surplus funds"
  could not be retrieved — ten URL forms were tried and all failed — so the scope of the defined
  term is [unverified]**, and everything above rests on the Surplus Funds Part calculation and Own
  Funds 3A.1(1)(d) rather than on a definition [REG-R45][REG-R77].
- **The asset-share recursion in this file *is* the regulatory retrospective calculation.** Surplus
  Funds 3.1 computes surplus funds per fund as with-profits assets, less with-profits policy
  liabilities, less tax and other costs on recognising future shareholder transfers, less other
  attributable liabilities, less **the value of future shareholder transfers**; and 3.3 values
  with-profits policy liabilities **retrospectively by default** as a ten-item signed roll-up
  [REG-R45]. Those ten items map onto "Asset share recursion (core)" above item for item: premiums
  received (`P(t)`); investment income and asset value movements (`r(t)`); permanent enhancements;
  past miscellaneous surplus or deficit allocated (`M(t)`); expenses incurred or deducted
  (`c_amc`); past deductions for the cost of guarantees, smoothing, options and life cover (`c_g`,
  `MC(t)`); partial benefits paid or due (`W_AS(t)`); attributable tax; reinsurance amounts; and
  past shareholder transfers **less any implicit allowance for the value of future shareholder
  transfers** (`ST(t)`) [REG-R45]. This is the same codification the model already cites locally as
  [R8]. It is also **the one place in this library where a model must carry history rather than
  project forward** [REG-R45][REG-R46].
- **The prospective route, and why chassis A is its archetype.** Surplus Funds 3.4 applies only
  where the retrospective value "does not adequately reflect the value" or is impracticable, with
  future discretionary additions clamped in 3.5 to what the retrospective calculation would have
  allowed [REG-R45]. **SS13/15 ¶3.1 names whole-of-life policies** as the case where the
  retrospective result "might be negative or significantly lower than the value calculated using
  the prospective approach" [REG-R46] — so the whole-of-life bond of chassis A is the archetypal
  prospective-route contract even though this model computes an asset share for it. Grouping is
  permitted only where it gives **the same or a higher** result and groups policies with similar
  attributes "**including the status of guarantees**" [REG-R46], which cuts directly across the
  specimen-policy convention.
- **What keeps the estate out of the best estimate — and the question that leaves open.** SS13/15
  ¶3.6: the PRA "would not expect a firm to include within benefits payable **distributions from
  the estate**" it might make in run-off [REG-R46]. **Whether estate distributions belong in the
  TP 9.1(3) best estimate is not answered by any retrieved source; ¶3.6 speaks only to the
  surplus-funds calculation** [REG-R46]. That is precisely the open question behind this product's
  estate variations — reattribution special bonuses [S5], annual ProfitShare [S6], excess-surplus
  unit-price enhancements [S1][S2] — and behind the COBS 20.2.21R at-least-annual excess-surplus
  determination [R1]. The base model's choice of a residual estate with no scheduled distribution
  **[std]** (product-spec (3)) sidesteps rather than settles it.
- **The shareholder transfer is not trapped in the ring fence; the estate is.** *Restricted own
  funds* exclude **the value of future transfers attributable to shareholders** [REG-R43], so the
  expected `ST` stream leaves the fence while the estate does not.
- **Own Funds 3L strikes out the surplus estate above the fund's own capital need.** The
  reconciliation reserve is reduced by `max(0, restricted own funds in the fund − that fund's
  notional SCR)`; where the assets, liabilities and risk in a ring-fenced fund are **not material**
  the firm may instead deduct the **total** restricted own funds and, per SCR-SF 2.2, then needs no
  notional SCR for it [REG-R77][REG-R62]. **Restricted own funds count towards entity own funds
  only up to the capital the fund itself needs.** **Whether that deduction also bites the MCR
  coverage test is not settled**: Own Funds 3L operates textually on the reconciliation reserve,
  while the EIOPA ring-fenced funds guideline is explicit that only own funds up to the notional SCR
  contribute to coverage of the SCR **and the MCR**, and no retrieved PRA rule says so — and those
  guidelines' continued UK application rests on SoP1/19, **which was not retrieved**
  [REG-R77][REG-R80c].
- **MCR: this product supplies the formula's only negative term.** `MCR_linear` for long-term
  business runs over guaranteed benefits of with-profit business (`TP_l1`), **future discretionary
  benefits of with-profit business (`TP_l2`), which carries the only negative coefficient in the
  whole formula** — so a larger FDB reserve *reduces* the linear MCR — linked liabilities
  (`TP_l3`), all other long-term obligations (`TP_l4`) and capital at risk, each **without the risk
  margin, net of reinsurance and floored at zero term by term**; the corridor is
  `min(max(MCR_linear, 0.25 × SCR), 0.45 × SCR)` and the absolute floor for long-term insurance is
  **£3,500,000** [REG-R78]. **Capital at risk is `(x)` for this product**: it arises only through
  the death benefit in excess of the fund or asset share — `g_db·(FV + FB) − AS` on chassis A,
  `G(t) +` interim accrual `+ FB − AS` on chassis B — **floored at zero per contract rather than on
  the portfolio sum**, and the definition's second limb needs a "sum payable on **immediate** death
  or disability" attribute on every model point distinct from the projected death-benefit stream
  [REG-R78]. **How the MCR interacts with ring-fenced funds at all is not settled — MCR 3C.1
  aggregates technical provisions across the firm with no RFF split and the MCR Part contains no
  RFF rule** [REG-R78].
- **The distributable-earnings pattern comes off the prudential balance sheet.** For a
  Solvency-II-authorised long-term insurer, CA 2006 s.833A substitutes `A − L − D` on **prudential**
  values for the realised-profits test, the deduction list `D` including the excess of **ring-fenced
  fund assets over ring-fenced fund liabilities** — for a with-profits writer the single largest
  deduction — with s.833A(3) capping distributable profits at the **accounts'** accumulated profits
  less accumulated losses [REG-R104]. So a with-profits distributable-earnings projection is a
  projection of the Solvency UK balance sheet **plus the ring-fenced fund surplus**, then the
  accounts-based cap — not a projection of the accounts.

### Statutory accounts and tax

- **Measurement model: VFA under IFRS 17, the realistic value of liabilities under UK GAAP.** The
  **UKEB's expectation for the UK is explicit — the variable fee approach "is expected to be applied
  to insurance contracts such as unit-linked contracts and with-profits contracts"**, the premium
  allocation approach to short-term contracts, leaving the general measurement model for protection
  and annuities [REG-R106]. Under the VFA, changes in fulfilment cash flows arising from the time
  value of money and financial risk go **into the CSM** rather than immediately to insurance finance
  income or expense, with CSM adjustments at **current** discount rates; eligibility is assessed at
  inception and **never reassessed** [REG-R106]. UK-adopted IFRS 17 has been effective since
  **1 January 2023** for IFRS-reporting insurers [REG-R38]. **IFRS 17 itself is paywalled and was
  never read anywhere in this library — every paragraph reference is one the UKEB quotes — and no
  confidence level, coverage-unit formula or transition proxy is stated** [REG-R107][REG-R106].
- **The inherited estate is the open IFRS 17 question, and the FFA is the UK GAAP answer to the
  same problem.** IFRS 17 does not explicitly address the inherited estate; there is an emerging
  consensus that a liability be recognised for the **policyholders'** share while the
  **shareholders'** share is contested, and entities are expected to recognise an **increase in
  equity on transition** under a fair value approach [REG-R106]. Under FRS 103 the same undetermined
  surplus sits in the **fund for future appropriations** — "all funds the allocation of which either
  to policyholders or to shareholders has not been determined by the end of the financial year",
  disclosed **separately** and never combined with technical provisions — which is neither
  policyholder liability nor equity [REG-R105][REG-R99]. **This is the sharpest UK GAAP / IFRS 17
  divergence for this product**, and it lands squarely on the estate that the model above treats as
  a residual.
- **UK GAAP measurement.** With-profits runs on the **realistic value of liabilities** rather than
  the modified statutory solvency basis, **adjusted to exclude the shareholders' share of projected
  future bonuses**, with the difference from MSSB routed through the FFA so that "there will
  generally be no change in the profit for the reporting period **except where the adjustments
  result in a negative balance on the FFA**" [REG-R99][REG-R100]. **The definitions the whole
  apparatus rests on — INSPRU 1.3.40 and 1.3.190 as at 31 December 2015 — were not retrieved**, the
  FCA Handbook rendering INSPRU 1.3 as a "Deleted" stub, **so "realistic value of liabilities" is a
  citation here and not a specification** [REG-R99][REG-R116]. Note the vocabulary trap this
  creates: in a Solvency UK context "with-profits benefits reserve" means the IR.12.06 R0010 item,
  which *is* Surplus Funds 3.2 policy liabilities; in a UK GAAP context "realistic value of
  liabilities" is the FRS 103 glossary term anchored to INSPRU as at 31 December 2015. **Two
  definitions with a shared ancestry, and no retrieved source states that they give the same
  number** [REG-R90][REG-R99].
- **UK GAAP reaches the same verdict on guarantees that the PRA rules do.** FRS 103 implementation
  guidance requires the options and guarantees liability of in-scope with-profits business to be
  measured **at fair value or by a market-consistent stochastic model**, states that "any
  deterministic approach … will generally fail to deal appropriately with the **time value** of the
  option", and requires the stochastic valuation to reflect, **scenario by scenario**, management
  actions **consistent with the published PPFM** [REG-R100][REG-R9]. That is the accounts ledger
  arriving independently at the conclusion "Cost of guarantees — cited, not specified" above draws
  from PRA Technical Provisions 9.2 [R7]: on **both** ledgers the deterministic `c_g` deduction is a
  *charging* proxy and not a valuation.
- **The only UK GAAP measurement floor, and how much of it bites here.** The **liability adequacy
  test** compares the carrying amount of recognised insurance liabilities **less related DAC and
  related intangibles** against a current-estimate projection of all contractual and related cash
  flows "**as well as cash flows resulting from embedded options and guarantees**", and **the entire
  deficiency** goes to profit or loss [REG-R99]. Alongside it, IG2.41: **no policy may have an
  overall negative provision except as allowed by PRA rules, nor a provision less than any
  guaranteed surrender or transfer value** [REG-R100]. **How much of the surrender-value limb bites
  is a design question, not a product-family fact**: chassis B's surrender values are expressly
  *not* guaranteed (product-spec, "Conventional guaranteed benefit stack") and chassis A's ordinary
  surrender value is subject to an MVR, but the 10th-anniversary MVR-free encashment right at
  `FV(t) + FB(t)` is a contractual amount payable on that date, and **whether IG2.41's "guaranteed
  surrender value" reaches a dated MVR-free encashment right is not settled by the retrieved text**
  [REG-R100][S4]. The framework records the floor row as mattering most for term assurance,
  critical illness and the unit-linked bond, where the Solvency UK number is routinely negative or
  has a routinely negative component; for this product, whose best estimate is not normally
  negative, the two ledgers diverge correspondingly less on the floor itself [REG-R100][REG-R41].
- **DAC — do not import the U.S. framing, and do not import its reversal blindly either.** The
  general UK position is the **opposite** of the U.S. one: SI 2008/410 Schedule 3 **para 13 requires**
  acquisition costs relating to a subsequent financial year to be **deferred**, with DAC at assets
  item **G.II** and its movement at technical account item **8(b)**, and FRS 103 **¶3.7 requires**
  deferral subject to three recoverability carve-outs [REG-R105][REG-R99]. **With-profits is the
  scoped exception**: FRS 103 **¶3.10** — "Acquisition costs shall not be deferred for with-profits
  funds" — but **¶3.1(b) applies ¶¶3.10–3.15 only to with-profits business and funds to which the
  PRA realistic capital regime (INSPRU section 1.3 as at 31 December 2015) applied before 1 January
  2016**, while ¶3.7 opens "Except as required by paragraph 3.10" and IG1.1 makes ¶3.12 optional
  outside that scope [REG-R99][REG-R100]. **Whether the ¶3.10 prohibition reaches a with-profits
  fund that was never in the realistic regime is not settled by the retrieved text, and neither
  reading is asserted here.** For this composite the answer is therefore a **configuration, not a
  product fact**: chassis B is a legacy conventional book that would have been inside the realistic
  regime, while the modern smoothed-fund variation [S2][S9][S11] is exactly the unsettled case. Two
  further contrasts hold regardless: **Solvency UK has no DAC at all** — acquisition expenses are
  projected outflows inside the best estimate (TPFR 16.1) and the Valuation Part recognises no
  unamortised expense asset (Val 8.1) [REG-R41][REG-R39] — and **IFRS 17 has no DAC asset either,
  for the opposite reason**, acquisition cash flows sitting inside the fulfilment cash flows and
  **reducing the CSM at initial recognition** [REG-R106]. On the tax side the seven-year BLAGAB
  acquisition-expense spread at FA 2012 s.79 is **repealed for accounting periods beginning on or
  after 1 January 2023** — relief now follows recognition in the income statement, legacy sevenths
  keep running, and a deduction for costs arising earlier but recognised post-transition
  **continues to be disallowed** [REG-R18 LAM04130][REG-R109]. The base model here carries **no
  acquisition-cost stream at all** (100% allocation with an explicit AMC **[std]**, product-spec
  (7)), so nothing bites until one is added.
- **Tax: BLAGAB and the I-E basis, and the model's `tax_basis` flag is the regulatory flag.** With-
  profits life business is **BLAGAB**, taxed on the **I-E** basis under FA 2012
  [REG-R17][REG-R18]; the framework matrix marks BLAGAB/I-E `x` for this product and the
  **non-BLAGAB trade basis `(x)`** for the pension cells. **The `tax_basis` enum {life_net,
  pension_gross} in the model point table above is exactly the BLAGAB / non-BLAGAB flag** the
  framework requires on every projected cash flow, asset and liability — and IR.12.06's split of
  the investment return into **non-taxable (e.g. pensions)** and **taxable (e.g. endowment)** asset
  shares is the same distinction on the reporting side [REG-R90]. The six-step s.73 computation,
  the `E` restriction excluding claims, and the commercial-allocation consistency requirement are
  in the framework [REG-R17][REG-R18]. Two points that are this product's own: for a **mutual the
  whole I-E profit is attributable to policyholders** (s.103), which is the ProfitShare variation's
  tax position (product-spec, "Ownership variation") [REG-R18 LAM06020]; and HMRC's worked
  illustration of the policyholder/shareholder split uses **2018 rates**, so its statement about the
  direction of the incentive **was true when written and is not true at the access date** — record
  the direction as period-dependent and do not restate HMRC's sentence as current
  [REG-R18 LAM01160][REG-R110].
- **Deferred tax needs three liability measures, not two** — accounts timing differences (FRS 102
  Section 29), the Solvency-UK-less-tax difference on all assets and liabilities including
  technical provisions (Valuation 11), and the tax value itself
  [REG-R102][REG-R39]. Generic, and in the framework; what bites here is the UK GAAP anti-double-
  count rule that where the long-term business provision has had regard to the timing of tax relief
  or the tax obligation **that effect must be excluded** from the deferred-tax determination
  [REG-R100]. That rule is live here because the UK GAAP with-profits liability is built off asset
  shares which are themselves credited net of life-fund tax for BLAGAB cells [S1][S2][REG-R17], so
  the timing of the tax obligation is already inside the provision.
- **Policyholder taxation is a separate regime and stays where it is.** Chargeable event gains on
  the bond and the cumulative 5%-of-premium annual allowance [REG-R15][REG-R16] shape withdrawal
  behaviour (see "Policyholder behavior modeling") but are not an insurer tax computation and do not
  enter any of the three measurements above.

### Traps peculiar to this product

1. **Shareholder transfers are not a best-estimate cash flow stream.** There is no TPFR 13.1 item
   for them; `ST(t)` enters through TP 9.1(3) and Surplus Funds 3.1(5), and restricted own funds
   exclude the value of future shareholder transfers [REG-R41][REG-R1][REG-R45][REG-R43].
2. **Netting life-fund tax into the credited return breaks two requirements at once** — TPFR
   13.1(8), which wants policyholder-charged tax identifiable, and IR.12.06 R0160, which wants the
   investment return **pre-tax** [REG-R41][REG-R90].
3. **Unit vocabulary is not unit-linked status.** IR.12.01's surrender-value, nominal-value-of-units
   and matching-value-of-units rows are C0020 only; the operational-risk provisions leg deducts only
   unit-linked technical provisions; and while the EIOPA guideline puts conventional unit-linked
   business outside ring-fenced-fund scope, the PRA expects **every with-profits fund to be an RFF**
   [REG-R89][REG-R62][REG-R80c][REG-R71].
4. **The lapse stress splits by cell.** Cells whose payout is lifted above the asset share by
   smoothing take lapse **up**; cells whose in-the-money guarantee is payable only on persistency —
   the 10th-anniversary MVR-free face value and the CWP maturity guarantee — take lapse **down**
   [REG-R62]. See the derivation above; it is **[std]**.
5. **The estate is one number carrying three meanings on three lines** — excluded from technical
   provisions, a Tier 1 unrestricted own-funds item, and restricted own funds recognised only up to
   the fund's notional SCR. Produce it once and tag it three ways
   [REG-R1][REG-R45][REG-R77][REG-R62].
6. **Surplus funds carry no risk margin**, so the estate is not `fund assets − technical provisions`
   [REG-R46].
7. **No equity risk premium in the best estimate.** The 5.0% p.a. return is a scenario level
   **[std]**; TPFR 9.1 requires returns consistent with the relevant risk-free curve off the assets
   actually held [REG-R41].
8. **FDB is frozen in the gross SCR run and responsive only in the net run**, and the selection
   among the lapse and interest-rate alternatives is made **net** with the reported gross number
   following it — one run scaled is not two runs [REG-R62].
9. **Mass lapse includes paid-up.** The CWP paid-up option is switched off in the base model
   **[std]** but must remain modellable [REG-R62][S4][S6].
10. **The COBS 20 numbers this product depends on could not be re-fetched in this effort.** COBS
    20.2 returned HTTP 500 on one attempt and COBS 20.3 content on another, so target-range
    percentages, MVR bounds and required percentages are carried from the frozen [R1] record and are
    **named, not restated**, in the shared reference material; **COBS 20.2.17R — the basis on which
    IR.12.05 R0040 requires reversionary bonus value to be discounted — is named and not
    specified** [REG-R9][REG-R90].
11. **Time-sensitive items to re-check before relying on this section.** The LACDT transitional
    printed as ending **30 December 2025** with no confirming instrument retrieved [REG-R62]; the
    Own Funds rules carrying live "future version after 31/12/2026" markers, with PS18/26's amended
    rule text in an appendix that **was not retrieved** [REG-R77][REG-R87]; PS18/26's removal of
    claims management expenses from IR.14.01's claims-paid definition from the **31 December 2026**
    reference date [REG-R87]; and the FRS 102 / FRS 103 Periodic Review 2024 amendments, effective
    for periods beginning on or after **1 January 2026** [REG-R101][REG-R102].

---

## Valuation and reserve pointers

This library projects **gross best-estimate liability cash flows**. The Solvency UK balance
sheet, the reporting templates, the SCR modules, own funds and the two other ledgers for this
product are in **Statutory accounting and capital** above; this section stays a pointer list for
the valuation layers themselves, which consume those flows but are not reproduced here.

- **Solvency UK BEL and future discretionary benefits.** Technical provisions = best estimate +
  risk margin; the best estimate is the probability-weighted, discounted value of all cash flows
  [R7][REG-R1]. For with-profits, the BEL includes **future discretionary benefits** — future
  regular and final bonuses expected under PPFM-consistent discretion — because expected payments
  count "whether or not ... contractually guaranteed", with the surplus-funds carve-out for the
  unallocated estate [R7][R8]. The With-Profits Actuary must advise whether the FDB assumptions
  are consistent with the PPFM [R5]. Contract boundary, cash-flow scope, the separate-FDB
  requirement and the reporting decomposition: Statutory accounting and capital, "Technical
  provisions".
- **Guarantees and options.** PRA Technical Provisions 9.2 requires guarantees and options
  (unit-price floors, guarantee dates, GAOs) to be valued market-consistently with dynamic
  policyholder behavior [R7]; the canonical methodology is stochastic simulation of the bonus,
  smoothing and MVR rules (Hibbert & Turnbull 2003; Hare et al. 2000 [R13]) — stochastic-on-
  deterministic use of this model. See "Cost of guarantees — cited, not specified" above; the
  accounts ledger reaches the same verdict independently (Statutory accounting and capital,
  "Statutory accounts and tax").
- **Risk margin.** Post-reform cost-of-capital method: CoC 4%, risk taper λ = 0.9
  (floor 0.25) for long-term business [R7][REG-R4]. Cited-not-specified; what is
  product-specific about it is above.
- **Ring-fencing and estate.** With-profits fund assets must cover the fund's
  liabilities [R6]; surplus funds (the estate) are own funds, excluded from
  technical provisions [R8]. The Tier 1 chain, the Own Funds 3L deduction and the
  notional-SCR-per-fund consequence are above, as are the two transitionals — TMTP and TMIR,
  which run on **different** admissibility dates [REG-R3][REG-R57].
- **Matching adjustment.** The guaranteed element of a with-profits immediate or
  deferred annuity can qualify as an MA "eligible element" [REG-R2] — relevant only
  to the annuity variations, not the composite cells. Conditions, and the unresolved question of
  how the asset share follows the guaranteed element, are above.
- **IFRS 17.** UK-adopted IFRS 17 (effective 1 January 2023) applies to
  IFRS-reporting insurers [REG-R38]; the fulfilment-cash-flow engine is this same projection. The
  UKEB's expected UK mapping (the variable fee approach) and the inherited-estate question are
  above; the standard text itself was never fetched anywhere in this library.
- **Conduct overlay.** Payout machinery in any valuation must respect the COBS
  target-range, MVR-bound and required-percentage rules [R1] — they are constraints
  on the FDB discretion, not just conduct background. COBS 20.2.17R is additionally the basis on
  which IR.12.05 requires reversionary bonus value to be discounted [REG-R90].

---

## Key sensitivities and model risks

1. **Fund return / equity backing.** Asset shares, final bonuses and MVR incidence
   all key off `r(t)`; the observed strategy ceiling is a benchmark equity backing
   ratio of 75% (Aviva EBR upper limit [S5]). Deterministic base runs materially understate
   guarantee costs (convexity) — the central model risk here [R7][R13].
2. **Bonus discretion path.** The split of payout between hardened regular bonus and
   final bonus changes guarantee costs without changing the target payout: a higher
   `θ` or faster `κ` hardens guarantees. The [std] parametrization is a genuine
   modeling choice with no public calibration.
3. **Smoothing parameters.** The ±10% cap and 80–120% corridor determine how much of
   a market shock passes to payouts immediately; firms' actual limits vary (5%–15%
   observed [S1][S5][S7]) and can be suspended under solvency stress [S5].
4. **MVR application.** Whether the discretion is exercised promptly (and the review
   buffer — Phoenix tolerates up to 10% return variation before an extra MVR review
   [S4]) drives surrender strain in down markets.
5. **Surrender behavior at guarantee dates.** The guarantee-date spike multiplier and
   MVR deterrent are unverified [std] shapes; anti-selective exit when guarantees are
   in the money is the dominant behavioral risk (dynamic assumptions required [R7]).
6. **Mortality proxy.** The 60%-of-ONS basis is a placeholder; insured with-profits
   experience differs by class and era, and current CMI tables are
   subscriber-restricted [R10][REG-R22][REG-R32].
7. **Expense and charge caps.** Where actual expenses exceed capped charges (1% caps
   [S1][S5]) the excess falls to the estate — a fund-level, not policy-level, cash
   flow this single-policy model does not capture.
8. **GAO interest-rate exposure.** Legacy GAO cells are long interest-rate optionality
   [S4]; omitting the stochastic layer understates their cost materially.
9. **Estate interactions.** Reattributions, special bonuses and ProfitShare
   [S5][S6] are fund-level discretions outside the base model; scenario overlays
   should treat them as management actions.
10. **Data-provenance limits.** Snapshot bonus rates, EGRs and MVR scales are [std]
    placeholders by design (declarations are not in PPFMs — research gap); a
    calibration pass against current bonus declarations is required before any
    quantitative use.
