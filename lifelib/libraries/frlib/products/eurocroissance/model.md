# Implementation Notes

**Status:** Draft, 2026-08-26. Built from
[`products/eurocroissance/technical-notes.md`](technical-notes.md);
the product it implements is specified in
[`product-spec.md`](product-spec.md).

> **This is a mechanics demonstration, not a pricing or reserving result.** The
> mechanics are sourced, and unusually completely so — eurocroissance is a statutory
> construct rather than a market convention, so arts. L. 134-1 to L. 134-5 [R1],
> R. 134-1 to R. 134-12 [R2] [R7] and A. 134-1 to A. 134-7 [R3] fix the two provisions,
> the six permitted charge bases, the surrender and maturity values, the minimum part
> value, the 90 %-of-TEC discount ceiling and the *provision pour garantie à terme*.
> Every **rate** is a **[std]** standardization. No *notice d'information*, *conditions
> générales* or PRIIPs *document d'information clé* for any eurocroissance support could
> be retrieved [S10], so every insurer-level parameter is either a third-party fact-sheet
> figure [S8] or a level taken from the one published actuarial *mémoire* [R13]; the
> regulatory mortality tables are cited by arrêté and never shipped [REG-R21] [REG-R22]
> [REG-R23]; and no eurocroissance lapse experience is public [R14] [R21].

## Run it

```bash
python products/eurocroissance/run.py           # Chassis A, the worked example
python products/eurocroissance/run.py 2         # Chassis B, same asset path
python products/eurocroissance/run.py 7         # an in-force Chassis A cell
```

Three lines to the same thing:

```python
import modelx as mx
model = mx.read_model("products/eurocroissance/EC_FR_S")
model.Projection[1].result_provisions()
```

`result_provisions()` gives the provision machinery — the account's assets against the
two provisions, the parts and their value, and the insurer's own-funds items beside them.
It is the table the notes' two worked-example tables print. `result_cf()` gives the cash
flows.

## The time index

`t` is **0-based**. Period `t` is the policy year running from time `t` to time `t + 1`,
so `t = 0` is the first policy year and the contractual **policy year is `t + 1`**.
`proj_len()` is the **number** of policy years projected — `policy_term()`, unchanged in
value — and it is the *exclusive* end of the frame:

```
result_cf().index == range(proj_start(), proj_len())      last row = proj_len() - 1
len(result_cf()) == proj_len() - proj_start()
```

A new-business cell has `proj_start() = 0` and `n` rows; the shipped worked example (`n` =
10) has **ten** rows, `t = 0 … 9`, and the last of them is the year that ends at the
*échéance*, where `maturity_value`, `pols_maturity` and `claims_maturity` live. An
in-force cell opens at `proj_start() = duration_ifo`, the completed policy years at the
valuation date — an elapsed count, and already 0-based — so shipped point 7 runs `t = 4 …
9`, six rows.

**The issue instant is not a row.** The initial *versement* creates the rights, strikes
both provisions and draws the acquisition costs; all of that is the **opening state** of
the first projected period rather than a row of its own. The state is reached through the
`"BOY"` timing — `own_assets_at(t, "BOY")`, `mg_at(t, "BOY")`, `pm_at(t, "BOY")`,
`prov_div_at(t, "BOY")`, `parts_at(t, "BOY")`, `part_value_at(t, "BOY")`,
`cum_prem_net_at(t, "BOY")`, `provision_value_at(t, "BOY")` — and the flows (the
*versement* itself, its entry charge, the acquisition commission and the maintenance
charged at that opening striking) are beginning-of-period flows of period `proj_start()`.
So the first row of `result_cf()` carries the initial *versement* **and** the first policy
year's levy, return and striking, and no number is lost from any total.

