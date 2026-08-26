"""Golden and structural tests for EC_FR_A.

The golden values are the worked example in
products/eurocroissance/technical-notes.md ("Worked example"), which is **two** model
points on one asset path: a Chassis A cell (1 deg engagement, provision mathematique plus
parts) and a Chassis B cell (2 deg engagement, parts only, guarantee at the echeance).
Both take EUR 10,000 gross at issue and EUR 2,000 gross at the end of policy year 3 with
a 2.00% entry charge, so net versements are 11,760.00; g = 100% at n = 10; male age 57;
parts levy 0.80% p.a. and performance levy 10% of positive performance; initial part
value 10.0000 and floor 5.0000; decrements switched off, so pols_if stays at 1 and the
provision path *is* the cash flow path.  The asset path is +4.00% to t = 5, **-25.00%**
at t = 6 and +6.00% after, and TEC10 is 2.50% then 1.00%, so i_pm is 2.25% then 0.90%.
Model points 1 and 2 are those two cells.

They are hard-coded here rather than pickled so that a reviewer can compare them against
the notes by eye.  Tolerances follow the precision the notes display: money to the cent,
parts and part values to four decimals.

Beyond the worked example this module asserts each product fact the notes list as a
modelling pitfall, because each is a way an implementation can look right and be wrong: a
Chassis B surrender before the echeance carries **no guarantee**; the insurer's own-funds
provisions never reach a policyholder before the term; the provision mathematique is
re-struck and never accumulated; the recurring charge is a levy in **number of parts**;
the guarantee is net of the entry charge; the part value has a contractual floor; a death
floor is a complementary guarantee funded outside the account; the maturity max(., mg)
exists only at t = n and only on Chassis B; the L. 134-3 contribution earns nothing for
the savers; one auxiliary account has one part value; and the discount rate is A. 134-1's
90%-of-TEC ceiling with a zero floor, not A. 132-1's or A. 132-3's.

The module also sweeps the whole model point table.  That sweep normally lives in
``test_model_conventions_fr.py``, which is parametrized over ``fr_registry.INPUT_FILES``;
that cannot list this model until every product in the library exists, so it is carried
here in the meantime and costs almost nothing, the module-scoped instance being warm.
"""
import shutil

import modelx as mx
import pandas as pd
import pytest
from modelx.core.errors import FormulaError

from fr_registry import MODELS, LIB


def model_files(folder):
    """The model's own file names, ignoring interpreter caches.

    ``__pycache__`` appears inside a model folder as soon as anything *imports* it, which
    is routine once the autodoc API pages have been built.  Those caches are not part of
    the model and must not make a round-trip comparison fail.
    """
    return {p.name for p in folder.rglob("*")
            if p.is_file() and "__pycache__" not in p.parts}


CENT = 0.005          # money displayed to 2 d.p.
PART = 0.00005        # parts and part values displayed to 4 d.p.

MODEL_DIR = LIB / MODELS["EC_FR_A"][0]

# Chassis A, the notes' first table.
# t: (parts levy, own assets A, pm, prov_div, parts, part value, C, surrender value)
WORKED_A = {
    0:  (0.00, 9800.00, 7845.00, 1955.00, 195.5001, 10.0000, 0.00, 9800.00),
    1:  (15.64, 10136.60, 8021.51, 2115.09, 193.9361, 10.9061, 0.00, 10136.60),
    2:  (16.92, 10483.98, 8202.00, 2281.99, 192.3846, 11.8616, 0.00, 10483.98),
    3:  (18.26, 12802.49, 10063.85, 2738.65, 212.8127, 12.8688, 0.00, 12802.49),
    4:  (21.91, 13240.69, 10290.29, 2950.40, 211.1102, 13.9756, 0.00, 13240.69),
    5:  (23.60, 13692.90, 10521.82, 3171.08, 209.4213, 15.1421, 0.00, 13692.90),
    6:  (25.37, 10250.65, 11346.00, 1038.73, 207.7460, 5.0000, 2134.08, 12384.73),
    7:  (8.31, 10795.42, 11448.11, 1030.42, 206.0840, 5.0000, 1683.11, 12478.53),
    8:  (8.24, 11369.69, 11551.14, 1022.18, 204.4353, 5.0000, 1203.63, 12573.32),
    9:  (8.18, 11975.03, 11655.10, 1014.00, 202.7998, 5.0000, 694.07, 12669.10),
    10: (8.11, 12613.13, 11760.00, 1005.89, 201.1774, 5.0000, 152.75, 12765.89),
}

# Chassis B, the notes' second table.  pm is identically 0, so prov_div is the assets.
# t: (parts levy, prov_div = own assets, parts, part value, pgt)
WORKED_B = {
    0:  (0.00, 9800.00, 980.0000, 10.0000, 0.00),
    1:  (78.40, 10071.58, 972.1600, 10.3600, 0.00),
    2:  (80.57, 10350.68, 964.3827, 10.7330, 0.00),
    3:  (82.81, 12597.52, 1132.9370, 11.1193, 0.00),
    4:  (100.78, 12946.62, 1123.8735, 11.5196, 0.00),
    5:  (103.57, 13305.40, 1114.8825, 11.9344, 0.00),
    6:  (106.44, 9899.22, 1105.9635, 8.9508, 1446.78),
    7:  (79.19, 10350.30, 1097.1158, 9.4341, 1097.81),
    8:  (82.80, 10821.95, 1088.3388, 9.9435, 729.20),
    9:  (86.58, 11315.08, 1079.6321, 10.4805, 340.02),
    10: (90.52, 11830.69, 1070.9951, 11.0464, 0.00),
}

