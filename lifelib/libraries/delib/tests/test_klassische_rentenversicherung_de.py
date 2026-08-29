"""Golden and structural tests for RV_DE_A.

The golden values are the worked example in
products/klassische_rentenversicherung/technical-notes.md ("Worked example"), which is a
**configuration** rather than a scenario: model point 1, ``DE-RV-0001``, a *klassische
aufgeschobene private Rentenversicherung* on a male aged 50 at issue in 2026, new business
(``duration_init = 0``) so the frame opens at ``t = 1``, one policy in force; a *laufender
Beitrag* of 3 000,00 EUR a year payable annually (``freq_load = 1,000``) for seventeen years
over a seventeen-year *Aufschubzeit*, so the *Rentenbeginn* falls at the end of policy year 17
at attained age 67; a *Rechnungszins* of 1,00 %, the 2026 guarantee vintage; the ``zillmer_25``
charge set, hence a *Beitragssumme* of 51 000,00 EUR and a zillmered acquisition charge of
1 275,00 EUR taken in full from the first premium; a *garantierter Rentenfaktor* of 28,00 EUR
against a ``base`` *aktueller Rentenfaktor* of 32,00 EUR at age 67, so the current factor wins
the ``max``; a ``base`` declared *laufende Verzinsung* of 2,55 %, hence an interest-surplus rate
of 1,55 %; a *Beitragsrückgewähr* death benefit on premiums only (``db_incl_surplus = 0``); no
guaranteed contract value; a *Rentengarantiezeit* of ten years; a *Kapitalwahlrecht* take-up of
30 %; the ``konstant`` payout system; no *Dynamik*, no *Beitragsfreistellung* and no opening
balances.  Hence ``proj_len() = 121 - 50 = 71``: the accumulation phase is ``t = 1 ... 17``, the
*Rentengarantiezeit* covers ``t = 18 ... 27``, and the survivor-weighted annuity runs from
``t = 28`` to ``t = 71``.

Because a life annuity is projected to exhaustion the frame is seventy-one rows long, so the
notes print the **whole** accumulation phase and sample the payout at ``t = 18, 27, 28, 40, 55``
and ``71``.  All twenty-three rows are asserted here, with the totals, which the notes sum **at
full precision and then round** — 23 485,03 EUR of annuity payments that way against
23 484,99 EUR from the rounded cells.  The goldens are hard-coded rather than pickled so a
reviewer can compare them with the notes by eye, at the precision the notes display: money to
the cent, ``pols_if`` to six decimals.

Beyond the worked example this module asserts the notes' three independent rebuilds and its two
closure identities; both documented variants, the *Einmalbeitrag* form (model point 2) and the
2,75 % legacy vintage (model point 6), row by row and in total; all nine ``check_*`` identities
and their per-``t`` residuals, on the anchor and on the six points that switch an option on,
``check_net_cf()`` among them — this library's first ruling, which rebuilds ``net_cf`` from
``result_cf()``'s own published columns; **one test per numbered modeling pitfall in the
technical notes**, eighteen of them, each named for its pitfall; and the frame's shape and sign
convention, the enum accessors, the docstrings a reader relies on, the shipped tables' own
provenance, and that an input can be swapped without touching a formula.

There is **no whole-model-point-table sweep here**: the conventions suite owns the single
sweep, because a model point's first evaluation is the most expensive thing in the run.
"""
import re

import modelx as mx
import pytest
from modelx.core.errors import FormulaError

from de_registry import MODELS, LIB


def flat(doc):
    """Collapse whitespace, so a phrase split across a line break still matches.

    The conventions suite normalises the same way, and for the same reason.
    """
    return re.sub(r"\s+", " ", doc)


CENT = 0.005          # money displayed to 2 d.p.
SIX_DP = 0.0000005    # pols_if displayed to 6 d.p.

MODEL_DIR = LIB / MODELS["RV_DE_A"][0]
INPUT_DIR = MODEL_DIR.parent

CSV_FILES = {
    "model_point_table.csv", "mort_table.csv", "decl_rate_table.csv",
    "rentenfaktor_table.csv", "charge_table.csv", "lapse_table.csv",
    "freq_load_table.csv", "param_table.csv",
}

# The notes' worked-example table, model point 1.  Rows 1-17 are the whole accumulation phase;
# 18, 27, 28, 40, 55 and 71 sample the payout at the first annuity year, the last guaranteed
# year, the first survivor-weighted year and three points down the tail.  `av` and `av_sur` are
# the two balances at the **start** of the row's year, and are state rather than cash flow.
#
# t: (pols_if, av, av_sur, premiums, claims_death, claims_lapse, claims_commutation,
#     annuity_payments, expenses, net_cf)

WORKED_EXAMPLE = {
    1:  (1.000000,     0.00,    0.00, 3000.00,   5.02,  158.54,    0.00,   0.00, 452.39,  2384.04),
    2:  (0.938426,  1517.10,   23.28, 2815.28,  10.12,  248.91,    0.00,   0.00,  48.90,  2507.35),
    3:  (0.889902,  4032.52,   84.53, 2669.71,  15.46,  319.83,    0.00,   0.00,  46.67,  2287.75),
    4:  (0.848216,  6335.16,  179.84, 2544.65,  21.09,  362.62,    0.00,   0.00,  44.78,  2116.15),
    5:  (0.812600,  8474.57,  306.74, 2437.80,  27.12,  445.12,    0.00,   0.00,  43.69,  1921.87),
    6:  (0.778360, 10439.40,  461.52, 2335.08,  33.47,  525.93,    0.00,   0.00,  42.62,  1733.06),
    7:  (0.745440, 12238.83,  641.09, 2236.32,  40.15,  601.23,    0.00,   0.00,  41.58,  1553.36),
    8:  (0.713787, 13881.56,  842.56, 2141.36,  47.17,  587.35,    0.00,   0.00,  40.12,  1466.71),
    9:  (0.686908, 15455.93, 1068.70, 2060.72,  54.83,  647.55,    0.00,   0.00,  39.34,  1319.01),
    10: (0.660906, 16904.27, 1313.89, 1982.72,  62.94,  704.05,    0.00,   0.00,  38.56,  1177.17),
    11: (0.635750, 18232.03, 1575.91, 1907.25,  71.50,  756.98,    0.00,   0.00,  37.79,  1040.97),
    12: (0.611408, 19444.42, 1852.62, 1834.22,  81.20, 1382.42,    0.00,   0.00,  38.87,   331.74),
    13: (0.572603, 20013.45, 2086.42, 1717.81,  89.21,  711.72,    0.00,   0.00,  35.01,   881.87),
    14: (0.553206, 21091.10, 2390.82, 1659.62, 100.57,  751.23,    0.00,   0.00,  34.47,   773.35),
    15: (0.534287, 22078.63, 2706.76, 1602.86, 112.82,  788.38,    0.00,   0.00,  33.94,   667.73),
    16: (0.515827, 22978.50, 3032.52, 1547.48, 126.01,  823.18,    0.00,   0.00,  33.40,   564.89),
    17: (0.497806, 23793.00, 3366.34, 1493.42, 140.21,  855.65, 8596.26,   0.00,  50.15, -8148.86),
    18: (0.336143,     0.00,    0.00,    0.00,   0.00,    0.00,    0.00, 862.65,  14.36,  -877.01),
    27: (0.311032,     0.00,    0.00,    0.00,   0.00,    0.00,    0.00, 862.65,  17.36,  -880.01),
    28: (0.307034,     0.00,    0.00,    0.00,   0.00,    0.00,    0.00, 787.95,  16.24,  -804.19),
    40: (0.229120,     0.00,    0.00,    0.00,   0.00,    0.00,    0.00, 588.00,  16.02,  -604.02),
    55: (0.055062,     0.00,    0.00,    0.00,   0.00,    0.00,    0.00, 141.31,   6.09,  -147.39),
    71: (0.000000,     0.00,    0.00,    0.00,   0.00,    0.00,    0.00,   0.00,   0.00,    -0.00),
}

# The notes' Total row: summed over all 71 policy years at full precision, then rounded.
TOTALS = {
    "premiums": 35986.30, "claims_death": 1038.91, "claims_lapse": 10670.70,
    "claims_commutation": 8596.26, "annuity_payments": 23485.03, "expenses": 1669.77,
    "net_cf": -9474.37,
}

# The same columns summed from the *rounded* cells, which the notes say the Total row is not.
ROUNDED_CELL_TOTALS = {
    "premiums": 35986.30, "claims_death": 1038.89, "claims_lapse": 10670.69,
    "claims_commutation": 8596.26, "annuity_payments": 23484.99, "expenses": 1669.75,
    "net_cf": -9474.40,
}

# The notes' independent check 1 -- policy year 1 rebuilt from the tariff parameters alone.
YEAR_ONE = {
    "beitragssumme": 51000.00, "alpha_total": 1275.00, "beta": 120.00, "gamma": 0.00,
    "mort_rate_guar": 0.00145610, "rho": 4.3683, "charges_due": 1399.3683,
    "prem_to_av": 1600.6317, "int_credited": 16.0063, "av_end": 1616.6380,
    "mort_rate": 0.00167451, "deaths": 0.00167451, "lapses": 0.05989953,
    "claims_death": 5.0235, "spread_diff": 1030.2000, "cv_floor": 2646.8380,
    "cv_tariff": 1608.6189, "claims_lapse": 158.5444, "expenses": 452.3889,
    "net_cf": 2384.0432,
}

# The notes' independent check 3 -- the Rentenbeginn rebuilt from the two balances.
CONVERSION = {
    "av_pp": 51070.4278, "av_sur_pp": 7718.5532, "capital_gross": 58788.9809,
    "val_reserve": 881.8347, "capital_conv": 59670.8156,
    "rate_guar": 28.00, "rate_curr": 32.00, "rate_appl": 32.00,
    "annuity_guar_mth": 190.9466, "annuity_pp": 2566.3224,
    "pols_surv_rb": 0.480205, "pols_death_17": 0.002749, "pols_lapse_17": 0.014852,
    "commutations": 0.144061, "claims_commutation": 8596.2645,
    "annuitisations": 0.336143, "annuity_payments_18": 862.6523,
}

