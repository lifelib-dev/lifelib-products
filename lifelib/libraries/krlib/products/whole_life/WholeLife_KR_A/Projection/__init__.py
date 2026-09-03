# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""The by-policy projection of the :mod:`~.WholeLife_KR_A` model.

The Space is parameterized by ``point_id``, so ``Projection[1]`` is an ItemSpace
projecting model point 1::

    >>> Projection[1].result_cf()          # the worked example's anchor cell
    >>> Projection.point_id = 5            # or switch the default

``t`` counts **policy years**, 1-based: ``t = 1`` is the first policy year and
``t = proj_len() = omega_age() - age_at_entry() + 1`` the last. A 종신 contract has no
maturity date and no 만기보험금, so the horizon is the terminal age of the mortality table,
every remaining life dies in year ``proj_len()``, and nothing is paid there but the death
benefit. **There are no tail states.**

.. rubric:: The age basis is 보험나이

Ages are **보험나이** (*boheom nai*, insurance age) throughout — the model point's
``issue_age``, the mortality table's index and :func:`age`. 보험나이 is the 만 나이 at the
계약일 with a fraction under six months discarded and six months or more rounded up, and it
increments on each 계약해당일 (policy anniversary) rather than on the birthday [REG-R25
제21조]. That is exactly what an annual grid stepped on anniversaries does, so the ageing
is correct by construction. What is **not** correct by construction is the table: the
public statistics the shipped ``mort_table.csv`` is calibrated against — 국가데이터처
완전생명표 and its 기대여명 [REG-R38] — are published on **만나이**, and no public mapping
between the two bases exists, so no conversion is applied **[std]**. The six-month rule
means 보험나이 and 만나이 differ for half of all issue dates, and the resulting bias reads
the table about half a year of ageing too young.

.. rubric:: Input data

Inputs are **external files**: plain CSVs living in the model folder's parent directory,
``products/whole_life/``, read at run time rather than stored inside the model. Each table
has a filename Reference and a reader Cells, both on :mod:`~.WholeLife_KR_A.Data`, reached
here through the ``data`` Reference:

======================  ==============================  ==========================
Reference               Cells                           File
======================  ==============================  ==========================
model_point_file        data.model_point_table()        model_point_table.csv
mort_table_file         data.mort_table()               mort_table.csv
lapse_table_file        data.lapse_table()              lapse_table.csv
======================  ==============================  ==========================

.. rubric:: Naming

Cells names follow lifelib's ``basiclife.BasicTerm_S`` and ``savings.CashValue_SE``
wherever those models have an analogue — ``pols_*`` for policy counts, plural nouns for
cash flows, ``*_rate`` for rates, ``*_pp`` for per-policy amounts, ``claims(t, kind)`` with
an uppercase ``kind`` string, ``pols_if_at(t, timing)`` for the within-year in-force reads.
The technical notes use the compact actuarial symbols of the product specification instead.
The mapping is:

=========================  ==================================  ============================
Notes symbol               Cells                               Meaning
=========================  ==================================  ============================
(none)                     model_point()                       The selected model point row
x                          age_at_entry()                      가입나이 (보험나이) at issue
x + t - 1                  age(t)                              Attained 보험나이 in year t
omega                      omega_age()                         Terminal age of the table
T                          proj_len()                          Projection length in years
m                          prem_term(), prem_period()          납입기간; 0 is 전기납
(none)                     prem_end()                          Last year a premium is due
n_sc                       surr_chg_period()                   해약공제기간 = min(m, 7)
SA                         sum_assured(), sum_assured_at(t)     보험가입금액, at issue and in year t
G                          premium_pp(), premium_at_pp(t)       Annual 영업보험료
(none)                     prem_gross_calc_pp()                Loaded premium on the model's own basis
P                          prem_net_level_pp()                 연납순보험료 over 납입기간
P20                        prem_net_20yr_pp()                  연납순보험료 on the 별표 14 20년납 footing
i                          prem_int_rate                       예정이율, the pricing rate
(declared)                 decl_rate()                         공시이율 on a 금리연동형 contract
(floor)                    min_guar_rate                       최저보증이율
i_acc                      acc_int_rate()                      The rate the account accrues at
q(x+t)                     mort_rate(t)                        적용위험률 in policy year t
(table q)                  mort_rate_at_age(y)                 Table rate at attained age y
(none)                     mort_be_factor()                    Multiplier on the table rate
w(t)                       lapse_rate(t)                       Annual 해지율
(base w)                   lapse_rate_base(t)                  Before the 유지보너스 spike
s                          lapse_spike()                       Additional lapse at a bonus date
u(t)                       waiver_rate(t)                      납입면제 incidence
V(t)                       pol_val_pp(t)                       계약자적립액 at anniversary t
(unreduced V)              pol_val_base_pp(t)                  계약자적립액 before any 감액
(prospective V)            prosp_val_pp(t)                     The same value, prospectively
SC(t)                      surr_chg_pp(t)                      해약공제액
(cap)                      surr_chg_cap_pp()                   표준해약공제액, 별표 14
W(t)                       cv_std_pp(t)                        표준형 twin's 해약환급금
k                          cv_floor_ratio()                    Suppression factor
(none)                     cv_mult(t)                          k before 납입완료, 1 after it
CV(t)                      cv_pp(t)                            해약환급금 actually payable
k W(t)                     cv_susp_pp(t)                       Suppressed value at every t
(bonus)                    bonus_pp(t)                         유지보너스 credited at 납입완료
cumprem(t)                 cum_prem_pp(t)                      Premiums paid to year t
(환급률)                    refund_ratio(t)                     CV(t) / cumprem(t)
L(t)                       loan_pp(t)                          보험계약대출 balance
D(t)                       loan_draw(t)                        Amount drawn in year t
i_L                        loan_int_rate()                     보험계약대출이율 = i + 1.5%
l(t)                       pols_if(t)                          In force at start of year t
(paying)                   pols_if_pay(t)                      In force and paying premium
(waived)                   pols_waived(t)                      In force with premiums waived
l(t)(1-q), l(t+1)          pols_if_at(t, timing)               BEF_DECR/BEF_LAPSE/AFT_DECR
(deaths)                   pols_death(t)                       Expected deaths in year t
(lapses)                   pols_lapse(t)                       Expected 해지 in year t
(surrenders paid)          pols_surr(t)                        Lapses that are not reinstated
(부활)                      pols_reinstate(t)                   Reinstatements at the start of t
G lp(t)                    premiums(t)                         Premium income
(SA - L)D, (CV - L)S       claims(t, kind)                     Benefit outgo by kind
ec D(t)                    claim_expenses(t)                   Claim handling expense
E0, e(t)                   expenses(t)                         Acquisition and maintenance
(none)                     acq_cost_pp()                       계약체결비용 at issue
c0, c_r                    commissions(t)                      Commission outgo
CF(t)                      net_cf(t)                           Net cash flow, income positive
=========================  ==================================  ============================

Three names needed care.

``surr_chg_pp`` is the 해약공제액 and ``surr_chg_cap_pp`` the **표준해약공제액** that bounds
it. The cross-library review retired ``surr_charge_pp`` for the first; the second is a
Korean quantity with no analogue in any sister library, and the ``_cap_`` in the middle is
what says which of the two a reader is looking at.

``cv_floor_ratio`` is ``k``. The register retired the bare ``cv_ratio`` because a Korean
whole life model carries two ratios on the same object — the suppression factor and the
환급률 — and a name that does not say which is which is a bug waiting to be written.
:func:`refund_ratio` is the other one.

``pol_val_pp`` is the **계약자적립액**, a contractual quantity, and not a reserve. The two
were the same object under a different name until IFRS 17: a pre-2023 상품요약서 writes
「순보험료식 책임준비금에서 해지공제액을 공제한 금액」 and a 2024 one writes 「계약자적립액에서
미상각신계약비를 공제한 금액」 for the identical identity [S2] [S8]. Under K-IFRS 제1117호 the
insurer no longer books a 보험료적립금 as a separate statutory reserve, so the surrender
basis had to be re-anchored on a contractually defined account. **This model computes no
책임준비금 at all**, and none of ``pol_val_pp``, ``cv_std_pp`` or ``cv_pp`` may be read as
one.

.. rubric:: The 무해지 / 저해지 cliff is a step, not a ramp

``CV(t) = k W(t)`` for ``t < m`` and ``CV(t) = W(t)`` for ``t >= m``, where ``W(t)`` is the
**표준형 comparison twin's** surrender value — a non-marketed product with identical
benefits priced with the lapse assumption switched off, which four carriers name in the
same sentence and say they do not sell [S1] [S2] [S3] [S4]. Three consequences follow and
none is optional.

The factor multiplies **one** policy value, so there is no second account run anywhere in
this model, and ``CV(t)`` is independent of the sold form's own premium. That single fact
is the whole of the 환급률 arithmetic that sells the product: the suppressed form's
post-완납 surrender value is identical to the 표준형's while its premiums are lower, so its
refund ratio is mechanically higher — nothing is credited that the 표준형 does not get, the
denominator is simply smaller.

The transition at ``t = m`` is a **step**: ``cv_pp(m) / cv_susp_pp(m)`` is exactly
``1 / k``, and anything between is an interpolation the contract does not have. Both
quantities exist at ``t = m`` and the model publishes both.

**The step is not a surrender-charge effect.** 감독규정 제7-66조제1항제2호 caps the
해약공제기간 at seven years, so on the anchor's 20년납 contract the charge is fully
amortised by duration 7 — thirteen years before the cliff. The step is the removal of ``k``
and nothing else.

On a 전기납 point (``prem_term = 0``) the suppressed period runs for life and the step never
happens, which is why one shipped model point is written that way.

.. rubric:: Lapse is behavioural, and the lapse vector is the whole argument