# The notes state these separately, t = 1 to 10.
PERF_LEVY_A = [39.14, 40.48, 41.86, 51.12, 52.87, 0.00, 61.45, 64.72, 68.17, 71.80]
PERF_LEVY_B = [38.89, 39.96, 41.07, 49.99, 51.37, 0.00, 58.92, 61.61, 64.41, 67.35]


# ---------------------------------------------------------------------------
# The worked example


@pytest.mark.parametrize("t", sorted(WORKED_A))
def test_worked_example_chassis_a_row(fr_ec_anchor, t):
    """Every cell of the notes' Chassis A table, to the displayed precision."""
    levy, assets, pm, prov_div, parts, u, contrib, surr = WORKED_A[t]
    p = fr_ec_anchor
    assert p.parts_levy(t) == pytest.approx(levy, abs=CENT)
    assert p.own_assets(t) == pytest.approx(assets, abs=CENT)
    assert p.pm(t) == pytest.approx(pm, abs=CENT)
    assert p.prov_div(t) == pytest.approx(prov_div, abs=CENT)
    assert p.parts(t) == pytest.approx(parts, abs=PART)
    assert p.part_value(t) == pytest.approx(u, abs=PART)
    assert p.insurer_contribution(t) == pytest.approx(contrib, abs=CENT)
    assert p.surrender_value(t) == pytest.approx(surr, abs=CENT)
    # The parts and their value multiply back to the provision they came from.
    assert p.parts(t) * p.part_value(t) == pytest.approx(p.prov_div(t), abs=CENT)


@pytest.mark.parametrize("t", sorted(WORKED_B))
def test_worked_example_chassis_b_row(eurocroissance, t):
    """Every cell of the notes' Chassis B table, to the displayed precision."""
    levy, prov_div, parts, u, pgt = WORKED_B[t]
    p = eurocroissance.Projection[2]
    assert p.parts_levy(t) == pytest.approx(levy, abs=CENT)
    assert p.prov_div(t) == pytest.approx(prov_div, abs=CENT)
    assert p.own_assets(t) == pytest.approx(prov_div, abs=CENT)
    assert p.pm(t) == 0.0
    assert p.parts(t) == pytest.approx(parts, abs=PART)
    assert p.part_value(t) == pytest.approx(u, abs=PART)
    assert p.pgt(t) == pytest.approx(pgt, abs=CENT)
    assert p.insurer_contribution(t) == 0.0


def test_the_performance_levy_is_asymmetric(eurocroissance, fr_ec_anchor):
    """10% of positive financial performance, and nothing at all on a negative one."""
    a, b = fr_ec_anchor, eurocroissance.Projection[2]
    for i, want in enumerate(PERF_LEVY_A, start=1):
        assert a.perf_levy(i) == pytest.approx(want, abs=CENT), i
    for i, want in enumerate(PERF_LEVY_B, start=1):
        assert b.perf_levy(i) == pytest.approx(want, abs=CENT), i
    assert a.invest_income(6) < 0.0 and a.perf_levy(6) == 0.0
    assert b.invest_income(6) < 0.0 and b.perf_levy(6) == 0.0


def test_the_year_three_versement_splits_at_the_just_struck_values(
        eurocroissance, fr_ec_anchor):
    """The free versement is priced on the striking it follows, not on last year's.

    The notes state the t = 3 row post-versement and the pre-versement state explicitly;
    both are asserted, because the split is what makes ``parts_added_eoy`` right or wrong.
    """
    a = fr_ec_anchor
    assert a.own_assets_at(3, "AFT_PERF") == pytest.approx(10842.49, abs=CENT)
    assert a.pm_at(3, "AFT_STRIKE") == pytest.approx(8386.54, abs=CENT)
    assert a.prov_div_at(3, "AFT_STRIKE") == pytest.approx(2455.95, abs=CENT)
    assert a.parts_at(3, "AFT_PREM") == pytest.approx(190.8455, abs=PART)
    assert a.part_value_at(3, "AFT_STRIKE") == pytest.approx(12.8688, abs=PART)
    # pm_added = 1,960.00 x 1.0225^-7 = 1,677.31, so pd_added = 282.69 buys 21.9672
    # parts.  Recomputing the division from the notes' rounded intermediates lands
    # within 2e-4 of the model's exact figure.
    assert a.premium_top_up_net_pp(3) == pytest.approx(1960.00, abs=CENT)
    assert a.parts_added_eoy(3) == pytest.approx(21.9672, abs=PART)
    assert 282.69 / 12.8688 == pytest.approx(21.9672, abs=0.0002)
    # On Chassis B nothing goes to a PM, so the whole net versement buys parts.
    b = eurocroissance.Projection[2]
    assert b.prov_div_at(3, "AFT_STRIKE") == pytest.approx(10637.52, abs=CENT)
    assert b.parts_at(3, "AFT_PREM") == pytest.approx(956.6677, abs=PART)
    assert b.parts_added_eoy(3) == pytest.approx(176.2694, abs=PART)
    assert 1960.00 / 11.1193 == pytest.approx(176.2694, abs=0.001)


def test_the_exit_values_the_two_chassis_pay(eurocroissance, fr_ec_anchor):
    """The notes' exit table: the year-6 shock and the maturity, on each chassis."""
    a, b = fr_ec_anchor, eurocroissance.Projection[2]
    assert a.surrender_value(6) == pytest.approx(12384.73, abs=CENT)
    assert b.surrender_value(6) == pytest.approx(9899.22, abs=CENT)
    assert a.surrender_value(6) / 11760.00 == pytest.approx(1.0531, abs=0.00005)
    assert b.surrender_value(6) / 11760.00 == pytest.approx(0.8418, abs=0.00005)
    assert a.maturity_value(10) == pytest.approx(12765.89, abs=CENT)
    assert b.maturity_value(10) == pytest.approx(11830.69, abs=CENT)
    # 12,765.89 = 11,760.00 + 201.1774 x 5.0000, reproduced independently of the path.
    assert 11760.00 + 201.1774 * 5.0 == pytest.approx(12765.89, abs=CENT)
    assert max(a.insurer_contribution(t) for t in range(11)) == pytest.approx(
        2134.08, abs=CENT)
    assert max(b.pgt(t) for t in range(11)) == pytest.approx(1446.78, abs=CENT)


