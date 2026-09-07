"""Golden and structural tests for Term_KR_A.

The golden values are the worked example in
products/term_life/technical-notes.md ("Worked example"), which projects the anchor cell
M40 / 20년만기 전기납 / 비갱신형 / KRW 100,000,000 of cover / KRW 15,080 a month — the cell
that is doubly prescribed in Korea, being both the 감독규정 기준연령 요건 and the
생명보험협회 disclosure's 대표계약, so its premium is a published figure rather than a
standardization.  They are hard-coded here rather than pickled so that a reviewer can
compare them against the notes by eye.

Tolerances follow the precision the notes display: money to the won's second decimal,
in-force and the exit split to the ten decimals the notes print them at, and the decrement
rates to the eight the basis table prints.

The 갱신형 (*gaengsinhyeong*, renewable) panel is asserted beside the anchor, because the
mechanic that makes this the library's protection chassis does not appear on the anchor
cell at all: model points 3 and 4 are one policy on the two contract-boundary readings, and
the published renewal ladder — 9,000 -> 21,000 -> 56,000 -> 201,000 won a month — is a
sourced quantity in Korea where it is a standardization everywhere else in this repository.

Beyond the worked example this module asserts every product fact the notes list under
"Known modeling pitfalls", because each of them is a way an implementation can look right
and be wrong.  There is one ``test_pitfall_*`` per bullet, naming the pitfall in its
docstring: the renewal decline that is not lapse and whose processing order is not
cosmetic; truncation that shortens the **cycle** and not the horizon; a 비갱신형 contract
that never renews; a premium indexed by the renewal cycle and not by the policy year; a
premium waiver that does not survive a 갱신 where the suicide and contestability clocks do;
a waiver incidence that must not be scaled off ``mort_rate``; a 재해사망 uplift that splits
the death decrement rather than adding one; a lapse that pays nothing and a zero that must
be published rather than inferred; a 전기납 resolution that couples ``pay_term`` to the
contract boundary; a ``qbar`` built on **table** rates and not best-estimate ones; a premium
that rounds to 10 won *before* annualization and an annualization exact in amount and
standardized only in timing; a 선지급 cap reached exactly at the anchor and an accelerated
amount taken out of the death benefit rather than beside it; a 부활 pool carried by vintage
that renewal declines never enter; tables read at 보험나이 and at nothing else; a 장해 state
that is not a benefit, Korea having no 高度障害保険金 analogue; and the absence of a
``claims`` aggregate column beside the split ones.

The seven ``check_*`` cells are asserted **by name**, because a generic sweep cannot notice
a check that has quietly disappeared, and the [std] scalar assumptions are read off the
model so that a silent change to an assumption fails a test rather than moving a result.
The whole-table sweep belongs to ``test_model_conventions_kr.py``; the model points taken
here are the ones that exercise a particular mechanic.
"""
import modelx as mx
import pandas as pd
import pytest
from modelx.core.errors import FormulaError

from kr_registry import LIB, MODELS

WON = 0.005          # money displayed to 2 d.p.
INFORCE = 5e-11      # in-force and exit counts, displayed to 10 d.p.
RATE = 5e-9          # the decrement basis table's rates, displayed to 8 d.p.

MODEL_DIR = LIB / MODELS["Term_KR_A"][0]
CSV_DIR = MODEL_DIR.parent

# ---------------------------------------------------------------------------
# The notes' worked example, anchor cell (point_id = 1)

# "The decrement basis, year by year": t -> (보험나이, q_x^tab, q(t), w(t), l(t)).
WORKED_EXAMPLE_BASIS = {
    1:  (40, 0.00065000, 0.00055250, 0.0460000000, 1.0000000000),
    2:  (41, 0.00069504, 0.00059078, 0.0376048847, 0.9534729150),
    3:  (42, 0.00074482, 0.00063310, 0.0307418990, 0.9170755621),
    4:  (43, 0.00079985, 0.00067987, 0.0251314254, 0.8883201687),
    5:  (44, 0.00086067, 0.00073157, 0.0205448773, 0.8654066502),
    6:  (45, 0.00092789, 0.00078871, 0.0167953857, 0.8470068787),
    7:  (46, 0.00100219, 0.00085186, 0.0137301857, 0.8321242517),
    8:  (47, 0.00108431, 0.00092166, 0.0112243924, 0.8199999093),
    9:  (48, 0.00117508, 0.00099882, 0.0091759127, 0.8100486275),
    10: (49, 0.00127541, 0.00108410, 0.0075012856, 0.8018140251),
    11: (50, 0.00138630, 0.00117836, 0.0061322822, 0.7949366641),
    12: (51, 0.00150887, 0.00128254, 0.0050131253, 0.7891309148),
    13: (52, 0.00164435, 0.00139770, 0.0040982174, 0.7841678848),
    14: (53, 0.00179408, 0.00152497, 0.0033502824, 0.7798626566),
    15: (54, 0.00195959, 0.00166565, 0.0027388475, 0.7760646153),
    16: (55, 0.00214252, 0.00182114, 0.0022390010, 0.7726499798),
    17: (56, 0.00234471, 0.00199300, 0.0018303777, 0.7695160610),
    18: (57, 0.00256820, 0.00218297, 0.0014963292, 0.7665767149),
    19: (58, 0.00281521, 0.00239293, 0.0012232453, 0.7637587538),
    20: (59, 0.00308823, 0.00262500, 0.0010000000, 0.7609991050),
}

# "The cash flow statement, t = 1..20": t -> (pols_if, premiums, claims_death,
# claim_expenses, expenses, commissions, net_cf).  The four other claims_* columns are
# 0.00 in every row of this model point; the notes say so and the row test asserts it.
WORKED_EXAMPLE_CF = {
    1:  (1.0000000000, 180960.00,  55250.00, 165.75, 144000.00, 108576.00, -127031.75),
    2:  (0.9534729150, 172540.46,  56329.65, 168.99,  23341.02,   5176.21,   87524.58),
    3:  (0.9170755621, 165953.99,  58059.78, 174.18,  22899.01,   4978.62,   79842.41),
    4:  (0.8883201687, 160750.42,  60394.45, 181.18,  22624.62,   4822.51,   72727.66),
    5:  (0.8654066502, 156603.99,  63310.51, 189.93,  22481.86,   4698.12,   65923.57),
    6:  (0.8470068787, 153274.36,  66803.98, 200.41,  22443.94,   4598.23,   59227.80),
    7:  (0.8321242517, 150581.20,  70885.46, 212.66,  22490.57,   4517.44,   52475.08),
    8:  (0.8199999093, 148387.18,  75576.40, 226.73,  22606.13,   4451.62,   45526.31),
    9:  (0.8100486275, 146586.40,  80909.12, 242.73,  22778.43,   4397.59,   38258.54),
    10: (0.8018140251, 145096.27,  86924.54, 260.77,  22997.81,   4352.89,   30560.26),
    11: (0.7949366641, 143851.74,  93671.76, 281.02,  23256.56,   4315.55,   22326.85),
    12: (0.7891309148, 142801.13, 101209.16, 303.63,  23548.44,   4284.03,   13455.87),
    13: (0.7841678848, 141903.02, 109602.95, 328.81,  23868.35,   4257.09,    3845.82),
    14: (0.7798626566, 141123.95, 118926.56, 356.78,  24212.05,   4233.72,   -6605.16),
    15: (0.7760646153, 140436.65, 129265.32, 387.80,  24576.02,   4213.10,  -18005.58),
    16: (0.7726499798, 139818.74, 140710.53, 422.13,  24957.24,   4194.56,  -30465.73),
    17: (0.7695160610, 139251.63, 153364.82, 460.09,  25353.14,   4177.55,  -44103.97),
    18: (0.7665767149, 138719.72, 167341.40, 502.02,  25761.42,   4161.59,  -59046.71),
    19: (0.7637587538, 138209.78, 182762.01, 548.29,  26180.05,   4146.29,  -75426.86),
    20: (0.7609991050, 137710.40, 199761.92, 599.29,  26607.17,   4131.31,  -93389.29),
}

# "Load-bearing values at full float64 precision", printed in the notes so that a reader
# reconciling to the model rather than to the rounded table has something exact to
# reconcile to.  claims_death(1) is carried as the float the notes print, not as 55,250.
FULL_PRECISION = {
    "pols_if(2)": 0.953472915,
    "pols_if(3)": 0.917075562112279,
    "pols_if(10)": 0.8018140250566161,
    "pols_if(20)": 0.7609991050099496,
    "premiums(2)": 172540.4586984,
    "claims_death(1)": 55249.99999999999,
    "claim_expenses(1)": 165.74999999999997,
    "expenses(1)": 144000.0,
    "commissions(1)": 108576.0,
    "net_cf(1)": -127031.75,
    "net_cf(2)": 87524.5847539274,
    "net_cf(3)": 79842.40590172037,
    "net_cf(10)": 30560.25860988572,
    "net_cf(12)": 13455.869541227945,
    "net_cf(20)": -93389.29024513016,
}

TOTAL_POLS_IF = 16.4929323384
TOTAL_PREMIUMS = 2984561.04
TOTAL_CLAIMS_DEATH = 2071060.31
TOTAL_CLAIM_EXPENSES = 6213.18
TOTAL_EXPENSES = 596983.81
TOTAL_COMMISSIONS = 192684.03
TOTAL_NET_CF = 117619.70
TOTAL_POLS_DEATH = 0.0207106031
TOTAL_POLS_LAPSE = 0.2210469126
POLS_MATURITY_20 = 0.7582424843

# The published 갱신형 ladder: (cycle k, first policy year, attained 보험나이, P_m, P_a).
RENEWAL_LADDER = [
    (1,  1, 40,   9000.0,  108000.0),
    (2, 11, 50,  21000.0,  252000.0),
    (3, 21, 60,  56000.0,  672000.0),
    (4, 31, 70, 201000.0, 2412000.0),
]

# The notes' boundary-row table for model point 3, the long boundary reading:
# t -> (pols_if, renewal_decline_rate, pols_decline, wop_waived_frac, net_cf).
GAENGSIN_BOUNDARY_ROWS = {
    9:  (0.7571341236, 0.0, 0.0000000000, 0.0063821086,  -18330.11),
    10: (0.7405136863, 0.2, 0.1451293946, 0.0071770030,  -24739.94),
    11: (0.5805175782, 0.0, 0.0000000000, 0.0000000000,   56307.38),
    20: (0.5126702892, 0.2, 0.1015364175, 0.0071770030,  -28486.45),
    21: (0.4061456699, 0.0, 0.0000000000, 0.0000000000,  132875.76),
    30: (0.3743068750, 0.2, 0.0741053844, 0.0071770030,  -53389.60),
    31: (0.2964215375, 0.0, 0.0000000000, 0.0000000000,  434066.03),
    40: (0.2588401346, 0.0, 0.0000000000, 0.0071770030,   17271.43),
}

YEAR_10_EXITS = (0.0008027898, 0.0140639237, 0.1451293946)   # deaths, lapses, declines
GAENGSIN_TOTAL_NET_CF = 2976124.30
CURRENT_TERM_NET_CF = -179423.24
GAENGSIN_FIRST_TEN_NET_CF = -170638.50
WAIVED_AT_CYCLE_END = 0.0071770029564316665

# "The other eight shipped model points, undiscounted":
# pid -> (proj_len, premium_mth_pp(1), premiums, all claims, net_cf).
POINT_SUMMARY = {
    1:  (20,  15080.0,  2984561.04,  2071060.31,   117619.70),
    2:  (20,   8010.0,  1591097.71,  1068175.07,  -181709.67),
    3:  (40,   9000.0, 11602888.01,  7395004.02,  2976124.30),
    4:  (10,   9000.0,   975113.10,   704034.28,  -179423.24),
    5:  (20,   6620.0,   720742.73,   510526.26,  -486000.29),
    6:  (20,  44250.0,  8750021.45,  8743053.57, -1161992.41),
    7:  (15,  40040.0,  5928269.28,  3854803.57,  1122485.11),
    8:  (30,  15640.0,  4582634.96,  3182705.30,   249585.36),
    9:  (35, 109490.0, 21719050.30, 13708083.40,  5558126.05),
    10: (20,  49480.0,  9643343.42,  6726143.18,  1681748.06),
}

MORT_BE_SENSITIVITY = {0.75: 361807.55, 0.85: 117619.70, 1.00: -247394.11}
LAPSE_BE_SENSITIVITY = {0.5: 116375.66, 1.0: 117619.70, 2.0: 114628.90}
DECLINE_SENSITIVITY = {                      # d -> (net_cf, premium income)
    0.00: (5655717.05, 19813117.38),
    0.05: (4880486.34, 17459448.71),
    0.20: (2976124.30, 11602888.01),
    0.40: (1285094.11,  6237291.04),
}

CHECKS = {
    "check_pols_roll_fwd", "check_lapse_pool", "check_pols_payer", "check_prem_level",
    "check_decline_timing", "check_waiver_reset", "check_net_cf",
}
CHECKS_WITH_RESID = {
    "check_pols_roll_fwd", "check_lapse_pool", "check_pols_payer", "check_prem_level",
    "check_net_cf",
}

# The scalar assumptions the notes tabulate; every one of them [std].
STD_SCALARS = {
    "mort_be_factor": 0.85, "lapse_be_factor": 1.0, "prem_int_rate": 0.025,
    "renewal_decline_base": 0.20, "renewal_decline_beta": 0.0,
    "renewal_decline_max": 0.40, "expense_acq": 120000.0, "expense_maint": 24000.0,
    "expense_claim": 300000.0, "inflation_rate": 0.02, "comm_init_rate": 0.60,
    "comm_renewal_rate": 0.03, "comm_new_term_rate": 0.0, "accel_cap": 50000000.0,
    "accel_full_limit": 10000000.0, "accel_share_max": 0.5, "accel_take_up": 0.10,
    "wop_inc_rate": 0.0008, "wop_rec_rate": 0.0, "reinstate_rate": 0.10,
}

