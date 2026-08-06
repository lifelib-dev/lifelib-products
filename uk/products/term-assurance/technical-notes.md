# Term Assurance — Liability Cash Flow Model: Technical Notes (United Kingdom)

**Status:** Draft, 2026-08-03 (all cited sources accessed 2026-08-03).

**Scope note.** These notes specify a reference liability cash-flow projection model
for the standardized composite product defined in `product-spec.md` (same directory).
This is not any single insurer's product. [S#]/[R#] tags refer to the source list in
`sources.md` (numbering carried from `uk/_research/term-assurance.md`; frozen);
[REG-R#] tags refer to the cross-product reference library
`uk/references/regulatory-and-actuarial-references.md` (its own R-numbering; research
provenance in `uk/_research/regulatory-actuarial.md`). **[std]** marks
standardizations introduced for the reference implementation; [unverified] marks
claims not confirmed against a retrieved document. Parameter values are identical to
those in `product-spec.md`.

---

## Model scope and conventions

- **Purpose.** Project gross best-estimate liability cash flows (premiums, death and
  terminal illness claims by benefit shape, expenses, commission) for a single-policy
  model point of guaranteed-premium UK term assurance, in the sense required for a
  Solvency UK best-estimate projection: probability-weighted future cash-flows, gross
  of reinsurance [R1], covering the cash-flow categories of the PRA cash-flows rule
  (benefits, expenses, premiums, intermediary payments) [R2]. Discounting, risk
  margin and capital layers are out of scope (see Valuation and reserve pointers).
- **Projection frequency.** Annual grid **[std]**, with a monthly option. The only
  intra-year contractual structure is the monthly step-down of the decreasing-shape
  benefit and the monthly FIB instalments [S6][S8]; the annual grid handles both with
  mid-year approximations (below), and the monthly grid removes the approximation.
- **Timing conventions [std].** Premiums received at the start of each policy year
  (annualized, in advance); maintenance expenses at the start of each year; death/TI
  claims paid at the end of the policy year of death; lapses occur at the end of the
  policy year, after deaths. Acquisition expenses and initial commission at issue
  (start of year 1).
- **Age basis.** Age nearest birthday at entry, plus curtate policy year — attained
  age in year `t` is `x + t − 1` **[std]**. (The fetched product documents do not
  state an age basis; UK assured-lives tables are select tables — AM92 has a 2-year
  select period, TMNL16/TFNL16 a 5-year select period [R12] — so the mortality
  interface must accept select-by-duration rates.)
- **Currency.** GBP throughout. Benefits are paid in sterling to UK bank accounts
  [S1].
- **Model points.** Single-policy model points projected on an expected
  (probability-weighted) basis: survivorship factors multiply per-policy cash flows.
  No aggregation logic is specified here.
- **Termination.** All states terminate at the end of the term: cover expires with no
  maturity value, no renewal, and no conversion — there is no US-style post-level-term
  ART tail [S1][S2][S6][S8][R8]. The projection horizon is exactly `n` years.
- **Contract boundary.** Premiums are guaranteed, so the insurer has no unilateral
  repricing right and the Solvency UK contract boundary is the full term [R3]: all
  `n` years of premiums and benefits are inside the boundary. (Reviewable-premium
  variants — CI riders, out of scope — would require the rules 3.3/3.7 test [R3].)
- **Rounding.** Intermediate values at full precision; displayed cash flows to pence
  **[std]**.

---

## Model point attributes

| Attribute | Type | Example (anchor cell **[std]**) |
|---|---|---|
| `shape` | enum {level, decreasing, fib} | level |
| `issue_age` | int (age nearest birthday) | 35 |
| `sex` | enum {M, F} | M |
| `smoker` | enum {N, S} | N |
| `term_y` (`n`) | int, years (1–50; decreasing 5–50; FIB 5–40) | 25 |
| `sum_assured` (`SA0`) | GBP (level/decreasing shapes) | 150,000 |
| `fib_income` (`I`) | GBP/month (fib shape) | 1,000 |
| `sched_rate` (`j`) | annual effective (decreasing shape) | 0.06 **[std]** |
| `joint_first_death` | bool (base model: false) | false |
| `indexation` | bool (RPI option elected) | false |
| `wop` | bool (waiver rider; base model: false) | false |
| `premium_monthly` (`P_m`) | GBP/month | 12.00 **[std]** |
| `premium_mode` | enum {monthly, annual} | monthly |
| `issue_date` | date | — |

The anchor premium is a pure modeling value: no UK insurer publishes premium rate
tables (quote-engine pricing; only the £5/month minimum is public [S5]), so any
reference premium basis is constructed, not observed **[std]**.

---

## State variables

| Variable | Description | Updated |
|---|---|---|
| `l(t)` | In-force probability at the start of policy year t; `l(1) = 1` | annual recursion |
| `q(t)` | Mortality rate (incl. TI acceleration) applied in year t | assumption lookup |
| `w(t)` | Lapse rate applied in year t | assumption lookup |
| `D(t)` | Expected deaths/TI claims in year t = `l(t) × q(t)` | annual |
| `DB(t)` | Death benefit payable for deaths in year t (shape-dependent) | annual (schedule) |
| `idx(t)` | Cumulative indexation factor (1 if option not elected/declined) | on anniversaries |
| `FIBcum(t)` | Cumulative expected FIB income streams in payment at start of year t = `Σ_{s<t} D(s)` (fib shape) | annual |
| `CF(t)` | Net liability cash flow of year t (insurer perspective, + = inflow) | annual |

The FIB in-payment ledger is **not** decremented by mortality after the claim: the
instalments are an annuity-certain to the end of the term regardless of any life
[S6][S8].

---

## Assumption inputs

Three classes are distinguished explicitly.

### (a) Contractual / guaranteed elements (cited; the insurer cannot change them)

| Input | Value | Basis |
|---|---|---|
| Premium `P_m` | Level, guaranteed for the full term | guarantee [S2][S6][S9]; level **[std]** |
| Level benefit | `SA0` constant | [S1][S6] |
| Decreasing benefit schedule | `B(k)` amortization formula at rate `j` (below) | mechanics [S1][S6][S8]; `j` = 6% **[std]** |
| FIB benefit | `I`/month, in arrears, death to end of term; annuity-certain | [S2][S6][S8] |
| Terminal illness | 100% acceleration, two-limb 12-month definition, terms ≥ 2 years | [S1][S6][S8][R8][S2][S4] |
| Suicide exclusion | 12 months, year-one only | [S1][S6][S8] |
| Grace | 60 days from due date; then lapse without value | [S1][S6] |
| Surrender/paid-up value | None | [S1][S6][S8][R8] |
| Indexation option terms | cover +min(max(RPI,0),10%); premium ×(1 + 1.5×increase), cap 15%; removed after 3 declines | [S1][S2][S6][S7]; composite **[std]** |
| Expiry | Cover ceases at end of term; no renewal/conversion | [S1][S2][S6][S8][R8] |

### (b) Insurer-discretionary current elements

For guaranteed-premium life-only term assurance this class is **nearly empty** — a
deliberate contrast with cash-value products: there are no bonus rates, no MVRs, no
reviewable premiums, and no non-guaranteed charge scales on the composite. The two
residual discretionary items:

| Input | Snapshot value | Basis |
|---|---|---|
| FIB commutation basis | Commuted value = PV of remaining instalments at `r_c` = 3.0% p.a. **[std]** snapshot; base model take-up 0% | discretion ("fairly and reasonably") [S6][S8]; rate **[std]** (no insurer publishes the basis) |
| Underwriting exclusions / rated terms | None on the composite cell (standard rates) | case-by-case schedule exclusions exist [S1][S3]; scope **[std]** |

Reviewable-premium mechanics (5-yearly reviews on claims experience, reinsurance
cost, lapses, expenses, etc.) exist on CI-type covers at Aviva and Royal London
[S6][S8] and are documented there as a modeling template, but are out of scope here.

### (c) Behavioral / experience assumptions (modeler's view)

**Mortality.** The current UK protection experience tables are the CMI "16" Series —
term assurance mortality *including terminal illness* and accelerated CI, graduated
on 2015–2018 experience [R10] — with public confirmation of the table names
TMNL16/TFNL16 (male/female non-smoker, 5-year select) via their adoption in the IFoA
Formulae and Tables 2025 edition [R12]. **However, CMI tables issued after 1 March
2013 are subscriber-only** [R11], so the full 16-Series set (including
smoker/duration variants) cannot be redistributed in an open reference
implementation. The reference basis is therefore a **[std] proxy**, stated honestly:

| Input | Recommended public basis | Basis tags |
|---|---|---|
| Best-estimate mortality (incl. TI) | Shape of the public "00" Series temporary assurance tables — TMN00/TMS00 (male non-smoker/smoker), TFN00/TFS00 (female), 1999–2002 experience — scaled by a **[std]** adjustment factor (suggested 75%) to proxy improvement to the 16-Series era; AM92 (2-year select, prior Formulae and Tables basis) is the teaching-table alternative | tables [R13][R11]; AM92 role [R12]; factor **[std]** |
| Mortality improvement | None in base **[std]**. The CMI Mortality Projections Model is the market-standard overlay — CMI_2024 (June 2025, WP201) [R14], superseded by CMI_2025 (March 2026, WP211) [REG-R30] — but the model is subscriber-restricted; a production basis would be "x% of TMNL16/TFNL16 with CMI_2025 improvements at a chosen long-term rate", all subscriber inputs | [R14][REG-R30][R11] |
| Population fallback | ONS national life tables (single-age qx, freely redistributable under OGL) — heavier than insured experience; use only as a last-resort open base | [REG-R32] |
| TI acceleration timing | None modeled: death and TI are one decrement, one benefit; acceleration shifts payment earlier by less than 12 months, immaterial on an annual grid **[std]** | definition [S1][S6][S8]; 16-Series mortality includes TI [R10] |
| Suicide-exclusion offset | Year-one claims not reduced for excluded suicides **[std]** (immaterial; no incidence data in fetched sources) | clause [S1][S6][S8] |

**Lapse.** FCA evidence (2024, pure protection in force): average lapse rate 5% p.a.;
highest observed early lapse 23% in policy year 1 (non-advised intermediated sales
with 4-year clawback); modest lapse spikes just after the 2-year and 4-year
commission clawback periods end [R9]. A full duration curve is not public, so the
reference table is **[std]**, anchored to the 5% average and the clawback-spike
pattern:

| Policy year | 1 | 2 | 3 | 4 | 5 | 6+ |
|---|---|---|---|---|---|---|
| Annual lapse `w(t)` **[std]** | 10% | 8% | 7% | 5% | 6% | 4% |

(Year 3 staying elevated after the 2-year clawback period ends, and the year-5
uptick after the 4-year clawback period ends, echo the post-clawback spike pattern
[R9]; levels are standardized calibrations to be replaced with the user's
experience.)

**Expenses and commission (all levels [std]; structure evidence as cited).**

| Input | Value | Basis |
|---|---|---|
| Initial (acquisition) expense | £150 per policy at issue | **[std]** |
| Initial commission | 150% of annualized premium, paid upfront at issue | upfront pattern ~96% of commission [R9]; level **[std]** |
| Commission clawback | On lapse in years 1–4: clawback of `(48 − months in force)/48` of initial commission (linear, 4-year) — optional module, base model off | clawback periods 2–4 years [R9]; formula **[std]** |
| Renewal commission | 2.5% of premiums from year 2 | **[std]** |
| Maintenance expense | £30 per policy p.a., inflating 3% p.a. | **[std]** |
| Claim expense | £250 per death/TI claim | **[std]** |
| Expense inflation | 3% p.a. flat | **[std]** |

---

## Cash flow components and recursions

### Notation (defined once, used throughout)

| Symbol | Meaning |
|---|---|
| `t` | policy year, t = 1..n; attained age in year t = x + t − 1 (x = issue age) |
| `k` | policy month, k = 0..N, N = 12n (monthly grid / benefit schedules) |
| `P_a` | annualized premium = 12 × P_m = 144.00 (anchor cell) **[std]** |
| `q(t)` | mortality (incl. TI) rate for year t, select-adjusted |
| `w(t)` | lapse rate for year t (end-of-year, after deaths) **[std order]** |
| `l(t)` | in-force probability at start of year t; l(1) = 1 |
| `D(t)` | expected claims in year t = l(t) × q(t) |
| `SA0` | initial sum assured (level/decreasing) |
| `I` | FIB monthly income |
| `j`, `j_m` | decreasing schedule annual rate; j_m = (1+j)^(1/12) − 1 |
| `B(k)` | decreasing-shape benefit after k months (formula below) |
| `idx(t)` | cumulative indexation factor at start of year t (1 if not indexed) |
| `E0`, `e(t)` | initial expense (150); maintenance expense = 30 × 1.03^(t−1) |
| `c0`, `c_r` | initial commission (1.5 × P_a); renewal commission rate (0.025, from year 2) |
| `ec` | claim expense (250) |
| `CF(t)` | net cash flow of year t, insurer perspective (+ inflow, − outflow) |

Dimensional check: `q`, `w` are per-annum probabilities (dimensionless); `B`, `SA0`
are GBP; `I` is GBP/month so FIB outgo terms carry explicit month counts; all `CF`
components are GBP per year.

### Benefit amount by shape

**Level:** `DB(t) = SA0 × idx(t)`.

**Decreasing** [S1][S6][S8]:

    B(k) = SA0 × [(1+j_m)^N − (1+j_m)^k] / [(1+j_m)^N − 1],   B(0) = SA0, B(N) = 0

Annual-grid death benefit uses the mid-year balance **[std]**:

    DB(t) = B(12(t−1) + 6)

(whole-year identity `(1+j_m)^12 = 1+j` allows `B(12t) = SA0 × [(1+j)^n − (1+j)^t] /
[(1+j)^n − 1]`; the monthly grid uses `B(k)` at the exact month of death).
Numeric anchor (SA0 = 150,000, j = 6%, n = 25): `B(60) = 150,000 × (1.06^25 − 1.06^5)
/ (1.06^25 − 1) = 150,000 × (4.291871 − 1.338226) / 3.291871 = £134,588` — the
benefit after 5 years. Indexation and the decreasing shape are not combined
**[std scope]** (no fetched insurer offers indexed decreasing cover).

**Family income benefit** [S2][S6][S8]: a death in month k triggers `N − k` monthly
instalments of `I`, in arrears, ending at month N — an annuity-certain independent of
survival. On the annual grid, with deaths at mid-year **[std]**, a death in year s
generates expected instalment outgo:

    FIB outgo in year s (year of death):        6 × I × D(s)
    FIB outgo in later year u, s < u ≤ n:      12 × I × D(s)

so total FIB claim outgo in year t is

    Claims_fib(t) = I × [ 6 × D(t) + 12 × FIBcum(t) ],   FIBcum(t) = Σ_{s<t} D(s)

Optional commutation module **[std]**: replace the instalment stream at death with a
lump sum `CV(k) = I × a(N−k)` where `a(m) = [1 − (1+r_c)^(−m/12)] / [(1+r_c)^(1/12) − 1]`
is the m-month annuity-certain factor at the snapshot commutation rate `r_c` = 3%
**[std]** (contractually the insurer reduces the sum of remaining instalments
"fairly and reasonably" [S6][S8]). Base model: no commutation.

### In-force recursion and processing order

Annual processing for year t = 1..n **[std]**:

1. **Start of year:** premium income `P_a × idx_p(t) × l(t)` (where `idx_p(t)` is the
   cumulative *premium* indexation factor — equal to 1 in the base run); maintenance
   expense `e(t) × l(t)`; renewal commission `c_r × P_a × idx_p(t) × l(t)` (from
   t ≥ 2). At t = 1 additionally `E0` and `c0` (per policy issued, l(1) = 1).
2. **Benefit schedule:** compute `DB(t)` per shape (mid-year balance for decreasing).
3. **End of year — claims:** expected death/TI outgo `DB(t) × D(t)` (level/
   decreasing) or the FIB formula above; claim expense `ec × D(t)`.
4. **End of year — lapses:** applied to survivors of mortality **[std order: death
   before lapse]**; lapse pays nothing (no surrender value [S6][R8]).
5. **Update:**

       l(t+1) = l(t) × (1 − q(t)) × (1 − w(t))

6. **Anniversary (if indexation elected):** with acceptance (behavior section),
   `idx(t+1) = idx(t) × (1 + min(max(RPI, 0), 0.10))` and
   `idx_p(t+1) = idx_p(t) × (1 + min(1.5 × increase, 0.15))` [S1][S2][S6].

At t = n the projection ends: no maturity payment, no tail states [S1][S6][S8][R8].

### Net cash flow

Level/decreasing shapes:

    CF(t) = P_a × idx_p(t) × l(t)                                   (premiums)
          − DB(t) × D(t)                                            (death/TI claims)
          − ec × D(t)                                               (claim expense)
          − e(t) × l(t)                                             (maintenance)
          − c_r × P_a × idx_p(t) × l(t) × 1{t ≥ 2}                  (renewal commission)
          − (E0 + c0) × 1{t = 1}                                    (acquisition)

FIB shape: replace the claims term with `Claims_fib(t)` and add `− ec × D(t)` only in
the year of death. Premiums stop at death, but FIB instalments continue — premium
income always carries `l(t)`, never the FIB ledger.

Monthly-grid variant: the same components at monthly frequency with `P_m`, monthly
decrements `q_m = 1 − (1 − q)^(1/12)`, `w_m = 1 − (1 − w)^(1/12)` **[std]**, exact
`B(k)`, and exact FIB instalments; the annualization and mid-year approximations
disappear. The annual grid slightly overstates premium income (no allowance for
premiums ceasing at mid-year deaths/lapses) — a known bias of the annual-in-advance
convention **[std]**, quantified in the pitfalls list.

### Waiver of premium (optional module, base off)

With `wop = true`, an incapacity state is added: incidence `inc(t)` **[std]**
(no public UK incidence basis for the WOP work-tasks definitions is in the fetched
sources), 26-week deferred period [S1], premiums waived while incapacitated (premium
income multiplied by the active-payer probability), mortality unchanged. The WOP
extra premium and the incidence/recovery basis are both **[std]** placeholders.

---

## Policyholder behavior modeling

All dynamic formulas are **[std]** reference constructions; calibration evidence is
cited where it exists.

- **Base lapse [std].** Duration table above, anchored to the FCA 5% in-force average
  and clawback-spike pattern [R9]. Channel matters: the 23% year-1 observation is
  specific to non-advised intermediated business with 4-year clawback [R9]; the
  composite table is channel-blended.
- **Selective lapsation [std] (optional module).** Lapsers are healthier on average;
  persisters' mortality is loaded:

      q_eff(t) = q(t) × [1 + λ × max(0, w_cum(t) − w_ref)]

  with `w_cum(t)` = cumulative lapse proportion to date, `w_ref` = 0.20 and λ = 0.25
  **[std]**. Base run: off (λ = 0).
- **Rebroking/dynamic lapse [std].** Guaranteed premiums mean no premium-shock lapse;
  the economic driver is rebroking when quoted market premiums for the attained age
  fall below the in-force premium (younger select lives, falling mortality). A
  reference multiplier:

      M_reb(t) = min(2.0, max(1.0, P_inforce / P_market(t)))

  applied to `w(t)`, with `P_market(t)` an external input; base run `P_market =
  P_inforce`, so M_reb = 1.
- **Indexation take-up [std].** If `indexation = true`: each anniversary the increase
  is accepted with probability 80% **[std]**; after 3 consecutive declines the option
  is removed [S1][S6] (RL: 2 [S8]). Deterministic base run: always accept, RPI
  scenario input flat 3% **[std]**, giving `idx(t+1) = idx(t) × 1.03` and
  `idx_p(t+1) = idx_p(t) × 1.045` (premium factor 1.5 [S1][S2][S6]).
- **GIO exercise.** Not modeled: exercises create *new* policies at then-current
  rates [S1][S6][S8], so they add model points rather than changing this one
  **[std scope]**.

---

## Worked example

Anchor cell: male 35 non-smoker, single life, level shape, `n` = 25, `SA0` =
£150,000, `P_m` = £12.00 (`P_a` = £144.00) **[std]**; no indexation, no WOP, no
commutation; base lapse table; no selective-lapse or rebroking modules. Mortality
placeholders `q(1) = 0.00055, q(2) = 0.00060, q(3) = 0.00065` are **[std]
illustrative values in the shape of a non-smoker temporary assurance table** — they
are NOT taken from any CMI table (the current tables are subscriber-only [R11]; see
assumption class (c)). Expenses per the [std] table: `E0` = 150, `c0` = 1.5 × 144 =
216.00, `e(t)` = 30 × 1.03^(t−1), `c_r` = 2.5% from year 2, `ec` = 250.

| t | l(t) | Premiums `P_a·l(t)` | Claims `SA0·D(t)` | Claim exp `ec·D(t)` | Maint. + initial exp | Commission | Net CF(t) |
|---|---|---|---|---|---|---|---|
| 1 | 1.000000 | 144.00 | 82.50 | 0.14 | 180.00 | 216.00 | −334.64 |
| 2 | 0.899505 | 129.53 | 80.96 | 0.13 | 27.79 | 3.24 | +17.41 |
| 3 | 0.827048 | 119.09 | 80.64 | 0.13 | 26.32 | 2.98 | +9.02 |

Trace, year 1: `D(1) = 1.0 × 0.00055 = 0.00055`; claims = 150,000 × 0.00055 = 82.50;
claim expense = 250 × 0.00055 = 0.14; expenses = E0 + e(1) = 150.00 + 30.00 = 180.00;
commission = c0 = 216.00; CF(1) = 144.00 − 82.50 − 0.14 − 180.00 − 216.00 = −334.64.
Update: `l(2) = 1.0 × (1 − 0.00055) × (1 − 0.10) = 0.899505`.

Trace, year 2: premiums = 144 × 0.899505 = 129.53; `D(2) = 0.899505 × 0.00060 =
0.000540`; claims = 150,000 × 0.000540 = 80.96; claim expense = 0.13; maintenance =
30 × 1.03 × 0.899505 = 27.79; renewal commission = 0.025 × 129.53 = 3.24;
CF(2) = 129.53 − 80.96 − 0.13 − 27.79 − 3.24 = +17.41.
Update: `l(3) = 0.899505 × (1 − 0.00060) × (1 − 0.08) = 0.827048`.

The pattern is characteristic of guaranteed term: a deep new-business strain in year
1 (upfront commission and acquisition expense against one year's premium [R9]) and
thin positive margins thereafter — the level premium prefunds the rising mortality
cost, so early-duration lapses forfeit margin to the insurer while late-duration
lapses relieve it.

---

## Statutory accounting and capital

Framework and the shared model-output contract are in
`uk/regulatory/statutory-accounting-and-capital.md` (what the items are) and
`uk/regulatory/technical-notes.md` (how to calculate them); this section states only what
is specific to term assurance. [REG-R#] resolves against the shared UK numbering in
`uk/references/regulatory-and-actuarial-references.md`, which now runs **R1–R120**, with
**R50–R52, R74–R76 and R121–R133 unused by design** — an unused number is not a missing
entry. Product-local [S#] and [R#] tags continue to resolve against `sources.md`.

**Three ledgers, not one.** The UK has no "statutory accounting" in the U.S. sense. One
projection feeds three separate measurements: the **Solvency UK regulatory balance sheet**
(PRA Rulebook — a supervisory measurement, not a set of accounts), the **statutory
accounts** (Companies Act accounts under FRS 102 + FRS 103, or UK-adopted IFRS 17), and
**tax**, which is not a liability measurement at all but is computed *from the accounts*
with the Finance Act 2012 overlay [REG-R39][REG-R99][REG-R105][REG-R17][REG-R18]. For this
product the three answers differ in sign, not merely in size — see **Technical provisions**
and **Statutory accounts and tax** below.

### Contract classification and reporting

- **Regulated Activities Order class.** Long-term insurance, **Class I** (life and annuity),
  RAO 2001 Schedule 1 Part II [REG-R14] (product-local [R6]). This is fixed for every cell of
  the composite — level, decreasing and family income benefit alike — because all three pay on
  death or terminal illness of a named life and carry no investment element [S1][S6][S8].
- **Solvency UK line of business: 32, "other long-term insurance business".** Segmentation is
  into homogeneous risk groups and at minimum by line of business (TP 10.1), the lines being
  those in **Annex 1** to the TPFR Part; assignment "must reflect the nature of the risks" and
  the **legal form is not necessarily determinative** (TPFR 26.2) [REG-R1][REG-R41]. **Annex 1
  names no products**, so the assignment of non-profit term assurance to LoB 32 is the
  library's inference from TPFR 26.2/26.3 and the Annex 1 definitions, not a quotation
  [REG-R41]. A death benefit is not "financial compensation arising from illness, accident,
  disability or infirmity", so it is not a health insurance obligation and LoB 29 is not in
  play [REG-R42].
- **PRA three-digit product codes: 404 and 424.** The IR.14.01 instruction file's appendix —
  the former SS36/15 content, and the single best map from UK product taxonomy to regulatory
  reporting — gives protection the codes **404 level term regular premium**, **414 level term
  single premium**, **424 decreasing term regular premium** and **434 decreasing term single
  premium** [REG-R89]. The composite is regular-premium monthly direct debit throughout
  [S6][S9], so only **404** (level shape) and **424** (decreasing shape) are reachable; 414 and
  434 belong to a single-premium variant this library does not specify.
- **Family income benefit has no code in the retrieved appendix.** No code in the protection
  block names family income benefit, and the appendix as retrieved offers none [REG-R89]. Two
  routes are available on the retrieved text and **neither is asserted here**: the FCA
  characterises FIB as a form of decreasing term assurance in present-value terms [R8], which
  points at 424; and the instruction's own fallback — where technical provisions are calculated
  for a combination of products, or "the product code is uncertain, firms should use an
  approximation to apportion between product codes" [REG-R89]. Record the choice made; do not
  treat it as settled.
- **Templates this product drives.** **IR.12.01** life technical provisions, in the LoB 32
  column — and *not* the unit-linked rows R0300/R0302/R0304, and with no technical-provisions-as-
  a-whole amount to disclose in R0025/R0026/R0030, since TPFR 22.2 declares biometric-dependent
  cash flows and **all** servicing expenses non-replicable [REG-R89][REG-R41]. **IR.14.01** life
  obligations analysis, per product code per fund per line of business: contracts in force at
  year end, new contracts in the year, gross written premiums, gross claims paid, gross best
  estimate and **capital at risk "as defined in Solvency Capital Requirement – Standard Formula
  7.8 and 7.10"**; direct and accepted reinsurance only, **reinsurance ceded is not reported**
  [REG-R89]. **IR.26.03** SCR life underwriting risk, **IR.28.01** MCR, **IR.05.03** life income
  and expenditure (prepared on financial accounting conventions, not on a Solvency II basis)
  and **IR.05.10** excess capital generation, plus the SFCR templates and section D.2 narrative
  [REG-R84][REG-R90][REG-R85].
- **IR.12.04 is where this product has rows of its own.** The best-estimate assumption pack
  carries, for each assumption type, the current-year valuation basis, the prior-year basis and
  **five years of the firm's own experience**, expressed as percentages of a **named** mortality
  or morbidity table in column C0080 [REG-R89]. The rows that are this product's own:
  mortality **R0010 / R0090** male non-smoker / male smoker and **R0130 / R0210** female
  non-smoker / female smoker (matching the model point's `sex` and `smoker` fields exactly),
  **R0250 assurance mortality change per annum** (the ten-year equivalent annual rate, left
  blank where no allowance for change is made), lapse **R0810 / R0850 / R0890 level term years
  1–5 / 6–10 / 11+** and **R0930 / R0970 / R1010 decreasing term years 1–5 / 6–10 / 11+**, and
  **R1890 per-policy renewal management expense unit cost — term assurance**, with **R1290**
  expense inflation after the valuation date [REG-R89]. The lapse row bands are **not** the
  band structure of this file's [std] duration table (10/8/7/5/6/4% by year); the template wants
  the arithmetic average of the annual rates within each band for the basis columns, and permits
  arithmetic or weighted averaging for the experience columns "provided this is applied
  consistently" [REG-R89]. The template applies where the firm's gross best estimate exceeds
  **£50m** *or* gross written premiums exceed **£10m** — a **firm-level**, not a product-level,
  test [REG-R89].
- **The with-profits templates do not bite.** IR.12.05 (value of bonus) and IR.12.06
  (WPBR/FPRL decomposition) are triggered by with-profits business with net BEL above **£500m**
  and are completed per ring-fenced fund that is a with-profits fund [REG-R90]; the composite is
  non-participating with no bonus and no discretionary benefit [S2][S6][S9], so there is nothing
  to report. Neither do IRR.22.02/IRR.22.03 or MALIR 1–7, which are matching-adjustment
  templates [REG-R91] (see **Technical provisions** on MA ineligibility).
- **What the retrieved instructions do not settle.** (i) The FIB product code, above.
  (ii) IR.14.01 column C0030 is a **closed list of lines of business that the firm applies
  itself**, so the LoB 32 assignment above is the firm's, not the template's [REG-R89].
  (iii) **PS18/26 removes claims management expenses from the IR.14.01 "claims paid" definition
  from the 31 December 2026 reference date** [REG-R87] — a definition change inside the
  reporting horizon of any model built now, and the two definitions must not be blended across
  years. (iv) The IR.12.04 requirement for a **named** table collides with this library's
  mortality basis: the current UK protection tables are subscriber-only [R11][R13], so the
  reference basis here is an honest **[std]** proxy that could not be filed as a named table in
  a real return (see **Traps** below).

### Technical provisions

- **Contract boundary: the full term, and the long-term carve-out is confirmatory only.**
  Premiums are level and guaranteed for the whole term on life-only cover [S2][S6][S9], so the
  firm holds none of the three TPFR 3.3 rights — no unilateral right to terminate, none to
  reject premiums, and none to amend premiums or benefits so that they fully reflect the risks
  [REG-R41] (product-local [R3]). TPFR 3.3(3)'s carve-out — that for long-term business
  individually underwritten at inception, where the assessment cannot be repeated before
  repricing, the "premiums fully reflect the risks" test is applied **at the level of the
  contract** rather than the portfolio — does real work only where a repricing right exists, on
  **reviewable-premium** critical illness and income protection. On guaranteed-premium term
  assurance it merely confirms a full-term boundary [REG-R41]. TPFR 3.7 is in any case a
  demanding test: premiums fully reflect the risks only where there is **no circumstance** under
  which portfolio benefits and expenses exceed portfolio premiums. TPFR 3.5's savings-contract
  cut has nothing to operate on: this contract compensates for a specified uncertain adverse
  event. Reinsurance recoverables inherit the same boundary (TPFR 23.1) [REG-R41].
- **Cash flows in scope, and the one that is usually mis-classified.** TPFR 13.1 requires eight
  streams; four are live here — benefit payments, expenses, **premiums and any additional cash
  flows resulting from them**, and **payments between the firm and intermediaries** [REG-R41].
  That fourth stream makes **initial commission and its clawback an in-scope best-estimate cash
  flow, not an expense-loading convention**: the `c0` = 1.5 × `P_a` upfront commission and the
  optional `(48 − months in force)/48` clawback module specified above are BEL cash flows and
  must be projected as such. Salvage and subrogation, benefits in kind, and payments to
  investment firms for index-linked and unit-linked benefits are all nil. Stream (8),
  **policyholder-charged taxation**, is nil on the composite: there is no surrender value and no
  investment element [S6][R8], so no chargeable-event machinery arises [REG-R15][REG-R16].
  Shareholder corporation tax is **not** a best-estimate cash flow; it enters through deferred
  tax under Valuation 11 [REG-R39][REG-R41].
- **Expenses: two bases, and the library's inflation choice is unsourced.** TPFR 16.1 names four
  categories — administrative, investment management, claims management and **acquisition** —
  each including allocated overheads, allocated "in a realistic and objective manner and on a
  consistent basis over time" (16.2); **TPFR 16.4 requires expenses to be projected on the
  assumption that the firm will write new business in the future** [REG-R41]. So the £30 p.a.
  per-policy maintenance expense **[std]** above is a *going-concern* unit cost, not a run-off
  unit cost with overheads re-spread over a shrinking book. **Nothing in the rules prescribes an
  inflation index (RPI, CPI or national average earnings), an inflation rate, or a
  per-policy/per-premium split** [REG-R41] — the flat 3% p.a. and the per-policy basis are
  library **[std]** choices, and remain so. TP 9.1(2) does require inflation, including expense
  and claims inflation, to be allowed for [REG-R1]. This sits in unreconciled tension with the
  risk margin, whose reference undertaking "assumes no new obligations" after the transfer (TP
  4B.1(5)) [REG-R1]: a model must carry **two expense bases**, and **no retrieved source
  explains how the reference undertaking's expenses should be set given that tension**.
- **The best estimate is normally negative, and nothing floors it.** For profitable
  guaranteed-premium term assurance the present value of premiums inside a full-term boundary
  exceeds the present value of claims and expenses, so `BEL < 0` at issue — an asset on the
  regulatory balance sheet. The technical-provisions research searched the **Valuation,
  Technical Provisions and TPFR Parts** in full and found no zero floor, no surrender-value
  floor and no contract-level non-negativity rule; the single occurrence of "negative" is TPFR
  25.2's EUR-peg currency adjustment [REG-R41]. Three independent confirmations from the product
  side: the Solvency I floor at **INSPRU 1.2.62R was expressly not carried over**, INSPRU 1.2
  not applying to a Solvency II firm [REG-R115]; a secondary source states there is no
  surrender-value floor in the rules [REG-R118 — **an entry with no recorded URL, cited without
  one rather than with a guessed one**]; and the reporting layer treats surrender value as a
  **disclosure** item in IR.14.01, not a constraint [REG-R89]. This product goes one step
  further than the general case: it has **no surrender value and no paid-up value at all**
  [S1][S6][S8][R8], so there is no floor candidate to argue about on the prudential ledger. The
  projection must therefore emit the **unfloored** best estimate with the sign preserved through
  every aggregation; the floor that does exist belongs to the statutory accounts (below), never
  inside the projection [REG-R41][REG-R100].
- **Options and guarantees, and why no stochastic valuation is required.** TP 9.2(1) requires
  the value of financial guarantees and contractual options to be taken into account, and 9.2(2)
  requires realistic exercise assumptions **including lapses and surrenders**, allowing for the
  impact of future changes in financial and non-financial conditions [REG-R1]. TPFR 19.4–19.5
  force a scenario-based method only where the present value depends on **expected future
  outcomes and on scenario deviation from the expected outcome** [REG-R41]. A level-premium term
  assurance with no surrender value, no account value, no bonus and no financial guarantee has
  no such asymmetry, which is why the applicability matrix marks stochastic valuation `--` for
  this product. The three options the representative design actually carries are all
  non-financial: **terminal illness acceleration** (embedded, no extra premium, a timing shift
  of the same benefit [S1][S6][S8]); the **RPI indexation option** (an escalation right whose
  take-up is behavioural — modelled at 80% acceptance **[std]** above); and the **guaranteed
  insurability option**, which is written as a *new policy at then-current rates*
  [S1][S6][S8]. **No retrieved source addresses the contract-boundary treatment of a guaranteed
  insurability option.** TPFR 3.2 brings in obligations relating to unilateral rights of **the
  firm** to renew or extend [REG-R41]; a GIO is a policyholder right whose exercise creates a
  separately-priced contract, so this library's treatment — new model points, no in-boundary
  obligation on the parent policy **[std scope]** — is a modelling decision, recorded as such
  and not resolved from the sources.
- **Policyholder behaviour: the rule against a static lapse table, and why this product can
  nearly satisfy it.** TPFR 11.1 requires an analysis of past behaviour and a prospective
  assessment, taking account of how beneficial exercise was and will be, past and future
  economic conditions, past and future management actions, and closes: "**The likelihood shall
  only be considered to be independent of the elements referred to in (1) to (4) where there is
  empirical evidence to support such an assumption**" [REG-R41]. The research records that for a
  term assurance with no surrender value the evidence for independence is much easier to sustain
  than for an option-bearing contract — but the analysis and the prospective assessment are
  still required, and the **rebroking** driver modelled above (`M_reb(t)` on the ratio of
  in-force to market premium) is exactly the moneyness dependence TPFR 11.1 has in mind. The
  [std] duration table is a calibration, not an exemption.
- **The matching adjustment is unavailable, on the first condition.** MA 2.2 requires, among
  other things, **no future premium payments** on the portfolio; permits only longevity, expense,
  revision, mortality or recovery-time underwriting risk; and where mortality risk is present
  caps the increase in best estimate under the prescribed mortality stress at **5%** [REG-R2]. A
  regular-premium term assurance fails at the first condition and would fail the 5% cap in any
  case, mortality being its whole risk. The **eligible-element route** (MA 1.2) does not reach it
  either: an eligible element is either the guaranteed element of a with-profits immediate or
  deferred annuity, or the in-payment element of a group death-in-service dependants' annuity or
  an income protection policy [REG-R2]; term assurance is not in that list, and SS7/18 records
  that outside those cases the PRA regards no notional splitting of a contract as compatible
  with MA 2.3 [REG-R8]. Every MA, MAIA and attestation row is therefore `--` for this product,
  and the SFCR MA/VA disclosure does not arise.
- **Reinsurance recoverables and the one hard numeric floor.** UK protection is heavily reinsured
  and reinsurers influence pricing and product design [R8] (the frequently-quoted 70–90%+ cession
  range remains **[unverified]**). Recoverables are calculated on the same apparatus and the same
  boundaries as the gross best estimate, adjusted for the time difference between amounts
  becoming recoverable and actually received (TP 11.1), and reported **separately** for SPVs, for
  finite reinsurance and for other reinsurance (TPFR 23.2) [REG-R1][REG-R41]. The
  counterparty-default adjustment is calculated separately from the recoverables, ignoring
  risk-mitigation techniques other than collateral, over the lifetime of the contract, and
  **separately by counterparty and by line of business** (TPFR 24.1–24.3); TPFR 24.4 then imposes
  the only hard numeric floor in the whole technical-provisions apparatus — the average loss
  "**must not be assessed at lower than 50% of the amounts recoverable … unless there is a
  reliable basis for another assessment**" [REG-R41]. **What counts as a "reliable basis" is not
  settled by any retrieved source.** SS20/16 on reinsurance counterparty credit risk was
  retrieved at **landing-page level only** and nothing beyond its existence is asserted
  [REG-R120].

### The risk margin

Formula, cost-of-capital rate and taper are in `uk/regulatory/technical-notes.md`, "The risk
margin"; they are not restated here. Technical provisions = best estimate + risk margin (TP 2.4)
[REG-R1], cost-of-capital **4%**, life risk-tapering factor **λ = 0.9** with floor **0.25**
[REG-R1][REG-R4][REG-R44]. Three things are specific to this product.

1. **The shared worked example is a term assurance.** The three-year illustration carried through
   `uk/regulatory/technical-notes.md` ("The risk margin", and "Worked example — one policy,
   carried through") is a term assurance cell, driven by expected sum assured in force. Read it
   before implementing; it is the closest thing in the library to a validation target for this
   product's risk margin.
2. **The risk margin offsets but does not floor the negative best estimate.** It is non-negative
   by construction, so `TP = BEL + RM` can and routinely does remain **negative** for a
   profitable protection cell — in the shared example, `BEL = −23.790911` and `RM = 21.045512`
   give `TP = −2.745399` [REG-R1].
3. **Run-off shape differs by benefit shape.** On the 25-year anchor cell the taper is still in
   its `λ^t` regime for `t = 0…13` and sits on the `λ_floor = 0.25` floor only for `t = 14…24` —
   14 of the 25 run-off terms in the decay regime against 11 on the floor — and because each term
   is discounted over `t+1` years and the sum-assured-in-force driver falls, the decay regime
   carries the large majority of the weight, not the floor. The floor covers more *terms* than the
   decay only beyond about `n = 29` within the 1–50-year envelope [S2][S4][S7]; even at `n = 50`
   the early decay terms still carry more of the discounted sum, so the floor lengthens the tail
   rather than dominating the answer. On the three-year illustration the floor never binds. (Both
   the threshold `ln 0.25 / ln 0.9 ≈ 13.16` and the `n ≈ 29` crossover are **derived from the rule
   and appear in no retrieved source**, and must never be cited to [REG-R1], [REG-R4] or
   [REG-R44].) For the **decreasing** shape the natural driver falls on both `l(t)` and the
   amortisation schedule `B(k)`, so the run-off is materially faster than the level shape; for the
   **FIB** shape the capital-at-risk driver is the maximum remaining instalments, `I × (N − k)`,
   which also amortises. Choosing one driver per sub-module and re-aggregating with the **same**
   correlation matrices at each `t` is the shared file's **[std]** drivers approach — an
   engineering suggestion legally usable only after a documented TPFR 27.4 error assessment
   [REG-R41].

### SCR — the modules that bite

Module tree, correlation matrices, stress sizes and the aggregation arithmetic are in
`uk/regulatory/technical-notes.md`, "The standard formula SCR". What follows is only this
product's incidence.

**Life underwriting `3B`, not health `3C`.** `SCR-SF 3.2A` sends life obligations *other than
health insurance obligations* to the life module and health obligations to the health module —
the health module is not a residual, it **takes precedence** [REG-R62][REG-R42]. A death benefit
is not "financial compensation arising from illness, accident, disability or infirmity" in the
Glossary sense, so term assurance is a life obligation and the whole of chapter `3C` is out of
scope. **Terminal illness benefit is the one loose thread**: it accelerates the death benefit on
diagnosis, which raises the same TPFR 26.7 unbundling question as accelerated critical illness —
"where a contract of insurance includes health insurance obligations and other insurance
obligations, those obligations must, **where possible**, be unbundled" — at much smaller
materiality. Since the benefit pays **once**, on the earlier of death and diagnosis, the legs are
not additive and unbundling is not obviously "possible". **Recorded, not resolved**
[REG-R41][REG-R42].

| Sub-module | Rule | Stress | Bites? |
|---|---|---|---|
| Mortality | `3B1.1` | permanent **+15%** (relative) to the mortality rates used for the TP calculation | **yes — the dominant charge** |
| Longevity | `3B2.1` | permanent **−20%** | no: lower mortality reduces provisions, so the `3B2.2` filter excludes it |
| Disability-morbidity | `3B3.1` | +35% / +25% / −20% recovery | no: no disability benefit on the composite (WOP is an optional rider, base off) |
| Life expense | `3B4.1` | **+10%** to the amount of expenses **and +1 percentage point** to expense inflation | yes |
| Revision | `3B5.1` | permanent **+3%** to annuity benefits | no: no annuity benefit and no revision right |
| Lapse | `3B6` | highest of three — see below | **yes** |
| Life catastrophe | `3B7.1` | **+0.15 percentage points** (absolute, i.e. +0.0015 in decimal) to year-1 mortality rates, **following 12 months only** | yes |

All of these require a **full revaluation** of the best estimate on the stressed assumption set
[REG-R62]. Mortality, longevity and life catastrophe apply **only to policies for which the
stress increases technical provisions without the risk margin**; multiple policies on the same
insured person may be treated as one (`3B1.2`, `3B1.3`, `3B2.2`, `3B7.2`) — which is where the
composite's **joint life first death** basis and any GIO-generated sibling policies have to be
identified as one exposure [S1][S2][S6].

**Two shape-specific observations, both derivations from the rule and this product's mechanics;
no retrieved source addresses family income benefit.** (i) `3B7.1` stresses **year-1 rates only**,
but on the FIB shape a year-one claim generates up to `N − 1` further monthly instalments of `I`,
so the catastrophe charge per unit of first-year claim is far larger than the level shape's
single lump sum. (ii) The `3B1.1` +15% acts on the same decrement that drives both the new-claim
term and the growth of the in-payment ledger `FIBcum(t)`, so the FIB revaluation must re-run the
whole annuity-certain ledger, not just the claim year.

**Lapse: the direction is computed, never named.** `3B6.1` takes the **highest** of three
scenarios and two of them carry a directional filter [REG-R62]:

- `3B6.2` **lapse up** — permanent **+50% relative** increase in option exercise rates, capped so
  the increased rates do not exceed 100%, applying **only to options for which exercise would
  *increase* technical provisions without the risk margin**;
- `3B6.3` **lapse down** — permanent **−50% relative** decrease, the decrease not to exceed **20
  percentage points**, applying **only where exercise would *decrease* technical provisions**;
- `3B6.6(2)` **mass lapse** — **40%** instantaneous discontinuance, again only of policies for
  which discontinuance would increase technical provisions without the risk margin.

For this product the best estimate is negative because expected future premiums exceed expected
future claims and expenses, and **lapse pays nothing** [S6][R8]. Discontinuance therefore removes
a *negative* liability and **increases** technical provisions, so a policy in that state is
filtered **into** `3B6.2` and into the 40% mass event, and **out of** `3B6.3`. That is the
applicability matrix's mark for term assurance — lapse up and mass lapse material, lapse down
conditional [REG-R62].

**The contrast that makes this a classic error.** A genuinely **lapse-supported** design — the
over-50s guaranteed-acceptance whole of life, where the policyholder has paid premiums, there is
no surrender value and lapsing makes a *certain* future claim disappear — has a **positive**
technical provision that discontinuance *reduces*. It is therefore filtered into `3B6.3` and out
of `3B6.2` and the mass event, and **the binding stress on it is lapse *down***, with the mass
lapse charge nil [REG-R62]. Naming a product "protection" and reaching for lapse-up, or naming it
"lapse-supported" and reaching for lapse-down, both skip the step the rule actually requires.
**One tension is reproduced rather than resolved:** the product-applicability research's §13.2
closes by extending the lapse-down logic to "any cell whose best estimate is negative because
expected future premiums exceed expected future claims", while its own matrix and notes mark
lapse **up** material for term assurance and the 40% mass event applicable. The two readings point
opposite ways; the rule text is the arbiter, and it is a **per-policy, per-valuation** filter
whose answer flips as a policy matures. The natural diagnostic is the **surrender strain** defined
at `7.12(3)` — *(amount currently payable on discontinuance, net of amounts recoverable from
policyholders or intermediaries) − (technical provisions without the risk margin)*, signed, per
policy [REG-R62]. On this product the first term is identically **zero** [S1][S6][S8], so the sign
of the surrender strain is simply the sign of the negated best estimate.

Three further lapse points that are this product's own:

- **`1.2` defines discontinuance to include making a contract paid-up**, and `3B6.8` requires the
  mass event to use **the type of discontinuance that most negatively affects basic own funds on
  a per-policy basis** [REG-R62]. This product has **no surrender value and no paid-up value**
  [S1][S6][S8], so the discontinuance menu has exactly one member and the worst-of collapses — a
  rare simplification, and one that disappears the moment a variant with values is modelled.
- **`3B6.4` reaches the indexation option, not just termination.** "Relevant options" include the
  rights to establish, renew, increase, extend or resume insurance cover, and for those **the
  change in exercise rate is applied to the rate reflecting that the option is *not* exercised**
  [REG-R62]. The 80% **[std]** indexation take-up assumed above is therefore inside the lapse
  sub-module, not the mortality sub-module — implemented as a stress on the 20% decline rate.
- **The 70% mass-lapse limb never applies.** `3B6.6(1)` as corrected reaches **RAO Schedule 1 Part
  II class VII (pension fund management)** only; the class III reference published in PRA2024/13
  was declared an error on 20 December 2024 and deleted with effect from 31 December 2024
  [REG-R62][REG-R64][REG-R42]. This product is class I [REG-R14], so it takes the 40% limb.

**Market risk reaches this product mainly through one sub-module.** Interest rate up and down
(`3D5`/`3D6`) each require the curve to be rebuilt and **both the assets and the best estimate
revalued**; the requirement is the higher of the sum across currencies of the up requirements and
the sum of the down requirements, maximised across directions rather than per currency (`3D4.1`)
[REG-R62]. **On a negative best estimate the *up* scenario is normally the adverse one** — the
mirror image of an annuity writer, whose charge normally comes from the down shock — because a
higher discount rate shrinks the magnitude of a net-inflow present value and so reduces basic own
funds. *That directional statement is a derivation from the sign of the best estimate; no
retrieved source states it for term assurance.* It has a concrete consequence: the market
correlation coefficient `A` between interest rate and each of equity, property and spread is **0
where the interest-rate charge comes from the UP scenario and 0.5 in all other cases**
(`3.11A(3)`), so the model must **record which direction won** [REG-R62]. Equity and property do
not reach this product (no fund, no participating benefit); spread, concentration and currency
enter only through the assets held against the risk margin and SCR, not through the liability.
`3D25` — spread on a matching-adjustment portfolio — cannot arise, there being no MA permission
available (above).

**Counterparty default is this product's other real charge.** Reinsurance arrangements are
**type 1** exposures under `3E13`, a three-branch step function on the standard deviation of the
loss distribution against total loss-given-default [REG-R62]; for a heavily reinsured protection
book this is the dominant non-underwriting module, sitting alongside the TPFR 24.4 **50% LGD
floor** inside the best estimate [REG-R41].

**Operational risk collapses onto the premium leg.** `Op = max(Op_premiums; Op_provisions)` with
`Op_provisions = 0.45% × max(0; TP_life − TP_life-ul)` [REG-R62 `5.4`]. On a **negative** long-term
technical provision the `max(0; ·)` makes the provisions leg **nil**, so `Op` is
`Op_premiums = 4% × (Earn_life − Earn_life-ul)` plus the **growth surcharge** at the same rate on
the excess of the last 12 months' premium over **1.2 ×** the preceding 12 months' — which for a
fast-growing protection writer is the live term. There is no `0.25 × Exp_ul` leg, no unit-linked
business being written on this chassis. *The collapse of the provisions leg is a derivation from
the sign of the best estimate; the rule text is as cited.*

**Adjustments and what is never reached.** `Adj_TP` (loss-absorbing capacity of technical
provisions) is **zero**: it is capped at future discretionary benefits (`6.3(1)`), and a
non-participating term assurance has none — so `BSCR = nBSCR` and **one run suffices**, where a
with-profits product forces the two-run gross/net architecture [REG-R62]. `Adj_DT` (deferred
taxes) does apply, computed on an instantaneous loss of `BSCR + Adj_TP + SCR_operational`, with an
increase in deferred tax assets **not** utilisable now that the `6.5` transitional ended
**30 December 2025** [REG-R62]. Never reached by this product: the whole health module `3C`; the
ring-fenced-fund notional SCR `9.1` and the loss of diversification that comes with it (no RFF —
non-participating business in the shareholder fund); the MA-portfolio notional SCR; and
undertaking-specific parameters, which are available for **revision risk only** [REG-R65].

**Counting the runs.** Base valuation plus `3B1`, `3B4`, `3B6.2`, `3B6.3`, `3B6.6(2)`, `3B7`,
`3D5` and `3D6` — **eight** complete revaluations of the best estimate, with no gross/net second
pass and no per-fund repetition. *(Count derived from the incidence above; the shared file's
"Counting the runs" gives the general formula.)* The life simplifications at `7.8` (mortality),
`7.11` (expense), `7.12` (lapse) and `7.14` (life catastrophe, the exact factor equivalent of the
`3B7.1` shock, `Σ_i 0.0015 × CAR_i`) can replace some of them, but only after a documented `7.2`
proportionality assessment including **an evaluation of the error introduced**, and never where
that error could influence the user's decision-making unless the simplification produces a
**higher** SCR [REG-R62]. One product-specific consequence if `7.12` is used: `l_up` is the higher
of the average lapse rate on positive-surrender-strain policies and **67%**, and since every
policy here has positive surrender strain while its best estimate is negative, `l_up` is **67%**
against a [std] table that never exceeds 10% — the simplification is far more onerous than the
scenario it replaces *(derivation from `7.12(1)`, `7.12(3)` and this product's zero discontinuance
value)*. **There is no simplification for mass lapse** [REG-R62].

### Own funds, ring-fenced funds and the MCR

- **No ring fence, no estate, no surplus funds.** The composite is non-participating with no
  bonus, no discretionary benefit and no with-profits fund [S2][S6][S9], so it generates no
  restricted own funds, attracts no Own Funds **3L** deduction from the reconciliation reserve,
  produces no surplus funds under the Surplus Funds Part, and engages no part of the With-Profits
  Part [REG-R77][REG-R45]. Business is written in the shareholder fund.
- **The negative technical provision reaches Tier 1 unrestricted, undiminished.** Basic own funds
  are the excess of assets over liabilities less own shares plus subordinated liabilities (Own
  Funds 2.2), and the **reconciliation reserve** is a residual which "may be positive or negative"
  (3C.2, 3C.3) [REG-R77]. With no RFF and no MA portfolio there is nothing to strike it out, so
  for this product the whole of the negative best estimate flows into the reconciliation reserve
  and thence into Tier 1 unrestricted — which is precisely why the contract-boundary, expense and
  lapse assumptions above are capital assumptions, not merely valuation assumptions.
- **EPIFP is not required.** The Own Funds Part contains no "expected profit" requirement and
  PS3/24 records its removal from all Solvency UK reporting **including disclosure**
  [REG-R77][REG-R86]. This is the product whose expected profit included in future premiums is
  largest, so the absence matters: a UK model does **not** need the re-run-with-zero-future-
  premiums decomposition an EU model still needs.
- **MCR: the folk rule fails here.** `MCR_linear_l` includes `0.021 × TP_l4` (all other long-term
  obligations) and `0.0007 × CAR`, with **each term floored at zero separately** [REG-R78 3C.1].
  A negative technical provision therefore contributes `TP_l4 = 0` while the capital-at-risk term
  stays large, so "the MCR is 25% of the SCR" is not safe for pure protection — check which limb
  of the `min(max(MCR_linear, 0.25 × SCR), 0.45 × SCR)` corridor binds, against the absolute floor
  of **£3,500,000** for long-term insurance [REG-R78].
- **Capital at risk, twice over, on two different definitions.** MCR 3C.1(5) defines `CAR` per
  contract as `max(0, A − B)`, floored at zero **per contract**, where A is the amount the firm
  would currently pay on death or disability of the persons insured **plus** the expected present
  value of amounts not so covered payable on **immediate** death or disability, and B the best
  estimate of the corresponding obligations, net of reinsurance [REG-R78]. Two consequences here.
  First, **on the whole-contract reading of B** — the deduction is the contract's own best
  estimate, negative here because future premiums sit inside the boundary — the per-contract floor
  means `CAR` is roughly *benefit + |BEL|*, so it does not shrink as the block becomes more
  profitable. The rule does not say whether B is the whole-contract best estimate or the best
  estimate of the death and disability benefit outgo alone; on the latter reading `CAR` sits just
  *below* the sum assured instead, and the two readings move `MCR_linear` in opposite directions.
  **The fork is recorded, not resolved** *[std, reading of MCR 3C.1(5)]*; the worked example in
  `uk/regulatory/technical-notes.md`, "Worked example — one policy, carried through", adopts the
  benefit-obligation reading, so its `CAR` figure must not be mixed with one taken on this basis. Second, the **FIB shape needs both limbs**:
  limb (i) is the instalment payable immediately and limb (ii) the expected present value of the
  remaining `N − k` instalments — the model must carry a "sum payable on immediate death"
  attribute distinct from the projected benefit stream *(the two-limb reading for FIB is a
  derivation; the rule does not name family income benefit)*. And the reporting layer uses a
  **different** definition: IR.14.01 column C0190 requires capital at risk "as defined in Solvency
  Capital Requirement – Standard Formula **7.8 and 7.10**" [REG-R89], which is the simplification
  chapter, not MCR 3C.1(5). Carry both; do not let one overwrite the other.

### Statutory accounts and tax

- **In scope of FRS 103 without argument.** The contract transfers significant insurance risk and
  nothing else, so it is an insurance contract for UK GAAP purposes [REG-R99] — unlike a
  unit-linked bond, which frequently fails the test and falls out into FRS 102 Sections 11/12 and
  23. FRS 103 largely **grandfathers** existing practice: it names the modified statutory solvency
  basis as "the established accounting treatment for long-term insurance business" (¶3.11), permits
  continuation of practices that could not be newly introduced including **undiscounted** insurance
  liabilities (¶2.6), permits but does not require the elimination of excessive prudence (¶2.7),
  and applies a rebuttable presumption against introducing future investment margins (¶2.8)
  [REG-R99].
- **The floor that the prudential ledger does not have.** FRS 103 implementation guidance **IG2.41**
  — "**no policy may have an overall negative provision except as allowed by PRA rules, nor a
  provision less than any guaranteed surrender or transfer value**" — and the **liability adequacy
  test** at ¶¶2.14–2.18, which compares the carrying amount less related DAC against a
  current-estimate projection of all contractual cash flows *including embedded options and
  guarantees* and recognises **the entire deficiency** in profit or loss if inadequate
  [REG-R100][REG-R99]. This product has no surrender value, so only the **non-negative** limb of
  IG2.41 operates — and it operates hard, because the Solvency UK number is routinely negative.
  The applicability matrix bolds the UK GAAP floor row for term assurance precisely for that
  reason: **the same business carries a negative best estimate on the Solvency UK balance sheet
  and a floored provision in the statutory accounts** [REG-R100][REG-R41].
- **DAC is required, not prohibited — the U.S. story reversed.** Company law: SI 2008/410 Schedule
  3 **para 13** requires costs of acquiring insurance policies incurred in one financial year but
  relating to a subsequent year to be **deferred**, with DAC at assets item **G.II** and its
  movement at technical account item **8(b) change in deferred acquisition costs** [REG-R105]. The
  standard: FRS 103 **¶3.7** — acquisition costs "**shall be deferred**" — subject to three
  carve-outs (costs already recovered; insufficient net present value of margins; insufficiently
  certain future premiums or margins given expected discontinuance); **¶3.9** amortises over no
  longer than the recoverability period **and in a similar profile to those margins**, with **no
  amortisation basis prescribed** [REG-R99]. **¶3.10's prohibition on deferring acquisition costs
  applies to with-profits funds and does not reach this product**, which is non-participating
  [REG-R99][S2][S6][S9]. One configuration fork to make explicit: **note 17 to Schedule 3** removes
  DAC to the extent the long-term business provision (item C.2) already allows for the costs,
  explicitly or implicitly through anticipation of future income — which is how a zillmerised or
  gross-premium reserve absorbs acquisition costs *inside the liability* instead of showing an
  asset. **Make that a switch, not an accident** [REG-R105].
- **What that does to this file's worked example.** The year-1 net cash flow of **−£334.64**
  (£216.00 initial commission and £150.00 acquisition expense, plus £30.00 maintenance and £82.64
  of expected claims and claim expense, against £144.00 of premium) is a **cash-flow** fact, and it is also, essentially unchanged, a *Solvency UK* fact — acquisition
  expenses are projected outflows inside the best estimate (TPFR 16.1(4)) and the Valuation Part
  recognises no unamortised expense asset (Val 8.1) [REG-R41][REG-R39]. It is **not** a statutory
  accounts fact: in the accounts those costs are deferred subject to recoverability and released
  against margins, so **there is no U.S.-style first-year surplus strain in the UK accounts**. And
  on the prudential ledger the same policy is an *asset* at issue, because the acquisition expense
  sits inside a best estimate that is negative overall. Three ledgers, three signs, one set of cash
  flows. Any statement in this library that carries the U.S. "no DAC, first-year strain" framing
  into UK material is wrong [REG-R105][REG-R99].
- **IFRS 17, for an IFRS reporter: the general measurement model.** UK-adopted IFRS 17 applies to
  IFRS reporters [REG-R38], and the UKEB's expected UK mapping is **GMM for protection business and
  annuities, VFA for unit-linked and with-profits, PAA for short-term contracts** [REG-R106]. So
  this product is **GMM**. The **premium allocation approach** is optional and available only where
  it reasonably approximates the GMM **or** the coverage period of each contract in the group is
  **one year or less** [REG-R106]; the composite's terms run 1–50 years [S2][S4][S7], so PAA is
  reachable only for a one-year-term cell — hence the conditional mark. Under IFRS 17 there is no
  DAC asset either, **but for the opposite reason to the U.S.**: acquisition cash flows sit inside
  the fulfilment cash flows and **reduce the CSM at initial recognition**, emerging as reduced
  revenue over the coverage period [REG-R106]. Grouping is by portfolio × profitability bucket ×
  annual cohort, fixed at initial recognition and **never reassessed**; the CSM is released by
  **coverage units** reflecting the **quantity of benefits** and the expected coverage period —
  which for this product is *not* a constant across shapes: the level shape's quantity of benefits
  is flat, the decreasing shape's follows `B(k)`, and the FIB shape's follows the maximum remaining
  instalments *(the shape mapping is a derivation from the coverage-unit requirement and this
  product's mechanics, not a statement in [REG-R106])*. **IFRS 17 itself is paywalled and was never
  read** [REG-R107]; every paragraph reference in this library is one the UKEB quotes [REG-R106].
- **Tax: non-BLAGAB trade profit.** Protection business written from **1 January 2013** is excluded
  from BLAGAB and taxed on a trading basis like general insurance; policies written **before** that
  date continue to be taxed as BLAGAB unless the LAM14040 election has been made
  [REG-R17][REG-R18 LAM01080]. The composite is assembled from insurers' **current** retail
  products [S1]–[S9], so its tax basis is **non-BLAGAB trade profit** and **no I-E computation
  arises** — a per-product tax-basis flag, not a cash-flow driver. A pre-2013 back-book modelled on
  the same chassis is the exception and would need the I-E engine. Since **1 January 2013** trade
  profits are based on **accounting** profits (before that date, on the insurance regulatory
  returns) [REG-R18 LAM01100], so it is the accounts' DAC amortisation profile — not the cash
  outflow — that drives the timing of the acquisition-cost deduction for this product *(a
  derivation from LAM01100 read with FRS 103 ¶¶3.7–3.9; neither source states it for term
  assurance)*. The FA 2012 s.79 **seven-year acquisition-expense spread** is a BLAGAB "E" mechanic
  and does not touch a non-BLAGAB trade computation; it is in any case repealed for accounting
  periods beginning on or after **1 January 2023** [REG-R18][REG-R109].
- **Policyholder tax is not a behavioural driver here.** With no surrender value and no investment
  element [S6][R8] there are no chargeable-event gains to time, so the ITTOIA Part 4 Chapter 9 /
  IPTM machinery that shapes lapse behaviour on bonds and participating contracts is inert
  [REG-R15][REG-R16]. The product spec's statements on IHT and trusts [S7] and on qualifying-policy
  conditions [S1] stand unchanged there and are not repeated here.
- **Deferred tax needs three numbers, and distributable profits come off the prudential balance
  sheet.** Valuation 11 measures deferred tax on **all** assets and liabilities **including
  technical provisions**, as the difference between the Solvency UK value and the tax value
  [REG-R39]; FRS 102 Section 29 measures it on timing differences [REG-R102]; the tax computation
  is a third number. For distributions, CA 2006 **s.833A** replaces the realised-profits test for a
  Solvency-II-authorised long-term insurer with **A − L − D** on the *prudential* balance sheet,
  capped by the accounts' accumulated profits [REG-R104]. The two product-specific deductions in
  that formula — the **ring-fenced fund** surplus and the **matching-adjustment portfolio** surplus
  — are **both nil** for this product, so a pure protection writer's distributable-earnings pattern
  is a projection of the Solvency UK balance sheet with the accounts as a ceiling and no deductions
  in between. That is a real simplification relative to a with-profits or annuity writer, and it is
  the reason the SCR and own-funds assumptions above are also the dividend assumptions.

### Traps peculiar to this product

1. **Do not import the U.S. acquisition-cost story.** SI 2008/410 Sch 3 para 13 **requires** DAC and
   FRS 103 ¶3.7 **requires** deferral subject to recoverability [REG-R105][REG-R99]. The U.S.
   "expensed as incurred, no DAC asset, first-year surplus strain" narrative is *reversed* in the UK
   accounts, and the year-1 cash strain in the worked example above must not be read across to them.
2. **Lapse direction is a computed filter, not a product attribute.** Run the `3B6.2`/`3B6.3`
   filters — or the `7.12(3)` surrender-strain diagnostic — per policy at every valuation
   [REG-R62]. The answer flips as a policy matures, and hard-coding "protection ⇒ lapse up" fails
   on exactly the cells where it matters.
3. **Two capital-at-risk definitions.** MCR 3C.1(5) for the MCR [REG-R78]; `SCR-SF 7.8`/`7.10` for
   IR.14.01 column C0190 [REG-R89]. They are not the same quantity and the model must emit both.
4. **Never floor the best estimate inside the projection.** The Solvency UK ledger has no floor
   [REG-R41][REG-R115]; the accounts floor is IG2.41 and belongs downstream [REG-R100]. A model
   that clamps at zero destroys the own-funds number and the s.833A distributable-profits number
   together.
5. **Commission is a best-estimate cash flow.** TPFR 13.1(5) makes payments between the firm and
   intermediaries an in-scope stream [REG-R41]; with ~96% of UK protection commission paid upfront
   and clawback periods of 2–4 years [R9], modelling it as an expense loading rather than a cash
   flow both misstates the BEL and loses the clawback asymmetry.
6. **Two expense bases, unreconciled in the sources.** Going-concern with new business assumed in
   the best estimate (TPFR 16.4) [REG-R41]; no new obligations in the risk-margin reference
   undertaking (TP 4B.1(5)) [REG-R1]. Both are correct as printed and **no retrieved source
   explains how to set the reference undertaking's expenses given the tension**.
7. **The reference mortality basis could not be filed.** IR.12.04 column C0080 requires a **named**
   table, with "adjusted" appended where the percentage varies by age and the CMI projection
   parameterisation given in CMI notation [REG-R89]; the current UK protection tables and the CMI
   Mortality Projections Model are available only to CMI authorised users [R11], so this library's
   scaled "00" Series proxy **[std]** is an honest stand-in and not a production basis.
8. **Terminal illness and family income benefit are the two places the sources run out.** TI raises
   the TPFR 26.7 unbundling question, recorded and not resolved [REG-R41][REG-R42]; FIB has no PRA
   product code in the retrieved appendix [REG-R89] and is not named in any stress or MCR rule this
   library retrieved, so every FIB-specific statement above is flagged as a derivation.
9. **No discount curve exists anywhere in this library.** The four monthly PRA technical-information
   spreadsheets were not opened — the retrieval helper handles HTML and PDF only — so **no
   risk-free curve, ultimate forward rate, fundamental spread, volatility adjustment or symmetric
   adjustment value appears anywhere in `uk/`** [REG-R54]. A best estimate cannot be discounted from
   this library's contents alone; the curve is an input, and the PRA publishes it — the firm has no
   discretion over it for a PRA relevant currency [REG-R44][REG-R55]. Two related gaps, kept
   distinct: the **Annexes to the SCR – Standard Formula Part were not retrieved** [REG-R73],
   taking the health catastrophe inputs and the **numbered** line-of-business list used by
   `3.10B` — neither of which this product needs; separately, **TPFR Annex 1 was retrieved but
   names no products** [REG-R41], which is why the LoB 32 assignment above is an inference rather
   than a quotation.

---

## Valuation and reserve pointers

The valuation layers, templates and capital components for this product are in
**Statutory accounting and capital** above; this section stays a pointer list. This
library projects gross best-estimate liability cash flows; the layers that consume
them are cited, not reproduced.

- **Solvency UK best estimate.** `BEL = Σ_t v(t) × [outgo(t) − income(t)]` over the
  recursion above: the probability-weighted average of future cash-flows discounted
  at the relevant risk-free term structure, on realistic assumptions, gross of
  reinsurance with recoverables separate [R1]; cash-flow categories per the PRA
  cash-flows rule — benefits, expenses, premiums, intermediary payments,
  policyholder-charged taxation [R2]; contract boundary = full term for guaranteed
  premiums [R3]. The BEL is commonly **negative** at issue and must not be floored —
  see **Technical provisions** above, where that is now sourced rather than derived.
  Method and notation: `uk/regulatory/technical-notes.md`, "The best estimate
  liability".
- **Risk margin.** Technical provisions = best estimate + risk margin [REG-R1];
  cost-of-capital method at 4% with life risk-tapering factor λ = 0.9, floor 0.25
  [REG-R4]. Requires an SCR run-off projection: formula, reference-undertaking
  configuration and a **three-year term assurance worked example** are in
  `uk/regulatory/technical-notes.md`, "The risk margin".
- **SCR and MCR.** Module incidence for this product is in **SCR — the modules that
  bite** and **Own funds, ring-fenced funds and the MCR** above; the module tree,
  correlation matrices, stress sizes and aggregation arithmetic are in
  `uk/regulatory/technical-notes.md`, "The standard formula SCR" and "Own funds, the
  reconciliation reserve and the minimum capital requirement".
- **Regime.** PS15/24 completed the restatement of Solvency II assimilated law into
  PRA rules from end-2024 ("Solvency UK") [R5]. Framework overview:
  `uk/regulatory/statutory-accounting-and-capital.md`.
- **Statutory accounts and tax.** FRS 102 + FRS 103, or UK-adopted IFRS 17 — adopted
  16 May 2022, effective 1 January 2023, applying to IFRS reporters [REG-R38]. The
  fulfilment-cash-flow engine is the same expected-cash-flow projection; grouping,
  CSM and risk-adjustment mechanics are carried in the framework files from the UKEB
  assessment [REG-R106] (**IFRS 17 itself is paywalled and was never read**
  [REG-R107], so every paragraph reference is one the UKEB quotes). Measurement
  model, DAC and tax basis for this product: **Statutory accounts and tax** above;
  roll-forward mechanics: `uk/regulatory/technical-notes.md`, "Statutory accounts and
  tax roll-forward".
- **Professional standards.** Technical actuarial work using this model in scope of
  UK regulation falls under TAS 100 v2.0 [R15] and TAS 200 v2.0 [R16].

---

## Key sensitivities and model risks

Dominant assumptions, in rough order for a protection block:

1. **Mortality basis risk.** The reference basis is a [std] proxy (scaled "00"
   Series) because the current 16-Series tables are subscriber-only [R11][R13];
   the proxy scaling factor (75% [std]) is the single largest lever on claims.
   Production users should substitute subscriber tables (TMNL16/TFNL16 [R12][R10])
   and a CMI projections overlay [R14][REG-R30].
2. **Early-duration lapse.** With ~96% of commission upfront and 2–4 year clawback
   [R9], year-1–4 lapse rates drive new-business strain recovery; the clawback
   module changes the sign of the sensitivity inside the clawback window.
3. **Selective lapsation.** Guaranteed premiums plus healthy-life rebroking imply
   persisting lives are progressively impaired; the λ loading materially moves
   late-duration claims on long terms.
4. **Expense inflation on small premiums.** Premiums as low as £5/month [S5] against
   £30/year maintenance make per-policy expense inflation a solvency-relevant
   assumption for small-sum-assured blocks.
5. **Shape-specific risks.** Decreasing: the schedule rate `j` is contractual, so
   the risk is *specification* error, not experience (mis-implementing the
   amortization or the monthly convention); FIB: the annuity-certain run-off means
   claim outgo persists up to `n − 1` years after death — omitting the in-payment
   ledger understates liabilities.
6. **Indexation take-up.** The ×1.5 premium factor [S1][S2][S6] makes accepted
   increases premium-margin-accretive if mortality is proportional to cover;
   selective acceptance (impaired lives accept, healthy decline) reverses the sign
   **[std]** concern; no public take-up data exists in the fetched sources.

Known modeling pitfalls:

- **TI is not an extra benefit.** Death and terminal illness are one decrement and
  one payment [S1][S6][S8]; adding a separate TI decrement double-counts claims.
  The 16-Series mortality tables already include terminal illness [R10].
- **FIB instalments are certain, not contingent.** Do not decrement the in-payment
  income by mortality or lapse; only *new* claims depend on `l(t)` [S6][S8].
- **Decreasing-schedule conventions.** `j_m = (1+j)^(1/12) − 1` **[std]** vs a
  nominal `j/12` convention changes `B(k)` slightly; state the convention and use
  the `B(60) = £134,588` anchor to validate implementations.
- **Annual-grid biases.** Mid-year benefit for the decreasing shape and
  annual-in-advance premiums are offsetting small biases; the monthly grid is the
  arbiter. Do not apply both the mid-year claim timing and a separate half-year
  premium adjustment — pick one convention.
- **Lapse pays nothing.** There is no surrender value [S6][R8]; a lapse row in the
  cash-flow output must be zero-valued (it affects only `l(t)`), unlike US models
  with CSV outflows.
- **No tail states.** Terminate everything at month N: no renewal, no conversion,
  no extended coverage [S1][S2][S6][S8][R8]. Importing a US-style post-level-term
  tail materially misstates UK term liabilities.
- **Joint life first death.** Model as a single joint decrement
  `q_joint = 1 − (1−q_1)(1−q_2)` on one policy **[std]**; the policy pays once and
  ends [S1][S6]. Separation/replacement options create new policies and are out of
  scope.
- **Boundary discipline.** All guaranteed premiums are inside the contract boundary
  [R3]; truncating premium income at an assumed "repricing" point (a Solvency II
  habit from reviewable business) is wrong for this product.
