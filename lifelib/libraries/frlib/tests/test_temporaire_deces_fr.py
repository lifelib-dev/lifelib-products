"""Golden and structural tests for TD_FR_A.

The golden values are the worked example in
products/temporaire_deces/technical-notes.md ("Worked example"), which is a
**configuration** rather than a scenario: a revisable-cotisation *assurance temporaire
décès* on a male aged 58 on the *différence de millésime* basis, 150 000 EUR of constant
capital, death cover to attained age 75 and PTIA cover to 65, annual cotisation, standard
rates, no waiting period and no accidental option.  Model point 1 is that cell, and
because ``proj_len = 75 - 58 = 17`` the notes' table is the **entire** projection rather
than a slice of one -- so every row of it is asserted here, not three of them.

They are hard-coded rather than pickled so that a reviewer can compare them against the
notes by eye.  Tolerances follow the precision the notes display: money to the cent,
``pols_if`` to six decimals, and the totals at full precision -- 10 396,90 EUR of death
claims that way against 10 396,89 EUR if the seventeen rounded cells are added.

Beyond the worked example this module asserts the fourteen product facts the notes list
as modeling pitfalls -- the ways an implementation of *this* product looks right and is
wrong: the cotisation is **revisable** and moves every year; PTIA is an **acceleration**
and never a second payment; PTIA cover stops **before** death cover, at a hard age gate;
``q_d`` and ``q_p`` are **dependent** rates and therefore additive; there is **no
surrender value**, by statute, at any duration; the age basis is the *différence de
millésime*; the tariff grid is a lookup whose +38 % step at age 60 must survive; the
suicide factor touches death claims in year 1 and nothing else; the premium-cessation rule
is applied once; nothing exists at ``t = proj_len + 1``; the two premium forms do **not**
collect the same projected total; a *surprime* scales the cotisation and never the
capital; the fractionation loading and the *frais d'échéance* are charges of different
kinds; and the accidental option is a share and not an uplift.
"""
import modelx as mx
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
SIX_DP = 0.0000005    # pols_if displayed to 6 d.p.

MODEL_DIR = LIB / MODELS["TD_FR_A"][0]

# t: (attained age, r(x), pols_if, premiums, claims_death, claims_ptia, expenses, net_cf)
# The notes' worked-example table, in full.  claims_lapse is 0.00 at every t and is
# omitted from the notes' table for space; it is asserted in the row test all the same.
WORKED_EXAMPLE = {
    1:  (58, 0.0105, 1.000000, 1575.00, 588.00, 120.00, 905.72,  -38.72),
    2:  (59, 0.0113, 0.875776, 1484.44, 572.76, 114.55,  97.24,  699.89),
    3:  (60, 0.0156, 0.784075, 1834.73, 558.94, 111.79, 112.80, 1051.21),
    4:  (61, 0.0168, 0.717235, 1807.43, 557.30, 111.46, 110.07, 1028.60),
    5:  (62, 0.0181, 0.670010, 1819.08, 567.46, 113.49, 109.77, 1028.35),
    6:  (63, 0.0197, 0.625542, 1848.48, 577.48, 115.50, 110.38, 1045.11),
    7:  (64, 0.0214, 0.583667, 1873.57, 587.32, 117.46, 110.82, 1057.97),
    8:  (65, 0.0233, 0.544230, 1902.08, 596.92,   0.00, 111.33, 1193.83),
    9:  (66, 0.0255, 0.507836, 1942.47, 607.14,   0.00, 112.61, 1222.73),
    10: (67, 0.0278, 0.473561, 1974.75, 617.11,   0.00, 113.50, 1244.13),
    11: (68, 0.0288, 0.441280, 1906.33, 626.80,   0.00, 109.39, 1170.14),
    12: (69, 0.0314, 0.410875, 1935.22, 636.14,   0.00, 110.17, 1188.91),
    13: (70, 0.0343, 0.382236, 1966.60, 645.06,   0.00, 111.09, 1210.45),
    14: (71, 0.0374, 0.355260, 1993.01, 653.49,   0.00, 111.79, 1227.72),
    15: (72, 0.0409, 0.329849, 2023.62, 661.36,   0.00, 112.72, 1249.54),
    16: (73, 0.0446, 0.305913, 2046.56, 668.57,   0.00, 113.29, 1264.70),
    17: (74, 0.0486, 0.283369, 2065.76, 675.04,   0.00, 113.69, 1277.03),
}

# The notes' Total row, summed at full precision and then rounded.
TOTALS = {"premiums": 31999.13, "claims_death": 10396.90, "claims_ptia": 804.25,
          "expenses": 2676.38, "net_cf": 18121.59}

# The level-premium variant -- the same cell with premium_form = constante and
# level_premium = 0, so P_lev is derived by equivalence.  Model point 2.
# t: (prem_pp, premiums, claims_death, claims_ptia, expenses, net_cf).
LEVEL_VARIANT = {
    1:  (3914.39, 3914.39, 588.00, 120.00, 1841.48, 1364.91),
    2:  (3914.39, 3428.13, 572.76, 114.55,  194.43, 2546.39),
    3:  (3914.39, 3069.17, 558.94, 111.79,  174.52, 2223.93),
    8:  (3914.39, 2130.33, 596.92,   0.00,  122.74, 1410.66),
    17: (3914.39, 1109.22, 675.04,   0.00,   65.86,  368.32),
}

LEVEL_TOTALS = {"premiums": 36367.46, "claims_death": 10396.90, "claims_ptia": 804.25,
                "expenses": 3713.59, "net_cf": 21452.72}


# ---------------------------------------------------------------------------
# The worked example