def test_the_a134_3_gates_and_the_a134_4_headroom(fr_ec_anchor):
    """Both revaluation tests pass at t = 5; the second fails at t = 6.

    Neither discretion is exercised, and both are computed, because a model that revalued
    guarantees without testing the gates would exercise a discretion A. 134-3 withholds.
    """
    p = fr_ec_anchor
    assert 1.5 * (p.mg(5) - p.pm(5)) == pytest.approx(1857.27, abs=CENT)
    assert p.prov_div(5) - p.parts(5) * 5.0 == pytest.approx(2123.98, abs=CENT)
    assert 0.10 * p.pm(5) == pytest.approx(1052.18, abs=CENT)
    assert p.gate_revalue_ok(5) is True
    # At t = 6 the part-value floor has taken the headroom to nil.
    assert p.prov_div(6) - p.parts(6) * 5.0 == pytest.approx(0.00, abs=CENT)
    assert 0.10 * p.pm(6) == pytest.approx(1134.60, abs=CENT)
    assert p.gate_revalue_ok(6) is False
    # C solving pd - C - N u_min = 15% (pm + C).
    assert p.conversion_headroom(5) == pytest.approx(474.52, abs=CENT)
    assert p.conversion_headroom(6) == 0.0


def test_the_guarantee_level_is_the_products_real_dial(eurocroissance, fr_ec_anchor):
    """At g = 80% the same path cuts the year-6 contribution by 61%.

    Model point 3 is point 1 with the guarantee level moved and nothing else.
    """
    p80 = eurocroissance.Projection[3]
    assert p80.guarantee_rate() == 0.80
    assert p80.pm(6) == pytest.approx(9076.80, abs=CENT)
    assert p80.insurer_contribution(6) == pytest.approx(829.17, abs=CENT)
    assert fr_ec_anchor.insurer_contribution(6) == pytest.approx(2134.08, abs=CENT)
    # The PM is 80.1% of the initial net versement at g = 100% and 64.0% at g = 80%.
    assert fr_ec_anchor.pm(0) / 9800.0 == pytest.approx(0.801, abs=0.0005)
    assert p80.pm(0) / 9800.0 == pytest.approx(0.640, abs=0.0005)


def test_the_apport_dactifs_endows_the_pcdd_and_not_the_savers(eurocroissance):
    """A statutory-maximum apport at t = 6 cuts the PGT and changes no saver value.

    Model point 4 is point 2 with the R. 134-12 contribution switched on.
    """
    plain, apport = eurocroissance.Projection[2], eurocroissance.Projection[4]
    assert apport.apport(6) == pytest.approx(989.92, abs=CENT)
    assert apport.apport(6) == pytest.approx(0.10 * plain.prov_div(6), abs=CENT)
    assert apport.pcdd(6) == pytest.approx(989.92, abs=CENT)
    assert apport.pgt(6) == pytest.approx(456.86, abs=CENT)
    assert plain.pgt(6) == pytest.approx(1446.78, abs=CENT)
    for t in range(11):        # not one cent of policyholder value moves
        assert apport.prov_div(t) == pytest.approx(plain.prov_div(t), abs=1e-9)
        assert apport.surrender_value(t) == pytest.approx(
            plain.surrender_value(t), abs=1e-9)


# ---------------------------------------------------------------------------
# Pitfall 1: the Chassis B surrender value is not guaranteed


def test_a_chassis_b_surrender_before_the_echeance_can_pay_less_than_the_guarantee(
        eurocroissance):
    """9,899.22 against a guarantee of 11,760.00 -- the product's central error.

    A 2 deg engagement pays parts x part value and nothing else before the echeance
    (R. 134-5).  A model that floors it at g x premiums, or at the discounted guarantee,
    is modelling a contract that does not exist.
    """
    b = eurocroissance.Projection[2]
    assert b.mg(6) == pytest.approx(11760.00, abs=CENT)
    assert b.surrender_value(6) == pytest.approx(9899.22, abs=CENT)
    assert b.surrender_value(6) < b.mg(6)
    assert b.surrender_value(6) == pytest.approx(
        b.parts(6) * b.part_value(6), abs=CENT)
    # The shortfall is 1,860.78, carried by the insurer and not by the contract.
    assert b.mg(6) - b.surrender_value(6) == pytest.approx(1860.78, abs=CENT)
    assert all(b.surrender_value(t) < b.mg(t) for t in (6, 7, 8, 9))
    # Chassis A, whose PM has been marked up by the same fall in rates, does not.
    assert eurocroissance.Projection[1].surrender_value(6) > 11760.00


# ---------------------------------------------------------------------------
# Pitfalls 2 and 9: the insurer's own funds are not the savers' money


def test_the_own_funds_provisions_never_reach_a_policyholder(eurocroissance):
    """No benefit before the echeance exceeds the two savers' provisions.

    The PGT is the insurer's own-funds provision, outside the participation account
    (A. 134-2), and the L. 134-3 contribution is capital completing the representation.
    The check is live because the shipped Chassis B cell carries a positive PGT for four
    consecutive years.
    """
    for point_id in eurocroissance.Data.model_point_table().index:
        p = eurocroissance.Projection[point_id]
        assert p.check_own_funds_not_paid() is True, point_id
        for t in range(p.proj_start(), p.proj_len()):
            assert p.surrender_value(t) <= p.provision_value(t) + 1e-9
            assert p.death_value(t) == pytest.approx(p.provision_value(t), abs=1e-9)
    cols = eurocroissance.Projection[2].result_cf().columns
    assert "pgt" not in cols and "insurer_contribution" not in cols


