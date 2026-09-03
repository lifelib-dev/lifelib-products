"""Golden and structural tests for Pension_KR_A.

The golden values are the worked example in
products/pension_savings/technical-notes.md ("Worked example"), which projects the anchor
cell: male, 보험나이 40 at issue, level 기본보험료 KRW 6,000,000 a year (KRW 500,000 a
month) for twenty years, a five-year gap to a 연금개시일 at 보험나이 65, and a 종신연금형
with a ten-year 보증지급기간.  The premium is not a standardization: it is the
annualisation of a published illustration at an identical model point, and it is exactly
the ₩6,000,000 세액공제 ceiling, so the anchor saver sits on the corner of the tax
schedule.  The values are hard-coded here rather than pickled so that a reviewer can
compare them against the notes by eye.

Tolerances follow the precision the notes display: money to the won's second decimal,
counts and rates to the ten decimals the notes print them at, and the annuitisation
quantities — which the notes print to ten decimals on numbers of order 1e8, past what a
float64 can carry — to a relative tolerance of one part in 1e15, which is the same double.

This is the library's **deferred tax-qualified accumulation contract**, and it inherits
the accumulation half of the whole life chassis rather than restating it, so this module
asserts what this product adds: crediting at the 공시이율 over a stepped 최저보증이율, the
annuitisation step and its 100.1%-of-premiums floor, the monthly annuity factor that
reconstructs eight published implied factors on two interest bases, and the tax layer that
is a policyholder-behaviour driver and never an insurer cash flow.

Beyond the worked example, every product fact the notes list under "Known modeling
pitfalls" earns its own test, named after the pitfall, because each is a way an
implementation can look right and be wrong:

* a survivorship release in the fund — the 계약자적립액 is an **account**, and the
  Japanese deferred annuity's ``/(1 - q')`` overstates the 연금개시 fund silently;
* a deferral-phase mortality strain, which on this contract is exactly zero;
* a death product's best-estimate adjustment, whose **sign** is wrong here;
* the decrement order — deaths from the whole opening in-force, surrenders from the
  survivors;
* stopping the lapse decrement a year early, which deletes a real ₩987,174.98 payment;
* an **annual** annuity-due factor, which is the error ``product-spec.md`` contains;
* mortality in the 확정기간 factor, or none in the 종신 one — a factor of two and a half;
* decrementing ``pols_if`` inside a guaranteed or certain period;
* recomputing ``B``, or keeping the fund alive after annuitisation;
* forgetting that the maintenance charge outlives the premium;
* forgetting that the acquisition charge stops at seven years;
* treating the 최저보증이율 as a guarantee on the **return** rather than the credited rate;
* mistaking the 예정이율 — or the 평균공시이율 — for a crediting rate;
* putting the tax layer into the cash flow;
* applying the 연금수령한도 formula where the statute disapplies it;
* computing the 표준해약공제액 on the **gross** premium rather than the 연납순보험료;
* reading ``proj_len()`` as a count rather than as the last index;
* and assuming the 100.1% floor protects a **death** claim, which it does not.

The nine ``check_*`` cells this model publishes are asserted **by name**, because a
generic sweep cannot notice a check that has quietly disappeared, and the [std] scalar
assumptions the notes state are read off the model, so that a silent change to an
assumption fails a test rather than moving a result.
"""
import contextlib

import modelx as mx
import pandas as pd
import pytest
from modelx.core.errors import FormulaError

from kr_registry import LIB, MODELS

WON = 0.005          # money displayed to 2 d.p.
INFORCE = 5e-11      # counts and probabilities, displayed to 10 d.p.
RATE = 5e-11         # decrement and crediting rates, displayed to 10 d.p.
SAME_DOUBLE = 1e-15  # relative: the notes' full-precision values are these doubles

MODEL_DIR = LIB / MODELS["Pension_KR_A"][0]
CSV_DIR = MODEL_DIR.parent

# ---------------------------------------------------------------------------
# The notes' worked example, anchor cell (point_id = 1)

# "Annuitisation quantities, at full precision, all read off the model".
CUM_PREM_AT_N = 120000000.0000000000
AV_AT_PAID_UP = 144311957.5668485165      # av_pp(20), 납입완료
AV_AT_COMMENCEMENT = 160294805.5909655988  # av_pp(25), 연금개시
MIN_FUND = 120119999.9999999851           # 100.1% of premiums paid; not binding
ANNUITY_FUND = 160294805.5909655988       # F, after the floor
ANNUITY_FACTOR = 23.58191601796395        # adue, monthly, 종신 g = 10, issue vintage
ANNUITY_AMOUNT = 6763374.5893045263       # B, 연금연액, struck once at t = n
ANNUITY_MONTH = 563614.5491087105
IMPLIED_FACTOR = 23.7004181085            # F / B, against a published 23.70
GUARANTEED_TOTAL = 67633745.8930452615    # 10B, 42.19% of F
CERTAIN_FACTOR_10 = 9.015951040563765     # the ten-year certain factor on the same fund
SURR_CHG_CAP = 1421988.7174578153         # 표준해약공제액, 별표 14
TAX_CREDIT_PA = 990000.0000000000         # 세액공제; not an insurer cash flow
SURR_TAX_AT_10 = 10590733.1198662240      # 기타소득세; not an insurer cash flow

# The premium net of both charges, and the charge the fund pays after 납입완료.
U_FACTOR = 0.990316187680581               # prem_timing_factor, twelve monthly instalments
NP_WITH_ACQ = 5674511.7554097297           # t = 0..6
NP_AFTER_ACQ = 5763640.2123009823          # t = 7..19
CHARGE_PAID_UP = 39810.7107447594          # t = 20..24, taken from the 적립액

# "Deferral phase, the first eleven years": t -> (pols_if, premiums, claims_death,
# claims_lapse, expenses, claim_expenses, net_cf).  claims_annuity, commissions and
# policy_loans are 0.00 in every one of these rows.
WORKED_EXAMPLE_DEFERRAL = {
    0:  (1.0000000000, 6000000.00,  4674.99,  231673.55, 230000.00, 24.20, 5533627.26),
    1:  (0.9592257427, 5755354.46,  9270.29,  393071.13,  29352.31, 23.73, 5323636.99),
    2:  (0.9248893924, 5549336.35, 13884.90,  492533.66,  28867.65, 23.45, 5014026.70),
    3:  (0.8963846174, 5378307.70, 18618.45,  536123.38,  28537.52, 23.33, 4795005.03),
    4:  (0.8732168767, 5239301.26, 23575.35,  659909.74,  28355.94, 23.38, 4527436.85),
    5:  (0.8506267363, 5103760.42, 28720.33,  623835.27,  28174.82, 23.48, 4423006.52),
    6:  (0.8328473436, 4997084.06, 34268.90,  720369.62,  28137.64, 23.75, 4214284.16),
    7:  (0.8154145906, 4892487.54, 40222.79,  816351.98,  28099.65, 24.08, 4007789.04),
    8:  (0.7983196126, 4789917.68, 46568.20,  910297.18,  28060.76, 24.48, 3804967.06),
    9:  (0.7815535795, 4689321.48, 53366.48, 1002232.72,  28020.87, 24.94, 3605676.47),
    10: (0.7651077050, 4590646.23, 60688.75,  819137.74,  27979.86, 25.48, 3682814.39),
}

# "The rows where the product does something": t -> (pols_if, premiums, claims_annuity,
# claims_death, claims_lapse, expenses, net_cf).
WORKED_EXAMPLE_EVENTS = {
    6:  (0.8328473436, 4997084.06,       0.00,  34268.90,  720369.62, 28137.64,
         4214284.16),
    7:  (0.8154145906, 4892487.54,       0.00,  40222.79,  816351.98, 28099.65,
         4007789.04),
    19: (0.6595725461, 3957435.28,       0.00, 174520.48, 1425145.27, 28826.18,
         2328907.07),
    20: (0.6484877699,       0.00,       0.00, 187658.61,  953825.77, 28908.56,
         -1170431.14),
    21: (0.6407422762,       0.00,       0.00, 203261.34,  962296.51, 29134.55,
         -1194732.91),
    24: (0.6174807928,       0.00,       0.00, 261465.85,  987174.98, 29795.37,
         -1278485.13),
    25: (0.6096911403,       0.00, 4123569.57,      0.00,       0.00, 20005.26,
         -4143574.82),
    26: (0.6096911403,       0.00, 4123569.57,      0.00,       0.00, 20405.36,
         -4143974.93),
    33: (0.6096911403,       0.00, 4123569.57,      0.00,       0.00, 23439.35,
         -4147008.91),
    34: (0.6096911403,       0.00, 4123569.57,      0.00,       0.00, 23908.14,
         -4147477.70),
    35: (0.5837918602,       0.00, 3948403.03,      0.00,       0.00, 23350.38,
         -3971753.42),
    36: (0.5797787348,       0.00, 3921260.76,      0.00,       0.00, 23653.67,
         -3944914.43),
    79: (0.0023319211,       0.00,   15771.66,      0.00,       0.00,   222.92,
         -15994.58),
    80: (0.0012516484,       0.00,    8465.37,      0.00,       0.00,   122.05,
         -8587.41),
}

# "The fund, the surrender value and the 환급률": t -> (cum_prem_pp, av_pp, 환급률).
# av_pp, cv_pp and db_pp are the same number at every duration on this composite.
WORKED_EXAMPLE_FUND = {
    0:  (0.0,             0.00,         None),
    1:  (6000000.00,      5796513.76,   0.966086),
    2:  (12000000.00,     11717652.56,  0.976471),
    3:  (18000000.00,     17766095.85,  0.987005),
    4:  (24000000.00,     23944580.67,  0.997691),
    5:  (30000000.00,     30255902.91,  1.008530),
    6:  (36000000.00,     36702918.58,  1.019526),
    7:  (42000000.00,     43288545.09,  1.030680),
    10: (60000000.00,     64186261.33,  1.069771),
    15: (90000000.00,     102120559.88, 1.134673),
    19: (114000000.00,    135510914.43, 1.188692),
    20: (120000000.00,    144311957.57, 1.202600),
    21: (120000000.00,    147373998.01, 1.228117),
    24: (120000000.00,    156960814.72, 1.308007),
    25: (120000000.00,    160294805.59, 1.335790),
    26: (120000000.00,    0.00,         None),
}

# "Decrements at the same durations": t -> (mort_rate, lapse_rate, pols_death, pols_lapse,
# lives_if).
WORKED_EXAMPLE_DECREMENTS = {
    0:  (0.0008065180, 0.0400000000, 0.0008065180, 0.0399677393, 1.0000000000),
    1:  (0.0008247685, 0.0350000000, 0.0007911392, 0.0335452111, 0.9991934820),
    5:  (0.0009199195, 0.0200000000, 0.0007825081, 0.0169968846, 0.9957710983),
    10: (0.0011100950, 0.0150000000, 0.0008493422, 0.0114638754, 0.9908608859),
    19: (0.0018335025, 0.0150000000, 0.0012093279, 0.0098754483, 0.9786482084),
    20: (0.0019635675, 0.0100000000, 0.0012733495, 0.0064721442, 0.9768538545),
    24: (0.0026416305, 0.0100000000, 0.0016311561, 0.0061584964, 0.9683012203),
    25: (0.0028596130, 0.0000000000, 0.0000000000, 0.0000000000, 0.9657433263),
    34: (0.0062631185, 0.0000000000, 0.0258992801, 0.0000000000, 0.9305473107),
    35: (0.0068742400, 0.0000000000, 0.0040131254, 0.0000000000, 0.9247191826),
    80: (1.0000000000, 0.0000000000, 0.0012516484, 0.0000000000, 0.0019825957),
}

# "Undiscounted totals, t = 0 .. 80".
WORKED_EXAMPLE_TOTALS = {
    "premiums": 95084920.7600,
    "claims_annuity": 136717952.0369,
    "claims_death": 2486087.7722,
    "claims_lapse": 22509174.0135,
    "expenses": 1887294.7545,
    "claim_expenses": 756.7500,
    "commissions": 0.0000,
    "policy_loans": 0.0000,
    "net_cf": -68516344.5672,
}

# "The nine model points": point_id -> (sex, x, m, d, n, Y, P, proj_len, F, adue, B,
# sum net_cf).
MODEL_POINTS = {
    1: ("M", 40, 20,  5, 25, 65,  6000000.0, 80, 160294805.59, 23.58192,  6763374.59,
        -68516344.57),
    2: ("F", 40, 20,  5, 25, 65,  6000000.0, 80, 160294805.59, 25.26673,  6312383.96,
        -73799636.48),
    3: ("M", 45, 20,  0, 20, 65,  3600000.0, 75,  86587174.54, 24.08957,  3576412.79,
        -34649402.87),
    4: ("F", 25, 20, 15, 35, 60,  1200000.0, 54,  39568543.38, 16.30428,  2414746.68,
        -16598163.32),
    5: ("M", 30, 10, 20, 30, 60, 12000000.0, 39, 194438355.78,  9.01595, 21458209.25,
        -45678507.48),
    6: ("F", 50,  5,  0,  5, 55,  6000000.0, 19,  30030000.00, 13.94004,  2143455.00,
        -2440820.60),
    7: ("M", 40, 20,  5, 25, 65,  6000000.0, 80, 160294805.59, 24.30417,  6562384.22,
        -70853187.86),
    8: ("M", 40, 20,  5, 25, 65,  6000000.0, 80, 326721162.46, 23.58192, 13785459.86,
        -141563203.47),
    9: ("M", 40, 20,  5, 27, 65,  6000000.0, 80, 162892867.42, 22.70113,  4266770.29,
        -37607123.25),
}

# "Eight published figures, one formula, two interest bases and both annuity forms":
# (payout_form, term, rate_scenario) -> the published implied factor F / B, which is the
# model's own annuity factor grossed up for the 0.5% 연금수령기간 관리비용.
PUBLISHED_IMPLIED_FACTORS = {
    ("certain",   10, "base"):  9.06,
    ("certain",   15, "base"):  12.92,
    ("certain",   20, "base"):  16.39,
    ("certain",   10, "floor"): 9.81,
    ("certain",   15, "floor"): 14.53,
    ("certain",   20, "floor"): 19.13,
    ("life_guar", 10, "base"):  23.70,
    ("life_guar", 10, "floor"): 31.18,
}
# The same eight, at the precision the notes' own "Model" column prints them.
RECONSTRUCTED_IMPLIED_FACTORS = {
    ("certain",   10, "base"):  9.061,
    ("certain",   15, "base"):  12.918,
    ("certain",   20, "base"):  16.386,
    ("certain",   10, "floor"): 9.806,
    ("certain",   15, "floor"): 14.528,
    ("certain",   20, "floor"): 19.134,
    ("life_guar", 10, "base"):  23.700,
    ("life_guar", 10, "floor"): 31.180,
}

# The nine check cells this model publishes.  Every one of them carries a per-t residual.
CHECKS = {
    "check_pols_roll_fwd",
    "check_av_roll_fwd",
    "check_cv_floor",
    "check_surr_chg_cap",
    "check_min_fund",
    "check_annuity_total",
    "check_annuity_limit",
    "check_mort_law",
    "check_net_cf",
}

# The scalar assumptions the notes mark [std] — a modeller's choice with no contractual
# counterpart — read off the model so a silent change fails a test.
STD_SCALARS = {
    "mort_be_factor": 1.15,
    "loan_rate": 0.04,
    "loan_draw_frac": 0.50,
    "loan_draw_year": 15,
    "holiday_start_year": 8,
}
STD_EXPENSES = {
    "expense_acq": 200000.0,
    "expense_maint_defer": 30000.0,
    "expense_maint_payout": 20000.0,
    "expense_claim": 30000.0,
    "inflation_rate": 0.02,
}