# The notes' closure split, summed over all 71 years at full precision.
CLOSURE = {"deaths": 0.371640, "lapses": 0.484298, "commutations": 0.144061,
           "survivors": 0.000000}

# Variant A -- the Einmalbeitrag form, model point 2.
# t: (pols_if, av, av_sur, premiums, claims_death, claims_lapse, annuity_payments,
#     expenses, net_cf)
EINMAL = {
    1:  (1.000000,     0.00,    0.00, 50000.00, 79.07, 2888.80,    0.00, 452.39, 46579.73),
    2:  (0.938426, 44310.12,  680.01,     0.00, 80.31, 2265.12,    0.00,  48.90, -2394.33),
    12: (0.611187, 31246.12, 5757.88,     0.00, 121.01, 2218.99,   0.00,  38.86, -2378.86),
    13: (0.572308,     0.00,    0.00,     0.00,  0.00,    0.00, 1548.54,  22.06, -1570.60),
    24: (0.532497,     0.00,    0.00,     0.00,  0.00,    0.00, 1440.82,  25.86, -1466.68),
    40: (0.370668,     0.00,    0.00,     0.00,  0.00,    0.00, 1002.94,  26.07, -1029.01),
    66: (0.000285,     0.00,    0.00,     0.00,  0.00,    0.00,    0.77,   0.07,    -0.84),
}
EINMAL_TOTALS = {"premiums": 50000.00, "claims_death": 1151.58, "claims_lapse": 21350.16,
                 "claims_commutation": 0.00, "annuity_payments": 47525.47,
                 "expenses": 1936.55, "net_cf": -21963.77}
EINMAL_ROUNDED_NET_CF = -21963.79

# Variant B -- the 2,75 % legacy vintage, model point 6, an in-force cell whose frame opens at
# t = 21 and whose Rentenbeginn falls at t = 25.
# t: (pols_if, av, av_sur, premiums, int_credited, bonus_credited, claims_death,
#     claims_lapse, claims_commutation, annuity_payments, net_cf)
LEGACY = {
    21: (1.000000, 61190.90, 3200.00, 2592.00, 1747.81, 81.60, 262.93, 2047.65,     0.00,    0.00,    210.40),
    22: (0.965315, 63039.53, 3167.78, 2502.10, 1796.18, 80.78, 287.15, 2099.79,     0.00,    0.00,     45.25),
    23: (0.931471, 64758.71, 3134.66, 2414.37, 1841.04, 79.93, 312.98, 2147.90,     0.00,    0.00,   -115.28),
    24: (0.898434, 66348.31, 3100.58, 2328.74, 1882.41, 79.06, 340.53, 2191.96,     0.00,    0.00,   -271.38),
    25: (0.866171, 67807.93, 3065.46, 2245.12, 1920.26, 78.17, 369.88, 2231.94, 21974.56,    0.00, -22427.79),
    26: (0.584254,     0.00,    0.00,    0.00,    0.00,  0.00,   0.00,    0.00,     0.00, 2343.02,  -2372.27),
    50: (0.342195,     0.00,    0.00,    0.00,    0.00,  0.00,   0.00,    0.00,     0.00, 1372.29,  -1401.65),
    79: (0.000000,     0.00,    0.00,    0.00,    0.00,  0.00,   0.00,    0.00,     0.00,    0.00,     -0.00),
}
LEGACY_TOTALS = {"premiums": 12082.32, "int_credited": 9187.70, "bonus_credited": 399.55,
                 "claims_death": 1573.47, "claims_lapse": 10719.25,
                 "claims_commutation": 21974.56, "annuity_payments": 61580.87,
                 "expenses": 1471.45, "net_cf": -85237.27}

# What a single global 1,00 % Rechnungszins does to the legacy cell (pitfall 15).  The point is
# that it is a misallocation between the two accounts, not a hole in the total.
LEGACY_VINTAGE_PROBE = {
    "av_own": 82833.3752, "av_global": 76439.8722,
    "sur_own": 3629.3454, "sur_global": 9292.7587,
    "conv_own": 87759.6614, "conv_global": 87018.6203,
}

# The counterfactual of pitfall 1: crediting the declared rate *on top of* the guarantee.
DOUBLE_CREDIT = {"year_one": 56.8224, "correct_year_one": 40.8161,
                 "capital_gross": 63768.6926, "av_sur": 12698.2649}

CHECKS = ("check_net_cf", "check_pols_roll_fwd", "check_decrement_closure",
          "check_av_roll_fwd", "check_av_sur_roll_fwd", "check_prem_split",
          "check_cv_floor", "check_annuity_conv", "check_annuity_guarantee")

# --- The worked example
@pytest.mark.parametrize("t", sorted(WORKED_EXAMPLE))
def test_worked_example_row(de_rv_anchor, t):
    """Every cell of the notes' twenty-three-row table, to the displayed precision."""
    (pols_if, av, av_sur, prem, cd, cl, cc, ann, exp, net) = WORKED_EXAMPLE[t]
    p = de_rv_anchor
    assert p.pols_if(t) == pytest.approx(pols_if, abs=SIX_DP)
    assert p.av(t) == pytest.approx(av, abs=CENT)
    assert p.av_sur(t) == pytest.approx(av_sur, abs=CENT)
    assert p.premiums(t) == pytest.approx(prem, abs=CENT)
    assert p.claims(t, "DEATH") == pytest.approx(cd, abs=CENT)
    assert p.claims(t, "LAPSE") == pytest.approx(cl, abs=CENT)
    assert p.claims(t, "COMMUTATION") == pytest.approx(cc, abs=CENT)
    assert p.annuity_payments(t) == pytest.approx(ann, abs=CENT)
    assert p.expenses(t) == pytest.approx(exp, abs=CENT)
    assert p.net_cf(t) == pytest.approx(net, abs=CENT)
    assert p.liability_cf(t) == pytest.approx(-net, abs=CENT)


def test_the_worked_example_totals_are_summed_at_full_precision(de_rv_anchor):
    """The notes' Total row is a full-precision sum, then rounded -- not a sum of cells.

    The largest gap is ``annuity_payments``, 23 485,03 EUR against 23 484,99 EUR.
    """
    df = de_rv_anchor.result_cf()
    for column, total in TOTALS.items():
        assert df[column].sum() == pytest.approx(total, abs=CENT), column
    for column, total in ROUNDED_CELL_TOTALS.items():
        rounded = sum(round(v, 2) for v in df[column])
        assert rounded == pytest.approx(total, abs=CENT), column
    assert TOTALS["net_cf"] != ROUNDED_CELL_TOTALS["net_cf"]
    # Undiscounted, the cell collects 35 986,30 EUR and pays out 45 460,68 EUR.
    outgo = (df["claims_death"] + df["claims_lapse"] + df["claims_commutation"]
             + df["annuity_payments"] + df["expenses"]).sum()
    assert outgo == pytest.approx(45460.68, abs=CENT)
    assert df["premiums"].sum() - outgo == pytest.approx(TOTALS["net_cf"], abs=CENT)


def test_year_one_rebuilt_from_the_tariff_parameters(de_rv_anchor):
    """The notes' check 1: policy year 1 from the tariff parameters, reading no recursion.

    The acquisition charge takes 42,5 % of the year-one premium, and the Sec. 169(3) floor
    then stands 1 030,20 EUR **above** the tariff *Deckungskapital*.
    """
    p = de_rv_anchor
    assert p.beitragssumme_pp() == pytest.approx(17 * 3000.00, abs=CENT)
    assert p.beitragssumme_pp() == pytest.approx(YEAR_ONE["beitragssumme"], abs=CENT)
    assert p.alpha_total_pp() == pytest.approx(0.025 * p.beitragssumme_pp(), abs=CENT)
    assert p.alpha_total_pp() == pytest.approx(YEAR_ONE["alpha_total"], abs=CENT)
    assert p.charge_acq_pp(1) == pytest.approx(YEAR_ONE["alpha_total"], abs=CENT)
    assert p.charge_acq_pp(2) == 0.0                     # zillmered: all of it in year 1
    assert p.charge_prem_pp(1) == pytest.approx(YEAR_ONE["beta"], abs=CENT)
    assert p.charge_admin_pp(1) == YEAR_ONE["gamma"]     # the account is empty
    assert p.mort_rate_guar(1) == pytest.approx(YEAR_ONE["mort_rate_guar"], abs=5e-9)
    assert p.charge_risk_pp(1) == pytest.approx(YEAR_ONE["rho"], abs=5e-5)
    assert p.charge_due_pp(1) == pytest.approx(YEAR_ONE["charges_due"], abs=5e-5)
    assert p.charge_from_av_pp(1) == 0.0                 # the premium covers them all
    assert p.prem_to_av_pp(1) == pytest.approx(YEAR_ONE["prem_to_av"], abs=5e-5)
    assert p.int_credited_pp(1) == pytest.approx(YEAR_ONE["int_credited"], abs=5e-5)
    assert p.av_pp_at(1, "AFT_INT") == pytest.approx(YEAR_ONE["av_end"], abs=5e-5)
    assert p.pols_death(1) == pytest.approx(YEAR_ONE["deaths"], abs=5e-9)
    assert p.pols_lapse(1) == pytest.approx(YEAR_ONE["lapses"], abs=5e-9)
    assert p.claims(1, "DEATH") == pytest.approx(YEAR_ONE["claims_death"], abs=5e-5)
    assert p.spread_diff_pp_at(1, "AFT_INT") == pytest.approx(
        (0.0 + 1275.00 - 255.00) * 1.01, abs=5e-5)
    assert p.cv_tariff_pp(1) == pytest.approx(YEAR_ONE["cv_tariff"], abs=5e-5)
    assert p.cv_pp(1) == pytest.approx(YEAR_ONE["cv_floor"], abs=5e-5)   # the floor wins
    assert p.claims(1, "LAPSE") == pytest.approx(YEAR_ONE["claims_lapse"], abs=5e-5)
    assert p.expenses(1) == pytest.approx(400.00 + 45.00 + 120.00 * 0.06157405, abs=5e-5)
    assert p.net_cf(1) == pytest.approx(YEAR_ONE["net_cf"], abs=5e-5)