@pytest.mark.parametrize("t", sorted(WORKED_EXAMPLE))
def test_worked_example_row(fr_td_anchor, t):
    """Every cell of the notes' seventeen-row table, to the displayed precision."""
    age, rate, pols_if, prem, cd, cp, exp, net = WORKED_EXAMPLE[t]
    p = fr_td_anchor
    assert p.age(t) == age
    assert p.prem_rate(t) == pytest.approx(rate, rel=1e-12)
    assert p.pols_if(t) == pytest.approx(pols_if, abs=SIX_DP)
    assert p.premiums(t) == pytest.approx(prem, abs=CENT)
    assert p.claims(t, "DEATH") == pytest.approx(cd, abs=CENT)
    assert p.claims(t, "PTIA") == pytest.approx(cp, abs=CENT)
    assert p.expenses(t) == pytest.approx(exp, abs=CENT)
    assert p.net_cf(t) == pytest.approx(net, abs=CENT)
    assert p.claims(t, "LAPSE") == 0.0


def test_the_worked_example_totals_are_summed_at_full_precision(fr_td_anchor):
    """The notes' Total row is a full-precision sum, then rounded -- not a sum of cells."""
    df = fr_td_anchor.result_cf()
    for column, total in TOTALS.items():
        assert df[column].sum() == pytest.approx(total, abs=CENT), column
    # And the rounded-cell sum really does differ, which is why this test exists.
    assert sum(round(WORKED_EXAMPLE[t][4], 2) for t in WORKED_EXAMPLE) == pytest.approx(
        10396.89, abs=CENT)


def test_year_three_rebuilt_from_scratch(fr_td_anchor):
    """The notes' own independent rebuild of year 3, component by component.

    ``l(3) = 0,875776 x (1 - 0,005232) x 0,90``, then the claims and each of the three
    expense lines separately, then ``net_cf(3)``.  The last step carries the notes' own
    one-cent rounding artefact: the four *displayed* figures subtract to 1 051,20 while
    the full-precision result is 1 051,2108, printed as 1 051,21.  Both are asserted.
    """
    p = fr_td_anchor
    assert p.pols_if(2) == pytest.approx(0.99520 * 0.88, rel=1e-9)
    assert p.mort_rate(2) == pytest.approx(0.00400 * 1.09, rel=1e-9)
    assert p.ptia_rate(2) == pytest.approx(0.000872, rel=1e-9)
    assert p.pols_if(3) == pytest.approx(0.875776 * 0.8952912, abs=1e-8)
    assert p.mort_rate(3) == pytest.approx(0.0047524, rel=1e-9)
    assert p.ptia_rate(3) == pytest.approx(0.00095048, rel=1e-9)
    assert p.claims(3, "DEATH") == pytest.approx(150000 * 0.78407455 * 0.0047524, abs=CENT)
    assert p.claims(3, "PTIA") == pytest.approx(150000 * 0.78407455 * 0.00095048, abs=CENT)
    assert p.commissions(3) == pytest.approx(0.05 * 2340.00 * 0.78407455, abs=CENT)
    assert p.claim_expenses(3) == pytest.approx(150 * 0.78407455 * 0.00570288, abs=0.0005)
    assert p.expenses(3) == pytest.approx(20.3938 + 91.7367 + 0.6707, abs=CENT)
    assert p.net_cf(3) == pytest.approx(1051.21, abs=CENT)
    assert 1834.73 - 558.94 - 111.79 - 112.80 == pytest.approx(1051.20, abs=CENT)


def test_the_decrements_close_four_ways(fr_td_anchor):
    """The notes' closure split: deaths, PTIA, lapses and survivors sum to exactly one.

    The last term is ``pols_if(proj_len + 1)``, the expiring cohort, which exists so the
    identity closes and is a weight on no cash flow.
    """
    p = fr_td_anchor
    n = p.proj_len()
    deaths = sum(p.pols_death(t) for t in range(1, n + 1))
    ptia = sum(p.pols_ptia(t) for t in range(1, n + 1))
    lapses = sum(p.pols_lapse(t) for t in range(1, n + 1))
    assert deaths == pytest.approx(0.06939268, abs=5e-9)
    assert ptia == pytest.approx(0.00536169, abs=5e-9)
    assert lapses == pytest.approx(0.64637711, abs=5e-9)
    assert p.pols_if(n + 1) == pytest.approx(0.27886852, abs=5e-9)
    assert deaths + ptia + lapses + p.pols_if(n + 1) == pytest.approx(1.0, abs=1e-12)


# ---------------------------------------------------------------------------
# The level-premium variant


@pytest.mark.parametrize("t", sorted(LEVEL_VARIANT))
def test_level_premium_variant_row(temporaire_deces, t):
    """The notes' constante table: only the premium and the commission change."""
    prem_pp, prem, cd, cp, exp, net = LEVEL_VARIANT[t]
    p = temporaire_deces.Projection[2]
    assert p.premium_form() == "constante"
    assert p.prem_pp(t) == pytest.approx(prem_pp, abs=CENT)
    assert p.premiums(t) == pytest.approx(prem, abs=CENT)
    assert p.claims(t, "DEATH") == pytest.approx(cd, abs=CENT)
    assert p.claims(t, "PTIA") == pytest.approx(cp, abs=CENT)
    assert p.expenses(t) == pytest.approx(exp, abs=CENT)
    assert p.net_cf(t) == pytest.approx(net, abs=CENT)