# The scalar parameters the notes cite to a document rather than standardize.  A [std] tag
# on any of these would be a claim that the sources do not say what they say.
SOURCED_SCALARS = {
    "prem_freq": 12,
    "annuity_freq": 12,
    "prem_int_rate": 0.0250,
    "avg_decl_rate": 0.0250,
    "acq_charge_rate": 0.0150,
    "acq_charge_years": 7,
    "maint_charge_rate": 0.0300,
    "maint_charge_rate_paid_up": 0.0067,
    "addl_charge_rate": 0.0200,
    "addl_prem_cap_ratio": 2.00,
    "annuity_charge_rate": 0.0050,
    "min_fund_ratio": 1.001,
    "surr_chg_years": 5,
    "surr_chg_cap_rate": 0.03,
    "surr_chg_cap_rate_par": 0.04,
    "surr_chg_cap_term_cap": 12,
    "surr_chg_cap_level_years": 10,
    "holiday_max_years": 3,
    "div_int_rate": 0.0215,
}

# The tax basis of class (a) and the statutory tests, none of which is an insurer cash flow.
TAX_SCALARS = {
    "credit_rate_low_income": 0.165,
    "credit_rate_high_income": 0.132,
    "credit_cap": 6000000.0,
    "contribution_ceiling": 18000000.0,
    "other_income_tax_rate": 0.165,
    "pension_tax_rate_under70": 0.055,
    "pension_tax_rate_70to79": 0.044,
    "pension_tax_rate_80plus": 0.033,
    "pension_tax_rate_life": 0.033,
    "min_annuity_age": 55,
    "min_account_years": 5,
    "limit_denominator_base": 11,
    "limit_uplift": 1.20,
}

# The 표준해약공제액, computed in full by 별표 14 at the anchor cell.
SURR_CAP_WORKINGS = {
    "whole_term_loading": 4230000.00,     # 6,000,000 x (0.045 x 7 + 0.030 x 13)
    "levelled": 423000.00,                # over min(m, 10)
    "net_annual_premium": 5577000.00,     # 연납순보험료, 주3
    "gross_cap": 2007720.00,              # 3% x 연납순보험료 x min(m, 12), 주2 and 주5
    "note_6_deduction": 585731.28,        # the discounted acquisition loading, 주6
    "cap": 1421988.72,
}


def _reread(suffix):
    """A private copy of the model, for tests that move a Reference or rewrite an input."""
    return mx.read_model(MODEL_DIR, name="Pension_KR_A_" + suffix)


@contextlib.contextmanager
def alt_model_points(suffix, overrides):
    """A private model projecting model points the shipped table does not carry.

    ``overrides`` maps a new ``point_id`` to a dict of columns to change on the anchor
    row.  The point is supplied through the ``model_point_file`` Reference, which is the
    same swappable-input property the library advertises, and the temporary CSV is removed
    again so that the directory keeps the exact file set the conventions suite asserts.
    """
    src = pd.read_csv(CSV_DIR / "model_point_table.csv", index_col="point_id")
    rows, index = [], []
    for point_id, changes in sorted(overrides.items()):
        row = src.loc[1].copy()
        row["policy_id"] = "KR-PEN-%04d" % point_id
        for column, value in changes.items():
            row[column] = value
        rows.append(row)
        index.append(point_id)
    frame = pd.DataFrame(rows)
    frame.index = pd.Index(index, name="point_id")

    model = _reread(suffix)
    alt_name = "model_point_table_%s.csv" % suffix
    alt_path = model.Data.input_dir() / alt_name
    try:
        frame.to_csv(alt_path)
        model.Data.model_point_file = alt_name
        model.Data.clear_all()
        model.Projection.clear_all()
        yield model
    finally:
        alt_path.unlink(missing_ok=True)
        model.close()


# ---------------------------------------------------------------------------
# The worked example — the annuitisation quantities


def test_worked_example_annuitisation_quantities(kr_pension_anchor):
    """The notes' full-precision annuitisation table, cell by cell.

    This is the transition the whole product turns on and the only place the model can be
    checked against the public record: the implied factor ``F / B`` of 23.7004181085
    reproduces the one published annuitisation illustration's 23.70, and ``B / F`` of
    0.0421933485 reproduces its 0.042194 to five decimal places.  Every other number here
    feeds it, so a silent change anywhere in the deferral phase surfaces as one of these.
    """
    a = kr_pension_anchor
    assert a.cum_prem_pp(25) == pytest.approx(CUM_PREM_AT_N, rel=SAME_DOUBLE)
    assert a.av_pp(20) == pytest.approx(AV_AT_PAID_UP, rel=SAME_DOUBLE)
    assert a.av_pp(25) == pytest.approx(AV_AT_COMMENCEMENT, rel=SAME_DOUBLE)
    assert a.min_fund_pp() == pytest.approx(MIN_FUND, rel=SAME_DOUBLE)
    assert a.annuity_fund_pp() == pytest.approx(ANNUITY_FUND, rel=SAME_DOUBLE)
    assert a.annuity_fund_net_pp() == pytest.approx(ANNUITY_FUND, rel=SAME_DOUBLE)
    assert a.annuity_due_factor() == pytest.approx(ANNUITY_FACTOR, rel=SAME_DOUBLE)
    assert a.annuity_amount_pp() == pytest.approx(ANNUITY_AMOUNT, rel=SAME_DOUBLE)
    assert a.annuity_amount_pp() / 12 == pytest.approx(ANNUITY_MONTH, rel=SAME_DOUBLE)
    assert a.annuity_due_certain_factor() == pytest.approx(
        CERTAIN_FACTOR_10, rel=SAME_DOUBLE)
    assert a.surr_chg_cap_pp() == pytest.approx(SURR_CHG_CAP, rel=SAME_DOUBLE)
    # The floor does not bind, with a third to spare, and it is not decorative elsewhere.
    assert a.annuity_fund_pp() > a.min_fund_pp()
    assert a.annuity_fund_pp() / a.min_fund_pp() == pytest.approx(1.334, abs=0.001)
    # The published calibration, and the guaranteed total the contract warns may be less
    # than the fund: 10B is 42.19% of F.
    assert a.annuity_fund_pp() / a.annuity_amount_pp() == pytest.approx(
        IMPLIED_FACTOR, abs=5e-11)
    assert a.annuity_amount_pp() / a.annuity_fund_pp() == pytest.approx(
        0.042194, abs=5e-6)
    assert 10 * a.annuity_amount_pp() == pytest.approx(GUARANTEED_TOTAL, rel=SAME_DOUBLE)
    assert 10 * a.annuity_amount_pp() / a.annuity_fund_pp() == pytest.approx(
        0.4219, abs=5e-5)


def test_worked_example_the_tax_quantities_are_published_and_are_not_cash_flows(
        kr_pension_anchor):
    """세액공제 ₩990,000 a year, 기타소득세 ₩10,590,733.12 at t = 10, 연금소득세 3.3%.

    The notes print all four in the annuitisation table and none of them in the cash flow,
    which is the whole point of carrying them: they are what drives the lapse assumption
    and the annuitisation election, and neither passes through the insurer's account.
    """
    a = kr_pension_anchor
    assert a.tax_credit_pp(0) == pytest.approx(TAX_CREDIT_PA, rel=SAME_DOUBLE)
    assert a.surr_tax_pp(10) == pytest.approx(SURR_TAX_AT_10, rel=SAME_DOUBLE)
    assert a.pension_tax_rate(25) == pytest.approx(0.033, abs=RATE)
    assert a.annuity_year_no(25) == 11
    # The credit is a flat 16.5% of a contribution capped at the ceiling, over m years.
    assert a.tax_credit_pp(19) == pytest.approx(TAX_CREDIT_PA, rel=SAME_DOUBLE)
    assert a.tax_credit_pp(20) == 0.0
    assert sum(a.tax_credit_pp(t) for t in range(0, a.proj_len() + 1)) == pytest.approx(
        19800000.0, abs=WON)
    # 16.5% of the surrender value, so the net proceeds are the 83.5% the one published
    # 세후지급 예상액 column shows at every duration.
    assert a.surr_tax_pp(10) == pytest.approx(0.165 * a.cv_pp(10), rel=SAME_DOUBLE)


# ---------------------------------------------------------------------------
# The worked example — the cash flow statement


@pytest.mark.parametrize("t", sorted(WORKED_EXAMPLE_DEFERRAL))
def test_worked_example_deferral_row(kr_pension_anchor, t):
    """Every cell of the notes' eleven-row deferral table, at the precision it prints.

    The row is read off the published ``result_cf()`` frame as well as off the cells, so
    the table a reader has in front of them is the table the model publishes rather than
    a parallel computation that happens to agree.
    """
    pols_if, premiums, death, lapse, expenses, claim_exp, net = WORKED_EXAMPLE_DEFERRAL[t]
    a = kr_pension_anchor
    assert a.pols_if(t) == pytest.approx(pols_if, abs=INFORCE)
    assert a.premiums(t) == pytest.approx(premiums, abs=WON)
    assert a.claims(t, "DEATH") == pytest.approx(death, abs=WON)
    assert a.claims(t, "LAPSE") == pytest.approx(lapse, abs=WON)
    assert a.expenses(t) == pytest.approx(expenses, abs=WON)
    assert a.claim_expenses(t) == pytest.approx(claim_exp, abs=WON)
    assert a.net_cf(t) == pytest.approx(net, abs=WON)
    # The deferral phase carries no annuity, no commission and no loan.
    assert a.claims(t, "ANNUITY") == 0.0
    assert a.commissions(t) == 0.0
    assert a.policy_loans(t) == 0.0

    row = a.result_cf().loc[t]
    assert row["pols_if"] == pytest.approx(pols_if, abs=INFORCE)
    assert row["premiums"] == pytest.approx(premiums, abs=WON)
    assert row["claims_death"] == pytest.approx(death, abs=WON)
    assert row["claims_lapse"] == pytest.approx(lapse, abs=WON)
    assert row["net_cf"] == pytest.approx(net, abs=WON)


@pytest.mark.parametrize("t", sorted(WORKED_EXAMPLE_EVENTS))
def test_worked_example_event_row(kr_pension_anchor, t):
    """"The rows where the product does something" — the notes' second table, row by row.

    These are the fourteen rows that carry the contract's structure: the 계약체결비용
    stopping at t = 7, the last premium at t = 19, 납입완료 at t = 20 and the first
    negative net cash flow of the projection, the 연금개시일 at t = 25, the last guaranteed
    instalment at t = 34, and the terminal row at t = 80 where q = 1.
    """
    pols_if, premiums, annuity, death, lapse, expenses, net = WORKED_EXAMPLE_EVENTS[t]
    a = kr_pension_anchor
    assert a.pols_if(t) == pytest.approx(pols_if, abs=INFORCE)
    assert a.premiums(t) == pytest.approx(premiums, abs=WON)
    assert a.claims(t, "ANNUITY") == pytest.approx(annuity, abs=WON)
    assert a.claims(t, "DEATH") == pytest.approx(death, abs=WON)
    assert a.claims(t, "LAPSE") == pytest.approx(lapse, abs=WON)
    assert a.expenses(t) == pytest.approx(expenses, abs=WON)
    assert a.net_cf(t) == pytest.approx(net, abs=WON)
    assert a.result_cf().loc[t, "net_cf"] == pytest.approx(net, abs=WON)


def test_worked_example_the_four_regimes_the_notes_read_off_the_shape(kr_pension_anchor):
    """A positive year 0, twenty declining years, five thin negative ones, then outgo.

    Each regime is a contractual fact rather than an artefact, and the boundaries are
    dated: 납입완료 at t = 20 is the first row with no premium and the first negative
    ``net_cf``; the 연금개시일 at t = 25 is where the fund disappears into the annuity.
    Asserting the *signs* by regime is what catches a projection whose phases have slipped
    a year without any single row looking wrong.
    """
    a = kr_pension_anchor
    df = a.result_cf()
    assert df.loc[0, "net_cf"] == pytest.approx(5533627.26, abs=WON)
    assert all(df.loc[t, "net_cf"] > 0 for t in range(0, 20))
    assert df.loc[19, "net_cf"] == pytest.approx(2328907.07, abs=WON)
    assert all(df.loc[t, "net_cf"] < 0 for t in range(20, 81))
    # The five thin negative years between 납입완료 and 연금개시, and what they cost.
    assert df.loc[20:24, "net_cf"].sum() == pytest.approx(-6112938.99, abs=WON)
    assert a.av_pp(25) - a.av_pp(20) == pytest.approx(15982848.02, abs=WON)
    # Then fifty-six years of pure outgo, flat in B and declining in count.
    assert df.loc[25:, "net_cf"].sum() == pytest.approx(-137688724.63, abs=WON)
    # net_cf rises at t = 10, which is the lapse rate stepping down and not a fund effect.
    assert df.loc[10, "net_cf"] > df.loc[9, "net_cf"]
    assert a.lapse_rate(9) == pytest.approx(0.02, abs=RATE)
    assert a.lapse_rate(10) == pytest.approx(0.015, abs=RATE)
    # By the last premium year the surrender payment is more than a third of the premium.
    assert df.loc[19, "claims_lapse"] / df.loc[19, "premiums"] > 1 / 3


def test_worked_example_totals(kr_pension_anchor):
    """The notes' undiscounted totals, column by column, and the three ratios beside them.

    A total is the one number a reader checks with a calculator, and it is also the only
    place a sign error in a single distant row shows up as anything at all.
    """
    df = kr_pension_anchor.result_cf()
    for column, total in WORKED_EXAMPLE_TOTALS.items():
        assert df[column].sum() == pytest.approx(total, abs=WON), column
    assert df["net_cf"].sum() == pytest.approx(-68516344.5672, abs=WON)
    # premiums is 79.24% of the ₩120,000,000 nominal, the difference being the decrements.
    assert df["premiums"].sum() / 120000000.0 == pytest.approx(0.7924, abs=5e-5)
    # claims_annuity is B times the sum of pols_if over the payout phase.
    pols = sum(kr_pension_anchor.pols_if(t) for t in range(25, 81))
    assert pols == pytest.approx(20.2145, abs=5e-5)
    assert df["claims_annuity"].sum() == pytest.approx(
        kr_pension_anchor.annuity_amount_pp() * pols, abs=WON)
    # claims_lapse is nine times claims_death on decrements whose rates differ by fifty.
    assert df["claims_lapse"].sum() / df["claims_death"].sum() == pytest.approx(
        9.054, abs=5e-4)
    # Undiscounted the projection is a large negative; at the rate the fund credits it is
    # a small positive, and that pair is the product in one line.
    discounted = sum(df.loc[t, "net_cf"] / 1.0215 ** t for t in df.index)
    assert discounted == pytest.approx(2913938.37, abs=WON)


# ---------------------------------------------------------------------------
# The worked example — the fund and the decrements


@pytest.mark.parametrize("t", sorted(WORKED_EXAMPLE_FUND))
def test_worked_example_fund_row(kr_pension_anchor, t):
    """cum_prem_pp, av_pp = cv_pp = db_pp and the 환급률, at the notes' own durations.

    The 환급률 — ``cv_pp(t) / cum_prem_pp(t)``, the ratio a Korean illustration quotes —
    crosses 100% in the **fifth** policy year at 100.85%, having been 96.61% after one.
    That crossing is the whole visible signature of the adopted expense schedule, so it is
    asserted as a shape and not only as a number.
    """
    cum_prem, fund, ratio = WORKED_EXAMPLE_FUND[t]
    a = kr_pension_anchor
    assert a.cum_prem_pp(t) == pytest.approx(cum_prem, abs=WON)
    assert a.av_pp(t) == pytest.approx(fund, abs=WON)
    # One number carries all three on this composite, because 해약공제액 is nil.
    assert a.cv_pp(t) == pytest.approx(fund, abs=WON)
    assert a.db_pp(t) == pytest.approx(fund, abs=WON)
    assert a.surr_chg_pp(t) == 0.0
    if ratio is not None:
        assert a.cv_pp(t) / a.cum_prem_pp(t) == pytest.approx(ratio, abs=5e-7)