**No 자동대출납입 was found in any Korean document read for this library.** ``jplib``'s
whole life chassis turns on the 自動振替貸付, which advances the premium against the
surrender value at the end of grace and keeps the contract in force, so that lapse there is
a *funded* event. In Korea, on the evidence retrieved, there is no such test: a policyholder
who misses a 14-day 납입최고기간 loses the contract whatever its cash value, and on a
무해지 form receives nothing at all. That absence is **[unverified]** rather than
established — the 생명보험 표준약관 is understood to contain such an article and the
retrieved 별표 15 extract does not carry it — and it is the single highest-value item for a
later research pass, because finding one would change this chassis in kind.

So lapse is a behavioural decrement, and which vector it runs on is a supervisory question.
:func:`lapse_rate` reads ``lapse_table.csv`` by basis. ``loglinear`` is the FSS 원칙모형 of
the November 2024 계리가정 decision — a log-linear decay converging on **0.1% at 납입완료**,
then an ultimate **0.8%** [REG-R27]. ``flat`` is the level comparison basis the same
guidance obliges an insurer to disclose against it. The two are shipped side by side
because that comparison is the disclosure, not an afterthought: the problem the supervisor
named was insurers assuming high lapse right up to 완납 on contracts where lapsing pays
nothing, booking CSM that would never be realised. **A Korean whole life model that does not
expose the lapse vector as a parameter cannot be used in Korea at all.**

.. rubric:: Modules that are off in the base run

Six constructions are implemented and switched off, so that the base run reproduces the
worked example while the machinery stays visible and testable:

- **보험계약대출**, ``loan_util`` at 0. Model point 6 draws the contractual maximum — 80% of
  the *payable* surrender value — at the tenth anniversary of a 저해지 contract, where the
  limit is half its 표준형 size; model point 3 makes the same election on a **무해지**
  contract and draws **exactly nothing**, because during 납입기간 there is no value to lend
  against. The rate is a **vintage** rate, 예정이율 + 1.5% on a 금리확정형 contract and
  공시이율 + 1.5% on a 금리연동형 one, so a policy written in a high-rate era carries a high
  loan rate for life. There is no Korean equivalent of the Japanese loan-excess lapse: the
  balance is simply deducted from every exit.
- **보험료 납입면제**, ``waiver_rate`` at 0 except on model point 7. The trigger is a **50%
  장해지급률** aggregated across body parts from one cause, accident or disease alike, and
  the premiums are **deemed paid to the end of 납입기간** for benefit and surrender-value
  purposes [S2] [S3] [S6] [S8]. That is what makes the waiver an option with value rather
  than a protection feature: on a suppressed form it is the only route to the cliff that the
  policyholder does not have to fund.
- **유지보너스**, ``bonus_rate`` at 0 except on model point 8, a 7년납 단기납 design
  crediting **13.8%** of total premiums to the 계약자적립액 at 납입완료 [S7]. The
  supervisor requires an **additional lapse of at least 30%** at any such bonus date
  [REG-R27], so :func:`lapse_spike` turns on with it; turning the bonus on without the spike
  would misstate the liability in the insurer's favour, which is exactly what the guidance
  exists to prevent.
- **금리연동형 crediting**, ``int_basis`` ``fixed`` except on model point 9. The accrual rate
  becomes a declared 공시이율 floored at a 최저보증이율 of 0.75% [S5], while the net premium
  stays on the 예정이율 fixed at issue — so the account is genuinely path-dependent and the
  prospective identity :func:`check_pol_val_prosp` no longer applies, which is why it is
  defined as zero there rather than asserted.
- **감액**, ``reduce_year`` at 0 except on model point 10. The reduced portion is **treated
  as surrendered** and pays the corresponding 해약환급금 on the basis applying at that
  duration; the sum assured, the premium and the account all restate pro rata, which is
  exact here because every one of them is proportional to the 보험가입금액.
- **부활**, ``reinstate_rate`` at 0 except on model point 10. A stated proportion of one
  year's lapses returns to the paying cohort a year later and is **not** paid a surrender
  value, which is the substantive effect: 부활 requires that the 해약환급금 has not been
  drawn, and the 약관 expressly includes the case where there was none to draw — so a
  무해지 contract is always reinstatable within three years.

``mort_be_factor`` is the last lever, 1.00 on every point but 10. At 1.00 the base run is a
**pricing-table run, not a best estimate**: the shipped table is calibrated toward the
insured level implied by the 제10회 경험생명표 summary, and no retrieved source sizes the
margin inside a Korean carrier's 적용위험률 against its own experience. Claims move
proportionately with it; the terminal rate is held at 1 whatever it is set to, because
``omega_age`` is the horizon of the table and not an experience assumption.

.. rubric:: Sign convention