# The diagnostic qbar values the notes publish as "checkable from the shipped table".
QBAR_DIAGNOSTICS = {
    ("M", 40, 20): 0.00152337, ("F", 40, 20): 0.00077569, ("M", 30, 20): 0.00070037,
    ("M", 65, 15): 0.01348403, ("F", 45, 35): 0.00370477, ("M", 19, 30): 0.00053910,
    ("M", 55, 20): 0.00655454,
}

# The three 예정 경험사망률 rates per sex that every 상품요약서 must print, and which the
# shipped Makeham law is fitted to exactly.
SOURCED_ANCHORS = {
    ("M", 20): 0.000280, ("M", 40): 0.000650, ("M", 60): 0.003390,
    ("F", 20): 0.000200, ("F", 40): 0.000430, ("F", 60): 0.001390,
}


def _reread(suffix):
    """A private copy of the model, for tests that move a Reference."""
    return mx.read_model(MODEL_DIR, name="Term_KR_A_" + suffix)


def _totals(projection):
    """(premiums, all benefit outgo, net_cf) summed over a projection's result_cf()."""
    df = projection.result_cf()
    claims = df[[c for c in df.columns if c.startswith("claims_")]].sum().sum()
    return df["premiums"].sum(), claims, df["net_cf"].sum()


# ---------------------------------------------------------------------------
# The worked example — the decrement basis


@pytest.mark.parametrize("t", sorted(WORKED_EXAMPLE_BASIS))
def test_worked_example_decrement_basis_row(kr_term_anchor, t):
    """Every cell of the notes' twenty-row decrement basis table, at its own precision.

    Every won in the cash flow statement is built from this table, so a drift in any one of
    its four columns would move the whole statement without any single printed figure
    obviously being wrong.
    """
    age, q_tab, q, w, pols = WORKED_EXAMPLE_BASIS[t]
    a = kr_term_anchor
    assert a.age(t) == age
    assert a.mort_rate_at_age(age) == pytest.approx(q_tab, abs=RATE)
    assert a.mort_rate(t) == pytest.approx(q, abs=RATE)
    assert a.lapse_rate(t) == pytest.approx(w, abs=INFORCE)
    assert a.pols_if(t) == pytest.approx(pols, abs=INFORCE)


def test_worked_example_the_lapse_curve_is_the_prescribed_shape(term_life,
                                                               kr_term_anchor):
    """w(t) = 0.046 (0.001/0.046)^((t-1)/19), from three disclosed endpoints.

    The endpoints are published 적용해지율 figures and the log-linear interpolation between
    them is the 계리가정 가이드라인's 원칙모형 for 무·저해지 business, so the whole curve is
    checkable rather than chosen — which is unique in this repository.  The file therefore
    ships three rows, not a fitted curve: a CSV holding the curve would hide which two
    numbers are sourced.
    """
    table = term_life.Data.lapse_table()
    assert list(table.index) == ["in_payment_start", "in_payment_end", "post_payment"]
    assert float(table.loc["in_payment_start", "lapse_rate"]) == 0.046
    assert float(table.loc["in_payment_end", "lapse_rate"]) == 0.001
    assert float(table.loc["post_payment", "lapse_rate"]) == 0.008
    assert table["provenance"].notna().all()

    a = kr_term_anchor
    assert a.lapse_be_factor == 1.0 and a.pay_term() == 20 == a.proj_len()
    for t in range(1, 21):
        assert a.lapse_rate(t) == pytest.approx(
            0.046 * (0.001 / 0.046) ** ((t - 1.0) / 19.0), rel=1e-13)
    rates = [a.lapse_rate(t) for t in range(1, 21)]
    assert rates[0] == pytest.approx(0.046, rel=1e-14)
    assert rates[-1] == pytest.approx(0.001, rel=1e-14)
    assert rates == sorted(rates, reverse=True) and 0.008 not in rates
    # The two means the notes quote for this cell.
    assert sum(rates) / 20.0 == pytest.approx(0.012379, abs=5e-7)
    assert (sum(a.pols_if(t) * a.lapse_rate(t) for t in range(1, 21))
            / sum(a.pols_if(t) for t in range(1, 21))) == pytest.approx(
                0.013413, abs=5e-7)


# ---------------------------------------------------------------------------
# The worked example — the cash flow statement


@pytest.mark.parametrize("t", sorted(WORKED_EXAMPLE_CF))
def test_worked_example_cash_flow_row(kr_term_anchor, t):
    """Every cell of the notes' twenty-row statement, off the cells and off the frame.

    Both, because a column construction error would otherwise hide behind correct cells and
    a cells error behind a correct frame.  The four columns the notes omit from the printed
    table are asserted here too: they are published columns whose zeros the notes state
    rather than imply.
    """
    a = kr_term_anchor
    row = a.result_cf().loc[t]
    cells = (a.pols_if(t), a.premiums(t), a.claims(t, "DEATH"), a.claim_expenses(t),
             a.expenses(t), a.commissions(t), a.net_cf(t))
    columns = ("pols_if", "premiums", "claims_death", "claim_expenses", "expenses",
               "commissions", "net_cf")
    for got, column, expected, tol in zip(
            cells, columns, WORKED_EXAMPLE_CF[t], (INFORCE,) + (WON,) * 6):
        assert got == pytest.approx(expected, abs=tol), column
        assert row[column] == pytest.approx(expected, abs=tol), column
    for zero in ("claims_acc_death", "claims_accel", "claims_maturity", "claims_lapse"):
        assert row[zero] == 0.0, f"{zero} is not zero at t={t}"


def test_worked_example_assumption_table(kr_term_anchor):
    """"Every assumption value the cell uses", asserted off the model rather than described.

    The premium half of the notes' table is **sourced** — 15,080 won a month appears
    independently in the carrier's 상품요약서 grid and in the cross-carrier disclosure,
    agreeing to the won — and the decrement half is a standardization: q(t) = 0.85 x c_q x
    q_x^tab, with c_q = 1 on a 표준체 point.  That asymmetry is the shape of every Korean
    product document here, so both halves are pinned, and the decomposition is asserted
    rather than only the product: a model that folded ``mort_be_factor`` into the shipped
    table would reproduce every golden and would then move the premium scale with it.
    """
    a = kr_term_anchor
    assert (a.sex(), a.age_at_entry(), a.renewal_type()) == ("M", 40, "bi_gaengsin")
    assert (a.rate_class(), a.maturity_form()) == ("standard", "pure")
    assert (a.policy_term(), a.pay_term(), a.proj_len()) == (20, 20, 20)
    assert a.sum_assured() == 100000000.0 and a.contract_boundary() == "ceiling"
    assert (a.acc_death(), a.waiver(), a.accel(), a.reinstatement()) == (
        False, False, False, False)
    assert a.prem_rate_mth(1) == 15080.0 and a.class_prem_ratio() == 1.0
    assert a.pay_factor(1) == 1.0
    assert a.premium_mth_pp(1) == 15080.0 and a.prem_pp(1) == 180960.0
    assert a.mort_be_factor == 0.85 and a.class_mort_ratio() == 1.0
    assert a.mort_rate_at_age(40) == 0.000650     # a disclosed anchor, to the digit
    for t in sorted(WORKED_EXAMPLE_BASIS):
        assert a.mort_rate_base(t) == pytest.approx(
            a.mort_rate_at_age(a.age(t)), rel=1e-14)
        assert a.mort_rate(t) == pytest.approx(
            0.85 * a.mort_rate_at_age(a.age(t)), rel=1e-14)
    for cells in (a.renewal_decline_rate, a.wop_waived_frac, a.accel_share,
                  a.pols_reinstate):
        assert all(cells(t) == 0.0 for t in range(1, 21)), cells


def test_worked_example_full_precision_values(kr_term_anchor):
    """The fifteen full-float64 values the notes print beneath the rounded statement.

    They exist so that a reader reconciling to the model has something exact to reconcile
    to, which makes them a promise about the arithmetic and not only about the display.
    """
    a = kr_term_anchor
    got = {
        "pols_if(2)": a.pols_if(2), "pols_if(3)": a.pols_if(3),
        "pols_if(10)": a.pols_if(10), "pols_if(20)": a.pols_if(20),
        "premiums(2)": a.premiums(2), "claims_death(1)": a.claims(1, "DEATH"),
        "claim_expenses(1)": a.claim_expenses(1), "expenses(1)": a.expenses(1),
        "commissions(1)": a.commissions(1), "net_cf(1)": a.net_cf(1),
        "net_cf(2)": a.net_cf(2), "net_cf(3)": a.net_cf(3),
        "net_cf(10)": a.net_cf(10), "net_cf(12)": a.net_cf(12),
        "net_cf(20)": a.net_cf(20),
    }
    for name, expected in FULL_PRECISION.items():
        assert got[name] == pytest.approx(expected, rel=1e-14, abs=1e-9), name
    assert a.pols_if(21) == 0.0
    assert all(a.prem_pp(t) == 180960.0 for t in range(1, 21))


# ---------------------------------------------------------------------------
# The worked example — the hand traces


def test_worked_example_year_one_trace(kr_term_anchor):
    """The notes' year-one hand trace, line by line: the acquisition strain.

    Year-one outgo is 307,991.75 won against 180,960.00 of premium, and the acquisition
    charge alone — 120,000 of expense plus 108,576 of commission — is 126% of the year's
    premium.  That is the strain the protection shape starts from, and it is why the first
    three lapse rates decide how long the strain takes to recover.
    """
    a = kr_term_anchor
    assert a.pols_if_init() == 1.0 and a.pols_if(1) == 1.0
    assert a.prem_payable(1) == 1.0 and a.wop_waived_frac(1) == 0.0
    assert a.pols_payer(1) == 1.0
    assert a.premiums(1) == pytest.approx(180960.00, abs=WON)
    assert a.pols_death(1) == pytest.approx(0.0005525, rel=1e-14)
    assert a.claims(1, "DEATH") == pytest.approx(
        100000000.0 * (1 - 0.0) * 0.0005525, rel=1e-14)
    assert a.claim_expenses(1) == pytest.approx(300000.0 * 0.0005525, rel=1e-14)
    assert a.expenses(1) == pytest.approx(120000.0 + 24000.0 * 1.02 ** 0, abs=WON)
    assert a.comm_init_pp() == pytest.approx(0.60 * 180960.0, abs=WON)
    assert a.net_cf(1) == pytest.approx(
        180960.00 - 55250.00 - 165.75 - 144000.00 - 108576.00, abs=1e-9)
    outgo = a.claims(1) + a.claim_expenses(1) + a.expenses(1) + a.commissions(1)
    assert outgo == pytest.approx(307991.75, abs=WON)
    assert (120000.0 + 108576.0) / a.premiums(1) == pytest.approx(1.263, abs=5e-4)


def test_worked_example_year_one_roll_forward(kr_term_anchor):
    """The notes' year-one roll-forward, in the processing order and no other.

    After mortality 1 x (1 - 0.0005525); then w(1) = 0.046 exactly on the survivors of it,
    giving a lapse of 0.045974585 and l(2) = 0.953472915.  d(1) = 0 on a 비갱신형 point, and
    neither a reinstatement nor a maturity moves the year.
    """
    a = kr_term_anchor
    assert a.pols_if_at(1, "BEF_DECR") == 1.0
    assert a.pols_if_at(1, "BEF_LAPSE") == pytest.approx(0.9994475, rel=1e-14)
    assert a.pols_lapse(1) == pytest.approx(0.045974585, rel=1e-12)
    assert a.pols_if_at(1, "BEF_DECLINE") == pytest.approx(0.9994475 * 0.954, rel=1e-14)
    assert a.renewal_decline_rate(1) == 0.0
    assert a.pols_if_at(1, "AFT_DECR") == a.pols_if_at(1, "BEF_DECLINE")
    assert a.pols_reinstate(1) == 0.0 and a.pols_maturity(1) == 0.0
    assert a.pols_if(2) == pytest.approx(0.953472915, rel=1e-15)


def test_worked_example_years_two_and_three_traces(kr_term_anchor):
    """The notes' year-two and year-three traces: ordinary years, with no acquisition in them.

    ``expense_acq`` and ``comm_init_pp`` are t = 1 only, and the commission is three per
    cent of *premium income* rather than of ``prem_pp``, so it is already net of any waived
    fraction.  Year three carries the inflation factor squared, which is the cheapest way
    to catch an off-by-one in the exponent that year two alone cannot distinguish.
    """
    a = kr_term_anchor
    assert a.premiums(2) == pytest.approx(180960.0 * 0.953472915, rel=1e-14)
    assert a.pols_death(2) == pytest.approx(0.00056329654262, rel=1e-11)
    assert a.claims(2, "DEATH") == pytest.approx(56329.65426154, abs=1e-6)
    assert a.claim_expenses(2) == pytest.approx(168.98896278, abs=1e-7)
    assert a.inflation_factor(2) == pytest.approx(1.02, rel=1e-15)
    assert a.expenses(2) == pytest.approx(24480.0 * 0.953472915, rel=1e-14)
    assert a.commissions(2) == pytest.approx(0.03 * a.premiums(2), rel=1e-14)
    assert a.commissions(2) == pytest.approx(5176.21376095, abs=1e-6)
    assert a.net_cf(2) == pytest.approx(87524.58475393, abs=1e-6)
    assert a.pols_if_at(2, "BEF_LAPSE") == pytest.approx(0.95290961845738, abs=5e-13)
    assert a.pols_lapse(2) == pytest.approx(0.03583405634511, abs=5e-13)
    assert a.pols_if(3) == pytest.approx(0.917075562112279, rel=1e-15)

    assert a.premiums(3) == pytest.approx(165953.99371984, abs=1e-6)
    assert a.pols_death(3) == pytest.approx(0.00058059778715, abs=5e-13)
    assert a.claims(3, "DEATH") == pytest.approx(58059.77871466, abs=1e-6)
    assert a.claim_expenses(3) == pytest.approx(174.17933614, abs=1e-7)
    assert a.inflation_factor(3) == pytest.approx(1.02 ** 2, rel=1e-15)
    assert a.expenses(3) == pytest.approx(24969.60 * 0.917075562112279, rel=1e-13)
    assert a.commissions(3) == pytest.approx(4978.61981160, abs=1e-6)
    assert a.net_cf(3) == pytest.approx(79842.40590172, abs=1e-6)


