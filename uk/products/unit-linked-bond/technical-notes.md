# Unit-Linked Investment Bond — Liability Cash Flow Model: Technical Notes (United Kingdom)

**Status:** Draft, 2026-08-03 (all cited sources accessed 2026-08-03; see `sources.md`).

**Scope note.** These notes specify a reference liability cash-flow projection model for
the standardized composite product defined in `product-spec.md` (same directory). This is
not any single insurer's product. [S#]/[R#] tags refer to the source list in
`uk/_research/unit-linked-bond.md` (carried into `sources.md` here); [REG-R#] tags refer
to the cross-product reference library
`uk/references/regulatory-and-actuarial-references.md` (its own R-numbering; research
provenance for R1–R38 in `uk/_research/regulatory-actuarial.md`, and for R39–R120 in the six
research files listed in `uk/regulatory/statutory-accounting-and-capital.md`). **[std]** marks standardizations
introduced for the reference implementation; [unverified] marks claims not confirmed
against a retrieved document. Parameter values are identical to those in
`product-spec.md`; the implementation anchor for mechanics is the Prudential Investment
Plan KFD + Policy Provisions pair [S1][S2].

---

## Model scope and conventions

- **Purpose.** Project gross liability cash flows for a single-policy model point of a
  clean-charge onshore unit-linked bond, decomposed in the classic UK way into the
  **unit fund** (the bid value of units, matched by the linked assets) and the
  **non-unit ("sterling") cash flows** accruing to the insurer: charges collected and
  fund-based margins, less expenses and death strain. This decomposition is standard
  UK actuarial practice but is tagged [unverified] as terminology — the IFoA archive
  papers evidencing the "sterling reserve" usage could not be text-extracted [R9];
  the rule-level anchor is the Solvency UK requirement that the best estimate reflect
  *all* cash in- and out-flows [R5 TP 3.2] applied to the product cash flows in
  [S1]–[S5]. Reserves are not computed (see Valuation and reserve pointers).
- **Projection frequency.** Monthly **[std]**. The contract accrues the AMC daily
  through the unit price [S2 §5.1.1] and prices funds daily/at least monthly
  [S2 §3.2][S3 Part E]; the model discretizes to monthly steps with all
  intra-month flows at the conventions below.
- **Timing conventions [std].** Fund growth, tax provision and fund-based charges
  accrue over the month; withdrawals, adviser charges and rider charges are unit
  cancellations at end of month (EOM); decrements (death, surrender) are EOM events
  after cancellations. Settlement frictions (12:00 cut-offs, 2-working-day large
  deals, 28-day PruFund waits, deferral powers [S2 §4, §8][S5 Q9]) are ignored.
- **Age basis.** Age last birthday (ALB) **[std]**, chosen to index directly into
  single-year-of-age qx vectors of the ONS national life tables used as the [std]
  mortality proxy [REG-R32]. (Contractual age limits are quoted "next birthday" in
  the anchor documents [S1]; the difference is immaterial to a product with a 0.1%
  death strain.)
- **Currency.** GBP. Intermediate values carried at full precision; cash flows
  reported to pence **[std]**.
- **Model points.** Single-policy model points projected on an expected
  (probability-weighted) basis: survivorship factors multiply per-policy cash flows.
  A "policy" here is the whole bond of 100 identical segments **[std]** (spec
  footnote 3); per-segment values are the bond values ÷ 100 [S1][S2 §2.4]. No
  aggregation logic is specified.
- **Top-ups.** Excluded from the base projection; a top-up is a new model point with
  its own premium, allowance clock and segments **[std]** (spec footnote 4)
  [R2 per-premium allowance arithmetic].

---

## Model point attributes

| Attribute | Type | Example (anchor cell) |
|---|---|---|
| `issue_age` | int (ALB) | 65 **[std]** |
| `sex` | enum {M, F} | M **[std]** |
| `lives` | enum {single} (joint last-death out of scope, spec footnote 1) | single |
| `premium` | currency (single premium, net of set-up adviser charge [S2 §1, §12.2]) | 100,000 **[std]** |
| `n_segments` | int | 100 **[std]** |
| `db_uplift` | factor `u` | 1.001 [S1][S2]; choice **[std]** |
| `amc_rate` | annual rate `c` | 0.0100 **[std]** |
| `further_costs_rate` | annual rate `f` | 0.0010 **[std]** |
| `tax_provision_rate` | rate `t_pf` | 0.20 **[std]** proxy [R6] |
| `wd_pattern` | enum {none, allowance_5pct, custom} | allowance_5pct **[std]** |
| `oac_rate` | annual rate on unit value (ongoing adviser charge) | 0 (module value 0.005 [S1][S2 §7.1 example]) |
| `gmdb_flag` | bool (return-of-premium rider [S1][S2 §5.2, §10][S5]) | false **[std]** |
| `uf_initial` | currency (premium at issue; >0 for in-force cells) | 100,000 |
| `issue_date` / `policy_month_offset` | date / int | month 1 |

---

## State variables

| Variable | Description | Updated |
|---|---|---|
| `UF(t)` | Unit fund = bid value of units at end of month t | monthly recursion |
| `l(t)` | In-force probability at end of month t; l(0) = 1 | monthly decrements |
| `y` | Policy year = ceil(t/12); insurance year for allowance tracking [R2] | monthly |
| `CumWD(n)` | Cumulative withdrawals + ongoing/ad hoc adviser charges to end of insurance year n (allowance-relevant [S2 §12.1.1][S4][S5 Q15]) | on withdrawal/charge |
| `CumAllow(n)` | Cumulative allowable element = premium × min(n, 20) × 5% [R2] | yearly |
| `ExcessGain(n)` | Excess-event gain at insurance-year end (policyholder-side flag, no insurer cash flow) [R1 s498/s507][R2] | yearly |
| `G(t)` | GMDB guaranteed amount = premium − withdrawals − ongoing/ad hoc adviser charges (if `gmdb_flag`) [S2 §10] | on events |
| `E(t)` | Maintenance expense in month t | monthly |

---

## Assumption inputs

Three classes are distinguished explicitly.

### (a) Contractual / guaranteed elements (cited)

In a clean-charge unit-linked bond the guaranteed layer is thin — that is the point
of the design:

| Input | Value | Basis |
|---|---|---|
| Death benefit | `u × UF`, u = 1.001 (sum assured = 100.1% of bid value of units) | [S1][S2]; u choice **[std]** (spec footnote 6) |
| Surrender value | `UF` (bid value of units; no penalty) | [S4]; composite scope **[std]** (spec footnote 13) |
| Withdrawal machinery | Regular/partial/segment surrender; 12-month regular cap = max(7.5% of plan value, 7.5% of total paid in) incl. ongoing adviser charges | [S1][S2 §7.1, §7] |
| Charge basis | AMC accrues daily through the unit price; adviser/rider charges by unit cancellation | [S2 §5.1.1, §12] |
| Segmentation | 100 identical policies; premium and units divided equally | count **[std]**; mechanics [S1][S2 §2.4] |
| Liability cap | Benefits derived from fund assets only; no make-whole on external default | [S2 §3.1.9][S4] |

### (b) Insurer-discretionary current elements (snapshot)

All revisable by the insurer (AMC increase provisions are documented on the legacy
booklet [S3 Part D]); the model holds the snapshot level:

| Input | Snapshot value | Basis |
|---|---|---|
| AMC `c` | 1.00% p.a. | **[std]** — per-fund AMC rate cards not fetched (research gap 5); only the discount tier table is public [S1] |
| Further costs `f` | 0.10% p.a. (fund-borne, not insurer income) | existence [S1][S2 §3.1.7]; level **[std]** |
| Fund-size discount | Off (level net AMC assumed) | tiers [S1][S2 §5.1.4]; scope **[std]** |
| Life-fund tax pass-through `t_pf` | 20% of gross fund return, in-price, neutral to insurer | mechanism [S2 §3.2.1][S4][S5 Q15]; rate proxy **[std]** of the policyholder rate [R6] |
| GMDB mortality-factor scale | = monthly mortality rate from the class-(c) basis at attained age (cost-of-insurance style), applied to max(0, G − u×UF) | design [S2 §5.2, §10]; scale **[std]** — factors not published |
| MVR / bonus rates | Not applicable — with-profits and PruFund funds out of scope; see `uk/products/with-profits/` | [S2 §3.3][S3] |

The `t_pf` proxy deliberately ignores I-E timing detail: actual pass-through
distinguishes income (as received), realised gains (next charge date), an annual
deemed-disposal charge, and full-surrender settlement [S5 Q15][S4], and the company's
I-E position includes an expense offset and minimum profits test [R6]. The base model
treats collected tax as exactly offsetting tax payable (zero insurer margin impact)
**[std]**.

### (c) Behavioral / experience assumptions (modeler's view)

| Input | Recommended public basis | Basis tags |
|---|---|---|
| Best-estimate mortality | 80% × ONS national life tables qx (single year of age, sex-distinct) **[std]** proxy | [REG-R32]; factor **[std]** |
| Mortality improvement | None in base **[std]**; production overlay "CMI_20xx with long-term rate p% **[std]**" | [REG-R30] |
| Base surrender (full) | [std] table below | **[std]**; design holding period [S1][S4][S5] |
| Withdrawal take-up | anchor cell: 5% of premium p.a., monthly | **[std]** (spec footnote 14) [R2][S1][S4][S5] |
| Acquisition expense | £300 per policy at issue | **[std]** |
| Maintenance expense | £60 per policy p.a., inflating 2.5% p.a. | **[std]** |
| Gross fund return scenario `g` | 5.0% p.a. (deterministic base) | **[std]** |

**Honesty note on the mortality basis.** The CMI's current assured-lives tables and
Projections Model are restricted to Authorised Users (subscribers); older
publications are free but current qx cannot be redistributed [R8][REG-R30]. The
canonical teaching tables (AM92/AF92) show the *shape* an assured-lives basis takes
[REG-R24], and the ONS national life tables are the only fully redistributable UK
mortality source (Open Government Licence; qx by single year of age) [REG-R32] —
hence the [std] proxy above, with the caveat that population mortality is heavier
than insured-lives experience [REG-R32] (the 80% factor is a crude allowance,
**[std]**). Specific CMI assured-lives table names for this product could not be
confirmed from the fetched CMI page and remain [unverified] (research gap 8) [R8].
Mortality is nearly irrelevant to this product — the net amount at risk is 0.1% of
the unit fund in the composite (0.1%–1% across insurers [S1][S2][S3][S4][S5]) —
unless the GMDB rider is enabled.

Reference base surrender table **[std]** (annual rates; to be replaced by portfolio
experience; shape rationale: the product is designed to be held 5–10 years or more
[S1][S4][S5], so surrenders are low early, rise as the advised holding period
completes, and settle at a high ultimate level):

| Policy year | 1 | 2 | 3–5 | 6–10 | 11+ |
|---|---|---|---|---|---|
| Annual full-surrender rate `w_base` | 2% | 3% | 5% | 8% | 10% |

---

## Cash flow components and recursions

### Notation (defined once, used throughout)

| Symbol | Meaning |
|---|---|
| t | policy month, t = 1, 2, …; y = ceil(t/12); a = attained age (ALB) = issue_age + y − 1 |
| `P` | single premium (100,000) |
| `UF(t)` | unit fund at end of month t; UF(0) = P |
| `g` | annual gross fund return (0.05); `g_m` = (1+g)^(1/12) − 1 = 0.0040741 (derived) |
| `t_pf` | tax-provision rate (0.20) **[std]** |
| `c`, `f` | AMC (0.0100) and further costs (0.0010), annual; `c_m` = c/12 = 0.0008333, `f_m` = f/12 = 0.0000833 **[std 1/12 accrual convention]** |
| `u` | death-benefit uplift factor (1.001) |
| `W(t)` | regular + one-off withdrawals cancelled at EOM of month t (anchor: 5%×P/12 = 416.67) |
| `AC(t)` | ongoing/ad hoc adviser charges cancelled at EOM (0 in anchor cell) |
| `GC(t)` | GMDB rider charge (0 unless `gmdb_flag`) |
| `TX(t)` | tax provision deducted in month t; `AMC$(t)`, `FC$(t)` monetary AMC/further costs |
| `DS(t)` | death strain per death in month t |
| `q_m(t)` | monthly mortality rate = 1 − (1 − q_a)^(1/12) from the class-(c) basis; `w_m(t)` monthly surrender rate = 1 − (1 − w_ann)^(1/12) |
| `l(t)` | in-force probability at end of month t; l(0) = 1 |
| `E(t)` | maintenance expense = 60/12 × 1.025^(y−1) **[std]** |

Dimension check: `g_m`, `c_m`, `f_m`, `t_pf` are dimensionless per-month rates or
fractions; every product with `UF` is in GBP; `q_m × DS` is GBP per policy-month.
`W`, `AC`, `GC`, `TX`, `AMC$`, `FC$`, `E` are GBP per month.

### Monthly processing order **[std]**

For month t, per policy in force at t−1:

1. Update y, a, E(t).
2. **Fund growth and tax provision** (within unit price [S2 §3.2.1][S4][S5 Q15]):
   `G$(t) = g_m × UF(t−1)`;  `TX(t) = t_pf × G$(t)`;
   `UF_g(t) = UF(t−1) + G$(t) − TX(t) = UF(t−1) × (1 + g_m(1 − t_pf))`.
3. **Fund-based charges** (AMC accrues via price [S2 §5.1.1]; further costs
   fund-borne [S2 §3.1.7]):
   `AMC$(t) = c_m × UF_g(t)`;  `FC$(t) = f_m × UF_g(t)`;
   `UF'(t) = UF_g(t) × (1 − c_m − f_m)`.
4. **Unit cancellations (EOM):** withdrawals, adviser charges, rider charge:
   `GC(t) = q_m(t) × max(0, G(t) − u × UF'(t))` if `gmdb_flag` else 0
   (design [S2 §5.2, §10]; scale **[std]**);
   `UF(t) = UF'(t) − W(t) − AC(t) − GC(t)`.
   Enforce the product cap: rolling-12-month W + AC ≤ max(0.075 × UF, 0.075 × P)
   [S1][S2 §7.1].
5. **Death strain per death:**
   `DS(t) = (u − 1) × UF(t) + max(0, G(t) − u × UF(t)) × 1{gmdb_flag}`
   — the sum assured is u × UF funded by cancelling the whole unit fund, so the
   non-unit cost is the 0.1% uplift [S1][S2] plus any GMDB in-the-money amount
   [S2 §10][S5].
6. **Decrements (EOM), deaths before surrenders [std]:**
   `l(t) = l(t−1) × (1 − q_m(t)) × (1 − w_m(t))`.
   Surrender pays `UF(t)` by cancelling all units — no non-unit cash flow (clean
   design [S4]; spec footnote 13) — but extinguishes all future margins.
7. **Allowance tracker (insurance-year end, policyholder side only):**
   `CumAllow(n) = P × min(n, 20) × 0.05` [R2];
   `ExcessGain(n) = max(0, CumWD(n) − CumAllow(n) − Σ prior excess gains)`
   [R1 s498/s507][R2]. Generates **no insurer cash flow**; feeds behavior only.
   Chargeable events on death/full surrender follow s484/s491 [R1] and are likewise
   policyholder-side (the insurer issues certificates [S5 Q15]).

The core unit-fund recursion (anchor cell: AC = GC = 0):

    UF(t) = UF(t−1) × (1 + g_m(1 − t_pf)) × (1 − c_m − f_m) − W(t)

### Non-unit (insurer) cash flow extraction

Per policy in force at t−1, before survivorship weighting:

| Cash flow | Formula | Sign |
|---|---|---|
| AMC margin | AMC$(t) = c_m × UF_g(t) | + |
| GMDB rider charge | GC(t) (0 in base) | + |
| Set-up adviser charge / commission | 0 — post-RDR adviser charges are pass-throughs facilitated by unit cancellation [S1][S2 §12][S4] | 0 |
| Maintenance expense | E(t) | − |
| Acquisition expense (t = 0) | 300 **[std]** | − |
| Death strain (per death) | DS(t) | − |
| Further costs FC$(t) | pass-through to fund costs — excluded from insurer margin **[std]** | 0 |
| Tax provision TX(t) | pass-through to corporation tax — neutral **[std]** (class (b) note) [R6] | 0 |
| Surrender / withdrawal payments | funded by unit cancellation — no non-unit flow (clean design) [S4] | 0 |

Aggregate expected cash flows multiply each row by the in-force factor: AMC, GC and
expenses by l(t−1); death strain by l(t−1) × q_m(t); nothing by surrenders (their
non-unit flow is zero) **[std timing]**. The expected net non-unit cash flow:

    NUCF(t) = l(t−1) × [ AMC$(t) + GC(t) − E(t) − q_m(t) × DS(t) ]  −  300 × 1{t=0}

Because AMC$(t) ≈ c_m × UF and DS(t) ≈ 0.001 × UF, the insurer's result is a
fund-based margin stream: proportional to the unit fund and to persistency, with
mortality contributing only ~0.001 × q of the fund per year. Lapse/withdrawal
behavior, not mortality, dominates value. Future margins typically exceed future
costs, so the non-unit best estimate is commonly negative (an asset-like offset to
the unit reserve) [unverified as standard-practice terminology — see scope note; the
rule anchor is R5 TP 3.2].

---

## Policyholder behavior modeling

All dynamic formulas are **[std]** reference constructions; no public UK bond
persistency study was fetched (calibration is portfolio-specific).

- **Withdrawal take-up [std].** `wd_pattern = allowance_5pct`: W(t) = 0.05 × P / 12
  every month. Rationale: the 5%/20-year tax-deferred allowance [R2] is the pattern
  every fetched KFD leads with [S1][S4][S5], it sits inside the 7.5% product cap
  [S2 §7.1], and adviser charges consume the same allowance [S2 §12.1.1][S5 Q15] —
  so rational take-up gravitates to 5% inclusive of charges. Sensitivity: `none`
  (accumulation cell) and `custom`.
- **Base surrender [std].** `w_base(y)` per the class-(c) table, converted monthly.
- **Dynamic surrender multiplier — market performance [std].**
  `M_perf(t) = min(2.0, 1 + 2.0 × max(0, g_ref − R_12m(t)))`,
  where `R_12m` is the trailing 12-month gross fund return and `g_ref` = g (5%).
  Poor recent performance raises surrender; base deterministic run has
  R_12m = g_ref so M_perf = 1.
- **Allowance-exhaustion step [std].**
  `M_allow(y) = 1.5 for y ≥ 21, else 1.0`. After 20 insurance years the cumulative
  allowance is fully drawn under the anchor withdrawal pattern [R2]; continued
  withdrawals then generate immediate excess-event gains [R1 s507], pushing
  policyholders toward full surrender (or advice-driven restructuring).
- **Total surrender.** `w_ann(y,t) = min(0.35, w_base(y) × M_perf(t) × M_allow(y))`
  **[std cap]**.
- **Segment vs part-surrender election.** Whether a policyholder cashes whole
  segments or part-surrenders across all segments changes their tax [S1][S4]
  [S5 Q12][R1 s484/s498], not the insurer's cash flow (both cancel the same unit
  value) — carried as a model note only **[std]**.