:func:`net_cf` is **income positive** — premiums less claims, expenses and commission —
which is both the notes' own sign and the library-wide one, so there is no outgo-positive
``liability_cf`` companion to publish: one stream, one sign, one name.
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

    The female premium runs 87%-91% of the male at 보험나이 40 on the three published
    grids, and the female issue-age ceiling is 3 to 8 years higher at the same payment
    term everywhere it is stated.
    """
    v = model_point()["sex"]
    if v not in ("M", "F"):
        raise ValueError("invalid sex")
    return v


def age_at_entry():
    """x: the 가입나이 at issue, on **보험나이**, 15 to 65 on the composite envelope.

    보험나이 (*boheom nai*, insurance age) is the 만 나이 at the 계약일 with a fraction
    under six months discarded and six months or more rounded up, incrementing on each
    계약해당일 rather than on the birthday [REG-R25 제21조].  An annual grid stepped on
    anniversaries therefore ages it correctly by construction.  The maximum issue age of 65
    is much lower than Japan's 80, and the minimum of 15 is statutory: 상법 제732조 voids a
    contract on the death of a person under 15.
    """
    return int(model_point()["issue_age"])


def sum_assured():
    """SA: the 보험가입금액 at issue, level for life on the 평준형 composite.

    ₩10,000,000 to ₩1,000,000,000 (1,000만원 ~ 10억원) on the composite envelope.  One
    amount pays one benefit: Korea puts **no severe-disability acceleration** on this
    chassis, so unlike Japanese whole life there is no second benefit inside the same
    decrement.  The 체증형, 체감형, 전환나이-step and max(가입금액, premiums x ratio)
    shapes are all real in the market and all excluded from the composite.
    """
    return float(model_point()["sum_assured"])


def prem_term():
    """m: the 보험료 납입기간 in years as entered, with **0 denoting 전기납 (종신납)**.

    The composite menu is 5 / 7 / 10 / 15 / 20 / 30년납, 60 / 65 / 70세납 and 전기납.
    Korean payment terms are shorter and denser at the front than Japanese ones — 5년납 and
    7년납 appear everywhere — and 전기납 is offered but is the default nowhere, which is the
    단기납 market structure showing through.  On a 전기납 contract there is no 납입완료 date,
    the suppressed period runs for life and the cliff never occurs; use :func:`prem_period`
    for the effective number of years.
    """
    return int(model_point()["prem_term"])


def prem_period():
    """m: the effective 납입기간, ``proj_len()`` on a 전기납 contract.

    The suppressed period is identical to the premium-paying period on the composite
    design, so this is also the duration at which :func:`cv_pp` steps up where it steps up
    at all.  Two of the five suppression designs in the source set put the step somewhere
    else — at seven years on one and at 납입기간 + 3년 on another — which is why the model
    exposes the date rather than hard-coding it.
    """
    return prem_term() if prem_term() > 0 else proj_len()


def prem_end():
    """The last policy year in which a premium is due, which is ``prem_period()``.

    Kept as its own cells because nothing else about the contract stops there: maintenance
    expense, death claims, surrender benefits and the account all continue for life, and a
    projection truncated at 납입완료 misses the majority of the liability.
    """
    return prem_period()


def premium_pp():
    """G: the level annual 영업보험료 per policy, payable in advance in years 1 to m.

    Level and guaranteed for the whole of 납입기간 on the 금리확정형 composite, with no
    review and no crediting-rate feedback, which puts every year of it inside any
    defensible contract boundary.  On model point 2 the value is **sourced**: ₩257,050 a
    month is published for exactly that cell — 남 40세, 1억원, 종신, 20년납, 월납, 표준형
    [S4] — and the annual figure is 12 times it **[std]**, no carrier in the set publishing
    an annual-mode scale, so the modal discount a real 연납 rate would carry is not applied
    and the annual premium is slightly overstated.  The anchor's own premium is that figure
    times the **90.0%** ratio a carrier publishes for a 50% suppression at one identical
    cell [S1].  On the other points it is a **[std]** loading of
    :func:`prem_net_level_pp`; :func:`prem_gross_calc_pp` reproduces the rule and the fit
    against the sourced cell is reported in the technical notes.

    Note that the published figure is already **net of the 1.5% 고액계약할인**, which bites
    at the anchor because 1억원 is well above the 3,000만원 threshold [S1]; a model applying
    the discount again would double-count it.
    """
    return float(model_point()["premium_annual"])


def prem_susp_ratio():
    """The ratio of this form's premium to the 표준형's — the price of the suppression.

    1.000 표준형; **0.900** at ``k = 0.50``, the 처브라이프 observation at that exact factor
    [S1]; **0.815** at ``k = 0.30``, the DB생명 1종 observation [S4]; and **0.780** at
    ``k = 0.00`` **[std]**, extrapolating the observed relation below the deepest sold
    design in the set.  The observed range across real products is 81.5%-95.4%, deepest
    discount at deepest suppression.  The FSC's own illustration of a post-2020 design shows
    62.2% [REG-R28], much larger than any sold product, and is best read as an illustration
    of returning the whole give-up as premium rather than as a market observation.
    """
    return float(model_point()["prem_susp_ratio"])


def cv_floor_ratio():
    """k: the suppression factor — 1.00 표준형, 0.50 저해지환급형, 0.00 무해지환급형.

    A **multiplier on one common policy value**, not a second reserve basis: from 납입완료
    the suppressed and the 표준형 surrender values are identical to the won in every
    published grid [S1] [S4] [S6].  0.50 is the composite because it is the modal factor —
    three carriers — and because 감독규정 제7-66조제4항제2호 attaches two further design
    conditions only where the value during 납입기간 falls **below** 50% of the 표준형's, so a
    design at exactly 50% sits at the threshold rather than under it [REG-R19].  The 0.30
    and 0.00 columns are shipped so the cliff can be seen at all three depths.
    """
    k = float(model_point()["cv_floor_ratio"])
    if not 0.0 <= k <= 1.0:
        raise ValueError("cv_floor_ratio must lie in [0, 1]")
    return k


def int_basis():
    """The crediting basis: ``fixed`` (금리확정형, the composite) or ``linked`` (금리연동형).

    The composite is 금리확정형 for an evidential reason: the 상품요약서 that publish
    complete cash values are 금리확정형 [S8], and the one full 약관 retrieved is a 유니버셜
    contract whose account mechanics belong to ``Pension_KR_A`` and ``VA_KR_S`` [S5].
    """
    v = model_point()["int_basis"]
    if v not in ("fixed", "linked"):
        raise ValueError("invalid int_basis")
    return v


def decl_rate():
    """The declared 공시이율 on a 금리연동형 contract; ignored on a 금리확정형 one.

    A Korean declared rate is 공시기준이율 plus or minus a 조정률, and the 공시기준이율 is
    ``외부지표금리 x alpha + 운용자산이익률 x (1 - alpha)`` with **alpha capped at 60%**
    [REG-R23] [REG-R24].  That cap is the modelling point: the rate is majority-weighted to
    the insurer's own realised 운용자산이익률 rather than to market yields, which is why a
    crediting assumption in this library is a slow-moving **[std]** scalar and not a
    function of a yield curve.  The shipped value on the 금리연동형 point is 2.75%, the
    평균공시이율 in force before its 2026 fall to 2.50% [S10] [REG-R48].
    """
    return float(model_point()["decl_rate"])


def acc_int_rate():
    """i_acc: the rate the 계약자적립액 accrues at.

    The 예정이율 on a 금리확정형 contract, and the declared 공시이율 floored at the
    최저보증이율 on a 금리연동형 one — 감독규정 제7-60조제10호 requires such a product to set
    a 최저보증이율 or a 최저보증금액, and 연복리 **0.75%** is the floor stated verbatim in the
    one full 약관 retrieved [S5] [REG-R16].  The **net premium stays on the 예정이율**,
    fixed at issue: only the accrual moves, which is what makes the linked account
    path-dependent.
    """
    if int_basis() == "linked":
        return max(decl_rate(), min_guar_rate)                       # noqa: F821
    return prem_int_rate                                             # noqa: F821


def lapse_basis():
    """The lapse basis in force: ``loglinear`` (the FSS 원칙모형) or ``flat``."""
    v = model_point()["lapse_basis"]
    if v not in tuple(data.lapse_table().index):                     # noqa: F821
        raise ValueError("invalid lapse_basis")
    return v


def mort_be_factor():
    """The multiplier on the table mortality rate; **1.00 in the base run**.

    1.00 is a choice, not a default: it means the base run is a **pricing-table run, not a
    best estimate**.  The shipped table is calibrated toward the insured level implied by
    the 제10회 경험생명표 summary statistics, and no retrieved source sizes the margin a
    Korean carrier's 적용위험률 carries against its own experience — the two disclosed grids
    differ from each other by 10%-23% at every age and sex [S2] [S8], which brackets the
    level rather than fixing it.  A production basis would move claims proportionately.
    """
    return float(model_point()["mort_be_factor"])


def waiver_rate(t):
    """u(t): the 보험료 납입면제 incidence rate in policy year t; **0 in the base run**.

    The transition out of the premium-paying cohort into the waived state, on a **50%
    장해지급률** aggregated across body parts from one cause — accident or disease alike —
    on the 장해분류표 of 생명보험 표준약관 부표 3 [S2] [S3] [S6] [S8] [REG-R25].  Zero once
    no premium is due, because there is then nothing to waive.  The level is **[std]**: no
    Korean disability incidence table is public, and the disease riders that extend the
    trigger — 3대질병 and 6대질병 forms with a 90-day 면책기간 on the cancer limb — are
    parameterized through the same rate rather than modelled separately.
    """
    if t < 1 or t > prem_end():
        return 0.0
    return float(model_point()["waiver_rate"])


def loan_util():
    """The fraction of the **contractual** 보험계약대출 limit drawn; 0 in the base run.

    1.0 draws the contractual maximum.  There is no public Korean take-up data of any kind,
    so both this and :func:`loan_year` are **[std]** model point inputs; the limit and the
    rate are sourced.
    """
    return float(model_point()["loan_util"])


def loan_year():
    """The policy year at which the 보험계약대출 is drawn, or 0 for no drawdown.

    A model point column rather than a fixed Reference, because *when* the loan is taken is
    the whole demonstration: a draw during 납입기간 on a 저해지 contract is limited to 80%
    of the **suppressed** value, half its 표준형 size, and the same election on a 무해지
    contract draws nothing at all.
    """
    v = int(model_point()["loan_year"])
    if v == 1:
        raise ValueError("loan_year must be 0 or at least 2")
    return v


def bonus_rate():
    """The 유지보너스 rate credited to the 계약자적립액 at 납입완료; 0 in the base run.

    A **단기납** feature rather than a whole-life one: the published rates are 10.8% of
    total 주보험 premiums on a 5년납 design, 13.8% on a 7년납 and 15.0% on a 10 or 15년납,
    with a second 18.5% credit at duration 10 on the short terms [S7].  It produces a
    **second step** in the surrender-value curve, and it is the feature that produced the
    2023-24 refund-ratio competition.  Switching it on switches :func:`lapse_spike` on with
    it, because the supervisor requires an additional lapse of at least 30% at the bonus
    date [REG-R27].
    """
    return float(model_point()["bonus_rate"])


def reduce_year():
    """The policy year at whose anniversary a 감액 is made, or 0 for none.

    감액 is universal on this chassis and is a **partial surrender**: 「그 감액된 부분은
    해지된 것으로 보며 … 해지환급금을 계약자에게 지급합니다」 [S5 제20조].  On a suppressed
    contract that is not a caveat but the main event — a reduction made during 납입기간 pays
    at ``k W(t)``, and on a 무해지 contract it pays nothing.
    """
    v = int(model_point()["reduce_year"])
    if v < 0:
        raise ValueError("reduce_year must be 0 or positive")
    return v


def reduce_frac():
    """The fraction of the 보험가입금액 surrendered at :func:`reduce_year`.

    The sum assured, the premium and the account all restate pro rata, which is **exact**
    on this design rather than an approximation, because each is proportional to the
    보험가입금액.  The 약관's own worked example restates 이미 납입한 보험료 by the ratio of
    the post- to the pre-reduction 계약자적립금 [S5 제20조].
    """
    f = float(model_point()["reduce_frac"])
    if not 0.0 <= f < 1.0:
        raise ValueError("reduce_frac must lie in [0, 1)")
    return f


def reinstate_rate():
    """The proportion of a year's lapses reinstated a year later; 0 in the base run.

    부활 is available within **three years** of a 해지, on fresh 고지 and payment of the
    arrears with interest, and the 약관's parenthesis is the operative point for this
    product: the 해약환급금 counts as undrawn 「해지환급금이 없는 경우를 포함」 — so **a
    무해지 contract is always reinstatable**, there having been no value to draw [S5 제26조]
    [REG-R25 제27조].  That makes lapse on this chassis a non-terminal state.  The
    proportion is **[std]**; no Korean reinstatement statistic is public.  On the annual
    grid the lag is one year and no premium instalment falls inside it, so the arrears of
    제27조 produce no separate cash flow **[std]**; what the module does produce is a lapse
    that is **not** paid a surrender value, which is the substantive effect.
    """
    return float(model_point()["reinstate_rate"])


def pols_if_init():
    """The number of policies in force at the start of policy year 1: one.

    Every model point is a single policy, so the whole ``result_cf()`` frame is a
    per-policy-issued statement and can be scaled by a real portfolio count directly.
    """
    return 1.0


def omega_age():
    """omega: the terminal age of the mortality table, the first age at which q = 1.

    115 on the shipped **[std]** table, for both sexes.  It is a hard model parameter and
    not a rounding: a 종신 contract has no expiry, so the horizon is the table's, and
    projecting a Korean whole life contract to 100 truncates the liability while projecting
    it to 120 invents one.  The 제10회 경험생명표's own terminal age is not public.
    """
    tbl = data.mort_table().loc[sex()]                               # noqa: F821
    return int(tbl.index[tbl["mort_rate"] >= 1.0][0])


def proj_len():
    """T = omega - x + 1: the projection length in policy years.

    There is no maturity date and no 만기보험금, so the horizon is the table's and not the
    contract's.  Every remaining life dies in year T, ``pols_if(T + 1)`` is zero, and
    nothing is paid at the horizon other than the death benefit.
    """
    return omega_age() - age_at_entry() + 1


def age(t):
    """x + t - 1: the attained 보험나이 at the start of policy year t."""
    return age_at_entry() + t - 1


def mort_rate_at_age(y):
    """The shipped table's 적용위험률 at attained 보험나이 y, before ``mort_be_factor``.

    Read from ``mort_table.csv``, a **[std]** construction anchored on the two disclosed
    carrier grids [S2] [S8] and calibrated to an insured 65세 기대여명 [REG-R38] [REG-R33];
    **not** the 제10회 경험생명표, which is not published.  This is the rate the contractual
    account construction uses, unadjusted: ``mort_be_factor`` is a best-estimate lever on
    the *decrement*, not a change to the 산출방법서 basis.
    """
    return float(data.mort_table().loc[(sex(), y), "mort_rate"])     # noqa: F821


def mort_rate_base(t):
    """The table mortality rate in policy year t, at attained 보험나이 ``age(t)``."""
    return mort_rate_at_age(age(t))


def mort_rate(t):
    """q(t): the mortality decrement applied in policy year t.

    The table rate times :func:`mort_be_factor`, capped at 1.  At the table's terminal age
    the rate is held at 1 whatever the factor is: ``omega_age`` is the horizon of the table
    and a structural property of the projection, not an experience assumption, and scaling
    it would leave lives alive past the end of the table.

    There is **no separate disability decrement**.  Korea pays no 고도장해보험금 at the sum
    assured on this chassis; the disability trigger waives the premium and continues the
    contract, which is :func:`waiver_rate` and a state rather than an exit.
    """
    if age(t) >= omega_age():
        return 1.0
    return min(1.0, mort_rate_base(t) * mort_be_factor())


def disc_factor():
    """v = 1 / (1 + i_acc): the discount factor the account accrues on."""
    return 1.0 / (1.0 + acc_int_rate())


def disc_factor_prem():
    """v = 1 / (1 + i): the discount factor of the pricing basis, the 예정이율.

    **2.50% flat [std]**, taken as the centre of the 2.25%-2.75% band actually read from
    six carrier documents [S1] [S2] [S5] [S6] [S7] [S8], on the 0.25 percentage-point grid
    Korean rate-setting uses, and equal to the **2026 평균공시이율** [REG-R48], which is the
    regulatory reference rate against which product design is tested.  Unlike Japan, Korea
    publishes the pricing rate — but what carriers publish is a disclosure of it, not the
    filed 산출방법서.
    """
    return 1.0 / (1.0 + prem_int_rate)                               # noqa: F821


def epv_death(y):
    """A(y): the EPV at attained age y of 1 payable at the end of the year of death.

    On the **pricing** rate and the shipped table, unadjusted by ``mort_be_factor``.
    Recursive: ``A(y) = v [q(y) + (1 - q(y)) A(y + 1)]`` with ``A(omega + 1) = 0`` and
    ``q(omega) = 1``, so ``A(omega) = v`` and the recursion terminates at the table.
    """
    if y > omega_age():
        return 0.0
    q = mort_rate_at_age(y)
    return disc_factor_prem() * (q + (1.0 - q) * epv_death(y + 1))


def annuity_due(y, n):
    """a-due(y, n): the n-year annuity-due of 1 per year at age y, on the pricing rate.

    ``1 + v p(y) a(y + 1, n - 1)``, zero for ``n <= 0``.  Measured in years of premium, so
    ``SA A(x) / a(x, m)`` is an amount per year.
    """
    if n <= 0:
        return 0.0
    return 1.0 + disc_factor_prem() * (1.0 - mort_rate_at_age(y)) * annuity_due(y + 1, n - 1)


def epv_death_acc(y):
    """A(y) on the **accrual** rate — the same quantity as :func:`epv_death` on i_acc.

    Identical to :func:`epv_death` on a 금리확정형 contract, where the two rates coincide.
    It exists so that :func:`prosp_val_pp` can state the prospective form of the account on
    the rate the account actually accrues at.
    """
    if y > omega_age():
        return 0.0
    q = mort_rate_at_age(y)
    return disc_factor() * (q + (1.0 - q) * epv_death_acc(y + 1))


def annuity_due_acc(y, n):
    """a-due(y, n) on the **accrual** rate; see :func:`epv_death_acc`."""
    if n <= 0:
        return 0.0
    return 1.0 + disc_factor() * (1.0 - mort_rate_at_age(y)) * annuity_due_acc(y + 1, n - 1)


def prem_net_level_pp():
    """P: the 연납순보험료, fixed at issue by equivalence over the 납입기간.

    ``P a-due(x, m) = SA A(x)`` on the 예정이율 and the shipped 적용위험률.  Three
    properties of the recursion it feeds are contractual rather than conventional and a
    model must not lose them: it is **net level**, so the acquisition cost is not
    Zillmerised into the account but deducted from it; it runs on the **표준형** net
    premium, not on the sold form's lower one; and it is bounded below by nothing, the
    account being permitted to sit under the surrender charge with the 해약환급금 floored at
    zero rather than going negative [REG-R19 제7-66조제1항제1호].
    """
    return sum_assured() * epv_death(age_at_entry()) / annuity_due(
        age_at_entry(), prem_period())


def prem_net_20yr_pp():
    """P20: the 연납순보험료 recomputed on a **20년납** footing, for 별표 14.

    별표 14 주3 recomputes the 연납순보험료 that enters the 표준해약공제액 on a 전기납 basis,
    or on a **20년납** basis where the 보험기간 is 20 years or more — which for a 종신
    contract it always is [REG-R20].  So the statutory surrender-charge cap of every model
    point here is already normalised to twenty-year pay, whatever the contract's own
    payment term, and a 단기납 point's cap is computed on the same footing as a 20년납 one's.
    """
    return sum_assured() * epv_death(age_at_entry()) / annuity_due(
        age_at_entry(), surr_chg_prem_years)                         # noqa: F821


def prem_gross_calc_pp():
    """G on the model's own **[std]** loading rule, for comparison with :func:`premium_pp`.

    ``prem_loading x P x prem_susp_ratio()``.  The loading is calibrated once, so that the
    표준형 anchor cell reproduces the published 12 x ₩257,050 [S4]; every other shipped
    point's premium is generated from this rule and rounded to the won.  It is published as
    its own cells rather than folded into :func:`premium_pp` because the anchor premium is
    a **sourced** number and must stay one, and the difference between the two is the fit
    the technical notes report.

    **No expense basis is behind the loading.** Both 상품요약서 in the set define
    계약체결비용 and 계약관리비용 and then give no number, and the 산출방법서 that holds the
    예정사업비율 is a filed but unpublished 기초서류 [S2] [S5] [S8] [REG-R2].
    """
    return prem_loading * prem_net_level_pp() * prem_susp_ratio()    # noqa: F821


def surr_chg_cap_pp():
    """표준해약공제액: the statutory cap on the surrender charge, from 별표 14.

    ``연납순보험료 x 5% x 해약공제계수 + 보험가입금액 x 10/1000``, with the 해약공제계수 for
    a 보장성보험 equal to the **보험기간 capped at 20 years** and the 연납순보험료 recomputed
    on a 20년납 footing [REG-R20].  A 종신 contract always falls in that case, so the formula
    collapses to **one year's net premium plus one per cent of the sum assured**.  The
    보험가입금액 that enters it is the 일반사망보험금 taken before any 체증 or 체감 [REG-R21
    별표 15 제3호·제8호], which on the 평준형 composite is the face amount itself.

    This cap has no US or UK analogue at this level of prescription, and it is the reason a
    Korean surrender-value construction can be defended at all when no insurer publishes an
    expense rate.  The FSC states the same cap as 「보장성보험 월 보험료의 13배 수준」
    [REG-R29]; two forms of one rule agreeing to a few per cent is the strongest available
    check on a parameter nobody publishes.
    """
    return (surr_chg_prem_rate * surr_chg_coef * prem_net_20yr_pp()  # noqa: F821
            + surr_chg_sa_rate * sum_assured())                      # noqa: F821


def surr_chg_period():
    """n_sc: the 해약공제기간 = min(m, 7) years.

    감독규정 제7-66조제1항제2호: 「해약공제기간은 보험료 납입기간 또는 신계약비 부가기간으로
    하되 … 7년 이상일 때에는 7년으로 한다」 [REG-R19].  **The duration is fixed by regulation
    and it is short.**  On the anchor's 20년납 contract the charge is fully amortised by
    duration 7, thirteen years before the cliff — which is why the step at 납입완료 has
    nothing whatever to do with the surrender charge running off.
    """
    return min(prem_period(), surr_chg_max_years)                    # noqa: F821


def surr_chg_pp(t):
    """SC(t): the 해약공제액 embedded in the surrender value at anniversary t.

    ``표준해약공제액 x max(0, 1 - t / n_sc)`` **[std]** — a straight-line run-off of the
    unrecovered 계약체결비용, which is what the 약관 defines the deduction to be: 「이미
    지출한 계약체결비용 해당액으로서 산출방법서에서 정한 방법에 따라 계산한 금액」 [S5
    제2조].  The *cap* is sourced and exact, the *level* is set at the cap by
    :func:`acq_cost_pp`, and only the **shape between the two ends** is standardized, the
    real run-off living in the unpublished 산출방법서.  It scales with any 감액, the
    미상각신계약비 of a surrendered portion being written off with it.
    """
    return (surr_chg_cap_pp() * max(0.0, 1.0 - t / surr_chg_period())
            * sa_factor(t))


def acq_cost_pp():
    """계약체결비용: the acquisition cost incurred at issue, per policy **[std]**.

    Set at the **표준해약공제액 exactly**, which makes :func:`surr_chg_pp` literally the
    unamortised balance of it and closes the loop between the expense the insurer incurs and
    the deduction the policyholder bears.  Footnote-worthy because nobody publishes the
    number: 감독규정 제7-45조제11항 exempts a whole-life death-benefit 보장성보험 from
    publishing a 계약체결비용지수 provided its 계약체결비용 stays within **1.4 x** the
    표준해약공제액, so a reference implementation sitting **at** the cap is conservative and
    defensible [REG-R22].  A research presentation to the FSC's own public hearing records
    that competition had pushed some carriers past it [REG-R37].
    """
    return acq_cost_ratio * surr_chg_cap_pp()                        # noqa: F821


def comm_init_pp():
    """The first-year distributor remuneration per policy **[std]**.

    A share of :func:`acq_cost_pp`, capped by 감독규정 제4-32조제5항, under which first-year
    remuneration may not exceed the **first year's expected premium** — with the projected
    one-year surrender value added to the commission side where the contract deducts 80% or
    more of the 표준해약공제액, which is exactly what a 무해지 or 저해지 design does
    [REG-R22] [REG-R29].  The cap binds on the long-payment-term points, where the premium
    is small against a cap computed on a 20년납 footing.
    """
    return min(comm_init_share * acq_cost_pp(),                      # noqa: F821
               comm_cap_rate * premium_pp())                         # noqa: F821


def sa_factor(t):
    """The proportion of the issue 보험가입금액 still in force in policy year t.

    1 until the 감액 anniversary and ``1 - reduce_frac()`` after it.  Every quantity
    proportional to the sum assured — the premium, the account, the surrender charge — is
    scaled by this one factor, which is exact rather than approximate on a level contract.
    """
    if reduce_year() <= 0 or t <= reduce_year():
        return 1.0
    return 1.0 - reduce_frac()


def sum_assured_at(t):
    """The 사망보험금 in force in policy year t: ``SA`` scaled by any 감액."""
    return sum_assured() * sa_factor(t)


def premium_at_pp(t):
    """The annual 영업보험료 due in policy year t, scaled by any 감액."""
    return premium_pp() * sa_factor(t)


def pol_val_base_pp(t):
    """V(t): the 계약자적립액 at anniversary t on the **issue** sum assured.

    The classical net level recursion the product specification states, solved forward on
    the annual grid::

        V(0) = 0
        V(t) (1 - q) = ( V(t-1) + P 1{t <= m} ) (1 + i_acc) - q SA

    with ``q = q(x + t - 1)``, the rate of the year just ended.  ``V(T)`` is defined as zero:
    at the terminal age ``q = 1``, every remaining life has died and the recursion
    degenerates.

    감독규정 제7-65조제1항 says only that 「계약자적립액은 … 산출방법서에 따라 계산한
    금액으로 한다」 and 제2항 permits it to be computed on an **annualised premium** basis,
    which is the permission that lets an annual grid carry a monthly-premium product's
    account [REG-R18].  제7-66조제1항제4호 adds that the account accrues **monthly before
    납입완료 and daily afterwards**; both formulas render as images in the 고시 and did not
    extract, so the annual accrual here is a **[std]** approximation of them [REG-R19].
    """
    if t <= 0 or t >= proj_len():
        return 0.0
    q = mort_rate_at_age(age(t))
    prem = prem_net_level_pp() if t <= prem_period() else 0.0
    return (((pol_val_base_pp(t - 1) + prem) * (1.0 + acc_int_rate())
             - q * sum_assured()) / (1.0 - q))


def pol_val_pp(t):
    """V(t): the 계약자적립액 actually held at anniversary t, any 감액 applied.

    :func:`pol_val_base_pp` scaled by :func:`sa_factor`.  This is a **contractual** quantity
    and not a 책임준비금: under K-IFRS 제1117호 the insurer books no 보험료적립금 as a
    separate statutory reserve, which is why the 2024 상품요약서 wording re-anchors the
    surrender basis on 계약자적립액 where the pre-2023 one said 순보험료식 책임준비금 [S2]
    [S8].  It never produces a cash flow of its own; what it produces is
    :func:`cv_std_pp`.
    """
    return pol_val_base_pp(t) * sa_factor(t)


def prosp_val_pp(t):
    """The same account, stated prospectively: ``SA A(x+t) - P a-due(x+t, m-t)`` on i_acc.

    Equal to :func:`pol_val_base_pp` at every t **when the accrual rate is the pricing
    rate**, which is the substantive cross-check :func:`check_pol_val_prosp` asserts.  On a
    금리연동형 contract the two rates differ, the account is genuinely path-dependent, and
    the prospective form no longer starts at zero — so the check is defined as zero there
    rather than asserted, and this cells is a diagnostic.
    """
    return (sum_assured() * epv_death_acc(age_at_entry() + t)
            - prem_net_level_pp() * annuity_due_acc(
                age_at_entry() + t, max(prem_period() - t, 0)))


def cv_std_pp(t):
    """W(t): the **표준형** twin's 해약환급금 at anniversary t.

    ``max(0, V(t) - SC(t))``.  The identity 해약환급금 = 적립금 − 해약공제액 is sourced twice
    over and the floor is regulatory rather than decorative: 감독규정 제7-66조제1항제1호 says
    a negative difference 「이를 영(零)으로 처리한다」 [S2] [S8] [REG-R19].

    This is the quantity the suppression multiplies.  Every carrier selling a suppressed
    form names a **comparison product** in the same sentence and says it is not sold:
    「"표준형"의 경우는 … 동일한 보장내용으로 **해지율을 적용하지 않고** … 계산된 상품이며 …
    비교안내를 위한 종목으로 **실제로 판매하지 않습니다**」 [S1], with the same sentence at
    three more carriers [S2] [S3] [S4].  So there is **one** account run in this model and
    one multiplier, never two.
    """
    return max(0.0, pol_val_pp(t) - surr_chg_pp(t))


def cv_mult(t):
    """The multiplier applying to :func:`cv_std_pp` at anniversary t: ``k``, then 1.

    ``k`` for ``t < m`` and 1 for ``t >= m``, and the transition is a **step**.  A surrender
    occurring in policy year m is paid at the end of that year on the **full** value
    **[std ordering]**; the suppressed value applies to years 1 to m - 1.  Always ``k`` on a
    전기납 contract, where the suppressed period runs for life and the step never happens.
    """
    if prem_term() == 0:
        return cv_floor_ratio()
    return cv_floor_ratio() if t < prem_period() else 1.0


def cum_prem_pp(t):
    """cumprem(t): 영업보험료 paid per policy by the end of policy year t.

    The denominator of the **환급률**, which is the number the product is sold on and the
    number the supervisor regulates: 감독규정 제7-66조제4항제2호나목 conditions the deepest
    suppressed designs on their post-완납 환급률 exceeding the greater of 100% and the
    표준형's [REG-R19].
    """
    if t <= 0:
        return 0.0
    add = premium_at_pp(t) if t <= prem_end() else 0.0
    return cum_prem_pp(t - 1) + add


def bonus_pp(t):
    """The 유지보너스 credited at 납입완료 and carried thereafter; 0 in the base run.

    ``bonus_rate() x cum_prem_pp(m)`` from ``t >= m``, an addition to the payable surrender
    value rather than a change to the account recursion **[std]** — the credit is made to
    the 계약자적립액 in the contract, and reproducing that on the annual grid without a
    published crediting formula would be an invention.  Never credited on a 전기납 contract,
    which has no 납입완료 date.
    """
    if bonus_rate() <= 0.0 or prem_term() == 0 or t < prem_period():
        return 0.0
    return bonus_rate() * cum_prem_pp(prem_period())


def cv_pp(t):
    """CV(t): the 해약환급금 actually payable at anniversary t, per policy.

    ``cv_mult(t) W(t)`` plus any 유지보너스.  Everything derived from the surrender value is
    suppressed with it — the 보험계약대출 limit and the 감액 proceeds are computed off this
    number and not off ``W`` — so on a 무해지 contract during 납입기간 both are **zero**, a
    point the FSS made in terms in its 2019 소비자경보 and the 표준약관 repeats [REG-R28]
    [REG-R25 제33조].
    """
    return cv_mult(t) * cv_std_pp(t) + bonus_pp(t)


def cv_susp_pp(t):
    """k W(t): the suppressed value at **every** anniversary, step or no step.

    The value an instant before the step at ``t = m``, against which :func:`cv_pp` an
    instant after must stand in the exact ratio ``1 / k``.  On the fullest published run —
    남 40세, 5,000만원, 10년납, a 50% factor — the payable value goes from ₩25,640,000 at
    duration 9 to ₩57,655,500 at duration 10, a 2.25 x step in one year, and the 환급률 from
    49.9% to 101.0% [S1].
    """
    return cv_floor_ratio() * cv_std_pp(t)


def refund_ratio(t):
    """환급률: the payable surrender value over cumulative premiums paid, at anniversary t.

    Zero where no premium has yet been paid.  The suppressed form's ratio after the cliff is
    mechanically **higher** than the 표준형's — 116.4% against 94.9% at duration 20 on one
    published grid [S4] — because the post-완납 values are identical while the premiums are
    not.  Nothing is credited that the 표준형 does not get; the denominator is smaller.
    """
    cp = cum_prem_pp(t)
    return cv_pp(t) / cp if cp > 0.0 else 0.0


def lapse_rate_base(t):
    """The base annual 해지율 in policy year t, before any bonus-date spike.

    On the ``loglinear`` basis, log-linear in the rate from the first-year value to the
    completion value at ``t = m``, then flat at the ultimate value — the FSS **원칙모형** of
    the November 2024 계리가정 decision, whose practical convergence point is **0.1% at
    납입완료** and whose ultimate rate is **0.8%** [REG-R27].  On the ``flat`` basis, a level
    rate throughout.  The endpoints are read from ``lapse_table.csv``; the **shape between
    them is [std]**, no Korean lapse curve by duration being public.  Two independent bases
    exist in Korea and they do not agree: the *pricing* 적용해지율 is disclosed in the
    상품요약서 at 연 1%~10% during 납입기간 at one carrier and 연 0%~13.4% at another [S2]
    [S8], while the *valuation* basis above is much lower.  This is the single largest
    assumption gap on this product.
    """
    row = data.lapse_table().loc[lapse_basis()]                      # noqa: F821
    w1 = float(row["first_year_rate"])
    wm = float(row["completion_rate"])
    wu = float(row["ultimate_rate"])
    m = prem_period()
    if t > m:
        return wu
    if m <= 1 or w1 <= 0.0:
        return wm
    return w1 * (wm / w1) ** ((min(max(t, 1), m) - 1) / (m - 1))


def lapse_spike():
    """s: the additional 해지율 applied at a 유지보너스 date; 0 unless the bonus is on.

    **30 percentage points**, and it is not a behavioural guess: the supervisor requires an
    additional lapse of at least 30% at any bonus date on a 단기납 design, or a rate backed
    out of the 표준형 product's cumulative persistency, calibrated to the 29.4%-30.2%
    eleventh-year lapse observed on single-premium bancassurance savings [REG-R27].  Turning
    the bonus on without turning the spike on would misstate the liability in the insurer's
    favour, which is exactly what the guidance exists to prevent.
    """
    return lapse_bonus_spike if bonus_rate() > 0.0 else 0.0          # noqa: F821


def lapse_rate(t):
    """w(t): the annual 해지율 applied at the end of policy year t.

    The base rate plus any bonus-date spike, capped at 1.  This is the **annual** rate;
    there is no monthly companion on an annual-grid model.  A lapse is not a pure decrement
    here: unless it is reinstated it pays :func:`cv_pp` net of any 보험계약대출 — and on a
    무해지 contract during 납입기간 that is nothing at all, the whole of the accumulated
    value being forfeited to the fund.  That is the consumer-detriment finding behind the
    2019 소비자경보 [REG-R28].
    """
    w = lapse_rate_base(t)
    if bonus_rate() > 0.0 and prem_term() > 0 and t == prem_period():
        w = w + lapse_spike()
    return min(1.0, w)


def loan_int_rate():
    """i_L: the 보험계약대출이율 — 예정이율 + 1.5%, or 공시이율 + 1.5% on a 금리연동형.

    The formula 「적용이율 + 1.5%」 / 「예정이율 + 1.5%」 is stated at three carriers
    independently, with a 가산금리 of +1.40%~1.50% at one [S9] [S11] [S13].  It is a
    **vintage** rate: because the base is the contract's own 예정이율, a policy written in a
    high-rate era carries a high loan rate for life — one carrier's live published range
    spans 연 3.5%~10.5% across its in-force book, under a 최고 적용 대출이율 of 9.90% [S11]
    [S12].  Korea's sharpest contrast with Japan here is that the *rate* is standard across
    the market and the *limit* is not.
    """
    return acc_int_rate() + loan_spread                              # noqa: F821


def loan_draw(t):
    """D(t): the 보험계약대출 drawn at the start of policy year t; zero in the base run.

    A single drawdown at :func:`loan_year` **[std]** of the elected fraction of the
    contractual limit, which is **80% of the payable 해약환급금 at the previous
    anniversary** net of any existing balance.  The observed limits run 50%-85% at one
    carrier and 50%-80% at another, and the whole value net of the existing loan in the one
    full 약관; the composite takes 80% [S5 제34조] [S11] [S13] [REG-R25 제33조].

    Because the limit is a fraction of the **payable** value it is suppressed with it: half
    its 표준형 size on a 저해지 contract during 납입기간, and **zero on a 무해지 one**.
    """
    if loan_util() <= 0.0 or loan_year() <= 0 or t != loan_year():
        return 0.0
    room = loan_limit * cv_pp(t - 1) - loan_pp(t)                    # noqa: F821
    return max(0.0, min(1.0, loan_util()) * room)


def loan_pp(t):
    """L(t): the 보험계약대출 principal and interest at the start of policy year t.

    ``L(t + 1) = (L(t) + D(t)) (1 + i_L)``, compound, with interest capitalised into
    principal and **no repayment modelled [std]** — repayment is permitted at any time
    without fee, and no Korean repayment statistic is public.  Identically zero in the base
    run, where every benefit is therefore gross.

    The balance is settled **first on every exit**: deducted from a death claim, from a
    voluntary 해약 and, 즉시, from the 해약환급금 on 해지 for non-payment [S5 제34조]
    [REG-R25 제26조].  Korea has no equivalent of the Japanese loan-excess lapse notice —
    the deduction is automatic and termination is driven by the demand period, not by the
    balance — so a balance that outgrows the value simply floors the payment at zero.
    """
    if t <= 1:
        return 0.0
    return (loan_pp(t - 1) + loan_draw(t - 1)) * (1.0 + loan_int_rate())


def pols_waiver(t):
    """Policies moving out of the paying cohort into the 납입면제 state at the start of year t.

    ``pols_if_pay(t) u(t)``.  Zero in the base run, and zero once no premium is due.
    """
    return pols_if_pay(t) * waiver_rate(t)


def pols_pay_exp(t):
    """The premium-paying cohort exposed to the year-t decrements, after the waiver exit."""
    return pols_if_pay(t) - pols_waiver(t)


def pols_waived_exp(t):
    """The 납입면제 cohort exposed to the year-t decrements, this year's entrants included."""
    return pols_waived(t) + pols_waiver(t)


