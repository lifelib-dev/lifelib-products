"""Golden and structural tests for FRV_DE_S.

The golden values are the worked example in
products/fondsgebundene_rentenversicherung/technical-notes.md ("Worked example"), which
is a **configuration** rather than a scenario: a *fondsgebundene Rentenversicherung* --
the German unit-linked deferred private annuity, Schicht 3, single life, one fund, no
*Beitragsgarantie* -- sold to a man aged 37 last birthday, new business so
``duration_init_m = 0`` and ``proj_start() = 1``, with a level recurring *Beitrag* of
200,00 EUR a month for 30 years and *Rentenbeginn* at 67, so ``proj_len() = 360`` and the
frame is ``t = 1 ... 360``.  The *Beitragssumme* is 200.00 x 12 x 30 = 72 000,00 EUR, the
acquisition charge is 2.50 % of it -- the *Höchstzillmersatz* -- spread over sixty monthly
instalments of 30,00 EUR, so the *Anlagebeitrag* is 162,00 EUR while the instalment runs
and 192,00 EUR from month 61.  The death benefit is the *Beitragsrückgewähr*
``max(Fondsguthaben, Summe der gezahlten Beiträge)``; the charge scale is ``std_gross``
(beta 4.00 % of each *Beitrag*, gamma 0.30 % p.a. of the *Fondsguthaben* taken as
0.30 %/12 a month, *Stückkosten* 3,00 EUR a month, no *Stornoabzug*); the fund is ``base``,
5.00 % p.a. gross less a 0.45 % TER, so 0,371482 % a month; the conversion factors are
``std_2026``, guaranteed and current both 25.00 at age 67.  No *Zuzahlung*, no
*Teilentnahme*, no *Beitragsdynamik*, no *Ablaufmanagement* and no behaviour module.

``proj_len() = 360`` is far too long to assert row by row, so this module asserts the
seventeen months the notes print -- the first six, 12, 24, the acquisition cliff at 59 to
61, 120, 240, the tax-threshold lapse step at 300 to 301, and the last two -- together
with **every column total at full precision**, which is where a slice of rows cannot hide
an error.  The goldens are hard-coded rather than pickled so a reviewer can compare them
against the notes by eye.  Tolerances follow the precision the notes display: money to the
cent, ``pols_if`` and unit counts to six decimals, rates to eight.

Beyond the worked example this module asserts:

* the notes' three independent rebuilds -- month 1 from the tariff alone, month 61 at the
  cliff with the risk charge at a second attained age, and the reduction in yield read as
  a savings account accumulating 200,00 EUR a month at the model's own IRR;
* the four closure identities the notes print: the decrements summing to one, the
  *Risikoergebnis* being exactly a quarter of the *Risikobeitrag*, the acquisition ledger
  closing on the *Höchstzillmersatz*, and the benefit-funding split;
* the *Einmalbeitrag* variant (model point 2) and the four-tariff reduction-in-yield
  comparison the notes tabulate;
* the seven ``check_*()`` identities and their per-month residuals, ``check_net_cf()``
  among them -- delib's first ruling, that the headline number of a cash flow model must
  be reconstructible from the parts the frame publishes;
* **one test per numbered modeling pitfall in the technical notes**, eighteen of them, each
  named for the pitfall it guards: the fund-based charge cancelling units rather than being
  netted off the premium; the fund's TER never appearing as a policy charge; the
  *Risikobeitrag* priced on a death table and not on the annuity table; one mortality basis
  for charge and decrement deleting the risk result; the two monthly conversions staying
  different; the net amount at risk floored at zero; the acquisition instalment stopping at
  its window; an in-force cell never charged again for acquisition; the *Beitragssumme* not
  following the premiums paid; *Storno* and *Beitragsfreistellung* staying two things; the
  *Rückkaufswert* being the *Fondsguthaben*; the *Stornoabzug* not built out of unamortised
  acquisition costs; no account-value benefit booked as an insurer outgo; the age at
  *Rentenbeginn* not off by one; the *Rentenfaktor* rule being a maximum of two; the
  *Ratenzahlungszuschlag* not applied twice; the *Beitragsrückgewähr* base being the
  premiums paid and not the premiums invested; and no fixed charge driving the fund
  negative;
* the product's own invariants -- the frame's shape and both signs of the net flow, the
  behaviour modules being off and reachable, the enum accessors validating, and the shipped
  tables marking their own provenance.

There is deliberately **no sweep of the whole model point table** here: the conventions
suite owns the single sweep, because a model point's first evaluation is the most expensive
thing in the run.
"""
import modelx as mx
import pytest
from modelx.core.errors import FormulaError

from de_registry import MODELS, LIB


CENT = 0.005          # money displayed to 2 d.p.
SIX_DP = 0.0000005    # pols_if and unit counts displayed to 6 d.p.
EIGHT_DP = 5e-9       # decrement rates displayed to 8 d.p.

MODEL_DIR = LIB / MODELS["FRV_DE_S"][0]
INPUT_DIR = MODEL_DIR.parent

CSV_FILES = {
    "model_point_table.csv",
    "mort_table.csv",
    "lapse_table.csv",
    "charge_table.csv",
    "fund_scenario_table.csv",
    "rentenfaktor_table.csv",
}

# ---------------------------------------------------------------------------
# The worked example: Panel A, the non-unit ledger.
#
# t: (pols_if, premiums, prem_to_av, charge_acq, charge_admin_prem, charge_admin_fund,
#     charge_policy_fee, charge_risk, expenses, net_cf)
#
# stornoabzug and withdrawals are 0.00 in every month of this cell -- the composite
# tariff has no Stornoabzug and this model point takes no Teilentnahme -- so the notes
# omit them from the printed table.  They are asserted in the row test all the same,
# because a zero column states a product fact where a missing one would hide it.
PANEL_A = {
    1:   (1.000000, 200.00, 162.00, 30.00, 8.00, 0.04, 3.00, 0.00, 2007.26, -1966.22),
    2:   (0.994807, 198.96, 161.16, 29.84, 7.96, 0.08, 2.98, 0.01,    7.23,    33.64),
    3:   (0.989641, 197.93, 160.32, 29.69, 7.92, 0.12, 2.97, 0.01,    7.20,    33.49),
    4:   (0.984502, 196.90, 159.49, 29.54, 7.88, 0.16, 2.95, 0.01,    7.17,    33.35),
    5:   (0.979390, 195.88, 158.66, 29.38, 7.84, 0.20, 2.94, 0.01,    7.14,    33.21),
    6:   (0.974304, 194.86, 157.84, 29.23, 7.79, 0.24, 2.92, 0.02,    7.11,    33.08),
    12:  (0.944340, 188.87, 152.98, 28.33, 7.55, 0.46, 2.83, 0.03,    6.93,    32.26),
    24:  (0.887098, 177.42, 143.71, 26.61, 7.10, 0.88, 2.66, 0.05,    6.58,    30.69),
    59:  (0.738908, 147.78, 119.70, 22.17, 5.91, 1.93, 2.22, 0.10,    5.67,    26.58),
    60:  (0.735054, 147.01, 119.08, 22.05, 5.88, 1.95, 2.21, 0.10,    5.64,    26.47),
    61:  (0.731221, 146.24, 140.39,  0.00, 5.85, 1.98, 2.19, 0.11,    5.52,     4.53),
    120: (0.625891, 125.18, 120.17,  0.00, 5.01, 4.02, 1.88, 0.00,    5.01,     5.89),
    240: (0.459656,  91.93,  88.25,  0.00, 3.68, 7.71, 1.38, 0.00,    4.19,     8.58),
    300: (0.385184,  77.04,  73.96,  0.00, 3.08, 9.16, 1.16, 0.00,    3.76,     9.64),
    301: (0.384018,  76.80,  73.73,  0.00, 3.07, 9.19, 1.15, 0.00,    3.83,     9.58),
    359: (0.304251,  60.85,  58.42,  0.00, 2.43, 9.82, 0.91, 0.00,    3.18,     9.98),
    360: (0.303239,  60.65,  58.22,  0.00, 2.43, 9.84, 0.91, 0.00,   33.44,   -20.27),
}

# The notes' Total row for Panel A, summed at full precision and then rounded.
PANEL_A_TOTALS = {
    "pols_if": 202.931416,
    "premiums": 40586.28,
    "prem_to_av": 37413.08,
    "charge_acq": 1549.75,
    "charge_admin_prem": 1623.45,
    "charge_admin_fund": 2033.18,
    "charge_policy_fee": 608.79,
    "charge_risk": 5.85,
    "expenses": 3728.76,
    "net_cf": 2087.87,
}

# Panel B -- the benefits, and what funds them.
# t: (claims_death, claims_lapse, claims_maturity, av_releases, death_strain, liability_cf)
PANEL_B = {
    1:   ( 0.01,   0.82,     0.00,     0.83, 0.0020, 1966.22),
    2:   ( 0.02,   1.64,     0.00,     1.65, 0.0040,  -33.64),
    6:   ( 0.06,   4.84,     0.00,     4.89, 0.0114,  -33.08),
    12:  ( 0.11,   9.48,     0.00,     9.57, 0.0212,  -32.26),
    24:  ( 0.23,  18.18,     0.00,    18.38, 0.0398,  -30.69),
    60:  ( 0.65,  40.13,     0.00,    40.70, 0.0745,  -26.47),
    61:  ( 0.72,  20.10,     0.00,    20.73, 0.0799,   -4.53),
    120: ( 1.90,  40.75,     0.00,    42.64, 0.0000,   -5.89),
    240: ( 9.43,  78.11,     0.00,    87.54, 0.0000,   -8.58),
    301: (19.90, 237.76,     0.00,   257.66, 0.0000,   -9.58),
    359: (31.15,  99.47,     0.00,   130.61, 0.0000,   -9.98),
    360: (31.19,   0.00, 39298.91, 39330.11, 0.0000,   20.27),
}

PANEL_B_TOTALS = {
    "claims_death": 3047.80,
    "claims_lapse": 22522.64,
    "claims_maturity": 39298.91,
    "av_releases": 64864.97,
    "death_strain": 4.39,
    "liability_cf": -2087.87,
}

# Panel C -- the Fondsguthaben, per policy.  Balances have no total, being balances.
# t: (unit_price, units_pp, av_pp, bef_charge, aft_charge, bef_decr, cum_prem_pp,
#     nar_pp, lapse_rate_mth, mort_rate_mth)
PANEL_C = {
    1:   (100.371482,   0.000000,      0.00,    162.60,    159.56,    159.56,
          200.00,    40.44, 0.00514301, 0.00005000),
    2:   (100.744344,   1.589679,    159.56,    322.75,    319.67,    319.67,
          400.00,    80.33, 0.00514301, 0.00005000),
    6:   (102.249694,   7.885561,    803.31,    968.90,    965.66,    965.64,
          1200.00,  234.34, 0.00514301, 0.00005000),
    60:  (124.916609,  83.728674,  10420.39,  10621.70,  10616.05,  10615.91,
          12000.00, 1383.95, 0.00514301, 0.00007321),
    61:  (125.380652,  84.984001,  10615.91,  10848.06,  10842.35,  10842.20,
          12200.00, 1357.65, 0.00253505, 0.00008053),
    94:  (141.700579, 131.144920,  18514.53,  18776.02,  18768.33,  18768.33,
          18800.00,   31.67, 0.00253505, 0.00009744),
    95:  (142.226971, 132.450597,  18768.33,  19030.76,  19023.00,  19023.00,
          19000.00,    0.00, 0.00253505, 0.00009744),
    240: (243.489783, 274.678167,  66633.79,  67074.04,  67054.27,  67054.27,
          48000.00,    0.00, 0.00253505, 0.00030580),
    359: (378.539129, 340.534729, 128428.63, 129098.43, 129063.16, 129063.16,
          71800.00,    0.00, 0.00253505, 0.00079315),
    360: (379.945333, 340.950641, 129063.16, 129735.32, 129699.88, 129699.88,
          72000.00,    0.00, 0.00000000, 0.00079315),
}

