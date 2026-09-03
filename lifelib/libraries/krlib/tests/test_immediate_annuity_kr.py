"""Golden and structural tests for Immediate_KR_A.

The golden values are the worked example in
products/immediate_annuity/technical-notes.md ("Worked example"), which projects the
anchor cell 남자 / 보험나이 60 / 일시납 ₩100,000,000 (1억원) / 종신연금형 with a ten-year
보증지급기간 on the ``decl_2017`` crediting basis — the cell that sits on the tax boundary
the product is designed around, the ₩100,000,000 being both the median of the only public
dataset and exactly the 소득세법 ten-year exemption cap.  They are hard-coded here rather
than pickled so that a reviewer can compare them against the notes by eye.

Tolerances follow the precision the notes display: money to the won's second decimal in the
tables and to a fraction of a won in the hand traces, in-force to six decimals, the survival
curve and the payment weight to the nine the notes print them at, mortality to eight, and
the annuity and accumulation factors to twelve.

This is the library's **payout-phase chassis**, so the module carries more than a cash-flow
comparison.  A single premium arrives at inception and an annuity is in payment thereafter,
so there is no premium term, no lapse machinery of the usual kind and — the structural
difference from every other model in ``krlib`` — **no acquisition strain after t = 0**.
Three shapes are model point columns of one projection and they are three different
liabilities, so the panels the notes print for each of them are asserted beside the anchor:

* points **6 and 7** are one 상속연금형 contract on the two readings of the 만기보험금
  지급재원, which is the **즉시연금 과소지급 분쟁** in a column — the retention that stood in
  the 산출방법서 and not in the 약관, ordered away by 금융분쟁조정위원회 조정결정
  제2017-17호 and restored by the Supreme Court in 2025 for the contracts before it;
* point **8** is the only shipped point whose crediting rate is not constant, so it is the
  one that exercises the 최저보증이율 stepping and the retention being re-struck each year;
* point **9** is the 확정기간연금형, which carries no mortality in its annuity at all and is
  therefore the sharpest available test of the expense load.

Each of the twenty-one product facts the notes list under **Known modeling pitfalls** earns
its own test, named after the pitfall and naming it again in its docstring, because each of
them is a way an implementation can look right and be wrong — beginning with the two the
whole shape turns on, that ``pols_if`` is the probability a **payment obligation remains**
rather than a survival probability, and that the 보증지급기간 is a ``max`` on that
obligation and never a second stream.

The eleven ``check_*`` cells this model publishes are asserted **by name**, because a
generic sweep cannot notice a check that has quietly disappeared, and the [std] parameters
the notes state are read off the model so that a silent change to an assumption fails a test
rather than moving a result.  That every check is *True* on every shipped model point is
``test_model_conventions_kr.py``'s single sweep and is not repeated here.
"""
import pandas as pd
import pytest
from modelx.core.errors import FormulaError

from kr_registry import LIB, MODELS

WON = 0.005          # money displayed to 2 d.p.
SUB_WON = 5e-7       # the hand traces' full-precision won amounts
INFORCE = 5e-7       # pols_if, displayed to 6 d.p.
PROB = 5e-10         # lives_if and payment_factor, displayed to 9 d.p.
RATE = 5e-9          # mort_rate, displayed to 8 d.p.
FACTOR = 5e-13       # annuity and accumulation factors, displayed to 12 d.p.
EXACT = 5e-13        # probabilities the notes print to 12 d.p.

MODEL_DIR = LIB / MODELS["Immediate_KR_A"][0]
CSV_DIR = MODEL_DIR.parent

# ---------------------------------------------------------------------------
# The notes' worked example, anchor cell (point_id = 1)

# "First periods of the base run": t -> (pols_if, premiums, annuity_payments,
# commissions, expenses, net_cf).  claims_death, claims_lapse and claims_maturity are
# 0.00 in every row of this model point and are asserted separately, as zeros.
WORKED_EXAMPLE_CF = {
    0:  (1.000000, 100000000.00, 4948039.16, 2000000.00, 1539584.31, 91512376.53),
    1:  (1.000000, 0.00, 4948039.16, 0.00, 39584.31, -4987623.47),
    2:  (1.000000, 0.00, 4948039.16, 0.00, 39584.31, -4987623.47),
    3:  (1.000000, 0.00, 4948039.16, 0.00, 39584.31, -4987623.47),
    4:  (1.000000, 0.00, 4948039.16, 0.00, 39584.31, -4987623.47),
    5:  (1.000000, 0.00, 4948039.16, 0.00, 39584.31, -4987623.47),
    6:  (1.000000, 0.00, 4948039.16, 0.00, 39584.31, -4987623.47),
    7:  (1.000000, 0.00, 4948039.16, 0.00, 39584.31, -4987623.47),
    8:  (1.000000, 0.00, 4948039.16, 0.00, 39584.31, -4987623.47),
    9:  (1.000000, 0.00, 4948039.16, 0.00, 39584.31, -4987623.47),
    10: (0.953470, 0.00, 4683461.38, 0.00, 37467.69, -4720929.08),
    11: (0.946529, 0.00, 4645610.42, 0.00, 37164.88, -4682775.30),
    12: (0.938879, 0.00, 4603712.54, 0.00, 36829.70, -4640542.24),
    20: (0.835652, 0.00, 4031289.14, 0.00, 32250.31, -4063539.46),
    25: (0.703150, 0.00, 3301327.71, 0.00, 26410.62, -3327738.33),
    27: (0.627749, 0.00, 2893663.24, 0.00, 23149.31, -2916812.54),
    28: (0.584810, 0.00, 2664690.24, 0.00, 21317.52, -2686007.76),
    30: (0.489248, 0.00, 2164694.60, 0.00, 17317.56, -2182012.16),
    40: (0.041492, 0.00, 121342.12, 0.00, 970.74, -122312.85),
    49: (0.000003, 0.00, 1.67, 0.00, 0.01, -1.68),
    50: (0.000000, 0.00, 0.00, 0.00, 0.00, 0.00),
}

# "The state behind those rows, from result_pols()":
# t -> (보험나이, mort_rate, lives_if, payment_factor, av_pp).  annuity_pp is
# 4,948,039.16 in every row and is asserted once, as the level it is.
WORKED_EXAMPLE_STATE = {
    0:  (60, 0.00353000, 1.000000000, 1.000000000, 96500000.00),
    1:  (61, 0.00369813, 0.996470000, 1.000000000, 93964460.84),
    2:  (62, 0.00389473, 0.992784928, 1.000000000, 91365533.21),
    3:  (63, 0.00412461, 0.988918303, 1.000000000, 88701632.38),
    4:  (64, 0.00439341, 0.984839401, 1.000000000, 85971134.03),
    5:  (65, 0.00470769, 0.980512602, 1.000000000, 83172373.23),
    6:  (66, 0.00507513, 0.975896656, 1.000000000, 80303643.40),
    7:  (67, 0.00550471, 0.970943851, 1.000000000, 77363195.33),
    8:  (68, 0.00600689, 0.965599088, 1.000000000, 74349236.06),
    9:  (69, 0.00659390, 0.959798841, 1.000000000, 71259927.80),
    10: (70, 0.00728000, 0.953470025, 0.946528763, 68093386.84),
    11: (71, 0.00808184, 0.946528763, 0.938879073, 64847682.35),
    12: (72, 0.00901881, 0.938879073, 0.930411501, 61520835.25),
    20: (80, 0.02504325, 0.835652028, 0.814724584, 31730520.38),
    25: (85, 0.05112774, 0.703149640, 0.667199188, 9891652.03),
    27: (87, 0.06840075, 0.627748566, 0.584810092, 372637.63),
    28: (88, 0.07912911, 0.584810092, 0.538534591, -4566085.59),
    30: (90, 0.10580035, 0.489247948, 0.437485342, -14817022.97),
    40: (100, 0.40896710, 0.041492230, 0.024523273, -74401813.77),
    49: (109, 0.88297585, 0.000002884, 0.000000338, -142173018.91),
    50: (110, 1.00000000, 0.000000338, 0.000000000, -150675383.54),
}

# "Derived quantities at inception, at the precision the model produces them", and the
# hand traces' intermediate values, at the precision the notes print them.
AV_PP_INIT = 96500000.0000000000
ANNUITY_FACTOR = 19.502675087912
FACTOR_GUARANTEED = 8.752063930971     # SUM t=0..9 v^(t+1), the annuity-certain half
FACTOR_TAIL = 10.750611156941          # SUM t=10..50 v^(t+1) l(t+1), the life half
ANNUITY_PP = 4948039.1569365682
PROJ_LEN = 50
EXPENSE_CHARGE = 39584.3132554925      # 0.80% of the 연금연액, at a weight of one
EXPENSES_0 = 1539584.3132554926
NET_CF_0 = 91512376.5298079401
NET_CF_1 = -4987623.4701920608
AV_PP_1 = 93964460.8430634141
AV_PP_1_CREDITED = 98912499.9999999851  # V(0) x 1.025, before the instalment
ANN_10 = 4683461.3842575438
EXPENSES_10 = 37467.6910740604
NET_CF_10 = -4720929.0753316041
POLS_IF_10 = 0.953470025140            # l(10): the obligation after the guarantee
PAYMENT_FACTOR_10 = 0.946528763357     # l(11): the first payment the guarantee misses
POLS_EXIT_9 = 0.046529974860           # the whole cohort that died inside the guarantee
AV_PP_27 = 372637.6262347791
AV_PP_28 = -4566085.5900459196
AV_PP_50 = -150675383.54
ANN_49 = 1.67                          # ₩1.67 on a weight of 0.000000337522
PAYMENT_FACTOR_49 = 0.000000337522

# "Undiscounted totals", over t = 0 … 50, per policy, income-positive.
TOTALS = {
    "pols_if": 28.875654,
    "premiums": 100000000.00,
    "annuity_payments": 138160059.32,
    "claims_death": 0.00,
    "claims_lapse": 0.00,
    "claims_maturity": 0.00,
    "commissions": 2000000.00,
    "expenses": 2605280.47,
    "liability_cf": 42765339.80,
    "net_cf": -42765339.80,
}
SUM_LIVES = 28.691418                  # Σ l(t) over t = 0 … 50
SUM_LIVES_GUARANTEE = 9.815764         # Σ l(t) over t = 0 … 9
GUARANTEE_YEARS_ADDED = 0.184236       # 10 − Σ l(t) inside the guarantee: 2.2 months
ACQ_EXPENSE_0 = 1500000.00             # the day-one acquisition and admin expense
ANNUITY_CHARGE_TOTAL = 1105280.47      # 0.0080 x the annuity total
CUM_ANNUITY_20 = 98007125.57           # below the premium at the end of row 20
CUM_ANNUITY_21 = 101922278.93          # above it at the end of row 21

# The readings of the factor the notes take, and the reconciliation to a 연금월액.
GROSS_FACTOR = 20.2100                 # P / A, against published 23.81 and 23.15 at 55
GROSS_PREMIUM_ANNUITY = 5127501.72     # P / ä, had the gross premium been converted
LOAD_FROM_THE_INCOME_SIDE = 0.0362694  # 3.63%: the 3.50% load grossed up by itself
FACTOR_NO_GUARANTEE = 19.309113
ANNUITY_NO_GUARANTEE = 4997640.34
GUARANTEE_COST = 0.009925              # 1.00% of income, for ten guaranteed years
E60_COMPLETE = 28.1914                 # complete e(60) on the shipped table
I_TWELVE = 0.024718035238              # i^(12) at 2.50%
I_OVER_I_TWELVE = 1.0114072482
ANNUITY_MONTHLY_NAIVE = 412336.60      # A / 12
ANNUITY_MONTHLY_TRUE = 407686.02       # the monthly-in-arrears annuity of equal value

# Pitfall 2: the additive construction, and what it would pay.
ADDITIVE_FACTOR = 28.061177
ADDITIVE_ANNUITY = 3438914.97
ADDITIVE_SHARE = 0.6950                # 69.50% of the right answer, for life

# Pitfall 5: reading q at the end of the period rather than the start.
WRONG_END_ANNUITY = 5060720.68
WRONG_END_UPLIFT = 0.0227730           # +2.28%

# ---------------------------------------------------------------------------
# The dispute panel — model points 6 and 7, one contract on two bases

AV_PP_INIT_LOADED = 95029999.9999999851   # P (1 − 0.0350 − 0.0147), the two other shapes
MATURITY_BENEFIT = 100000000.00           # 만기보험금 = the **gross** single premium
S_10_AT_250 = 11.203381767854             # s(10, 2.50%), the retention's denominator
DISC_10_AT_250 = 0.781198401726           # v(10) on the crediting path

# t = 0 hand trace, as designed (point 6) and as ordered (point 7).
DESIGNED = {
    "annuity_pp": 1932133.9470096088,
    "retention_pp": 443616.0529903907,
    "av_pp_1": 95473616.0529903620,
    "payment_factor": 0.996470000000,
    "annuity_payments": 1925313.5141766649,
    "pols_death": 0.003530000000,
    "claims_death": 372321.8646670560,
    "pols_lapse": 0.019929400000,
    "claims_lapse": 1902731.8837664661,
    "expenses": 1515402.5081134134,
    "net_cf": 92284230.2292763889,
}
ORDERED = {
    "annuity_pp": 2375749.9999999995,
    "retention_pp": 0.0,
    "av_pp_1": 95029999.9999999702,
    "payment_factor": 0.996470000000,
    "annuity_payments": 2367363.6024999996,
    "pols_death": 0.003530000000,
    "claims_death": 370755.8999999999,
    "pols_lapse": 0.019929400000,
    "claims_lapse": 1893890.8819999993,
    "expenses": 1518938.9088200000,
    "net_cf": 91849050.7066799849,
}

# "The two liabilities side by side", undiscounted totals.
DISPUTE_TOTALS = {
    6: {"annuity_payments": 17278079.84, "claims_death": 4540094.23,
        "claims_lapse": 15858445.72, "claims_maturity": 79495349.97,
        "expenses": 1638224.64, "net_cf": -20810194.4082},
    7: {"annuity_payments": 21245109.97, "claims_death": 4421328.16,
        "claims_lapse": 15485199.36, "claims_maturity": 79495349.97,
        "expenses": 1669960.88, "net_cf": -24316948.3440},
}
DISPUTE_NET_CF_DIFFERENCE = -3506753.9358
RETENTION_SHORTFALL = 3882556.0565768769
ANNUITY_UPLIFT_AS_ORDERED = 0.2296            # +22.96% of income on one boolean
DESIGNED_MONTHLY = (161011.16, 159195.18)     # A / 12, and the true monthly equivalent
ORDERED_MONTHLY = (197979.17, 195746.24)
RETENTION_PATH = [                            # R(t), t = 0 … 9, on point 6
    443616.05, 454706.45, 466074.12, 477725.97, 489669.12,
    501910.85, 514458.62, 527320.08, 540503.08, 554015.66,
]
MATURITY_EARLIER_WEIGHT = 80023013.57         # pitfall 18: IF(N) M instead of IF(N+1) M

# ---------------------------------------------------------------------------
# The floor-stepping panel — model point 8, 여자 70, 상속연금형 20년, min_guar