def pols_if_pay(t):
    """The premium-paying cohort in force at the **start** of policy year t.

    ``pols_if_init()`` in year 1, then the survivors of the previous year's mortality and
    lapse plus any 부활.  Equal to :func:`pols_if` in the base run, where no policy ever
    enters the waived state.
    """
    if t < 1 or t > proj_len():
        return 0.0
    if t == 1:
        return pols_if_init()
    return (pols_pay_exp(t - 1) * (1.0 - mort_rate(t - 1))
            * (1.0 - lapse_rate(t - 1)) + pols_reinstate(t))


def pols_waived(t):
    """The 납입면제 cohort in force at the **start** of policy year t.

    A distinct in-force state with its own persistency: **no premium income, full benefit
    outgo, full account accrual** — the premiums are deemed paid to the end of 납입기간 for
    both the 사망보험금 and the 해약환급금 [S2] [S3] [S6] [S8] — and the ordinary mortality
    and lapse decrements.  Carrying the same lapse rate as the paying cohort is **[std]**:
    no Korean persistency statistic distinguishes the two.
    """
    if t < 2 or t > proj_len():
        return 0.0
    return (pols_waived_exp(t - 1) * (1.0 - mort_rate(t - 1))
            * (1.0 - lapse_rate(t - 1)))