# The Einmalbeitrag variant -- model point 2.  50 000,00 EUR at age 50, Rentenbeginn at
# 67 so proj_len() = 204, a `fund` death benefit so charge_risk is 0.00 at every month.
# t: (pols_if, premiums, prem_to_av, charge_acq, charge_admin_prem, charge_admin_fund,
#     charge_policy_fee, expenses, net_cf, av_bef_decr)
SINGLE_PREMIUM = {
    1:   (1.000000, 50000.00, 46750.00, 1250.00, 2000.00, 11.73, 3.00, 2204.28, 1060.45, 46908.94),
    2:   (0.994685,     0.00,     0.00,    0.00,    0.00, 11.71, 2.98,    4.27,   10.43, 47068.42),
    3:   (0.989399,     0.00,     0.00,    0.00,    0.00, 11.69, 2.97,    4.25,   10.40, 47228.46),
    12:  (0.943067,     0.00,     0.00,    0.00,    0.00, 11.48, 2.83,    4.11,   10.20, 48694.00),
    60:  (0.728611,     0.00,     0.00,    0.00,    0.00, 10.45, 2.19,    3.43,    9.20, 57329.28),
    120: (0.611558,     0.00,     0.00,    0.00,    0.00, 10.76, 1.83,    3.09,    9.50, 70347.78),
    204: (0.457239,     0.00,     0.00,    0.00,    0.00, 10.72, 1.37,   48.30,  -36.21, 93766.43),
}

SINGLE_PREMIUM_TOTALS = {
    "pols_if": 136.171795,
    "premiums": 50000.00,
    "prem_to_av": 46750.00,
    "charge_acq": 1250.00,
    "charge_admin_prem": 2000.00,
    "charge_admin_fund": 2206.15,
    "charge_policy_fee": 408.52,
    "expenses": 2911.63,
    "net_cf": 2953.04,
}

# The reduction in yield across the four shipped charge scales.  The four cells differ in
# premium and term as well as in tariff, so this is not a controlled experiment -- what it
# shows is that the charge scale moves the measure by a factor of five.
# point_id: (charge_id, scenario_id, reduction_in_yield, av_maturity_pp)
RIY_BY_TARIFF = {
    11: ("std_netto", "etf",  0.004484, 255658.29),
    13: ("std_low",   "base", 0.007799, 158606.04),
    1:  ("std_gross", "base", 0.013407, 129699.88),
    5:  ("std_high",  "base", 0.024073, 229128.42),
}

# The closure identities the notes print below the worked-example table.
DECREMENT_CLOSURE = {"deaths": 0.04377181, "lapses": 0.65322937, "maturity": 0.30299882}
RISK_RESULT = {"charge_risk": 5.849973, "death_strain": 4.387480, "risikoergebnis": 1.462493}
ACQUISITION_CLOSURE = {"instalment": 30.00, "count": 60, "total": 1800.00}
BENEFIT_FUNDING_CLOSURE = {"benefits": 64869.355293, "av_releases": 64864.967813,
                           "death_strain": 4.387480}

CHECKS = ("check_net_cf", "check_prem_split", "check_units_roll_fwd", "check_av_roll_fwd",
          "check_benefit_funding", "check_pols_roll_fwd", "check_acq_charge")


# ---------------------------------------------------------------------------
# The worked example


@pytest.mark.parametrize("t", sorted(PANEL_A))
def test_worked_example_panel_a_row(de_frv_anchor, t):
    """Every printed row of the notes' non-unit ledger, to the displayed precision."""
    (pols_if, prem, to_av, acq, admin_prem, admin_fund,
     fee, risk, exp, net) = PANEL_A[t]
    p = de_frv_anchor
    assert p.pols_if(t) == pytest.approx(pols_if, abs=SIX_DP)
    assert p.premiums(t) == pytest.approx(prem, abs=CENT)
    assert p.prem_to_av(t) == pytest.approx(to_av, abs=CENT)
    assert p.charge_acq(t) == pytest.approx(acq, abs=CENT)
    assert p.charge_admin_prem(t) == pytest.approx(admin_prem, abs=CENT)
    assert p.charge_admin_fund(t) == pytest.approx(admin_fund, abs=CENT)
    assert p.charge_policy_fee(t) == pytest.approx(fee, abs=CENT)
    assert p.charge_risk(t) == pytest.approx(risk, abs=CENT)
    assert p.expenses(t) == pytest.approx(exp, abs=CENT)
    assert p.net_cf(t) == pytest.approx(net, abs=CENT)
    # The two columns the notes omit for space, because they are zero throughout.
    assert p.stornoabzug(t) == 0.0
    assert p.withdrawals(t) == 0.0


@pytest.mark.parametrize("t", sorted(PANEL_B))
def test_worked_example_panel_b_row(de_frv_anchor, t):
    """The benefits and what funds them: every one is the policyholder's own fund.

    ``death_strain`` is carried to four decimals here rather than to the cent, because
    for most of the projection it is a hundredth of a cent a month and rounds to zero.
    """
    cd, cl, cm, releases, strain, liab = PANEL_B[t]
    p = de_frv_anchor
    assert p.claims(t, "DEATH") == pytest.approx(cd, abs=CENT)
    assert p.claims(t, "LAPSE") == pytest.approx(cl, abs=CENT)
    assert p.claims(t, "MATURITY") == pytest.approx(cm, abs=CENT)
    assert p.av_releases(t) == pytest.approx(releases, abs=CENT)
    assert p.death_strain(t) == pytest.approx(strain, abs=5e-5)
    assert p.liability_cf(t) == pytest.approx(liab, abs=CENT)
    assert p.liability_cf(t) == pytest.approx(-p.net_cf(t), rel=1e-12)


@pytest.mark.parametrize("t", sorted(PANEL_C))
def test_worked_example_panel_c_row(de_frv_anchor, t):
    """The per-policy unit side: the price, the units, and the four within-month balances.

    ``av_pp_at(t, "AFT_WD")`` equals ``av_pp_at(t, "AFT_CHARGE")`` throughout, there being
    no *Teilentnahme* on this cell, and the notes omit the column for that reason; it is
    asserted here so the omission stays a product fact rather than a gap.
    """
    (price, units, av, bef_charge, aft_charge, bef_decr,
     cum_prem, nar, lapse_mth, mort_mth) = PANEL_C[t]
    p = de_frv_anchor
    assert p.unit_price(t) == pytest.approx(price, abs=SIX_DP)
    assert p.units_pp(t) == pytest.approx(units, abs=SIX_DP)
    assert p.av_pp(t) == pytest.approx(av, abs=CENT)
    assert p.av_pp_at(t, "BEF_CHARGE") == pytest.approx(bef_charge, abs=CENT)
    assert p.av_pp_at(t, "AFT_CHARGE") == pytest.approx(aft_charge, abs=CENT)
    assert p.av_pp_at(t, "AFT_WD") == pytest.approx(aft_charge, abs=CENT)
    assert p.av_pp_at(t, "BEF_DECR") == pytest.approx(bef_decr, abs=CENT)
    assert p.cum_prem_pp(t) == pytest.approx(cum_prem, abs=CENT)
    assert p.db_floor_pp(t) == pytest.approx(cum_prem, abs=CENT)   # Beitragsrückgewähr
    assert p.nar_pp(t) == pytest.approx(nar, abs=CENT)
    assert p.lapse_rate_mth(t) == pytest.approx(lapse_mth, abs=EIGHT_DP)
    assert p.mort_rate_mth(t) == pytest.approx(mort_mth, abs=EIGHT_DP)
    # The in-force fund is the per-policy balance weighted by the start-of-month count.
    assert p.av_at(t, "BEF_DECR") == pytest.approx(
        p.av_pp_at(t, "BEF_DECR") * p.pols_if(t), rel=1e-12)


def test_the_totals_are_summed_at_full_precision(de_frv_anchor):
    """Every column total, summed at full precision and then rounded -- not cell by cell.

    Rounding each of the 360 cells to the cent first changes fourteen of the eighteen
    totals by one to twelve cents.  ``death_strain`` is the worst case and the reason the
    rule exists: it rounds to zero in almost every month, so the rounded sum loses six
    cents of a 4,39 EUR total.
    """
    df = de_frv_anchor.result_cf()
    for column, total in PANEL_A_TOTALS.items():
        tol = SIX_DP * len(df) if column == "pols_if" else CENT
        assert df[column].sum() == pytest.approx(total, abs=tol), column
    for column, total in PANEL_B_TOTALS.items():
        assert df[column].sum() == pytest.approx(total, abs=CENT), column
    assert df["stornoabzug"].sum() == 0.0
    assert df["withdrawals"].sum() == 0.0
    # And the rounded-cell sum really does differ, which is why this test exists.
    rounded = sum(round(de_frv_anchor.death_strain(t), 2) for t in df.index)
    assert rounded == pytest.approx(4.33, abs=CENT)
    assert df["death_strain"].sum() == pytest.approx(4.39, abs=CENT)


def test_month_one_rebuilt_from_the_tariff_alone(de_frv_anchor):
    """The notes' first independent check: month 1 from the parameters, not the recursion.

    Nine decimals are carried because six do not close the chain -- the *Gammakosten* at
    0.040650 would leave 159.561151 instead of 159.561150.
    """
    p = de_frv_anchor
    assert p.beitragssumme() == pytest.approx(200.00 * 12 * 30, rel=1e-12) == 72000.0
    assert p.charge_acq_total() == pytest.approx(0.025 * 72000.0, rel=1e-12) == 1800.0
    assert p.acq_instalments() == 60
    assert p.charge_acq_pp(1) == pytest.approx(1800.0 / 60, rel=1e-12) == 30.0
    assert p.charge_acq_pp(1) / p.prem_pp(1) == pytest.approx(0.15, rel=1e-12)
    assert p.charge_admin_prem_pp(1) == pytest.approx(0.04 * 200.00, rel=1e-12) == 8.0
    assert p.prem_to_av_pp(1) == pytest.approx(200.0 - 30.0 - 8.0, rel=1e-12) == 162.0
    assert p.units_bought_pp(1) == pytest.approx(162.0 / 100.0, rel=1e-12) == 1.62

    i = p.fund_return_net_mth(1)
    assert i == pytest.approx(1.0455 ** (1.0 / 12.0) - 1.0, rel=1e-14)
    assert i == pytest.approx(0.0037148195588312, abs=5e-16)
    assert p.unit_price(1) == pytest.approx(100.0 * (1.0 + i), rel=1e-14)
    assert p.av_pp_at(1, "BEF_CHARGE") == pytest.approx(1.62 * p.unit_price(1), rel=1e-14)
    assert p.av_pp_at(1, "BEF_CHARGE") == pytest.approx(162.601800769, abs=5e-9)

    assert p.charge_admin_fund_pp(1) == pytest.approx(
        0.0030 / 12 * 162.601800769, abs=5e-9)
    assert p.charge_admin_fund_pp(1) == pytest.approx(0.040650450, abs=5e-9)
    assert p.charge_policy_fee_pp(1) == 3.0
    assert p.av_pp_at(1, "AFT_CHARGE") == pytest.approx(159.561150318, abs=5e-9)

    # The Beitragsrückgewähr floor is the premium paid, so the risk charge is live.
    assert p.db_floor_pp(1) == 200.0
    assert p.nar_pp(1) == pytest.approx(200.0 - 159.561150318, abs=5e-9)
    assert p.nar_pp(1) == pytest.approx(40.438849682, abs=5e-9)
    assert p.charge_risk_pp(1) == pytest.approx(
        0.00080 / 12 * 40.438849682, abs=5e-10)
    assert p.charge_risk_pp(1) == pytest.approx(0.002695923, abs=5e-10)
    assert p.av_pp_at(1, "BEF_DECR") == pytest.approx(159.558454395, abs=5e-9)
    # ... which is exactly the unit count month 2 opens with.
    assert p.units_pp(2) == pytest.approx(159.558454395 / p.unit_price(1), abs=5e-9)
    assert p.units_pp(2) == pytest.approx(1.589679, abs=SIX_DP)


