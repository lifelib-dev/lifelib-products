# Indexed Universal Life Insurance — Liability Cash Flow Model: Technical Notes (United States)

**Status:** Draft, 2026-08-03.
**Scope note:** Standardized composite for reference modeling, not any insurer's product.
[S#]/[R#] cite `sources.md` (provenance: `us/_research/indexed-ul.md`); [REG-R#] cites
the cross-product reference library `us/references/regulatory-and-actuarial-references.md`
(research provenance: `us/_research/regulatory-actuarial.md`, same R-numbering).
**[std]** marks standardizations introduced for
the reference implementation. Parameter values here are identical to those in
`product-spec.md`; [unverified] flags carry over.

---

## Model scope and conventions

- **Product:** the representative baseline of `product-spec.md`: flexible-premium UL
  chassis + one AG 49-A Benchmark-Index-Account-style indexed account (1-yr S&P 500 PTP,
  cap 10.00% current [S2], 100% par [S2], 0% floor [S2][R1]) + fixed account (4.50%
  current / 1.00% guaranteed [S2]). Standard loans only **[std]**.
- **Base chassis:** the UL-pattern monthly mechanics — monthiversary processing order,
  NAAR convention (DB discounted one month at the guaranteed rate, AV measured before
  the monthly deduction), deduction-before-interest recursion — follow the
  universal-life reference notes (`us/products/universal-life/technical-notes.md`);
  these notes specify only what the indexed crediting engine adds or changes **[std]**.
- **Projection frequency:** monthly. All policy processing occurs on the monthiversary
  ("monthly policy date"), consistent with segment creation on monthly policy dates
  [S3] **[std]**.
- **Timing:** beginning-of-month (BOM) processing for premium, deductions, sweeps, and
  segment events; interest credited over the month (end-of-month effect). Decrements
  (death, lapse) applied at end of month after crediting **[std]**.
- **Rate conversions:** an effective annual rate i is applied monthly as
  (1+i)^(1/12) − 1 **[std]**.
- **Decrement conversions:** an annual decrement rate q is converted to monthly as
  q_m = 1 − (1 − q)^(1/12) **[std]**.
- **Age basis:** age nearest birthday (ANB) **[std]** (spec Table 1, F1); attained age
  increments on policy anniversaries **[std]**.
- **Model points:** single-policy model points, projected on expected decrements
  (probability-weighted in-force), one segment ladder per model point. Seriatim or
  grouped runs are an implementation choice outside these notes.
- **Projection horizon:** to attained age 121 **[std]**, [unverified] maturity inference
  (spec F5).
- **Currency/rounding:** USD; no rounding in the recursion (display rounding only) **[std]**.

## Model point attributes

| Attribute | Type | Example |
|---|---|---|
| Issue age (ANB) | int | 45 |
| Sex | enum {M, F} | M |
| Risk class | enum (per spec Table 1) | Non-Tobacco |
| Face amount F | currency | 250,000 |
| DB option | enum {A, B} | A |
| Planned annual premium | currency | 10,000 **[std]** example |
| Premium mode | enum | annual, paid at BOM of policy month 1 each year **[std]** |
| Indexed allocation w_ix | percent of sweepable balance | 100% **[std]** |
| Issue date / duration offset | date, months | t = 0 |
| Existing loan balance | currency | 0 |
| Tax test | enum {GPT, CVAT} | GPT **[std]** (spec F4) |
| MNLP rate (no-lapse premium per $1,000 face p.a.) | rate table lookup | 20.80 for M/NT/45/band 1 [S3] (band-1 rate as placeholder — the 250,000 example face is a higher band whose rate is not public **[std]**) |

## State variables

| Symbol | Description | Initial value |
|---|---|---|
| FA_t | Fixed (holding) account balance | 0 |
| S_{k,t} | Balance of segment k (k indexed by creation month m_k; 12-month term) | created at sweep |
| AV_t | Account value = FA_t + Σ_k S_{k,t} + LCA_t | 0 |
| LCA_t | Loan collateral account (standard loans) | 0 |
| L_t | Loan principal + accrued interest | 0 |
| SC_t | Surrender charge (per spec Table 3, F17 schedule) | $25/$1,000 × F/1,000 **[std]** |
| CSV_t | Cash surrender value = AV_t − SC_t − L_t | — |
| CumP_t / CumMNLP_t | Cumulative premiums less withdrawals & loans / cumulative MNLP | 0 / 0 |
| DB_t | Current death benefit (post-corridor) | — |
| l_t | In-force probability (survivorship of death & lapse) | 1.0 |
| 7-pay / GPT accumulators | §7702/§7702A test state [R4][R5] | per issue |

## Assumption inputs

The model distinguishes three assumption classes explicitly:

**(a) Contractual / guaranteed elements** (from `product-spec.md`, all cited there):
guaranteed minimum fixed rate 1.00% [S2]; guaranteed minimum cap 2.00% [S2]; guaranteed
participation 100% [S2]; floor 0% [S2][R1]; guaranteed maximum charges (premium load 8%
**[std]**, policy fee $15 **[std]**, per-unit $0.40 all years **[std]**, COI at 2017 CSO
ANB ultimate **[std]**/[REG-R17]); surrender charge schedule **[std]**; loan charged rate
3.00% **[std]**; corridor factors [R4]; MNLP rates [S3]. Guaranteed-basis projections use
only this class.

**(b) Current non-guaranteed scales** (insurer-declared; snapshots, re-declarable —
NGE discipline per ASOP 2 [REG-R26]): fixed account 4.50% [S2]; cap 10.00% [S2]
(snapshot — observed 10.00–13.75% across carriers/dates [S2][S3][S4][S5][S7], and the cap
is re-set at each segment start [S3][S4]); premium load 5% **[std]**; policy fee $10
[S3][S5]; per-unit $0.30 years 1–10 **[std]**; current COI = 65% of guaranteed **[std]**;
loan credited rate 2%/3% **[std]**. In projection, current scales are held level unless a
cap-re-declaration model (option-budget-driven, below) is switched on **[std]**.

**(c) Behavioral / experience assumptions** (model-owner best estimates; recommended
public bases):
- Best-estimate mortality: 2015 VBT (sex/smoker-distinct, ANB, RR table fit to class)
  [REG-R18], validated/adjusted with ILEC 2012–2019 A/E experience [REG-R19]; guaranteed
  elements use 2017 CSO [REG-R17]. VM-20 prudent estimates credibility-blend company
  experience toward the industry (VBT) tables [REG-R3][REG-R23].
- Base lapse and surrender: LIMRA/SOA U.S. individual life persistency study (2009–2013
  observations) [REG-R20] and the 2015–2021 UL premium persistency and lapse/surrender
  study (24 companies, ~80% of market for lapse; 14 companies for premium persistency)
  [REG-R21]. Numeric base-lapse levels in this library are placeholders **[std]**: 6%/yr
  durations 1–10 grading to 4%/yr, with a surrender-charge-expiry spike (below).
- Premium persistency (flexible-premium behavior — the assumption unique to UL-type
  products [REG-R21]): planned premium paid with annual persistency factor 98% **[std]**,
  compounding (i.e., expected premium_y = planned × 0.98^(y−1)).
- Expense (insurer own-expense, distinct from policy charges): per-policy maintenance
  $75/yr + $150 per issue **[std]** placeholders; premium tax 2.0% of premium **[std]**
  placeholder. Calibrate to company studies; no public source in the research set.
- Index scenarios: see "Stochastic index scenarios vs illustrated-rate projections".

## Cash flow components and recursions

### Notation (defined once; monthly step t → t+1, policy month t = 0, 1, 2, …)

| Symbol | Meaning |
|---|---|
| P_t | premium received at BOM t |
| l_prem | premium load rate (current 5% **[std]**) |
| NP_t = P_t (1 − l_prem) | net premium |
| e_pol, e_unit | policy fee $10/mo; per-unit charge $0.30 per $1,000 (mos of yrs 1–10) |
| coi_t | current monthly COI rate per $1,000 NAAR (65% of guaranteed **[std]**) |
| NAAR_t | net amount at risk |
| MD_t | total monthly deduction |
| i_fix, i_g | fixed-account current rate 4.50% [S2]; guaranteed 1.00% [S2] |
| c, p, f | cap 10.00% [S2]; participation 100% [S2]; floor 0% [S2] |
| I(t) | index level at monthiversary t (S&P 500 price return) [S2][S3] |
| S_{k,t} | balance of segment k created at m_k, maturing at m_k + 12 |
| W_t | partial withdrawal (gross of $25 fee [S3]) |
| B_t | new standard loan taken at t |
| i_L^c, i_L^e | loan charged 3.00%; collateral credited 2.00%/3.00% **[std]** |
| κ_x | §7702 corridor factor at attained age x [R4] |
| q^d_t, q^w_t | monthly death / lapse rates (class (c) assumptions) |
| v_g = (1+i_g)^(−1/12) | one-month discount at guaranteed rate **[std]** |

### Monthly processing order (monthiversary t) **[std]** (carrier ordering conventions vary; this order is fixed for the reference model and matches the universal-life base-chassis order — premium, withdrawal, DB/NAAR, deduction, interest, decrements — per `us/products/universal-life/technical-notes.md`; the segment steps are the IUL additions)

1. **Anniversary resets** (if t ≡ 0 mod 12): attained age +1; re-declare NGEs if the
   re-declaration model is on; update corridor factor κ_x [R4]; annual premium P_t
   received (net premium NP_t → FA).
2. **Segment maturity** (for any k with t = m_k + 12): compute index credit (below), add
   to S_k; roll matured value into a new segment (standing instructions) **[std]**.
3. **Withdrawals / new loans** processed: W_t + fee from FA then pro rata from segments
   [S3]; new loan B_t moves collateral FA-first-then-pro-rata [S3] into LCA.
4. **Death benefit and NAAR:** DB_t per option and corridor on the post-premium,
   post-withdrawal account value; NAAR_t per the recursion below (DB discounted one
   month at the guaranteed rate, AV measured before the monthly deduction — the
   universal-life base convention).
5. **Monthly deduction** MD_t = e_pol + e_unit·F/1000·1{yr≤10} + coi_t·NAAR_t/1000
   (+ rider charges, none in baseline), taken from FA first, shortfall pro rata from
   active segments **[std]** (convention; Transamerica instead half-weights in-segment
   deductions in its credit base [S3] — see variation note below). Shortfall test: if
   CSV_t cannot cover MD_t and the no-lapse test fails (CumP_t < CumMNLP_t during the
   no-lapse period [S3][S4]) → grace/lapse processing (61 days [S3]; modeled as lapse
   at t+2 months if unfunded **[std]**).
6. **Sweep:** transfer w_ix × FA balance (after 1–5) into a new segment created at t
   **[std]** (monthiversary sweep; spec F10).
7. **Interest crediting for the month:** FA × ((1+i_fix)^(1/12) − 1); LCA at the loan
   collateral credited rate; segments earn 0 interim interest (0% floor design [S2];
   contrast Transamerica's in-segment 0.75% [S3]); loan balance accrues
   L_{t+1} = (L_t + B_t) (1+i_L^c)^(1/12) (new loans B_t from step 3 added to principal).
8. **Decrements:** expected claims and surrender cash flows; update in-force l_{t+1}.

### Core recursions

Fixed (holding) account:

    FA_{t+1} = [ FA_t + NP_t − MD^FA_t − W^FA_t − B^FA_t − Sweep_t + Roll^FA_t ] × (1+i_fix)^(1/12)

Segment k (created at m_k with S_{k,m_k} = Sweep_{m_k} share; term 12 months):

    S_{k,t+1} = S_{k,t} − MD^seg_{k,t} − W^seg_{k,t} − B^seg_{k,t}      (no interim interest)
    r_k       = I(m_k+12) / I(m_k) − 1                                  [S2][S3]
    cr_k      = max(f, min(c, p × r_k))                                 [S2][S3][R1]
    Credit_k  = cr_k × S_{k, m_k+12}                                    **[std]** credit base
    matured value = S_{k,m_k+12} × (1 + cr_k)  → new segment (or FA per instructions)

Credit-base variation (not baseline): Transamerica's contractual formula credits
(adjusted index change %) × (segment's adjusted beginning value) − (interest already
credited at the guaranteed minimum during the segment), where the adjusted beginning value
subtracts withdrawals, loan transfers, and one-half of monthly deductions and
index-account charges taken during the segment [S3].

Net amount at risk and COI (discounting convention **[std]**, consistent with the
universal-life base chassis; AV_t is measured before the monthly deduction):

    NAAR_t = max(0, DB_t × v_g − AV_t)          v_g = (1+i_g)^(−1/12)
    COI_t = coi_t × NAAR_t / 1000

Death benefit (Option A baseline **[std]**):

    DB_t = max(F, κ_x × AV_t)                  κ_x per §7702(d): 2.50 at ages 0–40 → 1.00 at 90–95 [R4]
    death claim outflow = DB_t − L_t

Cash surrender value and policyholder cash flows:

    CSV_t = AV_t − SC_t − L_t
    surrender outflow at t = CSV_t ;  withdrawal outflow = W_t − $25 fee [S3]

Liability cash flow (insurer perspective, month t) **[std]** sign convention (inflow +):

    CF_t = l_t·[ P_t − E_t ] − l_t·q^d_t·(DB_t − L_t) − l_t·q^w_t·CSV_t − l_t·(W_t − fee) + net loan cash flows
    where E_t = insurer own expenses (class (c)); policy charges are internal transfers
    within AV, not direct cash flows — they emerge in profit as margins, but the *gross
    liability cash flow* projection tracks premiums in, benefits/withdrawals out.

### Option-budget economics and cap re-declaration

The AG 49-A "Hedge Budget" is "the total annualized amount assumed to be used to generate
the Indexed Credits of the account, expressed as a percent of the account value," required
to be consistent with the insurer's actual hedging program [R1]. Economically: the
general-account net investment earnings rate (NIER) funds the purchase of index options;
the cap is what that budget buys [R1][R6]. For the baseline account (100% par, 0% floor),
the embedded position per $1 of segment value is a one-year call spread, and the cap c
satisfies approximately **[std]** formulation of the sourced concept [R1][R6]:

    HB ≈ [ C(K = I_0) − C(K = I_0(1+c)) ] / I_0        HB ≈ NIER − target spread

where C(K) is the one-year call price at strike K. Charge-funded accounts add an explicit
asset charge that funds a Supplemental Hedge Budget — e.g., a 1.0% strategy charge buys a
13.25% cap vs 10.25% without [S5]; 0.80%/yr buys 12.0% vs 10.0% [S2] — the mechanism
AG 49-A uses to bound their illustrated rates [R1]. Dynamic hedging is the production
mechanism per insurer marketing [S8]. A cap re-declaration module (optional **[std]**)
resets c each segment year so the call-spread cost matches a projected hedge budget;
otherwise the model holds the current cap level.

### Stochastic index scenarios vs deterministic illustrated-rate projections

- **Deterministic (illustration-style):** apply a level annual credited rate to every
  maturing segment. The rate must respect AG 49-A for anything presented as an
  illustration: BIA maximum illustrated rate = min(arithmetic mean of 25-year geometric
  average credited rates computed daily over lookback windows starting 66 years prior;
  145% of NIER); other accounts capped by reference to the BIA; alternate scale =
  min(illustrated − 100 bps, fixed rate) shown with equal prominence [R1]. Research
  snapshots usable as the level rate: 6.40% carrier-published 1988–2023 lookback for the
  10%-cap account [S2]; carrier current illustrated rates 5.61%–7.38%, e.g. 6.59% [S6].
  Baseline deterministic rate: 6.40% [S2].
- **Stochastic (best-estimate/valuation-style):** simulate I(t) (real-world lognormal
  **[std]**: μ = 6.0%, σ = 16% p.a. placeholders **[std]**), apply the crediting formula
  path by path, average outcomes. Because the cap truncates the entire right tail while
  the 0% floor only offsets losses (cr = max(0, min(c, r)) is piecewise linear, not
  globally concave), at realistic parameters — cap near the mean index return — the mean
  credited rate falls materially below the formula applied at the mean return;
  historical frequency of 0% credits for single-index allocations was 12.55%–23.81% in a
  carrier's 2005–2017 issue-date study [S8]. Deterministic-at-illustrated-rate projections
  therefore overstate credits relative to the stochastic mean at matched expected index
  growth — a first-order model risk (below). Risk-neutral scenarios are used only when
  valuing the embedded option/hedges, not for gross cash flow projection **[std]**.

### Guaranteed floor accumulation test (variation, not baseline)

Some designs guarantee a retrospective cumulative accumulation: Securian's "2% cumulative
average upon death or termination" [S7]; Transamerica's in-segment 0.75% (with a 2%
declared-account minimum) [S3]. Modeling: carry a shadow account accumulating premiums
less deductions/withdrawals at the guarantee rate; on death/surrender pay
max(actual value, shadow value) **[std]** implementation convention. The baseline (0%
annual floor [S2][R1]) needs no shadow account.

## Policyholder behavior modeling

All dynamic formulas are **[std]** (no retrieved source prescribes them); levels are
placeholders to be calibrated to [REG-R20][REG-R21] data and company experience.

- **Base lapse** (annual, converted monthly): 6% durations 1–10, 4% thereafter **[std]**;
  a surrender-charge-expiry spike multiplier 2.0 applied in policy year 11 **[std]**
  (rationale: the 10-year surrender charge period [S1][S5][S7] creates a cliff in
  surrender economics; UL lapse/surrender experience by duration is available in
  [REG-R21] for calibration).
- **Dynamic lapse** **[std]**: multiply base lapse by
  min(2.0, max(0.5, 1 + 3.0 × (r_alt − r_cred,t))) where r_cred,t is the policy's
  trailing credited rate and r_alt a competitor/market alternative rate. Rationale: caps
  and declared rates are NGEs; uncompetitive re-declarations (caps fell 13.75% → 12.00%
  between two print dates of one product [S3][S4]) plausibly drive excess lapse.
- **Premium persistency** **[std]**: planned premium paid with 98% annual persistency,
  plus a funding-stop state (probability 1%/yr **[std]**) after which the policy runs
  charge-only. Rationale: premium persistency is the UL-specific behavior dimension; the
  2015–2021 LIMRA/SOA study is the recommended public calibration base [REG-R21].
- **NLG-tested behavior** **[std]**: while the no-lapse guarantee is in effect and CSV ≤ 0,
  lapse is suppressed (policyholders paying MNLP-level premiums persist); on NLG expiry,
  apply a shock lapse 25% **[std]** for underfunded policies.
- **Loan utilization** (baseline scenario: none **[std]**; distribution-scenario module):
  from a start age (e.g., 65 **[std]**), borrow a level amount annually via standard
  loans; the Overloan Protection Rider caps loan-driven lapse risk [S3].
- **Withdrawal behavior:** none in baseline **[std]**; scenario module mirrors loans.

## Worked example

One segment year; parameters as specified (cap 10.00% [S2], par 100% [S2], floor 0% [S2];
credit base = remaining balance at maturity **[std]**). Segment created at month m with
$12,000 from the sweep; its pro-rata share of monthly deductions is $15.00 in each of the
12 segment months **[std]** example values. Two index scenarios (A: +12%, B: −15%).

| Item | Scenario A (up year) | Scenario B (down year) |
|---|---|---|
| Segment balance at creation, S_{k,m} | 12,000.00 | 12,000.00 |
| Monthly deductions charged to segment | 15.00 × 12 = 180.00 | 15.00 × 12 = 180.00 |
| Balance at maturity before credit, S_{k,m+12} | 11,820.00 | 11,820.00 |
| Index at segment start, I(m) | 4,500.00 | 4,500.00 |
| Index at maturity, I(m+12) | 5,040.00 | 3,825.00 |
| Index change r = I(m+12)/I(m) − 1 | +12.00% | −15.00% |
| Credited rate = max(0%, min(10.00%, 100% × r)) | 10.00% (cap binds) | 0.00% (floor binds) |
| Index credit = rate × 11,820.00 | 1,182.00 | 0.00 |
| Matured segment value → new segment | 13,002.00 | 11,820.00 |

Notes: deductions taken mid-segment earned no index credit (they left the segment before
maturity) **[std]**; under the Transamerica variant the credit base would add back half of
the 180.00 of deductions, giving credit 10.00% × (12,000.00 − 90.00) = 1,191.00 in
Scenario A (before netting the in-segment guaranteed interest that design credits) [S3].
Under the guaranteed-cap-only scenario (class (a)), the Scenario A credit would be
2.00% × 11,820.00 = 236.40 [S2 guaranteed cap].

## Statutory accounting and capital

Concepts and the applicability matrix:
`us/regulatory/statutory-accounting-and-capital.md`; formulas and algorithms:
`us/regulatory/technical-notes.md`. Only what is specific to indexed UL
appears here, with that directory's [unverified] flags and retrieval limits
unchanged; **no AVR factor, IMR amortisation factor or untranscribed RBC
factor appears anywhere in this library** [REG-R89][REG-R128]. **[REG-R#]**
cites the shared numbering, now **R1–R142** (R114–R124 and R143–R149 unused by
design).

### Contract classification and reporting

- **A life contract, immutably, so considerations are premium income.** SSAP
  No. 50 ¶9 lists **universal life type** contracts among life contracts, and
  this chassis charges a monthly COI on a net amount at risk, so mortality
  risk is present throughout; it is never deposit-type, that class being for
  contracts acting "exclusively as [an] investment vehicle" [REG-R78 ¶¶5,
  9][REG-R80 ¶¶2, 5]. Classification is made **at inception and does not
  change** [REG-R78 ¶5]. Premium is therefore recognised **gross, when due,
  including flexible premiums when received**, never credited direct to
  reserve, and the change in **loading** on deferred and uncollected premium
  is an **expense**, not a reduction of premium [REG-R79 ¶¶2–5, ¶11] — so
  premium persistency (98%/yr **[std]**, above) drives a reported income line,
  not only account value. The reserve reports in **Exhibit 5, never Exhibit
  7** [REG-R89][REG-R90].
- **Which Analysis of Operations column is a design decision, not a product
  label.** Individual Life has a distinct **Indexed Life** column *and* a
  **Universal Life With Secondary Guarantees** column; indexed UL **with**
  secondary guarantees reports in the **ULSG** column and **still reports
  there after the guarantee has expired**, while incidental riders report on
  the **base contract's** line [REG-R89]. The baseline carries a no-lapse
  guarantee (spec Table 1, F6), so the choice is live and must agree with the
  VM-20 reserving category below.
- **No separate account, and no DAC.** The indexed account is general account
  and book value, so SSAP No. 56 does not reach this product [REG-R83] — no
  separate-account AVR/IMR question, no transfers line, no C-1cs or C-4a
  separate-account charge, the whole contrast with variable UL. Acquisition
  costs are **expensed as incurred** (SSAP No. 71 ¶6 rejecting the GAAP
  standards that defer them), so `E_t` hits surplus in the issue period
  against one year's flexible premium, with no DAC or EGP amortisation to
  reuse [REG-R75].

### Reserve basis

**The fork that decides everything else: is the no-lapse guarantee a
*material* secondary guarantee?** VM-20 categories are Term, **ULSG** and
**All Other** [REG-R3]. Indexed UL without a material secondary guarantee is
**All Other**; with one it is **ULSG**, changing the NPR method, the
exclusion-test position, the annual statement column and the C-2 bucket at
once. **This library does not reproduce VM-01's "non-material secondary
guarantee" definition** — resolve it from [REG-R3] before branching; the
baseline MNLP design (spec F6) is not assumed to fall on either side.

**Which method, and from when.** For pre-operative-date issues and for the
*All Other* net premium reserve the standard is **CRVM** under Standard
Valuation Law §5, reached through **VM-A / VM-C**, whose index carries
**A-585, the universal life model regulation** [REG-R1][REG-R110][REG-R41];
VM-20 §3.B.6 is explicit that **All Other, and indexed UL where no
deterministic or stochastic reserve is computed, take the VM-A/VM-C basic
reserve** — the old CRVM engine inside a PBR-era manual [REG-R3][REG-R110].
**A-585, A-820 and A-830 were not retrieved**, so nothing beyond the Standard
Valuation Law [REG-R1] and Model #830 [REG-R6] is stated for that track
[REG-R110]. For operative-date issues **VM-20 constitutes CRVM**, minimum
reserve per category = Σ NPR + max(0, max(DR, SR) − (A − B)), categories
**summed, never maximised** [REG-R3]; both engines are therefore in scope for
one book. Two NPR details bite this chassis: the §3.D floor for a **UL**
policy is the cost of insurance to the next processing date on which COI
charges are deducted, **on the net amount at risk and the valuation mortality
rate, not the contractual COI or expense charges**, so `MD_t` is not its
input; and on the ULSG branch §3.B.5 drives the NPR off **FFSG / ASG / LSG**
shadow-account state, which the baseline MNLP test does not carry [REG-R3].

**Exclusion tests, where the hedging bar bites** [REG-R3]. §6.A.1.b: a group
**may not be excluded from the SR** where one or more future hedging
strategies exist, except where all relate solely to features immaterial under
§7.B.1 **due to low utilization** — and an indexed account's option budget is
the crediting mechanism itself, not a low-utilization feature, so a model
projecting the hedge programme forward should expect the **SR to be required**
(consequence derived from the cited rule **[std, derived]**; no source names
indexed UL). §6.B then **deems the DET failed** for any group not excluded
from the SR requirement, pulling the **DR** in with it, and deems it failed
outright for a ULSG whose guarantee is not "non-material"; the outright bar on
the DET reaches only term, which this is not, but the **SET Certification
Method is unavailable to ULSG**, so that branch must pass by SERT or
Demonstration Test — either of which **re-imposes VM-G Sections 2 and 3**
[REG-R109]. §6.B.6 supplies the flexible-premium convention: where no
guaranteed gross premium is specified it is the **level annual gross premium
at issue that would keep the policy in force for the whole coverage period on
the guarantees**, i.e. solved on the guaranteed minimum cap (2.00% [S2]),
guaranteed fixed rate (1.00% [S2]) and guaranteed maximum charges — a derived
quantity, not a policy field. §4.A.5 bars an SR-excluded group from including
**future non-hedging derivative program transactions** in its DR.

**Asset adequacy and governance.** Under VM-30 any shortfall becomes an
**additional reserve** that Standard Valuation Law §6.B makes part of
*minimum* reserves [REG-R100][REG-R1], on starting assets capped at the
statement value of the liabilities tested [REG-R29]; **AG 53** and **AG 55**
trigger on **company- and treaty-level** tests, not by product
[REG-R105][REG-R103]; **VM-31** and **VM-G** bind even a company computing no
DR or SR, which must still file a sub-report and report **readiness to
compute** them [REG-R108][REG-R109]. Change in valuation basis — moving a
cohort from A-585 CRVM to VM-20 — goes **direct to surplus** at the
**beginning of the year**, excluded from the Summary and Analysis of
Operations [REG-R79][REG-R89].

### What this product's model must additionally produce

The generic contract is `us/regulatory/technical-notes.md`, "Required model
outputs", and is not restated; these are the indexed-UL-specific additions to
it. All annual statement page and line references reached through them are
**2025** reporting-year and must be re-verified against the 2026 blank before
being hard-coded [REG-R89][REG-R90].

| Statutory / capital item | Indexed-UL-specific model output |
|---|---|
| Exhibit 5 and Exhibit of Life Insurance [REG-R89] | Reserve by **valuation standard × year of issue**, VM-20 split **NPR / excess over NPR**, gross and ceded produced separately and never netted [REG-R92]; face in force and counts on an **incurred** roll-forward in thousands, including face increase and decrease layers |
| Analysis of Operations column [REG-R89] | A per-contract **Indexed Life vs ULSG** flag that persists after guarantee expiry, agreeing with the VM-20 reserving category |
| Analysis of Increase in Reserves [REG-R90] | Tabular net premium, tabular interest and tabular cost on the **valuation** basis (valuation mortality and interest, not the projected index credit), plus line **6.1, change in excess of the VM-20 DR/SR over the NPR** |
| C-2 exposure [REG-R142] | **Face in force − statutory reserve (GA + SA), net of reinsurance**, at statement level — **not** the model's `NAAR_t = max(0, DB_t·v_g − AV_t)`, a per-policy COI base on a different definition |
| C-2 and C-3a bases [REG-R128] | PV of margin available from re-declaring **cap, participation, COI and loads** over the next **5 policy years** (a repricing scenario, not only the base scenario), and life reserves **on guaranteed values ignoring those related to the index** — assumption class (a) run as its own valuation |
| Derivative programme [REG-R96][REG-R86] | Projected option positions and fair values **and** the hedged-item measurement per hedge relationship, with a designation flag and an effectiveness result at least quarterly; plus counterparty exposure by NAIC designation, which sits in the AVR bond and preferred stock sub-component and so in the base the C-1o factors read |
| Tax [REG-R16][REG-R97] | Tax reserve = max(net surrender value, 92.81% × NAIC-method reserve) capped at statutory, plus the temporary-difference reversal pattern and character |

### Risk-based capital

- **C-2 mortality dominates and is NAR-based.** Exposure is face in force less
  life reserves, net of reinsurance, from the annual statement [REG-R142].
  Bucketing is by **pricing flexibility**, not product code: the instructions
  name **UL without secondary guarantees** as a *with*-flexibility example and
  put **ULSG** in **Permanent without** at the highest factors — **0.00400 /
  0.00175 / 0.00120** against **0.00220 / 0.00105 / 0.00080** — and the
  category must be **earned** (PV of margin from repricing over the next **5
  policy years** ≥ flexibility factor × NAR), the default where no assessment
  is performed being that highest-factor bucket [REG-R128][REG-R133]. The
  repricing levers are exactly the NGEs of assumption class (b) — cap,
  participation, COI, loads, governed by ASOP 2 [REG-R26]. **Size is a
  company-level driver**: the bands (first **$500M**, next **$24,500M**, over
  **$25,000M**) apply to *total* individual and industrial life NAR, then
  allocate proportionately [REG-R128][REG-R133].
- **The §7702 corridor makes both exposure bases endogenous to index
  performance.** A strong index run raises account value, raising the reserve
  (the C-3a base) and, through `DB_t = max(F, κ_x·AV_t)` [R4], face in force
  (the C-2 base) while also raising the reserve subtracted from it **[std,
  derived]**.
- **C-3a is factor-based and the index is ignored.** Life insurance reserves
  sit in the **Low** category, **0.0095** pre-tax falling to **0.0063** where
  the company files an unqualified opinion based on asset adequacy testing,
  and **equity-indexed products take the same factors as their non-indexed
  counterparts, "based on guaranteed values ignoring those related to the
  index", and are excluded from C-3 cash flow testing** [REG-R128]. Phase I
  scope ("Certain Annuities" **plus single premium life**) reaches a life
  product only in a single-premium design, where that exclusion still applies
  [REG-R128][REG-R135]; **Phase II does not apply** (not AG 43 / VM-21
  business) and **C-2 longevity does not apply**, attaching as it does to
  life-contingent annuity reserves [REG-R128].
- **C-1o, C-4a and how the mix combines.** C-1o rides on the backing general
  account — designation factors from **0.00158** (1.A) to **0.30000** (5.C and
  NAIC 6) on book/adjusted carrying value, modified by the **bond size
  factor**, a blank issuer count charged the maximum **2.40**
  [REG-R128][REG-R130] — with the option programme adding counterparty
  exposure to that same AVR-sourced base [REG-R86]; C-4a is **2.53%** of
  Schedule T life premiums, so premium persistency feeds a capital charge as
  well as a cash flow [REG-R128]. Because C-2 is a **standalone squared term**
  while C-3a joins C-1o inside one squared term and C-0 and C-4a sit
  **outside** the radical [REG-R128], a protection-oriented model point (large
  NAR, small account value) puts weight in the diversifying C-2 term while an
  accumulation-oriented one shifts it into the (C-1o + C-3a) term where it is
  additive with asset risk **[std, derived]**.
- **Total Adjusted Capital depends on the AAT run**: it includes the AVR but
  **only the portion not utilized in asset adequacy testing**, so that run
  must report the AVR it consumed [REG-R128][REG-R29]. Action levels, the 3.0×
  trend-test safe harbour and Model #312's five-year projection of statutory
  operating income, net income and surplus apply at entity level
  [REG-R125][REG-R128].

### Product-specific interactions and traps

- **VM-20 with the index credit as a nonguaranteed element.** Cap and
  participation are re-declared at every segment start [S2][S3][S4], so they
  are projected NGEs inside the DR and SR, not contract terms; VM-20 §4.A's
  APV of premiums and related amounts includes **net
  derivative-liability-program flows allocated to the group**, and §2.I
  disallows an alternative investment strategy without first showing it
  produces a **higher** reserve [REG-R3]. The cap re-declaration module above
  is therefore a valuation component, not only a pricing convenience. The
  quantified hedge-inefficiency margin (payoffs reduced by ≥1.5%
  multiplicatively, or ≥20% absent credible experience) is stated for
  **VM-21/VM-22 annuities, not for VM-20 life business**; "Valuation and
  reserve pointers" below records that limit [R3].
- **Hedging brings SSAP No. 86 into the statutory earnings projection.** An
  effective hedge is "valued and reported in a manner that is consistent with
  the hedged asset or liability"; one that fails, or ceases to meet, the
  criteria sits at **fair value with changes through unrealized gains and
  losses**; there is **no bifurcation**; and effectiveness — within
  **80%–125%** of the opposite change in the hedged item, or **R² ≥ 0.80** —
  is assessed at least quarterly [REG-R96]. So an option book designated and
  documented against the index-credit liability can be carried consistently
  with it, while a macro/ALM programme that fails injects surplus volatility
  the projection must show. On termination the gain or loss adjusts the hedged
  item's basis or, **where the hedged item is subject to IMR, may be realized
  and subjected to IMR** [REG-R96 ¶17] — with up to 12 concurrent segments
  [S3][S4] that election is not a rare event. **SSAP No. 86 paragraph
  numbering here is [unverified]** (a 2010 standalone print, never
  cross-checked against the March 2026 manual), and **whether an index-credit
  liability is an item "subject to IMR" is not addressed in the documents this
  library retrieved — no treatment is asserted** [REG-R96].
- **A pending SSAP would materially change projected surplus volatility.**
  SAPWG had at exposure in March 2026 an **amortized cost measurement method
  for a qualifying derivative program**; the exposure documents **were not
  fetched** and adoption is unknown [REG-R88], and the "Clearly Defined
  Hedging Strategy" framing attached to it is **[unverified]**
  [REG-R96][REG-R88]. Keep fair value as the base case and amortized cost as a
  scenario.
- **Negative IMR is a hedging writer's condition and feeds back into the
  reserve.** INT 23-01 ¶9.c admits derivative losses into negative IMR only
  with documented evidence that fair-value derivative **gains** were
  historically reversed into IMR, and ¶9.e requires admitted negative IMR to
  be captured in the PBR calculation or in asset adequacy testing under
  **VM-20 §7.D.7 and VM-30 §3.B.5** with a reconciliation [REG-R87]; VM-30
  §3.B.5 independently requires a **sign-aware** allocation, positive or
  negative [REG-R100]. An admittance decision therefore changes a reserve, is
  retested at **every** reporting date, and sits under an **automatic
  nullification on January 1, 2027** as currently written [REG-R87].
- **AG 49 / AG 49-A govern illustrations, not reserves — do not conflate
  them.** The Benchmark Index Account, the maximum illustrated rate (25-year
  lookback mean capped at 145% of the Annual Net Investment Earnings Rate),
  the other-account leverage cap, the 50 bp loan-spread limit and the
  alternate scale are all Model #582 illustration machinery [R1][R2][R6].
  **Nothing in AG 49-A sets a statutory reserve**, and the baseline
  illustrated rate (6.40% [S2]) is a disclosure ceiling, not a valuation or
  asset-adequacy assumption; nor is the **illustration actuary's**
  self-support / lapse-support certification [R2] the **appointed actuary's**
  VM-30 opinion [REG-R100].

## Valuation and reserve pointers

Statutory accounting consequences of these measurement choices — classification,
Exhibit 5 placement and column, AVR/IMR, derivative accounting and RBC — are in
the preceding section, "Statutory accounting and capital"; the pointers below
state only which measurement standard applies, and are consistent with it.

This library projects **gross liability cash flows**; measurement layers are cited, not
reproduced:

- Statutory: VM-20 net premium reserve plus deterministic/stochastic reserves as
  applicable; IUL is reserved as a UL (life) product under VM-20 — reserving category, the
  formulaic VM-A/VM-C fallback and the exclusion-test position are in the preceding
  section; projections must include
  cash flows of assets hedging indexed credits, under the clearly-defined-hedging-strategy
  (CDHS) framework, with margins increased where hedging documentation is incomplete
  [R3][REG-R3]. Implementation guidance: AAA VM-20 practice note [REG-R23]; governing
  standard ASOP 52 [REG-R31]; enabling statute Model #820 [REG-R1]. A quantified analogue
  for hedge inefficiency exists on the annuity side (VM-21/VM-22 index credit hedge
  margin: reduce hedge payoffs by ≥1.5% multiplicatively, or ≥20% absent credible
  experience) — stated for annuities, not VM-20 life business [R3].
- Interest-indexed UL filings/opinion: Model #585 Section 10 (assets held, falling-rate
  risk, annual actuarial opinion) [R10][REG-R5].
- Illustration testing (if the model doubles as an illustration engine): Model 582
  self-support/lapse-support and DCS limits [R2]; AG 49-A rate limits [R1]; ASOP 24
  [REG-R30]; AAA illustrations practice note [R8].
- Tax reserves: IRC §807 — greater of net surrender value and 92.81% of the NAIC-method
  reserve, capped at statutory [REG-R16].
- Model governance for the implementation itself: ASOP 56 (modeling) [REG-R32]; cash-flow
  analysis standard ASOP 7 [REG-R27].

## Key sensitivities and model risks

Dominant assumptions (in rough order for an accumulation-funded model point):

1. **Credited-rate level and dynamics** — cap re-declaration is the insurer's primary
   lever; caps on the same product fell from 13.75% to 12.00% between print dates
   [S3][S4]; guaranteed minima (2.00% cap [S2]) are far below current levels, so the
   guaranteed-basis projection diverges dramatically.
2. **Deterministic vs stochastic crediting** — using the illustrated rate (6.40% [S2],
   market range 5.61%–7.38% [S6]) as a level credit overstates mean credits vs a
   stochastic run at matched expected index growth (cap truncation; 0%-credit frequency
   12.55%–23.81% historically for single allocations [S8]).
3. **Premium persistency** — flexible premiums mean the funding pattern is behavior, not
   contract; it drives account growth, NLG status, MEC/GPT headroom, and lapse [REG-R21].
4. **Lapse (level + dynamic + SC-expiry spike)** — high sensitivity of both cash flows and
   any illustration lapse-support test [R2][REG-R21].
5. **COI margin vs mortality** — current-vs-guaranteed COI spread is a major profit and
   re-rating lever [S3][REG-R26]; best-estimate mortality from 2015 VBT/ILEC
   [REG-R18][REG-R19].
6. **Loan design and utilization** — participating loans embed an index-vs-5%-charge
   spread bet [S5][S7]; heavy late-life loans plus a 0%-credit sequence can force lapse
   absent overloan protection [S3].

Known modeling pitfalls:

- **Segment bookkeeping**: monthly segment ladders (up to 12 concurrent [S3][S4]) must
  track per-segment index start levels; collapsing to a single annual segment mis-times
  credits and distorts mid-segment surrender values [S3].
- **Deduction sourcing vs credit base**: conventions differ by carrier (pro-rata remaining
  balance **[std]** vs adjusted-beginning-value with half-weighting [S3]); pick one and
  keep DB/CSV/credit formulas consistent.
- **Floor ≠ guarantee confusion**: a 0% annual floor [S2] is not the same guarantee as an
  in-segment 0.75% credit [S3] or a 2% retrospective cumulative test [S7]; mixing them
  double-counts guarantees.
- **Illustrated-rate anchoring**: AG 49-A bounds what may be *illustrated*, not what will
  be *credited* [R1][R6]; a projection model should treat the illustrated rate as a
  disclosure constraint, not a best-estimate assumption.
- **Corridor/MEC interplay**: high funding triggers corridor DB increases (raising NAAR
  and COI) [R4] and 7-pay/MEC status [R5]; omitting these overstates late-duration
  account values and understates charges.
- **Maturity mechanics**: age-121 behavior is [unverified] (spec F5); confirm before
  relying on tail cash flows.