def test_worked_example_year_twenty_trace_and_the_maturity_that_pays_nothing(
        kr_term_anchor):
    """The notes' final-year trace, where the 순수보장형 pays nothing at maturity.

    w(20) = 0.001 exactly — the disclosed convergence point, reached at 납입완료 — and
    ``pols_maturity(20)`` then removes the **entire** surviving cohort, 0.7582424843 of it,
    for no benefit at all.  l(21) = 0 exactly, which is what makes the roll-forward close in
    the last year rather than leaving a residual a model with no maturity term would carry.
    """
    a = kr_term_anchor
    assert a.premiums(20) == pytest.approx(137710.39804260, abs=1e-6)
    assert a.pols_death(20) == pytest.approx(0.00199761922616, abs=5e-13)
    assert a.claims(20, "DEATH") == pytest.approx(199761.92261551, abs=1e-6)
    assert a.claim_expenses(20) == pytest.approx(599.28576785, abs=1e-7)
    assert a.expenses(20) == pytest.approx(
        24000.0 * 1.02 ** 19 * a.pols_if(20), rel=1e-13)
    assert a.commissions(20) == pytest.approx(4131.31194128, abs=1e-6)
    assert a.net_cf(20) == pytest.approx(-93389.29024513, abs=1e-6)
    assert a.pols_if_at(20, "BEF_LAPSE") == pytest.approx(0.75900148578379, abs=5e-13)
    assert a.pols_if_at(20, "AFT_DECR") == pytest.approx(0.75824248429801, abs=5e-13)
    assert a.pols_maturity(20) == pytest.approx(POLS_MATURITY_20, abs=INFORCE)
    assert a.pols_maturity(20) == a.pols_if_at(20, "AFT_DECR") + a.pols_reinstate(20)
    assert a.maturity_form() == "pure" and a.claims(20, "MATURITY") == 0.0
    assert a.cum_prem_pp(20) == 3619200.0        # what a rop point would have paid
    assert a.pols_if(21) == 0.0
    assert a.check_pols_roll_fwd_resid(20) == pytest.approx(0.0, abs=1e-15)
    assert all(a.pols_maturity(t) == 0.0 for t in range(1, 20))


# ---------------------------------------------------------------------------
# The worked example — totals, decomposition and shape


def test_worked_example_totals(kr_term_anchor):
    """The notes' undiscounted twenty-year totals, column by column.

    Including the exposure column, which is what the per-policy expense and commission
    figures are proportional to and so the one total a reader can re-derive the others from
    by hand.
    """
    df = kr_term_anchor.result_cf()
    assert df["pols_if"].sum() == pytest.approx(TOTAL_POLS_IF, abs=INFORCE)
    assert df["premiums"].sum() == pytest.approx(TOTAL_PREMIUMS, abs=WON)
    assert df["claims_death"].sum() == pytest.approx(TOTAL_CLAIMS_DEATH, abs=WON)
    assert df["claim_expenses"].sum() == pytest.approx(TOTAL_CLAIM_EXPENSES, abs=WON)
    assert df["expenses"].sum() == pytest.approx(TOTAL_EXPENSES, abs=WON)
    assert df["commissions"].sum() == pytest.approx(TOTAL_COMMISSIONS, abs=WON)
    assert df["net_cf"].sum() == pytest.approx(TOTAL_NET_CF, abs=WON)
    for zero in ("claims_acc_death", "claims_accel", "claims_maturity", "claims_lapse"):
        assert df[zero].sum() == 0.0


def test_worked_example_cohort_decomposition(kr_term_anchor):
    """Deaths, lapses, maturities and the residual in force sum to one policy, exactly.

    The roll-forward read as a cohort decomposition: of a hundred policies issued, 2.07
    die, 22.10 lapse and 75.82 reach the end of the twenty years, with no renewal decline
    on this point at all.  A model losing or creating lives fails here even where every
    single year's residual is inside tolerance, because the errors accumulate.
    """
    a = kr_term_anchor
    deaths = sum(a.pols_death(t) for t in range(1, 21))
    lapses = sum(a.pols_lapse(t) for t in range(1, 21))
    declines = sum(a.pols_decline(t) for t in range(1, 21))
    maturities = sum(a.pols_maturity(t) for t in range(1, 21))
    reinstates = sum(a.pols_reinstate(t) for t in range(1, 21))
    assert deaths == pytest.approx(TOTAL_POLS_DEATH, abs=INFORCE)
    assert lapses == pytest.approx(TOTAL_POLS_LAPSE, abs=INFORCE)
    assert declines == 0.0 and reinstates == 0.0
    assert maturities == pytest.approx(POLS_MATURITY_20, abs=INFORCE)
    assert deaths + lapses + declines + maturities + a.pols_if(21) == pytest.approx(
        1.0, abs=1e-13)


def test_worked_example_reading_the_shape(kr_term_anchor):
    """The cumulative path the notes describe: strain, crossing, peak at t = 13, giveback.

    Every part of the protection shape is mechanical and the notes assert each part with a
    number, so each is pinned: the crossing back through zero during year 3, the peak of
    +444,663.00 at t = 13 and the 327,043.30 given back over the last seven years — 73% of
    the peak — as the level premium falls behind a table rate that has multiplied by 4.75
    between 보험나이 40 and 59.
    """
    a = kr_term_anchor
    df = a.result_cf()
    cum = df["net_cf"].cumsum()
    assert cum.loc[1] == pytest.approx(-127031.75, abs=WON)
    assert cum.loc[2] == pytest.approx(-39507.17, abs=WON)
    assert cum.loc[3] == pytest.approx(40335.24, abs=WON)
    assert cum.loc[13] == pytest.approx(444663.00, abs=WON)
    assert cum.idxmax() == 13
    assert cum.loc[13] - cum.loc[20] == pytest.approx(327043.30, abs=WON)
    assert (cum.loc[13] - cum.loc[20]) / cum.loc[13] == pytest.approx(0.735, abs=5e-4)
    assert a.net_cf(13) > 0.0 > a.net_cf(14)
    assert all(a.net_cf(t) < 0.0 for t in range(14, 21))
    assert a.mort_rate_at_age(59) / a.mort_rate_at_age(40) == pytest.approx(
        4.751, abs=5e-4)
    assert a.prem_pp(20) == a.prem_pp(1)
    # The answer is a difference of large numbers: premium is 1.44x death claims.
    assert df["premiums"].sum() / df["claims_death"].sum() == pytest.approx(
        1.441, abs=5e-4)
    loading = df["expenses"].sum() + df["commissions"].sum()
    assert loading / df["premiums"].sum() == pytest.approx(0.2646, abs=5e-5)
    assert (144000.0 + 108576.0) / loading == pytest.approx(0.320, abs=5e-4)


@pytest.mark.parametrize("point_id", sorted(POINT_SUMMARY))
def test_the_shipped_model_point_summary_table(term_life, point_id):
    """The notes' ten-row summary: horizon, issue premium, premium, claims and net_cf.

    The table is the worked example's coverage statement — both sexes, both renewal
    structures, both boundary readings, both maturity forms, 전기납 and shortened pay,
    년만기 and 세만기, all four rate classes and every optional module — so a change to any
    of them shows up as one failing row rather than as a moved total somewhere.
    """
    proj_len, prem_mth, premiums, claims, net_cf = POINT_SUMMARY[point_id]
    p = term_life.Projection[point_id]
    assert p.proj_len() == proj_len
    assert p.premium_mth_pp(1) == prem_mth
    got_prem, got_claims, got_net = _totals(p)
    assert got_prem == pytest.approx(premiums, abs=WON)
    assert got_claims == pytest.approx(claims, abs=WON)
    assert got_net == pytest.approx(net_cf, abs=WON)


def test_the_maturity_form_point_pays_back_the_premiums_it_collected(term_life):
    """Model point 6: 8,016,046.20 of ``claims_maturity`` beside 727,007.36 of death claims.

    A 만기환급형 hands back 100% of 「이미 납입한 주계약 보험료」, so on an undiscounted gross
    projection it **must** show a loss: the contract is financed out of investment income
    this model never credits.  The loss is evidence that an undiscounted stream is the
    wrong lens for a savings-shaped contract, which is why the savings chassis is
    ``WholeLife_KR_A`` and not this one.
    """
    p = term_life.Projection[6]
    assert p.maturity_form() == "rop"
    df = p.result_cf()
    n = p.proj_len()
    assert df["claims_maturity"].sum() == pytest.approx(8016046.20, abs=WON)
    assert df["claims_death"].sum() == pytest.approx(727007.36, abs=WON)
    assert (df["claims_maturity"][:n - 1] == 0.0).all()
    assert p.claims(n, "MATURITY") == pytest.approx(
        p.cum_prem_pp(n) * p.pols_maturity(n), rel=1e-14)
    assert p.cum_prem_pp(n) == pytest.approx(
        sum(p.prem_pp(s) for s in range(1, n + 1)), rel=1e-14)
    assert df["net_cf"].sum() < 0.0


def test_the_accidental_uplift_point_prints_the_split_the_notes_quote(term_life):
    """Model point 10: acc_mort_share 0.1236207830 / 0.0871551347 / 0.0536694127.

    474,744.49 won of ``claims_acc_death`` against 6,251,398.68 of ``claims_death`` is a
    7.6% uplift in claim cost for a **doubled** benefit, which is the order of magnitude
    that lets a carrier bundle 재해사망 into a product 형 rather than price it as a rider.
    The share is taken on the 표준체 **table** basis, so neither the class relativity nor the
    best-estimate factor disturbs it — neither has anything to say about cause of death.
    """
    p = term_life.Projection[10]
    assert p.acc_death() is True and p.rate_class() == "preferred"
    for t, share in ((1, 0.1236207830), (10, 0.0871551347), (20, 0.0536694127)):
        assert p.acc_mort_share(t) == pytest.approx(share, abs=INFORCE)
        assert p.acc_mort_share(t) == pytest.approx(
            p.acc_mort_rate_at_age(p.age(t)) / p.mort_rate_at_age(p.age(t)), rel=1e-14)
    df = p.result_cf()
    assert df["claims_acc_death"].sum() == pytest.approx(474744.49, abs=WON)
    assert df["claims_death"].sum() == pytest.approx(6251398.68, abs=WON)
    assert df["claims_acc_death"].sum() / df["claims_death"].sum() == pytest.approx(
        0.0759, abs=5e-4)


# ---------------------------------------------------------------------------
# The 갱신형 panel of the worked example


def test_the_renewal_ladder_is_read_off_published_cells_with_no_extension(term_life):
    """9,000 -> 21,000 -> 56,000 -> 201,000 a month, and the 2.33 / 2.67 / 3.59 jumps.

    This is the mandatory 예상 갱신보험료 예시 reproduced to the won, and the issue cell
    appears three times independently — in the carrier's 상품요약서, in the cross-carrier
    disclosure and in the projection itself.  A renewable term at attained-age rates
    converges on term-cost pricing, and the accelerating jump is what that convergence looks
    like; it is why carriers stop renewing at 보험나이 80.
    """
    p = term_life.Projection[3]
    assert p.renewal_type() == "gaengsin"
    assert p.policy_term() == 10 and p.renew_ceiling() == 80
    tbl = term_life.Data.prem_rate_table()
    for k, t, entry_age, p_m, p_a in RENEWAL_LADDER:
        assert p.term_index(t) == k
        assert p.term_start_age(k) == entry_age and p.term_len(k) == 10
        assert ("pure", "M", entry_age, 10) in tbl.index    # published, not extended
        assert p.prem_rate_mth(t) == p_m and p.premium_mth_pp(t) == p_m
        assert p.prem_pp(t) == p_a
    assert [round(p.prem_pp(t) / p.prem_pp(1), 2) for _, t, *_ in RENEWAL_LADDER] == [
        1.00, 2.33, 6.22, 22.33]
    jumps = [round(p.prem_pp(t + 1) / p.prem_pp(t), 2) for t in (10, 20, 30)]
    assert jumps == [2.33, 2.67, 3.59] == sorted(jumps)


@pytest.mark.parametrize("t", sorted(GAENGSIN_BOUNDARY_ROWS))
def test_the_gaengsin_boundary_rows(term_life, t):
    """The notes' eight-row boundary table on model point 3, cell by cell.

    Three rows per boundary — the year before, the boundary itself and the repriced year
    after — plus the final year, where cover ends at the ceiling rather than renewing.
    Between them they pin the decline rate, the exits it produces, the waiver reset and the
    saw-tooth, which are the four things a 갱신형 model gets wrong independently.
    """
    pols, decline_rate, declines, waived, net_cf = GAENGSIN_BOUNDARY_ROWS[t]
    p = term_life.Projection[3]
    assert p.pols_if(t) == pytest.approx(pols, abs=INFORCE)
    assert p.renewal_decline_rate(t) == pytest.approx(decline_rate, abs=1e-15)
    assert p.pols_decline(t) == pytest.approx(declines, abs=INFORCE)
    assert p.wop_waived_frac(t) == pytest.approx(waived, abs=INFORCE)
    assert p.net_cf(t) == pytest.approx(net_cf, abs=WON)