- **No paid-up state.** Single-premium product; no premium obligation exists
  [unverified as an explicit statement; consistent with S1–S5].

---

## Worked example

Anchor cell: male 65, P = £100,000, 100 segments (£1,000 each), u = 1.001,
c = 1.00%, f = 0.10%, t_pf = 20%, g = 5.0% p.a., W = £416.67/month (5% of premium
p.a. [R2 allowance]), AC = GC = 0; all parameters **[std]** per the tables above.
Derived monthly rates: g_m = 0.0040741; g_m(1−t_pf) = 0.0032593; c_m = 0.0008333;
f_m = 0.0000833. Placeholder mortality for the year: q_a = 1.0% **[std order-of-
magnitude placeholder consistent with the class-(c) proxy]**, q_m = 0.000837.
Figures in GBP, displayed to pence, full precision carried.

| t | UF(t−1) | Gross return G$ | Tax TX | AMC$ | FC$ | W | UF(t) |
|---|---|---|---|---|---|---|---|
| 1 | 100,000.00 | 407.41 | 81.48 | 83.60 | 8.36 | 416.67 | 99,817.30 |
| 2 | 99,817.30 | 406.67 | 81.33 | 83.45 | 8.35 | 416.67 | 99,634.17 |
| 3 | 99,634.17 | 405.92 | 81.18 | 83.30 | 8.33 | 416.67 | 99,450.61 |
| … | … | … | … | … | … | … | … |
| 12 | 97,966.60 | 399.13 | 79.83 | 81.90 | 8.19 | 416.67 | 97,779.14 |
| **Yr 1** | — | **4,839.44** | **967.89** | **993.10** | **99.31** | **5,000.00** | **97,779.14** |