def test_the_l134_3_contribution_earns_nothing_for_the_savers(fr_ec_anchor):
    """The year-7 asset roll starts from 10,250.65, not from the 12,384.73 surrendered.

    A model that rolls the topped-up balance forward as savers' assets manufactures
    investment return out of the insurer's capital.
    """
    p = fr_ec_anchor
    assert p.insurer_contribution(6) == pytest.approx(2134.08, abs=CENT)
    assert p.own_assets(6) == pytest.approx(10250.65, abs=CENT)
    assert p.provision_value(6) == pytest.approx(12384.73, abs=CENT)
    # The surrender value exceeds the account's own assets by exactly the contribution.
    assert p.provision_value(6) - p.own_assets(6) == pytest.approx(
        p.insurer_contribution(6), abs=1e-9)
    assert p.own_assets_at(7, "AFT_LEVY") == pytest.approx(10242.34, abs=CENT)
    assert p.check_assets_roll_fwd() is True


# ---------------------------------------------------------------------------
# Pitfalls 3 and 12: the PM is re-struck at the current A. 134-1 rate


def test_the_pm_is_restruck_and_not_accumulated(fr_ec_anchor):
    """The year-6 move decomposes into +236.74 of time and +587.44 of rate.

    Rolling pm(t-1) forward at last year's rate removes the rate effect entirely, which
    is more than twice the time effect here.
    """
    p = fr_ec_anchor
    assert p.i_pm(5) == pytest.approx(0.0225, abs=1e-12)
    assert p.i_pm(6) == pytest.approx(0.0090, abs=1e-12)
    at_old_rate = 11760.00 * 1.0225 ** -4
    assert at_old_rate == pytest.approx(10758.56, abs=CENT)
    assert at_old_rate - p.pm(5) == pytest.approx(236.74, abs=0.02)     # time effect
    assert p.pm(6) - at_old_rate == pytest.approx(587.44, abs=0.02)     # rate effect
    assert p.pm(6) - p.pm(5) == pytest.approx(824.18, abs=0.02)
    # Accumulating pm(5) at last year's rate lands exactly on the time-effect figure,
    # 587.44 short of the re-strike.
    assert p.pm(5) * (1 + p.i_pm(5)) == pytest.approx(10758.56, abs=CENT)
    assert p.pm(10) == pytest.approx(11760.00, abs=CENT)


def test_the_pm_funds_the_guarantee_exactly_at_the_echeance(eurocroissance):
    """pm(t) accumulated at i_pm(t) to t = n equals mg(t) at every t -- the headline check."""
    p = eurocroissance.Projection[1]
    assert p.check_guarantee_funding() is True
    assert p.pm(10) == pytest.approx(p.mg(10), abs=1e-9)
    for t in range(11):
        assert p.pm(t) * (1 + p.i_pm(t)) ** (10 - t) == pytest.approx(
            p.mg(t), abs=1e-6)
    # On Chassis B both sides are nil: nothing inside the account funds the guarantee,
    # and the own-funds provisions carry it instead.
    b = eurocroissance.Projection[2]
    assert b.check_guarantee_funding() is True
    assert all(b.pm(t) == 0.0 for t in range(11))
    assert b.check_pgt_covers_guarantee() is True


def test_the_discount_rate_is_a134_1_and_not_a132_1_or_a132_3(eurocroissance):
    """90% of the TEC at the remaining maturity, interpolated, and floored at zero."""
    p = eurocroissance.Projection[1]
    assert p.i_pm(0) == pytest.approx(0.90 * 0.0250, abs=1e-12)
    assert p.i_pm(6) == pytest.approx(0.90 * 0.0100, abs=1e-12)
    # Model point 10 runs on an upward-sloping curve, so the interpolation bites: at
    # t = 13 of a 20-year term the maturity is 7, between the 5-year 1.50% and 10-year
    # 2.50% nodes, giving 1.90% and an i_pm of 1.71%.
    sloped = eurocroissance.Projection[10]
    assert sloped.tec_rate(10) == pytest.approx(0.0250, abs=1e-12)     # maturity 10
    assert sloped.tec_rate(13) == pytest.approx(0.0190, abs=1e-12)     # maturity 7
    assert sloped.i_pm(13) == pytest.approx(0.0171, abs=1e-12)
    assert sloped.tec_rate(0) == pytest.approx(0.0300, abs=1e-12)      # maturity 20
    # Model point 11 runs on a negative curve, so the article's zero floor binds and the
    # PM equals the guarantee outright rather than exceeding it.
    floored = eurocroissance.Projection[11]
    assert floored.tec_rate(0) == pytest.approx(-0.0050, abs=1e-12)
    assert all(floored.i_pm(t) == 0.0 for t in range(9))
    assert floored.disc_factor(0) == 1.0
    assert floored.pm(0) == pytest.approx(floored.mg(0), abs=1e-9)


def test_an_in_force_extract_is_checked_against_the_restrike(eurocroissance):
    """Model point 7 supplies a PM; the model re-derives it and compares.

    An extract built by accumulating the PM disagrees here -- the same error
    ``check_guarantee_funding`` catches inside the projection, from the data side.
    """
    p = eurocroissance.Projection[7]
    assert p.duration_inforce() == 4 and p.proj_start() == 4
    assert p.pm_init() == pytest.approx(8575.24, abs=CENT)
    assert p.pm(4) == pytest.approx(p.pm_init(), abs=CENT)
    assert p.pm(4) == pytest.approx(p.mg(4) * p.disc_factor(4), abs=1e-9)
    assert p.check_pm_restruck() is True
    # A new-business cell has no extract to check, and the residual is zero throughout.
    fresh = eurocroissance.Projection[1]
    assert all(fresh.check_pm_restruck_resid(t) == 0.0 for t in range(11))