def test_the_gaengsin_year_ten_trace(term_life):
    """The notes' boundary-year trace: the old premium, in the year the contract reprices.

    Premium income in the boundary year is collected at the **old** premium, the repricing
    taking effect at the start of year 11 and not before.  Then the roll-forward in the
    processing order — mortality, ordinary lapse, and the renewal decline on the survivors
    of both — takes l(10) from 0.7405136863 to 0.5805175782.
    """
    p = term_life.Projection[3]
    assert p.pols_if(10) == pytest.approx(0.7405136863039591, rel=1e-14)
    assert p.wop_waived_frac(10) == pytest.approx(WAIVED_AT_CYCLE_END, rel=1e-12)
    assert p.pols_payer(10) == pytest.approx(0.7351990174, abs=INFORCE)
    assert p.prem_pp(10) == 108000.0
    assert p.premiums(10) == pytest.approx(79401.49, abs=WON)
    assert p.mort_rate(10) == pytest.approx(0.85 * 0.00127541, rel=1e-14)
    assert p.pols_death(10) == pytest.approx(0.0008027898, abs=INFORCE)
    assert p.claims(10, "DEATH") == pytest.approx(80278.98, abs=WON)
    assert p.claim_expenses(10) == pytest.approx(240.84, abs=WON)
    assert p.expenses(10) == pytest.approx(
        24000.0 * 1.02 ** 9 * p.pols_if(10), rel=1e-13)
    assert p.commissions(10) == pytest.approx(0.03 * p.premiums(10), rel=1e-14)
    assert p.net_cf(10) == pytest.approx(-24739.94, abs=WON)
    assert p.lapse_rate(10) == pytest.approx(0.0190127302, abs=INFORCE)
    assert p.pols_if_at(10, "BEF_LAPSE") == pytest.approx(0.7397108965, abs=INFORCE)
    assert p.pols_if_at(10, "BEF_DECLINE") == pytest.approx(0.7256469728, abs=INFORCE)
    assert p.pols_if_at(10, "AFT_DECR") == pytest.approx(0.5805175782, abs=INFORCE)
    assert p.pols_if(11) == pytest.approx(0.5805175782471498, rel=1e-14)


def test_the_gaengsin_year_eleven_trace_and_the_saw_tooth(term_life):
    """84% more premium on 22% fewer policies, then the same shape three times over.

    The crossing is the signature of a 갱신형 contract and no UK or U.S. term model in this
    repository has it.  ``net_cf`` runs -156,215.75 at t = 1, positive from t = 2, decays to
    -1,036.78 at t = 6 and -24,739.94 at t = 10, then jumps to +56,307.38 — and the
    amplitude grows at each boundary, because the premium resets to attained age while the
    in-force does not reset at all.
    """
    p = term_life.Projection[3]
    assert p.term_index(11) == 2 and p.term_start_age(2) == 50
    assert p.prem_rate_mth(11) == 21000.0 and p.prem_pp(11) == 252000.0
    assert p.wop_waived_frac(11) == 0.0
    assert p.pols_payer(11) == pytest.approx(p.pols_if(11), rel=1e-15)
    assert p.premiums(11) == pytest.approx(146290.43, abs=WON)
    assert p.pols_death(11) == pytest.approx(0.00068405579, abs=5e-12)
    assert p.claims(11, "DEATH") == pytest.approx(68405.58, abs=WON)
    assert p.claim_expenses(11) == pytest.approx(205.22, abs=WON)
    assert p.expenses(11) == pytest.approx(16983.54, abs=WON)
    assert p.commissions(11) == pytest.approx(4388.71, abs=WON)
    assert p.net_cf(11) == pytest.approx(56307.38, abs=WON)
    assert p.pols_if(11) < 0.79 * p.pols_if(10)
    assert p.premiums(11) / p.premiums(10) == pytest.approx(1.84, abs=5e-3)
    # The saw-tooth.
    assert p.net_cf(1) == pytest.approx(-156215.75, abs=WON)
    assert p.net_cf(2) > 0.0
    assert p.net_cf(6) == pytest.approx(-1036.78, abs=WON)
    for t in (10, 20, 30):
        assert p.net_cf(t) < 0.0 < p.net_cf(t + 1), f"boundary at {t}"
    jumps = [p.net_cf(t + 1) - p.net_cf(t) for t in (10, 20, 30)]
    assert jumps == sorted(jumps)


def test_the_contract_boundary_is_published_both_ways_and_ruled_on_neither(term_life):
    """+2,976,124.30 to the ceiling against -179,423.24 over the cycle in force.

    Nothing retrieved settles where a Korean 갱신 falls relative to the IFRS 17 boundary —
    the repricing is of the whole 기초율 on a new product code, which argues one way, and it
    is guaranteed-issue at portfolio level, which argues the other — so the model implements
    the long reading and carries the short one as a switch.  The two do not even share a
    sign, which is why naming the convention is part of reporting the number.
    """
    p3, p4 = term_life.Projection[3], term_life.Projection[4]
    assert p3.contract_boundary() == "ceiling" and p3.proj_len() == 40
    assert p4.contract_boundary() == "current_term" and p4.proj_len() == 10
    assert p3.horizon_ceiling() == 40 == p4.horizon_ceiling()
    assert p4.policy_term() == 10 and p3.age(p3.proj_len()) + 1 == 80
    assert p3.result_cf()["net_cf"].sum() == pytest.approx(
        GAENGSIN_TOTAL_NET_CF, abs=WON)
    assert p4.result_cf()["net_cf"].sum() == pytest.approx(CURRENT_TERM_NET_CF, abs=WON)
    assert p3.result_cf()["net_cf"].sum() * p4.result_cf()["net_cf"].sum() < 0.0
    for attr in ("sex", "age_at_entry", "renewal_type", "policy_term", "sum_assured",
                 "rate_class", "maturity_form", "waiver"):
        assert getattr(p3, attr)() == getattr(p4, attr)()


# ---------------------------------------------------------------------------
# The check_* cells and the roll-forward identities


def test_which_checks_this_model_publishes(term_life, kr_term_anchor):
    """The seven check cells, asserted **by name**, and the five that carry a residual.

    A generic sweep over ``check_*`` cannot notice a check that has quietly disappeared: it
    would call the six that remain, pass, and prove less than it did before.  Naming the set
    turns "every check passes" into a statement about *which* checks.
    ``check_decline_timing`` and ``check_waiver_reset`` are the two with no per-t residual,
    each being a statement about *where* a quantity is non-zero rather than about how far an
    identity misses.
    """
    published = {n for n in term_life.Projection.cells
                 if n.startswith("check_") and not n.endswith("_resid")}
    assert published == CHECKS
    resid = {n[:-len("_resid")] for n in term_life.Projection.cells
             if n.startswith("check_") and n.endswith("_resid")}
    assert resid == CHECKS_WITH_RESID
    a = kr_term_anchor
    for name in sorted(CHECKS):
        value = getattr(a, name)()
        assert value is True and isinstance(value, bool), name
    for name in sorted(CHECKS_WITH_RESID):
        residual = getattr(a, name + "_resid")
        for t in range(1, a.proj_len() + 1):
            assert residual(t) == pytest.approx(0.0, abs=1e-8), f"{name}_resid({t})"


def test_the_check_tolerances_are_named_references(term_life, kr_term_anchor):
    """No bare literal tolerance: ``roll_fwd_tol`` for the ledgers, ``cash_tol`` for cash.

    The two are different quantities and must not collapse into one.  ``roll_fwd_tol``
    closes identities between cells evaluated in one expression, where the residual is a
    unit or two in the last place of a count near 1.0; ``cash_tol`` closes ``check_net_cf``,
    which re-reads won amounts of order 1e7 back out of the frame.  It must therefore be
    wider — and still far below one won, the smallest error a reader could observe.
    """
    refs = term_life.Projection.refs
    assert refs["roll_fwd_tol"] == 1e-12 and refs["cash_tol"] == 1e-6
    assert refs["roll_fwd_tol"] < refs["cash_tol"] < 1.0
    a = kr_term_anchor
    worst = max(abs(a.check_net_cf_resid(t)) for t in range(1, a.proj_len() + 1))
    assert worst < refs["cash_tol"] / 100.0


def test_the_inforce_rollforward_is_the_notes_identity(term_life):
    """l(t) - l(t+1) = deaths + lapses + declines + maturities - reinstatements.

    Asserted on the four points that exercise the terms separately — the anchor, the 갱신형
    point that has declines, the 부활 point that has reinstatements and the 만기환급형 point
    whose maturity pays — because a term that is identically zero on the cell under test
    proves nothing about the term.  In force is a probability and nothing creates lives,
    except through 부활.
    """
    for point_id in (1, 3, 6, 8):
        p = term_life.Projection[point_id]
        for t in range(1, p.proj_len() + 1):
            out = (p.pols_death(t) + p.pols_lapse(t) + p.pols_decline(t)
                   + p.pols_maturity(t) - p.pols_reinstate(t))
            assert p.pols_if(t) - p.pols_if(t + 1) == pytest.approx(out, abs=1e-13), (
                f"point {point_id}, t={t}")
            assert 0.0 <= p.pols_if(t) <= 1.0
            if not p.reinstatement():
                assert p.pols_if(t + 1) <= p.pols_if(t) + 1e-15
        assert p.check_pols_roll_fwd() is True
        assert p.pols_if(p.proj_len() + 1) == 0.0


def test_the_decrements_are_taken_in_the_notes_processing_order(term_life):
    """Death, then ordinary lapse, then the renewal decline — steps 4, 5 and 6.

    Each timing reads the population the next decrement is taken from, which is what makes
    the decline a decrement on the survivors of lapse rather than one competing with it.
    Asserted on the 갱신형 point, where the third factor is not identically one.
    """
    p = term_life.Projection[3]
    for t in (1, 5, 10, 20, 31, 40):
        assert p.pols_if_at(t, "BEF_DECR") == p.pols_if(t)
        assert p.pols_if_at(t, "BEF_LAPSE") == pytest.approx(
            p.pols_if(t) * (1 - p.mort_rate(t)), rel=1e-15)
        assert p.pols_if_at(t, "BEF_DECLINE") == pytest.approx(
            p.pols_if_at(t, "BEF_LAPSE") * (1 - p.lapse_rate(t)), rel=1e-15)
        assert p.pols_if_at(t, "AFT_DECR") == pytest.approx(
            p.pols_if_at(t, "BEF_DECLINE") * (1 - p.renewal_decline_rate(t)), rel=1e-15)
        assert p.pols_death(t) == pytest.approx(
            p.pols_if_at(t, "BEF_DECR") * p.mort_rate(t), rel=1e-15)
        assert p.pols_lapse(t) == pytest.approx(
            p.pols_if_at(t, "BEF_LAPSE") * p.lapse_rate(t), rel=1e-15)
        assert p.pols_decline(t) == pytest.approx(
            p.pols_if_at(t, "BEF_DECLINE") * p.renewal_decline_rate(t), rel=1e-15)
    assert p.pols_if_at(0, "BEF_DECR") == 0.0
    assert p.pols_if_at(p.proj_len() + 1, "BEF_DECR") == 0.0
    with pytest.raises(FormulaError):
        p.pols_if_at(1, "BEF_NOTHING")


def test_the_published_statement_adds_up(term_life):
    """``result_cf`` columns are a decomposition of ``net_cf``, not a selection from it.

    ``check_net_cf`` re-derives the ledger from the **published frame** rather than from the
    cells behind it, so the identity a reader adds up with a calculator is the identity the
    model asserts.  It is the guard against a benefit kind that exists in ``claims()`` but
    was never given a column, which would leave the statement short of the outgo it charges.
    """
    for point_id in (1, 3, 6, 7, 10):
        p = term_life.Projection[point_id]
        df = p.result_cf()
        outgo = df[["claims_death", "claims_acc_death", "claims_accel",
                    "claims_maturity", "claims_lapse", "claim_expenses",
                    "expenses", "commissions"]].sum(axis=1)
        assert (df["premiums"] - outgo - df["net_cf"]).abs().max() == pytest.approx(
            0.0, abs=1e-8)
        assert p.check_net_cf() is True


def test_the_two_published_frames_and_the_sign_they_carry(kr_term_anchor, term_life):
    """``result_cf`` columns in order, and ``result_pols`` making a boundary legible.

    Column order is part of the published artefact — ``run.py`` prints the frames and the
    notes tabulate them — so a reordering is a documentation break even though every number
    is unchanged.  ``net_cf`` is income-positive, which is the notes' own sign as well as the
    library's, so there is no ``liability_cf`` companion.  And the renewal machinery is only
    readable next to the decrements it drives, which is why ``result_pols`` prints
    ``term_index`` and ``prem_pp`` beside ``renewal_decline_rate``: a boundary is the row
    whose decline rate is non-zero and whose premium moves on the next one.
    """
    df = kr_term_anchor.result_cf()
    assert list(df.index) == list(range(1, 21)) and df.index.name == "t"
    assert list(df.columns) == [
        "pols_if", "premiums", "claims_death", "claims_acc_death", "claims_accel",
        "claims_maturity", "claims_lapse", "claim_expenses", "expenses",
        "commissions", "net_cf",
    ]
    assert df.notna().all().all()
    assert "liability_cf" not in term_life.Projection.cells
    assert kr_term_anchor.net_cf(1) < 0.0 < kr_term_anchor.net_cf(2)

    pols = term_life.Projection[3].result_pols()
    assert pols.index.name == "t" and list(pols.columns)[0] == "pols_if"
    for name in ("pols_decline", "renewal_decline_rate", "term_index", "prem_pp",
                 "pols_waived", "pols_lapse_pool"):
        assert name in pols.columns
    boundaries = [t for t in pols.index if pols.loc[t, "renewal_decline_rate"] > 0.0]
    assert boundaries == [10, 20, 30]
    for t in boundaries:
        assert pols.loc[t + 1, "prem_pp"] > pols.loc[t, "prem_pp"]
        assert pols.loc[t + 1, "term_index"] == pols.loc[t, "term_index"] + 1