def test_worked_example_the_hwangeupryul_crosses_a_hundred_in_the_fifth_year(
        kr_pension_anchor):
    """96.61% after one year, break-even in the fifth, against a published 96.7% / fourth.

    The published curve is the same product's own at a 2.40% declared rate; the composite
    runs at 2.15%, and a quarter of a point of interest is worth about a year of
    break-even on this design.  A model whose loading is level rather than front-loaded
    cannot produce this shape at all.
    """
    a = kr_pension_anchor
    ratios = {t: a.cv_pp(t) / a.cum_prem_pp(t) for t in range(1, 21)}
    assert ratios[1] == pytest.approx(0.966086, abs=5e-7)
    assert all(ratios[t] < 1.0 for t in (1, 2, 3, 4))
    assert ratios[5] == pytest.approx(1.008530, abs=5e-7)
    assert all(ratios[t] > ratios[t - 1] for t in range(2, 21))


@pytest.mark.parametrize("t", sorted(WORKED_EXAMPLE_DECREMENTS))
def test_worked_example_decrement_row(kr_pension_anchor, t):
    """mort_rate, lapse_rate, pols_death, pols_lapse and lives_if, to ten decimals.

    ``pols_if`` and ``lives_if`` are two different measures and the notes print both: at
    the 연금개시일 the first is 0.6096911403 and the second 0.9657433263, because a
    surrender removes a contract without removing a life.  Collapsing them is the first
    pitfall on this product and this table is where it would show.
    """
    mort, lapse, death, surrender, lives = WORKED_EXAMPLE_DECREMENTS[t]
    a = kr_pension_anchor
    assert a.mort_rate(t) == pytest.approx(mort, abs=RATE)
    assert a.lapse_rate(t) == pytest.approx(lapse, abs=RATE)
    assert a.pols_death(t) == pytest.approx(death, abs=INFORCE)
    assert a.pols_lapse(t) == pytest.approx(surrender, abs=INFORCE)
    assert a.lives_if(t) == pytest.approx(lives, abs=INFORCE)


def test_worked_example_the_two_inforce_measures_separate_and_stay_separate(
        kr_pension_anchor):
    """pols_if counts contracts with an obligation open; lives_if counts annuitants alive.

    They separate for one reason in deferral — a surrender removes a contract, not a life —
    and for the opposite reason in payment, where the guarantee makes the instalments
    unconditional so ``pols_if`` is flat while ``lives_if`` runs down.  Both directions are
    asserted, because a model that used one for the other would still look monotone.
    """
    a = kr_pension_anchor
    assert a.pols_if(25) == pytest.approx(0.6096911403, abs=INFORCE)
    assert a.lives_if(25) == pytest.approx(0.9657433263, abs=INFORCE)
    assert a.pols_if(25) < a.lives_if(25)
    # Flat through the ten-year guarantee, and only then survivorship.
    assert all(a.pols_if(t) == pytest.approx(a.pols_if(25), abs=INFORCE)
               for t in range(25, 35))
    assert all(a.lives_if(t) < a.lives_if(t - 1) for t in range(26, 35))
    assert a.pols_if(35) == pytest.approx(
        a.pols_if(25) * a.lives_if(35) / a.lives_if(25), rel=SAME_DOUBLE)
    assert a.pols_if(35) == pytest.approx(0.5837918602, abs=INFORCE)


def test_worked_example_the_persistency_the_behaviour_section_reads_off_the_model(
        kr_pension_anchor):
    """39.03% leave before annuitisation — 36.51 points surrender, 2.52 points die.

    And the two weightings of the same lapse curve that the notes insist are not
    interchangeable: 1.9225% count-weighted against 1.4025% weighted by ``av_pp``, the gap
    being that lapse is front-loaded and the fund is back-loaded.  Any future calibration
    has to say which one it means, so both are pinned here.
    """
    a = kr_pension_anchor
    n = a.annuitisation_t()
    surrenders = sum(a.pols_lapse(t) for t in range(0, n))
    deaths = sum(a.pols_death(t) for t in range(0, n))
    assert 1.0 - a.pols_if(n) == pytest.approx(0.3903, abs=5e-5)
    assert surrenders == pytest.approx(0.3651, abs=5e-5)
    assert deaths == pytest.approx(0.0252, abs=5e-5)
    assert surrenders + deaths == pytest.approx(1.0 - a.pols_if(n), abs=1e-12)

    by_count = (sum(a.pols_if(t) * a.lapse_rate(t) for t in range(0, n))
                / sum(a.pols_if(t) for t in range(0, n)))
    by_fund = (sum(a.av_pp(t) * a.lapse_rate(t) for t in range(0, n))
               / sum(a.av_pp(t) for t in range(0, n)))
    assert by_count == pytest.approx(0.019225, abs=5e-7)
    assert by_fund == pytest.approx(0.014025, abs=5e-7)
    assert by_fund < by_count


def test_worked_example_the_tax_hand_off_that_argues_the_lapse_curve(kr_pension_anchor):
    """The net tax cost of surrendering is −₩33,575.23 at t = 1 and +₩42,223.98 at t = 5.

    The saver took a 16.5% credit on the way in and pays 16.5% of the surrender value on
    the way out, so the net cost is 16.5% of (해약환급금 − contributions): negative while
    the 환급률 is under 100% and positive after.  The tax turns against the surrendering
    saver at almost exactly the duration at which the expense loading stops hurting — the
    two frictions hand off — and that hand-off is the entire argument for a lapse vector
    that is flat rather than steeply front-loaded.
    """
    a = kr_pension_anchor
    rate = a.tax_basis("other_income_tax_rate")
    net_at_1 = rate * (a.cv_pp(1) - a.cum_prem_pp(1))
    net_at_5 = rate * (a.cv_pp(5) - a.cum_prem_pp(5))
    assert net_at_1 == pytest.approx(-33575.23, abs=WON)
    assert net_at_5 == pytest.approx(42223.98, abs=WON)
    assert net_at_1 < 0.0 < net_at_5
    assert a.tax_credit_rate() == pytest.approx(rate, abs=RATE)


# ---------------------------------------------------------------------------
# The worked example — the hand traces


def test_worked_example_year_zero_trace(kr_pension_anchor):
    """Year 0 — issue, term by term, including the intermediates the notes print.

    The trace is where the processing order is visible: the premium is allocated net of
    both charges and rolled at the credited rate **before** any decrement is taken, the
    death benefit paid at the end of the year is ``AV(1)`` and not ``AV(0)``, and the
    surrender is taken from the survivors of mortality.
    """
    a = kr_pension_anchor
    assert a.mort_rate_base(0) == pytest.approx(0.00070132, abs=5e-9)
    assert a.mort_rate(0) == pytest.approx(1.15 * 0.00070132, abs=RATE)
    assert a.lapse_rate(0) == pytest.approx(0.04, abs=RATE)
    assert a.premiums(0) == pytest.approx(6000000.00, abs=WON)
    assert a.prem_timing_factor(0) == pytest.approx(U_FACTOR, rel=SAME_DOUBLE)
    assert a.prem_to_av_pp(0) == pytest.approx(
        6000000 * (1 - 0.015 - 0.030) * U_FACTOR, rel=SAME_DOUBLE)
    assert a.prem_to_av_pp(0) == pytest.approx(NP_WITH_ACQ, rel=SAME_DOUBLE)
    assert a.charge_from_av_pp(0) == 0.0
    assert a.av_pp(0) == 0.0
    assert a.av_pp(1) == pytest.approx(NP_WITH_ACQ * 1.0215, rel=SAME_DOUBLE)
    assert a.av_pp(1) == pytest.approx(5796513.7581510395, rel=SAME_DOUBLE)
    assert a.cv_pp(1) == a.av_pp(1) == a.db_pp(1)
    assert a.pols_death(0) == pytest.approx(0.0008065180, abs=INFORCE)
    assert a.claims(0, "DEATH") == pytest.approx(4674.99, abs=WON)
    assert a.claim_expenses(0) == pytest.approx(24.20, abs=WON)
    assert a.pols_lapse(0) == pytest.approx(0.0399677393, abs=INFORCE)
    assert a.claims(0, "LAPSE") == pytest.approx(231673.55, abs=WON)
    assert a.expenses(0) == pytest.approx(200000.0 + 30000.0, abs=WON)
    assert a.commissions(0) == 0.0
    assert a.net_cf(0) == pytest.approx(5533627.26, abs=WON)
    assert a.pols_if(1) == pytest.approx(
        (1 - 0.0008065180) * (1 - 0.04), abs=INFORCE)
    assert a.lives_if(1) == pytest.approx(1 - 0.0008065180, abs=INFORCE)


def test_worked_example_year_one_trace(kr_pension_anchor):
    """Year 1 — the first year the fund carries a balance into the recursion.

    ``AV(2) = (AV(1) + NP(1)) x 1.0215``, so the opening balance and the new allocation
    are rolled together at one rate.  A model that rolled the opening balance and credited
    the premium separately at a different timing would miss here and nowhere else.
    """
    a = kr_pension_anchor
    assert a.mort_rate_base(1) == pytest.approx(0.00071719, abs=5e-9)
    assert a.mort_rate(1) == pytest.approx(0.0008247685, abs=RATE)
    assert a.lapse_rate(1) == pytest.approx(0.035, abs=RATE)
    assert a.premiums(1) == pytest.approx(5755354.46, abs=WON)
    assert a.av_pp_at(1, "AFT_PREM") == pytest.approx(
        11471025.5135607682, rel=SAME_DOUBLE)
    assert a.av_pp(2) == pytest.approx(11717652.5621023253, rel=SAME_DOUBLE)
    assert a.pols_death(1) == pytest.approx(0.0007911392, abs=INFORCE)
    assert a.claims(1, "DEATH") == pytest.approx(9270.29, abs=WON)
    assert a.claim_expenses(1) == pytest.approx(23.73, abs=WON)
    assert a.pols_lapse(1) == pytest.approx(0.0335452111, abs=INFORCE)
    assert a.claims(1, "LAPSE") == pytest.approx(393071.13, abs=WON)
    assert a.expenses(1) == pytest.approx(30000 * 1.02 * a.pols_if(1), abs=WON)
    assert a.expenses(1) == pytest.approx(29352.31, abs=WON)
    assert a.net_cf(1) == pytest.approx(5323636.99, abs=WON)
    assert a.pols_if(2) == pytest.approx(0.9248893924, abs=INFORCE)


def test_worked_example_year_seven_trace_the_acquisition_charge_stops(kr_pension_anchor):
    """Year 7 — α stops, β does not, and NP steps up by ₩89,128.4569 for thirteen years.

    The step is the whole of the acquisition charge — 1.50% x ₩500,000 x 12 — valued at
    the same timing factor, and it is small in the year it happens and compounds for the
    rest of the payment term.  Everything else in the row is unchanged in form.
    """
    a = kr_pension_anchor
    assert a.acq_charge_rate(6) == pytest.approx(0.015, abs=RATE)
    assert a.acq_charge_rate(7) == 0.0
    assert a.maint_charge_rate(7) == pytest.approx(0.030, abs=RATE)
    assert a.prem_to_av_pp(7) == pytest.approx(
        6000000 * (1 - 0.030) * U_FACTOR, rel=SAME_DOUBLE)
    assert a.prem_to_av_pp(7) == pytest.approx(NP_AFTER_ACQ, rel=SAME_DOUBLE)
    step = a.prem_to_av_pp(7) - a.prem_to_av_pp(6)
    assert step == pytest.approx(89128.4569, abs=5e-5)
    assert step == pytest.approx(0.015 * 500000 * 12 * U_FACTOR, rel=1e-12)
    assert a.premiums(7) == pytest.approx(4892487.54, abs=WON)
    assert a.pols_death(7) == pytest.approx(a.pols_if(7) * 0.0009844575, abs=INFORCE)
    assert a.claims(7, "DEATH") == pytest.approx(40222.79, abs=WON)
    assert a.claims(7, "LAPSE") == pytest.approx(816351.98, abs=WON)
    assert a.expenses(7) == pytest.approx(30000 * 1.02 ** 7 * a.pols_if(7), abs=WON)
    assert a.expenses(7) == pytest.approx(28099.65, abs=WON)
    assert a.net_cf(7) == pytest.approx(4007789.04, abs=WON)


def test_worked_example_year_twenty_trace_the_row_that_decides_the_shape(
        kr_pension_anchor):
    """Year 20 — 납입완료: no premium, and the maintenance charge comes out of the fund.

    납입완료 and 연금개시 are different dates, five years apart, and in between the contract
    is a fund that pays a charge, pays out on death and surrender, and receives nothing.
    A model that annuitises at 납입완료 loses these five years, ₩6,112,938.99 of
    undiscounted outgo and ₩15,982,848.02 of fund growth.
    """
    a = kr_pension_anchor
    assert a.prem_end_t() == 20
    assert a.annuitisation_t() == 25
    assert a.prem_paying(19) is True and a.prem_paying(20) is False
    assert a.premiums(20) == 0.0
    assert a.prem_to_av_pp(20) == 0.0
    assert a.charge_from_av_pp(20) == pytest.approx(
        6000000 * 0.0067 * U_FACTOR, rel=SAME_DOUBLE)
    assert a.charge_from_av_pp(20) == pytest.approx(CHARGE_PAID_UP, rel=SAME_DOUBLE)
    assert a.av_pp_at(20, "AFT_PREM") == pytest.approx(
        144272146.8561037481, rel=SAME_DOUBLE)
    assert a.av_pp(21) == pytest.approx(147373998.0135099888, rel=SAME_DOUBLE)
    # The fund still grows: 2.15% on ₩144m is many times a ₩39,810 charge.
    assert a.av_pp(21) - a.av_pp(20) == pytest.approx(3062040.45, abs=WON)
    assert a.mort_rate(20) == pytest.approx(1.15 * 0.00170745, abs=RATE)
    assert a.lapse_rate(20) == pytest.approx(0.01, abs=RATE)
    assert a.pols_death(20) == pytest.approx(0.0012733495, abs=INFORCE)
    assert a.claims(20, "DEATH") == pytest.approx(187658.61, abs=WON)
    assert a.claim_expenses(20) == pytest.approx(38.20, abs=WON)
    assert a.pols_lapse(20) == pytest.approx(0.0064721442, abs=INFORCE)
    assert a.claims(20, "LAPSE") == pytest.approx(953825.77, abs=WON)
    assert a.expenses(20) == pytest.approx(30000 * 1.02 ** 20 * a.pols_if(20), abs=WON)
    assert a.expenses(20) == pytest.approx(28908.56, abs=WON)
    assert a.net_cf(20) == pytest.approx(-1170431.14, abs=WON)
    assert a.net_cf(19) > 0.0 > a.net_cf(20)