def test_the_level_premium_is_reached_two_independent_ways(temporaire_deces):
    """P_lev = 60 476,2476 / 15,449728 = 3 914,3891, and also a weighted mean of the grid.

    The second route never forms the premium stream: ``P_lev / SA`` is the
    ``v^(t-1) p_tau(t)``-weighted mean of the seventeen grid rates, 2,60959276 %.
    """
    p = temporaire_deces.Projection[2]
    assert p.tariff_prem_pv() == pytest.approx(60476.2476, abs=CENT)
    assert p.tariff_annuity() == pytest.approx(15.449728, abs=5e-7)
    assert p.prem_level_pp() == pytest.approx(3914.3891, abs=5e-5)
    weights = [p.disc_factor(t) * p.pols_tariff(t) for t in range(1, p.proj_len() + 1)]
    mean_rate = sum(w * p.prem_rate(t) for t, w in enumerate(weights, start=1))
    mean_rate /= sum(weights)
    assert mean_rate == pytest.approx(0.0260959276, rel=1e-8)
    assert p.sum_assured() * mean_rate == pytest.approx(3914.3891, abs=5e-5)
    assert p.prem_level_pp() * p.tariff_annuity() == pytest.approx(60476.25, abs=CENT)
    # Model point 3 supplies 3 900,00 EUR instead, so the derivation branch is not taken.
    given = temporaire_deces.Projection[3]
    assert given.level_premium() == 3900.0
    assert all(given.prem_pp(t) == 3900.0 for t in (1, 5, 17))
    assert given.result_cf()["premiums"].sum() < p.result_cf()["premiums"].sum()


# ---------------------------------------------------------------------------
# Pitfalls 1 and 7 -- the cotisation is revisable, and the grid is not smoothed


def test_the_revisable_cotisation_moves_with_attained_age(temporaire_deces, fr_td_anchor):
    """The French default is revisable, not constante -- the notes' first pitfall.

    ``prem_pp(3)/prem_pp(2) = 1,56/1,13 = 1,380531``, and over the whole cover the
    cotisation multiplies by ``r(74)/r(58) = 4,6286`` -- a figure that depends only on the
    grid and not at all on the capital.
    """
    p = fr_td_anchor
    assert p.premium_form() == "revisable"
    assert len({p.prem_pp(t) for t in range(1, 18)}) == 17
    assert p.prem_pp(3) / p.prem_pp(2) == pytest.approx(1.56 / 1.13, rel=1e-12)
    assert p.prem_pp(3) / p.prem_pp(2) == pytest.approx(1.380531, abs=5e-7)
    assert p.prem_pp(1) == pytest.approx(1575.00, abs=CENT)
    assert p.prem_pp(17) == pytest.approx(7290.00, abs=CENT)
    assert p.prem_pp(17) / p.prem_pp(1) == pytest.approx(4.86 / 1.05, rel=1e-12)
    assert p.prem_pp(17) / p.prem_pp(1) == pytest.approx(4.6286, abs=5e-5)
    # Model point 12 is the same cell at 20 000 EUR: the same ratios, 7,5x less money.
    # It is also the notes' expense sensitivity -- a year-one cotisation of 210 EUR
    # against 250 EUR of acquisition expense, so on small capitals the expense assumption
    # and not mortality decides whether the cell is viable.
    small = temporaire_deces.Projection[12]
    assert small.prem_pp(1) == pytest.approx(210.00, abs=CENT)
    assert small.prem_pp(17) / small.prem_pp(1) == pytest.approx(
        p.prem_pp(17) / p.prem_pp(1), rel=1e-12)
    assert small.net_cf(1) < 0.0


def test_the_tariff_grid_is_a_lookup_and_keeps_its_step(temporaire_deces):
    """The +38 % step from 59 to 60 is in the published grid; a fitted curve loses it."""
    table = temporaire_deces.Data.premium_rate_table()
    r59 = float(table.loc[("maif_2019", 59), "prem_rate"])
    r60 = float(table.loc[("maif_2019", 60), "prem_rate"])
    assert r60 / r59 == pytest.approx(1.380531, abs=5e-7)
    assert float(table.loc[("maif_2019", 58), "prem_rate"]) == 0.0105
    assert float(table.loc[("maif_2019", 74), "prem_rate"]) == 0.0486
    # The flat 18-34 entry band is a feature of the card, not a gap in it.
    assert {float(table.loc[("maif_2019", a), "prem_rate"])
            for a in range(18, 35)} == {0.0015}


# ---------------------------------------------------------------------------
# Pitfalls 2, 3 and 4 -- PTIA


def test_the_capital_is_never_paid_twice(fr_td_anchor):
    """PTIA is an acceleration: total claim events cannot exceed the policy.

    And the amounts follow the events exactly but for the first-year suicide withholding:
    ``150 000 x (0,06939268 + 0,00536169) = 11 213,155`` against 11 201,155 paid, a gap of
    12,00 EUR which is precisely ``150 000 x 0,00400 x 0,02``.  That the exclusion is the
    *only* gap is what "acceleration, not addition" means arithmetically.
    """
    p = fr_td_anchor
    n = p.proj_len()
    events = sum(p.pols_death(t) + p.pols_ptia(t) for t in range(1, n + 1))
    paid = sum(p.claims(t, "DEATH") + p.claims(t, "PTIA") for t in range(1, n + 1))
    assert events <= 1.0
    assert p.sum_assured() * events == pytest.approx(11213.155, abs=CENT)
    assert paid == pytest.approx(11201.155, abs=CENT)
    assert p.sum_assured() * events - paid == pytest.approx(12.00, abs=CENT)
    assert (1 - p.suicide_factor(1)) * p.sum_assured() * p.pols_death(1) == (
        pytest.approx(12.00, abs=CENT))


def test_a_ptia_life_leaves_the_in_force(fr_td_anchor):
    """A life removed by the PTIA decrement must not appear in ``l(t+1)``.

    If it did, the closure residual would be positive at every t after the first PTIA
    claim while the cash flows still looked plausible.
    """
    p = fr_td_anchor
    assert p.check_pols_roll_fwd() is True
    assert p.check_decrement_closure() is True
    for t in (1, 7, 8, 17):
        assert p.check_pols_roll_fwd_resid(t) == pytest.approx(0.0, abs=1e-12)
        assert p.check_decrement_closure_resid(t) == pytest.approx(0.0, abs=1e-12)


