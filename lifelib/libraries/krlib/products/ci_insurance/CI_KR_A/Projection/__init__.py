# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-policy projection of the :mod:`~.CI_KR_A` model.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace
projecting model point 1::

    >>> Projection[1].result_cf()          # the worked example's anchor cell
    >>> Projection.point_id = 3            # or switch the default

``t`` counts **policy years**, 1-based: ``t = 1`` is the first policy year and
``t = proj_len() = omega_age() - age_at_entry() + 1`` the last. There is no maturity date
and no 만기보험금; the horizon is the terminal age of the mortality table, every remaining
life dies in year ``proj_len()``, and nothing is paid there but a death benefit.

.. rubric:: The age basis

Ages are **보험나이** (*boheom nai*, insurance age): 만나이 at the 계약일 with a fraction
under six months discarded and six months or more rounded up, incrementing on each
계약해당일. It is the contractual age, the index of every Korean rate card, and the basis
[S3]'s disclosed 예정위험률 grid is stated on, so a projection stepped on anniversaries
steps it correctly by construction. The one contractual exception — 계약의 무효 for an
age outside the permitted range, which is judged on 만나이 — produces no cash flow and is
not modelled. This is a **보험나이** model throughout; nothing here is on 만나이, and the
two differ by about half a year of ageing on every row.

.. rubric:: Input data

Inputs are **external files**: plain CSVs in the model folder's parent directory,
``products/ci_insurance/``, read at run time rather than stored inside the model. The
model folder therefore holds nothing but formulas. This follows ``annuallife.TradLife_A``;
contrast ``basiclife.BasicTerm_S``, which keeps its inputs *inside* the model.

Each table has a filename Reference and a reader Cells, both on :mod:`~.CI_KR_A.Data`,
reached here through the ``data`` Reference:

======================  ==================================  ==========================
Reference               Cells                               File
======================  ==================================  ==========================
model_point_file        data.model_point_table()            model_point_table.csv
mort_table_file         data.mort_table()                   mort_table.csv
ci_incidence_file       data.ci_incidence_table()           ci_incidence_table.csv
lapse_table_file        data.lapse_table()                  lapse_table.csv
======================  ==================================  ==========================

.. rubric:: Naming

Cells names follow lifelib's ``basiclife.BasicTerm_S`` and ``savings.CashValue_SE``
wherever those models have an analogue — ``pols_*`` for policy counts, plural nouns for
cash flows, ``*_rate`` for rates, ``*_pp`` for per-policy amounts, ``claims(t, kind)``
with an uppercase ``kind`` string. The technical notes use compact actuarial symbols
instead. The mapping is:

=========================  ==================================  ============================
Notes symbol               Cells                               Meaning
=========================  ==================================  ============================
(none)                     model_point()                       The selected model point row
x                          age_at_entry()                      가입나이 at issue, 보험나이
x + t - 1                  age(t)                              Attained age in year t
omega                      omega_age()                         Terminal age of the table
T                          proj_len()                          Projection length in years
m                          prem_term(), prem_period()          납입기간
(none)                     prem_end()                          Last year a premium is due
n_CI                       ci_cover_end()                      Last year of CI cover
SA                         sum_assured()                       보험가입금액
G                          premium_pp()                        Annual gross premium
P                          prem_net_level_pp()                 Annual net level premium
i                          prem_int_rate                       예정이율
a                          accel_rate()                        선지급 비율
r = 1 - a                  resid_rate()                        Residual death fraction
c                          resid_floor_mult()                  계약자적립금 floor multiple
f                          first_year_factor                   First-year 감액 factor
k                          cv_floor_ratio()                    저해지 suppression factor
q(x+t)                     mort_rate(t)                        Pre-CI death decrement
q'(x+t)                    mort_rate_ci(t)                     Post-CI death decrement
(table q)                  mort_rate_at_age(y)                 Table rate at attained age y
(none)                     mort_rate_base(t)                   Pricing-basis rate in year t
q_ci(t)                    ci_rate(t)                          The CI decrement
(none)                     ci_rate_base(t)                     Pricing-basis CI rate
(by cause)                 ci_rate_at_age(y, cause)            Table rate by cause
w(t)                       lapse_rate(t)                       Pre-CI surrender rate
w'(t)                      lapse_rate_ci(t)                    Post-CI surrender rate
(none)                     disc_factor()                       1 / (1 + i)
A1(t)                      epv_resid(t)                        EPV of the residual, post-CI
A0(t)                      epv_ben(t)                          EPV of all benefits, pre-CI
a-double-dot(t)            annuity_due(t)                      EPV of 1 p.a. while pre-CI
V(t)                       pol_val_pp(t)                       계약자적립액 at anniversary t
cumprem(t)                 cum_prem_pp(t)                      Premiums paid to year t
B(t)                       base_benefit_pp(t)                  기본보험금
SC_max                     surr_chg_cap_pp()                   표준해약공제액
SC(t)                      surr_chg_pp(t)                      해약공제액
W(t)                       cv_std_pp(t)                        표준형 twin's 해약환급금
CV(t)                      cv_pp(t)                            Payable value, pre-CI
CV'(t)                     cv_pp_ci(t)                         Payable value, post-CI
(none)                     cv_mult(t)                          k or 1, by policy year
a B(s)                     accel_benefit_pp(s)                 The 선지급 of cohort s
r B(s)                     resid_nominal_pp(s)                 Nominal residual of cohort s
max(rB, cV)                resid_db_pp(t, s)                   Residual death benefit
(weighted mean)            resid_db_avg_pp(t)                  In-force mean residual
L(t)                       loan_pp(t)                          보험계약대출 balance
i_L                        i_loan                              보험계약대출이율
(available)                loan_avail_pp(t)                    Loan limit, pre-CI
(available)                loan_avail_ci_pp(t)                 Loan limit, post-CI
l(t)                       pols_if(t)                          In force, start of year t
l0(t)                      pols_if_pre(t)                      In force and pre-CI
l1(t)                      pols_if_ci(t)                       In force and post-CI
l1(t, s)                   pols_if_ci_at(t, s)                 Post-CI, by cohort s
lp(t)                      pols_if_pay(t)                      In force and paying
(waived)                   pols_waived(t)                      Waived on 장해 50%+
C(t)                       pols_ci(t)                          CI accelerations in year t
C(t, s)                    pols_ci_in(t, s)                    Entrants into cohort s
D(t)                       pols_death(t)                       Pre-CI deaths in year t
D'(t)                      pols_death_ci(t)                    Post-CI deaths in year t
S(t)                       pols_lapse(t)                       Pre-CI surrenders
S'(t)                      pols_lapse_ci(t)                    Post-CI surrenders
G lp(t)                    premiums(t)                         Premium income
(by kind)                  claims(t, kind)                     Benefit outgo by kind
ec                         claim_expenses(t)                   Claim expense
E0, e(t)                   expenses(t)                         Acquisition and maintenance
c0, c_r                    commissions(t)                      Commission outgo
CF(t)                      net_cf(t)                           Net cash flow, income positive
=========================  ==================================  ============================

.. rubric:: The acceleration, in one paragraph

On the first qualifying event the insurer pays ``a B(t)``, the contract does **not**
terminate, the death benefit becomes ``max(r B(t_CI), c V(s))`` for every later ``s``, and
the premium stops. The contract's survival is a regulatory requirement and not a design
choice: 감독규정 제7-60조제8호 forbids a contract to be extinguished while the risk it
covers remains effective [REG-R16]. **The complement is exact** — ``a + r = 1``, and
:func:`check_accel_complement` asserts it cohort by cohort — so the acceleration
redistributes one sum assured across two dates and never adds cover.

.. rubric:: Two cohorts, and why the post-CI one is indexed by its entry year

:func:`pols_if_pre` and :func:`pols_if_ci` are the two states, and the second is carried
**by the policy year it accelerated in**, :func:`pols_if_ci_at`. That is not tidiness: the
residual a post-CI policy carries was fixed at its own acceleration date, at ``r`` times
the 기본보험금 *then*, and the 기본보험금 grows with the account. Collapsing the cohorts
to one average residual would let a policy that accelerated at duration 3 inherit the
larger residual of one that accelerated at duration 40.

Cohort ``0`` is the exception and is the first-year 감액 cohort: a breast-cancer claim in
policy year 1 is paid at ``a f B(1)`` with ``f = 0.5`` and leaves a residual of
``(1 - a f) B(1)``, which is a different amount from every other cohort's. Where the model
point sets ``first_year_scope`` to ``all``, the whole of year one's accelerations go into
it, which is the GI-generation design.

.. rubric:: Processing order

Within policy year ``t``, in this order **[std order]**: premium, acquisition expense,
maintenance expense and commission at the start of the year; then the CI transition;
then death among those who did not accelerate; then surrender among those who neither
accelerated nor died. A life accelerating in year ``t`` receives ``a B(t)`` at the end of
year ``t`` and joins the post-CI cohort at the start of year ``t + 1``, so it is not
exposed to the residual death benefit until the following year. That lag is deliberate
and conservative in the right direction: the 장해분류표 defers assessment of a 중대한
뇌졸중 for **twelve months** after onset [S1 별표3], so a CI claim and the death that may
follow it are not simultaneous events even on a finer grid.

.. rubric:: One policy value, three surrender values

There is a single ``V(t)`` in this model, :func:`pol_val_pp`, the 계약자적립액 of the
**표준형 twin** — the non-marketed comparison contract. The 해약환급금 is
``W(t) = max(0, V(t) - SC(t))`` and the amount actually payable is a multiplier on it:

* ``cv_pp(t) = k W(t)`` for a pre-CI policy inside the 납입기간, ``W(t)`` after it;
* ``cv_pp_ci(t) = W(t)`` for a post-CI policy at **every** duration.

**The suppression therefore has two exits, not one: 납입완료 and a CI/LTC 지급사유.** The
second is contractual — [S2] conditions the suppression on 「CI/LTC보험금 지급사유가
발생하지 않은 경우」 and [S4] on 「「선지급 진단보험금」 지급사유 발생 전 납입기간 동안」 —
and it is the CI-specific delta on the chassis, whose cliff is a deterministic function of
duration. Here it is at ``min(m, t_CI)``, a **random** date correlated with the product's
own decrement. :func:`check_cv_carve_out` asserts the consequence the carve-out exists to
produce: a CI claimant is never worse off on surrender than an unaccelerated policyholder
at the same duration.

The same carve-out **doubles the policy loan** at the acceleration date, because the loan
is computed off the payable value: compare :func:`loan_avail_pp` with
:func:`loan_avail_ci_pp` at any duration inside the 납입기간.

.. rubric:: The pricing basis, and what it deliberately leaves out