def pols_if(t):
    """l(t): the number of policies in force at the **start** of policy year t.

    The premium-paying cohort plus the 납입면제 cohort.  This is the weight on every cash
    flow of the same ``result_cf()`` row.  It is :func:`pols_if_init` in the first policy
    year and 0 at ``proj_len() + 1``, because the table terminates and every remaining life
    dies in the final year.
    """
    if t < 1 or t > proj_len():
        return 0.0
    return pols_if_pay(t) + pols_waived(t)


def pols_if_at(t, timing):
    """The number of policies in force at a point inside policy year t.

    ``"BEF_DECR"``
        l(t), the start of the year, before anything happens; the same number as
        :func:`pols_if` and the weight on that year's cash flows.

    ``"BEF_LAPSE"``
        after deaths and before 해지 — the processing order is **death before lapse**
        **[std order]** — so this is the population surrenders and any 감액 are taken from.

    ``"AFT_DECR"``
        l(t+1) before any 부활, and zero at ``proj_len()`` because the table's terminal rate
        is 1 and nobody survives the final year.
    """
    if timing == "BEF_DECR":
        return pols_if(t)
    if timing == "BEF_LAPSE":
        return pols_if(t) * (1.0 - mort_rate(t))
    if timing == "AFT_DECR":
        return pols_if_at(t, "BEF_LAPSE") * (1.0 - lapse_rate(t))
    raise ValueError("invalid timing")