# ---------------------------------------------------------------------------
# Pitfall: the renewal decline is not lapse, and the order is not cosmetic


def test_pitfall_renewal_decline_is_not_lapse_and_the_order_is_not_cosmetic(term_life):
    """A different event, in a different year, from a different population — 90.7% of exits.

    The multiplicative roll-forward is order-invariant, so a model applying the decline
    **first** still balances its policy count to the last digit — and books 20% fewer death
    claims in the boundary year: 64,223.18 won instead of 80,278.98, with l(11) identical
    either way.  Folding the decline into w(t) is worse, because it makes the boundary
    invisible: on this row the decline is 0.1451293946 of 0.1599610806 total exits.
    """
    p = term_life.Projection[3]
    deaths, lapses, declines = YEAR_10_EXITS
    assert p.pols_death(10) == pytest.approx(deaths, abs=INFORCE)
    assert p.pols_lapse(10) == pytest.approx(lapses, abs=INFORCE)
    assert p.pols_decline(10) == pytest.approx(declines, abs=INFORCE)
    total = p.pols_death(10) + p.pols_lapse(10) + p.pols_decline(10)
    assert total == pytest.approx(sum(YEAR_10_EXITS), abs=INFORCE)
    assert p.pols_if(10) - p.pols_if(11) == pytest.approx(total, abs=1e-13)
    assert p.pols_decline(10) / total == pytest.approx(0.907, abs=5e-4)

    # The counterfactual: decline first, then mortality on the survivors of it.
    l10, q10, w10, d10 = (p.pols_if(10), p.mort_rate(10), p.lapse_rate(10),
                          p.renewal_decline_rate(10))
    reversed_deaths = l10 * (1 - d10) * q10
    assert reversed_deaths == pytest.approx(0.0006422318, abs=INFORCE)
    assert 100000000.0 * reversed_deaths == pytest.approx(64223.18, abs=WON)
    assert reversed_deaths == pytest.approx(0.80 * p.pols_death(10), rel=1e-12)
    assert l10 * (1 - d10) * (1 - q10) * (1 - w10) == pytest.approx(
        p.pols_if(11), rel=1e-14)          # the roll-forward cannot catch it

    # Taken after lapse, from the survivors of it, and only at a boundary.
    assert p.pols_decline(10) == pytest.approx(
        p.pols_if_at(10, "BEF_DECLINE") * 0.20, rel=1e-14)
    assert p.check_decline_timing() is True
    for t in range(1, p.proj_len() + 1):
        boundary = t % 10 == 0 and t < p.proj_len()
        assert (p.renewal_decline_rate(t) > 0.0) is boundary, t
        assert (p.pols_decline(t) > 0.0) is boundary, t
    assert p.lapse_rate(11) < p.lapse_rate(10) < p.lapse_rate(9)   # w absorbs nothing

    # A declined renewal is an expiry: nothing is paid, and nobody is re-counted.
    assert p.claims(10, "LAPSE") == 0.0
    assert p.pols_if(11) == pytest.approx(
        p.pols_if_at(10, "BEF_DECLINE") * 0.80, rel=1e-14)
    assert p.pols_lapse(11) == pytest.approx(
        p.pols_if_at(11, "BEF_LAPSE") * p.lapse_rate(11), rel=1e-14)
    assert p.pols_lapse(11) < p.pols_decline(10)
    assert p.renewal_decline_rate(p.proj_len()) == 0.0
    assert p.pols_decline(p.proj_len()) == 0.0


# ---------------------------------------------------------------------------
# Pitfall: truncation shortens the cycle, not the horizon


def test_pitfall_truncation_shortens_the_cycle_not_the_horizon():
    """A 갱신형 issued at 45 on ten-year cycles has a **five**-year final cycle to 80.

    「갱신일부터 최종 갱신계약의 보험기간 종료일까지가 10년미만일 경우에는 … 갱신계약의
    보험기간 종료일까지 이 계약의 보험기간으로 합니다」, so the ceiling truncates rather than
    refuses, and the truncated cycle is priced over its own shorter length.  Shortening the
    *horizon* instead invents or destroys cover.  No shipped point reaches a truncated
    cycle, so the point is supplied through the filename Reference — which is the same
    swappable-input property the library advertises.
    """
    src = pd.read_csv(CSV_DIR / "model_point_table.csv", index_col="point_id")
    row = src.loc[3].copy()
    row["issue_age"] = 45
    row["policy_id"] = "KR-TL-TRUNC"
    alt = pd.DataFrame([row])
    alt.index = pd.Index([99], name="point_id")

    model = _reread("trunc")
    alt_name = "model_point_table_trunc.csv"
    alt_path = model.Data.input_dir() / alt_name
    try:
        alt.to_csv(alt_path)
        model.Data.model_point_file = alt_name
        model.Data.clear_all()
        model.Projection.clear_all()
        p = model.Projection[99]
        assert p.age_at_entry() == 45 and p.renew_ceiling() == 80
        assert p.horizon_ceiling() == 35 == p.proj_len()
        assert p.age(p.proj_len()) + 1 == 80        # the horizon still ends at 80
        assert [p.term_start_age(k) for k in (1, 2, 3, 4)] == [45, 55, 65, 75]
        assert [p.term_len(k) for k in (1, 2, 3, 4)] == [10, 10, 10, 5]
        assert p.term_index(31) == 4 == p.term_index(35)
        assert p.mort_table_mean(75, 5) < p.mort_table_mean(75, 10)
        anchor = model.Data.prem_anchor_table().loc[("pure", "M")]
        assert p.prem_rate_mth(31) == pytest.approx(
            float(anchor["prem_mth_per_100m"]) * p.mort_table_mean(75, 5)
            / p.mort_table_mean(40, 20), rel=1e-12)
        assert p.renewal_decline_rate(30) == 0.20   # the last renewal
        assert p.renewal_decline_rate(35) == 0.0    # the cover ends; it does not renew
        assert p.check_pols_roll_fwd() is True
        assert p.check_decline_timing() is True and p.check_prem_level() is True
    finally:
        alt_path.unlink(missing_ok=True)
        model.close()


def test_pitfall_bi_gaengsin_never_renews(term_life):
    """One 보험기간, one premium, no repricing — and the decline rate is 0 at every t.

    Applying the renewal machinery to a 비갱신형 point invents cover the contract does not
    have, and 비갱신형 is the base here because it is the market: only three of the 45
    disclosed products renew at all.  ``check_decline_timing`` asserts the biconditional in
    both directions, which is what catches the opposite error too — a decline invented in
    the final year, where cover ends rather than renewing.
    """
    for point_id in (1, 2, 5, 6, 7, 8, 9, 10):
        p = term_life.Projection[point_id]
        n = p.proj_len()
        assert p.renewal_type() == "bi_gaengsin"
        assert p.horizon_ceiling() == p.policy_term() == n
        assert all(p.term_index(t) == 1 for t in range(1, n + 1))
        assert all(p.term_start_age(k) == p.age_at_entry() for k in (1, 2, 3))
        assert all(p.renewal_decline_rate(t) == 0.0 for t in range(1, n + 1))
        assert all(p.pols_decline(t) == 0.0 for t in range(1, n + 1))
        assert all(p.prem_pp(t) == p.prem_pp(1) for t in range(1, n + 1))
        assert p.check_decline_timing() is True
    p7 = term_life.Projection[7]                    # a 세만기 point: term from expiry age
    assert p7.age_at_entry() == 65 and p7.policy_term() == 15
    assert p7.age(p7.proj_len()) + 1 == 80


def test_pitfall_the_premium_follows_the_renewal_index_not_the_policy_year(term_life):
    """Freezing P_a at the issue value collects 2,217,536.20 instead of 11,602,888.01.

    That is one-fifth of the right price: indexing the premium by ``t`` converts a 갱신형
    into a 비갱신형 without changing anything a policy roll-forward can see.
    ``check_prem_level`` asserts the complement — level **within** a cycle, changing across
    a boundary — which catches the opposite error, a rate lookup keyed on attained age that
    makes the premium drift year by year instead of stepping.
    """
    p = term_life.Projection[3]
    assert p.check_prem_level() is True
    for t in range(1, p.proj_len() + 1):
        assert p.check_prem_level_resid(t) == pytest.approx(0.0, abs=1e-12)
    assert all(p.prem_pp(t) == p.prem_pp(1) for t in range(2, 11))
    for t in (10, 20, 30):
        assert p.prem_pp(t + 1) > p.prem_pp(t)
        assert p.check_prem_level_resid(t + 1) == 0.0   # zero by definition, not by luck
    frozen = sum(p.prem_pp(1) * p.pols_payer(t) for t in range(1, p.proj_len() + 1))
    assert frozen == pytest.approx(2217536.20, abs=WON)
    assert p.result_cf()["premiums"].sum() == pytest.approx(11602888.01, abs=WON)
    assert frozen / p.result_cf()["premiums"].sum() == pytest.approx(0.191, abs=5e-4)


# ---------------------------------------------------------------------------
# Pitfall: the waiver, and what a 갱신 does and does not reset


def test_pitfall_a_premium_waiver_does_not_survive_a_gaengsin(term_life):
    """u(t) is 0.0 exactly at t = 1, 11, 21, 31 and rebuilds to 0.0071770030 by t = 10.

    Sourced, not assumed: 「다만, 새로이 갱신되는 계약에서는 갱신 전 보험료 납입면제 사유로
    인한 보험료 납입면제를 적용하지 않고, 보험료를 계속 납입하여야 합니다」.  A disabled life
    resumes paying at the renewal date, so a model carrying the waived fraction across the
    boundary loses premium income the contract entitles the insurer to collect — invisibly,
    because no policy count moves.
    """
    p = term_life.Projection[3]
    assert p.waiver() is True and p.check_waiver_reset() is True
    for t in (1, 11, 21, 31):
        assert p.wop_waived_frac(t) == 0.0, f"the waiver survived into t={t}"
        assert p.pols_waived(t) == 0.0
        assert p.pols_payer(t) == pytest.approx(p.pols_if(t), rel=1e-15)
    for first in (1, 11, 21, 31):
        run = [p.wop_waived_frac(t) for t in range(first, first + 10)]
        assert run == sorted(run)
        assert run[-1] == pytest.approx(WAIVED_AT_CYCLE_END, rel=1e-12)
    assert p.wop_rec_rate == 0.0
    for t in range(2, 10):
        u = p.wop_waived_frac(t - 1)
        assert p.wop_waived_frac(t) == pytest.approx(u + (1 - u) * 0.0008, rel=1e-13)
    assert p.check_pols_payer() is True
    for t in (5, 10, 25, 40):
        assert p.pols_payer(t) + p.pols_waived(t) == pytest.approx(
            p.pols_if(t) * p.prem_payable(t), rel=1e-15)


def test_pitfall_the_suicide_and_contestability_clocks_do_not_reset_at_a_gaengsin(
        term_life):
    """``pols_if`` is continuous across every boundary — a 갱신 reprices, it does not reissue.

    The contract is fresh for pricing and for the waiver and continuous for the exclusions,
    which run from the original 보장개시일 and restart only on 부활.  The observable
    consequence is asserted: no reset of the in-force to 1, no acquisition expense and no
    initial commission at a renewal, and an inflation clock that runs from issue.
    """
    p = term_life.Projection[3]
    for t in (10, 20, 30):
        assert p.pols_if(t + 1) == pytest.approx(p.pols_if_at(t, "AFT_DECR"), rel=1e-15)
        assert p.pols_if(t + 1) < 0.6                     # never a reset to 1
        assert p.expenses(t + 1) == pytest.approx(
            24000.0 * 1.02 ** t * p.pols_if(t + 1), rel=1e-13)
        assert p.commissions(t + 1) == pytest.approx(0.03 * p.premiums(t + 1), rel=1e-13)
        assert p.comm_new_term(t + 1) == 0.0
    assert p.expenses(1) - 24000.0 == pytest.approx(120000.0, abs=WON)
    assert p.commissions(1) == pytest.approx(0.60 * p.prem_pp(1), abs=WON)


def test_pitfall_the_waiver_is_cause_neutral_so_it_is_not_scaled_off_mort_rate(
        term_life):
    """``wop_inc_rate`` is a flat placeholder, deliberately not a function of q.

    The trigger is a 장해지급률 of 50% or more from 「동일한 재해 또는 재해이외의 동일한
    원인」 — sickness qualifies equally with accident — so the incidence is a general
    disability incidence.  A number derived from ``mort_rate`` would be a false derivation
    dressed as a real one, and would import the mortality best-estimate factor into a
    disability assumption.  The signature is that the increment is flat while q is not.
    """
    p = term_life.Projection[3]
    assert p.wop_inc_rate == 0.0008
    increments = [p.wop_waived_frac(t) - p.wop_waived_frac(t - 1) for t in range(2, 11)]
    assert max(increments) / min(increments) < 1.01
    assert p.mort_rate(10) / p.mort_rate(1) > 1.6
    names = set(term_life.Projection.cells) | set(term_life.Projection.refs)
    for absent in ("wop_mort_ratio", "wop_rate_factor", "disab_from_mort"):
        assert absent not in names