def test_ptia_cover_stops_before_death_cover(temporaire_deces, fr_td_anchor):
    """A hard gate on the attained age, not a taper, at both extremes of the model points.

    On the anchor cell ``age(8) = ptia_end_age = 65``, so the cover is off for the whole
    of policy year 8 -- ``>=``, not ``>``.  Model point 11 enters at exactly
    ``ptia_end_age`` and never attaches; model point 7 never switches off.
    """
    p = fr_td_anchor
    assert p.ptia_end_age() == 65 and p.cover_end_age() == 75
    assert all(p.ptia_rate(t) > 0.0 for t in range(1, 8))
    assert all(p.ptia_rate(t) == 0.0 for t in range(8, 18))
    assert all(p.claims(t, "PTIA") == 0.0 for t in range(8, 18))
    assert all(p.claims(t, "DEATH") > 0.0 for t in range(8, 18))
    assert p.check_ptia_gate() is True

    never = temporaire_deces.Projection[11]
    assert never.issue_age() == never.ptia_end_age() == 65
    assert never.proj_len() == 10
    assert never.result_cf()["claims_ptia"].sum() == 0.0
    assert never.result_cf()["claims_death"].sum() > 0.0
    assert never.check_ptia_gate() is True

    always = temporaire_deces.Projection[7]
    assert always.ptia_end_age() == always.cover_end_age() == 65
    assert all(always.ptia_rate(t) > 0.0 for t in range(1, always.proj_len() + 1))
    assert always.check_ptia_gate() is True


def test_the_competing_risks_are_dependent_rates_and_therefore_additive(fr_td_anchor):
    """q_d + q_p, not 1 - (1-q_d)(1-q_p): 0.00480000 against 0.00479680 in year 1.

    Immaterial here -- 0,48 EUR of year-one claims per 150 000 EUR of capital -- and
    material at older ages.  The in-force recursion is where the convention shows.
    """
    p = fr_td_anchor
    qd, qp = p.mort_rate(1), p.ptia_rate(1)
    assert qd + qp == pytest.approx(0.00480000, rel=1e-12)
    assert 1.0 - (1.0 - qd) * (1.0 - qp) == pytest.approx(0.00479680, rel=1e-9)
    assert p.pols_if_at(1, "BEF_LAPSE") == pytest.approx(1.0 - qd - qp, rel=1e-12)
    assert p.pols_if(2) == pytest.approx((1.0 - qd - qp) * (1.0 - 0.12), rel=1e-12)


# ---------------------------------------------------------------------------
# Pitfall 5 -- there is no surrender value


def test_a_lapse_pays_nothing_at_any_duration(temporaire_deces, fr_td_anchor):
    """Art. L. 132-23 forbids both rachat and reduction, so the column is zeros.

    The absent names are asserted too: they are exactly what a reader arriving from a US
    model with cash surrender values would add, and every total would still look sane.
    """
    p = fr_td_anchor
    assert all(p.claims(t, "LAPSE") == 0.0 for t in range(1, 18))
    assert (p.result_cf()["claims_lapse"] == 0.0).all()
    assert p.check_no_cash_value() is True
    assert p.pols_lapse(1) > 0.0          # the lapses are real; only the benefit is nil
    names = set(temporaire_deces.Projection.cells) | set(
        temporaire_deces.Projection.refs)
    for absent in ("av_pp_at", "av_at", "prem_to_av_pp", "cv_pp", "surr_charge_rate",
                   "surr_value_pp", "paid_up_factor", "asset_share", "mvr",
                   "claims_surr", "withdrawals", "wd_free_pp"):
        assert absent not in names, absent


# ---------------------------------------------------------------------------
# Pitfall 6 -- the age basis


def test_the_age_basis_is_the_difference_de_millesime(fr_td_anchor):
    """Calendar year less birth year, so age(t) = issue_age + t - 1 and nothing else.

    A one-year shift moves ``prem_pp(1)`` from 1 575,00 EUR (age 58) to 1 695,00 EUR (age
    59) -- a 7,6 % error in year one that compounds through the whole projection.
    """
    p = fr_td_anchor
    assert p.issue_age() == 58
    assert [p.age(t) for t in (1, 2, 17)] == [58, 59, 74]
    assert p.prem_pp(1) == pytest.approx(1575.00, abs=CENT)
    assert p.prem_pp(2) == pytest.approx(1695.00, abs=CENT)
    assert 1695.00 / 1575.00 - 1 == pytest.approx(0.076, abs=0.0005)
    # issue_date is carried and drives nothing: the millesime basis needs only the age.
    assert p.issue_date() == "2026-01-01"


def test_pricing_is_unisex_while_the_model_point_still_carries_sex(temporaire_deces):
    """Art. L. 111-7 forbids sex-based premium and benefit differences.

    Model point 8 is the anchor cell as a woman: same tariff rate, same mortality rate.
    Only the payment frequency differs, which is what actually moves her cotisation.
    """
    male, female = temporaire_deces.Projection[1], temporaire_deces.Projection[8]
    assert male.sex() == "M" and female.sex() == "F"
    assert female.prem_rate(1) == male.prem_rate(1)
    assert female.mort_rate(1) == male.mort_rate(1)
    assert female.benefit_pp(1) == male.benefit_pp(1)
    assert female.prem_pp(1) == pytest.approx(150000 * 0.0105 * 1.04 + 6.0, abs=CENT)


# ---------------------------------------------------------------------------
# Pitfall 8 -- the suicide factor