def pols_death(t):
    """Expected 사망보험금 claims in policy year t, falling at the end of the year.

    One decrement on one amount.  There is no 고도장해 acceleration to add and no separate
    disability exit: the disability trigger on a Korean 종신보험 waives the premium and the
    contract continues, which is :func:`pols_waiver`.
    """
    return pols_if(t) * mort_rate(t)


def pols_lapse(t):
    """Expected 해지 at the end of policy year t, on the survivors of mortality.

    The gross count.  Those that return under 부활 a year later are :func:`pols_reinstate`
    and are **not** paid a surrender value; the rest are :func:`pols_surr`.
    """
    return pols_if_at(t, "BEF_LAPSE") * lapse_rate(t)


def pols_reinstate(t):
    """부활: policies returning to the paying cohort at the start of policy year t.

    ``reinstate_rate()`` of the previous year's lapses, a one-year lag **[std]** that sits
    well inside the three-year 부활 window [S5 제26조] [REG-R25 제27조].  Zero in the base
    run.  The 보장개시일 resets on reinstatement, restarting the two-year suicide clock and
    both contestability clocks — none of which produces a cash flow here, so the resetting is
    stated and not modelled.
    """
    if t < 2 or t > proj_len() or reinstate_rate() <= 0.0:
        return 0.0
    return reinstate_rate() * pols_lapse(t - 1)


def pols_surr(t):
    """The lapses of policy year t that are actually paid a 해약환급금.

    ``pols_lapse(t)`` less those reinstated a year later.  The 약관 conditions 부활 on the
    해약환급금 not having been drawn, so a policy that comes back is one that was never paid
    out — and the parenthesis 「해지환급금이 없는 경우를 포함」 is what makes a 무해지 contract
    always reinstatable [S5 제26조].
    """
    return pols_lapse(t) - pols_reinstate(t + 1)


def premiums(t):
    """Premium income at the start of policy year t, an inflow.

    Carried on :func:`pols_pay_exp` alone: the 납입면제 cohort pays nothing while its
    premiums are **deemed paid** for every benefit purpose, which is the whole point of the
    waiver and the reason it is a state rather than a rate adjustment.  Zero from
    ``prem_end() + 1``; nothing else about the contract stops there.
    """
    if t < 1 or t > prem_end():
        return 0.0
    return premium_at_pp(t) * pols_pay_exp(t)