# ---------------------------------------------------------------------------
# Pitfall: one decrement, and what may be split out of it


def test_pitfall_acc_death_is_a_split_of_the_decrement_never_a_second_decrement(
        term_life):
    """The uplift pays 2 x SA on 재해사망 and 1 x otherwise, on **one** decrement.

    ``claims_acc_death`` is the *second* sum assured on the accidental subset and sits
    beside the full ``claims_death``, so the total on an accidental death is exactly 2 x SA.
    An accidental incidence added as a decrement of its own would double-count the deaths
    and break the roll-forward; the arithmetic guard is that a year's benefit outgo can
    never exceed two sums assured on that year's decrement.
    """
    p = term_life.Projection[10]
    for t in range(1, p.proj_len() + 1):
        assert p.acc_mort_share(t) <= 1.0
        assert p.claims(t, "DEATH") == pytest.approx(
            p.sum_assured() * p.pols_death(t), rel=1e-14)
        assert p.claims(t, "ACC_DEATH") == pytest.approx(
            p.sum_assured() * p.acc_mort_share(t) * p.pols_death(t), rel=1e-14)
        assert p.claims(t) <= 2.0 * p.sum_assured() * p.pols_death(t) + 1e-9
    assert p.pols_death(1) == pytest.approx(p.pols_if(1) * p.mort_rate(1), rel=1e-15)
    assert p.check_pols_roll_fwd() is True
    for point_id in (1, 3, 7):
        q = term_life.Projection[point_id]
        assert q.acc_death() is False
        assert (q.result_cf()["claims_acc_death"] == 0.0).all()


def test_pitfall_the_disability_state_is_not_a_benefit(term_life):
    """Korea has no 高度障害保険金 analogue: the 장해 state waives premiums and nothing more.

    Adding a disability claim on top of the death decrement invents a benefit the contract
    does not carry, and doing it on the Japanese pattern also double-counts, the table there
    already including the second event.  Names alone are not coverage, so the guard is the
    product fact: on a point without the 재해사망 uplift, benefit outgo never exceeds **one**
    sum assured on the year's decrement.
    """
    names = set(term_life.Projection.cells) | set(term_life.Projection.refs)
    for absent in ("disability_rate", "disab_rate", "ci_rate", "morbidity_rate",
                   "claims_disability", "janghae_rate"):
        assert absent not in names, f"{absent} would invent a benefit"
    assert not [n for n in names if "disab" in n or "morbid" in n]
    for point_id in (1, 3, 5):
        p = term_life.Projection[point_id]
        for t in range(1, p.proj_len() + 1):
            if p.pols_maturity(t) == 0.0:
                assert p.claims(t) <= p.sum_assured() * p.pols_death(t) + 1e-9, (
                    f"point {point_id}, t={t}: outgo exceeds one sum assured")
    with pytest.raises(FormulaError):
        term_life.Projection[1].claims(1, "DISABILITY")


def test_pitfall_no_claims_aggregate_column_beside_the_splits(term_life):
    """``claims(t, kind)`` stays a cells; ``result_cf()`` publishes only the five splits.

    An aggregate column beside the splits double-counts the whole benefit outgo, and
    ``check_net_cf`` — which re-derives the ledger from the published frame — would then fail
    on every row.  The kind argument is validated rather than defaulted, so a typo in a
    benefit name raises instead of silently returning zero.
    """
    df = term_life.Projection[1].result_cf()
    assert "claims" not in df.columns
    assert [c for c in df.columns if c.startswith("claims")] == [
        "claims_death", "claims_acc_death", "claims_accel", "claims_maturity",
        "claims_lapse"]
    p = term_life.Projection[10]
    for t in (1, 10, 20):
        assert p.claims(t) == pytest.approx(
            sum(p.claims(t, k) for k in
                ("DEATH", "ACC_DEATH", "ACCEL", "MATURITY", "LAPSE")), rel=1e-15)
    with pytest.raises(FormulaError):
        p.claims(1, "SURRENDER")


# ---------------------------------------------------------------------------
# Pitfall: a lapse pays nothing, and what follows from that


def test_pitfall_lapse_pays_nothing_and_the_zero_is_published(term_life):
    """``claims_lapse`` is identically 0.00 on every model point, and is shipped anyway.

    On a 전기납 무해지 contract the 약관 pays nothing at any duration and the published
    해약환급금 예시 shows 환급률 0.0% at every duration printed.  But the **표준형 comparator
    does have a surrender value**, and a shortened-pay 무해지 contract acquires 50% of it
    after 납입완료, so a Korea term chassis cannot assume the absence the way a UK one can:
    the zero is asserted from the composite's own form, which is why the column is published
    rather than dropped.  No surrender value also means no 보험계약대출 and no 자동대출납입 in
    fact, so none of the savings chassis's cash-value machinery may appear here.
    """
    for point_id in sorted(POINT_SUMMARY):
        p = term_life.Projection[point_id]
        df = p.result_cf()
        assert "claims_lapse" in df.columns and (df["claims_lapse"] == 0.0).all()
        assert all(p.claims(t, "LAPSE") == 0.0 for t in range(1, p.proj_len() + 1))
        assert any(p.pols_lapse(t) > 0.0 for t in range(1, p.proj_len() + 1))
    names = set(term_life.Projection.cells) | set(term_life.Projection.refs)
    for absent in ("cv_pp", "av_pp", "policy_loan", "loan_bal", "apl", "apl_rate",
                   "surr_charge", "prem_to_av_pp", "cv_rate"):
        assert absent not in names, f"{absent} belongs to a chassis with a cash value"
    assert not [n for n in names if "loan" in n or n.startswith("cv_")]


def test_pitfall_the_jeongi_nap_resolution_couples_pay_term_to_the_boundary(term_life):
    """Model point 4 is **not** model point 3 truncated: -179,423.24 against -170,638.50.

    ``pay_term_y = 0`` means 전기납 and resolves to ``proj_len()``, so truncating a 갱신형
    point at the cycle in force compresses the 적용해지율 curve from forty years to ten with
    it.  That is a consequence of the boundary reading rather than a bug, and it is asserted
    here so that a later change making the two agree fails a test.  Model point 5, a genuine
    10년납 contract, is the mirror image and the only shipped point that reaches the
    ``post_payment`` row at all: its curve runs the disclosed shape at its disclosed length
    and then **steps** to the 0.8% ultimate rather than converging smoothly, the premium
    ceases and cover does not, and the 무해지 post-완납 surrender-value step-up this makes
    possible is the quantity the chassis deliberately does not compute.
    """
    p3, p4 = term_life.Projection[3], term_life.Projection[4]
    assert p3.pay_term() == 40 and p4.pay_term() == 10
    assert p3.result_cf()["net_cf"][:10].sum() == pytest.approx(
        GAENGSIN_FIRST_TEN_NET_CF, abs=WON)
    assert p4.result_cf()["net_cf"].sum() == pytest.approx(CURRENT_TERM_NET_CF, abs=WON)
    assert p3.result_cf()["net_cf"][:10].sum() != pytest.approx(
        p4.result_cf()["net_cf"].sum(), abs=1.0)
    assert p3.lapse_rate(1) == pytest.approx(p4.lapse_rate(1), rel=1e-14)
    assert p4.lapse_rate(10) == pytest.approx(0.001, rel=1e-14)
    assert p3.lapse_rate(10) > p4.lapse_rate(10)
    assert p3.lapse_rate(40) == pytest.approx(0.001, rel=1e-14)

    p = term_life.Projection[5]
    assert p.pay_term() == 10 and p.proj_len() == 20
    assert p.lapse_rate(10) == pytest.approx(0.001, rel=1e-14)
    assert all(p.lapse_rate(t) == 0.008 for t in range(11, 21))
    assert p.prem_payable(10) == 1.0 and p.prem_payable(11) == 0.0
    assert p.pols_payer(11) == 0.0 and p.premiums(11) == 0.0
    assert p.commissions(11) == 0.0 and p.check_pols_payer() is True
    assert p.pols_death(11) > 0.0 and p.claims(11, "DEATH") > 0.0
    assert all(p.claims(t, "LAPSE") == 0.0 for t in range(11, 21))


# ---------------------------------------------------------------------------
# Pitfall: the premium chassis


def test_pitfall_qbar_is_a_mean_of_table_rates_not_best_estimate_rates(term_life):
    """``mort_table_mean`` averages ``mort_rate_at_age``, unadjusted by anything.

    A premium scale is not a best-estimate quantity, so feeding ``mort_rate`` into the
    extension would move a published rate card by an assumption with nothing to do with
    pricing.  A class-adjusted qbar would **cancel in the ratio** and fail silently only on a
    preferred-class point, which is the worst kind of error — so it is the preferred-class
    point that is asserted here.  The seven diagnostic values the notes publish are asserted
    alongside, because they are what lets a reader verify the extension against the shipped
    mortality table with a spreadsheet.
    """
    a = term_life.Projection[1]
    assert a.mort_table_mean(40, 20) == pytest.approx(
        sum(a.mort_rate_at_age(x) for x in range(40, 60)) / 20.0, rel=1e-14)
    assert a.mort_table_mean(40, 1) == a.mort_rate_at_age(40)      # not 0.85 x it
    for (sex, x, m), qbar in sorted(QBAR_DIAGNOSTICS.items()):
        q = term_life.Projection[1 if sex == "M" else 2]
        assert q.sex() == sex
        assert q.mort_table_mean(x, m) == pytest.approx(qbar, abs=5e-9), (sex, x, m)
    p = term_life.Projection[10]
    assert p.rate_class() == "preferred" and p.class_mort_ratio() < 1.0
    anchor = float(term_life.Data.prem_anchor_table().loc[
        ("pure", "M"), "prem_mth_per_100m"])
    assert p.prem_rate_mth(1) == pytest.approx(
        anchor * p.mort_table_mean(55, 20) / p.mort_table_mean(40, 20), rel=1e-12)
    # A class-adjusted qbar would cancel; a best-estimate one would not.
    classed = (anchor * p.mort_table_mean(55, 20) * p.class_mort_ratio()
               / (p.mort_table_mean(40, 20) * p.class_mort_ratio()))
    assert classed == pytest.approx(p.prem_rate_mth(1), rel=1e-12)
    be_scaled = (anchor * sum(p.mort_rate(t) for t in range(1, 21)) / 20.0
                 / p.mort_table_mean(40, 20))
    assert be_scaled != pytest.approx(p.prem_rate_mth(1), rel=1e-3)
    # The class enters through class_prem_ratio, once, and not through qbar.
    raw = p.prem_rate_mth(1) * p.class_prem_ratio() * p.sum_assured() / 100000000.0
    assert p.premium_mth_pp(1) == float(int(raw / 10.0 + 0.5) * 10)


def test_the_premium_scale_uses_published_cells_where_they_exist(term_life):
    """Points 1-6 read published cells only; points 7-10 use the [std] extension.

    The extension is anchored on the age-40 20-year cell of the matching form and sex, so a
    published cell is always used where one exists.  The 10-year rows and the 20-year rows
    come from **different carriers** and the model never mixes them: a 갱신형 point reaches
    published 10-year cells, and an unpublished cell runs off the 20-year anchor.
    """
    tbl = term_life.Data.prem_rate_table()
    published, extended = set(), set()
    for point_id in sorted(POINT_SUMMARY):
        p = term_life.Projection[point_id]
        key = (p.maturity_form(), p.sex(), p.term_start_age(1), p.term_len(1))
        (published if key in tbl.index else extended).add(point_id)
    assert published == {1, 2, 3, 4, 5, 6} and extended == {7, 8, 9, 10}
    anchors = term_life.Data.prem_anchor_table()
    assert set(anchors.index) == {("pure", "M"), ("pure", "F"),
                                  ("rop", "M"), ("rop", "F")}
    for form, sex in anchors.index:
        assert int(anchors.loc[(form, sex), "issue_age"]) == 40
        assert int(anchors.loc[(form, sex), "term_y"]) == 20
    assert float(tbl.loc[("pure", "M", 40, 20), "prem_mth_per_100m"]) == 15080.0
    assert float(tbl.loc[("pure", "F", 40, 20), "prem_mth_per_100m"]) == 8010.0
    assert term_life.Projection[2].prem_rate_mth(1) == 8010.0


def test_pitfall_the_premium_rounds_to_ten_won_before_annualization(term_life):
    """``round_10(r c_p g SA/1e8)`` then ``x 12`` — and the order reproduces 15,080.

    Rounding after annualization, or not at all, breaks the reproduction of the published
    15,080 / 180,960 at the anchor and of 9,000 / 108,000 on the 갱신형 point, and those are
    figures three independent documents agree on.  The extension points are where the
    rounding actually bites, so one of them is asserted explicitly.
    """
    for point_id in sorted(POINT_SUMMARY):
        p = term_life.Projection[point_id]
        raw = (p.prem_rate_mth(1) * p.class_prem_ratio() * p.pay_factor(1)
               * p.sum_assured() / 100000000.0)
        assert p.premium_mth_pp(1) == float(int(raw / 10.0 + 0.5) * 10)
        assert p.premium_mth_pp(1) % 10 == 0
        assert p.prem_pp(1) == 12.0 * p.premium_mth_pp(1)
    p10 = term_life.Projection[10]
    raw10 = p10.prem_rate_mth(1) * p10.class_prem_ratio() * p10.sum_assured() / 1e8
    assert raw10 != pytest.approx(p10.premium_mth_pp(1), abs=1e-9)
    assert abs(raw10 - p10.premium_mth_pp(1)) < 5.0 and p10.premium_mth_pp(1) == 49480.0
    assert term_life.Projection[1].premium_mth_pp(1) == 15080.0
    assert term_life.Projection[3].prem_pp(1) == 108000.0