def test_worked_example_year_twentyfive_trace_the_annuitisation_transition(
        kr_pension_anchor):
    """Year 25 — 연금개시일: five things happen in one step, in the notes' own order.

    The fund is fixed and floored; ``B`` is struck once; both deferral decrements go to
    zero; the first instalment is paid **in advance**, so the row t = n carries a payment;
    and the fund is gone from t = n + 1.  Each is asserted separately, because a model can
    get the annuity right and the row it falls on wrong.
    """
    a = kr_pension_anchor
    # 1. Fund fixed.
    assert a.av_pp_at(24, "AFT_PREM") == pytest.approx(
        156921004.0048610866, rel=SAME_DOUBLE)
    assert a.av_pp(25) == pytest.approx(AV_AT_COMMENCEMENT, rel=SAME_DOUBLE)
    # 2. Floor tested and not binding.
    assert a.min_fund_pp() == pytest.approx(1.001 * 120000000.0, rel=SAME_DOUBLE)
    assert a.annuity_fund_pp() == pytest.approx(a.av_pp(25), rel=SAME_DOUBLE)
    # 3. Factor struck on the issue vintage at the credited rate, monthly.
    assert a.mort_table_name() == "annuitant_issue"
    assert a.credit_rate(25) == pytest.approx(0.0215, abs=RATE)
    assert a.annuity_due_factor() == pytest.approx(ANNUITY_FACTOR, rel=SAME_DOUBLE)
    # 4. Annuity struck, once, net of the 0.5% 연금수령기간 관리비용.
    assert a.annuity_amount_pp() == pytest.approx(
        a.annuity_fund_net_pp() / a.annuity_due_factor() * 0.995, rel=SAME_DOUBLE)
    assert a.annuity_amount_pp() == pytest.approx(ANNUITY_AMOUNT, rel=SAME_DOUBLE)
    # 5. First instalment paid in advance, to every contract with an obligation open.
    assert a.annuity_pp(24) == 0.0
    assert a.annuity_pp(25) == pytest.approx(ANNUITY_AMOUNT, rel=SAME_DOUBLE)
    assert a.claims(25, "ANNUITY") == pytest.approx(4123569.57, abs=WON)
    # 6. Decrements off, and the fund gone from the following year.
    assert a.lapse_rate(25) == 0.0
    assert a.pols_death(25) == 0.0
    assert a.claims(25, "DEATH") == 0.0
    assert a.claims(25, "LAPSE") == 0.0
    assert a.av_pp(26) == a.cv_pp(26) == a.db_pp(26) == 0.0
    # 7. The maintenance level drops from ₩30,000 to ₩20,000 at annuitisation.
    assert a.expenses(25) == pytest.approx(20000 * 1.02 ** 25 * a.pols_if(25), abs=WON)
    assert a.expenses(25) == pytest.approx(20005.26, abs=WON)
    assert a.claim_expenses(25) == 0.0
    # 8. The row.
    assert a.net_cf(25) == pytest.approx(-4143574.82, abs=WON)


def test_worked_example_year_thirtyfive_trace_the_guarantee_ends(kr_pension_anchor):
    """Year 35 — the tenth guaranteed instalment fell at t = 34; from here it is mortality.

    ``B`` has not changed and never will; the count has.  The first fall in payout outgo
    in eleven years is survivorship and not arithmetic, and asserting the ratio
    ``L(35) / L(25)`` explicitly is what separates the two.
    """
    a = kr_pension_anchor
    assert a.annuity_pp(34) == a.annuity_pp(35) == pytest.approx(
        ANNUITY_AMOUNT, rel=SAME_DOUBLE)
    assert a.pols_if(34) == pytest.approx(a.pols_if(25), abs=INFORCE)
    assert a.lives_if(35) / a.lives_if(25) == pytest.approx(0.9575206553, abs=INFORCE)
    assert a.pols_if(35) == pytest.approx(0.5837918602, abs=INFORCE)
    assert a.claims(35, "ANNUITY") == pytest.approx(3948403.03, abs=WON)
    assert a.expenses(35) == pytest.approx(20000 * 1.02 ** 35 * a.pols_if(35), abs=WON)
    assert a.expenses(35) == pytest.approx(23350.38, abs=WON)
    assert a.net_cf(35) == pytest.approx(-3971753.42, abs=WON)
    assert a.net_cf(34) == pytest.approx(-4147477.70, abs=WON)
    assert a.net_cf(35) > a.net_cf(34)      # outgo falls for the first time in eleven years


def test_worked_example_the_assumption_values_the_notes_list(kr_pension_anchor):
    """The whole "Assumption values it uses" paragraph, read off the model.

    The declared rate is level at 2.15% and the 최저보증이율 ladder never binds in the base
    run, which is a fact about this scenario rather than about the product: it is the
    comparison the ``floor`` scenario exists to make.
    """
    a = kr_pension_anchor
    assert all(a.decl_rate(t) == pytest.approx(0.0215, abs=RATE) for t in range(0, 26))
    assert a.min_guar_rate(0) == pytest.approx(0.0125, abs=RATE)
    assert a.min_guar_rate(4) == pytest.approx(0.0125, abs=RATE)
    assert a.min_guar_rate(5) == pytest.approx(0.0100, abs=RATE)
    assert a.min_guar_rate(9) == pytest.approx(0.0100, abs=RATE)
    assert a.min_guar_rate(10) == pytest.approx(0.0050, abs=RATE)
    assert all(a.credit_rate(t) == pytest.approx(0.0215, abs=RATE) for t in range(0, 26))
    assert all(a.credit_rate(t) > a.min_guar_rate(t) for t in range(0, 26))
    assert a.prem_freq() == 12 and a.annuity_freq() == 12
    assert a.mort_be_factor() == pytest.approx(1.15, abs=RATE)
    assert a.proj_len() == 80
    assert len(a.result_cf()) == 81
    # The prescribed lapse shape: 4.0 / 3.5 / 3.0 / 2.5 / 2.0 / 1.5 / 1.0 / 0.
    expected = ([0.040, 0.035, 0.030] + [0.025] * 2 + [0.020] * 5 + [0.015] * 10
                + [0.010] * 5 + [0.0] * 56)
    assert [a.lapse_rate(t) for t in range(0, 81)] == pytest.approx(expected, abs=RATE)
    assert a.lapse_basis() == "pension"


# ---------------------------------------------------------------------------
# The annuity factor and the published illustration


def test_the_factor_reconstructs_eight_published_implied_factors():
    """Eight published figures, one formula, two interest bases and both annuity forms.

    Dividing the published fund at annuitisation by each published annuity gives the
    factor the carrier actually used; the model's own factor, grossed up for the 0.5%
    charge, is that factor.  This is the correction to ``product-spec.md``, and it is the
    only external validation the public record offers for the payout side of this product.
    The six 확정기간 points and the 0.5% life point are not shipped model points, so they
    come in through the ``model_point_file`` Reference.
    """
    overrides = {}
    keys = sorted(PUBLISHED_IMPLIED_FACTORS)
    for i, (form, term, scenario) in enumerate(keys):
        overrides[200 + i] = {
            "payout_form": form,
            "payout_term_y": term,
            "guar_term_y": term,
            "rate_scenario": scenario,
        }
    with alt_model_points("factors", overrides) as model:
        for i, key in enumerate(keys):
            form, term, scenario = key
            p = model.Projection[200 + i]
            expected_rate = 0.0215 if scenario == "base" else 0.005
            assert p.credit_rate(25) == pytest.approx(expected_rate, abs=RATE), key
            implied = p.annuity_fund_pp() / p.annuity_amount_pp()
            assert implied == pytest.approx(
                p.annuity_due_factor() / 0.995, rel=SAME_DOUBLE), key
            assert implied == pytest.approx(
                RECONSTRUCTED_IMPLIED_FACTORS[key], abs=5e-4), key
            assert implied == pytest.approx(
                PUBLISHED_IMPLIED_FACTORS[key], abs=0.006), key


def test_the_certain_factor_carries_no_mortality_and_the_life_factor_does():
    """The two forms are priced differently and the difference is a factor of two and a half.

    확정기간연금형 is 「공시이율을 적용하여 … 나누어 계산」 — the declared rate alone — and
    its instalments are paid to the count whether or not the annuitant lives.  The
    종신연금형 is priced on the 연금사망률 as well.  Sex therefore moves the life factor and
    must not move the certain one, which is the cleanest way to show that no mortality
    reaches it.
    """
    overrides = {
        210: {"payout_form": "certain", "payout_term_y": 20, "sex": "M"},
        211: {"payout_form": "certain", "payout_term_y": 20, "sex": "F"},
        212: {"payout_form": "life_guar", "sex": "M"},
        213: {"payout_form": "life_guar", "sex": "F"},
    }
    with alt_model_points("forms", overrides) as model:
        male_certain = model.Projection[210].annuity_due_factor()
        female_certain = model.Projection[211].annuity_due_factor()
        male_life = model.Projection[212].annuity_due_factor()
        female_life = model.Projection[213].annuity_due_factor()
        assert male_certain == female_certain          # no mortality anywhere in it
        assert female_life > male_life                 # the female table is a setback
        assert (female_life - male_life) / female_life == pytest.approx(0.0667, abs=5e-4)
        # And the certain form's own factor is what annuity_due_certain_factor computes.
        assert male_certain == pytest.approx(
            model.Projection[210].annuity_due_certain_factor(), rel=SAME_DOUBLE)


# ---------------------------------------------------------------------------
# The nine shipped model points


@pytest.mark.parametrize("point_id", sorted(MODEL_POINTS))
def test_the_shipped_model_point_summary_table(pension_savings, point_id):
    """The notes' nine-row model point table, row by row.

    Each row states the point's whole shape — the dates, the form, the vintage, the fund
    at annuitisation, the factor, the annuity and the undiscounted total — so a module
    switched on or off by accident moves one of these and nothing else in the library
    would notice.
    """
    (sex, x, m, d, n, y, premium, proj_len, fund, factor, annuity,
     total) = MODEL_POINTS[point_id]
    p = pension_savings.Projection[point_id]
    assert p.sex() == sex
    assert p.issue_age() == x
    assert p.premium_term_y() == m
    assert p.defer_gap_y() == d
    assert p.annuitisation_t() == n
    assert p.annuity_start_age() == y
    assert p.prem_pp() == pytest.approx(premium, abs=WON)
    assert p.proj_len() == proj_len
    assert len(p.result_cf()) == proj_len + 1
    assert p.annuity_fund_pp() == pytest.approx(fund, abs=WON)
    assert p.annuity_due_factor() == pytest.approx(factor, abs=5e-6)
    assert p.annuity_amount_pp() == pytest.approx(annuity, abs=WON)
    assert p.result_cf()["net_cf"].sum() == pytest.approx(total, abs=WON)


def test_the_sex_twin_changes_the_factor_and_nothing_else(pension_savings):
    """Point 2 is the anchor with the sex switched, and that is all sex does here.

    The deferral phase carries no mortality risk, so the fund, the surrender values and
    the premiums are identical to the anchor's; only the annuity factor and the run-off
    of the in-force move.  A model that let sex touch the fund would fail on the first
    line of this.
    """
    male = pension_savings.Projection[1]
    female = pension_savings.Projection[2]
    for t in (1, 5, 10, 20, 25):
        assert female.av_pp(t) == pytest.approx(male.av_pp(t), rel=SAME_DOUBLE)
        assert female.cv_pp(t) == pytest.approx(male.cv_pp(t), rel=SAME_DOUBLE)
    assert female.annuity_fund_pp() == pytest.approx(
        male.annuity_fund_pp(), rel=SAME_DOUBLE)
    assert female.annuity_due_factor() > male.annuity_due_factor()
    change = (male.annuity_amount_pp() - female.annuity_amount_pp())
    assert change / male.annuity_amount_pp() == pytest.approx(0.0667, abs=5e-5)


def test_the_hundred_and_one_tenths_floor_binds_exactly_at_model_point_six(
        pension_savings):
    """Point 6 is the statutory-minimum contract and the one point where the floor binds.

    Five years of premiums and a 만 55세 start on the guaranteed-rate scenario leave
    ``av_pp(5)`` at ₩29,573,776.73, and the guarantee tops it to exactly
    ₩30,030,000 = 100.1% x ₩30,000,000.  It is the only element of this contract that
    behaves like an option rather than an account, and this is the shipped demonstration
    that it is not decorative.
    """
    p = pension_savings.Projection[6]
    assert p.rate_scenario() == "floor"
    assert p.min_fund_on() is True
    assert p.premium_term_y() == 5           # the statutory minimum
    assert p.annuity_start_age() == 55       # drawn from 만 55세
    assert p.cum_prem_pp(5) == pytest.approx(30000000.0, abs=WON)
    assert p.av_pp(5) == pytest.approx(29573776.73, abs=WON)
    assert p.min_fund_pp() == pytest.approx(30030000.0, abs=WON)
    assert p.annuity_fund_pp() == pytest.approx(30030000.0, abs=WON)
    assert p.annuity_fund_pp() > p.av_pp(5)
    assert p.check_min_fund() is True
    # The credited rate is the ladder, because the declared rate is driven below it.
    assert p.decl_rate(0) == 0.0
    assert p.credit_rate(0) == pytest.approx(0.0125, abs=RATE)
    assert p.credit_rate(4) == pytest.approx(0.0125, abs=RATE)


def test_the_vintage_switch_is_worth_three_per_cent_and_the_ratchet_is_out_of_the_money(
        pension_savings):
    """Points 7 and 9 exercise the two readings of the 연금사망률 ratchet clause.

    ``commencement`` strikes the factor on the 연금개시시점 table and costs 2.97% of the
    annuity — the size of the vintage question, and the reason it is a switch rather than
    an assumption.  ``ratchet`` implements the clause itself, and because successive
    경험생명표 revisions have **lightened** mortality it is out of the money: the model
    keeps the issue vintage, whose smaller factor is the larger annuity.
    """
    anchor = pension_savings.Projection[1]
    commencement = pension_savings.Projection[7]
    ratchet = pension_savings.Projection[9]
    assert anchor.mort_vintage() == "issue"
    assert anchor.mort_table_name() == "annuitant_issue"
    assert commencement.mort_vintage() == "commencement"
    assert commencement.mort_table_name() == "annuitant_revised"
    change = anchor.annuity_amount_pp() - commencement.annuity_amount_pp()
    assert change / anchor.annuity_amount_pp() == pytest.approx(0.0297, abs=5e-5)
    assert ratchet.mort_vintage() == "ratchet"
    assert ratchet.mort_table_name() == "annuitant_issue"
    issue_factor = ratchet.annuity_due_factor_on("annuitant_issue")
    revised_factor = ratchet.annuity_due_factor_on("annuitant_revised")
    assert issue_factor == pytest.approx(22.70113, abs=5e-6)
    assert revised_factor == pytest.approx(23.43728, abs=5e-6)
    assert issue_factor < revised_factor     # the smaller factor is the larger annuity
    assert ratchet.annuity_due_factor() == pytest.approx(issue_factor, rel=SAME_DOUBLE)


def test_the_module_point_carries_every_switch_at_once(pension_savings):
    """Point 9 runs the ratchet, a two-year 납입유예, the loan, a dividend and no floor.

    The 납입유예 is the contractual alternative to lapsing and it is **not** lapse: the
    premiums stop for two years, the charges are still taken from the fund, and both the
    premium dates and the annuity date move by ``h``, so ``n`` goes from 25 to 27.  Where
    it runs, the 100.1% guarantee is withdrawn — which is what the contracts do — and the
    annuity date is deferred instead.
    """
    p = pension_savings.Projection[9]
    assert p.holiday_years() == 2
    assert p.on_holiday(8) is True and p.on_holiday(9) is True
    assert p.on_holiday(7) is False and p.on_holiday(10) is False
    assert p.prem_paying(8) is False and p.prem_paying(21) is True
    assert p.prem_end_t() == 22 and p.annuitisation_t() == 27
    # Twenty premiums are still paid, so the contribution base is unchanged.
    assert p.cum_prem_pp(27) == pytest.approx(120000000.0, abs=WON)
    # The charge is still taken during the holiday, and it is the premium-paying rate.
    assert p.charge_from_av_pp(8) == pytest.approx(
        6000000 * (0.0 + 0.03) * p.prem_timing_factor(8), rel=SAME_DOUBLE)
    # The guarantee is withdrawn.
    assert p.min_fund_on() is False
    assert p.min_fund_pp() == 0.0
    assert p.check_min_fund() is True
    # The loan is drawn at year 15 and deducted from the fund that buys the annuity.
    assert p.loan_on() is True
    assert p.loan_pp(14) == 0.0
    assert p.loan_pp(15) == pytest.approx(0.5 * p.cv_pp(15), rel=SAME_DOUBLE)
    assert p.policy_loans(15) == pytest.approx(p.loan_pp(15) * p.pols_if(15),
                                               rel=SAME_DOUBLE)
    assert p.annuity_fund_net_pp() < p.annuity_fund_pp()
    # And a declared dividend accumulates and is applied at t = n as an 증액연금.
    assert p.par() is True and p.div_rate() == pytest.approx(0.002, abs=RATE)
    assert p.div_acc_pp(27) > 0.0
    assert p.annuity_fund_net_pp() == pytest.approx(
        p.annuity_fund_pp() + p.div_acc_pp(27) - p.loan_pp(27), rel=SAME_DOUBLE)