# ---------------------------------------------------------------------------
# Pitfall 4: the recurring charge is a levy in number of parts


def test_the_recurring_charge_is_a_levy_in_number_of_parts(eurocroissance, fr_ec_anchor):
    """15.64 in year 1 on Chassis A, not the 78.40 an encours levy would have taken.

    R. 134-3 3 deg permits an encours levy only where the auxiliary account holds no
    1 deg engagements, and no base permits any levy on the provision mathematique.
    """
    p = fr_ec_anchor
    assert p.parts_levy(1) == pytest.approx(15.64, abs=CENT)
    assert p.parts_levy(1) == pytest.approx(0.008 * p.prov_div(0), abs=1e-9)
    assert 0.008 * p.provision_value(0) == pytest.approx(78.40, abs=CENT)
    # The levy cancels parts rather than reducing their value, and seven years of it
    # and nothing else close the count.
    assert p.parts_at(1, "AFT_LEVY") == pytest.approx(p.parts(0) * 0.992, abs=1e-12)
    assert p.check_parts_roll_fwd() is True
    assert p.parts(3) * 0.992 ** 7 == pytest.approx(201.1774, abs=PART)
    # With no 1 deg engagement the parts are the whole account, so the levy *is* 78.40.
    b = eurocroissance.Projection[2]
    assert b.pm(0) == 0.0 and b.parts_levy(1) == pytest.approx(78.40, abs=CENT)
    assert b.parts(3) * 0.992 ** 7 == pytest.approx(1070.9951, abs=PART)


# ---------------------------------------------------------------------------
# Pitfall 5: the guarantee is net of the entry charge


def test_the_entry_charge_cuts_the_guarantee_and_a_rachat_runs_it_down(
        eurocroissance, fr_ec_anchor):
    """mg after the year-3 top-up is 11,760.00, not 12,000.00, and it runs down."""
    p = fr_ec_anchor
    assert p.entry_charge_rate() == 0.02
    assert p.mg(0) == pytest.approx(9800.00, abs=CENT)
    assert p.mg(2) == pytest.approx(9800.00, abs=CENT)
    assert p.mg(3) == pytest.approx(11760.00, abs=CENT)
    assert p.prem_after_charge_pp(0) == pytest.approx(9800.00, abs=CENT)
    assert p.premium_top_up_net_pp(3) == pytest.approx(1960.00, abs=CENT)
    assert p.entry_charge(3) == pytest.approx(40.00, abs=CENT)
    assert p.check_guarantee_roll_fwd() is True
    # Model point 5 takes 6% of the provision in year 1, so mg falls by 6% with it.
    w = eurocroissance.Projection[5]
    assert w.wd_rate(1) == pytest.approx(0.06, abs=1e-12)
    assert w.mg(1) == pytest.approx(9212.00, abs=CENT)
    assert w.wd_gross_pp(1) == pytest.approx(0.06 * w.provision_value(0), abs=1e-9)
    assert w.check_guarantee_roll_fwd() is True
    # A partial rachat is an owner election, in its own column and never a claim.
    df = w.result_cf()
    assert df.loc[1, "withdrawals"] > 0.0
    assert "claims_wd" not in df.columns and "claims_surr" not in df.columns


# ---------------------------------------------------------------------------
# Pitfall 6: the minimum part value


def test_the_minimum_part_value_stops_the_provision_going_negative(fr_ec_anchor):
    """Without the floor the Chassis A diversification provision reaches -1,095.35."""
    p = fr_ec_anchor
    assert p.min_part_value() == 5.0
    assert p.own_assets(6) - p.pm(6) == pytest.approx(-1095.35, abs=CENT)
    assert p.prov_div(6) == pytest.approx(p.parts(6) * 5.0, abs=1e-9)
    assert p.prov_div(6) == pytest.approx(1038.73, abs=CENT)
    assert p.part_value(6) == pytest.approx(5.0000, abs=PART)
    assert p.check_part_value_floor() is True
    # The floor binding is exactly what creates the insurer's contribution.
    assert p.insurer_contribution(6) == pytest.approx(
        p.pm(6) + p.prov_div(6) - p.own_assets(6), abs=1e-9)


# ---------------------------------------------------------------------------
# Pitfall 7: the death benefit is the current provision value


def test_the_death_floor_is_a_rider_and_not_the_maturity_guarantee(eurocroissance):
    """The year-6 Chassis B death pays 11,760.00, of which 1,860.78 is outside the account."""
    b = eurocroissance.Projection[2]
    assert b.death_floor_flag() is True
    assert b.death_value(6) == pytest.approx(9899.22, abs=CENT)
    assert b.death_payout(6) == pytest.approx(11760.00, abs=CENT)
    assert b.rider_claim_pp(6) == pytest.approx(1860.78, abs=CENT)
    assert b.cum_prem_net(6) == pytest.approx(11760.00, abs=CENT)
    # On Chassis A the provision already exceeds the floor, so the rider costs nothing.
    a = eurocroissance.Projection[1]
    assert a.death_payout(6) == pytest.approx(12384.73, abs=CENT)
    assert a.rider_claim_pp(6) == 0.0
    # The floor coincides with mg only because g is 100%.  Point 3 is g = 80%.
    p80 = eurocroissance.Projection[3]
    assert p80.cum_prem_net(6) == pytest.approx(11760.00, abs=CENT)
    assert p80.mg(6) == pytest.approx(9408.00, abs=CENT)
    # Model point 8 carries no rider, and its exit charge and indemnity apply instead.
    n = eurocroissance.Projection[8]
    assert n.death_floor_flag() is False
    assert n.death_payout(5) == pytest.approx(n.provision_value(5), abs=1e-9)
    assert n.rider_claim_pp(5) == 0.0
    assert n.exit_charge_rate() == 0.01 and n.surrender_indemnity(5) == 0.03
    assert n.surrender_value(5) == pytest.approx(
        n.provision_value(5) * 0.99 * 0.97, abs=1e-9)
    # R. 132-5-3 permits no indemnity after ten years in force.
    assert n.surrender_indemnity(10) == 0.03 and n.surrender_indemnity(11) == 0.0