def test_the_suicide_factor_touches_death_in_year_one_and_nothing_else(
        temporaire_deces, fr_td_anchor):
    """Art. L. 132-7 voids the death cover for suicide in year 1.  PTIA is not death.

    The art. R. 132-5 immediate-cover ceiling of 120 000 EUR belongs to
    principal-residence loan cover; importing it would cap the anchor cell's first-year
    death benefit, so its absence is visible in the numbers and not only in the cells list.
    """
    p = fr_td_anchor
    assert p.suicide_factor(1) == 0.98
    assert all(p.suicide_factor(t) == 1.0 for t in (2, 3, 17))
    assert p.claims(1, "DEATH") == pytest.approx(
        0.98 * p.benefit_pp(1) * p.pols_death(1), rel=1e-12)
    assert p.claims(2, "DEATH") == pytest.approx(
        p.benefit_pp(2) * p.pols_death(2), rel=1e-12)
    assert p.claims(1, "PTIA") == pytest.approx(
        p.benefit_pp(1) * p.pols_ptia(1), rel=1e-12)
    assert p.benefit_death_pp(1) == 150000.0
    assert p.claims(1, "DEATH") / p.pols_death(1) > 120000.0
    names = set(temporaire_deces.Projection.cells) | set(
        temporaire_deces.Projection.refs)
    for absent in ("immediate_cover_cap", "suicide_cover_cap", "loan_cover_cap"):
        assert absent not in names


# ---------------------------------------------------------------------------
# Pitfall 9 and the expense ledger


def test_the_premium_cessation_rule_is_applied_once(fr_td_anchor):
    """Cotisations are in advance and claims at year end, so a claimant has already paid.

    Multiplying ``premiums(t)`` by ``(1 - q_d - q_p)`` as well applies the rule twice and
    understates year-t income by about 0,5 % at the anchor age.
    """
    p = fr_td_anchor
    for t in (1, 5, 17):
        assert p.premiums(t) == pytest.approx(p.prem_pp(t) * p.pols_if(t), rel=1e-12)
    twice = p.prem_pp(1) * p.pols_if(1) * (1 - p.mort_rate(1) - p.ptia_rate(1))
    assert p.premiums(1) - twice == pytest.approx(1575.00 * 0.0048, abs=CENT)


def test_commissions_are_inside_expenses_not_beside_them(fr_td_anchor):
    """expenses(1) = 250 + 25 + 0,72 + 630 = 905,72, and the last term is the commission.

    ``result_cf()`` publishes both columns because the notes' table does, so an
    implementation that also subtracted ``commissions`` from ``net_cf`` would charge it
    twice -- loudest in year one, where the commission is 40 % of the cotisation.
    """
    p = fr_td_anchor
    assert p.commissions(1) == pytest.approx(0.40 * 1575.00, abs=CENT)
    assert p.claim_expenses(1) == pytest.approx(150 * 0.0048, abs=CENT)
    assert p.expenses(1) == pytest.approx(250.0 + 25.0 + 0.72 + 630.0, abs=CENT)
    assert p.net_cf(1) == pytest.approx(
        p.premiums(1) - p.claims(1) - p.expenses(1), rel=1e-12)
    assert (p.result_cf()["commissions"] <= p.result_cf()["expenses"]).all()
    assert p.commissions(2) == pytest.approx(0.05 * p.premiums(2), rel=1e-12)


# ---------------------------------------------------------------------------
# Pitfall 10 -- nothing exists past the age limit


def test_nothing_runs_past_the_age_limit(temporaire_deces, fr_td_anchor):
    """proj_len = cover_end_age - issue_age, and there is no tail state after it.

    No maturity benefit, no renewal, no conversion and no post-level-term phase -- the
    last of which ``Term_US_A`` has and importing it here would invent.  In the final year
    a lapse and an expiry are the same event paying the same nothing, so ``lapse_rate(17)``
    is zero: that is what makes the notes' closure split 64,638 % lapses and 27,887 %
    survivors rather than 66,311 % and 26,214 %, and it changes no cash flow.
    """
    p = fr_td_anchor
    assert p.proj_len() == 75 - 58 == 17
    df = p.result_cf()
    assert list(df.index) == list(range(1, 18))
    assert df.index.name == "t"
    assert p.pols_if(18) == pytest.approx(0.27886852, abs=5e-9)
    assert p.pols_if(19) == 0.0
    assert p.pols_if_at(17, "AFT_DECR") == pytest.approx(p.pols_if(18), rel=1e-12)
    assert p.lapse_rate_base(17) == 0.06 and p.lapse_rate(17) == 0.0
    assert p.pols_lapse(17) == 0.0
    assert p.lapse_rate(16) == pytest.approx(0.06, rel=1e-12) and p.pols_lapse(16) > 0.0
    names = set(temporaire_deces.Projection.cells) | set(
        temporaire_deces.Projection.refs)
    for absent in ("claims_maturity", "pols_maturity", "maturity_benefit_pp",
                   "conv_rate", "renewal_rate", "jump_ratio", "shock_lapse_rate"):
        assert absent not in names


# ---------------------------------------------------------------------------
# Pitfalls 11, 12, 13 and 14


def test_the_two_premium_forms_do_not_collect_the_same_total(temporaire_deces):
    """36 367,46 EUR against 31 999,13 EUR -- correct, not a bug.

    The equivalence ignores lapse, so once lapses truncate the expensive late years the
    level form collects more.  The identity that holds is the discounted one, and not a
    single claim moves.
    """
    rev, lev = temporaire_deces.Projection[1], temporaire_deces.Projection[2]
    rdf, ldf = rev.result_cf(), lev.result_cf()
    assert rdf["premiums"].sum() == pytest.approx(31999.13, abs=CENT)
    for column, total in LEVEL_TOTALS.items():
        assert ldf[column].sum() == pytest.approx(total, abs=CENT), column
    assert (rdf["claims_death"] - ldf["claims_death"]).abs().max() < 1e-9
    assert (rdf["claims_ptia"] - ldf["claims_ptia"]).abs().max() < 1e-9
    assert (rdf["pols_if"] - ldf["pols_if"]).abs().max() < 1e-12
    # The notes' sensitivity: +13,7 % of premium and +18,4 % of net_cf.
    assert ldf["premiums"].sum() / rdf["premiums"].sum() - 1 == pytest.approx(
        0.137, abs=0.001)
    assert ldf["net_cf"].sum() / rdf["net_cf"].sum() - 1 == pytest.approx(0.184, abs=0.001)
    assert lev.prem_level_pp() * lev.tariff_annuity() == pytest.approx(
        rev.tariff_prem_pv(), rel=1e-9)