def test_the_two_credits_sum_to_the_declared_rate_to_ten_decimals(de_rv_anchor):
    """The notes' check 2: guarantee plus interest surplus **is** the declared rate.

    Both are struck on the same base, so the sum is the declared rate applied once.
    """
    p = de_rv_anchor
    base = p.av_pp_at(1, "AFT_PREM")
    guarantee, surplus = 0.0100 * base, 0.0155 * base
    assert guarantee == pytest.approx(16.0063170368, abs=5e-11)
    assert surplus == pytest.approx(24.8097914070, abs=5e-11)
    assert guarantee + surplus == pytest.approx(0.0255 * base, abs=5e-11)
    assert p.int_credited_pp(1) == pytest.approx(guarantee, rel=1e-12)
    assert p.bonus_credited_pp(1) == pytest.approx(surplus, rel=1e-12)


def test_the_rentenbeginn_rebuilt_from_the_two_balances(de_rv_anchor):
    """The notes' check 3, and the row-17 and row-18 figures it lands on."""
    p = de_rv_anchor
    assert p.av_pp_at(17, "AFT_INT") == pytest.approx(CONVERSION["av_pp"], abs=CENT)
    assert p.av_sur_pp_at(17, "AFT_INT") == pytest.approx(CONVERSION["av_sur_pp"], abs=CENT)
    assert p.capital_gross_pp() == pytest.approx(
        CONVERSION["av_pp"] + CONVERSION["av_sur_pp"], abs=CENT)
    assert p.val_reserve_pp() == pytest.approx(0.015 * p.capital_gross_pp(), rel=1e-12)
    assert p.val_reserve_pp() == pytest.approx(CONVERSION["val_reserve"], abs=CENT)
    assert p.capital_conv_pp() == pytest.approx(CONVERSION["capital_conv"], abs=CENT)
    assert p.annuity_rate_appl() == CONVERSION["rate_appl"]
    assert p.annuity_guar_mth_pp() == pytest.approx(
        p.capital_conv_pp() / 10000.0 * 32.00, rel=1e-12)
    assert p.annuity_guar_mth_pp() == pytest.approx(CONVERSION["annuity_guar_mth"], abs=5e-5)
    assert p.annuity_pp(18) == pytest.approx(CONVERSION["annuity_pp"], abs=CENT)
    assert p.pols_death(17) == pytest.approx(CONVERSION["pols_death_17"], abs=SIX_DP)
    assert p.pols_lapse(17) == pytest.approx(CONVERSION["pols_lapse_17"], abs=SIX_DP)
    assert p.pols_surv_rb() == pytest.approx(CONVERSION["pols_surv_rb"], abs=SIX_DP)
    assert p.pols_commutation(17) == pytest.approx(0.30 * p.pols_surv_rb(), rel=1e-12)
    assert p.pols_commutation(17) == pytest.approx(CONVERSION["commutations"], abs=SIX_DP)
    assert p.claims(17, "COMMUTATION") == pytest.approx(
        CONVERSION["claims_commutation"], abs=CENT)
    assert p.pols_annuitization(17) == pytest.approx(
        CONVERSION["annuitisations"], abs=SIX_DP)
    assert p.pols_annuitization(17) == pytest.approx(p.pols_if(18), rel=1e-12)
    assert p.annuity_payments(18) == pytest.approx(
        CONVERSION["annuity_payments_18"], abs=CENT)
    # Applying the guaranteed factor alone would give 167,0783 EUR, 87,5 % of the answer.
    assert p.capital_conv_pp() / 10000.0 * 28.00 == pytest.approx(167.0783, abs=5e-5)
    assert 28.00 / 32.00 == pytest.approx(0.875, rel=1e-12)


def test_the_decrements_close_and_the_account_rolls_forward(de_rv_anchor):
    """The notes' two closure identities, rebuilt here rather than read off a check.

    The 99,54 EUR released at ``t = 1`` is the end-of-year balance carried out by the
    0,061574 of a policy that died or surrendered.
    """
    p = de_rv_anchor
    n = p.proj_len()
    deaths = sum(p.pols_death(t) for t in range(1, n + 1))
    lapses = sum(p.pols_lapse(t) for t in range(1, n + 1))
    commut = sum(p.pols_commutation(t) for t in range(1, n + 1))
    assert deaths == pytest.approx(CLOSURE["deaths"], abs=SIX_DP)
    assert lapses == pytest.approx(CLOSURE["lapses"], abs=SIX_DP)
    assert commut == pytest.approx(CLOSURE["commutations"], abs=SIX_DP)
    assert p.pols_if(n + 1) == CLOSURE["survivors"] == 0.0
    assert deaths + lapses + commut == pytest.approx(p.pols_if_init(), abs=1e-12)

    assert p.av_release(1) == pytest.approx(99.5429, abs=5e-5)
    assert p.av_release(1) == pytest.approx(
        p.av_pp_at(1, "AFT_INT") * (p.pols_if(1) - p.pols_if(2)), rel=1e-12)
    assert (p.av(1) + p.prem_to_av(1) + p.int_credited(1) - p.av_release(1)) == (
        pytest.approx(p.av(2), abs=5e-5))
    assert p.av(2) == pytest.approx(1517.0951, abs=5e-5)
    # At t = n the whole balance is released: the annuitants convert and the commuters cash in.
    assert p.av_release(17) == pytest.approx(
        p.av_pp_at(17, "AFT_INT") * p.pols_if(17), rel=1e-12)


def test_the_rentengarantiezeit_costs_what_the_notes_say(de_rv_anchor):
    """At t = 27 the instalment is paid on 0,336143 policies, not the 0,311032 alive:
    862,65 EUR against 798,21 EUR, in each of the ten guaranteed years."""
    p = de_rv_anchor
    assert p.pols_annuity(27) == pytest.approx(0.336143, abs=SIX_DP)
    assert p.pols_if(27) == pytest.approx(0.311032, abs=SIX_DP)
    survivor_weighted = p.annuity_pp(27) * p.pols_if(27)
    assert survivor_weighted == pytest.approx(798.2097, abs=CENT)
    assert p.annuity_payments(27) - survivor_weighted == pytest.approx(64.44, abs=CENT)

# --- Variant A -- the Einmalbeitrag form (model point 2)
@pytest.mark.parametrize("t", sorted(EINMAL))
def test_einmalbeitrag_variant_row(klassische_rentenversicherung, t):
    """The notes' variant A table: a 55-year-old woman, one premium, twelve-year deferment."""
    (pols_if, av, av_sur, prem, cd, cl, ann, exp, net) = EINMAL[t]
    p = klassische_rentenversicherung.Projection[2]
    assert p.pols_if(t) == pytest.approx(pols_if, abs=SIX_DP)
    assert p.av(t) == pytest.approx(av, abs=CENT)
    assert p.av_sur(t) == pytest.approx(av_sur, abs=CENT)
    assert p.premiums(t) == pytest.approx(prem, abs=CENT)
    assert p.claims(t, "DEATH") == pytest.approx(cd, abs=CENT)
    assert p.claims(t, "LAPSE") == pytest.approx(cl, abs=CENT)
    assert p.annuity_payments(t) == pytest.approx(ann, abs=CENT)
    assert p.expenses(t) == pytest.approx(exp, abs=CENT)
    assert p.net_cf(t) == pytest.approx(net, abs=CENT)


def test_the_einmalbeitrag_variant_reads_as_the_notes_say(klassische_rentenversicherung):
    """The three things the notes read off variant A, and its totals: a year-one *Sparbeitrag*
    of 93,5 % of the premium against the anchor's 53,4 %, a net amount at risk that is
    identically zero, and a larger conversion capital than the anchor's."""
    p = klassische_rentenversicherung.Projection[2]
    df = p.result_cf()
    for column, total in EINMAL_TOTALS.items():
        assert df[column].sum() == pytest.approx(total, abs=CENT), column
    assert sum(round(v, 2) for v in df["net_cf"]) == pytest.approx(
        EINMAL_ROUNDED_NET_CF, abs=CENT)
    assert p.model_point()["premium_form"] == "einmal"
    assert p.prem_pp(1) == pytest.approx(50000.00, abs=CENT)
    assert all(p.prem_pp(t) == 0.0 for t in range(2, 13))
    assert p.beitragssumme_pp() == pytest.approx(50000.00, abs=CENT)
    assert p.alpha_total_pp() == pytest.approx(1250.00, abs=CENT)
    assert p.prem_to_av_pp(1) == pytest.approx(46750.00, abs=CENT)
    assert p.prem_to_av_pp(1) / 50000.00 == pytest.approx(0.935, abs=0.0005)
    assert all(p.nar_pp(t) == 0.0 and p.charge_risk_pp(t) == 0.0 for t in range(1, 13))
    assert p.capital_conv_pp() == pytest.approx(62913.28, abs=CENT)
    assert p.annuity_guar_mth_pp() == pytest.approx(201.32, abs=CENT)
    assert p.capital_conv_pp() > CONVERSION["capital_conv"]
    assert float(p.model_point()["kapitalwahl_rate"]) == 0.0

# --- Variant B -- the 2,75 % legacy vintage (model point 6)
@pytest.mark.parametrize("t", sorted(LEGACY))
def test_legacy_vintage_variant_row(klassische_rentenversicherung, t):
    """The notes' variant B table, including the two crediting columns whose ratio is the point."""
    (pols_if, av, av_sur, prem, interest, bonus, cd, cl, cc, ann, net) = LEGACY[t]
    p = klassische_rentenversicherung.Projection[6]
    assert p.pols_if(t) == pytest.approx(pols_if, abs=SIX_DP)
    assert p.av(t) == pytest.approx(av, abs=CENT)
    assert p.av_sur(t) == pytest.approx(av_sur, abs=CENT)
    assert p.premiums(t) == pytest.approx(prem, abs=CENT)
    assert p.int_credited(t) == pytest.approx(interest, abs=CENT)
    assert p.bonus_credited(t) == pytest.approx(bonus, abs=CENT)
    assert p.claims(t, "DEATH") == pytest.approx(cd, abs=CENT)
    assert p.claims(t, "LAPSE") == pytest.approx(cl, abs=CENT)
    assert p.claims(t, "COMMUTATION") == pytest.approx(cc, abs=CENT)
    assert p.annuity_payments(t) == pytest.approx(ann, abs=CENT)
    assert p.net_cf(t) == pytest.approx(net, abs=CENT)