FLOOR_STEP = {
    0:  (0.0125, 967602.6635299305, 220272.3364700692, 95030000.00),
    4:  (0.0125, 967602.6635299291, 231494.1848643858, 95927747.87),
    5:  (0.0100, 722990.0183330460, 238602.4022310498, 96159242.06),
    9:  (0.0100, 722990.0183330459, 248290.6165572634, 97128063.49),
    10: (0.0075, 476691.5833813021, 253631.0724106092, 97376354.11),
    19: (0.0075, 476691.5833813062, 271273.8626488275, 99728726.14),
}
S_16_AT_125 = 17.591163816233
S_15_AT_100 = 16.096895537000
AV_PP_4_POINT_8 = 95927747.8715451956
AV_PP_5_POINT_8 = 96159242.0564095676
AV_PP_20_POINT_8 = 100000000.00
FIRST_STEP_FALL = -0.2528               # −25.28% on a −20.0% move in the rate
SECOND_STEP_FALL = -0.3407              # −34.07%
TWO_STEP_FALL = -0.5073                 # −50.73% from year 1 to year 11
FLOOR_MONTHLY = (80633.56, 39724.30)

# ---------------------------------------------------------------------------
# The load cross-check — model point 9, 확정기간연금형 10년

A_10_AT_250 = 8.752063930971
CERTAIN_ANNUITY = 10858010.2647236791
CERTAIN_MONTHLY_NAIVE = 904834.19
CERTAIN_MONTHLY_TRUE = 894628.93        # against 교보's published 90만원 on 2.52%
CERTAIN_LAST_INSTALMENT = 9052841.76    # 9.1% of the annuity total: pitfall 4's cost
CERTAIN_TOTALS = {
    "annuity_payments": 99311267.03,
    "claims_death": 420958.60,
    "claims_lapse": 8468964.56,
    "expenses": 2294490.14,
    "net_cf": -12495680.32,
}

# ---------------------------------------------------------------------------
# The eleven check cells this model publishes, and the six that carry a residual

CHECKS = {
    "check_annuity_basis",
    "check_av_roll_fwd",
    "check_av_terminal",
    "check_guarantee_certain",
    "check_lives_roll_fwd",
    "check_net_cf",
    "check_payment_factor",
    "check_pols_roll_fwd",
    "check_premium_split",
    "check_rate_level",
    "check_surr_value",
}
CHECKS_WITH_RESID = {
    "check_annuity_basis",     # the only residual taking no argument: it is one number
    "check_av_roll_fwd",
    "check_lives_roll_fwd",
    "check_net_cf",
    "check_payment_factor",
    "check_pols_roll_fwd",
}

# The charge basis, by shape, every rate of it [std] in its adoption or its derivation.
CHARGE_RATES = {
    "life": {"acq_charge_rate": 0.0220, "admin_charge_rate": 0.0130,
             "risk_prem_rate": 0.0000, "comm_rate": 0.0200,
             "acq_expense_rate": 0.0150, "annuity_charge_rate": 0.0080,
             "db_rate": 0.00},
    "inheritance": {"acq_charge_rate": 0.0220, "admin_charge_rate": 0.0130,
                    "risk_prem_rate": 0.0147, "comm_rate": 0.0200,
                    "acq_expense_rate": 0.0150, "annuity_charge_rate": 0.0080,
                    "db_rate": 0.10},
    "certain": {"acq_charge_rate": 0.0220, "admin_charge_rate": 0.0130,
                "risk_prem_rate": 0.0147, "comm_rate": 0.0200,
                "acq_expense_rate": 0.0150, "annuity_charge_rate": 0.0080,
                "db_rate": 0.10},
}

# The 최저보증이율 schedule, by the completed policy year the band contains.
MIN_GUAR_SCHEDULE = {0: 0.0125, 4: 0.0125, 5: 0.0100, 9: 0.0100, 10: 0.0075, 30: 0.0075}
DECL_RATE = 0.0250
OMEGA_AGE = 110

# "The ten shipped model points": point_id -> proj_len(), the notes' own column.
SHIPPED_HORIZONS = {1: 50, 2: 50, 3: 50, 4: 65, 5: 30,
                    6: 9, 7: 9, 8: 19, 9: 9, 10: 29}

# The two published 개인연금사망률 the construction reproduces exactly, per sex.
SOURCED_MORT_ANCHORS = {("M", 60): 0.00353, ("M", 70): 0.00728,
                        ("F", 60): 0.00118, ("F", 70): 0.00251}


def _true_monthly(annual, rate=0.025):
    """The monthly-in-arrears annuity of the same present value as an annual one.

    ``A / 12 x i^(12) / i``.  The notes make every comparison with a carrier's published
    연금월액 on this figure rather than on ``A / 12``, because the within-year interest the
    monthly mode pays and the annual mode does not is worth 1.14% at 2.50%.
    """
    i12 = 12.0 * ((1.0 + rate) ** (1.0 / 12.0) - 1.0)
    return annual / 12.0 * (i12 / rate)


# ---------------------------------------------------------------------------
# The worked example — the quantities struck at inception


def test_worked_example_inception_quantities(kr_immediate_anchor):
    """V(0), ä, A(0), B, M and N, at the precision the notes produce them.

    Everything else on the anchor cell is a function of these six numbers and of the
    mortality table, so an error in any of them moves every row of the statement.  ``N`` is
    ω − x = 110 − 60 and is a **last row index**, which is the pitfall the notes list
    fourth.
    """
    a = kr_immediate_anchor
    assert a.av_pp_init() == pytest.approx(AV_PP_INIT, abs=SUB_WON)
    assert a.av_pp_init() == pytest.approx(
        a.prem_pp() * (1.0 - 0.0350 - 0.0000), rel=1e-15)
    assert a.annuity_factor() == pytest.approx(ANNUITY_FACTOR, abs=FACTOR)
    assert a.annuity_pp(0) == pytest.approx(ANNUITY_PP, abs=SUB_WON)
    assert a.annuity_pp(0) == pytest.approx(
        a.av_pp_init() / a.annuity_factor(), rel=1e-15)
    assert a.risk_prem_pp() == 0.0
    assert a.maturity_benefit() == 0.0
    assert a.retention_shortfall_pp() == 0.0
    assert a.proj_len() == PROJ_LEN == OMEGA_AGE - a.age_at_entry()
    assert len(a.result_cf()) == PROJ_LEN + 1 == 51


def test_worked_example_annuity_factor_decomposition(kr_immediate_anchor):
    """ä(60, 10, 2.5%) = 8.752063930971 + 10.750611156941, and only the second half reads.

    The factor is the one quantity in the notes a reader cannot check by inspection, so it
    is decomposed there and asserted here.  The first sum is exactly the annuity-certain
    ``a(10, 2.50%)``, because inside the guarantee the weight is one whatever the annuitant
    does; 44.9% of the factor is that certain block and 55.1% is the life-contingent tail.
    """
    a = kr_immediate_anchor
    i = a.crediting_rate(0)
    v = 1.0 / (1.0 + i)
    guaranteed = sum(v ** (t + 1) * a.pricing_factor(t) for t in range(0, 10))
    tail = sum(v ** (t + 1) * a.pricing_factor(t) for t in range(10, a.proj_len() + 1))
    assert guaranteed == pytest.approx(FACTOR_GUARANTEED, abs=FACTOR)
    assert guaranteed == pytest.approx(a.annuity_factor_certain(10, i), abs=FACTOR)
    assert tail == pytest.approx(FACTOR_TAIL, abs=FACTOR)
    assert guaranteed + tail == pytest.approx(a.annuity_factor(), rel=1e-14)
    assert guaranteed / a.annuity_factor() == pytest.approx(0.449, abs=5e-4)
    assert tail / a.annuity_factor() == pytest.approx(0.551, abs=5e-4)
    # Only the tail reads the mortality table: inside the guarantee the weight is one.
    assert all(a.pricing_factor(t) == 1.0 for t in range(0, 10))
    assert all(a.pricing_factor(t) < 1.0 for t in range(10, a.proj_len() + 1))


def test_worked_example_the_three_readings_of_the_factor(kr_immediate_anchor):
    """The gross factor of 20.2100, the 3.63% load and the 1.00% the guarantee costs.

    Three sanity checks the notes take on a number that cannot be compared with a published
    one, no carrier publishing an annuity factor.  The premium divided by the annual annuity
    sits where a 남자 60 cell should, against implied factors of 23.81 and 23.15 at 55;
    converting the **gross** premium rather than the fund would raise the annuity by 3.63%,
    the 3.50% load grossed up by itself; and the same fund with no 보증지급기간 at all buys
    ₩4,997,640.34 instead of ₩4,948,039.16, so ten guaranteed years cost **1.00% of income**
    — the quantitative reason 97.3% of life-shape buyers take them.  Ten years also sits far
    inside the complete ``e(60)`` of 28.1914 on the shipped table, the 소득세법 시행령
    제25조제4항제3호 test a tax-exempt 종신형 must clear.
    """
    a = kr_immediate_anchor
    assert a.prem_pp() / a.annuity_pp(0) == pytest.approx(GROSS_FACTOR, abs=5e-5)
    gross = a.prem_pp() / a.annuity_factor()
    assert gross == pytest.approx(GROSS_PREMIUM_ANNUITY, abs=WON)
    assert gross / a.annuity_pp(0) - 1.0 == pytest.approx(
        LOAD_FROM_THE_INCOME_SIDE, abs=5e-7)
    assert gross / a.annuity_pp(0) - 1.0 == pytest.approx(
        0.0350 / (1.0 - 0.0350), rel=1e-12)
    v = 1.0 / (1.0 + a.crediting_rate(0))
    no_guarantee = sum(v ** (t + 1) * a.lives_if(t + 1)
                       for t in range(0, a.proj_len() + 1))
    assert no_guarantee == pytest.approx(FACTOR_NO_GUARANTEE, abs=5e-7)
    assert a.av_pp_init() / no_guarantee == pytest.approx(ANNUITY_NO_GUARANTEE, abs=WON)
    assert 1.0 - a.annuity_pp(0) / (a.av_pp_init() / no_guarantee) == pytest.approx(
        GUARANTEE_COST, abs=5e-6)
    complete = sum(a.lives_if(t) for t in range(1, a.proj_len() + 2)) + 0.5
    assert complete == pytest.approx(E60_COMPLETE, abs=5e-5)
    assert a.annuity_term() < complete


def test_worked_example_monthly_reconciliation(kr_immediate_anchor):
    """₩412,336.60 a month naively, ₩407,686.02 on the ``i / i^(12)`` adjustment.

    The whole of the annual-grid reconciliation: the market default is a monthly 연금월액,
    the 1.14% between the two figures is the within-year interest the monthly mode pays and
    the annual mode does not, and it is exactly the 「신공시이율로 계산한 이자를
    가산합니다」 of the two carriers who state it.  Every comparison the documents make with
    a published 연금월액 is made on the adjusted figure, so the adjustment is asserted here
    rather than left in prose.
    """
    a = kr_immediate_anchor
    i = a.crediting_rate(0)
    i12 = 12.0 * ((1.0 + i) ** (1.0 / 12.0) - 1.0)
    assert i12 == pytest.approx(I_TWELVE, abs=5e-13)
    assert i / i12 == pytest.approx(I_OVER_I_TWELVE, abs=5e-11)
    assert a.annuity_pp(0) / 12.0 == pytest.approx(ANNUITY_MONTHLY_NAIVE, abs=WON)
    assert _true_monthly(a.annuity_pp(0)) == pytest.approx(ANNUITY_MONTHLY_TRUE, abs=WON)
    # The adjustment is worth 1.14% of the annuity's timing value and no more.
    assert a.annuity_pp(0) / 12.0 / _true_monthly(a.annuity_pp(0)) == pytest.approx(
        I_OVER_I_TWELVE, abs=5e-10)


def test_worked_example_assumption_table(kr_immediate_anchor):
    """The notes' "assumption values used, in full, with tags", read off the model.

    Every quantitative parameter of the anchor cell in one place, so that a change to any
    of them fails a test rather than moving a result.  Three of the rows are contractual and
    the rest are [std] in their adoption; which is which is in the notes and in the CSVs'
    ``provenance`` columns, not here.
    """
    a = kr_immediate_anchor
    assert a.acq_charge_rate() == 0.0220
    assert a.admin_charge_rate() == 0.0130
    assert a.expense_load_rate() == pytest.approx(0.0350, rel=1e-15)
    assert a.risk_prem_rate() == 0.0000
    assert a.comm_rate() == 0.0200
    assert a.acq_expense_rate() == 0.0150
    assert a.annuity_charge_rate() == 0.0080
    assert a.db_rate() == 0.00
    assert a.decl_rate() == DECL_RATE
    assert [a.min_guar_rate(t) for t in (0, 4, 5, 9, 10, 50)] == [
        0.0125, 0.0125, 0.0100, 0.0100, 0.0075, 0.0075]
    assert all(a.crediting_rate(t) == DECL_RATE for t in range(0, a.proj_len() + 1))
    assert a.mort_rate(0) == 0.00353 and a.mort_rate(10) == 0.00728
    assert all(a.lapse_rate(t) == 0.0 for t in range(0, a.proj_len() + 1))
    assert a.shape() == "life" and a.sex() == "M" and a.age_at_entry() == 60
    assert a.prem_pp() == 100000000.0 and a.annuity_term() == 10
    assert a.crediting_basis() == "decl_2017" and a.pols_if_init() == 1.0


# ---------------------------------------------------------------------------
# The worked example — the cash flow statement and the state behind it


@pytest.mark.parametrize("t", sorted(WORKED_EXAMPLE_CF))
def test_worked_example_cash_flow_row(kr_immediate_anchor, t):
    """Every cell of the notes' twenty-one-row cash flow table, to the displayed precision.

    Asserted against the cells **and** against the published ``result_cf()`` row, because a
    column that dropped out of the frame would leave the cells intact and the statement
    wrong — and the statement is what a reader of the notes is holding.
    """
    pols, prem, ann, comm, exp, net = WORKED_EXAMPLE_CF[t]
    a = kr_immediate_anchor
    assert a.pols_if(t) == pytest.approx(pols, abs=INFORCE)
    assert a.premiums(t) == pytest.approx(prem, abs=WON)
    assert a.annuity_payments(t) == pytest.approx(ann, abs=WON)
    assert a.commissions(t) == pytest.approx(comm, abs=WON)
    assert a.expenses(t) == pytest.approx(exp, abs=WON)
    assert a.net_cf(t) == pytest.approx(net, abs=WON)
    row = a.result_cf().loc[t]
    assert row["pols_if"] == pytest.approx(pols, abs=INFORCE)
    assert row["premiums"] == pytest.approx(prem, abs=WON)
    assert row["annuity_payments"] == pytest.approx(ann, abs=WON)
    assert row["commissions"] == pytest.approx(comm, abs=WON)
    assert row["expenses"] == pytest.approx(exp, abs=WON)
    assert row["net_cf"] == pytest.approx(net, abs=WON)
    assert row["liability_cf"] == pytest.approx(-net, abs=WON)


