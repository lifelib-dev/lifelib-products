# modelx: pseudo-python
# This file is part of a modelx model.
# It can be imported as a Python module, but functions defined herein
# are model formulas and may not be executable as standard Python.

"""Reference liability cash flow model for Korean whole life assurance (종신보험).

:mod:`~.WholeLife_KR_A` is the executable counterpart of
``products/whole_life/technical-notes.md`` in the ``krlib`` library. It projects gross
best-estimate liability cash flows for a single-policy model point of the standardized
composite 종신보험 (*jongsin boheom*) — a level premium payable for a stated 납입기간, a
사망보험금 level for life, no expiry date and no 만기보험금, and therefore a 계약자적립액
and a 해약환급금 that carry the whole economics of the product.

This is the library's **savings/protection chassis**. Five mechanics are specified once
here and inherited by ``CI_KR_A`` and ``Pension_KR_A``:

* the 계약자적립액 (*gyeyakja jeongnibaek*, the policyholder account) recursion, the
  contractual successor of the 보험료적립금 policy reserve;
* the 해약환급금 (*haeyak hwangeupgeum*, surrender value) and its 해약공제액, capped by
  the 표준해약공제액 of 보험업감독규정 별표 14;
* the **무해지환급형 / 저해지환급형** suppressed forms — the surrender value is a stated
  fraction ``k`` of the 표준형 twin's during 납입기간 and steps up to it at 납입완료. The
  suppression is a **model point column**, not a separate model, so the cliff and the
  ordinary curve appear side by side in one projection;
* the 보험계약대출 (policy loan) as a modelled state, unavailable during 납입기간 on a
  무해지환급형 contract because there is no value to lend against; and
* 보험료 납입면제 (premium waiver), a distinct in-force state in which premiums cease and
  are **deemed paid** for benefit and surrender-value purposes.

Three structural facts separate this model from its Japanese sister. There is **no
automatic premium loan**: no 자동대출납입 provision was found in any Korean document read
for this library, so lapse here is a behavioural decrement acting at the end of a 14-day
납입최고기간 rather than a funded event. There is **no severe-disability acceleration**;
the slot Japanese whole life fills with a 高度障害保険金 is filled in Korea by the premium
waiver, which continues the contract instead of extinguishing it. And there is **no
expiry**: the projection runs to the terminal age of the mortality table, every remaining
life dies in the final year, and nothing is paid at the horizon but the death benefit.

**Spaces.** The model contains two:

:mod:`~.WholeLife_KR_A.Data`
    Reads the three input CSVs and holds their filename References. It takes no
    parameters, so each file is read **once per model**.

:mod:`~.WholeLife_KR_A.Projection`
    The by-policy projection, parameterized by ``point_id``: ``Projection[1]`` is an
    ItemSpace projecting model point 1, the technical notes' worked-example anchor cell.
    It reaches the input tables through its ``data`` Reference, which resolves to the
    single :mod:`~.WholeLife_KR_A.Data` Space.

The split matters for more than tidiness. Because ``Projection`` is parameterized, every
``Projection[N]`` is a separate ItemSpace with its own cells cache; readers placed there
would re-read every file for every policy. In ``Data`` they are evaluated once, however
many policies are projected.

Input data is **external**: CSVs in the model folder's parent directory, read at run time
rather than stored inside the model. The model folder itself holds no data, so the model
and its inputs must travel together.

**Projection basis.** Annual steps on policy years running 계약해당일 to 계약해당일, on
**보험나이** (*boheom nai*, insurance age). 감독규정 제7-65조제2항 expressly permits the
계약자적립액 of a monthly-premium contract to be computed on an annualised premium basis —
「연납보험료를 기준으로 하여 산출할 수 있다」 — and that permission is what lets an annual
grid carry this product. Premium, maintenance expense and renewal commission fall at the
start of the policy year; acquisition expense and initial commission at issue; death
claims at the end of the year of death; surrenders and any 감액 at the end of the year,
after deaths.

**What is sourced and what is not.** The contractual mechanics are sourced: the level
whole-of-life benefit, the identity 해약환급금 = 계약자적립액 − 해약공제액, the
표준해약공제액 formula and the seven-year 해약공제기간 cap, the fact that the suppression
multiplies a **표준형 comparison twin priced with the lapse assumption switched off** and
is not sold, the equality of the suppressed and 표준형 values from 납입완료, the policy
loan rate formula 예정이율 + 1.5% and the 50%-장해지급률 waiver with premiums deemed paid.
The quantitative basis is not. The 예정이율, the 적용위험률 and the 예정사업비율 live in
the filed but unpublished 산출방법서, and the 제10회 경험생명표 is not published in full,
so the mortality table is a **[std]** construction and every expense parameter is a
**[std]** standardization bounded above by the 표준해약공제액. **This model is a mechanics
demonstration, not a pricing or reserving result.** Replace the assumption tables with
company data, and the account recursion with a real 산출방법서, before drawing any
conclusion from the output.

**What it does not compute.** No 책임준비금, no IFRS 17 CSM, no K-ICS 요구자본 and no
해약환급금준비금. ``result_cf()`` is a gross, undiscounted best-estimate stream and the
three Korean measurement bases that consume it are a separate layer.

**Model points.** Ten, covering both sexes, the issue-age envelope 30 to 65, sum assureds
from ₩10,000,000 to ₩1,000,000,000, the four suppression factors 1.00 / 0.50 / 0.30 /
0.00, payment terms of 7, 10, 20 and 30 years and 전기납, and each optional module: the
policy loan on a 저해지 and on a 무해지 contract, the premium waiver, the 단기납
유지보너스 with its mandatory lapse spike, the 금리연동형 crediting basis, 감액, 부활 and
the level lapse basis. Model point 1 is the anchor cell of the worked example in the
technical notes.

**Verification.** ``tests/test_whole_life_kr.py`` asserts the notes' worked example, the
exact ``1 / k`` step at 납입완료, the nil surrender value of the 무해지 form throughout
납입기간, the zero policy loan that follows from it, and every ``check_*`` identity on
every shipped model point.

Example:

    >>> import modelx as mx
    >>> model = mx.read_model("products/whole_life/WholeLife_KR_A")
    >>> model.Projection[1].result_cf()
"""

from modelx.serialize.jsonvalues import *

_name = "WholeLife_KR_A"

_allow_none = False

_spaces = [
    "Data",
    "Projection"
]