def test_the_legacy_vintage_variant_reads_as_the_notes_say(klassische_rentenversicherung):
    """Variant B's totals and its three legacy asymmetries: every euro of the 399,55 EUR of
    surplus is the declared rate on the *Ansammlungsguthaben*'s own balance, because
    ``bonus_rate`` is zero at every ``t``; the 2005 *Rentenfaktor* beats the current one; and
    the 40 permille charge set carries no *Stornoabzug*."""
    p = klassische_rentenversicherung.Projection[6]
    df = p.result_cf()
    for column, total in LEGACY_TOTALS.items():
        assert df[column].sum() == pytest.approx(total, abs=CENT), column
    assert df.index[0] == 21 and int(p.model_point()["duration_init"]) == 20
    assert p.int_rate_guar() == 0.0275
    assert all(p.decl_rate(t) == 0.0255 and p.bonus_rate(t) == 0.0 for t in range(21, 26))
    assert all(p.bonus_credited_pp(t) == pytest.approx(
        0.0255 * p.av_sur_pp(t), rel=1e-12) for t in range(21, 26))
    assert df["int_credited"].sum() > 20 * df["bonus_credited"].sum()
    assert p.annuity_rate_guar() == 34.00 and p.annuity_rate_curr() == 32.00
    assert p.annuity_rate_appl() == 34.00                       # the guarantee wins
    assert p.capital_conv_pp() == pytest.approx(87759.66, abs=CENT)
    assert p.model_point()["charge_id"] == "zillmer_40"
    assert p.surr_charge_pp(21) == 0.0
    assert p.cv_pp(21) == pytest.approx(68586.25, abs=CENT) == p.cv_tariff_pp(21)
    assert p.cv_floor_pp(21) == pytest.approx(65304.65, abs=CENT)
    assert p.cv_floor_pp(21) < p.cv_tariff_pp(21)               # inoperative twenty years in
    assert p.alpha_total_pp() == pytest.approx(0.040 * 64800.00, abs=CENT)


# --- Pitfall 1: adding the declared rate on top of the guarantee
def test_pitfall_1_the_declared_rate_is_not_added_on_top_of_the_guarantee(
        klassische_rentenversicherung, de_rv_anchor):
    """``bonus_rate = max(0, decl_rate - int_rate_guar)``, on the same base as the guarantee.

    The counterfactual is rebuilt rather than asserted from prose: crediting the whole declared
    rate as a *surplus* reaches 63 768,69 EUR at the *Rentenbeginn* against 58 788,98 EUR.
    """
    p = de_rv_anchor
    for t in (1, 5, 12, 17):
        base = p.av_pp_at(t, "AFT_PREM")
        assert p.bonus_rate(t) == pytest.approx(0.0255 - 0.0100, abs=1e-12)
        assert p.int_credited_pp(t) + p.bonus_rate(t) * base == pytest.approx(
            p.decl_rate(t) * base, rel=1e-12)
    wrong = 0.0                       # the double-credited Ansammlungsguthaben, year by year
    for t in range(1, 18):
        d = p.decl_rate(t)
        wrong = wrong + d * p.av_pp_at(t, "AFT_PREM") + d * wrong
    assert wrong == pytest.approx(DOUBLE_CREDIT["av_sur"], abs=CENT)
    assert p.av_pp_at(17, "AFT_INT") + wrong == pytest.approx(
        DOUBLE_CREDIT["capital_gross"], abs=CENT)
    assert (p.av_pp_at(17, "AFT_INT") + wrong) / p.capital_gross_pp() - 1 == (
        pytest.approx(0.085, abs=0.0005))
    assert 0.0355 * p.av_pp_at(1, "AFT_PREM") == pytest.approx(
        DOUBLE_CREDIT["year_one"], abs=5e-5)
    assert p.int_credited_pp(1) + p.bonus_credited_pp(1) == pytest.approx(
        DOUBLE_CREDIT["correct_year_one"], abs=5e-5)
    # The mirror image: a vintage above the declaration receives no interest surplus at all.
    legacy = klassische_rentenversicherung.Projection[6]
    assert all(legacy.bonus_rate(t) == 0.0 and legacy.int_credited_pp(t) > 0.0
               for t in range(21, 26))


# --- Pitfall 2: getting the within-year order wrong
def test_pitfall_2_the_within_year_order_is_premium_then_charges_then_interest(de_rv_anchor):
    """Interest is credited on the post-premium, post-charge balance and on nothing else.

    Crediting it on the opening balance alone would change year-one interest by the whole of
    ``i x (S(1) - C(1))``, 16,01 EUR of a 1 616,64 EUR closing balance.
    """
    p = de_rv_anchor
    for t in (1, 2, 9, 17):
        assert p.av_pp_at(t, "BEF_PREM") == p.av_pp(t)
        assert p.av_pp_at(t, "AFT_PREM") == pytest.approx(
            p.av_pp(t) + p.prem_to_av_pp(t) - p.charge_from_av_pp(t), rel=1e-12)
        assert p.int_credited_pp(t) == pytest.approx(
            p.int_rate_guar() * p.av_pp_at(t, "AFT_PREM"), rel=1e-12)
        assert p.av_pp_at(t, "AFT_INT") == pytest.approx(
            p.av_pp_at(t, "AFT_PREM") + p.int_credited_pp(t), rel=1e-12)
    opening_only = p.av_pp(1) * (1 + p.int_rate_guar()) + p.prem_to_av_pp(1)
    assert p.av_pp_at(1, "AFT_INT") - opening_only == pytest.approx(
        p.int_rate_guar() * (p.prem_to_av_pp(1) - p.charge_from_av_pp(1)), rel=1e-12)
    assert p.av_pp_at(1, "AFT_INT") - opening_only == pytest.approx(16.0063, abs=5e-5)
    assert (p.av_pp(2) + p.prem_pp(2)) * 1.01 > p.av_pp_at(2, "AFT_INT")
    # The two charges struck on start-of-year balances, without which it would be circular.
    assert p.charge_admin_pp(2) == pytest.approx(0.0020 * p.av_pp(2), rel=1e-12)
    assert p.charge_risk_pp(2) == pytest.approx(p.mort_rate_guar(2) * p.nar_pp(2), rel=1e-12)
    assert p.nar_pp(2) == pytest.approx(max(0.0, p.db_base_pp(2) - p.av_pp(2)), rel=1e-12)


# --- Pitfall 3: applying only the guaranteed Rentenfaktor
def test_pitfall_3_the_applied_rentenfaktor_is_the_higher_of_two(
        klassische_rentenversicherung, de_rv_anchor):
    """``max(garantierter, aktueller)``, with both branches shipped and both exercised."""
    p = de_rv_anchor
    assert (p.annuity_rate_guar(), p.annuity_rate_curr(), p.annuity_rate_appl()) == (
        28.00, 32.00, 32.00)                                    # the current factor wins
    # Point 13: the guarantee binds over a `low` scenario, and guar_capital_pp binds with it.
    guar = klassische_rentenversicherung.Projection[13]
    assert guar.model_point()["rf_scenario_id"] == "low"
    assert (guar.annuity_rate_guar(), guar.annuity_rate_curr(),
            guar.annuity_rate_appl()) == (27.00, 24.27, 27.00)  # the guarantee wins
    assert guar.capital_gross_pp() == pytest.approx(50930.99, abs=CENT)
    assert guar.capital_conv_pp() == 60000.00                   # the contract-value floor
    assert guar.annuity_guar_mth_pp() == pytest.approx(60000.0 / 10000.0 * 27.00, rel=1e-12)
    for point_id in (1, 2, 5, 6, 9, 13, 14):
        q = klassische_rentenversicherung.Projection[point_id]
        assert q.annuity_rate_appl() >= q.annuity_rate_guar()
        assert q.check_annuity_conv() is True


# --- Pitfall 4: weighting the guaranteed annuity by survivors
def test_pitfall_4_the_guaranteed_annuity_is_not_weighted_by_survivors(
        klassische_rentenversicherung, de_rv_anchor):
    """Inside the *Rentengarantiezeit* the instalment is due whether the annuitant lives or not."""
    p = de_rv_anchor
    n, m = 17, 10
    assert int(p.model_point()["rgz_years"]) == m
    assert all(p.pols_annuity(t) == pytest.approx(p.pols_annuitization(n), rel=1e-12)
               for t in range(n + 1, n + m + 1))
    assert all(p.pols_annuity(t) == pytest.approx(p.pols_if(t), rel=1e-12)
               for t in (n + m + 1, n + m + 5, 55))
    assert all(p.pols_annuity(t) == 0.0 for t in range(1, n + 1))
    assert p.pols_annuity(18) == pytest.approx(p.pols_if(18), rel=1e-12)
    assert p.pols_annuity(27) > p.pols_if(27)
    assert p.check_annuity_guarantee() is True
    # Point 10 carries a twenty-year window; point 9 carries none at all.
    long_rgz = klassische_rentenversicherung.Projection[10]
    n10 = int(long_rgz.model_point()["aufschub_y"])
    assert int(long_rgz.model_point()["rgz_years"]) == 20
    assert long_rgz.pols_annuity(n10 + 20) == pytest.approx(
        long_rgz.pols_annuitization(n10), rel=1e-12)
    assert long_rgz.pols_annuity(n10 + 21) == pytest.approx(
        long_rgz.pols_if(n10 + 21), rel=1e-12)
    none_rgz = klassische_rentenversicherung.Projection[9]
    n9 = int(none_rgz.model_point()["aufschub_y"])
    assert int(none_rgz.model_point()["rgz_years"]) == 0
    assert all(none_rgz.pols_annuity(t) == pytest.approx(none_rgz.pols_if(t), rel=1e-12)
               for t in range(n9 + 1, n9 + 6))
    assert long_rgz.check_annuity_guarantee() is none_rgz.check_annuity_guarantee() is True