@pytest.mark.parametrize("t", sorted(WORKED_EXAMPLE_STATE))
def test_worked_example_state_row(kr_immediate_anchor, t):
    """Every cell of the notes' state table from ``result_pols()``, at its own precision.

    The attained 보험나이, the 개인연금사망률 at it, the survival probability, the payment
    weight and the 계약자적립액 — the five quantities the cash flow rows are built out of.
    The annuity is level at ₩4,948,039.16 in every row and is asserted as the level it is.
    """
    age, q, lives, weight, av = WORKED_EXAMPLE_STATE[t]
    a = kr_immediate_anchor
    assert a.age(t) == age == a.age_at_entry() + t
    assert a.mort_rate(t) == pytest.approx(q, abs=RATE)
    assert a.lives_if(t) == pytest.approx(lives, abs=PROB)
    assert a.payment_factor(t) == pytest.approx(weight, abs=PROB)
    assert a.av_pp(t) == pytest.approx(av, abs=WON)
    assert a.annuity_pp(t) == pytest.approx(ANNUITY_PP, abs=SUB_WON)
    row = a.result_pols().loc[t]
    assert row["lives_if"] == pytest.approx(lives, abs=PROB)
    assert row["payment_factor"] == pytest.approx(weight, abs=PROB)
    assert row["av_pp"] == pytest.approx(av, abs=WON)
    assert row["cv_pp"] == 0.0                 # nil at every t, and omitted from the notes
    assert row["surr_if"] == 1.0               # surrender is contractually impossible
    assert row["crediting_rate"] == DECL_RATE


def test_the_three_claims_columns_are_zero_at_every_t(kr_immediate_anchor):
    """claims_death, claims_lapse and claims_maturity are 0.00 in every row, as columns.

    Each zero is a product fact — no death benefit after annuitisation, no surrender at all,
    no maturity on a 종신연금형 — and each is published as a column all the same, because a
    statement whose columns appear and disappear with the model point cannot be compared
    across model points.  The notes omit them from the printed table and say so; omitting
    them from the *frame* would be a different statement.
    """
    a = kr_immediate_anchor
    df = a.result_cf()
    for column in ("claims_death", "claims_lapse", "claims_maturity"):
        assert column in df.columns
        assert (df[column] == 0.0).all(), column
    assert all(a.claims(t, "DEATH") == 0.0 for t in range(0, a.proj_len() + 1))
    assert all(a.claims(t, "LAPSE") == 0.0 for t in range(0, a.proj_len() + 1))
    assert all(a.claims(t, "MATURITY") == 0.0 for t in range(0, a.proj_len() + 1))


# ---------------------------------------------------------------------------
# The worked example — the hand traces


def test_worked_example_period_zero_trace(kr_immediate_anchor):
    """The notes' period-0 trace, line by line, at full precision.

    V(0) = P(1 − c − b); ä decomposed; A(0) = V(0)/ä; F(0) = max(l(1), 1{1 ≤ 10}) = 1;
    ANN(0) = A(0); COM(0) = 0.0200 P; EXP(0) = 0.0150 P + 0.0080 A(0); and net_cf(0) =
    +₩91,512,376.53, the only positive row in the statement.  **The premium split reads
    straight off this line**: ₩2,000,000 of commission and ₩1,500,000 of expense sum to the
    ₩3,500,000 deducted from the premium to make V(0), with nothing left over in either
    direction, which is what "no acquisition strain" means arithmetically.
    """
    a = kr_immediate_anchor
    assert a.av_pp_init() == pytest.approx(AV_PP_INIT, abs=SUB_WON)
    assert a.annuity_factor() == pytest.approx(
        FACTOR_GUARANTEED + FACTOR_TAIL, abs=FACTOR)
    assert a.annuity_pp(0) == pytest.approx(ANNUITY_PP, abs=SUB_WON)
    assert a.payment_factor(0) == pytest.approx(1.0, abs=EXACT)
    assert a.payment_factor(0) == max(a.lives_if(1), 1.0)
    assert a.lives_if(1) == pytest.approx(0.996470000000, abs=EXACT)
    assert a.annuity_payments(0) == pytest.approx(ANNUITY_PP, abs=SUB_WON)
    assert a.premiums(0) == 100000000.0
    assert a.commissions(0) == pytest.approx(2000000.0, abs=SUB_WON)
    assert a.expenses(0) == pytest.approx(EXPENSES_0, abs=SUB_WON)
    assert a.expenses(0) - ACQ_EXPENSE_0 == pytest.approx(EXPENSE_CHARGE, abs=SUB_WON)
    assert a.net_cf(0) == pytest.approx(NET_CF_0, abs=SUB_WON)
    assert a.net_cf(0) == pytest.approx(
        100000000.0 - ANNUITY_PP - 2000000.0 - EXPENSES_0, abs=SUB_WON)
    # The split, read off the same line.
    assert a.check_premium_split() is True
    assert (a.commissions(0) + ACQ_EXPENSE_0 + a.risk_prem_pp()
            + a.av_pp_init()) == pytest.approx(a.prem_pp(), abs=SUB_WON)
    assert a.commissions(0) + ACQ_EXPENSE_0 == pytest.approx(
        a.expense_load_rate() * a.prem_pp(), abs=SUB_WON)


def test_worked_example_period_one_trace(kr_immediate_anchor):
    """The notes' period-1 trace: the recursion runs, and the annuity does not move.

    V(1) = V(0)(1 + i) − A(0) = 98,912,499.99999999 − 4,948,039.1569365682; l(1) = 1 − q(60);
    F(1) is again one, the guarantee covering the payment at time 2; and A(1) is A(0),
    struck once at commencement against 「연금개시시의 계약자적립액」.  **The fund is falling
    by ₩2.5m a year and has no contractual role at all on this shape.**  Rows 1 to 9 are
    this row repeated to the last digit.
    """
    a = kr_immediate_anchor
    assert a.av_pp(0) * (1.0 + a.crediting_rate(0)) == pytest.approx(
        AV_PP_1_CREDITED, abs=SUB_WON)
    assert a.av_pp(1) == pytest.approx(AV_PP_1, abs=SUB_WON)
    assert a.av_pp(1) == pytest.approx(
        a.av_pp(0) * 1.025 - a.annuity_pp(0), rel=1e-15)
    assert a.lives_if(1) == pytest.approx(1.0 * (1.0 - 0.00353), rel=1e-15)
    assert a.payment_factor(1) == pytest.approx(1.0, abs=EXACT)
    assert a.annuity_pp(1) == a.annuity_pp(0)
    assert a.annuity_payments(1) == pytest.approx(ANNUITY_PP, abs=SUB_WON)
    assert a.expenses(1) == pytest.approx(EXPENSE_CHARGE, abs=SUB_WON)
    assert a.net_cf(1) == pytest.approx(NET_CF_1, abs=SUB_WON)
    # Rows 1 to 9 are identical, and the fund alone moves.
    assert all(a.net_cf(t) == pytest.approx(NET_CF_1, abs=SUB_WON) for t in range(1, 10))
    assert 2.5e6 < a.av_pp(1) - a.av_pp(2) < 2.7e6      # "roughly 2.5m a year"
    assert all(a.av_pp(t) > a.av_pp(t + 1) for t in range(0, 10))


def test_worked_example_period_ten_guarantee_cliff_trace(kr_immediate_anchor):
    """The notes' period-10 trace: **two different things step, to two different numbers**.

    IF steps from 1.000000 to l(10) = 0.953470025140 — everyone who died in the first ten
    years leaves the obligation at once, and ``pols_exit(9)`` is that whole cohort,
    0.046529974860, in a single period.  The payment weight steps to l(11) = 0.946528763357,
    because the payment on row 10 falls at time 11 and is the first one the guarantee does
    not cover.  The cash flow falls 5.35% between rows 9 and 10 and a further 0.81% between
    rows 10 and 11: the first step is the guarantee expiring, the second is one year of
    mortality.
    """
    a = kr_immediate_anchor
    assert a.pols_if(9) == pytest.approx(1.0, abs=EXACT)
    assert a.pols_if(10) == pytest.approx(POLS_IF_10, abs=EXACT)
    assert a.pols_if(10) == a.lives_if(10)
    assert a.pols_exit(9) == pytest.approx(POLS_EXIT_9, abs=EXACT)
    assert a.pols_exit(9) == pytest.approx(
        a.pols_if_init() - a.lives_if(10), rel=1e-14)
    assert a.pols_if(9) - a.pols_exit(9) - a.pols_if(10) == pytest.approx(0.0, abs=1e-14)
    assert a.payment_factor(10) == pytest.approx(PAYMENT_FACTOR_10, abs=EXACT)
    assert a.payment_factor(10) == a.lives_if(11)
    assert a.pols_if(10) != a.payment_factor(10)
    assert a.annuity_payments(10) == pytest.approx(ANN_10, abs=SUB_WON)
    assert a.expenses(10) == pytest.approx(EXPENSES_10, abs=SUB_WON)
    assert a.net_cf(10) == pytest.approx(NET_CF_10, abs=SUB_WON)
    assert a.net_cf(10) / a.net_cf(9) - 1.0 == pytest.approx(-0.0535, abs=5e-5)
    assert a.net_cf(11) / a.net_cf(10) - 1.0 == pytest.approx(-0.0081, abs=5e-5)


def test_worked_example_the_tail_and_the_fund_that_goes_negative(kr_immediate_anchor):
    """The 계약자적립액 crosses zero between t = 27 and t = 28, and that is not a defect.

    V(27) = ₩372,637.63 and V(28) = 372,637.63 × 1.025 − 4,948,039.16 = −₩4,566,085.59,
    falling to −₩150,675,383.54 at t = 50.  A life annuity's fund is not its reserve: the
    annuitant still alive at 88 is being paid out of the mortality of the cohort he was
    priced with.  At the far end ``lives_if(51)`` is exactly zero because q(110) = 1, so row
    50 carries no payment at all and the obligation is **exhausted rather than truncated**;
    row 49 pays ₩1.67 on a weight of 0.000000337522.
    """
    a = kr_immediate_anchor
    assert a.av_pp(27) == pytest.approx(AV_PP_27, abs=SUB_WON)
    assert a.av_pp(28) == pytest.approx(AV_PP_28, abs=SUB_WON)
    assert a.av_pp(27) > 0.0 > a.av_pp(28)
    assert a.av_pp(28) == pytest.approx(
        a.av_pp(27) * 1.025 - a.annuity_pp(27), rel=1e-14)
    assert a.av_pp(50) == pytest.approx(AV_PP_50, abs=WON)
    assert a.cv_pp(28) == 0.0                       # nothing can be paid out of it
    assert a.mort_rate(50) == 1.0
    assert a.lives_if(51) == 0.0
    assert a.payment_factor(49) == pytest.approx(PAYMENT_FACTOR_49, abs=5e-13)
    assert a.annuity_payments(49) == pytest.approx(ANN_49, abs=WON)
    assert a.payment_factor(50) == 0.0
    assert a.annuity_payments(50) == 0.0
    assert a.net_cf(50) == 0.0
    assert a.check_av_roll_fwd() is True            # the closed form holds past t = 28
    assert a.check_av_terminal() is True            # True on this shape by design


# ---------------------------------------------------------------------------
# The worked example — totals and the shape of the result


def test_worked_example_undiscounted_totals(kr_immediate_anchor):
    """The notes' undiscounted totals over t = 0 … 50, column by column.

    ₩138.2m of annuity outgo against ₩100m of premium, ₩2.6m of expense and
    **−₩42,765,339.80** of net cash flow.  Undiscounted the contract loses money and must:
    the insurer receives the premium at time 0 and pays out over half a century, and the
    sign becomes meaningful only when the stream is discounted, which this library does not
    do.
    """
    df = kr_immediate_anchor.result_cf()
    for column, total in TOTALS.items():
        tol = 5e-7 if column == "pols_if" else WON
        assert df[column].sum() == pytest.approx(total, abs=tol), column
    assert df["liability_cf"].sum() == pytest.approx(-df["net_cf"].sum(), rel=1e-15)
    assert df["annuity_payments"].sum() / df["premiums"].sum() == pytest.approx(
        1.3816, abs=5e-5)


def test_worked_example_the_obligation_years_decompose(kr_immediate_anchor):
    """Σ IF(t) = 28.875654 = Σ l(t) + (10 − Σ l(t) inside the guarantee).

    The expected number of years the payment obligation stays open, and it decomposes
    exactly: 28.691418 of survival plus 0.184236 of guarantee.  **The ten-year guarantee
    extends the obligation by 2.2 months in expectation** on a 60-year-old male — a cheap
    option, which the market buys almost universally, and the arithmetic behind the 1.00% of
    income it costs.
    """
    a = kr_immediate_anchor
    ts = range(0, a.proj_len() + 1)
    obligation = sum(a.pols_if(t) for t in ts)
    survival = sum(a.lives_if(t) for t in ts)
    inside = sum(a.lives_if(t) for t in range(0, a.annuity_term()))
    assert obligation == pytest.approx(TOTALS["pols_if"], abs=5e-7)
    assert survival == pytest.approx(SUM_LIVES, abs=5e-7)
    assert inside == pytest.approx(SUM_LIVES_GUARANTEE, abs=5e-7)
    added = a.annuity_term() * a.pols_if_init() - inside
    assert added == pytest.approx(GUARANTEE_YEARS_ADDED, abs=5e-7)
    assert obligation == pytest.approx(survival + added, abs=5e-9)
    assert added * 12.0 == pytest.approx(2.2, abs=0.05)      # 2.2 months


def test_worked_example_the_expense_total_and_the_break_even(kr_immediate_anchor):
    """₩2,605,280.47 = ₩1,500,000 + ₩1,105,280.47, and break-even at the 21st instalment.

    The second expense term is exactly 0.0080 × the annuity total, because the
    연금수령기간 중 비용 is measured on the 연금연액 and carried at the payment's own weight
    rather than per policy in force, and **no other expense exists in this projection** —
    there is no maintenance expense and no inflation, the only recurring charge any retrieved
    즉시연금 document publishes being this one.  The cumulative payments cross the premium
    between rows 20 and 21, at attained age 81: the number a Korean buyer's own arithmetic
    produces, and the reason the shape is understood as a longevity hedge.
    """
    a = kr_immediate_anchor
    df = a.result_cf()
    total = df["expenses"].sum()
    assert total == pytest.approx(TOTALS["expenses"], abs=WON)
    assert total - ACQ_EXPENSE_0 == pytest.approx(ANNUITY_CHARGE_TOTAL, abs=WON)
    assert total - ACQ_EXPENSE_0 == pytest.approx(
        0.0080 * df["annuity_payments"].sum(), rel=1e-12)
    assert total / df["annuity_payments"].sum() == pytest.approx(0.019, abs=5e-4)
    for absent in ("expense_maint", "inflation_factor", "inflation_rate"):
        assert absent not in set(a.cells), f"{absent}: no maintenance expense here"
    cum20 = sum(a.annuity_payments(t) for t in range(0, 21))
    cum21 = sum(a.annuity_payments(t) for t in range(0, 22))
    assert cum20 == pytest.approx(CUM_ANNUITY_20, abs=WON)
    assert cum21 == pytest.approx(CUM_ANNUITY_21, abs=WON)
    assert cum20 < a.prem_pp() < cum21 and a.age(21) == 81