def test_month_sixty_one_is_the_cliff_and_the_risk_charge_at_a_second_age(de_frv_anchor):
    """The notes' second rebuild: the acquisition instalment stops and the age steps.

    The same row carries a second step -- ``claims_lapse`` halves from 40.13 to 20.10,
    because month 61 opens policy year 6 and the annual lapse rate drops from 6.0 % to
    3.0 %.
    """
    p = de_frv_anchor
    assert p.charge_acq_pp(60) == 30.0 and p.charge_acq_pp(61) == 0.0
    assert p.prem_to_av_pp(60) == pytest.approx(162.0, rel=1e-12)
    assert p.prem_to_av_pp(61) == pytest.approx(200.0 - 8.0, rel=1e-12) == 192.0

    i = p.fund_return_net_mth(61)
    assert p.av_pp_at(61, "BEF_CHARGE") == pytest.approx(
        (10615.913263 + 192.00) * (1.0 + i), abs=5e-6)
    assert p.av_pp_at(61, "BEF_CHARGE") == pytest.approx(10848.062710117, abs=5e-6)
    assert p.charge_admin_fund_pp(61) == pytest.approx(2.712015678, abs=5e-8)
    assert p.av_pp_at(61, "AFT_CHARGE") == pytest.approx(10842.350694440, abs=5e-6)

    # The attained age has stepped to 42, so the tariff rate is q(37) x 1.10^5.
    assert p.policy_year(61) == 6 and p.age(61) == 42
    assert p.mort_rate_tariff(61) == pytest.approx(0.00080 * 1.10 ** 5, rel=1e-9)
    assert p.mort_rate_tariff(61) == pytest.approx(0.001288408, abs=5e-10)
    assert p.mort_rate_tariff_mth(61) == pytest.approx(0.000107367333, abs=5e-13)
    assert p.cum_prem_pp(61) == pytest.approx(61 * 200.0, rel=1e-12) == 12200.0
    assert p.nar_pp(61) == pytest.approx(1357.649305560, abs=5e-6)
    assert p.charge_risk_pp(61) == pytest.approx(0.145767186, abs=5e-9)
    assert p.charge_risk(61) == pytest.approx(0.10658796, abs=5e-8)

    # The lapse step at the same boundary.
    assert p.lapse_rate(60) == pytest.approx(0.06, rel=1e-12)
    assert p.lapse_rate(61) == pytest.approx(0.03, rel=1e-12)
    assert p.claims(60, "LAPSE") == pytest.approx(40.13, abs=CENT)
    assert p.claims(61, "LAPSE") == pytest.approx(20.10, abs=CENT)


def test_the_reduction_in_yield_read_as_a_savings_account(de_frv_anchor):
    """The notes' third rebuild: 200,00 a month at the model's own IRR reaches the fund.

    Accumulating the same 360 premiums at the scenario's **gross** 5.00 % instead reaches
    163 739,57, and the 34 039,69 between the two is what the charge stack and the fund's
    own TER cost this policyholder over thirty years.
    """
    p = de_frv_anchor
    irr = p.irr_ann()
    assert irr == pytest.approx(0.036592629, abs=5e-9)
    monthly = (1.0 + irr) ** (1.0 / 12.0) - 1.0
    balance = sum(200.0 * (1.0 + monthly) ** (360 - t + 1) for t in range(1, 361))
    assert balance == pytest.approx(129699.8842, abs=CENT)
    assert p.av_maturity_pp() == pytest.approx(129699.8842, abs=CENT)

    gross_monthly = 1.05 ** (1.0 / 12.0) - 1.0
    gross_balance = sum(200.0 * (1.0 + gross_monthly) ** (360 - t + 1)
                        for t in range(1, 361))
    assert gross_balance == pytest.approx(163739.57, abs=1.0)
    assert gross_balance - balance == pytest.approx(34039.69, abs=1.0)

    assert p.gross_return_ref() == pytest.approx(0.05, abs=1e-12)
    assert p.reduction_in_yield() == pytest.approx(0.05 - irr, rel=1e-12)
    assert p.reduction_in_yield() == pytest.approx(0.013407, abs=5e-7)


def test_the_four_identities_that_close(de_frv_anchor):
    """The closure lines the notes print below the table, each exact.

    The acquisition line is the one worth reading twice: the ledger closes on 1 800,00 --
    the *Höchstzillmersatz* -- while the ``charge_acq`` **column** totals 1 549,75,
    because it is weighted by ``pols_if``.  Roughly one policy in seven has lapsed by
    month 60, which is the insurer's acquisition-cost problem in one number: it pays
    1 800,00 at inception and collects 1 549,75.
    """
    p = de_frv_anchor
    n = p.proj_len()
    df = p.result_cf()

    deaths = sum(p.pols_death(t) for t in range(1, n + 1))
    lapses = sum(p.pols_lapse(t) for t in range(1, n + 1))
    maturity = p.pols_maturity(n)
    assert deaths == pytest.approx(DECREMENT_CLOSURE["deaths"], abs=5e-9)
    assert lapses == pytest.approx(DECREMENT_CLOSURE["lapses"], abs=5e-9)
    assert maturity == pytest.approx(DECREMENT_CLOSURE["maturity"], abs=5e-9)
    assert deaths + lapses + maturity == pytest.approx(1.0, abs=1e-12)
    assert p.pols_if(n + 1) == 0.0

    charge_risk = df["charge_risk"].sum()
    strain = df["death_strain"].sum()
    assert charge_risk == pytest.approx(RISK_RESULT["charge_risk"], abs=5e-7)
    assert strain == pytest.approx(RISK_RESULT["death_strain"], abs=5e-7)
    assert charge_risk - strain == pytest.approx(RISK_RESULT["risikoergebnis"], abs=5e-7)
    assert charge_risk - strain == pytest.approx(0.25 * charge_risk, rel=1e-12)

    assert ACQUISITION_CLOSURE["count"] * ACQUISITION_CLOSURE["instalment"] == 1800.0
    assert p.cum_charge_acq_pp(n) == pytest.approx(1800.0, abs=1e-9)
    assert p.cum_charge_acq_pp(n) == pytest.approx(
        p.alpha_rate() * p.beitragssumme(), rel=1e-12)
    assert df["charge_acq"].sum() == pytest.approx(1549.75, abs=CENT)

    benefits = (df["claims_death"].sum() + df["claims_lapse"].sum()
                + df["claims_maturity"].sum())
    assert benefits == pytest.approx(BENEFIT_FUNDING_CLOSURE["benefits"], abs=5e-6)
    assert (df["av_releases"].sum() + df["death_strain"].sum()) == pytest.approx(
        BENEFIT_FUNDING_CLOSURE["benefits"], abs=5e-6)

    # And the net_cf total rebuilt from its own parts.
    charges = sum(df[c].sum() for c in ("charge_acq", "charge_admin_prem",
                                        "charge_admin_fund", "charge_policy_fee",
                                        "charge_risk", "stornoabzug"))
    assert charges == pytest.approx(5821.018511, abs=5e-6)
    assert charges - df["expenses"].sum() - strain == pytest.approx(2087.866187, abs=5e-6)


def test_the_annuity_the_contract_exists_for(de_frv_anchor):
    """The Fondsguthaben at Rentenbeginn, the factor it is read at, and the annuity."""
    p = de_frv_anchor
    assert p.av_maturity_pp() == pytest.approx(129699.88, abs=CENT)
    assert p.av_maturity_pp() == pytest.approx(
        p.av_pp_at(p.proj_len(), "BEF_DECR"), rel=1e-15)
    assert p.annuity_age() == 67
    assert p.rentenfaktor_guar() == 25.0 and p.rentenfaktor_curr() == 25.0
    assert p.rentenfaktor_applied() == 25.0
    assert p.annuity_mth_pp() == pytest.approx(129699.88 / 10000.0 * 25.0, abs=CENT)
    assert p.annuity_mth_pp() == pytest.approx(324.25, abs=CENT)
    # The maturity claim is the whole surviving cohort's fund, and nothing else.
    assert p.claims(p.proj_len(), "MATURITY") == pytest.approx(
        p.pols_maturity(p.proj_len()) * p.av_maturity_pp(), rel=1e-12)


# ---------------------------------------------------------------------------
# The variants the notes tabulate


@pytest.mark.parametrize("t", sorted(SINGLE_PREMIUM))
def test_the_einmalbeitrag_variant_row(fondsgebundene_rentenversicherung, t):
    """Model point 2: the charges are taken once, at the front, and the sign reverses.

    Month 1 carries a ``net_cf`` of **+1 060,45** where the anchor's is -1 966,22, because
    the 3 250,00 withheld at inception more than covers the 2 204,28 of acquisition cost
    and there is no sixty-month recovery to wait for.
    """
    (pols_if, prem, to_av, acq, admin_prem, admin_fund,
     fee, exp, net, av) = SINGLE_PREMIUM[t]
    p = fondsgebundene_rentenversicherung.Projection[2]
    assert p.prem_form() == "einmal"
    assert p.pols_if(t) == pytest.approx(pols_if, abs=SIX_DP)
    assert p.premiums(t) == pytest.approx(prem, abs=CENT)
    assert p.prem_to_av(t) == pytest.approx(to_av, abs=CENT)
    assert p.charge_acq(t) == pytest.approx(acq, abs=CENT)
    assert p.charge_admin_prem(t) == pytest.approx(admin_prem, abs=CENT)
    assert p.charge_admin_fund(t) == pytest.approx(admin_fund, abs=CENT)
    assert p.charge_policy_fee(t) == pytest.approx(fee, abs=CENT)
    assert p.expenses(t) == pytest.approx(exp, abs=CENT)
    assert p.net_cf(t) == pytest.approx(net, abs=CENT)
    assert p.av_pp_at(t, "BEF_DECR") == pytest.approx(av, abs=CENT)
    # No Beitragssumme to zillmer against and no net amount at risk on a `fund` benefit.
    assert p.charge_risk(t) == 0.0


def test_the_einmalbeitrag_variant_totals_and_conversion(fondsgebundene_rentenversicherung):
    """The acquisition charge is the *Zuzahlungskosten*, levied once on receipt."""
    p = fondsgebundene_rentenversicherung.Projection[2]
    df = p.result_cf()
    assert p.proj_len() == 12 * (67 - 50) == 204
    assert p.acq_window_months() == 0 and p.acq_instalments() == 1
    assert p.beitragssumme() == 50000.0
    assert p.charge_acq_total() == pytest.approx(
        p.zuzahlung_charge_rate() * 50000.0, rel=1e-12) == 1250.0
    for column, total in SINGLE_PREMIUM_TOTALS.items():
        tol = SIX_DP * len(df) if column == "pols_if" else CENT
        assert df[column].sum() == pytest.approx(total, abs=tol), column
    assert p.av_maturity_pp() == pytest.approx(93766.43, abs=CENT)
    assert p.annuity_mth_pp() == pytest.approx(234.42, abs=CENT)
    assert p.reduction_in_yield() == pytest.approx(0.012320, abs=5e-7)
    assert all(getattr(p, c)() is True for c in CHECKS)


@pytest.mark.parametrize("point_id", sorted(RIY_BY_TARIFF))
def test_the_reduction_in_yield_across_the_four_charge_scales(
        fondsgebundene_rentenversicherung, point_id):
    """The charge scale moves the measure by a factor of five across the argued range.

    The four cells differ in premium and term as well as in tariff, so this is not a
    controlled experiment and must not be read as one.  What it is for: the gap between
    model point 11's *Nettotarif* and the anchor's commission tariff **is** the
    acquisition load, the parameter this library most needs and cannot source.
    """
    charge_id, scenario_id, riy, av = RIY_BY_TARIFF[point_id]
    p = fondsgebundene_rentenversicherung.Projection[point_id]
    assert p.charge_id() == charge_id and p.scenario_id() == scenario_id
    assert p.reduction_in_yield() == pytest.approx(riy, abs=5e-7)
    assert p.av_maturity_pp() == pytest.approx(av, abs=CENT)
    assert p.gross_return_ref() == pytest.approx(0.05, abs=1e-9)


def test_the_nettotarif_gap_is_the_acquisition_load(fondsgebundene_rentenversicherung):
    """std_netto carries no acquisition charge at all, and the model shows what that costs.

    ``comm_acq_rate`` is a flat scalar, so on the two low-load tariffs the assumed
    commission exceeds the tariff's own acquisition charge and those cells carry a
    projected loss.  That is the flat assumption showing, not a product fact -- a real
    *Nettotarif* pays no acquisition commission at all -- and it is stated in model.md
    rather than left to be discovered in a negative total.
    """
    netto = fondsgebundene_rentenversicherung.Projection[11]
    gross = fondsgebundene_rentenversicherung.Projection[1]
    assert netto.alpha_rate() == 0.0 and gross.alpha_rate() == 0.025
    assert netto.charge_acq_total() == 0.0
    assert netto.result_cf()["charge_acq"].sum() == 0.0
    assert netto.reduction_in_yield() < gross.reduction_in_yield()
    assert netto.result_cf()["net_cf"].sum() < 0.0
    assert gross.result_cf()["net_cf"].sum() > 0.0
    assert netto.expense_acq_pp(1) == pytest.approx(
        0.025 * netto.beitragssumme() + 200.0, rel=1e-12)