# --- Pitfall 5: treating Beitragsfreistellung as a lapse
def test_pitfall_5_beitragsfreistellung_is_not_a_lapse(klassische_rentenversicherung):
    """The conversion moves no policy; the contract keeps its vintage and its factor.

    Surrender does **not** cease -- a *beitragsfrei* contract keeps its Sec. 168 VVG
    *Kündigung* right -- and only the Sec. 165 cash-out branch empties a cohort in one year.
    """
    p = klassische_rentenversicherung.Projection[7]
    pup = int(p.model_point()["pup_year"])
    assert pup == 10 and p.pup_cashout() is False
    assert p.paid_up(pup) is True and p.paid_up(pup - 1) is False
    assert p.prem_pp(pup - 1) == pytest.approx(3600.00, abs=CENT)
    assert all(p.prem_pp(t) == 0.0 for t in (pup, pup + 1, pup + 5))
    assert p.int_rate_guar() == 0.0100 and p.annuity_rate_guar() == 28.00   # both unchanged
    # The conversion itself moves nobody: the year-9 exit is the ordinary table rate.
    assert p.lapse_rate(pup - 1) == 0.035
    assert p.pols_lapse(pup - 1) == pytest.approx(
        p.pols_if_at(pup - 1, "BEF_LAPSE") * 0.035, rel=1e-12)
    assert p.pols_if(pup) == pytest.approx(0.668738, abs=SIX_DP)
    # The reset is real money, and it is credited in the transition year.
    assert p.av_pp_at(pup - 1, "AFT_INT") == pytest.approx(30261.4467, abs=CENT)
    assert p.pup_value_pp() == pytest.approx(30303.9053, abs=CENT)
    assert p.av_pp(pup) == pytest.approx(p.pup_value_pp(), rel=1e-12)
    assert p.pup_uplift(pup - 1) == pytest.approx(28.3937, abs=CENT)
    assert p.pup_uplift(pup) == 0.0
    assert p.spread_diff_pp(pup) == 0.0                       # the two accounts have merged
    # Surrender continues after the election, and the admin charge steps up.
    assert p.claims(pup, "LAPSE") == pytest.approx(764.1229, abs=CENT)
    assert p.charge_admin_pp(pup - 1) == pytest.approx(0.0020 * p.av_pp(pup - 1), rel=1e-12)
    assert p.charge_admin_pp(pup) == pytest.approx(0.0030 * p.av_pp(pup), rel=1e-12)
    assert p.charge_from_av_pp(pup) == pytest.approx(p.charge_due_pp(pup), rel=1e-12)
    assert p.check_av_roll_fwd() is p.check_pols_roll_fwd() is True
    # Point 8 is the other statutory branch: below the Mindestversicherungsleistung the
    # contract is cashed out instead of made paid-up, and the whole cohort leaves at once.
    cash = klassische_rentenversicherung.Projection[8]
    assert cash.pup_cashout() is True
    assert cash.pup_value_pp() / 10000.0 * cash.annuity_rate_guar() == pytest.approx(
        5.4518, abs=5e-5)
    assert cash.lapse_rate(2) == 1.0
    assert cash.claims(2, "LAPSE") == pytest.approx(1828.4915, abs=CENT)
    assert cash.pols_if(3) == 0.0
    assert cash.result_cf().loc[3:].abs().sum().sum() == 0.0


# --- Pitfall 6: booking the Kostenbeitrag as an expense
def test_pitfall_6_the_kostenbeitrag_is_not_an_expense(de_rv_anchor, tmp_path):
    """``expenses`` is invariant to ``beta_rate`` and ``gamma_rate``; ``av_pp(t+1)`` is not."""
    import pandas as pd

    p = de_rv_anchor
    assert p.expenses(1) == pytest.approx(452.3889, abs=5e-5)
    assert p.charge_due_pp(1) * p.pols_if(1) == pytest.approx(1399.3683, abs=5e-5)
    assert p.expenses(1) != pytest.approx(p.charge_due_pp(1) * p.pols_if(1), abs=CENT)
    assert p.net_cf(1) == pytest.approx(
        p.premiums(1) - p.claims(1) - p.annuity_payments(1) - p.expenses(1), rel=1e-12)

    charges = pd.read_csv(INPUT_DIR / "charge_table.csv")
    is_25 = charges["charge_id"] == "zillmer_25"
    charges.loc[is_25 & (charges["item"] == "beta_rate"), "value"] = 0.08
    charges.loc[is_25 & (charges["item"] == "gamma_rate"), "value"] = 0.004
    alt = tmp_path / "charge_table_doubled.csv"
    charges.to_csv(alt, index=False)

    model = mx.read_model(MODEL_DIR, name="RV_DE_A_charges")
    try:
        model.Data.charge_file = str(alt)
        model.Data.clear_all()
        model.Projection.clear_all()
        q = model.Projection[1]
        assert q.charge_prem_pp(1) == pytest.approx(0.08 * 3000.00, abs=CENT)
        assert all(q.expenses(t) == pytest.approx(p.expenses(t), rel=1e-12)
                   for t in (1, 5, 17))
        assert p.av_pp(2) - q.av_pp(2) == pytest.approx(0.04 * 3000.00 * 1.01, abs=CENT)
    finally:
        model.close()


# --- Pitfall 7: computing the surrender value off the zillmered reserve
def test_pitfall_7_the_surrender_value_is_floored_at_the_spread_reserve(de_rv_anchor):
    """The Sec. 169(3) floor binds through t = 4 and stops at t = 5, so both branches of
    ``max(cv_tariff_pp, cv_floor_pp)`` are exercised on the anchor cell alone."""
    p = de_rv_anchor
    for t in range(1, 18):
        assert p.cv_pp(t) == pytest.approx(
            max(p.cv_tariff_pp(t), p.cv_floor_pp(t)), rel=1e-12)
        assert p.cv_floor_pp(t) == pytest.approx(
            p.av_pp_at(t, "AFT_INT") + p.spread_diff_pp_at(t, "AFT_INT"), rel=1e-12)
    assert all(p.cv_floor_pp(t) > p.cv_tariff_pp(t) for t in range(1, 5))
    assert all(p.cv_floor_pp(t) < p.cv_tariff_pp(t) for t in range(5, 18))
    assert p.cv_pp(4) == pytest.approx(10709.9704, abs=CENT)
    assert p.cv_pp(5) == pytest.approx(13724.8830, abs=CENT)
    assert all(p.charge_acq_spread_pp(t) == pytest.approx(1275.00 / 5, abs=CENT)
               for t in range(1, 6))
    assert p.charge_acq_spread_pp(6) == 0.0
    assert p.spread_diff_pp_at(2, "AFT_INT") == pytest.approx(
        (p.spread_diff_pp(2) + p.charge_acq_pp(2) - p.charge_acq_spread_pp(2)) * 1.01,
        rel=1e-12)
    assert p.spread_diff_pp_at(2, "AFT_INT") == pytest.approx(782.952, abs=CENT)
    assert p.spread_diff_pp_at(17, "AFT_INT") > 0.0        # it never returns to zero
    # Omitting the floor would cut the year-2 surrender claim by the whole of the gap.
    without_floor = p.cv_tariff_pp(2) * p.pols_lapse(2)
    assert without_floor == pytest.approx(212.3528, abs=CENT)
    assert p.claims(2, "LAPSE") - without_floor == pytest.approx(
        (p.cv_floor_pp(2) - p.cv_tariff_pp(2)) * p.pols_lapse(2), rel=1e-9)
    assert p.check_cv_floor() is True


# --- Pitfall 8: letting the Stornoabzug recover acquisition costs
def test_pitfall_8_the_stornoabzug_cannot_recover_acquisition_costs(de_rv_anchor, tmp_path):
    """A flat percentage of the pre-deduction value with no duration term, and never below the
    floor however large it is set: a deduction unwinding over the first years would be exactly
    the kind Sec. 169(5) VVG voids."""
    import pandas as pd

    p = de_rv_anchor
    for t in (1, 5, 12, 17):
        assert p.surr_charge_pp(t) == pytest.approx(
            0.020 * (p.av_pp_at(t, "AFT_INT") + p.av_sur_pp_at(t, "AFT_INT")), rel=1e-12)
        assert p.cv_tariff_pp(t) == pytest.approx(
            (p.av_pp_at(t, "AFT_INT") + p.av_sur_pp_at(t, "AFT_INT")) * 0.98, rel=1e-12)
    ratios = {round(p.surr_charge_pp(t)
                    / (p.av_pp_at(t, "AFT_INT") + p.av_sur_pp_at(t, "AFT_INT")), 12)
              for t in range(2, 18)}
    assert ratios == {0.02}                       # flat in t: no duration term anywhere

    charges = pd.read_csv(INPUT_DIR / "charge_table.csv")
    is_25 = charges["charge_id"] == "zillmer_25"
    charges.loc[is_25 & (charges["item"] == "stornoabzug_rate"), "value"] = 0.50
    alt = tmp_path / "charge_table_storno.csv"
    charges.to_csv(alt, index=False)

    model = mx.read_model(MODEL_DIR, name="RV_DE_A_storno")
    try:
        model.Data.charge_file = str(alt)
        model.Data.clear_all()
        model.Projection.clear_all()
        q = model.Projection[1]
        assert q.cv_tariff_pp(10) < q.cv_floor_pp(10)
        assert all(q.cv_pp(t) == pytest.approx(q.cv_floor_pp(t), rel=1e-12)
                   for t in range(1, 18))
        assert q.check_cv_floor() is True
    finally:
        model.close()