# ---------------------------------------------------------------------------
# Pitfall 8: the maturity max is terminal, and Chassis B only


def test_the_maturity_max_is_chassis_b_only_and_terminal_only(eurocroissance):
    """max(N u, mg) at t = n on Chassis B; nowhere else, and never on Chassis A."""
    a, b = eurocroissance.Projection[1], eurocroissance.Projection[2]
    assert all(a.maturity_value(t) == 0.0 for t in range(10))
    assert all(b.maturity_value(t) == 0.0 for t in range(10))
    # Chassis A pays the provisions, which exceed the bare guarantee.
    assert a.maturity_value(10) == pytest.approx(a.provision_value(10), abs=1e-9)
    assert a.maturity_value(10) == pytest.approx(12765.89, abs=CENT)
    assert a.maturity_value(10) > a.mg(10)
    # Chassis B's account recovered to 0.60% above the guarantee, so the max does not
    # bite -- but it is the max that is being taken.
    assert b.maturity_value(10) == pytest.approx(
        max(b.provision_value(10), b.mg(10)), abs=1e-9)
    assert b.maturity_value(10) / b.mg(10) == pytest.approx(1.0060, abs=0.00005)
    # Where it does bite, the guarantee is paid out of the PGT.  Model point 6 ends far
    # under water, and its maturity amount is the guarantee itself.
    under = eurocroissance.Projection[6]
    n = under.proj_len()
    assert under.provision_value(n) < under.mg(n)
    assert under.maturity_value(n) == pytest.approx(under.mg(n), abs=1e-9)
    assert under.pgt(n - 1) > 0.0


# ---------------------------------------------------------------------------
# Pitfall 10: one auxiliary account has one part value


def test_two_accounts_on_one_asset_path_do_not_share_a_part_value(eurocroissance):
    """The shipped model points are separate accounts, and their part values diverge.

    R. 134-2 makes the part value common to every engagement of an auxiliary account, so
    two engagements of one account would share one path.  A per-policy model can only
    approximate that, and the two worked-example cells are two accounts rather than two
    engagements of one -- which is why they diverge on the same asset return.
    """
    a, b = eurocroissance.Projection[1], eurocroissance.Projection[2]
    assert a.scenario() == b.scenario()
    assert a.part_value(0) == b.part_value(0) == 10.0
    assert a.part_value(1) != b.part_value(1)
    assert a.part_value(6) == pytest.approx(5.0000, abs=PART)
    assert b.part_value(6) == pytest.approx(8.9508, abs=PART)
    # Model point 4 *is* point 2's account with an apport added to the PCDD, so it
    # shares the part value exactly -- the account-level statement holding.
    assert eurocroissance.Projection[4].part_value(6) == pytest.approx(
        b.part_value(6), abs=1e-12)


# ---------------------------------------------------------------------------
# Behaviour


def test_the_guarantee_imminent_suppression_is_gated_on_the_guarantee_biting(
        eurocroissance):
    """0.5 in the two years before the echeance on Chassis B, and only while N u < mg.

    A saver who surrenders a 2 deg engagement gives up the entire guarantee, so the
    deterrent exists precisely then; applying it unconditionally would invent behaviour.
    """
    p = eurocroissance.Projection[6]
    assert p.proj_len() == 12
    assert p.parts(10) * p.part_value(10) < p.mg(10)
    assert p.guarantee_imminent(10) == 0.5 and p.guarantee_imminent(11) == 0.5
    assert p.lapse_rate(10) == pytest.approx(0.0125, abs=1e-12)
    # Three years out it does not apply, in the money or not.
    assert p.guarantee_imminent(9) == 1.0
    assert p.lapse_rate(9) == pytest.approx(0.025, abs=1e-12)
    # And it never applies on Chassis A, which has no such cliff.
    a = eurocroissance.Projection[1]
    assert all(a.guarantee_imminent(t) == 1.0 for t in (8, 9, 10))


def test_the_duration_eight_spike_and_the_lock_up(eurocroissance):
    """1.5 at t = 8 where n > 8; nil surrender inside a non-surrender period."""
    p5 = eurocroissance.Projection[5]
    assert p5.duration8_spike(8) == 1.5 and p5.duration8_spike(7) == 1.0
    assert p5.lapse_rate(8) == pytest.approx(0.025 * 1.5, abs=1e-12)
    # A contract maturing at eight has no such choice to make.
    p11 = eurocroissance.Projection[11]
    assert p11.proj_len() == 8 and p11.duration8_spike(8) == 1.0
    # Model point 9 is barred from surrender for four years, and pays scheduled
    # versements at the start of each of its first five.
    p9 = eurocroissance.Projection[9]
    assert p9.lock_up_years() == 4
    assert all(p9.lapse_rate(t) == 0.0 and p9.wd_rate(t) == 0.0 for t in (1, 2, 3, 4))
    assert p9.lapse_rate(5) == pytest.approx(0.025, abs=1e-12)
    assert p9.premium_gross_pp(0) == 10000.0
    assert p9.premium_gross_pp(5) == 1200.0 and p9.premium_gross_pp(6) == 0.0