def claims(t, kind=None):
    """Benefit outgo in policy year t, by kind; the total when kind is omitted.

    ``"DEATH"``
        the 사망보험금 at the end of the year of death, ``(SA - L) D(t)`` floored at zero.
        The benefit is net of any outstanding 보험계약대출 원금과 이자 [S5 제34조] [REG-R25
        제33조].  A refused claim is **not** a zero-payment event in Korea — 상법 제736조
        obliges the insurer to pay 「보험수익자를 위하여 적립한 금액」, in practice the
        계약자적립액 — but the composite carries no exclusion incidence, so nothing is
        deducted here for one **[std]**.

    ``"LAPSE"``
        the 해약환급금 on voluntary 해지, ``(CV(t) - L) S(t)`` floored at zero, paid on the
        survivors of mortality that are not reinstated.  On a 무해지 contract during
        납입기간 this is **identically zero**: there is no surrender cash flow at all until
        납입완료, which is precisely why the lapse assumption over that period is worth so
        much CSM.

    ``"REDUCTION"``
        the 감액 proceeds, ``f (CV(t) - L)`` on the continuing policies at the reduction
        anniversary.  The reduced portion is treated as surrendered and paid on the basis
        applying at that duration, so a reduction made during 납입기간 pays at ``k W(t)``.

    Every one of these is floored at zero: a loan can outgrow both the surrender value and,
    given long enough, the sum assured, and none of them may produce a negative payment.
    """
    if kind is None:
        return sum(claims(t, k) for k in ("DEATH", "LAPSE", "REDUCTION"))
    if kind == "DEATH":
        return max(0.0, sum_assured_at(t) - loan_pp(t)) * pols_death(t)
    if kind == "LAPSE":
        return max(0.0, cv_pp(t) - loan_pp(t)) * pols_surr(t)
    if kind == "REDUCTION":
        if reduce_year() <= 0 or t != reduce_year():
            return 0.0
        return (reduce_frac() * max(0.0, cv_pp(t) - loan_pp(t))
                * pols_if_at(t, "AFT_DECR"))
    raise ValueError("invalid kind")


def claim_expenses(t):
    """The claim handling expense on the year's death claims **[std]**.

    ₩300,000 per claim, uninflated.  **No Korean expense rate as a percentage of premium was
    obtained from any source**: both 상품요약서 in the set define 계약체결비용 and
    계약관리비용 and then give no number, and the 산출방법서 that holds the 예정사업비율 is a
    filed but unpublished 기초서류 [S2] [S5] [S8] [REG-R2].  Published as its own
    ``claim_expenses`` column in :func:`result_cf` and deducted explicitly in
    :func:`net_cf`; it is **not** inside :func:`expenses`.
    """
    return expense_claim_pp * pols_death(t)                          # noqa: F821


def inflation_factor(t):
    """The expense inflation factor in policy year t: ``(1 + pi)^(t-1)`` **[std]**.

    2.0% a year, the Bank of Korea's own inflation target, chosen because no Korean expense
    basis exists to anchor anything better.  Over an eighty-year whole-life horizon 2%
    compounds to 4.9, so the assumption is load-bearing on the tail and is held as its own
    parameter for that reason.
    """
    return (1.0 + inflation_rate) ** (t - 1)                         # noqa: F821


def expenses(t):
    """계약체결비용 and 계약관리비용 in policy year t **[std]** — acquisition and maintenance.

    At issue, the part of :func:`acq_cost_pp` not paid away as :func:`comm_init_pp`.
    Thereafter the 계약관리비용, which the 약관 subdivides into 유지관련비용 and 기타비용 and
    quantifies nowhere: ₩60,000 per policy a year inflating at 2%, plus 2% of premium income
    while premiums are paid.  Maintenance continues **for life**, not to 납입완료 — that is
    the structural point of this product, a contract on which premiums stop after m years and
    obligations do not.  There is no separate surrender expense; it is folded into
    maintenance **[std]**.  The claim handling expense is **not** here: it is
    :func:`claim_expenses`, published in its own column.
    """
    acq = max(0.0, acq_cost_pp() - comm_init_pp()) * pols_if(t) if t == 1 else 0.0
    maint = expense_maint_pp * inflation_factor(t) * pols_if(t)      # noqa: F821
    return acq + maint + expense_maint_prem_rate * premiums(t)       # noqa: F821


def commissions(t):
    """Commission outgo in policy year t **[std]**.

    :func:`comm_init_pp` at issue, then 3% of premium income in years 2 to ``prem_end()``.
    Both levels are standardizations; no Korean carrier publishes a commission scale, and
    what regulation supplies instead is a **cap** — first-year remuneration within the first
    year's expected premium, and an obligation to offer an instalment structure paying no
    more than 60% of the 표준해약공제액 a year [REG-R22] [REG-R29].  No renewal commission is
    paid after 납입완료: a projection that keeps charging it there is charging commission on a
    premium nobody pays.
    """
    init = comm_init_pp() * pols_if(t) if t == 1 else 0.0
    renew = comm_renewal_rate * premiums(t) if 2 <= t <= prem_end() else 0.0  # noqa: F821
    return init + renew


def net_cf(t):
    """CF(t): the net cash flow of policy year t, **income positive**.

    Premiums less death claims, surrender and 감액 benefits, claim handling expense,
    acquisition and maintenance expense and commission.  The library-wide sign, which is
    also the notes' own, so there is no outgo-positive ``liability_cf`` companion.

    The shape to expect on a suppressed form is a new business strain in year 1, a long
    positive stretch while the premium runs and the surrender value is suppressed, and then
    a sign change at ``prem_end() + 1``, where the premium stops and nothing else does.
    **The cliff itself moves less cash than a reader expects, and that is the point.** The
    payable value steps up by ``1 / k`` at 납입완료, but the FSS 원칙모형 puts the lapse rate
    at 0.1% in exactly that year, so almost nobody is there to be paid the step; the
    surrender outgo jumps in the year *after* it, when the rate returns to its 0.8%
    ultimate against a value that has doubled.  Run the same point on the ``flat`` lapse
    basis and the cliff produces a visible one-year hole instead — which is the whole
    reason the two bases are shipped side by side [REG-R27].
    """
    return (premiums(t) - claims(t) - claim_expenses(t) - expenses(t)
            - commissions(t))


def check_pols_roll_fwd_resid(t):
    """The in-force roll-forward residual in policy year t; zero everywhere.

    ``l(t) - l(t+1)`` less deaths and lapses plus the 부활 entering at ``t + 1``.  The last
    term is zero in the base run and is what makes the identity close when the module is on:
    a policy that comes back has not left, and netting it inside the lapse count instead
    would hide a decrement.
    """
    return (pols_if(t) - pols_if(t + 1) - pols_death(t) - pols_lapse(t)
            + pols_reinstate(t + 1))


def check_pols_roll_fwd():
    """True when the in-force roll-forward closes in every projected policy year.

    The library-wide form of a roll-forward check: no argument, one bool over all t, so one
    test can call it across every model.  :func:`check_pols_roll_fwd_resid` gives the signed
    residual of the year that failed.
    """
    return all(abs(check_pols_roll_fwd_resid(t)) <= roll_fwd_tol     # noqa: F821
               for t in range(1, proj_len() + 1))


def check_decrement_sum_resid(t):
    """The cumulative-decrement residual at policy year t; zero everywhere.

    ``l(1)`` plus every 부활 up to ``t + 1``, less every exit up to and including year t,
    less ``l(t+1)``.  At ``t = T`` it is the statement that the decrements sum to one:
    because the table terminates, every policy leaves by one of them, ``l(T + 1) = 0``, and
    there is no residual population and no tail state anywhere in this model.
    """
    exits = sum(pols_death(u) + pols_lapse(u) for u in range(1, t + 1))
    back = sum(pols_reinstate(u) for u in range(2, t + 2))
    return pols_if(1) + back - exits - pols_if(t + 1)


def check_decrement_sum():
    """True when every policy issued leaves by a modelled decrement, in every year."""
    return all(abs(check_decrement_sum_resid(t)) <= roll_fwd_tol     # noqa: F821
               for t in range(1, proj_len() + 1))


def check_pol_val_roll_fwd_resid(t):
    """The 계약자적립액 recursion residual at anniversary t; zero everywhere.

    ``(V(t-1) + P 1{t <= m}) (1 + i_acc) - [q SA + (1 - q) V(t)]`` on the issue sum assured
    and the table rate.  It catches a mis-set 납입기간, a rate applied on the wrong side and
    an off-by-one in the age the rate is read at.  The terminal year is excluded: at
    ``q = 1`` the recursion degenerates and ``V(T)`` is defined as zero rather than solved.
    """
    q = mort_rate_at_age(age(t))
    prem = prem_net_level_pp() if t <= prem_period() else 0.0
    return ((pol_val_base_pp(t - 1) + prem) * (1.0 + acc_int_rate())
            - q * sum_assured() - (1.0 - q) * pol_val_base_pp(t))


def check_pol_val_roll_fwd():
    """True when the account rolls forward on its own basis in every year but the last."""
    tol = val_tol * max(sum_assured(), 1.0)                          # noqa: F821
    return all(abs(check_pol_val_roll_fwd_resid(t)) <= tol
               for t in range(1, proj_len()))


def check_pol_val_prosp_resid(t):
    """The retrospective-to-prospective residual at anniversary t; zero everywhere.

    ``V(t) - [SA A(x+t) - P a-due(x+t, m-t)]``, the substantive cross-check on the account:
    the forward recursion and the closed-form prospective value must agree, and they do only
    if the net premium, the payment period and the discount basis are all consistent.

    Defined as zero on a **금리연동형** contract, where the account accrues at the 공시이율
    while the net premium is fixed on the 예정이율: the account is then genuinely
    path-dependent, the prospective form does not start at zero, and the identity is not a
    property of the contract.
    """
    if acc_int_rate() != prem_int_rate:                              # noqa: F821
        return 0.0
    return pol_val_base_pp(t) - prosp_val_pp(t)


def check_pol_val_prosp():
    """True when the account's retrospective and prospective forms agree at every t."""
    tol = val_tol * max(sum_assured(), 1.0)                          # noqa: F821
    return all(abs(check_pol_val_prosp_resid(t)) <= tol
               for t in range(1, proj_len()))