# --- Pitfall 9: using one mortality basis where the product uses two
def test_pitfall_9_the_product_uses_two_mortality_bases(de_rv_anchor):
    """First order fixes the risk charge and the guarantees; second order drives the projection.

    ``mort_be_factor`` is **above one** on purpose: for an annuity, prudence is lower mortality.
    """
    p = de_rv_anchor
    assert p.mort_be_factor() == 1.15 > 1.0
    for t in (1, 8, 17, 40):
        assert p.mort_rate(t) == pytest.approx(
            min(1.0, p.mort_rate_guar(t) * 1.15), rel=1e-12)
        assert p.mort_rate(t) > p.mort_rate_guar(t)
    for t in (1, 9, 17):
        assert p.charge_risk_pp(t) == pytest.approx(
            p.mort_rate_guar(t) * p.nar_pp(t), rel=1e-12)         # first order
        assert p.charge_risk_pp(t) != pytest.approx(p.mort_rate(t) * p.nar_pp(t), rel=1e-6)
        assert p.pols_death(t) == pytest.approx(
            p.pols_if(t) * p.mort_rate(t), rel=1e-12)             # second order
    assert p.claims(1, "DEATH") / (3000.00 * p.pols_if(1) * p.mort_rate_guar(1)) == (
        pytest.approx(1.15, rel=1e-12))
    assert p.omega_age() == 121 and p.age(71) == 120
    assert p.mort_rate_guar(71) == p.mort_rate(71) == 1.0         # capped at the terminal age


# --- Pitfall 10: using a period mortality table
def test_pitfall_10_the_mortality_surface_is_generational_not_period(de_rv_anchor):
    """``mort_rate_guar`` depends on ``calendar_year(t)`` as well as ``age(t)``.

    The anchor's annuitant reaches 67 in 2043, so the rate is strictly below the same age's
    rate for a life reaching 67 in 2026, by the seventeen further improvement years.
    """
    p = de_rv_anchor
    assert p.age(18) == 67 and p.calendar_year(18) == 2043
    q_base, improve = p.mort_rate_at_age(67), p.improve_rate(67)
    at_2043, at_2026 = p.mort_rate_guar(18), q_base * (1 - improve) ** (2026 - 2005)
    assert at_2043 == pytest.approx(q_base * (1 - improve) ** (2043 - 2005), rel=1e-12)
    assert at_2043 < at_2026
    assert at_2043 / at_2026 == pytest.approx((1 - improve) ** 17, rel=1e-12)
    assert at_2043 == pytest.approx(0.00521377, abs=5e-9)
    assert p.mort_rate_at_age(50) == 0.002000            # the anchor a substitute must keep
    assert p.mort_rate_at_age(51) / p.mort_rate_at_age(50) == pytest.approx(1.09, rel=1e-6)
    assert p.calendar_year(1) == 2026 and p.age(1) == 50
    assert p.mort_rate_guar(1) < p.mort_rate_at_age(50)
    assert p.mort_rate_guar(40) < p.mort_rate_at_age(p.age(40))


# --- Pitfall 11: charging the risk premium on a zero net amount at risk
def test_pitfall_11_no_risk_premium_on_a_zero_net_amount_at_risk(
        klassische_rentenversicherung, de_rv_anchor):
    """With ``death_benefit_form = deckungskapital`` the benefit **is** the reserve.

    On the anchor the amount at risk **rises** to 4 587,95 EUR at ``t = 6`` and ends the
    deferment at 3 204,24 EUR rather than at zero, because the *Deckungskapital* never
    overtakes the premiums paid: *Beitragsrückgewähr* is real cover here, not a formality.
    """
    p = de_rv_anchor
    assert p.model_point()["death_benefit_form"] == "prem_refund"
    assert all(p.charge_risk_pp(t) > 0.0 for t in range(1, 18))
    assert p.nar_pp(6) == pytest.approx(4587.95, abs=CENT)
    assert p.nar_pp(6) == max(p.nar_pp(t) for t in range(1, 18))
    assert p.nar_pp(17) == pytest.approx(3204.24, abs=CENT) and p.nar_pp(17) > 0.0
    assert p.charge_risk_pp(1) == pytest.approx(4.37, abs=CENT)
    assert p.charge_risk_pp(17) == pytest.approx(15.39, abs=CENT)
    assert all(p.charge_risk_pp(t + 1) > p.charge_risk_pp(t) for t in range(1, 17))
    assert p.db_base_pp(2) == pytest.approx(6000.00, abs=CENT)     # the premiums paid
    for point_id, last in ((2, 12), (12, 22)):
        q = klassische_rentenversicherung.Projection[point_id]
        assert q.model_point()["death_benefit_form"] == "deckungskapital"
        assert all(q.nar_pp(t) == 0.0 and q.charge_risk_pp(t) == 0.0
                   and q.db_base_pp(t) == q.av_pp(t) for t in range(1, last + 1))
    assert all(p.charge_risk_pp(t) == 0.0 for t in (18, 30, 71))   # none after Rentenbeginn


# --- Pitfall 12: deducting the payout-phase administration charge from the annuity
def test_pitfall_12_the_payout_administration_charge_is_not_deducted(de_rv_anchor):
    """``annuity_admin_rate`` ships at 1,5 % and is never applied: the *Rentenfaktor* already
    carries the tariff's payout loading, so deducting again would charge it twice.

    Payout-phase ``expenses`` are the inflated ``expense_annuity_pp`` on the exposed count plus
    the settlement cost of that year's deaths, and nothing else.
    """
    import pandas as pd

    charges = pd.read_csv(INPUT_DIR / "charge_table.csv")
    recorded = charges[(charges["charge_id"] == "zillmer_25")
                       & (charges["item"] == "annuity_admin_rate")]
    assert float(recorded["value"].iloc[0]) == 0.015
    assert "NOT applied" in recorded["provenance"].iloc[0]

    p = de_rv_anchor
    for t in (18, 27, 28, 40):
        assert p.annuity_payments(t) == pytest.approx(
            12.0 * (p.annuity_guar_mth_pp() + p.annuity_sur_mth_pp(t)) * p.pols_annuity(t),
            rel=1e-12)
        assert p.annuity_payments(t) != pytest.approx(
            0.985 * p.annuity_pp(t) * p.pols_annuity(t), rel=1e-9)
        assert p.expenses(t) == pytest.approx(
            p.expenses_pp(t) * p.pols_annuity(t) + 120.0 * p.pols_death(t), rel=1e-12)
    assert p.expenses_pp(18) == pytest.approx(30.0 * 1.02 ** 17, rel=1e-12)
    assert p.expenses(18) == pytest.approx(14.1205 + 0.2419, abs=CENT)
    # The konstant system: the Ueberschussrente is level at 12 % of the garantierte Rente.
    assert p.model_point()["payout_system"] == "konstant"
    assert p.annuity_sur_mth_pp(18) == pytest.approx(
        0.12 * p.annuity_guar_mth_pp(), rel=1e-12)
    assert all(p.annuity_sur_mth_pp(t) == pytest.approx(p.annuity_sur_mth_pp(18), rel=1e-12)
               for t in (27, 40, 60))


# --- Pitfall 13: paying a death benefit after the Rentenbeginn
def test_pitfall_13_no_death_benefit_after_the_rentenbeginn(klassische_rentenversicherung):
    """*Beitragsrückgewähr in der Rentenbezugsphase* was established by no source, so it is not
    asserted: ``claims_death(t) = 0`` for every ``t > n``, on every model point.  Deaths still
    happen there and carry a settlement expense; they simply pay nothing."""
    for point_id in (1, 2, 3, 5, 6, 12, 13, 14):
        p = klassische_rentenversicherung.Projection[point_id]
        n = int(p.model_point()["aufschub_y"])
        assert p.result_cf().loc[n + 1:, "claims_death"].sum() == 0.0, point_id
        assert all(p.db_pp(t) == 0.0 for t in (n + 1, n + 5)), point_id
        assert p.pols_death(n + 1) > 0.0, point_id      # the decrement is real
        assert p.pols_if(n + 2) < p.pols_if(n + 1), point_id
    names = set(klassische_rentenversicherung.Projection.cells) | set(
        klassische_rentenversicherung.Projection.refs)
    for absent in ("db_annuity_pp", "prem_refund_annuity_pp", "claims_survivor",
                   "pols_survivor", "hinterbliebenenrente_pp"):
        assert absent not in names, absent


# --- Pitfall 14: letting the Kapitalwahlrecht leave the account behind
def test_pitfall_14_the_kapitalwahlrecht_leaves_no_account_behind(
        klassische_rentenversicherung, de_rv_anchor):
    """Commuters receive ``capital_conv_pp``, the same capital the annuitants convert."""
    p = de_rv_anchor
    n = 17
    assert float(p.model_point()["kapitalwahl_rate"]) == 0.30
    assert p.claims(n, "COMMUTATION") == pytest.approx(
        p.capital_conv_pp() * 0.30 * p.pols_surv_rb(), rel=1e-12)
    assert all(p.claims(t, "COMMUTATION") == 0.0
               for t in list(range(1, n)) + list(range(n + 1, 72)))
    assert p.pols_commutation(n) + p.pols_annuitization(n) == pytest.approx(
        p.pols_surv_rb(), rel=1e-12)
    assert all(p.av_pp(t) == 0.0 and p.av_sur_pp(t) == 0.0 for t in (18, 30, 71))
    # Point 9 commutes the whole surviving cohort: nothing survives the Rentenbeginn.
    full = klassische_rentenversicherung.Projection[9]
    n9 = int(full.model_point()["aufschub_y"])
    assert float(full.model_point()["kapitalwahl_rate"]) == 1.0
    assert full.pols_annuitization(n9) == 0.0
    assert full.pols_commutation(n9) == pytest.approx(full.pols_surv_rb(), rel=1e-12)
    assert full.claims(n9, "COMMUTATION") == pytest.approx(30882.0276, abs=CENT)
    assert full.capital_conv_pp() == pytest.approx(43630.1733, abs=CENT)
    assert full.pols_if(n9 + 1) == 0.0
    assert full.result_cf().loc[n9 + 1:].abs().sum().sum() == 0.0
    assert full.check_decrement_closure() is True