:func:`pol_val_pp` is a prospective net level premium reserve on the 예정이율 and the
shipped tables, solved from :func:`epv_ben` and :func:`annuity_due` and asserted by
:func:`check_pol_val_roll_fwd`. Two simplifications are **[std]** and are stated rather
than hidden. The pricing recursion values benefits at ``SA`` and the residual at
``r SA``, ignoring both floors on the 기본보험금 and the 105% floor under the residual;
pricing the second one in would make ``V`` self-referential, since the floor is a multiple
of ``V`` itself. And the reserve is computed on the **pricing** decrements, not the
best-estimate ones, which is what makes the identity testable at all. The floors are
benefit-payment rules and are applied in full in the cash-flow projection, where
:func:`check_resid_floor` asserts them.

The gross premium is a model point input. On the anchor cell it is **sourced**: ₩306,740
a month is published for exactly that cell and the annual figure is twelve times it
**[std]**, no carrier publishing an annual-mode scale, so the annual premium is slightly
overstated. On the other cells it is this model's own ``prem_net_level_pp()`` grossed up
by the loading the anchor implies, times the published 저해지-to-기본환급형 form factor
**[std]**. The relativity that falls out is a check rather than an input: the model prices
the 80% form at 1.079 times the 50% form at male 40, against the 1.085 [S4] publishes.

.. rubric:: 예정위험률 are not a best estimate

``mort_be_factor`` and ``ci_be_factor`` are 1.00 on every model point but one, so the base
run is a **valuation-basis run**. [S3]'s rates are 예정위험률 carrying a 안전할증 whose
regulatory cap was 30% in the early 2000s, 50% from 2015 and removed in 2017 [R1]; no
retrieved source sizes the margin against current Korean insured experience, so any
best-estimate basis derived from them is a standardization and model point 9 is where it
is exercised.

.. rubric:: Modules that are off in the base run

* **보험계약대출**, ``pol_loan_util`` at 0, drawn on model point 7 at duration 12 — inside
  the 납입기간, so the suppressed base binds and the doubling at a CI event is visible.
* **The 표준형 lapse basis**, ``lapse_basis`` at ``table``. The suppressed forms run the
  **로그-선형 원칙모형** of the IFRS17 주요 계리가정 가이드라인 instead, converging to
  0.1% at 납입완료 with a 0.8% post-완납 ultimate [REG-R27]. No separate 완납 surrender
  spike is imposed: the eightfold step at 납입완료 is produced by the guideline's own
  shape.
* **The all-trigger first-year 감액**, ``first_year_scope`` at ``all``, on model point 4.
* **The best-estimate levers**, on model point 9, which also carries the 110% residual
  floor multiple [S3] publishes instead of 105%.

.. rubric:: What is not modelled, and is named so that it is not mistaken for absent

중도인출 and 추가납입 are arguments of the 기본보험금 definition [S1 별표1 주7] and are
held at **zero** rather than dropped. 부활 and the 90-day 중대한 암 보장개시일 it restarts,
the 예정위험률 revision right that takes effect as a **benefit reduction** rather than a
lapse, the 가지급제도, 감액, 연금전환 (which appears in no retrieved CI 약관) and the
multi-pay CI generation are all outside this model. So is any 요구자본: the projection
produces gross liability cash flows and leaves the 책임준비금, the IFRS 17 CSM and the
K-ICS 장해ㆍ질병위험액 to a layer that consumes them.

.. rubric:: Sign convention