Four cells are indexed by a **time point** `k` instead of by a period — `age(k)`,
`tec_rate(k)`, `i_pm(k)`, `disc_factor(k)` — with `k` = 0 at issue and `k` = `n` at the
*échéance*. Period `t` opens at `k = t` and is struck at `k = t + 1`, which is why
`pm(t) = mg(t)·(1 + i_pm(t+1))^−(n−t−1)` and why `result_provisions()` publishes
`i_pm(t + 1)` in its `i_pm` column: the rate that period's provisions were struck at.
`mort_rate(t)` reads `age(t + 1)`, the *âge atteint* at the end of the policy year, which
is where the decrement is applied.

### What the input files are keyed by

No CSV value changed in the conversion; what changed is what the readers say the key
means.

| File | Time-like column | Decision |
|---|---|---|
| `model_point_table.csv` | `duration_ifo` | An **elapsed count** of completed policy years, 0-based by nature. Unchanged, and it is `proj_start()` directly. |
| `model_point_table.csv` | `premium_top_up_t`, `apport_t` | Contractual **policy-year labels**, 1-based, with 0 as the "none" sentinel. Unchanged; the model maps them as `t + 1 == premium_top_up_year()` and `t + 1 == apport_year()`. |
| `model_point_table.csv` | `policy_term`, `premium_regular_years`, `lock_up_years` | **Counts** of years, not indices. Unchanged. `lock_up_years` is compared as `t < lock_up_years()` (policy years 1 to `lock_up_years`), where it used to be `t <= lock_up_years()`. |
| `lapse_table.csv` | `policy_year` | A contractual **1-based policy-year label**, 1 to 40. File unchanged; `lapse_rate_base` and `wd_rate_base` read row `t + 1`. |
| `scenario_table.csv` | `year` | The elapsed **year end** at which the return is credited: row `k` is the return over the year ending `k` years after issue. File unchanged; `asset_return(t)` reads row `t + 1`, and row 0 — a 0.0000 placeholder for the inception instant — is now never read. |
| `tec_curve.csv` | `year` | An elapsed **time point** `k`, `k` = 0 at issue. File unchanged, and it is exactly the index `tec_rate(k)` uses. |
| `mort_table.csv` | `age` | Attained age, not time. Unchanged; read at `age(t + 1)`. |

## Two provisions, two state variables, one rebalancing a year