def test_a_surprime_scales_the_cotisation_and_never_the_capital(temporaire_deces):
    """Model point 5 is the anchor cell at rating_factor 1.50 on a smoker.

    Claims are invariant to it: a *surprime* buys the same capital at a higher price.
    """
    rated, std = temporaire_deces.Projection[5], temporaire_deces.Projection[1]
    assert rated.rating_factor() == 1.5 and rated.smoker() == "S"
    assert rated.prem_pp(1) == pytest.approx(1.5 * std.prem_pp(1), rel=1e-12)
    rdf, sdf = rated.result_cf(), std.result_cf()
    assert (rdf["claims_death"] - sdf["claims_death"]).abs().max() < 1e-9
    assert (rdf["claims_ptia"] - sdf["claims_ptia"]).abs().max() < 1e-9
    assert (rdf["pols_if"] - sdf["pols_if"]).abs().max() < 1e-12
    assert rated.benefit_pp(1) == std.benefit_pp(1)
    assert rdf["premiums"].sum() == pytest.approx(1.5 * sdf["premiums"].sum(), rel=1e-12)


def test_the_fractionation_loading_and_the_fee_are_charges_of_different_kinds(
        temporaire_deces):
    """A multiplier inside the cotisation, plus a fixed euro fee added once.

    Model point 4 is monthly: 200 000 x 0,44 % x 1,04 = 915,20 EUR of loaded cotisation
    plus 18,00 EUR of *frais d'échéance*.  Applying the fee as a further percentage, or
    loading the already-loaded cotisation with it, overstates premium income.
    """
    p = temporaire_deces.Projection[4]
    assert p.prem_freq() == "monthly"
    assert p.prem_freq_load() == 1.04 and p.prem_freq_fee() == 18.0
    assert p.prem_tariff_pp(1) == pytest.approx(200000 * 0.0044 * 1.04, abs=CENT)
    assert p.prem_pp(1) == pytest.approx(915.20 + 18.00, abs=CENT)
    # The fee is flat in t while the loaded cotisation climbs with the grid, and it is
    # charged once a year at every t -- the notes' P(t) = P_tar(t) + F.
    assert p.prem_pp(30) - p.prem_tariff_pp(30) == pytest.approx(18.0, abs=CENT)
    assert all(p.prem_pp(t) - p.prem_tariff_pp(t) == pytest.approx(18.0, abs=CENT)
               for t in range(1, p.proj_len() + 1))
    # It is part of what the policyholder pays, so it reaches premium income and the
    # commission base -- while the constante equivalence is struck on P_tar alone.
    assert p.premiums(1) == pytest.approx(p.prem_pp(1) * p.pols_if(1), rel=1e-12)
    assert p.commissions(2) == pytest.approx(
        0.05 * p.prem_pp(2) * p.pols_if(2), rel=1e-12)
    half = temporaire_deces.Projection[10]
    assert half.prem_freq() == "half_yearly"
    assert half.prem_pp(1) == pytest.approx(250000 * 0.0015 * 1.025 + 3.0, abs=CENT)
    annual = temporaire_deces.Projection[1]
    assert annual.prem_freq_load() == 1.0 and annual.prem_freq_fee() == 0.0


def test_the_accidental_option_is_a_share_and_not_an_uplift(temporaire_deces):
    """It pays an additional capital on the accidental share, not on every claim.

    Model point 6 is model point 1 with the multiplier at 2.00.  With ``acc_share = 0`` --
    no retrieved source gives an accidental share of deaths -- the two frames must be
    identical to the last bit; supply a share and the multiplier starts to matter.
    """
    opt, base = temporaire_deces.Projection[6], temporaire_deces.Projection[1]
    assert opt.accident_multiplier() == 2.0 and base.accident_multiplier() == 1.0
    assert opt.acc_share == 0.0
    assert all(opt.accident_extra_pp(t) == 0.0 for t in range(1, 18))
    assert (opt.result_cf() - base.result_cf()).abs().max().max() == 0.0

    model = mx.read_model(MODEL_DIR, name="TD_FR_A_acc")
    try:
        model.Projection.acc_share = 0.1
        model.Projection.clear_all()
        # (2.00 - 1) x 0.10 x 150 000 = 15 000 EUR of extra capital per claim.
        assert model.Projection[6].accident_extra_pp(1) == pytest.approx(15000.0)
        assert model.Projection[1].accident_extra_pp(1) == 0.0
        assert model.Projection[6].result_cf()["claims_death"].sum() > (
            base.result_cf()["claims_death"].sum())
    finally:
        model.close()


# ---------------------------------------------------------------------------
# The delai d'attente


def test_the_waiting_period_returns_the_cotisations_and_suspends_ptia(temporaire_deces):
    """Model point 9 carries a one-year *délai d'attente* on a 40 000 EUR capital.

    Inside the window an illness-caused death pays back what was paid -- 296,00 EUR, the
    single cotisation collected in advance -- and PTIA pays nothing; from year 2 the full
    capital is at risk again.  The window changes what a claim pays, never who leaves.
    Only this one model point elects one; five of the eight carriers have none.
    """
    p = temporaire_deces.Projection[9]
    assert p.waiting_period_y() == 1
    assert p.in_waiting(1) is True and p.in_waiting(2) is False
    assert p.prem_pp(1) == pytest.approx(296.00, abs=CENT)
    assert p.prem_refund_pp(1) == pytest.approx(296.00, abs=CENT)
    assert p.benefit_death_pp(1) == pytest.approx(296.00, abs=CENT)
    assert p.benefit_ptia_pp(1) == 0.0
    assert p.claims(1, "PTIA") == 0.0
    assert p.claims(1, "DEATH") == pytest.approx(0.98 * 296.00 * p.pols_death(1), abs=CENT)
    assert p.benefit_death_pp(2) == 40000.0
    assert p.claims(2, "PTIA") > 0.0
    assert p.pols_ptia(1) > 0.0            # a benefit is suppressed, not a decrement
    assert p.check_decrement_closure() is True
    table = temporaire_deces.Data.model_point_table()
    assert (table["waiting_period_y"] > 0).sum() == 1
    assert table.loc[1, "waiting_period_y"] == 0