def test_worked_example_reading_the_shape_of_the_result(kr_immediate_anchor):
    """Three regions: one positive row, nine identical rows, then a decaying tail.

    Row 0 is almost the whole of the insurer's cash and there is never another positive row;
    rows 1 to 9 are a flat annuity-certain, identical to the last digit, because the
    guarantee makes survival irrelevant and the level rate makes the annuity level; rows 10
    onward are the same 연금연액 weighted by a survival probability falling from 0.9465 to
    0.0000003.  The liability is front-loaded in *certainty* and back-loaded in *duration*,
    which is the risk profile that makes longevity and not interest the dominant model risk.
    """
    a = kr_immediate_anchor
    assert a.net_cf(0) > 0.0
    assert all(a.net_cf(t) < 0.0 for t in range(1, a.proj_len()))
    assert a.net_cf(50) == 0.0
    assert len({round(a.net_cf(t), 6) for t in range(1, 10)}) == 1
    tail = [a.payment_factor(t) for t in range(10, a.proj_len() + 1)]
    assert tail == sorted(tail, reverse=True) and tail[-1] == 0.0
    assert tail[0] == pytest.approx(PAYMENT_FACTOR_10, abs=PROB)
    guaranteed = sum(a.annuity_payments(t) for t in range(0, 10))
    assert guaranteed / TOTALS["annuity_payments"] == pytest.approx(0.358, abs=5e-4)


# ---------------------------------------------------------------------------
# The dispute panel — 즉시연금 과소지급 분쟁, model points 6 and 7


def test_the_dispute_panel_is_one_contract_on_two_bases(immediate_annuity):
    """Points 6 and 7 differ in one column, ``retention_basis``, and in nothing else.

    That is what makes the difference between their cash flow statements the quantity that
    was litigated from 2017 to 2025, rather than a comparison of two products.  Both open at
    V(0) = P(1 − 0.0350 − 0.0147) and both carry a 만기보험금 of the **gross** premium, which
    is the whole mechanic of the retention: the fund opens below the benefit it must reach.
    """
    designed, ordered = immediate_annuity.Projection[6], immediate_annuity.Projection[7]
    table = immediate_annuity.Data.model_point_table()
    differing = [c for c in table.columns
                 if str(table.loc[6, c]) != str(table.loc[7, c]) and c != "policy_id"]
    assert differing == ["retention_basis"]
    assert designed.retention_basis() == "as_designed"
    assert ordered.retention_basis() == "as_ordered"
    for p in (designed, ordered):
        assert p.shape() == "inheritance"
        assert p.av_pp_init() == pytest.approx(AV_PP_INIT_LOADED, abs=SUB_WON)
        assert p.av_pp_init() == pytest.approx(
            p.prem_pp() * (1.0 - 0.0350 - 0.0147), rel=1e-15)
        assert p.maturity_benefit() == MATURITY_BENEFIT == p.prem_pp()
        assert p.maturity_benefit() > p.av_pp_init()
        assert p.proj_len() == 9
        assert p.accum_factor(10, 0.025) == pytest.approx(S_10_AT_250, abs=FACTOR)


def test_the_dispute_panel_period_zero_trace_as_designed(immediate_annuity):
    """The notes' period-0 trace on point 6, line by line, at full precision.

    R(0) = (M − V(0)) / s(10, 2.5%) = ₩443,616.05; A(0) = V(0) i − R(0) = ₩1,932,133.9470;
    the annuity is weighted by survival to the payment date; the 사망보험금 is
    0.00353 × (0.10 P + V(1)); the surrender is taken after the deaths, so its weight carries
    a (1 − q); and net_cf(0) = +₩92,284,230.23.
    """
    p = immediate_annuity.Projection[6]
    assert p.retention_pp(0) == pytest.approx(DESIGNED["retention_pp"], abs=SUB_WON)
    assert p.retention_pp(0) == pytest.approx(
        (p.maturity_benefit() - p.av_pp(0)) / p.accum_factor(10, 0.025), rel=1e-14)
    assert p.annuity_pp(0) == pytest.approx(DESIGNED["annuity_pp"], abs=SUB_WON)
    assert p.annuity_pp(0) == pytest.approx(
        p.av_pp(0) * 0.025 - p.retention_pp(0), rel=1e-14)
    assert p.payment_factor(0) == pytest.approx(DESIGNED["payment_factor"], abs=EXACT)
    assert p.annuity_payments(0) == pytest.approx(
        DESIGNED["annuity_payments"], abs=SUB_WON)
    assert p.av_pp(1) == pytest.approx(DESIGNED["av_pp_1"], abs=SUB_WON)
    assert p.pols_death(0) == pytest.approx(DESIGNED["pols_death"], abs=EXACT)
    assert p.claims(0, "DEATH") == pytest.approx(DESIGNED["claims_death"], abs=SUB_WON)
    assert p.claims(0, "DEATH") == pytest.approx(
        p.pols_death(0) * (0.10 * p.prem_pp() + p.av_pp(1)), rel=1e-14)
    assert p.pols_lapse(0) == pytest.approx(DESIGNED["pols_lapse"], abs=EXACT)
    assert p.claims(0, "LAPSE") == pytest.approx(DESIGNED["claims_lapse"], abs=SUB_WON)
    assert p.commissions(0) == pytest.approx(2000000.0, abs=SUB_WON)
    assert p.expenses(0) == pytest.approx(DESIGNED["expenses"], abs=SUB_WON)
    assert p.net_cf(0) == pytest.approx(DESIGNED["net_cf"], abs=SUB_WON)


def test_the_dispute_panel_period_zero_trace_as_ordered(immediate_annuity):
    """The notes' period-0 trace on point 7: one term goes to zero and everything moves.

    R(0) = 0, so A(0) is the whole interest ₩2,375,750.00, V(1) = V(0) — **the fund stands
    still** — and the death benefit, the surrender value and the expense all follow it down
    or up.  net_cf(0) = +₩91,849,050.71, ₩435,179.52 below the designed basis in the first
    row alone.
    """
    p = immediate_annuity.Projection[7]
    assert p.retention_pp(0) == 0.0
    assert all(p.retention_pp(t) == 0.0 for t in range(0, p.proj_len() + 1))
    assert p.annuity_pp(0) == pytest.approx(ORDERED["annuity_pp"], abs=SUB_WON)
    assert p.annuity_pp(0) == pytest.approx(p.av_pp(0) * 0.025, rel=1e-15)
    assert p.av_pp(1) == pytest.approx(ORDERED["av_pp_1"], abs=SUB_WON)
    assert p.av_pp(1) == pytest.approx(p.av_pp(0), abs=1e-6)
    assert p.annuity_payments(0) == pytest.approx(
        ORDERED["annuity_payments"], abs=SUB_WON)
    assert p.claims(0, "DEATH") == pytest.approx(ORDERED["claims_death"], abs=SUB_WON)
    assert p.claims(0, "LAPSE") == pytest.approx(ORDERED["claims_lapse"], abs=SUB_WON)
    assert p.expenses(0) == pytest.approx(ORDERED["expenses"], abs=SUB_WON)
    assert p.net_cf(0) == pytest.approx(ORDERED["net_cf"], abs=SUB_WON)


@pytest.mark.parametrize("point_id", sorted(DISPUTE_TOTALS))
def test_the_dispute_panel_totals(immediate_annuity, point_id):
    """The notes' side-by-side table of undiscounted totals, column by column.

    ``claims_maturity`` is ₩79,495,349.97 on **both**, the maturity benefit being
    contractually the gross premium either way: the dispute was never about whether the
    ₩100m came back, but about whether the policyholder had been told that part of his
    interest was being taken to fund it.
    """
    p = immediate_annuity.Projection[point_id]
    df = p.result_cf()
    for column, total in DISPUTE_TOTALS[point_id].items():
        assert df[column].sum() == pytest.approx(total, abs=WON), column
    assert p.check_net_cf() is True


def test_the_dispute_costs_the_insurer_the_whole_first_day_deduction(immediate_annuity):
    """+22.96% of income, ₩3.51m of undiscounted outgo, and ₩3,882,556.06 at inception.

    With R = 0 the fund never grows, so the 만기보험금 of the **gross** premium has to be
    found from somewhere the contract does not fund.  ``retention_shortfall_pp()`` is what
    that costs at inception — (M − V(0)) v(10) — and it appears on the right-hand side of
    ``check_annuity_basis()`` rather than being tolerated away, because under ``as_ordered``
    the pricing identity does **not** close on V(0) and should not.
    """
    designed, ordered = immediate_annuity.Projection[6], immediate_annuity.Projection[7]
    assert ordered.annuity_pp(0) / designed.annuity_pp(0) - 1.0 == pytest.approx(
        ANNUITY_UPLIFT_AS_ORDERED, abs=5e-5)
    difference = (ordered.result_cf()["net_cf"].sum()
                  - designed.result_cf()["net_cf"].sum())
    assert difference == pytest.approx(DISPUTE_NET_CF_DIFFERENCE, abs=WON)
    assert designed.retention_shortfall_pp() == 0.0
    assert ordered.retention_shortfall_pp() == pytest.approx(
        RETENTION_SHORTFALL, abs=SUB_WON)
    assert ordered.disc_factor(10) == pytest.approx(DISC_10_AT_250, abs=5e-13)
    assert ordered.retention_shortfall_pp() == pytest.approx(
        (ordered.maturity_benefit() - ordered.av_pp_init()) * ordered.disc_factor(10),
        rel=1e-14)
    # Both close their own pricing identity, the second only with the shortfall in it.
    assert designed.check_annuity_basis() is True
    assert ordered.check_annuity_basis() is True


def test_the_retention_rises_every_year_even_on_a_level_rate(immediate_annuity):
    """R(t) runs 443,616.05 → 554,015.66 while A(t) stays exactly level.

    The remaining term shortens faster than the shortfall M − V(t) closes, so the retention
    rises; the interest V(t) i rises by precisely the same amount, which is the algebraic
    content of V(t) = V(0) + R s(t, i).  **On a falling rate the two move the same way
    instead of opposite ways**, and that is model point 8.
    """
    p = immediate_annuity.Projection[6]
    path = [p.retention_pp(t) for t in range(0, 10)]
    for got, printed in zip(path, RETENTION_PATH):
        assert got == pytest.approx(printed, abs=WON)
    assert path == sorted(path)
    assert all(p.annuity_pp(t) == pytest.approx(DESIGNED["annuity_pp"], abs=SUB_WON)
               for t in range(0, 10))
    for t in range(1, 10):
        assert (p.av_pp(t) * 0.025 - p.av_pp(t - 1) * 0.025) == pytest.approx(
            p.retention_pp(t) - p.retention_pp(t - 1), abs=1e-6)
    # The fund lands on the maturity benefit exactly, which is what R was sized to do.
    assert p.av_pp(10) == pytest.approx(MATURITY_BENEFIT, abs=1e-6)
    assert p.check_av_terminal() is True


def test_the_external_check_on_the_inheritance_annuity(immediate_annuity):
    """₩161,011.16 a month against ``product-spec.md``'s independent ₩161,000.

    The strongest external check the inheritance shape has: the spec reconstructs the
    ten-year 만기형 monthly annuity from published figures without touching the model, and
    the two constructions agree to four significant figures.
    """
    designed, ordered = immediate_annuity.Projection[6], immediate_annuity.Projection[7]
    assert designed.annuity_pp(0) / 12.0 == pytest.approx(DESIGNED_MONTHLY[0], abs=WON)
    assert _true_monthly(designed.annuity_pp(0)) == pytest.approx(
        DESIGNED_MONTHLY[1], abs=WON)
    assert ordered.annuity_pp(0) / 12.0 == pytest.approx(ORDERED_MONTHLY[0], abs=WON)
    assert _true_monthly(ordered.annuity_pp(0)) == pytest.approx(
        ORDERED_MONTHLY[1], abs=WON)
    assert designed.annuity_pp(0) / 12.0 == pytest.approx(161000.0, rel=1e-4)


# ---------------------------------------------------------------------------
# The floor-stepping panel — model point 8


@pytest.mark.parametrize("t", sorted(FLOOR_STEP))
def test_the_floor_stepping_panel_row(immediate_annuity, t):
    """Every row of the notes' point-8 table: the rate, the annuity, R(t) and the fund.

    여자 70, ₩100,000,000, 상속연금형 만기형 20년 on the ``min_guar`` basis, where the
    declared rate is zero so that Max[공시이율, 최저보증이율] resolves to the floor at every
    duration: 1.25% for t = 0 … 4, 1.00% for t = 5 … 9 and 0.75% from t = 10.
    """
    rate, annuity, retention, av = FLOOR_STEP[t]
    p = immediate_annuity.Projection[8]
    assert p.crediting_rate(t) == rate
    assert p.crediting_rate(t) == p.min_guar_rate(t)      # the floor binds, not the rate
    assert p.annuity_pp(t) == pytest.approx(annuity, abs=SUB_WON)
    assert p.retention_pp(t) == pytest.approx(retention, abs=SUB_WON)
    assert p.av_pp(t) == pytest.approx(av, abs=WON)


def test_the_floor_stepping_hand_trace_across_the_first_step(immediate_annuity):
    """The notes' t = 4 → t = 5 trace: s(16, 1.25%) and s(15, 1.00%), and the fund between.

    **The rate falls by one fifth and the annuity falls by one quarter.** 1.25% → 1.00% is
    −20.0%; ₩967,602.66 → ₩722,990.02 is −25.28%.  The extra 5.3 points are the retention
    *rising*, from ₩231,494.18 to ₩238,602.40, at the same moment as the interest it is
    deducted from falls.
    """
    p = immediate_annuity.Projection[8]
    assert p.accum_factor(16, 0.0125) == pytest.approx(S_16_AT_125, abs=FACTOR)
    assert p.accum_factor(15, 0.0100) == pytest.approx(S_15_AT_100, abs=FACTOR)
    assert p.av_pp(4) == pytest.approx(AV_PP_4_POINT_8, abs=SUB_WON)
    assert p.retention_pp(4) == pytest.approx(
        (p.maturity_benefit() - p.av_pp(4)) / p.accum_factor(16, 0.0125), rel=1e-13)
    assert p.annuity_pp(4) == pytest.approx(
        p.av_pp(4) * 0.0125 - p.retention_pp(4), rel=1e-13)
    assert p.av_pp(5) == pytest.approx(AV_PP_5_POINT_8, abs=SUB_WON)
    assert p.av_pp(5) == pytest.approx(
        p.av_pp(4) * 1.0125 - p.annuity_pp(4), rel=1e-14)
    assert p.retention_pp(5) == pytest.approx(
        (p.maturity_benefit() - p.av_pp(5)) / p.accum_factor(15, 0.0100), rel=1e-13)
    assert p.annuity_pp(5) / p.annuity_pp(4) - 1.0 == pytest.approx(
        FIRST_STEP_FALL, abs=5e-5)
    assert p.retention_pp(5) > p.retention_pp(4)
    assert p.crediting_rate(5) / p.crediting_rate(4) - 1.0 == pytest.approx(-0.20)