# --- Pitfall 15: forgetting that the guarantee vintage is a model-point attribute
def test_pitfall_15_the_guarantee_vintage_is_a_model_point_attribute(
        klassische_rentenversicherung, tmp_path):
    """Three vintages credit three rates in one run, from the same tables.

    A single global rate makes a **misallocation between the two accounts** rather than a hole
    in the total: point 6's *Deckungskapital* at *Rentenbeginn* falls 7,7 % while its
    *Ansammlungsguthaben* rises 156 % and the conversion capital moves 0,8 %.
    """
    import pandas as pd

    rates = {point_id: klassische_rentenversicherung.Projection[point_id].int_rate_guar()
             for point_id in (1, 6, 14)}
    assert rates == {1: 0.0100, 6: 0.0275, 14: 0.0090}
    legacy = klassische_rentenversicherung.Projection[6]
    assert legacy.av_pp_at(25, "AFT_INT") == pytest.approx(
        LEGACY_VINTAGE_PROBE["av_own"], abs=CENT)
    assert legacy.av_sur_pp_at(25, "AFT_INT") == pytest.approx(
        LEGACY_VINTAGE_PROBE["sur_own"], abs=CENT)
    assert legacy.capital_conv_pp() == pytest.approx(
        LEGACY_VINTAGE_PROBE["conv_own"], abs=CENT)

    points = pd.read_csv(INPUT_DIR / "model_point_table.csv", index_col="point_id")
    points.loc[6, "int_rate_guar"] = 0.0100
    alt = tmp_path / "model_point_table_one_rate.csv"
    points.to_csv(alt)

    model = mx.read_model(MODEL_DIR, name="RV_DE_A_one_rate")
    try:
        model.Data.model_point_file = str(alt)
        model.Data.clear_all()
        model.Projection.clear_all()
        q = model.Projection[6]
        assert q.int_rate_guar() == 0.0100
        assert q.av_pp_at(25, "AFT_INT") == pytest.approx(
            LEGACY_VINTAGE_PROBE["av_global"], abs=CENT)
        assert q.av_sur_pp_at(25, "AFT_INT") == pytest.approx(
            LEGACY_VINTAGE_PROBE["sur_global"], abs=CENT)
        assert q.capital_conv_pp() == pytest.approx(
            LEGACY_VINTAGE_PROBE["conv_global"], abs=CENT)
        assert q.av_pp_at(25, "AFT_INT") / legacy.av_pp_at(25, "AFT_INT") - 1 == (
            pytest.approx(-0.077, abs=0.001))
        assert q.av_sur_pp_at(25, "AFT_INT") / legacy.av_sur_pp_at(25, "AFT_INT") - 1 == (
            pytest.approx(1.560, abs=0.005))
        assert q.capital_conv_pp() / legacy.capital_conv_pp() - 1 == pytest.approx(
            -0.008, abs=0.001)
        assert q.bonus_rate(21) == pytest.approx(0.0155, abs=1e-12)   # and now it is positive
    finally:
        model.close()


# --- Pitfall 16: letting sex reach the tariff
def test_pitfall_16_sex_never_reaches_the_tariff(klassische_rentenversicherung, tmp_path):
    """Unisex has been compulsory since 21 December 2012: ``sex`` reaches the mortality basis
    and nothing else.  The probe is the anchor cell as a woman, so the premium, the charges
    other than the *Risikobeitrag*, and the applied *Rentenfaktor* must all be identical."""
    import pandas as pd

    data = klassische_rentenversicherung.Data
    assert list(data.mort_table().index.names) == ["sex", "age"]
    for table in (data.rentenfaktor_table(), data.charge_table(), data.decl_rate_table()):
        assert "sex" not in (table.index.names or []) and "sex" not in table.columns
    assert "sex" not in data.lapse_table().columns
    assert "sex" not in data.freq_load_table().columns

    points = pd.read_csv(INPUT_DIR / "model_point_table.csv", index_col="point_id")
    twin = points.loc[1].copy()
    twin["sex"], twin["policy_id"] = "F", "DE-RV-0001F"
    points.loc[99] = twin
    alt = tmp_path / "model_point_table_unisex.csv"
    points.to_csv(alt)

    model = mx.read_model(MODEL_DIR, name="RV_DE_A_unisex")
    try:
        model.Data.model_point_file = str(alt)
        model.Data.clear_all()
        model.Projection.clear_all()
        male, female = model.Projection[1], model.Projection[99]
        assert male.model_point()["sex"] == "M" and female.model_point()["sex"] == "F"
        assert female.prem_pp(1) == male.prem_pp(1) == 3000.00
        assert female.freq_load() == male.freq_load()
        assert female.beitragssumme_pp() == male.beitragssumme_pp()
        assert female.alpha_total_pp() == male.alpha_total_pp()
        assert female.charge_prem_pp(1) == male.charge_prem_pp(1)
        assert female.charge_acq_pp(1) == male.charge_acq_pp(1)
        assert female.annuity_rate_guar() == male.annuity_rate_guar()
        assert female.annuity_rate_appl() == male.annuity_rate_appl() == 32.00
        assert female.lapse_rate(1) == male.lapse_rate(1)
        assert female.decl_rate(1) == male.decl_rate(1)
        # The one place sex is allowed to reach: the mortality basis, hence the Risikobeitrag.
        assert female.mort_rate_guar(1) / male.mort_rate_guar(1) == pytest.approx(
            0.001300 / 0.002000, rel=1e-9)
        assert female.charge_risk_pp(1) < male.charge_risk_pp(1)
        assert female.capital_conv_pp() > male.capital_conv_pp()
    finally:
        model.close()


# --- Pitfall 17: amortising against a shrunken Beitragssumme
def test_pitfall_17_the_beitragssumme_survives_a_beitragsfreistellung(
        klassische_rentenversicherung, de_rv_anchor):
    """The Sec. 4 DeckRV base is the premiums payable **as written**, not what is left:
    ``beitragssumme_pp`` sums ``prem_pp_sched``, which ignores ``pup_year``."""
    p = klassische_rentenversicherung.Projection[7]
    assert int(p.model_point()["pup_year"]) == 10
    assert p.beitragssumme_pp() == pytest.approx(22 * 3600.00, abs=CENT)
    assert p.alpha_total_pp() == pytest.approx(0.025 * 79200.00, abs=CENT)
    assert p.prem_pp_sched(10) == pytest.approx(3600.00, abs=CENT)   # as written
    assert p.prem_pp(10) == 0.0                                      # as charged
    assert p.beitragssumme_pp() > sum(p.prem_pp(t) for t in range(1, 23))
    assert all(p.alpha_cum_pp(t) <= p.alpha_total_pp() + 1e-9 for t in (1, 5, 10, 22))
    assert p.alpha_cum_pp(2) == pytest.approx(p.alpha_total_pp(), rel=1e-12)
    assert p.charge_acq_pp(2) == 0.0
    # The Dynamik grows the base rather than shrinking it: point 12 at 5 % a year.
    dyn = klassische_rentenversicherung.Projection[12]
    assert float(dyn.model_point()["dynamik_rate"]) == 0.05
    assert dyn.prem_pp(2) == pytest.approx(1500.00 * 1.05, abs=CENT)
    assert dyn.beitragssumme_pp() == pytest.approx(
        sum(1500.00 * 1.05 ** (t - 1) for t in range(1, 23)), abs=CENT)
    assert dyn.beitragssumme_pp() == pytest.approx(57757.82, abs=CENT)
    assert dyn.alpha_total_pp() == pytest.approx(0.025 * 57757.82, abs=CENT)
    assert de_rv_anchor.beitragssumme_pp() == pytest.approx(51000.00, abs=CENT)


# --- Pitfall 18: truncating the payout phase
def test_pitfall_18_the_payout_phase_is_not_truncated(de_rv_anchor):
    """``proj_len() = omega_age - issue_age``, and the frame ends there with no survivors: a
    40-year horizon would strand 0,219599 of a policy at attained age 90 and drop 5 757,00 EUR
    of annuity payments, 24,5 % of the payout phase."""
    p = de_rv_anchor
    df = p.result_cf()
    assert p.proj_len() == 121 - 50 == 71
    assert list(df.index) == list(range(1, 72)) and df.index.name == "t"
    assert df.index[-1] == p.proj_len()
    assert p.pols_if(72) == 0.0 and p.pols_if(71) > 0.0
    assert p.check_decrement_closure() is True
    assert p.check_decrement_closure_resid(71) == pytest.approx(0.0, abs=1e-12)
    assert p.pols_if(41) == pytest.approx(0.219599, abs=SIX_DP) and p.age(41) == 90
    dropped = df.loc[41:, "annuity_payments"].sum()
    assert dropped == pytest.approx(5757.00, abs=CENT)
    assert dropped / df["annuity_payments"].sum() == pytest.approx(0.245, abs=0.0005)
    assert p.pols_if(71) < SIX_DP and abs(p.net_cf(71)) < CENT


# --- The published identities
def test_every_check_identity_holds_on_the_anchor(de_rv_anchor):
    """All nine ``check_*`` cells return True, and their residuals are zero at every t."""
    p = de_rv_anchor
    for name in CHECKS:
        assert getattr(p, name)() is True, name
    for t in (1, 2, 5, 12, 17, 18, 27, 40, 71):
        assert p.check_net_cf_resid(t) == pytest.approx(0.0, abs=1e-9)
        assert p.check_pols_roll_fwd_resid(t) == pytest.approx(0.0, abs=1e-12)
        assert p.check_decrement_closure_resid(t) == pytest.approx(0.0, abs=1e-12)
        assert p.check_av_roll_fwd_resid(t) == pytest.approx(0.0, abs=1e-8)
        assert p.check_av_sur_roll_fwd_resid(t) == pytest.approx(0.0, abs=1e-8)
        assert p.check_prem_split_resid(t) == pytest.approx(0.0, abs=1e-9)
        assert p.check_cv_floor_resid(t) == pytest.approx(0.0, abs=1e-9)
        assert p.check_annuity_conv_resid(t) == pytest.approx(0.0, abs=1e-6)
        assert p.check_annuity_guarantee_resid(t) == pytest.approx(0.0, abs=1e-12)