:func:`net_cf` is **income positive** — premiums less claims, expenses and commission —
which is the notes' own sign and the library-wide one, so there is no outgo-positive
``liability_cf`` companion to publish.
"""

from modelx.serialize.jsonvalues import *

_formula = lambda point_id: None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def model_point():
    """The selected model point as a Series."""
    return data.model_point_table().loc[point_id]                    # noqa: F821


def sex():
    """The sex of the insured, M or F; the two are rated and tabulated separately.

    The sex effect on this product runs in **opposite directions** on price and on
    incidence, and a reader must not infer one from the other.  Female premium is
    0.79-0.86 of male on the published grid [S4], while at age 40 the three headline CI
    rates sum to 1.10 times the male ones [S3] — the excess being breast and thyroid
    cancer, which is exactly the exposure that broke the 2002 pricing [R1].  The
    reconciliation is that the premium is dominated by the death benefit, by old-age CI
    incidence where the female rates are far below the male ones, and by the savings
    element, which is sex-neutral.
    """
    v = model_point()["sex"]
    if v not in ("M", "F"):
        raise ValueError("invalid sex")
    return v


def age_at_entry():
    """x: the 가입나이 at issue on **보험나이**, 15 to 60.

    보험나이 (*boheom nai*, insurance age) is 만나이 at the 계약일 with a fraction under
    six months discarded and six months or more rounded up, incrementing on each
    계약해당일 [S1 제26조] [REG-R25 제21조].  The 15-60 envelope is invariant across every
    CI source retrieved [S3] [S4] [R13] and is five years below the whole life chassis's
    15-65 ceiling.
    """
    return int(model_point()["issue_age"])


def sum_assured():
    """SA: the 보험가입금액 at issue, level for life.

    The envelope is ₩10,000,000 to ₩200,000,000, and the underwriting cap binds the
    **accelerated** exposure rather than the face amount: [S3] publishes 2,000만-1억
    5,000만원 on the 50% form against 1,000만-9,000만원 on the 80% form, so
    0.5 x 1억5,000만 and 0.8 x 9,000만 are within 4% of each other [S3].  중도인출 and
    추가납입 are held at zero **[std]**, so ``SA`` is also the 기본사망보험금 of
    [S1 별표1 주7].
    """
    return float(model_point()["sum_assured"])


def pols_if_init():
    """The number of policies in force at the start of the first projected year.

    1 on every shipped model point: these are single-policy cells, as everywhere in this
    library.  It is read from the model point rather than hard-coded so that a user can
    project a block by scaling one row.
    """
    return float(model_point()["pols_if_init"])


def prem_term():
    """m: the 납입기간 in years, as entered on the model point.

    20년납 on the anchor, which is the term every published Korean CI rate card and every
    해약환급금 illustration in the source set is quoted on [S3] [S4], and which puts
    납입완료 at attained age 60 — well inside the CI cover period, so the surrender-value
    step and the acceleration can be observed separately.  The menu runs 5 to 30년납 in
    fives and 55 to 80세납, with 5년납 and 10년납 offered on the 기본환급형 only [S4].
    """
    return int(model_point()["prem_term"])


def prem_period():
    """m: the effective 납입기간, and the duration at which the suppression would end.

    Identical to :func:`prem_term` on every shipped point; the cells exists because the
    chassis admits a 종신납 form on which the suppressed period runs for life, and a model
    reading ``prem_term`` directly would silently mis-place the step if one were added.
    """
    return prem_term() if prem_term() > 0 else proj_len()


def prem_end():
    """The last policy year in which a premium is actually due.

    ``prem_period()``.  Nothing else about the contract stops there: maintenance expense,
    death cover, CI cover to 100세 and the account value all continue, which is the
    structural point of a whole-life chassis and the reason a projection truncated at
    납입완료 misses the majority of the liability.
    """
    return prem_period()


def premium_pp():
    """G: the level annual gross premium per policy, payable in advance in years 1 to m.

    Level and guaranteed for the whole of 납입기간, subject only to the statutory
    예정위험률 revision right from five years — which, where it bites, is applied by
    **reducing the benefit or the sum assured** rather than by raising the premium [S3],
    so its exercise would show up as benefit erosion and not as a decrement.  There is no
    renewal mechanic on the main contract.

    On the anchor cell the value is **sourced**: ₩306,740 a month is published for 남 40,
    80% 선지급형, 17대보장형, 해지환급금이 적은 유형, 1억원, 20년납, 월납, net of the
    고액계약할인, and the annual figure is twelve times it **[std]** — no carrier publishes
    an annual-mode scale, so the modal discount a real 연납 rate would carry is not applied
    and the annual premium is slightly overstated [S4].  On the other cells it is this
    model's own :func:`prem_net_level_pp` grossed up by the 1.2400 loading the anchor
    implies, times the 저해지-to-기본환급형 form factor of 1.10224 published for one
    identical cell [S4], with 0.937 for the 무해지 form **[std]**.
    """
    return float(model_point()["premium_annual"])


def accel_rate():
    """a: the 선지급 비율, the fraction of the 기본보험금 the CI benefit pays.

    0.80 on the composite, 0.50 as a model point flag; both appear together in every
    complete 약관 retrieved [S1] [S2] [S3] [S4] [S5] [S6].  **Paid once only across the
    whole trigger set** — eight 중대한 질병, four 중대한 수술, 중대한 화상 및 부식 and
    장기요양상태 — so ``ci_rate`` is a first-event rate and not a sum of marginal
    incidences [S1 별표1] [R1].

    80% is the composite's choice for three reasons stated in ``product-spec.md``, of
    which the modelling one is that the residual's 105%-of-account floor actually binds
    inside a normal projection on this form: at the anchor cell ``r SA`` is ₩20,000,000
    and the floor takes over as soon as ``V(t)`` passes ₩19,050,000.  On the 50% form the
    same test needs ₩47,600,000 and is reached far later.  The 100% 선지급플러스형 is
    excluded because it is not a pure acceleration: it extinguishes the death benefit and
    replaces it with a separately funded 유족위로금 [S4].
    """
    a = float(model_point()["accel_rate"])
    if not 0.0 < a < 1.0:
        raise ValueError("accel_rate must lie strictly between 0 and 1")
    return a


def resid_rate():
    """r = 1 - a: the residual death fraction, the exact complement of the acceleration.

    ``80 + 20 = 100`` and ``40 + 60 = 100`` exactly [S1] [S2].  **The acceleration never
    adds cover**, and keeping ``r`` as the arithmetic complement rather than as a second
    model point column is what makes that unfalsifiable here;
    :func:`check_accel_complement` asserts it against the 기본보험금 cohort by cohort.
    """
    return 1.0 - accel_rate()


def resid_floor_mult():
    """c: the 계약자적립금 multiple flooring the post-CI death benefit.

    1.05 at [S1 별표1 주8], 1.10 at [S3]'s older universal version of the same product, so
    it is a carrier and vintage parameter and is carried as one rather than hard-coded.
    The clause reads 「CI/LTC보험금 지급사유 발생당시의 기본보험금의 20%와 … 계약자적립금의
    105% 중 큰 금액」, which is why the residual is a **growing** quantity and not the
    stated complement: on a long-surviving post-CI policy the account overtakes the nominal
    and the floor becomes the benefit.
    """
    return float(model_point()["resid_floor_mult"])


def cv_floor_ratio():
    """k: the 저해지환급형 suppression factor applied to the 표준형 twin's 해약환급금.

    1.00 표준형 / 기본환급형, 0.50 저해지환급형, 0.00 무해지환급형.  [S2] states both
    grades it offers in terms — 「'30% 저해지환급형'의 경우 '기본형' 해지환급금의 30%…
    '50% 저해지환급형'의 경우 … 50%」 — and 0.50 is taken because it is the modal fraction
    on the chassis and one of the two grades this carrier offers on the CI product itself
    **[std]**.  [S4] rebrands the same mechanic as 해지환급금이 적은 유형 and prices it
    9-12% below the 기본환급형.

    The suppression is a **regulatory dispensation** rather than a contractual gimmick:
    감독규정 제7-66조제4항 permits an insurer to pay less than the 별표-14 floor only where
    the premium was calculated on a 최적해지율, which is why the lapse assumption on this
    product is a supervisory matter [REG-R19] [REG-R27].
    """
    k = float(model_point()["cv_floor_ratio"])
    if not 0.0 <= k <= 1.0:
        raise ValueError("invalid cv_floor_ratio")
    return k


def first_year_scope():
    """The scope of the first-year 감액: ``breast`` (the composite) or ``all``.

    Two designs are in the sources and they differ in **scope, not in depth** — both
    halve.  [S1] and [S2] reduce only for breast cancer and only in the first policy year,
    so an 80% form pays 40% and the death benefit's complement rises to 60% [S1 별표1]
    [S2 별표1].  [S4]'s GI product halves **every** trigger in the first year, carving back
    only a 중대한 화상 및 부식 claim on the 17대보장형 [S4].

    The composite takes the breast-cancer design because it is the CI-generation design in
    both complete 약관 retrieved and because it is the only one with an identifiable
    experience rationale: it is the lineal descendant of the 180-day breast-cancer 부담보
    imposed across the market from 2008 after the female claim excess of 2003-2005 [R1].
    The modelling consequence is real — it requires the 중대한 암 incidence to be split
    into a breast component and the rest, which :func:`breast_share` supplies.
    """
    v = model_point()["first_year_scope"]
    if v not in ("breast", "all"):
        raise ValueError("invalid first_year_scope")
    return v


def breast_share():
    """The share of 중대한 암 incidence attributable to breast cancer **[std]**.

    0.268 for females and 0.005 for males, calibrated on the national cancer registry
    [REG-R40]: 유방 29,871 cases in 2023 against female cases of 137,487 less the 19.0%
    of the female burden that is 갑상선, which 중대한 암 excludes as C73 — so
    29,871 / 111,364 = 0.268.  Male breast cancer is under 1% of breast cases and is
    carried at 0.005 rather than nil so that the male first-year 감액 is present and
    negligible rather than absent and unexplained.

    The registry publishes incidence on **만나이** while this model runs on 보험나이; the
    quantity used here is a *share* of one age's incidence, which is first-order
    insensitive to the half-year shift, and no adjustment is made **[std]**.
    """
    return breast_share_f if sex() == "F" else breast_share_m        # noqa: F821


def lapse_basis():
    """The surrender basis: ``log_linear`` (the 원칙모형) or ``table`` (the 표준형 curve).

    The IFRS17 주요 계리가정 가이드라인 of 2024-11-07 adopts a **로그-선형 모형** as the
    원칙모형 for 무·저해지 lapse rates, converging to 0.1% at 납입완료 with a 0.8%
    post-완납 ultimate; departure is permitted only on disclosure, against the principle
    model, of the CSM, best-estimate liability, K-ICS and net-income differences
    [REG-R27] [R3].  The suppressed model points run it; the 기본환급형 points run the
    표준형 duration curve in ``lapse_table.csv``.  **Carrying both is the comparison the
    guideline requires an insurer to disclose**, and it is the reason the table survives
    on a product whose representative form does not use it.

    The problem the supervisor named bites here with particular force: with no experience
    on 무·저해지 business, insurers assumed high lapse right up to 완납, which flatters
    profitability, and the resulting switching raised observed 표준형 lapse, which was fed
    back into the 무해지 assumption — 「악순환」 [REG-R27].
    """
    v = model_point()["lapse_basis"]
    if v not in ("log_linear", "table"):
        raise ValueError("invalid lapse_basis")
    return v


def mort_be_factor():
    """The multiplier turning the shipped valuation mortality into the projection basis.

    1.00 on every model point but 9, so the base run is a **valuation-basis run and not a
    best estimate**: [S3]'s rates are 예정위험률 carrying a 안전할증 whose regulatory cap
    was 30% in the early 2000s, 50% from the 2015 로드맵 and removed from 2017, and no
    retrieved source sizes the margin against current Korean insured experience [R1].
    Claims move proportionately with it; the terminal rate is held at 1 whatever it is set
    to, because ``omega_age`` is the horizon of the table and a structural property of the
    projection rather than an experience assumption.
    """
    return float(model_point()["mort_adj"])


def ci_be_factor():
    """The same lever on the CI decrement; 1.00 on every model point but 9 **[std]**.

    Held apart from :func:`mort_be_factor` because the two margins are not the same size
    and there is no reason to move them together: the mortality basis is a life table and
    the CI basis is a morbidity table built on six disclosed numbers, and the second is by
    far the weaker of the two.  0.75 on model point 9, removing a third of the rate as a
    stated **[std]** unwinding of the 안전할증 [R1].
    """
    return float(model_point()["ci_adj"])


def mort_ci_factor():
    """The multiplier on mortality after a CI event **[std]**; 3.00 in the base run.

    **The CI and death decrements are not independent competing risks**, and the product
    is built on the fact that they are not.  There is no survival period anywhere in a
    Korean CI contract — the supervisor refused the overseas 30-day requirement on
    consumer-protection grounds, holding that requiring survival would create disputes
    where the insured died [R1] — so the CI rate already includes lives who die of the CI
    cause, and a fraction of what would be a death claim on an ordinary 종신보험 is a CI
    claim here followed shortly by a residual death claim.

    No Korean post-CI mortality is published.  3.00 is a standardization whose rationale
    is the registry's own survival data: five-year relative survival across all cancers
    excluding thyroid is 69.6% against a general population at 100% by construction
    [REG-R40], and the CI trigger set is deliberately the severe tail of each disease.
    It is a model point column so that the sensitivity can be read directly, and model
    point 9 runs it at 2.00.
    """
    return float(model_point()["mort_ci_factor"])


def waiver_rate(t):
    """The 납입면제 rate on the **장해 50%+** limb alone, in policy year t **[std]**.

    [S1] waives all future 기본보험료 on either a 장해지급률 of 50% or more from one
    accident or one non-accidental cause, **or** any CI/LTC 지급사유 [S1 별표1 주4].
    Because the second limb fires with essentially every CI claim, the waiver is **not an
    independent decrement on the CI limb** and is not modelled as one: it is implicit in
    the post-CI cohort, which pays no premium at all.  What is left is the first limb, a
    real if second-order decrement on the same 장해분류표 percentage scale the chassis uses
    [REG-R25].

    0.03% a year during the 납입기간 **[std]**; no Korean disability inception rate at the
    50% threshold is published.  A waived policy stays pre-CI, keeps its full death cover
    and — the chassis's **"waived premiums count as paid"** rule — continues to accrue
    surrender value on the full premium scale, so the waiver is the only route to the
    저해지 step without funding it.  Zero once no premium is due.
    """
    if t < 1 or t > prem_end():
        return 0.0
    return float(model_point()["waiver_rate"])


def pol_loan_util():
    """The fraction of the available 보험계약대출 drawn; 0 in the base run **[std]**.

    There is no public Korean take-up data of any kind, so the level is a model point
    input and the contractual limit in :func:`loan_avail_pp` binds it whatever it is set
    to.  Model point 7 draws half the available amount at duration 12, inside the
    납입기간, where the base is the **suppressed** value — which is the configuration in
    which the CI carve-out's doubling of the limit is visible.
    """
    return float(model_point()["pol_loan_util"])


def pol_loan_year():
    """The policy year in which the 보험계약대출 is drawn; 0 for no draw."""
    return int(model_point()["pol_loan_year"])


def omega_age():
    """omega: the terminal age of the mortality table, the first age at which q = 1.

    110 on the shipped construction, for both sexes **[std]**.  The 제10회 경험생명표's
    terminal age is not published — 보험개발원 releases only 평균수명 and 기대여명
    [REG-R33] [REG-R34] — so the horizon is a stated property of the constructed table and
    not a transcription.  It is a hard model parameter and not a rounding: projecting a
    whole-life contract to 100 truncates the liability and projecting to 120 invents one.
    """
    tbl = data.mort_table().loc[sex()]                               # noqa: F821
    return int(tbl.index[tbl["mort_rate"] >= 1.0][0])


def proj_len():
    """T = omega - x + 1: the projection length in policy years.

    There is no maturity date and no 만기보험금, so the horizon is the table's and not the
    contract's.  Every remaining life dies in year T and ``pols_if(T + 1)`` is zero; there
    are no tail states.  **CI cover ends earlier**, at the 100세 계약해당일 — see
    :func:`ci_cover_end` — so the projection carries a long stretch on which the death
    benefit is the only cover left.
    """
    return omega_age() - age_at_entry() + 1


def age(t):
    """x + t - 1: the attained 보험나이 at the start of policy year t."""
    return age_at_entry() + t - 1


def ci_cover_end():
    """n_CI: the last policy year in which the CI benefit is covered.

    The death benefit is 종신 but **CI/LTC cover ends at the 100세 계약해당일**, so the
    last covered year is the one opening at attained age 99 and ``n_CI = 100 - x``.  This
    is the post-2008 design and is the one a contract written today has: the 2002 product
    put the acceleration inside a 제1보험기간 running to the 80세 계약해당일 and paid 100%
    of the death benefit thereafter [S6] [R1], and that legacy split is named in
    ``product-spec.md`` and deliberately not modelled, because a second discontinuity at
    80 would collide with the 저해지 step in any model point trying to isolate either.
    """
    return max(0, ci_cover_end_age - age_at_entry())                 # noqa: F821


def mort_rate_at_age(y):
    """The shipped table's mortality rate at attained age y, before any adjustment.

    Read from ``mort_table.csv``, a **[std]** construction anchored on the 예정 경험
    사망률 one Korean CI 상품요약서 discloses at ages 20, 40 and 60 [S3]; see
    :mod:`~.CI_KR_A.Data`.  This is the rate the pricing recursions use unadjusted:
    ``mort_be_factor`` is a lever on the *decrement*, not a change to the 산출방법서 basis.
    """
    return float(data.mort_table().loc[(sex(), y), "mort_rate"])     # noqa: F821


def mort_rate_base(t):
    """The pricing-basis mortality rate in policy year t, at attained age ``age(t)``."""
    return mort_rate_at_age(age(t))


def mort_rate(t):
    """q(t): the death decrement applied to the **pre-CI** cohort in policy year t.

    The table rate times :func:`mort_be_factor`, capped at 1 and held at 1 at the table's
    terminal age whatever the factor is set to.
    """
    if age(t) >= omega_age():
        return 1.0
    return min(1.0, mort_rate_base(t) * mort_be_factor())


def mort_rate_ci_base(t):
    """The pricing-basis mortality of a **post-CI** life in policy year t.

    The table rate times :func:`mort_ci_factor`.  It is what :func:`epv_resid` values the
    residual on, so the reserve carries the same excess mortality the projection does; a
    pricing basis that valued the residual on ordinary mortality would hold too little
    against it.
    """
    if age(t) >= omega_age():
        return 1.0
    return min(1.0, mort_rate_base(t) * mort_ci_factor())


def mort_rate_ci(t):
    """q'(t): the death decrement applied to the **post-CI** cohort in policy year t.

    :func:`mort_rate` times :func:`mort_ci_factor`, capped at 1.  The post-CI cohort is
    the only place in this model where the correlation between the two decrements appears
    as a number, and it is the reason the residual death benefit is paid earlier than an
    ordinary 종신보험's would be.
    """
    if age(t) >= omega_age():
        return 1.0
    return min(1.0, mort_rate(t) * mort_ci_factor())


def ci_rate_at_age(y, cause):
    """The shipped incidence rate at attained age y for one of the five modelled causes.

    ``cancer``, ``ami`` and ``stroke`` are 중대한 암, 중대한 급성심근경색증 and 중대한
    뇌졸중, sourced at ages 20, 40 and 60 [S3] and constructed elsewhere; ``other`` covers
    the five remaining 중대한 질병, the four 중대한 수술 and 중대한 화상 및 부식; ``ltc``
    is 장기요양상태 on 노인장기요양 1·2등급.  See :mod:`~.CI_KR_A.Data` for what each rests
    on.  Zero above the last tabulated age.
    """
    if y > ci_cover_end_age:                                         # noqa: F821
        return 0.0
    return float(data.ci_incidence_table().loc[                      # noqa: F821
        (sex(), y, cause), "ci_rate"])


def ci_wait_factor():
    """The first-year proration for the 90-day 보장개시일 **[std]**.

    ``1 - 90/365 = 0.7534``.  The 중대한 암 보장개시일 is 「계약일(부활일)부터 그 날을
    포함하여 90일이 지난날의 다음날」 [S1 제7조] [S1 별표1 주1] and is **invariant across
    every document retrieved** [S1] [S2] [S3] [S4]; 장기요양상태 carries the same 90 days,
    waived where the state arises directly from a 재해 [S1 별표1 주2].  Everything else —
    the other seven 중대한 질병, the four 중대한 수술 and 중대한 화상 및 부식 — is covered
    **from the 계약일** with no waiting period at all [S1] [S2 별표1 주1].

    On an annual grid the wait is applied as a straight-line proration of the first year's
    exposure for the two causes that carry it, which is a standardization: it assumes
    incidence is uniform over the first policy year, and it does not model the two consumer
    protections that ride on the wait — the right to cancel and recover the premiums where
    중대한 암 is diagnosed before the 보장개시일, and the five-year revival of cover for a
    pre-inception cancer [S1 제7조⑤⑥].
    """
    return 1.0 - ci_wait_days / 365.0                                # noqa: F821


def ci_rate_base(t):
    """The pricing-basis CI decrement in policy year t: one **first-event** rate.

    The five causes summed, with the 90-day 보장개시일 proration applied in year 1 to the
    two that carry it, capped at 1, and **zero after** :func:`ci_cover_end`.  Summing is
    legitimate here only because the shipped rates are themselves first-event rates across
    the competing-risk set: the benefit is payable once only across every trigger
    [S1 별표1], and Korea's supervisor required the overlap between CI causes to be
    reflected in the filed rate rather than ignored for rate stability as overseas practice
    does — 「CI 질병들 간 중복해서 발생할 수 있는 확률을 최대한 반영한 최종 위험률로
    검증받고 사용하였다」 [R1].  A table built by adding published site-specific incidences
    would be wrong in exactly the direction the regulation addresses.
    """
    if t < 1 or t > ci_cover_end():
        return 0.0
    y = age(t)
    total = 0.0
    for cause in ("cancer", "ami", "stroke", "other", "ltc"):
        rate = ci_rate_at_age(y, cause)
        if t == 1 and cause in ("cancer", "ltc"):
            rate = rate * ci_wait_factor()
        total = total + rate
    return min(1.0, total)


def ci_rate(t):
    """q_ci(t): the CI decrement applied in policy year t.

    :func:`ci_rate_base` times :func:`ci_be_factor`, capped at 1.  **Morbidity dominates
    mortality on this chassis**: on [S3]'s own disclosure the three headline rates sum to
    3.70 times the death rate at male 40 and 6.70 times it at male 60, which is why a
    projection of this product is a morbidity projection with a mortality tail rather than
    the reverse, and why the CI benefit takes about half the risk premium at a 50%
    acceleration despite paying only half the sum assured [S3].
    """
    return min(1.0, ci_rate_base(t) * ci_be_factor())


def ci_reduced_share(t):
    """The share of policy year t's CI claims paid at the reduced first-year rate.

    Zero in every year but the first.  In year 1 it is 1 where ``first_year_scope`` is
    ``all``, and otherwise the breast-cancer share of that year's own CI decrement —
    :func:`breast_share` times the 중대한 암 component after the 90-day proration, over
    :func:`ci_rate_base`.  Splitting the decrement rather than averaging the benefit is
    what lets the two first-year cohorts carry different residuals, which they must:
    a reduced claim leaves ``(1 - a f) B(1)`` and a full one leaves ``r B(1)``.
    """
    if t != 1 or first_year_factor >= 1.0:                           # noqa: F821
        return 0.0
    if first_year_scope() == "all":
        return 1.0
    base = ci_rate_base(t)
    if base <= 0.0:
        return 0.0
    cancer = ci_rate_at_age(age(t), "cancer") * ci_wait_factor()
    return min(1.0, breast_share() * cancer / base)


def lapse_rate_base(t):
    """The 표준형 voluntary surrender rate in policy year t, from ``lapse_table.csv``.

    9% / 7% / 5.5% / 4.5% / 3.8% / 3.2% and a 2.8% tail, all **[std]**.  **No CI lapse
    experience of any kind was retrieved** — [R1] gives one cession ratio and no lapse data
    at all — so the curve is bounded rather than fitted: Korean 상품요약서 publish the
    적용해지율 used in pricing in envelope form, and one carrier's protection product
    discloses 0%-13.4% during the payment period against 1%-10% at another.  The tail sits
    far above the 0.8% post-완납 ultimate the supervisor's 원칙모형 sets, and that gap is
    the subject of [REG-R27].
    """
    tbl = data.lapse_table()                                         # noqa: F821
    return float(tbl.loc[min(max(t, 1), int(tbl.index.max())),
                         "lapse_rate"])


def lapse_rate_ult():
    """The post-납입완료 ultimate surrender rate of whichever basis is in force.

    0.8% on the 로그-선형 원칙모형, which the IFRS17 주요 계리가정 가이드라인 sets as the
    post-완납 rate for 무·저해지 business [REG-R27]; the table's own tail otherwise.
    """
    if lapse_basis() == "log_linear":
        return lapse_post_paidup                                     # noqa: F821
    return lapse_rate_base(prem_end() + 1)


def lapse_rate(t):
    """w(t): the annual voluntary surrender rate of the **pre-CI** cohort in year t.

    This is the **annual** rate; there is no monthly companion on an annual-grid model.
    On the ``log_linear`` basis it is the guideline's 원칙모형 — geometric decay from a
    first-year 10% **[std]** to the 0.1% the guideline sets at 납입완료, then the 0.8%
    post-완납 ultimate [REG-R27].  On the ``table`` basis it is
    :func:`lapse_rate_base` unchanged.

    **No separate 완납 surrender spike is imposed.**  The eightfold step from 0.1% to 0.8%
    at 납입완료 is produced by the guideline's own shape, and the contractual step in
    :func:`cv_pp` that provokes a real surge is a different object from the behavioural
    assumption about it; conflating the two is how a spike gets counted twice.

    A surrender is not a pure decrement here: it pays :func:`cv_pp` net of any loan, and
    that value is **suppressed** during the 납입기간, which is precisely why early
    surrender on this form is assumed low.
    """
    if lapse_basis() != "log_linear":
        return min(1.0, lapse_rate_base(t))
    m = prem_end()
    if t > m:
        return lapse_post_paidup                                     # noqa: F821
    if m <= 1:
        return lapse_ll_target                                       # noqa: F821
    lam = math.log(lapse_ll_first / lapse_ll_target) / (m - 1)       # noqa: F821
    return min(1.0, lapse_ll_first * math.exp(-lam * (t - 1)))       # noqa: F821


def lapse_rate_ci(t):
    """w'(t): the annual voluntary surrender rate of the **post-CI** cohort.

    The ultimate rate of the basis in force times ``lapse_ci_factor`` **[std]**, level in
    t.  A post-CI policy is premium-waived, so it is in the paid-up state by construction
    and the paying-period curve does not describe it whichever basis is chosen.

    The factor is 0.50 and its **direction is genuinely ambiguous**, which is why it is a
    lever rather than a finding.  A CI claimant has no premium to fund and may value the
    residual cover highly, which argues for less surrender; but the carve-out has just
    doubled the cash available, which argues for more.  Nothing in any retrieved document
    bears on it.
    """
    return min(1.0, lapse_ci_factor * lapse_rate_ult())              # noqa: F821


def disc_factor():
    """v = 1 / (1 + i): the discount factor of the 예정이율.

    2.50% flat, inherited unchanged from the whole life chassis and **[std]**.  No
    CI-specific pricing rate later than 2011 was retrieved and the two that exist bracket
    it from too far away to be useful — 연복리 4.0% on a January 2011 CI product [S3] and
    about 2.75% on a 2019 종신 illustration basis [S4] — while the chassis reads six values
    off 2021-2025 carrier documents spanning 2.25%-2.75% and takes the mid-point, which is
    also the 2026 평균공시이율 [REG-R48].  A library whose CI product and whose whole-life
    product discounted on different rates would make the cost of the acceleration
    impossible to read off the difference between them.

    Note that **예정이율 is not a regulatory term in Korea**: a full-text search of the
    감독규정 returns no occurrence, and the regulation speaks only of the 계약자적립액
    적용이율 and of the 금리연동형 / 금리확정형 distinction [REG-R9] [REG-R48].  Interest
    matters less here than on the chassis, because a CI benefit is paid a decade or more
    before the death benefit it accelerates and the liability is correspondingly shorter.
    """
    return 1.0 / (1.0 + prem_int_rate)                               # noqa: F821


def epv_resid(t):
    """A1(t): the EPV at the start of policy year t of the residual, for a post-CI life.

    ``v [q' r SA + (1 - q') A1(t + 1)]`` on the pricing basis, with ``A1(T + 1) = 0``.
    It values the residual at its **nominal** ``r SA`` and ignores the 105% account floor
    **[std]**: the floor is a multiple of ``V`` and ``V`` is built out of this quantity, so
    pricing it in would make the reserve self-referential.  The projection applies the
    floor in full, and :func:`check_resid_floor` asserts it there.
    """
    if t < 1 or t > proj_len():
        return 0.0
    q = mort_rate_ci_base(t)
    return disc_factor() * (q * resid_rate() * sum_assured()
                            + (1.0 - q) * epv_resid(t + 1))


def epv_ben(t):
    """A0(t): the EPV at the start of policy year t of every future benefit, pre-CI.

    The two-state recursion this whole product reduces to::

        A0(t) = v [ q_ci a SA + (1 - q_ci) q SA
                    + q_ci A1(t + 1) + (1 - q_ci)(1 - q) A0(t + 1) ]

    **The acceleration is a timing effect and nothing else.**  Because ``a + r = 1``
    exactly, a life that accelerates and then dies pays the same total as a life that
    simply dies; the CI event moves ``a SA`` of it forward by the years between the two
    events.  At the anchor cell that is worth 24.4% of the net premium against the same
    contract with no acceleration, and it is the whole actuarial content of the product.
    """
    if t < 1 or t > proj_len():
        return 0.0
    qc = ci_rate_base(t)
    qd = mort_rate_base(t)
    return disc_factor() * (
        qc * accel_rate() * sum_assured()
        + (1.0 - qc) * qd * sum_assured()
        + qc * epv_resid(t + 1)
        + (1.0 - qc) * (1.0 - qd) * epv_ben(t + 1))


def annuity_due(t):
    """The EPV at the start of policy year t of 1 a year while pre-CI and premium due.

    ``1 + v (1 - q_ci)(1 - q) a(t + 1)`` for ``t <= m``, zero after.  **The CI decrement
    is in the annuity as well as in the benefit**, because any CI/LTC 지급사유 waives all
    future 기본보험료 [S1 별표1 주4]: a premium stream that ran on through the post-CI
    state would over-fund the contract by the whole of the waiver.
    """
    if t < 1 or t > prem_period():
        return 0.0
    return 1.0 + disc_factor() * (1.0 - ci_rate_base(t)) * (
        1.0 - mort_rate_base(t)) * annuity_due(t + 1)


def prem_net_level_pp():
    """P: the annual net level premium on the pricing basis, ``A0(1) / a(1)``.

    A **pricing** quantity that never becomes a cash flow: what is collected is
    :func:`premium_pp`.  On the anchor cell it is ₩2,968,514 against a gross of
    ₩3,680,880, a loading of 24.0% — which sits close to, and is a different quantity
    from, the 보험료지수 of 130.1% [S3] publishes for the same form, that ratio being
    against the 표준순보험료 computed on the supervisor's prescribed rates rather than on
    this model's.

    It is **not** the 연납순보험료 that enters the 표준해약공제액; that is
    :func:`surr_chg_cap_pp`, which follows the chassis in taking 80% of the gross premium
    **[std]** so that the statutory cap can be reproduced from published quantities alone.
    """
    return epv_ben(1) / annuity_due(1)


def pol_val_pp(t):
    """V(t): the 계약자적립액 at anniversary t, prospective and net level premium.

    ``A0(t + 1) - P a(t + 1)``, zero at ``t = 0`` and at ``t = T``.  It is the account of
    the **표준형 twin** — the non-marketed comparison contract priced with the lapse
    assumption switched off — and there is exactly one of it in this model: the suppression
    is a haircut on this value, the post-CI carve-out lifts the haircut off this value, and
    the 기본보험금 and residual floors read off this value.  **CV(t) is therefore
    independent of the sold form's own premium**, which is the whole of the 환급률
    arithmetic that sells the 저해지 form.

    The recursion it satisfies is asserted by :func:`check_pol_val_roll_fwd`.  [S3] words
    the same identity in a CI product's own terms — 「보험료 계산시 적용한 위험률로 산출한
    순보험료식 책임준비금에서 미상각신계약비(해지공제액)를 공제한 금액을 해지환급금으로
    지급합니다」 — and [S1]'s 약관 sends the calculation to the 산출방법서, which is filed
    and unpublished [REG-R2].
    """
    if t <= 0:
        return 0.0
    return epv_ben(t + 1) - prem_net_level_pp() * annuity_due(t + 1)


def cum_prem_pp(t):
    """cumprem(t): gross premiums paid per policy by the end of policy year t.

    ``G min(t, m)``.  **Waived premiums count as paid** — the chassis's rule, carried over
    — so a policy on the 장해 50%+ waiver reaches the same cumulative figure without
    funding it.  This is one of the three limbs of the 기본보험금.
    """
    return premium_pp() * min(t, prem_end())


def base_benefit_pp(t):
    """B(t): the 기본보험금, the floored base every percentage in this contract applies to.

    ``max(기본사망보험금, 이미 납입한 보험료, c V(t))`` with 기본사망보험금 =
    보험가입금액 - 중도인출금액 + 추가납입보험료 [S1 별표1 주7], the last two held at zero
    **[std]** — named rather than dropped, because a model that ignores them must say it
    holds them at zero rather than silently leaving them out of the definition.

    **At the anchor cell neither floor binds within the 납입기간**, and it is worth saying
    so plainly so that the model is not read as being built around a clause that never
    fires: cumulative premiums at 납입완료 are ₩73,617,600 against a face of
    ₩100,000,000, and ``c V(t)`` reaches the face only when ``V`` passes ₩95,238,095.  The
    floors bind where a Korean designer would want them to — a short-pay or high-premium
    cell, and a very old attained age.  The floor on the **residual** is a different matter
    and binds early: see :func:`resid_db_pp`.

    The premiums-paid limb is the contractual form of a supervisory design rule, 감독규정
    제7-60조제9호, which requires the death benefit to be at least cumulative premiums paid
    except where the payment period ends at age 80 or below [REG-R16] — and on the anchor
    cell 납입완료 falls at attained age 60, so the exception applies and the rule does not
    strictly bite.
    """
    return max(sum_assured(), cum_prem_pp(t),
               resid_floor_mult() * pol_val_pp(t))


def surr_chg_cap_pp():
    """SC_max: the statutory 표준해약공제액, the cap on the surrender charge.

    ``연납순보험료 x 5% x 해약공제계수 + 보험가입금액 x 10/1000`` [REG-R20], the
    해약공제계수 being the 보험기간 capped at 20 years for a 보장성보험 — so on a 종신
    contract it is **one year's net premium plus 1% of the sum assured**.  The
    연납순보험료 is taken as 80% of the gross **[std]**, the chassis's ratio, so that the
    cap can be reproduced from published quantities rather than from this model's own
    pricing basis.

    At the anchor that is ₩2,944,704 + ₩1,000,000 = **₩3,944,704**.  Cross-check: the
    FSC's 보장성보험 rule of thumb of 13 times the monthly premium gives ₩3,987,620, which
    agrees within 1.1% [REG-R29].  The 보험가입금액 that enters the formula is the
    **pre-acceleration** death benefit, by 감독규정 [별표 15] 제3호 read with 제8호
    [REG-R21]: a CI contract covers death from any cause, so 일반사망 applies directly and
    the figure is ₩100,000,000 and not the ₩20,000,000 residual — a clean instance of the
    acceleration form buying this product a simpler regulatory position than a standalone
    진단비 product, which must build a notional 보험가입금액 instead.
    """
    return (net_prem_ratio * premium_pp() * surr_chg_rate            # noqa: F821
            * surr_chg_coef_cap                                      # noqa: F821
            + surr_chg_sa_rate * sum_assured())                      # noqa: F821


def surr_chg_pp(t):
    """SC(t): the 해약공제액 (미상각신계약비) outstanding at anniversary t.

    The cap running off in a straight line over the 해약공제기간, which is the 납입기간 or
    the 신계약비 부가기간 **capped at 7 years** [REG-R19 제7-66조제1항제2호].  On the
    anchor's 20년납 contract the charge is therefore gone by duration 7, **thirteen years
    before 납입완료** and, on most lives, before any CI event — which is why the step in
    :func:`cv_pp` at 납입완료 is not a surrender-charge effect and cannot be explained as
    one.  The straight-line run-off is **[std]**: the amortisation schedule lives in the
    unpublished 산출방법서.
    """
    n = min(prem_period(), surr_chg_years_cap)                       # noqa: F821
    if n <= 0 or t >= n:
        return 0.0
    return surr_chg_cap_pp() * (n - t) / n


def cv_std_pp(t):
    """W(t): the 표준형 twin's 해약환급금 at anniversary t, floored at zero.

    ``max(0, V(t) - SC(t))``.  The 미경과보험료 that 감독규정 제7-66조제5항 adds on
    termination is not modelled **[std]**: on an annual grid with premiums paid in advance
    on the anniversary there is none to add.
    """
    return max(0.0, pol_val_pp(t) - surr_chg_pp(t))


def cv_mult(t):
    """The multiplier on W(t) for a **pre-CI** policy: k inside the 납입기간, 1 after it.

    A **step, not a ramp**.  A surrender occurring in policy year m is paid at the end of
    that year on the full value **[std ordering]**; the suppressed value applies to years
    1 to m - 1.  Both quantities exist at every duration and the model publishes both,
    :func:`cv_pp` and :func:`cv_pp_ci`.
    """
    return 1.0 if t >= prem_period() else cv_floor_ratio()


def cv_pp(t):
    """CV(t): the 해약환급금 actually payable on a **pre-CI** surrender at anniversary t.

    ``cv_mult(t) W(t)``.  On the 무해지 form (``k = 0``) this is nil throughout the
    납입기간, and the FSS's finding that such a contract cannot support a policy loan at
    all during the payment period [REG-R28] [REG-R25 제33조] follows arithmetically —
    which is one reason the composite's representative form is 저해지 rather than 무해지.
    """
    return cv_mult(t) * cv_std_pp(t)


def cv_pp_ci(t):
    """CV'(t): the 해약환급금 payable on a **post-CI** surrender — the carve-out.

    ``W(t)``, the full 표준형 value, at **every** duration, before and after 납입완료
    [S2] [S4].  This is the CI-specific delta on the chassis and it is contractual: [S2]
    conditions the suppression on 「제7조 … 제2호의 CI/LTC보험금 지급사유가 발생하지 않은
    경우」 and [S4] on 「「선지급 진단보험금」 지급사유 발생 전 납입기간 동안」.

    Three consequences follow and each is a modelling requirement.  The surrender strain
    on the post-CI cohort is materially larger than on the pre-CI cohort at the same
    duration, so a projection running one surrender-value scale over one aggregate policy
    count understates outgo.  The policy loan available jumps at the same date.  And the
    premium stops at the same date, so from ``t_CI`` the contract pays nothing, holds a
    full-value surrender right and owes only the residual — which is what makes the post-CI
    state a genuinely different liability rather than a scaled-down version of the pre-CI
    one.

    There is an accounting asymmetry worth naming: the 해약환급금준비금 appropriation test
    measures the IFRS 17 잔여보장요소 against the surrender value computed under 제7-66조
    제1항, on the unsuppressed basis, **even for the 제4항 products that may contractually
    pay less** [REG-R11].  So this carve-out doubles the contractual value from one day to
    the next and changes the reserve it is measured against not at all.
    """
    return cv_std_pp(t)


def ci_cohort_ids(t):
    """The post-CI cohort labels that can carry policies at the start of policy year t.

    ``[0] + [1 .. t - 1]``.  A cohort is labelled by the policy year it accelerated in;
    label **0** is the first-year 감액 cohort, whose residual differs from cohort 1's
    because its acceleration was halved.  Entrants join at the start of the year after
    they accelerate, so no label ``>= t`` can be populated at t.
    """
    return [0] + list(range(1, max(t, 1)))


def accel_benefit_pp(s):
    """a B(s): the 선지급 CI/LTC보험금 paid to cohort s, per policy.

    ``a B(s)`` for a full claim in policy year s, and ``a f B(1)`` for cohort 0, the
    first-year reduced claim, with ``f = 0.5`` — 40% of the 기본보험금 instead of 80% on
    the composite, 25% instead of 50% on the 50% form [S1 별표1] [S2 별표1].  Paid at the
    end of the year of the event, **once only** across the whole trigger set, and **not**
    netted against any policy loan: the contract continues and the loan stays outstanding
    against the residual.
    """
    if s <= 0:
        return accel_rate() * first_year_factor * base_benefit_pp(1)  # noqa: F821
    return accel_rate() * base_benefit_pp(s)


def resid_nominal_pp(s):
    """r B(s): the nominal residual death benefit cohort s carries, per policy.

    The exact complement of what was paid — ``(1 - a) B(s)``, and ``(1 - a f) B(1)`` for
    the first-year reduced cohort 0, so 60% where 40% was accelerated [S1] [S2].  It is
    fixed at the acceleration date and does not move afterwards; what moves is the floor
    beneath it, :func:`resid_db_pp`.
    """
    if s <= 0:
        return (1.0 - accel_rate() * first_year_factor) * base_benefit_pp(1)  # noqa: F821
    return resid_rate() * base_benefit_pp(s)


def resid_db_pp(t, s):
    """The death benefit payable in policy year t to a policy that accelerated in year s.

    ``max(r B(s), c V(t))`` — 「CI/LTC보험금 지급사유 발생당시의 기본보험금의 20%와
    CI/LTC보험금 지급사유 발생 후 계약자적립금의 105% 중 큰 금액」 [S1 별표1 주8].  **The
    residual is not a constant**, and on the 80% form the floor binds early and stays
    bound: at the anchor cell ``r B`` is ₩20,000,000 and the account passes ₩19,050,000
    well inside the 납입기간, so for most of the contract's life the residual death benefit
    **is the account value and not the stated complement**.  A model that hard-codes 20% of
    the sum assured understates the post-CI liability by a growing margin, and that
    asymmetry is one of the three reasons the composite takes the 80% fraction.
    """
    return max(resid_nominal_pp(s), resid_floor_mult() * pol_val_pp(t))


def resid_db_avg_pp(t):
    """The in-force-weighted mean residual death benefit across the post-CI cohorts at t.

    A reporting quantity only; no cash flow uses it.  It is published because the spread
    between it and ``r SA`` is the clearest single reading of how far the 105% floor has
    taken over the residual.
    """
    n = pols_if_ci(t)
    if n <= 0.0:
        return 0.0
    return sum(pols_if_ci_at(t, s) * resid_db_pp(t, s)
               for s in ci_cohort_ids(t)) / n


def loan_avail_pp(t):
    """The 보험계약대출 available at anniversary t to a **pre-CI** policy.

    80% of the *payable* 해약환급금 [REG-R25 제33조], which during the 납입기간 is the
    **suppressed** value.  The chassis argues the 80% limit against published Korean ranges
    of 「해약환급금의 50% ~ 85%」 and 「50 ~ 80%이내」 and this product inherits it.
    """
    return loan_cap_rate * cv_pp(t)                                  # noqa: F821


def loan_avail_ci_pp(t):
    """The 보험계약대출 available at anniversary t to a **post-CI** policy.

    The same 80% of the payable value, which after a CI event is the **full** 표준형 value
    — so on the composite's ``k = 0.50`` form **the available loan doubles the moment a
    CI/LTC 지급사유 arises**, at the same duration and with no other change to the
    contract.  Nothing in the retrieved documents restricts the loan after a CI payment, so
    the post-acceleration contract carries a full-value loan facility against a sum assured
    that is now a fifth of its original size; whether any carrier restricts it further is
    **[unverified]**.  Published as its own cells so that the doubling can be read directly
    rather than inferred.
    """
    return loan_cap_rate * cv_pp_ci(t)                               # noqa: F821


def pol_loan_draw(t):
    """The 보험계약대출 drawn at anniversary t, per policy; zero in the base run."""
    if pol_loan_year() <= 0 or t != pol_loan_year():
        return 0.0
    return pol_loan_util() * loan_avail_pp(t)


def loan_pp(t):
    """L(t): the 보험계약대출 balance carried into policy year t, per policy.

    ``L(t + 1) = (L(t) + draw(t))(1 + i_L)`` at ``i_L = 예정이율 + 1.5% = 4.00%``
    compound, the chassis's rate.  One balance per policy, carried unchanged across the CI
    transition — a policy that borrowed before accelerating still owes it afterwards — and
    deducted from every terminal payment, floored at zero.  The 보험계약대출 is a modelled
    state and not a decrement: no policy leaves because of it here, and a loan that
    outgrows the benefit simply reduces the payment to nil.
    """
    if t <= 1:
        return 0.0
    return (loan_pp(t - 1) + pol_loan_draw(t - 1)) * (1.0 + i_loan)  # noqa: F821


def pols_if_pre(t):
    """l0(t): policies in force and **pre-CI** at the start of policy year t.

    Decremented in the year by the CI transition first, then death among those who did not
    accelerate, then surrender among those who neither accelerated nor died, so
    ``l0(t + 1) = l0(t)(1 - q_ci)(1 - q)(1 - w)``.
    """
    if t < 1 or t > proj_len():
        return 0.0
    if t == 1:
        return pols_if_init()
    return (pols_if_pre(t - 1) - pols_ci(t - 1) - pols_death(t - 1)
            - pols_lapse(t - 1))


def pols_waived(t):
    """Policies in force, pre-CI and on the **장해 50%+** premium waiver at the start of t.

    A subset of :func:`pols_if_pre`, not a separate state: a waived policy keeps its full
    death cover, stays exposed to the CI decrement and continues to accrue surrender value
    on the full premium scale.  What it stops doing is paying, so it is subtracted from
    :func:`pols_if_pay` and from the renewal commission that follows the cash.  The waiver
    on the CI limb is not counted here — it is implicit in the post-CI cohort, which pays
    nothing at all.
    """
    if t < 1 or t > proj_len():
        return 0.0
    if t == 1:
        return 0.0
    u = t - 1
    entered = (pols_waived(u)
               + (pols_if_pre(u) - pols_waived(u)) * waiver_rate(u))
    return entered * (1.0 - ci_rate(u)) * (1.0 - mort_rate(u)) * (
        1.0 - lapse_rate(u))


def pols_if_pay(t):
    """lp(t): policies in force, pre-CI and actually paying a premium in policy year t.

    ``l0(t)`` less the waived subset, and nil once no premium is due.  **The post-CI cohort
    never appears here**: any CI/LTC 지급사유 waives all future 기본보험료 [S1 별표1 주4],
    so the residual death benefit is funded entirely out of the reserve standing at the
    acceleration date — which [S4] states in terms, computing the post-waiver reserve on
    the post-acceleration basis 「「선지급 진단보험금」 발생 이후 기준의 책임준비금을 계산」.
    """
    if t < 1 or t > prem_end():
        return 0.0
    return pols_if_pre(t) - pols_waived(t)


def pols_ci(t):
    """C(t): CI/LTC accelerations in policy year t, taken from the pre-CI cohort.

    ``l0(t) q_ci(t)``.  This is a **state transition and not an exit**: the contract
    continues, which 감독규정 제7-60조제8호 requires — a contract must not be extinguished
    while the risk it covers remains effective [REG-R16] — so these policies reappear in
    :func:`pols_if_ci` at the start of the next year and stay in :func:`pols_if`
    throughout.
    """
    return pols_if_pre(t) * ci_rate(t)


def pols_ci_in(t, s):
    """C(t, s): accelerations in policy year t entering post-CI cohort s.

    Cohort ``t`` takes the full-benefit claims of year ``t``; cohort ``0`` takes the
    first-year reduced ones, and is empty in every year but the first.
    """
    if t < 1 or t > proj_len():
        return 0.0
    if s <= 0:
        return pols_ci(1) * ci_reduced_share(1) if t == 1 else 0.0
    return pols_ci(t) * (1.0 - ci_reduced_share(t)) if t == s else 0.0


def pols_if_ci_at(t, s):
    """l1(t, s): policies in force and post-CI at the start of year t, from cohort s.

    Entrants join at the start of the year **after** they accelerate, and are then
    decremented by post-CI mortality and post-CI surrender.  Kept by cohort because the
    residual is a cohort property: see :func:`resid_nominal_pp`.
    """
    if t <= 1 or t > proj_len() + 1:
        return 0.0
    u = t - 1
    return (pols_ci_in(u, s)
            + pols_if_ci_at(u, s) * (1.0 - mort_rate_ci(u))
            * (1.0 - lapse_rate_ci(u)))


def pols_if_ci(t):
    """l1(t): policies in force and post-CI at the start of policy year t, all cohorts."""
    return sum(pols_if_ci_at(t, s) for s in ci_cohort_ids(t))


def pols_if(t):
    """l(t): the total number of policies in force at the **start** of policy year t.

    Pre-CI plus post-CI.  A CI claimant's contract is still in force — that is the whole
    point of an acceleration — so both states are counted here, and this is the weight on
    every maintenance-expense figure of the same ``result_cf()`` row.  It is
    :func:`pols_if_init` in the first policy year and 0 at ``proj_len() + 1``, because the
    table terminates and every remaining life dies in the final year.
    """
    if t < 1 or t > proj_len():
        return 0.0
    return pols_if_pre(t) + pols_if_ci(t)


def pols_if_at(t, timing):
    """The number of policies in force at a point inside policy year t.

    ``"BEF_DECR"``
        l(t), the start of the year, before anything happens; the same number
        as :func:`pols_if`.

    ``"BEF_LAPSE"``
        after the CI transition and after deaths, before surrenders — the
        processing order is **CI, then death, then lapse** **[std order]**, so
        this is the population surrenders are taken from.

    ``"AFT_DECR"``
        l(t + 1), the end-of-year state, and zero at ``proj_len()`` because the
        table's terminal rate is 1 and nobody survives the final year.
    """
    if timing == "BEF_DECR":
        return pols_if(t)
    if timing == "BEF_LAPSE":
        return (pols_if_pre(t) * (1.0 - ci_rate(t)) * (1.0 - mort_rate(t))
                + pols_ci(t)
                + pols_if_ci(t) * (1.0 - mort_rate_ci(t)))
    if timing == "AFT_DECR":
        return pols_if(t + 1)
    raise ValueError("invalid timing")


def pols_death(t):
    """D(t): expected deaths of **pre-CI** policies in policy year t, at the end of it.

    Taken from the survivors of the CI transition.  These policies never received an
    acceleration, so they are paid the whole 기본보험금 [S1].
    """
    return pols_if_pre(t) * (1.0 - ci_rate(t)) * mort_rate(t)


def pols_death_ci(t):
    """D'(t): expected deaths of **post-CI** policies in policy year t, at the end of it.

    On :func:`mort_rate_ci`, which carries the excess mortality a 중대한 질병 event
    implies.  Each cohort is paid its own residual, so the aggregate count here is a
    reporting figure and the benefit is computed cohort by cohort in :func:`claims`.
    """
    return pols_if_ci(t) * mort_rate_ci(t)


def pols_lapse(t):
    """S(t): expected surrenders of **pre-CI** policies at the end of policy year t.

    Taken from the survivors of the CI transition and of mortality — **CI, then death,
    then lapse** **[std order]** — and paid :func:`cv_pp` net of any loan, which inside
    the 납입기간 is the *suppressed* value.
    """
    return (pols_if_pre(t) * (1.0 - ci_rate(t)) * (1.0 - mort_rate(t))
            * lapse_rate(t))


def pols_lapse_ci(t):
    """S'(t): expected surrenders of **post-CI** policies at the end of policy year t.

    Paid :func:`cv_pp_ci`, the **full** 표준형 value, at every duration.  The surrender
    strain on this cohort is therefore materially larger than on the pre-CI cohort at the
    same duration, which is the modelling consequence of the carve-out.
    """
    return pols_if_ci(t) * (1.0 - mort_rate_ci(t)) * lapse_rate_ci(t)


def premiums(t):
    """Premium income at the start of policy year t, an inflow.

    ``G lp(t)``, carried on the paying cohort alone: the post-CI cohort pays nothing
    because any CI/LTC 지급사유 waives the premium, and the 장해 50%+ waived subset pays
    nothing either.  Zero from ``prem_end() + 1``; **nothing else about the contract stops
    there.**

    There is no 자동대출납입 behind the 납입최고 in any retrieved Korean 약관 — a
    conventional Korean contract is 해지 the day after a 14-day demand period ends
    [REG-R25 제26조] — so Korean lapse is behavioural rather than funded, and a model that
    imported the Japanese automatic-premium-loan machinery onto this chassis would remove a
    decrement the contract has.
    """
    return premium_pp() * pols_if_pay(t)


def claims(t, kind=None):
    """Benefit outgo in policy year t, by kind; the total when kind is omitted.

    ``"CI"``
        the 선지급 CI/LTC보험금, ``a B(t)`` on the full-benefit claims and
        ``a f B(1)`` on the first-year reduced ones, paid at the end of the
        year of the event and **not** netted against any policy loan, because
        the contract continues and the loan does with it.

    ``"DEATH"``
        the 사망보험금 of a policy with no prior CI payment, ``B(t)`` net of
        any loan, floored at zero.

    ``"DEATH_CI"``
        the residual death benefit, ``max(r B(s), c V(t))`` net of any loan,
        summed cohort by cohort because each carries its own nominal.

    ``"LAPSE"``
        the 해약환급금 on a pre-CI surrender, ``CV(t)`` net of any loan.

    ``"LAPSE_CI"``
        the 해약환급금 on a post-CI surrender, the **full** ``W(t)`` net of
        any loan — the carve-out, at every duration.

    Every one of these is floored at zero: a loan can outgrow the surrender value and,
    given long enough, the residual, and none of them may produce a negative payment.
    """
    if kind is None:
        return (claims(t, "CI") + claims(t, "DEATH") + claims(t, "DEATH_CI")
                + claims(t, "LAPSE") + claims(t, "LAPSE_CI"))
    if kind == "CI":
        return sum(pols_ci_in(t, s) * accel_benefit_pp(s)
                   for s in ci_cohort_ids(t + 1))
    if kind == "DEATH":
        return max(0.0, base_benefit_pp(t) - loan_pp(t)) * pols_death(t)
    if kind == "DEATH_CI":
        return sum(pols_if_ci_at(t, s) * mort_rate_ci(t)
                   * max(0.0, resid_db_pp(t, s) - loan_pp(t))
                   for s in ci_cohort_ids(t))
    if kind == "LAPSE":
        return max(0.0, cv_pp(t) - loan_pp(t)) * pols_lapse(t)
    if kind == "LAPSE_CI":
        return max(0.0, cv_pp_ci(t) - loan_pp(t)) * pols_lapse_ci(t)
    raise ValueError("invalid kind")


def claim_expenses(t):
    """The claim handling expense on the year's claim events **[std]**.

    ₩300,000 per event, uninflated, on CI accelerations and on both kinds of death.  **A
    CI claim is charged the same as a death claim**, which is a standardization and
    probably a generous one: the whole dispute record of this product is about
    adjudicating the 중대한 definitions, and an accelerated claim on a 중대한 뇌졸중
    requires a 장해 assessment deferred twelve months after onset [S1 별표3].  No Korean
    carrier publishes an expense basis of any kind — [S1] names the components as
    계약체결비용 and 계약관리비용 and never quantifies them — so every expense level here is
    a standardization, bounded above by the 표준해약공제액 [REG-R20] and by the 보험료지수
    of 130.1% [S3].  Published as its own ``claim_expenses`` column and deducted explicitly
    in :func:`net_cf`; it is **not** inside :func:`expenses`.
    """
    return expense_claim * (pols_ci(t) + pols_death(t)               # noqa: F821
                            + pols_death_ci(t))


def inflation_factor(t):
    """The expense inflation factor in policy year t: ``(1 + pi)^(t-1)`` **[std]**.

    1.0% a year.  Over a seventy-year whole-life horizon 1% compounds to 2.0 and 3% to
    7.9, so importing a Western inflation assumption here produces a different product
    rather than a stressed one.  There is no published Korean expense basis to anchor
    either figure.
    """
    return (1.0 + inflation_rate) ** (t - 1)                         # noqa: F821


def expenses(t):
    """E0 and e(t) in policy year t: **acquisition and maintenance only** **[std]**.

    ₩500,000 per policy at issue, then ₩60,000 per policy per year inflating at 1%, both
    at the start of the year.  Maintenance is carried on :func:`pols_if`, the **total**
    in force, so a post-CI policy costs the same to administer as a pre-CI one; it
    continues **for life** and not to 납입완료, which is the structural point of this
    chassis.  There is no separate surrender expense; it is folded into maintenance
    **[std]**.  The claim handling expense is not here: it is :func:`claim_expenses`,
    deducted separately and published in its own column.
    """
    acq = expense_acq * pols_if(1) if t == 1 else 0.0                # noqa: F821
    maint = expense_maint * inflation_factor(t) * pols_if(t)         # noqa: F821
    return acq + maint


def commissions(t):
    """Commission outgo in policy year t **[std]**.

    80% of the annual premium at issue, then 3% of premium income in years 2 to
    ``prem_end()``.  The initial rate is set below the **1,200% rule** — the 2019 사업비
    reform caps first-year 모집수수료 at twelve times the monthly premium, so at one annual
    premium [REG-R29] — and it sits just under the 표준해약공제액 of ₩3,944,704, which is
    the statutory bound on what a surrender may be made to repay.  Renewal commission
    follows the premium **actually collected in cash**, so neither the waived subset nor
    the post-CI cohort produces any, and none is paid after 납입완료.
    """
    init = (comm_init_rate * premium_pp() * pols_if(1)               # noqa: F821
            if t == 1 else 0.0)
    renew = (comm_renewal_rate * premiums(t)                         # noqa: F821
             if 2 <= t <= prem_end() else 0.0)
    return init + renew


def net_cf(t):
    """CF(t): the net cash flow of policy year t, **income positive**.

    Premiums less the five kinds of benefit, claim expense, acquisition and maintenance
    expense and commission.  The notes' own sign, which is also the library-wide
    convention, so there is no outgo-positive ``liability_cf`` companion to publish.

    The shape to expect is a deep new business strain in year 1, a long positive stretch
    while the premium runs against a CI decrement that is still small, a steepening drain
    as the incidence curve turns over from the fifties, a negative step at 납입완료 where
    the premium stops and the suppression lifts, and then a run-off in which the whole of
    the outgo is claims and maintenance against no income at all.  **The acceleration
    front-loads that outgo**: on the anchor cell the CI benefit is paid a decade or more
    before the death benefit it accelerates.
    """
    return (premiums(t) - claims(t) - claim_expenses(t) - expenses(t)
            - commissions(t))


def check_pols_roll_fwd_resid(t):
    """The total in-force roll-forward residual in policy year t; zero everywhere.

    ``l(t) - l(t + 1)`` less deaths and surrenders in **both** states.  The CI
    acceleration is deliberately absent from this identity: it is a transition and not an
    exit, and a model in which it reduced the in-force count would be modelling a
    standalone 진단비 benefit rather than an acceleration.
    """
    return (pols_if(t) - pols_if(t + 1) - pols_death(t) - pols_death_ci(t)
            - pols_lapse(t) - pols_lapse_ci(t))


def check_pols_roll_fwd():
    """True when the total in-force roll-forward closes in every projected policy year."""
    return all(abs(check_pols_roll_fwd_resid(t)) <= roll_fwd_tol     # noqa: F821
               for t in range(1, proj_len() + 1))


def check_ci_state_roll_fwd_resid(t):
    """The two-state transition residual in policy year t; zero everywhere.

    Two identities added: the pre-CI cohort loses exactly its accelerations, deaths and
    surrenders, and the post-CI cohort gains exactly the accelerations and loses exactly
    its own deaths and surrenders.  This is the check that catches a policy accelerating
    out of one state and not arriving in the other, which the total roll-forward above
    cannot see.
    """
    pre = (pols_if_pre(t) - pols_if_pre(t + 1) - pols_ci(t)
           - pols_death(t) - pols_lapse(t))
    post = (pols_if_ci(t + 1) - pols_if_ci(t) - pols_ci(t)
            + pols_death_ci(t) + pols_lapse_ci(t))
    return pre + post


def check_ci_state_roll_fwd():
    """True when both cohorts roll forward and the transition between them balances."""
    return all(abs(check_ci_state_roll_fwd_resid(t)) <= roll_fwd_tol  # noqa: F821
               for t in range(1, proj_len() + 1))


def check_decrement_sum_resid(t):
    """The cumulative-decrement residual at policy year t; zero everywhere.

    ``l(1)`` less every exit up to and including year t less ``l(t + 1)``.  At ``t = T``
    it is the statement that the decrements sum to 1: because the table terminates, every
    policy leaves by a death or a surrender in one of the two states and there is no
    residual population and no tail state anywhere in this model.
    """
    exits = sum(pols_death(u) + pols_death_ci(u) + pols_lapse(u)
                + pols_lapse_ci(u) for u in range(1, t + 1))
    return pols_if(1) - exits - pols_if(t + 1)


def check_decrement_sum():
    """True when every policy issued leaves by a modelled decrement, in every year."""
    return all(abs(check_decrement_sum_resid(t)) <= roll_fwd_tol     # noqa: F821
               for t in range(1, proj_len() + 1))


def check_pol_val_roll_fwd_resid(t):
    """The 계약자적립액 recursion residual at anniversary t; zero everywhere.

    ``(V(t-1) + P 1{t <= m})(1 + i)`` less ``q_ci [a SA + A1(t+1)] + (1 - q_ci) q SA +
    (1 - q_ci)(1 - q) V(t)`` on the pricing decrements — the retrospective form of the
    same prospective value.  It is what catches a mis-set 납입기간, a discount factor
    applied on the wrong side, or a CI decrement left out of the premium annuity but
    present in the benefit.
    """
    pi = prem_net_level_pp() if t <= prem_period() else 0.0
    qc = ci_rate_base(t)
    qd = mort_rate_base(t)
    return ((pol_val_pp(t - 1) + pi) * (1.0 + prem_int_rate)         # noqa: F821
            - qc * (accel_rate() * sum_assured() + epv_resid(t + 1))
            - (1.0 - qc) * qd * sum_assured()
            - (1.0 - qc) * (1.0 - qd) * pol_val_pp(t))


def check_pol_val_roll_fwd():
    """True when the 계약자적립액 rolls forward on its own basis in every year."""
    tol = val_tol * max(sum_assured(), 1.0)                          # noqa: F821
    return all(abs(check_pol_val_roll_fwd_resid(t)) <= tol
               for t in range(1, proj_len() + 1))


def check_accel_complement_resid(t):
    """The complement residual for every cohort formed in policy year t; zero everywhere.

    **The identity this product exists to demonstrate**: what is accelerated and what is
    left add to exactly the 기본보험금 that was in force when the claim arose,
    ``a B + r B = B`` and ``a f B + (1 - a f) B = B``, so the acceleration is a
    redistribution of one sum assured across two dates and never adds cover [S1] [S2].
    It is asserted on the cohorts actually formed in the year, so a first-year model point
    checks both the full and the reduced arithmetic.
    """
    resid = 0.0
    for s in ci_cohort_ids(t + 1):
        if pols_ci_in(t, s) == 0.0:
            continue
        base = base_benefit_pp(1) if s <= 0 else base_benefit_pp(s)
        resid = resid + (accel_benefit_pp(s) + resid_nominal_pp(s) - base)
    return resid


def check_accel_complement():
    """True when the acceleration and its residual sum to the 기본보험금, every cohort."""
    tol = val_tol * max(sum_assured(), 1.0)                          # noqa: F821
    return all(abs(check_accel_complement_resid(t)) <= tol
               for t in range(1, proj_len() + 1))


def check_resid_floor_resid(t):
    """The residual-floor residual at policy year t; zero everywhere.

    The post-CI death benefit must be at or above **both** of its limbs — the nominal
    complement fixed at the acceleration date and 105% of the account now — so the two
    shortfalls, each floored above at zero, must vanish.  A one-sided ``max`` written the
    wrong way round, or a floor read off the wrong anniversary's account, shows up here
    and nowhere else.
    """
    resid = 0.0
    for s in ci_cohort_ids(t):
        db = resid_db_pp(t, s)
        resid = resid + min(0.0, db - resid_nominal_pp(s))
        resid = resid + min(0.0, db - resid_floor_mult() * pol_val_pp(t))
    return resid


def check_resid_floor():
    """True when the residual death benefit is the maximum of its two limbs, every year."""
    tol = val_tol * max(sum_assured(), 1.0)                          # noqa: F821
    return all(abs(check_resid_floor_resid(t)) <= tol
               for t in range(1, proj_len() + 1))


def check_cv_carve_out_resid(t):
    """The carve-out residual at anniversary t; zero everywhere.

    ``min(0, CV'(t) - CV(t))``.  The consumer-protection design the carve-out exists to
    produce is that **a CI claimant is never worse off on surrender than an unaccelerated
    policyholder at the same duration** [S2] [S4], and this is that statement as an
    inequality with a signed residual.  It is not tautological: it fails the moment the
    suppression is applied to the post-CI cohort, which is the natural mistake to make when
    one surrender-value scale is run over one aggregate policy count.
    """
    return min(0.0, cv_pp_ci(t) - cv_pp(t))


def check_cv_carve_out():
    """True when the post-CI surrender value is never below the pre-CI one."""
    tol = val_tol * max(sum_assured(), 1.0)                          # noqa: F821
    return all(abs(check_cv_carve_out_resid(t)) <= tol
               for t in range(1, proj_len() + 1))


def check_loan_roll_fwd_resid(t):
    """The 보험계약대출 roll-forward residual in policy year t; zero everywhere.

    ``L(t + 1) - (L(t) + draw(t))(1 + i_L)``.  Identically zero in the base run, where
    there is no loan at all; non-trivial the moment the module is switched on, which is
    the point of it.
    """
    return (loan_pp(t + 1)
            - (loan_pp(t) + pol_loan_draw(t)) * (1.0 + i_loan))      # noqa: F821


def check_loan_roll_fwd():
    """True when the loan balance accumulates at ``i_loan`` in every year."""
    tol = val_tol * max(sum_assured(), 1.0)                          # noqa: F821
    return all(abs(check_loan_roll_fwd_resid(t)) <= tol
               for t in range(1, proj_len()))


def check_net_cf_resid(t):
    """The published cash-flow statement's residual in policy year t; zero everywhere.

    :func:`net_cf` less the published ``result_cf()`` columns of the same row.  It closes
    the loop between the total benefit outgo and the five kinds that make it up, so a
    sixth kind added to :func:`claims` and left out of the statement shows up here rather
    than silently vanishing from it.
    """
    return (net_cf(t) - premiums(t) + claims(t, "CI") + claims(t, "DEATH")
            + claims(t, "DEATH_CI") + claims(t, "LAPSE")
            + claims(t, "LAPSE_CI") + claim_expenses(t) + expenses(t)
            + commissions(t))


def check_net_cf():
    """True when the net cash flow equals the sum of its published columns, every year."""
    tol = val_tol * max(sum_assured(), 1.0)                          # noqa: F821
    return all(abs(check_net_cf_resid(t)) <= tol
               for t in range(1, proj_len() + 1))


def result_cf():
    """Result table of cash flows, indexed by policy year t.

    ``pols_if`` is the start-of-year count of policies in force in **both** states, which
    is the weight on the maintenance expense of the same row; the decrement-weighted
    figures are in ``result_pols()``.  ``net_cf`` carries the notes' own income-positive
    sign.  ``expenses`` is acquisition and maintenance; the claim handling expense is
    beside it in ``claim_expenses``, as in every model in the sister libraries.  The five
    ``claims_*`` columns are published rather than their total, so that the columns sum to
    ``net_cf`` and the acceleration can be read apart from the death benefit it
    accelerates.
    """
    ts = list(range(1, proj_len() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "claims_ci": [claims(t, "CI") for t in ts],
            "claims_death": [claims(t, "DEATH") for t in ts],
            "claims_death_ci": [claims(t, "DEATH_CI") for t in ts],
            "claims_lapse": [claims(t, "LAPSE") for t in ts],
            "claims_lapse_ci": [claims(t, "LAPSE_CI") for t in ts],
            "claim_expenses": [claim_expenses(t) for t in ts],
            "expenses": [expenses(t) for t in ts],
            "commissions": [commissions(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_pols():
    """Result table of policy counts and decrement rates, indexed by policy year t.

    The two states side by side, so that the migration from ``pols_if_pre`` to
    ``pols_if_ci`` — which is the product — can be read directly.
    """
    ts = list(range(1, proj_len() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "pols_if_pre": [pols_if_pre(t) for t in ts],
            "pols_if_ci": [pols_if_ci(t) for t in ts],
            "pols_if_pay": [pols_if_pay(t) for t in ts],
            "pols_ci": [pols_ci(t) for t in ts],
            "pols_death": [pols_death(t) for t in ts],
            "pols_death_ci": [pols_death_ci(t) for t in ts],
            "pols_lapse": [pols_lapse(t) for t in ts],
            "pols_lapse_ci": [pols_lapse_ci(t) for t in ts],
            "mort_rate": [mort_rate(t) for t in ts],
            "ci_rate": [ci_rate(t) for t in ts],
            "lapse_rate": [lapse_rate(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_val():
    """Result table of the account, the surrender values and the benefit levels, by t.

    ``cv_pp`` is the amount payable before a CI event and ``cv_pp_ci`` the amount payable
    after one, so the carve-out and the step at 납입완료 can be read off the same table.
    ``resid_db_avg_pp`` against ``resid_nominal_pp`` at any duration shows how far the 105%
    account floor has taken over the residual.
    """
    ts = list(range(1, proj_len() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pol_val_pp": [pol_val_pp(t) for t in ts],
            "surr_chg_pp": [surr_chg_pp(t) for t in ts],
            "cv_std_pp": [cv_std_pp(t) for t in ts],
            "cv_pp": [cv_pp(t) for t in ts],
            "cv_pp_ci": [cv_pp_ci(t) for t in ts],
            "base_benefit_pp": [base_benefit_pp(t) for t in ts],
            "accel_benefit_pp": [accel_benefit_pp(t) for t in ts],
            "resid_nominal_pp": [resid_nominal_pp(t) for t in ts],
            "resid_db_avg_pp": [resid_db_avg_pp(t) for t in ts],
            "loan_pp": [loan_pp(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

prem_int_rate = 0.025

i_loan = 0.04

loan_cap_rate = 0.8

net_prem_ratio = 0.8

surr_chg_rate = 0.05

surr_chg_coef_cap = 20

surr_chg_sa_rate = 0.01

surr_chg_years_cap = 7

ci_cover_end_age = 100

ci_wait_days = 90

first_year_factor = 0.5

breast_share_m = 0.005

breast_share_f = 0.268

lapse_ll_first = 0.1

lapse_ll_target = 0.001

lapse_post_paidup = 0.008

lapse_ci_factor = 0.5

expense_acq = 500000.0

expense_maint = 60000.0

expense_claim = 300000.0

inflation_rate = 0.01

comm_init_rate = 0.8

comm_renewal_rate = 0.03

roll_fwd_tol = 1e-10

val_tol = 1e-08

math = ("Module", "math")

pd = ("Module", "pandas")