def test_the_annuity_halves_while_the_floor_is_honoured_at_every_step(immediate_annuity):
    """−50.73% from year 1 to year 11, and ``av_pp(20)`` is ₩100,000,000.00 exactly.

    That is the substance of the dispute in one table: **the floor is a rate on the fund,
    never a floor on the annuity**.  The second step costs a further 34.07%, the monthly
    income falls from 80,633.56 to 39,724.30, and the fund still reaches its 만기보험금 to
    the won because the retention is re-struck against the remaining term at the current
    rate each year.
    """
    p = immediate_annuity.Projection[8]
    assert p.annuity_pp(10) / p.annuity_pp(9) - 1.0 == pytest.approx(
        SECOND_STEP_FALL, abs=5e-5)
    assert p.annuity_pp(10) / p.annuity_pp(0) - 1.0 == pytest.approx(
        TWO_STEP_FALL, abs=5e-5)
    assert p.annuity_pp(0) / 12.0 == pytest.approx(FLOOR_MONTHLY[0], abs=WON)
    assert p.annuity_pp(10) / 12.0 == pytest.approx(FLOOR_MONTHLY[1], abs=WON)
    assert p.av_pp(20) == pytest.approx(AV_PP_20_POINT_8, abs=1e-6)
    assert p.check_av_terminal() is True
    assert p.check_av_roll_fwd() is True
    # The floor was honoured at every single step while the annuity halved.
    assert all(p.crediting_rate(t) >= 0.0075 for t in range(0, p.proj_len() + 1))
    assert all(p.av_pp(t + 1) > p.av_pp(t) for t in range(0, p.proj_len() + 1))


# ---------------------------------------------------------------------------
# The load cross-check — model point 9, the shape with no mortality in its annuity


def test_the_certain_shape_load_cross_check(immediate_annuity):
    """A(0) = V(0)/a(10, 2.5%) = ₩10,858,010.26, i.e. ₩894,628.93 a month adjusted.

    Against 교보's published 90만원 on a 2.52% basis — the −0.5% of ``product-spec.md``'s own
    cross-check table, reproduced by the model rather than by a spreadsheet.  **The
    annuitant's age and sex are irrelevant to a 확정기간연금형**, so a 남자 55 published
    figure is directly comparable with the model's 남자 60 one, and because this shape
    carries no mortality in its annuity it is the sharpest available test of the expense
    load.
    """
    p = immediate_annuity.Projection[9]
    assert p.shape() == "certain"
    assert p.av_pp_init() == pytest.approx(AV_PP_INIT_LOADED, abs=SUB_WON)
    assert p.annuity_factor_certain(10, 0.025) == pytest.approx(A_10_AT_250, abs=FACTOR)
    assert p.annuity_pp(0) == pytest.approx(CERTAIN_ANNUITY, abs=SUB_WON)
    assert p.annuity_pp(0) == pytest.approx(
        p.av_pp_init() / p.annuity_factor_certain(10, 0.025), rel=1e-15)
    assert p.annuity_pp(0) / 12.0 == pytest.approx(CERTAIN_MONTHLY_NAIVE, abs=WON)
    assert _true_monthly(p.annuity_pp(0)) == pytest.approx(CERTAIN_MONTHLY_TRUE, abs=WON)
    assert round(_true_monthly(p.annuity_pp(0)) / 10000.0, 1) == 89.5
    assert abs(_true_monthly(p.annuity_pp(0)) / 900000.0 - 1.0) < 0.01
    # The residual against the spec's own -0.5% is the 0.02 points of declared rate:
    # the spec solves the same identity on 교보's 2.52%, this model runs the
    # representative 2.50%.
    assert p.decl_rate() == DECL_RATE < 0.0252
    # No mortality in the annuity: the factor is pure interest on this shape.
    assert all(p.pricing_factor(t) == 1.0 for t in range(0, p.proj_len() + 1))
    with pytest.raises(FormulaError):
        p.annuity_factor()


def test_the_certain_shape_totals_and_the_fund_that_exhausts(immediate_annuity):
    """The notes' point-9 totals, and ``av_pp(10)`` = −0.0000000410 of float noise.

    The fund runs off to zero on its own, the annuity-certain's run-off being what
    ``check_av_terminal()`` tolerates, and ``claims_lapse(9) = 0.00`` because the surrender
    rate is suppressed in the final period on every shape, so a contract in its last year
    runs to its last instalment.
    """
    p = immediate_annuity.Projection[9]
    df = p.result_cf()
    for column, total in CERTAIN_TOTALS.items():
        assert df[column].sum() == pytest.approx(total, abs=WON), column
    assert p.av_pp(10) == pytest.approx(0.0, abs=1e-6)
    assert abs(p.av_pp(10)) < 1e-7 * p.prem_pp()
    assert p.check_av_terminal() is True
    assert p.claims(9, "LAPSE") == 0.0
    assert p.annuity_payments(9) == pytest.approx(CERTAIN_LAST_INSTALMENT, abs=WON)
    assert p.annuity_payments(9) / df["annuity_payments"].sum() == pytest.approx(
        0.091, abs=5e-4)
    assert df["claims_maturity"].sum() == 0.0     # the instalments exhaust the fund


# ---------------------------------------------------------------------------
# Which check_* cells this model publishes


def test_which_checks_this_model_publishes(immediate_annuity, kr_immediate_anchor):
    """The eleven check cells, asserted **by name**, with the six that carry a residual.

    A generic sweep over ``check_*`` cannot notice a check that has quietly disappeared: it
    would call the ten that remain, pass, and prove less than it did before.  Naming the set
    here is what turns "every check passes" into a statement about *which* checks.  That
    every one of them is True on **every** shipped model point is
    ``test_model_conventions_kr.py``'s single sweep and is not repeated here.

    ``check_annuity_basis_resid`` is the one residual taking no argument, because the
    pricing identity is a single statement about the contract at inception rather than a
    per-period one.  ``check_av_terminal``, ``check_premium_split``, ``check_rate_level``,
    ``check_guarantee_certain`` and ``check_surr_value`` carry no residual at all: each is a
    statement about *where* a quantity stands rather than about how far an identity misses.
    """
    cells = set(immediate_annuity.Projection.cells)
    published = {n for n in cells
                 if n.startswith("check_") and not n.endswith("_resid")}
    assert published == CHECKS
    resid = {n[:-len("_resid")] for n in cells
             if n.startswith("check_") and n.endswith("_resid")}
    assert resid == CHECKS_WITH_RESID
    a = kr_immediate_anchor
    for name in sorted(CHECKS):
        value = getattr(a, name)()
        assert value is True, f"{name}() is not True on the anchor cell"
        assert isinstance(value, bool), f"{name}() must return a real bool"
    assert a.check_annuity_basis_resid() == pytest.approx(0.0, abs=1e-4)
    money = {"check_av_roll_fwd", "check_net_cf"}
    for name in sorted(CHECKS_WITH_RESID - {"check_annuity_basis"}):
        residual = getattr(a, name + "_resid")
        tol = 1e-12 * a.prem_pp() if name in money else 1e-10
        for t in range(0, a.proj_len() + 1):
            assert residual(t) == pytest.approx(0.0, abs=tol), f"{name}_resid({t})"


def test_the_check_tolerances_are_named_references(immediate_annuity,
                                                   kr_immediate_anchor):
    """``roll_fwd_tol`` for the probability identities, ``val_tol`` scaled by the premium.

    The two are different quantities and must not collapse into one.  ``roll_fwd_tol``
    closes dimensionless identities between probabilities near 1.0.  ``val_tol`` is
    *relative* and is multiplied by ``prem_pp()`` at every use, because this product's
    monetary quantities run from ₩10,000,000 to ₩5,000,000,000 across the shipped table and
    a fixed absolute tolerance would be slack at one end and impossible at the other.  Both
    are far below one won at every shipped premium.
    """
    refs = immediate_annuity.Projection.refs
    assert "roll_fwd_tol" in refs and "val_tol" in refs
    assert refs["roll_fwd_tol"] == 1e-10 and refs["val_tol"] == 1e-12
    assert refs["omega_age"] == OMEGA_AGE
    table = immediate_annuity.Data.model_point_table()
    assert refs["val_tol"] * table["prem_pp"].max() < 1.0
    # The tolerance is not slack the checks hide behind.
    a = kr_immediate_anchor
    worst = max(abs(a.check_net_cf_resid(t)) for t in range(0, a.proj_len() + 1))
    assert worst < refs["val_tol"] * a.prem_pp() / 100.0


# ---------------------------------------------------------------------------
# The product's own invariants, recursions and processing order


def test_the_obligation_rolls_forward_on_its_own_decrements(immediate_annuity,
                                                            kr_immediate_anchor):
    """IF(t) − exits(t) − IF(t + 1) = 0, with ``pols_exit`` built independently of IF.

    On the life shape the identity has real content: nothing exits inside the 보증지급기간,
    the whole cohort that died in it exits at t = g − 1, and the deaths of each later period
    exit as they fall.  Asserted here on the anchor and on one point of each other shape,
    where the exits are the decrements themselves.
    """
    a = kr_immediate_anchor
    assert a.check_pols_roll_fwd() is True
    for t in range(0, a.proj_len() + 1):
        assert a.pols_if(t) - a.pols_exit(t) - a.pols_if(t + 1) == pytest.approx(
            0.0, abs=1e-12)
    assert sum(a.pols_exit(t) for t in range(0, a.proj_len() + 1)) == pytest.approx(
        1.0, abs=1e-9)
    for point_id, expected in ((6, "inheritance"), (9, "certain")):
        p = immediate_annuity.Projection[point_id]
        assert p.shape() == expected
        assert p.check_pols_roll_fwd() is True
        for t in range(0, p.proj_len() + 1):
            built = (p.pols_lapse(t) if p.shape() == "certain"
                     else p.pols_death(t) + p.pols_lapse(t))
            assert p.pols_exit(t) == pytest.approx(built, rel=1e-14), (point_id, t)


def test_the_survival_curve_closes_against_a_direct_product(kr_immediate_anchor):
    """l(t) equals the explicit product of (1 − q) over the attained ages, with no recursion.

    ``lives_if`` is a one-step recursion and ``check_lives_roll_fwd`` rebuilds the same
    probability from the table directly, so an off-by-one in the age indexing shows up from
    the first period rather than as a plausible-looking annuity.
    """
    a = kr_immediate_anchor
    assert a.check_lives_roll_fwd() is True
    built = 1.0
    for t in range(0, a.proj_len() + 1):
        assert a.lives_if(t) == pytest.approx(built, abs=1e-14)
        built *= (1.0 - a.mort_rate(t))
    assert built == 0.0                        # q(110) = 1 closes the table
    assert a.lives_if(a.proj_len() + 1) == 0.0


def test_the_fund_recursion_closes_against_a_closed_form_on_every_shape(
        immediate_annuity, kr_immediate_anchor):
    """V(t + 1) = V(t)(1 + i(t)) − A(t), against four genuinely different derivations.

    ``check_av_roll_fwd`` rebuilds the fund per shape — the retrospective closed form on the
    life shape, the annuity-certain's own run-off on the certain shape, the algebraic
    reduction ``V + (M − V)/s`` under ``as_designed`` and a standing fund under
    ``as_ordered`` — so it is a second derivation and not the recursion written twice.
    """
    a = kr_immediate_anchor
    assert a.check_av_roll_fwd() is True
    for t in range(0, a.proj_len() + 1):
        assert a.av_pp(t + 1) == pytest.approx(
            a.av_pp(t) * (1.0 + a.crediting_rate(t)) - a.annuity_pp(t), rel=1e-12)
    i0 = a.crediting_rate(0)
    for t in (1, 10, 28, 50):
        assert a.av_pp(t) == pytest.approx(
            a.av_pp_init() * (1.0 + i0) ** t
            - a.annuity_pp(0) * a.accum_factor(t, i0), abs=1e-3)
    for point_id in (6, 7, 8, 9):
        p = immediate_annuity.Projection[point_id]
        assert p.check_av_roll_fwd() is True, point_id
        assert p.check_av_terminal() is True, point_id


def test_the_pricing_identity_ties_the_projection_to_the_fund(immediate_annuity,
                                                              kr_immediate_anchor):
    """V(0) is the present value of everything it was struck to buy, on all three shapes.

    ``check_annuity_basis`` discounts the projected annuity on the crediting-rate path — so a
    stepping floor is handled without assuming a level rate — and adds the discounted
    만기보험금 where there is one.  It is what holds the **life** shape to its basis, that
    shape having no contractual terminal fund value for ``check_av_terminal`` to test.
    """
    a = kr_immediate_anchor
    assert a.check_annuity_basis() is True
    built = sum(a.annuity_pp(t) * a.pricing_factor(t) * a.disc_factor(t + 1)
                for t in range(0, a.proj_len() + 1))
    assert built == pytest.approx(a.av_pp_init(), abs=1e-6)
    for point_id in (6, 8, 9):
        p = immediate_annuity.Projection[point_id]
        assert p.check_annuity_basis() is True, point_id
        assert p.check_annuity_basis_resid() == pytest.approx(
            0.0, abs=1e-12 * p.prem_pp()), point_id


def test_the_premium_split_closes_and_there_is_no_acquisition_strain(immediate_annuity):
    """A = B + C + D, on every shape, with nothing left over in either direction.

    The 약관's own division of the single premium into the 보장계약 보험료, the 사업비 and the
    연금계약 순보험료 that becomes the opening fund.  It is the statement that this product
    has **no acquisition strain**: the charge taken from the fund at inception is exactly the
    outgo at inception, so ``net_cf(0)`` is positive on every shipped model point — the only
    model in ``krlib`` of which that is true.
    """
    for point_id in (1, 6, 9):
        p = immediate_annuity.Projection[point_id]
        assert p.check_premium_split() is True, point_id
        built = (p.prem_pp() * p.comm_rate()
                 + p.prem_pp() * p.acq_expense_rate()
                 + p.risk_prem_pp()
                 + p.av_pp_init())
        assert built == pytest.approx(p.prem_pp(), abs=1e-6), point_id
        assert p.comm_rate() < p.acq_charge_rate()      # the charge covers the commission
        assert p.net_cf(0) > 0.0
        assert all(p.net_cf(t) < 0.0 for t in range(1, p.proj_len()))