# ---------------------------------------------------------------------------
# Modules that are off in the base run


def test_the_behaviour_modules_are_off_and_reachable(temporaire_deces):
    """Base run values, so the worked example reproduces with the machinery still there."""
    proj = temporaire_deces.Projection
    assert proj.tariff_drift == 0.0
    assert proj.shock_lapse_beta == 0.0 and proj.shock_lapse_g0 == 0.1
    assert proj.sel_lapse_lambda == 0.0 and proj.sel_lapse_ref == 0.3
    assert proj.acc_share == 0.0
    p = temporaire_deces.Projection[1]
    assert all(p.shock_lapse_factor(t) == 1.0 for t in (1, 3, 17))
    assert all(p.sel_lapse_factor(t) == 1.0 for t in (1, 3, 17))
    assert all(p.mort_rate(t) == p.mort_rate_base(t) for t in (1, 3, 17))


def test_the_premium_shock_module_bites_where_the_grid_steps():
    """Switched on, M_shock lifts the lapse rate at t = 3 and nowhere else.

    The grid's +38 % step at age 60 is the only year whose cotisation rise clears the 10 %
    tolerance, which is the whole point of carrying the module on a revisable form.
    """
    model = mx.read_model(MODEL_DIR, name="TD_FR_A_shock")
    try:
        model.Projection.shock_lapse_beta = 1.5
        model.Projection.clear_all()
        p = model.Projection[1]
        assert p.shock_lapse_factor(3) == pytest.approx(
            1.0 + 1.5 * (1.380531 - 1.0 - 0.10), abs=1e-6)
        assert all(p.shock_lapse_factor(t) == 1.0 for t in (1, 2, 4, 5, 10, 16))
        assert p.lapse_rate(3) > 0.08
        assert p.result_cf()["premiums"].sum() < 31999.13
    finally:
        model.close()


def test_the_selective_lapsation_module_loads_persisters():
    """q_d_eff = q_d (1 + lambda max(0, w_cum - w_ref)), off at lambda = 0.

    Cumulative lapse reaches 64,6 % over the worked configuration, so the loading is
    reached and then grows -- larger here than on a UK guaranteed-premium term policy.
    """
    model = mx.read_model(MODEL_DIR, name="TD_FR_A_sel")
    try:
        model.Projection.sel_lapse_lambda = 0.25
        model.Projection.clear_all()
        p = model.Projection[1]
        assert p.lapse_cum(1) == 0.0 and p.sel_lapse_factor(1) == 1.0
        assert p.lapse_cum(17) > 0.30
        assert p.sel_lapse_factor(17) == pytest.approx(
            1.0 + 0.25 * (p.lapse_cum(17) - 0.30), rel=1e-12)
        assert p.mort_rate(17) > p.mort_rate_base(17)
        assert p.check_pols_roll_fwd() is True
        assert p.check_decrement_closure() is True
    finally:
        model.close()


def test_tariff_drift_reprices_the_card_and_nothing_else():
    """A drift assumption is a premium-income assumption, not a mortality one."""
    model = mx.read_model(MODEL_DIR, name="TD_FR_A_drift")
    try:
        model.Projection.tariff_drift = 0.02
        model.Projection.clear_all()
        p = model.Projection[1]
        assert p.prem_rate(1) == pytest.approx(0.0105, rel=1e-12)
        assert p.prem_rate(3) == pytest.approx(0.0156 * 1.02 ** 2, rel=1e-12)
        assert p.mort_rate(3) == pytest.approx(0.00400 * 1.09 ** 2, rel=1e-8)
        assert p.result_cf()["premiums"].sum() > 31999.13
    finally:
        model.close()


# ---------------------------------------------------------------------------
# Structure, documentation and inputs


def test_result_cf_shape_and_both_signs_of_the_net_flow(fr_td_anchor):
    """The notes' eight columns plus liability_cf, the notes' own outgo orientation."""
    df = fr_td_anchor.result_cf()
    assert list(df.index) == list(range(1, 18))
    assert list(df.columns) == [
        "pols_if", "premiums", "claims_death", "claims_ptia", "claims_lapse",
        "expenses", "commissions", "net_cf", "liability_cf",
    ]
    # A cash flow statement must not publish its own subtotal beside its parts.
    assert "claims" not in df.columns
    assert (df["net_cf"] + df["liability_cf"]).abs().max() == pytest.approx(0.0, abs=1e-9)
    outgo = df["claims_death"] + df["claims_ptia"] + df["claims_lapse"] + df["expenses"]
    assert (df["premiums"] - outgo - df["net_cf"]).abs().max() == pytest.approx(
        0.0, abs=1e-9)
    # Almost no new business strain on the revisable form, then thin positive margins.
    assert df["net_cf"].iloc[0] == pytest.approx(-38.72, abs=CENT)
    assert (df["net_cf"].iloc[1:] > 0).all()


def test_invalid_enum_values_raise(fr_td_anchor):
    """The enum accessors validate rather than propagating a typo into a lookup."""
    with pytest.raises(FormulaError):
        fr_td_anchor.claims(1, "SURRENDER")
    with pytest.raises(FormulaError):
        fr_td_anchor.pols_if_at(1, "AFTER_LAPSE")