def check_surr_chg_cap_resid(t):
    """The 표준해약공제액 breach at anniversary t; zero everywhere.

    Two regulatory bounds in one residual: 해약공제액 may not exceed the 표준해약공제액 of
    별표 14 [REG-R20], and it must be **gone** by the end of the 해약공제기간, which
    감독규정 제7-66조제1항제2호 caps at seven years [REG-R19].  Both are properties of the
    construction here, and asserting them is what keeps a later change to the run-off shape
    honest.
    """
    over = max(0.0, surr_chg_pp(t) - surr_chg_cap_pp())
    late = surr_chg_pp(t) if t >= surr_chg_period() else 0.0
    return over + late


def check_surr_chg_cap():
    """True when the 해약공제액 stays under the statutory cap and dies at the 해약공제기간."""
    tol = val_tol * max(sum_assured(), 1.0)                          # noqa: F821
    return all(abs(check_surr_chg_cap_resid(t)) <= tol
               for t in range(0, proj_len() + 1))


def check_cv_cliff_resid(t):
    """The suppression residual at anniversary t; zero everywhere.

    ``CV(t) - [k W(t) 1{t < m} + W(t) 1{t >= m}] - bonus``.  It is the wiring of the
    product's signature mechanic: one policy value, one multiplier, a step at 납입완료 and
    nothing in between.  A ramp introduced anywhere — the shape two of the five suppression
    designs in the source set actually use, and which this composite deliberately does not —
    shows up here rather than quietly changing the answer.
    """
    return cv_pp(t) - cv_mult(t) * cv_std_pp(t) - bonus_pp(t)


def check_cv_cliff():
    """True when the payable value is the multiplier times the twin's, at every duration.

    Three things at once: the residual above closes; the suppressed and 표준형 values are
    **identical from 납입완료**, which every published grid confirms to the won [S1] [S4]
    [S6]; and the payable **value** never exceeds the 표준형 twin's at any duration, which
    is what ``k <= 1`` on one common policy value means.

    That is the value test and not the **환급률** test.  감독규정 제7-66조제4항제2호나목
    conditions the deepest designs on their post-완납 refund *ratio* exceeding the greater of
    100% and the 표준형's [REG-R19], while the FSC's own announcement of the same amendment
    frames it the other way — 「전(全) 보험기간 동안 표준형 보험의 환급률 이내로」 [REG-R28].
    The two readings differ because the denominators differ: the suppressed form's premiums
    are lower, so a value that is never above the 표준형's produces a ratio that is always
    above it after 납입완료.  Both statements are recorded in ``product-spec.md`` as they
    stand and neither is asserted here as a ratio.
    """
    tol = val_tol * max(sum_assured(), 1.0)                          # noqa: F821
    ok = all(abs(check_cv_cliff_resid(t)) <= tol
             for t in range(0, proj_len() + 1))
    ok = ok and all(cv_pp(t) - bonus_pp(t) <= cv_std_pp(t) + tol
                    for t in range(0, proj_len() + 1))
    if prem_term() > 0:
        m = prem_period()
        ok = ok and abs(cv_pp(m) - bonus_pp(m) - cv_std_pp(m)) <= tol
    return bool(ok)


def check_loan_roll_fwd_resid(t):
    """The 보험계약대출 roll-forward residual in policy year t; zero everywhere.

    ``L(t + 1) - (L(t) + D(t)) (1 + i_L)``.  Identically zero in the base run, where there
    is no loan at all; non-trivial the moment the module is switched on, which is the point
    of it.  It also catches the 무해지 case, where the draw is zero because the payable value
    is zero and the balance must therefore stay at zero for ever.
    """
    return (loan_pp(t + 1)
            - (loan_pp(t) + loan_draw(t)) * (1.0 + loan_int_rate()))


def check_loan_roll_fwd():
    """True when the loan balance accumulates at the 보험계약대출이율 in every year."""
    tol = val_tol * max(sum_assured(), 1.0)                          # noqa: F821
    return all(abs(check_loan_roll_fwd_resid(t)) <= tol
               for t in range(1, proj_len()))


def check_acq_cost_cap_resid(t):
    """The acquisition-cost overrun in policy year t; zero everywhere.

    Non-zero only at ``t = 1``, both charges falling at issue; the argument is carried so
    that the cells keeps the library's residual signature.  Two published bounds:
    계약체결비용 within **1.4 x** the 표준해약공제액, the tolerance under which a whole-life
    death-benefit 보장성보험 need not publish a 계약체결비용지수 [REG-R22 제7-45조제11항]; and
    first-year remuneration within the **first year's expected premium** [REG-R22
    제4-32조제5항].
    """
    if t != 1:
        return 0.0
    return (max(0.0, acq_cost_pp() - acq_cost_tolerance * surr_chg_cap_pp())  # noqa: F821
            + max(0.0, comm_init_pp() - comm_cap_rate * premium_pp()))        # noqa: F821


def check_acq_cost_cap():
    """True when the acquisition cost and the first-year commission are inside their caps."""
    tol = val_tol * max(sum_assured(), 1.0)                          # noqa: F821
    return all(abs(check_acq_cost_cap_resid(t)) <= tol
               for t in range(1, proj_len() + 1))


def check_net_cf_resid(t):
    """The published cash-flow statement's residual in policy year t; zero everywhere.

    :func:`net_cf` less the published ``result_cf()`` columns of the same row.  It closes
    the loop between the total benefit outgo and the three kinds that make it up, so a
    fourth kind added to :func:`claims` and left out of the statement shows up here rather
    than silently vanishing from it.
    """
    return (net_cf(t) - premiums(t) + claims(t, "DEATH") + claims(t, "LAPSE")
            + claims(t, "REDUCTION") + claim_expenses(t) + expenses(t)
            + commissions(t))


def check_net_cf():
    """True when the net cash flow equals the sum of its published columns, every year."""
    tol = val_tol * max(sum_assured(), 1.0)                          # noqa: F821
    return all(abs(check_net_cf_resid(t)) <= tol
               for t in range(1, proj_len() + 1))


def result_cf():
    """Result table of cash flows, indexed by policy year t.

    ``pols_if`` is the start-of-year count, which is the weight applied to every cash flow
    on the same row.  ``net_cf`` carries the income-positive sign.  ``expenses`` is
    acquisition and maintenance; the claim handling expense is beside it in
    ``claim_expenses``, as it is in every model in the six libraries.  ``claims_reduction``
    is a column of zeros on every model point but one and is published rather than dropped,
    because 감액 is universal on this chassis and is the only partial-surrender route Korea
    offers — 감액완납 and 연장정기보험 appear in no retrieved Korean document.
    """
    ts = list(range(1, proj_len() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "premiums": [premiums(t) for t in ts],
            "claims_death": [claims(t, "DEATH") for t in ts],
            "claims_lapse": [claims(t, "LAPSE") for t in ts],
            "claims_reduction": [claims(t, "REDUCTION") for t in ts],
            "claim_expenses": [claim_expenses(t) for t in ts],
            "expenses": [expenses(t) for t in ts],
            "commissions": [commissions(t) for t in ts],
            "net_cf": [net_cf(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_pols():
    """Result table of policy counts and decrement rates, indexed by policy year t."""
    ts = list(range(1, proj_len() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pols_if": [pols_if(t) for t in ts],
            "pols_if_pay": [pols_if_pay(t) for t in ts],
            "pols_waived": [pols_waived(t) for t in ts],
            "pols_death": [pols_death(t) for t in ts],
            "pols_lapse": [pols_lapse(t) for t in ts],
            "pols_surr": [pols_surr(t) for t in ts],
            "pols_reinstate": [pols_reinstate(t) for t in ts],
            "mort_rate": [mort_rate(t) for t in ts],
            "lapse_rate": [lapse_rate(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


def result_val():
    """Result table of the account, the surrender charge and the surrender value, by t.

    ``cv_pp`` is the amount payable and ``cv_susp_pp`` the suppressed value at every
    anniversary, so the step at 납입완료 and the value an instant before it can be read off
    the same table.  ``refund_ratio`` is the 환급률 the product is sold on and the ratio the
    supervisor regulates.
    """
    ts = list(range(1, proj_len() + 1))
    return pd.DataFrame(                                             # noqa: F821
        {
            "pol_val_pp": [pol_val_pp(t) for t in ts],
            "surr_chg_pp": [surr_chg_pp(t) for t in ts],
            "cv_std_pp": [cv_std_pp(t) for t in ts],
            "cv_pp": [cv_pp(t) for t in ts],
            "cv_susp_pp": [cv_susp_pp(t) for t in ts],
            "cum_prem_pp": [cum_prem_pp(t) for t in ts],
            "refund_ratio": [refund_ratio(t) for t in ts],
            "loan_pp": [loan_pp(t) for t in ts],
        },
        index=pd.Index(ts, name="t"),                                # noqa: F821
    )


# ---------------------------------------------------------------------------
# References

data = ("Interface", ("..", "Data"), "auto")

point_id = 1

prem_int_rate = 0.025

min_guar_rate = 0.0075

prem_loading = 1.4642

surr_chg_prem_rate = 0.05

surr_chg_coef = 20

surr_chg_sa_rate = 0.01

surr_chg_prem_years = 20

surr_chg_max_years = 7

acq_cost_ratio = 1.0

acq_cost_tolerance = 1.4

comm_init_share = 0.65

comm_cap_rate = 1.0

comm_renewal_rate = 0.03

expense_maint_pp = 60000.0

expense_maint_prem_rate = 0.02

expense_claim_pp = 300000.0

inflation_rate = 0.02

loan_spread = 0.015

loan_limit = 0.8

lapse_bonus_spike = 0.3

roll_fwd_tol = 1e-10

val_tol = 1e-07

pd = ("Module", "pandas")