def test_the_notes_processing_order_is_the_order_the_model_runs(immediate_annuity):
    """Steps 2 to 6 of the notes' processing order, each by a quantity that would differ.

    The order is not presentational: four of the flows depend on it, so each is asserted by a
    number an out-of-order model would produce differently.

    **Credit, then strike the annuity** — on the certain shape A(t) = V(t)/a(m, i) and not
    V(t)(1 + i)/a(m, i), the two differing by the whole year's interest; the order is what
    exhausts the fund to zero at the end of the term rather than to a residue.
    **Deaths at the end of the period** — the 사망보험금 is measured on the fund carried
    forward, so on point 6 at t = 0 it is 0.00353 × (0.10 P + V(1)) = ₩372,321.86 against
    ₩370,755.90 on the fund at the start, and the two differ in every period.
    **Surrenders after the deaths** — the inheritance branch carries a (1 − q) the certain
    branch does not, so the weight is 0.0199294 rather than 0.02; on the certain shape the
    contract survives the annuitant and the decrement bites on persistency alone.
    **The 만기보험금 last, at IF(N + 1)** — one further period of decrement away from the row
    that carries it, and nil at every earlier t and on both other shapes.
    """
    inheritance = immediate_annuity.Projection[6]
    certain = immediate_annuity.Projection[9]

    for t in range(0, certain.proj_len() + 1):
        i, m = certain.crediting_rate(t), certain.annuity_term() - t
        assert certain.annuity_pp(t) == pytest.approx(
            certain.av_pp(t) / certain.annuity_factor_certain(m, i), rel=1e-14)
        credited = certain.av_pp(t) * (1.0 + i) / certain.annuity_factor_certain(m, i)
        assert credited / certain.annuity_pp(t) == pytest.approx(1.025, rel=1e-12)
    assert certain.av_pp(certain.proj_len() + 1) == pytest.approx(0.0, abs=1e-6)

    for t in range(0, inheritance.proj_len() + 1):
        rho_p = inheritance.db_rate() * inheritance.prem_pp()
        assert inheritance.claims(t, "DEATH") == pytest.approx(
            inheritance.pols_death(t) * (rho_p + inheritance.av_pp(t + 1)), rel=1e-14)
        assert inheritance.claims(t, "DEATH") != pytest.approx(
            inheritance.pols_death(t) * (rho_p + inheritance.av_pp(t)), rel=1e-9)
        assert inheritance.pols_lapse(t) == pytest.approx(
            inheritance.lives_if(t) * (1.0 - inheritance.mort_rate(t))
            * inheritance.surr_if(t) * inheritance.lapse_rate(t), rel=1e-14)
        assert certain.pols_lapse(t) == pytest.approx(
            certain.surr_if(t) * certain.lapse_rate(t), rel=1e-14)
    assert inheritance.claims(0, "DEATH") == pytest.approx(
        DESIGNED["claims_death"], abs=SUB_WON)
    assert inheritance.pols_death(0) * (0.10 * inheritance.prem_pp()
                                        + inheritance.av_pp(0)) == pytest.approx(
        370755.90, abs=WON)
    assert inheritance.pols_lapse(0) == pytest.approx(0.0199294, abs=EXACT)
    assert certain.pols_lapse(0) == pytest.approx(0.02, rel=1e-14)

    n = inheritance.proj_len()
    assert inheritance.claims(n, "MATURITY") == pytest.approx(
        inheritance.pols_if(n + 1) * inheritance.maturity_benefit(), rel=1e-14)
    assert all(inheritance.claims(t, "MATURITY") == 0.0 for t in range(0, n))
    assert inheritance.pols_if(n + 1) < inheritance.pols_if(n)
    for point_id in (1, 9):
        q = immediate_annuity.Projection[point_id]
        assert q.maturity_benefit() == 0.0
        assert all(q.claims(t, "MATURITY") == 0.0 for t in range(0, q.proj_len() + 1))


def test_the_published_statement_adds_up(immediate_annuity, kr_immediate_anchor):
    """``net_cf`` equals the published columns of the same row, rebuilt from the frame.

    ``check_net_cf`` re-reads ``result_cf()``'s own columns rather than the formulas, so a
    component missing from the statement fails there rather than being reconciled only in
    prose.  Asserted on the anchor and on one point of each other shape, the three shapes
    having three different sets of non-zero columns.
    """
    for point_id in (1, 6, 8, 9):
        p = immediate_annuity.Projection[point_id]
        assert p.check_net_cf() is True, point_id
        df = p.result_cf()
        outgo = df[["annuity_payments", "claims_death", "claims_lapse",
                    "claims_maturity", "commissions", "expenses"]].sum(axis=1)
        assert (df["premiums"] - outgo - df["net_cf"]).abs().max() == pytest.approx(
            0.0, abs=1e-6)
    a = kr_immediate_anchor
    assert "claims" not in a.result_cf().columns


def test_the_two_result_frames_and_the_sign_they_publish(immediate_annuity,
                                                         kr_immediate_anchor):
    """Both frames' columns in order, and both signs of the net flow published as columns.

    ``result_cf()`` puts ``pols_if`` first because the library publishes the in-force measure
    first, and carries the three ``claims_*`` splits with no subtotal beside them;
    ``liability_cf`` is the notes' outgo-positive CF(t) and ``net_cf`` its exact negative, so
    that neither a reader of the notes nor a reader of the library has to negate anything by
    hand.  ``result_pols()`` is the companion frame — everything the statement is built out
    of and nothing that is a cash flow itself, stated at the **start** of the period.
    """
    a = kr_immediate_anchor
    df = a.result_cf()
    assert list(df.columns) == [
        "pols_if", "premiums", "annuity_payments", "claims_death", "claims_lapse",
        "claims_maturity", "commissions", "expenses", "liability_cf", "net_cf",
    ]
    assert df.index.name == "t"
    assert list(df.index) == list(range(0, PROJ_LEN + 1))
    assert df.notna().all().all()
    assert df.loc[0, "net_cf"] == pytest.approx(NET_CF_0, abs=WON) and df.loc[
        0, "net_cf"] > 0.0                      # the single premium is income
    assert (df["liability_cf"] + df["net_cf"]).abs().max() == 0.0
    assert "liability_cf" in immediate_annuity.Projection.cells
    pols = a.result_pols()
    assert list(pols.columns) == [
        "pols_if", "lives_if", "surr_if", "pols_death", "pols_lapse", "payment_factor",
        "crediting_rate", "av_pp", "cv_pp", "annuity_pp", "retention_pp",
    ]
    assert pols.index.name == "t" and len(pols) == PROJ_LEN + 1
    assert pols.loc[0, "av_pp"] == pytest.approx(AV_PP_INIT, abs=SUB_WON)
    assert (pols["retention_pp"] == 0.0).all()  # no maturity benefit on this shape
    assert not any(c.startswith("premium") or c.endswith("_cf") for c in pols.columns)


def test_the_surrender_deduction_is_nil_and_the_statutory_cap_binds_nothing(
        immediate_annuity, kr_immediate_anchor):
    """해약공제액 = 0 at every duration, so 해약환급금 is the 계약자적립액 exactly.

    Not generosity but structure: a single-premium annuity has no unamortised acquisition
    cost to recover, the cost having been taken in full at inception, so 별표 14's
    표준해약공제액 cap binds nothing here.  The zero was **observed** on the published run
    rather than assumed, which is why the cells exists at all instead of the deduction being
    dropped from the formula.
    """
    a = kr_immediate_anchor
    assert all(a.surr_chg_pp(t) == 0.0 for t in range(0, a.proj_len() + 1))
    assert a.check_surr_value() is True
    for point_id in (6, 9):
        p = immediate_annuity.Projection[point_id]
        assert p.check_surr_value() is True
        for t in range(0, p.proj_len() + 2):
            assert p.surr_chg_pp(t) == 0.0
            assert p.cv_pp(t) == pytest.approx(max(p.av_pp(t), 0.0), abs=1e-6)
        assert p.claims(0, "LAPSE") == pytest.approx(
            p.pols_lapse(0) * p.cv_pp(1), rel=1e-14)


def test_the_crediting_rate_is_a_max_and_the_floor_is_inert_on_the_anchor(
        immediate_annuity, kr_immediate_anchor):
    """i(t) = Max[공시이율, 최저보증이율(t)], the 약관's own rule, both ways round.

    On ``decl_2017`` the declared rate is above every step of the floor, so the rate is level
    and the floor is inert — which is the condition the life shape's once-struck factor
    relies on and ``check_rate_level()`` asserts.  On ``min_guar`` the declared rate is zero
    and the floor binds at every duration.
    """
    a = kr_immediate_anchor
    assert a.check_rate_level() is True
    for t in (0, 4, 5, 9, 10, 50):
        assert a.crediting_rate(t) == max(a.decl_rate(), a.min_guar_rate(t))
        assert a.crediting_rate(t) == a.decl_rate() > a.min_guar_rate(t)
    stepping = immediate_annuity.Projection[8]
    assert stepping.decl_rate() == 0.0
    for t in (0, 4, 5, 9, 10, 19):
        assert stepping.crediting_rate(t) == stepping.min_guar_rate(t)
    # The life shape asserts levelness; the other two carry a stepping rate correctly.
    assert stepping.check_rate_level() is True      # True on a non-life shape by design
    assert stepping.crediting_rate(0) != stepping.crediting_rate(19)


# ---------------------------------------------------------------------------
# Known modeling pitfalls — one test per pitfall, named after it


def test_pitfall_pols_if_is_not_a_survival_probability(kr_immediate_anchor):
    """Pitfall 1: treating ``pols_if`` as a survival probability.

    It is the probability that a **payment obligation remains**.  On the anchor it is exactly
    1.000000 for ten years while the annuitant's survival probability has already fallen to
    0.959799 by t = 9, so any per-policy quantity weighted by survival inside the guarantee
    is understated.  The model says so in that cells' own docstring, in the phrase the
    conventions suite reads.
    """
    a = kr_immediate_anchor
    assert all(a.pols_if(t) == 1.0 for t in range(0, 10))
    assert a.lives_if(9) == pytest.approx(0.959798841, abs=PROB)
    assert a.pols_if(9) != a.lives_if(9)
    assert a.pols_if(9) > a.lives_if(9)
    for t in range(0, a.proj_len() + 1):
        assert a.pols_if(t) >= a.lives_if(t)
    doc = a.cells["pols_if"].doc.replace("*", "")
    assert "payment obligation remains" in doc
    assert "not a policy count" in doc
    assert "not a survival probability" in doc


def test_pitfall_the_guarantee_is_a_max_and_not_a_sum(kr_immediate_anchor):
    """Pitfall 2: adding the guarantee to the survival probability instead of taking the max.

    An additive form pays ``1 + l(t + 1)`` for the whole guaranteed term, giving a factor of
    **28.061177** against the correct **19.502675** and an annuity of ₩3,438,914.97 — 69.50%
    of the right answer, a 30% under-payment for life.
    """
    a = kr_immediate_anchor
    v = 1.0 / (1.0 + a.crediting_rate(0))
    additive = sum(
        v ** (t + 1) * (a.lives_if(t + 1) + (1.0 if t + 1 <= a.annuity_term() else 0.0))
        for t in range(0, a.proj_len() + 1))
    assert additive == pytest.approx(ADDITIVE_FACTOR, abs=5e-7)
    assert a.av_pp_init() / additive == pytest.approx(ADDITIVE_ANNUITY, abs=WON)
    assert (a.av_pp_init() / additive) / a.annuity_pp(0) == pytest.approx(
        ADDITIVE_SHARE, abs=5e-5)
    assert additive > a.annuity_factor()
    # The model takes the max, and the checks that would fail on the sum both pass.
    for t in range(0, a.proj_len() + 1):
        guaranteed = 1.0 if t + 1 <= a.annuity_term() else 0.0
        assert a.payment_factor(t) == max(a.lives_if(t + 1), guaranteed)
    assert a.check_guarantee_certain() is True
    assert a.check_payment_factor() is True


def test_pitfall_nothing_exits_inside_the_guarantee(kr_immediate_anchor):
    """Pitfall 3: decrementing the obligation on a death inside the 보증지급기간.

    Nothing exits until the guarantee expires and then the whole cohort that died inside it
    exits at once: ``pols_exit(t) = 0`` for t = 0 … 8 and ``pols_exit(9) = 0.046529974860``.
    The same pitfall covers confusing the two guarantee tests — the obligation is open at
    time t for t = 0 … 9 while the instalments the guarantee covers fall at times 1 … 10, so
    ``pols_if(10) = l(10)`` and ``payment_factor(10) = l(11)`` are different numbers on the
    same row, and either error shifts the cliff by a year.
    """
    a = kr_immediate_anchor
    assert all(a.pols_exit(t) == 0.0 for t in range(0, 9))
    assert a.pols_exit(8) == 0.0
    assert a.pols_exit(9) == pytest.approx(POLS_EXIT_9, abs=EXACT)
    assert a.pols_exit(9) > 6.0 * a.pols_exit(10)      # a step, not a curve
    assert a.pols_if(10) == pytest.approx(a.lives_if(10), rel=1e-15)
    assert a.payment_factor(10) == pytest.approx(a.lives_if(11), rel=1e-15)
    assert a.pols_if(10) - a.payment_factor(10) == pytest.approx(
        POLS_IF_10 - PAYMENT_FACTOR_10, abs=EXACT)
    assert a.check_pols_roll_fwd() is True
    assert a.check_guarantee_certain() is True


def test_pitfall_proj_len_is_a_last_index_not_a_row_count(immediate_annuity):
    """Pitfall 4: ``proj_len()`` read as a row count.

    It is the **last row index**.  The anchor has 51 rows, 0 … 50, and ω − x = 110 − 60 = 50.
    An off-by-one drops the last instalment on the term shapes — on point 9 that is
    ₩9,052,841.76 of outgo, 9.1% of the annuity total.  The notes' horizon column is asserted
    beside it for all ten shipped points, N being max(g − 1, ω − x) on the life shape and
    n − 1 on the other two: a structural property of the shape and not a rounded projection
    length, so that the life shape's obligation is exhausted rather than truncated.
    """
    for point_id, horizon in SHIPPED_HORIZONS.items():
        p = immediate_annuity.Projection[point_id]
        df = p.result_cf()
        assert len(df) == p.proj_len() + 1, point_id
        assert df.index[0] == 0 and df.index[-1] == p.proj_len(), point_id
        assert p.proj_len() == horizon
        if p.shape() == "life":
            assert p.proj_len() == max(p.annuity_term() - 1,
                                       OMEGA_AGE - p.age_at_entry())
            assert p.mort_rate(p.proj_len()) == 1.0
            assert p.lives_if(p.proj_len() + 1) == 0.0
        else:
            assert p.proj_len() == p.annuity_term() - 1
    certain = immediate_annuity.Projection[9]
    dropped = certain.annuity_payments(certain.proj_len())
    assert dropped == pytest.approx(CERTAIN_LAST_INSTALMENT, abs=WON)
    total = certain.result_cf()["annuity_payments"].sum()
    assert dropped / total == pytest.approx(0.091, abs=5e-4)


def test_pitfall_the_mortality_rate_is_read_at_the_start_of_the_period(
        kr_immediate_anchor):
    """Pitfall 5: reading the mortality rate at the wrong end of the period.

    ``lives_if`` applies q(x + t − 1), the age attained at the **start** of the period.
    Reading q(x + t) raises the factor's mortality by a year throughout and gives an annuity
    of ₩5,060,720.68, +2.28% — and on the anchor walks off the end of the table at age 111
    and raises rather than returning a wrong answer, which is the good case.
    """
    a = kr_immediate_anchor
    assert a.check_lives_roll_fwd() is True
    for t in range(1, a.proj_len() + 2):
        assert a.lives_if(t) == pytest.approx(
            a.lives_if(t - 1) * (1.0 - a.mort_rate(t - 1)), rel=1e-14)
    with pytest.raises(FormulaError):
        a.mort_rate(a.proj_len() + 1)          # 보험나이 111 is off the shipped table
    v = 1.0 / (1.0 + a.crediting_rate(0))
    lives = [1.0]
    for t in range(0, a.proj_len() + 1):
        lives.append(lives[-1] * (1.0 - a.mort_rate(t + 1)) if t < a.proj_len() else 0.0)
    wrong = sum(v ** (t + 1) * max(lives[t + 1],
                                   1.0 if t + 1 <= a.annuity_term() else 0.0)
                for t in range(0, a.proj_len() + 1))
    assert a.av_pp_init() / wrong == pytest.approx(WRONG_END_ANNUITY, abs=WON)
    assert (a.av_pp_init() / wrong) / a.annuity_pp(0) - 1.0 == pytest.approx(
        WRONG_END_UPLIFT, abs=5e-6)