def test_docstrings_describe_the_current_structure(temporaire_deces):
    """Specifics a reader would rely on, asserted so they cannot go stale silently."""
    doc = temporaire_deces.doc
    assert "temporaire décès" in doc
    assert "mechanics demonstration" in doc
    assert "external" in doc                     # inputs are not stored in the model
    assert "once per model" in doc               # why Data exists
    assert "revisable" in doc and "constante" in doc
    assert "acceleration" in doc
    assert "ADE_FR_S" in doc and "Obseques_FR_S" in doc   # the siblings on this chassis
    proj = temporaire_deces.Projection.doc
    assert "Notes symbol" in proj
    for cells in ("proj_len", "model_point", "prem_pp", "ptia_rate", "suicide_factor",
                  "benefit_death_pp", "lapse_cum", "pols_if_at"):
        assert cells in proj, cells
    data = temporaire_deces.Data.doc
    assert "TradLife_A" in data
    for cells in ("input_dir", "model_point_table", "premium_rate_table",
                  "mort_table"):
        assert cells in data, cells


def test_the_protection_chassis_vocabulary_is_present(temporaire_deces):
    """Names ADE_FR_S and Obseques_FR_S inherit must mean the same thing on all three."""
    shared = {
        "model_point", "proj_len", "age", "pols_if", "pols_if_at", "pols_if_init",
        "pols_death", "pols_ptia", "pols_lapse", "mort_rate", "mort_rate_base",
        "ptia_rate", "lapse_rate", "lapse_rate_base", "lapse_cum", "prem_rate",
        "prem_pp", "premiums", "benefit_pp", "benefit_death_pp", "benefit_ptia_pp",
        "suicide_factor", "claims", "claim_expenses", "commissions", "expenses",
        "inflation_factor", "net_cf", "liability_cf", "result_cf",
    }
    names = set(temporaire_deces.Projection.cells) | set(
        temporaire_deces.Projection.refs)
    assert shared <= names, f"missing: {sorted(shared - names)}"


def test_the_shipped_tables_mark_their_own_provenance():
    """Six CSVs beside run.py, and each says what it is -- especially what it is not.

    The mortality table is a **[std]** proxy -- TH 00-02 / TF 00-02 are cited by name,
    never shipped -- and the anchor a substitute must preserve is the rate at age 58.  The
    tariff grid is the one real French artefact and marks its own entry cap.
    """
    import pandas as pd

    expected = {"model_point_table.csv", "premium_rate_table.csv", "mort_table.csv",
                "lapse_table.csv", "freq_loading_table.csv", "benefit_schedule.csv"}
    assert expected == {p.name for p in MODEL_DIR.parent.iterdir() if p.suffix == ".csv"}

    mort = pd.read_csv(MODEL_DIR.parent / "mort_table.csv", index_col="age")
    assert all(p.startswith("[std]") for p in mort["provenance"])
    assert float(mort.loc[58, "mort_rate"]) == 0.00400
    assert float(mort.loc[59, "mort_rate"]) == pytest.approx(0.00436, rel=1e-9)
    assert mort["mort_rate"].max() <= 1.0
    assert list(mort.index) == list(range(18, 75))
    assert float(mort.loc[74, "mort_rate"]) / float(mort.loc[73, "mort_rate"]) == (
        pytest.approx(1.09, rel=1e-6))

    rates = pd.read_csv(MODEL_DIR.parent / "premium_rate_table.csv")
    assert set(rates["rate_id"]) == {"maif_2019"}
    assert all("entry grid" in p for p in rates[rates["age"] <= 65]["provenance"])
    assert all("en cours de contrat" in p for p in rates[rates["age"] > 65]["provenance"])

    lapse = pd.read_csv(MODEL_DIR.parent / "lapse_table.csv", index_col="policy_year")
    assert list(lapse["lapse_rate"]) == [0.12, 0.10, 0.08, 0.06]
    assert all("no observed range" in p for p in lapse["provenance"])


def test_an_input_can_be_swapped_without_touching_formulas():
    """This is what a production user does with a company or licensed mortality basis."""
    import pandas as pd

    lighter = pd.read_csv(MODEL_DIR.parent / "mort_table.csv", index_col="age")
    lighter["mort_rate"] = lighter["mort_rate"] * 0.5

    model = mx.read_model(MODEL_DIR, name="TD_FR_A_swap")
    try:
        alt_name = "mort_table_light.csv"
        lighter.to_csv(model.Data.input_dir() / alt_name)
        try:
            base = model.Projection[1].result_cf()["claims_death"].sum()
            model.Data.mort_table_file = alt_name
            model.Data.clear_all()
            model.Projection.clear_all()
            # Lighter mortality means fewer death claims and more premium collected.
            assert model.Projection[1].result_cf()["claims_death"].sum() < base
            assert model.Projection[1].result_cf()["premiums"].sum() > 31999.13
        finally:
            (model.Data.input_dir() / alt_name).unlink(missing_ok=True)
    finally:
        model.close()


def test_round_trip_is_stable(tmp_path):
    """read -> write -> re-read reproduces the goldens and the same file set."""
    import shutil

    model = mx.read_model(MODEL_DIR, name="TD_FR_A_rt_src")
    try:
        dest = tmp_path / MODEL_DIR.name
        mx.write_model(model, str(dest), backup=False)
    finally:
        model.close()

    for csv in MODEL_DIR.parent.glob("*.csv"):
        shutil.copy(csv, tmp_path / csv.name)

    reread = mx.read_model(dest, name="TD_FR_A_rt")
    try:
        p = reread.Projection[1]
        for t, row in WORKED_EXAMPLE.items():
            assert p.premiums(t) == pytest.approx(row[3], abs=CENT)
            assert p.claims(t, "DEATH") == pytest.approx(row[4], abs=CENT)
            assert p.net_cf(t) == pytest.approx(row[7], abs=CENT)
        assert "Notes symbol" in reread.Projection.doc
        assert p.check_decrement_closure() is True
    finally:
        reread.close()

    assert model_files(dest) == model_files(MODEL_DIR)