def test_pitfall_twelve_times_p_m_is_exact_in_amount_and_standardized_only_in_timing(
        term_life):
    """``P_a = 12 P_m`` exactly, with no mode discount and no half-year adjustment.

    The policyholder does pay twelve monthly premiums a year and no carrier publishes a mode
    discount, so the annualized **amount** is not an approximation — only the timing is.  Do
    not apply a further half-year adjustment on top of the end-of-year claim timing: the two
    conventions are a matched pair, and the bias does not enter an undiscounted projection.
    """
    for point_id in (1, 3, 9):
        p = term_life.Projection[point_id]
        assert p.premium_mode() == "monthly"
        for t in (1, p.proj_len()):
            assert p.prem_pp(t) == 12.0 * p.premium_mth_pp(t)
    a = term_life.Projection[1]
    for t in (1, 2, 10, 20):
        assert a.premiums(t) == pytest.approx(a.prem_pp(t) * a.pols_payer(t), rel=1e-15)
    names = set(term_life.Projection.cells) | set(term_life.Projection.refs)
    for absent in ("mode_factor", "prem_mode_discount", "half_year_adj",
                   "prem_timing_adj"):
        assert absent not in names


def test_the_shortened_pay_uplift_is_an_annuity_certain_ratio(term_life):
    """g = 1.781198 on model point 5 and 1.484695 on model point 9, at the 적용이율.

    No Korean document retrieved publishes a shortened-pay premium for a **term** contract
    at all, so an equivalence had to be chosen; a certain annuity rather than a life annuity
    overstates the uplift slightly, by the mortality that would have been shed between the
    two periods.  It is 1.0 on a 전기납 contract, where there is nothing to uplift.
    """
    v = 1.0 / 1.025
    p5, p9 = term_life.Projection[5], term_life.Projection[9]
    assert p5.prem_int_rate == 0.025
    assert p5.pay_factor(1) == pytest.approx(1.781198, abs=5e-7)
    assert p9.pay_factor(1) == pytest.approx(1.484695, abs=5e-7)
    assert p5.pay_factor(1) == pytest.approx((1 - v ** 20) / (1 - v ** 10), rel=1e-14)
    assert p9.pay_factor(1) == pytest.approx((1 - v ** 35) / (1 - v ** 20), rel=1e-14)
    assert p5.term_pay_years(1) == 10 and p5.term_len(1) == 20
    for point_id in (1, 2, 3, 6, 7, 8, 10):
        p = term_life.Projection[point_id]
        assert p.pay_factor(1) == 1.0
        assert p.term_pay_years(1) == p.term_len(1)


# ---------------------------------------------------------------------------
# Pitfall: the 선지급 acceleration


def test_pitfall_the_accel_cap_is_reached_exactly_at_the_anchor_and_reduces_nothing(
        term_life):
    """``accel_cap_binds()`` is a **strict** inequality and is False at SA = 100,000,000.

    The cap is 「사망보험금액의 50% 이내에서 피보험자별로 통산하여 최고 5,000만원까지」, so at
    the anchor's cover the 50% limb gives exactly 50,000,000 and the aggregate cap is exactly
    reached and reduces nothing.  A model reporting it as binding there has a
    strict-versus-weak inequality error.  Model point 9, at 200,000,000 won, genuinely binds.
    """
    a = term_life.Projection[1]
    assert a.accel_share_max * a.sum_assured() == a.accel_cap == 50000000.0
    assert a.accel_cap_binds() is False and a.accel_full_limit == 10000000.0
    p7 = term_life.Projection[7]
    assert p7.accel() is True and p7.sum_assured() == 30000000.0
    assert p7.accel_cap_binds() is False and p7.accel_amount() == 15000000.0
    p9 = term_life.Projection[9]
    assert p9.accel() is True and p9.sum_assured() == 200000000.0
    assert p9.accel_cap_binds() is True and p9.accel_amount() == 50000000.0
    assert p9.accel_share_max * p9.sum_assured() == 100000000.0


def test_pitfall_the_accelerated_amount_comes_out_of_the_death_benefit(term_life):
    """``claims_death`` carries (1 - a(t)) and ``claims_accel`` carries a(t).

    The 보험가입금액 is treated as reduced by the amount paid from the payment date and no
    surrender value arises on the reduction, so the acceleration is a re-timing and
    re-pricing of the death benefit rather than a second claim; adding it on top of a full
    death claim pays the benefit twice.  The payout is discounted over the 12-month
    prognosis, which is why switching the rider off *raises* total benefit outgo.
    """
    p = term_life.Projection[7]
    v = 1.0 / 1.025
    assert (p.accel_take_up, p.accel_disc_rate, p.accel_prognosis_months) == (
        0.10, 0.025, 12)
    for t in range(1, p.proj_len() + 1):
        assert p.accel_available(t) is True and p.accel_share(t) == 0.10
        assert p.claims(t, "DEATH") == pytest.approx(
            p.sum_assured() * 0.90 * p.pols_death(t), rel=1e-14)
        assert p.claims(t, "ACCEL") == pytest.approx(
            p.accel_payout_pp(t) * 0.10 * p.pols_death(t), rel=1e-14)
        assert p.claims(t) <= p.sum_assured() * p.pols_death(t) + 1e-9
    amount = p.accel_amount()
    assert p.accel_payout_pp(1) == pytest.approx(
        amount * v - 12 * p.premium_mth_pp(1) * amount / p.sum_assured() * v ** 0.5,
        rel=1e-13)
    assert p.accel_payout_pp(1) < amount
    on = sum(p.claims(t) for t in range(1, p.proj_len() + 1))

    model = _reread("accoff")
    try:
        model.Projection.accel_take_up = 0.0
        model.Projection.clear_all()
        off = model.Projection[7]
        n = off.proj_len()
        assert off.accel_share(1) == 0.0
        assert all(off.pols_death(t) == pytest.approx(p.pols_death(t), abs=1e-15)
                   for t in range(1, n + 1))
        assert sum(off.claims(t) for t in range(1, n + 1)) > on
    finally:
        model.close()
    # Off in the base run, with the column published and zero.
    a = term_life.Projection[1]
    assert a.accel() is False and a.accel_amount() == 0.0
    assert (a.result_cf()["claims_accel"] == 0.0).all()


# ---------------------------------------------------------------------------
# Pitfall: the 부활 pool is carried by vintage


def test_pitfall_the_buhwal_window_runs_from_each_life_s_own_lapse(term_life):
    """The pool is the last three years' lapses, each net of its own reinstatements.

    The window runs from **each life's own 실효**, so a single indicator on one balance drops
    a whole cohort a year early or late.  ``reinstate_window = 3`` is sourced and the clause
    expressly covers a policy with no surrender value, so a 무해지 policy is always eligible;
    the rate beside it is an arbitrary placeholder, which is why the module is off in the
    base run and why the pool is tracked in both positions of the switch.
    """
    p = term_life.Projection[8]
    assert p.reinstatement() is True
    assert p.reinstate_rate_eff() == 0.10 and p.reinstate_window == 3
    assert p.pols_lapse_pool(1) == 0.0
    assert p.pols_reinstate(2) == pytest.approx(0.10 * p.pols_lapse_pool(2), rel=1e-14)
    assert p.pols_if(3) > p.pols_if_at(2, "AFT_DECR")        # lives come back in
    for t in range(2, p.proj_len() + 1):
        rebuilt = sum(p.pols_lapse(s) * 0.9 ** (t - 1 - s)
                      for s in range(max(1, t - 3), t))
        assert p.pols_lapse_pool(t) == pytest.approx(rebuilt, abs=1e-14)
    assert p.pols_lapse_expire(3) == 0.0
    assert p.pols_lapse_expire(4) == pytest.approx(p.pols_lapse(1) * 0.9 ** 3, rel=1e-13)
    assert p.check_lapse_pool() is True
    a = term_life.Projection[1]
    assert a.reinstatement() is False and a.reinstate_rate_eff() == 0.0
    assert all(a.pols_reinstate(t) == 0.0 for t in range(1, a.proj_len() + 1))
    assert a.pols_lapse_pool(4) > 0.0 and a.check_lapse_pool() is True


def test_pitfall_declines_never_enter_the_reinstatement_pool(term_life):
    """A declined 갱신 is an expiry, not a 실효, so there is nothing to reinstate.

    Only ordinary lapses flow into the pool.  Folding the boundary exits in would reinstate
    lives whose contract ended rather than lapsed — and on the 갱신형 anchor the declines are
    90.7% of the boundary year's exits, so the error would be large as well as wrong.
    """
    p = term_life.Projection[3]
    assert p.pols_decline(10) > 0.0
    for t in (10, 11, 12, 13):
        assert p.pols_lapse_pool(t) == pytest.approx(
            sum(p.pols_lapse(s) for s in range(max(1, t - 3), t)), abs=1e-14)
    assert p.check_lapse_pool() is True
    model = _reread("pool")
    try:
        model.Projection.reinstate_rate = 0.10
        model.Projection.clear_all()
        q = model.Projection[3]
        assert q.reinstatement() is False          # the column, not the Reference
        assert q.pols_lapse_pool(11) == pytest.approx(
            sum(q.pols_lapse(s) for s in range(8, 11)), abs=1e-14)
    finally:
        model.close()


# ---------------------------------------------------------------------------
# Pitfall: read the tables at 보험나이 and at nothing else


def test_pitfall_read_the_tables_at_boheom_nai_and_at_nothing_else(term_life):
    """Reading the anchor cell a year early cuts death claims to 1,905,170.00 — 8.0% out.

    보험나이 is 만나이 with fractions of six months or more rounded up, incrementing on the
    **policy anniversary** and not on the birthday, and the premium grid, the mortality table
    and the model point ages are all on that one basis.  Unlike ``jplib``, where the contract
    age and the table basis differ and an optional shift exists, **no shift is correct
    here** — importing one is the error, and the model carries no lever that could.
    """
    a = term_life.Projection[1]
    assert a.age_at_entry() == 40 and a.age(1) == 40 and a.age(20) == 59
    for t in (1, 10, 20):
        assert a.age(t) == a.age_at_entry() + t - 1
        assert a.mort_rate_base(t) == a.mort_rate_at_age(a.age(t)) * a.class_mort_ratio()
    names = set(term_life.Projection.cells) | set(term_life.Projection.refs)
    for absent in ("mort_age_shift", "age_shift", "age_basis_shift", "man_nai_shift"):
        assert absent not in names, f"{absent} would apply a shift this model must not"
    # The counterfactual is the whole projection read a year early — the shifted rate
    # drives the survivorship too, which is what a mis-specified model would actually do.
    understated, pols = 0.0, 1.0
    for t in range(1, 21):
        q = a.mort_be_factor * a.mort_rate_at_age(a.age(t) - 1)
        understated += a.sum_assured() * pols * q
        pols *= (1.0 - q) * (1.0 - a.lapse_rate(t))
    assert understated == pytest.approx(1905170.00, abs=WON)
    assert 1.0 - understated / TOTAL_CLAIMS_DEATH == pytest.approx(0.080, abs=5e-4)
    assert TOTAL_CLAIMS_DEATH - understated > TOTAL_NET_CF   # more than the whole answer
    assert "보험나이" in term_life.Projection.doc


# ---------------------------------------------------------------------------
# The [std] parameters the notes state


def test_the_std_scalar_assumptions_the_notes_state(term_life):
    """Every scalar the notes tabulate, read off the model's References.

    The house rule is that every quantitative parameter is source-tagged or marked [std],
    and the notes carry each of these with its tag.  Pinning them means a silent change to
    an assumption fails a **named** test rather than moving a golden and looking like an
    arithmetic problem.  Three parameters beside them are **sourced** and are asserted as
    such: ``reinstate_window = 3`` is the 약관's own 부활 window,
    ``accel_prognosis_months = 12`` is its prognosis (twice Japan's six), and
    ``accel_disc_rate = 0.025`` is the 2026 평균공시이율 the 약관 names for this discount.  That
    the last equals the composite's 적용이율 is a coincidence of level and not an identity of
    concept, so moving one must not move the other.
    """
    refs = term_life.Projection.refs
    for name, value in STD_SCALARS.items():
        assert name in refs, f"{name} is no longer a Reference"
        assert refs[name] == pytest.approx(value, rel=1e-15), name
    assert refs["renewal_decline_base"] < refs["renewal_decline_max"]
    assert 0.0 < refs["wop_inc_rate"] < 0.01
    assert 0.0 < refs["accel_take_up"] < 1.0
    assert 0.0 < refs["reinstate_rate"] < 1.0
    assert refs["reinstate_window"] == 3 and refs["accel_prognosis_months"] == 12
    assert refs["accel_disc_rate"] == 0.025 == refs["prem_int_rate"]
    model = _reread("rates")
    try:
        model.Projection.accel_disc_rate = 0.04
        model.Projection.clear_all()
        p = model.Projection[7]
        assert p.prem_int_rate == 0.025           # unmoved: a different quantity
        assert p.premium_mth_pp(1) == term_life.Projection[7].premium_mth_pp(1)
        assert p.accel_payout_pp(1) < term_life.Projection[7].accel_payout_pp(1)
    finally:
        model.close()