def test_pitfall_the_model_runs_on_boheom_nai_and_not_man_nai(immediate_annuity):
    """Pitfall 6: running the model on 만나이 instead of 보험나이.

    The tables, the model point column and the issue-age band are all 보험나이; the 완전생명표
    and every Korean population statistic are 만나이, and the six-month rule makes the two
    differ for half of all issue dates.  The error is worth about half a year of ageing on
    every row and **raises nothing**, so the basis is recorded in the registry metadata and
    named in the docstring where a reader will meet it.
    """
    assert MODELS["Immediate_KR_A"][1]["age_basis"] == "보험나이"
    assert MODELS["Immediate_KR_A"][1]["grid"] == "annual"
    proj = immediate_annuity.Projection.doc
    assert "보험나이" in proj and "만나이" in proj
    assert "six-month rule" in proj
    doc = immediate_annuity.Projection.cells["age"].doc
    assert "보험나이" in doc and "계약해당일" in doc
    a = immediate_annuity.Projection[1]
    assert a.age(0) == a.age_at_entry()
    assert a.age(10) == a.age_at_entry() + 10
    assert a.mort_rate(10) == 0.00728          # the published rate at 보험나이 70


def test_pitfall_the_mortality_table_is_never_the_gyeongheom_saengmyeongpyo():
    """Pitfall 7: presenting ``mort_table.csv`` as the 경험생명표.

    It is a **[std]** Makeham construction on three published anchors, it misses the
    보험나이 50 anchor by +22.01% for men, and the 제10회 경험생명표 is not published at all.
    Every row carries a ``provenance`` cell, the two fit-anchor rows per sex say they are the
    published 개인연금사망률 reproduced exactly, and the residual row reports its own miss
    rather than hiding it.
    """
    table = pd.read_csv(CSV_DIR / "mort_table.csv")
    assert list(table.columns) == ["sex", "age", "mort_rate", "provenance"]
    assert table["provenance"].notna().all()
    assert (table["provenance"].str.strip() != "").all()
    assert table["provenance"].str.contains("NOT published|residual|limiting age").any()
    for (sex, age), rate in SOURCED_MORT_ANCHORS.items():
        row = table[(table["sex"] == sex) & (table["age"] == age)].iloc[0]
        assert row["mort_rate"] == pytest.approx(rate, abs=5e-12)
        assert "fit anchor" in row["provenance"]
        assert "[S1 IV-2]" in row["provenance"]
    residual = table[(table["sex"] == "M") & (table["age"] == 50)].iloc[0]
    assert residual["mort_rate"] / 0.00225 == pytest.approx(1.220, abs=5e-4)
    assert "residual" in residual["provenance"]
    for sex in ("M", "F"):
        sub = table[table["sex"] == sex]
        assert sub["age"].min() == 40 and sub["age"].max() == OMEGA_AGE
        assert sub[sub["age"] == OMEGA_AGE]["mort_rate"].iloc[0] == 1.0
        assert not sub["provenance"].str.contains("경험생명표를 전재").any()


def test_pitfall_the_life_shape_annuity_is_not_re_struck_each_year(immediate_annuity):
    """Pitfall 8: recomputing the life-shape annuity from the fund each year.

    ``av_pp`` on the life shape is **not** the reserve and goes negative at t = 28; an annuity
    re-struck as V(t)/ä(x+t, ·) would collapse toward zero and then turn negative.  The 약관
    bases the annuity on 「연금개시시의 계약자적립액」 and the annuitant-mortality ratchet is
    inert on an immediate annuity, there being no interval between issue and annuitisation.
    """
    for point_id in (1, 2, 3, 4, 5):
        p = immediate_annuity.Projection[point_id]
        assert p.shape() == "life"
        level = p.annuity_pp(0)
        assert all(p.annuity_pp(t) == level for t in range(0, p.proj_len() + 1)), point_id
        assert p.check_rate_level() is True, point_id
    a = immediate_annuity.Projection[1]
    assert a.annuity_pp(30) == a.annuity_pp(0)
    assert a.av_pp(30) < 0.0                    # a re-struck annuity would be negative
    assert a.annuity_pp(0) == pytest.approx(
        a.av_pp_init() / a.annuity_factor(), rel=1e-15)


def test_pitfall_av_pp_is_not_floored_at_zero(kr_immediate_anchor):
    """Pitfall 9: flooring ``av_pp`` at zero on the life shape.

    It would hide the fact that a life annuity's fund is not its reserve and would break the
    retrospective closed form V(0)(1 + i)^t − A s(t, i) from t = 28 onward.  Nothing
    downstream reads the negative value: ``cv_pp`` is nil and surrender is impossible there.
    """
    a = kr_immediate_anchor
    assert a.av_pp(28) < 0.0
    assert min(a.av_pp(t) for t in range(0, a.proj_len() + 2)) < -1.4e8
    assert a.check_av_roll_fwd() is True
    i0 = a.crediting_rate(0)
    for t in (28, 40, 50):
        assert a.av_pp(t) == pytest.approx(
            a.av_pp_init() * (1.0 + i0) ** t
            - a.annuity_pp(0) * a.accum_factor(t, i0), abs=1e-3)
        assert a.cv_pp(t) == 0.0
    assert all(a.claims(t, "LAPSE") == 0.0 for t in range(0, a.proj_len() + 1))
    assert "payment obligation remains" in a.cells["pols_if"].doc


def test_pitfall_the_retention_is_re_struck_every_year(immediate_annuity):
    """Pitfall 10: computing the retention once, at inception, instead of every year.

    On a level rate the two agree and the fund still lands on M, so the error is **invisible
    on model points 6 and 7**.  It appears only on a stepping rate: point 8's retention runs
    220,272.34 → 271,273.86 over twenty years, and the fund reaches ₩100,000,000.00 exactly
    because R is recomputed against the remaining term at the current rate.
    """
    p = immediate_annuity.Projection[8]
    frozen = p.retention_pp(0)
    path = [p.retention_pp(t) for t in range(0, p.proj_len() + 1)]
    assert path[0] == pytest.approx(220272.3364700692, abs=SUB_WON)
    assert path[-1] == pytest.approx(271273.8626488275, abs=SUB_WON)
    assert path == sorted(path)
    assert path[-1] / frozen - 1.0 > 0.23
    for t in (0, 5, 10, 19):
        m = p.annuity_term() - t
        assert p.retention_pp(t) == pytest.approx(
            (p.maturity_benefit() - p.av_pp(t))
            / p.accum_factor(m, p.crediting_rate(t)), rel=1e-13)
    assert p.av_pp(20) == pytest.approx(MATURITY_BENEFIT, abs=1e-6)
    assert p.check_av_terminal() is True
    assert p.check_av_roll_fwd() is True

    # The error itself, run: an implementation that strikes R once and holds the annuity
    # it implies.  On the level-rate point that reproduces the model's whole fund path to
    # float noise and still lands on M, which is what makes it invisible there; on the
    # stepping rate it lands ₩6,422,726 short of the 만기보험금.
    def frozen_fund(projection):
        annuity, fund = projection.annuity_pp(0), projection.av_pp_init()
        for t in range(0, projection.annuity_term()):
            fund = fund * (1.0 + projection.crediting_rate(t)) - annuity
        return fund

    level = immediate_annuity.Projection[6]
    assert frozen_fund(level) == pytest.approx(MATURITY_BENEFIT, abs=1e-3)
    assert level.av_pp(10) == pytest.approx(MATURITY_BENEFIT, abs=1e-6)
    assert frozen_fund(p) == pytest.approx(93577273.65, abs=WON)
    assert MATURITY_BENEFIT - frozen_fund(p) == pytest.approx(6422726.35, abs=WON)
    assert abs(MATURITY_BENEFIT - frozen_fund(p)) > 0.06 * MATURITY_BENEFIT


def test_pitfall_the_floor_is_a_rate_on_the_fund_not_a_floor_on_the_annuity(
        immediate_annuity):
    """Pitfall 11: reading the 최저보증이율 as a floor on the annuity.

    It is a rate on the fund.  Point 8 is the demonstration: the annuity falls **50.73%** from
    year 1 to year 11 while the floor is honoured at every step and the fund reaches its
    maturity benefit exactly.  The disputed 2012 contract's own published annuity fell 55.4%
    in five years on the same mechanism.
    """
    p = immediate_annuity.Projection[8]
    assert all(p.crediting_rate(t) == p.min_guar_rate(t)
               for t in range(0, p.proj_len() + 1))
    assert p.annuity_pp(10) / p.annuity_pp(0) - 1.0 == pytest.approx(
        TWO_STEP_FALL, abs=5e-5)
    assert p.annuity_pp(10) < 0.5 * p.annuity_pp(0)
    assert p.av_pp(20) == pytest.approx(MATURITY_BENEFIT, abs=1e-6)
    # The floor never touches the annuity: it is applied to the fund and to nothing else.
    for t in (0, 5, 10, 19):
        assert p.annuity_pp(t) == pytest.approx(
            p.av_pp(t) * p.crediting_rate(t) - p.retention_pp(t), rel=1e-13)
    doc = immediate_annuity.Projection.cells["min_guar_rate"].doc
    assert "never a floor on the annuity" in doc


def test_pitfall_the_floor_bands_are_half_open_in_completed_policy_years(
        immediate_annuity):
    """Pitfall 12: getting the floor's duration bands wrong by one.

    The bands are half-open [dur_from, dur_to) in **completed policy years**, so period t is
    policy year t + 1 and the test is on t: t = 0 … 4 is 1.25%, t = 5 … 9 is 1.00%, t ≥ 10 is
    0.75%.  Testing on t + 1 moves both steps a year early.
    """
    p = immediate_annuity.Projection[8]
    for t, rate in MIN_GUAR_SCHEDULE.items():
        assert p.min_guar_rate(t) == rate, t
    assert p.crediting_rate(4) == 0.0125 and p.crediting_rate(5) == 0.0100
    assert p.crediting_rate(9) == 0.0100 and p.crediting_rate(10) == 0.0075
    assert [p.min_guar_rate(t) for t in range(0, 5)] == [0.0125] * 5
    assert [p.min_guar_rate(t) for t in range(5, 10)] == [0.0100] * 5
    table = pd.read_csv(CSV_DIR / "crediting_table.csv")
    bands = table[table["basis_id"] == "min_guar"][["dur_from", "dur_to"]]
    assert list(bands["dur_from"]) == [0, 5, 10]
    assert list(bands["dur_to"]) == [5, 10, 999]
    with pytest.raises(FormulaError):
        p.min_guar_rate(999)                    # outside every band, and it says so


def test_pitfall_the_annuity_charge_is_not_netted_off_the_payment(kr_immediate_anchor):
    """Pitfall 13: netting the 0.80% 연금수령기간 중 비용 off the policyholder's payment.

    It is disclosed in the **cost** table and not the benefit table, so it is an insurer
    expense measured on the 연금연액 and the annuitant receives the full amount.  Netting it
    would cut the anchor's income by ₩39,584.31 a year and would also break the pricing
    identity, since the fund bought the gross annuity.
    """
    a = kr_immediate_anchor
    for t in range(1, a.proj_len() + 1):
        assert a.expenses(t) == pytest.approx(
            0.0080 * a.annuity_payments(t), rel=1e-13), t
    assert a.expenses(1) == pytest.approx(EXPENSE_CHARGE, abs=SUB_WON)
    assert a.annuity_payments(1) == pytest.approx(a.annuity_pp(1), rel=1e-15)
    # The payment is the gross annuity, and the identity closes on the gross annuity.
    assert a.annuity_pp(0) * (1.0 - 0.0080) < a.annuity_payments(0)
    assert a.check_annuity_basis() is True
    # The charge follows the payment's weight, not the policy count.
    assert a.expenses(20) == pytest.approx(
        0.0080 * a.annuity_pp(20) * a.payment_factor(20), rel=1e-14)
    assert a.expenses(50) == 0.0


def test_pitfall_no_death_benefit_is_paid_on_the_jongsin_yeongeum_hyeong(
        immediate_annuity):
    """Pitfall 14: paying a death benefit on the 종신연금형.

    There is none after annuitisation — 「별도의 사망보험금은 지급되지 않습니다」 — the unpaid
    guaranteed instalments being what survives the annuitant, and they are already inside
    ``annuity_payments``.  Adding one double-counts the guarantee.
    """
    for point_id in (1, 2, 3, 4, 5):
        p = immediate_annuity.Projection[point_id]
        assert p.shape() == "life"
        assert p.db_rate() == 0.0
        assert p.risk_prem_rate() == 0.0        # and no 위험보험료 is deducted for one
        assert p.risk_prem_pp() == 0.0
        assert all(p.claims(t, "DEATH") == 0.0
                   for t in range(0, p.proj_len() + 1)), point_id
        assert p.result_cf()["claims_death"].sum() == 0.0
    a = immediate_annuity.Projection[1]
    # What survives the annuitant is inside the annuity, at a weight of one.
    assert a.payment_factor(5) == 1.0 > a.lives_if(6)
    assert a.annuity_payments(5) == pytest.approx(a.annuity_pp(5), rel=1e-15)


def test_pitfall_the_death_benefit_is_measured_on_the_fund_carried_forward(
        immediate_annuity):
    """Pitfall 15: paying the death benefit on the fund at the start of the period.

    Deaths are taken at the **end**, after the crediting and after the annuity due to the
    survivors, so the 사망보험금 on the inheritance shape is ρP + V(t + 1) and not ρP + V(t).
    On point 6 at t = 0 that is 0.00353 × 105,473,616.05 = ₩372,321.86 rather than
    0.00353 × 105,030,000.00 = ₩370,755.90.
    """
    p = immediate_annuity.Projection[6]
    assert p.claims(0, "DEATH") == pytest.approx(DESIGNED["claims_death"], abs=SUB_WON)
    assert p.claims(0, "DEATH") == pytest.approx(
        0.00353 * (0.10 * p.prem_pp() + p.av_pp(1)), rel=1e-13)
    start_of_period = 0.00353 * (0.10 * p.prem_pp() + p.av_pp(0))
    assert start_of_period == pytest.approx(370755.90, abs=WON)
    assert p.claims(0, "DEATH") - start_of_period == pytest.approx(1565.96, abs=WON)
    # On the certain shape it is the 10% alone: the instalments run on their own dates.
    certain = immediate_annuity.Projection[9]
    assert certain.claims(0, "DEATH") == pytest.approx(
        certain.pols_death(0) * 0.10 * certain.prem_pp(), rel=1e-14)
    assert certain.db_rate() == 0.10


