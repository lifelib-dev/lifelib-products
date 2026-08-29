# Technical Notes

**Status:** Draft, 2026-08-29 (access date for every citation: 2026-08-29).

**Scope note.** These notes specify a reference liability cash-flow projection model — model name
**`BU_DE_S`**, **monthly** grid — for the standardized composite German *selbständige
Berufsunfähigkeitsversicherung* defined in `product-spec.md` (same directory). This is not any
single insurer's product. [S#] / [R#] tags refer to the source list in `sources.md` (numbering
carried from `_research/berufsunfaehigkeit.md`; frozen); [REG-R#] tags refer to the cross-product
reference library `references/regulatory-and-actuarial-references.md` (its own R-numbering).
**[std]** marks a standardization introduced for the reference implementation; [unverified] marks a
claim no search corroborated. Parameter values are identical to those in `product-spec.md`. Cells
names, model-point columns and CSV headers are English `lower_snake_case`; German terms of art keep
their German form in prose.

**Retrieval conditions.** **No document cited here was retrieved and none was corroborated by a web
search** — direct HTTP egress was blocked and the session's search budget was exhausted before this
product was reached. A citation is a **pointer, not a certificate**. The practical consequence for
these notes is unusual and is stated once, here: **every biometric level in this model is [std]**,
because the DAV 1997 family and DAV 2008 T are the property of the Deutsche Aktuarvereinigung, are
not public and are not redistributed by delib [R16] [R17] [REG-R50] [REG-R48]; **every charge level
is [std]**, because no German insurer publishes a BU charge structure and a pure risk contract
carries no *Effektivkosten* disclosure [R12] [S14]; and **the premium itself is [std]**, because no
German BU rate card of any kind was obtained. The *mechanics* below are not [std]. They are the
established German ones, and each carries the instrument it must be checked against.

---

## Model scope and conventions

- **Purpose.** Project **gross best-estimate liability cash flows, undiscounted**, for a
  single-policy model point on an expected (probability-weighted) basis: *Bruttobeitrag* income,
  the *Beitragsverrechnung* credited back out of it, *BU-Rente* outgo, the *Wiedereingliederungshilfe*,
  administration expense and *Leistungsbearbeitungskosten*. **Out of scope**, and cited rather than
  computed: discounting; the *Deckungsrückstellung* for active lives and the *Leistungsrückstellung*
  for claims in payment; Solvency II technical provisions and SCR; IFRS 17; and every tax
  [REG-R47] [REG-R1] [REG-R55]. There is **no surrender or paid-up cash flow** — see *No cash value
  is modelled* below.
- **Model structure.** A **four-ledger multi-state chain**: *aktiv* (paying premium, exposed to
  inception, active-lives mortality and lapse) → *leistungspflichtig* (receiving the *BU-Rente*,
  premium-free, exposed to reactivation and to disabled-lives mortality) → a **three-month § 174
  run-off** (still receiving the *BU-Rente*, still premium-free, no longer *berufsunfähig*) → back
  to *aktiv*. Death and lapse are the only absorbing exits. **The return arc is what makes this a
  genuine multi-state model rather than a decrement model**, and it is the structural difference
  from delib's `risikolebensversicherung` [R3] [R16] [REG-R50].
- **Projection frequency.** **Monthly**, matching the *BU-Rente* paid monthly in advance and the
  retail monthly premium [S1]. `t` is the **policy month**, `t = 0, 1, …, proj_len()`, **0-based**:
  `t = 0` is the first projected month — the month of inception for a new-business point, the
  valuation month for an in-force one.
- **Projection horizon.** `proj_len() = 12 × (cover_end_age − entry_age) − 1 − duration_init_months`,
  the **last projected month index**, so `result_cf()` is indexed `t = 0 … proj_len()` and
  `result_cf().index[-1] == proj_len()`. On the anchor cell that is `12 × (67 − 30) − 1 = 443`, i.e.
  444 monthly rows. Cover ceases at attained age `cover_end_age`; the last projected month is the
  last month of attained age `cover_end_age − 1`.
- **Timing conventions [std].** *Bruttobeitrag* and the *Beitragsverrechnung* credit at the
  **start** of the month, and only from the premium-paying population; administration expense at
  the start of the month; the *BU-Rente* and the claim-maintenance cost at the **start** of the
  month, in advance [S1]; all state transitions and the claim-assessment cost at the **end** of the
  month; the *Wiedereingliederungshilfe* at the end of the month in which the run-off completes.
- **Age basis.** *Eintrittsalter*, age last birthday, advancing at the policy anniversary:
  `age(t) = entry_age + duration_mth(t) // 12` **[std]** (product spec, footnote 5).
- **Claim duration.** `z` is **months since the onset of the BU**, `z ≥ 1`; a life whose BU incepts
  at end of month `t` is in duration cohort `z = 1` at the start of month `t + 1`, which is when its
  first *BU-Rente* is due if `karenz_months = 0`. The *Karenzzeit* clock and the *Leistungsdynamik*
  clock both run on `z`.
- **No cash value is modelled.** § 169 VVG through § 176 gives this contract a real *Rückkaufswert*
  and § 165 a real *beitragsfreie BU-Rente* [R8] [R9] [R5] [REG-R28], but both are the release of a
  reserve this model deliberately does not compute. **A lapse removes the policy and pays nothing**:
  there is no `av_pp_at`, no surrender cells, no paid-up state, and `claims(t, "LAPSE")` is
  structurally zero at every `t`. That zero is a scope statement, published rather than implied.
- **No death benefit.** An SBU pays nothing on death, before or during a claim [S1], so there is no
  `claims_death` — `pols_death(t)` is a decrement, not a cash flow. A reader coming from a term-life
  model will look for the column and must not find one.
- **Unisex.** `sex` is a model-point attribute for **decrement and reporting** purposes only. It
  **must not** enter the premium: sex-differentiated pricing has been unlawful in Germany for new
  contracts since 21 December 2012 [R15] [REG-R34]. The shipped decrement tables are unisex, so in
  the base parameterization `sex` moves nothing at all, and that invariance is a test.
- **Currency, sign and rounding.** EUR throughout. `net_cf(t)` is **income-positive** (premium +,
  the surplus credit, claims and expenses −), with the outgo-positive orientation published as
  `liability_cf(t) = −net_cf(t)`. Intermediates at full double precision; displayed state
  probabilities to six decimals and cash flows to the cent **[std]**. Rounded monthly rows do not
  re-add to displayed totals; totals are sums of unrounded values.

---

## Model point attributes

| Attribute | Type | Meaning | Exercised by |
|---|---|---|---|
| `point_id` | int | Index of `model_point_table.csv`; `Projection.parameters == ("point_id",)` | all |
| `status` | enum {`aktiv`, `leistung`} | State at `t = 0` | 7 (`leistung`) |
| `entry_age` | int | *Eintrittsalter*, age last birthday at inception | all; 25 – 50 across the table |
| `sex` | enum {M, F} | Decrement and reporting only — **never prices** [REG-R34] | 1 / 2 (the unisex twin) |
| `berufsgruppe` | str | Key into `occupation_table.csv`; BG1 … BG5 | 1 / 3 (BG1 vs BG4), 5, 8, 9, 11 |
| `bu_rente_mth` | EUR/month | The agreed *BU-Rente* at inception | all; 1 000 – 2 500 |
| `cover_end_age` | int | *Endalter* — the *Versicherungsdauer* ends at this attained age | 8 (60), 9 (67) |
| `benefit_end_age` | int | *Leistungsendalter* — the *Leistungsdauer* ends here | 9 (63 against a cover end of 67) |
| `karenz_months` | int | *Karenzzeit*, months of deferment of payment | 5 (6), 8 (3), 13 (12) |
| `leistungsdyn_rate` | float p.a. | *Leistungsdynamik*, escalation of the *BU-Rente* **in payment**, on each anniversary of onset | all at 0,02; 12 at 0,00 |
| `premium_form` | enum {`level`, `dynamik`} | Level *Bruttobeitrag*, or *Beitragsdynamik* | 4 (`dynamik`) |
| `beitragsdyn_rate` | float p.a. | Effective *Beitragsdynamik*, net of declined increases; 0 on the `level` form | 4 (0,03) |
| `prem_mode` | enum {`monthly`,`quarterly`,`half_yearly`,`annual`} | Payment frequency; keys `freq_loading_table.csv` | 1 (monthly), 4 (annual), 5 (quarterly), 6 (half-yearly) |
| `gross_prem_ann` | EUR p.a. | *Bruttobeitrag* override; **0 = derive by equivalence** | 13 (2 400,00) |
| `beitragsverrechnung` | float | *Zahlbeitrag* / *Bruttobeitrag* | all at 0,70; 13 at 0,55 |
| `risk_factor` | float | *Risikozuschlag* — a multiplier on the *Bruttobeitrag* **only** | 11 (1,50) |
| `au_klausel` | bool | *AU-Klausel* switch | 10 (true) |
| `au_uplift` | float | Inception uplift when the clause is on. **Shipped at 1,00 everywhere** — no source quantifies it (gap 12) | 10, inertly |
| `wiedereingliederung_months` | int | *Wiedereingliederungshilfe*, in monthly *Renten*; 0 = off | all at 6; 12 at 0 |
| `duration_init_months` | int | Elapsed policy months at `t = 0`; 0 for new business | 6 (180), 7 (200) |
| `claim_duration_init` | int | Months since onset at `t = 0`, for a `leistung` point | 7 (8) |

`pols_if_init()` is **1.0 for every model point**: the model is a per-policy probability projection,
one model point at a time, so `pols_if(0) == 1.0` exactly and `result_cf()`'s first `pols_if` value
is that. There is no `policy_count` column.

**Three columns a reader is most likely to get wrong.** `berufsgruppe` loads **the inception rate**,
and so reaches the premium only through the equivalence, while `risk_factor` loads **the premium
alone** and leaves every claim untouched — they are not two spellings of the same thing.
`benefit_end_age` is a separate contractual term from `cover_end_age`, not a synonym.
And `leistungsdyn_rate` escalates the *BU-Rente* **in payment on the anniversary of onset**, while
`beitragsdyn_rate` escalates the **insured** *BU-Rente* and the premium together on the policy
anniversary, before any claim: different quantities, different clocks.

---

## State variables

| Variable | Description | Updated |
|---|---|---|
| `pols_actv(t)` | Probability *aktiv* — in force, premium-paying, exposed to inception — at the **start** of month `t` | monthly |
| `pols_dis_dur(t, z)` | Probability *leistungspflichtig* at the start of month `t`, `z` months since onset | monthly, two-dimensional |
| `pols_dis(t)` | `Σ_z pols_dis_dur(t, z)` | derived |
| `pols_runoff_slot(t, k)`, `k = 1,2,3` | Probability in the § 174 three-month run-off, `k` months into it | monthly |
| `runoff_val(t, k)` | The same population **times the monthly *BU-Rente* it is being paid** — a value ledger, because the run-off carries amounts frozen at the *Nachprüfung* date | monthly |
| `pols_runoff(t)` | `Σ_k pols_runoff_slot(t, k)` | derived |
| `pols_if(t)` | `pols_actv(t) + pols_dis(t) + pols_runoff(t)` — the count at the **start** of month `t` and the weight on that same `result_cf()` row | derived |
| `pols_prem(t)` | The **premium-paying** count: `pols_actv(t)` plus disabled cohorts still inside the *Karenzzeit*, `Σ_{z ≤ karenz_months} pols_dis_dur(t, z)` | derived |
| `pols_inception(t)` | Transitions *aktiv* → *leistungspflichtig* at end of month `t` | monthly |
| `pols_recovery(t)` | Claim terminations other than death at end of month `t` — recovery **and** *konkrete Verweisung*, which this model does not separate — entering run-off slot 1 | monthly |
| `pols_reactivation(t)` | Run-off completions returning to *aktiv* at end of month `t` | monthly |
| `pols_death(t)` | Deaths from all three ledgers at end of month `t` | monthly |
| `pols_lapse(t)` | Lapses, from `pols_actv` only | monthly |
| `bu_rente_pp(t)` | The **insured** monthly *BU-Rente* at time `t`, after any *Beitragsdynamik* | at anniversaries |
| `rente_pay_pp(t, z)` | The monthly *BU-Rente* **in payment** for the duration-`z` cohort | at claim anniversaries |
| `prem_gross_level_pp()` | The level annual *Bruttobeitrag* — derived by equivalence or overridden | once per model point |
| `prem_gross_pp(t)`, `prem_zahl_pp(t)` | The *Bruttobeitrag* and *Zahlbeitrag* **instalments due** at month `t`; both zero in a month that is not a payment month | monthly |
| **First-order shadow** | `pols_actv_first(t)`, `pols_dis_dur_first(t, z)`, `pols_runoff_first(t)`, `pols_prem_first(t)` — the same chain on *Rechnungsgrundlagen erster Ordnung* **without lapse**, used only to fix `prem_gross_level_pp()` | monthly |

**Four absences are product facts, not gaps.** There is **no account value and no surrender value**
[R9] [R5], so no `av_pp_at` exists and a lapse carries no cash flow. There is **no death benefit**
[S1], so no `claims_death` exists. There is **no maturity benefit** — survival to the *Endalter*
pays nothing. And there is **no "acknowledged" state**: § 173's once-only *befristetes Anerkenntnis*
would justify one [R2] [REG-R29], but this model pays from onset and does not model the decision
delay, so acknowledgement is a timing event with no cash-flow consequence here (pitfall 7).

`pols_runoff` is the ledger a naive model omits, and omitting it is a first-order error in exactly
the way `pols_red` is on frlib's `dependance`: a recovery does not release the liability in the
month it happens, it releases it three months later [R3].

---

## Assumption inputs

### (a) Contractual / guaranteed elements (cited)

| Input | Value | Basis |
|---|---|---|
| Benefit | The agreed monthly *BU-Rente*, paid **monthly in advance** while *berufsunfähig*, to the *Leistungsendalter* | [S1] [R1] |
| Trigger | Inability to exercise the last occupation as arranged, **to at least 50 %**, **prospectively for at least six months** — an AVB convention, **not statute** | [S1] [REG-R37]; statutory limbs [R1] |
| Degree | **All-or-nothing at 50 %.** The modelled object is the incidence of a ≥ 50 % incapacity, not a severity distribution | [S1] [REG-R37] |
| *Beitragsbefreiung* | Full waiver of the premium while the *BU-Rente* is in payment, including through the run-off | [S1] [S2] |
| End of benefit | At `benefit_end_age`; on death; or on a *Nachprüfung* termination followed by the **three-month run-off** of § 174 — the insurer remains liable to the end of the third month after the notice reaches the policyholder | [S1] [R3] [REG-R29] |
| *Reaktivierung* | The cover revives: the *Beitragsbefreiung* stops, the premium resumes **at the same *Zahlbeitrag***, and a fresh BU may be claimed later | [S1] |
| *Karenzzeit* | An agreed deferment of **payment** on a BU already established — **not** the six-month prognosis period | [S1] |
| *Bruttobeitrag* | The contractually **guaranteed maximum** premium, computed on first-order bases; level for the term on the `level` form | [R10] [S13] [S16] |
| *Zahlbeitrag* | *Bruttobeitrag* less the *Beitragsverrechnung* — the anticipated surplus credited against the premium in advance under § 153 VVG through § 176, with the MindZV risk-result minimum behind it | [R10] [R14] [R5] [REG-R24] [REG-R18] |
| Death benefit, maturity value, surrender value | **All none** as modelled cash flows | [S1]; scope **[std]** |
| Unisex | Sex may not enter premiums or benefits for contracts written from 21 December 2012 | [R15] [REG-R34] |
| Premium tax | None | [R31] `[unverified]` |

### (b) Insurer-discretionary current elements

Thin, and on this product the discretion bites in exactly one place — but that one place is worth
43 % of premium income.

| Input | Snapshot value | Basis |
|---|---|---|
| *Beitragsverrechnung* ratio | **0,70**, held **constant for the whole projection** **[std]** (1) | recalled range 0,50 – 0,80, most commonly 0,60 – 0,75 `[unverified]`; mechanic [R10] [R14] |
| *Zahlbeitrag* re-rating | **None in the base run** — the ratio does not drift **[std]** (1) | the insurer may reduce the *Beitragsverrechnung* up to the *Bruttobeitrag* and no further [S13] [S16]; frequency and size **not established** [R23] |
| Alternative *Überschussverwendungen* | **Not modelled**: no *Bonusrente*, no *verzinsliche Ansammlung*, no *Überschussrente im Leistungsfall* | `[unverified]` market shares; *Beitragsverrechnung* is dominant |
| Surplus account, RfB, declaration mechanic | **None.** Correct for BU, because the surplus is applied immediately rather than accumulated | [R10] [R14] |
| *Nachprüfung* intensity | Folded into the reactivation assumption rather than modelled as a review cycle | [R3] `[unverified]` frequency |
| *Anerkennungsquote* | **0,80**, as an acceptance factor on the inception rate **[std]** (2) | recalled 75 – 80 % [R21] [R20] `[unverified]` |

1. **Holding the ratio constant is the model's single largest discretionary assumption, and it is
   the one the product's own consumer literature warns about.** Setting it to 0,70 and freezing it
   makes the base run reproducible from a stated construction; a user modelling the *Zahlbeitrag*
   risk raises `surplus_credit` toward zero over time, which raises collected premium toward the
   *Bruttobeitrag* — the whole cash-flow effect of the risk, and it moves nothing else.
2. The acceptance factor multiplies the **inception rate**, not the benefit: a declined claim
   produces no annuity at all rather than a smaller one. **It belongs on top of a gross incidence
   basis and nowhere else.** The shipped inception proxy is gross of declinature by construction;
   a user substituting a table already net of declinature must set the factor to 1,00, or the
   effect is counted twice [REG-R53]. That double-count is pitfall 10.

### (c) Behavioural / experience assumptions (the modeller's view)

**Every input in this class is [std].** The DAV 1997 family and DAV 2008 T are DAV property, are
not public and are not shipped [R16] [R17] [REG-R50] [REG-R48]; no German insurer publishes a BU
lapse rate, expense loading or acquisition cost [R12] [S14]. What the shipped proxies must
reproduce, and what a replacement built from the real tables must preserve, is stated with each.

**Inception — *Invalidisierungswahrscheinlichkeit* i(x).** A two-slope Gompertz form, unisex, gross
of declinature, for the reference occupational class BG1, ages 18 – 66:

    i(x) = 0.00110 x 1.06^(min(x,45) - 30) x 1.13^(max(x,45) - 45)     **[std]**

giving 0,000822 at 25, **0,001100 at 30**, 0,001970 at 40, 0,002636 at 45, 0,004857 at 50,
0,008949 at 55, 0,016488 at 60 and 0,034326 at 66. The **shape** is what the research establishes
and the proxy reproduces it: low and nearly flat to 30, moderate through the forties, and a sharp
acceleration from the mid-forties that makes the last decade before the *Endalter* dominate the
liability — which is why the *Endalter* is the single most effective premium lever in the product
[R16] [R20]. The **level** is a construction, **anchored at `i(30) = 0.001100`** so the worked
example reproduces exactly. A replacement built on DAV 1997 I must preserve the age shape and must
declare whether it is gross or net of declinature.

**Occupational loading.** Multiplicative on `i(x)`, from `occupation_table.csv`: **BG1 1,00**,
BG2 1,40, BG3 2,10, **BG4 3,00**, BG5 4,50 **[std]**. One base table with occupational loadings is
how German BU pricing works [S6]; the anchors 1,00 (office) and 3,00 (reference manual) sit inside
the recalled 2× – 4× band and the rest are interpolated (product spec, footnote 12).

**Reactivation — *Reaktivierungswahrscheinlichkeit* r(z).** Annual, by **claim duration year only**,
from `claim_duration_table.csv` **[std]**:

| Claim year | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11+ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `recov_rate` | 0,250 | 0,130 | 0,070 | 0,040 | 0,025 | 0,018 | 0,014 | 0,011 | 0,009 | 0,008 | 0,006 |

The **front-loading is the point**: reactivation is concentrated in the first one to two years of a
claim and is close to zero after about five, so a claim surviving its first two years is very likely
to run to the *Leistungsendalter* [R16] [REG-R50]. **A flat reactivation rate is a modelling error,
not a simplification**, and it is pitfall 4. Two things this proxy does **not** do, both named
rather than hidden: it carries **no age-at-disablement dimension**, which DAV 1997 RI does [R16],
and it does **not** separate recovery from *konkrete Verweisung*, because no public data separates
them and both end the benefit through the same *Nachprüfung* with the same run-off [R3] [R29].

**Mortality.** Two tables in `mortality_table.csv`, plus a duration select factor **[std]**:

    mort_rate_actv(x) = 0.00035 x 1.095^(x - 30)          active lives, DAV 2008 T shape [R17]
    mort_rate_dis(x)  = 0.00140 x 1.095^(x - 30)          disabled lives, ultimate — 4.00x active
    mort_dis_sel_factor(z-year) = 3.0 / 2.0 / 1.6 / 1.4 / 1.3 / 1.2 from claim year 6

so disabled-lives mortality in the first claim year is **12× active-lives mortality at the same
age**, falling to 4,8× ultimate. **Using one rate for both states is a numbered pitfall** and the
reference library names it as such [REG-R50]. Anchored at `mort_rate_actv(30) = 0.000350`. The
active table is an insured-lives *Todesfall*-character shape, not a population table; a replacement
must preserve the excess of disabled over active mortality and the first-year selection.

**The direction of prudence, and why it forks.** On the **first-order** basis used to fix the
*Bruttobeitrag*, prudence for a disability product means **higher incidence, lower reactivation and
lower disabled-lives mortality** — a claim that starts more often, ends less often and lasts longer
[REG-R47]. It also means **lower active-lives mortality and no lapse**, because on this contract an
active death and a lapse both release a liability: they are favourable to the insurer, so a prudent
basis does not anticipate them. The loads are **[std]**:

| First-order load | Value | Applied to |
|---|---|---|
| `inc_load_first` | **1,30** | `i(x)` — higher incidence |
| `recov_load_first` | **0,70** | `r(z)` — lower reactivation |
| `mort_dis_load_first` | **0,80** | disabled-lives mortality — longer claims |
| `mort_actv_load_first` | **0,80** | active-lives mortality — fewer premium-paying lives lost |
| lapse | **0** | no lapse in the first-order basis |
| `rechnungszins` | **1,00 % p.a.** | the *Höchstrechnungszins* for contracts written from 1 January 2025 `[unverified]` [R13] [REG-R14] [REG-R15] |

**Lapse — *Stornoquote*.** Annual, by policy year, from `lapse_table.csv` **[std]**:

| Policy year | 1 | 2 | 3 | 4 | 5 | 6+ |
|---|---|---|---|---|---|---|
| `lapse_rate` | 0,040 | 0,040 | 0,035 | 0,030 | 0,025 | 0,020 |

German BU lapse is **low** — the cover is hard to replace once health has changed, which is a
powerful anti-lapse force — and the shape follows the research's own construction of about 4 % in
the first two years falling to 2 % **[std]**. The 30-day *Widerruf* [REG-R23] sits inside the first
year's rate. **Lapse selection is not modelled and that is a stated model risk**: BU lapse is
strongly selective, because the healthy leave and the impaired cannot, so a non-selective rate
understates the average inception rate of the surviving book. Correcting it needs an assumption no
source supplies.

**Charges [std], with the one statutory ceiling marked.**

| Input | Value | Basis |
|---|---|---|
| `acq_rate` — *Abschluss- und Vertriebskosten* | **2,5 % of the *Beitragssumme***, charged once at issue | at the § 4 DeckRV *Höchstzillmersatz* of 25 ‰ [R13] [REG-R16]; level **[std]** |
| `admin_prem_rate` — proportional *Verwaltungskosten* | **9 % of the *Bruttobeitrag***, every month a premium is due | **[std]** |
| `admin_flat_ann` — flat *Verwaltungskosten* | **18,00 € per policy per year**, charged 1/12 monthly, **level in euro** | **[std]** |
| `claim_assess_cost` — *Leistungsbearbeitung*, assessment | **800,00 € per claim inception** | **[std]** |
| `claim_maint_cost_mth` — *Leistungsbearbeitung*, maintenance | **12,00 € per month a claim is in payment** | **[std]** |
| Expense inflation | **None.** A German *Verwaltungskostenzuschlag* is fixed in the tariff at conclusion | **[std]** |
| Commission | Not a separate line — it sits inside `acq_rate`, which is the German taxonomy | **[std]** |
| `freq_load` — *Ratenzahlungszuschlag* | annual **1,00**; half-yearly **1,02**; quarterly **1,03**; monthly **1,05** | German market convention `[unverified]`; **[std]** |

**Input files.** Seven CSVs sit beside `run.py`, read once per model by the unparameterized `Data`
Space (the `annuallife/TradLife_A` layout). Every one but `model_point_table.csv` carries a
**`provenance` column**, one tag per row, as delib's second ruling requires.

| File | Index | Value columns |
|---|---|---|
| `model_point_table.csv` | `point_id` | the 20 model-point attributes above (no `provenance` — a model point is a configuration, not an assumption) |
| `inception_table.csv` | `age` (18 – 66) | `inc_rate`, `provenance` |
| `claim_duration_table.csv` | `dur_year` (1 – 11, the last being ultimate) | `recov_rate`, `mort_dis_sel_factor`, `provenance` |
| `mortality_table.csv` | `age` (18 – 70) | `mort_rate_actv`, `mort_rate_dis`, `provenance` |
| `occupation_table.csv` | `berufsgruppe` (BG1 – BG5) | `occ_factor`, `label`, `provenance` |
| `lapse_table.csv` | `policy_year` (1 – 6, the last being ultimate) | `lapse_rate`, `provenance` |
| `freq_loading_table.csv` | `prem_mode` | `prem_mode_months`, `freq_load`, `provenance` |

---

## Cash flow components and recursions

### Notation (defined once, used throughout)

| Symbol | Meaning |
|---|---|
| `t` | policy month, `t = 0 … n`, `n = proj_len()` |
| `u(t)` | `duration_mth(t) = duration_init_months + t`, elapsed policy months at the start of `t` |
| `x(t)` | `age(t) = entry_age + u(t) // 12` |
| `y(t)` | `policy_year(t) = u(t) // 12 + 1` |
| `z` | claim duration in months since onset, `z ≥ 1` |
| `k` | run-off slot, `k = 1, 2, 3` |
| `R` | `bu_rente_mth`, the agreed monthly *BU-Rente* |
| `R(t)` | `bu_rente_pp(t)` — the **insured** monthly *BU-Rente*, `= R × (1 + g_B)^(y(t) − 1)` |
| `R_p(t, z)` | `rente_pay_pp(t, z)` — the monthly *BU-Rente* **in payment** for cohort `z` |
| `K` | `karenz_months`; `g_L` = `leistungsdyn_rate`; `g_B` = `beitragsdyn_rate` |
| `θ` | `beitragsverrechnung`; `ρ` = `risk_factor`; `φ` = `freq_load`; `M` = `prem_mode_months` |
| `κ` | `occ_factor` for the model point's `berufsgruppe`; `α` = `accept_factor` = 0,80; `υ` = `au_uplift` |
| `P` | `prem_gross_level_pp()`, the **level annual** *Bruttobeitrag* |
| `P_b(t)` | `prem_gross_pp(t)` — the *Bruttobeitrag* instalment due at `t`; `P_z(t)` the *Zahlbeitrag* instalment |
| `i(x)`, `i_m(t)` | inception, annual and monthly |
| `r(z)`, `r_m(z)` | reactivation, annual and monthly |
| `q^a(x)`, `q^a_m(t)` | active-lives mortality, annual and monthly |
| `q^i(x, z)`, `q^i_m(t, z)` | disabled-lives mortality including the duration select factor `s(z)` |
| `w(y)`, `w_m(t)` | lapse, annual and monthly |
| `l_a(t)`, `l_d(t, z)`, `l_r(t, k)` | `pols_actv`, `pols_dis_dur`, `pols_runoff_slot` |
| `V_r(t, k)` | `runoff_val(t, k)` — the run-off population times the *BU-Rente* it is being paid |
| `L(t)`, `L_p(t)` | `pols_if(t)`, `pols_prem(t)` |
| `v` | `(1 + rechnungszins)^(−1/12)`, used **only** in the equivalence, never to discount a published cash flow |
| `λ_i, λ_r, λ_d, λ_a` | the four first-order safety loads: 1,30 / 0,70 / 0,80 / 0,80 |
| `A`, `β`, `γ` | `acq_rate` 0,025; `admin_prem_rate` 0,09; `admin_flat_ann` 18,00 |
| `c_a`, `c_m` | `claim_assess_cost` 800,00; `claim_maint_cost_mth` 12,00 |

**Annual rates convert to monthly by** `p_m = 1 − (1 − p)^(1/12)`, applied to `i`, `r`, `q^a`, `q^i`
and `w` alike **[std]**. The library's convention is that `mort_rate` and `lapse_rate` are the
**annual** rates and `mort_rate_mth` / `lapse_rate_mth` the monthly ones, and the monthly rate is
strictly below the annual one wherever the annual one is positive.

### The decrement rates as composed

    i_m(t)      = 1 - (1 - i(x(t)) x κ x α x υ)^(1/12)
    r_m(z)      = 1 - (1 - r(z))^(1/12)
    q^a_m(t)    = 1 - (1 - q^a(x(t)))^(1/12)
    q^i_m(t,z)  = 1 - (1 - q^i(x(t)) x s(z))^(1/12)
    w_m(t)      = 1 - (1 - w(y(t)))^(1/12)

`κ`, `α` and `υ` are the **only** three multipliers on the inception rate, and their composition is
the model's published definition of `inc_rate(t)`. `ρ` (`risk_factor`) is **not** among them: it
loads the premium and nothing else.

### The premium — and the equivalence that fixes it

**No German BU rate card exists in this corpus**, so the *Bruttobeitrag* is an **output of a stated
first-order basis**, not an input. Run the same four-ledger chain on *Rechnungsgrundlagen erster
Ordnung* — `i × λ_i`, `r × λ_r`, `q^i × λ_d`, `q^a × λ_a`, **no lapse** — write the resulting
ledgers `l_a^1`, `l_d^1`, `l_r^1`, `L_p^1`, `L^1`, and form, with `d(t) = v^t`:

    PV_prem  = Σ_t d(t) x (1 + g_B)^(y(t)-1) x L_p^1(t) / 12         per 1 EUR p.a. of Bruttobeitrag
    PV_rente = Σ_t d(t) x [ Σ_{z>K} R_p(t,z) l_d^1(t,z) + Σ_k V_r^1(t,k) ]   , 0 once x(t) >= benefit_end_age
    PV_wgh   = Σ_t d(t) x wiedereingliederung_months x V_r^1(t,3) x (1 - q^a_m(t))
    PV_cost  = Σ_t d(t) x [ c_a x n_inc^1(t) + c_m x (paying count) ]
    PV_admin = Σ_t d(t) x γ x L^1(t) / 12
    BS_unit  = Σ_{y=1..Y} (1 + g_B)^(y-1)                            Beitragssumme per 1 EUR p.a.

and solve the equivalence, which is linear in `P` because both the acquisition and the proportional
administration loadings are proportional to it:

    P x PV_prem = PV_rente + PV_wgh + PV_cost + PV_admin
                + A x P x BS_unit + β x P x PV_prem

    =>  P = (PV_rente + PV_wgh + PV_cost + PV_admin) / ( PV_prem x (1 - β) - A x BS_unit )

Then `prem_gross_level_pp() = ρ × P`, or `ρ × gross_prem_ann` where the model point overrides it.
**The equivalence is struck before `ρ` and without lapse**, which is deliberate on both counts: a
*Risikozuschlag* prices an individually assessed impairment the base table does not carry, and the
model does not carry it either, so the loaded contract is priced above its own modelled cost — the
direction is stated and is pitfall 11; and German pricing does not anticipate lapse. **The
recursion is acyclic**: no decrement in this model depends on the premium, so nothing in `PV_*`
depends on `P`.

**The instalments actually billed.** With `M` months between payments,

    prem_due(t)      = 1 if u(t) mod M = 0 else 0
    P_b(t)           = prem_due(t) x prem_gross_level_pp() x (1 + g_B)^(y(t)-1) x φ x M / 12
    P_z(t)           = θ x P_b(t)
    surplus_credit_pp(t) = (1 - θ) x P_b(t)

The *Ratenzahlungszuschlag* `φ` loads the tariff premium, so it scales the *Bruttobeitrag* and the
*Beitragsverrechnung* together and `θ` stays exactly the ratio the tariff quotes. On the anchor cell
`M = 1` and a premium falls in every month; on model point 4 (`annual`) it falls in months
0, 12, 24, … and is twelve times as large, which is the whole reason the grid is monthly and the
frequency is a parameter rather than a smoothing.

### Benefit amounts

    R(t)       = R x (1 + g_B)^(y(t) - 1)                     insured BU-Rente, escalating pre-claim
    R_p(t, z)  = R(t - z) x (1 + g_L)^((z - 1) // 12)          BU-Rente in payment for cohort z

`R(t − z)` is the insured *BU-Rente* at the moment of onset, which for a cohort at duration `z` in
month `t` is month `t − z`; on the `level` form it is simply `R`. The *Leistungsdynamik* steps on
each **anniversary of onset**: cohorts `z = 1 … 12` are paid `R(t−z)`, `z = 13 … 24` are paid
`1,02 × R(t−z)`, and so on. **A model that escalates the *BU-Rente* on the policy anniversary rather
than the claim anniversary has the wrong clock** (pitfall 9).

The run-off carries **amounts, not just counts**, because a cohort entering the run-off keeps the
*BU-Rente* it was on at the *Nachprüfung* date and receives **no further *Leistungsdynamik***
**[std]** — three months is inside one anniversary in every realistic case, so the simplification
costs nothing and removes a second duration dimension.

### The four-ledger chain

At end of month `t`, from the active ledger, in the order **mortality, then lapse, then incidence
among the survivors of both** **[std]**:

    surv(t)            = l_a(t) x (1 - q^a_m(t))
    pols_lapse(t)      = surv(t) x w_m(t)
    base(t)            = surv(t) - pols_lapse(t)
    pols_inception(t)  = base(t) x i_m(t)
    l_a(t+1)          <- base(t) - pols_inception(t)                 (before the run-off feed)

From each disabled cohort `z`, deaths first and terminations on the survivors:

    dsurv(t, z)        = l_d(t, z) x (1 - q^i_m(t, z))
    rec(t, z)          = dsurv(t, z) x r_m(z)
    l_d(t+1, z+1)      = dsurv(t, z) - rec(t, z)
    l_d(t+1, 1)        = pols_inception(t)
    pols_recovery(t)   = Σ_z rec(t, z)

From the run-off slots, at **active-lives** mortality — these lives have recovered:

    l_r(t+1, 1)        = pols_recovery(t)
    V_r(t+1, 1)        = Σ_z rec(t, z) x R_p(t, z)
    l_r(t+1, k+1)      = l_r(t, k) x (1 - q^a_m(t))          k = 1, 2
    V_r(t+1, k+1)      = V_r(t, k) x (1 - q^a_m(t))          k = 1, 2
    pols_reactivation(t) = l_r(t, 3) x (1 - q^a_m(t))
    l_a(t+1)          += pols_reactivation(t)

with `pols_death(t)` the sum of the three ledgers' deaths. **`pols_recovery` feeds the run-off, not
the active ledger**: a life that recovers in month `t` is still paid in months `t+1`, `t+2` and
`t+3`, and only then rejoins `l_a` [R3] [REG-R29].

**Closure.** Death and lapse are the only exits, so at every `t`

    L(t+1) = L(t) - pols_death(t) - pols_lapse(t)

and over the whole projection `Σ_t [pols_death(t) + pols_lapse(t)] + pols_if_at(n, "END") = 1`.
Inception, recovery and reactivation are **internal transfers** and must not appear in that
identity — putting them there is how a multi-state model silently loses mass.

**At the *Leistungsendalter*** the benefit stops but **the mass is held, not deleted**: once
`x(t) ≥ benefit_end_age` every payment and every claim-maintenance cost is zero while the ledgers
keep rolling, so `check_states` and `check_pols_roll_fwd` still close. Those lives do **not** resume
paying premium **[std]** — they are still *berufsunfähig*, and the *Beitragsbefreiung* clause is
read here as keyed to the state rather than to the payment. The alternative reading is defensible;
it is named so that a user who takes it knows what to change. On eleven of the thirteen model points
`benefit_end_age = cover_end_age` and the question does not arise.

### Cash flows and net_cf

    premiums(t)         = P_b(t) x L_p(t)
    surplus_credit(t)   = (1 - θ) x P_b(t) x L_p(t)
    claims(t,"BU_RENTE")      = [ Σ_{z>K} R_p(t,z) l_d(t,z) + Σ_k V_r(t,k) ]  x 1{x(t) < benefit_end_age}
    claims(t,"REINTEGRATION") = wiedereingliederung_months x V_r(t,3) x (1 - q^a_m(t))
    claims(t,"LAPSE")         = 0                                              [R9] [R5]
    expenses(t)         = A x prem_gross_level_pp() x BS_unit x 1{t = 0 and duration_init_months = 0}
                        + β x P_b(t) x L_p(t)
                        + γ / 12 x L(t)
    claim_expenses(t)   = c_a x pols_inception(t)
                        + c_m x [ Σ_{z>K} l_d(t,z) + Σ_k l_r(t,k) ] x 1{x(t) < benefit_end_age}
    net_cf(t)           = premiums(t) - surplus_credit(t)
                        - claims(t,"BU_RENTE") - claims(t,"REINTEGRATION") - claims(t,"LAPSE")
                        - expenses(t) - claim_expenses(t)
    liability_cf(t)     = - net_cf(t)

`premiums` is the **gross** *Bruttobeitrag* and `surplus_credit` the *Beitragsverrechnung* returned
out of it, so the cash actually collected is the difference and the *Überschussbeteiligung* is a
visible line rather than a netting hidden inside the premium. **The acquisition charge is levied
once, at `t = 0`, and only on a new-business point**: an in-force point has already incurred it, and
charging it again at the valuation date is pitfall 14.

`result_cf()` publishes, indexed by `t` with `df.index.name == "t"`, in this order:

    pols_if, pols_actv, pols_dis, pols_runoff, pols_prem, premiums, surplus_credit,
    claims_bu_rente, claims_reintegration, claims_lapse, expenses, claim_expenses,
    liability_cf, net_cf

`result_states()` publishes beside it `pols_inception`, `pols_recovery`, `pols_reactivation`,
`pols_death`, `pols_lapse`, `inc_rate`, `recov_rate`, `mort_rate`, `lapse_rate`, `bu_rente_pp`,
`prem_gross_pp` and `prem_zahl_pp`.

### The published identities

Seven `check_*()` cells, each returning a single `bool` over all `t` with a per-`t`
`check_*_resid(t)` companion:

| Check | Identity |
|---|---|
| **`check_net_cf`** (delib ruling 1) | `net_cf(t) = premiums(t) − surplus_credit(t) − Σ_kind claims(t, kind) − expenses(t) − claim_expenses(t)` |
| `check_states` | `pols_if(t) = pols_actv(t) + pols_dis(t) + pols_runoff(t)` |
| `check_pols_roll_fwd` | `pols_if(t+1) = pols_if(t) − pols_death(t) − pols_lapse(t)` — inception, recovery and reactivation are internal transfers |
| `check_dis_roll_fwd` | `pols_dis(t+1) = pols_dis(t) − pols_death_dis(t) − pols_recovery(t) + pols_inception(t)` |
| `check_runoff_roll_fwd` | `pols_runoff(t+1) = pols_runoff(t) − pols_death_runoff(t) − pols_reactivation(t) + pols_recovery(t)` |
| `check_prem_split` | `premiums(t) − surplus_credit(t) = prem_zahl_pp(t) × pols_prem(t)` — the *Brutto*/*Zahl* pair reconciles to the *Zahlbeitrag* actually billed |
| `check_cover_end` | `claims(t, "BU_RENTE") = 0` wherever `age(t) ≥ benefit_end_age`, and `premiums(t) = 0` wherever `age(t) ≥ cover_end_age` |

### Monthly processing order

For `t = 0, 1, …, proj_len()`, in this order:

1. **Anniversary (start of month, `u(t) mod 12 = 0` and `u(t) > 0`).** Advance `y(t)` and `x(t)`.
   On the `dynamik` form, escalate the insured *BU-Rente* and the annual *Bruttobeitrag* by
   `(1 + g_B)`. Escalate each disabled cohort whose own claim anniversary falls in this month, i.e.
   `z mod 12 = 1`; the run-off values are **not** escalated **[std]**.
2. **Premium (start of month).** `prem_due(t)`; then `premiums(t) = P_b(t) × L_p(t)` and
   `surplus_credit(t) = (1 − θ) × P_b(t) × L_p(t)`. `L_p(t)` is `pols_actv(t)` **plus** disabled
   cohorts `z ≤ K` — a life inside the *Karenzzeit* is *berufsunfähig* but is not yet being paid, so
   the *Beitragsbefreiung* has not started **[std]**.
3. **Administration expense (start of month).** `β × P_b(t) × L_p(t) + γ/12 × L(t)`, plus, at
   `t = 0` on a new-business point only, `A × prem_gross_level_pp() × BS_unit`.
4. **Benefit (start of month).** `claims(t, "BU_RENTE")` on disabled cohorts past the *Karenzzeit*
   and on all three run-off slots — zero once `x(t) ≥ benefit_end_age`.
5. **Claim-maintenance cost (start of month)** on the same paying population.
6. **Look up the rates** at `x(t)`, `y(t)` and each `z`: `i_m`, `q^a_m`, `w_m`, `q^i_m(·, z)`,
   `r_m(z)`.
7. **End of month — active ledger:** deaths, then lapses on the survivors, then inceptions on the
   survivors of both. Charge `c_a` on the inceptions.
8. **End of month — disabled cohorts:** deaths at `q^i_m(t, z)`, then terminations at `r_m(z)` on
   the survivors; the terminations enter run-off slot 1 carrying their *BU-Rente* as a value.
9. **End of month — run-off:** deaths at active-lives mortality; slot 1 → 2, slot 2 → 3; slot-3
   survivors return to the active ledger and are paid the *Wiedereingliederungshilfe*.
10. **Roll every ledger to `t + 1`.** At `t = proj_len()` the projection ends: no maturity payment,
    no residual value, and any claim still in payment simply stops [S1].

### Known modeling pitfalls

These are the specific ways an implementation of *this* product looks right and is wrong. Each one
is a test.

1. **Weighting the premium by `pols_if` instead of `pols_prem`.** This is the classic German BU
   error: it charges premium to lives in claim and so silently deletes the *Beitragsbefreiung*,
   which is not an option but part of the core cover [S1]. Assert
   `premiums(t) = prem_gross_pp(t) × pols_prem(t)` at every `t`, and that
   `pols_prem(t) < pols_if(t)` wherever `pols_dis(t) + pols_runoff(t) > 0`.
2. **Projecting one premium stream instead of two.** A model carrying only the *Zahlbeitrag*
   silently assumes the *Beitragsverrechnung* is permanent; one carrying only the *Bruttobeitrag*
   overstates collected premium by `1/θ − 1 = 42,86 %` [R10] [S13] [S16]. Assert `check_prem_split`
   and `Σ premiums / Σ(premiums − surplus_credit) = 1 / 0,70` exactly.
3. **One mortality rate for both states.** Disabled-lives mortality is materially heavier than
   active-lives mortality and is itself select on duration [R16] [REG-R50]. Assert
   `mort_rate_dis(t, 1) / mort_rate(t) = 4,00 × 3,0 = 12,0` and `mort_rate_dis(t, 61)/mort_rate(t)
   = 4,80` at every `t`, and that the ratio is never 1.
4. **A flat reactivation rate.** Reactivation is front-loaded and near zero after about five years
   [R16] [REG-R50]. Assert `recov_rate(1) = 0,250`, `recov_rate(13) = 0,130`, `recov_rate(61) =
   0,025` and strict decrease across the first five claim years. A flat rate at the year-1 level
   roughly halves the projected benefit; at the ultimate level it roughly doubles it.
5. **Forgetting the § 174 three-month run-off.** A recovery does not stop the annuity in the month
   it happens; three further monthly payments follow the notice [R3] [REG-R29]. Assert
   `pols_runoff(t) > 0` wherever `pols_recovery(t−1) + pols_recovery(t−2) + pols_recovery(t−3) > 0`,
   and that suppressing the run-off strictly reduces `Σ claims_bu_rente`.
6. **Treating recovery and *konkrete Verweisung* as two decrements.** They end the benefit the same
   way, through the same *Nachprüfung*, with the same run-off, and no public data separates them
   [R3] [R29]. Assert the model publishes exactly one claim-termination-other-than-death rate.
7. **Confusing the *Karenzzeit* with the six-month prognosis period.** The prognosis is part of the
   *definition* of BU; the *Karenzzeit* defers *payment* on a BU already established [S1]. On the
   anchor (`K = 0`) the first *BU-Rente* falls in the month **after** an onset, not six months
   after: assert `claims(t, "BU_RENTE") > 0` at the first `t` with `pols_dis(t) > 0`.
8. **Waiving the premium during the *Karenzzeit*.** The *Beitragsbefreiung* runs with the benefit,
   so a life inside the *Karenzzeit* still pays [S1] **[std]**. On model point 5 (`K = 6`) assert
   `pols_prem(t) = pols_actv(t) + Σ_{z ≤ 6} pols_dis_dur(t, z)` and that this exceeds `pols_actv(t)`
   at some `t`; on the anchor assert the two are equal at every `t`.
9. **Escalating the *BU-Rente* on the wrong clock.** *Leistungsdynamik* steps on the anniversary of
   **onset**, *Beitragsdynamik* on the **policy** anniversary before any claim. With
   `beitragsdyn_rate = 0` assert `bu_rente_pp(t)` is constant at 1 500,00 € while
   `rente_pay_pp(t, 13) = 1,02 × rente_pay_pp(t, 12)` and `rente_pay_pp(t, 12) = rente_pay_pp(t, 1)`.
10. **Double-counting the *Anerkennungsquote*.** The shipped inception table is **gross** of
    declinature and `accept_factor = 0,80` sits on top of it [REG-R53]. Assert the published
    composition `inc_rate(t) = inc_rate_base(t) × occ_factor × accept_factor × au_uplift` exactly,
    so that a substitution which is already net is visible rather than silent.
11. **Confusing the two rating multipliers.** `occ_factor` loads the **inception rate** and reaches
    the premium only through the equivalence; `risk_factor` loads the **premium alone**. On model
    point 11 (`ρ = 1,50`) assert every claim and every decrement is identical to the unloaded twin
    while `premiums` scales by exactly 1,50; on model point 3 (BG4 against the anchor's BG1) assert
    `inc_rate` scales by exactly 3,00 while the premium ratio is slightly **below** 3,00, because
    the flat administration and assessment costs do not scale with the risk.
12. **Letting `sex` price.** Unlawful in Germany since 21 December 2012 [R15] [REG-R34]. Model
    points 1 and 2 differ **only** in `sex`: assert their `prem_gross_level_pp()` and every column
    of `result_cf()` are identical to 1e-12.
13. **Running benefit past the *Leistungsendalter* or premium past the *Versicherungsdauer*.** On
    model point 9 (`benefit_end_age = 63`, `cover_end_age = 67`) assert
    `claims(t, "BU_RENTE") = 0` and `claim_expenses(t)` carries no maintenance component for every
    `t` with `age(t) ≥ 63`, while `premiums(t) > 0` continues to 67.
14. **Charging acquisition cost to an in-force model point.** On points 6 and 7
    (`duration_init_months > 0`) assert `expenses(0)` contains no acquisition component and equals
    `β × P_b(0) × L_p(0) + γ/12 × L(0)` exactly.
15. **Deleting the disabled mass at the *Leistungsendalter* instead of holding it.** Deleting breaks
    both state identities. On model point 9 assert `check_states()` and `check_pols_roll_fwd()` are
    `True` and that `pols_if(t)` is continuous across `age(t) = 63`.
16. **Paying the *Wiedereingliederungshilfe* on every recovery.** It is paid on the **completion of
    the run-off**, so a life that dies inside the run-off never returns to work and is paid nothing
    [S1] **[std]**. Assert
    `Σ claims_reintegration < wiedereingliederung_months × Σ (pols_recovery(t) × their Rente)`
    strictly, and that it equals `wiedereingliederung_months × Σ_t V_r(t,3) × (1 − q^a_m(t))`.
17. **Inventing a surrender or paid-up cash flow.** § 169 and § 165 VVG through § 176 give this
    contract both, and the model prices neither [R8] [R9] [R5]. Assert `claims(t, "LAPSE") = 0,0` at
    every `t` and that no `av_pp_at`, `cv_pp` or surrender cells exist.
18. **Assuming the *Beitragsdynamik* buys proportional cover.** The German mechanic prices each
    increment at the attained age, so a given premium increase buys **less** than proportional cover
    and less of it with age `[unverified]`. This model instead escalates premium and *BU-Rente* by
    the same `g_B` and prices the whole escalating stream by one equivalence at inception — which is
    internally consistent but is *not* the market's annual-repricing practice, and understates the
    premium the market would charge for the cover projected. On model point 4 assert both
    `bu_rente_pp` and `prem_gross_ann_pp` grow by exactly `1,03` a year and record the direction.

---

## Policyholder behaviour modeling

All dynamic formulas are **[std]** reference constructions; there is no German calibration evidence
for any of them, and the two that would matter most are the two no source supplies.

- **Base lapse [std].** The duration table above, 4 % falling to 2 %. It is low by the standards of
  every other product in delib, and that is a real product fact rather than a modelling choice: once
  health has changed the cover cannot be replaced, so an insured with a claimable impairment cannot
  rationally lapse [S16].
- **Lapse selection [std], not modelled, direction known.** BU lapse is strongly selective — the
  healthy leave, the impaired stay — so a non-selective rate **understates** the average inception
  rate of the surviving book, and the understatement grows with duration. The reference construction
  a user should apply is `i_eff(t) = i(t) × [1 + λ × max(0, w_cum(t) − w_ref)]` with `w_ref = 0,20`
  and `λ = 0,30` **[std]**; the base run sets `λ = 0`, because stacking a selection loading on an
  already-[std] inception proxy compounds two unsourced choices. It is named in the model risks.
- **Premium-shock lapse [std], off.** On the `dynamik` form the policyholder receives a rising bill
  each year, and declining two or three consecutive increases extinguishes the option permanently
  `[unverified]`. The composite folds take-up into the **effective** `beitragsdyn_rate` — a
  policyholder accepting two increases in three is represented by a lower effective rate — rather
  than modelling a decision. That is the honest treatment of an option whose decline behaviour no
  source quantifies, and it keeps the equivalence acyclic: a shock-lapse module would make the lapse
  rate depend on the premium, which depends on the projection, which depends on the lapse rate.
- **Option take-up.** The *Nachversicherungsgarantie* is **not modelled at all** — it needs a
  take-up assumption **and** an anti-selection loading on the incremental cover, and neither is
  sourceable [S1] [S4] [S5]. The *Verlängerungsoption* is expressed as the model-point *Endalter*.
  The *AU-Klausel* is present as machinery with its uplift shipped at 1,00, so it is demonstrably
  inert until a user supplies a number (gap 12).
- **No dynamic reactivation behaviour.** Reactivation depends on claim duration alone here. In
  reality it depends on the insured's incentive to return to work, which depends on the ratio of the
  *BU-Rente* to her former income — the reason insurers cap the insurable *BU-Rente* at an
  *Angemessenheitsgrenze* of 60–70 % of gross [S1] [S16] `[unverified]`. Modelling that feedback
  would need a replacement-ratio elasticity no source supplies.

---

## Worked example

**Configuration.** Model point 1, the anchor cell, in full: `status = aktiv`, `entry_age = 30`,
`sex = F`, `berufsgruppe = BG1` (*Bürotätigkeit*, `occ_factor` 1,00), `bu_rente_mth = 1 500,00 €`,
`cover_end_age = 67`, `benefit_end_age = 67`, `karenz_months = 0`, `leistungsdyn_rate = 0,02`,
`premium_form = level`, `beitragsdyn_rate = 0,00`, `prem_mode = monthly` (`prem_mode_months = 1`,
`freq_load = 1,05`), `gross_prem_ann = 0` so the *Bruttobeitrag* is **derived by equivalence**,
`beitragsverrechnung = 0,70`, `risk_factor = 1,00`, `au_klausel = false`, `au_uplift = 1,00`,
`wiedereingliederung_months = 6`, `duration_init_months = 0`, `claim_duration_init = 0`. Hence
`pols_if_init() = 1,0`, `proj_len() = 12 × (67 − 30) − 1 = 443`, and the projection runs over
attained ages 30 to 66 inclusive — 444 monthly rows, of which the table below shows a selection and
the totals cover all of them.

**Assumptions, each tagged.** Inception `i(x) = 0,00110 × 1,06^(min(x,45) − 30) ×
1,13^(max(x,45) − 45)` **[std]**, unisex, gross of declinature, anchored at `i(30) = 0,001100`;
occupational factor `κ = 1,00` for BG1 **[std]**; acceptance factor `α = 0,80` **[std]**
[R21] [R20]; *AU-Klausel* uplift `υ = 1,00` **[std]** (gap 12), so
`inc_rate(t) = i(x(t)) × 1,00 × 0,80 × 1,00`. Reactivation `r(z)` by claim year
0,250 / 0,130 / 0,070 / 0,040 / 0,025 / 0,018 / 0,014 / 0,011 / 0,009 / 0,008 / 0,006 **[std]**
[R16]. Active-lives mortality `q^a(x) = 0,00035 × 1,095^(x − 30)` **[std]** [R17], anchored at
`q^a(30) = 0,000350`; disabled-lives mortality `q^i(x) = 0,00140 × 1,095^(x − 30)` **[std]** [R16],
four times the active rate, with duration select factors 3,0 / 2,0 / 1,6 / 1,4 / 1,3 / 1,2 from
claim year 6 **[std]**. Lapse 4,0 % / 4,0 % / 3,5 % / 3,0 % / 2,5 % / 2,0 % from policy year 6
**[std]**, with **no selection loading** (`λ = 0`). All annual rates converted by
`p_m = 1 − (1 − p)^(1/12)` **[std]**. First-order loads for the equivalence: inception × **1,30**,
reactivation × **0,70**, disabled-lives mortality × **0,80**, active-lives mortality × **0,80**,
**no lapse**, `rechnungszins` **1,00 % p.a.** **[std]** [R13] [REG-R14] [REG-R15]. Charges
**[std]**: `acq_rate` **2,5 % of the *Beitragssumme*** at issue, at the § 4 DeckRV cap [REG-R16];
`admin_prem_rate` **9 % of the *Bruttobeitrag***; `admin_flat_ann` **18,00 €** per policy per year
charged 1/12 monthly with **no inflation**; `claim_assess_cost` **800,00 €** per inception;
`claim_maint_cost_mth` **12,00 €** per month in payment. *Beitragsverrechnung* **0,70**, held
constant **[std]**. *Ratenzahlungszuschlag* **1,05** for the monthly mode **[std]**.
*Wiedereingliederungshilfe* **6 monthly *Renten*** on each completed run-off **[std]**.
*Leistungsdynamik* **2 % a year** on each anniversary of onset **[std]**. No *Beitragsdynamik*, no
*Risikozuschlag*, no premium-shock lapse, no lapse selection, no *Nachversicherungsgarantie*.

<!-- WORKED EXAMPLE TABLE -- filled by the model stage from the model's own output -->

---

## Valuation and reserve pointers

This library projects gross best-estimate-style liability cash flows, undiscounted, on a declared
grid. The valuation layers consume them and are cited, not reproduced.

- **The two German statutory reserves.** A BU book carries a *Deckungsrückstellung* for **active**
  lives — the prospective difference between future benefits and future premiums on
  *Rechnungsgrundlagen erster Ordnung*, at the *Rechnungszins* capped by the DeckRV — and a
  *Leistungsrückstellung*, the *Deckungsrückstellung für laufende Renten*, for **claims in
  payment**, which is the present value of the remaining annuity on disabled-lives bases and is much
  the larger per life [R9] [R21] [REG-R14]. This model computes neither. It does, however, carry the
  machinery: the first-order shadow ledgers that fix `prem_gross_level_pp()` are exactly the ledgers
  a *Deckungsrückstellung* recursion runs on, and discounting `liability_cf` at `rechnungszins` on
  those ledgers is the natural extension.
- **Why the active reserve is real here.** A level *Bruttobeitrag* charged against an inception rate
  that rises about 13 % per year of age after 45 overcharges heavily in the early years, and the
  excess accumulates. That is the *provision pour risques croissants* problem in German dress, and
  it is what makes this product a better mechanics demonstration than a term-life contract
  [R9] [REG-R28].
- ***Zillmerung* and the surrender value.** § 4 DeckRV caps the *Zillmersatz* at 25 ‰ of the
  *Beitragssumme*, cut from 40 ‰ on 1 January 2015, with the rate in use at conclusion applying for
  the whole term [R13] [REG-R16] [REG-R20]; § 169 VVG independently requires acquisition costs to be
  spread over at least five years for the *Mindestrückkaufswert* [R9] [REG-R28]. **The two rules
  bind separately and the tighter one governs**: the DeckRV says what may be reserved, § 169 what
  must be paid.
- **Solvency II.** Best estimate plus risk margin under Directive 2009/138/EG and Delegated
  Regulation (EU) 2015/35, with EIOPA publishing the curves monthly [REG-R1] [REG-R2] [REG-R4];
  `BEL = Σ_t v(t) × liability_cf(t)` over the recursion above. **No cost-of-capital rate,
  contract-boundary rule or standard-formula shock in this library was read from a retrieved
  instrument**, so every such figure is **[std]** [REG-R2].
- **The contract boundary is not an open question here, and that is worth saying.** Unlike a French
  annually revisable *temporaire décès*, a German BU contract guarantees the *Bruttobeitrag* for the
  whole term; the insurer's only lever is the *Beitragsverrechnung*, which can move the *Zahlbeitrag*
  **up** to a contractually fixed ceiling and not beyond [S13] [S16]. The obligation therefore runs
  to the *Endalter* and the projection does too.
- **Statutory accounts and IFRS 17.** §§ 341–341o HGB with the RechVersV and BerVersV on the German
  side [REG-R54]; fulfilment cash flows plus a contractual service margin under IFRS 17 for IFRS
  reporters [REG-R55]. The same expected-cash-flow engine feeds both; grouping, CSM and the risk
  adjustment are out of scope.
- **Professional standards.** The *Verantwortlicher Aktuar* certifies that the
  *Deckungsrückstellung* is properly calculated and the premiums sufficient, under §§ 141–143 VAG
  [R15] [REG-R11], against the DAV's *Fachgrundsätze* [REG-R56].

---

## Key sensitivities and model risks

In rough order of leverage for a German BU block:

1. **The inception basis — level and slope.** Both are **[std]**, and the slope is the more
   dangerous on a 444-month run because it compounds: the proxy rises 6 % per year of age to 45 and
   13 % after, and the last decade before the *Endalter* carries most of the liability. Nothing in
   the corpus constrains either number. The *Endalter* is the same sensitivity seen from the other
   side, and it is the market's own dominant premium lever: cutting it from 67 to 60 removes the
   seven most expensive years of cover.
2. **The reactivation shape.** Front-loaded against flat is worth roughly a factor of two on
   projected benefit in either direction, and no public German source gives the duration profile
   [R16] [REG-R50]. It also interacts with the run-off: the more reactivation, the more three-month
   tails, and the tails are pure additional outgo.
3. **The *Beitragsverrechnung* ratio.** At 0,70 the model returns 30 % of every *Bruttobeitrag* as
   *Überschussbeteiligung*. Across the recalled 0,50 – 0,80 range, collected premium moves by ±43 %
   relative to the base — **the single largest parameter uncertainty in the model, and the one gap
   the corpus most conspicuously leaves open** (product spec, footnote 7). It is also the
   policyholder's principal risk, and its empirical history is not established [R23].
4. **The *Leistungsdynamik*.** Compounding 2 % over a claim that can run thirty years raises the
   final payment to about 1,70× the first and the total benefit by roughly a third against a level
   annuity. Turning it off with the *Wiedereingliederungshilfe* is model point 12, and the premium
   difference against the anchor is the clean measure of what the two options cost.
5. **The occupational factor.** BG1 to BG5 spans 4,5× on the inception rate, and the classification
   itself is not comparable between carriers [S6]. A model point misclassified by one *Berufsgruppe*
   is wrong by 40 % or more in claim cost — a larger error than any assumption on this list can
   produce on its own.
6. **Lapse level and, more importantly, lapse selection.** The level is low, so the level matters
   less here than in any other delib product; the **selection** matters more, and it is not
   modelled. The direction is known and one-sided: the surviving book is sicker than the shipped
   inception rate assumes, so projected claims are understated, increasingly so with duration.
7. **The acceptance factor.** 0,80 scales every claim linearly and interacts with whether the
   inception basis is gross or net of declinature [REG-R53]. Getting the interaction wrong is a 20 %
   error in one direction or the other, and it is invisible in the totals.
8. **The three-month run-off, and the timing simplifications around it.** The run-off is small in
   aggregate but structural, and it is the one place where a German statutory rule reaches directly
   into a monthly cash flow [R3]. Beside it sit two deliberate timing simplifications, both stated
   rather than discovered: **the claims-decision delay is not modelled**, so the model pays from
   onset instead of paying a catch-up lump some months later — right in amount, early in timing; and
   the two-week *qualifizierte Mahnung* period is not modelled, so lapse falls about a month early
   [REG-R30].
9. **The charge basis.** Every level is **[std]** and the only sourced number in it is a ceiling
   [R13] [REG-R16]. Acquisition cost at the cap on a 37-year *Beitragssumme* is the largest single
   expense item and is charged entirely in month 0, so it dominates the first-year `net_cf` and
   nothing else in the projection.
10. **The *Rechnungszins*.** It touches nothing in the published cash flows — they are undiscounted —
    and everything in the premium that generates them. At 1,00 % over a 37-year contract it is a
    material lever on `prem_gross_level_pp()`, and both the rate and its effective date are
    `[unverified]` [R13] [REG-R15].