def test_the_certain_form_ends_by_counting_and_publishes_a_maturity(pension_savings):
    """Point 4 runs the 확정기간연금형: k unconditional instalments, then nothing.

    ``pols_if`` is flat for the whole term while ``lives_if`` runs down, ``pols_death`` is
    zero throughout, and ``pols_maturity`` in the final year is the count reaching the
    scheduled end — which the in-force roll-forward needs, because those survivors neither
    die nor surrender.  There is still no ``claims(t, "MATURITY")``: 연금저축보험 has no
    maturity benefit and no maturity date, and that absence is a product fact.
    """
    p = pension_savings.Projection[4]
    n, k = p.annuitisation_t(), p.payout_term_y()
    assert p.payout_form() == "certain"
    assert (n, k) == (35, 20)
    assert p.proj_len() == n + k - 1 == 54
    assert all(p.pols_if(t) == pytest.approx(p.pols_if(n), abs=INFORCE)
               for t in range(n, n + k))
    assert p.pols_if(n + k) == 0.0
    assert all(p.pols_death(t) == 0.0 for t in range(n, n + k))
    assert p.lives_if(54) < p.lives_if(35)
    assert all(p.pols_maturity(t) == 0.0 for t in range(0, 54))
    assert p.pols_maturity(54) == pytest.approx(p.pols_if(54), rel=SAME_DOUBLE)
    assert p.check_pols_roll_fwd() is True
    with pytest.raises(FormulaError):
        p.claims(54, "MATURITY")


# ---------------------------------------------------------------------------
# Which check_* cells this model publishes


def test_which_checks_this_model_publishes(pension_savings, kr_pension_anchor):
    """The nine check cells, asserted **by name**, each with a per-t residual.

    A generic sweep over ``check_*`` cannot notice a check that has quietly disappeared:
    it would call the eight that remain, pass, and prove less than it did before.  Naming
    the set here is what turns "every check passes" into a statement about *which* checks.
    Every one of the nine carries a signed ``<name>_resid(t)``, so a failure says where.
    """
    published = {name for name in pension_savings.Projection.cells
                 if name.startswith("check_") and not name.endswith("_resid")}
    assert published == CHECKS
    resid = {name[:-len("_resid")] for name in pension_savings.Projection.cells
             if name.startswith("check_") and name.endswith("_resid")}
    assert resid == CHECKS
    a = kr_pension_anchor
    for name in sorted(CHECKS):
        value = getattr(a, name)()
        assert value is True, "%s() is not True on the anchor cell" % name
        assert isinstance(value, bool), "%s() must return a real bool" % name


def test_the_check_residuals_close_on_the_anchor_cell(kr_pension_anchor):
    """Every published residual is zero at every t, not merely inside its own tolerance.

    The ``check_*`` cells compare against ``roll_fwd_tol`` scaled by the quantity under
    test, which is the right thing for a check that has to hold on a ₩3 x 10^8 fund and
    on a policy count near one.  This test looks at the residuals directly, so a check
    that had quietly widened its own tolerance would still be caught here.
    """
    a = kr_pension_anchor
    ts = range(0, a.proj_len() + 1)
    for name, tol in (("check_pols_roll_fwd", 1e-12),
                      ("check_av_roll_fwd", 1e-6),
                      ("check_cv_floor", 1e-6),
                      ("check_annuity_total", 1e-6),
                      ("check_mort_law", 1e-15),
                      ("check_net_cf", 1e-6)):
        residual = getattr(a, name + "_resid")
        worst = max(abs(residual(t)) for t in ts)
        assert worst < tol, "%s_resid worst |residual| = %r" % (name, worst)
    # The three one-sided checks are inequalities, so their residuals are signed.
    assert min(a.check_surr_chg_cap_resid(t) for t in ts) >= 0.0
    assert min(a.check_min_fund_resid(t) for t in ts) >= 0.0
    assert min(a.check_annuity_limit_resid(t) for t in ts) >= 0.0


def test_the_check_tolerance_is_a_named_reference(pension_savings, kr_pension_anchor):
    """``roll_fwd_tol`` is a Reference, not a literal, and the checks scale it.

    A bare literal tolerance inside a formula is invisible to a reader and unchangeable by
    a user with a different appetite.  Here it is 1e-10, and every check that closes on a
    money quantity multiplies it by the size of that quantity rather than comparing a
    ₩1.6 x 10^8 fund against an absolute 1e-10 it could never reach.
    """
    refs = pension_savings.Projection.refs
    assert "roll_fwd_tol" in refs
    assert refs["roll_fwd_tol"] == 1e-10
    a = kr_pension_anchor
    scaled = refs["roll_fwd_tol"] * a.annuity_fund_pp()
    assert 1e-6 < scaled < 1.0            # far below one won, and above float64 noise
    worst = max(abs(a.check_av_roll_fwd_resid(t)) for t in range(0, a.proj_len() + 1))
    assert worst < scaled


# ---------------------------------------------------------------------------
# The product's own invariants: the recursions and the processing order


def test_the_fund_recursion_is_the_notes_identity(pension_savings):
    """AV(t+1) = (AV(t) + NP(t) − C(t))(1 + i_c(t)) over the whole deferral phase.

    Asserted directly rather than through ``check_av_roll_fwd`` alone, and on the points
    that exercise the terms separately: the anchor, the additional-premium point, the
    guaranteed-rate point and the payment-holiday point, where ``C(t)`` is non-zero in a
    year that also has no premium.
    """
    for point_id in (1, 6, 8, 9):
        p = pension_savings.Projection[point_id]
        n = p.annuitisation_t()
        assert p.av_pp(0) == 0.0
        for t in range(0, n):
            expected = ((p.av_pp(t) + p.prem_to_av_pp(t) - p.charge_from_av_pp(t))
                        * (1.0 + p.credit_rate(t)))
            assert p.av_pp(t + 1) == pytest.approx(expected, rel=SAME_DOUBLE), (
                "point %d, t=%d" % (point_id, t))
        assert p.av_pp(n + 1) == 0.0
        assert p.check_av_roll_fwd() is True


def test_the_inforce_rollforward_is_the_notes_identity(pension_savings):
    """l(t) − l(t+1) = deaths + surrenders + maturities, on every phase of every form.

    The identity has to hold across the annuitisation step, where two of its three terms
    switch off at once, and across the end of a guarantee or a certain term, where the
    third one switches on.  Asserted on the life form, the certain form and the module
    point, because a term that is identically zero on the cell under test proves nothing.
    """
    for point_id in (1, 4, 6, 9):
        p = pension_savings.Projection[point_id]
        for t in range(0, p.proj_len() + 1):
            out = p.pols_death(t) + p.pols_lapse(t) + p.pols_maturity(t)
            assert p.pols_if(t) - p.pols_if(t + 1) == pytest.approx(out, abs=1e-13), (
                "point %d, t=%d" % (point_id, t))
        assert p.check_pols_roll_fwd() is True
        assert p.pols_if(p.proj_len() + 1) == 0.0
        assert all(0.0 <= p.pols_if(t) <= 1.0 for t in range(0, p.proj_len() + 1))
        assert all(p.pols_if(t + 1) <= p.pols_if(t) + 1e-15
                   for t in range(0, p.proj_len() + 1))


def test_the_decrements_are_taken_in_the_notes_processing_order(kr_pension_anchor):
    """Deaths from the whole opening in-force, surrenders from the survivors of mortality.

    Each ``pols_if_at`` timing reads the population the next decrement is taken from,
    which is what makes the surrender a decrement on the survivors rather than one
    competing with mortality.  The order is asserted by a quantity that would differ if it
    changed: at t = 0 the surrender count is 0.0399677393 and not 0.04.
    """
    a = kr_pension_anchor
    for t in (0, 1, 5, 19, 20, 24):
        assert a.pols_if_at(t, "BEF_DECR") == a.pols_if(t)
        assert a.pols_if_at(t, "BEF_LAPSE") == pytest.approx(
            a.pols_if(t) - a.pols_death(t), rel=SAME_DOUBLE)
        assert a.pols_if_at(t, "AFT_DECR") == pytest.approx(
            a.pols_if_at(t, "BEF_LAPSE") * (1 - a.lapse_rate(t)), rel=SAME_DOUBLE)
        assert a.pols_if_at(t, "AFT_DECR") == pytest.approx(
            a.pols_if(t + 1), rel=SAME_DOUBLE)
        assert a.pols_death(t) == pytest.approx(
            a.pols_if(t) * a.mort_rate(t), rel=SAME_DOUBLE)
        assert a.pols_lapse(t) == pytest.approx(
            a.pols_if_at(t, "BEF_LAPSE") * a.lapse_rate(t), rel=SAME_DOUBLE)
        # The order is not cosmetic: taking lapse off the whole cohort would be larger.
        assert a.pols_lapse(t) < a.pols_if(t) * a.lapse_rate(t)
    assert a.pols_lapse(0) == pytest.approx(0.0399677393, abs=INFORCE)
    assert a.pols_lapse(0) != pytest.approx(0.04, abs=1e-6)
    with pytest.raises(FormulaError):
        a.pols_if_at(1, "BEF_NOTHING")


def test_the_fund_timings_are_premium_then_charge_then_interest(kr_pension_anchor):
    """av_pp_at reads BEF_PREM, AFT_PREM and AFT_INT, and they are that order.

    Interest is credited on the balance **after** the premium is allocated and the charge
    deducted, which is what the annualised-premium convention of 감독규정 제7-65조제2항
    permits and what ``prem_timing_factor`` then corrects for.  Crediting before the
    allocation would lose a year of interest on every premium.
    """
    a = kr_pension_anchor
    for t in (0, 1, 7, 19, 20, 24):
        assert a.av_pp_at(t, "BEF_PREM") == a.av_pp(t)
        assert a.av_pp_at(t, "AFT_PREM") == pytest.approx(
            a.av_pp(t) + a.prem_to_av_pp(t) - a.charge_from_av_pp(t), rel=SAME_DOUBLE)
        assert a.av_pp_at(t, "AFT_INT") == pytest.approx(
            a.av_pp_at(t, "AFT_PREM") * (1 + a.credit_rate(t)), rel=SAME_DOUBLE)
        assert a.av_pp_at(t, "AFT_INT") == pytest.approx(a.av_pp(t + 1), rel=SAME_DOUBLE)
    with pytest.raises(FormulaError):
        a.av_pp_at(1, "AFT_NOTHING")


def test_the_published_statement_adds_up(pension_savings):
    """``result_cf`` columns are a decomposition of ``net_cf``, not a selection from it.

    ``check_net_cf`` re-derives the ledger from the published columns, so the identity a
    reader adds up with a calculator is the identity the model asserts.  It is the guard
    against a benefit kind that exists in ``claims()`` but was never given a column — and,
    on this product, against anyone folding the tax layer in.
    """
    for point_id in (1, 4, 6, 8, 9):
        df = pension_savings.Projection[point_id].result_cf()
        outgo = df[["claims_annuity", "claims_death", "claims_lapse", "claim_expenses",
                    "expenses", "commissions", "policy_loans"]].sum(axis=1)
        assert (df["premiums"] - outgo - df["net_cf"]).abs().max() == pytest.approx(
            0.0, abs=1e-6)
        assert pension_savings.Projection[point_id].check_net_cf() is True


def test_result_cf_shape(kr_pension_anchor):
    """The published statement's columns, in order, with ``pols_if`` first.

    Column order is part of the published artefact: ``run.py`` prints the frame and the
    notes tabulate it, so a reordering is a documentation break even though every number
    is unchanged.  ``claims_annuity`` leads the benefit columns because it is the largest.
    """
    df = kr_pension_anchor.result_cf()
    assert list(df.index) == list(range(0, 81))
    assert df.index.name == "t"
    assert list(df.columns) == [
        "pols_if", "premiums", "claims_annuity", "claims_death", "claims_lapse",
        "expenses", "claim_expenses", "commissions", "policy_loans", "net_cf",
    ]
    assert df.notna().all().all()
    assert "claims" not in df.columns
    assert df.loc[0, "net_cf"] == pytest.approx(5533627.26, abs=WON)


def test_the_companion_frames_publish_the_state_and_the_tax(kr_pension_anchor):
    """``result_pols`` and ``result_tax`` are where everything that is not cash lives.

    The tax layer has its own frame precisely so that it cannot leak into ``result_cf()``,
    and the state frame carries both in-force measures side by side so that a reader can
    see them diverge rather than having to trust that they do.
    """
    a = kr_pension_anchor
    pols = a.result_pols()
    assert list(pols.columns) == [
        "pols_if", "lives_if", "pols_death", "pols_lapse", "pols_maturity", "mort_rate",
        "lapse_rate", "credit_rate", "cum_prem_pp", "av_pp", "cv_pp", "loan_pp",
    ]
    assert pols.index.name == "t" and len(pols) == 81 and pols.notna().all().all()
    tax = a.result_tax()
    assert list(tax.columns) == [
        "tax_credit_pp", "cv_pp", "surr_tax_pp", "annuity_pp", "pension_tax_rate",
        "annuity_tax_pp", "annuity_year_no", "annuity_limit_pp",
    ]
    assert tax.index.name == "t" and len(tax) == 81 and tax.notna().all().all()
    # No column of the tax frame appears in the cash flow statement.
    cash = set(a.result_cf().columns)
    assert cash.isdisjoint({"tax_credit_pp", "surr_tax_pp", "annuity_tax_pp",
                            "annuity_limit_pp", "pension_tax_rate"})


def test_the_model_point_table_exercises_the_product(pension_savings):
    """Both sexes, both payout forms, all three vintages, every module and both bases.

    The table is the model's coverage statement, so what it must contain is asserted here
    rather than left to a reader counting rows.  ``annuity_start_age`` is derived and not
    free: the model rejects a point where it is not ``x + m + d``, because two spellings of
    one date is how a projection silently annuitises in the wrong year.
    """
    table = pension_savings.Data.model_point_table()
    assert len(table) == 9
    assert list(table.index) == list(range(1, 10))
    assert set(table["sex"]) == {"M", "F"}
    assert set(table["payout_form"]) == {"life_guar", "certain"}
    assert set(table["mort_vintage"]) == {"issue", "commencement", "ratchet"}
    assert set(table["lapse_basis"]) == {"pension", "savings"}
    assert set(table["rate_scenario"]) == {"base", "floor", "hybrid"}
    assert set(table["min_fund_on"]) == {0, 1}
    for module in ("loan_on", "par"):
        assert set(table[module]) == {0, 1}, "%s is not exercised both ways" % module
    assert (table["addl_prem_pp"] > 0).any()
    assert (table["surr_chg_rate"] > 0).any()
    assert (table["holiday_years"] > 0).any()
    assert table["premium_term_y"].min() == 5      # the statutory minimum
    assert table["annuity_start_age"].min() == 55  # 만 55세, the statutory earliest
    for point_id, row in table.iterrows():
        assert (row["annuity_start_age"]
                == row["issue_age"] + row["premium_term_y"] + row["defer_gap_y"]), point_id