def test_the_worked_example_switches_the_decrements_off(fr_ec_anchor):
    """pols_if stays at 1 to the echeance, so the provision path is the cash flow path."""
    p = fr_ec_anchor
    assert p.decrement_basis() == "none"
    assert all(p.mort_rate(t) == 0.0 and p.lapse_rate(t) == 0.0 for t in range(11))
    # pols_if is the START-of-year count, so it is 1 on every row including the echeance.
    assert all(p.pols_if(t) == 1.0 for t in range(11))
    # The notes' end-of-year l(t) is pols_if_at(t, "AFT_DECR"); it is nil at the echeance,
    # where the survivors mature.
    assert p.pols_if_at(10, "AFT_DECR") == 0.0 and p.pols_maturity(10) == 1.0
    assert p.check_pols_roll_fwd() is True


def test_pols_if_is_the_start_of_year_count_and_l_of_t_survives(eurocroissance):
    """The published exposure is the weight on its own row, not last year's.

    ``pols_if(t)`` is the count at the START of policy year t and is what every flow on the
    same ``result_cf()`` row is weighted by, so the opening row is ``pols_if_init()`` and a
    flow divided by its own row's ``pols_if`` is the per-policy amount.  The notes' ``l(t)``
    -- the count at the END of the year -- is unchanged and reached as
    ``pols_if_at(t, "AFT_DECR")``.  This model published ``l(t)`` under the bare name until
    the exposure column was found to sit one year ahead of the flows beside it, which
    nothing raised on.
    """
    for point_id in eurocroissance.Data.model_point_table().index:
        p = eurocroissance.Projection[point_id]
        t0, n = p.proj_start(), p.proj_len()
        df = p.result_cf()
        assert df["pols_if"].iloc[0] == pytest.approx(p.pols_if_init(), rel=1e-12), point_id
        assert p.pols_if(t0) == p.pols_if_init()
        # Start of year t is the end of year t - 1, and the year closes on AFT_DECR.
        for t in range(t0 + 1, n + 1):
            assert p.pols_if(t) == pytest.approx(
                p.pols_if_at(t - 1, "AFT_DECR"), rel=1e-12), (point_id, t)
        assert p.pols_if_at(n, "AFT_DECR") == 0.0
        # The maturity claim is carried by the survivors of the last year's mortality, and
        # the published exposure on that row is the count that entered it.
        assert p.pols_maturity(n) == pytest.approx(
            p.pols_if(n) * (1.0 - p.mort_rate(n)), rel=1e-12), point_id
        # And a flow divided by its own row's pols_if is the per-policy amount.
        row = df.loc[t0]
        assert row["premiums"] / row["pols_if"] == pytest.approx(
            p.total_premium_pp(t0), rel=1e-12), point_id


# ---------------------------------------------------------------------------
# Structure, documentation and inputs


def test_result_cf_shape_and_what_it_leaves_out(fr_ec_anchor):
    """The cash flow table publishes no provision, no own-funds item and no subtotal."""
    df = fr_ec_anchor.result_cf()
    assert list(df.index) == list(range(0, 11)) and df.index.name == "t"
    assert list(df.columns) == [
        "pols_if", "premiums", "claims_death", "claims_lapse", "claims_maturity",
        "withdrawals", "expenses", "charges_taken", "rider_claims",
        "liability_cf", "net_cf",
    ]
    for absent in ("claims", "pm", "prov_div", "own_assets", "parts", "part_value",
                   "insurer_contribution", "pgt", "pcdd", "mg", "av_pp_at"):
        assert absent not in df.columns
    prov = fr_ec_anchor.result_provisions()
    assert prov.index.name == "t"
    for present in ("own_assets", "pm", "prov_div", "parts", "part_value",
                    "insurer_contribution", "pgt", "pcdd"):
        assert present in prov.columns


def test_both_signs_of_the_net_flow_are_published(fr_ec_anchor):
    """liability_cf is the notes' outgo-positive CF(t); net_cf is the library's sign."""
    df = fr_ec_anchor.result_cf()
    assert (df["net_cf"] + df["liability_cf"]).abs().max() == pytest.approx(
        0.0, abs=1e-9)
    outgo = df[["claims_death", "claims_lapse", "claims_maturity", "withdrawals",
                "expenses"]].sum(axis=1)
    assert (outgo - df["premiums"] - df["liability_cf"]).abs().max() == pytest.approx(
        0.0, abs=1e-9)
    # charges_taken and rider_claims are memo lines outside net_cf.
    assert df["charges_taken"].sum() > 0.0


def test_invalid_enum_values_raise(fr_ec_anchor):
    """The enum accessors validate rather than propagating a typo into a lookup."""
    with pytest.raises(FormulaError):
        fr_ec_anchor.claim_pp(1, "SURRENDER")
    with pytest.raises(FormulaError):
        fr_ec_anchor.claims(1, "LAPSED")
    with pytest.raises(FormulaError):
        fr_ec_anchor.own_assets_at(1, "AFT_CHARGE")
    with pytest.raises(FormulaError):
        fr_ec_anchor.parts_at(1, "BEF_LEVY")
    with pytest.raises(FormulaError):
        fr_ec_anchor.pols_if_at(1, "AFT_SURR")
    # The rente viagere option at the echeance needs the TGH05 / TGF05 tables, cited
    # and never shipped, so no model point elects it and the accessor rejects one.
    assert not fr_ec_anchor.model_point()["annuity_option_flag"]
    assert fr_ec_anchor.annuity_option_flag() is False


