# Technical Notes

**Status:** Draft, 2026-09-03 (all cited sources accessed 2026-09-03).

**Scope note.** These notes turn the standardized composite critical illness assurance
(*CI boheom*, CI보험, also sold as 중대질병보험 — *jungdae jilbyeong boheom*) of
`product-spec.md` (same directory) into a reference liability cash-flow projection on
paper, and then into `CI_KR_A` beside it. **They describe no single insurer's contract.**
[S#] and [R#] tags resolve against `sources.md`, whose numbering is carried verbatim from
`_research/ci-insurance.md` and is frozen; [REG-R#] tags resolve against the cross-product
reference library `references/regulatory-and-actuarial-references.md`, whose own R1–R60
numbering is separate and also frozen. **[std]** marks a standardization introduced for the
reference implementation; [unverified] marks a claim that could not be confirmed against a
retrieved document. **Every parameter value here is identical to `product-spec.md`'s**, and
every number in the worked example is read off the shipped model rather than recomputed by
hand.

**This document states its deltas against the [whole life chassis
(종신보험)](../whole_life/technical-notes.md) and does not restate it.** The chassis
specifies, once, for the whole library: the 계약자적립액 (*gyeyakja jeongnibaek*, the
policyholder account) recursion and the 예정이율 that accrues it; the 해약환급금
(*haeyak hwangeupgeum*, surrender value) as that account net of a 해약공제액 bounded by the
statutory 표준해약공제액 of 별표 14 [REG-R20] and running off inside seven years [REG-R19];
the 무해지환급형 / 저해지환급형 suppression, the non-marketed 표준형 twin it multiplies and
the step at 납입완료; 보험계약대출 (policy loan) as a modelled state; 보험료 납입면제
(premium waiver) as a state rather than a rate adjustment; 감액; 부활; the 14-day
납입최고(독촉)기간 and the chassis's negative finding that Korea has **no 자동대출납입**, so
that lapse here is behavioural and not funded; and 보험나이 (*boheom nai*, insurance age) as
the age basis. All of it applies here unchanged unless this document says otherwise.

**What is new is acceleration, and it is the whole content of this file.** One decrement
produces **two payments at two dates on one sum assured**. A 중대한 질병 (*jungdaehan
jilbyeong*, "critical" disease) pays a stated fraction — the 선지급 비율, 80% on the
composite — of the 기본보험금 at once; the contract does **not** terminate; the death
benefit becomes the residual complement, floored at 105% of the account; the premium stops;
and the surrender value jumps to its unsuppressed level. Between the two payments the
contract is a genuinely different liability, so the projection carries **two in-force
states**, and the second is indexed by the policy year it was entered in, because the
residual it carries was fixed at that date.

Five quantities appear here that the specification names but does not fix, because all five
are internal to the decrement and expense construction the specification defers to this
document: the post-CI mortality multiple, the post-CI lapse factor, the breast-cancer share
of 중대한 암, the first-year proration of the 90-day 중대한 암 보장개시일 onto an annual
grid, and the expense and commission basis. Each is **[std]** and each is derived, bounded
or stated as a defect below rather than asserted.

The [term life technical notes (정기보험)](../term_life/technical-notes.md) carry the
protection chassis and the 갱신형 / 비갱신형 split; the [cancer technical notes
(암보험)](../cancer/technical-notes.md) carry the fixed-benefit 제3보험 chassis whose 진단비
riders displaced this product in the market; the [long-term care technical notes
(간병보험)](../long_term_care/technical-notes.md) own the 노인장기요양 등급 inception
construction that this model's `ltc` incidence limb is a placeholder for.

---

## Model scope and conventions

- **Purpose.** Project **gross best-estimate liability cash flows** per policy — premiums,
  CI accelerations, pre-CI and post-CI death claims, pre-CI and post-CI surrender benefits,
  claim expenses, maintenance and acquisition expense and commission — for a single model
  point, undiscounted and gross of reinsurance. The chassis's three live measurement bases
  — IFRS 17 (K-IFRS 제1117호) [REG-R60], K-ICS [REG-R13] and the 해약환급금준비금 [REG-R11] —
  all consume this stream and none is reproduced. **Discounting, the risk adjustment, the
  CSM, 요구자본 and every reserve are out of scope** and are cited in *Valuation and reserve
  pointers*.
- **Projection frequency.** **Annual**, on policy years running 계약해당일 to 계약해당일,
  identical to the chassis's grid and permitted on the chassis's authority — 감독규정
  제7-65조제2항 allows the 계약자적립액 of a monthly-premium contract to be computed on an
  annualised premium basis [REG-R18]. The delta is that this product **does** have
  intra-year contractual structure that the chassis does not: the **90-day 중대한 암
  보장개시일** and the **first policy year's 감액** both live inside year 1, and the
  acceleration and the death that may follow it are separated by days rather than by years.
  What the annual grid does with each is stated below and is **[std]** in every case.
- **What the annual grid approximates on this product [std].** Three things. (i) The 90-day
  wait is applied as a straight-line proration of the first year's cancer and 장기요양 rate
  by `1 − 90/365 = 0.7534246575`, which assumes incidence is uniform across the first policy
  year; the 약관's cancel-and-refund right and its five-year revival of a pre-inception
  cancer are not modelled at all [S1 제7조⑤⑥]. (ii) A life accelerating in policy year `t`
  is paid at the **end** of year `t` and joins the post-CI state at the **start** of year
  `t + 1`, so the two payments are at least one annual step apart. That lag is deliberate
  and defensible on the contract's own terms: the 장해분류표 defers assessment of a 중대한
  뇌졸중 for **twelve months** after onset [REG-R25 부표 3](#krlib-reg-r25) [S1 별표3], so a CI claim and the
  death that follows are not simultaneous even on a finer grid. (iii) The suppression is
  released at the **anniversary** at which the CI event is recognised, not at the day of
  diagnosis.
- **Timing conventions [std].** Premium at the **start** of each policy year, in advance,
  years 1 … m, on the paying pre-CI cohort only; maintenance expense and renewal commission
  at the start of each year; acquisition expense and initial commission at issue; **the CI
  acceleration at the end of the policy year of the event**; death claims and claim expenses
  at the end of the policy year of death; surrenders at the end of the policy year, **after**
  the CI transition and **after** deaths.
- **Age basis: 보험나이**, the chassis's. 보험나이 is the 만 나이 at the 계약일 with a
  fraction under six months discarded and six months or more rounded up, incrementing on
  each 계약해당일 [S1 제26조] [REG-R25 제21조](#krlib-reg-r25). Attained age in year `t` is `x + t − 1`
  exactly. **The disclosed rate grid this model is built on is itself stated on 보험나이**
  [S3], which is the one respect in which this product's basis is cleaner than the chassis's:
  the chassis calibrates against 만나이 population statistics and carries a known half-year
  bias, while [S3]'s six 예정위험률 rows are contractual-age rates to begin with. The
  national statistics used to sanity-check the constructions — 국가데이터처 생명표 [REG-R38]
  and the 국가암등록통계 [REG-R40] — are still on 만나이, and **no conversion is applied
  [std]**, so every check against them carries the half-year.
- **Two horizons, not one.** Death cover is **종신**; **CI cover ends at the 100세
  계약해당일** [R1] [R13]. The projection therefore has an inner boundary at
  `n_CI = 100 − x` policy years and an outer boundary at `T = ω − x + 1`. On the anchor cell
  that is `n_CI = 60` and `T = 71`. `ci_rate(t)` is identically zero from `t = 61`; nothing
  else stops there. A projection that runs the CI decrement to the end of the table
  over-states accelerations at ages the contract does not cover, and a projection that stops
  at `n_CI` throws away eleven years of residual death claims.
- **Terminal age.** `ω = 110` for both sexes, the first age at which the shipped
  `mort_table.csv` reaches `q = 1`. It is a **[std]** choice and it is **not** the chassis's
  115: the two tables are different constructions on different anchors, the chassis's fitted
  to 기대여명 targets from [REG-R38] and this one to [S3]'s three disclosed 예정 경험
  사망률 rates, and neither is a 경험생명표, whose terminal age is not published any more
  than its rates are [REG-R33] [REG-R34]. **The two files must not be swapped.**
- **Currency.** KRW throughout, written ₩ with thousands separators and given in the Korean
  만원 / 억원 convention where a Korean reader would expect it: the anchor's ₩100,000,000 is
  1억원. `run.py` prints `KRW` and pure ASCII.
- **Model points.** Single-policy model points projected on an expected
  (probability-weighted) basis. `point_id` parameterizes `Projection`; **`point_id = 1` is
  the worked-example anchor cell.** **Nine** points ship, one fewer than the chassis's ten,
  because this product has no 금리연동형 base run to exercise — the interest-sensitive CI
  variant exists [S1 제36조] but is carried as a documented variant rather than as a model
  point, the whole of its machinery being the chassis's.
- **Rounding.** Intermediate values at full double precision; displayed cash flows and
  surrender values to **two decimal places [std]**, policy counts to six or ten, rates to
  eight or ten. That is the precision `tests/test_ci_insurance_kr.py` asserts.
- **Sign convention.** `net_cf` is **income-positive** — premiums less claims, claim
  expenses, expenses and commission — the library-wide sign, so there is **no**
  outgo-positive `liability_cf` companion.

---

## Model point attributes

| Attribute | Type | Anchor cell (`point_id = 1`) |
|---|---|---|
| `policy_id` | str | `CI-KR-0001` |
| `sex` | enum {M, F} | M |
| `issue_age` (`x`) | int, **보험나이**, 15–60 | **40** |
| `sum_assured` (`SA`) | KRW, ₩10,000,000–₩200,000,000 | **100,000,000** (1억원) |
| `prem_term` (`m`) | int years, 0 for 전기납 | **20** |
| `premium_annual` (`G`) | KRW, level for years 1 … m | **3,680,880** |
| `accel_rate` (`a`) | 선지급 비율, strictly in (0, 1) | **0.80** |
| `cv_floor_ratio` (`k`) | 해약환급금 suppression factor, 1.00 / 0.50 / 0.00 | **0.50** — 저해지환급형 |
| `first_year_scope` | enum {`breast`, `all`} — scope of the first-year 감액 | `breast` |
| `resid_floor_mult` (`c`) | 계약자적립금 floor multiple under the residual | **1.05** |
| `lapse_basis` | enum {`log_linear`, `table`} — the FSS 원칙모형 or the 표준형 curve | `log_linear` |
| `waiver_rate` | 장해 50%+ 납입면제 incidence p.a., during 납입기간 | **0.0003** |
| `pol_loan_util` / `pol_loan_year` | 보험계약대출 take-up fraction, and the year of the draw | 0.0 / 0 |
| `mort_adj` | best-estimate multiplier on the table death rate | 1.0 |
| `ci_adj` | best-estimate multiplier on the CI incidence rate | 1.0 |
| `mort_ci_factor` | post-CI mortality multiple | **3.0** |
| `pols_if_init` | policies in force at the start of year 1 | 1 |

**Five of these are the product**, and each is a column rather than a constant for a
reason. `accel_rate` is the choice the whole document turns on and both observed values —
0.50 and 0.80 — appear in every complete 약관 retrieved [S1] [S2] [S3] [S4] [S5] [S6].
`resid_floor_mult` is a carrier and vintage parameter, not a constant: the CI-generation
약관 floor the residual at **105%** of the 계약자적립금 [S1 별표1 주8] and the older
universal version of the same product uses **110%** [S3], which is why `point_id = 9`
carries 1.10. `first_year_scope` distinguishes the CI-generation design, which halves only
for **breast cancer in the first policy year** [S1 별표1] [S2 별표1], from the
GI-generation design, which halves **every** trigger in year one [S4]; it is a flag, not a
separate product, and `point_id = 4` runs it. `mort_ci_factor` is the post-CI mortality
multiple and has no Korean source at all. `waiver_rate` is the **residual** waiver
incidence — the 장해 50%+ limb only — because on this chassis the CI event itself waives
the premium and is already in `ci_rate`.

**There is no issue-date attribute**, for the chassis's reason: the projection runs on
policy years, 보험나이 is fixed at the 계약일, and the two dates inside a year that matter
— the 납입완료일 and the 100세 계약해당일 — are anniversaries by construction. The **90-day
보장개시일 is the exception**, and it is handled by a rate proration rather than by a date.

**`prem_term = 0` denotes 전기납 (종신납)**, in which `m` is the whole projection, the
suppression never lifts by 납입완료 and **the only exit from it is a CI event**. That
configuration is not in the shipped table on this product — every published Korean CI rate
card in the source set quotes a fixed 납입기간 [S3] [S4] — but the code path is the
chassis's and is live.

**The anchor premium is sourced.** ₩306,740 a month is published for exactly this cell —
남 40세, 1억원, 20년납, 월납, 80% 선지급형, 저해지환급형 — and the annual figure is
12 × that = **₩3,680,880 [std]**, no carrier in the set publishing an annual-mode scale
[S4]. The annual premium is therefore slightly overstated relative to a real 연납 rate and
the first year's interest credit correspondingly understated; the direction is stated, not
corrected. On the other eight points the gross premium is this model's own
`prem_net_level_pp()` grossed up by the loading the anchor implies (**1.2399868**, computed
below) and multiplied by the published 저해지-to-기본환급형 form factor — 1.10224 for the
기본환급형 [S4], 1.000 for the 저해지 form the anchor is on, 0.937 for the 무해지 form
**[std]**.

---

## State variables

The chassis carries one in-force count split into a paying and a waived cohort. **This
model carries two states and four counts**, and the split is the delta.

| Variable | Description | Updated |
|---|---|---|
| `pols_if_pre(t)` | `l0(t)` — in force and **pre-CI** at the start of year `t`; `= 1` at `t = 1` | annual recursion |
| `pols_if_ci_at(t, s)` | `l1(t, s)` — in force and **post-CI**, among those who accelerated in year `s` | annual recursion |
| `pols_if_ci(t)` | `l1(t)` — the post-CI cohort, summed over `s` | sum |
| `pols_if(t)` | `l(t) = l0(t) + l1(t)` — **total** in force; the first `result_cf()` column | sum |
| `pols_if_pay(t)` | `lp(t)` — of the pre-CI cohort, those still paying in cash | `l0 − lw` |
| `pols_waived(t)` | `lw(t)` — of the pre-CI cohort, those in **납입면제** on the 장해 50%+ limb | annual recursion |
| `pols_ci(t)` | `C(t)` — accelerations in year `t` | decrement |
| `pols_ci_in(t, s)` | entrants into post-CI cohort `s` in year `t` | allocation |
| `pols_death(t)`, `pols_death_ci(t)` | `D(t)`, `D'(t)` — deaths pre- and post-CI | decrement |
| `pols_lapse(t)`, `pols_lapse_ci(t)` | `S(t)`, `S'(t)` — surrenders pre- and post-CI | decrement |
| `ci_rate(t)` | `q_ci(t)` — the CI decrement, a **first-event rate across the whole trigger set** | table lookup |
| `mort_rate(t)`, `mort_rate_ci(t)` | `q(t)`, `q'(t) = q(t) × mort_ci_factor` | table lookup |
| `lapse_rate(t)`, `lapse_rate_ci(t)` | `w(t)`, `w'(t)` — pre- and post-CI surrender rates | assumption |
| `pol_val_pp(t)` | `V(t)` — the **계약자적립액** of the 표준형 twin, on the three-state pricing basis | prospective |
| `surr_chg_pp(t)` | `SC(t)` — the 해약공제액, bounded by the 표준해약공제액 | closed form |
| `cv_std_pp(t)` | `W(t) = max(0, V − SC)` — the 표준형 twin's 해약환급금 | closed form |
| `cv_pp(t)`, `cv_pp_ci(t)` | `CV(t) = κ(t) W(t)`, `CV'(t) = W(t)` — payable pre- and post-CI | closed form |
| `base_benefit_pp(t)` | `B(t)` — the **기본보험금**, itself a maximum of three things | closed form |
| `accel_benefit_pp(s)`, `resid_nominal_pp(s)` | `a B(s)` and `r B(s)` for cohort `s` | closed form |
| `resid_db_pp(t, s)`, `resid_db_avg_pp(t)` | `max(r B(s), c V(t))`, and its in-force mean | closed form |
| `loan_pp(t)`, `pol_loan_draw(t)` | `L(t)` — 보험계약대출 balance, and the draw | annual recursion |
| `loan_avail_pp(t)`, `loan_avail_ci_pp(t)` | the limit off `CV(t)` and off `CV'(t)` — **they differ by 1/k** | closed form |

Four of these carry design decisions that a reader must not skip.

**`pols_if` is the total in force, both states.** It is `l0 + l1`, it is the first column of
`result_cf()`, and it is the weight on maintenance expense. Where these notes write `l(t)`
they mean it; where they mean the pre-CI cohort they write `l0(t)` and the cells is
`pols_if_pre`. A reader coming from the chassis, where there is only one count, will reach
for the wrong one. The `Projection` docstring's symbol map distinguishes all three.

**The post-CI state is indexed by its entry year and this is not tidiness.** The residual a
post-CI policy carries was fixed at **its own** acceleration date, at `r` times the
기본보험금 *then*, and the 기본보험금 grows with the account and with cumulative premiums
[S1 별표1 주7]. Collapsing the post-CI cohort to one average residual lets a policy that
accelerated at duration 3 inherit the larger residual of one that accelerated at duration
40. On the anchor cell that error is invisible for six years — every cohort's nominal
residual is ₩20,000,000 while the 기본보험금 is flat at `SA` — and then becomes the whole
of the answer, because from `t = 7` every cohort is on the **shared** floor `c V(t)` and
from `t = 64` the 기본보험금 itself starts to grow.

**Cohort `0` is the first-year 감액 cohort and it is a different amount, not a different
rate.** A breast-cancer claim in policy year 1 is paid `a f B(1)` with `f = 0.5` and leaves
a residual of `(1 − a f) B(1)` — 40% and 60% of the 기본보험금 on the 80% form [S1 별표1]
[S2 별표1]. It is carried as a cohort rather than as a scaling because its residual, 60% of
`SA`, is **three times** every other cohort's and survives for the whole projection.

**There is exactly one policy value in this model**, `pol_val_pp`, and it is the 표준형
twin's 계약자적립액 — the chassis's architecture, unchanged. The suppression is a
multiplier on the surrender value derived from it, not a second account run. What is new is
that the **multiplier has two exits**, so three surrender values coexist at every duration:
`cv_std_pp` the twin's, `cv_pp` the pre-CI payable one, and `cv_pp_ci` the post-CI payable
one, which equals the twin's at **every** duration.

The base run carries **no policy loan**: `pol_loan_util = 0`, so `loan_pp ≡ 0` and every
`max(0, benefit − L)` is the benefit. It does carry a **non-zero 장해 50%+ waiver** at
0.03% p.a., unlike the chassis's base run, because on this product the waiver is not an
optional module — the CI event itself waives the premium — and the residual limb has to be
visible somewhere.

---

## Assumption inputs

Three classes, kept apart on the chassis's terms and for the chassis's reason: the
보험가격지수 exists precisely because a Korean consumer cannot see the pricing basis
[REG-R22 제7-45조제7항](#krlib-reg-r22), the 산출방법서 is a filed but **unpublished** 기초서류 [REG-R2],
and the November 2024 계리가정 decision draws a hard line between an assumption an insurer
may choose and one the supervisor now sets [REG-R27].

### (a) Contractual / guaranteed elements (cited; the insurer cannot change them)

| Input | Value | Basis |
|---|---|---|
| CI/LTC보험금 | **`a` = 80%** of the 기본보험금, payable **once only** across 중대한 질병 (eight), 중대한 수술 (four), 중대한 화상 및 부식 and 장기요양상태 | [S1 별표1] [S2] [S3] [S4] [S5] [S6]; the 80% choice **[std]** |
| The complement | Residual death benefit `r = 1 − a` = **20%**, exactly. 「사망보험금은 CI/LTC보험금을 수령한 경우에는 기본보험금의 50%(50%선지급형) 또는 20%(80%선지급형) 만 지급합니다」 | [S1]; 50 + 50, 80 + 20, 25 + 75 and 40 + 60 all hold exactly [S1] [S2] |
| The contract survives its own acceleration | 감독규정 제7-60조제8호 — a contract must not be extinguished while the risk it covers remains effective | [REG-R16 제7-60조제8호](#krlib-reg-r16) |
| Residual floor | The later death benefit is 「… 기본보험금의 20%와 … 계약자적립금의 **105%** 중 큰 금액」, so `max(r B(t_CI), c V(s))` with `c = 1.05` | [S1 별표1 주8]; `c = 1.10` on the older universal version [S3] |
| 기본보험금 `B(t)` | `max(기본사망보험금, 이미 납입한 보험료, c × V(t))`, with 기본사망보험금 = 보험가입금액 − 중도인출금액 + 추가납입보험료 | [S1 별표1 주7] |
| 사망보험금, no prior CI | **100%** of `B(t)` | [S1] |
| Premium waiver on a CI event | Any CI/LTC 지급사유 waives all future 기본보험료 | [S1 별표1 주4] [S1 제7조] |
| Premium waiver, residual limb | A **50%** 장해지급률 aggregated across body parts from one accident or one non-accidental cause | [S1 별표1 주4]; scale at [REG-R25 부표 3](#krlib-reg-r25) |
| Suppression carve-out | `k` applies only 「CI/LTC보험금 지급사유가 발생하지 않은 경우」 / 「「선지급 진단보험금」 지급사유 발생 전 납입기간 동안」 — **so the suppression has two exits** | [S2] [S4] |
| 중대한 암 보장개시일 | **90 days** from the 계약일 (or 부활일), counting that day; cover attaches the day after the ninetieth | [S1 제7조] [S1 별표1 주1] [S2] [S3] [S4] |
| Everything else | Covered from the **계약일** — no waiting period on the other seven diseases, the four surgeries or the burn | [S1] [S2 별표1 주1] |
| 장기요양상태 보장개시일 | **90 days**, waived where the state arises directly from a 재해 | [S1 별표1 주2] |
| First-year 감액 | Breast cancer within the first policy year pays **`a f` = 40%**, residual 60%; `f = 0.5` | [S1 별표1] [S2 별표1] [S4] [S5] |
| Survival period | **None**, anywhere. The benefit is payable even where the insured dies of the CI cause | [R1] |
| CI cover period | To the **100세 계약해당일**, while death cover runs 종신 | [R1] [R13]; adoption **[std]** |
| 해약환급금 identity | 계약자적립액 less 미상각신계약비(해지공제액), floored at zero; 「순보험료식 책임준비금에서 미상각신계약비(해지공제액)를 공제한 금액」 in a CI product's own words | [S3]; [REG-R19 제7-66조제1항제1호](#krlib-reg-r19) |
| 표준해약공제액 | 연납순보험료 × 5% × 해약공제계수 + 보험가입금액 × 10/1000, the 계수 being the 보험기간 capped at **20** for a 보장성보험 | [REG-R20 별표 14 주2·주3](#krlib-reg-r20) |
| The 보험가입금액 entering the cap | The **일반사망보험금 before any 증감** — i.e. the **pre-acceleration** ₩100,000,000, not the ₩20,000,000 residual | [REG-R21 별표 15 제3호·제8호](#krlib-reg-r21) |
| 해약공제기간 | 납입기간 or 신계약비 부가기간, **capped at 7년** | [REG-R19 제7-66조제1항제2호](#krlib-reg-r19) |
| Post-acceleration surrender | The **full** 표준형 value at every duration | [S2] [S4] |
| 보험계약대출 | Within the **payable** 해약환급금 net of principal and interest; settled first on every exit | [S1]; [REG-R25 제33조·제26조](#krlib-reg-r25) |
| 예정위험률 revision right | From **5 years**, with 금융위원회 approval; an increase is applied by **reducing the benefit** unless the policyholder funds it | [S3] |
| 자살면책 | **2년** from the 보장개시일, reset on 부활 | [S1 제10조] |
| 부활 restarts the 90-day wait | 「계약일(부활(효력 회복)일)부터」 — so a reinstated contract is uncovered for 중대한 암 for ninety days | [S1 별표1 주1] [REG-R25 제27조](#krlib-reg-r25) |
| 예금자보호 | **₩100,000,000** per person per insurer since 2025-09-01 | [REG-R52] [REG-R32] |

**Two of these rows are the reason this product is a life-insurer instrument.** The
acceleration exists only because 제7-60조제8호 forbids the contract to close on payment
[REG-R16], and it can only be built at all by a carrier that may write 질병사망 as the
주보험 — which a 손해보험회사 may not, so the non-life market's answer to the same disease
list is a 독립급부 특약 with no acceleration in it [R1] [REG-R1].

**And one is a quiet regulatory advantage.** Because the contract covers death from any
cause, 별표 15 제3호 applies directly and the 보험가입금액 entering the 표준해약공제액 is
the **pre-acceleration** death benefit [REG-R21]. The 제3보험 siblings in this library —
[cancer (암보험)](../cancer/technical-notes.md) and [children's insurance
(어린이보험)](../child/technical-notes.md) — have no 일반사망 cover and must construct a
notional 보험가입금액 through 제9호's risk-premium ratio instead. The acceleration form buys
this product a simpler regulatory position than the standalone form would have.

### (b) Insurer-discretionary current elements

| Input | Model value (cells / Reference) | Basis |
|---|---|---|
| 예정이율 `i` (`prem_int_rate`) | **2.50% p.a., 연복리, flat** | Chassis, inherited unchanged **[std]**; equal to the 2026 평균공시이율 [REG-R48]. CI evidence brackets it too far away to be useful: 연복리 4.0% on a 2011 product [S3], 「약 2.75%」 for 종신보험 in 2019 [S4] |
| 최저보증이율 (금리연동형 variant) | 연복리 **1.5%** to ten years, **0.5%** beyond — not modelled | [S1 제36조]; required by [REG-R16 제7-60조제10호](#krlib-reg-r16) |
| 보험계약대출이율 `i_L` (`i_loan`) | **4.00% p.a.** = 예정이율 + 1.5%, compound, a **vintage** rate | Chassis, formula at three carriers; level **[std]** |
| 보험계약대출 limit (`loan_cap_rate`) | **80%** of the **payable** 해약환급금 | Chassis range 50%–85%; pick **[std]**; [REG-R25 제33조](#krlib-reg-r25) |
| Net-premium ratio for the cap (`net_prem_ratio`) | **0.80** — the 연납순보험료 entering 별표 14 is taken as 0.80 × `G` | Chassis ratio **[std]**, so the cap rests on published figures alone |
| 표준해약공제액 coefficients | `surr_chg_rate` 0.05, `surr_chg_coef_cap` 20, `surr_chg_sa_rate` 0.01 | [REG-R20 별표 14](#krlib-reg-r20) |
| 해약공제기간 (`surr_chg_years_cap`) | **7** years, then a straight-line run-off **[std]** | [REG-R19 제7-66조제1항제2호](#krlib-reg-r19); the shape **[std]** |
| Acquisition expense `E0` (`expense_acq`) | **₩500,000** per policy at issue | **[std]** |
| Maintenance expense `e` (`expense_maint`) | **₩60,000** p.a. for life, inflating at 1.0% | **[std]** |
| Claim handling expense `ec` (`expense_claim`) | **₩300,000** per **claim event** — CI, pre-CI death and post-CI death alike | **[std]** |
| Expense inflation `π` (`inflation_rate`) | **1.0% p.a.** | **[std]**; 3% compounds to 7.9 over a 71-year horizon |
| Initial commission `c₀` (`comm_init_rate`) | **0.80** of one annual premium at `t = 1` | **[std]**, below the 1,200% rule [REG-R29] |
| Renewal commission `c_r` (`comm_renewal_rate`) | **3.0%** of premium collected, years 2 … m | **[std]** |
| 계약자배당 | **None.** Every CI product in the retrieved set is 무배당 | [S1] [S2] [S3] |

**Every expense parameter here is [std] and nothing in the source set bounds it from
below.** [S1] names the components — 계약체결비용 and 계약관리비용, the latter split into
유지관련비용 and 기타비용, deducted as part of the 월대체보험료 [S1] — and gives no number;
[S3]'s 예정사업비율 table did not extract. Three public handles bound the construction from
above and the model sits inside all three: the **표준해약공제액** itself [REG-R20], the
**보험료지수 of 130.1%** disclosed at exactly this cell [S3], and the 2019 사업비 reform's
first-year remuneration cap [REG-R29]. The model's own gross-to-net loading is
**1.2399868** — ₩3,680,880 over a net level premium of ₩2,968,483.20 — which is of the same
order as the 130.1% 보험료지수 but is **not** the same ratio, the index being computed
against the 금융감독원's prescribed 표준순보험료 rather than against this model's own net
premium. The agreement is an order check, not a fit.

**The claim expense is charged on the CI event as well as on death**, which the chassis has
no occasion to do. That is a **[std]** decision with a real consequence: on the anchor cell
0.433 accelerations and 0.548 deaths occur per policy issued, so the claim-expense stream is
about **79%** larger than a death-only chassis would produce — 0.981006 claim events per
policy issued against 0.548006 deaths.

### (c) Behavioral / experience assumptions (modeler's view — all [std])

**Korea publishes neither table this product needs, and the reason is structural.** The
제10회 경험생명표, applied from 2024-04, is released only as 평균수명 and 기대여명
[REG-R33] [REG-R34]. The 참조순보험요율 is defined by 감독규정 제1-2조제1호 as the 위험률
the bureau **files** with the supervisor, not as a published table [REG-R4]; the 장기손해보험
참조순보험요율 display that *is* public carries a 「기타피부암 및 갑상선암 이외의 암
발생률」 grid and a 질병입원율 grid [REG-R61], which is what `Cancer_KR_S` and `Medical_KR_S`
source their bases from — and **neither reaches this product**, because the 중대한 암
definition is not the insured-cancer definition that grid is stated on. What exists is a
single 2011 상품요약서 that prints its 예정위험률 by sex at ages 20, 40 and 60 [S3]. **Both
decrement files in this product are built on it and nothing else.**

[S3]'s grid, reproduced exactly, is the whole public evidence base:

| 예정위험률 (연) | 남20 | 남40 | 남60 | 여20 | 여40 | 여60 |
|---|---|---|---|---|---|---|
| 예정 경험 사망률 | 0.00051 | 0.00068 | 0.00290 | 0.00027 | (0.00068) | (0.00290) |
| 중대한 암 발생률 | 0.000144 | 0.001023 | 0.011063 | 0.000291 | 0.002220 | 0.006010 |
| 중대한 급성심근경색증 발생률 | 0.000027 | 0.000589 | 0.004371 | 0.000009 | 0.000148 | 0.001814 |
| 중대한 뇌졸중 발생률 | 0.000038 | 0.000907 | 0.003999 | 0.000040 | 0.000399 | 0.002764 |

The two parenthesised female mortality values extract **identical to the male ones**, which
is not plausible for a Korean life table and is almost certainly a PDF column-merge
artefact; they are **[unverified]** and are not used [S3].

**Mortality — `mort_table.csv`, sex × attained age 15 … 110.** A **[std]** construction with
a `provenance` column on every row.

| Row kind | Construction | Basis |
|---|---|---|
| **ANCHOR** (male 20, 40, 60) | [S3]'s three disclosed male 예정 경험 사망률 taken as given | [S3] |
| **FIT** (male, to 60) | Makeham `μ(y) = A + B c^y` fitted **exactly** to those three: `A = 4.960424e−04`, `B = 1.077496e−06`, `c = 1.1371590` | **[std]** |
| **RAMP** (male, above 60) | Log-linear in `q` from the age-60 anchor to `q(110) = 1`: `q(y) = 0.00290 × 1.1240^(y−60)` | **[std]** |
| **FEMALE** (every age) | `q_F(y) = 0.5294 × q_M(y)`, the ratio being [S3]'s own female/male ratio at age 20 (0.00027 / 0.00051) | **[std]** on [S3] |
| **TERMINAL** | `q = 1` at `ω = 110` | **[std]** |

Two properties of this file must be stated rather than discovered. **The old-age shape is a
separate rule, not a continuation**: the fitted Makeham slope of 13.7% a year passes `q = 1`
well before age 100, so extrapolating the fit is not an option. And the female construction
is a **known defect**: a flat ratio gives a 15-to-80 death probability ratio of **0.60**
against the **0.50** implied by 국가데이터처's survival to age 80 of 남 64.4% / 여 82.2%
[REG-R38], so it **understates the female advantage**. Age 20 is the only usable female
anchor because [S3]'s female rates at 40 and 60 are the corrupted ones.

**CI incidence — `ci_incidence_table.csv`, long form sex × attained age 15 … 100 × cause.**
Five causes, each with its own `provenance` tag, because they do not rest on the same thing.

| Cause | What it covers | Construction |
|---|---|---|
| `cancer`, `ami`, `stroke` | 중대한 암, 중대한 급성심근경색증, 중대한 뇌졸중 | **[S3]** at ages 20, 40 and 60; log-linear in `ln(rate)` between and below; above 60 the 40-to-60 log-slope **decaying geometrically at 0.90 a year** **[std]** |
| `other` | the five remaining 중대한 질병, the four 중대한 수술, 중대한 화상 및 부식 | **10.5%** of the three headline rates **[std]** |
| `ltc` | 장기요양상태 on 노인장기요양 1·2등급 | nil below 65, then `0.0012 × 1.14^(y−65)` **[std]** |

**`other` is the one construction in this file with a derivation rather than a shape.**
[S4] publishes the office-premium step from its 3대보장형 to its 17대보장형 at 남40 / 50% /
기본환급형 — 295,960 to 311,640, a **5.30%** increase — and [S3]'s 보장위험별 연간보험료
disclosure gives the CI benefit **50.6%** of the risk premium at male 40 (₩165,419 of
₩327,136 per 1,000만원) [S3] [S4]. Loading a 5.30% office-premium step onto a benefit
carrying 50.6% of the risk cost implies a **10.5%** uplift on the CI rate, which is the
number the file carries. It is [std] because the step is an office premium and the divisor
is a comparison metric — the two are not the same denominator — but it is a derivation from
two published figures rather than a guess, and it reproduces [S4]'s own headline finding
that **the three headline diseases carry almost all the cost**.

**`ltc` is the weakest number in the model and is named as such.** No Korean 장기요양 1·2등급
inception rate at insured ages is published; the level is scaled to the order implied by
[REG-R42]'s 154,688 1·2등급 인정자 at an assumed three-year mean duration, and the shape is
proportional where a real inception curve is not. It is a **placeholder for the construction
[`LTC_KR_S`](../long_term_care/technical-notes.md) owns**, and the 노인성 질병 route below
65 [REG-R55] is not modelled at all. On the anchor cell it contributes nothing before policy
year 26 and then becomes the largest single limb at the oldest ages — 0.1033 of a total
0.1586 at age 99 — so a reader taking any conclusion from the tail of this projection is
taking it from this construction.

**Three properties of the incidence basis are contractual and a modeller must not lose
them.**

**It is a first-event rate across a competing-risk set, not a sum of marginal incidences.**
The benefit is payable **once only** across every trigger [S1 별표1], and Korea's supervisor
required the overlap between CI causes to be priced in rather than ignored: 「국내의 경우
위험률과 담보 간 일치에 대한 규제가 강하고 … CI 질병들 간 중복해서 발생할 수 있는 확률을
최대한 반영한 최종 위험률로 검증받고 사용하였다」 [R1]. Building the table by adding
published site-specific incidences is wrong in exactly the direction the regulation
addresses.

**It already contains the lives who die of the CI cause.** There is no survival period
anywhere in Korean CI, the supervisor having refused one on consumer-protection grounds
[R1], so a life who suffers a qualifying event and dies of it the same week generates
**both** payments. [R1] records that the underlying diagnosis statistics do not capture
those lives, an acknowledged upward bias in exposure that the filed rate absorbs. A model
that imports the overseas 30-day requirement understates the CI decrement and overstates the
death decrement by the same lives.

**The narrowness of 중대한 lives in the level of the rate, not in the prose.** An ordinary
뇌졸중 진단비 rider pays on I60–I63 with no severity condition; the CI trigger adds a
**25% 장해지급률** gate on the statutory 장해분류표 [REG-R25]. An ordinary 암 rider pays on
any C code; the CI trigger removes C44, C61, C73, melanoma at or below T2aN0M0, 대장점막내암,
제자리암 (D00–D09), 경계성종양 and 전암상태 [S1 별표4 Ⅰ]. **How much narrower is not
established** — no Korean population stroke incidence and no CI 부지급률 statistic was
retrieved [R1] — so the model does not apply a narrowing factor to a broader rate. It uses
[S3]'s **already-narrow** disclosed rates directly, which is the only defensible route: the
0.001023 at male 40 is a 중대한 암 rate, not a cancer rate. The check is the registry
arithmetic in `product-spec.md`: 갑상선 is 12.3% of Korean registered cancers and 전립선
7.8%, so those two exclusions alone remove about a fifth of registered incidence before the
rest are taken out [REG-R40].

**Everything else in class (c).**

| Input | Value | Note |
|---|---|---|
| `mort_be_factor`, `ci_be_factor` | **1.00** on every point but `point_id = 9` (0.85 / 0.75) | **[std]**. [S3]'s rates are 예정위험률 carrying a 안전할증 whose regulatory cap was 30%, then 50% from 2015, then removed from 2017 [R1]. **The base run is a valuation-basis run, not a best estimate** |
| Post-CI mortality multiple (`mort_ci_factor`) | **3.00** | **[std]**, and the single largest unsourced number in the file. No Korean post-CI mortality is published; the multiple is anchored qualitatively on 69.6% five-year cancer survival excluding thyroid [REG-R40]. `point_id = 9` runs 2.00 |
| 90-day wait proration (`ci_wait_days`) | **90**, giving `1 − 90/365 = 0.7534246575` on the first year's `cancer` and `ltc` limbs | **[std]** shape; the 90 days sourced at four documents [S1 제7조] [S2] [S3] [S4] |
| First-year 감액 factor (`first_year_factor`) | **0.5** | [S1 별표1] [S2 별표1] [S4] [S5] |
| Breast share of 중대한 암 (`breast_share_m` / `_f`) | **0.005 (M) / 0.268 (F)** | **[std]** on [REG-R40]: 유방 29,871 cases over the female burden less the 19.0% that is 갑상선. A registry share is on 만나이 but a **share** is insensitive to the half-year |
| Pre-CI lapse, `log_linear` basis | `lapse_ll_first` **0.10** → `lapse_ll_target` **0.001** at 납입완료, then `lapse_post_paidup` **0.008** | Endpoints [REG-R27] [R3]; the first-year level **[std]** at the top of a disclosed 적용해지율 envelope; the interpolation **[std]** |
| Pre-CI lapse, `table` basis | `lapse_table.csv`: 0.09 / 0.07 / 0.055 / 0.045 / 0.038 / 0.032, then 0.028 for life | **[std]** 표준형 comparison curve, bounded only by disclosed 적용해지율 envelopes; **no CI lapse experience of any kind was retrieved** [R1] |
| Post-CI lapse factor (`lapse_ci_factor`) | **0.50** of the ultimate rate, i.e. 0.004 flat | **[std]**, and the **direction is genuinely ambiguous** — see *Policyholder behavior modeling* |
| 장해 50%+ waiver incidence | **0.03% p.a.** during 납입기간 | **[std]**. No Korean inception rate at the 50% 장해지급률 threshold is published |
| 보험계약대출 take-up | **0**; a single draw of 50% of the contractual room at `t = 12` on `point_id = 7` | **[std]**. No Korean take-up data is public; no repayment is modelled |
| Tolerances | `roll_fwd_tol` = 1e−10 on counts; `val_tol` = 1e−08, scaled by `SA`, on values | conventions |

**The lapse assumption is the chassis's and the inheritance is not free.** 감독규정
제7-66조제4항 permits the suppressed form **only** where the premium was computed
「최적해지율을 사용하여」 — using a best-estimate lapse rate [REG-R19] — so the lapse vector
is a condition of the product's legality and not only an earnings assumption. The November
2024 계리가정 decision makes the **로그-선형 원칙모형** the default, converging to 0.1% at
납입완료 with a 0.8% ultimate, with departure permitted only against audited disclosure of
the CSM, BEL, K-ICS and net-income differences [REG-R27] [R3]. `CI_KR_A` uses it and ships
the 표준형 `table` basis beside it, which is exactly the comparison the guideline requires an
insurer to disclose. **The functional form of the guideline's model is [unverified] at
instrument level**: the 보도자료 values were retrieved and the HWP attachment carrying the
form was not, so the log-linear interpolation between the two endpoints is this library's
reading.

**One delta on the chassis is worth stating: there is no 완납 lapse spike here.** The
chassis wires a mandatory ≥ 30% additional lapse to the 유지보너스 date [REG-R27]; this
product's composite carries no 유지보너스, so no spike is imposed. The eightfold step in
`lapse_rate` at `t = 21` — 0.001 to 0.008 — is produced by the guideline's own shape and is
not an added assumption.

---

## Cash flow components and recursions

### Notation

Defined once, used throughout, identical to `product-spec.md`'s, and carried in the
`Projection` docstring's symbol map.

| Symbol | Meaning | Cells |
|---|---|---|
| `t`, `s` | policy year; the policy year a post-CI cohort accelerated in | — |
| `x`, `T`, `ω` | 가입나이 (보험나이); `T = ω − x + 1`; table terminal age | `age_at_entry()`, `proj_len()`, `omega_age()` |
| `m` | 납입기간; `m = T` on a 전기납 contract | `prem_period()`, `prem_end()` |
| `n_CI` | last policy year of CI cover, `= 100 − x` | `ci_cover_end()` |
| `n_sc` | 해약공제기간, `= min(m, 7)` | inside `surr_chg_pp(t)` |
| `SA`, `G` | 보험가입금액; annual 영업보험료, level for `t ≤ m` | `sum_assured()`, `premium_pp()` |
| `a`, `r` | 선지급 비율; residual fraction `r = 1 − a` | `accel_rate()`, `resid_rate()` |
| `c`, `f`, `k` | residual account-floor multiple; first-year 감액 factor; suppression factor | `resid_floor_mult()`, `first_year_factor`, `cv_floor_ratio()` |
| `i`, `v`, `i_L` | 예정이율; `v = 1/(1+i)`; 보험계약대출이율 | `prem_int_rate`, `disc_factor()`, `i_loan` |
| `q_ci(t)` | the CI decrement, first-event across the trigger set | `ci_rate(t)` |
| `q(t)`, `q'(t)` | pre-CI and post-CI death rate; `q' = q × mort_ci_factor` | `mort_rate(t)`, `mort_rate_ci(t)` |
| `w(t)`, `w'(t)` | pre-CI and post-CI surrender rate | `lapse_rate(t)`, `lapse_rate_ci(t)` |
| `u(t)` | 장해 50%+ waiver incidence | `waiver_rate(t)` |
| `φ(t)` | share of year `t`'s accelerations routed to the reduced cohort | `ci_reduced_share(t)` |
| `A1(t)`, `A0(t)`, `ä(t)` | EPV of the residual post-CI; EPV of all benefits pre-CI; EPV of 1 p.a. while pre-CI | `epv_resid(t)`, `epv_ben(t)`, `annuity_due(t)` |
| `P`, `V(t)` | 연납순보험료; 계약자적립액 at anniversary `t` | `prem_net_level_pp()`, `pol_val_pp(t)` |
| `B(t)` | 기본보험금 | `base_benefit_pp(t)` |
| `SC*`, `SC(t)`, `W(t)` | 표준해약공제액; 해약공제액; 표준형 twin's 해약환급금 | `surr_chg_cap_pp()`, `surr_chg_pp(t)`, `cv_std_pp(t)` |
| `κ(t)`, `CV(t)`, `CV'(t)` | suppression multiplier; payable value pre-CI; payable value post-CI | `cv_mult(t)`, `cv_pp(t)`, `cv_pp_ci(t)` |
| `l(t)`, `l0(t)`, `l1(t)`, `l1(t,s)` | in force total; pre-CI; post-CI; post-CI cohort `s` | `pols_if(t)`, `pols_if_pre(t)`, `pols_if_ci(t)`, `pols_if_ci_at(t,s)` |
| `lp(t)`, `lw(t)` | paying; waived on the 장해 limb | `pols_if_pay(t)`, `pols_waived(t)` |
| `C(t)`, `C(t,s)` | accelerations in year `t`; entrants into cohort `s` | `pols_ci(t)`, `pols_ci_in(t,s)` |
| `D(t)`, `D'(t)`, `S(t)`, `S'(t)` | pre-CI deaths; post-CI deaths; pre-CI surrenders; post-CI surrenders | `pols_death(t)`, `pols_death_ci(t)`, `pols_lapse(t)`, `pols_lapse_ci(t)` |
| `L(t)`, `Δ(t)` | 보험계약대출 balance at the start of year `t`; the draw | `loan_pp(t)`, `pol_loan_draw(t)` |
| `E0`, `e`, `ec`, `π`, `c₀`, `c_r` | acquisition expense; per-policy maintenance; claim expense; inflation; initial and renewal commission | `expense_acq`, `expense_maint`, `expense_claim`, `inflation_rate`, `comm_init_rate`, `comm_renewal_rate` |
| `CF(t)` | net cash flow of year `t`, **income-positive** | `net_cf(t)` |

**Dimensional check.** `q`, `q'`, `q_ci`, `w`, `w'`, `u`, `a`, `r`, `k`, `κ`, `f`, `φ`, `c`,
`c₀`, `c_r`, `l`, `l0`, `l1`, `lp`, `lw` are dimensionless; `i`, `i_L`, `π` are per annum;
`A0`, `A1` are ₩ (they carry `SA` inside the recursion) and `ä` is a pure number in years of
premium, so `A0 / ä` is ₩ per year; `SA`, `G`, `P`, `V`, `B`, `SC`, `W`, `CV`, `L`, `E0`,
`e`, `ec` are ₩; every term of `CF(t)` is ₩ per policy issued per year. **`c` multiplies a
₩ stock and `a` multiplies a ₩ stock; neither is a rate**, which is worth saying because
both are written as decimals near a page of rates.

### The pricing basis: three states, two annuities that are the same, and one that is not

The chassis prices a two-state contract (alive, dead). This one prices a **three-state**
contract — pre-CI, post-CI, dead — and the recursions are stated forward from the last year
because that is how the model computes them. All three run on the **pricing** decrements,
`ci_rate_base` and `mort_rate_base`, unadjusted by `mort_be_factor` or `ci_be_factor`, which
is what makes the reserve identity testable at all.

    v      = 1 / (1 + i)

    A1(t)  = v * [ q'(t) * r * SA  +  (1 - q'(t)) * A1(t+1) ]              t = 1 .. T
    A1(t)  = 0                                                            t > T

    A0(t)  = v * [ q_ci(t) * a * SA
                 + (1 - q_ci(t)) * q(t) * SA
                 + q_ci(t) * A1(t+1)
                 + (1 - q_ci(t)) * (1 - q(t)) * A0(t+1) ]                 t = 1 .. T
    A0(t)  = 0                                                            t > T

    ad(t)  = 1 + v * (1 - q_ci(t)) * (1 - q(t)) * ad(t+1)                 t = 1 .. m
    ad(t)  = 0                                                            t > m

    P      = A0(1) / ad(1)

    V(t)   = A0(t+1) - P * ad(t+1),        V(0) = 0,  V(T) = 0

Read `A0` term by term, because each term is a contractual clause. `q_ci · a · SA` is the
acceleration. `(1 − q_ci) · q · SA` is the pre-CI death benefit, paid only to those who did
**not** accelerate first — the ordering is in the pricing basis, not only in the cash-flow
projection. `q_ci · A1(t+1)` is the value of the residual handed to the post-CI state, and
it enters at `t + 1` because the acceleration and the residual death are one step apart.
And `(1 − q_ci)(1 − q) · A0(t+1)` continues the pre-CI state.

**The premium annuity carries the CI decrement.** `ad(t)` discounts on `(1 − q_ci)(1 − q)`,
not on `(1 − q)`, because the premium stops on a CI event as surely as on death
[S1 별표1 주4]. A model that prices a CI acceleration off an ordinary life annuity-due
over-values the premium stream by the whole of the CI decrement — on the anchor cell that is
the difference between `ad(1) = 15.1228758581` and the ordinary-life value of
**15.8467943703** on the same table, a **4.8%** over-statement of the annuity and a **4.6%**
under-statement of `P` (₩2,832,875.97 against ₩2,968,483.20).

**Two simplifications inside the pricing recursion are [std] and are stated rather than
hidden.** `A0` values the acceleration at `a · SA` and `A1` values the residual at `r · SA`,
ignoring both the 기본보험금 floors and the **105% account floor** — pricing the second one
in would make `V` self-referential, since the floor is a multiple of `V` itself. Both floors
are applied in full in the cash-flow projection, where `check_resid_floor()` asserts them.
The consequence is quantified in *Key sensitivities*: the reserve is priced on a residual of
₩20,000,000 and the projection pays a residual averaging four times that at long durations.

**The gross premium is an input, not an output**, on the chassis's terms. `G` is the model
point's; the model's own loading ratio is reported and never allowed to drive cash flows.

### 기본보험금 — the floored base every percentage applies to

    B(t) = max( SA - withdrawals + additional_premiums,  cumprem(t),  c * V(t) )
    cumprem(t) = G * min(t, m)

with 중도인출 and 추가납입 held at **zero [std]** so the first limb is `SA`. They are named
rather than dropped because they are **arguments of the 기본보험금 definition**
[S1 별표1 주7]: a model that silently omits them has changed the benefit definition, not
just the parameterisation.

On the anchor cell neither floor binds for sixty-four years and then the third one does.
`cumprem(20) = ₩73,617,600` never reaches ₩100,000,000; `c V(t)` first exceeds it at
**`t = 64`** (attained age 103), where `1.05 × V(64) = ₩100,368,120.65`, and `B` then grows
to a maximum of **₩102,439,024.39** at `t = 70`. The premiums-paid limb is the contractual
form of 감독규정 제7-60조제9호 [REG-R16], whose exception for a 납입기간 ending at age 80 or
below means the rule does not strictly bite here — the floor is market practice that happens
to coincide with the rule.

### The acceleration, the residual, and the two exits from the suppression

    accel_benefit(s)   = a * B(s)                            for s >= 1
    accel_benefit(0)   = a * f * B(1)                        the first-year reduced cohort
    resid_nominal(s)   = r * B(s)                            for s >= 1
    resid_nominal(0)   = (1 - a * f) * B(1)
    resid_db(t, s)     = max( resid_nominal(s),  c * V(t) )

`check_accel_complement()` asserts `a B(s) + r B(s) = B(s)` and
`a f B(1) + (1 − a f) B(1) = B(1)` cohort by cohort at every `t`. **The acceleration never
adds cover**, and that identity is the one thing in this product that is exact rather than
standardized [S1] [S2].

**The residual floor is two-sided and both limbs must be live.** `resid_db` is a maximum,
not a switch: the nominal binds early and the account binds late, and
`check_resid_floor()` asserts that the paid residual is at or above **both**. On the anchor
cell the crossing is at `t = 7`: `1.05 × V(6) = ₩18,093,561.15` is below the nominal
₩20,000,000 and `1.05 × V(7) = ₩21,298,539.04` is above it. From there the residual is the
account and not the stated complement, and by `t = 40` the in-force mean residual is
**₩86,520,318.75** — 4.33 times the nominal.

The 기본보험금 also carries the surrender-value machinery, unchanged from the chassis except
for the multiplier:

    SC*    = net_prem_ratio * G * 0.05 * 20  +  0.01 * SA
    SC(t)  = SC* * (n_sc - t) / n_sc     for t < n_sc,  else 0,   n_sc = min(m, 7)
    W(t)   = max( 0, V(t) - SC(t) )
    kappa(t) = k   for t <  m
    kappa(t) = 1   for t >= m
    CV(t)  = kappa(t) * W(t)                pre-CI  payable value
    CV'(t) = W(t)                           post-CI payable value, at EVERY duration

**`CV'(t) = W(t)` at every duration is the CI-specific delta on the chassis and it is
contractual**, conditioned in [S2] on 「CI/LTC보험금 지급사유가 발생하지 않은 경우」 and in
[S4] on 「「선지급 진단보험금」 지급사유 발생 전 납입기간 동안」. On the chassis the cliff is
a deterministic function of duration and a model can place it at `t = m`. Here it is at
`min(m, t_CI)` — **a random date, correlated with the product's own decrement.**
`check_cv_carve_out()` asserts the consequence the carve-out exists to produce: a CI claimant
is never worse off on surrender than an unaccelerated policyholder at the same duration.

The same carve-out **doubles the policy loan** at the acceleration date, because the limit is
computed off the payable value:

    loan_avail(t)     = loan_cap_rate * CV(t)
    loan_avail_ci(t)  = loan_cap_rate * CV'(t)          = loan_avail(t) / k  while t < m

**The step at 납입완료 is `1 / k` on the same anniversary**, not between adjacent years, and
that distinction is worth money — see the worked example, where `CV(20) / (k W(20))` is
exactly 2.0000000000 while the year-on-year ratio `CV(20) / CV(19)` is 2.1290 and includes a
year of account growth. And, as on the chassis, **the step is not a surrender-charge effect**:
`n_sc = 7`, so on a 20년납 contract the charge has been zero for thirteen years by then.

### Decrements, and the state transition

Within policy year `t`, the CI transition happens **first**, death **second** among those who
did not accelerate, and surrender **third** among those who neither accelerated nor died.

    C(t)   = l0(t) * q_ci(t)
    D(t)   = l0(t) * (1 - q_ci(t)) * q(t)
    S(t)   = l0(t) * (1 - q_ci(t)) * (1 - q(t)) * w(t)
    D'(t)  = l1(t) * q'(t)
    S'(t)  = l1(t) * (1 - q'(t)) * w'(t)

    l0(t+1) = l0(t) - C(t) - D(t) - S(t)
    l1(t+1, s) = C(t, s) + l1(t, s) * (1 - q'(t)) * (1 - w'(t))
    l1(t+1)    = sum over s of l1(t+1, s)
    l(t)       = l0(t) + l1(t)

with the allocation of year `t`'s accelerations to cohorts

    phi(t)     = 0                                             for t >= 2
    phi(1)     = 1                                             if first_year_scope = "all"
    phi(1)     = breast_share * cancer_rate(1) / q_ci(1)       if first_year_scope = "breast"
    C(t, 0)    = C(1) * phi(1)                                 at t = 1 only
    C(t, s)    = C(t) * (1 - phi(t))                           at s = t

**A life that accelerates in year `t` is not exposed to the residual death benefit until
year `t + 1`.** That is the annual grid's rendering of the fact that the two payments are
sequential, and it is asserted rather than assumed: `check_ci_state_roll_fwd()` requires the
pre-CI cohort to lose exactly its accelerations, deaths and surrenders **and** the post-CI
cohort to gain exactly the accelerations, at every `t`.

**The CI transition is deliberately not in the total roll-forward.**
`check_pols_roll_fwd()` asserts `l(t) − l(t+1) = D + D' + S + S'` — four exits, not five —
because an acceleration is a **transition**, not an exit, and a policy that accelerates is
still in force. Adding `C(t)` to that identity is the most natural mistake on this product
and it would double-count every CI claimant out of the population.

The 장해 50%+ waiver rides on the pre-CI cohort only, since a CI event waives the premium
anyway:

    lw(t+1) = [ lw(t) + (l0(t) - lw(t)) * u(t) ] * (1 - q_ci(t)) * (1 - q(t)) * (1 - w(t))
    lp(t)   = l0(t) - lw(t)                                       for t <= m,  else 0

The waived subset stays inside the pre-CI cohort, carries the same three decrements
**[std]** — no Korean source distinguishes the persistency of a waived contract — and keeps
accruing surrender value on the full premium scale, the chassis's 「보험료가 … 정상적으로
납입된 것으로 하여」 rule.

### Benefits, expenses and the loan

    premiums(t)         = G * lp(t)                                        for t <= m

    claims_ci(t)        = sum over s of  C(t, s) * accel_benefit(s)
    claims_death(t)     = max(0, B(t) - L(t)) * D(t)
    claims_death_ci(t)  = sum over s of  l1(t, s) * q'(t) * max(0, resid_db(t, s) - L(t))
    claims_lapse(t)     = max(0, CV(t)  - L(t)) * S(t)
    claims_lapse_ci(t)  = max(0, CV'(t) - L(t)) * S'(t)

    claim_expenses(t)   = ec * ( C(t) + D(t) + D'(t) )
    expenses(t)         = E0 * l(1) * 1{t = 1}  +  e * (1 + pi)^(t-1) * l(t)
    commissions(t)      = c0 * G * l(1) * 1{t = 1}  +  c_r * premiums(t) * 1{2 <= t <= m}

    L(1)     = 0
    L(t+1)   = ( L(t) + Delta(t) ) * (1 + i_L)
    Delta(t) = pol_loan_util * loan_avail(t)     at t = pol_loan_year,  else 0

Four of these lines carry a decision.

**`claims_death_ci` is summed cohort by cohort, not computed off an average.** The residual
differs across cohorts whenever the nominal binds — which is `t ≤ 6` on the anchor and, on
cohort 0, for ever. `resid_db_avg_pp(t)` is published for reading, not for computing.

**`expenses` is weighted by `l(t)`, the total in force, post-CI included.** A post-CI policy
is still a policy: it is administered, it can surrender, it can claim. Weighting maintenance
expense by `l0(t)` alone would drop 0.221670 of a policy at `t = 36` — **48.8%** of the
in-force count at that anniversary, and 21.8% of the projection's person-years.

**`claim_expenses` is charged on the acceleration too.** Two payments, two claim events, two
handling costs.

**Nothing is netted against the loan except the payments.** The acceleration itself is paid
**gross**, not net of `L(t)`: no retrieved document says the 선지급 is reduced by the loan
balance, and the 표준약관's netting rule speaks to 보험금 payment and to 해지 [REG-R25
제33조](#krlib-reg-r25). That is a **[std]** reading and it is the conservative one for the policyholder; on
`point_id = 7`, the only point with a loan, it is also the reading that keeps the loan
balance intact into the residual, which is where it does bite.

### Processing order (policy year `t = 1 … T`)

Explicit, because three steps in it are worth money and two are conventions.

1. **Start of year — the two-state split.** `l(t) = l0(t) + l1(t)`. This is the
   `result_cf()` row's `pols_if` and the weight on maintenance expense and claim expense.
2. **Start of year — the 장해 50%+ waiver transition**, out of the paying cohort, before the
   premium is taken.
3. **Start of year — premium.** `G × lp(t)` for `t ≤ m`, in advance, on the **pre-CI paying**
   cohort only. **The post-CI cohort never pays**, at any duration, because the CI event
   waived it [S1 별표1 주4].
4. **Start of year — expenses and commission.** `E0` and `c₀ G` at `t = 1` on `l(1)`;
   maintenance `e (1+π)^(t−1) l(t)` every year for life; renewal commission on the premium
   actually collected, years 2 … m.
5. **Start of year — 보험계약대출 draw**, where one is elected, off `CV(t)`.
6. **Values.** `V(t)`, `SC(t)`, `W(t)`, `CV(t)`, `CV'(t)`, `B(t)` at the year-end
   anniversary.
7. **End of year — the CI transition, first.** `C(t) = l0(t) q_ci(t)`, paid `a B(t)` (or
   `a f B(1)` for the year-1 reduced part) **gross of the loan**. Entrants join the post-CI
   state at the **start of year `t + 1`**.
8. **End of year — deaths, second, among those who did not accelerate.**
   `D(t) = l0(t)(1 − q_ci)q`, paying `max(0, B(t) − L(t))`. Post-CI deaths
   `l1(t,s) q'(t)` pay `max(0, max(r B(s), c V(t)) − L(t))`, cohort by cohort.
9. **End of year — surrenders, third, among those who neither accelerated nor died.**
   `S(t) = l0(t)(1 − q_ci)(1 − q)w`, paying `max(0, CV(t) − L(t))`. Post-CI surrenders pay
   `max(0, CV'(t) − L(t))`, the **full** 표준형 value.
10. **End of year — loan roll-up.** `L(t+1) = (L(t) + Δ(t))(1 + i_L)`.
11. **Update in force**, per the two-state recursion above.
12. **At `t = n_CI`** the CI decrement stops; the projection continues. **At `t = T`** the
    table's terminal rate is 1, everyone dies, `l(T+1) = 0`, and `V(T) := 0`.

**"CI before death before lapse" is a [std] ordering and it is not neutral.** Reversing the
first two would apply the death rate to the full pre-CI count and route lives that would
have accelerated into the death decrement, which on the anchor cell is a decrement 3.7 times
smaller at issue and 6.7 times smaller at 60 [S3]. It is stated here, asserted by
`check_ci_state_roll_fwd()`, and should be the first thing a reader checks against their own
convention.

**The account recursion runs on its own clock.** `V(t)` is a function of `t`, `P`, `i`,
`q_ci` and `q` alone — **not of `l`, `l0`, `l1`, `w` or `u`**. It is a per-policy contractual
quantity, so the decrements' *incidence* enters it through the pricing basis and the
decrements' *population* does not.

### Net cash flow

Income-positive, per policy issued:

    CF(t) =   premiums(t)
            - claims_ci(t)
            - claims_death(t)
            - claims_death_ci(t)
            - claims_lapse(t)
            - claims_lapse_ci(t)
            - claim_expenses(t)
            - expenses(t)
            - commissions(t)

`result_cf()` publishes exactly these as, in order, `pols_if`, `premiums`, `claims_ci`,
`claims_death`, `claims_death_ci`, `claims_lapse`, `claims_lapse_ci`, `claim_expenses`,
`expenses`, `commissions`, `net_cf` — `pols_if` first, `net_cf` last, **no `claims`
subtotal column**, so the columns sum exactly to `net_cf`. The `claims(t, kind)` cells
stays, with `kind` in {`CI`, `DEATH`, `DEATH_CI`, `LAPSE`, `LAPSE_CI`}, and
`check_net_cf()` asserts the ledger at every `t`.

**The five-way claims split is the point of the publication order.** A three-column
statement — premiums, claims, expenses — would hide the entire subject of this document,
which is that `claims_ci` and `claims_death_ci` are two payments arising from **one**
decrement at two different dates, and that on the 80% form the second is the larger of the
two.

**Nine identities close the projection.** Each `check_*()` takes no argument and returns a
bool over all `t`, with the per-`t` signed residual at `check_*_resid(t)`. All nine are
`True` on all nine model points.

| Check | The identity | What breaks it |
|---|---|---|
| `check_pols_roll_fwd` | `l(t) − l(t+1) = D + D' + S + S'` — **four** exits | putting the CI transition in the identity |
| `check_ci_state_roll_fwd` | the pre-CI cohort loses exactly `C + D + S` **and** the post-CI cohort gains exactly `C` | a policy leaving one state and not arriving in the other |
| `check_decrement_sum` | every policy issued leaves by a modelled decrement | a residual population, a tail state |
| `check_pol_val_roll_fwd` | `(V(t−1) + P·1{t≤m})(1+i)` = the year's expected outgo plus `(1−q_ci)(1−q)V(t)` | the CI decrement left out of the premium annuity |
| `check_accel_complement` | `a B + r B = B`, and `a f B + (1 − a f) B = B`, cohort by cohort | an acceleration that adds or destroys cover |
| `check_resid_floor` | the residual is at or above **both** `r B(s)` and `c V(t)` | a one-sided max, or the floor read off the wrong anniversary |
| `check_cv_carve_out` | `CV'(t) ≥ CV(t)` at every `t` | the suppression applied to the post-CI cohort |
| `check_loan_roll_fwd` | `L(t+1) = (L(t) + Δ(t))(1 + i_L)` | a balance not accumulating at `i_loan` |
| `check_net_cf` | `net_cf` equals the sum of the published `result_cf()` columns | a benefit kind missing from the statement |

Tolerances: `roll_fwd_tol = 1e−10` on the count identities, `val_tol × SA = 1e−08 × SA` on
the value identities.

### Optional modules (all off in the base run)

| Module | Switch | Base | Exercised on |
|---|---|---|---|
| 보험계약대출 | `pol_loan_util`, `pol_loan_year` | 0 | `point_id = 7`, 50% of the room at `t = 12` |
| 50% 선지급형 | `accel_rate` | 0.80 | `point_id = 3` (기본환급형) and `8` (저해지) |
| 무해지환급형 / 기본환급형 | `cv_floor_ratio` | 0.50 | `point_id = 4` (`k` = 0.00), `3` and `6` (`k` = 1.00) |
| All-trigger first-year 감액 | `first_year_scope` | `breast` | `point_id = 4` |
| 표준형 lapse curve | `lapse_basis` | `log_linear` | `point_id = 3`, `6`, `8` |
| 110% residual floor | `resid_floor_mult` | 1.05 | `point_id = 9` |
| Best-estimate levers | `mort_adj`, `ci_adj`, `mort_ci_factor` | 1.00 / 1.00 / 3.00 | `point_id = 9`, at 0.85 / 0.75 / 2.00 |

**Nothing in this list is a placeholder**, and the 장해 50%+ waiver is deliberately not in
it: it runs at 0.03% p.a. on **every** shipped point, because on this product the waiver is
part of the main contract rather than an option [S1 별표1 주4].

**Not modelled, and named so that it is not mistaken for absent.** 중도인출 and 추가납입,
held at zero although they are arguments of the 기본보험금 definition [S1 별표1 주7]; 부활
and the 90-day cancer wait it restarts [S1 별표1 주1]; the pre-inception cancer carve-out and
its five-year revival [S1 제7조⑥]; the 예정위험률 revision right, which takes effect as a
**benefit reduction** rather than as a lapse [S3]; 가지급제도 [S1 제13조]; 감액; 연금전환,
which appears in no retrieved CI 약관; the 다중지급 (multi-pay) generation [R1]; the 100%
선지급플러스형, which is not a pure acceleration because it replaces the residual with a
separately funded 유족위로금 [S4]; the 80세 two-period design of the 2002 product [S6] [R1];
and the chassis's clawback, whose interaction with the CI carve-out is **[unverified]** —
`CI_KR_A` assumes it does not gate it. No 요구자본 anywhere.

---

## Policyholder behavior modeling

All dynamic forms are **[std]** reference constructions, and on this product the evidence
base is thinner than on the chassis: **no CI lapse experience of any kind was retrieved**
[R1].

- **Pre-CI surrender.** The `log_linear` vector of class (c): 10% in year 1 decaying
  log-linearly to 0.1% at 납입완료, then 0.8% for life, the FSS 원칙모형 [REG-R27] [R3].
  The decay constant is `λ = ln(0.10/0.001)/(m − 1) = 0.2423773782` on the anchor, so
  `w(1) = 0.10` and `w(20) = 0.001` are exact by construction. The 표준형 `table` basis
  runs beside it, and the two produce **materially different products**: re-running the
  anchor on a level 4% rate through the 납입기간, the 0.8% post-완납 ultimate unchanged,
  gives an undiscounted `Σ net_cf` of **−₩34,122,514.19** against the base run's
  **−₩51,285,700.32**, a third of the whole liability, because a higher lapse rate removes
  lives before the acceleration reaches them.
- **Post-CI surrender is the assumption whose *direction* is unknown.** `lapse_ci_factor` is
  **0.50** of the ultimate rate, i.e. 0.004 flat, and the argument runs both ways with equal
  force. A CI claimant has just received 80% of the sum assured in cash, has no premium to
  pay, and holds a contract whose surrender value has doubled — every one of which is a
  reason to surrender. Against that, the claimant is uninsurable elsewhere, the residual is
  now floored at 105% of a growing account, and the contract costs nothing to keep. **No
  Korean source settles it.** Setting the factor to 1.00 instead of 0.50 moves the
  undiscounted `Σ net_cf` from −₩51,285,700.32 to **−₩50,954,936.47**, a 0.6% swing on the
  whole liability, so the level does not matter much in aggregate; **the sign of the
  behavioural story does**, and it is unresolved.
- **The 환급률 crossing is not modelled as a driver.** On the chassis the economically
  natural dynamic-lapse trigger is the refund ratio crossing 1. Here there are **two**
  candidate triggers — the refund ratio, and the CI event itself, which doubles the value
  overnight — and no dynamic form is shipped for either **[std]**. The reason is the
  chassis's: the November 2024 decision fixes the base vector, and a dynamic overlay on a
  supervised assumption is a departure requiring the full disclosure regime [REG-R27]. The
  hook is `lapse_rate(t)` and `lapse_rate_ci(t)`; a user adding one changes no other formula.
- **The premium waiver is not an independent decrement on this chassis, and that is a
  simplification with a direction.** A CI event waives the premium [S1 별표1 주4], so on
  essentially every CI claim the waiver and the acceleration fire together and the waiver is
  already inside `ci_rate`. What remains is the 장해 50%+ limb, at 0.03% p.a. **[std]**.
  **But the trigger sets are of different widths and the model uses one rate for the narrow
  one.** [S4]'s GI product waives on a 50%+ disability **or** on 암 including 특정암 (breast
  and prostate, which it does **not** accelerate), 뇌출혈, 급성심근경색증, 중증질환, 중대한
  화상 및 부식 or a 중대한 수술 [S4]; one carrier advertises **25** distinct waiver triggers
  [R11]. A modern Korean accelerated product therefore has **a narrow trigger set for the
  money and a wide one for the premium waiver**, and this model has only the narrow one. The
  waiver incidence is understated by the whole of the difference, which is unquantified.
- **보험계약대출 take-up is static and the loan does not terminate the contract.** A single
  draw of a chosen fraction of the contractual room at a chosen year, no repayment, and the
  balance netted off every payment except the acceleration and floored at zero. Korea has no
  loan-excess-lapse notice [REG-R25], so the balance can only absorb a payout. **What is new
  here is that the room itself doubles on a diagnosis**: on `point_id = 7` at `t = 12` the
  pre-CI limit is ₩23,581,915.16 and the post-CI limit at the same duration is
  ₩47,163,830.33.
- **부활 is not modelled and the omission is larger here than on the chassis.** 부활 within
  three years restarts the **90-day 중대한 암 보장개시일** [S1 별표1 주1], so a reinstated CI
  contract is uncovered for cancer for ninety days — a decrement the chassis has no
  counterpart for. Setting `reinstate` to zero understates later-duration in force and
  therefore both premium income and claims, and it also removes a real ninety-day gap in
  cover. Both biases are stated rather than corrected because no Korean reinstatement rate
  was retrieved.
- **The pre-inception cancer carve-out is a state this model does not have.** A cancer
  diagnosed before the 보장개시일 puts the policyholder in a position where the premium is
  **not** waived and the cancer is **not** covered, with cover reviving only after five
  claim-free years [S1 제7조⑥] [S1 별표1 주5]. It is a third in-force state with its own
  economics and it is out of scope; a policyholder in it pays premiums on cover they cannot
  claim.
- **면책 incidence is zero in the base run [std], and refusal is not forfeiture.** The
  chassis's finding carries over: where a claim is refused for an 면책사유 the insurer must
  still pay 「보험수익자를 위하여 적립한 금액」 [REG-R50 제736조](#krlib-reg-r50) [REG-R25 제22조](#krlib-reg-r25). **On this
  product the refusal rate is the whole consumer story** — the 중대한 definitions are the
  most litigated wording in the Korean market [R5] [R6] [R7] [R10] [R16] — and **no Korean CI
  부지급률 statistic exists in any retrieved source** [R1]. A model that treated a refused CI
  claim as a zero-payment event would be wrong by the amount of the account, not by the
  amount of the claim.

---

## Worked example

### The anchor cell

**`point_id = 1`, `CI-KR-0001`** — 남자, 보험나이 **40세**, 보험가입금액 **₩100,000,000
(1억원)**, 보험기간 **종신** with **CI 보장 to the 100세 계약해당일**, 납입기간 **20년**,
월납 annualized, **80% 선지급형**, **저해지환급형 `k = 0.50`**, first-year 감액 scope
`breast`, residual floor `c = 1.05`, lapse basis `log_linear`, annual premium
**₩3,680,880**. `T = 110 − 40 + 1 = 71` policy years, attained 보험나이 40 to 110;
`n_CI = 100 − 40 = 60` policy years of CI cover. The policy loan is off
(`pol_loan_util = 0`), the best-estimate levers are at 1.00, and the 장해 50%+ waiver runs
at 0.0003 p.a.

**Assumption values used, in full.** `i = 2.50%` **[std]**, the chassis's, on a disclosed
2.25%–2.75% band and equal to the 2026 평균공시이율 [REG-R48]; `q` from `mort_table.csv`
남 at attained 보험나이 with `mort_be_factor = 1.00`, a **[std]** Makeham fit to [S3]'s
three disclosed anchors; `q' = 3.00 q` **[std]**; `q_ci` from `ci_incidence_table.csv`
summed over five causes with `ci_be_factor = 1.00`, **[S3]** at ages 20, 40 and 60 and
**[std]** elsewhere; the first year's `cancer` and `ltc` limbs prorated by
`1 − 90/365 = 0.7534246575` **[std]** on a 90-day 보장개시일 sourced at four documents
[S1 제7조] [S2] [S3] [S4]; `w` the `log_linear` vector, endpoints [REG-R27] [R3] and the
interpolation **[std]**; `w' = 0.50 × 0.008 = 0.004` **[std]**; `u = 0.0003` **[std]**;
`f = 0.5` [S1 별표1] [S2 별표1]; `breast_share_m = 0.005` **[std]** on [REG-R40];
`SC*` from 별표 14 [REG-R20] with the 7-year 해약공제기간 of [REG-R19] and a **[std]**
straight-line run-off; `E0 = ₩500,000`, `e = ₩60,000` p.a. inflating at 1.0%,
`ec = ₩300,000` per claim event, `c₀ = 0.80`, `c_r = 3.0%`, all **[std]**; `i_L = 4.00%`,
unused here because `loan_pp ≡ 0`.

**Derived scalars, at full precision.**

| Quantity | Cells | Value |
|---|---|---|
| Terminal age ω | `omega_age()` | **110** |
| Projection length `T` | `proj_len()` | **71** |
| Last CI-covered policy year `n_CI` | `ci_cover_end()` | **60** (attained age 99) |
| 납입기간 `m` | `prem_period()`, `prem_end()` | 20 |
| 해약공제기간 `n_sc` | `min(m, surr_chg_years_cap)` | **7** |
| `v` | `disc_factor()` | 0.9756097560975611 |
| `A0(1)` | `epv_ben(1)` | **₩44,892,002.9507502913** (0.448920 × `SA`) |
| `A1(1)` | `epv_resid(1)` | ₩8,148,218.3575074952 |
| `ä(1)` | `annuity_due(1)` | **15.1228758581** |
| 연납순보험료 `P` | `prem_net_level_pp()` | **₩2,968,483.2020010490** |
| 영업보험료 `G` | `premium_pp()` | **₩3,680,880.0000000000** |
| Gross-to-net loading `G / P` | — | **1.2399868045** |
| **표준해약공제액** `SC*` | `surr_chg_cap_pp()` | **₩3,944,704.00** |
| 선지급 비율 `a` / residual `r` | `accel_rate()`, `resid_rate()` | 0.80 / 0.20 |
| Breast share of 중대한 암 | `breast_share()` | 0.005 |
| 90-day proration factor | `ci_wait_factor()` | 0.7534246575342466 |
| Ultimate pre-CI lapse | `lapse_rate_ult()` | 0.008 |

`P × ä(1) = 2,968,483.2020010490 × 15.1228758581 = ₩44,892,002.95` reproduces `A0(1)` to
the won, which is the equivalence principle asserted rather than assumed.

**The 표준해약공제액 arithmetic, in one line, from published figures alone:**

    SC* = 0.80 * 3,680,880 * 0.05 * 20  +  0.01 * 100,000,000
        = 2,944,704.00 + 1,000,000.00  =  KRW 3,944,704.00

against the FSC's 「보장성보험 월 보험료의 13배 수준」 rule of thumb of
13 × ₩306,740 = **₩3,987,620** — the two independent statements of the same cap agree to
**1.1%** [REG-R20] [REG-R29]. That is tighter than the chassis's own 7.0% agreement at its
anchor, and it is the one place in this document where a [std] input (the 0.80 net-premium
ratio) is corroborated from outside.

**Floating-point note.** `resid_rate()` is computed as `1.0 − 0.8` and is therefore
`0.19999999999999996` in binary; `resid_nominal_pp(s)` prints as ₩19,999,999.9999999963.
It is the exact complement in the sense the model asserts — `check_accel_complement()`
closes to `1e−08 × SA` = ₩1 — and it is written **₩20,000,000** throughout this document.

### Two cross-checks that fell out of the model rather than being imposed

| Quantity | Model | Published | Gap |
|---|---|---|---|
| 80% form net premium ÷ 50% form, 남 40 | **1.0794** | **1.085** [S4] | 0.5% |
| 표준해약공제액 at the anchor | **₩3,944,704** | ₩3,987,620 on the 13× rule [REG-R29] | 1.1% |

The first is the more interesting of the two, because nothing in the construction was fitted
to it. Re-running the pricing recursion with `a = 0.50` on the same table gives
`A0(1) = ₩41,589,404.25` and `P = ₩2,750,098.90`, so the 80% form costs **1.0794** times the
50% form; [S4]'s published 96-cell grid gives 338,100 / 311,640 = **1.085** at 남40 / 17대 /
기본환급형. Two independent routes to the price of thirty percentage points of acceleration
agree to five parts in a thousand.

**And one that does not agree, stated as such.** The gross-to-net loading of **1.2400** sits
beside a disclosed 보험료지수 of **130.1%** [S3]. They are not the same ratio — the index is
computed against the 금융감독원's prescribed 표준순보험료, this is against the model's own
net premium — so the agreement is one of order only, and neither figure was used to
calibrate the other.

### The decrement basis at the anchor, `t = 1 … 25`

`q_ci` is the sum of five causes; `q' = 3.00 q`; `w'` is flat at 0.004.

| t | attained age | `ci_rate(t)` | `mort_rate(t)` | `mort_rate_ci(t)` | `lapse_rate(t)` |
|---|---|---|---|---|---|
| 1 | 40 | 0.0025312484 | 0.00068000 | 0.00204000 | 0.1000000000 |
| 2 | 41 | 0.0030721810 | 0.00070525 | 0.00211575 | 0.0784759970 |
| 3 | 42 | 0.0033921090 | 0.00073395 | 0.00220185 | 0.0615848211 |
| 4 | 43 | 0.0037467810 | 0.00076660 | 0.00229980 | 0.0483293024 |
| 5 | 44 | 0.0041401050 | 0.00080372 | 0.00241116 | 0.0379269019 |
| 6 | 45 | 0.0045764400 | 0.00084593 | 0.00253779 | 0.0297635144 |
| 7 | 46 | 0.0050606550 | 0.00089392 | 0.00268176 | 0.0233572147 |
| 8 | 47 | 0.0055981780 | 0.00094850 | 0.00284550 | 0.0183298071 |
| 9 | 48 | 0.0061950720 | 0.00101056 | 0.00303168 | 0.0143844989 |
| 10 | 49 | 0.0068581080 | 0.00108113 | 0.00324339 | 0.0112883789 |
| 11 | 50 | 0.0075948480 | 0.00116137 | 0.00348411 | 0.0088586679 |
| 12 | 51 | 0.0084137370 | 0.00125261 | 0.00375783 | 0.0069519280 |
| 13 | 52 | 0.0093242150 | 0.00135635 | 0.00406905 | 0.0054555948 |
| 14 | 53 | 0.0103368310 | 0.00147431 | 0.00442293 | 0.0042813324 |
| 15 | 54 | 0.0114633740 | 0.00160843 | 0.00482529 | 0.0033598183 |
| 16 | 55 | 0.0127170250 | 0.00176092 | 0.00528276 | 0.0026366509 |
| 17 | 56 | 0.0141125250 | 0.00193430 | 0.00580290 | 0.0020691381 |
| 18 | 57 | 0.0156663570 | 0.00213143 | 0.00639429 | 0.0016237767 |
| **19** | 58 | 0.0173969630 | 0.00235554 | 0.00706662 | 0.0012742750 |
| **20** | 59 | 0.0193249700 | 0.00261034 | 0.00783102 | **0.0010000000** |
| **21** | 60 | 0.0214734650 | **0.00290000** | 0.00870000 | **0.0080000000** |
| 22 | 61 | 0.0236169160 | 0.00325949 | 0.00977847 | 0.0080000000 |
| 23 | 62 | 0.0257338530 | 0.00366355 | 0.01099065 | 0.0080000000 |
| 24 | 63 | 0.0278056050 | 0.00411769 | 0.01235307 | 0.0080000000 |
| 25 | 64 | 0.0298164800 | 0.00462814 | 0.01388442 | 0.0080000000 |

`q(40) = 0.00068` and `q(60) = 0.00290` are **ANCHOR** rows, [S3]'s own disclosed 예정 경험
사망률 at those ages, and so is `q(20) = 0.00051`; everything between is the Makeham fit.
At `t = 21` (attained 60) the three headline CI rates read **0.011063 / 0.004371 /
0.003999** exactly — [S3]'s disclosed anchors, again — summing with `other` (0.002040465) and
`ltc` (0) to the 0.0214734650 in the table. **The CI decrement is 3.72 times the death
decrement in policy year 1 and 7.40 times it at attained 60** — 0.0025312484 / 0.00068 and
0.0214734650 / 0.00290 — which is why a projection of this product is a morbidity projection
with a mortality tail rather than the reverse.

`ci_rate(1) = 0.0025312484` is **below** the age-40 table sum of 0.0027834950 because of the
90-day wait:

    0.0027834950 - (1 - 0.7534246575) * 0.001023 = 0.0025312484

Per-cause incidence, male, at the ages worth printing:

| attained age | `cancer` | `ami` | `stroke` | `other` | `ltc` | sum |
|---|---|---|---|---|---|---|
| 20 | 0.000144000 | 0.000027000 | 0.000038000 | 0.000021945 | 0 | 0.000230945 |
| 40 | 0.001023000 | 0.000589000 | 0.000907000 | 0.000264495 | 0 | 0.002783495 |
| 50 | 0.003364142 | 0.001604531 | 0.001904493 | 0.000721682 | 0 | 0.007594848 |
| 60 | 0.011063000 | 0.004371000 | 0.003999000 | 0.002040465 | 0 | 0.021473465 |
| 80 | 0.028353209 | 0.009653117 | 0.007188769 | 0.004745485 | 0.008565526 | 0.058506106 |
| 99 | 0.031734378 | 0.010613464 | 0.007711596 | 0.005256241 | 0.103263346 | 0.158579025 |

The rows at 20, 40 and 60 are [S3]'s for the first three columns; the 80 and 99 rows are the
damped log-slope extrapolation, and the `ltc` column above 65 is the placeholder discussed
above. **Read the last row with the warning attached**: at attained 99 the 장기요양 limb is
two thirds of the whole CI rate and rests on nothing published.

### The first-year 감액 cohort

| Quantity | Cells | Anchor (male) | Female twin (`point_id = 2`) |
|---|---|---|---|
| Share of year-1 accelerations routed to cohort 0 | `ci_reduced_share(1)` | **0.0015224768** | **0.1785788593** |
| Accelerations in year 1 | `pols_ci(1)` | 0.0025312484 | 0.0025101377 |
| Into cohort 0 (reduced) | `pols_ci_in(1, 0)` | 0.0000038538 | 0.0004482575 |
| Into cohort 1 (full) | `pols_ci_in(1, 1)` | 0.0025273947 | 0.0020618802 |
| `accel_benefit_pp(0)` / `resid_nominal_pp(0)` | — | ₩40,000,000 / ₩60,000,000 | same |
| `accel_benefit_pp(1)` / `resid_nominal_pp(1)` | — | ₩80,000,000 / ₩20,000,000 | same |

**The male number is a rounding error and the female number is material**, which is exactly
what the 2003–2005 claim experience would predict: women bought about 150% of the male policy
count and generated about 244% of the male claim count, on breast and thyroid cancer, and the
market's answer from 2008 was a 180-day breast-cancer 부담보 whose lineal descendant this
clause is [R1]. On `point_id = 4`, where `first_year_scope = all`, the share is **1.00000**
and every year-1 acceleration is halved — the GI-generation design [S4].

### First periods of the base run

Per policy issued, income-positive, to two decimal places — the precision the tests assert.
`pols_if` is the **total** in force, pre-CI and post-CI together.

| t | `pols_if` | premiums | claims_ci | claims_death | claims_death_ci | claims_lapse | claims_lapse_ci | claim_expenses | expenses | commissions | net_cf |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 1.000000 | 3,680,880.00 | 202,345.72 | 67,827.88 | 0.00 | 0.00 | 0.00 | 962.86 | 560,000.00 | 2,944,704.00 | −94,960.46 |
| 2 | 0.899643 | 3,301,168.86 | 220,487.09 | 63,074.41 | 107.44 | 95,837.96 | 27.61 | 1,017.66 | 54,518.35 | 99,035.07 | 2,767,063.27 |
| 3 | 0.828861 | 3,029,712.40 | 223,496.20 | 60,242.25 | 232.50 | 155,031.92 | 129.16 | 1,022.32 | 50,731.24 | 90,891.37 | 2,447,935.45 |
| 4 | 0.777714 | 2,830,554.84 | 230,706.13 | 58,782.68 | 369.83 | 177,671.85 | 307.63 | 1,047.04 | 48,076.77 | 84,916.65 | 2,228,676.26 |
| 5 | 0.740045 | 2,680,801.41 | 241,510.24 | 58,362.95 | 524.37 | 180,329.00 | 568.27 | 1,088.61 | 46,205.65 | 80,424.04 | 2,071,788.28 |
| 6 | 0.711873 | 2,565,614.83 | 255,569.54 | 58,780.55 | 701.60 | 172,218.87 | 918.80 | 1,145.25 | 44,891.16 | 76,968.44 | 1,954,420.62 |
| **7** | 0.690531 | 2,475,022.37 | 272,713.12 | 59,910.73 | 966.82 | 158,624.07 | 1,369.16 | 1,216.02 | 43,980.77 | 74,250.67 | 1,861,991.02 |
| 8 | 0.674179 | 2,402,109.36 | 292,880.17 | 61,681.16 | 1,413.19 | 139,275.07 | 1,886.08 | 1,300.60 | 43,368.68 | 72,063.28 | 1,788,241.12 |
| 9 | 0.661516 | 2,341,951.30 | 316,085.82 | 64,051.88 | 2,006.80 | 120,917.74 | 2,513.60 | 1,399.07 | 42,979.60 | 70,258.54 | 1,721,738.25 |
| 10 | 0.651600 | 2,290,957.96 | 342,399.04 | 67,008.12 | 2,790.65 | 104,026.79 | 3,266.73 | 1,511.80 | 42,758.74 | 68,728.74 | 1,658,467.34 |
| 11 | 0.643742 | 2,246,456.27 | 371,927.65 | 70,551.95 | 3,820.76 | 88,809.28 | 4,162.71 | 1,639.42 | 42,665.52 | 67,393.69 | 1,595,485.30 |
| 12 | 0.637425 | 2,206,416.97 | 404,807.21 | 74,699.16 | 5,170.03 | 75,311.49 | 5,221.15 | 1,782.73 | 42,669.32 | 66,192.51 | 1,530,563.38 |
| 19 | 0.612442 | 1,951,820.87 | 741,988.66 | 123,396.38 | 36,300.58 | 20,539.84 | 19,430.89 | 3,320.79 | 43,954.29 | 58,554.63 | 904,334.83 |
| **20** | 0.609667 | 1,910,336.10 | 806,942.87 | 133,615.29 | 47,357.04 | 33,523.33 | 22,857.18 | 3,632.94 | 44,192.65 | 57,310.08 | 760,904.71 |
| **21** | 0.606785 | **0.00** | 876,156.24 | 144,730.49 | 58,914.27 | **265,334.96** | 25,572.73 | 3,972.33 | 44,423.61 | **0.00** | **−1,419,104.62** |
| 22 | 0.600132 | 0.00 | 932,664.85 | 157,102.22 | 73,927.95 | 259,864.97 | 28,519.43 | 4,281.19 | 44,375.84 | 0.00 | −1,500,736.45 |
| 30 | 0.534280 | 0.00 | 1,119,820.70 | 274,344.69 | 370,227.02 | 195,551.95 | 55,220.20 | 6,440.56 | 42,779.95 | 0.00 | −2,064,385.07 |
| **36** | 0.454429 | 0.00 | 939,735.86 | 369,909.07 | 927,116.19 | 137,915.69 | 66,808.55 | 7,972.83 | 38,624.73 | 0.00 | −2,488,082.92 |
| 40 | 0.376450 | 0.00 | 760,086.23 | 421,392.17 | 1,450,315.78 | 101,218.63 | 63,423.56 | 9,143.32 | 33,296.00 | 0.00 | −2,838,875.69 |
| 50 | 0.118327 | 0.00 | 310,774.99 | 376,037.80 | 1,712,695.56 | 28,635.64 | 18,781.38 | 7,761.07 | 11,560.65 | 0.00 | −2,466,247.11 |
| **60** | 0.003694 | 0.00 | 32,650.34 | 59,881.52 | 91,380.48 | 1,173.85 | 71.52 | 580.86 | 398.65 | 0.00 | −186,137.21 |
| **61** | 0.002152 | 0.00 | **0.00** | 48,303.96 | 55,170.51 | 807.14 | 15.24 | 312.26 | 234.62 | 0.00 | −104,843.72 |
| **71** | 0.000000 | 0.00 | 0.00 | 12.35 | 0.00 | 0.00 | 0.00 | 0.04 | 0.01 | 0.00 | −12.41 |

**Seven rows do something.**

- **`t = 1`** carries the whole acquisition cost — ₩500,000 of expense plus ₩2,944,704 of
  commission — and is the only negative year before 완납. `claims_lapse` is **zero** because
  `CV(1) = 0`: `V(1) = ₩2,760,145.77` against `SC(1) = ₩3,381,174.86`, so
  `max(0, V − SC) = 0` and 「이를 영(零)으로 처리한다」 does the flooring [REG-R19]. Every
  published Korean grid shows nil at duration 1.
- **`t = 7`** is where the **105% account floor first binds**: `1.05 × V(7) =
  ₩21,298,539.04` overtakes the ₩20,000,000 nominal residual. It is also the year the
  해약공제액 reaches zero, thirteen years before 납입완료.
- **`t = 20`** is the **cliff**: `cv_pp` goes from ₩30,842,253.88 to ₩65,663,373.78, exactly
  `1 / k = 2.0` on the same anniversary's twin value.
- **`t = 21`** is the **first premium-free year** and the largest single discontinuity in the
  stream. Premium and commission both go to zero, the pre-CI lapse rate steps eightfold from
  0.001 to 0.008, and `net_cf` falls from **+₩760,904.71** to **−₩1,419,104.62** — a swing of
  ₩2.18m in one year.
- **`t = 36`** is where the **post-CI cohort peaks** at 0.221670 policies in force, and the
  first year in which `claims_death_ci` (₩927,116.19) exceeds `claims_ci` (₩939,735.86) is
  the next one. The 20% residual has become the larger stream.
- **`t = 60`** is the **last CI-covered year** (attained age 99).
- **`t = 61`** is the first year with `claims_ci = 0.00`. Nothing else stops: death claims,
  surrenders and expenses all continue for another ten years.
- **`t = 71`** is the horizon: `q = 1`, `pols_if(71) = 1.235e−07` (printed 0.000000),
  everyone dies, and nothing is paid but the pre-CI death benefit.

### The values run at the same anniversaries

| t | `pol_val_pp` | `surr_chg_pp` | `cv_std_pp` | `cv_pp` (pre-CI) | `cv_pp_ci` (post-CI) | `resid_db_avg_pp` |
|---|---|---|---|---|---|---|
| 1 | 2,760,145.77 | 3,381,174.86 | 0.00 | 0.00 | 0.00 | 0.00 |
| 2 | 5,550,566.30 | 2,817,645.71 | 2,732,920.59 | 1,366,460.29 | 2,732,920.59 | 20,060,899.07 |
| 3 | 8,392,607.38 | 2,254,116.57 | 6,138,490.80 | 3,069,245.40 | 6,138,490.80 | 20,029,061.61 |
| 4 | 11,286,594.94 | 1,690,587.43 | 9,596,007.52 | 4,798,003.76 | 9,596,007.52 | 20,018,954.53 |
| 5 | 14,232,900.33 | 1,127,058.29 | 13,105,842.05 | 6,552,921.02 | 13,105,842.05 | 20,013,924.12 |
| 6 | 17,231,963.00 | 563,529.14 | 16,668,433.86 | 8,334,216.93 | 16,668,433.86 | 20,010,881.51 |
| **7** | 20,284,322.89 | **0.00** | 20,284,322.89 | 10,142,161.45 | 20,284,322.89 | **21,307,079.49** |
| 8 | 23,390,658.22 | 0.00 | 23,390,658.22 | 11,695,329.11 | 23,390,658.22 | 24,566,693.06 |
| 9 | 26,551,836.49 | 0.00 | 26,551,836.49 | 13,275,918.24 | 26,551,836.49 | 27,884,412.47 |
| 10 | 29,768,973.76 | 0.00 | 29,768,973.76 | 14,884,486.88 | 29,768,973.76 | 31,261,242.19 |
| 11 | 33,043,510.43 | 0.00 | 33,043,510.43 | 16,521,755.22 | 33,043,510.43 | 34,698,593.36 |
| 12 | 36,377,303.35 | 0.00 | 36,377,303.35 | 18,188,651.67 | 36,377,303.35 | 38,198,350.35 |
| 15 | 46,761,639.79 | 0.00 | 46,761,639.79 | 23,380,819.90 | 46,761,639.79 | 49,100,464.66 |
| **19** | 61,684,507.76 | 0.00 | 61,684,507.76 | **30,842,253.88** | 61,684,507.76 | 64,768,733.14 |
| **20** | 65,663,373.78 | 0.00 | 65,663,373.78 | **65,663,373.78** | 65,663,373.78 | 68,946,542.47 |
| 21 | 66,650,546.84 | 0.00 | 66,650,546.84 | 66,650,546.84 | 66,650,546.84 | 69,983,074.18 |
| 30 | 74,586,898.30 | 0.00 | 74,586,898.30 | 74,586,898.30 | 74,586,898.30 | 78,316,243.21 |
| 40 | 82,400,303.57 | 0.00 | 82,400,303.57 | 82,400,303.57 | 82,400,303.57 | 86,520,318.75 |
| 60 | 93,654,892.89 | 0.00 | 93,654,892.89 | 93,654,892.89 | 93,654,892.89 | 98,337,637.53 |
| 71 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

`base_benefit_pp(t)` is a flat ₩100,000,000 from `t = 1` to `t = 63` and then rises with the
account: ₩100,368,120.65 at `t = 64`, ₩102,439,024.39 at `t = 70`. `accel_benefit_pp(t)` is
correspondingly ₩80,000,000 until then, and `resid_nominal_pp(t)` ₩20,000,000.

**Three readings of this table are the substance of the product.**

**The step at 납입완료 is exactly `1/k` on one anniversary.** `cv_pp(20) / (k × cv_std_pp(20))
= 2.0000000000`. The year-on-year ratio `cv_pp(20) / cv_pp(19) = 2.1290` mixes the step with
the year's account accrual and **must not be quoted as the step**.

**The 해약공제액 is gone at `t = 7`**, thirteen years before the cliff, running off in seven
equal steps of `3,944,704 / 7 = ₩563,529.1428571429`. Nothing about the step at `t = 20` is
a surrender-charge effect.

**`resid_db_avg_pp` sits just above ₩20,000,000 before `t = 7` for a reason that is not the
floor.** Cohort 0 — the first-year breast-cancer cohort — carries a ₩60,000,000 residual and
is inside the average, which is why the mean reads ₩20,060,899.07 at `t = 2` and decays
toward ₩20,000,000 as the full cohorts accumulate. From `t = 7` the average tracks
`1.05 V(t)` and the decay reverses: ₩21,307,079.49, then ₩31,261,242.19 at `t = 10`,
₩49,100,464.66 at `t = 15` and ₩86,520,318.75 at `t = 40`. **The "20% residual" is a
₩20,000,000 promise for six years and an account-value promise for the following fifty-four.**

The policy-loan room at the same anniversaries, showing the doubling the carve-out produces:

| t | `loan_avail_pp` (pre-CI) | `loan_avail_ci_pp` (post-CI) | ratio |
|---|---|---|---|
| 5 | 5,242,336.82 | 10,484,673.64 | 2.00 |
| 7 | 8,113,729.16 | 16,227,458.31 | 2.00 |
| 10 | 11,907,589.50 | 23,815,179.01 | 2.00 |
| 15 | 18,704,655.92 | 37,409,311.83 | 2.00 |
| 19 | 24,673,803.10 | 49,347,606.21 | 2.00 |
| **20** | 52,530,699.02 | 52,530,699.02 | **1.00** |
| 21 | 53,320,437.47 | 53,320,437.47 | 1.00 |

### Hand trace, year 1

Counts. `l0(1) = 1.000000000`, `l1(1) = 0`, `l(1) = 1.000000000`, `lw(1) = 0`, so
`lp(1) = 1.000000000`.

    premiums(1)    = 3,680,880 * 1.000000000                     = 3,680,880.00
    expenses(1)    = 500,000 * 1 + 60,000 * 1.01^0 * 1           =   560,000.00
    commissions(1) = 0.80 * 3,680,880 * 1                        = 2,944,704.00

CI transition, first. `q_ci(1) = 0.0025312484246575`, so

    C(1)     = 1.000000000 * 0.0025312484246575                  = 0.0025312484246575
    phi(1)   = 0.005 * (0.001023 * 0.7534246575) / 0.0025312484  = 0.0015224768480830
    C(1, 0)  = 0.0025312484246575 * 0.0015224768480830           = 0.0000038537671233
    C(1, 1)  = 0.0025312484246575 * 0.9984775231519              = 0.0025273946575342

    claims_ci(1) = 0.0000038537671233 * 40,000,000
                 + 0.0025273946575342 * 80,000,000
                 =        154.15 +    202,191.57               =   202,345.72

Death, second, among those who did not accelerate. `q(1) = 0.00068`:

    D(1)  = 1.000000000 * (1 - 0.0025312484246575) * 0.00068     = 0.0006782787510712
    claims_death(1) = max(0, 100,000,000 - 0) * 0.0006782787510712 =  67,827.88

Surrender, third. `w(1) = 0.10`:

    S(1)  = 1.000000000 * 0.9974687515753 * 0.99932 * 0.10       = 0.0996790472824
    CV(1) = 0.50 * max(0, 2,760,145.7725 - 3,381,174.8571) = 0.50 * 0 = 0.00
    claims_lapse(1) = 0.00 * 0.0996790472824                     =         0.00

Claim expense, on **two** kinds of event:

    claim_expenses(1) = 300,000 * (0.0025312484246575 + 0.0006782787510712 + 0)
                      = 300,000 * 0.0032095271757287             =       962.86

    CF(1) = 3,680,880.00 - 202,345.72 - 67,827.88 - 0.00 - 0.00 - 0.00
                         -     962.86 - 560,000.00 - 2,944,704.00
          = -94,960.46

Update. `l0(2) = 1 − 0.0025312484 − 0.0006782788 − 0.0996790473 = 0.8971114255418441`;
`l1(2) = C(1) = 0.0025312484246575`; `l(2) = 0.8996426739665017`. And the waiver:
`lw(2) = [0 + 1 × 0.0003] × 0.9974687516 × 0.99932 × 0.9003209527 = 0.0002691334277`, so
`lp(2) = 0.8971114255 − 0.0002691334 = 0.8968422921141815`.

### Hand trace, year 2 — the first year with a residual death claim

Counts at the start: `l0(2) = 0.8971114255418441`, `l1(2) = 0.0025312484246575`,
`l(2) = 0.8996426739665017`, `lp(2) = 0.8968422921141815`.

    premiums(2)    = 3,680,880 * 0.8968422921141815              = 3,301,168.86
    expenses(2)    = 60,000 * 1.01^1 * 0.8996426739665017        =    54,518.35
    commissions(2) = 0.03 * 3,301,168.86                         =    99,035.07

CI transition. `q_ci(2) = 0.003072181`, `phi(2) = 0` — the reduced cohort exists in year 1
only:

    C(2)     = 0.8971114255418441 * 0.003072181                  = 0.0027560886764326
    claims_ci(2) = 0.0027560886764326 * 80,000,000               =   220,487.09

Pre-CI death. `q(2) = 0.00070525`:

    D(2)  = 0.8971114255418441 * (1 - 0.003072181) * 0.00070525  = 0.0006307441013243
    claims_death(2) = 100,000,000 * 0.0006307441013243           =    63,074.41

**Post-CI death, cohort by cohort.** `q'(2) = 3.00 × 0.00070525 = 0.00211575`. Two cohorts
exist. `1.05 × V(2) = ₩5,828,094.62`, below both nominals, so both are on their nominal:

    l1(2, 0) = 0.0000038537671233   resid_db(2, 0) = max(60,000,000, 5,828,094.62) = 60,000,000
    l1(2, 1) = 0.0025273946575342   resid_db(2, 1) = max(20,000,000, 5,828,094.62) = 20,000,000

    claims_death_ci(2) = 0.0000038537671233 * 0.00211575 * 60,000,000
                       + 0.0025273946575342 * 0.00211575 * 20,000,000
                       =          0.49      +        106.95        =      107.44

    D'(2) = 0.0025312484246575 * 0.00211575                       = 0.0000053554888545

and `resid_db_avg_pp(2) = (0.0000038537671 × 60,000,000 + 0.0025273947 × 20,000,000) /
0.0025312484 = ₩20,060,899.07` — the cohort-0 effect, visible in one line.

Surrenders. `w(2) = 0.0784759970351461`, `w'(2) = 0.004`:

    S(2)  = 0.8971114255418441 * 0.996927819 * 0.99929475 * 0.0784759970 = 0.0701359284920
    CV(2) = 0.50 * (5,550,566.3032 - 2,817,645.7143) = 0.50 * 2,732,920.5889 = 1,366,460.29
    claims_lapse(2) = 1,366,460.2944697973 * 0.0701359284919917  =    95,837.96

    S'(2) = 0.0025312484246575 * (1 - 0.00211575) * 0.004         = 0.0000101035717432
    CV'(2) = 2,732,920.5889395946                                 the FULL twin value
    claims_lapse_ci(2) = 2,732,920.5889395946 * 0.0000101035717432 =       27.61

    claim_expenses(2) = 300,000 * (0.0027560886764 + 0.0006307441013 + 0.0000053554889)
                      = 300,000 * 0.0033921882666                  =    1,017.66

    CF(2) = 3,301,168.86 - 220,487.09 - 63,074.41 - 107.44 - 95,837.96 - 27.61
                         -   1,017.66 -  54,518.35 - 99,035.07
          = 2,767,063.27

**Read the last two surrender lines together.** The post-CI policyholder surrendering at
duration 2 is paid ₩2,732,920.59 and the pre-CI policyholder at the same duration
₩1,366,460.29 — exactly twice. That is the carve-out, in one row, eighteen years before the
chassis's cliff would have produced it.

### Hand trace, year 7 — the year the 105% floor takes over

Counts: `l0(7) = 0.6736112278450073`, `l1(7) = 0.0169199804209265`,
`l(7) = 0.6905312082659337`, `lw(7) = 0.0012115911986317`,
`lp(7) = 0.6723996366463756`.

    premiums(7)    = 3,680,880 * 0.6723996366463756              = 2,475,022.37
    expenses(7)    = 60,000 * 1.01^6 * 0.6905312082659337
                   = 60,000 * 1.0615201506010 * 0.6905312083     =    43,980.77
    commissions(7) = 0.03 * 2,475,022.3745389110                 =    74,250.67

The floor. `V(7) = ₩20,284,322.8932926692`, so `c V(7) = 1.05 × 20,284,322.8932926692 =
₩21,298,539.0379573030`. One year earlier `c V(6) = 1.05 × 17,231,963.0042976141 =
₩18,093,561.1545124950`, **below** the ₩20,000,000 nominal. The crossing is inside year 7,
and from this anniversary every full cohort's residual is the same number:

    resid_db(7, s) = max(20,000,000.00, 21,298,539.04) = 21,298,539.04   for s = 1 .. 6
    resid_db(7, 0) = max(60,000,000.00, 21,298,539.04) = 60,000,000.00

Six cohorts and the reduced one are in force:

    s = 0:  0.0000037338177352   at 60,000,000.00
    s = 1:  0.0024487289175376   at 21,298,539.04
    s = 2:  0.0026867133117816   at 21,298,539.04
    s = 3:  0.0027403514656868   at 21,298,539.04
    s = 4:  0.0028466616949308   at 21,298,539.04
    s = 5:  0.0029991719154471   at 21,298,539.04
    s = 6:  0.0031946192978073   at 21,298,539.04
            ------------------
    l1(7) = 0.0169199804209265   resid_db_avg_pp(7) = 21,307,079.4852701761

    q'(7)  = 3.00 * 0.00089392 = 0.00268176
    D'(7)  = 0.0169199804209265 * 0.00268176                      = 0.0000453753266936
    claims_death_ci(7) = 0.0169199804209265 * 0.00268176 * 21,307,079.4852701761
                       =      966.82

`surr_chg_pp(7) = 0` — the seventh and last step of `3,944,704 / 7 = 563,529.1428571429`
takes it there — so `cv_std_pp(7) = V(7) = ₩20,284,322.89`, `CV(7) = 0.50 × that =
₩10,142,161.45` and `CV'(7) = ₩20,284,322.89`. The rest of the row follows the year-2
pattern and closes at `CF(7) = +₩1,861,991.02`.

**What this row shows.** From here on, the reserve the model priced — which values the
residual at a flat `r SA` — and the benefit the model pays diverge, permanently and in one
direction. That divergence is the subject of the first entry in *Key sensitivities*.

### Hand trace, year 21 — the first premium-free year

Counts: `l0(21) = 0.5100226227551737`, `l1(21) = 0.0967627562645090`,
`l(21) = 0.6067853790196827`. **`lp(21) = 0`** — `pols_if_pay` is defined as zero beyond
`m` — so premium and renewal commission are both zero.

    premiums(21)    = 0.00
    commissions(21) = 0.00
    expenses(21)    = 60,000 * 1.01^20 * 0.6067853790196827
                    = 60,000 * 1.2201900399480 * 0.6067853790     =    44,423.61

    C(21)  = 0.5100226227551737 * 0.021473465                     = 0.0109519529389414
    claims_ci(21) = 0.0109519529389414 * 80,000,000               =   876,156.24

    D(21)  = 0.5100226227551737 * (1 - 0.021473465) * 0.0029      = 0.0014473049424671
    claims_death(21) = 100,000,000 * 0.0014473049424671           =   144,730.49

    q'(21) = 3.00 * 0.0029 = 0.0087
    D'(21) = 0.0967627562645090 * 0.0087                          = 0.0008418359795012
    c V(21) = 1.05 * 66,650,546.8373005900 = 69,983,074.18
    every cohort, cohort 0 included, is on that floor (60,000,000 < 69,983,074.18)
    claims_death_ci(21) = 0.0008418359795012 * 69,983,074.18         =    58,914.27

    w(21) = 0.008  (the eightfold step from 0.001 at t = 20)
    S(21) = 0.5100226227551737 * 0.978526535 * 0.9971 * 0.008     = 0.0039809869189901
    CV(21) = 1.00 * 66,650,546.8373005900                          the suppression is gone
    claims_lapse(21) = 66,650,546.8373005900 * 0.0039809869189901 =   265,334.96

    S'(21) = 0.0967627562645090 * (1 - 0.0087) * 0.004            = 0.0003836836811400
    claims_lapse_ci(21) = 66,650,546.8373005900 * 0.0003836836811400 =  25,572.73

    claim_expenses(21) = 300,000 * (0.0109519529389 + 0.0014473049425 + 0.0008418359795)
                       = 300,000 * 0.0132410938609                =     3,972.33

    CF(21) = 0.00 - 876,156.24 - 144,730.49 - 58,914.27 - 265,334.96 - 25,572.73
                  -   3,972.33 -  44,423.61
           = -1,419,104.62

**Three things change in this one row and only one of them is the premium.** The premium
stops; the renewal commission stops; and the pre-CI lapse rate steps from 0.001 to 0.008,
multiplying pre-CI surrender outgo eightfold on a value that has itself just doubled. A
fourth has already happened: the 105% floor overtook cohort 0's ₩60,000,000 at `t = 18`, so
by now **every** post-CI cohort carries the same residual. `net_cf` goes from +₩760,904.71
to −₩1,419,104.62 and never returns to positive.

### Roll-forward and undiscounted totals

Every policy issued leaves by one of **four** decrements — the CI transition is not one of
them:

| Decrement | Total over `t = 1 … 71` | Share |
|---|---|---|
| `pols_death` (pre-CI) | 0.1368261313 | 13.68% |
| `pols_death_ci` (post-CI) | 0.4111798384 | 41.12% |
| `pols_lapse` (pre-CI) | 0.4301735885 | 43.02% |
| `pols_lapse_ci` (post-CI) | 0.0218204418 | 2.18% |
| **the four exits** | **1.0000000000** | **100.00%** |
| `pols_ci` (accelerations — a **transition**, not an exit) | **0.4330002802** | 43.30% |

`pols_if(72) = 0`. Person-years: `Σ pols_if = 26.9098928068`, of which
`Σ pols_if_pre = 21.0436025135` and `Σ pols_if_ci = 5.8662902933`;
`Σ pols_if_pay = 13.1487304967`. The post-CI cohort peaks at **0.2216701767 policies in
force at `t = 36`**, attained age 75.

**43.30% of the cohort accelerates; 41.12% die having accelerated and 13.68% die without.**
Of the 54.80% who die in force, three quarters die post-CI. That single pair of numbers is
the product.

Undiscounted totals per policy issued, over `t = 1 … 71`:

| Column | Total (KRW) |
|---|---|
| `premiums` | 48,398,899.11 |
| `claims_ci` | 34,639,868.26 |
| `claims_death` | 13,682,929.43 |
| `claims_death_ci` | **36,441,532.16** |
| `claims_lapse` | 6,222,421.82 |
| `claims_lapse_ci` | 1,627,249.46 |
| `claim_expenses` | 294,301.87 |
| `expenses` | 2,490,051.85 |
| `commissions` | 4,286,244.57 |
| **`net_cf`** | **−51,285,700.32** |

Split by phase: `Σ net_cf` over `t = 1 … 20` is **+₩30,720,479.96** and over `t = 21 … 71`
is **−₩82,006,180.28**.

### Reading the shape of the result

The stream is a twenty-year accumulation followed by a fifty-one-year run-off, and the
undiscounted total of −₩51.3m is not a defect. The contract is balanced on the 2.50%
예정이율 — `P × ä(1)` reproduces `A0(1)` to the won — and undiscounted benefits falling
forty to seventy years out necessarily dwarf undiscounted premiums that stop at year twenty.
What is worth reading is the **composition**, and it says three things that no whole-life
chassis can say.

**The 20% residual is the larger of the two payments.** `claims_death_ci` totals
₩36,441,532.16 against `claims_ci`'s ₩34,639,868.26 and `claims_death`'s ₩13,682,929.43. A
benefit specified as one fifth of the sum assured pays out more, undiscounted, than the four
fifths paid at the acceleration — because 41% of the cohort reaches it and because the 105%
account floor has by then replaced the nominal. **Multiply the post-CI death stream by its
nominal residual instead and it collapses to ₩8,223,730.34**: the floor is worth **4.43×**
the nominal complement over the life of this contract. Anyone who reads "80% now, 20% later"
as a description of where the money goes has the product backwards.

**The morbidity decrement, not the mortality decrement, drives the liability.** Total
benefits are ₩92,614,001.14, of which the two CI-originated streams — the acceleration and
the residual death benefit it creates — are ₩71,081,400.43, or **76.7%**. The pre-CI death
benefit, which is the whole of the chassis's liability, is 14.8% of it. This is a health
product wearing a whole-life chassis, and the 예정위률 grid is where its risk lives.

**And the acceleration is expensive.** Re-running the pricing recursion with `a = 0` on the
identical table and decrements — the same three-state contract, paying the full sum assured
on death whenever it falls — gives `A0(1) = ₩36,085,073.09` and `P = ₩2,386,125.06` against
the anchor's ₩2,968,483.20. **The acceleration costs 24.4% of the net premium**, purely for
moving four fifths of one sum assured forward in time and floorng the remainder at 105% of
the account. Against the market, [S4]'s published grid puts the 80% CI form at 1.19 times the
표준형 종신 office premium at the same cell, and the chassis's anchor puts the CI product at
1.33 times a 저해지 종신 contract on the same life; the model's 24.4% is a **net-premium**
figure on a **fixed decrement basis** and the two published ratios are office premiums across
different products, so they agree in order and are not comparable line by line.

---

## Valuation and reserve pointers

This library projects gross liability cash flows. Every valuation layer consumes them and is
cited, never reproduced. **The chassis sets out all three Korean layers in full** — IFRS 17
(K-IFRS 제1117호, mandatory since 2023-01-01) [REG-R60], K-ICS [REG-R13], the
해약환급금준비금 [REG-R11], the 책임준비금 delegation [REG-R3] [REG-R10], the unpublished
산출방법서 [REG-R2] [REG-R18] and the 선임계리사 sign-off [REG-R5]. Four things are
CI-specific and are stated here.

- **`pol_val_pp` is a 계약자적립액 on a three-state basis, and it is not a reserve.** The
  chassis's point that under K-IFRS 제1117호 the insurer no longer books a 보험료적립금 as a
  separate statutory reserve carries over unchanged. What is new is that the account
  recursion this model asserts, `check_pol_val_roll_fwd()`, carries the **CI decrement in the
  premium annuity and the residual EPV in the outgo term**. A reserve computed on an ordinary
  two-state whole-life recursion is a different number, and on this product it is a wrong
  one: it over-values the premium stream by 4.6% of the annuity.
- **The 해약환급금준비금 test creates an asymmetry the carve-out makes visible.** The
  appropriation compares the IFRS 17 잔여보장요소 against the surrender value computed
  **under 제7-66조제1항 — on that basis even for the 제7-66조제4항 products that may
  contractually pay less** [REG-R11]. So a CI event **doubles** the contractual surrender
  value from one day to the next and changes the reserve the appropriation is measured
  against **not at all**, because that reserve was already on the unsuppressed 별표-14 basis.
  The carve-out is a pure transfer to the CI claimant, visible in the fulfilment cash flows
  and invisible in the surrender-value reserve. `cv_std_pp(t)` is exactly the quantity the
  test needs and is published for that reason.
- **K-ICS: this product loads a sub-risk the chassis barely touches.** The life and
  long-term-health module's seven sub-risks include **장해ㆍ질병위험액**, which on an ordinary
  종신보험 is negligible and here carries 76.7% of the benefit stream. **해지위험액** matters
  for the chassis's reason — the 무·저해지 form and the 대량해지 shock — and **사업비위험액**
  and **사망위험액** are unchanged. The 대량해지 shock magnitudes live in 시행세칙 별표 22,
  which was **not retrieved**, so everything resting on them is second-hand and
  **[unverified]** [REG-R26] [REG-R36]. No `krlib` model computes 요구자본.
- **The 예정위험률 revision right is an unmodelled option inside the liability and it is
  asymmetric.** From five years, with 금융위원회 approval, the insurer may revise the
  예정위험률; where the change raises the premium or the reserve, the default position for a
  policyholder who does not fund the increase is a **reduced sum assured**, not a lapse [S3].
  So the exercise of the right shows up as benefit erosion, not as a decrement, and a
  contract-boundary or CSM analysis that treats it as a repricing right of the ordinary kind
  will mis-place it. It is named here and nowhere modelled.

**And the negative finding that bounds every parameter in this document.** For mortality the
chassis can at least bracket the level from two carriers' published 적용위험률 grids. For CI
morbidity there is **exactly one disclosed table in the whole of Korea and it is fifteen
years old** [S3]. The bureau's 참조순보험요율 is filed and never published [REG-R4]; the
장기손해보험 display that *is* public [REG-R61] is stated on the insured-cancer definition
that excludes C44 and C73, which is not the 중대한 암 definition. **No amount of further
research converts a decrement in this document into a sourced value**; what research can do,
and did, is anchor it on three ages and bound it by two published premium relativities.

---

## Key sensitivities and model risks

In rough order of leverage on this product:

1. **The residual floor multiple `c`.** One number, `1.05`, carries a stream of
   ₩36,441,532.16 — the largest benefit line in the projection. Removing the floor and
   paying the nominal `r B(s)` collapses it to ₩8,223,730.34, a factor of **4.43**. `c` is
   sourced at 1.05 [S1 별표1 주8] and at 1.10 on an older version of the same product [S3],
   so it is a carrier and vintage parameter and is a model point column for that reason;
   `point_id = 9` runs 1.10. **The floor is the single largest structural feature of this
   liability and the easiest to omit.**
2. **The post-CI mortality multiple.** `mort_ci_factor = 3.00` **[std]**, with **no Korean
   source of any kind**. It determines how long the post-CI cohort survives to collect the
   floored residual, and it moves `claims_death_ci` and the post-CI cohort's size in
   opposite directions, so its net effect is not monotone and cannot be reasoned about
   without running it. `point_id = 9` runs 2.00. A user with reinsurer data replaces this
   number first.
3. **The lapse vector.** The `log_linear` 원칙모형 against a level 4% paying-period rate —
   the same 0.8% post-완납 ultimate either way — changes the undiscounted `Σ net_cf` from
   −₩51,285,700.32 to **−₩34,122,514.19**, a third of the liability, because lapse removes
   lives before the acceleration reaches them. Both
   endpoints are supervisory [REG-R27]; the interpolation is **[std]** and the guideline's
   functional form is **[unverified]** at instrument level.
4. **The `ltc` incidence limb above age 65.** A placeholder scaled to an order of magnitude
   [REG-R42] and proportional in shape where a real inception curve is not. It is nil before
   policy year 26 and two thirds of the CI rate at attained 99. Anything read off the tail
   of this projection is read off it.
5. **The `other` limb, at 10.5% of the three headline rates.** Derived from two published
   figures with different denominators [S3] [S4], and flat as a proportion across every age,
   which no real set of seventeen conditions is.
6. **The 90-day wait's annual-grid proration.** `0.7534246575` **[std]** on an assumption of
   uniform first-year incidence. Setting the wait to zero moves the undiscounted `Σ net_cf`
   by only **₩25,542.20** (0.05%), so the *level* is immaterial — but the *mechanism* is not,
   because 부활 restarts the ninety days [S1 별표1 주1] and reinstatement is not modelled.
7. **The first-year 감액 scope.** Immaterial on a male cell — moving `first_year_factor` to
   1.00 changes `Σ net_cf` by ₩149.44 — and material on a female one, where
   `ci_reduced_share(1) = 0.1786` against the male 0.0015. A model tested only on the anchor
   will not notice a bug here.
8. **The horizon and the two boundaries.** `ω = 110` **[std]**; CI cover ends at `n_CI = 60`.
   The eleven post-CI-cover years still carry **₩214,816.68** of claims, and **69.8%** of the
   post-CI death benefit and **42.6%** of all benefits fall after `t = 40`. Truncating the
   projection at the end of CI cover, or at attained age 100, understates materially.
9. **Expense inflation over seventy-one years.** 1.0% **[std]** compounds to **2.01** over
   the run; 3% compounds to **7.92**. There is no published Korean expense basis to anchor
   either.
10. **The base run is a valuation-basis run.** `mort_be_factor = ci_be_factor = 1.00` on
    [S3]'s 예정위험률, which carry a 안전할증 whose cap was 30%, then 50% from 2015, then
    removed from 2017 [R1]. A best-estimate basis sits below 1.00 on both and `point_id = 9`
    is where the levers are exercised.

### Known modeling pitfalls

Each of these is a mistake a competent modeller would actually make on this product, and
each is checkable.

- **The acceleration is a transition, not an exit.** `check_pols_roll_fwd()` asserts
  `l(t) − l(t+1) = D + D' + S + S'` — **four** terms. Adding `C(t)` removes every CI
  claimant from the population on the day they claim, which is precisely what 감독규정
  제7-60조제8호 forbids the contract to do [REG-R16]. The symptom is a decrement sum above 1
  and a post-CI cohort that never accumulates.
- **The residual floor is two-sided.** `max(r B(s), c V(t))`, not `r B(s)` and not `c V(t)`.
  A one-sided max is right for most of the projection and wrong at the ends: before `t = 7`
  the nominal binds and after it the account does, and cohort 0's ₩60,000,000 stays on the
  nominal until `t = 18`. `check_resid_floor()` tests both limbs separately for a reason.
- **The floor is read off the current anniversary and the nominal off the entry
  anniversary.** `resid_db_pp(t, s) = max(r B(s), c V(t))` mixes two clocks on purpose:
  `B(s)` is the 기본보험금 at the acceleration date, `V(t)` the account **now**. Reading both
  off `t`, or both off `s`, is wrong in opposite directions and neither error shows up before
  `t = 7`.
- **Collapsing the post-CI cohorts loses the first-year reduced one.** Cohort 0 carries
  ₩60,000,000 where every other cohort carries ₩20,000,000, and it survives the whole
  projection. On a male cell it is 0.15% of year-1 accelerations and the error is invisible;
  on the female twin it is 17.86% and it is not. Test on `point_id = 2` or `4`, never only on
  `point_id = 1`.
- **The premium annuity must carry the CI decrement.** `ä` discounts on `(1 − q_ci)(1 − q)`.
  Using an ordinary life annuity gives 15.8467943703 against the correct 15.1228758581 —
  a 4.8% over-statement, and a net premium of ₩2,832,875.97 against ₩2,968,483.20 — and
  `check_pol_val_roll_fwd()` fails immediately, which is what it is for.
- **The post-CI cohort never pays a premium.** `pols_if_pay(t)` is
  `pols_if_pre(t) − pols_waived(t)` and the post-CI count is nowhere in it, because a
  CI/LTC 지급사유 waives all future
  기본보험료 [S1 별표1 주4]. Weighting premium by `pols_if(t)` reproduces the base run's
  first year exactly and diverges from year 2 onward — a slow, quiet error worth
  **0.695569** person-years of spurious premium inside the 납입기간, about ₩2.56m.
- **The suppression has two exits, and one of them is random.** `cv_pp_ci(t) = cv_std_pp(t)`
  at **every** duration, not from `t = m`. Applying `k` to the post-CI cohort halves the
  surrender benefit of exactly the policyholders the carve-out exists to protect, and
  `check_cv_carve_out()` catches it. Over the whole projection the carve-out is worth only
  **₩52,813.69** — ₩1,627,249.46 paid against ₩1,574,435.76 on the suppressed counterfactual,
  a **3.4%** uplift — because most post-CI surrenders happen after 납입완료 anyway. So this
  bug is **nearly invisible in the totals and factor-of-two wrong at every individual
  duration inside 납입기간**. Test it at `t = 2`, not on the sum.
- **The step at 납입완료 is `1/k` on one anniversary.** `cv_pp(20) / (k × cv_std_pp(20))
  = 2.0000000000` exactly. The adjacent-year ratio `cv_pp(20) / cv_pp(19) = 2.1290` includes
  a year of account accrual and is not the step. Interpolating, grading or smoothing the
  boundary is wrong; so is paying year-`m` surrenders on the suppressed basis.
- **The step is not a surrender-charge effect.** `surr_chg_pp(t) = 0` from `t = 7`, thirteen
  years before the cliff, running off in seven equal steps of ₩563,529.1428571429. A model
  that ties the two together will place the cliff at the wrong duration on any point where
  `m ≠ 7`.
- **The 표준해약공제액 uses the pre-acceleration sum assured.** ₩100,000,000, not the
  ₩20,000,000 residual: 별표 15 제3호 read with 제8호 takes the 일반사망보험금 before any
  증감 [REG-R21]. Using the residual would cut the statutory cap from ₩3,944,704 to
  ₩3,144,704, a 20% under-statement of the surrender charge.
- **CI before death before lapse.** Reversing the first two routes lives that would have
  accelerated into the death decrement, which is 3.72 times smaller in policy year 1 and
  7.40 times smaller at attained 60. The order is [std] and it is asserted; state your own
  convention before comparing numbers with anyone.
- **The two payments are one step apart, not simultaneous.** A life accelerating in year `t`
  joins the post-CI state at the **start of year `t + 1`** and is not exposed to `q'` until
  then. Paying an acceleration and a residual death benefit in the same year on the same life
  double-counts the claim expense and mis-times the residual.
- **The CI decrement stops at `n_CI` and nothing else does.** `ci_rate(t) = 0` from `t = 61`
  on the anchor; premiums stop at `t = 21`; death claims, surrenders and maintenance expense
  run to `t = 71`. Three different end dates in one projection, and only one of them is the
  horizon.
- **`ci_rate` is a first-event rate, not a sum of marginal incidences.** The benefit is
  payable once across the whole trigger set [S1 별표1], and the Korean supervisor required
  the overlap to be in the filed rate [R1]. Building the table by adding published
  site-specific incidences double-counts every life with two qualifying conditions.
- **There is no survival period.** Importing the overseas 30-day requirement moves lives from
  the CI decrement to the death decrement and changes the benefit they are paid from
  `a B + later r B` to `B` once. The Korean supervisor refused the requirement expressly
  [R1].
- **`pols_if` is the total in force, both states.** It is the weight on maintenance expense
  and it is **not** the pre-CI count. Weighting maintenance by `pols_if_pre` drops **48.8%**
  of the in-force count at `t = 36`; weighting premium by `pols_if` adds a cohort that pays
  nothing.
- **The claim expense is charged on three events, not one.** CI, pre-CI death and post-CI
  death. Charging it on deaths alone under-states the expense stream by 44%.
- **Everything the loan touches is floored at zero, and the acceleration is not netted at
  all.** `max(0, B − L)`, `max(0, resid_db − L)`, `max(0, CV − L)`, `max(0, CV' − L)`; the
  선지급 is paid gross **[std]**, no retrieved document saying otherwise. And the loan room
  itself is computed off the **payable** value, so it doubles at the acceleration date —
  ₩23,581,915.16 against ₩47,163,830.33 at `t = 12` on `point_id = 7`.
- **The two decrement tables are not the chassis's.** `ω = 110` here against 115 there, and
  the two files are fitted to different anchors on different bases. Swapping them changes the
  horizon by five years and the whole mortality level.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #krlib-ci_insurance-r1
[R10]: #krlib-ci_insurance-r10
[R11]: #krlib-ci_insurance-r11
[R13]: #krlib-ci_insurance-r13
[R16]: #krlib-ci_insurance-r16
[R3]: #krlib-ci_insurance-r3
[R5]: #krlib-ci_insurance-r5
[R6]: #krlib-ci_insurance-r6
[R7]: #krlib-ci_insurance-r7
[REG-R1]: #krlib-reg-r1
[REG-R10]: #krlib-reg-r10
[REG-R11]: #krlib-reg-r11
[REG-R13]: #krlib-reg-r13
[REG-R16]: #krlib-reg-r16
[REG-R18]: #krlib-reg-r18
[REG-R19]: #krlib-reg-r19
[REG-R2]: #krlib-reg-r2
[REG-R20]: #krlib-reg-r20
[REG-R21]: #krlib-reg-r21
[REG-R25]: #krlib-reg-r25
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
[REG-R40]: #krlib-reg-r40
[REG-R42]: #krlib-reg-r42
[REG-R48]: #krlib-reg-r48
[REG-R5]: #krlib-reg-r5
[REG-R52]: #krlib-reg-r52
[REG-R55]: #krlib-reg-r55
[REG-R60]: #krlib-reg-r60
[REG-R61]: #krlib-reg-r61
[std]: #krlib-std
[unverified]: #krlib-unverified
<!-- END generated citation links -->