# ---------------------------------------------------------------------------
# Pitfall 1: a survivorship release in the fund


def test_pitfall_no_survivorship_release_in_the_fund(pension_savings, kr_pension_anchor):
    """Pitfall 1 — putting a survivorship release into the 계약자적립액.

    The fund is an account: charges off the premium, the remainder credited, and nothing
    else moves.  The Japanese deferred annuity on the other page of this repository divides
    by ``(1 - q')`` each year, and porting that shape here **overstates the 연금개시 fund
    silently**.  There is nothing to release — the death benefit *is* the fund.  The test
    that catches it is that mortality does not reach ``av_pp`` at all: the male and female
    anchors, on materially different tables, hold the same fund at every duration, and the
    recursion misses a survivorship-loaded roll-forward by a visible margin.
    """
    male, female = pension_savings.Projection[1], pension_savings.Projection[2]
    assert male.mort_rate(10) != female.mort_rate(10)
    for t in range(0, 26):
        assert male.av_pp(t) == pytest.approx(female.av_pp(t), rel=SAME_DOUBLE)
    a = kr_pension_anchor
    # What a survivorship release would have produced, one year in.
    released = a.av_pp_at(0, "AFT_PREM") * 1.0215 / (1 - a.mort_rate(0))
    assert released > a.av_pp(1)
    assert a.av_pp(1) == pytest.approx(a.av_pp_at(0, "AFT_PREM") * 1.0215,
                                       rel=SAME_DOUBLE)
    assert a.check_av_roll_fwd() is True


# ---------------------------------------------------------------------------
# Pitfall 2: a deferral-phase mortality strain


def test_pitfall_the_deferral_mortality_strain_is_exactly_zero(kr_pension_anchor):
    """Pitfall 2 — projecting a deferral-phase mortality strain.

    ``db_pp_net(t+1)`` and ``cv_pp_net(t+1)`` are the same number at every duration on this
    composite, so the strain is exactly zero and no deferral-phase death cover basis is
    needed.  Mortality still matters — it decides how many policies reach the 연금개시일 —
    but a model that priced a death benefit here would be pricing a risk the contract does
    not run.  There is no death cover above the fund and no sum assured anywhere.
    """
    a = kr_pension_anchor
    for t in range(1, 26):
        assert a.db_pp(t) == pytest.approx(a.cv_pp(t), rel=SAME_DOUBLE)
        assert a.db_pp_net(t) == pytest.approx(a.cv_pp_net(t), rel=SAME_DOUBLE)
        assert a.db_pp(t) - a.cv_pp(t) == 0.0
    assert "sum_assured" not in a.model_point().index
    # The two decrements differ in their rate, never in their payment.
    for t in (0, 5, 19, 24):
        per_policy_death = a.claims(t, "DEATH") / a.pols_death(t)
        per_policy_lapse = a.claims(t, "LAPSE") / a.pols_lapse(t)
        assert per_policy_death == pytest.approx(per_policy_lapse, rel=SAME_DOUBLE)


# ---------------------------------------------------------------------------
# Pitfall 3: a death product's best-estimate adjustment


def test_pitfall_the_best_estimate_factor_runs_the_other_way(kr_pension_anchor):
    """Pitfall 3 — applying a death product's best-estimate adjustment.

    ``mort_be_factor`` is **1.15**, greater than one, because the published 연금사망률 is a
    pricing basis for a longevity liability and is loaded on the *survival* side.  A 0.85
    lifted from a death-cover table has the sign wrong and produces both too many survivors
    and, if it were fed into the factor, too large an annuity.  The uplift is applied to
    the decrement and **not** to the factor, which is struck on the table itself.
    """
    a = kr_pension_anchor
    assert a.mort_be_factor() == pytest.approx(1.15, abs=RATE)
    assert a.mort_be_factor() > 1.0
    for t in (0, 10, 25, 40):
        assert a.mort_rate(t) == pytest.approx(
            1.15 * a.mort_rate_base(t), rel=SAME_DOUBLE)
        assert a.mort_rate(t) > a.mort_rate_base(t)
    assert a.mort_rate(80) == 1.0                 # the min(1, ...) cap at the terminal age
    # The annuity factor is struck on the table, not on the best-estimate decrement: a
    # factor built on the loaded rates would be materially smaller.
    assert a.annuity_due_factor_on("annuitant_issue") == pytest.approx(
        a.annuity_due_factor(), rel=SAME_DOUBLE)
    assert a.mort_rate_at_age("annuitant_issue", 65) == pytest.approx(
        a.mort_rate_base(25), rel=SAME_DOUBLE)
    assert a.mort_rate_at_age("annuitant_issue", 65) < a.mort_rate(25)


# ---------------------------------------------------------------------------
# Pitfall 5: stopping the lapse decrement a year early


def test_pitfall_the_lapse_decrement_runs_through_the_year_before_annuitisation(
        kr_pension_anchor):
    """Pitfall 5 — stopping the lapse decrement a year early.

    Surrender is available right up to the day before the 연금개시일, so ``lapse_rate(t)``
    is non-zero **through t = n − 1** and zero from t = n.  Zeroing it a year early deletes
    the ₩987,174.98 of surrender benefit that year 24 pays on the full fund and leaves the
    in-force too high going into the annuity.
    """
    a = kr_pension_anchor
    n = a.annuitisation_t()
    assert a.lapse_rate(n - 1) == pytest.approx(0.01, abs=RATE)
    assert a.lapse_rate(n) == 0.0
    assert a.pols_lapse(n - 1) > 0.0
    assert a.pols_lapse(n) == 0.0
    assert a.claims(n - 1, "LAPSE") == pytest.approx(987174.98, abs=WON)
    # The contracts leaving in year n - 1 are paid CV(n), the full fund.
    assert a.claims(n - 1, "LAPSE") == pytest.approx(
        a.cv_pp_net(n) * a.pols_lapse(n - 1), rel=SAME_DOUBLE)
    assert a.cv_pp(n) == pytest.approx(AV_AT_COMMENCEMENT, rel=SAME_DOUBLE)
    # And the lapse curve steps *down* at 납입완료, not up: the commonest trigger is gone.
    assert a.lapse_rate(19) == pytest.approx(0.015, abs=RATE)
    assert a.lapse_rate(20) == pytest.approx(0.010, abs=RATE)


# ---------------------------------------------------------------------------
# Pitfall 6: an annual annuity-due factor


def test_pitfall_the_annuity_factor_is_monthly_not_annual(kr_pension_anchor):
    """Pitfall 6 — using an annual annuity-due factor.

    The annuity is paid 매월 and the factor is therefore ``adue^(12)``, the annual factor
    less the standard ``(f − 1) / 2f = 11/24`` correction.  On the annual reading the
    anchor's ``B`` would be ₩6,634,429.17 instead of ₩6,763,374.59 — **1.91% low** — and
    the model would reproduce none of the eight published implied factors.  This is the
    error ``product-spec.md`` contains and the technical notes correct.
    """
    a = kr_pension_anchor
    assert a.annuity_freq() == 12
    annual_factor = a.annuity_due_factor() + 11.0 / 24.0
    assert annual_factor == pytest.approx(24.04025, abs=5e-6)
    annual_amount = a.annuity_fund_net_pp() / annual_factor * 0.995
    assert annual_amount == pytest.approx(6634429.17, abs=WON)
    assert annual_amount < a.annuity_amount_pp()
    assert (a.annuity_amount_pp() - annual_amount) / a.annuity_amount_pp() == (
        pytest.approx(0.0191, abs=5e-5))
    # The certain factor is a monthly annuity-due as well, through d^(12).
    i = a.credit_rate(25)
    d = i / (1.0 + i)
    d12 = 12.0 * (1.0 - (1.0 - d) ** (1.0 / 12.0))
    assert a.annuity_due_certain_factor() == pytest.approx(
        (1.0 - (1.0 + i) ** -a.payout_term_y()) / d12, rel=1e-13)
    # The nominal discount rate payable twelve times a year sits between the annual
    # discount rate and the interest rate, which is what makes the monthly factor the
    # smaller of the two and the annuity the larger.
    assert d < d12 < i


# ---------------------------------------------------------------------------
# Pitfall 7: sharing one factor between the two payout forms


def test_pitfall_the_two_payout_forms_do_not_share_a_factor(kr_pension_anchor):
    """Pitfall 7 — mortality in the 확정기간 factor, or none in the 종신 one.

    At the anchor cell the two factors on the same fund are 9.01595 and 23.58192: the life
    annuity pays **38.23%** of what a ten-year certain annuity pays.  Sharing one code path
    between them is not a tidy-up, it is a factor of two and a half, and the direction of
    the error depends on which way round the sharing goes.
    """
    a = kr_pension_anchor
    assert a.payout_form() == "life_guar"
    assert a.annuity_due_certain_factor() == pytest.approx(
        CERTAIN_FACTOR_10, rel=SAME_DOUBLE)
    assert a.annuity_due_factor() == pytest.approx(ANNUITY_FACTOR, rel=SAME_DOUBLE)
    assert a.annuity_due_certain_factor() != a.annuity_due_factor()
    ratio = a.annuity_due_certain_factor() / a.annuity_due_factor()
    assert ratio == pytest.approx(0.3823, abs=5e-5)
    # The life factor is the one actually used on this point, and it is the larger.
    assert a.annuity_due_factor() > a.annuity_due_certain_factor()


# ---------------------------------------------------------------------------
# Pitfall 8: decrementing inside a guaranteed period


def test_pitfall_the_guarantee_is_unconditional_and_its_runoff_is_not_a_claim(
        kr_pension_anchor):
    """Pitfall 8 — decrementing ``pols_if`` by mortality inside a guaranteed period.

    Inside the 보증지급기간 the obligation is unconditional, so ``pols_if`` is flat from
    t = 25 to 34 while ``lives_if`` falls from 0.9657433263 to 0.9305473107, and not one of
    those deaths changes a won.  Conversely ``pols_death(34) = 0.0258992801`` is a run-off
    of the in-force and **not** a claim: ``db_pp(t) = 0`` once the annuity is in payment,
    so ``claims_death`` is zero from t = 25 even where ``pols_death`` is not.
    """
    a = kr_pension_anchor
    assert a.guar_term_y() == 10
    assert all(a.pols_if(t) == pytest.approx(0.6096911403, abs=INFORCE)
               for t in range(25, 35))
    assert a.lives_if(34) == pytest.approx(0.9305473107, abs=INFORCE)
    assert a.lives_if(34) < a.lives_if(25)
    assert all(a.pols_death(t) == 0.0 for t in range(25, 34))
    assert a.pols_death(34) == pytest.approx(0.0258992801, abs=INFORCE)
    assert a.pols_death(35) == pytest.approx(0.0040131254, abs=INFORCE)
    for t in range(25, 40):
        assert a.db_pp(t + 1) == 0.0
        assert a.claims(t, "DEATH") == 0.0
        assert a.claim_expenses(t) == 0.0
    # The guaranteed instalments are level and total gB, which is what check_annuity_total
    # asserts and what a model that decremented them would fail.
    assert sum(a.annuity_pp(t) for t in range(25, 35)) == pytest.approx(
        10 * ANNUITY_AMOUNT, rel=SAME_DOUBLE)
    assert a.check_annuity_total() is True


# ---------------------------------------------------------------------------
# Pitfall 9: recomputing B, or keeping the fund alive


def test_pitfall_b_is_struck_once_and_the_fund_does_not_survive_it(kr_pension_anchor):
    """Pitfall 9 — recomputing ``B``, or keeping the fund alive after annuitisation.

    ``B`` is struck once at t = n from ``F_net`` and never recomputed, and ``av_pp``,
    ``cv_pp`` and ``db_pp`` are zero from t = n + 1.  A model that kept rolling the fund
    forward and also paid the annuity would be double-counting the same money, and it
    would not fail any single row — only this identity.
    """
    a = kr_pension_anchor
    n = a.annuitisation_t()
    assert all(a.annuity_pp(t) == pytest.approx(ANNUITY_AMOUNT, rel=SAME_DOUBLE)
               for t in range(n, 81))
    assert a.annuity_pp(n - 1) == 0.0
    for t in range(n + 1, 81):
        assert a.av_pp(t) == 0.0
        assert a.cv_pp(t) == 0.0
        assert a.db_pp(t) == 0.0
        assert a.surr_tax_pp(t) == 0.0
    # The fund goes out exactly once: as the annuity, weighted by the count that receives
    # it, and never again as a benefit.
    df = a.result_cf()
    assert df.loc[n:, ["claims_death", "claims_lapse"]].to_numpy().sum() == 0.0
    assert df.loc[n:, "claims_annuity"].sum() == pytest.approx(
        ANNUITY_AMOUNT * sum(a.pols_if(t) for t in range(n, 81)), abs=WON)


# ---------------------------------------------------------------------------
# Pitfall 10: the maintenance charge outlives the premium


def test_pitfall_the_maintenance_charge_outlives_the_premium(kr_pension_anchor):
    """Pitfall 10 — forgetting that the maintenance charge outlives the premium.

    ``C(t)`` is ₩39,810.71 a year at t = 20…24, ₩199,053.55 in total, taken from the
    적립액 with no premium bearing it.  A model whose charges are all premium-based charges
    nothing in the five-year gap and overstates the fund at annuitisation by exactly that
    much, rolled up.
    """
    a = kr_pension_anchor
    assert a.maint_charge_rate(19) == pytest.approx(0.0300, abs=RATE)
    assert a.maint_charge_rate(20) == pytest.approx(0.0067, abs=RATE)
    # While a premium is due the charge comes off the premium, not off the fund.
    assert all(a.charge_from_av_pp(t) == 0.0 for t in range(0, 20))
    for t in range(20, 25):
        assert a.charge_from_av_pp(t) == pytest.approx(CHARGE_PAID_UP, rel=SAME_DOUBLE)
    assert sum(a.charge_from_av_pp(t) for t in range(20, 25)) == pytest.approx(
        199053.55, abs=WON)
    # And it stops at the 연금개시일, where the charge is the 0.5% inside the factor.
    assert a.charge_from_av_pp(25) == 0.0


# ---------------------------------------------------------------------------
# Pitfall 11: the acquisition charge stops


def test_pitfall_the_acquisition_charge_stops_after_seven_years(kr_pension_anchor):
    """Pitfall 11 — forgetting that the 계약체결비용 stops.

    ``alpha(t)`` runs for seven policy years only, so ``NP`` steps up by ₩89,128.4569 at
    t = 7.  A level-loading model gets the fund wrong in both directions — too high early,
    too low late — and cannot reproduce the published 환급률 curve at all.
    """
    a = kr_pension_anchor
    assert [a.acq_charge_rate(t) for t in range(0, 7)] == [0.015] * 7
    assert [a.acq_charge_rate(t) for t in range(7, 20)] == [0.0] * 13
    assert all(a.prem_to_av_pp(t) == pytest.approx(NP_WITH_ACQ, rel=SAME_DOUBLE)
               for t in range(0, 7))
    assert all(a.prem_to_av_pp(t) == pytest.approx(NP_AFTER_ACQ, rel=SAME_DOUBLE)
               for t in range(7, 20))
    assert a.prem_to_av_pp(20) == 0.0
    assert NP_AFTER_ACQ - NP_WITH_ACQ == pytest.approx(89128.4569, abs=5e-5)
    # The contract's whole acquisition cost is 1.50% x ₩500,000 x 84 = ₩630,000, and it
    # is itself well inside 별표 14's cap — which is a coherent explanation of why the
    # source product's published 해약공제 table is all zeros.
    whole = 0.015 * 500000 * 12 * 7
    assert whole == pytest.approx(630000.0, abs=WON)
    assert whole < a.surr_chg_cap_pp()


# ---------------------------------------------------------------------------
# Pitfall 12: the floor guarantees the rate, not the return