Trace, month 1: G$ = 0.0040741 × 100,000 = 407.41; TX = 0.20 × 407.41 = 81.48;
UF_g = 100,325.93; AMC$ = 0.0008333 × 100,325.93 = 83.60; FC$ = 8.36;
UF' = 100,233.96; UF(1) = 100,233.96 − 416.67 = 99,817.30.
Reconciliation, year 1: 100,000 + 4,839.44 − 967.89 − 993.10 − 99.31 − 5,000.00
= 97,779.14. ✓ Per segment: 977.79.

Insurer-side extraction, year 1 (per policy, survivorship factors ≈ 1 at this q/w):

- AMC margin collected: **+993.10**
- Maintenance expense (£60, year 1): **−60.00**
- Expected death strain: Σ q_m × 0.001 × UF(t) = **−0.99**
  (per actual death at month 12 the sum assured would be 1.001 × 97,779.14
  = 97,876.92, of which 97,779.14 is funded by cancelling units — strain 97.78)
- Tax provision (967.89) and further costs (99.31): pass-throughs, nil margin **[std]**
- **Net non-unit cash flow ≈ +932.11** (acquisition expense −300 falls at issue)

Policyholder-side check (no insurer cash flow): year-1 withdrawals 5,000 =
allowable element 100,000 × 1/20 = 5,000 [R2] — no excess event; unused allowance
carried forward is nil, and the 7.5% product cap (7,500 on paid-in) is not breached
[S2 §7.1].

---

## Statutory accounting and capital

