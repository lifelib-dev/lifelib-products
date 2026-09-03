# Technical Notes

**Status:** Draft, 2026-09-03 (all cited sources accessed 2026-09-03).

**Scope note.** These notes turn the standardized composite tax-qualified pension savings
contract (*yeongeum jeochuk boheom*, 연금저축보험) of `product-spec.md` (same directory)
into a reference liability cash-flow projection on paper, and then into `Pension_KR_A`
beside it. **They describe no single insurer's contract.** [S#] and [R#] tags resolve
against `sources.md`, whose numbering is carried verbatim from
`_research/pension-savings.md` and is frozen; [REG-R#] tags resolve against the
cross-product reference library `references/regulatory-and-actuarial-references.md`, whose
own R1–R62 numbering is separate and also frozen. **[std]** marks a standardization
introduced for the reference implementation; [unverified] marks a claim that could not be
confirmed against a retrieved document. **Every parameter that appears in both documents
carries the same value here as in `product-spec.md`**, and every number in the worked
example is read off the shipped model rather than recomputed by hand.

**This document inherits the accumulation half of the [whole life chassis
(종신보험)](../whole_life/technical-notes.md)** — the 계약자적립액 (*gyeyakja
jeongnibaek*, policyholder account value) recursion, the 해약공제액 and its
표준해약공제액 (*pyojun haeyak gongjeaek*) cap under 보험업감독규정 별표 14 [REG-R20],
and the 해약환급금 (*haeyak hwangeupgeum*, surrender value) floor of 제7-66조제1항제1호
[REG-R19] — and does not restate that machinery. What it adds, and specifies here for the
first time in the library, is five things:

1. crediting at the **공시이율** (*gongsi iyul*, the declared rate) over a stepped
   **최저보증이율** (*choejeo bojeung iyul*, guaranteed floor), rather than at a fixed
   예정이율;
2. the **세액공제** (*seaek gongje*, tax credit) and the 16.5% **기타소득세** (*gita
   sodeukse*) on a non-pension withdrawal as **policyholder-behaviour drivers that are not
   insurer cash flows** — the reason the lapse assumption on this product is not the
   savings lapse assumption;
3. the statutory 연금수령 conditions — five years of contributions, drawing from 만 55세,
   and the 연금수령한도 — as constraints on the projection [R6 제40조의2제3항·제4항](#krlib-pension_savings-r6);
4. the **annuitisation step**: a 100.1%-of-premiums minimum fund, and conversion into a
   종신연금형 (life annuity with a guarantee period) or a 확정기간연금형 (annuity-certain)
   at a factor struck on the 경험생명표 proxy; and
5. the question of **which vintage of that table the factor is struck on** — at 가입 or at
   연금개시 — which the retrieved contracts settle only by inference and on which two
   carriers could legitimately differ.

**One correction to `product-spec.md` is carried here and it changes a number.** The
specification writes the payout formula on an **annual** annuity-due,
`연금연액 = 계약자적립액 ÷ ä_n(공시이율) × (1 − 0.005)`, and calls the reconstruction of
the published illustration exact. It is not: on an annual factor the reconstruction misses
all eight published implied factors by about half a per cent, and it misses them *in the
wrong direction*. **The annuity is paid 매월 on every retrieved contract** [S1] [S2] [S5]
[S6] [S7], and the factor is therefore the annuity-due payable twelve times a year. With
that one change the same formula and the same 0.5% charge reproduce all eight published
figures on both interest bases. The correction, and the evidence for it, are in *The
annuitisation transition* below; `Pension_KR_A` implements the corrected form and the
worked example is struck on it.

Parameters introduced **here** that the specification does not carry — each because the
specification defers it, or because it is a modelling construct with no contractual
counterpart — are flagged **new here** at the point of introduction. They are: the
sub-annual timing adjustment `u(t)` and the `(f − 1)/(2f)` annuity correction; the whole
cash-expense and commission set; both lapse vectors; the best-estimate mortality factor and
the Makeham construction that generates `mort_table.csv`; the terminal age ω = 120; the
policy-loan rate, draw year and draw fraction; the payment-holiday start year; the
definitive 표준해약공제액 computation and the reading of 별표 14 주3 it rests on; the
treatment of the 연금수령한도 평가액; and the decision not to round the 연금연액.

---

## Model scope and conventions

- **Purpose.** Project **gross best-estimate liability cash flows** per policy — premiums,
  deferral-phase death benefits, surrender payments, annuity instalments, expenses and
  commission — for a single model point, undiscounted and gross of reinsurance. Korea runs
  **three** measurement bases over one such stream and all three are live: IFRS 17 (K-IFRS
  제1117호, mandatory since 2023-01-01) [REG-R60], K-ICS in the same quarter [REG-R13], and
  the **해약환급금준비금** (surrender-value reserve) that has no counterpart anywhere else
  in this repository [REG-R11]. This model stops deliberately before all three.
  **Discounting, the risk adjustment, the CSM, 요구자본 and every reserve are out of
  scope** and are cited, not reproduced — see *Valuation and reserve pointers*.
- **Projection frequency.** **Annual**, on policy years running 계약해당일 to 계약해당일
  (`Pension_KR_A`). The permission is explicit rather than assumed: 감독규정
  제7-65조제2항 allows the 계약자적립액 of a monthly-premium contract to be computed on an
  annualised premium basis — 「계약자적립액은 … 연납보험료를 기준으로 하여 산출할 수
  있다」 [REG-R18]. This is therefore a filed-basis convention, not a modelling shortcut.
- **What the annual grid approximates [std].** Three things, each named rather than
  hidden. (i) The contract credits interest 「납입일부터 일자계산을 하여」 — by day, from
  the date each of the twelve monthly instalments is received [S1] [S2] — and 감독규정
  제7-66조제1항제4호 accrues the account **monthly before 납입완료 and daily afterwards**;
  both of the regulation's formulas render as images in the 고시 and did not extract
  [REG-R19]. The annual grid carries the difference in one explicit factor, `u(t)`, rather
  than dropping it. (ii) The annuity is paid **매월** [S1] [S2] [S5] [S6] [S7], and the
  annual grid carries one instalment per row; the frequency lives inside the annuity factor
  instead. (iii) The 14-day **납입최고(독촉)기간** collapses into the anniversary
  [REG-R25 제26조](#krlib-reg-r25), so a lapse is dated to the policy year and not to the month, and
  **미경과보험료** — which 제7-66조제5항 requires to be added on termination [REG-R19] —
  is nil on an annual grid with premiums in advance and surrenders at the anniversary.
- **Timing conventions [std].** Premium at the **start** of the policy year, in advance, on
  the in-force cohort; annuity instalments at the **start** of the year, in advance;
  acquisition cash expense at `t = 0`; maintenance cash expense and commission at the start
  of each year; any policy-loan advance at the start of the draw year; death benefits and
  surrender payments at the **end** of the policy year, **deaths before lapses**.
- **Time index.** `t` counts completed policy years since issue, **0-based**, matching
  `product-spec.md`: premiums fall at `t = 0 … m − 1`, the fund accumulates over
  `t = 0 … n` where `n = m + d`, and the annuity is paid from `t = n`. `pols_if(t)` is the
  in-force count at the **start** of year `t` and is the weight on that same `result_cf()`
  row. **`proj_len()` is the last projected index, not a count**: at the anchor cell it is
  80 and `result_cf()` has 81 rows, `t = 0 … 80`.
- **Age basis: 보험나이.** Every age in the contract is 보험나이 (*boheom nai*, insurance
  age): the exact age at the 계약일 with a remainder under six months discarded and six
  months or more rounded up, incrementing on each 계약해당일 [S6 제20조]
  [REG-R25 제21조](#krlib-reg-r25). An annual grid stepped on anniversaries therefore ages the policy
  correctly by construction and the attained age in year `t` is `x + t` exactly.
  **Korea's other convention, 만나이 (age last birthday), governs the two statutory tests
  this product depends on** — one retrieved 약관 states the split in terms, 「이 약관에서의
  피보험자의 나이는 보험나이를 기준으로 합니다. 다만, 연금개시나이가 만 55세 이상에
  해당되는지 여부의 판단은 실제 만 나이를 적용합니다」 [S6 제20조] — and the model reads
  both the 만 55세 test and the withholding age bands off `age(t)`, which is 보험나이. That
  is a **[std]** simplification worth at most one year. It cannot bite at the anchor cell,
  whose annuity date is 65 and clears 만 55세 by a decade; it is exactly the case a model
  point annuitising **on** 55 would test, and model point 6 is that case.
- **Currency.** KRW throughout. Amounts are written ₩ with thousands separators and the
  Korean 만원 / 억원 convention is given alongside where a Korean reader would expect it:
  the anchor cell's fund at annuitisation, ₩160,294,806, is about 1.6억원. `run.py` prints
  `KRW` and pure ASCII.
- **Model points.** Single-policy model points projected on an expected
  (probability-weighted) basis: survivorship and persistency multiply per-policy amounts.
  `point_id` parameterizes `Projection`; **`point_id = 1` is the worked-example anchor
  cell.** Nine points ship. No aggregation logic is specified here.
- **Termination and horizon.** The contract does not mature: **there is no 만기보험금 and
  no maturity date**, because the deferral phase ends by conversion rather than by payment.
  On the 확정기간연금형 form the horizon is `n + k − 1`, the last instalment, and there are
  no tail states. On the 종신연금형 form there is no natural end, so the horizon is the
  terminal age of the annuitant table less the issue age — `proj_len = ω − x` = 120 − 40 =
  80 at the anchor cell, ω = 120 being a **[std, new here]** choice, since no Korean
  industry table publishes a terminal age any more than it publishes its rates
  [REG-R33] [REG-R34].
- **Contract boundary.** The 기본보험료 is level and guaranteed for the whole 납입기간 with
  no review right [S1] [S2] [S4] [S6] [S7], so all `m` premiums sit inside any defensible
  boundary and the model projects them. The harder question on this chassis is the other
  one: the **공시이율 is reset monthly at the insurer's discretion** inside a regulated
  construction [REG-R18] [REG-R24], which is the classic fact pattern for a *direct
  participating* contract under IFRS 17. Whether a 금리연동형 연금저축보험 is measured
  under the variable fee approach is a live question for a Korean reporter and **is
  [unverified] here**: no retrieved document settles it, and this model computes no IFRS 17
  measurement of any kind. What it owes the regime is only that the projection be
  re-runnable on a basis re-set at a stated valuation date.
- **Rounding.** Intermediate values at full double precision. Displayed cash flows and
  per-policy amounts to **two decimal places [std]**, policy counts and rates to ten. That
  is the precision `tests/test_pension_savings_kr.py` asserts. **The 연금연액 is not
  rounded [std, new here]**: no retrieved document gives a contractual rounding step for
  it, unlike the ¥100 step Japanese specimens publish, so `B` is carried unrounded and a
  model that rounds it is making a contractual assertion the sources do not support.
- **Sign convention.** `net_cf` is **income-positive** — premiums less benefits, expenses,
  claim expenses, commission and any loan advanced. That is both these notes' orientation
  and the library-wide one, so there is **no** outgo-positive `liability_cf` companion:
  one stream, one sign, one name. A reader comparing the payout rows with an outgo-positive
  presentation must flip the sign; they are large negatives here.

---

## Model point attributes

| Attribute | Type | Anchor cell (`point_id = 1`) |
|---|---|---|
| `policy_id` | str | `KR-PEN-0001` |
| `sex` | enum {M, F} | M |
| `issue_age` (`x`) | int, 보험나이, 0 – (Y − m) | 40 |
| `premium_term_y` (`m`) | int, years, ≥ 5 | 20 |
| `defer_gap_y` (`d`) | int, years, 납입완료 → 연금개시 | 5 |
| `annuity_start_age` (`Y`) | int, 보험나이, `= x + m + d`, 55–80 | 65 |
| `premium_pp` (`P`) | KRW p.a., level 기본보험료 | 6,000,000 |
| `addl_prem_pp` (`P_a`) | KRW p.a., 추가납입, ≤ 200% of `P` | 0 |
| `payout_form` | enum {life_guar, certain} | life_guar |
| `payout_term_y` (`k`) | int, 확정기간연금형 term | 10 (unused on the life form) |
| `guar_term_y` (`g`) | int, 보증지급기간 | 10 |
| `mort_vintage` | enum {issue, commencement, ratchet} | issue |
| `min_fund_on` | bool, the 100.1% floor applies | true |
| `surr_chg_rate` | float, first-year 해약공제액 ÷ `P` | 0.0 |
| `holiday_years` (`h`) | int, 납입유예 spells of one year | 0 |
| `loan_on` | bool, 보험계약대출 module | false |
| `par` | bool, 배당 (participating) | false |
| `div_rate` | float, declared 계약자배당 rate on the fund | 0.000 |
| `lapse_basis` | enum {pension, savings} | pension |
| `rate_scenario` | enum {base, floor, hybrid} | base |

Six of these are switches on modules that are off in the base run, which is deliberate: the
composite is one contract and the variations are model point values, not code branches.
`annuity_start_age` is **derived rather than free** — the model rejects a model point where
`Y ≠ x + m + d`, because two spellings of one date is how a projection silently annuitises
in the wrong year — and `n`, `prem_end_t` and `proj_len` are derived from it. At the anchor
cell `prem_end_t() = 20`, `annuitisation_t() = 25`, `annuity_age_eff() = 65` and
`proj_len() = 80`.

The anchor premium is not a modelling invention. It is the annualisation of a published
illustration at an identical model point — 남자 40세, 기본보험료 월 500,000원, 20년납,
60세 완납, 65세 개시 [S2] — and it is **exactly the 세액공제 ceiling** of ₩6,000,000 a year
[R1 제59조의3제1항](#krlib-pension_savings-r1) [R8] [R10], so the anchor saver sits on the corner of the tax schedule.
Both facts are what make the calibration below checkable.

---

## State variables

| Variable | Description | Updated |
|---|---|---|
| `pols_if(t)` | Contracts with an obligation open at the start of year `t`; `pols_if(0) = 1` | annual recursion |
| `lives_if(t)` | Probability the annuitant is alive at the start of year `t`; `lives_if(0) = 1` | annual recursion |
| `av_pp(t)` | 계약자적립액 per policy at the start of year `t`, before that year's premium | annual recursion |
| `cv_pp(t)` | 해약환급금 per policy at time `t` | derived from `av_pp` |
| `db_pp(t)` | Death benefit for a death in year `t − 1`, paid at `t` — the fund itself | derived from `av_pp` |
| `cum_prem_pp(t)` | Cumulative 기본보험료 and 추가납입보험료 paid to time `t` | annual recursion |
| `loan_pp(t)` | 보험계약대출 balance per policy; zero in the base run | annual recursion |
| `div_acc_pp(t)` | Accumulated 계약자배당; zero in the base run | annual recursion |
| `annuity_pp(t)` | Instalment payable at the start of year `t`; `B` from `t = n` | fixed at `t = n` |
| `mort_rate(t)` | Best-estimate annual mortality applied in year `t` | assumption lookup |
| `lapse_rate(t)` | Best-estimate annual 해지 rate applied at the end of year `t` | assumption lookup |
| `credit_rate(t)` | Rate the fund is credited with in year `t` | assumption lookup |

**Two in-force measures are carried and they are not interchangeable.** `pols_if` counts
contracts with an obligation open; `lives_if` counts annuitants alive. In the deferral
phase the two separate because a surrender removes a contract without removing a life: at
the anchor cell's annuitisation date `pols_if(25)` = 0.6096911403 against `lives_if(25)` =
0.9657433263. In the payout phase they separate for the opposite reason — inside the
보증지급기간 the instalments are unconditional, so `pols_if` is **flat** while `lives_if`
runs down on the annuitant basis, and on a 확정기간연금형 that holds for the whole term.
Collapsing the two is the most likely way to build this product wrongly, and it is the
first pitfall below.

**`av_pp` is an account, not a reserve, and the model is built that way.** The
계약자적립액 is a contractual balance defined identically across the retrieved 2026-vintage
documents — 「「계약자적립액」이란 순보험료(기본보험료에서 계약체결비용 및 계약관리비용을
뺀 금액)를 「공시이율」로 납입일부터 일자계산을 하여 적립한 금액」 [S1] [S2] — so charges
come off the premium, the remainder is credited at the declared rate, and **nothing else
moves**. There is no net-level-premium structure, no survivorship release and no mortality
in the recursion at all. `cv_pp`, not `av_pp`, is the surrender quantity, as the library's
naming ruling requires; on this composite the two are the same number at every duration,
because the adopted 해약공제액 schedule is zero everywhere, and that is a property of the
adopted schedule rather than of the product.

---

## Assumption inputs

### (a) Contractual / guaranteed elements (cited; the insurer cannot change them)

| Input | Value | Basis |
|---|---|---|
| 기본보험료 `P` | Level, guaranteed for the whole 납입기간; no review right | [S1] [S2] [S4] [S6] [S7] |
| Premium frequency | 월납, 12 instalments a year, in advance | [S1] [S2] [S6] [S7]; annual grid **[std]** |
| Interest accrual on premiums | 「납입일부터 일자계산을 하여」 — by day from receipt | [S1] [S2] |
| 계약체결비용 `α` | **1.50%** of the monthly 기본보험료, policy years 1–7 | [S1] |
| 계약관리비용 `β` | **3.00%** a month while premiums are due; **0.67%** a month after 납입완료, taken from the 적립액 | [S1] [S5] |
| 추가납입 charge | **2.00%**, 계약관리비용 only — the additional premium bears no 계약체결비용 | [S1] [S8] |
| 연금수령기간 관리비용 `θ` | **0.5%** of the 연금연액 | [S1] [S7] |
| 모집수수료 | **0.00% in every year** — a direct-channel product | [S1] |
| 최저보증이율 ladder | **1.25%** to 5 years, **1.00%** to 10 years, **0.50%** after; compound annual | [S1] [S2] [S13] |
| Why a floor exists at all | 감독규정 제7-60조제10호 requires every 금리연동형보험 to set one | [REG-R16] |
| What the floor guarantees | The **credited rate**, not the return: charges are still deducted beneath it | [S4] [S8] |
| 해약환급금 | 계약자적립액 less 해약공제액, **floored at zero** | [S1] [S8] [REG-R19 제7-66조제1항제1호](#krlib-reg-r19) |
| 해약공제액 | **Zero at every duration** on the adopted schedule | [S1] |
| 해약공제기간 cap | The premium term or the acquisition-loading period, **capped at 7 years** | [REG-R19 제7-66조제1항제2호](#krlib-reg-r19) |
| 표준해약공제액 | 연납순보험료 × **3%** (무배당) × min(m, 12), less 주6's discounted loading | [REG-R20 주2·주3·주5·주6](#krlib-reg-r20) [R14] |
| Death benefit before annuitisation | **The 계약자적립액 at the date of death**; the contract then ends | [S1] [S2] [S4] [S6] |
| Death cover above the fund | **None** | [S1] [S2] [S4] [S6] |
| Why none is required | 감독규정 제7-60조제9호 exempts a contract whose premium term ends at 80 or below | [REG-R16 제9호](#krlib-reg-r16) |
| 연금개시일 | The 계약해당일 at which 보험나이 reaches the elected 연금개시나이 | [S1] [S2] [S6] |
| Minimum fund at 연금개시 | **100.1% of premiums paid** | [S2] [S4 별표1 주10] [S7] |
| Why 100.1% | 감독규정 제7-60조제2호 requires a 저축성보험's survival benefits to **exceed** premiums paid | [REG-R16 제2호](#krlib-reg-r16) |
| Floor disapplication | Withdrawn, and the annuity date deferred, where a 납입유예 or a one-instalment reinstatement caused the shortfall | [S4] [S6] [S7] |
| 종신연금형 basis | 연금사망률 **and** 공시이율, per the 산출방법서 | [S1] [S2] [S6] |
| 확정기간연금형 basis | **공시이율 alone** — no mortality, and no survival condition | [S1] [S2] [S6] |
| Annuity frequency | 매월 / 매3개월 / 매6개월, deferred instalments credited at the 공시이율 | [S1] [S2] [S5] [S6] [S7] |
| Death inside the 보증지급기간 | The unpaid guaranteed instalments are paid; commutable at the 공시이율 | [S1] [S2] [S6] |
| Death after the 보증지급기간 | Nothing further; the contract ends | [S1] [S2] [S6] |
| Death during a 확정기간 term | The remaining instalments are paid to the count | [S1] [S2] [S4] [S6] |
| Guaranteed total vs the fund | The guaranteed instalments may total **less** than the fund at annuitisation | [S1] [S2] [S6] |
| Surrender after the first instalment | **Not available** on a 종신연금형 | [S2] [S4 제5조③] [S5] [S9] |
| Contributions after annuitisation | Barred | [R6 제40조의2제2항제2호](#krlib-pension_savings-r6) |
| 연금사망률 ratchet | Where a revision **increases** the annuity, the 연금개시시점 table is substituted | [S1 주6] [S2] [S4 별표1 주11] [S6 별표1 주10] [S9 별표2 주9] |
| Annual contribution ceiling | **₩18,000,000** across every 연금계좌 the saver holds | [R6 제40조의2제2항제1호](#krlib-pension_savings-r6) [R11] [REG-R56] [S1] |
| 계약이전 (transfer out) | Permitted; **not** a withdrawal and not taxed | [S1] |
| Premium waiver (납입면제) | **None** — 「보험료 납입면제 사유 : 없음」 | [S1] |
| Underwriting | None; 전건 무진단 | [S7] |

Two absences in that table are product facts and not omissions. **There is no death cover
above the fund**, so the insurer carries no deferral-phase mortality risk at all and the
death payment equals the surrender payment at every duration; and **there is no premium
waiver**, so there is no disabled-life state to project. Both are asserted by the sources
rather than assumed, and both are testable properties of the model.

### (b) Insurer-discretionary current elements

| Input | Base-run value | Basis |
|---|---|---|
| 공시이율 `i(t)` | **2.15% p.a.**, level at every duration | [S2]; adoption **[std]** (1) |
| — how it is set | 공시기준이율 (외부지표금리 × α + 운용자산이익률 × (1−α), α ≤ 60%) ± 조정률, reset monthly, fixed for the calendar month | [S1] [S2] [S4 제6조①②] [REG-R18] [REG-R24] |
| — the 조정률 | **Not modelled**: a discretionary margin whose range lives in an unpublished 사업방법서 | [S1] [S8]; scope **[std]** |
| Credited rate `i_c(t)` | `max(i(t), i_min(t))` = **2.15%** at every duration; the floor never binds in the base run | derived |
| 예정이율 `i'` | **2.50% 연복리** — prices the charge and benefit structure; **not a guarantee, not a crediting rate**, and it appears nowhere in the fund recursion | [S1] [S5] [S7] |
| 평균공시이율 | **2.50%** for 2026 — a supervisory average; enters only as a constraint, inside the 표준해약공제액 | [REG-R48] [S14] [REG-R9 제1-2조제13호](#krlib-reg-r9) |
| Annuity-phase charge `θ` | **0.5%** of the 연금연액 — a carrier choice, not a market convention | [S1] [S7]; adoption **[std]** (2) |
| Annuitant table vintage | Held at the **가입시점** table; the ratchet is carried and is out of the money | reading `[derived]` [S1] [S2]; **[std]** (3) |
| 해약공제액 schedule | The direct-channel product's, **zero at every duration** | [S1]; adoption **[std]** (4) |
| — the alternative | The postal insurer's front-end 해지공제액, ₩104,000 on a ₩1,200,000 annual premium (**8.67%**), running off to zero at year 5 | [S7]; model point 8 |
| 계약자배당 | **Zero declared.** Machinery retained: credit on the fund, accumulate at the 공시이율, apply at `t = n` as an 증액연금, never in cash | [S2] [S7]; zero base run **[std]** (5) |
| 배당 accumulation rate | 2.15%, the 공시이율, where a dividend is run | [S2]; **[std]** |
| 보험계약대출이율 | **4.00%** where the module is on | **[std] [unverified], new here** (6) |
| 납입유예 | Module off; up to three spells of one year, charges still taken from the fund | [S5] [S7] [S8]; scope **[std]** |

1. The observed range of declared rates on 연금저축 books is roughly **2.1% to 3.0%** —
   3.01% and 2.82% at one carrier on 2026-09-01 [S12], 2.40% at 2026-01 [S1], 2.15% at
   2025-12 [S2], 2.3% at 2024-10 [S11] — with a 19-basis-point spread between two vintages
   inside one carrier on one date [S12] `[derived]`. The composite takes **2.15%**, the
   conservative arm and the rate on which the anchor illustration and every derived annuity
   factor are struck [S2]: it is the only choice under which the published fund, the
   published annuities and the reconstructed factors form one consistent set. The rate is
   modelled as a **step function of policy year**, level in the base scenario, because a
   Korean declared rate is majority-weighted to the insurer's own realised investment
   return and moves slowly: one carrier's published thirteen-month history falls 57 basis
   points in steps of two to seven, never once reversing [S5] `[derived]`. **It is not a
   market rate and must not be modelled as one.**
2. Two carriers disclose 「연금수령기간 중의 관리비용: 연금연액의 0.5%」 [S1] [S7]; a
   third discloses none and its implied factors run about 0.6% the other way [S5]
   `[derived]`. The composite takes 0.5% because it is the value that makes the payout
   formula reconstruct eight published figures on two interest bases (below).
3. Six independently retrieved contracts carry the same one-way ratchet clause and none
   states the base vintage, so the reading that the base factor is the **가입시점** one is
   `[derived]`, corroborated by two carriers publishing the 연금사망률 in the 상품요약서
   handed over at inception [S1] [S7] and by trade reporting that a 경험생명표 revision
   applies to new business only [R18] [R20]. Because revisions have **lightened** mortality
   — the 제10회 raised 평균수명 by 2.8 years for men and cut the monthly annuity on a fixed
   fund by roughly 15% [R18] [R19] [REG-R33] — a revision normally *reduces* the annuity
   and the ratchet does not bite. Model point 9 confirms it numerically:
   `mort_table_name()` returns `annuitant_issue` even though the vintage is `ratchet`.
4. The composite pairs the **only complete published expense schedule** [S1] with the
   **only complete published annuitisation illustration** [S2], and those are two different
   products of the same carrier. The consequence is stated openly: the composite's
   early-duration surrender values look like the direct-channel product's (96.6% of
   premiums after one year) and **not** like the tied-channel product's (82.7%), even
   though the anchor model point is taken from the latter [S1] [S2].
5. No retrieved carrier publishes a dividend **rate** on a 연금저축보험, which is one of
   the two reasons the composite is 무배당; the other is that 별표 14 주5 gives a 무배당
   연금저축보험 the **tighter** surrender-charge coefficient, 3% against 4% [REG-R20]
   [R14], so the composite states the tighter constraint.
6. **No retrieved document gives a numeric 보험계약대출이율 for a 연금저축보험** [S1] [S2]
   [S4] [S5]. The module is off in the base run for exactly that reason; switching it on
   switches on an invented rate, and the model says so on the cells.

### (c) Behavioral / experience assumptions (modeler's view — all [std])

**Mortality — one table, on the annuitant basis, and it is a construction.** 경험생명표
(*gyeongheom saengmyeongpyo*, the industry experience table), currently the 제10회 applied
to new business from 2024-04, is produced by 보험개발원 under the statutory office of
보험요율산출기관, 보험업법 제176조, which carries **no publication obligation**
[REG-R4] [R16]. What is public is the summary — 평균수명 남 86.3세 / 여 90.7세 and
65세 기대여명 남 23.7년 / 여 27.1년 [REG-R33] [R18] — and not the rates; the KIDI press
page is JavaScript-driven and the release could not be opened [R17] [REG-R34], and the
big-data portal refused connections [R24]. **`mort_table.csv` is therefore a [std]
construction with a `provenance` column on every row, and it is never presented as the
경험생명표.** It ships with its recipe, in three parts, all recorded in
`mort_anchor_table.csv` and re-derived by `check_mort_law()`:

    mu(x) = A + B c**y,   q(x) = round(1 - exp(-mu(x)), 8),   y = max(0, x - setback)

| Part | Value | Status |
|---|---|---|
| Makeham `A` | 5.5583e−04 | **[std, new here]** |
| Makeham `B` | 2.3281e−06 | **[std, new here]** |
| Makeham `c` | 1.108956 | **[std, new here]** |
| Female table | The male law **set back 4 years** | **[std, new here]** |
| `annuitant_revised` vintage | The issue vintage × **0.85** | **[std, new here]** |
| Terminal age ω | **120**, both sexes and both vintages | **[std, new here]** |

The law is fitted **jointly** to the six annuitant rates two carriers publish in their
statutory product summaries — 「연금사망률」 at ages 50/60/70 [S1] and 「개인연금사망률」 at
40/60/80 [S7] — and to the annuity factors the one published annuitisation illustration
implies at **two** interest bases [S2]. A three-parameter law cannot honour both, and the
residuals are recorded rather than smoothed: on the male table the fitted rate runs about
1.30× the published rate at 70 and 0.72× at 80, and the female table, being a setback
rather than an independent fit, runs 1.9 to 2.8 times the published female rates over ages
50 to 70. An
independent female fit was **tried and rejected**, because it produces a female annuity
*larger* than the male's at the same age, which no carrier's rate card does: the sourced
sex differential beat the sourced female rates, and both facts sit on the file's provenance
rows.

**What the construction says about longevity, stated rather than hidden.** On the shipped
male table the curtate expectation at 65 is **33.31 years**, against the 제10회's published
23.7 [REG-R33]; the female table gives 36.97, a gap of **3.66 years** against a published
3.4. The first number is not a mistake and it is not this library's invention: solving
`ä_n = 23.70` at 2.15% gives `n ≈ 32.5`, so the published life annuity **is** priced as if
a 65-year-old male lived to about 97 [S2] `[derived]`. That is what a 연금사망률 loaded on
the *survival* side looks like when it is read back off a published annuity, and the table
reproduces the annuity because the annuity is what it was fitted to.

**The best-estimate factor, and why its sign is the opposite of a death product.**
`mort_rate(t) = min(1, 1.15 × table rate)` **[std, new here]**. Greater than one, and the
direction is the point: the published 연금사망률 is a **pricing** basis for a longevity
liability, so it is loaded on the survival side and a best-estimate death decrement runs
**heavier** than the table, not lighter. The size is a standardization — the only direct
evidence of the margin is that the two carriers publishing annuitant rates differ by about
9% at age 60 (0.00150 against 0.00164 for men) [S1] [S7] `[derived]`, and 1.15 sits a
little above that. A model that carries a death product's downward adjustment here has the
sign wrong.

**The table is used in exactly two places** — the annuity factor at the 연금개시일, and the
in-force decrement — and it **must not be shared with `WholeLife_KR_A`**: one table is
loaded for survival and the other for death, and using either for both is wrong in a known
direction.

**Lapse — argued, not fitted [std, new here].** There is **no public Korean lapse statistic
for 연금저축보험 by policy year**: one carrier's regulatory disclosure carries a
경과기간별 중도해지율 column in which every row reads 「적용안함」 [S13], the supervisor's
comparison table could not be opened [S19], and the behavioural tables in the 2025
whitepaper sit in attachments that did not convert [R13]. The reference vector is therefore
**[std]** and is argued from the contract:

| Policy year `t` | 0 | 1 | 2 | 3–4 | 5–9 | 10 – (m−1) | m … n−1 | ≥ n |
|---|---|---|---|---|---|---|---|---|
| `lapse_rate(t)`, `pension` **[std]** | 4.0% | 3.5% | 3.0% | 2.5% | 2.0% | 1.5% | 1.0% | 0% |
| `lapse_rate(t)`, `savings` **[std]** | 8.0% | 7.0% | 6.0% | 5.0% | 4.0% | 3.0% | 2.0% | 0% |

Four features are load-bearing. The vector is **materially flatter than a non-qualified
savings contract's**, which the second row carries so the two can be run side by side: a
surrender costs **16.5% 기타소득세** on essentially the whole payout once the contributions
have been credited [S5] [S8] `[derived]`, a frictional cost nothing else in this repository
has. It steps **down** at 납입완료 rather than up, because the commonest lapse trigger — a
premium falling due — is absent between 납입완료 and 연금개시. It is **zero from `t = n`**
and not from `t = n − 1`: surrender is available right up to the day before the 연금개시일
[S2] [S4], so the decrement runs through year `n − 1` and the contracts leaving there are
paid `CV(n)`, a real payment of the full fund. And it is **net of 부활** by construction,
because reinstatement is not implemented on an annual grid.

It is deliberately **not** the supervisory 무·저해지 lapse guidance — the log-linear decay
to 0.1% at 납입완료 of the 제4차 보험개혁회의 [REG-R27] — which is calibrated to
순수보장성 and 무해지 protection business. This product is neither: it has a full surrender
value from the first month and no cliff at 납입완료. That guidance is the shape a Korean
supervisor expects a lapse curve to have; it is not this product's numbers.

**Expenses and commission (all levels [std, new here]; structure conventional).**

| Input | Value |
|---|---|
| Acquisition cash expense `E0` | ₩200,000 per policy at `t = 0` |
| Maintenance cash expense `e(t)` | ₩30,000 p.a. in deferral, ₩20,000 p.a. in payment |
| Expense inflation `π` | 2.0% p.a. flat, applied as `(1 + π)^t` |
| Claim expense `ec` | ₩30,000 per death claim, deferral only |
| Initial commission `c0` | **0.00%** of premium |
| Renewal commission `c_r` | **0.00%** of premium |

These are best-estimate **cash** expenses and are entirely separate from the 계약체결비용
and 계약관리비용 of class (a), which are contractual loadings living **inside** `av_pp`.
Charging the loadings against the cash flow, or projecting these into the fund,
double-counts expense in one direction and destroys the fund calibration in the other. The
commission rows are zero because the source product's published 모집수수료율 is 0.00% in
every year [S1]; `commissions()` is retained and returns zero, because a zero states the
fact where a missing column would hide it.

**Option take-up.** Annuitisation form: **100% 종신연금형 with a ten-year guarantee**
[std], the composite's base election; the 확정기간연금형 alternative runs at model points 4,
5 and 6. Commutation of unpaid guaranteed instalments: **0% [std]** — the base run assumes
**continuation at 100%**, under which death inside the guarantee leaves the instalment
stream unchanged. 부활 / 간편부활, 계약이전, 의료비인출, the six 부득이한 사유 withdrawals
and 배우자 승계 are **out of scope [std scope]**: each is a real contract term with a real
tax effect, and no public frequency exists for any of them.

---

## Cash flow components and recursions

### Notation

| Symbol | Meaning |
|---|---|
| `t` | policy year, 0-based; attained 보험나이 in year `t` is `x + t` |
| `x`, `m`, `d`, `h` | 가입나이; 납입기간; the 납입완료 → 연금개시 gap; 납입유예 length |
| `n` | `= m + h + d`, the policy year of the 연금개시일 |
| `k`, `g` | 확정기간연금형 term; 보증지급기간 of the 종신연금형 |
| `P`, `P_a` | annual 기본보험료; annual 추가납입보험료 |
| `α(t)`, `β(t)` | 계약체결비용 rate; 계약관리비용 rate, both on the 기본보험료 |
| `θ` | 연금수령기간 관리비용, 0.5% of the 연금연액 |
| `i(t)`, `i_min(t)` | 공시이율; 최저보증이율 |
| `i_c(t)` | credited rate, `max(i(t), i_min(t))` |
| `f` | instalment frequency, 12 for both premiums and annuity |
| `u(t)` | sub-annual premium timing factor (`prem_timing_factor`) |
| `NP(t)` | premium credited to the fund (`prem_to_av_pp`) |
| `C(t)` | charge taken **from the fund** where no premium bears it (`charge_from_av_pp`) |
| `AV(t)` | 계약자적립액 at the start of year `t`, before that year's premium (`av_pp`) |
| `SC(t)`, `SC_max` | 해약공제액; the 표준해약공제액 cap (`surr_chg_pp`, `surr_chg_cap_pp`) |
| `CV(t)`, `DB(t)` | 해약환급금; death benefit (`cv_pp`, `db_pp`) |
| `G` | 100.1% minimum fund at the 연금개시일 (`min_fund_pp`) |
| `F` | 연금개시시점 계약자적립액 after the floor (`annuity_fund_pp`) |
| `ä` | the annuity-due factor the annuity is bought at (`annuity_due_factor`) |
| `B` | 연금연액, struck once at `t = n` (`annuity_amount_pp`) |
| `q(t)`, `w(t)` | best-estimate mortality; best-estimate 해지 rate |
| `l(t)`, `L(t)` | `pols_if(t)`; `lives_if(t)` |
| `D(t)`, `W(t)` | expected deaths; expected surrenders in year `t` |
| `E0`, `e(t)`, `ec` | acquisition, maintenance and claim cash expense |
| `CF(t)` | net cash flow of year `t`, insurer perspective, **income-positive** (`net_cf`) |

Dimensional check: `q`, `w`, `α`, `β`, `θ`, `u`, `i` are dimensionless; `P`, `AV`, `CV`,
`DB`, `F`, `B`, `E0`, `e`, `ec` are KRW; `ä` is dimensionless (years of income per unit of
annual income); `l` and `L` are probabilities. `B = F(1 − θ)/ä` is therefore KRW per year,
and because the annual grid carries exactly one instalment per row, no month count ever
enters a cash flow — the twelve-per-year structure is carried entirely inside `u(t)` on the
way in and inside `ä` on the way out.

### Processing order

Within policy year `t`, in this order. The order is part of the specification, not an
implementation detail: three of the pitfalls below are order errors.

1. **Premium**, `(P + P_a) · l(t)` at the **start** of the year, if a premium is due —
   that is, `t < m + h` and not inside a payment holiday.
2. **Annuity instalment**, `B · l(t)` at the **start** of the year, if `t ≥ n`. Paid in
   advance, so the row `t = n` carries an instalment.
3. **Acquisition cash expense** at `t = 0`; **maintenance cash expense** at the start of
   every year, inflated by `(1 + π)^t` and weighted by `l(t)`; **commission** at the start
   (nil on this composite).
4. **Policy-loan advance** at the start of the draw year (nil in the base run).
5. **Fund roll-forward**, `AV(t+1) = (AV(t) + NP(t) − C(t))(1 + i_c(t))`. **No mortality
   and no lapse appear here.**
6. **Death, at the end of the year, from the whole opening in-force**: `D(t) = l(t) q(t)`,
   paid `DB(t+1) = AV(t+1)` net of any loan, plus a claim expense `ec · D(t)`.
7. **Surrender, at the end of the year, from the survivors of mortality** — **death before
   lapse [std order]**: `W(t) = (l(t) − D(t)) w(t)`, paid `CV(t+1)` net of any loan.
8. **Roll to `t + 1`**: `l(t+1) = (l(t) − D(t))(1 − w(t))` in deferral, and the payout-phase
   rules below from `t = n`; `L(t+1) = L(t)(1 − q(t))` throughout.

**At `t = n` exactly**, five things happen in one step and in this order: the fund is fixed
and floored; `B` is struck, once, and never recomputed; `lapse_rate` and the deferral death
decrement go to zero; the first instalment is paid at the **start** of that same year; and
`AV`, `CV` and `DB` become zero from `t = n + 1`. So the row `t = n` carries an annuity
payment and no premium, no death benefit and no surrender.

### The premium, its two charges, and the timing factor

    NP(t) = [ P (1 - alpha(t) - beta(t)) + P_a (1 - 0.02) ] * u(t)      for t < m + h
          = 0                                                          otherwise

    u(t) = (1/f) * sum_{j=0..f-1} ( 1 + i_c(t) )^(-j/f)

`u(t)` **[std, new here]** values the twelve monthly instalments of a policy year as one
start-of-year payment. It is 0.990316187680581 at 2.15%, so an annual premium credited at
the start of the year without it would earn about half a year of interest too much — worth
roughly ₩60,000 a year of fund at the anchor cell. The same factor multiplies the monthly
charges taken from the fund, which are monthly for the same reason.

**The charges come off the premium, not off the fund, while premiums are being paid** —
「동 이율은 납입한 주계약(또는 적립) 보험료에서 계약체결·유지관리에 필요한 경비 … 를
차감한 금액에 대해서만 적용됩니다」 [S4] [S6] — and there is no risk premium to deduct,
because there is no cover above the fund. That is what gives an insurance-wrapper pension
its negative early-duration return, and the supervisor says so in terms [R12].

**The 계약체결비용 stops after seven years and the 계약관리비용 does not stop at
납입완료.** Both are visible in the model as steps: `NP(t)` rises from ₩5,674,511.7554 to
₩5,763,640.2123 at `t = 7`, and from `t = m + h` the fund starts paying

    C(t) = P * beta_paid_up * u(t)                                     for m + h <= t < n
         = P * ( alpha(t) + beta_premium_paying ) * u(t)               during a 납입유예
         = 0                                                           for t >= n

which is ₩39,810.7107 a year at the anchor cell, taken from the 적립액 with no premium
arriving — 「보험료 납입 완료 후에는 월계약해당일에 계약관리비용 중 유지관련비용(납입후)을
적립액에서 차감합니다」 [S5] [S1]. Zero once the annuity is in payment, where the charge is
the 0.5% already inside the annuity factor.

### The 계약자적립액 recursion

    AV(0)   = 0
    AV(t+1) = ( AV(t) + NP(t) - C(t) ) * ( 1 + i_c(t) )        for t = 0 .. n-1
    AV(t)   = 0                                                for t > n

**There is no mortality in this recursion and there is no lapse in it.** The fund is a
contractual balance and the death benefit *is* the balance, so there is no survivorship
release to credit and no death strain to subtract; and the surrender release that a
deduction would produce is nil, because the 해약공제액 is nil. This is the single largest
structural difference from the deferred annuity on the Japanese page of this repository,
whose fund divides by `(1 − q')` each year and pays a **larger** annuity out of the same
premium as a result. A model that ports that shape here does not fail loudly: it silently
overstates the 연금개시 fund. `check_av_roll_fwd()` asserts the recursion above over the
whole deferral phase, and it is the check that would catch it.

The accumulation cross-check against the published illustration closes. Rolling that
carrier's published year-20 surrender value forward the five years of the gap at the stated
rate gives ₩140,811,363 × 1.0215⁵ ≈ ₩156,600,000 against a published ₩156,420,000, and
₩120,595,257 × 1.005⁵ ≈ ₩123,640,000 against a published ₩123,460,000 [S2] `[derived]` —
both residuals ₩180,000, of the order of five years of the post-payment maintenance charge
(0.67% × ₩500,000 × 60 = ₩201,000) [S1]. **The accumulation is a plain roll-forward at the
declared rate net of a small level charge, with no other moving parts.**

### Deferral-phase benefit amounts, and the statutory cap

    SC(t) = min( surr_chg_rate * P * max(0, (5 - max(t,1)) / 4), SC_max )
    CV(t) = max( 0, AV(t) - SC(t) )        for t <= n,   and 0 for t > n
    DB(t) = AV(t)                          for t <= n,   and 0 for t > n

`CV`'s zero floor is 감독규정 제7-66조제1항제1호 written out — 「계약자적립액에서
해약공제액을 공제한 금액이 음(陰)의 값인 경우에는 이를 영(零)으로 처리한다」 [REG-R19] —
and `check_cv_floor()` asserts it at every duration. On the composite `SC(t) = 0` at every
duration [S1], so **`CV(t) = AV(t) = DB(t)`**: death and surrender pay the same amount and
the two decrements differ in their rate, not in their payment. The run-off shape in `SC`
is the postal insurer's, first-year amount falling linearly to zero at the fifth policy
year [S7], and it is exercised at model point 8.

**The 표준해약공제액, computed in full.** 별표 14 gives 표준해약공제액 = 연납순보험료의 5%
× 해약공제계수 + 보장성보험의 보험가입금액의 10/1000, with 주2 setting the 저축성보험
coefficient at the premium term **capped at 12**, 주3 defining the 연납순보험료 as the
annual premium less the average loading spread evenly over the payment term **capped at
10 years**, 주5 replacing the 5% with **4% for a 연금저축보험 and 3% if 무배당**, and 주6
subtracting the acquisition amount loaded into the premium **discounted at the
평균공시이율** [REG-R20] [R14]. 주4's 6% concession for a whole-of-life survival annuity is
expressly **denied** to this product, and the second term of the formula is nil because the
contract has no 보장성 element. At the anchor cell:

| Step | Arithmetic | Value |
|---|---|---|
| Whole-term loading | ₩6,000,000 × (0.045 × 7 + 0.030 × 13) | ₩4,230,000.00 |
| Levelled over min(m, 10) | ₩4,230,000 ÷ 10 | ₩423,000.00 |
| 연납순보험료 (주3) | ₩6,000,000 − ₩423,000 | ₩5,577,000.00 |
| Gross cap (주2, 주5) | 3% × ₩5,577,000 × min(20, 12) | ₩2,007,720.00 |
| 주6 deduction | Σ ₩90,000 ÷ 1.025^s, s = 0…6 | ₩585,731.28 |
| **표준해약공제액** | | **₩1,421,988.72** |

That is about **2.8 months of 기본보험료**, the order of magnitude 금융위원회 stated for a
저축성보험 in 2019 [REG-R29]. **The composite uses none of it**, and that is the finding:
the regulator has singled this product out for the tightest coefficient in the schedule and
the reference implementation sits far inside it. The composite's whole acquisition cost —
1.50% × ₩500,000 × 84 = ₩630,000 — is itself inside the cap, which is a coherent
explanation of why the source product's published 해약공제 table is all zeros [S1].
`check_surr_chg_cap()` asserts `SC(t) ≤ SC_max` at every duration on every model point,
including the one carrying a real front-end charge.

**The reading of 주3 is a choice and it moves the number [std, new here].** The
computation above levels the **whole term's** loading over the ten-year cap. The
alternative reading — levelling only the first ten years' loading, ₩2,430,000 ÷ 10 =
₩243,000 — gives a 연납순보험료 of ₩5,757,000, a gross cap of ₩2,072,520 and a
표준해약공제액 of **₩1,486,788.72** `[derived]`, 4.56% higher. Neither is excluded by the
text. The model implements the first and the alternative is a one-line change; the cap
binds nothing on this composite either way, which is why the choice can be stated openly
rather than defended.

### The annuitisation transition

At `t = n` the fund is fixed, floored, and divided by a factor.

**The floor.** `G = 1.001 × cum_prem_pp(n)`, and `F = max(AV(n), G)`. Three retrieved
contracts guarantee it in those words — 「연금개시시의 계약자적립액은 이미 납입한 보험료의
100.1%를 최저보증 합니다」 [S4 별표1 주10] [S2] [S7] — and two more write the functionally
identical 「이미 납입한 보험료 + 1,000원」 [S5] [S6]. The base is **premiums paid**, basic
and additional together, because 「이미 납입한 보험료」 is the whole contribution. It is a
**survival** guarantee: a death claim in deferral is not floored at premiums paid on this
composite, so the floor is payable only to a policy that reaches the 연금개시일 in force.
It is not decorative — on the published guaranteed-rate illustration the fund reaches only
**100.5%** of premiums at the end of the twenty-year payment term [S2], so on a
persistently low-rate path the floor is close to binding, and it is the only element of
this contract that behaves like an option rather than an account. Model point 6 is the
demonstration: on the guaranteed-rate scenario its fund at annuitisation is **exactly
₩30,030,000 = 100.1% × ₩30,000,000**, the floor and not the interest. `check_min_fund()`
asserts `F ≥ G` where the guarantee applies, and model point 9 carries it **withdrawn**,
which is what the contracts do where a 납입유예 or a one-instalment reinstatement caused the
shortfall — they defer the annuity date instead [S4] [S6] [S7].

**The factor, and the correction to `product-spec.md`.** The 확정기간연금형 is priced on
the declared rate alone — 「연금개시시점의 계약자적립액을 기준으로 공시이율을 적용하여 …
계약자가 선택한 확정된 연금지급기간 동안 나누어 계산」 [S1] [S2] [S6] — and the 종신연금형
on the 연금사망률 **and** the declared rate [S1] [S2] [S6]. Both instalments are paid
**매월**. The factors are therefore annuities-due payable `f = 12` times a year:

    adue_certain = ( 1 - v**k ) / d_f,       d_f = f * ( 1 - (1 - d)**(1/f) ),  d = i/(1+i)

    adue_life    = sum_{j>=0} max( 1{j < g}, jp_(x+n) ) * v**j  -  (f - 1) / (2 f)

    B            = ( F_net / adue ) * ( 1 - theta )

with `v = 1/(1 + i_c(n))`, survival on the annuitant table at **100%** — a pricing basis,
not the best-estimate one — and `(f − 1)/(2f) = 11/24` the standard correction for
instalments payable `f` times a year **[std, new here]**. `F_net` is `F` plus any
accumulated 계약자배당 and less any outstanding 보험계약대출; both are zero in the base run.

**`product-spec.md` writes this on an *annual* annuity-due and that is wrong.** The
evidence is that the monthly form reconstructs every published figure and the annual form
reconstructs none of them. [S2] publishes one fund at annuitisation and five annuities on
each of two interest bases; dividing the fund by the annuity gives the implied factor the
carrier actually used:

| Form | Published implied factor | Model | Interest basis |
|---|---|---|---|
| 확정기간 10년 | 9.06 | **9.061** | 공시이율 2.15% |
| 확정기간 15년 | 12.92 | **12.918** | 2.15% |
| 확정기간 20년 | 16.39 | **16.386** | 2.15% |
| 확정기간 10년 | 9.81 | **9.806** | 최저보증 0.50% |
| 확정기간 15년 | 14.53 | **14.528** | 0.50% |
| 확정기간 20년 | 19.13 | **19.134** | 0.50% |
| 종신 10년보증, 남 65 | 23.70 | **23.700** | 2.15% |
| 종신 10년보증, 남 65 | 31.18 | **31.180** | 0.50% |

`[derived]` from [S2]. **Eight published figures, one formula, two interest bases and both
annuity forms.** On the annual reading the certain factors come out at 9.104 / 12.978 /
16.464 at 2.15% — larger than the published ones, so the reconstructed annuity is *smaller*
than the published annuity, and the 0.5% charge makes the gap worse rather than better.
The specification's footnote records the discrepancy as a uniform 0.995 at 2.15% and an
unexplained 1.003 at the guaranteed rate "running the other way" and tells the reader not
to over-read it. There is nothing to over-read: **it is the monthly instalment**, and once
the factor is `ä^(12)` the 0.5% charge falls out with the same sign on both bases.

**Which vintage the life factor is struck on** is `mort_vintage`. `issue` is the composite
and the base run; `commencement` strikes it on the 연금개시시점 table; `ratchet` implements
the contractual clause itself, evaluating both and taking whichever gives the **larger**
annuity — the smaller factor — because the clause bites only where a revision *increases*
the annuity. Since revisions have lightened mortality, the ratchet is out of the money and
returns the issue vintage; model points 7 and 9 exercise the other two readings.

### The payout forms

**종신연금형 with a 보증지급기간 (base form).** Instalments are unconditional for `g` years
and life-contingent after:

    pols_if(t) = pols_if(n) * max( 1{t - n < g}, L(t) / L(n) )        for t > n

on the best-estimate annuitant basis, so `pols_if` is **flat** through the guarantee and
then runs off. Death inside the guarantee pays the unpaid guaranteed instalments and the
base run assumes **continuation at 100% [std]**, under which the stream is unchanged; the
contract warns that the guaranteed total may come to **less** than the fund at
annuitisation [S1] [S2] [S6], and at the anchor cell it does — `10B` = ₩67,633,745.89
against `F` = ₩160,294,805.59, 42.19% of it. `pols_death(t)` in this phase is the run-off
of `pols_if` itself and **carries no cash flow**: `db_pp(t) = 0` for `t > n`, so
`claims_death` is zero from `t = n` even where `pols_death` is not.

**확정기간연금형 (module).** `k` unconditional instalments at `t = n … n + k − 1`, so

    pols_if(t) = pols_if(n)   for n <= t < n + k,   and 0 at t = n + k

while `lives_if` continues to run down. `pols_death(t) = 0` throughout the term and
`pols_maturity(t) = pols_if(t)` in the final year — the count reaching the scheduled end of
the contract, which the in-force roll-forward needs because those survivors neither die nor
surrender. **There is no `claims(t, "MATURITY")` on this product**, and the absence is a
product fact: 연금저축보험 has no maturity benefit and no maturity date.

`check_annuity_total()` asserts that the guaranteed instalments are level and total `gB` on
the life form and `kB` on the certain form. A model that had decremented the guaranteed
period by mortality, or recomputed `B` after the 연금개시일, fails it.

### In-force recursion

    l(0)   = 1
    l(t+1) = ( l(t) - D(t) ) * ( 1 - w(t) )          for t < n   (death before lapse)
    L(t+1) = L(t) * ( 1 - q(t) )                              throughout
    D(t)   = l(t) * q(t)          for t < n;  the payout-phase rules above from t = n
    W(t)   = ( l(t) - D(t) ) * w(t)   for t < n;   0 from t = n

### Net cash flow

    CF(t) = (P + P_a) * l(t) * 1{premium due}                     (premiums)
          - B * l(t) * 1{t >= n, in payment}                      (claims_annuity)
          - DB(t+1) * D(t)                                        (claims_death)
          - CV(t+1) * W(t)                                        (claims_lapse)
          - ec * D(t)                                             (claim_expenses)
          - ( E0 * 1{t = 0} + e(t) * (1 + pi)**t ) * l(t)         (expenses)
          - commission                                            (commissions, nil)
          - loan advance                                          (policy_loans, nil)

**Nothing in the tax layer appears here.** The 세액공제 is a payment from the state to the
saver and the 기타소득세 is a withholding from the saver's proceeds; neither passes through
the insurer's account, and folding either in would misstate the liability in a way no
reconciliation would catch. The tax quantities are published in `result_tax()` instead, and
`check_net_cf()` — which asserts that the published columns sum to `net_cf` in every year —
is the check that would fail if anyone added one.

**The nine checks**, each taking no argument and returning a `bool`, with the signed
per-`t` residual at `<name>_resid(t)`:

| Cells | Identity asserted |
|---|---|
| `check_pols_roll_fwd` | `l(t) − l(t+1) − D(t) − W(t) − pols_maturity(t) = 0` |
| `check_av_roll_fwd` | `(AV(t) + NP(t) − C(t))(1 + i_c(t)) − AV(t+1) = 0` over the deferral |
| `check_cv_floor` | `CV(t) = max(0, AV(t) − SC(t))` — 감독규정 제7-66조제1항제1호 [REG-R19] |
| `check_surr_chg_cap` | `SC(t) ≤ 표준해약공제액` — 별표 14 [REG-R20] |
| `check_min_fund` | `F ≥ 100.1% × premiums paid` where the guarantee applies |
| `check_annuity_total` | the guaranteed instalments are level and total `gB` (or `kB`) |
| `check_annuity_limit` | no instalment exceeds the 연금수령한도 [R6 제40조의2제4항](#krlib-pension_savings-r6) |
| `check_mort_law` | every shipped rate equals the stated [std] Makeham construction |
| `check_net_cf` | the published columns sum to `net_cf` in every year |

All nine are `True` on all nine model points.

### Optional modules (all off in the base run)

| Module | Switch | What it changes | Model point |
|---|---|---|---|
| 확정기간연금형 | `payout_form` | Factor on the declared rate alone; `pols_if` flat for `k` years; `pols_maturity` in the last year | 4, 5, 6 |
| Mortality vintage | `mort_vintage` | The table the life factor is struck on; `ratchet` takes the larger annuity | 7, 9 |
| 100.1% floor withdrawn | `min_fund_on` | `G = 0`; the annuity date is deferred instead | 9 |
| 연금저축추가납입특약 | `addl_prem_pp` | An additional premium bearing 계약관리비용 only, inside the 200% and ₩18,000,000 caps | 8 |
| Front-end 해지공제액 | `surr_chg_rate` | `CV` separates from `AV` for five years | 8 |
| 납입유예 | `holiday_years` | Premiums suspended, charges still taken from the fund, `n` deferred by `h` | 9 |
| 보험계약대출 | `loan_on` | Half the 해약환급금 drawn at year 15 at a [std] 4.00%, deducted from `DB`, `CV` and `F` | 9 |
| 계약자배당 | `par`, `div_rate` | Credits and accumulates a dividend, applied at `t = n` as an 증액연금; moves 별표 14's coefficient from 3% to 4% | 9 |

---

## Policyholder behavior modeling

All dynamic constructions are **[std]** reference forms; calibration evidence is cited
where any exists, and on this product very little does.

- **Base lapse [std].** The `pension` vector of class (c). On the anchor cell its
  count-weighted mean over the deferral phase — `Σ l(t) w(t) ÷ Σ l(t)`, `t = 0 … n − 1` —
  is **1.9225%**, and the same curve weighted by `av_pp` instead averages **1.4025%**
  `[derived]` from the model, because lapse is front-loaded and the fund is back-loaded.
  The two weightings are not interchangeable and any future calibration must say which it
  means. Over the whole deferral phase **39.03% of policies leave before annuitisation**,
  of which 36.51 points are surrenders and 2.52 points are deaths.
- **The tax layer is the behavioural model on this product, and it has a sign change.**
  The saver took a credit of 16.5% of contributions on the way in and pays 16.5% of the
  surrender value on the way out, so the **net** tax cost of surrendering is
  `16.5% × (해약환급금 − cumulative contributions)` `[derived]`: *negative* while the
  환급률 is under 100% and positive after. On the model's own numbers that is
  **−₩33,575.23** at `t = 1` and **+₩42,223.98** at `t = 5` — the tax turns against the
  surrendering saver at almost exactly the duration at which the expense loading stops
  hurting. The two frictions do not overlap; they hand off. That is the whole argument for
  a lapse vector that is flat rather than steeply front-loaded, and it is why the `savings`
  vector is carried as a comparison rather than as this product's basis.
- **The 16.5% charge falls on essentially the whole payout**, not on the gain. The base is
  the credited money and its return [S8], but on a contract whose contributions were all
  inside the ₩6,000,000 credit cap that is nearly everything: one carrier's surrender
  illustration carries a 세후지급 예상액 column uniformly **83.5%** of the surrender value
  at every duration and on both interest bases [S5] `[derived]`. `surr_tax_pp(t)` publishes
  the charge at every duration and is **not** deducted from `claims`: the insurer pays the
  whole surrender value and the withholding is taken from the policyholder's proceeds.
- **Part of what looks like lapse is 계좌이체, and it is not a withdrawal.** A transfer to
  another 연금저축 or to an IRP attracts no income tax [S1], and the market moved that way
  hard in 2025 — 연금저축펀드 reserves +50.7% against 연금저축보험 −1.2% [R13] [R22]. An
  insurer's termination count and the wrapper's persistency are different numbers, and this
  model's `lapse_rate` is the former.
- **부활 and the 납입최고 state, and why neither survives the annual grid [std].** On an
  annual grid a premium unpaid at `t` terminates the contract at `t`: there is no
  partial-year 납입최고(독촉) state [REG-R25 제26조](#krlib-reg-r25) and no reinstatement re-entry, so
  `lapse_rate` here is a **net-of-부활** rate by construction and a user substituting a
  gross experience rate will over-decrement. The reinstatement interest ceiling of
  평균공시이율 + 1% [REG-R25 제27조](#krlib-reg-r25) is therefore not modelled either.
- **납입유예 is the contractual alternative to lapsing, and it is not lapse.** Up to three
  spells of one year, charges still deducted from the fund, both the premium dates and the
  annuity date deferred by `h`, and the holiday ending prematurely if the fund cannot bear
  the deduction [S5] [S7] [S8]. Where it runs it also **withdraws the 100.1% guarantee**
  [S4] [S6] [S7]. Model point 9 carries a two-year holiday with the guarantee withdrawn:
  `n` moves from 25 to 27 and the annuity date with it.
- **No dynamic lapse function is implemented [std], and the reason is structural.** On a
  fixed-rate savings contract the economic lapse driver is a new-business rate rising above
  the rate at issue. Here the declared rate **resets monthly on the in-force contract**
  [S1] [S2] [S4 제6조①], so an in-force policy does not go stale in that way and the
  competitive pressure expresses itself as 계좌이체 to a better-yielding wrapper rather
  than as surrender. A production model that wants a rate-driven decrement on this product
  should build it on the *spread* between this carrier's declared rate and the market's,
  and should route it to transfer rather than to surrender.
- **Annuitisation-election take-up [std].** 100% 종신연금형 with a ten-year guarantee in
  the base run. The tax code prices the choice and prices it in a dated, quantified way: a
  종신계약 draws a flat **3.3%** withholding at every age from 55, against 5.5% until 70 on
  a fixed-term annuity, the 종신 rate having fallen from 4% to 3% for pensions received on
  or after **2026-01-01** [R5] [R9] [R21]. That is a standing **2.2-percentage-point**
  advantage where before 2026 it was 1.1 points. Against it runs the raw arithmetic of the
  two factors — at the anchor cell the life form pays **38.23%** of what a ten-year certain
  annuity pays out of the same fund — so the election is a real decision and not a coin
  flip. One caution travels with the 3.3%: 종신계약 is defined by 소득세법 시행령
  제187조의2, whose **operative text could not be retrieved** [R7], so whether a guarantee
  period of any length is compatible with the status is **[unverified]**. If a ten-year
  guarantee disqualified the contract the anchor cell's withholding would be 5.5% until 70.
- **The 연금수령한도 constrains the election where it binds, and the contract enforces
  it.** Every retrieved contract makes the default election the tax-recognised maximum —
  「연금액은 관련 세법에서 정한 바에 따라 연금소득으로 인정받을 수 있는 범위 이내로
  합니다」 [S3 제21조②] [S5] [S7] [S8]. At the anchor cell it does not bind at all: the
  연금수령연차 reaches **11** by the 연금개시일 and the formula is disapplied
  [R6 제40조의2제4항](#krlib-pension_savings-r6). At model point 6, annuitising at 55, the counter is 1 and the limit
  in the first payment year is 12% of the 평가액 — ₩3,603,600 against an instalment of
  ₩2,143,455, so the fifteen-year term chosen there clears it. A payout term shorter than
  about ten years on a contract annuitised as early as it can be would not.
- **Commutation, 자유설계연금형 (fund split), 계약이전, 의료비인출 and the six 부득이한
  사유 withdrawals are out of scope [std scope].** Each is a real contract term; none has a
  public frequency; and each is recorded in `product-spec.md` rather than guessed at here.

---

## Worked example

**Anchor cell (`point_id = 1`).** Male, 보험나이 40 at issue; level 기본보험료 of
₩6,000,000 a year (₩500,000 a month) payable at `t = 0 … 19` (`m` = 20, ₩120,000,000
cumulative); 추가납입 nil; gap `d` = 5; 연금개시일 at `t` = `n` = 25, 보험나이 65;
**종신연금형 with a ten-year 보증지급기간**; 무배당; annuitant vintage `issue`; the 100.1%
floor **on**; 해약공제액 nil; 납입유예, 보험계약대출, the dividend and the 추가납입특약 all
**off**; `pension` lapse basis, `base` rate scenario.

Assumption values it uses, all listed above: `i(t)` = 2.15% at every `t` and `i_min(t)` =
1.25 / 1.00 / 0.50% by duration, so `i_c(t)` = **2.15% at every `t`** and the floor never
binds; `α(t)` = 1.50% for `t` = 0…6 and nil after; `β(t)` = 3.00% for `t` < 20 and 0.67%
after; `u(t)` = **0.990316187680581**; `θ` = 0.5%; `f` = 12 both ways; `E0` = ₩200,000,
`e(t)` = ₩30,000 in deferral and ₩20,000 in payment, `π` = 2%, `ec` = ₩30,000, commission
nil; mortality 1.15 × the [std] `annuitant_issue` male table, `q(0)` = 0.0008065180 (table
0.00070132) and `q(25)` = 0.0028596130 (table 0.00248662); lapse 4.0 / 3.5 / 3.0 / 2.5 /
2.0 / 1.5 / 1.0 / 0%; ω = 120, so `proj_len()` = **80** and `result_cf()` has **81 rows**.

The premium net of both charges is therefore

    t = 0..6   NP(t) = 6,000,000 * (1 - 0.015 - 0.030) * u = 5,674,511.7554097297
    t = 7..19  NP(t) = 6,000,000 * (1 - 0.030)         * u = 5,763,640.2123009823
    t >= 20    NP(t) = 0                                       with u = 0.990316187680581

and the charge taken from the fund after 납입완료 is

    t = 20..24  C(t) = 6,000,000 * 0.0067 * u = 39,810.7107447594

**Annuitisation quantities**, at full precision, all read off the model:

| Quantity | Cells | Value |
|---|---|---|
| Cumulative premiums to `t = n` | `cum_prem_pp(25)` | 120,000,000.0000000000 |
| 계약자적립액 at 납입완료 | `av_pp(20)` | 144,311,957.5668485165 |
| 계약자적립액 at 연금개시 | `av_pp(25)` | 160,294,805.5909655988 |
| 100.1% minimum fund | `min_fund_pp()` | 120,119,999.9999999851 (**not binding**) |
| Fund after the floor | `annuity_fund_pp()` | 160,294,805.5909655988 |
| Fund converted | `annuity_fund_net_pp()` | 160,294,805.5909655988 |
| Annuity-due factor, monthly | `annuity_due_factor()` | **23.58191601796395** |
| 연금연액 | `annuity_amount_pp()` | **6,763,374.5893045263** |
| — a month | — | 563,614.5491087105 |
| Implied factor `F ÷ B` | `[derived]` | **23.7004181085** (published **23.70**) |
| Guaranteed total `10B` | `[derived]` | 67,633,745.8930452615 (42.19% of `F`) |
| Ten-year certain factor on the same fund | `annuity_due_certain_factor()` | 9.01595104056377 |
| 표준해약공제액 | `surr_chg_cap_pp()` | **1,421,988.7174578153** |
| 해약공제액 | `surr_chg_pp(t)` | 0.0000000000 at every `t` |
| 세액공제 a year | `tax_credit_pp(0)` | 990,000.0000000000 (**not** an insurer cash flow) |
| 기타소득세 on a surrender at `t = 10` | `surr_tax_pp(10)` | 10,590,733.1198662240 (**not** a cash flow) |
| 연금소득세 rate in payment | `pension_tax_rate(25)` | 0.0330000000 (종신계약) |
| 연금수령연차 at `t = n` | `annuity_year_no(25)` | **11** — the 연금수령한도 is disapplied |

**The implied factor of 23.7004181085 against the published 23.70 is the calibration that
matters**, and it is the only one the public record offers [S2]. The fund itself is
₩160,294,805.59 against the published ₩156,420,000, and that difference is intended and
stated in `product-spec.md`: the composite takes the tied-channel product's model point
[S2] and the direct-channel product's lighter expense schedule [S1]. The ratio `B ÷ F` =
0.0421933485 reproduces the published one (0.042194) to five decimal places.

**Deferral phase, the first eleven years.** `expenses` is acquisition plus maintenance;
`claim_expenses` is its own column, as in `result_cf()`; `commissions` and `policy_loans`
are zero in every row and are omitted from the printed tables.

| `t` | `pols_if(t)` | premiums | claims_death | claims_lapse | expenses | claim_expenses | `net_cf(t)` |
|---|---|---|---|---|---|---|---|
| 0 | 1.0000000000 | 6,000,000.00 | 4,674.99 | 231,673.55 | 230,000.00 | 24.20 | 5,533,627.26 |
| 1 | 0.9592257427 | 5,755,354.46 | 9,270.29 | 393,071.13 | 29,352.31 | 23.73 | 5,323,636.99 |
| 2 | 0.9248893924 | 5,549,336.35 | 13,884.90 | 492,533.66 | 28,867.65 | 23.45 | 5,014,026.70 |
| 3 | 0.8963846174 | 5,378,307.70 | 18,618.45 | 536,123.38 | 28,537.52 | 23.33 | 4,795,005.03 |
| 4 | 0.8732168767 | 5,239,301.26 | 23,575.35 | 659,909.74 | 28,355.94 | 23.38 | 4,527,436.85 |
| 5 | 0.8506267363 | 5,103,760.42 | 28,720.33 | 623,835.27 | 28,174.82 | 23.48 | 4,423,006.52 |
| 6 | 0.8328473436 | 4,997,084.06 | 34,268.90 | 720,369.62 | 28,137.64 | 23.75 | 4,214,284.16 |
| 7 | 0.8154145906 | 4,892,487.54 | 40,222.79 | 816,351.98 | 28,099.65 | 24.08 | 4,007,789.04 |
| 8 | 0.7983196126 | 4,789,917.68 | 46,568.20 | 910,297.18 | 28,060.76 | 24.48 | 3,804,967.06 |
| 9 | 0.7815535795 | 4,689,321.48 | 53,366.48 | 1,002,232.72 | 28,020.87 | 24.94 | 3,605,676.47 |
| 10 | 0.7651077050 | 4,590,646.23 | 60,688.75 | 819,137.74 | 27,979.86 | 25.48 | 3,682,814.39 |

Two features of that table are the product rather than the arithmetic. `claims_lapse` is
**two orders of magnitude larger** than `claims_death` at every duration, because the two
decrements pay the same amount per policy and the surrender rate is fifty times the
mortality rate; and `net_cf` **rises** at `t` = 10, from ₩3,605,676.47 to ₩3,682,814.39,
which is not a fund effect but the lapse rate stepping down from 2.0% to 1.5%.

**The rows where the product does something.**

| `t` | `pols_if(t)` | premiums | claims_annuity | claims_death | claims_lapse | expenses | `net_cf(t)` |
|---|---|---|---|---|---|---|---|
| 6 | 0.8328473436 | 4,997,084.06 | 0.00 | 34,268.90 | 720,369.62 | 28,137.64 | 4,214,284.16 |
| 7 | 0.8154145906 | 4,892,487.54 | 0.00 | 40,222.79 | 816,351.98 | 28,099.65 | 4,007,789.04 |
| 19 | 0.6595725461 | 3,957,435.28 | 0.00 | 174,520.48 | 1,425,145.27 | 28,826.18 | 2,328,907.07 |
| 20 | 0.6484877699 | 0.00 | 0.00 | 187,658.61 | 953,825.77 | 28,908.56 | −1,170,431.14 |
| 21 | 0.6407422762 | 0.00 | 0.00 | 203,261.34 | 962,296.51 | 29,134.55 | −1,194,732.91 |
| 24 | 0.6174807928 | 0.00 | 0.00 | 261,465.85 | 987,174.98 | 29,795.37 | −1,278,485.13 |
| 25 | 0.6096911403 | 0.00 | 4,123,569.57 | 0.00 | 0.00 | 20,005.26 | −4,143,574.82 |
| 26 | 0.6096911403 | 0.00 | 4,123,569.57 | 0.00 | 0.00 | 20,405.36 | −4,143,974.93 |
| 33 | 0.6096911403 | 0.00 | 4,123,569.57 | 0.00 | 0.00 | 23,439.35 | −4,147,008.91 |
| 34 | 0.6096911403 | 0.00 | 4,123,569.57 | 0.00 | 0.00 | 23,908.14 | −4,147,477.70 |
| 35 | 0.5837918602 | 0.00 | 3,948,403.03 | 0.00 | 0.00 | 23,350.38 | −3,971,753.42 |
| 36 | 0.5797787348 | 0.00 | 3,921,260.76 | 0.00 | 0.00 | 23,653.67 | −3,944,914.43 |
| 79 | 0.0023319211 | 0.00 | 15,771.66 | 0.00 | 0.00 | 222.92 | −15,994.58 |
| 80 | 0.0012516484 | 0.00 | 8,465.37 | 0.00 | 0.00 | 122.05 | −8,587.41 |

`t` = 6 and 7 bracket the end of the 계약체결비용 period, where `NP` steps up by
₩89,128.4569 a year. `t` = 19 is the last premium year. `t` = 20 is **납입완료**: the first
row with no premium, and the first negative `net_cf` of the projection. `t` = 25 is the
**연금개시일**, where the first instalment is paid, both deferral decrements go to zero and
the fund disappears into the annuity. `t` = 34 is the **last guaranteed instalment** — the
last row on which `pols_if` is flat — and from `t` = 35 the in-force runs off on
survivorship, which is why `claims_annuity` starts falling there while `B` itself never
changes. `t` = 80 is the terminal row, where `q` = 1.

**The fund, the surrender value and the 환급률.** On this composite `av_pp`, `cv_pp` and
`db_pp` are the same number at every duration, so one column carries all three; the
환급률 is `cv_pp(t) ÷ cum_prem_pp(t)`, the ratio a Korean illustration quotes.

| `t` | `cum_prem_pp(t)` | `av_pp(t)` = `cv_pp(t)` = `db_pp(t)` | 환급률 |
|---|---|---|---|
| 0 | 0.00 | 0.00 | — |
| 1 | 6,000,000.00 | 5,796,513.76 | 0.966086 |
| 2 | 12,000,000.00 | 11,717,652.56 | 0.976471 |
| 3 | 18,000,000.00 | 17,766,095.85 | 0.987005 |
| 4 | 24,000,000.00 | 23,944,580.67 | 0.997691 |
| 5 | 30,000,000.00 | 30,255,902.91 | **1.008530** |
| 6 | 36,000,000.00 | 36,702,918.58 | 1.019526 |
| 7 | 42,000,000.00 | 43,288,545.09 | 1.030680 |
| 10 | 60,000,000.00 | 64,186,261.33 | 1.069771 |
| 15 | 90,000,000.00 | 102,120,559.88 | 1.134673 |
| 19 | 114,000,000.00 | 135,510,914.43 | 1.188692 |
| 20 | 120,000,000.00 | 144,311,957.57 | 1.202600 |
| 21 | 120,000,000.00 | 147,373,998.01 | 1.228117 |
| 24 | 120,000,000.00 | 156,960,814.72 | 1.308007 |
| 25 | 120,000,000.00 | 160,294,805.59 | 1.335790 |
| 26 | 120,000,000.00 | 0.00 | — |

**The 환급률 crosses 100% in the fifth policy year**, at 100.85%, having been 96.61% after
one. That is the shape the adopted expense schedule produces and it is close to the one
that schedule's own carrier publishes: 96.7% at one year and break-even in the fourth year
on a 2.40% declared rate [S1], against 96.61% and the fifth year here at 2.15%. A quarter
of a point of interest is worth about a year of break-even on this design.

**Decrements at the same durations.**

| `t` | `mort_rate(t)` | `lapse_rate(t)` | `pols_death(t)` | `pols_lapse(t)` | `lives_if(t)` |
|---|---|---|---|---|---|
| 0 | 0.0008065180 | 0.0400000000 | 0.0008065180 | 0.0399677393 | 1.0000000000 |
| 1 | 0.0008247685 | 0.0350000000 | 0.0007911392 | 0.0335452111 | 0.9991934820 |
| 5 | 0.0009199195 | 0.0200000000 | 0.0007825081 | 0.0169968846 | 0.9957710983 |
| 10 | 0.0011100950 | 0.0150000000 | 0.0008493422 | 0.0114638754 | 0.9908608859 |
| 19 | 0.0018335025 | 0.0150000000 | 0.0012093279 | 0.0098754483 | 0.9786482084 |
| 20 | 0.0019635675 | 0.0100000000 | 0.0012733495 | 0.0064721442 | 0.9768538545 |
| 24 | 0.0026416305 | 0.0100000000 | 0.0016311561 | 0.0061584964 | 0.9683012203 |
| 25 | 0.0028596130 | 0.0000000000 | 0.0000000000 | 0.0000000000 | 0.9657433263 |
| 34 | 0.0062631185 | 0.0000000000 | 0.0258992801 | 0.0000000000 | 0.9305473107 |
| 35 | 0.0068742400 | 0.0000000000 | 0.0040131254 | 0.0000000000 | 0.9247191826 |
| 80 | 1.0000000000 | 0.0000000000 | 0.0012516484 | 0.0000000000 | 0.0019825957 |

Note `t` = 34 and 35: `pols_death` is **0.0258992801** at the end of the guarantee and
**0.0040131254** the year after, and neither moves a single won of cash flow, because
`db_pp(t) = 0` once the annuity is in payment. It is the run-off of the in-force, not a
claim.

### Traces

Six periods, term by term, at the precision the model produces. Intermediates are full
double precision; the displayed cash flows are those intermediates rounded to two places.

**Year 0 — issue.** `q(0)` = 1.15 × 0.00070132 = **0.0008065180**; `w(0)` = 0.04.

- Premium: 6,000,000 × 1.0000000000 = **6,000,000.00**.
- Allocated: `NP(0)` = 6,000,000 × (1 − 0.015 − 0.030) × 0.990316187680581 = 5,730,000 ×
  0.990316187680581 = **5,674,511.7554097297**. `C(0)` = 0.
- Fund: `AV(1)` = (0 + 5,674,511.7554097297 − 0) × 1.0215 = **5,796,513.7581510395**, and
  `SC(1)` = 0, so `CV(1)` = `DB(1)` = the same number.
- Deaths: `D(0)` = 1 × 0.0008065180 = **0.0008065180**; death outgo = 5,796,513.7581510395
  × 0.0008065180 = **4,674.99**; claim expense = 30,000 × 0.0008065180 = **24.20**.
- Surrenders, from the survivors of mortality: `W(0)` = (1 − 0.0008065180) × 0.04 =
  **0.0399677393**; surrender outgo = 5,796,513.7581510395 × 0.0399677393 = **231,673.55**.
- Expenses: `E0` + `e(0)` = 200,000 + 30,000 × 1.02⁰ = **230,000.00**. Commission nil.
- `CF(0)` = 6,000,000.00 − 4,674.9927 − 231,673.5506 − 230,000.00 − 24.1955 =
  **+5,533,627.26**.
- Update: `l(1)` = (1 − 0.0008065180)(1 − 0.04) = **0.9592257427**; `L(1)` = 1 −
  0.0008065180 = **0.9991934820**.

**Year 1.** `q(1)` = 1.15 × 0.00071719 = **0.0008247685**; `w(1)` = 0.035.

- Premium: 6,000,000 × 0.9592257427 = **5,755,354.46**.
- Fund: `AV(2)` = (5,796,513.7581510395 + 5,674,511.7554097297) × 1.0215 =
  11,471,025.5135607682 × 1.0215 = **11,717,652.5621023253**.
- Deaths: `D(1)` = 0.9592257427 × 0.0008247685 = **0.0007911392**; death outgo =
  11,717,652.5621023253 × 0.0007911392 = **9,270.29**; claim expense = **23.73**.
- Surrenders: `W(1)` = (0.9592257427 − 0.0007911392) × 0.035 = 0.9584346035 × 0.035 =
  **0.0335452111**; surrender outgo = 11,717,652.5621023253 × 0.0335452111 =
  **393,071.13**.
- Expenses: 30,000 × 1.02 × 0.9592257427 = 30,600 × 0.9592257427 = **29,352.31**.
- `CF(1)` = 5,755,354.4563 − 9,270.2940 − 393,071.1291 − 29,352.3077 − 23.7342 =
  **+5,323,636.99**.
- Update: `l(2)` = (0.9592257427 − 0.0007911392)(1 − 0.035) = **0.9248893924**.

**Year 7 — the 계약체결비용 has stopped.** `α(7)` = 0 while `β(7)` is still 3.00%, so

    NP(7) = 6,000,000 * (1 - 0.030) * 0.990316187680581 = 5,820,000 * 0.990316187680581
          = 5,763,640.2123009823

against ₩5,674,511.7554097297 in each of the seven preceding years — **₩89,128.4569 more
into the fund every year from here to 납입완료**, which is the whole of the acquisition
charge, 1.50% × ₩500,000 × 12, valued at the same timing factor. Everything else in the row
is unchanged in form: premium 6,000,000 × 0.8154145906 = **4,892,487.54**, death outgo
₩40,222.79 on `D(7)` = 0.8154145906 × 0.0009844575, surrender outgo ₩816,351.98,
maintenance 30,000 × 1.02⁷ × 0.8154145906 = **28,099.65**, and `CF(7)` = **+4,007,789.04**.
The step is small in the year it happens and compounds for thirteen years.

**Year 20 — 납입완료.** No premium is due; the maintenance charge is taken from the fund
instead. `q(20)` = 1.15 × 0.00170745 = **0.0019635675**; `w(20)` steps down to 0.01.

- Premium: **0.00**. `NP(20)` = 0.
- Charge from the fund: `C(20)` = 6,000,000 × 0.0067 × 0.990316187680581 = 40,200 ×
  0.990316187680581 = **39,810.7107447594**.
- Fund: `AV(21)` = (144,311,957.5668485165 − 39,810.7107447594) × 1.0215 =
  144,272,146.8561037481 × 1.0215 = **147,373,998.0135099888**. The fund still grows —
  ₩3,062,040.45 in the year — because 2.15% on ₩144m is many times a ₩39,810 charge.
- Deaths: `D(20)` = 0.6484877699 × 0.0019635675 = **0.0012733495**; death outgo =
  147,373,998.0135099888 × 0.0012733495 = **187,658.61**; claim expense = 30,000 ×
  0.0012733495 = **38.20**.
- Surrenders: `W(20)` = (0.6484877699 − 0.0012733495) × 0.01 = 0.6472144204 × 0.01 =
  **0.0064721442**; surrender outgo = 147,373,998.0135099888 × 0.0064721442 =
  **953,825.77**.
- Expenses: 30,000 × 1.02²⁰ × 0.6484877699 = 44,578.4218793506 × 0.6484877699 =
  **28,908.56**.
- `CF(20)` = 0 − 187,658.6080 − 953,825.7671 − 28,908.5614 − 38.2005 = **−1,170,431.14**.

This is the row that decides the shape of the whole projection. **납입완료 and 연금개시 are
different dates**, five years apart, and in between the contract is a fund that pays a
charge, pays out on death and surrender, and receives nothing. A model that annuitises at
납입완료 loses these five years, and with them ₩6,112,938.99 of undiscounted outgo and
₩15,982,848.02 of fund growth.

**Year 25 — 연금개시일.** The transition, in the order it happens.

1. Fund fixed: `AV(25)` = (156,960,814.7156058550 − 39,810.7107447594) × 1.0215 =
   156,921,004.0048610866 × 1.0215 = **160,294,805.5909655988**.
2. Floor tested: `G` = 1.001 × 120,000,000 = 120,119,999.9999999851, and
   `F` = max(160,294,805.5909655988, 120,119,999.9999999851) =
   **160,294,805.5909655988**. The floor does not bind, with 33.4% to spare.
3. Factor struck on the `annuitant_issue` male table at 2.15% with `g` = 10 and `f` = 12:
   `ä` = **23.58191601796395**.
4. Annuity struck, once: `B` = 160,294,805.5909655988 ÷ 23.58191601796395 × (1 − 0.005) =
   6,797,361.3962859558 × 0.995 = **6,763,374.5893045263** a year, ₩563,614.55 a month.
5. First instalment paid, in advance, to every contract with an obligation open:
   `claims_annuity(25)` = 6,763,374.5893045263 × 0.6096911403 = **4,123,569.57**.
6. Decrements: `lapse_rate(25)` = 0 and `pols_death(25)` = 0, so no death benefit and no
   surrender; `AV`, `CV` and `DB` are zero from `t` = 26.
7. Expenses: 20,000 × 1.02²⁵ × 0.6096911403 = 32,812.1198892946 × 0.6096911403 =
   **20,005.26** — the maintenance level drops from ₩30,000 to ₩20,000 at annuitisation.
8. `CF(25)` = 0 − 4,123,569.5656 − 20,005.2588 = **−4,143,574.82**.

**Year 35 — the guarantee ends.** The tenth and last guaranteed instalment was paid at
`t` = 34. From here `pols_if` stops being flat and becomes survivorship:

    l(35) = l(25) * L(35) / L(25) = 0.6096911403 * 0.9247191826 / 0.9657433263
          = 0.6096911403 * 0.9575206553 = 0.5837918602

- Annuity: 6,763,374.5893045263 × 0.5837918602 = **3,948,403.03** — the instalment `B` has
  not changed and never will; the count has.
- Expenses: 20,000 × 1.02³⁵ × 0.5837918602 = 39,997.7910532491 × 0.5837918602 =
  **23,350.38**.
- `CF(35)` = −3,948,403.0326 − 23,350.3848 = **−3,971,753.42**, against −4,147,477.70 the
  year before: the first fall in payout outgo in eleven years, and it is mortality, not
  arithmetic.

### Undiscounted totals, `t = 0 … 80`

| Column | Total |
|---|---|
| `premiums` | 95,084,920.7600 |
| `claims_annuity` | 136,717,952.0369 |
| `claims_death` | 2,486,087.7722 |
| `claims_lapse` | 22,509,174.0135 |
| `expenses` | 1,887,294.7545 |
| `claim_expenses` | 756.7500 |
| `commissions` | 0.0000 |
| `policy_loans` | 0.0000 |
| **`net_cf`** | **−68,516,344.5672** |

`premiums` is 79.24% of the ₩120,000,000 nominal, the difference being the decrements;
`claims_annuity` is `B` × 20.2145, the sum of `pols_if` over the payout phase; and
`claims_lapse` is nine times `claims_death`, on decrements whose rates differ by a factor
of about fifty and whose payments are identical — the ratio is what survivorship does to
the weighting over twenty-five years.

### Reading the shape

The projection has four distinct regimes and each one is a contractual fact rather than an
artefact. **Year 0 is strongly positive, +₩5,533,627.26**, because Korean direct-channel
acquisition cost is almost nothing against a ₩6,000,000 premium: no commission at all, a
₩200,000 cash expense, and an acquisition charge that lives inside the fund rather than in
the cash flow. Contrast the UK term composite in this repository, which pays 150% of an
annualized premium of upfront commission. **Then twenty years of declining positive
margin**, from ₩5.53m to ₩2.33m, as surrender outgo grows against a level premium base:
by `t` = 19 the surrender payment of ₩1,425,145.27 is more than a third of the premium
income.
**Then five thin negative years**, `t` = 20…24, totalling −₩6,112,938.99, in which the
contract has stopped paying premiums but has not started paying an annuity. **Then
fifty-six years of pure outgo**, −₩137,688,724.63, flat in `B` and declining in count.

Undiscounted the projection is **−₩68,516,344.57**. Discounted at the rate the fund itself
credits, 2.15%, it is **+₩2,913,938.37** `[derived]`. That pair is the product in one line:
an account contract with a 4.5%-of-premium loading and a longevity promise is close to a
wash at the rate it credits, and the whole of the insurer's result therefore sits in the
spread between what it credits and what it earns, and in whether the annuitants live as
long as the factor assumes. **Neither of those is in this model**, which is the reason it
is a mechanics demonstration and not a pricing result.

### The nine model points

| # | sex | x | m | d | n | Y | `P` | form | vintage | `proj_len` | `F` | `ä` | `B` | Σ `net_cf` |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | M | 40 | 20 | 5 | 25 | 65 | 6,000,000 | 종신 g=10 | issue | 80 | 160,294,805.59 | 23.58192 | 6,763,374.59 | −68,516,344.57 |
| 2 | F | 40 | 20 | 5 | 25 | 65 | 6,000,000 | 종신 g=10 | issue | 80 | 160,294,805.59 | 25.26673 | 6,312,383.96 | −73,799,636.48 |
| 3 | M | 45 | 20 | 0 | 20 | 65 | 3,600,000 | 종신 g=20 | issue | 75 | 86,587,174.54 | 24.08957 | 3,576,412.79 | −34,649,402.87 |
| 4 | F | 25 | 20 | 15 | 35 | 60 | 1,200,000 | 확정 k=20 | issue | 54 | 39,568,543.38 | 16.30428 | 2,414,746.68 | −16,598,163.32 |
| 5 | M | 30 | 10 | 20 | 30 | 60 | 12,000,000 | 확정 k=10 | issue | 39 | 194,438,355.78 | 9.01595 | 21,458,209.25 | −45,678,507.48 |
| 6 | F | 50 | 5 | 0 | 5 | 55 | 6,000,000 | 확정 k=15 | issue | 19 | **30,030,000.00** | 13.94004 | 2,143,455.00 | −2,440,820.60 |
| 7 | M | 40 | 20 | 5 | 25 | 65 | 6,000,000 | 종신 g=10 | commencement | 80 | 160,294,805.59 | 24.30417 | 6,562,384.22 | −70,853,187.86 |
| 8 | M | 40 | 20 | 5 | 25 | 65 | 6,000,000 + 6,000,000 | 종신 g=10 | issue | 80 | 326,721,162.46 | 23.58192 | 13,785,459.86 | −141,563,203.47 |
| 9 | M | 40 | 20 | 5 | 27 | 65 | 6,000,000 | 종신 g=10 | ratchet | 80 | 162,892,867.42 | 22.70113 | 4,266,770.29 | −37,607,123.25 |

Four of them are worth a sentence. **Point 2** is the anchor cell's twin with the sex
switched: the same fund buys a factor of 25.26673 instead of 23.58192 and an annuity
**6.67% smaller**, and that is the only thing sex changes on this product. **Point 6** is
the statutory-minimum contract — five years of premiums, 만 55세 start — run on the `floor`
rate scenario, and it is the one shipped point where the **100.1% guarantee binds exactly**:
the fund at annuitisation is ₩30,030,000 = 100.1% × ₩30,000,000, against an `av_pp(5)` of
₩29,573,776.73 that the guarantee tops up. **Point 7** is the anchor cell struck on the
연금개시시점 vintage instead: the annuity falls **2.97%**, which is the size of the vintage
question and the reason it is a switch rather than an assumption. **Point 9** carries the
ratchet, a two-year 납입유예 (so `n` = 27), the 100.1% floor withdrawn, a policy loan and a
declared dividend all at once, and it confirms the ratchet is out of the money:
`mort_table_name()` returns `annuitant_issue` because the issue-vintage factor, 22.70113,
is smaller than the revised-vintage factor, 23.43728, and the smaller factor is the larger
annuity.

---

## Valuation and reserve pointers

This library projects gross cash flows and builds no reserve. Each layer below consumes
them and is cited, not reproduced.

- **책임준비금 (policy reserve).** 보험업법 제120조 requires it [REG-R3]; 감독규정
  제6-11조 gives the post-2023 taxonomy — 보험계약부채, 재보험계약부채, 투자계약부채, each
  of the first two split into 잔여보장요소 and 발생사고요소 — and **delegates the
  calculation to the FSS Governor**, which is why the 고시 no longer carries accumulation
  rules [REG-R10]. Paragraphs ⑤–⑩ of the old article were deleted on 2022-12-21, and that
  deletion is the visible trace of the switch from a locked-in statutory reserve to a
  current-estimate one.
- **해약환급금준비금, and this product is one of the two it was built for.** 감독규정
  제6-11조의6 makes the insurer compare, at every balance-sheet date including quarterly
  interim closes, its IFRS 17 liability for remaining coverage against the aggregate
  **해약환급금 computed under 제7-66조제1항** plus 미경과보험료, and appropriate any
  shortfall to a surrender-value reserve inside 이익잉여금 — at **company level**, not
  contract level [REG-R11]. Since 2025-06-11 an insurer whose pre-transitional K-ICS ratio
  was 130% or more at the previous quarter-end appropriates only 80% of the shortfall. On
  this product the exposure is maximal by construction: **`CV(t) = AV(t)` at every
  duration**, so the aggregate contractual surrender value is the whole of the fund, and
  the whole of the gap between it and an IFRS 17 measurement is the earnings profile. The
  reserve stood at ₩23.7tn at end-2022 and ₩32.2tn at end-2023 [REG-R11] [REG-R36].
  `Pension_KR_A` computes none of it, and `cv_pp(t)` is the input it would need.
- **보증준비금 (guarantee reserve).** 감독규정 제6-11조의5 requires one inside retained
  earnings for expected losses on benefit guarantees, junior to the 해약환급금준비금
  [REG-R10]. The **100.1% minimum fund is a benefit guarantee**, so this product sits
  inside that perimeter in principle even though the guarantee is shallow. The basis lives
  in 시행세칙 별표 24, which was **not retrieved** [REG-R26], so anything further is
  [unverified] here.
- **K-ICS.** In force since 2023-01-01 alongside IFRS 17 [REG-R13] [REG-R14]. Two of its
  modules bear directly on this contract and neither is computed here: the **대량해지위험**
  shock, reported at second hand as a 35% immediate surrender for 저축성보험 contracts
  [REG-R36] and resting on 별표 22, which was **not retrieved** — so that figure is
  **[unverified]** [REG-R26] — and longevity risk on the annuity in payment. The 35% is the
  one to watch on this product, because a mass surrender pays the full account value.
- **IFRS 17 (K-IFRS 제1117호).** Mandatory since 2023-01-01 [REG-R60]. Whether a 금리연동형
  연금저축보험 qualifies as a direct participating contract measured under the variable fee
  approach is a real question with a large earnings consequence and is **[unverified]**
  here; no retrieved document addresses it. The cash flows above are basis-agnostic input
  to whichever answer a reporter reaches.
- **계약자배당.** 감독규정 제6-11조의7 and 제6-13조 govern the dividend reserve and its
  distribution [REG-R12]. The composite is 무배당 and declares nothing; where a dividend is
  run it may not be paid in cash before annuitisation and is applied as an 증액연금 [S2].
- **The actuarial opinion.** 보험업법 제181조 and 제184조 put the reserve and the basis
  under the 선임계리사 [REG-R5]. The shape of `result_cf()` — a long-dated, undiscounted,
  assumption-explicit projection — is what that office consumes.
- **Policyholder protection.** 예금자보호법 시행령 제18조제7항 sets the limit at
  **₩100,000,000** from 2025-09-01 and applies it to four separate buckets, the second of
  which is the combined total of **연금저축계좌 claims** [REG-R52] [REG-R32]. A
  `Pension_KR_A` policyholder's protection is therefore separate from the ₩100,000,000
  covering their other insurance claims against the same insurer. Not a cash flow in this
  model.

---

## Key sensitivities and model risks

In rough order of leverage on this block.

1. **The credited rate, over twenty-five years of accumulation.** `i_c(t)` is the only
   thing that turns ₩120,000,000 of premium into ₩160,294,805.59 of fund, and it is
   discretionary within a regulated construction whose external-index weight is **capped at
   60%** [REG-R18] [REG-R24]. The composite's 2.15% is the conservative arm of an observed
   2.1%–3.0% range [S12] [S1] [S2] [S11]. The `floor` scenario is not a stress but a
   published illustration column [S2], and at model point 6 it is what makes the 100.1%
   guarantee bind exactly. Nothing else in the model has comparable leverage.
2. **The annuity factor, and its four separate inputs.** `B` moves inversely with `ä`, and
   `ä` is a function of the table, the vintage, the interest basis and the payment
   frequency. On the shipped model points: the **vintage** is worth 2.97% (points 1 vs 7),
   the **sex** 6.67% (1 vs 2), the **frequency correction** 1.91% (the annual factor
   24.04025 would give `B` = ₩6,634,429.17), and the **0.5% charge** 0.5% exactly. A
   production model must re-derive all four; this one exposes each as an input.
3. **Longevity, which is the only insurance risk in the contract.** The fitted table's
   curtate `e(65)` of 33.31 years is the *illustration's* implied longevity, not a Korean
   population estimate — 국가데이터처's 2024 완전생명표 gives 65세 기대여명 남 19.5 and the
   제10회 경험생명표 gives 23.7 [REG-R38] [REG-R33]. Re-striking the factor on a table
   anywhere near either of those would raise `B` by tens of per cent, and the model would
   then no longer reproduce the published annuity. **That tension is the product's, not the
   library's**, and it is the single most important thing to understand before using this
   model for anything but mechanics.
4. **The expense schedule, which is a choice between two published products.** The composite
   takes the direct-channel schedule, so its first-year 환급률 is 96.61% rather than the
   82.7% of the tied-channel product from which the anchor model point comes [S1] [S2].
   That difference is the largest single standardization in the composite and it changes
   early-duration surrender cost, break-even duration and, through them, any lapse
   calibration built on 환급률.
5. **Lapse, which nothing public constrains.** The vector is [std] and argued, its
   count-weighted deferral mean 1.9225% and its `av_pp`-weighted mean 1.4025%. On the
   `savings` comparison vector the same chassis loses far more business before
   annuitisation — model point 5 reaches its annuity date with 0.3831301998 in force. The
   direction of the error is knowable even where the level is not: this vector is
   net-of-부활 and net-of-계좌이체, so an experience rate lifted from an insurer's
   termination statistics will over-decrement.
6. **The 100.1% floor is an option and it is priced at zero here.** It binds at one date on
   one path, and the model tests it by comparison rather than valuing it. On a persistently
   low-rate scenario it is the whole of the guarantee, and a stochastic valuation of it
   belongs in the 보증준비금 [REG-R10] [REG-R26], not in this projection.
7. **Mass surrender.** `CV = AV` at every duration, so a K-ICS 대량해지 shock on this
   product pays the entire account value with no deduction [REG-R36] [unverified], and the
   해약환급금준비금 is measured off the same number [REG-R11]. There is no
   무해지/저해지환급형 dispensation to soften it: 제7-66조제4항 does not apply to a contract
   with a full surrender value from the first month [REG-R19].
8. **The 종신계약 withholding rate, which is [unverified].** The flat 3.3% rests on
   소득세법 시행령 제187조의2, whose operative text was not retrieved [R7]. If a ten-year
   guarantee period disqualified the contract from 종신계약 status the anchor cell's
   withholding would be 5.5% until 70, and the annuitisation-election assumption — 100%
   life form — would need re-arguing.
9. **The 표준해약공제액 reading.** ₩1,421,988.72 on the reading implemented,
   ₩1,486,788.72 on the alternative, 4.56% apart [REG-R20 주3](#krlib-reg-r20). It binds nothing on this
   composite; it would matter to a design that used its headroom.
10. **The 세액공제 band.** The model takes 16.5%, the lower-income band, because a contract
    does not know its owner's income; the alternative is 13.2% [R1] [R8] [R10]. The
    grossing-up of the statutory 15% / 12% is itself **[unverified]** arithmetic, because
    the 지방세법 imposing the surtax was not retrieved [REG-R56]. Nothing in `net_cf`
    depends on it; the lapse argument does.

### Known modeling pitfalls

Each of these is a mistake a competent modeller would actually make on this product, and
each is checkable against the shipped model.

1. **Putting a survivorship release into the fund.** The 계약자적립액 is an account:
   `AV(t+1) = (AV(t) + NP(t) − C(t))(1 + i_c(t))`, full stop. The deferred annuity on the
   Japanese page of this repository divides by `(1 − q')` each year and subtracts a death
   benefit, and porting that shape here **overstates the 연금개시 fund silently**. There is
   nothing to release: the death benefit *is* the fund. `check_av_roll_fwd()` is the check
   that catches it.
2. **Projecting a deferral-phase mortality strain.** `db_pp_net(t+1)` and `cv_pp_net(t+1)`
   are the **same number at every duration** on this composite, so the strain is exactly
   zero and no deferral-phase death cover basis is needed. Mortality still matters — it
   decides how many policies reach the 연금개시일, and hence the charge income and the
   expense — but a model that prices a death benefit here is pricing a risk the contract
   does not run.
3. **Applying a death product's best-estimate adjustment.** `mort_be_factor` is **1.15**,
   greater than one, because the published 연금사망률 is loaded on the *survival* side. A
   0.85 lifted from a death-cover table has the sign wrong and produces both too many
   survivors and, if it is fed into the factor, too large an annuity.
4. **Getting the decrement order wrong.** Deaths are taken from the whole opening in-force
   and surrenders from the survivors: `W(t) = (l(t) − D(t))w(t)`, not `l(t)w(t)`. At `t` = 0
   that is 0.0399677393 against 0.04 — small, and wrong in the same direction every year for
   twenty-five years. `check_pols_roll_fwd()` closes only on the stated order.
5. **Stopping the lapse decrement a year early.** Surrender is available right up to the day
   before the 연금개시일 [S2] [S4], so `lapse_rate(t)` is non-zero **through `t = n − 1`**
   and zero from `t = n`. At the anchor cell year 24 pays ₩987,174.98 of surrender benefit
   on the full fund; zeroing the decrement there deletes it and leaves the in-force too
   high going into the annuity.
6. **Using an annual annuity-due factor.** The annuity is paid 매월 and the factor is
   `ä^(12)`. On the annual factor the anchor cell's `B` would be ₩6,634,429.17 instead of
   ₩6,763,374.59, **1.91% low**, and the model would reproduce none of the eight published
   implied factors. This is the error `product-spec.md` contains and this document corrects.
7. **Putting mortality into the 확정기간연금형 factor, or leaving it out of the
   종신연금형 one.** The certain form is priced on the declared rate alone and its
   instalments are paid to the count whether or not the annuitant lives [S1] [S2] [S6]; the
   life form is priced on the 연금사망률. At the anchor cell the two factors are 9.01595 and
   23.58192 on the same fund — the life annuity pays **38.23%** of the certain one — so
   sharing one code path between them is not a tidy-up, it is a factor of two and a half.
8. **Decrementing `pols_if` by mortality inside a guaranteed or certain period.** Inside
   the 보증지급기간 the obligation is unconditional, so `pols_if` is flat from `t` = 25 to
   34 while `lives_if` falls from 0.9657433263 to 0.9305473107, and not one of those deaths
   changes a won. Conversely `pols_death(34)` = 0.0258992801 is a **run-off of the
   in-force, not a claim**: `db_pp(t) = 0` once the annuity is in payment, so
   `claims_death` is zero from `t` = 25.
9. **Recomputing `B`, or keeping the fund alive after annuitisation.** `B` is struck once at
   `t = n` from `F_net` and never recomputed, and `av_pp`, `cv_pp` and `db_pp` are zero from
   `t = n + 1`. A model that keeps rolling the fund forward and also pays the annuity is
   double-counting the same money. `check_annuity_total()` asserts the instalments are level
   and total `gB`.
10. **Forgetting that the maintenance charge outlives the premium.** `C(t)` = ₩39,810.71 a
    year at `t` = 20…24, ₩199,053.55 in total, taken from the fund with no premium bearing
    it [S1] [S5]. A model whose charges are all premium-based charges nothing in the gap and
    overstates the fund at annuitisation.
11. **Forgetting that the acquisition charge stops.** `α(t)` runs for seven policy years
    only, so `NP` steps up by ₩89,128.4569 a year at `t` = 7. A level-loading model gets the
    fund wrong in both directions — too high early, too low late — and cannot reproduce the
    published 환급률 curve.
12. **Treating the 최저보증이율 as a guarantee on the return.** It guarantees the
    **credited rate**; the charges are still deducted beneath it [S4] [S8]. So
    `charge_from_av_pp` must not consult the floor, and a contract crediting the floor still
    loses the loading.
13. **Mistaking the 예정이율 for a crediting rate.** 2.50% appears in the sources as the
    rate the charge and benefit structure was priced on, and every document that discloses
    it says it is not a guarantee [S1] [S5] [S7]. It appears **nowhere** in the fund
    recursion. The 평균공시이율, also 2.50% in 2026, is a third rate again and enters only
    inside the 표준해약공제액 [REG-R48].
14. **Putting the tax layer into the cash flow.** The 세액공제 (₩990,000 a year at the
    anchor cell, ₩19,800,000 over the premium term) is paid by the state to the saver, and
    the 16.5% 기타소득세 is withheld from the saver's proceeds. Neither passes through the
    insurer's account. Both are published in `result_tax()`, and `check_net_cf()` fails the
    moment either is added to `result_cf()`.
15. **Applying the 연금수령한도 formula where it does not apply.** Where the 연금수령연차
    reaches 11 the formula is **disapplied entirely** [R6 제40조의2제4항](#krlib-pension_savings-r6) [S3], and at the
    anchor cell it is 11 in the first payment year. A model that evaluates
    `평가액 ÷ (11 − 연금수령연차) × 120/100` regardless divides by zero, or caps an annuity
    that no rule caps.
16. **Computing the 표준해약공제액 on the gross premium.** 별표 14 주3 works on the
    **연납순보험료** — the annual premium less the levelled loading, ₩5,577,000 here, not
    ₩6,000,000 — and 주6 then subtracts the discounted acquisition loading. Using the gross
    premium gives ₩2,160,000 before 주6 against ₩2,007,720, a 7.6% overstatement of a cap
    that is meant to bind.
17. **Reading `proj_len()` as a count.** It is the **last index**: 80 at the anchor cell,
    with 81 rows in `result_cf()`. Off-by-one here silently drops the terminal row, which on
    the life form is where the last survivors die.
18. **Assuming the 100.1% floor protects a death claim.** It is a **survival** guarantee
    applied once, at `t = n`, to a policy in force; a death in deferral is paid the fund,
    which may be less than premiums paid — and is, for the first four policy years at the
    anchor cell. Its base is premiums paid **including 추가납입**, which is why
    `cum_prem_pp` adds both.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #krlib-pension_savings-r1
[R10]: #krlib-pension_savings-r10
[R11]: #krlib-pension_savings-r11
[R12]: #krlib-pension_savings-r12
[R13]: #krlib-pension_savings-r13
[R14]: #krlib-pension_savings-r14
[R16]: #krlib-pension_savings-r16
[R17]: #krlib-pension_savings-r17
[R18]: #krlib-pension_savings-r18
[R19]: #krlib-pension_savings-r19
[R20]: #krlib-pension_savings-r20
[R21]: #krlib-pension_savings-r21
[R22]: #krlib-pension_savings-r22
[R24]: #krlib-pension_savings-r24
[R5]: #krlib-pension_savings-r5
[R7]: #krlib-pension_savings-r7
[R8]: #krlib-pension_savings-r8
[R9]: #krlib-pension_savings-r9
[REG-R10]: #krlib-reg-r10
[REG-R11]: #krlib-reg-r11
[REG-R12]: #krlib-reg-r12
[REG-R13]: #krlib-reg-r13
[REG-R14]: #krlib-reg-r14
[REG-R16]: #krlib-reg-r16
[REG-R18]: #krlib-reg-r18
[REG-R19]: #krlib-reg-r19
[REG-R20]: #krlib-reg-r20
[REG-R24]: #krlib-reg-r24
[REG-R26]: #krlib-reg-r26
[REG-R27]: #krlib-reg-r27
[REG-R29]: #krlib-reg-r29
[REG-R3]: #krlib-reg-r3
[REG-R32]: #krlib-reg-r32
[REG-R33]: #krlib-reg-r33
[REG-R34]: #krlib-reg-r34
[REG-R36]: #krlib-reg-r36
[REG-R38]: #krlib-reg-r38
[REG-R4]: #krlib-reg-r4
[REG-R48]: #krlib-reg-r48
[REG-R5]: #krlib-reg-r5
[REG-R52]: #krlib-reg-r52
[REG-R56]: #krlib-reg-r56
[REG-R60]: #krlib-reg-r60
[std]: #krlib-std
[unverified]: #krlib-unverified
<!-- END generated citation links -->