def test_the_docstrings_describe_the_current_structure(eurocroissance):
    """Specifics a reader would rely on, asserted so they cannot go stale silently.

    The model docstring carries the house disclaimers, Projection the symbol mapping,
    and Data the account of the input arrangement.
    """
    doc = eurocroissance.doc
    assert "eurocroissance" in doc
    assert "mechanics demonstration" in doc
    assert "external" in doc                     # inputs are not stored in the model
    assert "once per model" in doc               # why Data exists
    assert "re-struck, never accumulated" in doc
    assert "84.18" in doc                        # the Chassis B surrender fact
    proj = eurocroissance.Projection.doc
    assert "Notes symbol" in proj
    for cells in ("proj_len", "model_point", "prov_div", "part_value", "pgt",
                  "insurer_contribution", "provision_value"):
        assert cells in proj
    data = eurocroissance.Data.doc
    assert "TradLife_A" in data
    for cells in ("input_dir", "model_point_table", "tec_curve"):
        assert cells in data


def test_inputs_live_beside_the_model_and_mark_their_own_provenance(eurocroissance):
    """Five CSVs, two of them scenario files; the decrement tables say what they are."""
    assert {"model_point_table.csv", "mort_table.csv", "lapse_table.csv",
            "scenario_table.csv", "tec_curve.csv"} == {
                p.name for p in MODEL_DIR.parent.iterdir() if p.suffix == ".csv"}
    mort = pd.read_csv(MODEL_DIR.parent / "mort_table.csv")
    assert len(set(mort["provenance"])) == 1
    prov = mort["provenance"].iloc[0]
    assert prov.startswith("[std]") and "never shipped" in prov
    assert mort["mort_rate"].max() <= 1.0
    # Anchored so that the 80% best-estimate factor gives 0.5000% at male 57.
    anchor = mort[(mort["sex"] == "M") & (mort["age"] == 57)]["mort_rate"].iloc[0]
    assert anchor * 0.80 == pytest.approx(0.0050, rel=1e-12)
    assert mort[(mort["sex"] == "M") & (mort["age"] == 120)]["mort_rate"].iloc[0] == 1.0
    # And the projection reaches the table through that same factor.
    p = eurocroissance.Projection[8]              # decrements on, male 61 at entry
    raw = float(eurocroissance.Data.mort_table().loc[("M", 62), "mort_rate"])
    assert p.age(1) == 62 and p.mort_rate(1) == pytest.approx(raw * 0.80, rel=1e-12)
    lapse = pd.read_csv(MODEL_DIR.parent / "lapse_table.csv")
    assert set(lapse["provenance"]) == {
        "[std] no eurocroissance lapse experience is public"}
    assert lapse["lapse_rate"].max() == 0.025
    assert list(lapse["wd_rate"][:3]) == [0.06, 0.06, 0.03]


def test_a_tec_curve_can_be_swapped_without_touching_formulas():
    """This is what a production user does with a real published TEC term structure.

    A lower curve raises the provision mathematique, which is the product's dominant risk
    and the reason the curve is a table with a maturity dimension rather than a Reference.
    """
    lower = pd.read_csv(MODEL_DIR.parent / "tec_curve.csv",
                        index_col=["scenario", "year", "maturity"])
    lower["tec_rate"] = lower["tec_rate"] * 0.5

    model = mx.read_model(MODEL_DIR, name="EC_FR_A_swap")
    try:
        alt_name = "tec_curve_low.csv"
        lower.to_csv(model.Data.input_dir() / alt_name)
        try:
            base = model.Projection[1].pm(0)
            model.Data.tec_curve_file = alt_name
            model.Data.clear_all()
            model.Projection.clear_all()
            assert model.Projection[1].pm(0) > base
            # And the guarantee still lands exactly on the PM at the echeance.
            assert model.Projection[1].check_guarantee_funding() is True
        finally:
            (model.Data.input_dir() / alt_name).unlink(missing_ok=True)
    finally:
        model.close()


def test_every_model_point_projects_and_every_check_holds(eurocroissance):
    """No model point may sit in the table that the input tables cannot serve."""
    checks = [c for c in eurocroissance.Projection.cells
              if c.startswith("check_") and not c.endswith("_resid")]
    assert len(checks) >= 2
    columns = None
    for point_id in eurocroissance.Data.model_point_table().index:
        p = eurocroissance.Projection[point_id]
        df = p.result_cf()
        assert len(df) > 0 and df.notna().all().all(), point_id
        assert df["net_cf"].sum() == df["net_cf"].sum(), point_id      # not NaN
        if columns is None:
            columns = list(df.columns)
        else:
            assert list(df.columns) == columns, point_id
        for c in checks:
            value = getattr(p, c)()
            assert isinstance(value, bool) and value is True, (point_id, c)


def test_round_trip_is_stable(tmp_path):
    """read -> write -> re-read reproduces the goldens and the same file set."""
    model = mx.read_model(MODEL_DIR, name="EC_FR_A_rt_src")
    try:
        dest = tmp_path / MODEL_DIR.name
        mx.write_model(model, str(dest), backup=False)
    finally:
        model.close()

    for csv in MODEL_DIR.parent.glob("*.csv"):
        shutil.copy(csv, tmp_path / csv.name)

    reread = mx.read_model(dest, name="EC_FR_A_rt")
    try:
        p, b = reread.Projection[1], reread.Projection[2]
        for t, row in WORKED_A.items():
            assert p.own_assets(t) == pytest.approx(row[1], abs=CENT)
            assert p.pm(t) == pytest.approx(row[2], abs=CENT)
            assert p.prov_div(t) == pytest.approx(row[3], abs=CENT)
        for t, row in WORKED_B.items():
            assert b.prov_div(t) == pytest.approx(row[1], abs=CENT)
            assert b.pgt(t) == pytest.approx(row[4], abs=CENT)
        assert "Notes symbol" in reread.Projection.doc
    finally:
        reread.close()

    assert model_files(dest) == model_files(MODEL_DIR)