Framework and the shared model-output contract are in
`uk/regulatory/statutory-accounting-and-capital.md` (what the items are) and
`uk/regulatory/technical-notes.md` (how to compute them); this section states only what is
specific to the unit-linked investment bond. Note the terminology the UK forces: there is no
"statutory accounting" in the U.S. sense — the three measurements are the **Solvency UK
regulatory balance sheet** (PRA Rulebook), the **statutory accounts** (FRS 102 + FRS 103, or
UK-adopted IFRS 17), and **tax**, computed from the accounts with the FA 2012 overlay. [REG-R#]
resolves against the shared UK numbering in
`uk/references/regulatory-and-actuarial-references.md`, which now runs **R1–R120**, with
**R50–R52, R74–R76 and R121–R133 unused by design** (parallel block allocation — an unused
number is not a missing entry). Product-local [S#] and [R#] tags resolve against `sources.md`
in this directory, unchanged.

### Contract classification and reporting

- **Legal class is settled and constant.** The bond is a contract of long-term insurance
  [S2 §18.5] in **RAO Schedule 1 Part II class III, "Linked long term"** [REG-R14][R4]. That
  class membership is not decorative: it is the hinge on which the mass-lapse question below
  turns. The capital-redemption variant noted in `product-spec.md` (Riders, out of scope) would
  be **class VI** instead [REG-R14], but no fetched document supplies its product terms
  [unverified].
- **Solvency UK line of business: Annex 1 LoB 31, index-linked and unit-linked insurance**
  [REG-R41 TPFR Annex 1]. Assignment "must reflect the **nature of the risks**… The **legal
  form** of the obligation **is not necessarily determinative**" (TPFR 26.2) — the technical
  basis decides, not the product label. **The mapping of this library's seven products onto
  Annex 1 is the drafter's inference from TPFR 26.2/26.3 and the Annex 1 definitions; Annex 1
  names no products** [REG-R41], and that flag is carried forward here rather than upgraded.
- **PRA product code 112 — "single premium bond UL"** (113 if index-linked, 114 if non-profit)
  [REG-R89]. Two conventions in the IR.14.01 appendix decide this and are easy to get wrong.
  "Single premium bond" **includes 'investment bond'**; and the whole-of-life and endowment
  codes **exclude single premium bonds "which are technically whole of life"** [REG-R89] — so
  this contract, which *is* a whole-of-life assurance with no maturity date [S1][S2][S4][S5],
  nevertheless reports under 112 and never under a whole-of-life code. "UL" is recorded as "the
  same as the legal term '**property linked**'"; "IL" **excludes RPI/CPI-linked policies**
  [REG-R89]. The unitised-with-profits sibling on the same chassis is code **111** and belongs
  to `uk/products/with-profits/`.
- **The 100 segments are one contract for reporting.** IR.14.01 counts "multiple policies issued
  as part of the same premium, identifiable increments and rider benefits" as **a single
  contract** [REG-R89]. The composite's 100 segments are carved out of one premium [S1][S2 §2.4]
  (**[std]** count, spec footnote 3), so C0040/C0050 count **one**, matching the bond-level state
  these notes already carry. A top-up, modelled here as a new model point (**[std]**, spec
  footnote 4), is an "identifiable increment" and does **not** add a contract.
- **IR.14.01 fields this product must produce per code** [REG-R89]: C0030 line of business (31),
  C0040 contracts in force at year end, C0050 new contracts, C0060 gross written premiums,
  C0070 claims paid gross — **including claims management expenses, a definition PS18/26 changes
  from the 31 December 2026 reference date** [REG-R87] — C0180 gross best estimate, and C0190
  capital at risk as defined in SCR – Standard Formula 7.8 and 7.10. The instruction is explicit
  that "**all insurance contracts shall be reported even if classified as investment contract on
  accounting basis**" [REG-R89], which matters precisely because this product may be an
  investment contract in the accounts (below, "Statutory accounts and tax").
- **IR.12.01 / IRR.12.01 — column C0020, and three rows nothing else collects.** The unit-linked
  column carries **R0300 surrender value**, **R0302 nominal value of units** and **R0304 matching
  value of units** [REG-R89], and all three are separate quantities from the best estimate and
  from each other. Applied to this design: R0300 is the bid value of units — no penalty layer in
  the clean structure [S4] (spec footnote 13) — reported net of charges and taxes, **including
  non-guaranteed surrender values**, after any duration-based penalties and **assuming that any
  clause deferring the availability of the surrender value does not apply** [REG-R89], which is a
  real adjustment here because the contract reserves deferral of up to 6 months for property
  funds and 1 month otherwise [S1][S2 §4.4, §8]. R0302 must allow for **actuarial funding /
  discounting where units are "initial" or "capital" units subject to a higher management
  charge** [REG-R89]; the clean design has no initial- or capital-unit layer (allocation rates
  and initial/capital units were not present in any retrieved document and remain an [unverified]
  legacy variation, spec Variations 3), so R0302 is the plain unit value — a **back-book** cell
  carrying capital units would need the funding adjustment. R0304 ties to the units held reported
  in IR.02.01 R0220 and R0340 [REG-R89].
- **IR.12.04 has rows that are this product's own.** The template is triggered at **firm** level —
  gross BEL for long-term business other than reinsurance above **£50 million**, *or* gross
  written premiums above **£10 million** [REG-R84 Art 21A(3)(a)][REG-R89] — but once in scope it
  demands, for the investment bond specifically: **R1050 / R1090 / R1130 lapse and surrender
  rates for years 1–5 / 6–10 / 11+, "including both part surrenders and full surrenders"**, and
  **R1930 per-policy renewal management expense unit cost — investment bond** [REG-R89]. Two
  consequences for these notes. First, the reported surrender rate **aggregates the regular
  withdrawal stream and the full-surrender decrement into one figure**, whereas the recursion
  above keeps `W(t)` and `w_ann` strictly apart — the reporting basis is not the modelling basis,
  and the reconciliation must be explicit. Second, the template requires the **current basis, the
  prior-year basis and five years of the firm's own experience**, with a credibility guideline of
  **200 claims per annum** per line and up to three subcategories in descending size [REG-R89] —
  which is the direct regulatory hook onto the **[std]** surrender table and the **[std]** £60 p.a.
  maintenance expense in these notes, both of which are placeholders with no fetched UK
  persistency or expense study behind them. C0080 requires the **named underlying table**, with
  CMI projections described "consistent with latest guidance from the CMI" [REG-R89] — the hook
  the library can only proxy, since current CMI tables are restricted to authorised users
  [R8][REG-R30].
- **Templates that do not bite the representative design.** IR.12.05 and IR.12.06 (with-profits
  value of bonus; with-profits liabilities and assets) are triggered by with-profits net BEL above
  **£500 million** and are completed per with-profits ring-fenced fund [REG-R84][REG-R90]; a
  non-participating linked bond has no bonus, no with-profits benefits reserve and no future
  policy related liabilities, so it populates none of them — the UWP sibling (code 111) does.
  **IR.05.10 excess capital generation cannot be triggered by this book at all**: its scope test
  is on life premiums **excluding unit-linked premiums** [REG-R84 Art 9(1)(k)][REG-R90], so a
  pure unit-linked bond writer never comes into scope on its own account. Note the framework
  file records that the IR.05.10 scope test is **stated inconsistently** between the Rulebook and
  the instruction file, unresolved [REG-R84][REG-R90] — inert here, but do not restate either
  version as settled.
- **What the retrieved instructions do not settle.** Whether the UK collects a life
  best-estimate **cash-flow projection** template at all: PS3/24 ¶4.70 states that "S.13.01 and
  SR.22.02 will continue to be collected", yet the final Reporting Part contains **no IR.13.01**
  in any Article or in the Chapter 9 inventory and the PRA's published instruction library
  contains no `ir1301` file [REG-R86][REG-R84][REG-R88]. The conflict is recorded, not resolved,
  and **PS15/24 and its appendices were not fetched in the reporting stream** [REG-R86]. Also
  unsettled: how a **partial** discontinuance — a segment surrender [S1][S2 §2.4.5] — is
  reported against a contract count of one.

### Technical provisions

- **Contract boundary: the single premium closes the question, and the regular-premium variant
  opens it.** TPFR 3.5 cuts future premiums out of a pure savings wrapper where **all three** of
  no compensation for a specified uncertain adverse event, no financial guarantee of benefits,
  and no power to compel the premium hold [REG-R41]. On the representative **single-premium**
  design there are no future premiums for the rule to operate on, so 3.5 is inert and the
  boundary is the contract; top-ups are separate contracts with their own boundaries [REG-R41],
  which is exactly the **[std]** treatment in "Model scope and conventions" above (spec footnote
  4). On a **regular-premium** variant the answer is genuinely open: whether a 100.1% death
  uplift [S1][S2] is "a specified uncertain event that adversely affects the insured person" turns
  on the "**no discernible effect on the economics of the contract**" qualifier, **for which no
  quantitative threshold exists in any retrieved source** [REG-R41]. The applicability matrix
  marks the row `?` deliberately to force a drafter to say which variant is meant.
- **The long-term repricing carve-out does not reach this product, and the AMC review right is a
  gap.** TPFR 3.3(3) cuts the boundary at a date on which the firm may amend premiums or benefits
  so that premiums fully reflect the risks, assessed at **portfolio** level *except* for long-term
  insurance business where an individual risk assessment made at inception cannot be repeated
  before amending premiums — there the test is applied **at the level of the contract** [REG-R41].
  That carve-out is what keeps reviewable-rate protection open to full term; it has nothing to
  operate on here, because a single-premium bond has no future premiums to reprice. **The bond
  does carry an insurer right to increase the AMC** [S3 Part D] and to introduce switching charges
  [S2 §6.3.1.2] — but **no retrieved source addresses whether a discretionary charge-review right
  on a single-premium contract engages TPFR 3.3 at all**, and none is invented here; this library
  runs the boundary to the contract and flags the point.
- **Cash flows in scope, and the three TPFR 13.1 streams that are this product's own.** TPFR 13.1
  requires **eight** separately identifiable streams [REG-R41]. Three bite here in ways a generic
  reading misses. (6) **Payments between the firm and investment firms in relation to index-linked
  and unit-linked benefits** makes the unit-fund leg an in-scope best-estimate cash flow, not an
  internal transfer or a memorandum item. (8) **Taxation payments which are, or are expected to
  be, charged to policyholders** is what the composite's **20% in-price life-fund tax provision**
  actually is [S2 §3.2.1][S3 Part E][S4][S5 Q15][R6] — so `TX(t)` must be projected as its own
  stream even though the model books it at **zero insurer margin** (**[std]**, class (b) note
  above); the zero is a statement about *margin*, not a licence to suppress the *stream*.
  Shareholder corporation tax is **not** a best-estimate cash flow — it enters through deferred
  tax under Valuation 11 [REG-R39]. (5) **Payments between the firm and intermediaries** is nil in
  the clean post-RDR design, where set-up, ongoing and ad hoc adviser charges are policyholder
  pass-throughs facilitated by unit cancellation [S1][S2 §12][S4], but a commission-bearing legacy
  cell populates it and it is not an expense-loading convention [REG-R41].
- **Expenses are on a going-concern unit cost, and the inflation rate is the modeller's.** TPFR
  16.1 names administrative, investment management, claims management and acquisition expenses,
  each including allocated overheads, allocated "in a realistic and objective manner and on a
  consistent basis over time" (16.2); **TPFR 16.4 requires expenses to be projected on the
  assumption that the firm will write new business in the future** [REG-R41]. The **[std]** £60
  p.a. per-policy maintenance expense above is therefore a going-concern unit cost, not a run-off
  cost with overheads re-spread over a shrinking book. **Nothing in the rules prescribes an
  inflation index or rate**, so the 2.5% p.a. **[std]** is a modelling choice and stays one. The
  going-concern basis sits in **unreconciled tension** with the risk margin's reference
  undertaking, which "assumes no new obligations" (TP 4B.1(5)) — both correct as printed, and **no
  retrieved source explains how to set the reference undertaking's expenses given that tension**
  [REG-R41][REG-R1]. A model must carry two expense bases.
- **The non-unit best estimate is normally negative, and nothing on the Solvency UK ledger floors
  it.** The applicability matrix records the product-level fact: the **non-unit ("sterling")
  component is commonly negative while the total is positive** [REG-R41][REG-R115], because the
  present value of future AMC exceeds the present value of expenses and death strain — exactly
  the `NUCF(t)` stream above. Nothing floors it: **TP 3.1 contains no floor, no minimum and no
  reference to a surrender value or account value**; TP 2.2 requires a **transfer value**, which
  for a profitable charge stream is legitimately negative before the risk margin; the risk margin
  is non-negative by construction so it offsets but does not floor; and the reporting layer treats
  surrender value as a **disclosure item** (IR.14.01 and IR.12.01 R0300), not a constraint
  [REG-R1][REG-R89]. Decisively for this product, the **Solvency I unit-reserve floor was
  expressly not carried over**: INSPRU 1.2.62R required mathematical reserves to be at least the
  value of the units allocated, and INSPRU 1.2 does not apply to a Solvency II firm [REG-R115].
  Any residual instinct that "the unit reserve cannot be less than the units" is a Solvency I
  instinct. The other two ledgers **do** floor it (below, "Statutory accounts and tax"), which is
  why this product needs three liability measures per period and why the divergence between them
  is among the largest in the library [REG-R100].
- **The unit / non-unit split is required to exist, but the formula for it is a market reading.**
  No retrieved PRA rule creates, requires or names a "unit reserve", a "non-unit reserve" or a
  "sterling reserve" — TP 3.1 gives one best estimate [REG-R1]. What forces a decomposable
  liability is **Investments 4.3**, which attaches the coverage obligation to "technical
  provisions in respect of **linked long-term liabilities**", and **Investments 5.1**, which
  applies the non-linked prudent-person requirements to assets covering a linked contract **only
  to the extent** they cover provisions in respect of any guarantee of investment performance or
  other guaranteed benefit [REG-R114]; and, on the accounts side, Schedule 3 note 26 [REG-R105].
  The widely-used arithmetic — unit-linked BEL = surrender value **less** the PV of future AMCs on
  **existing** units (excluding AMCs on units bought by future premiums), with the sterling BEL as
  the PV of the non-unit cash flows, and the risk margin treated in practice as wholly unit-linked
  because lapse risk dominates — is a **consultancy reading, not a rule** [REG-R118, secondary],
  and the practice of "unit matching" that it enables is possible only because Solvency UK imposes
  no surrender-value floor [REG-R118][REG-R115]. It is tagged as such wherever used.
- **Technical provisions as a whole reach this product and no other in the library — partially.**
  TP 2.5(2) requires TP to be the market value of replicating instruments where cash flows can be
  replicated reliably [REG-R1], and TPFR 22.2 declares three categories non-replicable: cash flows
  depending on the likelihood of policyholders exercising contractual options **including lapses
  and surrenders**; cash flows depending on the level, trend or volatility of mortality,
  disability, sickness and morbidity rates; and **all expenses** incurred in servicing the
  obligations [REG-R41]. Only the **unit-fund component**, in principle replicable by the units
  held, can qualify; the charges, expenses, the 0.1% mortality element and any rider guarantee
  cannot. The reporting layer expects any TP-as-a-whole amount **inside** gross best estimate
  (IR.12.01 R0025/R0026/R0030), so the split is a disclosure attribute, not a separate liability
  line [REG-R89]. One conflict is carried unresolved: the Glossary defines *market value* by
  reference to generally accepted accounting practice while Valuation 2.1 states the Article-75
  standard and Val 12.1 forbids cost and amortised cost, and TPFR 22.3–22.4 use *market value* for
  precisely this calculation [REG-R43][REG-R39][REG-R41].
- **The options and guarantees this design actually contains — and it is fewer than the product
  literature suggests.** The base cell has a 100.1%-of-bid-value death benefit [S1][S2], free
  unlimited switching with the right to introduce charges reserved [S2 §6.3.1.2], regular and
  partial withdrawal and whole-segment surrender at bid value with no penalty [S2 §7,
  §2.4.5][S4], and 30-day cooling-off [S1][S4][S5 Q19]. **None of these is a financial guarantee
  of investment performance**, so TPFR 19.4–19.5 scenario-dependent valuation is `(x)` rather than
  `x` for the representative design and a deterministic run satisfies the rule [REG-R41]. Electing
  the return-of-premium GMDB [S1][S2 §5.2, §10], Quilter's capital-protected death benefit [S5] or
  a PruFund Protected guarantee [S2 §5.3, §11] **makes it `x`** — the guarantee is asymmetric and
  path-dependent, TPFR 15.1 requires dependency of cash flows on circumstances prior to the cash
  flow to be reflected, and Investments 5.1 then pulls the guarantee's backing assets into the
  non-linked prudent-person regime [REG-R41][REG-R114]. Enable a rider and the valuation
  architecture changes, not just a parameter.
- **A static lapse table is not permitted here without evidence.** TP 9.2(2) requires assumptions
  on the likelihood of option exercise **including lapses and surrenders** to take into account,
  explicitly or implicitly, the impact of future changes in financial and non-financial conditions
  [REG-R1]; TPFR 11.1 requires an analysis of past behaviour and a prospective assessment covering
  how beneficial exercise was and will be, past and future economic conditions and past and future
  management actions, and closes: "**The likelihood shall only be considered to be independent of
  the elements referred to in (1) to (4) where there is empirical evidence to support such an
  assumption**" [REG-R41]. For a bond whose surrender value is the fund itself and whose withdrawal
  behaviour is driven by the 5%/20-year allowance clock [R1 s498/s507][R2], that evidence is
  unlikely to exist — which is what `M_perf` and `M_allow` in "Policyholder behavior modeling"
  above are for. They remain **[std]** constructions with no fetched UK bond persistency study
  behind them, and that is a compliance exposure as well as a modelling one.
- **Charge discretion is a TPFR 8 future management action the moment it is assumed.** The AMC is
  insurer-reviewable [S3 Part D] (class (b) above), and the switching-charge right [S2 §6.3.1.2]
  and dilution levy [S2 §3.2.6] are reserved powers. Assuming any of them in the best estimate
  engages TPFR 8: assumptions are realistic only where determined objectively, consistent with
  current business practice and strategy, consistent with each other, **not contrary to any
  obligations towards policyholders or to legal requirements**, and taking account of **any public
  indications by the firm** as to what it would or would not do — with a **comprehensive future
  management actions plan approved by the governing body** covering the circumstances in which the
  firm **may not be able** to act, the order of actions, implementation time and any expenses
  caused [REG-R41]. The "legal requirements" limb is where the Consumer Duty price-and-value
  outcome enters [REG-R12; outcome-location detail unverified]. The base model holds the AMC at
  its **[std]** snapshot and assumes no review, which is the conservative configuration and is a
  choice, not a default.
- **Matching adjustment: ineligible on both routes.** MA 2.2(1) (no future premium payments),
  2.2(2) (permitted underwriting risks limited to longevity, expense, revision, mortality or
  recovery time) and 2.2(4) (no policyholder options, or only a surrender option whose surrender
  value does not exceed the value of the covering assets) **exclude protection and savings
  contracts as a whole** [REG-R2]; the pension annuity in payment is the paradigm case that passes.
  This bond fails 2.2(4) on the face of its own terms — it carries switching, regular-withdrawal
  and segment-surrender rights alongside full surrender [S2 §6.3.1.2, §7, §2.4.5] — *that
  application of the rule to these terms is the drafter's, not a quoted conclusion*, and the
  applicability matrix's `—` mark is the sourced fact [REG-R2]. The **eligible-element** route is
  also closed: MA 1.2 admits only the **guaranteed element of a with-profits immediate or deferred
  annuity** and the **in-payment element of a group death-in-service dependants' annuity or an
  income protection policy** [REG-R2] — a linked bond is on neither list. No MA means no
  attestation, no MAIA, no MA-breach reduction formula, no MA-portfolio notional SCR and no
  MALIR/IRR.22.02/IRR.22.03 return for this product [REG-R2][REG-R8][REG-R91].
- **Discounting: the basic GBP curve, and the tail does not bite.** The best estimate is
  discounted at the relevant risk-free term structure, which the PRA **publishes** — the firm has
  no discretion over it for a PRA relevant currency [REG-R1][REG-R44][REG-R55]. Extrapolation
  beyond the last liquid point does **not** materially reach this product: GBP LLP was retained at
  **50 years** in the 2025 assessment, published 28 November 2025 and effective 1 January 2026
  [REG-R56], and the curve bites only on the non-unit reserve — independently corroborated by the
  PRA's own relevant-currency materiality test, which **excludes unit-linked technical provisions**
  [REG-R55]. **No risk-free rate, ultimate forward rate, convergence period or Smith-Wilson
  parameter appears anywhere in this library**: the four monthly PRA technical-information
  spreadsheets were not opened [REG-R54]. The **volatility adjustment** is permission-dependent
  and entity-level, marked `(x)` rather than `x` for that reason [REG-R1][REG-R55]. **TMTP and TMIR
  are keyed to different gates.** **TMTP** may be applied only with a TMTP Permission, and only to
  technical provisions for obligations that were the firm's *qualifying* obligations on
  **31 December 2024** or were assumed after that date through a transfer event [REG-R3]. **TMIR**
  reaches only *admissible obligations* — contracts concluded **before 1 January 2016** whose
  technical provisions were determined under INSPRU 1.1.16R as at 31 December 2015 and which are
  **not** subject to an MA permission — and requires a s138BA permission [REG-R57]. **A firm
  applying one must not apply the other** [REG-R3][REG-R57]. The `(x)` materiality mark for a
  unit-linked bond rests on a judgement that pre-2016 blocks are small relative to the reserve —
  the research's judgement, not a retrieved fact — carried forward here **[unverified]**
  [REG-R3][REG-R57].

### The risk margin

The formula, the cost-of-capital rate, the taper and the discounting convention are in
`uk/regulatory/technical-notes.md`, "The risk margin". Only three things are product-specific.

- **What the reference undertaking carries for a fee-funded bond.** TP 4B.1 restricts the
  reference undertaking's notional SCR to **underwriting risk** on the transferred business,
  **market risk other than interest rate risk** where material, **credit risk** on reinsurance,
  SPVs, intermediaries and policyholders, and **operational risk** — and nothing else [REG-R1].
  For this product that keeps in the two things that matter (lapse, and the equity/property
  exposure of the *charge base*) and drops the one that is second order anyway (interest rate).
  So `SCR(t)` runs off with the **projected unit fund and the persistency curve**, not with a
  benefit schedule — the risk-margin run-off inherits the same market beta as the AMC margin
  stream and the same sensitivity to the **[std]** surrender table. The reference undertaking also
  applies **no MA, VA, risk-free transitional or TMTP** [REG-R1], which is inert here since none
  is applied in the base design.
- **`SCR(t)` must be projected, and there is no UK simplification to fall back on.** The formula
  sums a discounted, tapered stream of notional SCRs indexed by integer year, so the model must
  produce `SCR(0), SCR(1), SCR(2), …` [REG-R1]. **The Delegated Regulation's risk-margin
  simplification hierarchy was not restated into Solvency UK** — Article 58 of the revoked
  DR (EU) 2015/35 has no UK rule text, the TPFR Part's "SIMPLIFICATIONS" heading introduces
  Chapter 27 (proportionality) only, and IRPR regulation 7C preserves a PRA *power* to permit
  simplified methods that, on the Rulebook text retrieved on 2026-08-06, **has not been exercised**
  [REG-R41][REG-R49][REG-R42][REG-R44]. A driver-based proxy (for example, scaling `SCR(t)` on the
  projected unit fund) must be justified against TPFR 27.4 on its own merits; **no rule text
  sanctions any specific proxy**.
- **Allocation to lines of business is required and unspecified.** The calculation is for the whole
  portfolio, then **allocated** so as to reflect the contributions of the lines of business over
  the lifetime of the portfolio (TP 4A.3) — **no allocation formula is prescribed** [REG-R1]. The
  market convention of treating a linked contract's risk margin as wholly unit-linked, on the
  ground that lapse risk dominates, is a **consultancy reading, not a rule** [REG-R118, secondary].
  Separately, the IR.12.01 instruction permits **SS8/24 §3.2** to be used to calculate the risk
  margin during the financial year — **SS8/24 was not retrieved and its title is not asserted
  here** [REG-R89].

### SCR — the modules that bite

Every stress size, correlation and factor below is stated for orientation only; the full tables,
the aggregation and the worked arithmetic are in `uk/regulatory/technical-notes.md`, "The standard
formula SCR". Every module measures a **loss in basic own funds**, every scenario is instantaneous
at the valuation date, and every scenario-based requirement is **floored at zero** — where a
scenario would increase basic own funds the calculation must assume it has no impact
(`SCR-SF 3.3A(5)`) [REG-R61][REG-R62].

- **Lapse `3B6` is the dominant sub-module, and for this product the direction is UP.** Three
  scenarios, three complete revaluations of the best estimate, charge = the **highest** of them
  [REG-R62]: `3B6.2` an instantaneous permanent **relative increase of 50%** in option exercise
  rates, capped so the increased rates do not exceed **100%**, applied **only to options whose
  exercise increases technical provisions without the risk margin**; `3B6.3` an instantaneous
  permanent **relative decrease of 50%**, the decrease **not to exceed 20 percentage points**,
  applied only where exercise **decreases** them; and `3B6.6(2)` an instantaneous **mass
  discontinuance of 40%**. The filter decides the direction, and for this design it decides it
  cleanly: surrender pays the bid value of units with no penalty [S4] while the non-unit best
  estimate is negative [REG-R41], so discontinuance **increases** technical provisions without the
  risk margin and routes the bond to the **up** and **mass** limbs. **This is the opposite of a
  lapse-supported design** — the over-50s guaranteed-acceptance whole of life is the paradigm
  lapse-supported cell and is stressed by lapse **down** [REG-R62]; assuming the same direction for
  a charge-funded bond is a classic and expensive error. Lapse **down** reaches this product only
  through a cell in which continued persistency costs money, i.e. an **in-the-money
  return-of-premium GMDB** [S1][S2 §10], which is why the applicability matrix carries `(x)` rather
  than `—` on that row [REG-R62]. **The SCR research stream marked lapse-up `x` uniformly across
  six products; the product stream splits the direction per product, and the divergence is
  recorded, not resolved** [REG-R62].
- **The 70% mass-lapse limb does NOT apply, and PS15/24 read alone gets this wrong.** `3B6.6(1)`'s
  **70%** event reaches only policies within **RAO Schedule 1 Part II class VII (pension fund
  management)** [REG-R62][REG-R14]. As published in **PS15/24 Appendix 6 Annex O** the rule also
  named **class III, "linked long term"** — this contract's own class — and the PRA declared that
  reference an **error on 20 December 2024**, deleting it by the Solvency II Amendment (No 1)
  Instrument 2024 **effective 31 December 2024** [REG-R64]. **A UK unit-linked bond therefore takes
  the 40% limb.** Two caveats travel with it: the correcting statement **conflicts with itself on
  the class list** — its narrative mentions class II and class VII while its conclusion and the
  live rule text name class VII only — and **PS15/24 ¶¶6.16 and 6.18 remain published and
  unamended** [REG-R64][REG-R42]. This is the single most product-consequential correction in
  Solvency UK for a unit-linked writer, and it is a 30-percentage-point difference on the sub-module
  that dominates this product's SCR.
- **Mass lapse is not "surrender 40% of policies".** `SCR-SF 1.2` defines **discontinuance** to
  include surrender, lapse without value, **making a contract paid-up**, automatic non-forfeiture
  provisions and exercising other discontinuity options, and `3B6.8` requires the mass-lapse
  calculation to be based on **the type of discontinuance that most negatively affects basic own
  funds on a per-policy basis** [REG-R62]. On this contract there is **no paid-up state** — a
  single-premium bond carries no premium obligation ([unverified] as an explicit contractual
  statement; consistent with S1–S5) — so the per-policy worst-discontinuance search collapses to
  surrender for the base cell. **What no retrieved source settles** is how a **partial**
  discontinuance interacts with the event: a whole-segment surrender is a partial exercise on one
  contract [S1][S2 §2.4.5], and `3B6.7` requires the events to be applied **uniformly** to all
  relevant contracts without saying how uniformity is measured on a partially-surrenderable bond.
- **The scenario assumptions are in tension, and the tension is live for this product.**
  `3.3A(1)` fixes that a scenario **does not change the risk margin, deferred taxes or future
  discretionary benefits, and that no management actions are taken during the scenario**, while
  `3.3A(2)(a)` requires the recalculated technical provisions to take account of future management
  actions complying with TPFR 8 [REG-R62]. **The research recorded the tension rather than
  resolving it, and so does this note.** It bites here because the AMC-review right [S3 Part D] is
  exactly the management action a firm would want to assume in a stressed run, and the two limbs
  point opposite ways on whether it may be.
- **Mortality `3B1` and life catastrophe `3B7` bite only through the 0.1% uplift — but the
  direction filter puts the bond inside them.** `3B1.1` is an instantaneous **permanent increase of
  15%** in the mortality rates used to calculate technical provisions, applied **only** to policies
  for which an increase in mortality increases technical provisions without the risk margin
  (`3B1.2`); `3B7.1` is an instantaneous **absolute increase of 0.15 percentage points** in those
  rates for the **following 12 months** only — an addition of +0.0015 in decimal, **not** a
  multiplicative shock — with the same TP-increasing filter [REG-R62]. Because the death benefit
  is **above** the unit fund (`u = 1.001`), higher mortality raises the non-unit provision, so the
  bond is inside the mortality subset — immaterial in amount but non-zero in sign [S1][S2].
  Enabling the return-of-premium rider changes the **size**, not the sign, and makes the exposure
  market-contingent through `max(0, G − u×UF)` [S2 §5.2, §10][S5].
- **Longevity `3B2` and the whole health module do not reach it.** `3B2.1`'s 20% decrease in
  mortality *reduces* this product's provisions, and the sub-module's own filter excludes such
  policies [REG-R62]. `SCR-SF 3.2A` routes **health** obligations to the health module, **life**
  obligations other than health to the life module — the health module takes precedence and is not
  a residual — and a unit-linked investment bond carries no health obligation at all [REG-R62].
- **Life expense `3B4` is the sub-module most likely to be under-tested here.** `3B4.1` applies a
  **+10% increase in the amount of expenses** used in the technical provisions **and** a
  **+1 percentage point addition to the expense inflation rate**, simultaneously and permanently
  [REG-R62]. On a product whose income is proportional to the fund while its expenses are per
  policy and inflating (**[std]** £60 p.a. at 2.5% **[std]**), this stress and the AMC snapshot
  interact: it is the mechanism by which small-fund cells go margin-negative late in life, which
  "Key sensitivities and model risks" below flags on the modelling side.
- **Equity `3D9` is the market sub-module that actually revalues the liability, and it does so
  through the fee base.** The unit leg self-immunises — the linked assets and the linked liability
  move together — so the residual exposure is the **present value of future charges**, which falls
  with the fund. Stress sizes: type 1 other **39% + SA**, type 2 other **49% + SA**, strategic and
  long-term-equity participations **22%**, qualifying infrastructure equity **30% + 77%×SA** and
  qualifying infrastructure corporate equity **36% + 92%×SA**, where the symmetric adjustment is
  `SA = 0.5 × ((CI − AI)/AI − 8%)` on a 36-month equally-weighted average, bounded at **−10% and
  +10%** [REG-R62]. **No symmetric adjustment value appears anywhere in this library** — the SAECC
  spreadsheet published with the PRA technical information was not retrieved [REG-R54]. One
  modelling consequence specific to a permitted-links product: because COBS 21.3 classifies
  permitted links by **economic substance over legal form** [REG-R10][R3], the market sub-modules
  require a **look-through** to the underlying assets, consistent with `SCR-SF 2.3(1)` [REG-R62] —
  and the composite's collapse of the fund menu to a single composite fund (**[std]**, spec
  Variations 5) deliberately suppresses exactly that look-through. It is adequate for liability
  cash flows and **inadequate for capital work**; unwind it before computing a market SCR.
- **Interest rate `3D5`/`3D6` is second order but still a full revaluation, twice.** Only the
  non-unit charge and expense stream is rate-sensitive, which the PRA's own exclusion of
  unit-linked technical provisions from its relevant-currency materiality test corroborates
  [REG-R55]. The mechanics are unchanged: rebuild the curve, revalue **assets and** the best
  estimate, take the higher direction, summing across currencies within each direction [REG-R62].
  The research flags the **downward shocks as non-monotonic at maturities 14–20** in the retrieved
  rendering, transcribed as an extraction defect and **not silently corrected** [REG-R62].
- **Operational risk is inverted for this product, and it is the one module where a unit-linked
  bond is charged differently from every other product in the library.** `5.4(4)(b)` deducts
  `TP_life-ul` from the provisions leg, so **a pure unit-linked book contributes nothing** to the
  0.45%-of-technical-provisions charge, and `5.4(3)` likewise excludes unit-linked premium via
  `Earn_life-ul` from the 4% premium leg. Instead `5.4(1)` charges **0.25 × `Exp_ul`**, 25% of the
  expenses incurred **during the previous 12 months** on long-term business where the investment
  risk is borne by policyholders — and that term is **added on top of `min(0.3 × BSCR; Op)` and is
  itself uncapped** [REG-R62]. For a pure bond writer the operational charge is therefore
  essentially `0.25 × Exp_ul`, **independent of fund size**. Consequences: `Exp_ul` is a required,
  separately tagged model output (the **[std]** £300 acquisition and £60 p.a. maintenance expenses
  are its inputs here); a two-year earned-premium history is still needed for the growth surcharge
  on any non-linked business [REG-R62]; and booking unit-linked technical provisions into
  `Op_provisions` double-charges. The research flags **mismatched brackets in the extracted LaTeX
  for `5.4(3)`** as a rendering defect, transcribed rather than corrected [REG-R62].
- **Modules that expressly do not reach the representative design.** **LACTP `Adj_TP` is nil**:
  `Adj_TP = −max(min(BSCR − nBSCR; FDB); 0)` is capped at future discretionary benefits, which a
  non-participating linked bond does not have, so `BSCR = nBSCR` and **one run suffices** —
  with-profits is the product that forces the two-run architecture [REG-R62]. **LACDT `Adj_DT`
  still applies**: the change in deferred taxes from an instantaneous loss of
  `BSCR + Adj_TP + SCR_operational`, with **no benefit taken for an increase in deferred tax
  assets** — the transitional permitting otherwise ran only to **30 December 2025**, is **still
  printed in the 05/08/2026 Rulebook view, and no PRA instrument confirming expiry or extension was
  retrieved**; treat it as expired for a current-date calculation and flag it [REG-R62]. **No
  ring-fenced fund and no matching adjustment portfolio**, so `SCR-SF 9.1` perimeter aggregation
  and the loss of diversification between perimeters do not apply — the authority is **EIOPA
  Guideline 2(a)**, that conventional unit-linked and index-linked products are generally outside
  the scope of ring-fenced-fund treatment, and it carries its own status caveat: those guidelines
  cite the Solvency II Directive and the Delegated Regulation rather than PRA rules, and their
  continued UK application rests on **SoP1/19, which was not retrieved** [REG-R80c]. **No
  undertaking-specific parameters**: the replaceable-parameter list is **exhaustive** and reaches
  only non-life and NSLT health premium and reserve risk, the non-proportional reinsurance
  adjustment factor and the increase in annuity benefits for life and health revision risk — there
  is **no USP for any lapse, expense, mortality or market parameter** [REG-R65]. **No EPIFP
  decomposition**: the requirement has been removed from Solvency UK reporting and disclosure
  altogether [REG-R86][REG-R77], so a UK document describing an EPIFP figure for this product is
  describing the EU regime.

### Own funds, ring-fenced funds and the MCR

Tiering, the eligibility limits and the MCR coefficients are in `uk/regulatory/technical-notes.md`,
"Own funds, the reconciliation reserve and the minimum capital requirement". Product-specific:

- **The whole result lands in the reconciliation reserve, in Tier 1 unrestricted.** The
  reconciliation reserve is a **residual** and **may be positive or negative** (Own Funds 3C.2),
  and a firm is **not required to look through** to the underlying assets and liabilities to
  establish that it displays the Tier 1 features (3C.3) [REG-R77]. So this product's **negative
  non-unit best estimate feeds the highest tier of capital directly**, and every assumption in
  these notes — the surrender table, the AMC snapshot, the expense basis — reaches regulatory
  capital through that single line.
- **No ring-fenced fund, no MA portfolio, therefore no Own Funds 3L deduction.** Restricted own
  funds above a perimeter's notional SCR are struck out of the reconciliation reserve for firms
  with an RFF or an MA portfolio [REG-R77]; neither exists for a non-participating linked bond
  written in the main fund [REG-R80c]. **No surplus funds either** — the Surplus Funds Part
  operates on with-profits business and the estate belongs to `uk/products/with-profits/`
  [REG-R45]. (EIOPA's companion point, subject to the same SoP1/19 caveat: surplus funds are not
  ring-fenced merely by being surplus funds, only by arising inside a ring-fenced fund
  [REG-R80c].) A **unitised with-profits** bond on the same chassis (code 111) flips every one of
  these marks.
- **The MCR terms this product populates.** `MCR_linear` for long-term business is a five-term
  linear formula over technical provisions **without the risk margin**, net of reinsurance and
  **floored at zero term by term** [REG-R78]. This bond's term is **`TP_l3`, linked liabilities** —
  it is the only product in this library for which that is the primary term. **`TP_l2`** (future
  discretionary benefits of with-profit business, carrying the formula's only **negative**
  coefficient) is nil here. **Capital at risk** is `max(0, A − B)` per contract — A being the
  amount the firm would currently pay on death or disability plus the expected present value of
  further amounts payable on immediate death or disability, B the best estimate of the
  corresponding obligations — and it is floored at zero **per contract, not on the portfolio sum**
  [REG-R78]. At a 0.1% death uplift it is negligible in amount [S1][S2], but it is a required
  per-contract output (and, per the reporting convention above, a **per-bond** rather than
  per-segment one [REG-R89]). In practice `MCR_linear` sits far below 25% of the SCR, so the MCR is
  normally the **25% collar**, with the long-term **absolute floor of £3,500,000** [REG-R78]. Two
  points the sources leave open are carried: **MCR 3.1B versus MCR 3.3** on whether the corridor
  SCR includes capital add-ons, and **how the MCR interacts with ring-fenced funds at all** — the
  second inert here [REG-R78].

### Statutory accounts and tax

- **The accounting classification fork comes first, and it is this product's largest accounting
  fact.** A unit-linked bond frequently fails FRS 103's significant-insurance-risk test and is an
  **investment contract** rather than an insurance contract. HMRC records exactly that treatment:
  such policies "are not regarded as insurance for accounts purposes; these are treated as
  '**investment contracts**' with premiums from customers generally held on balance sheet as
  **policyholder deposits** and only the fees charged within the policy treated as income"
  [REG-R18 LAM01100]. Investment contracts fall **outside FRS 103**, into FRS 102 Sections 11/12
  and Section 23 for the service element [REG-R99][REG-R102][REG-R100 IG1.8]. The accounts
  signature is therefore **deposit-plus-fee-income**, not premium-and-claims — which is the shape
  of the `NUCF(t)` stream in these notes, not of the gross premium and claim flows. **FRS 103
  Appendix II, the significant-insurance-risk test that would decide it, was not read**
  [REG-R99], and on the representative 100.1% uplift the classification is a **per-design
  determination, not a product-family fact** — which is why the applicability matrix marks the
  FRS 103 rows `(x)` rather than `x` or `—` [REG-R99]. The 101% variant [S3 pre-2006][S4][S5
  pre-25/11/2024] does not obviously change the answer and **no retrieved source supplies a
  threshold**. A model must therefore make the classification an explicit switch.
- **If it is an insurance contract, the accounts balance sheet is two-part.** Schedule 3 to
  SI 2008/410, note 26: liabilities item **D, technical provisions for linked liabilities**, covers
  provisions relating to investment under linked policies, and "**any additional technical
  provisions constituted to cover death risks, operating expenses or other risks (such as benefits
  payable at maturity or guaranteed surrender values) must be included under item C.2**", the
  long-term business provision [REG-R105]. That is the accounts mandate for exactly the unit /
  non-unit split these notes already produce: `UF(t)` to item D, the non-unit provision to C.2.
- **Deposit-component unbundling binds this product directly; it reaches whole of life and
  with-profits only conditionally, and no other product in this library at all** [REG-R99]. FRS 103
  ¶2.23: unbundling is **required** where the deposit component can be measured separately *and*
  the accounting policies would not otherwise recognise all its rights and obligations;
  **permitted** where it can be measured separately but is fully recognised anyway; and
  **prohibited** where it cannot be measured separately. On unbundling, FRS 103 applies to the
  insurance component and FRS 102 Section 11 or 12 to the deposit component (¶2.25) [REG-R99].
- **UK GAAP floors what Solvency UK does not, and this is the largest two-ledger divergence for
  this product.** FRS 103 implementation guidance **IG2.47**: the relevant provision for any
  contract should **not be less than the element of any surrender or transfer value calculated by
  reference to the relevant fund(s) or index**; **IG2.41**: no policy may have an overall negative
  provision except as allowed by PRA rules, nor a provision less than any guaranteed surrender or
  transfer value [REG-R100]. So the same business carries a **negative non-unit best estimate on
  the Solvency UK balance sheet and a floored provision in the accounts** — never reconcile the two
  by flooring the Solvency UK number. Two companions: **IG2.48** requires disclosure of the reasons
  for any significant mismatch between the assets held to cover linked liabilities and the linked
  technical provisions [REG-R100] — the accounts-side counterpart of unit matching; and **IG2.49**
  requires that where the linked provision has had regard to **the timing of the tax obligation**,
  that effect is **excluded from the determination of deferred tax** [REG-R100], which bites
  directly on the composite's in-price 20% tax provision [S2 §3.2.1].
- **Acquisition costs are deferred, not expensed — the U.S. story is reversed here.** SI 2008/410
  Schedule 3 **para 13** requires costs of acquiring insurance policies incurred in one financial
  year but relating to a subsequent one to be **deferred**, with DAC at assets item **G.II** and
  its movement at technical account item **8(b)** [REG-R105]; FRS 103 **¶3.7** states that
  acquisition costs "**shall be deferred**", subject to three carve-outs (costs already recovered,
  insufficient net present value of margins, insufficiently certain future premiums or margins),
  with **¶3.9** requiring amortisation over no longer than the recoverability period and **in a
  similar profile to those margins**, no basis prescribed [REG-R99]. **There is no U.S.-style
  first-year statutory strain in the UK accounts**: the **[std]** £300 acquisition expense is
  capitalised and amortised against the AMC margin stream subject to recoverability, not charged in
  full at issue. Three qualifications specific to this product. The **note 17 carve-out** excludes
  DAC to the extent item C.2 **or item D** already allows for the costs, explicitly or implicitly
  through anticipation of future income [REG-R105] — for a linked contract that is a live fork and
  must be an **explicit model configuration**, not an accident of the reserve basis. On the
  **investment-contract** route the FRS 103 DAC rules do not apply at all and FRS 102 Section 23
  governs the service element [REG-R99][REG-R102]. And on the **Solvency UK** ledger there is no
  DAC of any kind: acquisition expenses are projected cash outflows inside the best estimate
  (TPFR 16.1(4)) and the Valuation Part recognises no unamortised expense asset (Val 8.1)
  [REG-R41][REG-R39]. FRS 103 ¶3.10's prohibition on deferring acquisition costs **in with-profits
  funds** is not this product's — it is scoped by ¶3.1(b) to with-profits business and funds inside
  the pre-2016 PRA realistic capital regime, and **whether it reaches a with-profits fund that was
  never in that regime is not settled by the retrieved text** [REG-R99][REG-R100].
- **IFRS 17: the variable fee approach, on the UKEB's stated expectation.** "In the UK, the VFA is
  expected to be applied to insurance contracts such as **unit-linked contracts** and with-profits
  contracts" [REG-R106] — that supersedes the "candidate for the variable fee approach [mechanics
  unverified — general knowledge]" note this file previously carried, and it upgrades the source,
  not the certainty: **IFRS 17 itself is paywalled and was never read anywhere in this library**,
  so every paragraph number here is one the UKEB quotes [REG-R107][REG-R106]. Mechanics that matter
  for a bond model: under VFA, changes in fulfilment cash flows arising from the **time value of
  money and financial risk** go **into the CSM** rather than immediately to insurance finance
  income or expense, with VFA CSM adjustments at **current** discount rates against the GMM's
  **locked-in** rates; eligibility is assessed **at inception and never reassessed**; and
  **acquisition cash flows sit inside the fulfilment cash flows and reduce the CSM at initial
  recognition** — a third acquisition-cost pattern, with no asset, for the opposite reason to the
  U.S. one [REG-R106]. **Annual cohorts** bind: contracts issued more than one year apart may not
  share a group and groups are never reassessed [REG-R106], so the **[std]** treatment of a top-up
  as a new model point (spec footnote 4) also implies a potentially separate IFRS 17 cohort. **No
  confidence level, no coverage-unit formula and no transition proxy is stated anywhere in this
  library** [REG-R107]. And FRS 103 and IFRS 17 will not converge in the near term: the FRC's own
  published position is that FRS 103 "is not aligned with IFRS 17" and that conflicts between
  IFRS 17 and UK company law "mean that it is not currently possible to align" them [REG-R101].
- **Tax basis: BLAGAB, on the I-E computation.** An onshore unit-linked bond is basic life
  assurance and general annuity business [REG-R17][REG-R18 LAM01080][R6]. FA 2012 **s.68** charges
  corporation tax on the **I-E profit** and **s.69** excludes BLAGAB income and gains from any
  other charge; the six-step **s.73** computation runs income referable to BLAGAB, BLAGAB
  chargeable gains as adjusted for allowable losses, certain I-E receipts, `I` as the sum of those
  three reduced by the relievable amount of any non-trading loan-relationship deficit, `E` as
  adjusted BLAGAB management expenses, and `I − E` — a negative result being carried forward as
  **excess BLAGAB expenses** [REG-R17]. **Underwriting-related expenses such as claims are
  excluded from `E`**, which is restricted to accounts-based operational expenses
  [REG-R18 LAM04010]. The **minimum profits test** (s.93–94) ensures taxable income is at least the
  BLAGAB trade profit excluding dividends, creating an I-E receipt and an equal carried-forward
  management expense where it bites [REG-R18 LAM07230]. The **policyholder / shareholder split**
  (s.102–103): the policyholders' rate is the **basic rate of income tax applying in England, Wales
  and Northern Ireland** — **the Scottish basic rate does not apply** — with the main corporation
  tax rate on the shareholders' share, the split being made by comparing the I-E profit with the
  adjusted BLAGAB trade profit [REG-R18 LAM06010, LAM06020]. **This chain is what the composite's
  20% in-price tax proxy stands in for** (**[std]**, spec footnote 11) and what produces the
  basic-rate credit in the policyholder's hands [R6][S4][S5]. One period-sensitivity to carry
  rather than restate: HMRC's own worked illustration uses **2018 rates** and its statement that
  "with CT rates below the basic rate of income tax" there is no longer an advantage in attributing
  more profit to trade profit **was true when written and is not true at the access date**, the
  main CT rate being 25% and the basic rate 20% [REG-R18 LAM01160][REG-R110]. Record the direction
  of the incentive as period-dependent.
- **Two tax mechanics that change the model's expense line.** FA 2012 **s.79's seven-year spreading
  of BLAGAB acquisition expenses is repealed for accounting periods beginning on or after
  1 January 2023**; from that date the deduction follows recognition in the income statement under
  GAAP, with legacy pre-2023 sevenths continuing to run off and any deduction for acquisition costs
  such as DAC arising earlier but recognised in a post-2023 income statement **continuing to be
  disallowed**, so relief is given only once across the transition [REG-R18 LAM04130][REG-R109].
  Descriptions of "1/7th per year" without a date qualifier are stale. And allocation between
  BLAGAB and non-BLAGAB runs through **two separate "commercial allocation" regimes** — one for I-E
  items, one for trade profits — with an overriding requirement that "the overall effect of the
  methods taken together must be **fair**" [REG-R18 LAM05020], so every projected cash flow, asset
  and liability carries a **BLAGAB / non-BLAGAB flag**.
- **Deferred tax exists on two different models, which is why this product needs three liability
  measures.** FRS 102 Section 29 recognises deferred tax on accounts **timing differences**,
  expressly not on balance-sheet temporary differences [REG-R102]; Valuation 11 recognises it on
  **all** assets and liabilities **including technical provisions**, measured as the **Solvency UK
  value less the tax value** [REG-R39]. Structurally different numbers for the same company — hence
  Solvency UK, accounts and tax carried per period, not two of the three. IG2.49's anti-double-count
  rule above sits alongside [REG-R100].
- **Policyholder chargeable-event tax stays exactly where these notes already put it.** The s.484
  events, the s.491–s.494 gain computation, the 5%/20-year allowance under s.498/s.507 as applied
  in IPTM3560, top-slicing at s.535–s.537 and deficiency relief at s.539 [R1][R2] are
  **policyholder-side and generate no insurer cash flow** — modelled through behaviour only. What
  *is* an insurer cash flow, and is easy to conflate with it, is **TPFR 13.1(8) policyholder-charged
  taxation**, the in-price life-fund tax [REG-R41]. Keep the two apart in the code as well as in
  the prose.
- **Distributable earnings run off the Solvency UK balance sheet, not the accounts.** CA 2006 s.830
  restricts distributions to accumulated realised profits less losses, but **s.830(3) makes that
  subject to s.833A** for an authorised insurance company carrying on long-term business, where the
  realised profit or loss is **A − L − D** on **prudential** values, D including the excess of
  ring-fenced-fund assets over RFF liabilities and, where an MA permission is held, the excess of
  the assigned asset portfolio over the MA obligations; **s.833A(3) then caps** distributable
  profits at accumulated profits (realised **or not**) less accumulated losses [REG-R104]. For this
  product neither product-specific deduction in D arises — there is no ring-fenced fund and no MA
  portfolio — so the pattern is a projection of the **Solvency UK own-funds movement**, subject to
  the accounts-based cap.

### Traps peculiar to this product

1. **Lapse direction.** Up and mass, not down. The fee-funded bond pays the fund on surrender [S4]
   against a negative non-unit best estimate [REG-R41], so discontinuance **increases** technical
   provisions and the `3B6.2`/`3B6.6` filters route it there; only an in-the-money GMDB cell
   attracts `3B6.3` [S1][S2 §10][REG-R62].
2. **40%, not 70%, mass lapse.** PS15/24 as published names RAO class III — this product's class —
   in `3B6.6(1)`; the PRA declared that an error and deleted it effective 31 December 2024, and
   PS15/24 remains unamended [REG-R64][REG-R62][REG-R14].
3. **No unit-reserve floor on the Solvency UK ledger; floors on both other ledgers.** INSPRU
   1.2.62R was expressly not carried over [REG-R115], while FRS 103 IG2.41/IG2.47 floor the
   accounts [REG-R100]. Produce all three measures; never reconcile them by flooring the prudential
   one.
4. **Operational risk is driven by `Exp_ul`, not by provisions or premiums.** Unit-linked technical
   provisions and premiums are **deducted** from the ordinary legs and a separate, **uncapped**
   `0.25 × Exp_ul` is added; booking unit-linked TP into `Op_provisions` double-charges [REG-R62].
5. **The in-price tax provision is a required cash-flow stream, not a netting convention.** TPFR
   13.1(8) makes policyholder-charged tax one of the eight streams [REG-R41]; the model's
   zero-margin treatment (**[std]**) is a statement about margin only.
6. **The 100 segments are one contract** for IR.14.01 counts and for per-contract capital at risk
   [REG-R89][REG-R78] — but how a **segment** surrender interacts with the uniform 40% mass-lapse
   event is not settled by any retrieved source [REG-R62].
7. **This product may not be an insurance contract in the accounts at all.** The
   investment-contract route puts it in FRS 102 Sections 11/12 and 23 with a deposit-and-fee
   signature [REG-R18 LAM01100][REG-R99]; do not assume a premium-and-claims technical account,
   and do not assume the answer for one design carries to another uplift level.
8. **Do not port the U.S. no-DAC / first-year-strain framing.** Schedule 3 para 13 and FRS 103 ¶3.7
   both **require** deferral [REG-R105][REG-R99]; the acquisition-cost story reverses at the UK
   border.
9. **The whole-of-life product reports as a bond.** Code **112**, not a whole-of-life code, because
   the whole-life codes exclude single premium bonds that are technically whole of life [REG-R89].
10. **A single composite fund is fine for cash flows and wrong for capital.** COBS 21.3 classifies
    permitted links by economic substance and `SCR-SF 2.3(1)` requires look-through [REG-R10][R3]
    [REG-R62]; the **[std]** single-fund collapse (spec Variations 5) has to be unwound before an
    equity, property, spread or concentration charge means anything.

---

## Valuation and reserve pointers

This library projects gross best-estimate liability cash flows. The reporting templates, the SCR
modules, the MCR terms, the two accounting routes and the tax basis for this product are in
**Statutory accounting and capital** above; this section stays a pointer list for the valuation
layers themselves, which consume these cash flows and are cited, not reproduced:

- **Solvency UK technical provisions.** TP = best estimate + risk margin [R5 TP 2.4];
  BE = probability-weighted average of future cash flows discounted at the risk-free
  term structure, gross of reinsurance, covering *all* cash in- and out-flows
  [R5 TP 3.1, 3.2]. For this product the natural presentation is unit reserve =
  UF(t) (replicated by the linked assets; cf. the TP 2.5 replication rule [R5], which reaches only
  the unit-fund component — see above, "Technical provisions") plus the non-unit BE of the NUCF
  stream above — commonly negative [unverified as terminology; R9 archive papers not extractable],
  and **unfloored** on this ledger.
- **Risk margin.** Reformed Solvency UK cost-of-capital formula: CoC = 4%, risk
  taper λ = 0.9 (floor 0.25) for long-term business, on the notional SCR runoff
  [R5 TP 1.2, 4A.1][REG-R4]. What the reference undertaking does and does not carry for this
  product, and why no UK simplification hierarchy exists, are above.
- **Matching adjustment / TMTP.** Not applied. MA eligibility fails on the whole-contract route and
  the eligible-element route alike, and the TMTP/TMIR marks are materiality judgements the research
  carries as [unverified] — above, "Technical provisions".
- **IFRS 17.** UK-adopted IFRS 17 (effective 1 January 2023) is the accounting frame
  [REG-R38]; the measurement model for a unit-linked bond is the **variable fee approach**, on the
  UKEB's stated UK expectation rather than on IFRS 17 text, which is paywalled and was never read
  — above, "Statutory accounts and tax". The fulfilment-cash-flow engine is the same projection.
- **Standards for the modeling work.** TAS 100 v2.0 (effective 1 July 2023, all
  technical actuarial work; Principle 5 covers models) [R7][REG-R33 same standard];
  TAS 200 v2.0 (insurance work, effective 1 January 2025) [REG-R34].

---

## Key sensitivities and model risks

Dominant assumptions, in order, for a fund-margin product:

1. **Surrender and withdrawal behavior.** Every margin line is proportional to the
   unit fund *and* persistency; surrender costs nothing at the point of exit (SV =
   UF) but truncates the entire future AMC stream. The [std] base table, the
   performance multiplier and the year-21 allowance step are the first assumptions
   to sensitivity-test — no public UK bond persistency study backs them.
2. **Fund return level and path.** AMC income scales with UF, so the liability model
   inherits full market beta on the margin stream; a −20% market move cuts the
   margin base ~20% and (via M_perf) raises surrenders simultaneously.
3. **AMC snapshot vs expense inflation.** The 1.00% **[std]** AMC is a snapshot of a
   discretionary element (per-fund rate cards not public — research gap 5 [S1]);
   maintenance expenses inflate at 2.5% **[std]** while the margin is
   proportional-to-fund — small-fund cells go margin-negative late in life.
4. **Tax pass-through neutrality.** The 20%-of-gross-return in-price proxy **[std]**
   assumes collected tax exactly equals tax payable; the true I-E position has
   timing (deemed disposals, realised-gain charge dates [S5 Q15][S4]) and base
   differences (expense relief, minimum profits test [R6]) that create insurer-side
   tax strain or float not captured here.
5. **Mortality — only if GMDB is enabled.** Base death strain is 0.001 × UF (≈ £1
   p.a. expected per £100k at q = 1%): negligible. With the return-of-premium rider
   the strain becomes market-contingent (max(0, G − u×UF)) and the unpublished
   charge scale [S2 §5.2] is a [std] guess — enable only with its own sensitivity
   set [S1][S2 §10][S5].

Known modeling pitfalls:

- **Charge-base ordering.** AMC accrues on the post-growth, pre-cancellation fund
  (in-price accrual [S2 §5.1.1]). Charging c_m on UF(t−1) or after withdrawals
  changes the margin by ~½ month's growth/withdrawal — small monthly, systematic
  over decades.
- **Counting pass-throughs as margin.** Further costs [S1][S2 §3.1.7] and the tax
  provision [S4][S5 Q15] reduce the unit fund but are not insurer income; booking
  them as margin overstates NUCF by ~107% of the AMC in the anchor cell (year-1
  tax provision 967.89 ≈ 97% and further costs 99.31 ≈ 10% of the 993.10 AMC).
- **Treating the 5% allowance as a product feature.** It is policyholder tax
  machinery [R1][R2]: it never caps what can be withdrawn (the product cap is 7.5%
  [S2 §7.1]) and generates no insurer cash flow. Model it in behavior only.
- **Adviser charges are not insurer income.** Post-RDR set-up/ongoing/ad hoc adviser
  charges are facilitated pass-throughs by unit cancellation [S2 §12][S4]; they
  reduce UF and consume allowance but add nothing to NUCF.
- **Segment-level granularity.** Modeling at bond level is exact only while all 100
  segments stay identical; segment surrenders break symmetry. The composite keeps
  bond-level modeling and notes the approximation **[std]**.
- **Smoothed funds must not be bolted on.** PruFund EGR/smoothing-limit mechanics
  [S2 §3.3.7–3.3.10] and MVR-bearing with-profits funds [S3] change the unit-price
  dynamics and add guarantee costs; they belong to the with-profits reference
  product (`uk/products/with-profits/`), not this recursion.
- **Uplift factor slip.** 100.1% vs 101% [spec footnote 6] is a ×10 difference in
  death strain; keep `u` a parameter, never a hard-coded 1.001.