def test_pitfall_the_guaranteed_floor_does_not_waive_the_charges():
    """Pitfall 12 — treating the 최저보증이율 as a guarantee on the **return**.

    It guarantees the **credited rate**; the charges are still deducted beneath it.  So
    ``charge_from_av_pp`` must not consult the floor, and a contract crediting the floor
    still loses the loading: on the guaranteed-rate scenario the 환급률 after one year is
    under 100%, and at 납입완료 the fund is short of a charge-free accumulation of the same
    premiums at the same guaranteed rates by the whole loading, compounded.  The floor is a
    floor on ``credit_rate``, which is ``max`` of the two rates and nothing more.
    """
    with alt_model_points("floorscen", {220: {"rate_scenario": "floor"}}) as model:
        p = model.Projection[220]
        assert p.decl_rate(0) == 0.0
        assert p.credit_rate(0) == pytest.approx(p.min_guar_rate(0), abs=RATE)
        assert all(p.credit_rate(t) == pytest.approx(
            max(p.decl_rate(t), p.min_guar_rate(t)), abs=RATE) for t in range(0, 26))
        # The charges are unchanged in structure and still bite.
        assert p.acq_charge_rate(0) == pytest.approx(0.015, abs=RATE)
        assert p.maint_charge_rate(0) == pytest.approx(0.030, abs=RATE)
        assert p.prem_to_av_pp(0) == pytest.approx(
            6000000 * (1 - 0.015 - 0.030) * p.prem_timing_factor(0), rel=SAME_DOUBLE)
        for t in range(20, 25):
            assert p.charge_from_av_pp(t) == pytest.approx(
                6000000 * 0.0067 * p.prem_timing_factor(t), rel=SAME_DOUBLE)
            assert p.charge_from_av_pp(t) > 0.0
        # And the loading is still lost.  Against the same premiums accumulated at the
        # same guaranteed rates with no charges at all, the fund is short by the whole
        # loading, compounded — which is what "the floor guarantees the rate, not the
        # return" means arithmetically.
        unloaded = 0.0
        for t in range(0, 20):
            unloaded = ((unloaded + 6000000 * p.prem_timing_factor(t))
                        * (1.0 + p.credit_rate(t)))
        assert p.av_pp(20) < unloaded
        assert p.av_pp(20) / unloaded == pytest.approx(0.964456, abs=5e-6)
        # The shortfall sits between the two loading levels: 4.5% while the 계약체결비용
        # runs and 3.0% after it stops at seven years.
        assert 1.0 - 0.045 < p.av_pp(20) / unloaded < 1.0 - 0.030
        assert p.cv_pp(1) < p.cum_prem_pp(1)
        assert p.check_av_roll_fwd() is True and p.check_cv_floor() is True


# ---------------------------------------------------------------------------
# Pitfall 13: three interest rates that are not the crediting rate


def test_pitfall_the_yejeong_iyul_is_not_a_crediting_rate(kr_pension_anchor):
    """Pitfall 13 — mistaking the 예정이율, or the 평균공시이율, for a crediting rate.

    2.50% appears in the sources as the rate the charge and benefit structure was priced
    on, and every document that discloses it says it is not a guarantee.  It appears
    **nowhere** in the fund recursion.  The 평균공시이율, also 2.50% in 2026, is a third
    rate again and enters only inside the 표준해약공제액.  Three rates, three uses, and the
    only one the fund ever sees is ``credit_rate``.
    """
    a = kr_pension_anchor
    assert a.prem_int_rate() == pytest.approx(0.0250, abs=RATE)
    assert a.avg_decl_rate() == pytest.approx(0.0250, abs=RATE)
    assert a.decl_rate(0) == pytest.approx(0.0215, abs=RATE)
    assert a.credit_rate(0) == pytest.approx(0.0215, abs=RATE)
    assert a.credit_rate(0) != a.prem_int_rate()
    # The recursion runs on credit_rate, and only on credit_rate.
    for t in (0, 10, 24):
        assert a.av_pp(t + 1) == pytest.approx(
            a.av_pp_at(t, "AFT_PREM") * (1 + a.credit_rate(t)), rel=SAME_DOUBLE)
        assert a.av_pp(t + 1) != pytest.approx(
            a.av_pp_at(t, "AFT_PREM") * (1 + a.prem_int_rate()), rel=1e-9)
    # The 평균공시이율 is the discount rate inside 별표 14's 주6 and nowhere else.
    deduction = sum(6000000 * 0.015 / 1.025 ** s for s in range(7))
    assert deduction == pytest.approx(SURR_CAP_WORKINGS["note_6_deduction"], abs=WON)


# ---------------------------------------------------------------------------
# Pitfall 14: the tax layer is not a cash flow


def test_pitfall_the_tax_layer_never_enters_the_cash_flow(kr_pension_anchor):
    """Pitfall 14 — putting the tax layer into the cash flow.

    The 세액공제 (₩990,000 a year, ₩19,800,000 over the premium term) is paid by the state
    to the saver and the 16.5% 기타소득세 is withheld from the saver's proceeds.  Neither
    passes through the insurer's account, and folding either in would misstate the
    liability in a way no reconciliation would catch — which is why ``check_net_cf``
    re-derives the ledger from the published columns and fails the moment one is added.
    """
    a = kr_pension_anchor
    assert a.net_cf(0) == pytest.approx(
        a.premiums(0) - a.claims(0) - a.expenses(0) - a.claim_expenses(0)
        - a.commissions(0) - a.policy_loans(0), rel=SAME_DOUBLE)
    assert a.tax_credit_pp(0) > 0.0
    assert a.net_cf(0) + a.tax_credit_pp(0) != pytest.approx(a.net_cf(0), abs=1.0)
    # The surrender payment is the whole surrender value: the withholding is taken from
    # the policyholder's proceeds, not from the insurer's payment.
    assert a.claims(9, "LAPSE") == pytest.approx(
        a.cv_pp_net(10) * a.pols_lapse(9), rel=SAME_DOUBLE)
    assert a.surr_tax_pp(10) > 0.0
    assert a.claims(9, "LAPSE") != pytest.approx(
        (a.cv_pp_net(10) - a.surr_tax_pp(10)) * a.pols_lapse(9), rel=1e-6)
    # And the annuity instalment is paid gross of the 연금소득세 withholding.
    assert a.annuity_tax_pp(25) == pytest.approx(
        a.annuity_pp(25) * 0.033, rel=SAME_DOUBLE)
    assert a.claims(25, "ANNUITY") == pytest.approx(
        a.annuity_pp(25) * a.pols_if(25), rel=SAME_DOUBLE)
    assert a.check_net_cf() is True


# ---------------------------------------------------------------------------
# Pitfall 15: the 연금수령한도 where the statute disapplies it


def test_pitfall_the_annuity_limit_is_disapplied_from_the_eleventh_year(
        pension_savings, kr_pension_anchor):
    """Pitfall 15 — applying the 연금수령한도 formula where it does not apply.

    Where the 연금수령연차 reaches 11 the formula is **disapplied entirely**, and at the
    anchor cell it is 11 in the first payment year.  A model that evaluated
    ``평가액 / (11 − 연금수령연차) x 120/100`` regardless divides by zero, or caps an
    annuity that no rule caps.  Point 6, annuitising at 55, is the case where the counter
    starts at 1 and the limit is a real number: 12% of the 평가액, ₩3,603,600 against an
    instalment of ₩2,143,455.
    """
    a = kr_pension_anchor
    assert a.annuity_year_no(25) == 11
    assert a.annuity_limit_pp(25) == pytest.approx(
        a.annuity_fund_net_pp(), rel=SAME_DOUBLE)
    assert a.annuity_limit_pp(25) > a.annuity_pp(25)
    assert a.check_annuity_limit() is True

    p = pension_savings.Projection[6]
    assert p.annuity_year_no(5) == 1
    assert p.annuity_limit_pp(5) == pytest.approx(
        p.annuity_fund_net_pp() / 10.0 * 1.2, rel=SAME_DOUBLE)
    assert p.annuity_limit_pp(5) == pytest.approx(3603600.0, abs=WON)
    assert p.annuity_amount_pp() == pytest.approx(2143455.00, abs=WON)
    assert p.annuity_limit_pp(5) > p.annuity_amount_pp()
    assert p.check_annuity_limit() is True
    # The counter runs from the later of 만 55세 and five years of the account.
    assert [p.annuity_year_no(t) for t in range(5, 16)] == list(range(1, 12))


# ---------------------------------------------------------------------------
# Pitfall 16: the 표준해약공제액 on the gross premium


def test_pitfall_the_statutory_cap_works_on_the_net_annual_premium(kr_pension_anchor):
    """Pitfall 16 — computing the 표준해약공제액 on the gross premium.

    별표 14 주3 works on the **연납순보험료** — the annual premium less the levelled
    loading, ₩5,577,000 here, not ₩6,000,000 — and 주6 then subtracts the discounted
    acquisition loading.  Using the gross premium gives ₩2,160,000 before 주6 against
    ₩2,007,720, a 7.6% overstatement of a cap that is meant to bind.  The whole
    computation is reproduced step by step, because it is a five-line reading of a
    regulation and each line is a place to go wrong.
    """
    a = kr_pension_anchor
    m = a.premium_term_y()
    loading = sum(6000000 * (a.acq_charge_rate(s) + a.maint_charge_rate(s))
                  for s in range(m))
    assert loading == pytest.approx(SURR_CAP_WORKINGS["whole_term_loading"], abs=WON)
    levelled = loading / 10.0
    assert levelled == pytest.approx(SURR_CAP_WORKINGS["levelled"], abs=WON)
    net_premium = 6000000 - levelled
    assert net_premium == pytest.approx(SURR_CAP_WORKINGS["net_annual_premium"], abs=WON)
    gross_cap = 0.03 * net_premium * min(m, 12)
    assert gross_cap == pytest.approx(SURR_CAP_WORKINGS["gross_cap"], abs=WON)
    assert a.surr_chg_cap_pp() == pytest.approx(
        gross_cap - SURR_CAP_WORKINGS["note_6_deduction"], abs=WON)
    assert a.surr_chg_cap_pp() == pytest.approx(SURR_CAP_WORKINGS["cap"], abs=WON)
    # The gross-premium reading, and how far out it is.
    on_gross = 0.03 * 6000000 * min(m, 12)
    assert on_gross == pytest.approx(2160000.0, abs=WON)
    assert (on_gross - gross_cap) / gross_cap == pytest.approx(0.076, abs=5e-4)
    # The composite uses none of the headroom: the charge is zero at every duration.
    assert all(a.surr_chg_pp(t) == 0.0 for t in range(0, 26))
    assert a.check_surr_chg_cap() is True


def test_the_cap_binds_the_point_that_carries_a_real_front_end_charge(pension_savings):
    """별표 14's cap is asserted on the point where 해약공제액 is not zero.

    Point 8 carries the postal insurer's front-end schedule — 8.67% of the annual premium
    at year 1 running off linearly to zero at the fifth — so ``cv_pp`` separates from
    ``av_pp`` for five years, which on the composite it never does.  ``check_surr_chg_cap``
    holds the charge inside the statutory cap on both, which is what makes it a check
    rather than a restatement of a zero.
    """
    p = pension_savings.Projection[8]
    assert p.surr_chg_rate() == pytest.approx(0.0867, abs=1e-6)
    assert p.surr_chg_pp(1) == pytest.approx(0.0867 * 6000000, abs=WON)
    assert p.surr_chg_pp(1) == pytest.approx(520200.0, abs=WON)
    assert p.surr_chg_pp(2) == pytest.approx(390150.0, abs=WON)
    assert p.surr_chg_pp(3) == pytest.approx(260100.0, abs=WON)
    assert p.surr_chg_pp(4) == pytest.approx(130050.0, abs=WON)
    assert p.surr_chg_pp(5) == 0.0
    for t in range(1, 5):
        assert p.cv_pp(t) == pytest.approx(p.av_pp(t) - p.surr_chg_pp(t), rel=SAME_DOUBLE)
        assert p.cv_pp(t) < p.av_pp(t)
        assert p.db_pp(t) > p.cv_pp(t)          # the death benefit bears no 해약공제액
    assert p.cv_pp(5) == pytest.approx(p.av_pp(5), rel=SAME_DOUBLE)
    assert max(p.surr_chg_pp(t) for t in range(0, 26)) < p.surr_chg_cap_pp()
    assert p.check_surr_chg_cap() is True and p.check_cv_floor() is True


# ---------------------------------------------------------------------------
# Pitfall 17: proj_len is the last index


def test_pitfall_proj_len_is_the_last_index_not_a_count(pension_savings):
    """Pitfall 17 — reading ``proj_len()`` as a count.

    It is the **last index**: 80 at the anchor cell, with 81 rows in ``result_cf()``.  An
    off-by-one here silently drops the terminal row, which on the life form is where the
    last survivors die — ``q`` = 1 at the terminal age and the whole remaining in-force
    goes out at once.
    """
    for point_id in (1, 4, 6):
        p = pension_savings.Projection[point_id]
        assert len(p.result_cf()) == p.proj_len() + 1
        assert list(p.result_cf().index) == list(range(0, p.proj_len() + 1))
    a = pension_savings.Projection[1]
    assert a.proj_len() == a.omega_age("annuitant_issue") - a.issue_age() == 80
    assert a.age(a.proj_len()) == 120
    assert a.mort_rate(80) == 1.0
    assert a.pols_death(80) == pytest.approx(a.pols_if(80), rel=SAME_DOUBLE)
    assert a.pols_if(81) == 0.0
    assert a.claims(80, "ANNUITY") == pytest.approx(8465.37, abs=WON)
    # The certain form's horizon is the last instalment, not a mortality terminal age.
    c = pension_savings.Projection[4]
    assert c.proj_len() == c.annuitisation_t() + c.payout_term_y() - 1


# ---------------------------------------------------------------------------
# Pitfall 18: the 100.1% floor is a survival guarantee


def test_pitfall_the_minimum_fund_does_not_protect_a_death_claim(pension_savings,
                                                                kr_pension_anchor):
    """Pitfall 18 — assuming the 100.1% floor protects a **death** claim.

    It is a survival guarantee applied once, at t = n, to a policy in force; a death in
    deferral is paid the fund, which may be less than premiums paid — and is, for the first
    four policy years at the anchor cell.  Its base is premiums paid **including 추가납입**,
    which is why ``cum_prem_pp`` adds both and why point 8's floor is ₩240,240,000 on a
    ₩240,000,000 contribution.
    """
    a = kr_pension_anchor
    for t in (1, 2, 3, 4):
        assert a.db_pp(t) < a.cum_prem_pp(t)
        assert a.db_pp(t) < 1.001 * a.cum_prem_pp(t)
    assert a.db_pp(5) > a.cum_prem_pp(5)
    # The guarantee applies once, at the 연금개시일, and only to the fund that buys the
    # annuity.
    assert a.min_fund_pp() == pytest.approx(1.001 * a.cum_prem_pp(25), rel=SAME_DOUBLE)
    assert a.annuity_fund_pp() == pytest.approx(
        max(a.av_pp(25), a.min_fund_pp()), rel=SAME_DOUBLE)
    assert a.check_min_fund() is True
    # And its base is the whole contribution, 기본 and 추가 together.
    p = pension_savings.Projection[8]
    assert p.addl_prem_pp() == pytest.approx(6000000.0, abs=WON)
    assert p.cum_prem_pp(25) == pytest.approx(240000000.0, abs=WON)
    assert p.min_fund_pp() == pytest.approx(240240000.0, abs=WON)
    assert p.check_min_fund() is True