# ---------------------------------------------------------------------------
# Pitfall 1 -- the fund-based charge cancels units; it is not netted off the premium


def test_pitfall_1_the_fund_charge_cancels_units_and_survives_the_premium(
        fondsgebundene_rentenversicherung):
    """Model point 7 goes beitragsfrei at month 121 and the fund charges carry on.

    A model that deducted gamma from the *Beitrag* would be right until month 120 and
    wrong from month 121, where ``premiums`` is zero and ``charge_admin_fund`` is not.
    """
    p = fondsgebundene_rentenversicherung.Projection[7]
    assert p.pup_month() == 121
    assert p.premiums(120) > 0.0
    for t in (121, 122, 200, 240, 324):
        assert p.premiums(t) == 0.0
        assert p.charge_admin_prem(t) == 0.0     # stops with the premium
        assert p.charge_acq(t) == 0.0
        assert p.charge_admin_fund(t) > 0.0      # continues by unit cancellation
        assert p.charge_policy_fee(t) > 0.0
        assert p.charge_risk(t) > 0.0
    # The fund decays on a zero-return path once the premiums stop.
    assert p.scenario_id() == "zero"
    assert p.av_pp_at(122, "BEF_DECR") < p.av_pp_at(121, "BEF_DECR")
    assert p.av_pp_at(324, "BEF_DECR") < p.av_pp_at(121, "BEF_DECR")
    # ... and the fund-based charge is a rate on the fund, not on anything else.
    assert p.charge_admin_fund_pp(200) == pytest.approx(
        p.gamma_rate_mth() * p.av_pp_at(200, "BEF_CHARGE"), rel=1e-12)
    assert p.gamma_rate_mth() == pytest.approx(0.0030 / 12.0, rel=1e-15) == 0.00025


# ---------------------------------------------------------------------------
# Pitfall 2 -- the fund's TER is a return item and never a policy charge


def test_pitfall_2_the_ter_lives_in_the_unit_price_and_in_no_charge_column(
        fondsgebundene_rentenversicherung, de_frv_anchor):
    """unit_price(t)/unit_price(t-1) = (1 + gross - ter)^(1/12), exactly.

    Charging the TER explicitly double-counts the fund's costs; ignoring it overstates
    the policyholder's return.  The model does neither: it nets it off the assumed return,
    so it appears in no ``charge_*`` cells and in no ``result_cf()`` column.
    """
    p = de_frv_anchor
    assert p.fund_return_gross_ann(1) == 0.05 and p.fund_ter_ann(1) == 0.0045
    assert p.fund_return_net_ann(1) == pytest.approx(0.0455, rel=1e-12)
    for t in (1, 2, 61, 180, 360):
        step = (1.0 + p.fund_return_gross_ann(t) - p.fund_ter_ann(t)) ** (1.0 / 12.0)
        assert p.unit_price(t) / p.unit_price(t - 1) == pytest.approx(step, rel=1e-14)
    # No column carries it, and no cells is named for it.
    charge_columns = [c for c in p.result_cf().columns if c.startswith("charge_")]
    assert charge_columns == ["charge_acq", "charge_admin_prem", "charge_admin_fund",
                              "charge_policy_fee", "charge_risk"]
    names = set(fondsgebundene_rentenversicherung.Projection.cells) | set(
        fondsgebundene_rentenversicherung.Projection.refs)
    for absent in ("charge_ter", "charge_fund_cost", "ter_charge_pp", "fund_cost_pp"):
        assert absent not in names, absent
    # The ETF fund differs from the composite only in its TER, and it shows in the price.
    etf = fondsgebundene_rentenversicherung.Projection[11]
    assert etf.fund_ter_ann(1) == 0.0015 and etf.fund_return_gross_ann(1) == 0.05
    assert etf.fund_return_net_mth(1) > p.fund_return_net_mth(1)


# ---------------------------------------------------------------------------
# Pitfall 3 -- the Risikobeitrag is priced on a death table, not the annuity table


def test_pitfall_3_the_two_mortality_bases_live_in_two_files(
        fondsgebundene_rentenversicherung, de_frv_anchor):
    """No cells reads both mort_table.csv and rentenfaktor_table.csv.

    A German fondsgebundene contract prices its death charge on a death table (DAV 2008 T)
    and its conversion guarantee on an annuity table (DAV 2004 R).  A model using one for
    both misprices one of them, and the arithmetic form of "two bases at once" is that no
    formula in this model touches both files.
    """
    proj = fondsgebundene_rentenversicherung.Projection
    readers = {}
    for nm in proj.cells:
        src = proj.cells[nm].formula.source or ""
        readers[nm] = {t for t in ("data.mort_table(", "data.rentenfaktor_table(")
                       if t in src}
    assert readers["mort_rate_tariff_at_age"] == {"data.mort_table("}
    assert readers["rentenfaktor_guar"] == {"data.rentenfaktor_table("}
    assert readers["rentenfaktor_curr"] == {"data.rentenfaktor_table("}
    both = [nm for nm, hits in readers.items() if len(hits) == 2]
    assert both == [], f"cells reading both mortality files: {both}"

    p = de_frv_anchor
    assert p.charge_risk_pp(1) == pytest.approx(
        p.mort_rate_tariff_mth(1) * p.nar_pp(1), rel=1e-12)
    # The tariff rate at the anchor age is the proxy's anchor value, exactly.
    assert p.mort_rate_tariff_at_age(37) == 0.00080
    assert p.mort_rate_tariff_at_age(47) == pytest.approx(
        0.00080 * 1.10 ** 10, rel=1e-9)
    # ... and the annuity factor is nowhere near it: a different table, a different job.
    assert p.rentenfaktor_guar() == 25.0


# ---------------------------------------------------------------------------
# Pitfall 4 -- one basis for charge and decrement deletes the Risikoergebnis


def test_pitfall_4_the_risk_result_is_exactly_a_quarter_of_the_risk_charge(de_frv_anchor):
    """Sum charge_risk - sum death_strain = (1 - mort_be_factor) x sum charge_risk.

    The tariff prices on the first-order table and the projection decrements on the
    second-order one; the wedge between them is the *Risikoergebnis*.  With a flat
    ``mort_be_factor`` the ratio is closed form, which is the whole point of it being
    flat -- a model decrementing on the tariff basis would print zero here and look
    healthy doing it.
    """
    p = de_frv_anchor
    df = p.result_cf()
    charge = df["charge_risk"].sum()
    strain = df["death_strain"].sum()
    assert charge > 0.0 and strain > 0.0
    assert charge - strain > 0.0
    assert charge - strain == pytest.approx(0.25 * charge, rel=1e-12)
    assert p.mort_rate(1) == pytest.approx(0.75 * p.mort_rate_tariff(1), rel=1e-15)
    assert p.mort_rate(1) == pytest.approx(0.00060, abs=5e-9)
    assert p.mort_rate_tariff(1) == pytest.approx(0.00080, abs=5e-9)
    assert p.mort_rate_at_age(37) == pytest.approx(0.75 * 0.00080, rel=1e-15)
    # Per month it holds too: the strain is the decrement times the amount at risk.
    for t in (1, 30, 61):
        assert p.death_strain(t) == pytest.approx(
            p.pols_death(t) * p.nar_pp(t), rel=1e-12)
        assert p.charge_risk(t) - p.death_strain(t) == pytest.approx(
            0.25 * p.charge_risk(t), rel=1e-9)


# ---------------------------------------------------------------------------
# Pitfall 5 -- the two monthly conversions are not the same conversion


def test_pitfall_5_mortality_is_split_linearly_and_lapse_geometrically(de_frv_anchor):
    """q/12 for the charge and the decrement; 1 - (1-w)^(1/12) for the lapse rate.

    At q = 0.00080 the two splits differ by 0.04 %, which would land entirely in the risk
    result -- the one quantity the model is trying to measure.  The lapse rate is split
    the other way because nothing is priced off it and the annual rate is the observable
    that twelve monthly steps must reproduce.
    """
    p = de_frv_anchor
    for t in (1, 61, 300, 360):
        assert p.mort_rate_mth(t) == pytest.approx(p.mort_rate(t) / 12.0, rel=1e-15)
        assert p.mort_rate_tariff_mth(t) == pytest.approx(
            p.mort_rate_tariff(t) / 12.0, rel=1e-15)
    geometric = 1.0 - (1.0 - 0.00080) ** (1.0 / 12.0)
    assert 0.00080 / 12.0 == pytest.approx(0.00006667, abs=5e-9)
    assert geometric == pytest.approx(0.00006669, abs=5e-9)
    assert geometric / (0.00080 / 12.0) - 1.0 == pytest.approx(0.0004, abs=5e-5)

    for t in (1, 61, 301):
        assert p.lapse_rate_mth(t) == pytest.approx(
            1.0 - (1.0 - p.lapse_rate(t)) ** (1.0 / 12.0), rel=1e-14)
        assert p.lapse_rate_mth(t) < p.lapse_rate(t)
    assert p.lapse_rate_mth(1) == pytest.approx(0.00514301, abs=EIGHT_DP)
    assert p.lapse_rate_mth(61) == pytest.approx(0.00253505, abs=EIGHT_DP)
    # The fund return compounds geometrically for the same reason the lapse rate does,
    # while the gamma charge is divided by twelve because the tariff quotes it nominally.
    assert (1.0 + p.fund_return_net_mth(1)) ** 12 - 1.0 == pytest.approx(
        p.fund_return_net_ann(1), rel=1e-14)
    assert p.gamma_rate_mth() * 12.0 == pytest.approx(p.gamma_rate_ann(), rel=1e-15)


def test_pitfall_5_the_tax_step_is_not_keyed_on_duration_alone(
        fondsgebundene_rentenversicherung, de_frv_anchor):
    """The 12/62 rule needs both limbs, so the anchor's step falls in policy year 26.

    The anchor cell passes duration 12 at attained age 48, fourteen years before the tax
    benefit exists.  A model keying the spike on duration alone would fire it at month 145
    instead of month 301.
    """
    p = de_frv_anchor
    step_year = max(13, 62 - p.entry_age() + 1)
    assert step_year == 26
    assert p.policy_year(301) == 26 and p.age(301) == 62
    assert p.lapse_tax_step(300) == 1.0
    assert all(p.lapse_tax_step(t) == 2.5 for t in (301, 306, 312))
    assert p.lapse_tax_step(313) == 1.0
    assert p.lapse_rate_base(301) == pytest.approx(0.03, rel=1e-12)
    assert p.lapse_rate(301) == pytest.approx(0.075, rel=1e-12)
    assert p.lapse_rate_mth(301) == pytest.approx(0.00647574, abs=EIGHT_DP)
    assert p.lapse_rate(145) == pytest.approx(0.03, rel=1e-12)   # duration 13, age 49
    # On model point 12 the step never fires: the projection ends before its step year.
    short = fondsgebundene_rentenversicherung.Projection[12]
    assert short.entry_age() == 55 and max(13, 62 - 55 + 1) == 13
    assert short.proj_len() == 144
    assert all(short.lapse_tax_step(t) == 1.0
               for t in range(1, short.proj_len() + 1))


# ---------------------------------------------------------------------------
# Pitfall 6 -- the net amount at risk is floored at zero