def test_pitfall_no_lapse_decrement_touches_the_life_shape(immediate_annuity):
    """Pitfall 16: applying a lapse decrement to the 종신연금형.

    Surrender is contractually impossible from month one — 「종신연금이 지급개시된 이후에는
    해지할 수 없습니다」 — and on an immediate annuity the annuity begins a month after
    inception, so the contract is irreversible.  A life-shape model point carrying a
    surrender rate is a defect in the table rather than a scenario, and
    ``check_surr_value()`` asserts a nil rate **and** a nil surrender value rather than
    leaving either to the CSV.
    """
    table = immediate_annuity.Data.model_point_table()
    for point_id in (1, 2, 3, 4, 5):
        p = immediate_annuity.Projection[point_id]
        assert p.shape() == "life"
        assert float(table.loc[point_id, "lapse_rate"]) == 0.0
        assert p.check_surr_value() is True, point_id
        assert all(p.lapse_rate(t) == 0.0 for t in range(0, p.proj_len() + 1))
        assert all(p.pols_lapse(t) == 0.0 for t in range(0, p.proj_len() + 1))
        assert all(p.cv_pp(t) == 0.0 for t in range(0, p.proj_len() + 1))
        assert all(p.surr_if(t) == 1.0 for t in range(0, p.proj_len() + 1))
        assert p.result_cf()["claims_lapse"].sum() == 0.0


def test_pitfall_no_surrender_fires_in_the_final_period(immediate_annuity):
    """Pitfall 17: letting a surrender fire in the final period.

    ``lapse_rate(N) = 0`` on every shape.  Without it a contract in its last year is
    surrendered a moment before its 만기보험금 and the maturity benefit is diverted into a
    surrender value of a different amount for no reason any contract states.
    """
    for point_id in (6, 7, 9):
        p = immediate_annuity.Projection[point_id]
        n = p.proj_len()
        assert p.lapse_rate(n - 1) == 0.02
        assert p.lapse_rate(n) == 0.0
        assert p.pols_lapse(n) == 0.0
        assert p.claims(n, "LAPSE") == 0.0, point_id
        assert p.result_cf().loc[n, "claims_lapse"] == 0.0
    inheritance = immediate_annuity.Projection[6]
    assert inheritance.claims(inheritance.proj_len(), "MATURITY") > 0.0
    assert inheritance.cv_pp(inheritance.proj_len() + 1) == pytest.approx(
        MATURITY_BENEFIT, abs=1e-6)          # the two amounts a lapse would confuse


def test_pitfall_the_maturity_benefit_is_weighted_one_period_later(immediate_annuity):
    """Pitfall 18: weighting the 만기보험금 by ``pols_if(N)`` instead of ``pols_if(N + 1)``.

    It is payable on survival **to** maturity, one further period of decrement away:
    ₩79,495,349.97 on point 6, against ₩80,023,013.57 if the earlier weight were used.
    """
    p = immediate_annuity.Projection[6]
    n = p.proj_len()
    assert p.claims(n, "MATURITY") == pytest.approx(
        DISPUTE_TOTALS[6]["claims_maturity"], abs=WON)
    assert p.claims(n, "MATURITY") == pytest.approx(
        p.pols_if(n + 1) * p.maturity_benefit(), rel=1e-14)
    earlier = p.pols_if(n) * p.maturity_benefit()
    assert earlier == pytest.approx(MATURITY_EARLIER_WEIGHT, abs=WON)
    assert earlier - p.claims(n, "MATURITY") == pytest.approx(527663.60, abs=WON)
    assert p.pols_if(n + 1) < p.pols_if(n)


def test_pitfall_the_hundred_point_one_percent_fund_floor_is_not_applied(
        kr_immediate_anchor):
    """Pitfall 19: applying the 100.1%-of-premiums fund floor.

    It is a **deferred**-contract mechanic — the floor on the fund at annuitisation, where a
    premium has been accumulating — and applying it to an immediate annuity would erase the
    entire 3.50% load on day one and make ``check_premium_split()`` fail by ₩3,600,000.
    """
    a = kr_immediate_anchor
    assert a.av_pp_init() == pytest.approx(AV_PP_INIT, abs=SUB_WON)
    assert a.av_pp_init() < a.prem_pp()
    floored = 1.001 * a.prem_pp()
    assert floored - a.av_pp_init() == pytest.approx(3600000.0, abs=WON)
    assert a.check_premium_split() is True
    names = set(a.cells) | set(a.refs)
    for absent in ("av_floor_pp", "av_floor_ratio", "prem_floor_rate", "cv_floor_ratio"):
        assert absent not in names, f"{absent}: a deferred-contract mechanic"


def test_pitfall_nothing_discounted_is_published(immediate_annuity, kr_immediate_anchor):
    """Pitfall 20: discounting the projected flows at the crediting rate and calling it a
    reserve.

    ``disc_factor`` exists for the pricing identity and for ``retention_shortfall_pp()``
    only, both being statements about the **contract's own basis** rather than about value.
    The best estimate discounts on a supervisory curve and the reserve is computed under
    감독규정 제6-11조, neither of which is in this model — so the statement carries no
    discounted column and must not acquire one.
    """
    a = kr_immediate_anchor
    columns = set(a.result_cf().columns) | set(a.result_pols().columns)
    for column in columns:
        assert "disc" not in column and "pv_" not in column, column
        assert not column.startswith("pv") and not column.endswith("_pv"), column
    names = set(immediate_annuity.Projection.cells)
    for absent in ("reserve_pp", "bel_pp", "csm_pp", "result_pv", "disc_rate"):
        assert absent not in names, absent
    assert "disc_factor" in names               # it exists, and is not a column
    doc = immediate_annuity.Projection.cells["disc_factor"].doc.replace("*", "")
    assert "not a valuation rate" in doc
    assert a.disc_factor(0) == 1.0
    assert a.disc_factor(10) == pytest.approx(1.025 ** -10, rel=1e-14)


def test_pitfall_no_aggregate_claims_column_stands_beside_the_split(kr_immediate_anchor):
    """Pitfall 21: publishing a ``claims`` column beside the ``claims_*`` columns.

    A statement must not carry its own subtotal beside its parts, or the columns stop summing
    to ``net_cf``.  The ``claims(t, kind)`` cells stays and the column does not, and
    ``check_net_cf()`` rebuilds the ledger from the **published** columns so that the
    difference is load-bearing rather than stylistic.
    """
    a = kr_immediate_anchor
    df = a.result_cf()
    assert "claims" not in df.columns
    assert [c for c in df.columns if c.startswith("claims")] == [
        "claims_death", "claims_lapse", "claims_maturity"]
    assert a.check_net_cf() is True
    with pytest.raises(FormulaError):
        a.claims(1, "SURRENDER")                # the kind argument validates
    assert a.claims(1, "DEATH") == 0.0


# ---------------------------------------------------------------------------
# The [std] parameters, and the modules asserted in both positions


@pytest.mark.parametrize("shape", sorted(CHARGE_RATES))
def test_the_std_charge_parameters_the_notes_state(immediate_annuity, shape):
    """The charge basis by shape, read off the model rather than off the CSV.

    Every rate here is [std] in its adoption or in its derivation, and a silent change to any
    of them would move a result rather than fail a test without this.  The two that carry the
    product's structure are ``acq_expense_rate``, which is the load less the commission and
    is what makes the premium split close, and ``comm_rate``, which sits **below** the
    계약체결비용 so that the charge covers the commission at the same moment.
    """
    point_id = {"life": 1, "inheritance": 6, "certain": 9}[shape]
    p = immediate_annuity.Projection[point_id]
    assert p.shape() == shape
    for name, value in CHARGE_RATES[shape].items():
        assert getattr(p, name)() == value, name
    assert p.expense_load_rate() == pytest.approx(0.0350, rel=1e-15)
    assert p.acq_expense_rate() == pytest.approx(
        p.expense_load_rate() - p.comm_rate(), rel=1e-15)
    assert p.av_pp_init() / p.prem_pp() == pytest.approx(
        1.0 - 0.0350 - CHARGE_RATES[shape]["risk_prem_rate"], rel=1e-15)


def test_the_std_rate_and_behaviour_assumptions_the_notes_state(immediate_annuity):
    """공시이율 2.50%, 최저보증이율 1.25 / 1.00 / 0.75%, ω = 110, and w = 2.00%.

    The declared rate is a **scalar** and not a derived quantity — 감독규정 제7-65조제3항
    makes it the product of a 공시기준이율 majority-weighted to the insurer's own
    운용자산이익률, which no model can derive — and the limiting age is what makes the
    life-shape obligation exhausted rather than truncated.  The surrender rate is the one row
    of the model's [std] table that is a **placeholder**: no retrieved source gives a rate for
    즉시연금 by duration, by shape or at all, so it is carried as a model point column where
    its effect can be isolated rather than in a table where it would look like a duration
    curve — and it is not second-order, producing ₩15.9m of ``claims_lapse`` on point 6
    against ₩17.3m of annuity payments.
    """
    a = immediate_annuity.Projection[1]
    assert a.decl_rate() == DECL_RATE
    assert [a.min_guar_rate(t) for t in (0, 4, 5, 9, 10)] == [
        0.0125, 0.0125, 0.0100, 0.0100, 0.0075]
    assert immediate_annuity.Projection.refs["omega_age"] == OMEGA_AGE
    table = pd.read_csv(CSV_DIR / "crediting_table.csv")
    assert set(table["basis_id"]) == {"decl_2017", "min_guar"}
    decl = table[table["basis_id"] == "decl_2017"]
    assert set(decl["decl_rate"]) == {DECL_RATE}     # one rate per basis, never a mean
    assert list(decl["min_guar_rate"]) == [0.0125, 0.0100, 0.0075]
    assert set(table[table["basis_id"] == "min_guar"]["decl_rate"]) == {0.0}
    assert table["provenance"].notna().all()
    doc = immediate_annuity.Projection.cells["decl_rate"].doc.replace("*", "")
    assert "It is a scalar and not a derived quantity" in doc

    points = immediate_annuity.Data.model_point_table()
    assert set(points["lapse_rate"]) == {0.0, 0.02}
    for point_id in (6, 7, 8, 9):
        p = immediate_annuity.Projection[point_id]
        assert p.lapse_rate(0) == 0.02
        assert p.shape() in ("inheritance", "certain")
    df = immediate_annuity.Projection[6].result_cf()
    assert df["claims_lapse"].sum() == pytest.approx(15858445.72, abs=WON)
    assert df["claims_lapse"].sum() / df["annuity_payments"].sum() == pytest.approx(
        0.918, abs=5e-4)
    # There is no lapse table: the assumption has nowhere else to hide.
    assert not (CSV_DIR / "lapse_table.csv").exists()
    assert "lapse_rate_mth" not in set(immediate_annuity.Projection.cells)


def test_the_four_optional_modules_are_asserted_in_both_positions(immediate_annuity):
    """The retention, the stepping floor, voluntary surrender and the longer guarantee.

    The anchor exercises none of the four, which is why its numbers are independent of all
    four; a module that is only ever seen switched off is machinery nobody has run, so each
    is asserted in the position the anchor holds it in **and** on the point that exercises it.
    """
    a = immediate_annuity.Projection[1]
    # 1. The retention: inert on the anchor, and both bases on points 6 and 7.
    assert all(a.retention_pp(t) == 0.0 for t in range(0, a.proj_len() + 1))
    assert immediate_annuity.Projection[6].retention_pp(0) > 0.0
    assert immediate_annuity.Projection[7].retention_pp(0) == 0.0
    # 2. The stepping floor: inert on the anchor, binding at every duration on point 8.
    assert all(a.crediting_rate(t) == a.decl_rate() for t in range(0, a.proj_len() + 1))
    stepping = immediate_annuity.Projection[8]
    assert len({stepping.crediting_rate(t)
                for t in range(0, stepping.proj_len() + 1)}) == 3
    # 3. Voluntary surrender: off by contract on the anchor, on for points 6 to 9.
    assert all(a.pols_lapse(t) == 0.0 for t in range(0, a.proj_len() + 1))
    assert immediate_annuity.Projection[9].pols_lapse(0) == pytest.approx(0.02)
    # 4. The longer guarantee: ten years on the anchor, twenty on point 3.
    longer = immediate_annuity.Projection[3]
    assert a.annuity_term() == 10 and longer.annuity_term() == 20
    assert longer.annuity_factor() > a.annuity_factor()
    assert longer.annuity_pp(0) < a.annuity_pp(0)
    assert all(longer.pols_if(t) == 1.0 for t in range(0, 20))
    assert longer.pols_exit(19) == pytest.approx(
        longer.pols_if_init() - longer.lives_if(20), rel=1e-14)
    assert longer.pols_if(20) == pytest.approx(longer.lives_if(20), rel=1e-15)


def test_the_model_point_table_exercises_the_product(immediate_annuity):
    """Both sexes, all three shapes, both retention bases, both crediting bases.

    The table is the model's coverage statement, so what it must contain is asserted here
    rather than left to a reader counting rows.  The premium envelope runs from the
    ₩10,000,000 carrier minimum through the ₩100,000,000 median and tax cap to the
    ₩5,000,000,000 maximum, and the issue ages span the 45–80 band.
    """
    table = immediate_annuity.Data.model_point_table()
    assert len(table) == 10 and list(table.index) == list(range(1, 11))
    assert set(table["sex"]) == {"M", "F"}
    assert set(table["shape"]) == {"life", "inheritance", "certain"}
    assert set(table["retention_basis"]) == {"as_designed", "as_ordered"}
    assert set(table["crediting_basis"]) == {"decl_2017", "min_guar"}
    assert table["age_at_entry"].min() == 45 and table["age_at_entry"].max() == 80
    assert table["prem_pp"].min() == 10000000
    assert table["prem_pp"].max() == 5000000000
    assert set(table["annuity_term"]) == {10, 20, 30}
    assert set(table["pols_if_init"]) == {1.0}
    # Points 6 and 7 are the same contract, which is what makes the panel a comparison.
    assert (table.loc[6].drop(["policy_id", "retention_basis"]).tolist()
            == table.loc[7].drop(["policy_id", "retention_basis"]).tolist())


def test_the_docstrings_carry_this_products_own_reference_material(immediate_annuity):
    """Product-specific phrases a reader relies on, which a generic sweep cannot know.

    The model docstring names the payout-phase chassis and the three shapes; the Projection
    docstring carries the notes' symbol map, the 보험나이 basis and the four names that
    needed care; and the Data docstring explains why there is no lapse table, no
    surrender-value schedule and no commission scale.  Asserted so that they cannot go stale
    silently while the numbers stay right.
    """
    doc = immediate_annuity.doc
    for phrase in ("mechanics demonstration", "external", "once per model",
                   "no acquisition strain", "종신연금형", "상속연금형", "확정기간연금형",
                   "즉시연금 과소지급"):
        assert phrase in doc, phrase
    proj = immediate_annuity.Projection.doc
    assert "Notes symbol" in proj
    for cells in ("proj_len", "model_point", "pols_if", "annuity_pp", "retention_pp",
                  "payment_factor", "av_pp", "annuity_factor", "crediting_rate",
                  "retention_shortfall_pp"):
        assert cells in proj, cells
    assert "payment obligation remains" in proj
    assert "보증지급기간" in proj and "산출방법서" in proj
    data = immediate_annuity.Data.doc
    assert "TradLife_A" in data
    for cells in ("input_dir", "model_point_table", "mort_table", "charge_table",
                  "crediting_table"):
        assert cells in data, cells
    assert "no lapse table" in data