def test_the_additional_premium_bears_the_management_charge_only(pension_savings):
    """추가납입 is a premium that bears 계약관리비용 and not 계약체결비용, and it is capped.

    That asymmetry is the whole economic point of the 연금저축추가납입특약, and it is why
    the additional premium cannot simply be added to the basic one: at the anchor's
    durations it is credited at 98% where the basic premium is credited at 95.5%.
    """
    p = pension_savings.Projection[8]
    basic = 6000000 * (1 - 0.015 - 0.030)
    additional = 6000000 * (1 - 0.02)
    assert p.prem_to_av_pp(0) == pytest.approx(
        (basic + additional) * p.prem_timing_factor(0), rel=SAME_DOUBLE)
    assert additional > basic
    # Inside the 200% relativity cap and the ₩18,000,000 statutory ceiling.
    assert p.addl_prem_pp() <= 2.0 * p.prem_pp()
    assert p.addl_prem_pp() + p.prem_pp() <= p.tax_basis("contribution_ceiling")
    # And the premium income column carries both.
    assert p.premiums(0) == pytest.approx(12000000.0, abs=WON)


# ---------------------------------------------------------------------------
# The [std] parameters the notes state


def test_the_std_scalar_assumptions_the_notes_state(pension_savings):
    """The five pricing-table [std] values, read off the model rather than off the notes.

    Each is a standardization with no contractual counterpart — the best-estimate uplift on
    a loaded pricing table, and the four numbers that describe a policy loan for which no
    retrieved document gives a rate at all.  A silent change to any of them should fail a
    test rather than move a result.
    """
    p = pension_savings.Projection[1]
    for item, value in STD_SCALARS.items():
        assert p.pricing_basis(item) == pytest.approx(value, rel=1e-12), item
    for item, value in STD_EXPENSES.items():
        assert p.expense_basis(item) == pytest.approx(value, rel=1e-12), item
    # And each of them says so on its own row.
    pricing = pension_savings.Data.pricing_table()
    for item in STD_SCALARS:
        assert "[std]" in pricing.loc[item, "provenance"], item
    expenses = pension_savings.Data.expense_table()
    for item in STD_EXPENSES:
        assert "[std]" in expenses.loc[item, "provenance"], item
    # The commission rows are zero because a source says so, not because a modeller chose.
    assert p.expense_basis("comm_init_rate") == 0.0
    assert p.expense_basis("comm_renewal_rate") == 0.0
    assert "[std]" not in expenses.loc["comm_init_rate", "provenance"]
    assert all(p.commissions(t) == 0.0 for t in range(0, 81))


def test_the_sourced_scalar_parameters_are_not_standardizations(pension_savings):
    """The contractual and regulatory scalars, with their values and their provenance.

    These are the numbers a retrieved document states — the two charge rates and their
    periods, the 0.5% annuity charge, the 100.1% floor, and 별표 14's four coefficients —
    and tagging any of them [std] would be a claim that the sources do not say what they
    say.  Asserting the value and the absence of a [std] tag together is what keeps the
    two kinds of number apart as the table is edited.
    """
    p = pension_savings.Projection[1]
    pricing = pension_savings.Data.pricing_table()
    for item, value in SOURCED_SCALARS.items():
        assert p.pricing_basis(item) == pytest.approx(value, rel=1e-12), item
        provenance = pricing.loc[item, "provenance"]
        assert "[std]" not in provenance, item
        assert "[S" in provenance or "[REG-R" in provenance, item


def test_the_tax_basis_the_notes_state(pension_savings):
    """The 세액공제, 기타소득세 and 연금소득세 parameters, and the two statutory tests.

    The model takes the 16.5% band because a contract does not know its owner's income;
    the 13.2% alternative is carried beside it so the choice is visible rather than
    implicit.  The 종신계약 rate of 3.3% is a standing 2.2-point advantage over the 5.5%
    that a fixed-term annuitant under 70 pays, which is why the base run elects the life
    form.
    """
    p = pension_savings.Projection[1]
    for item, value in TAX_SCALARS.items():
        assert p.tax_basis(item) == pytest.approx(value, rel=1e-12), item
    assert p.tax_credit_rate() == pytest.approx(0.165, abs=RATE)
    assert p.tax_basis("credit_rate_high_income") < p.tax_credit_rate()
    # The life form draws the flat 3.3% at every age; a certain form is banded on age.
    assert p.pension_tax_rate(25) == pytest.approx(0.033, abs=RATE)
    assert p.pension_tax_rate(55) == pytest.approx(0.033, abs=RATE)
    certain = pension_savings.Projection[4]
    assert certain.payout_form() == "certain"
    assert certain.pension_tax_rate(35) == pytest.approx(0.055, abs=RATE)   # 만 60
    assert certain.pension_tax_rate(45) == pytest.approx(0.044, abs=RATE)   # 만 70
    assert p.pension_tax_rate(24) == 0.0        # nothing is withheld before the payout
    # No shipped 확정기간 point reaches the 80-and-over band, so it is exercised on a
    # point supplied through the model_point_file Reference; leaving it unreached would
    # be a band nobody has run.
    with alt_model_points(
            "taxband",
            {230: {"payout_form": "certain", "payout_term_y": 20}}) as model:
        q = model.Projection[230]
        assert q.pension_tax_rate(25) == pytest.approx(0.055, abs=RATE)   # 만 65
        assert q.pension_tax_rate(30) == pytest.approx(0.044, abs=RATE)   # 만 70
        assert q.pension_tax_rate(39) == pytest.approx(0.044, abs=RATE)   # 만 79
        assert q.pension_tax_rate(40) == pytest.approx(0.033, abs=RATE)   # 만 80
        assert q.pension_tax_rate(44) == pytest.approx(0.033, abs=RATE)


def test_the_declared_rate_and_the_floor_ladder_are_step_functions(pension_savings):
    """공시이율 by scenario and 최저보증이율 by duration, both read as steps of policy year.

    A Korean declared rate is majority-weighted to the insurer's own realised investment
    return and moves slowly: it is not a market rate and must not be modelled as one.  The
    ``hybrid`` scenario is the one retrieved design that fixes a rate for the first five
    contract years, and it is exercised at model point 8.
    """
    p = pension_savings.Projection[1]
    assert all(p.decl_rate(t) == pytest.approx(0.0215, abs=RATE) for t in (0, 5, 19, 25))
    ladder = pension_savings.Data.guar_rate_table()
    assert list(ladder.index) == [0, 5, 10]
    assert list(ladder["min_guar_rate"]) == pytest.approx([0.0125, 0.0100, 0.0050],
                                                          abs=RATE)
    hybrid = pension_savings.Projection[8]
    assert hybrid.rate_scenario() == "hybrid"
    assert all(hybrid.decl_rate(t) == pytest.approx(0.035, abs=RATE) for t in range(0, 5))
    assert all(hybrid.decl_rate(t) == pytest.approx(0.0215, abs=RATE)
               for t in range(5, 26))
    # The floor never binds on the base scenario and always binds on the floor one.
    assert all(p.credit_rate(t) > p.min_guar_rate(t) for t in range(0, 26))
    floor = pension_savings.Projection[6]
    assert all(floor.credit_rate(t) == pytest.approx(floor.min_guar_rate(t), abs=RATE)
               for t in range(0, 5))


def test_the_lapse_table_ships_two_argued_vectors_and_not_a_fitted_one(pension_savings):
    """The ``pension`` vector and the ``savings`` comparison vector, side by side.

    No public Korean lapse statistic for 연금저축보험 by policy year exists, so both are
    [std] and argued from the contract: the pension vector is materially flatter, because
    a surrender costs 16.5% 기타소득세 on essentially the whole payout, and it steps
    **down** at 납입완료 rather than up.  Carrying the second vector is what lets the two
    be run side by side rather than asserted against each other in prose.
    """
    table = pension_savings.Data.lapse_table()
    assert set(table.index.get_level_values(0)) == {"pension", "savings"}
    assert set(table.index.get_level_values(1)) == {"premium_paying", "paid_up",
                                                    "in_payment"}
    assert all("[std]" in v or "[S" in v for v in table["provenance"])
    pension = pension_savings.Projection[1]
    savings = pension_savings.Projection[5]
    assert pension.lapse_basis() == "pension" and savings.lapse_basis() == "savings"
    assert [pension.lapse_rate(t) for t in (0, 1, 2, 3, 5, 10)] == pytest.approx(
        [0.040, 0.035, 0.030, 0.025, 0.020, 0.015], abs=RATE)
    assert [savings.lapse_rate(t) for t in (0, 1, 2, 3, 5)] == pytest.approx(
        [0.080, 0.070, 0.060, 0.050, 0.040], abs=RATE)
    # The comparison vector loses far more business before annuitisation.
    assert savings.pols_if(savings.annuitisation_t()) == pytest.approx(
        0.3831301998, abs=INFORCE)
    assert savings.pols_if(30) < pension.pols_if(25)
    # And both are zero once the annuity is in payment.
    assert pension.lapse_rate(25) == 0.0 and savings.lapse_rate(30) == 0.0


def test_the_mortality_table_is_a_construction_that_ships_its_own_recipe(
        pension_savings, kr_pension_anchor):
    """The shipped rates are the stated Makeham law, and the file says so on every row.

    경험생명표 is not published, so ``mort_table.csv`` is a [std] construction rather than a
    copy, and ``check_mort_law`` re-derives every rate the projection touches from the
    three parameters in ``mort_anchor_table.csv``.  The female table is the male law set
    back four years and the revised vintage is the issue vintage times 0.85; both are
    properties of the file, and both are asserted here so that swapping in a real table is
    a visible act rather than a silent one.
    """
    a = kr_pension_anchor
    assert a.check_mort_law() is True
    for x in (40, 65, 90):
        assert a.mort_rate_at_age("annuitant_issue", x) == pytest.approx(
            a.mort_rate_law("annuitant_issue", x), abs=1e-15)
    assert a.mort_anchor("annuitant_issue", "age_setback") == 0
    assert a.mort_anchor("annuitant_issue", "improve_factor") == 1.0
    assert a.mort_anchor("annuitant_revised", "improve_factor") == pytest.approx(
        0.85, abs=1e-12)
    assert a.omega_age("annuitant_issue") == 120
    female = pension_savings.Projection[2]
    assert female.mort_anchor("annuitant_issue", "age_setback") == 4
    assert female.mort_rate_at_age("annuitant_issue", 65) == pytest.approx(
        a.mort_rate_at_age("annuitant_issue", 61), abs=1e-12)
    table = pension_savings.Data.mort_table()
    assert set(table.index.get_level_values(0)) == {"annuitant_issue",
                                                    "annuitant_revised"}
    assert all("[std]" in v for v in table["provenance"])


def test_the_construction_reproduces_the_longevity_the_illustration_implies(
        pension_savings, kr_pension_anchor):
    """Curtate e(65) is 33.31 years for men and 36.97 for women, and that is the finding.

    Not the 제10회's published 23.7: solving the published life annuity at 2.15% gives a
    factor consistent with a 65-year-old male living to about 97, so the illustration is
    priced on a 연금사망률 loaded on the survival side, and the table reproduces the annuity
    because the annuity is what it was fitted to.  The sex gap of 3.66 years is the
    published 3.4 within the setback's resolution.  Stating both numbers here keeps the
    tension visible instead of letting a reader assume the table is a population one.
    """
    def curtate(projection, table, age):
        omega = projection.omega_age(table)
        survivors, total = 1.0, 0.0
        for x in range(age, omega):
            survivors *= 1.0 - projection.mort_rate_at_age(table, x)
            total += survivors
        return total

    male = curtate(kr_pension_anchor, "annuitant_issue", 65)
    female = curtate(pension_savings.Projection[2], "annuitant_issue", 65)
    assert male == pytest.approx(33.31, abs=0.005)
    assert female == pytest.approx(36.97, abs=0.005)
    assert female - male == pytest.approx(3.66, abs=0.005)
    assert male > 23.7          # the published 제10회 65세 기대여명, and not this table
    # The fitted law is honest about missing the published rates it was fitted to.
    assert kr_pension_anchor.mort_rate_at_age("annuitant_issue", 70) / 0.00291 == (
        pytest.approx(1.30, abs=0.005))
    assert kr_pension_anchor.mort_rate_at_age("annuitant_issue", 80) / 0.01346 == (
        pytest.approx(0.72, abs=0.005))


# ---------------------------------------------------------------------------
# Structure and inputs


def test_inputs_live_beside_the_model():
    """The nine input CSVs sit in the model folder's parent directory, not inside it."""
    expected = {"model_point_table.csv", "mort_table.csv", "mort_anchor_table.csv",
                "lapse_table.csv", "decl_rate_table.csv", "guar_rate_table.csv",
                "pricing_table.csv", "expense_table.csv", "tax_table.csv"}
    assert expected == {p.name for p in CSV_DIR.iterdir() if p.suffix == ".csv"}
    assert (MODEL_DIR / "_system.json").is_file()
    assert not list(MODEL_DIR.glob("*.csv"))


def test_the_input_csvs_are_utf8_without_a_bom():
    """A BOM survives into the first column name and breaks the index lookup silently."""
    for csv in CSV_DIR.glob("*.csv"):
        assert csv.open("rb").read(3) != b"\xef\xbb\xbf", "%s carries a BOM" % csv.name
        csv.read_text(encoding="utf-8")


def test_an_input_can_be_swapped_without_touching_formulas():
    """Point a filename Reference at a different file and the projection follows.

    This is the property the external-file layout buys, and it is what a user with a filed
    or company basis does: a same-schema CSV drops in with no formula change.  Doubling the
    declared rate has to move the fund at annuitisation and nothing about the structure.
    """
    src = pd.read_csv(CSV_DIR / "decl_rate_table.csv", index_col=["scenario", "from_year"])
    lifted = src.copy()
    lifted["decl_rate"] = lifted["decl_rate"] + 0.01

    model = _reread("swap")
    alt_name = "decl_rate_table_lifted.csv"
    alt_path = model.Data.input_dir() / alt_name
    try:
        lifted.to_csv(alt_path)
        base = model.Projection[1].annuity_fund_pp()
        model.Data.decl_rate_file = alt_name
        model.Data.clear_all()
        model.Projection.clear_all()
        p = model.Projection[1]
        assert p.decl_rate(0) == pytest.approx(0.0315, abs=RATE)
        assert p.credit_rate(0) == pytest.approx(0.0315, abs=RATE)
        assert p.annuity_fund_pp() > base
        assert p.check_av_roll_fwd() is True
        assert p.check_min_fund() is True
    finally:
        alt_path.unlink(missing_ok=True)
        model.close()


def test_the_docstrings_carry_this_product_s_own_reference_material(pension_savings):
    """The symbol map, the age basis, and the three names the notes say needed care.

    The ``Projection`` docstring is the cross-walk a reader holding the technical notes
    beside the model uses, so it has to name the symbols the notes actually use — ``n``,
    ``B``, ``F`` and ``adue`` among them — and to keep ``decl_rate``, ``credit_rate`` and
    ``prem_int_rate`` explicitly apart, since collapsing any two of those is a pitfall in
    its own right.
    """
    doc = " ".join(pension_savings.Projection.doc.split())
    assert "Notes symbol" in doc
    for symbol in ("proj_len", "model_point", "annuitisation_t", "annuity_amount_pp",
                   "annuity_fund_pp", "annuity_due_factor", "credit_rate", "decl_rate",
                   "prem_int_rate", "av_pp", "cv_pp"):
        assert symbol in doc, symbol
    assert "보험나이" in doc and "만나이" in doc
    assert "income positive" in doc
    model_doc = " ".join(pension_savings.doc.split())
    for phrase in ("mechanics demonstration", "external", "once per model",
                   "Data", "Projection"):
        assert phrase in model_doc, phrase
    data_doc = " ".join(pension_savings.Data.doc.split())
    assert "TradLife_A" in data_doc
    assert "input_dir" in data_doc and "model_point_table" in data_doc