def test_pitfall_6_the_net_amount_at_risk_is_floored_at_zero(
        fondsgebundene_rentenversicherung, de_frv_anchor):
    """max(D - F, 0), not D - F.  Without the floor the death strain turns negative.

    On the *Beitragsrückgewähr* shape the quantity is positive early and vanishes once the
    fund overtakes the premiums paid -- month 95 on the anchor cell -- and the unfloored
    difference is large and negative for the remaining 266 months.
    """
    p = de_frv_anchor
    n = p.proj_len()
    assert all(p.nar_pp(t) >= 0.0 for t in range(1, n + 1))
    assert all(p.death_strain(t) >= 0.0 for t in range(1, n + 1))
    assert p.nar_pp(94) > 0.0 and p.nar_pp(95) == 0.0
    assert p.av_pp_at(94, "AFT_WD") < p.cum_prem_pp(94)
    assert p.av_pp_at(95, "AFT_WD") > p.cum_prem_pp(95)
    unfloored = p.db_floor_pp(240) - p.av_pp_at(240, "AFT_WD")
    assert unfloored < -18000.0        # what an unfloored model would charge
    assert p.charge_risk_pp(240) == 0.0
    # A `fund` death benefit has no floor at all, so no Risikobeitrag anywhere.
    for point_id in (2, 13):
        q = fondsgebundene_rentenversicherung.Projection[point_id]
        assert q.db_form() == "fund"
        assert q.result_cf()["charge_risk"].sum() == 0.0
        assert q.result_cf()["death_strain"].sum() == 0.0
        assert all(q.nar_pp(t) == 0.0 for t in (1, q.proj_len() // 2, q.proj_len()))


# ---------------------------------------------------------------------------
# Pitfall 7 -- the acquisition instalment stops at its window


def test_pitfall_7_the_acquisition_instalment_stops_at_its_window(
        fondsgebundene_rentenversicherung, de_frv_anchor):
    """The instalment is zero for t > 60 on every cell, and the window follows the term.

    Two exceptions have to be stated rather than asserted away, and both follow from the
    definition of the charge: ``charge_acq(121)`` is non-zero on model point 9, where the
    *Zuzahlung* pays 500,00 of *Zuzahlungskosten* that the model books in ``charge_acq``;
    and the per-policy total equals ``alpha_rate x beitragssumme()`` on eleven points but
    not on point 6 (an in-force frame opening past the window) nor on point 9 (the
    *Zuzahlungskosten*).
    """
    p = de_frv_anchor
    assert p.acq_window_months() == 60 and p.acq_instalments() == 60
    assert all(p.charge_acq_pp(t) == 30.0 for t in (1, 30, 59, 60))
    assert all(p.charge_acq_pp(t) == 0.0 for t in (61, 62, 120, 360))
    assert p.check_acq_charge() is True

    # A two-year premium term spreads over 24 months, not 60, in 24 instalments.
    short = fondsgebundene_rentenversicherung.Projection[12]
    assert short.prem_term_y() == 2
    assert short.acq_window_months() == 24 and short.acq_instalments() == 24
    assert short.charge_acq_total() == pytest.approx(0.025 * 12000.0, rel=1e-12) == 300.0
    assert short.charge_acq_pp(24) == pytest.approx(300.0 / 24, rel=1e-12) == 12.5
    assert short.charge_acq_pp(25) == 0.0
    assert short.cum_charge_acq_pp(short.proj_len()) == pytest.approx(300.0, abs=1e-9)
    assert short.check_acq_charge() is True

    # The Zuzahlung exception, stated in the notes and asserted here.
    topup = fondsgebundene_rentenversicherung.Projection[9]
    assert topup.topup_month() == 121 and topup.topup_amount() == 20000.0
    assert topup.charge_acq_pp(121) == pytest.approx(0.025 * 20000.0, rel=1e-12) == 500.0
    assert topup.charge_acq_pp(122) == 0.0
    per_policy = sum(topup.charge_acq_pp(t)
                     for t in range(1, topup.proj_len() + 1))
    assert per_policy == pytest.approx(3380.0, abs=1e-9)
    assert topup.alpha_rate() * topup.beitragssumme() == pytest.approx(2880.0, rel=1e-12)
    assert topup.check_acq_charge() is True


def test_pitfall_7_the_instalment_count_follows_the_payment_frequency(
        fondsgebundene_rentenversicherung):
    """60 monthly, 20 quarterly, 10 half-yearly, 5 annual -- the window over the frequency.

    Spreading a quarterly contract's charge over sixty *months* would charge an instalment
    in months with no premium, and ``check_acq_charge`` counts the dates rather than
    accumulating the ledger, so it would fail there.
    """
    expected = {1: (1, 60, 30.0), 3: (3, 20, 111.0), 4: (6, 10, 132.0),
                5: (12, 5, 630.0)}
    for point_id, (mode, count, instalment) in expected.items():
        p = fondsgebundene_rentenversicherung.Projection[point_id]
        assert p.prem_mode_months() == mode, point_id
        assert p.acq_window_months() == 60, point_id
        assert p.acq_instalments() == count, point_id
        assert p.charge_acq_pp(1) == pytest.approx(instalment, abs=CENT), point_id
        assert p.charge_acq_total() == pytest.approx(count * instalment, abs=CENT)
        assert p.check_acq_charge() is True, point_id


# ---------------------------------------------------------------------------
# Pitfall 8 -- an in-force cell is not charged again for acquisition


def test_pitfall_8_an_in_force_cell_carries_no_acquisition_charge_or_commission(
        fondsgebundene_rentenversicherung):
    """Model point 6 opens at t = 97: the charge and the commission are both behind it.

    That is the whole of the difference between an in-force cell and a new-business one on
    this chassis, and it is why ``t`` counts policy months from inception rather than from
    the valuation date -- one ``charge_acq_pp`` rule serves both without a duration offset.
    """
    p = fondsgebundene_rentenversicherung.Projection[6]
    assert p.duration_init_m() == 96 and p.proj_start() == 97
    assert p.result_cf().index[0] == 97
    assert p.acq_window_months() == 60          # the window is real, and already closed
    assert p.charge_acq_total() == pytest.approx(0.025 * 111000.0, rel=1e-12) == 2775.0
    assert p.result_cf()["charge_acq"].sum() == 0.0
    assert p.cum_charge_acq_pp(p.proj_len()) == 0.0
    assert p.check_acq_charge() is True
    # expense_acq_pp falls at t = 1 and only there, so this frame never sees it.
    assert p.expense_acq_pp(97) == 0.0
    assert p.expenses(97) == pytest.approx(
        p.expense_maint_pp(97) * p.pols_if(97)
        + 0.015 * p.prem_pp(97) * p.pols_if(97)
        + 150.0 * p.pols_death(97) + 50.0 * p.pols_lapse(97), rel=1e-12)
    assert p.expenses(97) < 20.0
    # The cell opens with a live fund, a real Beitragsrückgewähr base and a live risk
    # charge -- 190 units at 118.40 against 24 000,00 of premiums already paid.
    assert p.units_init() == 190.0 and p.unit_price_init() == 118.4
    assert p.av_pp(97) == pytest.approx(190.0 * 118.4, rel=1e-12) == 22496.0
    assert p.cum_prem_init() == 24000.0 and p.cum_prem_pp(96) == 24000.0
    assert p.nar_pp(97) > 0.0 and p.charge_risk(97) > 0.0
    assert all(getattr(p, c)() is True for c in CHECKS)


# ---------------------------------------------------------------------------
# Pitfall 9 -- the Beitragssumme does not follow the premiums paid


def test_pitfall_9_the_beitragssumme_is_the_premiums_payable_at_the_initial_level(
        fondsgebundene_rentenversicherung, de_frv_anchor):
    """S is invariant to lapse, to Beitragsfreistellung and to the Beitragsdynamik.

    Letting it follow the premiums actually paid would make the acquisition charge a
    function of the lapse assumption -- wrong, and circular.
    """
    p = de_frv_anchor
    assert p.beitragssumme() == pytest.approx(
        p.prem_pp_base() * (12.0 / p.prem_mode_months()) * p.prem_term_y(), rel=1e-12)
    assert p.beitragssumme() == 72000.0
    # ... and it is not the premiums the projection actually collects, which lapse eats.
    assert p.result_cf()["premiums"].sum() == pytest.approx(40586.28, abs=CENT)
    assert p.result_cf()["premiums"].sum() < 0.6 * p.beitragssumme()

    # Beitragsfreistellung at month 121 does not shrink it.
    pup = fondsgebundene_rentenversicherung.Projection[7]
    assert pup.pup_month() == 121
    assert pup.beitragssumme() == pytest.approx(250.0 * 12 * 27, rel=1e-12) == 81000.0
    assert pup.charge_acq_total() == pytest.approx(0.025 * 81000.0, rel=1e-12) == 2025.0
    assert pup.cum_charge_acq_pp(pup.proj_len()) == pytest.approx(2025.0, abs=1e-9)
    paid = sum(pup.prem_pp(t) for t in range(1, pup.proj_len() + 1))
    assert paid < pup.beitragssumme()

    # A Beitragsdynamik raises the premium and not the Beitragssumme: a real tariff
    # re-zillmers each accepted increment over its own sixty months, and an increment
    # cannot be assumed at inception.
    dyn = fondsgebundene_rentenversicherung.Projection[10]
    assert dyn.dynamik_rate() == 0.03
    assert dyn.prem_pp(1) == 150.0 and dyn.prem_pp(12) == 150.0
    assert dyn.prem_pp(13) == pytest.approx(150.0 * 1.03, rel=1e-12)
    assert dyn.prem_pp(25) == pytest.approx(150.0 * 1.03 ** 2, rel=1e-12)
    assert dyn.beitragssumme() == pytest.approx(150.0 * 12 * 39, rel=1e-12) == 70200.0
    assert dyn.charge_acq_pp(13) == pytest.approx(
        dyn.charge_acq_total() / 60.0, rel=1e-12)

    # Nor does a Zuzahlung raise it.
    topup = fondsgebundene_rentenversicherung.Projection[9]
    assert topup.topup_amount() == 20000.0
    assert topup.beitragssumme() == pytest.approx(300.0 * 12 * 32, rel=1e-12) == 115200.0


# ---------------------------------------------------------------------------
# Pitfall 10 -- Storno and Beitragsfreistellung are two different things


def test_pitfall_10_beitragsfreistellung_is_a_change_of_state_and_not_an_exit(
        fondsgebundene_rentenversicherung):
    """pols_if is continuous across month 121 while premiums step to zero.

    One is an exit paying the *Rückkaufswert*; the other a change of state paying nothing.
    Conflating them would remove the policy from the in-force at month 121 and pay it a
    surrender value it never asked for.
    """
    p = fondsgebundene_rentenversicherung.Projection[7]
    assert p.premiums(120) > 0.0 and p.premiums(121) == 0.0
    # The in-force count steps by the ordinary monthly decrement and by nothing else.
    step = p.pols_if(120) / p.pols_if(121)
    ordinary = 1.0 / ((1.0 - p.mort_rate_mth(120)) * (1.0 - p.lapse_rate_mth(120)))
    assert step == pytest.approx(ordinary, rel=1e-12)
    assert p.pols_if(121) / p.pols_if(120) == pytest.approx(
        p.pols_if(122) / p.pols_if(121), rel=1e-3)
    # No benefit is paid at the paid-up month.
    assert p.claims(121, "LAPSE") == pytest.approx(
        p.pols_lapse(121) * p.av_pp_at(121, "BEF_DECR"), rel=1e-12)
    assert p.pols_lapse(121) > 0.0                # lapse continues, unrelated to the pup
    assert p.pols_maturity(121) == 0.0
    # Beitragsfreistellung is a model point election, not a cohort decrement: exactly one
    # shipped point carries it, and there is no paid-up rate anywhere in the model.
    table = fondsgebundene_rentenversicherung.Data.model_point_table()
    assert (table["pup_month"] > 0).sum() == 1
    assert table.loc[1, "pup_month"] == 0
    names = set(fondsgebundene_rentenversicherung.Projection.cells) | set(
        fondsgebundene_rentenversicherung.Projection.refs)
    for absent in ("pup_rate", "pols_pup", "paid_up_rate", "pols_paidup"):
        assert absent not in names, absent


# ---------------------------------------------------------------------------
# Pitfall 11 -- the Rückkaufswert is the Fondsguthaben


def test_pitfall_11_the_surrender_value_is_the_fund_and_nothing_else(
        fondsgebundene_rentenversicherung, de_frv_anchor):
    """claims_lapse = pols_lapse x av_pp_at(t, "BEF_DECR") exactly, wherever sigma = 0.

    § 169 VVG sends a fondsgebundene contract to the *Zeitwert*, and on a pure unit-linked
    contract the *Zeitwert* is the fund: no discounting, no *Rechnungszins*, no mortality
    basis, no *Zillmerung* residue, no second-basis *Mindestrückkaufswert*.
    """
    p = de_frv_anchor
    assert p.stornoabzug_rate() == 0.0
    for t in (1, 12, 61, 240, 359):
        assert p.claims(t, "LAPSE") == pytest.approx(
            p.pols_lapse(t) * p.av_pp_at(t, "BEF_DECR"), rel=1e-12)
    # The value is positive from the first month, because the acquisition charge is
    # spread rather than taken up front.
    assert p.av_pp_at(1, "BEF_DECR") > 0.0
    assert p.claims(1, "LAPSE") > 0.0
    names = set(fondsgebundene_rentenversicherung.Projection.cells) | set(
        fondsgebundene_rentenversicherung.Projection.refs)
    for absent in ("disc_factor", "tech_rate", "rechnungszins", "deckungskapital",
                   "min_surr_value_pp", "zillmer_rate", "surr_value_pp",
                   "paid_up_factor", "asset_share", "mvr"):
        assert absent not in names, absent
    # In the last month a surrender and an annuitisation are the same event, so the
    # convention books the whole surviving cohort as maturity and no cash flow moves.
    n = p.proj_len()
    assert p.lapse_rate_base(n) > 0.0 and p.lapse_rate_mth(n) == 0.0
    assert p.pols_lapse(n) == 0.0
    assert p.claims(n, "LAPSE") == 0.0
    assert p.pols_maturity(n) == pytest.approx(p.pols_if_at(n, "AFT_DECR"), rel=1e-15)


# ---------------------------------------------------------------------------
# Pitfall 12 -- the Stornoabzug is not built out of unamortised acquisition cost


def test_pitfall_12_the_stornoabzug_is_a_flat_rate_on_the_fund(
        fondsgebundene_rentenversicherung):
    """sigma x pols_lapse x av, and never a function of the unrecovered charge.

    § 169 VVG makes a deduction for *noch nicht getilgte Abschluss- und Vertriebskosten*
    ineffective, which is precisely what stops an insurer recovering through the deduction
    what the five-year spreading denies it.  Model point 5 is the only shipped cell with a
    non-zero rate.
    """
    p = fondsgebundene_rentenversicherung.Projection[5]
    assert p.charge_id() == "std_high" and p.stornoabzug_rate() == 0.02
    for t in (1, 13, 60, 240):
        assert p.stornoabzug_pp(t) == pytest.approx(
            0.02 * p.av_pp_at(t, "BEF_DECR"), rel=1e-12)
        assert p.stornoabzug(t) == pytest.approx(
            0.02 * p.pols_lapse(t) * p.av_pp_at(t, "BEF_DECR"), rel=1e-12)
        assert p.claims(t, "LAPSE") == pytest.approx(
            p.pols_lapse(t) * p.av_pp_at(t, "BEF_DECR") * 0.98, rel=1e-12)
    # It rises with the fund, while the unrecovered acquisition charge falls to zero --
    # so the deduction cannot be a function of it.
    unrecovered_13 = p.charge_acq_total() - p.cum_charge_acq_pp(13)
    unrecovered_240 = p.charge_acq_total() - p.cum_charge_acq_pp(240)
    assert unrecovered_13 > 0.0 and unrecovered_240 == 0.0
    assert p.stornoabzug_pp(240) > p.stornoabzug_pp(13)
    # The deduction is income to the insurer and part of the fund released at the same
    # time, which is why it appears on both sides of the funding identity.
    assert p.result_cf()["stornoabzug"].sum() == pytest.approx(853.00, abs=CENT)
    assert p.check_benefit_funding() is True
    assert p.check_net_cf() is True
    # Every other shipped tariff has none at all.
    charges = fondsgebundene_rentenversicherung.Data.charge_table()
    assert set(charges.index) == {"std_gross", "std_netto", "std_high", "std_low"}
    assert (charges["stornoabzug_rate"] > 0).sum() == 1
    assert float(charges.loc["std_gross", "stornoabzug_rate"]) == 0.0


# ---------------------------------------------------------------------------
# Pitfall 13 -- no account-value benefit is booked as an insurer outgo


def test_pitfall_13_the_fund_is_not_booked_as_an_insurer_outgo(de_frv_anchor):
    """net_cf is the non-unit stream; the fund is the policyholder's money passing through.

    This is the product's first-order failure mode: booking the whole *Fondsguthaben* as
    an outgo leaves every column in the frame looking reasonable and overstates the
    liability by the entire fund -- 64 865 EUR against a true insurer cost of 4,39 EUR on
    this cell.
    """
    p = de_frv_anchor
    df = p.result_cf()
    assert p.check_net_cf() is True
    assert p.check_benefit_funding() is True
    for t in (1, 61, 240, 360):
        rebuilt = (p.charge_acq(t) + p.charge_admin_prem(t) + p.charge_admin_fund(t)
                   + p.charge_policy_fee(t) + p.charge_risk(t) + p.stornoabzug(t)
                   - p.expenses(t) - p.death_strain(t))
        assert p.net_cf(t) == pytest.approx(rebuilt, rel=1e-12, abs=1e-9)
        funded = (p.claims(t, "DEATH") + p.claims(t, "LAPSE") + p.claims(t, "MATURITY")
                  + p.withdrawals(t) + p.stornoabzug(t))
        assert funded == pytest.approx(p.av_releases(t) + p.death_strain(t), abs=1e-8)
    # The maturity month is where the difference is loudest: 39 298,91 of claims and a
    # net_cf of -20,27, because none of the capital is an insurer cost.
    assert df.loc[360, "claims_maturity"] == pytest.approx(39298.91, abs=CENT)
    assert df.loc[360, "net_cf"] == pytest.approx(-20.27, abs=CENT)
    assert abs(df["net_cf"].sum()) < 0.05 * df["av_releases"].sum()
    # death_strain is the only benefit component that crosses the boundary.
    assert df["death_strain"].sum() == pytest.approx(4.39, abs=CENT)
    assert df["death_strain"].sum() < 0.0002 * df["claims_death"].sum() * 100


# ---------------------------------------------------------------------------
# Pitfall 14 -- the age at Rentenbeginn is not off by one


def test_pitfall_14_the_rentenfaktor_is_read_at_the_annuity_age(
        fondsgebundene_rentenversicherung, de_frv_anchor):
    """age(proj_len()) is annuity_age - 1, because the annuity begins at the month's end.

    The off-by-one would fetch 24.449878 at age 66 instead of 25.00 at 67 and understate
    the pension by 2.2 %.
    """
    p = de_frv_anchor
    n = p.proj_len()
    assert n == 12 * (67 - 37) == 360
    assert p.age(n) == 66 == p.annuity_age() - 1
    assert p.policy_year(n) == 30
    assert p.rentenfaktor_guar() == 25.0

    table = fondsgebundene_rentenversicherung.Data.rentenfaktor_table()
    off_by_one = float(table.loc[("std_2026", 66), "rentenfaktor_guar"])
    assert off_by_one == pytest.approx(24.449878, abs=5e-7)
    assert p.annuity_mth_pp() == pytest.approx(324.25, abs=CENT)
    wrong = p.av_maturity_pp() / 10000.0 * off_by_one
    assert wrong == pytest.approx(317.11, abs=CENT)
    assert 1.0 - wrong / p.annuity_mth_pp() == pytest.approx(0.022, abs=0.0005)
    # The derivation the [std] table carries: 10 000 / (12 T_eff), T_eff(67) = 100/3.
    assert 10000.0 / (12.0 * (100.0 / 3.0)) == pytest.approx(25.0, rel=1e-12)
    assert float(table.loc[("std_2026", 62), "rentenfaktor_guar"]) == pytest.approx(
        10000.0 / (400.0 - 9.0 * (62 - 67)), abs=5e-7)


# ---------------------------------------------------------------------------
# Pitfall 15 -- the Rentenfaktor rule is a maximum of two


def test_pitfall_15_the_applied_factor_is_the_higher_of_guaranteed_and_current(
        fondsgebundene_rentenversicherung, de_frv_anchor):
    """max(guaranteed, current): a guarantee with upside, not a ceiling.

    On ``std_2026`` the two are equal, so the max() is exercised without injecting an
    unsourced uplift; model point 13 carries ``rich_current``, 12 % higher, where it
    visibly bites -- and a model applying only the guaranteed factor would understate that
    cell's pension by the whole 12 %.
    """
    p = de_frv_anchor
    assert p.rentenfaktor_guar() == p.rentenfaktor_curr() == 25.0
    assert p.rentenfaktor_applied() == pytest.approx(
        max(p.rentenfaktor_guar(), p.rentenfaktor_curr()), rel=1e-15)

    rich = fondsgebundene_rentenversicherung.Projection[13]
    assert rich.rentenfaktor_id() == "rich_current" and rich.annuity_age() == 70
    assert rich.rentenfaktor_guar() == pytest.approx(26.809651, abs=5e-7)
    assert rich.rentenfaktor_curr() == pytest.approx(30.026809, abs=5e-7)
    assert rich.rentenfaktor_curr() / rich.rentenfaktor_guar() == pytest.approx(
        1.12, abs=5e-8)
    assert rich.rentenfaktor_applied() == rich.rentenfaktor_curr()
    assert rich.rentenfaktor_applied() > rich.rentenfaktor_guar()
    assert rich.annuity_mth_pp() == pytest.approx(
        rich.av_maturity_pp() / 10000.0 * rich.rentenfaktor_curr(), rel=1e-12)
    assert rich.annuity_mth_pp() == pytest.approx(476.24, abs=CENT)
    guaranteed_only = rich.av_maturity_pp() / 10000.0 * rich.rentenfaktor_guar()
    assert rich.annuity_mth_pp() / guaranteed_only == pytest.approx(1.12, abs=5e-8)
    # The Kapitalwahlrecht is a reporting split and moves no cash flow: both routes
    # release the same Fondsguthaben from this model.
    assert rich.kapitalwahl() is True
    assert rich.claims(rich.proj_len(), "MATURITY") == pytest.approx(
        rich.pols_maturity(rich.proj_len()) * rich.av_maturity_pp(), rel=1e-12)


# ---------------------------------------------------------------------------
# Pitfall 16 -- the Ratenzahlungszuschlag is not applied twice


def test_pitfall_16_the_stated_instalment_is_not_loaded_again(
        fondsgebundene_rentenversicherung, de_frv_anchor):
    """premiums(t) = prem_pp x pols_if(t) in a premium month, and 0.00 in between.

    ``prem_pp_base`` already contains whatever *Ratenzahlungszuschlag* the tariff applied
    for paying more often than annually, so loading it again would charge the fractionation
    twice.  There is no frequency-loading cells in this model, and that is deliberate.
    """
    p = de_frv_anchor
    for t in (1, 12, 61, 360):
        assert p.premiums(t) == pytest.approx(p.prem_pp(t) * p.pols_if(t), rel=1e-12)
        assert p.prem_pp(t) == pytest.approx(p.prem_pp_base(), rel=1e-12)

    for point_id, (mode, amount) in {3: (3, 600.0), 4: (6, 1200.0),
                                     5: (12, 3000.0)}.items():
        q = fondsgebundene_rentenversicherung.Projection[point_id]
        assert q.prem_mode_months() == mode
        assert q.prem_pp(1) == pytest.approx(amount, abs=CENT)
        assert q.premiums(1) == pytest.approx(amount * q.pols_if(1), rel=1e-12)
        # The intervening months carry nothing at all -- not a twelfth, not a loading.
        for offset in range(1, mode):
            assert q.prem_pp(1 + offset) == 0.0
            assert q.premiums(1 + offset) == 0.0
            assert q.charge_admin_prem(1 + offset) == 0.0
            assert q.charge_acq(1 + offset) == 0.0
        assert q.prem_pp(1 + mode) == pytest.approx(amount, abs=CENT)

    names = set(fondsgebundene_rentenversicherung.Projection.cells) | set(
        fondsgebundene_rentenversicherung.Projection.refs)
    for absent in ("prem_freq_load", "prem_freq_fee", "freq_loading_table",
                   "ratenzahlungszuschlag", "prem_tariff_pp"):
        assert absent not in names, absent


# ---------------------------------------------------------------------------
# Pitfall 17 -- the Beitragsrückgewähr base is the premiums paid


def test_pitfall_17_the_death_benefit_floor_is_the_premiums_paid_not_invested(
        de_frv_anchor):
    """cum_prem_pp(60) = 12 000,00 against 9 720,00 actually put into units.

    Reading the floor off the invested amount would understate the death benefit by 19 %
    over the whole of the acquisition window, which is exactly where the net amount at
    risk is largest.
    """
    p = de_frv_anchor
    assert p.cum_prem_pp(60) == pytest.approx(60 * 200.0, rel=1e-12) == 12000.0
    invested = sum(p.prem_to_av_pp(t) for t in range(1, 61))
    assert invested == pytest.approx(60 * 162.0, rel=1e-12) == 9720.0
    assert 1.0 - invested / p.cum_prem_pp(60) == pytest.approx(0.19, abs=0.0005)
    assert p.db_floor_pp(60) == pytest.approx(p.cum_prem_pp(60), rel=1e-15)
    assert p.db_form() == "prem_return"
    # It is a state variable, seeded from the model point and rolled forward gross.
    assert p.cum_prem_init() == 0.0
    for t in (1, 61, 240, 360):
        assert p.cum_prem_pp(t) == pytest.approx(
            p.cum_prem_pp(t - 1) + p.prem_pp(t) + p.topup_pp(t), rel=1e-12)
    assert p.cum_prem_pp(360) == pytest.approx(72000.0, rel=1e-12)
    # And what a death actually pays is the closing fund plus the amount at risk, so the
    # two sides of the benefit stay separable.
    for t in (1, 60, 94, 240):
        assert p.db_pp(t) == pytest.approx(
            p.av_pp_at(t, "BEF_DECR") + p.nar_pp(t), rel=1e-12)
        assert p.claims(t, "DEATH") == pytest.approx(
            p.pols_death(t) * p.db_pp(t), rel=1e-12)


# ---------------------------------------------------------------------------
# Pitfall 18 -- no fixed charge drives the fund negative


def test_pitfall_18_no_balance_goes_negative_and_no_floor_is_triggered(
        fondsgebundene_rentenversicherung, de_frv_anchor):
    """Every within-month balance is non-negative, and no shipped cell hits a floor.

    The ``min(.., remaining)`` guards on the *Stückkosten* and the *Risikobeitrag* are
    **[std]** safeguards rather than tariff terms; a contract that triggered one would in
    practice have had its cover terminated.  Model point 7 is the hardest case -- a
    decaying paid-up fund on a zero-return path with a fixed *garantierte
    Mindesttodesfallleistung*, so the amount at risk grows as the fund falls.
    """
    timings = ("BEF_CHARGE", "AFT_CHARGE", "AFT_WD", "BEF_DECR")
    p = de_frv_anchor
    for t in range(1, p.proj_len() + 1, 17):
        for timing in timings:
            assert p.av_pp_at(t, timing) >= 0.0, (t, timing)
        assert p.charge_policy_fee_pp(t) == pytest.approx(3.0, rel=1e-12)

    hard = fondsgebundene_rentenversicherung.Projection[7]
    assert hard.db_form() == "sum_assured" and hard.sum_assured() == 40000.0
    assert hard.scenario_id() == "zero"
    for t in range(hard.proj_start(), hard.proj_len() + 1, 11):
        for timing in timings:
            assert hard.av_pp_at(t, timing) >= 0.0, (t, timing)
        assert hard.charge_policy_fee_pp(t) == pytest.approx(3.0, rel=1e-12)
        assert hard.charge_risk_pp(t) == pytest.approx(
            hard.mort_rate_tariff_mth(t) * hard.nar_pp(t), rel=1e-12)
    # The feedback the notes describe: the fund falls, so the amount at risk rises, so the
    # risk charge rises, so the fund falls faster.  It is a product risk, not an artefact.
    assert hard.nar_pp(324) > hard.nar_pp(121)
    assert hard.charge_risk_pp(324) > hard.charge_risk_pp(121)
    assert hard.av_maturity_pp() > 0.0
    assert all(getattr(hard, c)() is True for c in CHECKS)


# ---------------------------------------------------------------------------
# The published identities


def test_the_seven_checks_hold_and_their_residuals_are_zero(de_frv_anchor):
    """Each check is a bool over all t; each residual is zero at every month sampled."""
    p = de_frv_anchor
    for name in CHECKS:
        assert getattr(p, name)() is True, name
        resid = getattr(p, name + "_resid")
        for t in (1, 2, 60, 61, 120, 240, 301, 359, 360):
            assert abs(resid(t)) < 1e-8, (name, t)


def test_check_net_cf_is_delib_ruling_one_and_crosses_the_unit_boundary(de_frv_anchor):
    """The residual rebuilds the premium-side charges as premiums - prem_to_av.

    That is a different route from the formula ``net_cf`` uses, which is what makes the
    check a check rather than a restatement: it closes the *Beitragsverrechnung* and the
    cash flow statement against each other in one line.
    """
    p = de_frv_anchor
    for t in (1, 2, 61, 240, 360):
        withheld = p.premiums(t) - p.prem_to_av(t)
        assert withheld == pytest.approx(
            p.charge_acq(t) + p.charge_admin_prem(t), abs=1e-9)
        rebuilt = (withheld + p.charge_admin_fund(t) + p.charge_policy_fee(t)
                   + p.charge_risk(t) + p.stornoabzug(t)
                   - p.expenses(t) - p.death_strain(t))
        assert p.check_net_cf_resid(t) == pytest.approx(
            p.net_cf(t) - rebuilt, abs=1e-12)
        assert abs(p.check_net_cf_resid(t)) < 1e-9
    assert p.check_net_cf() is True
    assert p.check_prem_split() is True


def test_the_unit_and_account_identities_are_not_redundant(de_frv_anchor):
    """One has no price term and the other carries it; an implementation can pass either.

    The unit identity catches a charge taken in euro without the matching units being
    cancelled; the account identity catches the month's return applied at the wrong point
    in the order.
    """
    p = de_frv_anchor
    for t in (1, 2, 61, 240, 359):
        assert p.units_pp(t + 1) == pytest.approx(
            p.units_pp(t) + p.units_bought_pp(t) - p.units_cancelled_pp(t), abs=1e-9)
        assert p.units_cancelled_pp(t) == pytest.approx(
            (p.charge_admin_fund_pp(t) + p.charge_policy_fee_pp(t)
             + p.withdrawals_pp(t) + p.charge_risk_pp(t)) / p.unit_price(t), rel=1e-12)
        rolled = ((p.av_pp(t) + p.prem_to_av_pp(t)) * (1.0 + p.fund_return_net_mth(t))
                  - p.charge_admin_fund_pp(t) - p.charge_policy_fee_pp(t)
                  - p.withdrawals_pp(t) - p.charge_risk_pp(t))
        assert p.av_pp_at(t, "BEF_DECR") == pytest.approx(rolled, abs=1e-8)
    assert p.check_units_roll_fwd() is True
    assert p.check_av_roll_fwd() is True
    # Premium is in advance, so the month's return accrues on the units it buys.
    assert p.units_bought_pp(1) == pytest.approx(
        p.prem_to_av_pp(1) / p.unit_price(0), rel=1e-12)
    assert p.unit_price(0) == p.unit_price_init() == 100.0


def test_the_in_force_roll_forward_closes_every_month(de_frv_anchor):
    """Everyone who starts a month dies, surrenders, reaches Rentenbeginn or is still there."""
    p = de_frv_anchor
    n = p.proj_len()
    for t in (1, 61, 240, 359, 360):
        assert p.pols_if(t) == pytest.approx(
            p.pols_death(t) + p.pols_lapse(t) + p.pols_maturity(t) + p.pols_if(t + 1),
            abs=1e-12)
    assert p.check_pols_roll_fwd() is True
    assert p.pols_if(1) == p.pols_if_init() == 1.0
    assert p.pols_if_at(1, "BEF_DECR") == p.pols_if(1)
    assert p.pols_if_at(1, "AFT_DEATH") == pytest.approx(
        p.pols_if(1) * (1.0 - p.mort_rate_mth(1)), rel=1e-15)
    assert p.pols_if_at(1, "AFT_DECR") == pytest.approx(p.pols_if(2), rel=1e-15)
    assert p.pols_if_at(n, "AFT_DECR") == pytest.approx(p.pols_maturity(n), rel=1e-15)
    assert p.pols_if(n + 1) == 0.0


# ---------------------------------------------------------------------------
# The product's own invariants


def test_result_cf_shape_and_both_signs_of_the_net_flow(de_frv_anchor):
    """Eighteen columns in the notes' order, pols_if first, liability_cf last."""
    df = de_frv_anchor.result_cf()
    assert list(df.columns) == [
        "pols_if", "premiums", "prem_to_av", "charge_acq", "charge_admin_prem",
        "charge_admin_fund", "charge_policy_fee", "charge_risk", "stornoabzug",
        "withdrawals", "claims_death", "claims_lapse", "claims_maturity",
        "av_releases", "death_strain", "expenses", "net_cf", "liability_cf",
    ]
    assert df.index.name == "t"
    assert list(df.index) == list(range(1, 361))
    assert df.index[-1] == de_frv_anchor.proj_len()
    assert df["pols_if"].iloc[0] == de_frv_anchor.pols_if_init()
    # A cash flow statement must not publish its own subtotal beside its parts.
    assert "claims" not in df.columns
    for retired in ("claims_surr", "claims_wd", "claims_commute", "av", "charge_ter"):
        assert retired not in df.columns, retired
    assert (df["net_cf"] + df["liability_cf"]).abs().max() == pytest.approx(0.0, abs=1e-12)
    # Large new-business strain in month 1, then a thin positive margin that grows.
    assert df["net_cf"].iloc[0] == pytest.approx(-1966.22, abs=CENT)
    assert (df["net_cf"].iloc[1:120] > 0).all()
    assert df.loc[240, "net_cf"] > df.loc[120, "net_cf"]


def test_result_fund_publishes_the_standmitteilung_state_vector(de_frv_anchor):
    """The per-policy frame a German annual statement's line items map onto."""
    df = de_frv_anchor.result_fund()
    assert list(df.columns) == [
        "unit_price", "units_pp", "av_pp", "av_pp_bef_charge", "av_pp_aft_charge",
        "av_pp_aft_wd", "av_pp_bef_decr", "cum_prem_pp", "db_floor_pp", "nar_pp",
        "mort_rate_mth", "mort_rate_tariff_mth", "lapse_rate_mth",
    ]
    assert df.index.name == "t"
    assert list(df.index) == list(range(1, 361))
    assert (df["units_pp"] >= 0.0).all()
    assert (df["nar_pp"] >= 0.0).all()
    assert (df["mort_rate_tariff_mth"] > df["mort_rate_mth"]).all()
    assert df["unit_price"].is_monotonic_increasing


def test_the_behaviour_modules_are_off_and_reachable(
        fondsgebundene_rentenversicherung, de_frv_anchor):
    """Base-run values, so the worked example reproduces with the machinery still there."""
    proj = fondsgebundene_rentenversicherung.Projection
    assert proj.lapse_dyn_beta == 0.0
    assert proj.lapse_cap == 0.4
    assert proj.mort_be_factor == 0.75
    assert proj.mmkt_return_ann == 0.015 and proj.glide_months == 60
    p = de_frv_anchor
    assert all(p.lapse_dyn_add(t) == 0.0 for t in (1, 61, 240, 360))
    assert all(p.lapse_rate(t) == pytest.approx(
        p.lapse_rate_base(t) * p.lapse_tax_step(t), rel=1e-12)
        for t in (1, 61, 301))
    assert p.ablauf_flag() is False
    assert all(p.fund_return_gross_ann(t) == 0.05 for t in (1, 300, 360))
    # No Überschussbeteiligung credit anywhere: the omission is stated, not hidden.
    names = set(proj.cells) | set(proj.refs)
    for absent in ("surplus_rate", "bonus_rate", "ueberschuss_pp", "schlussueberschuss",
                   "rfb_rate", "surplus_units_pp"):
        assert absent not in names, absent


def test_the_ablaufmanagement_glide_bites_only_in_the_last_sixty_months(
        fondsgebundene_rentenversicherung):
    """Model point 8 switches it on: a linear ramp of the gross return to 1.50 % p.a.

    With one fund and a deterministic return a reallocation and a change of assumed return
    are the same thing, which is why it is represented this way and why the model cannot
    show dispersion between funds.
    """
    p = fondsgebundene_rentenversicherung.Projection[8]
    assert p.ablauf_flag() is True and p.proj_len() == 240
    assert p.fund_return_gross_ann(180) == 0.05        # 60 months remaining
    assert p.fund_return_gross_ann(181) < 0.05         # the ramp starts
    assert p.fund_return_gross_ann(240) == pytest.approx(0.015, rel=1e-12)
    step = (0.05 - 0.015) / 60.0
    assert p.fund_return_gross_ann(181) == pytest.approx(0.05 - step, rel=1e-9)
    assert p.fund_return_gross_ann(210) == pytest.approx(0.0325, abs=5e-7)
    # The TER is untouched by the glide: it is a fund cost, not a return assumption.
    assert p.fund_ter_ann(240) == pytest.approx(p.fund_ter_ann(1), rel=1e-15)
    assert all(getattr(p, c)() is True for c in CHECKS)
    # Every other shipped point leaves it off.
    table = fondsgebundene_rentenversicherung.Data.model_point_table()
    assert table["ablauf_flag"].sum() == 1


def test_the_topup_and_the_teilentnahme_move_the_fund_and_the_floor(
        fondsgebundene_rentenversicherung):
    """A Zuzahlung buys units and raises the Beitragsrückgewähr base; a Teilentnahme is
    an owner election settled by cancelling units, published as withdrawals and never as
    a claim."""
    p = fondsgebundene_rentenversicherung.Projection[9]
    assert p.topup_month() == 121 and p.wd_month() == 241
    assert p.topup_pp(121) == 20000.0 and p.topup_pp(122) == 0.0
    assert p.prem_to_av_pp(121) == pytest.approx(
        p.prem_pp(121) + 20000.0 - 500.0 - 0.04 * p.prem_pp(121), rel=1e-12)
    assert p.cum_prem_pp(121) - p.cum_prem_pp(120) == pytest.approx(
        p.prem_pp(121) + 20000.0, rel=1e-12)
    assert p.av_pp_at(121, "BEF_DECR") > p.av_pp_at(120, "BEF_DECR") + 19000.0

    assert p.withdrawals_pp(241) == 15000.0 and p.withdrawals_pp(242) == 0.0
    assert p.withdrawals(241) == pytest.approx(15000.0 * p.pols_if(241), rel=1e-12)
    assert p.av_pp_at(241, "AFT_WD") == pytest.approx(
        p.av_pp_at(241, "AFT_CHARGE") - 15000.0, rel=1e-12)
    assert p.av_pp_at(241, "BEF_DECR") < p.av_pp_at(240, "BEF_DECR")
    # It is not a claim, and it is outside net_cf altogether.
    df = p.result_cf()
    assert df.loc[241, "claims_death"] >= 0.0
    assert "claims_wd" not in df.columns
    assert df["withdrawals"].sum() == pytest.approx(15000.0 * p.pols_if(241), rel=1e-12)
    assert all(getattr(p, c)() is True for c in CHECKS)


def test_the_stress_path_puts_the_fund_below_the_premiums_paid(
        fondsgebundene_rentenversicherung):
    """Model point 12: -20 % in year 1, a two-year premium term, a pct_fund death benefit.

    A `pct_fund` floor is a multiple of the fund, so the net amount at risk grows with the
    fund instead of vanishing -- the opposite behaviour from the *Beitragsrückgewähr* --
    which is why the cell exists beside the anchor.
    """
    p = fondsgebundene_rentenversicherung.Projection[12]
    assert p.scenario_id() == "stress" and p.db_form() == "pct_fund"
    assert p.db_pct() == 1.1
    assert p.fund_return_gross_ann(1) == pytest.approx(-0.20, rel=1e-12)
    assert p.fund_return_gross_ann(13) == pytest.approx(0.05, rel=1e-12)
    assert p.unit_price(12) < p.unit_price(0)
    assert p.av_pp_at(12, "BEF_DECR") < p.cum_prem_pp(12)
    for t in (1, 24, 144):
        assert p.db_floor_pp(t) == pytest.approx(
            1.1 * p.av_pp_at(t, "AFT_WD"), rel=1e-12)
        assert p.nar_pp(t) == pytest.approx(
            0.1 * p.av_pp_at(t, "AFT_WD"), rel=1e-9)
    assert p.result_cf()["charge_risk"].sum() > 0.0
    assert all(getattr(p, c)() is True for c in CHECKS)


def test_the_dynamic_lapse_module_bites_where_the_fund_is_under_water():
    """Switched on, the addition raises the lapse rate while the fund is below premiums.

    Off in the base run, because no German calibration for a coefficient of any size
    exists in this corpus.  It bites hardest on model point 12, whose stress path leaves
    the fund far below the premiums paid for years.
    """
    model = mx.read_model(MODEL_DIR, name="FRV_DE_S_dynlapse")
    try:
        model.Projection.lapse_dyn_beta = 0.15
        model.Projection.clear_all()
        p = model.Projection[12]
        assert p.av_pp(13) < p.cum_prem_pp(13)
        assert p.lapse_dyn_add(13) == pytest.approx(
            0.15 * (1.0 - p.av_pp(13) / p.cum_prem_pp(13)), rel=1e-12)
        assert p.lapse_dyn_add(13) > 0.0
        assert p.lapse_rate(13) > p.lapse_rate_base(13)
        assert p.lapse_rate(13) <= model.Projection.lapse_cap
        assert p.lapse_rate_mth(p.proj_len()) == 0.0
        assert p.check_pols_roll_fwd() is True
        assert p.check_net_cf() is True
        # Once the fund overtakes the premiums paid the addition switches itself off.
        late = p.proj_len()
        assert p.av_pp(late) > p.cum_prem_pp(late)
        assert p.lapse_dyn_add(late) == 0.0
    finally:
        model.close()


def test_invalid_enum_values_raise(de_frv_anchor):
    """The enum accessors validate rather than propagating a typo into a lookup."""
    with pytest.raises(FormulaError):
        de_frv_anchor.claims(1, "SURRENDER")
    with pytest.raises(FormulaError):
        de_frv_anchor.av_pp_at(1, "AFTER_CHARGE")
    with pytest.raises(FormulaError):
        de_frv_anchor.pols_if_at(1, "AFTER_DECR")


def test_the_shipped_tables_mark_their_own_provenance():
    """Six CSVs beside run.py, each saying what it is and -- for two of them -- what it is not.

    The mortality table is a **[std]** proxy anchored at ``q(37) = 0.00080``, the value the
    worked example rests on, and the *Rentenfaktor* table is derived rather than observed:
    DAV 2008 T and DAV 2004 R are cited by name and never shipped.  ``model_point_table.csv``
    is the library's one provenance-exempt input, because a model point is a configuration
    and not an assumption.
    """
    import pandas as pd

    assert CSV_FILES == {p.name for p in INPUT_DIR.iterdir() if p.suffix == ".csv"}

    mort = pd.read_csv(INPUT_DIR / "mort_table.csv", index_col="age")
    assert list(mort.index) == list(range(18, 101))
    assert all(p.startswith("[std]") for p in mort["provenance"])
    assert all("DAV 2008 T" in p for p in mort["provenance"])
    assert float(mort.loc[37, "qx_tariff"]) == 0.00080
    assert float(mort.loc[38, "qx_tariff"]) / float(mort.loc[37, "qx_tariff"]) == (
        pytest.approx(1.10, rel=1e-9))
    assert mort["qx_tariff"].max() <= 1.0

    lapse = pd.read_csv(INPUT_DIR / "lapse_table.csv", index_col="policy_year")
    assert [float(lapse.loc[y, "lapse_rate"]) for y in (1, 5, 6, 10, 11, 12, 13)] == [
        0.06, 0.06, 0.03, 0.03, 0.02, 0.02, 0.03]
    assert all("[std]" in p and "Stornoquote" in p for p in lapse["provenance"])

    charges = pd.read_csv(INPUT_DIR / "charge_table.csv", index_col="charge_id")
    assert float(charges.loc["std_gross", "alpha_rate"]) == 0.025
    assert int(charges.loc["std_gross", "alpha_spread_months"]) == 60
    assert float(charges.loc["std_netto", "alpha_rate"]) == 0.0
    assert "Hoechstzillmersatz" in charges.loc["std_gross", "provenance"]
    assert all("[std]" in p for p in charges["provenance"])

    funds = pd.read_csv(INPUT_DIR / "fund_scenario_table.csv")
    assert set(funds["scenario_id"]) == {"base", "etf", "zero", "stress"}
    assert all("[std]" in p for p in funds["provenance"])
    assert all("PRIIPs performance scenario" in p or "not a PRIIPs" in p
               for p in funds[funds["scenario_id"] == "base"]["provenance"])

    factors = pd.read_csv(INPUT_DIR / "rentenfaktor_table.csv")
    assert set(factors["factor_id"]) == {"std_2026", "rich_current"}
    assert all("[std]" in p for p in factors["provenance"])
    assert all("derived not observed" in p or "guaranteed factor as std_2026" in p
               for p in factors["provenance"])

    points = pd.read_csv(INPUT_DIR / "model_point_table.csv", index_col="point_id")
    assert len(points) == 13
    assert "provenance" not in points.columns      # the one exemption
    assert points.loc[1, "policy_id"] == "DE-FRV-0001"


def test_an_input_can_be_swapped_without_touching_formulas():
    """What a production user does with a real tariff or a licensed mortality basis."""
    import pandas as pd

    lighter = pd.read_csv(INPUT_DIR / "mort_table.csv", index_col="age")
    lighter["qx_tariff"] = lighter["qx_tariff"] * 0.5

    model = mx.read_model(MODEL_DIR, name="FRV_DE_S_swap")
    try:
        alt_name = "mort_table_light.csv"
        lighter.to_csv(model.Data.input_dir() / alt_name)
        try:
            base = model.Projection[1].result_cf()
            assert base["charge_risk"].sum() == pytest.approx(5.85, abs=CENT)
            model.Data.mort_file = alt_name
            model.Data.clear_all()
            model.Projection.clear_all()
            swapped = model.Projection[1].result_cf()
            # Half the tariff rate: half the risk charge and half the decrement, so more
            # policies persist and more charges are collected.
            assert swapped["charge_risk"].sum() == pytest.approx(
                0.5 * 5.85, abs=0.02)
            assert swapped["pols_if"].sum() > base["pols_if"].sum()
            assert model.Projection[1].check_net_cf() is True
        finally:
            (model.Data.input_dir() / alt_name).unlink(missing_ok=True)
    finally:
        model.close()


def test_docstrings_describe_the_current_structure(fondsgebundene_rentenversicherung):
    """Specifics a reader would rely on, asserted so they cannot go stale silently."""
    doc = fondsgebundene_rentenversicherung.doc
    assert "fondsgebundene Rentenversicherung" in doc
    assert "mechanics demonstration" in doc
    assert "external" in doc                       # inputs are not stored in the model
    assert "once per model" in doc                 # why Data exists
    assert "Rentenfaktor" in doc and "Beitragsverrechnung" in doc
    assert "sofortrente" in doc                    # where the payout phase lives
    proj = fondsgebundene_rentenversicherung.Projection.doc
    assert "Notes symbol" in proj
    for cells in ("proj_len", "model_point", "units_pp", "av_pp_at", "nar_pp",
                  "charge_acq_pp", "rentenfaktor_guar", "lapse_tax_step",
                  "reduction_in_yield"):
        assert cells in proj, cells
    data = fondsgebundene_rentenversicherung.Data.doc
    assert "TradLife_A" in data
    assert "provenance" in data
    for cells in ("input_dir", "model_point_table", "mort_table",
                  "rentenfaktor_table"):
        assert cells in data, cells


def test_the_unit_linked_chassis_vocabulary_is_present(fondsgebundene_rentenversicherung):
    """Names this model shares with frlib's UC_FR_S and with the library's own register."""
    shared = {
        "model_point", "proj_len", "proj_start", "age", "policy_year",
        "pols_if", "pols_if_at", "pols_if_init", "pols_death", "pols_lapse",
        "pols_maturity", "mort_rate", "mort_rate_mth", "lapse_rate", "lapse_rate_mth",
        "units_pp", "units_bought_pp", "units_cancelled_pp", "unit_price",
        "av_pp", "av_pp_at", "av_at", "prem_to_av_pp", "prem_to_av", "premiums",
        "nar_pp", "db_pp", "claims", "withdrawals", "av_releases", "death_strain",
        "expenses", "net_cf", "liability_cf", "result_cf",
    }
    names = set(fondsgebundene_rentenversicherung.Projection.cells) | set(
        fondsgebundene_rentenversicherung.Projection.refs)
    assert shared <= names, f"missing: {sorted(shared - names)}"
    # And the retired names the library's register forbids stay gone.
    for retired in ("lapse_rate_ann", "prem_net_pp", "mort_ae_factor", "mort_adj",
                    "mort_rate_table", "premium_net_pp", "check_pols_if", "pols_init",
                    "omega", "loan_bal", "pols_expiry", "check_cf_ledger"):
        assert retired not in names, retired