def test_check_net_cf_rebuilds_the_headline_from_the_published_columns(de_rv_anchor):
    """delib's first ruling, rebuilt from the frame: ``net_cf = premiums - claims_death -
    claims_lapse - claims_commutation - annuity_payments - expenses``, with
    ``liability_cf = -net_cf`` exactly.  The account movements beside them are internal and
    are reported, not summed."""
    df = de_rv_anchor.result_cf()
    rebuilt = (df["premiums"] - df["claims_death"] - df["claims_lapse"]
               - df["claims_commutation"] - df["annuity_payments"] - df["expenses"])
    assert (rebuilt - df["net_cf"]).abs().max() == pytest.approx(0.0, abs=1e-9)
    assert (df["net_cf"] + df["liability_cf"]).abs().max() == pytest.approx(0.0, abs=1e-9)
    assert de_rv_anchor.check_net_cf() is True
    assert df["prem_to_av"].sum() == pytest.approx(32671.5572, abs=CENT)
    assert df["int_credited"].sum() == pytest.approx(2695.8201, abs=CENT)
    assert df["bonus_credited"].sum() == pytest.approx(4737.8262, abs=CENT)
    internal = df["prem_to_av"].sum() + df["int_credited"].sum() + df["bonus_credited"].sum()
    assert internal > abs(df["net_cf"].sum())


@pytest.mark.parametrize("point_id", [2, 6, 7, 8, 9, 13])
def test_the_check_identities_hold_where_an_option_is_switched_on(
        klassische_rentenversicherung, point_id):
    """The six model points that exercise an option, each closing all nine identities: the
    *Einmalbeitrag*, the legacy vintage, the *Beitragsfreistellung* conversion and its Sec. 165
    cash-out branch, full commutation, and the guaranteed factor with the value floor."""
    p = klassische_rentenversicherung.Projection[point_id]
    for name in CHECKS:
        assert getattr(p, name)() is True, f"{point_id}: {name}"
    df = p.result_cf()
    assert df.index[-1] == p.proj_len()
    assert not df.isna().any().any()
    assert (df["pols_if"] >= -1e-12).all()


# --- Structure, documentation and inputs
def test_result_cf_shape_and_both_signs_of_the_net_flow(de_rv_anchor):
    """The fifteen published columns, the two account balances among them, and the sign."""
    df = de_rv_anchor.result_cf()
    assert list(df.columns) == [
        "pols_if", "pols_annuity", "av", "av_sur", "premiums", "prem_to_av",
        "int_credited", "bonus_credited", "claims_death", "claims_lapse",
        "claims_commutation", "annuity_payments", "expenses", "liability_cf", "net_cf",
    ]
    assert df["pols_if"].iloc[0] == de_rv_anchor.pols_if_init()
    # A cash flow statement must not publish its own subtotal beside its parts, and the
    # retired column names must not come back.
    for absent in ("claims", "claims_surr", "claims_wd", "claims_commute"):
        assert absent not in df.columns
    assert (df.loc[1:16, "net_cf"] > 0).all()
    assert df.loc[17, "net_cf"] == pytest.approx(-8148.86, abs=CENT)
    assert (df.loc[18:70, "net_cf"] < 0).all()


def test_invalid_enum_values_raise(de_rv_anchor):
    """The enum accessors validate rather than propagating a typo into a lookup."""
    with pytest.raises(FormulaError):
        de_rv_anchor.claims(1, "SURRENDER")
    with pytest.raises(FormulaError):
        de_rv_anchor.pols_if_at(1, "AFTER_LAPSE")
    with pytest.raises(FormulaError):
        de_rv_anchor.av_pp_at(1, "AFT_LAPSE")
    with pytest.raises(FormulaError):
        de_rv_anchor.av_sur_pp_at(1, "BEF_INT")


def test_docstrings_describe_the_current_structure(klassische_rentenversicherung):
    """Specifics a reader would rely on, asserted so they cannot go stale silently."""
    doc = flat(klassische_rentenversicherung.doc)
    assert "mechanics demonstration" in doc
    assert "external" in doc                      # inputs are not stored in the model
    assert "once per model" in doc                # why Data exists
    assert "Data" in doc and "Projection" in doc
    assert "Rentenfaktor" in doc and "Rentengarantiezeit" in doc and "Deckungskapital" in doc
    proj = flat(klassische_rentenversicherung.Projection.doc)
    assert "Notes symbol" in proj
    for cells in ("proj_len", "model_point", "av_pp_at", "pols_annuity", "bonus_rate",
                  "int_rate_guar", "annuity_rate_appl", "cv_floor_pp"):
        assert cells in proj, cells
    data = flat(klassische_rentenversicherung.Data.doc)
    assert "TradLife_A" in data and "provenance" in data
    for cells in ("input_dir", "model_point_table", "mort_table", "rentenfaktor_table"):
        assert cells in data, cells


def test_the_annuity_chassis_vocabulary_is_present(klassische_rentenversicherung):
    """Names the sister German models on this chassis share must mean the same thing here."""
    shared = {
        "model_point", "proj_len", "age", "calendar_year", "pols_if", "pols_if_at",
        "pols_if_init", "pols_death", "pols_lapse", "mort_rate", "mort_rate_guar",
        "lapse_rate", "prem_pp", "premiums", "prem_to_av_pp", "prem_to_av", "av_pp",
        "av_pp_at", "av", "av_at", "av_sur_pp", "av_sur", "cv_pp", "claims", "expenses",
        "net_cf", "liability_cf", "result_cf", "check_net_cf", "check_net_cf_resid",
    }
    names = set(klassische_rentenversicherung.Projection.cells) | set(
        klassische_rentenversicherung.Projection.refs)
    assert shared <= names, f"missing: {sorted(shared - names)}"


def test_the_shipped_tables_mark_their_own_provenance():
    """Eight CSVs beside run.py, and every one but the model point table says where it came
    from.  The mortality table is a **[std]** proxy anchored at ``q_base(M, 50) = 0.002000``,
    the *Rentenfaktor* table at age 67, and the lapse table's one shaped feature is the
    duration-12 step."""
    import pandas as pd

    assert {p.name for p in INPUT_DIR.iterdir() if p.suffix == ".csv"} == CSV_FILES
    for name in CSV_FILES - {"model_point_table.csv"}:
        frame = pd.read_csv(INPUT_DIR / name)
        assert "provenance" in frame.columns, name
        assert frame["provenance"].notna().all(), name
        assert (frame["provenance"].astype(str).str.len() > 0).all(), name
    assert "provenance" not in pd.read_csv(INPUT_DIR / "model_point_table.csv").columns

    mort = pd.read_csv(INPUT_DIR / "mort_table.csv", index_col=["sex", "age"])
    assert float(mort.loc[("M", 50), "q_base"]) == 0.002000
    assert float(mort.loc[("F", 50), "q_base"]) == 0.001300
    assert float(mort.loc[("M", 120), "q_base"]) == 1.0
    assert float(mort.loc[("M", 51), "q_base"]) / float(mort.loc[("M", 50), "q_base"]) == (
        pytest.approx(1.09, rel=1e-6))
    assert float(mort.loc[("M", 55), "improve"]) == 0.015
    assert float(mort.loc[("M", 110), "improve"]) == 0.0
    assert all(p.startswith("[std]") for p in mort["provenance"])
    gompertz = mort[mort["provenance"].str.contains("Gompertz")]["provenance"]
    assert len(gompertz) == len(mort) - 2          # every row but the two age-120 closures
    assert all("DAV 2004 R is DAV property and is not redistributed" in p for p in gompertz)

    factors = pd.read_csv(INPUT_DIR / "rentenfaktor_table.csv",
                          index_col=["rf_scenario_id", "age"])
    assert set(factors.index.get_level_values(0)) == {"base", "low", "high"}
    assert float(factors.loc[("base", 67), "annuity_rate_curr"]) == 32.00
    assert float(factors.loc[("low", 67), "annuity_rate_curr"]) == 25.50
    assert float(factors.loc[("high", 67), "annuity_rate_curr"]) == 35.00
    assert all("gap 3" in p for p in factors["provenance"])

    lapse = pd.read_csv(INPUT_DIR / "lapse_table.csv", index_col="duration")
    assert [float(lapse.loc[d, "lapse_rate"]) for d in (1, 11, 12, 13)] == [
        0.060, 0.035, 0.060, 0.030]                # the duration-12 step
    assert "EStG" in lapse.loc[12, "provenance"]

    charges = pd.read_csv(INPUT_DIR / "charge_table.csv", index_col=["charge_id", "item"])
    assert float(charges.loc[("zillmer_25", "alpha_rate"), "value"]) == 0.025
    assert float(charges.loc[("zillmer_40", "alpha_rate"), "value"]) == 0.040
    assert float(charges.loc[("zillmer_25", "alpha_spread_years"), "value"]) == 5
    assert float(charges.loc[("zillmer_40", "stornoabzug_rate"), "value"]) == 0.0

    points = pd.read_csv(INPUT_DIR / "model_point_table.csv", index_col="point_id")
    assert len(points) == 14 and points.loc[1, "policy_id"] == "DE-RV-0001"
    assert set(points["prem_freq"]) == {"annual", "half_yearly", "quarterly", "monthly"}
    assert set(points["death_benefit_form"]) == {"prem_refund", "deckungskapital", "max"}
    assert set(points["payout_system"]) == {"konstant", "teildynamisch", "volldynamisch"}
    assert sorted(set(points["int_rate_guar"])) == [0.0090, 0.0100, 0.0275]


def test_an_input_can_be_swapped_without_touching_formulas(tmp_path):
    """This is what a production user does with a licensed or company generational table."""
    import pandas as pd

    lighter = pd.read_csv(INPUT_DIR / "mort_table.csv", index_col=["sex", "age"])
    lighter["q_base"] = lighter["q_base"] * 0.5
    lighter.loc[(slice(None), 120), "q_base"] = 1.0
    alt = tmp_path / "mort_table_light.csv"
    lighter.to_csv(alt)

    model = mx.read_model(MODEL_DIR, name="RV_DE_A_swap")
    try:
        base = model.Projection[1].result_cf()
        model.Data.mort_file = str(alt)
        model.Data.clear_all()
        model.Projection.clear_all()
        light = model.Projection[1].result_cf()
        # Lighter mortality: fewer death claims, more premium collected, a longer annuity.
        assert light["claims_death"].sum() < base["claims_death"].sum()
        assert light["premiums"].sum() > base["premiums"].sum()
        assert light["annuity_payments"].sum() > base["annuity_payments"].sum()
        assert model.Projection[1].check_decrement_closure() is True
        assert model.Projection[1].check_net_cf() is True
    finally:
        model.close()