def test_the_shipped_mortality_table_marks_its_own_provenance_and_hits_the_published_e65():
    """Every row says whether it is a disclosed anchor or the [std] fit, and e(65) lands.

    The 제10회 경험생명표 is **not published** — only 평균수명 and 65세 기대여명 are released —
    so the library ships a Makeham construction fitted exactly to the three 예정 경험사망률
    rates per sex that every 상품요약서 must print, tilted above 60 so the table reproduces
    the published e(65) of 23.7 male and 27.1 female.  That reproduction is the only external
    check available, and the four-year gap over the public 완전생명표 is the underwriting
    selection a Korean insured-lives table must show.
    """
    table = pd.read_csv(CSV_DIR / "mort_table.csv")
    assert list(table.columns) == ["sex", "age", "mort_rate", "acc_mort_rate",
                                   "provenance"]
    assert table["provenance"].notna().all()
    assert (table["provenance"].str.contains(r"\[std\]")).all()
    assert (table["provenance"].str.contains("[S12]", regex=False)).all()
    anchors = table[table["provenance"].str.contains(" ANCHOR row:", regex=False)]
    assert {(r.sex, int(r.age)): float(r.mort_rate)
            for r in anchors.itertuples()} == SOURCED_ANCHORS
    assert (table["age"].min(), table["age"].max()) == (19, 120)
    assert set(table["sex"]) == {"M", "F"}
    assert (table["mort_rate"] > 0.0).all()
    assert (table["acc_mort_rate"] <= table["mort_rate"]).all()

    for sex, target, population in (("M", 23.7, 19.5), ("F", 27.1, 23.7)):
        q = table[table["sex"] == sex].set_index("age")["mort_rate"]
        lives, expectation = 1.0, 0.0
        for x in range(65, 121):
            rate = min(1.0, float(q.loc[x]))
            expectation += lives * (1.0 - rate / 2.0)
            lives *= (1.0 - rate)
        assert expectation == pytest.approx(target, abs=5e-4), sex
        assert expectation - population > 3.0


def test_the_rate_class_relativities_are_sourced_ratios(term_life):
    """Korea publishes the mortality behind its preferred classes; the ratios are read off it.

    Both a ``mort_ratio`` and a ``prem_ratio`` are shipped, and the premium ratio **exceeds**
    the mortality ratio in every cell, because the expense loading does not scale with the
    risk.  Holding the ratios flat across ages is the only [std] step, the disclosures being
    at three ages between which the ratios move little.
    """
    table = term_life.Data.rate_class_table()
    classes = ("standard", "nonsmoker", "preferred", "super_preferred")
    assert set(table.index) == {(c, s) for c in classes for s in ("M", "F")}
    assert table["provenance"].notna().all()
    for sex in ("M", "F"):
        assert float(table.loc[("standard", sex), "mort_ratio"]) == 1.0
        assert float(table.loc[("standard", sex), "prem_ratio"]) == 1.0
        for cls in classes[1:]:
            mort = float(table.loc[(cls, sex), "mort_ratio"])
            prem = float(table.loc[(cls, sex), "prem_ratio"])
            assert 0.0 < mort < 1.0 and 0.0 < prem < 1.0
        morts = [float(table.loc[(c, sex), "mort_ratio"]) for c in classes]
        assert morts == sorted(morts, reverse=True)
    p8 = term_life.Projection[8]
    assert p8.rate_class() == "super_preferred" and p8.sex() == "M"
    assert p8.class_mort_ratio() == pytest.approx(0.583077, abs=5e-7)
    assert p8.class_prem_ratio() == pytest.approx(0.586207, abs=5e-7)
    assert p8.mort_rate(1) == pytest.approx(
        0.85 * 0.583077 * p8.mort_rate_at_age(19), rel=1e-6)


# ---------------------------------------------------------------------------
# The sensitivities the notes tabulate


@pytest.mark.parametrize("factor", sorted(MORT_BE_SENSITIVITY))
def test_the_mortality_factor_sensitivity_the_notes_tabulate(factor):
    """+361,807.55 at 0.75, +117,619.70 at 0.85 and -247,394.11 at 1.00.

    The range crosses zero inside a plausible band and is more than five times the whole
    answer, which is why the notes name this the model's largest lever: the margin inside a
    Korean 예정 경험사망률 sits in a 기초서류 that is never published, so the factor cannot be
    argued from a stated adjustment the way ``jplib``'s can.
    """
    model = _reread("mbf%d" % round(factor * 100))
    try:
        model.Projection.mort_be_factor = factor
        model.Projection.clear_all()
        assert model.Projection[1].result_cf()["net_cf"].sum() == pytest.approx(
            MORT_BE_SENSITIVITY[factor], abs=WON)
    finally:
        model.close()


@pytest.mark.parametrize("d", sorted(DECLINE_SENSITIVITY))
def test_the_renewal_decline_sensitivity_the_notes_tabulate(d):
    """Net cash flow and premium income at d = 0%, 5%, 20% and 40% on the 갱신형 anchor.

    A factor of 4.4 across a range no document narrows, driven almost entirely by premium
    income — 19.81m to 6.24m won.  The rate is published nowhere in Korea for any product,
    the mandatory disclosure requiring the **price** path and not the persistency path, so
    the sensitivity is the honest form of the answer.
    """
    net_cf, premiums = DECLINE_SENSITIVITY[d]
    model = _reread("dec%d" % round(d * 100))
    try:
        model.Projection.renewal_decline_base = d
        model.Projection.clear_all()
        df = model.Projection[3].result_cf()
        assert df["net_cf"].sum() == pytest.approx(net_cf, abs=WON)
        assert df["premiums"].sum() == pytest.approx(premiums, abs=WON)
    finally:
        model.close()


@pytest.mark.parametrize("factor", sorted(LAPSE_BE_SENSITIVITY))
def test_the_lapse_level_sensitivity_is_third_order_and_that_is_the_finding(factor):
    """+116,375.66 / +117,619.70 / +114,628.90 over 0.5 / 1.0 / 2.0 — 3,000 won of range.

    On a no-surrender-value protection form a lapse forfeits a paying policy and saves its
    claims in nearly equal measure, so the leverage that dominates a savings chassis is
    third-order here.  The smallness is the finding: on a 무해지 form the lapse assumption is
    a CSM and 해약환급금준비금 question rather than a cash-flow one.
    """
    model = _reread("lbf%d" % round(factor * 10))
    try:
        model.Projection.lapse_be_factor = factor
        model.Projection.clear_all()
        total = model.Projection[1].result_cf()["net_cf"].sum()
        assert total == pytest.approx(LAPSE_BE_SENSITIVITY[factor], abs=WON)
        assert abs(total - TOTAL_NET_CF) < 0.03 * abs(TOTAL_NET_CF)
    finally:
        model.close()


def test_commission_at_a_gaengsin_is_off_and_changes_the_sign_when_switched_on():
    """Setting the rate to 0.60 turns year 11 from +56,307.38 to -31,466.88.

    A 갱신 is issued on a new product code, which argues for paying commission on it, and it
    takes no 고지, which argues against; no document discloses a scale at all, so the base run
    pays nothing and exposes the switch.  The sign flips at the first two boundaries and not
    at the third — by year 31 the repriced premium has grown enough to absorb it — which is
    worth pinning because the effect is easy to overstate.
    """
    model = _reread("comm")
    try:
        base = model.Projection[3]
        assert base.comm_new_term_rate == 0.0
        assert all(base.comm_new_term(t) == 0.0 for t in range(1, 41))
        before = {t: base.net_cf(t) for t in (11, 21, 31)}
        model.Projection.comm_new_term_rate = 0.60
        model.Projection.clear_all()
        p = model.Projection[3]
        for t in (10, 20, 30):
            assert p.comm_new_term(t + 1) == pytest.approx(
                0.60 * p.prem_pp(t + 1) * p.pols_if(t + 1), rel=1e-13)
            assert p.net_cf(t + 1) < before[t + 1]
        assert p.net_cf(11) < 0.0 and p.net_cf(21) < 0.0
        assert 0.0 < p.net_cf(31) < 0.02 * before[31]
        assert p.comm_new_term(1) == 0.0        # not the first cycle
        assert p.comm_new_term(12) == 0.0       # only the cycle's first year
        assert p.net_cf(11) == pytest.approx(-31466.88, abs=WON)
        assert p.result_cf()["net_cf"].sum() == pytest.approx(2295610.86, abs=WON)
        assert p.check_net_cf() is True
    finally:
        model.close()


def test_the_renewal_decline_elasticity_is_off_and_works_when_switched_on():
    """d = min(d_max, d_0 (P_a(k+1)/P_a(k))^beta); beta = 0 gives the flat 20%.

    The premium jump the elasticity responds to accelerates — 2.33, 2.67, 3.59 — so a
    non-zero beta makes the later boundaries shed more than the earlier ones, and
    ``renewal_decline_max`` is what stops it running away.  At beta = 2 every boundary is
    already at the cap, which is the behaviour the cap exists to produce.
    """
    model = _reread("beta")
    try:
        base = model.Projection[3]
        assert base.renewal_decline_beta == 0.0
        assert [base.renewal_decline_rate(t) for t in (10, 20, 30)] == [0.20] * 3
        model.Projection.renewal_decline_beta = 0.5
        model.Projection.clear_all()
        p = model.Projection[3]
        rates = [p.renewal_decline_rate(t) for t in (10, 20, 30)]
        assert rates == sorted(rates) and all(r < p.renewal_decline_max for r in rates)
        assert rates[0] == pytest.approx(0.20 * (252000.0 / 108000.0) ** 0.5, rel=1e-13)
        assert rates[-1] == pytest.approx(
            0.20 * (2412000.0 / 672000.0) ** 0.5, rel=1e-13)
        assert p.result_cf()["net_cf"].sum() < GAENGSIN_TOTAL_NET_CF
        assert p.check_decline_timing() is True
        model.Projection.renewal_decline_beta = 2.0    # above the cap everywhere
        model.Projection.clear_all()
        q = model.Projection[3]
        assert [q.renewal_decline_rate(t) for t in (10, 20, 30)] == [0.40] * 3
        assert q.result_cf()["net_cf"].sum() == pytest.approx(
            DECLINE_SENSITIVITY[0.40][0], abs=WON)
    finally:
        model.close()


# ---------------------------------------------------------------------------
# Documentation and inputs


def test_the_docstrings_carry_this_product_s_own_reference_material(term_life):
    """Product-specific phrases a reader relies on, which a generic sweep cannot know.

    The model docstring names the chassis and the 갱신형 split, the Projection docstring
    carries the notes' symbol map and the 보험나이 basis, and the Data docstring explains the
    layout it follows.  Asserted so that they cannot go stale silently while the numbers
    stay right.
    """
    doc = term_life.doc
    for phrase in ("mechanics demonstration", "external", "once per model",
                   "protection chassis", "갱신형", "비갱신형", "보험나이"):
        assert phrase in doc, phrase
    proj = term_life.Projection.doc
    assert "Notes symbol" in proj and "no tail state of any kind" in proj
    for cells in ("proj_len", "model_point", "pols_if", "term_index",
                  "renewal_decline_rate", "pols_lapse_pool", "prem_rate_mth",
                  "wop_waived_frac", "accel_share"):
        assert cells in proj, cells
    data = term_life.Data.doc
    assert "TradLife_A" in data
    for cells in ("input_dir", "model_point_table", "mort_table", "prem_rate_table",
                  "lapse_table", "rate_class_table"):
        assert cells in data, cells


def test_an_input_can_be_swapped_without_touching_formulas():
    """Point a filename Reference at a different file and the projection follows.

    This is the property the external-file layout buys, and it is what a user with a company
    mortality basis does: a same-schema CSV drops in with no formula change.  It is also the
    mechanism the truncation test above uses to supply a model point the shipped table does
    not carry.
    """
    doubled = pd.read_csv(CSV_DIR / "mort_table.csv", index_col=["sex", "age"])
    doubled["mort_rate"] = doubled["mort_rate"] * 2
    model = _reread("swap")
    alt_name = "mort_table_doubled.csv"
    try:
        alt_path = model.Data.input_dir() / alt_name
        doubled.to_csv(alt_path)
        try:
            base = model.Projection[1].claims(1, "DEATH")
            model.Data.mort_table_file = alt_name
            model.Data.clear_all()
            model.Projection.clear_all()
            assert model.Projection[1].claims(1, "DEATH") == pytest.approx(
                2 * base, rel=1e-12)
        finally:
            alt_path.unlink(missing_ok=True)
    finally:
        model.close()


def test_the_model_point_table_exercises_the_product(term_life):
    """Both sexes, both renewal structures, both boundaries, both forms, every module.

    The table is the model's coverage statement, so what it must contain is asserted here
    rather than left to a reader counting rows.
    """
    table = term_life.Data.model_point_table()
    assert len(table) == 10 and list(table.index) == list(range(1, 11))
    assert set(table["sex"]) == {"M", "F"}
    assert set(table["renewal_type"]) == {"gaengsin", "bi_gaengsin"}
    assert set(table["contract_boundary"]) == {"ceiling", "current_term"}
    assert set(table["maturity_form"]) == {"pure", "rop"}
    assert set(table["rate_class"]) == {"standard", "nonsmoker", "preferred",
                                        "super_preferred"}
    for module in ("acc_death", "waiver", "accel", "reinstatement"):
        assert set(table[module]) == {0, 1}, f"{module} is not exercised both ways"
    assert table["issue_age"].min() == 19 and table["issue_age"].max() == 65
    assert table["sum_assured"].min() == 30000000
    assert table["sum_assured"].max() == 500000000
    assert set(table["term_y"] > 0) == {True, False}       # 년만기 and 세만기
    assert set(table["pay_term_y"] > 0) == {True, False}   # 전기납 and shortened pay
