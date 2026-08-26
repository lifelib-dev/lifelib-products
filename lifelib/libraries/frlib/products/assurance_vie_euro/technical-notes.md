# Technical Notes

**Status:** Draft, 2026-08-26 (all cited sources accessed 2026-08-26).

**Scope note.** These notes specify a reference liability cash-flow projection model for
the standardized composite euro support defined in `product-spec.md` (same directory).
This is not any single insurer's fund. [S#]/[R#] tags refer to the source list in
`sources.md` (numbering carried from `_research/assurance-vie-euro.md`); [REG-R#] tags
refer to the cross-product reference library
`references/regulatory-and-actuarial-references.md` (its own frozen R1–R49 numbering).
**[std]** marks standardizations introduced for the reference implementation;
[unverified] marks claims not confirmed against a retrieved document. Parameter values
are identical to those in `product-spec.md`. The mechanics anchors are the insurers'
own booklets [S1] [S2] [S3] [S4] [S9]; the statutory arithmetic is arts. A132-10 to
A132-17 of the Code des assurances [R5] [REG-R15] [REG-R16]; the quantitative anchor is
the ACPR's 2025 revaluation study [R14]. The model is `Euro_FR_A`, an **annual** model,
`t` counted in policy years from the valuation date.

---

## Model scope and conventions

- **Purpose.** Project gross best-estimate liability cash flows — `versements` in;
  `rachats partiels`, death and total-surrender claims out; insurer expenses — for single
  model points on the euro support, together with the two state variables that make the
  product what it is: the `épargne acquise` and the `provision pour participation aux
  bénéfices` (PPB). Reserves are not computed here (see Valuation and reserve pointers).
- **The euro support only.** The UC compartment of a multisupport contract is a separate
  liability with a separate levy regime [R9], outside the A132-11 machinery
  [R5, art. A132-10](#frlib-assurance_vie_euro-r5); it is the sibling product `assurance_vie_uc`. `Arbitrages` between
  supports are out of scope.
- **Projection frequency.** Annual **[std]**: the PB is fixed for the closing year and
  credited at 31 December value date [S1] [S2] [S6] [S7] [S9], and the eight-year PPB
  clock counts financial years [R5, art. A132-16](#frlib-assurance_vie_euro-r5). Sub-annual mechanics — BoursoVie's
  daily compounding [S1], the `pro rata temporis` in-year floor rate for a mid-year
  `dénouement` [S1] [S2] [S11] — are compressed to annual equivalents and named as
  pitfalls below.
- **Timing conventions [std].** `Versements` and `rachats partiels` are spread evenly
  through the year and enter the crediting base at weight 0.5; the year's revalorisation
  and the `frais de gestion sur encours` land at 31 December; decrements act at 31
  December **after** crediting, so an exiting policy takes the full year's `taux servi`.
  That follows BoursoVie, which credits the annual PB to sums surrendered during the year
  provided the adhesion is in force on the following 1 January [S1], and Afer, which tops
  the in-year floor rate up to the definitive rate the following year [S11]. The
  alternative — `pro rata` at the TMG only, which with a zero TMG means no in-year
  interest at all [S1] — is a pitfall below, not the base.
- **The `taux servi` is a net rate.** `ts_net(t)` is the credited rate in the ACPR's
  sense, "net de prélèvements sur encours et avant prélèvements sociaux" [R14]. The
  `frais de gestion sur encours` is *inside* it and is reported only as a decomposition;
  deducting it again is the likeliest implementation error and the first pitfall below.
- **Age basis** age last birthday **[std]** — no retrieved French document fixes one, and
  mortality here drives the timing of `dénouement`, not the benefit amount.
  **Currency** EUR; single-policy model points projected on an expected basis, `pols_if(t)`
  multiplying per-policy amounts. **Rounding** full precision internally, reported cash
  flows to the cent **[std]**.
- **Out of scope, and said so.** The HCSF surrender-suspension power under art. L631-2-1
  5° ter [R8] [REG-R13] is **not modeled**, nor is the exceptional PPB `reprise` of art.
  A132-16-1 [REG-R16]. Both are solvency-stress management actions, both would materially
  change a mass-surrender projection, and neither has a published trigger a deterministic
  model could key off. A mass-lapse stress run here is a *pre-management-action* result.

---

## Model point attributes

| Attribute | Type | Example (worked configuration) |
|---|---|---|
| `point_id` | int | 1 |
| `policy_id` | str | FR-AVE-0001 |
| `sex` | enum {M, F} | M |
| `issue_age` | int, age at `adhésion` | 55 |
| `duration_init` | int, completed policy years at the valuation date | 5 |
| `pols_if_init` | float, policies represented | 1.0 |
| `av_pp_init` | currency, `épargne acquise` at the valuation date | 100 000.00 |
| `ppb_pp_init` | currency, PPB attributed to the model point | 4 000.00 |
| `ppb_vintages_init` | int, equal open vintages the opening PPB is split across | 8 |
| `prem_gross_pp` | currency p.a., `versements libres programmés` | 2 400.00 |
| `prem_charge_rate` | rate, `frais sur versement` | 0.0000 |
| `wd_pp` | currency p.a., `rachats partiels programmés` | 3 000.00 |
| `wd_start_year` | int, first projection year the programmed surrender runs | 6 |
| `fee_rate` | rate p.a., `frais de gestion sur encours` | 0.0060 |
| `tmg_rate` | rate p.a., `taux minimum garanti` | 0.0000 |
| `ts_target` | rate p.a., the insurer's target `taux servi`, net | 0.0230 |
| `soc_levy_rate` | rate, `prélèvements sociaux` | 0.1720 |
| `guarantee_form` | enum {gross, net} | net |
| `avance_on` | bool, `avance` outstanding | 0 |
| `scenario_id` | str, names the `r_fin` path in `fin_rate_table.csv` | base |

Every attribute name, every column of `model_point_table.csv` and every cells name is
English `lower_snake_case`, per the shared vocabulary; the French names stay in the prose,
where they are the name of the thing. `model_point()` selects the row, `age(t)` is
`issue_age + duration_init + t − 1`, and `proj_len()` is 40 years **[std]** — the euro
support has no term, so the horizon is a modeling choice, not a contract fact.

---

## State variables

| Variable | Description | Updated |
|---|---|---|
| `av_pp(t)` | `épargne acquise` per policy at the **start** of policy year `t` | annual recursion |
| `av_pp_at(t, timing)` | the within-year points of the same balance: `"BEF_PREM"`, `"AFT_PREM"`, `"AFT_WD"`, `"AFT_INT"` | within year `t` |
| `av_at(t, timing)` | `av_pp_at(t, timing) × pols_if(t)`, the fund-level balance | within year `t` |
| `ppb_pp(t)` | PPB attributed to the model point at the start of year `t` | annual recursion |
| `ppb_vintage_pp(t, v)` | remaining balance of the dotation carried in financial year `v`, at the start of year `t`; released FIFO | annual |
| `pb_cum_pp(t)` | cumulative PB credited since the valuation date — the `effet cliquet` ledger | annual, non-decreasing |
| `soc_levy_cum_pp(t)` | cumulative `prélèvements sociaux` deducted from the account | annual, non-decreasing |
| `guar_floor_pp(t)` | contractual capital floor: `versements` net of `frais sur versement`, less `rachats`, less cumulative `frais de gestion` | annual |
| `ts_net(t)` | `taux servi` credited for year `t` (net of charges on encours, before social levies) | annual, crediting rule |
| `pols_if(t)` | policies in force at the start of year `t`; `pols_if_at(t, timing)` gives `"BEF_DECR"` / `"BEF_LAPSE"` / `"AFT_DECR"` | annual decrements |

---

## Assumption inputs

Three classes are distinguished. Class (a) is contractual or statutory and is cited;
class (b) is the insurer's current discretionary scale, revisable annually within the
statutory floor [R5] and the eight-year clock [REG-R16]; class (c) is the modeler's view
of experience.

### (a) Contractual / guaranteed elements (cited)

| Input | Value | Basis |
|---|---|---|
| `frais sur versement` | 0.00% | [S1] [S3] [S13] |
| `frais de gestion sur encours` | 0.60% p.a., levied 31 December, pro rata temporis on in-year movements | [S3]; timing [S1] [S2] [S9]; level choice **[std]**, product-spec (4) |
| Capital guarantee | `versements` net of entry charges, **less** the annual management charges, measured before social and tax levies | [S3] [S5] [S6] [S7]; measurement [S1] [S2] [S3] |
| `Effet cliquet` | credited PB is definitively acquired and cannot be called back | [S1] [S9] |
| `Taux minimum garanti` | 0.00% p.a. | **[std]**, product-spec (7) |
| Statutory PB floor | 85% of the `compte financier` balance, plus the `compte technique` balance less the greater of 10% of its credit balance and 4.5% of annual premiums | [R5, art. A132-11](#frlib-assurance_vie_euro-r5) [R6] [R14, fn 12](#frlib-assurance_vie_euro-r14) [REG-R15] |
| Statutory minimum benefit | that credit balance less interest already credited to mathematical provisions | [R5, art. A132-12](#frlib-assurance_vie_euro-r5) [REG-R15] |
| PPB release horizon | eight financial years following the year of the dotation | [R5, art. A132-16](#frlib-assurance_vie_euro-r5) [R6] [S2] [REG-R16] |
| Death benefit | the `épargne acquise`, less outstanding `avances` and interest; **no additional guarantee** | [S3] |
| Surrender charge | 0.00%; settlement two months by statute, 30 days by contract | [S2] [S10] [S13]; [R7] [REG-R31]; [S3] [S6] |
| `Prélèvements sociaux` | 17.2%, on the products **as credited to the contract** each year | rate [S3]; timing [R9, art. L136-7 II](#frlib-assurance_vie_euro-r9) |

### (b) Insurer-discretionary current elements (snapshot; revisable annually)

| Input | Value | Basis |
|---|---|---|
| Target `taux servi` `ts_target` | 2.30% p.a. net, level | **[std]**, product-spec (9); market context [R14] |
| Crediting rule | credit `ts_target` where the PPB allows, never below `tmg_rate`, and always allocate the year's statutory minimum PB in full — credited or carried to the PPB; forced releases override the target upward | **[std]** (i) |
| PPB dotation policy | the excess of the statutory minimum PB over the target, carried to a new vintage | **[std]** (i) |
| PPB release order | FIFO, oldest vintage first | **[std]** (ii) |
| PPB earns no separate return | the return on PPB assets enters the `compte financier` instead, per the A132-14 basis of average technical provisions | [REG-R15]; convention **[std]** (iii) |
| Opening PPB | 4.0% of `av_pp_init`, in eight equal vintages | [R14] [REG-R47]; split **[std]**, product-spec (11) |
| UC-holding bonus | none | [R14]; exclusion **[std]**, product-spec (10) |
| Year-on-year cap on `ts_net` | none | **[std]** (iv) |

Footnotes: (i) No insurer publishes its dotation or release policy; only the outer bounds
are public — at least 85% of the `compte financier` and the A132-11 technical share must
reach policyholders [R5], and the PPB must be released within eight years [REG-R16].
Aggregate levels are (4.0% of provisions at end-2025 [R14]; EUR 53.6 bn, −11.1% year on
year, at end-2024 [REG-R47]), but no insurer publishes its own rule. (ii) The statute
prescribes no release order; FIFO is the only order that satisfies the eight-year
constraint without slack, and it makes `ppb_vintage_pp` testable. (iii) A132-14 computes
the financial result as average technical provisions times a `taux de rendement des
placements` [REG-R15] and the PPB is one of those provisions [REG-R6], so PPB assets earn
inside the `compte financier` and the vintage balances stay nominal; accreting the
vintages *and* including the PPB in the financial base double-counts. (iv) French insurers
do smooth the announced rate, but the PPB **is** the smoothing device here, and a second
cap on the year-on-year change would let the model credit rates the fund cannot fund.

### (c) Behavioral / experience assumptions (modeler's view)

No French euro-fund lapse experience is public: the ACPR publishes only aggregate flows —
EUR 71.0 bn of surrenders against EUR 1 361 bn of guaranteed-capital encours in 2025 —
with no split by duration, age or vintage [R15]. Every shape below is therefore **[std]**,
rationalized from the product's incentive structure.

| Input | Recommended basis | Basis tags |
|---|---|---|
| Base mortality `mort_rate` | 80% of a sex-distinct redistributable proxy table shaped like French population mortality, *not* the INSEE quotients themselves — the shipped `mort_table.csv` is an analytic Makeham-type curve anchored so that the 80% factor gives the worked example's q = 0.0060 at age 60 exactly | table **[std]** (vii); shape and the only redistributable French series [REG-R24]; permitted-table framework [REG-R23] |
| Base surrender `lapse_rate_base` | 4.0% p.a. at policy durations 1–7; **8.0% at duration 8**; 5.0% at durations 9+ | **[std]**; the duration-8 step is the tax threshold [R10] [R11] [REG-R40] |
| Dynamic surrender | additive in the gap between a market reference rate and `ts_net`: see Policyholder behavior modeling | **[std]** |
| Market reference rate `ref_rate` | 2.20% p.a. — the 2025 average Livret A rate | [R14]; use as the dynamic reference **[std]** |
| Partial-surrender utilisation | the programmed amount, taken in full from projection year `wd_start_year` | **[std]** |
| Insurer expenses | EUR 24 per policy p.a. inflating at 1.5% p.a., plus 0.35% p.a. of the average balance | **[std]** (v) |
| Fund financial rate `r_fin` | scenario path in `fin_rate_table.csv`; base path 3.30% falling to 2.30% over twelve years | **[std]** (vi) |
| `Avance` take-up | 0 | terms unpublished [S1] [S2] [S3]; exclusion **[std]** |

(v) Actual unit expenses are not public. The proportional 0.35% is sized so that the
loading margin leaves the statutory `compte technique` small relative to the `compte
financier`, which is what the market outturn implies: a 0.63% average charge rate against
a 2.8% asset return and a 2.63% credited rate [R14] leaves little technical margin once
distribution costs on encours are paid. The fixed/proportional split is a modeling choice.
(vi) The path is anchored to the ACPR's `taux de rendement de l'actif` — 2.8% in 2025,
2.5% in 2024, near 2.1–2.2% from 2020 to 2023, half of undertakings between 2.4% and 3.3%
[R14] — and to the reinvestment picture behind it: the 10-year OAT averaged 3.4% in 2025
while about 60% of fixed-coupon bonds maturing within four years still carry a coupon
below 3% [R14]. It is a scenario, not a forecast.
(vii) The shipped table is a synthetic curve, not a data extract. INSEE's T69QMORT
quotients are the only freely redistributable French mortality series and the only
public shape available [REG-R24] — TH 00-02 / TF 00-02 and TGH05 / TGF05 are cited by
name and article [REG-R23] and never shipped — but what `mort_table.csv` contains is a
Makeham-type curve whose first differences of `q` by age grow by a constant factor from
18 to 100, with `q(M, 60)` set to exactly 0.0075 so that the 0.8 best-estimate factor
reproduces this table's 0.0060 placeholder to the digit. Read it as a smooth stand-in of
roughly the right level and slope, not as population quotients scaled by 0.8, and do not
lift it for any purpose that needs actual French population mortality.

---

## Cash flow components and recursions

### Notation (defined once, used throughout)

| Symbol | Cells | Meaning |
|---|---|---|
| `t` | — | policy year index, 1, 2, … from the valuation date |
| `AV(t)` | `av_pp(t)` | `épargne acquise` per policy at the start of year `t`; `AV(1) = av_pp_init` |
| `P(t)`, `P_g(t)` | `prem_to_av_pp(t)`, `prem_gross_pp(t)` | `versements` credited net of `frais sur versement`, and before them |
| `W(t)` | `withdrawals_pp(t)` | `rachats partiels` paid during year `t` |
| `B(t)` | `pm_avg_pp(t)` | crediting base: `AV(t) + 0.5·P(t) − 0.5·W(t)` **[std]** |
| `c`, `F(t)` | `fee_rate`, `fee_pp(t)` | `frais de gestion sur encours`, 0.60% p.a.; the amount charged, `c · B(t)` |
| `E(t)`, `r(t)` | `expenses_pp(t)`, `r_fin(t)` | insurer expenses; the fund's financial return rate for year `t` |
| `Φ(t)`, `T(t)` | `fin_acct_pp(t)`, `tech_acct_pp(t)` | `compte financier` balance `r(t)·(B(t) + Q(t))`; `compte technique` balance `F(t) − E(t)` |
| `s(t)` | `insurer_tech_share_pp(t)` | insurer's technical share, `max(0.10·max(T(t),0), 0.045·P_g(t))` |
| `A(t)`, `A⁺(t)` | `pb_acct_pp(t)`, `pb_min_pp(t)` | `compte de participation aux résultats` balance; the statutory minimum PB |
| `Q(t)`, `Q_v(t)` | `ppb_pp(t)`, `ppb_vintage_pp(t, v)` | PPB at the start of year `t`; the remaining balance of the vintage carried in year `v` |
| `D(t)`, `R(t)` | `ppb_dotation_pp(t)`, `ppb_release_pp(t)` | PPB dotation and release in year `t` |
| `X(t)`, `I(t)` | `pb_credited_pp(t)`, `int_credited_pp(t)` | PB credited **gross** of `F(t)`; the net revalorisation added, `X(t) − F(t)` |
| `g`, `s*` | `tmg_rate`, `ts_target` | `taux minimum garanti` 0.00%; the insurer's target `taux servi` 2.30% |
| `ŝ(t)`, `σ(t)` | `ts_stat(t)`, `ts_net(t)` | statutory floor rate and credited `taux servi`, both net of the charge |
| `L(t)`, `G(t)` | `soc_levy_pp(t)`, `guar_floor_pp(t)` | `prélèvements sociaux` `0.172·max(I(t),0)`; the contractual capital floor |
| `q(t)`, `w(t)`, `l(t)` | `mort_rate(t)`, `lapse_rate(t)`, `pols_if(t)` | annual decrement rates; policies in force at the start of year `t`, `l(1) = pols_if_init` |

### Annual processing order [std]

1. **Start of year `t`.** `av_pp_at(t, "BEF_PREM") = av_pp(t) = AV(t)`.
2. **Through the year.** `versements` are received and credited net of the entry charge:
   `P(t) = P_g(t) · (1 − prem_charge_rate)`; `av_pp_at(t, "AFT_PREM") = AV(t) + P(t)`.
3. **Through the year.** `rachats partiels` are paid:
   `av_pp_at(t, "AFT_WD") = av_pp_at(t, "AFT_PREM") − W(t)`.
4. Crediting base struck `pro rata temporis` [S1]: `B(t) = AV(t) + 0.5·P(t) − 0.5·W(t)`.
5. The `compte de participation aux résultats` is built and the statutory minimum `A⁺(t)`
   determined (below).
6. The crediting rule fixes `R(t)`, `D(t)` and hence `X(t)` and `σ(t)` (below).
7. **31 December.** The net revalorisation is credited:
   `I(t) = σ(t)·B(t)`, `av_pp_at(t, "AFT_INT") = av_pp_at(t, "AFT_WD") + I(t)`.
   The `frais de gestion` `F(t) = c·B(t)` is inside `σ(t)`, not a further deduction.
8. **31 December.** `prélèvements sociaux` are withheld: `L(t) = 0.172 · max(I(t), 0)`;
   `av_pp(t+1) = av_pp_at(t, "AFT_INT") − L(t)`.
9. **31 December, after crediting.** Decrements act: deaths at `q(t)`, total surrenders
   at `w(t)`; each releases `av_pp(t+1)` as a claim.
10. `l(t+1) = l(t)·(1 − q(t))·(1 − w(t))`; the PPB vintage ledger rolls forward.

### The `épargne acquise` recursion

```
av_pp(t+1) = av_pp(t) + prem_to_av_pp(t) − withdrawals_pp(t)
             + int_credited_pp(t) − soc_levy_pp(t)

av(t+1)    = av(t) + premiums(t) − withdrawals(t) + int_credited(t) − soc_levy(t)
             − claims_death(t) − claims_lapse(t)
```

The second line is the fund-level form, where the releases appear;
`check_av_roll_fwd()` asserts it every year, with `av(t) = av_pp(t)·pols_if(t)` and every
aggregate the per-policy amount times `pols_if(t)`. The identity is exact because claims
are struck on `av_pp(t+1)`, the same balance the survivors carry forward.

### The `compte de participation aux résultats`

Built annually, per policy, on the two accounts art. A132-11 names [R5] [REG-R15]:

```
fin_acct_pp(t)          = r_fin(t) · ( pm_avg_pp(t) + ppb_pp(t) )
tech_acct_pp(t)         = fee_pp(t) − expenses_pp(t)
insurer_tech_share_pp(t)= max( 0.10 · max(tech_acct_pp(t), 0), 0.045 · prem_gross_pp(t) )
pb_acct_pp(t)           = 0.85 · fin_acct_pp(t)
                          + tech_acct_pp(t) − insurer_tech_share_pp(t)
pb_min_pp(t)            = max( 0, pb_acct_pp(t) − tmg_rate · pm_avg_pp(t) )
ts_stat(t)              = ( pb_min_pp(t) − fee_pp(t) ) / pm_avg_pp(t)
```

Four points of substance. **The 85% attaches to the financial account and the 90% to the
technical account, not the other way round** [R5, art. A132-11](#frlib-assurance_vie_euro-r5) [R14, fn 12](#frlib-assurance_vie_euro-r14) [REG-R15].
**The insurer's technical share has two limbs and the 4.5%-of-premiums limb often binds**,
so the policyholder share of a positive technical balance is at most 90% and can be much
less. **The PPB sits inside the financial base**, because A132-14 computes the financial
result on average technical provisions [REG-R15] and the PPB is one of them [REG-R6]. And
**`ts_stat(t)` is net of the charge**: `pb_min_pp` is gross of `fee_pp` because the charge
is a credit to the technical account, so it is subtracted once to reach the rate the
account actually grows by. For the euro support the underwriting result is nil — the death
benefit is the account value [S3] — so `tech_acct_pp` is the loading result alone. A
contract with a contractual PB percentage (90% at Suravenir Rendement [S4], 100% at Afer
[S9]) replaces the first line with that percentage of the ring-fenced fund's net financial
profits.

### The crediting rule, the TMG and the PPB lever

```
pb_target_pp(t)  = ts_target · pm_avg_pp(t) + fee_pp(t)
ppb_dotation_pp(t)  = max( 0, pb_min_pp(t) − pb_target_pp(t) )
ppb_discr_rel_pp(t) = min( max(0, pb_target_pp(t) − pb_min_pp(t)), ppb_pp(t) )
ppb_forced_pp(t)    = Σ_v { ppb_vintage_pp(t, v) : v + 8 ≤ t }
ppb_release_pp(t)   = max( ppb_discr_rel_pp(t), ppb_forced_pp(t) )
pb_credited_pp(t)   = pb_min_pp(t) − ppb_dotation_pp(t) + ppb_release_pp(t)
ts_net(t)           = max( tmg_rate,
                           ( pb_credited_pp(t) − fee_pp(t) ) / pm_avg_pp(t) )
int_credited_pp(t)  = ts_net(t) · pm_avg_pp(t)
```

Read it as three levers on one rate. The **statutory floor** `ts_stat(t)` is what the
year's result alone obliges the insurer to credit. The **PPB** moves the credited rate
above or below that floor: a dotation parks this year's excess, a release spends an
earlier year's. The **TMG** is a hard floor under the result, and because it guarantees
technical interest *plus* PB together [R3] [REG-R18] it is a floor on `ts_net`, not a
separate credit stacked on top — with `tmg_rate = 0` it never binds here, but a positive
TMG binds through the PPB, forcing a release the insurer did not choose. A dotation and a
forced release can coexist in one year — this year's excess goes in while an eight-year-old
vintage comes out — and both appear in the worked example's first three rows.

### The PPB and its eight-year clock

```
ppb_pp(t+1) = ppb_pp(t) + ppb_dotation_pp(t) − ppb_release_pp(t)
```

with the vintage ledger `ppb_vintage_pp(t, v)` carrying the detail: `ppb_dotation_pp(t)`
opens vintage `t`, `ppb_release_pp(t)` is drawn FIFO from the oldest open vintage forward,
and a vintage carried in year `v` must be exhausted by the end of year `v + 8`
[R5, art. A132-16](#frlib-assurance_vie_euro-r5) [REG-R16]. `check_ppb_roll_fwd()` asserts the balance identity and
`check_ppb_clock()` that `ppb_vintage_pp(t, v) = 0` for every `v ≤ t − 9` — one year past
the deadline, because `ppb_vintage_pp(t, v)` is a *start*-of-year balance and the vintage
with `v = t − 8` is still standing at the start of the year that forces it out. The
opening balance `ppb_pp_init` is
split into `ppb_vintages_init` equal vintages carried in years `0, −1, …, −7`, falling due
in projection years `8, 7, …, 1` **[std]**. The PPB is bounded below by zero — a negative
PPB is not a permitted state, and the exceptional `reprise` of art. A132-16-1 is a
supervised recovery measure, not a projection lever [REG-R16]. When `ppb_pp(t) = 0` and
`ts_stat(t) < ts_target`, the model credits `ts_stat(t)`.

### `Prélèvements sociaux`

```
soc_levy_pp(t)     = soc_levy_rate · max( int_credited_pp(t), 0 )
soc_levy_cum_pp(t) = Σ_{u<t} soc_levy_pp(u)
```

The levy is taken **as the interest is credited**, every year, whether or not anything is
withdrawn, because the rights are expressed in euros [R9, art. L136-7 II](#frlib-assurance_vie_euro-r9); the rate is
17.2% [S3]. **It sits inside the account roll-forward and outside `net_cf`.** Inside,
because it is money that genuinely leaves the contract each year, and a model that defers
it to surrender overstates the account and every benefit measured on it. Outside `net_cf`,
because `net_cf` is the insurer's liability stream while the levy is a policyholder tax
the insurer withholds and remits to the State — neither a benefit nor an insurer expense.
It is reported in its own `soc_levy` column of `result_cf()`, so a fund-level asset
projection adds it back as an outflow in one step. The base is the interest actually
inscribed on the contract, i.e. net of the management charge, which is **[std]**: art.
L136-7 fixes the timing but not the base [R9] (product-spec footnote 13).

### The capital guarantee floor and the `effet cliquet`

```
guar_floor_pp(t+1) = guar_floor_pp(t) + prem_to_av_pp(t) − withdrawals_pp(t) − fee_pp(t)

check_guar_floor():  av_pp(t) + soc_levy_cum_pp(t) ≥ guar_floor_pp(t)   for all t
check_cliquet():     pb_cum_pp(t+1) = pb_cum_pp(t) + max(pb_credited_pp(t), 0)
                     and pb_credited_pp(t) ≥ 0 and ts_net(t) ≥ tmg_rate  for all t
```

The floor recursion is the `guarantee_form = "net"` form [S3] [S5] [S6] [S7]; the
`"gross"` variant drops the `− fee_pp(t)` term [S4] [S8] [S9]. For an in-force cell the
premium history before the valuation date is not carried in the model point, so the floor
is seeded at `guar_floor_pp(1) = av_pp_init` **[std]** — deliberately conservative, since
the true floor on a five-year-old contract sits below its account value by the interest
already credited. It is tested on the account
value **before** cumulative social levies, because the published minimum surrender-value
tables are stated before social and tax levies [S1] [S2] [S3]. The `effet cliquet` is a
separate and weaker invariant, and conflating the two is a pitfall: what is ratcheted is
**credited PB**, not the balance. On a `garantie nette` contract the balance can fall in a
year that would need `ts_net(t) < 0` to cover the charge — the charge keeps biting, the
ratchet does not undo it, and both statements are true at once [S6] [S9].

### Decrements, claims and cash flow outputs

```
pols_death(t)  = pols_if(t) · mort_rate(t)
pols_lapse(t)  = pols_if(t) · (1 − mort_rate(t)) · lapse_rate(t)
pols_if(t+1)   = pols_if(t) − pols_death(t) − pols_lapse(t)
db_pp(t)       = av_pp(t+1)          death benefit: the épargne acquise, no uplift  [S3]
cv_pp(t)       = av_pp(t+1)          surrender value: no penalty  [S2] [S10] [S13]
claims(t, "DEATH") = pols_death(t) · db_pp(t)
claims(t, "LAPSE") = pols_lapse(t) · cv_pp(t)
```

There is no maturity decrement: the euro support has no term, and the contract's stated
maturity, where one exists, is renewable annually without limit [S6]. `result_cf()` is a
DataFrame indexed by `t`, first column `pols_if`, with

| Column | Formula |
|---|---|
| `premiums` | `prem_to_av_pp(t) · pols_if(t)` |
| `withdrawals` | `withdrawals_pp(t) · pols_if(t)` — an owner election, not a claim |
| `claims_death` | `claims(t, "DEATH")` |
| `claims_lapse` | `claims(t, "LAPSE")` |
| `expenses` | `expenses_pp(t) · pols_if(t)` |
| `int_credited` | `int_credited_pp(t) · pols_if(t)` — state movement, reported not summed |
| `soc_levy` | `soc_levy_pp(t) · pols_if(t)` — excluded from `net_cf` |
| `liability_cf` | `claims_death + claims_lapse + withdrawals + expenses − premiums` |
| `net_cf` | `− liability_cf(t)`, income-positive |

### Known modeling pitfalls

Each of these produces a plausible-looking projection that is wrong, and each becomes a
test.

1. **Deducting the management charge twice.** `ts_net(t)` is already net of the `frais de
   gestion sur encours` [R14]; applying `av × (1 + ts_net) × (1 − c)` costs the
   policyholder 0.60% a year that was already taken. Test: with `ts_net = 0` one year's
   movement equals exactly `−c · pm_avg_pp(t)`. The same error in another dress is
   deducting the fund's own 0.24% + 0.03% internal costs [S5], which a rate quoted net of
   contract charges already covers.
2. **Crediting on the closing balance instead of the `pro rata temporis` base.** The PB is
   allocated "weighted by the time the sums were present on the fund during the year"
   [S1]; crediting on `av_pp(t) + P(t) − W(t)` gives a full year's interest on a December
   payment. Test: with `P(t) = W(t) = 0` the two agree; with a payment they differ by
   exactly `0.5 · ts_net(t) · P(t)`.
3. **Getting the statutory split backwards.** "90% of the financial account and 85% of the
   technical result" is the popular form and it is wrong: the article says 85% of the
   `compte financier`, and the technical balance less the greater of 10% of it and 4.5% of
   premiums [R5, art. A132-11](#frlib-assurance_vie_euro-r5) [R14, fn 12](#frlib-assurance_vie_euro-r14) [REG-R15]. Test: with `tech_acct_pp = 0`,
   `pb_acct_pp(t)` equals `0.85 · fin_acct_pp(t)` exactly.
4. **Dropping the 4.5%-of-premiums limb.** With a small technical result and a live
   premium stream, `0.045 · prem_gross_pp(t)` exceeds `0.10 · tech_acct_pp(t)` and takes
   the larger bite. Test: in the worked example year 6,
   `insurer_tech_share_pp = EUR 108.00`, against EUR 28.43 for the 10% limb.
5. **Leaving the PPB out of the financial base.** `fin_acct_pp` is struck on
   `pm_avg_pp + ppb_pp` [REG-R15] [REG-R6]; omitting it understates the distributable
   amount by `0.85 · r_fin · ppb_pp` — EUR 41.81 in worked-example year 6. The mirror
   error is **accreting the vintages as well**, which distributes the PPB's return twice.
   Test: `ppb_vintage_pp(t, v)` changes only by releases.
6. **Releasing the PPB LIFO, or letting a vintage age past eight years.** Test:
   `ppb_vintage_pp(t, v) = 0` for every `v ≤ t − 9` [R5, art. A132-16](#frlib-assurance_vie_euro-r5) [REG-R16] — the
   vintage due *during* year `t` is the one with `v = t − 8`, and it is still standing at
   the start of that year.
7. **Letting the PPB go negative, or losing part of the year's statutory minimum.** A
   dotation year credits *less* than `ts_stat(t)` and that is legal — the balance goes to
   the PPB, not to the insurer — so the invariant is an allocation identity, not a rate
   inequality. Test: `ppb_pp(t) ≥ 0`, `ts_net(t) ≥ tmg_rate`, and
   `pb_credited_pp(t) + ppb_dotation_pp(t) − ppb_release_pp(t) == pb_min_pp(t)` for all
   `t`. `ts_net(t) ≥ ts_stat(t)` happens to hold on every row of the worked example,
   because the forced release always exceeds the dotation; it is not the invariant, and a
   model point with no vintage falling due would break it legitimately.
8. **Levying `prélèvements sociaux` only at surrender.** This is the euro fund's signature
   mechanic and the commonest foreign-model error: the levy is annual on euro-denominated
   rights and deferred only on the UC part [R9]. Test:
   `soc_levy_pp(t) = 0.172 · max(int_credited_pp(t), 0)` every year, and the twelve-year
   total is exactly 17.2% of the twelve-year credited interest.
9. **Levying it on the account rather than on the year's interest.** 17.2% of
   EUR 100 000 is EUR 17 200; 17.2% of year 1's EUR 2 827.60 is EUR 486.35.
10. **Testing the `effet cliquet` as "the account never falls".** Under the `garantie
    nette` the balance falls by the management charge in a zero-PB year, and the tables
    published for exactly that case [S2] [S3] prove it. Ratchet `pb_cum_pp(t)`, not
    `av_pp(t)`. Relatedly, compare the guarantee floor to
    `av_pp(t) + soc_levy_cum_pp(t)`, because the published minimum surrender values are
    stated before social and tax levies [S1] [S2] [S3].
11. **Adding a death-benefit uplift.** The death capital is the `épargne acquise` and
    nothing more [S3]; the optional riders price the **UC** capital at risk [S3] [S4].
    Test: `db_pp(t) == cv_pp(t) == av_pp(t+1)`, and no surrender penalty anywhere
    [S2] [S10] [S13].
12. **Giving mid-year exits a full year's interest silently.** The base model does exactly
    that and says so; the contractual rule is the announced floor rate `pro rata
    temporis`, which with a zero TMG is no in-year interest at all [S1]. Test: the
    alternative timing is a documented switch, and the base is labelled.

---

## Policyholder behavior modeling

All formulas are **[std]**; the shapes are rationalized from the incentive structure and
the aggregate market evidence, and dynamic option-exercise assumptions are the norm this
model is built to feed.

- **Base surrender.** 4.0% p.a. at durations 1–7, **8.0% at duration 8**, 5.0% at
  durations 9+. The duration-8 step is the tax threshold: the reduced 7.5% rate and the
  EUR 4 600 / EUR 9 200 annual allowance both switch on at eight years [R10] [R11]
  [REG-R40], and a French savings projection with no surrender step at duration 8 has
  ignored the single strongest driver of French partial-surrender timing [REG-R40].
- **The dynamic component — the French mechanic.** French surrender behaviour keys on the
  gap between the `taux servi` and the rate available elsewhere, most visibly the Livret A:

  ```
  lapse_dyn_add(t) = a · max( 0, ref_rate(t) − ts_net(t) − tol )
  lapse_rate(t)    = min( lapse_cap, lapse_rate_base(t) + lapse_dyn_add(t) )
  ```

  with `a = 4.0`, `tol = 0.25` point, `lapse_cap = 30%` **[std]**, and
  `ref_rate(t) = 2.20%`, the 2025 Livret A average [R14]. The sign of the relationship is
  observed rather than assumed: in 2025 the euro rate was 2.63% while the Livret A
  averaged 2.20% and fell from 2.4% to 1.7% in August and 1.5% in February 2026 [R14]
  [R15], and euro supports turned to a **+EUR 6.4 bn** net inflow after five consecutive
  years of net outflow [R15]. The magnitude — `a`, `tol` and the cap — has no public
  calibration and is the most consequential [std] in this file.
- **Asymmetry.** The dynamic term is one-sided: a `taux servi` above the reference rate
  does not push surrenders below the base, because the base already reflects needs-driven
  withdrawals. A two-sided variant is a scenario switch.
- **Partial before total.** Absent instruction an unspecified withdrawal drains the euro
  fund before the UC supports [S1] — in a euro-only model, a reminder that
  `withdrawals(t)` on a multisupport contract lands here first. The 30-day renunciation
  unwind [REG-R29] [S2] [S6] [S9] is a first-duration effect the anchor cell, at duration
  5, is past; a new-business cell needs it.
- **What the model deliberately does not do.** No `avance` take-up (terms unpublished
  [S1] [S2] [S3]); no beneficiary-acceptance block on liquidity, which is a real and
  absolute constraint [S1] [S3]; no mass-surrender scenario with the HCSF response
  [R8] [REG-R13]. The last is the important one: a mass-lapse stress here is a
  pre-management-action number, because the supervisor's power to freeze surrenders for up
  to six consecutive months is precisely what would change the answer.

---

## Worked example

Anchor cell, product-spec "Anchor model cell": `av_pp_init = EUR 100 000.00` at duration
5, male age 60; `prem_gross_pp = EUR 2 400.00` p.a. and `prem_charge_rate = 0`, so
`prem_to_av_pp = EUR 2 400.00`, spread evenly through the year; `withdrawals_pp =
EUR 3 000.00` p.a. from projection year 6, likewise spread evenly; `fee_rate = 0.60%`;
`tmg_rate = 0.00%`; `ts_target = 2.30%`; `soc_levy_rate = 17.2%`;
`ppb_pp_init = EUR 4 000.00` in eight equal vintages of EUR 500.00 falling due in
projection years 1 to 8; expenses EUR 24.00 p.a. inflating at 1.5% plus 0.35% of
`pm_avg_pp`; `r_fin` on the base path below. Twelve years are shown of the 40-year
`proj_len()`. Currency cells are full-precision model values rounded to the cent,
so a printed row reproduces the next row's opening balance to within EUR 0.01; assertions
are to EUR 0.01 and to the displayed precision on rates.

**Table 1 — the `taux servi` and the PPB.**

| `t` | `r_fin(t)` | `pm_avg_pp(t)` | 0.85 × `fin_acct_pp(t)` | policyholder technical share | `pb_min_pp(t)` | `ts_stat(t)` | PPB release (+) / dotation (−) | `ppb_pp(t+1)` | `ts_net(t)` |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 3.30% | 101 200.00 | 2 950.86 | 121.00 | 3 071.86 | 2.4354% | 362.94 | 3 637.06 | 2.7941% |
| 2 | 3.25% | 105 941.25 | 3 027.10 | 132.49 | 3 159.59 | 2.3824% | 412.70 | 3 224.36 | 2.7720% |
| 3 | 3.20% | 110 772.80 | 3 100.72 | 144.21 | 3 244.93 | 2.3294% | 467.48 | 2 756.88 | 2.7514% |
| 4 | 3.10% | 115 696.36 | 3 121.24 | 156.14 | 3 277.39 | 2.2327% | 500.00 | 2 256.88 | 2.6649% |
| 5 | 2.95% | 120 649.25 | 3 081.87 | 168.15 | 3 250.02 | 2.0938% | 500.00 | 1 756.88 | 2.5082% |
| 6 | 2.80% | 124 054.88 | 2 994.32 | 176.28 | 3 170.60 | 1.9558% | 500.00 | 1 256.88 | 2.3589% |
| 7 | 2.65% | 125 877.84 | 2 863.71 | 180.45 | 3 044.16 | 1.8183% | 606.30 | 650.58 | 2.3000% |
| 8 | 2.55% | 127 675.06 | 2 781.46 | 184.55 | 2 966.01 | 1.7231% | 650.58 | 0.00 | 2.2327% |
| 9 | 2.45% | 129 435.30 | 2 695.49 | 188.55 | 2 884.04 | 1.6282% | 0.00 | 0.00 | 1.6282% |
| 10 | 2.40% | 130 580.26 | 2 663.84 | 191.01 | 2 854.85 | 1.5863% | 0.00 | 0.00 | 1.5863% |
| 11 | 2.35% | 131 695.35 | 2 630.61 | 193.39 | 2 824.00 | 1.5443% | 0.00 | 0.00 | 1.5443% |
| 12 | 2.30% | 132 779.35 | 2 595.84 | 195.68 | 2 791.51 | 1.5024% | 0.00 | 0.00 | 1.5024% |

**Table 2 — the `épargne acquise` roll-forward.**

| `t` | `av_pp(t)` | `prem_to_av_pp(t)` | `withdrawals_pp(t)` | `int_credited_pp(t)` | `soc_levy_pp(t)` | `av_pp(t+1)` |
|---|---|---|---|---|---|---|
| 1 | 100 000.00 | 2 400.00 | 0.00 | 2 827.60 | 486.35 | 104 741.25 |
| 2 | 104 741.25 | 2 400.00 | 0.00 | 2 936.65 | 505.10 | 109 572.80 |
| 3 | 109 572.80 | 2 400.00 | 0.00 | 3 047.77 | 524.22 | 114 496.36 |
| 4 | 114 496.36 | 2 400.00 | 0.00 | 3 083.21 | 530.31 | 119 449.25 |
| 5 | 119 449.25 | 2 400.00 | 0.00 | 3 026.13 | 520.49 | 124 354.88 |
| 6 | 124 354.88 | 2 400.00 | 3 000.00 | 2 926.27 | 503.32 | 126 177.84 |
| 7 | 126 177.84 | 2 400.00 | 3 000.00 | 2 895.19 | 497.97 | 127 975.06 |
| 8 | 127 975.06 | 2 400.00 | 3 000.00 | 2 850.54 | 490.29 | 129 735.30 |
| 9 | 129 735.30 | 2 400.00 | 3 000.00 | 2 107.43 | 362.48 | 130 880.26 |
| 10 | 130 880.26 | 2 400.00 | 3 000.00 | 2 071.36 | 356.27 | 131 995.35 |
| 11 | 131 995.35 | 2 400.00 | 3 000.00 | 2 033.83 | 349.82 | 133 079.35 |
| 12 | 133 079.35 | 2 400.00 | 3 000.00 | 1 994.84 | 343.11 | 134 131.08 |

**Year-6 trace**, at full precision, because it is the year in which every lever is
active at once: `pm_avg_pp = 124 054.884701` (= 124 354.884701 + 1 200 − 1 500);
`fee_pp = 744.329308`; `expenses_pp = 460.046913` (= 0.0035 × 124 054.884701 + 24 ×
1.015⁵); `fin_acct_pp = 0.028 × (124 054.884701 + 1 756.875780) = 3 522.729293`, of which
85% is `2 994.319899`; `tech_acct_pp = 284.282396`; `insurer_tech_share_pp = max(28.428,
108.000) = 108.000000` — the 4.5%-of-premiums limb binds; policyholder technical share
`176.282396`; `pb_acct_pp = pb_min_pp = 3 170.602295`; `ts_stat = 1.955806%`;
`pb_target_pp = 0.023 × 124 054.884701 + 744.329308 = 3 597.591656`, so the discretionary
release wanted is `426.989361`, while the vintage falling due is `500.000000` — the
forced release wins; `pb_credited_pp = 3 670.602295`; `ts_net = 2.358853%`;
`int_credited_pp = 2 926.272987`; `soc_levy_pp = 503.318954`;
`av_pp(7) = 126 177.838734`.

**Decrement and cash-flow extract**, `pols_if_init = 1`, `ref_rate = 2.20%`, and
`mort_rate(t)` read from the shipped **[std]** proxy — 0.0060 at age 60, the placeholder
the table is anchored to, and graded upward from there, so 0.007130 at age 62, 0.009262
at age 65 and 0.012060 at age 68:

| `t` | `lapse_rate(t)` | `pols_if(t)` | `claims_death(t)` | `claims_lapse(t)` | `expenses(t)` | `liability_cf(t)` |
|---|---|---|---|---|---|---|
| 1 | 4.0000% | 1.000000 | 628.45 | 4 164.51 | 378.20 | 2 771.16 |
| 3 | 8.0000% | 0.910080 | 743.00 | 8 276.62 | 375.34 | 7 210.78 |
| 6 | 5.0000% | 0.738099 | 862.56 | 4 613.46 | 339.56 | 6 258.43 |
| 9 | 6.2873% | 0.613775 | 968.78 | 4 989.75 | 294.65 | 6 621.44 |

**Checks.**

*The `taux servi` from a different direction.* `ts_net(t)` decomposes as
`0.85·fin_acct_pp/pm_avg + (policyholder technical share)/pm_avg − fee_rate +
(PPB flow)/pm_avg`. Year 6: `2.413706% + 0.142100% − 0.600000% + 0.403047% = 2.358853%`,
which is the table's 2.3589%. Year 9, with the PPB exhausted:
`2.082500% + 0.145673% − 0.600000% + 0.000000% = 1.628173%`, the table's 1.6282%.

*The twelve-year account identity.* Summing Table 2, credited interest is EUR 31 800.82
and social levies EUR 5 469.74, and `5 469.74 / 31 800.82 = 0.172000` exactly — the levy
is 17.2% of credited interest and of nothing else. Then
`100 000.00 + 28 800.00 − 21 000.00 + 31 800.82 − 5 469.74 = 134 131.08`, the year-12
closing balance. The same total reached the other way: PB credited gross of the charge is
EUR 40 538.97 and `frais de gestion` EUR 8 738.15, and `40 538.97 − 8 738.15 =
31 800.82`.

*The PPB clock closes.* Releases over the twelve years total EUR 4 256.88, against an
opening PPB of EUR 4 000.00 plus three dotations (137.06, 87.30, 32.52) of EUR 256.88.
Every opening vintage is exhausted by its due year: the year-7 release of 606.30 clears
the last EUR 500.00 vintage and takes EUR 106.30 from the year-0 vintage, leaving
EUR 393.70 to be forced out in year 8 — which the year-8 discretionary need of EUR 650.58
more than covers, so the PPB reaches zero exactly at the clock's last date.

*The guarantee floor.* With no PB at all the account falls at exactly `fee_rate` a year,
reproducing the published minimum surrender values: `1 000 × (1 − 0.006)ⁿ` gives
994.0000, 988.0360, 982.1078, 976.2151, 970.3578, 964.5357, 958.7485, 952.9960, matching
Suravenir's 994.00 … 952.99 truncated to the cent [S3]; `970 × 0.995ⁿ` gives 965.1500,
960.3243, 955.5226, matching MACSF's 965.15, 960.32, 955.52 [S2]. Here
`guar_floor_pp(13) = 100 000.00 + 28 800.00 − 21 000.00 − 8 738.15 = 99 061.85` against
`av_pp(13) + soc_levy_cum_pp(13) = 134 131.08 + 5 469.74 = 139 600.82`: the floor never
binds on a path with a positive `taux servi` throughout.

*The aggregate roll-forward.* Year 1: `100 000.00 + 2 400.00 + 2 827.60 − 486.35 −
628.45 − 4 164.51 = 99 948.29`, and `pols_if(2) × av_pp(2) = 0.954240 × 104 741.25 =
99 948.29`. `liability_cf(1) = 628.45 + 4 164.51 + 0.00 + 378.20 − 2 400.00 = 2 771.16`,
so `net_cf(1) = −2 771.16`.

*What year 9 is telling you.* At `r_fin = 2.45%` and a 0.60% charge, the most the account
could grow by — if the insurer distributed the whole financial account and kept only its
loading margin — is `2.45% − 0.60% = 1.85%`. The model credits 1.6282%, and the
0.2218-point wedge is exactly `0.15 × 2.45% = 0.3675%` retained from the `compte
financier` less the 0.1457% of the technical account that flows back to policyholders
[R5, art. A132-11](#frlib-assurance_vie_euro-r5). A 2.30% target is simply not payable on a 2.45% asset return without
the PPB, and the model steps down rather than pretending otherwise; the two management
actions that would soften it — realising capital gains into the year's financial account,
and the `réserve de capitalisation` [REG-R6] — are outside this model. Years 1 to 8 credit
2.79% down to 2.23%, inside or just below the band covering 50% of encours in 2025
(2.3%–2.9% [R14]); years 9 onward do not, and that step is a model result, not a market
forecast.

---

## Valuation and reserve pointers

Gross best-estimate liability cash flows are what this library produces; valuation layers
are cited, not reproduced.

- **French statutory provisions.** The euro support's liability is the `provision
  mathématique` — commitments valued *including future management costs*, which is why a
  French PM is not a net-premium reserve — and the PPB is a technical provision in its own
  right [REG-R6]. `av_pp(t) × pols_if(t)` and `ppb_pp(t) × pols_if(t)` are the model's
  contributions to those two lines. The `provision pour risque d'exigibilité` [REG-R7] and
  the `provision pour aléas financiers` [REG-R8] [REG-R9] belong to the general account
  behind the fund and are not computed here.
- **Solvabilité II.** Technical provisions are a best estimate — the probability-weighted
  average of future cash flows discounted at the relevant risk-free term structure — plus
  a risk margin [REG-R4], with EIOPA publishing the curves, the volatility adjustment and
  the ultimate forward rate monthly [REG-R5]. The euro fund's **future discretionary
  benefits** — the PPB stock and the discretionary part of the credited rate — are the
  substance of its best estimate, and the crediting rule above is exactly the management
  action a market-consistent valuation must model. **None of the Solvency II treatment of
  future discretionary benefits, management actions or the time value of the capital
  guarantee could be read from a retrieved instrument** [R18] [REG-R2], so it is
  [unverified] here; no cost-of-capital rate or lapse shock in this library rests on a
  retrieved text [REG-R2].
- **The guarantee is an option.** The capital floor plus a TMG is a written put on the
  fund and the deterministic path above prices none of it; a stochastic-on-deterministic
  run — the crediting rule, the PPB lever and the dynamic surrender formula re-evaluated
  per scenario — is what a time-value-of-options-and-guarantees calculation consumes.
- **IFRS 17 and professional standards.** The fonds en euros is the archetypal
  direct-participating contract and would be measured under the variable fee approach; the
  standard's landing page confirms the fulfilment-cash-flow plus contractual-service-margin
  structure but the VFA mechanics were not read and are [unverified] [REG-R45]. The
  fulfilment-cash-flow engine is this same projection. NPA 2 applies "à tout modèle
  actuariel" under a proportionality principle [REG-R44], and the worked example above and
  the pitfall tests are the documentation it asks for.

---

## Key sensitivities and model risks

1. **The `r_fin` path dominates everything.** It sets the `compte financier`, hence the
   statutory floor, hence how fast the PPB drains. A 50 bp shift in the path moves
   `ts_stat` by about 42.5 bp (0.85 × 50) and changes the year in which the PPB is
   exhausted by several years.
2. **The PPB opening level and its vintage profile.** 4.0% of provisions is the market
   ratio [R14] [REG-R47], but the vintage split is pure **[std]** and it decides *when*
   the eight-year clock forces a release. A fund carrying its PPB in young vintages can
   defer; one carrying it in old vintages cannot.
3. **The crediting rule itself.** `ts_target` level, the absence of a year-on-year cap,
   and the decision to credit the forced release rather than smooth it are all [std]
   choices with no public calibration, and they change the payout path more than any
   experience assumption.
4. **The dynamic surrender parameters.** `a = 4.0` and `tol = 0.25` point are the largest
   unanchored numbers in the file. Because the credited rate and the surrender rate move
   together — a falling `ts_net` raises surrenders, which shrinks the base the fund earns
   on — the model has a feedback loop the deterministic run only samples once.
5. **The expense split and the 4.5%-of-premiums limb.** The proportional 0.35% and the
   fixed EUR 24 are [std] and feed the `compte technique`, so they move the statutory
   floor directly; a small-balance model point is dominated by the fixed part and credits
   materially less. The premiums limb vanishes on a paid-up contract, leaving the insurer
   only 10% of the technical result, and can exceed the whole technical result on a
   heavily premium-paying one — two model points identical but for their premium stream
   credit different rates, and that is the article working as written [R5].
6. **Mortality is a timing assumption, not an amount assumption.** The death benefit is
   the account value [S3], so the proxy basis [REG-R23] [REG-R24] affects only when the
   account is released — far less than in any protection product.
7. **The annual grid hides the in-year rate.** Every insurer credits only a floor rate
   `pro rata temporis` to a mid-year exit [S1] [S2] [S11]; with a zero TMG that is zero
   interest. The base model's full-year credit is generous to exiting policies by up to
   one year's `ts_net`, concentrated in the high-lapse years.
8. **The HCSF power is unmodeled by construction.** A mass-surrender scenario here
   produces the surrender values the contract owes, not the ones that would be paid if the
   freeze under art. L631-2-1 5° ter were in force [R8] [REG-R13].
9. **Data provenance.** The TMG is [std] because no contract publishes one [S1] [S2]
   [S11]; the `avance` terms are [unverified] because all three insurers push them into a
   separate document [S1] [S2] [S3]; the composition of the 17.2% levy is [unverified]
   [S3]; the capital/gain split of a partial surrender is [unverified]. A calibration pass
   against an insurer's own PB policy and its published `taux servi` history [REG-R31] is
   required before any quantitative use.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R10]: #frlib-assurance_vie_euro-r10
[R11]: #frlib-assurance_vie_euro-r11
[R14]: #frlib-assurance_vie_euro-r14
[R15]: #frlib-assurance_vie_euro-r15
[R18]: #frlib-assurance_vie_euro-r18
[R3]: #frlib-assurance_vie_euro-r3
[R5]: #frlib-assurance_vie_euro-r5
[R6]: #frlib-assurance_vie_euro-r6
[R7]: #frlib-assurance_vie_euro-r7
[R8]: #frlib-assurance_vie_euro-r8
[R9]: #frlib-assurance_vie_euro-r9
[REG-R13]: #frlib-reg-r13
[REG-R15]: #frlib-reg-r15
[REG-R16]: #frlib-reg-r16
[REG-R18]: #frlib-reg-r18
[REG-R2]: #frlib-reg-r2
[REG-R23]: #frlib-reg-r23
[REG-R24]: #frlib-reg-r24
[REG-R29]: #frlib-reg-r29
[REG-R31]: #frlib-reg-r31
[REG-R4]: #frlib-reg-r4
[REG-R40]: #frlib-reg-r40
[REG-R44]: #frlib-reg-r44
[REG-R45]: #frlib-reg-r45
[REG-R47]: #frlib-reg-r47
[REG-R5]: #frlib-reg-r5
[REG-R6]: #frlib-reg-r6
[REG-R7]: #frlib-reg-r7
[REG-R8]: #frlib-reg-r8
[REG-R9]: #frlib-reg-r9
[std]: #frlib-std
[unverified]: #frlib-unverified
<!-- END generated citation links -->