That sentence is the model. The *provision mathématique* is the guaranteed amount
discounted at the A. 134-1 rate; the *provision de diversification* takes whatever the
account's assets leave over, floored at the parts' minimum value [R2 R. 134-2, R. 134-4](#frlib-eurocroissance-r2).
**Neither is a cash flow.** The policy's cash flows are *versements* in and surrender,
death and maturity claims out; the two provisions reach them only through the R. 134-5
surrender and R. 134-6 maturity formulas.

| | Chassis A (1° engagement) | Chassis B (2° engagement) |
|---|---|---|
| `pm(t)` | `mg(t)·(1 + i_pm(t+1))^−(n−t−1)` | identically 0 |
| `prov_div(t)` | `max(A(t) − pm(t), N(t)·u_min)` | `max(A(t), N(t)·u_min)` |
| Surrender | `(pm + N·u)·(1 − f_x)` | `(N·u)·(1 − f_x)` — **no guarantee** |
| Death | `pm + N·u` | `N·u` |
| Maturity (at `t = n − 1`) | `pm + N·u` | `max(N·u, mg)` |
| Insurer's own funds | `insurer_contribution` (L. 134-3) | `pgt` (A. 134-2) |

## The provision mathématique is re-struck, never accumulated

```
pm(t) = mg(t)·(1 + i_pm(t+1))^−(n−t−1)      i_pm(k) = max(0, 0.90 × TEC(n−k))
```

`i_pm` is indexed by a **time point** `k`; period `t` closes at time `t + 1`, which is
`n − t − 1` years short of the *échéance*.

`i_pm` is A. 134-1's ceiling [R3]: 90 % of the *taux de l'échéance constante*, interpolated
linearly between the bracketing maturities of the published curve, the longest rate held
beyond it, and a floor at zero. The article as retrieved gives the index maturity as the
holder's **guarantee maturity** (method 1°) or the account's 1°-engagement **duration**
(method 2°) and is silent on how it is re-read after inception; this model applies method 1°
and takes the **remaining** term `n − k` at each valuation time, which is **[std]** and not the article —
`technical-notes.md` sets out the reasoning and is the source of truth for the value. It is
**not** the
A. 132-1 maximum technical rate [REG-R17] and **not** the A. 132-3 guaranteed-rate
ceiling [REG-R18]; those are different and stricter objects that apply to a tariff, while
this one is a valuation ceiling for a provision the saver has no right to withdraw at.

Rolling `pm(t−1)` forward at last year's rate silently removes the **rate effect**. In
the worked example's policy year 6 — period `t` = 5 — the move is +824.18, of which the
time effect on the
unchanged 2.25 % rate is only **+236.74** and the re-strike at 0.90 % contributes
**+587.44**. An accumulating implementation lands `pm(5)` at
`10,521.82 × 1.0225 = 10,758.56` against the 11,346.00 the re-strike gives, and every
later year inherits the gap.

In the last projected period, `t = n − 1`, the discount factor is 1, so **`pm` equals `mg`
identically** and the Chassis A
guarantee is pre-funded by construction. `check_guarantee_funding()` asserts it at every
`t`, and it is the model's headline check.

The same rule is why an in-force model point carries no accumulated PM. `pm_ifo` is
shipped in the table and read by `check_pm_restruck()` alone: it compares what an extract
reports against what R. 134-2 requires, which is how a reader discovers an extract built
by accumulation. The projection itself re-derives the number.

## The annual rebalancing, and the insurer's contribution

```
L(t) = f_p·prov_div_open(t)       A_a = A_open(t) − L(t) − W(t) + P_net(t)
I(t) = A_a·r(t)                   F(t) = f_perf·max(I(t), 0)
A(t) = A_a + I(t) − F(t)          N(t) = N_open(t)(1 − f_p)(1 − w_partial) + parts bought
prov_div(t) = max(A(t) − pm(t), N(t)·u_min)      u(t) = prov_div(t)/N(t)
C(t) = max(pm(t) + prov_div(t) − A(t), 0)
```

`X_open(t)` is the `"BOY"` timing: `X(t−1)` in every period but the first, and in the
first the state the initial *versement* — or the in-force extract — creates.

The diversification provision takes the **residual** and stops at the parts' contractual
floor: R. 134-4 permits a debit balance to reduce the part value only *within the limit
of its minimum* [R2]. Where the floor binds, the two provisions together exceed the
assets, and the excess is exactly the L. 134-3 contribution [R1]. In the notes' policy
year 6 — period `t` = 5 — the
raw residual is `10,250.65 − 11,346.00 = −1,095.35`, the floor binds at
`207.7460 × 5.0000 = 1,038.73`, and the contribution is **2,134.08** — so the contract
surrenders for 12,384.73 against account assets of 10,250.65.

`C(t)` carries **no return to the savers** [std]. `own_assets_at` rolls forward from
`A_open(t)` and never from `pm_open(t) + prov_div_open(t)`, so the policy-year-7 asset
roll — period `t` = 6 — starts from
10,250.65 and not from 12,384.73. Rolling the topped-up balance forward would manufacture
investment return out of the insurer's capital.

The processing order is not free. R. 134-4 and R. 134-12 III both say that asset
affectations completing the account's representation are made **on the dates the
participation account is struck, after its balance has been allocated** [R2] [R7], so
`own_assets_at(t, timing)` and `parts_at(t, timing)` expose the steps one at a time —
`BOY`, `AFT_LEVY`, `AFT_EXIT`, `AFT_PREM`, `AFT_RETURN`, `AFT_PERF`, `AFT_TOP_UP` — and
`check_assets_roll_fwd()` rebuilds the whole recursion in one expression so that a
mis-ordered step shows up rather than quietly shifting the answer. Because the recursion
now starts from `BOY` rather than from `X(t−1)`, the four roll-forward checks are live in
the **first** projected period too, where they were previously skipped.

A *versement* leaves the contribution unchanged, and that is worth knowing rather than
assuming: it adds `P_net` to the assets and `g·P_net·v + (P_net − g·P_net·v)`
to the two provisions, which is the same number. The order of steps 7 and 8 in the notes
is therefore immaterial, and the model strikes `C(t)` on the post-*versement* state.

## The Chassis B surrender value is not guaranteed

This is the single most important product fact, and the product's central error is to
model it otherwise. Before the *échéance* a 2° engagement pays `parts × part value` and
**nothing else** [R2 R. 134-5](#frlib-eurocroissance-r2). On the worked example's policy-year-6 shock, period `t` = 5, that is **9,899.22**
— **84.18 %** of net *versements* — against a guarantee of 11,760.00 that does not apply.
A model that floors it at `g ×` premiums, or at the discounted guarantee, is modelling a
contract that does not exist.

The shortfall is carried instead as the *provision pour garantie à terme*, on the
**insurer's** balance sheet, outside the participation account, on the A. 132-18 tables at
a rate at most 90 % of the TEC and counting **no cash flows other than guarantee
maturities and mortality** [R3 A. 134-2](#frlib-eurocroissance-r3) [R10]. It is 1,446.78 at `t` = 5 and runs off to
zero by the *échéance* as the account recovers. A model must not "improve" that
deliberately narrow basis by adding lapses or expenses to it, and must not let it reach a
benefit: `check_own_funds_not_paid()` asserts that no benefit before the term exceeds
`pm + prov_div`, and the shipped Chassis B cells carry a positive PGT for four consecutive
years, so the check is live rather than decorative.

One of A. 134-2's two admitted drivers is **not implemented**. `pgt()` discounts the
guaranteed amount to `t` and applies **no survival factor**, so the present value is the
amount for a guarantee certain to be reached. The simplification is **[std]** and prudent —
it overstates the provision — and it is invisible on the worked example, where `mort_rate`
is zero; it is live on every decrement-bearing cell. On model point 6 at `t` = 6 — the end of policy year 7 — the reported
`pgt` is **2,739.35**, against **2,477.36** with the five-year survival factor 0.972660 the
shipped **[std]** table gives. In this single-policy model the mortality decrement reaches
the projection through `pols_if` in `result_cf()` rather than through the provision; a
fund-level implementation of A. 134-2 should carry the survival factor inside the present
value, over the account's 2° engagements.

The `max(·, mg)` exists **only in the last projected period, `t = n − 1`** and **only on
Chassis B** [R2 R. 134-6](#frlib-eurocroissance-r2). On
Chassis A the maturity amount is `pm + parts × part value` there — **more** than the
guarantee whenever the parts retain any value, 12,765.89 against 11,760.00 here.

## The death benefit is not the maturity guarantee

Chapter IV contains no death valuation article, so the death benefit is the **current
provision value** [R2] [R13]. Any *garantie décès plancher* [S1] [S2] is a complementary
guarantee provisioned **outside** the auxiliary account [R2 R. 134-7](#frlib-eurocroissance-r2): `death_payout()`
floors the payout at cumulative net *versements* where the model point elects it, and
`rider_claim_pp()` reports the difference separately — **1,860.78** on the policy-year-6
Chassis B death, `t` = 5, which is not the account's money. `cum_prem_net` is kept as its own state
variable rather than read off `mg`, because the two coincide only while `g` is 100 %.

## The charge bases are not interchangeable

R. 134-3 permits six bases and no others, and base 3° — a levy on the *encours* of the
diversification provision — is available only in an auxiliary account holding **no** 1°
engagements. No base permits a levy on the *provision mathématique* at all [R2]. The
recurring charge here is therefore base 4°, a levy **in number of parts**: `parts_levy()`
is `f_p × prov_div_at(t, "BOY")` and `parts_at()` cancels `f_p` of the parts. On Chassis A
that is
**15.64** in policy year 1, `t` = 0; an *encours* levy on `pm + prov_div` would have been
78.40, five times as much and unlawful in a 1° account.

The base 5° performance levy takes 10 % of positive financial performance and **nothing at
all** on a negative one, which is why both chassis show a nil performance levy in policy
year 6, `t` = 5.

## Behaviour, and what is held at zero

All dynamic shapes are **[std]**: no eurocroissance lapse experience is public and the
product is too small and too young to have any [R14] [R21].

| Overlay | Factor | When |
|---|---|---|
| Guarantee-imminent suppression | 0.5 | the two policy years before the *échéance* — the periods with `n − t − 1 ≤ 2` — **Chassis B only**, and **only while `N·u < mg`** |
| Duration-8 spike | 1.5 | policy year 8, period `t` = 7, where `n > 8` — the assurance-vie *abattement* [REG-R40] |
| Lock-up | 0 | `t < lock_up_years`, i.e. policy years 1 to `lock_up_years`; the L. 132-23 hardship exits are not separately modelled |

**The gate on the first is the point.** A saver who surrenders a 2° engagement gives up
the *entire* guarantee [R2 R. 134-5](#frlib-eurocroissance-r2), so the deterrent exists precisely while the
guarantee is in the money and is worth nothing otherwise. Applying it unconditionally
would invent behaviour where there is none.

Held at zero or absent by design, and each for a stated reason:

- the **PCDD piloting rule** — run the fund at 30 bp above the insurer's own euro fund and
  carry the rest to the PCDD [R13] — and the PCDD's release back into the participation
  account. `pcdd()` accumulates the R. 134-12 *apport d'actifs* [R7] and nothing else.
  Holding it at zero **understates the smoothing the real product delivers**.
- the **conversion of parts into PM** under A. 134-4, whose 15 %-of-PM headroom
  `conversion_headroom()` computes without exercising — 474.52 at `t` = 4, on which the
  0.50 % *frais de conversion* [S8] would be 2.37;
- the **revaluation of guarantees** out of the participation account, whose two A. 134-3
  tests `gate_revalue_ok()` evaluates without exercising: both pass at `t` = 4 and the
  second fails at `t` = 5, where the part-value floor has taken the headroom to nil;
- the ***rente viagère*** option at the *échéance* [R2 R. 134-6](#frlib-eurocroissance-r2), which
  `annuity_option_flag()` rejects by name — it needs the TGH05 / TGF05 generational tables
  [REG-R21], which are cited and never shipped, and a projection that runs past the term;
- and the statutory **arbitrage into an SRI ≤ 2 support** that A. 134-6 makes the maturity
  default [R3] [REG-R33].

**Absent, and not by a switch:** the **commercial bonus devices** the product specification
records — AXA's *Eurocroissance +* adds **+2 %** to the base rate on 2026 payments subject to
a **≥ 45 %** unit-linked condition [S3] [S4]. There is no uplift Reference, no cells, no
model-point column and no eligibility flag, because a marketing promotion is not a term of
the statutory mechanics this model demonstrates. Adding one would mean a rate overlay on
`asset_return()` and an eligibility field the composite has no basis to populate.

## Inputs are external files

The five input CSVs live **in this directory**, beside `run.py` — not inside the model
folder. `EC_FR_S/` holds nothing but formulas:

```
products/eurocroissance/
  model_point_table.csv        <- inputs live here
  mort_table.csv
  lapse_table.csv
  scenario_table.csv
  tec_curve.csv
  run.py
  model.md
  product-spec.md              <- the documents this model implements
  technical-notes.md
  sources.md
  EC_FR_S/                     <- formulas only
    __init__.py                   (model docstring)
    _system.json
    Data/__init__.py              (reads the CSVs, once per model)
    Projection/__init__.py        (the by-policy projection)
```

This follows lifelib's `annuallife/TradLife_A`. `Projection` is parameterized by
`point_id`, so the CSV readers live in an unparameterized **`Data`** Space and each file
is read once per model rather than once per model point; a test counts the reads.

| Reference | Cells | File |
|---|---|---|
| `model_point_file` | `model_point_table()` | `model_point_table.csv` |
| `mort_table_file` | `mort_table()` | `mort_table.csv` |
| `lapse_table_file` | `lapse_table()` | `lapse_table.csv` |
| `scenario_table_file` | `scenario_table()` | `scenario_table.csv` |
| `tec_curve_file` | `tec_curve()` | `tec_curve.csv` |

| File | Contents | Provenance |
|---|---|---|
| `model_point_table.csv` | Eleven model points. **Points 1 and 2 are the worked example's two chassis** on one asset path — €10 000 gross at issue, €2 000 at the end of policy year 3 (`t` = 2), `g` = 100 %, `n` = 10, male 57, decrements off; point 3 is point 1 at `g` = 80 %; point 4 is point 2 with a statutory-maximum *apport d'actifs* at the end of policy year 6 (`t` = 5); points 5-11 turn the decrements on and exercise the variants — *rachats partiels*, a downside path that leaves Chassis B under its guarantee, an in-force cell at duration 4, an exit charge and surrender indemnity with no death floor, a lock-up with scheduled *versements*, a sloped TEC curve, and a negative TEC that floors `i_pm` at zero | anchor cells **[std]**, sizes and age from [R13]; guarantee level and term [S1] [S2] |
| `mort_table.csv` | Base annual mortality by sex and *âge atteint* 18-120, capped at 1 | **[std]** INSEE-shaped Makeham proxy [REG-R24], anchored so that the 80 % best-estimate factor gives exactly 0.5000 % at male 57 — *not* TH 00-02 / TF 00-02, which are cited by arrêté and never shipped [REG-R22] [REG-R23] |
| `lapse_table.csv` | Annual *rachat total* 2.5 % level, and *rachat partiel* 6 % in policy years 1-2 then 3 %, keyed by the 1-based `policy_year` | **[std]**; [R13] observes 2 %-3 % and 6 % then 2 %-4 %, and no other eurocroissance lapse experience is public |
| `scenario_table.csv` | Gross asset return net of asset management fees, by scenario and elapsed year end. `shock` is the notes' path: 4.00 % through policy year 5, **−25.00 %** in policy year 6, 6.00 % after | scenario **[std]**; the fee levels 0.20 % / 0.10 % from [R13] |
| `tec_curve.csv` | The TEC term structure at maturities 1, 2, 5, 10, 20 and 30, by scenario and elapsed time point `k` | **[std]**; the macro anchor is the 10-year OAT averaging 3.0 % in 2023 and 2024 [R19] |

Two of these are **scenario** files rather than assumption files, and that is a product
statement. `i_pm` is 90 % of the TEC [R3 A. 134-1](#frlib-eurocroissance-r3), read at the remaining maturity **[std]**, so the level
*and the slope* of the curve drive the *provision mathématique* directly — a 150 bp fall
adds 587.44 to `pm(5)` in the worked example, more than twice the year's time effect. A
model that carried a flat TEC in a `Projection` Reference would not be modelling this
product's dominant risk, so the curve is a table with a maturity dimension and
`tec_rate()` interpolates across it exactly as the article requires.

## Sign convention

`liability_cf(t)` prints **outgo positive**, as the technical notes print it: claims and
*rachats partiels* and expenses out, *versements* in. `net_cf(t) = −liability_cf(t)` is
the library's **income-positive** sign, so `result_cf()["net_cf"]` can be compared and
summed across products without checking which one it came from. The two are exact
negatives of each other by construction, and a test asserts it.

Neither the two provisions nor the insurer's own-funds items appear in either. The
provisions are state variables and reach the flows only through the claim formulas; the
contribution and the PGT are capital, not benefit. `charges_taken` and `rider_claims` are
published in `result_cf()` as **memo lines outside `net_cf`** — the first is a transfer
inside the account from the savers' provisions to the insurer, and the second is already
inside `claims_death`.

The first column, `pols_if`, is the **start**-of-period in-force count, which is the exposure
every flow on that same row is weighted by. `result_cf()["pols_if"].iloc[0]` is therefore
`pols_if_init()` on every model point, and a flow divided by its own row's `pols_if` is the
per-policy amount. The technical notes' `l(t)` — the count at the **end** of period `t`, nil
on the last projected row — is a different series and is reached as
`pols_if_at(t, "AFT_DECR")`;
it is not published in `result_cf()`. It weights the maintenance expense, and nothing else —
together with `pols_if(t)` itself in the first projected period, where the provisions are
struck twice: once when the initial *versement* creates them and once at that period's year
end.

## Naming

| Notes symbol | Cells | Why it needed care |
|---|---|---|
| `pd(t)` | `prov_div(t)` | `pd` is **pandas** in every model in this library. Shadowing it inside the one Space that has to build a `DataFrame` is not worth a two-letter symmetry, so the *provision de diversification* is spelled out and the *provision mathématique* keeps `pm`, whose symbol was free. |
| `pm_ifo` | *(not an input)* | R. 134-2 makes the PM the guarantee discounted at the **current** rate, so an extract cannot supply it and a projection cannot roll it forward. The column is shipped and read by `check_pm_restruck()` alone. |
| `w(t)`, partial *rachat* | `lapse_rate(t)`, `wd_rate(t)` | Two different events. A full surrender removes the policy; a partial one runs the guarantee, the parts and the assets down pro rata and leaves the contract in force. Sharing one name would have merged a decrement with an owner election. |
| *(exit charge)* | `wd_gross_pp(t)`, `wd_pp(t)` | What leaves the provision and what reaches the saver. The provision run-down keys off the gross amount, the cash flow off the net one. |
| `pm + N·u` | `provision_value(t)` | One expression for both chassis, because `pm` is identically zero on Chassis B — so R. 134-5 and R. 134-6 are one formula each rather than two. |
| `l(t)` | `pols_if_at(t, "AFT_DECR")` | The notes index the in-force probability at the **end** of the period, so the last projected row carries nil. The bare name `pols_if(t)` is the library's **start**-of-period count — the notes' `l(t−1)`, and the weight on that same `result_cf()` row's flows — so `result_cf()["pols_if"].iloc[0]` is `pols_if_init()` exactly. The model first published `l(t)` under the bare name, which put the exposure column one year ahead of the flows beside it; the quantity is unchanged, only the name it is reached by. |
| — | `premium_initial_pp(t)`, `prem_init_after_charge()` | The initial *versement* and its net amount. They are separate from `premium_gross_pp(t)`, the *scheduled* one, because the initial *versement* is the **opening state** of the first projected period — `own_assets_at(t, "BOY")` already carries it net of the entry charge — while still being a cash flow of that period, which is why it is in `total_premium_pp(t)`. |
| — | `*_at(t, "BOY")` | The opening timings — on `own_assets`, `mg`, `pm`, `prov_div`, `parts`, `part_value`, `cum_prem_net` and `provision_value`. This is where the issue instant lives, and where an in-force extract is seeded and `check_pm_restruck()` reads it. |
| — | `av_pp_at` | **Absent, deliberately.** A eurocroissance engagement is not an account value: the saver's rights are a number of *parts* whose value is common to the whole auxiliary account [R2 R. 134-2](#frlib-eurocroissance-r2), plus — on Chassis A — a share of a discounted promise. Naming either the library's account value would assert something false about the contract. |

## Standardizations used

Everything in this list is **[std]**. The annual grid, against A. 134-5's at-least-monthly
intermediate value and its forward part value for exits [R3]. The charge levels — entry
2.00 %, parts levy 0.80 % p.a., performance levy 10 %, exit 0 %, surrender indemnity 0 % —
and the routing of the recurring charge through base 4°; the levels come from [R13] and
[S8], the routing does not. The minimum part value of €5.0000, nowhere published for any
insurer. The initial part value of €10.0000. The credit-balance route that raises the part
value rather than awarding parts. The reference TEC levels and the whole curve shape. The
asset-return paths. The insurer's contribution earning nothing for the savers and being
released as soon as representation permits. The mortality proxy and the 80 % best-estimate
factor. The full and partial *rachat* levels and all three behavioural overlays. Expenses:
acquisition 5 % of *versements*, acquisition commission 2 % of the initial one, maintenance
0.20 % p.a. of the two provisions, all from [R13]. Death before surrender as the
processing order, 100 % of survivors taking the maturity amount, and *âge atteint* as the
age basis, since A. 335-1 fixes no model age basis [REG-R23]. The PCDD and the
*apport d'actifs* at zero in the base run. Reading A. 134-1's index maturity as the
**remaining** term `n − k` at each valuation time `k`, which the article does not state. The
**PGT without its survival factor**, one of the two cash-flow drivers A. 134-2 admits.
Returning a zero surrender indemnity beyond ten years unconditionally, which takes up a
permission R. 132-5-3 grants rather than obeying a prohibition it does not impose.
Publishing `pols_if` as the **start**-of-period count, the library's shared vocabulary, with
the notes' end-of-period `l(t)` reached as `pols_if_at(t, "AFT_DECR")`. Charging the
maintenance expense **at each striking of the provisions**, so the first projected period
carries two — the striking the initial *versement* (or the in-force extract) creates and
that period's own year end — which is the merged issue instant, and leaves the total
maintenance over the contract exactly what it was.

## Tests

`tests/test_eurocroissance_fr.py` asserts both chassis of the worked example row by row to
the cent — the opening state the initial *versement* creates, the asset roll, the parts
levy and its legal base, the performance levy and its
asymmetry, the re-strike of the PM and its rate/time decomposition, the minimum part value
and the insurer's contribution it creates, the *versement* split at the end of policy year
3 on both chassis,
the PGT and its run-off, the A. 134-3 gates and the A. 134-4 headroom — plus one test per
modelling pitfall the notes list, each named for the failure it catches, and all nine
invariant checks on every model point.

The goldens are keyed by the 0-based period index, so row `t` is the close of policy year
`t + 1`, and the notes' opening line is asserted separately against the `"BOY"` timings.
`test_result_cf_shape_and_what_it_leaves_out` pins the frame at
`range(proj_start(), proj_len())` — ten rows on the worked example, not eleven — and
`tests/test_model_conventions_fr.py` pins the same rule across the library.

```bash
python -m pytest tests -q
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #frlib-eurocroissance-r1
[R10]: #frlib-eurocroissance-r10
[R13]: #frlib-eurocroissance-r13
[R14]: #frlib-eurocroissance-r14
[R19]: #frlib-eurocroissance-r19
[R2]: #frlib-eurocroissance-r2
[R21]: #frlib-eurocroissance-r21
[R3]: #frlib-eurocroissance-r3
[R7]: #frlib-eurocroissance-r7
[REG-R17]: #frlib-reg-r17
[REG-R18]: #frlib-reg-r18
[REG-R21]: #frlib-reg-r21
[REG-R22]: #frlib-reg-r22
[REG-R23]: #frlib-reg-r23
[REG-R24]: #frlib-reg-r24
[REG-R33]: #frlib-reg-r33
[REG-R40]: #frlib-reg-r40
[std]: #frlib-std
<!-- END generated citation links -->
